# 临时扫描：源码中 CJK 相邻的行内标记敏感字符（静默误配风险），验证后删除。
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = {'_build', '.git', '_static', 'data', 'figures', 'scripts', 'tutorial', '.venv'}
cjk = '\u2e80-\u303f\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef'

patterns = {
    'CJK+单星': re.compile(f'[{cjk}]\\*(?!\\*)'),
    '单星+CJK': re.compile(f'(?<!\\*)\\*[{cjk}]'),
    'CJK+竖线': re.compile(f'[{cjk}]\\|'),
    '竖线+CJK': re.compile(f'\\|[{cjk}]'),
    'CJK+下划线': re.compile(f'[{cjk}]_'),
    'CJK+单引号': re.compile(f'(?<!`)`[{cjk}]|[{cjk}]`(?!`)'),
}

n = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP]
    for fn in filenames:
        if not fn.endswith(('.rst', '.py')):
            continue
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, ROOT)
        try:
            lines = open(full, encoding='utf-8').read().splitlines()
        except OSError:
            continue
        in_code = False
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if s.startswith('.. code') or s == '::':
                in_code = True
            elif s and not s[0].isspace() and not s.startswith(('-', '*', '#', '..')):
                in_code = False
            if in_code:
                continue
            for name, pat in patterns.items():
                if pat.search(line):
                    n += 1
                    print(f'[{name}] {rel}:{i}: {s[:100]}')
print('总计:', n)
