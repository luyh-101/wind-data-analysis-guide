# 风机运行工况与变桨故障排查

<script setup>
import { withBase } from 'vitepress'
import TeachingFigure from './.vitepress/theme/components/TeachingFigure.vue'
</script>

## 风机怎样把风转化为电能

气流带动由叶片和轮毂组成的**风轮**旋转。风轮直接或经传动系统带动发电机，把机械能转成电能。单片叶片还可以绕从叶根到叶尖的长轴转动，这个动作叫**变桨**。

<figure class="tutorial-figure">
  <a :href="withBase('/figures/pitch-concept.svg')" target="_blank" rel="noopener"><img src="/figures/pitch-concept.svg" width="720" height="668" loading="lazy" alt="上层画出三片叶片绕风轮轴转动、风从叶片一侧吹向机舱以及机舱内发电机。下层沿单片叶片长轴看翼型截面，用橙色圆弧标出基准方向到当前方向的夹角。" /></a>
  <figcaption><strong>风轮旋转与单片叶片变桨</strong> 风轮旋转时，叶尖绕轮毂移动。变桨时，从叶尖沿长轴看，看到的是同一片叶片的截面相对于基准方向转过的角度。</figcaption>
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

## 用三张散点图认识运行工况 {#运行参数图谱}

下面三张图用的是同一台小型机组的公开运行记录。每个点代表一个时段，三张图各从该时段选两个运行量作横纵坐标。绿色是正功率，棕色是零或负功率。先看点群的形状，再从时间戳回查同一条记录。

<TeachingFigure src="/figures/aventa-wind-speed.png" :width="1020" :height="562" title="先用风速和转速找平台" alt="低风速段的转速点群向上延伸，框内的高转速点群随风速增加仍接近水平。">
  看右上方框内的横向点群。风速继续升高，转速仍集中在较窄的范围，这就是转速平台。图中的转速数值只适用于该机组。
</TeachingFigure>

<TeachingFigure src="/figures/aventa-speed-power.png" :width="1020" :height="562" title="再看平台上的功率" alt="右上角框内的功率点在相近发电机转速下仍分布在不同高度。">
  把第一张图中的平台转速移到这张图的横轴。右上框内的点在相近转速下仍有高低，判断出力时要直接读纵轴的功率。
</TeachingFigure>

<TeachingFigure src="/figures/aventa-wind-pitch.png" :width="1020" :height="562" title="最后看同一风速下的桨距角" alt="左侧低风速区出现多条不同高度的窄点带，其中较高的棕色点带对应零或负功率记录。">
  看左侧，同一风速附近的桨距角排成几条窄带，这就是分层。上面的棕色点带对应零或负功率，先把这些时段与正常发电分开，再到<a :href="withBase('/pitch.html')">变桨章节</a>学习怎样比较同工况下的角度。
</TeachingFigure>
