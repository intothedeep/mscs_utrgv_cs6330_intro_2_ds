# T13 review: `chapters/01-data-attributes.tex` (T12 fill), cycle 1/2, 2026-09-24

Target: `chapters/01-data-attributes.tex` (numstat 599 added / 0 deleted)
Design: `research/architecture.md` §4.1, `research/arch-deck3.md` (+ 결정 기록), `reviews/T11.md`
AC: PLAN T12 (labels, 2×2, slide-4 answers, M1 pitfall) + §4 AC-W1..W12
Source: `notes_text/3_DataAndMatrix/slides.md`, `media/image17.png`, `media/image21.jpeg`

**Verdict: ISSUE** (build, numbers, coverage, skeleton, additions-only all pass; 3 substantive
text defects + several minor ones, all implementation class → `sonnet-writer`).

Line numbers below are in the current working-tree file.

## Build (AC-W1, AC-W2)

`latexmk -C` then `latexmk -xelatex -interaction=nonstopmode main.tex`: exit 0.
`grep -cE "undefined|multiply defined" main.log` = 0. Chapter 01 has 7 overfull hboxes of 1.2pt,
all in `pitfall`/`keyidea` boxes (same size as pre-existing line 176 box); environment artifact, not
flagged. Chapter 04 did not break the build.

## AC table

| AC | Result | Evidence |
| :-- | :-- | :-- |
| T12 labels (8 `sec:`) | PASS | all 8 present, order: In brief → background → existing 4 → discrete → data-matrix → dimension → vector → everything-matrix → apply → future |
| T12 2×2 table | PASS | `tab:attr-discrete-2x2` L297-311, cells match arch-deck3 §2.3 |
| T12 slide-4 answers | PASS | L328-335 명목, 구간, 순서, 비율, 명목 (= slides.md slide 4) |
| T12 pitfall slide 8 vs 11 | PASS (minor wording, see I-8) | L429-441 |
| AC-W1 build | PASS | exit 0 |
| AC-W2 refs | PASS | 0 |
| AC-W3 no em dash | PASS | added non-comment lines: 0 hits (L1, L23 em dashes are pre-existing, title unchanged per D3-Q2) |
| AC-W4 `\Cref` only | PASS | 0 `\ref/\autoref/\cref`, 0 hard-coded chapter numbers; every `\Cref` target resolves (duplicate `ch:*` labels only in `x_` files not `\input`) |
| AC-W5 bilingual | ISSUE (minor) | see I-6, I-7 |
| AC-W6 numbers | PASS | recompute table below |
| AC-W7 pitfalls E1/E2/E3 | PASS | E1 L479-484, E3 L539-545, E2 L547-552, all "슬라이드 값은 X ... 다시 계산하면 Y" |
| AC-W8 skeleton | PASS | chapter `inbrief` (= `\paragraph{In brief.}`+description, preamble L176) L5-13 before first `\section`; concept sections have In brief; everything-matrix omitted per design |
| AC-W9 slide coverage | PASS | `% source:` slides 1, 2-4, 3, 5-8, 9-12, 13-15, 16-19; slide 20 = Kahoot "내용 없음" in map |
| AC-W10 figures | ISSUE (minor) | 03_01..03_04 exist in `hw1/00_lecture_charts/figures/`, T11 PASS; captions Korean; but `tab:attr-synonyms` never `\Cref`'d (I-4) |
| AC-W11 | n/a | 02 not touched |
| AC-W12 additions only | PASS | numstat 599/0; `git diff -U0` has 0 `-` lines, so no existing line changed |
| Decision record | PASS | E1, E3 as pitfalls; M1 exempt from Q4 form; title unchanged |
| T11 note (`item`) | PASS | L438, L771-778: 107 of 126, not an identifier, row number identifies |
| No design IDs / media filenames in reader text | PASS | 0 hits for E1/R17/M1/C1/D3-Q/image N/T1x/A03 in added non-comment lines |
| `그림 (그림` / `표 (표` | ISSUE | 2 hits (I-3) |
| TikZ legibility | PASS | page 20 rendered at 80 dpi: both figures readable; matrix in `fig:attr-network` is `\scriptsize` and bracketless, small but legible |

## Recompute (`uv run python -c`, no fitting)

| Value | Book | Recomputed | Result |
| :-- | :-- | :-- | :-- |
| Adjacency row sums / total | 3,3,2,5,2 / 15 (L749) | [3,3,2,5,2], 15; symmetric; 7 edges + 1 loop | PASS |
| Matrix vs `image21.jpeg` | L736-740 | row-by-row match | PASS |
| Iris mean point | (5.8433, 3.0573) L635-636, L642 | 5.8433, 3.0573 | PASS |
| Iris 10 rows | L610-619 | `load_iris` rows 1-8, 149, 150 match | PASS |
| Jane–Dave raw / normalized | 1.0000 / 0.0476 | 1.0 / 0.0476 | PASS |
| Jane–John raw / normalized | 5000.0016 / 0.3839 | 5000.0016 / 0.3839 | PASS |
| Ranges | 21, 15000 | ptp age 21, salary 15000 | PASS |
| 5×3 cells, array dim, space dim | 15, 2, 3 (L520-522) | 15, 2, 3 | PASS |
| Name/Salary/Age matrix | $\mathbb{R}^{5\times2}$ | 5 rows, 3-1=2 | PASS |
| Iris numeric | $\mathbb{R}^{150\times4}$ | (150, 4) | PASS |
| HW1 df | 126×8, 7, $\mathbb{R}^{126\times5}$ | (126, 8), numeric (126, 5) | PASS |
| `item` uniques | 107 of 126 | 107; "Cheeseburger" in McDonald's, Burger King | PASS |
| King vector first 5, length 50 | L696-697 | matches `image17.png`; 10+11+10+11+8 = 50 | PASS |

## ISSUEs

All implementation class → route to `sonnet-writer`. Design and numbers are correct; only the prose
is wrong.

- **I-1 (substantive) L786, L788, L791: wrong currency.** "급여 0원 차이", "급여 5000원 차이",
  "급여 차이 5000원". The salary column is dollars (`tab:attr-name-salary-age` header
  "급여(Salary, \$)"). Fix: "\$0", "\$5000" (or "급여 차이 5000").
- **I-2 (substantive) L792-793: false claim "결과가 뒤집힌다".** The ranking does not flip:
  Jane–Dave stays closer both before (1 < 5000.0016) and after (0.0476 < 0.3839) normalization.
  What changes is age's share of the distance (4/21 = 0.1905 against 5000/15000 = 0.3333), which is
  what arch-deck3 §4.2 says ("정규화 뒤에야 나이가 거리에 기여한다"). Rewrite to that claim.
- **I-3 (substantive) L432, L486: "표 (표" in PDF.** `급여$\cdot$나이$\cdot$근속연수 표(\Cref{tab:attr-3d-data})`
  and `이름/급여/나이 표(\Cref{tab:attr-name-salary-age})` render as "... 표 (표 1.6)" and
  "... 표 (표 1.4)".
- **I-4 L380-394: `tab:attr-synonyms` has no `\Cref` in text** (AC-W10). Add one reference in the
  L367-378 paragraph.
- **I-5 L785-797: align lines not one operation each (one fix with I-2).** L796 writes
  "1.0000 / 21", dividing the raw distance by the age range, which is right only because the
  salary difference is 0. L785, L787 and L797 each fold several operations (square, sum, root;
  L797 also two divisions) into one line. Split per principle 10: $4/21 = 0.1905$,
  $5000/15000 = 0.3333$, $\sqrt{0.1905^2+0.3333^2} = 0.3839$, and $1/21 = 0.0476$ for Jane–Dave.
  The intermediate values 0.1905 and 0.3333 are exactly the evidence the corrected I-2 sentence
  needs (salary still larger, age share now visible).
- **I-6 L329, L596: proper names transliterated.** "그리니치" (Greenwich, no English at all) and
  "피셔의 붓꽃 데이터(Fisher's Iris Data)". Task criterion: names in English. Fix "그리니치" →
  "Greenwich" unconditionally. "피셔" also appears in lec07 L1025 and lec10 L201, L237; fixing only
  ch01 creates inconsistency, so fix it book-wide as a backlog item or have the owner accept the
  parenthesized form.
- **I-7 AC-W5 missing English at first introduction:** 막대그래프, 히스토그램 (In brief L267-268
  and L282; Bar Chart, Histogram), 산점도 (caption L494, first use in the book
  order), 평균 점 (L630), 유클리드 거리 (L781), 정규화 (L792), list heading `\textbf{이산화.}`
  (L814). \term hits otherwise all bilingual: 표(Table), 행(Row), 열(Column),
  좌표평면(Coordinate Plane), 이산형(Discrete), 연속형(Continuous), 표 데이터(Tabular Data),
  데이터 행렬(Data Matrix), 배열 차원(Array Dimension), 공간 차원(Space Dimension),
  벡터(Vector), 인접 행렬(Adjacency Matrix).
- **I-8 (minor) L429-441: M1 wording.** Decision record fixes the phrase "두 슬라이드가 세는
  대상이 다르다"; the text says "두 표가 세는 대상이 다르다" and does not say that the source
  slides count differently. Content is right; align the sentence to the decision record.
- **I-9 (minor) L298-299: 2×2 caption** says "빈 칸은 ... 존재하지 않는다" while the cell reads
  "없음". Refer to the "없음" cell. ("척도(행)" matches the PLAN AC wording; not flagged.)
- **I-10 (minor) principle 8 openings:** body first paragraphs of `sec:data-matrix` (L361),
  `sec:dimension` (L459) and `sec:vector` (L569) open with definitions. In brief Why carries the
  problem, but principle 8 asks the body's first paragraph to unfold it one step. `sec:attr-discrete`
  (L278-283) does this correctly and can serve as the model.

- **I-11 (minor) L597: tense of a forward reference.** "\Cref{sec:qq-iris-source}에서 밝혔듯"
  points forward (lec07 follows ch01 in `parts/part1-foundations.tex`). Use "밝힌다" or
  "자세한 출처는 ... 에 있다" (principle 9a).

Checked and not flagged: `\texttt{notes/3\_DataAndMatrix.pptx}` at L31 follows the same
background-section precedent as lec09, lec10, lec11, 02, 04.

## Observation (reasoning, not blocking; for pm/architect)

- L766 "`item` 열을 빼면 속성 7개" gives no reason, and L771 then says `item` is *not* an
  identifier. A beginner will ask why a non-identifier is removed from the attribute count. The
  design (arch-deck3 R18, T11 note) keeps "속성 7" without resolving this. Either state the reason
  (e.g. a label column that is neither a measured attribute nor a key) or count 8 attributes.
  Owner/architect call; not routed to the writer until decided.

## Observation (docs, for pm)

- PLAN.md L175 A03 and L177 T11 are still `[ ]`, though `reviews/T11.md` says PASS and AC-W10
  requires the developer task `[x]` before the writer dispatch. Bookkeeping per docs.md §7; not
  a writer defect.

## Re-review (cycle 2), 2026-09-24

numstat 617 added / 0 deleted. Build: `latexmk -C` then `latexmk -xelatex`, exit 0;
undefined/multiply defined = 0; "Log file appears" = 0. pdftotext "표 (표"/"그림 (그림" = 0.
Added non-comment lines: em dash 0; design IDs 0; filenames only in `\includegraphics` args.

Recompute (`uv run python -c`): 4/21 = 0.1905, 5000/15000 = 0.3333, hypot = 0.3839,
1/21 = 0.0476, raw 5000.0016. Book L809-812 match; ranking unchanged claim (L804-805, L818-819) correct.

| Item | Result | Evidence |
| :-- | :-- | :-- |
| I-1 currency | PASS | L797, L799, L802 `\$0`, `\$5000` |
| I-2 flip claim | PASS | L804-806, L815-819: order unchanged, age share changes |
| I-3 표 (표 | PASS | pdftotext 0 hits; L433 rephrased |
| I-4 synonyms ref | PASS | L381 `\Cref{tab:attr-synonyms}` |
| I-5 one op per line | PASS | L809-812 |
| I-6 names | PASS | L329 Greenwich, L606 Fisher (book-wide 피셔 in lec07/lec10 remains backlog) |
| I-7 glosses | ISSUE (minor) | Bar Chart/Histogram L268, Scatter Plot L501, Euclidean Distance L791-792, Normalization L804, Discretization L832 present; 평균 점 (In brief L568, `\paragraph` L640) still has no English |
| I-8 두 슬라이드가 | PASS | L436 |
| I-9 caption/cell | PASS | L298 caption refers to "없음", cell L308 "없음" |
| I-10 openings | PASS | L361, L462, L576 open with the problem; statements true |
| I-11 tense | PASS | L607 "다룬다" |

New (minor, implementation → `sonnet-writer`):

- **N-1 L796, L798, L815 "원 단위 거리".** Intended "raw units", but next to a salary column
  it reads as "won units", the exact confusion I-1 removed. Use "원래 단위 거리" or "정규화 전 거리".
- **N-2 L817 "같은 크기로 거리에 들어간다".** 0.1905 and 0.3333 are not the same size; the intended
  claim is the same scale (both divided by their range, 0 to 1). Say "같은 척도(0에서 1)로".

**Verdict: ISSUE (minor only).** All cycle-1 substantive defects resolved. Remaining: I-7 (평균 점
gloss), N-1, N-2. Cycle 2/2 exhausted; fixing these needs owner approval for a third cycle or a direct edit.
