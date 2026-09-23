"""Book section 2.3.2 'sign and direction of skewness' -> one figure per case.

Three synthetic, fixed-seed samples (right-skewed, symmetric, left-skewed;
left is the exact mirror of right) rendered through the same five chart types
taught in deck 5 (histogram, density line, box plot, violin plot, barcode),
all sharing one x-axis range so the three figures compare directly.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
from style import ACCENT, INK, SECOND, save

__all__ = ["build_all"]

N = 300
RIGHT_SEED = 6330
SYMMETRIC_SEED = 2024
MIRROR_CENTER = 60.0  # left = MIRROR_CENTER - right; negation is skew-exact


@dataclass(frozen=True)
class Case:
    name: str
    label: str
    values: np.ndarray


def _make_cases() -> list[Case]:
    """Build the three fixed-seed samples; left is the algebraic mirror of right."""
    rng_right = np.random.default_rng(RIGHT_SEED)
    right = rng_right.gamma(shape=2.0, scale=8.0, size=N)

    left = MIRROR_CENTER - right

    right_series = pd.Series(right)
    rng_sym = np.random.default_rng(SYMMETRIC_SEED)
    symmetric = rng_sym.normal(loc=right_series.mean(), scale=right_series.std(), size=N)

    return [
        Case("skew_right", "Right-skewed sample (gamma)", right),
        Case("skew_symmetric", "Symmetric sample (normal)", symmetric),
        Case("skew_left", "Left-skewed sample (mirror of right)", left),
    ]


def _shared_xlim(cases: list[Case]) -> tuple[float, float]:
    lo = min(c.values.min() for c in cases)
    hi = max(c.values.max() for c in cases)
    pad = 0.05 * (hi - lo)
    return lo - pad, hi + pad


def _summary(values: np.ndarray) -> dict[str, float]:
    s = pd.Series(values)
    mean, median, sd = s.mean(), s.median(), s.std()
    q1, q3 = np.percentile(values, [25, 75])
    return {
        "n": s.size,
        "g1": s.skew(),
        "mean": mean,
        "median": median,
        "sd": sd,
        "gap": (mean - median) / sd,
        "q1": q1,
        "q3": q3,
    }


def _tail_side(gap: float) -> str:
    if gap > 0.05:
        return "right tail longer"
    if gap < -0.05:
        return "left tail longer"
    return "no longer tail (symmetric)"


def _mark_center(ax: plt.Axes, mean: float, median: float) -> None:
    """Median = black solid line, mean = orange dashed line (matches q1_fig1)."""
    ax.axvline(median, color=INK, linewidth=2)
    ax.axvline(mean, color=SECOND, linewidth=2, linestyle="--")


def _plot_case(case: Case, xlim: tuple[float, float], summary: dict[str, float]) -> str:
    fig, axes = plt.subplots(5, 1, figsize=(6.5, 10.8), sharex=True)
    ax_hist, ax_density, ax_box, ax_violin, ax_barcode = axes

    ax_hist.hist(case.values, bins=24, color=ACCENT, edgecolor="white", linewidth=0.8)
    _mark_center(ax_hist, summary["mean"], summary["median"])
    ax_hist.set_ylabel("count")
    ax_hist.set_title("Histogram", fontsize=10, loc="left")
    ax_hist.legend(
        handles=[
            plt.Line2D([0], [0], color=INK, linewidth=2, label="median"),
            plt.Line2D([0], [0], color=SECOND, linewidth=2, linestyle="--", label="mean"),
        ],
        loc="upper right", fontsize=9, frameon=False,
    )

    grid = np.linspace(xlim[0], xlim[1], 400)
    kde = stats.gaussian_kde(case.values)
    density = kde(grid)
    ax_density.fill_between(grid, density, color=ACCENT, alpha=0.18)
    ax_density.plot(grid, density, color=ACCENT, linewidth=2)
    _mark_center(ax_density, summary["mean"], summary["median"])
    ax_density.set_ylabel("density")
    ax_density.set_title("Density line", fontsize=10, loc="left")

    ax_box.boxplot(case.values, orientation="horizontal", widths=0.5, patch_artist=True,
                    boxprops={"facecolor": ACCENT, "alpha": 0.3, "edgecolor": ACCENT},
                    medianprops={"color": INK, "linewidth": 2},
                    flierprops={"marker": "o", "ms": 4, "mfc": SECOND, "mec": SECOND, "alpha": 0.6})
    ax_box.axvline(summary["mean"], color=SECOND, linewidth=2, linestyle="--")
    ax_box.set_yticks([])
    ax_box.set_title("Box plot", fontsize=10, loc="left")

    parts = ax_violin.violinplot(case.values, orientation="horizontal", widths=0.8,
                                  showmedians=True, showextrema=False)
    for body in parts["bodies"]:
        body.set_facecolor(ACCENT)
        body.set_alpha(0.35)
        body.set_edgecolor(ACCENT)
    parts["cmedians"].set_edgecolor(INK)
    parts["cmedians"].set_linewidth(2)
    ax_violin.axvline(summary["mean"], color=SECOND, linewidth=2, linestyle="--")
    ax_violin.set_yticks([])
    ax_violin.set_title("Violin plot", fontsize=10, loc="left")

    ax_barcode.vlines(case.values, 0.62, 1.38, color=ACCENT, linewidth=1.0, alpha=0.7)
    _mark_center(ax_barcode, summary["mean"], summary["median"])
    ax_barcode.set_yticks([])
    ax_barcode.set_ylim(0.4, 1.6)
    ax_barcode.set_title("Barcode chart", fontsize=10, loc="left")
    ax_barcode.set_xlabel("value")
    ax_barcode.grid(axis="y", visible=False)

    ax_hist.set_xlim(*xlim)
    fig.suptitle(
        f"{case.label}\n"
        f"G1 = {summary['g1']:.2f}   mean = {summary['mean']:.2f}   "
        f"median = {summary['median']:.2f}   "
        f"(mean - median) / sd = {summary['gap']:.2f}",
        fontsize=11, fontweight="bold", color=INK, y=1.0,
    )
    fig.tight_layout()
    return str(save(fig, f"02_{case.name}"))


def build_all(_: pd.DataFrame | None = None) -> list[str]:
    """Render the three skew-sign figures; returns saved paths."""
    cases = _make_cases()
    xlim = _shared_xlim(cases)
    paths = []
    for case in cases:
        summary = _summary(case.values)
        paths.append(_plot_case(case, xlim, summary))
        print(
            f"  {case.name:<15} n={summary['n']}  G1={summary['g1']:.2f}  "
            f"mean={summary['mean']:.2f}  median={summary['median']:.2f}  "
            f"sd={summary['sd']:.2f}  (mean-median)/sd={summary['gap']:.2f}  "
            f"Q1={summary['q1']:.2f}  Q3={summary['q3']:.2f}  {_tail_side(summary['gap'])}"
        )
    return paths


if __name__ == "__main__":
    from style import apply_style

    apply_style()
    print("Skew-sign cases (book 2.3.2)")
    build_all()
