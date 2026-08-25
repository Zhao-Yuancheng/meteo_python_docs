r"""
气温场等值线分析（纯 Matplotlib）
============================================================

``contourf`` + ``contour`` 是气象场可视化的经典组合：填色看分布、
等值线读数值。本示例绘制西北地区 2024 年 1 月平均气温场：

1. ``contourf`` 填色，``levels`` 显式指定等值线间隔；
2. ``contour`` 叠加同层等值线，``clabel`` 在线上标注数值；
3. 标注兰州观测站，演示散点与文字在场图上的叠加。

与 Cartopy 示例的区别：这里不涉及地图投影，坐标轴直接就是经纬度——
适合快速查看格点场；需要地图要素（海岸线、国界）时再用 Cartopy。
数据文件为 ``./data/northwest_temp.nc``，缺失时自动改用同结构的合成场。
"""

# %%
# ---------- ① 导入库 + 中文字体配置 ----------
import os

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# %%
# ---------- ② 读取数据：优先项目配套 NetCDF，缺失时退回合成场 ----------
NC_CANDIDATES = ["./data/northwest_temp.nc",
                 "../data/northwest_temp.nc",
                 "../../data/northwest_temp.nc"]

nc_path = next((p for p in NC_CANDIDATES if os.path.exists(p)), None)

if nc_path:
    import xarray as xr

    ds = xr.open_dataset(nc_path)
    # 教学模拟数据：取值 6~18，按课程文档口径以 ℃ 使用
    temp = ds["temp"].mean(dim="time")      # 1 月 30 天平均 -> (lat, lon)
    lon, lat = ds["lon"].values, ds["lat"].values
    source = f"配套数据 {nc_path}"
else:
    lon = np.arange(100.0, 110.01, 0.5)      # 与配套文件同结构
    lat = np.arange(30.0, 40.01, 1.0)
    LON, LAT = np.meshgrid(lon, lat)
    temp = 12 + 0.8 * (LAT - 35) - 0.15 * (LON - 105) ** 2
    source = "合成场（未找到数据文件）"

print("数据来源：", source)
print("气温范围：{:.1f} ~ {:.1f} ℃".format(float(temp.min()),
                                        float(temp.max())))

# %%
# ---------- ③ 绘制填色场 + 等值线 + 站点标注 ----------
# levels 显式指定：从整 2 ℃ 起画，保证等值线数值"好读"
vmin, vmax = float(temp.min()), float(temp.max())
levels = np.arange(np.floor(vmin / 2) * 2, vmax + 2, 2)

fig, ax = plt.subplots(figsize=(9, 5.5))

# 填色场：contourf 用同一组 levels，颜色与等值线一一对应
cf = ax.contourf(lon, lat, temp, levels=levels, cmap="RdYlBu_r",
                 extend="both")

# 等值线：单色细线叠加在填色场之上，clabel 标注每条线的数值
cs = ax.contour(lon, lat, temp, levels=levels, colors="k",
                linewidths=0.6)
ax.clabel(cs, fmt="%.0f", fontsize=8)

# 兰州站标注：lon=103.83°E, lat=36.06°N
ax.scatter(103.83, 36.06, c="black", marker="*", s=90, zorder=5)
ax.text(104.1, 36.06, "兰州站", fontsize=9, va="center")

# 坐标轴与色标
ax.set_xlabel("经度 °E")
ax.set_ylabel("纬度 °N")
ax.set_title("西北地区 2024 年 1 月平均气温（等值线间隔 2 ℃）")
cbar = fig.colorbar(cf, ax=ax)
cbar.set_label("气温 ℃")

plt.show()
