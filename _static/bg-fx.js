/*
 * 云笺 CloudDocs 背景动效（P0 增强版）
 *
 * 功能：
 *  - 背景粒子点 + 近距离连线（球/线已放大 1.5x，密度加密 1.5x），随鼠标柔和牵引；
 *  - 天气面板点击触发小团烟花，独立开关可关；
 *  - 颜色随 pydata 主题 data-theme 亮暗自动切换（莫兰迪灰蓝，近乎背景）；
 *  - 两个开关按钮注入到页眉与小屏侧边栏的主题切换按钮旁（各一份，状态同步），
 *    显隐跟随主题 960px 断点自动切换，各自状态存 localStorage；
 *  - 默认：桌面 + 未声明"减少动效"时开启，触屏/ prefers-reduced-motion 默认关闭；
 *  - 动效层 fixed、pointer-events:none，不拦截选中与点击。
 *
 * 全部为原生 JS，零第三方依赖、零外部请求。
 */
(function () {
  'use strict';

  var KEY_BG = 'meteo_fx';      // 背景粒子开关键
  var KEY_FW = 'meteo_fx_fw';   // 烟花开关键

  /* ---------- 偏好读写 ---------- */
  function media(q) { return window.matchMedia ? window.matchMedia(q) : null; }
  function prefersReduce() {
    var m = media('(prefers-reduced-motion: reduce)');
    return !!(m && m.matches);
  }
  function isFinePointer() {
    var h = media('(hover: hover)');
    var c = media('(pointer: coarse)');
    if (h && !h.matches) return false;
    if (c && c.matches) return false;
    return true;
  }
  function defaultEnabled() {
    if (prefersReduce()) return false;   // 用户声明减少动效 -> 强制关
    return isFinePointer();              // 无精确指针(触屏) -> 默认关(省电)
  }
  function readPref(key) {
    var v = null;
    try { v = localStorage.getItem(key); } catch (e) { /* 隐私模式可能拒绝 */ }
    if (v === '1') return true;
    if (v === '0') return false;
    return defaultEnabled();
  }
  function storePref(key, on) {
    try { localStorage.setItem(key, on ? '1' : '0'); } catch (e) { /* 忽略 */ }
  }

  /* ---------- 亮暗配色（莫兰迪灰蓝，近乎背景） ---------- */
  function currentPalette() {
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    return dark
      ? { p: '205, 219, 238', line: '198, 214, 234' }   // 暗底：浅冷调
      : { p: '88, 106, 130', line: '84, 102, 126' };    // 亮底：低饱和灰蓝
  }

  /* ---------- 背景粒子配置（球/线 ×1.5，密度 ×1.5） ---------- */
  var CFG = {
    dens: 17333,   // 单个粒子铺展面积：×1.5 密度 => 面积 ÷1.5
    max: 96,       // 粒子数量上限 ×1.5
    line: 115,     // 连线距离阈值(px)
    mouseR: 165,   // 鼠标牵引半径
    pA: 0.30,      // 粒子不透明度（近背景）
    lA: 0.14,      // 连线最大不透明度
    pR: 1.5,       // 粒子半径放大 ×1.5
    lineW: 1.5     // 连线粗细放大 ×1.5
  };

  /* ---------- 单击烟花配置 ---------- */
  var FW = {
    count: 46,
    speedMin: 1.7, speedMax: 4.0,   // 初始速度(px/帧)：决定爆裂半径
    grav: 0.11,                     // 重力：明显的下坠抛物线（重力感）
    drag: 0.99,                     // 空气阻力
    lifeMin: 34, lifeMax: 60,       // 粒子寿命(帧)
    rMin: 0.9, rMax: 2.0,           // 拖尾半径
    alphaBase: 0.95
  };
  var FIRE = [                      // 低饱和彩色（r,g,b）
    '213,151,168', '224,170,110', '143,169,201',
    '159,185,138', '201,165,208', '176,196,222'
  ];

  function App() {
    var bgCv, bgCtx, fwCv, fwCtx;
    var W = 0, H = 0, DPR = 1;
    var particles = [], fireworks = [], raf = 0;
    var paused = false;
    var bgOn = readPref(KEY_BG), fwOn = readPref(KEY_FW);
    var mouse = { x: -1e4, y: -1e4, active: false };

    function makeCanvas(id) {
      var cv = document.createElement('canvas');
      cv.id = id;
      cv.setAttribute('aria-hidden', 'true');
      document.body.appendChild(cv);
      return cv;
    }

    function resize() {
      DPR = Math.min(window.devicePixelRatio || 1, 2);
      W = window.innerWidth; H = window.innerHeight;
      [bgCv, fwCv].forEach(function (cv) {
        cv.width = Math.round(W * DPR);
        cv.height = Math.round(H * DPR);
        cv.style.width = W + 'px';
        cv.style.height = H + 'px';
      });
      bgCtx.setTransform(DPR, 0, 0, DPR, 0, 0);
      fwCtx.setTransform(DPR, 0, 0, DPR, 0, 0);
      particles = [];
      var n = Math.min(Math.round(W * H / CFG.dens), CFG.max);
      for (var i = 0; i < n; i++) particles.push(newParticle());
    }
    function newParticle() {
      return {
        x: Math.random() * W, y: Math.random() * H,
        vx: (Math.random() - .5) * .5, vy: (Math.random() - .5) * .5,
        r: (Math.random() * 1.4 + .6) * CFG.pR
      };
    }

    function drawBg() {
      var pal = currentPalette();
      var pr = CFG.mouseR;
      var i, j, p, q, dx, dy, d, k;
      bgCtx.clearRect(0, 0, W, H);

      // 更新粒子 + 鼠标牵引 + 画点
      for (i = 0; i < particles.length; i++) {
        p = particles[i];
        if (mouse.active) {
          dx = mouse.x - p.x; dy = mouse.y - p.y; d = dx * dx + dy * dy;
          if (d < pr * pr && d > 1) {
            d = Math.sqrt(d); k = (1 - d / pr) * 0.05;
            p.vx += (dx / d) * k; p.vy += (dy / d) * k;
          }
        }
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > W) p.vx *= -1;
        if (p.y < 0 || p.y > H) p.vy *= -1;
        p.x = Math.min(W, Math.max(0, p.x));
        p.y = Math.min(H, Math.max(0, p.y));
        bgCtx.beginPath(); bgCtx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        bgCtx.fillStyle = 'rgba(' + pal.p + ', ' + CFG.pA + ')';
        bgCtx.fill();
      }

      // 近距离连线（透明度随距离递减），线宽 ×1.5
      bgCtx.lineWidth = CFG.lineW;
      for (i = 0; i < particles.length; i++) {
        for (j = i + 1; j < particles.length; j++) {
          p = particles[i]; q = particles[j];
          dx = p.x - q.x; dy = p.y - q.y; d = dx * dx + dy * dy;
          if (d < CFG.line * CFG.line) {
            var al = (1 - Math.sqrt(d) / CFG.line) * CFG.lA;
            bgCtx.strokeStyle = 'rgba(' + pal.line + ', ' + al.toFixed(3) + ')';
            bgCtx.beginPath(); bgCtx.moveTo(p.x, p.y); bgCtx.lineTo(q.x, q.y); bgCtx.stroke();
          }
        }
      }
    }

    /* ---------- 单击放烟花 ---------- */
    function fireBurst(x, y) {
      if (!fwOn) return;
      var n = FW.count;
      for (var i = 0; i < n; i++) {
        var a = (i / n) * 2 * Math.PI + Math.random() * 0.35;
        var sp = FW.speedMin + Math.random() * (FW.speedMax - FW.speedMin);
        var L = FW.lifeMin + Math.random() * (FW.lifeMax - FW.lifeMin);
        fireworks.push({
          x: x, y: y,
          vx: Math.cos(a) * sp, vy: Math.sin(a) * sp,
          life: L, maxLife: L,
          r: FW.rMin + Math.random() * (FW.rMax - FW.rMin),
          c: FIRE[(Math.random() * FIRE.length) | 0]
        });
      }
      loop();
    }

    function drawFw() {
      fwCtx.clearRect(0, 0, W, H);
      var alive = [], i, f, t, al;
      for (i = 0; i < fireworks.length; i++) {
        f = fireworks[i];
        f.vx *= FW.drag; f.vy = f.vy * FW.drag + FW.grav;
        f.x += f.vx; f.y += f.vy;
        f.life--; if (f.life <= 0) continue;
        t = f.life / f.maxLife; al = t * t * FW.alphaBase;
        // 拖尾（由前一段到当前位置的短线）
        fwCtx.strokeStyle = 'rgba(' + f.c + ', ' + al.toFixed(3) + ')';
        fwCtx.lineWidth = (f.r * 0.7) * Math.max(0.4, t * 1.8);
        fwCtx.beginPath();
        fwCtx.moveTo(f.x - f.vx * 3, f.y - f.vy * 3);
        fwCtx.lineTo(f.x, f.y);
        fwCtx.stroke();
        // 亮点内核
        fwCtx.fillStyle = 'rgba(255,255,255,' + (t * 0.9).toFixed(3) + ')';
        fwCtx.beginPath(); fwCtx.arc(f.x, f.y, f.r * 0.55 * t, 0, Math.PI * 2); fwCtx.fill();
        alive.push(f);
      }
      fireworks = alive;
    }

    function loop() {
      cancelAnimationFrame(raf);
      if (paused) return;
      if (!bgOn && fireworks.length === 0) return;   // 无动画可画 -> 停
      if (bgOn) drawBg();
      if (fireworks.length) drawFw();
      raf = requestAnimationFrame(loop);
    }

    function setLayer(key, on) {
      if (key === KEY_BG) {
        bgOn = on;
        if (on) loop();
      } else if (key === KEY_FW) {
        fwOn = on;
        if (!on) { fireworks = []; clearFw(); }
        if (on) loop();
      }
    }
    function getOn(key) { return key === KEY_BG ? bgOn : fwOn; }
    function clearFw() { if (fwCtx) fwCtx.clearRect(0, 0, W, H); }

    /* ---------- 事件 ---------- */
    function onMouseMove(e) { mouse.x = e.clientX; mouse.y = e.clientY; mouse.active = true; }
    function onMouseOut(e) { if (!e.relatedTarget) mouse.active = false; }
    function onClick(e) { fireBurst(e.clientX, e.clientY); }
    function onVisibility() { paused = document.hidden; if (!paused) loop(); }
    function onResize() { resize(); if (bgOn || fireworks.length) loop(); }

    window.addEventListener('resize', onResize);
    window.addEventListener('mousemove', onMouseMove, { passive: true });
    document.addEventListener('mousemove', onMouseMove, { passive: true });
    window.addEventListener('mouseout', onMouseOut);
    document.addEventListener('click', onClick);
    document.addEventListener('visibilitychange', onVisibility);

    bgCv = makeCanvas('meteo-fx-canvas');
    bgCtx = bgCv.getContext('2d');
    fwCv = makeCanvas('meteo-fw-canvas');
    fwCtx = fwCv.getContext('2d');
    resize();

    document.body.classList.toggle('meteo-fx-off', !bgOn);
    document.body.classList.toggle('meteo-fw-off', !fwOn);
    loop();

    return {
      getOn: getOn,
      setLayer: setLayer,
      destroy: function () {
        paused = true; cancelAnimationFrame(raf);
        window.removeEventListener('resize', onResize);
        window.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mousemove', onMouseMove);
        window.removeEventListener('mouseout', onMouseOut);
        document.removeEventListener('click', onClick);
        document.removeEventListener('visibilitychange', onVisibility);
        if (bgCv.parentNode) bgCv.parentNode.removeChild(bgCv);
        if (fwCv.parentNode) fwCv.parentNode.removeChild(fwCv);
      }
    };
  }

  /* ---------- 开关定义 ---------- */
  var DEFS = [
    { key: KEY_BG, id: 'meteo-fx-btn', label: '背景粒子开关',
      bodyOff: 'meteo-fx-off',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
            'stroke-width="1.5" stroke-linecap="round">' +
            '<path d="M5 10 L12 6 L19 10" opacity=".35"/>' +
            '<circle cx="5" cy="13" r="1.8"/><circle cx="12" cy="6" r="1.8"/>' +
            '<circle cx="19" cy="13" r="1.8"/><circle cx="12" cy="20" r="1.8"/></svg>' },
    { key: KEY_FW, id: 'meteo-fw-btn', label: '点击烟花开关',
      bodyOff: 'meteo-fw-off',
      icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
            'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M12 3.1c.33 2.6 1.42 4.15 4.1 4.5-2.68.35-3.77 1.9-4.1 4.5' +
            '-.33-2.6-1.42-4.15-4.1-4.5 2.68-.35 3.77-1.9 4.1-4.5z"/>' +
            '<path d="M12 12.4v6.4"/>' +
            '<path d="M9.5 11.2c-2.45 1.95-3.95 4.25-4.45 7.4"/>' +
            '<circle cx="4.9" cy="19" r=".9"/>' +
            '<path d="M14.5 11.2c2.45 1.95 3.95 4.25 4.45 7.4"/>' +
            '<circle cx="19.1" cy="19" r=".9"/>' +
            '<path d="M6.2 4.5c.18 1.52-.8 2.4-2.3 2.6 1.5.2 2.48 1.08 2.3 2.6' +
            '-.18-1.52.8-2.4 2.3-2.6-1.5-.2-2.48-1.08-2.3-2.6z" opacity=".7"/>' +
            '<path d="M17.8 13.8c.18 1.52-.8 2.4-2.3 2.6 1.5.2 2.48 1.08 2.3 2.6' +
            '-.18-1.52.8-2.4 2.3-2.6-1.5-.2-2.48-1.08-2.3-2.6z" opacity=".7"/></svg>' }
  ];

  /* ---------- 在每个主题切换容器旁注入开关（页眉 + 小屏侧边栏各一份） ----------
     pydata 主题在页眉（≥960px 显示）与小屏侧边栏（<960px 显示）各渲染一个
     .theme-switch-container；按钮注入到每个容器旁，显隐由主题 CSS 自动切换，
     同一开关的各枚按钮点击后状态同步。 */
  function setupToggles(app) {
    var hosts = document.querySelectorAll('.theme-switch-container');
    if (!hosts.length) return;
    var btnGroups = DEFS.map(function () { return []; });
    Array.prototype.forEach.call(hosts, function (host, ci) {
      if (!host.parentNode) return;
      var placed = [];
      DEFS.forEach(function (d, i) {
        var item = document.createElement('div');
        item.className = 'navbar-item meteo-fx-nav-item';
        item.setAttribute('title', d.label);

        var btn = document.createElement('button');
        btn.type = 'button';
        btn.id = ci === 0 ? d.id : d.id + '-' + (ci + 1);
        btn.setAttribute('aria-label', d.label);
        btn.innerHTML = d.icon;
        item.appendChild(btn);

        // 与主题切换同排：第 1 个插在它之前，后续依次向后排
        var ref = i === 0 ? host : placed[i - 1].nextSibling;
        host.parentNode.insertBefore(item, ref);

        var on = app.getOn(d.key);
        btn.setAttribute('aria-pressed', String(on));
        btn.classList.toggle('meteo-fx-on', on);
        btnGroups[i].push(btn);
        placed.push(item);
      });
    });
    DEFS.forEach(function (d, i) {
      btnGroups[i].forEach(function (btn) {
        btn.addEventListener('click', function () {
          var next = !app.getOn(d.key);
          storePref(d.key, next);
          app.setLayer(d.key, next);
          btnGroups[i].forEach(function (b) {
            b.setAttribute('aria-pressed', String(next));
            b.classList.toggle('meteo-fx-on', next);
          });
          document.body.classList.toggle(d.bodyOff, !next);
        });
      });
    });
  }

  /* ---------- 初始化 ---------- */
  function boot() {
    if (!document.body) { window.addEventListener('load', boot); return; }
    var app = App();
    setupToggles(app);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();