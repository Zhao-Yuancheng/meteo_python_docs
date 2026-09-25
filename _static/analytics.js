/* 云笺 CloudDocs —— 访问统计加载器（51LA V6）
   仅在正式域名下加载统计脚本：本地预览（localhost）与 file:// 打开都不计数，
   否则开发期反复刷新会把真实访问量淹没，统计就失去参考价值。
   51LA 后台「安装代码」给出的同步安装片段（两行 script）在此等价实现：
   脚本异步载入后回调 LA.init，采集能力与同步安装一致。 */
(function () {
  var SITE = { id: '3RJJwxuDnuwX8OEr', ck: '3RJJwxuDnuwX8OEr' };
  // 正式域名白名单：日后启用校内域名或自有域名时在此追加
  var DOMAINS = ['zhao-yuancheng.github.io'];
  if (DOMAINS.indexOf(location.hostname) === -1) return;

  var s = document.createElement('script');
  s.id = 'LA_COLLECT';
  s.charset = 'UTF-8';
  s.src = 'https://sdk.51.la/js-sdk-pro.min.js';
  s.onload = function () {
    if (window.LA && window.LA.init) {
      window.LA.init({ id: SITE.id, ck: SITE.ck, autoTrack: true });
    }
  };
  document.head.appendChild(s);
})();