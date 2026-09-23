# book_intro_2_ds: lecture decks to chapters (PLAN)

> Completed items live in `_archive/` (cold storage — do not read unless
> investigating history). Split detail, if any, is linked from stubs below;
> a stub's state is the truth if it and the detail disagree.

## 1. Decisions

Design input: `research/architecture.md` (system-architect, 2026-09-23). Writer
sources: `notes_text/<deck>/slides.md` + `media/` only.

Owner decisions, 2026-09-23 (recorded verbatim):

- **Q1:** new lecture chapters use `chapters/lecNN-slug.tex` (NN = deck number);
  reading order is set by `parts/*.tex`; existing 01–06 files are NOT renamed.
  book.md §3 needs a one-line exception noting this (task T00, main session/owner).
- **Q2:** when filling existing chapters 01–04 (and 03 for deck 5), add the
  principle-12 skeleton parts (chapter-level In brief, 배경, 어떻게 적용, 앞으로)
  before/after only; existing section bodies untouched.
- **Q3** (default, owner may override): skip deck 1; cite deck 2 slides 9–11
  without a chapter.
- **Q4:** slide errors are SHOWN in the text as pitfall boxes:
  "슬라이드 값은 X, 다시 계산하면 Y".
- **Q5** (default, owner may override): add one hypothesis-testing row to the
  preface analogy table (`tab:analogy`, architecture.md §5).
- **Q6** (default, owner may override): em-dash cleanup of existing titles is a
  separate later task, not mixed into fill work (§7 backlog).
- **Scope:** do ALL of it, sequentially, one chapter at a time: deck 9 pilot first
  (new chapter lec09), then deck 7 (new chapter lec07), then fills of 04 (deck 6),
  01 (deck 3), 02 (deck 4), 03 (deck 5 skeleton only).
- **Figures:** data plots come from Python generators in `hw1/00_lecture_charts/`
  (developer task, must precede the writer task of that chapter); TikZ only for
  flow diagrams.
- **Future decks:** the same pipeline repeats via `tools/extract_slides.py` →
  architect outline → this plan (§6).

Planning consequences (pm, 2026-09-23):

- Owner order overrides architecture.md U3←U2 (lec07 after 04). Cost: when lec07
  is written, `sec:cdf` and `sec:binomial` in 04 are still stubs, so lec07 and
  lec09 background sections self-summarize CDF / binomial (principle 9a). No
  shrink-back pass is scheduled (YAGNI).
- A figure is labelled once, in the first chapter that uses it; later chapters
  `\Cref` it. `06_01_normal_fit.png` therefore gets its label in lec07
  (`fig:normal-fit`), and the 04 fill references it. This deviates from
  architecture.md §4.2 item 4 (figure home = 04): pending architect/owner confirm.
- Architect addenda (A-tasks) precede writers wherever architecture.md lacks a
  §3.3-style slide map, a figure list, or verified numbers.
- The `sec:<prefix>` per chapter: lec09 `ht`, lec07 `qq`, 04 `dist`, 01 `attr`,
  02 `desc`, 03 `vis`.

## 2. Done

- [x] **2.3.2 "부호와 방향"** figures/table/example written and reviewed
  (`reviews/02-skew-sign.md`). A fix pass is in progress outside this plan.
  **No task in this plan edits that subsection** (guarded by AC-W11).

## 3. Chapter requirements and task list

Run strictly in ID order, one task at a time. Every writer/developer task is
followed by its reviewer task before the next chapter opens. "AC-W" = §4, applied
to the task's output file. Paths relative to `book_intro_2_ds/` unless they start
with `hw1/`. Every agent prompt restates: no model training, no notebook
execution, no `rm`, no `git commit`. Reviewer tasks (`T..r`, T04, T07, T10, T13,
T16, T18): In = the reviewed task's Out + its AC list; Out = `reviews/<id>.md`.
A-tasks: In = architecture.md + `notes_text/<deck>/`; Out = architecture.md (append only).

### 3.0 Setup

- [ ] **T00** main session/owner. Add a one-line exception to book.md §3:
  "lecture chapters use `lecNN-slug.tex`; reading order is `parts/*.tex`, not
  file sort". In: `.claude/rules/writing/book.md`. Out: same file (`.claude` is a
  submodule, commit separately). Dep: none. Gate: must land before T03 is
  COMMITTED (not before T03 is dispatched; the T03 prompt cites Q1).
  AC: one added line in §3, zero deleted lines; principle 12 unchanged.
- [ ] **T01** sonnet-writer. Add the hypothesis-testing row to `tab:analogy`
  (architecture.md §5, exact wording). In: `chapters/00-preface.tex`. Out: same.
  Dep: none. AC: AC-W1, W3, W4, W12; table gains exactly one row; no other line changes.
- [ ] **T01r** reviewer. Verify T01. Dep: T01.

### 3.1 Deck 9 pilot → `chapters/lec09-hypothesis-testing.tex` (`ch:hypothesis`)

Spec: architecture.md §3 (fully specified; no addendum needed).

- [ ] **T02** developer. `hw1/00_lecture_charts/deck9_hypothesis.py` → `figures/09_01_drug_experiments.png`,
  `09_02_pooled_vs_group.png`, `09_03_puppy_null.png` (+ optional `09_04_alien_null.png`);
  register in `main.py`. In: architecture.md §3.4–3.6, `notes_text/9_*/slides.md`.
  Dep: none, but the `main.py` edit is append-only (one import + one build call);
  the uncommitted 2.3.2 fix pass also touches `main.py`, so do not reformat it.
  AC: script runs in seconds, exits 0, writes the PNGs; values live once in the
  script with slide-source comments; 09_02 panels show 220.83 / 219.33; 09_03
  overlays exact `1000*C(15,k)/2^15`; prints `scipy.stats.binom.sf(55, 400, 0.1)`
  and the value is reported back (feeds R6). No training, no notebook run.
- [ ] **T02r** reviewer. Run T02 script once; confirm files + printed R6 value. Dep: T02.
- [ ] **T03** sonnet-writer. Write the chapter + one `\input` line in
  `parts/part1-foundations.tex` after `04-distributions`. In: architecture.md §3,
  R6 value from T02, `notes_text/9_*/`. Out: `chapters/lec09-hypothesis-testing.tex`,
  `parts/part1-foundations.tex`. Dep: T01r, T02r (T00 gates commit only).
  AC: AC-W1..W10. Plus:
  - sections/labels exactly as §3.2: `sec:ht-background`, `sec:ht-why`,
    `sec:ht-hypotheses`, `sec:ht-decision`, `sec:ht-forms`, `sec:ht-pvalue`,
    `sec:ht-simulation`, `sec:ht-exact`, `sec:ht-two-groups`, `sec:ht-apply`,
    `sec:ht-future`; examples `ex:ht-puppy`, `ex:ht-juan`, `ex:ht-distance`;
    tables `tab:ht-symbols`, `tab:ht-puppy`, `tab:ht-alien`, `tab:ht-wording`,
    `tab:ht-cases`; figures `fig:ht-flow`, `fig:ht-tails` (TikZ), `fig:ht-drug-experiments`,
    `fig:ht-pooled-vs-group`, `fig:ht-puppy-sim` (PNG).
  - numbers (AC-W6): 1000, 0.003, 121/32768, 0.0037, 0.064, 0.01024, 0.004096,
    6연승, 27.83, 220.83, 219.33, 1.50, 7/1000, $X \ge 56$, 2.58, 2.25; "%50" absent.
  - pitfalls (AC-W7): R4 (table is expected values, not a simulation), R7 (14%
    bin boundary can flip the verdict), R8 (direction chosen after data); plus the
    `p` two-meanings pitfall, 1% vs 5% pitfall, "기각 실패 ≠ 증명" pitfall.
  - background self-summarizes binomial (04 `sec:binomial` is a stub).
  - part1 diff = one added line.
- [ ] **T04** reviewer. Authoritative build + AC check of T03. Out:
  `reviews/lec09.md`. Dep: T03.

### 3.2 Deck 7 → `chapters/lec07-qq-normalization.tex` (`ch:qq-normalization`)

Spec: architecture.md §4.2 (outline only).

- [ ] **A07** system-architect. Append to architecture.md a §4.2 addendum: §3.3-style
  slide map (slides 1–26), §3.4-style recompute table (slide 18 formula restored from
  `media/image46.png` and 6000 / 5700 / 0.035 recomputed; iris discretization
  boundaries; quantile-normalization hand example), figure list (label, file
  `07_0N_*.png`, generator), iris data source, In brief drafts. Out:
  `research/architecture.md` (append only). Dep: T04 PASS.
  AC: every slide 1–26 in the map; every number the slides show has a recompute row
  with verdict; every data figure has a filename.
- [ ] **T05** developer. `hw1/00_lecture_charts/deck7_qq_normalization.py` → the
  A07 figure list; register in `main.py`. Also print the `calories` Shapiro p and
  `sugars` skew before/after log (architecture.md §4.2 item 14). Dep: A07.
  AC: as T02 (runs in seconds, exit 0, all listed PNGs exist, printed values reported back).
- [ ] **T05r** reviewer. Verify T05. Dep: T05.
- [ ] **T06** sonnet-writer. Write the chapter + insert its `\input` line between
  `04-distributions` and `lec09-hypothesis-testing` in part1. In: architecture.md §4.2 + A07, T05 values.
  Out: `chapters/lec07-qq-normalization.tex`, `parts/part1-foundations.tex`. Dep: T05r.
  AC: AC-W1..W10. Plus: labels `sec:qq-background`, `sec:qq-why`,
  `sec:dist-check-hist`, `sec:dist-check-cdf`, `sec:qq`, `sec:qq-two-samples`,
  `sec:discretization`, `sec:normalization`, `sec:quantile-norm`, `sec:robust-scaling`,
  `sec:log-transform`, `sec:impute`, `sec:qq-apply`, `sec:qq-future`;
  `fig:normal-fit` labels `06_01_normal_fit.png` here; background self-summarizes
  CDF; `\log 0` pitfall cites `ex:zero-as-missing`; deck 2 slides 9–11 cited in
  `sec:impute` (Q3); every A07 number and pitfall present.
- [ ] **T07** reviewer. Out: `reviews/lec07.md`. Dep: T06.

### 3.3 Deck 6 → fill `chapters/04-distributions.tex`

Spec: architecture.md §4.3.

- [ ] **A06** system-architect (small; §4.3 already has the recompute values).
  §4.3 addendum: slide map (1–30); whether any new figure beyond existing
  `06_0N_*.png` is needed (list or "none"). Dep: T07 PASS.
- [ ] **T08** developer. Extend `deck6_distributions.py` only for A06-listed figures
  (if "none": print the TODO values 96.0% and Shapiro 0.00038 and report). Dep: A06.
  AC: as T02.
- [ ] **T08r** reviewer. Verify T08. Dep: T08.
- [ ] **T09** sonnet-writer. Fill 04 per §4.3 items 1–9; keep existing labels and
  section order; new `sec:powerlaw` after `sec:exponential`; new `subsec:geometric`
  inside `sec:exponential`; `sec:cdf` does not redefine CDF (points to 02, see A02).
  Out: `chapters/04-distributions.tex`. Dep: T08r.
  AC: AC-W1..W12 (W12 allows deleting `\todo`/TODO lines only). Numbers: 0.4512,
  6분, 0.5654, 0.0801, 0.0800, 0.05, 0.0475, 0.045125, 0.04877, 0.04639, 0.04413,
  1/15, 95.45%, 1.96, 0.24, 0.3125. Pitfalls: 0.0801 → 0.5654; "$0<\lambda\le 1$" →
  "$\lambda > 0$"; ±2 SD = 95.45% not 95%. Geometric vs exact shown as a two-column
  table (approximation, not an error). `fig:normal-fit` referenced, not re-labelled.
- [ ] **T10** reviewer. Out: `reviews/04-fill.md`. Dep: T09.

### 3.4 Deck 3 → fill `chapters/01-data-attributes.tex`

Spec: architecture.md §4.1.

- [ ] **A03** system-architect (small). §4.1 addendum: slide map (1–20); confirm the 3D
  scatter is schematic (TikZ) or list a data figure. Dep: T10 PASS.
- [ ] **T11** developer (only if A03 lists a data figure; else mark `[x]` "n/a").
  In: A03 figure list. Out: `hw1/00_lecture_charts/deck3_data_matrix.py` + PNGs.
  Dep: A03. AC: as T02.
- [ ] **T12** sonnet-writer. Fill 01 per §4.1 items 1–8. Out: `chapters/01-data-attributes.tex`.
  Dep: A03 (and T11 reviewed, if it ran).
  AC: AC-W1..W12. Labels `sec:attr-background`, `sec:attr-discrete`, `sec:data-matrix`,
  `sec:dimension`, `sec:vector`, `sec:everything-matrix`, `sec:attr-apply`,
  `sec:attr-future`; 2×2 table (scale × discrete/continuous); slide-4 answers
  명목, 구간, 순서, 비율, 명목; pitfall on slide 8 vs 11 identifier-column count.
- [ ] **T13** reviewer. Out: `reviews/01-fill.md`. Dep: T12.

### 3.5 Deck 4 → fill `chapters/02-descriptive-statistics.tex`

Spec: architecture.md U5 (one line only). Blocked on A04.

- [ ] **A04** system-architect. Full outline for deck 4 slides 4–11, 19, 20
  (random variable, PMF, PDF, CDF definition, dice example, $P(X>3)=0.6$, mode
  resistance, range): section labels (CDF definition label, not `sec:cdf`), slide
  map 1–23, recompute table, figure list, placement relative to existing sections
  and outside 2.3.2. Dep: T13 PASS.
- [ ] **T14** developer. Figures from A04 (e.g. dice PMF/CDF) in
  `deck4_basic_stats.py`. Dep: A04. AC: as T02.
- [ ] **T14r** reviewer. Verify T14. Dep: T14.
- [ ] **T15** sonnet-writer. Fill 02 per A04. Out: `chapters/02-descriptive-statistics.tex`.
  Dep: T14r. AC: AC-W1..W12; AC-W11 (no hunk inside 2.3.2); every A04 number present;
  04 `sec:cdf` now resolves to this chapter's CDF definition via `\Cref`.
- [ ] **T16** reviewer. Out: `reviews/02-fill.md`. Dep: T15.

### 3.6 Deck 5 → skeleton retrofit `chapters/03-visualization.tex`

- [ ] **A05** system-architect (optional; skip if the main session judges the
  §1 coverage row enough). Slide map 2–27 → existing labels. Dep: T16 PASS.
- [ ] **T17** sonnet-writer. Add the four skeleton parts only: chapter In brief,
  배경 (deck 5 source, prerequisites + `\Cref`), 어떻게 적용, 앞으로 (links
  `ch:hypothesis` for the 5% rule). In: `notes_text/5_*/`, architecture.md §1.
  Out: `chapters/03-visualization.tex`. Dep: T16 (and A05 if run). AC: AC-W1..W5, W8, W10, W12 (zero deleted lines); no existing section
  body line changed.
- [ ] **T18** reviewer. Out: `reviews/03-skeleton.md`. Dep: T17.

## 4. Common acceptance criteria (AC-W)

`F` = the task's output `.tex`. "Added lines" = `git diff -U0 -- F | grep '^+[^+]'`
for tracked files, all lines of F for a new file. Comment lines (`^\s*%`) excluded
unless stated.

- **AC-W1 build:** `latexmk -xelatex main.tex` in `book_intro_2_ds/` exits 0.
- **AC-W2 refs:** `grep -cE "undefined|multiply defined" main.log` = 0.
- **AC-W3 no em dash:** added lines, `grep -cE '—|---'` = 0 (en dash `--` in ranges allowed).
- **AC-W4 `\Cref` only:** added lines, `grep -cE '\\(ref|autoref|cref)\{'` = 0;
  no hard-coded chapter numbers (`grep -cE '[0-9]+ ?장|Chapter [0-9]'` = 0).
- **AC-W5 bilingual:** every term introduced in added lines (`\term{}`, definition,
  table header/cell, caption, list heading, In brief) carries Korean + (English)
  per book.md principle 1. Reviewer lists each `\term{` hit with its English.
- **AC-W6 numbers:** every number listed in the task (and every row of the
  architecture.md recompute table for that deck) appears in F with the recomputed
  value; no slide value appears as fact where the table says it is wrong.
- **AC-W7 slide-error pitfalls (Q4):** each slide error listed in the task sits
  inside a `pitfall` env, in the form "슬라이드 값은 X, 다시 계산하면 Y".
- **AC-W8 skeleton:** chapter-level `\paragraph{In brief.}` (Why/When/Where/How)
  before the first `\section`; then `sec:<p>-background`, why, what sections,
  `sec:<p>-apply`, `sec:<p>-future`, in that order (fills: why/what are the
  existing sections). Every new concept section opens with In brief.
- **AC-W9 slide coverage:** each section carries `% source: deck N slide K[-L]`
  comments; the union covers every slide of the deck's map, or the map row says
  "내용 없음". In fills, the writer adds comment-only `% source:` lines inside
  existing sections (additions, so W12 holds; bodies unchanged).
- **AC-W10 figures:** every `\includegraphics` target exists in
  `hw1/00_lecture_charts/figures/` and its developer task is `[x]` before the
  writer is dispatched; data plots are PNG from a script, TikZ only for flow/schematic
  diagrams; captions in Korean; each figure/table has `\caption` + `\label` and is
  `\Cref`'d in text.
- **AC-W11 2.3.2 guard:** no diff hunk in `02-descriptive-statistics.tex` falls
  between `\subsection{부호와 방향}` and the next `\subsection`/`\section`.
- **AC-W12 additions only:** `git diff --numstat -- F` deletions = 0, except lines
  a task explicitly allows (e.g. `\todo`/TODO stubs in 04).

## 5. Exit criteria per chapter

A chapter is DONE only when all hold (a merged diff is not enough):

1. Its reviewer task is `[x]` with verdict PASS in `reviews/<chapter>.md`.
2. AC-W1/W2 re-run by the reviewer on the final tree, and the chapter's pages
   render in `main.pdf` in the order set by `parts/part1-foundations.tex`.
3. Every slide of the deck is mapped (AC-W9) and every recompute row is honored (AC-W6, W7).
4. Figures regenerate from `python hw1/00_lecture_charts/main.py` without manual steps.
5. `STATUS.md` has the closing line. The next chapter's first task opens only after this.

## 6. How to add a new deck

1. Main session: `python tools/extract_slides.py` → `notes_text/<deck>/slides.md` + `media/`.
2. system-architect: append to architecture.md a coverage row (§1), outline in the
   §3 shape (In brief drafts, slide map, recompute table, figure list, `\Cref` targets
   verified to exist), and any owner questions.
3. product-manager: add a §3.x block here: A (if gaps) → developer figures →
   developer review → sonnet-writer → reviewer, with deck-specific AC-W6/W7 lists.
4. New chapter: `chapters/lecNN-slug.tex`, `\input` in `parts/` by deck number.
   Existing chapter: fill per Q2 (skeleton before/after, bodies untouched).

## 7. Backlog (not scheduled)

- [ ] **X01** (Q6 default) em-dash cleanup of existing chapter titles/bodies,
  separate diff, never mixed with fill tasks. Needs owner go-ahead.
- [ ] **X02** decks 1 and 2: no chapter (Q3 default). Revisit only if owner overrides.
