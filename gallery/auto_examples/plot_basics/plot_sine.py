"""
绘制正弦波
==========

最简单的 Matplotlib 示例：生成一组角度，画出对应的正弦曲线。
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(x, y, color="#1f77b4")
ax.set_xlabel("角度 (rad)")
ax.set_ylabel("sin(x)")
ax.set_title("正弦波")
plt.tight_layout()
plt.show()
