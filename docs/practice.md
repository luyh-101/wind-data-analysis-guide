# 运行分析专题

<script setup>
import { withBase } from 'vitepress'
</script>

## 控制表现与多信号复核

散点图能指出哪些变量一起变化。按时间戳对齐后，可以进一步定位变化开始的时刻、各信号变化的先后和持续时间。

下图对齐 Aventa 在 2025 年 6 月 4 日的四路分钟信号。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/aventa-synchronized-signals.png')" target="_blank" rel="noopener"><img src="/figures/aventa-synchronized-signals.png" width="1050" height="990" loading="lazy" alt="Aventa 在 05:23 至 05:37 UTC 的四路同步时序。05:27 风速和转速上升、功率转正、桨距角下降，绿色条标出连续正功率窗口。" /></a>
  <figcaption><strong>对齐风速、功率、转速与桨距角</strong> 从 05:27 UTC 起的浅色区域标出连续正功率窗口，可直接用该起点定位原始记录。同一分钟内各动作的先后需用更高频的记录查看。</figcaption>
</figure>

[Aventa 分钟运行数据](/data/aventa-linked-scatter.csv)

### 转速–扭矩与共振穿越 {#转速扭矩与共振穿越}

在某些转速区间内，机组振动可能因共振增大。按机组资料确定区间，转速与扭矩取同一传动轴侧。

1. **在散点图上找区间。** 横轴为转速，纵轴为扭矩，标出规定的区间并回查时间戳。
2. **用时序识别穿越。** 从另一侧离开记为完整穿越，从同侧离开记为折返。停留时间等于退出时刻减进入时刻，短时穿越需要足够密的原始记录。
3. **复核同期信号。** 对照扭矩、振动、状态和告警，区分工况切换与持续偏离。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/resonance-crossing-timeline.svg')" target="_blank" rel="noopener" aria-label="在新标签页打开完整穿越时序图"><img src="/figures/resonance-crossing-timeline.svg" width="720" height="383" loading="lazy" alt="共振区间为 9 至 11 转每分钟。转速时序从下方穿到上方，两个橙点分别表示约 0.67 秒进入和 2.33 秒退出。" /></a>
  <figcaption><strong>转速区间的进入与退出</strong> 用相邻采样点估计边界时刻。本例区间内停留约 1.67 秒。</figcaption>
</figure>

采样足够密且边界附近转速近似连续时，在跨越边界的两个相邻采样点之间作线性插值。缺失进入或退出边界的片段，以及直接从区间一侧跳到另一侧且没有区间内样本的片段，应单列。

## 技改对照方法

先确定技改时间、目标机组和可用参考数据，再选前后对照方法。

| 数据条件 | 对照方法 |
| --- | --- |
| 前后风速口径一致 | 用共同风速箱比较技改前后功率曲线。 |
| 有同期未技改机组 | 用技改前同期记录拟合参考机组到目标机组的功率关系。验证后用技改后的参考功率估算基准。 |
| 机舱测风变化，有稳定参考测风 | 先估计可比风速，再用统一口径绘制前后功率曲线。 |
| 缺少参考机组，有独立来流测风 | 选风速、风向和工况可比的时段比较电量。比较期风况分布不同时，按共同风况加权。 |

参考机组或测点需检查前后测风、尾流和调度条件。对照结果可按风速箱报告功率差和共同覆盖。

## 缺测处理与结果回查 {#缺测处理与分析工具验收}

保留缺测和补值标记，性能验证优先用实测记录。输出表保留时间、机组、工况和筛选理由，便于从图上的点回查原始记录。
