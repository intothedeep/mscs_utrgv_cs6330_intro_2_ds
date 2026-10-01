"""
Shared code for HW2 Problem 1. Every answer has its own script (p1_airport_a_alpha.py,
..., p1_movie_j_discussion.py); this module holds what they share: data loading, the four
estimators, model sampling, the printed calculation steps, the plot style and the plots.
Problem 2 helpers are in common_p2.py.

Run one answer:   uv run python hw2/code/p1_airport_a_alpha.py
Run everything:   uv run python hw2/code/run_all.py
Figures go to hw2/figures/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: write PNGs only, no GUI backend needed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.transforms import blended_transform_factory
from scipy.stats import ks_2samp

HW_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = HW_DIR / "00_doc"
FIG_DIR = HW_DIR / "figures"
SEED = 20701313  # owner's student ID
VOTE_VIEW_MAX = 20.0  # x-limit for movie PDFs; ratings live in [1, 10]
# x-limit for linear-axis airport panels: 98% of airports have at most 200 routes, and the
# log-log panels beside them show the full tail.
ROUTE_VIEW_MAX = 200.0

DATA_COLOR = "#2a78d6"
MODEL_COLOR = "#eb6834"
INK = "#52514e"
GRID = "#e4e3df"
MEDIAN_COLOR = "#2e8b57"  # reference lines only, not data series
MEAN_COLOR = "#8e44ad"
# White box behind a line label so points or curves under it do not hide the text.
LABEL_BOX = dict(boxstyle="square,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85)

plt.rcParams.update({
    "axes.edgecolor": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 10, "axes.titlesize": 11, "legend.frameon": False,
})


# ---------------------------------------------------------------- estimators (pure)

def fit_power_law(x: np.ndarray) -> dict[str, float]:
    """Continuous MLE (Clauset et al. 2009) with x_min = min(x): alpha = 1 + n / sum ln(x/x_min)."""
    x_min = float(x.min())
    alpha = 1.0 + len(x) / float(np.log(x / x_min).sum())
    return {"alpha": alpha, "x_min": x_min}


def fit_exponential(x: np.ndarray) -> dict[str, float]:
    """MLE: lambda = 1 / mean."""
    return {"lambda": 1.0 / float(x.mean())}


def fit_uniform(x: np.ndarray) -> dict[str, float]:
    """MLE: [a, b] = [min, max]."""
    return {"a": float(x.min()), "b": float(x.max())}


def fit_normal(x: np.ndarray) -> dict[str, float]:
    """mu = sample mean, sigma = sample standard deviation (ddof = 1)."""
    return {"mu": float(x.mean()), "sigma": float(x.std(ddof=1))}


def sample_models(x: np.ndarray, rng: np.random.Generator) -> dict[str, tuple[str, np.ndarray]]:
    """Draw len(x) values from each fitted model; returns {key: (label, sample)}."""
    n = len(x)
    pl, ex, un, no = fit_power_law(x), fit_exponential(x), fit_uniform(x), fit_normal(x)
    # Inverse-CDF sampling of the Pareto form: x = x_min * (1 - u)^(-1 / (alpha - 1)).
    pl_sample = pl["x_min"] * (1.0 - rng.random(n)) ** (-1.0 / (pl["alpha"] - 1.0))
    return {
        "powerlaw": (f"power law  α={pl['alpha']:.3f}, x_min={pl['x_min']:g}", pl_sample),
        "exponential": (f"exponential  λ={ex['lambda']:.4f}",
                        rng.exponential(1.0 / ex["lambda"], n)),
        "uniform": (f"uniform  [a, b]=[{un['a']:g}, {un['b']:g}]",
                    rng.uniform(un["a"], un["b"], n)),
        "normal": (f"normal  μ={no['mu']:.3f}, σ={no['sigma']:.3f}",
                   rng.normal(no["mu"], no["sigma"], n)),
    }


# ---------------------------------------------------------------- plotting

def ccdf(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """P(X >= x) at each sorted value - a power law is a straight line on log-log."""
    xs = np.sort(x)
    return xs, 1.0 - np.arange(len(xs)) / len(xs)


def ecdf(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    xs = np.sort(x)
    return xs, np.arange(1, len(xs) + 1) / len(xs)


def qq_panel(ax: plt.Axes, data: np.ndarray, sample: np.ndarray, log: bool) -> None:
    q = np.linspace(0.005, 0.995, 199)
    dq, sq = np.quantile(data, q), np.quantile(sample, q)
    if log:
        keep = sq > 0  # normal / exponential samples can go <= 0; log axes cannot show them
        dq, sq = dq[keep], sq[keep]
        ax.set_xscale("log")
        ax.set_yscale("log")
    # Usual convention (scipy probplot, statsmodels, R qqnorm, lecture 7 slides): the model
    # is the reference on x, the observed data is on y.
    ax.scatter(sq, dq, s=12, color=MODEL_COLOR, zorder=3)
    lo, hi = min(dq.min(), sq.min()), max(dq.max(), sq.max())
    ax.plot([lo, hi], [lo, hi], color=INK, lw=1, ls="--", label="y = x (perfect fit)")
    ax.set(xlabel="model-sample quantile", ylabel="data quantile", title="QQ plot")
    ax.legend(loc="upper left")


def save(fig: plt.Figure, name: str, top: float = 1.0) -> None:
    """top < 1 keeps a band free above the panels (for a figure-level legend)."""
    fig.tight_layout(rect=(0, 0, 1, top))
    fig.savefig(FIG_DIR / f"{name}.png", dpi=160)
    plt.close(fig)


def label_vlines(ax: plt.Axes, lines: list[tuple[float, str, str, str]], is_log: bool,
                 at_bottom: bool = False, top_label: float = 0.6) -> None:
    """Vertical reference lines labelled on the line itself instead of in a legend.

    On log axes the lines are far apart, so each label runs up its own line. On linear axes
    the lines sit close together, so the labels are stacked to the right of the rightmost
    line with a short arrow back to their own line. Call this after setting the x-limits.
    """
    x_min, x_max = ax.get_xlim()
    label_x = max(x for x, *_ in lines) + 0.1 * (x_max - x_min)
    at_top = blended_transform_factory(ax.transData, ax.transAxes)  # x in data, y in axes
    for i, (x, color, style, text) in enumerate(lines):
        ax.axvline(x, color=color, lw=1.5, ls=style)
        if is_log:
            y, va = (0.03, "bottom") if at_bottom else (0.97, "top")
            ax.text(x * 1.08, y, text, transform=at_top, rotation=90, ha="left", va=va,
                    color=color, fontsize=9, bbox=LABEL_BOX)
        else:
            y = top_label - 0.13 * i  # stacked down from top_label (axes fraction)
            ax.annotate(text, xy=(x, y), xycoords=at_top, xytext=(label_x, y),
                        textcoords=at_top, va="center", color=color, fontsize=9,
                        bbox=LABEL_BOX, arrowprops=dict(arrowstyle="-", color=color, lw=0.8))


def plot_airport_data(x: np.ndarray) -> None:
    # Rows: PDF, PMF, CDF, CCDF. Left column on linear axes shows how bunched up the data
    # is; the right column on log-log axes spreads that bunch out so the shape and the tail
    # can be read. Each row is the same quantity on the two kinds of axes.
    fig, ((pdf_lin, pdf_log), (pmf_lin, pmf_log), (cdf_lin, cdf_log), (ccdf_lin, ccdf_log)) = (
        plt.subplots(4, 2, figsize=(10, 13)))
    n = len(x)
    pdf_lin.hist(x, bins=np.arange(0, ROUTE_VIEW_MAX + 5, 5), weights=np.full(n, 1 / n),
                 color=DATA_COLOR)
    pdf_lin.set(xlabel="routes per airport", ylabel="share of airports per bin",
                title="PDF (histogram), linear axes (bin = 5 routes)")
    # Log-width bins; three decades in 15 bins leave no empty bin between integers.
    pdf_log.plot(*log_binned_pdf(x, np.logspace(0, 3, 16)), "o-", ms=4, color=DATA_COLOR)
    pdf_log.set(xscale="log", yscale="log", xlabel="routes per airport (log)",
                ylabel="density (log)", title="PDF, log-log (log-width bins)")
    # Routes are integers, so these are PMFs: one dot per route count k. The left axis counts
    # airports; the right axis gives the same height as a share, P(X = k).
    values, counts = np.unique(x, return_counts=True)
    for ax, scale in ((pmf_lin, "linear"), (pmf_log, "log")):
        ax.scatter(values, counts, s=12, color=DATA_COLOR)
        ax.set(xscale=scale, yscale=scale, ylabel="number of airports",
               xlabel="routes per airport" + (" (log)" if scale == "log" else ""),
               title=f"PMF, {'linear axes' if scale == 'linear' else 'log-log'} "
                     "(airports with exactly k routes)")
        share_axis = ax.secondary_yaxis("right", functions=(lambda c: c / n, lambda s: s * n))
        share_axis.set_ylabel("share P(X = k)")
    cdf_lin.plot(*ecdf(x), color=DATA_COLOR, lw=2)
    cdf_lin.set(xlabel="routes per airport", ylabel="P(X ≤ x)", title="CDF, linear axes")
    cdf_log.plot(*ecdf(x), color=DATA_COLOR, lw=2)
    cdf_log.set(xscale="log", yscale="log", xlabel="routes per airport (log)",
                ylabel="P(X ≤ x) (log)", title="CDF, log-log")
    ccdf_lin.plot(*ccdf(x), color=DATA_COLOR, lw=2)
    ccdf_lin.set(xlabel="routes per airport", ylabel="P(X ≥ x)", title="CCDF, linear axes")
    ccdf_log.plot(*ccdf(x), color=DATA_COLOR, lw=2)
    ccdf_log.set(xscale="log", yscale="log", xlabel="routes per airport (log)",
                 ylabel="P(X ≥ x) (log)", title="CCDF, log-log")
    # The same reference lines in every panel. Median: half the airports are at or below
    # it. Mean: pulled far right of the median by a few hubs. x = 60: 92% of airports lie
    # left of it, and from 61 on a route count belongs to only 1-3 airports (the floor rows
    # in the log-log PMF).
    median, mean = float(np.median(x)), float(x.mean())
    share_60 = float(np.mean(x <= 60))
    lines = [(median, MEDIAN_COLOR, ":", f"median = {median:g}"),
             (mean, MEAN_COLOR, "-.", f"mean = {mean:.1f}"),
             (60.0, INK, "--", f"x = 60 ({share_60:.0%} at or below)")]
    beyond = float(np.mean(x > ROUTE_VIEW_MAX))
    for ax in (pdf_lin, pmf_lin, cdf_lin, ccdf_lin):
        ax.set_xlim(0, ROUTE_VIEW_MAX)
        ax.text(0.98, 0.12, f"{beyond:.1%} of airports have\nmore than {ROUTE_VIEW_MAX:g} routes",
                transform=ax.transAxes, ha="right", color=INK, fontsize=9)
        label_vlines(ax, lines, is_log=False)
    # Log PDF, CDF and CCDF run across the top, so their labels go in the empty bottom.
    for ax in (pdf_log, pmf_log, cdf_log, ccdf_log):
        label_vlines(ax, lines, is_log=True, at_bottom=ax is not pmf_log)
    fig.suptitle(f"Airport routes: empirical distribution (n = {n})")
    save(fig, "p1a_0_data")


def log_binned_pdf(v: np.ndarray, bins: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Density per log bin, normalised by the WHOLE sample so values off the bins still count."""
    counts, edges = np.histogram(v, bins=bins)
    density = counts / (len(v) * np.diff(edges))
    centers = np.sqrt(edges[:-1] * edges[1:])
    keep = counts > 0
    return centers[keep], density[keep]


def mark_at_one(ax: plt.Axes, values: list[tuple[float, str]], is_log: bool) -> None:
    """Dot and value at x = 1 for each curve: (height, colour).

    x = 1 is the smallest route count, where the integer data jump to 20.9% at once while a
    continuous model starts from 0; the KS gap of the power law sits here.
    Labels are placed from the highest point down: the first goes above its dot (below it
    if the dot is at the top of the panel); each next one goes above its own dot if that
    leaves a line of space under the previous label, otherwise just below.
    """
    ax.autoscale_view()  # settle the limits now, so data-to-screen heights are final
    points_per_pixel = 72 / ax.figure.dpi
    previous_label = None  # height of the previous label, in points
    for y, color in sorted(values, reverse=True):
        if is_log and y <= 0:  # log axes cannot show 0: say so above the line labels
            ax.text(1.1, 0.55, "0 at x = 1", transform=blended_transform_factory(
                ax.transData, ax.transAxes), color=color, fontsize=8, bbox=LABEL_BOX)
            continue
        at = ax.transData.transform((1.0, y))[1] * points_per_pixel
        if previous_label is None:
            dy = -10 if y > 0.9 else 10
        elif at + 10 <= previous_label - 13:
            dy = 10
        else:
            dy = min(-10, previous_label - 13 - at)
        previous_label = at + dy
        ax.plot([1.0], [y], "o", ms=6, color=color, mec="white", zorder=5)
        ax.annotate(f"{y:.3f} at x = 1", xy=(1.0, y), xytext=(8, dy), textcoords="offset points",
                    color=color, fontsize=8, va="center", bbox=LABEL_BOX)


def plot_airport_model(x: np.ndarray, key: str, label: str, sample: np.ndarray) -> None:
    # Rows: PDF, CDF, CCDF, QQ. Left column on linear axes, right column on log-log axes.
    # The linear QQ keeps what the log one drops (model values <= 0, e.g. the normal's
    # negative route counts); the log QQ spreads out a tail that spans several decades.
    # Linear distribution panels are cut at ROUTE_VIEW_MAX; the share beyond is printed.
    fig, axes = plt.subplots(4, 2, figsize=(10, 13))
    (pdf_lin, pdf_log), (cdf_lin, cdf_log), (ccdf_lin, ccdf_log), (qq_lin, qq_log) = axes
    x_hi = ROUTE_VIEW_MAX
    x_lo = min(0.0, float(np.quantile(sample, 0.001)))
    beyond_data, beyond_model = float(np.mean(x > x_hi)), float(np.mean(sample > x_hi))

    # PDF, linear: density histograms with 20-route bins. Weights (not density=True) keep
    # each curve normalised to its whole sample even where the axis cuts it off.
    width = 5.0
    bins = np.arange(np.floor(x_lo / width) * width, x_hi + width, width)
    pdf_lin.hist(x, bins=bins, weights=np.full(len(x), 1 / (len(x) * width)),
                 color=DATA_COLOR, alpha=0.55, label="data")
    pdf_lin.hist(sample, bins=bins, weights=np.full(len(sample), 1 / (len(sample) * width)),
                 histtype="step", color=MODEL_COLOR, lw=2, label="model sample")
    pdf_lin.set(xlabel="routes per airport", ylabel="density",
                title="PDF, linear axes (bin = 5 routes)")
    # PDF, log-log: log-width bins; the model sample is continuous, so the per-value mass
    # used for the data-only figure does not apply here.
    log_bins = np.logspace(0, 6, 37)
    pdf_log.plot(*log_binned_pdf(x, log_bins), "o-", ms=4, color=DATA_COLOR, label="data")
    pdf_log.plot(*log_binned_pdf(sample, log_bins), "o-", ms=4, color=MODEL_COLOR,
                 label="model sample")
    outside = float(np.mean((sample < log_bins[0]) | (sample > log_bins[-1])))
    if outside > 0.01:
        pdf_log.text(0.98, 0.92, f"{outside:.0%} of the sample\nlies outside [1, 1e6]",
                     transform=pdf_log.transAxes, ha="right", va="top", color=INK)
    pdf_log.set(xscale="log", yscale="log", xlabel="routes per airport (log)",
                ylabel="density (log)", title="PDF, log-log (log-width bins)")

    # CDF and CCDF over the FULL sample; on log axes only x > 0 is drawn (filtering first
    # would renormalise).
    xs, cdf_s = ecdf(sample)
    _, ccdf_s = ccdf(sample)
    cdf_lin.plot(*ecdf(x), color=DATA_COLOR, lw=2, label="data")
    cdf_lin.plot(xs, cdf_s, color=MODEL_COLOR, lw=2, label="model sample")
    cdf_lin.set(xlabel="routes per airport", ylabel="P(X ≤ x)", title="CDF, linear axes")
    cdf_log.plot(*ecdf(x), color=DATA_COLOR, lw=2, label="data")
    cdf_log.plot(xs[xs > 0], cdf_s[xs > 0], color=MODEL_COLOR, lw=2, label="model sample")
    cdf_log.set(xscale="log", yscale="log", xlabel="routes per airport (log)",
                ylabel="P(X ≤ x) (log)", title="CDF, log-log")
    ccdf_lin.plot(*ccdf(x), color=DATA_COLOR, lw=2, label="data")
    ccdf_lin.plot(xs, ccdf_s, color=MODEL_COLOR, lw=2, label="model sample")
    ccdf_lin.set(xlabel="routes per airport", ylabel="P(X ≥ x)", title="CCDF, linear axes")
    ccdf_log.plot(*ccdf(x), color=DATA_COLOR, lw=2, label="data")
    ccdf_log.plot(xs[xs > 0], ccdf_s[xs > 0], color=MODEL_COLOR, lw=2, label="model sample")
    ccdf_log.set(xscale="log", yscale="log", xlabel="routes per airport (log)",
                 ylabel="P(X ≥ x) (log)", title="CCDF, log-log")

    for ax in (pdf_lin, cdf_lin, ccdf_lin):
        ax.set_xlim(x_lo, x_hi)
        ax.text(0.98, 0.35, f"beyond {x_hi:g} routes:\ndata {beyond_data:.1%}, "
                f"model sample {beyond_model:.1%}", transform=ax.transAxes, ha="right",
                color=INK, fontsize=9)
    # Data median and mean in every distribution panel. These panels are too crowded for
    # labels on the lines, so the lines are named once in the shared legend at the top.
    median, mean = float(np.median(x)), float(x.mean())
    for ax in (pdf_lin, pdf_log, cdf_lin, cdf_log, ccdf_lin, ccdf_log):
        median_line = ax.axvline(median, color=MEDIAN_COLOR, lw=1.5, ls=":")
        mean_line = ax.axvline(mean, color=MEAN_COLOR, lw=1.5, ls="-.")
    handles, names = pdf_log.get_legend_handles_labels()
    fig.legend(handles + [median_line, mean_line],
               names + [f"data median = {median:g}", f"data mean = {mean:.1f}"],
               loc="upper center", ncol=4, bbox_to_anchor=(0.5, 0.975))

    # Value of each CDF / CCDF at x = 1, data above the model.
    cdf_at_1 = [(float(np.mean(x <= 1)), DATA_COLOR), (float(np.mean(sample <= 1)), MODEL_COLOR)]
    ccdf_at_1 = [(float(np.mean(x >= 1)), DATA_COLOR), (float(np.mean(sample >= 1)), MODEL_COLOR)]
    for ax, values, is_log in ((cdf_lin, cdf_at_1, False), (cdf_log, cdf_at_1, True),
                               (ccdf_lin, ccdf_at_1, False), (ccdf_log, ccdf_at_1, True)):
        mark_at_one(ax, values, is_log)

    qq_panel(qq_lin, x, sample, log=False)
    qq_lin.set_title("QQ plot, linear axes")
    qq_panel(qq_log, x, sample, log=True)
    qq_log.set_title("QQ plot, log-log")
    fig.suptitle(f"Airport routes vs {label}", y=0.995)
    save(fig, f"p1a_{key}", top=0.955)


def mark_center(ax: plt.Axes, x: np.ndarray) -> None:
    """Data median and mean as vertical lines, named in the panel's legend. For the votes
    they sit 0.07 apart, so labels on the lines would collide."""
    ax.axvline(float(np.median(x)), color=MEDIAN_COLOR, lw=1.5, ls=":",
               label=f"data median = {np.median(x):.2f}")
    ax.axvline(float(x.mean()), color=MEAN_COLOR, lw=1.5, ls="-.",
               label=f"data mean = {x.mean():.2f}")


def plot_movie_data(x: np.ndarray) -> None:
    # Votes lie in [1.9, 8.5] on a 0.1 grid, so every panel uses linear axes. A vote is an
    # average of many ratings, a continuous quantity that is only recorded to 0.1, so there
    # is no PMF panel: it would show the rounding, and with 0.1 bins the PDF already holds
    # the same information.
    n = len(x)
    fig, ((hist, pdf), (cdf, ccdf_ax)) = plt.subplots(2, 2, figsize=(10, 7.6))
    # Bin edges halfway between 0.1 grid points, so no vote sits on an edge.
    hist.hist(x, bins=np.arange(1.75, 8.75, 0.5), color=DATA_COLOR, edgecolor="white")
    hist.set(xlabel="average vote", ylabel="number of movies",
             title="Histogram (bin = 0.5 vote, counts)")
    pdf.hist(x, bins=np.arange(1.85, 8.65, 0.1), density=True, color=DATA_COLOR)
    pdf.set(xlabel="average vote", ylabel="density",
            title="PDF (bin = 0.1, one per vote value)")
    cdf.plot(*ecdf(x), color=DATA_COLOR, lw=2)
    cdf.set(xlabel="average vote", ylabel="P(X ≤ x)", title="CDF")
    ccdf_ax.plot(*ccdf(x), color=DATA_COLOR, lw=2)
    ccdf_ax.set(xlabel="average vote", ylabel="P(X ≥ x)", title="CCDF")
    for ax in (hist, pdf, cdf, ccdf_ax):
        mark_center(ax, x)
    fig.legend(*hist.get_legend_handles_labels(), loc="upper center", ncol=2,
               bbox_to_anchor=(0.5, 0.965))
    fig.suptitle(f"Movie votes: empirical distribution (n = {n})", y=0.995)
    save(fig, "p1b_0_data", top=0.94)


def plot_movie_model(x: np.ndarray, key: str, label: str, sample: np.ndarray) -> None:
    # PDF and CDF on top, QQ plot and box plot below. The CDF marks the KS gap D where it
    # occurs; the box plot compares centre and spread and shows ratings outside [1, 10].
    fig, ((ax1, ax_cdf), (ax2, ax_box)) = plt.subplots(2, 2, figsize=(10, 7.6))
    # A power-law sample reaches the thousands; clip the PDF view and say how much is hidden.
    lo = min(x.min(), np.quantile(sample, 0.001))
    hi = min(max(x.max(), np.quantile(sample, 0.999)), VOTE_VIEW_MAX)
    # Votes sit on a 0.1 grid; bin edges between grid points stop bins catching 1 or 2 values.
    bins = np.arange(np.floor(lo * 10) / 10 - 0.05, hi + 0.2, 0.2)
    width = bins[1] - bins[0]
    # Weights (not density=True) keep each curve normalised to its whole sample, even if clipped.
    ax1.hist(x, bins=bins, weights=np.full(len(x), 1 / (len(x) * width)), color=DATA_COLOR,
             alpha=0.55, label="data")
    ax1.hist(sample, bins=bins, weights=np.full(len(sample), 1 / (len(sample) * width)),
             histtype="step", color=MODEL_COLOR, lw=2, label="model sample")
    hidden = float(np.mean((sample < bins[0]) | (sample > bins[-1])))
    if hidden > 0.01:
        ax1.text(0.98, 0.4, f"{hidden:.0%} of the sample\nlies beyond this axis",
                 transform=ax1.transAxes, ha="right", color=INK)
    ax1.set(xlabel="average vote", ylabel="density", title="PDF: data vs model sample")
    mark_center(ax1, x)
    ax1.legend(loc="best")
    # CDF over the same view; D is measured on these two curves (ordinary probability scale).
    ax_cdf.plot(*ecdf(x), color=DATA_COLOR, lw=2, label="data")
    ax_cdf.plot(*ecdf(sample), color=MODEL_COLOR, lw=2, label="model sample")
    ks = ks_2samp(x, sample)
    at = float(ks.statistic_location)
    f_data, f_model = float(np.mean(x <= at)), float(np.mean(sample <= at))
    ax_cdf.annotate("", xy=(at, f_model), xytext=(at, f_data),
                    arrowprops=dict(arrowstyle="<->", color=INK, lw=1.5))
    ax_cdf.text(at + 0.15, (f_data + f_model) / 2, f"D = {ks.statistic:.3f}\nat {at:.2f}",
                color=INK, va="center", bbox=LABEL_BOX)
    ax_cdf.set_xlim(ax1.get_xlim())
    ax_cdf.set(xlabel="average vote", ylabel="P(X ≤ x)", title="CDF: data vs model sample")
    ax_cdf.legend(loc="lower right")
    qq_panel(ax2, x, sample, log=hi == VOTE_VIEW_MAX)
    # Box plot: median line, quartile box, whiskers at 1.5 IQR; outliers hidden to keep the
    # power-law sample's thousands from flattening the boxes. Dashed lines mark 1 and 10.
    boxes = ax_box.boxplot([x, sample], vert=False, showfliers=False, widths=0.5,
                           patch_artist=True, tick_labels=["data", "model\nsample"])
    for patch, color in zip(boxes["boxes"], (DATA_COLOR, MODEL_COLOR)):
        patch.set(facecolor=color, alpha=0.55)
    for line in boxes["medians"]:
        line.set(color=INK, lw=2)
    for edge in (1, 10):
        ax_box.axvline(edge, color=INK, ls="--", lw=1)
    ax_box.set_xlim(ax1.get_xlim()[0], max(11.0, ax1.get_xlim()[1]))
    outside = float(np.mean((sample < 1) | (sample > 10)))
    ax_box.text(0.98, 0.5, f"{outside:.0%} of the sample\nis outside [1, 10]",
                transform=ax_box.transAxes, ha="right", va="center", color=INK, bbox=LABEL_BOX)
    ax_box.set(xlabel="average vote", title="Box plot (dashed: possible ratings 1 to 10)")
    fig.suptitle(f"Movie votes vs {label}")
    save(fig, f"p1b_{key}")


# ---------------------------------------------------------------- Problem 1: data and samples

MODEL_KEYS = ("powerlaw", "exponential", "uniform", "normal")


def load_airports() -> np.ndarray:
    return pd.read_csv(DATA_DIR / "01_airport_routes.csv")["NumberOfRoutes"].to_numpy(float)


def load_movies() -> np.ndarray:
    return pd.read_csv(DATA_DIR / "01_movie_votes.csv")["AverageVote"].to_numpy(float)


def load(dataset: str) -> np.ndarray:
    return {"airport": load_airports, "movie": load_movies}[dataset]()


def model_samples(dataset: str) -> dict[str, tuple[str, np.ndarray]]:
    """Samples for one data set, identical to the ones in the report.

    The original single script drew every sample from ONE generator: the four airport
    models first, then the four movie models. Replaying that order keeps every figure and
    every KS distance in the report unchanged when each answer runs on its own.
    """
    rng = np.random.default_rng(SEED)
    samples = sample_models(load_airports(), rng)
    if dataset == "movie":
        samples = sample_models(load_movies(), rng)
    return samples


# ---------------------------------------------------------------- Problem 1: printed steps

def print_header(dataset: str, x: np.ndarray) -> None:
    print(f"== {dataset} data: n = {len(x)}, mean = {x.mean():.4f}, median = {np.median(x):.4f}")


def power_law_steps(x: np.ndarray) -> None:
    fit = fit_power_law(x)
    s = float(np.log(x / fit["x_min"]).sum())
    print(f"n              = {len(x)}")
    print(f"x_min          = min x_i = {fit['x_min']:g}")
    print(f"S              = sum ln(x_i / x_min) = {s:.2f}")
    print(f"n / S          = {len(x)} / {s:.2f} = {len(x) / s:.4f}")
    print(f"alpha          = 1 + n / S = {fit['alpha']:.3f}")


def exponential_steps(x: np.ndarray) -> None:
    print(f"sum x_i        = {x.sum():g}")
    print(f"mean           = {x.sum():g} / {len(x)} = {x.mean():.3f}")
    print(f"lambda         = 1 / mean = {fit_exponential(x)['lambda']:.4f}")


def uniform_steps(x: np.ndarray) -> None:
    fit = fit_uniform(x)
    print(f"a              = min x_i = {fit['a']:g}")
    print(f"b              = max x_i = {fit['b']:g}")


def normal_steps(x: np.ndarray) -> None:
    fit = fit_normal(x)
    ss = float(((x - x.mean()) ** 2).sum())
    print(f"mu             = mean = {fit['mu']:.3f}")
    print(f"sum (x - mu)^2 = {ss:.2f}")
    print(f"variance       = {ss:.2f} / ({len(x)} - 1) = {ss / (len(x) - 1):.4f}")
    print(f"sigma          = sqrt(variance) = {fit['sigma']:.3f}")


def ks_table(dataset: str) -> None:
    x = load(dataset)
    for key, (label, sample) in model_samples(dataset).items():
        print(f"KS vs {key:12s} D = {ks_2samp(x, sample).statistic:.3f}   ({label})")


# ---------------------------------------------------------------- Problem 1: figures

def plot_data_figure(dataset: str) -> None:
    FIG_DIR.mkdir(exist_ok=True)
    x = load(dataset)
    plot_airport_data(x) if dataset == "airport" else plot_movie_data(x)


def plot_model_figure(dataset: str, model: str) -> None:
    FIG_DIR.mkdir(exist_ok=True)
    x = load(dataset)
    label, sample = model_samples(dataset)[model]
    key = f"{MODEL_KEYS.index(model) + 1}_{model}"
    plot = plot_airport_model if dataset == "airport" else plot_movie_model
    plot(x, key, label, sample)
    print(f"wrote figure for {dataset} vs {label}")
