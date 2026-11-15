# 方法选择与公开案例

<script setup>
import { withBase } from 'vitepress'
</script>

## 分析目标与方法选择

<div class="method-map">
  <strong>要回答什么问题？</strong>
  <ul>
    <li><strong>桨距角是否偏离？</strong><span>风速、桨距角、工况。定位到单片时需要逐叶片数据。</span><a :href="withBase('/pitch.html')">变桨分析</a></li>
    <li><strong>两路风速是否可比？</strong><span>两路同期风速、测点及窗口口径。</span><a :href="withBase('/wind-speed.html')">风速拟合</a></li>
    <li><strong>给定风速下有多少出力？</strong><span>同窗风速、实测出力及工况。</span><a :href="withBase('/power.html')">功率曲线</a></li>
    <li><strong>各风速段出现了多久？</strong><span>同一测点和测高的有效风速及观测时长。</span><a :href="withBase('/wind-frequency.html')">风频与 Weibull</a></li>
    <li><strong>哪些因素影响发电量？</strong><span>可比的功率或电量基准、实测电量与事件记录。</span><a :href="withBase('/assessment.html')">风场后评估</a></li>
  </ul>
</div>

遇到共振穿越、跨机组差异或技改前后对照时，参见[运行分析专题](/practice)。

<span id="公开数据练习" aria-hidden="true"></span>

## 公开案例与复算资料

| 案例 | 先看什么 | 数据下载 |
| --- | --- | --- |
| Aventa AV-7 | [用三张散点图联合判读运行量](/operations#三张散点图的联合判读) | <a :href="withBase('/data/aventa-linked-scatter.csv')" download>分钟记录</a> |
| ENGIE La Haute Borne | [按风速分箱，筛查桨距角偏离](/pitch#建参考范围并手算一次) | <a :href="withBase('/data/engie-r80711-2014-02-03.csv')" download>桨距角记录</a> |
| Kelmarsh | [对照三片叶片和两台机组的角度](/pitch#逐叶片和跨机组对照) | <a :href="withBase('/data/kelmarsh-blade-pitch.csv')" download>逐叶片记录</a> |
| AWAKEN King Plains | [工况筛选](/scada#实测案例-有效记录与合格工况) → [风速拟合](/wind-speed#怎样读两路风速配对散点图) → [功率验证](/power#用实测记录复算一次)。单独看风频可从[雷达风频](/wind-frequency#用现场雷达的公开记录复算)开始。 | <a :href="withBase('/data/awaken-wt041-scada-1min.csv')" download>机组记录</a> · <a :href="withBase('/data/awaken-a1-lidar-80m-10min.csv')" download>雷达记录</a> · <a :href="withBase('/data/awaken-a1-wt041-2023-08-24.csv')" download>配对表</a> |

<span id="公开案例的来源与字段" aria-hidden="true"></span>

### 数据处理复现

从原始记录复算时，下载 <a :href="withBase('/data/reproduce-scada-cases.py')" download>Python 脚本</a>以及对应的数据文件：<a :href="withBase('/data/aventa-case-input.parquet')" download>Aventa（Parquet）</a>或 <a :href="withBase('/data/engie-case-input.zip')" download>ENGIE（ZIP）</a>。

运行命令、字段对照与数据署名见 <a :href="withBase('/data/case-data-notes.txt')" download>案例数据说明</a>。
