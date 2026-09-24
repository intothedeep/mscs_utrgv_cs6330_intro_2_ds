# T24 review: `chapters/lec11-comparing-distributions.tex` (cycle 1/2)

Date: 2026-09-23. Scope: new `chapters/lec11-comparing-distributions.tex` (861 lines), the one-line
diffs in `parts/part1-foundations.tex` and `chapters/lec10-p-value.tex` (`sec:pv-future`).
Criteria: PLAN.md T23 AC list, §4 AC-W1..W10, owner Q7/Q9/Q10/Q11; architecture.md §7.4 and
decision record 7.y; `reviews/T22.md` values. Source: `notes_text/11_Comparing_Distributions/slides.md`
+ media (image1, image34, image45 viewed: they confirm R1 $t=\bar x/\bar\sigma$, R12 "below $x$" with $F_{obs}(y_i)=i/n$, R16 one-sample table $n=1$-$6$). Deck 10 slides 22-25 checked against architecture §7.3.3.

Build: `latexmk -C` then `latexmk -xelatex -interaction=nonstopmode main.tex` in `book_intro_2_ds/`.

## Verdict: ISSUE

Numbers, KS verdicts, labels, build and the Q7/Q9 guards all pass. Blocking: a wrong claim in the
R1 pitfall (I1), a table that calls an exact p "근사" (I2), a broken TikZ figure (I3), and an
unreferenced, misplaced figure (I4). The rest are form and wording fixes. All route to `sonnet-writer`.
No reasoning issue. Ladder L1-L4: not applicable (book work, not system/app).

## Mechanical ACs

| AC | Result | Evidence |
| :-- | :-- | :-- |
| AC-W1 build | PASS | exit 0 |
| AC-W2 refs | PASS | `grep -cE "undefined\|multiply defined" main.log` = 0 (covers lec10's new `\Cref{ch:compare-dist}`) |
| AC-W3 em dash | PASS | 0 hits of `—`/`---` in non-comment lines |
| AC-W4 `\Cref` only | PASS | 0 `\ref`/`\cref`/`\autoref`; 0 hard-coded chapter numbers; all 34 T23 labels defined exactly once book-wide |
| Rendered "그림 (그림" / "표 (표" | PASS | 0 hits in `pdftotext main.pdf` |
| Overfull > 5pt from this file | **ISSUE (I3, I12)** | 75.18pt at l.151-154 (`fig:cd-choose`), 10.21pt at l.719-722 (`inbrief` How). All other boxes are 1.2pt |
| AC-W5 bilingual | **ISSUE (I11)** | `\term` hits all carry English except where listed in I11 |
| AC-W6 numbers | PASS | every listed number present (grep), and all recomputed below |
| AC-W7 pitfalls | **ISSUE (I7)** | R1, R7, R10, R12, R13, R15, R16 in form. R6 and R9 titles not in form |
| AC-W8 skeleton | PASS (form) / ISSUE I8 (openings) | `inbrief` before first `\section`; background, why, choose, t-one, t-table, t-two, anova, ks, ks-two, ks-pvalue, apply, future in order; every concept section has `inbrief` |
| AC-W9 slide coverage | PASS (I13 note) | `% source:` union covers deck 11 slides 1-24. Deck 10 slides 22-25 traced by lec10 l.753 and lec11 l.118, l.288 |
| Figure gate (T22) | PASS (doc lag) | `uv run python hw1/00_lecture_charts/deck11_compare.py`: "position mismatches = 0", no WARNING (T22r I1 fixed in 0cc1ad1); PNGs unchanged in git after the run. PLAN.md still shows `[ ] T22` / `[ ] T22r` (l.156, l.173): pm to close |
| AC-W10 figures | **ISSUE (I4)** | all 4 PNGs exist in `hw1/00_lecture_charts/figures/`; `fig:cd-anova` has 0 `\Cref` |
| Q7 | PASS | `git diff` on `04-distributions.tex`, `hw02-data-distributions.tex`, `99-appendix-toolchain.tex`: empty |
| Q9 | PASS | `sec:hw2-compare-how` 2, `tab:hw2-airport-verdict` 1, `tab:hw2-movie-verdict` 1, `sec:hw2-learned` 1; no p-value computed for HW2's $D$ (l.808-809) |
| `ch:qq-normalization` | PASS | 0 |
| lec10 diff | PASS | numstat 1/0; the line holds `\Cref{ch:compare-dist}` |
| part1 diff | PASS | numstat 1/0, after `lec10-p-value` |
| 7.y (KS two-sample) | PASS | 0.645 paired with Kolmogorov 0.0815 (fail to reject), exact 0.0499 (reject), 0.0674 in one parenthetical sentence, no "약 0.08" |

## Recomputed numbers (`uv run python -c`, scipy)

| Item | Chapter | Recomputed | Result |
| :-- | :-- | :-- | :-- |
| `t.cdf(-2.5,24)` | 0.0098 | 0.009827 | PASS |
| `2*t.sf(2.75,5)`, $t_{0.02,5}$ | 0.0403, 2.757 | 0.040310, 2.75651 | PASS |
| tomato $s^2/n$, sum, SE, $t$ | 0.011364, 0.00375, 0.015114, 0.12294, −2.4403 | 0.0113636, 0.00375, 0.0151136, 0.122938, −2.440264 | PASS |
| `2*t.sf(2.44,21)` | 0.0236 | 0.023641 | PASS |
| Welch df, p | 33.79, 0.0201 | 33.787, 0.020077 | PASS |
| `f.sf(12,2,6)`, `f.ppf(0.90,2,6)`, $5^{-3}$ | 0.008, 3.4633 | 0.008000, 3.463304, 0.008 (`f_oneway` F = 12.0) | PASS |
| ANOVA E5 (lec09 values C={20,28,34}, D={22,26,37}) | SSB 1.50, SSW 219.33, MSW 54.83, F 0.0274, SE 6.046, t 0.165, p 0.88 | 1.5, 219.333, 54.833, 0.027356, 6.0461, 0.16540 ($t^2$ = 0.027356 = F), p 0.87666 | PASS |
| lec09 "0.7%" | 0.7% | 1.5/220.83 = 0.68% | PASS |
| one-sample KS (script `KS_DATA`) | 0.0957 row 27 (x = −0.37), 0.092 row 88 (x = 0.80), p 0.2997 | below-step max 0.095691 at row 27; above-step max 0.091855 at row 88; `kstest` p 0.299681 | PASS |
| $\Phi(-0.37)$, $\Phi(0.80)$, $1.36/\sqrt{100}$ | 0.356, 0.7881, 0.136 | 0.35569, 0.78814, 0.136 | PASS |
| two-sample KS | D 0.6 at 4.8; 0.645; 0.0815; 2182/43758 = 0.0499; 0.0674; gap 0.00013 | D 0.6 at 4.8; 0.645105; `kstwobign.sf` 0.081519; exact 0.049865 ($\binom{18}{8}$ = 43758); asymp 0.067400; 0.000135 | PASS |

Formulas: one-sample $t$ with $\sqrt n$ (l.181) PASS; two-sample unpooled SE per slide + pooled vs Welch df in pitfall (l.280, l.316-335) PASS (Q11); $F$ = MSB/MSW with df $m-1$, $m(n-1)$ (= $k-1$, $N-k$ for equal $n$) PASS; ECDF "at or below" (l.533) PASS; KS $\sup_x$ with both step sides (l.556, l.597-601) PASS; closed-form tail for numerator df 2 PASS.

## ISSUEs

| ID | Lines | Class | Route | Blocking | Detail |
| :-- | :-- | :-- | :-- | :-- | :-- |
| I1 | 193 | implementation | sonnet-writer | yes | R1 pitfall: "$\sqrt n$이 없으면 표본 크기가 커져도 통계량이 작아지지 않는다" is backwards. $t = \sqrt n(\bar x-\mu_0)/s$ **grows** with $n$; without $\sqrt n$ it does not grow, so more data never adds evidence. Should read "커지지 않는다". Also R1 says the numerator is fine in the paired design ($\mu_0 = 0$); the text blames $\mu_0$ equally |
| I2 | 792-793 | implementation | sonnet-writer | yes | `tab:cd-tests` labels both KS rows "KS 분포(근사)", but 0.0499 is the **exact** p (the chapter's own E7 point, l.765-767) and 0.2997 is `kstest`'s exact kstwo(100) value (T22r I3: Kolmogorov limit would be 0.3191). Label them exact |
| I3 | 139-144 | implementation | sonnet-writer | yes | `fig:cd-choose`: 75pt overfull. Rendered (p. 58): leaf boxes 40mm wide at xshift ±14mm overlap pairwise ("집단 2개"/"집단 3개 이상", "가설 분포 있음"/"없음") and the right pair runs past the text edge |
| I4 | 834-840 | implementation | sonnet-writer | yes | `fig:cd-anova` has no `\Cref` anywhere (AC-W10) and sits in `sec:cd-apply` after the check questions, so it renders on p. 68, 13 pages after `ex:cd-cartoon`. Move it into `sec:cd-anova` and cite it there |
| I5 | 49, 612 | implementation | sonnet-writer | no | l.49 "누적분포함수(`sec:cdf`)는 04에서 그림과 정의만 요약한다" is false: `sec:cdf` is a TODO stub. Both lines also show the file prefix "04" to the reader. Say the chapter by `\Cref` only and drop the "summarises" claim |
| I6 | 467 | implementation | sonnet-writer | no | "R17" is a design-doc ID in reader text (renders). Delete it |
| I7 | 316, 432, 436-437 | implementation | sonnet-writer | no | AC-W7 form: R6 title "자유도를 무엇으로 잡느냐에 따라..." and R9 title "슬라이드의 m*n−1은..." are not "슬라이드 값은 X, 다시 계산하면 Y". R9 body "두 값이 우연히 6을 공유하는 것이 아니라" is incoherent: the slide shows df = 2+2+2 = 6 with the label $m*n-1$ (= 8). State that plainly |
| I8 | 176, 276, 352, 512, 242 | implementation | sonnet-writer | no | Principle 8: body after `inbrief` opens with the definition/statement (t-one l.176, t-two l.276, anova l.352, ks l.512) or straight into the example (t-table l.242). One problem → prescription paragraph each (e.g. t-one: $z$ needs $\sigma$ → estimate with $s$ → extra spread → t-distribution) |
| I9 | 651-663, 689-694 | implementation | sonnet-writer | no | Architecture §7.4.5 E7 / §7.4.6: `tab:cd-ks-two` = all 18 merged values with $F_y$ in 1/8 steps. The chapter has a 3-row excerpt, so the corrected $F_y$ column is packed into one sentence (l.691-694), against principle 10 |
| I10 | 398, 485, 672, 678 | implementation | sonnet-writer | no | One operation per `align*` line: l.672 and l.678 put two computations ($F_x$ and $F_y$) on one line; l.398 and l.485 chain two operations |
| I11 | 294, 377, 416, 481, 520-523, 736, 749, 788, 168, 266 | implementation | sonnet-writer | no | AC-W5 gaps: t분포/F분포 never given (t-distribution)/(F-distribution); 합동 분산 (Pooled Variance) l.377/481; "평균제곱(MS)" lacks Mean Square; 콜모고로프 극한분포 (Kolmogorov Distribution) l.736/749; `tab:cd-tomato` and `tab:cd-tests` headers Korean only; `fig:cd-ks-one` caption introduces 경험적/이론적 누적분포함수 without English. `\term{대응 설계}, Within-subjects Design` (l.168, 266) uses a comma instead of parentheses |
| I12 | 719-722 | implementation | sonnet-writer | no | 10.2pt overfull: `\texttt{scipy.stats.kstest}` in the `ks-pvalue` How line. Allow a break or shorten |
| I13 | 116-126 | implementation | sonnet-writer | no | Architecture §7.3.3 row 23: deck 10 slide 23's extra line "Different variables, from different populations?" should appear in `sec:cd-choose` as "비교 자체가 성립하는지부터 물어야 한다". Absent |
| I15 | 739-740 | implementation | sonnet-writer | no (fold into I2 fix) | "임계값 대신 p값 자체를 계산하면 결론이 갈린다" is false: the Kolmogorov p 0.0815 agrees with the 0.645 critical value. What flips the verdict is asymptotic vs exact, which is the E7 lesson |
| I16 | 176-186, 279-281 | implementation | sonnet-writer | no | §7.4.2: `def:t-statistic` holds one-sample AND two-sample in one box. The box has one-sample only; the two-sample formula is a bare display outside it |
| I14 | 850-852 | implementation | sonnet-writer | no | "Q-Q 플롯은 다음 강의의 몫" is wrong: that is deck 7, an earlier lecture. "해당 장이 아직 없으므로" is build-state talk in reader text. Say "Q-Q 플롯(Q-Q Plot)으로 확인한다" without the status remark |

Notes (no action): `sec:cd-future` `% source:` (l.845) is not in `deck N slide K` form; `deck 11 slide 3` (image1, normality) would do.
 `\texttt{imageN}` and `\textbf` in body follow the lec10 precedent (PASS there).
The `% source:` comments for deck 10 slides 22-25 live in lec10 l.753, which is acceptable under AC-W9.

## Re-review (cycle 2)

Date: 2026-09-23. Target: `chapters/lec11-comparing-distributions.tex` (962 lines, opened with Read).
Build: `latexmk -C` then `latexmk -xelatex -interaction=nonstopmode main.tex`, exit 0.

### Verdict: PASS (all blocking items closed), 3 non-blocking ISSUEs remain

### Mechanical re-checks

| Check | Result | Evidence |
| :-- | :-- | :-- |
| Build | PASS | exit 0 |
| Undefined / multiply defined | PASS | `grep -cE "undefined\|multiply defined" main.log` = 0 |
| `\Cref` targets | PASS | all 49 distinct targets defined once in the built tree (`ch:project` also in soft-deleted `x_05_project_log.tex`, which is not `\input`) |
| Overfull > 5pt from this file | PASS | only 1.2pt boxes (book-wide callout pattern) |
| Em dash (`—`, `---`) outside comments | PASS | 0 |
| Design-doc IDs (R/E/T/Q/I/AC/§/7.y) in reader text | PASS | 0 |
| Rendered "그림 (그림" / "표 (표" | PASS | 0 in `pdftotext main.pdf` |

### Cycle-1 ISSUEs

| ID | Result | Evidence |
| :-- | :-- | :-- |
| I1 | PASS | l.217-226: SE $s/\sqrt n$ shrinks with $n$, so $t$ grows; without $\sqrt n$ denominator is fixed $s$, $t$ "커지지 않는다". Numerator point for $\mu_0=0$ stated separately. Each step correct |
| I2 | PASS | `tab:cd-tests` l.899-900 both "KS 분포(정확)"; caption: both KS p exact, two-sample flips vs asymptotic 0.0815. Consistent with architecture 7.y (l.907-913) and the pitfall l.849-879 |
| I3 | PASS | 0 overfull on l.133-156; rendered p. 58 (pdftoppm): four leaves separated, all inside text width |
| I4 | PASS | `fig:cd-anova` at l.497-503 inside `ex:cd-cartoon` in `sec:cd-anova`, cited at l.495 |
| I5 | PASS | l.49 no "04", no "summarises" claim |
| I6 | PASS | "R17" gone |
| I7 | PASS | R6 (l.365-366) and R9 (l.506-507) titles in "슬라이드 값은 X, 다시 계산하면 Y" form; R9 body states 2+2+2=6 vs label $m*n-1$=8 plainly |
| I8 | PASS | 고치는 문제 / 아이디어 paragraphs added to t-one, t-table, t-two, anova, ks (see N1 for one wrong reference) |
| I9 | PASS | 18-row `tab:cd-ks-two` l.737-765. Recomputed (`uv run python -c`): every $F_x$, $F_y$, $\lvert F_x-F_y\rvert$ row matches; max 0.6 at 4.8; `ks_2samp` exact D 0.6, p 0.049865. Note: pitfall l.794-796 still repeats the $F_y$ list in a sentence; now redundant with the table, optional trim |
| I10 | **ISSUE (open)** | chained operations on one `align*` line remain: l.473 `24/2 / 6/6 = 12/1 = 12`, l.553 `1.50/1 / 219.33/4 = 1.50/54.83 = 0.0274` (also l.239, l.532). l.672/678 split fixed (l.768-782) |
| I11 | **ISSUE (partial)** | fixed: F분포(F-distribution) l.434, 합동 분산(Pooled Variance) l.440, 평균제곱(Mean Square, MS) l.481, 콜모고로프 극한분포(Kolmogorov Distribution) l.839, `fig:cd-ks-one` caption, 대응/독립 설계 parentheses. Open: "t분포" never paired with (t-distribution) (first at l.178/188); `tab:cd-tomato` header "밭" and `tab:cd-tests` headers "비교 대상", "이 장의 예제" Korean only |
| I12 | PASS | no overfull in `ks-pvalue` inbrief |
| I13 | PASS | l.126-129 |
| I14 | PASS | l.952 "Q-Q 플롯(Q-Q Plot)으로 확인한다", no status remark |
| I15 | PASS | l.843-847: critical value and Kolmogorov p agree; the flip is attributed to asymptotic vs exact. True |
| I16 | PASS | `def:t-statistic` l.193-211 holds one-sample and two-sample (unpooled SE, matches slide / tomato calc); df deferred to the t-two pitfall |

Recomputed values for 7.y: `kstwobign.sf(0.6*sqrt(80/18))` 0.081519, $1.36\sqrt{18/80}$ 0.645105, `method='asymp'` 0.0674, gap $0.05-0.049865$ = 0.000135. All match the text.

### New findings

| ID | Lines | Class | Route | Blocking | Detail |
| :-- | :-- | :-- | :-- | :-- | :-- |
| N1 | 328-329 | implementation | sonnet-writer | no | "두 표본이 독립이면 분산은 더해진다는 성질(\Cref{def:spread})": the claim is true, but `def:spread` (02-descriptive-statistics l.80-92) defines only SD and IQR, no variance additivity. The reference points at something that is not there. Drop the `\Cref` or state the property in place |

Note (no action): l.404-405 "매 검정마다 5\%씩 쌓이는 거짓 양성" is a loose simplification (familywise rate is $1-0.95^k$, not additive), acceptable at this level. l.921 "Q-Q 도표" vs l.952 "Q-Q 플롯": two Korean terms for one thing.

Cycle count: this is cycle 2/2. The open items are non-blocking form fixes; a third cycle needs the owner.
