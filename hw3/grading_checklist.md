# HW3 grading checklist

Rubric from `00_doc/hw3_introduction.txt` (due 2026-10-07 23:59), turned into boxes to tick.
Tick a box only after you have read that part of the report yourself and agree with it.

## Submission

- [ ] Word or PDF document "including your discussion and the screenshot of the wordClouds"
- [ ] "screenshots of the data and result" (`00_doc/Homework_1_.pdf`): stats, details and
      first comments of each video (`data/videos.csv`, `data/comments_<label>_all.csv`)
- [ ] Own YouTube API credentials used (key in `hw3/.env`, never in the report or code)
- [ ] Name on the first page

## Word clouds: 30 points per video

Video A = BTS 'Dynamite', video B = BLACKPINK 'Kill This Love'. Three clouds per video:
English (1000 comments), non-English, mixed (all languages). Grid: `figures/wordcloud_grid.png`.

- [ ] Video A comments collected and word clouds (`figures/wordcloud_video_a_<en|non_en|mixed>.png`)
- [ ] Video B comments collected and word clouds (`figures/wordcloud_video_b_<en|non_en|mixed>.png`)

## Discussion: 20 points

- [ ] Compare the two videos (`p3_compare.py`: engagement per 1k views, shared and
      distinctive top terms, per version)
- [ ] State the collection limits: top-level comments only, no replies
- [ ] State the sample: by relevance until its paging ends, then newest first, until 1000
      English comments; the `order` column says which; fetched vs total comment count
- [ ] State the language split: lingua detector over 20 candidate languages; URLs and
      @mentions removed first; emoji-only comments get no language and go to non-English
- [ ] State the cleaning: lowercase, punctuation, numbers, emoji, tm English stopwords, words
      under 3 letters dropped, no stemming; letters of every script kept (as tm does)
- [ ] State the limits of the non-English cloud: English stopwords only, so Spanish and
      Portuguese function words (que, los, por) rank high
