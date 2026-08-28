MeteoPython
===========

欢迎来到兰州大学大气科学学院编程社区的 **MeteoPython** 编程文档。
本站面向零基础起步的学习者，也适合想系统梳理气象数据可视化技巧的同学与科研人员。
我们仿照 Matplotlib 官方文档的组织方式，将「Python 基础、气象数据处理、气象数据可视化」
串成一条主线，并以贯穿全站的实战项目让你学一章、进一步，最终产出一份完整的气象数据分析报告。

你可以直接用浏览器在左侧翻阅教程，或在**示例画廊**里边看成品图边复制代码跑通自己的版本。

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

内容一览
--------

- :doc:`/user_guide/index` —— 从环境搭建到 Cartopy 地图绘图的核心教程，共 10 节。
- :doc:`/tutorials/index` —— 与章节配套的实战练习，附提示与参考答案，检验所学。
- :doc:`/gallery/index` —— 可执行的示例画廊：基础绘图、NumPy 计算、气象数据可视化、
  科研绘图四大分区，每个示例都可下载源码、Notebook 与数据。
- :doc:`/api/index` —— 术语速查，随学随用。
- :doc:`/qa/index` —— 常见问题汇总，含报错排查思路。

三大内容模块
------------

- **模块一 Python 编程基础**：Conda、数据类型、分支循环、函数与作用域、面向对象与高级语法。
  从零上手，不跳步。
- **模块二 气象数据处理**：NumPy 计算、Pandas 分析、Xarray 多维数据，学会操作格点与表格数据。
- **模块三 气象数据可视化**：Matplotlib 绘图、Cartopy 地图绘图，把数据变成清晰的科学图表。

贯穿项目
--------

全站 10 节共用一个递进式实战项目：**兰州气温观测数据分析与可视化系统**。从第 1 节搭建
``weather_project/`` 起，到第 10 节画出西北地区气温空间分布图止，最终产出一份完整的气象
数据分析报告（含图表），让你真正"能上手、出作品"。

如何使用本站
------------

- **跟着练**：按目录顺序学完 10 节，每节末尾都有对应练习；卡住了先查**术语参考**与**常见问题**。
- **抄示例**：想快速出图，直接进**示例画廊**选一张效果图，下载源码与数据本地运行，改参数即可。
- **遇到问题**：报错先看**常见问题**；仍未解决可在社区里带着报错信息提问。

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: MeteoPython

   user_guide/index
   tutorials/index
   gallery/index
   api/index
   qa/index