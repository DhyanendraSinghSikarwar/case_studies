# Review: Book 6, Part 8 (Data Interpretation)

Reviewer: Wave C, Part 08. File: `Book06_Aptitude/Book06_Part08.md`. Scratch script: `/tmp/claude-0/-home-user-case-studies/7227d798-1dc4-5a0c-b272-858a37cce3c1/scratchpad/C06_Part08/v.py`.

## Counts
- Answers checked: 94 of 94.
- Re-solved by code (each inline table re-read, every figure, step, Check and follow-up number recomputed with exact fractions or floats): 80 numeric items. The other 14 are concept or method items (Q1, Q2 partly, Q13, Q33, Q70, Q73, Q79 to Q81, Q89, Q92 to Q94 and similar); their worked mini-examples and numbers were recomputed too.
- Wrong answers (final answer): 0.
- Answers changed (any fix, including wrong follow-up, wrong sub-figure, wording): 12 (Q2, Q10, Q12, Q20, Q33, Q37, Q52, Q64, Q78, Q82, Q85, Q94); of these, 4 were substantive numeric or logic errors (Q20, Q82, Q37 incomplete, Q78 muddled), the rest assumption or wording fixes.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q20 | Compound rate quoted as 16.99%; (150/80)^(1/4) - 1 is 17.02% | Corrected to 17.02% |
| Q82 | Follow-up (20-30 band = 35, total 120) said the 60th/61st person is in 30-40; the 61st is in 40-50, so the median sits on the boundary | Rewritten: median at about 40 thousand, on the 30-40 / 40-50 boundary |
| Q37 | Follow-up gave only South's share move, no answer to "whose share rose most" | Added all four shares (South +1.50 pts, North +1.37, West and East fall) |
| Q52 | "Offer accepted = joined / offered" relied on an unstated assumption | Stated: everyone who accepted joined (no separate "accepted" row) |
| Q64 | "Selected" treated as "hires" without saying so | Assumption stated in step 1 |
| Q85 | Margin base not stated | Stated: margin taken on revenue |
| Q78 | Fast method sentence ("fell only 10 because pie grew 25%") mixed points, lakh and percent | Reworded: share down 10 points, rupees down 10 lakh (6.25%) |
| Q10 | Check claimed "verified by script" for a plain range sanity check | Relabelled as a sanity check, total confirmed by script |
| Q12 | Trap text ("stopping before January") did not make sense (January is the first row) | Reworded |
| Q2 | "Points always smaller than percent change" was unqualified | Added "in size" |
| Q33, Q94 | Thresholds (a few percent, 90 seconds, 15 to 20 seconds) read like fixed rules | Labelled as rules of thumb |

## Verified correct (no change needed)
All final answers and working: Q3-Q9 (16%, IT 30%, 6%, Rs 6,00,000, 64.8, 10:3, Rs 4,80,000), Q10-Q12, Q14-Q19, Q21-Q32, Q34-Q36, Q38-Q41, Q42-Q48, Q49-Q51, Q53-Q63, Q65-Q69, Q71-Q72, Q74-Q77, Q83-Q84, Q86-Q88, Q90-Q91. Follow-up and trap numbers also recomputed (for example 16.8% mean of department growth rates, 6.38%, 63.33 versus 62, 36.57%, 32.67%, 12.14%, 10.63%, 47.37%, 182.25, 9.81%, 78.33, 67.89, 303.75, 237.5%, 16.5%, 5.61, 1,980, 44.21%, 43.33%, 2.64). Shortcuts checked: successive change (Q74 a + b + ab/100), reverse percentage (Q71 x/(x+y)), CAGR roots (Q42, Q43, Q91), share-times-total (Q67, Q68), weighted averages, 3.6 degrees per percent, moving-average slide (Q86). All valid for the stated cases.
Rounding: Q30 (21.875 to 21.88 half-up) and Q49 (20.2586 to 20.26) confirmed.

## Claims
- "Asked at" lines match `research/Book06_Part08_sources.md` and `interview_processes.md`: Novartis pie-chart report (Sept 2025, snippet-level, mapping to specific questions unverified) and TCS/Infosys/Accenture/others as prep-site claims (unverified). No invented companies found. No change needed.
- Q13 Accenture axis/unit claim is supported by the Accenture guide row in the sources file (prep site, unverified).

## Style checks
No em dashes in answer text (title line only), no code fences, blank line after every table, no pasted scripts.

## Unresolved / report only
- Ordering/numbering: none; star blocks run 3-star (Q1-Q45), 2-star (Q46-Q78), 1-star (Q79-Q94) in order. Header says "Target 80, Actual 94" (left as is).
- Q54 and Q71 "Asked at" use odd phrasings ("3-star-level", "3-star-style") although Q54/Q71 are 2-star; cosmetic, left unchanged.
- Duplicate/overlap: Q35 (attrition on average headcount) and Q60 (weighted attrition) may overlap with attrition items in HR-metrics parts; Q42/Q43/Q91 (CAGR) overlap with each other and likely with compound-growth items in other Book 6 parts. Not checked against other parts.
- Several datasets repeat across questions by design (headcount, A/B monthly sales, payroll, funnel, pie shares).

## Left unverified
All prep-site frequency claims (TCS NQT, Infosys, Accenture lists) and the Novartis pie-chart report; time-per-question guidance in Q94 is rule of thumb.
