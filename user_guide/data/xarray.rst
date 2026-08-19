.. _tut-xarray:

气象数据分析（二）Xarray
========================

第 8 节 · 模块二 气象数据处理
贯穿项目第 8 步：用 Xarray 读取 NetCDF 再分析气温场，做区域平均与时间切片。

除了站点观测这类「表格」数据，气象里更常见的是**格点数据**——数值模式输出、卫星反演、再分析资料，本质都是**多维数组**：经度、纬度、高度、时间……维度一多，Pandas 的二维 DataFrame 就力不从心了。你总不能记着 ``temp[:, :, 0, :]`` 里第几个冒号是高度、第几个是纬度。

Xarray 正是为解决「多维标记数组」而生：它给 NumPy 数组的每个**轴贴上维度名**、每根轴标上**坐标值**，于是取数不再靠「数第几个」，而是直接说「取纬度 36°N 上」——这就是 :term:`DataArray` 与 :term:`Dataset` 的全部魔法所在。它对 NetCDF、GRIB、Zarr 等气象标准格式原生友好，可以把它当作「多维的 Pandas」。

先看一眼（感受「按名字取数」与「按位置取数」的差别）：

.. code-block:: python

   import numpy as np
   import xarray as xr

   da = xr.DataArray(
       np.random.randn(5, 8) + 15,          # 5 个纬度 × 8 个经度的一张小气温场
       dims=["lat", "lon"],
       coords={"lat": np.linspace(20, 50, 5), "lon": np.linspace(70, 140, 8)},
       name="t2m",
   )
   da.attrs["units"] = "°C"
   print(da.sel(lat=36, method="nearest"))   # 一句话取最接近 36°N 的那一条纬带

本章主线（贯穿项目第 8 步）：读取一份西北地区 NetCDF 再分析气温场——核对维度与单位、时间切片、空间裁剪、纬度加权区域平均、单时刻切片、简单绘图。这些动作正是气候与天气分析的基本功。

本章将覆盖的知识点：DataArray / Dataset、坐标与维度、``sel`` / ``isel``、``open_dataset``、简单绘图；提升拓展：``groupby`` 时间分组、``resample`` 重采样、加权平均。文中 :term:`重采样 resample`、:term:`属性 attrs` 等关键词可跳转术语参考。

8.1 DataArray 与 Dataset：带标签的多维数组
-------------------------------------------

Xarray 有两大核心数据结构，一句话分清：**DataArray = 一个带标签的多维变量；Dataset = 一串共享坐标的 DataArray 打包**。

.. list-table::
   :header-rows: 1

   * - 数据结构
     - 一句话
     - 类比
   * - :term:`DataArray`
     - 带坐标的多维数组，装**一个**气象变量
     - Pandas 的 Series（但可以 N 维）
   * - :term:`Dataset`
     - 装**多个**共享维度/坐标的变量
     - Pandas 的 DataFrame（但支持多维）

8.1.1 DataArray：给数字贴上标签
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import numpy as np
   import pandas as pd
   import xarray as xr

   # 3 站点 × 4 时次的气温数据
   data = np.array([
       [22.5, 23.1, 24.0, 22.8],
       [25.6, 26.2, 27.1, 26.5],
       [19.8, 20.3, 21.0, 20.5],
   ])
   da = xr.DataArray(
       data,
       dims=["站点", "时间"],                                  # 维度名
       coords={
           "站点": ["北京", "上海", "广州"],                   # 维度坐标
           "时间": pd.date_range("2026-08-14", periods=4),     # 时间坐标
       },
       name="气温",
       attrs={"单位": "°C", "说明": "逐日最高气温"},           # 元信息
   )
   print(da)

.. code-block:: text

   <xarray.DataArray '气温' (站点: 3, 时间: 4)>
   array([[22.5, 23.1, 24. , 22.8],
          [25.6, 26.2, 27.1, 26.5],
          [19.8, 20.3, 21. , 20.5]])
   Coordinates:
     * 站点     (站点) <U2 '北京' '上海' '广州'
     * 时间     (时间) datetime64[ns] 2026-08-14 ... 2026-08-17

.. admonition:: 四个常用属性

   - ``da.values``：底层 NumPy 数组；
   - ``da.dims``：维度名元组，如 ``('站点', '时间')``；
   - ``da.coords``：所有坐标；
   - ``da.attrs``：元信息字典（单位、说明等），见 :term:`属性 attrs`。

8.1.2 Dataset：一整本气象档案册
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

同一个 NetCDF 里通常同时装着气温、降水、气压好几个变量，用 :term:`Dataset` 装最自然：

.. code-block:: python

   ds = xr.Dataset(
       {
           "气温":   (["站点", "时间"], data),
           "降水量": (["站点", "时间"], np.array([[0.0, 3.5, 0.0, 0.0],
                                                 [0.0, 0.0, 12.1, 5.0],
                                                 [0.0, 0.0, 0.0, 0.0]])),
           "气压":   (["站点", "时间"], np.array([[1013, 1012, 1011, 1013],
                                                 [1008, 1007, 1006, 1008],
                                                 [1015, 1014, 1013, 1015]])),
       },
       coords={
           "站点": ["北京", "上海", "广州"],
           "时间": pd.date_range("2026-08-14", periods=4),
       },
   )

   print(ds["气温"])     # 字典式访问变量
   print(ds.气压)        # 属性式访问（点号）同样可行

8.2 坐标与维度：Xarray 的「灵魂」
----------------------------------------------------

把 :term:`维度 dim` 与 :term:`坐标 coords` 分清，是高效用 Xarray 的第一关：

- **维度（dim）**：轴的名字。``ds.dims`` 打印出 ``{'站点': 3, '时间': 4}``，只说明「沿哪个方向、有多少格」，不含具体数值；
- **坐标（coords）**：轴上每个位置的具体取值。``ds.coords`` 打印出每个站点叫什么、每个时间是哪一天。

.. code-block:: python

   print(ds.dims)     # {'站点': 3, '时间': 4}        轴的名字 + 长度
   print(ds.站点)     # ['北京', '上海', '广州']       轴上的真实取值
   print(ds.coords)   # 所有坐标一览

有了坐标，索引就不用记「第几个」了——直接 ``ds.sel(时间="2026-08-15")`` 按名字抓，这在动辄四维（时间×高度×纬度×经度）的气象数据里，意义不是好看，而是**不犯错**。

8.3 数据读取：open_dataset 与惰性加载
-------------------------------------

气象格点数据最常见格式是 **NetCDF** （后缀 ``.nc``，:term:`NetCDF` 词条讲清了它为什么是「密封档案盒」）。Xarray 的 ``xr.open_dataset`` 是读取的标准入口：

.. code-block:: python

   # 读取单个 NetCDF 文件
   ds = xr.open_dataset("era5_temperature_2026.nc")

   # 实际生产中的推荐参数
   ds = xr.open_dataset(
       "era5_temperature_2026.nc",
       engine="netcdf4",          # 可选：netcdf4 / h5netcdf / cfgrib
       decode_times=True,         # 自动解析时间坐标
       chunks={"time": 10},       # 分块读取（配合 Dask 用在大文件上）
   )
   print(ds)

.. code-block:: text

   <xarray.Dataset>
   Dimensions:    (time: 365, level: 37, latitude: 721, longitude: 1440)
   Coordinates:
     * time       (time) datetime64[ns] 2026-01-01 ... 2026-12-31
     * level      (level) int32 1000 975 950 925 900 ... 50 30 20 10
     * latitude   (latitude) float32 90.0 89.75 89.5 ... -89.5 -89.75 -90.0
     * longitude  (longitude) float32 0.0 0.25 0.5 ... 359.5 359.75
   Data variables:
       t          (time, level, latitude, longitude) float32 ...

.. admonition:: 惰性加载（Lazy Loading）——大文件的关键

   ``open_dataset`` **默认不把数据读进内存**，只读维度、坐标、属性这些「目录」。真正要算时才加载：

   .. code-block:: python

      ds = xr.open_dataset("large_file.nc")
      print(ds)          # 很快——此刻只是看了目录
      ds.load()          # 这一行才真正把数据搬进内存

   这对 GB 乃至 TB 级的格点数据至关重要：你先看一眼结构再决定取哪些，不会一上来就把内存撑爆。

8.4 索引与筛选：sel 与 isel
----------------------------

和 Pandas 的 ``loc``/``iloc`` 一一对应，Xarray 给了两套按维度取数的方法：

.. list-table::
   :header-rows: 1

   * - 方法
     - 按什么取
     - 对应 Pandas
   * - ``.sel(...)``
     - 按**坐标值**（时间、经纬度）
     - ``.loc``
   * - ``.isel(...)``
     - 按**数组序号**（第几个）
     - ``.iloc``

8.4.1 按坐标值取：sel
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   ds.sel(时间="2026-08-15")                              # 取某一天
   ds.sel(时间=slice("2026-08-14", "2026-08-16"))         # 取时间范围（含两端）
   ds.sel(站点="上海")                                    # 取某个站
   ds.sel(站点=["北京", "广州"], 时间=slice("2026-08-15", "2026-08-17"))
   ds.sel(时间="2026-08-14 12:00:00", method="nearest")   # 坐标没有精确值时取最近

8.4.2 按位置取：isel
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   ds.isel(时间=0)                 # 第 0 个时间步
   ds.isel(站点=1)                 # 第 1 个站点
   ds.isel(时间=slice(0, 2))       # 前 2 个时间步
   ds.isel(站点=[0, 2], 时间=[1, 3])

.. warning::

   也别小看方括号：``da[0, 1]`` 用的是位置，可读性差，还容易数错维度。**气象工作流的铁律：一律用 ``sel``/``isel`` 搭配维度名**，别依赖维度顺序。

8.5 简单绘图
------------

Xarray 内置基于 Matplotlib 的一行绘图，快速「看数据」极其方便：

.. code-block:: python

   import matplotlib.pyplot as plt

   ds["气温"].isel(站点=0).plot()               # 一维折线：北京站时间序列
   plt.title("北京站逐日最高气温"); plt.show()

   # 二维空间场填色（假设有格点数据 ds_grid：time, lat, lon）
   ds_grid["t"].isel(time=0).plot(
       figsize=(10, 6), cmap="RdBu_r",
       cbar_kwargs={"label": "温度 (°C)"},
   )
   plt.title("2026-08-14 地面气温空间分布"); plt.show()

   ds["气温"].plot(col="站点", marker="o")      # 按站点分面
   ds["气温"].plot.hist(bins=20)                # 直方图看分布

常用参数：``col``/``row`` 分面、``cmap`` 色带、``cbar_kwargs`` 色标、``marker`` 折线记号。更专业的绘图（地图投影等）留给模块三。

8.6 提升拓展（一）：groupby 时间分组
-------------------------------------

与 Pandas 的 :term:`分组聚合` 类似，Xarray 的 ``groupby`` 可沿坐标分组聚合，是气候统计的常客——比如算多年各月平均（气候态）。

.. code-block:: python

   # 按月份分组：逐月气候平均 / 标准差
   monthly_clim = ds.groupby("time.month").mean()
   monthly_std  = ds.groupby("time.month").std()

   # 按「一年中的第几天」分组：逐日气候态，再算每一天的距平（Anomaly）
   clim      = ds.groupby("time.dayofyear").mean()
   anomaly   = ds.groupby("time.dayofyear") - clim
   print(anomaly)

8.6.1 自定义分组：季节
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def get_season(month):
       if month in [12, 1, 2]: return "DJF"    # 冬
       if month in [3, 4, 5]:  return "MAM"    # 春
       if month in [6, 7, 8]:  return "JJA"    # 夏
       return "SON"                             # 秋

   seasonal = ds.groupby(ds.time.dt.month.map(get_season)).mean()
   print(seasonal)

.. note:: 常用时间属性（经 ``.dt`` 访问）：``.year`` / ``.month`` / ``.day`` / ``.dayofyear``（一年第几天）/ ``.season`` / ``.quarter``。

8.7 提升拓展（二）：resample 重采样
-------------------------------------

:term:`重采样 resample` 只针对**时间维度**做频率聚合，可降采样（日→月）也可升采样（月→日）。

.. code-block:: python

   # 降采样：日 → 月平均、月降水总量、年最大值
   ds_month    = ds.resample(time="ME").mean()      # ME=月末间隔
   precip_month = ds["降水量"].resample(time="ME").sum()
   max_annual  = ds["气温"].resample(time="YE").max()     # YE=年末

   # 升采样（会引入缺失，需填充或插值）：月 → 日
   ds_daily_ffill  = ds_month.resample(time="D").ffill()           # 向前填充
   ds_daily_lin    = ds_month.resample(time="D").interpolate("linear")   # 线性插值

.. admonition:: 常用频率串

   ``"D"`` 日、``"W"`` 周、``"ME"`` 月末（新版本优先于 ``"M"``）、``"MS"`` 月初、``"YE"`` 年末、``"H"`` 时、``"5D"`` 候（5 天）。

8.8 提升拓展（三）：面积加权平均【气象核心】
---------------------------------------------

地球是球体——同一份经纬网里，**越靠两极的网格面积越小**。直接对格点做算术平均，会高估极地地区（网格多但占比小）的贡献，产生系统偏差。因此计算区域平均气温的标准做法，是用 ``cos(lat)`` 当作纬度权重（面积正比于该纬度带的球面宽度）。

.. code-block:: python

   # 假设 ds 含格点变量 t，维度 (time, lat, lon)
   weights = np.cos(np.deg2rad(ds.lat))            # 纬度权重：cos(lat 弧度)
   weights = weights.broadcast_like(ds["t"])       # 扩展到与数据同形状

   # 方法一：.weighted() 内置加权平均
   area_avg = ds["t"].weighted(weights).mean(dim=["lat", "lon"])

   # 方法二：等价的手写加权（概率论的加权均值公式）
   area_avg2 = (ds["t"] * weights).sum(dim=["lat", "lon"]) / weights.sum(dim=["lat", "lon"])

.. admonition:: Xarray 官方示例

   .. code-block:: python

      air = xr.tutorial.load_dataset("air_temperature")
      w = np.cos(np.deg2rad(air.lat))
      air_weighted = air["air"].weighted(w).mean(dim=["lat", "lon"])
      print(air_weighted)

   权重数组必须是 DataArray，且不能含缺失值（有缺失可用 ``weights.fillna(0)``）。这是本章**最值得记住的物理要点**——直接算术平均是气象格点分析最常见错误之一。

8.9 综合实战：ERA5 格点气温分析
--------------------------------

串起全章的完整任务：**读取 ERA5 逐日气温，计算夏季（JJA）区域平均气温的逐年变化趋势**。

.. code-block:: python

   import numpy as np
   import xarray as xr
   import matplotlib.pyplot as plt

   # 1. 读取多年逐日再分析数据
   ds = xr.open_dataset("era5_t2m_2010_2020.nc")
   print(ds)   # time: 4015, latitude: 181, longitude: 360

   # 2. 单位换算：开尔文 → 摄氏度
   ds["t2m"] = ds["t2m"] - 273.15

   # 3. 筛选夏季月份（6、7、8 月）
   ds_summer = ds.isel(time=ds.time.dt.month.isin([6, 7, 8]))

   # 4. 纬度权重
   w = np.cos(np.deg2rad(ds.latitude)).broadcast_like(ds["t2m"])

   # 5. 先做区域（空间）加权平均 → 得到逐日的区域平均气温序列
   #    再按年份分组取平均 → 得到逐年 JJA 区域平均
   daily_series   = ds_summer["t2m"].weighted(w).mean(dim=["latitude", "longitude"])
   yearly_summer  = daily_series.groupby("time.year").mean()
   print(yearly_summer)

   # 6. 逐年变化趋势
   yearly_summer.plot(marker="o", figsize=(10, 5))
   plt.xlabel("年份"); plt.ylabel("夏季平均气温 (°C)")
   plt.title("2010–2020 年夏季区域平均气温变化"); plt.grid(True); plt.show()

   # 7. 结果存回 NetCDF，供后续分析或画图复用
   yearly_summer.to_netcdf("summer_temp_trend.nc")

.. admonition:: 一步一线索（读这段代码的顺序）

   第 4–5 行是核心：先**空间**压缩（纬度加权平均）把三维压成一维时间序列，再**时间**分组（按年取平均）得到逐年值。两层「平均」完全正交：一个是经纬加权、一个是年份分组。

8.10 常见陷阱与性能优化
-----------------------

1. **永远不要依赖维度顺序**：``ds["t"][:, 0, :]`` 鬼知道第 2 维是什么，请写 ``ds["t"].isel(level=0)``；
2. **先核对单位再动手**：再分析资料气温默认开尔文 K，减 ``273.15`` 才是 ℃——不核对单位，结果整体差出两百多度；
3. **大文件配合 Dask 分块**：``xr.open_dataset("huge.nc", chunks={"time": 10})`` 惰性加载、按需计算；
4. **坐标对齐产生的 NaN**：两个 Dataset 合并时维度不完全一致会在错格点处产生 NaN，显式 ``ds1.reindex_like(ds2, method="nearest")`` 可对齐；
5. **区域平均必须纬度加权**：见 8.8，禁止算术平均，防止高纬网格权重虚高。

读取、切片、加权平均、绘图、导出的**全套工程化流程与雷区**，见下节最佳实践。

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

.. seealso:: 术语参考：:doc:`/api/ch08_terms`　·　示例画廊 :doc:`/gallery/plot_numpy/index`。