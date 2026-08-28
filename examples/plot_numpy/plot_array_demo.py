r"""
格点气温场的 NumPy 维度运算
===========================

气象数据在 NumPy 里的标准形态是\ **带维度的三维数组** ``(time, lat, lon)``。
本示例读取项目配套的西北气温格点场，演示两个最常用的维度运算：

1. ``np.mean(axis=0)``——沿时间轴平均，得到 1 月平均气温场 ``(lat, lon)``；
2. ``np.ptp(axis=0)``——沿时间轴求极差，得到逐格点「日际波动幅度」。

两张图分别用 ``pcolormesh`` 展示，经纬度通过 ``extent`` 映射到坐标轴。
数据文件为 ``./data/northwest_temp.nc``，缺失时自动改用同结构的合成场。

需要先下载配套数据文件才能跑出与本书一致的效果，点击下方按钮即可获取：

.. container:: sphx-glr-download meteopy-download-nc

   :download:`下载配套数据文件 northwest_temp.nc </data/northwest_temp.nc>`
"""

# %%
# 
# ① 导入库 + 中文字体配置
import os

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# %%
# 
# ② 读取数据：优先项目配套 NetCDF，缺失时退回合成场
NC_CANDIDATES = ["./data/northwest_temp.nc",
                 "../data/northwest_temp.nc",
                 "../../data/northwest_temp.nc"]

nc_path = next((p for p in NC_CANDIDATES if os.path.exists(p)), None)

if nc_path:
    import xarray as xr

    ds = xr.open_dataset(nc_path)
    # 教学模拟数据：取值 6~18，按课程文档口径以 ℃ 使用
    temp = ds["temp"].values          # (time, lat, lon) ndarray
    lon = ds["lon"].values
    lat = ds["lat"].values
    source = f"配套数据 {nc_path}"
else:
    lon = np.arange(100.0, 110.01, 0.5)      # 与配套文件同结构
    lat = np.arange(30.0, 40.01, 1.0)
    LON, LAT = np.meshgrid(lon, lat)
    rng = np.random.default_rng(2026)
    n_t = 30
    temp = (12 + 0.8 * (LAT - 35) - 0.15 * (LON - 105) ** 2
            + rng.normal(0, 0.3, size=(n_t, len(lat), len(lon))))
    source = "合成场（未找到数据文件）"

print("数据来源：", source)
print("三维场 shape (time, lat, lon):", temp.shape, "dtype:", temp.dtype)

# %%
# 
# ③ 沿时间轴的两种统计：平均场 与 日际波动
# 
# axis=0 对应 time 维；结果都降为二维场 (lat, lon)
mean_field = np.mean(temp, axis=0)      # 1 月平均气温场
range_field = np.ptp(temp, axis=0)      # 逐格点 30 天内最高 - 最低（日际波动幅度）

print("平均场 shape:", mean_field.shape,
      "值域: {:.1f} ~ {:.1f} ℃".format(mean_field.min(), mean_field.max()))
print("波动场 shape:", range_field.shape,
      "值域: {:.1f} ~ {:.1f} ℃".format(range_field.min(), range_field.max()))

# %%
# 
# ④ 绘图：左=1 月平均场，右=日际波动幅度
# 
# pcolormesh 的 extent=[西经, 东经, 南纬, 北纬]，把数组下标映射为经纬度
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5),
                               layout="constrained")

pm1 = ax1.pcolormesh(lon, lat, mean_field, cmap="RdYlBu_r",
                     shading="nearest")
fig.colorbar(pm1, ax=ax1, label="气温 ℃")
ax1.set_xlabel("经度 °E")
ax1.set_ylabel("纬度 °N")
ax1.set_title("2024 年 1 月平均气温场")

pm2 = ax2.pcolormesh(lon, lat, range_field, cmap="YlGnBu",
                     shading="nearest")
fig.colorbar(pm2, ax=ax2, label="气温 ℃")
ax2.set_xlabel("经度 °E")
ax2.set_ylabel("纬度 °N")
ax2.set_title("逐格点日际波动幅度（30 天极差）")

fig.suptitle("NumPy 维度运算：沿时间轴的气温场统计")

plt.show()
