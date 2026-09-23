"""Deck 9 (Hypothesis Testing) -> figures on values transcribed from slides.md
(notes_text/9_Hypothesis_Testing/) and recomputed per architecture.md SS3.4-3.6.

Every value lives once here, with its slide source noted in a comment; this
script only plots and does exact arithmetic, it never fits or trains anything.
"""

from math import comb

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from style import ACCENT, INK, MUTED, SECOND, save

__all__ = ["build_all"]

WARN = "#c0392b"  # rejection-region color (k >= 13 bars, boundary lines)


def _drug_experiments() -> str:
    """Slides 3, 4, 7: a preliminary experiment gives the hypothesis "A needs
    15 fewer hours than B" (slide 3, image11); the follow-up experiment
    contradicts it by swinging 35h in the OPPOSITE direction, i.e. A becomes
    slower (slide 4, image12; confirmed across 9 repeats in image15) -> the
    large, contradicting follow-up lets us confidently reject the hypothesis.
    Right panel: slide 7 (E/F), where the two follow-ups are tiny and flip
    direction relative to each other (image20: F above E by 0.25h; image21: E
    above F by 0.5h) -> not enough evidence to reject H0. The slide axes carry
    no tick marks (R13, architecture.md SS3.4); the hour values here are the
    book's own schematic numbers chosen only to reproduce the labeled gaps.
    """
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(11.0, 4.6))

    # Drug A/B: slide 3 (image11) A=15 faster than B by 15h (the hypothesis);
    # slide 4 (image12, image15) follow-up flips direction, A now 35h SLOWER
    exp_a = [("Experiment 1\n(slide 3)", 15.0, 30.0), ("Experiment 2\n(slide 4)", 50.0, 15.0)]
    for i, (label, a_val, b_val) in enumerate(exp_a):
        ax_l.plot([i, i], [a_val, b_val], color=MUTED, lw=1.5, zorder=1)
        ax_l.scatter([i], [a_val], color=ACCENT, s=90, zorder=2, label="Drug A" if i == 0 else None)
        ax_l.scatter([i], [b_val], color=SECOND, s=90, zorder=2, label="Drug B" if i == 0 else None)
        gap = abs(b_val - a_val)
        ax_l.annotate(f"{gap:.0f}h", (i, (a_val + b_val) / 2), textcoords="offset points",
                      xytext=(14, 0), fontsize=10, color=INK)
    ax_l.set_xticks([0, 1])
    ax_l.set_xticklabels([e[0] for e in exp_a])
    ax_l.set_xlim(-0.5, 1.5)
    ax_l.set_ylabel("recovery time (hours, schematic)")
    ax_l.set_title("Follow-up contradicts the 15h hypothesis -> reject it", fontsize=11)
    ax_l.legend(loc="upper left", fontsize=9)

    # Drug E/F: slide 7 (image20, image21), direction flips between repeats
    exp_ef = [("Experiment 1", 20.25, 20.0), ("Experiment 2", 20.0, 20.5)]
    for i, (label, f_val, e_val) in enumerate(exp_ef):
        ax_r.plot([i, i], [min(e_val, f_val), max(e_val, f_val)], color=MUTED, lw=1.5, zorder=1)
        ax_r.scatter([i], [e_val], color=ACCENT, s=90, zorder=2, label="Drug E" if i == 0 else None)
        ax_r.scatter([i], [f_val], color=SECOND, s=90, zorder=2, label="Drug F" if i == 0 else None)
        gap = abs(f_val - e_val)
        ax_r.annotate(f"{gap:.2f}h", (i, (e_val + f_val) / 2), textcoords="offset points",
                      xytext=(14, 0), fontsize=10, color=INK)
    ax_r.set_xticks([0, 1])
    ax_r.set_xticklabels([e[0] for e in exp_ef])
    ax_r.set_xlim(-0.5, 1.5)
    ax_r.set_title("Follow-ups not far enough -> fail to reject $H_0$", fontsize=11)
    ax_r.legend(loc="upper left", fontsize=9)

    fig.suptitle("Repeated experiments: does the follow-up support the hypothesis? (slides 3-4, 7)",
                 fontsize=13, fontweight="bold", color=INK, y=1.03)
    fig.tight_layout()
    return str(save(fig, "09_01_drug_experiments"))


def _pooled_vs_group() -> str:
    """Slide 9 (image22/23 shape); the numbers are the book's own worked
    example (architecture.md SS3.5 ex:ht-distance), not read off the slide.
    """
    c = np.array([20.0, 28.0, 34.0])  # architecture.md SS3.5 ex:ht-distance, group C
    d = np.array([22.0, 26.0, 37.0])  # architecture.md SS3.5 ex:ht-distance, group D
    pooled = np.concatenate([c, d])
    pooled_mean = pooled.mean()
    c_mean, d_mean = c.mean(), d.mean()
    pooled_ss = float(((pooled - pooled_mean) ** 2).sum())
    group_ss = float(((c - c_mean) ** 2).sum() + ((d - d_mean) ** 2).sum())

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(11.0, 4.6), sharey=True)
    x_c, x_d = np.array([0, 1, 2]), np.array([3, 4, 5])

    ax_l.scatter(x_c, c, color=ACCENT, s=90, zorder=3, label="Drug C")
    ax_l.scatter(x_d, d, color=SECOND, s=90, zorder=3, label="Drug D")
    for x, y in zip(np.concatenate([x_c, x_d]), pooled):
        ax_l.plot([x, x], [pooled_mean, y], color=MUTED, lw=1.2, zorder=2)
    ax_l.axhline(pooled_mean, color=INK, lw=2, label=f"pooled mean = {pooled_mean:.2f}")
    ax_l.set_title(f"Pooled mean ($H_0$)\nsum sq. distance = {pooled_ss:.2f}", fontsize=11)
    ax_l.set_xticks([])
    ax_l.legend(loc="upper left", fontsize=9)
    ax_l.set_ylabel("recovery time (hours)")

    ax_r.scatter(x_c, c, color=ACCENT, s=90, zorder=3, label="Drug C")
    ax_r.scatter(x_d, d, color=SECOND, s=90, zorder=3, label="Drug D")
    for x, y in zip(x_c, c):
        ax_r.plot([x, x], [c_mean, y], color=MUTED, lw=1.2, zorder=2)
    for x, y in zip(x_d, d):
        ax_r.plot([x, x], [d_mean, y], color=MUTED, lw=1.2, zorder=2)
    ax_r.hlines(c_mean, x_c[0] - 0.4, x_c[-1] + 0.4, color=ACCENT, lw=2)
    ax_r.hlines(d_mean, x_d[0] - 0.4, x_d[-1] + 0.4, color=SECOND, lw=2)
    ax_r.set_title(f"Group means ($H_a$)\nsum sq. distance = {group_ss:.2f}", fontsize=11)
    ax_r.set_xticks([])
    ax_r.legend(loc="upper left", fontsize=9)

    reduction = pooled_ss - group_ss
    fig.suptitle(
        f"Distance from mean: pooled vs group (slide 9, book's example values)\n"
        f"reduction = {reduction:.2f} ({reduction / pooled_ss:.1%})",
        fontsize=12, fontweight="bold", color=INK, y=1.02,
    )
    fig.tight_layout()
    print(f"  09_02 pooled sum sq = {pooled_ss:.2f}, group sum sq = {group_ss:.2f}, "
          f"reduction = {reduction:.2f}")
    return str(save(fig, "09_02_pooled_vs_group"))


def _puppy_null() -> str:
    """Slide 11 table (media/image28.png); frequencies are the slide's own
    "1000 simulations" table. architecture.md R4 shows each row equals the
    rounded exact binomial expectation, not an actual simulation draw -- the
    overlaid exact points make that visible.
    """
    freq = [0, 0, 3, 14, 42, 92, 153, 196, 196, 153, 92, 42, 14, 3, 0, 0]  # slide 11, image28
    k = np.arange(16)
    exact = np.array([1000 * comb(15, kk) / 2 ** 15 for kk in k])
    colors = [WARN if kk >= 13 else ACCENT for kk in k]

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.bar(k, freq, color=colors, edgecolor="white", linewidth=0.8, label="slide's simulation table")
    ax.plot(k, exact, "o", color=INK, ms=5, zorder=3, label=r"exact $1000\binom{15}{k}/2^{15}$")
    ax.axvline(13, color=MUTED, lw=1.5, ls="--")
    ax.annotate("observed = 13", (13, max(freq) * 0.9), textcoords="offset points",
                xytext=(6, 0), fontsize=9, color=INK)
    ax.set_xlabel("number of male puppies out of 15")
    ax.set_ylabel("frequency (out of 1000)")
    ax.set_xticks(k)
    ax.set_title(r"$H_0$: $p=0.5$, null distribution of male puppies (slide 11)", fontsize=12)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()

    p_sim = sum(freq[13:]) / 1000
    p_exact = sum(comb(15, kk) for kk in range(13, 16)) / 2 ** 15
    print(f"  09_03 P(X>=13) from table = {p_sim:.3f}, exact = {p_exact:.5f} (121/32768, slide 11)")
    return str(save(fig, "09_03_puppy_null"))


def _alien_null() -> str:
    """Optional (architecture.md SS3.6, marked "선택"). Slide 12 table
    (media/image29.png), percent bins; architecture.md R7 flags the %-bin
    boundary ambiguity, shown here on the person-count axis (1% = 4 of 400).
    """
    pct = np.arange(6, 15)
    freq = np.array([7, 40, 93, 173, 327, 253, 73, 27, 7])  # slide 12, image29
    people = pct * 4  # 400 * pct / 100

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.bar(people, freq, width=3.2, color=ACCENT, edgecolor="white", linewidth=0.8,
           label="slide's simulation table (by % bin)")

    x = np.arange(20, 65)
    pmf = stats.binom.pmf(x, 400, 0.1) * 1000 * 4  # scale to 1000 sims x 4-person bin width
    ax.plot(x, pmf, color=INK, lw=2, label=r"$1000 \times 4 \times \mathrm{Bin}(400, 0.1)$ pmf")

    ax.axvline(54, color=WARN, lw=1.5, ls="--")
    ax.annotate("13.5% = 54", (54, max(freq) * 0.55), textcoords="offset points",
                xytext=(-72, 0), fontsize=9, color=INK)
    ax.axvline(56, color=MUTED, lw=1.5, ls="--")
    ax.annotate("14% = 56", (56, max(freq) * 0.55), textcoords="offset points",
                xytext=(6, 0), fontsize=9, color=INK)
    ax.set_xlabel("number of rebellious people out of 400")
    ax.set_ylabel("frequency (out of 1000)")
    ax.set_title("$H_0$: p=0.10, boundary at 13.5% vs 14% flips the verdict (slide 12)", fontsize=12)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    return str(save(fig, "09_04_alien_null"))


def build_all() -> list[str]:
    """Render every deck-9 figure; returns saved paths."""
    paths = [_drug_experiments(), _pooled_vs_group(), _puppy_null(), _alien_null()]
    sf = stats.binom.sf(55, 400, 0.1)  # R6: confirm exact P(X>=56) vs slide's table value 0.007
    print(f"  R6 exact scipy.stats.binom.sf(55, 400, 0.1) = {sf:.5f}")
    return paths


if __name__ == "__main__":
    from style import apply_style

    apply_style()
    print("Deck 9 - Hypothesis Testing")
    build_all()
