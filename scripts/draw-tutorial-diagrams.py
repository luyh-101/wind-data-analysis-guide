"""Draw the original concept and workflow figures used in the tutorial."""

from html import escape
from pathlib import Path


OUTPUT = Path(__file__).resolve().parents[1] / "docs/public/figures"
INK = "#19343b"
MUTED = "#44616a"
TEAL = "#006c60"
BLUE = "#385b81"
AMBER = "#a04d24"
LINE = "#cbdad9"
PAPER = "#f7faf9"


def label(x, y, value, size=22, color=INK, weight=500, anchor="start"):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')


def rect(x, y, w, h, fill="white", stroke=LINE, radius=8):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}"/>')


def path(d, color=TEAL, width=3, extra=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" {extra}/>'


def arrow(d, color=TEAL, width=2.5):
    return path(d, color, width, 'marker-end="url(#arrow)"')


def write(name, title, height, parts):
    content = "\n".join(parts)
    (OUTPUT / f"{name}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 {height}" '
        'font-family="Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif" '
        'stroke-linecap="round" stroke-linejoin="round">\n'
        f'<title>{escape(title)}</title>\n'
        '<defs><marker id="arrow" viewBox="0 0 10 10" markerWidth="7" markerHeight="7" '
        'refX="9" refY="5" orient="auto-start-reverse">'
        f'<path d="M1 1L9 5L1 9" fill="none" stroke="{TEAL}" stroke-width="1.5"/>'
        '</marker></defs>\n'
        f'{rect(1, 1, 718, height - 2, PAPER, LINE, 10)}\n{content}\n</svg>\n',
        encoding="utf-8",
    )


def pitch_concept():
    blade = '<path d="M-5 -8 C-13 -24 -9 -60 -1 -91 C5 -97 8 -85 7 -70 L6 -9Z"/>'
    airfoil = 'M-87 0 C-71 -25 14 -24 101 0 C26 11 -48 15 -87 0Z'
    center = '<circle cx="528" cy="482" r="4" fill="#19343b"/>'
    write("pitch-concept", "风轮旋转与单片叶片变桨", 668, [
        label(26, 43, "风轮旋转", 27, INK, 700),
        label(225, 44, "风轮通过传动系统带动发电机", 20, MUTED),
        rect(22, 65, 306, 246), rect(343, 65, 355, 246),
        label(41, 97, "从迎风面看", 19, MUTED),
        label(361, 97, "从侧面看", 19, MUTED),
        '<circle cx="167" cy="197" r="83" fill="none" stroke="#deebe8" stroke-dasharray="5 6"/>',
        '<g transform="translate(167 197)" fill="#3c8278">'
        f'{blade}<g transform="rotate(120)">{blade}</g><g transform="rotate(240)">{blade}</g>'
        '<circle r="13" fill="#19343b"/></g>',
        arrow("M 95 155 A 83 83 0 0 0 109 256"),
        path("M171 105L205 124H251", MUTED, 1.5), label(257, 130, "叶片", 19),
        path("M174 198H241", MUTED, 1.5), label(249, 205, "轮毂", 19),
        label(168, 294, "三片叶片绕风轮轴一起转", 18, MUTED, 500, "middle"),
        '<path d="M540 190L563 190L569 294H533Z" fill="#dce8e5" stroke="#9ab6b1"/>',
        rect(484, 145, 165, 56, "#e5efed", "#95b3ae", 18),
        '<path d="M480 168 H530" stroke="#44616a" stroke-width="5"/>',
        rect(530, 153, 62, 34, "#9cc5bf", TEAL, 5),
        path("M545 160v20 M555 160v20 M565 160v20 M575 160v20", TEAL, 2),
        '<path d="M465 110 Q476 143 471 172 Q466 205 472 253" fill="none" stroke="#3c8278" stroke-width="10"/>',
        '<circle cx="475" cy="170" r="12" fill="#19343b"/>',
        arrow("M363 143H431"), arrow("M363 168H431"), arrow("M363 193H431"),
        label(366, 225, "来流", 20, TEAL),
        path("M626 146V124H657", MUTED, 1.5), label(655, 116, "机舱", 19, INK, 500, "end"),
        path("M566 186V224H583", MUTED, 1.5), label(589, 232, "发电机", 19),
        label(26, 359, "单片叶片变桨", 27, INK, 700),
        label(254, 359, "叶片绕自身长轴转动", 20, MUTED),
        rect(22, 378, 306, 262), rect(343, 378, 355, 262),
        label(41, 411, "找准观察方向", 20, MUTED),
        '<path d="M49 478C111 445 226 468 301 487 C237 500 104 521 49 506Z" fill="#c9dfdb" stroke="#599087" stroke-width="2"/>',
        path("M49 490H302", MUTED, 2, 'stroke-dasharray="7 5"'),
        '<ellipse cx="153" cy="489" rx="10" ry="25" fill="none" stroke="#006c60" stroke-width="2" stroke-dasharray="3 3"/>',
        arrow("M144 459 C117 452 113 506 139 518"),
        label(50, 553, "叶根", 19), label(267, 553, "叶尖", 19),
        arrow("M257 587H92"),
        label(176, 618, "沿长轴从叶尖看向叶根", 19, TEAL, 600, "middle"),
        label(363, 411, "沿长轴观察的翼型截面", 20, MUTED),
        f'<path d="{airfoil}" transform="translate(528 482)" fill="#edf2f2" stroke="#67808a" stroke-width="2" stroke-dasharray="6 5"/>',
        f'<path d="{airfoil}" transform="translate(528 482) rotate(-32)" fill="#d5ece6" stroke="{TEAL}" stroke-width="2"/>',
        path("M441 482H647", MUTED, 1.7, 'stroke-dasharray="5 4"'),
        path("M454 528L614 428", TEAL, 1.7),
        path("M586 482A58 58 0 0 0 577 451", AMBER, 3), center,
        path("M630 482L649 533", MUTED, 1.5), label(676, 550, "基准方向", 19, MUTED, 500, "end"),
        path("M580 437L554 429H509", TEAL, 1.5), label(366, 436, "当前截面方向", 19, TEAL),
        path("M584 466L610 461H651", AMBER, 1.5), label(674, 456, "桨距角", 19, AMBER, 700, "end"),
        label(520, 616, "基准方向与当前方向之间的夹角", 19, INK, 600, "middle"),
    ])


def operation_trends():
    parts = [
        label(27, 43, "变速变桨机组的典型运行趋势", 26, INK, 700),
        label(694, 42, "原理示意，非实测数据", 18, MUTED, 500, "end"),
    ]
    for x, w, bg, caption in [(144, 105, "#eff2f5", "未发电"),
                              (249, 269, "#edf6f4", "正常发电上升段"),
                              (518, 170, "#f8f1e8", "额定附近及以上")]:
        parts.extend([rect(x, 68, w, 397, bg, "none", 0),
                      label(x + w / 2, 95, caption, 18, MUTED, 600, "middle")])
    for y, title, unit in [(220, "发电机转速", "（r/min）"), (336, "有功功率", "（kW）"), (452, "桨距角", "（°）")]:
        parts.extend([label(25, y - 55, title, 19, INK, 650), label(23, y - 29, unit, 17, MUTED),
                      path(f"M144 {y}H688", LINE, 1.4)])
    parts.extend([
        path("M249 105V480 M518 105V480", "#89a49e", 1.5, 'stroke-dasharray="5 6"'),
        path("M149 212H241 C260 209 278 199 304 181 C355 145 391 142 433 142H682", TEAL, 4),
        path("M149 331H245 C330 331 390 303 455 270 C480 258 499 251 518 251H682", BLUE, 4),
        path("M251 438H465 C505 438 524 423 548 411 C589 392 641 370 682 369", AMBER, 4),
        label(312, 210, "转速上升段", 18, TEAL), label(556, 132, "转速平台", 18, TEAL),
        label(562, 241, "额定功率", 18, BLUE), label(675, 444, "变桨调节更明显", 18, AMBER, 600, "end"),
        arrow("M144 478H692"),
        label(249, 508, "切入风速", 18, INK, 600, "middle"),
        label(518, 508, "额定风速", 18, INK, 600, "middle"),
        label(687, 508, "风速（m/s）", 18, MUTED, 500, "end"),
    ])
    write("operation-trends", "发电机转速、有功功率与桨距角随风速变化", 532, parts)


def flow(name, title, steps):
    """Lay out a six-step path in reading order on a single diagram."""
    positions = [(28, 78), (261, 78), (494, 78), (494, 190), (261, 190), (28, 190)]
    parts = [label(27, 44, title, 26, INK, 700)]
    for (x, y), (heading, note) in zip(positions, steps):
        parts.extend([rect(x, y, 198, 77),
                      label(x + 99, y + 30, heading, 20, TEAL, 700, "middle"),
                      label(x + 99, y + 58, note, 16, MUTED, 500, "middle")])
    parts.extend(arrow(d) for d in ("M232 116H255", "M465 116H488", "M593 162V183",
                                    "M488 228H465", "M255 228H232"))
    write(name, title, 293, parts)


def pitch_following():
    parts = [label(26, 43, "同一变桨指令下的两种反馈走势", 26, INK, 700)]
    for x, title, single in [(24, "多片同步变化", False), (370, "单片持续偏离", True)]:
        parts.extend([rect(x, 66, 326, 233), label(x + 18, 100, title, 21, INK, 700),
                      label(x + 23, 136, "桨距角（°）", 17, MUTED),
                      path(f"M{x+24} 150V258H{x+308}", LINE, 1.5),
                      path(f"M{x+37} 230H{x+119}L{x+141} 163H{x+296}", MUTED, 2.3,
                           'stroke-dasharray="6 5"'),
                      path(f"M{x+37} 230H{x+130}Q{x+144} 230 {x+150} 204 Q{x+160} 163 {x+176} 163H{x+296}", TEAL, 3.8),
                      label(x + 305, 282, "时间", 17, MUTED, 500, "end")])
        if single:
            parts.extend([path(f"M{x+37} 230H{x+296}", AMBER, 3.5),
                          label(x + 291, 227, "叶片 3", 17, AMBER, 600, "end"),
                          label(x + 292, 199, "叶片 1、2", 17, TEAL, 600, "end")])
        else:
            parts.append(label(x + 292, 200, "三片反馈近重合", 17, TEAL, 600, "end"))
    parts.extend([path("M29 330H62", MUTED, 2.3, 'stroke-dasharray="6 5"'),
                  label(74, 337, "指令", 18, MUTED), path("M159 330H192", TEAL, 3),
                  label(204, 337, "跟随指令的反馈", 18, MUTED),
                  label(695, 337, "原理示意", 18, MUTED, 500, "end")])
    write("pitch-following-patterns", "多片同步变化与单片持续偏离", 360, parts)


def wind_measurements():
    write("wind-measurements", "测风塔、地基激光雷达与机舱风速计的位置", 338, [
        label(27, 44, "三类测风位置", 26, INK, 700),
        label(693, 43, "布置示意", 18, MUTED, 500, "end"),
        arrow("M35 80H166"), label(182, 86, "示例来流", 19, TEAL),
        path("M27 277H692", "#a2bab5", 2),
        path("M83 273L117 126L152 273 M97 213H138 M107 168H128 M100 208L148 270 M135 208L87 270", MUTED, 2),
        path("M117 126V113H140", BLUE, 2),
        '<circle cx="140" cy="112" r="5" fill="#385b81"/>',
        path("M143 111H173", MUTED, 1.5), label(179, 118, "塔上测点", 18, BLUE),
        label(117, 310, "测风塔", 20, INK, 650, "middle"),
        '<path d="M345 277L310 138H421L386 277Z" fill="#ddf2ee"/>',
        path("M365 265L312 138 M365 265L417 138", TEAL, 2, 'stroke-dasharray="6 5"'),
        path("M307 138H424", TEAL, 2),
        label(366, 126, "雷达测层", 19, TEAL, 650, "middle"),
        rect(344, 254, 42, 22, TEAL, TEAL, 4),
        label(366, 310, "地基激光雷达", 20, INK, 650, "middle"),
        '<path d="M579 150H597L606 277H569Z" fill="#dce8e5" stroke="#9ab6b1"/>',
        rect(552, 125, 101, 28, "#dce8e5", MUTED, 10),
        '<path d="M540 69Q550 106 546 138Q540 171 544 212" fill="none" stroke="#599087" stroke-width="7"/>',
        '<circle cx="549" cy="139" r="8" fill="#19343b"/>',
        path("M632 125V108H655", AMBER, 2),
        '<circle cx="655" cy="108" r="5" fill="#a04d24"/>',
        label(689, 90, "机舱风速计", 18, AMBER, 650, "end"),
        label(589, 310, "风机", 20, INK, 650, "middle"),
    ])


def loss_timeline():
    x = lambda minute: 160 + minute * 51
    parts = [label(25, 43, "重叠事件按时间分段归因", 26, INK, 700)]
    for y, line in [(106, "原始限功率"), (160, "原始故障"), (230, "计入损失")]:
        parts.extend([label(24, y + 6, line, 19, INK, 650), path(f"M160 {y}H670", LINE, 1.4)])
    for start, end, y, color, value in [(2, 7, 106, BLUE, "限功率"), (5, 9, 160, AMBER, "故障"),
                                          (2, 5, 230, BLUE, "20 kWh"), (5, 9, 230, AMBER, "80 kWh")]:
        parts.extend([rect(x(start), y - 16, x(end) - x(start), 32, color, "none", 4),
                      label((x(start) + x(end)) / 2, y + 6, value, 17, "white", 650, "middle")])
    for minute in (0, 2, 5, 7, 9, 10):
        parts.extend([path(f"M{x(minute)} 254v9", MUTED, 1.5),
                      label(x(minute), 287, str(minute), 17, MUTED, 500, "middle")])
    parts.extend([path("M160 258H670", MUTED, 1.5),
                  label(669, 319, "窗口内时间（min）", 18, MUTED, 500, "end")])
    write("loss-event-timeline", "限功率与故障重叠时的损失归因", 339, parts)


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    pitch_concept()
    operation_trends()
    pitch_following()
    wind_measurements()
    loss_timeline()
    flow("pitch-fault-workflow", "从散点异常到事件复核", [
        ("发现散点偏离", "定位机组与时间"),
        ("区分单片和多片", "对齐逐叶片反馈"),
        ("对照运行状态", "功率、转速、工况"),
        ("查看控制记录", "指令、反馈、告警"),
        ("回查事件过程", "时序、检修、事件"),
        ("记录复核结论", "列明证据与事件范围"),
    ])
    flow("scada-workflow", "从原始记录到有效样本", [
        ("读取原始数据", "保留原表与质量标记"),
        ("核对字段", "单位、测点、状态码"),
        ("统一时间", "时区、间隔、窗口"),
        ("检查数据质量", "缺测、重复、异常值"),
        ("按用途筛选工况", "必要时配对独立测风"),
        ("输出有效样本", "同时保留筛选原因"),
    ])
    flow("pitch-screening-workflow", "由候选偏离查找异常证据", [
        ("标记散点偏离", "同工况下对照基线"),
        ("回到原始时序", "查看持续时间与边界"),
        ("逐叶片核对", "对比同期指令和反馈"),
        ("核查告警与工况", "查看共同指令和状态"),
        ("汇总现场证据", "关联事件和检修记录"),
        ("给出筛查判断", "疑似故障、工况变化等"),
    ])
    flow("assessment-workflow", "从功率基准到电量损失", [
        ("准备运行数据", "时窗、状态与计量边界"),
        ("建立可比基准", "测风对照、功率曲线"),
        ("估算参考电量", "窗口功率乘以时长"),
        ("匹配运行事件", "识别启停、限功率等"),
        ("分段计算损失", "重叠时段按规则归因"),
        ("汇总评价结果", "电量差、分项和覆盖"),
    ])
