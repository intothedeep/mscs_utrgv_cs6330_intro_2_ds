"""Deck 11 (Comparing Distributions) -> figures on values transcribed from
slides.md (notes_text/11_Comparing_Distributions/) and recomputed per
architecture.md SS7.4.4/7.4.6.

Every value lives once here, with its slide source noted in a comment; this
script only plots and does exact arithmetic, it never fits or trains anything.
"""

from collections import Counter

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from scipy.stats import kstwobign
from style import ACCENT, INK, MUTED, SECOND, save

__all__ = ["build_all"]

WARN = "#c0392b"  # rejection-region / gap-marker color

# source: media/image40.png (slide 17), transcribed once, row by row exactly
# as printed (10 rows x 10 columns, unsorted "given" data)
KS_DATA = np.array([
    -0.16, -0.68, -0.32, -0.85, 0.89, -2.28, 0.63, 0.41, 0.15, 0.74,
    1.30, -0.13, 0.80, -0.75, 0.28, -1.00, 0.14, -1.38, -0.04, -0.25,
    -0.17, 1.29, 0.47, -1.23, 0.21, -0.04, 0.07, -0.08, 0.32, -0.17,
    0.13, -1.94, 0.78, 0.19, -0.12, -0.19, 0.76, -1.48, -0.01, 0.20,
    -1.97, -0.37, 3.08, -0.40, 0.80, 0.01, 1.32, -0.47, 2.29, -0.26,
    -1.52, -0.06, -1.02, 1.06, 0.60, 1.15, 1.92, -0.06, -0.19, 0.67,
    0.29, 0.58, 0.02, 2.18, -0.04, -0.13, -0.79, -1.28, -1.41, -0.23,
    0.65, -0.26, -0.17, -1.53, -1.69, -1.60, 0.09, -1.11, 0.30, 0.71,
    -0.88, -0.03, 0.56, -3.68, 2.40, 0.62, 0.52, -1.25, 0.85, -0.09,
    -0.23, -1.16, 0.22, -1.68, 0.50, -0.35, -0.35, -0.33, -0.24, 0.25,
])

# source: media/image39.png (slide 17), the slide's own sorted table, used
# only to check the transcription above (R15's transcription-verification step)
KS_DATA_SORTED_SLIDE = np.array([
    -3.68, -2.28, -1.97, -1.94, -1.69, -1.68, -1.60, -1.53, -1.52, -1.48,
    -1.41, -1.38, -1.28, -1.25, -1.23, -1.16, -1.11, -1.02, -1.00, -0.88,
    -0.85, -0.79, -0.75, -0.68, -0.47, -0.40, -0.37, -0.35, -0.35, -0.33,
    -0.32, -0.26, -0.26, -0.25, -0.24, -0.23, -0.23, -0.19, -0.19, -0.17,
    -0.17, -0.17, -0.16, -0.13, -0.13, -0.12, -0.09, -0.08, -0.06, -0.06,
    -0.04, -0.04, -0.04, -0.03, -0.01, 0.01, 0.02, 0.07, 0.09, 0.13,
    0.14, 0.15, 0.19, 0.20, 0.21, 0.22, 0.25, 0.28, 0.29, 0.30,
    0.32, 0.41, 0.47, 0.50, 0.52, 0.56, 0.58, 0.60, 0.62, 0.63,
    0.65, 0.67, 0.71, 0.74, 0.76, 0.78, 0.80, 0.80, 0.85, 0.89,
    1.06, 1.15, 1.29, 1.30, 1.32, 1.92, 2.18, 2.29, 2.40, 3.08,
])

# source: media/image43.png (slide 21): two-sample KS example
KS_X = np.array([1.2, 1.4, 1.9, 3.7, 4.4, 4.8, 9.7, 17.3, 21.1, 28.4])  # n=10
KS_Y = np.array([5.6, 6.5, 6.6, 6.9, 9.2, 10.4, 10.6, 19.3])  # n=8


def _check_ks_transcription() -> int:
    """Sort KS_DATA and compare, element by element, to the slide's own
    sorted table (image39). Returns the position mismatch count.
    """
    mine_sorted = np.sort(KS_DATA)
    mismatch_mask = ~np.isclose(mine_sorted, KS_DATA_SORTED_SLIDE, atol=1e-9)
    mismatches = int(mismatch_mask.sum())
    diff = Counter(mine_sorted.tolist()) - Counter(KS_DATA_SORTED_SLIDE.tolist())
    diff_back = Counter(KS_DATA_SORTED_SLIDE.tolist()) - Counter(mine_sorted.tolist())
    print(f"  transcription check: {len(KS_DATA)} values, sorted vs image39, "
          f"position mismatches = {mismatches}, "
          f"multiset diff (image40 raw has extra) = {dict(diff)}, "
          f"(image39 sorted has extra) = {dict(diff_back)}")
    return mismatches


def _t_vs_normal() -> str:
    """Slide 3 (t formula), slide 9 (image20/21/22, t=2.75, df=5, two-sided
    p ~ 0.04, R4). N(0,1) vs t(df=5) vs t(df=24) (df=24 is the R3 example,
    slide 5): heavier tails at low df mean the same |t| gives a larger p.
    """
    x = np.linspace(-4.5, 4.5, 500)
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.plot(x, stats.norm.pdf(x), color=INK, lw=2, label="N(0, 1)")
    ax.plot(x, stats.t.pdf(x, df=24), color=ACCENT, lw=2, label="t, df=24 (R3, slide 5)")
    ax.plot(x, stats.t.pdf(x, df=5), color=SECOND, lw=2, label="t, df=5 (R4, slide 9)")

    t_crit = 2.75
    tail_lo = np.linspace(-4.5, -t_crit, 100)
    tail_hi = np.linspace(t_crit, 4.5, 100)
    ax.fill_between(tail_lo, stats.t.pdf(tail_lo, df=5), color=SECOND, alpha=0.5)
    ax.fill_between(tail_hi, stats.t.pdf(tail_hi, df=5), color=SECOND, alpha=0.5)
    two_sided_p = 2 * stats.t.sf(t_crit, df=5)
    ax.annotate(f"|t| >= 2.75, df=5\ntwo-sided p = {two_sided_p:.3f}", (t_crit, 0.02),
                textcoords="offset points", xytext=(10, 40), fontsize=9, color=INK)

    ax.set_xlabel("t")
    ax.set_ylabel("density")
    ax.set_title("t-distribution vs N(0,1): heavier tails at low df (slides 3, 9)", fontsize=12)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()

    p_r3 = stats.t.cdf(-2.5, df=24)
    print(f"  11_01 R3 t.cdf(-2.5, 24) = {p_r3:.4f} (architecture.md: approx 0.0098)")
    print(f"  11_01 R4 2*t.sf(2.75, 5) = {two_sided_p:.4f} (architecture.md: approx 0.040)")
    return str(save(fig, "11_01_t_vs_normal"))


def _anova_cartoon() -> str:
    """Slide 11: three groups of cartoon-watching hours, {3,2,1}, {5,3,4},
    {5,6,7}; group means 2, 4, 6; grand mean 4 (R8). Left panel: SSW (point
    to its own group mean). Right panel: SSB (group mean to grand mean).
    Same layout as deck9's fig:ht-pooled-vs-group.
    """
    college = np.array([3.0, 2.0, 1.0])
    highschool = np.array([5.0, 3.0, 4.0])
    elementary = np.array([5.0, 6.0, 7.0])
    groups = [("College", college), ("Highschool", highschool), ("Elementary", elementary)]
    all_vals = np.concatenate([college, highschool, elementary])
    grand_mean = all_vals.mean()
    group_means = [g.mean() for _, g in groups]

    ssw = float(sum(((g - g.mean()) ** 2).sum() for _, g in groups))
    ssb = float(sum(len(g) * (g.mean() - grand_mean) ** 2 for _, g in groups))

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(11.0, 4.6), sharey=True)
    colors = [ACCENT, SECOND, "#1baf7a"]
    xs = [np.array([0, 1, 2]), np.array([3, 4, 5]), np.array([6, 7, 8])]

    for (label, g), x, color, gm in zip(groups, xs, colors, group_means):
        ax_l.scatter(x, g, color=color, s=90, zorder=3, label=label)
        for xi, yi in zip(x, g):
            ax_l.plot([xi, xi], [gm, yi], color=MUTED, lw=1.2, zorder=2)
        ax_l.hlines(gm, x[0] - 0.4, x[-1] + 0.4, color=color, lw=2)
    ax_l.set_title(f"Within groups: SSW = {ssw:.0f} (df 6)", fontsize=11)
    ax_l.set_xticks([])
    ax_l.set_ylabel("hours watching cartoons")
    ax_l.legend(loc="upper left", fontsize=9)

    for (label, g), x, color, gm in zip(groups, xs, colors, group_means):
        ax_r.scatter(x, g, color=color, s=90, zorder=3, label=label)
        for xi in x:
            ax_r.plot([xi, xi], [grand_mean, gm], color=MUTED, lw=1.2, zorder=2)
    ax_r.axhline(grand_mean, color=INK, lw=2, label=f"grand mean = {grand_mean:.0f}")
    ax_r.set_title(f"Between groups: SSB = {ssb:.0f} (df 2)", fontsize=11)
    ax_r.set_xticks([])
    ax_r.legend(loc="upper left", fontsize=9)

    f_stat = (ssb / 2) / (ssw / 6)
    fig.suptitle(f"ANOVA cartoon-watching example (slide 11): F = {f_stat:.0f}, "
                 "critical F(0.10, 2, 6) = 3.46 (slide 12) -> reject",
                 fontsize=12, fontweight="bold", color=INK, y=1.03)
    fig.tight_layout()

    f_sf = stats.f.sf(12, 2, 6)
    f_ppf = stats.f.ppf(0.90, 2, 6)
    print(f"  11_02 SSW = {ssw:.1f} (architecture.md: 6), SSB = {ssb:.1f} (architecture.md: 24), "
          f"F = {f_stat:.4f} (architecture.md: 12)")
    print(f"  11_02 R11 f.sf(12, 2, 6) = {f_sf:.4f} (architecture.md: 0.008), "
          f"f.ppf(0.90, 2, 6) = {f_ppf:.4f} (architecture.md: 3.46)")
    return str(save(fig, "11_02_anova_cartoon"))


def _ks_one_sample() -> str:
    """Slides 14, 17-20 (image33, image39-42): empirical CDF of the 100
    values vs N(0,1), replacing the slide's repeated image33 with one
    figure. Marks both gaps (R15): 0.092 at the 88th sorted value (slide's
    own i/n - F(x) only, above the step) and 0.096 at the 27th (F(x) minus
    the step just below it, the true two-sided KS gap).
    """
    data_sorted = np.sort(KS_DATA)
    n = len(data_sorted)
    i = np.arange(1, n + 1)
    f_obs_at = i / n  # step height AT each sorted value (right-continuous)
    f_exp = stats.norm.cdf(data_sorted)

    above_gap = f_obs_at - f_exp  # slide's own one-sided calculation
    below_gap = f_exp - (i - 1) / n  # step just below each value
    i_above = int(np.argmax(above_gap)) + 1  # 1-indexed row, expect 88
    i_below = int(np.argmax(below_gap)) + 1  # expect 27

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.step(data_sorted, f_obs_at, where="post", color=ACCENT, lw=1.8, label="observed ECDF")
    x = np.linspace(data_sorted[0] - 0.3, data_sorted[-1] + 0.3, 400)
    ax.plot(x, stats.norm.cdf(x), color=INK, lw=2, label=r"expected $\Phi(x)$")

    x88 = data_sorted[i_above - 1]
    ax.plot([x88, x88], [f_exp[i_above - 1], f_obs_at[i_above - 1]], color=WARN, lw=2, zorder=4)
    ax.annotate(f"88th: gap {above_gap[i_above - 1]:.3f}\n(above step, slide's calc)",
                (x88, f_obs_at[i_above - 1]), textcoords="offset points",
                xytext=(8, 14), fontsize=9, color=INK)

    x27 = data_sorted[i_below - 1]
    ax.plot([x27, x27], [(i_below - 1) / n, f_exp[i_below - 1]], color=SECOND, lw=2, zorder=4)
    ax.annotate(f"27th: gap {below_gap[i_below - 1]:.3f}\n(below step, true D)",
                (x27, f_exp[i_below - 1]), textcoords="offset points",
                xytext=(-95, 10), fontsize=9, color=INK)

    ax.set_xlabel("x")
    ax.set_ylabel("cumulative probability")
    ax.set_title("100 observations vs N(0,1): both KS gaps (slides 14, 17-20)", fontsize=12)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()

    d_stat, p_val = stats.kstest(KS_DATA, "norm")
    print(f"  11_03 one-sided-only max = {above_gap.max():.4f} at row {i_above} "
          "(architecture.md: 0.092, row 88)")
    print(f"  11_03 below-step max (true D contributor) = {below_gap.max():.4f} at row {i_below} "
          "(architecture.md: 0.096, row 27)")
    print(f"  11_03 R15 kstest(data, 'norm') D = {d_stat:.4f} (architecture.md: approx 0.096), "
          f"p = {p_val:.4f}")
    return str(save(fig, "11_03_ks_one_sample"))


def _ks_two_sample() -> str:
    """Slides 21, 22 (image43, image44): X (n=10, 1/10 steps) vs Y (n=8,
    1/8 steps), D = 0.6 at x = 4.8 (R13, R16).

    Shows the exact-vs-asymptotic verdict flip (architecture.md SS7.y decision
    record): D = 0.6 is below the Kolmogorov asymptotic critical value 0.645
    (fail to reject, p = 0.0815) but the exact p = 0.0499 rejects at 0.05.
    """
    x_sorted = np.sort(KS_X)
    y_sorted = np.sort(KS_Y)
    fx = np.arange(1, len(x_sorted) + 1) / len(x_sorted)
    fy = np.arange(1, len(y_sorted) + 1) / len(y_sorted)

    # prepend a zero shelf at the left edge so F_x=0 / F_y=0 before the first
    # observation actually renders (needed to see the D=0.6 gap at x=4.8)
    x0 = 0.0
    x_plot = np.concatenate([[x0], x_sorted])
    fx_plot = np.concatenate([[0.0], fx])
    y_plot = np.concatenate([[x0], y_sorted])
    fy_plot = np.concatenate([[0.0], fy])

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.step(x_plot, fx_plot, where="post", color=ACCENT, lw=2, label=f"X ECDF (n={len(x_sorted)})")
    ax.step(y_plot, fy_plot, where="post", color=SECOND, lw=2, label=f"Y ECDF (n={len(y_sorted)})")
    ax.set_xlim(0, x_sorted[-1] + 1)

    d_stat = 0.6
    x_at_d = 4.8  # architecture.md R13: gap at 4.8 is F_x=0.6, F_y=0.0
    n_x, n_y = len(x_sorted), len(y_sorted)
    d_crit = 1.36 * np.sqrt((n_x + n_y) / (n_x * n_y))  # Kolmogorov asymptotic, alpha=0.05
    p_asymp_kolmogorov = kstwobign.sf(d_stat * np.sqrt(n_x * n_y / (n_x + n_y)))
    ax.plot([x_at_d, x_at_d], [0.0, d_stat], color=WARN, lw=2.5, zorder=4)
    ax.annotate(
        f"D = {d_stat} at x = {x_at_d}\n"
        f"critical (asymp, 0.05) = {d_crit:.3f}: fail to reject, p = {p_asymp_kolmogorov:.4f}\n"
        f"exact p = 0.0499: reject",
        # Text sits in the empty lower-right region so it never crosses either ECDF.
        (x_at_d, 0.3), textcoords="data", xytext=(11.5, 0.3), fontsize=9, color=INK,
        arrowprops={"arrowstyle": "->", "color": INK, "lw": 0.8})
    ax.set_xlabel("x")
    ax.set_ylabel("cumulative probability")
    ax.set_title("Two-sample KS: X vs Y (slides 21, 22)", fontsize=12)
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()

    d_exact, p_exact = stats.ks_2samp(KS_X, KS_Y, method="exact")
    d_asymp, p_asymp = stats.ks_2samp(KS_X, KS_Y, method="asymp")
    hand_count = 2182 / 43758  # architecture.md R16 hand-counted path count
    print(f"  11_04 R16 ks_2samp(X, Y, method='exact') D = {d_exact:.5f} (architecture.md: 0.6), "
          f"p = {p_exact:.6f} (architecture.md hand count 2182/43758 = {hand_count:.5f})")
    print(f"  11_04 Kolmogorov asymptotic: critical = {d_crit:.4f} (1.36*sqrt(18/80)), "
          f"p = kstwobign.sf(0.6*sqrt(80/18)) = {p_asymp_kolmogorov:.4f}")
    print(f"  11_04 R16 ks_2samp(X, Y, method='asymp') D = {d_asymp:.5f}, "
          f"p = {p_asymp:.6f} (a different approximation: scipy's kstwo with n_eff rounded to 4)")
    verdict_exact = "reject" if p_exact < 0.05 else "fail to reject"
    verdict_asymp = "reject" if p_asymp_kolmogorov < 0.05 else "fail to reject"
    print(f"  11_04 verdict flip at alpha=0.05: asymptotic (Kolmogorov) = {verdict_asymp} "
          f"(p = {p_asymp_kolmogorov:.4f}), exact = {verdict_exact} (p = {p_exact:.6f})")
    return str(save(fig, "11_04_ks_two_sample"))


def build_all() -> list[str]:
    """Render every deck-11 figure; returns saved paths. Also prints the
    scipy confirmations T22 lists, including the transcription check and R5,
    R6, R17.
    """
    mismatches = _check_ks_transcription()
    paths = [_t_vs_normal(), _anova_cartoon(), _ks_one_sample(), _ks_two_sample()]

    # R5, R6 slide 8 (= deck 10 slide 25): tomato field means/sds/ns
    mean_a, sd_a, n_a = 1.3, 0.5, 22
    mean_b, sd_b, n_b = 1.6, 0.3, 24
    se_diff = np.sqrt(sd_a ** 2 / n_a + sd_b ** 2 / n_b)
    t_stat = (mean_a - mean_b) / se_diff
    p_df21 = 2 * stats.t.sf(abs(t_stat), df=21)
    welch = stats.ttest_ind_from_stats(mean_a, sd_a, n_a, mean_b, sd_b, n_b, equal_var=False)
    # Welch-Satterthwaite df (scipy's Ttest_indResult carries no df field)
    va, vb = sd_a ** 2 / n_a, sd_b ** 2 / n_b
    welch_df = (va + vb) ** 2 / (va ** 2 / (n_a - 1) + vb ** 2 / (n_b - 1))
    print(f"  R5 t = ({mean_a}-{mean_b})/{se_diff:.5f} = {t_stat:.4f} (architecture.md: -2.440)")
    print(f"  R6 2*t.sf(|t|, 21) = {p_df21:.4f} (architecture.md: approx 0.024)")
    print(f"  R6 ttest_ind_from_stats(..., equal_var=False) p = {welch.pvalue:.4f} "
          f"(architecture.md: approx 0.020), Welch df = {welch_df:.2f} (architecture.md: approx 33.8)")

    # R17 (book's own): ex:ht-distance groups C, D from deck9, closed via ANOVA/t/F
    c = np.array([20.0, 28.0, 34.0])
    d = np.array([22.0, 26.0, 37.0])
    ssw_cd = float(((c - c.mean()) ** 2).sum() + ((d - d.mean()) ** 2).sum())
    ssb_cd = float(len(c) * (c.mean() - np.concatenate([c, d]).mean()) ** 2
                    + len(d) * (d.mean() - np.concatenate([c, d]).mean()) ** 2)
    f_cd = (ssb_cd / 1) / (ssw_cd / 4)
    se_cd = np.sqrt((ssw_cd / 4) * (1 / 3 + 1 / 3))
    t_cd = (d.mean() - c.mean()) / se_cd
    p_cd = 2 * stats.t.sf(abs(t_cd), df=4)
    print(f"  R17 SSB={ssb_cd:.2f} (architecture.md: 1.50), SSW={ssw_cd:.2f} (architecture.md: 219.33), "
          f"F={f_cd:.4f} (architecture.md: 0.0274)")
    print(f"  R17 SE={se_cd:.3f} (architecture.md: 6.046), t={t_cd:.4f} (architecture.md: 0.165), "
          f"p={p_cd:.4f} (architecture.md: approx 0.88), t^2={t_cd ** 2:.4f} vs F={f_cd:.4f}")

    if mismatches:
        print(f"  WARNING: transcription mismatch count = {mismatches} (expected 0)")

    return paths


if __name__ == "__main__":
    from style import apply_style

    apply_style()
    print("Deck 11 - Comparing Distributions")
    build_all()
