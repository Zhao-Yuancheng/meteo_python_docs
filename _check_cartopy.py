# -*- coding: utf-8 -*-
"""完整执行 cartopy 脚本（plt.show() 换成 savefig），验证代码产出完整地图。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

src = open(r"D:\Code\Vibe\meteo_python_docs\examples\plot_viz\plot_cartopy_temp.py",
           encoding="utf-8").read()
src = src.replace(
    "plt.show()",
    r'plt.savefig(r"D:\Code\Vibe\meteo_python_docs\_check_imgs\cartopy_full.png", dpi=110)')
exec(compile(src, "plot_cartopy_temp.py", "exec"))
print("saved")