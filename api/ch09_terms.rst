第 9 章术语：Matplotlib 绘图
=============================

配套 :ref:`tut-mpl` 正文使用。每个词条 = 一句话定义 + **生活类比** + **常用写法**\（`.. code-block:: python` 承载代码示例）+ **易混淆点**。这些词是读懂 Matplotlib 绘图代码的钥匙：报错时先看词条，再对症下药。

.. seealso:: 配套正文：:doc:`/user_guide/viz/matplotlib`　·　配套练习：:doc:`/tutorials/viz/ch09_practice`

.. glossary::

   Figure（画布）
      整张图的最外层容器。窗口大小、分辨率、保存成文件，针对的都是它；一张 ``Figure`` 里可以放一块绘图区，也可以放好几块。

      **生活类比** —— 一张空白画纸。纸有多宽、多高，决定整幅作品的尺寸；纸上画几块小图，是下一步的事。

      .. code-block:: python

         fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
         fig.suptitle("兰州站气温")          # 整张图的总标题
         fig.savefig("lanzhou_temp.png", dpi=150)

      .. note::

         ``figsize`` 的单位是英寸；``dpi`` 是每英寸点数。导出像素大约等于边长乘以 ``dpi``。例如 `(8, 4)`、``dpi=150``，宽约 1200 像素，高约 600 像素。创建 ``Figure`` 时的 ``dpi`` 主要影响窗口显示；``savefig(..., dpi=...)`` 决定导出文件，两处可以不同。

      **易混淆点** —— ``plt.figure()`` 只做出画布，还没有绘图区。多数入门代码用 ``plt.subplots()``，一次拿到 ``fig`` 和 ``ax``；改线宽、改坐标轴范围，是在 ``Axes`` 上操作，不是在 ``Figure`` 上。图太小应先改 ``figsize`` 而不是狂加 ``dpi``。

   Axes（坐标区 / 绘图区）
      真正画数据的那一块：横轴、纵轴、曲线、散点、标题、轴标签，都挂在它上面。一张 ``Figure`` 可以有多个 ``Axes``，也就是子图。

      **生活类比** —— 画纸上用直尺框出来的一块坐标纸。一张纸可以框出左右两块，两块各画各的，互不抢位置。

      .. code-block:: python

         fig, ax = plt.subplots()
         ax.plot(hours, temps)
         ax.set_xlabel("时次")
         ax.set_ylabel("气温 / ℃")
         ax.set_title("兰州站")
         ax.set_xlim(8, 20)
         ax.grid(True, linestyle="--", alpha=0.4)

     双子图时 ``ax`` 变成数组：

      .. code-block:: python

         fig, axes = plt.subplots(1, 2, figsize=(10, 4))
         axes[0].plot(hours, temps_lz)
         axes[1].plot(hours, temps_xn)

      **易混淆点** —— 英文 plural 是 ``Axes``，单块也叫 ``Axes``，不是 ``Axis``；``Axis`` 只指横轴或纵轴本身。``plt.plot(...)`` 画在"当前这块"上，多子图时优先写 ``axes[0].plot(...)``。

   Artist（绘图元素）
      Matplotlib 里能画出来的东西几乎都是 ``Artist``：整张 ``Figure``、一块 ``Axes``、一条折线、一个点、一段文字、一根刻度线，都算。它们叠在一起，组成最终那张图。

      **生活类比** —— 画纸上的每一笔。纸是一笔，框出来的坐标区是一笔，折线、数字、图例框也是一笔；改颜色、改线宽，改的是其中某一笔，不是整张纸作废重来。

      .. code-block:: python

         line, = ax.plot(hours, temps, color="C0", lw=2, marker="o")
         line.set_color("crimson")      # 事后改这一笔

      **易混淆点** —— ``ax.plot`` 返回的是折线对象组成的列表。逗号解包后 ``line`` 就是这一条线，以后可以单独改它的颜色、透明度、图例名；不要用 ``ax.plot(...)`` 的返回值做加法等运算。

   刻度（Ticks）
      坐标轴上的刻度线（tick）与刻度文字（tick label）。间距太大，读不出峰值出现在几点；间距太密，字会挤成一团。

      **生活类比** —— 温度计玻璃管旁边那一排刻痕和数字。管子是坐标轴，刻痕告诉你 20 在哪、30 在哪。

      .. code-block:: python

         ax.set_xticks([8, 11, 14, 17, 20])
         ax.set_xticklabels(["08", "11", "14", "17", "20"])
         ax.tick_params(axis="x", labelsize=10, rotation=0)
         ax.tick_params(axis="y", direction="in")

      **易混淆点** —— 气象图上时次常写成 ``08``、``14``，不要只留 ``8``、``14``，否则和观测记录对不齐；刻度太多时用 ``tick_params(axis="x")`` 稀疏或旋转文字，避免糊成一团。

   图例（Legend）
      说明图上各条线、各个点代表什么的符号说明。多站对比、多要素叠画时必须有；一条线若创建时没写 ``label``，图例里不会出现它。

      **生活类比** —— 天气图角落的符号说明：实线是气温，虚线是露点。没有这块说明，两条线颜色再不同，读图的人也不知道各是什么。

      .. code-block:: python

         ax.plot(hours, temps_lz, label="兰州")
         ax.plot(hours, temps_xn, label="西宁")
         ax.legend(loc="best")
         # 或指定位置：upper right / lower left / upper left

      **易混淆点** —— 必须先在 ``plot``/``scatter`` 里写 ``label="..."``，``legend()`` 才会显示该项；只写 ``legend()`` 而曲线不带 ``label``，图例是空的。

   色带（Colorbar）
      把颜色映射到数值的标尺。填色图、按第三变量上色的散点，必须有它，读者才能读出颜色对应的气温或高度。

      **生活类比** —— 红外云图旁边那条从蓝到红的竖条。云图上的红斑本身不写温度，温度写在旁边这条色标上。

      .. code-block:: python

         sc = ax.scatter(hours, temps, c=temps, cmap="coolwarm")
         cbar = fig.colorbar(sc, ax=ax)
         cbar.set_label("气温 / ℃")

      **易混淆点** —— ``colorbar`` 要绑一个"带颜色映射的对象"，上面那个 ``sc`` 就是；普通 ``ax.plot`` 没有这套映射，不能凭空加色带，否则报错或画不出。

   面向对象接口（Object-oriented interface）
      先明确在哪张画布、哪块坐标区上画，再调用这块区域的方法；和它相对的是 pyplot 状态机接口（``plt.plot``、``plt.xlabel``），后者依赖"当前图、当前坐标区"这个隐含状态。

      **生活类比** —— 先指定"在左边那张纸的右上那块画"，再下笔。pyplot 则像口头吩咐"就画在刚才那张上"；一个人画一张图还行，同时摊开几张纸时，最容易画错地方。

      .. code-block:: python

         # 推荐：对象写在明处
         fig, ax = plt.subplots()
         ax.plot(hours, temps)
         ax.set_xlabel("时次")
         fig.savefig("out.png", dpi=150)

         # 能跑，但当前画在哪一块不写在代码里
         plt.plot(hours, temps)
         plt.xlabel("时次")
         plt.savefig("out.png")

      **易混淆点** —— 多子图、多窗口、写进函数里复用时，pyplot 的全局"当前坐标系"会趁你不注意跑偏；面向对象接口把每个元素都挂在明确的 ``fig``/``ax`` 上，更强也更稳。

词条对照
--------

.. list-table::
   :widths: 22 30 48
   :header-rows: 1

   * - 词条
     - 管什么
     - 典型方法
   * - :term:`Figure（画布）`
     - 整张图的尺寸、导出
     - ``plt.subplots``、``fig.savefig``
   * - :term:`Axes（坐标区 / 绘图区）`
     - 一块坐标区里的数据与标注
     - ``ax.plot`` / ``scatter``、``ax.set_*``
   * - :term:`Artist（绘图元素）`
     - 图上可单独修改的一笔
     - ``line.set_color``
   * - :term:`刻度（Ticks）`
     - 轴上的位置与数字
     - ``ax.set_xticks``、``ax.tick_params``
   * - :term:`图例（Legend）`
     - 离散对象的名称
     - ``ax.legend``
   * - :term:`色带（Colorbar）`
     - 颜色与数值的对应
     - ``fig.colorbar``
   * - :term:`面向对象接口（Object-oriented interface）`
     - 明确画在哪个对象上
     - ``fig, ax = plt.subplots()``

读报错时先看词条：``Figure`` 对不上，多半是尺寸或保存；``Axes`` 对不上，多半是画错子图或标签没设上。