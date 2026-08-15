.. _tut-oop:

面向对象与高级语法
==================

第 5 节 · 模块一 Python 编程基础
贯穿项目第 5 步：设计 ``Station`` 类，封装站点信息与气温记录，支持均值/极值统计。

.. note::

   本节正文由 T-501 交付后填充，以下为内容概要与导读。

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

本章将覆盖的知识点：

- 类 / 对象 / ``__init__`` 构造函数 / 实例方法 / 属性；
- 继承、封装、多态；``@property`` 只读属性、``__repr__`` 自定义打印；
- 提升拓展：装饰器、生成器 ``yield``、列表推导式进阶、``match-case``。

.. seealso:: 前置知识见 :ref:`tut-func`（函数与模块）。
