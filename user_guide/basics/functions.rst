.. _tut-func:

函数及变量作用域、模块和包
==========================

第 4 节 · 模块一 Python 编程基础
贯穿项目第 4 步：把气温处理逻辑封装成函数，放到 ``utils.py`` 模块中。

.. note::

   本节正文由 T-401 交付后填充，以下为内容概要与导读。

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

本章将覆盖的知识点：

- 函数定义 / 调用 / 参数（位置、关键字、默认值）/ 返回值；
- 局部变量与全局变量、作用域规则（LEGB）；
- 模块与包、``import`` 的几种写法、自定义模块 ``utils.py``；
- 提升拓展：``*args`` / ``**kwargs``、``lambda``、``if __name__ == "__main__"`` 守卫。

.. seealso:: 前置知识见 :ref:`tut-flow`（分支与循环）。
