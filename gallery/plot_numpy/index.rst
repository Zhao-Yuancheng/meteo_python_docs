

.. _sphx_glr_gallery_plot_numpy:

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


.. toctree::
   :hidden:

   /gallery/plot_numpy/plot_array_demo
   /gallery/plot_numpy/plot_xarray_field
   /gallery/plot_numpy/plot_pandas_analysis
   /gallery/plot_numpy/plot_temperature_matrix

