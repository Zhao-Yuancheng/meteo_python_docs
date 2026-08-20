.. _tut-oop:

面向对象与高级语法
==================

第 5 节 · 模块一 Python 编程基础
贯穿项目第 5 步：设计 ``Station`` 类，封装站点信息与气温记录，支持均值/极值统计。

Python 编程可以粗略分为两种思路：**面向过程** 与 **面向对象**。前面各章讲的变量、列表、循环、函数，都是面向过程的写法——它把任务拆成一串"步骤"，用函数做最小单元，数据和处理数据的函数彼此分开，适合小脚本。而\ **面向对象（OOP）**\聚焦"事物（对象）"，把描述事物的数据（属性）和操作数据的功能（方法）整合成一个整体，代码高内聚、低耦合，是现代大型项目、框架和工具库的主流范式。

本课程的目标是：掌握 Python 类与对象、封装、继承等核心语法，能独立设计业务类，并结合文件读写完成气象数据统计的综合案例。需要说明的是，面向对象并非 Python 的必用语法——小工具脚本只用面向过程也完全没问题；但爬虫、数据分析系统、Web 项目、大型工具库几乎都优先采用面向对象，因为它的代码复用性强、更易维护。

请带着一个贯穿始终的比喻来读本章：**气象站就是一座"对象"**。它有区站号、经纬度、海拔这些"属性"，也能"做事"——记录气温、算平均、算极值。把气象站抽象成类，正是本章做的大事情。

下面按「基础概念 → 类定义 → 属性与方法（封装）→ 继承复用 → 模块中的类 → 综合实战 → 小结拓展」的顺序层层推进。

5.1 初识面向对象
----------------

.. note::

   本章标题虽为"面向对象与高级语法"，但装饰器、生成器等高级语法是建立在对"类与对象"的直觉之上的。把 5.1 的气象比喻读透，后面的 @property、装饰器都会顺理成章。

**面向过程与面向对象的思想对比**

- **面向过程**：聚焦"步骤"，按照执行顺序拆分代码，以函数为最小单元；数据和操作数据的函数相互分离。
- **面向对象**：聚焦"事物（对象）"，将描述事物的数据（属性）与操作数据的功能（方法）整合为整体。

**Python 核心特性：一切皆对象**。数字、字符串、列表、字典，甚至函数本身，全部是对象，每个对象都属于某个类。例如数字 ``5`` 属于 ``int`` 类，列表 ``[]`` 属于 ``list`` 类。对象有两大固定组成部分：

- **属性（attribute）**：描述对象状态、特征的数据；
- **方法（method）**：对象自带、用于修改 / 查询自身属性的函数。

**类与实例的逻辑关系**

- **类（Class）**：对象的通用模板，定义一类事物统一拥有的属性类别与可用方法；
- **实例（Instance）**：根据类模板创建出的具体个体，同一个类可以生成无数实例；
- **共性与差异**：同一类的所有实例拥有相同结构的属性、相同方法，但每个实例的属性值相互独立。

**生活化案例：把气象站拆成"学生小明"模型**

以"小明，12 岁学生，存款 1000 元"为例，对应面向对象封装中公有、私有成员的概念：

- **公有属性**\（外部可直接访问）：姓名（小明）、年龄（12）；
- **私有属性**\（外部无法直接查询、修改）：存款（1000 元，他人不能随便查看）；
- **公有方法**\（外部可主动调用）：写作业（对外公开的行为）、洗碗（每洗一个碗存款加 10 元，外部可以安排他洗碗）；
- **私有方法**\（仅对象内部可调用，对外隐藏）：珠心算（小明仅写作业时内部使用，不在外人面前展示）。

抽象成类就是：``Student``\（学生类）定义所有学生统一具备的姓名、年龄、存款属性，以及写作业、洗碗、珠心算三种方法。它对应到气象界，就像定义"台站说明书"``Station``，规定所有站都有的区站号、经纬度、海拔和通用统计方法——这是图纸，不是某一座真站。

**Python 的两类对象：类对象、实例对象**

- **类对象**：执行 ``class`` 定义语句时自动生成，全局仅存在唯一一个；存放类顶层共享的属性与全部方法函数。访问用 ``类名.属性``、``类名.方法``，而方法调用的 ``self`` 参数存在限制（见 5.3）。
- **实例对象**：调用类名（类似 ``类名()``）创建，可创建任意多个；每个实例有独立命名空间，存放仅属于自己的实例属性；所有实例共享类对象中的方法，并不单独复制，从而省内存。

命名空间规则也很关键：类对象与每个实例对象各自拥有独立命名空间，修改某实例自身的属性，不会影响类和其他实例。

**Python 面向对象语言的独有特性**

- 类拥有独立命名空间，变量、方法仅在类内部生效；
- 原生支持单继承与多重继承，实现代码复用；
- 支持运算符重载，自定义类对象可直接使用加、减、乘、除等运算符；
- Python 3 中所有类都是 ``type`` 类的实例，统一采用新式类规范；
- 与 C++/Java 不同，Python 没有严格的编译期访问控制，仅靠双下划线实现"伪私有"，无强制语法级私有隔离。

5.2 定义和使用类
----------------

**类的基础定义语法**。用 ``class`` 关键字定义类：

.. code-block:: python

   class 类名:
       # 类共享属性
       变量 = 值
       # 定义实例方法
       def 方法名(self, 参数):
           方法逻辑

**类内语句的执行规则**

- 类内顶层赋值语句生成类共享属性；``def`` 语句定义类的方法；
- ``class`` 是可执行语句：在交互模式或导入模块时，会自动执行类内顶层代码（比如类内直接写 ``print`` 会在定义类那一刻打印出来）；
- 语句顺序没有强制约束，属性与方法定义先后不影响类的使用。

**类对象的基础操作与限制**

- **访问类共享属性**：直接用 ``类名.属性名`` 读写，修改后所有实例读取该类属性都会同步变化；
- **类方法调用限制**：类对象无法直接调用带 ``self`` 的实例方法；``self`` 需要在调用时传入一个实例对象作为第一个参数，只有通过实例调用时 Python 才会自动填充。

**实例对象的创建与操作**

- **实例化语法**：``实例变量 = 类名()``，每执行一次生成全新独立实例；
- **调用方法的底层逻辑**：调用 ``实例.方法()`` 时，Python 自动把当前实例作为第一个实参传给方法的 ``self`` 形参；不同实例调用同一方法，``self`` 分别指向各自对象，属性互不干扰。

下面用一个可交互的完整例子体会"多实例隔离"。定义 ``testclass``，含类共享属性 ``data=100`` 与两个实例方法：

.. code-block:: python

   class testclass:
       data = 100                      # 类共享属性
       def setpdata(self, value):      # 给当前实例写入价格
           self.price = value
       def showpdata(self):            # 显示当前实例的价格
           print("price =", self.price)
       print("类 testclass 加载完成！")  # 定义类时立即执行

在这里，"类 testclass 加载完成！"会在定义类的那一行被执行并打印——这正是"类是可执行语句"的直观体现。接着分别用 ``x``、``y`` 两个实例赋值：

.. code-block:: python

   x = testclass()        # 创建实例 x
   x.setpdata(120)        # 给 x 写入 price=120
   y = testclass()        # 创建实例 y
   y.setpdata(90)         # 给 y 写入 price=90
   x.showpdata()          # price = 120：x 的属性
   y.showpdata()          # price = 90：y 的属性，互不干扰

输出 ``price = 120`` 与 ``price = 90``，说明两个实例的私有属性相互隔离，印证了"各实例拥有独立命名空间"。

5.3 对象的属性和方法（封装）
----------------------------

本节是封装的\ **核心章节**。我们仍然站在"气象站"的立场上，把类内部的数据与行为打理清楚。

**对象属性的分类、特性与访问规则**

- **类共享属性**：定义在 ``class`` 顶层直接赋值；所有实例、类对象共用同一份数据。修改差异很关键：``类名.属性 = 值`` 会对所有实例全局更新；而 ``实例.属性 = 值`` 只会在\ **当前实例**\新建同名属性，此后该实例不再读取类共享属性。
- **实例私有属性**：只能在类内部方法中通过 ``self.属性名 = 值`` 生成；实例刚创建时为空，只有调用方法赋值后才生成对应属性；仅当前实例可见，其他实例无法读取、修改。
- **属性动态创建特性**：Python 变量赋值即创建，类与实例都支持运行时动态新增属性——``类名.新属性 = 值`` 给类新增共享属性，``实例.新属性 = 值`` 给单个实例新增私有属性。可传入 ``dir()`` 查看类/实例的全部内置与自定义属性、方法，用于调试对象结构。

**对象方法的底层运行原理**。所有方法统一保存在类对象中，实例不会复制方法，仅通过引用调用，节约内存。

``self`` 参数深度解析：``self`` 只是约定俗成的名字，可以换成任意单词（``this``、``obj`` 等），核心在于它是\ **第一个形参**\的位置；作用是在方法内部代表调用该方法的实例对象，用于读写自身属性。

对比"有无 self"的区别：

- **无 ``self`` 的普通函数**：只能在类里当普通函数，仅能通过类名手动传参调用，用实例调用会报错；
- **带 ``self`` 的实例方法**：实例调用时自动填充 ``self``，是开发中的标准写法。

**Python 的伪私有机制（封装手段）**。属性 / 方法名以双下划线 ``__`` 开头即为"私有"，例如 ``__data2``、``__sub()``。在类外部直接写 ``类名.__属性``、``实例.__方法()`` 会触发 ``AttributeError``，提示不存在该属性。但它的本质并非语法级加密：Python 底层会自动把名称改写为 ``_类名__属性``，只是阻止常规的直接访问，属开发层面的隐藏规范。

**内置特殊魔法方法：构造函数、析构函数**

- **构造函数 ``__init__``**：实例化 ``类名(参数)`` 时自动触发，无需手动调用；核心作用是把实例属性初始化——例如把兰州站（区站号 52889）的站名、经纬度、海拔在创建对象时一次性写入；传入的参数会全部传递给 ``__init__`` 中除 ``self`` 以外的形参。
- **析构函数 ``__del__``**：实例被删除、程序结束内存回收时自动调用；适合关闭文件、释放连接等资源收尾操作；但无法精确控制执行时间，不适合强依赖它的释放逻辑。

下面是一个带 ``__init__`` 与 ``__del__`` 的演示类，实例化、赋值、删除对象时，两段打印会依次自动触发：

.. code-block:: python

   class Data:
       def __init__(self, value):
           self.value = value
           print("构造实例，value =", self.value)
       def __del__(self):
           print("析构实例，value =", getattr(self, "value", None))

   d = Data(42)    # 构造实例，value = 42
   del d           # 析构实例，value = 42

**@property 属性装饰器（封装数据、优雅取值）**

它的作用是把"由其它数据推算出的结果"伪装成普通属性来读取。外部只需写 ``实例.属性名`` 即可取到由方法计算的数值，不必加括号，又保护了内部求值逻辑。气象示例：给 ``Station`` 类加一个 ``@property`` 属性 ``mean_temp``，返回该站近期逐日气温序列的平均值。调用方写 ``zhou_station.mean_temp`` 即可，像读普通字段一样直观，而求平均的过程被隐藏在方法内部。

``@property`` 默认只读；配合 ``@xxx.setter`` 可在赋值时做校验。例如气温不能低于绝对零度 ``-273.15℃``，否则抛出 ``ValueError`` 拒绝非法气象记录：

.. code-block:: python

   class Station:
       def __init__(self, name, temps=None):
           self.name = name
           self._temps = temps if temps is not None else []

       @property
       def mean_temp(self):                     # 只读：像字段一样读
           return sum(self._temps) / len(self._temps) if self._temps else None

       @property
       def temperature(self):
           return self._temperature

       @temperature.setter
       def temperature(self, value):            # 赋值时校验
           if value < -273.15:
               raise ValueError("气温不能低于绝对零度 -273.15℃")
           self._temperature = value

5.4 类的继承
------------

**继承基础概念与语法**。

- **父类 / 超类（super class）**：被继承的原有类，包含通用属性、通用方法；
- **子类 / 派生类（sub class / derived class）**：继承父类生成的新类，复用父类代码并扩展自有功能。

继承的核心价值在于：无须重复编写通用代码，子类直接拥有父类全部公有属性、公有方法，降低冗余、便于统一维护。气象场景举例：父类 ``Station`` 负责站点基础信息（区站号、经纬度、海拔），子类 ``AutoStation`` 只需额外补写气温、湿度、气压，不必把父类属性重新写一遍。

**单继承标准语法**：

.. code-block:: python

   class 子类名(父类名):
       pass  # 空实现，完整继承父类所有内容

空继承案例里，定义父类 ``supper_class``\（含共享属性、普通方法、私有方法），再定义空子类 ``sub_class``，会发现子类实例可直接调用父类公有成员，而私有成员依旧无法外部访问。

**子类扩展、属性与方法重写**

- **新增自有内容**：子类内可定义全新的实例属性、全新方法，仅属于子类，父类无法使用；
- **同名重写覆盖**：若子类定义了与父类同名的属性 / 方法，子类实例优先使用子类自身定义，屏蔽父类同名成员；
- **主动调用父类方法**：重写后若想复用父类原有逻辑，用 ``父类名.方法(self)`` 手动调用，同时保留子类新增逻辑。

**子类构造函数调用父类构造函数**

- 默认规则：子类自定义 ``__init__`` 后，不会自动执行父类构造函数，父类属性无法自动初始化；
- 手动调用语法：在子类 ``__init__`` 内部执行 ``父类名.__init__(self, 所需参数)``；
- 案例：父类构造初始化 ``supper_data``，子类构造新增 ``sub_data``，同时调用父类构造完成全部属性初始化。

**多重继承**。语法为 ``class 子类(父类1, 父类2):``。当多个父类存在同名属性/方法时，Python 按子类定义括号内从左到右的顺序查找，找到第一个匹配项即停止。实操里定义 ``supper1``、``supper2`` 两个父类，都存在同名 ``show2`` 方法；子类同时继承两者，调用 ``show2`` 时优先执行左侧第一个父类的逻辑。

下面用继承把"普通站"升级为"自动站"：

.. code-block:: python

   class Station:
       def __init__(self, station_id, name, lat, lon, altitude):
           self.station_id = station_id
           self.name = name
           self.lat = lat
           self.lon = lon
           self.altitude = altitude
       def info(self):
           return f"{self.station_id} {self.name}"

   class AutoStation(Station):          # 继承父类
       def __init__(self, station_id, name, lat, lon, altitude,
                    temperature, humidity, pressure):
           super().__init__(station_id, name, lat, lon, altitude)  # 先调父类
           self.temperature = temperature
           self.humidity = humidity
           self.pressure = pressure
       def info(self):                  # 重写，先取父类再补内容
           return f"{super().info()} | {self.temperature}℃ {self.humidity}%"

   shanghai = AutoStation("58362", "上海", 31.40, 121.47, 6, 33.5, 78, 1008.1)
   print(shanghai.info())   # 58362 上海 | 33.5℃ 78%

``AutoStation`` 自动继承了 ``Station`` 的区站号、经纬度、海拔与 ``info()``，只需补写 ``temperature``、``humidity``、``pressure``——这正是典型的"站与自动站"继承关系，也是同名方法重写（多态）的雏形。

5.5 模块中的类
--------------

**在独立模块文件中定义类**。规范做法是把 ``class`` 写进单独的 ``.py`` 文件（如 ``classlib.py``）。模块自测代码使用 ``if __name__ == '__main__':`` 分支，仅当文件被单独运行时才执行测试代码，被 ``import`` 时不执行。案例：``classlib.py`` 中定义 ``test`` 类，内置 ``set``、``show`` 方法，自测代码创建实例并打印属性——代码结构如下。

.. code-block:: python

   # classlib.py
   class test:
       def __init__(self):
           self.value = 0
       def set(self, v):
           self.value = v
       def show(self):
           print("value =", self.value)

   if __name__ == '__main__':
       t = test()
       t.set(7)
       t.show()            # 仅直接运行 classlib.py 时才执行

**两种导入类的方式与区别**

- ``import 模块名``：使用时必须前缀模块名 ``模块名.类名``，适合模块内存在多个类的场景：

.. code-block:: python

   import classlib
   obj = classlib.test()        # 前缀模块名
   obj.set(1); obj.show()

- ``from 模块名 import 类名``：直接使用类名实例化，代码更简洁，适合只使用单一类的场景：

.. code-block:: python

   from classlib import test
   obj = test()                 # 直接用类名
   obj.set(2); obj.show()

两种方式均可对模块中的类做属性读写与方法调用，选择取决于你的代码组织习惯与模块内类的数量。

5.6 综合实战：MeteoStation 气象类
----------------------------------

前面五节把概念讲透了，这一节动真格：用面向对象封装一个能读 CSV、能统计的气象类。

**业务需求**：封装一个 ``MeteoStation`` 类，它读取兰州站 2024 年逐日气温 CSV，实现按月筛选气温序列、计算月平均气温、月最高温、月最低温，并返回站点基础信息。

**CSV 数据文件字段解析**：文件含 ``date, year, month, day, temp`` 五个字段，分别代表日期、年、月、日、气温。

**MeteoStation 类的结构设计**

- 构造函数 ``__init__(self, csv_file_path)``：接收 CSV 文件路径，内部读取 CSV，把全部逐日数据存入实例属性；
- ``get_month_data(self, target_month)``：根据传入月份，筛选返回该月全部气温列表；
- ``calc_month_mean(self, target_month)``：计算指定月份平均气温；
- ``calc_month_max(self, target_month)``：计算指定月份最高气温；
- ``calc_month_min(self, target_month)``：计算指定月份最低气温。

完整实现如下——它以真实的气象文件读写为骨架，把"数据 + 统计行为"一并封装进了类：

.. code-block:: python

   import csv

   class MeteoStation:
       def __init__(self, csv_file_path):
           # 读取 csv，全部逐日数据存入 self.data
           self.data = []
           with open(csv_file_path, encoding="utf-8") as f:
               for row in csv.DictReader(f):
                   self.data.append({
                       "date": row["date"], "year": int(row["year"]),
                       "month": int(row["month"]), "day": int(row["day"]),
                       "temp": float(row["temp"]),
                   })

       def get_month_data(self, target_month):
           # 筛选指定月份所有气温
           return [d["temp"] for d in self.data if d["month"] == target_month]

       def calc_month_mean(self, target_month):
           temps = self.get_month_data(target_month)
           return sum(temps) / len(temps)

       def calc_month_max(self, target_month):
           return max(self.get_month_data(target_month))

       def calc_month_min(self, target_month):
           return min(self.get_month_data(target_month))

   # 主程序测试：假定文件"兰州站2024年逐日气温.csv"已就位
   station = MeteoStation("兰州站2024年逐日气温.csv")
   print("7 月平均气温:", station.calc_month_mean(7))
   print("7 月最高气温:", station.calc_month_max(7))
   print("7 月最低气温:", station.calc_month_min(7))

一句话，``MeteoStation`` 把"从哪里读、怎么算、算什么"全部包进类，外部只需创建对象、选月份、拿结果——这就是面向对象在气象工程实践里的真实价值。

**让对象打印出来一眼可读：``__repr__``**。默认 ``print(station)`` 输出的是 ``<__main__.MeteoStation object at 0x...>``，一串地址对查数据没有帮助。给类补一个 ``__repr__``，返回构造该对象所需的关键字段，打印和排错都会舒适很多：

.. code-block:: python

   class MeteoStation:
       def __init__(self, csv_file_path):
           self.csv_file_path = csv_file_path
           self.data = []
           # ……读取 csv，填充 self.data……

       def __repr__(self):
           return f"MeteoStation(csv={self.csv_file_path!r}, 记录数={len(self.data)})"

   station = MeteoStation("兰州站2024年逐日气温.csv")
   print(station)                    # MeteoStation(csv='兰州站2024年逐日气温.csv', 记录数=365)
   print([station])                  # 容器里的元素也走 __repr__

``print(对象)`` 先找 ``__str__``，没有才退到 ``__repr__``；而列表等容器里的元素\ **一定走 ``__repr__``**。所以只写 ``__str__`` 时，``print([station])`` 仍是地址。``!r`` 让字符串带引号；``__repr__`` 里不要跑可能失败的统计（比如 ``mean_temp`` 是 ``None``），只放身份字段即可。

**（选做）继承实现格点数据子类**：利用继承机制，让父类 ``MeteoStation`` 实现通用统计逻辑，再写子类 ``NetCDFMeteo(MeteoStation)``：① 子类重写数据读取方法，读取 NetCDF 格点气温数据；② 复用父类 ``calc_month_mean`` / ``calc_month_max`` / ``calc_month_min`` 统计方法；③ 新增子类独有的方法 ``get_latlon_subset()`` 完成经纬度区域裁剪。无论数据源是逐日 CSV 还是格点 NetCDF，统一的统计接口不变——这是继承与多态最优雅的体现。

5.7 课程小结与拓展
------------------

**核心知识点梳理**

- **封装**：类整合属性与方法、公有私有成员、构造 / 析构函数；
- **继承**：单继承、多重继承、方法重写、父类构造调用；
- **基础使用**：类定义、实例化、``self`` 参数、动态属性、模块导入类；
- **气象工程实践**：使用面向对象封装 CSV、NetCDF 气象数据的读写与统计。

**高频易错点汇总**

1. 混淆类共享属性与实例私有属性，修改类属性后预期效果不符；
2. 定义实例方法遗漏 ``self`` 第一个参数，调用时报错；
3. 子类重写 ``__init__`` 后忘记调用父类构造，缺失父类属性；
4. 混淆私有成员访问规则，在外部直接使用 ``__属性名`` 访问；
5. 分不清类对象、实例对象的命名空间隔离关系；
6. 处理文件时忘记在析构函数里关闭 CSV、NetCDF 句柄，造成资源泄露。

**拓展学习方向**

- Sphinx 补充语法：装饰器、生成器、列表推导式进阶、``match-case`` 语法；
- OOP 进阶：``@property`` 属性装饰器、运算符重载、类方法 ``@classmethod``、静态方法 ``@staticmethod``；
- 气象开发：基于类封装批量气象文件处理（如一次性统计西北 8 站逐日气温并输出表格），开发面向对象的数据分析脚本。

至此，"把气象站抽象成类"的整条主线走完了——从一张"台站说明书"（类），到一座座活灵活现的真站（实例），再到站与自动站的继承接力。拿到配套练习，把 ``Station``、``AutoStation``、``MeteoStation`` 亲手实现一遍，本章就稳了。

.. seealso:: 配套练习：:doc:`/tutorials/basics/ch05_practice`　·　术语参考：:doc:`/api/ch05_terms`　·　示例画廊 :doc:`/gallery/plot_basics/index`