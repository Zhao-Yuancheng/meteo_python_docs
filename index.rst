云笺 CloudDocs
=================

.. meta::
   :description: 云笺 CloudDocs —— 兰州大学大气科学学院编程社区的 Python 编程文档：零基础起步的 Python 编程基础、气象数据处理与气象数据可视化主线教程，配示例画廊与贯穿全站的实战项目。

.. raw:: html

   <div class="mh-top">
   <link rel="stylesheet" href="_static/home.css?v=0">
   <!-- ============ Hero · 等压墨迹 Isobaric Ink（p5 生成艺术） ============ -->
   <section class="mh-hero" aria-label="站点横幅">
     <div id="mh-canvas-host" role="img" aria-label="生成艺术「等压墨迹」：示踪粒子在无散度风场中的墨色轨迹，叠加等压线与高（G）低（D）压中心标记"></div>
     <div class="mh-hero-inner">
       <p class="mh-eyebrow">兰州大学大气科学学院 · 编程社区「码上薪火」</p>
       <div class="mh-brand" aria-label="云笺 CloudDocs">
         <span class="mh-brand-cn">云笺</span>
         <span class="mh-brand-en">CloudDocs</span>
       </div>
       <h2 class="mh-headline">从第一行代码，<br>到第一份气象分析报告</h2>
       <p class="mh-sub">面向零基础起步的学习者：Python 编程基础 · 气象数据处理 · 气象数据可视化——10 节主线教程、可执行示例画廊与贯穿全站的实战项目，一站学完。</p>
       <div class="mh-cta">
         <a class="mh-btn mh-btn-primary" href="user_guide/basics/python_conda.html">开始学习</a>
         <a class="mh-btn mh-btn-ghost" href="gallery/index.html">浏览画廊</a>
         <a class="mh-more" href="about.html">关于本站 →</a>
       </div>
     </div>
     <div class="mh-station" aria-hidden="true">
       <span>兰州 LANZHOU · 36.06°N 103.83°E · 海拔 1517 M</span>
       <span>等压墨迹 ISOBARIC INK · SEED 10383</span>
     </div>
   </section>
   <!-- ============ 快捷入口 ============ -->
   <div class="mh-quick">
     <a class="mh-qcard" href="user_guide/basics/python_conda.html">
       <span class="mh-qicon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg></span>
       <span class="mh-qbody"><b>快速开始</b><span>安装 Conda 与 Python，画出第一张气象图。</span></span>
       <span class="mh-qarrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span>
     </a>
     <a class="mh-qcard" href="api/index.html">
       <span class="mh-qicon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></span>
       <span class="mh-qbody"><b>术语参考</b><span>整型、浮点型、切片……初学者术语逐一拆解。</span></span>
       <span class="mh-qarrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span>
     </a>
     <a class="mh-qcard" href="tutorials/index.html">
       <span class="mh-qicon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg></span>
       <span class="mh-qbody"><b>实战练习</b><span>章节实战练习，含提示与参考答案。</span></span>
       <span class="mh-qarrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span>
     </a>
   </div>
   </div><!-- /.mh-top -->

.. rst-class:: mh-lead

欢迎来到兰州大学大气科学学院编程社区的 **云笺 CloudDocs** 编程文档。
本站面向零基础起步的学习者，也适合想系统梳理气象数据可视化技巧的同学与科研人员。
我们仿照 Matplotlib 官方文档的组织方式，将「Python 基础、气象数据处理、气象数据可视化」
串成一条主线，并以贯穿全站的实战项目让你学一章、进一步，最终产出一份完整的气象数据分析报告。

.. rst-class:: mh-lead

你可以直接用浏览器在左侧翻阅教程，或在**示例画廊**里边看成品图边复制代码跑通自己的版本。

.. rst-class:: mh-sec mh-toc

内容一览
--------

- :doc:`/user_guide/index` —— 从环境搭建到 Cartopy 地图绘图的核心教程，共 10 节。
- :doc:`/tutorials/index` —— 与章节配套的实战练习，附提示与参考答案，检验所学。
- :doc:`/gallery/index` —— 可执行的示例画廊：基础绘图、NumPy 计算、气象数据可视化、
  科研绘图四大分区，每个示例都可下载源码、Notebook 与数据。
- :doc:`/api/index` —— 术语速查，随学随用。
- :doc:`/qa/index` —— 常见问题汇总，含报错排查思路。
- :doc:`/about` —— 本站与团队：项目缘起、指导教师、成员与实践足迹。

.. rst-class:: mh-sec mh-modules

三大内容模块
------------

- **模块一 Python 编程基础**：Conda、数据类型、分支循环、函数与作用域、面向对象与高级语法。
  从零上手，不跳步。
- **模块二 气象数据处理**：NumPy 计算、Pandas 分析、Xarray 多维数据，学会操作格点与表格数据。
- **模块三 气象数据可视化**：Matplotlib 绘图、Cartopy 地图绘图，把数据变成清晰的科学图表。

.. rst-class:: mh-sec mh-project

贯穿项目
--------

全站 10 节共用一个递进式实战项目：**兰州气温观测数据分析与可视化系统**。从第 1 节搭建
``weather_project/`` 起，到第 10 节画出西北地区气温空间分布图止，最终产出一份完整的气象
数据分析报告（含图表），让你真正"能上手、出作品"。

.. raw:: html

   <div class="mh-timeline" aria-hidden="true">
     <span class="mh-tl-label">第 1 节<br><code>weather_project/</code></span>
     <span class="mh-tl-track"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>
     <span class="mh-tl-label">第 10 节<br>西北气温空间分布图</span>
   </div>

.. rst-class:: mh-sec mh-usage

如何使用本站
------------

- **跟着练**：按目录顺序学完 10 节，每节末尾都有对应练习；卡住了先查**术语参考**与**常见问题**。
- **抄示例**：想快速出图，直接进**示例画廊**选一张效果图，下载源码与数据本地运行，改参数即可。
- **遇到问题**：报错先看**常见问题**；仍未解决可在社区里带着报错信息提问。

.. raw:: html

   <div class="mh-next">
     <span>准备好了？</span>
     <a href="user_guide/basics/python_conda.html">从第 1 节开始</a>
     <span class="mh-next-dot">·</span>
     <a href="qa/index.html">卡住看常见问题</a>
     <span class="mh-next-dot">·</span>
     <a href="about.html">了解本站与团队</a>
   </div>
   <script defer src="_static/p5.min.js?v=0"></script>
   <script defer src="_static/home-flow.js?v=0"></script>

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: 云笺 CloudDocs

   user_guide/index
   tutorials/index
   gallery/index
   api/index
   qa/index
   about
