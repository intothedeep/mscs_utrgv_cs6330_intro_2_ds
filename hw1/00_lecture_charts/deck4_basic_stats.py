"""Deck 4 (Basic Statistics) -> figures for random variables, PMF/PDF, CDF,
mode and range (arch-deck4.md SS4, SS6). Values are transcribed from
notes_text/4_BasicStats/slides.md with a slide-source comment, or recomputed
by exact arithmetic / sklearn's load_iris() (data only, no model fitting).

This script only plots, loads data and does arithmetic. It never fits or
trains anything.
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import binom, norm
from sklearn.datasets import load_iris
from style import ACCENT, INK, MUTED, SECOND, save

__all__ = ["build_all"]

# source: slide 11, x/15 example, P(X=x) = x/15 for x in {1..5}
FIFTEENTHS_X = np.array([1, 2, 3, 4, 5])
FIFTEENTHS_P = FIFTEENTHS_X / 15.0

# source: slide 9, iris binomial CDF panel, p rounded on the slide
IRIS_BINOM_P = 0.087
IRIS_BINOM_M = 10

# source: slide 10, fair-die PMF, P(X = k) = 1/6 for k in {1..6}
DICE_PMF = 1 / 6


def _triangle_pdf(x: np.ndarray) -> np.ndarray:
    """Slides 5, 15: triangle density f(x) = x on [0,1], f(x) = 2-x on (1,2]."""
    return np.where(x <= 1, x, 2 - x)


def _confirm_exact_fractions() -> None:
    """arch-deck4.md SS4.1: exact-fraction recompute table, hand values
    already confirmed by the architect; this reprints them next to a script
    computation so a slip in either place is visible."""
    dice_f = np.arange(1, 7) * DICE_PMF
    print(f"  dice F(1..6) = {np.round(dice_f, 4).tolist()} (architect: 0.167,0.333,0.5,0.667,0.833,1)")
    print(f"  dice F(3.5) = {dice_f[2]:.4f} (architect: 0.5, step is flat between integers)")
    print(f"  dice E[X] = {float(np.sum(np.arange(1, 7) * DICE_PMF)):.4f} (architect: 3.5)")

    fifteenths_sum = float(FIFTEENTHS_P.sum())
    f3 = float(FIFTEENTHS_P[:3].sum())
    p_gt3 = 1.0 - f3
    p_ge3 = 1.0 - float(FIFTEENTHS_P[:2].sum())
    print(f"  x/15 sum = {fifteenths_sum:.4f} (architect: 1)")
    print(f"  F(3) = {f3:.4f} (architect: 0.4)")
    print(f"  P(X>3) = 1 - F(3) = {p_gt3:.4f} (architect: 0.6; slide's own P(X>k)=1-P(X<=x) mixes k and x)")
    print(f"  P(X>=3) = 1 - F(2) = {p_ge3:.4f} (architect: 0.8, differs from P(X>3) since >= includes 3)")

    tri_area = float(np.trapezoid(_triangle_pdf(np.linspace(0, 2, 400)), np.linspace(0, 2, 400)))
    tri_p = 1 - 2 * (0.5 ** 2 / 2)
    tri_mean = 1 / 3 + 2 / 3
    print(f"  triangle PDF area = {tri_area:.4f} (architect: 1)")
    print(f"  triangle P(0.5<=X<=1.5) = {tri_p:.4f} (architect: 0.75)")
    print(f"  triangle E[X] = {tri_mean:.4f} (architect: 1)")

    range_before = float(np.ptp([1, 2, 3, 4, 5]))
    range_after = float(np.ptp([1, 2, 3, 4, 100]))
    print(f"  range example {{1,2,3,4,5}}->{{..,100}}: {range_before:.0f} -> {range_after:.0f} (architect: 4 -> 99)")

    mode_before = np.bincount([1, 2, 2, 3, 5]).argmax()
    mode_after = np.bincount([1, 2, 2, 3, 100]).argmax()
    print(f"  mode example {{1,2,2,3,5}}->{{..,100}}: {mode_before} -> {mode_after} (architect: 2 -> 2)")

    flip_before = np.bincount([1, 2, 2, 3, 3, 3]).argmax()
    flip_after = np.bincount([1, 2, 2, 2, 3, 3]).argmax()
    print(f"  mode flip {{1,2,2,3,3,3}}->{{1,2,2,2,3,3}}: {flip_before} -> {flip_after} (architect: 3 -> 2)")


def _confirm_iris_values(x: np.ndarray) -> None:
    """arch-deck4.md SS4.2/SS4.3: confirm iris sepal-length values via the
    same load_iris() data-only path as deck3_data_matrix.py's iris checks."""
    count_ge7 = int((x >= 7).sum())
    f1 = count_ge7 / 150.0
    f0 = 1 - f1
    mean = float(x.mean())
    var0 = float(x.var(ddof=0))
    var1 = float(x.var(ddof=1))
    rounded = np.round(x, 1)
    values, counts = np.unique(rounded, return_counts=True)
    mode_val = float(values[np.argmax(counts)])
    mode_count = int(counts.max())
    x_min, x_max = float(x.min()), float(x.max())
    x_range = round(x_max - x_min, 2)
    binom_f = [round(float(binom.cdf(k, IRIS_BINOM_M, IRIS_BINOM_P)), 4) for k in range(4)]

    print(f"  iris count(x>=7) = {count_ge7} (architect: 13)")
    print(f"  iris f(1)=P(A=1) = {f1:.4f} (architect: 0.0867)")
    print(f"  iris f(0)=P(A=0) = {f0:.4f} (architect: 0.9133)")
    print(f"  iris mean = {mean:.4f} (architect: 5.8433)")
    print(f"  iris var ddof=0 = {var0:.4f} (architect: 0.6811)")
    print(f"  iris var ddof=1 = {var1:.4f} (architect: 0.6857)")
    print(f"  iris mode (rounded 0.1) = {mode_val} count={mode_count} (architect: 5.0, 10 flowers)")
    print(f"  iris min/max/range = {x_min}, {x_max}, {x_range} (architect: 4.3, 7.9, 3.6)")
    print(f"  iris binom F(0..3), p={IRIS_BINOM_P}, m={IRIS_BINOM_M}: {binom_f} "
          "(architect: 0.4025, 0.786, 0.9504, 0.9922)")


def _dice_pmf_cdf() -> str:
    """Slide 10: dice PMF (six equal bars) and CDF (step, open/closed points,
    0 below 1 and 1 above 6)."""
    k = np.arange(1, 7)
    pmf = np.full(6, DICE_PMF)
    fig, (ax_p, ax_c) = plt.subplots(1, 2, figsize=(10.5, 4.6))

    ax_p.bar(k, pmf, color=ACCENT, width=0.5)
    ax_p.set(xlabel="k", ylabel="P(X = k)", title="Dice PMF", xticks=k, ylim=(0, 0.25))

    xs = np.linspace(0.5, 6.5, 400)
    cdf = np.searchsorted(k, xs, side="right") / 6.0
    cdf_closed = np.cumsum(pmf)
    cdf_open = np.concatenate(([0.0], cdf_closed[:-1]))
    ax_c.step(xs, cdf, where="post", color=SECOND, lw=2.0)
    ax_c.scatter(k, cdf_closed, color=SECOND, s=40, zorder=3, label="F(k), closed at k")
    ax_c.scatter(k, cdf_open, facecolors="none", edgecolors=SECOND, s=40, zorder=3,
                 label="open at jump's lower value")
    ax_c.axhline(0, color=MUTED, lw=0.8, ls=":")
    ax_c.axhline(1, color=MUTED, lw=0.8, ls=":")
    ax_c.set(xlabel="x", ylabel="F(x) = P(X <= x)", title="Dice CDF (F(3.5) = F(3) = 0.5)",
              xticks=k, ylim=(-0.05, 1.05))
    ax_c.legend(loc="upper left", fontsize=8)
    fig.suptitle("Dice PMF and CDF (slide 10)", fontsize=13, fontweight="bold", color=INK)
    fig.tight_layout()
    return str(save(fig, "04_01_dice_pmf_cdf"))


def _triangle_pdf_cdf() -> str:
    """Slides 5, 15: triangle density f(x)=x on [0,1], f(x)=2-x on (1,2];
    shaded area for P(0.5<=X<=1.5)=0.75; its CDF with F(1)=0.5 marked."""
    x_up = np.linspace(0, 1, 200)
    x_down = np.linspace(1, 2, 200)
    fig, (ax_p, ax_c) = plt.subplots(1, 2, figsize=(10.5, 4.6))

    ax_p.plot(x_up, _triangle_pdf(x_up), color=ACCENT, lw=2.0)
    ax_p.plot(x_down, _triangle_pdf(x_down), color=ACCENT, lw=2.0)
    fill_x = np.linspace(0.5, 1.5, 200)
    fill_y = _triangle_pdf(fill_x)
    ax_p.fill_between(fill_x, fill_y, color=ACCENT, alpha=0.30, label="P(0.5<=X<=1.5) = 0.75")
    ax_p.set(xlabel="x", ylabel="f(x)", title="Triangle PDF, area = 1", ylim=(0, 1.1))
    ax_p.legend(loc="upper right", fontsize=8)

    x_all = np.linspace(0, 2, 400)
    cdf = np.where(x_all <= 1, x_all ** 2 / 2, 1 - (2 - x_all) ** 2 / 2)
    ax_c.plot(x_all, cdf, color=SECOND, lw=2.0)
    ax_c.scatter([1], [0.5], color=INK, s=50, zorder=3, label="F(1) = 0.5")
    ax_c.set(xlabel="x", ylabel="F(x)", title="Triangle CDF", ylim=(-0.05, 1.05))
    ax_c.legend(loc="upper left", fontsize=8)
    fig.suptitle("Triangle PDF and CDF (slides 5, 15)", fontsize=13, fontweight="bold", color=INK)
    fig.tight_layout()
    return str(save(fig, "04_02_triangle_pdf_cdf"))


def _iris_cdfs(x: np.ndarray) -> str:
    """Slide 9: binomial CDF (p=0.087, m=10) and normal CDF (mu=5.843,
    sigma^2=0.681) side by side, with the iris empirical CDF overlaid on the
    normal panel for reference."""
    mean, var0 = float(x.mean()), float(x.var(ddof=0))
    sigma = float(np.sqrt(var0))
    fig, (ax_b, ax_n) = plt.subplots(1, 2, figsize=(10.5, 4.6))

    ks = np.arange(0, IRIS_BINOM_M + 1)
    cdf_vals = binom.cdf(ks, IRIS_BINOM_M, IRIS_BINOM_P)
    ax_b.step(ks, cdf_vals, where="post", color=ACCENT, lw=2.0)
    ax_b.scatter(ks, cdf_vals, color=ACCENT, s=30, zorder=3)
    ax_b.set(xlabel="k (successes out of 10)", ylabel="F(k)",
              title=f"Binomial CDF, p={IRIS_BINOM_P}, m={IRIS_BINOM_M}", ylim=(-0.05, 1.05))

    grid = np.linspace(mean - 4 * sigma, mean + 4 * sigma, 400)
    ax_n.plot(grid, norm.cdf(grid, mean, sigma), color=SECOND, lw=2.0, label="fitted normal CDF")
    xs = np.sort(x)
    emp = np.arange(1, xs.size + 1) / xs.size
    ax_n.step(xs, emp, where="post", color=MUTED, lw=1.2, alpha=0.7, label="iris empirical CDF")
    ax_n.scatter([mean], [0.5], color=INK, s=50, zorder=3, label=f"(mean={mean:.3f}, 0.5)")
    ax_n.set(xlabel="sepal length (cm)", ylabel="F(x)",
              title=f"Normal CDF, mu={mean:.3f}, sigma^2={var0:.3f} (n divisor)", ylim=(-0.05, 1.05))
    ax_n.legend(loc="upper left", fontsize=8)
    fig.suptitle("Iris binomial and normal CDFs (slide 9)", fontsize=13, fontweight="bold", color=INK)
    fig.tight_layout()
    return str(save(fig, "04_03_iris_cdfs"))


def _iris_mode_range(x: np.ndarray) -> str:
    """Slides 17, 19, 20: sepal-length frequency at 0.1 cm resolution, mode
    bar highlighted, mean line, min/max range arrow."""
    rounded = np.round(x, 1)
    values, counts = np.unique(rounded, return_counts=True)
    mode_val = float(values[np.argmax(counts)])
    mean = float(x.mean())
    x_min, x_max = float(x.min()), float(x.max())

    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    colors = [ACCENT if v == mode_val else MUTED for v in values]
    ax.bar(values, counts, width=0.08, color=colors)
    ax.axvline(mean, color=SECOND, lw=1.8, ls="--", label=f"mean = {mean:.3f}")
    ax.annotate("", xy=(x_max, -0.6), xytext=(x_min, -0.6),
                arrowprops={"arrowstyle": "<->", "color": INK, "lw": 1.4},
                annotation_clip=False)
    ax.text((x_min + x_max) / 2, -1.3, f"range = {x_max - x_min:.1f}", ha="center", color=INK, fontsize=9)
    ax.set(xlabel="sepal length (cm)", ylabel="count",
           title=f"Iris sepal length: mode = {mode_val} cm, min={x_min}, max={x_max}")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_ylim(bottom=-2)
    fig.tight_layout()
    return str(save(fig, "04_04_iris_mode_range"))


def build_all() -> list[str]:
    """Render every deck-4 figure; prints every hand-computed value
    arch-deck4.md asks to confirm, next to the architect's value."""
    _confirm_exact_fractions()

    iris = load_iris()
    x = iris.data[:, 0]  # sepal length, data only, no model fitting
    _confirm_iris_values(x)

    p1 = _dice_pmf_cdf()
    p2 = _triangle_pdf_cdf()
    p3 = _iris_cdfs(x)
    p4 = _iris_mode_range(x)
    return [p1, p2, p3, p4]


if __name__ == "__main__":
    from style import apply_style

    apply_style()
    print("Deck 4 - Basic Statistics")
    build_all()
