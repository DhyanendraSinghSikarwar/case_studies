# Review Part 03 (Book 13, inequalities, comparison, ranking, order puzzles)

## Counts
- Answers checked: 51. Questions independently re-solved by code (before comparing): 51 (inequalities by enumeration of integer models, order puzzles by full permutation search, ranking and counting by direct computation; Q48, Q50, Q51 minimum-comparison results use the known formulas n-1, ceil(3n/2)-2, n+ceil(log2 n)-2, not re-derived).
- Stated final answers wrong: 0. Non-unique or not forced: 0 (Q7, Q14, Q18, Q19, Q31, Q41, Q43, Q44 each have exactly one valid order).
- Answers changed because of errors in follow-ups or wording: 8 (list below). Formatting-only edits: tables.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q12 | Either-or list had a vague "= with one other" pair and a stray space in "> " | Reduced to the real complementary pairs |
| Q13 | Fast-method condition 3 garbled ("= and not-equal combined with > and <") | Rewritten as complements (> with <=, < with >=) |
| Q14 | Follow-up claimed third is still A without the F clue. False: F becomes free, third can be A, D or F | Corrected to "cannot be determined" with reason |
| Q16 | Mistakes line gave a muddled reason for 9+12+15=36 | Explained why it works and why to avoid it |
| Q23 | Called Q19's "D after A" a negative clue | Reworded as a plain ordering clue in the same final role |
| Q28 | Follow-up said B <= D makes F < D definite. False (gives F <= D only) | Needs strict B < D |
| Q32 | "at most 22 above-or-equal" unclear | Reworded (22 people at or above him, himself included) |
| Q39 | Follow-up question garbled ("less than Yash's rank counting Zoya") | Rewritten as "How many scored below Zoya?" (31) |
| Q40 | Claim that exams normally accept either-or when conclusions are >= and <= stated as fact | Labelled as from memory, unverified, and noted that both can be true at equality |
| Q45 | Follow-up "add D before E too: 120/8 = 15" wrong; correct is 10 (confirmed by brute force) | Corrected with reasoning |
| Layout | Tables lacked blank lines before or after (Q18, Q19, Q21, Q26, Q31, Q34, Q35, Q37) | Blank lines added |

## Verified without change
All main answers and the follow-up variants in Q1-Q11, Q15, Q17-Q22, Q24-Q27, Q29-Q31, Q33-Q38, Q41-Q44, Q46-Q51 reproduced by code (including Q11 variant, Q18 two queues without the Q-not-5th clue, Q19 second schedule, Q30 and Q38 follow-ups, Q31 non-unique when B may be last, Q42 variant giving 9, Q26 chaining table). Q42 count of 371 models (values 0 to 5) confirmed.

## Conventions
"Definitely follows" = true in every model; strict versus non-strict stated; rank from top = people above + 1; competition versus dense ranking both stated (Q21); "between" excludes endpoints; queue position 1 = front. No further convention gaps found. Q9 states the 75% reading (share of all 40 below her).

## Honesty
All "Asked at" lines say "commonly asked (no company-specific report found)" or cite only the prep-site claims in research/Book13_Part03_sources.md (Testbook, placement-prep page), marked unverified. Q25 time budget and order are labelled "our suggestion". SQL RANK/DENSE_RANK in Q21 is labelled from memory, not run.

## Style
No em or en dashes in answer text (title line keeps one). No code fences. No verification scripts pasted. The "Verified by script" lines in answers are now true for the items I re-ran; Q48, Q50 and Q51 say hand-checked/known result (their "simulated 2000 random orders" claims were not re-run by me, left as written).

## Unresolved / report only
- Ordering/numbering: Q10 to Q13 and Q28 to Q30 repeat the same coded or either-or skill; stars and order left unchanged. Heading says 50 target, 51 actual (consistent).
- Overlap: not compared line by line with Book 6 Part 7; no near copy noticed, but Q14, Q24 and Q45 to Q47 are generic enough to overlap Book 6 reasoning items, worth a dedupe check.
- Unverifiable: the lower bounds in Q48, Q50, Q51 (known results, not re-derived); all prep-site claims.
