# -*- coding: utf-8 -*-
import io, re

h = io.open(r'D:\Code\Vibe\meteo_python_docs\_build\html\index.html', encoding='utf-8').read()
# 找 head 里所有内联 <script>（无 src 的），打印含 mode/theme 的
for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', h, re.S):
    s = m.group(1)
    if 'mode' in s or 'theme' in s:
        print('--- inline script ---')
        print(s.strip()[:1200])
        print()
