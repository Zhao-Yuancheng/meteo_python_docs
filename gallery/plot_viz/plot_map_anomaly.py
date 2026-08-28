# -*- coding: utf-8 -*-
r"""
绘制中国地图上的气温等值线图与距平符号标注（1963 年 1 月）
============================================================

本章目标：
用 ``stipple.nc`` 数据绘制 1963 年 1 月的气温等值线图，并在同一张地图上标注
距平符号：正距平（1963 年 1 月比多年同期偏暖）的格点标 "+"，
负距平（偏冷）的格点标 "-"。

任务分为两层：

#. 底图：用 contourf 填充 1963 年 1 月的气温场 jan1963，直观呈现冷暖分布；
#. 符号：逐格点比较 jan1963 与气候态 climatology，偏暖处画 "+"、偏冷处画 "_"。

本示例综合运用：xarray 读取 NetCDF、Matplotlib 填充等值线、Cartopy 叠加
中国国界（shapefile）、GridSpec 排布主图与色标，以及中国地图惯例的
南海诸岛小图。

所需材料（点击按钮一键下载，含本示例代码、教程版 .ipynb 与全部数据）
----------------------------------------------------------------------

.. container:: sphx-glr-download meteopy-download-nc

   :download:`下载完整代码包（.py + .ipynb + 数据） plot_map_anomaly.zip </download/plot_map_anomaly.zip>`

也可仅下载单个数据文件，与本脚本放在同一目录：

.. container:: sphx-glr-download meteopy-download-nc

   :download:`下载格点温度数据 stipple.nc </data/stipple.nc>`

.. container:: sphx-glr-download meteopy-download-nc

   :download:`下载中国国界 shapefile（4 个文件） </data/china.dbf>`

中国国界 shapefile 实际为 ``china.shp``、``china.shx``、``china.prj``、``china.dbf``
四个配套文件，需一并下载放在同一目录。

数据说明
--------
``stipple.nc`` 是一份全球 73×96 的教学格点场：

* longitude：0°~356.25°，步长 3.75°（从本初子午线向东绕一圈）；
* latitude：90°N~90°S，步长 2.5°（从北极排到南极）；
* jan1963：1963 年 1 月的气温场（℃）；
* climatology：多年 1 月平均的气候态气温场（℃）。

距平（anomaly）＝ jan1963 − climatology，即某时次相对常年同期的偏差：
正距平表示当月较常年偏暖，负距平表示偏冷。
"""

# %%
# 
# ① 导入库 + 中文字体配置
import os

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from cartopy import crs as ccrs
from cartopy import feature as cft
from cartopy.io.shapereader import Reader

# 中文字体：Windows 常见微软雅黑 / 黑体；Linux 常见文泉驿；macOS 常见苹方。
# axes.unicode_minus=False 解决坐标轴负号显示为方块的问题。
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "WenQuanYi Micro Hei"]
plt.rcParams["axes.unicode_minus"] = False

# %%
# 
# ② 读取数据：优先项目配套 NetCDF，缺失时退回合成场 
# 
# 脚本可能在文档构建目录、或读者本地目录运行，逐个尝试常见相对路径：
# 解压下载包后数据在脚本同级（./xxx.nc）→ 项目 data 子目录 → 构建目录。
NC_CANDIDATES = ["./stipple.nc",
                 "./data/stipple.nc",
                 "../data/stipple.nc",
                 "../../data/stipple.nc",
                 "../../../data/stipple.nc"]
nc_path = next((p for p in NC_CANDIDATES if os.path.exists(p)), None)

if nc_path:
    ds = xr.open_dataset(nc_path)
    jan1963_data = ds["jan1963"].values          # 1963 年 1 月气温场 (lat, lon)
    climatology_data = ds["climatology"].values  # 多年 1 月气候态 (lat, lon)
    lon = ds["longitude"].values                 # 0°~356.25°
    lat = ds["latitude"].values                  # 90°N~90°S（北→南）
    source = f"配套数据 {nc_path}"
else:
    # 兜底：数据缺失时生成结构一致的合成场，保证脚本任何环境都能运行
    lon = np.arange(0.0, 357.0, 3.75)
    lat = np.arange(90.0, -90.5, -2.5)
    LON, LAT = np.meshgrid(lon, lat)
    rng = np.random.default_rng(1963)
    climatology_data = 10 + 0.05 * (LAT + 90)                  # 气候态：纬度越高越冷
    jan1963_data = climatology_data + rng.normal(0, 4.0, size=LON.shape)  # 叠加扰动
    source = "合成场（未找到数据文件）"

print("数据来源：", source)
print("jan1963 形状 (纬度数, 经度数):", jan1963_data.shape)

# %%
# 
# ③ 画布布局：GridSpec 把画布切成 20 列
# 
# 本图分多步逐块构建（布局→底图→填色→符号→色标），中间各步先不截图，
# 待最后一步完成再统一保存整图。
# 前 19 列给主图（中国区域），最后 1 列留给竖直色标；
# left/right 控制绘图区的水平范围，wspace 拉大主图与色标的间距。
COLS = 20      # 画布总列数
STEP = 1       # 距平符号的抽稀步长：1 = 逐格点标注；格点太密时可取 2、3

fig = plt.figure(figsize=(8, 6), dpi=300)
gs = fig.add_gridspec(nrows=1, ncols=COLS, left=0.05, right=0.95, wspace=1)
projection = ccrs.PlateCarree()                 # 等经纬度投影，与数据网格一致
ax = fig.add_subplot(gs[:, :COLS - 1], projection=projection)
# sphinx_gallery_defer_figures

# %%
# 
# ④ 主图：中国国界 + 陆海底图 + 经纬网格
# 
# 读取中国国界 shapefile，转为 Cartopy 可叠加的地理要素（只描边界、不填色）
SHP_CANDIDATES = ["./china.shp", "../china.shp", "../../china.shp",
                  "../../data/china.shp", "../../../data/china.shp"]
shp_path = next((p for p in SHP_CANDIDATES if os.path.exists(p)), None)

if shp_path:
    china = cft.ShapelyFeature(Reader(shp_path).geometries(),
                               crs=projection,
                               edgecolor="black",
                               facecolor="none")
else:
    # 兜底：无国界文件时用 Cartopy 自带的 50m 国界线代替
    china = cft.NaturalEarthFeature("cultural", "admin_0_boundary_lines_land",
                                    "50m", edgecolor="black", facecolor="none")
print("国界来源：", shp_path if shp_path else "Cartopy 内置 50m 国界")

ax.add_feature(china, lw=0.5, zorder=2)         # 国界描线，置于气温填色之上

# 经纬网格线：底、左两侧带刻度标签（地图的"轴标签"即经纬度读数）
grid_lines = ax.gridlines(crs=projection,
                          draw_labels={"bottom": "x", "left": "y"},
                          color="gray",
                          linestyle="--",
                          alpha=0.5)

# 陆地 / 海洋底图（50 m 中等分辨率）：随后被气温填色覆盖，仅在图廓边缘露出
ax.add_feature(cft.LAND.with_scale("50m"))
ax.add_feature(cft.OCEAN.with_scale("50m"))

# 限定主图显示范围：中国及周边 [73°E~138°E, 15°N~56°N]
ax.set_extent([73, 138, 15, 56])
# sphinx_gallery_defer_figures

# %%
# 
# ⑤ 南海诸岛小图（中国地图惯例）
# 
# 在主图右下角叠加一个小号地图框放大南海；与主图共用同一份国界要素。
# add_axes 的四个数是 figure 坐标 (左, 下, 宽, 高)，均以 0~1 计。
ax_so = fig.add_axes((0.665, 0.11, 0.31, 0.25), projection=projection)
ax_so.add_feature(china, lw=0.5, zorder=2)
ax_so.add_feature(cft.LAND.with_scale("50m"))
ax_so.add_feature(cft.OCEAN.with_scale("50m"))
ax_so.set_extent([105, 125, 0, 25])
# sphinx_gallery_defer_figures

# %%
# 
# ⑥ 填充等值线：1963 年 1 月气温场
# 
# 主图与小图画同一份数据；coolwarm 蓝冷红暖，与气温直觉一致；
# extend="max" 表示超出填色上限的值用最深色一并表示。
contourf = ax.contourf(lon, lat, jan1963_data,
                       cmap="coolwarm",
                       transform=ccrs.PlateCarree(),
                       extend="max")
contourf_so = ax_so.contourf(lon, lat, jan1963_data,
                             cmap="coolwarm",
                             transform=ccrs.PlateCarree(),
                             extend="max")
# sphinx_gallery_defer_figures

# %%
# 
# ⑦ 逐格点判定距平正负，收集要标注的经纬度
# 
# 距平 = jan1963 − climatology：差为正即偏暖（标 +），为负即偏冷（标 _）。
# 双重循环按 STEP 步长遍历全部格点；二维数组按 [纬度下标][经度下标] 取值。
# 全部格点都参与判定，显示范围由 set_extent 裁剪，因此只看得到中国附近。
pos_lon, pos_lat = [], []     # 正距平（偏暖）格点的经 / 纬度
neg_lon, neg_lat = [], []     # 负距平（偏冷）格点的经 / 纬度

for lon_idx in range(0, len(lon), STEP):
    for lat_idx in range(0, len(lat), STEP):
        if jan1963_data[lat_idx][lon_idx] > climatology_data[lat_idx][lon_idx]:
            pos_lon.append(lon[lon_idx])
            pos_lat.append(lat[lat_idx])
        elif jan1963_data[lat_idx][lon_idx] < climatology_data[lat_idx][lon_idx]:
            neg_lon.append(lon[lon_idx])
            neg_lat.append(lat[lat_idx])

print(f"正距平格点数：{len(pos_lon)}，负距平格点数：{len(neg_lon)}")
# sphinx_gallery_defer_figures

# %%
# 
# ⑧ 主图散点：+ 偏暖 / _ 偏冷
# 
ax.scatter(pos_lon, pos_lat, transform=ccrs.PlateCarree(),
           color="black", marker="+", s=16, label="正距平（偏暖）")
ax.scatter(neg_lon, neg_lat, transform=ccrs.PlateCarree(),
           color="black", marker="_", s=16, label="负距平（偏冷）")
ax.legend(loc="lower left", fontsize=8)
# sphinx_gallery_defer_figures

# %%
# 
# ⑨ 色标：挂在 GridSpec 预留的最后一列
# 
cax = fig.add_subplot(gs[:, COLS - 1:])
cbar = fig.colorbar(contourf, cax=cax)
cbar.set_label("1963 年 1 月气温（℃）")
# sphinx_gallery_defer_figures

# %%
# 
# ⑩ 小图散点（符号缩小）与总标题
ax_so.scatter(pos_lon, pos_lat, transform=ccrs.PlateCarree(),
              color="black", marker="+", s=8)
ax_so.scatter(neg_lon, neg_lat, transform=ccrs.PlateCarree(),
              color="black", marker="_", s=8)

ax.set_title("1963 年 1 月中国气温分布与距平符号标注", fontsize=12)

print("绘图完成：主图为气温填色 + 距平符号，右下角为南海诸岛小图。")

plt.show()
