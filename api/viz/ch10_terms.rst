第 10 章术语：Cartopy 地图绘图
===============================

配套 :ref:`tut-cartopy` 正文使用。每个词条 = 一句话定义 + **生活类比** + **常用写法**\（`.. code-block:: python` 承载代码示例）+ **易混淆点**。这些词是读懂 Cartopy 地图绘图代码的钥匙：报错时先看词条，再对症下药。

.. seealso:: 配套正文：:doc:`/user_guide/viz/cartopy`　·　配套练习：:doc:`/tutorials/viz/ch10_practice`

.. glossary::

   投影（Projection）
      将三维球面上的地理坐标（经纬度）转换为二维平面坐标的数学方法。Cartopy 将所有投影实现为 cartopy.crs.Projection 类的子类。

      **生活类比** —— 剥橙子：想把完整的橙子皮（球面）压成一张平面地图，无论怎么切都会变形。投影就是决定「从哪里下刀、怎么摊平」的规则。没有「完美」的投影，只有适合不同用途的投影。

      .. code-block:: python

         import cartopy.crs as ccrs
         import matplotlib.pyplot as plt

         # 创建一张等距圆柱投影地图
         fig = plt.figure(figsize=(8, 4))
         ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
         ax.coastlines()
         ax.set_title("PlateCarree 投影")

      .. note::

         经纬度本身（Geodetic）是球面坐标系，不是投影。绘图时必须区分「地图投影」和「数据坐标系」。

      **易混淆点** —— 投影是「球面→平面」的转换方法，结果是平面坐标系；经纬度本身（Geodetic）是球面坐标系，不是投影。不要混用不同投影的数据：经纬度相同的两个点，在不同投影下的平面位置完全不同。

   PlateCarree（等距圆柱投影）
      Cartopy 中最简单的投影，将经纬度直接映射为平面上的 x（经度）和 y（纬度），即把地球展开成等距矩形网格。可通过 central_longitude 参数设置中央经线。

      **生活类比** —— 世界地图挂图：经线是垂直的平行线，纬线是水平的平行线，地球被「剪开」摊平成一张长方形图纸。格陵兰岛看起来和非洲一样大，但实际上非洲面积是格陵兰的 14 倍。

      .. code-block:: python

         import cartopy.crs as ccrs
         import matplotlib.pyplot as plt

         # 中央经线设为 105°E，让中国位于地图中部
         proj = ccrs.PlateCarree(central_longitude=105)
         fig, ax = plt.subplots(
             figsize=(8, 4),
             subplot_kw={"projection": proj},
         )
         ax.coastlines(resolution="110m")
         ax.set_global()
         plt.savefig("platecarree.png", dpi=150, bbox_inches="tight")

      **易混淆点** —— 经纬度坐标可以直接「当作」 PlateCarree 来画，但在 Cartopy 内部，经纬度应属于 ccrs.Geodetic() 坐标系。用 transform=ccrs.PlateCarree() 绘制经纬度数据只是一种便捷写法。设置 central_longitude=180 可以让太平洋位于地图中央，避免亚洲被从中间切开。

   transform（数据坐标系声明）
      绘图函数中的 transform 参数，用于告诉 Cartopy 你的数据本身是在什么坐标系下定义的。Cartopy 会据此将数据实时转换到地图的投影坐标系中显示。

      **生活类比** —— 翻译官：你拿着一份中文写的文件（数据的原始坐标系），要给一个只懂英文的人（地图投影）看。transform 就是告诉翻译官「这份文件是中文」，翻译官才能正确地译成英文。

      .. code-block:: python

         import cartopy.crs as ccrs
         import matplotlib.pyplot as plt
         import numpy as np

         fig, ax = plt.subplots(
             figsize=(6, 4),
             subplot_kw={"projection": ccrs.PlateCarree()},
         )
         ax.coastlines()

         # 经纬度数据必须声明 transform，否则画错位置
         lons = np.linspace(70, 140, 50)
         lats = np.linspace(20, 50, 40)
         data = np.random.randn(40, 50)
         ax.contourf(lons, lats, data,
                     transform=ccrs.PlateCarree(),  # 关键！
                     cmap="coolwarm")
         plt.colorbar(label="模拟气温 / ℃")

      .. note::

         projection 决定地图目标坐标系，在创建 GeoAxes 时设定；transform 决定数据源坐标系，在每次绘图时指定。

      **易混淆点** —— 如果数据是经纬度但没加 transform=ccrs.PlateCarree()，Cartopy 会默认数据与地图投影一致，导致数据被错误地「当作」投影坐标来解读，点会飞到莫名其妙的位置。长距离连线用 Geodetic：绘制跨大洲的航线或轨迹时，用 transform=ccrs.Geodetic() 会沿球面大圆路径插值，画出弯曲的真实路线；用 PlateCarree 则画直线，在极地附近严重失真。

   海岸线（Coastlines）
      Cartopy 中用于在地图上绘制全球海岸轮廓线的方法。通过 ax.coastlines() 调用，数据来自 Natural Earth 数据集。

      **生活类比** —— 描红地图的轮廓：拿到一张空白地图，先用铅笔把各大洲的海岸线描出来，有了这个基本框架，才能知道陆地在哪、海洋在哪。

      .. code-block:: python

         import cartopy.crs as ccrs
         import matplotlib.pyplot as plt

         fig, ax = plt.subplots(
             figsize=(6, 4),
             subplot_kw={"projection": ccrs.PlateCarree()},
         )
         ax.coastlines(resolution="110m", color="black", linewidth=0.8)
         # 110m = 低分辨率（快），50m = 中等，10m = 高精度（慢）

      **易混淆点** —— 海岸线是「水陆分界」，国界线是「国家分界」。ax.coastlines() 画的是前者；要画国界需用 ax.add_feature(cfeature.BORDERS)。ax.coastlines(resolution="110m") 中的 110m 表示 1:1.1 亿比例尺（低分辨率、速度快），可选 50m\ （中）和 10m\ （高、文件大、加载慢）。

   Natural Earth（自然地球数据集）
      Cartopy 内置的免费开源地理数据集合，包含海岸线、国界、河流、湖泊、陆地、海洋等矢量数据。可通过 cartopy.feature 模块调用。

      **生活类比** —— 免费的地理底图素材库：里面已经画好了海岸线、国界、河流等图层，随拿随用，不用自己从头描。

      .. code-block:: python

         import cartopy.crs as ccrs
         import cartopy.feature as cfeature
         import matplotlib.pyplot as plt

         fig, ax = plt.subplots(
             figsize=(6, 4),
             subplot_kw={"projection": ccrs.PlateCarree()},
         )
         ax.add_feature(cfeature.LAND, facecolor="lightgray")
         ax.add_feature(cfeature.OCEAN, facecolor="lightblue")
         ax.add_feature(cfeature.BORDERS, edgecolor="black", linewidth=0.5)
         ax.coastlines(resolution="110m")
         ax.set_extent([70, 140, 15, 55])  # 中国区域

      **易混淆点** —— 常用要素有预定义常量，如 cfeature.LAND（陆地）、cfeature.OCEAN（海洋）、cfeature.BORDERS（国界）、cfeature.RIVERS（河流）。如果要加载非预定义要素（如省界），需手动创建 NaturalEarthFeature 实例。首次使用高分辨率数据（10m）时会自动下载，离线环境需提前缓存。

   色带映射（Colormap Mapping）
      将数据数值映射为颜色的过程。在 Cartopy 绘图中，通过 cmap 参数指定色带，通过 norm 参数控制数值到颜色的映射范围。

      **生活类比** —— 气温填色图：低温用蓝色、高温用红色，中间的数值按渐变过渡。色带映射就是决定「多少度对应什么颜色」的调色规则。

      .. code-block:: python

         import cartopy.crs as ccrs
         import matplotlib.pyplot as plt
         import matplotlib.colors as mcolors
         import numpy as np

         fig, ax = plt.subplots(
             figsize=(6, 4),
             subplot_kw={"projection": ccrs.PlateCarree()},
         )
         ax.coastlines()

         lons = np.linspace(70, 140, 50)
         lats = np.linspace(20, 50, 40)
         data = np.random.uniform(-5, 30, (40, 50))

         # cmap 定义色板，norm 定义映射范围
         levels = np.arange(-5, 31, 5)
         cf = ax.contourf(
             lons, lats, data, levels=levels,
             transform=ccrs.PlateCarree(),
             cmap="RdYlBu_r",  # 蓝(冷) → 红(暖)
         )
         cbar = fig.colorbar(cf, ax=ax, label="气温 / ℃")
         ax.set_global()

      .. note::

         cmap 定义色板（有哪些颜色）；norm 定义映射规则（数值如何对应到这些颜色上）。两者配合使用才能正确着色。绘制填色图后，颜色条不是自动添加的，需用 fig.colorbar() 或 plt.colorbar() 手动添加。

      **易混淆点** —— 气象要素如温度通常用连续渐变（如 RdYlBu_r、viridis）；灾害等级、天气类型等分类数据用离散色带（ListedColormap）。contourf 的 levels 参数会把连续色带切分成离散色块，适合气温等值线填色图。

词条对照
--------

.. list-table::
   :widths: 22 30 48
   :header-rows: 1

   * - 词条
     - 管什么
     - 典型方法
   * - :term:`投影（Projection）`
     - 球面 → 平面的数学变换
     - ccrs.PlateCarree()、ccrs.Mercator()
   * - :term:`PlateCarree（等距圆柱投影）`
     - 经纬度直接展开为矩形
     - projection=ccrs.PlateCarree()
   * - :term:`transform（数据坐标系声明）`
     - 声明数据的原始坐标系
     - transform=ccrs.PlateCarree()
   * - :term:`海岸线（Coastlines）`
     - 水陆分界轮廓
     - ax.coastlines()
   * - :term:`Natural Earth（自然地球数据集）`
     - 地理矢量要素库
     - cfeature.LAND、cfeature.BORDERS
   * - :term:`色带映射（Colormap Mapping）`
     - 数值 → 颜色的映射
     - cmap=、norm=、levels=

读报错时先看词条：数据位置不对多半是 transform 遗漏；地图一片空白多半是投影没设或 set_extent 越界；颜色不对多半是 cmap / levels 配错了。
