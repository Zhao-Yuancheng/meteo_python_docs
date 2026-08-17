.. _tut-flow:

分支、条件与循环
================

第 3 节 · 模块一 Python 编程基础
贯穿项目第 3 步：对逐日气温做等级判定（寒冷 / 偏冷 / 适宜 / 炎热），统计各等级天数。

前两章我们学会了"存数据"（变量与类型），但程序只会从头到尾线性执行。现实中的气象判断从来不是一条直线：兰州今天算不算高温？下的是小雨还是暴雨？该对哪几站发预警？——这些都需要程序**根据条件做出选择** （分支）、**重复处理一批数据** （循环）。本章就讲这两件核心武器。

学完本章你将能够：

#. 用 ``if`` / ``elif`` / ``else`` 根据条件选择执行路径；
#. 用 ``for`` 遍历列表、字典、字符串，用 ``while`` 做条件循环；
#. 用 ``break`` / ``continue`` 控制循环流程；
#. 用 ``range`` / ``enumerate`` / ``zip`` / 嵌套循环处理多站、多日数据。

.. grid:: 1 2 2 3
   :gutter: 2

   .. grid-item-card:: 🎬 配套动画
      :link: ch03-animation
      :link-type: ref
      :class-card: gallery-card

      ^^^

      分支流程图与循环遍历动画

   .. grid-item-card:: ✏️ 配套练习
      :link: /tutorials/ch03_practice
      :link-type: doc
      :class-card: gallery-card

      ^^^

      5 道气温等级与循环实战题

   .. grid-item-card:: 🖼 可执行示例
      :link: /gallery/plot_basics/plot_flow
      :link-type: doc
      :class-card: gallery-card

      ^^^

      气温等级判定与统计可视化

.. _ch03-animation:

配套动画（T-302）
-------------------

本动画把本节的三类控制流一口气演给你看：① ``if-elif-else`` 流程图——条件为真走这条路、为假走那条路（箭头高亮动画）；② ``for`` 循环遍历列表——指针逐个滑过元素；③ ``while`` 循环——条件检查 → 执行体 → 回到条件；④ ``break``（直接跳出）与 ``continue``（跳过本次）的跳转路径对比。点击播放，可暂停拖动进度条反复观看。

.. video:: /_static/videos/T302-分支、循环、条件动画_av1.webm
   :width: 100%

条件判断：if / elif / else
--------------------------

逻辑运算与运算符
~~~~~~~~~~~~~~~~

上一章讲过布尔值（``True`` / ``False``），这里展示它的用途。程序从"开始"走到一个判断框——"温度是否大于 35 ℃"，这个判断框就是一个**双刀开关**：

- 若判断为 ``True`` （是），程序走"高温天气"这条路；
- 若判断为 ``False`` （否），程序走"天气较凉爽"这条路。

（完整的分支流程图见本节上方"配套动画"处的动画。）

在这个判断框里，布尔值起到**双刀开关**的作用：开关拨向 ``True`` 走一条路，拨向 ``False`` 走另一条路。不同的执行路径就是**分支**，计算机判断 ``True`` / ``False`` 的过程就是**逻辑运算**。

实际问题中约束条件复杂多样，所以我们用**逻辑运算符**来组合判据：

.. list-table::
   :header-rows: 1
   :widths: 14 86

   * - 运算符
     - 含义
   * - ``x and y``
     - 要求 x 和 y 都为 True 才执行下一步
   * - ``x or y``
     - 只要 x 与 y 任意一个为 True 即可执行下一步
   * - ``not x``
     - 与条件 x 相反（取反）
   * - ``x in y``
     - x 在 y 序列中，执行下一步
   * - ``x not in y``
     - x 不在 y 序列中，执行下一步
   * - ``x != y``
     - x 不等于 y，执行下一步
   * - ``x == y``
     - x 等于 y，执行下一步

.. warning::

   在 Python 中，单独的等号 ``=`` **仅仅表示赋值**，判断相等必须用双等号 ``==``。把 ``==`` 写成 ``=`` 是第一高频报错。

if 语句的一般形式
~~~~~~~~~~~~~~~~~~

``if`` 语句根据一定条件执行不同操作，一般形式为：

.. code-block:: python

   if 条件1:
       条件1为真时执行的代码块
   elif 条件2:
       条件2为真时执行的代码块
   else:
       以上条件都不满足时执行的代码块

.. attention::

   三件事务必注意：① 条件后必须跟冒号 ``:``；② 分支内部代码必须**统一缩进**（Python 靠缩进划分从属关系）；③ ``else`` 后面**不跟条件**，它兜底其余所有情况。

天气判断最经典的例子是**雨量等级判定**（中国气象局标准，单位 mm）：

.. code-block:: python

   rain = float(input("请输入24小时降雨量(mm)："))
   if rain < 0.1:
       print("无雨")
   elif rain < 10:
       print("小雨")
   elif rain < 25:
       print("中雨")
   elif rain < 50:
       print("大雨")
   elif rain < 100:
       print("暴雨")
   elif rain < 250:
       print("大暴雨")
   else:
       print("特大暴雨")

.. tip::

   **为什么这样写更稳**：分支自上而下逐个检查，``elif`` 只在前一条件不满足时才判断下一个。所以"小于 10"自然落到小雨，无需写 ``0.1 <= rain < 10`` 这类又长又易留缝的区间——一连串 ``< 阈值`` 天然形成无缝隙、无重叠的阶梯。

遇到较为简单的条件，可以用**条件表达式**（三元表达式）写得更紧凑：

.. code-block:: python

   temp = float(input("请输入气温(°C)："))
   level = "高温" if temp >= 35 else "正常"
   print(level)

循环：反复处理一批数据
----------------------

实际工作常要重复做相同的事——对 30 天逐日气温求平均、对 5 个站点逐一判断高温。这就用到**循环结构**。Python 主要有 ``for`` 与 ``while`` 两种。

for 循环
~~~~~~~~~

``for`` 主要用于**遍历可迭代对象**（列表、字典、字符串等能逐一返回元素的对象），是气象数据处理中使用频率最高的循环：

.. code-block:: python

   for 临时变量 in 可迭代对象:
       要执行的重复代码

**逐站处理** （最典型场景）。先看不带 ``zip`` 的写法：

.. code-block:: python

   stations = ["北京", "上海", "广州", "武汉"]
   temps = [36.5, 35.2, 38.0, 37.5]
   for i in range(len(stations)):
       if temps[i] >= 35:
           print(f"{stations[i]} 高温：{temps[i]}℃")

用 ``zip`` 把两个列表"拉链式"成对打包，更简洁：

.. code-block:: python

   stations = ["北京", "上海", "广州", "武汉"]
   temps = [36.5, 35.2, 38.0, 37.5]
   for station, temp in zip(stations, temps):
       if temp >= 35:
           print(f"{station} 高温：{temp}℃")

.. tip::

   ``zip(a, b)`` 把两个序列按位置一一配对，一次循环同时拿到 ``station`` 和与之对应的 ``temp``，比用下标 ``i`` 挨个取更直观。

**遍历字典**：直接遍历拿到的是键，更推荐用 ``.items()`` 同时拿键和值：

.. code-block:: python

   weather = {"北京": 36.5, "上海": 35.2, "广州": 38.0, "武汉": 37.5}
   for station, temp in weather.items():
       if temp >= 35:
           print(f"{station} 高温：{temp}℃")

**遍历字符串**：字符串也是可迭代对象，处理"一串城市名"这种场景推荐用 ``.split()`` 按空格拆成列表再遍历：

.. code-block:: python

   cities = "北京 上海 广州 武汉"
   for city in cities.split():
       print(city)          # 北京 上海 广州 武汉（每行一个）

.. warning::

   不要用 ``str`` 给字符串变量命名！``str`` 是内置类型名，覆盖后你就无法再调用 ``str()`` 做类型转换了。

while 循环
~~~~~~~~~~~

``for`` 在**已知遍历几项**时用；``while`` 在**只知道条件、不知道次数**时用：

.. code-block:: python

   while 条件:
       要执行的重复代码

**代码示例**：温度从 28 ℃ 起，每小时升高 0.5 ℃，问多少小时后达到 35 ℃ 触发高温预警？

.. code-block:: python

   temp = 28.0
   hour = 0
   while temp < 35:
       hour += 1
       temp += 0.5
       print(f"第 {hour} 小时：温度 {temp:.1f}℃")
   print(f"经过 {hour} 小时后，温度达到 {temp:.1f}℃，触发高温预警！")

.. warning::

   **无限循环陷阱**：``while`` 循环体内必须**更新条件涉及的变量**（这里 ``temp += 0.5``），否则条件永远为真，程序卡死。这是 ``while`` 的第一大坑。

break 与 continue
~~~~~~~~~~~~~~~~~~~

``break`` 用于**终止整个循环**，跳出后执行循环体后的代码；``continue`` 用于**跳过本次迭代**，直接进入下一次。处理缺测数据时最常用：

.. code-block:: python

   raw_data = [25.5, None, 26.0, None, 27.2]

   # break：遇到第一个缺测就停（数据被截断，需人工介入）
   count = 0
   for temp in raw_data:
       count += 1
       if temp is None:
           print(f"数据{count}缺失！")
           break
   # 输出：数据2缺失！

   # continue：跳过缺测继续（缺测是常态，正常时段照常统计）
   count = 0
   for temp in raw_data:
       count += 1
       if temp is None:
           print(f"数据{count}缺失！")
           continue
       print(f"数据{count}：{temp}℃")
   # 输出：数据1：25.5℃ 数据2缺失！数据3：26.0℃ 数据4缺失！数据5：27.2℃

.. tip::

   **区别一句话**：``break`` 是"这个循环到此为止，全都不干了"；``continue`` 是"这一条跳过，下一条继续"。

range 与 enumerate
~~~~~~~~~~~~~~~~~~~

``range()`` 生成整数序列，用于控制循环次数；``enumerate()`` 在遍历时同时给出**下标**和**值**：

.. code-block:: python

   week_temps = [36.9, 35.6, 33.2, 31.5, 38.6, 37.5, 35.8]

   for day in range(7):                       # 用下标取值
       temp = week_temps[day]
       if temp >= 35:
           print(f"本周第 {day+1} 天为高温日，温度为 {temp}℃")

   for day, temp in enumerate(week_temps):    # 更优雅：同时拿下标和值
       if temp >= 35:
           print(f"本周第 {day+1} 天为高温日，温度为 {temp}℃")

嵌套循环
~~~~~~~~~~

外层循环走一步，内层循环完整走一遍——像时钟，时针走一小格分针走一整圈。适合处理**二维数据**（多站 × 多日）：

.. code-block:: python

   station_temps = [
       [28, 30, 32, 33],   # 北京 4 天
       [27, 29, 31, 32],   # 上海 4 天
       [29, 31, 33, 35]    # 广州 4 天
   ]
   station_names = ["北京", "上海", "广州"]
   for i in range(len(station_names)):
       total = 0
       for temp in station_temps[i]:
           total += temp
       avg = total / len(station_temps[i])
       print(f"{station_names[i]} 日平均温度：{avg:.1f}℃")

提升拓展
--------

while-else：循环正常结束才执行的兜底
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``while`` （和 ``for``）后面可以跟一个 ``else``，它只在循环**没有被 break 中断、正常跑完**时执行一次。非常适合"找东西，找不到就报未出现"：

.. code-block:: python

   temps = [18, 21, 24, 27, 32, 35]
   i = 0
   while i < len(temps) and temps[i] < 30:
       i += 1
   else:
       if i < len(temps) and temps[i] >= 30:
           print(f"首个超阈值下标：{i}")
       else:
           print("未出现")

列表推导式：一行筛出符合条件的元素
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

把"新建空列表 → for 循环 → if 判断 → append"压成一行（第 2 章已初见，这里正式登场）：

.. code-block:: python

   temps = [36.9, 35.6, 33.2, 31.5, 38.6, 37.5, 35.8]
   high_days = [t for t in temps if t >= 35]      # 只留 ≥35 °C
   print(high_days)                                # [36.9, 35.6, 38.6, 37.5]

最佳实践：分支与循环的气象规范
------------------------------

正文讲"怎么用"，这里讲"怎么写才稳"。以下规则来自一线数据处理踩坑经验，建议当作团队规范执行。

气温等级判定：用"阶梯式 elif"代替碎片区间
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

气象分级（雨量、风级、气温等级）本质是**把连续数值切成若干区间**。最稳的写法是**自上而下的 ``elif`` 阶梯**——每个阈值只写一边，绝不写 ``10 <= rain < 25`` 这类又长又容易留缝的双边区间。

**推荐写法** （雨量等级，单位 mm）：

.. code-block:: python

   rain = float(input("请输入24小时降雨量(mm)："))
   if rain < 0.1:
       print("无雨")
   elif rain < 10:
       print("小雨")
   elif rain < 25:
       print("中雨")
   elif rain < 50:
       print("大雨")
   elif rain < 100:
       print("暴雨")
   elif rain < 250:
       print("大暴雨")
   else:
       print("特大暴雨")

**为什么这样写**：``elif`` 只在前面条件不满足时才继续判断，所以 ``rain < 10`` 天然意味着"≥ 0.1 且 < 10"。这样写出的区间**无缝隙、无重叠**，改一个阈值只动一行，不会顾此失彼。

**反模式** （碎片区间，易留缝、难维护）：

.. code-block:: python

   if rain < 0.1:
       ...
   elif 0.1 <= rain < 9.9:      # ✗ 9.9 到 10 之间成"真空区"
       ...
   elif 10 <= rain < 24.9:      # ✗ 24.9 到 25 又有缝
       ...

.. tip::

   **铁律**：分级判断统一用"阶梯式 ``elif`` + 单边比较"，阈值写成规范的整数边界（10、25、50、100、250），不要写 9.9、24.9 这种"躲缝"的怪数字。

遍历多站找极值：初始化 + 逐个比较
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在多个站点（或多天）里找最大/最小气温，是 ``for`` 循环的经典用法。两条铁律：

1. **极值变量在循环外初始化**，且初始值要"小到任何数据都能超过 / 大到任何数据都超不过"；
2. **逐站比较**，一边遍历一边更新极值。

.. code-block:: python

   stations = ["北京", "上海", "广州"]
   temps = [36.5, 35.2, 38.0]

   max_temp = -999.0          # 初始值：低于任何正常气温
   max_station = ""
   for station, temp in zip(stations, temps):
       if temp > max_temp:
           max_temp = temp
           max_station = station
   print(f"气温最高的是 {max_station}：{max_temp}℃")

**更省事**：如果只要数值、不关心是哪个站，直接用内置 ``max()`` / ``min()``：

.. code-block:: python

   temps = [36.5, 35.2, 38.0]
   print(max(temps))          # 38.0
   print(min(temps))          # 35.2

.. tip::

   **铁律**：找最大值初始化为非常小的数（如 ``-float("inf")``），找最小值初始化为非常大的数（如 ``float("inf")``），这样无论数据正负都能正确更新。

避免无限循环：while 三大保命习惯
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **循环体内必须更新条件变量**：凡是 ``while`` 条件里出现的变量，循环体里至少要有一处让它"朝终止方向变化"；
2. **给循环加"安全上限"**：处理不确定的外部数据（如等待输入、读取文件）时，用 ``break`` 在达到上限时强制退出；
3. **优先用 ``for``**：只要已知要遍历的对象，就用 ``for``，它天然不会死循环。只有"次数未知、只靠条件"时才用 ``while``。

.. code-block:: python

   attempts = 0
   while True:                    # 看起来是死循环
       attempts += 1
       data = read_sensor()
       if data is not None:
           break                  # 拿到数据就退出
       if attempts >= 10:         # 但最多试 10 次
           print("传感器无响应，放弃")
           break

嵌套循环处理二维气象数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~

多站 × 多日的双层结构（如站点与时间），用嵌套循环：**外层站、内层日**。注意三点：

1. 内层循环在每次外层迭代时**重新初始化**累加器（求每日/每站均值）；
2. 缩进层次务必清晰（外层 4 空格、内层 8 空格）；
3. 数据量很大时，优先考虑 NumPy 向量化（第 6 章），嵌套循环只适合中小规模。

.. code-block:: python

   station_temps = [[28, 30, 32, 33], [27, 29, 31, 32]]
   station_names = ["北京", "上海"]
   for i, site in enumerate(station_temps):
       total = 0
       for t in site:
           total += t
       avg = total / len(site)
       print(f"{station_names[i]} 平均 {avg:.1f}℃")

常见反模式速查
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - 反模式
     - 后果
     - 正确姿势
   * - ``if temp = 35:``
     - ``SyntaxError``，``=`` 不能用于判断
     - ``if temp == 35:``
   * - ``else`` 后面跟条件
     - ``SyntaxError``，``else`` 不接条件
     - ``else:``
   * - 忘记冒号 ``:``
     - ``SyntaxError``
     - ``if ...:``、``for x in ...:``
   * - 缩进不一致
     - ``IndentationError``
     - 统一 4 空格
   * - ``while`` 内不更新条件变量
     - 死循环、程序卡死
     - 循环体更新变量 / 加安全上限
   * - 用 ``str`` 给变量命名
     - 覆盖内置类型，``str(x)`` 失效
     - 用 ``cities``、``station_name``
   * - 分级写 ``0.1 <= rain < 9.9``
     - 区间留缝、漏判
     - 阶梯式 ``elif`` + 单边比较

.. tip::

   **一句话总结**：分级判定用阶梯 ``elif``，找极值先初始化再逐个比，``while`` 三件套（更新变量、安全上限、能用 ``for`` 就用 ``for``）保平安——做到这三条，你的控制流代码就稳了。

贯穿项目 · 第 3 步：气温等级判定与统计
---------------------------------------

把本章知识点组装起来，完成 ``weather_project/scripts/ch03_levels.py``：

.. code-block:: python

   """ch03_levels.py —— 贯穿项目第 3 步：气温等级判定与统计"""

   # 兰州站近 7 日最高气温（°C）
   temps = [28.1, 29.4, 31.2, 33.6, 34.9, 35.7, 33.2]

   # 等级判定（≥30 炎热，20~30 适宜，10~20 偏冷，<10 寒冷）
   def temp_level(t):
       if t >= 30:
           return "炎热"
       elif t >= 20:
           return "适宜"
       elif t >= 10:
           return "偏冷"
       else:
           return "寒冷"

   # 统计各等级天数
   from collections import Counter

   counts = Counter(temp_level(t) for t in temps)

   for t in temps:
       print(f"{t:.1f}℃ → {temp_level(t)}")
   print("各等级天数：", dict(counts))

输出：

.. code-block:: text

   28.1℃ → 适宜
   29.4℃ → 适宜
   31.2℃ → 炎热
   33.6℃ → 炎热
   34.9℃ → 炎热
   35.7℃ → 炎热
   33.2℃ → 炎热
   各等级天数： {'炎热': 5, '适宜': 2}

**验收标准**：脚本对每个温度输出等级，并统计各等级天数。可运行版本见 :doc:`/gallery/plot_basics/plot_flow`。

本章小结
--------

- **分支**：``if`` / ``elif`` / ``else`` 根据条件选择执行路径；``elif`` 自上而下，条件用 ``==``、``!=``、``in``、``and``、``or``、``not`` 组合；
- **循环**：``for`` 遍历可迭代对象（列表、字典、字符串），``while`` 按条件循环；
- **调控**：``break`` 跳出循环，``continue`` 跳过本次；
- **进阶**：``range`` / ``enumerate`` / ``zip`` / 嵌套循环处理二维数据；
- **应用**：雨量等级判定、逐站高温预警、多站多日求平均，都是分支 + 循环的实战场景。

.. seealso::

   - 术语详解：:doc:`/api/ch03_terms` —— 每个名词的生活类比与易混淆点；
   - 动手练习：:doc:`/tutorials/ch03_practice` —— 5 道气温等级与循环实战题（含提示）；
   - 可执行示例：:doc:`/gallery/plot_basics/plot_flow` —— 气温等级判定与统计可视化。