# HW2 grading checklist

Grading criteria from the professor (pasted 2026-09-30), turned into boxes to tick.
"Where" points at `hw2/report/hw2_taeklim_report.pdf` (item letter, figure number) and the
script in `hw2/code/` that produces it. Tick a box only after you have read that part
yourself and agree with it.

## Submission

- [ ] Word or PDF document with the discussion and the chart screenshots
      (`hw2/report/hw2_taeklim_report.pdf`)
- [ ] Code for partial credit, submitted as separate files (the report no longer has a
      code appendix): `hw2/code/common.py`, `common_p2.py`, the 24 answer scripts,
      `run_all.py`
- [ ] Name on the first page

## Problem 1: 90 points

### Parameters for each distribution: (5 × 4) × 2 = 40

Airport data

- [ ] (a) power law α = 1.612, x_min = 1 (5) — `p1_airport_a_alpha.py`
- [ ] (b) exponential λ = 0.0504 (5) — `p1_airport_b_lambda.py`
- [ ] (c) uniform [a, b] = [1, 915] (5) — `p1_airport_c_uniform.py`
- [ ] (d) normal μ = 19.845, σ = 53.506 (5) — `p1_airport_d_normal.py`

Movie rating data

- [ ] (a) power law α = 1.851, x_min = 1.9 (5) — `p1_movie_a_alpha.py`
- [ ] (b) exponential λ = 0.1606 (5) — `p1_movie_b_lambda.py`
- [ ] (c) uniform [a, b] = [1.9, 8.5] (5) — `p1_movie_c_uniform.py`
- [ ] (d) normal μ = 6.227, σ = 0.893 (5) — `p1_movie_d_normal.py`

### Distribution of data: 5 × 2 = 10

- [ ] Airport (e), Figure 1 (5) — `p1_airport_e_data_plot.py`
- [ ] Movie (e), Figure 6 (5) — `p1_movie_e_data_plot.py`

### Distribution of the hypothetical distribution and final discussion: 20 × 2 = 40

Distribution may be a PDF, CDF or QQ plot.

Airport data (20)

- [ ] (f) power law, Figure 2 — `p1_airport_f_powerlaw_plot.py`
- [ ] (g) exponential, Figure 3 — `p1_airport_g_exponential_plot.py`
- [ ] (h) uniform, Figure 4 — `p1_airport_h_uniform_plot.py`
- [ ] (i) normal, Figure 5 — `p1_airport_i_normal_plot.py`
- [ ] (j) discussion: which distribution and why (KS table) — `p1_airport_j_discussion.py`

Movie rating data (20)

- [ ] (f) power law, Figure 7 — `p1_movie_f_powerlaw_plot.py`
- [ ] (g) exponential, Figure 8 — `p1_movie_g_exponential_plot.py`
- [ ] (h) uniform, Figure 9 — `p1_movie_h_uniform_plot.py`
- [ ] (i) normal, Figure 10 — `p1_movie_i_normal_plot.py`
- [ ] (j) discussion: which distribution and why (KS table) — `p1_movie_j_discussion.py`

## Problem 2: 30 points

"Smallest digit" is the last (ones) digit; "largest digit" is the first (leading) digit.

- [ ] Plot distribution of age (5): Figure 12, with Figure 11 (all ages before the filter)
      and the parsing note above it — `p2_a_age_plot.py`
- [ ] Plot distribution of smallest digit = last digit (5): Figure 14 — `p2_c_last_digit_plot.py`
- [ ] Plot distribution of largest digit = first digit (5): Figure 13 — `p2_b_first_digit_plot.py`
- [ ] Discussion (15): which digit is uniform, is it expected, what the other one follows
      and why (not Benford) — `p2_d_discussion.py`

## Before submitting

- [ ] `uv run python hw2/code/run_all.py` runs without errors from the repo root
- [ ] Rebuild the report (`latexmk -pdf hw2_taeklim_report.tex` in `hw2/report/`) and check
      that every figure, number and caption agree
- [ ] Discussion text is in your own words (course policy on tools; see the Tooling line)
