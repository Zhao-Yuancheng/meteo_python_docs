Xarray 气象数据处理（二）Q&A
==================================

   **章节定位**\ ：第 8 章（模块二）· 对应用户指南
   ``user_guide/data/xarray.rst`` 与配套幻灯片 08。
   **主题**\ ：带标签的多维格点数据（DataArray /
   Dataset）、\ ``open_dataset`` 读取 NetCDF / GRIB、按坐标 /
   按位置索引（\ ``sel`` / ``isel``\ ）、纬度加权区域平均、\ ``groupby``
   时间分组、\ ``resample`` 重采样、\ ``to_netcdf`` 保存。一句话：\ **把
   Pandas
   的「二维表」升级成「多维格点场」，用维度名和坐标值取数，而不是数第几个冒号**\ 。
   **通用排错方法论**\ ：见
   :doc:`00-通用排错指南 </qa/basics/00-通用排错指南>`\ （0.1 节「报错 / 警告 /
   静默错值」三分法、0.4 节「排查七招」、0.5 节「静默污染」先读）。
   **校正说明**\ ：本文所有 ``Traceback / Warning``
   均在本机真实运行验证、原文照录；其中「缺引擎打不开文件」的案例，是刻意在\ **未安装对应后端**\ （如不装
   cfgrib、zarr）的环境中复现的，为了让报错原原本本出现——你在缺库的机器上会看到一模一样的提示。错误消息在
   xarray 2025.x 各小版本基本稳定，个别措辞差异已标注。

--------------

.. _80-本章报错警告速查总表:

8.0 本章报错/警告速查总表
-------------------------

第 8 章的高频问题，先按「报错(中断) / 警告(不中断) /
静默错值」三分类摊开，方便快速锚定。

+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| 英文关键词                                                                                      | 类型      | 报错 / 现象一句话              |
+=================================================================================================+===========+================================+
| ``FileNotFoundError: No such file or directory: '...no_such_file.nc'``                          | 报错      | 打开的文件路径不存在           |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``ModuleNotFoundError: No module named 'cfgrib'``                                               | 报错      | 读了 ``.grib`` 却没有 cfgrib   |
|                                                                                                 |           | 引擎                           |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``ValueError: unrecognized engine 'cfgrib' ... must be one of your download engines``           | 报错      | ``engine=`` 指定的引擎没装 /   |
|                                                                                                 |           | 名字写错                       |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``ValueError: did not find a match in any of xarray's currently installed IO backends``         | 报错      | 扩展名无法匹配任何已装引擎（如 |
|                                                                                                 |           | ``.grib`` 但没 cfgrib）        |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``TypeError: Error: ... is not a valid NetCDF 3 file`` /                                        | 报错      | 文件不是合法                   |
| ``OSError: [Errno -51] NetCDF: Unknown file format``                                            |           | NetCDF（签名损坏）             |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``ImportError: The zarr package is required ...``                                               | 报错      | 用 Zarr 引擎却没装 zarr        |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``KeyError: "not all values found in index 'time'. Try setting the method keyword argument"``   | 报错      | ``sel`` 找的坐标值不存在（越界 |
|                                                                                                 |           | / 无精确值）                   |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``IndexError: index ... is out of bounds``                                                      | 报错      | ``isel`` 序号越界              |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``TypeError: invalid indexer array, does not have integer dtype``                               | 报错      | ``isel``                       |
|                                                                                                 |           | 给了坐标值/日期而不是序号      |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``KeyError: "'temp' is not a valid dimension or coordinate ..."``                               | 报错      | ``sel`` 把变量名当成坐标/维度  |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``KeyError: "No variable named 'station' ..."``                                                 | 报错      | ``groupby``                    |
|                                                                                                 |           | 的分组维不存在于数据里         |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``ValueError: replacement dimension 'lat' is not a 1D variable along the old dimension 'time'`` | 报错      | ``swap_dims``                  |
|                                                                                                 |           | 误用（把无关维换成维）         |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``ValueError: Invalid frequency: MX`` / ``FutureWarning: 'M' is deprecated ... use 'ME'``       | 报错/警告 | ``resample`` 频率串写错 /      |
|                                                                                                 |           | 旧写法弃用                     |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``ValueError: unrecognized engine for to_netcdf: 'seqfile'``                                    | 报错      | ``to_netcdf``                  |
|                                                                                                 |           | 指定不存在的写引擎             |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``PermissionError: [Errno 13] Permission denied``                                               | 报错      | 保存到不存在的目录             |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``ValueError: weights cannot contain missing values``                                           | 报错      | ``weighted()`` 权重里混了 NaN  |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``KeyError: '[100] not found in axis'``                                                         | 报错      | ``drop_sel``                   |
|                                                                                                 |           | 删一个不存在的坐标             |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``SerializationWarning: ... floating point data as an integer dtype without any _FillValue``    | 警告      | 浮点带 NaN                     |
|                                                                                                 |           | 却存成整型且没给缺测值         |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``RuntimeWarning: invalid value encountered in cast``                                           | 警告      | astype 截断时 NaN 被强转       |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``sel(time=0)`` 对 datetime 坐标返回空/报错                                                     | 静默/报错 | 用位置整数当坐标值             |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``isel(time="2024-01-15")`` 返回乱 index 报错                                                   | 报错      | 用坐标值当序号                 |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``mean()`` 忘写 ``dim`` 把全场压成一个数                                                        | 静默      | 忘了 ``mean(dim=[...])``       |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| 坐标被手改 / 把 data 换成裸 ndarray 丢坐标                                                      | 静默      | 坐标和数组不同步               |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| 单位没转 K→C 就统计/出图                                                                        | 静默      | 再分析气温默认开尔文，整体差   |
|                                                                                                 |           | 273.15                         |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| 高纬没做纬度加权就区域平均                                                                      | 静默      | 高纬网格面积小权重被高估（8.8  |
|                                                                                                 |           | 最佳实践）                     |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+
| ``lat`` 从大到小排列数据却 ``slice(30, 40)``                                                    | 静默      | 返回空切片（lat 方向反了）     |
+-------------------------------------------------------------------------------------------------+-----------+--------------------------------+

..

   **一句话记住**\ ：Xarray
   的核心控制在「\ **维度与坐标**\ 」这对概念上——绝大多数报错是「\ **用错了按什么取**\ （\ ``sel``
   按坐标值 / ``isel`` 按序号 / ``method=`` 邻近）」，以及「\ **缺了 IO
   引擎 / 维度不存在**\ 」。而最阴险的仍是第 3 类静默错值：\ **忘写
   ``dim``\ 、坐标与数组不同步、单位没转、区域平均没加权**\ 。

--------------

.. _81-无法打开文件缺-io-引擎--路径不存在--文件损坏:

8.1 无法打开文件：缺 IO 引擎 / 路径不存在 / 文件损坏
----------------------------------------------------

Xarray 打开 NetCDF
是靠\ **「引擎（engine）」**——一个实际的底层库（\ ``netcdf4`` /
``h5netcdf`` / ``scipy`` / ``cfgrib`` /
``zarr``\ ）去真正读写字节。文件扩展名决定 Xarray
默认猜哪个引擎，而引擎要\ **先安装对应的库**。这一节全部围绕「引擎」这一根线。

.. _811-文件路径不存在--filenotfounderror报错:

8.1.1 文件路径不存在 → ``FileNotFoundError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   import xarray as xr
   ds = xr.open_dataset("no_such_file.nc")    # 拼错路径/文件名

.. code:: text

   Traceback (most recent call last):
     ...
     File "src/netCDF4/_netCDF4.pyx", line 2521, in netCDF4._netCDF4.Dataset.__init__
     File "src/netCDF4/_netCDF4.pyx", line 2158, in netCDF4._netCDF4._ensure_nc_success
   FileNotFoundError: [Errno 2] No such file or directory: 'D:\\Code\\Vibe\\no_such_file.nc'

**原因**\ ：你把「一个本不存在的文件路径」交了出去，底层 netCDF4
库按路径去打开文件却找不到。\ ``FileNotFoundError`` 是 ``OSError``
的一种，气象里几乎都是「路径写错 / 文件名少个字母 /
当前工作目录和文件不在同一处」。

**解决办法**\ ：

- 用绝对路径或先打印当前目录：\ ``import os; print(os.getcwd())``\ ，然后确认真实文件名；
- 养成习惯：读之前 ``import os; print(os.path.exists("xxx.nc"))``\ ，为
  ``False`` 就先查路径而不是硬啃报错；
- 注意相对路径是基于「脚本所在工作目录」，不是脚本文件所在目录——Jupyter
  里尤其容易踩。

..

   **气象场景一句话**\ ：QuikSCAT/ERA5 转存的分析文件明明拷到了 lab
   但泄漏个 ``_v2`` 后缀，\ ``open_dataset``
   就报「文件不存在」——就像拿着台风路径图去档案馆找编号
   2024xx，结果文件名多了一位或少了一位，检索直接落空。

--------------

.. _812-缺-netcdf4-引擎用-scipy-兜底--显式指定-engine:

8.1.2 缺 ``netcdf4`` 引擎（用 scipy 兜底 / 显式指定 ``engine=``\ ）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实说明**\ ：\ ``open_dataset`` 默认会\ **自动选引擎**\ ：后缀
``.nc`` 通常优先 ``netcdf4``\ ，没装就降级 ``scipy``\ 。本机已装
netCDF4，显式指定 ``engine="netcdf4"`` 能正常打开：

.. code:: python

   import xarray as xr
   ds = xr.open_dataset("northwest_temp.nc", engine="netcdf4")
   print(dict(ds.sizes))     # {'time': 30, 'lat': 11, 'lon': 21}

.. code:: text

   engine=netcdf4 OK, dims = {'time': 30, 'lat': 11, 'lon': 21}

**原因**\ ：\ ``engine=``
参数把「用哪个底层库读」从自动变成手动。当你装了多个引擎，显式指定最稳、也最能控制行为（见
8.1.4 的格式差异）。

**几个 “缺引擎” 的连带报错（这些才是初学者常撞的墙）**\ ：

- **文件是 NetCDF4（HDF5 容器），但只有 scipy 引擎**\ （scipy 只懂
  NetCDF3 classic），就会报 8.1.4 的
  ``TypeError ... not a valid NetCDF 3 file``\ ，并贴心提示装 netcdf4；
- **缺 h5py**\ （h5netcdf 引擎的底层）时报：

.. code:: text

   ImportError: No module named 'h5py', backend not available. Please install 'h5py' into your Python environment.

**解决办法**\ ：安装对应库即可——``conda install -n met_p312 netcdf4`` 或
``pip install netcdf4 h5netcdf h5py``\ 。装完重启内核/脚本，再
``engine=...`` 指定。

   **气象场景一句话**\ ：\ ``engine``
   就像「用哪家解码器打开卫星原始二进制」——装了 ``netcdf4``
   这个「解码器」才能读 NetCDF4 容器；只装了 scipy
   这个「老式解码器」，碰到新式 HDF5 容器自然打不开。

--------------

.. _813-打开-grib-文件缺-cfgrib--modulenotfounderror--unrecognized-engine报错:

8.1.3 打开 GRIB 文件缺 ``cfgrib`` → ``ModuleNotFoundError`` / ``unrecognized engine``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：气象业务里大量欧洲中期（ECMWF）产品是
``.grib`` 格式，读它必须靠 ``cfgrib`` 引擎。本机刻意没装 cfgrib：

.. code:: python

   import xarray as xr
   xr.open_dataset("fake.grib")                      # 不给 engine, 让 xarray 猜

.. code:: text

   ValueError: did not find a match in any of xarray's currently installed IO backends ['netcdf4', 'h5netcdf', 'scipy']. Consider explicitly selecting one of the installed engines via the ``engine`` parameter, or installing additional IO dependencies, see:
   https://docs.xarray.dev/en/stable/getting-started-guide/installing.html
   https://docs.xarray.dev/en/stable/user-guide/io.html

而显式指定 ``engine="cfgrib"`` 时（因为 cfgrib
根本没注册成引擎），再报：

.. code:: python

   xr.open_dataset("fake.grib", engine="cfgrib")

.. code:: text

   ValueError: unrecognized engine 'cfgrib' must be one of your download engines: ['netcdf4', 'h5netcdf', 'scipy', 'store']. To install additional dependencies, see:
   https://docs.xarray.dev/en/stable/user-guide/io.html
   https://docs.xarray.dev/en/stable/getting-started-guide/installing.html

若你直接写 ``import cfgrib``\ ，也会以更直白的 ``ModuleNotFoundError``
呈现：

.. code:: text

   ModuleNotFoundError: No module named 'cfgrib'

**原因**\ ：\ ``.grib`` 不是 NetCDF，普通的 netcdf4/scipy
引擎都不认识它；读 GRIB 必须装 ``cfgrib``\ （内含 ECMWF 的 eccodes
解码器）。没装时，Xarray 默认引擎列表里根本没有
``cfgrib``——于是「没匹配」「引擎名无法识别」两类报错轮番登场。

**解决办法**\ ：装 cfgrib 并在 ``open_dataset`` 里指定引擎：

.. code:: bash

   conda install -c conda-forge cfgrib

.. code:: python

   ds = xr.open_dataset("era5_pressure.grib", engine="cfgrib")

**联想口诀**\ ：看到 ``No module named 'cfgrib'`` 或
``unrecognized engine 'cfgrib'``\ ，\ **第一反应就是「没装 GRIB
解码器」**——不是代码错，是缺库。

   **气象场景一句话**\ ：cfgrib 之于 GRIB，就像能读 ECMWF
   原始编码的解码员——你没请这位解码员（没装库），档案还是那个档案，只是没人能念给你听，前台只能回你一句「我不认识这种类型」（\ ``unrecognized engine``\ ）。

--------------

.. _814-文件不是合法-netcdf签名损坏拿文本冒充-typeerror--oserror报错:

8.1.4 文件不是合法 NetCDF（签名损坏/拿文本冒充）→ ``TypeError`` / ``OSError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：把一段文本误存成
``.nc``\ ，或用损坏的文件去读：

.. code:: python

   # 先用文本写一个"假的 .nc"
   with open("bogus.nc", "w") as f:
       f.write("01\n02\n03\nnot netcdf magic bytes\n")
   xr.open_dataset("bogus.nc", engine="scipy")      # scipy 引擎
   xr.open_dataset("bogus.nc", engine="netcdf4")    # netcdf4 引擎

scipy 版本（真实）：

.. code:: text

   TypeError: Error: data\bogus.nc is not a valid NetCDF 3 file
               If this is a NetCDF4 file, you may need to install the
               netcdf4 library, e.g.,
               $ pip install netcdf4

netcdf4 版本（真实）：

.. code:: text

   OSError: [Errno -51] NetCDF: Unknown file format: 'D:\\Code\\Vibe\\bogus.nc'

**原因**\ ：NetCDF 文件开头有固定的「魔数/签名」（\ ``CDF`` 或 HDF5 的
``\x89HDF``\ ），用来声明「我是 NetCDF」。这个 ``bogus.nc``
是纯文本，签名对不上——scipy 一口咬定它不是 NetCDF3，netcdf4 则抛出
``-51``\ （网际码「未知文件格式」）。

**解决办法**\ ：

- 先确认文件真的合法：命令行 ``ncdump -h 文件``\ （netcdf4 自带的
  ``ncdump``\ ）或 Python 里 ``file`` 读头部几个字节看签名；
- 若「文件是文本」，检查是不是下载/转换时没成功、网盘同步了一半、后缀被错改；
- 若「文件是 NetCDF4 但被 scipy 报了本错误」，明说
  ``engine="netcdf4"``\ ，因为 scipy 只支持老式 NetCDF3。

..

   **气象场景一句话**\ ：NetCDF
   签名就像身份证上的「民族信息」——你拿出生证复印件去读，系统核对开头签名发现不是有效证照，直接拒收；而
   ``-51`` 这种「Errno
   负号」是网际库特有的保密话术，翻译过来就是「格式不是我能认的」。

--------------

.. _815-指定一个不存在的-engine-名--valueerror报错:

8.1.5 指定一个不存在的 ``engine`` 名 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：把 ``engine`` 写成手滑的名字：

.. code:: python

   xr.open_dataset("northwest_temp.nc", engine="not_a_engine")

.. code:: text

   ValueError: unrecognized engine 'not_a_engine' must be one of your download engines: ['netcdf4', 'h5netcdf', 'scipy', 'store']. To install additional dependencies, see:
   https://docs.xarray.dev/en/stable/user-guide/io.html
   https://docs.xarray.dev/en/stable/getting-started-guide/installing.html

**原因**\ ：Xarray
只认识它安装时注册的那几个引擎名（列表写在报错里）。写错名字，它就只能把你给的字符串和已装列表比对，全不匹配就报错。

**解决办法**\ ：照着报错里给的列表
``['netcdf4', 'h5netcdf', 'scipy', 'store']`` 确认拼写；常见手滑是
``netcdf4`` 与 ``h5netcdf`` 拼错、或把 ``engine`` 与 ``backend``
混用（Xarray 常把这俩当作同一概念）。

   **气象场景一句话**\ ：\ ``engine``
   列表就是「你们单位已装的那几台都卜勒雷达型号」——你报了个未入列的型号（\ ``not_a_engine``\ ），调度中心只能回你「没这台」（unrecognized
   engine）。

--------------

.. _816-zarr-缺库--importerrorthe-zarr-package-is-required报错:

8.1.6 Zarr 缺库 → ``ImportError：The zarr package is required``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：用 Zarr（云盘存 NetCDF 的现代格式）却没装
zarr：

.. code:: python

   temp.to_zarr("output.zarr")

.. code:: text

   ModuleNotFoundError: No module named 'zarr'
   ...
   ImportError: The zarr package is required for working with Zarr stores but could not be imported. Please install it with your package manager (e.g. conda or pip).

**原因**\ ：Zarr 是独立生态，不是 netCDF4 能读的。\ ``to_zarr`` /
``open_zarr`` 自动去找 ``zarr`` 包，没有就给出上面这句「专项提示」。

**解决办法**\ ：\ ``pip install zarr`` 或
``conda install -c conda-forge zarr``\ 。这一条的重点是\ **让你养成「看到缺库提示就装库、而不是死改代码」的习惯**——Xarray
的报错几乎都会在最后告诉你该装什么。

   **气象场景一句话**\ ：Zarr 之于
   NetCDF，就像把气泡图存成「带索引的云盘目录」而不是单个文件——``open_zarr``
   是打开的钥匙，没装 zarr 相当于钥匙没配。

--------------

.. _82-索引方法混淆sel--isel--loc--iloc--isel_points:

8.2 索引方法混淆：sel / isel / loc / iloc / isel_points
-------------------------------------------------------

第 8 章的「重头戏」就是取数。Xarray 给两套取数方法：\ **``sel``
按「坐标值」，\ ``isel`` 按「序号」**\ 。90% 的索引报错来自「\ **把 sel
当 isel、把 isel 当 sel、或对不该取的东西取数**\ 」。

.. _821-sel-用位置整数当坐标值time-是-datetime-keyerror报错:

8.2.1 ``sel`` 用位置整数当坐标值（time 是 datetime）→ ``KeyError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：\ ``time`` 坐标是日期，你却拿整数 0
去按坐标值匹配：

.. code:: python

   import xarray as xr
   ds = xr.open_dataset("northwest_temp.nc")
   temp = ds["temp"]
   temp.sel(time=0)        # time 坐标是 datetime 数组, 没有 0 这个"坐标值"

.. code:: text

   KeyError: "not all values found in index 'time'. Try setting the `method` keyword argument (example: method='nearest')."

**原因**\ ：\ ``sel(time=0)`` 的意思是「我要找 time 坐标上 ``0``
这一个标签」，但 time 坐标存的是 ``2024-01-01 ... 2024-01-30`` 这种
datetime，根本没有 ``0``
这个值。注意这里\ **不是**\ 越界才报，而是「标签不存在」——它把 ``0``
当成坐标值而不是序号找。

**解决办法**\ ：

- 想「取第 0 天」用序号：\ ``temp.isel(time=0)``\ ；
- 想「取 2024 年 1 月 15
  日」用坐标值：\ ``temp.sel(time="2024-01-15")``\ ；
- 想取「最接近某时刻」用
  ``sel(time="2024-01-13 12:00", method="nearest")``\ （见 8.2.4）。

..

   **气象场景一句话**\ ：\ ``sel`` 给出的标签像「要查 2024 年 1 月 15
   日的观测」——你倒好，递上一张写着「第 0
   个格点」的纸条（整数），档案管理员翻了半天标签栏没有「0」这一项，只好回你一句「此标签不存在」（\ ``not all values found``\ ）。

--------------

.. _822-isel-用坐标值--日期字符串--日期对象--indexerror--typeerror报错:

8.2.2 ``isel`` 用坐标值 / 日期字符串 / 日期对象 → ``IndexError`` / ``TypeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：\ ``isel``
只能收「整数序号」，你却给了坐标值、字符串、或 pandas 时间戳：

.. code:: python

   import pandas as pd
   temp.isel(time="2024-01-15")          # isel 要第几个, 给成日期字符串

.. code:: text

   IndexError: index 1705276800000000000 is out of bounds for axis 0 with size 30

（\ ``1705276800000000000`` 是 ``2024-01-15`` 被当成纳秒时间戳了。）

给 pandas ``Timestamp`` 对象时，xarray 换了个更精准的说法：

.. code:: python

   temp.isel(time=pd.Timestamp("2024-01-15"))

.. code:: text

   TypeError: invalid indexer array, does not have integer dtype: array(Timestamp('2024-01-15 00:00:00'), dtype=object)

**原因**\ ：\ ``isel`` 的参数必须是\ **整数下标**\ （\ ``0,1,2,...``
或布尔掩码）。你给了字符串/时间对象，Xarray 先尝试把它当 np
数组下标，结果要么变成天文数字越界（直觉），要么明确告诉你「下标数组不是整数类型」。

**解决办法**\ ：

- 记住铁律：\ **``isel`` 收序号，\ ``sel`` 收坐标值**\ ；
- 想取第几个时次写 ``temp.isel(time=N)``\ ，想按日期取写
  ``temp.sel(time="...")``\ ；
- 混用的瞬间最容易在「时刻顺延/取第几个」处错——宁可多写一条注释。

..

   **气象场景一句话**\ ：\ ``isel`` 是「帮我拿第 5 份探空」，而 ``isel``
   你却报了「分子南纬那一份」——店员一脸困惑：你要第几号就说第几号，报坐标范围我这号牌上没有。

--------------

.. _823-sel-找的坐标值越界或不存在--keyerror报错:

8.2.3 ``sel`` 找的坐标值越界或不存在 → ``KeyError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：坐标数组 ``lat`` 只有 30°–40°，你却去
``sel(lat=100)``\ ：

.. code:: python

   temp.sel(lat=100)      # lat 范围 30.0 ~ 40.0

.. code:: text

   KeyError: "not all values found in index 'lat'. Try setting the `method` keyword argument (example: method='nearest')."

**原因**\ ：\ ``lat`` 坐标上不存在 ``100`` 这个值，\ ``sel``
的精确匹配找不到，于是抛 ``KeyError``\ 。注意：\ **精确匹配失败时抛的是
``KeyError``**\ ，不是空返回——除非你用了 ``slice``\ （见 8.2.6）。

**解决办法**\ ：

- 先看当前范围：\ ``print(temp.lat.values.min(), temp.lat.values.max())``\ ；
- 想要「最接近值」用 ``temp.sel(lat=100, method="nearest")``\ ；
- 想要「一段范围」用 slice：\ ``temp.sel(lat=slice(30, 40))``\ 。

..

   **气象场景一句话**\ ：格点文件只覆盖西北，你却 ``sel(lat=100)``
   想取北纬 100°（物理上不存在）——像 GPS
   坐标准确到火星坐标，地图界外自然无点可返。

--------------

.. _824-sel-无精确值想取邻近--methodnearest本章雏鹰装机键:

8.2.4 ``sel`` 无精确值想取邻近 → ``method="nearest"``\ （本章雏鹰装机键）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 正确用法**\ ：坐标为 2024-01-14，你想取「最接近 2024-01-13
中午」的时刻，就必须加 ``method="nearest"``\ ：

.. code:: python

   r = temp.sel(time="2024-01-13 12:00:00", method="nearest")
   print(str(r.time.values))      # -> 2024-01-14T00:00:00

.. code:: text

   result time = 2024-01-14T00:00:00.000000000

**原因**\ ：\ ``sel`` 默认只做「精确值匹配」，不精确就抛
``KeyError``\ （见 8.2.3）。加了 ``method="nearest"``
它就帮你找「最邻近的坐标」。\ ``method`` 可选 ``nearest`` /
``pad``\ （向前）/ ``backfill``\ （向后）。

**注意（版本差异，务必实测确认）**\ ：当前版本（xarray 2025.6.1）里
``method="nearest"`` 依然有效且\ **无弃用警告**\ （本机实测 0
条警告）。社区正推进用更直白的 ``nearest`` 接口取代 ``method=``
的讨论，但在你当前的 xarray 版本里照常工作；若你的版本升级后报
``AttributeError: ... has no attribute 'nearest_sel'`` 或
``KeyError: args``\ ，请查该版本 ``DataArray.sel``
的签名——用法以你安装版本打印的结果为准，别照抄旧教程死背。

**顺带验证**\ ：\ ``temp.sel(time="2024-01-13 12:00:00")`` **不加**
method 时的真实报错是
``KeyError: "not all values found in index 'time'..."``\ （见 8.2.1
开头）。

   **气象场景一句话**\ ：台风路径是整点报，你要查 12:30
   的位置——精确刻度上没有
   12:30，管库房的说「给你最接近的整点盘点」（\ ``nearest``\ ），这正是「用标签取数」相对裸数组最大的甜头：不用记住第几个冒号。

--------------

.. _825-sel-用-slice-选时间段区域含两头的左闭右闭语义:

8.2.5 ``sel`` 用 ``slice`` 选时间段/区域（含两头的左闭右闭语义）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 正确用法**\ ：\ ``slice`` 切片筛选 2024-01-10 到 2024-01-11：

.. code:: python

   r1 = temp.sel(time=slice("2024-01-10", "2024-01-11"))
   print("切片后 time 数量:", r1.sizes["time"])     # -> 2

.. code:: text

   用 '2024-01-10' slice -> time len: 2  (正常)

**原因与细节**\ ：先用 ``sel(time=slice(a, b))`` 选范围。注意选坐标的
slice 很像 Python 切片：\ ``a``\ 、\ ``b``
边界一般\ **都会包含**\ （也受 ``inclusive`` 影响，见 8.5.4），这是和
Pandas ``loc`` 类似的行为，和 Python 原生 ``a : b``\ （不含
b）不同。取两个端点都含，于是 10、11 这两天都在。

**Lat
方向陷阱（气象高频坑）**\ ：如果数据把纬度排成\ **从大到小（北纬→南纬）**\ ，要取
30–40°N 就必须写 ``sel(lat=slice(40, 30))``\ （从大到小的顺序）而不是
``slice(30, 40)``\ 。方向写反会得到\ **空切片且完全不报错**\ （实测）：

.. code:: python

   # 本机样本 lat 是从小到大(30->40), 因此直接 slice(35, 30) 递减就取空:
   sub = temp.sel(lat=slice(35, 30))
   print(sub.sizes["lat"])       # -> 0 (空, 静默!)

.. code:: text

   slice(35,30) 递减 -> lat len: 0  (空!)

**解决办法**\ ：取区域前先 ``print(ds.lat)`` 看排列方向；递增数据写
``slice(小, 大)``\ ，递减数据写
``slice(大, 小)``——这叫「跟着数组的方向读」。

   **气象场景一句话**\ ：取值范围 ``slice(70,110)``
   像给再分析资料的经纬度画框——数据纬度升序就顺向切，降序（CMA
   老产品常有）就得倒着切，方向反一刀切出去就是白框，程序还一声不吭。

--------------

.. _826-sel-用-slice-的无匹配范围既可能返回空静默也可能报错:

8.2.6 ``sel`` 用 ``slice`` 的无匹配范围既可能返回空（静默）也可能报错
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实规律**\ ：

- 用 **``slice``**
  时，找不到匹配标签\ **不会报错**\ ，只会返回空/截断（静默、宽容）；
- 用 **标量坐标值**\ （\ ``sel(lat=100)``\ ）时，找不到\ **必报
  ``KeyError``**\ （严格）。

对照实测：

.. code:: python

   temp.sel(lat=slice(0, 100))     # 超出范围 across slice -> 顺利返回(非空者都在)
   temp.sel(lat=100)               # 标量 100 不在 -> KeyError

（\ ``slice`` 版本返回的是所有坐标落在 [0,100]
内的点；\ ``sel(lat=100)`` 抛
``KeyError: "not all values found in index 'lat'..."``\ 。）

**原因**\ ：\ ``slice``
表示「一段区间」，区间和坐标交集为空也只是「没有点落在里面」，Python
选择宽容；标量表示「精确取这一个标签」，不在就严格报错。这跟 NumPy
的「切片宽容 / 整数下标严格」是同一套哲学（第 6 章 6.1 讲过）。

**解决办法**\ ：想要「一定取到东西」就用 slice + 事后
``if sub.sizes["lat"] == 0:`` 检查；想要「某个精确点」就 ``sel`` + 加
``method``\ ，或 ``.value`` 存在性检查。

   **气象场景一句话**\ ：区间索引像「截取 26–28
   型等压面之间的气层」——没有就空着；精确索引像「取第 500hPa
   层」——没有这一层档案就当场翻脸（KeyError）。

--------------

.. _827-isloc-已不复存在--loc-与-iloc-用法与-pandas-不同dataarray-上没有-pandas-式串引:

8.2.7 ``isloc`` 已不复存在 / ``loc`` 与 ``iloc`` 用法与 Pandas 不同（DataArray 上没有 pandas 式串引）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 名词澄清**\ ：很多同学在 DataArray 上下意识写 ``da.iloc[0]``
``da.loc[...]``\ 。Xarray 的 ``DataArray`` 其实\ **也有
``.loc``**\ （按坐标值）和\ **没有 ``.iloc``**\ （要用 ``.isel``
替代）：那种「一串逗号裸索引」\ ``da[0, 1]``
是位置索引，可读性极差，官方明令禁用（8.4.1 ``warning``\ ）。

**原因**\ ：Xarray 的设计哲学是「用维度名 +
标签取数，别数第几个」。所以它把 ``iloc`` 换成 ``isel``\ 、把 ``loc``
并入 ``sel``\ ，并鼓励 ``sel``/``isel`` 而\ **不是裸下标**\ 。

**解决办法**\ ：直接统一用
``sel``/``isel``\ ＋维度名。若确实要按位置多选，用 ``isel`` 的列表形式：

.. code:: python

   temp.isel(time=[0, 1, 2])        # 取时间上前 3 个时次
   print(temp.isel(time=[0, 1, 2]).shape)   # -> (3, 11, 21)

..

   **气象场景一句话**\ ：用裸下标 ``da[0, 1]`` 就像只报「第 0 行第 1
   格」而不说是哪个维度——遇到 time/lat/lon
   顺序一换，题就鬼畜；\ ``sel``/``isel``
   是「点名式」取数，当时间/纬度/经度哪都能对上就安全得多。

--------------

.. _828-isel_points-已是过去式--attributeerror报错:

8.2.8 ``isel_points`` 已是过去式 → ``AttributeError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：老教程的 ``isel_points`` 在 2025.x 已移除：

.. code:: python

   temp.isel_points(time=[0, 1])

.. code:: text

   AttributeError: 'DataArray' object has no attribute 'isel_points'

**原因**\ ：老版本有点儿状的 ``isel_points``/``sel_points``
用于沿像素采样，新版用\ **向量化的 ``sel``/``isel``
数组索引**\ 取代（直接给列表即可，见 8.2.7）。它已从 API
里删除，触发的是「属性不存在」的 ``AttributeError``\ 。

**解决办法**\ ：沿坐标取多点用
``temp.sel(time=[该天1, 该天2])``\ （多点坐标值）或
``temp.isel(time=[0, 1, 2])``\ （多点序号）。

   **气象场景一句话**\ ：老版「沿固定扫描线取逐个格点」的 API
   已退役（像老旧探空仪的读数模块），新版只要把想取的点牌写成列表一并交给
   ``sel``/``isel`` 即可。

--------------

.. _83-维度与坐标问题swap_dims--rename--dims-顺序--broadcast--groupby:

8.3 维度与坐标问题：swap_dims / rename / dims 顺序 / broadcast / groupby
------------------------------------------------------------------------

.. _831-swap_dims-误用--valueerror报错:

8.3.1 ``swap_dims`` 误用 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：想用 ``swap_dims``
把「时间维」换成「纬度维」，语义上根本不成立：

.. code:: python

   import numpy as np, xarray as xr
   ds = xr.open_dataset("northwest_temp.nc")
   try:
       ds.swap_dims({"time": "lat"})     # lat 不是沿 time 的一维变量
   except Exception as e:
       import traceback; traceback.print_exc()

.. code:: text

   ValueError: replacement dimension 'lat' is not a 1D variable along the old dimension 'time'

**原因**\ ：\ ``swap_dims`` 的正确用途是「把一个\ **原来沿某维的 1D
坐标/辅助变量**\ 提升成维度」——例如把沿 lon 的 ``station_id`` 提升为
``station`` 维。你用它把毫不相干的 ``lat`` 与 ``time`` 交换，Xarray
检查出「lat 并不是沿 time 的一维变量」，立刻拒绝。

**解决办法**\ ：

- ``swap_dims`` 只用于「把 1D
  辅助坐标升级为维度坐标」，别当「重命名」用；
- 想改维度名用 ``rename``\ （见 8.3.2）；想改维度顺序用
  ``transpose``\ （见 8.3.4）。

..

   **气象场景一句话**\ ：\ ``swap_dims`` 是把「沿 lon
   分布的站号」变成「站维」，把天气图网格的坐标轴从「经度」换成「站序」；你却试图把「时间轴」硬掰成「纬度轴」，结构上两轴没有一一对应，Xarray
   一眼识破。

--------------

.. _832-rename-只改名字不改顺序误当它排序才是坑:

8.3.2 ``rename`` 只改名字不改顺序（误当它排序才是坑）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 正确用法**\ ：

.. code:: python

   ds3 = ds.rename({"temp": "TEMP"})
   print(list(ds3.data_vars))     # -> ['TEMP', 'pres']

.. code:: text

   rename 变量 OK: ['TEMP', 'pres']

**原因与坑**\ ：\ ``rename`` 只是给「变量 / 维度 /
坐标」换个标签，\ **不改变数据在内存的顺序**\ 。很多新手误以为 rename
能「重新排列维度」，结果顺序没变、名字却变了，后面引用旧名直接
``KeyError``\ 。

**解决办法**\ ：改名用 ``rename``\ ，排维度顺序用
``transpose``\ ，排序坐标值用 ``sortby``\ 。三件套别混。

   **气象场景一句话**\ ：改名是把「t2m」登成「TEMP」的名牌，改完格点排布纹丝不动；想调整维序是另一台机器（transpose）的活儿，名牌和排序不可混为一件。

--------------

.. _833-维度顺序与广播同维度不同顺序相加会对齐并可能产生-nan静默陷阱:

8.3.3 维度顺序与广播：同维度不同顺序相加会「对齐」并可能产生 NaN（静默陷阱）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：把 ``(lat, lon)`` 和 ``(lon, lat)``
两个同元素数组相加，Xarray
按\ **维名对齐**\ （不是按第几个轴对齐），结果正确，且正常算子不会填
NaN：

.. code:: python

   o      = temp.isel(time=0)            # dims = (lat, lon)
   o_rev  = o.transpose("lon", "lat")    # dims = (lon, lat)
   s = o + o_rev
   print("shape:", s.shape, " NaN 数量:", int(s.isnull().sum()))

.. code:: text

   shape: (11, 21)  NaN 数量: 0

**原因与坑**\ ：Xarray
自动做「坐标对齐」——同名维度相加，会各自按坐标排序后再对位。所以\ **维度顺序不同不报错**\ ，这正是它比裸
NumPy
安全的地方；但\ **坐标值不同（如经度步长不一致）时，对齐不到的位置会填
NaN**\ （见 8.3.7 ``xr.align``\ ）。新手最怕的「维度顺序错导致计算错」在
Xarray 里多半被自动化解，反而要注意\ **坐标不对齐的静默 NaN**\ 。

**注意**\ ：如果两组坐标本身不完全重合（例如一段 0–14 天一段 10–29
天），加法会产生「只对交集有意义、其余 NaN」的结果（实测见 8.3.7），别被
``sum`` 出的数字骗了。

   **气象场景一句话**\ ：天气图上「今天温度和昨天温度」两个场维度顺序不同，Xarray
   自动按 time/lat/lon
   对了位——比人脑数第几个冒号强多了；但两个场的范围不同（一个含 15
   天，一个只到第 10 天）时，凑不平的格点悄悄变
   NaN，跟凑数掺缺测一样阴险。

--------------

.. _834-transpose-改变维度顺序静默合法:

8.3.4 ``transpose`` 改变维度顺序（静默、合法）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 正确用法**\ ：

.. code:: python

   print(temp.dims)          # ('time', 'lat', 'lon')
   print(temp.transpose("lon", "lat", "time").dims)   # -> ('lon', 'lat', 'time')

.. code:: text

   temp dims: ('time', 'lat', 'lon')
   transpose lon,lat,time: ('lon', 'lat', 'time')

**原因**\ ：\ ``transpose``
只是交换轴的先后顺序，不搬走数据本身；只要名目齐全顺序任意都成立，且完全静默。它在需要某轴放前面的绘图/输出场合常用。

**解决/注意**\ ：\ ``transpose``
合法且静默，但\ **不要依赖维度顺序**——一旦 ``transpose`` 后去看
``shape``\ ，务必再核对维度名：\ ``print(da.dims)``\ 。千万别认为「\ ``shape[1]``
就是经度」，维度名才是唯一真相。

   **气象场景一句话**\ ：transpose
   像把天气图横过来看——数据一个没少，只是把「先纬度再经度」翻成「先经度再纬度」；谁先谁后不影响天气，只会影响你眼睛怎么读
   shape。

--------------

.. _835-xrbroadcast-维度不完全匹配--不报错静默补全成最大形状别误以为会报错:

8.3.5 ``xr.broadcast`` 维度不完全匹配 → 不报错，静默补全成最大形状（别误以为会报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：两个一维数组维度\ **名不同**\ 时，\ ``broadcast``
不会报错，而是各自扩展补齐到能对齐的最大形状：

.. code:: python

   a = xr.DataArray(np.ones(5), dims=["lat"])
   b = xr.DataArray(np.ones(7), dims=["lon"])     # 注意维名不同(这里演示错误写法 lon 是独立维)
   c = xr.broadcast(a, b)
   print(c[0].shape)      # -> (5, 7)

.. code:: text

   broadcast OK: (7, 5)   # 一个变 5x7, 一个也补成 5x7

**原因与坑**\ ：\ ``broadcast``
把两个数组沿着它们\ **没有的维度**\ 各自铺开，使其最终维度为两者的并集、形状为逐维最大。所以「维度名不同」\ **不会报
``ValueError``**\ （和 numpy 纯数值广播参数错时才报
:math:`... broadcast...` 不同，见第 6 章 6.2）。真正会报 broadcast
错的是\ **相同维度名长度却不兼容**\ 时：

.. code:: python

   a = xr.DataArray(np.ones(5), dims=["lat"])
   b = xr.DataArray(np.ones(7), dims=["lat"])     # 同维 lat 长度 5 vs 7
   try:
       r = a + b
   except Exception as e:
       import traceback; traceback.print_exc()

.. code:: text

   xarray.structure.alignment.AlignmentError: cannot reindex or align along dimension 'lat' because of conflicting dimension sizes: {5, 7}

**解决办法**\ ：\ ``xr.broadcast``
不报错、静默补齐；真正会因为广播/对齐报错的是「同一维度名长度冲突」（\ ``AlignmentError ... conflicting dimension sizes``\ ）。所以想让两个场和坐标对齐相加，务必先核对维度名和坐标一致。

   **气象场景一句话**\ ：\ ``broadcast_like`` 是把一维的 ``cos(lat)``
   权重「铺满」到和平面场同形状，如同把纬度权重拷贝到每个经度——若两个东西叫同一个名却尺寸不同（你说纬度
   5 格我却有 7 格），就当场「名字冲突」（conflicting sizes）。

--------------

.. _836-groupby-分组维不存在--keyerror报错:

8.3.6 ``groupby`` 分组维不存在 → ``KeyError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：数据里根本没有 ``station`` 维，你却
``groupby("station")``\ ：

.. code:: python

   ds.groupby("station").mean()

.. code:: text

   KeyError: "No variable named 'station'. Variables on the dataset include ['time', 'lat', 'lon', 'temp', 'pres']"

**原因**\ ：\ ``groupby``
要求按一个\ **存在的维度或坐标**\ 分组。你给的名字不在数据里，Xarray
查阅组名失败并列出当前所有变量给你对。\ **看到列表
``[... ]``\ ，第一反应就是查该名字是否存在**\ 。

**解决办法**\ ：先 ``print(list(ds.coords))`` / ``print(ds.dims)``
看有哪些可分组项；按时间月份分组要写 ``ds.groupby("time.month")``\ （见
8.5.5，这是 Xarray 特有的「一维取分组键」语法）。

   **气象场景一句话**\ ：groupby
   像按「站点」归档某区域的观测记录，但这份资料压根没建 ``station``
   维度——归档前先确认「按什么分组」，它把现有字段列给你看（include
   […]），就是要你从列表里挑一个存在的键。

--------------

.. _837-xralign-坐标不重叠--自动补-nan静默最阴险之一:

8.3.7 ``xr.align`` 坐标不重叠 → 自动补 NaN（静默，最阴险之一）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：把一段 ``time[0:15]`` 与另一段 ``time[10:30]``
做外对齐（outer join），未重叠段全补 NaN：

.. code:: python

   va = temp.isel(time=slice(0, 15))
   vb = temp.isel(time=slice(10, 30))
   a2, b2 = xr.align(va, vb, join="outer")
   print(a2.shape, " 补了几个 NaN:", int(a2.isnull().sum()))

.. code:: text

   align outer 后 shape: (30, 11, 21)  补了多少 nan: 3465

默认 ``join="inner"`` 则只留交集（比 ``outer`` 少 15–5 段）：

.. code:: python

   a2, b2 = xr.align(va, vb)          # 默认 inner
   print(a2.sizes["time"])            # -> 5  (两段公共的时间)

.. code:: text

   align 默认(inner) 后 time len: 5

**原因**\ ：\ ``xr.align``
用于把两组坐标对齐到「同一套坐标」，\ ``outer`` 取并集、未处合的格点补
NaN；\ ``inner`` 取交集。新手常忘传 ``join``\ ，默认 inner
会\ **悄悄丢掉不叠的时间**\ ，若你没注意到公共段只有 5
天，后续「平均」就只算交集。

**解决办法**\ ：想做「补齐到并集」就显式
``join="outer"``\ （并留意生成了很多 NaN）；只想取公共部分就接受
inner；两段范围该不该并集，取决于你想不想把缺测以 NaN 形式补出来。

   **气象场景一句话**\ ：align
   像把两把冷暖锋前的观测时间线对齐——``outer``
   把两边缺的时段都补成空格（NaN），\ ``inner``
   只保留两线都有的公共窗口；不指定 join 默认 inner，可能把你要的「前 15
   天」悄悄砍成「中间 5 天」。

--------------

.. _84-dataarray-vs-dataset混用会怎么错:

8.4 DataArray vs Dataset：混用会怎么错
--------------------------------------

.. _841-daseltemp20-而-temp-是变量不是坐标维度--keyerror报错:

8.4.1 ``da.sel(temp=20)`` 而 temp 是\ **变量**\ 不是坐标/维度 → ``KeyError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   temp = ds["temp"]
   temp.sel(temp=20)     # temp 是 data variable, 不是坐标/维度

.. code:: text

   KeyError: "'temp' is not a valid dimension or coordinate for Dataset with dimensions FrozenMappingWarningInAbc({'time': 30, 'lat': 11, 'lon': 21})"

**原因**\ ：\ ``sel(temp=20)`` 要求 ``temp``
是一个\ **维度或坐标**\ 。但你的数据集里 ``temp``
是\ **数据变量**\ （变量，不是坐标）。\ ``sel`` 只在坐标/维度里找
``temp``\ ，找不到就报
``'temp' is not a valid dimension or coordinate``\ 。

**解决办法**\ ：

- 想「按温度值过滤格点」用掩码：\ ``ds["temp"].where(ds["temp"] > 20)``\ （where
  是布尔掩码，见 8.4.5）；
- 想「取 temp 这个变量」用 ``ds["temp"]`` 或 ``ds.temp``\ ；
- 分清楚：\ **坐标（coords）是你索引用的标签，变量（data_vars）是被索引的数据**\ 。

..

   **气象场景一句话**\ ：\ ``sel(temp=20)`` 像你说「把气温 ＝ 20℃
   那一行叫出来」——可气温不是它的行标题，而是档案里的数值栏；要筛数值得用
   where 面具，索引得用来定位的维度（time/lat/lon）。

--------------

.. _842-numpy-数学运算作用于-dataset--返回-dataset别当报错:

8.4.2 numpy 数学运算作用于 Dataset → 返回 Dataset（别当报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：\ ``np.sin(ds)`` 对整个 Dataset
逐变量运算，返回一个 Dataset：

.. code:: python

   nds = np.sin(ds)
   print(type(nds).__name__)     # -> Dataset

.. code:: text

   np.sin(ds) 类型: Dataset

**原因与坑**\ ：Xarray 的 Dataset 实现了 NumPy 的
``__array_ufunc__``\ ，所以 ``np.sin``\ 、\ ``np.exp`` 等会对每个
data_vars 执行并保留坐标，返回 Dataset。\ **这通常不是
bug**\ ，但新手若误以为返回的是数组/DataArray，就可能错用 ``.values``
或误判 ``len()``\ 。

**解决办法**\ ：先 ``print(type(obj))``\ ；对单一变量用
``da = ds["temp"]`` 后再
``np.sin(da)``\ 。想「每个变量分别处理、再装回一个表」，返回 Dataset
反而是便利。

   **气象场景一句话**\ ：对整本 Dataset 做 ``np.exp``
   就像对整张观测表每列都做指数换算——Xarray
   贴心地逐个变量算还保留坐标，返回的还是「多变量档案册」，不是一张裸表。

--------------

.. _843-assign_coords-vs-coordsupdate一个返回新对象一个就地改:

8.4.3 ``assign_coords`` vs ``coords.update``\ ：一个返回新对象、一个就地改
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   dsA = ds.assign_coords({"newcoord": (("time",), np.arange(30))})
   print("newcoord in coords?", "newcoord" in dsA.coords)     # -> True

   dsB = ds.copy()
   dsB.coords.update({"lat": dsB.lat * 2})     # 就地改坐标, 放大 2 倍
   print(dsB.lat.values[:2])                    # -> [60. 62.]

.. code:: text

   assign_coords 后 newcoord 在: True
   coords.update 后 lat 前2个: [60. 62.]

**原因与坑**\ ：

- ``assign_coords`` **返回一个新对象**\ ，不改原
  ``ds``——若你不接返回值，改了等于没改（静默丢改动）；
- ``coords.update`` 是\ **就地（in-place）修改**\ ，会直接改原
  ``ds``\ 。两者行为一个「新」一个「改」，用错场合极易「改了没生效 /
  悄悄改了原对象」。

**解决办法**\ ：习惯用「新对象」风格
``ds2 = ds.assign_coords(lat=ds.lat*2)``\ ，可读性好、可复现；就地
``coords.update`` 只在确实想改原对象时用，且注意它不返回新表。

   **气象场景一句话**\ ：assign_coords
   像打印一份修订版天气图（原图不动），coords.update
   像直接在底图上改坐标标注（原图被涂改）——气象归档多半要保留原图，别用就地修改污染源数据。

--------------

.. _844-坐标对齐产生的-nanreindex_like-补全810-重点坑:

8.4.4 坐标对齐产生的 NaN：\ ``reindex_like`` 补全（8.10 重点坑）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 说明**\ ：第 8 章 8.10 第 4 条专门警告「两个 Dataset
合并时维度不完全一致，会在错位格点产生 NaN」。这正是 8.3.7 的
``xr.align`` 例子的业务来源。补法是用 ``reindex_like``\ ：

.. code:: python

   ds2 = ds1.reindex_like(ds_large, method="nearest")

**原因**\ ：合并/相加时坐标只对齐公共部分，不同部分补
NaN。\ ``reindex_like`` 能把 ``ds1`` 重采样到 ``ds_large``
的坐标网格上（\ ``method="nearest"`` 取邻近），使坐标完全一致、消除
NaN。

**解决办法**\ ：合并前先 ``xr.align`` 或 ``reindex_like``
统一坐标；对齐后要 ``print(da.isnull().sum())`` 检查有没有无心补出的一堆
NaN。

   **气象场景一句话**\ ：把两张分辨率/范围不同的再分析画到一张图上，坐标格点对不上就咬合处冒出
   NaN——``reindex_like``
   像把两套网格重新对到同一套刻度尺，邻近值顶替，缺测自然消于无形。

--------------

.. _845-where-掩码条件不满足被置-nan静默别忘它会把全场变成全-nan:

8.4.5 ``where`` 掩码：条件不满足被置 NaN（静默，别忘它会把全场变成全 NaN）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：用绝对 K 温度（~12K）对一个注定全 False 的条件
``> 100`` 做 ``where``\ ，结果整场被置 NaN，比例 1.0：

.. code:: python

   mask = temp.isel(time=0) > 100          # temp ~ 12 K, 全 False
   snap = temp.isel(time=0).where(mask)
   print(float(snap.isnull().mean()))      # -> 1.0 (全场 NaN!)

.. code:: text

   where 全 False 后 NaN 比例: 1.0

**原因与坑**\ ：\ ``where(cond)`` 把「条件为假」的位置全部置
NaN（默认）；若条件设计失误（例如把摄氏度的阈值套在开尔文数据上），会导致\ **全场变
NaN**\ ，不报任何错。这是典型的「掩码加单位错位」的静默污染。

**解决办法**\ ：用 ``where`` 前先明确单位（K 还是 ℃）；条件写完后
``print(mask.mean())``
看保留比例，别等画出来才发现一片空；想保留原值可用
``da.where(cond, other)`` 指定填充。

   **气象场景一句话**\ ：\ ``where``
   像用温度阈值给格点「打勾」——你拿着摄氏观感（>100℃）去给开尔文数据（约
   285K）打勾，结果整片都不满足、全被判「缺测」清空，看似没报错其实图都空了，这是单位错位最阴险的出场方式。

--------------

.. _85-时间维dt-属性--resample--inclusive--groupbytimemonth:

8.5 时间维：dt 属性 / resample / inclusive / groupby(‘time.month’)
------------------------------------------------------------------

.. _851-dt-时间属性dtmonth-dtdayofyear-等正常注意别名:

8.5.1 ``.dt`` 时间属性：\ ``.dt.month`` ``.dt.dayofyear`` 等（正常，注意别名）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 正确用法**\ ：时间坐标可以直接挑出「月份、一年第几天」：

.. code:: python

   print(temp.time.dt.month.values[:3])       # -> [1 1 1]
   print(temp.time.dt.dayofyear.values[:3])   # -> [1 2 3]

.. code:: text

   dt 访问 month: [1 1 1]
   dt.dayofyear: [1 2 3]

**原因与坑**\ ：\ ``.dt`` 是「时间串接器」，把 datetime
拆成可用的年/月/日等。常见错误是漏写 ``.dt``\ ：直接 ``temp.time.month``
会报
``AttributeError: 'DataArray' object has no attribute 'month'``\ （实测），因为
``month`` 是 ``.dt`` 下的小道具。\ **记住：拆时间的属性要挂在 ``.dt``
后面。**

**解决办法**\ ：\ ``temp.time.dt.month``\ 、\ ``temp.time.dt.dayofyear``\ 、\ ``temp.time.dt.season``
等；漏了 ``.dt`` 就补上。

   **气象场景一句话**\ ：\ ``.dt``
   像给时间坐标配的一把「放大镜」，从一年 365
   天的串里挑出月份、第几天、季节等小刻度；忘了加 ``.dt``\ ，就像问一个
   Sequence 对象「你的 month 属性在哪」——它根本没有。

--------------

.. _852-resample-频率串写错--valueerror-invalid-frequency报错:

8.5.2 ``resample`` 频率串写错 → ``ValueError: Invalid frequency``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：把 ``"ME"`` 打成不存在的 ``"MX"``\ ：

.. code:: python

   temp.resample(time="MX").mean()

.. code:: text

   ValueError: Invalid frequency: MX, failed to parse with error message: KeyError('MX')

（中间还套了 pandas 内部的 ``KeyError: 'MX'``——频率是给 pandas
解析的，\ ``MX`` 不在它认识的频率字典里。）

**原因**\ ：\ ``resample(time=频率串)`` 的频率字符串是 pandas
规定的枚举（\ ``D/W/ME/MS/YE/H`` 等），不是随取。打错字母
``ME→MX``\ 、或把数字前缀写错（如 ``5M`` 这种旧写法），都会让 pandas
解析失败扔 ``Invalid frequency``\ 。

**解决办法**\ ：频率串严格用官方写法——``D`` 日、\ ``W`` 周、\ ``ME``
月末、\ ``MS`` 月初、\ ``YE`` 年末、\ ``H`` 时、\ ``5D``
五天（候）。对照官方频率表对一遍再跑。

   **气象场景一句话**\ ：resample
   的频率串像日历里的「抽样间隔编号」——你想「按月抽样」却手滑成
   ``MX``\ ，日历根本不认这个编号，只能回你「Invalid
   frequency：MX，查无此号」。

--------------

.. _853-resample-旧写法-m--y-被弃用--futurewarning警告不中断:

8.5.3 ``resample`` 旧写法 ``'M'`` / ``'Y'`` 被弃用 → ``FutureWarning``\ （警告，不中断）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实警告**\ ：新版推荐 ``ME``/``YE``\ ，旧写法 ``M``/``Y``
会触发 ``FutureWarning``\ （但仍可运行）：

.. code:: python

   import warnings; warnings.simplefilter("always")
   r = temp.resample(time="M").mean()

.. code:: text

   FutureWarning: 'M' is deprecated and will be removed in a future version, please use 'ME' instead.

**原因**\ ：pandas 3.0 移除了月份/年份的 ``M``/``Y``
旧缩写，改用明确含时序的 ``ME``\ （month end）、\ ``YE``\ （year
end）。Xarray 的 resample 把频率串转给
pandas，于是也收到同样的弃用警告。

**解决办法**\ ：日→月用 ``"ME"``\ 、日→年用 ``"YE"``\ 。练习里若课件还写
``"M"``\ ，见到这条 FutureWarning 就把它升级成
``ME``——这是很典型的「老教程写法 +
新版本弃用」现场，学会读警告说明并迁移到新写法。

   **气象场景一句话**\ ：\ ``M``\ →\ ``ME``
   就像把「月」这个简称升级成「月底」精确说法——老车型还能开，但交通部（新版本）已经预告它要淘汰（FutureWarning），趁早换成新缩写最省心。

--------------

.. _854-sel-时间坐标的边界当天语义与-inclusive-参数注意版本差异:

8.5.4 ``sel`` 时间坐标的边界/当天语义与 ``inclusive`` 参数（注意版本差异！）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 关键版本差异说明（务必实测）**\ ：尝试给 ``.sel`` 直接传
``inclusive="left"``\ ，在测试环境（xarray 2025.6.1）\ **会报错**——因为
``sel`` 在这个版本不接收 ``inclusive`` 参数：

.. code:: python

   sample = xr.DataArray(np.arange(4), dims="time", coords={
       "time": pd.to_datetime(["2024-01-01","2024-01-02","2024-01-03","2024-01-04"])})
   try:
       sample.sel(time=slice("2024-01-02","2024-01-03"), inclusive="left")
   except Exception as e:
       import traceback; traceback.print_exc()

.. code:: text

   KeyError: "'inclusive' is not a valid dimension or coordinate for Dataset with dimensions {...({'time': 4})}"

**原因与坑**\ ：历史上有版本的 ``sel`` 允许 ``inclusive``
控制边界含不含；本机这个版本把它当成一个「维/坐标名」去解析，于是报「不是有效维/坐标」。\ **这说明时间边界语义在不同版本有出入**——千万不要照抄别人教程的高版本关键词就假设自己版本也支持。稳妥做法：

.. code:: python

   # 确定要含两端: 直接用 slice 默认(左闭右含中间按 pandas 处理)
   sh = sample.sel(time=slice("2024-01-01","2024-01-03"))
   print(sh.time.dt.day.values)   # -> [1 2 3]  两端都保留

**当天的边界坑**\ ：若数据是「日」，\ ``sel(time="2024-01-13 12:00")``
这种不到整点的时间点不属于任何一天，必报 KeyError（见
8.2.4）。想当天整取，要么给当天 00:00 的精确标签，要么
``method="nearest"``\ 。

**解决办法**\ ：涉及「时间段两端到底含不含」的判断，先用 8.5.5 的 small
例子跑一遍看结果，再决定用 slice + 精确到「天」的标签。最稳的是\ **先
``print(da.time)`` 看清粒度，再按粒度写标签**\ 。

   **气象场景一句话**\ ：时间点取数像「查 1 月 15 日 12
   点的探空」——数据按天给就没有 12
   点这一条；而时间边界含不含、\ ``inclusive``
   反不反，是版本敏感项，务必现场自测而不是背教程结论。

--------------

.. _855-groupbytimemonth-多分组正确写法与单一分组输出:

8.5.5 ``groupby('time.month')`` 多分组（正确写法）与单一分组输出
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 正确用法**\ ：

.. code:: python

   mbins = temp.groupby("time.month").mean()
   print(mbins.month.values)     # -> [1]  (本样本只有 1 月)

.. code:: text

   month bins: [1]

**原因与说明**\ ：\ ``groupby('time.month')`` 会先 ``dt.month``
取出月份，再按月份分组取平均。样本只有 2024-01 一个月份，所以只有 1
个分组 ``[1]``\ 。若数据跨多月（如 8.9 综合实战的多年 6/7/8 月），会得到
``[6 7 8]``\ 。

**解决办法**\ ：想多年各月气候态
``ds.groupby("time.month").mean()``\ ；后面配合
``ds.isel(time=ds.time.dt.month.isin([6,7,8]))`` 取夏季；按年取可用
``groupby("time.year")``\ 。多个分组时要先确认数据里确实有多年的值，否则只有一个分组也不奇怪。

   **气象场景一句话**\ ：\ ``groupby('time.month')``
   像把整年的逐日气温按「月份」归档成 12
   沓再各算均值——若你只存了某一个月，归档出来当然只有一沓，先看数据覆盖范围再谈分组数。

--------------

.. _86-写入--保存to_netcdf-缺引擎--路径不存在--dtype-与-encoding:

8.6 写入 / 保存：to_netcdf 缺引擎 / 路径不存在 / dtype 与 encoding
------------------------------------------------------------------

.. _861-to_netcdf-保存到不存在的目录--permissionerror报错:

8.6.1 ``to_netcdf`` 保存到不存在的目录 → ``PermissionError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   temp.to_netcdf("no/such/dir/out.nc")     # 父目录不存在

.. code:: text

   PermissionError: [Errno 13] Permission denied: 'D:\\Code\\Vibe\\no\\such\\dir\\out.nc'

**原因**\ ：netCDF4 想往 ``no/such/dir/``
里写文件，可那个目录不存在（也没有写权限），于是抛
``[Errno 13] Permission denied``\ 。新手总以为「保存到不存在的路径会自己建目录」——**不会**\ ，目录必须提前存在。

**解决办法**\ ：保存前
``os.makedirs(os.path.dirname(path), exist_ok=True)``\ ；或者存到已存在的目录，用绝对路径避免猜工作目录。

   **气象场景一句话**\ ：\ ``to_netcdf``
   像把观测归档放进一个还没建好的文件夹——门卫没钥匙也没看到门牌，只能回你「Permission
   denied：此路不通」，先 mkdir 建好目录再存。

--------------

.. _862-to_netcdf-指定不存在的引擎--valueerror报错:

8.6.2 ``to_netcdf`` 指定不存在的引擎 → ``ValueError``\ （报错）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：

.. code:: python

   temp.isel(time=0).to_netcdf("x.nc", engine="seqfile")

.. code:: text

   ValueError: unrecognized engine for to_netcdf: 'seqfile'

**原因**\ ：写引擎的名字也就那几个（netcdf4 / h5netcdf / scipy /
zarr…）。写成 ``seqfile``\ （笔误/臆想），Xarray 找不到对应的写后端，报
``unrecognized engine for to_netcdf``\ 。

**解决办法**\ ：确认拼写
``engine="netcdf4"``\ （或省略由默认）。特别注意：\ ``to_netcdf`` 与
``open_dataset`` 的引擎名几乎相同，但 ``open_dataset`` 拼错名字报的是
``unrecognized engine ... must be one of ... download engines``\ （8.1.5），\ ``to_netcdf``
报
``unrecognized engine for to_netcdf``——两处关键词不同，都是同一类「名字错」。

   **气象场景一句话**\ ：写档也有「写引擎」选择——你要求用 ``seqfile``
   这个 3D 打印模式存
   NetCDF，打印机（to_netcdf）根本没这型号，自然报「型号无法识别」。

--------------

.. _863-enginescipy-的局限只支持-netcdf3写回数据须兼容读回丢-info-也常见:

8.6.3 ``engine='scipy'`` 的局限：只支持 NetCDF3，写回数据须兼容（读回丢 info 也常见）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 正确/失败演示**\ ：scipy 引擎只能读写老式 NetCDF3
classic，本机会新装的 NetCDF4
文件用它写没问题（模型片段可顺利写+读回）：

.. code:: python

   ds_small = ds.isel(time=slice(0, 2))
   ds_small.to_netcdf("scipy_out.nc", engine="scipy")
   back = xr.open_dataset("scipy_out.nc", engine="scipy")
   print(dict(back.sizes))     # -> {'lon': 21, 'lat': 11, 'time': 2}

.. code:: text

   engine='scipy' 写入 OK
   scipy 读回 dims: {'lon': 21, 'lat': 11, 'time': 2}

**局限与坑**\ ：scipy 引擎对「NetCDF3」之外的特性（压缩、某些
``_FillValue``\ 、字符编码、多重索引）支持有限；它会把文件名里的 ``.nc``
当作 NetCDF3。若数据是 NetCDF4 独有的特性，用 scipy 写可能报
``TypeError ... not a valid NetCDF 3 file`` 或静默丢信息（尤其 8.1.4
那类签名错误）。

**解决办法**\ ：生产写作首选
``engine="netcdf4"``\ （功能最全）；只有必要时才用 scipy（如抽老数据互通
NetCDF3）。写完务必 ``xr.open_dataset`` 读回核对 ``dims`` 与坐标，防丢。

   **气象场景一句话**\ ：scipy
   引擎像一台只能打老式复写纸的老打印机——小样打起来顺手（NetCDF3），一旦文件用了四维压缩的「新式纸张」（NetCDF4
   特性）它就罢机或悄悄印丢内容，写完读回核对一次保平安。

--------------

.. _864-带-nan-的浮点存整型且没给-_fillvalue--serializationwarning警告丢失:

8.6.4 带 NaN 的浮点存整型且没给 ``_FillValue`` → ``SerializationWarning``\ （警告+丢失）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实警告**\ ：浮点数据里有 NaN，却用 ``encoding`` 把 dtype
指定成整型且没给缺测值：

.. code:: python

   t3 = temp.isel(time=0).where(temp.isel(time=0) > 13)   # 部分 NaN
   t3.to_netcdf("int_nan_out.nc", encoding={"temp": {"dtype": "int16"}})

.. code:: text

   SerializationWarning: saving variable temp with floating point data as an integer dtype without any _FillValue to use for NaNs
     t3.to_netcdf("int_nan_out.nc",
   RuntimeWarning: invalid value encountered in cast
     return data.astype(dtype, **kwargs)

**原因**\ ：把浮点写回整型，Xarray
需要一个整型「缺测哨兵」（\ ``_FillValue``\ ，如 ``-999``\ ）来代表
NaN。你没给，它就一边警告
``without any _FillValue to use for NaNs``\ ，一边把 NaN
硬转（\ ``invalid value encountered in cast``\ ）。

**解决办法**\ ：想保留缺测语义就用返回下述两种：

1. 别指定整型，让其默认 float 存储（NaN 天然可表示）；
2. 若要省空间存整型，务必给缺测值：\ ``encoding={"temp": {"dtype": "int16", "_FillValue": -9999}}``\ ，读回时
   NaN 会用 ``-9999`` 还原（配合 ``ds.attrs`` 记单位）。
   **核心**\ ：\ **浮点数据别随便用整型存**\ ，否则 NaN
   这个「缺测占位」无处安放。

..

   **气象场景一句话**\ ：把带缺测的浮点气温整存，像把「有降雨量
   NaN(无观测)」的一列硬塞进整数记账本——需要先约定一个「无观测」哨兵值（如
   -9999），否则程序只能把 NaN
   硬塞成垃圾数还提醒你「没有缺测哨兵」（without any \_FillValue）。

--------------

.. _865-to_zarr-缺-zarr-包--importerror报错见-816:

8.6.5 ``to_zarr`` 缺 zarr 包 → ``ImportError``\ （报错，见 8.1.6）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错**\ ：保存成 Zarr 但没装 zarr，报
``The zarr package is required for working with Zarr stores ...``\ （完整输出见
8.1.6）。原因、解决全同：装 ``zarr`` 再用 ``to_zarr`` /
``open_zarr``\ 。

**与 to_netcdf 关系**\ ：Zarr 与 NetCDF 是两套生态，\ ``to_zarr``
不存在于 ``to_netcdf`` 的引擎列表，也不接受 ``engine="netcdf4"``——想用
Zarr 一律 ``to_zarr`` + 装 zarr。

--------------

.. _87-气象相关的静默错误与排查最需要培养的尾部报警:

8.7 气象相关的静默错误与排查（最需要培养的“尾部报警”）
------------------------------------------------------

.. _871-meandimlat-忘写-dim--全场压成标量静默attention-brain:

8.7.1 ``.mean(dim='lat')`` 忘写 dim → 全场压成标量（静默！attention brain）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：\ ``temp.mean()``
**不报错**\ 、直接返一个标量；而你本来想要「逐时刻的区域平均」时间序列：

.. code:: python

   full = temp.mean(dim=["lat", "lon"])   # -> (30,) 每时刻一值, 正确
   sca  = temp.mean()                      # 忘写 dim -> 标量 0-D
   print(full.dims, full.shape)            # ('time',) (30,)
   print(sca.dims, sca.shape)              # () ()
   print(float(full.values[0]), "vs", float(sca.values))

.. code:: text

   正确 mean(dim=[lat,lon]) shape: (30,)
   忘写 dim mean -> shape: ()  值: 12.198932102452936
   两者不同:  12.193908413092343 vs 12.198932102452936

**原因**\ ：Xarray 的 ``.mean()`` **没写 dim
时默认对所有轴求均值**\ ，把整个 3D 场压成一个数。这和 NumPy 的
``arr.mean()`` 一样（第 6 章 6.6 强调的 axis/dim 语义）。你只差一个
``dim=[...]``\ ，结果就从「随时间的序列」退化成「一个总平均」。

**解决办法**\ ：改
``.mean(dim=["lat","lon"])``\ （逐时刻区域平均）、\ ``.mean(dim="time")``\ （逐格点时间平均）。这几乎是第
8 章\ **最高频静默错**——``mean()``
明明没报错，却悄悄把你想保留的维度也压没了。写完立即
``print(result.dims)``\ ，确认维度对不对。

   **气象场景一句话**\ ：区域平均是「把每个时刻的空间格点横向压缩」，必须指定压哪两个维度（lat/lon）；忘写
   dim 就像把 30 天 × 11 纬 × 21
   经的整个气温立方体「咣」一股脑平均成一个数，等价于拿全月全区域的单个数去当趋势——程序绿灯到底，科学结论崩盘。

--------------

.. _872-坐标与数据脱钩把坐标当裸数组改--把-data-换裸-ndarray静默丢标签:

8.7.2 坐标与数据「脱钩」：把坐标当裸数组改 / 把 data 换裸 ndarray（静默丢标签）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出（两种脱钩）**\ ：

- ① 手工改坐标值，数据没动，坐标与格点语义错位：

.. code:: python

   ds2 = ds.copy()
   ds2.coords["lat"] = ds2.lat + 100
   print(ds2.lat.values[:5])     # -> [130. 131. ...]  坐标整体平移但数据没动

.. code:: text

   改后 lat: [130. 131. 132. 133. 134.]  (坐标变, 数据没变, 语义错)

- ② 把 data 换成裸 ndarray 后仍拿它当 DataArray 用（坐标其实是假的）：

.. code:: python

   arr_np = temp.values        # 裸 numpy, 无标签
   print(type(arr_np).__name__)   # -> ndarray

.. code:: text

   arr 是 ndarray: ndarray  无坐标标签

**原因**\ ：坐标与数据在 DataArray
里是一对「对齐的内存视图」。你只改坐标、不动数据，整个场的 lat/lon
就整体平移，而温度仍原位——画出来的图经纬度标签全错。把 ``.values``
取出来做计算再塞回去，坐标标签并不会拽着数据一起走，容易造成「数据对了、标签错了」。

**解决办法**\ ：好习惯是「在 DataArray 层面操作」，别轻易 ``.values``
再手动塞回；真要改坐标，用 ``assign_coords``/``coords.update``
并同步改数据数组才安全；取出 ``.values`` 计算后，重新包
``xr.DataArray(result, dims=..., coords=...)`` 或被其维度/坐标。结束后
``print(ds)`` 看一眼「坐标值」与「数据 shape」匹配否。

   **气象场景一句话**\ ：坐标和格点数据像「底图 +
   覆盖层」的精确对位——你光挪底图不改覆盖层，或把覆盖层换成裸图不更新底图，就会印出「温度在
   130°E 结果坐标写的是
   30°」错位图，全程不报警，直到你对着可疑的经纬度标签才惊觉。

--------------

.. _873-惰性加载-open_dataset-与-load只看目录-vs-真正搬到内存:

8.7.3 惰性加载 ``open_dataset`` 与 ``.load()``\ ：只看目录 vs 真正搬到内存
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：\ ``open_dataset``
默认惰性（只读目录），\ ``.load()`` 才真正把数据搬进内存：

.. code:: python

   dsL = xr.open_dataset("northwest_temp.nc")
   print(type(dsL["temp"].data).__name__)      # 惰性时可能是 ndarray(小型)
   dsL.load()
   print(type(dsL["temp"].data).__name__)      # 加载后

.. code:: text

   惰性打开, data 类型: ndarray
   load 后 data 类型: ndarray  shape: (30, 11, 21)

（小型文件没走 Dask 所以数据显示为 ndarray；真正大文件配 ``chunks``
时惰性态会是 dask.array。）

**原因与记忆**\ ：\ ``open_dataset`` 默认不读取全部数据，只把「目录 +
坐标 + 属性」读进来，真正要算时才异步加载。这对 GB 级格点数据极关键——先
``print(ds)`` 看结构再决定取哪些，不会一上来撑爆内存。普通小文件没装
Dask 就直接读了，仍建议养成 ``print(ds)`` 的习惯。

**解决办法**\ ：一切按官方
8.3「惰性加载」套路走：\ ``ds = xr.open_dataset("large.nc", chunks={"time": 10})``
分块惰性加载，\ ``ds.load()`` 显式搬入内存；实在要只取一部分，先
``sel``/``isel`` 缩到小了再 ``.load()``\ ，避免大文件全量载入。

   **气象场景一句话**\ ：\ ``open_dataset``
   惰性加载像「先看地图目录、查明有多少格点变量」，\ ``.load()``
   才是「把成千上万张天气图卷宗全部摊到桌上」——大档案要按需取（\ ``chunks``\ ），别一进门就把整库搬空吞内存。

--------------

.. _874-可能违反检查的静默物理错单位没转-kc-就统计出图:

8.7.4 可能违反检查的静默物理错：单位没转 K→C 就统计/出图
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：再分析气温默认开尔文 K，模仿文件 temp 单位是
``K``\ ，首个值
``~12.46 K``\ （小模型片段，数值示意）。你若直接统计/出图而不减
273.15，数值整体离谱：

.. code:: python

   print(ds["temp"].attrs.get("units"))            # -> K
   print(float(temp.isel(time=0, lat=0, lon=0).values), "K")     # 原始 K
   c = temp - 273.15
   print(float(c.isel(time=0, lat=0, lon=0).values), "C")        # 转 C 后

.. code:: text

   temp 单位: K  首个值: 12.46058085... K
   转 C 后首个值: -260.689419... C

**原因与坑**\ ：8.10 与最佳实践双双点名：再分析资料气温大多是\ **开尔文
K**\ ，转摄氏度要先 ``-273.15``\ 。忘转直接算平均/画图，整体差出
273.15，图虽“平滑”但全是错的——这是第 3 类静默错误的典型。

**解决办法**\ ：接数据先 ``print(ds["temp"].attrs.get("units"))``
确认单位；是 K 就 ``temp = temp - 273.15``\ （必要时算完再
``assign_attrs({"units":"degC"})`` 标注）；做完立刻
``print(temp.min(), temp.max())`` 自查——气温应落在约 -40 ~
+50℃，若显示早在 230K~330K 那就是没转。

   **气象场景一句话**\ ：开尔文转摄氏度就像「华氏/摄氏」的单位校对——拿到
   ERA5 的 285K 直接当 ℃ 画图，整幅图就是“夏天零下 12℃”的鬼图。先看
   attrs 里的 units，先减 273.15 再到统计/绘图，是气象数据的第一道守门。

--------------

.. _875-区域平均漏加纬向权重-coslat--高纬网格权重虚高静默系统偏差:

8.7.5 区域平均漏加纬向权重 ``cos(lat)`` → 高纬网格权重虚高（静默系统偏差）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 正确做法**\ ：第 8.8
最佳实践反复强调：直接算术平均会高估高纬（网格多但面积小）贡献，必须用
``cos(lat)`` 加权：

.. code:: python

   w = np.cos(np.deg2rad(ds.lat))          # 纬度权重 (lat,)
   w2 = w.broadcast_like(ds["temp"])       # 铺到 (time, lat, lon)
   avg = ds["temp"].weighted(w2).mean(dim=["lat","lon"])
   print("weighted mean shape:", avg.shape, " 首值:", float(avg.values[0]))

.. code:: text

   broadcast_like 后 shape: (30, 11, 21)
   weighted mean shape: (30,)  首值: 12.198558...

**原因与坑**\ ：地球是球体，同一经度间距在高纬的球面宽度更小，网格面积正比于
``cos(lat)``\ 。直接
``np.mean``\ （算术平均）把每一格当等面积，高纬格点权重虚高，区域平均产生系统偏差。这是气象格点分析最常见的错误之一。

**解决办法**\ ：用 ``.weighted(np.cos(np.deg2rad(lat)))``
求加权平均（\ ``.mean(dim=[...])``\ ）。注意权重必须与 lat
对齐、不含缺失；用 ``broadcast_like`` 铺到数据形状，权重数组必须是无 NaN
的（见 8.7.6）。

   **气象场景一句话**\ ：同一份经纬网，赤道一格摊着大片海面，高纬一格却挤得只有一小条地——算术平均把高纬那“小格”当“大格”算，就像拿不同大小的秤砣却按等重记，区域平均必然偏心高纬。\ ``cos(lat)``
   加权是把每一个纬度带的“真实面积”给正回来。

--------------

.. _876-weighted-权重里含-nan--valueerror报错反而救你:

8.7.6 ``weighted()`` 权重里含 NaN → ``ValueError``\ （报错，反而救你）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ ：权重数组混进 NaN（漏测），xarray 的
``weighted`` 会拦截而不是闷算：

.. code:: python

   w = np.cos(np.deg2rad(ds.lat))
   w = xr.where(ds.lat > 38, np.nan, w)     # 高纬权重变 NaN
   ds["temp"].weighted(w).mean(dim=["lat","lon"])

.. code:: text

   ValueError: `weights` cannot contain missing values. Missing values can be replaced by `weights.fillna(0)`.

**原因**\ ：权重含 NaN 时，加权统计无法确定 NaN 格点权重，结果会被 NaN
污染。Xarray 明确抛 ``ValueError`` 并\ **贴心给出修法**\ 「用
``weights.fillna(0)`` 替换缺测」——这正是第 8.8 官方示例
``weights.fillna(0)`` 的来历。

**解决办法**\ ：\ ``weights = weights.fillna(0)`` 再
``weighted(weights)``\ ；或先把缺测纬度权重置
0（等价于不贡献面积）。这一条是「报错商良」的典型——报错直接告诉你下一步怎么救，照做即可。

   **气象场景一句话**\ ：权重缺测就像某条纬带面积未知——你要分子（加权求和）没有分母的权重都配不平，xarray
   宁可喊停（cannot contain missing
   values）也不让你用带洞的面积去平均；填
   0（fillna(0)）表示“这条带面积算 0 不参与”，平均才成立。

--------------

.. _877-权重-1d-维度名与数据不匹配--静默返回奇怪形状不报错但结果可疑:

8.7.7 权重 1D 维度名与数据不匹配 → 静默返回奇怪形状（不报错，但结果可疑）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：给 ``weighted``
传一个「长度碰巧对、但维度名不同」的权重，不报错，返回一个多了个
``wrongdim`` 的怪形状：

.. code:: python

   w_bad = xr.DataArray(np.ones(11), dims="wrongdim")   # 长度 11 == lat 长度, 但维名错
   avg2  = ds["temp"].weighted(w_bad).mean(dim=["lat","lon"])
   print("weighted bad-dim 结果 dims:", avg2.dims)      # -> ('time','wrongdim')

.. code:: text

   weighted with bad dim 结果: ('time', 'wrongdim')

**原因与坑**\ ：\ ``weighted``
会把权重按维度名对齐；维度名对不上时，它会\ **当作不同维**\ 而静默铺开 +
平均，于是在结果里留下一个不该存在的 ``wrongdim``
维。这不报错，但说明权重根本没跟你想要的 lat 对上，结果是虚构的。

**解决办法**\ ：权重一定用它目标数据同名的维（如
``dims="lat"``\ ）。写完 ``.weighted(w)`` 后
``print(avg.dims)``\ ，若多出非预期维名（\ ``wrongdim``
之类），就是权重维名写错了。\ **凡 multi-dim
都有同样的验证纪律：print(dims) 是最后的审判**\ 。

   **气象场景一句话**\ ：你把一维权重命名成 ``wrongdim``
   塞给加权——长度虽巧合一模一样，可它认的是维度名不是长度，于是它把
   ``wrongdim``
   当成另一根多出来的轴铺开，最后给你一个多必的轴。数轴名（dims）永远比数格数（shape）可靠。

--------------

.. _878-drop_vars-与-drop_sel-混淆丢坐标-vs-丢坐标值维度成员:

8.7.8 ``drop_vars`` 与 ``drop_sel`` 混淆（丢坐标 vs 丢坐标值/维度成员）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ ：

.. code:: python

   r1 = ds.drop_vars("lat")              # 丢掉 lat 这个坐标
   print("drop_vars 后 lat 还在?", "lat" in r1.coords)     # -> False
   r2 = ds.drop_sel(time="2024-01-01")   # 去掉 2024-01-01 这一天的所有数据
   print("drop_sel 后 time len:", r2.sizes["time"])          # -> 29

.. code:: text

   drop_vars('lat') 后 coords 还有 lat? False
   drop_sel 后 time len: 29

**原因与区别**\ ：

- ``drop_vars("lat")``\ ：\ **按名字丢掉一个变量/坐标**\ （把 lat
  这条轴从 coords 移除）；
- ``drop_sel(time="2024-01-01")``\ ：\ **按坐标值丢掉那一条记录**\ （把这一天从
  time 轴上剔除）。

混用后果：既想省内存丢坐标、又想同日剔除数据，新手容易写反——``drop_vars(time="2024-01-01")``
会把 ``time`` 当作「变量名」去找，找不到就报 ``KeyError`` 或啥都不删。

**越界 drop 的真实报错**\ ：\ ``drop_sel`` 删一个不存在的坐标值会报：

.. code:: python

   ds.drop_sel(lat=100)          # lat 范围 30-40, 100 不存在

.. code:: text

   KeyError: '[100] not found in axis'

**解决办法**\ ：\ ``drop_vars`` +
名字（删变量/坐标本体）；\ ``drop_sel`` / ``drop_isel`` +
标签/序号（删同维上的某些记录）。删之前确认标签存在，否则会
``not found in axis``\ 。

   **气象场景一句话**\ ：drop_vars
   是「把这把尺（相坐标）收起来」，drop_sel
   是「把尺上的某一刻度（某天）划掉再进一步平均」——一个删尺子，一个删刻度，别把“去掉第
   1
   天数据”写成“drop_vars(‘time’)”，那样不是删时刻而是企图删时间维本体。

--------------

.. _88-综合对照常见我以为是-a-结果却是-b的静默错位速查:

8.8 综合对照：常见“我以为是 A 结果却是 B”的静默错位速查
-------------------------------------------------------

以下都是「程序正常结束、结果却不对」的静默陷阱，专门供你练习“尾部报警”。

+----------------+----------------------------------+--------------------------------------+----------------------------------+
| 你想做         | 你写成了                         | 静默后果                             | 正确写法                         |
+================+==================================+======================================+==================================+
| 取第 0 时次    | ``temp.sel(time=0)``             | ``KeyError``\ （time 坐标为日期，无  | ``temp.isel(time=0)``            |
|                |                                  | 0 标签）                             |                                  |
+----------------+----------------------------------+--------------------------------------+----------------------------------+
| 取 2024-01-15  | ``temp.isel(time="2024-01-15")`` | ``IndexError``/``TypeError``\ （isel | ``temp.sel(time="2024-01-15")``  |
|                |                                  | 要序号）                             |                                  |
+----------------+----------------------------------+--------------------------------------+----------------------------------+
| 取最接近某时刻 | ``temp.sel(time="...12:00")``    | ``KeyError``\ （无精确值）           | 加 ``method="nearest"``          |
+----------------+----------------------------------+--------------------------------------+----------------------------------+
| 逐时刻区域平均 | ``temp.mean()``                  | 全场压成标量                         | ``temp.mean(dim=["lat","lon"])`` |
+----------------+----------------------------------+--------------------------------------+----------------------------------+
| 存整型省空间   | 直接                             | ``SerializationWarning`` + NaN       | 补 ``"_FillValue": -9999``       |
|                | ``encoding={"dtype": "int16"}``  | 变垃圾                               |                                  |
+----------------+----------------------------------+--------------------------------------+----------------------------------+
| 单位转换       | 拿了 K 直接统计                  | 整体差 273.15                        | 先 ``-273.15``                   |
+----------------+----------------------------------+--------------------------------------+----------------------------------+
| 加权平均       | ``np.mean``                      | 高纬权重虚高                         | ``.weighted(cos(lat))``          |
+----------------+----------------------------------+--------------------------------------+----------------------------------+
| 删某天         | ``drop_vars(time=...)``          | ``KeyError`` 或没作用                | ``drop_sel(time=...)``           |
+----------------+----------------------------------+--------------------------------------+----------------------------------+
| 读 GRIB        | 直接 ``open_dataset``            | ``did not find a match...``          | 装 cfgrib + ``engine="cfgrib"``  |
+----------------+----------------------------------+--------------------------------------+----------------------------------+

--------------

.. _89-本章高频速查表关键词--原因:

8.9 本章高频速查表（关键词 → 原因）
-----------------------------------

+--------------------------+---------------------------------------------------------------+---------------+
| 记一记                   | 关键词 → 原因                                                 | 对应条目      |
+==========================+===============================================================+===============+
| 文件路径不存在           | ``FileNotFoundError: ... no_such_file.nc``                    | 8.1.1         |
+--------------------------+---------------------------------------------------------------+---------------+
| 缺 netCDF4/h5py 库       | ``ImportError: No module named 'h5py'``                       | 8.1.2         |
+--------------------------+---------------------------------------------------------------+---------------+
| 读 GRIB 缺 cfgrib        | ``No module named 'cfgrib'`` /                                | 8.1.3 / 8.1.5 |
|                          | ``unrecognized engine 'cfgrib'``                              |               |
+--------------------------+---------------------------------------------------------------+---------------+
| 文件不是 NetCDF          | ``-51 Unknown file format`` / ``not a valid NetCDF 3 file``   | 8.1.4         |
+--------------------------+---------------------------------------------------------------+---------------+
| 缺 zarr 库用 Zarr        | ``The zarr package is required``                              | 8.1.6         |
+--------------------------+---------------------------------------------------------------+---------------+
| sel 用整数/标签不存在    | ``KeyError: "not all values found in index '...'"``           | 8.2.1 / 8.2.3 |
+--------------------------+---------------------------------------------------------------+---------------+
| isel 用标签/日期         | ``IndexError ... out of bounds`` /                            | 8.2.2         |
|                          | ``invalid indexer array, does not have integer dtype``        |               |
+--------------------------+---------------------------------------------------------------+---------------+
| sel 无精确值加 method    | ``method='nearest'`` 消 KeyError                              | 8.2.4         |
+--------------------------+---------------------------------------------------------------+---------------+
| 时间区域切片 inclusive   | 版本敏感，\ ``inclusive`` 可能 ``KeyError`` /                 | 8.5.4         |
|                          | 边界含不含需自测                                              |               |
+--------------------------+---------------------------------------------------------------+---------------+
| sel 变量名 temp          | ``KeyError: "'temp' is not a valid dimension or coordinate"`` | 8.4.1         |
+--------------------------+---------------------------------------------------------------+---------------+
| groupby 不存在维         | ``KeyError: "No variable named 'station' ... include [...]"`` | 8.3.6         |
+--------------------------+---------------------------------------------------------------+---------------+
| swap_dims 误用           | ``replacement dimension ... is not a 1D variable along ...``  | 8.3.1         |
+--------------------------+---------------------------------------------------------------+---------------+
| dims                     | 静默对齐，范围不同才补 NaN                                    | 8.3.3 / 8.3.7 |
| 顺序不影响加法（对齐）   |                                                               |               |
+--------------------------+---------------------------------------------------------------+---------------+
| 同维名长度冲突           | ``AlignmentError ... conflicting dimension sizes: {5, 7}``    | 8.3.5         |
+--------------------------+---------------------------------------------------------------+---------------+
| 忘写 dim 求均值          | 静默压成标量                                                  | 8.7.1         |
+--------------------------+---------------------------------------------------------------+---------------+
| 坐标与数据脱钩           | 静默，图错/标签错                                             | 8.7.2         |
+--------------------------+---------------------------------------------------------------+---------------+
| 单位 K→C 没转            | 静默相差 273.15                                               | 8.7.4         |
+--------------------------+---------------------------------------------------------------+---------------+
| 区域平均没加权           | 静默高纬虚高                                                  | 8.7.5         |
+--------------------------+---------------------------------------------------------------+---------------+
| weighted 权重含 NaN      | ``ValueError: weights cannot contain missing values``         | 8.7.6         |
+--------------------------+---------------------------------------------------------------+---------------+
| to_netcdf 目录不存在     | ``PermissionError [Errno 13]``                                | 8.6.1         |
+--------------------------+---------------------------------------------------------------+---------------+
| to_netcdf 引擎名错       | ``unrecognized engine for to_netcdf: '...'``                  | 8.6.2         |
+--------------------------+---------------------------------------------------------------+---------------+
| 浮点存整型没缺测哨兵     | ``SerializationWarning ... without any _FillValue``           | 8.6.4         |
+--------------------------+---------------------------------------------------------------+---------------+
| drop_vars vs drop_sel    | 一个删坐标/变量、一个删记录                                   | 8.7.8         |
+--------------------------+---------------------------------------------------------------+---------------+
| resample 频率串错        | ``ValueError: Invalid frequency: MX``                         | 8.5.2         |
+--------------------------+---------------------------------------------------------------+---------------+
| resample 旧写法 M/Y      | ``FutureWarning: 'M' ... use 'ME'``                           | 8.5.3         |
+--------------------------+---------------------------------------------------------------+---------------+

..

   **收尾口诀（气象风）**\ ：\ ``sel`` 用坐标值、\ ``isel``
   用序号；\ ``mean`` 一定要带 ``dim``\ ；区域平均必须 ``cos(lat)``
   加权、单位先减 273.15、坐标先对 ``dims`` 再对
   ``shape``\ ；缺引擎先装库再看 code——凡是静默的（忘
   dim、单位不转、坐标脱钩、加权缺席、加权数组维度名错）都是格点分析最大的隐形杀手。看到
   ``print(da)`` 多读一眼，能救你好几天的火。
