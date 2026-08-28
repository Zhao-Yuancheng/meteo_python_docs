# -*- coding: utf-8 -*-
r"""
全球平均温度距平时间序列与趋势空间分布
======================================

本章目标：用 **HadCRUT5** 数据集绘制逐年全球平均温度距平的时间序列图（X 轴为年份，Y 轴为温度 ℃/K）与全球气温变化趋势的空间分布图（用 contourf 或 pcolormesh）。

这份数据是英国气象局 Hadley 中心 / CRU 提供的逐月 5°×5° 格点距平场。
通过本示例你将掌握：用 xarray 打开 NetCDF、纬度加权的全球平均、
按年聚合、用最小二乘拟合逐年与逐格点的线性趋势，并用 Matplotlib 双图呈现。

数据来源与下载
--------------
HadCRUT5 提供月平均温度距平（相对 1961–1990 年气候基准），变量 tas_mean，
单位 K，逐月格点场。距平的优点是直接表达"这月比常年偏暖还是偏冷"，
不受站网疏密干扰，是研究气候变化的标准数据。

数据可从 HadCRU 官网获取：
``https://crudata.uea.ac.uk/cru/data/temperature/``

本项目已备好 1850–2026 年的版本（约 32 MB），点击下方按钮下载并放在脚本同级目录：

.. container:: sphx-glr-download meteopy-download-nc

   :download:`下载完整代码包（.py + .ipynb + 数据） plot_hadcrut_trend.zip </download/plot_hadcrut_trend.zip>`

也可单独下载数据文件：

.. container:: sphx-glr-download meteopy-download-nc

   :download:`下载 HadCRUT5 逐月距平数据 HadCRUT.5.1.0.0.analysis.anomalies.ensemble_mean.nc </data/HadCRUT.5.1.0.0.analysis.anomalies.ensemble_mean.nc>`

注意：文件约 32 MB，加载稍慢；若下载受限也可用上方官网链接自行获取。
"""

# %%
# 
# ① 导入库 + 中文字体配置
import os

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from cartopy import crs as ccrs

# 中文字体：Windows 微软雅黑/黑体；Linux 文泉驿；macOS 苹方，按系统替换即可。
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "WenQuanYi Micro Hei"]
plt.rcParams["axes.unicode_minus"] = False

# %%
# 
# ② 读取数据
# 
# 路径候选依次覆盖三种运行场景：读者解压 zip 后数据在脚本同级（./xxx.nc）、
# 文档/项目目录下的 data 子目录（./data/xxx.nc）、sphinx-gallery 构建目录（../../data/）。
NC_CANDIDATES = ["./HadCRUT.5.1.0.0.analysis.anomalies.ensemble_mean.nc",
                 "./data/HadCRUT.5.1.0.0.analysis.anomalies.ensemble_mean.nc",
                 "../data/HadCRUT.5.1.0.0.analysis.anomalies.ensemble_mean.nc",
                 "../../data/HadCRUT.5.1.0.0.analysis.anomalies.ensemble_mean.nc",
                 "../../../data/HadCRUT.5.1.0.0.analysis.anomalies.ensemble_mean.nc"]
nc_path = next((p for p in NC_CANDIDATES if os.path.exists(p)), None)

if nc_path:
    try:
        ds = xr.open_dataset(nc_path, engine="netcdf4")
    except Exception:
        ds = xr.open_dataset(nc_path)      # 回退到 xarray 自动选择的引擎
    da = ds["tas_mean"]                     # (time, latitude, longitude) 距平 K
    source = f"HadCRUT5 配套数据 {nc_path}"
else:
    # 兜底：生成结构一致的合成"距平"场，保证脚本任何环境都可演示绘图流程
    time = xr.date_range("1980-01", "2025-12", freq="MS")
    lon  = np.arange(-177.5, 180.0, 5.0)
    lat  = np.arange(-87.5, 90.0, 5.0)
    rng  = np.random.default_rng(2026)
    base = 0.02 * (lat + 45)[:, None]                     # 高纬增暖
    ease = np.linspace(-0.2, 0.9, len(time))[:, None, None]
    da   = xr.DataArray(base + ease +
                        rng.normal(0, 0.15, (len(time), len(lat), len(lon))),
                        dims=["time", "latitude", "longitude"],
                        coords={"time": time, "latitude": lat, "longitude": lon},
                        name="tas_mean")
    source = "合成演示场（未找到数据文件）"

# 统一成短坐标名 lat/lon（HadCRUT5 原生名为 latitude/longitude），方便书写
if {"latitude", "longitude"} <= set(da.dims):
    da = da.rename({"latitude": "lat", "longitude": "lon"})

print("数据来源：", source)
print("场维度:", dict(da.sizes))

# %%
# 
# ③ 转成逐年平均，并剔除不完整的年份
# 
# 数据最后一年（2026）只有 1 个月，直接平均会污染该年结果，需剔除。
# 判据：某年要有 95% 的格点都凑齐 12 个月数据，才认为是"完整年份"。
# （不宜对全体格点取 min——两极、早年探空缺测会让 min 恒为 0；也不宜取 max，
# 单个格点 12 个月就判完整偏宽松。取高分位数在二者间折中。）
annual_spatial = da.groupby("time.year").mean("time", skipna=True)   # (year, lat, lon)
count_annual   = da.groupby("time.year").count("time")
span = count_annual.quantile(0.95, dim=["lat", "lon"])               # 每年"格点月数"的 95 分位
complete_years = span.year.values[span.values >= 12]

annual_spatial = annual_spatial.sel(year=complete_years)
years = annual_spatial["year"].values
print(f"完整年份范围：{years.min()}~{years.max()}，共 {annual_spatial.shape[0]} 年")

# %%
# 
# ④ 全球平均温度距平年序列（纬度加权）
# 
# 每个格点代表的地球表面积正比于 cos(lat)，高纬格点覆盖面积小。
# 若直接算术平均会高估高纬权重，必须做"纬度加权"平均。weighted().mean 遇到
# 缺测时自动对权重归一，结果无系统偏差。
lat_w = np.cos(np.deg2rad(annual_spatial.lat))
global_anomaly = annual_spatial.weighted(lat_w).mean(dim=["lat", "lon"]).values

print("全球平均距平 (℃，相对 1961–1990):", f"{global_anomaly.min():.2f} ~ {global_anomaly.max():.2f}")

# %%
# 
# ⑤ 左图：逐年全球平均温度距平时间序列 + 线性趋势
# 
# numpy.polyfit 最小二乘拟合直线 y = slope*year + intercept，斜率×10 = 每 10 年增暖 ℃。
# 本图分多块构建（左图→趋势计算→右图），中间各块末尾的 defer 标记让截图推迟，
# 待最后一块完成整图再统一保存。
valid = np.isfinite(global_anomaly)
slope, intercept = np.polyfit(years[valid], global_anomaly[valid], 1)
trend_per_10y = slope * 10.0
fit_line = slope * years + intercept
print(f"1850 年以来全球增暖速率 ≈ {trend_per_10y:.2f} ℃/10a（整段拟合）")

fig = plt.figure(figsize=(14, 5.2))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.5], wspace=0.22)
ax1 = fig.add_subplot(gs[0])                     # 左轴：普通坐标轴，画时间序列

ax1.plot(years, global_anomaly, color="tab:blue", linewidth=1.0, alpha=0.85,
         label="全球平均温度距平")
ax1.plot(years, fit_line, color="tab:red", linewidth=2.0, ls="--",
         label=f"线性趋势 {trend_per_10y:.2f} ℃/10a")
ax1.axhline(0, color="k", linewidth=0.8)
ax1.set_xlabel("年份（year）")
ax1.set_ylabel("温度距平（℃，相对 1961–1990）")
ax1.set_title("全球平均温度距平时间序列")
ax1.legend(loc="upper left", fontsize=9)
ax1.grid(True, ls=":", alpha=0.5)
# sphinx_gallery_defer_figures

# %%
# 
# ⑥ 计算每个格点的线性趋势（以近 45 年 1980–2024 为例）
# 
# 对每个 (lat, lon) 格点的逐年序列做线性回归，斜率即该点的增温速率（℃/10a）。
sel = annual_spatial.sel(year=slice(1980, 2024))
y_c, lon_c, lat_c = sel.year.values, sel.lon.values, sel.lat.values
trend_grid = np.full((len(lat_c), len(lon_c)), np.nan)

for i, la in enumerate(lat_c):
    for j, lo in enumerate(lon_c):
        cell = sel.isel(lat=i, lon=j).values
        v = np.isfinite(cell)
        if v.sum() >= 10:                       # 有效年份足够才拟合
            slope_c, _ = np.polyfit(y_c[v], cell[v], 1)
            trend_grid[i, j] = slope_c * 10.0

print("格点趋势范围 (℃/10a):",
      f"{np.nanmin(trend_grid):.2f} ~ {np.nanmax(trend_grid):.2f}")
# sphinx_gallery_defer_figures

# %%
# 
# ⑦ 右图：全球气温变化趋势空间分布
proj = ccrs.PlateCarree()
ax2 = fig.add_subplot(gs[1], projection=proj)   # 右轴：Cartopy 地理投影轴

cf2 = ax2.contourf(lon_c, lat_c, trend_grid, transform=proj, cmap="RdBu_r",
                   levels=15, extend="both")
ct2 = ax2.contour(lon_c, lat_c, trend_grid, transform=proj, colors="k",
                  linewidths=0.6, levels=7)
ax2.clabel(ct2, inline=True, fontsize=6, fmt="%.1f")
ax2.coastlines(resolution="50m", linewidth=0.5, color="gray")
ax2.set_global()
gl2 = ax2.gridlines(crs=proj, draw_labels=True, linewidth=0.5,
                    color="gray", linestyle="--", alpha=0.5, dms=True)
gl2.top_labels = False
gl2.right_labels = False
ax2.set_title("全球气温变化趋势（1980–2024 线性拟合）")

# 给右图（趋势空间分布）配一条专属色标：与左图量纲不同，宜各自独立呈现
cbar2 = fig.colorbar(cf2, ax=ax2, orientation="vertical", pad=0.03,
                     aspect=35, label="趋势（℃/10 a）")
ax1.tick_params(labelsize=9)

print("绘图完成：左图为全球平均距平年序列，右图为格点趋势空间分布。")
plt.show()