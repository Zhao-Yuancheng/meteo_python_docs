Cartopy 气象绘图
===============================

配套 :ref:`tut-cartopy` 正文。共四题，难度递增，覆盖全球填色图、区域裁剪、地理要素叠加与兰伯特投影——全部围绕西北地区气温场的空间分布展开。每题给出 **提示** 与 **参考答案**，先自己动手写，再对照参考。

.. seealso:: 配套正文：:doc:`/user_guide/viz/cartopy`　·　术语参考：:doc:`/api/viz/ch10_terms`

**通用约定**：前提已安装 Cartopy。作图前在脚本开头统一导入：

.. code-block:: python

   import matplotlib.pyplot as plt
   import cartopy.crs as ccrs
   import cartopy.feature as cfeature   # 练习 3、4 用
   import xarray as xr

.. note::

   **数据说明**：本章统一使用贯穿项目的 NetCDF 气温格点场 northwest_temp.nc，由  统一提供。变量 temp 单位 ℃，网格覆盖经度 100°~110°E、纬度 30°~40°N。**注意 temp 是三维数组（time, lat, lon），绘图前必须先沿时间维求平均**，否则 contourf 会因维度不是二维而报错。读取方式沿用第 8 章：

   .. code-block:: python

      ds = xr.open_dataset("northwest_temp.nc")
      temp = ds["temp"].mean(dim="time")  # 三维 → 二维时间平均场

   若你本地暂时没有这份文件，可先看文末「数据自备：生成一份模拟气温场」小节，用几行 NumPy 代码生成一份经纬度格点场来练习——题目改的只是数据，换成模拟场后画图逻辑完全一致。

入门题
------

第 1 题 基础全球填色图
----------------------

题目要求：

1. 使用 PlateCarree 投影创建画布，绘制一张全球简易填色底图；
2. 加载 northwest_temp.nc 气温数据，用 contourf 绘制气温填色；
3. 添加海岸线，配置 colorbar 色条，并设置标题「全球气温场示例」；
4. 保存为 ex1_global_temp.png。

.. dropdown:: 参考答案


   .. code-block:: python

      import matplotlib.pyplot as plt
      import cartopy.crs as ccrs
      import xarray as xr

      ds = xr.open_dataset("northwest_temp.nc")
      temp = ds["temp"].mean(dim="time")  # 三维 (time,lat,lon) 先平均成二维

      plt.figure(figsize=(10, 6), dpi=100)
      ax = plt.subplot(projection=ccrs.PlateCarree())

      cs = temp.contourf(ax=ax, transform=ccrs.PlateCarree(),
                         levels=20, cmap="RdBu_r")
      ax.coastlines(linewidth=0.8)

      plt.colorbar(cs, shrink=0.7, label="气温(℃)")
      ax.set_title("全球气温场示例", fontsize=13)

      plt.savefig("ex1_global_temp.png", dpi=150)
      plt.show()

.. dropdown:: 易错点

   ① 忘记写 :term:`transform（数据坐标系声明）` ← transform=ccrs.PlateCarree() 是 Cartopy 最高频报错点，会出现图片坐标错乱、数据错位；② contourf 要在 ax 对象上绘图（temp.contourf(ax=ax, ...)），不要直接用 plt.contourf；③ NetCDF 文件路径写错会报「文件不存在」，确认数据文件与脚本同级。

第 2 题 限定西北地区区域绘图
----------------------------

题目要求：

1. 设置地图投影 PlateCarree，地理范围：经度 100°~110°E，纬度 30°~40°N（西北地区）；
2. 读取气温数据，绘制 contourf 填色图；
3. 叠加海岸线；
4. 设置标题「西北地区气温空间分布」，并加 colorbar\（标签「气温 ℃」）；
5. 保存为 ex2_nw_temp.png。

.. dropdown:: 参考答案


   .. code-block:: python

      import matplotlib.pyplot as plt
      import cartopy.crs as ccrs
      import xarray as xr

      ds = xr.open_dataset("northwest_temp.nc")
      temp = ds["temp"].mean(dim="time")  # 三维 (time,lat,lon) 先平均成二维

      plt.figure(figsize=(9, 7), dpi=100)
      ax = plt.subplot(projection=ccrs.PlateCarree())

      ax.set_extent([99, 111, 29, 41], crs=ccrs.PlateCarree())

      cs = temp.contourf(ax=ax, transform=ccrs.PlateCarree(),
                         cmap="RdBu_r", levels=18)
      ax.coastlines(linewidth=0.9)

      cbar = plt.colorbar(cs, shrink=0.82)
      cbar.set_label("气温 ℃")
      ax.set_title("西北地区气温空间分布", fontsize=13)

      plt.savefig("ex2_nw_temp.png", dpi=150)
      plt.show()

.. dropdown:: 易错点

   ① set_extent() 的第二个参数 crs= 不能省略，否则区域裁剪失效；② 经纬度顺序是 [lon_min, lon_max, lat_min, lat_max]，写反会得到空白图；③ 色板 RdBu_r（蓝冷红暖）适合气温，不要用不适合气象要素的色板。

第 3 题 叠加地理要素
--------------------

题目要求：

1. 西北地区范围：经度 100°~110°E，纬度 30°~40°N；投影 PlateCarree；
2. 绘制气温填色 contourf；
3. 叠加海岸线、国界线；
4. 添加经纬度网格（gridlines），网格半透明；
5. 设置标题与 colorbar；
6. 保存为 ex3_nw_detail.png。

.. dropdown:: 参考答案


   .. code-block:: python

      import matplotlib.pyplot as plt
      import cartopy.crs as ccrs
      import cartopy.feature as cfeature
      import xarray as xr

      ds = xr.open_dataset("northwest_temp.nc")
      temp = ds["temp"].mean(dim="time")  # 三维 (time,lat,lon) 先平均成二维

      plt.figure(figsize=(9, 7), dpi=100)
      ax = plt.subplot(projection=ccrs.PlateCarree())
      ax.set_extent([99, 111, 29, 41], crs=ccrs.PlateCarree())

      cs = temp.contourf(ax=ax, transform=ccrs.PlateCarree(),
                         cmap="RdBu_r", levels=18)
      ax.coastlines(resolution="50m", lw=0.8)
      ax.add_feature(cfeature.BORDERS, lw=0.7, edgecolor="k")

      gl = ax.gridlines(draw_labels=True, alpha=0.4, linestyle="--")
      gl.top_labels = False
      gl.right_labels = False

      cbar = plt.colorbar(cs, shrink=0.82)
      cbar.set_label("气温 ℃")
      ax.set_title("西北地区气温（带国界与经纬度网格）", fontsize=12)

      plt.savefig("ex3_nw_detail.png", dpi=150)
      plt.show()

.. dropdown:: 易错点

   ① :term:`Natural Earth（自然地球数据集）` 的 cfeature.BORDERS 需要联网下载地理数据，首次运行自动下载，离线环境会报错；② gridlines(draw_labels=True) 才显示经纬度数字，可关闭上、右两侧标签防止图面拥挤；③ 分辨率 resolution="50m" 练习够用，用 10m 下载体积大、加载慢。

进阶题
------

第 4 题 更换兰伯特投影
----------------------

题目要求：

1. 使用 LambertConformal 兰伯特投影（气象常用投影，central_longitude=105、central_latitude=35）；
2. 限定西北地区范围，绘制气温填色与海岸线；
3. 添加 colorbar，标题「兰伯特投影西北地区气温场」；
4. 保存为 ex4_lambert_temp.png。

.. note::

   **重点**：即便画布子图用的是兰伯特投影，数据本身仍是经纬度坐标，所以 contourf 的 transform 依然写 ccrs.PlateCarree()，不能写 LambertConformal。

.. dropdown:: 参考答案


   .. code-block:: python

      import matplotlib.pyplot as plt
      import cartopy.crs as ccrs
      import cartopy.feature as cfeature
      import xarray as xr

      ds = xr.open_dataset("northwest_temp.nc")
      temp = ds["temp"].mean(dim="time")  # 三维 (time,lat,lon) 先平均成二维

      plt.figure(figsize=(9, 7), dpi=100)
      proj_lam = ccrs.LambertConformal(central_longitude=105, central_latitude=35)
      ax = plt.subplot(projection=proj_lam)

      ax.set_extent([99, 111, 29, 41], crs=ccrs.PlateCarree())

      # 注意：数据是经纬度，transform 依旧是 PlateCarree，不是 lambert！
      cs = temp.contourf(ax=ax, transform=ccrs.PlateCarree(),
                         cmap="RdBu_r", levels=18)
      ax.coastlines(lw=0.8)
      ax.add_feature(cfeature.BORDERS, lw=0.7)

      gl = ax.gridlines(draw_labels=True, alpha=0.4, linestyle="--")
      gl.top_labels = False
      gl.right_labels = False

      plt.colorbar(cs, shrink=0.8)
      ax.set_title("兰伯特投影西北地区气温场", fontsize=12)

      plt.savefig("ex4_lambert_temp.png", dpi=150)
      plt.show()

.. dropdown:: 易错点

   ax 是兰伯特投影、而原始 NetCDF 数据是经纬度坐标系，两者的分离正是 :term:`投影（Projection）` 与 :term:`transform（数据坐标系声明）` 的区别。若误把 transform 写成 LambertConformal，整个地理场会错位扭曲。

思考题
------

1. Cartopy 绘图中，ax = plt.subplot(projection=xxx) 与 contourf(transform=yyy) 二者分别代表什么含义？为什么经常两者不一样？
2. set_extent() 中第二个参数 crs= 的作用是什么？如果省略会出现什么现象？
3. 绘制地图填色图时出现数据完全错位，优先排查哪一项参数？

.. dropdown:: 思考题参考答案


   1. projection=xxx 表示画布子图使用的地图投影方式（输出图像的平面投影）；transform=yyy 表示原始数据本身的坐标系。NetCDF 气象数据大多是经纬度（PlateCarree），而画布可以换成 Lambert／Mercator，所以两者经常不同。
   2. crs= 指定 set_extent() 里输入的经纬度数值属于什么坐标系；省略会导致地图裁剪范围错乱，无法框选出目标区域。
   3. 优先排查 transform 参数是否与原始数据坐标系匹配——最常见错误就是漏写、写错 transform。

数据自备：生成一份模拟气温场
----------------------------

若本地暂无 northwest_temp.nc，可以先用 NumPy 生成一份带经纬度坐标的模拟气温场（高斯形状的暖区，像「高压脊」一样），用于练习画图逻辑：

.. code-block:: python

   import numpy as np
   import xarray as xr

   lons = np.linspace(100, 110, 21)
   lats = np.linspace(30, 40, 11)
   lon2d, lat2d = np.meshgrid(lons, lats)

   # 以 (105°E, 35°N) 为中心的暖脊状气温场，跨越 100~110°E、30~40°N
   temp2d = 12 - 0.06 * (lon2d - 105) ** 2 - 0.12 * (lat2d - 35) ** 2

   ds = xr.Dataset(
       {"temp": (["lat", "lon"], temp2d)},
       coords={"lat": lats, "lon": lons},
   )
   ds["temp"].attrs["units"] = "°C"
   temp = ds["temp"]
   ds.to_netcdf("northwest_temp.nc")

   # 之后即可照常读取
   # ds = xr.open_dataset("northwest_temp.nc")
   # temp = ds["temp"]

.. dropdown:: 小结

   第 10 章练习的四个关键词：**① transform 千万不要漏/写错**；**② set_extent 范围与 crs 搭配**；**③ 海岸线 / 国界 / 网格的地理要素叠加**；**④ 画布投影（Lambert）与数据坐标系（PlateCarree）分离**。把这四条吃透，Cartopy 地图绘图就能画得又快又对。