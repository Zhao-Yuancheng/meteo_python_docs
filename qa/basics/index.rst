模块一 Python 编程基础（常见问题 Q&A）
============================================

本模块与 :doc:`/user_guide/basics/index` 正文一一对应，收录第 0–5 篇最高频的报错、警告与「静默错值」：环境搭建、数据类型与运算符、分支条件循环、函数与作用域、面向对象与高级语法。每一篇都说清：**可搜索的报错关键词 · 一句话原因 · 真实 Traceback· 排查步骤 · 气象场景类比**。建议先读 :doc:`00-通用排错指南 <00-通用排错指南>`\ ，再按篇对号入座。

.. toctree::
   :maxdepth: 2
   :hidden:

   00-通用排错指南
   01-Python简介与Conda环境-QA
   02-数据类型与运算符-QA
   03-分支条件循环-QA
   04-函数作用域模块包-QA
   05-面向对象函数式高级语法-QA

各篇速览
--------

.. grid:: 1 1 2 3
   :gutter: 2

   .. grid-item-card:: 通用排错指南
      :link: 00-通用排错指南
      :link-type: doc
      :class-card: gallery-card

      ^^^

      顶层的「报错 / 警告 / 静默错值」三分法、异常层级树与排查七招。

   .. grid-item-card:: Python 简介及安装环境 Q&A
      :link: 01-Python简介与Conda环境-QA
      :link-type: doc
      :class-card: gallery-card

      ^^^

      Conda / 环境 / PATH / 交互式命令行 / 运行方式常见报错。

   .. grid-item-card:: 基本数据类型、变量和运算符 Q&A
      :link: 02-数据类型与运算符-QA
      :link-type: doc
      :class-card: gallery-card

      ^^^

      ``NameError``、类型错误、运算符陷阱与浮点精度。

   .. grid-item-card:: 分支、条件与循环 Q&A
      :link: 03-分支条件循环-QA
      :link-type: doc
      :class-card: gallery-card

      ^^^

      ``IndentationError``、``for``/``while`` 与冒号缩进经典报错。

   .. grid-item-card:: 函数、变量作用域、模块与包 Q&A
      :link: 04-函数作用域模块包-QA
      :link-type: doc
      :class-card: gallery-card

      ^^^

      ``return`` 与 ``print``、可变默认参数、``ImportError`` 与模块路径。

   .. grid-item-card:: 面向对象、函数式编程与高级语法 Q&A
      :link: 05-面向对象函数式高级语法-QA
      :link-type: doc
      :class-card: gallery-card

      ^^^

      ``self``、``__init__``、只读属性、装饰器与生成器的坑。