/* ============================================================
   等压墨迹 · Isobaric Ink —— 云笺 CloudDocs 首页 hero 生成艺术
   ------------------------------------------------------------
   算法哲学见 design/isobaric-ink.md：
   · 流函数 ψ 取 Perlin 噪声，速度场取其旋度（u=∂ψ/∂y, v=−∂ψ/∂x），
     得到无散度风场——二维准地转大气的天性；叠加微弱盛行西风（兰州风系）。
   · 数百个示踪粒子被场平流，低透明度轨迹逐帧累积，如墨在笺上洇开。
   · marching squares 逐格描绘 ψ 等值线——天气图的等压线。
   · 局地极值标记 G（高压）/ D（低压），中国天气图记法。
   · 固定种子 10383（兰州经度 103.83°E）：同一颗种子同一幅图，
     如同确定性数值预报。
   工程约束：p5 实例模式；主题切换重绘（MutationObserver）；
   IntersectionObserver 离屏暂停；prefers-reduced-motion 定格为
   预积分的静态完成品。
   ============================================================ */
(function () {
  'use strict';

  var HOST_ID = 'mh-canvas-host';
  var SEED = 10383;        // 兰州经度
  var NS = 0.0032;         // 噪声空间尺度
  var TSTEP = 0.0032;      // 时间演化步长（天气尺度，缓慢生消）
  var DRIFT = 0.12;        // 盛行西风分量（向东）
  var K = 330;             // 平流速度尺度
  var VMAX = 1.9;          // 单步位移上限 px
  var FADE = 8 / 255;      // 每帧褪色——墨迹将干未干
  var INK_A = 38;          // 笔迹透明度（单次经过）
  var ISO_A = 14;          // 等压线单帧透明度（累积至半实）
  var ISO_STEP = 20;       // 等值线网格步长 px
  var LEVELS = [0.28, 0.36, 0.44, 0.52, 0.60, 0.68, 0.76];
  var REDUCED = !!(window.matchMedia
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  /* 莫兰迪墨色：亮=纸上青灰墨，暗=夜空微光笔；末位为暖灰（气团变化） */
  var THEMES = {
    light: {
      bgA: [238, 242, 246], bgB: [224, 231, 238],
      inks: [[58, 84, 114], [92, 119, 149], [128, 150, 172],
             [163, 180, 195], [148, 127, 106]],
      weights: [0.20, 0.30, 0.25, 0.12, 0.13],
      iso: [110, 130, 152],
      markG: [74, 115, 150], markD: [169, 117, 107]
    },
    dark: {
      bgA: [27, 34, 44], bgB: [18, 23, 31],
      inks: [[150, 185, 222], [120, 155, 195], [96, 126, 162],
             [74, 100, 132], [176, 152, 124]],
      weights: [0.26, 0.30, 0.22, 0.10, 0.12],
      iso: [120, 148, 180],
      markG: [128, 168, 203], markD: [203, 148, 138]
    }
  };

  function themeNow() {
    return document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
  }

  function boot() {
    var host = document.getElementById(HOST_ID);
    if (!host || typeof p5 === 'undefined') { return; }

    var T = THEMES[themeNow()];
    var W = 0, H = 0, t = 13.7;
    var parts = [], markers = [];
    var frames = 0, visible = true, running = false;

    var sketch = function (p) {
      /* —— 场 —— */
      function psi(x, y) {
        return p.noise(x * NS + 11.3, y * NS + 5.7, t + 37.2);
      }
      function vel(x, y) {
        var e = 2.4;
        var dpx = psi(x + e, y) - psi(x - e, y);
        var dpy = psi(x, y + e) - psi(x, y - e);
        var u = dpy / (2 * e) * K + DRIFT;   // u = ∂ψ/∂y + 西风
        var v = -dpx / (2 * e) * K;          // v = −∂ψ/∂x
        var s = Math.sqrt(u * u + v * v);
        if (s > VMAX) { u *= VMAX / s; v *= VMAX / s; }
        return [u, v];
      }

      /* —— 示踪粒子 —— */
      function pickInk() {
        var r = p.random(), acc = 0, ws = T.weights;
        for (var i = 0; i < ws.length; i++) { acc += ws[i]; if (r < acc) return i; }
        return 1;
      }
      function spawn(pa) {
        var fromWest = p.random() < 0.35;    // 西风入流
        pa.x = fromWest ? -4 : p.random(-4, W + 4);
        pa.y = p.random(0, H);
        pa.px = pa.x; pa.py = pa.y;
        pa.life = 140 + p.random(260);
        pa.ink = T.inks[pickInk()];
        return pa;
      }
      function initParts() {
        var n = Math.max(140, Math.min(480, Math.round(W * H / 2400)));
        parts = [];
        for (var i = 0; i < n; i++) { parts.push(spawn({})); }
      }

      /* —— 底色 / 褪色 —— */
      function grad() {
        var g = p.drawingContext.createLinearGradient(0, 0, 0, H);
        g.addColorStop(0, 'rgb(' + T.bgA.join(',') + ')');
        g.addColorStop(1, 'rgb(' + T.bgB.join(',') + ')');
        return g;
      }
      function repaint() {
        p.noStroke();
        var ctx = p.drawingContext;
        ctx.globalAlpha = 1;
        ctx.fillStyle = grad();
        ctx.fillRect(0, 0, W, H);
      }
      function fade() {
        var ctx = p.drawingContext;
        ctx.globalAlpha = FADE;
        ctx.fillStyle = grad();
        ctx.fillRect(0, 0, W, H);
        ctx.globalAlpha = 1;
      }

      /* —— 等压线：marching squares —— */
      function drawIsobars() {
        var cols = Math.ceil(W / ISO_STEP), rows = Math.ceil(H / ISO_STEP);
        var stride = cols + 1, g = new Array(stride * (rows + 1));
        for (var j = 0; j <= rows; j++) {
          for (var i = 0; i <= cols; i++) {
            g[j * stride + i] = psi(i * ISO_STEP, j * ISO_STEP);
          }
        }
        p.noFill();
        p.stroke(T.iso[0], T.iso[1], T.iso[2], ISO_A);
        p.strokeWeight(1);
        for (var j2 = 0; j2 < rows; j2++) {
          for (var i2 = 0; i2 < cols; i2++) {
            var a = g[j2 * stride + i2], b = g[j2 * stride + i2 + 1],
                c = g[(j2 + 1) * stride + i2 + 1], d = g[(j2 + 1) * stride + i2];
            for (var L = 0; L < LEVELS.length; L++) {
              var v = LEVELS[L];
              var id = (a > v ? 8 : 0) | (b > v ? 4 : 0)
                     | (c > v ? 2 : 0) | (d > v ? 1 : 0);
              if (id === 0 || id === 15) { continue; }
              drawCell(id, v, a, b, c, d,
                       i2 * ISO_STEP, j2 * ISO_STEP);
            }
          }
        }
      }
      function drawCell(id, v, a, b, c, d, x0, y0) {
        var s = ISO_STEP, x1 = x0 + s, y1 = y0 + s;
        function pt(e) {
          var k;
          switch (e) {
            case 0: k = (v - a) / ((b - a) || 1e-9); return [x0 + s * k, y0];
            case 1: k = (v - b) / ((c - b) || 1e-9); return [x1, y0 + s * k];
            case 2: k = (v - d) / ((c - d) || 1e-9); return [x0 + s * k, y1];
            default: k = (v - a) / ((d - a) || 1e-9); return [x0, y0 + s * k];
          }
        }
        var SEG = {
          1: [[3, 2]], 2: [[2, 1]], 3: [[3, 1]], 4: [[0, 1]],
          5: [[0, 3], [2, 1]], 6: [[0, 2]], 7: [[0, 3]],
          8: [[0, 3]], 9: [[0, 2]], 10: [[0, 1], [3, 2]],
          11: [[0, 1]], 12: [[3, 1]], 13: [[2, 1]], 14: [[3, 2]]
        };
        var segs = SEG[id];
        for (var q = 0; q < segs.length; q++) {
          var p1 = pt(segs[q][0]), p2 = pt(segs[q][1]);
          p.line(p1[0], p1[1], p2[0], p2[1]);
        }
      }

      /* —— 高低压中心：G / D（中国天气图记法）—— */
      function findMarkers() {
        var step = 30, cols = Math.floor(W / step), rows = Math.floor(H / step);
        var found = [];
        for (var j = 2; j < rows - 2; j++) {
          for (var i = 2; i < cols - 2; i++) {
            var v = psi(i * step, j * step);
            var isMax = true, isMin = true;
            for (var dj = -1; dj <= 1; dj++) {
              for (var di = -1; di <= 1; di++) {
                if (!di && !dj) { continue; }
                var w = psi((i + di) * step, (j + dj) * step);
                if (w >= v) { isMax = false; }
                if (w <= v) { isMin = false; }
              }
            }
            if (isMax || isMin) {
              found.push({ x: i * step, y: j * step, v: v, max: isMax });
            }
          }
        }
        /* 取极值最显著的高/低压各至多 2 个，彼此相距 ≥ 130px */
        found.sort(function (m1, m2) {
          return Math.abs(m2.v - 0.5) - Math.abs(m1.v - 0.5);
        });
        var kept = [];
        for (var q = 0; q < found.length && kept.length < 4; q++) {
          var m = found[q], ok = true;
          for (var r = 0; r < kept.length; r++) {
            var dx = kept[r].x - m.x, dy = kept[r].y - m.y;
            if (Math.sqrt(dx * dx + dy * dy) < 130) { ok = false; break; }
          }
          if (ok && kept.filter(function (k) { return k.max === m.max; }).length >= 2) {
            ok = false;
          }
          if (ok) { kept.push(m); }
        }
        markers = kept;
      }
      function drawMarkers() {
        p.strokeWeight(1.3);
        p.textAlign(p.CENTER, p.CENTER);
        p.textFont('Consolas, "Courier New", monospace');
        p.textSize(12);
        for (var q = 0; q < markers.length; q++) {
          var m = markers[q];
          var col = m.max ? T.markG : T.markD;
          p.noFill();
          p.stroke(col[0], col[1], col[2], 16);
          p.ellipse(m.x, m.y, 21, 21);
          p.noStroke();
          p.fill(col[0], col[1], col[2], 22);
          p.text(m.max ? 'G' : 'D', m.x, m.y + 0.5);
        }
      }

      /* —— 逐帧：褪色 → 等压线 → 标记 → 平流示踪 —— */
      function frame() {
        t += TSTEP;
        fade();
        drawIsobars();
        drawMarkers();
        p.strokeWeight(1.15);
        for (var i = 0; i < parts.length; i++) {
          var pa = parts[i];
          var uv = vel(pa.x, pa.y);
          pa.px = pa.x; pa.py = pa.y;
          pa.x += uv[0]; pa.y += uv[1];
          pa.life -= 1;
          if (pa.life <= 0 || pa.x < -6 || pa.x > W + 6
              || pa.y < -6 || pa.y > H + 6) {
            spawn(pa);
            continue;
          }
          p.stroke(pa.ink[0], pa.ink[1], pa.ink[2], INK_A);
          p.line(pa.px, pa.py, pa.x, pa.y);
        }
        frames += 1;
        if (frames % 150 === 1) { findMarkers(); }
      }

      /* —— p5 生命周期 —— */
      p.setup = function () {
        var rect = host.getBoundingClientRect();
        W = Math.round(rect.width);
        H = Math.round(rect.height);
        if (W < 40 || H < 40) { H = 380; }
        p.createCanvas(W, H);
        p.pixelDensity(Math.min(window.devicePixelRatio || 1, 2));
        p.randomSeed(SEED);
        p.noiseSeed(SEED);
        p.noSmooth();
        initParts();
        findMarkers();
        repaint();
        if (REDUCED) {
          for (var i = 0; i < 260; i++) { frame(); }
          p.noLoop();
        } else {
          running = true;
        }
      };
      p.draw = frame;

      /* 尺寸变化：重设画布并重新落墨 */
      p.windowResized = null;
      function applySize() {
        var rect = host.getBoundingClientRect();
        var w = Math.round(rect.width), h = Math.round(rect.height);
        if (Math.abs(w - W) < 2 && Math.abs(h - H) < 2) { return; }
        W = w; H = h;
        p.resizeCanvas(W, H);
        p.randomSeed(SEED);
        p.noiseSeed(SEED);
        initParts();
        findMarkers();
        repaint();
        if (REDUCED) { for (var i = 0; i < 260; i++) { frame(); } }
      }

      /* 主题切换：换墨色重绘 */
      function retheme() {
        var now = THEMES[themeNow()];
        if (now === T) { return; }
        T = now;
        for (var i = 0; i < parts.length; i++) {
          parts[i].ink = T.inks[pickInk()];
        }
        repaint();
        if (REDUCED) { for (var q = 0; q < 260; q++) { frame(); } }
      }
      new MutationObserver(retheme).observe(
        document.documentElement,
        { attributes: true, attributeFilter: ['data-theme'] });

      /* 离屏 / 后台暂停 */
      function sync() {
        if (REDUCED) { return; }
        var want = visible && !document.hidden;
        if (want && !running) { running = true; p.loop(); }
        else if (!want && running) { running = false; p.noLoop(); }
      }
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (en) {
          visible = en[0].isIntersecting;
          sync();
        }).observe(host);
      }
      document.addEventListener('visibilitychange', sync);

      /* 容器尺寸变化（侧栏开合 / 窗口缩放），去抖 */
      var rzT = null;
      if ('ResizeObserver' in window) {
        new ResizeObserver(function () {
          clearTimeout(rzT);
          rzT = setTimeout(applySize, 160);
        }).observe(host);
      } else {
        window.addEventListener('resize', function () {
          clearTimeout(rzT);
          rzT = setTimeout(applySize, 160);
        });
      }
    };

    new p5(sketch, host);
  }

  if (document.readyState !== 'loading') { boot(); }
  else { document.addEventListener('DOMContentLoaded', boot); }
})();
