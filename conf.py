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


def _patch_cjk_inline_markup() -> None:
    # docutils 的行内标记识别规则要求 **粗体** 等标记的起始串之前、结束串
    # 之后必须紧邻空白或西文标点（punctuation_chars 里的 openers/closers/
    # delimiters 字符类），汉字不是合法边界，因此「在**示例画廊**里」这类
    # 紧贴中文的加粗会把双星号原样显示出来。
    #
    # Inliner.init_customizations() 在每篇文档解析时读取 punctuation_chars
    # 模块属性组装行内标记正则；这里包装该函数，在组装正则的瞬间向四个边界
    # 字符类临时追加 CJK 区段再复原。西文规则保持不变：x**2、100**8 等
    # 字母数字旁的星号依旧按字面处理（官方 character_level_inline_markup
    # 开关会对任何字符放开边界，导致 (u**2 + v**2) ** 0.5 被误识别为
    # 粗体，故弃用，删除了 docutils.conf）。
    from docutils.parsers.rst import states
    from docutils.utils import punctuation_chars

    cjk = (
        '\u2e80-\u303f'                                # CJK 部首补充、CJK 符号和标点
        '\u3040-\u30ff'                                # 平假名、片假名
        '\u3105-\u312f\u31a0-\u31ff'                   # 注音符号及扩展
        '\u3130-\u318f'                                # 谚文兼容字母
        '\u3400-\u4dbf\u4e00-\u9fff'                   # CJK 扩展 A、常用汉字
        '\ua960-\ua97f\uac00-\ud7ff'                   # 谚文扩展、谚文音节
        '\uf900-\ufaff\ufe30-\ufe4f'                   # CJK 兼容表意文字及形式
        '\uff00-\uffef'                                # 全角形式（含全角字母数字）
        '\U00020000-\U0002ffff\U00030000-\U0003ffff'   # CJK 扩展 B 及以后
    )
    names = ('openers', 'closers', 'delimiters', 'closing_delimiters')
    original = states.Inliner.init_customizations

    def with_cjk_boundaries(self, settings):
        saved = {name: getattr(punctuation_chars, name) for name in names}
        try:
            for name in names:
                setattr(punctuation_chars, name, saved[name] + cjk)
            return original(self, settings)
        finally:
            for name in names:
                setattr(punctuation_chars, name, saved[name])

    states.Inliner.init_customizations = with_cjk_boundaries


_patch_cjk_inline_markup()

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
templates_path = ['_templates']

html_logo = '_static/logo.svg'
html_favicon = './_static/favicon.svg'

html_theme_options = {
    # 顶部导航栏：「关于」进主导航（about.rst 的 toctree 项，放最后）；
    # 阈值提到 6，六个中文短链接全部直接展示，不再折叠进「更多」下拉
    'navbar_align': 'content',
    'header_links_before_dropdown': 6,
    'header_dropdown_text': '更多',
    # 页眉右侧组件：主题切换 + 图标链接
    'navbar_end': ['theme-switcher', 'navbar-icon-links'],
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
    # 页脚：去掉 "Created using Sphinx …" 行，仅保留版权；
    # 右侧主题版本来一行替换为格言（footer-motto 模板）。
    'footer_start': ['copyright'],
    'footer_end': ['footer-motto'],
}

# 仅「关于」页隐藏全部侧边栏（主导航 + 页内目录），正文全宽展示；
# 其余页面仍走主题默认侧边栏。
html_sidebars = {
    'about': [],
}

# -- 自定义 CSS --（含背景动效层与开关按钮样式）
html_css_files = ['./custom.css', './bg-fx.css']

# -- 自定义 JS —— 背景粒子动效（P0）+ 搜索跳转高亮 + 正文字号调节 --
html_js_files = ['./bg-fx.js', './search-nav.js', './font-scale.js']

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
    'examples_dirs': ['./examples'],            # 源脚本目录（子目录构成画廊分区）
    'gallery_dirs':  ['./gallery'],             # 生成画廊目录（顶层「示例」导航直连画廊）
    # 顶层分区顺序：按内容主线固定为 基础绘图 → NumPy 计算 → 气象数据可视化 → 科研绘图。
    # （默认按子目录名升序，plot_sci 会排在 plot_viz 前，故用 ExplicitOrder 显式指定。）
    'subsection_order': ['examples/plot_basics', 'examples/plot_numpy',
                         'examples/plot_viz', 'examples/plot_sci'],
    # Windows 路径用 \ 分隔，正则需同时兼容 / 与 \
    'filename_pattern': r'[/\\]plot_[^/\\]+\.py$',   # 仅执行 plot_ 开头的脚本
    'ignore_pattern': r'__init__\.py$|GALLERY_HEADER',
    'thumbnail_size': (800, 560),
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
html_title = '云笺 CloudDocs'
html_last_updated_fmt = '%Y-%m-%d'
exclude_patterns = [
    './_build', './Thumbs.db', './.DS_Store',
    './examples/GALLERY_HEADER.rst',
    './examples/plot_basics/GALLERY_HEADER.rst',
    './examples/plot_numpy/GALLERY_HEADER.rst',
    './examples/plot_viz/GALLERY_HEADER.rst',
    './examples/plot_sci/GALLERY_HEADER.rst',
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
