常见问题 Q&A
============

收集学习与搭建本文档时的常见问题，按类别整理。完整版（≥30 条）由 T-004 交付后上线。

安装与构建
----------

.. dropdown:: sphinx-build 提示找不到扩展？

   确认在 ``P312`` 环境里装齐工具链：

   .. code-block:: bash

      pip install sphinx pydata-sphinx-theme sphinx-design \
                  sphinx-gallery sphinx-copybutton myst-parser

.. dropdown:: 构建时 sphinx-gallery 执行示例很慢或报错？

   首次构建会真实运行每个 ``plot_`` 脚本。可临时关闭执行以加速：

   .. code-block:: bash

      sphinx-build -b html -D sphinx_gallery_conf.plot_gallery=False . _build/html

第 2 章 · 数据类型相关
---------------------

.. dropdown:: 为什么 0.1 + 0.2 不等于 0.3？

   浮点数按 IEEE 754 二进制存储，0.1 无法被精确表示。这不是 bug，是所有编程语言的共同行为。

   .. code-block:: python

      print(0.1 + 0.2)               # 0.30000000000000004
      print(abs(0.1 + 0.2 - 0.3) < 1e-9)   # True：用容差比较

.. dropdown:: TypeError: can only concatenate str (not "int") to str？

   你在对字符串和数字做 ``+`` 拼接，例如 ``"气温：" + 25``。数字与文本组合请用 f-string：

   .. code-block:: python

      temp = 25
      print(f"气温：{temp} °C")   # ✓

.. dropdown:: SyntaxError: name 'true' is not defined？

   Python 的布尔值只有 ``True`` / ``False`` 两种写法，首字母必须大写。``true``、``false``、``TRUE`` 都不是布尔值。

.. dropdown:: KeyError: 'xxx'？

   访问了字典中不存在的键。稳妥写法：

   .. code-block:: python

      station.get("wind")        # 键不存在时返回 None，不报错
      station.get("wind", 0.0)   # 也可指定默认值

.. dropdown:: 中文输出或注释报 SyntaxError: Non-UTF-8 code？

   Python 3 源码默认 UTF-8，此错误通常是文件被另存为 GBK 等编码。在 VS Code 右下角把文件编码改回 UTF-8 重新保存即可。

绘图相关
--------

.. dropdown:: 图中中文显示为方块？

   Matplotlib 默认字体不含中文字形。设置：

   .. code-block:: python

      import matplotlib
      matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
      matplotlib.rcParams["axes.unicode_minus"] = False   # 顺便修复负号显示

.. dropdown:: Cartopy 画海岸线时卡住或报错？

   首次使用会下载 Natural Earth 数据，需联网。离线环境可提前在有网机器上缓存 ``~/.local/share/cartopy``（Windows 在 ``%LOCALAPPDATA%``）后整体拷贝。
