# Review: Book 4 Part 12 (Q1-Q25)

## Counts
- Answers checked: 25 (Q1-Q25). Pandas snippets run OK with pandas 3.0.5: 7 (Q4, Q6, Q12, Q13, Q17, Q22, plus Q23 which reuses Q4/Q12/Q17). All printed outputs and Result lines matched.
- Answers fixed: 10 (Q2, Q6, Q7, Q10, Q12, Q13, Q14, Q20, Q21; Q12 twice).
- DAX re-derived by hand on the sample data: Q4 (shares), Q6 (75,000), Q12 (start 7, end 6, leavers 2, 30.8%, per-dept rates, mean of rates 0.267), Q13, Q17, Q22. All correct.

## Fixes
| Q | Wrong | Fix |
|---|---|---|
| Q2 | "central facts table" | "fact table" |
| Q6 | Excel/Power Query and Power Pivot overlap stated as fact | Labelled "from memory, unverified" (answer and version note) |
| Q7 | Account manager click-path not labelled | Added "from memory, unverified" |
| Q10 | Say-this "12 to 14 hours a week" contradicted its own arithmetic (10.5; 13 at 2 h weekdays) | Changed to "10 to 13" and added the 13 h note to the example |
| Q12 | Pandas snippet used undefined `tot`, `bd`; output omitted departments | Made snippet self-contained (ran it); added per-department output |
| Q13 | Vague "a community thread contradicted the docs in earlier notes" on DISTINCTCOUNT blanks | Replaced with "from memory, unverified", test on small table, DISTINCTCOUNTNOBLANK pointer |
| Q14 | PDF export claim and publish click-path unlabelled | Labelled from memory, unverified |
| Q20 | README example numbers (1,470 rows, finding) read as real | Marked illustrative |
| Q21 | "each roughly a quarter" while manage-and-secure is 15-20% | Reworded to "roughly a quarter each (the last a little less)" |

## Checks passed
- Template: all 25 answers have every required field; measure answers (Q4, Q6, Q12, Q13, Q17, Q22, Q23) have Sample data, DAX, Alternative, Result, Pandas check. All DAX/Steps labelled "not run here"; Results say "reproduced with pandas".
- "Asked at": only "commonly asked" plus source-backed notes (Coursera Dec 2025, Deloitte Sept 2025, market_skills_2026 JD counts); checked 13/40 = 32.5%, Tableau 12.5%, SQL 57.5% against research/market_skills_2026.md. OK.
- Numbering Q1-Q25 continuous; stars descending (3,3,3,3 then 2s, then 1s); within stars, the green-to-red order is not strictly sorted in places (Q4 is 3-star yellow after greens is fine; 2-star block mixes green Q5-Q10 then yellow Q11-Q18, fine). Not changed.
- Markdown: code fences balanced, tables followed by blank lines.

## Unresolved / unverified
- Q6/Q12/Q17 DAX uses `ISBLANK(column)` as a boolean CALCULATE filter and `<> 2024` on a column that includes blanks; believed valid, not runnable here (labelled from memory).
- Q7 licence tiers, F64 threshold, Mac statements, Q16 monthly cadence, Q19/Q21 PL-300 facts: rely on Microsoft pages recorded in the sources file (2026-03 to 2026-10); could not re-fetch.
- Q9/Q22 IBM HR Attrition dataset (1,470 rows) and licence, Q18 Tableau Public, Q5/Q15 Copilot licensing, Q14 Publish to web and refresh without gateway: from memory, unverified (already labelled).
- Q12 DAX Opening HC is a simplified, hard-coded assumption (labelled in the answer).
- Header says target 20, actual 25 (not changed). Sources file refers to 27 questions (Q1-Q27), stale vs 25.

## Overlap (report only)
- Q13 (DISTINCTCOUNT), Q12 (attrition), Q17 (payroll per head) and Q22 overlap in topic with DAX parts (Parts 4-5) and Book 1/2 Part 12 learning-journey questions; all use unique Part 12 sample data, so no duplicate text found.
