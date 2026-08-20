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
import subprocess
import sys
import argparse

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
