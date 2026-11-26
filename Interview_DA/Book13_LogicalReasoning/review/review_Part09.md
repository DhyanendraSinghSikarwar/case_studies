# Review: Book 13 Part 9 (Data-analyst logic), Wave C

## Counts
- Answers checked: 60 of 60.
- Questions re-solved by code (sqlite3 3.53.1 for all SQL items; Python for truth tables, traces, series, decision tables, puzzles): 60 of 60. Q10, Q18, Q24, Q39, Q40, Q42, Q50, Q53, Q54 (Excel/PostgreSQL parts) cannot be run here; their sqlite3/Python parts were run.
- Answers wrong: 0. Final answers all matched the code output.
- Non-unique puzzles: 0 (Q60 unique: true-counts 2, 2, 1; Q27, Q59 gaps confirmed: YNN+NYN, and YNN with YYY overlap).
- Answers changed (wording in follow-ups or check lines only): 3.

Honest note: I read the written answers while loading the file, before running the code. The code was still written from the question and data lines and compared line by line, including every "Likely follow-ups" variant I could run.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q12 | Follow-up 1 said a "plain join" gives 5 rows. Only a plain LEFT JOIN gives 5; an inner join gives 4. | Reworded to "plain LEFT JOIN", added the inner-join count 4. |
| Q32 | Step 4 and Check listed `>=5000` as a "coding slip"; it is not a slip of the upper bound and changes 2500 too. "Four slips" were not named. | Removed it; named the slips (`>1000`, `>=1001`, `<=5000`, `<4999`) and which edge each flips (re-run: each flips exactly one edge, 2500 unchanged). |
| Q26 | Follow-up with OR was vague. | Stated the result: 111 passes, prints 1 111 (script). |

## Verified items (spot list of non-trivial results)
- Q1 table, Q6, Q15, Q22, Q57 NOT IN / NOT EXISTS outputs, Q16 four-column table, Q36, Q37 (inner 2, left 4, full outer 6), Q49, Q55 output all match printed sqlite3 output.
- Q3 only (b) is equivalent; Q23: 3 tautologies; Q46: 9, 7, 49; Q17: 4 (exactly-one gives 3).
- Q21 C1, C5, C6 (strict `>2` gives C1, C6; unbracketed gives C1, C2, C5, C6, as stated).
- Q33 f(6)=13, calls 25, f(5) calls 15, f(2) evaluated 3 times in f(5). Q34 33,000 (25,000 variant). Q35 3 (5 variant). Q51 [2,4,1,3,5], 4 swaps, 3 passes to sort. Q11 counts and both follow-ups. Q60 follow-ups (exactly two true, exactly one false: both non-unique).
- Q59 follow-up (Rule 2 as Y,N,Y): 7 covered, gap YNN: correct.

## Conventions and honesty
- "Asked at" lines are all "commonly asked (no company-specific report found)" or prep-site claims labelled unverified; consistent with research/Book13_Part09_sources.md. No change needed.
- Excel, PostgreSQL, MySQL, Oracle, SQL Server behaviour is labelled "from memory, not run here" throughout. Left unverified: Excel blank comparisons (Q10, Q18), COUNTIF "<>5" and SUMPRODUCT variant (Q24), text-versus-number comparisons (Q39, Q53), IF on numbers (Q40), AND over ranges (Q42), IFS #N/A (Q50), PostgreSQL 3.5000000000000000 display and error on divide by zero (Q54, Q55), `<=>`, MINUS, ALL set operators (Q16, Q36).
- Style: no em or en dashes in answers (only the part-title line), code fences balanced (68), no pasted verification scripts; SQL blocks carry real sqlite3 output.

## Unresolved / report only
- Overlap: Q23 (tautologies), Q41 (contrapositive), Q60 (exactly one statement true) are reasoning-style items that may resemble Book 6 Part 7 logic items; I did not read Book 6 Part 7 in this pass, so no near-copy flag is confirmed. Suggest a quick title grep at merge.
- Q14/Q31/Q15/Q22 and Q6/Q57 overlap each other on NOT IN and three-valued logic (deliberate variants, different data); Q9 and Q16 also overlap lightly. Consider thinning if the part needs trimming.
- Q5 follow-up says "script-verified for a 2-row all-NULL case" while talking about 8 rows; harmless, left as is.
- Ordering: stars descend 3, 2, 1 across Q1-15, 16-37, 38-60; Q15 is 3 stars but sits after Q14 red items: fine.
