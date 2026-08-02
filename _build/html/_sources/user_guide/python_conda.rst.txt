.. _tut-conda:

Python 与 Conda 简介
====================

第 1 节。介绍 Python 在气象领域的定位，以及如何用 Conda 管理互不干扰的环境。

为什么要用 Conda
----------------

气象计算依赖 NumPy、Cartopy 等含 C 扩展的库，Conda 把它们连同二进制依赖一起装好，避免编译踩坑。

.. code-block:: bash

   # 创建专用环境
   conda create -n P312 python=3.12
   conda activate P312
   conda install numpy pandas xarray matplotlib cartopy

第一个气象图
------------

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt

   lon = np.linspace(70, 140, 200)
   temp = 15 + 10 * np.sin(np.deg2rad(lon))   # 模拟气温随经度变化

   fig, ax = plt.subplots(figsize=(7, 3))
   ax.plot(lon, temp, color="#d62728")
   ax.set_xlabel("经度 (°E)")
   ax.set_ylabel("气温 (°C)")
   ax.set_title("沿纬圈的模拟气温")
   plt.show()

点上面代码块的 **▶ 运行** 即可在网页端查看这张图。
