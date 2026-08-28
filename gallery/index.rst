:orphan:

示例画廊
====================

本部分针对科研绘图，循序渐进地给予项目案例，帮助理解 Python 基础、气象数据处理以及气象数据可视化。

.. raw:: html

  <div id='sg-tag-list' class='sphx-glr-tag-list'></div>


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. thumbnail-parent-div-close

.. raw:: html

    </div>

基础绘图示例
---------------

本节展示 Python 基础语法的可视化示例，帮助理解数据类型与控制流。


.. raw:: html

  <div id='sg-tag-list' class='sphx-glr-tag-list'></div>


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="最简单的 Matplotlib 示例：生成一组角度，画出对应的正弦曲线。">

.. only:: html

  .. image:: /gallery/plot_basics/images/thumb/sphx_glr_plot_sine_thumb.png
    :alt:

  :doc:`/gallery/plot_basics/plot_sine`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">绘制正弦波</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="第 1 章示例：环境搭建好后，用最短的代码画出一张&quot;模拟兰州气温随日期变化&quot; 的折线图——用来验证 NumPy 与 Matplotlib 是否安装成功。绘图细节属于第 9 章内容， 这里先感受一下&quot;环境跑通&quot;的成就感。">

.. only:: html

  .. image:: /gallery/plot_basics/images/thumb/sphx_glr_plot_first_weather_thumb.png
    :alt:

  :doc:`/gallery/plot_basics/plot_first_weather`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">我的第一个气象图</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="第 2 章示例：不借助任何数据处理库，仅用 str / int / float / tuple / list / dict 这些内置类型，存储兰州站的元信息与近 7 日气温， 完成统计并绘制一张气温柱状图——每个类型的选择理由都写在行尾注释里。">

.. only:: html

  .. image:: /gallery/plot_basics/images/thumb/sphx_glr_plot_datatypes_thumb.png
    :alt:

  :doc:`/gallery/plot_basics/plot_datatypes`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">用基本数据类型存储站点信息</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="第 3 章示例：用 if/elif/else 对兰州站近 7 日最高气温做等级判定， 用 for 循环 + 字典统计各等级天数，最后用 Matplotlib 画一张&quot;逐日气温 + 等级配色&quot;的柱状图——把分支与循环的实战成果&quot;画&quot;出来。">

.. only:: html

  .. image:: /gallery/plot_basics/images/thumb/sphx_glr_plot_flow_thumb.png
    :alt:

  :doc:`/gallery/plot_basics/plot_flow`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">气温等级判定与逐日可视化</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="本示例演示第 4 章「函数及变量作用域、模块和包」的完整应用：把华氏温度转换、 热量指数（有效积温）计算、气温统计分别收成 独立函数，再用兰州站近几日气温数据 驱动整个流程，最后用面向对象的 matplotlib 接口绘图并标记高温日。">

.. only:: html

  .. image:: /gallery/plot_basics/images/thumb/sphx_glr_plot_functions_thumb.png
    :alt:

  :doc:`/gallery/plot_basics/plot_functions`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">函数化气温处理流程</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="本脚本演示面向对象编程在气象数据处理中的应用。它以兰州站（区站号 52889，纬 36.05°N、经 103.88°E、海拔约 1517 m）最近几日的逐日气温为 数据，展示三个要点：">

.. only:: html

  .. image:: /gallery/plot_basics/images/thumb/sphx_glr_plot_oop_thumb.png
    :alt:

  :doc:`/gallery/plot_basics/plot_oop`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Station 类的气温统计与可视化（兼用兰州站示例数据）</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>

气象数据处理示例
------------------

本节展示气象数据处理进阶与可视化的示例。


.. raw:: html

  <div id='sg-tag-list' class='sphx-glr-tag-list'></div>


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="气象数据在 NumPy 里的标准形态是\ 带维度的三维数组 (time, lat, lon)。 本示例读取项目配套的西北气温格点场，演示两个最常用的维度运算：">

.. only:: html

  .. image:: /gallery/plot_numpy/images/thumb/sphx_glr_plot_array_demo_thumb.png
    :alt:

  :doc:`/gallery/plot_numpy/plot_array_demo`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">格点气温场的 NumPy 维度运算</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="本章目标：用 Xarray 读取项目配套的 NetCDF 气温场，对其进行\ 时间切片、 空间子区域裁剪，并做\ 纬度加权区域平均，最后画出「某时刻空间气温场 + 区域平均时间序列」两张图，贯穿项目第 8 步。">

.. only:: html

  .. image:: /gallery/plot_numpy/images/thumb/sphx_glr_plot_xarray_field_thumb.png
    :alt:

  :doc:`/gallery/plot_numpy/plot_xarray_field`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Xarray 西北气温场分析</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="用 Pandas 对兰州站 2024 年全年逐日气温做「月度统计」与「高温日筛选」。">

.. only:: html

  .. image:: /gallery/plot_numpy/images/thumb/sphx_glr_plot_pandas_analysis_thumb.png
    :alt:

  :doc:`/gallery/plot_numpy/plot_pandas_analysis`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Pandas 气温月度分析</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="本示例演示 NumPy 处理气象多站气温矩阵的完整链路： 创建 7 天 × 5 站 的气温矩阵，沿 axis 做逐站均值 / 逐日极值， 再逐站做 Z-score 标准化，最后用 imshow 热力图把原始矩阵和标准化矩阵画出来。">

.. only:: html

  .. image:: /gallery/plot_numpy/images/thumb/sphx_glr_plot_temperature_matrix_thumb.png
    :alt:

  :doc:`/gallery/plot_numpy/plot_temperature_matrix`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">多站气温矩阵的计算与可视化</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>

气象数据可视化示例
--------------------

本节展示 Matplotlib 与 Cartopy 绘制气象场的示例。


.. raw:: html

  <div id='sg-tag-list' class='sphx-glr-tag-list'></div>


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="本章目标：用 HadCRUT5 数据集绘制逐年全球平均温度距平的时间序列图（X 轴为年份，Y 轴为温度 ℃/K）与全球气温变化趋势的空间分布图（用 contourf 或 pcolormesh）。">

.. only:: html

  .. image:: /gallery/plot_viz/images/thumb/sphx_glr_plot_hadcrut_trend_thumb.png
    :alt:

  :doc:`/gallery/plot_viz/plot_hadcrut_trend`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">全球平均温度距平时间序列与趋势空间分布</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="本章目标： 用 stipple.nc 数据绘制 1963 年 1 月的气温等值线图，并在同一张地图上标注 距平符号：正距平（1963 年 1 月比多年同期偏暖）的格点标 &quot;+&quot;， 负距平（偏冷）的格点标 &quot;-&quot;。">

.. only:: html

  .. image:: /gallery/plot_viz/images/thumb/sphx_glr_plot_map_anomaly_thumb.png
    :alt:

  :doc:`/gallery/plot_viz/plot_map_anomaly`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">绘制中国地图上的气温等值线图与距平符号标注（1963 年 1 月）</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>

科研绘图示例
----------------

本节展示面向科研论文 / 结课报告的进阶绘图：以大气化学 EKMA 曲线为代表，
演示如何把实验室导出的长表数据网格化为一幅科学等值面图，并标注机理分区。

.. raw:: html

  <div id='sg-tag-list' class='sphx-glr-tag-list'></div>


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="经验动力学建模方法（Empirical Kinetic Modeling Approach, EKMA）曲线， 是研究 O₃ 与前体物关系的经典工具：固定 VOCs 组分谱，系统扫描 NOx 与 VOCs 的 总浓度组合，把每个组合对应的最大 O₃ 浓度填到网格上，再用等值线画出 &quot;O₃ 浓度关于（NOx, VOCs）的平面&quot;。它揭示了 O₃ 生成对两种前体物的 非线性响应，并据此把一个城市的污染状态划分为三个特征区域：">

.. only:: html

  .. image:: /gallery/plot_sci/images/thumb/sphx_glr_plot_ekma_curve_thumb.png
    :alt:

  :doc:`/gallery/plot_sci/plot_ekma_curve`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">绘制 EKMA 曲线：城市臭氧敏感性分析</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>


.. toctree::
   :hidden:
   :includehidden:


   /./gallery/plot_basics/index.rst
   /./gallery/plot_numpy/index.rst
   /./gallery/plot_viz/index.rst
   /./gallery/plot_sci/index.rst


.. only:: html

  .. container:: sphx-glr-footer sphx-glr-footer-gallery

    .. container:: sphx-glr-download sphx-glr-download-python

      :download:`下载全部示例源码：gallery_python.zip </gallery/gallery_python.zip>`

    .. container:: sphx-glr-download sphx-glr-download-jupyter

      :download:`下载全部示例的 Jupyter Notebook：gallery_jupyter.zip </gallery/gallery_jupyter.zip>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
