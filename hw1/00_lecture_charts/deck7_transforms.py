"""Deck 7 (Q-Q Plot and Normalization) -> the transform-half figures
(discretization, scaling, quantile normalization, log transform, applied
calories Q-Q), split out of deck7_qq_normalization.py (code.md 300/400 line
rule). Recomputed per architecture.md SS8.

This module only plots and does exact arithmetic (the Iris read is a data
load, not a model fit). It never fits, trains, or runs a notebook.
"""

import numpy as np
import pandas as pd
from deck7_values import (
    AGE,
    E4_A,
    E4_B,
    INCOME,
    QNORM_MATRIX,
    check_iris_transcription,
    qq_positions,
    quantile_normalize,
)
from matplotlib import pyplot as plt
from scipy import stats
from sklearn.datasets import load_iris
from style import ACCENT, CATEGORICAL, INK, MUTED, SECOND, save

__all__ = ["build_all"]


def _iris_bins() -> str:
    """Slides 13-15 (E2): equal-width vs equal-frequency bins on sepal length.
    Boundaries computed on integer tenths to avoid float-grid mismatches (R19).
    """
    iris = load_iris()  # data load only, no fit/predict
    assert iris.feature_names[0].startswith("sepal length"), "column order changed"
    sepal = iris.data[:, 0]
    mismatches = check_iris_transcription(sepal)

    tenths = np.rint(sepal * 10).astype(int)
    lo, hi = tenths.min(), tenths.max()
    w = (hi - lo) / 4  # equal-width, in tenths (R19: w = 0.9cm = 9 tenths)
    edges = [lo + round(i * w) for i in range(5)]

    def _count_right_closed(edges: list[int]) -> list[int]:
        counts = []
        for i in range(4):
            left, right = edges[i], edges[i + 1]
            mask = (tenths > left) & (tenths <= right) if i > 0 else (tenths >= left) & (tenths <= right)
            counts.append(int(mask.sum()))
        return counts

    def _count_left_closed(edges: list[int]) -> list[int]:
        counts = []
        for i in range(4):
            left, right = edges[i], edges[i + 1]
            mask = (tenths >= left) & (tenths < right) if i < 3 else (tenths >= left) & (tenths <= right)
            counts.append(int(mask.sum()))
        return counts

    ew_right = _count_right_closed(edges)
    ew_left = _count_left_closed(edges)

    q = [0.25, 0.5, 0.75]
    inv_cdf = np.quantile(sepal, q, method="inverted_cdf")
    linear = np.quantile(sepal, q, method="linear")
    ef_edges_tenths = [lo] + [round(v * 10) for v in inv_cdf] + [hi]
    ef_counts = _count_right_closed(ef_edges_tenths)

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(8.6, 8.2))
    ax_top.hist(sepal, bins=np.arange(4.25, 8.0, 0.1), color=ACCENT, alpha=0.35,
                edgecolor="white", linewidth=0.3, label="sepal length")
    for e in edges[1:-1]:
        ax_top.axvline(e / 10, color=SECOND, lw=1.6, ls="--")
    for e in inv_cdf:
        ax_top.axvline(e, color=CATEGORICAL[2], lw=1.6, ls=":")
    ax_top.plot([], [], color=SECOND, lw=1.6, ls="--",
                label=f"equal-width  {[round(float(e) / 10, 1) for e in edges[1:-1]]}")
    ax_top.plot([], [], color=CATEGORICAL[2], lw=1.6, ls=":", label=f"equal-freq  {np.round(inv_cdf, 1).tolist()}")
    ax_top.set(xlabel="sepal length (cm)", ylabel="count",
               title=f"Iris sepal length, n={sepal.size} (right-closed bins)")
    ax_top.set_ylim(0, ax_top.get_ylim()[1] * 1.45)  # headroom for the count labels below (I1)
    ax_top.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8)

    # I1: per-bin counts on the chart, right-closed (matches E2's slide convention;
    # the left-closed alternative is printed to console only, since it disagrees here).
    ew_edges_cm = [e / 10 for e in edges]
    ef_edges_cm = [lo / 10] + inv_cdf.tolist() + [hi / 10]
    ymax = ax_top.get_ylim()[1]
    for i in range(4):
        mid_ew = (ew_edges_cm[i] + ew_edges_cm[i + 1]) / 2
        ax_top.text(mid_ew, ymax * 0.92, str(ew_right[i]), color=SECOND, ha="center",
                    va="top", fontsize=9, fontweight="bold")
        mid_ef = (ef_edges_cm[i] + ef_edges_cm[i + 1]) / 2
        ax_top.text(mid_ef, ymax * 0.80, str(ef_counts[i]), color=CATEGORICAL[2], ha="center",
                    va="top", fontsize=9, fontweight="bold")
    ax_top.text(0.01, 0.02, "counts shown: equal-width / equal-freq (legend colors), both right-closed",
                transform=ax_top.transAxes, fontsize=7, color=INK, ha="left", va="bottom")

    xs = np.sort(sepal)
    fhat = np.arange(1, xs.size + 1) / xs.size
    ax_bot.step(fhat, xs, where="post", color=ACCENT, lw=1.8, label="empirical inverse CDF")
    for qi, vi in zip(q, inv_cdf):
        ax_bot.plot([0, qi], [vi, vi], color=MUTED, lw=1, ls=":")
        ax_bot.plot([qi, qi], [xs.min(), vi], color=MUTED, lw=1, ls=":")
    ax_bot.set(xlabel="q", ylabel="F-hat^-1(q)", title="Empirical inverse CDF, q = 0.25, 0.5, 0.75")
    ax_bot.legend(loc="upper left", fontsize=8)
    fig.suptitle("Discretization: equal-width vs equal-frequency (E2, slides 13-15)",
                 fontsize=13, fontweight="bold", color=INK, y=1.01)
    fig.tight_layout()

    print(f"  E2 iris n = {sepal.size}, range = [{sepal.min():.1f}, {sepal.max():.1f}] "
          f"(architecture.md SS8.7: n=150, [4.3, 7.9])")
    print(f"  E2 equal-freq (inverted_cdf) quantiles = {np.round(inv_cdf, 1).tolist()} "
          f"(architecture.md: [5.1, 5.8, 6.4])")
    print(f"  E2 equal-freq (linear) quantiles = {np.round(linear, 4).tolist()}")
    print(f"  E2 equal-freq counts (right-closed) = {ef_counts} (architecture.md: [41, 39, 35, 35])")
    print(f"  E2 equal-width edges = {[round(float(e) / 10, 1) for e in edges[1:-1]]} "
          f"(architecture.md R19: [5.2, 6.1, 7.0])")
    print(f"  E2 equal-width counts right-closed = {ew_right} (architecture.md R19: [45, 50, 43, 12])")
    print(f"  E2 equal-width counts left-closed  = {ew_left} (architecture.md R19: [41, 48, 48, 13])")
    if mismatches:
        print(f"  WARNING: iris transcription mismatch count = {mismatches} (expected 0)")
    return str(save(fig, "07_06_iris_bins"))


def _age_income_scaling() -> str:
    """Slides 16-18, 21 (E5, E6): original, range, z (n-1), robust scaling side by side."""
    range_age = (AGE - AGE.min()) / (AGE.max() - AGE.min())
    range_income = (INCOME - INCOME.min()) / (INCOME.max() - INCOME.min())
    z_age = (AGE - AGE.mean()) / AGE.std(ddof=1)
    z_income = (INCOME - INCOME.mean()) / INCOME.std(ddof=1)
    med_age, med_income = np.median(AGE), np.median(INCOME)
    q1_age, q3_age = np.percentile(AGE, [25, 75])
    q1_income, q3_income = np.percentile(INCOME, [25, 75])
    rob_age = (AGE - med_age) / (q3_age - q1_age)
    rob_income = (INCOME - med_income) / (q3_income - q1_income)

    panels = [
        ("original", AGE, INCOME), ("range [0, 1]", range_age, range_income),
        ("z (n-1)", z_age, z_income), ("robust (median, IQR)", rob_age, rob_income),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(15.0, 4.0))
    for ax, (name, xa, xi) in zip(axes, panels):
        ax.scatter(xa, xi, color=ACCENT, s=55, zorder=2)
        ax.scatter([xa[1]], [xi[1]], color=SECOND, s=90, zorder=3, label="x2")
        if name == "original":
            # I1: same numeric range (0 to max income) on both axes, so age
            # (max 40) collapses to a thin band near zero against income (max
            # 6000) -- this is what "income dominates Euclidean distance"
            # looks like, not an equal aspect ratio (that gives a ~200:1 strip).
            top = float(INCOME.max()) * 1.05
            ax.set_xlim(0, top)
            ax.set_ylim(0, top)
            ax.annotate("age barely moves;\nincome dominates\nEuclidean distance",
                        xy=(0.42, 0.55), xycoords="axes fraction", fontsize=8, color=INK)
            ax.legend(loc="upper right", fontsize=8)
        else:
            ax.legend(loc="upper left", fontsize=8)
        ax.set(xlabel="age", ylabel="income", title=name)
    fig.suptitle("Scaling age and income, 10 people (E5, slides 16-18, 21)",
                 fontsize=13, fontweight="bold", color=INK, y=1.03)
    fig.tight_layout()

    print(f"  E5 range x2 = ({range_age[1]:.3f}, {range_income[1]:.3f}) (architecture.md: (0.071, 0.035))")
    print(f"  E5 z(n) x2 = ({(AGE[1] - AGE.mean()) / AGE.std(ddof=0):.2f}, "
          f"{(INCOME[1] - INCOME.mean()) / INCOME.std(ddof=0):.2f}) (architecture.md slide value: (-1.35, -1.26))")
    print(f"  E5 z(n-1) x2 = ({z_age[1]:.2f}, {z_income[1]:.2f}) (architecture.md recomputed: (-1.28, -1.20))")
    print(f"  E6 robust x2 = ({rob_age[1]:.3f}, {rob_income[1]:.3f}) (architecture.md: (-0.794, -0.800))")

    income_typo = INCOME.copy()
    income_typo[7] = 60000.0
    z_income_typo = (income_typo[1] - income_typo.mean()) / income_typo.std(ddof=0)
    range_income_typo = (income_typo[1] - income_typo.min()) / (income_typo.max() - income_typo.min())
    med_typo, q1_typo, q3_typo = np.median(income_typo), *np.percentile(income_typo, [25, 75])
    rob_income_typo = (income_typo[1] - med_typo) / (q3_typo - q1_typo)
    print(f"  E6 income 6000->60000 typo: z(n) = {z_income_typo:.3f} (architecture.md: -0.437), "
          f"range = {range_income_typo:.5f} (architecture.md: 0.00335), "
          f"robust = {rob_income_typo:.3f} (architecture.md: unchanged, -0.800)")

    # I3: E7 (ex:qq-impute, slide 25 + book's assumption) -- x8's income (6000,
    # index 7) treated as missing. Three standard deviations: the true 10-value
    # sd, the 9-value sd with that row dropped, and the 9-value sd with the
    # gap filled by the 9-value mean.
    dropped = np.delete(INCOME, 7)
    mean_fill = dropped.mean()
    filled = np.append(dropped, mean_fill)
    sd_true, sd_drop, sd_fill = INCOME.std(ddof=1), dropped.std(ddof=1), filled.std(ddof=1)
    print(f"  E7 impute: mean (n=9) = {mean_fill:.1f}, median (n=9) = {np.median(dropped):.1f} "
          f"(architecture.md: mean 2311.1, median 2500)")
    print(f"  E7 sd (true n=10 / dropped n=9 / mean-filled n=10) = "
          f"{sd_true:.1f} / {sd_drop:.1f} / {sd_fill:.1f} "
          f"(architecture.md: 1819.5 / 1481.1 / 1396.4)")
    return str(save(fig, "07_07_age_income_scaling"))


def _quantile_norm_figure() -> str:
    """Slide 20 (R24): original matrix vs quantile-normalized, per-gene color."""
    normed = quantile_normalize(QNORM_MATRIX)
    n_rows, n_cols = QNORM_MATRIX.shape
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.4, 4.4))
    for row in range(n_rows):
        color = CATEGORICAL[row % len(CATEGORICAL)]
        ax_l.plot(range(n_cols), QNORM_MATRIX[row], "o-", color=color, label=f"gene {row + 1}")
        ax_r.plot(range(n_cols), normed[row], "o-", color=color, label=f"gene {row + 1}")
    ax_l.set(xlabel="sample", ylabel="value", xticks=range(n_cols), title="Original")
    ax_r.set(xlabel="sample", ylabel="value", xticks=range(n_cols), title="Quantile-normalized")
    ax_l.legend(loc="upper left", fontsize=8)
    fig.suptitle("Quantile normalization: every sample gets the same value set (slide 20)",
                 fontsize=12, fontweight="bold", color=INK, y=1.03)
    fig.tight_layout()

    matches_slide = bool(np.array_equal(
        normed, np.array([[2, 4.5, 4.5, 2], [3, 2, 6, 4.5], [4.5, 3, 3, 3], [6, 6, 2, 6]])))
    assert matches_slide, "I4 tie-handling fix broke the slide-20 (no-tie) matrix"
    tie_normed = quantile_normalize(np.column_stack([E4_A, E4_B]))
    print(f"  R24 quantile-normalized matrix matches slide 20 exactly = {matches_slide}")
    print(f"  E4 tie example A={E4_A.tolist()}, B={E4_B.tolist()} -> "
          f"A' = {tie_normed[:, 0].tolist()}, B' = {tie_normed[:, 1].tolist()} "
          f"(architecture.md: A' = [4.5, 1.5, 3.5], B' = [4.0, 4.0, 1.5])")
    return str(save(fig, "07_08_quantile_norm"))


def _sugars_log(df: pd.DataFrame) -> str:
    """Slide 22: sugars before/after log1p. log(1+x) because sugars has zeros (R26)."""
    v = df["sugars"].to_numpy(float)
    zero_count = int((v == 0).sum())
    logv = np.log1p(v)
    skew_before = float(pd.Series(v).skew())
    skew_after = float(pd.Series(logv).skew())

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.4))
    for col, (label, data) in enumerate([("sugars (g)", v), ("log(1 + sugars)", logv)]):
        ax_h, ax_q = axes[0, col], axes[1, col]
        ax_h.hist(data, bins=20, color=ACCENT, alpha=0.35, edgecolor="white", linewidth=0.3)
        ax_h.set(xlabel=label, ylabel="count",
                 title=f"skew (pandas .skew(), G1) = {(skew_before if col == 0 else skew_after):.3f}")
        xs = np.sort(data)
        n = xs.size
        z = stats.norm.ppf(qq_positions(n))
        mu, sigma = xs.mean(), xs.std(ddof=1)
        ax_q.scatter(z, xs, color=ACCENT, s=12, alpha=0.6)
        line = np.linspace(z.min(), z.max(), 50)
        ax_q.plot(line, mu + sigma * line, color=SECOND, lw=1.6)
        ax_q.set(xlabel="theoretical (normal)", ylabel=label, title="Normal Q-Q")
    fig.suptitle(f"Log transform of sugars: {zero_count} zero items use log(1 + x) (slide 22)",
                 fontsize=13, fontweight="bold", color=INK, y=1.02)
    fig.tight_layout()
    print(f"  sugars zero count = {zero_count} (architecture.md: 17)")
    print(f"  sugars skew before = {skew_before:.4f}, after log1p = {skew_after:.4f} "
          f"(pandas .skew(), bias-corrected Fisher-Pearson G1, matches def:skewness)")
    return str(save(fig, "07_09_sugars_log"))


def _calories_qq(df: pd.DataFrame) -> str:
    """Applied section, R28: calories Q-Q + Shapiro-Wilk p (04 stub TODO = 0.00038)."""
    v = df["calories"].to_numpy(float)
    xs = np.sort(v)
    n = xs.size
    z = stats.norm.ppf(qq_positions(n))
    mu, sigma = xs.mean(), xs.std(ddof=1)
    _stat, p = stats.shapiro(v)

    fig, ax = plt.subplots(figsize=(7.4, 5.6))
    ax.scatter(z, xs, color=ACCENT, s=20, alpha=0.7, label="calories")
    line = np.linspace(z.min(), z.max(), 50)
    ax.plot(line, mu + sigma * line, color=SECOND, lw=1.8, label=f"y = {mu:.1f} + {sigma:.1f}z")
    ax.annotate(f"Shapiro-Wilk p = {p:.5f}\n{'reject' if p < 0.05 else 'cannot reject'} normality at 0.05",
                (0.03, 0.90), xycoords="axes fraction", fontsize=10, color=INK)
    ax.set(xlabel="theoretical (normal)", ylabel="calories",
           title="calories: histogram looks bell-shaped, Q-Q and Shapiro disagree")
    ax.legend(loc="lower right")
    print(f"  R28 calories Shapiro-Wilk p = {p:.5f} (04 stub TODO / architecture.md: 0.00038)")
    return str(save(fig, "07_10_calories_qq"))


def build_all(df: pd.DataFrame) -> list[str]:
    """Render the transform-half figures (07_06-07_10)."""
    p6 = _iris_bins()
    p7 = _age_income_scaling()
    p8 = _quantile_norm_figure()
    p9 = _sugars_log(df)
    p10 = _calories_qq(df)
    return [p6, p7, p8, p9, p10]
