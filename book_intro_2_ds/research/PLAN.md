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
- [x] **H03** HW2 P2 age-rule update (2026-09-23, professor's instruction via owner):
  age = 2026 − birth year, two-digit years stay 19yy, keep 1 ≤ age ≤ 100; 453,905 rows
  kept (was 458,015). Code, figures, `hw2/report` and the book HW2 chapter updated
  (commit 4551718). `hw2/report_submit/` is the owner's own template, not touched.
  Out of plan; added closed.

## 3. Chapter requirements and task list

Run strictly in block order 3.0 → 3.1 → 3.1a → 3.1b → 3.1c → 3.2 → 3.2a → 3.3 → 3.4 →
3.5 → 3.6, IDs in order inside a block, one task at a time (T19–T26 run before A07:
owner Order, 2026-09-23; T27 runs before A06). Every writer/developer task is
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

### 3.2 Deck 7 → `lec07-qq-normalization.tex`: DONE (2026-09-24)

> [x] A07 (architecture.md §8 + §8.z Q12–Q16), [x] T05, [x] T05r (`reviews/T05.md`,
> cycle-2 fixes; scikit-learn in uv env for `load_iris` only, Q13), [x] T06, [x] T07
> (`reviews/lec07.md` PASS cycle 2; minor items fixed by main session). <!-- ARCHIVE: history-only -->
> Detail: [_archive/lec07.md](./_archive/lec07.md)

### 3.2a Q14 forward links → lec07 (lec09, lec11, hw02): DONE (2026-09-24)

> [x] T27 (main session: one new `\Cref{sec:qq}` line each in lec09, lec11, hw02). <!-- ARCHIVE: history-only -->
> Detail: [_archive/fills-04-01-02-03.md](./_archive/fills-04-01-02-03.md)

### Architect addenda: separate files (2026-09-24)

A06, A03 and A04 were written as separate files instead of appending to
architecture.md (the §3 header's "Out = architecture.md (append only)"), because
three architects ran in parallel. Each carries its own decision record:
[arch-deck6.md](./arch-deck6.md) (deck 6), [arch-deck3.md](./arch-deck3.md) (deck 3),
[arch-deck4.md](./arch-deck4.md) (deck 4).

### 3.3 Deck 6 → fill `chapters/04-distributions.tex`: DONE (2026-09-24)

> [x] A06 (`arch-deck6.md`), [x] T08, [x] T08r (`reviews/T08.md`), [x] T09, [x] T10
> (`reviews/04-fill.md` PASS cycle 2; commit ea5da8d). <!-- ARCHIVE: history-only -->
> Detail: [_archive/fills-04-01-02-03.md](./_archive/fills-04-01-02-03.md)

### 3.4 Deck 3 → fill `chapters/01-data-attributes.tex`: DONE (2026-09-24)

> [x] A03 (`arch-deck3.md`), [x] T11, [x] T11r (`reviews/T11.md`), [x] T12, [x] T13
> (`reviews/01-fill.md`; cycle-2 leftovers fixed by main session; commit ac3102d). <!-- ARCHIVE: history-only -->
> Detail: [_archive/fills-04-01-02-03.md](./_archive/fills-04-01-02-03.md)

### 3.5 Deck 4 → fill `chapters/02-descriptive-statistics.tex`: DONE (2026-09-24)

> [x] A04 (`arch-deck4.md`), [x] T14, [x] T14r (`reviews/T14.md`), [x] T15, [x] T16
> (`reviews/02-fill.md`; cycle-2 leftover fixed by main session; commit a20b2b0). <!-- ARCHIVE: history-only -->
> Detail: [_archive/fills-04-01-02-03.md](./_archive/fills-04-01-02-03.md)

### 3.6 Deck 5 → skeleton retrofit `chapters/03-visualization.tex`: DONE (2026-09-24)

> [x] A05 skipped (architecture.md §1 coverage judged sufficient), [x] T17, [x] T18
> (`reviews/03-skeleton.md`; cycle-2 fix, then main session corrected a burger/milkshake
> description; commit 74d241c). <!-- ARCHIVE: history-only -->
> Detail: [_archive/fills-04-01-02-03.md](./_archive/fills-04-01-02-03.md)

### Out of plan, closed (2026-09-24)

- [x] Slide media filenames leaking into reader text removed from lec07, lec09,
  lec10, lec11 (commit ccdb0da).

### Schedule state (2026-09-24)

No scheduled task remains: every §3 block is DONE. Only §7 backlog items are
open (X01–X04), and each needs an owner decision before it is scheduled.

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
