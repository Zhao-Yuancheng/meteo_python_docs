"""
我的第一个气象图
================

第 1 章示例（T-106）：环境搭建好后，用最短的代码画出一张"模拟兰州气温随日期变化"
的折线图——用来验证 NumPy 与 Matplotlib 是否安装成功。绘图细节属于第 9 章内容，
这里先感受一下"环境跑通"的成就感。

.. note::

   本脚本需要 NumPy 与 Matplotlib，请先在 ``met_p312`` 环境安装：
   ``conda install numpy matplotlib``
"""

# %%
# 兰州站连续 7 天日最高气温（°C）
import numpy as np

days = np.arange(1, 8)                     # 第 1~7 天
temp = np.array([28.1, 29.4, 31.2, 33.6, 34.9, 35.7, 33.2])
print("日期：", days)
print("气温：", temp)

# %%
# 面向对象绘图：fig 是画布，ax 是坐标系
import matplotlib.pyplot as plt

# 中文字体设置（独立运行时保证中文正常显示）
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei",
                                   "Noto Sans CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(6.4, 4))
ax.plot(days, temp, marker="o", color="#d62728", label="日最高气温")
ax.set_xlabel("日期（天）")
ax.set_ylabel("气温 (°C)")
ax.set_title("兰州站近 7 日最高气温")
ax.set_xticks(days)
ax.legend()
plt.tight_layout()
plt.show()

print("环境验证成功！能画出这张折线图，说明 NumPy + Matplotlib 已生效。")