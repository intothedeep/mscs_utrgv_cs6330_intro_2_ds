# Review: chapters/04-distributions.tex (T09 fill), T10 cycle 1/2

Date: 2026-09-24. Reviewer: T10. Target diff: `git diff --numstat` 613 added, 13 deleted.
Criteria: research/PLAN.md T09 AC + §4 AC-W1..W12; design research/arch-deck6.md (+ decision record), architecture.md §4.3; source notes_text/6_DataDistribution/slides.md.

**Verdict: ISSUE.** No build, number or deletion defect. 7 implementation issues in reader text, rendering and source comments, all routed to `sonnet-writer`. No reasoning or ladder issues.

## Checks

| AC | Result | Evidence |
| :-- | :-- | :-- |
| AC-W1 build | PASS | `latexmk -C`, then `latexmk -xelatex -interaction=nonstopmode main.tex`: exit 0, 124 pages |
| AC-W2 refs | PASS | `grep -cE "undefined\|multiply defined" main.log` = 0 |
| AC-W3 no em dash | PASS | added lines: 0 hits (`---` only in the untouched chapter title, line 1) |
| AC-W4 `\Cref` only | PASS | 0 `\ref/\autoref/\cref`, 0 hard-coded chapter numbers. All targets resolve (build clean); spot-checked sec:qq-apply, sec:ht-background, sec:qq-background, ch:compare-dist, def:ecdf |
| AC-W5 bilingual | ISSUE-5 (minor) | `\term` hits all bilingual: 분포(Distribution), 확률밀도함수(PDF), 확률질량함수(PMF), 가우스분포(Gaussian Distribution), 종 모양 곡선(Bell Curve), 멱법칙(Power Law), 파레토분포(Pareto Distribution), 여집합 누적분포함수(Complementary CDF), 누적분포함수(CDF), 경험적 누적분포함수(Empirical CDF), 콜모고로프-스미르노프 통계량(Kolmogorov-Smirnov Statistic). Non-term intros are also bilingual (Exponential, Uniform, Bernoulli, Binomial, Geometric). Gaps are listed under ISSUE-5 |
| AC-W6 numbers | PASS | all 16 T09 numbers present and recomputed (see table below) |
| AC-W7 pitfalls | ISSUE-1 | all three slide errors sit in `pitfall` envs with the correct X and Y, but the pitfalls print the template text itself (see ISSUE-1) |
| AC-W8 skeleton | PASS | chapter `inbrief` (preamble 176: expands to `\paragraph{In brief.}` + description) before the first `\section`. Order: background, normal, exponential(+subsec:geometric), powerlaw, uniform, binomial, cdf, 요약, dist-apply, dist-future, matching arch-deck6 §2.1. Every concept section opens with `inbrief` |
| AC-W9 slide coverage | ISSUE-3 | slide 10 has no `% source:` comment |
| AC-W10 figures | PASS | 6 `\includegraphics` (06_02..06_07) resolve in the build. Each has a caption and a label and is `\Cref`'d. `06_01` is not included; `fig:normal-fit` is only `\Cref`'d (lines 154, 629) |
| AC-W11 | n/a | 02 not touched |
| AC-W12 additions only | PASS | all 13 deleted lines are TODO placeholders (see below) |
| Protected labels | PASS | sec:normal, sec:exponential, sec:uniform, sec:binomial, sec:cdf, ch:distributions, def:normal present in 04. ch:distributions also appears in the soft-deleted `x_03_distributions.tex`, which is not `\input`, and there is no multiply-defined warning |
| sec:cdf design | PASS | no CDF redefinition: one-line F(x)=P(X<=x) + `\Cref{def:ecdf}` (line 565), `def:ks-statistic`, `sec:cd-ks`, `sec:dist-check-cdf` |
| serving_size gap | PASS | 0.152 vs 0.101 (line 451), matches T08 output (reviews/T08.md ISSUE-2) |
| Geometric as approximation | PASS | two-column table `tab:dist-geometric` (lines 283-296), text "근사이지 오류가 아니다" (263). No pitfall |
| E6 symbol fix | PASS | lines 403-405, prose sentence, no "E6" in reader text |
| Design IDs in reader text | ISSUE-2 | no R*/E*/Q-*/AC-* IDs, but pptx media names leak (ISSUE-2) |
| pdftotext `그림 (그림` / `표 (표` / `??` | PASS | 0 |
| def:normal and KS pitfall untouched | PASS | no diff hunk touches HEAD 20-29 (def:normal) or 33-37 (KS pitfall). Hunk deletions 4+2+1+3+1+1+1 = 13 = numstat. Lines 171-175 are identical to HEAD (its own `% TODO` comment is kept, as the design requires) |

## Deleted lines (AC-W12)

| HEAD line | Content | Verdict |
| :-- | :-- | :-- |
| 4 lines | `\item[Why/When/Where/How] % TODO` in the sec:normal inbrief | TODO stubs, refilled at 85-92 |
| 2 lines | `% TODO: 06_01_normal_fit.png, 06_02...` + continuation `% 68-95-99.7 ... (96.0%)` | comment TODO block, replaced by fig:dist-sigma-bands + the fig:normal-fit ref |
| 1 line | `% TODO: $\lambda = 1/\text{mean}$, 06_04...` | TODO, replaced by fig:dist-exponential |
| 3 lines | `% TODO: 06_05...` + `% 주의: serving_size ...(0.153 > 0.101)` (2 lines) | comment TODO block. Its content survives as the pitfall at 447-454 with the corrected 0.152 |
| 1 line | `% TODO: 06_07...` | TODO |
| 1 line | `% TODO: 06_03_cdf.png -- ... KS 통계량 D` | TODO |
| 1 line | `% TODO` (요약) | TODO |

None removed an `\includegraphics`, a `\label` or a reader sentence. All 13 are comments or `% TODO` items.

## AC-W6 recompute (`uv run python -c`, arithmetic + data summaries only, no model training)

| Value in chapter | Line | Recomputed | Result |
| :-- | :-- | :-- | :-- |
| 0.4512 (e^-0.6 = 0.548812) | 213-215 | 0.4512, 0.548812 | PASS |
| 6분 | 227 | 60/10 = 6 (but see ISSUE-7: 분 does not render) | PASS (value) |
| 0.5654 (e^-0.8333 = 0.434598) | 236-238 | 0.5654, 0.434598 | PASS |
| 0.0801 slide / 0.0800 no-λ | 240-241 | 0.07996 | PASS |
| 0.05, 0.0475, 0.045125 | 271-274, 288-290 | same | PASS |
| 0.04877, 0.04639, 0.04413; diffs 0.0012/0.0011/0.0010 | 288-290 | 0.04877, 0.04639, 0.04413; 0.00123, 0.00111, 0.00100 | PASS |
| 1/15 | 409 | 1/3 * 1/5 | PASS |
| 95.45%, 68.27%, 1.96 | 134-136, 148 | 0.9545, 0.6827, 1.960 | PASS |
| 2.5, 1.4434 | 426-427 | 1.44338 | PASS |
| 0.24 (0.144 + 0.096) | 485-486 | 0.24 | PASS |
| 0.03125, 0.3125 | 509, 521 | same | PASS |
| sugars mean 13.29, λ 0.0753 | 308, 632 | 13.2889, 0.0752508 | PASS |
| sodium p 0.4524, np 4.52, SD 1.57 | 541-542 | 0.4524, 4.524, 1.574 | PASS |
| calories μ 532.49, σ 249.85, D 0.1007, 96.0%, Shapiro 0.00038 | 149, 576-577, 629 | 532.49, 249.85, 0.1007, 96.0, 0.000376 | PASS |
| sugars CCDF "항목 수(126개)" | 364 | the dataset has n = 126, but the plotted CCDF uses sugars > 0, which is 109 points | ISSUE-6 |

## Issues

All are **implementation issues, route to `sonnet-writer`**. None changes a number or a design decision.

- **ISSUE-1 (AC-W7, template leak into reader text), lines 133, 198, 448.** The writer printed the AC format as prose. The rendered PDF reads "슬라이드 값은 X, 다시 계산하면 Y 형식으로 적으면: 슬라이드 값은 ...". Fix: drop the meta prefix so each pitfall reads "슬라이드 값은 ±2 표준편차 안에 95%, 다시 계산하면 95.45%다." Line 199 should also say "다시 계산하면" (it currently says "다시 확인하면"). Line 448: delete the sentence "... 형식은 이 항목에 적용되지 않는다(...)". The serving_size pitfall is not a slide error and needs no disclaimer.
- **ISSUE-2 (internal artifact names in reader text), lines 138, 495-496, 532.** `\texttt{image5}` and "(image52, image53과 같은 식)" are pptx media filenames from the design notes, and the reader cannot see those files. Fix: "슬라이드 7의 그림", "슬라이드 25, 29의 식과 같다", or remove.
- **ISSUE-3 (AC-W9), slide 10 missing.** There is no `% source: deck 6 slide 10` anywhere. The map (arch-deck6 §1) puts it at `def:normal` as "주석만 추가". Also add `% source: deck 6 slide 16` before `ex:dist-laptop` (line 205). Today slide 16 is covered only through sec:cdf's "slide 16-17 (CDF as tool)" comment.
- **ISSUE-4 (book.md principle 2: names must not be transliterated), lines 352, 356.** The text has "미시간 대학 마크 뉴먼" and "산타페 연구소 에런 클로셋". Slides 21-22 give "Mark Newman, University of Michigan" and "Aaron Clauset, Santa Fe Institute". Write the names in English.
- **ISSUE-5 (minor: book.md 9b/10 and AC-W5).**
  (a) The one-operation-per-`align*`-line rule is broken at 225 (formula + substitution), 227 (two conversions), 272 and 274 (formula = substitution = result), and 521 (formula = substitution = fraction = result). Split these lines.
  (b) The `tab:dist-summary` cells (602-612) and the chapter In brief "Where" line (15-16) name distributions in Korean only. Tables and In brief count as introduction points, so add the English.
  (c) "최대우도추정(MLE)" at 648 lacks the English (Maximum Likelihood Estimation).
- **ISSUE-6 (minor, figure/text mismatch), line 364.** The caption says 126 items, but the CCDF panel plots only the 109 nonzero sugars values (deck6_distributions.py:161). Say 109 nonzero values, or drop the count.
- **ISSUE-7 (latex.md §5, rendering defect), line 227.** `\mathbf{6분}` puts Hangul in math mode. main.log has 2 "Missing character" warnings for 분, and pdftotext shows "= 0.1 시간 = 6" followed by a replacement glyph. The reader sees "6" with a missing glyph where the unit should be. Fix: `\mathbf{6}\,\text{분}`. This is reader-facing, in the same tier as ISSUE-1.
- **Note (not scored), lines 431-434.** Slide 13 lists "Smiling times ... (in secs.)" as the uniform example, and "Generating Random Numbers" is a separate bullet. The text says the smiling times were "난수로 만드는" data, which merges the two. Reword to "웃는 시간 55개를 균등분포의 예로 들고, 난수 생성을 함께 보인다".

## Out of scope, observed

- The stale inbound sentences at lec07:46-47, lec09:58 and hw02:91 are the main session's task under decision Q-B. Not checked here.
- `\textbf{}` body emphasis also appears in the PASSed lec07 (45 hits), so it is this book's convention. Not flagged.
- Concurrent edits to 01-data-attributes.tex did not break the build.

Status: DONE (cycle 1/2). Re-review after the sonnet-writer fix: ISSUE-1..4 and ISSUE-7 required, ISSUE-5/6 recommended.

## Re-review (cycle 2)

Date 2026-09-24, against the working-tree `chapters/04-distributions.tex`.

| Item | Result | Evidence |
|---|---|---|
| ISSUE-1 template leak | PASS | pitfalls at 134, 198 read "슬라이드 값은 X, 다시 계산하면 Y"; no "형식으로 적으면" in source or PDF; serving_size pitfall (452) has no disclaimer |
| ISSUE-2 media names | PASS | no `image[0-9]` in ch04; line 138 reads "슬라이드 7의 그림". The `notes/6\_DataDistribution.pptx` line 24 is the deck name, which lec09/10/11 and ch01 also cite, not a media file |
| ISSUE-3 slide 10/16 | PASS | `% source: deck 6 slide 10` at 119 (def:normal), `% source: deck 6 slide 16` at 205 (ex:dist-laptop); slides 1-30 all appear in `% source:` comments |
| ISSUE-4 names | PASS | 356, 360: "University of Michigan의 Mark Newman", "Santa Fe Institute의 Aaron Clauset" |
| ISSUE-5a align split | PASS | 225-229, 236-240, 273-279, 523-526 are one step per line. Recomputed with uv: 1-e^-0.6=0.4512, 1-e^(-10*5/60)=0.5654, 1-e^(-5/60)=0.0800, 0.95*0.05=0.0475, 0.95^2*0.05=0.045125, C(5,2)=10, 10/32=0.3125, 0.5^5=0.03125, 1/3*1/5=1/15; 60*0.1=6 |
| ISSUE-5b bilingual table / In brief | PASS | tab:dist-summary rows and the line 15 "Where" item carry the English names |
| ISSUE-5c MLE | PASS | 653 "최대우도추정(Maximum Likelihood Estimation, MLE)" |
| ISSUE-6 caption count | PASS | 368-369 says 126 total, 109 plotted after dropping values ≤ 0. `data.load()`: n=126, sugars>0 = 109, ≤0 = 17, NaN 0; matches `deck6_distributions.py` `df["sugars"] > 0` + `loglog` |
| ISSUE-7 분 render | PASS | 229 `\mathbf{6}\,\text{분}`; main.log 0 "Missing character"; pdftotext shows "= 6분" |
| Deletions vs HEAD | PASS | 13 removed lines, all the original `% TODO` / TODO-note lines; the pre-existing calories Shapiro `% TODO` (175) is retained as a comment, not deleted |
| Em dash in added text | PASS | 0 |
| "그림 (그림" / "표 (표" | PASS | 0 in source and PDF |
| Build | PASS | `latexmk -C` then `latexmk -xelatex` in book_intro_2_ds/: exit 0, 0 undefined, 0 `!` errors (second attempt, after a concurrent build by another agent finished) |

Note (out of scope, not ch04): the PDF shows "image5" from `chapters/lec11-comparing-distributions.tex`. It is the same class of leak as ISSUE-2. Report it to the main session for separate routing.

Nit (non-blocking): line 211 `\lambda = 1/5 = 0.2` does two steps on one line. That is a definition, not a calculation, and it was not flagged in cycle 1.

Status: DONE (cycle 2/2). Verdict: PASS. ISSUE-1..7 are closed and no new ch04 issue was found.
