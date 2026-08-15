.. _tut-mpl:

气象数据绘图（一）Matplotlib
============================

第 9 节 · 模块三 气象数据可视化
贯穿项目第 9 步：绘制兰州气温时间序列图、散点图、直方图。

.. note::

   本节正文由 T-901 交付后填充，以下为内容概要与导读。

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

本章将覆盖的知识点：Figure / Axes 面向对象接口、``plot`` / ``scatter`` / ``bar`` / ``hist``、标签 / 标题 / 图例、子图、``savefig``；提升拓展：``twinx`` 双轴、``annotate`` 标注、自定义样式。

.. seealso:: 示例画廊 :doc:`/gallery/auto_examples/plot_viz/index`。
