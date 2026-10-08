# Discussion: owner's words (verbatim, 2026-10-07)

Source for Section "Discussion" of `hw3_taeklim_report.tex`. Kept as given; the report holds the English translation.

```
BTS, Blackpink 둘 한국 kpop 남자 여자 그룹이다. 

- 조사 전
둘다 글로벌로 팬덤이 많으 그룹 한국어 이외에도 영어 다국어가 많을 것 같다.
그룹명, 노래, 구성원 이름, 사랑해, 팬덤 이름, 노래, 등이 많이 나올거라고 생각했다. 
특정 멤버가 좀 더 유명해서 그 멤버를 칭하는 댓글이 많을 거라고 예상했다.
다국어로 댓글이 달릴 걸 예상 



- 조사 후 공통
실제로, 그룹명, 사랑해, 팬덤 이름, 노래 등이 많이 나왔고 top 10
멤버이름은 top10은 아니지만 영어, 다국어 뭉치에 유의미하게 크게 등장하고 있다. 
유튜브 조회 수 그리고 유명세를 자랑스럽게 생각하는 단어가 보인다. billion, viesw, 
팬덤: army, blinks
그리고 다국어 버전에 여러 나라 언어가 보이는 걸 보아 글로벌하게 

- 조사 후 차이 걸 보이 그룹 
bts: comments 댓글 단 사람들이 비디오 달린 댓글 숫자를 자랑스럽게 생각하는 것 같다. boys, fandom이 유명해서 그런지 단어가 보인다. 파이팅 이라는 단언가 보이네? 그리고 최근 멤버 전원이 군복무를 마치고 복귀해서 모든 멤버가 뭉쳐 투어를 하고 있어서 comback 이라는 글자도 보인다. 
blackpink: 멤버 중 jennie, Lisa 가 크게 보임, 최근 10주년이어서 최근 댓글 그래서 그런지  anniversary가 특별하게 잘 보임 queen , beatufiful


- 조사 후 차이 영어 vs 다국어, Black pink

다국어에서 Lisa 출신인 태국  태국어 답글이 보인다. 
```

## Data checks applied in the English version (saved terms_*.csv, comments_*_all.csv)

- "comback": typo, comeback. It is rare (rank 467 English, 371 mixed), so not in the 150-term clouds. Written as "appears, but rarely".
- "queen": rank 210, not in the cloud. "queens" is rank 36. Written as queens.
- "jennie, Lisa": Lisa is rank 4 in the BLACKPINK mixed top 10. Jennie ties Jisoo (59 each, mixed). Written as Lisa only.
- "멤버이름은 top10은 아니지만": true except Lisa (mixed). Written as "mostly below the top 10".
- "10주년": confirmed; 78 of 80 "anniversary" comments are newest-first, many say "10th anniversary".
- "태국어 답글": these are top-level comments, not replies (replies are not fetched). 17 Thai comments for BLACKPINK, 0 for BTS. No Thai term reaches the mixed top 150.
- "viesw", "beatufiful": typos, views and beautiful.

## Addition (verbatim, 2026-10-07)

```
after analysis: we can add this found? que -> means spain so both has some spanish fandom?
```

Data check: `que` is a Spanish and Portuguese word (not only Spain). Comments with `que`: BTS 72 (es 47, pt 23), BLACKPINK 26 (es 14, pt 7). `que` is in the top 30 of both mixed versions ("In both", tables/shared_terms.tex). Written as "Spanish- and Portuguese-speaking fans, more for BTS".

## Addition (verbatim, 2026-10-07)

```
최근 댓글이 포함되어 있기 때문에 bts는 실제 콜럼비아서 콘서트 이게 반영이 된 것 같다? 추가?
```

Data check (comments_video_a_all.csv): 7 comments name Colombia or Bogotá; 6 are dated 2026-10-03 or 2026-10-04 (data fetched 2026-10-04), two name "Tour Arirang Bogotá". All 7 came through relevance order, not newest-first. Written as "recent comments ... concert in Bogotá".

## Addition (verbatim, 2026-10-07)

```
예상대로 멤버 이름들이 상위권을 차지하고 있다.
```

Data check (terms_*_{en,mixed}.csv ranks): Lisa 15 / 4, Jisoo 16 / 14, Jennie 19 / 15, rose 27 / 18; Jungkook 24 / 16, Jimin 38 / 22 (English / mixed). Replaces the earlier "mostly below the top 10" line.

## Addition (verbatim, 2026-10-07)

```
amo -> fandom in latin? with que?
```

Data check: amo ranks 13 (BTS) and 55 (BLACKPINK) in mixed; que is in both mixed top 30. Language does not show the country (Spain and Portugal also use these words), so written as "Spanish- and Portuguese-speaking fans", merged into the que line.

## Addition (verbatim, 2026-10-07)

```
- One better-known member gets more mentions.: results? bts 2 out of 7 mentioned? blackpink: 4 members in ranks?
yes
```

Data check (top 150 = cloud): BTS English 2 of 7 (Jungkook 24, Jimin 38), mixed 6 of 7 (others 96-146, J-Hope 301). BLACKPINK 4 of 4 in both; English 15-27, mixed Lisa 4 (96) vs next 59. V and RM short names are dropped by the 3-letter rule. Replaces "lisa stands out most, in the mixed top 10".

## Addition (verbatim, 2026-10-07)

```
  - anyone: returning viewers greet others ("September 2026 anyone?"). The year is cut as a number.
>> new found: 7 yeras old so some fans come to watch and ask others anyone now? so we can see that there are many old fans comming and comming to watch
```

Data check (videos.csv published dates): BLACKPINK 2019-04-04 (7 years), BTS 2020-08-21 (6 years). Written with both ages.

## Addition (verbatim, 2026-10-07)

```
I will take your opinions 1, 2, 3
```

Owner adopted the assistant's suggested wording (Korean, as offered in chat):
1. "BTS 팬이 댓글을 훨씬 많이 단다. 조회수는 비슷한데 댓글은 약 7배." (Table 5: comments per 1k views 7.41 vs 1.11)
2. "두 팬덤 모두 글로벌하고 오래된 팬이 돌아온다. BTS는 기록과 공연, BLACKPINK는 멤버와 10주년이 중심이다."
3. Move the que/amo line into "English vs. mixed".

## Conclusion revision (verbatim, 2026-10-07)

```
- BTS centers on records and concerts: hmmm? do not know? but it seems their tour affects comments: see more spanish comments. 
- both have global fandom, recent comments BLACKPINK centers on members and its 10th anniversary.
```

Data check (comments_video_a_all.csv): Spanish share is 8.8% in 2026-09/10 vs 11.7% before; 7 Spanish comments mention a concert or tour. So the tour does not raise the Spanish share; it shows in comment content (Bogota). Written as "the tour shows in recent comments ... Spanish comments are many, but not more recently".

## Addition (verbatim, 2026-10-07)

```
we can see boys and girl group based on different words: boys, fighting, queens beautiful
```

Data check (terms_*_en.csv ranks, BTS / BLACKPINK): boys 76 / -, kings 139 / -, girls 620 / 34, queens - / 36, beautiful 54 / 72, fighting 35 / 165. beautiful is in both clouds (higher for BTS); fighting is the Korean cheer, not gendered. Written as boys, kings vs girls, queens; fighting kept as its own BTS line; beautiful dropped.

## Addition (verbatim, 2026-10-07)

```
  - BLACKPINK: fans miss the group (miss): 속속사 하나에서 각자 소속사로 흩어져서 개인활동을 많이 하는 걸 알 수 있다.   - BLACKPINK: the fan chant "BLACKPINK in your area" (area).: 2 are ok to add
```

Data check: miss in 24 English comments, area in 35 (comments_video_b_all.csv). The agency move is the owner's own knowledge, not in the data; written as the owner's reason.
