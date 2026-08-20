第 5 章术语：面向对象与高级语法
===============================

配套 :ref:`tut-oop` 正文使用。每个词条 = 一句话定义 + **生活类比** + **气象示例** + **易混淆点**\（`.. code-block:: python` 承载代码示例）。本章术语围绕"把气象站抽象成类"展开。

.. seealso:: 配套正文：:doc:`/user_guide/basics/oop`　·　配套练习：:doc:`/tutorials/basics/ch05_practice`

.. glossary::

   类（Class）
      对象的模板，定义一组对象共有的属性与方法，是一张抽象的设计图纸；类本身不占具体"实物"，只描述"应该长什么样、会做什么"。

      **生活类比** —— 汽车设计图纸：规定车子有车轮、颜色、行驶功能，但图纸本身不是真车。

      .. code-block:: python

         class Station:
             def __init__(self, station_id, name, lat, lon):
                 self.station_id = station_id
                 self.name = name
                 self.lat, self.lon = lat, lon
             def info(self):
                 return f"{self.name}站（区站号 {self.station_id}）"

      **易混淆点** —— 类（图纸）≠ 实例（真车）。``Station`` 类只是"台站说明书"，不会自己算气温；必须先 ``类名()`` 造出一座具体的站，才能读写与统计。

   对象 / 实例（Object / Instance）
      依据类创建出来的具体实体，称为实例（对象），在内存中占有一块真实的存储空间。

      **生活类比** —— 按照图纸造出来的一台真实汽车：图纸是类，这台实物汽车就是实例。

      .. code-block:: python

         lz = Station("52889", "兰州", 36.05, 103.88)
         print(lz.info())          # 兰州站（区站号 52889）

      **易混淆点** —— ``lz`` 是真真切切的兰州站对象，可读取、可统计；而 ``Station`` 本身仍然只是"图纸"。

   属性（Attribute）
      类 / 实例身上存储的数据变量，描述对象的特征，反映对象的"状态"。

      **生活类比** —— 汽车的颜色、车牌号、行驶里程，属于这辆车的特征信息。

      .. code-block:: python

         lz.station_id = "52889"   # 区站号
         lz.lat = 36.05
         lz.lon = 103.88
         lz.altitude = 1517        # 海拔 / m

      **易混淆点** —— 属性描述"它是什么样"，方法描述"它能做什么"。``lz.name`` 是属性（站名），``lz.info()`` 是方法（要加括号调用）。

   方法（Method）
      写在类内部的函数，用来描述对象可以执行的行为动作；调用时 Python 会自动传入 ``self`` 指向当前实例。

      **生活类比** —— 汽车的刹车、加速、开灯，是汽车可以完成的动作。

      .. code-block:: python

         lz.record(31.6)            # 记录一次气温
         print(lz.calc_mean(7))     # 算出 7 月平均气温

      **易混淆点** —— 方法调用要加括号 ``info()``，属性访问不加括号 ``name``；实例方法的第一个参数必须是 ``self``，漏写是最常见报错之一。

   构造函数 __init__
      实例创建时自动调用的特殊方法，用来初始化实例的属性；名字固定为 ``__init__``，且第一个参数必须是 ``self``。

      **生活类比** —— 新车出厂装配流程：造车的时候给它装好颜色、轮胎等初始配置。

      .. code-block:: python

         class Station:
             def __init__(self, station_id, name, lat, lon, altitude):
                 self.station_id = station_id
                 self.name = name
                 self.lat, self.lon = lat, lon
                 self.altitude = altitude

         lz = Station("52889", "兰州", 36.05, 103.88, 1517)  # "出生"即带全部信息

      **易混淆点** —— ``__init__`` 由 ``类名(参数)`` 自动触发，不能手动 ``lz.__init__(...)``；它只做初始化，不负责"返回创建好的对象"。

   继承（Inheritance）
      子类复用父类的属性与方法，还可以扩展属于自己的新功能，实现代码复用；同名改写时以子类内容为优先。

      **生活类比** —— 普通轿车图纸（父类）→ 电动轿车图纸（子类）：继承轿车全部功能，新增充电功能。

      .. code-block:: python

         class AutoStation(Station):              # 继承父类 Station
             def __init__(self, *args, temperature=0.0, humidity=0.0, pressure=0.0):
                 super().__init__(*args)          # 先初始化父类属性
                 self.temperature = temperature
                 self.humidity = humidity
                 self.pressure = pressure

      **易混淆点** —— 子类重写 ``__init__`` 后，父类构造函数不会自动执行，须显式调用 ``super().__init__(...)``，否则父类属性缺失。

   封装（Encapsulation）
      把数据和操作数据的方法打包到类内，对外隐藏内部细节，只暴露可供调用的接口（公有成员）。

      **生活类比** —— 开车只需踩油门握方向盘，不用关心发动机内部齿轮如何运转。

      .. code-block:: python

         mean = station.calc_month_mean(7)        # 对外只需这一个接口
         # 内部究竟是遍历逐日数据还是查表，被封装在类里，外部不可见也不可篡改

      **易混淆点** —— Python 的"私有"只是约定（双下划线 ``__`` 名称改写为 ``_类名__属性``），并非语法级强制隔离；封装是设计规范，不是安全机制。

   多态（Polymorphism）
      不同子类重写同一个方法，调用同一个方法名，不同对象会表现出不同行为——同一接口，多种实现。

      **生活类比** —— 同样"鸣叫"这个动作：狗对象执行"汪汪叫"，猫对象执行"喵喵叫"。

      .. code-block:: python

         class AutoStation(Station):
             def info(self):                      # 重写父类 info()
                 return f"{super().info()} | {self.temperature}℃ {self.humidity}%"

         print(Station("54511", "北京", 39.8, 116.47).info())   # 普通站：只有基础信息
         print(shanghai.info())                                  # 自动站：多出气象要素

      **易混淆点** —— 多态靠"同名重写 + 运行时绑定"实现：调用方只认方法名 ``info()``，具体输出由对象的实际类型决定。

   装饰器（Decorator）
      在不修改原函数代码的前提下，用 ``@`` 语法包装、增强函数功能的一种工具；本质是"接收函数、返回新函数"的高阶函数。

      **生活类比** —— 给手机套手机壳：不改变手机本身，额外增加防摔保护功能。

      .. code-block:: python

         def log_record(func):
             def wrapper(temperature):
                 print("开始记录气温")
                 result = func(temperature)
                 print(f"已记录 {temperature}℃")
                 return result
             return wrapper

         @log_record
         def record_temperature(temperature):
             print("写入:", temperature)

         record_temperature(31.6)

      **易混淆点** —— 装饰器只是"包装层"，不会丢失原函数的行为；务必在 ``wrapper`` 里 ``return func(...)`` 的返回值，否则原函数的返回会被吞掉。

   生成器（Generator）
      使用 ``yield`` 惰性逐个产出数据的函数；调用生成器函数得到的是生成器对象，用 ``for`` 遍历时逐个取出，不会一次性把全部数据载入内存。

      **生活类比** —— 饮水机接水：需要一杯接一杯出水，而不是一次性把整桶水全部倒出来。

      .. code-block:: python

         def temp_seq(records):
             for hour, temperature in records:
                 yield hour, temperature          # 惰性逐个产出

         for hour, temperature in temp_seq([(8, 21.6), (14, 31.6)]):
             print(hour, temperature)

      **易混淆点** —— 含 ``yield`` 的函数是"生成器函数"，调用即返回生成器对象，函数体并不立即执行；用 ``return`` 直接返回列表会立刻占用全部内存，违背惰性初衷。