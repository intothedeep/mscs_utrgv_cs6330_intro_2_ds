# HW3 report review (reviewer, 2026-10-07)

Target: `hw3/report/hw3_taeklim_report.tex` (built PDF, 8 pages).
Inputs checked: `hw3/code/*.py`, `hw3/data/*.csv`, `hw3/report/tables/*.tex`, `hw3/figures/*.png`,
`hw3/00_doc/*`, `hw3/report/discussion_owner.md`.
Check script and outputs: scratchpad `review/check.py`, `review/check_out.txt`, `review/page-*.png`.
`% src:` / `[S-...]` check: N/A. No research directory or Sources table was named for this task.

## Overall verdict

**PASS with fixes.** No blocker. 4 should-fix, 16 nit.

- Build is clean: 0 errors, 0 undefined references, 0 overfull boxes, 0 missing characters, 8 pages.
- Every table row spot-checked matches the CSVs. Every number in the text traces to a file or a code constant, with one hand-typed date (nit 5).
- Discussion claims hold against the data, with three wording problems (should-fix 1-3).
- The "data screenshot" the assignment asks for is not in the PDF (should-fix 4, owner decision).
- Fixes 1-3 add hand-typed ranks to §6. The report already does this ("Lisa 4th"), so it is not a new class of problem.

## Findings

| # | Severity | Location | What is wrong | Evidence | Suggested fix |
| --- | --- | --- | --- | --- | --- |
| 1 | should-fix | §6, line 404 | `amo` is said to "appear in both mixed clouds (Table 8)". Table 8 lists `amo` under "Only in BTS" (top 30). A reader who checks Table 8 sees a contradiction. | `terms_video_b_mixed.csv`: amo rank 55 (17), outside top 30 but inside the 150-term cloud. `tables/shared_terms.tex` row 2, column "Only in BTS". | Cite Table 8 for `que` only: "`que` is in both mixed top 30 (Table 8). `amo` is in both mixed clouds (BTS rank 13, BLACKPINK rank 55)." |
| 2 | should-fix | §6, line 396 | "Lisa leads only in mixed" depends on whether `rose` and `rosé` are merged. Per term Lisa leads in English too (45 vs 39). Per member, rose + rosé = 46 ties her. The report never says `rose` and `rosé` are one member, and Table 8 lists both. `rose` is also an English word, so 27 is an upper bound. | `terms_video_b_en.csv`: lisa 45, jisoo 39, jennie 35, rose 27, rosé 19. `terms_video_b_mixed.csv`: lisa 96, jisoo 59, jennie 59, rose 41, rosé 32. | "Lisa stands out only in mixed (96 vs 59 for the next member). In English the four are close (Lisa 45, Jisoo 39, Jennie 35, Rosé 27 + 19 under two spellings)." Add one clause that `rose` and `rosé` are the same member. |
| 3 | should-fix | §6, line 389 | "`boys`, `kings` only in the BTS cloud": `kings` is in the BTS English cloud only, not the mixed cloud. "the BTS cloud" is singular and ambiguous. | `terms_video_a_en.csv`: kings rank 139 (7). `terms_video_a_mixed.csv`: kings rank 191, outside 150. boys 76 / 63 (both clouds). girls b 34 / 38, queens b 36 / 39, neither in any BTS cloud. | "`boys`, `kings` only in the BTS English cloud. `girls`, `queens` only in the BLACKPINK clouds." |
| 4 | should-fix (owner decision) | §1.3, lines 186-219 (commented out) | The assignment asks for "screenshots of the data and result". With §1.3 off, no raw comment row is shown. Tables 2-3 show API statistics and counts, not the comments data. Grading scores only clouds and discussion, so the risk is small, but the instruction is explicit. | `00_doc/Homework_1_.pdf`: "Submit a word/pdf document with the screenshots of the data and result". `tables/first_comments_video_{a,b}.tex` exist and are current (2026-10-07 21:31). | Re-enable §1.3 (uncomment lines 187-219), or add one short sentence in §1.2 pointing to `hw3/data/comments_*_all.csv` as the data. Owner decides. |
| 5 | nit | Tooling, line 78. §1.1, line 118. Table 2 "As of". Fig. 1 node, line 162 | "none typed by hand": the date 2026-10-04 is hand-typed in the .tex and in `p4_report_tables.AS_OF`. `videos.csv` has no `fetched_at` column (the saved data predates the p1 change that writes it). The Figure 1 node "Stop at 1,000 English" is also typed, not the macro. | `data/videos.csv` columns: no `fetched_at`. `p4_report_tables.py` line 25: `AS_OF = "2026-10-04"`. Max `published_at` in both `_all.csv`: 2026-10-05T00:50Z UTC = 2026-10-04 19:50 CDT, so the date itself is right. | Either soften line 78 ("numbers in tables are generated") or leave as is. The date is correct. |
| 6 | nit | Table 1, line 101 | `write.csv` is mapped to `p1_collect.fetch_comments`. The CSV write is in `p1_collect.__main__`, not in `fetch_comments`. | `p1_collect.py`: `fetched.to_csv(...)` under `if __name__ == "__main__"`. | "`p1_collect.fetch_comments`, `p1_collect` (main)" or drop `write.csv` from the R column. |
| 7 | nit | §1, line 89. Table 1 | The assignment requires "your own YouTube API credentials". The report says "Data: YouTube Data API" and never says the key is the author's own, nor that Python uses an API key where R uses OAuth (`yt_oauth`). Also the bullet has no period. | `common.load_api_key`: key from `hw3/.env`. R script: `yt_oauth(client_id, client_secret)`. | "Data: YouTube Data API v3, own API key (R: OAuth via `yt_oauth`)." |
| 8 | nit | §6, line 379 | "song ... in the top 10" is ambiguous: the word `song` or the song title. `dynamite` is rank 8 (BTS English), but `kill` is rank 39 (BLACKPINK English), not top 10. | Tables 6-7. `terms_video_b_en.csv`: kill 39 (19). | Write ``song'' in quotes like ``love'', so it reads as the word. |
| 9 | nit | §6, line 389 | `kings` and `girls` are not in the owner's words. The owner wrote "boys, fighting, queens beautiful". The data check added them. | `discussion_owner.md`, last-but-one addition. | Owner confirms, or revert to "`boys` only in BTS, `queens` only in BLACKPINK". |
| 10 | nit | §6, line 395 | "2 of 7" is right for the cloud, but V and RM cannot appear under the 3-letter rule, and `jin` (rank 275) is a common string. The method hides two members. | `common.MIN_WORD_LENGTH = 3`. `terms_video_a_en.csv`: taehyung 178, jin 275, suga 274, namjoon 464. | Add "(V and RM are shorter than 3 letters and are dropped by the cleaning)". |
| 11 | nit | §6, line 380 | "member names rank high, mostly in the top 30": true for BLACKPINK (all 4 in top 30 both versions) and for Jungkook. For BTS, 3 members are below rank 170 in English and 2 (V, RM) are not detectable. "mostly" is generous. | Ranks (en/mixed): lisa 15/4, jisoo 16/14, jennie 19/15, rose 27/18. jungkook 24/16, jimin 38/22, taehyung 178/96, suga 274/146, jin 275/134, namjoon 464/130. | "BLACKPINK: all four in the top 30. BTS: Jungkook in the top 30, Jimin close (38)." |
| 12 | nit | §6, line 405 | "Thai comments appear" sits under "English vs. mixed", which implies they show in the mixed cloud. No Thai term reaches the top 150: Thai has no word spaces, so each comment becomes one unique term. The claim is true of the data only. | `comments_video_b_all.csv`: th 17. Video a: 0. Highest Thai-script term rank in `terms_video_b_mixed.csv`: 154. | "17 Thai comments for BLACKPINK (Lisa's home country), none for BTS. Thai has no word spaces, so no Thai word enters the cloud." |
| 13 | nit | §6, line 390 | "about 7 times": 7.41 / 1.11 = 6.65. | `compare_videos.csv`. | "almost 7 times" or "6.7 times". |
| 14 | nit | Table 3 caption, line 183 | Caption says ``Time'' with a capital. The table cells read `time`. | `tables/sample.tex`. | ``time''. |
| 15 | nit | Table 2, line 130 (`stats.tex`) | The BTS title cell is set in Arial Unicode (sans, straight quotes `'Dynamite'`) and the BLACKPINK title in Latin Modern (serif, curly quotes `’Kill This Love’`). The two cells look different. | `page-1.png`. `cell()` in `p4_report_tables.py` wraps only cells with non-Latin letters. | Accept, or set the whole Title row in `\unifont`. |
| 16 | nit | Page 3, page 7 | Page 3 is 60 % empty after Table 4 and page 7 is 55 % empty after Table 8, because of `\clearpage` before §3 and §6. | `page-3.png`, `page-7.png`. Lines 269, 364. | Keep if "one page per video" is wanted. Otherwise drop the `\clearpage` on line 364 so §6 follows Table 8. |
| 17 | nit | Page 8, line 389 | "BLACK-PINK" is hyphenated across a line break in the PDF. | `page-8.png`, first bullet of "After: boy group vs. girl group". | `\mbox{BLACKPINK}` in that line, or reorder the sentence. |
| 18 | nit | Table 8 | 5 underfull `\hbox` warnings in `shared_terms.tex` (`\scriptsize`, three 0.27 columns). Some lines are visibly spaced out ("blackpink, anniversary, blinks,"). | `hw3_taeklim_report.log` lines 873-893. | `\raggedright` in the three p-columns. |
| 19 | nit | Line 8 (comment) | Build comment still names "the non-English term tables", which were dropped. Comment only, not in the PDF. | `hw3_taeklim_report.tex` line 8. | "the mixed term tables". |
| 20 | nit | Table 8, §6 | `rose` and `rosé` appear as two terms in Table 8 and the BLACKPINK clouds. The report never says they are one member (Rosé). | `tables/shared_terms.tex`: rose in "Only in BLACKPINK" (both versions), rosé in mixed. | One clause in §6 or Table 8 caption: "`rose` and `rosé` are both Rosé." (See should-fix 2.) |

## Verified claims (no finding)

| Claim | Location | Evidence |
| --- | --- | --- |
| Table 2 values | §1.1 | `videos.csv`: all 10 rows match. |
| Table 3 values | §1.2 | Recomputed from `comments_*_all.csv` by order and `lang`: 660/413/176/1249, 340/289/87/716, 579/424/105/1108, 421/434/164/1019, totals 1,965 and 2,127. All match. |
| Table 5 values | §5 | Recomputed from `videos.csv`: 18.47, 7.41, 0.0124 %, 0.0063 % (BTS) and 11.92, 1.11, 0.0851 %, 0.0400 % (BLACKPINK). All match. |
| Tables 6-7 | §5 | Match `terms_*_{en,mixed}.csv` rows 1-10. `terms_video_a_en.csv` top 10 recomputed from comments with `common.count_terms`: identical. |
| Table 8 | §5 | Recomputed top-30 split for both versions: identical to `compare_terms.csv`. |
| Counts macros | captions | `counts.tex`: nEn 1,000 / 1,000, nMixed 1,965 / 2,127 match Table 3 totals. |
| "20 languages" | Fig. 1, §2 | `common.LANGUAGES` has 20 entries. |
| "Sotho or Tswana" | §2 | `common.py` comment, first run 2026-10-04. |
| Table 4 steps 2-7 | §2 | `clean_terms`: lowercase, `_NON_WORD` keeps `\w` of every script, `TM_STOPWORDS`, `MIN_WORD_LENGTH = 3`, no stemming. `MAX_WORDS = 150`, `random_state=SEED`. |
| "army → armi, happy → happi" | §2 | Snowball English stems. |
| "with 2, de, la, en enter the clouds" | §2 | Mixed comments: BTS de 83, la 43, en 38 vs 150th term count 9. BLACKPINK de 46, la 29, en 27 vs 7. |
| Lisa 4th in BLACKPINK mixed | §6 | `terms_video_b_mixed.csv` rank 4 (96). |
| All 4 BLACKPINK members in both clouds | §6 | English ranks 15, 16, 19, 27 (rosé 40). Mixed ranks 4, 14, 15, 18. |
| `views`, `billion`, `army`, `blinks`, `comments`, `fighting`, `miss`, `area` in the clouds named | §6 | views a 12/14, b 9/12. billion a 21/27, b 32/35. comments a 5/5. fighting a 35/41. miss b 30/33. area b 20/21. |
| `comeback` "appears, but rarely" | §6 | 5 BTS comments. Rank 467 en, 371 mixed (not in the cloud). |
| Video ages 6 and 7 years | §6 | `videos.csv`: 2020-08-21, 2019-04-04. Today 2026-10-07. |
| "September 2026 anyone?" | §6 | 6 BTS comments contain "september 2026". `anyone` in 63 BTS and 67 BLACKPINK comments. |
| Bogotá comments 2026-10-03/04 | §6 | 7 BTS comments name Bogotá or Colombia. 6 dated 2026-10-03 or 10-04 (one 2020-08-21). 0 for BLACKPINK. |
| Spanish share not rising recently | §6 | BTS es share: 8.8 % in comments dated >= 2026-09-01 (n = 1,692) vs 11.7 % before (n = 273). Overall es 181 of 1,965 (3rd after en and none). |
| `que` in both mixed clouds | §6 | a rank 4 (94), b rank 28 (30). `que` comments: BTS 72 (es 47, pt 23), BLACKPINK 26 (es 14, pt 7). |
| `anniversary` mostly newest, 10th | §6 | 80 BLACKPINK comments. 78 via time order. 66 mention "10th" or "10 year". |
| "recent comments center on members and 10th anniversary" | §6 | BLACKPINK time-order terms: blackpink 271, love 96, anniversary 82, happy 51, song 44, blink 42, lisa 37, black 32, jennie 31, ... jisoo 25, rose 18. |
| Thai only for BLACKPINK | §6 | th 17 vs 0 (see nit 12). |
| Figure references and labels | all | Every `\ref` resolves. `tab:first_a/b` only inside comments. No "Video A/B", "non-English", "Limits", "open question", "first five", hard-coded "Table N" in live text. |
| Em dashes, semicolons | all | `grep` per `style.md` §3: none. Semicolons only inside TikZ code. No typos found in the PDF text. |
| Figures | §3-5 | Single clouds match the grid panels (same seed). Hangul in grid titles renders (AppleGothic). No tofu. |
| Files from one run | data, figures, tables | `terms_*.csv`, `wordcloud_*.png`, `compare_*.csv`: 2026-10-07 19:53. `tables/*.tex`: 21:31. `comments_*_all.csv`, `videos.csv`: 2026-10-04 20:04. Consistent. |

UNVERIFIED (needs a run that is not allowed here): the detector's language labels themselves (`lang` column), and "all 75" lingua languages. Taken as saved.

## Per-check verdicts

1. Assignment coverage: **PASS with a risk.** Two videos, own key (code), four clouds plus grid, comparison tables, discussion. Raw comment data is not shown (should-fix 4, owner decision). Own-key use is not stated in the text (nit 7).
2. Numbers trace to saved files: **PASS.** All table rows spot-checked match. One hand-typed date, correct (nit 5). Derived numbers in the text ("about 7 times", 6 and 7 years, 2 of 7, dates) are right. Nit 13 on rounding.
3. Factual claims, Sections 1-6: **PASS with fixes.** Three wording errors in §6 (should-fix 1-3). Nits 8-12, 20.
4. Table 1 (R vs Python): **PASS with a nit** (write.csv placement, nit 6. OAuth vs API key, nit 7).
5. Internal consistency: **PASS.** All references resolve to the right objects. Captions match. Names consistent. No leftovers in live text (nit 14, 19).
6. Writing: **PASS.** No em dashes, no semicolons in prose, no typos found. Hyphenated "BLACK-PINK" (nit 17).
7. Build and page render: **PASS.** `latexmk -C` then `latexmk -xelatex`: exit 0, 8 pages, 0 errors, 0 undefined references, 0 overfull boxes, 0 missing characters. 5 underfull boxes in Table 8 (nit 18). Pages: no overlap, no cut-off text, no missing glyphs. Large blank areas on pages 3 and 7 from `\clearpage` (nit 16).
