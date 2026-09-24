# Archived from PLAN.md §3.0 + §3.1 (2026-09-23): setup + deck 9 pilot, all DONE

> Cold storage (rules/docs.md §3). Live stub: PLAN.md §3.0/§3.1.

### 3.0 Setup

- [x] **T00** main session/owner. DONE DIFFERENTLY (owner directive): the lecture-chapter
  naming rule (`lecNN-slug.tex`, reading order = `parts/*.tex`) now lives in the repo-root
  `CLAUDE.md` (commit 916ed59), NOT in `.claude/rules/writing/book.md`; book.md untouched.
  Original spec: Add a one-line exception to book.md §3:
  "lecture chapters use `lecNN-slug.tex`; reading order is `parts/*.tex`, not
  file sort". In: `.claude/rules/writing/book.md`. Out: same file (`.claude` is a
  submodule, commit separately). Dep: none. Gate: must land before T03 is
  COMMITTED (not before T03 is dispatched; the T03 prompt cites Q1).
  AC: one added line in §3, zero deleted lines; principle 12 unchanged.
- [x] **T01** sonnet-writer. Add the hypothesis-testing row to `tab:analogy`
  (architecture.md §5, exact wording). In: `chapters/00-preface.tex`. Out: same.
  Dep: none. AC: AC-W1, W3, W4, W12; table gains exactly one row; no other line changes.
- [x] **T01r** reviewer. Verify T01. Dep: T01. (`reviews/T01.md`)

### 3.1 Deck 9 pilot → `chapters/lec09-hypothesis-testing.tex` (`ch:hypothesis`)

Spec: architecture.md §3 (fully specified; no addendum needed).

- [x] **T02** developer. `hw1/00_lecture_charts/deck9_hypothesis.py` → `figures/09_01_drug_experiments.png`,
  `09_02_pooled_vs_group.png`, `09_03_puppy_null.png` (+ optional `09_04_alien_null.png`);
  register in `main.py`. In: architecture.md §3.4–3.6, `notes_text/9_*/slides.md`.
  Dep: none, but the `main.py` edit is append-only (one import + one build call);
  the uncommitted 2.3.2 fix pass also touches `main.py`, so do not reformat it.
  AC: script runs in seconds, exits 0, writes the PNGs; values live once in the
  script with slide-source comments; 09_02 panels show 220.83 / 219.33; 09_03
  overlays exact `1000*C(15,k)/2^15`; prints `scipy.stats.binom.sf(55, 400, 0.1)`
  and the value is reported back (feeds R6). No training, no notebook run.
  Result: R6 = binom.sf(55,400,0.1) = 0.006637.
- [x] **T02r** reviewer. Run T02 script once; confirm files + printed R6 value. Dep: T02. (`reviews/T02.md`, PASS)
- [x] **T03** sonnet-writer. Write the chapter + one `\input` line in
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
- [x] **T04** reviewer. Authoritative build + AC check of T03. Out:
  `reviews/lec09.md`. Dep: T03. Verdict: cycle 1 ISSUE (B1–B7), cycle 2 PASS; committed.
  Non-blocking nits left to the owner (PLAN.md backlog X03).
