.. _tut-pandas:

气象数据分析（一）Pandas
========================

第 7 节 · 模块二 气象数据处理
贯穿项目第 7 步：用 Pandas 读取 CSV 气温数据，做筛选、排序、分组统计。

.. note::

   本节正文由 T-701 交付后填充，以下为内容概要与导读。

Pandas 适合站点观测等表格数据：

.. code-block:: python

   import pandas as pd

   df = pd.DataFrame({
       "站名": ["兰州", "西安", "成都"],
       "气压": [850, 970, 950],
       "气温": [5.1, 8.2, 12.0],
   })
   df["位势高度"] = df["气压"] * 8.0   # 粗略估算
   print(df.sort_values("气温", ascending=False))

本章将覆盖的知识点：Series / DataFrame、``read_csv``、索引 / 筛选 / 排序、分组聚合；提升拓展：时间序列、透视表、``merge``。

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

1. 使用 ``parse_dates`` 在读取阶段就**直接解析日期**，不要读取完成后再转换——一步到位，后续分组、切片全部可用；
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

使用 ``pd.Grouper(key="date", freq="M")``，按完整的「年-月」分组。这样 ``2024-01`` 与 ``2025-01`` 会被分成**两组**，互不干扰，绝无跨年合并。

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

用布尔索引筛选，并在后面加上 ``.copy()`` 生成一份独立的 DataFrame，彻底消除 ``SettingWithCopyWarning``（链式赋值警告）。

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

1. **日期处理**：读取 CSV 时直接 ``parse_dates`` 解析日期；按月聚合优先 ``pd.Grouper(key="date", freq="M")``，保证「年+月」同时分组，**禁止只用 ``df["date"].dt.month`` 分组**（否则跨年合并）；
2. **气象缺测处理**：读取时通过 ``na_values`` 把 ``9999`` / ``-999.0`` 转为 ``NaN``，不能让它直接参与统计计算；
3. **编码规范**：读写 CSV 统一使用 ``encoding="utf-8-sig"``，解决 Excel 中文乱码；
4. **子集筛选**：布尔索引筛选后使用 ``.copy()``，规避 ``SettingWithCopyWarning``；
5. **数据顺序**：时间序列处理前务必对日期排序，保证聚合结果可靠；
6. **结果校验**：关注缺失统计，当某月有效样本过少时，该月统计结果不具备参考价值，宁可标注也不硬用。

.. seealso:: 配套练习：:doc:`/tutorials/ch07_practice`　·　示例画廊 :doc:`/gallery/plot_numpy/index`。