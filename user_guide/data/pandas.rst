.. _tut-pandas:

气象数据分析（一）Pandas
========================

第 7 节 · 模块二 气象数据处理
贯穿项目第 7 步：用 Pandas 读取 CSV 气温数据，做筛选、排序、分组统计。

气象观测记录天生就是「表格」：某日某时全国几千个站点的气温、气压、降水，或者兰州站自 1982 年以来逐日的最高／最低气温——这类\ **二维表格数据**\正是 Pandas 的主场。如果说 NumPy 是「数字的万能作坊」，Pandas 就是「表格的 Excel Pro 版」，只不过它完全可编程、可复现：同样的三步操作，点鼠标要做一秒，代码可以重复一千遍而不出错。

先看一眼它长什么样（别急着理解，感受即可）：

.. code-block:: python

   import pandas as pd

   # 把兰州、西安、成都三站的几次观测拼成一张表
   df = pd.DataFrame({
       "站名": ["兰州", "西安", "成都"],
       "气压": [850, 970, 950],
       "气温": [5.1, 8.2, 12.0],
   })
   print(df.groupby("站名")["气温"].mean())   # 一句话求每站平均气温

本章主线（贯穿项目第 7 步）：把兰州站的逐日气温 CSV 读进来——先「摸清家底」（探查结构、筛缺测）、再挑高温日、按月算报表、合并站点元数据、最后导出。每一步都只有几行，却对应一个气象数据处理的关键动作。

本章将覆盖的知识点：Series / DataFrame、``read_csv``、索引 / 筛选 / 排序、分组聚合；提升拓展：时间序列、透视表、``merge``。正文中标注的关键词（如 :term:`DataFrame`、:term:`布尔索引`）可跳转到术语参考一词一查。

7.1 Series 与 DataFrame：Pandas 的两块积木
------------------------------------------

Pandas 的一切都建立在两个容器之上：**Series** （一维带标签的数组）与 **DataFrame** （二维表格）。把这两个概念真正吃掉，后面所有操作都会顺理成章。

7.1.1 Series：带标签的一维数组
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:term:`Series` 可以看作把一组\ **数据**\与一组\ **索引（标签）**\绑在一起的一维数列。它像一份贴了姓名贴的名单：你可以说「我要找第三个同学」（按位置），也可以说「我要找小王同学」（按标签)。

.. code-block:: python

   import pandas as pd

   # 5 个站点的「昨日最高气温」
   temp_series = pd.Series(
       [32.5, 28.3, 35.1, 22.8, 30.6],
       index=["北京", "上海", "广州", "哈尔滨", "成都"],
       name="最高气温(°C)",
   )
   print(temp_series)

.. code-block:: text

   北京      32.5
   上海      28.3
   广州      35.1
   哈尔滨    22.8
   成都      30.6
   Name: 最高气温(°C), dtype: float64

.. admonition:: 关键点

   - 不指定 ``index`` 时，Pandas 自动填上 ``0, 1, 2, ...`` 整数标签；
   - ``temp_series.values`` 取到底层 NumPy 数组，``temp_series.index`` 取到标签；
   - ``Series`` 天然支持\ **按标签（``.loc``）**\与\ **按位置（``.iloc``）**\两种取法，下一节一并讲清。

7.1.2 DataFrame：二维表格容器
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:term:`DataFrame` 由多个 Series 按列拼接而成，共享同一套行索引——它是气象站点观测数据最自然的存放方式：一行一条观测，一列一个要素。

.. code-block:: python

   # 模拟 2 个站点、2 天（逐日）的地面观测
   data_dict = {
       "站点": ["北京", "北京", "上海", "上海"],
       "日期": ["2026-08-14", "2026-08-15", "2026-08-14", "2026-08-15"],
       "最高气温": [32, 34, 29, 31],
       "最低气温": [22, 24, 21, 23],
       "降水量": [0.0, 3.5, 0.0, 12.1],
   }
   df = pd.DataFrame(data_dict)
   print(df)

.. code-block:: text

      站点          日期  最高气温  最低气温   降水量
   0  北京  2026-08-14    32    22    0.0
   1  北京  2026-08-15    34    24    3.5
   2  上海  2026-08-14    29    21    0.0
   3  上海  2026-08-15    31    23   12.1

DataFrame 还可以从二维 NumPy 数组、嵌套列表、甚至直接读 CSV 文件创建（见 7.2）。

.. admonition:: 轴（Axis）——先记住这个方向感

   - ``axis=0`` 沿\ **行**\方向（垂直），通常指「跨记录」操作（如逐站聚合）；
   - ``axis=1`` 沿\ **列**\方向（水平），通常指「跨字段」操作。

   和 NumPy 一章里的 axis 口诀同源：**0 是向下压、行消失；1 是向右挤、列消失**。

7.2 数据读取：read_csv 完全指南
-------------------------------

气象数据最常见的存储格式是 **CSV** （逗号分隔值，多半用 Excel 打开）。``pd.read_csv`` 是 Pandas 功能最强、参数最多的读写函数之一。假设我们有一个 ``weather_stations.csv``\（UTF-8 编码），含字段 ``站号, 站名, 纬度, 经度, 观测时间, 气温, 湿度, 气压``：

.. code-block:: python

   # 最基础的读取
   df_weather = pd.read_csv("weather_stations.csv")

   # 实际业务中强烈建议把下面这些关键参数打开：
   df_weather = pd.read_csv(
       "weather_stations.csv",
       encoding="utf-8",                # 解决中文乱码（乱码时改 "utf-8-sig" 或 "gbk"）
       sep=",",                         # 分隔符，默认就是逗号
       parse_dates=["观测时间"],        # 一步把日期字符串解析成时间类型
       dtype={"站号": str},             # 区站号当作字符串存，避免被误当数字
       na_values=["-999", "NA", ""],    # 把气象缺测标记识别为 NaN
   )
   print(df_weather.head(3))   # 查看前 3 行

.. note::

   **关于日期解析**：如果日期列是 ``20260814`` 这种固定格式，读取后再用 ``pd.to_datetime(df["观测时间"], format="%Y%m%d")`` 手动转换往往更快、格式更可控。日期一旦变成时间类型，后面的按月统计、时间切片才能用。

7.3 数据探索与索引筛选
----------------------

拿到数据先「摸清家底」，再按需切出想要的子集。

7.3.1 基础探索
^^^^^^^^^^^^^^

.. code-block:: python

   print(df_weather.info())      # 列名、非空数量、类型 —— 一图看全貌
   print(df_weather.describe())  # 数值列的统计描述：均值、标准差、分位数
   print(df_weather.shape)       # (行数, 列数)
   print(df_weather.columns)     # 所有列名（注意列名区分大小写）

7.3.2 筛选三利器：[]、loc、iloc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: 三种取数方式的对照
   :header-rows: 1

   * - 方法
     - 干什么
     - 典型场景
   * - ``df[列名]`` / ``df[列名列表]``
     - 取一列或多列（单列返回 Series，多列返回 DataFrame）
     - 只关心特定要素
   * - ``df.loc[行标签, 列标签]``
     - 按\ **标签**\取，含结束边界
     - 索引是时间/站名时的精准定位
   * - ``df.iloc[行位置, 列位置]``
     - 按\ **整数位置**\取，不含结束边界
     - 取「第 N 行」「前 5 行」

.. code-block:: python

   # 1. 列筛选：单列 / 多列（多列必须传列表）
   print(df_weather["气温"].head())
   print(df_weather[["站名", "气温", "湿度"]].head())

   # 2. loc 按标签：取 2026-08-14 全天（假设观测时间已作为索引）
   daily = df_weather.loc["2026-08-14"]
   subset = df_weather.loc["2026-08-14":"2026-08-15", ["气温", "气压"]]
   print(subset)

   # 3. iloc 按位置：取第 1 行第 2 列 / 前 5 行
   print(df_weather.iloc[0, 1])
   print(df_weather.iloc[:5, :])

7.3.3 条件筛选（布尔索引）
^^^^^^^^^^^^^^^^^^^^^^^^^^

这是气象预警最常用的操作——把满足气象条件的观测「筛」出来。:term:`布尔索引` 的核心是：先对一列算出 True/False，再把它盖到表格上，只留 True 的行。

.. code-block:: python

   # 同时满足「气温 > 30 且 湿度 < 60%」的干热天气
   hot_dry = df_weather[(df_weather["气温"] > 30) & (df_weather["湿度"] < 60)]
   print(hot_dry)

   # 只取北京、上海两个站（用 isin 判断值是否在列表内）
   cities = df_weather[df_weather["站号"].isin(["58367", "54511"])]

   # 复杂条件还可改用 query，读起来更像 SQL
   hot_dry_q = df_weather.query("气温 > 30 and 湿度 < 60")

.. warning::

   多条件组合必须用 **``&``（且）、``|``（或）、``~``（非）**，并且\ **每个条件都要用圆括号括起来**。直接写 ``df["气温"] > 30 and df["湿度"] < 60`` 会报 ``ValueError``——因为 Python 的关键字 ``and`` 只能用在布尔值上，不能用在数组上。

7.4 排序
--------

排序能快速定位极值（哪个站最热、哪场雨最大）。

.. code-block:: python

   # 按气温降序排列，看最热的 5 条
   df_sorted = df_weather.sort_values(by="气温", ascending=False)
   print(df_sorted[["站名", "气温"]].head(5))

   # 多列排序：先按站号升序，再按观测时间降序
   df_sorted_multi = df_weather.sort_values(
       by=["站号", "观测时间"], ascending=[True, False]
   )

.. note:: ``sort_values`` 默认返回\ **新** DataFrame，不修改原表；想原地改才用 ``inplace=True``。对初学者，养成「生成新表、赋给新变量」的习惯更安全。

7.5 分组聚合（GroupBy）：气象统计的核心
---------------------------------------

「按站点算年平均温度」「按月份算累计降水量」——这类「分组 → 计算」需求占了气象数据分析的半壁江山。Pandas 的分组聚合遵循 **Split–Apply–Combine（拆分—应用—合并）** 范式，一句话即可完成 :term:`分组聚合`。

.. code-block:: python

   # 按站名分组，算每个站的平均气温和总降水量
   print(df_weather.groupby("站名")[["气温", "降水量"]].mean())

   # 不同列用不同聚合函数：气温求平均、降水量求和
   result = df_weather.groupby("站名").agg({
       "气温": "mean",
       "降水量": "sum",
   })
   print(result)

7.5.1 多级分组：站点 × 月份
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   df_weather["月份"] = df_weather["观测时间"].dt.month          # 从时间列抽月份数字
   monthly_avg = (df_weather
                  .groupby(["站名", "月份"])["气温"]
                  .mean().reset_index())     # reset_index 把分组键还原成普通列
   print(monthly_avg)

.. note::

   分组列默认会成为结果的\ **索引**。若后续还想按「站名」筛选行，务必加 ``as_index=False`` 或 ``.reset_index()``，否则会报 ``KeyError``。

7.5.2 自定义聚合与 transform
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # 自定义函数：气温日较差（极差）
   def temp_range(s):
       return s.max() - s.min()

   custom = df_weather.groupby("站名")["气温"].agg(["mean", "max", "min", temp_range])
   print(custom)

   # agg 同时给不同列配不同函数
   advanced = df_weather.groupby("站名").agg(
       平均气温=("气温", "mean"),
       最高气压=("气压", "max"),
       降水总量=("降水量", "sum"),
   )

   # transform：把组内均值广播回每一行，用来算「距平」（Anomaly）
   df_weather["气温距平"] = df_weather.groupby("站名")["气温"].transform(
       lambda x: x - x.mean())
   print(df_weather[["站名", "气温", "气温距平"]].head())

7.6 提升拓展（一）：时间序列处理
--------------------------------

气象数据几乎都带时间标签。把时间列设为索引后，Pandas 提供 ``resample`` （重采样）、``rolling`` （滑动窗口）、``shift`` （位移）三件利器。

.. code-block:: python

   df_weather.set_index("观测时间", inplace=True)     # 若读取时没设 index_col，可在此补设

   # 按月重采样：月平均气温（“M”=月末，新版本建议用 “ME”）
   monthly_mean = df_weather["气温"].resample("ME").mean()
   print(monthly_mean)

   # 按周求和：每周一截止（W-MON）
   weekly_rain = df_weather["降水量"].resample("W-MON").sum()

   # 滑动平均：5 天滑动平均气温，平滑日际噪声、看气候趋势
   df_weather["气温_5日滑动"] = df_weather["气温"].rolling(window=5, min_periods=3).mean()
   df_weather["气温_5日滑动最高"] = df_weather["气温"].rolling(window=5).max()

.. note::

   常用频率串：``"D"`` 日、``"W"`` 周、``"ME"`` 月末、``"MS"`` 月初、``"H"`` 小时、``"T"``/``"min"`` 分钟。新版本 Pandas 里用 ``"ME"`` 表示月末（``"M"`` 会触发弃用提醒）。

7.7 提升拓展（二）：透视表（Pivot Table）
-----------------------------------------

:term:`透视表` 能把一列的值展开成新表的\ **列**，最擅长把数据重塑成「站点 × 时间」矩阵，方便横向比站点、纵向比季节。

.. code-block:: python

   df_weather["月份"] = df_weather.index.month           # 从时间索引抽月份
   pivot_temp = df_weather.pivot_table(
       index="站名",       # 行索引（行标题）
       columns="月份",     # 列标签（列标题）
       values="气温",      # 要聚合的值
       aggfunc="mean",     # 聚合方式，默认 mean
       fill_value=np.nan,  # 没有数据的格子填 NaN
   )
   print(pivot_temp)

   # 双指标透视 + 行列合计（margins）
   pivot_multi = df_weather.pivot_table(
       index="站名",
       columns="月份",
       values=["气温", "降水量"],
       aggfunc={"气温": "mean", "降水量": "sum"},
       margins=True,
       margins_name="合计",
   )
   print(pivot_multi)

.. warning::

   透视表务必用 ``pivot_table`` 而非 ``pivot``：原始观测大概率存在重复（同一站同一月多天记录），``pivot`` 遇到重复会直接报 ``ValueError``，而 ``pivot_table`` 会用 ``aggfunc`` 自动聚合，正是气象场景需要的特性。

7.8 提升拓展（三）：数据合并（merge）
-------------------------------------

气象数据往往分散在多张表：逐日观测（站号、时间、温度、降水）与站点元数据（站号、站名、纬度、经度、海拔）分家存放。``pd.merge`` 类似 SQL 里的 JOIN，能按共同的键把它们拼到一起，极大丰富分析维度。

.. code-block:: python

   stations_meta = pd.DataFrame({
       "站号": ["58367", "54511", "57494"],
       "站名": ["上海", "北京", "武汉"],
       "海拔": [4.5, 31.3, 23.1],
   })
   obs_data = pd.DataFrame({
       "站号": ["58367", "58367", "54511", "57494"],
       "气温": [25.0, 26.5, 22.0, 28.1],
   })

   # 内连接：只保留两边都有的站号
   print(pd.merge(obs_data, stations_meta, on="站号", how="inner"))
   # 左连接：保留观测全部行，元数据缺失处填 NaN
   print(pd.merge(obs_data, stations_meta, on="站号", how="left"))

   # 连接键名称不同时用 left_on / right_on
   # 两边都有同名列时用 suffixes 加后缀区分
   pd.merge(obs_data, stations_meta, left_on="站号", right_on="站号",
            how="left", suffixes=("_观测", "_元数据"))

.. list-table:: 四种连接方式
   :header-rows: 1
   :widths: 20 80

   * - how 参数
     - 效果
   * - ``inner``
     - 取键的交集（默认）
   * - ``left``
     - 保留左表全部行
   * - ``right``
     - 保留右表全部行
   * - ``outer``
     - 取键的并集，缺失处填 NaN

7.9 综合实战：从原始观测到「高温热浪」报告
--------------------------------------------

把 7.1–7.8 串成一个完整小任务：**统计每个站点在 2026 年夏季（6–8 月）的高温日数（最高气温 > 35°C）及平均最高气温**。

.. code-block:: python

   # 1. 读取数据并解析日期，把时间列设为索引
   df = pd.read_csv("summer_2026_obs.csv", parse_dates=["时间"], index_col="时间")

   # 2. 读取站点元数据并左连接合并
   stations_info = pd.read_csv("stations_info.csv")
   df = pd.merge(df, stations_info, on="站号", how="left")

   # 3. 筛选夏季月份（6、7、8 月）
   summer_df = df[df.index.month.isin([6, 7, 8])]

   # 4. 标记高温日（True 会按 1 参与求和）
   summer_df["高温标识"] = (summer_df["最高气温"] > 35).astype(int)

   # 5. 按站点分组聚合，高温日数多的排前面
   report = (
       summer_df.groupby("站名")
       .agg(
           夏季平均最高温=("最高气温", "mean"),
           高温日数=("高温标识", "sum"),
           极端最高温=("最高气温", "max"),
       )
       .sort_values("高温日数", ascending=False)
   )
   print(report)

   # 6. 结果写回 CSV（加 BOM 防 Excel 中文乱码，index 保存站名本身）
   report.to_csv("heatwave_report.csv", encoding="utf-8-sig")
   print("已导出 heatwave_report.csv")

.. admonition:: 踩坑提醒

   - ``astype(int)`` 只是让 True/False 变成 0/1 便于求和，不影响原始数据；
   - 用 pandas 做这类报表时，缺测的 ``NaN`` 行会被布尔条件自动过滤——这正好符合气象业务逻辑。

7.10 小结：五条保命心法
------------------------

1. **列名大小写敏感**：先 ``print(df.columns)`` 再复制粘贴真实列名，别手敲；
2. **筛选后加 ``.copy()``** ：规避 ``SettingWithCopyWarning`` （链式赋值警告）；
3. **用 ``&``/``|`` 组合条件**，且每个条件加括号；
4. **日期先解析**：``parse_dates`` 或 ``pd.to_datetime``，时间操作才有意义；
5. **跨年按月分组用 ``pd.Grouper``/``to_period``**：只取 ``dt.month`` 会把不同年份的同月并到一组。

数据读取、预处理、分组、筛选、导出的\ **全套工程化姿势与雷区**，见下节最佳实践。

最佳实践：气象 CSV 气温处理
----------------------------

业务任务：读取气温 CSV、按月分组求均温/极值、按条件筛选高温日。

最佳实践到底是这么一回事：经过验证、稳定抗错、可复现的编码流程，适配气象观测数据（存在缺测、异常气温、日期格式、中文编码问题）。

> 🎯 一句话主线：把兰州站的原始气温 CSV，变成「一张可信的月报表」——中间每一步都要先摆平「缺测的坑、编码的坑、日期的坑、跨年分组的坑」。

拿到一份气象气温 CSV，别急着动手算。标准动作是一条装配流水线：

1. **导入库**——``pandas`` 一家就够了；
2. **读取 CSV 文件**——处理编码、直接解析日期、识别气象缺测标识、按需选取列；
3. **数据预处理校验**——统计缺失值、异常气温检查、按时间排序；
4. **按月分组聚合**——计算每个「年月」的月均温、月最高温、月最低温，区分不同年份的相同月份；
5. **条件筛选**——提取高温日记录，规避链式赋值警告；
6. **结果导出保存**——选择正确编码，避免中文乱码。

每个环节的「正确姿势」和「踩坑雷区」，下面逐节拆开。

读取气温 CSV 文件
^^^^^^^^^^^^^^^^^

✅ **最佳实践**

1. 使用 ``parse_dates`` 在读取阶段就\ **直接解析日期**，不要读取完成后再转换——一步到位，后续分组、切片全部可用；
2. 中文表头 CSV 优先 ``encoding="utf-8-sig"``；Windows 生成的 CSV 读取异常时再改用 ``gbk``；
3. 通过 ``usecols`` 只加载需要的字段，大数据量时能明显减少内存开销；
4. 设置 ``na_values`` 识别气象领域缺测标记 ``9999``、``-999.0``，把缺测转成 ``NaN``，防止缺测值混入运算。

.. code-block:: python

   import pandas as pd

   df = pd.read_csv(
       "temp_data.csv",
       parse_dates=["date"],
       encoding="utf-8-sig",
       usecols=["date", "t_avg", "t_max", "t_min"],
       na_values=["9999", "-999.0"]
   )

   # 基础校验：行数、每列类型
   print("数据总行数：", len(df))
   print(df.dtypes)

⚠️ **风险点**

- 不解析日期，日期列保存为字符串，后续所有时间分组、按月统计全部失效；
- 忽略气象缺测标识，把 ``9999`` 当成真实气温参与求平均、求极值——兰州夏天平均气温被一个虚假的几千度拉爆；
- 编码不匹配，中文表头乱码，列名对不上，读取直接失败。

数据预处理（缺失统计 / 异常气温 / 排序）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

✅ **最佳实践**

1. 统计气温字段缺失数量，评估数据完整性，心里有数；
2. 对时间列做升序排序；时间聚合前保证时序有序；
3. 气象气温合理范围一般是 ``-60℃ ~ 60℃``，可做简单异常值筛查（地球实测地表气温极值都落在这个区间内）。

.. code-block:: python

   # 统计各列缺失数量
   print(df[["t_avg", "t_max", "t_min"]].isna().sum())

   # 异常气温筛查：把物理上不可能的值挑出来检查
   suspicious = df[(df["t_avg"] < -60) | (df["t_avg"] > 60)]
   print("疑似异常气温行数：", len(suspicious))

   # 按日期升序重排，并重置行索引
   df = df.sort_values("date").reset_index(drop=True)

⚠️ **风险点**

- 原始数据不排序直接做时间分组，聚合结果的先后顺序错乱；
- 不关注缺失样本——当某个月整月大量缺测时，``mean()`` 依旧会输出一个数值，但业务结果根本不可信。

按月分组求均温、极值
^^^^^^^^^^^^^^^^^^^^

✅ **最佳实践**

使用 ``pd.Grouper(key="date", freq="M")``，按完整的「年-月」分组。这样 ``2024-01`` 与 ``2025-01`` 会被分成\ **两组**，互不干扰，绝无跨年合并。

💡 这里正是很多人栽跟头的地方：只想按月统计，却只用 ``dt.month`` 取月份数字。结果 2024 年 1 月和 2025 年 1 月被当成同一组，平均气温被「两冬叠一起」算了——那根本不是任何一年的 1 月。

.. code-block:: python

   monthly_result = (
       df.groupby(pd.Grouper(key="date", freq="M"))
         .agg(
             月均温=("t_avg", "mean"),
             月最高气温=("t_max", "max"),
             月最低气温=("t_min", "min"),
         )
   )
   print(monthly_result)

💡 **备选方案**：把日期设为索引后，用 ``resample("M")`` 重采样，适合纯时间序列分析场景（内插、向前填充等）。

⚠️ **风险点**

- ❌ **高频错误写法**：``groupby(df["date"].dt.month)`` 只取月份数字，不同年份的 1 月会合并到一组——务必用 ``pd.Grouper(freq="M")`` 保证「年+月」一起分组；
- 当月全部数据缺失时，``max``/``min`` 会返回 ``NaN``，需要结合实际判断该月结果是否可用。

条件筛选高温日
^^^^^^^^^^^^^^

✅ **最佳实践**

用布尔索引筛选，并在后面加上 ``.copy()`` 生成一份独立的 DataFrame，彻底消除 ``SettingWithCopyWarning`` （链式赋值警告）。

.. code-block:: python

   # 筛选最高气温 ≥ 35℃ 的高温日（兰州夏天的高温日）
   high_temp_days = df[df["t_max"] >= 35].copy()

   print("高温日总数量：", len(high_temp_days))
   print(high_temp_days.head())

⚠️ **风险点**

- 把数值和字符串比较：``df["t_max"] >= "35"``——字符串比较按字典序，条件判断彻底失效；
- 不使用 ``.copy()``，后续一旦修改这个筛选出来的子集，就抛出链式赋值警告，甚至悄悄改了原始数据；
- 补充一句业务常识：缺测的 ``NaN`` 行会自动被布尔条件过滤掉，这正好符合气象业务逻辑。

结果导出保存
^^^^^^^^^^^^

✅ **最佳实践**

导出 CSV 时固定使用 ``encoding="utf-8-sig"``，这样用 Excel 打开时中文表头不会变成乱码。

.. code-block:: python

   monthly_result.to_csv("monthly_temp_result.csv", encoding="utf-8-sig")

   high_temp_days.to_csv("high_temp_days.csv", encoding="utf-8-sig")

⚠️ **风险点**

- 不指定编码（或者用了纯 ``utf-8`` 不带 BOM），Windows 版 Excel 打开 CSV 时中文表头变乱码——``utf-8-sig`` 自带 BOM 头，是 Excel 的「亲儿子」格式。

完整总代码
^^^^^^^^^^

把上面几节串成一条流水线（实际项目中请把 ``temp_data.csv`` 换成你的真实观测文件）。

.. code-block:: python

   import pandas as pd

   # 1. 读取 CSV：解析日期、识别气象缺测、按需选列
   df = pd.read_csv(
       "temp_data.csv",
       parse_dates=["date"],
       encoding="utf-8-sig",
       usecols=["date", "t_avg", "t_max", "t_min"],
       na_values=["9999", "-999.0"],
   )

   # 2. 预处理：缺测统计 + 异常气温筛查 + 按时间排序
   print("缺失统计：")
   print(df[["t_avg", "t_max", "t_min"]].isna().sum())

   suspicious = df[(df["t_avg"] < -60) | (df["t_avg"] > 60)]
   print("疑似异常气温行数：", len(suspicious))

   df = df.sort_values("date").reset_index(drop=True)

   # 3. 按【年-月】分组聚合（pd.Grouper 保证跨年不合并）
   monthly_result = (
       df.groupby(pd.Grouper(key="date", freq="M"))
         .agg(
             月均温=("t_avg", "mean"),
             月最高气温=("t_max", "max"),
             月最低气温=("t_min", "min"),
         )
   )
   print("\n==== 按月统计结果 ====")
   print(monthly_result)

   # 4. 筛选高温日（.copy() 规避链式赋值警告）
   high_days = df[df["t_max"] >= 35].copy()
   print("\n==== 高温日记录 ====")
   print(f"高温日数量：{len(high_days)}")
   print(high_days.head())

   # 5. 结果导出（utf-8-sig 防 Excel 中文乱码）
   monthly_result.to_csv("monthly_output.csv", encoding="utf-8-sig")
   high_days.to_csv("high_day_output.csv", encoding="utf-8-sig")

   print("\n已导出：monthly_output.csv / high_day_output.csv")

要点总结
^^^^^^^^

1. **日期处理** ：读取 CSV 时直接 ``parse_dates`` 解析日期；按月聚合优先 ``pd.Grouper(key="date", freq="M")``，保证「年+月」同时分组，**禁止只用 ``df["date"].dt.month`` 分组** （否则跨年合并）；
2. **气象缺测处理** ：读取时通过 ``na_values`` 把 ``9999`` / ``-999.0`` 转为 ``NaN``，不能让它直接参与统计计算；
3. **编码规范** ：读写 CSV 统一使用 ``encoding="utf-8-sig"``，解决 Excel 中文乱码；
4. **子集筛选** ：布尔索引筛选后使用 ``.copy()``，规避 ``SettingWithCopyWarning``；
5. **数据顺序** ：时间序列处理前务必对日期排序，保证聚合结果可靠；
6. **结果校验** ：关注缺失统计，当某月有效样本过少时，该月统计结果不具备参考价值，宁可标注也不硬用。

.. seealso:: 配套练习：:doc:`/tutorials/data/ch07_practice`　·　示例画廊 :doc:`/gallery/plot_numpy/index`。