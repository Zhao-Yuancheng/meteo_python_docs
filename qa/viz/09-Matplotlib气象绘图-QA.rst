气象数据绘图（一）Matplotlib Q&A
======================================

   **章节定位**\ ：第 9 章（模块三 · 气象数据可视化第一讲）·
   对应用户指南 ``user_guide/viz/matplotlib.rst``
   **通用排错方法论**\ ：见
   :doc:`00-通用排错指南 </qa/basics/00-通用排错指南>`\ （0.1 节「报错 / 警告 /
   静默错值」三分法、0.4 节「排查七招」、0.5 节「静默污染」先读）。
   **校正说明**\ ：本文全部报错 / 警告 /
   异常现象均在本机真实运行验证，报错被脚本捕获后以原文照录，警告以完整
   stderr 片段呈现。绘图全部使用
   ``matplotlib.use('Agg')``\ （无显示器后端），中文、轴名、NaN、经纬度等“异常现象”通过保存
   PNG 与读取 ``ax`` 属性共同验证。 **绘图流程回顾**\ （正文第 9
   节）：准备数据 → 建 ``Figure``\ （画布，\ ``figsize``/``dpi``\ ）→ 在
   ``Figure`` 上加 ``Axes``\ （坐标区；推荐
   ``fig, ax = plt.subplots()``\ ）→ 在 ``Axes`` 里画
   ``plot / scatter / bar / hist / contourf / imshow`` → 输出或
   ``savefig`` 保存。全章警醒你：\ **凡是“对某个具体图”的操作，一律挂在
   ``ax.xxx`` 上；\ ``plt``
   只在开图画布、多图画板、清图回收时出场**\ （正文「面向对象接口，别让
   pyplot 全局状态打游击」）。

--------------

.. _90-本章报错--警告--异常现象速查总表:

9.0 本章报错 / 警告 / 异常现象速查总表
--------------------------------------

第 9 章的核心是“把图画对、画好看”。三大类问题里，\ **第 3
类“静默”在本章最密集**——中文变方块、坐标轴翻转、NaN
破洞、刻度拥挤都\ **不报错**\ ，全靠你脑子里那份“现象 →
原因”映射来盯。先看总表。

+-------------------------------------------------------------------+------+-------------------------------+
| 英文关键词 / 现象                                                 | 类型 | 报错 / 现象一句话             |
+===================================================================+======+===============================+
| ``Glyph ... missing from font(s) DejaVu Sans.``                   | 警告 | 中文字没配字体 → 方块(□□)     |
+-------------------------------------------------------------------+------+-------------------------------+
| ``Glyph 8722 (\N{MINUS SIGN}) missing ... SimHei.``               | 警告 | 负号变方块                    |
+-------------------------------------------------------------------+------+-------------------------------+
| ``'Figure' object has no attribute 'plot'``                       | 报错 | 在画布上直接 ``plot``\ （应在 |
|                                                                   |      | ``ax.plot``\ ）               |
+-------------------------------------------------------------------+------+-------------------------------+
| ``'numpy.ndarray' object has no attribute 'plot'``                | 报错 | 在数组上直接 ``plot``         |
+-------------------------------------------------------------------+------+-------------------------------+
| ``x and y must have same first dimension``                        | 报错 | ``x`` 与 ``y`` 长度不等       |
+-------------------------------------------------------------------+------+-------------------------------+
| ``x and y must be the same size``                                 | 报错 | ``scatter`` 的 ``x``/``y``    |
|                                                                   |      | 长度不等                      |
+-------------------------------------------------------------------+------+-------------------------------+
| 2D 数组当多条曲线                                                 | 静默 | 不报错却画出一堆线            |
+-------------------------------------------------------------------+------+-------------------------------+
| ``set_xlim``/``set_ylim`` 顺序写反                                | 静默 | x 轴被静默反转                |
+-------------------------------------------------------------------+------+-------------------------------+
| ``FixedLocator locations (5) ... labels (3)`` 不匹配              | 报错 | 刻度与标签个数不匹配          |
+-------------------------------------------------------------------+------+-------------------------------+
| ``'Axes' object has no attribute 'cmap'``                         | 报错 | ``fig.colorbar(ax)``          |
|                                                                   |      | 传错了对象                    |
+-------------------------------------------------------------------+------+-------------------------------+
| ``No mappable was found to use for colorbar creation``            | 报错 | ``plt.colorbar()``            |
|                                                                   |      | 没任何可映射对象              |
+-------------------------------------------------------------------+------+-------------------------------+
| ``No artists with labels found to put in legend``                 | 警告 | 曲线没写 ``label`` 就         |
|                                                                   |      | ``legend()``                  |
+-------------------------------------------------------------------+------+-------------------------------+
| ``'uper right' is not a valid value for loc``                     | 报错 | ``loc`` 拼错                  |
+-------------------------------------------------------------------+------+-------------------------------+
| ``module 'matplotlib.pyplot' has no attribute 'scatters'``        | 报错 | 方法名多/少个 s               |
+-------------------------------------------------------------------+------+-------------------------------+
| ``Rectangle.set() got an unexpected keyword argument 'normed'``   | 报错 | ``hist`` 误用                 |
|                                                                   |      | ``np.histogram`` 的旧参数     |
+-------------------------------------------------------------------+------+-------------------------------+
| ``Contour levels must be increasing``                             | 报错 | ``levels`` 写成降序           |
+-------------------------------------------------------------------+------+-------------------------------+
| ``imshow`` 之 ``origin``/``extent`` 反                            | 静默 | 图片上下/左右翻转             |
+-------------------------------------------------------------------+------+-------------------------------+
| 含 NaN 的场彩图有白洞                                             | 静默 | 缺测格不闭合、留白斑          |
+-------------------------------------------------------------------+------+-------------------------------+
| ``FileNotFoundError: No such file ...``                           | 报错 | ``savefig`` 目录不存在        |
+-------------------------------------------------------------------+------+-------------------------------+
| ``print_png() got an unexpected keyword argument 'bound_inches'`` | 报错 | ``bbox_inches`` 拼错成        |
|                                                                   |      | ``bound_inches``              |
+-------------------------------------------------------------------+------+-------------------------------+
| ``Format 'xyzz' is not supported``                                | 报错 | 保存格式后缀不支持            |
+-------------------------------------------------------------------+------+-------------------------------+
| ``num must be an integer with 1 <= num <= 4, not 9``              | 报错 | ``add_subplot`` 子图序号越界  |
+-------------------------------------------------------------------+------+-------------------------------+
| ``sharex`` 顶层子图 x 刻度消失                                    | 静默 | 只留最底子图画 x 轴标签       |
+-------------------------------------------------------------------+------+-------------------------------+
| 时间序列刻度挤成一团数字纹                                        | 静默 | ``datetime`` 没配             |
|                                                                   |      | ``DateFormatter``             |
+-------------------------------------------------------------------+------+-------------------------------+
| ``Date ordinal ... converts to 0000-...``                         | 报错 | 日期超出 Matplotlib           |
|                                                                   |      | 可表示范围                    |
+-------------------------------------------------------------------+------+-------------------------------+
| 温度标 ``K`` 却用 ℃ 数据                                          | 静默 | 轴名/单位写错，图中无法自查   |
+-------------------------------------------------------------------+------+-------------------------------+
| 经纬度 ``extent`` 写反导致图片翻转                                | 静默 | 上北下南不成立                |
+-------------------------------------------------------------------+------+-------------------------------+

..

   **一句话记住**\ ：第 9 章大多数“Bug”不像第 6
   章那样抛异常，而是\ **图悄悄画错、中文悄悄变方块、坐标悄悄反转**\ 。见到
   ``missing from font``\ 、\ ``same first dimension``\ 、\ ``must be the same size``\ 、\ ``No mappable``\ 、\ ``No artists with labels``
   这些关键字，立刻把矛头指向对应的一类，正是 00 篇 0.5
   节强调的“静默污染”在绘图上的翻版。

--------------

.. _91-中文字体中文变方块-负号变方块:

9.1 中文字体：中文变方块（□□）/ 负号变方块
------------------------------------------

.. _911-中文没配字体会话方块--glyph--missing-from-fonts警告不中断:

9.1.1 中文没配字体会话方块 + ``Glyph ... missing from font(s)``\ （警告，不中断）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：运行 ``fig, ax = plt.subplots()`` 后，用
``ax.set_title("兰州某月逐日平均温")`` 之类写中文，保存 PNG
**并不报错**\ ，但 stderr 冒出每缺一个中文字符就各一行的
``UserWarning``\ ，而图里中文全变成一排小方块（□□）。

.. code:: python

   import matplotlib
   matplotlib.use('Agg')
   import matplotlib.pyplot as plt
   import numpy as np

   x = np.arange(1, 32)
   t = 15 + 3.5 * np.sin(2 * np.pi * x / 31)
   fig, ax = plt.subplots(figsize=(7, 4))
   ax.plot(x, t, color="tab:red")
   ax.set_xlabel("日期（日）")
   ax.set_ylabel("气温（℃）")
   ax.set_title("兰州某月逐日平均温")
   fig.savefig(r"...\sim\t1_no_font.png")   # 图里中文都是方框

.. code:: text

   UserWarning: Glyph 28201 (\N{CJK UNIFIED IDEOGRAPH-6E29}) missing from font(s) DejaVu Sans.
                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
     fig.savefig(r"...\sim\t1_no_font.png")
   UserWarning: Glyph 65288 (\N{FULLWIDTH LEFT PARENTHESIS}) missing from font(s) DejaVu Sans.
     fig.savefig(r"...\sim\t1_no_font.png")
   UserWarning: Glyph 26376 (\N{CJK UNIFIED IDEOGRAPH-6708}) missing from font(s) DejaVu Sans.   # "月"
     .....(每个缺失汉字 / 全角括号各一条)

**原因**\ ：Matplotlib 默认字体是 **DejaVu
Sans**\ ，它根本没有中文字形。一遇到中文字符（\ ``missing from font(s) DejaVu Sans``\ ），就画一个“缺字形”的占位方块
□。每个缺的字都发一条
``UserWarning``\ ，但\ **程序照跑、图照存**——所以你不会被拦住，只会看到满屏方块。注意
``（℃）`` 里的全角括号（\ ``FULLWIDTH ... PARENTHESIS``\ ）同样缺失。

**解决办法**\ ：在绘图脚本\ **最顶部**\ 一次性配置中文字体白名单，让
Matplotlib 从 ``font.sans-serif`` 里挑一个带中文的字体：

.. code:: python

   import matplotlib.pyplot as plt
   plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei",
                                      "Noto Sans CJK SC", "WenQuanYi Micro Hei"]

配好后图里中文正常、警告消失。

   **气象场景一句话**\ ：DejaVu Sans
   像一张“只印西文字母的底图”，你硬要往上面写“兰州”两个字，就像把中文地名排进纯英文自动站报文——编码表里没这个字，只能吐个占位框。看到
   ``missing from font(s)`` 就默念“字体白名单没装中文”，别怀疑数据。

--------------

.. _912-负号也变方块axesunicode_minus警告不中断:

9.1.2 负号也变方块：\ ``axes.unicode_minus``\ （警告，不中断）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：只配了 ``font.sans-serif``\ ，却没关
``axes.unicode_minus``\ 。此时中文正常，但\ **坐标轴上负数前面的减号**\ 变成一个方块，stderr
提示 ``MINUS SIGN`` 缺失：

.. code:: python

   import matplotlib.pyplot as plt
   plt.rcParams["font.sans-serif"] = ["SimHei"]      # 只配了中文字体
   # 故意不写 plt.rcParams["axes.unicode_minus"] = False

   x = np.arange(1, 32); t = 14 + 4 * np.sin(2 * np.pi * x / 31) - 18   # 出现负温
   fig, ax = plt.subplots(figsize=(7, 4))
   ax.plot(x, t, color="tab:red")
   ax.set_yticks([-8, -4, 0, 4, 8])      # y 轴有负数刻度
   fig.savefig(r"...\sim\t1_no_unicode_minus.png")   # 负刻度前 "-" 是方块

.. code:: text

   UserWarning: Glyph 8722 (\N{MINUS SIGN}) missing from font(s) SimHei.
                                             ^^^^^^^^^^^^^^^^
     fig.savefig(r"...\sim\t1_no_unicode_minus.png")

**原因**\ ：负号在数学上常用
``U+2212 MINUS SIGN``\ （长一些的减号）。Matplotlib 默认
``axes.unicode_minus=True``\ ，想用这个更漂亮的 Unicode 减号；但 SimHei
等号并不带这个字形，于是又变成一个方块——**数据没丢，难看且误导**\ 。

**解决办法**\ ：跟中文字体一行一起，把 ``unicode_minus``
关掉，让减号回退成普通 ``-``\ ：

.. code:: python

   plt.rcParams["axes.unicode_minus"] = False   # 负号用 ASCII "-", 避免方块

..

   **气象场景一句话**\ ：冬半年气温场里的负温明明合理，可图上每个
   ``-8 ℃`` 却顶着个小方框，读者会以为机器出
   bug——``axes.unicode_minus=False`` 是让“负号回归正常 ‘-’
   的开关”，和中文字体是配套的两行，\ **F5
   一次配齐**\ （正文最佳实践踩坑清单第 2 条）。

--------------

.. _913-只给单个注释造中文局部-fontproperties补充写法:

9.1.3 只给单个注释造中文：局部 ``FontProperties``\ （补充写法）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象**\ ：整图别处不用中文、不想全局改
``rcParams``\ ，只想某一段注释用中文字体。

**解决办法**\ ：用 ``matplotlib.font_manager.FontProperties(fname=...)``
指定字体文件，再在 ``ax.text / ax.annotate`` 里传
``fontproperties=``\ （对应 PPT 第 31 页“中文支持”做法）：

.. code:: python

   from matplotlib.font_manager import FontProperties
   myfont = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc")   # 微软雅黑
   ax.annotate("7 月最热", xy=(200, 22), fontproperties=myfont,
               arrowprops=dict(arrowstyle="->"))

..

   **气象场景一句话**\ ：这种“局部刷中文”适合在面上只标一句“\ ``CB``
   高层强辐散”的探空 / 风场注释——影响面小、不污染整图风格。

--------------

.. _92-figure--axes--artist-三层模型画错了对象:

9.2 Figure / Axes / Artist 三层模型：画错了对象
-----------------------------------------------

.. _921-在-figure-上直接-plot--attributeerror报错:

9.2.1 在 ``Figure`` 上直接 ``plot`` → ``AttributeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：\ ``fig, ax = plt.subplots()`` 拿到的是“画布
+ 坐标区”两个对象，你却把绘图方法误挂到 ``fig`` 上：

.. code:: python

   import matplotlib.pyplot as plt
   import numpy as np

   x = np.arange(5)
   fig, ax = plt.subplots()
   fig.plot(x, x**2)     # 错! plot 是 ax 的方法, 不是 fig 的

.. code:: text

   AttributeError: 'Figure' object has no attribute 'plot'

**原因**\ ：\ ``fig``\ （\ ``Figure``\ ）只负责“画布有多大、存几个
``Axes``\ ”；真正“在某块区域画线”的方法是 ``Axes.plot``\ 。查 ``fig.``
后面补出的方法里根本没有 ``plot``\ ，于是报 ``AttributeError``\ 。

**解决办法**\ ：改成
``ax.plot(x, x**2)``\ 。口诀：\ **凡是“画内容”，都从 ``ax.``
开头**\ （\ ``ax.plot / ax.scatter / ax.set_xlabel / ax.legend ...``\ ）。

   **气象场景一句话**\ ：\ ``fig`` 是一整块展板，\ ``ax``
   是展板上你面前这块白板——你想在白板上描气温折线，却去找展板负责人（fig）要笔，他说“我这没画线的笔”，\ ``AttributeError``
   就是这句“没这服务”。

--------------

.. _922-在-numpyndarray-上直接-plot--attributeerror报错:

9.2.2 在 ``numpy.ndarray`` 上直接 ``.plot`` → ``AttributeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：把 ``plot``
当成“数据的自带方法”，写在数组后面：

.. code:: python

   import numpy as np
   np.array([1, 2, 3]).plot()      # 数据是数组, 它不是绘图对象

.. code:: text

   AttributeError: 'numpy.ndarray' object has no attribute 'plot'

**原因**\ ：\ ``plot`` 只存在于 ``Axes``\ （和 pandas 的
``DataFrame.plot`` 这类封装）上，\ ``ndarray``
只是个数据箱子，压根没有画图功能。这是新手最常见的“对象搞混”之一。

**解决办法**\ ：先 ``fig, ax = plt.subplots()``\ ，再
``ax.plot(np.array([1,2,3]))``\ ；或确认你要装的是 pandas 里的
``df.plot(ax=ax)``\ （那才有 ``plot`` 方法）。

   **气象场景一句话**\ ：站点温度数据 ``t`` 只是一串数字，你喊
   ``t.plot()``
   等于让一台“气象数据采集箱”去画图——采集箱只负责记录，画图得交给制图员
   ``ax``\ 。

--------------

.. _923-pltsubplot-vs-pltsubplots-混淆返回对象不一样:

9.2.3 ``plt.subplot`` vs ``plt.subplots`` 混淆：返回对象不一样
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：两者拼写差一个 ``s``\ ，但返回的东西截然相反：

- ``plt.subplots(2, 2)`` → 返回 **(fig, 2×2 的 axes
  数组)**\ （推荐，多子图用这个）；
- ``plt.subplot(2, 2, 1)`` → 返回\ **单个 Axes**\ （“当前第 1
  个格子”）。

新手拿 ``fig, axes = plt.subplots(1, 3)``
之后，想取下个子图的子图，却对单个标量 ``ax`` 做下标：

.. code:: python

   fig, axes = plt.subplots(1, 3)     # axes 是一维数组, 长度 3
   axes[1][2]                         # axes[1] 是一个 Axes, Axes 不能再下标

.. code:: text

   TypeError: 'Axes' object is not subscriptable

（\ ``subplots(2,2)`` 的 ``axes`` 是 ``(2,2)`` 二维数组，越界写法
``axes[2,3]`` 则抛 ``IndexError``\ ，见 9.2.4。）

**原因**\ ：\ ``subplots(行,列)`` 返回的是一个 **axes
数组**\ （\ ``np.ndarray``\ ），要用 ``axes[行,列]`` 取单个
``Axes``\ ；而 ``axes[1]`` 取出的是一个 ``Axes``\ ，再 ``[2]`` 就是对
``Axes`` 下标 → ``'Axes' object is not subscriptable``\ 。

**解决办法**\ ：

- 想画多子图，生成时就用 ``fig, axes = plt.subplots(2, 2)``\ （复数
  axes），一次性拿到数组；
- 取坐标区用 ``axes[r, c]``\ ；记不住就统一 ``axes.flat`` /
  ``axes.flatten()`` 遍历（见 9.2.5）；
- ``plt.subplot(行,列,序号)`` 是“单格子”配套写法，和“一次变出数组”的
  ``subplots`` 是两套用法，别混。

..

   **气象场景一句话**\ ：\ ``subplots`` 像一次性开出 2×2
   的站房图纸，给你一张“格子地图”（数组）；\ ``subplot`` 是“我现在只进第
   3 间（序号从 1
   数）”。拿地图却想单点进房、或进房后还想再下标，自然串味报错。

--------------

.. _924-用-axes23-取不存在的子图--indexerror报错:

9.2.4 用 ``axes[2,3]`` 取不存在的子图 → ``IndexError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：\ ``plt.subplots(2,2)`` 只有 4 个子图（行 0/1
× 列 0/1），你却取 ``axes[2,3]``\ ：

.. code:: python

   fig, axes = plt.subplots(2, 2)
   axes[2, 3]        # 越界

.. code:: text

   IndexError: index 2 is out of bounds for axis 0 with size 2

**原因**\ ：\ ``axes`` 是 ``(2,2)`` 数组，第一维（\ ``axis 0``\ ）只有
0、1 两个下标，\ ``2`` 越界 → ``IndexError``\ 。\ ``axis 0 with size 2``
就是在告诉你“第一根轴长度只有 2”。

**解决办法**\ ：记住 ``axes`` 下标对应“行、列”，二维数组每个维度从 0
数起。越界前先 ``print(axes.shape)`` 核对。

   **气象场景一句话**\ ：第 9 步要拼一张“折线 + 散点 + 直方图”的 2×2
   图板，却去取第 3 行第 4
   列的格子——展板上根本没有，\ ``axis 0 with size 2``
   是展板告诉你“这方向最多只能数到 2”。

--------------

.. _925-二维-axes-遍历flatten--flat-保平安技巧:

9.2.5 二维 ``axes`` 遍历：\ ``flatten()`` / ``flat`` 保平安（技巧）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象**\ ：\ ``plt.subplots(2,2)`` 返回的 ``axes`` 是
``(2,2)``\ ，逐个填内容时若手写 ``axes[0]...axes[3]``
会得到怪异结果（\ ``axes[0]`` 是第一行数组，不是第一个 ``Axes``\ ）。

**解决办法**\ ：用 ``axes.flat`` 或 ``axes.flatten()``
把二维展平成竖排逐个填：

.. code:: python

   fig, axes = plt.subplots(2, 2, figsize=(11, 7))
   for i, ax in enumerate(axes.flatten()):
       ax.plot([0, 1], [0, i])
       ax.set_title(f"子图 {i}")        # 0,1,2,3 按行展平
   fig.savefig(r"...\sim\t2_flatten.png")

**关键辨析**\ ：\ ``fig, ax = plt.subplots()``\ （不带行列，默认
1×1）返回的 ``ax`` 是\ **单个 Axes**\ ，不是数组，不能
``.flatten()``\ ；只有 ``subplots(2,2)``
这种多格返回数组。判断“它是标量还是数组”用
``print(type(ax), getattr(ax, 'shape', None))``\ 。

   **气象场景一句话**\ ：2×2
   图板循环填充就像照着“预报图板”逐格贴天气图——``flatten()`` 把 4
   个格子排成一行挨个贴，避免手工数格子数到串位。

--------------

.. _926-axfigure-是属性还是方法正确用法:

9.2.6 ``ax.figure`` 是属性还是方法？（正确用法）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：有人想从 ``ax`` 找回它所属的 ``Figure``\ ，写
``ax.figure()`` 会报错 — 实际上 ``figure`` 是\ **属性**\ ，不是方法：

.. code:: python

   fig, ax = plt.subplots()
   print(ax.figure is fig)    # True, ax.figure 是属性, 不用加括号

.. code:: text

   True

**原因 / 解决办法**\ ：\ ``Axes`` 上 ``figure`` 是指向父 ``Figure``
的\ **属性**\ ，读取时\ **不要加括号**\ 。同理 ``ax.axes``
指向自身所在的 ``Axes`` 对象、\ ``ax.lines`` 是已画线的列表——这些“拿对象
/ 拿属性”的都不加括号；而“做动作”的
``ax.set_title()``\ 、\ ``ax.plot()``\ 、\ ``ax.legend()`` 才加括号。

   **气象场景一句话**\ ：\ ``ax.figure``\ 、\ ``ax.lines``
   是“读数器”，看一眼不必喊话（不加括号）；\ ``set_/plot/scatter``
   是“下指令”，必须喊（加括号）。想反查“这块白板挂在哪面墙上”，就读
   ``ax.figure`` 这个属性即可。

--------------

.. _93-数据长度不匹配:

9.3 数据长度不匹配
------------------

.. _931-x-与-y-长度不等--valueerror报错:

9.3.1 ``x`` 与 ``y`` 长度不等 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：\ ``plot``
要求每个横坐标都配一个纵坐标，长度不同直接中断：

.. code:: python

   import matplotlib.pyplot as plt
   import numpy as np
   plt.plot(np.arange(5), np.arange(3))   # x 有 5 个点, y 只有 3 个点

.. code:: text

   ValueError: x and y must have same first dimension, but have shapes (5,) and (3,)
                   ^^^^^^^^^^^^^^^^^^^^^^

**原因**\ ：折线是“把 (x_i, y_i) 逐点连起来”，x 有 5 个点、y 只有 3
个点，从第 4 个点起没有 y 可匹配，Matplotlib
拒绝这种“拄拐杖的线”。关键英文是
**``same first dimension``**——第一条维度的长度必须一样。

**解决办法**\ ：先 ``print(len(x), len(y))`` 或 ``x.shape, y.shape``
核对；最常见的元凶是切片没对齐或 ``y`` 用了
``[:-1]``\ （少一个尾点）。气象里“逐日温度比降水多一天”很常见，用
``min(len(x),len(y))`` 切片到一致再画。

.. code:: python

   n = min(len(x), len(y))
   ax.plot(x[:n], y[:n])

..

   **气象场景一句话**\ ：365 天的气温曲线，可 ``y`` 是从第 2
   天到某天的“日距”只切出 364 个点——像把 365 天的雷达回波和 364
   天的资料拼同一张图，尾巴一天对不上，报错正是“你没有给第 365
   天配好配对点”。

--------------

.. _932-plot-传列名校对不上--把字符串当数值--keyerror-或静默类别轴:

9.3.2 ``plot`` 传列名校对不上 / 把字符串当数值 → ``KeyError`` 或静默类别轴
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：从 dict / pandas 里取两列画年周期，列名拼错：

.. code:: python

   d = {"temp": [1, 2, 3, 4, 5]}
   plt.plot(d["temp"], d["hum"])      # "hum" 这一列不存在

.. code:: text

   KeyError: 'hum'

**原因**\ ：\ ``d["hum"]`` 在字典里查不到键，是 ``KeyError``\ （查第 7
章），跟你数据多长无关。真正“不报错但错”的是把字符串列当
x：\ ``ax.plot(['0','1','2','3'], [0,1,4,9])``
会把字符串当\ **类别轴**\ ，x 轴刻度不是你想象的 0,1,2,3
数值，而是“按字符串排序的标签”（静默、可塑错）。

**解决办法**\ ：把列取进手里再画，先确认
``d.keys()``\ ；要用数值轴，先把 x 列转成数值
``x = d["t"].astype(float)``\ 。

   **气象场景一句话**\ ：手动抄了“湖站、兰州、张掖、敦煌”四个站名当横轴，图上刻度却是字符串排出来的——拿字符串当坐标就像拿台站中文名当经纬度，Matplotlib
   只能当“分类标签”处理，画出来跟你想的数值坐标差之千里。

--------------

.. _933-二维数组被当成多条曲线静默:

9.3.3 二维数组被当成“多条曲线”（静默！）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：\ ``plot`` 传二维 ``y``\ ，Matplotlib
**不报错**\ ，而是把\ **每一列当一条曲线**\ （矩阵是（行,
列），每列一条线）：

.. code:: python

   mat2d = np.arange(12).reshape(3, 4)     # (3,4)
   fig, ax = plt.subplots()
   ax.plot(mat2d)                          # 不报错, 但画出 4 条线
   print(len(ax.lines))                    # 4, 每条线的 x 默认是 0,1,2

.. code:: text

   4

但若 x 长度对不上列数，才终于报：

.. code:: python

   plt.plot(np.arange(10), np.arange(12).reshape(3, 4))

.. code:: text

   ValueError: x and y must have same first dimension, but have shapes (10,) and (3, 4)

**原因**\ ：\ ``plot`` 对 ``ndim=2`` 的 ``y`` 会自动逐列画（隐式
``.T``\ ），行数成了隐式 x 的长度。所以 (3,4) 会画出 **4
条**\ 线（每列一条，x=0,1,2）。它不报错，只是“悄悄多画了好几条”——这是典型的\ **静默错值**\ 。

**解决办法**\ ：确认
``y.ndim``\ 。要画\ **一条**\ 序列，先把矩阵拉成一维 ``y.ravel()`` /
``y.flatten()``\ ；要画多列就把每列单独 ``ax.plot(x, col)``\ 。

   **气象场景一句话**\ ：你把一个“5 天 × 3 站”的气温矩阵直接
   ``plot``\ ，以为画一条时间序列，结果 Matplotlib
   帮你按站点“每站一条线”画了 3
   条（列数条）——图上一夜之间多出一堆线，\ ``len(ax.lines)``
   是点破它的第一照妖镜。

--------------

.. _934-scatter-的-xy-长度不等--valueerror报错:

9.3.4 ``scatter`` 的 ``x``/``y`` 长度不等 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：散点图每个点也要求 x、y 一一配对，报错措辞和
``plot`` 不一样：

.. code:: python

   plt.scatter([1, 2, 3], [1, 2])     # 3 个 x, 2 个 y

.. code:: text

   ValueError: x and y must be the same size
                      ^^^^^^^^^^^^^^^^^^^^^

**原因**\ ：\ ``scatter`` 用 ``x`` 和 ``y``
分别是散点的横纵坐标，\ ``x`` 多一个点、\ ``y``
少一个点，点就对不齐。关键英文是 **``the same size``**\ （和 ``plot`` 的
``same first dimension`` 措辞不同，但意思都是长度必等）。

**解决办法**\ ：核对长度后取交集 ``n = min(len(x), len(y))``\ ，用
``x[:n]``\ 、\ ``y[:n]``\ 。

   **气象场景一句话**\ ：日最高温 (60 天) 对日最低温 (59 天)
   做相关散点，最后一个点凭空少个配对——一张“错位的相关点云”，\ ``must be the same size``
   就是点名你少配了一天。

--------------

.. _94-坐标轴与刻度:

9.4 坐标轴与刻度
----------------

.. _941-set_xlim--set_ylim-顺序写反--静默反转坐标轴:

9.4.1 ``set_xlim`` / ``set_ylim`` 顺序写反 → 静默反转坐标轴
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：\ ``set_xlim(右, 左)`` 或 ``set_ylim(上, 下)``
顺序写反\ **不报错**\ ，Matplotlib 静默把该坐标轴反向：

.. code:: python

   x = np.arange(1, 32); t = 15 + 3.5*np.sin(2*np.pi*x/31)
   fig, ax = plt.subplots()
   ax.plot(x, t)
   ax.set_xlim(31, 1)          # 想 [1,31], 却写反
   print(ax.get_xlim())

.. code:: text

   (np.float64(31.0), np.float64(1.0))    # x 轴被静默反转

**原因**\ ：\ ``set_xlim(left, right)``
两个参数是“左端点、右端点”。写成升序它正常，写成降序它就\ **让 x
轴反过来**\ （这是合法功能，有时故意用来看序列回放）。因为不报错，最容易漏看。

**解决办法**\ ：写 ``ax.set_xlim(1, 31)``
保持增序；若只想“固定范围、不理会顺序”，可先 ``lo, hi = min(x), max(x)``
再 ``ax.set_xlim(lo, hi)``\ 。

   **气象场景一句话**\ ：时间序列的“1 月 → 12 月”被写成
   ``31 → 1``\ ，整条气温曲线横着倒着走，冬夏曲线反过来——程序不拦你，全靠
   ``get_xlim()`` 回读，是第 9 章最典型的“静默轴反转”之一。

--------------

.. _942-set_xticks-与-set_xticklabels-个数不匹配--valueerror报错:

9.4.2 ``set_xticks`` 与 ``set_xticklabels`` 个数不匹配 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：手动设了 5 个刻度，却只给 3 个标签：

.. code:: python

   fig, ax = plt.subplots()
   ax.set_xticks([1, 2, 3, 4, 5])
   ax.set_xticklabels(["a", "b", "c"])    # 3 个标签 vs 5 个刻度

.. code:: text

   ValueError: The number of FixedLocator locations (5), usually from a call to set_ticks,
               does not match the number of labels (3).
                                           ^^^^^^^^^^

**原因**\ ：\ ``set_xticklabels``
要求标签个数和刻度个数\ **一一对应**\ ，多/少都会直接报
``does not match the number of labels``\ 。老版本曾静默补空，新版本（3.10）改为硬报错。

**解决办法**\ ：要么标签数与 ``set_xticks``
的刻度数一致，要么只写一个刻度就配几个标签；不想自己数，可让 Matplotlib
自动刻度再用 ``.set_xticklabels``\ （此时个数天然匹配）。

   **气象场景一句话**\ ：你要在 x
   轴上标“1月、4月、7月、10月、1月”五个点，却只给三张“月份牌”贴到五个钉上——钉子的位置（ticks）数和牌子数对不上，Matplotlib
   当场把你叫停，\ ``does not match the number of labels``
   就是“牌子不够/多了”的判词。

--------------

.. _943-locator--formatter-未导入--刻度旋转参数:

9.4.3 ``locator`` / ``formatter`` 未导入 & 刻度旋转参数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象**\ 一（未导入）：把 ``matplotlib.ticker`` 里的
``MultipleLocator``\ 、\ ``FuncFormatter`` 当“自带全局”，没 ``import``
就 ``NameError``\ 。其实它们需要显式导入：

.. code:: python

   from matplotlib.ticker import MultipleLocator, FuncFormatter   # 不导入会 NameError
   ax.xaxis.set_major_locator(MultipleLocator(5))                # 每 5 个单位一个大刻度

**现象**\ 二（旋转参数挂错方法）：想让日期标签竖着，新手会到处找
``rotation=`` 参数并写错方法。正确的是
``plt.xticks(rotation=45)``\ （pyplot 版，作用于当前轴），或针对某个轴：

.. code:: python

   plt.xticks(rotation=45)                                  # 可行, 转 45°
   # 或 (最省心, 常配 datetime):
   fig.autofmt_xdate()

**原因 / 解决办法**\ ：\ ``set_xticklabels(..., rotation=45)``
其实也可用，但新手常把 ``rotation`` 误写到 ``set_xticks``\ （那里没有
rotation 参数）。碰到
``TypeError: ... got an unexpected keyword argument 'rotation'``\ ，先想这个参数到底挂在哪个方法上——``rotation``
是“排版标签的方向”，属于 ``set_xticklabels`` / ``plt.xticks`` /
``fig.autofmt_xdate``\ ，不属于“放钉子的位置” ``set_xticks``\ 。

   **气象场景一句话**\ ：夏至前后航天日期的 x
   轴标签堆成一团，你要的是“转 45°
   排队排开”——旋转是标签排版（\ ``set_xticklabels``\ ）的能力，不是“放钉子的位置”（\ ``set_xticks``\ ）的能力，放错地方自然被打回
   ``unexpected keyword argument``\ 。

--------------

.. _944-刻度太密--自动刻度范围不对用-maxnlocator-限量技巧:

9.4.4 刻度太密 / 自动刻度范围不对：用 ``MaxNLocator`` 限量（技巧）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：数据范围大到离谱时（如把一天当成一个刻度、跨度
10^5 甚至 10^15），Matplotlib 默认的 ``MaxNLocator``
会自动\ **限量**\ 到十几个刻度，并不会一股脑全塞进去（实测）：

.. code:: python

   from matplotlib.ticker import MaxNLocator
   for dl in (MaxNLocator(integer=True, steps=[1,2,4,5,10]),
              MaxNLocator(integer=True),
              MaxNLocator(integer=True, nbins=10)):
       v = dl.tick_values(0, 100000)
       print(len(v), "个刻度")

.. code:: text

   11 个刻度
   11 个刻度
   11 个刻度

**原因 / 解决办法**\ ：\ ``MaxNLocator``
会尽量选“好读的整数步长”并把刻度数控制在一个健康范围内（\ ``nbins``
决定最多几个）。所以“刻度太多”一般不靠它报错，而是\ **你想要的刻度间隔并不漂亮**\ （如跨月和跨年混排、粒度不对）。气象排图碰到“时间轴刻度乱”时，别指望自动刻度，显式给刻度策略：

- 日期轴用 ``mdates.MonthLocator()`` / ``YearLocator()`` +
  ``DateFormatter``\ （见 9.9.1）；
- 想每 N 个单位一个大刻度用 ``MultipleLocator(N)``\ ；要自定义文本用
  ``FuncFormatter``\ ；
- 偷懒版先看 ``len(ax.get_xticks())``
  到底几个，别让日期标签糊成一团还以为是数据错。

..

   **气象场景一句话**\ ：自动刻度像“智能取整的尺子”，跨度和步长不搭时它只给你十来个刻度，看着稀疏但日期语义全乱——天气预报图要按“时次/日/月”这种气象节奏落刻度，就得人工派
   ``MonthLocator`` 这类“刻度管家”去管时间轴，而不是让通用刻度自己硬配。

--------------

.. _95-colorbar-与图例:

9.5 colorbar 与图例
-------------------

.. _951-figcolorbarax-传错了对象--attributeerror报错:

9.5.1 ``fig.colorbar(ax)`` 传错了对象 → ``AttributeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：\ ``colorbar``
只能挂在\ **带颜色映射的图**\ （\ ``imshow``\ 、\ ``contourf``\ 、\ ``scatter``
的 ``c=``\ ）上，你把 ``ax`` 传给 ``fig.colorbar``\ ：

.. code:: python

   fig, ax = plt.subplots()
   ax.plot([1,2,3],[1,4,2])       # 普通折线, 没有颜色映射
   fig.colorbar(ax)               # 错: 传了 Axes

.. code:: text

   AttributeError: 'Axes' object has no attribute 'cmap'

**原因**\ ：\ ``colorbar`` 需要一个\ **ScalarMappable**\ （内部有
``cmap``\ 、\ ``norm`` 的对象，即 ``im`` / ``cf`` / 散点的
``sc``\ ），而 ``ax`` 是 ``Axes``\ ，没有 ``cmap`` 属性 → 一取 ``cmap``
就报 ``AttributeError``\ 。

**解决办法**\ ：把“存返回值的那个对象名”传给 ``colorbar``\ ：

.. code:: python

   im = ax.imshow(grid)          # 把 imshow 的返回值存下来
   fig.colorbar(im, ax=ax)       # 正确, colorbar 挂在 im 上

.. code:: python

   cf = ax.contourf(xx, yy, zz, levels=8)        # contourf 同理
   fig.colorbar(cf, ax=ax)
   sc = ax.scatter(x, y, c=temp, cmap="turbo")   # scatter 同理
   fig.colorbar(sc, ax=ax)

..

   **气象场景一句话**\ ：\ ``colorbar``
   像“给色块图配一张颜色-数值对照表”，你得把有颜色的那张图（\ ``im/cf/sc``\ ）交给它；把一块空白白板
   ``ax`` 递过去，它要取色板却摸了个空——``no attribute 'cmap'``
   就是“这图根本没有色版可配”。

--------------

.. _952-pltcolorbar-当前图没有任何-mappable--runtimeerror报错:

9.5.2 ``plt.colorbar()`` 当前图没有任何 mappable → ``RuntimeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：\ ``plt.colorbar()``
不带参数想“自动找图配色标”，可前面只画了普通曲线：

.. code:: python

   import matplotlib.pyplot as plt
   plt.colorbar()     # 前面没有 imshow/contourf/scatter 之类的图

.. code:: text

   RuntimeError: No mappable was found to use for colorbar creation. First define a mappable such
                 as an image (with imshow) or a contour set (with contourf).

**原因**\ ：\ ``plt.colorbar()`` 不接参数时会去
Matplotlib“当前状态”自动找最近一个有颜色映射的图；找不到就报
``RuntimeError``\ 。关键英文是 **``No mappable was found``**\ 。

**解决办法**\ ：规范写法永远用 ``fig.colorbar(im, ax=ax)`` 显式把
mappable 递进去，别依赖“自动找”（那依赖全局状态，多子图时最容易找错）。

   **气象场景一句话**\ ：你在中间画了折线又画了 ``contourf``\ ，却想让
   ``plt.colorbar()``
   自己猜给哪个场配色板——它就像末班地铁里没人告诉它“去备图面板取哪张”，只好喊一句
   ``No mappable``\ （没有可配色的对象）。

--------------

.. _953-曲线没写-label-就-legend--userwarning-no-artists-with-labels警告:

9.5.3 曲线没写 ``label`` 就 ``legend()`` → ``UserWarning: No artists with labels``\ （警告）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：\ ``ax.plot`` 没写 ``label=``\ ，随后
``ax.legend()`` 不报错，只发一条 ``UserWarning``\ ，图上没有图例条目：

.. code:: python

   fig, ax = plt.subplots()
   ax.plot([1,2],[1,2])          # 没写 label
   ax.legend()                   # 找不到有 label 的线条

.. code:: text

   UserWarning: No artists with labels found to put in legend.  Note that artists whose label start
                with an underscore are ignored when legend() is called with no argument.
                ^^^^^^^^^^^^^^^^^^^^^^^^^

**原因**\ ：\ ``legend()`` 不传参数时，自动收集当前轴上\ **带 ``label=``
的图元**\ ；一条线都没给 ``label``\ ，它一无所获就发
``No artists with labels ... to put in legend``\ （\ **注意以 ``_``
开头的 label 也会被忽略**\ ）。

**解决办法**\ ：

- 画图时给每条曲线 ``label="逐日平均温"``\ ，然后统一
  ``ax.legend()``\ ；
- 或手动传 ``ax.legend([line1, line2], ["气温", "降水"])``\ （handles 与
  labels 要等长，见 9.5.4）。

..

   **气象场景一句话**\ ：你画了三条要素曲线却不告诉 ``legend``
   谁是谁（没写
   ``label``\ ），它自然没内容可展示——就像没排门牌号的天气图例，读者只能靠猜颜色对应什么物理量。

--------------

.. _954-legend-的-handles--labels-数量错配--静默截断:

9.5.4 ``legend`` 的 ``handles`` / ``labels`` 数量错配 → 静默截断
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：手动传 handles 与 labels
数量不等，\ **不报错**\ ，只按少的那个截取：

.. code:: python

   fig, ax = plt.subplots()
   ln1, = ax.plot([1,2],[1,2], label="a")
   ln2, = ax.plot([1,2],[2,1], label="b")
   lg = ax.legend([ln1, ln2], ["A"])      # 2 个 handle, 1 个 label
   print(len(lg.legend_handles))          # 只有 1 条进图例

.. code:: text

   1

**原因**\ ：\ ``legend(handles, labels)``
会把两者“按位置配对”，多出的那只 handle
没有标签名字就悄悄丢弃，\ ``legend_handles`` 只剩 1 条——程序完全不吭声。

**解决办法**\ ：牢记 ``handles`` 与 ``labels``
**一一对应、等长**\ ；最稳的做法是“写 ``label=`` 再 ``ax.legend()``
自动配对”，避免手工两列错位。

   **气象场景一句话**\ ：你给图例递了“三条线的句柄”却只配了“两个名字”，多的那条线成了无名英雄被悄悄请出图例——排错时数
   ``len(legend_handles)`` 一眼就抓出“有曲线没名字”。

--------------

.. _955-loc-参数拼错--valueerror报错:

9.5.5 ``loc`` 参数拼错 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 /
真实报错信息**\ ：\ ``loc="uper right"``\ （字母颠倒）等拼错的字符串会被严格校验：

.. code:: python

   fig, ax = plt.subplots()
   ax.plot([1,2],[1,2], label="a")
   ax.legend(loc="uper right")     # 应为 "upper right"

.. code:: text

   ValueError: 'uper right' is not a valid value for loc; supported values are 'best', 'upper right',
               'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right',
               'lower center', 'upper center', 'center'

**原因**\ ：\ ``loc``
只接受上面这串\ **白名单**\ 字符串，拼错任意字符都触发
``ValueError``\ （\ ``not a valid value``\ ）。还想用 ``loc="best"``
自动避让最省心。

**解决办法**\ ：从报错里列出的 supported values 里抄一个；想放图外，用
``bbox_to_anchor=(1.02, 1)`` 结合 ``loc="upper left"``\ 。

   **气象场景一句话**\ ：心想图例放“右上”，手一抖打了
   ``uper right``\ ，像把台站的“upper
   right”写成错别字——坐标名不能有歧义，Matplotlib
   报出完整可选清单正是为了让你从白名单里重新挑。

--------------

.. _96-绘图函数敲错--参数差异:

9.6 绘图函数敲错 / 参数差异
---------------------------

.. _961-pltscatter-多一个-s-成-scatters--attributeerror报错:

9.6.1 ``plt.scatter`` 多一个 ``s`` 成 ``scatters`` → ``AttributeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：方法名多打一个 ``s``\ ：

.. code:: python

   import matplotlib.pyplot as plt
   plt.scatters([1,2],[1,2])     # 没有 scatters 这个函数

.. code:: text

   AttributeError: module 'matplotlib.pyplot' has no attribute 'scatters'

**原因**\ ：\ ``matplotlib.pyplot`` 模块里函数名是精确的
``scatter``\ ；你拼的 ``scatters`` 不存在，模块就报
``has no attribute 'scatters'``\ 。关键英文 ``has no attribute``
说明“模块里没这个名字”。

**解决办法**\ ：\ ``plt.scatter`` /
``ax.scatter``\ （对象接口：\ ``ax.scatter(tmin, tmax, c=month, cmap="turbo")``\ ）。拼错多半是把“复数概念”加了
s——函数名\ **不加复数后缀**\ 。

   **气象场景一句话**\ ：想把“日最高温 vs 日最低温”点云画出来，手滑把
   ``scatter`` 打成 ``scatters``——``plt`` 这位制图员没有叫 ``scatters``
   的手艺，报 ``has no attribute`` 提醒你“查查是不是多打了个
   s”。养成看补全提示再下笔的习惯。

--------------

.. _962-axhist-与-nphistogram-参数差异normed-已废弃报错:

9.6.2 ``ax.hist`` 与 ``np.histogram`` 参数差异：\ ``normed`` 已废弃（报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：把 ``np.histogram`` 的老习惯往 ``ax.hist``
里塞，用废弃参数 ``normed=True``\ ：

.. code:: python

   data = np.random.default_rng(1).normal(15, 3, 200)
   fig, ax = plt.subplots()
   ax.hist(data, bins=20, normed=True)     # normed 已被 density 取代

.. code:: text

   AttributeError: Rectangle.set() got an unexpected keyword argument 'normed'

**原因**\ ：\ ``ax.hist`` 的老参数 ``normed`` 早在老版本就改为
``density``\ （\ ``np.histogram``
亦然）。\ ``Rectangle.set() got an unexpected keyword argument 'normed'``
就是“这个方柱不接受 ``normed`` 这个参数”。

**另注意**\ ：两者\ **返回值不同**\ ，别混：

- ``np.histogram(data, bins=20)`` 只\ **计算**\ ，返回 **2
  个对象**\ ：\ ``(counts, edges)``\ ；
- ``ax.hist(data, bins=20)`` **画出并计算**\ ，返回 **3
  个对象**\ ：\ ``(n, bins, patches)``\ （频数、边界、每个方柱对象）。

.. code:: python

   hist, edges = np.histogram(data, bins=20)     # 2 个返回值
   n, b, paths = ax.hist(data, bins=20)          # 3 个返回值

**解决办法**\ ：要画图用
``ax.hist(data, bins=20, density=True)``\ （\ ``density``
把纵轴换成分布概率密度）；想画《全年气温分布、双峰偏态》用
``ax.hist(day_mean, bins=30, edgecolor="white", alpha=0.9)``\ （正文示例）。

   **气象场景一句话**\ ：直方图是“气温大多待在几度这一档”的统计条，\ ``ax.hist``
   是“画 + 数”一体，\ ``np.histogram`` 只是“数”不算“画”。把 ``normed``
   当成通用参数塞给画图方法，新本不给 ``normed`` 这面子，改叫
   ``density``\ 。

--------------

.. _963-contour-vs-contourf--levels-写降序--valueerror报错:

9.6.3 ``contour`` vs ``contourf`` & ``levels`` 写降序 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：\ ``contour``\ （线）和
``contourf``\ （填色）是两种“等值”，\ ``levels``
是一组\ **严格递增**\ 的等值线值，写成\ **降序**\ 直接报错：

.. code:: python

   import numpy as np
   import matplotlib.pyplot as plt
   xx, yy = np.meshgrid(np.linspace(0, 4, 40), np.linspace(0, 4, 40))
   zz = np.sin(xx) * np.cos(yy)
   fig, ax = plt.subplots()
   ax.contourf(xx, yy, zz, levels=np.linspace(1, -1, 10))   # 递减!

.. code:: text

   ValueError: Contour levels must be increasing
                            ^^^^^^^^^^^^^^

**原因**\ ：等值线（色）按“从小到大”一层层爬（低→高），\ ``levels``
必须严格递增；写成降序（\ ``1,0,-1,...``\ ）让哪层该在哪层的上下关系一团糟，Matplotlib
直接 ``ValueError``\ 。关键词 **``levels must be increasing``**\ 。

**解决办法**\ ：\ ``levels``
用递增序列：\ ``np.linspace(-1, 1, 10)``\ ；或直接给整数分层
``levels=8``\ （Matplotlib 自动从数据范围取递增层）。

**与 ``contour`` 的取舍**\ ：想要“纯线条等值线”看走势用
``ax.contour``\ ；想要“填色场”看量级用 ``ax.contourf``\ 。气象里
``levels`` 太少（如只给 1 条）会让等值线“破开不成环”，要 ``levels``
给足够多层。

   **气象场景一句话**\ ：气压场从低到高是一级级爬的，你把 ``levels``
   写成从高往低，就像 500hPa
   等压面“层级倒着编”——没了明确的低→高次序，\ ``levels must be increasing``
   是“层级排序错了”的判词，改成 ``np.linspace`` 递增即好。

--------------

.. _964-imshow-的-origin--extent-静默翻转图片:

9.6.4 ``imshow`` 的 ``origin`` / ``extent`` 静默翻转图片
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：\ ``imshow`` 默认 ``origin="upper"``\ （第 1
行在顶），二维数组的第 0 行画在最上面；想按“左上角经纬度”定义范围用
``extent``\ ，若把纬度范围写反，图片会\ **上下颠倒**——全程不报错：

.. code:: python

   d = np.arange(100).reshape(10, 10)
   fig, ax = plt.subplots()
   # 想经度 40~50, 纬度升序 30~35; 误写成 lat 降序 [35,30]
   ax.imshow(d, origin="upper", extent=[40, 50, 35, 30])

.. code:: text

   (不报错, 但图上下颠倒: 因为 extent 里 y 从 35 到 30 递减, 常见 lat 递增被反)

**原因 / 解决办法**\ ：\ ``origin``
决定“首行数据的像素列是从顶排还是从底排”（气象类数据几乎都要
``origin="lower"``\ ），\ ``extent=[x0, x1, y0, y1]``
决定每格对应的经纬度框。只要 ``y0>y1``\ （纬度倒着写），Matplotlib
就当“图本来就是反的”照画——**静默**\ 。

- 数据数组第 0 行对应“最南/最下”，就 ``origin="lower"``\ ；
- ``extent``
  里\ **经度、纬度各自升序**\ ：\ ``extent=[lon_min, lon_max, lat_min, lat_max]``\ ；
- 存图后立刻肉眼核对整幅是“上北下南”。

..

   **气象场景一句话**\ ：雷达反射率格点第 0 行是“最南侧”，你要
   ``origin="lower"``\ ；若还忘了它的 ``extent``
   纬度范围应从南到北升序，图就会上下倒置——像把一张北纬站点地图倒着贴，\ ``imshow``
   不拦你，全靠“北纬数字升序才是正常”的常识和核对。

--------------

.. _965-imshow--contourf-遇-nan白斑破洞vminvmax-色标错位静默:

9.6.5 ``imshow`` / ``contourf`` 遇 NaN：白斑、破洞、\ ``vmin/vmax`` 色标错位（静默）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：彩图数据里有 ``NaN``\ （缺测）格，\ ``imshow``
默认用 ``cmap`` 的“坏色”（常是透明的）显示，\ ``contourf`` 则在 NaN
位置\ **破洞不闭合**\ ，图上一块块白斑——全程无警告：

.. code:: python

   dd = np.random.rand(10, 10)
   dd[3,3] = np.nan; dd[7,7] = np.nan     # 两个缺测格
   fig, ax = plt.subplots()
   ax.imshow(dd, cmap="viridis")           # NaN 格以"坏色/透明"出现

.. code:: text

   (不报错; 图中两格透明/留白, 缺陷一目了然或漏看不思)

**原因**\ ：\ ``NaN`` 没有数值，无法映射到某个颜色档位；Matplotlib
默认把这类数据格画成 ``cmap.set_bad``
指定色（默认透明/留白）。\ ``contourf`` 需要连续数据插值等值，碰 NaN
那圈就画不出闭合层 → 白洞。\ **``vmin``/``vmax``** 没设时自动按数据
min/max 定色标；一旦数据里藏
NaN/极端异常值，色标会自动被拉到异常范围，颜色看起来全糊。

**解决办法**\ ：

- 画图前显式遮罩缺测：\ ``data = np.where(np.isfinite(data), data, np.nan)``\ ，并
  ``im.set_bad('0.8')`` 让缺测格呈浅灰而非刺眼白；
- 统一色标范围用
  ``vmin, vmax = np.nanmin(dd), np.nanmax(dd)``\ （\ ``nanmin/nanmax``
  躲开 NaN），再 ``imshow(..., vmin=..., vmax=..., cmap="RdBu_r")``\ ；
- 多子图想同比色标（PPT 36~39 的 ``Normalize`` / ``levels``
  话题），给所有子图用\ **同一 ``vmin/vmax``**\ 。

..

   **气象场景一句话**\ ：西北 8 站有一个站当天缺测（NaN），你 ``imshow``
   一画，那块缺测格透明漏出底子，\ ``contourf``
   在那直接破个大白洞——像地面填图刮掉一块。图不报错，全靠你盯“图上凭什么有洞
   / 有刺眼的影”反查 NaN，再配合 ``vmin/vmax``
   把色标按真实物理范围定死。

--------------

.. _97-保存与显示:

9.7 保存与显示
--------------

.. _971-savefig-目录不存在--filenotfounderror报错:

9.7.1 ``savefig`` 目录不存在 → ``FileNotFoundError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：保存路径的\ **文件夹**\ 不存在，Matplotlib
不会自动建目录，直接报找不到文件：

.. code:: python

   fig, ax = plt.subplots(); ax.plot([1,2],[1,2])
   fig.savefig(r"...\sim\no_such_dir\a.png")

.. code:: text

   FileNotFoundError: [Errno 2] No such file or directory: 'D:\\Code\\Vibe\\QA\\_sim\\no_such_dir\\a.png'

**原因**\ ：\ ``savefig``
只负责“往这个路径写文件”，不负责“先造好这个文件夹”；目录不存在 →
``FileNotFoundError``\ 。Windows 下反斜杠、\ ``/`` 都行。

**解决办法**\ ：保存前先 ``os.makedirs(路径, exist_ok=True)``\ ：

.. code:: python

   import os
   os.makedirs(r"...\sim\sub", exist_ok=True)
   fig.savefig(r"...\sim\sub\a.png")   # 现在能存了

..

   **气象场景一句话**\ ：你用 ``savefig`` 想把图“分站存到 8
   个站点文件夹”，却忘了随手新建 ``site_3``
   这个目录——像给文件柜订了个不存在的抽屉，\ ``No such file or directory``
   就是“这抽屉还没打”，先 ``makedirs`` 再开口。

--------------

.. _972-参数拼错bbox_inches-写成-bound_inches--typeerror报错:

9.7.2 参数拼错：\ ``bbox_inches`` 写成 ``bound_inches`` → ``TypeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：想裁掉图边空白，把 ``bbox_inches`` 拼成
``bound_inches``\ ：

.. code:: python

   fig, ax = plt.subplots(); ax.plot([1,2],[1,2])
   fig.savefig(r"...\sim\_t7.png", bound_inches="tight")

.. code:: text

   TypeError: FigureCanvasAgg.print_png() got an unexpected keyword argument 'bound_inches'

**原因 / 解决办法**\ ：\ ``savefig`` 内部转到后端 ``print_png()``
等，参数名是精确的 ``bbox_inches``\ ；拼错成 ``bound_inches`` 不存在 →
``got an unexpected keyword argument``\ 。写到
``bbox_inches="tight"``\ （把图裁到贴合内容、四周不留白，正文最佳实践：\ ``savefig("a.png", bbox_inches="tight", dpi=150)``\ ）。

   **气象场景一句话**\ ：\ ``bbox_inches``
   是“把图画边裁成贴合内容”的金标准参数，手滑把 bbox 拼成 bound
   让后端措手不及——``unexpected keyword argument``
   就是“我没见过这个名字”，改正拼写即通。

--------------

.. _973-保存格式后缀不支持--valueerror报错:

9.7.3 保存格式后缀不支持 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：后缀名不在支持列表里：

.. code:: python

   fig, ax = plt.subplots(); ax.plot([1,2],[1,2])
   fig.savefig("demo_bad.xyzz")     # 不是图片格式

.. code:: text

   ValueError: Format 'xyzz' is not supported (supported formats: eps, jpeg, jpg, pdf, pgf, png, ps,
               raw, rgba, svg, svgz, tif, tiff, webp)

**原因 / 解决办法**\ ：Matplotlib
按\ **文件名后缀**\ 判断保存成什么格式，给的 ``xyzz`` 不在白名单就
``Format 'xyzz' is not supported``\ （列表还给全了支持的格式让你挑）。用列表里有的后缀（常用
``png``\ 、\ ``jpg``\ 、\ ``pdf``\ 、\ ``svg``\ ）；出版/贴文档用
``dpi>=300`` 的 ``png/jpg``\ ，矢量给 ``pdf/svg``\ 。

   **气象场景一句话**\ ：后缀名就是“图该存成哪种出版格式”的开关，写了个
   ``xyzz`` 像给气象产品定了个不存在的编码——``Format not supported``
   把能用的格式名单抛给你，照抄一个即可。

--------------

.. _974-dpi-太低模糊--pltshow-与-savefig-顺序:

9.7.4 ``dpi`` 太低模糊 & ``plt.show()`` 与 ``savefig`` 顺序
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：\ ``dpi``\ （默认 72~100）太低时 PNG
放大糊成马赛克；更坑的是\ **只 ``plt.show()`` 不 ``savefig``**\ ，或先
``plt.show()`` 后 ``savefig`` 把画布关了导致空图：

.. code:: python

   fig, ax = plt.subplots(); ax.plot([1,2],[1,2])
   fig.savefig("low.png", dpi=72)        # 72 dpi -> 小又糊
   fig.savefig("hi.png", dpi=300, bbox_inches="tight")   # 清晰

.. code:: text

   (72 dpi 图小糊、300 dpi 图清晰, 不报错, 但输出差距巨大)

**解决办法**\ ：出版/论文图 ``dpi=300`` 起步；截屏预览先 ``plt.show()``
看完，定稿务必 ``savefig(...)``\ 。\ **顺序**\ ：\ ``plt.show()``
默认会“结束并关闭当前画布”，一般应\ **先 ``savefig`` 再
``plt.show()``**\ ；批处理画完还要 ``plt.close(fig)`` 回收内存，否则循环
100 张图内存爆表（正文最佳实践最后一条）。

.. code:: python

   fig.savefig(out_png, bbox_inches="tight", dpi=150)   # 先存
   plt.show()                                            # 后看
   plt.close(fig)                                        # 最后回收

..

   **气象场景一句话**\ ：冬夏两季图 dpi 只有
   72，放大投到报告里糊成一团；或批处理里只 ``show()`` 没
   ``savefig``\ ，一百张图一闪而过一个文件都没落盘。气象出图三件套——先
   ``savefig`` 定稿、\ ``plt.close`` 回收、\ ``dpi``
   按用途定——一次写全。

--------------

.. _98-子图布局:

9.8 子图布局
------------

.. _981-布局混用constrained_layouttrue-后又调-figtight_layout--userwarning警告:

9.8.1 布局混用：\ ``constrained_layout=True`` 后又调 ``fig.tight_layout()`` → ``UserWarning``\ （警告）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：开头用了
``constrained_layout=True``\ ，收尾却又补一句
``fig.tight_layout()``\ ，两种自动布局打架，Matplotlib 发一条
``UserWarning``\ 、\ **退回一种布局**\ （程序照跑）：

.. code:: python

   import matplotlib.pyplot as plt
   fig, ax = plt.subplots(constrained_layout=True)   # 已要求 constrained 布局
   ax.plot([1, 2])
   fig.tight_layout()                                # 又手动调 tight 布局 — 冲突!

.. code:: text

   UserWarning: The figure layout has changed to tight_layout.

**原因**\ ：一张 ``Figure`` 只能用一种自动布局策略。你又开
``constrained_layout`` 又调 ``fig.tight_layout()``\ ，Matplotlib
只能选一个生效（这里报“布局已改为
tight_layout”），另一个被静默放弃。初学者常“保险起见”叠加多个布局函数，反而触发这种
layout 冲突警告。

**解决办法**\ ：布局二选一——要么在 ``subplots(constrained_layout=True)``
一路走到底（后来也别再 ``tight_layout``\ ），要么就只用收尾的
``fig.tight_layout()``\ ；\ **不要混用**\ 。真遇“colorbar
把子图挤没地方”，用 ``fig.colorbar(im, ax=axes, shrink=0.8)``
给色标留空间，或手动 ``fig.subplots_adjust()`` 排版。

   **气象场景一句话**\ ：\ ``constrained_layout`` 和 ``tight_layout``
   是两位都想替你排版的“自动排版员”，你同时请两位上岗，图板只会听最后发话那位。气象多子图（折线+散点+直方图+箱线）里，认准一个排版负责人写到底，别贪心全上。

--------------

.. _982-add_subplot-序号越界--valueerror报错:

9.8.2 ``add_subplot`` 序号越界 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：\ ``add_subplot(行,列,序号)`` 里的序号从 1
数到 ``行*列``\ ，超出就报：

.. code:: python

   fig = plt.figure()
   ax1 = fig.add_subplot(2,2,1); ax2 = fig.add_subplot(2,2,2)
   bad = fig.add_subplot(2,2,9)     # 2x2=4, 最多 4

.. code:: text

   ValueError: num must be an integer with 1 <= num <= 4, not 9

**原因 / 解决办法**\ ：\ ``add_subplot`` 的 ``num``
是“第几个格子”，合法区间 ``1..行*列``\ ；9 超出 →
``num must be an integer with 1 <= num <= 4, not 9``\ （报错里把范围
``1..4`` 直接列出来）。先算好总格子数 ``行*列``\ ，序号在其内；或干脆用
``plt.subplots(2,2)`` 一次性拿数组。PPT 里“重叠子图
``add_subplot``\ ”适用场景是\ **要精确叠加**\ 而非布局主图。

   **气象场景一句话**\ ：你要在 2×2 展板上打第 9 个格子，板上只有 4
   格——像给只有四排的雷达扫描层圈里放第五圈，\ ``1 <= num <= 4, not 9``
   已把合法编号写给你。

--------------

.. _983-sharextrue--shareytrue-后刻度消失静默:

9.8.3 ``sharex=True`` / ``sharey=True`` 后刻度“消失”（静默）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：开了 ``sharex=True`` 后，\ **只有最底下的子图保留
x 轴刻度标签**\ ，上面子图的 x 刻度标签被默认隐藏（共享了就不重复画）：

.. code:: python

   fig, axes = plt.subplots(2, 1, sharex=True)
   axes[0].set_xticks([1,2,3]); axes[1].set_xticks([1,2,3])
   axes[0].plot([1,2,3]); axes[1].plot([1,3,2])
   fig.canvas.draw()
   print([t.get_visible() for t in axes[0].get_xticklabels()])
   print([t.get_visible() for t in axes[1].get_xticklabels()])

.. code:: text

   axes[0] 上层 x ticklabel: []                 (被 sharex 共享掉, 不重复画)
   axes[1] 底层 x ticklabel: [True, True, True]

**原因 / 解决办法**\ ：\ ``sharex=True`` 让所有子图\ **共用同一个 x
轴位置/刻度**\ ，默认只保留最下（\ ``labelbottom`` 开启）的那个显示 x
刻度标签，其余隐藏——为了省空间、让刻度对齐好看（正文：共享横轴子图必须
``sharex=True``\ ，让底部 y
对齐）。这通常是\ **预期行为**\ ，别慌。想让上面子图也显示标签，手动
``for t in axes[0].get_xticklabels(): t.set_visible(True)``\ ，但共享的本意就是“只要最下面一行带刻度”。

   **气象场景一句话**\ ：2×2 图板四格共享 ``sharex=True``
   后，除了最底下一行，上面的图的 x
   轴不重复写字，画面立刻清爽——这是功能不是
   bug，像多通道气象图板里“只有最后一张标时间刻度”，别当缺陷删掉
   ``sharex``\ 。

--------------

.. _984-展开-axes用-flat--flatten-而不是逐个-01-手数技巧:

9.8.4 展开 ``axes``\ ：用 ``.flat`` / ``.flatten()`` 而不是逐个 ``[0][1]`` 手数（技巧）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象**\ ：\ ``plt.subplots(2,2)`` 返回二维数组，向
``axes[0,0]...axes[1,1]`` 四格逐个填，手数容易漏/串。

**解决办法**\ ：用 ``axes.flat``\ （省内存）或
``axes.flatten()``\ （返回新数组）逐格填：

.. code:: python

   fig, axes = plt.subplots(2, 2, figsize=(10, 7))
   for ax in axes.flat:          # 二维展平成一列, 逐个
       ax.plot([0,1],[0,1])
   print(axes.shape)             # (2,2)

``axes.flat`` / ``axes.flatten()``
都按“先行后列”展平（左上→右上→左下→右下）。它与 9.2.4
的越界是同一家人：记不清维度永远 ``axes.shape`` 心里有数，再用 ``.flat``
安全遍历。

   **气象场景一句话**\ ：给 2×2
   图板四格分别贴折线、散点、直方、箱线时，\ ``for ax in axes.flat``
   让四格按序逐个到队，谁也不再被手数错位。

--------------

.. _99-气象静默错误无报错但图坐标错:

9.9 气象静默错误（无报错但图/坐标错）
-------------------------------------

.. _991-时间序列-x-轴没配-dateformatter--刻度拥挤数字纹静默:

9.9.1 时间序列 x 轴没配 ``DateFormatter`` → 刻度拥挤、数字纹（静默）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：直接把 ``datetime`` 对象数组当横轴去
``ax.plot``\ ，Matplotlib
能自动画，但默认刻度策略会把日期塞得\ **密密麻麻甚至重叠成一团数字纹**\ ：

.. code:: python

   import matplotlib.dates as mdates
   import datetime
   n = 90
   days = [datetime.date(2001,1,1) + datetime.timedelta(days=i) for i in range(n)]
   fig, ax = plt.subplots(figsize=(9,4))
   ax.plot(days, 15 + 5*np.sin(np.arange(n)/6))
   print(len(ax.get_xticks()))      # 刻度挤成一堆

.. code:: text

   7      # 拥挤的刻度个数(自动策略结果, 日期标签叠成一团)

**原因 / 解决办法**\ ：datetime 数据 Matplotlib
会转成“自世纪起算的天数序数”，配上默认刻度定位会横七竖八摆一堆日期
tick，横轴窄、日期字符串长 => 重叠。配
``MonthLocator``\ （按年/月落点）+ ``DateFormatter``\ （%Y-%m
之类）把刻度稀疏化，再 ``fig.autofmt_xdate()`` 旋转防重叠：

.. code:: python

   ax.xaxis.set_major_locator(mdates.MonthLocator())     # 按月落大刻
   ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
   fig.autofmt_xdate()                                   # 自动旋转日期标签
   ax.set_xlabel("日期"); ax.set_ylabel("气温（℃）")

..

   **气象场景一句话**\ ：90 天逐日温度序列不给布局帮手，x
   轴自己码一堆日期 tick
   挤到互相叠影，像“逐日天气值班表”的日期列被挤成一团墨——``MonthLocator``
   把时间捻成“按月扣”，\ ``autofmt_xdate`` 把标签竖起来，横轴立刻清爽。

--------------

.. _992-用远古日期画-datetime--valueerror-date-ordinal--out-of-range报错:

9.9.2 用远古日期画 datetime → ``ValueError: Date ordinal ... out of range``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：Matplotlib
只能处理一个有限日期范围（公元元年前后），拿远早于世纪起点的日期去画：

.. code:: python

   import datetime
   big = [datetime.datetime(1,1,1) + datetime.timedelta(days=i) for i in range(5)]
   fig, ax = plt.subplots()
   ax.plot(big, [1,2,3,4,5])

.. code:: text

   ValueError: Date ordinal -719162.2 converts to 0000-12-31T19:12:00.000008 (using epoch
   1970-01-01T00:00:00), but Matplotlib dates must be between year 0001 and 99

**原因 / 解决办法**\ ：Matplotlib
内部按“距世纪起点的天数序数”存日期，一旦日期换算出的序数超出可表示范围（\ ``must be between year 0001 and 99``\ ），就
``ValueError``\ 。关键词 **``must be between ... and ...``**
一出，必是日期超出范围。检查日期上/下限是否落在合理年代（气象数据一般
1900–2100）；数据里若混进 ``0000-00`` 之类的脏日期先清洗成 ``NaN``
或正确年份再画。

   **气象场景一句话**\ ：探空/再分析资料里偶有一个 ``0000-01-01``
   的坏日期，一 ``plot`` 就爆
   ``must be between year 0001 and 99``——像自动站报文混入一条史上最早的假记录，先把这种“跨世纪的脏日期”剔除再画时间序列。

--------------

.. _993-contourf-数据含-nan--破洞白斑静默:

9.9.3 ``contourf`` 数据含 NaN → 破洞白斑（静默）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：等值线填色场里若有缺测
NaN，那一圈\ **无法闭合的层**\ 会呈白洞/破边，程序不报错：

.. code:: python

   xx, yy = np.meshgrid(np.linspace(35, 45, 60), np.linspace(20, 40, 60))
   zz = np.sin(xx)*np.cos(yy)
   zz[::7, ::9] = np.nan      # 按规律打出一片洞
   fig, ax = plt.subplots(figsize=(6,5))
   ax.contourf(xx, yy, zz, levels=10, cmap="RdYlBu_r")
   fig.savefig("t9_nan_hole.png")     # 洞处不填色, 呈白斑/破边

.. code:: text

   (不报错; NaN 所在的格子不做等值填充 -> 一张"破了几个洞"的场)

**原因 / 解决办法**\ ：\ ``contourf``
要在连续插值上勾出各等级闭合层，NaN
导致那一圈插值断层、层画不闭，就空出白洞。这与 9.6.5 的 ``imshow``
是同一类“NaN 静默”。画之前显式把缺测处理成 ``np.nan`` 后用
``np.ma.masked_invalid(zz)`` 遮罩，或
``zz = np.where(np.isfinite(zz), zz, np.nan)``\ ；\ ``cmap`` 配
``set_bad``\ （浅灰）让洞不刺眼。\ **原则：绝不 ``fillna(0)`` 假装 0
K**\ ，那只会在等值场上造出假冷核。

   **气象场景一句话**\ ：你把有缺测站的气温格点场直接
   ``contourf``\ ，缺测处破个白洞——像拼图板缺了几块。气象铁律是“缺测就要承认缺测”（标成
   ``NaN``/用 ``mask``\ ），而不是拿 0
   去填成假冷区，填色场一破洞先回头查 ``np.isnan(zz).sum()``\ 。

--------------

.. _994-extent-经纬度范围写反--图片上下左右翻转静默:

9.9.4 ``extent`` 经纬度范围写反 → 图片上下/左右翻转（静默）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：给 ``imshow`` 的 ``extent=[x0,x1,y0,y1]``
里把纬度写成递减，图上下颠倒还不报错（见 9.6.4）：

.. code:: python

   d = np.arange(100).reshape(10,10)
   fig, ax = plt.subplots(figsize=(6,5))
   ax.imshow(d, origin="upper", extent=[40, 50, 35, 30])   # y: 35→30 递减

.. code:: text

   (不报错; 纬度范围反了 => 图上下颠倒, "北"在下面)

**原因 / 解决办法**\ ：\ ``extent`` 里 ``y0``\ 、\ ``y1``
必须按数据行的顺序约定。气象格点若第 0 行是“南行”用 ``origin="lower"``
并让纬度\ **升序** ``[lat_min, lat_max]``\ ；若用 ``origin="upper"``
则纬度降序。想稳，存图后肉眼核对“上北下南”。另一静默坑：\ ``extent=[40,50,35,45]``
却把 East 抄成
West（数值写成西经偶数位），会让整幅图东西向镜像——对台风路径、雷达拼图尤其坑。

   **气象场景一句话**\ ：雷达回波数组第 0 行是最南侧，你要
   ``origin="lower"``\ 、纬度升序；否则整张图头下脚上——像把北半球雷达回波图倒着挂，\ ``imshow``
   一句不吭。存图后盯“上北下南、左西右东”一眼，是最便宜的排雷。

--------------

.. _995-温度和单位标签写错-数据标成-k静默:

9.9.5 温度和单位标签写错：℃ 数据标成 K（静默）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 /
真实输出**\ ：轴标题/图例标注写错了量纲，这在代码里\ **永远不报错**\ ，只有图读者能发现，或靠你自查数据与单位的一致性：

.. code:: python

   fig, ax = plt.subplots()
   ax.plot([1, 2], [280, 290])     # 数据其实是 K 的曲线的绝对值, 却想当 ℃
   ax.set_ylabel("气温（K）")       # 轴标签标的是 K

.. code:: text

   (不报错; 图注写 "K" 而心里当 ℃, 读者会被误导)

**原因 /
解决办法**\ ：轴名、图例、标题都是“你写什么是什么”的文本；开尔文/摄氏度的换算（T[K]
= T[℃] +
273.15）不会被自动检查。这是典型\ **静默错值**\ 。画之前统一“这是什么物理量、什么单位”，轴标签如
``"气温（℃）"`` 或 ``"气温（K）"``\ ；若两端数据单位不同，先显式
``temp_c = temp_k - 273.15`` 并加注释。至少每张图加一句单位备注。

   **气象场景一句话**\ ：再分析资料给的是 K，你直接叠线却没换算成 ℃
   又标成“℃”，曲线形状没错但绝对值全错——像把绝对温标当摄氏温标贴标签，图漂亮的假象最危险。动手前先默念“单位定生死”。

--------------

.. _996-双轴-twinx-未分色两套刻度混淆静默:

9.9.6 “双轴 twinx” 未分色：两套刻度混淆（静默）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：温度 ℃ 与降水 mm
各走左右纵轴（\ ``twinx``\ ），若不按颜色区分两套刻度和曲线，读者分不清哪个刻度属于哪条线——不报错：

.. code:: python

   fig, ax1 = plt.subplots(figsize=(8,4))
   ax1.plot([1,2,3],[15,20,18], color="tab:red")          # 气温
   ax2 = ax1.twinx()                                       # 另起右纵轴
   ax2.bar([1,2,3],[10,40,6], alpha=0.3)                   # 降水
   ax1.set_xlabel("日期（日）"); ax1.set_ylabel("气温（℃）")
   ax2.set_ylabel("降水（mm）")

.. code:: text

   (不报错; 若不再给右轴 tick 也着色, 左红右蓝刻度混在一起难读)

**原因 / 解决办法**\ ：\ ``twinx()`` 生成一个共享横轴、独占右纵轴的
``ax2``\ 。正文最佳实践强调：\ **两轴用颜色区分**\ （左轴标题/刻度一种色，右轴一种色），\ ``tick_params(axis="y", colors=...)``
分别上色；两轴量程也别差几十倍否则矮的一方被碾成直线：

.. code:: python

   ax1.set_ylabel("气温（℃）", color="tab:red"); ax1.tick_params(axis="y", colors="tab:red")
   ax2.set_ylabel("降水（mm）", color="tab:blue"); ax2.tick_params(axis="y", colors="tab:blue")

..

   **气象场景一句话**\ ：温度与降水双变量同框，只用 ``twinx()``
   而不分色，红曲线对左轴刻度、蓝柱对右轴刻度两败俱伤——像一张图上两把尺不标颜色，读者不知道温度该读左尺还是右尺。\ ``color=``\ +\ ``tick_params(colors=)``
   成对上色就一环扣一环，清晰无误。

--------------

.. _910-常见坑位速查表收尾:

9.10 常见坑位速查表（收尾）
---------------------------

+--------------------------+--------------------------------------------------------------+---------------+
| 记一记                   | 关键词 → 原因                                                | 对应条目      |
+==========================+==============================================================+===============+
| 中文方块、负号方块       | ``missing from font(s) DejaVu Sans`` /                       | 9.1.1 / 9.1.2 |
|                          | ``MINUS SIGN missing``                                       |               |
+--------------------------+--------------------------------------------------------------+---------------+
| 画到 fig 上、数组上      | ``'Figure' object has no attribute 'plot'`` /                | 9.2.1 / 9.2.2 |
|                          | ``'numpy.ndarray' ...``                                      |               |
+--------------------------+--------------------------------------------------------------+---------------+
| 多子图返回数组要         | ``'Axes' object is not subscriptable`` / ``IndexError``      | 9.2.3 / 9.2.4 |
| ``[行,列]`` 取           |                                                              |               |
+--------------------------+--------------------------------------------------------------+---------------+
| 二维数组展平最稳         | ``axes.flat`` / ``axes.flatten()``                           | 9.2.5         |
+--------------------------+--------------------------------------------------------------+---------------+
| x 与 y 长度不等          | ``x and y must have same first dimension``                   | 9.3.1 / 9.3.4 |
+--------------------------+--------------------------------------------------------------+---------------+
| 列名/字符串当x           | ``KeyError`` 或静默类别轴                                    | 9.3.2         |
+--------------------------+--------------------------------------------------------------+---------------+
| 2D                       | ``len(ax.lines)>=2``                                         | 9.3.3         |
| 数组被当多条曲线(静默)   |                                                              |               |
+--------------------------+--------------------------------------------------------------+---------------+
| set_xlim 写反            | 静默倒置, ``get_xlim()`` 回读                                | 9.4.1         |
+--------------------------+--------------------------------------------------------------+---------------+
| ticks 与 labels 个数不等 | ``does not match the number of labels``                      | 9.4.2         |
+--------------------------+--------------------------------------------------------------+---------------+
| 旋转参数挂错方法         | ``unexpected keyword argument 'rotation'``                   | 9.4.3         |
+--------------------------+--------------------------------------------------------------+---------------+
| 刻度太密/要显式locator   | 自动刻度限量, 日期轴用 ``MonthLocator``                      | 9.4.4         |
+--------------------------+--------------------------------------------------------------+---------------+
| colorbar 传 Axes         | ``'Axes' object has no attribute 'cmap'``                    | 9.5.1         |
+--------------------------+--------------------------------------------------------------+---------------+
| colorbar 无对象          | ``RuntimeError: No mappable was found``                      | 9.5.2         |
+--------------------------+--------------------------------------------------------------+---------------+
| 图例无 label             | ``UserWarning: No artists with labels found``                | 9.5.3         |
+--------------------------+--------------------------------------------------------------+---------------+
| handles/labels 错配      | 静默截断, ``len(legend_handles)``                            | 9.5.4         |
+--------------------------+--------------------------------------------------------------+---------------+
| loc 拼错                 | ``'uper right' is not a valid value for loc``                | 9.5.5         |
+--------------------------+--------------------------------------------------------------+---------------+
| 函数名多/少 s、旧参数    | ``has no attribute 'scatters'`` / ``normed``                 | 9.6.1 / 9.6.2 |
+--------------------------+--------------------------------------------------------------+---------------+
| contour levels 降序      | ``Contour levels must be increasing``                        | 9.6.3         |
+--------------------------+--------------------------------------------------------------+---------------+
| imshow origin/extent 反  | 静默翻转, 检查上北下南                                       | 9.6.4 / 9.9.4 |
+--------------------------+--------------------------------------------------------------+---------------+
| NaN 破洞、色标乱         | imshow/contourf 白斑, ``nanmin/nanmax``, ``set_bad``         | 9.6.5 / 9.9.3 |
+--------------------------+--------------------------------------------------------------+---------------+
| 保存目录不存在           | ``FileNotFoundError`` → ``os.makedirs(exist_ok=True)``       | 9.7.1         |
+--------------------------+--------------------------------------------------------------+---------------+
| bbox_inches 拼错         | ``unexpected keyword argument 'bound_inches'``               | 9.7.2         |
+--------------------------+--------------------------------------------------------------+---------------+
| 后缀不支持               | ``ValueError: Format '...' is not supported``                | 9.7.3         |
+--------------------------+--------------------------------------------------------------+---------------+
| dpi 太低/只 show 不存    | 糊图/无文件 → ``dpi=300`` + ``savefig`` + ``plt.close``      | 9.7.4         |
+--------------------------+--------------------------------------------------------------+---------------+
| 布局混用                 | ``UserWarning: ...layout has changed to tight_layout`` →     | 9.8.1         |
| tight+constrained        | 二选一                                                       |               |
+--------------------------+--------------------------------------------------------------+---------------+
| add_subplot 序号越界     | ``1 <= num <= 4, not 9``                                     | 9.8.2         |
+--------------------------+--------------------------------------------------------------+---------------+
| sharex 上层刻度“消失”    | 静默隐藏, 预期行为                                           | 9.8.3         |
+--------------------------+--------------------------------------------------------------+---------------+
| 时间序列未格式化         | 刻度拥挤 →                                                   | 9.9.1         |
|                          | ``MonthLocator``\ +\ ``DateFormatter``\ +\ ``autofmt_xdate`` |               |
+--------------------------+--------------------------------------------------------------+---------------+
| 日期超范围               | ``Date ordinal ... must be between year 0001 and 99``        | 9.9.2         |
+--------------------------+--------------------------------------------------------------+---------------+
| 单位/量纲标错            | 静默, ℃ vs K 先换算                                          | 9.9.5         |
+--------------------------+--------------------------------------------------------------+---------------+
| twinx 双轴未分色         | 静默 → ``tick_params(colors=...)``                           | 9.9.6         |
+--------------------------+--------------------------------------------------------------+---------------+

..

   **收尾口诀（气象风）**\ ：第 9
   章先治“三道急症”——``missing from font``
   配中文汉字字体、\ ``same first dimension / must be the same size``
   查数据长短、\ ``No mappable / No artists``
   查对象类型；再收拾三窝“静默鬼”——中文字体方块、坐标轴/经纬度反置、NaN
   破洞，守住
   ``get_xlim()``\ 、\ ``get_xticks()``\ 、\ ``len(ax.lines)``
   三根照妖镜。出图前默念四问：\ **单位对不对、经纬度反没反、缺测遮没遮、刻度挤没挤**——这四问全过，第
   9 章的图就“立”得住了。
