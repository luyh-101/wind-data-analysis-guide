# 变桨状态监测与异常筛查

<script setup>
import { withBase } from 'vitepress'
</script>

同一风速下，待机、限功率和发电时的桨距角可能不同。先用可比工况建立角度**基线**，再把偏离基线的记录列为候选，回查时序与设备记录。

## 监测数据与证据

角度数据的粒度决定能定位到哪一步。以下分析都需要机组编号和时间戳。

| 想判断什么 | 需要的信号 | 先看哪里 |
| --- | --- | --- |
| 相近风速下有没有偏离 | 风速、实测角度、运行状态或事件 | 用正常发电样本建基线，叠加待查记录。用转速和功率设定区分控制阶段。 |
| 哪一片叶片偏离 | 同一时刻的逐叶片反馈角 | 在可比的控制条件下，比较三片叶片的角度。 |
| 叶片有没有跟上指令 | 同一叶片的同步指令和反馈，采样间隔足以分辨动作 | 在时序上找指令变化的时刻，查看反馈随后怎样变化。 |

## 正常工况基线与候选事件

1. **选正常时段。** 用整机状态和事件选出正常发电记录，按机组、叶片和控制条件分开。
2. **按风速分箱。** 例如 `[8, 9) m/s`。每箱用中位数描述典型角度，第 5 至第 95 百分位作为参考范围，样本不足的箱单列。
3. **筛查后续记录。** 用各自风速箱的参考范围标记偏离，再看是否持续、是否只出现在某片叶片上。遇缺测或工况切换时分段。

若同一风速箱内仍有不同点带，再按转速、功率或设定值分组。

## 风速–桨距角散点图判读

看相近风速下的角度点带，再按时间戳核对状态。连续偏离需回到时间序列判断。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/pitch-scatter.png')" target="_blank" rel="noopener"><img src="/figures/pitch-scatter.png" width="1110" height="690" loading="lazy" alt="ENGIE 风速–桨距角全范围散点，阴影标出 8 至 9 m/s 箱，橙色菱形标出三个候选窗口。" /></a>
  <figcaption><strong>ENGIE 风速–桨距角散点</strong> 每点对应一个 10 分钟窗口，角度来自汇总字段 <code>Ba_avg</code>。先用字段齐全且功率为正筛出参考记录，现场分析还要用状态和事件确认工况。</figcaption>
</figure>

### 实测案例：分段参考范围 {#建参考范围并手算一次}

2 月 8–9 m/s 风速箱有 442 条参考样本，中位数为 −0.99°，第 5 至第 95 百分位约为 −0.99° 至 −0.90°。下图将该风速箱的低角度区域放大。绿色带表示 2 月的参考范围，橙色菱形标出 3 月略高于上界的三个窗口。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/pitch-reference-zoom.png')" target="_blank" rel="noopener"><img src="/figures/pitch-reference-zoom.png" width="945" height="600" loading="lazy" alt="放大 8 至 9 m/s 箱的低桨距角范围，三个橙色候选点略高于浅绿色参考带。" /></a>
  <figcaption><strong>8–9 m/s 风速箱的候选窗口</strong> 用下表核对越界量，再回查前后窗口各自所在的风速箱。</figcaption>
</figure>

| 记录时间（UTC） | 风速（m/s） | 桨距角（°） | 高于上界（°） |
| --- | ---: | ---: | ---: |
| 2014-03-03 05:00 | 8.97 | −0.86 | 0.04 |
| 2014-03-21 11:30 | 8.86 | −0.85 | 0.05 |
| 2014-03-22 10:00 | 8.52 | −0.86 | 0.04 |

这些候选窗口的偏离约为 0.04–0.05°，解释时要结合角度读数精度、运行状态和前后变化。以 3 月 21 日 11:30 为例，前后两个窗口的风速分别为 10.50 和 11.12 m/s，应分别查各自风速箱的参考范围，再判断偏离是否持续。 [ENGIE 案例 CSV](/data/engie-r80711-2014-02-03.csv)

## 逐叶片和跨机组对照

共同变桨时，可用同一时刻三片反馈角的最大值减最小值来找分歧。各叶片指令不同时，分别比较各自的指令和反馈。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/blade-pitch-comparison.png')" target="_blank" rel="noopener"><img src="/figures/blade-pitch-comparison.png" width="1280" height="976" loading="lazy" alt="左右列分别是 Kelmarsh 1、2 号机组的逐叶片角度，上排显示全范围，下排放大两台机组的 2 至 6 m/s 低角度区域。" /></a>
  <figcaption><strong>Kelmarsh 逐叶片及跨机组对照</strong> 先看同一机组三片点带的位置，再比较两台机组在同一风速、转速和设定下的差异。两台均用 2016 年 7 月的正功率窗口。</figcaption>
</figure>

[Kelmarsh 逐叶片数据](/data/kelmarsh-blade-pitch.csv)

## 指令跟踪与事件复核 {#变桨监测方法与选用条件}

沿同一时间轴对照逐叶片指令和反馈。共同指令变化时，先比较各片跟踪的方向和持续时间。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/pitch-following-patterns.svg')" target="_blank" rel="noopener"><img src="/figures/pitch-following-patterns.svg" width="720" height="360" loading="lazy" alt="左图三片在共同指令升高后同步跟随，右图叶片 1 和 2 跟随，叶片 3 反馈仍停在原位置。" /></a>
  <figcaption><strong>多片同步变化与单片持续偏离</strong> 指令改变后留出机型规定的响应时间，再判断反馈是否持续偏离。</figcaption>
</figure>

再按下图逐步核对记录，判断偏离与跟踪表现、整机工况或测量信号的关系。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/pitch-screening-workflow.svg')" target="_blank" rel="noopener"><img src="/figures/pitch-screening-workflow.svg" width="720" height="293" loading="lazy" alt="从散点标记候选后，依次检查原始时序、叶片指令和反馈、告警与工况，结合事件和检修给出判断。" /></a>
  <figcaption><strong>变桨异常筛查流程</strong> 对同一候选时段汇集证据。若同期功率偏低，可与相似工况的参考功率进一步对照。</figcaption>
</figure>

### 候选事件记录 {#事件复核与检测验证}

合并连续候选窗口，记录机组、叶片、起止时间、工况、最大偏离和复核依据。
