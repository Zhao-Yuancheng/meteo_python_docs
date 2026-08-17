第 4 章练习：函数及变量作用域、模块和包
========================================

配套 :ref:`tut-func` 正文。多数题需编写函数与模块，请保存为 ``.py`` 脚本后运行。提交前先确认代码能跑通，并留意题目中的易混淆点。

.. seealso:: 配套正文：:doc:`/user_guide/basics/functions`　·　术语参考：:doc:`/api/ch04_terms`

第 1 题（实操填空）气温转换函数
-------------------------------

**题目**：编写函数 ``celsius_to_fahrenheit(celsius)``，将摄氏温度转换为华氏温度：接受一个摄氏温度，返回相应的华氏温度。然后在主程序中调用该函数，把兰州站一组气温 ``[25, 30, 35]``（单位 ℃，℃ 与华氏 F 的关系 ``F = C * 9 / 5 + 32``）全部转换为华氏温度并打印结果。

.. tip:: 提示

   1. 公式为 ``F = C * 9/5 + 32``。
   2. 使用 for 循环或列表推导遍历列表中的摄氏温度，逐个调用函数进行转换。
   3. 调用前必须先 ``def`` 定义函数；名字拼错或忘了定义就直接调用，会报 ``NameError``。

.. admonition:: 参考答案

   .. code-block:: python

      # 1. 创建函数
      def celsius_to_fahrenheit(celsius):
          return celsius * 9 / 5 + 32

      # 2. 创建列表
      celsius_temps = [25, 30, 35]

      # 3. 遍历列表并调用函数（这里用列表推导得到新列表）
      fahrenheit_temps = [celsius_to_fahrenheit(temp) for temp in celsius_temps]

      # 4. 输出结果
      print(f"华氏温度: {fahrenheit_temps}")   # [77.0, 86.0, 95.0]

第 2 题（实操填空）统计平均温度
-------------------------------

**题目**：编写函数 ``calculate_average(temps, decimal_places=1)``，默认保留一位小数，用于计算兰州站一组气温的平均值。但输出结果时，要求把 ``[25.5, 24.8, 26.9, 26.3]`` 四个数（单位 ℃）的平均温度保留 2 位小数并打印。

.. tip:: 提示

   1. 使用 ``sum()`` 计算列表中所有温度的总和，使用 ``len()`` 计算温度个数，总和除以个数即为平均值。
   2. 保留小数用 ``round(值, 位数)``；默认一位就用默认参数，要两位时在实参上直接改 ``decimal_places=2`` 或写第二个位置参数。

.. admonition:: 参考答案

   .. code-block:: python

      # 1. 创建函数，带默认参数 decimal_places=1
      def calculate_average(temps, decimal_places=1):
          avg = sum(temps) / len(temps)
          return round(avg, decimal_places)

      # 2. 数据即题目给出的兰州站四个气温
      daily_temps = [25.5, 24.8, 26.9, 26.3]

      # 3. 调用默认参数结果（保留 1 位）
      print(calculate_average(daily_temps))        # 25.9

      # 4. 在实参处修改默认参数，改为保留 2 位小数
      print(calculate_average(daily_temps, 2))     # 25.88

第 3 题（分析题）变量作用域分析
-------------------------------

**题目**：阅读以下代码，在纸上写出它的输出结果：

.. code-block:: python

   temp = 20

   def update_temp(t):
       temp = t
       print(f"内部温度: {temp}")

   update_temp(30)
   print(f"外部温度: {temp}")

.. tip:: 提示

   1. 在函数内部，``temp = t`` 会新建一个局部变量 ``temp``，赋值为 30，并打印出"内部温度: 30"。
   2. 在函数外部打印的 ``temp`` 是全局变量，值仍是 20，函数内部的赋值不会影响外部变量。
   3. 若把函数内部那行注释掉直接 ``print(temp)`` 而 temp 又没定义，会抛 ``NameError``；本函数内部已新建局部变量，所以不报错，只是内外是两个 temp。

.. admonition:: 参考答案

   .. code-block:: text

      内部温度: 30
      外部温度: 20

.. admonition:: 易混淆点

   1. 函数内部 ``temp = t`` 的 ``temp`` 仅在函数内有效，所以内部打印的是 t（30）；这个赋值不影响外部全局变量 ``temp``，外部打印仍是 20，内外的 ``temp`` 是两个不同变量。
   2. 如果想在函数里修改全局变量，必须加 ``global`` 声明：

   .. code-block:: python

      temp = 20

      def update_temp(t):
          global temp
          temp = t
          print(f"内部温度: {temp}")

      update_temp(30)
      print(f"外部温度: {temp}")   # 30

第 4 题（实战挑战 · 模块）创建模块并导入
-----------------------------------------

**题目**：创建一个模块文件，定义函数 ``wind_chill(temp, wind_speed)`` 用以计算兰州站冬季的体感温度（风冷指数）。导入该模块，调用函数计算气温 5 摄氏度、风速 20 km/h 时的体感温度，并打印结果。

体感温度公式为：

.. code-block:: text

   T_wc = 13.12 + 0.6215 × T - 11.37 × V^0.16 + 0.3965 × T × V^0.16

其中 T 为气温，V 为风速（km/h），返回值保留一位小数。

建议目录结构：

.. code-block:: text

   package/__init__.py
   package/wind/__init__.py
   package/wind/wind_utils.py
   main.py        # 与 package 同级

.. tip:: 提示

   1. 创建 ``__init__.py`` 时注意是前后各两道下划线（``init`` 两边各 ``__``），不要打成单下划线。
   2. 保留一位小数可以使用 ``round(值, 1)``。
   3. 调用模块函数可以使用 ``from 包.模块 import 函数``，导入后直接按函数名调用即可。
   4. 别把包做成互相 import：主程序只单向导入工具包，否则可能形成循环导入，表现为"模块明明有这函数却提示没定义"。

.. admonition:: 参考答案

   .. code-block:: python

      # 1. 新建 wind_utils.py，编写函数代码
      def wind_chill(temp, wind_speed):
          result = (13.12 + 0.6215 * temp
                    - 11.37 * (wind_speed ** 0.16)
                    + 0.3965 * temp * (wind_speed ** 0.16))
          return round(result, 1)

      # 2. 创建包：文件夹 package 内存放 __init__.py 和子文件夹 wind；
      #    wind 内再放 __init__.py 与 wind_utils.py。

      # 3. 在 package/wind/__init__.py 中写：from .wind_utils import wind_chill
      #    （包内的相对导入，注意开头的点）

      # 4. 主程序导入并调用：from ... import 后直接按函数名用即可
      from package.wind import wind_chill

      temp, wind = 5, 20
      chill = wind_chill(temp, wind)   # 已用 from 导入，直接调用，不要再写 wind_utils.wind_chill
      print(f"气温 {temp}℃，风速 {wind}km/h，体感温度：{chill}℃")

.. admonition:: 提示 · 易错点

   1. 主程序（导入模块并调用函数的部分）所在文件必须与 ``package`` 包同级，而不是放到 ``package`` 里面。
   2. 报错 ``ModuleNotFoundError`` 时，通常是主程序所在文件与 ``package`` 不在同一目录；Spyder 用户可点击右上角路径栏切换当前目录。
   3. 报错 ``ImportError`` 时，多半是 ``wind/__init__.py`` 里的相对导入路径填错了、漏了开头的点（``.``），或没保存，按此方向检查。
   4. 报 ``NameError`` 时，多为 ``from package.wind import wind_chill`` 后又写成了 ``wind_utils.wind_chill(...)``——用 ``from ... import`` 导入后只能直接写函数名。
   5. 若同时导入了互相引用的多个模块导致循环导入，可把次要 import 移到函数的内部再写，保证先定义后引用。