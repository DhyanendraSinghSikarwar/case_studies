# Review: Book 2 Part 08 (Scenario business queries), Wave C

Reviewer scope: `Book02_SQL/Book02_Part08.md`, 74 answers (Q1-Q74). Environment: Python sqlite3 (SQLite 3.45.1), pandas 3.0.5, no duckdb.

## Counts
- Answers checked: 74
- Executed OK (SQL output matches the printed Output, pandas matches SQL): 73 of 74 after fixes. Q73's second (MEDIAN) query is not SQLite and was not run; its main query ran OK.
- Answers fixed: 18 (Q3, Q6, Q10, Q11, Q12, Q13, Q15, Q18, Q19, Q25, Q28, Q31, Q32, Q33, Q35, Q38, Q73, Q74; Q33 and Q73 are wording fixes; Q25/28/31/32/35/38 share one defect type, see table).
- Not changed: headings, numbers, stars, order. Template fields: all 74 have every required field (checked by script). Order (stars descending, then green/yellow/red) and numbering Q1-Q74 are correct. Code fences balanced.

## Method
Each answer's sample tables were parsed from the markdown, loaded into SQLite, every SELECT run and compared with the printed Output tables (values and column names). Every pandas snippet was run statement by statement and compared with the SQL result. Scripts are in the scratchpad folder C_Part08 (h.py, run.py).

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q3, Q6, Q10, Q12, Q13, Q15, Q18, Q19, Q74 | Sample data was cut ("first 8 of N rows shown"), so the printed Output could not be reproduced from the page (running the shown rows gave different numbers). | Rebuilt the hidden rows so that the full table reproduces the printed Output and the Example text, and printed the full table (Q3 +2 rows, Q6 +2, Q10 +4, Q12 +5, Q13 all 32, Q15 +20, Q18 +4, Q19 +45, Q74 +6). Re-ran: SQL and pandas now match the Output. The added rows are author-constructed sample values, not sourced data. |
| Q13 | The 8 "working days" included Saturday 7 Mar and Sunday 8 Mar, contradicting the Edge-case line that weekends must not be in the denominator. | Full table uses 8 weekdays (2-6, 9-11 Mar 2026). Attendance counts unchanged (emp 2: 5, emp 3: 6, emp 4: 4 of 8). |
| Q6, Q11, Q12 | pandas snippets used the variable `today` without defining it (NameError). | Added `today = pd.Timestamp("2026-10-21")` (the same fixed date as the SQL). |
| Q25, Q28, Q31, Q32, Q35, Q38 | Plain-text captions ("All orders in the denominator", "Products to re-order", "Correct: NOT EXISTS", etc.) sat inside python code fences as bare lines, a SyntaxError if pasted. 11 such lines in total. | Turned each into a `# comment`. After the fix every pandas block parses and matches. |
| Q33 | Sample note said "Employee 3 as in the example"; hidden 84 rows not reproducible from the page. | Spelled out Employee 3 (15 days of 12 h + 5 days of 6 h) and said how it was checked. A rebuilt 84-row set gives exactly the printed Output (3: 45.0, 1: 44.0). The exact 84 rows are still not printed (too long); stated openly. |
| Q73 | Claimed the MEDIAN query "ran in DuckDB here and matched", but this environment has no DuckDB. | Reworded to "not run here, from memory" (MEDIAN exists in DuckDB, Snowflake, Oracle). |

## Verified as correct without change
Q1, Q2, Q4, Q5, Q7-Q9, Q14, Q16, Q17, Q20-Q24, Q26, Q27, Q29, Q30, Q34, Q36, Q37, Q39-Q72: SQL output and pandas equal the printed Output exactly. Q25 and Q38 harness warnings were harness limits (pandas result built in two steps / two result sets), checked by hand: correct. Q31 "NOT IN with a NULL returns nothing" confirmed empty by execution. Q64 duplicate-result warning is also a harness artefact.

## Claims labelled unverified
- Non-SQLite dialect lines (PostgreSQL, MySQL, SQL Server date/interval/TOP/EXTRACT syntax, MEDIAN, PERCENTILE_CONT) are marked "not run here / from memory" in the file; I read them for syntax only.
- "Asked at" lines (11 of 74 carry a source note) cite only sources listed in `research/Book02_Part08_sources.md`; all are consistent with it. The other 63 say "commonly asked (no company-specific report found)", which makes no company claim.
- Q33 hidden 84 rows: reconstructed, not printed (see above).

## Unresolved / observations
- Beginner clarity was spot-checked (Q1-Q22 read in full; later answers scanned for term definitions); no jargon fixes were needed beyond those above.
- Overlap with other parts (report only): Q10 and Q18 (attrition, roll-forward) overlap with Part 9 retention/cohort topics only in theme; Q18 vs Q37 (voluntary split) and Q36 are distinct. Q3 and Q20 are related to Part 10 "nth highest/top N per group"; Q74 deciles may overlap a Part 9/10 NTILE question. Not checked against other parts' text.
