# Wave C review: Book 2, Part 04 (Subqueries and CTEs)

Reviewer: Wave C. Environment: Python sqlite3 (SQLite 3.45.1), pandas 3.0.5, no DuckDB.

## Counts
- Answers checked: 55 of 55 (every Q read in full).
- Executed OK: 52 answers. SQL rebuilt in SQLite from the markdown tables and compared with the printed Output; all pandas snippets run and compared. Q8, Q13, Q18, Q29, Q37 had to be re-run by hand-built tables because the sample section omitted a table (see fixes).
- Not executable here: Q10 (other-DB error text), Q26 (ANY/ALL; MAX/MIN equivalents were run), Q46 (LATERAL; output checked by hand and by the pandas version). Q38 non-SQLite syntax read only.
- Answers edited: 22. No question heading, number, star or order was changed.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| 6 | No pandas equivalent | Added (both averages), run |
| 8 | Sample data lacked `departments` although the SQL joins it | Added the table |
| 9 | Example said "HR 2, IT 3 vs average 2" (HR is not above 2); no pandas | Corrected wording; added pandas, run |
| 10 | Claimed "DuckDB was run here" (not installed) and printed a DuckDB error as output; no pandas | Relabelled error texts as from memory / not run here (PostgreSQL text, Oracle ORA-01427 added); added pandas, run |
| 15 | Index row said only materialized views; omitted SQL Server indexed views | Added, marked from memory |
| 20-35 | Boilerplate comment "employees, customers... are DataFrames" was misleading | Replaced (replace_all) |
| 24, 26 | No pandas equivalent | Added, run |
| 28 | No sample data, no pandas; PostgreSQL CTE sentence vague | Added sample table and pandas; clarified (CTE used 2+ times is computed once); SQLite plans re-run and match |
| 29 | Output said "8 rows left" (3 rows are shown); `departments` table missing | Fixed to 3 rows; added departments table; SQL and pandas re-run, match |
| 34 | SQL output showed prev_total as 500.0 / 800.0 (SQLite prints ints) | Changed to 500 / 800 |
| 36 | No sample data, no pandas | Added both; plans re-run and match |
| 37 | No `departments` / `leavers` setup, no pandas | Added tables and CREATE note, added pandas; all three statements run, outputs match |
| 38 | No sample data, no output for first query, no pandas | Added all three; run |
| 41 | "Sales" for dept 2 (no departments table in that dataset) | Changed to "department 2" |
| 44 | Called the subquery-in-LIMIT form valid for MySQL (MySQL rejects it) | Relabelled: SQLite verified, PostgreSQL from memory, MySQL not supported |
| 46 | Said "run on DuckDB" (not installed) | Marked not run here; output hand-checked and matched by pandas run; version numbers marked from memory |
| 48 | `USING` shortcut offered without noting SQL Server lacks it | Replaced by ON form with note |
| 51 | Example said Bala is above average in 2022 and 2024; 2024 is false (61,000 < 65,500) | Corrected text (above only in 2022) |

## Verified by execution (no change needed)
Q1-Q5, Q7, Q11, Q12, Q14, Q16-Q25, Q27, Q30-Q33, Q35, Q39-Q43, Q45, Q47, Q49, Q50, Q52-Q55 (SQL output exact match; pandas matches). Q13 error text `no such table: dept_hc`, Q18 NOT IN returns no rows and NOT EXISTS returns Legal after adding a NULL-department employee, Q46 SQLite error `no such column: d.dept_id`, Q28/Q36/Q39/Q53 SQLite plans: all confirmed.

## Claims labelled unverified (from memory / not run here)
- Error messages and numbers for PostgreSQL, MySQL (1242, 1093), SQL Server (512) and Oracle; LATERAL, EXPLAIN ANALYZE and CTE-support version dates (Q38 table, already labelled by the author); indexed views; PostgreSQL 12 CTE inlining; row-value IN on SQL Server; FETCH FIRST WITH TIES versions.
- "Asked at" lines were compared with research/Book02_Part04_sources.md and research/interview_processes.md; all supported (Meesho, Infosys, Deloitte, Wipro, Amazon, Microsoft Hyderabad, Indium panel). No additions.

## Unresolved / report only
- Pandas equivalent still absent on Q13 and Q15 (pure scope/object-lifetime concepts, no sensible pandas form).
- Q20-Q36 use a second employees dataset (with left_date; HR 55k, Sales 250k total, IT 320k) while Q1-Q19 use the Q1 dataset, and Q39-Q55 use a third. Each answer is self-consistent; consider a note in Part 4 intro.
- Q47 sample shows `ASHA@x.com ` with a trailing space that is invisible in rendered markdown; output is correct either way.
- Q20-Q36 pandas snippets store the answer in `res`, others in `result` (cosmetic).
- Ordering: stars descending and difficulty green to red within each star: correct. Numbering Q1-Q55 continuous. Code fences balanced (246). Zero ANSWER_PENDING.
- Overlap (report only): Q36/Q5/Q19 (correlated per-department average), Q14/Q41 (row-value IN, near-identical), Q23/Q27/Q55 (compare group size with average group size), Q7/Q24/Q50 (nested to CTE refactor), Q8/Q24 (average of department totals), Q47 and Q52 overlap Part 10 by design.
