"""Deck 10 (P-value) -> figures on values transcribed from slides.md
(notes_text/10_P-value/) and recomputed per architecture.md SS7.3.4/7.3.6.

Every value lives once here, with its slide source noted in a comment; this
script only plots and does exact arithmetic or fixed-seed random draws, it
never fits or trains anything.
"""

from math import comb

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from style import ACCENT, INK, MUTED, SECOND, save

__all__ = ["build_all"]

WARN = "#c0392b"  # rejection-region / more-extreme color
SEED = 10  # fixed seed, deck number, for every RNG draw in this module
Z_99 = 2.576  # 99% two-sided normal critical value, used for both CIs below

# Vitamin D example (slides 15-20): null mean 100, SE 3.3 (slide 18, image41).
VITD_NULL_MEAN = 100.0  # slide 15-18 null hypothesis average
VITD_SE = 3.3  # slide 18 (image41) standard error
# architecture.md decision record (2026-09-23, T19r I3): unify on observed 63
# (slides 17, 18) everywhere; slide 15's own 62 is a book-text-only footnote.
VITD_OBS = 63.0
VITD_CI95_LO, VITD_CI95_HI = VITD_OBS - 2 * VITD_SE, VITD_OBS + 2 * VITD_SE  # slide 15 rule, R13


def _coin_pvalue() -> str:
    """Slides 9, 10, 12: coin flipped twice (probabilities 0.25/0.5/0.25) and
    five times (observed 4 heads; 12/32 = 0.375, architecture.md R7, R8).
    """
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(11.0, 4.6))

    k2 = np.arange(3)
    p2 = np.array([0.25, 0.5, 0.25])  # slides 9, 10: 0/1/2 heads out of 2 flips
    # colour mapping matches the right panel: observed = SECOND, equally rare =
    # ACCENT, not part of the p-value = MUTED with no label (I1, T19r)
    ax_l.bar([k2[1]], [p2[1]], color=MUTED, edgecolor="white", linewidth=0.8)
    ax_l.bar([k2[0]], [p2[0]], color=ACCENT, edgecolor="white", linewidth=0.8,
             label="equally rare (0 heads)")
    ax_l.bar([k2[2]], [p2[2]], color=SECOND, edgecolor="white", linewidth=0.8,
             label="observed (2 heads)")
    ax_l.set_xticks(k2)
    ax_l.set_xlabel("heads out of 2 flips")
    ax_l.set_ylabel("probability")
    ax_l.set_title("Two flips (slides 9, 10)", fontsize=11)
    ax_l.set_ylim(0, 0.62)  # headroom so the legend clears the 0.5 bar (I1)
    ax_l.legend(loc="upper left", fontsize=9)

    k5 = np.arange(6)
    counts = np.array([comb(5, kk) for kk in k5])  # slide 12: 1,5,10,10,5,1
    ax_r.bar([k5[4]], [counts[4]], color=SECOND, edgecolor="white", linewidth=0.8, label="observed")
    ax_r.bar([k5[1]], [counts[1]], color=ACCENT, edgecolor="white", linewidth=0.8,
             label="equally rare")
    ax_r.bar([k5[0], k5[5]], [counts[0], counts[5]], color=WARN, edgecolor="white", linewidth=0.8,
             label="more extreme")
    ax_r.bar([k5[2], k5[3]], [counts[2], counts[3]], color=MUTED, edgecolor="white", linewidth=0.8)
    ax_r.set_xticks(k5)
    ax_r.set_xlabel("heads out of 5 flips")
    ax_r.legend(loc="upper left", fontsize=9)
    ax_r.set_ylabel("count out of 32 outcomes")
    tail = sum(comb(5, kk) for kk in (0, 1, 4, 5))
    p_two_sided = tail / 32
    ax_r.set_title(f"Five flips, observed 4 (slide 12): {tail}/32 = {p_two_sided:.3f}",
                    fontsize=11)

    fig.suptitle("Coin-flip p-value: observed vs equally rare vs more extreme",
                 fontsize=13, fontweight="bold", color=INK, y=1.03)
    fig.tight_layout()
    print(f"  10_01 two-sided p (5 flips, observed 4) = {tail}/32 = {p_two_sided:.4f}")
    return str(save(fig, "10_01_coin_pvalue"))


def _height_pvalue() -> str:
    """Slides 13, 14: Brazilian women's height, N(155.7, 6.89^2) (sigma is
    the book's own derivation from the 95% interval [142, 169], R9). Left:
    two-tailed p for 142 cm (slide claims 0.025 + 0.025 = 0.05, R11). Right:
    band [155.4, 156] and the two remaining tails (slide: 0.04 + 0.48 + 0.48
    = 1, R12).
    """
    mu, sigma = 155.7, 6.89  # architecture.md R9: sigma derived, not on slide
    dist = stats.norm(mu, sigma)
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(11.0, 4.6))

    x = np.linspace(mu - 4.5 * sigma, mu + 4.5 * sigma, 500)
    ax_l.plot(x, dist.pdf(x), color=INK, lw=2)
    lo_x = np.linspace(x[0], 142, 100)
    hi_x = np.linspace(169, x[-1], 100)
    ax_l.fill_between(lo_x, dist.pdf(lo_x), color=WARN, alpha=0.6)
    ax_l.fill_between(hi_x, dist.pdf(hi_x), color=WARN, alpha=0.6)
    p_lo = dist.cdf(142)
    p_hi = dist.sf(169)
    ax_l.axvline(142, color=MUTED, ls="--", lw=1.2)
    ax_l.axvline(169, color=MUTED, ls="--", lw=1.2)
    ax_l.annotate(f"P(h<142)={p_lo:.4f}", (142, dist.pdf(142)), textcoords="offset points",
                  xytext=(-95, 30), fontsize=9, color=INK)
    ax_l.annotate(f"P(h>169)={p_hi:.4f}", (169, dist.pdf(169)), textcoords="offset points",
                  xytext=(6, 30), fontsize=9, color=INK)
    ax_l.set_xlabel("height (cm)")
    ax_l.set_ylabel("density")
    ax_l.set_title(
        f"142/169 cm tails (slide: 0.025 each)\ntwo-sided p = {p_lo + p_hi:.4f} (slide: 0.05)",
        fontsize=10)

    ax_r.plot(x, dist.pdf(x), color=INK, lw=2)
    band_x = np.linspace(155.4, 156, 50)
    ax_r.fill_between(band_x, dist.pdf(band_x), color=ACCENT, alpha=0.7)
    left_x = np.linspace(x[0], 155.4, 100)
    right_x = np.linspace(156, x[-1], 100)
    ax_r.fill_between(left_x, dist.pdf(left_x), color=SECOND, alpha=0.5)
    ax_r.fill_between(right_x, dist.pdf(right_x), color=SECOND, alpha=0.5)
    p_band = dist.cdf(156) - dist.cdf(155.4)
    p_below = dist.cdf(155.4)
    p_above = dist.sf(156)
    ax_r.set_xlabel("height (cm)")
    ax_r.set_title(f"[155.4, 156] band (slide: 0.04 + 0.48 + 0.48 = 1)\n"
                    f"band={p_band:.3f}, below={p_below:.3f}, above={p_above:.3f}", fontsize=10)

    fig.suptitle(r"Brazilian women's height, $N(155.7, 6.89^2)$ (slides 13, 14)",
                 fontsize=13, fontweight="bold", color=INK, y=1.04)
    fig.tight_layout()
    print(f"  10_02 142/169 tails: {p_lo:.4f}/{p_hi:.4f} (slide: 0.025 each), "
          f"two-sided p={p_lo + p_hi:.4f} (slide: 0.05)")
    print(f"  10_02 band [155.4,156]={p_band:.4f}, below={p_below:.4f}, above={p_above:.4f} "
          f"(slide: 0.04, 0.48, 0.48)")
    return str(save(fig, "10_02_height_pvalue"))


def _vitd_null() -> str:
    """Slides 17, 18: 10,000 simulated sample means under H0 (mean 100, SE
    3.3), observed value 63 (image39/41). Right panel is the sampling
    distribution of the sample mean around that same observed 63 (slide 15,
    image36, plots the sample mean, not the population mean). Per the
    architecture.md decision record (2026-09-23, T19r I3), the book unifies
    on 63 everywhere; slide 15's own 62 is a footnote in the book text only,
    not shown here.
    """
    rng = np.random.default_rng(SEED)
    draws = rng.normal(VITD_NULL_MEAN, VITD_SE, size=10_000)
    n_below_63 = int((draws < VITD_OBS).sum())

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(11.0, 4.6))
    ax_l.hist(draws, bins=40, color=MUTED, edgecolor="white", linewidth=0.5)
    ax_l.axvline(VITD_OBS, color=WARN, lw=2, ls="--")
    ax_l.set_xlim(min(draws.min(), VITD_OBS - 2), draws.max())
    ax_l.annotate(f"observed = 63\n{n_below_63} of 10,000 below", (VITD_OBS, 20),
                  textcoords="offset points", xytext=(8, 0), fontsize=9, color=INK)
    ax_l.set_xlabel("simulated sample mean")
    ax_l.set_ylabel("frequency (of 10,000)")
    ax_l.set_title(r"$H_0$ null distribution, $N(100, 3.3^2)$ (slides 17, 18)", fontsize=10)

    x = np.linspace(VITD_OBS - 4.2 * VITD_SE, VITD_OBS + 4.2 * VITD_SE, 500)
    dist_obs = stats.norm(VITD_OBS, VITD_SE)
    ax_r.plot(x, dist_obs.pdf(x), color=INK, lw=2)
    band_x = np.linspace(VITD_CI95_LO, VITD_CI95_HI, 100)
    ax_r.fill_between(band_x, dist_obs.pdf(band_x), color=ACCENT, alpha=0.6)
    ax_r.axvline(VITD_NULL_MEAN, color=WARN, lw=2, ls="--")
    ax_r.annotate("null = 100 (outside interval)", (VITD_NULL_MEAN, 0), textcoords="offset points",
                  xytext=(-90, 10), fontsize=9, color=INK)
    ax_r.set_xlabel("sample mean (centered on observed 63)")
    ax_r.set_title(
        f"95% CI [{VITD_CI95_LO}, {VITD_CI95_HI}] around observed 63 "
        "(slide 15 rule, recomputed on 63)", fontsize=10)

    fig.suptitle("Vitamin D: null distribution vs observed sample mean (slides 15-18)",
                 fontsize=13, fontweight="bold", color=INK, y=1.04)
    fig.tight_layout()

    z = (VITD_OBS - VITD_NULL_MEAN) / VITD_SE  # architecture.md R16: -37/3.3 = -11.21
    p_two_sided = 2 * stats.norm.cdf(z)
    print(f"  10_03 simulation: {n_below_63} of 10,000 draws below observed 63 "
          "(slide: 0 of 10,000)")
    print(f"  10_03 R16 z = (63-100)/3.3 = {z:.4f} (slide text omits sign; |z|=11.2), "
          f"two-sided p = {p_two_sided:.3e}")
    print("  10_03 note: slide 15 (image36) prints observed 62; the book unifies on 63 "
          "(architecture.md decision record, T19r I3), 62 is a footnote in text only")
    return str(save(fig, "10_03_vitd_null"))


def _ci_vs_test() -> str:
    """Slide 19 (image42/43): vitamin D 95%/99% confidence intervals against
    the null value 100. Slide 20 (image44): Bosc vs Anjou pear calories, 99%
    interval on the difference against the null value 0.
    """
    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(8.4, 7.2))

    ci99_lo, ci99_hi = VITD_OBS - Z_99 * VITD_SE, VITD_OBS + Z_99 * VITD_SE  # R17
    ax_top.plot([VITD_CI95_LO, VITD_CI95_HI], [1, 1], color=ACCENT, lw=6, solid_capstyle="butt")
    ax_top.plot([ci99_lo, ci99_hi], [0, 0], color=SECOND, lw=6, solid_capstyle="butt")
    ax_top.scatter([VITD_NULL_MEAN], [0.5], color=WARN, s=80, zorder=3, marker="x")
    ax_top.annotate("null = 100", (VITD_NULL_MEAN, 0.5), textcoords="offset points",
                     xytext=(8, 0), fontsize=9, color=INK)
    ax_top.set_yticks([0, 1])
    ax_top.set_yticklabels([
        f"99% [{ci99_lo:.1f}, {ci99_hi:.1f}]",
        f"95% [{VITD_CI95_LO:.1f}, {VITD_CI95_HI:.1f}]",
    ])
    ax_top.set_ylim(-0.6, 1.6)
    ax_top.set_xlabel("vitamin D level")
    ax_top.set_title("Vitamin D: interval excludes null 100 (slide 19)", fontsize=11)

    bosc_mean, bosc_sd, n = 120.0, 15.0, 65  # slide 20 (image44)
    anjou_mean, anjou_sd = 116.0, 13.0
    se_bosc = bosc_sd / np.sqrt(n)
    se_anjou = anjou_sd / np.sqrt(n)
    se_diff = np.sqrt(se_bosc ** 2 + se_anjou ** 2)  # architecture.md R18: 2.462
    diff = bosc_mean - anjou_mean  # 4
    margin = 6.44  # architecture.md R18 / T19 AC (slide's own 99% margin)
    ci_lo, ci_hi = diff - margin, diff + margin  # [-2.44, 10.44]
    ax_bot.plot([ci_lo, ci_hi], [0, 0], color=ACCENT, lw=6, solid_capstyle="butt")
    ax_bot.scatter([0.0], [0], color=WARN, s=80, zorder=3, marker="x")
    ax_bot.annotate("null = 0", (0.0, 0), textcoords="offset points",
                     xytext=(8, -18), fontsize=9, color=INK)
    ax_bot.set_yticks([0])
    ax_bot.set_yticklabels([f"99% diff [{ci_lo:.2f}, {ci_hi:.2f}]"])
    ax_bot.set_ylim(-0.6, 0.6)
    ax_bot.set_xlabel("calorie difference (Bosc - Anjou)")
    ax_bot.set_title("Pears: interval includes null 0, fail to reject (slide 20)", fontsize=11)

    fig.suptitle("Confidence interval vs hypothesis test (slides 19, 20)",
                 fontsize=13, fontweight="bold", color=INK, y=1.01)
    fig.tight_layout()

    t_ratio = margin / se_diff  # architecture.md R18: 6.44/2.462
    t_crit = stats.t.ppf(0.995, df=2 * n - 2)
    z_margin = Z_99 * se_diff
    print(f"  10_04 SE_diff = sqrt({se_bosc:.3f}^2 + {se_anjou:.3f}^2) = {se_diff:.4f} "
          "(slide: 2.462)")
    print(f"  10_04 R18 margin/SE_diff = {margin}/{se_diff:.4f} = {t_ratio:.4f} "
          f"vs t.ppf(0.995, df={2 * n - 2}) = {t_crit:.4f}")
    print(f"  10_04 z-based 99% margin = {Z_99} * {se_diff:.4f} = {z_margin:.4f} "
          "(slide: 6.44 uses t)")
    return str(save(fig, "10_04_ci_vs_test"))


def _false_positive() -> str:
    """Slide 5, 6: "Drug A" tested against itself in two independent 198-
    patient trials (both true cure rate 36.9%, R1). Simulated 1,000 times to
    show the false-positive rate near 5% at alpha=0.05 (slide 6 text, no
    slide numbers to transcribe).
    """
    rng = np.random.default_rng(SEED)
    n_trials = 1000
    n_per_arm = 198  # slide 4 (image9): 73 + 125 = 198 patients
    true_rate = 0.369  # architecture.md R1: 73/198 = 0.3687 -> 36.9%

    pvals = np.empty(n_trials)
    for i in range(n_trials):
        cured_a = rng.binomial(n_per_arm, true_rate)
        cured_b = rng.binomial(n_per_arm, true_rate)
        table = [[cured_a, n_per_arm - cured_a], [cured_b, n_per_arm - cured_b]]
        _, p, _, _ = stats.chi2_contingency(table, correction=False)
        pvals[i] = p

    share_below = float((pvals < 0.05).mean())

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    bins = np.arange(0, 1.05, 0.05)
    counts, _ = np.histogram(pvals, bins=bins)
    colors = [WARN if b < 0.05 else MUTED for b in bins[:-1]]
    ax.bar(bins[:-1], counts, width=0.05, align="edge", color=colors, edgecolor="white",
           linewidth=0.8)
    ax.axvline(0.05, color=INK, lw=1.5, ls="--")
    ax.annotate(f"p < 0.05: {share_below:.1%}", (0.05, ax.get_ylim()[1] * 0.85),
                textcoords="offset points", xytext=(8, 0), fontsize=10, color=INK)
    ax.set_xlabel("p-value (chi-square, uncorrected)")
    ax.set_ylabel("count out of 1,000 trials")
    ax.set_title("Drug A vs Drug A, 1,000 trials: false positives at true rate 36.9% (slides 5, 6)",
                  fontsize=11)
    fig.tight_layout()

    print(f"  10_05 share of simulated p < 0.05 = {share_below:.4f} "
          "(1000 trials, chi-square uncorrected)")
    return str(save(fig, "10_05_false_positive"))


def build_all() -> list[str]:
    """Render every deck-10 figure; returns saved paths. Also prints the
    scipy confirmations T19 lists for R3a-R6.
    """
    paths = [_coin_pvalue(), _height_pvalue(), _vitd_null(), _ci_vs_test(), _false_positive()]

    # R3a slide 4: [[73,125],[59,131]] -> slide says p = 0.24
    table_r3a = [[73, 125], [59, 131]]
    _, fisher_p = stats.fisher_exact(table_r3a)
    chi2_nc, p_nc, _, _ = stats.chi2_contingency(table_r3a, correction=False)
    chi2_y, p_y, _, _ = stats.chi2_contingency(table_r3a, correction=True)
    print(f"  R3a fisher_exact({table_r3a}) p = {fisher_p:.4f} (slide: 0.24)")
    print(f"  R3a chi2 uncorrected = {chi2_nc:.4f}, p = {p_nc:.4f} (architecture.md: 1.461/0.227)")
    print(f"  R3a chi2 Yates = {chi2_y:.4f}, p = {p_y:.4f} (architecture.md: 1.214/0.271)")

    # R4 slide 5: two pairs, Yates-corrected
    table_r4a = [[71, 127], [72, 126]]
    table_r4b = [[73, 125], [71, 127]]
    _, p_r4a, _, _ = stats.chi2_contingency(table_r4a, correction=True)
    _, p_r4b, _, _ = stats.chi2_contingency(table_r4b, correction=True)
    print(f"  R4 Yates p {table_r4a} = {p_r4a:.4f} (architecture.md: 1.0)")
    print(f"  R4 Yates p {table_r4b} = {p_r4b:.4f} (architecture.md: approx 0.917)")

    # R5 slide 5: [[60,138],[84,114]] -> slide p = 0.01
    table_r5 = [[60, 138], [84, 114]]
    chi2_r5_nc, p_r5_nc, _, _ = stats.chi2_contingency(table_r5, correction=False)
    chi2_r5_y, p_r5_y, _, _ = stats.chi2_contingency(table_r5, correction=True)
    print(f"  R5 chi2 uncorrected = {chi2_r5_nc:.4f}, p = {p_r5_nc:.4f} "
          "(architecture.md: 6.29/0.012)")
    print(f"  R5 chi2 Yates = {chi2_r5_y:.4f}, p = {p_r5_y:.4f} (architecture.md: 0.016)")

    # R6 slide 7: [[5005,9868],[4800,9000]] -> slide p = 0.04
    table_r6 = [[5005, 9868], [4800, 9000]]
    chi2_r6, p_r6, _, _ = stats.chi2_contingency(table_r6, correction=False)
    print(f"  R6 chi2 uncorrected = {chi2_r6:.4f} (z={np.sqrt(chi2_r6):.4f}), p = {p_r6:.4f} "
          f"(architecture.md: 4.07/2.02/0.044)")

    return paths


if __name__ == "__main__":
    from style import apply_style

    apply_style()
    print("Deck 10 - P-value")
    build_all()
