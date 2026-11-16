---
layout: home

hero:
  name: 风电数据分析教程
  text: 风机运行监测与性能评估
  tagline: 用风机运行记录筛查变桨异常、比较两路实测风速，并估算和对照同期发电量。
  image:
    src: /wind-field.webp
    alt: 田野中的风力发电机组
  actions:
    - theme: brand
      text: 风机运行工况
      link: /operations

features:
  - title: 运行监测与变桨异常筛查
    details: 用正常运行记录学出各片叶片通常怎么调，再用实测角度和可取得的辅助信号找偏离。
    link: /pitch
    linkText: 变桨异常筛查
  - title: 两路实测风速对照
    details: 对齐机舱和雷达的观测时段，算哪一路读数更高、差多少，再按需要比较风频或验证换算。
    link: /wind-speed
    linkText: 风速差的计算
  - title: 风场运行后评估
    details: 用已测风速估算同期功率和电量，与实测比较，结合运行记录查电量差出现在哪些时段。
    link: /assessment
    linkText: 同期电量对照
---

<div class="home-reading">

## 学习路径

<ol class="learning-path">
  <li><strong>认识运行与数据</strong>

[运行工况](/operations) · [SCADA 数据](/scada)

  </li>
  <li><strong>筛查变桨偏离</strong>

[变桨监测](/pitch)

  </li>
  <li><strong>算两路测风差异</strong>

[实测风速差](/wind-speed#怎样配对和拟合) · [两路风频](/wind-frequency#两路风频怎么比)

  </li>
  <li><strong>估算并对照同期发电量</strong>

[功率曲线](/power) · [风场后评估](/assessment#怎么计算同期电量差)

  </li>
</ol>

## 这些方法怎样用到项目里

先选一台运行记录可用的机组。变桨筛查找出哪片叶片、哪个时段值得复核。测风对照算出同期两路风速差，判断在哪些条件下可以用来估算功率。发电后评估对照同期的参考电量和实发电量，找出差异较大的时段并回查运行记录。先把这三步在一台机组上跑通，再判断哪些方法能用于其他机组。

</div>
