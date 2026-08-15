第 2 章配套练习：站点信息与气温数据
====================================

配套 :ref:`tut-datatype` 使用。练习全部围绕西北地区 8 个气象站（兰州、西安、成都、银川、西宁、乌鲁木齐、喀什、敦煌）的观测数据展开，与贯穿项目"兰州气温观测数据分析与可视化系统"第 2 步衔接。

做题建议：先自己写，卡住了再看 💡 提示；写完点开参考答案，重点比对**思路**而非字符。所有代码块均可复制到本地运行验证。

.. contents:: 本页练习
   :local:
   :backlinks: none

练习 1 · 站点名片（变量、多重赋值与 f-string）
----------------------------------------------

**任务**：定义兰州站的四项元信息——站名 ``"兰州"``、区站号 ``52889``、经度 ``103.83``、纬度 ``36.06``（要求经纬度用**一行多重赋值**完成），然后用 **f-string** 打印出如下格式：

.. code-block:: text

   == 站点名片 ==
   站名：兰州（52889）
   位置：103.83°E, 36.06°N

.. dropdown:: 💡 提示

   - 多重赋值：``lon, lat = 103.83, 36.06``；
   - f-string 的 ``{}`` 里可以放任何表达式，经度符号 ``°E`` 直接写在 ``{}`` 外面；
   - 想让三行输出各占一行，可以在一个 f-string 里用 ``\n``（三引号字符串支持真实换行），也可以用多条 ``print``。

.. dropdown:: 参考答案

   .. code-block:: python

      name = "兰州"
      station_id = 52889
      lon, lat = 103.83, 36.06        # 多重赋值：经纬度成对出现

      print(f"""== 站点名片 ==
      站名：{name}（{station_id}）
      位置：{lon}°E, {lat}°N""")

   .. attention::

      三引号 f-string 里的续行会保留缩进空格，输出格式要求严格时可改用三条 ``print``。

练习 2 · 气温列表操作（list 与统计五件套）
------------------------------------------

**任务**：兰州站某周（7 月 8 日—14 日）的日最高气温为：

.. code-block:: python

   temp_max_week = [28.1, 29.4, 31.2, 33.6, 34.9, 35.7, 33.2]

依次完成：

#. 7 月 15 日升温到 ``36.5``，把它**追加**进列表；
#. 输出本周**最高**、**最低**气温与**平均**气温（平均保留 1 位小数）；
#. 用**切片**取出周末两天的气温（列表最后两个元素）；
#. 统计本周**高温日**（≥35 °C）天数，输出格式如 ``高温日：2 天``。

.. dropdown:: 💡 提示

   - 统计五件套：``max`` / ``min`` / ``sum`` / ``len`` / ``sorted``；
   - 平均保留 1 位小数：``f"{avg:.1f}"``，别提前 ``round``；
   - 高温日数可用列表推导式 ``[t for t in temp_max_week if t >= 35]`` 再取 ``len``。

.. dropdown:: ⚠️ 类型混淆 tip

   ``"高温日：" + 2`` 会因 ``str + int`` 抛 ``TypeError``——数字和文本拼接必须经过 f-string 或 ``str()``。

.. dropdown:: 参考答案

   .. code-block:: python

      temp_max_week = [28.1, 29.4, 31.2, 33.6, 34.9, 35.7, 33.2]

      temp_max_week.append(36.5)                          # ① 追加

      avg = sum(temp_max_week) / len(temp_max_week)       # ② 统计
      print(f"最高 {max(temp_max_week)} °C，最低 {min(temp_max_week)} °C，平均 {avg:.1f} °C")

      weekend = temp_max_week[-2:]                        # ③ 负索引切片：最后两个
      print(f"周末两日：{weekend} °C")

      high_days = [t for t in temp_max_week if t >= 35]   # ④ 筛选高温日
      print(f"高温日：{len(high_days)} 天")

   输出：

   .. code-block:: text

      最高 36.5 °C，最低 28.1 °C，平均 32.6 °C
      周末两日：[35.7, 33.2] °C
      高温日：2 天

练习 3 · 站点档案库（dict 的增删改查与嵌套）
--------------------------------------------

**任务**：先建立两个站的档案：

.. code-block:: python

   stations = {
       "52889": {"name": "兰州", "temp": 25.6, "humidity": 40},
       "57036": {"name": "西安", "temp": 28.1, "humidity": 62},
   }

依次完成：

#. 查询并打印兰州站的气温；
#. 把西安站的湿度更新为 ``55``；
#. 新增敦煌站：键 ``"52418"``，值为 ``{"name": "敦煌", "temp": 27.4, "humidity": 26}``；
#. 给**每个站**新增一个键 ``"temp_f"``，值为华氏气温（换算式 ``c * 9 / 5 + 32``，保留 1 位小数）；
#. 遍历打印三站名片，格式如 ``52889 兰州 25.6°C / 78.1°F``。

.. dropdown:: 💡 提示

   - 第 4 问遍历 ``stations.values()``，对每个内层字典直接写入 ``s["temp_f"] = ...``；
   - 第 5 问遍历 ``stations.items()`` 可同时拿到站号与档案（元组解包）。

.. dropdown:: ⚠️ 键相关 tip

   访问不存在的键会抛 ``KeyError``：``stations["51463"]``；不确定键是否存在时用 ``stations.get("51463")``（返回 ``None`` 而不报错）。字典的键必须不可变——用列表当键会抛 ``TypeError``；站号用字符串可避免前导零丢失。

.. dropdown:: 参考答案

   .. code-block:: python

      stations = {
          "52889": {"name": "兰州", "temp": 25.6, "humidity": 40},
          "57036": {"name": "西安", "temp": 28.1, "humidity": 62},
      }

      print(stations["52889"]["temp"])                    # ① 两级索引

      stations["57036"]["humidity"] = 55                  # ② 更新

      stations["52418"] = {"name": "敦煌", "temp": 27.4, "humidity": 26}   # ③ 新增

      for s in stations.values():                          # ④ 批量写入华氏温度
          s["temp_f"] = round(s["temp"] * 9 / 5 + 32, 1)

      for sid, s in stations.items():                      # ⑤ 打印名片
          print(f"{sid} {s['name']} {s['temp']}°C / {s['temp_f']}°F")

   输出：

   .. code-block:: text

      25.6
      52889 兰州 25.6°C / 78.1°F
      57036 西安 28.1°C / 82.6°F
      52418 敦煌 27.4°C / 81.3°F

练习 4 · 运算符综合应用（算术、逻辑与成员运算）
-----------------------------------------------

**任务**：给定兰州站某日观测：

.. code-block:: python

   temp = 31.5        # 气温 °C
   rh = 58            # 相对湿度 %
   wind_deg = 373     # 风向（累积角度）
   u, v = 3.0, -4.0   # 风的 u、v 分量 m/s
   stations_nw = ["兰州", "西安", "银川", "西宁", "乌鲁木齐", "喀什", "敦煌"]

依次计算并输出：

#. 气温的**华氏值**与**开尔文值**（开尔文 = 摄氏 + 273.15）；
#. 规范化风向角（提示：``% 360``），并判断是否为北风扇区（``315 ≤ 角度 ≤ 45``，需要处理跨 0° 的情况）；
#. 风速 ``√(u² + v²)``（用 ``**`` 运算符，不 import 任何库）；
#. 判断是否为"闷热天"：``temp ≥ 30 且 rh ≥ 55``，输出布尔值；
#. 判断 ``"成都"`` 是否在西北站点名单 ``stations_nw`` 中（按本练习名单为准）。

.. dropdown:: 💡 提示

   - 第 2 问跨 0° 处理：先 ``deg % 360``，北风扇区再写成 ``angle >= 315 or angle <= 45``；
   - 第 3 问：``(u**2 + v**2) ** 0.5``，括号不能省。

.. dropdown:: ⚠️ 除法与精度 tip

   ``/`` 结果永远是 float，``9 / 5 == 1.8``；若误用 ``//`` 会得到 ``1``，换算悄悄错一截。判断温度恰好等于某值时避免 ``==``（想想 ``0.1 + 0.2`` 的教训），本题为区间判断，无此顾虑。

.. dropdown:: 参考答案

   .. code-block:: python

      temp, rh = 31.5, 58
      wind_deg = 373
      u, v = 3.0, -4.0
      stations_nw = ["兰州", "西安", "银川", "西宁", "乌鲁木齐", "喀什", "敦煌"]

      temp_f = temp * 9 / 5 + 32                 # ① 华氏
      temp_k = temp + 273.15                     #    开尔文
      print(f"{temp}°C = {temp_f}°F = {temp_k} K")

      angle = wind_deg % 360                     # ② 风向规范化：373 → 13
      is_north = angle >= 315 or angle <= 45
      print(f"风向 {angle}°，北风扇区：{is_north}")

      speed = (u**2 + v**2) ** 0.5               # ③ 风速
      print(f"风速 {speed} m/s")

      is_muggy = temp >= 30 and rh >= 55         # ④ 闷热判据
      print(f"闷热天：{is_muggy}")

      print("成都在名单中：", "成都" in stations_nw)   # ⑤ 成员运算

   输出：

   .. code-block:: text

      31.5°C = 88.7°F = 304.65 K
      风向 13°，北风扇区：True
      风速 5.0 m/s
      闷热天：True
      成都在名单中： False

练习 5 · 天气现象统计（set 与 None 综合）
-----------------------------------------

**任务**：兰州站某旬（10 天）的天气现象记录与降水数据如下（``None`` 表示当日记录缺测）：

.. code-block:: python

   phenomena = ["晴", "多云", "晴", "扬沙", "浮尘", "多云", "晴", "小雨", "晴", None]
   precip = [0.0, 0.0, 0.0, None, None, 0.0, 0.0, 3.6, 0.0, None]

依次完成：

#. 统计这旬**出现过哪几种**天气现象（去重，缺测不计），输出集合与种数；
#. 找出**有效降水日**（观测值存在且 >0 mm）的索引位置（从 0 开始）；
#. 统计**缺测天数**，并区分"无降水日"与"缺测日"分别有多少天；
#. 思考并回答：如果把 ``None`` 换成 ``0.0`` 填充，第 3 问的统计会丢失什么信息？

.. dropdown:: 💡 提示

   - 去重前先过滤 ``None``：``[p for p in phenomena if p is not None]``；
   - 判断 ``None`` 一律用 ``is not None``，不要用 ``!=``；
   - 第 2 问可遍历 ``range(len(precip))``；``enumerate`` 更优雅（第 3 章预告）。

.. dropdown:: ⚠️ 语义 tip

   ``0.0`` 是"观测到无降水"，``None`` 是"没有观测"——降水日数与数据完整率是两个统计口径，混填会永久丢失后者的信息。

.. dropdown:: 参考答案

   .. code-block:: python

      phenomena = ["晴", "多云", "晴", "扬沙", "浮尘", "多云", "晴", "小雨", "晴", None]
      precip = [0.0, 0.0, 0.0, None, None, 0.0, 0.0, 3.6, 0.0, None]

      valid_phen = [p for p in phenomena if p is not None]   # ① 剔除缺测再去重
      kinds = set(valid_phen)
      print(f"天气现象：{kinds}，共 {len(kinds)} 种")

      rain_days = [i for i, p in enumerate(precip) if p is not None and p > 0]   # ②
      print(f"有效降水日索引：{rain_days}")

      missing = sum(1 for p in precip if p is None)          # ③ 两套口径分开数
      dry = sum(1 for p in precip if p is not None and p == 0.0)
      print(f"无降水 {dry} 天，缺测 {missing} 天")

   输出（集合无序，元素顺序可能不同）：

   .. code-block:: text

      天气现象：{'晴', '多云', '扬沙', '浮尘', '小雨'}，共 5 种
      有效降水日索引：[7]
      无降水 6 天，缺测 3 天

   第 4 问：把 ``None`` 换成 ``0.0`` 后，"缺测 3 天"的信息永久丢失——统计出的"无降水 9 天"把"没观测"谎报成了"观测到无降水"，旬降水日数、数据完整率都不可信了。

拓展挑战（选做）
----------------

用本章全部知识，为贯穿项目第 2 步升级 ``ch02_types.py``：把西北 8 站全部建进嵌套字典 ``stations``，站点信息参考 ``weather_project/data/stations_metadata.csv``；统计 8 站的平均海拔与最高海拔站，输出对齐的报表。

.. hint:: f-string 的 ``:>8`` 右对齐格式可以让多行报表的列对齐。

.. seealso::

   - 返回正文：:ref:`tut-datatype`
   - 术语速查：:doc:`/api/ch02_terms`
   - 可执行示例：:doc:`/gallery/auto_examples/plot_basics/plot_datatypes`
