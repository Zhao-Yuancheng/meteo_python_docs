第 8 章练习：气象数据分析（二）Xarray
=====================================

配套 :ref:`tut-xarray` 正文使用。第 1–2 题为入门题，第 3–4 题为提升题。试题沿着贯穿项目推进——从「给数字贴上经纬度标签」起步，到区域平均、按坐标取数，最后落到时间重采样。

.. seealso:: 配套正文：:doc:`/user_guide/data/xarray`　·　术语参考：:doc:`/api/ch08_terms`　·　示例画廊 :doc:`/gallery/plot_numpy/index`

💡 **通用提示**：

- ``sel()`` 按\ **坐标值**\取数，``isel()`` 按\ **数组序号**\取数，Met 到维度名错配立刻报错；
- 坐标是浮点数时，直接写整数值可能因浮点精度匹配失败（如 31 找不到 ``31.0000001``），拿不准就用 ``method="nearest"`` 取最近格点。

入门题
------

第 1 题（实操）创建 DataArray 并添加坐标属性
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

创建一个名为 ``temperature`` 的 DataArray：数据是 3×2 的随机数组（温度值范围 280~300 K），维度为 ``(lat, lon)``。要求：

1. 纬度坐标 ``[30, 31, 32]`` （单位 degrees_north），经度坐标 ``[120, 121]`` （单位 degrees_east）；
2. 给数组添加长名称属性 ``long_name: "air_temperature"``；
3. 用 ``sel`` 提取纬度 31°N、经度 121°E 处的温度值（标量）。

.. admonition:: 提示

   1. 随机数可用 ``np.random.randint(280, 300, size=(3, 2))``；
   2. 提取标量用 ``.sel(lat=31, lon=121)``，拿不到精确值时记得 ``method="nearest"``、要纯数字加 ``.values``；
   3. 纬度、经度坐标的 ``units`` 建议记进坐标属性（``coords`` 里可加 ``attrs``），保证「自解释」。

**参考答案**：

.. code-block:: python

   import numpy as np
   import xarray as xr

   data = np.random.randint(280, 300, size=(3, 2)).astype(float)
   da = xr.DataArray(
       data,
       dims=["lat", "lon"],
       coords={
           "lat": ("lat", [30, 31, 32], {"units": "degrees_north"}),
           "lon": ("lon", [120, 121], {"units": "degrees_east"}),
       },
       attrs={"long_name": "air_temperature", "units": "K"},
   )
   print(da)

   temp_value = da.sel(lat=31, lon=121, method="nearest").values
   print(f"31°N, 121°E 处温度：{temp_value} K")

第 2 题（实操）简单矩形区域平均
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

创建一个 5×5 的 DataArray（经度 100~120°E，纬度 30~40°N），数据为随机温度（单位 K）。要求：

1. 计算整个区域的平均温度；
2. 计算子区域（经度 105~115°E，纬度 32~38°N）的平均温度；
3. 计算该子区域的最大值。

.. admonition:: 提示

   1. 用 ``.sel(lat=slice(32, 38), lon=slice(105, 115))`` 选取子区域；
   2. 不指定 ``dim`` 时，``.mean()`` 默认压缩所有维度、返回标量；
   3. 若只想沿某个维度平均，务必指定 ``dim`` 参数。

**参考答案**：

.. code-block:: python

   import numpy as np
   import xarray as xr

   lat = np.linspace(30, 40, 5)
   lon = np.linspace(100, 120, 5)
   da = xr.DataArray(
       np.random.uniform(280, 300, size=(5, 5)),
       dims=["lat", "lon"],
       coords={"lat": lat, "lon": lon},
       attrs={"units": "K"},
   )

   global_mean = da.mean()                                   # 1. 全区域平均
   print(f"全区域平均温度：{global_mean.values:.2f} K")

   sub = da.sel(lat=slice(32, 38), lon=slice(105, 115))      # 2. 子区域平均
   print(f"子区域平均温度：{sub.mean().values:.2f} K")
   print(f"子区域最大温度：{sub.max().values:.2f} K")        # 3. 子区域最大值

提升题
------

第 3 题（实操）sel 与 isel：按坐标值与按位置取数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

沿用第 1 题的 ``da`` （尺寸 3×2），完成以下操作：

1. 用 ``isel`` 提取\ **第 2 行** （纬度索引 ``1``）、**第 1 列** （经度索引 ``0``）的温度；
2. 用 ``sel`` 提取纬度在 30~31.5、经度在 120~120.8 之间的所有数据；
3. 用 ``sel`` 提取最接近 (31.8°N, 120.6°E) 的格点值。

.. admonition:: 提示

   1. ``isel`` 按整数位置，``sel`` 按坐标值——两者对应 pandas 的 ``iloc`` 与 ``loc``；
   2. 切片语法：``sel(lat=slice(30, 31.5), lon=slice(120, 120.8))``；
   3. 邻近查找：``sel(lat=31.8, lon=120.6, method="nearest")``；
   4. ``method="nearest"`` 返回单个值的 DataArray，想拿纯数字记得 ``.values``。

**参考答案**：

.. code-block:: python

   # 1. isel：取第 2 行、第 1 列
   val_isel = da.isel(lat=1, lon=0)
   print(f"isel 取值：{val_isel.values}")

   # 2. sel 区域切片
   region = da.sel(lat=slice(30, 31.5), lon=slice(120, 120.8))
   print("切片区域：\n", region)

   # 3. sel 最近邻
   nearest_val = da.sel(lat=31.8, lon=120.6, method="nearest")
   print(f"最近格点温度：{nearest_val.values}")

第 4 题（实操）时间重采样与分组聚合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

生成一个逐小时温度数据集：时间范围 2026-08-01 00:00 至 2026-08-03 23:00（共 72 个小时），温度由下面公式给出（``hour`` 为一天内的小时数 0~23）：

.. code-block:: text

   T = 20 + 5 * sin(hour / 24 * 2π)

要求：

1. 计算\ **逐日平均温度**；
2. 得到\ **每日最高温度出现的时间**\（时次）；
3. 将结果保存为新的 DataArray，维度为 ``(day,)``。

.. admonition:: 提示

   1. 用 ``pd.date_range("2026-08-01", periods=72, freq="H")`` 生成时间坐标；
   2. 重采样：``da.resample(time="D").mean()`` （按天聚合）；
   3. 找每日最高温对应的时次：``da.groupby("time.day").idxmax()``。

.. admonition:: 易错点

   - ``time="D"`` 按天分组后结果的 ``time`` 坐标默认是\ **每天的开始时刻**\（如 ``2026-08-01 00:00``）；想保留其它标签需用 ``label`` 参数；
   - ``da.idxmax()`` 返回的是\ **坐标标签**\（时间戳），不是位置索引——用它对 ``da.sel`` 选出的才是「最高温出现的那一时次」。

**参考答案**：

.. code-block:: python

   import numpy as np
   import pandas as pd
   import xarray as xr

   # 1. 生成逐时数据（72 小时 = 3 天）
   times = pd.date_range("2026-08-01 00:00", periods=72, freq="H")
   temps = 20 + 5 * np.sin(times.hour / 24 * 2 * np.pi)   # 温度公式
   da = xr.DataArray(temps, dims=["time"], coords={"time": times},
                     attrs={"units": "℃"})

   # 2. 逐日平均
   daily_mean = da.resample(time="D").mean()
   print("逐日平均温度：\n", daily_mean)

   # 3. 每日最高温出现时次（groupby + idxmax 找回原始时间戳，再 sel）
   max_idx = da.groupby("time.day").idxmax()
   max_time = da.sel(time=max_idx)
   print("每日最高温出现时间：\n", max_time)

练习 tips 汇总
--------------

📌 **重要提示 1：维度名错配**

``sel`` / ``isel`` 的键必须与维度名一致。如果数据维度叫 ``latitude``，你写 ``sel(lat=36)`` 会立刻报 ``KeyError``。先 ``print(ds.dims)`` 看清楚维度名再写。

📌 **重要提示 2：method 参数**

按坐标取数而坐标里没有精确值时，普通 ``sel`` 会报错；加 ``method="nearest"`` 取\ **最近的格点**，只精确匹配时才省略。

📌 **重要提示 3：resample 的坐标含义**

按天重采样后 ``time`` 坐标默认落在每天开始时刻，必要时用 ``label="right"`` / ``offset`` 调整，避免把「末日 00 时」误当成「当天 24 时」。