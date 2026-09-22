/*
 * 云笺 CloudDocs 正文字号调节（7 档滑杆）
 *
 * 功能：
 *  - 「A±」按钮注入到页眉与小屏侧边栏的主题切换旁（pydata 主题两处
 *    .theme-switch-container，显隐跟随主题 960px 断点自动切换）；
 *  - 点击按钮弹出滑杆面板，拖动实时生效；同时打开的面板只保留一个；
 *  - 档位以 ×1.125 为中心：0.75 / 0.875 / 1.0 / 1.125(默认) / 1.25 / 1.375 / 1.5；
 *  - 同时缩放正文与侧边栏目录（覆盖 4 个 CSS 变量），标题字号不受影响；
 *  - 所选档位存 localStorage（meteo_font_scale），多实例面板状态同步；
 *  - build.py 另在 <head> 注入早期脚本提前应用偏好，避免渲染后字体跳变；
 *    这里在 DOM 就绪后幂等重设一次，兼容未注入早期脚本的旧缓存页。
 *
 * 零依赖、零外部请求；按钮复用 .meteo-fx-nav-item 图标按钮样式。
 */
(function () {
  'use strict';

  var KEY = 'meteo_font_scale';
  var DEFAULT_IDX = 4;                       // 第 4 档 = ×1.125
  var SCALES = [0.75, 0.875, 1.0, 1.125, 1.25, 1.375, 1.5];
  var NAMES  = ['特小', '偏小', '标准', '适中', '较大', '大', '特大'];

  /* ---------- 偏好读写 ---------- */
  function readIdx() {
    var i = null;
    try { i = parseInt(localStorage.getItem(KEY) || '', 10); } catch (e) { /* 忽略 */ }
    return (i >= 1 && i <= SCALES.length) ? i : DEFAULT_IDX;
  }
  function storeIdx(i) {
    try { localStorage.setItem(KEY, String(i)); } catch (e) { /* 忽略 */ }
  }

  /* ---------- 应用档位：在 <html> 上内联覆盖字号变量 ---------- */
  function rem(x) { return (Math.round(x * 10000) / 10000) + 'rem'; }

  function apply(idx) {
    var v = SCALES[idx - 1];
    var s = document.documentElement.style;
    s.setProperty('--bs-body-font-size', rem(v));
    s.setProperty('--pst-sidebar-font-size', rem(0.9 * v));
    s.setProperty('--pst-sidebar-font-size-mobile', rem(1.1 * v));
    s.setProperty('--pst-sidebar-header-font-size', rem(1.2 * v));
  }

  /* ---------- 页眉控件（多实例：页眉 + 小屏侧边栏） ---------- */
  var ICON =
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M2.8 18.6 L8.2 5.8 L13.6 18.6"/>' +   /* “A”两斜 */
    '<path d="M5.0 14.2 L11.4 14.2"/>' +            /* “A”横 */
    '<path d="M16.6 10.2 h5.6"/>' +                 /* “+”横 */
    '<path d="M19.4 7.4 v5.6"/>' +                  /* “+”竖 */
    '<path d="M16.6 16.6 h5.6"/></svg>';            /* “−”横 */

  var instances = [];   // { item, btn, panel, range, curLabel, open }

  function syncAll(idx) {
    instances.forEach(function (t) {
      if (t.range) t.range.value = String(idx);
      if (t.curLabel) {
        var pct = (SCALES[idx - 1] * 100).toFixed(1).replace(/\.0$/, '');
        t.curLabel.textContent = pct + '% ' + NAMES[idx - 1];
      }
      if (t.btn) t.btn.classList.toggle('meteo-fx-on', idx !== DEFAULT_IDX);
    });
  }

  function setPanel(t, on) {
    t.open = on;
    if (t.panel) t.panel.style.display = on ? 'block' : 'none';
    if (t.btn) t.btn.setAttribute('aria-expanded', String(on));
    if (on && t.range && t.range.focus) {
      try { t.range.focus({ preventScroll: true }); } catch (e) { /* 忽略 */ }
    }
  }
  function closeAll() {
    instances.forEach(function (t) { setPanel(t, false); });
  }
  function togglePanel(t) {
    var next = !t.open;
    closeAll();
    if (next) setPanel(t, true);
  }

  function onDocClick(e) {
    for (var k = 0; k < instances.length; k++) {
      if (instances[k].open && instances[k].item.contains(e.target)) return;
    }
    closeAll();
  }
  function onKey(e) {
    if (e.key === 'Escape') closeAll();
  }

  function buildUI(host, ci) {
    var item = document.createElement('div');
    item.className = 'navbar-item meteo-fx-nav-item meteo-fs-nav-item';
    item.setAttribute('title', '正文字号');

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.id = ci === 0 ? 'meteo-fs-btn' : 'meteo-fs-btn-' + (ci + 1);
    btn.setAttribute('aria-label', '调节正文字号');
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = ICON;
    item.appendChild(btn);

    var panel = document.createElement('div');
    panel.className = 'meteo-fs-pop';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', '正文字号调节');
    panel.style.display = 'none';
    panel.innerHTML =
      '<div class="meteo-fs-head"><span>正文字号</span>' +
      '<span class="meteo-fs-cur"></span></div>' +
      '<input type="range" class="meteo-fs-range" min="1" max="' +
      SCALES.length + '" step="1" aria-label="字号档位">' +
      '<div class="meteo-fs-ends"><span>小</span><span>大</span></div>' +
      '<div class="meteo-fs-hint">默认 112.5% · 标准 100%</div>';
    item.appendChild(panel);

    var t = {
      item: item,
      btn: btn,
      panel: panel,
      range: panel.querySelector('.meteo-fs-range'),
      curLabel: panel.querySelector('.meteo-fs-cur'),
      open: false
    };

    // 插到这排开关的最前面（A± 在背景粒子 / 烟花 / 主题切换 之前）
    var first = host.parentNode.querySelector('.meteo-fx-nav-item');
    host.parentNode.insertBefore(item, first || host);

    btn.addEventListener('click', function () { togglePanel(t); });

    t.range.addEventListener('input', function () {
      var i = parseInt(t.range.value, 10);
      storeIdx(i);
      apply(i);
      syncAll(i);
    });

    instances.push(t);
  }

  /* ---------- 初始化 ---------- */
  function boot() {
    if (!document.body) { window.addEventListener('load', boot); return; }
    var idx = readIdx();
    apply(idx);
    var hosts = document.querySelectorAll('.theme-switch-container');
    Array.prototype.forEach.call(hosts, function (h, ci) {
      if (h.parentNode) buildUI(h, ci);
    });
    syncAll(idx);
    document.addEventListener('click', onDocClick);
    document.addEventListener('keydown', onKey);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
