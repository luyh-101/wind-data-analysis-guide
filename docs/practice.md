# 运行分析专题

<script setup>
import { withBase } from 'vitepress'
</script>

当散点图出现分层或出力偏离时，可用时序定位变化，再用控制记录核对。

## 控制表现与多信号复核

相近风速下出现多条点带时，先按状态、功率设定和控制版本分组。用[三张散点图](/operations#三张散点图的联合判读)找出差异，再从同一时间轴回看运行量、指令和反馈。

下图对齐 Aventa 在 2025 年 6 月 4 日的四路分钟信号，浅色标出连续正功率的窗口。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/aventa-synchronized-signals.png')" target="_blank" rel="noopener"><img src="/figures/aventa-synchronized-signals.png" width="1050" height="990" loading="lazy" alt="Aventa 在 05:23 至 05:37 UTC 的四路同步时序。05:27 风速和转速上升、功率转正、桨距角下降，绿色条标出连续正功率窗口。" /></a>
  <figcaption><strong>对齐风速、功率、转速与桨距角</strong> 从 05:27 UTC 起，几路信号在相邻分钟内一起变化。图中时段按功率标记，具体状态要回查控制器或事件记录。</figcaption>
</figure>

[Aventa 分钟运行数据](/data/aventa-linked-scatter.csv)

### 转速–扭矩与共振穿越 {#转速扭矩与共振穿越}

在某些转速区间内，机组振动可能因共振增大。按机组资料确定区间，转速与扭矩取同一传动轴侧，例如都取发电机侧。

1. **在散点图上找区间。** 横轴为转速，纵轴为扭矩，标出规定的区间并回查时间戳。
2. **用时序识别穿越。** 从另一侧离开记为完整穿越，从同侧离开记为折返。停留时间等于退出时刻减进入时刻，短时穿越需要足够密的原始记录。
3. **复核同期信号。** 对照扭矩、振动、状态和告警，区分工况切换与持续偏离。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/resonance-crossing-timeline.svg')" target="_blank" rel="noopener" aria-label="在新标签页打开完整穿越时序图"><img src="/figures/resonance-crossing-timeline.svg" width="720" height="383" loading="lazy" alt="共振区间为 9 至 11 转每分钟。转速时序从下方穿到上方，两个橙点分别表示约 0.67 秒进入和 2.33 秒退出。" /></a>
  <figcaption><strong>转速区间的进入与退出</strong> 用相邻采样点估计边界时刻。本例区间内停留约 1.67 秒。</figcaption>
</figure>

::: details 穿越事件的识别与时间计算

1. **划分连续片段。** 按机组和时间排序。遇到记录缺失、时间间隔超过允许值、工况切换或控制版本切换时断开。允许间隔应根据原始采样周期确定。按技术文件的转速下限和上限，把有效样本分为区间下方、区间内和区间上方，等于边界的样本计入区间内。
2. **记录进入和退出。** 从某一侧进入区间时，记下进入侧及时间。回到同一侧记为折返，从另一侧离开记为完整穿越。片段开始或结束时已在区间内、途中发生中断，分别标记缺少进入或退出边界。相邻采样点直接从一侧跳到另一侧时，标记为“跨区、无区间内样本”，单列其时间分辨率。
3. **计算停留时间。** 进入和退出的实际时刻各落在一对采样点之间。采样足够密且局部转速近似连续时，可在相邻点之间插值求过界时刻。完整穿越的时长为退出时刻减进入时刻。注明估计方法、采样间隔、方向和状态。

:::

变桨反馈迟滞时，可回查同期驱动电流、温度与告警。低出力事件的分段计量见[发电量损失与低效分析](/assessment#发电量损失与低效分析)。

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

::: details 逐叶片散点图的 Python 示例

下载站内逐叶片 CSV 后，将它与脚本放在同一目录。示例用 pandas 和 Matplotlib，机组间共享坐标轴，三片叶片共用配色规则。

```python
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("kelmarsh-blade-pitch.csv")
turbines = list(data.groupby("turbine", sort=True))
fig, axes = plt.subplots(
    1, len(turbines), squeeze=False, sharex=True, sharey=True, layout="constrained"
)
for ax, (turbine, rows) in zip(axes[0], turbines):
    for blade, color in zip("abc", ["#3069a2", "#d38124", "#1e836a"]):
        ax.scatter(
            rows["wind_ms"], rows[f"pitch_{blade}_deg"],
            s=7, alpha=0.35, color=color, label=f"Blade {blade.upper()}"
        )
    ax.set(title=turbine, xlabel="Wind speed (m/s)")
axes[0, 0].set_ylabel("Pitch angle (deg)")
axes[0, 0].legend()
plt.show()
```

局部比较时，在两台机组上使用相同的风速与桨距角显示区间。查询点带时用同一区间筛选原表，并回到相邻窗口检查工况。 [逐叶片案例 CSV](/data/kelmarsh-blade-pitch.csv)

:::
