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
