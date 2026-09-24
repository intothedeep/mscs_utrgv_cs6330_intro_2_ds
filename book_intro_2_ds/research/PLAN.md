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

Owner decisions on decks 10 and 11, 2026-09-23 (recorded verbatim; design input
architecture.md §7):

- **Q7:** KS definition stays where it is in each place (HW2 chapter and appendix keep their own explanations; lec11 also defines KS). Duplication accepted by owner. So architecture.md §7's "KS defined only in lec11 / appendix KS part loses effect" is overridden: no task edits the appendix or HW2 KS text.
- **Q8:** YES, add one forward \Cref line each in the reviewed chapters lec09, 03, hw02 pointing to the new chapters; bodies untouched (additions only, one line each).
- **Q9:** NO, do not convert HW2's D to p-values.
- **Q10:** already decided by Q4: show slide value and recomputed value (pitfall "슬라이드 값은 X, 다시 계산하면 Y").
- **Q11:** two-sample t-test: text follows the slide's formula; a pitfall box shows the Welch degrees-of-freedom result (scipy equal_var=False) side by side (0.020 vs 0.024 per architecture; confirm in the figure script).
- **Order:** decks 10 and 11 run BEFORE the remaining deck 7 and 04/01/02/03 fill tasks (follow the lecture schedule). Do not delete or renumber existing tasks; insert the new blocks so the execution order is clear.

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
  02 `desc`, 03 `vis`, lec10 `pv`, lec11 `cd`.
- T00 closed differently: the naming rule of Q1 lives in the repo-root `CLAUDE.md`
  (owner directive, commit 916ed59), not in book.md. Q1 itself stands.
- Q7 voids architecture.md §7.2 decision 5 and the §7.6 "U2 (범위 변경)" row: T09's AC is
  unchanged; no task edits 04 `sec:cdf`/`sec:normal` KS text or hw02 KS text. lec11 still
  owns `def:ks-statistic` (one definition inside lec11; other chapters keep theirs).
- The Order decision supersedes the Scope line's "then deck 7" (Scope kept verbatim above).
  Execution order: §3.1a → §3.1b → §3.1c → §3.2 → … → §3.6.
- Q8 links are NEW source lines, not parentheticals appended to existing sentences
  (architecture §7.5 Q8 "괄호 안 링크만 덧붙인다" would show a deletion in numstat).

## 2. Done

- [x] **2.3.2 "부호와 방향"** figures/table/example written and reviewed
  (`reviews/02-skew-sign.md`). A fix pass is in progress outside this plan.
  **No task in this plan edits that subsection** (guarded by AC-W11).
- [x] **H02** HW2 chapter `chapters/hw02-data-distributions.tex` (+ one `\input` in
  `parts/part2-practice.tex`) written; `reviews/hw02.md` PASS in cycle 2; committed.
  Not in the original plan; added closed. Non-blocking leftovers → backlog X04.

## 3. Chapter requirements and task list

Run strictly in block order 3.0 → 3.1 → 3.1a → 3.1b → 3.1c → 3.2 → 3.3 → 3.4 →
3.5 → 3.6, IDs in order inside a block, one task at a time (T19–T26 run before A07:
owner Order, 2026-09-23). Every writer/developer task is
followed by its reviewer task before the next chapter opens. "AC-W" = §4, applied
to the task's output file. Paths relative to `book_intro_2_ds/` unless they start
with `hw1/`. Every agent prompt restates: no model training, no notebook
execution, no `rm`, no `git commit`. Reviewer tasks (`T..r`, T04, T07, T10, T13,
T16, T18, T21, T24, T26): In = the reviewed task's Out + its AC list; Out = `reviews/<id>.md`.
A-tasks: In = architecture.md + `notes_text/<deck>/`; Out = architecture.md (append only).

### 3.0 Setup: DONE (2026-09-23)

> [x] T00 (done differently: rule in repo-root `CLAUDE.md`, not book.md), [x] T01
> (`tab:analogy` row), [x] T01r. <!-- ARCHIVE: history-only -->
> Detail: [_archive/lec09-pilot.md](./_archive/lec09-pilot.md)

### 3.1 Deck 9 pilot → `lec09-hypothesis-testing.tex`: DONE (2026-09-23)

> [x] T02 (R6 = `binom.sf(55,400,0.1)` = 0.006637), [x] T02r, [x] T03, [x] T04
> (`reviews/lec09.md` PASS cycle 2; committed). <!-- ARCHIVE: history-only -->
> Detail: [_archive/lec09-pilot.md](./_archive/lec09-pilot.md)

### 3.1a Deck 10 → `lec10-p-value.tex`: DONE (2026-09-23)

> [x] T19, [x] T19r (`reviews/T19.md`; architecture.md §7.x: vitamin D mean = 63),
> [x] T20, [x] T21 (`reviews/lec10.md` PASS cycle 2; committed). <!-- ARCHIVE: history-only -->
> Detail: [_archive/lec10-lec11.md](./_archive/lec10-lec11.md)

### 3.1b Deck 11 → `lec11-comparing-distributions.tex`: DONE (2026-09-23)

> [x] T22, [x] T22r (`reviews/T22.md`; architecture.md §7.y: KS two-sample asymptotic
> p 0.0815, critical 0.645; exact p 0.0499 → E7 기각), [x] T23, [x] T24
> (`reviews/lec11.md` PASS cycle 2; leftovers fixed by main session; committed). <!-- ARCHIVE: history-only -->
> Detail: [_archive/lec10-lec11.md](./_archive/lec10-lec11.md)

### 3.1c Q8 forward links → lec09, 03, hw02: DONE (2026-09-23)

> [x] T25 (main session: one-line `\Cref` in each file, numstat 1/0 each), [x] T26
> (closed differently: main-session numstat + clean build, no reviewer dispatch). <!-- ARCHIVE: history-only -->
> Detail: [_archive/lec10-lec11.md](./_archive/lec10-lec11.md)

### 3.2 Deck 7 → `chapters/lec07-qq-normalization.tex` (`ch:qq-normalization`)

Spec: architecture.md §4.2 (outline only).

- [ ] **A07** system-architect. Append to architecture.md a §4.2 addendum: §3.3-style
  slide map (slides 1–26), §3.4-style recompute table (slide 18 formula restored from
  `media/image46.png` and 6000 / 5700 / 0.035 recomputed; iris discretization
  boundaries; quantile-normalization hand example), figure list (label, file
  `07_0N_*.png`, generator), iris data source, In brief drafts. Out:
  `research/architecture.md` (append only). Dep: T26 PASS (was T04; owner Order 2026-09-23).
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
- [ ] **X03** lec09 non-blocking nits (`reviews/lec09.md` cycle 2 "Non-blocking": N2
  "1.2--1.5%", doubled subject l.455-457, $np=40$ order, 기댓값 wording). Owner decides.
- [ ] **X04** hw02 non-blocking leftovers (`reviews/hw02.md` cycle 2: I partial, N1–N3).
  Owner decides.
