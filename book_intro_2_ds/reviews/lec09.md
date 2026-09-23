# T04 review: lec09-hypothesis-testing (cycle 1/2)

Reviewer: reviewer agent, 2026-09-23. Target: `chapters/lec09-hypothesis-testing.tex`
(702 lines), `parts/part1-foundations.tex` (one-line diff). Criteria: PLAN.md T03 AC list +
§4 AC-W1..W10; architecture.md §3. Source: `notes_text/9_Hypothesis_Testing/slides.md` +
`media/` (image12, 20, 21, 28, 29, 31 viewed).

Note: the main session committed the target (b484029) during this review. `git show --numstat`
shows 702/0 for the chapter and 1/0 for part1, and `git diff HEAD` on the chapter is empty, so
the reviewed text is the committed text.

## Verdict: ISSUE

7 blocking issues, all routed to `sonnet-writer` (implementation). The fix for row B2 is
spelled out below so it does not need an architect round trip. Nothing on the MVP ladder
applies (book work, not system work).

## Blocking issues

| # | Line | Finding | Class |
|:--|:--|:--|:--|
| B1 | 467-468 | `\footnote` inside `tabularx` in a float: the note text is **lost** (grep of the full `main.pdf` text finds 0 hits for "묶은 값일 수 있어") and the mark renders as "14" + superscript 1, which pdftotext reads as **"141"**. The R7 boundary warning on the table is gone. Fix: move it into the caption (simplest), or use `\footnotemark` in the cell plus `\footnotetext` after the table. | implementation |
| B2 | 607-608 | `tab:ht-cases` alien row pairs $H_a: p<0.10$(재설정) with p값 0.00664 and 판정 기각. That combination is wrong. Under $H_a: p<0.10$ the p값 is $P(X\le 56)$ = `binom.cdf(56,400,0.1)` = 0.9957, so the verdict is 기각 실패. 0.00664 is the upper-tail value for the slide's $H_a: p>0.10$. Fix (one edit): show the slide's test ($H_a: p>0.10$, 0.00664, 기각), note "(방향 문제는 \Cref{pit:ht-alien})", and keep the reset inside the pitfall. Also minor: architecture §3.6 lists a 관측 column that the table lacks. | implementation (the content is reasoning, but the fix is fully specified here) |
| B3 | 136-137, 290 | Internal spec IDs leak into reader text. The caption reads `(\Cref{sec:ht-why} R13)`, which cites the section it sits in plus an architecture.md row ID. Line 290 reads "R8이 이 함정의 구체적인 예다". Both show up in the PDF ("절 5.2 R13", "R8 이"). Readers cannot resolve R13 or R8. Replace them with plain wording or `\Cref{pit:ht-alien}`. | implementation |
| B4 | 420 | The rendered text has a doubled word: `표(\Cref{tab:ht-alien})` renders as "표 (표 5.4)". Use `\Cref{tab:ht-alien}` alone. This is the only doubling in the chapter's PDF text. | implementation |
| B5 | 588-595, 475-482 | AC-W10: `fig:ht-pooled-vs-group` and `fig:ht-alien-null` are labelled but never `\Cref`'d in the text (count 0). | implementation |
| B6 | 1, whole file | AC-W5 / principle 1: the chapter's own subject, 가설검정, never gets its English gloss (Hypothesis Testing). The only hit is the pptx filename on l.28. It should appear at the chapter's first occurrence (title or In brief). | implementation |
| B7 | 426-428, 436-437, 355/359, 366-375 | AC-W5 + principle 9(c): new terms and notation appear with no gloss or explanation. They are 연속성 보정 (Continuity Correction), 정규근사 (Normal Approximation), 이항계수 (Binomial Coefficient) together with the $\binom{n}{k}$ notation (never read out as "n개 중 k개를 고르는 경우의 수"), 기댓값 (Expected Value, which is also the R4 pitfall title), and the binomial SD formula $\sqrt{np(1-p)}$ and $z$ (neither defined in this chapter). A beginner cannot follow R7 as written. Each needs one or two sentences where it first appears. | implementation |

## Non-blocking (fix in the same pass if cheap)

| # | Line | Finding | Class |
|:--|:--|:--|:--|
| N1 | 359, 561-564, 570-576, 579, 427, 436-437 | The named check "each align* line = one operation" fails in places. l.570-576 fold six squarings plus a sum into one line each (=220.83, =98.67, =120.67), although architecture §3.5 E3 lists the intermediate squares (61.36, 0.03, 38.03, ...). l.359 and 561-564 chain two or three steps per line. l.579 (검산) and l.427, 436-437 ($z$, SD) do the arithmetic inside prose (principle 10). | implementation |
| N2 | 427-428 | "정규근사 p값은 약 1.2--1.5%" is mislabelled. The normal approximation with continuity correction gives 1.22%. 1.49% is the exact binomial value (quoted correctly on l.432). Split the two. | implementation |
| N3 | 438-439 | The Q4 error format "슬라이드 값은 0.007이나, 다시 계산하면 0.00664" is applied to R6, which architecture marks 대체로 맞음. 7/1000 is a correct table reading and 0.00664 is the theoretical value, so this is not a slide error. Recommend "표로 읽은 값 0.007, 이론값 0.00664" instead. | implementation |
| N4 | 136 | The caption says "슬라이드 그림에는 축 눈금이 없어", but slide 7's image20 and image21 do show ticks (10-40 h). The actual problem there is that the dot positions do not match the 0.25/0.5 labels. Slide 4's image12 has unlabelled ticks. Reword the caption. | implementation |
| N5 | 352, 364, 376 | After R4, "시뮬레이션으로 구한 p값" (l.352) and "시뮬레이션 값(0.003)" (l.364) still call the table value a simulation. Suggest "슬라이드 표로 구한 p값". l.376 "항상 0으로 반올림되지는 않는다" is off: real simulation counts are integers, not rounded. Suggest "항상 0으로 나오지는 않는다". | implementation |
| N6 | 163, 305, 241 | Principle 8: the bodies of `sec:ht-hypotheses`, `sec:ht-pvalue` and `sec:ht-forms` open with a definition right after In brief. This is defensible because `sec:ht-why`'s 처방 leads into it, but a one-line "왜" first paragraph would satisfy the principle. | implementation |
| N7 | 58, 556 | l.58 "현재는 뼈대만 있는 절" is book-state text that goes stale once T09 fills 04. l.556 puts media filenames (`image22`, `image23`) in reader text. | implementation |
| N8 | spec | architecture.md §3.6's spec for `fig:ht-drug-experiments` ("왼쪽: 재실험도 같은 방향, 기각") contradicts slide 4, where A is slower in the repeat (image12). The writer and figure correctly follow the slide. The spec row should be corrected. | reasoning (→ system-architect, doc fix only) |
| N9 | process | AC-W10 requires the developer task to be `[x]` before the writer is dispatched, but PLAN.md still shows T01, T01r, T02 and T02r as `[ ]` even though `reviews/T01.md` and `reviews/T02.md` exist (T02 all PASS). The checkboxes need closing by pm. Also out of T03 scope: in-figure text in 09_0N PNGs is English only (T02). | process (→ product-manager) |

## Checklist (dispatch items 1-7)

| Item | Check | Result | Evidence |
|:--|:--|:--|:--|
| 1 | Six-part skeleton + labels | PASS | Chapter `inbrief` (l.5-19; preamble l.176-177 renders it as `\paragraph{In brief.}`), then 배경 l.32, 왜 l.98, 무엇 l.151, 어떻게 적용 l.618, 앞으로 l.686, in that order. All 11 `sec:ht-*`, 3 `ex:`, 5 `tab:`, 5 required `fig:` and `ch:hypothesis` labels exist exactly once. Every concept (sub)section opens with `inbrief`. |
| 2 | Slides 1-14 per §3.3 | PASS | `% source:` union covers 1-14 (l.3, 34, 100, 161, 197, 239, 303, 333, 493, 546, 620, 688). Minor: `sec:ht-exact` (l.493) omits slide 11, which the map lists as "(11)". Slide 7 is used in why (l.123) and cited in decision (l.197). |
| 3 | Recompute every number | PASS with B2, N1, N2, N3 | Independent `uv run python` (scipy): C(15,13..15) = 105+15+1 = 121, 121/32768 = 0.003693 → 0.0037. The table column $1000\binom{15}{k}/2^{15}$ gives 152.74, 196.38, 91.64, 41.66, 13.89, 3.20, 0.46, 0.03, all matching tab:ht-puppy. binom.sf(55,400,0.1) = 0.006637 → 0.00664. binom.sf(53,400,0.1) = 0.014917 → 0.0149. SD = 6, z = 2.583 / 2.25. 0.4^3 = 0.064, 0.4^5 = 0.01024, 0.4^6 = 0.004096, so 6연승 holds. Means 167/6 = 27.83, 82/3 = 27.33, 85/3 = 28.33. SS: 220.83, 98.67, 120.67, 219.33, 1.50, check 0.75+0.75 = 1.50, 1.50/220.83 = 0.68% → 0.7%. Slide tables are sum-verified: puppy = 1000 (image28 matches row by row), alien = 1000 (image29 matches), cumulative 1000/993/953/860/687/360/107/34/7 correct. Every AC-W6 number is present. "%50" is absent. |
| 4a | R4 = expected values, not simulation | PASS (see N5) | l.366-369 and pitfall l.371-378: "슬라이드 값은 '1000회 시뮬레이션 결과'라고 적혀 있지만, 다시 계산하면 정확히 ... 반올림값과 일치하는 **기댓값 표**다. 실제 무작위 시뮬레이션을 돌리면 이 값 근처에서 흔들리며". This clearly says the table is not a simulation. |
| 4b | R7 | PASS (see N2, B7) | l.424-434: "슬라이드 값은 7/1000 = 0.007 ... 다시 계산하면 P(X≥54) = 0.0149", "1% 기준을 넘는다", tail defined as the head count X≥56. Inside a `pitfall`. |
| 4c | R8 | PASS (table B2 contradicts it) | l.441-447: "슬라이드 값은 H_a: p>10%이나, ... 다시 세우면 H_a: p<10%", with a link to `pit:ht-direction`. This matches the slide text (image31: "less than 10%" / "higher"). |
| 4d | p two meanings | PASS | l.68-76 pitfall. The parameter keeps $p$, and the p-value is always written as "p값". The claim that `sec:ci` already used it is verified (03 l.447 "$p<0.05$"). |
| 4e | 1% vs 5% | PASS | l.314-321. 03 has $z=1.96$ (l.377, 383). The analogy to `subsec:fence` "관례" is verified (02 l.150). |
| 4f | 기각 실패 ≠ 증명 | PASS | l.203-211 (slides 2 and 5 quoted, link to `subsec:ci-compare` "겹친다고 같은 것은 아니다", verified at 03 l.455), plus `tab:ht-wording`. |
| 5a | fig:ht-drug-experiments | PASS (see B3, N4) | Text l.114-118: A was 35 h **slower** (image12: A high, B low), and the rejection is of the preliminary 15 h hypothesis ("아직 귀무가설이 아니라"). The caption says the same and marks hours as 개략(schematic). The PNG left panel title "Follow-up contradicts the 15h hypothesis -> reject it" is consistent. E/F: F +0.25 then E +0.5 (image20/21), matching l.124. |
| 5b | fig:ht-pooled-vs-group | PASS (not Cref'd: B5) | Caption l.590-591: "책 자체의 예시, 슬라이드 데이터 아님". l.556-557 in the text says the same. The PNG suptitle reads "book's example values". |
| 6a | No em dash | PASS | `grep -nE '—|---'` = 0. |
| 6b | Bilingual | ISSUE (B6, B7) | `\term` hits, each with its English: 평균 Mean, 퍼짐 Spread, 표본 Sample, 모집단 Population, 모수 Parameter, 확률의 곱셈 규칙 Multiplication Rule of Probability, 독립 시행 Independent Trial, 이항분포 Binomial Distribution, 신뢰구간 Confidence Interval, 부트스트랩 Bootstrap, 귀무가설 Null Hypothesis, 대립가설 Alternative Hypothesis, p값 p-value, 기각 Reject, 기각 실패 Fail to Reject, 유의수준 Significance Level, 유의성 검정 Significance Test, 단측검정 One-sided Test, 양측검정 Two-sided Test, 순열검정 Permutation Test, 통계적 유의성 Statistical Significance, 차등 분석 Differential Analysis. All have English. The misses are the non-`\term` items in B6/B7. |
| 6c | `\Cref` only, targets exist | PASS | No `\ref`, `\cref` or `\autoref`, and no hard-coded 장 numbers. All 34 distinct targets resolve. `ch:hw1` is also labelled in the soft-deleted `x_04_hw1_casebook.tex`, but that file is not `\input`, so no duplicate. |
| 6d | No invented literature | PASS | No `\cite`. The source is the pptx itself (l.28-29). Future topics are attributed to the syllabus. |
| 6e | Principle 9 / 8 | ISSUE (B7, N1, N6) | 배경 self-summarizes the binomial (l.56-60, T03 AC met), and `sec:ht-why` follows 문제→처방 (l.109-148). The gaps are listed in B7, N1 and N6. |
| 7a | Build | PASS | Forced `latexmk -g -xelatex -interaction=nonstopmode main.tex` from `book_intro_2_ds/`: exit 0. |
| 7b | Undefined refs | PASS | `grep -cE "undefined|multiply defined" main.log` = 0. |
| 7c | Overfull boxes in this file | PASS (none attributable) | The lec09 log segment has 8 overfulls, all exactly 1.20001pt, at the paragraph ranges of the `keyidea`/`pitfall` boxes (l.22-26, 68-76, 203-211, 285-291, 314-321, 371-378, 414-452, 520-528). The same 1.2pt overfull appears on every callout box in every chapter, so it comes from the preamble box width, not this file. |
| 7d | Doubled words in PDF | ISSUE (B4) | pdftotext of chapter 5 (PDF p.31-40): one hit, "표 (표 5.4)". The "이 이" hits are grammatical (particle plus demonstrative). |

## AC-W summary

W1 PASS · W2 PASS · W3 PASS · W4 PASS · W5 ISSUE (B6, B7) · W6 PASS (B2 is a table
inconsistency, not a missing number) · W7 PASS (R4, R7, R8 in pitfalls with the Q4 form; see N3) · W8 PASS ·
W9 PASS · W10 ISSUE (B1, B5; checkbox process N9). T03 extras: labels PASS, numbers PASS,
pitfalls PASS, binomial self-summary PASS, part1 = one added line PASS.

## Routing

- `sonnet-writer`: B1-B7, and N1-N7 in the same pass.
- `system-architect`: N8 (correct the §3.6 figure spec row, doc only).
- `product-manager`: N9 (close the T01/T01r/T02/T02r checkboxes).
- Re-review after the fix pass needs cycle 2/2.

## Re-review (cycle 2)

Reviewer: reviewer agent, 2026-09-23. Target: current working-tree
`chapters/lec09-hypothesis-testing.tex` (721 lines, uncommitted). Build: `latexmk -g -xelatex
-interaction=nonstopmode main.tex` from `book_intro_2_ds/`. Numbers were recomputed with scipy.

### Verdict: PASS

All of B1-B7 are closed, and the fixes add no new blocking problem. A few non-blocking items
remain (listed below).

| # | Result | Evidence |
|:--|:--|:--|
| B1 | PASS | `grep footnote` hits only the `\footnotesize` font switch in the TikZ flowchart (l.660, 663). The boundary warning now sits in the `tab:ht-alien` caption (l.489-490), and the PDF shows it: "Table 5.4: ... "14" 행은 [13.5%, 14.5%) 를 묶은 값일 ...". The stray "141" mark is gone. |
| B2 | PASS | Row l.626-627 now reads $p=0.10$ / $p>0.10$ / 0.00664 / 1% / 기각(방향 문제는 \Cref{pit:ht-alien}). This matches slide 12's upper-tailed test: binom.sf(55,400,0.1) = 0.006637, which is below 0.01, so reject. It also matches pitfall item 2 (0.00664, 기각, $X\ge56$) and item 3 (the direction caveat). The PDF renders: "외계인 침공 (절 5.3.4) p = 0.10 p > 0.10 0.00664 1% 기각 (방향 문제는 절 5.3.4)". The 관측 column is still absent (minor, carried from cycle 1). |
| B3 | PASS | `grep -E '\bR[0-9]+\b'` = 0. The caption (l.133-137) and `pit:ht-direction` (l.289-291) now use plain wording and `\Cref{pit:ht-alien}`. |
| B4 | PASS | l.426 is `\Cref{tab:ht-alien}의`. pdftotext of the full `main.pdf` has 0 hits for `그림 ?\(그림` or `표 ?\(표`. |
| B5 | PASS | `fig:ht-alien-null` is `\Cref`'d at l.469 and `fig:ht-pooled-vs-group` at l.600 (1 each). |
| B6 | PASS | l.6: `\term{가설검정}(Hypothesis Testing)` in the chapter In brief. |
| B7 | PASS | This item covers the glosses at l.356-359, 372-375 and 429-439. (1) Binomial coefficient: $\binom{n}{k}$ is read as "n개 중 k개를 고르는 경우의 수", with the $\binom{15}{13}$ example. Correct. (2) Expected value: "여러 번 반복했을 때 평균적으로 나올 것으로 예상되는 값", tied to $1000\binom{15}{k}/2^{15}$. Correct. (3) Normal approximation: for large n, approximate the binomial with a bell-shaped normal. Correct. (4) Continuity correction: widen the boundary by 0.5, so "54 이상" becomes "53.5 이상". Correct direction for an upper tail $P(X\ge54)\approx P(Y\ge53.5)$. (5) $z=(\text{관측값}-\text{평균})/\text{표준편차}$. Correct. (6) Binomial SD $\sqrt{np(1-p)}$, with $\sqrt{400\cdot0.1\cdot0.9}=6$. Correct. Mean $np=40$ is stated at l.454. Recomputed: z = 13.5/6 = 2.25, z = 15.5/6 = 2.583 (the text says 2.58), sf(53) = 0.014917 (0.0149), sf(55) = 0.006637 (0.00664). All match. |
| New: em dash | PASS | `grep -nE '—\|---'` = 0. |
| New: `\Cref` targets | PASS | All 35 distinct targets resolve to exactly one `\label` in `chapters/`, `parts/` and `main.tex` (excluding `x_*`). |
| New: build | PASS | Exit 0. `grep -cE "undefined\|multiply defined" main.log` = 0. |

### Non-blocking (remaining, no cycle needed)

- N2 is still open at l.445-446. "정규근사 p값은 약 1.2--1.5%" still mixes two values. The normal approximation with continuity correction gives norm.sf(2.25) = 1.22%, and 1.49% is the exact binomial value. The next sentence already quotes 0.0149 as exact, so a reader can untangle it.
- l.455-457 has a garbled sentence: "정확한 이항 꼬리 확률은 \textbf{슬라이드 값은 $0.007$이나, 다시 계산하면 ... $= 0.00664$}다" has a doubled subject ("확률은 슬라이드 값은"). Grammar only.
- l.445 (pitfall item 1) uses mean 40 and SD 6 before l.454 states "평균 40". Placing $np=40$ in the l.437-439 gloss would put it first.
- l.373-374: the 기댓값 instance "1000번 시행했을 때 k명이 수컷일 경우의 수 평균" is loosely worded ("경우의 수" here means the expected number of runs with k males). This is acceptable.
- The table row repeats `\Cref{pit:ht-alien}` twice (in the 사례 cell and the 판정 cell). This is harmless.
- N1, N3-N9 from cycle 1 were not re-checked in this cycle (out of scope).

Routing: none blocking. The four text nits above, if taken, go to `sonnet-writer`.
