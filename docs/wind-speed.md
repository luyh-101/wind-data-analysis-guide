# 现场测风对照与风速拟合

<script setup>
import { withBase } from 'vitepress'
import CaseWalkthrough from './.vitepress/theme/components/CaseWalkthrough.vue'
</script>

## 两路风速为何会不同 {#测风来源与元数据}

机舱风速和地基激光雷达风速来自不同位置。建立两路读数的对应关系，可判断它们能否直接用于同一种分析，或是否需要先换算。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/wind-measurements.svg')" target="_blank" rel="noopener"><img src="/figures/wind-measurements.svg" width="720" height="338" loading="lazy" alt="从侧面画出测风塔上的风速测点、地基激光雷达的测层以及风机机舱后方的风速计。" /></a>
  <figcaption><strong>测风位置与高度</strong> 机舱读数受安装位置附近的气流影响，雷达反映其测层的风况。位置和高度不同，同一时窗的两路读数也可能有差别。</figcaption>
</figure>

## 时间配对、偏差分析与拟合 {#怎样配对和拟合}

1. **按窗口配对。** 统一时区和单位，将分钟数据汇总到 [SCADA 时间窗口](/scada#时间戳采样间隔与统计窗口)。雷达若用中点标记，先换成窗口起点，再按机组、测点和窗口配对。
2. **先看差异。** 用时序找缺测和错位，用散点看两路是否接近。原始差值按“机舱风速 − 雷达风速”计算。
3. **确定拟合方向。** 用机舱风速估算雷达风速时，机舱为输入，雷达为目标。以机舱原值为基准，可比较减去拟合段平均差值与直线拟合两种方法。

## 独立时段验证与适用范围

拟合段用来定修正量、斜率和截距。留出段只用来计算误差，参数在这一步保持固定。每窗的误差取“估算风速 − 雷达风速”。

| 指标 | 计算方法 | 判读 |
| --- | --- | --- |
| 平均有符号误差 | 直接对误差取均值 | 正值表示整体偏高，负值表示整体偏低。正负误差可能相互抵消。 |
| 平均绝对误差（MAE） | 对每个误差取绝对值后再平均 | 数值越大，表明单窗估算通常偏离得越多。 |

用同一批处在拟合范围内的窗口比较，范围外的记录单列。用于其他机组或时段前，复核风速和风向覆盖。

## 实测案例：时间对齐与散点图判读 {#怎样读两路风速配对散点图}

本例对照 A1 雷达 80 m 层风速与 WT041 修正后的机舱风速。后者来自 SCADA，发布时已通过机舱风速传递函数换算为约 89 m 轮毂高度的风速。

<CaseWalkthrough example="pairing" />

[WT041 分钟记录](/data/awaken-wt041-scada-1min.csv) · [A1 雷达窗口记录](/data/awaken-a1-lidar-80m-10min.csv)

144 个窗口中有 131 个可用。16:00 UTC 之前的 93 个用于拟合，从 16:00 UTC 起的 38 个用于留出验证。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/wind-pairs.png')" target="_blank" rel="noopener"><img src="/figures/wind-pairs.png" width="1050" height="615" loading="lazy" alt="AWAKEN 机舱与雷达风速配对散点，青绿实心点用于拟合，蓝色空心点用于验证，灰色虚线为等值线，橙色线为拟合结果。" /></a>
  <figcaption><strong>两路风速对照与拟合</strong> 横轴为机舱风速，纵轴为雷达风速。1:1 线表示两者相等，拟合线给出按机舱风速估计雷达读数的结果。16:00 UTC 的点位于 1:1 线下方，机舱读数 6.94 m/s 高于雷达的 6.10 m/s。</figcaption>
</figure>

38 个验证窗口中有 37 个落在拟合所用的机舱风速范围内。误差图和下表均使用这 37 个共同窗口。 [风速配对数据](/data/awaken-a1-wt041-2023-08-24.csv)

<figure class="tutorial-figure">
  <a :href="withBase('/figures/wind-fit-errors.png')" target="_blank" rel="noopener"><img src="/figures/wind-fit-errors.png" width="1050" height="615" loading="lazy" alt="37 个共同验证窗口的绝对误差变化。横轴为窗口次序，纵轴为拟合后的绝对误差减去直接用机舱风速的绝对误差。零线以下有 21 柱，以上有 16 柱。" /></a>
  <figcaption><strong>拟合在每个窗口改善了多少</strong> 每根柱比较同一窗。零线以下表示拟合后误差变小，以上表示变大。这 37 个窗口中有 21 个改善、16 个变差。</figcaption>
</figure>

| 估算方法 | 共同窗口 MAE（m/s） | 平均有符号误差（m/s） |
| --- | ---: | ---: |
| 直接使用机舱风速 | 0.81 | −0.44 |
| 机舱风速减去拟合段的平均差值 0.29 m/s | 0.97 | −0.73 |
| 雷达估算值 ≈ 0.223 × 机舱风速 + 5.177 m/s | 0.69 | +0.18 |

表中直线拟合的 MAE 最低，为 0.69 m/s，但图上仍有部分窗口误差增大。固定修正则加重了这一天的整体低估。选模型时，可先用 MAE 排序，再检查误差增大的窗口是否集中在项目关心的风速段。
