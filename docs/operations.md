# 风机运行工况与变桨故障排查

<script setup>
import { withBase } from 'vitepress'
</script>

## 风机怎样把风转化为电能

气流带动由叶片和轮毂组成的**风轮**旋转。风轮直接或经传动系统带动发电机，把机械能转成电能。单片叶片还可以绕从叶根到叶尖的长轴转动，这个动作叫**变桨**。

<input class="motion-toggle" id="operations-still-motion" type="checkbox" />
<label class="motion-label" for="operations-still-motion">显示静态画面</label>
<figure class="pitch-angle">
  <a :href="withBase('/figures/blade-pitch-angle-still.webp')" target="_blank" rel="noopener" aria-label="在新标签页打开桨距角示意大图">
    <picture class="motion-playing">
      <source media="(prefers-reduced-motion: no-preference)" srcset="/figures/blade-pitch-angle.webp" />
      <img src="/figures/blade-pitch-angle-still.webp" width="720" height="500" alt="上图标出叶片上的一个截面和从叶尖看向叶根的方向。下图沿长轴看这个截面，青色翼型绕黑点转动，灰色基准线固定。橙色夹角随之从 0 度增至 50 度。" />
    </picture>
    <img class="motion-still" src="/figures/blade-pitch-angle-still.webp" width="720" height="500" alt="沿叶片长轴看，青色截面的当前方向与灰色基准方向相差 50 度。这是示意角度。" />
  </a>
  <figcaption>上图标出观察位置。下图沿叶片长轴看，青色截面绕黑点转，灰色虚线固定。橙色圆弧标出的就是桨距角。</figcaption>
</figure>

<style scoped>
.pitch-angle {
  max-width: 720px;
  margin: 0;
}

.pitch-angle img {
  display: block;
  width: 100%;
  height: auto;
  background: var(--vp-c-bg-soft);
  border-radius: 8px;
}

.pitch-angle .motion-still,
.motion-toggle:checked ~ .pitch-angle .motion-playing {
  display: none;
}

.motion-toggle:checked ~ .pitch-angle .motion-still {
  display: block;
}

.motion-toggle {
  appearance: auto;
  accent-color: var(--vp-c-brand-1);
  margin-right: 0.45rem;
}

.motion-label {
  display: inline-block;
  margin-bottom: 0.75rem;
  color: var(--vp-c-text-2);
  cursor: pointer;
}

.pitch-angle figcaption {
  margin-top: 0.45rem;
}
</style>

### 四个常用运行量

- **风速**（m/s）表示测点处气流流动的快慢。比较机舱和激光雷达的风速时，要看测点位置和高度。
- **发电机转速**（r/min）是发电机转子每分钟转过的圈数。带齿轮箱的机组，发电机转速与风轮转速可能相差很大，画图前要核对字段的测点。
- **桨距角**（°）表示叶片相对零桨距位置绕自身长轴转过多少。沿长轴看同一个截面，比较它在当前姿态和基准姿态下的方向，就能量出这个角。变桨改变叶片迎风的姿态，调节风轮吸收的能量。实际机型各有自己的零位和正负方向。
- **有功功率**（kW）表示机组实际输出电能的速率，发电时常称为出力。分析时区分实测功率与控制系统给出的功率目标或上限。

## 典型运行工况

风速达到**切入风速**后，机组具备启动发电的风速条件。正常发电时，转速和功率通常随风速上升。转速在一段风速内基本不变，散点图上就会出现近水平的**转速平台**。达到**额定功率**所对应的风速称为**额定风速**，具体数值按机组的规定条件确定。

<figure>
  <a :href="withBase('/figures/operation-trends.svg')" target="_blank" rel="noopener" aria-label="在新标签页打开典型运行规律示意图"><img src="/figures/operation-trends.svg" width="720" height="520" alt="切入风速和额定风速把横轴分为三个阶段。切入前通常不发电。切入后转速和功率上升，示意中的转速先进入平台，功率随后达到额定值。接近和超过额定风速时，变桨调节更明显。" /></a>
  <figcaption>这张图示意转速先趋稳、功率随后达到额定值。接近额定风速后，通常能看到更明显的变桨调节。</figcaption>
</figure>

工况是机组当时所处的运行状态。相同风速下的待机、正常发电和限功率记录可能落在不同点带，比较前先查运行状态。

| 运行工况 | 运行特点 | 数据中可能出现的现象 |
| --- | --- | --- |
| 待机与启停 | 风速低于切入风速（机组开始发电所需的风速）时，机组通常待机。启动或停机时，转速和桨距角会随控制过程改变。 | 待机功率接近零。启停窗口内，功率、转速或桨距角可能连续变化。 |
| 额定风速以下正常发电 | 风机随风况调整运行点，功率通常随风速增加。 | 风速–功率散点总体呈上升趋势，变速机组的转速也常出现上升段。 |
| 额定风速附近及以上正常发电 | 达到额定输出后，机组通过变桨等调节将转速和功率控制在允许范围内。 | 功率多在额定值附近波动。桨距角可能继续随风速改变。 |
| 限功率与降额 | 调度限发会降低功率上限，设备或环境条件也可能使机组主动降低可输出功率，即降额。 | 风速足以发电时，功率仍可能低于正常发电样本，或在某一水平形成密集点带。 |
| 保护停机、故障停机与检修 | 高风速保护、故障或计划检修都可能使机组停机。 | 有风时也可能出现低转速、零功率和停机桨距角。结合状态、告警与工单区分原因。 |

上游机组形成的**尾流**通常会降低下游的平均风速、增强湍流。尾流、地形和覆冰都可能影响出力，可以结合风向和运行事件复核。[SCADA 数据质量与工况筛选](/scada)

## 常用运行参数图表 {#运行参数图谱}

相似记录在散点图上排成的窄条叫**点带**。同一风速附近出现几条高度不同的桨距角点带，就是**分层**。下面用同一批记录画三张图，看看各自能读出什么。

### 三张散点图的联合判读

三张图共用 Aventa AV-7 的 10,032 条分钟记录。绿色为正功率，棕色为零或负功率。点击图表可查看原图。[三图案例 CSV](/data/aventa-linked-scatter.csv)

<div class="linked-scatter-grid">
  <figure><a :href="withBase('/figures/wind-generator.png')" target="_blank" rel="noopener" aria-label="在新标签页打开风速–发电机转速原图"><img src="/figures/wind-generator-guide.png" width="656" height="496" alt="风速和发电机转速散点图，角框标出上方近水平的转速平台。" /></a><figcaption>1. 风速–发电机转速<br />上方约 750–780 r/min 形成平台</figcaption></figure>
  <figure><a :href="withBase('/figures/generator-power.png')" target="_blank" rel="noopener" aria-label="在新标签页打开发电机转速–有功功率原图"><img src="/figures/generator-power-guide.png" width="656" height="496" alt="发电机转速和有功功率散点图，角框标出右侧相近转速下的功率差异。" /></a><figcaption>2. 发电机转速–有功功率<br />看右侧相近转速下的功率差异</figcaption></figure>
  <figure><a :href="withBase('/figures/wind-pitch.png')" target="_blank" rel="noopener" aria-label="在新标签页打开风速–桨距角原图"><img src="/figures/wind-pitch-guide.png" width="656" height="496" alt="风速和桨距角散点图，角框标出低风速处不同高度的桨距角点带。" /></a><figcaption>3. 风速–桨距角<br />左侧约 39° 的点带含零功率记录</figcaption></figure>
</div>

用时间戳把三张图连起来。每张图从同一行取对应的两列来定位同一条记录。

| 时间（2025-06-04 UTC） | 风速（m/s） | 发电机转速（r/min） | 功率（kW） | 桨距角（°） |
| --- | ---: | ---: | ---: | ---: |
| 21:44 | 5.61 | 753 | 6.12 | 17.16 |
| 00:00 | 1.27 | 0 | 0 | 38.86 |

21:44 的记录在第一张图靠近转速平台，在第三张图落在较低的角度带。00:00 的零功率记录则落在约 39° 的角度带。要判断后一条为何没有发电，回查前后几分钟的状态码或事件。机组额定参数按设备资料确定。

桨距角与功率是否同时偏离，可以在相近风速、转速和工况下补看桨距角–功率图。风速–功率图的典型形状、建模和验证见 [功率曲线建模与验证](/power)。

### 跨机组控制差异判读

先选机型、测点和运行条件可比的机组，再用同一时间范围、统一坐标分别出图。若转速平台或低速点带出现差异，先查启停比例、功率设定及控制版本，再将差异对应到原始时序。 [运行分析专题](/practice#控制表现与多信号复核)

## 变桨故障线索与复核

散点图适合筛查，判断叶片有没有跟上指令要回到时序。下面示意三片叶片收到相同指令时的两种走势。

<figure>
  <a :href="withBase('/figures/pitch-following-patterns.svg')" target="_blank" rel="noopener" aria-label="在新标签页打开变桨指令与反馈示意图"><img src="/figures/pitch-following-patterns.svg" width="720" height="340" loading="lazy" alt="左图三片叶片的实际角度几乎重合，均跟上指令。右图有两片跟上，叶片 3 的实际角度仍停在原位置。" /></a>
  <figcaption>判读示意。指令升高后，右图中叶片 3 的反馈角仍停在原位置。</figcaption>
</figure>

单片长期偏离时，查该叶片的指令、反馈和告警。多片同步变化时，先查整机工况、功率设定和共同指令。驱动和角度测量问题都可能表现为偏离，可结合时序与检修记录复核。[变桨状态监测与异常筛查](/pitch)

## 测量与分析工具

用 SCADA（监控与数据采集系统）查看运行量和状态，用控制器记录、告警、检修工单复核事件。测风塔、激光雷达和机舱风速计提供不同位置的风速观测。电子表格适合初看数据，Python 可批量清洗、绘图和统计，OpenOA 可用于风场运行评估。
