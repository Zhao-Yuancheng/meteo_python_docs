.. _tut-cartopy:

气象数据绘图（二）Cartopy
=========================

第 10 节 · 模块三 气象数据可视化
贯穿项目第 10 步：绘制西北地区气温空间分布图（等值线填色 + 海岸线）。

.. note::

   本节正文由 T-1001 交付后填充，以下为内容概要与导读。

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

本章将覆盖的知识点：地图投影、PlateCarree / Mercator、``coastlines`` 与地理要素、``contourf`` + ``transform``、``colorbar``；提升拓展：自定义投影、省界叠加、风场矢量图 ``quiver``。

.. note::

   Cartopy 首次使用海岸线时会下载 Natural Earth 数据，需联网或提前缓存。
