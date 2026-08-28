术语参考
========

本站的术语参考与常规文档不同，是 **术语 API**：常规 API 讲「函数怎么调用」，术语 API 讲「**词是什么意思**」。Python 教程里总有那么些词——整型、浮点型、可变、切片、作用域——它们是专业术语，或与日常用语含义不同。本栏目专门为初学者拆解这些词。

每个词条包含四个部分：

#. **一句话定义**：这个词的准确含义；
#. **生活类比**：用身边的经验理解它（气象与地理场景优先）；
#. **代码示例**：两三行可运行的代码；
#. **易混淆点**：初学者最容易踩的坑。

正文中出现的术语可用 :term:`行内链接 <变量>` 跳转到这里，例如 :term:`浮点型 <浮点型 float>`、:term:`切片 <切片>`。

.. toctree::
   :maxdepth: 2
   :hidden:

   basics/index
   data/index
   viz/index

三大模块速览
------------

.. grid:: 1 1 2 3
   :gutter: 2

   .. grid-item-card:: 模块一 Python 编程基础
      :link: basics/index
      :link-type: doc
      :class-card: gallery-card

      ^^^

      第 1–5 节 · 环境、数据类型、控制流、函数与作用域、面向对象与高级语法。

   .. grid-item-card:: 模块二 气象数据处理
      :link: data/index
      :link-type: doc
      :class-card: gallery-card

      ^^^

      第 6–8 节 · NumPy 计算、Pandas 分析、Xarray 多维数据。

   .. grid-item-card:: 模块三 气象数据可视化
      :link: viz/index
      :link-type: doc
      :class-card: gallery-card

      ^^^

      第 9–10 节 · Matplotlib 绘图、Cartopy 地图绘图。

每个模块的索引页都按章收录具体词条，也可从左侧导航逐层展开进入。

使用提示
--------

- 词条按「遇到不懂的词 → 查这里」的方式使用，也可在每章小结处通过链接批量回顾；
- 每个词条的 **易混淆点** 都来自初学者的高频报错，读一遍能省几次调试；
- 与 Python 官方文档的术语表（`Glossary <https://docs.python.org/zh-cn/3/glossary.html>`_）互为补充：官方版严谨，本站版好懂。