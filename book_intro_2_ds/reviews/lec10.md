# T21 review: lec10-p-value.tex (cycle 1/2)

Date: 2026-09-23. Target: `chapters/lec10-p-value.tex` (new, 702 lines), `parts/part1-foundations.tex` (+1 line).
Criteria: PLAN.md T20 AC + §4 AC-W1..W10; architecture.md §7.3; §7.x decision record (63 everywhere,
63-based intervals in main text, 62-based slide intervals only inside pitfalls).
Source checked: `notes_text/10_P-value/slides.md`, media image13, image29, image44; figures 10_01, 10_03, 10_04 viewed.
Build: `latexmk -C` then `latexmk -xelatex -interaction=nonstopmode main.tex` from `book_intro_2_ds/`.

## Verdict: ISSUE

The build is clean and nearly every number checks out. But the chapter teaches one wrong number: the
one-sided coin p-value is 7/32 = 0.21875, and it should be 6/32 = 0.1875 (I1). It also misstates what
slide 20 concludes (I2). Six figures/tables are never `\Cref`'d (I5), slide 11 is not used (I3), and
two pitfalls do not have the required form (I4). All issues are **implementation → sonnet-writer**.
No reasoning issue was found. The spec (R8: (5+1)/32) is correct, and the writer departed from it.

## Mechanical ACs

| AC | Result | Evidence |
| :-- | :-- | :-- |
| AC-W1 build | PASS | exit 0, 2,481,448-byte PDF |
| AC-W2 refs | PASS | `grep -cE "undefined\|multiply defined" main.log` = 0 |
| AC-W3 em dash | PASS | 0 hits of `—\|---` in non-comment lines |
| AC-W4 `\Cref` only | PASS | 0 `\ref/\cref/\autoref`, 0 hard-coded chapter numbers. All 45 distinct `\Cref` targets exist |
| Rendered text | PASS | pdftotext: 0 "그림 (그림" / "표 (표" / "??" |
| Overfull >5pt from lec10 | PASS | the only overfulls are 1.20pt, the book-wide callout-box width (54 in the whole log) |
| Labels, each once | PASS | all 26 required labels occur exactly once. Extra: `tab:pv-three-parts-compare`, `pit:pv-null-reversed`, `pit:pv-vitd-62-63`, `pit:pv-vitd-ci` |
| p-value not redefined | PASS | `begin{definition}[p값]` = 0, `\begin{definition}` = 0, `\Cref{def:pvalue}` = 4 |
| `ch:compare-dist` absent | PASS | 0 |
| part1 diff | PASS | numstat `1 0` |
| Design-doc IDs in reader text | PASS | 0 hits for R/U/Q/E/T-ids (the chapter's `\texttt{imageNN}` names are slide media, as allowed by spec) |
| AC-W8 skeleton | PASS | `inbrief` before first `\section`; background → why → 6 what sections → apply → future; every concept section opens with `inbrief` |
| AC-W10 files | PASS | five PNGs exist (19:27, after the 63 decision); 10_03 and 10_04 show 63 / [56.4, 69.6] / [54.5, 71.5] |
| AC-W10 each figure/table `\Cref`'d | **ISSUE I5** | never referenced: `fig:pv-coin`, `fig:pv-three-parts`, `fig:pv-height`, `fig:pv-vitd`, `fig:pv-ci-test`, `tab:pv-ci-vs-p` |

## Recompute (scipy, run by reviewer)

| Item | Chapter | Recomputed | Result |
| :-- | :-- | :-- | :-- |
| Fisher [[73,125],[59,131]] | 약 0.24 | 0.2398 | PASS |
| 73/198, 59/190 | 36.9%, 31.1% | 0.3687, 0.3105 | PASS |
| 1043/1046, 2/1434 | 99.7%, 0.14% | 0.99713, 0.001395 | PASS |
| Yates [[71,127],[72,126]] | χ² 0, p 1.0 | 0.0, 1.0 | PASS |
| Yates [[73,125],[71,127]] | χ² 0.011, p 0.917 | 0.011, 0.9168 | PASS |
| [[60,138],[84,114]] | 30.3%, 42.4%, χ² 6.29, p 0.012, Yates 0.016 | 6.286, 0.0122, 0.0163 | PASS |
| [[5005,9868],[4800,9000]] | 33.65%, 34.78%, 1.1pt, χ² 4.07, z 2.02, p 0.044 | 4.069, 2.017, 0.0437 | PASS |
| 2 flips / 5 flips two-sided | 0.5, 12/32 = 0.375 | same | PASS |
| **5 flips one-sided (H_a: 앞면이 더 잘)** | **(5+2)/32 = 7/32 = 0.21875** (L311, L323) | P(X≥4) = 6/32 = **0.1875** | **ISSUE I1** |
| σ, tails, two-sided | 6.89, 0.0234, 0.0268, 0.0502 | with σ = 6.89: 0.02338, 0.02678, 0.05017 | PASS |
| band / remainders | 0.035, 0.483, 0.483 | 0.0347, 0.4826, 0.4826 | PASS |
| z vitamin D | −11.21, p ≈ 3.6e−29 | −11.2121, 3.556e−29 | PASS |
| z with 62 | −11.52 | −11.515 | PASS |
| 95% (1.96) | 56.53, 69.47 | 56.532, 69.468 | PASS |
| 95% (2), 99% (63) | [56.4, 69.6], [54.5, 71.5] | same | PASS (decision record) |
| slide 62 intervals | [55.4, 68.6], [53.5, 70.5] only in `pit:pv-vitd-ci` | same | PASS (only inside pitfall) |
| pears | 1.860, 1.612, 2.462, 2.616, [−2.44, 10.44] | 1.8605, 1.6125, 2.4620, 2.6157 | PASS |
| df for 2.616 | "자유도 약 128" (L587) | t.ppf(.995,128) = 2.6148; 2.6157 ↔ df ≈ 125 (Welch 125.5) | **ISSUE I11 (minor)** |
| 10_05 caption | 4.6% vs 3.3% | T19r: 4.6% / 3.3% / 3.3% | PASS |
| check question | 2/8 = 0.25 | 0.25 | PASS |

AC-W6 list: all present except **0.1875** (I1). 31% appears only in L131.

## Pitfalls (AC-W7)

| Row | Where | Form | Result |
| :-- | :-- | :-- | :-- |
| 29% → 31.1% | L129 | "슬라이드 값은 29%, 다시 계산하면 31.1%" | PASS (see I12) |
| 0.001% → 0.14% | L116 | correct form | PASS |
| reversed H0 | L410 | "슬라이드 값은 …, 바르게는 반대다" | PASS |
| p = 0.05 called 유의 | L418 | "슬라이드는 …, 바르게는 경계에서 기각 실패다" | PASS |
| question < vs H_a ≠ | L510 | title "연구 질문과 대립가설의 방향이 어긋난다"; `\Cref{pit:ht-direction}` present | **ISSUE I4** (form) |
| 62 vs 63 | L494, L549 | L549 in correct form; L494 "슬라이드는 …섞어 쓴다, 이 책은 63으로 통일한다" | PASS (L500 wording, see I4) |
| 11.2 → −11.21 | L504 | "슬라이드는 부호 없이 z=11.2, 다시 계산하면 z=−11.21" | PASS |
| interval reading / Apples / "the same" | L596 | title "슬라이드 문장 세 개가 모두 틀렸다" | **ISSUE I4** (form), **I2** (content) |
| 0.24 ≠ 24% | L215 | present | PASS |
| effect size | L246 | present, 0.044, 1.1pt | PASS |
| 세 부분 = 양측 | L303 | present, but number is wrong | **ISSUE I1** |
| threshold arbitrary | L209 | links `\Cref{pit:ht-alpha}`, but it is a whole new `pitfall` box, not "one line, no new box" | minor, folded into I4 |

## Slide coverage (AC-W9)

`% source:` comments cover slides 1–25. The content check:

- Slide 11 (flower, "equally rare things make it less special"): **no content anywhere**. The spec requires one sentence. `grep 꽃` = 0. **ISSUE I3.**
- Slide 3 (dog trial): in the chapter-head `keyidea` (L23). `sec:pv-why` claims slide 3, but the section never uses the trial. The spec puts the prescription intuition there. Minor, folded into I3.
- Slide 5 text "P-value = 0.9": the pair is named with 0.917 (L182), but the slide's 0.9 is not tied to it. Minor.
- Slide 19 "A p-value can always be derived from the CI": the R17 condition (true only under the same estimate ± z·SE model) is absent. **ISSUE I14.**
- Slides 22–25: prose only in `sec:pv-future`, with no `ch:compare-dist`. PASS.

## Bilingual (AC-W5), `\term{}` hits

p값(p-value), 귀무가설(Null Hypothesis), 대립가설(Alternative Hypothesis), 정규분포(Normal Distribution),
표준오차(Standard Error) ×2, 신뢰구간(Confidence Interval), 표준화 점수(z-score), 거짓 양성(False Positive) ×2,
1종 오류(Type I Error) ×2, 효과 크기(Effect Size) ×2, t검정(t-test), 콜모고로프-스미르노프 검정(Kolmogorov-Smirnov Test),
2종 오류(Type II Error), 검정력(Power): PASS.
Missing English: L621 table cell `\term{거짓 양성}(1종 오류, …)` and L623 "2종 오류" (table cells are introduction sites).
"카이제곱"/χ² (L179–243, caption L203), "Yates 보정" and "피셔 정확검정" (caption L204) appear with no gloss and no English. **ISSUE I10.**

## Issues (all implementation → sonnet-writer)

- **I1 (blocking) L311, L323: wrong one-sided p-value.** For H_a "앞면이 더 잘 나온다" with 4 heads observed,
  the one-sided p is P(X≥4) = (5+1)/32 = 6/32 = 0.1875. 0 heads is in the *opposite* direction, so it
  does not count. The chapter's (5+2)/32 = 0.21875 counts it anyway. The pitfall exists to teach exactly this distinction, so this
  is a wrong fact, not a typo. The required AC-W6 number 0.1875 is absent. Also fix the L311 comment "관측값 + 더 드묾만" to name only 5 heads.
- **I2 (blocking) L611–613: slide 20 misread.** The slide's "P < 0.01 → reject → the pears are different" is the
  hypothetical branch ("If it did not overlap…"). The slide's actual conclusion is "0 is in the interval → P > 0.01 → fail
  to reject". The chapter says the book's result is the "반대 결론" to the slide. That is false: both fail to reject. The real
  slide faults are the mixed hypothetical (architecture R19), the "Apples" typo, and "the same" wording. Items 2–3 (L603–609) should be reworded to match.
- **I3 slide 11 missing** (AC-W9): add the one-sentence flower point in `sec:pv-discrete`. Minor: the slide-3 trial should also appear in `sec:pv-why`.
- **I4 pitfall form** (AC-W7): L510 (direction) and L596 (slide 20) need titles in "슬라이드는 X, 바르게는 Y" form. L500
  says "여기 각주로만 남긴다", but it is a pitfall box, and 62 also appears in `pit:pv-vitd-ci`. Reword. L209: the spec says
  "one line + `\Cref{pit:ht-alpha}`, no new box".
- **I5 unreferenced floats** (AC-W10): add in-text `\Cref` for `fig:pv-coin`, `fig:pv-three-parts`, `fig:pv-height`, `fig:pv-vitd`, `fig:pv-ci-test`, `tab:pv-ci-vs-p`.
- **I6 L155 wrong cross-ref:** the caption sends the 29% error to "`\Cref{pit:ht-fail-not-proof}` 근처 함정", which is
  lec09's non-proof pitfall. Label the L129 pitfall and point there.
- **I7 L134–136:** "계산은 `\Cref{sec:pv-threshold}`에서 이어간다". No calculation of 0.24 exists there. The spec says 약 0.24 with no computation. Remove the pointer or replace it.
- **I8 `tab:pv-drug-trials`** (spec §7.3.6): it lacks the 약 · 완치 · 비완치 columns and the A-vs-A rows (three pairs) and the 34%-vs-35% row.
- **I9 one operation per align line** (principle 9b/10): L179, L183, L191 and L243 pack χ², z, p (and Yates) on one line. L395 and L484 chain two operations.
- **I10 bilingual/gloss** (AC-W5, principle 9c): see the section above.
- **I11 minor L587:** "자유도 약 128" should be "약 125". At df 128 the critical value is 2.6148, not 2.616 (T19r note).
- **I12 minor L131:** "본문은 반올림한 31%를 쓴다", but the body (L126) and the table (L151) show 31.1%. Make it consistent.
- **I13 minor L149:** `--` is used as an empty table cell. Principle 11 says leave it empty or write 없음.
- **I14 R17 condition missing** in `sec:pv-ci-duality` (see coverage above).

Minor, no action required: `tab:pv-error-types` sits in `sec:pv-ci-duality` but belongs to `sec:pv-threshold`. The L438–440 keyidea sentence ("p값이 크다고…정반대로") reads confusingly.

## Routing

All items go to `sonnet-writer` (cycle 2/2). No architect action is needed. The T19 figures already follow the 63 decision.

## Addendum (after second pass)

| Check | Result | Evidence |
| :-- | :-- | :-- |
| 10_02 vs caption L445–448 | PASS | the figure prints 0.0234, 0.0268, "two-sided p = 0.0502 (slide: 0.05)", band 0.035, 0.483 ×2. The T19r I2 fix has landed |
| 10_05 vs caption L202–205 | PASS | "p < 0.05: 4.6%", chi-square uncorrected, 36.9%. Minor: the caption does not explain why the histogram is jagged (discrete 2x2 p-values, T19r note) |
| Principle 8 (문제→처방 openings) | PASS with note | every concept section's `inbrief` Why states the problem. `sec:pv-why`, `sec:pv-discrete` and `sec:pv-continuous` bodies open on the failure. `sec:pv-ci-duality` (L540) and `sec:pv-sim-vs-param` open on procedure/example. Acceptable under principle 8's section rule, so no ISSUE |
| Principle 9 (beginner steps) | **ISSUE I10b** | 9(c): the raw 2x2 notation `[[71,127],[72,126]]` (L178, L182, L189, L236) is never explained (rows = 약, columns = 완치/비완치). A beginner cannot read it. χ², "Yates 보정" and "피셔 정확검정" are used as machinery with no gloss, while spec R3a/E1 says test names are not taught in this deck. Either explain them in one line each or drop them to "p값(슬라이드)" values. 9(b): see I9 |

**I10 extended (AC-W5):** there are also missing English glosses at introduction sites: L535 In brief "유의수준 = 1 − 신뢰수준" and the L565 table header 신뢰수준 / 유의수준($\alpha$). Add (Confidence Level) and (Significance Level).
The full I10 list is L535, L565, L621, L623, plus the χ²/Yates/Fisher names.

**I10b (implementation → sonnet-writer):** as in the table row above.

Verdict unchanged: **ISSUE**. Blocking items: I1, I2. All implementation → sonnet-writer; no architect action.

## Re-review (cycle 2)

Date: 2026-09-23. Target: current `chapters/lec10-p-value.tex` (770 lines), opened with Read.
Build: `latexmk -C` then `latexmk -xelatex -interaction=nonstopmode main.tex` from `book_intro_2_ds/`.
Source images viewed this cycle: image7, image8, image9, image10, image11, image12, image13, image14, image15 (slides 4–7), image44 (slide 20), image3/image4 (slide 4 1-vs-1 people).

### Verdict: PASS

All of I1–I14 (and I10b) are closed. No new blocking problem. Two minor notes (N1, N2) are recorded below. Neither is blocking.

### Mechanical re-check

| Check | Result | Evidence |
| :-- | :-- | :-- |
| Build | PASS | exit 0, main.pdf 2,488,160 bytes |
| Undefined / multiply defined | PASS | `grep -ciE 'undefined\|multiply defined' main.log` = 0 |
| Overfull | PASS | 53 in the log, all 1.20001pt (the book-wide callout width) |
| Em dash | PASS | 0 `—` / `---` in non-comment lines. The only `--` are ranges (15--49, 142--169, 155.4--156, 22--25) |
| Design-doc IDs in reader text | PASS | 0 R/U/Q/E/T/AC/I-ids in non-comment lines |
| Rendered text (pdftotext) | PASS | "그림 (그림" 0, "표 (표" 0, "??" 0 |
| `\ref/\cref/\autoref` | PASS | 0 |
| Duplicate labels | PASS | none |
| part1 diff | PASS | numstat `1 0` |
| Every fig/tab `\Cref`'d | PASS | all 11 fig/tab labels are `\Cref`'d, including the six from I5: `fig:pv-coin` L302, `fig:pv-three-parts` L312, `fig:pv-height` L434, `fig:pv-vitd` L521, `fig:pv-ci-test` L609, `tab:pv-ci-vs-p` L611 |
| `pit:pv-drug-2931` | PASS | defined once (L134), used in the `tab:pv-drug-trials` caption (L173). It renders as "절 6.2 함정 참고". Pitfalls have no counter of their own, so `\Cref` resolves to the enclosing section, and 6.2 is `sec:pv-why`, where the pitfall sits. This is correct |

### Recompute (scipy, this cycle)

| Item | Chapter | Recomputed | Result |
| :-- | :-- | :-- | :-- |
| One-sided coin (I1) | (5+1)/32 = 6/32 = 0.1875 (L351, L366) | 0.1875 | PASS |
| Welch df for pears (I11) | "자유도 약 125" (L644) | df = 125.465; t.ppf(0.995,125) = 2.61573; 6.44/2.462 = 2.6157 | PASS |
| 59/190 (I12) | 31.1% (L130, L136, L157) | 0.31053 | PASS. "31%" alone no longer appears |
| 73/198 | 36.9% | 0.36869 | PASS |
| Table rows 71/198, 72/198 | 35.9%, 36.4% | 0.3586, 0.3636 | PASS |
| 60/198, 84/198 | 30.3%, 42.4% | 0.3030, 0.4242 | PASS |
| 1043/1046, 2/1434 | 99.7%, 0.14% | 0.99713, 0.001395 | PASS |
| 5005/14873, 4800/13800 | 33.65%, 34.78% | 0.33652, 0.34783 | PASS |

### `tab:pv-drug-trials` rows vs slide images (I8)

| Row | Chapter | Slide image | Result |
| :-- | :-- | :-- | :-- |
| 대규모 A / B | 1043·3 / 2·1432 | image7 1,043·3; image8 2·1,432 | PASS |
| 약 200명씩 A / B | 73·125 / 59·131 | image9 73·125 "37%"; image10 59·131 "29%" | PASS (caption states slide's 37%, 29%) |
| A 대 A(1) | 71·127 / 72·126, p = 1.0 | image13 71·127 P=1 72·126 | PASS |
| A 대 A(2) | 73·125 / 71·127, p = 0.917 | image11 73·125; image12 71·127; slide 5 text "P-value = 0.9" | PASS |
| A 대 A(3) | 60·138 / 84·114, p = 0.012 | image14 60·138 P=0.01 84·114 | PASS |
| 대표본 | 5005·9868 / 4800·9000, p = 0.044 | image15 5005·9868 "34%", 4800·9000 "35%" | PASS |
| 1명씩, 2명씩 | 없음 cells | image3/image4 (1-vs-1 illustration, no counts) | PASS. `없음` replaces `--` (I13 closed) |

Columns 약 · 완치 · 비완치 are present; the three A-vs-A pairs and the 34%-vs-35% row are present. I8 closed.

### Issue-by-issue status

| ID | Status | Evidence |
| :-- | :-- | :-- |
| I1 | CLOSED | L351 "(5+1)/32 = 6/32 = 0.1875 … 관측값(앞4) + 더 드묾(앞5)만"; L354–355 explains why 0 heads is excluded; `tab:pv-three-parts-compare` L366 shows 6/32 = 0.1875 |
| I2 | CLOSED | L653–681 matches slides.md slide 20 and image44: the "P < 0.01 → reject → pears are different" line is flagged as the "If it did not overlap" hypothetical; the slide's actual conclusion is "0 is in the interval → P > 0.01 → fail to reject"; L678–680 now says the book and slide conclusions are the **same**, with no "반대 결론". The Apples typo (item 3) and the "the same" wording (item 4, `\Cref{tab:ht-wording}`) are kept |
| I3 | CLOSED | slide 11 flower point at L323–326 in `sec:pv-discrete` (matches slides.md slide 11 text). Slide-3 trial now tied into `sec:pv-why` at L104–106 |
| I4 | CLOSED (see N2) | L653 title has "슬라이드는 …, 바르게는 처음부터 끝까지 기각 실패다". L542 no longer says "각주로만 남긴다". Threshold point (L242–244) is now one plain paragraph + `\Cref{pit:ht-alpha}`, no new box |
| I5 | CLOSED | see mechanical table |
| I6 | CLOSED | caption L173 now points to `pit:pv-drug-2931`, not `pit:ht-fail-not-proof` |
| I7 | CLOSED | L139–140 gives 0.24 as the slide value with no pointer to a nonexistent calculation |
| I8 | CLOSED | see table above |
| I9 | CLOSED | χ², z, p, Yates now on separate lines (L205–225, L270–277); the vitamin D z is split into L531 (63−100 = −37) and L532 (−37/3.3 = −11.21). Single operations checked at L306, L308, L438–441, L533, L642 |
| I10 / I10b | CLOSED | `[[a,b],[c,d]]` notation explained (L194–197). Glossed with English: 카이제곱 검정(Chi-squared Test), Yates 보정(Yates' Continuity Correction), 피셔 정확검정(Fisher's Exact Test) (L197–203, one line each, with "계산식은 다루지 않는다"); 유의수준(Significance Level) / 신뢰수준(Confidence Level) in In brief L584–585 and table header L616; L688 거짓 양성(False Positive, 1종 오류/Type I Error); L690 2종 오류(Type II Error) |
| I11 | CLOSED | see recompute |
| I12 | CLOSED | L136 "(이 장은 이 값을 그대로 쓴다)", consistent with L130 and L157 |
| I13 | CLOSED | `없음` in L153 |
| I14 | CLOSED | L627–631 states the condition: the CI-to-p conversion holds only when the interval has the form 관측값 ± z·SE, and not for asymmetric or bootstrap intervals |

### Minor notes (non-blocking, implementation → sonnet-writer if a later pass happens)

- **N1 L151 column header.** The header reads `판정(p값 슬라이드)`, but three of the p-values in that column are the book's recomputed values, not slide values: 0.917 (slide 5: 0.9), 0.012 (image14: P=0.01), 0.044 (slide 7: 0.04). A header such as "판정(p값)" would be accurate. The numbers themselves are correct.
- **N2 L557–558 pitfall title.** "슬라이드는 연구 질문을 단측으로, 대립가설을 양측으로 적어 서로 어긋난다" states the slide side only. The "바르게는 …" half is in the first body sentence (L561). This is the same shape cycle 1 passed for the 62/63 title (L542), so it is recorded as PASS with a note, not an ISSUE.
- Residual: L337 `(5+5+2)/32 = 12/32 = 0.375` and L351 `(5+1)/32 = 6/32 = 0.1875` chain a sum and a fraction-to-decimal conversion on one line. Read as one computation plus its decimal form. Acceptable.

### Routing

No ISSUE remains. No reasoning or ladder/schema issue. N1 and N2 are optional wording touches, not required for T21 to close.
