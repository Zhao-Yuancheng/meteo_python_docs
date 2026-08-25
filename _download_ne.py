# -*- coding: utf-8 -*-
"""触发 cartopy 下载画廊 cartopy 例子所需的 4 个 Natural Earth 110m 数据集并永久缓存。"""
from cartopy.io import shapereader

NEED = [
    ("110m", "physical", "coastline"),
    ("110m", "cultural", "admin_0_boundary_lines_land"),
    ("110m", "physical", "rivers_lake_centerlines"),
    ("110m", "physical", "ocean"),
]

for res, cat, name in NEED:
    path = shapereader.natural_earth(resolution=res, category=cat, name=name)
    print(f"[OK] {name:35s} -> {path}")

print("全部下载完成")