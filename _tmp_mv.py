# -*- coding: utf-8 -*-
import io, re

root = r'D:\Code\Vibe\meteo_python_docs\_build\html'
h = io.open(root + r'\about.html', encoding='utf-8').read()

print('title:', re.search(r'<title>(.*?)</title>', h).group(1))
print('meta desc:', '云笺 CloudDocs —— 兰州大学' in h)
print('about.css link:', re.search(r'href="[^"]*about\.css[^"]*"', h).group(0))
print('container div:', '<div id="meteo-about">' in h)
print('h1 followed by div:', bool(re.search(r'</h1>\s*<div id="meteo-about">', h)))
print('photos:', h.count('_static/photos/'))
print('theme-sync injected:', 'meteo-theme-sync' in h)
print('font-early injected:', 'meteo-fs-early' in h)
print('dark logo patched:', 'logo-dark.svg' in h)
print('no old topbar:', 'topbar' not in h and 'backBtn' not in h)
print('sections:', re.findall(r'id="(ma-[a-z]+)"', h))

# 导航：所有页面页眉含 about 链接
for rel in ('index.html', 'qa/index.html'):
    p = io.open(root + '\\' + rel.replace('/', '\\'), encoding='utf-8').read()
    m = re.search(r'href="([^"]*about\.html[^"]*)"[^>]*>\s*关于', p)
    nav = re.findall(r'class="nav-link nav-internal"[^>]*href="([^"]+)"', p)
    print(rel, '关于 link:', m.group(1) if m else 'MISSING', '| nav items:', len(nav))

# 搜索索引含关于页
s = io.open(root + r'\searchindex.js', encoding='utf-8', errors='ignore').read()
print('searchindex has about:', '"about"' in s or 'about' in s)
sn = io.open(root + r'\_static\search_snippets.js', encoding='utf-8', errors='ignore').read()
print('snippets has about:', "'about'" in sn or '"about"' in sn)
