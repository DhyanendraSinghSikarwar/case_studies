# Review report: Book 2, Part 06 (window functions: running totals, LAG/LEAD, moving averages)

Environment: Python sqlite3 (SQLite 3.45.1), pandas 3.0.5, no duckdb. Own harness rebuilt every sample table from the markdown, ran every SQL statement and every pandas snippet, and compared with the printed Output and the printed pandas text blocks.

## Counts
- Answers checked: 52 of 52.
- Executed OK (SQL output equals printed Output, pandas equals SQL): 50 as printed.
- Not fully runnable in SQLite: Q40 Query 1 (RANGE with INTERVAL) and Q49 Query 1 (PERCENTILE_CONT). Their numbers were cross-checked against SQLite Query 2 and the pandas run (both match).
- Q20 and Q35 have no printed Output table to compare beyond SQL; SQL re-run matches and the new pandas matches it.
- Answers with at least one edit: 30 (18 only got a table-name label, plus the fixes below).

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q22, Q26, Q28, Q34 | pandas `res = d` had different column order or extra columns (emp_id) versus the SQL select list | `res` now selects the SQL columns in order; printed text blocks already matched |
| Q49 | "Portable (MySQL 8 / SQLite)" median used `(n+1)/2`; in MySQL `/` returns a decimal, so even-n medians would be wrong | Replaced by `rn BETWEEN n / 2.0 AND n / 2.0 + 1` (works everywhere); re-run in SQLite, same output; Explain and Common mistakes text updated |
| Q49, Q40 | Output labelled "run in duckdb", but duckdb is not installed here | Relabelled as PostgreSQL/DuckDB syntax, not re-run, numbers cross-checked |
| Q14, Q16, Q35, Q43 | Said SQL Server does not support the named WINDOW clause (it was added in SQL Server 2022); Q16 header comment claimed SQL Server support | Now "SQL Server 2022+ only (from memory)"; Q16 comment corrected |
| Q43 | Said NTH_VALUE exists in SQL Server 2022 and supports IGNORE NULLS there | SQL Server has no NTH_VALUE (from memory); IGNORE NULLS now Oracle only |
| Q20 | Same SQL Server claim; also no pandas equivalent | Claim corrected; pandas equivalent added and run |
| Q35 | Said SQLite 3.28+; no pandas equivalent | Version removed (ran on 3.45.1); pandas equivalent added and run |
| Q24 | Said SQL Server AVG of integers returns decimal (it returns an integer) | Corrected, marked from memory |
| Q39 | PERCENT_RANK described as fraction of "rows" below | Now "of the other rows" (formula is (rank-1)/(n-1)) |
| Q10 | Vague "MySQL and PostgreSQL differ" about RANGE offsets | Now says SQL Server does not allow it, from memory |
| Q45 | IGNORE NULLS support list unqualified | Marked from memory |
| Q52 | Follow-up claimed DuckDB allows approximate distinct windows (unsupported) | Replaced by "support varies, from memory; flag method works everywhere" |
| Q37 to Q52 (and Q40, Q46) | Markdown tables were followed directly by `**SQL:**` or `**pandas equivalent:**` with no blank line, which makes the bold line render as a table row | Blank line inserted after every such table (whole file) |
| Q19 to Q36 (18 answers) | Sample table had no table name | Added the name used in the SQL (`dsales`, `emp`, `orders`, `hc`, `logins`, `prices`, `msales`, `gr`) |

## Checks with no change needed
- Template: all 52 answers contain every required field (re-checked by script after edits). Code fences balanced.
- Ordering: stars descending, then green, yellow, red within each star; numbering Q1 to Q52 continuous. No problems.
- Q12 SQLite error text "misuse of window function AVG()" confirmed by running it.
- "Asked at": only Q4 names a company (Indium Software, AmbitionBox Feb 2024), which matches research/Book02_Part06_sources.md; all others say "commonly asked".

## Overlap (report only)
- Q7, Q32, Q33 (month-on-month difference, year-on-year, percent change) overlap Part 9 growth business cases; Part 06 keeps the mechanics only, which fits its scope line.
- Q17, Q25, Q39 (NTILE) and Q20 (ranking family) touch Part 5 ranking; Q26 notes ROW_NUMBER is in Part 5.
- Q4 and Q19 (LAG/LEAD offset) and Q9 and Q31 (moving vs running average) are close but teach different points. I did not diff other parts line by line.

## Unresolved / labelled unverified
- Not run here, labelled "from memory": all MySQL, SQL Server, PostgreSQL and Oracle dialect claims (SQL Server WINDOW clause 2022+, no NTH_VALUE, AVG of int, RANGE offsets, IGNORE NULLS, division-by-zero behaviour in Q33, PERCENTILE_CONT forms in Q49, MAXRECURSION default 100 in Q48).
- Q33 "SQLite and MySQL return NULL on divide by zero" is correct to my knowledge but was only run for SQLite.
- No duckdb: Q40 and Q49 first-query numbers rest on cross-checks, not a DuckDB run.
- Scratch harness: scratchpad C_Part06/h.py.
