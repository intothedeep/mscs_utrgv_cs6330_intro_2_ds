# Review: 02 skew sign (sec:skew-sign)

- Cycle: 1/2
- Date: 2026-09-23
- Target: `book_intro_2_ds/chapters/02-descriptive-statistics.tex` added lines 300 and 332-448 (+ `\label{sec:skew-rule}` at 450), `hw1/00_lecture_charts/skew_cases.py`, `hw1/00_lecture_charts/figures/02_skew_{right,symmetric,left}.png`
- Build: `latexmk -xelatex -interaction=nonstopmode main.tex` from `book_intro_2_ds/`, exit 0, 43 pages
- Script run: `uv run python hw1/00_lecture_charts/skew_cases.py` (plotting only, no training)

Overall: **ISSUE** (1 reasoning, 4 implementation). No blockers for numbers or figures; the fixes are all text-level.

## AC1: one figure per case, caption then label, \Cref in text: PASS

- `fig:skew-right` L344-352, `fig:skew-symmetric` L354-360, `fig:skew-left` L362-369. Each has `\caption` then `\label`.
- All three referenced at L337 (`\Cref{fig:skew-right,fig:skew-symmetric,fig:skew-left}`); also L365, L425, L443.
- Note: the new table `tab:skew-by-chart` (L395) is never referenced by `\Cref` anywhere. See ISSUE-3.

## AC2: 3-5 chart types from deck 5: PASS

Each PNG has 5 panels: Histogram, Density line, Box plot, Violin plot, Barcode chart.
All in `notes_text/5_StatandVisualization/slides.md`: Histogram (slide 12), Line Chart "getting closer to the probability density function" (slide 14), Violin Plot (slide 17), Barcode Chart (slide 19), Box Plot (slide 20). Shared x-axis (-20 to 75) across the three figures, so direct comparison works.

## AC3: numbers match script, align* arithmetic: PASS

Script stdout:

```
skew_right      n=300  G1=1.48  mean=16.32  median=13.95  sd=11.15  (mean-median)/sd=0.21  Q1=8.40  Q3=22.06
skew_symmetric  n=300  G1=-0.07  mean=16.48  median=16.78  sd=10.95  (mean-median)/sd=-0.03  Q1=9.55  Q3=23.49
skew_left       n=300  G1=-1.48  mean=43.68  median=46.05  sd=11.15  (mean-median)/sd=-0.21  Q1=37.94  Q3=51.60
```

Every number in captions (G1 1.48, -0.07, -1.48), example (n=300) and the three align* blocks matches. Arithmetic rechecked:
- Right: 16.32-13.95=2.37; 2.37/11.15=0.2126->0.21; 22.06-13.95=8.11; 13.95-8.40=5.55. OK.
- Left: 43.68-46.05=-2.37; -2.37/11.15=-0.21; 51.60-46.05=5.55; 46.05-37.94=8.11. OK.
- Symmetric: 16.48-16.78=-0.30; -0.30/10.95=-0.027->-0.03; 23.49-16.78=6.71; 16.78-9.55=7.23. OK.
- Mirror claim (L423-425, "정확히 자리를 바꾼다"): holds exactly. n=300 linear-interpolation quantile positions 74.75 and 224.25 are mirror images (299-224.25=74.75), so Q1_left = 60-Q3_right = 37.94 and G1 negates exactly.
- `|G1|=0.07<0.5` vs `sec:skew-rule` table (L452-460, `|gamma|<0.5` = 거의 대칭): consistent.
- Deck title checked: L332 "강의 5강(Basic Statistics and Visualization)" matches slide 1 of `notes_text/5_StatandVisualization/slides.md`.
- Minor (not an ISSUE): L340-341 "평균과 표준편차를 맞춘 정규 분포" does not say matched to what; the script sets loc/scale to the right sample's mean/sd (16.32/11.15), realized 16.48/10.95. Consider "우측 왜도 표본과 평균·표준편차를 맞춘".

## AC4: tab:skew-by-chart claims visible in PNGs: PASS

Checked each cell against the PNGs:
- Histogram: right peak at ~10 with bars trailing to ~70; symmetric peak ~17 with tails to ~-16 and ~50 (similar); left is the mirror. OK.
- Density line: right peak (~10) left of mean dash (16.3); symmetric peak on mean; left mirrored. OK.
- Box plot: right median 13.95 left of box centre 15.23, left whisker ~7 vs right whisker ~18, 7 orange outliers on the right; symmetric whiskers ~21 vs ~20, median near centre; left mirrored. OK. (Symmetric also shows 3 left and 1 right outlier; the table does not deny this.)
- Violin: right thin long tail to ~70; symmetric near mirror-symmetric; left mirrored. OK.
- Barcode: dense left, sparse right; symmetric even; left mirrored. OK.
Figure captions (L345-349, L356-358, L363-367) also match the PNGs.

## AC5: data labelled synthetic: PASS

L337-341: "\textbf{실제 강의 자료가 아니라 합성(synthetic) 표본}", with seed and generator named. Script docstring (L3) also says synthetic.
Note (not an ISSUE): the PNG titles read "Right-skewed sample (gamma)" etc. without the word "synthetic", and the files sit in the same `figures/` directory as course-data charts. A reader who sees the PNG alone could not tell. Consider adding "synthetic" to the suptitle.
Note (not an ISSUE): L332 opens with "같은 표본을" right after a pitfall about the cereal `sodium`/`sugars` sample, so a reader can take it as "the same (course) sample" before reaching the synthetic sentence at L338. Suggest "한 표본을".


## AC6: style: ISSUE

- No em dash in added lines: PASS (grep of `+` lines for `—` and `---` returns nothing).
- One calculation per line with comments: PASS (L405-410, L417-422, L431-436).
- `\Cref` only, all targets exist: PASS. `sec:histogram` 03:115, `sec:density-line` 03:177, `sec:violin` 03:247, `sec:barcode` 03:272, `sec:boxplot` 03:299, `fig:skew-gap` 02:321, `sec:skew-rule` 02:450. No undefined references in `main.log`.
- **ISSUE-1 (implementation):** cleveref multi-reference renders English conjunctions in a Korean sentence. PDF p.10: "그림 2.4 to 2.6 의 데이터는" (from L337); PDF p.14: "그림 2.4 and 2.6 는" (from L443). These are the only two such occurrences in the book. `preamble.tex` L150 sets `\crefname{figure}` but no `\crefrangeconjunction` / `\crefpairconjunction` / `\creflastconjunction`. Fix options: set Korean conjunctions in the preamble (touches the whole book), or write the references separately in the text. Also the particle after the number is wrong: L425 renders "그림 2.6 가" (should be 이), L443 renders "2.6 는" (should be 은).
- **ISSUE-2 (implementation):** English is missing at introduction sites in the table and captions (book.md §1 counts table headers, cells and captions as introduction sites):
  - L374 header `그림 & 우측 왜도 & 대칭 & 좌측 왜도`: no English (e.g. 우측 왜도(Right-skewed), 대칭(Symmetric), 좌측 왜도(Left-skewed), 그림(Chart)).
  - L379 row label `선 그래프(밀도 곡선)`: no English, while the other four row labels have it (Line Chart / Density Line).
  - L394 caption `다섯 가지 그림에서 왜도가 남기는 흔적.`: 왜도 has no (Skewness).
  - Figure captions L345-349 and L363-367 name 히스토그램, 선 그래프(밀도 곡선), 박스플롯, 바이올린 플롯, 바코드 차트, 중앙값 without English. The rule says to add it when unsure. These caption items are softer: L333-336 already gives the English for all five chart types in the same subsection, so they fall under the "when unsure, add it" clause. The table header (L374), the row label (L379) and the table caption (L394) are the firm part of this ISSUE.

## AC7: additions only: PASS

`git diff` for the chapter has only `+` lines: `\label{sec:skew-sign}` (L300), the block L332-448, and `\label{sec:skew-rule}` (L450). The existing sign table (L302-312), `fig:skew-gap` (L317-322) and its pitfall (L324-330) are untouched. The `hw1/00_lecture_charts/main.py` diff only adds the `skew_cases` call (outside this AC but in scope, fine).

## AC8: build: ISSUE (build clean, layout splits the example)

- exit 0; no undefined or multiply-defined references.
- Overfull boxes: `lines 324--330` (existing pitfall) and `lines 441--447` (new pitfall), each 1.20001pt. The same 1.2pt overfull shows up on every `pitfall` callout in every chapter (about 29 in `main.log`), so it comes from the environment, not the new text. Not attributed.
- Page flow (logical pages): subsection starts p.9; text + example `ex:skew-three-cases` p.10; `fig:skew-right` p.11, `fig:skew-symmetric` p.12, `fig:skew-left` p.13 (full float pages, `[p]`); `tab:skew-by-chart` + new pitfall + `sec:skew-rule` p.14.
- **ISSUE-5 (implementation):** the example `ex:skew-three-cases` (L398-439) is split across four pages. PDF p.10 ends at the last align line of the left-skew case (`46.05 - 37.94 = 8.11`). The paragraph "이번에는 아래쪽 거리..." and the whole 대칭 표본 block land on p.14, after the three full-page floats (p.11-13). A reader loses the example in the middle. Cause: `[p]` floats go out at the next page break after their source position, and the three `figure` envs (L344-369) plus the `table` (L371-396) sit before the example. Fix: move the three figures and the table to after `\end{example}` (or after the new pitfall, L447), so the example stays on consecutive pages.
- **ISSUE-3 (implementation):** `tab:skew-by-chart` (L371-396) has no `\Cref` in the text (book.md §2: every table is referenced with `\Cref`). It floats to p.14, after the example and after three full-page figures, so a reader never gets pointed to it. Add a `\Cref{tab:skew-by-chart}` in the intro paragraph (L332-342), and consider `[p]`/placement so it sits closer.

## Reasoning findings

- **ISSUE-4 (reasoning):** New pitfall L441-447 says "박스플롯은 원래 다섯 수치 요약(최솟값, $Q_1$, 중앙값, $Q_3$, 최댓값)만 그리며". This contradicts (a) the book's own definition in `03-visualization.tex` L305-306 (whiskers go to the farthest point within $1.5\times\IQR$, points beyond are plotted as outliers) and (b) the new figures themselves, which show whiskers stopping short of min/max and orange outlier points (the captions at L348-349 and L366-367 point to these outliers). Suggested wording: box = $Q_1$-$Q_3$, median line, whiskers to $1.5\times\IQR$, outliers as points. The point about the mean not being drawn by default still holds.
- Minor: L443 says only `fig:skew-right,fig:skew-left` had the mean line added, but `fig:skew-symmetric` has it too (and so do the violin panels). Consider citing all three.

## Summary

| AC | Result |
| --- | --- |
| AC1 | PASS |
| AC2 | PASS |
| AC3 | PASS |
| AC4 | PASS |
| AC5 | PASS (note: PNG titles do not say synthetic) |
| AC6 | ISSUE-1, ISSUE-2 (implementation) |
| AC7 | PASS |
| AC8 | ISSUE-3, ISSUE-5 (implementation); build itself clean |
| extra | ISSUE-4 (reasoning, pitfall box-plot definition) |

Routing: ISSUE-1/2/3/5 -> `sonnet-writer`. ISSUE-4 is a factual correction that the book's own `sec:boxplot` already settles, so `sonnet-writer` can apply it directly. No research is needed.

## Re-review (cycle 2)

- Date: 2026-09-23
- Target: `chapters/02-descriptive-statistics.tex` L299-452 (current line numbers)
- Build: `latexmk -xelatex -interaction=nonstopmode main.tex`, exit 0; no undefined or multiply-defined references in `main.log`
- Script: `uv run python hw1/00_lecture_charts/skew_cases.py` (plotting only, no training); stdout identical to cycle 1
- Rendered text checked with `pdftotext -layout main.pdf`

Overall: **ISSUE** (1 new implementation issue introduced by the ISSUE-1 fix). ISSUE-1..5 are all resolved.

### Earlier issues

| ID | Result | Evidence |
| --- | --- | --- |
| ISSUE-1 (cleveref English conjunctions, particles) | PASS | Multi-refs removed. PDF p.14: "그림 2.4 부터 그림 2.6 까지"; no "to"/"and" left. Caption of `fig:skew-left` renders "그림 2.4 를" (correct). But see ISSUE-6. |
| ISSUE-2 (English at introduction sites) | PASS | L421 header has Chart / Right-skewed / Symmetric / Left-skewed; L426 row label has Line Chart, Density Line; L441 caption has Chart, Skewness; `fig:skew-right` / `fig:skew-left` captions now give Histogram, Line Chart, Box Plot, Median, Outlier, etc. Soft note: `fig:skew-symmetric` caption (L402-404) still names 중앙값, 박스플롯, 바이올린 플롯, 바코드 차트 without English (same subsection already gives them, so not re-raised). |
| ISSUE-3 (`tab:skew-by-chart` never referenced) | PASS | L337 `(\Cref{tab:skew-by-chart})`, renders "(표 2.1)". |
| ISSUE-4 (box plot drawn as five-number summary) | PASS | L446-448 now: box Q1-Q3, median line, whiskers to farthest point within 1.5×IQR (`\Cref{sec:boxplot}`), outliers as points. Matches `03-visualization.tex` and the figures. |
| ISSUE-5 (example split across four pages) | PASS | Figures moved after the example. Example: p.15-16 (consecutive); table 2.1 + pitfall p.16; figures 2.4/2.5/2.6 on p.17/18/19; `sec:skew-rule` p.20. |

### AC re-run

| AC | Result | Note |
| --- | --- | --- |
| AC1 | PASS | Three figures, caption then label; referenced at L337-338, L372, L411, L448-449. |
| AC2 | PASS | PNGs unchanged in content (script output identical, fixed seed). |
| AC3 | PASS | All align* numbers (L353-380) and captions (G1 1.48, -0.07, -1.48) match script stdout. |
| AC4 | PASS | Table cells unchanged apart from English additions. |
| AC5 | PASS | L339 synthetic statement intact. |
| AC6 | ISSUE | ISSUE-6 below. No em dash in `+` lines of `git diff` (the `---` in L460-462 is the pre-existing `sec:skew-rule` table, untouched). |
| AC7 | PASS | `git diff` has no `-` lines for the chapter. |
| AC8 | PASS | exit 0; only overfull boxes are the book-wide 1.2pt `pitfall` ones (L324-330, L445-452), same as cycle 1. |

### New issue

- **ISSUE-6 (implementation, route to `sonnet-writer`):** the particle workaround writes `그림(\Cref{...})`, and `\Cref` already prints "그림", so the noun is doubled in the PDF.
  - L372: PDF p.15 "이것이 그림 (그림 2.6) 이 그림 (그림 2.4) 의 좌우 반전으로 보이는 이유다."
  - L448-449: PDF p.16 "그림 (그림 2.4) 과 그림 (그림 2.6) 은 설명을 위해 ..."
  Suggested fix: rephrase so that the particle follows a Korean noun, not the number, e.g. "\Cref{fig:skew-left}의 모양이 \Cref{fig:skew-right}의 모양을 좌우로 뒤집은 것처럼 보이는 이유다", and "\Cref{fig:skew-right,fig:skew-symmetric,fig:skew-left}" is not an option (brings back ISSUE-1), so use "세 그림(\Cref{fig:skew-right}부터 \Cref{fig:skew-left}까지)은" or "\Cref{fig:skew-right}와 \Cref{fig:skew-left}의 박스플롯은". Note: 2.4 (사) takes 와/를/는, 2.6 (육) takes 과/을/은/이.

### Carried-over minor (not an ISSUE)

- L448-449 still names only `fig:skew-right` and `fig:skew-left` as having the added mean line; `fig:skew-symmetric` has it too.
- Float labels render as "Figure 2.x" / "Table 2.x" book-wide (caption name setting); pre-existing, not from this change.

Routing: ISSUE-6 -> `sonnet-writer`. This was cycle 2/2; a third cycle needs the owner.
