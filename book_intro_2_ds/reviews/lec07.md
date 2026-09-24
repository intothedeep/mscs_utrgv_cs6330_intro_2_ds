# Review: lec07-qq-normalization (task T07, cycle 1/2)

Target: `book_intro_2_ds/chapters/lec07-qq-normalization.tex` (1030 lines, new), `book_intro_2_ds/parts/part1-foundations.tex` (one-line `\input`, between `04-distributions` and `lec09`: correct).

Status: DONE

## Verdict

**ISSUE (not PASS).** Build, refs, skeleton, slide coverage and all architecture/T05 numbers pass. Four content errors
(two wrong numbers, one wrong software claim, one invented fact), one logically inverted sentence, and style
issues (design-doc IDs in reader text, multi-operation `align*` lines). All route to `sonnet-writer`; none needs
the architect.

## Build

- `latexmk -C` then `latexmk -xelatex -interaction=nonstopmode main.tex`: exit 0.
- `grep -cE "undefined|multiply defined" main.log` = 0.
- `pdftotext main.pdf - | grep -cE "그림 \(그림|표 \(표"` = 0.

## Numbers (recomputed)

`uv run python hw1/00_lecture_charts/deck7_qq_normalization.py`: every printed value matches the chapter
(R8 movie fits, E1 ppf, R10/R12 gaps, E3 both rules, iris quantiles and all three count rows, E5, E6, E7, R24, E4, sugars 17 zeros,
skew 2.7088 / 0.0146, calories Shapiro p 0.00038).

Independent spot check (`uv run python`, scratch script, no fitting):

| Item | Chapter | Recomputed | Verdict |
| :-- | :-- | :-- | :-- |
| Slide-18 income range, x2 | 5700, 0.0351 | 5700, 0.03509 | PASS |
| z x2, ddof 0 / 1 | (-1.352, -1.263) / (-1.282, -1.198) | same | PASS |
| Iris equal-width right / left closed | 45,50,43,12 / 41,48,48,13 | same | PASS |
| Quantile-norm 4x4 result | slide 20 matrix | identical | PASS |
| calories Shapiro p (n=126) | 0.00038 | 0.000376 | PASS |
| sugars skew before / after log1p | 2.7088 / 0.0146 | 2.70883 / 0.01459 | PASS |
| Iris F-hat(5.0), F-hat(5.1) (l.505-506) | 0.207, 0.273 | **0.2133**, 0.2733 | **ISSUE I1** |
| Mean-filled median (tab:qq-impute l.878) | 2500 | **2405.6** | **ISSUE I2** |
| scipy.stats.probplot first position, n=15 (l.329-330) | "(i-0.5)/n" = 0.0333 | **0.0452** (Filliben) | **ISSUE I3** |

## AC checklist

| AC | Result | Note |
| :-- | :-- | :-- |
| W1 build | PASS | exit 0 |
| W2 refs | PASS | 0 undefined / multiply defined |
| W3 no em dash | PASS | 0 hits for `—` / `---` |
| W4 `\Cref` only | PASS | no `\ref`/`\cref`/`\autoref`, no "N장" |
| W5 bilingual | PASS with a note | `\term` hits: 경험적 CDF (Empirical CDF), 플로팅 위치 (Plotting Position), 콜모고로프-스미르노프 통계량 (KS Statistic), 분위수 대 분위수 도표 (QQ Plot), 로버스트 (Robust). In-brief and section terms bilingual. Table cells in tab:qq-scaling / tab:qq-transforms are Korean-only (re-mentions; minor, I7) |
| W6 numbers | ISSUE | I1, I2 (all architecture recompute rows present and correct) |
| W7 slide-error pitfalls | PASS | R20 "슬라이드 값은 2400, 다시 계산하면 5700" (l.559), R22 (-1.35,-1.26) vs (-1.28,-1.20) (l.580). R4/R5 symbol pitfall, R14, R15 present |
| W8 skeleton | PASS | chapter inbrief → sec:qq-background → sec:qq-why → 8 what sections (each opens with inbrief + 고치는 문제/아이디어) → sec:qq-apply → sec:qq-future |
| W9 slide coverage | PASS | `% source:` union = slides 1-26 |
| W10 figures | PASS | 07_01..07_10 and 06_01 included, captioned, labelled, `\Cref`'d; fig:qq-flow TikZ |
| T06 labels | PASS | all 14 `sec:` labels present; `fig:normal-fit` labelled once, here |
| T06 CDF self-summary, `\log 0` → ex:zero-as-missing | PASS | l.45-50, l.789-796 |
| T06 deck 2 slides 9-11 in sec:impute | PARTIAL (I8) | source comment lists 9-11; reader text cites slide 10 only |
| T05 note: log1p sugars not "normal" | PASS | l.803-809 pitfall and fig:qq-log caption say multimodal, Q-Q still bends |
| Formulas | ISSUE | QQ positions, min-max, z (n-1), robust median/IQR, quantile-norm ties (mean-of-slots) correct. I4 below |

## Issues

| ID | Line | Class | Route | Item |
| :-- | :-- | :-- | :-- | :-- |
| I1 | 505 | implementation | sonnet-writer | F-hat(5.0) = 0.207 is wrong; 32/150 = 0.213 |
| I2 | 878 (tab:qq-impute) | implementation | sonnet-writer | Mean-imputed median shown as 2500; with 2311.1 filled in, the n=10 median is (2311.1+2500)/2 = 2405.6. (Architecture's E7 table had no median column; writer added it) |
| I3 | 329-330 | implementation (unsourced claim added by writer) | sonnet-writer | "scipy.stats.probplot 같은 소프트웨어는 (i-0.5)/n" is false: probplot uses Filliben medians (p1 = 0.0452 for n=15). Either drop the scipy attribution or state the Filliben rule |
| I4 | 261-262 | implementation | sonnet-writer | Logic inverted: "후보 분포가 정규분포일 때는 Φ^{-1}을 그 분포의 역CDF로 바꿔 쓴다" should read "정규분포가 아닐 때는". Also the baseline y = μ̂ + σ̂z is stated as holding for any candidate |
| I5 | 1017 | implementation (invented fact) | sonnet-writer | "축구 경기 영상 데이터": image67 says "soccer data" (red cards vs skin colour); nothing about video. Also "변환 선택" narrows the figure's "statistical method" |
| I6 | 73, 309, 328, 410, 425, 427, 503, 729 | implementation | sonnet-writer | Design-doc / file IDs in reader text: "E1", "E3", "$E1$의 간격", "03의 규칙", "03 규칙". Use `\Cref{ex:qq-...}` / `\Cref{ex:quantile}` |
| I7 | 476, 573, 574, 577, 656 | implementation | sonnet-writer | `align*` lines hold 2-4 computations each (book.md principle 10: one calculation per line). Minor: tab:qq-scaling / tab:qq-transforms cells Korean-only |
| I8 | 836-840 | implementation (minor) | sonnet-writer | Deck 2 slides 9 and 11 cited only in the `% source` comment, not in reader text. Also this intro paragraph comes before 고치는 문제 in sec:impute, which breaks the problem→prescription order slightly |
| I9 | 998-999 | implementation (minor) | sonnet-writer | `\label{sec:qq-iris-source}` on `\subsection*` resolves to the enclosing numbered section (sec:qq-apply), so `\Cref` at l.469 prints that section's number |

No reasoning or ladder issue: every architecture.md §8.4 row and T05 value is honoured.

## Re-review (cycle 2)

Date 2026-09-24. Target `chapters/lec07-qq-normalization.tex` (1052 lines).

### Build
`latexmk -C` then `latexmk -xelatex -interaction=nonstopmode main.tex`: exit 0, 0 "undefined" in main.log, no multiply-defined labels. pdftotext: 0 hits for "그림 (그림" / "표 (표". Chapter 5 (lec07) PDF text has 0 em dashes; source has 0 `—` / `---`.

### Recomputed (uv + sklearn load_iris, data only; scipy)
| Check | Chapter | Recomputed | Status |
| --- | --- | --- | --- |
| Iris F-hat(5.0), F-hat(5.1) (l.516-517) | 0.2133, 0.2733 | 0.2133, 0.2733 (n=150, [4.3, 7.9]) | PASS |
| Mean-filled median (l.882, tab l.900) | (2311.1+2500)/2 = 2405.6 | 2405.56 | PASS |
| sd rows (l.883-885) | 1819.5 / 1481.1 / 1396.4, SS 17,548,889 | same | PASS |
| probplot p1, n=15 (l.337) | 0.0452 | 0.0452 (Filliben 1-0.5^(1/15)) | PASS |
| Phi^-1 of Filliben p1 (l.339) | -1.693 | -1.6937 (rounds to -1.694) | minor, I11 |
| Chapter rule i/(n+1), p1 = 0.0625 (l.328, 336) | stated | 1/16, Phi^-1 = -1.534 | PASS |
| 03 rule (l.329-330) | (i-1)/(n-1) | 03-visualization.tex l.77 `(i-1)/(n-1)` | PASS |

### Prior issues
| ID | Status | Evidence |
| --- | --- | --- |
| I1 | CLOSED | l.516 0.2133 |
| I2 | CLOSED | l.882, l.900 2405.6 with derivation line |
| I3 | CLOSED | l.327-342: Filliben formula, 0.0452, scipy attribution correct |
| I4 | CLOSED (residual minor) | l.261 now "정규분포가 **아닐** 때". Residual: l.264-265 still states baseline y = mu-hat + sigma-hat z for any candidate; for uniform[0,1] quantiles the line is not mean + sd times p. Not blocking |
| I5 | CLOSED | l.1039-1044 "축구 경기 데이터", 29 teams, 20 significant / 9 not: counted on image67 (9 grey, 20 green). FiveThirtyEight and "Brian Nosek et al." are printed in the figure. No invented detail |
| I6 | CLOSED | grep `E[0-9]`, `R[0-9]`, "03 규칙", "03의" in non-comment lines: 0 hits |
| I7 | CLOSED | align* at l.483-487, 562-566, 581-591, 668-673: one computation per line, values re-checked (age SS 953.6, sum 272) |
| I8 | CLOSED | l.855-861 cite deck 2 slides 9, 10, 11; matches notes_text/2_Data/slides.md l.80-105 (Completeness; "Zeros replace missing values"; badly chosen categories, suspicious values, too coarse). Wording nit: slide 11 says "badly chosen", chapter says "나쁘게 정의됨" |
| I9 | CLOSED | `\subsection{붓꽃 데이터 출처}` numbered; main.aux resolves sec:qq-iris-source to 5.13.1 |

### New findings
| ID | Line | Class | Route | Issue |
| --- | --- | --- | --- | --- |
| I10 | 888-889 | implementation (minor) | sonnet-writer | "나누는 수만 10으로 커져": with the n-1 sd used on l.884-885 the divisor goes 8 to 9, not to 10. l.885 itself divides by 9 |
| I11 | 339 | implementation (minor) | sonnet-writer | Phi^-1(0.0452) = -1.6937, which rounds to -1.694; chapter prints -1.693 |

### Verdict (cycle 2)
PASS with minor issues. I1-I9 closed. I10 is a small wording error in the imputation explanation, and I11 is a rounding slip. Neither blocks the build or any AC. No reasoning or ladder issue.
