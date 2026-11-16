"""Rebuild tutorial charts from the CSV files distributed with the site."""

import argparse
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
from matplotlib import font_manager, pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator, PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs/public/data"
OUTPUT = ROOT / "docs/public/figures"
INK = "#19343b"
MUTED = "#44616a"
TEAL = "#006c60"
BLUE = "#385b81"
AMBER = "#a04d24"
GRID = "#dae6e4"
HIGHLIGHT = "#e9f3ef"
CUTOFF = pd.Timestamp("2023-08-24T16:00:00Z")

def configure_font(font_path):
    if font_path is not None:
        font_manager.fontManager.addfont(font_path)
        family = font_manager.FontProperties(fname=font_path).get_name()
    else:
        available = {font.name for font in font_manager.fontManager.ttflist}
        candidates = ("Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "SimHei")
        family = next((name for name in candidates if name in available), None)
        if family is None:
            raise SystemExit("请安装中文字体，或用 --font 指定中文字体文件。")
    plt.rcParams.update({
        "font.family": [family, "DejaVu Sans"],
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelcolor": INK,
        "axes.edgecolor": GRID,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.axisbelow": True,
        "axes.unicode_minus": True,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": INK,
        "grid.color": GRID,
        "legend.frameon": False,
        "figure.dpi": 150,
    })

def csv(name, time_column):
    data = pd.read_csv(DATA / f"{name}.csv")
    data[time_column] = pd.to_datetime(data[time_column], utc=True)
    return data

def panel(width=7, height=4.1):
    return plt.subplots(figsize=(width, height), layout="constrained")

def axis(ax, x, y, title=None):
    ax.set(xlabel=x, ylabel=y)
    ax.grid(axis="both", linewidth=0.7)
    if title is not None:
        ax.set_title(title, loc="left", pad=14)

def save(fig, name):
    fig.savefig(OUTPUT / f"{name}.png", facecolor="white")
    plt.close(fig)

def aventa_scatter(data):
    positive = data.power_kw.gt(0)
    charts = (
        ("aventa-wind-speed", "风速–发电机转速", "wind_ms", "风速（m/s）",
         "generator_rpm", "发电机转速（r/min）", (4.5, 735, 14.2, 796),
         (12.5, 785), (11.8, 637), "转速平台"),
        ("aventa-speed-power", "发电机转速–有功功率", "generator_rpm", "发电机转速（r/min）",
         "power_kw", "有功功率（kW）", (750, 5.82, 780, 6.89),
         (758, 6.35), (342, 5.65), "转速平台段的功率范围"),
        ("aventa-wind-pitch", "风速–桨距角", "wind_ms", "风速（m/s）",
         "pitch_deg", "桨距角（°）", (0, 11, 4.2, 42),
         (4.1, 39), (6.6, 48), "低风速点带"),
    )
    for (name, title, x, xlabel, y, ylabel, bounds, point, note, caption) in charts:
        fig, ax = panel(6.8, 3.75)
        left, bottom, right, top = bounds
        ax.add_patch(Rectangle((left, bottom), right - left, top - bottom,
                               facecolor=HIGHLIGHT, edgecolor=TEAL, alpha=.70,
                               linestyle=(0, (4, 3)), linewidth=1.25))
        for mask, color, caption_key in ((positive, TEAL, "正功率"), (~positive, AMBER, "零或负功率")):
            ax.scatter(data.loc[mask, x], data.loc[mask, y], c=color, s=8, alpha=.38,
                       linewidths=0, label=caption_key)
        ax.annotate(caption, xy=point, xytext=note, color=INK, fontsize=11,
                    bbox={"fc": "white", "ec": GRID, "pad": 3.5},
                    arrowprops={"arrowstyle": "->", "color": TEAL})
        axis(ax, xlabel, ylabel, title)
        ax.legend(loc="upper center", bbox_to_anchor=(.5, -.19), ncol=2, markerscale=2)
        save(fig, name)

def sample_counts(minutes, paired):
    valid = minutes[["nacelle_ms", "power_kw", "curtailment"]].notna().all(axis=1)
    generating = valid & minutes.nacelle_ms.gt(0) & minutes.power_kw.gt(0) & minutes.curtailment.eq(0)
    fig, axes = plt.subplots(2, 1, figsize=(7, 5.25), layout="constrained")
    series = [
        ("一分钟记录（条）", ["原始记录", "字段齐全", "通过发电筛选"],
         [len(minutes), int(valid.sum()), int(generating.sum())]),
        ("十分钟窗口（个）", ["全日窗口", "10 条有效分钟", "通过筛选且雷达有效"],
         [len(paired), int(paired.valid_minute.eq(10).sum()), int(paired.eligible.sum())]),
    ]
    for ax, (title, names, counts) in zip(axes, series):
        bars = ax.barh(names, counts, color=["#aabebc", BLUE, TEAL], height=.55)
        ax.set_title(title, loc="left", pad=9)
        ax.invert_yaxis()
        ax.set_xlim(0, counts[0] * 1.15)
        ax.xaxis.set_major_locator(MaxNLocator(4, integer=True))
        ax.grid(axis="x")
        ax.bar_label(bars, [f"{count:,}" for count in counts], padding=5)
    save(fig, "scada-sample-counts")

def bin_means(data, wind, minimum):
    usable = data[[wind, "power_kw"]].dropna()
    means = usable.groupby(np.floor(usable[wind]).astype(int)).agg(
        wind=(wind, "mean"), power=("power_kw", "mean"), count=("power_kw", "size"),
    )
    return means[means["count"] >= minimum]

def consecutive_bins(means):
    return means.groupby(means.index.to_series().diff().ne(1).cumsum())

def plot_bins(ax, bins, color, style, name):
    for index, (_, group) in enumerate(consecutive_bins(bins)):
        ax.plot(group.wind, group.power, color=color, linestyle=style, linewidth=2.2,
                marker="o", markersize=4.8, label=name if index == 0 else None)

def wind_fit(train, test):
    slope, intercept = np.polyfit(train.nacelle_ms, train.lidar_ms, 1)
    low, high = train.nacelle_ms.agg(["min", "max"])
    common = test[test.nacelle_ms.between(low, high)].sort_values("window_start_utc")
    fitted = slope * common.nacelle_ms + intercept

    fig, ax = panel()
    limits = [min(train.nacelle_ms.min(), test.nacelle_ms.min(), train.lidar_ms.min(), test.lidar_ms.min()) - .2,
              max(train.nacelle_ms.max(), test.nacelle_ms.max(), train.lidar_ms.max(), test.lidar_ms.max()) + .2]
    ax.plot(limits, limits, color=MUTED, linestyle="--", label="1:1 参考线")
    ax.scatter(train.nacelle_ms, train.lidar_ms, c=TEAL, alpha=.58, label="拟合窗口")
    ax.scatter(test.nacelle_ms, test.lidar_ms, facecolors="none", edgecolors=BLUE,
               linewidths=1.4, label="留出窗口")
    x = np.asarray([low, high])
    ax.plot(x, slope * x + intercept, color=AMBER, linewidth=2.2, label="直线拟合")
    ax.set(xlim=limits, ylim=limits, aspect="equal")
    axis(ax, "WT041 机舱风速（m/s）", "A1 雷达风速（m/s）", "两路风速对照与拟合")
    ax.legend(loc="lower right", fontsize=9.5, frameon=True, framealpha=.95, edgecolor=GRID)
    save(fig, "wind-pairs")

    raw_error = (common.nacelle_ms - common.lidar_ms).abs()
    change = (fitted - common.lidar_ms).abs() - raw_error
    positions = np.arange(1, len(change) + 1)
    fig, ax = panel()
    ax.axhline(0, color=MUTED, linewidth=1.3)
    ax.bar(positions, change, color=np.where(change < 0, TEAL, AMBER), width=.75)
    axis(ax, "验证窗口（按 UTC 时间排序）", "绝对误差变化（m/s）", "拟合后绝对误差的变化")
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
    ax.margins(y=.12)
    ax.text(.98, .96, "误差增大", transform=ax.transAxes, ha="right", va="top", color=AMBER)
    ax.text(.98, .04, "误差减小", transform=ax.transAxes, ha="right", va="bottom", color=TEAL)
    save(fig, "wind-fit-errors")

def estimate(wind, bins):
    """Interpolate only between consecutive retained wind-speed bins."""
    for _, group in consecutive_bins(bins):
        if group.wind.iloc[0] <= wind <= group.wind.iloc[-1]:
            return np.interp(wind, group.wind, group.power)
    return np.nan

def power_curves(train, test):
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.2), sharex=True, sharey=True,
                             layout="constrained")
    fitted = {}
    for ax, (wind, title, color) in zip(axes, [
        ("lidar_ms", "A1 雷达风速", TEAL),
        ("nacelle_ms", "WT041 机舱风速", BLUE),
    ]):
        ax.scatter(train[wind], train.power_kw, c=color, s=20, alpha=.43, label="拟合段实测窗口")
        means = bin_means(train, wind, 3)
        plot_bins(ax, means, color, "-", "分箱均值与插值曲线")
        axis(ax, "风速（m/s）", "", title)
        ax.legend(loc="upper left", fontsize=8.7, markerscale=.8)
        fitted[wind] = test[wind].map(lambda value: estimate(value, means))
    axes[0].set_ylabel("有功功率（kW）")
    save(fig, "power-curves")

    prediction = pd.DataFrame(fitted).dropna()
    actual = test.loc[prediction.index, "power_kw"]
    fig, ax = panel()
    high = max(prediction.max().max(), actual.max()) * 1.07
    ax.plot([0, high], [0, high], linestyle="--", color=MUTED, label="估算等于实测")
    ax.scatter(actual, prediction.lidar_ms, edgecolors=TEAL, facecolors="none",
               s=49, linewidths=1.5, label="雷达曲线")
    ax.scatter(actual, prediction.nacelle_ms, c=BLUE, marker="+", s=64,
               linewidths=1.55, label="机舱曲线")
    ax.set(xlim=(0, high), ylim=(0, high), aspect="equal")
    axis(ax, "实测有功功率（kW）", "估算有功功率（kW）",
         f"功率估算与实测对照（{len(prediction)} 个共同窗口）")
    ax.legend(loc="lower right", fontsize=10)
    save(fig, "power-validation")

def weibull_frequency(lidar):
    speeds = np.sort(lidar.lidar_ms.to_numpy())
    n = len(speeds)
    position = (np.arange(1, n + 1) - .3) / (n + .4)
    shape, intercept = np.polyfit(np.log(speeds), np.log(-np.log1p(-position)), 1)
    scale = np.exp(-intercept / shape)
    edges = np.arange(np.floor(speeds.min()) - 1, np.ceil(speeds.max()) + 2)
    x = np.linspace(edges[0], edges[-1], 400)
    density = (shape / scale) * (x / scale)**(shape - 1) * np.exp(-(x / scale)**shape)
    fig, ax = panel()
    ax.axvspan(6, 7, color=HIGHLIGHT, zorder=0)
    ax.hist(speeds, bins=edges, weights=np.full(n, 1 / n), color="#8cbdb4",
            edgecolor="white", linewidth=.8, label="实测风频密度（箱宽 1 m/s）")
    ax.plot(x, density, color=AMBER, linewidth=2.4, label="Weibull 概率密度")
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.set_xticks(edges)
    axis(ax, "雷达风速（m/s）", "频率密度（% / (m/s)）", "A1 雷达风速分布与 Weibull 拟合")
    ax.legend(loc="upper right", fontsize=10)
    save(fig, "lidar-wind-frequency")

def synchronized_signals(aventa):
    start = pd.Timestamp("2025-06-04T05:23:00Z")
    end = pd.Timestamp("2025-06-04T05:37:00Z")
    window = aventa[aventa.time_utc.between(start, end)]
    elapsed = (window.time_utc - start).dt.total_seconds() / 60
    fig, axes = plt.subplots(5, 1, figsize=(7, 6.6), sharex=True, layout="constrained",
                             gridspec_kw={"height_ratios": [1, 1, 1, 1, .45]})
    positive = elapsed[window.power_kw.gt(0)]
    start_positive, end_positive = positive.min(), positive.max() + 1
    assert len(positive) == end_positive - start_positive
    for ax, (column, title, unit, color) in zip(axes, [
        ("wind_ms", "风速", "m/s", TEAL), ("power_kw", "功率", "kW", BLUE),
        ("generator_rpm", "转速", "r/min", TEAL), ("pitch_deg", "桨距角", "°", AMBER),
    ]):
        ax.axvspan(start_positive, end_positive, color=HIGHLIGHT)
        ax.axvline(start_positive, color=MUTED, linestyle="--", linewidth=1)
        ax.plot(elapsed, window[column], color=color, linewidth=2, marker="o", markersize=3)
        ax.set_ylabel(f"{title}\n{unit}", rotation=0, labelpad=24, va="center")
        ax.yaxis.set_major_locator(MaxNLocator(4))
        ax.grid(axis="y")
    axes[0].set_title("Aventa 同一时窗的四路运行信号", loc="left", pad=12)
    axes[-1].broken_barh([(start_positive, end_positive - start_positive)], (0, 1), color=TEAL)
    axes[-1].set(yticks=[], ylim=(0, 1), xlim=(0, 14), xlabel="时间（UTC）")
    axes[-1].spines["left"].set_visible(False)
    axes[-1].text((start_positive + end_positive) / 2, .5, "连续正功率窗口",
                  va="center", ha="center", color="white", fontsize=10)
    axes[-1].set_xticks([0, 4, 8, 12, 14], ["05:23", "05:27", "05:31", "05:35", "05:37"])
    save(fig, "aventa-synchronized-signals")

def pitch_reference_reading():
    fig, ax = panel(6.8, 3.87)
    ranges = [(5, 3.2, 4.2, 5.5), (6, 3.7, 4.8, 6.1), (7, 4.3, 5.4, 6.6)]
    ax.fill_between([], [], [], color=HIGHLIGHT, label="正常参考范围")
    ax.plot([], [], color=TEAL, linewidth=2.1, label="正常角度中位数")
    for start, low, middle, high in ranges:
        ax.add_patch(Rectangle((start, low), 1, high - low, facecolor=HIGHLIGHT,
                               edgecolor=TEAL, linewidth=1))
        ax.hlines(middle, start, start + 1, color=TEAL, linewidth=2.1)
    ax.scatter(5.62, 4.5, c=BLUE, marker="o", s=52, zorder=3)
    ax.scatter(6.62, 7.0, c=AMBER, marker="D", s=58, zorder=3)
    ax.annotate("在范围内", (5.62, 4.5), xytext=(5.27, 2.8),
                arrowprops={"arrowstyle": "-", "color": BLUE}, color=BLUE)
    ax.annotate("候选偏离", (6.62, 7.0), xytext=(6.89, 7.5),
                arrowprops={"arrowstyle": "-", "color": AMBER}, color=AMBER)
    ax.set(xlim=(4.9, 8.1), ylim=(2.2, 9.0), xticks=[5, 6, 7, 8])
    axis(ax, "风速（m/s）", "桨距角（°）", "同一片叶片的正常参考与待查记录（示意）")
    ax.legend(loc="upper left")
    save(fig, "pitch-reference-reading")


def pitch_motion_reading():
    fig, ax = panel(6.8, 3.87)
    time = np.arange(0, 36, 5)
    ax.axvspan(20, 35, color="#f8efe9")
    ax.plot(time, [3, 4, 7, 8, 8, 10, 12, 14], color=TEAL, linewidth=2.4,
            marker="o", markersize=4, label="叶片 1")
    ax.plot(time, [2, 3, 6, 7, 7, 9, 11, 13], color=BLUE, linewidth=2.2,
            linestyle="--", marker="s", markersize=4, label="叶片 2")
    ax.plot(time, [1, 2, 5, 6, 6, 7, 7, 8], color=AMBER, linewidth=2.2,
            linestyle="-.", marker="D", markersize=4, label="叶片 3")
    ax.text(8, 11.7, "三片一起变化", ha="center", color=MUTED)
    ax.text(28, 4.3, "第 3 片变化较小", ha="center", color=AMBER)
    ax.set(xlim=(0, 35.5), ylim=(0, 17.5), xticks=time)
    axis(ax, "经过时间（s）", "桨距角（°）", "逐叶片实测角度时序画法（示意）")
    ax.legend(loc="upper left", ncols=3, columnspacing=1.2)
    save(fig, "pitch-motion-reading")


def wind_difference_reading(paired):
    paired = paired.sort_values("window_start_utc")
    times = paired.window_start_utc
    difference = paired.nacelle_ms - paired.lidar_ms
    fig, (wind_ax, diff_ax) = plt.subplots(
        2, 1, figsize=(6.8, 5), sharex=True, layout="constrained",
    )
    wind_ax.plot(times, paired.nacelle_ms, color=BLUE, linewidth=1.7, label="机舱")
    wind_ax.plot(times, paired.lidar_ms, color=TEAL, linewidth=1.7,
                 linestyle="--", label="雷达")
    axis(wind_ax, "", "风速（m/s）", "同一时段，两路风速怎样变化")
    wind_ax.legend(loc="upper left", ncols=2)
    diff_ax.axhline(0, color=MUTED, linestyle="--")
    diff_ax.plot(times, difference, color=AMBER, linewidth=1.6)
    axis(diff_ax, "时间（UTC）", "机舱 − 雷达（m/s）")
    diff_ax.xaxis.set_major_locator(HourLocator(byhour=range(0, 24, 4)))
    diff_ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
    diff_ax.set_xlim(times.min(), times.max())
    save(fig, "wind-difference-reading")


def paired_wind_frequency(paired):
    paired = paired[["nacelle_ms", "lidar_ms"]].dropna()
    start = int(np.floor(paired.min().min()))
    stop = int(np.floor(paired.max().max())) + 1
    bins = np.arange(start, stop + 1)
    positions = bins[:-1]
    fig, ax = panel(6.8, 3.87)
    ax.axvspan(5.55, 6.45, facecolor=HIGHLIGHT, edgecolor=TEAL,
               linewidth=1.2, linestyle="--")
    ax.bar(positions - .19, np.histogram(paired.nacelle_ms, bins)[0] / len(paired),
           width=.35, color=BLUE, label="机舱")
    ax.bar(positions + .19, np.histogram(paired.lidar_ms, bins)[0] / len(paired),
           width=.35, color=TEAL, label="雷达")
    ax.set_xticks(positions, [f"{value}–{value + 1}" for value in positions])
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    axis(ax, "风速区间（m/s）", "共同观测时段占比", "两路风速在各区间出现的比例")
    ax.legend(loc="upper left", ncols=2)
    save(fig, "paired-wind-frequency")


def power_curve_reading(train):
    fig, ax = panel(6.8, 3.87)
    ax.scatter(train.nacelle_ms, train.power_kw, c=BLUE, s=29, alpha=.43,
               label="同期实测窗口")
    means = bin_means(train, "nacelle_ms", 3)
    plot_bins(ax, means, TEAL, "-", "分箱均值与插值曲线")
    reading_wind = 7.0
    reading_power = estimate(reading_wind, means)
    ax.scatter(reading_wind, reading_power, c=AMBER, marker="D", s=57, zorder=3)
    ax.vlines(reading_wind, 0, reading_power, color=AMBER, linestyle="--")
    ax.hlines(reading_power, 4, reading_wind, color=AMBER, linestyle="--")
    ax.annotate("按风速读出估算功率", (reading_wind, reading_power), xytext=(7.2, 650),
                arrowprops={"arrowstyle": "-", "color": AMBER}, color=AMBER)
    ax.set(xlim=(4, 9.7), ylim=(0, 2460))
    axis(ax, "机舱风速（m/s）", "有功功率（kW）", "散点、分箱均值和功率曲线")
    ax.legend(loc="upper left")
    save(fig, "power-curve-reading")


def energy_gap_reading():
    fig, ax = panel(6.8, 3.87)
    positions = np.arange(4)
    reference = [250, 300, 250, 200]
    actual = [250, 140, 60, 150]
    ax.axvspan(.5, 2.5, color="#f8efe9")
    reference_bars = ax.bar(positions - .18, reference, width=.31, color=BLUE, label="参考电量")
    actual_bars = ax.bar(positions + .18, actual, width=.31, color=TEAL, label="实发电量")
    ax.bar_label(reference_bars, padding=3)
    ax.bar_label(actual_bars, padding=3)
    ax.set_xticks(positions, ["09:00–10:00", "10:00–11:00", "11:00–12:00", "12:00–13:00"])
    ax.set_ylim(0, 380)
    axis(ax, "时段", "电量（kWh）", "按时段对照参考电量与实发电量（示意）")
    ax.legend(loc="upper right", ncols=2)
    save(fig, "energy-gap-reading")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, help="中文字体文件（可选）")
    args = parser.parse_args()
    configure_font(args.font)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    aventa = csv("aventa-linked-scatter", "time_utc")
    minutes = csv("awaken-wt041-scada-1min", "time_utc")
    paired = csv("awaken-a1-wt041-2023-08-24", "window_start_utc")
    lidar = csv("awaken-a1-lidar-80m-10min", "time_center_utc")
    eligible = paired[paired.eligible]
    train = eligible[eligible.window_start_utc < CUTOFF]
    test = eligible[eligible.window_start_utc >= CUTOFF]
    aventa_scatter(aventa)
    sample_counts(minutes, paired)
    wind_fit(train, test)
    power_curves(train, test)
    weibull_frequency(lidar)
    synchronized_signals(aventa)
    pitch_reference_reading()
    pitch_motion_reading()
    wind_difference_reading(paired)
    paired_wind_frequency(paired)
    power_curve_reading(train)
    energy_gap_reading()

if __name__ == "__main__":
    main()
