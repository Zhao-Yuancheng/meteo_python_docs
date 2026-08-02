气象数据绘图
============

第 9–10 节。Matplotlib 画通用图表，Cartopy 在地图投影上叠加气象场。

.. _tut-mpl:

Matplotlib 绘图（一）
---------------------

面向对象接口（``fig, ax``）是推荐写法，便于拼多子图：

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt

   x = np.linspace(0, 2 * np.pi, 200)
   fig, ax = plt.subplots(figsize=(7, 3))
   ax.plot(x, np.sin(x), label="sin")
   ax.plot(x, np.cos(x), label="cos")
   ax.set_xlabel("x")
   ax.set_ylabel("值")
   ax.legend()
   ax.set_title("正弦与余弦")
   plt.show()

.. _tut-cartopy:

Cartopy 绘图（二）
------------------

Cartopy 提供地图投影与地理特征，配合 Matplotlib 绘制气象场。下面用 PlateCarree 投影画一个全球温度场：

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt
   import cartopy.crs as ccrs
   import cartopy.feature as cfeature

   lon = np.linspace(-180, 180, 144)
   lat = np.linspace(-90, 90, 73)
   LON, LAT = np.meshgrid(lon, lat)
   temp = 15 - 0.5 * (LAT ** 2) + 5 * np.sin(np.deg2rad(LON))

   fig = plt.figure(figsize=(8, 4))
   ax = plt.axes(projection=ccrs.PlateCarree())
   cf = ax.contourf(lon, lat, temp, 20, transform=ccrs.PlateCarree(), cmap="RdBu_r")
   ax.coastlines()
   ax.add_feature(cfeature.LAND, facecolor="lightgray")
   plt.colorbar(cf, orientation="horizontal", label="°C")
   ax.set_global()
   plt.title("模拟全球气温场")
   plt.show()

.. note::
   Cartopy 首次使用海岸线时会下载 Natural Earth 数据。在线运行器里若无法联网，
   可先在本地运行 ``cartopy.io.shapereader.natural_earth`` 触发下载并缓存。
