# -*- coding: utf-8 -*-
r"""
绘制 EKMA 曲线：城市臭氧敏感性分析
==================================

经验动力学建模方法（Empirical Kinetic Modeling Approach, EKMA）曲线，
是研究 O₃ 与前体物关系的经典工具：固定 VOCs 组分谱，系统扫描 NOx 与 VOCs 的
总浓度组合，把每个组合对应的最大 O₃ 浓度填到网格上，再用等值线画出
"O₃ 浓度关于（NOx, VOCs）的平面"。它揭示了 O₃ 生成对两种前体物的
非线性响应，并据此把一个城市的污染状态划分为三个特征区域：

#. VOCs 控制区（图中偏右侧）：NOx 充足、VOCs 不足，增 O₃ 主要靠增 VOCs，
   削减 VOCs 排放最见效；
#. NOx 控制区（图中左上方）：VOCs 充足、NOx 不足，削减 NOx 排放最见效；
#. 过渡区 / 脊线（二者之间的弧形高曲率带）：O₃ 对两种前体物都高度敏感，
   单边减排可能造成"反弹效应"。

背景：写给没学过大气化学的读者
------------------------------

近地面臭氧（O₃）不是工厂直接排放的，而是由两类"前体物"在太阳光
（尤其是紫外光）下经一连串光化学反应生成的：

* VOCs：挥发性有机物（如汽油挥发、溶剂、工业喷涂排放的烯烃、芳香烃等）；
* NOx：氮氧化物，即 NO 与 NO₂（机动车、电厂、工业炉窑燃烧产生）。

好消息是：光化学烟雾的强大氧化性在这里只是背景知识，本示例无需任何大气化学
功底也能照跑。你只需把它理解成一个"输入—输出"黑箱：输入两个自变量
（NOx 浓度、VOCs 浓度），输出一个因变量（O₃ 浓度）。我们要做的，就是
重复 121 次实验，得到一张 "O₃ 浓度等高线图"，并据此讨论污染治理该往哪个方向使劲。


数据文件 ``clean_data.xlsx`` 是老师提供的一套现成的、有效的 EKMA 模拟结果，
含 121 行（11×11 网格）、三列：NOx ppb、VOCs ppb、O3 ppb（单位均为
ppb，即十亿分之一体积比）。点击按钮下载后放在脚本同级目录：

.. container:: sphx-glr-download meteopy-download-nc

   :download:`下载完整代码包（.py + .ipynb + 数据） plot_ekma_curve.zip </download/plot_ekma_curve.zip>`

也可单独下载数据文件：

.. container:: sphx-glr-download meteopy-download-nc

   :download:`下载 EKMA 模拟数据 clean_data.xlsx </data/clean_data.xlsx>`
"""
# %%
# 
# ① 导入库 + 中文字体配置
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 中文字体：Windows 常见微软雅黑 / 黑体；Linux 常见文泉驿；macOS 常见苹方。
# axes.unicode_minus=False 解决坐标轴负号显示为方块的问题。
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "WenQuanYi Micro Hei"]
plt.rcParams["axes.unicode_minus"] = False

# %%
# 
# ② 读取长表数据（优先项目配套 xlsx，缺失时退回合成网格）
# 
# 路径候选依次覆盖三种运行场景：读者解压 zip 后数据在脚本同级（./clean_data.xlsx）、
# 文档/项目目录下的 data 子目录（./data/）、sphinx-gallery 构建目录（../../data/）。
XLSX_CANDIDATES = ["./clean_data.xlsx",
                   "./data/clean_data.xlsx",
                   "../data/clean_data.xlsx",
                   "../../data/clean_data.xlsx",
                   "../../../data/clean_data.xlsx"]
xlsx_path = next((p for p in XLSX_CANDIDATES if os.path.exists(p)), None)

if xlsx_path:
    df = pd.read_excel(xlsx_path)          # 按输入顺序读入，即"长表 / 长格式"
    source = f"配套数据 {xlsx_path}"
else:
    # 兜底：数据缺失时合成一张"类 EKMA"的钟形曲面，保证脚本任何环境都能演示流程。
    _nox = np.arange(0, 241, 24)            # 11 个 NOx 浓度
    _voc = np.arange(0, 101, 10)            # 11 个 VOCs 浓度
    _gx, _gy = np.meshgrid(_nox, _voc)
    _peak = 180 * np.exp(-0.5 * ((_gx - 180) / 140) ** 2
                         - 0.5 * ((_gy - 70) / 35) ** 2)
    _noise = np.random.default_rng(0).normal(0, 3, size=_gx.shape)
    df = pd.DataFrame({
        "NOx ppb": np.tile(_nox, len(_voc)),
        "VOCs ppb": np.repeat(_voc, len(_nox)),
        "O3 ppb": (_peak + _noise).ravel(),
    })
    source = "合成网格（未找到数据文件）"

print("数据来源：", source)
print("表规模 (行, 列):", df.shape)
print(df.head(6).to_string(index=False))

# %%
# 
# ③ 关键一步：把"长表"重塑为"二维网格"（宽表 / 短表）
# 
# 上面读入的是一列到底的 121 行数据，而我们要画"关于两个自变量的等值面"，
# 需要 (NOx, VOCs) 的一张 11×11 平面。pandas.pivot 能按两列索引、
# 一列取值，自动把它转成二维矩阵：index→行（VOCs），columns→列（NOx），values→O₃。
# 这一行是本示例的"含金量"所在：长表 → 宽表的转换是科研绘图的通用技能。
piv = (df.pivot(index="VOCs ppb", columns="NOx ppb", values="O3 ppb")
         .sort_index())                     # 行/列都按浓度升序，网格与坐标严格对齐

nox = piv.columns.values                    # 横轴刻度：0, 24, ..., 240（ppb）
voc = piv.index.values                      # 纵轴刻度：0, 10, ..., 100（ppb）
o3  = piv.values                            # (VOCs 行, NOx 列) 的 O₃ 浓度二维数组

print("网格形状 (VOCs 行数, NOx 列数):", o3.shape)
print("O₃ 浓度范围 (ppb):", f"{o3.min():.1f} ~ {o3.max():.1f}")

# %%
# 
# ④ 绘图主体：填充等值面 + 等值线 + 色标
# 
# contourf 画"填充等值面"，直观展示 O₃ 浓度场的低→高；contour 在其上叠"等值线"
# 便于读具体数值，clabel 把数值标到线上。三层叠加是等值面图的经典配比。
# 标签里的 O$_3$ 用 mathtext 下标：中文字体缺下标 ₃ 的字形，直接写 O₃ 会显示成方块。
# 本图分两块构建（图形主体→分区标注），第一块末尾的 defer 标记让截图推迟到下一块，
# 保证保存的是带分区标注的完整图。
fig, ax = plt.subplots(figsize=(7.5, 6), layout="constrained")

cf = ax.contourf(nox, voc, o3, levels=20, cmap="viridis",
                 extend="both")                 # extend="both"：超出色阶范围用两端色
ct = ax.contour(nox, voc, o3, levels=6, colors="k", linewidths=0.8)
ax.clabel(ct, inline=True, fontsize=8, fmt="%.0f")   # 在等值线上标注 O₃ 数值

# 横、纵轴与色标三要素必须齐全：这是"坐标轴标签 + colorbar"的规范写法
ax.set_xlabel("NOx 浓度（ppb）")
ax.set_ylabel("VOCs 浓度（ppb）")
ax.set_title("EKMA 曲线：O$_3$ 浓度对 NOx 与 VOCs 的响应", fontsize=12)

cbar = fig.colorbar(cf, ax=ax, aspect=30, pad=0.02)
cbar.set_label("最大 O$_3$ 浓度（ppb）")
# sphinx_gallery_defer_figures

# %%
# 
# ⑤ 补充：标注三个臭氧敏感性分区（科学解读层）
# 
# 依据 ③ 的物理分区，在图上加文字框，把"看图"升级为"读懂机理"。
region = [
    (200, 20,  "VOCs 控制区\n（削减 VOCs 见效）"),
    (40,  92,  "NOx 控制区\n（削减 NOx 见效）"),
    (125, 55,  "过渡区 / 脊线\n（协同减排，防反弹）"),
]
for rx, ry, text in region:
    ax.text(rx, ry, text, ha="center", va="center",
            fontsize=9, color="white", weight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc="#2b3a55", ec="none", alpha=0.85))

print("绘制完成：填充等值面 + 等值线标注 + 三个敏感性分区文字框。")
plt.show()

# %%
# 
# ⑥ 延伸思考（供读者 / 报告讨论）
# 
# 1. 观察等值线走向：右侧近垂直（O₃ 对 VOCs 敏感）→ 左上方近水平（对 NOx 敏感）；
# 2. 若一个城市落在脊线上，只减 NOx 可能让 O₃ 短期不降反升——这就是"反弹效应"；
# 3. 治理需"精准诊断 + 协同减排"，并把基于物种的 VOCs 活性纳入长期战略。