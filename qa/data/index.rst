模块二 气象数据处理（常见问题 Q&A）
==========================================

本模块与 :doc:`/user_guide/data/index` 正文一一对应，收录第 6–8 章关于气象数据计算的报错与静默错值：NumPy 数值计算、Pandas 表格分析、Xarray 多维格点。读报错时先想清楚"处理的是哪种数据结构"，再对症下药。

.. toctree::
   :maxdepth: 2
   :hidden:

   06-NumPy气象计算-QA
   07-Pandas气象分析-QA
   08-Xarray气象分析-QA

各篇速览
--------

.. grid:: 1 2 2 3
   :gutter: 2

   .. grid-item-card:: 气象数据计算 NumPy Q&A
      :link: 06-NumPy气象计算-QA
      :link-type: doc
      :class-card: gallery-card

      ^^^

      dtype 不匹配、广播规则、``nan`` 静默错值、内存与视图。

   .. grid-item-card:: 气象数据分析（一）Pandas Q&A
      :link: 07-Pandas气象分析-QA
      :link-type: doc
      :class-card: gallery-card

      ^^^

      ``read_csv`` 编码、索引对齐、缺失值、分组聚合报错。

   .. grid-item-card:: Xarray 气象数据处理（二）Q&A
      :link: 08-Xarray气象分析-QA
      :link-type: doc
      :class-card: gallery-card

      ^^^

      DataArray/Dataset 维度对齐、坐标不匹配与 NetCDF IO 报错。