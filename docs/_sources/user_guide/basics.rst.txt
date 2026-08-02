基本数据类型、分支与循环
========================

第 2–3 节。覆盖数据类型、运算符，以及分支、条件、循环三种控制流。

.. _tut-datatype:

数据类型与运算符
----------------

Python 内置数字、字符串、列表、字典等类型。气象数据常用列表存站点观测、字典存元信息：

.. code-block:: python

   station = "兰州"            # str
   elev = 1517.2              # float，海拔(m)
   temps = [5.1, 6.3, 4.8]    # list，近三日气温
   meta = {"lat": 36.06, "lon": 103.83}   # dict

   avg = sum(temps) / len(temps)
   print(f"{station} 平均气温 {avg:.1f} °C")

.. _tut-flow:

分支、条件与循环
----------------

用 ``if/elif/else`` 做判断，用 ``for`` 遍历序列、``while`` 做条件循环：

.. code-block:: python

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
