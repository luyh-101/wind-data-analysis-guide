# 方法选择与公开案例

<script setup>
import { withBase } from 'vitepress'
</script>

## 分析目标与方法选择

先从现有数据和要回答的问题选方法。例如，仅有汇总角度时，可以筛查角度是否偏离历史范围。若要定位到某片叶片，还需要逐叶片反馈。下表对应各章的具体做法。

| 分析目标 | 所需数据条件 | 可用方法 |
| --- | --- | --- |
| 定位变桨偏离 | 风速、实测桨距角和工况。定位到叶片或检查跟踪时，再增加逐叶片反馈或同步指令。 | [分箱基线、逐叶片对照与事件复核](/pitch) |
| 比较两路风速 | 有同期观测，并知道测点、测高和窗口定义。 | [时间配对、偏差分析与拟合验证](/wind-speed) |
| 建立单机功率曲线 | 有同一窗口的风速、实测有功功率和工况。 | [分箱曲线与留出验证](/power) |
| 描述测点的风况 | 有测高说明、有效风速和观测时长。 | [风频统计及 Weibull 拟合](/wind-frequency) |
| 判断功率、发电量及损失变化 | 有可比基准。分原因计算损失还需要事件记录和相应的功率或电量。 | [机组性能比较和风场运行后评估](/assessment) |
| 复核运行控制表现 | 按问题准备转速、角度、扭矩或同步控制信号及适用的机组文件。 | [联合制图、控制信号回查与穿越分析](/practice#控制表现与多信号复核) |
| 评价技改效果 | 有变更时间和前后记录，并能取得口径可比的测风或参考机组数据。 | [功率曲线、参考关系与同风况电量对照](/practice#技改对照方法) |

<span id="公开数据练习" aria-hidden="true"></span>

## 公开案例与复算资料

从下表进入案例，可对照图表和计算结果。要从原始记录复算 Aventa 或 ENGIE，请见[数据处理复现](#数据处理复现)。

| 公开案例 | 分析方法 | 提供的资料或主要结果 |
| --- | --- | --- |
| Aventa AV-7 | [运行参数的三图联读](/operations#三张散点图的联合判读) | 同一批 10,032 条分钟记录和三张散点图，可按时间戳在图表间对照。 |
| ENGIE La Haute Borne | [桨距角分段参考与候选筛查](/pitch#建参考范围并手算一次) | 8–9 m/s 箱的 442 条参考样本、百分位范围和 3 月候选记录。 |
| Kelmarsh | [逐叶片和跨机组对照](/pitch#逐叶片和跨机组对照) | 两台机组的逐叶片角度 CSV，以及全范围和低风速局部图。 |
| AWAKEN King Plains | [工况筛选](/scada#实测案例-有效记录与合格工况)、[测风配对与拟合](/wind-speed#怎样读两路风速配对散点图)、[功率验证](/power#用实测记录复算一次) | WT041 分钟记录、A1 雷达窗口和配对表，展示从原始记录到共同验证窗口的过程。 |
| AWAKEN King Plains | [风频与 Weibull](/wind-frequency#用现场雷达的公开记录复算)、[分时段功率对照](/assessment#实测案例-比较同一台机组的两个时段) | A1 单日风频与拟合分布，以及用两种风速来源分箱时的功率对照。 |

## 公开案例的来源与字段

::: details Aventa AV-7

Sarah Barber、Florian Hammer、Yuriy Marykovskiy，*Aventa AV-7 (6kW) IET-OST Research Wind Turbine SCADA with Static Yaw Offset*，第 2 版，DOI `10.5281/zenodo.16738078`，CC BY 4.0。

取 2025 年 6 月 4–10 日 UTC 的记录。原始的 `datetime` 转为 `time_utc`，`wind_speed`、`generator_speed`、`power_output`、`blade_pitch_deg` 对应 `wind_ms`、`generator_rpm`、`power_kw`、`pitch_deg`。对四个数值字段做有效性检查，风速和转速须非负。按 UTC 分钟求均值，每窗至少 55 条有效记录，共得到 10,032 个窗口。55 是记录数门槛，实际采样时间可能有抖动。 [三图案例 CSV](/data/aventa-linked-scatter.csv)

:::

::: details ENGIE La Haute Borne

ENGIE Renewables 发布，采用 Etalab Open Licence 2.0，来源为 OpenOA 示例归档中的 2014–2015 年 SCADA 表。

取 R80711 机组 2014 年 2–3 月记录。将 `Wind_turbine_name` 和 `Date_time` 整理为 `turbine` 和 `time_utc`，`Ws_avg`、`Ba_avg`、`P_avg` 分别记为 `wind_ms`、`pitch_deg`、`power_kw`。转为 UTC 后，3 月 30 日 01:00–01:50 有 6 个时间戳各对应两条冲突记录。分析表排除这 12 条，保留 8,490 条，并标记正功率且分析字段有效的样本。 [桨距角案例 CSV](/data/engie-r80711-2014-02-03.csv)

:::

::: details Kelmarsh

Charlie Plumley（Cubico），*Kelmarsh wind farm data*，DOI `10.5281/zenodo.8252025`，CC BY 4.0。

取 1、2 号机组 2016 年 7 月 UTC 的 10 分钟记录，保留风速、功率与三片桨距角，以正功率作初筛。三片角度对应 `pitch_a_deg`、`pitch_b_deg`、`pitch_c_deg`。 [逐叶片案例 CSV](/data/kelmarsh-blade-pitch.csv)

:::

::: details AWAKEN King Plains

Nicola Bodini，*AWAKEN wind farm wake benchmark inputs*，DOI `10.5281/zenodo.15623845`，CC BY 4.0。

提取 WT041 的 1 分钟 SCADA 记录和 A1 雷达 80 m 的风速、风向，再按统计窗口配对。`nacelle_ms` 是发布数据中已用机舱风速传递函数修正的轮毂高度风速，`lidar_ms` 是该雷达测层的风速。`valid_minute` 和 `generating_minute` 分别是有效分钟数和通过发电筛选的分钟数，`eligible` 标记进入比较的窗口。 [机组分钟记录](/data/awaken-wt041-scada-1min.csv) · [雷达记录](/data/awaken-a1-lidar-80m-10min.csv) · [配对表](/data/awaken-a1-wt041-2023-08-24.csv)

:::

CC BY 4.0 的许可网址为 `https://creativecommons.org/licenses/by/4.0/`。再分发时保留署名与许可，并注明所作修改。ENGIE 数据继续采用 Etalab Open Licence 2.0。

### 数据处理复现

站内 CSV 可直接用于复算。Aventa 分钟汇总和 ENGIE 冲突记录清洗另提供 <a :href="withBase('/data/reproduce-scada-cases.py')" download>Python 脚本</a>与原始数据节选。输入文件保留案例所需的时间段、字段和原始读数。

- <a :href="withBase('/data/aventa-case-input.parquet')" download>Aventa 原始记录节选（Parquet，约 5.4 MB）</a>
- <a :href="withBase('/data/engie-case-input.zip')" download>ENGIE 原始记录节选（ZIP，约 91 KB）</a>

安装 pandas 和 pyarrow 后，可在下载目录运行以下命令，也可只指定其中一个案例。

```powershell
python reproduce-scada-cases.py --aventa aventa-case-input.parquet --engie engie-case-input.zip
```

脚本将处理后的 CSV 保存到 `reproduced-data`。可按机组和 UTC 时间戳将结果与站内 CSV 对照。AWAKEN 的处理口径见 [有效记录与合格工况](/scada#实测案例-有效记录与合格工况) 和 [时间对齐与散点图判读](/wind-speed#怎样读两路风速配对散点图)。
