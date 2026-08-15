模块二 气象数据处理
===================

模块二覆盖第 6–8 节：NumPy 做数值计算，Pandas 处理表格型观测，Xarray 处理带标注的多维网格。三者层层递进——``ndarray`` 是地基，DataFrame 管表格，DataArray/Dataset 管带坐标的格点场。

.. toctree::
   :maxdepth: 2
   :hidden:

   numpy
   pandas
   xarray

各节速览
--------

.. grid:: 1 2 2 3
   :gutter: 2

   .. grid-item-card:: 气象数据计算 NumPy
      :link: tut-numpy
      :link-type: ref
      :class-card: gallery-card

      ^^^

      第 6 节 · ndarray、向量化与广播

   .. grid-item-card:: 气象数据分析（一）Pandas
      :link: tut-pandas
      :link-type: ref
      :class-card: gallery-card

      ^^^

      第 7 节 · DataFrame、read_csv 与分组聚合

   .. grid-item-card:: 气象数据分析（二）Xarray
      :link: tut-xarray
      :link-type: ref
      :class-card: gallery-card

      ^^^

      第 8 节 · DataArray/Dataset 与 NetCDF
