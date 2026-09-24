# Review T18: 03-visualization.tex skeleton (67 added lines)

Reviewer, cycle 1/2, 2026-09-24. Target: `git diff` of
`book_intro_2_ds/chapters/03-visualization.tex` (new lines 3-16, 31-52, 535-565).
Criteria: PLAN.md T17 (AC-W1..W5, W8, W10, W12, no body line changed), book.md
principles 1, 7, 9, 12, latex.md.

**Verdict: ISSUE** (mechanics all PASS; five content claims in 적용/앞으로 are false
or misanchored; bilingual gaps in In brief and 적용/앞으로).

## Mechanical checks

| AC | Result | Evidence |
| --- | --- | --- |
| AC-W1 build | PASS | `latexmk -C` then `latexmk -xelatex -interaction=nonstopmode main.tex`: exit 0 |
| AC-W2 refs | PASS | `grep -cE "undefined\|multiply defined" main.log` = 0 |
| AC-W3 em dash | PASS | added non-comment lines, `—\|---` = 0 (line 1 `---` is pre-existing, not added) |
| AC-W4 `\Cref` only | PASS | `\ref/\autoref/\cref{` = 0; no hard-coded `N장`; no `그림 (그림` / `표 (표` |
| AC-W4 targets exist | PASS | sec:center, sec:spread, sec:pmf-pdf (02); sec:normal (04); sec:ci, sec:histogram, ex:quantile, pit:sd-se-ci, subsec:ci-compare, tab:form-choice (03); ch:hw1 (05); ch:hw2; sec:qq (lec07); sec:cd-t-two, sec:cd-ks-two (lec11); ch:hypothesis (lec09). Duplicate labels only in `x_` files, which are not `\input` |
| AC-W8 skeleton | PASS | chapter `inbrief` (= `\paragraph{In brief.}` via preamble l.176) with Why/When/Where/How before first `\section`; `sec:vis-background` first; `sec:vis-apply`, `sec:vis-future` last; titles match 01/02/04 precedent |
| AC-W10 figures | PASS (n/a) | no `\includegraphics` added |
| AC-W12 additions only | PASS | numstat 67 / 0; hunks are pure insertions, no existing body line changed |
| 배경 names deck 5 | PASS | l.34 comment + l.36 `5_StatandVisualization.pptx`; file exists in `notes/` |

## Prerequisite one-liners (배경, l.41-51)

| Line | Claim | Result |
| --- | --- | --- |
| 42-44 | Mean/SD covered in sec:center, sec:spread; sec:ci formula builds on them | PASS (02 l.434, 485; 03 CI eq. uses $\bar x$, $s$, $\sqrt n$) |
| 45-47 | PDF in sec:pmf-pdf; histogram is empirical PDF approximation | PASS (02 l.128; 03 sec:histogram says 경험적 표현) |
| 48-50 | Normal and $z=1.96$ in sec:normal ("다룬다", forward ref) | PASS (04 l.83, l.137 1.96 tied to sec:ci) |

## Content ISSUEs (claims about other chapters)

All are **implementation issues** (writer misstated what the cited chapters say); route to
`sonnet-writer` for rewording (no research needed, the facts are in the cited chapters).

1. **l.543-544, ch:hw1.** Claims HW1 reads burger/nugget calorie distributions "with
   this chapter's tools". `05-hw1-casebook.tex` uses no chart, box plot, histogram,
   error bar or CI (grep = 0); it compares menu types by summary-statistics tables
   (l.108-127, mean/SD/min/max). Those are ch02 tools. The CI burger-vs-nugget
   comparison lives in this chapter (subsec:ci-compare), not in HW1.
2. **l.545-546, ch:hw2.** Says HW2 uses histograms for airport route counts. HW2
   l.147-150 explicitly rejects a histogram for airports and uses a CCDF on log-log
   axes. Ratings (l.155) and age (l.399) histograms are correct.
3. **l.547-549, sec:qq.** Says Q-Q "그대로 이어받아" the ex:quantile rule. It does
   not: ex:quantile uses position $(i-1)/(n-1)$; lec07 uses $p_i = i/(n+1)$ and
   contrasts the two rules in a pitfall (lec07 l.72-73).
4. **l.550-551 and l.563-565, sec:cd-t-two / sec:cd-ks-two.** l.563-565 says comparing
   the *whole distribution* needs the two-sample $t$ test or KS test. The $t$ test
   compares means only (lec11 sec:cd-t-two When: "두 독립 표본의 평균을 비교할 때"),
   so it is the formal version of the CI-overlap check, not a whole-distribution
   method; only KS (sec:cd-ks-two) compares whole distributions. Likewise l.550-551
   calls KS a formalization of CI overlap, which it is not.
5. **l.560-561, misanchor.** "\Cref{pit:sd-se-ci} 뒤에서 던진 ``구간이 겹치면 같은
   것인가''" points to the SD/SE/CI error-bar pitfall (l.262), which does not pose
   that question. The question is the unlabeled pitfall in subsec:ci-compare
   (l.491-496). lec09 l.208 itself anchors it to subsec:ci-compare. The claim that
   ch:hypothesis answers it is true (lec09 l.205-210).

## Bilingual (AC-W5, principle 1) ISSUE

`\term{}` hits in added lines, all bilingual: 요약통계(Summary Statistics),
평균(Mean), 표준편차(Standard Deviation), 확률밀도함수(Probability Density Function,
PDF), 정규분포(Normal Distribution). PASS.

Missing English at introduction sites (In brief and first mention in a section),
**implementation issue**, route to `sonnet-writer`:

- l.7 In brief: 봉우리, 치우침, 이상치 (e.g. Mode/Peak, Skewness, Outlier).
- l.12 In brief: 박스플롯, 이봉분포 (Box Plot, Bimodal Distribution).
- l.15 In brief: 에러바 (Error Bar).
- l.550/564-565: 두 표본 $t$검정, KS검정 (Two-Sample t-Test, Kolmogorov-Smirnov Test).
- l.559: 귀무가설, 유의수준, 기각 규칙 (Null Hypothesis, Significance Level, Rejection Rule).

Precedent: 04's chapter In brief carries English on every named term.

## Minor (no action required)

- In brief Why (l.6-8) and Where (l.11-12) are two sentences each; principle 7 says
  one. 04's chapter In brief does the same, so not raised as ISSUE.

## Routing

Items 1-5 and the bilingual list: `sonnet-writer`, additions/edits limited to lines
3-16 and 535-565 (new lines only; existing body stays untouched per T17).
