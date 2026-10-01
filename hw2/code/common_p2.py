"""
Shared code for HW2 Problem 2 (age, first digit, last digit of IMDB-WIKI birth dates).
Each answer has its own script, p2_a_age_plot.py ... p2_d_discussion.py.
"""

import numpy as np
import pandas as pd
from common import DATA_COLOR, DATA_DIR, FIG_DIR, INK, MEAN_COLOR, MEDIAN_COLOR, plt, save

DOB_PATH = DATA_DIR / "01_DoB.txt"
REFERENCE_YEAR = 2026  # ages are 2026 minus birth year (owner/professor direction, 2026-09-23)
MAX_AGE = 99  # the assignment: "pick the ones ranging from 1 to 99 years"

# Parsing decisions (checked against the raw year counts, not assumed):
# - Dates are "dd-Mon-yy" or "dd-Mon-yyyy". Every 2-digit year is read as 19yy: IMDB-WIKI was
#   crawled in 2015, so "20"-"24" cannot be 2020-2024, and the counts fall smoothly from the
#   1920s down to "00" with no break that would mark a century switch.
# - Year "0000" is a missing-value placeholder and is dropped.
# - Age = REFERENCE_YEAR - birth year (month/day ignored), kept only if 1 <= age <= 99, the
#   range the assignment asks for.

def parse_birth_dates(raw: pd.Series) -> pd.Series:
    """dd-Mon-yy / dd-Mon-yyyy -> Timestamp; 2-digit years -> 19yy; year 0000 -> NaT."""
    parts = raw.str.strip().str.split("-", expand=True)
    year = parts[2].astype(int)
    year = year.where(parts[2].str.len() == 4, 1900 + year)
    year = year.where(year > 0)
    text = parts[0] + "-" + parts[1] + "-" + year.astype("Int64").astype(str)
    return pd.to_datetime(text, format="%d-%b-%Y", errors="coerce")


def compute_ages(birth: pd.Series, reference_year: int) -> pd.Series:
    """Year difference only (month/day ignored), restricted to 1-MAX_AGE."""
    age = (reference_year - birth.dt.year).dropna().astype(int)
    return age[(age >= 1) & (age <= MAX_AGE)]


def load_birth_dates() -> pd.Series:
    raw = pd.read_csv(DOB_PATH, header=None, names=["dob"], dtype=str)["dob"]
    return parse_birth_dates(raw)


def load_ages() -> pd.Series:
    return compute_ages(load_birth_dates(), REFERENCE_YEAR)


def first_digits(age: pd.Series) -> pd.Series:
    return age.astype(str).str[0].astype(int)


def last_digits(age: pd.Series) -> pd.Series:
    return age % 10


def share_per_value(values: pd.Series, support: range) -> pd.Series:
    return values.value_counts(normalize=True).reindex(support, fill_value=0.0)


def normal_ref(digits: pd.Series, support: range) -> tuple[pd.Series, str]:
    """Normal fitted to the digits (mean, sample SD), as a share per digit: the area between
    d - 0.5 and d + 0.5, so it is comparable to the bars."""
    from scipy.stats import norm
    mu, sigma = float(digits.mean()), float(digits.std(ddof=1))
    k = np.array(list(support), dtype=float)
    shares = norm.cdf(k + 0.5, mu, sigma) - norm.cdf(k - 0.5, mu, sigma)
    return pd.Series(shares, index=list(support)), f"normal fit (μ = {mu:.2f}, σ = {sigma:.2f})"


def mark_center(ax: plt.Axes, values: pd.Series, decimals: int = 2) -> None:
    """Median and mean of the plotted values as vertical lines, named in the legend."""
    ax.axvline(float(values.median()), color=MEDIAN_COLOR, lw=1.8, ls=":",
               label=f"median = {values.median():g}")
    ax.axvline(float(values.mean()), color=MEAN_COLOR, lw=1.8, ls="-.",
               label=f"mean = {values.mean():.{decimals}f}")


def plot_bars(share: pd.Series, uniform: float | None, title: str, xlabel: str, name: str,
              normal: tuple[pd.Series, str] | None = None, n: int | None = None,
              values: pd.Series | None = None, show_spread: bool = False,
              legend_on_top: bool = False, show_mode: bool = False) -> None:
    """Bars of shares; with n, a right-hand axis gives the same heights as numbers of actors;
    with values, their median and mean are drawn as vertical lines, and with show_spread the
    band mean ± σ is shaded and the legend gives σ and the variance; legend_on_top moves the
    legend above the plot, between the title and the bars; show_mode adds the most common
    value as a third centre line."""
    FIG_DIR.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.4 if legend_on_top else 3.6))
    ax.set_axisbelow(True)  # grid behind the bars
    ax.bar(share.index, share.to_numpy(), width=0.8, color=DATA_COLOR, edgecolor="white", lw=0.5,
           label="data")
    if uniform is not None:
        ax.axhline(uniform, color=INK, ls="--", lw=1.2, label=f"uniform = {uniform:.3f}")
    if normal is not None:
        ax.plot(normal[0].index, normal[0].to_numpy(), color=MEDIAN_REF_COLOR, marker="s", ms=5,
                lw=2, ls="--", label=normal[1])
    if values is not None:
        mark_center(ax, values)
    if values is not None and show_mode:
        mode = values.mode().iloc[0]
        # Wide and below the other lines, so a median at the same digit still shows on top.
        ax.axvline(float(mode), color=MODE_COLOR, lw=4, ls="-", alpha=0.6, zorder=1.5,
                   label=f"mode = {mode:g} ({share.max():.1%})")
    if values is not None and show_spread:
        mean, sd = float(values.mean()), float(values.std())
        ax.axvspan(mean - sd, mean + sd, color=MEAN_COLOR, alpha=0.12, lw=0, zorder=0,
                   label=f"mean ± σ (σ = {sd:.2f}, var = {sd ** 2:.2f})")
    if uniform is not None or normal is not None or values is not None:
        refs = [] if normal is None else [normal[0].max()]
        top = max([share.max(), *refs])
        if legend_on_top:
            ax.set_ylim(top=top * 1.1)
            legend = ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=3,
                               frameon=False)
        else:
            # Headroom keeps the legend off the bars; an opaque box keeps the median and mean
            # lines from running through its text.
            ax.set_ylim(top=top * 1.45)
            legend = ax.legend(loc="upper right", ncol=2, frameon=True, facecolor="white",
                               edgecolor="none", framealpha=1)
    ax.set(xlabel=xlabel, ylabel="share of actors")
    if legend_on_top:
        # The title must clear the legend, whose height is known only after a draw.
        fig.canvas.draw()
        ax.set_title(title, pad=legend.get_window_extent().height * 72 / fig.dpi + 12)
    else:
        ax.set_title(title)
    if n is not None:
        count_axis = ax.secondary_yaxis("right", functions=(lambda s: s * n, lambda c: c / n))
        count_axis.set_ylabel("number of actors")
    save(fig, name)


REMOVED_COLOR = "#ff7f50"  # coral: ages the 1-MAX_AGE filter drops
MEDIAN_REF_COLOR = "#2e8b57"  # green: the normal reference curve on the first-digit plot
MODE_COLOR = "#b8860b"  # dark gold: the mode line, a colour no other line uses


def raw_ages(birth: pd.Series) -> pd.Series:
    """Every parseable age before the 1-MAX_AGE filter (placeholder years are already NaT)."""
    return (REFERENCE_YEAR - birth.dt.year).dropna().astype(int)


def plot_age_filter(age_all: pd.Series, name: str) -> None:
    """All ages, one bar per year; bars the 1-MAX_AGE filter removes are coral. Log y, because
    the removed years hold under 2% of people and would be invisible on a linear axis."""
    FIG_DIR.mkdir(exist_ok=True)
    counts = age_all.value_counts().sort_index()
    is_kept = (counts.index >= 1) & (counts.index <= MAX_AGE)
    n_kept, n_removed = int(counts[is_kept].sum()), int(counts[~is_kept].sum())
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.set_axisbelow(True)
    ax.bar(counts.index[is_kept], counts[is_kept], width=0.9, color=DATA_COLOR,
           label=f"kept, age 1-{MAX_AGE} ({n_kept:,})")
    ax.bar(counts.index[~is_kept], counts[~is_kept], width=0.9, color=REMOVED_COLOR,
           label=f"removed, age > {MAX_AGE} ({n_removed:,}, {n_removed / len(age_all):.1%})")
    ax.axvline(MAX_AGE + 0.5, color=INK, ls="--", lw=1)
    mark_center(ax, age_all)
    ax.set_yscale("log")
    ax.set(title=f"All ages in {REFERENCE_YEAR} before the filter (n = {len(age_all):,})",
           xlabel="age (years)", ylabel="number of actors (log)")
    ax.legend(loc="upper right")
    save(fig, name)
