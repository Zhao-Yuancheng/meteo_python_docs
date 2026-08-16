.. _tut-conda:

Python 与 Conda 简介
====================

第 1 节 · 模块一 Python 编程基础
贯穿项目第 1 步：搭建项目环境，创建 ``weather_project/`` 目录并跑通第一个验证脚本。

本章是"兰州气温观测数据分析与可视化系统"的**开篇**。学会这一节，你就拥有了一个"气象专用实验室"：装好 Miniconda、建好虚拟环境、配好 VS Code，并运行出第一段打印兰州站点信息的气象代码。

学完本章你将能够：

#. 理解 Python 为什么是气象数据分析的首选语言；
#. 安装 Miniconda 并创建气象专用虚拟环境 ``met_p312``；
#. 用 VS Code 绑定解释器，搭建 ``weather_project`` 项目目录；
#. 运行第一个气象脚本，验证环境搭建成功。

.. grid:: 1 2 2 3
   :gutter: 2

   .. grid-item-card:: 🎬 配套视频
      :link: ch01-video
      :link-type: ref
      :class-card: gallery-card

      ^^^

      安装与配置录屏 + 执行流程动画

   .. grid-item-card:: ✏️ 配套练习
      :link: /tutorials/ch01_practice
      :link-type: doc
      :class-card: gallery-card

      ^^^

      环境创建、安装包、运行脚本实战题

   .. grid-item-card:: 🖼 可执行示例
      :link: /gallery/auto_examples/plot_basics/plot_first_weather
      :link-type: doc
      :class-card: gallery-card

      ^^^

      第一个气象折线图

.. _ch01-video:

配套视频（T-102）
-----------------

三支视频分别对应安装 Anaconda、配置 VS Code、Python 执行流程动画，点击即可播放：

.. .. raw:: html

..    <div class="ch-videos">
..      <video controls preload="metadata" width="100%" poster="">
..        <source src="/_static/videos/T102-安装Anaconda.mp4" type="video/mp4">
..        您的浏览器不支持 HTML5 视频，请下载观看。
..      </video>
..      <p class="ch-video-caption">视频 1-1 · Miniconda 安装与 PATH 配置（T-102）</p>
..    </div>

.. .. raw:: html

..    <div class="ch-videos">
..      <video controls preload="metadata" width="100%" poster="">
..        <source src="/_static/videos/T102-VSCode安装.mp4" type="video/mp4">
..        您的浏览器不支持 HTML5 视频，请下载观看。
..      </video>
..      <p class="ch-video-caption">视频 1-2 · VS Code 配置与 Python 扩展（T-102）</p>
..    </div>

.. .. raw:: html

..    <div class="ch-videos">
..      <video controls preload="metadata" width="100%" poster="">
..        <source src="/_static/videos/T102-Python代码执行流程.mp4" type="video/mp4">
..        您的浏览器不支持 HTML5 视频，请下载观看。
..      </video>
..      <p class="ch-video-caption">视频 1-3 · Python 代码执行流程动画（T-102）</p>
..    </div>

（1）安装 Anaconda

.. video:: /_static/videos/T102-安装Anaconda_av1.webm
   :width: 100%


（2）配置 VS Code

.. video:: /_static/videos/T102-VSCode安装_av1.webm
   :width: 100%

（3）Python 执行流程动画

.. video:: /_static/videos/T102-安装Anaconda_av1.webm
   :width: 100%


为什么气象数据分析首选 Python
-----------------------------

1. **开源免费**：无软件版权限制，高校、气象台站均可用于教学、科研与业务处理，无授权费用。
2. **气象领域生态完善，专业工具库全覆盖**：

   - 数值矩阵计算：NumPy；
   - 站点表格观测数据：Pandas；
   - 气象格点再分析数据：Xarray；
   - 基础可视化绘图：Matplotlib；
   - 地理地图专业绘图：Cartopy（本项目绘制西北地区气温分布图专用）。

3. **语法简洁易懂**：对比 Fortran、C、C++ 等传统气象编程语言，实现相同气温统计逻辑代码行数大幅减少，零基础学生可快速入门。
4. **兼容主流气象数据格式**：原生支持 CSV 站点逐日观测数据、NetCDF 气象场数据。本项目配套模拟数据均采用这两种格式。

Python 代码底层执行逻辑
~~~~~~~~~~~~~~~~~~~~~~~~~

Python 代码无法直接被电脑硬件识别，完整执行流程分三步：``.py`` 源码文件 → 编译生成字节码 ``.pyc`` → Python 虚拟机 PVM 逐行解释执行。

> 形象地说，源码是你的"乐谱"，字节码是"编译好的谱本"，而 PVM 虚拟机是"演奏家"——它按谱本逐行"演奏"出结果。完整动态演示见上面的视频 1-3。

.. note::

   Python 既不是"纯解释型"也不是"纯编译型"：它先把整个源文件编译成字节码，再逐条解释执行字节码。术语细节见 :doc:`/api/ch01_terms` 中的"解释器"词条。

Miniconda 极简环境管理器
------------------------

Miniconda 是轻量化的 conda 发行版，只保留 conda 管理器与 Python 基础组件，安装包不足 100 MB，需要什么库再手动安装。与之相对的 Anaconda 集成了数百个第三方库、体积超 1 GB，启动慢、冗余多，本课程**统一采用 Miniconda**。

conda 虚拟环境是气象学习的**必备**工具，三大优势：

1. **多 Python 版本隔离**：一台电脑可同时存在多个 Python 版本，本项目固定使用 3.12；
2. **第三方库版本隔离**：不同项目独立虚拟环境，彻底解决 Cartopy、Xarray、NetCDF4 等气象底层库的版本冲突；
3. **一键备份迁移**：导出环境配置文件，更换电脑、机房设备可一键复现完全相同环境。

安装 Miniconda（Windows）
-------------------------

- 官方国外源慢，推荐清华镜像站下载 Windows 64 位离线安装程序；
- **全程使用纯英文路径**，禁止中文、空格、括号，推荐 ``D:\Software\miniconda3``。

安装六步走：

1. 双击安装程序，同意用户许可协议；
2. 安装类型选【Just Me】，无需管理员权限；
3. 自定义安装路径（推荐 ``D:\Software\miniconda3``）；
4. 高级选项**两项必须勾选**：Register Miniconda3 as my default Python 3.12 environment、Add Miniconda3 to my PATH environment variable；
5. 等待进度条走完，点击完成；
6. 验证：``Win+R`` → ``cmd``，依次输入：

.. code-block:: bash

   conda --version
   python --version

成功标准：正常输出版本号，Python 版本显示 ``3.12.x``。若提示"conda 不是内部或外部命令"，说明 PATH 未勾选，重跑安装程序修复即可。

安装 Miniconda（macOS）
-----------------------

**方式 1：图形化 pkg 安装（新手推荐）**

1. 清华镜像下载对应芯片版本 pkg（Intel x86_64 / Apple M 系列 arm64）；
2. 双击 pkg 跟随引导安装，默认路径 ``~/miniconda3``；
3. 终端初始化：

.. code-block:: bash

   # Intel 芯片 Mac
   /Users/用户名/miniconda3/bin/conda init bash
   # Apple M 系列芯片 Mac
   /Users/用户名/miniconda3/bin/conda init zsh

4. 完全关闭终端后重开，输入 ``conda --version`` 校验。

**方式 2：Homebrew 命令行安装（有终端基础）**

.. code-block:: bash

   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install --cask miniconda

创建气象专用虚拟环境
--------------------

本课程统一环境命名 ``met_p312``，固定 Python 3.12：

.. code-block:: bash

   conda create -n met_p312 python=3.12

环境全套基础操作：

.. code-block:: bash

   conda activate met_p312     # 激活
   conda env list               # 查看所有环境
   conda deactivate             # 退出

激活后批量安装全书核心库：

.. code-block:: bash

   conda install numpy pandas xarray matplotlib cartopy netcdf4

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 库
     - 在兰州气温项目中的用途
   * - ``numpy``
     - 把逐日气温存成数组，做批量统计、标准化
   * - ``pandas``
     - 读取气温 CSV 表格，按月份分组统计
   * - ``xarray``
     - 打开西北地区 NetCDF 格点场，做区域平均
   * - ``matplotlib``
     - 画气温时间序列折线图
   * - ``cartopy``
     - 画西北地区气温空间分布地图
   * - ``netcdf4``
     - 读写 NetCDF 气象数据文件的底层引擎

VS Code 配置 Python 开发环境
-----------------------------

安装 **3 个必备插件**：Python（微软官方）、Pylint（语法检测）、Code Spell Checker（拼写检查）。然后左下角选择解释器，选中 ``met_p312 (Python 3.12.x)``，底部状态栏显示环境名即绑定成功。

新建项目总文件夹 ``weather_project``，全书统一目录结构：

.. code-block:: text

   weather_project/
   ├── data/          # 存放 CSV、NetCDF 气象模拟数据
   ├── scripts/       # 各章节实战 Python 脚本
   ├── figures/       # 所有绘图生成图片保存目录
   ├── utils.py       # 第 4 章自定义气象工具模块
   └── main.py        # 项目主程序入口文件

运行第一段气象代码
------------------

在 ``weather_project`` 新建 ``main.py``，复制以下代码（无本地文件依赖，可直接运行）：

.. code-block:: python

   # 兰州气温数据分析系统 - 第 1 章演示代码
   print("===== 兰州气象观测数据分析项目 =====")

   station_name = "兰州气象观测站"
   lon, lat, alt = 103.83, 36.06, 1517.2

   print(f"站点名称：{station_name}")
   print(f"经纬度：东经{lon}°，北纬{lat}°")
   print(f"站点海拔：{alt} m")
   print("环境搭建完成，可正式开展气温数据处理工作！")

在终端切换到项目目录并运行：

.. code-block:: bash

   cd weather_project
   python main.py

预期输出：

.. code-block:: text

   ===== 兰州气象观测数据分析项目 =====
   站点名称：兰州气象观测站
   经纬度：东经103.83°，北纬36.06°
   站点海拔：1517.2 m
   环境搭建完成，可正式开展气温数据处理工作！

输出与上面完全一致，即代表环境、代码全部正常。

最佳实践：环境与工程规范
------------------------

正文讲了"怎么装"，这里讲"怎么装得稳"。以下规则来自一线踩坑经验，建议当作团队规范执行。

类型与命名规范
~~~~~~~~~~~~~~~

- 安装路径、项目、环境备份文件**一律纯英文路径**，不出现中文、空格、括号；
- 所有代码**只用相对路径**，不写 C/D 盘绝对路径，机房、多设备可直接运行；
- 环境统一命名 ``met_p312``，固定 Python 3.12，**禁止** 用系统 Python 或 base 环境做气象分析。

环境备份与迁移
~~~~~~~~~~~~~~~

.. code-block:: bash

   conda env export > ./met_p312_env.yml      # 快照导出
   conda env create -f met_p312_env.yml       # 一键复现

适用机房统一授课、更换电脑、小组共享代码，保证所有人生成环境一致。

国内镜像加速（解决下载超时）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
   conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
   conda config --set show_channel_urls yes

日常维护避坑清单
~~~~~~~~~~~~~~~~~~

1. **不随意升级 Python 主版本**，锁定 3.12，防止 Cartopy、Xarray 兼容失效；
2. **不混用 conda 与 pip 大量装库**，底层气象库只用 conda，轻量工具少量 pip；
3. **不随意删除 miniconda 安装文件夹**，卸载环境通过 conda 命令；
4. 环境与项目备份文件统一英文路径，不出现中文命名的 yml/py/png；
5. 多人协作共享 ``met_p312_env.yml``，保证环境完全统一。

.. seealso:: 术语详解见 :doc:`/api/ch01_terms`——解释器、环境、PATH、包管理器、IDE、脚本等词条，每个都配有"一句话定义 + 生活类比 + 代码示例 + 易混淆点"。配套练习见 :doc:`/tutorials/ch01_practice`。

贯穿项目 · 第 1 步：搭建环境并跑通验证脚本
------------------------------------------

本章的项目推进：完成环境搭建、创建 ``weather_project`` 目录、运行 ``main.py`` 打印兰州站信息。**验收标准**：终端能跑通上面的演示代码并输出一致结果。

可运行示例见 :doc:`/gallery/auto_examples/plot_basics/plot_first_weather`。

本章小结
--------

- 掌握 Miniconda 在 Windows / macOS 的安装流程；
- 能创建并管理气象专用虚拟环境 ``met_p312``；
- 完成 VS Code 插件安装、解释器绑定，搭建 ``weather_project`` 目录；
- 成功运行第一段打印兰州站点信息的气象代码。