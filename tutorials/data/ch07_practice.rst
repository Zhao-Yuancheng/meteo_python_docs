第 7 章练习：气象数据分析（一）Pandas
=====================================

配套 :ref:`tut-pandas` 正文使用。本练习贯穿一条现实主线：兰州站的一组逐日观测，你要把它拆开揉碎——先看清（读取）、再挑出高温日（筛选）、再按月算报表（分组）、再排出名次（排序）、最后存好文件（导出）。

.. seealso:: 配套正文：:doc:`/user_guide/data/pandas`　·　示例画廊 :doc:`/gallery/plot_numpy/index`

练习使用一份气象站点 CSV 数据。示例 CSV 字段：``date, station_id, temp, pressure``

- ``date``：观测日期，``YYYY-MM-DD`` 格式
- ``station_id``：站点编号
- ``temp``：气温（℃）
- ``pressure``：气压（hPa）

练习统一导入（每道题开头都先跑这句）：

.. code-block:: python

   import pandas as pd

第 1 题（实操）读取数据，基础查看
---------------------------------

**任务**：

1. 使用 ``pd.read_csv()`` 读取气象观测文件 ``weather.csv``，保存为 ``df``。
2. 分别打印前 5 行、数据表基本信息、数据表统计描述。
3. 输出数据表的列名，观察列名字母大小写。

.. admonition:: 提示

   **列名严格区分大小写**：``df['Temp']`` 和 ``df['temp']`` 是完全不同的列。若 CSV 里列名是 ``Temp``，你却写 ``df['temp']``，会直接抛出 ``KeyError``。先 ``print(df.columns)`` 看一眼真实列名，再复制粘贴过来，比手敲更稳。

**参考答案**：

.. code-block:: python

   import pandas as pd

   df = pd.read_csv("weather.csv")

   print(df.head())        # 前 5 行
   print(df.info())        # 表基本信息：行数、列数、数据类型、内存占用
   print(df.describe())    # 数值列的统计描述
   print(df.columns)       # 列名（观察大小写）

第 2 题（实操）条件筛选，筛选高温日
-----------------------------------

**任务**：

1. 筛选气温 ``temp`` 大于等于 35℃ 的高温记录，得到数据子集 ``high_temp_df``。
2. 统计一共有多少条高温记录。
3. 打印高温记录的全部内容。

.. admonition:: 提示

   这里很容易触发 ``SettingWithCopyWarning``\（链式赋值警告）。原因是：筛选结果可能只是原数据的一个「视图」，直接对它赋值修改，可能会悄悄改动原始 DataFrame，pandas 用警告提醒你。

   **✅ 正确做法**：筛选结果立刻 ``.copy()``，得到一份完全独立的副本，再修改就互不影响、也无警告：

   .. code-block:: python

      high_temp_df = df[df["temp"] >= 35].copy()

   **❌ 不推荐（会弹出警告）**：

   .. code-block:: python

      # 没有 .copy()，后续若对 high_temp_df 赋值修改，会触发 SettingWithCopyWarning
      high_temp_df = df[df["temp"] >= 35]

**参考答案**：

.. code-block:: python

   # .copy() 生成独立副本，规避 SettingWithCopyWarning
   high_temp_df = df[df["temp"] >= 35].copy()

   print("高温记录条数：", len(high_temp_df))
   print(high_temp_df)

第 3 题（实操）按月分组统计气象数据
-----------------------------------

**任务**：

1. 将 ``date`` 列转换为 pandas 时间格式。
2. 从 ``date`` 提取月份，新增一列 ``month``。
3. 按照 ``month`` 分组，计算每月气温的\ **平均气温、最高气温、最低气温**。
4. 将分组统计结果保存为 ``month_stats``。

.. admonition:: 提示

   - ``date`` 列读进来通常是字符串，必须先 ``pd.to_datetime(df["date"])`` 转成时间类型，之后 ``.dt.month``、时间切片等操作才能正常进行。
   - 只用 ``.dt.month`` 分组，会把不同年份的相同月份（2024-01 与 2025-01）并到一组。如果数据只覆盖一年，这样没问题；如果有多年的数据，请改用 ``df.groupby(df["date"].dt.to_period("M"))`` 或 ``pd.Grouper(freq="M")``，保证「年+月」一起分组。
   - ``df.groupby("month")["temp"].agg(["mean", "max", "min"])`` 会一次算出三列统计量：mean 均值、max 最高、min 最低。

**参考答案**：

.. code-block:: python

   df["date"] = pd.to_datetime(df["date"])
   df["month"] = df["date"].dt.month

   month_stats = df.groupby("month")["temp"].agg(["mean", "max", "min"])
   print(month_stats)

第 4 题（实操）数据排序
-----------------------

**任务**：

1. 在原始 ``df`` 上，按气温 ``temp`` 从高到低降序排序。
2. 输出全年温度最高的 10 条观测记录。
3. 说明：排序可以原地修改，也可以生成一个新的 DataFrame。

.. admonition:: 提示

   - ``df.sort_values(by="temp", ascending=False)``：``by`` 指定排序列，``ascending=False`` 表示降序（从大到小）。升序就写 ``ascending=True``，或省略。
   - ``sort_values`` 默认返回\ **新** DataFrame，不会改原表；想原地修改则加参数 ``inplace=True``。对初学者，养成「生成新表、赋值给新变量」的习惯更安全。
   - 排完取前 N 条用 ``.head(10)``，从大到小取前 10 就是全年最高温的 10 条记录。

**参考答案**：

.. code-block:: python

   # 降序排序，生成新 DataFrame（不改原表）
   df_sorted = df.sort_values(by="temp", ascending=False)

   # 全年温度最高的 10 条观测记录
   print(df_sorted.head(10))

第 5 题（实操）数据导出保存
---------------------------

**任务**：

1. 将第 2 题得到的高温记录 ``high_temp_df`` 导出保存为 ``high_temperature.csv``，**不要**\保存 pandas 自动生成的行索引。
2. 将第 3 题的按月统计结果 ``month_stats`` 导出保存为 ``month_temp_stat.csv``。

.. admonition:: 提示

   - ``to_csv(index=False)``：关掉 pandas 默认写入的 0、1、2… 行号列。日常导出气象数据做交接、给 Excel 用时，几乎都要加 ``index=False``，否则文件里多出一列没意义的行号。
   - 导出含中文表头的文件，建议同时加 ``encoding="utf-8-sig"``，这样 Windows 的 Excel 打开不会乱码（如 ``to_csv("xxx.csv", index=False, encoding="utf-8-sig")``）。

**参考答案**：

.. code-block:: python

   high_temp_df.to_csv("high_temperature.csv", index=False)
   month_stats.to_csv("month_temp_stat.csv")

练习 tips 汇总
--------------

📌 **重要提示 1：列名大小写**

Pandas 列名严格区分大小写。如果你的 CSV 列名是 ``Temp``，写 ``df["temp"]`` 会直接报 ``KeyError``。

调试技巧：先 ``print(df.columns)``，再把真实的列名\ **复制粘贴**\进代码，避免手动输入写错。

📌 **重要提示 2：SettingWithCopyWarning**

警告含义：你操作的 DataFrame 可能只是原数据的切片视图，修改它可能会改动原始数据，结果不可预期。

**✅ 正确写法**\（筛选后加 ``.copy()``）：

.. code-block:: python

   subset = df[df["temp"] > 30].copy()
   subset["new_col"] = subset["temp"] + 1

**❌ 不推荐写法**\（会弹出警告）：

.. code-block:: python

   subset = df[df["temp"] > 30]
   subset["new_col"] = subset["temp"] + 1

📌 **小提示**

- ``to_csv(index=False)``：导出 CSV 时关闭 pandas 自带行号索引，日常导出气象数据几乎都要加这个参数；
- ``pd.to_datetime()`` 一定要用来处理日期列，时间相关操作（提取年月、时间切片、按月重采样）才可以正常运行。