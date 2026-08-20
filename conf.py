# -*- coding: utf-8 -*-
"""气象 + Python 编程文档 —— Sphinx 配置。

技术栈：Sphinx + PyData Sphinx Theme + sphinx-design + sphinx-gallery
        + sphinx-copybutton + myst-parser。
构建：python build.py   或   sphinx-build -b html . _build/html
"""
import os
import sys
import warnings

# sphinx-gallery 生成“下载例句 ipynb 的 zip 包”时，同一示例会被多个打包入口
# 重复写盘并触发 zipfile 的 ``Duplicate name`` UserWarning（纯重复项拉警告，
# 无实际数据丢失）。这类 Python 通知不属于文档问题，提前静默。
warnings.filterwarnings('ignore', message='Duplicate name:')

sys.path.insert(0, os.path.abspath('.'))

project = '气象 + Python 编程文档'
author = '兰州大学大气科学学院编程社区'
copyright = '2026, ' + author
version = '0.1'
release = '0.1.0'
language = 'zh_CN'
html_search_language = 'zh'
html_search_options = {
    'dict': None,   # 使用 jieba 默认词典
}

extensions = [
    'sphinx_design',                # 卡片 / 网格 / 标签页
    'sphinx_gallery.gen_gallery',   # 可执行示例画廊
    'sphinx_copybutton',            # 代码块复制按钮
    'sphinxcontrib.video',
    'myst_parser',                  # Markdown 源文件支持（Q&A 章节）
]

# MyST：允许在 .md 中用 {} 指令，与 reST 互通
myst_enable_extensions = ['colon_fence', 'deflist', 'substitution']
# Markdown 内部相对链接：把指向 .md/.rst 的链接解析为 Sphinx 文档交叉引用
myst_heading_anchors = 3
myst_links_external = False

# -- 主题 --
html_theme = 'pydata_sphinx_theme'
html_static_path = ['./_static']

html_logo = '_static/logo.svg'
html_favicon = './_static/favicon.svg'

html_theme_options = {
    # 顶部导航栏
    'navbar_align': 'content',
    'header_links_before_dropdown': 4,
    'header_dropdown_text': '更多',
    # 侧边栏
    'show_nav_level': 2,
    'navigation_depth': 4,
    'collapse_navigation': False,
    'navigation_with_keys': True,
    # 暗色 / 亮色高亮
    'pygments_light_style': 'a11y-high-contrast-light',
    'pygments_dark_style': 'a11y-high-contrast-dark',
    # 版本切换器（本地 JSON，构建期不远程校验）
    'switcher': {
        'json_url': '_static/switcher.json',
        'version_match': release,
    },
    'check_switcher': False,
    # 图标链接
    'icon_links': [
        {
            'name': 'GitHub',
            'icon': 'fab fa-github-square',
        },
    ],
    # 次侧栏：只保留本页目录
    'secondary_sidebar_items': ['page-toc'],
    'show_prev_next': True,
    'back_to_top_button': True,
    'search_bar_text': '搜索文档…',
}

# -- 自定义 CSS --
html_css_files = ['./custom.css']

# -- sphinx-gallery --

_ZH_FONTS = ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC', 'DejaVu Sans']


def _reset_mpl_zh(gallery_conf, fname):
    """默认 matplotlib 重置 + 中文字体回填。

    sphinx-gallery 每个示例执行前会调用 plt.rcdefaults() 抹掉 rcParams，
    0.21.0 尚无 matplotlib_rcparams 配置键，故用 reset_modules 钩子
    在重置之后立刻把中文字体配回去，保证画廊图中文不变成方块。
    """
    from sphinx_gallery.scrapers import _reset_matplotlib
    _reset_matplotlib(gallery_conf, fname)
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = list(_ZH_FONTS)
    plt.rcParams['axes.unicode_minus'] = False


sphinx_gallery_conf = {
    'examples_dirs': ['./examples'],            # 源脚本目录
    'gallery_dirs':  ['./gallery'],  # 生成画廊目录（顶层「示例」导航直连画廊）
    # Windows 路径用 \ 分隔，正则需同时兼容 / 与 \
    'filename_pattern': r'[/\\]plot_[^/\\]+\.py$',   # 仅执行 plot_ 开头的脚本
    'ignore_pattern': r'__init__\.py$|GALLERY_HEADER',
    'thumbnail_size': (400, 280),
    'backreferences_dir': './gallery/backreferences',
    'doc_module': ('numpy', 'matplotlib'),
    'notebook_extensions': {'.py', '.ipynb'},
    'reset_modules': (_reset_mpl_zh, 'seaborn'),
    'only_warn_on_example_error': True,       # 单个示例失败不中断构建
    'plot_gallery': True,
    # Windows 不区分大小写的文件系统找不到 matplotlib.rc.backrefs 等
    # backreferences 文件（属已知噪音），降级为 debug 不再计入告警。
    'log_level': {'backreference_missing': 'debug'},
}

# -- 复制按钮：去掉提示符前缀 --
copybutton_prompt_text = r'>>> |\.\.\. |\$ '
copybutton_prompt_is_regexp = True

# -- 输出 --
html_title = 'MeteoPython'
html_last_updated_fmt = '%Y-%m-%d'
exclude_patterns = [
    './_build', './Thumbs.db', './.DS_Store',
    './examples/GALLERY_HEADER.rst',
    './examples/plot_basics/GALLERY_HEADER.rst',
    './examples/plot_numpy/GALLERY_HEADER.rst',
    './examples/plot_viz/GALLERY_HEADER.rst',
]

# sphinx-gallery 的两类固有告警，属于预期行为，统一静默：
#   - config.cache：sphinx_gallery_conf.reset_modules 含函数对象，无法 pickle；
#   - toc.not_included：各 GALLERY_HEADER.rst 是画廊的内嵌模板，本就无须挂入 toctree。
# 画廊示例的其它基础设施噪音（backreferences 缺失、ipynb zip 打包重复项）见下方
# sphinx_gallery_conf 的 log_level 与 conf.py 顶部的 warnings.filterwarnings。
suppress_warnings = ['config.cache', 'toc.not_included']


# -- matplotlib 中文字体（sphinx-gallery 缩略图用）--
def setup(app):
    try:
        import matplotlib
        matplotlib.use('Agg')
        matplotlib.rcParams['font.sans-serif'] = list(_ZH_FONTS)
        matplotlib.rcParams['axes.unicode_minus'] = False
    except ImportError:
        pass
