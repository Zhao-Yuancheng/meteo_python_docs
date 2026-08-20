第 9 章练习：Matplotlib 气象绘图
================================

配套 :ref:`tut-mpl` 正文。共五题，难度递增，覆盖折线图、散点图、双子图与 ``savefig`` 导出。每题给出 **提示** 与 **参考答案**，先自己动手写，再对照参考。

.. seealso:: 配套正文：:doc:`/user_guide/viz/matplotlib`　·　术语参考：:doc:`/api/ch09_terms`

💡 **通用约定**：各题用例行 ``fig, ax = plt.subplots(...)``（或多子图时的 ``axes``）绘图；气温保留一位小数；时次在图上标成 ``08``、``14``、``20``。作图前先在脚本开头加上（Windows 下避免中文缺字、负号变方块）：

.. code-block:: python

   import matplotlib.pyplot as plt

   plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
   plt.rcParams["axes.unicode_minus"] = False

入门题
------

第 1 题 折线图
--------------

已知兰州站（区站号 52889）某日三个时次的气温如下表。这三个时次分别代表早晨、午后最高和傍晚，试绘制气温折线图。

.. list-table::
   :widths: 40 20 20 20
   :header-rows: 1

   * - 时次
     - 08
     - 14
     - 20
   * - 气温 / ℃
     - 21.6
     - 31.6
     - 23.1

试完成下列各问：

1. 用 ``fig, ax = plt.subplots(figsize=(8, 4))`` 创建画布与坐标区；
2. 用 ``ax.plot`` 画折线：横轴为时次，纵轴为气温，折线须带标记点；
3. 横轴名称 ``时次``，纵轴名称 ``气温 / ℃``，标题 ``兰州站气温``；
4. 横轴刻度与表中三个时次一致。

**参考答案**：

.. code-block:: python

   import matplotlib.pyplot as plt

   plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
   plt.rcParams["axes.unicode_minus"] = False

   hours = [8, 14, 20]
   temps = [21.6, 31.6, 23.1]

   fig, ax = plt.subplots(figsize=(8, 4))
   ax.plot(hours, temps, marker="o")
   ax.set_xlabel("时次")
   ax.set_ylabel("气温 / ℃")
   ax.set_title("兰州站气温")
   ax.set_xticks(hours)
   ax.set_xticklabels(["08", "14", "20"])
   fig.tight_layout()
   plt.show()

> 💡 提示：第一步按表写出两个列表 ``hours = [8, 14, 20]``、``temps = [21.6, 31.6, 23.1]``；第二步 ``fig, ax = plt.subplots(...)`` 后写 ``ax.plot(hours, temps, marker="o")``；第三步用 ``ax.set_xlabel`` / ``ax.set_ylabel`` / ``ax.set_title`` 写名称和标题；第四步 ``ax.set_xticks(hours)`` + ``ax.set_xticklabels(["08", "14", "20"])`` 把刻度写成两位时次。折线应先升后降，14 时最高，为 31.6 ℃。

第 2 题 散点图
--------------

同一日的相对湿度见下表。午后气温最高时湿度最低，试用散点图查看气温与相对湿度的关系。

.. list-table::
   :widths: 40 20 20 20
   :header-rows: 1

   * - 时次
     - 08
     - 14
     - 20
   * - 气温 / ℃
     - 21.6
     - 31.6
     - 23.1
   * - 相对湿度 / %
     - 48
     - 26
     - 41

试完成下列各问：

1. 横轴为气温，纵轴为相对湿度，用 ``ax.scatter`` 绘图；
2. 轴名称分别为 ``气温 / ℃``、``相对湿度 / %``，标题为 ``兰州站气温与相对湿度``；
3. 用 ``ax.annotate`` 在各点旁标出时次，以便认出 14 时那一点。

**参考答案**：

.. code-block:: python

   import matplotlib.pyplot as plt

   plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
   plt.rcParams["axes.unicode_minus"] = False

   hours = [8, 14, 20]
   temps = [21.6, 31.6, 23.1]
   humidity = [48, 26, 41]

   fig, ax = plt.subplots(figsize=(6, 5))
   ax.scatter(temps, humidity)
   for hour, t, rh in zip(hours, temps, humidity):
       ax.annotate(f"{hour:02d}", (t, rh), textcoords="offset points", xytext=(6, 4))
   ax.set_xlabel("气温 / ℃")
   ax.set_ylabel("相对湿度 / %")
   ax.set_title("兰州站气温与相对湿度")
   fig.tight_layout()
   plt.show()

> 💡 提示：第一步写出三个等长列表 ``hours``、``temps``、``humidity``；第二步 ``ax.scatter(temps, humidity)``，横轴必须是气温，不要写成时次；第三步用 ``for hour, t, rh in zip(...)`` 循环对每个点 ``ax.annotate`` 标时次；第四步写轴名称和标题。14 时应落在最右、最下（气温最高、湿度最低）。

进阶题
------

第 3 题 双子图
--------------

将折线与散点画在同一张画布的左右两块坐标区中。数据同上两题。

试完成下列各问：

1. 用 ``fig, axes = plt.subplots(1, 2, figsize=(10, 4))`` 创建一行两列；
2. 左图：气温折线，要求与第 1 题相同；
3. 右图：气温–相对湿度散点，要求与第 2 题相同；
4. 左右两块都须有自己的轴名称和标题。

**参考答案**：

.. code-block:: python

   import matplotlib.pyplot as plt

   plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
   plt.rcParams["axes.unicode_minus"] = False

   hours = [8, 14, 20]
   temps = [21.6, 31.6, 23.1]
   humidity = [48, 26, 41]

   fig, axes = plt.subplots(1, 2, figsize=(10, 4))

   axes[0].plot(hours, temps, marker="o")
   axes[0].set_xlabel("时次")
   axes[0].set_ylabel("气温 / ℃")
   axes[0].set_title("气温变化")
   axes[0].set_xticks(hours)
   axes[0].set_xticklabels(["08", "14", "20"])

   axes[1].scatter(temps, humidity)
   axes[1].set_xlabel("气温 / ℃")
   axes[1].set_ylabel("相对湿度 / %")
   axes[1].set_title("气温与相对湿度")

   fig.tight_layout()
   plt.show()

> 💡 提示：左图用 ``axes[0]``，右图用 ``axes[1]``；在 ``axes[0]`` 上 ``plot`` 气温并设刻度 ``08``、``14``、``20``，在 ``axes[1]`` 上 ``scatter``；最后 ``fig.tight_layout()`` 自动排布。

第 4 题 savefig 导出
--------------------

按第 1 题的数据绘制兰州站气温折线，并导出文件。本题须用到 ``figsize`` 和 ``dpi``。

试完成下列各问：

1. 绘图要求与第 1 题相同，创建时使用 ``figsize=(8, 4)``、``dpi=100``；
2. 保存为 ``lanzhou_temp_150.png``，``savefig`` 的 ``dpi=150``，并加 ``bbox_inches="tight"``；
3. 再保存 ``lanzhou_temp_300.png``，``dpi=300``，其余不变；
4. 按「像素宽度 ≈ 宽（英寸）× dpi」估算两份图的大约宽度。

**参考答案**：

.. code-block:: python

   import matplotlib.pyplot as plt

   plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
   plt.rcParams["axes.unicode_minus"] = False

   hours = [8, 14, 20]
   temps = [21.6, 31.6, 23.1]

   fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
   ax.plot(hours, temps, marker="o")
   ax.set_xlabel("时次")
   ax.set_ylabel("气温 / ℃")
   ax.set_title("兰州站气温")
   ax.set_xticks(hours)
   ax.set_xticklabels(["08", "14", "20"])
   fig.tight_layout()

   fig.savefig("lanzhou_temp_150.png", dpi=150, bbox_inches="tight")
   fig.savefig("lanzhou_temp_300.png", dpi=300, bbox_inches="tight")
   plt.show()

约宽：150 dpi → 1200 像素；300 dpi → 2400 像素。

> 💡 提示：``bbox_inches="tight"`` 避免轴名称被裁掉；先 ``savefig`` 再 ``plt.show()``；宽度约为 ``8 × dpi``。``figsize`` 改的是英寸大小，``dpi`` 改的是每英寸点数，只加 ``dpi`` 不会把字体按英寸放大。

提升题
------

第 5 题 双子图综合导出
----------------------

兰州站海拔较低、午后更热；西宁站海拔较高、同样时段气温偏低。按下表在上下两块子图中对比，并导出。

.. list-table::
   :widths: 40 20 20 20
   :header-rows: 1

   * - 时次
     - 08
     - 14
     - 20
   * - 兰州气温 / ℃
     - 21.6
     - 31.6
     - 23.1
   * - 西宁气温 / ℃
     - 16.2
     - 24.8
     - 17.0

试完成下列各问：

1. 用 ``fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)`` 创建上下两块；
2. 上图兰州，下图西宁，折线须带 ``label`` 并显示图例；
3. 两块图纵轴范围相同，例如都设为 ``14`` 到 ``34``；
4. 整张图总标题为 ``兰州与西宁气温对比``；
5. 导出为 ``lanzhou_xining_temp.png``：``dpi=150``，``bbox_inches="tight"``。

**参考答案**：

.. code-block:: python

   import matplotlib.pyplot as plt

   plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
   plt.rcParams["axes.unicode_minus"] = False

   hours = [8, 14, 20]
   temps_lz = [21.6, 31.6, 23.1]
   temps_xn = [16.2, 24.8, 17.0]

   fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

   axes[0].plot(hours, temps_lz, marker="o", label="兰州")
   axes[0].set_ylabel("气温 / ℃")
   axes[0].set_title("兰州")
   axes[0].legend()
   axes[0].set_ylim(14, 34)

   axes[1].plot(hours, temps_xn, marker="o", color="C1", label="西宁")
   axes[1].set_xlabel("时次")
   axes[1].set_ylabel("气温 / ℃")
   axes[1].set_title("西宁")
   axes[1].set_xticks(hours)
   axes[1].set_xticklabels(["08", "14", "20"])
   axes[1].legend()
   axes[1].set_ylim(14, 34)

   fig.suptitle("兰州与西宁气温对比")
   fig.tight_layout()
   fig.savefig("lanzhou_xining_temp.png", dpi=150, bbox_inches="tight")
   plt.show()

两站都是 14 时最高：兰州 31.6 ℃，西宁 24.8 ℃。纵轴对齐后，西宁曲线整体在兰州下方。

> 💡 提示：``sharex=True`` 让上下两块共享横轴、省去重复刻度；``set_ylim(14, 34)`` 统一纵轴量程才能公平对比；总标题用 ``fig.suptitle``；导出用 ``fig.savefig(..., dpi=150, bbox_inches="tight")``。