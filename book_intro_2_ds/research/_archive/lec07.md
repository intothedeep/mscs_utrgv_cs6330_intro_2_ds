# Archived from PLAN.md §3.2 (2026-09-24): deck 7 → lec07, DONE

Closing notes (pm, 2026-09-24):

- A07: architecture.md §8 (§4.2 addendum: slide map, recompute table, figure list,
  iris source, In brief drafts) + §8.z decision record (Q12–Q16, 2026-09-23).
- T05/T05r: deck 7 figures from `hw1/00_lecture_charts/deck7_qq_normalization.py`;
  `reviews/T05.md`, cycle-2 fixes applied. `scikit-learn` added to the uv env for
  `sklearn.datasets.load_iris()` only, no training (owner decision Q13, overriding the
  architect's recommended option (b)).
- T06/T07: `chapters/lec07-qq-normalization.tex` + part1 `\input` line;
  `reviews/lec07.md` PASS cycle 2; last minor items fixed by the main session.
- Q14 (forward links lec09/lec11/hw02 → lec07) decided YES in §8.z; carried as a new
  open task T27 in PLAN.md §3.2a (not part of this archive).

---

### 3.2 Deck 7 → `chapters/lec07-qq-normalization.tex` (`ch:qq-normalization`)

Spec: architecture.md §4.2 (outline only).

- [x] **A07** system-architect. Append to architecture.md a §4.2 addendum: §3.3-style
  slide map (slides 1–26), §3.4-style recompute table (slide 18 formula restored from
  `media/image46.png` and 6000 / 5700 / 0.035 recomputed; iris discretization
  boundaries; quantile-normalization hand example), figure list (label, file
  `07_0N_*.png`, generator), iris data source, In brief drafts. Out:
  `research/architecture.md` (append only). Dep: T26 PASS (was T04; owner Order 2026-09-23).
  AC: every slide 1–26 in the map; every number the slides show has a recompute row
  with verdict; every data figure has a filename.
- [x] **T05** developer. `hw1/00_lecture_charts/deck7_qq_normalization.py` → the
  A07 figure list; register in `main.py`. Also print the `calories` Shapiro p and
  `sugars` skew before/after log (architecture.md §4.2 item 14). Dep: A07.
  AC: as T02 (runs in seconds, exit 0, all listed PNGs exist, printed values reported back).
- [x] **T05r** reviewer. Verify T05. Dep: T05.
- [x] **T06** sonnet-writer. Write the chapter + insert its `\input` line between
  `04-distributions` and `lec09-hypothesis-testing` in part1. In: architecture.md §4.2 + A07, T05 values.
  Out: `chapters/lec07-qq-normalization.tex`, `parts/part1-foundations.tex`. Dep: T05r.
  AC: AC-W1..W10. Plus: labels `sec:qq-background`, `sec:qq-why`,
  `sec:dist-check-hist`, `sec:dist-check-cdf`, `sec:qq`, `sec:qq-two-samples`,
  `sec:discretization`, `sec:normalization`, `sec:quantile-norm`, `sec:robust-scaling`,
  `sec:log-transform`, `sec:impute`, `sec:qq-apply`, `sec:qq-future`;
  `fig:normal-fit` labels `06_01_normal_fit.png` here; background self-summarizes
  CDF; `\log 0` pitfall cites `ex:zero-as-missing`; deck 2 slides 9–11 cited in
  `sec:impute` (Q3); every A07 number and pitfall present.
- [x] **T07** reviewer. Out: `reviews/lec07.md`. Dep: T06.
