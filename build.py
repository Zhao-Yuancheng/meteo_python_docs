# -*- coding: utf-8 -*-
"""气象 + Python 编程文档 —— 一键构建脚本。

用法（在 P312 环境下）：
    python build.py            # 增量构建
    python build.py --clean    # 先清空再全量构建
    python build.py --serve    # 构建后启动本地预览服务器

脚本会：
  1. 自动把 conda 环境的 Library/bin 加入 PATH（修复 Windows 下 DLL 找不到的问题）。
  2. 调用 sphinx-build 编译 HTML 到 _build/html。
"""
import os
import hashlib
import subprocess
import sys
import argparse
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))


def setup_conda_path():
    """把 conda 环境的 Library/bin 等目录加入 PATH。

    Windows 上，直接调用 python.exe 时不会自动激活 conda 环境，
    导致 numpy / matplotlib 等含 C 扩展的库找不到 DLL 而崩溃。
    此函数检测当前解释器是否在 conda 环境中，并补全 PATH。
    """
    python_dir = os.path.dirname(sys.executable)          # .../envs/P312
    env_dir = os.path.dirname(python_dir)                  # .../envs
    extra_dirs = [
        os.path.join(python_dir, 'Library', 'mingw-w64', 'bin'),
        os.path.join(python_dir, 'Library', 'bin'),
        os.path.join(python_dir, 'Scripts'),
        os.path.join(python_dir, 'bin'),
        python_dir,
    ]
    existing = set(os.environ.get('PATH', '').split(os.pathsep))
    additions = [d for d in extra_dirs if os.path.isdir(d) and d not in existing]
    if additions:
        os.environ['PATH'] = os.pathsep.join(additions) + os.pathsep + os.environ.get('PATH', '')
        print(f'[build] 已补充 PATH: {additions[0]} ...' if len(additions) > 1
              else f'[build] 已补充 PATH: {additions[0]}')


def build(clean=False):
    setup_conda_path()
    # 用户级 site-packages 里装有一份与 conda 环境冲突的 shapely，
    # 会让 cartopy 画廊示例在导入 shapely.lib 时 DLL 加载失败。
    # 构建期间统一禁用用户 site，改用 conda 环境的包（子进程会继承该环境变量）。
    os.environ['PYTHONNOUSERSITE'] = '1'

    args = [sys.executable, '-m', 'sphinx']
    if clean:
        # 全量重建：Sphinx 的 -E 忽略环境缓存、-a 重读全部源文件并删除
        # 已不再生成的历史文件。不整目录 rmtree —— _build/html 下可能内嵌
        # .git（只读文件会抛 PermissionError，且删除会丢构建站点的版本历史）。
        args += ['-E', '-a']
    args += ['-b', 'html', HERE, os.path.join(HERE, '_build', 'html')]
    print('[build] 运行:', ' '.join(args))
    rc = subprocess.call(args, cwd=HERE)
    if rc != 0:
        sys.exit(rc)
    print('[build] 完成 -> _build/html/index.html')
    patch_search_stemmer()
    build_search_snippets()
    patch_search_results()
    patch_search_searchtools()
    patch_font_scale_early()
    patch_theme_sync()
    patch_logo_dark()
    patch_cachebust()


# 注入到每个 HTML 页面 <head> 的早期脚本：页面渲染前读取字号偏好并立即生效，
# 避免正文先按 CSS 默认档（×1.125）渲染、等页脚 font-scale.js 加载后再跳变。
# 档位表与 _static/font-scale.js 保持一致（1–7 档，默认第 4 档 ×1.125）。
_FONT_EARLY_JS = """<script id="meteo-fs-early">\
/* 正文字号偏好提前应用（面板控件见 font-scale.js） */
(function(){try{var i=parseInt(localStorage.getItem('meteo_font_scale')||'',10);\
if(!(i>=1&&i<=7))i=4;if(i!==4){var v=[.75,.875,1,1.125,1.25,1.375,1.5][i-1],\
s=document.documentElement.style,q=function(x){return(Math.round(x*10000)/10000)+'rem'};\
s.setProperty('--bs-body-font-size',q(v));\
s.setProperty('--pst-sidebar-font-size',q(.9*v));\
s.setProperty('--pst-sidebar-font-size-mobile',q(1.1*v));\
s.setProperty('--pst-sidebar-header-font-size',q(1.2*v));}}catch(e){}})();
</script>"""


def patch_font_scale_early():
    """向所有 HTML 页面的 </head> 前注入字号偏好早期脚本（幂等）。"""
    root = os.path.join(HERE, '_build', 'html')
    if not os.path.isdir(root):
        print('[build] 跳过字号早期脚本注入（_build/html 不存在）')
        return
    skip_dirs = {'_static', '_sources', '_modules', '.git'}
    n_patched = n_done = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in filenames:
            if not fn.endswith('.html'):
                continue
            full = os.path.join(dirpath, fn)
            try:
                with open(full, 'r', encoding='utf-8') as f:
                    content = f.read()
            except OSError:
                continue
            if 'meteo-fs-early' in content:
                n_done += 1
                continue
            if '</head>' not in content:
                continue
            patched = content.replace('</head>', _FONT_EARLY_JS + '</head>', 1)
            try:
                with open(full, 'w', encoding='utf-8') as f:
                    f.write(patched)
                n_patched += 1
            except OSError:
                continue
    print(f'[build] 字号早期脚本: 新注入 {n_patched} 页，已就绪 {n_done} 页')


# 注入到每个 HTML 页面 <head> 的主题同步脚本：pydata 主题的初始内联脚本只在
# 首次加载执行，页面经 bfcache（前进/后退）恢复时不重跑——在关于页（或其它
# 页签）切换主题后返回文档页，文档页仍停在旧主题。此脚本注册 pageshow /
# storage 监听，按 pydata 同一规则（mode 优先，auto 回退系统偏好）重读
# localStorage 并重应用 data-theme，只更新属性不写回存储。
_THEME_SYNC_JS = """<script id="meteo-theme-sync">
/* 主题同步：bfcache 恢复(pageshow)与跨页签改动(storage)时重读本地偏好 */
(function(){
  function r(){var m=null;
    try{m=localStorage.getItem('mode');}catch(e){}
    if(m!=='light'&&m!=='dark')m='auto';
    var d=window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches;
    return{mode:m,theme:m==='auto'?(d?'dark':'light'):m};}
  function a(){var s=r(),el=document.documentElement;
    el.dataset.mode=s.mode;el.dataset.theme=s.theme;
    document.querySelectorAll('.dropdown-menu').forEach(function(x){
      x.classList.toggle('dropdown-menu-dark',s.theme==='dark');});
    document.querySelectorAll('.theme-change-button').forEach(function(b){
      b.classList.toggle('active',b.dataset.mode===s.mode);});}
  window.addEventListener('pageshow',a);
  window.addEventListener('storage',function(e){
    if(e.key==='mode'||e.key==='theme')a();});
})();
</script>"""


def patch_theme_sync():
    """向所有 HTML 页面注入主题重同步脚本（幂等）。"""
    root = os.path.join(HERE, '_build', 'html')
    if not os.path.isdir(root):
        print('[build] 跳过主题同步脚本注入（_build/html 不存在）')
        return
    skip_dirs = {'_static', '_sources', '_modules', '.git'}
    n_patched = n_done = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in filenames:
            if not fn.endswith('.html'):
                continue
            full = os.path.join(dirpath, fn)
            try:
                with open(full, 'r', encoding='utf-8') as f:
                    content = f.read()
            except OSError:
                continue
            if 'meteo-theme-sync' in content:
                n_done += 1
                continue
            if '</head>' not in content:
                continue
            patched = content.replace('</head>', _THEME_SYNC_JS + '</head>', 1)
            try:
                with open(full, 'w', encoding='utf-8') as f:
                    f.write(patched)
                n_patched += 1
            except OSError:
                continue
    print(f'[build] 主题同步脚本: 新注入 {n_patched} 页，已就绪 {n_done} 页')


# 自定义静态资源：构建后按内容哈希重写页面中的 ?v= 指纹。
# Sphinx 增量构建不重写未变更页面，页面上这些资源的 ?v= 摘要会停留在旧值，
# 资源内容更新后浏览器仍按旧 URL 命中缓存（曾导致旧脚本在新构建下运行）。
_CACHEBUST_ASSETS = ['bg-fx.js', 'font-scale.js', 'search-nav.js', 'analytics.js',
                     'custom.css', 'bg-fx.css', 'search_snippets.js',
                     'logo.svg', 'logo-dark.svg', 'favicon.svg',
                     'about.css', 'home.css', 'home-flow.js', 'p5.min.js']


def patch_cachebust():
    """用 _static 下自定义资源的当前内容 MD5 前 8 位替换页面引用的 ?v=。"""
    import re
    root = os.path.join(HERE, '_build', 'html')
    static_dir = os.path.join(root, '_static')
    digests = {}
    for name in _CACHEBUST_ASSETS:
        p = os.path.join(static_dir, name)
        if os.path.exists(p):
            with open(p, 'rb') as f:
                digests[name] = hashlib.md5(f.read()).hexdigest()[:8]
    if not digests:
        print('[build] 跳过缓存指纹补丁（无自定义资源）')
        return
    patterns = {
        name: re.compile(
            r'((?:src|href)=["\'][^"\']*?/' + re.escape(name) + r')'
            r'(?:\?v=[0-9a-fA-F]+)?(["\'])')
        for name in digests
    }
    skip_dirs = {'_static', '_sources', '_modules', '.git'}
    n_updated = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in filenames:
            if not fn.endswith('.html'):
                continue
            full = os.path.join(dirpath, fn)
            try:
                with open(full, 'r', encoding='utf-8') as f:
                    content = f.read()
            except OSError:
                continue
            patched = content
            for name, pat in patterns.items():
                patched = pat.sub(
                    lambda m: m.group(1) + '?v=' + digests[name] + m.group(2),
                    patched)
            if patched != content:
                try:
                    with open(full, 'w', encoding='utf-8') as f:
                        f.write(patched)
                    n_updated += 1
                except OSError:
                    continue
    print(f'[build] 缓存指纹: 已更新 {n_updated} 页（{len(digests)} 个资源）')


def patch_logo_dark():
    """把每个页面中 .only-dark 的 logo <img> src 指向 logo-dark.svg。

    logo 以 <img src=logo.svg> 加载，SVG 内的 currentColor 固定解析为默认黑色，
    无法随页面主题变化，导致 dark 深色导航栏上黑字几乎不可见。pydata 主题为
    .only-light 与 .only-dark 渲染两个同名 img，这里仅把 only-dark 那一个的
    src 换为浅色文字的 logo-dark.svg，light 仍用原 logo.svg，解决对比问题。
    仅在文件已生成且页面同时含 logo__image 与 only-dark 两个类时替换。
    """
    import re
    root = os.path.join(HERE, '_build', 'html')
    static_dir = os.path.join(root, '_static')
    if not os.path.exists(os.path.join(static_dir, 'logo-dark.svg')):
        print('[build] 跳过 dark logo 补丁（logo-dark.svg 不存在）')
        return
    # 匹配每个完整 <img> 标签（[^>]* 不跨闭合 >），仅在回调里判断它同时带
    # logo__image 与 only-dark 两个类且 src 指向 logo.svg 时，把 src 换为
    # logo-dark.svg。不引入 lookahead 跨标签，避免把相邻 img 的 class 误并入。
    img_tag = re.compile(r'<img[^>]*>')

    def _swap_dark(m):
        tag = m.group(0)
        if ('logo__image' in tag and 'only-dark' in tag
                and re.search(r'src="[^"]*?logo\.svg"', tag)):
            tag = tag.replace('logo.svg', 'logo-dark.svg', 1)
        return tag
    skip_dirs = {'_static', '_sources', '_modules', '.git'}
    n_updated = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in filenames:
            if not fn.endswith('.html'):
                continue
            full = os.path.join(dirpath, fn)
            try:
                with open(full, 'r', encoding='utf-8') as f:
                    content = f.read()
            except OSError:
                continue
            patched = img_tag.sub(_swap_dark, content)
            if patched != content:
                try:
                    with open(full, 'w', encoding='utf-8') as f:
                        f.write(patched)
                    n_updated += 1
                except OSError:
                    continue
    print(f'[build] dark logo: 已更新 {n_updated} 页 .only-dark 指向 logo-dark.svg')



def patch_search_stemmer():
    """修正 Sphinx 中文搜索的词干器引用。

    Sphinx 9 的 zh 搜索模块在客户端复用 english-stemmer(见 search/zh.py 的
    ``js_stemmer_rawcode = 'english-stemmer.js'``)，但生成的 ``language_data.js``
    却把 ``window.Stemmer`` 赋给从未定义的 ``ChineseStemmer``，执行即抛
    ``ReferenceError``，导致搜索一直停在"正在搜索中"。
    这里把该行替换为 ``window.EnglishStemmer``（文件内已定义、提供 .stemWord()），
    保持与 searchtools.js 的 ``new Stemmer().stemWord()`` 调用一致。
    """
    path = os.path.join(HERE, '_build', 'html', '_static', 'language_data.js')
    if not os.path.exists(path):
        print('[build] 跳过中文词干器补丁（language_data.js 不存在）')
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    bad = 'window.Stemmer = ChineseStemmer;'
    good = 'window.Stemmer = window.EnglishStemmer;'
    if bad in content:
        fixed = content.replace(bad, good)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print('[build] 已修复中文词干器引用: ChineseStemmer -> EnglishStemmer')
    elif good in content:
        print('[build] 中文词干器引用已就绪（无需补丁）')
    else:
        print('[build] 注意: language_data.js 未匹配到词干器赋值行')


# 注入到 search.html 的脚本：改进 Sphinx 搜索结果摘要，
# 让每条结果的 <p class="context"> 以命中关键词为窗口居中（纯文本，不依赖 fetch）。
_SEARCH_RESULTS_JS = """\
<script>
/* 优化 Sphinx 搜索结果：摘要以命中关键词为窗口居中，纯文本来源（兼容 file://）。 */
(function () {
  if (typeof Search === "undefined") return;
  /* 兜底：万一拿到的是整段 HTML（如缓存导致走了 fetch 路径），先转成纯文本，
     绝不把 <!DOCTYPE html> / <meta> 等源码显示在摘要里。 */
  var toText = function (s) {
    s = String(s || "");
    if (s.indexOf("<") >= 0) {
      try {
        var doc = new DOMParser().parseFromString(s, "text/html");
        s = doc.body ? doc.body.textContent : s;
      } catch (e) { /* 保留原样 */ }
    }
    return s;
  };
  Search.makeSearchSummary = function (text, keywords, anchor) {
    text = toText(text);
    if (!text) return null;
    var lower = text.toLowerCase();
    var terms = Array.from(keywords || []);
    var pos = -1;
    for (var i = 0; i < terms.length; i++) {
      var t = String(terms[i]).toLowerCase();
      if (!t) continue;
      var idx = lower.indexOf(t);
      if (idx >= 0 && (pos < 0 || idx < pos)) pos = idx;
    }
    var found = pos >= 0;
    if (!found) pos = 0;
    var start = Math.max(pos - 90, 0);
    var end = Math.min(start + 240, text.length);
    var chunk = text.slice(start, end).trim();
    var p = document.createElement("p");
    p.className = "context";
    p.textContent =
      (start > 0 && found ? "\\u2026 " : "") +
      chunk +
      (end < text.length ? " \\u2026" : "");
    return p;
  };
})();
</script>
"""


def patch_search_results():
    """在生成的 search.html 中注入脚本，改进搜索结果摘要的展示。

    依赖 build_search_snippets() 生成的 search_snippets.js（每页正文纯文本）：
      - 在 searchindex.js 之前加载 search_snippets.js；
      - 在 searchindex.js 之后注入 makeSearchSummary 覆盖脚本（以关键词为窗口居中）。
    """
    path = os.path.join(HERE, '_build', 'html', 'search.html')
    if not os.path.exists(path):
        print('[build] 跳过搜索结果补丁（search.html 不存在）')
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    marker = '<script src="searchindex.js"></script>'
    if marker not in content:
        print('[build] 注意: search.html 未找到 searchindex.js 锚点，跳过注入')
        return
    changed = False
    # 1) 在 searchindex.js 之前载入离线摘要文本
    loader = '<script src="_static/search_snippets.js"></script>'
    if loader not in content:
        content = content.replace(marker, loader + '\n  ' + marker)
        changed = True
    # 2) 在 searchindex.js 之后注入 makeSearchSummary 覆盖脚本
    if '改进 Sphinx 搜索结果' not in content:
        content = content.replace(marker, marker + '\n  ' + _SEARCH_RESULTS_JS)
        changed = True
    if not changed:
        print('[build] 搜索结果补丁已就绪（无需重复注入）')
        return
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('[build] 已注入搜索结果摘要补丁 -> search.html')


# --- Sphinx 检索词在生成 searchtools.js 中的原 fetch 摘要块（将其替换为离线取词） ---
_SEARCHTOOLS_OLD_BLOCK = """\
  } else if (showSearchSummary)
    fetch(requestUrl)
      .then((responseData) => responseData.text())
      .then((data) => {
        if (data)
          listItem.appendChild(
            Search.makeSearchSummary(data, searchTerms, anchor),
          );
        // highlight search terms in the summary
        if (SPHINX_HIGHLIGHT_ENABLED)
          // SPHINX_HIGHLIGHT_ENABLED is set in sphinx_highlight.js
          highlightTerms.forEach((term) =>
            _highlightText(listItem, term, "highlighted"),
          );
      });"""

_SEARCHTOOLS_NEW_BLOCK = """\
  } else if (showSearchSummary) {
    const _stored =
      typeof SEARCH_SNIPPETS !== "undefined" && SEARCH_SNIPPETS[docName]
        ? SEARCH_SNIPPETS[docName]
        : null;
    if (_stored) {
      const _snip = Search.makeSearchSummary(_stored, searchTerms, anchor);
      if (_snip) listItem.appendChild(_snip);
      if (SPHINX_HIGHLIGHT_ENABLED)
        highlightTerms.forEach((term) =>
          _highlightText(listItem, term, "highlighted"),
        );
    }
  }"""


def patch_search_searchtools():
    """替换 searchtools.js 的摘要生成方式：改为读取内存中的 SEARCH_SNIPPETS。

    原生实现用 fetch() 逐个拉取结果页来提取摘要，在 file:// (直接双击打开) 下会被
    浏览器拦截，导致摘要完全空白。这里改为从构建期生成的 search_snippets.js
    （window.SEARCH_SNIPPETS，按 docname 存正文纯文本）同步取词，兼容 file:// 与 http://。
    """
    path = os.path.join(HERE, '_build', 'html', '_static', 'searchtools.js')
    if not os.path.exists(path):
        print('[build] 跳过 searchtools.js 补丁（文件不存在）')
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'SEARCH_SNIPPETS' in content:
        print('[build] searchtools.js 摘要补丁已应用（跳过重复注入）')
        return
    if _SEARCHTOOLS_OLD_BLOCK not in content:
        print('[build] 注意: searchtools.js 未匹配到原摘要块，跳过')
        return
    patched = content.replace(_SEARCHTOOLS_OLD_BLOCK, _SEARCHTOOLS_NEW_BLOCK)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(patched)
    print('[build] 已替换 searchtools.js 摘要取词（离线，兼容 file://）')


class _ArticleText(HTMLParser):
    """提取 [role=main] 下的正文纯文本，剔除脚本/导航/表单等噪音。"""

    _SKIP_TAGS = {'script', 'style', 'nav', 'header', 'footer', 'form'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.main_depth = 0
        self.skip_stack = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if self.skip_stack:
            self.skip_stack += 1
            return
        if tag in self._SKIP_TAGS:
            self.skip_stack = 1
            return
        if tag == 'main':
            for k, v in attrs:
                if k == 'role' and v == 'main':
                    self.main_depth += 1
                    break

    def handle_endtag(self, tag):
        if self.skip_stack:
            self.skip_stack -= 1
            return
        if tag == 'main' and self.main_depth:
            self.main_depth -= 1

    def handle_data(self, data):
        if self.main_depth and not self.skip_stack:
            self.parts.append(data)


def build_search_snippets():
    """为每个已生成的 HTML 页预提取正文纯文本，写入 search_snippets.js。

    产物 window.SEARCH_SNIPPETS 以 Sphinx 的 docname（相对 html 根、去掉 .html）
    为键，供搜索页离线生成结果摘要。
    """
    import json
    root = os.path.join(HERE, '_build', 'html')
    skip_dirs = {'_static', '_sources', '_modules', '.git'}
    skip_files = {'search.html', 'genindex.html', 'py-modindex.html', 'objects.inv'}
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in filenames:
            if not fn.endswith('.html') or fn in skip_files:
                continue
            if fn.startswith('sg_execution_times'):
                continue
            full = os.path.join(dirpath, fn)
            key = os.path.relpath(full, root).replace('\\', '/')[:-5]
            try:
                with open(full, encoding='utf-8') as f:
                    html_doc = f.read()
            except OSError:
                continue
            parser = _ArticleText()
            try:
                parser.feed(html_doc)
            except Exception:
                continue
            txt = ' '.join(' '.join(parser.parts).split()).strip()
            if txt:
                out[key] = txt[:20000]
    dest = os.path.join(root, '_static', 'search_snippets.js')
    with open(dest, 'w', encoding='utf-8') as f:
        f.write('/* 由 build.py 生成：各页正文纯文本，供搜索摘要离线取词（兼容 file://）。 */\n')
        f.write('window.SEARCH_SNIPPETS = ' + json.dumps(out, ensure_ascii=False) + ';')
    print(f'[build] 已生成搜索摘要文本 {dest}（{len(out)} 页）')


def serve():
    import http.server
    import socketserver
    os.chdir(os.path.join(HERE, '_build', 'html'))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(('127.0.0.1', 8000), handler) as httpd:
        print('[serve] http://127.0.0.1:8000  (Ctrl+C 退出)')
        httpd.serve_forever()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--clean', action='store_true')
    ap.add_argument('--serve', action='store_true')
    ns = ap.parse_args()
    build(clean=ns.clean)
    if ns.serve:
        serve()
