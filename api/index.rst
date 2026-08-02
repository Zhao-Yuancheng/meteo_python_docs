API 参考
========

本版块汇总文档中用到的关键函数与类的签名。后续可接入 ``sphinx.ext.autodoc`` 自动从源码抽取，
并用 ``sphinx.ext.intersphinx`` 链接到 NumPy / Matplotlib / Xarray 的官方 API。

下面是文档示例里出现过的两个辅助函数的手写签名示例。

.. py:function:: celsius_to_kelvin(c)
   :noindex:

   摄氏度转开尔文。

   :param float c: 摄氏温度
   :returns: 开尔文温度
   :rtype: float

   .. code-block:: python

      from meteo.utils import celsius_to_kelvin
      celsius_to_kelvin(25)   # 298.15

.. py:function:: pressure_profile(levels, p0=1013.25)
   :noindex:

   简化的气压随高度递减序列。

   :param int levels: 层数
   :param float p0: 地面气压 (hPa)
   :returns: 各层气压列表
   :rtype: list[float]

.. py:class:: Station(name, lat, lon)
   :noindex:

   气象站抽象，封装观测数据与统计。

   .. py:method:: record(temp)
      :noindex:

      记录一次气温观测。

   .. py:property:: mean_temp
      :noindex:

      已记录气温的均值。
