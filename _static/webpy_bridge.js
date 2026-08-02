// 气象 + Python 文档：在线运行器桥接脚本
// 作用：1) 注入悬浮 WebPy iframe；2) 给 Python 代码块加"运行"按钮；3) postMessage 送码。
(function () {
  'use strict';

  function init() {
    // 用 Sphinx 注入的 URL_ROOT 拼出同源运行器地址，兼容任意页面深度
    var root = (typeof DOCUMENTATION_OPTIONS !== 'undefined' && DOCUMENTATION_OPTIONS.URL_ROOT) || '';
    var webpySrc = root + '_static/webpy/index.html';

    // ① 悬浮运行器面板
    var panel = document.createElement('div');
    panel.id = 'webpy-panel';
    panel.innerHTML =
      '<div id="webpy-bar"><span>🐍 在线 Python 运行器</span>' +
      '<button id="webpy-toggle" title="收起/展开">—</button></div>' +
      '<iframe id="webpy-frame" src="' + webpySrc + '" title="WebPy Runner"></iframe>';
    document.body.appendChild(panel);

    var frame = document.getElementById('webpy-frame');
    var toggle = document.getElementById('webpy-toggle');
    var collapsed = false;
    toggle.addEventListener('click', function () {
      collapsed = !collapsed;
      panel.classList.toggle('collapsed', collapsed);
      toggle.textContent = collapsed ? '▢' : '—';
    });
    window.addEventListener('message', function (e) {
      if (e.data && e.data.type === 'webpyReady') {
        panel.setAttribute('data-ready', '1');
      }
    });

    // ② 给 Python 代码块注入"运行"按钮
    function addRunButtons() {
      var blocks = document.querySelectorAll('.highlight-python, .highlight-default');
      blocks.forEach(function (wrap) {
        if (wrap.querySelector('.webpy-run-btn')) return;
        var pre = wrap.querySelector('pre');
        if (!pre) return;
        var btn = document.createElement('button');
        btn.className = 'webpy-run-btn';
        btn.type = 'button';
        btn.textContent = '▶ 运行';
        btn.title = '把这段代码送进在线运行器执行';
        wrap.style.position = 'relative';
        btn.addEventListener('click', function () {
          var code = pre.textContent.replace(/\u00a0/g, ' ');
          if (collapsed) toggle.click();
          frame.contentWindow.postMessage({ type: 'runCode', code: code }, '*');
          panel.classList.add('flash');
          setTimeout(function () { panel.classList.remove('flash'); }, 600);
        });
        wrap.appendChild(btn);
      });
    }

    addRunButtons();
    setTimeout(addRunButtons, 800); // 兜底：sphinx-gallery 异步内容
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
