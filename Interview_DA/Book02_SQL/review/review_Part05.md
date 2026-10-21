# Review: Book 2, Part 05 (window ranking, top-N per group)

Reviewer: Wave C. Environment: Python sqlite3 (SQLite 3.45.1), pandas 3.0.5, no DuckDB.
Method: a harness rebuilt each answer's sample tables from the markdown, ran every SQL block on SQLite, compared with the printed Output tables, ran every pandas snippet and compared it with the SQL result and with any printed pandas output. Anything the harness could not parse was checked by hand (Q23, Q32, Q46, Q53, Q58, Q60, Q61, Q62, Q67, Q31, Q68).

## Counts
| Item | Count |
|---|---|
| Answers checked | 71 (Q1-Q71) |
| Executed and matching SQL Output + pandas | 64 |
| Not executable on SQLite, labelled "not run here" | 3 (Q53 LATERAL, Q70 QUALIFY, Q62 index plan re-run by hand: matches) |
| Intentional error demos, errors reproduced | 3 (Q13, Q23, Q67) |
| Random output, SQL runs, rows illustrative only | 1 (Q60) |
| Answers edited | 14 (Q23, Q31, Q40, Q41, Q43, Q45, Q48, Q53, Q56, Q60, Q62, Q68, Q70 plus layout fix across 40+ answers) |

No wrong SQL result was found. Defects were in sample data, pandas row order, version claims and layout.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q43 | Sample data showed 6 order rows, but Output named C18/C20 and a "20 customers" claim; reader could not reproduce. | Replaced with a 21-row orders table (20 customers, C20 has two orders). Re-ran SQL and pandas: output unchanged (C20 3500, C18 3240). |
| Q53 | Sample data had only HR and Sales rows but Output listed Eng and Support. LATERAL cannot run on SQLite, and the "verified in DuckDB" claim could not be re-checked. | Sample data now the full 18-row table. Added a "not run here" note; Output verified with the equivalent ROW_NUMBER query on SQLite. Version note marked from memory. |
| Q48 | Claimed SQLite 3.49.1 and DuckDB 1.5.6 verification; this environment has SQLite 3.45.1 and no DuckDB. Query used `employees` with no table named. | Changed to 3.45.1, removed DuckDB claim, output cell updated, pointed to the Q37 table. |
| Q62 | Plan text quoted from SQLite 3.49 with subquery labels that differ in 3.45.1. | Re-ran on a generated 50,000-row table: same behaviour (temp B-tree before the index, `USING INDEX` after, 15 rows). Updated labels and version, noted labels vary by version. |
| Q70 | QUALIFY output claimed "run in DuckDB 1.5", not re-runnable here; support list said "verified for DuckDB". | Relabelled as not re-run in review; subquery result shown as SQLite 3.45.1; support list marked from memory. |
| Q55 | "Main query was run in SQLite 3.49"; "runs unchanged on PostgreSQL/MySQL/SQL Server/Oracle" unqualified. | Version corrected, cross-dialect claim marked not run here / from memory. Both queries re-run: OK. |
| Q40 | pandas `res` row order differed from the SQL Output order. | Added `.sort_values(['dept','name'])`; now identical. |
| Q41 | Same: pandas row order differed from SQL. | Added sort matching the SQL ORDER BY; now identical. |
| Q56 | Edge case said NULL sorts "last in SQLite/MySQL for ASC". Wrong: SQLite/MySQL/SQL Server treat NULL as smallest (first on ASC). | Corrected, cross-referenced Q32, marked from memory for other engines. |
| Q23 | "can't use a SELECT alias in WHERE" is false for SQLite (it allows plain aliases). | Reworded to "most databases"; window alias still errors in SQLite (verified). |
| Q45 | SQL Server COUNT(DISTINCT) window claim unqualified. | Marked from memory, not run here. |
| Q60 | `MD5(emp_id \|\| 'seed')` is not valid in MySQL and needs a cast in PostgreSQL. | Replaced with PostgreSQL and MySQL forms, marked not run here. |
| Q31, Q68 | Query answers had no pandas equivalent. | Added short pandas snippets; run on pandas 3.0.5, results equal the SQL tables. |
| Layout (Q19-Q71) | 133 places where a markdown table touched the preceding or following line (`Table `emp`:` then `\| ... \|`, or table then `**SQL:**`), which breaks table rendering in GFM. | Inserted blank lines only; no text changed. Backup of the pre-fix file kept in the scratch folder. |

## Checks with no change needed
- Template: all 71 answers have Asked at, interviewer check, Say this, Explain simply, Example, Likely follow-ups, Common mistakes. Query answers have Sample data, SQL, Output, pandas, Edge cases. Q23, Q48, Q62, Q67, Q70 are concept or error demos with no pandas (acceptable per template).
- Order and numbering: Q1-Q71 continuous; stars descending, then green/yellow/red inside each star. No issue.
- "Asked at": every answer says "commonly asked (no company-specific report found)" optionally with "generic prep sources list ..."; consistent with `research/Book02_Part05_sources.md`. No invented company claims.
- Code fences balanced (even count); no ANSWER_PENDING left.
- Header says Target 65, Actual 71; consistent with the answers present.

## Unresolved / notes
- Q37-Q53 pandas snippets use the variable `emp` for the `employees` table (comment in snippet says so). Works, slightly confusing; left as is.
- Q60 output is random by design (one real run shown); pandas snippet uses a fixed seed and gives different people, not claimed equal.
- Pandas snippets in Q19-Q36 and several later answers show no printed pandas output, only "(result checked equal to the SQL output)". I verified this by execution; printing output was not added.
- Overlap (report only): Q12 / Q29 / Q47 / Q57 / Q71 all explain DENSE_RANK vs RANK gaps; Q10 / Q14 near-identical top-N pattern; Q13 / Q23 / Q41 / Q67 all explain "window function not allowed in WHERE". Part 10 (nth-highest, dedup) and Part 06 (running totals) are referenced but not duplicated.

## Claims labelled unverified (from memory / not run here)
Dialect NULL ordering defaults (PostgreSQL/Oracle vs others); NULLS FIRST/LAST support; RANK without ORDER BY on SQL Server/Oracle (Q9); window-function version history in Q48 (PostgreSQL 8.4, MySQL 8.0, SQLite 3.25, MariaDB 10.2, SQL Server 2005/2012); LATERAL/CROSS APPLY support and MySQL 8.0.14+ (Q53); QUALIFY support list (Q41, Q67, Q70); named WINDOW in SQL Server (Q2, Q28, Q51); IGNORE NULLS in Oracle/SQL Server 2022 (Q51); SQL Server integer AVG and COUNT(DISTINCT) windows (Q54, Q45); TOP/FETCH WITH TIES (Q34, Q37); date functions in Q27, Q33, Q58; MySQL RAND, SQL Server NEWID (Q60); BigQuery QUALIFY clause requirement (Q70).
