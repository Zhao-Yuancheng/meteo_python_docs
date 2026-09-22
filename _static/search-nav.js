/* 跳转后正文关键词标黄。
 *
 * pydata-sphinx-theme 在每个内容页也加载了 searchtools.js，
 * 导致 Search 对象始终存在，Sphinx 自带的"SphinxHighlight.highlightSearchWords"
 * 因其内部 `typeof Search === 'undefined'` 判断而永远不会触发。
 * 这里在非搜索页主动调用它：从 localStorage 读取上次检索词并标黄。
 */
/* SphinxHighlight 与 DOCUMENTATION_OPTIONS 都是 Sphinx 生成脚本里的顶层
 * const（经典脚本的全局词法绑定），只能以裸标识符访问，window 上没有。 */
(function () {
  if (typeof SphinxHighlight === "undefined") return;

  var run = function () {
    // 搜索页不执行——否则会高亮上一次搜索的词
    if (
      typeof DOCUMENTATION_OPTIONS === "undefined"
      || DOCUMENTATION_OPTIONS.pagename === "search"
    ) {
      return;
    }

    // 是否从搜索页跳转而来（localStorage 存有检索词），以及是否无 # 锚点
    //（正文检索结果没有锚点；若有锚点则交给浏览器跳到对应章节）
    var fromSearch = !!localStorage.getItem("sphinx_highlight_terms");
    var hasAnchor = window.location.hash.length > 0;

    SphinxHighlight.highlightSearchWords();

    // 焦点定位：把正文里第一个命中的关键词滚动到视野中央
    if (fromSearch && !hasAnchor) {
      setTimeout(function () {
        var root = document.querySelector('[role="main"]') || document.body;
        var el = root.querySelector("span.highlighted");
        if (!el) return;
        try {
          el.scrollIntoView({ block: "center", inline: "nearest" });
        } catch (e) {
          el.scrollIntoView();
        }
      }, 80);
    }
  };

  if (document.readyState !== "loading") {
    run();
  } else {
    document.addEventListener("DOMContentLoaded", run);
  }
})();