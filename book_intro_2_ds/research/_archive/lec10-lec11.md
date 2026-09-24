# Archived from PLAN.md §3.1a + §3.1b + §3.1c (2026-09-23): decks 10, 11 + Q8 links, all DONE

Closing notes (pm, 2026-09-23; all committed on main):

- T19/T19r: `reviews/T19.md`; cycle-2 fixes include architecture.md §7.x decision record
  (vitamin D observed mean unified on 63).
- T20/T21: `chapters/lec10-p-value.tex`; `reviews/lec10.md` PASS cycle 2. Minor note N1
  (table header) fixed in tree (header now "판정(재계산한 p값, p-value)"); N2 recorded by
  the reviewer as PASS with a note, no action.
- T22/T22r: `reviews/T22.md`; architecture.md §7.y decision record: two-sample KS
  asymptotic = Kolmogorov limit p 0.0815 (critical 0.645, D 0.6 → 기각 실패); exact
  p 0.0499 (< 0.05 → 기각). E7 verdict from the exact p.
- T23/T24: `chapters/lec11-comparing-distributions.tex`; `reviews/lec11.md` PASS cycle 2;
  remaining non-blocking items (I10, I11 partial, N1) fixed by the main session.
- T25: done by the main session directly (three one-line forward `\Cref` additions in
  lec09, 03, hw02; `git diff --numstat` 1/0 each; clean build exit 0, no undefined refs).
- T26: closed differently. Verified by the main session with the numstat + clean build
  check instead of a reviewer dispatch (trivial one-line edits); no `reviews/q8-links.md`.

### 3.1a Deck 10 → `chapters/lec10-p-value.tex` (`ch:pvalue`)

Spec: architecture.md §7.3 (fully specified; no A-task). Opens now (T04 PASS).

- [x] **T19** developer. `hw1/00_lecture_charts/deck10_pvalue.py` → `figures/10_01_coin_pvalue.png`,
  `10_02_height_pvalue.png`, `10_03_vitd_null.png`, `10_04_ci_vs_test.png`,
  `10_05_false_positive.png` (all five required; 10_05 promoted from "선택": cheap RNG,
  makes slide 6 visible). Register in `main.py` append-only (one import + one build
  call, no reformat). In: architecture.md §7.3.4, §7.3.6, `notes_text/10_*/slides.md`. Dep: none.
  AC: as T02 (seconds, exit 0, five PNGs exist, values once in the script with slide
  comments, fixed numpy seed, no training, no notebook). Figure content per §7.3.6
  (10_01 three colours + "12/32 = 0.375"; 10_03 line at 63; 10_04 intervals
  [55.4, 68.6], [53.5, 70.5], [−2.44, 10.44]). Prints and reports back: R3a
  `fisher_exact([[73,125],[59,131]])` p (slide 0.24); R4 Yates p of [[71,127],[72,126]]
  (1.0) and [[73,125],[71,127]] (≈0.917); R5 [[60,138],[84,114]] (≈0.012 / 0.016);
  R6 [[5005,9868],[4800,9000]] (≈0.044); R12 0.483 and band 0.035; R16 z = −11.21 and
  its two-sided p; R18 SE_diff 2.462 and 6.44/2.462; 10_05 share of p < 0.05.
- [x] **T19r** reviewer. Run T19 once; confirm the five PNGs and every printed value vs
  §7.3.4 (a mismatch is reported, not smoothed). Out: `reviews/T19.md`. Dep: T19.
- [x] **T20** sonnet-writer. Write the chapter + one `\input` line after
  `lec09-hypothesis-testing` in part1. In: architecture.md §7.3, T19r values,
  `notes_text/10_*/`. Out: `chapters/lec10-p-value.tex`, `parts/part1-foundations.tex`.
  Dep: T19r PASS. AC: AC-W1..W10 (W8's In brief = `inbrief` env, as lec09). Plus:
  - labels, each exactly once: `ch:pvalue`; `sec:pv-background`, `sec:pv-why`,
    `sec:pv-threshold`, `sec:pv-effect-size`, `sec:pv-discrete`, `sec:pv-continuous`,
    `sec:pv-sim-vs-param`, `sec:pv-ci-duality`, `sec:pv-apply`, `sec:pv-future`;
    `ex:pv-drug`, `ex:pv-coin5`, `ex:pv-height`, `ex:pv-vitd`, `ex:pv-pears`;
    `tab:pv-symbols`, `tab:pv-drug-trials`, `tab:pv-error-types`, `tab:pv-ci-vs-p`;
    `fig:pv-coin`, `fig:pv-height`, `fig:pv-vitd`, `fig:pv-ci-test`,
    `fig:pv-false-positive` (PNG), `fig:pv-three-parts` (TikZ).
  - p값 not redefined: `grep -c 'begin{definition}\[p값\]'` in lec10 = 0; `\Cref{def:pvalue}` ≥ 1.
  - numbers (AC-W6): 36.9%, 31%, 31.1%, 99.7%, 0.14%, 약 0.24 (T19r Fisher value),
    0.917 (pair named), 30.3%, 42.4%, 0.044, 1.1%포인트, 0.5, 12/32, 0.375, 0.1875,
    6.89, 0.05, 0.035, 0.483, 55.4, 68.6, 1.96, −11.21, 1/10,000, 53.5, 70.5,
    1.860, 1.612, 2.462, 6.44, −2.44, 10.44, 0.25 (확인 문제 $2/8$).
  - pitfalls (AC-W7, Q4/Q10 form; non-numeric rows as "슬라이드는 X, 바르게는 Y"):
    R2 (29% → 31.1%), R3 (0.001% → 0.14%), R10 (reversed $H_0$), R11 (p = 0.05 called
    유의 → boundary, 기각 실패), R14 (question $<$ vs $H_a \neq$, `\Cref{pit:ht-direction}`),
    R15 (62 vs 63; text uses 63), R16 (11.2 → −11.21), R19 (interval reading, "Apples",
    "the same"). Plus: "0.24 ≠ 24% 확률로 차이 없음"; effect size (34% vs 35%, p ≈ 0.044);
    세 부분 = 양측 (0.375 vs 0.1875); threshold arbitrary = one line + `\Cref{pit:ht-alpha}`, no new box.
  - σ = 6.89 stated as the book's derived value (text and `fig:pv-height` caption).
  - `grep -c 'ch:compare-dist'` in lec10 = 0 (label absent until T23); slides 22–25
    only as `% source:` + prose in `sec:pv-future`; slide 2 = one line + `\Cref{def:ht-null,def:ht-alt}`.
  - part1 diff = one added line.
- [x] **T21** reviewer. Out: `reviews/lec10.md`. Dep: T20.

### 3.1b Deck 11 → `chapters/lec11-comparing-distributions.tex` (`ch:compare-dist`)

Spec: architecture.md §7.4, with Q7/Q9/Q11 (§1) overriding it. Opens after T21 PASS
(lec11 `\Cref`s `sec:pv-*`).

- [x] **T22** developer. `hw1/00_lecture_charts/deck11_compare.py` → `figures/11_01_t_vs_normal.png`,
  `11_02_anova_cartoon.png`, `11_03_ks_one_sample.png`, `11_04_ks_two_sample.png`;
  register in `main.py` append-only. In: architecture.md §7.4.4, §7.4.6,
  `notes_text/11_*/` (slides.md, `media/image39.png`, `image40.png`, slide 21 table).
  Dep: T21 PASS. AC: as T02. Plus:
  - the 100 slide-17 values transcribed once from `image40` with a source comment;
    the sorted list is checked against `image39`, mismatch count reported (must be 0;
    if `image39` shows fewer than 100 rows, report which rows were checkable). $X$ (10)
    and $Y$ (8) of slide 21 transcribed once.
  - prints and reports back: R3 `t.cdf(-2.5, 24)` (≈0.0098); R4 `2*t.sf(2.75, 5)`
    (≈0.040); R5 t = −2.440; R6 `2*t.sf(2.44, 21)` (≈0.024) and
    `ttest_ind_from_stats(1.3,0.5,22,1.6,0.3,24,equal_var=False)` p (≈0.020) with Welch
    df (≈33.8); R11 `f.sf(12, 2, 6)` (0.008), `f.ppf(0.90, 2, 6)` (3.46); R15
    `kstest(data, 'norm')` D (≈0.096) and p, the one-sided-only max (0.092) and the rows
    (27th, 88th); R16 `ks_2samp(X, Y, method='exact')` D (0.6) and p (hand count 0.0499)
    plus `method='asymp'` p (≈0.08); R17 F = 0.0274, t = 0.165, p (≈0.88).
  - 11_03 marks both gaps 0.092 and 0.096; 11_04 draws $Y$ in 1/8 steps and $D$ at 4.8.
- [x] **T22r** reviewer. Run T22 once; confirm files, the transcription check and every
  printed value; state the exact two-sample p and whether it is < 0.05 (this fixes E7's
  verdict). Out: `reviews/T22.md`. Dep: T22.
- [x] **T23** sonnet-writer. Write the chapter + one `\input` line after `lec10-p-value`
  in part1 + ONE added line in lec10 `sec:pv-future` carrying `\Cref{ch:compare-dist}`.
  In: architecture.md §7.4, T22r values, `notes_text/11_*/`. Out:
  `chapters/lec11-comparing-distributions.tex`, `parts/part1-foundations.tex`,
  `chapters/lec10-p-value.tex`. Dep: T22r PASS. AC: AC-W1..W10 on lec11 (`inbrief` env). Plus:
  - labels, each exactly once: `ch:compare-dist`; `sec:cd-background`, `sec:cd-why`,
    `sec:cd-choose`, `sec:cd-t-one`, `sec:cd-t-table`, `sec:cd-t-two`, `sec:cd-anova`,
    `sec:cd-ks`, `sec:cd-ks-two`, `sec:cd-ks-pvalue`, `sec:cd-apply`, `sec:cd-future`;
    `def:t-statistic`, `def:f-statistic`, `def:ecdf`, `def:ks-statistic`; `ex:cd-rory`,
    `ex:cd-t-table`, `ex:cd-tomato`, `ex:cd-cartoon`, `ex:cd-revisit`, `ex:cd-ks-normal`,
    `ex:cd-ks-two`; `tab:cd-symbols`, `tab:cd-tomato`, `tab:cd-anova`, `tab:cd-ks-two`,
    `tab:cd-tests`; `fig:cd-choose` (TikZ), `fig:cd-t-dist`, `fig:cd-anova`,
    `fig:cd-ks-one`, `fig:cd-ks-two` (PNG).
  - Q7: no diff in `04-distributions.tex` or `hw02-data-distributions.tex`.
  - numbers (AC-W6): 0.4, −2.5, 24, 0.0098, 2.75, 2.757, 0.04, 0.011364, 0.00375,
    0.12294, −2.44, 0.024 (df 21), 0.020 (Welch), 33.8, 36, 6, 24, 30, 8, 12, 3.46,
    0.008, 0.125, 0.375, 0.875, 0.6, 0.475, 0.075, 0.092, 0.096, 0.356, 0.7881, 0.136,
    0.645, 1.50, 219.33, 54.83, 0.0274, 6.046, 0.165, 0.88; KS p values = T22r's.
  - E7 verdict written only from T22r's exact p (< 0.05 → 기각, else 기각 실패); a pitfall
    in `sec:cd-ks-pvalue` shows asymptotic and exact p side by side.
  - pitfalls (AC-W7, Q4/Q10 form): R1 ($\bar x/\bar\sigma$ → $(\bar x-\mu_0)/(s/\sqrt n)$),
    R6 = Q11 (slide formula in text; pitfall: 0.024 (df 21) vs Welch 0.020, `equal_var=False`),
    R7 (Comparing Variances vs means), R9 ("m·n−1" = 8 is total df; SSW df = 6),
    R10 ($\alpha < 0.10$ → $\alpha = 0.10$), R12 (below → at or below), R13 ($F_y$ 0.1
    steps → 1/8), R15 (0.092 → 0.096), R16 ($n \le 6$ one-sample table; asymptotic vs
    exact). Plus: $F$ two meanings; KS after estimating parameters = one line +
    `\Cref{sec:normal}` (E6 unaffected, HW2 affected); `keyidea` $F = t^2$ via E5.
  - Q9: HW2 links `\Cref{sec:hw2-compare-how}`, `tab:hw2-airport-verdict`,
    `tab:hw2-movie-verdict`, `sec:hw2-learned` each ≥ 1; no p-value computed for HW2's $D$.
  - `grep -c 'ch:qq-normalization'` in lec11 = 0.
  - lec10: `git diff --numstat` = 1 added, 0 deleted; the line holds `\Cref{ch:compare-dist}`.
  - part1 diff = one added line.
- [x] **T24** reviewer. Out: `reviews/lec11.md`; AC-W2 re-run covers lec10's new line. Dep: T23.

### 3.1c Q8 forward links → lec09, 03, hw02

- [x] **T25** sonnet-writer (done by the main session directly). One NEW source line (inside the paragraph, no blank line)
  in each file: (a) `lec09-hypothesis-testing.tex` `sec:ht-future`, after the
  "정식 검정 통계량" sentence (≈l.603) → `\Cref{sec:cd-anova}`; (b) `03-visualization.tex`
  `subsec:ci-compare` pitfall, after "별도의 검정이 필요하다" (≈l.458) → `\Cref{sec:cd-t-two}`;
  (c) `hw02-data-distributions.tex` `sec:hw2-compare-how`, after the KS distance
  paragraph (≈l.188) → `\Cref{sec:cd-ks-two}`. Out: those three files. Dep: T24 PASS.
  AC: per file `git diff --numstat` = 1 added, 0 deleted; the added line holds exactly
  its listed `\Cref`; AC-W1..W4; no new number; the hw02 line names no p-value (Q9).
- [x] **T26** reviewer (closed differently: main-session numstat + clean build check, no
  reviewer dispatch, no `reviews/q8-links.md`). Out: `reviews/q8-links.md`. Dep: T25.
