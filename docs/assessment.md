# 风场运行后评估

<script setup>
import { withBase } from 'vitepress'
import TeachingFigure from './.vitepress/theme/components/TeachingFigure.vue'
</script>

风场运行后评估比较同一历史时段的**参考发电量和实际发电量**，找出差距集中在哪些时段。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/assessment-workflow.svg')" target="_blank" rel="noopener"><img src="/figures/assessment-workflow.svg" width="720" height="293" loading="lazy" alt="用同期实测风速和验证过的功率曲线估算参考功率，换算为参考电量，与实际电量对照，再回查差距大的时段。" /></a>
  <figcaption><strong>从现场测风到同期电量对照</strong> 参考电量与实际电量对齐后，再结合运行记录查原因。</figcaption>
</figure>

## 怎么计算同期电量差 {#怎么计算同期电量差}

1. **先估算参考功率。** 把现场已测风速代入与测风来源相匹配、已经验证过的[功率曲线](/power)，得到同一时间段的参考功率。
2. **算参考电量和实际电量。** 每段平均功率（kW）乘以持续的小时数，就是电量（kWh）。实际发电量优先看计量记录。若给的是累计电量，核对计量连续后，用时段末读数减去起始读数。只有同期实测平均功率时，也可乘时长换算。
3. **在相同范围内比较。** 按同一机组或同一计量范围，汇总两边都有有效结果的时段。用 **参考电量 − 实际电量** 算差值，注明比较覆盖了多长时间。供应商给的资料要先确认是实测值还是参考值。

## 有差距就回查对应时段

例如，四个连续时段合计参考电量为 **1,000 度**，实发电量为 **600 度**。要解释这 **400 度**，先把两种电量按时段画在一起。

<TeachingFigure src="/figures/energy-gap-reading.png" :width="1020" :height="580" title="总电量有差距，先找差距集中的时段" alt="四组柱逐小时对照参考电量和实发电量。10 时至 11 时、11 时至 12 时的两根柱高度差最大。图为示意。">
  看同组两根柱的高度差。示意中 10:00–12:00 的两个时段合计相差 350 度，优先回查这两个时段的限功率、停机或检修记录，同时核对测风、计量范围和模型误差。
</TeachingFigure>

如果在可比条件下仍反复出现明显差距，把对应时段、功率曲线和运行记录交给现场及厂商核查。确认与控制设置有关后，再提出调整要求。

一度电等于 1 kWh。报告写清**参考发了多少、实际发了多少、哪些时段需要核查**。超出模型适用范围或数据缺失的时段单列。
