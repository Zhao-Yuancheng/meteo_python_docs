气象数据分析（一）Pandas Q&A
==================================

   **章节定位**\ ：第 7 章（模块二）· 对应用户指南
   ``user_guide/data/pandas.rst`` 与配套 PPT 第 07 讲。 通用排错方法论见
   :doc:`00-通用排错指南 </qa/basics/00-通用排错指南>`\ （0.1 节「报错 / 警告 /
   静默错值」三分法、0.4 节「排查七招」、0.5
   节「静默污染」先读）。本章反复用这三分类，尤其\ **第 3
   类静默错值**\ 是 Pandas 的主战场。 **校正说明**\ ：本文所有
   ``Traceback / Warning / 异常现象``
   均在本机真实运行验证、原文照录。pandas 2.x 与 3.x
   之间存在行为差异，已在相关条目中逐条标注，供不同版本读者对照。

--------------

.. _70-本章报错总览表:

7.0 本章报错总览表
------------------

第 7 章「Pandas 气象数据分析」的高频问题，先按「报错(中断) /
警告(不中断) / 静默错值」三分类摊开。\ **看懂这张表 =
一条报错秒定位**\ 。

+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| 英文关键词（报错里看到的）                                                                | 类型      | 报错 / 现象一句话                  | 解决办法一句话                        |
+===========================================================================================+===========+====================================+=======================================+
| ``KeyError: '列名/标签'``                                                                 | 报错      | loc / df[..]                       | 先 ``print(df.columns)`` 复制真实列名 |
|                                                                                           |           | 里键名不存在，或列名大小写/拼写错  |                                       |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``TypeError: Cannot index by location index with a non-integer key``                      | 报错      | 用 ``iloc``                        | 位置索引 ``iloc`` 只能整数；标签改    |
|                                                                                           |           | 传了字符串（列名/标签）            | ``loc``                               |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``IndexError: single positional indexer is out-of-bounds``                                | 报错      | ``iloc`` 整数下标越界              | 先 ``len(df)``/``df.shape`` 看范围    |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``KeyError: '气温' not found in axis``                                                    | 报错      | ``drop`` 默认 axis=0               | 删列要 ``df.drop(列名, axis=1)`` 或   |
|                                                                                           |           | 删行，把列名当行删                 | ``df.drop(columns=...)``              |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``ValueError: could not convert string to float: 'MISS'``                                 | 报错      | ``astype(float)`` 遇到非数字字符串 | 清洗 /                                |
|                                                                                           |           |                                    | ``to_numeric(errors='coerce')`` 转    |
|                                                                                           |           |                                    | NaN                                   |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``ValueError: Unable to parse string "MISS"``                                             | 报错      | ``to_numeric(errors='raise')``     | 用 ``errors='coerce'`` 或先           |
|                                                                                           |           | 撞上坏值                           | ``replace`` 缺测                      |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``ValueError: The truth value of a Series is ambiguous``                                  | 报错      | 条件组合用了 ``and`` /             | \`）                                  |
|                                                                                           |           | ``or``\ （应 ``&``/\`              |                                       |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``AttributeError: 'Series' object has no attribute 'strftime'``                           | 报错      | 对一列时间直接调 ``.strftime``     | 用 ``.dt.strftime(...)``              |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``AttributeError: 'str' object has no attribute 'strftime'``                              | 报错      | 时间是字符串还不是 Timestamp       | 先 ``pd.to_datetime`` 再              |
|                                                                                           |           |                                    | ``.dt.strftime``                      |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``TypeError: Addition/subtraction of integers ... with Timestamp is no longer supported`` | 报错      | 时间戳直接 ``+ int``               | ``+ pd.Timedelta / pd.DateOffset`` 或 |
|                                                                                           |           |                                    | ``n * obj.freq``                      |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``TypeError: Cannot subtract tz-naive and tz-aware datetime-like``                        | 报错      | naive/aware 时区混算               | 先统一 ``tz_convert`` /               |
|                                                                                           |           |                                    | ``tz_localize``                       |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``TypeError: NDFrame.fillna() got an unexpected keyword argument 'method'``               | 报错      | pandas 3.x 用                      | 改用 ``.ffill()`` / ``.bfill()``      |
|                                                                                           |           | ``fillna(method='ffill')``         |                                       |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``ValueError: 'M' is no longer supported for offsets. Please use 'ME'``                   | 报错      | ``resample("M")`` /                | 用 ``"ME"``\ （2.x 里是弃用警告）     |
|                                                                                           |           | ``pd.Grouper(freq="M")`` 老写法    |                                       |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``ValueError: Index contains duplicate entries, cannot reshape``                          | 报错      | ``pivot`` 遇到重复键               | 用 ``pivot_table``\ （自动聚合）      |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``ParserError: Expected 3 fields in line 3, saw 4``                                       | 报错      | ``sep`` 分隔符判断错 /             | 检查 ``sep``\ ，核对脏行              |
|                                                                                           |           | 数据行多一个逗号                   |                                       |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``UnicodeDecodeError: ... invalid start byte``                                            | 报错      | 文件编码不是 utf-8（多是 gbk）     | 改 ``encoding="gbk"`` /               |
|                                                                                           |           |                                    | ``"utf-8-sig"``                       |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``FileNotFoundError: [Errno 2] No such file ...``                                         | 报错      | 文件路径/文件名写错                | 用绝对路径并确认文件在                |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``ValueError: Usecols do not match columns ... not found``                                | 报错      | ``usecols`` 列名列表含不存在的列   | 与 ``df.columns`` 对一遍              |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``ValueError: time data "notadate" doesn't match format``                                 | 报错      | ``to_datetime(format=...)``        | 去掉 format / 用 ``format='mixed'``   |
|                                                                                           |           | 格式不齐                           |                                       |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``KeyError: '站名'``\ （排序后）                                                          | 报错      | groupby                            | ``groupby(...).reset_index()`` 或     |
|                                                                                           |           | 后分组键成了索引，筛选又用普通列名 | ``as_index=False``                    |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``SettingWithCopyWarning``\ （2.x）/ ``ChainedAssignmentError``\ （3.x）                  | 警告/报错 | 链式赋值 ``df[条件][列]=值``       | 筛选用 ``.copy()``\ ，赋值用          |
|                                                                                           |           |                                    | ``.loc[条件,列]=值``                  |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``dtype: str`` / ``object`` 排进比较                                                      | 静默/报错 | 温度被当字符串，比较按字典序错     | ``print(df.dtypes)`` 先盯类型         |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| mean 默认跳过 NaN，\ ``skipna=False`` 返回 NaN                                            | 静默      | 满列缺测仍输出数字，或想跳过却没跳 | ``df.isna().sum()`` 先看缺测          |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| NaN 算术传染 / ``NaN == NaN`` 为 False                                                    | 静默      | 缺测参与加减乘除悄悄变 NaN         | 先 ``fillna``/``dropna``\ ，判断用    |
|                                                                                           |           |                                    | ``isna()``                            |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``fillna(0)`` 处理缺测再求平均                                                            | 静默      | 缺测当 0℃，平均被拉低              | 剔除可用 ``dropna``\ ，别当 0         |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| 只按 ``.dt.month`` 分组                                                                   | 静默      | 不同年份同月被并成一组             | ``pd.Grouper(key='date', freq='ME')`` |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| 时间未排序就 ``ffill``                                                                    | 静默      | 前向填充覆盖错误方向               | 先 ``sort_index()`` 再 ``ffill()``    |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``sort_values`` 后 index 没重置                                                           | 静默      | 行序号错乱，后续按位置取错         | 排序后 ``.reset_index(drop=True)``    |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+
| ``apply`` 忘写 ``axis=1``                                                                 | 静默      | 想按行算成了按列，形状对数值错     | 想逐行就 ``axis=1`` 写明白            |
+-------------------------------------------------------------------------------------------+-----------+------------------------------------+---------------------------------------+

..

   **一句话记住**\ ：Pandas 的报错有八成是
   **``KeyError``\ （键名/列名）、\ ``TypeError``\ （类型）、\ ``ValueError``\ （值非法）**
   三兄弟；剩下的阴险货全是\ **第 3 类静默错值**——NaN 传染、缺测当
   0、字符串字典序比较、跨年合并、ffill
   方向反。记一条铁律：\ **报错不可怕，怕的是「程序绿灯到底、数据科学全错」**\ ，下手前先
   ``print(df.dtypes)`` 和 ``print(df.isna().sum())``
   摸清类型与缺测，这就是 Pandas 的守门双式。

--------------

.. _71-索引三利器-lociloc--标签与位置的分野:

7.1 索引三利器 []、loc、iloc —— 标签与位置的分野
------------------------------------------------

.. _711-loc-传入列名不存在标签-keyerror报错:

7.1.1 ``loc`` 传入「列名/不存在标签」→ ``KeyError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：索引明明是字符串，却用 ``loc``
传整数；或把列名当成行标签取。先看成功与失败对照（真实运行）：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站名":["兰州","西安"],"气温":[5.1,8.2]},
                     index=["st1","st2"])   # 行索引是字符串标签
   print(df.loc["st1"])        # 成功: 按标签取
   print("---下面故意用位置整数当标签---")
   print(df.loc[0])            # 0 不是标签 -> KeyError

.. code:: text

   站名     兰州
   气温    5.1
   Name: st1, dtype: object
   ---下面故意用位置整数当标签---
   Traceback (most recent call last):
     ...
   KeyError: 0

另一例——想取列却把列名塞进 ``loc`` 的第一维（行位置）：

.. code:: python

   df2 = pd.DataFrame({"气温":[5.1,8.2,12.0]})     # 默认整数索引 0,1,2
   print(df2.loc["气温"])                           # '气温' 是列名, 不是行标签

.. code:: text

   KeyError: '气温'

**高亮关键词联想**\ ：\ ``KeyError: 'xxx'``——键不存在。\ ``xxx``
就是要找的名字：要么不在索引里（那是行标签），要么是拼写/大小写/中英文符号不对，要么你把它错放在了行位而它其实是列名。

**原因**\ ：\ ``loc``
的\ **第一维是行标签、第二维是列标签**\ 。标签有几分别写几，整数下标
``0`` 只有当你的行索引恰好是整数 ``0`` 时才合法；\ ``'气温'``
是列名，不在行索引里必 ``KeyError``\ 。

**解决办法**\ ：

- 先 ``print(df.index)`` 看行标签、\ ``print(df.columns)``
  看列名，\ **复制粘贴**\ ，别手敲；
- 按标签取行：\ ``df.loc["st1"]``\ ；按标签取列：\ ``df.loc[:, "气温"]``\ ；
- 你其实是想「取第 1 行」？那是位置，改用 ``df.iloc[0]``\ 。

..

   **气象场景一句话**\ ：\ ``loc``
   像「查台站名录」——你说要看「兰州站」这一页，名录里没有就只能回
   ``KeyError: 查无此站``\ ；而列名 ``气温``
   是「页面上那一栏」，你把它当成「页码」去翻，当然翻不到。报错里那个
   ``''`` 就是「你想查的名字」，顺着它去对 ``index``/``columns``
   清单最管用。

--------------

.. _712-iloc-传字符串标签-typeerror报错:

7.1.2 ``iloc`` 传字符串（标签）→ ``TypeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站名":["兰州","西安","成都"],"气温":[5.1,8.2,12.0]})
   print(df.iloc["x"])        # iloc 只能整数位置

.. code:: text

   Traceback (most recent call last):
     ...
   TypeError: Cannot index by location index with a non-integer key

**高亮关键词联想**\ ：\ ``Cannot index by location index with a non-integer key``——「位置索引只能用\ **非整数键**\ 之外的东西」。意思是：\ ``iloc``
是\ **位置**\ 运算符，它的键必须是整数（\ ``0,1,2...``
或切片），你却喂给它一个字符串。

**原因**\ ：\ ``iloc``\ （integer
location）管的是「第几格」，下标天生是整数；列名/行标签由 ``loc``
管。拿到
``TypeError: non-integer``\ ，十有八九是「把列名当位置、或把位置当标签」串了线。

**解决办法**\ ：想按名字 → ``loc``\ ；想按位置 →
``iloc``\ 。口诀：\ **``loc`` 是「查名字」，\ ``iloc``
是「数格子」，名字用 ``loc``\ 、格子用 ``iloc``**\ 。

   **气象场景一句话**\ ：点名报「第 3
   个站」是位置（\ ``iloc[2]``\ ），报「兰州站」是名字（\ ``loc['兰州']``\ ）。你把「兰州」两个字丢给报位置的人，他只能回一句「我只认数字，不认字」。

--------------

.. _713-iloc-整数下标越界--indexerror报错:

7.1.3 ``iloc`` 整数下标越界 → ``IndexError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"气温":[5.1,8.2,12.0]})   # 3 行, 下标 0,1,2
   print(df.iloc[10])

.. code:: text

   Traceback (most recent call last):
     ...
   IndexError: single positional indexer is out-of-bounds

**高亮关键词联想**\ ：\ ``IndexError ... out-of-bounds``——「下标越界」。位置下标的合法范围永远是
``0 .. 行数-1``\ ，超出即报。注意它的行数是“行数”不是长度单位，先
``len(df)`` 打底。

**原因**\ ：\ ``iloc[10]`` 想取第 11 行，表只有 3
行。位置索引严格校验，越界当场叫停（与第 6 章 numpy 整数下标越界同源）。

**解决办法**\ ：先 ``df.shape`` / ``len(df)``\ ，确认
``0 ≤ 位置 ≤ 行数-1``\ 。想取前 N 行用
``df.iloc[:5]``\ （切片不越界，见正文 7.3.2）。

   **气象场景一句话**\ ：\ ``iloc`` 越界就像「从 8 站的观测记录里抽第 9
   站」——点名册里根本没这人，立即报
   ``IndexError: 查无此人``\ ，绝不会静默给你占位。

--------------

.. _714-loc-的返回类型单列-series列表包一下-dataframe常被忽视的静默差异:

7.1.4 ``loc`` 的返回类型：单列 ``=``\ Series、列表包一下 ``=``\ DataFrame（常被忽视的静默差异）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ （不是报错，是隐蔽的类型坑）：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站名":["兰州","西安","成都"],"气温":[5.1,8.2,12.0]})
   print(type(df.loc[:, "气温"]))        # 单个列名 -> Series (一维)
   print(type(df.loc[:, ["气温"]]))      # 列名列表 -> DataFrame (二维)

.. code:: text

   <class 'pandas.Series'>
   <class 'pandas.DataFrame'>

**原因**\ ：\ ``loc``/``df[]`` 里，\ **一个列名给出一维
Series，列名列表给出一张二维 DataFrame**\ 。初学者常想「我要一张表继续做
``.columns``\ 」，结果拿到 Series 就报
``AttributeError``\ ；或反过来想在 Series 上用 DataFrame 的语法。

**解决办法**\ ：想保留
DataFrame（多列/当作表的操作）就\ **用列表包住列名**
``df[["气温"]]``\ ；只要一列数值就
``df["气温"]``\ 。若对返回值是不是表有疑虑，\ ``print(type(x))``
一眼看穿。

   **气象场景一句话**\ ：\ ``df["气温"]``
   是「单独一根气温柱」，\ ``df[["气温"]]``
   是「把这一格画成一张单列报表」。报表能装进报表框（受 DataFrame
   方法约束），一根柱子只能当一维数组用——先想清楚你要柱子还是报表，再决定加不加那个方括号。

--------------

.. _72-nan-与缺测pandas-的毒与药:

7.2 NaN 与缺测：Pandas 的「毒」与「药」
---------------------------------------

   **先立一个铁律**\ ：在 Pandas 里，\ ``mean/sum/max/min/std``
   等聚合方法\ **默认 ``skipna=True``\ （跳过 NaN）**\ ，这与 NumPy 的
   ``np.mean`` **正好相反**\ （numpy 不跳、一遇 NaN 就返回 NaN，见第 6
   章 6.5.1）。这两家行为相反，是本章最容易混的静默坑——用 NumPy
   那套「看到了 NaN 就得手动 nanmean」的手感套
   Pandas，反而想跳过却跳掉了该关注的缺测。\ **下面每个例子都是实测。**

.. _721-mean-默认跳过-nan但缺测转-numpy-或-skipnafalse-就返回-nan静默:

7.2.1 ``mean()`` 默认跳过 NaN，但缺测转 numpy 或 ``skipna=False`` 就返回 NaN（静默！）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd, numpy as np
   t = pd.Series([22.0, np.nan, 28.0, 31.0])
   print("1) pandas .mean() 默认skipna=True ->", t.mean())
   print("2) skipna=False ->", t.mean(skipna=False))
   print("3) 转成 numpy 再用 np.mean ->", np.mean(t.values))
   print("4) 算术传染 ->", list(t + 10))
   print("5) .sum() 默认也跳过 ->", t.sum(), " skipna=False ->", t.sum(skipna=False))

.. code:: text

   1) pandas .mean() 默认skipna=True -> 27.0
   2) skipna=False -> nan
   3) 转成 numpy 再用 np.mean -> nan
   4) 算术传染 -> [32.0, nan, 38.0, 41.0]
   5) .sum() 默认也跳过 -> 81.0  skipna=False -> nan

**高亮关键词联想**\ ：输出里那个 ``nan`` 就是信号。它出现在第 2、3、5
个里：\ **``skipna=False`` 时缺测毒化结果**\ 、\ **转成 numpy 再
``np.mean`` 也被毒化**\ ；而普通 ``t.mean()`` 给出正常的 ``27.0``\ （4
个数里有 3 个有效 → 均 27）。

**原因**\ ：Pandas 聚合默认跳过 NaN（只对有效值计算），所以第
1（\ ``.mean()``\ ）和第 5（\ ``.sum()``\ ）默认安全；但一旦你（a）显式
``skipna=False``\ ，或（b）把 Series ``.values`` 丢给 numpy 的
``np.mean``\ （numpy 不跳），或（c）让 NaN
参与逐元素四则运算（\ ``t + 10``\ ），NaN 就会传染成一片（第 4
行即每次元素 ``+10`` 时把 NaN 保留成 NaN）。

**解决办法**\ ：气象业务里「这一站/这一天缺测」是常态。逐站点统计优先用
Pandas 自带聚合（默认跳过即可），但\ **心里要有数**\ ：跳过 NaN
的均值在用缺测少的样本算，别拿它当「全站平均」。若某段全缺测，\ ``mean()``
会返回 ``nan``——这是「该段不可信」的正确表达，宁可保留 ``nan`` 也别
``fillna(0)``\ 。想 numpy 也能跳过就用 ``np.nanmean(t.values)``\ 。

   **气象场景一句话**\ ：Pandas 的默认「跳过缺测」像气象台统计 8
   站均温时\ **自动把缺测站剔除只用其余 7 站**\ ；而 ``skipna=False`` /
   ``np.mean`` / 四则运算就是「带着缺测站一起算」，一个 NaN
   像一粒毒，把整锅平均毒成 ``nan``\ 。报不报错？\ **不报。**
   所以「结果是一串 nan」时，先怀疑 ``skipna`` 和缺测。

--------------

.. _722-nan--nan-永为-false判断缺测要用-isna静默:

7.2.2 ``NaN == NaN`` 永为 False，判断缺测要用 ``isna()``\ （静默！）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd, numpy as np
   s = pd.Series([1.0, np.nan, 2.0])
   print("NaN == NaN 逐元素 ->", list(s == np.nan))   # 全False!
   print("(s>1) 也有NaN:", list(s > 1))
   print("用 isna 才对:", list(s.isna()))
   print("where(True保留):", list(s.where(s.notna(), "缺")))
   print("mask(True替换):", list(s.mask(s.isna(), 0.0)))

.. code:: text

   NaN == NaN 逐元素 -> [False, False, False]
   (s>1) 也有NaN: [False, False, True]
   用 isna 才对: [False, True, False]
   where(True保留): [1.0, '缺', 2.0]
   mask(True替换): [1.0, 0.0, 2.0]

**高亮关键词联想**\ ：三个元素里明明有个 ``nan``\ ，\ ``s == np.nan``
却\ **全是 False**——因为 ``NaN``
不等于任何值、甚至不等于它自己。想「找出缺测在哪」用 ``==``
是找不到的；\ ``isna()`` / ``notna()``
才是探测缺测的专业工具；\ ``where``/``mask`` 是更精细的替换开关。

**原因**\ ：IEEE 规定 ``NaN != NaN``\ 。用等号筛缺测必得全
False，等于「舞弊式」地以为没有缺测，你的高温筛选就把缺测行全漏了。

**解决办法**\ ：探测缺测用
``s.isna()``\ ；替换两者皆可：\ ``s.where(s.notna(), 填充值)``\ （不满足处填）或
``s.mask(s.isna(), 填充值)``\ （满足处填）。\ ``where``/``mask``
把「条件控制替换」交给 pandas，比手写循环干净。

   **气象场景一句话**\ ：\ ``NaN``
   是「观测失效」的标记，像一张被雨淋花了的记录纸——你拿「这张纸是不是记录纸（==）」去问，它会回答「不是」，因为它已经花到认不出自己了。\ ``.isna()``
   才是拿着官网缺测目录逐条对的稽查员。

--------------

.. _723-把缺测当-0-求平均--均值被拉低静默最经典的业务错误:

7.2.3 把缺测当 0 求平均 → 均值被拉低（静默！最经典的业务错误）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd, numpy as np
   df = pd.DataFrame({"站名":["兰州","西安","成都","西宁"],
                      "气温":[np.nan,8.2,12.0,9.5]})
   wrong = df["气温"].fillna(0.0).mean()     # 错误: 缺测当0℃
   right = df["气温"].dropna().mean()        # 正确: 剔除缺测
   print("fillna(0) 再 mean =", round(wrong,2), "  <- 缺测被当成0℃")
   print("dropna() 再 mean   =", round(right,2), "  <- 剔除缺测")
   print("缺测个数:", df["气温"].isna().sum())

.. code:: text

   fillna(0) 再 mean = 7.42   <- 缺测被当成0℃
   dropna() 再 mean   = 9.9   <- 剔除缺测
   缺测个数: 1

**高亮关键词联想**\ ：没有报错，只有数字差别——``7.42`` 对 ``9.9``\ 。这
2.5℃ 的差，就是「把缺测填 0 再平均」凭空造出来的误差。

**原因**\ ：\ ``fillna(0)`` 把缺失气温当成真实的 0℃ 放进平均，3 个样本
9.9 变成 4 个样本里的 0 →
平均被狠狠拉低。气象里「缺测」意思是\ **没测到**\ ，不是「0℃也无所谓」；0
是真实且合理的低温值，两者语义完全不同。

**解决办法**\ ：统计前先 ``print(df.isna().sum())``\ （正文
7.3/最佳实践第一步）。处理二选一：\ **要用均值 → ``dropna()``
剔除**\ ；\ **要保留行形状 →
对别的列统计，缺测列标记为“不可用”**\ 。绝不要 ``fillna(0)``
后直接平均——除非你明确知道缺测含义就是 0（如「无降水」可填
0mm，但气温/湿度绝不可）。

   **气象场景一句话**\ ：兰州这天温度缺测，你把它填 0℃
   一起平均，等于「没测到的 25℃ 被记成 0℃」——西北 7
   月秒变冰窟，任何一张区域平均温度图都会被这一下拉出冰点。\ **缺测 ≠
   0**\ ，是气象里比任何报错都贵的一条经验。

--------------

.. _724-在筛选子集上-fillna-inplacetrue--不生效--链式赋值告警静默或警告:

7.2.4 在筛选子集上 ``fillna(..., inplace=True)`` → 不生效 / 链式赋值告警（静默或警告）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出（pandas 3.x）**\ ：

.. code:: python

   import pandas as pd, numpy as np
   df = pd.DataFrame({"站名":["兰州","西安","成都"],"气温":[np.nan,8.2,12.0]})
   sub = df[df["气温"]>5.0]                       # 筛选出的子集
   sub["气温"].fillna(0.0, inplace=True)          # 想在此填缺测
   print(df)   # 原表缺测没被填! 填的是个副本

.. code:: text

   <你脚本路径>/t08_fillna_inplace_subset.py:6: ChainedAssignmentError:
     A value is being set on a copy of a DataFrame or Series through chained
     assignment using an inplace method.
     Such inplace method never works to update the original DataFrame or Series,
     because the intermediate object on which we are setting values always behaves
     as a copy (due to Copy-on-Write).
     ... try using 'df.method({col: value}, inplace=True)' instead ...
     sub["气温"].fillna(0.0, inplace=True)   # 改的可能只是副本
      站名    气温
   0  兰州   NaN
   1  西安   8.2
   2  成都  12.0

**版本说明**\ ：pandas 2.x 这里弹的警告叫
``SettingWithCopyWarning``\ （不中断）；pandas 3.x 升级为
``ChainedAssignmentError``\ （见
7.6.3）。共同点：\ **子集是临时副本，inplace
改的是副本，原表纹丝不动**——你看输出里 ``气温`` 的 ``NaN`` 一个没少。

**高亮关键词联想**\ ：\ ``ChainedAssignmentError`` /
``SettingWithCopyWarning``——链式赋值、改副本；\ ``.inplace=True``
用在了既不是原表又不是可落地对象的地方，等于白改。

**原因**\ ：\ ``df[df["气温"]>5]["气温"]``
是一次\ **链式取值**\ ，得到的是可能存在 write 问题的中间副本；对它
``inplace`` 填缺测，修改流进临时对象不回流原表。

**解决办法**\ ：要么直接对原列赋值
``df.loc[df["气温"]>5, "气温"] = df.loc[df["气温"]>5, "气温"].fillna(0)``\ ；要么先
``.copy()`` 再改 ``sub = df[df["气温"]>5].copy()``\ ；要么干脆
``df["气温"] = df["气温"].fillna(0)``\ （一行搞定原列）。\ **气象实操更推荐第三种**——先统一清洗好全表缺测，再做筛选，步骤少、坑也少。

   **气象场景一句话**\ ：你想「把兰州这天的缺温补上」，却在「筛出来的一份复印件」上改——原件（原表）还是缺测。链式赋值警告就是打印机在你耳边说「你改的是副本，原件没动」，可惜它只是小声提醒，没报错，有心人才听得到。

--------------

.. _73-数据类型astype--to_numeric--读-csv-的类型推断:

7.3 数据类型：astype / to_numeric / 读 CSV 的类型推断
-----------------------------------------------------

.. _731-astypefloat-遇到非数字字符串--valueerror报错:

7.3.1 ``astype(float)`` 遇到非数字字符串 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"气温_原始":["5.1","8.2","MISS"]})   # 温度记录混进缺测标记
   print(df["气温_原始"].astype(float))

.. code:: text

   Traceback (most recent call last):
     ...
   ValueError: could not convert string to float: 'MISS'

**高亮关键词联想**\ ：\ ``could not convert string to float: 'MISS'``——「不能把字符串转成浮点数」，其中
``'MISS'`` 就是那个转不动的字符串。和 NumPy 6.4.2
是同一句灵魂：\ **字符串里藏了非数字符**\ 。

**原因**\ ：\ ``astype(float)`` 要求每个字符串都能被 ``float()``
解析；\ ``"5.1"``\ 、\ ``"8.2"``
行，\ ``"MISS"``\ （缺测标记）转不了直接中断。

**解决办法**\ ：

- 知道缺测标识 → 读取时用 ``na_values=["MISS","9999"]``\ （正文 read_csv
  最佳实践），或 ``df.replace("MISS", np.nan).astype(float)``\ ；
- 兜底 → ``pd.to_numeric(df["气温"], errors="coerce")``\ （见 7.3.2）。

..

   **气象场景一句话**\ ：温度记录里混进一行
   ``MISS``\ ，等于自动站报文里夹了句「本时次故障」——你得先认出这个哨兵转成
   NaN，而不是让求和在半路当场噎住报 ``could not convert``\ 。

--------------

.. _732-astype-一次失败-vs-to_numericerrorscoerce-丢卒保车对比:

7.3.2 ``astype`` 一次失败 vs ``to_numeric(errors='coerce')`` 丢卒保车（对比）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"气温txt":["5.1","8.2","MISS","12.0"]})
   print("coerce =", list(pd.to_numeric(df["气温txt"], errors="coerce")))
   print("errors='raise' 则是报错:")
   print(pd.to_numeric(df["气温txt"], errors="raise"))

.. code:: text

   coerce = [5.1, 8.2, nan, 12.0]
   errors='raise' 则是报错:
   Traceback (most recent call last):
     ...
   ValueError: Unable to parse string "MISS" at position 2

**高亮关键词联想**\ ：\ ``coerce`` 就是「强行转，转不动的塞成
NaN（coerce =
强迫/强转）」；\ ``Unable to parse string "MISS" at position 2``——第 2
个元素解析失败（注意是位置，从 0 起，所以 ``"MISS"`` 在下标 2）。

**原因**\ ：\ ``astype``
是「非转不可，不行就报错」；\ ``to_numeric(errors='coerce')``
是「能转的转、不能转的放 NaN」——前者一个坏蛋拖全队，后者单个处理。

**解决办法**\ ：气象清洗缺测优先 ``errors='coerce'``\ ，把坏值转 NaN
后再结合 ``dropna``/``isna`` 处理；若想彻底查清哪个值坏，先
``errors='raise'`` 报一次位置看现场。

   **气象场景一句话**\ ：\ ``astype``
   像「全班必须交出学号，缺一张揪出来重罚」；\ ``to_numeric(coerce)``
   像「没学号的先记成待定(NaN)，等补录再处理」。气象数据缺测常态，多交给「待定」而非「判死刑」。

--------------

.. _733-读-csv-后温度被推断成字符串与数字比较出错静默--报错取决于版本:

7.3.3 读 CSV 后温度被推断成字符串，与数字比较出错（静默 / 报错取决于版本）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 a —— pandas
2.x（多数网上的老代码行为）：字符串按字典序比较，静默错误**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"气温":["100","9","30","50"]})   # 温度读成了字符串
   hot = df[df["气温"] > "30"]
   print(hot)      # 字符串按字典序: "9" > "30" 为真!

.. code:: text

      气温
   1   9
   3  50

**高亮关键词联想**\ ：筛选出的居然有 ``9`` 和 ``50`` 而漏掉
``100``——因为字符串 ``"100" < "30"``\ （\ ``'1'`` 比 ``'3'``
小）、\ ``"9" > "30"``\ （\ ``'9'`` 比 ``'3'``
大）。这就是\ **字典序（lexicographic）比较**\ ：按字符一个个比，不是按数值大小比。

**原因**\ ：\ ``dtype`` 是字符串时，\ ``>``
是逐字符字典序遍历；\ ``"9"`` 和 ``"30"`` 首字符 ``'9' > '3'``\ ，于是“9
比 30 大”这种荒谬结论出现。气象里「温度 9 > 30」就是假象。

**现象 b —— pandas 3.x 新字符串 dtype：同比较直接报错**\ ：

.. code:: python

   from io import StringIO
   txt2 = "站名,气温\n兰州,5.1\n西安,缺\n成都,12.0\n"
   df2 = pd.read_csv(StringIO(txt2))            # 混入"缺" -> 整列变字符串
   print("dtype:", df2["气温"].dtype)
   print(df2["气温"] > 10)

.. code:: text

   dtype: str
   Traceback (most recent call last):
     ...
   TypeError: Invalid comparison between dtype=str and int

**高亮关键词联想**\ ：\ ``dtype=str`` +
``Invalid comparison between dtype=str and int``——**类型是字符串却拿去和整数比较**\ 。这是
pandas 3.x 的「新好人病」：宁可报错也不让你静默错算。

**原因**\ ：只要一列里混进任意文本（如本站一条“缺”），read_csv
无法整列转数值，就把整列推断成字符串；3.x 对 str vs int 比较直接抛
``TypeError``\ ，2.x 则静默给出字典序错结果。

**解决办法**\ ：先 ``print(df.dtypes)`` 盯一眼类型；发现
``str``/``object`` 就 ``pd.to_numeric(df["气温"], errors="coerce")``
转回数值再比较、再筛选。\ **这是 7.0
里最该背的前置动作——气象里一半的“筛选没筛对”都栽在类型上。**

   **气象场景一句话**\ ：站表里混进一个“缺”字，整列气温被读成文本——你按
   ``>30`` 筛高温日，字典序把 ``9`` 当成了比 ``30``
   还高的气温，高温日清单当场造假。3.x 干脆报 ``dtype=str``
   让你先转清楚再算，反而是救你。

--------------

.. _74-datetime64-时间类型一整套时间专项坑:

7.4 datetime64 时间类型：一整套时间专项坑
-----------------------------------------

.. _741-对一列时间直接-strftime--attributeerror报错:

7.4.1 对一列时间直接 ``.strftime`` → ``AttributeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   s = pd.Series(["2026-08-14","2026-08-15"])     # 还是字符串
   print(s.strftime("%Y"))                          # Series 没有 strftime 方法

.. code:: text

   Traceback (most recent call last):
     ...
   AttributeError: 'Series' object has no attribute 'strftime'. Did you mean: 'at_time'?

**高亮关键词联想**\ ：\ ``'Series' object has no attribute 'strftime'``——**Series（整列）没有
strftime 方法**\ 。时间方法都挂在一个叫 ``.dt`` 的访问器下面，得写
``s.dt.strftime(...)``\ 。

**原因**\ ：Pandas 把「对一列每个元素做时间格式化」统一放在
``Series.dt`` 命名空间；直接对 Series 调 ``.strftime``
不存在（提示给的是相近误拼 ``at_time``\ ）。

**解决办法**\ ：格式化成字符串 →
``s.dt.strftime("%Y-%m")``\ ；如果你的列还是普通字符串，\ **先
``pd.to_datetime(s)``**\ （见 7.4.2/7.4.5）。元素取出后是
``Timestamp``\ ，它有
``strftime``\ ：\ ``t0 = pd.to_datetime("2026-08-14"); t0.strftime("%Y")``\ （见
7.4.5）。

**顺带第三条**\ （字符串本身 ``.strftime``\ ）：

.. code:: python

   print("2026-08-14".strftime("%Y"))     # 字符串没有 strftime

.. code:: text

   AttributeError: 'str' object has no attribute 'strftime'

..

   **气象场景一句话**\ ：\ ``.dt`` 是 Pandas
   给「一整列日期」配的专属工具箱——年、月、日、季度、星期几都在这儿。你绕过
   ``.dt`` 直接喊 ``.strftime``\ ，等于绕过工具箱伸手抓工具，自然
   ``AttributeError``\ 。

--------------

.. _742-时间戳直接--int--typeerror报错:

7.4.2 时间戳直接 ``+ int`` → ``TypeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   t = pd.Timestamp("2026-08-20")
   print(t + 3)          # 妄图"日期+3"=加3天

.. code:: text

   Traceback (most recent call last):
     ...
   TypeError: Addition/subtraction of integers and integer-arrays with Timestamp is no longer supported.  Instead of adding/subtracting `n`, use `n * obj.freq`

**高亮关键词联想**\ ：\ ``Timestamp is no longer supported`` +
``use n * obj.freq``——老版本里警告过「别用整数直接加时间」，新版本直接改成报错，并提示你用\ **时间偏移量**\ 。

**原因**\ ：\ ``2026-08-20`` 是时刻，\ ``3`` 是「3
个单位天数」，两个量纲不同，不能直接相加。「日期加 3
天」必须显式给出偏移对象。

**解决办法**\ （三选一）：

.. code:: python

   t + pd.Timedelta(days=3)      # 推荐的"加 N 天"
   t + pd.DateOffset(months=1)   # 加月用 DateOffset (不是均一的30天)
   t + 3 * pd.Timedelta(days=1)

**实测对照**\ （正确加法，真实输出）：

.. code:: python

   a = pd.Timestamp("2026-08-14")
   print("加一天:", a + pd.Timedelta(days=1))
   print("加一个月:", a + pd.DateOffset(months=1))

.. code:: text

   加一天: 2026-08-15 00:00:00
   加一个月: 2026-09-14 00:00:00

..

   **气象场景一句话**\ ：往前推一天、往前推一月，是气候统计的常客。但
   ``Timestamp + 3`` 就像「今天+3」——3 是什么？3 天？3
   小时？语义模糊，Pandas 干脆报错让你说清楚偏移量
   ``Timedelta("3D")``\ 。加小时用 ``pd.Timedelta(hours=6)``\ ，加月必用
   ``DateOffset``\ 。

--------------

.. _743-两个-timestamp-相减--timedelta不是浮点取-daystotal_seconds:

7.4.3 两个 Timestamp 相减 → Timedelta（不是浮点，取 ``.days``/``.total_seconds()``\ ）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd
   a = pd.Timestamp("2026-08-14")
   b = pd.Timestamp("2026-08-25")
   d = b - a
   print("两个Timestamp相减 ->", repr(d), "类型:", type(d).__name__)

.. code:: text

   两个Timestamp相减 -> Timedelta('11 days 00:00:00') 类型: Timedelta

**高亮关键词联想**\ ：类型是 ``Timedelta``\ ，打印出来
``11 days 00:00:00``\ 。你若直接拿 ``d`` 当普通数字 →
``TypeError``\ ；取天数要用 ``d.days``\ （整数天）或
``d.total_seconds()``\ （含小数秒）。

**原因**\ ：两个时刻之差是「时间间隔」，这是第三种时间类型
``Timedelta``\ ，不是 float，不是 int。

**解决办法**\ ：\ ``d.days`` 得 11；跨时几小时几分几秒用
``d.total_seconds()/3600``
得小时数。气象里「从某时刻距今天数」「间隔小时数」常靠它。

   **气象场景一句话**\ ：台风 8 月 25 日登陆、8 月 14
   日生成，中间隔几天？「11 天」是 Timedelta 的属性 ``days``——不是随便
   ``str(d)`` 里的字串，是能继续参与计算的数值 ``d.days``\ 。

--------------

.. _744-忘了-import-datetime-就用-strptime--nameerror报错:

7.4.4 忘了 ``import datetime`` 就用 ``strptime`` → ``NameError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   # 忘了: from datetime import strptime
   print(strptime("20260814","%Y%m%d"))

.. code:: text

   Traceback (most recent call last):
     ...
   NameError: name 'strptime' is not defined

**高亮关键词联想**\ ：\ ``NameError: name 'strptime' is not defined``——``strptime``
没定义。它来自标准库 **``datetime`` 模块**\ ，不 import 就不在命名空间。

**原因**\ ：\ ``strptime``\ （string parse time，字符串→时间）是
``datetime.datetime.strptime`` 的用法，须先
``from datetime import datetime, strptime``\ （或 ``import datetime``
后用 ``datetime.datetime.strptime``\ ）。注意正文区分：\ **Pandas
里几乎只用 ``pd.to_datetime``\ ，\ ``strptime`` 是 Python
标准库的事**\ ，别混。

**解决办法**\ ：二选一——``from datetime import datetime; datetime.strptime("20260814","%Y%m%d")``\ ，或直接用
Pandas
``pd.to_datetime("20260814", format="%Y%m%d")``\ （气象更常见）。两者的关系：\ ``pd.to_datetime``
内部就是对整列批处理 ``strptime``\ ，所以你想批处理 → 用
pandas；想算单个时刻/伪照标准库用 strptime。

   **气象场景一句话**\ ：\ ``strptime`` 像「驿站翻译官」，把
   ``20260814``
   这种报文翻译成年月日。但翻译官得先请进门（import），没进门就喊他 =
   对讲机里呼叫一个不在岗的人，报 ``NameError``\ 。

--------------

.. _745-pdto_datetimeformat-格式不齐--valueerror报错用-formatmixed去掉-format:

7.4.5 ``pd.to_datetime(format=...)`` 格式不齐 → ``ValueError``\ （报错），用 ``format='mixed'``/去掉 format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   s = pd.Series(["20260814","20260815","notadate"])
   print(pd.to_datetime(s, format="%Y%m%d"))

.. code:: text

   Traceback (most recent call last):
     ...
   ValueError: time data "notadate" doesn't match format "%Y%m%d". You might want to try:
       - passing `format` if your strings have a consistent format;
       - passing `format='ISO8601'` ...
       - passing `format='mixed'`, and the format will be inferred ...

**高亮关键词联想**\ ：\ ``doesn't match format "%Y%m%d"``——有表达格式串但数据不听话；提示的三点里
``format='mixed'`` 是「让 pandas 逐条猜格式」。

**原因**\ ：指定了 ``format``\ （严格要求每格都是
``8 位年月日``\ ），遇到非格式化数据 ``"notadate"``
直接解析失败。缺测/异常值混进来时很常见。

**解决办法**\ ：数据格式统一 → 用
``format``\ （更快更稳）；含不齐格式/脏数据 →
``format="mixed"``\ （逐条推断）或先清洗 ``errors="coerce"`` 把坏值塞成
NaN。正文提示的 ``20260814`` 固定格式手动
``to_datetime(format="%Y%m%d")`` 正是为了快。

   **气象场景一句话**\ ：观测档案里某行日期写成了
   ``notadate``\ （录入事故），你要求整列必须 ``YYYYMMDD``\ ，Pandas
   读到这里当场反水。给 ``format='mixed'``
   让它「哪条合适哪条猜」，才像审档案的主任一样逐个放行。

--------------

.. _75-read_csv-读取路径编码分隔符列名的四大坑:

7.5 read_csv 读取：路径、编码、分隔符、列名的四大坑
---------------------------------------------------

.. _751-文件路径不对--filenotfounderror报错:

7.5.1 文件路径不对 → ``FileNotFoundError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   pd.read_csv("D:/Code/Vibe/QA/_sim/data/not_exist_123.csv")

.. code:: text

   Traceback (most recent call last):
     ...
   FileNotFoundError: [Errno 2] No such file or directory: 'D:/Code/Vibe/QA/_sim/data/not_exist_123.csv'

**高亮关键词联想**\ ：\ ``No such file or directory: '路径'``——文件或目录不存在。\ ``Errno 2``
是系统级「查无此文件」。

**原因**\ ：路径写错一字、文件名错、文件根本不在那个盘/目录，或工作目录不对。Thread
里读中文路径/目录带中文空格在 Windows
上一般能读，但最容易栽的是「相对路径」算错了基准。

**解决办法**\ ：最稳是写\ **绝对路径**\ 且确认文件真的在那：先在资源管理器里打开目录核对文件名（含后缀
``.csv``\ ）；或 ``import os; print(os.path.exists(path))`` 返回 False
就说明路径错。建议把路径一顿 print 出来复制，别手敲。

   **气象场景一句话**\ ：你让程序去读
   ``data/weather.csv``\ ，程序按当前工作目录找，「查无此文件」就像气象台值班室去存放间拿今天的报文却被告知没这份记录——先问「文件真在那吗？名字对吗？」

--------------

.. _752-编码不对中文乱码--读不了-unicodedecodeerror报错:

7.5.2 编码不对（中文乱码 / 读不了）→ ``UnicodeDecodeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：文件是 gbk 编码（Excel 在 Windows 常存成 gbk
/ 或你之前 ``to_csv`` 用了 gbk），却用 utf-8 读。

.. code:: python

   import pandas as pd
   csv_path = "D:/Code/Vibe/QA/_sim/data/gbk_cn.csv"
   # (该文件已用 encoding="gbk" 写入超码后)
   df = pd.read_csv(csv_path, encoding="utf-8")
   print(df)

.. code:: text

   Traceback (most recent call last):
     ...
   UnicodeDecodeError: 'utf-8' codec can't decode byte 0xba in position 2: invalid start byte

**高亮关键词联想**\ ：\ ``UnicodeDecodeError: 'utf-8' codec can't decode byte 0xba in position 2``——解码器撞到无效字节
``0xba``\ 。中文 UTF-8 时首字节是 ``0xE..`` 系列；出现 ``0xba/0xbb``
多半是 **gbk 编码**\ （或 gbk 写、utf-8
读）。这是中文表头乱码/读不了的元凶。

**原因**\ ：文件实际字节是 gbk，用 utf-8（或纯 utf-8 不带
BOM）去解码到某个中文字时就对不上。

**解决办法**\ ：循环换编码试：\ ``gbk`` → ``gb18030`` →
``utf-8-sig``\ 。正文的最佳实践是\ **固定用 ``utf-8-sig``**\ （带
BOM，Excel 亲儿子）；遇到 ``UnicodeDecodeError`` 就改
``encoding="gbk"``\ 。读出来没关系、图/列表中文变乱码，多半是「没带
``utf-8-sig``\ 」写出的文件被 Excel 打开成乱码（见 7.5.6）。

   **气象场景一句话**\ ：编码不匹配就像用「英文键盘的对照表去读一份俄文电报」——读到某个字节
   0xba 发现对不上号，只能当场报 ``UnicodeDecodeError``
   告诉你「这份电报不是 utf-8 语系」。气象中文表头尤其爱踩。

--------------

.. _753-分隔符判断错--数据行多一个逗号--parsererror报错:

7.5.3 分隔符判断错 / 数据行多一个逗号 → ``ParserError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：文件某行多出一个逗号，列数与表头对不上。

.. code:: python

   import pandas as pd
   from io import StringIO
   txt = "站号,站名,气温\n58367,上海,32.0\n54511,北京,3,4.0\n"   # 第2行多了个逗号
   df = pd.read_csv(StringIO(txt), sep=",")

.. code:: text

   Traceback (most recent call last):
     ...
   pandas.errors.ParserError: Error tokenizing data. C error: Expected 3 fields in line 3, saw 4

**高亮关键词联想**\ ：\ ``ParserError`` +
``Expected 3 fields in line 3, saw 4``——第三行本应 3 个字段(逗号 2
个)，却看到了 4 个。\ **列数不满/超贵**\ ，pandas 报解析错误。

**原因**\ ：\ ``sep`` 分错了方向（文件实际用 ``;`` 或制表符但你没设
``sep``\ ），或某个数据行内部夹了逗号（如数值 ``3,4`` 当作 ``3.4``
的笔误、或多余分隔符）。一行字段数与表头不一致直接中断。

**解决办法**\ ：

- 换 ``sep``\ ：分号文件 ``sep=";"``\ ，制表符 ``sep="\t"``\ ，多空格
  ``sep=r"\s+"``\ ；
- 只在特定几列需要字段内逗号时可加 ``quoting``/``quotechar``\ ，但气象
  CSV 少用；先查源文件那一行为何多一个逗号；
- 暂时跳过坏行可用 ``error_bad_lines``\ （老版）/
  ``on_bad_lines='skip'``\ （新版），但\ **最好查清坏行根因**\ 再决定
  skip 还是修。

..

   **气象场景一句话**\ ：\ ``Expected 3 fields, saw 4``
   就像你让助手把每份报文按逗号拆成「站号,站点,温度」三段，结果婉档里某条多塞了个「,」多了段——助手不会猜，直接停手报告「第
   3 行段落数不对劲」。

--------------

.. _754-usecols-列名对不上--valueerror报错:

7.5.4 ``usecols`` 列名对不上 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   path = "D:/Code/Vibe/QA/_sim/data/weather_stations.csv"
   df = pd.read_csv(path, usecols=["站号","气温","不存在列"])

.. code:: text

   Traceback (most recent call last):
     ...
   ValueError: Usecols do not match columns, columns expected but not found: ['不存在列']

**高亮关键词联想**\ ：\ ``Usecols do not match columns ... expected but not found: ['不存在列']``——``usecols``
里有个列名文件里没有。这是拼写/中文符号/大小写问题。

**解决办法**\ ：先 ``df = pd.read_csv(path)`` 读一次看
``df.columns``\ ，把真列名复制进 ``usecols``\ ；或干脆先全部读入再用
``df[["站号","气温"]]`` 选列。\ ``usecols`` 还能传位置
0/1/2（但传名字更可读）。

   **气象场景一句话**\ ：你只要 ``["站号","气温"]``
   两三列省内存，却把列表里的列名写错——像点名想让「兰州站、西安站」出列，单子上却写成了「兰州站、兰卅站」，名单对不上，报
   ``ValueError`` 让你改。

--------------

.. _755-csv-没有表头--第一行其实是数据--静默把数据当列名静默:

7.5.5 CSV 没有表头 / 第一行其实是数据 → 静默把数据当列名（静默！）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd
   from io import StringIO
   txt = "上海,32.0\n北京,34.0\n武汉,38.0\n"    # 第一行其实是数据, 没有表头
   df = pd.read_csv(StringIO(txt))               # header 默认=0: 第一行当列名!
   print(df)
   print("列名被污染:", list(df.columns))

.. code:: text

      上海  32.0
   0  北京  34.0
   1  武汉  38.0
   列名被污染: ['上海', '32.0']

**高亮关键词联想**\ ：列名变成了
``['上海','32.0']``——第一行数据被当成了表头，整张表少了一行、列名被污染。

**原因**\ ：\ ``read_csv`` 默认 ``header=0``\ （把第 0
行当列名）。文件如果真有表头那是对的；如果文件本来就是「第一行 =
数据、无表头」，就会把第一行数据吞成列名。

**解决办法**\ ：无表头文件加 ``header=None`` 并自定义名字
``df = pd.read_csv(txt, header=None, names=["站名","气温"])``\ ；或
``header=0`` 明确告诉它「第 0 行是表头」。对策前先
``pd.read_csv(path).head(3)`` 看第一行是不是数据。

**顺带**\ ：正文读写都建议 ``index=False`` / ``index_col``——``to_csv``
默认会把索引写成第一列，读回来的第一列常是莫名排水的 index 配
``Unnamed: 0``\ 。

   **气象场景一句话**\ ：自动站给的文件有时前排一条注释当表头、有时没有。你若错把第一行数据当列名，相当于「把“北京、34.0”这一份观测记成了标题栏」，后面所有按站名取值都对着不存在的列，全是静默错——``print(df.head())``
   先看表长啥样，是这坑的解药。

--------------

.. _756-路径含中文空格--excel-中文乱码utf-8-sig不是报错但总翻车:

7.5.6 路径含中文/空格 & Excel 中文乱码（\ ``utf-8-sig``\ ）——不是报错但总翻车
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd
   p = "D:/Code/Vibe/QA/_sim/data/观测 数据.csv"
   # 该文件已用 utf-8-sig 写入
   print(pd.read_csv(p, encoding="utf-8-sig"))

   from io import StringIO
   # header=None + names 处理无表头
   df = pd.read_csv(StringIO("上海,32.0\n北京,34.0\n"), header=None, names=["站名","气温"])
   print(df)

.. code:: text

      站名    气温
   0  兰州  5.1
   1  西安  8.2
      站名    气温
   0  上海  32.0
   1  北京  34.0

**原因**\ ：Windows 上中文路径、中文/括号空格一般 pandas+Path
能读，但\ **保险起见**\ 用 ``pathlib``
或原样引号包裹；真正常翻车的是「写文件没带 ``utf-8-sig`` → Excel
打开中文表头变乱码」。\ ``utf-8-sig`` 自带头 BOM，是 Excel
的中文「亲儿子」编码。

**解决办法**\ ：

- ``to_csv(..., encoding="utf-8-sig")``\ ：正文导出固定写法；
- 存活中文表头：读 ``encoding="utf-8-sig"``\ ；
- 路径尽量英文目录，文件内中文用 ``utf-8-sig`` 写读闭环。

..

   **气象场景一句话**\ ：导出报告给老师/同学，Excel
   打开中文列名全乱码=灰常难看。\ ``.to_csv(path, encoding="utf-8-sig")``
   就像给 CSV 戴了个「我是 UTF-8」的防呆帽，Excel 一眼认出中文不用猜。

--------------

.. _76-dataframe--series-常见陷阱applygroupbycopyinplacedropsortrename:

7.6 DataFrame / Series 常见陷阱：apply、groupby、copy、inplace、drop、sort、rename
----------------------------------------------------------------------------------

.. _761-apply-忘写-axis1--想按行却按列静默:

7.6.1 ``apply`` 忘写 ``axis=1`` → 想按行却按列（静默！）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站名":["兰州","西安","成都","西宁"],
                      "气温":[5.1,8.2,12.0,9.5],
                      "湿度":[40.0,50.0,45.0,38.0]})
   print("axis=0 逐列:", df[["气温","湿度"]].apply(lambda c: c.mean(), axis=0))
   print("axis=1 逐行:", round(df[["气温","湿度"]].apply(lambda r: r.mean(), axis=1),2))
   print("--- 想按行, 却忘写 axis=1, 默认按列(错!) ---")
   print(df[["气温","湿度"]].apply(lambda r: r.mean()))   # 静默错算: 仍是每列均值

.. code:: text

   axis=0 逐列(每列一个数):
   气温     8.70
   湿度    43.25
   dtype: float64
   axis=1 逐行(每行一个数):
   0    22.55
   1    29.10
   2    28.50
   3    23.75
   dtype: float64
   --- 想按行, 却忘写 axis=1, 默认按列(错!) ---
   气温     8.70
   湿度    43.25
   dtype: float64

**高亮关键词联想**\ ：输出 ``0,1,2,3`` 四个值 = 逐行算对了；输出
``气温/湿度`` 两个值 =
逐列算。\ **没有报错**\ ，只是结果形状和含义错了。

**原因**\ ：\ ``df.apply(func)`` 默认
``axis=0``\ ，把\ **每一列**\ 当函数输入；想按行（把每一行当输入，得到每行的
1 个数）须
``axis=1``\ 。忘记写后，气象里「逐站算日较差」会莫名变成「跨要素算成一堆标量」。

**解决办法**\ ：想逐行→\ ``axis=1``\ ；想逐列→\ ``axis=0``\ （默认）。与正文
7.5.2 的 ``transform`` 搭配：想「组内均值广播回每行」用 ``transform``
而非 ``apply``\ 。写函数前先想清楚是「列是单位」还是「行是单位」。

   **气象场景一句话**\ ：\ ``apply`` 像「按什么切一刀再加工」。axis=0
   是竖着切（把每列切出来）、axis=1
   是横着切（把每行切出来）。你想逐站算个日较差（每行一个站），却用默认竖切，把几个要素的均值混到一起——形状对、含义错，最阴险的静默坑之一。

--------------

.. _762-groupby-后分组键成了索引忘-reset_index-导致-keyerror报错:

7.6.2 groupby 后分组键成了索引，忘 ``reset_index`` 导致 ``KeyError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站名":["兰州","西安","成都","西宁"],"气温":[5.1,8.2,12.0,9.5]})
   g = df.groupby("站名")["气温"].mean()         # 默认返回: 站名成为索引
   print(g)
   print("--- 后续想按站名当普通列查 ---")
   print(g["站名"])

.. code:: text

   站名
   兰州    5.1
   西安    8.2
   成都    12.0
   西宁    9.5
   Name: 气温, dtype: float64
   Traceback (most recent call last):
     ...
   KeyError: '站名'

**高亮关键词联想**\ ：\ ``KeyError: '站名'`` 出现在 groupby
之后——因为分组键 ``站名``
已经从「列」变成了结果的\ **索引**\ ，\ ``g["站名"]`` 想当列取自然没有。

**原因**\ ：\ ``groupby(...).agg/mean(...)``
默认把分组键放进索引（MultiIndex/Index），不是普通列。正文 7.5.1
明确提示：后续还想按「站名」筛选/当列，必须 ``reset_index()`` 或
``as_index=False``\ 。

**解决办法**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站站"...})  # 见上
   print(df.groupby("站名")["气温"].mean().reset_index())   # 站名还原成列
   # 或
   print(df.groupby("站名", as_index=False)["气温"].mean())

.. code:: text

     站名   气温
   0  兰州   5.1
   1  西安   8.2
   2  成都  12.0
   3  西宁   9.5

..

   **气象场景一句话**\ ：.groupby
   像把全国站点按省分了筐，返回的账本「省名」成了表头（索引）而不是普通一列。你想接着当普通列用省名，得
   ``reset_index()`` 把它从「表头」放回「单元格」，否则查 ``['站名']``
   就是 ``KeyError``\ 。

--------------

.. _763-链式赋值-df条件列值--settingwithcopywarning2x--chainedassignmenterror3x:

7.6.3 链式赋值 ``df[条件][列]=值`` → ``SettingWithCopyWarning``\ （2.x） / ``ChainedAssignmentError``\ （3.x）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出（pandas 3.x，弹了错误级提示但仍继续）**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站名":["兰州","西安","成都"],"气温":[5.1,8.2,12.0]})
   df[df["气温"]>8]["湿度"] = 60.0        # 链式赋值, 改的是副本
   print(df)

.. code:: text

   <你脚本路径>/t24_settingwithcopy.py:5: ChainedAssignmentError: A value is being set on a copy
   ... (链式赋值, 改的是临时副本; 由于 Copy-on-Write 永远无法更新原表)
   Try using '.loc[row_indexer, col_indexer] = value' instead ...
     df[df["气温"]>8]["湿度"] = 60.0
      站名    气温
   0  兰州   5.1
   1  西安   8.2
   2  成都  12.0

**版本说明**\ ：pandas 2.x 是
``SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame.``\ （警告，不中断）；pandas
3.x 升级为 ``ChainedAssignmentError``\ （字面是 Error 但本例在 3.0
下仍继续执行并打印了 df）。共同本质：\ **``df[A][B]=x``
是链式赋值，改的是中间对象（view/副本），原表不更新**——你辛苦加的列根本没写进去。

**高亮关键词联想**\ ：\ ``SettingWithCopy`` /
``ChainedAssignment``——「链式赋值」「改在了副本上」。这是 Pandas
初学者第一高发告警。

**原因**\ ：\ ``df[条件]`` 返回子集，再 ``[列]=值``
是对该子集赋值；Pandas
无法确定这子集是视图还是副本，于是打旗警告你可能白改了别人。

**解决办法**\ （正文 7.10 心法 2 与最佳实践）：

- 用 ``.loc`` 单步赋值：\ ``df.loc[df["气温"]>8, "湿度"] = 60.0``\ ；
- 或先 ``.copy()``\ ：\ ``sub = df[df["气温"]>8].copy()`` 再改
  sub（不再打扰原表，也无警告）；
- 最简单：整列赋值 ``df["新列"] = 计算表达式``\ ，一次到位。

..

   **气象场景一句话**\ ：\ ``df[高温日][某列]=值``
   就像在复印件上批改，原件一字未动还打小报告(Python:
   你可能在改副本)。Pandas 3.x 直接升级成 ``ChainedAssignmentError``
   呵斥你，逼你改用
   ``.loc[条件,列]``——确实，单步骤赋值比复印件靠谱一百倍。

--------------

.. _764-drop-的默认-axis0-删行删列要-dropcolumns--不然-keyerror报错:

7.6.4 ``drop`` 的默认 ``axis=0`` 删行，删列要 ``drop(columns=...)`` —— 不然 KeyError（报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：想删列却写 ``df.drop("站名")``\ ，Pandas 按
axis=0（删行）去找行标签 ``站名``\ ，找不到报 ``KeyError``\ 。

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站名":["兰州","西安","成都"],"气温":[5.1,8.2,12.0]})
   print(df.drop("站名"))        # 误把列名当行删

.. code:: text

   Traceback (most recent call last):
     ...
   KeyError: "['站名'] not found in axis"

**高亮关键词联想**\ ：\ ``"['站名'] not found in axis"``——**在 axis
里没找到 ``站名``**\ 。axis 默认 0
查的是行索引（站名所在的是列），列名不在行索引里自然「not found in
axis」。

**原因**\ ：\ ``df.drop(标签)`` 默认 ``axis=0``\ （删行）；删列必须
``axis=1`` 或 ``drop(columns=标签)``\ 。正文
7.9/Ppt「删除行或列」都强调：不指定轴，默认按行。

**解决办法**\ ：

.. code:: python

   df.drop("站名", axis=1)        # 删列
   df.drop(columns=["站名"])      # 删列(更可读)
   df.drop(0)                     # 删第 0 行(axis=0)

再叠加 ``inplace``\ ：\ ``drop`` 默认返回新对象，想原地改
``inplace=True`` 或不 inplace 就赋值。

   **气象场景一句话**\ ：你想删掉报表里的「站名」这一列，却忘了指方向，Pandas
   以为你要删一行叫 ``站名`` 的记录——结果在行名册里翻遍没有，报
   ``not found in axis``\ 。删列喊
   ``axe=1``/``columns=``\ ，跟点名册的方向对清楚。

--------------

.. _765-sort_values-排序后-index-没重置--行序号错乱静默:

7.6.5 ``sort_values`` 排序后 index 没重置 → 行序号错乱（静默！）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站名":["兰州","西安","成都","西宁"],"气温":[5.1,12.0,8.2,9.5]})
   s = df.sort_values("气温", ascending=False)      # 降序
   print("s.iloc[0] =", s.iloc[0].to_dict())
   print("s 的 index =", list(s.index), " (没重置!)")
   s2 = df.sort_values("气温", ascending=False).reset_index(drop=True)
   print("reset 后 index =", list(s2.index))

.. code:: text

   s.iloc[0] = {'站名': '西安', '气温': 12.0}
   s 的 index = [1, 3, 2, 0]  (没重置!)
   reset 后 index = [0, 1, 2, 3]

**高亮关键词联想**\ ：\ ``s.index = [1,3,2,0]``——排序后行是新的顺序（西安=原第1行排最前），但索引仍保留原行号
``1,3,2,0``\ 。若后续 ``.iloc[0]``\ （位置）取对了是西安，用
``.loc[0]``\ （标签）取到的却是原来的第 0 行。

**原因**\ ：\ ``sort_values``
默认\ **保留原始索引**\ （原行号），行标签和当前排列错位。这本身不报错，但「排好序后拿旧
index 去对齐别的表 / ``loc`` 取值」就会错位（静默污染）。

**解决办法**\ ：气象里排序后通常要干净的连续行号 →
``df.sort_values(...).reset_index(drop=True)``\ （正文最佳实践正是
``df = df.sort_values("date").reset_index(drop=True)``\ ）。若只想改变顺序不动结果，也用这招收尾。

   **气象场景一句话**\ ：按气温把站点重排后，每站还挂着自己的老牌号（原行号）。你想「取最热那行」，用位置
   ``iloc[0]`` 对，用标签 ``loc[0]``
   却拎出个无关行——就像重排队列后大家忘换号牌，号码对不上座位。\ ``reset_index``
   = 重新发号。

--------------

.. _766-rename--sort_values--cut-等返回新对象忘赋值--白做静默:

7.6.6 ``rename`` / ``sort_values`` / ``cut`` 等返回新对象，忘赋值 = 白做（静默！）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站名":["兰州","西安","成都"]})
   r1 = df.rename(columns={"站名":"站点"})    # rename 返回新对象
   print("rename 后原df列没变:", list(df.columns))
   print("新对象列:", list(r1.columns))

.. code:: text

   rename 后原df列没变: ['站名']
   新对象列: ['站点']

**高亮关键词联想**\ ：\ ``['站名']`` 原样未变——``rename``
没改原表。若你看完 ``r1`` 却继续用 ``df``\ ，名字等于白改。

**原因**\ ：\ ``rename/sort_values/drop/copy/groupby 结果``
默认都是\ **返回新对象、不原地改**\ （除非
``inplace=True``\ ）。初学常犯「\ ``df.rename(...)`` 一行跑完转头还在 df
上找新列」。

**解决办法**\ ：要么接收返回值 ``df = df.rename(...)``\ ，要么明确
``inplace=True``\ （但 inplace 见 7.6.7
也有自己的坑）。统一习惯：\ **Pandas
操作大多返回新对象，想保存就赋值给变量**\ 。

   **气象场景一句话**\ ：\ ``df.rename``
   像「下发新站名牌，换的是复印件，原件不动」——你需把复印件拿回来当新原件（\ ``df = df.rename(...)``\ ），否则第二天看原表还是旧名字，白忙一场。这不报错，只在你「咦名字怎么没变」时才察觉。

--------------

.. _767-inplacetrue-的连环坑返回-none子集链式多数是安静翻车:

7.6.7 ``inplace=True`` 的连环坑：返回 None、子集/链式（多数是安静翻车）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：\ ``inplace=True`` 的方法\ **返回
None**\ （只原地改、没有返回值）；配合「筛选子集」「链式取值」时还不一定作用到原对象（见
7.2.4 t08）。把它当常规返回值接住，拿到的是 ``None``\ （黑盒）：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"气温":[5.1,8.2,12.0]})
   df3 = df.drop(0, inplace=True)         # inplace 返回 None!
   print("df3 =", df3)
   print("df 在 drop(0, inplace=True) 后:")
   print(df)
   df4 = pd.DataFrame({"气温":[5.1,8.2,12.0]}).drop(0)   # 非 inplace 接住返回值
   print("非 inplace 接住返回值 df4:")
   print(df4)

.. code:: text

   df3 = None
   df 在 drop(0, inplace=True) 后:
        气温
   1   8.2
   2  12.0
   非 inplace 接住返回值 df4:
        气温
   1   8.2
   2  12.0

**高亮关键词联想**\ ：\ ``df3 = None``——``inplace=True`` 的方法\ **返回
None**\ （没有返回值，只原地改）。把它当常规返回值用，拿到的是
``None``\ 。

**原因**\ ：\ ``inplace=True`` 的含义是「就地修改并返回
None」；子集/视图上用 inplace 又不一定作用到原对象（7.2.4/7.6.3
的副本坑）。两者叠加，初学者最易翻车。

**解决办法**\ ：气象数据处理\ **优先「返回新对象 + 重新赋值」**\ （正文
7.4 note
的无坑姿势）：\ ``df = df.drop(0)``\ 、\ ``df = df.sort_values(...).reset_index(drop=True)``\ 。仅在确认操作目标就是原对象本身时才用
``inplace=True``\ ，并\ **不要靠它的返回值**\ 。一行原则：\ **返回新表就接住赋值，inplace=True
就忘掉返回值**\ 。

   **气象场景一句话**\ ：\ ``inplace=True``
   像「直接把原始观测本改掉」，快捷但危险——改错了没备份，而且它不给你回执（返回
   None）。气象数据宝贵，先留原件副本、用「返回新表再赋值」的稳妥路线，比
   llsync 到真副本。

--------------

.. _77-布尔索引条件组合的括号与符号:

7.7 布尔索引：条件组合的括号与符号
----------------------------------

.. _771-多条件用-andor而非--valueerror报错:

7.7.1 多条件用 ``and``/``or``\ （而非 ``&``/``|``\ ）→ ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"气温":[5.1,8.2,12.0],"湿度":[40,50,45]})
   print(df[df["气温"]>8 and df["湿度"]<50])    # 用了 Python 关键字 and

.. code:: text

   Traceback (most recent call last):
     ...
   ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().

**高亮关键词联想**\ ：\ ``The truth value of a Series is ambiguous``——「一个布尔
Series 的真值是多义的」。\ ``df["气温"]>8`` 是一串 True/False
数组，Python 的 ``and`` 需要单个 True/False，喂给一串它无法判真假。

**原因**\ ：Python 的 ``and``/``or`` 只能用于标量布尔；数组（boolean
Series）要逐个元素做逻辑，用\ **位运算符
``&``\ （且）\ ``|``\ （或）\ ``~``\ （非）**\ ，并且\ **每个条件都要套圆括号**\ （否则
``&`` 优先级比比较低会语法错/语义错）。正文 7.3.3 warning
原句就是这个坑。

**解决办法**\ ：

.. code:: python

   hot_dry = df[(df["气温"]>8) & (df["湿度"]<50)]     # 每个条件加括号, 用 &
   print(hot_dry)
   # 或读起来更像 SQL:
   print(df.query("气温 > 8 and 湿度 < 50"))

.. code:: text

      气温  湿度
   2  12.0  45

**补充**\ ：\ ``&``/``|`` 用错优先级（忘加括号）时常见
``ValueError``/``TypeError``\ ；气象里「干热天气 = 气温>30 且
湿度<60」正是正文手把手教的写法。

   **气象场景一句话**\ ：\ ``and``
   想同时满足「气温>30」和「湿度<60」，但前者是 8 站的 8
   个布尔值，Python 的 ``and``
   只收单个真假——好比问「这八站是不是都干热？」它没法一句答。交给
   ``&``\ （逐站逐个“且”）并每条件加括号，才有意义。

--------------

.. _772-isin-过滤某一批值多点筛选非报错但易撞空:

7.7.2 ``isin`` 过滤某一批值（多点筛选，非报错但易撞空）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ （正确示范）：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站名":["兰州","西安","成都","西宁"],
                      "气温":[5.1,8.2,12.0,9.5],"湿度":[40,50,45,38]})
   print(df[df["站名"].isin(["兰州","成都"])])
   print("高温+低湿:", df[(df["气温"]>8) & (df["湿度"]<50)])

.. code:: text

      站名   气温  湿度
   0  兰州   5.1  40
   2  成都  12.0  45
      站名   气温  湿度
   2  成都  12.0  45

**高亮关键词联想**\ ：\ ``isin([...])``\ 「值是否在列表里」是筛选一批站点/月份的利器（正文
7.3.3 与 7.9 的
``df.index.month.isin([6,7,8])``\ ）。常见坑：列表里站号用字符串
``"58367"``\ ，而数据列被读成 ``int``\ ，则匹配全空（静默）。

**解决办法**\ ：\ ``isin``
要求\ **比对双方类型一致**\ （字符串对字符串、int 对 int）。正文 7.2 读
CSV 用 ``dtype={"站号": str}`` 把区站号存成字符串，正是为了和
``"58367"`` 这类字符串 isin 匹配；若数据列是 int，列表也用 int。

   **气象场景一句话**\ ：\ ``isin``
   像「只挑兰州、成都两个站出场」。但若列表写
   ``"58367"``\ （字符串）而表里站号是数字
   ``58367``\ ，比对类型不匹配悄悄全 False——筛出来的报表空得诡异，先
   ``print(df.dtypes)`` 再对 isin 的列表类型。

--------------

.. _78-merge--concat拼表的对键方向与连接类型:

7.8 merge / concat：拼表的对键、方向与连接类型
----------------------------------------------

.. _781-merge-的-on-键不存在--keyerror报错:

7.8.1 ``merge`` 的 ``on=`` 键不存在 → ``KeyError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   obs  = pd.DataFrame({"站号":["58367","54511","57494"],"气温":[25,22,28]})
   meta = pd.DataFrame({"站号":["58367","54511"],"海拔":[4.5,31.3]})
   print(pd.merge(obs, meta, on="站名", how="inner"))   # 两张表都没有 '站名' 列

.. code:: text

   Traceback (most recent call last):
     ...
   KeyError: '站名'

**高亮关键词联想**\ ：\ ``KeyError: '站名'``——``on``
指定的连接键在两表里都不存在。

**原因**\ ：\ ``pd.merge(左表, 右表, on=键, how=...)``
要求键是两表共有（或 ``left_on``/``right_on`` 分别指定）。键名拼错 /
两表键名不同却只用 ``on``\ ，都报 KeyError。

**解决办法**\ ：先 ``print(obs.columns); print(meta.columns)``
找共同键（正文 7.8 用「站号」连接逐日观测和站点元数据）。键名不同时用
``left_on="站号", right_on="站点ID"``\ （否则自动加列）。大小写、中文符号都要对。

   **气象场景一句话**\ ：你要把「逐日观测」和「站点元数据」按站号拼起来，却让
   mergftp 按 ``站名`` 做键——两张表里压根没有这列，自然是
   ``KeyError``\ 。拼接前先亮出两表 ``columns`` 找那个「共同身份证号」。

--------------

.. _782-concat-方向错axis1-并排但索引对不齐--满屏-nan静默:

7.8.2 ``concat`` 方向错：axis=1 并排但索引对不齐 → 满屏 NaN（静默！）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd
   a = pd.DataFrame({"站号":["58367","54511"],"气温":[25,22]})
   b = pd.DataFrame({"站号":["57494"],"气温":[28]})
   c = pd.concat([a,b], axis=1)      # 想并排, 但索引没对齐
   print(c)
   print("--- 上下拼接(正确方向) ---")
   print(pd.concat([a,b], axis=0, ignore_index=True))

.. code:: text

         站号    气温     站号    气温
   0  58367  25  57494  28.0
   1  54511  22    NaN   NaN
   --- 上下拼接(正确方向) ---
         站号  气温
   0  58367  25
   1  54511  22
   2  57494  28

**高亮关键词联想**\ ：并排结果里 ``NaN`` 一大片、列名还重复——因为
``concat(axis=1)``
按\ **索引对齐**\ 并排，若两组记录的行索引不是「同一套」，缺的位置补
NaN。\ **这多半不是你想要的「拼观测」，想竖向追加应 axis=0。**

**原因**\ ：\ ``pd.concat`` 的 ``axis=0``
是\ **上下（竖向追加行）**\ ，\ ``axis=1``
是\ **左右（横向对齐列）**\ 。数组对齐时默认
``outer``\ （并集），对不上的补 NaN。\ ``concat`` 的 axis 语义和 numpy
相反应用场不同：气象里「追加更多时次」用 axis=0。

**解决办法**\ ：

- 追加记录 →
  ``pd.concat([a,b], axis=0, ignore_index=True)``\ （ignore_index
  重新编号，避免 index 打架）；
- 真正想按站号横向对齐多列数据 → 用
  ``merge``/``join``\ （按键接），而不是 concat axis=1；
- axis=1 且希望按共同键对齐 →
  ``pd.concat([a.set_index("站号"), b.set_index("站号")], axis=1)``\ 。

..

   **气象场景一句话**\ ：\ ``concat`` 的 axis=0
   是把「8月14日、8月15日」两天观测\ **连带子目录地竖着叠**\ （追加行）；axis=1
   是横着拼列。你若拿索引没对齐的两批站点并排，缺少那批的行就会补
   ``NaN`` 空洞——像把站号对不齐的两张观测表硬贴在一起，贴缝全是空档。

--------------

.. _783-merge-用错-howinnerouterleft-行数缺测与预期不符静默:

7.8.3 ``merge`` 用错 how（inner/outer/left）→ 行数/缺测与预期不符（静默）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd
   obs  = pd.DataFrame({"站号":["58367","54511","57494"],"气温":[25,22,28]})
   meta = pd.DataFrame({"站号":["58367","54511","99999"],"海拔":[4.5,31.3,100.0]})
   print("inner :", pd.merge(obs, meta, on="站号", how="inner")["站号"].tolist())
   print("outer 整表:")
   print(pd.merge(obs, meta, on="站号", how="outer"))
   print("left  整表:")
   print(pd.merge(obs, meta, on="站号", how="left"))

.. code:: text

   inner : ['58367', '54511']
   outer 整表:
         站号    气温     海拔
   0  54511  22.0   31.3
   1  57494  28.0    NaN
   2  58367  25.0    4.5
   3  99999   NaN  100.0
   left  整表:
         站号  气温    海拔
   0  58367  25   4.5
   1  54511  22  31.3
   2  57494  28   NaN

**高亮关键词联想**\ ：同是「按站号拼」，\ ``inner`` 只剩 2
站（两表都有）、\ ``outer`` 给 4 站（并集缺的一侧 NaN）、\ ``left``
保留左表 3 站元数据缺的站填 ``NaN``\ 。行数和 NaN 完全由 ``how`` 决定。

**原因**\ ：\ ``how`` 就是 SQL 的 join 类型（正文 7.8 列表：inner 交集 /
left / right / outer 并集）。初学默认
inner，把只在一个表里的站（元数据里多的
``99999``\ ）悄悄丢掉，气象里就是「有降水记录却查不到这个站」。

**解决办法**\ ：先想清楚「保留哪些行」——想保留观测全量配已知元数据用
``left``\ ；只保留两边都有的站用 ``inner``\ 。\ ``:merge`` 后
``print(结果.shape, 结果.isna().sum())`` 检查是否掉站/多 NaN。常用
``how="left"`` 保留观测全量（正文 7.9 正是 ``left``\ ）。

   **气象场景一句话**\ ：\ ``inner``
   像「只留下两本名册都登记过的站」；\ ``left``
   像「以观测名册为准，元数据查不到的站先空着（NaN）」。做「高温热浪汇报」必须保留全部观测站，所以用
   ``left``——用 inner 会默默删掉几个有记录的站，报表少站却不知情。

--------------

.. _79-气象专属静默错误最容易让你程序绿灯科学全错的一批:

7.9 气象专属静默错误：最容易让你「程序绿灯、科学全错」的一批
------------------------------------------------------------

   这一节对应第 7
   章正文与最佳实践反复强调的「雷区」。每一条都实测过，\ **没有报错、只有悄悄错掉的结果**——这才是气象分析最贵的学习。

.. _791-时间没排序就-ffill前向填充-缺测填错方向静默:

7.9.1 时间没排序就 ``ffill``\ （前向填充）→ 缺测填错方向（静默！）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"date":pd.to_datetime(["2026-08-14","2026-08-12","2026-08-13","2026-08-15"]),
                      "气温":[22.0, float("nan"), float("nan"), 25.0]}).set_index("date")
   print("未排序数据:")
   print(df)
   print("未排序直接 ffill:")
   print(df["气温"].ffill())
   df2 = df.sort_index()
   print("先排序再 ffill:")
   print(df2["气温"].ffill())

.. code:: text

   未排序数据:
                 气温
   date
   2026-08-14  22.0
   2026-08-12   NaN
   2026-08-13   NaN
   2026-08-15  25.0
   未排序直接 ffill:
   date
   2026-08-14    22.0
   2026-08-12    22.0
   2026-08-13    22.0
   2026-08-15    25.0
   先排序再 ffill:
   date
   2026-08-12     NaN
   2026-08-13     NaN
   2026-08-14    22.0
   2026-08-15    25.0
   Name: 气温, dtype: float64

**高亮关键词联想**\ ：未排序时 ``2026-08-12、13``\ （记录的 NaN）被
``ffill`` 用\ **其上一行的 22.0** 填上了——但按时间看 8-12 明明在 8-14
之前，用「往后的值补前面的缺」完全背离前向填充本意；真正按时间排序后，8-12、13
前面没有有效值，正确地保持 NaN。

**原因**\ ：\ ``ffill``
是「用上一行未缺测的值往下填」，\ **它认的是行先后，不是时间先后**\ 。数据未按时间排序时，「上一行」不一定是「上一个时刻」，填充方向就错。

**解决办法**\ ：时间序列处理前\ **务必
``sort_index()``/``sort_values("date")``**\ （正文最佳实践第 4
条「处理器前先排序」）。同时，pandas 3.x 里 ``fillna(method="ffill")``
已移除，直接改用 ``.ffill()`` / ``.bfill()``\ 。

   **气象场景一句话**\ ：\ ``ffill``
   像「缺测就借用上一时次的观测」。可表格没按时间排队，8 月 14
   的记录正好排 8 月 12 前面，缺着缺着把「未来 14 日的值」硬借给「过去
   12 日」——时序全倒灌。先排队（sort）再借，才认「上一个时刻」。

--------------

.. _792-只按-dtmonth-分组--不同年份同月被并成一组静默跨年合并:

7.9.2 只按 ``.dt.month`` 分组 → 不同年份同月被并成一组（静默！跨年合并）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   import pandas as pd, numpy as np
   df = pd.DataFrame({"date":pd.to_datetime(["2024-01-15","2024-02-10","2025-01-05","2025-01-20"]),
                      "气温":[1.0,2.0,0.0,3.0]})
   w  = df.groupby(df["date"].dt.month)["气温"].mean()   # 只按月份数字
   print("错误: 只按 dt.month -> 1月均值 =", round(w[1],2), "(两冬叠一起)")
   ok = df.groupby(pd.Grouper(key="date", freq="ME"))["气温"].mean()   # 按完整年-月
   print("正确: pd.Grouper(freq=ME):")
   print(ok)

.. code:: text

   错误: 只按 dt.month -> 1月均值 = 1.33 (两冬叠一起)
   正确: pd.Grouper(freq=ME):
   date
   2024-01-31    1.0
   2024-02-29    2.0
   2025-01-31    1.5
   Name: 气温, dtype: float64

**高亮关键词联想**\ ：错误写法把 ``2024-01`` 和 ``2025-01``
并成一组，均温 ``1.33``——两个不同年份的 1 月被当成了同一个「1
月」。正确写法文件名里清清楚楚分出 ``2024-01-31`` 和 ``2025-01-31``
两组。

**原因**\ ：\ ``df["date"].dt.month`` 只取「月份数字
1~12」，丢掉了年份，于是 2024 和 2025 的 1 月共享标签
1。这正是正文最佳实践反复强调的「跨年按月分组必须用
``pd.Grouper(key="date", freq="M"/"ME")``\ ，禁止只用 dt.month」。

**解决办法**\ ：

.. code:: python

   df.groupby(pd.Grouper(key="date", freq="ME"))["气温"].mean()   # 按完整 年-月
   # 老写法 freq="M" 在 pandas 3.x 已报错(见 7.9.5), 请用 "ME"

若确实只想要「某月的气候均值」不想分年，也要在分组里带上 ``year``
维度再单独平均，别让 dt.month 一把抓。

   **气象场景一句话**\ ：气候统计说「1 月平均气温」，前提是「2024 年 1
   月」和「2025 年 1 月」分开算、再谈统计规律。\ ``.dt.month``
   只留月号，等于把两个冬天叠成同一个冬天，均温被「两冬拼一冬」算歪——这正是
   7.9.2 无报错却全错的典型。

--------------

.. _793-时区-naive--aware-混用--typeerror-或静默错:

7.9.3 时区 naive / aware 混用 → ``TypeError`` 或静默错
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   naive = pd.Timestamp("2026-08-14 12:00")                       # 无时区
   aware = pd.Timestamp("2026-08-14 12:00", tz="Asia/Shanghai")  # 有时区
   print(aware - naive)

.. code:: text

   Traceback (most recent call last):
     ...
   TypeError: Cannot subtract tz-naive and tz-aware datetime-like objects.

**高亮关键词联想**\ ：\ ``Cannot subtract tz-naive and tz-aware``——不能直接减「无时区」和「有时区」的时间。时区字段不一致，Pandas
拒绝含糊相减。

**原因**\ ：\ ``naive``\ （naive，无时区信息）与
``aware``\ （aware，带时区）是两类时间，混算有歧义（同一时刻在
UTC/东八区含义不同），减法直接报错；若放在同一列整体比较也可能出
``TypeError``\ 。

**解决办法**\ ：

- 统一到底用哪个：\ ``aware.tz_convert(None)`` 丢掉时区当 naive，或用
  ``naive.tz_localize("Asia/Shanghai")`` 给 naive 安上时区；两表都 aware
  后各自 ``tz_convert`` 到同一时区再比较/减。
- 气象多用「本地时间」当 naive 处理，领取 ``.dt`` 时先确认来源。

..

   **气象场景一句话**\ ：一条观测写着「12:00」没带时区，另一条写着「北京时
   12:00」。两者相减，Pandas 没法说清「差的是哪 12
   点」——时区一份试卷两份标准答案，直接判错。先
   ``tz_localize``/``tz_convert`` 统一到同一时刻口径，才能算时间差。

--------------

.. _794-把字符型温度-astype-成数值撞上异常值业务必现-与-731-呼应:

7.9.4 把字符型温度 astype 成数值撞上异常值（业务必现）—— 与 7.3.1 呼应
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：合并多站 / openpyxl 读 Excel / 读 CSV
时，温度列可能有 ``""``\ 、\ ``"缺"``\ 、\ ``-`` 等，直接
``astype(float)`` 报错。若先 ``to_numeric(coerce)`` 则坏值变
NaN（静默但可后续统计）。

.. code:: python

   import pandas as pd
   t = pd.Series(["25.1","abc","27.7"])
   print(t.astype(float))

.. code:: text

   Traceback (most recent call last):
     ...
   ValueError: could not convert string to float: 'abc'

**高亮关键词联想**\ ：这句 ``could not convert string to float: 'abc'``
和 7.3.1
同句——列里字混入非数字。气象业务尤其常见：\ ``""``\ （空）、\ ``"缺测"``\ 、\ ``"-"``\ 、单位残留
``"25.1℃"``\ 。

**解决办法**\ ：

- 先清洗：\ ``to_numeric(errors="coerce")`` 转 NaN，再 ``isna().sum()``
  看有多少坏样本；
- 特殊字符：\ ``df["气温"] = df["气温"].str.replace("℃","")`` 再去
  ``to_numeric``\ ；
- 千分位逗号：国内外降水/气压常带 ``,``\ ，\ ``str.replace(",","")``\ 。
- 读 CSV 直接用 ``dtype``/``na_values`` 提前把这些哨兵声明为 NaN（正文
  7.2 的 ``na_values`` 数组）。

..

   **气象场景一句话**\ ：自动站/Excel 导出的温度，偶发夹一条 ``-`` 或
   ``"缺"``\ 。\ ``astype`` 直接噎，\ ``to_numeric(coerce)`` 变成 NaN
   让你看清「哪几条没测到」，再决定补还是剔——气象里「缺测可补、错值必查」，先识别哨兵再转数是基本功。

--------------

.. _795-老写法的报警报错升级resamplem--valueerrorfillnamethodffill--typeerror:

7.9.5 老写法的报警/报错升级：\ ``resample("M")`` → ``ValueError``\ ，\ ``fillna(method="ffill")`` → ``TypeError``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   s = pd.Series(pd.to_datetime(["2026-08-14","2026-08-15"]))
   df = pd.DataFrame({"观测时间":s,"气温":[30.0,31.0]}).set_index("观测时间")
   print("resample('ME') 正确:")
   print(df["气温"].resample("ME").mean())
   print("resample('M') 老写法:")
   print(df["气温"].resample("M").mean())

.. code:: text

   resample('ME') 正确:
   观测时间
   2026-08-31    30.5
   Freq: ME, Name: 气温, dtype: float64
   resample('M') 老写法:
   Traceback (most recent call last):
     ...
   ValueError: 'M' is no longer supported for offsets. Please use 'ME' instead.

.. code:: python

   s2 = pd.Series([1.0, float("nan")])
   s2.fillna(method="ffill")     # 3.x 已移除 method 参数

.. code:: text

   TypeError: NDFrame.fillna() got an unexpected keyword argument 'method'

**高亮关键词联想**\ ：\ ``'M' is no longer supported ... use 'ME'`` 与
``fillna() got an unexpected keyword argument 'method'``——两个都是\ **升级弃用的写法**\ ：位
``M`` → ``ME``\ ，\ ``fillna(method=)`` → 直接
``.ffill()``/``.bfill()``\ 。

**原因**\ ：pandas 2.x 里这些产生
``FutureWarning``\ （弃用提醒，仍能用）；pandas 3.x
收紧了直接\ **报错**\ （M 报 ValueError、method 报
TypeError）。正文已标注「新版本建议用 ME」，老师课上用的
``resample("ME")`` 正是新语法。

**解决办法**\ ：看到 ``is no longer supported`` / ``no longer`` /
``unexpected keyword``
字样，就该想到「版本语法定级了，去查该写法现版本换成啥」——``M``\ →\ ``ME``\ ，\ ``method="ffill"``\ →\ ``.ffill()``\ ，\ ``method="m"末日``\ →\ ``.bfill()``\ 。强烈建议全项目统一新写法，避免跨环境报错。

   **气象场景一句话**\ ：老版本「能跑但亮黄灯」的写法，新版直接「红灯叫停」——像旧版仪器给个提示、新版直接锁机。你拿到
   ``no longer supported`` 就明白：pandas 换语法了，把 ``M`` 换成
   ``ME``\ 、\ ``fillna(method=)`` 换成 ``.ffill()``\ ，跟上课保持一致。

--------------

.. _796-pivot-遇重复键--valueerror用-pivot_table报错正文-77-陷阱原句:

7.9.6 ``pivot`` 遇重复键 → ``ValueError``\ ，用 ``pivot_table``\ （报错，正文 7.7 陷阱原句）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import pandas as pd
   df = pd.DataFrame({"站名":["兰州","兰州","西安","西安"],
                      "月份":[7,7,8,8],"气温":[25.0,26.0,27.0,28.0]})
   print(df.pivot(index="站名", columns="月份", values="气温"))

.. code:: text

   Traceback (most recent call last):
     ...
   ValueError: Index contains duplicate entries, cannot reshape

**高亮关键词联想**\ ：\ ``Index contains duplicate entries, cannot reshape``——索引有重复条目没法重排。同一「站名×月份」出现了两条记录，\ ``pivot``
无法决定格子放哪个值，直接竖起 ``ValueError``\ 。

**原因**\ ：真实观测几乎必有重复（同一站同一月多天有记录），\ ``pivot``
要求 index×columns 组合唯一。

**解决办法**\ ：用 ``pivot_table``\ （正文 7.7 强调），并给聚合
``aggfunc``\ ：

.. code:: python

   p = df.pivot_table(index="站名", columns="月份", values="气温", aggfunc="mean")
   print(p)

``pivot_table`` 会自动用 ``aggfunc``\ （默认
mean）聚合重复格；\ ``aggfunc="sum"``
做月度累计时尤其常用。气象里透视表几乎总是 ``pivot_table``\ 。

   **气象场景一句话**\ ：\ ``pivot``
   想要「站名×月份」一格只装一个温度，可某站某月偏偏有好几天的观测——它无法决定塞哪天，直接报
   ``duplicate``\ 。\ ``pivot_table``
   像「同格先平均再装格」，才符合逐日观测转月表的气象语义。

--------------

.. _797-气象排查线索速答你的数据绿灯但不对时先问这几句:

7.9.7 气象「排查线索」速答：你的数据「绿灯但不对」时先问这几句
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

把本节（以及
7.2/7.6/7.7/7.8）的静默坑合成一张自查表——结果不对最可能卡在哪：

+-------------------------+-------------------------------------------------------------+
| 异常现象                | 最可能的原因 → 排查线索                                     |
+=========================+=============================================================+
| 平均值偏小得离谱        | 缺测被 ``fillna(0)`` 当 0（7.2.3）；先 ``isna().sum()`` 和  |
|                         | ``fillna`` 找「0℃ 冒充」                                    |
+-------------------------+-------------------------------------------------------------+
| 全线 NaN 或一片 nan     | ``skipna=False`` / 转 numpy 用 np.mean / NaN                |
|                         | 传染（7.2.1）；\ ``print`` 中间量                           |
+-------------------------+-------------------------------------------------------------+
| 高温日 / 条件筛选不对劲 | 温度列是字符串，字典序比较（7.3.3）；\ ``print(df.dtypes)`` |
+-------------------------+-------------------------------------------------------------+
| 按月统计跨年合并        | 只用 ``.dt.month`` 分组（7.9.2）；改                        |
|                         | ``pd.Grouper(freq="ME")``                                   |
+-------------------------+-------------------------------------------------------------+
| 缺测没填上 / 填错方向   | 数据未按时间排序就 ffill（7.9.1）；先 ``sort_index()``      |
+-------------------------+-------------------------------------------------------------+
| 时区加减报错            | naive/aware 混用（7.9.3）；\ ``tz_localize``/``tz_convert`` |
|                         | 统一                                                        |
+-------------------------+-------------------------------------------------------------+
| 排序后取错行            | ``sort_values`` 后 index                                    |
|                         | 没重置（7.6.5）；\ ``reset_index(drop=True)``               |
+-------------------------+-------------------------------------------------------------+
| 想按行算成按列          | ``apply`` 忘写 axis=1（7.6.1）；\ ``apply(..., axis=1)``    |
+-------------------------+-------------------------------------------------------------+
| 改了副本人均白改        | 链式赋值 / inplace on                                       |
|                         | 子集（7.6.3/7.2.4）；\ ``.loc[条件,列]=值`` 或 ``.copy()``  |
+-------------------------+-------------------------------------------------------------+
| 拼表后少站/多 NaN       | merge 的 how 选错（7.8.3）；想保全量用 ``left``             |
+-------------------------+-------------------------------------------------------------+

..

   **实战一句**\ ：面对任何「结果不对劲又没报错」的气象结果，先补两道
   ``print``\ ：\ ``print(df.dtypes)``\ （看温度/日期是不是字符串）、\ ``print(df.isna().sum())``\ （看缺测去向）。这两行能破掉本节八成静默坑——正如第
   6 章守门双式里说的「遇事不决先 dtype+isna」。

--------------

.. _710-本章高频速查表:

7.10 本章高频速查表
-------------------

+------------------------------------------------------------------------------+---------------+
| 记一记（关键词 → 原因）                                                      | 对应条目      |
+==============================================================================+===============+
| ``KeyError: 'xxx'`` → loc/df[] 键名不存在 / 列名错 / 把列名当行标签          | 7.1.1         |
+------------------------------------------------------------------------------+---------------+
| ``iloc`` 传字符串 → ``TypeError: non-integer key``\ ；\ ``iloc`` 越界 →      | 7.1.2 / 7.1.3 |
| ``IndexError``                                                               |               |
+------------------------------------------------------------------------------+---------------+
| single 列名 → Series，列表包住 → DataFrame                                   | 7.1.4         |
+------------------------------------------------------------------------------+---------------+
| Pandas 聚合默认\ **跳过** NaN（skipna=True）；转 numpy / ``skipna=False``    | 7.2.1         |
| 才传染                                                                       |               |
+------------------------------------------------------------------------------+---------------+
| ``NaN != NaN``\ ，筛缺测用 ``isna()``\ ；\ ``where``/``mask`` 精细替换       | 7.2.2         |
+------------------------------------------------------------------------------+---------------+
| 缺测 ≠ 0；\ ``fillna(0)`` 再 mean = 均值被拉低                               | 7.2.3         |
+------------------------------------------------------------------------------+---------------+
| 子集上 ``inplace`` 不生效 → 链式赋值警告/错误                                | 7.2.4 / 7.6.3 |
+------------------------------------------------------------------------------+---------------+
| ``could not convert string to float: 'xxx'`` → 字符串里有渣 → coerce 转 NaN  | 7.3.1 / 7.3.2 |
+------------------------------------------------------------------------------+---------------+
| 字符串温度字典序比较全错（2.x 静默 / 3.x 报 dtype=str）                      | 7.3.3         |
+------------------------------------------------------------------------------+---------------+
| ``Series.strftime`` → AttributeError → ``.dt.strftime`` / 先 to_datetime     | 7.4.1         |
+------------------------------------------------------------------------------+---------------+
| ``Timestamp + int`` → TypeError → ``+ pd.Timedelta / DateOffset``            | 7.4.2         |
+------------------------------------------------------------------------------+---------------+
| Timestamp 相减 → Timedelta（取 ``.days``\ ）                                 | 7.4.3         |
+------------------------------------------------------------------------------+---------------+
| ``strptime`` NameError → 先 import datetime 或直接用 ``pd.to_datetime``      | 7.4.4         |
+------------------------------------------------------------------------------+---------------+
| ``to_datetime(format=)`` 撞坏值 → ``format='mixed'`` 或 coerce               | 7.4.5         |
+------------------------------------------------------------------------------+---------------+
| ``FileNotFoundError`` → 路径错；\ ``UnicodeDecodeError`` → 编码错换          | 7.5.1 / 7.5.2 |
| gbk/utf-8-sig                                                                |               |
+------------------------------------------------------------------------------+---------------+
| ``ParserError: Expected N fields ... saw M`` → 分隔符/脏行                   | 7.5.3         |
+------------------------------------------------------------------------------+---------------+
| ``usecols`` 不符 → ``ValueError``\ ；无表头 → header=None+names              | 7.5.4 / 7.5.5 |
+------------------------------------------------------------------------------+---------------+
| 中文乱码 → 写 ``utf-8-sig`` 读 ``utf-8-sig``                                 | 7.5.6         |
+------------------------------------------------------------------------------+---------------+
| ``apply`` 忘写 axis=1 = 想按行按列（静默）                                   | 7.6.1         |
+------------------------------------------------------------------------------+---------------+
| groupby 忘 reset_index → 分组键成索引 → ``KeyError``                         | 7.6.2         |
+------------------------------------------------------------------------------+---------------+
| ``SettingWithCopyWarning``\ (2.x) / ``ChainedAssignmentError``\ (3.x) →      | 7.6.3         |
| 链式赋值改副本 → 用 ``.loc[条件,列]`` 或 ``.copy()``                         |               |
+------------------------------------------------------------------------------+---------------+
| ``drop("列名")`` 默认 axis=0 删行 → ``not found in axis`` →                  | 7.6.4         |
| ``drop(columns=)``                                                           |               |
+------------------------------------------------------------------------------+---------------+
| ``sort_values`` 不重置 index（静默）→ 排序后 ``reset_index(drop=True)``      | 7.6.5         |
+------------------------------------------------------------------------------+---------------+
| ``rename``/``drop`` 等返回新对象，忘赋值=白做                                | 7.6.6         |
+------------------------------------------------------------------------------+---------------+
| ``inplace=True`` 返回 None；子集/别名上 inplace 可能白改                     | 7.6.7         |
+------------------------------------------------------------------------------+---------------+
| ``and``/``or`` 组合条件 → ``ValueError: truth value ambiguous`` →            | 7.7.1         |
| ``&``/``|``\ +括号 / query                                                   |               |
+------------------------------------------------------------------------------+---------------+
| ``isin`` 类型不匹配 → 静默全 False                                           | 7.7.2         |
+------------------------------------------------------------------------------+---------------+
| ``merge on=``\ 键不存在 → KeyError；键名不同用 left_on/right_on              | 7.8.1         |
+------------------------------------------------------------------------------+---------------+
| ``concat`` axis 方向错 → 索引不齐满屏 NaN                                    | 7.8.2         |
+------------------------------------------------------------------------------+---------------+
| merge 的 how（inner/left/outer）决定行数与 NaN                               | 7.8.3         |
+------------------------------------------------------------------------------+---------------+
| 时间未排序 ffill → 填充方向错                                                | 7.9.1         |
+------------------------------------------------------------------------------+---------------+
| 只按 dt.month → 跨年合并                                                     | 7.9.2         |
+------------------------------------------------------------------------------+---------------+
| naive/aware 混用 → TypeError，先统一时区                                     | 7.9.3         |
+------------------------------------------------------------------------------+---------------+
| 字符温度 astype → could not convert → coerce 后看 isna                       | 7.9.4         |
+------------------------------------------------------------------------------+---------------+
| ``M``\ →\ ``ME``\ 、\ ``fillna(method=)``\ →\ ``.ffill()``\ ：新版本才不报错 | 7.9.5         |
+------------------------------------------------------------------------------+---------------+
| ``pivot`` 重复键 → ValueError → 用 ``pivot_table(aggfunc=...)``              | 7.9.6         |
+------------------------------------------------------------------------------+---------------+
| 结果绿但错 → 先 ``print(df.dtypes)`` 和 ``print(df.isna().sum())``           | 7.9.7         |
+------------------------------------------------------------------------------+---------------+

..

   **收尾口诀（气象风）**\ ：\ ``KeyError``\ 查列名/标签、\ ``TypeError``\ 查类型/参数、\ ``ValueError``\ 查值非法——Pandas
   报错三兄弟；而\ **真正要命的静默四害**\ 是：\ **NaN
   传染/缺测当0、字符串字典序比较、跨年一月并组、时间未排序就f填充**\ 。先
   ``dtypes`` 再 ``isna``\ ，两条守门咒念完，Pandas 的雷池你已趟过大半。
