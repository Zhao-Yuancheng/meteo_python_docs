.. _tut-func:

函数及变量作用域、模块和包
==========================

第 4 节 · 模块一 Python 编程基础
贯穿项目第 4 步：把气温处理逻辑封装成函数，放到 ``utils.py`` 模块中。

气象数据处理经常是同一套流程套在不同数据上：今天算兰州站气温，明天算西宁站降水。逻辑差不多，换的是数据源。每次都从头写一遍，效率低；更麻烦的是，一个笔误（比如把 ``* 9 / 5`` 写成 ``* 5 / 9``）会跟着复制粘贴散到各处，不好查。

函数把重复逻辑收成一块，起个名字，换数据再调用。模块再往上走一步：相近的函数放进同一个文件，方便管理和复用。

.. _ch04-animation:

配套动画（T-402）
-------------------

本动画把本节的"函数"讲透：① ``def`` 定义与 ``return`` 返回——调用时进入函数体、返回结果交还给调用者的过程；② 形参／实参的绑定与位置参数、关键字参数的传参方式；③ 变量作用域——函数内部的局部变量与外部全局变量的隔离；④ 模块与 ``import``——把离散的函数收敛进一个文件再整体复用。点击播放，配合下文逐步消化。

.. video:: /_static/videos/T402-函数、作用域、模块动画_av1.webm
   :width: 100%

4.1 函数：把重复的逻辑收起来
----------------------------

从复制粘贴到调用
^^^^^^^^^^^^^^^^

还没学函数时，重复代码最省事的办法就是复制。比如兰州、西宁、张掖三站都要算平均，就抄三遍 ``sum / len``。量小时能跑；一旦算法要改（比如先剔除异常值），每一处都得改，漏一处就是 bug。

函数把这段逻辑收成一个单元，需要时调用即可。调用时看清传入什么、返回什么就够了，内部怎么算可以先不管。这是在做\ **抽象**：细节留在函数里，外面只看到一个简短的接口。

定义与调用
^^^^^^^^^^

.. code-block:: python

   def celsius_to_fahrenheit(celsius):
       """摄氏温度转华氏温度"""
       f = celsius * 9 / 5 + 32
       return f

   # 调用
   result = celsius_to_fahrenheit(25)
   print(result)   # 77.0

``def`` 用来定义函数，后面是函数名和括号。括号里是参数，也就是外界要传入的数据。函数体按缩进写，``return`` 把结果交还给调用者。

定义时函数体不会执行，只是把代码和函数名绑在一起。执行到 ``celsius_to_fahrenheit(25)`` 才会真正跑进去。定义和调用是两件事；而且调用必须写在定义\ **之后**——程序自上而下执行，执行到调用语句时函数必须先定义好，否则会抛 ``NameError``。有一个例外：默认参数的表达式会在定义时算一次，见 4.2。

**常见错误**

- 写了 ``def`` 却忘了调用，以为定义完就会自动跑。
- 该 ``return`` 的地方写了 ``print``。屏幕上有输出，但调用处拿到的是 ``None``，后面没法接着算。
- 函数体缩进不对：少缩进会报错，多缩进则可能把后面不该进函数的代码卷进去。

4.2 参数：函数怎么接收外部数据
------------------------------

参数是函数接收外部数据的通道。把参数搞清楚，函数基本就会用了。

形参和实参
^^^^^^^^^^

- **形参**\（形式参数）：定义时写在括号里的名字，函数内部用来接值。
- **实参**\（实际参数）：调用时真正传进去的值。

.. code-block:: python

   def describe_station(name, lon, lat):   # name, lon, lat 是形参
       return f"{name}: {lon}°E, {lat}°N"

   describe_station("兰州站", 103.82, 36.06)   # "兰州站", 103.82, 36.06 是实参

形参名和调用处的变量名没有对应关系。形参只在函数内部有效，调用时传什么就绑什么，也可以直接传常量，就像上面这样。外面就算有个也叫 ``name`` 的变量，不写进括号里，函数也收不到。

位置参数：按顺序赋值
^^^^^^^^^^^^^^^^^^^^

调用时，实参按顺序依次赋给形参。

.. code-block:: python

   describe_station("兰州站", 103.82, 36.06)   # 正确
   describe_station("兰州站", 36.06, 103.82)   # 经纬度颠倒了

经纬度对调后，站点会落到完全不同的位置。Python 不会报错：它不知道哪个该是经度，只按顺序赋值。程序能跑、结果是错的，这种问题最难查。用位置参数时，实参顺序必须和形参定义一致。

关键字参数：按名字匹配
^^^^^^^^^^^^^^^^^^^^^^

调用时写上形参名再赋值，顺序就无所谓了。

.. code-block:: python

   describe_station(lat=36.06, name="兰州站", lon=103.82)   # 顺序可以打乱

看到 ``lat=36.06`` 就知道这是纬度，读代码也轻松一些。

位置参数和关键字参数可以混用，但位置参数必须在前：

.. code-block:: python

   describe_station("兰州站", 103.82, lat=36.06)   # 正确
   describe_station(name="兰州站", 103.82, 36.06)  # 错误：关键字参数不能出现在位置参数前面

写错形参名（比如 ``latitude=36.06``）会立刻 ``TypeError``，这比经纬度对调好查。漏传没有默认值的参数，也会 ``TypeError``。

默认参数
^^^^^^^^

定义时给形参一个默认值。调用时不传就用默认值，传了就用新值。没有默认值的参数必须写在有默认值的前面，``def f(decimal=1, celsius):`` 会直接语法错误。

.. code-block:: python

   def celsius_to_fahrenheit(celsius, decimal=1):
       f = celsius * 9 / 5 + 32
       return round(f, decimal)

   celsius_to_fahrenheit(26.3)      # decimal 默认 1，返回 79.3
   celsius_to_fahrenheit(26.3, 2)   # decimal 改为 2，返回 79.34

``round`` 改的是数值精度，不是打印时的位数。``round(77.0, 2)`` 仍是 ``77.0``，要显示成 ``77.00`` 得用格式化，例如 ``f"{x:.2f}"``。

多数调用只关心气温，小数位数用默认值即可；真要细控时再显式传入。

有一个常见坑：默认值在函数\ **定义时**\只计算一次，所以不要用列表、字典这类可变对象当默认值。否则多次调用会“记住”上次改过的内容：

.. code-block:: python

   def add_temp(temp, temps_list=[]):   # 错误示范
       temps_list.append(temp)
       return temps_list

   add_temp(25)   # [25]
   add_temp(30)   # [25, 30]，上次的 25 还在

用 ``None`` 占位，在函数里再创建新列表：

.. code-block:: python

   def add_temp(temp, temps_list=None):
       if temps_list is None:
           temps_list = []
       temps_list.append(temp)
       return temps_list

``*args`` 和 ``**kwargs``：数量不确定时
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

有时不知道调用方会传几个值。比如记录气温，有时 1 天，有时 30 天。

``*args`` 把位置参数收进一个元组。若前面还有别的形参，收进来的是剩下的那些；若它是唯一的形参，就是全部位置参数。``args`` 是约定俗成的名字，换成别的也能跑，但别人一看 ``args`` 就懂。

.. code-block:: python

   def log_daily_temps(*args):
       for i, temp in enumerate(args, 1):
           print(f"第{i}天: {temp}°C")

   log_daily_temps(18, 22, 25)          # 3 天
   log_daily_temps(5, 8, 12, 15, 20)    # 5 天

``**kwargs`` 同样只收\ **剩下的**\关键字参数。前面已经对上形参名的，不会进这个字典。函数里它就是普通字典，需要时可以用 ``.get()`` 取值。

.. code-block:: python

   def show_station(**kwargs):
       for key, value in kwargs.items():
           print(f"{key}: {value}")

   show_station(name="兰州站", elevation=1520, region="西北")

最常见的形参顺序是：普通位置参数、带默认值的参数、``*args``、``**kwargs``。

.. code-block:: python

   def func(name, decimal=1, *args, **kwargs):
       pass

这不是全部规则。``*args`` 后面还可以写仅关键字参数，也可以用 ``/`` 标出仅位置参数。入门先按上面这个顺序写即可。顺序写反会语法错误，不是运行到一半才报错。

参数解包：把列表或字典拆开传入
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

已经有一份列表或字典时，不必把值一个个抄进调用括号，用 ``*`` / ``**`` 拆开即可。这和定义时的 ``*args`` / ``**kwargs`` 方向相反。

.. code-block:: python

   info = ["兰州站", 103.82, 36.06]
   describe_station(*info)   # 列表拆成三个位置参数

   info_dict = {"name": "兰州站", "lon": 103.82, "lat": 36.06}
   describe_station(**info_dict)   # 字典拆成关键字参数

列表元素个数对不上，或字典里多了、少了、写错了键，都会 ``TypeError``。解包前先核对长度和键名。

4.3 返回值
----------

函数算完后用 ``return`` 把结果交给调用者。``return`` 一执行，函数立刻结束，后面的代码不会再跑。

.. code-block:: python

   def get_temp_level(temp):
       if temp > 30:
           return "炎热"
       return "其他"   # 只有 temp <= 30 才会走到这里

可以一次返回多个值。Python 实际返回的是一个元组，左边用多个变量接住：

.. code-block:: python

   def calc_stats(temps):
       return min(temps), max(temps), sum(temps) / len(temps)

   t_min, t_max, t_avg = calc_stats([-2, 5, 12, 20, 28])

没写 ``return``，或写了 ``return`` 却没有值，返回的都是 ``None``，表示“没有可用的结果”。

**常见错误**

- 左边变量个数和返回值个数对不上，会 ``ValueError``。返回了三个值，左边只写两个变量，就会炸。
- ``temps`` 若是空列表，``min`` / ``max`` / ``len`` 当除数都会出问题。工具函数里要先判断，不要把“没数据”算成 0°C，见 4.9。
- 在 ``return`` 后面还写处理逻辑。那些行永远不会执行，不是“返回之后再做一次”。

4.4 变量作用域
--------------

作用域决定某段代码能不能访问某个变量。搞不清作用域，会出现很难解释的 bug。

局部变量
^^^^^^^^

在函数内部赋值的变量是局部变量，只能在函数里用。函数结束后，这个名字就没了。

.. code-block:: python

   def process():
       temp = 25   # 局部变量
       print(temp)

   process()
   # print(temp)   # 报错，外面没有 temp

这样函数有自己的工作空间，调用它时不会随便改掉外面的变量。

全局变量
^^^^^^^^

写在模块最顶层的变量是全局变量，模块里各处都能读。

.. code-block:: python

   station = "兰州站"   # 全局变量

   def show():
       print(station)   # 可以读

   show()
   print(station)       # 外面也能读

注意：只要函数里\ **某处给这个名字赋了值**，整个函数都把它当局部变量，包括赋值前面的读取。下面会报 ``UnboundLocalError``，不是先打印全局的 ``station`` 再改局部的：

.. code-block:: python

   station = "兰州站"

   def show():
       print(station)     # 这里也会报错
       station = "西宁站"  # 有这行赋值，station 在整个函数里都是局部的

在函数里修改全局变量：``global``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

只读全局变量不用声明。要\ **换掉这个名字指向的对象**\（``count = 1``、``count += 1``），必须写 ``global``。

.. code-block:: python

   count = 0

   def count_record():
       global count   # 改的是外面的 count，不要新建局部变量
       count += 1

   count_record()
   print(count)   # 1

两种容易混的情况：

- 不加 ``global`` 就写 ``count += 1``：Python 把 ``count`` 当成局部变量，右边却还没赋值，会报 ``UnboundLocalError``，不是“全局悄悄没变”。
- 不加 ``global`` 写 ``count = 1``：不会报错，但改的是局部变量，外面的 ``count`` 仍是 ``0``。

改列表、字典\ **里面的内容**\不用 ``global``。``append``、改某个元素，动的是同一个对象，不是把名字指到别处：

.. code-block:: python

   temps = []

   def add(temp):
       temps.append(temp)   # 不用 global，外面的列表会被加上新值

   add(25)
   print(temps)   # [25]

如果写成 ``temps = temps + [temp]``，那是在创建新列表再赋值，就必须 ``global``。先分清“改对象”和“换名字”。

尽量少用全局变量。函数的输入最好从参数进来，结果从返回值出去。全局变量谁都能改，出了问题要沿整份代码去追。

嵌套函数与 ``nonlocal``
^^^^^^^^^^^^^^^^^^^^^^^

函数里面还可以再定义函数。内层要改外层函数的局部变量时，用 ``nonlocal``：

.. code-block:: python

   def outer():
       station = "兰州站"
       def inner():
           nonlocal station
           station = "西宁站"
       inner()
       print(station)   # 西宁站

``global`` 改的是模块顶层的名字，``nonlocal`` 改的是外层函数里的名字。对象搞反了会 ``SyntaxError``\（外层没有这个局部变量），或改到你以为没在改的地方。

4.5 lambda：单行匿名函数
-------------------------

``lambda`` 用来写只有一个表达式的匿名函数。冒号后面的表达式就是返回值，不能写多行，只适合很短的逻辑。

.. code-block:: python

   def c_to_f(c):
       return c * 9 / 5 + 32

   c_to_f = lambda c: c * 9 / 5 + 32   # 和上面等价；若要起名字，更常见的是直接用 def

最常见的用法是当作别的函数的参数，例如 ``sorted`` 的 ``key``：

.. code-block:: python

   stations = [
       {"name": "兰州站", "elevation": 1520},
       {"name": "西宁站", "elevation": 2295},
   ]
   sorted_stations = sorted(stations, key=lambda s: s["elevation"])

不用 ``lambda`` 就得先单独定义一个函数再传给 ``key``，这里用它只是少写几行。

逻辑一长就改回 ``def``。另外，在循环里造一批 ``lambda`` 时要小心，它们用到的循环变量是\ **用的时候**\才取值，不是创建时定住的：

.. code-block:: python

   funcs = [lambda: i for i in range(3)]
   print(funcs[0]())   # 2，不是 0

需要定住的话，写成 ``lambda i=i: i`` 这种默认参数，或直接用普通函数。入门阶段更稳妥的办法是少在循环里堆 ``lambda``。

4.6 递归：函数调用自己
----------------------

递归就是函数调用自身。适合能拆成同类子问题的情况，比如走一层套一层的站点树，或处理本身就按递归定义的结构。

.. code-block:: python

   def sum_first_n(temps, n):
       """递归求前 n 天气温之和（不是气象学里的积温）"""
       if n == 0:
           return 0
       return temps[n - 1] + sum_first_n(temps, n - 1)

气象上的积温一般是日均温超过某个界限温度后再累加，不能把原始气温直接加起来。上面只是用求和演示递归。

必须有\ **终止条件**。没有的话会一直调用自己，直到超过 Python 的递归深度上限（默认大约 1000 层）后崩溃。代码可以写得很短，但层数深时更费内存、也更慢，这种求和用循环更合适。

**常见错误**

- 漏写终止条件，或终止条件永远进不去（比如写成 ``if n == 0`` 却从 ``n = -1`` 往下减）。
- ``n`` 比 ``len(temps)`` 大，会 ``IndexError``；``n`` 为负数，终止条件够不着，最后还是递归爆掉。
- 把简单求和、遍历列表做成递归。能用 ``for`` / ``sum`` 解决的，不必为了“用上递归”硬写。

4.7 函数是对象
--------------

在 Python 里，函数和其他对象一样，可以赋值、当作参数、当作返回值。

.. code-block:: python

   # 赋值给变量
   c_to_f = celsius_to_fahrenheit
   print(c_to_f(25))   # 77.0

   # 作为参数传递
   def apply_to_temps(temps, func):
       return [func(t) for t in temps]

   apply_to_temps([0, 10, 20], c_to_f)

   # 作为返回值（闭包）
   def make_checker(threshold):
       def checker(temp):
           return temp > threshold
       return checker

   check_hot = make_checker(30)
   check_hot(28)   # False

最后这个例子是\ **闭包**：内层的 ``checker`` 会记住外层传入的 ``threshold``，外层函数已经返回也不影响。可以用来生成不同阈值的检查函数。

注意括号：``c_to_f = celsius_to_fahrenheit`` 是把函数本身交给变量；``c_to_f = celsius_to_fahrenheit()`` 是先调用再赋值，右边往往得到一个数字或 ``None``，不是转换函数。传给 ``apply_to_temps`` 时同样不要多写括号。

``make_checker`` 返回的是 ``checker`` 这个函数，不是 ``checker(...)`` 的结果。少写一对括号，外面才能按不同气温反复检查。

4.8 模块与包
------------

一个 ``.py`` 里堆了几十个函数就不好找了。把相近的函数分到不同文件里，每个 ``.py`` 就是一个\ **模块**。

导入
^^^^

.. code-block:: python

   import weather_utils                     # 导入整个模块
   import weather_utils as wu               # 重命名
   from weather_utils import c_to_f         # 只导入特定函数
   from weather_utils import c_to_f as c2f  # 导入时改名

少用 ``from weather_utils import *``。它会把模块里的名字一股脑倒进当前文件，和自己写的函数重名时，后导入的会盖住前面的，不好查。

模块文件不要和标准库同名。项目目录里如果有 ``json.py``、``random.py``，``import json`` 可能先导入到你自己的空文件，报一些莫名其妙的 ``AttributeError``。

``__name__``：区分“直接运行”和“被导入”
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

每个模块都有 ``__name__``。直接运行 ``python weather_utils.py`` 时，它是 ``"__main__"``；被导入时，它是模块的导入名（单文件一般是去掉 ``.py`` 的文件名，例如 ``"weather_utils"``；若在包里则可能是 ``"pkg.weather_utils"``）。

.. code-block:: python

   # weather_utils.py
   def c_to_f(c):
       return c * 9 / 5 + 32

   if __name__ == "__main__":
       # 只有直接运行本文件时才执行
       print(c_to_f(25))

这样可以在模块底部放演示或自测。别人 ``import`` 时这些代码不会跑；你自己运行这个文件时才会跑。

自测代码如果写在 ``if __name__ == "__main__":`` 外面，一被导入就会打印一堆东西，主程序的输出会夹杂工具模块的调试信息。

包
^^

模块再多，就用文件夹分组，这就是包。入门项目里通常放一个 ``__init__.py``\（可以是空的）。Python 3.3 之后没有它也可以构成命名空间包，但常规包仍然建议留着这个文件。

两个模块互相 ``import``，可能形成循环导入，表现为“模块有这个函数，却提示没有”。入门阶段把工具放进 ``utils.py``、主程序放进 ``main.py``、只让主程序导入工具，一般能避开。

4.9 项目实践：气温工具模块
--------------------------

学完本章后，「兰州气温观测数据分析与可视化系统」要把气温处理收成函数，放到独立模块里。下面的冷/热分界是教学用的自拟阈值，不是气象规范。

先看不拆函数时常见的写法：

.. code-block:: python

   temps = [-5, -3, 0, 2, -1, -4, -6, -2, 1, 3]

   avg = sum(temps) / len(temps)
   print(f"平均气温: {avg}°C")

   cold = cool = warm = hot = 0
   for t in temps:
       if t <= -5:
           cold += 1
       elif -5 < t <= 5:
           cool += 1
       elif 5 < t <= 28:
           warm += 1
       else:
           hot += 1
   print(f"寒冷: {cold}天, 偏冷: {cool}天, 适宜: {warm}天, 炎热: {hot}天")

能跑。换西宁站、张掖站，或把 28°C 改成 30°C，就得连着改好几份拷贝。流程没变，变的是数据；阈值也不该复制多份，集中写在一个函数里即可。入门阶段不必把阈值再做成参数。

工具函数写小一点，再拼起来用。``classify_temperature`` 判定单日，``classify_temperatures`` 复用它做批量统计：

.. code-block:: python

   # utils.py

   def classify_temperature(temp):
       """判定单个气温的等级（教学用阈值）。"""
       if temp <= -5:
           return "寒冷"
       elif -5 < temp <= 5:
           return "偏冷"
       elif 5 < temp <= 28:
           return "适宜"
       else:
           return "炎热"


   def classify_temperatures(temps):
       """统计一批气温中各等级的天数。"""
       result = {"寒冷": 0, "偏冷": 0, "适宜": 0, "炎热": 0}
       for t in temps:
           result[classify_temperature(t)] += 1
       return result


   def calc_average(temps):
       """计算平均气温。空列表没有平均值，不能当成 0°C。"""
       if not temps:
           raise ValueError("气温列表为空，无法计算平均值")
       return sum(temps) / len(temps)


   if __name__ == "__main__":
       test_temps = [-8, 0, 15, 30]
       for t in test_temps:
           print(f"{t}°C → {classify_temperature(t)}")
       print(f"平均: {calc_average(test_temps)}°C")

直接运行 ``python utils.py`` 时会执行自测；在 ``main.py`` 里 ``import utils`` 时 ``__name__`` 是 ``"utils"``，自测不会跟着跑。规则见 4.8。

.. code-block:: python

   # main.py
   import utils

   jan_temps = [-5, -3, 0, 2, -1, -4, -6, -2, 1, 3]

   avg = utils.calc_average(jan_temps)
   stats = utils.classify_temperatures(jan_temps)

   print(f"平均气温: {avg:.1f}°C")
   for level, count in stats.items():
       print(f"{level}: {count}天")

主程序只负责准备数据、调用工具、打印结果。等级怎么划分、平均怎么算，留在 ``utils.py``。

**写的时候容易踩的坑**

- ``classify_temperatures`` 里的字典键，必须和 ``classify_temperature`` 的返回值对得上。一边改成“偏暖”、另一边字典还是“适宜”，会 ``KeyError``。
- 空列表不要返回 ``0``。``0°C`` 是一个真实气温，和“没有数据”不是一回事。
- 改完 ``utils.py`` 后要重新运行 ``main.py``。只盯着编辑器看，运行的还是旧代码。
- 从项目以外的目录运行时，确认当前目录能找到 ``utils.py``，否则会 ``ModuleNotFoundError``。

.. seealso:: 配套练习：:doc:`/tutorials/basics/ch04_practice`　·　术语参考：:doc:`/api/ch04_terms`　·　示例画廊 :doc:`/gallery/plot_basics/index`。