第 1 章练习：Python 简介及安装环境
==================================

配套 :ref:`tut-conda` 正文。环境类命令无本地文件依赖，可直接在终端执行；代码类题目保存为 ``.py`` 脚本后运行。提交前先确认激活的是 ``met_p312`` 环境。

.. seealso:: 配套正文：:doc:`/user_guide/basics/python_conda`　·　术语参考：:doc:`/api/ch01_terms`

💡 **通用提示**：环境类命令无本地文件依赖，可在终端直接执行；代码类题目可保存为 ``.py`` 脚本后运行。提交前先确认激活的是 ``met_p312`` 环境。

第 1 题（单选题）创建虚拟环境
------------------------------

用 conda 创建名为 ``met_env``、Python 版本 3.10 的虚拟环境，正确命令是（　）

- A. ``conda new met_env python=3.10``
- B. ``conda create -n met_env python=3.10``
- C. ``conda install met_env``
- D. ``conda build met_env``

**参考答案**：B。``create`` 是创建环境，``-n`` 指定环境名，``python=3.10`` 指定版本。

第 2 题（单选题）激活虚拟环境
------------------------------

激活上面创建好的 ``met_env`` 虚拟环境，正确命令是（　）

- A. ``conda open met_env``
- B. ``conda run met_env``
- C. ``conda activate met_env``
- D. ``conda start met_env``

**参考答案**：C。激活环境用 ``conda activate``；退出用 ``conda deactivate``。

第 3 题（实操填空）
--------------------

需要在 ``met_env`` 环境中安装气象绘图库 matplotlib。请写出\ **安装命令**，以及\ **运行脚本 ``plot_first_weather.py``** 的终端命令。

**参考答案**：

.. code-block:: bash

   conda activate met_env
   conda install matplotlib
   python plot_first_weather.py

> 💡 提示：直接运行脚本前务必先激活目标环境，否则可能装错环境或找不到库。

第 4 题（实操简答）
--------------------

新建脚本文件 ``hello.py``，脚本需完成两件事：① 定义变量 ``name``，赋值为自己的名字；② 打印输出 ``你好：XXX``\（XXX 为变量里的名字）。请写出完整代码，并写出终端运行该脚本的命令。

**参考答案**：

.. code-block:: python

   # hello.py
   name = "张三"
   print(f"你好：{name}")

终端运行命令：

.. code-block:: bash

   python hello.py

第 5 题（实战挑战 · 贯穿项目）
------------------------------

结合贯穿项目，在 ``weather_project/main.py`` 中完成：定义兰州站信息（站名、经度、纬度、海拔），并打印成一行规范观测报告，格式如下：

.. code-block:: text

   兰州站：东经103.83°，北纬36.06°，海拔1517.2 m

**参考答案**：

.. code-block:: python

   # weather_project/main.py
   station_name = "兰州"
   lon, lat, alt = 103.83, 36.06, 1517.2
   print(f"{station_name}站：东经{lon}°，北纬{lat}°，海拔{alt} m")

> 💡 提示：``f"{...}"`` 是 f-string，``{}`` 里放变量，``.2f`` 可控制小数位数（第 2 章详述）。