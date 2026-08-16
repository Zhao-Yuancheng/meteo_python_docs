MeteoPython
===========

欢迎来到兰州大学大气科学学院编程社区的 **MeteoPython** 编程文档。
本站仿照 Matplotlib 官方文档体系组织，覆盖 Python 基础、气象数据处理与气象数据可视化三大模块，
以"兰州气温观测数据分析与可视化系统"贯穿项目为主线，每学完一章，项目就往前推进一步。

.. grid:: 1 1 2 3
   :gutter: 2

   .. grid-item-card:: 快速开始
      :link: user_guide/basics/python_conda
      :link-type: doc
      :class-card: gallery-card

      ^^^

      安装 Conda 与 Python，画出第一张气象图。

   .. grid-item-card:: 术语参考
      :link: api/index
      :link-type: doc
      :class-card: gallery-card

      ^^^

      整型、浮点型、切片……初学者术语逐一拆解。

   .. grid-item-card:: 练习
      :link: tutorials/index
      :link-type: doc
      :class-card: gallery-card

      ^^^

      章节实战练习，含提示与参考答案。

三大内容模块
------------

- **模块一 Python 编程基础**：Conda、数据类型、分支循环、函数与作用域、面向对象与高级语法。
- **模块二 气象数据处理**：NumPy 计算、Pandas 分析、Xarray 多维数据。
- **模块三 气象数据可视化**：Matplotlib 绘图、Cartopy 地图绘图。

贯穿项目
--------

全站 10 节共用一个递进式实战项目：**兰州气温观测数据分析与可视化系统**。从第 1 节搭建 ``weather_project/`` 起，到第 10 节画出西北地区气温空间分布图止，最终产出一份完整的气象数据分析报告（含图表）。

文档导航
--------

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: MeteoPython

   user_guide/index
   tutorials/index
   gallery/index
   api/index
   qa/index
