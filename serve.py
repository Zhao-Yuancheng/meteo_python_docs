# -*- coding: utf-8 -*-
"""本地预览服务器：serve _build/html，HTML 响应带 no-cache 头。

python -m http.server 不发缓存控制头，浏览器按启发式缓存旧版 HTML——
页面里的内联补丁（主题同步/字号早期脚本等）更新后，用户不强制刷新就
一直看到旧页面。此服务器对 HTML（含目录索引）强制 no-cache，静态资源
已有 ?v= 指纹照常缓存。

用法：python serve.py [port]
"""
import http.server
import os
import socketserver
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '_build', 'html')


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        path = self.path.split('?', 1)[0].split('#', 1)[0]
        base = os.path.basename(path)
        if path.endswith('/') or path.endswith('.html') or '.' not in base:
            self.send_header('Cache-Control', 'no-cache, must-revalidate')
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write('[serve] %s\n' % (fmt % args))


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('127.0.0.1', port), Handler) as httpd:
        print(f'[serve] http://127.0.0.1:{port}/ -> {ROOT}')
        httpd.serve_forever()
