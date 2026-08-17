.. _tut-mpl:

气象数据绘图（一）Matplotlib
============================

第 9 节 · 模块三 气象数据可视化
贯穿项目第 9 步：绘制兰州气温时间序列图、散点图、直方图。

.. note::

   本节正文由 T-901 交付后填充，以下为内容概要与导读。

面向对象接口（``fig, ax``）是推荐写法，便于拼多子图：

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt

   x = np.linspace(0, 2 * np.pi, 200)
   fig, ax = plt.subplots(figsize=(7, 3))
   ax.plot(x, np.sin(x), label="sin")
   ax.plot(x, np.cos(x), label="cos")
   ax.set_xlabel("x")
   ax.set_ylabel("值")
   ax.legend()
   ax.set_title("正弦与余弦")
   plt.show()

本章将覆盖的知识点：Figure / Axes 面向对象接口、``plot`` / ``scatter`` / ``bar`` / ``hist``、标签 / 标题 / 图例、子图、``savefig``；提升拓展：``twinx`` 双轴、``annotate`` 标注、自定义样式。此外，下面这份「气象绘图最佳实践」浓缩了把"画对图"的关键经验——气象里"数据是米，绘图是炊"，米再好，炊不好，读者端起饭碗就皱眉头。

最佳实践：气象绘图规范
----------------------

□ 项目第 9 步的整体画面：绘制兰州气温时间序列图、散点图、直方图。这份规范把走弯路后回头的经验浓缩成册，可供读者逐条对照。

面向对象接口，别让 pyplot 全局状态"打游击"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Matplotlib 有两种用法，初学者最常踩的就是把两种混在一起用。

**状态机（pyplot）写法**：``plt.plot(...)``、``plt.xlabel(...)``、``plt.title(...)`` 一层一层叠在 Matplotlib 内部的"当前画布"上，像流水线上工人轮流往同一块板上钉钉子，谁最后改的谁说了算。

**面向对象（OO）写法**：先 ``fig, ax = plt.subplots()`` 创建"画布 + 坐标区"这对搭档，之后所有操作都**明确指定**是画在哪个 ``ax`` 上。就像每个小组都有自己的白板和记号笔，互不串台。

.. code-block:: python

   import matplotlib.pyplot as plt
   import numpy as np

   # ✅ 推荐：面向对象接口，一切操作挂在 ax 上
   fig, ax = plt.subplots(figsize=(7, 4))
   x = np.arange(1, 32)                 # 1~31 日
   t = 15 + 3.5 * np.sin(2 * np.pi * x / 31)   # 模拟一条正弦气温曲线
   ax.plot(x, t, color="tab:red", lw=2, label="逐日平均温")
   ax.set_xlabel("日期（日）")
   ax.set_ylabel("气温（℃）")
   ax.set_title("兰州某月逐日平均温")
   ax.legend()
   ax.grid(True, ls="--", alpha=0.4)
   plt.show()

.. warning::

   风险点：``plt.plot`` 之后又混用 ``ax.plot``，当前坐标系是谁你心里没数，多图、多子图时元素会画错地方，排错如大海捞针——这就是全局状态混乱在"打游击"。

   💡 什么时候才特意用 pyplot？只有三类场景：**多张独立图**（一张画完 ``plt.figure()`` 再开下一张）、**多子图布局**用 ``plt.subplots()``、以及**清画布** ``plt.clf()`` / ``plt.close()`` 回收内存时。其余画图细节，一律交给 ``ax``。

✅ 最佳实践口诀：画每个坐标系的元素，永远从 ``fig, ax = plt.subplots()`` 起步；凡是对"某个具体图"的操作，都用 ``ax.xxx``。

四种气象图的做法与要点
^^^^^^^^^^^^^^^^^^^^^^

气温时间序列折线图（``plot``）
"""""""""""""""""""""""""""""

时间和温度养在同一个坐标系里，折线把"这是一天一个点"的断续观测连绵成"冷暖起伏"的生命线。做折线图只需保证：横轴是时间，纵轴是气温，连线别太粗，别在点与点之间填太多视觉噪音。

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt

   fig, ax = plt.subplots(figsize=(9, 4))
   doy = np.arange(1, 32)                     # 一年中的第 1~31 天
   temp = 8 + 12 * np.cos(2 * np.pi * (doy - 200) / 365)  # 冬冷夏热的年周期

   # ✅ plot 画折线：color 定颜色、lw 定粗细、marker 定节点
   ax.plot(doy, temp, color="tab:blue", lw=1.8, marker="o",
           ms=4, label="日平均温")
   ax.axhline(temp.mean(), color="gray", ls="--", lw=1, label="年均值")
   ax.fill_between(doy, temp, temp.mean(), color="tab:blue",
                   alpha=0.15)                # 填色增强冷暖「气泡感」
   ax.set_xlabel("一年中的第几天")
   ax.set_ylabel("气温（℃）")
   ax.legend(loc="best")
   plt.show()

✅ 要点：趋势着重用折线；点太多且间隔不等时别用 ``marker='o'``（会糊成一团墨），实心折线更能体现实测的连续感；年均值或气候均值用一条虚线 ``axhline`` 当"地平线"，比读者自动脑补强得多。

两要素相关性散点图（``scatter``）
""""""""""""""""""""""""""""""""

想看"逐日最高温"和"逐日最低温"是不是手牵手一起涨，散点图最直观：每个点代表一天，横轴最低温、纵轴最高温。若点子沿一条对角线密集排布，说明两要素强相关，那一刻"日最高温"和"日最低温"像一对默契的双胞胎。

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt

   rng = np.random.default_rng(7)
   day_mean = 15 + 6 * np.cos(2 * np.pi * (np.arange(1, 61) - 200) / 365)
   tmin = day_mean - 7 + rng.normal(0, 1.5, 60)   # 每天的最低温
   tmax = day_mean + 7 + rng.normal(0, 1.5, 60)   # 每天的最高温

   fig, ax = plt.subplots(figsize=(7, 5))
   ax.scatter(tmin, tmax, s=25, alpha=0.75, color="tab:orange",
              edgecolors="k", linewidths=0.4)
   # ✅ 参考线：没有任何一天的最高温低于最低温，这条对角线是"物理下限"
   lo, hi = ax.get_xlim()
   ax.plot([lo, hi], [lo, hi], ls="--", color="gray", lw=1, label="tmax = tmin")
   ax.set_xlabel("日最低温（℃）")
   ax.set_ylabel("日最高温（℃）")
   ax.set_aspect("equal", adjustable="box")      # 保证对角线是 45°
   ax.legend()
   plt.show()

.. warning::

   风险点：散点没 ``alpha``（透明度）时，几十上百个点叠在一起会变成一团实心色块，掩盖真实的点云密度。适当 ``alpha``（0.5~0.8）和细白描边 ``edgecolors='k'`` 能救回可读性。

✅ 要点：想读"相关性强不强、线性不线性、有没有离群点"，颜色的深浅由点密不密来决定；不要一进门就追求拟合回归线，先用裸散点观察数据长什么样。

气温分布直方图（``hist``）
"""""""""""""""""""""""""

直方图回答"气温大多待在哪一档"。把整年逐日均温和逐日温差（最高温 − 最低温）都码进直方图，能一眼看出：年气温分布到底偏不偏（**偏态**）、有没有**双峰**（春天和秋天挤成两个山头）、以及这个内陆城市的**昼夜温差**是否常年被拉得很开。

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt

   rng = np.random.default_rng(1)
   # 演示数据：偏态 + 双峰并存，模拟「春秋温和、夏季酷热」的全年温度
   t = np.concatenate([
       rng.normal(12, 6, 200),     # 春秋一坨，偏冷
       rng.normal(27, 4, 120),     # 夏季一坨，偏热
   ])

   fig, ax = plt.subplots(figsize=(7, 4))
   ax.hist(t, bins=25, color="tab:green", edgecolor="white", alpha=0.9)
   ax.axvline(t.mean(), color="k", ls="--", lw=1.5, label=f"均值 {t.mean():.1f} ℃")
   ax.set_xlabel("气温（℃）")
   ax.set_ylabel("频数（天）")
   ax.legend()
   plt.show()

✅ 要点：``bins`` 是"切几格"，太少糊成一根根柱子看不清形状，太多又抖成锯齿；可从 15~30 起步试试手感。想看"占了多少比例"，加 ``density=True`` 把纵轴换成概率密度。均值在图上画一条竖直虚线，读者立刻知道分布的中轴在哪。

多子图布局（``subplots(2,2)`` / ``sharex``）
"""""""""""""""""""""""""""""""""""""""""""""

图太多就分房子住——一张画布装 2×2 或 3×1 个坐标区，各管一事。要点是：共享横轴的子图一定开 ``sharex=True``，让它们底部 y 轴对齐、刻度一致，读者扫一眼就能横着对比时间轴。

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt

   doy = np.arange(1, 31)
   t = 16 + 5 * np.cos(2 * np.pi * (doy - 195) / 200)

   # ✅ 2×2 布局：四格各司其职
   fig, axes = plt.subplots(2, 2, figsize=(11, 7), sharex=True)
   axes[0, 0].plot(doy, t, color="tab:red");   axes[0, 0].set_title("折线：逐日气温")
   axes[0, 1].scatter(t[:-1], t[1:], s=20, color="tab:blue"); axes[0, 1].set_title("散点：相邻日相关")
   axes[1, 0].hist(t, bins=12, color="tab:green");            axes[1, 0].set_title("直方：分布")
   axes[1, 1].boxplot(t);                                     axes[1, 1].set_title("箱线：离散度")

   # 下一行统一 X 轴刻度标题（sharex 只共享刻度线，标题要单独写）
   for ax in axes[1, :]:
       ax.set_xlabel("日期（日）")
   for ax in axes[:, 0]:
       ax.set_ylabel("气温（℃）")

   fig.suptitle("兰州某时段气候速览", fontsize=14)   # 整图标题
   fig.tight_layout()
   plt.show()

💡 记忆：``plt.subplots(2, 2)`` 返回的 ``axes`` 是个二维数组，用 ``axes[行, 列]`` 取元；开了 ``sharex``，上面那行省掉一堆重复的横轴刻度，画面立刻清爽。

常规参数：让图"立"得起来
^^^^^^^^^^^^^^^^^^^^^^^^

- ``figsize``：画布尺寸，多子图或长序列数据要放大，别让梅西挤进电话亭；
- ``dpi``：分辨率（常用 100~150），PNG 导出时像素密度所在；
- 每个 ``ax`` 都要有 ``set_xlabel`` / ``set_ylabel`` / ``set_title``，多曲线加 ``legend(loc=...)``，线太多加 ``grid(ls='--', alpha=0.3)``；
- ``colorbar``：**只对有颜色映射的图**（``scatter`` 用 ``c=``、``pcolormesh``、``contourf``）用，普通折线散点别乱挂；
- 保存必须 ``savefig("a.png", bbox_inches="tight", dpi=150)``——``bbox_inches='tight'`` 会把图边裁剪到刚好贴合内容，四周不留白；
- 画完 ``plt.show()`` 看效果，批处理时 ``plt.close(fig)`` 释放画布内存，否则 100 张图跑完内存爆表。

.. code-block:: python

   import matplotlib.pyplot as plt
   import numpy as np

   fig, ax = plt.subplots(figsize=(8, 4))
   x = np.linspace(0, 2 * np.pi, 200)
   ax.plot(x, np.sin(x), color="tab:blue")
   ax.plot(x, np.cos(x), color="tab:orange")
   ax.set_title("正弦与余弦"); ax.legend(["sin", "cos"]); ax.grid(ls="--", alpha=0.3)

   # ✅ 半成品先 show 抽查，定稿务必 savefig（加 dpi 和 bbox_inches）
   plt.tight_layout()
   plt.show()
   fig.savefig("D:\\Code\\Vibe\\SUBMIT\\Chapter09\\demo_out.png",
               bbox_inches="tight", dpi=150)
   plt.close(fig)          # ✅ 批处理关键：画完就回收

提升技巧：一键从"能用的图"到"好看的图"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**双轴 ``twinx``**：当同一时间轴上要摆两个量纲不同的物理量（温度 ℃ 与降水 mm，风速 m/s 与气压 hPa），各走各的坐标轴：

.. code-block:: python

   import matplotlib.pyplot as plt
   import numpy as np

   x = np.arange(1, 32)
   temp = 15 + 4 * np.sin(2 * np.pi * x / 31)      # ℃
   rain = np.random.default_rng(3).uniform(0, 12, 30)  # mm

   fig, ax1 = plt.subplots(figsize=(8, 4))
   ax1.plot(x, temp, color="tab:red", lw=2, label="气温")
   ax1.set_ylabel("气温（℃）", color="tab:red"); ax1.tick_params(axis="y", colors="tab:red")

   ax2 = ax1.twinx()                 # ✅ 共享横轴、另起右纵轴
   ax2.bar(x, rain, color="tab:blue", alpha=0.35, label="降水")
   ax2.set_ylabel("降水（mm）", color="tab:blue"); ax2.tick_params(axis="y", colors="tab:blue")

   ax1.set_xlabel("日期（日）")
   fig.suptitle("温度与降水——量纲不同，双轴共舞")
   plt.show()

.. warning::

   风险点：双轴一定要用**颜色区分两套刻度**（左轴、右轴各自着色），否则读者分不清哪个刻度属于哪条线；两轴的量程比例也别相差几十倍，否则矮的一方会被碾成水平线。

**``annotate`` 标注极值点**：年最热、年最冷那天，用箭头一针见血指出来：

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt

   doy = np.arange(1, 367)
   temp = 10 + 15 * np.cos(2 * np.pi * (doy - 202) / 365)

   fig, ax = plt.subplots(figsize=(9, 4))
   ax.plot(doy, temp, color="tab:blue", lw=1.5)
   i_hot = int(np.argmax(temp)); i_cold = int(np.argmin(temp))

   ax.annotate(f"最热 ≈{temp[i_hot]:.0f}℃（第 {i_hot+1} 天）",
               xy=(i_hot + 1, temp[i_hot]), xytext=(i_hot + 40, temp[i_hot] - 4),
               arrowprops=dict(arrowstyle="->", color="k"), fontsize=9)
   ax.annotate(f"最冷 ≈{temp[i_cold]:.0f}℃（第 {i_cold+1} 天）",
               xy=(i_cold + 1, temp[i_cold]), xytext=(i_cold - 150, temp[i_cold] + 6),
               arrowprops=dict(arrowstyle="->", color="k"), fontsize=9)
   ax.set_xlabel("一年中的第几天"); ax.set_ylabel("气温（℃）"); ax.set_title("标注冬夏极值点")
   plt.show()

**自定义样式 ``rcParams`` / 风格**：全局主题用 ``plt.style.use("seaborn-v0_8-whitegrid")``、``"ggplot"`` 一把梭；想改字体、字号、线宽等默认值，用 ``plt.rcParams`` 一次性配好：

.. code-block:: python

   import matplotlib.pyplot as plt

   # ✅ 工程开始处统一风格，整个文件生效，不用每张图重复设
   plt.style.use("seaborn-v0_8-whitegrid")
   plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei",
                                      "Noto Sans CJK SC", "WenQuanYi Micro Hei"]
   plt.rcParams["axes.unicode_minus"] = False   # 让负号不是方块
   plt.rcParams["figure.dpi"] = 120

.. warning::

   风险点：中文显示为"□□方块"的根因，不是缺库，而是**没把中文字体装进 ``font.sans-serif`` 白名单**，顺带漏了 ``axes.unicode_minus = False`` 导致负号也是方块。三行 ``rcParams`` 一起上，F5 一次到位。

常见坑位一次排雷
^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 22 32 46
   :header-rows: 1

   * - 坑
     - 症状
     - 排雷
   * - 混用 pyplot 与 OO
     - 元素画到"错误的画布/子图"上
     - 全文件统一用 ``fig, ax``，只在开图/清图时碰 pyplot
   * - 中文未配置
     - 图上全是一条条小方块
     - 顶部 ``rcParams["font.sans-serif"]`` + ``unicode_minus``
   * - 只 ``show()`` 不 ``savefig``
     - 跑批处理时"图一闪而过、无文件产出"
     - 每次 ``savefig(..., bbox_inches="tight", dpi=150)``
   * - 图例 ``loc`` 不合适
     - legend 压住曲线趋势
     - ``loc="best"`` 或手动 ``bbox_to_anchor=(1.02, 1)`` 放到图外
   * - 刻度重叠
     - 日期/标签糊成一坨
     - 加 ``figsize``、``plt.xticks(rotation=45)``、或用 ``tick_params`` 稀疏刻度
   * - 不 ``close``
     - 跑多张循环内存疯涨
     - 循环里画完 ``plt.close(fig)``

完整综合示例：一张多子图图板
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

把折线、散点、直方图装进一张 3 行图板，是第 9 步收官之作的雏形——数据在脚本内用 NumPy 构造，不开任何外部文件。

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt

   plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei",
                                      "Noto Sans CJK SC", "WenQuanYi Micro Hei"]
   plt.rcParams["axes.unicode_minus"] = False

   rng = np.random.default_rng(2024)
   days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
   doy = np.arange(1, 366)
   month = np.repeat(np.arange(1, 13), days_per_month)

   # 兰州年周期：峰值在 7 月中旬
   day_mean = (10.5 + 15 * np.cos(2 * np.pi * (doy - 202) / 365)
               + rng.normal(0, 1.8, 365))
   diurnal = 6 + rng.normal(0, 2.0, 365)          # 昼夜温差
   tmax = day_mean + diurnal
   tmin = day_mean - diurnal

   hot = int(np.argmax(day_mean)); cold = int(np.argmin(day_mean))
   monthly = np.array([day_mean[month == m].mean() for m in range(1, 13)])

   fig, axes = plt.subplots(3, 1, figsize=(11, 12))

   # ① 上：逐日平均温折线 + 月均温阶梯叠加 + 冬夏极值标注
   axes[0].plot(doy, day_mean, color="tab:blue", lw=1.2, label="逐日平均温")
   axes[0].plot(np.arange(1, 13) * 30, monthly, color="tab:red", lw=2,
                marker="o", label="月均温")
   axes[0].annotate(f"7 月最热 ≈{day_mean[hot]:.1f}℃",
                    xy=(hot + 1, day_mean[hot]),
                    xytext=(hot - 60, day_mean[hot] + 4),
                    arrowprops=dict(arrowstyle="->", color="k"))
   axes[0].annotate(f"1 月最冷 ≈{day_mean[cold]:.1f}℃",
                    xy=(cold + 1, day_mean[cold]),
                    xytext=(cold + 220, day_mean[cold] - 8),
                    arrowprops=dict(arrowstyle="->", color="k"))
   axes[0].set_title("逐日平均温（年周期，冬冷夏热）")
   axes[0].legend(); axes[0].grid(ls="--", alpha=0.3)

   # ② 中：日最高温 vs 日最低温散点（看相关）
   sc = axes[1].scatter(tmin, tmax, c=month, cmap="turbo", s=14, alpha=0.7)
   lo, hi = axes[1].get_xlim()
   axes[1].plot([-15, 40], [-15, 40], ls="--", color="gray", lw=1, label="tmax = tmin")
   axes[1].set_xlabel("日最低温（℃）"); axes[1].set_ylabel("日最高温（℃）")
   axes[1].set_title("日最高温 vs 日最低温散点（颜色=月份）")
   axes[1].legend()
   fig.colorbar(sc, ax=axes[1], label="月份")

   # ③ 下：全年逐日平均温分布直方图
   axes[2].hist(day_mean, bins=30, color="tab:green", edgecolor="white", alpha=0.9)
   axes[2].axvline(day_mean.mean(), color="k", ls="--", lw=1.5)
   axes[2].set_xlabel("逐日平均温（℃）"); axes[2].set_ylabel("频数（天）")
   axes[2].set_title(f"全年气温分布（均值 {day_mean.mean():.1f} ℃，呈双峰偏态）")

   fig.suptitle("兰州 2024 全年气温综合分析", fontsize=15)
   fig.tight_layout()
   plt.show()
   plt.close(fig)

要点总结
^^^^^^^^

1. 画图从 ``fig, ax = plt.subplots()`` 起步，具体元素全归 ``ax`` 管；pyplot 只在开图、多图/多子图、清画布时出场；
2. 折线 ``plot`` 看趋势、散点 ``scatter`` 看相关（配对角线参考线）、直方图 ``hist`` 看分布（偏态 / 双峰 / 昼夜温差）；
3. 多子图 ``subplots(行,列)`` 配 ``sharex=True`` 共享时间轴，刻度对齐横着可比；
4. ``figsize`` / ``dpi`` / 标签 / 标题 / 图例 / 网格 是图的地基；``colorbar`` 只给颜色映射图用；
5. 保存 ``savefig(bbox_inches="tight", dpi=150)``，画完 ``plt.close(fig)`` 防内存泄漏；
6. ``twinx`` 双轴管不同量纲、``annotate`` 定点标极值、``rcParams`` 统一定中文字体与风格；
7. 中文字体、负号方块、不 savefig、图例挡数据、刻度重叠——五座大头坑，各有排雷口诀。

.. seealso:: 示例画廊 :doc:`/gallery/auto_examples/plot_viz/index`　·　配套练习：第 9 章练习《Matplotlib 气象绘图》将在随后交付后上线（链接到时补全）　·　术语参考：第 9 章术语表将在随后交付后上线（链接到时补全）