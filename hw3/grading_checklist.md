# HW3 grading checklist

Rubric from `00_doc/hw3_introduction.txt` (due 2026-10-07 23:59), turned into boxes to tick.
Tick a box only after you have read that part of the report yourself and agree with it.

## Submission

- [ ] Word or PDF document "including your discussion and the screenshot of the wordClouds"
- [ ] "screenshots of the data and result" (`00_doc/Homework_1_.pdf`): stats, details and
      first comments of each video (`data/videos.csv`, `data/comments_<label>.csv`)
- [ ] Own YouTube API credentials used (key in `hw3/.env`, never in the report or code)
- [ ] Name on the first page

## Word clouds: 30 points per video

- [ ] Video A comments collected and word cloud (`figures/wordcloud_video_a.png`)
- [ ] Video B comments collected and word cloud (`figures/wordcloud_video_b.png`)

## Discussion: 20 points

- [ ] Compare the two videos (`p3_compare.py`: engagement per 1k views, shared and
      distinctive top terms)
- [ ] State the collection limits: top-level comments only, cap of 1000, order = relevance,
      collected vs total comment count
- [ ] State the cleaning: lowercase, punctuation, numbers, tm English stopwords, words under
      3 letters dropped, no stemming; emoji and non-Latin text dropped (deviation from tm)
