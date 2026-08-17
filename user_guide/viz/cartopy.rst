.. _tut-cartopy:

气象数据绘图（二）Cartopy
=========================

第 10 节 · 模块三 气象数据可视化
贯穿项目第 10 步：绘制西北地区气温空间分布图（等值线填色 + 海岸线）。

Cartopy 概述与选取理由
----------------------

为什么气象格点绘图选用 Cartopy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

把一张气温「表格」变成一张「地图」，比想象中要难得多——地球是个球，纸是平的。气象格点数据里的每一个温度，都带着它的经纬度「身份证」；而 Cartopy 就是那个能帮你把球面上的数据摊平到纸面上、还不至于画得面目全非的「绘图地图册」。

1. 原生适配气象科研场景：Cartopy 专为地球地理坐标系设计，完美对接 NetCDF 再分析气温场、区域气候模拟数据，内置经纬度坐标转换逻辑，无需手动做坐标换算。

2. 内置全球地理矢量要素：自带有海岸线、国界、省界、河流、湖泊等 Natural Earth 地理数据，无需再费劲下载地图底图 shp 文件。

3. 多类地图投影完整支持：涵盖气象绘图最常用的等经纬度投影、墨卡托、兰伯特等面积投影，适配全球、中国区域、西北区域不同绘图需求。

4. 与 Matplotlib 无缝联动：Cartopy 基于 Matplotlib 二次开发，可直接复用 ``contourf``、``contour``、``quiver``、``colorbar`` 等绘图接口，与前文 Matplotlib 绘图语法完全统一，学习成本更低。

5. 适配本项目实战目标：本章核心任务绘制**西北地区气温空间填色分布图**，Cartopy 是完成该图的标准工业工具，也是大气科学专业毕业论文、期刊附图的通用绘图库。

本章承接贯穿项目说明
^^^^^^^^^^^^^^^^^^^^

本章为整套《兰州气温观测数据分析与可视化系统》的最终可视化章节，承接前文全部内容：

1. **数据来源**：T-001 统一提供西北地区 NetCDF 气温格点数据（Xarray 读取逻辑见第 8 章）；

2. **前置基础**：第 6 章 NumPy 数组运算、第 8 章 Xarray 格点数据切片、第 9 章 Matplotlib 画布与子图语法；

3. **本章产出**：完整西北地区气温等值线填色地图，包含投影转换、地理边界、色标、标题、坐标刻度等完整要素，可直接作为项目报告附图；

4. **全书闭环逻辑**：环境搭建 → 基础语法 → 数据处理 → 数值计算 → 表格分析 → 格点读取 → 空间地图可视化。

本章学习目标
^^^^^^^^^^^^

1. 理解地图投影原理，区分气象常用的 3 种投影适用场景；

2. 掌握 Cartopy 创建地理画布、绑定坐标变换 ``transform`` 参数；

3. 学会叠加海岸线、国界、区域边界等地理矢量要素；

4. 使用 ``contourf`` 完成气温场等值线填色，配置配套色标 ``colorbar``；

5. 限定绘图区域裁剪西北地区范围，输出规范科研风格地图；

6. 拓展：绘制风场矢量、兰伯特投影切换、批量逐月绘图、分季节多子图对比。

基础概念与核心组件
------------------

核心基础名词解释
^^^^^^^^^^^^^^^^

1. **地图投影**：把三维球面的经纬度数据映射到二维平面画布的数学变换。你可以把地球想象成一张橘子皮——想把它完整摊平在桌上，四周就会裂开、变形，这种「摊平」就是投影。不同投影会产生不同形变，气象绘图需根据研究区域选择对应投影。

2. **transform 坐标变换**：NetCDF 数据默认是球面地理坐标（带「经纬度标签」），而画布是平面像素坐标。``transform`` 就像给一个个散落的格点贴上经纬度标签，告诉 Cartopy「这份数据真实的家在哪里」，只有这样才能把数据准确「贴在」地图上。**这一步最容易被遗漏。**

3. **GeoAxes**：Cartopy 专用的地理坐标轴，替代普通 Matplotlib 的 Axes，自带经纬度刻度、地理要素加载能力。

4. **Natural Earth**：开源免费的全球地理矢量数据集，Cartopy 内置自动调用，首次使用会自动下载，无需手动找 shp 文件。

气象绘图三大主流投影详解
^^^^^^^^^^^^^^^^^^^^^^^^

（1）PlateCarree 等经纬度投影（日常最常用）

- 特点：经纬线互相垂直，无角度形变，经纬度刻度均匀分布，「横平竖直、简单直观」；
- 适用场景：全球大范围图、中国区域、西北地区气温填色图（本项目统一使用）；
- 代码创建方式：``ccrs.PlateCarree()``。

（2）Mercator 墨卡托投影

- 特点：保证角度不变（等角投影），船舶航线画成直线，但高纬度区域面积被严重拉伸——格陵兰在图上大得像整个非洲；
- 适用场景：航海图、低纬度区域气候图，**不推荐**做中高纬度气象场绘图。

（3）LambertAzimuthalEqualArea 兰伯特等面积投影

- 特点：区域面积无畸变（等面积投影），中心区域形变最小；
- 适用场景：中纬度区域气候、季风、区域气候模拟（如东亚、西北干旱区专题图）；
- 拓展内容会提供西北区域专用的兰伯特投影配置代码。

.. note::

   一句话记忆：**PlateCarree 图省事、Mercator 保角度、Lambert 保面积**。日常西北气温图用 PlateCarree 就够；做区域面积对比专题时再请出兰伯特。

Cartopy 标准绘图固定流程
^^^^^^^^^^^^^^^^^^^^^^^^

完整标准化流程，本章所有示例、练习统一遵循（编号与后续各小节一一对应）：

1. 导入库：``matplotlib``、``cartopy``、``cartopy.crs``、``xarray``、``numpy``；
2. 创建画布与地理子图，指定画布投影；
3. 读取 NetCDF 气温场，用 Xarray ``sel`` 截取西北区域；
4. 调用 ``contourf`` 绘制气温填色场，绑定地理坐标 ``transform``；
5. 添加海岸线、国界、省界、河流等地理要素；
6. 设置经纬度刻度、画布范围（裁剪西北地区）；
7. 添加色标 ``colorbar``、标题、坐标轴标签；
8. 高清导出图片，设置 DPI、画布尺寸。

基础绘图：西北地区气温填色图完整实操
------------------------------------

前置库安装（met_p312 环境）
^^^^^^^^^^^^^^^^^^^^^^^^^^^

确保虚拟环境已安装依赖，未安装则执行命令：

.. code-block:: bash

   conda install cartopy xarray netcdf4 numpy matplotlib

.. warning::

   Cartopy 捆绑了不少地理底层库（GEOS、Proj），**优先用 conda 安装**，不要只用 pip——pip 通常装不出能正常加载海岸线的版本。

完整基础绘图可运行代码
^^^^^^^^^^^^^^^^^^^^^^

首先说明数据文件：本项目 T-001 统一提供的格点数据文件 ``./data/northwest_temp.nc`` 内含三个变量——经度 ``lon``（一维，单位 °E）、纬度 ``lat``（一维，单位 °N）和气温 ``temp``（二维，(lat, lon)，单位 ℃），覆盖西北地区范围（东经 90°~112°，北纬 32°~43°）。主轴入仓后，直接读取绘图即可。

.. code-block:: python

   # 第10章 Cartopy 西北地区气温填色图

   import matplotlib.pyplot as plt
   import cartopy.crs as ccrs
   import cartopy.feature as cfeature
   import xarray as xr

   # 1. 读取 T-001 提供的西北 NetCDF 气温数据（字段：lon/lat/temp）
   ds = xr.open_dataset("./data/northwest_temp.nc")
   temp = ds.temp   # 气温变量（二维，(lat, lon)）
   lon = ds.lon     # 经度（一维，°E）
   lat = ds.lat     # 纬度（一维，°N）

   # 2. 创建画布，指定等经纬度投影
   fig, ax = plt.subplots(figsize=(10, 6),
                          subplot_kw={"projection": ccrs.PlateCarree()})

   # 3. 绘制气温等值线填色，必须指定 transform
   contour = ax.contourf(lon, lat, temp, levels=20, cmap="coolwarm",
                         transform=ccrs.PlateCarree())

   # 4. 叠加基础地理要素
   ax.coastlines(linewidth=0.8, color="black")                 # 海岸线
   ax.add_feature(cfeature.BORDERS, linewidth=0.8, color="black")  # 国界
   ax.add_feature(cfeature.RIVERS, linewidth=0.5, color="blue")    # 河流

   # 5. 限定绘图范围：西北地区经纬度
   ax.set_extent([90, 112, 32, 43], crs=ccrs.PlateCarree())

   # 6. 添加经纬度刻度
   ax.gridlines(draw_labels=True, linestyle="--", alpha=0.6)

   # 7. 色标、标题
   cbar = fig.colorbar(contour, shrink=0.8)
   cbar.set_label("气温 ℃")
   ax.set_title("西北地区2024年平均气温空间分布图", fontsize=14)

   # 8. 导出高清图片
   plt.savefig("./figures/northwest_temp_map.png", dpi=300, bbox_inches="tight")
   plt.show()

.. note::

   无文件时的构造数据备选。如果本地一时拿不到 ``northwest_temp.nc``（例如想先在自己的电脑上练手），可以用下面这段代码临时构造一份「伪格点场」，字段结构与真实文件完全一致，替换掉上面的数据读取部分即可运行：

   .. code-block:: python

      import numpy as np

      # 构造西北范围经纬度网格（与 T-001 文件字段 lon/lat/temp 一致）
      lon = np.linspace(90, 112, 45)      # 东经 90°~112°
      lat = np.linspace(32, 43, 33)       # 北纬 32°~43°
      lon, lat = np.meshgrid(lon, lat)    # 变成二维网格，和 temp 形状匹配

      # 合成气温场：随纬度线性变化（南暖北冷），并加入一点经向起伏
      temp = 15 + 0.5 * (40 - lat) - 0.02 * (lon - 101) ** 2

   之后把上面的 ``contourf``/``scatter`` 等依赖 ``ds.lon`` 的地方，改成直接用局部变量 ``lon``、``lat``、``temp`` 即可。

代码分步解析
^^^^^^^^^^^^

1. **数据读取**：对接项目 ``data`` 目录下 NetCDF 文件，和第 8 章 Xarray 读取逻辑保持统一。记住文件字段是 ``lon`` / ``lat`` / ``temp`` 三个变量。

2. **subplot_kw 关键参数**：``projection=ccrs.PlateCarree()`` 把普通 Axes 转换成地理绘图的 GeoAxes——这一行决定了「纸往哪张地图坐标架上铺」。

3. **contourf 核心参数说明**：
   - ``levels``：等值分层数量，数值越大色彩过渡越细腻；
   - ``cmap``：色带，``coolwarm`` 冷-暖色系是气温绘图的标准配色（蓝色冷、红色暖）；
   - ``transform=ccrs.PlateCarree()``：**最容易遗漏的核心参数**，缺失会导致格点地图错位——没有它，Cartopy 根本不知道这份散落的数据该贴在地图哪个经纬度上。

4. **set_extent**：裁剪画布范围，锁定西北区域，去掉无关的空白区域，让图面更聚焦。

5. **gridlines(draw_labels=True)**：自动生成经纬度刻度标注。

6. **savefig**：300 DPI 满足课程报告、论文附图的清晰度标准。

地理要素自定义与精细化美化
--------------------------

调整线条样式、颜色、粗细
^^^^^^^^^^^^^^^^^^^^^^^^

想让国界限粗黑、省界用浅灰细线、河流用淡蓝，只需在调用时指定参数即可：

.. code-block:: python

   import cartopy.feature as cfeature

   # 国界：粗一些、纯黑，作为最上一层的阅读骨架
   ax.add_feature(cfeature.BORDERS, linewidth=1.2, color="black")

   # 海岸线：中等粗细，深灰
   ax.coastlines(linewidth=0.8, color="dimgray")

   # 河流：浅蓝细线，不抢气温填色场的主视觉
   ax.add_feature(cfeature.RIVERS, linewidth=0.4, color="#4488dd")

   # 湖泊：淡蓝填充，透明度低一些更好
   ax.add_feature(cfeature.LAKES, edgecolor="none", facecolor="#aaddff", alpha=0.6)

.. note::

   图层层次感口诀：**主图（气温填色）最显眼，地名河流靠边站，国界海岸来收边，站点标记点最上端。**

自定义经纬度刻度间隔
^^^^^^^^^^^^^^^^^^^^

自动刻度可能在西北这种窄条区域显得拥挤，可以手动指定经度每 5°、纬度每 3° 一条刻度：

.. code-block:: python

   import matplotlib.ticker as mticker

   gl = ax.gridlines(draw_labels=True, linestyle="--", alpha=0.6)
   gl.xlocator = mticker.FixedLocator([90, 95, 100, 105, 110])  # 经度每5°
   gl.ylocator = mticker.FixedLocator([32, 35, 38, 41, 43])     # 纬度每3°

色标自定义配置
^^^^^^^^^^^^^^

1. 手动设定气温等值区间，让分级更贴近论文图例需求：

.. code-block:: python

   levels = [-10, -5, 0, 5, 10, 15, 20, 25]
   contour = ax.contourf(lon, lat, temp, levels=levels, cmap="coolwarm",
                         transform=ccrs.PlateCarree())

2. 修改色标位置、尺寸、文字字号：

.. code-block:: python

   cbar = fig.colorbar(contour, ax=ax, shrink=0.8, pad=0.02)
   cbar.set_label("气温 ℃", fontsize=12)
   cbar.ax.tick_params(labelsize=10)

3. 反色带、自定义渐变色：若想「暖色表示低温」，直接在 cmap 后加 ``_r``（``"coolwarm_r"``）；想要连续渐变色带，用 ``matplotlib.colors.LinearSegmentedColormap`` 从调色板拼接自定义色带。

叠加城市站点标记
^^^^^^^^^^^^^^^^

在地图上标注兰州站点坐标，对接本项目兰州观测站数据（第 2、3、4、5 章都用过它的信息）：

.. code-block:: python

   # 兰州站固定坐标：lon=103.83°E, lat=36.06°N
   ax.scatter(103.83, 36.06, c="black", marker="o", s=30,
              transform=ccrs.PlateCarree())
   ax.text(104.2, 36.06, "兰州站", fontsize=9,
           transform=ccrs.PlateCarree())

.. warning::

   注意：``scatter`` 和 ``text`` 也必须带 ``transform=ccrs.PlateCarree()``！否则点会画到地图外或错位——这和 ``contourf`` 是同一个道理：不贴经纬度标签，就贴不到正确的位置。

拓展提升板块
------------

多投影切换：兰伯特等面积投影绘制西北图
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

区域面积对比宜用兰伯特等面积投影，中心对准西北腹地（经度 101°E、纬度 38°N），形变最小。替换整段画布创建与裁剪代码即可，绘图逻辑与 PlateCarree 完全一致：

.. code-block:: python

   import cartopy.crs as ccrs
   import xarray as xr
   import matplotlib.pyplot as plt
   import cartopy.feature as cfeature

   ds = xr.open_dataset("./data/northwest_temp.nc")

   # 兰伯特等面积投影，中心对准西北腹地
   proj = ccrs.LambertAzimuthalEqualArea(central_longitude=101, central_latitude=38)
   fig, ax = plt.subplots(figsize=(10, 7), subplot_kw={"projection": proj})

   contour = ax.contourf(ds.lon, ds.lat, ds.temp, levels=20, cmap="coolwarm",
                         transform=ccrs.PlateCarree())

   ax.coastlines(linewidth=0.8, color="black")
   ax.add_feature(cfeature.BORDERS, linewidth=0.8, color="black")

   # 注意：set_extent 的经纬度范围以 PlateCarree 坐标给出，并显式指定 crs
   ax.set_extent([90, 112, 32, 43], crs=ccrs.PlateCarree())

   ax.gridlines(draw_labels=True, linestyle="--", alpha=0.6)

   cbar = fig.colorbar(contour, shrink=0.8)
   cbar.set_label("气温 ℃")

   plt.savefig("./figures/northwest_temp_lambert_annual.png",
               dpi=300, bbox_inches="tight")
   plt.show()

.. note::

   观察对比：同一份数据，兰伯特投影下西北这片高纬、拉伸小的区域面积关系更贴近真实，适合「面积比较」类专题图；而 PlateCarree 经纬线横平竖直，更便于直接读数。两者按需求选用，没有绝对的好坏。

叠加风场矢量 quiver 绘图
^^^^^^^^^^^^^^^^^^^^^^^^

在气温填色底图上叠加风矢量箭头，实现「温风联合」空间图。风场数据同样来自 NetCDF 文件中的 ``u``（纬向风）、``v``（经向风）变量，均需注意坐标方向和 ``transform``：

.. code-block:: python

   import cartopy.crs as ccrs
   import matplotlib.pyplot as plt
   import xarray as xr

   ds = xr.open_dataset("./data/northwest_temp.nc")
   u = ds.u   # 纬向风（m/s）
   v = ds.v   # 经向风（m/s）

   fig, ax = plt.subplots(figsize=(10, 6),
                          subplot_kw={"projection": ccrs.PlateCarree()})

   contour = ax.contourf(ds.lon, ds.lat, ds.temp, levels=20, cmap="coolwarm",
                         transform=ccrs.PlateCarree())

   # 每第4个格点取一个箭头，避免箭头过密
   ax.quiver(ds.lon[::4], ds.lat[::4], u[::4, ::4], v[::4, ::4],
             scale=20, transform=ccrs.PlateCarree())

   ax.coastlines(linewidth=0.8, color="black")
   ax.add_feature(cfeature.BORDERS, linewidth=0.8, color="black")
   ax.set_extent([90, 112, 32, 43], crs=ccrs.PlateCarree())

   cbar = fig.colorbar(contour, shrink=0.8)
   cbar.set_label("气温 ℃")

   plt.savefig("./figures/northwest_temp_uv_annual.png", dpi=300, bbox_inches="tight")
   plt.show()

.. warning::

   ``quiver`` 传参注意：风矢量的起点坐标是「经纬度数组」，箭头分量是 ``u``、``v``（经向风、纬向风），不要与 x、y 混用。坐标与分量缺一不可，同样都要带上 ``transform``。

批量绘制逐月气温地图循环代码
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

用 ``for`` 循环遍历 NetCDF 时间维度，自动生成 12 个月西北气温图，批量保存到 ``figures`` 文件夹：

.. code-block:: python

   import os
   import matplotlib.pyplot as plt
   import cartopy.crs as ccrs
   import cartopy.feature as cfeature
   import xarray as xr

   ds = xr.open_dataset("./data/northwest_temp.nc")
   os.makedirs("./figures", exist_ok=True)

   months = ds.time.values   # 假定时维名为 time，取值形如 2024-01 等

   for m in ds.time:
       month_temp = ds.temp.sel(time=m)   # 取出单月气温场
       # 统一色标范围，保证 12 张图冷暖尺可互相比较
       vmin, vmax = -12, 28

       fig, ax = plt.subplots(figsize=(10, 6),
                              subplot_kw={"projection": ccrs.PlateCarree()})
       contour = ax.contourf(ds.lon, ds.lat, month_temp,
                             levels=20, cmap="coolwarm",
                             vmin=vmin, vmax=vmax,
                             transform=ccrs.PlateCarree())
       ax.coastlines(linewidth=0.8, color="black")
       ax.add_feature(cfeature.BORDERS, linewidth=0.8, color="black")
       ax.set_extent([90, 112, 32, 43], crs=ccrs.PlateCarree())

       cbar = fig.colorbar(contour, shrink=0.8)
       cbar.set_label("气温 ℃")
       ax.set_title(f"西北 {m} 气温分布图")

       # 文件名用月份字符串，存进 figures 文件夹
       plt.savefig(f"./figures/northwest_temp_{m.year}{m.month:02d}.png",
                   dpi=300, bbox_inches="tight")
       plt.close(fig)   # 循环里务必关闭画布，否则内存溢出、运行卡顿

.. warning::

   批量绘图三黄金法则：**循环里统一 ``vmin/vmax``（可比性）、画完 ``plt.close()``（释放内存）、文件名按时间命名（可检索）。** 缺一不可。

多子图布局：分季节气温对比地图
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2 行 2 列子图，分别绘制春、夏、秋、冬的气温场，统一色标便于季节对比：

.. code-block:: python

   import matplotlib.pyplot as plt
   import cartopy.crs as ccrs
   import cartopy.feature as cfeature
   import xarray as xr

   ds = xr.open_dataset("./data/northwest_temp.nc")

   seasons = {
       "春季": ("2024-03-01T00", "2024-05-01T00"),   # 起止时间切片用
       "夏季": ("2024-06-01T00", "2024-08-01T00"),
       "秋季": ("2024-09-01T00", "2024-11-01T00"),
       "冬季": ("2024-12-01T00", "2025-02-01T00"),
   }
   vmin, vmax = -20, 30   # 四图统一色标范围

   fig, axes = plt.subplots(
       2, 2, figsize=(12, 9),
       subplot_kw={"projection": ccrs.PlateCarree()})

   for ax, (season, (t0, t1)) in zip(axes.flat, seasons.items()):
       season_temp = ds.temp.sel(time=slice(t0, t1)).mean(dim="time")  # 季节平均

       contour = ax.contourf(ds.lon, ds.lat, season_temp,
                             levels=20, cmap="coolwarm",
                             vmin=vmin, vmax=vmax,
                             transform=ccrs.PlateCarree())
       ax.coastlines(linewidth=0.8, color="black")
       ax.add_feature(cfeature.BORDERS, linewidth=0.8, color="black")
       ax.set_extent([90, 112, 32, 43], crs=ccrs.PlateCarree())
       ax.set_title(f"西北地区{season}平均气温")

   # 四张子图共用一只色标，只给最后一列显示纬度刻度以免重叠，此处统一用一个 cbar
   fig.colorbar(contour, ax=axes, shrink=0.8, pad=0.02, label="气温 ℃")
   plt.tight_layout()
   plt.savefig("./figures/northwest_temp_seasons.png", dpi=300, bbox_inches="tight")
   plt.show()

.. note::

   2×2 子图的色标用 ``fig.colorbar(contour, ax=axes)`` 可以让四张图共享一个大色条，视觉更整齐；配合统一的 ``vmin/vmax``，四季冷暖差异一目了然。

常见报错核心解决方案
^^^^^^^^^^^^^^^^^^^^

1. **地图格点严重错位**：漏写 ``transform=ccrs.PlateCarree()``。排查 ``contourf``、``scatter``、``quiver`` 是否都带了 ``transform``。

2. **set_extent 无裁剪效果**：``extent`` 经纬度范围写反（顺序应为 ``[西经, 东经, 南纬, 北纬]``，即 ``[90, 112, 32, 43]``）、或 ``crs`` 参数缺失。

3. **海岸线加载缓慢**：第一次运行会自动下载 Natural Earth 矢量文件，耐心等待一次即可；也可提前配置本地缓存路径，避免课堂绘图中途卡顿。

4. **图片导出边缘缺失**：``savefig`` 添加 ``bbox_inches="tight"``。

5. **cartopy 安装失败**：优先 ``conda install cartopy``，不要只用 pip（地理底层依赖 pip 无法自动配置）。

本章小结
--------

1. 掌握 Cartopy 三种气象常用地图投影的原理与适用场景（PlateCarree 图省事、Mercator 保角度、Lambert 保面积）；

2. 熟练使用 GeoAxes、``transform`` 参数，解决气象格点数据地图错位问题；

3. 独立完成西北地区气温填色地图，叠加海岸线、国界、河流、刻度、色标全套要素；

4. 掌握画布区域裁剪（``set_extent([90, 112, 32, 43])``）、图片高清导出（``dpi=300`` + ``bbox_inches="tight"``）、地图美化细节调整；

5. 拓展学会兰伯特投影、风场叠加、批量时序绘图、多子图季节对比等进阶绘图技巧；

6. 完整完成本项目最终可视化成果，形成一套从环境搭建到空间地图的完整气象 Python 分析流程。

最佳实践：Cartopy 地图成果规范
------------------------------

下面的规范是一套可以照抄的西北气温地图「施工规范」：每节先给结论（✅），再给常见坑（⚠️），代码均为可直接复制的标准写法。

项目目录文件规范（与全书 weather_project 统一）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

所有 Cartopy 地图脚本、输出图片、数据严格遵循固定路径，避免路径报错、文件杂乱：

1. ✅ 格点数据读取路径：``./data/northwest_temp.nc``（T-001 统一提供模拟 NetCDF 气温文件，**禁止写绝对本地磁盘路径**）；
2. ✅ 绘图脚本存放路径：``./scripts/plot_cartopy_temp.py``；
3. ✅ 地图输出保存路径：``./figures/``，所有地图统一存入该文件夹，不散落根目录；
4. ✅ 输出文件命名规范：``区域_要素_投影_时间.png``，例如 ``northwest_temp_platecarree_annual.png``、``northwest_temp_lambert_july.png``。

路径最佳实践代码模板：

.. code-block:: python

   import os

   # 统一路径定义，全局复用
   data_path = os.path.join("./data", "northwest_temp.nc")
   fig_save_path = os.path.join("./figures", "northwest_temp_map.png")

   # 自动创建图片文件夹，避免无目录保存报错
   os.makedirs("./figures", exist_ok=True)

.. warning::

   不做 ``os.makedirs(..., exist_ok=True)``，目录不存在时 ``savefig`` 会直接报 ``FileNotFoundError``——批量绘图时最常见的第一声「哎呀」。

虚拟环境与库安装规范
^^^^^^^^^^^^^^^^^^^^

1. ✅ 绘图固定使用 ``met_p312`` Python 3.12 虚拟环境，不使用系统默认 Python；
2. ✅ Cartopy 优先 conda 安装，禁止单独 pip 安装（底层地理依赖 pip 无法自动配置）。

标准安装命令：

.. code-block:: bash

   conda install cartopy xarray netcdf4 numpy matplotlib

3. ⚠️ 禁止混用多源安装方式（一部分 conda、一部分 pip），防止版本冲突、海岸线加载失败。

地图画布与投影选型规范（西北区域专用）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. ✅ 常规年度/逐月气温分布图：``PlateCarree`` 等经纬度投影（项目默认）。
   - 画布尺寸固定：单张子图 ``figsize=(10, 6)``，双列子图 ``figsize=(12, 5)``，四季对比 2×2 子图 ``figsize=(12, 9)``；
   - 强制书写 ``subplot_kw={"projection": ccrs.PlateCarree()}``，不可省略地理投影参数。

2. ✅ 区域气候专题分析图：``LambertAzimuthalEqualArea`` 兰伯特等面积投影，西北区域统一投影中心配置，减少区域形变：

.. code-block:: python

   proj = ccrs.LambertAzimuthalEqualArea(central_longitude=101, central_latitude=38)
   fig, ax = plt.subplots(figsize=(10, 7), subplot_kw={"projection": proj})

3. ⚠️ **禁止行为**：不使用 Mercator 墨卡托投影绘制西北中纬度气温图——高纬面积被严重拉伸，不符合气象期刊绘图标准。

核心绘图参数标准化（contourf 气温填色统一规范）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. ✅ 气温填色 ``levels`` 分层：常规气温场统一设置 ``levels=20``，过渡平滑；如需自定义分级（用于论文分级图例）手动传入数值列表：

.. code-block:: python

   levels = [-10, -5, 0, 5, 10, 15, 20, 25]

2. ✅ 色带固定选用 ``cmap="coolwarm"``（冷蓝-暖红，气象气温通用配色），**禁止**使用七彩杂乱色带 ``jet``；
3. ✅ 强制添加 ``transform=ccrs.PlateCarree()`` 至 ``contourf``，这是地图不偏移的硬性规范，所有示例脚本必须包含该参数。

标准填色代码片段：

.. code-block:: python

   contour = ax.contourf(
       ds.lon, ds.lat, ds.temp,
       levels=20,
       cmap="coolwarm",
       transform=ccrs.PlateCarree()
   )

.. warning::

   ``transform`` 相当于给每个格点贴「经纬度标签」。漏写它，Cartopy 不知道数据该贴在地图哪个位置，整片色块会错位、跑偏甚至消失。所有空间绘图（``contourf``、``scatter``、``quiver``、``text``）都要记得贴这个标签。

地理要素叠加样式统一标准
^^^^^^^^^^^^^^^^^^^^^^^^
为保证整套项目图表视觉统一，固定各类地理线条粗细、颜色：

1. ✅ 海岸线：``ax.coastlines(linewidth=0.8, color="black")``
2. ✅ 国界线：``cfeature.BORDERS``，``linewidth=0.8, color="black"``
3. ✅ 河流：``cfeature.RIVERS``，``linewidth=0.4, color="#4488dd"``
4. ✅ 省界（拓展绘图）：自定义 shp 省界文件，线条宽度 0.5、浅灰色，不遮盖气温填色场
5. ✅ 图层绘制顺序规范（由底层到顶层）：**气温填色场 → 河流 → 海岸线 → 国界 → 站点标记散点**

.. warning::

   图层顺序错了：如果先画国界/海岸线、再画气温填色，兜底上去的色块会把国界、海岸线整个埋住，图上一片「糊」——先铺底图色，再画边框与标记，顺序绝不能倒。

研究区域裁剪（西北地区固定经纬度范围）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
所有西北气温地图统一裁剪范围，杜绝图表大小不一：

.. code-block:: python

   # 西北标准经纬度：东经90°~112°，北纬32°~43°
   ax.set_extent([90, 112, 32, 43], crs=ccrs.PlateCarree())

配套网格刻度规范：

.. code-block:: python

   # 显示经纬度标签，虚线网格，降低透明度不抢视觉重心
   ax.gridlines(draw_labels=True, linestyle="--", alpha=0.6)

.. warning::

   ``set_extent`` 的列表顺序是 ``[西经, 东经, 南纬, 北纬]``，即 ``[90, 112, 32, 43]``。写反成 ``[32, 43, 90, 112]`` 或漏掉 ``crs=ccrs.PlateCarree()``，裁剪就会失效。

色标 colorbar 标准化规范
^^^^^^^^^^^^^^^^^^^^^^^^
1. ✅ 缩放比例统一 ``shrink=0.8``，避免色条过长/过短与画布不协调；
2. ✅ 色标标签固定：``cbar.set_label("气温 ℃", fontsize=11)``；
3. ✅ 字号统一：标题 14 号、坐标轴与色标文字 11 号、刻度 10 号。

完整色标代码：

.. code-block:: python

   cbar = fig.colorbar(contour, shrink=0.8)
   cbar.set_label("气温 ℃", fontsize=11)
   ax.set_title("西北地区2024年平均气温空间分布图", fontsize=14)

图片导出高清规范（课程报告/期刊附图通用）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. ✅ DPI 固定 300，满足印刷清晰度标准；
2. ✅ 增加 ``bbox_inches="tight"`` 自动裁剪空白白边，无需手动截图裁剪；
3. ✅ 图片格式统一 PNG，兼顾清晰度与文件体积。

标准保存代码：

.. code-block:: python

   plt.savefig(fig_save_path, dpi=300, bbox_inches="tight")
   plt.close()   # 绘图完成关闭画布，释放内存，批量绘图必备

.. warning::

   批量绘图最佳实践：循环绘图后必须 ``plt.close()``，否则会累积大量画布导致内存溢出、运行卡顿——开一次 ``fig`` 就相当于打开一扇窗，画完不关，窗会越叠越多。

兰州站点标记统一规范（串联全书实战项目）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

每张西北气温地图统一标注兰州观测站点，串联第 2、3、4、5 章站点信息数据：

.. code-block:: python

   # 兰州站固定坐标 lon=103.83, lat=36.06
   ax.scatter(103.83, 36.06, c="black", marker="o", s=30, transform=ccrs.PlateCarree())
   ax.text(104.2, 36.06, "兰州站", fontsize=9, transform=ccrs.PlateCarree())

.. warning::

   ``scatter`` 与 ``text`` 必须带 ``transform=ccrs.PlateCarree()``，否则站点标在地图外或错位，跟 ``contourf`` 是同一个道理。

批量绘图、多子图通用规范
^^^^^^^^^^^^^^^^^^^^^^^^

1. ✅ 逐月循环绘图：使用 xarray 内置 ``groupby("time")`` 或 ``sel(time=...)`` 遍历时间，搭配 ``for`` 循环批量出图，自动命名存储；
2. ✅ 四季对比 2×2 子图：统一色标范围 ``vmin``、``vmax``，保证四张图冷暖色标尺完全一致，便于对比季节差异。

示例统一色标约束：

.. code-block:: python

   vmin, vmax = -12, 28

   contour = ax.contourf(
       ds.lon, ds.lat, ds.temp,
       levels=20, cmap="coolwarm",
       vmin=vmin, vmax=vmax,
       transform=ccrs.PlateCarree()
   )

.. warning::

   多子图若各自自动定色标，每张图的冷暖含义就完全不同——图 A 的「暖红」可能是 15℃、图 B 却是 25℃。统一 ``vmin/vmax`` 才能保证「同一颜色=同一温度」，季节比较才成立。

避坑最佳实践（高频报错预防规范）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. ⚠️ 禁止省略 ``transform`` 参数：所有空间绘图函数 ``contourf``、``scatter``、``quiver``、``text`` 均必须携带 ``transform``，防止地图坐标错位；
2. ⚠️ 不使用中文路径、中文文件名：NetCDF 读取、图片保存路径全程英文，避免系统编码报错；
3. ⚠️ 第一次运行 Cartopy 提前缓存地理文件：Natural Earth 矢量文件首次加载会自动下载，可提前配置缓存路径，避免课堂绘图卡顿；
4. ✅ 环境锁定：项目交付附带 ``met_p312_env.yml`` 环境配置文件，保证不同设备绘图效果完全一致；
5. ✅ 代码可移植：全程使用相对路径，不写入 ``D:/xxx``、``C:/User/xxx`` 等绝对磁盘路径，机房、小组协作可直接运行。

科研绘图通用审美规范
^^^^^^^^^^^^^^^^^^^^

1. ✅ 图表元素精简：不堆砌多余装饰，核心突出气温填色场；
2. ✅ 网格透明度降低，仅作为坐标参考，不干扰主图；
3. ✅ 线条深浅分层：国界粗、省界细、河流浅蓝，层次分明；
4. ✅ 标题简洁规范：统一格式「区域+时段+气象要素空间分布图」，无冗余文字；
5. ✅ 字体统一使用无衬线字体，避免系统缺失字体导致文字乱码（中文字体配置见相应章节，如 ``SimHei``/``Microsoft YaHei``）。

.. seealso:: 配套练习：第 10 章练习《Cartopy 气象地图》将在随后交付后上线（链接到时补全）　·　示例画廊 :doc:`/gallery/plot_viz/index`