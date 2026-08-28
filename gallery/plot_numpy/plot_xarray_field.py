# -*- coding: utf-8 -*-
r"""
Xarray 西北气温场分析
=====================

本章目标：用 Xarray 读取项目配套的 NetCDF 气温场，对其进行\ **时间切片**、
**空间子区域裁剪**，并做\ **纬度加权区域平均**，最后画出「某时刻空间气温场 +
区域平均时间序列」两张图，贯穿项目第 8 步。

数据文件为 ``./data/northwest_temp.nc``（2024 年 1 月 1–30 日、经度
100–110°E、纬度 30–40°N 的教学模拟格点场，变量 ``temp`` 单位 ℃、
``pres`` 单位 hPa）。用 ``open_dataset`` 读取时，xarray 会自动解析
time/lat/lon 坐标并识别缺测 ``_FillValue``。文件不在时自动改用结构
一致的合成场，保证脚本在任何环境都能运行。

需要先下载配套数据文件才能跑出与本书一致的效果，点击下方按钮即可获取：

.. container:: sphx-glr-download meteopy-download-nc

   :download:`下载配套数据文件 northwest_temp.nc </data/northwest_temp.nc>`
"""

# %%
# 
# ① 导入库 + 中文字体配置
# 
import os

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]  # 中文字体
plt.rcParams["axes.unicode_minus"] = False                        # 负号正常显示

# %%
# 
# ② 读取数据：优先项目配套 NetCDF，缺失时退回合成场
# 
# 依次尝试三个候选路径：项目根目录运行、画廊构建目录运行、独立运行。
NC_CANDIDATES = ["./data/northwest_temp.nc",
                 "../data/northwest_temp.nc",
                 "../../data/northwest_temp.nc"]

nc_path = next((p for p in NC_CANDIDATES if os.path.exists(p)), None)

if nc_path:
    ds = xr.open_dataset(nc_path)
    # 教学模拟数据：取值 6~18，按课程文档口径以 ℃ 使用
    da_c = ds["temp"]
    source = f"配套数据 {nc_path}"
else:
    lon = np.arange(100.0, 110.01, 0.5)        # 与配套文件同结构
    lat = np.arange(30.0, 40.01, 1.0)
    time = np.arange("2024-01-01", "2024-01-31", dtype="datetime64[D]")
    LON, LAT = np.meshgrid(lon, lat)
    rng = np.random.default_rng(2026)
    field = (12 + 0.8 * (LAT - 35) - 0.15 * (LON - 105) ** 2
             + rng.normal(0, 0.3, size=(len(time), len(lat), len(lon))))
    da_c = xr.DataArray(
        data=field,
        dims=["time", "lat", "lon"],
        coords={"time": time, "lat": lat, "lon": lon},
        name="temp",
        attrs={"long_name": "2m 空气温度", "units": "degC",
               "source": "合成演示数据"},
    )
    source = "合成场（未找到数据文件）"

print("数据来源：", source)
print("读取完成 shape(time, lat, lon):", da_c.shape)

# %%
# 
# ③ 时间切片：只保留 2024 年 1 月中旬（1-11 至 1-20）
da_season = da_c.sel(time=slice("2024-01-11", "2024-01-20"))
print("时间切片后 shape:", da_season.shape)

# %%
# 
# ④ 空间子区域裁剪：聚焦西北地区东部
# 
# lon 102–108°E, lat 33–39°N（本例 lat 从小到大排列，故 slice(33, 39)）
da_region = da_season.sel(lon=slice(102, 108), lat=slice(33, 39))
print("空间裁剪后 shape:", da_region.shape)

# %%
# 
# ⑤ 纬度加权区域平均（气象核心，禁止算术平均）
# 
# 球面格点面积正比于 cos(lat)，高纬格点面积更小，直接平均会造成系统偏差
lat_weight = np.cos(np.radians(da_region.lat))
series = da_region.weighted(lat_weight).mean(dim=["lat", "lon"])
print("纬度加权区域平均时间序列维度:", series.shape)
print("区域平均气温(℃)序列前 5 个时次:")
print(series.values[:5])

# %%
# 
# ⑥ 绘图：左=某时刻空间气温场，右=区域平均时间序列
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5),
                               layout="constrained")

# 左图：取裁剪区域内第 0 个时次的空间场（lat, lon）
da_region.isel(time=0).plot(ax=ax1, cmap="RdBu_r",
                            cbar_kwargs={"label": "气温 ℃"})
ax1.set_title("2024-01-11 西北东部气温场")

# 右图：纬度加权区域平均的时间序列
ax2.plot(series.time.astype("datetime64[D]").astype(str), series.values,
         marker="o", color="tab:red")
ax2.set_title("纬度加权区域平均气温时间序列")
ax2.set_ylabel("气温 ℃")
ax2.set_xlabel("日期")
ax2.tick_params(axis="x", rotation=30)

fig.suptitle("Xarray 西北气温场分析示例")

# 关键结果打印，便于校验
print("区域平均气温变化范围 (℃):",
      f"{float(series.min()):.1f} ~ {float(series.max()):.1f}")

plt.show()
