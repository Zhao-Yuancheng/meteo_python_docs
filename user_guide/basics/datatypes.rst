.. _tut-datatype:

基本数据类型、变量和运算符
==========================

第 2 节 · 模块一 Python 编程基础
贯穿项目第 2 步：用变量和基本类型存储兰州站元信息（站名、经纬度、海拔）。

计算机程序的基本任务是**处理数据**，而数据类型（data type）就是给数据贴上的"分类标签"——它告诉解释器这份数据是数字、文字还是一个容器，以及能对它做什么运算。气象工作里到处都是类型选择问题：气温要用带小数的 ``float``、站号要用 ``int`` 或 ``str``、经纬度适合用 :term:`元组 <不可变类型>`、一站多要素的记录适合用 ``dict``。选对了类型，后面的计算、绘图才不会处处报错。

学完本章你将能够：

#. 区分 Python 的常用内置类型：``int``、``float``、``complex``、``str``、``list``、``tuple``、``dict``、``set``、``bool``、``NoneType``；
#. 正确给变量赋值、命名，并用 ``type()`` 与 ``isinstance()`` 检查类型；
#. 熟练使用算术、比较、逻辑、成员运算符处理气象数据；
#. 用 f-string 把计算结果格式化成规范的观测报告。

.. grid:: 1 2 2 3
   :gutter: 2

   .. grid-item-card:: 🎬 配套动画
      :link: ch02-animation
      :link-type: ref
      :class-card: gallery-card

      ^^^

      变量"贴标签"与三种容器对比

   .. grid-item-card:: ✏️ 配套练习
      :link: /tutorials/ch02_practice
      :link-type: doc
      :class-card: gallery-card

      ^^^

      5 道西北站点实战题（含提示）

   .. grid-item-card:: 🖼 可执行示例
      :link: /gallery/plot_basics/plot_datatypes
      :link-type: doc
      :class-card: gallery-card

      ^^^

      用基本类型存储站点信息并绘图

.. _ch02-animation:

配套动画（T-202 占位）
---------------------

.. figure:: /_static/animations/ch02_types_placeholder.svg
   :alt: 第 2 章配套动画占位图
   :width: 88%
   :align: center

   **图 2-1** 配套动画（T-202 交付后替换本占位图）：① 变量是"贴标签"——内存盒子先存在，变量名标签贴上去；② ``int`` 与 ``float`` 的精度差异（``0.1 + 0.2 != 0.3`` 的可视化）；③ 列表 / 元组 / 字典三种容器类比（抽屉、密封盒、标签柜）。

变量与赋值：先有盒子，再贴标签
------------------------------

Python 的 :term:`变量 <变量>` 不是"盒子"，而是**贴在对象上的标签**：解释器先在内存里创建对象 ``1517.2``，再把变量名 ``elevation`` 这张标签贴上去。同一个对象可以贴多张标签，赋值只是换标签、贴新标签，从不复制数据本身。

.. code-block:: python

   station_name = "兰州"     # str：站名
   station_id = 52889        # int：区站号
   elevation = 1517.2        # float：海拔（m）

   print(type(station_name))  # <class 'str'>
   print(type(station_id))    # <class 'int'>
   print(type(elevation))     # <class 'float'>

命名遵循 PEP 8 的几条硬规矩，气象变量推荐"物理量 + 方向/统计量"的全拼写法：

- 只用字母、数字、下划线，且不能以数字开头（``1temp`` ✗，``temp_1`` ✓）；
- 区分大小写：``Temp`` 与 ``temp`` 是两个变量；
- 不能与关键字重名（``if``、``for``、``class`` 等）；
- 用 ``snake_case`` 蛇形命名：``temp_max``、``temp_min``、``wind_speed_u``，见名知义；
- 慎用 ``l``、``O`` 这类容易看成 ``1``、``0`` 的单字符名。

.. code-block:: python

   temp_max = 32.6        # 日最高气温（°C）
   temp_min = 18.4        # 日最低气温（°C）
   temp_range = temp_max - temp_min   # 日较差
   print(f"今日日较差 {temp_range:.1f} °C")

赋值还有两种常用变体：

.. code-block:: python

   # ① 多重赋值：一次给一组"标签"（经度、纬度天然成对出现）
   lon, lat = 103.83, 36.06

   # ② 增量赋值：累加观测
   temp_sum = 0.0
   for t in [5.1, 6.3, 4.8]:   # for 循环下一章细讲，这里先混个脸熟
       temp_sum += t
   print(temp_sum)   # 16.2

检查类型除了 ``type()``，更推荐 ``isinstance()``——它对"是不是某类"返回 :term:`布尔值 <布尔值>`，方便写判断：

.. code-block:: python

   humidity = 45.0
   print(isinstance(humidity, float))         # True
   print(isinstance(humidity, (int, float)))  # True：允许 int 或 float 都行

.. seealso:: 名词详解见 :doc:`/api/ch02_terms`（:term:`变量 <变量>`、:term:`可变类型`、:term:`不可变类型`）。

数字类型：int、float 与 complex
-------------------------------

整型 int
~~~~~~~~

:term:`整型 <整型 int>` 是**没有小数部分**的整数，Python 的 ``int`` 没有大小上限（只受内存限制），这在处理大数值（如以秒计的再分析数据时间戳）时很省心。气象里典型的整型：区站号、年份、一天的观测时次（08 时、14 时、20 时）。

.. code-block:: python

   station_id = 52889          # 兰州站区站号
   year_days = 366             # 2024 年是闰年
   obs_hour = 14               # 14 时观测

   print(type(station_id))     # <class 'int'>

浮点型 float
~~~~~~~~~~~~

带小数部分的数是 :term:`浮点型 <浮点型 float>`。气温、气压、湿度、经纬度、海拔……几乎所有连续物理量都用 ``float`` 存储——它像一把带毫米刻度的尺子，能分辨 36.06°N 与 36.07°N 的差别。

.. code-block:: python

   temp = 12.7                 # 气温（°C）
   pressure = 848.6            # 本站气压（hPa）
   print(type(temp))           # <class 'float'>

.. warning::

   **必知考点：浮点数有精度误差。** 浮点型按 IEEE 754 标准用二进制存储，``0.1`` 无法被精确表示，于是 ``0.1 + 0.2`` 得到 ``0.30000000000000004``，``0.1 + 0.2 == 0.3`` 为 ``False``。
   对气象数据而言，这意味着**判断两个温度"相等"时不要直接用 ``==``**，改用容差比较：

   .. code-block:: python

      t1, t2 = 0.1 + 0.2, 0.3
      print(abs(t1 - t2) < 1e-9)           # True：差值小于容差即视为相等
      print(round(t1, 6) == round(t2, 6))  # True：先四舍五入再比较

保留小数位最常用的办法是 f-string 格式说明符 ``:.2f``（详见 :ref:`ch02-fstring`）：

.. code-block:: python

   pi = 3.1415926
   print(f"{pi:.2f}")          # 3.14（四舍五入保留两位）

复数 complex（了解即可）
~~~~~~~~~~~~~~~~~~~~~~~

复数由实部和虚部组成，虚部以 ``j`` 结尾。基础阶段用得少，但它在波动与信号分析（如研究大气振荡时做傅里叶变换）里会重新登场。注意：实部和虚部**都是浮点数**，哪怕你写的是整数。

.. code-block:: python

   number_3 = 2 + 3j
   print(type(number_3))       # <class 'complex'>
   print(number_3.real)        # 2.0（注意是 float）
   print(number_3.imag)        # 3.0

.. dropdown:: 拓展：需要精确小数时用 Decimal

   观测数据建档、经费核算等不容许 ``0.1 + 0.2`` 这类误差的场合，可以用标准库 ``decimal`` 指定有效位数（注意用**字符串**构造）：

   .. code-block:: python

      from decimal import Decimal, getcontext

      getcontext().prec = 5          # 设定有效数字为 5 位
      x = Decimal("0.3")
      y = Decimal("0.36")
      print(x + y)                   # 0.66，绝无精度误差

   气象计算里一般保留 ``float`` 即可——10⁻¹⁷ 量级的误差远小于观测仪器精度，科学计算库 NumPy 也只认 ``float``。``Decimal`` 知道有这回事就好。

序列之一：字符串 str
--------------------

:term:`字符串 <字符串 str>` 是由字符组成的序列，用单引号或双引号包裹均可。它相当于观测记录本上的**文字描述**：站名、天气现象、风向的十六方位码……只用于读取和展示，不能直接参与算术运算。

索引与切片
~~~~~~~~~~

字符串是序列，就能按下标取字符。Python 序列**从 0 开始计数**，:term:`切片 <切片>` ``[a:b]`` 遵循**左闭右开**——取到下标 ``a``，取不到下标 ``b``（:term:`索引 <索引>` 详解见术语 API）。

.. code-block:: python

   str1 = "Lanzhou"
   print(str1[1:4])    # anz  （下标 1、2、3）
   print(str1[:3])     # Lan  （省略起点：从头开始）
   print(str1[-2:])    # hu   （负号：从末尾倒数，-1 是最后一个）
   print(str1[::2])    # Lnzu （步长 2：隔一个取一个）

拼接与格式化
~~~~~~~~~~~~

.. code-block:: python

   station = "Lanzhou"
   report = f"{station} station, temp 25.6 C"   # f-string，:ref:`ch02-fstring` 详述
   print(report)
   print(station + " " + "52889")                # + 直接拼接
   print("-".join(["2024", "07", "15"]))         # join：用 - 连接成日期 2024-07-15

常用方法速查：``.upper()`` / ``.lower()`` 转大小写、``.strip()`` 去首尾空白、``.split(",")`` 按逗号拆成列表、``.replace("T", "t")`` 替换子串。CSV 气温文件的每一行，就是靠 ``split`` 拆开再用的。

.. warning::

   两个易错点：

   #. **数字加引号就成了字符串**：``"25"`` 是文本，``"25" + 5`` 直接抛 ``TypeError``，须先转换 ``int("25") + 5``；
   #. **字符串不可变**：``str1[0] = "H"`` 会报错，只能生成新串 ``str1 = "H" + str1[1:]``。

序列之二：列表 list
-------------------

列表用方括号 ``[]`` 表示，**有序、可增删改**，能混装任意类型——像一排贴了顺序标签的抽屉（:term:`可变类型`）。逐日气温序列、多站站名、探空各层高度，都先用列表存。

增、删、改、查
~~~~~~~~~~~~~~

.. code-block:: python

   max_temps = [32.6, 34.1, 36.9]     # 近三日日最高气温（°C）

   max_temps.append(37.2)             # 尾部追加新的一天
   print(max_temps)                   # [32.6, 34.1, 36.9, 37.2]

   max_temps[0] = 33.0                # 修改：下标 0 的复核值
   max_temps.remove(34.1)             # 按值删除第一个匹配项
   last = max_temps.pop()             # 弹出末尾元素并返回
   print(max_temps, last)             # [33.0, 36.9] 37.2

统计运算
~~~~~~~~

列表配 ``sum`` / ``max`` / ``min`` / ``len`` / ``sorted`` 五件套，就能完成初级气候统计：

.. code-block:: python

   temps = [32.6, 34.1, 36.9, 37.2]
   avg = sum(temps) / len(temps)      # 平均值
   print(f"{avg:.1f}")                # 35.2
   print(max(temps), min(temps))      # 37.2 32.6
   print(sorted(temps, reverse=True)) # [37.2, 36.9, 34.1, 32.6]

隔位切片：从混合记录中提取气温
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

旧式观测文件常把"日期、温度"交替写在一行里。利用步长切片可以隔位取出温度（下标 1、3、5……），再用列表推导式筛出高温日：

.. code-block:: python

   record = [711, 35.6, 712, 37.8, 713, 34.5]   # 日期、气温交替
   temps = record[1::2]                          # [35.6, 37.8, 34.5]
   high_days = [t for t in temps if t >= 35]     # 列表推导式：只留 ≥35 °C
   print(f"高温天气有 {len(high_days)} 天")      # 高温天气有 2 天

.. note::

   实际项目中应优先用字典（日期→温度）或 Pandas 表格存混合数据，"隔位切片"只是演示序列能力。

序列之三：元组 tuple
--------------------

元组与列表相似，但**一经创建不可修改**，用圆括号 ``()`` 表示。它像封装出厂的探空仪器参数：坐标、海拔、传感器标定值——写入后谁都不许动，动了就报错，反而安全（:term:`不可变类型`）。

.. code-block:: python

   location = (103.83, 36.06, 1517.2)   # (经度, 纬度, 海拔) —— 兰州站坐标
   # location[0] = 104.0                # TypeError！元组不支持修改

   print(location[0])                   # 103.83：可以读，不可改

.. warning::

   **单元素元组必须带逗号**：``(1517,)`` 是元组，``(1517)`` 只是一个加了括号的 ``int``。

元组最常用的操作是**解包**——按顺序一一对应地取值，经纬度、多要素观测记录拆开写最舒服：

.. code-block:: python

   data = (25.2, 1013.0, 60)            # (气温, 海平面气压, 相对湿度)
   temp, pressure, humidity = data      # 解包：按位置对应
   print(f"温度 {temp} °C，气压 {pressure} hPa，湿度 {humidity} %")

因为不可变，元组的方法只有两个"只读"统计：``count`` 计次数、``index`` 查下标。

.. code-block:: python

   temps = (36.9, 35.6, 38.3, 35.6)
   print(temps.count(35.6))   # 2
   print(temps.index(38.3))   # 2

另一个隐藏福利：**元组可以做字典的键，列表不行**（详见下节）。

映射：字典 dict
---------------

列表按"位置"取值，字典按"名字"取值。字典由**键（key）与值（value）**成对组成，是映射类型——像站点的档案柜：报出"温度"这个抽屉名，直接取出里面的数值，与存放顺序无关。

.. code-block:: python

   station = {
       "station_id": "52889",
       "name": "兰州",
       "temp": 35.6,
       "humidity": 90,
       "location": (103.83, 36.06),
   }

   print(station["name"])        # 兰州：按键查值
   station["temp"] = 30.4        # 改：更新已有键
   station["wind"] = 3.5         # 增：新增键值对
   del station["humidity"]       # 删：删除键值对
   print(station)

遍历字典的三种姿势：

.. code-block:: python

   for key in station:                    # 只遍历键
       print(key)
   for value in station.values():         # 只遍历值
       print(value)
   for key, value in station.items():     # 键值成对（注意这里又用到了元组解包）
       print(f"{key}: {value}")

站点多了，就**嵌套**——外层键是站号，内层又是一台档案柜：

.. code-block:: python

   stations = {
       "52889": {"name": "兰州", "temp": 25.6, "humidity": 40},
       "52418": {"name": "敦煌", "temp": 28.1, "humidity": 26},
   }
   print(stations["52418"]["temp"])       # 28.1：两级索引

.. tip::

   **规则**：值可以是任意类型；键必须是**不可变**类型——``str``、``int``、``float``、``tuple`` 都行，``list`` 不行（可变的东西没有稳定的"档案编号"）。
   **小技巧**：站号若以 ``0`` 开头（如 ``"010"``），必须存成字符串，存成 ``int`` 会丢掉前导零。

集合 set
-------

集合用大括号 ``{}`` 表示（空集合须写 ``set()``，因为 ``{}`` 是空字典），两大特性：**无序**、**元素唯一**。它最适合回答"有哪些、重不重、交不交叉"这类问题——比如统计本月出现过哪些天气现象、两地高温站的重合情况。

.. code-block:: python

   high_temp = {"兰州", "西安", "重庆", "南京"}    # 出现高温的站
   heavy_rain = {"西安", "广州", "深圳", "南京"}   # 出现暴雨的站

   print(high_temp & heavy_rain)   # 交集 &：又高温又暴雨
   print(high_temp | heavy_rain)   # 并集 |：至少占其一
   print(high_temp - heavy_rain)   # 差集 -：只高温未暴雨
   print(high_temp ^ heavy_rain)   # 对称差 ^：恰好只占其一

唯一性天然适合**去重**：

.. code-block:: python

   phenomena = ["晴", "多云", "晴", "扬沙", "多云"]
   print(set(phenomena))           # {'晴', '多云', '扬沙'}（顺序随机）
   print(len(set(phenomena)))      # 3：本月出现过 3 种天气现象

增删元素：

.. code-block:: python

   stations = {"北京", "上海"}
   stations.add("广州")            # 添加
   stations.discard("武汉")        # 删除（元素不存在也不报错，推荐）
   stations.remove("北京")         # 删除（元素不存在会抛 KeyError）

布尔型 bool 与空值 None
-----------------------

布尔型 bool
~~~~~~~~~~~

布尔型只有两个值：``True`` 和 ``False``（**首字母必须大写**，写 ``true`` 会得到 ``NameError``）。它对应观测里大量的是非判断：是否高温、是否达暴雨量级、风是否超阈值。比较运算的结果就是布尔值：

.. code-block:: python

   temp = 36.2
   is_high = temp >= 35            # 高温日判据
   print(is_high)                  # True
   print(type(is_high))            # <class 'bool'>

数字与布尔可以互通：``0``、``0.0``、``""``、``[]`` 等空容器视为 ``False``，其余视为 ``True``。因此 ``if temps:`` 可以优雅地表达"列表非空才统计"。

空值 None
~~~~~~~~~

:term:`空值 <空值>` ``None`` 是独立的类型 ``NoneType``，表示"**这里暂时没有值**"——不是 0，也不是空字符串，而是"还没观测"。缺测记录、函数暂无返回值、初始化未定的变量，都用 ``None`` 占位：

.. code-block:: python

   precip = None                   # 降水缺测
   print(precip is None)           # True：判断空值一律用 is，不用 ==
   # ... 等仪器修复后补录
   precip = 0.0
   print(precip is None)           # False：0.0 是"观测到没下雨"，None 是"没观测"

.. note::

   数据处理中请始终区分 ``None``（未观测）与 ``0.0``（观测为零）——气象上这是两件完全不同的事，NumPy 里的 ``NaN`` 扮演的就是类似 ``None`` 的角色。

运算符
------

算术运算符
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 10 25 45

   * - 运算符
     - 含义
     - 气象示例
   * - ``+`` ``-`` ``*``
     - 加、减、乘
     - 日较差 ``temp_max - temp_min``
   * - ``/``
     - 除（结果必为 float）
     - 均温 ``sum(temps) / len(temps)``
   * - ``//``
     - 整除（向下取整）
     - 30 天观测折合 ``30 // 7`` 个整周
   * - ``%``
     - 取模（余数）
     - 风向角归一 ``(90 + 720) % 360`` → 90
   * - ``**``
     - 幂
     - 有效平方流速 ``u**2 + v**2``

.. code-block:: python

   temp_c = 37.5
   temp_f = temp_c * 9 / 5 + 32          # 摄氏转华氏
   print(temp_f)                         # 99.5

   wind_deg = 375                        # 仪器累积角度
   print(wind_deg % 360)                 # 15：规范到 [0, 360)

   total_hours = 730
   print(total_hours // 24, total_hours % 24)   # 30 天 10 小时

.. attention::

   ``/`` 永远返回 float，即使整除：``10 / 5 == 2.0``。要整型结果用 ``//``。

比较运算符
~~~~~~~~~~

``>`` ``<`` ``>=`` ``<=`` ``==`` ``!=``，返回布尔值。再次提醒：浮点数慎用 ``==``。

.. code-block:: python

   temp = 36.5
   print(temp > 35)         # True
   print(temp <= 35)        # False
   print(temp != 36.5)      # False

链式比较是 Python 的特色写法，读起来几乎像数学不等式：

.. code-block:: python

   temp = 18.3
   print(10 <= temp < 20)   # True：适宜温度区间，等价于 10 <= temp and temp < 20

逻辑运算符
~~~~~~~~~~

``and``（且）、``or``（或）、``not``（非）用来组合判据。气象预警常常就是一条逻辑表达式：

.. code-block:: python

   temp, humidity = 36.8, 55

   heatwave = temp >= 35 and humidity >= 50       # 高温高湿"桑拿天"
   night_heat = temp >= 28 or humidity >= 80      # 夜间闷热
   print(heatwave)        # True
   print(not heatwave)    # False

成员运算符
~~~~~~~~~~

``in`` / ``not in`` 判断元素是否在序列或字典中：

.. code-block:: python

   stations = ["兰州", "敦煌", "西宁"]
   print("兰州" in stations)          # True
   print("西安" not in stations)      # True

   station = {"name": "兰州", "temp": 25.6}
   print("temp" in station)           # True：对字典判断的是键

运算符优先级（常用速查）
~~~~~~~~~~~~~~~~~~~~~~~

从高到低：``**`` → 一元负号 → ``*`` ``/`` ``//`` ``%`` → ``+`` ``-`` → 比较运算 → ``not`` → ``and`` → ``or``。拿不准时**加括号**——括号不要钱，可读性值千金：

.. code-block:: python

   u, v = 3.0, 4.0
   speed = (u**2 + v**2) ** 0.5    # 风速 5.0，括号让意图一目了然
   print(speed)

.. _ch02-fstring:

提升拓展
--------

f-string 格式化进阶
~~~~~~~~~~~~~~~~~~~

f-string（格式化字符串字面量）是当前最主流的字符串拼接方式：字符串前加 ``f``，``{}`` 里既能放变量，也能放表达式。

.. code-block:: python

   station_id = 52889
   temp = 37.5
   print(f"站点 {station_id} 日最高气温 {temp} °C")
   print(f"折合华氏 {temp * 9 / 5 + 32} °F")     # {} 里可以写算式

``:`` 后跟**格式说明符**，是把数字变成规范报告的关键：

.. list-table::
   :header-rows: 1
   :widths: 15 30 40

   * - 写法
     - 含义
     - 示例输入 → 输出
   * - ``:.1f``
     - 保留 1 位小数
     - ``12.765`` → ``12.8``
   * - ``:+.1f``
     - 带正负号
     - ``0.5`` → ``+0.5``（距平常用）
   * - ``:.0%``
     - 百分数
     - ``0.456`` → ``46%``（相对湿度）
   * - ``:.2e``
     - 科学计数
     - ``12345.6`` → ``1.23e+04``
   * - ``:>8.2f``
     - 右对齐占 8 格
     - 对齐输出多站报表
   * - ``:08.2f``
     - 补零占 8 格
     - ``12.5`` → ``00012.50``（排序友好）

.. code-block:: python

   anomaly = 1.456            # 气温距平（°C）
   humidity = 0.456           # 相对湿度（小数）
   print(f"气温距平 {anomaly:+.1f} °C")     # 气温距平 +1.5 °C
   print(f"相对湿度 {humidity:.0%}")        # 相对湿度 46%

列表推导式初探
~~~~~~~~~~~~~~

处理列表数据时，"新建空列表 → for 循环 → append"是常见三步，列表推导式把三步压成一行：

**语法**：``[表达式 for 变量 in 可迭代对象 if 条件]`` —— 对每个元素，先过 ``if`` 关卡，通过者按 *表达式* 加工后收进新列表。

以整批摄氏温度转华氏为例（熟悉 Fortran 的同学可以类比 ``do`` 循环 + ``write``）：

.. code-block:: python

   celsius = [1, 2, 3, 4, 5, 6, 7, 8, 9]

   # 方法一：传统三步
   fahrenheit = []
   for c in celsius:
       f = c * 9 / 5 + 32
       fahrenheit.append(f)
   print(fahrenheit)

   # 方法二：列表推导式，一行等价
   fahrenheit = [c * 9 / 5 + 32 for c in celsius]
   print(fahrenheit)   # [33.8, 35.6, 37.4, 39.2, 41.0, 42.8, 44.6, 46.4, 48.2]

加 ``if`` 条件即可边遍历边筛选，比如挑出高温日：

.. code-block:: python

   temps = [33.0, 35.6, 34.2, 37.8, 29.9]
   high = [t for t in temps if t >= 35]
   print(high, len(high))    # [35.6, 37.8] 2

.. tip::

   建议一行不超过一个 ``for`` + 一个 ``if``；更复杂的逻辑老老实实写循环，可读性优先。学完第 3 章循环后再回头看这一节，会有更深的体会。

.. _ch02-bestpractice:

最佳实践：类型选择与单位标注
----------------------------

正文回答了"每种类型是什么"，这一节回答更实际的问题：**面对一个具体的气象量，该选哪种类型？数值和单位怎么标注才不会在三个月后坑到自己？** 以下规则来自一线数据处理的踩坑经验，建议当作团队代码规范执行。

气象量的类型选择速查表
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 24 12 26 38

   * - 气象量
     - 推荐类型
     - 示例
     - 理由
   * - 站名、省份
     - ``str``
     - ``name = "兰州"``
     - 文本，无需运算
   * - 区站号（无前导零）
     - ``int``
     - ``station_id = 52889``
     - 纯数字、不参与算术，排序自然
   * - 区站号（含前导零）
     - ``str``
     - ``station_id = "01001"``
     - ``int`` 会吃掉前导零
   * - 气温、气压、湿度、风速
     - ``float``
     - ``temp = 12.7``
     - 连续物理量，必须保留小数
   * - 经纬度、海拔
     - ``tuple``
     - ``(103.83, 36.06, 1517.2)``
     - 定位参数天然一组、不容篡改
   * - 逐日/逐时序列
     - ``list``
     - ``[5.1, 6.3, 4.8]``
     - 有序、需追加、需统计
   * - 一站多要素档案
     - ``dict``
     - ``{"temp": 25.6}``
     - 按要素名取值，见名知义
   * - 多站档案库
     - 嵌套 ``dict``
     - ``stations["52889"]["temp"]``
     - 外层站号、内层要素
   * - 天气现象、站名去重
     - ``set``
     - ``set(phenomena)``
     - 自动去重、支持交并差
   * - 是非判据
     - ``bool``
     - ``temp >= 35``
     - 直接用于 ``if``，语义清晰
   * - 缺测记录
     - ``None``
     - ``precip = None``
     - 区分"没观测"与"观测为零"

**三条铁律**：

#. **连续量永远用 float**。把 12.7 °C 存成 ``int`` 的 12，误差 0.7 °C——比多数观测仪器精度还大一个量级，日积月累会把气候统计悄悄带偏。
#. **成对出现且不允许中途修改的参数用 tuple**。坐标用列表存，等于给后续代码留了"随手改掉经度"的后门；元组则会在误改时立刻报错。
#. **"编号"类数字先问自己：会拿它做算术吗？** 不会（如站号、日期字符串 ``"2024-07-15"``）就倾向 ``str``；会（如年积温累加）才用数字类型。

单位标注三习惯
~~~~~~~~~~~~~~

气象数据相当一部分"神秘 bug"来自单位混乱：一份代码里同时混着 °C 与 K、hPa 与 Pa、m/s 与 km/h。养成三个习惯：

**习惯 1：变量名带单位后缀。**

.. code-block:: python

   temp_c = 25.6          # °C
   pressure_hpa = 848.6   # hPa
   wind_ms = 3.5          # m/s
   precip_mm = 12.4       # mm
   elev_m = 1517.2        # m

**习惯 2：转换动作集中在入口处。** 单位转换只做一次、写在读入处，绝不散落在各处计算中：

.. code-block:: python

   # 读入即统一：数据在项目内部永远用 °C
   temp_c = (temp_f - 32) * 5 / 9     # 入口转换
   dtemp = temp_c2 - temp_c1          # 之后全是纯 °C 运算

**习惯 3：输出与文档显式写单位。**

.. code-block:: python

   print(f"兰州站 7 月平均气温 {temp_c:.1f} °C")   # 数值旁必须有单位

字典/表格存元数据时，把单位写进键名，一眼可查：

.. code-block:: python

   station = {
       "name": "兰州",
       "temp_c": 25.6,
       "pressure_hpa": 848.6,
       "elev_m": 1517.2,
   }

命名与格式规范（PEP 8 摘要）
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 34 34

   * - 规则
     - 推荐
     - 不推荐
   * - 变量/函数：蛇形命名
     - ``temp_max``, ``wind_speed``
     - ``TempMax``, ``tempmax``
   * - 常量：全大写
     - ``FREEZING_POINT_C = 0.0``
     - ``freezingPoint``
   * - 见名知义
     - ``temp_min_2024``
     - ``t1``, ``data2``
   * - 布尔值用 is/has 开头
     - ``is_heatwave``, ``has_precip``
     - ``flag1``
   * - 禁止覆盖内置名
     - ``station_list``
     - ``list = [...]``

类型转换检查清单
~~~~~~~~~~~~~~~~

- 转换前先想清楚**方向与合法性**：``int("25")`` ✓、``int("25.6")`` ✗（须先 ``float``）、``float("12.7")`` ✓；
- ``str → number`` 随时可能抛 ``ValueError``，读外部数据（CSV、键盘输入）时用 ``try/except`` 兜底（第 3 章后可回头实践）；
- ``float → int`` 是**截断**不是四舍五入：``int(25.9)`` 得 ``25``；要四舍五入用 ``round(25.9)``；
- 显示与计算分离：**计算用原值，显示才格式化**——``f"{avg:.1f}"`` 只影响打印，别提前 ``round`` 破坏精度。

常见反模式（反面教材）
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # 反模式 1：温度用 int，精度蒸发
   temp = 12                 # ✗ 12.7 °C 被截成 12
   temp = 12.7               # ✓

   # 反模式 2：坐标用 list，埋下误改隐患
   location = [103.83, 36.06]          # ✗ 任何代码都能 location[0] = 999
   location = (103.83, 36.06)          # ✓ 元组防误改，且可作字典键

   # 反模式 3：变量名不带单位，换算 bug 找三天
   pressure = 848.6          # ✗ hPa 还是 Pa？
   pressure_hpa = 848.6      # ✓

   # 反模式 4：缺测用 999 填充再忘掉
   temp = 999                # ✗ 气象惯例的缺测码 999 会混进 max() 统计
   temp = None               # ✓ 缺测显式化；进阶章节用 np.nan

   # 反模式 5：浮点直接判等
   if temp_avg == 25.0:      # ✗ 0.1 + 0.2 != 0.3 的远房亲戚
       ...
   if abs(temp_avg - 25.0) < 1e-6:   # ✓ 容差比较
       ...

.. tip::

   **一句话总结**：类型选对（float 管连续量、tuple 管定位、dict 管档案）、单位进名字（``temp_c``）、缺测交给 ``None``——做到这三条，你的气象代码就有了职业素养的底子。

贯穿项目 · 第 2 步：存储兰州站元信息
------------------------------------

把本章知识点组装起来，完成 ``weather_project/notebooks/ch02_types.py``：

.. code-block:: python

   """ch02_types.py —— 贯穿项目第 2 步：用基本类型存储兰州站信息"""

   # —— 站点元信息 ——
   station_name = "兰州"                     # str：站名
   station_id = 52889                        # int：区站号
   location = (103.83, 36.06, 1517.2)        # tuple：(经度, 纬度, 海拔 m)
   lon, lat, elev = location                 # 解包

   # —— 近三日气温（°C）——
   temp_max_list = [12.6, 13.4, 11.9]
   temp_min_list = [1.4, 2.2, 0.8]

   # —— 档案与统计 ——
   station = {
       "station_id": station_id,
       "name": station_name,
       "lon": lon,
       "lat": lat,
       "elevation": elev,
   }
   avg_max = sum(temp_max_list) / len(temp_max_list)
   avg_min = sum(temp_min_list) / len(temp_min_list)
   station["temp_max_avg"] = avg_max         # 动态写入统计结果
   station["temp_min_avg"] = avg_min

   # —— 输出观测报告 ——
   print(f"站点：{station_name}（{station_id}）")
   print(f"位置：{lon:.2f}°E, {lat:.2f}°N, 海拔 {elev:.1f} m")
   print(f"近三日平均最高气温：{avg_max:.1f} °C，平均最低气温：{avg_min:.1f} °C")

输出：

.. code-block:: text

   站点：兰州（52889）
   位置：103.83°E, 36.06°N, 海拔 1517.2 m
   近三日平均最高气温：12.6 °C，平均最低气温：1.5 °C

**验收标准**：脚本输出站名、站号、经纬度、海拔与三日均温，数值格式正确（保留 1 位小数）。可运行版本见 :doc:`/gallery/plot_basics/plot_datatypes`。

本章小结
--------

.. list-table::
   :header-rows: 1
   :widths: 14 24 8 8 46

   * - 类型
     - 字面量
     - 有序
     - 可变
     - 典型气象用途
   * - ``int``
     - ``52889``
     - —
     - ✗
     - 站号、年份、时次
   * - ``float``
     - ``1517.2``
     - —
     - ✗
     - 气温、气压、经纬度、海拔
   * - ``str``
     - ``"兰州"``
     - ✓
     - ✗
     - 站名、天气现象、日期文本
   * - ``list``
     - ``[32.6, 34.1]``
     - ✓
     - ✓
     - 逐日气温序列、站名清单
   * - ``tuple``
     - ``(103.83, 36.06)``
     - ✓
     - ✗
     - 坐标、不可变的标定参数
   * - ``dict``
     - ``{"temp": 25.6}``
     - 按键取
     - ✓
     - 站点档案、多要素元数据
   * - ``set``
     - ``{"晴", "多云"}``
     - ✗
     - ✓
     - 天气现象去重、站点集合运算
   * - ``bool``
     - ``True``
     - —
     - ✗
     - 高温/暴雨判据
   * - ``NoneType``
     - ``None``
     - —
     - ✗
     - 缺测占位、无返回值

.. seealso::

   - 术语详解：:doc:`/api/ch02_terms` —— 每个名词的生活类比与易混淆点；
   - 动手练习：:doc:`/tutorials/ch02_practice` —— 5 道西北站点实战题（含提示与参考答案）；
   - 可执行示例：:doc:`/gallery/plot_basics/plot_datatypes` —— 用基本类型存储站点信息并绘图。
