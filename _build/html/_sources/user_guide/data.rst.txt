气象数据计算与分析
==================

第 6–8 节。NumPy 做数值计算，Pandas 处理表格型观测，Xarray 处理带标注的多维网格。

.. _tut-numpy:

NumPy 计算
----------

NumPy 的 ``ndarray`` 是气象多维数据的底层数据结构，支持向量化运算：

.. code-block:: python

   import numpy as np

   # 模拟 5 天 × 3 站的气温(°C)
   temps = np.array([[5.1, 6.3, 4.8],
                     [7.0, 8.1, 6.5],
                     [9.2, 10.0, 8.7],
                     [11.5, 12.0, 10.9],
                     [8.4, 9.1, 7.6]])

   print("逐站平均:", temps.mean(axis=0))
   print("逐日最高:", temps.max(axis=1))
   print("标准化:", (temps - temps.mean()) / temps.std())

Pandas 分析（一）
-----------------

Pandas 适合站点观测等表格数据：

.. code-block:: python

   import pandas as pd

   df = pd.DataFrame({
       "站名": ["兰州", "西安", "成都"],
       "气压": [850, 970, 950],
       "气温": [5.1, 8.2, 12.0],
   })
   df["位势高度"] = df["气压"] * 8.0   # 粗略估算
   print(df.sort_values("气温", ascending=False))

.. _tut-xarray:

Xarray 分析（二）
-----------------

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
