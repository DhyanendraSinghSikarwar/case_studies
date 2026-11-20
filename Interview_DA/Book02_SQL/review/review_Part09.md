# Review: Book 2, Part 09 (Retention, Cohorts, Funnels, MoM Growth)

Reviewer: Wave C. Environment: Python sqlite3 (SQLite 3.45.1), pandas 3.0.5. Scratch: scratchpad/C_Part09 (h.py, h2.py, h3.py).

## Counts
- Answers checked: 46 (Q1-Q46).
- Executed OK: 46/46. Every sample table was rebuilt from the markdown; every runnable SQL block was run and matched the printed Output (Q9 alternative self-join returns users 1, 3, 5 as stated). The 6 MISMATCH hints in rerun.json (Q1, Q3, Q10, Q24, Q26, Q31) were harness limits: my own run matched.
- pandas: all 49 snippets run under pandas 3.0.5; each printed "Result (actual run)" is identical to the real result, and every value agrees with the SQL Output.
- Claims verified by execution: Q8 NOT IN with a NULL returns 0 rows; Q12 LAG(12) gives no growth on the gappy data; Q40 raw vs clean DAU (3 to 2) and 5 clean events; Q10 strict funnel (paid = 2); Q35, Q36, Q37, Q41, Q42 worked numbers in the Example lines.
- Fixed: 5 wording/claim fixes (no SQL or output changes needed).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q2 | Common mistakes said `100*(a-b)/b` with whole numbers "can be fine"; it still truncates decimals | Reworded: both forms drop decimals, use `100.0 *` |
| Q22 | "recursive CTE" used without explanation (first explained in Q5) | Added a short plain-words definition and pointer to Q5 |
| Q26 | "minute-truncating DATEDIFF" was vague/inaccurate | Now says SQL Server DATEDIFF(minute) counts minute boundaries crossed; labelled from memory, not run here |
| Q28 | "ROWS ... usually faster" unqualified performance claim | Qualified as "some engines ... from memory, not run here" |
| Q36 | "survival-style view" jargon in follow-up | Replaced with plain wording (count only customers old enough, as in Q41) |

## Checks passed
- Template: all 12 required fields present in all 46 answers; code fences balanced; tables render; no ANSWER_PENDING.
- Ordering: stars descending then green-yellow-red, numbering Q1-Q46 continuous, no changes needed.
- Asked at: only "commonly asked (no company-specific report found)" variants; consistent with research/Book02_Part09_sources.md; no company claims.
- Dialect claims (PostgreSQL DATE_TRUNC, MySQL YEARWEEK mode 1, SQL Server DATETRUNC 2022+, DATEADD, PIVOT availability) are labelled "not run here"; read by eye, look correct (from memory).

## Unresolved / unverified
- Non-SQLite syntax (PostgreSQL, MySQL, SQL Server, Oracle PIVOT, PERCENTILE_CONT, ROLLUP) was not run; judged by reading only.
- Q15 "about 20% stickiness is decent" and Q42 "NRR above 100% is good" are already labelled from memory/not sourced; kept.
- Q28 engine-speed claim is from memory.

## Overlap (report only)
- Q10 and Q33 both cover strict funnels (Q10 part 2 vs Q33 with timestamps): intentional, cross-referenced.
- Q6, Q11, Q34, Q38, Q41 share month-1 cohort logic; Q27 and Q35 share day-N retention; Q9 and Q30 share gaps-and-islands. Cross-references exist; no part-level duplicates found with other parts seen (Part 10 covers dedupe and recursive CTE per scope line).
