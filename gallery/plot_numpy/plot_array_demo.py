"""
二维数组可视化
==============

用 NumPy 生成一个二维场，Matplotlib 的 ``imshow`` 展示其结构。
"""

import matplotlib.pyplot as plt
import numpy as np

data = np.linspace(-3, 3, 300).reshape(30, 10)
field = np.sin(data) * np.cos(data)   # 同形相乘，避免广播错误

fig, ax = plt.subplots(figsize=(5, 3))
im = ax.imshow(field, cmap="RdBu_r", origin="lower")
ax.set_xlabel("列")
ax.set_ylabel("行")
ax.set_title("二维场 imshow")
plt.colorbar(im, ax=ax, label="值")
plt.tight_layout()
plt.show()
