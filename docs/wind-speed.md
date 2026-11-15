# 现场测风对照与风速拟合

<script setup>
import { withBase } from 'vitepress'
import CaseWalkthrough from './.vitepress/theme/components/CaseWalkthrough.vue'
</script>

## 两路风速为何会不同 {#测风来源与元数据}

机舱测风系统和地基激光雷达观测的是不同位置的气流。遇到读数差异，先把测量条件摆在一起核对。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/wind-measurements.svg')" target="_blank" rel="noopener"><img src="/figures/wind-measurements.svg" width="720" height="338" loading="lazy" alt="从侧面画出测风塔上的风速测点、地基激光雷达的测层以及风机机舱后方的风速计。" /></a>
  <figcaption><strong>测风位置与高度</strong> 比较同期数据前，先按风向核对位置、测高和尾流影响。图中布置仅用于说明测点差异。</figcaption>
</figure>

机舱读数受安装位置附近的气流影响，雷达读数随测层高度和来流改变。比较前核对测点、测高、风向、质量标志和机舱读数的修正口径。

## 时间配对、偏差分析与拟合 {#怎样配对和拟合}

1. **对齐时间。** 统一时区、单位和[窗口起止时间](/scada#时间戳采样间隔与统计窗口)，按机组、测点和窗口配对，记录有效配对数。
2. **先看差异。** 用时序找缺测和错位，用散点看两路是否接近。原始差值按“机舱风速 − 雷达风速”计算。
3. **确定拟合方向。** 用机舱风速估算雷达风速时，机舱为输入，雷达为目标。以机舱原值为基准，可比较减去拟合段平均差值与直线拟合两种方法。

## 独立时段验证与适用范围

用较早时段估计修正量和模型参数，再用独立的后续时段检验。令每个验证窗口的误差为“估算风速 − 雷达风速”，用同一批窗口计算两项指标。

| 指标 | 计算方法 | 判读 |
| --- | --- | --- |
| 平均有符号误差 | 直接对误差取均值 | 正值表示整体偏高，负值表示整体偏低。正负误差可能相互抵消。 |
| 平均绝对误差（MAE） | 对每个误差取绝对值后再平均 | 数值越大，表明单窗估算通常偏离得越多。 |

用同一批处在拟合范围内的窗口比较，范围外的记录单列。用于其他机组或时段前，复核风速和风向覆盖。

## 实测案例：时间对齐与散点图判读 {#怎样读两路风速配对散点图}

AWAKEN 案例比较 A1 地基雷达 80 m 层与 WT041 的机舱数据。发布方已经用机舱风速传递函数修正 WT041 的风速，发布字段对应轮毂高度（约 89 m）。两路观测的地点和高度不同，拟合描述的是这两个测点在本案例条件下的关系。

<CaseWalkthrough example="pairing" />

[WT041 分钟记录](/data/awaken-wt041-scada-1min.csv) · [A1 雷达窗口记录](/data/awaken-a1-lidar-80m-10min.csv)

144 个窗口中有 131 个可用。窗口起点在 16:00 UTC 之前的 93 个用于拟合，从 16:00 UTC 起的 38 个用于留出验证。下面以机舱风速为横轴输入、雷达风速为纵轴目标。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/wind-pairs.png')" target="_blank" rel="noopener"><img src="/figures/wind-pairs.png" width="1050" height="615" loading="lazy" alt="AWAKEN 机舱与雷达风速配对散点，青绿实心点用于拟合，蓝色空心点用于验证，灰色虚线为等值线，橙色线为拟合结果。" /></a>
  <figcaption><strong>两路风速对照与拟合</strong> 点在等值线下方时，机舱风速高于雷达风速。例如 16:00 UTC 窗口两者分别为 6.94 和 6.10 m/s。</figcaption>
</figure>

38 个验证窗口中有 37 个落在拟合所用的机舱风速范围内。误差图和下表均使用这 37 个共同窗口。 [风速配对数据](/data/awaken-a1-wt041-2023-08-24.csv)

<figure class="tutorial-figure">
  <a :href="withBase('/figures/wind-fit-errors.png')" target="_blank" rel="noopener"><img src="/figures/wind-fit-errors.png" width="1050" height="615" loading="lazy" alt="共同窗口的估算误差对照。横轴为机舱风速，纵轴为估算风速减雷达风速，图中比较直接使用机舱风速与直线拟合。" /></a>
  <figcaption><strong>留出窗口的风速估算误差</strong> 点离零线越近，估算误差越小。蓝叉为直接使用机舱读数，青绿空心点为拟合结果。</figcaption>
</figure>

| 估算方法 | 共同窗口 MAE（m/s） | 平均有符号误差（m/s） |
| --- | ---: | ---: |
| 直接使用机舱风速 | 0.81 | −0.44 |
| 机舱风速减去拟合段的平均差值 0.29 m/s | 0.97 | −0.73 |
| 雷达估算值 ≈ 0.223 × 机舱风速 + 5.177 m/s | 0.69 | +0.18 |

这个案例中，直线拟合把 MAE 从 0.81 降到 0.69 m/s，估算平均偏高 0.18 m/s。换用其他时段时，按风速段和风向重新检查误差。
