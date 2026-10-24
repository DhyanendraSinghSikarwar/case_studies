# Review: Book 2 Part 07 (CASE WHEN, NULL handling, string and date functions)
Reviewer: Wave C. Environment: Python sqlite3 (SQLite 3.45.1), pandas 3.0.5, no DuckDB/PostgreSQL/MySQL/SQL Server.

## Counts
- Answers checked: 60 of 60 (headings, numbers, stars and order untouched).
- Executed OK (SQLite SQL matches printed Output, pandas matches SQL): 54. These are all answers except those below.
- Not fully executable here: Q33 (main query was DuckDB/PostgreSQL; SQLite version matches Output and was run), Q51 (regex; checked with Python `re`), Q59 (AT TIME ZONE; pandas half run, SQL not run), Q53 (concept, DDL only), Q56 (EXPLAIN plans re-run: both plans match), Q7 (output is the live clock, so cannot match).
- Answers with fixes: 12 (Q15, Q33, Q34, Q41, Q42, Q43, Q51, Q56, Q58, Q59, Q60, plus file-wide formatting).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q33 | Main SQL and "verified" claims relied on DuckDB, which is not available here | Relabelled `date_trunc` query as PostgreSQL syntax, not run; SQLite query marked as the source of the Output; DuckDB "verified" claim removed |
| Q34 | "DuckDB (run here)" line and bullet unverifiable | Removed the DuckDB line; bullet now says only SQLite was run |
| Q42 | pandas snippet wrong: `full.difference(att.work_date)` with text dates returns every day, not just 2025-03-05 | Added `pd.to_datetime` conversion; re-run gives 2025-03-05 |
| Q51 | SQL is DuckDB `regexp_matches`, claimed "run here" | Labelled not run here; flags verified with Python `re` (all 10 flags match) |
| Q59 | "run here in DuckDB" claim | Labelled PostgreSQL syntax, not run; pandas tz_convert run and matches 14:30 / 05:00 |
| Q15 | "MySQL returns NULL on /0" stated without qualification | Qualified: plain SELECT returns NULL, strict-mode INSERT/UPDATE can error (from memory) |
| Q43 | No note that SQLite supports `IS NOT DISTINCT FROM` | Added: SQLite 3.39+ (ran on 3.45.1); output verified |
| Q56 | No sample data or pandas field | Added sample-data line (499 generated rows) and "pandas: not applicable" with the equivalent filter |
| Q58 | Query question missing pandas equivalent | Added pandas snippet, run; matches all four SQL results |
| Q41 | Wording "HR has 3 IT staff" confusing | Reworded |
| Q41-Q60 | Sample tables unnamed, SQL not labelled, pandas used undefined names (att, tk, nm, ...) | Added table name above each sample table, "-- SQLite (run here)" label on SQL, and a comment naming each pandas DataFrame |
| Q1-Q60 | Tables ran straight into the following line with no blank line, so **SQL:** / **pandas equivalent:** would render as table rows | Inserted blank lines before and after every table (fences balanced: 260 fence lines) |
| Q33, Q60 | DuckDB/Snowflake/BigQuery function claims unqualified | Marked "from memory" / "neither run here" |

## Unresolved / report only
- Ordering OK: stars descending, then green, yellow, red; numbering continuous Q1-Q60. Header says Target 50, Actual 60 (fine).
- Overlap with each other or other parts (not edited): Q15/Q16 (NULLIF vs safe percentage), Q1/Q5/Q40 (NULL counting), Q13/Q43 (NULL comparisons), Q9/Q29 (concat with NULL), Q19/Q32/Q45/Q57 (text cleaning), Q8/Q54/Q56 (date filtering), Q42/Q60 (calendar CTE), Q30/Q31/Q49 (SUBSTR+INSTR), Q11/Q33 (group by month). Likely also overlaps Part 6/8 on COALESCE/dates; not checked.
- Q7 Output is a timestamp from the day it was run (2026-10-21), by design.
- Q16/Q15 Output shows `50` where SQLite prints `50.0`; cosmetic, left as is.
- Q41-Q60 SQL has no `;` terminator, and Q21-Q40 use a `-- table:` comment instead of a table name header; consistent enough, not changed.

## Claims labelled unverified (kept, marked "from memory / not run here")
Dialect behaviour for MySQL, PostgreSQL, SQL Server and Oracle (CONCAT NULL rules, DATEDIFF argument order, weekday numbering, collation defaults, LPAD truncation, group_concat_max_len 1024, CONVERT_TZ zone tables, IIF 10-level nesting, SQL Server 2017/2022 feature versions, MySQL DATETIME/TIMESTAMP ranges) are from memory; no docs or servers available. "Asked at" lines all say "commonly asked (no company-specific report found)", consistent with research/Book02_Part07_sources.md.
