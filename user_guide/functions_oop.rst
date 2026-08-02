函数、作用域、模块与面向对象
============================

第 4–5 节。把代码组织成函数与类，理解作用域，并掌握模块化与高级语法。

.. _tut-func:

函数与变量作用域
----------------

函数把可复用的逻辑封装起来。函数内赋值的变量是局部变量，除非用 ``global`` 显式声明：

.. code-block:: python

   def celsius_to_kelvin(c):
       """摄氏度转开尔文"""
       return c + 273.15

   def pressure_profile(levels, p0=1013.25):
       """简化的气压随高度递减"""
       return [p0 * 0.9 ** i for i in range(levels)]

   print(celsius_to_kelvin(25))
   print(pressure_profile(5))

.. _tut-oop:

面向对象与高级语法
------------------

把"气象站"抽象成类，封装数据与行为。装饰器、生成器等高级语法也在此介绍：

.. code-block:: python

   class Station:
       def __init__(self, name, lat, lon):
           self.name, self.lat, self.lon = name, lat, lon
           self._records = []

       def record(self, temp):
           self._records.append(temp)

       @property
       def mean_temp(self):
           return sum(self._records) / len(self._records) if self._records else None

       def __repr__(self):
           return f"<Station {self.name} @ ({self.lat},{self.lon})>"

   lz = Station("兰州", 36.06, 103.83)
   for t in [5.1, 6.3, 4.8]:
       lz.record(t)
   print(lz, "平均", lz.mean_temp)
