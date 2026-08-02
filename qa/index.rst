常见问题 Q&A
============

收集搭建与使用本文档时的常见问题。

安装与构建
----------

.. dropdown:: sphinx-build 提示找不到扩展？

   确认在 ``P312`` 环境里装齐工具链：

   .. code-block:: bash

      pip install sphinx pydata-sphinx-theme sphinx-design \
                  sphinx-gallery sphinx-copybutton myst-parser

.. dropdown:: 构建时 sphinx-gallery 执行示例很慢或报错？

   首次构建会真实运行每个 ``plot_`` 脚本。可临时关闭执行以加速：

   .. code-block:: bash

      sphinx-build -b html -D sphinx_gallery_conf.plot_gallery=False . _build/html

在线运行器
----------

.. dropdown:: 点"运行"按钮没反应？

   - 确认已把 WebPy 构建产物拷到 ``_static/webpy/``（``build.py`` 会自动拷贝）。
   - 打开浏览器控制台，检查 iframe 是否同源；跨域会拦截 ``postMessage`` 之外的操作。
   - Pyodide 首次加载约 10 MB，稍候片刻再点。

.. dropdown:: 中文输出乱码？

   WebPy 已用 UTF-8 流式解码，正常情况中文可直接显示。若在 ``print`` 中混入
   非法编码字节，会显示为替换符，检查数据源编码即可。

.. dropdown:: 如何上传文件练习 open()？

   在运行器左侧文件浏览器点"上传文件"或直接拖入，文件进入虚拟文件系统根目录，
   随后在代码里 ``open("文件名")`` 即可读取。
