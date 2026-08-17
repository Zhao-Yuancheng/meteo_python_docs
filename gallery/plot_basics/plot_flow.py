"""
气温等级判定与逐日可视化
========================

第 3 章示例（T-306）：用 ``if/elif/else`` 对兰州站近 7 日最高气温做等级判定，
用 ``for`` 循环 + 字典统计各等级天数，最后用 Matplotlib 画一张"逐日气温 +
等级配色"的柱状图——把分支与循环的实战成果"画"出来。

绘图部分属于第 9 章 Matplotlib 的内容，此处先睹为快，不必深究。
"""

# %%
# 兰州站近 7 日最高气温（°C）
days = [1, 2, 3, 4, 5, 6, 7]
temp_max = [19.5, 23.8, 28.4, 31.6, 33.9, 34.2, 29.5]

# %%
# 气温等级判定：用一个 if/elif/else 阶梯，把每个温度"翻译"成等级
def temp_level(t):
    if t >= 30:
        return "炎热"
    elif t >= 20:
        return "适宜"
    elif t >= 10:
        return "偏冷"
    else:
        return "寒冷"


# %%
# 统计各等级天数：for 循环 + 字典计数
counts = {"炎热": 0, "适宜": 0, "偏冷": 0, "寒冷": 0}
levels = []
for t in temp_max:
    lev = temp_level(t)
    levels.append(lev)
    counts[lev] += 1

print("逐日等级：", list(zip(days, temp_max, levels)))
print("各等级天数：", counts)

# %%
# 绘图：柱状图按等级配色，颜色与等级一一对应
import matplotlib.pyplot as plt

# 中文字体设置（文档画廊构建时已配置，独立运行时也稳妥）
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei",
                                   "Noto Sans CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

level_color = {
    "炎热": "#d62728",
    "适宜": "#ff7f0e",
    "偏冷": "#1f77b4",
    "寒冷": "#2ca02c",
}
colors = [level_color[lev] for lev in levels]

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(days, temp_max, color=colors, edgecolor="white", width=0.6)
ax.set_xticks(days)
ax.set_xlabel("日期（天）")
ax.set_ylabel("日最高气温 (°C)")
ax.set_title("兰州站近 7 日最高气温与等级")
ax.set_ylim(0, 40)

# 在柱顶标注气温值和等级
for d, t, lev in zip(days, temp_max, levels):
    ax.text(d, t + 1, f"{t:.1f}\n{lev}", ha="center", va="bottom", fontsize=9)

# 图例：按等级生成
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c, label=lev) for lev, c in level_color.items()],
          loc="upper left")

plt.tight_layout()
plt.show()

print("等级统计可视化完成！")