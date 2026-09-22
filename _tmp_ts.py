# -*- coding: utf-8 -*-
import io

h = io.open(r'D:\Code\Vibe\meteo_python_docs\_build\html\index.html', encoding='utf-8').read()
print('index theme-sync injected:', "id=\"meteo-theme-sync\"" in h)
print('index pageshow listener:', h.count('pageshow'))

a = io.open(r'D:\Code\Vibe\meteo_python_docs\_build\html\about.html', encoding='utf-8').read()
print('about head mode-first:', "localStorage.getItem('mode')" in a)
print('about pageshow/storage:', "addEventListener('pageshow'" in a and "addEventListener('storage'" in a)
print('about backBtn:', 'history.back()' in a)