第 5 章练习：面向对象与高级语法
==============================

配套 :ref:`tut-oop` 正文。第 1–3 题为入门题，第 4–5 题为提升题。试题中的台站均为西北地区真实气象站，其中兰州站区站号为 ``52889``，是大家最熟悉的家乡站点。数据以表格形式列于题中，可直接按表中数值构造对象，无需额外文件。

.. seealso:: 配套正文：:doc:`/user_guide/basics/oop`　·　术语参考：:doc:`/api/ch05_terms`

💡 **通用提示**：实例方法的第一参数必须为 ``self``，漏写后一经调用即报 ``TypeError``——这是第 5 章新手最高频的报错之一。属性名一律采用小写字母加下划线，不得写成 ``StationID``，亦不得写成 ``station-id``。

入门题
------

第 1 题（设计 Station 类）
^^^^^^^^^^^^^^^^^^^^^^^^^^

已知若干地面气象站的区站号、站名、纬度、经度及海拔如下表。试编写程序，完成下列各问。

（1）定义类 ``Station``，用以表示一座地面气象站。

（2）构造方法为 ``__init__(self, station_id, name, lat, lon, altitude)``，分别保存区站号、站名、纬度、经度、海拔。

（3）定义方法 ``info(self)``，返回该站基本信息，格式规定为：

.. code-block:: text

   52889 兰州 36.05°N, 103.88°E, 1517 m

（4）根据表中兰州、北京、拉萨三站资料，分别创建对象，并输出各对象 ``info()`` 的返回值。

.. list-table:: 地面气象站资料
   :header-rows: 1
   :stub-columns: 1

   * - 区站号
     - 站名
     - 纬度
     - 经度
     - 海拔
   * - 52889
     - 兰州
     - 36.05
     - 103.88
     - 1517
   * - 54511
     - 北京
     - 39.80
     - 116.47
     - 31
   * - 55591
     - 拉萨
     - 29.67
     - 91.13
     - 3649

.. admonition:: 提示

   1. 第一步：写出 ``class Station`` 及 ``__init__``；
   2. 第二步：将各参数依次赋给 ``self.station_id``、``self.name``、``self.lat``、``self.lon``、``self.altitude``；
   3. 第三步：在 ``info`` 中按题设格式拼接字符串；
   4. 第四步：按表创建兰州 ``52889``、北京 ``54511``、拉萨 ``55591`` 三个对象并输出。

**参考答案**：

.. code-block:: python

   class Station:
       def __init__(self, station_id, name, lat, lon, altitude):
           self.station_id = station_id
           self.name = name
           self.lat = lat
           self.lon = lon
           self.altitude = altitude

       def info(self):
           return (
               f"{self.station_id} {self.name} "
               f"{self.lat}°N, {self.lon}°E, {self.altitude} m"
           )

   for item in [
       ("52889", "兰州", 36.05, 103.88, 1517),
       ("54511", "北京", 39.80, 116.47, 31),
       ("55591", "拉萨", 29.67, 91.13, 3649),
   ]:
       print(Station(*item).info())

.. code-block:: text

   52889 兰州 36.05°N, 103.88°E, 1517 m
   54511 北京 39.8°N, 116.47°E, 31 m
   55591 拉萨 29.67°N, 91.13°E, 3649 m

第 2 题（继承与扩展）
^^^^^^^^^^^^^^^^^^^^^

自动气象站除台站基本信息外，尚观测气温、相对湿度及本站气压。试在第 1 题 ``Station`` 类的基础上，用继承完成扩展。不得另起与 ``Station`` 无关的新类。

（1）定义子类 ``AutoStation(Station)``，增加属性 ``temperature``、``humidity``、``pressure``。

（2）子类构造方法中须先调用 ``super().__init__(station_id, name, lat, lon, altitude)``，再为新增属性赋值。

（3）重写 ``info(self)``，先取父类 ``info()`` 的返回值，再补写气温、相对湿度及气压。格式规定为：

.. code-block:: text

   58362 上海 31.4°N, 121.47°E, 6 m | 33.5℃ 78% 1008.1 hPa

（4）根据表中上海站资料创建对象，并输出 ``info()`` 的返回值。

.. list-table:: 自动气象站资料
   :header-rows: 1
   :stub-columns: 1

   * - 区站号
     - 站名
     - 纬度
     - 经度
     - 海拔
     - 气温
     - 相对湿度
     - 气压
   * - 52889
     - 兰州
     - 36.05
     - 103.88
     - 1517
     - 31.2
     - 32
     - 846.2
   * - 54511
     - 北京
     - 39.80
     - 116.47
     - 31
     - 36.8
     - 68
     - 1002.4
   * - 58362
     - 上海
     - 31.40
     - 121.47
     - 6
     - 33.5
     - 78
     - 1008.1

.. admonition:: 提示

   说明：兰州海拔较高，其本站气压为 846.2 hPa，属正常情形，不得改为海平面气压。

   1. 第一步：写出 ``class AutoStation(Station):``，括号内填写父类名；
   2. 第二步：编写子类 ``__init__``，第一个参数仍为 ``self``，先调用 ``super().__init__(...)``，再写 ``self.temperature = temperature`` 等语句；
   3. 第三步：在 ``info`` 中先取 ``super().info()``，再拼接气温、相对湿度及气压；
   4. 第四步：按上海站一行资料创建对象并输出。

**参考答案**：

.. code-block:: python

   class AutoStation(Station):
       def __init__(self, station_id, name, lat, lon, altitude,
                    temperature, humidity, pressure):
           super().__init__(station_id, name, lat, lon, altitude)
           self.temperature = temperature
           self.humidity = humidity
           self.pressure = pressure

       def info(self):
           return (
               f"{super().info()} | "
               f"{self.temperature}℃ {self.humidity}% {self.pressure} hPa"
           )

   shanghai = AutoStation("58362", "上海", 31.40, 121.47, 6, 33.5, 78, 1008.1)
   print(shanghai.info())

.. code-block:: text

   58362 上海 31.4°N, 121.47°E, 6 m | 33.5℃ 78% 1008.1 hPa

第 3 题（简单装饰器）
^^^^^^^^^^^^^^^^^^^^^

记录气温时须输出提示信息。试编写一简单装饰器完成该项工作，不得在每一函数中重复书写相同语句。

已知若干时次的气温如下表。本题仅使用 14 时的 31.6℃。

.. list-table:: 时次与气温
   :header-rows: 1

   * - 时次
     - 08
     - 14
     - 20
   * - 气温
     - 21.6
     - 31.6
     - 23.1

（1）定义函数 ``record_temperature(temperature)``，用以输出本次写入的气温。

（2）定义装饰器 ``log_record``，包装（1）中函数。

（3）规定：调用前输出 ``开始记录气温``，调用后输出 ``已记录 31.6℃``。

（4）使用语法 ``@log_record``，传入 31.6，调用一次。

.. admonition:: 提示

   1. 第一步：先写出普通函数 ``record_temperature(temperature)``；
   2. 第二步：定义 ``log_record(func)``，于其中再定义 ``wrapper``：先输出提示，再调用 ``func(temperature)``，然后再输出提示；
   3. 第三步：``return wrapper``，并在 ``record_temperature`` 上一行加 ``@log_record``；
   4. 第四步：调用 ``record_temperature(31.6)``，核验两行提示是否出现。

**参考答案**：

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

.. code-block:: text

   开始记录气温
   写入: 31.6
   已记录 31.6℃

提升题
------

第 4 题（生成器产生气温序列）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

已知兰州站（区站号 ``52889``）某日部分时次气温如下表。试编写生成器，按顺序产生气温序列。

.. list-table:: 兰州站当日部分时次气温
   :header-rows: 1

   * - 时次
     - 08
     - 11
     - 14
     - 17
     - 20
   * - 气温
     - 21.6
     - 28.3
     - 31.6
     - 28.9
     - 23.1

（1）定义生成器函数 ``temp_seq(records)``，其中 ``records`` 为 ``(时次, 气温)`` 组成的列表。

（2）函数中须使用 ``yield``，依次产生每一对 ``(时次, 气温)``。

（3）用 ``for`` 循环遍历该生成器，按行输出时次与气温。

.. admonition:: 提示

   1. 第一步：将表中数据写成 ``records = [(8, 21.6), (11, 28.3), ...]``；
   2. 第二步：在 ``temp_seq`` 中写 ``for hour, temperature in records:``，然后 ``yield hour, temperature``；
   3. 第三步：不得以 ``return`` 代替 ``yield``，否则不能逐条产生；
   4. 第四步：用 ``for hour, temperature in temp_seq(records):`` 输出。

**参考答案**：

.. code-block:: python

   records = [(8, 21.6), (11, 28.3), (14, 31.6), (17, 28.9), (20, 23.1)]

   def temp_seq(records):
       for hour, temperature in records:
           yield hour, temperature

   for hour, temperature in temp_seq(records):
       print(hour, temperature)

.. code-block:: text

   8 21.6
   11 28.3
   14 31.6
   17 28.9
   20 23.1

第 5 题（生成器处理缺测并求最高气温）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在第 4 题基础上增加缺测处理。规定：缺测记为 ``-999``，该时次不得参与最高气温的计算。

已知兰州站资料如下表，其中 16 时缺测。

.. list-table:: 兰州站资料（16 时缺测）
   :header-rows: 1

   * - 时次
     - 08
     - 11
     - 14
     - 16
     - 17
     - 20
   * - 气温
     - 21.6
     - 28.3
     - 31.6
     - -999
     - 28.9
     - 23.1

（1）定义生成器函数 ``valid_temp(records)``，依次产生有效的 ``(时次, 气温)``。

（2）若气温为 ``-999``，则跳过该时次。

（3）遍历该生成器，输出全部有效时次，并求最高气温。

.. admonition:: 提示

   1. 第一步：将表中数据写成列表，16 时对应 ``-999``；
   2. 第二步：循环中若 ``temperature == -999``，则执行 ``continue``，否则 ``yield``；
   3. 第三步：设变量 ``t_max = None``，在循环中与当前气温比较并更新；
   4. 第四步：输出最高气温。正确结果为 31.6。

**参考答案**：

.. code-block:: python

   records = [(8, 21.6), (11, 28.3), (14, 31.6),
              (16, -999), (17, 28.9), (20, 23.1)]

   def valid_temp(records):
       for hour, temperature in records:
           if temperature == -999:
               continue
           yield hour, temperature

   t_max = None
   for hour, temperature in valid_temp(records):
       print(hour, temperature)
       if t_max is None or temperature > t_max:
           t_max = temperature
   print("最高气温:", t_max)

.. code-block:: text

   8 21.6
   11 28.3
   14 31.6
   17 28.9
   20 23.1
   最高气温: 31.6

16 时缺测，不得出现于输出中。