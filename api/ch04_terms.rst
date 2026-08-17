第 4 章术语：函数及变量作用域、模块和包
========================================

配套 :ref:`tut-func` 正文使用。每个词条 = 一句话定义 + **生活类比** + **代码示例** + **易混淆点**。本章术语围绕"把逻辑收成函数、用模块与包组织代码"展开。

.. seealso:: 配套正文：:doc:`/user_guide/basics/functions`　·　配套练习：:doc:`/tutorials/ch04_practice`

.. glossary::

   函数 function
      把一段可复用的逻辑打包并命名的程序单元，随取随用。相当于气象站里一套"标准化观测流程"：读表、换算、记录，步骤固定。把兰州站数据放进去能跑，换西宁站数据也能跑，不用每次重写一遍。

      .. code-block:: python

         def c_to_f(celsius):
             """摄氏度转华氏度"""
             return celsius * 9 / 5 + 32

         print(c_to_f(25))     # 77.0
         print(type(c_to_f))   # <class 'function'>

      **易混淆点** —— 函数名后面必须带括号才算"调用"：``c_to_f`` 是函数本身，``c_to_f(25)`` 才是执行并拿到结果；定义时函数体不会运行，只有调用才执行；用 ``return`` 把结果交出去，没写 ``return`` 的返回 ``None``。

   形参与实参
      形参（形式参数）是定义时写在括号里接收值的名字标签，实参（实际参数）是调用时真正传进去的具体数值。相当于站点观测表的"登记栏"：形参是登记栏上预留的空位（写"气温"、"风速"的地方），实参是每次真正填进去的具体数值。

      .. code-block:: python

         def describe(name, elev):        # name, elev 是形参
             return f"{name}海拔{elev}米"

         print(describe("兰州站", 1520))   # "兰州站", 1520 是实参

      **易混淆点** —— 形参在定义时写、实参在调用时传；位置参数按顺序匹配（顺序颠倒不会报错，只是结果错），关键字参数 ``name="兰州站"`` 按名字匹配、顺序可以打乱；写错形参名会立刻 ``TypeError``。

   返回值 return
      函数算完后通过 ``return`` 交还给调用者的结果，调用处才能接着往下算。相当于观测完成后交上去的"结果报告"。

      .. code-block:: python

         def avg_temp(temps):
             return sum(temps) / len(temps)

         result = avg_temp([12, 15, 18])
         print(result)   # 15.0

      **易混淆点** —— ``return`` 一执行函数立刻结束，后面的代码不会跑；可以一次返回多个值（内部打包成元组），左边用多个变量接住；该写 ``return`` 却只写了 ``print``，调用处拿到的是 ``None``，没法继续计算。

   局部变量 local variable
      在函数内部赋值、只在函数内有效的变量。像只在当天该站流程内有效的"工作草稿纸"：函数结束，草稿纸就被收走，函数外部看不到、也取不到。

      .. code-block:: python

         def process():
             temp = 25      # 局部变量
             print(temp)

         process()
         # print(temp)      # 报错 NameError，函数外没有 temp

      **易混淆点** —— 局部变量只在函数内有效，函数结束后这个名字就消失；只要函数里某处给某个名字赋了值，整个函数都把它当局部变量（包括它前面的读取，会报 ``UnboundLocalError``）。

   全局变量 global variable
      写在模块最顶层、模块里各处都能读的变量。像挂在值班室里人人能读的"全站公告板"。读着方便，乱改却容易出问题。

      .. code-block:: python

         station = "兰州站"      # 全局变量

         def show():
             print(station)      # 函数内可以直接读

         show()

      **易混淆点** —— 函数内只做"读取"不需要声明；要让 ``station`` 指到新对象（``station = "西宁站"``）就必须写 ``global``，否则只是新建一个局部变量、外面全局值不变；``append`` 这类"修改列表/字典里的内容"不改变名字，不需要 ``global``。

   作用域 scope
      决定某个名字在哪段代码里"可见"、在哪里可以访问的规则。相当于气象资料的"可见范围"：基层站数据只在站内可查，省台汇总数据全省可查。Python 里每个名字也有它的可见范围——局部、全局、外层函数（``nonlocal``）。

      .. code-block:: python

         station = "兰州站"        # 全局作用域

         def show():
             local_sta = "西宁站"   # 局部作用域
             print(local_sta)
             print(station)        # 可以向上读到全局

      **易混淆点** —— 查找规则是从内向外：函数内优先找局部名，没有再去全局找；函数内"读"全局不用声明，"改"全局才需要 ``global``；``nonlocal`` 用在嵌套函数里修改外层函数的局部变量。

   global 声明
      在函数内声明某个名字指向模块顶层全局变量的关键字，让改动真正落到全局变量上。像在公告栏上改写前先"申请权限"：声明了 ``global``，改动才真正落到全局变量上；没声明，改动只会新建一个同名局部变量。

      .. code-block:: python

         count = 0

         def add_record():
             global count     # 改的是外面的 count，不新建局部变量
             count += 1

         add_record()
         print(count)         # 1

      **易混淆点** —— 只读不用 ``global``；要重新赋值就必须要，否则 ``count += 1`` 会报 ``UnboundLocalError``，而 ``count = 1`` 只是改了局部（全局仍是 0）；先分清"修改对象内容"（如 ``append``，不用 ``global``）和"换名字指向新对象"（如 ``temp = temp + [x]``，需要 ``global``）。

   模块 module
      以一个 ``.py`` 文件形式存在、把相近函数收在一起的代码单元。像一本装订好的"专业操作规程手册"，方便复用，也避免整个项目堆在一个文件里找不到。

      .. code-block:: python

         # weather_utils.py
         def c_to_f(celsius):
             return celsius * 9 / 5 + 32

      **易混淆点** —— 模块就是一个 ``.py`` 文件；用 ``import weather_utils`` 导入整个模块后，要用 ``weather_utils.c_to_f(...)`` 调用；模块名别和标准库同名（如 ``json.py``、``random.py``），否则 ``import json`` 可能导成你自己的空文件，报莫名其妙的 ``AttributeError``。

   包 package
      用文件夹把多个模块分组构成的目录，通常放一个（可以是空的）``__init__.py`` 作标识。像档案柜里按站点分格子的"文件夹柜"。

      .. code-block:: python

         # 目录结构
         # weather_pkg/
         #   __init__.py
         #   utils.py
         # main.py

         from weather_pkg import utils          # 从包导入模块
         average = utils.calc_average(temps)    # 用 模块.函数名 调用

      **易混淆点** —— 导入写完整路径 ``from weather_pkg.utils import c_to_f``，直接拿函数名用；常规包一般保留 ``__init__.py``（Python 3.3 之后没有它也能构成命名空间包）；两个模块互相 ``import`` 会形成循环导入，表现为"模块明明有这个函数却提示没定义"——入门阶段让主程序单向导入工具模块即可避开。

   导入 import 与 __name__
       ``import`` 把别的模块里的工具"借"进当前文件来用；``__name__`` 用来判断当前这本手册是被"直接翻看运行"，还是被别的文件"引用"。

      .. code-block:: python

         if __name__ == "__main__":
             print("只有直接运行本文件时才执行")

      **易混淆点** —— ``import 模块`` 要用 ``模块.函数名``；``from 模块 import 函数`` 直接用函数名；少用 ``from 模块 import *``，避免名字被批量覆盖、查不出冲突；自测代码要放进 ``if __name__ == "__main__":``，否则被导入时会莫名打印一堆调试信息。