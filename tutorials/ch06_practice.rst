第 6 章练习：气象数据计算 NumPy
===============================

配套 :ref:`tut-numpy` 正文使用。第 1–3 题为入门题，第 4–5 题为提升题。试题延续贯穿项目——把兰州站的气温数据存进 NumPy 数组，做分组统计、高温预警筛选与标准化。

.. seealso:: 配套正文：:doc:`/user_guide/data/numpy`　·　术语参考：:doc:`/api/ch06_terms`　·　示例画廊 :doc:`/gallery/plot_numpy/index`

💡 **通用提示**：数组下标从 0 开始；练习用 ``np.random.seed(42)`` 固定随机种子，保证每个人跑出来的随机数一致、方便对答案。

入门题
------

第 1 题（实操）创建气温矩阵
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

某气象站记录了 2026 年 1 月（31 天）每天 4 个时次（02、08、14、20 时）的气温数据。请：用 ``np.random.randint(-10, 35, size=(31, 4))`` 生成气温数组，将其转换为 ``np.float32`` 类型，并打印数组的 ``shape`` 与 ``dtype``。

.. admonition:: 提示

   - ``np.random.randint`` 默认生成**整数**，若想得到浮点数组，用 ``.astype(np.float32)`` 转换；
   - 生成随机数前加 ``np.random.seed(42)``，结果可复现、方便调试。

**参考答案**：

.. code-block:: python

   import numpy as np

   np.random.seed(42)                     # 固定随机种子，结果可复现
   temps = np.random.randint(-10, 35, size=(31, 4)).astype(np.float32)
   print("shape:", temps.shape)           # (31, 4)：31 天 × 4 时次
   print("dtype:", temps.dtype)           # float32

第 2 题（实操）axis 参数：逐时均温与逐日极值
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

沿用第 1 题的数组 ``temps``（形状 ``(31, 4)``，行 = 日期，列 = 时次）：

1. 计算每一天的**日平均气温**（沿时次方向求平均），结果形状应为 ``(31,)``；
2. 计算每一个时次在 31 天中的**最高温**（沿日期方向取最大），结果形状应为 ``(4,)``。

要求使用 ``np.mean`` / ``np.max`` 并正确指定 ``axis``。

.. admonition:: 提示

   **axis 方向口诀**：``axis=0`` 沿垂直方向（跨日期，压掉行），``axis=1`` 沿水平方向（跨时次，压掉列）。
   记不清时可以拿一个小数组（如 ``(2, 3)``）分别试 ``np.sum(..., axis=0)`` 与 ``axis=1``，比较输出形状。

**参考答案**：

.. code-block:: python

   # axis=1：消掉时次列 → 得到每天的日平均气温
   daily_mean = temps.mean(axis=1)
   print("逐日均温 shape:", daily_mean.shape)     # (31,)

   # axis=0：消掉日期行 → 得到每个时次的 31 天最高温
   hourly_max = temps.max(axis=0)
   print("逐时极值 shape:", hourly_max.shape)     # (4,)

第 3 题（实操）广播运算：开尔文转摄氏度并加上站间修正
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

现有一组格点温度 ``temps_kelvin``（形状 ``(5, 3)``，单位开尔文 K，数值约 280~310）与每个站点的修正偏移量 ``offset = [0.5, -0.3, 0.8]``（形状 ``(3,)``）。请利用**广播机制**将其转换为摄氏度，转换公式：℃ = K − 273.15，并同时叠加各站修正偏移，即 ``temps_kelvin - 273.15 + offset``。检查结果的形状。

.. admonition:: 提示

   - 广播规则：从后往前对齐维度，某维相等或为 **1** 即可扩展。``offset`` 形状 ``(3,)`` 会自动沿行方向扩展到 ``(5, 3)``；
   - ``-273.15`` 是标量，同样会广播；
   - 不确定是否成功时先 ``print(result.shape)`` 验证，应为 ``(5, 3)``。

**参考答案**：

.. code-block:: python

   temps_kelvin = np.random.rand(5, 3) * 30 + 280      # (5, 3)，模拟 5 站 3 时刻
   offset = np.array([0.5, -0.3, 0.8])                 # 每站修正偏移

   result = temps_kelvin - 273.15 + offset             # 广播：(5,3) 与 (3,) 运算
   print("结果 shape:", result.shape)                  # (5, 3)

提升题
------

第 4 题（实操）布尔筛选：高温预警
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``temps`` 数组形状为 ``(31, 4)``，代表 31 天 4 个时次的温度（℃）。请完成：

1. 找出所有**温度大于 35℃** 的元素，输出数量与具体数值；
2. 将**温度低于 0℃** 的元素替换为 ``np.nan`` （表示缺测）；
3. 统计每个时次（列）出现高温（> 35℃）的天数。

.. admonition:: 提示

   - 布尔索引返回一维数组，统计数量用 ``np.sum(mask)`` 或 ``np.count_nonzero(mask)``；
   - 若要 ``temps[temps < 0] = np.nan`` 生效，``temps`` 必须是**浮点型**（整数数组无法存 NaN，会报错）——第 1 题已转成 ``float32``，正好可用；
   - 统计每列高温天数：``np.sum(temps > 35, axis=0)``，因为 True 计作 1、False 计作 0。

**参考答案**：

.. code-block:: python

   mask_hot = temps > 35
   print("高温元素个数：", np.count_nonzero(mask_hot))
   print("高温具体数值：", temps[mask_hot])

   temps[temps < 0] = np.nan                     # 0℃ 以下的观测转为缺测
   hot_count_per_hour = np.sum(temps > 35, axis=0)   # 每个时次的高温天数
   print("各时次高温天数：", hot_count_per_hour)     # shape (4,)

第 5 题（实操）标准化（Z-score）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

给定数组 ``data``（形状 ``(10, 5)``，代表 10 个站点测得的 5 项气象指标）。请对**每一列（每项指标）**做标准化，使每个指标均值为 0、标准差为 1。标准化公式：``z = (x - mean) / std``。要求用向量化操作，禁止 for 循环。

.. admonition:: 提示

   - ``np.mean(data, axis=0)`` 得每列均值、``np.std(data, axis=0)`` 得每列标准差，二者形状均为 ``(5,)``；
   - 利用广播，``data - mean`` 与 ``/ std`` 都会自动按列扩展；
   - 若某列标准差为 0（所有值相同），会除以 0——可先判断，或用 ``np.seterr(divide="ignore")`` 临时忽略警告；
   - 验证：标准化后 ``np.mean(z, axis=0)`` ≈ 0、``np.std(z, axis=0)`` ≈ 1。

**参考答案**：

.. code-block:: python

   np.random.seed(0)
   data = np.random.rand(10, 5) * 40 - 5        # 10 站 × 5 指标

   mean = np.mean(data, axis=0)
   std  = np.std(data, axis=0)
   z = (data - mean) / std                      # 广播，按列标准化

   print("标准化后每列均值：", np.round(np.mean(z, axis=0), 6))   # 全为 0
   print("标准化后每列标准差：", np.round(np.std(z, axis=0), 6))   # 全为 1

练习 tips 汇总
--------------

📌 **axis 方向终极记忆表**

.. list-table:: axis 对照
   :header-rows: 1

   * - 操作
     - ``axis=0``
     - ``axis=1``
   * - 含义
     - 沿**行**方向（垂直），压掉行维度
     - 沿**列**方向（水平），压掉列维度
   * - 口诀
     - 0 是向下压，行消失
     - 1 是向右挤，列消失
   * - 例（``arr.shape = (3, 4)``）
     - ``np.sum(arr, axis=0)`` → 结果 ``(4,)``
     - ``np.sum(arr, axis=1)`` → 结果 ``(3,)``

📌 **补充提醒**

- 布尔索引结果是一维数组，统计数量用 ``np.count_nonzero``，别用 ``len`` 误当元素数量；
- 整数数组存不下 ``NaN``——气象缺测必须用浮点数组承载；
- ``NaN`` 会「传染」：一旦出现，均值、极值、标准化都会受影响，需要用 ``np.nanmean`` 等跳过缺测的函数。