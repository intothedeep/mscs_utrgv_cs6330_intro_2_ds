# Review T16: chapters/02-descriptive-statistics.tex (T15 fill)

Status: COMPLETE, reviewer T16, 2026-09-24

## Checks
| AC | Result | Evidence |
| :-- | :-- | :-- |
| AC-W1 build | PASS | `latexmk -C` + `latexmk -xelatex -interaction=nonstopmode main.tex`: exit 0 (first attempt exit 12 with no process running afterwards, treated as a collision with concurrent builds; retry clean exit 0), 143 pages |
| AC-W2 refs | PASS | `grep -cE "undefined|multiply defined" main.log` = 0 on final log |
| AC-W11 2.3.2 guard | PASS | hunks at new lines 4-17, 31-418, 422, 473, 561-663, 1062-1103; `부호와 방향` spans 806-960; zero hunks inside |
| AC-W12 additions only | PASS | numstat 549 added / 0 deleted |
| AC-W3 no em dash | PASS | 450 added non-comment lines, `grep -cE '—|---'` = 0 (the `---` in lines 1, 420, 471, 665, 717, 1014, 466 are pre-existing) |
| AC-W4 `\Cref` only | PASS | `\ref/\autoref/\cref` = 0; hard-coded chapter numbers = 0 |
| AC-W4 targets | PASS | build 0 undefined. `sec:data-matrix` exists at 01:346 (NOTE: in 01's uncommitted fill; 02 depends on it landing). `sec:cdf` 04:553, `def:ecdf` lec11:617, `sec:hw1-q2`, `sec:hw2-estimators`, `sec:hw2-compare-how` exist. Chain 02 `def:cdf` -> 04 `sec:cdf` (L415) -> lec11 `def:ecdf` (L417) present. 04 -> 02 back-link absent, owned by T09 per decision record |
| AC-W5 bilingual | ISSUE (minor) | every `\term{}` carries English: 표본공간 (Sample Space), 확률변수 (Random Variable), 이산/연속 확률변수, 항등 확률변수, PMF, 베르누이 분포, PDF, 기댓값 (Expected Value), CDF, 최빈값 (Mode), 범위 (Range), 일변량 분석, 불편추정량. Gaps: chapter In brief L13 중심/퍼짐/최빈값/범위 without English; `sec:mode-range` In brief L567-574 introduces 최빈값/범위 before the definition, Korean only; `tab:robustness` header L639 `통계량` without (Statistic) |
| AC-W6 numbers | PASS | all recomputed (`uv run python -c`, data load only, no fit): dice F(k)=k/6, F(3.5)=0.5, E[X]=3.5; x/15 sum 1, F(3)=0.4, P(X>3)=0.6, P(4)+P(5)=0.6, P(X>=3)=0.8; triangle area 1, P(0.5..1.5)=0.75, E[X]=1, F(1)=0.5; iris count 13, 0.0867/0.9133, mean 5.8433 (text 5.843), var 0.6811/0.6857 (text 0.681/0.686), mode 5.0 (10), 4.3-7.9, range 3.6; binom F(0..3)=0.4024/0.7859/0.9504/0.9922 (matches T14, not the design's 0.4025/0.7860); range 4->99 (x24.75, "25배 가까이"), mode 2->2, flip 3->2; median m in [3,4] satisfies both inequalities |
| Die vs x/15 mix | PASS | F(3)=0.5 only in dice contexts (L285 ex:dice-cdf, L374 "주사위에서는"); F(3)=0.4 only in ex:cdf-fifteenths (L318 states P(X=x)=x/15). Not mixed |
| AC-W7 slide-11 pitfall | PASS | `pit:cdf-slide-kx` L361: "슬라이드 값은 $P(X>k)=1-P(X\le x)$, 다시 계산하면 $P(X>x)=1-F(x)$, 즉 $P(X>3)=0.6$"; correct, and says the 0.6 result stands. Confirmed against T14's image17 reading |
| Variance box framing | PASS | `pit:variance-n` L408-412 uses the Q4 wording but the next sentence is "이것은 오류가 아니라 관례 차이다", and it explains both conventions; does not imply the slide was wrong |
| Formulas | PASS with NOTE | PMF sum 1 (L150, L161, L323), PDF integral 1 and not a probability (L171, `pit:pdf-not-prob`), P(X=v)=0, P(X>k)=1-F(k) (L335, L364). NOTE (reasoning, minor): `def:cdf` L274-276 lists three properties and omits right-continuity; the figure caption L311-312 relies on it (open/closed dots). Design §2.5 omitted it too |
| align* one operation per line | ISSUE | L234 (sum, expand, 21/6, 3.5 in one line), L240 (split integral, evaluate, add), L352 `\[` chain of five steps. Borderline two-step lines: L157-158, L329, L335, L341 |
| AC-W8 skeleton | PASS | chapter `inbrief` L4-15 before first `\section` (decision record: `inbrief` env); background L32, concept sections, apply L1063, future L1089, then existing 요약. New concept sections 확률변수, PMF/PDF, CDF, 최빈값과 범위 open with In brief |
| AC-W9 slide coverage | ISSUE (minor) | `% source:` comments cover 1-11, 13, 15-22; 12 and 23 are "내용 없음" in the map. Slide 14 (univariate) is used at L54-56 but no `% source: deck 4 slide 14` comment exists (L34 says 1-3) |
| Slide 14 content | ISSUE | L54 "여러 속성을 한 번에 보는 일을 일변량 분석(Univariate Analysis)이라고 부른다" contradicts slide 14 (image19: "focuses on a single attribute at a time", D is n x 1). Should be one attribute at a time; the next sentence (one column = one random variable) is right |
| Apply section claim | ISSUE | L1069-1070 "HW1 요약표(\Cref{sec:hw1-q2})는 이 장의 평균, 중앙값, 표준편차, IQR을 그대로 계산한 결과다": `sec:hw1-q2` is about min/max calories over complete records; 05-hw1-casebook.tex has no median/SD/IQR summary table (grep). Unsupported |
| Binomial framing | ISSUE (minor) | L382 and caption L400 call the binomial CDF a CDF "of sepal length"; L384 correctly says it is the count of "long" in m=10 draws. Caption should say so |
| AC-W10 figures | PASS | 04_01..04_04 exist; each float has caption + label and is `\Cref`'d (dice-pmf-cdf 1, triangle 1, iris-cdfs 2, mode-range 1, tab:dice-cdf 1, tab:robustness 1). 04_01 now shows open/closed dots (T14 ISSUE-1 fixed), matching caption L310-312. PLAN still shows T14/T14r `[ ]` (doc lag, pm) |
| pdftotext "그림 (그림"/"표 (표" | PASS for 02 | 2 hits, both in chapter 01 text (lines 1244, 1296 of pdftotext output), not in 02 |
| Design IDs / media names / leaked instructions | PASS | added lines: 0 hits for E1/C1-5/O1-7/NOTE-n/A04/T14/Q4/AC-W; 0 `imageNN` names outside `\includegraphics`; 0 TODO/writer/설계/grep. `notes/4\_BasicStats.pptx` at L36 is the source file, same pattern as 01, 04, lec09, lec10 |
| Minor notes (no route) | NOTE | L244 refers to "\Cref{def:center}의 평균 $\hat\mu$" but def:center writes $\mu$; L577 definition title "최빈값과 범위" but it defines only mode (range is L586); L582 `\operatorname{mode}` inline (latex.md §5 prefers `\DeclareMathOperator`; would need a preamble edit outside T15); L643-644 `tab:robustness` cites `ex:mode-range` (iris example) for mode/range resistance, while the resistance demo is the unlabeled table L619-628; `subsec:expectation` L223 opens with the definition, not the why (principle 8) |

## Verdict

**ISSUE** (cycle 1/2). Build, refs, W3, W4, W6, W7, W8, W10, W11, W12 PASS. No ladder/schema issue (book work; L1-L4 not applicable).

| ID | Class | Route | Line(s) | Fix |
| :-- | :-- | :-- | :-- | :-- |
| ISSUE-1 | implementation | sonnet-writer | 54 | univariate = one attribute at a time (slide 14) |
| ISSUE-2 | implementation | sonnet-writer | 1069-1070 | drop or retarget the HW1 claim to a section that actually computes those statistics |
| ISSUE-3 | implementation | sonnet-writer | 234, 240, 352 | split into one operation per `align*` line with `&&\text{}` comments |
| ISSUE-4 | implementation | sonnet-writer | 34 or 54 | add `% source: deck 4 slide 14` |
| ISSUE-5 (minor) | implementation | sonnet-writer | 13, 567-574, 639 | add English at introduction points |
| ISSUE-6 (minor) | implementation | sonnet-writer | 382, 400 | binomial is the count of "long" in 10 draws, not a CDF of sepal length |
| ISSUE-7 (minor) | reasoning | researcher / main session | 274-276 | add right-continuity to `def:cdf` properties (design omission) |

All fixes are additions/edits to lines T15 added; none touch `sec:skew-sign`.

### Addenda (post-check)

- Slide 11 PMF confirmed from image12: $P(X=x)=x/15$, $x\in\{1,\dots,5\}$. Matches L318.
- ISSUE-5 also covers: L300-301 `tab:dice-cdf` uses `--` as a blank cell (book.md principle 11: blank or `없음`; en dash only for ranges); captions L304 (확률/누적확률) and L608-610 (최빈값/평균/범위) lack English (design §6 requires bilingual captions).
- Minor note: L58 `\Cref{ch:descriptive}` is a self-reference from inside the chapter; the intended target is the intro analogy at L19 / `tab:analogy`.
- ISSUE-7 re-routed: **implementation -> sonnet-writer** (one textbook property line, no research needed; pm note: design §2.5 omitted it). ISSUE-2 is classed implementation, not reasoning, for the same reason: the fix is a retarget/deletion of an in-book cross-reference, not new sourcing.

## Re-review (cycle 2)

reviewer T16, 2026-09-24. Build from clean (`latexmk -C`, then `latexmk -xelatex`): exit 0, 0 `undefined` in main.log. numstat 563 added / 0 deleted. Hunks at new lines 4, 32-431, 435, 486, 574-676, 1075-1117; `sec:skew-sign` L820-973 untouched. Added lines: 0 em dash, 0 design IDs / media names.

| ID | Result | Evidence |
| :-- | :-- | :-- |
| ISSUE-1 | PASS | L55-56 "한 번에 한 속성만 들여다보는 일을 일변량 분석(Univariate Analysis)" |
| ISSUE-2 | ISSUE | Target exists: `tab:hw1-burger-vs-shake` (05:123), columns 평균/SD/최소/최대 for Burger, Milkshake. But (a) L1082-1083 says the table "평균과 표준편차를 계산해 저항성을 비교한 결과다"; the table and 05 L108-109, L126 compare spread (SD 277.16 vs 98.84) and representativeness, not resistance (outlier sensitivity, 02 L460). Also omits the min/max columns. (b) `표(\Cref{...})` renders "표 (표 9.2)" in pdftotext (1 hit, this line) |
| ISSUE-3 | PASS | L236-240 (expand, reduce), L244-248 (split integral, values, sum), L349-353 pitfall chain one step per line with `&&\text{}`; all recomputed: 21/6=3.5, 1/3+2/3=1, 1-3/15=0.8 |
| ISSUE-4 | PASS | L57 `% source: deck 4 slide 14` |
| ISSUE-5 | PASS | L13-14 Center/Mode/Spread/Range; L309-310 `없음`; L313 caption bilingual; L582-583, L621-623 Mode/Range; L652 통계량(Statistic) |
| ISSUE-6 | PASS | L395-398 and caption L413-415 say count of "길다" in m=10 draws, not sepal length. Recomputed with p=0.087: F(0..3)=0.4024/0.7859/0.9504/0.9922 (match). Note: unrounded p=13/150 gives 0.4039/0.7872/0.9509/0.9923; text states p=0.087, so consistent |
| ISSUE-7 | PASS | L284-286 right-continuity $\lim_{h\to0^+}F(x+h)=F(x)$, correct; "네 가지 성질" count matches |

### Verdict (cycle 2)

**ISSUE** (cycle 2/2 exhausted; further fix needs owner). One remaining: ISSUE-2, implementation, route sonnet-writer: say the HW1 table compares mean against spread (SD, min, max) to show the mean is not a good representative, not "저항성"; and drop the duplicated noun, e.g. `\Cref{tab:hw1-burger-vs-shake}의 버거 대 밀크셰이크 비교`. All else PASS; no ladder/schema issue (book work).
