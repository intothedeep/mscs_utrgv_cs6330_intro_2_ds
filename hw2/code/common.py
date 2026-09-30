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
SEED = 6330
VOTE_VIEW_MAX = 20.0  # x-limit for movie PDFs; ratings live in [1, 10]

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


def save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{name}.png", dpi=160)
    plt.close(fig)


def label_vlines(ax: plt.Axes, lines: list[tuple[float, str, str, str]], is_log: bool,
                 at_bottom: bool = False) -> None:
    """Vertical reference lines labelled on the line itself instead of in a legend.

    On log axes the lines are far apart, so each label runs up its own line. On linear axes
    4, 19.8 and 60 sit within a few millimetres of each other, so the labels are stacked to
    the right with a short arrow back to their line.
    """
    at_top = blended_transform_factory(ax.transData, ax.transAxes)  # x in data, y in axes
    for i, (x, color, style, text) in enumerate(lines):
        ax.axvline(x, color=color, lw=1.5, ls=style)
        if is_log:
            y, va = (0.03, "bottom") if at_bottom else (0.97, "top")
            ax.text(x * 1.08, y, text, transform=at_top, rotation=90, ha="left", va=va,
                    color=color, fontsize=9, bbox=LABEL_BOX)
        else:
            y = 0.6 - 0.13 * i  # mid-height: both linear panels are empty there on the right
            ax.annotate(text, xy=(x, y), xycoords=at_top, xytext=(x + 120, y),
                        textcoords=at_top, va="center", color=color, fontsize=9,
                        bbox=LABEL_BOX, arrowprops=dict(arrowstyle="-", color=color, lw=0.8))


def plot_airport_data(x: np.ndarray) -> None:
    # Rows: PDF, PMF, CDF/CCDF. Left column on linear axes shows how bunched up the data is;
    # the right column on log-log axes spreads that bunch out so the shape and the tail can
    # be read. Each row is the same quantity on the two kinds of axes.
    fig, ((pdf_lin, pdf_log), (pmf_lin, pmf_log), (cdf_lin, ccdf_log)) = plt.subplots(
        3, 2, figsize=(10, 10.5))
    n = len(x)
    pdf_lin.hist(x, bins=np.arange(0, x.max() + 20, 20), weights=np.full(n, 1 / n),
                 color=DATA_COLOR)
    pdf_lin.set(xlabel="routes per airport", ylabel="share of airports per bin",
                title="PDF (histogram), linear axes (bin = 20 routes)")
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
    for ax in (pdf_lin, pmf_lin, cdf_lin):
        label_vlines(ax, lines, is_log=False)
    # Log PDF and CCDF run across the top, so their labels go in the empty bottom.
    for ax in (pdf_log, pmf_log, ccdf_log):
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


def plot_airport_model(x: np.ndarray, key: str, label: str, sample: np.ndarray) -> None:
    fig, ((axp, ax0), (ax1, ax2)) = plt.subplots(2, 2, figsize=(10, 7.2))
    # PDF on log-log axes with log-width bins: the model sample is continuous, so the
    # per-value mass used for the data-only figure does not apply here.
    bins = np.logspace(0, 6, 37)
    axp.plot(*log_binned_pdf(x, bins), "o-", ms=4, color=DATA_COLOR, label="data")
    axp.plot(*log_binned_pdf(sample, bins), "o-", ms=4, color=MODEL_COLOR,
             label="model sample")
    outside = float(np.mean((sample < bins[0]) | (sample > bins[-1])))
    if outside > 0.01:
        axp.text(0.98, 0.92, f"{outside:.0%} of the sample\nlies outside [1, 1e6]",
                 transform=axp.transAxes, ha="right", va="top", color=INK)
    axp.set(xscale="log", yscale="log", xlabel="routes per airport (log)",
            ylabel="density (log)", title="PDF, log-log (log-width bins)")
    axp.legend(loc="lower left")
    # Linear-axis CDF, cut at the data's range; the share of the sample beyond it is stated.
    ax0.plot(*ecdf(x), color=DATA_COLOR, lw=2, label="data")
    ax0.plot(*ecdf(sample), color=MODEL_COLOR, lw=2, label="model sample")
    x_hi = 1.1 * float(x.max())
    ax0.set_xlim(min(0.0, float(np.quantile(sample, 0.001))), x_hi)
    beyond = float(np.mean(sample > x_hi))
    if beyond > 0.001:
        ax0.text(0.98, 0.35, f"{beyond:.1%} of the sample\nlies beyond this axis",
                 transform=ax0.transAxes, ha="right", color=INK)
    ax0.set(xlabel="routes per airport", ylabel="P(X ≤ x)", title="CDF, linear axes")
    ax0.legend(loc="lower right")
    ax1.plot(*ccdf(x), color=DATA_COLOR, lw=2, label="data")
    # CCDF over the FULL sample, then hide x <= 0 (log axis); filtering first would renormalise.
    xs, ps = ccdf(sample)
    ax1.plot(xs[xs > 0], ps[xs > 0], color=MODEL_COLOR, lw=2, label="model sample")
    ax1.set(xscale="log", yscale="log", xlabel="routes per airport (log)",
            ylabel="P(X ≥ x) (log)", title="CCDF: data vs model sample")
    ax1.legend(loc="lower left")
    qq_panel(ax2, x, sample, log=True)
    fig.suptitle(f"Airport routes vs {label}")
    save(fig, f"p1a_{key}")


def plot_movie_data(x: np.ndarray) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8))
    ax1.hist(x, bins=np.arange(1.85, 8.65, 0.1), density=True, color=DATA_COLOR)
    ax1.set(xlabel="average vote", ylabel="density",
            title="PDF, histogram (bin = 0.1, one per vote value)")
    ax2.plot(*ecdf(x), color=DATA_COLOR, lw=2)
    ax2.set(xlabel="average vote", ylabel="P(X ≤ x)", title="CDF")
    fig.suptitle(f"Movie votes: empirical distribution (n = {len(x)})")
    save(fig, "p1b_0_data")


def plot_movie_model(x: np.ndarray, key: str, label: str, sample: np.ndarray) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8))
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
        ax1.text(0.98, 0.58, f"{hidden:.0%} of the sample\nlies beyond this axis",
                 transform=ax1.transAxes, ha="right", color=INK)
    ax1.set(xlabel="average vote", ylabel="density", title="PDF: data vs model sample")
    ax1.legend(loc="upper right")
    qq_panel(ax2, x, sample, log=hi == VOTE_VIEW_MAX)
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
