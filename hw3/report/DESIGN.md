# HW3 report design: YouTube comments, word clouds, comparison

Status: design only. The report and its LaTeX do not exist yet.
Mission block: none. There is no `hw3/PLAN.md` (`rules/docs.md` §0.1). See Q1 in §6.
The A/B/C architecture template does not apply: this is a document design, not a system.

Sources read for this design (all numbers below come from these files):

| Short name | File |
| --- | --- |
| assignment | `hw3/00_doc/hw3_introduction.txt`, `hw3/00_doc/Homework_1_.pdf`, `hw3/00_doc/Homework_YoutubeVideo_1__1_.R` |
| checklist | `hw3/grading_checklist.md` |
| videos | `hw3/data/videos.csv` |
| terms | `hw3/data/terms_<video_a/video_b>_<en/non_en/mixed>.csv` |
| comments | `hw3/data/comments_<label>_all.csv`, `hw3/data/comments_<label>.csv` (not in git, hold handles) |
| clouds | `hw3/figures/wordcloud_video_<a/b>_<en/non_en/mixed>.png`, `hw3/figures/wordcloud_grid.png` |
| code | `hw3/code/{common,p1_collect,p2_wordcloud,p3_compare,run_all}.py` |
| format model | `hw2/report/hw2_taeklim_report.tex` (filled), `hw2/report_submit/hw2_taeklim_report.tex` (step template) |

---

## 1. Section outline

```
page 1  Header line + Tooling line
  |
  S1 Data collection ........ "screenshots of the data"   T1 pipeline, T2 stats, T3 sample, T4a/T4b first comments
  |
  S2 Text cleaning and language split ..... method       T5 cleaning steps
  |
  S3 Video A word clouds ............ 30 pts            F1 F2 F3
  S4 Video B word clouds ............ 30 pts            F4 F5 F6
  |
  S5 Comparison (results) ........... feeds 20 pts      F7 grid, T6 engagement, T7 top terms, T8 shared/distinct
  |
  S6 Discussion ..................... 20 pts            owner's words only (book.md principle 13)
  |
  S7 Limits of the method
```

| # | Section | Purpose | Checklist items covered | Figures and tables |
| --- | --- | --- | --- | --- |
| 0 | Header (page 1) | Name, course, homework title. Same right-aligned line as hw2 (`\hfill Taek Lim \quad CS 6330 Homework 3: ...`). One "Tooling" line as in hw2. | Submission: "Name on the first page" | none |
| 1 | Data collection | Show which videos, how the comments were fetched, and the first rows of the data. This is the "screenshot of the data". | Submission: "screenshots of the data and result" (stats, details, first comments); "Own YouTube API credentials used"; Discussion: "State the collection limits"; "State the sample" | T1, T2, T3, T4a, T4b |
| 2 | Text cleaning and language split | State how a comment becomes terms, and how the English / non-English split is made. | Discussion: "State the language split"; "State the cleaning" | T5 |
| 3 | Video A word clouds | The three clouds of BTS 'Dynamite'. | Word clouds: "Video A comments collected and word clouds" | F1 `hw3/figures/wordcloud_video_a_en.png`, F2 `..._video_a_non_en.png`, F3 `..._video_a_mixed.png` |
| 4 | Video B word clouds | The three clouds of BLACKPINK 'Kill This Love'. | Word clouds: "Video B comments collected and word clouds" | F4 `hw3/figures/wordcloud_video_b_en.png`, F5 `..._video_b_non_en.png`, F6 `..._video_b_mixed.png` |
| 5 | Comparison (results) | Put the two videos side by side: engagement, top terms, shared and distinctive terms per version. Tables only, no opinion. | Discussion: "Compare the two videos" | F7 `hw3/figures/wordcloud_grid.png`, T6, T7, T8 |
| 6 | Discussion | The owner's comparison and interpretation. Placeholders (`\todo{}`) until the owner gives the text. §4(b) lists the questions. | Discussion: "Compare the two videos" (the 20-point text) | none (cites F1 to F7, T6 to T8 by number) |
| 7 | Limits | One short list: top-level only, sample order, English stopwords only, detector errors. | Discussion: "State the collection limits"; "State the limits of the non-English cloud" | none |

Notes on the figures:

- Each cloud PNG is 1200 x 800 (`p2_wordcloud.make_cloud`). Place each at `\linewidth`, one per figure, as `\answerfig` does in hw2. Three clouds of one video fit on about two pages.
- The figure caption states the comment count. The counts are in the grid titles of `wordcloud_grid.png` and follow from `videos.csv` (see §4(a) A3). The table script (M1) must write them, so the caption does not copy them by hand.
- Every figure and table gets a number and a caption (`rules/visualization.md` §3). Floats use `[H]` (`rules/writing/latex.md` §14).

---

## 2. Table designs

All tables use booktabs with `\midrule` between every row (`rules/writing/latex.md` §8). Every table body is written by a script (M1), never typed by hand.

### T1 Pipeline (S1)

The method flow, R step next to the Python step (`rules/visualization.md` §4).

| Columns | step, R function (assignment script), Python script and function, output file |
| --- | --- |
| Source | `hw3/code/*.py` docstrings, `Homework_YoutubeVideo_1__1_.R`. Static text, no numbers. |
| Rows | 1. stats and details: `get_stats`, `get_video_details` -> `p1_collect.fetch_video` -> `data/videos.csv`. 2. comments: `get_comment_threads`, `write.csv` -> `p1_collect.fetch_comments` -> `data/comments_<label>_all.csv`, `data/comments_<label>.csv`. 3. terms: `Corpus`, `DocumentTermMatrix`, `colSums` -> `common.clean_terms`, `common.count_terms` -> `data/terms_<label>_<version>.csv`. 4. cloud: `wordcloud` -> `p2_wordcloud.make_cloud` -> `figures/wordcloud_*.png`. 5. compare: none in R -> `p3_compare.py` -> (today stdout only, see M2). |

This table is the only table that may be static text in the `.tex`. It holds no numbers.

### T2 Video statistics and details (S1)

| Columns | row label, video A, video B |
| --- | --- |
| Source | `hw3/data/videos.csv` |
| Rows | title, channel, video ID, published (date), views, likes, comments (YouTube total), comments fetched, English comments kept, as-of date (missing, see M5) |

Transposed (one column per video) so long titles fit. Numbers with thousands separators.
The title of video A holds Hangul (`BTS (방탄소년단) 'Dynamite' Official MV`, `videos.csv`). See Q4 on the engine.

### T3 Sample composition (S1)

| Columns | video, order (relevance / time), English, non-English with a language, no language (emoji or links only), total |
| --- | --- |
| Source | `hw3/data/comments_<label>_all.csv`, columns `order` and `lang` |
| Rows | per video: relevance row, time row, total row |

These counts are in no saved file today. `p1_collect.py` printed "English by order" and "languages" but did not save them. See M3.

### T4a, T4b First comments, one table per video (S1)

This is the "screenshot of the data" without handles.

| Columns | #, order, published (date), likes, replies, lang, comment text (masked, cut) |
| --- | --- |
| Source | `hw3/data/comments_<label>_all.csv`, first N rows in file order (the fetch order, relevance first) |
| Dropped columns | `author` (the handle), `comment_id` (links to the account's comment) |
| Text rules | replace every `@\S+` with `@user`; cut to about 120 characters plus "..."; strip emoji (fonts do not draw them); escape LaTeX special characters |
| Rows | N = 5 per video (Q3) |

A real screenshot of the CSV would show the `author` column. A rendered table with the column removed meets "screenshot of the data" and hides the handles. See Q2.

### T5 Cleaning steps (S2)

| Columns | step, what it does, why (tm equivalent) |
| --- | --- |
| Source | `common.clean_terms`, `common.detect_language`, `common.TM_STOPWORDS`, `common.MIN_WORD_LENGTH`, `common.LANGUAGES` |
| Rows | 1. language: lingua over the 20 languages in `common.LANGUAGES`, URLs and @mentions removed first, no words gives "" (goes to non-English). 2. lowercase. 3. drop punctuation, numbers, emoji; keep letters of every script. 4. drop tm English stopwords. 5. drop words under 3 letters (`MIN_WORD_LENGTH = 3`). 6. no stemming (the R script loads SnowballC but never calls it). 7. cloud: top 150 words (`p2_wordcloud.MAX_WORDS`), fixed seed (`common.SEED`). |

Static text. Constants should be read from the code by the script, so a code change updates the table.

### T6 Engagement (S5)

| Columns | measure, video A, video B |
| --- | --- |
| Source | `hw3/data/videos.csv`, ratios as `p3_compare.py` defines them |
| Rows | likes per 1k views, comments per 1k views, share of comments fetched (`comments_collected / comment_count` in `p3_compare.py`) |

The ratios are in no saved file. `p3_compare.py` prints them only. See M2. Do not compute them by hand.
Note: `p3_compare.share_collected` divides English comments kept by the total. The checklist says "fetched vs total". Q6 asks which one the report shows.

### T7 Top terms (S5)

| Columns | rank, then for each video: term, count |
| --- | --- |
| Source | `hw3/data/terms_<label>_<version>.csv` |
| Rows | top 10 per version; three sub-tables or three panels: English, non-English, mixed |

### T8 Shared and distinctive top terms (S5)

| Columns | version, top-30 terms in both, only in video A, only in video B |
| --- | --- |
| Source | `p3_compare.top_terms` over `hw3/data/terms_*.csv`, `TOP_N = 30` |
| Rows | one row per version (3 rows) |

The lists are printed only. See M2.

---

## 3. File layout and build path

Copy of the hw2 setup (`hw2/report/`): one `.tex` file, figures by relative path `../figures/`, the PDF committed (`.gitignore` line 78: "The compiled report PDF IS committed"), `hw*/report/*.log` ignored (`.gitignore` line 91).

```
hw3/
  code/
    p1_collect.py  p2_wordcloud.py  p3_compare.py  run_all.py   (exist)
    p4_report_tables.py                                          (missing, M1)
  data/      videos.csv, terms_*.csv (exist); compare_*.csv (missing, M2/M3)
  figures/   wordcloud_*.png (exist)
  report/
    DESIGN.md                    this file
    hw3_taeklim_report.tex       the report (missing, sonnet-writer's job)
    hw3_taeklim_report.pdf       build output, committed
    tables/                      generated by M1, \input by the .tex
      stats.tex  sample.tex  first_comments_video_a.tex  first_comments_video_b.tex
      engagement.tex  top_terms_<en|non_en|mixed>.tex  shared_terms.tex
```

Preamble: as `hw2/report/hw2_taeklim_report.tex` lines 13 to 53 (geometry 0.75in, booktabs, graphicx, caption, enumitem, `\answerfig`, `\answer`). Add `float` for `[H]`.

Build (from `hw3/report/`, do not run now):

```
latexmk -C
latexmk -xelatex hw3_taeklim_report.tex
```

- `latexmk -C` first: `rules/writing/latex.md` §12.
- `-xelatex`, not hw2's `-pdf`: the title of video A holds Hangul, and the non-English term tables may hold Hangul, Thai and kana (visible in F2, F5). pdfLaTeX with `inputenc` cannot set them. XeLaTeX with `fontspec` and `xeCJK` (`rules/writing/latex.md` §1, §2) can. Q4 asks the owner to confirm this break from hw2.
- Data step before the build: `uv run python hw3/code/p4_report_tables.py` (after M1 and M2 exist). It reads saved CSVs only, so it is a "light job" under `~/.claude/CLAUDE.md` "Allowed locally" (one core, `timeout 300`). The main session runs it, not an agent. It must not call the API or `p1_collect.py`.

---

## 4. Discussion points

### (a) Facts the data shows

| # | Fact | Source |
| --- | --- | --- |
| A1 | Views: video A 2,146,874,108; video B 2,243,728,665. | `data/videos.csv` `view_count` |
| A2 | Likes: video A 39,661,294; video B 26,742,200. Comments (YouTube total): video A 15,898,150; video B 2,500,163. | `data/videos.csv` `like_count`, `comment_count` |
| A3 | Fetched top-level comments: video A 1,965; video B 2,127. English kept: 1,000 each. The grid titles show non-English 965 (A) and 1,127 (B). | `data/videos.csv` `comments_fetched`, `comments_collected`; `figures/wordcloud_grid.png` titles |
| A4 | Published: video A 2020-08-21; video B 2019-04-04. | `data/videos.csv` `published_at` |
| A5 | English top term is the group name: `bts` 262 (A), `blackpink` 351 (B). | `data/terms_video_a_en.csv`, `data/terms_video_b_en.csv` row 1 |
| A6 | `love` is the second English term in both: 148 (A), 207 (B). | same files, row 2 |
| A7 | Fandom names rank high in English: `army` 88, `armys` 64 (A); `blinks` 77, `blink` 49 (B). | same files |
| A8 | Member names: video B English has `lisa` 45, `jisoo` 39, `jennie` 35, `rose` 27, `rosé` 19. Video A English top 30 has `jungkook` 25. | same files |
| A9 | The same name splits into two terms: `rose` 27 and `rosé` 19 (B English). Cleaning keeps accents and does not merge them. | `data/terms_video_b_en.csv`; `common.clean_terms` |
| A10 | Video B English has `anniversary` 83 and `happy` 51. Neither is in video A's English top 30. | `data/terms_video_b_en.csv`, `data/terms_video_a_en.csv` |
| A11 | Count words appear: `views` 43, `million` 31, `billion` 27 (A); `views` 61, `billion` 22 (B). Video A also has `comments` 74 and `comment` 23. | `data/terms_video_a_en.csv`, `data/terms_video_b_en.csv` |
| A12 | Non-English clouds are led by Spanish or Portuguese function words: `que` 93 (rank 1), `los` 51 (A); `que` 27, `las` 19, `por` 13 (B). English stopwords only, so these stay. | `data/terms_video_a_non_en.csv`, `data/terms_video_b_non_en.csv`; checklist last item |
| A13 | Video B non-English holds terms from other scripts and languages, for example `sawadika` 12, `selama` 11, `lamanya` 11; F5 shows Hangul and Thai words. | `data/terms_video_b_non_en.csv`; `figures/wordcloud_video_b_non_en.png` |
| A14 | Mixed top term: `bts` 345 (A), `blackpink` 448 (B). | `data/terms_video_a_mixed.csv`, `data/terms_video_b_mixed.csv` |
| A15 | Engagement ratios, sample composition by order and language, shared and distinctive top-30 terms. | NOT in a saved file yet: M2, M3 |

Ratios between A and B (for example "A has N times the comments") are not facts in a file. They come from M2.

### (b) Interpretations only the owner can give

Each is a question. Sonnet-writer leaves a `\todo{}` for each until the owner answers.

| # | Question for the owner | Facts it rests on |
| --- | --- | --- |
| B1 | The views are close, but the comment totals differ a lot. What do you think explains this? | A1, A2, T6 |
| B2 | Video A ranks `army`, `comments`, `million`, `views`. Do the comments talk about the song, or about the fandom and its counts? | A7, A11 |
| B3 | Video B ranks `anniversary` and `happy`. What anniversary do you think the comments mean? | A10 |
| B4 | `love` ranks second in both. Is it the same meaning in both? (Video B's title holds "Love".) | A6 |
| B5 | Video B names four members, video A mostly one. What does that say, if anything? | A8 |
| B6 | Which of the three cloud versions best supports your comparison, and why? | F1 to F7 |
| B7 | What does the non-English cloud say about each audience? Is it useful given the stopword limit? | A12, A13 |
| B8 | Does mixing relevance order and newest-first order change what the clouds show? | T3 (M3) |
| B9 | What is your overall conclusion: how are the two comment sections alike, and how do they differ? | all |

---

## 5. Missing items (named only, not created)

| # | Item | Why it is needed | Owner of the work |
| --- | --- | --- | --- |
| M1 | `hw3/code/p4_report_tables.py`: reads saved CSVs and writes `hw3/report/tables/*.tex` (T2, T3, T4a, T4b, T6, T7, T8). Drops `author` and `comment_id`, masks `@mentions`, strips emoji, escapes LaTeX, cuts text. Also writes the caption counts of F1 to F6. | No number is typed by hand (`rules/answering.md` §3). No handle reaches the report. | developer |
| M2 | `p3_compare.py` writes its output to files, for example `hw3/data/compare_videos.csv` (ratios) and `hw3/data/compare_terms.csv` (shared and distinctive lists per version). Today it prints only. | T6 and T8 need a saved source. | developer |
| M3 | Sample composition counts (order x language) saved to a file, for example `hw3/data/sample_composition.csv`, derived from `comments_<label>_all.csv`. No API call and no new language detection: use the saved `lang` column. | T3 and the checklist "order column says which". | developer (in M1 or M2) |
| M4 | `.gitignore` entry for `hw3/data/comments_*.csv`. Git status shows these files as untracked (`??`), not ignored. One `git add hw3` would commit other users' handles. | Privacy risk. | main session |
| M5 | Collection date ("as of") for the stats. `videos.csv` has no fetch timestamp. Views and likes change daily, so T2 needs a date. | T2 row "as of". Q5. | owner gives it, or developer adds a column on the next fetch |
| M6 | `run_all.py` lists `p4_report_tables.py` after `p3_compare.py`. | One command rebuilds every table. | developer |
| M7 | `hw3/PLAN.md` with the mission block. | Decision hierarchy needs goal lines (`rules/core.md`). Q1. | product-manager, after the owner approves |
| M8 | `hw3/report/hw3_taeklim_report.tex`. | The deliverable. | sonnet-writer |

---

## 6. Open questions for the owner

Q1. `[CLARIFICATION REQUIRED] There is no hw3/PLAN.md, so no mission block. Draft goal: "Submit a PDF that earns the 80 points of hw3_introduction.txt (30 + 30 + 20) by 2026-10-07 23:59". / Approve or change this goal line, or say that hw3 needs no PLAN.md.`

Q2. `[CLARIFICATION REQUIRED] The assignment asks for "screenshots of the data". This design shows a generated table (T4a, T4b) without the author column, not an image of the CSV. / Is a rendered table acceptable, or do you want an image (for example a PNG of the table)?`

Q3. `[CLARIFICATION REQUIRED] How many first comments per video, and from which order? / Give N (design default 5), and say if the time-order part should also show its first rows.`

Q4. `[CLARIFICATION REQUIRED] hw2 builds with pdfLaTeX (latexmk -pdf). The hw3 title of video A and the non-English terms hold Hangul and Thai, which pdfLaTeX cannot set. / Build hw3 with XeLaTeX (rules/writing/latex.md §1), or keep pdfLaTeX and drop non-Latin text from the tables and titles?`

Q5. `[CLARIFICATION REQUIRED] videos.csv has no fetch date, and the stats change daily. / Which date should the report give as "as of" for T2 (the fetch was on or around 2026-10-04 per common.VIDEOS comments, not a saved timestamp)?`

Q6. `[CLARIFICATION REQUIRED] The checklist says "fetched vs total comment count", but p3_compare.share_collected divides English kept by the total. / Which share should T6 show: fetched / total, English kept / total, or both?`

Q7. `[CLARIFICATION REQUIRED] The prompt asks for the student ID on page 1, but the hw2 reports show the name only (hw2/report/hw2_taeklim_report.tex line 57). / Add the student ID to the header line? If yes, give the exact text.`

Q8. `[CLARIFICATION REQUIRED] hw2 had no code appendix. / Should the hw3 report include the code (listings appendix), submit the .py files separately, or neither?`

Q9. `[CLARIFICATION REQUIRED] The checklist item "Own YouTube API credentials used" needs a sentence in S1. / Confirm the key is from your own Google Cloud project, and say how much to state (the key itself never appears).`

### Owner answers (2026-10-04)

- Q2, Q3: rendered tables are fine. 5 rows per video, relevance order, handles dropped, @mentions masked.
- Q4: build with XeLaTeX.
- Q7, Q8: name only on page 1. No code appendix: the report links the GitHub repo.
- Comment CSVs are now in `.gitignore` (M4 closed).
- Still open: Q1, Q5, Q6, Q9.
- Q1: no PLAN.md for hw3; `grading_checklist.md` holds the goal (owner, 2026-10-05).
- Q5: stats are "as of 2026-10-04". p1 saves `fetched_at` from the next run on; no re-collection.
- Q6: T6 shows both shares: fetched / total and English kept / total.
- Q9: S1 says the key is a YouTube Data API v3 key from the owner's own Google Cloud project; the key value never appears.
