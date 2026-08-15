.. _tut-flow:

分支、条件与循环
================

第 3 节 · 模块一 Python 编程基础
贯穿项目第 3 步：对逐日气温做等级判定（寒冷 / 偏冷 / 适宜 / 炎热），统计各等级天数。

.. note::

   本节正文由 T-301 交付后填充，以下为内容概要与导读。

用 ``if/elif/else`` 做判断，用 ``for`` 遍历序列、``while`` 做条件循环：

.. code-block:: python

   temps = [5.1, 6.3, -2.0, 12.4]
   for t in temps:
       if t < 0:
           print("冰点以下")
       elif t < 10:
           print("偏冷")
       else:
           print("温暖")

   # 找第一个超过阈值的时刻
   series = [3, 4, 8, 12, 6]
   i = 0
   while i < len(series) and series[i] < 10:
       i += 1
   print(f"首次达到 10 的索引: {i}")

本章将覆盖的知识点：

- ``if`` / ``elif`` / ``else`` 分支结构与嵌套；
- ``for`` 遍历列表、字符串、字典，``range()`` 生成等差序列；
- ``while`` 条件循环与避免无限循环；
- ``break`` 跳出、``continue`` 跳过本次；
- 提升拓展：``enumerate``、``zip``、嵌套循环处理多站数据。

.. seealso:: 前置知识见 :ref:`tut-datatype`（数据类型与运算符）；术语见 :doc:`/api/index`。
