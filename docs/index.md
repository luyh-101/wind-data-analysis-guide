---
layout: home

hero:
  name: 风电数据分析教程
  text: 风机运行监测与性能评估
  tagline: 利用 SCADA 和现场测风数据识别变桨异常、建立功率曲线，评估机组和风场的发电性能。
  image:
    src: /wind-field.webp
    alt: 田野中的风力发电机组
  actions:
    - theme: brand
      text: 风机运行工况
      link: /operations
    - theme: alt
      text: 公开实测案例
      link: /research#公开案例与复算资料

features:
  - title: 运行监测与变桨异常筛查
    details: 按工况确定桨距角的正常范围，再结合转速、变桨指令和告警排查异常。
    link: /pitch
    linkText: 变桨异常筛查
  - title: 现场测风与风资源分析
    details: 比较不同测点的同期风速，统计各风速区间的出现频率。
    link: /wind-speed
    linkText: 风速配对与验证
  - title: 功率曲线与发电评估
    details: 用可比工况的数据建立功率曲线，在独立时段检验估算误差，再用于机组比较和风场评估。
    link: /power
    linkText: 功率曲线建模
---

<div class="home-reading">

## 学习路径

1. **读懂运行记录。** 先认识风机工况和运行量，再核对 SCADA 字段与时间窗口。 [风机运行工况](/operations) · [SCADA 数据质量与工况筛选](/scada)
2. **从图表到模型。** 在可比工况下筛查变桨偏离，对齐两路测风数据，再建立并验证功率曲线。 [变桨状态监测](/pitch) · [现场测风对照](/wind-speed) · [功率曲线建模](/power)
3. **从功率到电量。** 把长期风频与功率曲线结合，再区分设备表现、停机和限发造成的电量差。 [风频与 Weibull 拟合](/wind-frequency) · [风场运行后评估](/assessment)
4. **按问题回查。** 查看共振穿越、技改对照等专题，或下载公开记录复算。 [运行分析专题](/practice) · [方法选择与公开案例](/research)

</div>
