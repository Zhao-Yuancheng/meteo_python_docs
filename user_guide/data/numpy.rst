.. _tut-numpy:

气象数据计算 NumPy
==================

第 6 节 · 模块二 气象数据处理
贯穿项目第 6 步：用 NumPy 数组存储多站气温矩阵，做向量化计算与标准化。

.. note::

   本节正文由 T-601 交付后填充，以下为内容概要与导读。

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

本章将覆盖的知识点：ndarray 创建 / 索引 / 切片、向量化运算、广播机制、常用统计函数；提升拓展：布尔索引、花式索引、数组拼接、结构化数组。

.. seealso:: 示例画廊 :doc:`/gallery/auto_examples/plot_numpy/index`。
