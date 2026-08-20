Python 简介及安装环境 Q&A
===============================

   **章节定位**\ ：第 1 章（模块一 · 环境搭建）· 对应用户指南
   ``user_guide/basics/python_conda.rst`` **通用排错方法论**\ ：先读
   :doc:`00-通用排错指南 </qa/basics/00-通用排错指南>`\ ，把「报错 → 关键词 →
   原因联想」的肌肉记忆练起来；本章是第 1 章的可检索详细清单。

   **关于本文例子怎么来的**\ ：本章「现象」里凡是 Python
   报错，一律在本机 Python 环境真实跑过，Traceback
   原文照抄。凡是\ **装包 / 建环境 /
   网络下载**\ 这类会写入环境/联网的操作，需要你在自己的 conda
   环境里亲自验证，故相关条目标注
   **（环境操作，需在本机执行）**\ ，并附上真实、可搜索的关键报错文本——照抄去搜即可命中。

   **太长不看的一句话**\ ：第 1 章 80%
   的错误就三类——**「包没装对地方」**\ （\ ``ModuleNotFoundError``\ ）、\ **「命令没找到」**\ （\ ``command not found / 不是内部或外部命令``\ ）、\ **「装包/网络没通」**\ （\ ``PackagesNotFoundError``\ 、超时、SSL）。下面一个个拆。

--------------

.. _10-本章报错总览表:

1.0 本章报错总览表
------------------

+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| #  | 报错关键词（可搜索）                                                                      | 一句话原因                             | 对应条目 |
+====+===========================================================================================+========================================+==========+
| 1  | ``ModuleNotFoundError: No module named 'xxx'``                                            | 包没装 / 没 ``conda activate``         | §1.1.1   |
|    |                                                                                           | 到装了它的环境 / 名字拼错              |          |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 2  | ``ModuleNotFoundError``\ （明明装过却报没装）                                             | 用错了解释器（\ ``where python``       | §1.1.2   |
|    |                                                                                           | 与装包的 python 不是同一个）           |          |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 3  | ``ModuleNotFoundError: No module named 'nyumpy'``                                         | 库名 / 别名拼写错误                    | §1.1.3   |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 4  | ``NameError: name 'np' is not defined``                                                   | 用了 ``np`` 忘了                       | §1.1.4   |
|    |                                                                                           | ``import numpy as np``                 |          |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 5  | ``python`` / ``python3`` 版本对不上（\ ``where python``\ ）                               | PATH 里同时有多个                      | §1.1.5   |
|    |                                                                                           | python，命令解析到了别的版本           |          |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 6  | VS Code 里 import 失败，终端却可以                                                        | **解释器选错**\ ，VS Code 用的不是     | §1.1.6   |
|    |                                                                                           | ``met_p312``                           |          |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 7  | ``'jupyter' 不是内部或外部命令`` / command not found                                      | 没装 jupyter / 没激活环境 / Scripts    | §1.2.1   |
|    |                                                                                           | 没进 PATH                              |          |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 8  | ``'conda' 不是内部或外部命令``                                                            | PATH 未勾选 / 没 ``conda init``        | §1.2.2   |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 9  | ``Python was not found; run without arguments``                                           | 只装了微软商店版，App 执行别名坑       | §1.2.3   |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 10 | ``The term 'xxx' is not recognized...`` / 拼错命令                                        | 命令名 / 前缀拼写错误                  | §1.2.4   |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 11 | ``conda install jupyter-notebook`` → ``PackagesNotFoundError``                            | 包名不对，Jupyter 的包名是 ``jupyter`` | §1.3.1   |
|    |                                                                                           | / ``notebook``                         |          |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 12 | ``PackagesNotFoundError: The following packages are not available from current channels`` | 第三方库装了默认 channel 没有，得加    | §1.3.2   |
|    |                                                                                           | ``-c conda-forge``                     |          |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 13 | ``conda create -n xx python=3.12`` 的各种参数坑                                           | 语法 / 环境名 / Python 版本写法不对    | §1.3.3   |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 14 | 下载慢 / 超时 / ``http 000`` / ``CondaSSLError``                                          | 境外官方源慢、代理 / SSL、未配镜像     | §1.3.4   |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 15 | ``Solving environment`` 卡死 / ``priority`` 冲突                                          | 依赖解析空间爆炸、channel 优先级没设好 | §1.3.5   |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 16 | ``（无报错）装完包 import 仍失败``                                                        | pip 装到了另一个 python 的环境（串台） | §1.4.1   |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 17 | ``UnicodeDecodeError`` / 中文路径乱码                                                     | 用户名 / 路径含中文、空格、括号        | §1.4.2   |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+
| 18 | ``conda list`` / ``conda env list`` / ``import sys``                                      | 「排查三件套」：先确认装在哪、跑在哪个 | §1.5.1   |
+----+-------------------------------------------------------------------------------------------+----------------------------------------+----------+

--------------

.. _11-环境激活与解释器错位modulenotfounderror-家族:

1.1 环境激活与解释器错位（\ ``ModuleNotFoundError`` 家族）
----------------------------------------------------------

   这一节解决第 1 章最经典的「\ **明明装过却 import
   不了**\ 」。根因只有一个：\ **你正在用的 Python
   解释器，跟当初装包的是不是同一个？** 第 0
   篇的顶层异常树里，\ ``ModuleNotFoundError`` 挂在 ``ImportError``
   之下，一看就联想「没装 / 没激活 / 拼错」。本机有两个 python
   这个事实（\ ``python`` 默认是系统 3.10，气象库在
   met_p312（3.12）），正好把它讲透。

.. _111-modulenotfounderror-no-module-named-rioxarray--包压根没装到这个环境:

1.1.1 ``ModuleNotFoundError: No module named 'rioxarray'`` —— 包压根没装到这个环境
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ （在 met_p312 环境直接 import
一个没装的库，Traceback 原文）：

.. code:: text

   Traceback (most recent call last):
     File "...\sim\ch01\_tmp_m1.py", line 2, in <module>
       import rioxarray
   ModuleNotFoundError: No module named 'rioxarray'

..

   注意第 0 篇口诀：\ **从下往上读**\ 。最后一行 ``ModuleNotFoundError``
   是主菜，\ ``line 2`` 是坐标，\ ``import rioxarray``
   是现场。这表示「Python
   在它的安装目录清单（\ ``sys.path``\ ）里翻了个底朝天，也没找到叫
   ``rioxarray`` 的模块」。

**原因** 三种可能，按概率排：

1. 这个包从来没装进你当前的 conda 环境；
2. 你 ``conda activate`` 到了 A 环境，却在一个没这个包的 B 环境（或
   base）里运行；
3. 你想装的其实是 ``rioxarray``\ ，但装的是别的（名字对不上）。

**解决办法**\ （先确认在哪个环境）：

.. code:: bash

   conda env list                 # 看现在激活的是哪一个（前面带 * 号）
   conda activate met_p312        # 激活到你装包的那个环境
   conda list | findstr rioxarray # 或 conda list ripgrep 验证
   conda install -c conda-forge rioxarray
   python -c "import rioxarray; print('ok')"   # 装完必须再验一遍

**核对命令**\ ：\ ``python -c "import sys; print(sys.executable)"`` —
输出应指向 ``...\envs\met_p312\python.exe`` 而不是系统 python。

   **气象场景一句话**\ ：就像「你要的兰州站逐日气温文件存在
   ``met_p312/`` 这台实验室机器上，可你却跑到了 ``base/``
   那台没有这份数据的机器上去读」——不是数据丢了，是\ **你站错了机器（环境）**\ 。站点数据（包）都在，只是通道（PATH）没指对。

--------------

.. _112-modulenotfounderror-明明装过包却报没装--用错了解释器没-activate-到装了包的环境:

1.1.2 ``ModuleNotFoundError`` 明明装过包却报没装 —— 用错了解释器（没 activate 到装了包的环境）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ （本机 ``geopandas`` 只装进 met_p312，用默认
``python``\ (3.10) 去 import，实测原文）：

.. code:: text

   解释器: ...\py3.10\python.exe 3.10.11
   Traceback (most recent call last):
     File "...\sim\ch01\_tmp_m4.py", line 3, in <module>
       import geopandas
   ModuleNotFoundError: No module named 'geopandas'

而同一个文件切到
met_p312（\ ``...\envs\met_p312\python.exe``\ ）就能正常
``import``\ 。\ **报错前后，包都在，只是「跑代码的解释器」不对。**

**原因** 一句话：\ **``python``
这个命令实际指向的解释器，跟「装包的那个解释器」不是同一个**\ 。本机验证
``where python`` 输出（实测原文）：

.. code:: text

   ...\py3.10\python.exe    # ← 默认 python=3.10
   ...\py3.10\bin\python.exe
   ...\envs\base\python.exe                      # ← base
   C:\Users\<你的用户名>\AppData\Local\Microsoft\WindowsApps\python.exe   # ← 微软商店别名

PATH 里一堆 ``python.exe``\ ，\ ``where python``
取\ **最前面那个**\ 。而 ``...\envs\met_p312\python.exe`` 是 3.12 ——
**它根本不在默认 PATH 里**\ 。所以你没有 ``conda activate met_p312``
就跑，\ ``python`` 优先级排到系统 3.10，自然找不到包。

**解决办法**

.. code:: bash

   # 1) 永远是先激活再跑
   conda activate met_p312
   python --version                          # 应显示 3.12.x
   python -c "import geopandas; print('ok')"

   # 2) 或直接指定解释器路径（有多个 python 时的兜底）
   ...\envs\met_p312\python.exe 你的脚本.py

**校验法宝（记一辈子）**\ ：报\ ``ModuleNotFoundError``\ 先跑
``where python``\ （Windows）/ ``which python``\ （Linux/macOS），再跑
``python -c "import sys;print(sys.executable)"``\ ，跟装包时的路径比对。两者一致才算「解释器是对的」。

   **气象场景一句话**\ ：一场台风需要 GPS
   探空和自动站两套数据融合。你发现在 FACT(自动站)
   上读不到探空——不是探空丢了，是你\ **连的是 FACT，不是
   GPS**\ 。\ ``where python``
   就是你的「数据源清单」，先看清楚自己连的是哪台设备再骂数据。

--------------

.. _113-modulenotfounderror-no-module-named-nyumpy--库名--别名拼写错误:

1.1.3 ``ModuleNotFoundError: No module named 'nyumpy'`` —— 库名 / 别名拼写错误
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ （把 numpy 记成 nyumpy，本机实测原文）：

.. code:: text

   Traceback (most recent call last):
     File "...\sim\ch01\_tmp_m3.py", line 2, in <module>
       import nyumpy as np
   ModuleNotFoundError: No module named 'nyumpy'

**原因**
纯手滑：库名拼错（\ ``numpy→nyumpy``\ ）、或记了习惯的大小写（\ ``matplotlib→matplotlip``\ 、\ ``xarray→xarr``\ ）。第
0 篇说过，\ ``ModuleNotFoundError``
一级就联想「名字」。\ **注意：\ ``import numpy as nyumpy``
那种把「别名」写错，报的是 ``AttributeError``
或正常运行但名字引用不到；而 ``import nyumpy``
这种「模块名」写错，报的才是 ``No module named``\ 。**

**解决办法**

.. code:: python

   import numpy as np           # 库名 numpy 正确，别名 np 你想叫啥都行

善用 Tab 补全 / 搜索引擎复制库名，不手打。也可以 ``conda list``
看它到底写着什么名。

   **气象场景一句话**\ ：报站名写错「兰州」变「兰州(机场)」，雷达资料系统当然查无此站。模块名也是「站号」，抄准了再查。

--------------

.. _114-nameerror-name-np-is-not-defined--用了-np-却忘-import-numpy:

1.1.4 ``NameError: name 'np' is not defined`` —— 用了 ``np`` 却忘 ``import numpy``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实报错信息**\ （本机实测原文，注意新版 Python 还贴心画了个
``^^`` 箭头指出是那段代码）：

.. code:: text

   Traceback (most recent call last):
     File "...\sim\ch01\_tmp_m2.py", line 2, in <module>
       arr = np.array([285.0, 288.2, 290.5])
             ^^
   NameError: name 'np' is not defined

**原因** ``NameError`` 在异常树里属于「名称/引用」类（见 00
篇），意思是\ **这个名字 ``np`` 从来没人定义过**\ 。这里 ``np`` 是 numpy
的别名，不先写出 ``import numpy as np`` 这一行，\ ``np``
就不存在。它是「别名没建」，不是「numpy 没装」。

**注意区分**\ （对照复习）：

- ``NameError: name 'np' is not defined`` → **忘写
  ``import numpy as np``**\ （本章重点）。
- ``ModuleNotFoundError: No module named 'numpy'`` → numpy
  压根没装/没激活（见 §1.1.1）。
- ``NameError: name 'nmp' is not defined`` → 别名叫错：应
  ``as np``\ ，你却写 ``as nmp``\ ，那 ``np`` 自然没定义。

**解决办法**\ ：文件最顶部先写：

.. code:: python

   import numpy as np

..

   **气象场景一句话**\ ：\ ``np``
   相当于观测资料的「快捷通道编号」，你不先开通道（import），去调用
   ``np.array``
   就等于对着空气喊站在隔壁的同事——当然找不到这个人（NameError）。资料在，通道没开。

--------------

.. _115-同时有-python-和-python3用了错的命令--path-顺序错乱:

1.1.5 同时有 ``python`` 和 ``python3``\ ，用了错的命令 / PATH 顺序错乱
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ （本机实测）：

- ``python --version`` → ``Python 3.10.11``\ （PATH 里第一个是系统
  python）
- ``...\envs\met_p312\python.exe --version`` → ``Python 3.12.12``
- ``where python`` 列出 4 个 python.exe（见 §1.1.2），\ ``where``
  取最前面一个。

也就是说\ **同一个 ``python``
命令，在不同终端/不同时刻可能指向不同解释器**——这就是「昨天还能跑，今天
import 失败」的元凶之一。

**原因** Windows 上 ``python``,\ ``python``\ （launcher
``py.exe``\ ）、微软商店别名、conda 的 python 全都叫
``python.exe``\ ，谁在 PATH 前面谁赢；部分机器还区分 ``python`` /
``python3``\ （\ ``python3`` 在 Linux/macOS 是标准名，Windows
上常没有或映射到同名）。

**解决办法**

1. 统一用 ``conda activate met_p312`` 后再 ``python``\ ，让 conda
   把该环境排到 PATH 最前；
2. 想查清现在是哪个：\ ``where python`` →
   看路径；\ ``python -c "import sys;print(sys.version)"`` → 看版本；
3. 别在两个「我都觉得对」的解释器之间来回 ``python``/``python3``
   碰运气，\ **先把 PATH 理顺**\ 。

..

   **气象场景一句话**\ ：兰州站和榆中站的自动站，站点代码都叫「LZ」开头的自动站，只写着
   ``python`` 你到底连哪台的传感器？\ ``where python`` = 站点 ID
   对照表，先把名字对应清楚再采数。

--------------

.. _116-vs-code-里明明装了包还是-modulenotfounderror--解释器选错:

1.1.6 VS Code 里明明装了包还是 ``ModuleNotFoundError`` —— 解释器选错
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象** 在终端 ``conda activate met_p312`` 后 ``python`` 能
import；但转到 VS Code 点运行就报
``ModuleNotFoundError: No module named 'cartopy'``\ 。\ **同一份代码、同一个环境，两个地方表现不一样。**

**原因** VS Code 的「Python
解释器」是\ **每个工作区独立记忆**\ 的。你之前在别处按过选择解释器，它记的可能是系统
python 或 base，而不是 ``met_p312``\ 。VS Code 用的 python 和终端
activate 的那个\ **不是同一个**\ ，包自然「失踪」。

**解决办法**

.. code:: text

   1. 打开任意 .py 文件；
   2. 按 Ctrl+Shift+P → 输入 "Python: Select Interpreter"；
   3. 选择 met_p312 (Python 3.12.x)；
   4. 看左下角状态栏：出现 "met_p312" 字样 = 绑定成功。

装完包后在 VS Code 里 ``print(sys.executable)`` 复核输出是否为
``...envs\met_p312\python.exe``\ 。

   **气象场景一句话**\ ：数据在 FAC 服务器，你的数据浏览器（VS
   Code）默认连的是第 3 台备用机,自然查不到。选解释器 =
   给你的编辑器指一下「该去连哪台」。

--------------

.. _12-命令找不到command-not-found--不是内部或外部命令:

1.2 命令找不到（\ ``command not found`` / 「不是内部或外部命令」）
------------------------------------------------------------------

   这一节全是「在命令行敲一个命令，系统说我不认识你」。第 0 篇 0.6
   节第一次示范的「关键词→联想」就是这一类：\ **``command not found`` /
   ``not recognized`` → 没 activate / 没装 / PATH 没配**\ 。

.. _121-jupyter-不是内部或外部命令--jupyter-command-not-found:

1.2.1 ``'jupyter' 不是内部或外部命令`` / ``jupyter: command not found``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ （本机故意把命令拼错，PowerShell 原文）：

.. code:: text

   jupyter-noteboo : The term 'jupyter-noteboo' is not recognized as the name of a cmdlet, function, script file, or operable program.

在
**cmd**\ （\ ``Win+R``\ →\ ``cmd``\ ，正文里学生用的就是这个）里则显示：

.. code:: text

   'jupyter' 不是内部或外部命令，也不是可运行的程序或批处理文件。

（两者同一回事：操作系统在 PATH 里找不到这个命令。）

**原因** 绝大多数是 **没先 ``conda activate`` 到装 jupyter 的环境/或没装
jupyter**\ ，少数是 Python 的 ``Scripts\`` 目录没进 PATH。\ ``jupyter``
是一个「可执行入口脚本」，它位于
``...\envs\met_p312\Scripts\jupyter.exe``\ ，只有激活该环境后 PATH
里才有它。

**解决办法**

.. code:: bash

   conda activate met_p312            # ① 先激活
   conda install -c conda-forge jupyter   # ② 没有就装（jupyter 是"一本全包"，见 §1.3.1）
   jupyter notebook --no-browser     # ③ 再启动

..

   可以先用 ``where jupyter`` 确认入口脚本在不在，再谈激活的事。

   **气象场景一句话**\ ：\ ``jupyter``
   是你气象实验室的一台「交互式探空气球站」——器材（脚本）都塞在
   ``met_p312`` 仓库里，你从 ``base``
   大门喊它当然不应声。先进仓库（activate）再喊（运行）。

--------------

.. _122-conda-不是内部或外部命令--conda-command-not-found:

1.2.2 ``'conda' 不是内部或外部命令`` / ``conda: command not found``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象** 安装 Miniconda 后，打开 cmd 敲 ``conda --version``\ ，报

.. code:: text

   'conda' 不是内部或外部命令，也不是可运行的程序或批处理文件。

（Linux/macOS 终端为 ``conda: command not found``\ ）

**原因** 两条路都通，缺一不可：

1. 安装勾选里没勾 **Add Miniconda3 to my PATH**\ （正文强调的复选框）→
   conda 的 ``Scripts/``/``condabin/`` 没进 PATH；
2. 装了 PATH 也勾了，但 shell 没执行 ``conda init``\ ，conda
   的激活钩子没装进你的 shell 配置文件（尤其 PowerShell）。

**解决办法**

.. code:: bash

   # ① 若 PATH 根本没勾：重跑安装程序，勾上那两项；或手动把下面三个路径加进 PATH
   #    D:\Software\miniconda3
   #    D:\Software\miniconda3\Scripts
   #    D:\Software\miniconda3\Library\bin
   # ② 若已能敲 conda（在 Anaconda Prompt 里敲得动）：
   conda init powershell        # PowerShell 用户
   # 或
   conda init cmd.exe           # cmd 用户
   # 然后“完全关闭终端、重开一个”再验证：
   conda --version

macOS/Linux：安装后跑 ``conda init bash`` /
``conda init zsh``\ ，关终端重开。

   若 ``conda activate`` 报
   ``Run 'conda init' before 'conda activate'``\ ，多半是 **PowerShell
   执行策略**\ 挡了脚本（报错不带这个真实原因）。执行
   ``Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`` 后重开
   PowerShell 一般即好。

..

   **气象场景一句话**\ ：conda
   是气象实验室的「总控台」，你人站在实验室门口（未进
   PATH）喊台台长，保安不认识你。\ ``conda init``
   就是给系统「办一张门禁卡」，让每个终端都认得这个台长。

--------------

.. _123-python-was-not-found-run-without-arguments-to-install-from-the-microsoft-store:

1.2.3 ``Python was not found; run without arguments to install from the Microsoft Store``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象** 在 cmd 敲
``python``\ ，不报「不是内部或外部命令」，而是弹出这么一句，还可能自动打开微软商店。

**原因** 这是微软商店版 Python 的 **App 执行别名（App Execution
Alias）** 在捣乱：\ ``WindowsApps\python.exe`` 是个「空壳」，真实 Python
没装进 PATH。于是 ``python``
表面「能找到」，实际指向一个转发到商店的占位符。

**解决办法**

.. code:: text

   1. 设置 → 应用 → 可选功能/别名，把「python」「python3」两个执行别名关掉；
   2. 本项目统一用 Miniconda，别去商店装；装好 conda 后 PATH 让 conda 的 python 排前面；
   3. 验证：python --version 应显示 3.12.x 且路径指向 conda 目录。

..

   这与 §1.1.2、§1.2.2 同根：搞清楚 ``python``
   到底指向谁，问题就化解一半。

   **气象场景一句话**\ ：这就像场站里贴了张「观测房」的门牌，但门牌底下其实是空的杂物间（WindowsApps
   空壳），数据自然没有。真实验资料得看去 ``D:\Software\miniconda3``
   那一间。

--------------

.. _124-命令拼写错误-the-term-xxx-is-not-recognized:

1.2.4 命令拼写错误 ``The term 'xxx' is not recognized...``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ （本机把 ``jupyter notebook`` 敲成
``jupyter-noteboo`` 的 PowerShell 原文）：

.. code:: text

   jupyter-noteboo : The term 'jupyter-noteboo' is not recognized as the name of a cmdlet, function, script file, or operable program.

cmd 里对应为：

.. code:: text

   'jupyter-noteboo' 不是内部或外部命令，也不是可运行的程序或批处理文件。

**原因**
命令名/前缀拼错（多一个横线、少一个字母）。\ ``jupyter notebook`` 和
``jupyter-notebook`` 是两个东西——``jupyter notebook`` 是 ``jupyter``
主子命令 + ``notebook`` 子命令；直接敲
``jupyter-notebook``\ （带连字符的可执行入口）也可能存在、但拼错就找不到。

**解决办法**

.. code:: bash

   conda activate met_p312
   jupyter notebook --no-browser     # 正确；注意空格
   # 不要敲 jupyter-noteboo / jumpyter 之类的

..

   **气象场景一句话**\ ：命令就像国际站号（如 52866 兰州、52983
   榆中），少抄一位号，填单（shell）必然查无此站。抄全了再回车。

--------------

.. _13-装包报错conda--pip:

1.3 装包报错（conda / pip）
---------------------------

   第 1 章最大的「挫败感来源」集中在装包。下面几条默认你已经
   ``conda activate`` 到目标环境。凡是会\ **写 conda
   环境**\ 的命令（\ ``conda install``/``conda create``\ ），需要在你自己机器上执行才能验证，故相关条目依据
   **conda 官方文档 / conda-forge / Anaconda 权威资料**
   给出现象与解决，并在条末标注来源供自查。

.. _131-conda-install-jupyter-notebook-报-packagesnotfounderror--包名不对:

1.3.1 ``conda install jupyter-notebook`` 报 ``PackagesNotFoundError`` —— 包名不对
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 /
报错文本**\ （环境操作，依据官方/社区公认形态；来源见文末附注）：

.. code:: text

   PackagesNotFoundError: The following packages are not available from current channels:

     - jupyter-notebook

..

   你可能会想「明明有个 ``jupyter-notebook``
   项目名，怎么就查无此包？」——因为\ **conda
   里的包名不带连字符的短横**\ 。Jupyter 全家桶在 conda 里的正确包名是
   ``jupyter``\ （装笔记簿+内核+全部组件）或单个的 ``notebook``\ 。

**原因** 包名写错。\ ``jupyter-notebook``\ （带连字符）不是官方 conda
包名；conda 包名一般用\ **下划线或不带分隔符**\ （如 ``scikit-learn``
是特例）。

**解决办法**

.. code:: bash

   # 二选一，推荐装全家桶：
   conda install -c conda-forge jupyter          # 一本全包，含 notebook/lab
   # 或只装经典笔记本：
   conda install -c conda-forge notebook

拿不准先搜：\ ``conda search jupyter`` 或上
``anaconda.org``/``conda-forge`` 页面搜包名。

   **气象场景一句话**\ ：就像你想装「西北气温分布图包」，却把包名报成了「西北-气温分布图」（多了连字符）。气象数据集的变量名严格区分符号,对齐变量名词典（conda
   search）再装。

--------------

.. _132-packagesnotfounderror-the-following-packages-are-not-available-from-current-channels--第三方库不加--c-conda-forge:

1.3.2 ``PackagesNotFoundError: The following packages are not available from current channels`` —— 第三方库不加 ``-c conda-forge``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 报错文本**\ （环境操作，依据官方/社区公认形态。』关于默认
channel：标准安装自带的 channels 通常只有 ``main`` /
``defaults``\ ，这类第三方包不在其中，必踩此坑）：

.. code:: text

   PackagesNotFoundError: The following packages are not available from current channels:

     - cartopy
     - geopandas
     - rioxarray
     - netcdf4

**原理**\ ：默认 channels（\ ``main``/``defaults``\ ，或只配了清华
``pkgs/main``\ ）里\ **没有**\ 这些地理/气象扩展包，它们住在
**conda-forge** 仓库。conda 找不到合适的包就抛
``PackagesNotFoundError``\ 。

**解决办法（多举几个具体例子）**

.. code:: bash

   # 方式一：单条加 -c conda-forge（推荐，最干净）
   conda install -c conda-forge cartopy
   conda install -c conda-forge geopandas
   conda install -c conda-forge rioxarray netcdf4

   # 方式二：想让以后默认就搜 conda-forge（一劳永逸），在 .condarc 里加 channel + 设优先级
   conda config --add channels conda-forge
   conda config --set channel_priority strict     # strict=优先 conda-forge，减少冲突
   conda config --set show_channel_urls yes

试试搜一下确认包在不在
conda-forge：\ ``conda search -c conda-forge rioxarray``\ 。

   **气象场景一句话**\ ：\ ``PackagesNotFoundError``
   就像你在「国家气象站编排目录」里查「地面自动站」，天呀默认目录只挂「国家站」，自动站得去另一个专册（conda-forge）查。翻对册子（加
   ``-c conda-forge``\ ）就有。

--------------

.. _133-conda-create--n-xx-python312-的参数坑:

1.3.3 ``conda create -n xx python=3.12`` 的参数坑
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 常见报错**\ （环境操作，依据 conda 官方案例的公认形态）：

.. code:: text

   CondaValueError: The target prefix is the base prefix.  (给环境名加 '-p'/'--prefix' 误用)
   CondaValueError: could not parse environment name 'met_p312' (语法残缺常见)
   InvalidSpec: Spec error 'python 3.12'  (缺 `=`，写成空格)

**原因**\ （逐一拆解「参数坑」）

- ``/`` 与 ``\``\ ：有些同学把 ``-``\ （短横）敲成 ``-``\ 没问题，但把
  ``-n`` 记成 ``-p``\ （\ ``--prefix``
  是“按路径建环境”），\ ``--prefix``/``-p``
  需要的是路径，给了名字就报错；
- ``python=3.12``\ ：注意是\ **等号** ``=`` 不是空格。\ ``python 3.12``
  会被解析成两个包？不认识，报 InvalidSpec；
- 环境名大小写：conda 环境名\ **大小写敏感但要一致**\ ，\ ``Met_p312``
  和 ``met_p312`` 是不同环境，\ ``conda activate met_p312`` 找不到
  ``Met_p312`` 会报 ``EnvironmentNameNotFound``\ ；
- ``-c conda-forge`` 若跟在 create
  后面：\ ``conda create -n xx -c conda-forge python=3.12``\ （channel
  写在前面）。

**解决办法（正文标准写法）**

.. code:: bash

   conda create -n met_p312 python=3.12     # 正确：-n 环境名，python=3.12 用等号
   conda activate met_p312
   conda env list                            # 验证建好了

..

   若报
   ``EnvironmentNameNotFound: Could not find conda environment: xxx``\ ，就是
   **activate 时环境名拼错 / 环境没建成**——先 ``conda env list``
   看真实名字列表（见 §1.5.1）。

   **气象场景一句话**\ ：\ ``conda create``
   相当于在机房\ **划分出一台专机**\ 给气象项目（\ ``python=3.12``
   是这台机预装的操作系统版本号）。写混了 ``-p``/``-n``\ 、把 ``=``
   打成空格，就等于把划分单填错——机房说你格式不对（InvalidSpec），或者根本找不到你写的这台机。

--------------

.. _134-下载慢--超时--http-000--condasslerror--境外源与代理ssl:

1.3.4 下载慢 / 超时 / ``http 000`` / ``CondaSSLError`` —— 境外源与代理/SSL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 报错文本**\ （网络操作，依据官方/社区公认形态）：

.. code:: text

   Could not connect to https://repo.anaconda.com
   CondaHTTPError: HTTP 000 CONNECTION FAILED for url <https://...> Unable to connect
   CondaSSLError: OpenSSL SSL_connect: Connection reset by peer
   ReadTimeoutError / 下载突然卡住

**原因**

1. 官方仓库 ``repo.anaconda.com`` 在境外，直连慢/超时；
2. 校园网/代理环境没配，conda 连不上；
3. 代理证书导致 SSL 握手失败；镜像源地址敲错（清华/中科大）。

**解决办法**\ （正文给的清华镜像，照此即可）

.. code:: bash

   # 1) 配置镜像通道（无极；清华 tuna）
   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
   conda config --set show_channel_urls yes
   # 也推荐中科大镜像仓库（秤 conda-forge 也镜像吧）
   conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
   conda config --add channels https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/

   # 2) 若涉及代理，在 .condarc 里配：
   conda config --set proxy_servers.http  http://user:pass@host:port
   conda config --set proxy_servers.https https://user:pass@host:port

   # 3) 慎用关闭 SSL 校验（只建议排障，别长期开着）：
   conda config --set ssl_verify false     # 用完记得 conda config --remove-key ssl_verify

   # 4) 清了缓存再重试：
   conda clean --all

仓库地址如清华/中科大漏加\ **尾部 ``/``
或路径写错域名的后缀**\ ，就是另一个 ``PackagesNotFoundError``/``HTTP``
报错的来源——先核对 URL 拼写。

   **气象场景一句话**\ ：数据源（包仓库）在美国，你局域网到那边绕远路/过安检（SSL）老失败。换个「镜像站」=
   数据源搬到兰州大学的镜像机房，路近自然快；PPT 里 TUNA(清华) 就是给
   AWS 例子的「本地数据中心镜像」。

--------------

.. _135-solving-environment-卡死--依赖冲突--channel-优先级:

1.3.5 ``Solving environment`` 卡死 / 依赖冲突 / channel 优先级
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象** ``conda install`` 后长时间卡在

.. code:: text

   Solving environment: \

(反斜杠/横线不停转) 或几十分钟没动静；或者装一批包时报出依赖冲突让你选
``[y/N]``\ ，最终失败回滚。

**原因**

- conda 老求解器（SAT 求解）在多
  channel、多约束下搜索空间爆炸；包越多越慢；
- 没设 ``channel_priority``\ ，conda 在各 channel
  之间反复挣扎找「折中方案」，保守无所谓就慢；
- 装了互相要不同版本的包（如某包要 numpy<2、又要 numpy>=2）形成死循环 →
  无解回滚。

**解决办法**

.. code:: bash

   # 1) 严格 channel 优先级，减少搜索量、少冲突
   conda config --set channel_priority strict
   # 2) 避开 base 大量混装；尽量一次把相关包装齐再微调
   # 3) 卡死就 Ctrl+C 停掉，清缓存重来
   conda clean --all
   # 4) 仍卡：用更快的求解器 mamba（conda-forge 的 mamba 同门更快）
   mamba install -n met_p312 -c conda-forge cartopy
   # 5) 真冲突无解：宁可新建干净环境退出；不要硬 `--force-reinstall` 叠

..

   特别提醒：为「省事」给包强行降级 numpy/cartopy
   主版本，常让环境崩得更彻底（见 §1.5.1 的
   ``conda env list``/``conda list`` 排查法）。

   **气象场景一句话**\ ：装包求解器像个运筹员，在「标量天气预报室（base）」和「西北格点室（conda-forge）」之间排班，要求每个包都要上班得能对齐班表。约束互相打架（某馆要上班、某馆同时要下班），排班就是排不出来（无解回滚）。设好
   ``channel_priority`` 等于告诉排班员「先顾 conda-forge
   馆」——班表一下好排了。

--------------

.. _14-静默异常与路径坑不报红结果却不对:

1.4 静默异常与路径坑（不报红、结果却不对）
------------------------------------------

   第 0 篇 §0.5
   反复强调：最阴险的是「没报错，但结果的错」。本节两条也是「看着对、实则错」的典型——尤其装包串台，\ **装都成功、跑却失败**\ 。

.. _141-装包成功但-import-失败--pip-装到了另一个-python--环境串台:

1.4.1 装包成功但 import 失败 —— pip 装到了另一个 python / 环境串台
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象** ``pip install xyz`` 显示
``Successfully installed xyz``\ ，没报错；可 ``python -c "import xyz"``
还是
``ModuleNotFoundError``\ 。你可能会很抓狂：\ **明明显示装成功了呀？**

**原因** 真实输出里上一行其实写明白了 pip 到底进了哪个环境：

- 若你 ``conda activate met_p312`` 后再 ``pip``\ ，但 ``pip`` 这个命令在
  PATH 里\ **仍解析到系统 python 的 pip**\ （\ ``where pip`` 并非指向
  met_p312），就装进了系统/别处；
- 汇总一句话：\ **``pip`` 和 ``python``
  不是同一对**\ 。\ ``pip install`` 装到的 site-packages，和
  ``python -c "import"`` 搜索的 ``sys.path``\ ，不是同一个文件夹 →
  装了=没装到，跑就必失败。

**解决办法：永远用 ``python -m pip``\ ，让 pip 和当前 python 永远同源**

.. code:: bash

   conda activate met_p312
   python -m pip install xyz          # 关键：用 python -m pip，而不是裸 pip
   python -c "import xyz; print('ok')"  # 装完立刻用同一个 python 验证

诊断：\ ``where python``\ 、\ ``where pip``\ 、以及
``python -c "import sys;print(sys.executable);print(sys.path)"``——看到两处都指向
``...envs\met_p312\`` 才放心。

   别用 ``pip``\ （裸）的根源在于裸 pip
   可能指向别处；\ ``python -m pip`` 强制「用刚才运行的这个 python 的
   pip」。

..

   **气象场景一句话**\ ：你把雷达拼图程序塞进「兰州站的电脑」（met_p312），却开枪校准用「榆中站的程序」（裸
   pip）——当然是装了却没装对机上。\ **``python -m pip``\ =
   确保「装的机器」和「跑的机器」是同一台**\ 。

--------------

.. _142-中文用户名--中文路径导致报错乱码甚至装包失败:

1.4.2 中文用户名 / 中文路径导致报错、乱码、甚至装包失败
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象**

- Jupyter 无法启动 / 内核闪退，报错退出码 1，日志指向路径出现中文；
- 运行时抛 ``UnicodeDecodeError: 'ascii' codec can't decode...`` /
  ``FileNotFoundError``\ ；
- conda/pip 在 ``C:\Users\张三\...`` 下动作诡异、乱码。

**原因** Windows 用户主目录常带中文（如
``C:\Users\张三``\ ），而一部分底层库（尤其编译型依赖）对非 ASCII
路径支持不完善；conda 的缓存、RECIPES
里一旦吃到中文路径就会出幺蛾子。这是第 1
章开头就强调「\ **全程纯英文路径**\ 」的现实原因。

**解决办法**

1. 安装路径与项目路径\ **一律英文、无空格、无括号**\ ，推荐
   ``D:\Software\miniconda3``\ 、\ ``D:\Code\weather_project``\ ；
2. 若用户名本身是中文，把环境/项目建到纯英文盘符下（如
   ``D:\``\ ），别放在 ``C:\Users\张三\`` 之下；
3. 实在避不开，可尝试 ``conda config --set ...``
   相关缓存路径前先重建干净环境，并保证 ``%HOMEPATH%``
   相关脚本目录为英文。

..

   这也连带解释了正文「禁止中文命名
   yml/py/png」的规范——导出/迁移环境、读写文件时中文名是乱码与
   ``FileNotFoundError`` 的重灾区。

   **气象场景一句话**\ ：观测系统要求所有站点编码
   ASCII（英文+数字），你给测站起名「兰州站01」，NC 文件加载器（底层 C
   代码）一到中文就『卡住读编码』。号码系统不认中文站名，路径也一样。

--------------

.. _15-排查三件套与验证手段把环境看清:

1.5 「排查三件套」与验证手段（把环境看清）
------------------------------------------

   第 1 章所有「装完 import 失败」「activate
   不上」类问题，都能靠下面三条命令三分钟内定位。\ **遇到问题先跑这仨，再回来对表。**

.. _151-conda-list--conda-env-list--where-python--环境排查三板斧:

1.5.1 ``conda list`` / ``conda env list`` / ``where python`` —— 环境排查三板斧
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象**\ ：搞不清「我到底在哪、装了啥、跑的是哪个 python」。

**真实输出参照**\ （本机实测原文）：

.. code:: text

   conda env list
   # conda environments:
   base                     ...\miniforge3
   met_p312                     ...\envs\met_p312
   ...

.. code:: text

   conda list -n met_p312 | findstr numpy
   numpy  2.4.3  py312ha3f287d_0  conda-forge

.. code:: text

   where python
   => 第一个才是 PATH 实际调用的那个

**三句口诀**

1. ``conda env list`` → **我在哪个环境**\ （带 ``*``
   的是激活的）；找不到目标环境名 → 去 activate 或 create；
2. ``conda list | findstr 包名`` →
   **这个包装没装、装着什么版本、来自哪个 channel**\ ；装到别的环境 /
   版本不对都能一眼看出；
3. ``where python`` + ``python -c "import sys;print(sys.executable)"`` →
   **跑的到底是哪个 python**\ 。

**用法场景**

- 报 ``ModuleNotFoundError`` → 先 ``conda list`` 看包在不在，再
  ``where python`` 看解释器对没对；
- ``conda activate xx`` 报找不到 → ``conda env list``
  看真实名（大小写/拼写）；
- 环境被改乱、包版本崩了 → **能修就
  ``conda install --revision N``\ ，不能修就重建**\ ：\ ``conda env export > env.yml``
  留着，\ ``conda env remove -n met_p312`` 后再
  ``conda env create -f env.yml`` 一键复现。

..

   升级/降级把环境搞崩（如把 numpy 主版本降下去、pip 转述「bad
   interpreter」）时，最稳的不是硬
   ``--force-reinstall``\ ，而是\ **导出快照、删掉重建**\ 。

   **气象场景一句话**\ ：这三条命令就是气象值班的「观测三查」——查站名（env
   list 在哪个站）、查要素（list 装没装）、查传感器（where python
   是谁在报数）。先自查三查，再去翻分析报告（搜报错）。

--------------

.. _16-环境运行期崩溃与依赖冲突实测新增:

1.6 环境运行期崩溃与依赖冲突（实测新增）
----------------------------------------

   前几节讲的都是「装不上 / 找不到 /
   激活不了」。这一节记两类\ **更隐蔽、更真实**\ 的坑：\ **环境能装、能激活，但一
   ``import`` 某个包就整段崩溃（甚至把 Python 自己搞死）**\ ，或\ **包的
   DLL
   被“截胡”加载错版本**\ 。这些几乎都在家/实验室真实验证过，且最容易让大一新生误以为「是自己代码写错了」——其实不是。

.. _161-windows-fatal-exception-code-0xc06d007f--一-import-numpy-整段崩溃blas-版本不兼容:

1.6.1 ``Windows fatal exception: code 0xc06d007f`` —— 一 ``import numpy`` 整段崩溃（BLAS 版本不兼容）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ （Traceback 原文照录，\ ``import numpy`` 即死）：

.. code:: text

   python.exe : Windows fatal exception: code 0xc06d007f
   Current thread 0x... (most recent call first):
     File "...\envs\met_p312\Lib\site-packages\numpy\__init__.py", line 878 in blas_fpe_check
     File "...\envs\met_p312\Lib\site-packages\numpy\__init__.py", line 887 in <module>
     ...

程序\ **没有熟悉的 ``Traceback``\ 、没有 ``Error`` 名**\ ，而是直接把
Python 进程整个干掉（退出码异常、终端可能直接报
``Windows fatal exception``\ ）。这是「异常层级树」山顶之上的特殊类别——它不是
``Exception``\ ，而是\ **解释器/进程级崩溃**\ 。

**原因** 罪魁是 **NumPy 与它链接的 BLAS 动态库（MKL /
OpenBLAS）版本不匹配**\ 。\ ``import numpy`` 时 numpy 会对链接进来的
BLAS 做「浮点异常检查」（\ ``blas_fpe_check``\ ），一旦检测到 BLAS
行为异常就触发
``0xc06d007f``\ （STATUS_DLL_INIT_FAILED，动态库初始化失败）。常见诱因：\ **同一环境里
conda-forge 的 numpy 与 MKL 版本配对坏了、或有人用 pip 覆盖过 conda 的
numpy、或 ``PYTHONPATH`` 污染**\ 。这和 §1.3.5 说的「乱降级
numpy/cartopy 主版本会把环境搞崩」是一个家族。

**解决办法（按顺序试）**

1. 先看\ **根本不是代码错、是环境崩了**——单独开一个空脚本只写
   ``import numpy`` 复现，能复现就不是你业务代码的问题；
2. 用 pip 把 numpy 重装成与同机其他可用环境一致的版本（如
   ``2.4.2``\ ），覆盖掉崩溃的那个 conda 构建：

   .. code:: bash

      python -m pip install --force-reinstall "numpy==2.4.2"
      python -c "import numpy; print(numpy.__version__)"   # 转过即好

3. 若还不行，回到
   §1.5.1：\ **导出快照、删掉重建**\ 干净环境，或换一个能用的 conda
   环境补上同样的包跑业务（\ ``conda env list`` 选别的）。

..

   这类崩溃最常见于「别人给的环境 / 你自己手滑 conda+pip 混装」——**conda
   和 pip 不要在同一环境重复装同一个科学计算包**\ ，这正是
   §1.4.1「\ ``python -m pip`` 才同源」的延伸。

   **气象场景一句话**\ ：天气雷达主机上装了两套互不兼容的采集板驱动（MKL
   vs
   OpenBLAS），一道开机自检（\ ``blas_fpe_check``\ ）就认出来「你俩对不上」，直接整机断电（进程崩溃）——不是你的观测程序写错了，是\ **底层元器件（编译好的
   DLL）撞了**\ 。

--------------

.. _162-importerror-dll-load-failed--用户目录的旧包抢跑了-conda-环境的包pythonpath-优先级:

1.6.2 ``ImportError: DLL load failed`` —— 用户目录的旧包抢跑了 conda 环境的包（PYTHONPATH 优先级）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**现象 / 真实输出**\ （本机实测原文，\ ``import cartopy`` 报错，且栈里
``shapely`` 被从\ **用户目录**\ 加载）：

.. code:: text

   ImportError: DLL load failed while importing lib: 找不到指定的模块。

再深挖 ``sys.path``\ ，发现
``AppData\Roaming\Python\Python312\site-packages`` 出现在 conda 的
``Lib\site-packages`` **之前**\ ：

.. code:: text

   ...\envs\met_p312\Lib ...
   ...\AppData\Roaming\Python\Py312\site-packages   # ← 用户目录，排前面！
   ...\envs\met_p312\Lib\site-packages                  # ← conda 环境，反而在后面

**原因** 你把 pip 装到了\ **「环境（site-packages）」**，但 Python 的
``sys.path`` 里还有一个系统级「用户
site-packages」目录（\ ``AppData\Roaming\Python\Python312\site-packages``\ ，是之前某次
``pip install --user`` 留下的）。Python
找包是\ **从左到右、先到先得**，用户目录排前面，于是 ``import shapely``
命中了用户目录里那份\ **旧版、DLL 与新 Python 不匹配**\ 的 sharply →
加载 DLL 失败。\ **报错的包 (cartopy) 是好的，被一个“冒名顶替”的依赖
(shapely) 拖下水。**

**解决办法**

1. 先确认是不是它在捣乱：打印 ``sys.path``\ ，看有没有
   ``AppData\Roaming\Python\...\site-packages``\ ；并看
   ``shapely.__file__`` 指向哪：

   .. code:: bash

      python -c "import sys; [print(p) for p in sys.path]"

2. 临时验证：设置环境变量忽略用户 site，再 import 是否就好了：

   .. code:: powershell

      $env:PYTHONNOUSERSITE="1"
      python -c "import cartopy; import shapely; print(shapely.__version__)"
      Remove-Item Env:\PYTHONNOUSERSITE

   （能用 = 确认是用户目录的包抢跑。）
3. 彻底修：删掉用户目录里那份旧包（\ ``pip uninstall`` 时注意它归属
   ``--user``\ ），或保证 conda
   环境里的包版本是正的，且不要给科学计算包用 ``pip install --user``\ 。

..

   与 §1.1.2「跑代码的解释器和装包的 python
   不是同一个」呼应：这里是「\ **同一个是 conda 的，但用户级
   site-packages 抢跑**\ 」。两者都指向\ **「先看清 ``sys.path``
   到底在搜哪几个文件夹」**。

   **气象场景一句话**\ ：雷达拼图系统里，你把最新版「格点插值模块」装进了数据机柜（conda
   环境），但总有台常年不维护的旧终端（用户目录）里也装着一份 2018
   年的老模块，局域网名字还撞车。系统一 ``import`` 就优先连上那台旧终端
   → 数据结构对不上（DLL 不匹配），整段模块（cartopy）诈尸报错。\ **改
   ``sys.path`` 顺序 = 让主机优先连着谁。**

--------------

.. _本章高频关键词--一句话复习表:

本章高频「关键词 → 一句话」复习表
---------------------------------

   把下面的表背下来，第 1 章就逃不出你的五指山。每条都对应上面的条目号。

+------------------------------------------------------+------------------------------------------------------------+----------+
| 报错关键词                                           | 一句话原因                                                 | 对应条目 |
+======================================================+============================================================+==========+
| ``ModuleNotFoundError: No module named 'xxx'``       | 包没装 / 没 activate 到装了它的环境 / 名字拼错             | §1.1.1   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ModuleNotFoundError「明明装过还报」                  | 跑代码的解释器与装包的不是同一个                           | §1.1.2   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ModuleNotFoundError + 名字像『nyumpy』               | 库名/别名拼错                                              | §1.1.3   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``NameError: name 'np' is not defined``              | 忘了 ``import numpy as np``                                | §1.1.4   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``python``/``python3`` 版本对不上                    | PATH 里多个 python，命令解析到别人                         | §1.1.5   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| 同代码终端能跑 VS Code 不能                          | VS Code 解释器没选 ``met_p312``                            | §1.1.6   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``'jupyter' 不是内部或外部命令``                     | 没激活 / 没装 / Scripts 没进 PATH                          | §1.2.1   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``'conda' 不是内部或外部命令``                       | PATH 没勾 / 没 ``conda init``                              | §1.2.2   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``Python was not found; run without...``             | 微软商店空壳别名，没真装 python                            | §1.2.3   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``The term 'xxx' is not recognized``                 | 命令名拼错                                                 | §1.2.4   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``install jupyter-notebook`` 报 PackagesNotFound     | 包名不对，应 ``jupyter`` / ``notebook``                    | §1.3.1   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``PackagesNotFoundError``\ （geo/cartopy/rioxarray） | 第三方库要加 ``-c conda-forge``                            | §1.3.2   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``conda create -n xx python=3.12`` 报错              | ``-n``/``=``/环境名语法坑                                  | §1.3.3   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| 下载慢/``http 000``/``CondaSSLError``                | 境外源慢、代理/SSL、没配镜像                               | §1.3.4   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``Solving environment`` 卡死/priority 冲突           | 依赖搜索爆炸、channel 优先级没设                           | §1.3.5   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| pip 显示 Success 但 import 失败                      | pip 和 python 不是同一对，串台了                           | §1.4.1   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| 中文路径乱码 / UnicodeDecodeError                    | 用户名/路径含中文空格括号                                  | §1.4.2   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``import numpy`` 就                                  | numpy 与 BLAS 版本不兼容，进程级崩溃                       | §1.6.1   |
| ``Windows fatal exception 0xc06d007f``               |                                                            |          |
+------------------------------------------------------+------------------------------------------------------------+----------+
| ``ImportError: DLL load failed`` 但包装得很好        | 用户目录旧包抢跑 conda 的包（site-packages 顺序）          | §1.6.2   |
+------------------------------------------------------+------------------------------------------------------------+----------+
| 一切装包/激活报错不知道从哪查                        | 用                                                         | §1.5.1   |
|                                                      | ``conda env list``\ +\ ``conda list``\ +\ ``where python`` |          |
+------------------------------------------------------+------------------------------------------------------------+----------+

--------------

附注：环境操作条目的来源与验证
------------------------------

涉及「写入/迁移 conda
环境、联网下载」的报错，需在你自己的机器上执行才能复现，本文的现象与解决方案依据
**conda / conda-forge / Anaconda
官方文档与权威社区资料**\ 整理，供自查（如需进一步核实，可按关键词检索官方文档）：

- §1.3.1 ``conda install jupyter-notebook`` →
  ``PackagesNotFoundError``\ （conda 官方：Jupyter 包名为
  ``jupyter``/``notebook``\ ）；
- §1.3.2 ``PackagesNotFoundError`` + 第三方库“不加
  ``-c conda-forge``\ ”（conda-forge
  文档：cartopy/geopandas/rioxarray/netcdf4 属 conda-forge
  独有；\ ``conda config --show channels`` 可核对你的默认
  channel——标准安装通常只有 ``main``/``defaults``\ ）；
- §1.3.3 ``conda create`` 参数坑 / ``CondaValueError`` /
  ``InvalidSpec``\ （conda 官方与 GitHub issues）；
- §1.3.4 下载慢 / ``HTTP 000`` / ``CondaSSLError``\ （Anaconda
  故障排查文档：代理与镜像配置）；
- §1.3.5 ``Solving environment`` 卡死 / ``channel_priority``\ （conda
  官方概念文档 conda-performance）；
- §1.2.2 的 ``Set-ExecutionPolicy RemoteSigned`` 修
  ``Run 'conda init' before 'conda activate'``\ （conda GitHub issue
  #15762）。

其余偏向「纯 Python 语法 / 解释器行为」的条目（§1.1.1–1.1.4、§1.2.1 /
§1.2.4 等），现象栏内的 Traceback 均可在本机任何 Python
解释器上原样复现。
