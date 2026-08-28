模块二 气象数据处理（术语参考）
=================================

术语参考按三大内容模块组织，与 :doc:`/user_guide/index` 正文一一对应。本模块覆盖第 6–8 节的气象数据处理术语：NumPy 数值计算、Pandas 表格分析、Xarray 多维网格。三者层层递进——ndarray 是地基，DataFrame 管表格，DataArray/Dataset 管带坐标的格点场。

.. toctree::
   :maxdepth: 2
   :hidden:

   ch06_terms
   ch07_terms
   ch08_terms

各节术语速览
------------

.. grid:: 1 2 2 3
   :gutter: 2

   .. grid-item-card:: 第 6 节 · 气象数据计算 NumPy
      :link: ch06_terms
      :link-type: doc
      :class-card: gallery-card

      ^^^

      数组、维度/轴、形状、dtype、广播、向量化、NaN

   .. grid-item-card:: 第 7 节 · 气象数据分析（一）Pandas
      :link: ch07_terms
      :link-type: doc
      :class-card: gallery-card

      ^^^

      DataFrame、Series、索引、布尔索引、分组聚合、透视表、NaN

   .. grid-item-card:: 第 8 节 · 气象数据分析（二）Xarray
      :link: ch08_terms
      :link-type: doc
      :class-card: gallery-card

      ^^^

      DataArray、Dataset、维度、坐标、NetCDF、属性 attrs、重采样