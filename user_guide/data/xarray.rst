.. _tut-xarray:

气象数据分析（二）Xarray
========================

第 8 节 · 模块二 气象数据处理
贯穿项目第 8 步：用 Xarray 读取 NetCDF 再分析气温场，做区域平均与时间切片。

.. note::

   本节正文由 T-801 交付后填充，以下为内容概要与导读。

Xarray 给多维数组加上经纬度、时间等坐标标注，是读 NetCDF 的主力：

.. code-block:: python

   import numpy as np
   import xarray as xr

   lon = np.linspace(70, 140, 8)
   lat = np.linspace(20, 50, 5)
   temp = 15 + 10 * np.sin(np.deg2rad(lon))[None, :] * np.cos(np.deg2rad(lat))[:, None]

   da = xr.DataArray(temp, coords=[("lat", lat), ("lon", lon)], name="t2m")
   da.attrs["units"] = "°C"
   print(da.sel(lat=36, method="nearest"))

本章将覆盖的知识点：DataArray / Dataset、坐标与维度、``sel`` / ``isel``、``open_dataset``、简单绘图；提升拓展：``groupby`` 时间分组、``resample`` 重采样、加权平均。
