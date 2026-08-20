模块二 气象数据处理（配套练习）
========================================

本模块与 :doc:`/user_guide/data/index` 正文一一对应，含第 6–8 章的实战练习。从把气温数据装进 NumPy 数组，到用 Pandas 做逐日观测处理，再到用 Xarray 处理带经纬度标签的格点场，层层递进。

.. toctree::
   :maxdepth: 2
   :hidden:

   ch06_practice
   ch07_practice
   ch08_practice

各节速览
--------

.. grid:: 1 2 2 3
   :gutter: 2

   .. grid-item-card:: 第 6 章 · 气象数据计算 NumPy
      :link: ch06_practice
      :link-type: doc
      :class-card: gallery-card

      ^^^

      数组存取、分组统计、高温预警筛选与标准化。

   .. grid-item-card:: 第 7 章 · 气象数据分析（一）Pandas
      :link: ch07_practice
      :link-type: doc
      :class-card: gallery-card

      ^^^

      读取、筛选高温日、按月报表、排序与导出。

   .. grid-item-card:: 第 8 章 · Xarray 气象数据处理（二）
      :link: ch08_practice
      :link-type: doc
      :class-card: gallery-card

      ^^^

      贴上经纬度标签、区域平均、按坐标取数与重采样。