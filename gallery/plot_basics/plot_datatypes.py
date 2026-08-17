"""
用基本数据类型存储站点信息
==========================

第 2 章示例（T-206）：不借助任何数据处理库，仅用 ``str`` / ``int`` / ``float`` /
``tuple`` / ``list`` / ``dict`` 这些内置类型，存储兰州站的元信息与近 7 日气温，
完成统计并绘制一张气温柱状图——每个类型的选择理由都写在行尾注释里。

绘图部分属于第 9 章 Matplotlib 的内容，此处先睹为快，不必深究。
"""

# %%
# 站点元信息：str 存名称、int 存站号、多重赋值存经纬度
station_name = "兰州"              # str   站名：文本，不参与算术
station_id = 52889                 # int   区站号：无前导零，纯数字
lon, lat = 103.83, 36.06           # float 经纬度：连续量，必须保留小数
elevation = 1517.2                 # float 海拔 (m)

# %%
# 近 7 日日最高气温（°C）：有序、可追加，适合用 list
dates = ["7-08", "7-09", "7-10", "7-11", "7-12", "7-13", "7-14"]
temp_max = [28.1, 29.4, 31.2, 33.6, 34.9, 35.7, 33.2]

# 统计五件套：sum / len / max / min + 列表推导式筛选高温日
t_mean = sum(temp_max) / len(temp_max)
t_high, t_low = max(temp_max), min(temp_max)
high_days = [t for t in temp_max if t >= 35]   # 高温日判据：≥ 35 °C

# %%
# 组装站点档案（dict）：按键取值，一处集中管理
station = {
    "id": station_id,
    "name": station_name,
    "lon": lon,
    "lat": lat,
    "elev": elevation,
    "temp_max": temp_max,
}

print(f"站点：{station['name']}（{station['id']}）")
print(f"位置：{lon:.2f}°E, {lat:.2f}°N, 海拔 {elevation:.1f} m")
print(f"近 7 日最高 {t_high} °C / 最低 {t_low} °C / 平均 {t_mean:.1f} °C")
print(f"高温日（≥35 °C）：{len(high_days)} 天")

# %%
# 绘图：柱状图展示逐日气温，均值做参考线，高温日标红
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6.4, 4))
colors = ["#d62728" if t >= 35 else "#1f77b4" for t in temp_max]
ax.bar(dates, temp_max, color=colors, edgecolor="white")
ax.axhline(t_mean, color="#2ca02c", ls="--", lw=1.5,
           label=f"7 日均值 {t_mean:.1f} °C")
ax.set_xlabel("日期（2024 年 7 月）")
ax.set_ylabel("日最高气温 (°C)")
ax.set_title(f"{station_name}站近 7 日最高气温")
ax.set_ylim(20, 40)
ax.legend()
plt.tight_layout()
plt.show()
