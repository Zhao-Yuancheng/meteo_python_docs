# 临时验证脚本：扫描 _build/html 中 docutils 解析失败标记（problematic）与
# 正文残留字面 **，验证后删除。
import os
import re
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_build', 'html')
SKIP_DIRS = {'_static', '_sources', '_modules', '.git', '_downloads', '_images'}
CODE_TAGS = {'pre', 'code', 'samp', 'kbd', 'script', 'style', 'textarea', 'svg'}


class Scanner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.hits = []

    def handle_starttag(self, tag, attrs):
        if tag in CODE_TAGS:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag in CODE_TAGS and self.depth > 0:
            self.depth -= 1

    def handle_data(self, data):
        if self.depth == 0 and '**' in data:
            self.hits.append(' '.join(data.split())[:90])


cjk = re.compile(r'[\u2e80-\u303f\u3040-\u30ff\u3105-\u312f\u31a0-\u31ff'
                 r'\u3130-\u318f\u3400-\u4dbf\u4e00-\u9fff'
                 r'\ua960-\ua97f\uac00-\ud7ff\uf900-\ufaff\ufe30-\ufe4f'
                 r'\uff00-\uffef]')
prob_ctx = re.compile(r'.{0,70}<span class="problematic"')

n_files = n_cjk = n_plain = n_prob = 0
plain_samples = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if not fn.endswith('.html'):
            continue
        n_files += 1
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, ROOT)
        doc = open(full, encoding='utf-8', errors='ignore').read()

        for m in prob_ctx.finditer(doc):
            n_prob += 1
            s = ' '.join(doc[max(0, m.start() - 80):m.end() + 70].split())
            print(f'[problematic] {rel} :: ...{s[-140:]}')

        s = Scanner()
        try:
            s.feed(doc)
        except Exception as e:
            print(f'[parse-error] {rel}: {e}')
            continue
        for text in s.hits:
            if cjk.search(text):
                n_cjk += 1
                print(f'[CJK-相邻 **] {rel}: {text}')
            else:
                n_plain += 1
                if len(plain_samples) < 8:
                    plain_samples.append(f'{rel}: {text}')

print(f'\n扫描 {n_files} 页：problematic {n_prob} 处；中文相邻 ** 残留 {n_cjk} 处；西文字面 {n_plain} 处。')
for line in plain_samples:
    print('  西文字面:', line)
