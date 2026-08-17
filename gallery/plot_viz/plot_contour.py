"""
等值线填色图
============

绘制一个二维函数的等值线填色（contourf），是气象场可视化的常见形式。
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 200)
y = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y) * np.exp(-(X ** 2 + Y ** 2) / 8)

fig, ax = plt.subplots(figsize=(5, 4))
cf = ax.contourf(X, Y, Z, levels=20, cmap="viridis")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("等值线填色 contourf")
plt.colorbar(cf, ax=ax, label="Z")
plt.tight_layout()
plt.show()
