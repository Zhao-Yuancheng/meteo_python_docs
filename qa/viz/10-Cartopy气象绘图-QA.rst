气象数据绘图（二）Cartopy Q&A
===================================

   **章节定位**\ ：第 10 章（模块三）· 对应用户指南
   ``user_guide/viz/cartopy.rst``\ ，贯穿项目第 10
   步：绘制西北地区气温空间分布图（等值线填色 +
   海岸线）。重点是「把一张带经纬度标签的格点表，经投影铺到地图上」时的报错、警告与静默异常现象。
   **通用排错方法论**\ ：见
   :doc:`00-通用排错指南 </qa/basics/00-通用排错指南>`\ （0.1 节「报错 / 警告 /
   静默错值」三分法、0.4 节「排查七招」、0.5 节「静默污染」先读；0.3
   节的 ``ImportError / AttributeError / DeprecationWarning / URLError``
   家谱图在本章会反复用到）。 **校正说明**\ ：本文全部
   ``Traceback / Warning / DeprecationWarning / URLError`` 均来自
   Cartopy **0.25.0** + Matplotlib **3.10.8**
   的真实运行输出，原文照录。文中涉及 DLL / PROJ
   的备注，是提醒你：\ **用 ``conda install cartopy`` 装出的版本会自动把
   PROJ/GEOS 底层库放进环境，无需手动补 DLL**——若你自行用 pip 裸装后出现
   DLL 报错，可回看 10.7 的依赖清单补装 ``shapely / pyproj / pyshp``\ 。
   **联网说明**\ ：Cartopy 首次使用 ``add_feature`` / ``coastlines``
   会联网下载 Natural Earth
   数据。若你身处断网/被墙环境，首次必报网络下载错（见
   10.6)——这地方同时给了「预缓存 +
   离线」两个标准方案，课前可先在有网机器上合好缓存。

--------------

.. _100-本章报错警告异常现象速查总表:

10.0 本章报错/警告/异常现象速查总表
-----------------------------------

第 10 章的高频坑先按「类别 \| 类型 \| 一句现象提示 \|
解决办法一句话」摊开，方便你快速锚定。

+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| 英文关键词 / 现象                                                                          | 类型      | 一句现象提示                                     | 解决办法一句话                                        |
+============================================================================================+===========+==================================================+=======================================================+
| 地图上出现\ **白色竖线/白条**\ （全球图 ±180 或 0 处）                                     | 静默现象  | 数据经度范围与投影中央经线错位，跨存线处填色断裂 | 统一数据经度与 ``central_longitude``\ ，或用          |
|                                                                                            |           |                                                  | ``add_cyclic_point`` / 平移经度                       |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| 漏写 ``transform=``                                                                        | 静默/错位 | 换非 PlateCarree 投影后数据跑到旁边/图外         | 每个空间绘图都补 ``transform=ccrs.PlateCarree()``     |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| ``projection=`` 与 ``transform=`` 混淆                                                     | 静默/错位 | 把「画布投影」当作「数据投影」混着写             | 分清：\ ``projection`` 在轴、\ ``transform``          |
|                                                                                            |           |                                                  | 在每个绘图调用                                        |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| ``set_extent`` 裁剪失效/画面空白                                                           | 静默现象  | 经纬序写反、漏 ``crs=``\ 、投影坐标系混用        | 写                                                    |
|                                                                                            |           |                                                  | ``set_extent([西,东,南,北], crs=ccrs.PlateCarree())`` |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| ``contourf`` 报 ``Input z must be 2D, not 3D``                                             | 报错      | 给 z 多留了一个 time 维                          | 取单时刻/做 ``sel``/``squeeze`` 后再画                |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| ``contourf`` 报 ``Shapes of x (...) and z (...) do not match``                             | 报错      | x/y 网格shape 与 z 对不上（常因 ``.T`` 转置）    | 统一 ``meshgrid`` 的纬度数×经度数与 z 一致            |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| ``pcolormesh`` 报 ``Dimensions of C ... one smaller than X ...``                           | 报错      | 1D x/y 与 z 尺寸关系错                           | 用 ``shading="auto"`` 或让 x/y 比 z 各多一格一致      |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| ``add_feature``/``coastlines`` 报 ``URLError``/超时                                        | 报错      | 首次用要联网下载 Natural Earth，断网/被墙失败    | 配 ``config["data_dir"]`` 缓存、或预下载 NE 到本地    |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| ``ModuleNotFoundError: No module named 'pyproj'/'shapely'``                                | 报错      | ``cartopy`` 依赖的地理库没装/环境没激活          | ``conda install cartopy shapely pyproj`` 或           |
|                                                                                            |           |                                                  | ``conda activate``                                    |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| ``AttributeError: 'GeoAxes' object has no attribute 'natural_earth_shp'``                  | 报错      | 用了老版本/教科书旧的 API                        | 用 ``cfeature`` /                                     |
|                                                                                            |           |                                                  | ``add_geometries(shapereader.Reader(...))``           |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| ``DeprecationWarning: geos_to_path is deprecated... Use cartopy.mpl.path.shapely_to_path`` | 警告      | 旧版内部 API 被官方弃用                          | 更新为新写法；老代码按提示迁移                        |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| 站点点到\ **大洋/图外**\ （静默）                                                          | 静默现象  | 点位经纬度装反或顺序传错                         | ``scatter(lon, lat, transform=...)``\ ，lon 在前 lat  |
|                                                                                            |           |                                                  | 在后                                                  |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| 站点/要素\ **不显示**                                                                      | 静默/错位 | 非 PlateCarree 轴上漏 ``transform``              | 加 ``transform``\ ，检查 ``set_extent`` 是否盖住它    |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| 中文标题/色标显示\ **方框**\ （汉字缺失）                                                  | 警告      | 系统未配置中文字体，Glyph missing                | 配 ``SimHei``/``Microsoft YaHei``\ （同第 9 章）      |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| 图外/空白一片（等值线在图测）                                                              | 静默现象  | 数据范围远小于 ``set_extent``\ 、或字段全 NaN    | 先 ``print(vmin/vmax/nan)``\ ，再配 ``levels`` 与     |
|                                                                                            |           |                                                  | ``vmin/vmax``                                         |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+
| ``UserWarning: ... identical low and high ylims makes transformation singular``            | 警告      | 范围退化为一个点                                 | 检查 ``set_extent``/首位数据使窗口至少占一个区域      |
+--------------------------------------------------------------------------------------------+-----------+--------------------------------------------------+-------------------------------------------------------+

..

   **一句话记住**\ ：Cartopy
   的「白色竖线、图层错位、点画到海里去」大多是\ **第 3
   类静默现象**——程序绿灯到底、图也能存，只是位置错了。它们不会主动报错，靠的是你给\ **每个空间绘图函数都贴上
   ``transform`` 标签**\ ，并盯住经度单位（度 vs 弧度）、经度范围（0–360
   vs −180–180）与维度顺序（lat,lon vs
   lon,lat）。凡“画完总觉得哪儿不对劲”，先开 ``set_extent`` 附近和
   ``transform`` 三连问。

--------------

.. _101-全球图--跨日界线出现的白色竖线白条:

10.1 全球图 / 跨日界线出现的白色竖线（白条）
--------------------------------------------

   这是 Cartopy
   新手与气象数据打交道最经典、也最神秘的“静默现象”——程序不报任何错，可全球图上就是有一条（或一窄条）竖白缝，把本该连续的气象场劈成两半。它几乎永远出现在\ **经度不连续的那条经线**\ 上（±180
   日界线，或 0/360 交界）。

.. _1011-暖脊骑在日界线上platecarree-默认中央经线-0-时在-180-裂出白缝:

10.1.1 暖脊骑在日界线上：\ ``PlateCarree()`` 默认中央经线 0 时在 ±180 裂出白缝
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 异常现象描述**\ ：构造一场「暖脊横跨 +-180°
日界线」的温度场（全球格点场），用默认
``ccrs.PlateCarree()``\ （中央经线 0）去 ``pcolormesh``
填色，得到的图上，暖脊本应在日界线处连续地“跨过去”，却在地图左右两条
±180°
边附近各出现一道\ **白色竖缝**\ ，暖脊被劈成两半，好像地图被撕开过。

.. code:: python

   import numpy as np, matplotlib
   matplotlib.use("Agg")
   import matplotlib.pyplot as plt
   import cartopy.crs as ccrs

   lon = np.arange(-180, 180, 2.5)          # 经度：-180, -177.5, ..., 178.75
   lat = np.arange(-75, 76, 1.0)
   LON, LAT = np.meshgrid(lon, lat)
   # "到日界线的最短球面距离": 经度 +-180 都是同一根线
   dist = np.minimum(np.abs(LON - 180), np.abs(LON + 180))
   TEMP = 18 * np.cos(np.deg2rad(LAT)) + 25 * np.exp(-((dist) ** 2) / 6.0)

   fig = plt.figure(figsize=(10, 4.4))
   ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())  # 默认中央经线 0
   pc = ax.pcolormesh(LON, LAT, TEMP, cmap="coolwarm", shading="auto",
                      transform=ccrs.PlateCarree())
   fig.colorbar(pc, shrink=0.8)
   ax.set_title("warm ridge crossing +-180 on central_longitude=0 -> white seam at map edge")
   fig.savefig(r"...\sim\10b2_seam_pcmesh.png", dpi=110, bbox_inches="tight")

**像素证据**\ ：对保存的图统计“地图左右两侧 2%
宽度内的白色（空白）占比”，\ ``central_longitude=0`` 时\ **左缘
0.98、右缘 0.90** 皆近乎全白；改用 ``central_longitude=180``
后\ **左缘降到
0.06**\ ，白缝消失。这把「白缝跟着经度不连续线走」坐实了。

**原因（地理学解释，务必理解）**\ ：地球经线是\ **周期性的**——178.9°E 和
-179.1°E 其实只隔约 2°，是全球邻接的两格；但文件里经度数组
``lon = -180..180`` 是把这条线\ **硬生生切开摊平**\ 存储的，第 0
格（-180）和第 1
格相邻，最后一格（+180）和“虚拟的下一格(-180)”在\ **数组头尾两端**\ 。当你用中央经线为
0 的 PlateCarree 画全球图，图幅左右两条边正好对齐 ±180，Cartopy
在「末格(+178°)与下一格(-179°)」之间做插值填色时，发现这两格在数组里相距不是
2° 而是
``360°-``——它宁可留白，也不愿把颜色“绕地球一圈”缝合。于是经度不连续性，就在地图边缘变成一条白缝。\ **也就是
PPT 里说的：\ ``nc 文件存储的问题，在 0 度经线上出现白条``\ 。**

**解决办法**\ ：三选一（都要确保“数据经度网格”与“地图如何看待经度”一致）：

1. **投影中央经线对准数据断裂点**——数据是 0–360，就把轴与 ``transform``
   都设 ``PlateCarree(central_longitude=180)``\ ；数据是
   -180–180，就常保留默认（中央 0）。这样 **180
   那条“缝”正好藏在图幅中央（日界线画在地图中间），左右两侧不再有经度跳跃**\ ：

.. code:: python

   proj = ccrs.PlateCarree(central_longitude=180)
   fig, ax = plt.subplots(subplot_kw={"projection": proj})
   pc = ax.pcolormesh(LON, LAT, TEMP, cmap="coolwarm", shading="auto", transform=proj)
   # 轴投影与数据投影都用同一个 180 中央 —— 白色竖缝消失（图上见 10b2_seam_fixed.png）

2. **``cartopy.util.add_cyclic_point``
   补一列循环格点**\ ：把经度首尾接起来（在经度数组末尾再接一个
   ``lon[0]+360`` 的副本列），Cartopy 就能把末列和首列连续缝合：

.. code:: python

   from cartopy.util import add_cyclic_point
   TEMP_cyc, lon_cyc = add_cyclic_point(TEMP, coord=lon)   # TEMP 形如 (nlat, nlon)
   proj = ccrs.PlateCarree(central_longitude=180)
   LONc, LATc = np.meshgrid(lon_cyc, lat)
   ax.pcolormesh(LONc, LATc, TEMP_cyc, transform=proj, shading="auto")

3. **手动平移经度**\ ：全局数据多是从 ``-180..180``\ （或
   ``0..360``\ ）来的，可先用 ``(lon+180) % 360``
   并把数据按新经度重排，让它与中央 180 的图幅对齐（见 10.1.2 代码）。

..

   **气象/地理场景一句话**\ ：\ ``-180°E`` 和 ``180°E``
   在地球上是同一根经线，好比「标准子午线」0° 与 360°
   也是同一根——可平铺在地图册上，人非要把球皮沿某根经线剪开摊平，剪开的那条缝就叫\ **经度不连续线（dateline
   /
   剪口）**\ 。你的图在哪条经线上出现白缝，哪条经线就是你手里的“剪子剪开的地方”。要做的不是“把缝磨平”，而是\ **让剪口避开你要看的区域**\ ，或者\ **用
   ``add_cyclic_point`` 把剪口计价缝合回去**\ 。

--------------

.. _1012-数据-0360-与画布--180180-混用右半边世界-0360-白条:

10.1.2 数据 0–360 与画布 -180–180 混用（「右半边世界」+ 0/360 白条）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 异常现象描述**\ ：很多再分析（ERA5
部分变量、WRF/模式输出）经度存成 **0–360**\ ，而你用的
``ccrs.PlateCarree()`` 画布默认把经度当 **-180–180** 解读。把 0–360
数据直接 ``pcolormesh``
上去，地图右半边会出现“整个世界被塞进来又错位”的样子，0/360
那条接缝同样裂成白条；更坑的是你\ **完全看不出哪不对**\ ，因为程序照跑、图也能存。

.. code:: python

   lon = np.linspace(0, 360, 97)             # 数据经度 0..360
   lat = np.linspace(-90, 90, 37)
   LON, LAT = np.meshgrid(lon, lat)
   TEMP = 25 * np.cos(np.deg2rad(LAT)) + 10 * np.sin(np.radians(LON))

   # 错：画布中央 0，数据却 0..360
   ax1 = plt.subplot(projection=ccrs.PlateCarree())
   pc = ax1.pcolormesh(LON, LAT, TEMP, transform=ccrs.PlateCarree(), shading="auto")  # 静默错位

**原因 / 解决办法**\ ：\ ``transform=ccrs.PlateCarree()``
都等价的——但「用 0–360 数据」配上「中央经线 0 的轴」时，Cartopy 把 >180
的那些度全部当成了东度西边（-…°），整片东半球叠错。正确做法：\ **要么把数据平移成
-180..180**\ ，要么\ **把轴与 ``transform`` 的中央经线也设成 180 以匹配
0–360**\ ：

.. code:: python

   # 方案 A：把 0..360 重排成 -180..180（经纬都平移对齐）
   lon2 = (lon - 180) % 360 - 180             # 0..360 -> -180..180
   order = np.argsort(lon2)
   proj = ccrs.PlateCarree()                  # 中央 0，匹配 -180..180
   ax.pcolormesh(lon2[order], lat, TEMP[:, order],
                 transform=proj, shading="auto", cmap="coolwarm")

   # 方案 B：轴与数据都用中央 180 的 PlateCarree（保持 0..360 不动）
   proj2 = ccrs.PlateCarree(central_longitude=180)
   ax2 = plt.subplot(projection=proj2)
   ax2.pcolormesh(LON, LAT, TEMP, transform=proj2, shading="auto", cmap="coolwarm")

..

   **排查经验（联网补充）**\ ：若你混合两个数据源（一个 -180..180、一个
   0..360）在同一张图，二者会自动错位半个地球——这是最阴险的「0-360 与
   -180-180 混用」静默错误（对应任务清单第 9 点）。动手前务必
   ``print("lon min/max =", lon.min(), lon.max())``
   确认经度范围，再决定要不要平移或换 ``central_longitude``\ 。

--------------

.. _1013-进阶用-xarray-的经度换球roll-补循环:

10.1.3 进阶：用 xarray 的经度换球（roll）/ 补循环
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果数据是 xarray 读进来的全球场，不必手写平移。Cartopy 推荐用 xarray 的
``.roll()`` 配合经度重排来做 wrap，或用
``cartopy.util.add_cyclic_point``
补齐首尾。课堂西北区域图没有全球白条困扰，这里只需知道：\ **凡是看到全球图中央（或
±180 / 0）一缕白条，第一反应就是经度周期性没处理好。**
处理要点只有一句：\ **让「数据切断的经线」和你「地图中央的经线」错开。**

--------------

.. _102-transform-与-projection这两个参数别搞混第-10-章强调得最多的坑:

10.2 transform 与 projection：这两个参数别搞混（第 10 章强调得最多的坑）
------------------------------------------------------------------------

.. _1021-漏写-transformccrsplatecarree在-platecarree-下静默通过换投影才爆发:

10.2.1 漏写 ``transform=ccrs.PlateCarree()``\ ：在 PlateCarree 下\ **静默通过**\ ，换投影才“爆发”
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 异常现象描述**\ ：教科书、用户指南反复强调 ``transform``
是坐标变换、最容易被遗漏。但你如果\ **刚好**\ 用 ``PlateCarree``
当画布投影，又漏写了
``transform=``\ ，往往会\ **很顺地画出正确的图**——因为 PlateCarree
的“显示坐标系”就是经纬度，数据按经纬度贴上去天然就对：

.. code:: python

   lon = np.linspace(90, 112, 45); lat = np.linspace(32, 43, 33)
   LON, LAT = np.meshgrid(lon, lat)
   TEMP = 10 + 0.5 * (40 - LAT) - 0.02 * (LON - 101) ** 2
   fig = plt.figure(figsize=(10, 5))
   ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
   ax.contourf(LON, LAT, TEMP, levels=15, cmap="coolwarm")   # 漏 transform：在 PlateCarree 下仍画对!

**为什么这是更凶的坑**\ ：因为 PlateCarree
掩盖了错误！等你哪天按用户指南的“拓展”去换
``LambertConformal``\ （西北兰勃脱）或 ``Mercator``\ ，漏写
``transform``
的数据会被当成那座投影的平面坐标（米），立刻错位/消失——而那时你已经“学会了”错误写法。真正严谨的姿势：\ **``transform=``
永远显式写上
``ccrs.PlateCarree()``\ ，养成肌肉记忆，不赌投影恰好一样。**

**真实现象（非 PlateCarree 投影上漏 transform）**\ ：把西北数据画在
``LambertConformal`` 轴上但不写 ``transform``\ ，图完全乱/几乎空白（配图
``10d_lambert_notransform.png``\ ）；scatter
一个点更是直接跑没影（\ ``10d_scatter_notransform.png``\ ）。

   **气象/地理场景一句话**\ ：\ ``transform``
   是给数据贴的「经纬度身份证」，告诉
   Cartopy「这份数据原始家住在经纬网上、还没投影过」。PlateCarree
   就像“你恰好把图铺在经纬网上”，所以漏贴身份证也不扣罚；一旦换到兰勃脱/墨卡托，就变成“把写满经纬度的户籍本直接当像素/米坐标去贴”，哪能不跑偏。

.. _1022-transform-与-projection-二者互换了搞混:

10.2.2 ``transform=`` 与 ``projection=`` 二者互换了/搞混
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 现象描述**\ ：把 ``transform`` 误当装饰性参数删掉，或把
``transform=ccrs.PlateCarree()`` 写成 ``ccrs.LambertConformal()``
之类（错误地认为“数据应该用跟我画布一样的投影变换”），数据会被投影二次，图层整体移位、扭曲。

**核心区分表**\ ：

+--------------------+-------------------------------------------------------------------------+------------------------+----------------------------------------------------+
| 参数               | 出现在哪                                                                | 含义                   | 例子                                               |
+====================+=========================================================================+========================+====================================================+
| ``projection=...`` | 创建\ **画布轴**\ 时（\ ``plt.subplots(subplot_kw=...)``\ ）            | 这张地图用哪种投影摊平 | ``projection=ccrs.LambertAzimuthalEqualArea(...)`` |
+--------------------+-------------------------------------------------------------------------+------------------------+----------------------------------------------------+
| ``transform=...``  | 每个\ **绘图调用**\ （\ ``contourf/scatter/quiver/text/pcolormesh``\ ） | 数据本身的原始坐标系   | ``transform=ccrs.PlateCarree()``\ （NetCDF         |
|                    |                                                                         |                        | 的经纬格点）                                       |
+--------------------+-------------------------------------------------------------------------+------------------------+----------------------------------------------------+

..

   口诀：\ **画布选 ``projection``\ （舞台搭在哪），数据标
   ``transform``\ （演员从哪来）。** 数据一直是经纬格点，所以
   ``transform`` 几乎永远是
   ``ccrs.PlateCarree()``\ ；只有你想把“已经投影好的坐标”画上时才改。西北数据
   ``transform=ccrs.PlateCarree()`` 是铁律。

.. _1023-text-与-scatter-同样要-transform:

10.2.3 ``text`` 与 ``scatter`` 同样要 ``transform``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   ax.scatter(103.83, 36.06, c="black", s=30, transform=ccrs.PlateCarree())  # 兰州站
   ax.text(104.2, 36.06, "兰州站", fontsize=9, transform=ccrs.PlateCarree())

漏掉任何一个，点在 ``LambertConformal`` 等非 PlateCarree
画布上就定位错（配图 ``10d_text_notransform.png``\ ）。与 ``contourf``
同一道理——**所有空间绘图函数 ``contourf/scatter/quiver/text/pcolormesh``
的 ``transform`` 一个都不能少**\ 。

   **气象/地理场景一句话**\ ：兰州站 (103.83°E, 36.06°N)
   想标在地图上，\ ``scatter`` 不写
   transform，等于你只报了个“103.83、36.06
   两个数”，没告诉人家这两个数是不是经纬度——在兰勃脱画布上，它被当成以米为单位的平面坐标，站名自然跑到荒郊野岭去了。

--------------

.. _103-坐标范围与投影冲突set_extent--crs--经度顺序--单位:

10.3 坐标范围与投影冲突：\ ``set_extent`` / ``crs=`` / 经度顺序 / 单位
----------------------------------------------------------------------

.. _1031-set_extent-经纬序写反画布变成一片空白:

10.3.1 ``set_extent`` 经纬序写反：画布变成一片空白
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实现象描述**\ ：\ ``set_extent`` 的正确顺序是
``[西经, 东经, 南纬, 北纬]``\ ，即 ``[90, 112, 32, 43]``\ 。写成
``[32, 43, 90, 112]``
后，代码不报错，但画布范围完全错乱——像素统计显示内容占比仅
~0.03（几乎全白）（配图 ``10e_extent_wrongorder.png``\ ）。

.. code:: python

   ax.set_extent([32, 43, 90, 112], crs=ccrs.PlateCarree())   # 错误：把纬度当经度
   # 正确：ax.set_extent([90, 112, 32, 43], crs=ccrs.PlateCarree())

**原因**\ ：\ ``[西,东,南,北]`` 把 90–112°E 误当纬度、32–43°N
误当经度，二者在经纬网上找不到交叉区域，于是渲染出一片几乎没有内容的空白窗口。

.. _1032-set_extent-漏-crs尤其非-platecarree-画布:

10.3.2 ``set_extent`` 漏 ``crs=``\ （尤其非 PlateCarree 画布）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实现象描述**\ ：在兰勃脱/兰伯特等面积投影的画布上写
``ax.set_extent([90,112,32,43])`` 而\ **不写
``crs=ccrs.PlateCarree()``**\ ，那四个数字会被当成\ **该投影自身的平面坐标**\ （米）。因为
90/112
作为“米”远超该投影量程，窗口被挤到远处，图上明明画了数据却“找不到角度”，成为奇怪的空白或极狭窄条带（配图
``10e_extent_nocrs.png``\ ）。正确写法永远带 ``crs=``\ ：

.. code:: python

   proj = ccrs.LambertAzimuthalEqualArea(central_longitude=101, central_latitude=38)
   ax = plt.subplot(projection=proj)
   ax.set_extent([90, 112, 32, 43], crs=ccrs.PlateCarree())   # crs 必须有

**排查经验**\ ：\ ``set_extent`` 没裁剪效果的三大元凶——①顺序写反、②漏
``crs=``\ 、③给的经纬范围就不在数据/图幅内。先 ``print`` 再逐条核对。

   **气象/地理场景一句话**\ ：\ ``set_extent``
   像相机的“取景框”，\ ``crs=ccrs.PlateCarree()``
   是告诉相机“我报的这串数单位是经纬度”；漏了它，等于把“经纬度”当成“像素坐标”去调焦，相框自然套不住你的西北格点。

.. _1033-经纬度单位混淆把弧度当度把-0-360-当--180-180:

10.3.3 经纬度单位混淆：把弧度当度、把 0-360 当 -180-180
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 现象描述**\ ：不小心把经度做成弧度（如三角函数 ``np.cos(lon)``
忘了 ``np.deg2rad``\ ，或从某些库拿到的项目已把经纬换算成弧度），或混用
0–360 / -180–180
两套经度，图上要素严重错位、旋转、跑偏——程序通常不报错。

**排查经验**\ ：画任何要素前 ``print(lon.min(), lon.max())``\ ：

- 若数值落在 ``[0, 6.28]`` 左右 → 是弧度，需 ``np.rad2deg(lon)``\ ；
- 若落在 ``[0, 360]`` → 语义“东经累加”，需与 ``central_longitude``
  匹配或平移成 ``[-180,180]``\ （见 10.1.2）。

..

   **气象/地理场景一句话**\ ：气象里几乎所有“觉得纬度不对劲、经度不对劲”的疑难杂症，九成是\ **单位或范围**\ 二选一错位——经纬度永远是“度”，不是弧度；全球图永远先想清楚它是
   0–360 还是 -180–180 的“户籍”。

--------------

.. _104-contourf--pcolormesh-在地图轴上的经典报错真实-traceback:

10.4 ``contourf`` / ``pcolormesh`` 在地图轴上的经典报错（真实 Traceback）
-------------------------------------------------------------------------

.. _1041-typeerror-input-z-must-be-2d-not-3d多留了一个-time-维:

10.4.1 ``TypeError: Input z must be 2D, not 3D``\ （多留了一个 time 维）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：\ ``xarray`` 读进来很多 NetCDF 的气温是
``(time, lat, lon)`` 三维。直接 ``ax.contourf(lon, lat, temp3d)`` 时报：

.. code:: text

     File "...\matplotlib\contour.py", line 1385, in _check_xyz
       raise TypeError(f"Input z must be 2D, not {z.ndim}D")
   TypeError: Input z must be 2D, not 3D

**原因**\ ：\ ``contourf`` 要求 z
是\ **二维场**\ （每格一个值）；\ ``temp3d`` 还带着 time 轴（3
维）。气象新手里最常见的写法是把整个时间序列直接扔进 ``contourf``\ 。

**解决办法**\ ：先取单时刻，\ ``isel/sel`` 后 ``.squeeze()`` 掉长度 1
的维，再画：

.. code:: python

   temp2d = ds.temp.sel(time="2024-01-01").squeeze()   # (lat, lon)
   ax.contourf(lon, lat, temp2d, levels=20, cmap="coolwarm",
               transform=ccrs.PlateCarree())

..

   **气象/地理场景一句话**\ ：你想画“某一时候的气温场”，手里却攥着“整段
   30 年逐日 + 每天全球格点”的三维大货柜——``contourf``
   只认一张“横纬纵经的快照”，要先 ``sel`` 取出你要的那一帧再画。

.. _1042-typeerror-shapes-of-x--and-z--do-not-match转置-t-惹的祸:

10.4.2 ``TypeError: Shapes of x (...) and z (...) do not match``\ （转置 .T 惹的祸）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：\ ``meshgrid(lon, lat)`` 出来的网格 shape 是
``(纬度数, 经度数)`` = ``(33, 45)``\ （lat 有 33 个、lon 有 45
个）。若你给 z 的是这个 2D 数组的\ **转置
``.T``**\ （\ ``(45, 33)``\ ），shape 就对不上：

.. code:: text

     File "...\matplotlib\contour.py", line 1406, in _check_xyz
       raise TypeError(
   TypeError: Shapes of x (33, 45) and z (45, 33) do not match

**原因 / 解决办法**\ ：\ ``contourf(x, y, z)`` 三者的第 0 维、第 1
维必须一一对应（都 ``(nlat, nlon)``\ ）。出现此错十有八九是 ``.T``
转置或 ``(lon,lat)`` 与 ``(lat,lon)`` 约定混了。统一口径：

.. code:: python

   LON, LAT = np.meshgrid(lon, lat)            # 22 行第 (nlat, nlon)
   print(LON.shape, TEMP.shape)                # 两者必须都是 (33, 45)
   # TEMP 若不是 (nlat,nlon)，用 TEMP.T 或按坐标来源校正

..

   **气象/地理场景一句话**\ ：NetCDF 里 ``temp`` 常存成
   ``(lat, lon)``\ ，\ ``meshgrid`` 默认也是
   ``(lat, lon)``——一个顺的，别在中间莫名 ``.T`` 一下把它翻成
   ``(lon, lat)``\ ，否则“大小坑”就填不平。

.. _1043-pcolormesh-报-dimensions-of-c--should-be-one-smaller-than-x--y:

10.4.3 ``pcolormesh`` 报 ``Dimensions of C ... should be one smaller than X / Y``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：给 ``pcolormesh`` 传 1D 的 ``lon``\ （45
个）、\ ``lat``\ （33 个），z 却是 ``(33,45)``\ ，用
``shading="flat"``\ （默认）时：

.. code:: text

     File "...\matplotlib\axes\_axes.py", line 6060, in _pcolorargs
       raise TypeError(f"Dimensions of C {C.shape} should")
   TypeError: Dimensions of C (33, 45) should be one smaller than X(33) and Y(45) while using shading='flat' see help(pcolormesh)

**原因**\ ：\ ``pcolormesh`` 历史上把 x/y
当成“单元格顶点的经纬网”，\ ``shading='flat'`` 要求 **C 的每个维度比 X/Y
各少一个顶点**\ （45 个经度顶点 → 44 个经度单元格）。你数据 z 是
``(33,45)``\ ，与“顶点数-1”的规则对不上。

**解决办法**\ ：

- 最简单：\ ``shading="auto"``\ （自动在 ``flat`` 与 ``nearest``
  间选合适的，单元格对齐数据格点）——本项目西北图推荐，多半直接通过：

.. code:: python

   pc = ax.pcolormesh(lon, lat, TEMP, shading="auto", cmap="coolwarm",
                      transform=ccrs.PlateCarree())

- 或把 z 裁掉末行末列，让 C = ``(nlat-1, nlon-1)`` 与“顶点-1”一致。

**对照（能通过的写法）**\ ：\ ``pcolormesh`` 传 1D ``lon``/``lat`` +
``shading="auto"``\ ，z 为 ``(nlat, nlon)``——正常出图（配图
``10g_pcolormesh_ok.png``\ ）。

   **气象/地理场景一句话**\ ：\ ``pcolormesh``
   把它当作“一个个色块”画，色块的数目永远比格点少一（首尾两格各算半个）。就像
   45 把尺子量出的 44
   个间隔——你给足了格子却忘了颜色数要比格子少一，人家就喊“你对不上”。

.. _1044-contourf-里-levels-数量与色标问题nan-破洞:

10.4.4 ``contourf`` 里 ``levels`` 数量与色标问题、NaN 破洞
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 现象描述（静默 + 报错各一种）**\ ：

- 传 ``levels`` 一个\ **数值**\ （如 ``levels=20``\ ）→ 自动在
  ``vmin..vmax`` 里切 20 层；若数据全 NaN
  或范围小，等值线可能“画不出来”或只零星几根。
- 传 ``levels=[]``\ （空列表）或传一个\ **不含任何数据数值**\ 的列表 →
  ``contour`` 会报与层级相关的 ``ValueError``\ ，或画出空图。
- 数据里混入 ``NaN``\ （缺测没转）→
  填色在那些格子上“破洞”，露出白/底图。

**排查经验**\ ：画之前先
``print(np.nanmin(TEMP), np.nanmax(TEMP), np.isnan(TEMP).sum())``\ ；缺测先
``TEMP = np.where(TEMP > 900, np.nan, TEMP)`` 之类统一成 NaN，再用
``vmin/vmax`` 约束色标范围（本章“十二图统一 vmin/vmax”正是为可比性）。

   **气象/地理场景一句话**\ ：等值线是“数学意义上的等高线”，\ ``levels``
   列表就是你要画几层、画在哪些值；给了它却一个都不在数据范围内，等于“纸上画飞机航迹却不在你这段空域”，自然空无一物。先核对量级和缺测，再谈分层。

--------------

.. _1045-全球-contourf-跨投影边界typeerror-geometrycollection-object-is-not-subscriptable进阶坑:

10.4.5 全球 ``contourf`` 跨投影边界：\ ``TypeError: 'GeometryCollection' object is not subscriptable``\ （进阶坑）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：把全球数据（0–360）直接 ``contourf`` 到一个
``PlateCarree(central_longitude=180)`` 的画布上，个别版本/组合会让
Cartopy 把跨越日界线的等值线环投影成碎片：

.. code:: text

     File "...\cartopy\crs.py", line 1270, in _rings_to_multi_polygon
       return sgeom.MultiPolygon(polygon_bits)
     File "...\shapely\geometry\multipolygon.py", line 76, in __new__
       shell = ob[0]
   TypeError: 'GeometryCollection' object is not subscriptable

**原因**\ ：全球等值线跨越投影边界时被切成“几条环”，拼合时出现
``GeometryCollection``\ （混合几何），Cartopy 组装 ``MultiPolygon``
失败。是 cartopy 在跨日界线全局 ``contourf`` 上的一个已知边角问题。

**解决办法**\ ：这类“全球填色+跨日界线”优先用 **``pcolormesh`` +
``add_cyclic_point``**\ ，或先 ``add_cyclic_point`` 再
``contourf``\ ，或把数据平移成与图幅中央一致（见
10.1.2）后再画。\ **普通西北局地场不会踩到**\ ，这里只是让你知道：全球
``contourf`` 踩坑时的第一招是改 ``pcolormesh``/补循环。

--------------

.. _105-shapefile-读取与-api-弃用deprecationwarning--旧函数:

10.5 shapefile 读取与 API 弃用（DeprecationWarning / 旧函数）
-------------------------------------------------------------

.. _1051-旧版-api-已移除attributeerror-geoaxes-object-has-no-attribute-natural_earth_shp:

10.5.1 旧版 API 已移除：\ ``AttributeError: 'GeoAxes' object has no attribute 'natural_earth_shp'``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：老教程/老代码里那句
``ax.natural_earth_shp('10m_land')`` 在新版 Cartopy 已经不存在：

.. code:: text

     File "...\sim\10j_attr.py", line 17, in <module>
       ax.natural_earth_shp("10m_land")
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   AttributeError: 'GeoAxes' object has no attribute 'natural_earth_shp'

**原因**\ ：\ ``GeoAxes.natural_earth_shp`` 是很早版本的接口，新版本改用
``cartopy.feature`` 的 ``cfeature.*`` 或 ``shapereader.Reader`` +
``add_geometries``\ 。凡 ``AttributeError``
且方法名带时间感（\ ``natural_earth_shp``\ 、\ ``add_feature`` vs 旧
``ax.add_geometries(Reader...)``\ ），第一怀疑就是\ **你抄的是老
API，版本对不上**\ 。

**解决办法**\ （读 shapefile 画自定义边界的标准写法）：

.. code:: python

   import cartopy.crs as ccrs
   from cartopy.io import shapereader

   fname = shapereader.natural_earth(resolution="10m", category="cultural",
                                     name="admin_1_states_provinces")   # 或你自己的 .shp 路径
   # 用 Reader 读本地 shp:
   records = list(shapereader.Reader("我的省界.shp").geometries())
   ax.add_geometries(records, crs=ccrs.PlateCarree(),
                     facecolor="none", edgecolor="gray", linewidth=0.5)

..

   **排查经验**\ ：\ ``DeprecationWarning``
   提示里往往会带上要替换的新对象（例如
   ``Use cartopy.mpl.path.shapely_to_path instead``\ ）。照着提示改即可；若提示只写“将被移除”，就先查官网当前文档里的同功能新写法。

.. _1052-真实-deprecationwarningcartopymplpatchgeos_to_path-弃用:

10.5.2 真实 ``DeprecationWarning``\ ：\ ``cartopy.mpl.patch.geos_to_path`` 弃用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ （\ ``geos_to_path``
在新版本已标记弃用，但老代码常出现）：

.. code:: text

   D:\...\10n_patch_deprec.py:13: DeprecationWarning: geos_to_path is deprecated and will be removed in a future
   release.  Use cartopy.mpl.path.shapely_to_path instead.
     path = patch.geos_to_path(ring)

**说明**\ ：这是一条\ **警告**\ ，程序照跑、返回结果也没变（我们运行后
``geos_to_path`` 仍正常返回 ``list``\ ）；但 Cartopy
官方已把它标注弃用。看到 ``DeprecationWarning`` 的正确态度与 00
篇一致：\ **它不打断你，但提示你“老的写法会被删除”，趁早在作业里换成新写法**\ ，别等库升级后一下链式报错。

**关于 ``cartopy.io.shapereader`` 的澄清**\ ：在你 conda 装的 Cartopy
0.25 里，\ ``shapereader.Reader`` 与 ``shapereader.natural_earth``
是\ **当前正式 API（并未弃用）**\ 。新手最常见的“shapefile
部分弃用”其实来自两点——①把老网页上的 ``ax.natural_earth_shp``
当接口抄（见 10.5.1 报错）；②混用 ``pip``/``conda`` 装了奇怪的 cartopy
版本。\ **读 shapefile 一律走 ``shapereader.Reader`` +
``add_geometries``**\ ，就不会踩坑。

   **气象/地理场景一句话**\ ：\ ``DeprecationWarning``
   就是国家站仪器的“换代提前通告”——旧观云器还在用，但气象局已经官宣它明后年退役，用新站（新
   API）才是正道。看到 “is deprecated and will be
   removed”，翻译过来是“给力用旧写法留着，但该准备了”。

--------------

.. _106-网络--数据下载add_feature--coastlines--缓存:

10.6 网络 / 数据下载：\ ``add_feature`` / ``coastlines`` / 缓存
---------------------------------------------------------------

.. _1061-首次-add_featurecoastlines-联网下载失败urlerror--超时:

10.6.1 首次 ``add_feature``/``coastlines`` 联网下载失败：\ ``URLError`` / 超时
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ （断网 / 被墙 / 缓存未命中，首次调用触发）：

.. code:: text

     File "...\cartopy\io\shapereader.py", line 374, in acquire_resource
       shapefile_online = self._urlopen(url)
     File "...\urllib\request.py", line 1347, in do_open
       raise URLError(err)
   urllib.error.URLError: <urlopen error [WinError 10061] 由于目标计算机积极拒绝，无法连接。>

**原因**\ ：\ ``cfeature.COASTLINE``\ 、\ ``ax.coastlines()``\ 、\ ``cfeature.LAKES/BORDERS/RIVERS``
首次使用要\ **联网下载 Natural Earth 的矢量 shp**
并缓存。断网、被墙（国内常见）、或公司代理拦截，就会在
``cartopy.io.shapereader.acquire_resource`` 这一层抛 ``URLError`` /
``TimeoutError``\ 。\ **注意区分：这是“网络下载失败”，不是代码语法错**——排查时先看是不是
``URLError / [WinError ...] / Connection ...`` 之类，别误改投影代码。

**解决办法**\ ：

1. **联网环境下一次性预下载**\ ：先 ``import cartopy; cartopy.config``
   看缓存目录，手动下载 Natural Earth
   放到该目录（或让程序首跑完成一次下载）；
2. **设本地缓存目录，避免课堂信道挤爆**\ ：

.. code:: python

   from cartopy import config
   import os
   os.makedirs("./ne_cache", exist_ok=True)
   config["data_dir"] = os.path.abspath("./ne_cache")   # 缓存放项目内，离线/多机复用

3. 离线环境就别硬刚
   ``add_feature(COASTLINE)``\ ；可先画填色主图，把海岸线留作“联网后补”。

..

   **气象/地理场景一句话**\ ：\ ``coastlines()``
   第一次画就像第一次查全网海图——要先上网“下载一副海岸线底图”；断网时它就卡在“下载”这步（\ ``URLError``\ ），不是你的填色代码错了。预下载并指向缓存目录，等于把海图先拷进本地图库，之后离线也能画。

.. _1062-别把网络下载超时误当绘图代码报错:

10.6.2 别把「网络下载超时」误当「绘图代码报错」
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 排查经验**\ ：已有数据也正常读出、\ ``contourf`` 也正常，但一调
``ax.coastlines()`` 就卡住/报 ``URLError``\ 。这往往是缓存目录里没有 NE
数据，网络又不通。判据：报错信息含
``acquire_resource``\ 、\ ``_urlopen``\ 、\ ``urllib.error``\ 、\ ``WinError``\ 、\ ``TimeoutError``\ 、\ ``Connection``
等字眼 → 是网络；含
``cartopy\crs.py``\ 、\ ``contour.py``\ 、\ ``TypeError/ValueError`` →
才是代码。

   **气象/地理场景一句话**\ ：就像发传真给对方没打通——``URLError``
   是“对方电话没接”（网络/服务器），不是“我传真内容写错”（代码）。先分清这两类，再去改参数。

--------------

.. _107-版本与依赖modulenotfounderror--attributeerror-全家桶:

10.7 版本与依赖：\ ``ModuleNotFoundError`` / ``AttributeError`` 全家桶
----------------------------------------------------------------------

.. _1071-缺核心依赖modulenotfounderror-no-module-named-pyprojshapelypyshp:

10.7.1 缺核心依赖：\ ``ModuleNotFoundError: No module named 'pyproj'/'shapely'/'pyshp'``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 /
真实报错信息**\ （在你机器上缺包/环境没激活时，\ ``import cartopy``
或首次画图会触发）：

.. code:: text

   ModuleNotFoundError: No module named 'cartopy'           # 压根没装 cartopy / 环境没激活
   ModuleNotFoundError: No module named 'pyproj'            # cartopy 在 import cartopy.crs 时找不到 pyproj
   ModuleNotFoundError: No module named 'shapely'           # add_feature/几何运算找不到 shapely
   ModuleNotFoundError: No module named 'pyshp'             # 读 shapefile 时找不到 pyshp(shapefile.py 包)

**原因**\ ：Cartopy 是“地图引擎壳”，它靠 ``pyproj``\ （PROJ
投影库）、\ ``shapely``\ （几何）、\ ``pyshp``\ （shapefile
解析）在底层工作。\ ``cartopy`` 装了但不代表它也装了——尤其
``pip install cartopy`` 老版本时坑多。

**解决办法（铁律）**\ ：\ **优先
``conda install cartopy shapely pyproj pyshp``**\ （conda 会把这些底层 C
库 GEOS/PROJ 一起配好），不要只
``pip install cartopy``\ 。装了之后若仍报，检查：①Conda 环境是否
activate（见第 1 章）；②是不是在自己脚本里用了 ``import cartopy.crs``
但没先 ``import cartopy`` 的初始化链（默认会链式）。

   **气象/地理场景一句话**\ ：Cartopy
   像“绘图外包公司”，\ ``shapely/pyproj/pyshp``
   是它雇的三个施工队（做几何/投影/读边界）。只装了“公司”没招“施工队”，一上项目就喊“没有人干活”（\ ``ModuleNotFoundError``\ ）。conda
   打包会一起招齐，这正是文档反复强调“别只用 pip”的原因。

.. _1072-版本间-api-改名导致的-attributeerror:

10.7.2 版本间 API 改名导致的 ``AttributeError``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: text

   AttributeError: module 'cartopy.crs' has no attribute 'PlateCarree'   # 记错模块名/拼错
   AttributeError: 'GeoAxes' object has no attribute 'natural_earth_shp' # 旧 API 移除（见 10.5.1）
   AttributeError: 'Gridliner' object has no attribute 'xlines'          # 属性改名/版本差

**原因**\ ：Cartopy 从 0.x
迭代很快，不少方法、类、参数名变过（\ ``natural_earth_shp``\ →\ ``add_geometries``\ 、某些
``*_style`` 属性→\ ``gridliner`` 新写法等）。看见 ``AttributeError``
且\ **你确定调用的是“某个对象的方法/属性”**\ ，先猜三点：拼错、对象类型不对（拿
``Gridliner`` 当 ``GeoAxes`` 用）、版本 API 变了。

**解决思路**\ ：

.. code:: python

   print(type(ax))                    # 确认到底是不是 GeoAxes
   print([a for a in dir(ax) if "coast" in a])   # 看真实有哪些方法
   import cartopy; print(cartopy.__version__)    # 先对版本再搜文档

.. _1073-proj-相关geographiccrs--网格报错进阶:

10.7.3 proj 相关：\ ``GeographicCRS`` / 网格报错（进阶）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pyproj`` 报 ``KeyError: 'proj'`` 或 ``ProjError: ...``
多在\ **数据自带投影字符串**\ 与 ``transform``
写死无关时出现；西北数据就是经纬格点，\ ``transform=ccrs.PlateCarree()``
不会触发。若报 proj 相关，优先查 ``pip 与 conda 混装``\ 导致 proj
二进制错位——重装一个干净环境即可。

   **气象/地理场景一句话**\ ：版本错配的 ``AttributeError``
   就像“用新版的仪器操作手册去开旧型号的探空仪”——方法按键对不上。先
   ``----.__version__`` 对齐手册版本，再能谈操作。

--------------

.. _108-图例--colorbar--子图--地理要素:

10.8 图例 / colorbar / 子图 / 地理要素
--------------------------------------

.. _1081-geoaxes-上加-colorbarfigcolorbarcontour-axax-shrink08:

10.8.1 GeoAxes 上加 colorbar：\ ``fig.colorbar(contour, ax=ax, shrink=0.8)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实现象**\ ：Cartopy 的轴是
``GeoAxes``\ （自带经纬刻度、固定纵横比）。直接不加 ``ax=`` 地用
``plt.colorbar(contour)``\ 、或想缩窄色标时，容易“吃掉/挤压地图”或警告。标准写法（已实测通过并出图，见
``10h_colorbar.png``\ ）：

.. code:: python

   cbar = fig.colorbar(contour, ax=ax, shrink=0.8, pad=0.02)
   cbar.set_label("气温 ℃", fontsize=11)
   cbar.ax.tick_params(labelsize=10)

多子图（2×2
季节对比）想共用一只色标：\ ``fig.colorbar(contour, ax=axes.ravel().tolist(), shrink=0.8, pad=0.02)``\ （\ ``ax=``
传子图列表）。

**注意中文字体**\ ：\ ``cbar.set_label("气温 ℃")``
若系统没配中文字体，保存时会刷屏
``UserWarning: Glyph ... missing from font(s) DejaVu Sans``\ ，图上相应中文变方框（见
10.9.4）。

.. _1082-地理要素-lakes--rivers--borders-与-add_geometries-投影错误:

10.8.2 地理要素 ``lakes / rivers / borders`` 与 ``add_geometries`` 投影错误
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 现象描述**\ ：\ ``ax.add_feature(cfeature.LAKES)``
画不出或位置怪，常常不是代码错而是\ **图层顺序**\ （先画了填色把要素盖住，或
``set_extent``
范围太小根本没盖到要素）。用户指南已给图层顺序口诀：\ **填色场 → 河流 →
海岸线 → 国界 → 站点标记**\ （自底到顶）。

用 ``Reader`` 读 shp 后
``add_geometries(geoms, crs=ccrs.PlateCarree())`` 时，\ ``crs``
参数必须写\ **数据的原始坐标系**——读的 shp 本身是经纬度，就写
``ccrs.PlateCarree()``\ ；若 shp 已是投影坐标，写对应投影。写错 →
要素整体错位/不显示（也是静默）。

   **气象/地理场景一句话**\ ：图层顺序就像“先铺桌布再摆餐具”——先画气温填色（桌布）再画河流国界（餐具），否则餐具被桌布盖住看不见。

.. _1083-批量绘图不关画布内存累积--卡顿:

10.8.3 批量绘图不关画布：内存累积 / 卡顿
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

用户指南强调循环里 ``plt.close(fig)``\ 。不关的话 ``fig``
累计占用内存，图越多越卡，甚至无报错误卡死。属“静默资源泄漏”（00 篇 0.5
节）。统一 ``vmin/vmax`` 保证十二图可比。

--------------

.. _109-气象静默错误不报错但结果错最阴险的一类:

10.9 气象静默错误（不报错但结果错）——最阴险的一类
-------------------------------------------------

.. _1091-站点经纬度数组装反点画到大洋图外:

10.9.1 站点经纬度数组装反：点画到大洋/图外
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实现象描述**\ ：\ ``ax.scatter(103.83, 36.06, ...)``
是“经度在前、纬度在后”。把它写成
``scatter(36.06, 103.83)``\ （先纬度后经度），兰州站就变成“东经
36°、北纬
103°”，跑出图外，图上只剩坐标刻度附近一个小点或根本看不见（配图
``10f_site_swap.png``\ ）。代码不报错、能存图——这就是静默错误。

.. code:: python

   ax.scatter(36.061, 103.831, c="red", s=60, transform=ccrs.PlateCarree())  # 装反，点消失
   # 正确：ax.scatter(103.831, 36.061, ..., transform=ccrs.PlateCarree())

**排查经验**\ ：凡清单上“站点没显示在预期位置”，先问两件事：①传参顺序对不对（lon
前 lat 后）；②\ ``transform`` 写了没有（非 PlateCarree 漏写会跑偏，见
10.2.3）。再核对 ``set_extent`` 是否覆盖该点经纬。

   **气象/地理场景一句话**\ ：兰州(103.83°E,
   36.06°N)你偏写成“北上南下”，等于给探测车发错了经纬度——它真跑到东经 36
   度的荒原去盘点，程序却一点不喊冤。先检查“经纬顺序”这四个字。

.. _1092-温度场-lonlat-与-latlon-切片反了图像被转置侧躺:

10.9.2 温度场 ``(lon,lat)`` 与 ``(lat,lon)`` 切片反了：图像被转置/侧躺
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实现象描述**\ ：NetCDF 里 ``temp`` 常是 ``(lat, lon)`` 或
``(lon, lat)`` 两种存储均可。若读进来的数组是 ``(lon,lat)`` 存法，你却用
``(lat,lon)``
的网格（\ ``meshgrid(lon,lat)``\ ）去对位，不报错但\ **地图的南北向和东西向会被偷偷对调/翻转**——等值线走向整个不对。真“shape
一致但顺序错”时，甚至报 ``Shapes of x ... and z ... do not match``\ （见
10.4.2）；顺序微妙错位时则静默地“侧躺”或“翻面”（\ ``contourf(lat, lon, ...)``
把经纬轴互换，图会反过来，见配图 ``10f_transposed.png``\ ）。

**排查经验**\ ：画第一张图前固定三步：

.. code:: python

   print(TEMP.shape)                 # 期望 (nlat, nlon)
   print(lon.shape, lat.shape)       # (nlon,), (nlat,)
   print("比较:", TEMP.shape[0], len(lat), "|", TEMP.shape[1], len(lon))

若第一个维度数≠\ ``len(lat)``\ ，多半存储是 ``(lon, lat)``\ ，需
``TEMP = TEMP.T``\ （并确认不再转重叠）。\ **先对齐维度语义，再谈绘图。**

   **气象/地理场景一句话**\ ：一张“横纬纵经”的表你偏偏当“横经纵纬”读，等于把地球横过来了画——等值线都不指向真实的北。这就是
   00 篇 0.5 节警告的静默坐标错位。

.. _1093-经纬-0360-与--180180-混用静默错位:

10.9.3 经纬 0–360 与 -180–180 混用（静默错位）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

详见
10.1.2。两个数据源经度范围不一致时，它们在图上会\ **相差整整半个地球**\ 地叠在一起、却无报错。判读见
10.3.3。

.. _1094-中文显示方框userwarning-glyph--missing-from-font:

10.9.4 中文显示方框：\ ``UserWarning: Glyph ... missing from font``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实警告**\ （没配中文字体时，保存含中文标题/色标地图会出现）：

.. code:: text

   D:\...\10h_colorbar.py:21: UserWarning: Glyph 27668 (\N{CJK UNIFIED IDEOGRAPH-6C14}) missing from font(s) DejaVu Sans.

**原因 / 解决办法**\ ：Matplotlib 默认字体 DejaVu Sans
不含汉字。配中文字体（\ ``SimHei`` / ``Microsoft YaHei``\ ，同第 9
章做法）后重画即可；若一时不想配字体，把标题/标签写成英文也是折中。

.. _1095-等值线画在图外整片空白数据范围与窗口不匹配:

10.9.5 等值线画在图外/整片空白（数据范围与窗口不匹配）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 现象描述**\ ：数据范围（比如西北全境 90–112°E）比
``set_extent`` 窗口（比如只框 103–104°）大很多，或多层 ``levels``
全在数据范围之外，图“该有的一片天空”却是空白。静默不报错。

**排查**\ ：\ ``print(np.nanmin(TEMP), np.nanmax(TEMP))`` 与
``levels``\ 、\ ``vmin/vmax``\ 、\ ``set_extent``
对一下，确保取景框、图层分档都落在数据实际范围里。

--------------

.. _1010-高频坑自查速查表含联网补充:

10.10 高频坑自查速查表（含联网补充）
------------------------------------

+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| 看到的现象/报错                                                               | 立刻联想到                      | 处理                                                  |
+===============================================================================+=================================+=======================================================+
| 地图出现竖白条                                                                | 经度不连续线（±180/0/360）与    | 统一经度/``add_cyclic_point``/平移到中央 180          |
|                                                                               | ``central_longitude`` 错位      |                                                       |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| 数据画到别处/消失                                                             | 漏 ``transform=``               | 补 ``transform=ccrs.PlateCarree()``                   |
|                                                                               | 或投影坐标系混                  |                                                       |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| ``set_extent`` 不裁剪/空白                                                    | 经纬序反、漏 ``crs=``\ 、弧度过 | ``set_extent([西,东,南,北], crs=ccrs.PlateCarree())`` |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| ``Input z must be 2D, not 3D``                                                | contourf 拿到带 time 的三维     | ``sel(time=...).squeeze()``                           |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| ``Shapes of x (..) and z (..) do not match``                                  | ``.T``                          | 统一 ``(nlat,nlon)``                                  |
|                                                                               | 转置、\ ``(lat,lon)/(lon,lat)`` |                                                       |
|                                                                               | 混用                            |                                                       |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| ``Dimensions of C ... one smaller than X/Y``                                  | pcolormesh 顶点-色块差一        | ``shading="auto"``                                    |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| ``URLError``/``WinError``/超时                                                | ``add_feature``/``coastlines``  | 预下载/设 ``config["data_dir"]`` 缓存                 |
|                                                                               | 要联网下载 NE                   |                                                       |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| ``ModuleNotFoundError: No module named 'pyproj/shapely/pyshp/cartopy'``       | 依赖没装/环境没激活/pip 装的坑  | ``conda install cartopy shapely pyproj pyshp``        |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| ``AttributeError: ... natural_earth_shp``                                     | 抄了老 API                      | 用 ``cfeature`` / ``add_geometries(Read)``            |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| ``DeprecationWarning: geos_to_path is deprecated ... Use ...shapely_to_path`` | 旧内部 API 弃用                 | 按提示换新写法                                        |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| 站点点到大洋/图外(静默)                                                       | 经纬顺序装反 / 漏 transform     | ``scatter(经, 纬, transform=...)``                    |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| 中文变方框 + ``Glyph missing``                                                | 没配中文字体                    | 配 SimHei/微软雅黑                                    |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| ``identical low and high ylims makes transformation singular``                | 范围退化成一个点                | 检查 ``set_extent``/首尾数据                          |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+
| ``GeometryCollection object is not subscriptable``                            | 全球 contourf 跨日界线边角 bug  | 改 ``pcolormesh``/``add_cyclic_point``                |
+-------------------------------------------------------------------------------+---------------------------------+-------------------------------------------------------+

..

   **收尾口诀（气象风）**\ ：看到 **白竖线**\ 先查 ``central_longitude``
   与经度范围；看到 **图层错位/点画到海里**\ 先查 ``transform=``
   和经纬顺序；看到 ``.do not match / one smaller / must be 2D``
   查维度与形状；看到 ``URLError / ModuleNotFoundError``
   先分清“网络/环境”再说；看到 ``DeprecationWarning / AttributeError``
   查版本
   API。\ **凡是“程序绿灯到底、图却别扭”的静默现象，一律三连问：transform
   贴了吗？经纬顺序对吗？0-360 与 -180-180 统一了吗？** —— 第 10
   章守门三问。
