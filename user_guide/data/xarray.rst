.. _tut-xarray:

气象数据分析（二）Xarray
========================

第 8 节 · 模块二 气象数据处理
贯穿项目第 8 步：用 Xarray 读取 NetCDF 再分析气温场，做区域平均与时间切片。

.. note::

   本节正文由 T-801 交付后填充，以下为内容概要与导读。

Xarray 给多维数组加上经纬度、时间等坐标标注，是读 NetCDF 的主力：

.. code-block:: python

   import numpy as np
   import xarray as xr

   lon = np.linspace(70, 140, 8)
   lat = np.linspace(20, 50, 5)
   temp = 15 + 10 * np.sin(np.deg2rad(lon))[None, :] * np.cos(np.deg2rad(lat))[:, None]

   da = xr.DataArray(temp, coords=[("lat", lat), ("lon", lon)], name="t2m")
   da.attrs["units"] = "°C"
   print(da.sel(lat=36, method="nearest"))

本章将覆盖的知识点：DataArray / Dataset、坐标与维度、``sel`` / ``isel``、``open_dataset``、简单绘图；提升拓展：``groupby`` 时间分组、``resample`` 重采样、加权平均。

最佳实践：NetCDF 气温场处理
----------------------------

业务任务：读取 NetCDF 气温场、区域平均、时间切片、简单绘图。

最佳实践一句话：**气象 nc 文件要安全读取、正确核对维度（time/lat/lon）与单位（K↔℃），区域平均必须做纬度加权（cos(lat)），合理切片、绘图屏蔽缺测，保证结果可复现。**

完整标准化工作流程如下：

1. 导入依赖库（``xarray``、``numpy``、``matplotlib``）；
2. 读取 NetCDF 文件，检查维度、变量、缺测值 ``_FillValue``；
3. 时间切片：选取指定时间范围，裁剪时间维度；
4. 空间裁剪：截取目标经纬度研究区域；
5. **区域加权平均**：纬度加权计算区域平均气温（气象必须纬度加权，不能直接算术平均）；
6. 空间场切片：取出某时刻的空间气温场；
7. 简单绘图：绘制气温空间填色图，自动屏蔽缺测 NaN；
8. 输出结果，保存图片与序列数据。

读取 NetCDF 气温场
^^^^^^^^^^^^^^^^^^

✅ **最佳实践**

1. 优先用 ``xarray`` 的 ``xr.open_dataset`` 读取 nc，它会**自动识别缺测 ``_FillValue``** 并转为 NaN、自动解析坐标 ``time/lat/lon``；
2. 读取后 ``print(ds)`` 核对维度顺序，气象场一般为 ``(time, lat, lon)``；
3. 确认气温变量名，检查单位：海量再分析资料默认 **K（开尔文）**，需要转 ℃ 时减 ``273.15``。

.. code-block:: python

   import xarray as xr
   import numpy as np
   import matplotlib.pyplot as plt

   # 读取 nc 文件（实际项目中的项目数据文件）
   ds = xr.open_dataset("temp_field.nc")
   print(ds)                 # 用 print 一眼核对维度、变量、单位、_FillValue

   # 提取气温变量，注意部分数据单位是 K
   temp = ds["temp"]

   # 开尔文 K 转摄氏度 ℃；若数据已经是 ℃，注释掉这一行
   temp = temp - 273.15

   print("气温维度 (time, lat, lon):", temp.shape)

⚠️ **风险点**

- 不看单位直接使用开尔文数值，气温结果完全错误（差 273.15）；
- 忽略 ``_FillValue`` 缺测标识，缺测被当成正常大数值参与计算；
- 维度顺序错乱，``time/lat/lon`` 搞混，切片、平均全部出错。

时间切片（选取指定时间段）
^^^^^^^^^^^^^^^^^^^^^^^^^^

✅ **最佳实践**

用 ``sel()`` 按时间字符串区间切片（``time`` 坐标必须是 datetime 类型）。``slice(start, end)`` 是**左闭右含**的，边界日期本身也会被包含进来。

.. code-block:: python

   # 时间切片：选取 2000-01-01 ~ 2010-12-31
   temp_time_slice = temp.sel(time=slice("2000-01-01", "2010-12-31"))
   print("切片后维度:", temp_time_slice.shape)

⚠️ **风险点**

- 时间字符串格式不匹配（例如写成 ``"2000/01/01"``）会返回空数据；
- ``sel()`` 是按**坐标值**筛选；``isel(time=0)`` 是按**第几个时次**取，只取序号，不做时间筛选。

空间经纬度裁剪，截取研究区域
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

✅ **最佳实践**

用 ``sel + slice`` 裁剪目标经纬度范围。注意 lat 方向：部分再分析资料的纬度是**从大到小（北纬 → 南纬）排列**，此时要写 ``slice(大lat, 小lat)`` 才能取到目标区域。

.. code-block:: python

   # 裁剪研究区域 lon:70-110E ；lat:30-40N
   # 本例样本文件纬度仍为从小到大排列，故写 slice(30, 40)
   temp_region = temp_time_slice.sel(lon=slice(70, 110), lat=slice(30, 40))
   print("裁剪后维度 (time, lat, lon):", temp_region.shape)

⚠️ **风险点**

- lat 上下限写反：若数据集纬度由北向南递减，应写 ``sel(lat=slice(大, 小))``；
- 经纬度超出文件实际范围，裁剪结果全为 NaN，后续平均全是缺测。

纬度加权区域平均【气象核心】
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

✅ **最佳实践**

地球球面网格**越靠两极、面积越小**，直接 ``np.mean`` 算术平均会让高纬格点权重偏大、造成系统偏差。必须用 ``cos(np.radians(lat))`` 作纬度权重（面积正比于 ``cos(lat)``），配合 xarray 内置的 ``.weighted()`` 与方法链 ``.mean(dim=[...])`` 求区域平均，得到一维时间序列。

.. code-block:: python

   # 纬度权重：纬度的弧度余弦，正比于该纬度带的球面宽度
   lat_weight = np.cos(np.radians(temp_region.lat))

   # 纬度加权求区域平均，得到一维时间序列 (time,)
   temp_area_mean = temp_region.weighted(lat_weight).mean(dim=["lat", "lon"])
   print("区域平均气温序列维度:", temp_area_mean.shape)

⚠️ **风险点**

- 直接 ``.mean(dim=["lat","lon"])`` 做算术平均，高纬网格权重偏大，结果有系统偏差——这是气象格点分析最常见的错误之一；
- 使用 ``.weighted()`` 务必保证权重一维坐标与 ``lat`` 对齐，且维度名一致，否则维度不匹配会报错。

空间场切片：取出某一个时刻的空间二维场
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

✅ **最佳实践**

``isel(time=idx)`` 按序号取第 idx 个时次；``sel(time="2001-01-01")`` 按具体日期取，得到 ``(lat, lon)`` 二维空间场。

.. code-block:: python

   # 取第 0 个时刻的 (lat, lon) 二维空间场
   temp_snapshot = temp_region.isel(time=0)
   print("单时刻空间场维度 (lat, lon):", temp_snapshot.shape)

⚠️ **风险点**

误用 ``sel(time=0)`` 把 time 当成数字坐标去匹配，会因坐标中不存在「0」而报错；取时刻序号务必用 ``isel()``。

简单绘图，绘制气温空间填色图
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

✅ **最佳实践**

用 xarray 内置 ``.plot()`` 绘制填色图，它能**自动跳过 NaN 缺测**不渲染。配好 colorbar 标签、标题，保存时用 ``bbox_inches="tight"`` 防止标题被截断，绘图结束 ``plt.close()`` 释放画布。中文标题记得配置中文字体。

.. code-block:: python

   plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]  # 中文字体
   plt.figure(figsize=(8, 5))
   temp_snapshot.plot(cmap="RdBu_r", cbar_kwargs={"label": "气温 ℃"})
   plt.title("某时刻区域气温场")
   plt.savefig("temp_map.png", dpi=150, bbox_inches="tight")
   plt.close()

⚠️ **风险点**

- 不 ``plt.close()``，多次绘图导致多图内容重叠到同一画布；
- 不设置 ``bbox_inches="tight"``，图片标题与坐标标签被截断；
- 不配置中文字体，``plt.title`` 中文渲染成方块。

输出时间序列结果
^^^^^^^^^^^^^^^^

✅ **最佳实践**

xarray 序列 ``.to_dataframe()`` 转成 DataFrame 后用 ``.to_csv`` 导出，可把时间坐标一并保留。

.. code-block:: python

   temp_area_mean.to_dataframe().to_csv("area_mean_temp.csv", encoding="utf-8-sig")

⚠️ **风险点**

``encoding="utf-8-sig"`` 是为了让 Excel 不乱码；若省略则为纯 UTF-8，中文列名在旧版 Excel 中可能乱码。

完整总代码
^^^^^^^^^^

.. code-block:: python

   import xarray as xr
   import numpy as np
   import matplotlib.pyplot as plt

   # ---- 1 读取 NetCDF 气温场 ----
   ds = xr.open_dataset("temp_field.nc")
   print(ds)
   temp = ds["temp"]
   temp = temp - 273.15                      # 单位转换：K → ℃（已是℃则注释）

   # ---- 2 时间切片 ----
   temp_time_slice = temp.sel(time=slice("2000-01-01", "2010-12-31"))

   # ---- 3 空间裁剪（注意 lat 方向，样本文件纬度为从小到大）----
   temp_region = temp_time_slice.sel(lon=slice(70, 110), lat=slice(30, 40))

   # ---- 4 纬度加权区域平均（气象核心，禁止算术平均）----
   lat_weight = np.cos(np.radians(temp_region.lat))
   temp_area_mean = temp_region.weighted(lat_weight).mean(dim=["lat", "lon"])
   print("区域平均气温序列:\n", temp_area_mean)

   # ---- 5 取单个时刻空间场 ----
   temp_snapshot = temp_region.isel(time=0)

   # ---- 6 绘图保存 ----
   plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]  # 中文字体
   plt.figure(figsize=(8, 5))
   temp_snapshot.plot(cmap="RdBu_r", cbar_kwargs={"label": "气温 ℃"})
   plt.title("单时刻区域气温场")
   plt.savefig("temp_map.png", dpi=150, bbox_inches="tight")
   plt.close()

   # ---- 7 输出时间序列 ----
   temp_area_mean.to_dataframe().to_csv("area_mean_temp.csv", encoding="utf-8-sig")

要点总结
^^^^^^^^

1. **NetCDF 读取**：优先用 ``xarray``，自动处理 ``_FillValue`` 缺测；务必核对气温单位，区分开尔文 K 与摄氏度 ℃；
2. **切片原则**：``sel()`` 按坐标值（时间、经纬度），``isel()`` 按数组序号；注意纬度数组排序方向，许多样本数据纬度从北到南递减；
3. **区域平均关键**：气象格点数据**禁止直接算术平均**，必须用纬度余弦 ``cos(lat)`` 加权，消除不同纬度网格面积差异——这是本章最佳实践的物理核心；
4. **NaN 安全**：xarray 运算自动跳过缺测，不要手动填充缺测值；
5. **绘图规范**：配置中文字体、使用 ``bbox_inches="tight"`` 防止标题截断；绘图完成 ``plt.close()`` 释放画布，避免多图重叠；
6. **校验习惯**：每一步 ``print(shape)`` 核对维度 ``(time, lat, lon)``，及时发现维度错乱。

.. seealso:: 术语参考：:doc:`/api/ch08_terms`　·　示例画廊 :doc:`/gallery/auto_examples/plot_numpy/index`。