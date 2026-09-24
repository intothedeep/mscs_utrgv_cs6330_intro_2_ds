"""Deck 7 (Q-Q Plot and Normalization) -> the distribution-check figures
(candidate PDFs/CDFs, Q-Q plots) on the fast-food and HW2 movie-vote data,
plus the transcribed slide constants in deck7_values.py. Recomputed per
architecture.md SS8. deck7_transforms.py carries the transform-half figures
(discretization, scaling, quantile norm, log, applied calories) -- this
module's own responsibility is "how do we tell what distribution this is"
(code.md 300/400 line rule).

This script only plots and does exact arithmetic. It never fits, trains, or
runs a notebook.
"""

from pathlib import Path

import deck7_transforms
import numpy as np
import pandas as pd
from deck7_values import E1_DATA, E3_A, E3_B, qq_positions
from matplotlib import pyplot as plt
from scipy import stats
from style import ACCENT, INK, MUTED, SECOND, save

__all__ = ["build_all"]

SEED = 6330
MOVIE_PATH = Path(__file__).resolve().parents[2] / "hw2" / "00_doc" / "01_movie_votes.csv"


def _load_movies() -> np.ndarray:
    """Slides 2-4 data source (R8, confirmed = HW2 movie votes)."""
    return pd.read_csv(MOVIE_PATH)["AverageVote"].to_numpy(float)


def _movie_fits(x: np.ndarray) -> dict[str, float]:
    """Same MLE formulas as hw2/code/p1.py fit_power_law/exponential/uniform/normal."""
    x_min, x_max = float(x.min()), float(x.max())
    alpha = 1.0 + len(x) / float(np.log(x / x_min).sum())
    return {
        "alpha": alpha, "x_min": x_min, "lambda": 1.0 / float(x.mean()),
        "a": x_min, "b": x_max, "mu": float(x.mean()), "sigma": float(x.std(ddof=1)),
    }


def _movie_four_pdf(x: np.ndarray, fit: dict[str, float]) -> str:
    """Slide 3 (image9): histogram + four candidate densities, one panel each."""
    bins = np.arange(1.85, 8.65, 0.1)  # same grid as hw2/code/p1.py plot_movie_data
    grid = np.linspace(fit["x_min"], x.max(), 500)
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))
    panels = [
        ("power law", stats.pareto.pdf(grid, fit["alpha"] - 1, scale=fit["x_min"]),
         f"alpha = {fit['alpha']:.3f}"),
        ("exponential", stats.expon.pdf(grid, scale=1 / fit["lambda"]), f"lambda = {fit['lambda']:.4f}"),
        ("uniform", stats.uniform.pdf(grid, fit["a"], fit["b"] - fit["a"]), f"[{fit['a']:.1f}, {fit['b']:.1f}]"),
        ("normal", stats.norm.pdf(grid, fit["mu"], fit["sigma"]), f"mu={fit['mu']:.2f}, sigma={fit['sigma']:.2f}"),
    ]
    for ax, (name, curve, label) in zip(axes.flat, panels):
        ax.hist(x, bins=bins, density=True, color=ACCENT, alpha=0.30,
                edgecolor="white", linewidth=0.4, label="movie votes")
        ax.plot(grid, curve, color=SECOND, lw=2.0, label=f"{name}  {label}")
        ax.set(xlabel="average vote", ylabel="density", title=name.title())
        ax.legend(loc="upper right", fontsize=8)
    fig.suptitle("Four candidate distributions over movie votes (slide 3)",
                 fontsize=13, fontweight="bold", color=INK, y=1.02)
    fig.tight_layout()
    return str(save(fig, "07_01_movie_four_pdfs"))


def _movie_four_cdf(x: np.ndarray, fit: dict[str, float]) -> str:
    """Slide 4 (image10): empirical vs candidate CDFs; log x for the heavy-tailed pair."""
    xs = np.sort(x)
    n = xs.size
    emp = np.arange(1, n + 1) / n
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))
    cdfs = {
        "power law": stats.pareto.cdf(xs, fit["alpha"] - 1, scale=fit["x_min"]),
        "exponential": stats.expon.cdf(xs, scale=1 / fit["lambda"]),
        "uniform": stats.uniform.cdf(xs, fit["a"], fit["b"] - fit["a"]),
        "normal": stats.norm.cdf(xs, fit["mu"], fit["sigma"]),
    }
    for ax, (name, cand) in zip(axes.flat, cdfs.items()):
        above = emp - cand
        below = cand - (np.arange(0, n) / n)
        i_above, i_below = int(np.argmax(above)), int(np.argmax(below))
        if above[i_above] >= below[i_below]:
            d, d_x = float(above[i_above]), float(xs[i_above])
        else:
            d, d_x = float(below[i_below]), float(xs[i_below])
        ax.step(xs, emp, where="post", color=ACCENT, lw=1.6, label="empirical CDF")
        ax.plot(xs, cand, color=SECOND, lw=1.8, ls="--", label=f"{name} CDF")
        ax.axvline(d_x, color=INK, lw=1.3, ls="-.", label=f"max gap D={d:.3f} @ x={d_x:.2f}")
        if name in ("power law", "exponential"):
            ax.set_xscale("log")
        ax.set(xlabel="average vote", ylabel="P(X <= x)", title=f"{name.title()}  D = {d:.3f}")
        ax.legend(loc="lower right", fontsize=8)
    fig.suptitle("Empirical vs candidate CDFs (slide 4). One-sample D, "
                  "optimistic since parameters were fit to this same data",
                  fontsize=12, fontweight="bold", color=INK, y=1.02)
    fig.tight_layout()
    return str(save(fig, "07_02_movie_four_cdfs"))


def _qq_steps() -> str:
    """Slides 6-8 (E1 by hand): normal (top row) and uniform (bottom row), three
    steps each. Reference line for normal uses mean/std(ddof=1), matching def:spread.
    """
    xs = np.sort(E1_DATA)
    n = xs.size
    p = qq_positions(n)
    mean, std = xs.mean(), xs.std(ddof=1)
    z = stats.norm.ppf(p)
    a, b = xs.min(), xs.max()  # uniform MLE

    fig, axes = plt.subplots(2, 3, figsize=(12.6, 7.4))

    # --- normal row ---
    ax = axes[0, 0]
    ax.scatter(np.zeros(n), xs, color=ACCENT, s=70, zorder=3)
    ax.set(xticks=[], ylabel="data value", title="1. Sort the data")
    ax.set_xlim(-1, 1)

    ax = axes[0, 1]
    grid = np.linspace(-3, 3, 400)
    ax.plot(grid, stats.norm.pdf(grid), color=MUTED, lw=1.6)
    for zi in z:
        ax.axvline(zi, color=ACCENT, lw=1.2, ls=":")
    middle_gap, edge_gap = z[3] - z[2], z[1] - z[0]
    ax.set(xlabel="z", title=f"2. Theoretical quantiles $\\Phi^{{-1}}(i/{n+1})$\n"
                              f"middle gap {middle_gap:.3f}, edge gap {edge_gap:.3f}")

    ax = axes[0, 2]
    ax.scatter(z, xs, color=ACCENT, s=70, zorder=3, label="Q-Q points")
    line_x = np.linspace(z.min() - 0.3, z.max() + 0.3, 50)
    ax.plot(line_x, mean + std * line_x, color=SECOND, lw=1.8, label=f"y = {mean:.1f} + {std:.3f}z")
    ax.set(xlabel="theoretical (normal)", ylabel="data", title="3. Q-Q plot vs Normal")
    ax.legend(loc="upper left", fontsize=8)

    # --- uniform row: theoretical quantiles are on [0, 1] (E1: "구간 [0, 1],
    # p_i 그대로" -- the Uniform[0, 1] quantile function is the identity, so
    # u = p exactly, not scaled to the data's own [min, max]).
    u = p
    ax = axes[1, 0]
    ax.scatter(np.zeros(n), xs, color=SECOND, s=70, zorder=3)
    ax.set(xticks=[], ylabel="data value", title="1. Sort the data")
    ax.set_xlim(-1, 1)

    ax = axes[1, 1]
    ax.hlines(1.0, 0, 1, color=MUTED, lw=1.6)
    for ui in u:
        ax.axvline(ui, color=SECOND, lw=1.2, ls=":")
    ax.set(xlabel="x", ylim=(0, 1.5), title="2. Theoretical quantiles, Uniform[0, 1]")

    ax = axes[1, 2]
    ax.scatter(u, xs, color=SECOND, s=70, zorder=3, label="Q-Q points")
    line_u = np.linspace(0, 1, 50)
    ax.plot(line_u, a + (b - a) * line_u, color=ACCENT, lw=1.8, ls="--",
            label=f"y = {a:.0f} + {b - a:.0f}p")
    ax.set(xlabel="theoretical (uniform, [0, 1])", ylabel="data", title="3. Q-Q plot vs Uniform")
    ax.legend(loc="upper left", fontsize=8)

    fig.suptitle("Q-Q plot, step by step, on 5 points {3, 4, 5, 6, 12} (E1, slides 6-8)",
                 fontsize=13, fontweight="bold", color=INK, y=1.02)
    fig.tight_layout()
    print(f"  E1 p_i = i/{n + 1}: {np.round(p, 4).tolist()}")
    print(f"  E1 norm.ppf(p_i): {np.round(z, 4).tolist()}")
    print(f"  E1 own middle gap = {z[3] - z[2]:.4f}, edge gap = {z[1] - z[0]:.4f} "
          f"(this is E1's n=5 gap, not R12 which is slide 6's n=15 example)")
    print(f"  E1 uniform quantiles (interval [0, 1]): u_i = p_i = {np.round(u, 4).tolist()}")
    return str(save(fig, "07_03_qq_steps"))


def _qq_shapes() -> str:
    """Slides 9-10: five shapes, histogram + normal Q-Q, each n=1000, seed 6330.
    Overlaid normal curve uses the SAMPLE's own mean/std (avoids R15's weak example).
    """
    rng = np.random.default_rng(SEED)
    n = 1000
    normal = rng.normal(0, 1, n)
    right = rng.lognormal(0, 0.6, n)
    left = -right  # mirror: exact negation of right skew (skew_cases.py convention)
    fat = rng.standard_t(3, n)
    thin = rng.uniform(-1.7, 1.7, n)
    cases = [
        ("Normal", normal), ("Right skew (lognormal)", right),
        ("Left skew (mirrored lognormal)", left), ("Fat tails (t, df=3)", fat),
        ("Thin tails (uniform)", thin),
    ]
    fig, axes = plt.subplots(5, 2, figsize=(9.6, 15.5))
    for row, (name, sample) in enumerate(cases):
        mu, sigma = sample.mean(), sample.std(ddof=1)
        ax_h, ax_q = axes[row]
        lo, hi = np.percentile(sample, [1, 99]) if "t, df=3" in name else (sample.min(), sample.max())
        ax_h.hist(sample, bins=40, range=(lo, hi), density=True, color=ACCENT, alpha=0.35,
                   edgecolor="white", linewidth=0.3)
        grid = np.linspace(lo, hi, 300)
        ax_h.plot(grid, stats.norm.pdf(grid, mu, sigma), color=SECOND, lw=1.8)
        ax_h.set(ylabel=name, title="histogram" if row == 0 else None)
        if "t, df=3" in name:
            ax_h.set_xlabel("clipped to 1st-99th percentile (heavy tails)")

        xs = np.sort(sample)
        p = qq_positions(n)
        z = stats.norm.ppf(p)
        ax_q.scatter(z, xs, color=ACCENT, s=4, alpha=0.5)
        line = np.linspace(z.min(), z.max(), 50)
        ax_q.plot(line, mu + sigma * line, color=SECOND, lw=1.5)
        ax_q.set(title="Normal Q-Q" if row == 0 else None)
    fig.suptitle("Reading Q-Q shapes: skew and tail weight (slides 9-10)",
                 fontsize=13, fontweight="bold", color=INK, y=1.005)
    fig.tight_layout()
    return str(save(fig, "07_04_qq_shapes"))


def _qq_two_samples() -> str:
    """Slide 11 (E3): A (n=15) vs B (n=4), B's positions (i-1)/(n-1) matched into A
    by linear interpolation (03's rule, since this compares two samples).
    """
    a_sorted = np.sort(E3_A)
    b_sorted = np.sort(E3_B)
    pos_a = np.linspace(0, 1, a_sorted.size)
    pos_b = np.linspace(0, 1, b_sorted.size)
    a_at_b = np.interp(pos_b, pos_a, a_sorted)

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(11.0, 4.8))
    ax_l.scatter(np.zeros(a_sorted.size), a_sorted, color=ACCENT, s=50, label=f"A (n={a_sorted.size})")
    ax_l.scatter(np.ones(b_sorted.size), b_sorted, color=SECOND, s=70, label=f"B (n={b_sorted.size})")
    for bi, ai in zip(b_sorted, a_at_b):
        ax_l.plot([0, 1], [ai, bi], color=MUTED, lw=1, ls=":")
    ax_l.set(xticks=[0, 1], xticklabels=["A", "B"], ylabel="value",
             title="B's positions matched into A by interpolation")
    ax_l.legend(loc="upper left", fontsize=8)

    ax_r.scatter(b_sorted, a_at_b, color=ACCENT, s=80, zorder=3)
    line = np.linspace(min(b_sorted.min(), a_at_b.min()), max(b_sorted.max(), a_at_b.max()), 50)
    ax_r.plot(line, line, color=SECOND, lw=1.6, ls="--", label="y = x")
    ax_r.set(xlabel="B (data)", ylabel="A (interpolated quantile)",
             title="Q-Q: A more spread than B (slope > 1)")
    ax_r.legend(loc="upper left", fontsize=8)
    fig.suptitle("Two-sample Q-Q, different sizes (E3, slide 11)",
                 fontsize=13, fontweight="bold", color=INK, y=1.03)
    fig.tight_layout()
    print(f"  E3 A quantiles at B's positions (i-1)/(n-1): {np.round(a_at_b, 3).tolist()} "
          f"(architecture.md: [2, 4.833, 6.167, 11])")
    p_alt = qq_positions(4)
    a_at_b_alt = np.interp(p_alt, pos_a, a_sorted)
    print(f"  E3 same B with i/(n+1) instead: {np.round(a_at_b_alt, 3).tolist()} (architecture.md notes 0.2/0.4/0.6/0.8 quantiles of A)")
    return str(save(fig, "07_05_qq_two_samples"))


def build_all(df: pd.DataFrame) -> list[str]:
    """Render every deck-7 figure and print every value T05/A07 asked for."""
    movies = _load_movies()
    fit = _movie_fits(movies)
    print(f"  R8 movie fits: power_law alpha={fit['alpha']:.4f} x_min={fit['x_min']:.1f}, "
          f"exponential lambda={fit['lambda']:.4f}, uniform=[{fit['a']:.1f}, {fit['b']:.1f}], "
          f"normal mu={fit['mu']:.3f} sigma={fit['sigma']:.3f} "
          f"(architecture.md: alpha=1.851 x_min=1.9, lambda=0.1606, [1.9, 8.5], mu=6.227 sigma=0.893)")

    p1 = _movie_four_pdf(movies, fit)
    p2 = _movie_four_cdf(movies, fit)
    p3 = _qq_steps()

    n16 = np.array([1, 2, 3, 8, 9])
    z16 = stats.norm.ppf(n16 / 16)
    print(f"  R10 norm.ppf(i/16) i={n16.tolist()}: {np.round(z16, 4).tolist()} "
          f"(architecture.md: -1.534, -1.150, -0.887, 0, 0.157)")
    print(f"  R12 slide-6 (n=15) middle gap = {z16[4] - 0:.4f}, edge gap = {z16[1] - z16[0]:.4f} "
          f"(architecture.md: 0.157, 0.384)")

    p4 = _qq_shapes()
    p5 = _qq_two_samples()
    rest = deck7_transforms.build_all(df)

    return [p1, p2, p3, p4, p5, *rest]


if __name__ == "__main__":
    from data import load
    from style import apply_style

    apply_style()
    print("Deck 7 - Q-Q Plot and Normalization")
    build_all(load())
