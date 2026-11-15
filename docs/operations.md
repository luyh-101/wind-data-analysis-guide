# 风机运行工况与变桨故障排查

<script setup>
import { withBase } from 'vitepress'
</script>

## 风机怎样把风转化为电能

气流带动由叶片和轮毂组成的**风轮**旋转。风轮直接或经传动系统带动发电机，把机械能转成电能。单片叶片还可以绕从叶根到叶尖的长轴转动，这个动作叫**变桨**。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/pitch-concept.svg')" target="_blank" rel="noopener"><img src="/figures/pitch-concept.svg" width="720" height="668" loading="lazy" alt="上层画出三片叶片绕风轮轴转动、风从叶片一侧吹向机舱以及机舱内发电机。下层沿单片叶片长轴看翼型截面，用橙色圆弧标出基准方向到当前方向的夹角。" /></a>
  <figcaption><strong>风轮旋转与单片叶片变桨</strong> 从迎风面看三片叶片一起旋转，再沿单片叶片长轴看同一翼型截面转过的角度。</figcaption>
</figure>

### 四个常用运行量

<dl class="quantities">
  <div><dt>风速（m/s）</dt><dd>测点处气流运动的速度。</dd></div>
  <div><dt>发电机转速（r/min）</dt><dd>发电机转子每分钟转过的圈数。</dd></div>
  <div><dt>桨距角（°）</dt><dd>叶片相对于基准位置绕自身长轴转过的角度。零位与正方向由机型定义，变桨会改变叶片的迎风姿态和吸收的风能。</dd></div>
  <div><dt>有功功率（kW）</dt><dd>机组实际输出电能的速率，发电时也称出力。</dd></div>
</dl>

## 典型运行工况

达到**切入风速**后，机组具备启动发电的风速条件。正常发电的上升段里，转速和功率通常随风速升高。达到额定功率所对应的风速称为**额定风速**。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/operation-trends.svg')" target="_blank" rel="noopener"><img src="/figures/operation-trends.svg" width="720" height="532" loading="lazy" alt="三个面板共用风速轴。切入前通常不发电，切入后转速和功率上升。图中转速先趋于稳定，功率随后达到额定值，变桨调节在额定附近及以上更明显。" /></a>
  <figcaption><strong>变速变桨机组的典型运行趋势</strong> 若转速先达到控制目标，发电机扭矩还可继续增大，功率就会在转速趋稳后继续上升。接近额定功率时，变桨通过调节风轮吸收的能量来限制转速和出力。</figcaption>
</figure>

工况是机组当时所处的运行状态。下表列出各类工况在运行记录中的典型表现。

| 运行工况 | 运行特点 | 数据中可能出现的现象 |
| --- | --- | --- |
| 待机与启停 | 切入前通常待机，启停时控制量随过程调整。 | 待机功率接近零。启停时功率、转速或桨距角连续变化。 |
| 额定风速以下正常发电 | 随来流调整转速和发电机扭矩。 | 功率点带总体向上，变速机组通常有转速上升段。 |
| 额定风速附近及以上正常发电 | 通过变桨等方式限制转速和功率。 | 功率在额定值附近波动，桨距角随风速调整。 |
| 限功率与降额 | 调度要求或设备、环境约束使功率上限降低。 | 风速足够时，功率仍低于正常参考，或形成水平点带。 |
| 保护停机、故障停机与检修 | 保护动作、故障或计划检修使机组停机。 | 有风时也可出现低转速和零功率。按状态、告警与工单区分原因。 |

上游机组形成的**尾流**通常会降低下游的平均风速、增强湍流。尾流、地形和覆冰都可能影响出力，可以结合风向和运行事件复核。[SCADA 数据质量与工况筛选](/scada)

## 常用运行参数图表 {#运行参数图谱}

相似记录在散点图上排成的窄条叫**点带**。同一风速附近出现多个高度不同的桨距角点带，称为**分层**。

### 三张散点图的联合判读

三张图共用 Aventa AV-7 的 10,032 条分钟记录。绿色为正功率，棕色为零或负功率。点击图表可查看原图。[三图案例 CSV](/data/aventa-linked-scatter.csv)

<ol class="scatter-reading">
  <li><figure class="tutorial-figure"><a :href="withBase('/figures/wind-generator.png')" target="_blank" rel="noopener"><img src="/figures/aventa-wind-speed.png" width="1020" height="562" loading="lazy" alt="风速–发电机转速图框出了约 750–780 r/min 的水平点群。" /></a><figcaption><strong>先看风速–发电机转速</strong> 约 750–780 r/min 的横向点群标出案例中的高转速运行区间，可据此筛出平台段的记录。</figcaption></figure></li>
  <li><figure class="tutorial-figure"><a :href="withBase('/figures/generator-power.png')" target="_blank" rel="noopener"><img src="/figures/aventa-speed-power.png" width="1020" height="562" loading="lazy" alt="发电机转速–有功功率图框出了右侧同一转速附近纵向分散的功率点。" /></a><figcaption><strong>再看发电机转速–有功功率</strong> 转速平台对应的功率仍有高低。判断是否接近额定出力，要直接看功率列。</figcaption></figure></li>
  <li><figure class="tutorial-figure"><a :href="withBase('/figures/wind-pitch.png')" target="_blank" rel="noopener"><img src="/figures/aventa-wind-pitch.png" width="1020" height="562" loading="lazy" alt="风速–桨距角图框出了低风速的多条角度点带，其中约 39 度的一带有棕色记录。" /></a><figcaption><strong>最后对照风速–桨距角</strong> 低风速下出现多条角度带，约 39° 的点带含零功率记录。这些点带提供了按运行状态分组的线索。</figcaption></figure></li>
</ol>

用时间戳把三张图连起来。每张图从同一行取对应的两列来定位同一条记录。

| 时间（2025-06-04 UTC） | 风速（m/s） | 发电机转速（r/min） | 功率（kW） | 桨距角（°） |
| --- | ---: | ---: | ---: | ---: |
| 21:44 | 5.61 | 753 | 6.12 | 17.16 |
| 00:00 | 1.27 | 0 | 0 | 38.86 |

21:44 在第一张图位于约 753 r/min 的平台段，第二张图对应 6.12 kW，接近该机组 6 kW 的标称功率。00:00 的转速和功率均为零，第三张图中约 39° 的桨距角对应这里的一条非发电记录。

[跨机组出现不同点带时的判读方法](/practice#控制表现与多信号复核)

## 变桨故障线索与复核

相近风速下，桨距角持续偏离原有点带或某一片叶片与其他叶片出现持续差异，都值得标为候选。第三章用[分箱参考范围](/pitch#正常工况基线与候选事件)筛查偏离，再用[逐叶片指令和反馈](/pitch#变桨监测方法与选用条件)复核。

## 测量与分析工具

SCADA 提供运行量和状态，控制器与工单提供事件记录。电子表格便于查阅样本，Python 适合批量统计和制图。
