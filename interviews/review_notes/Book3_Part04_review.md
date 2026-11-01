# Book 3 Part 04 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 50 questions, Q1-Q50. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (50 of 50 merged, 0 skipped, 0 pending). All four agents were interrupted once by a spend limit and resumed after the reset. Header status updated after the merge.

## Structure checks (scripted, scratch/review_scripts/check_book3.py)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q50 | pass |
| Star order and counts 19 / 19 / 12 | pass (matches header) |
| All template labels in every answer | pass for all 50 |
| Exactly one sqlite3 Code program per question, run standalone with `python3 -I` | 50 of 50 exit 0 |

## Code
Each program builds the data in SQLite 3.45.1, runs the SQL (window functions), runs pandas 3.0.5 and asserts SQL equals pandas with a stated sort and an explicit tie-break. Outputs pasted from real runs. Part 4 stays on ranking and top-N (running totals, LAG/LEAD, moving averages are Part 5; gaps-islands Part 7).

## Behaviours the Wave A note listed as unverified, now run (3.45.1 / 3.0.5)
SQLite NULLs sort smallest in window ORDER BY (ASC first, DESC last) and are peers; NULLS FIRST/LAST work; a named window without ORDER BY can be extended, one with ORDER BY or PARTITION cannot be overridden; window functions in WHERE, GROUP BY or inside an aggregate fail ("misuse of window function"); QUALIFY, DISTINCT ON, FETCH FIRST WITH TIES, PERCENTILE_CONT, IGNORE NULLS and NTH_VALUE ... FROM LAST are syntax errors; NTILE vs qcut bucket sizes and tie handling differ (3,3,2,2 vs 3,2,2,3; 11 of 23 customers in a different decile), reproducible with integer arithmetic on rank(method='first'); cumcount starts at 0; nlargest keep='all' equals RANK <= n; idxmax raises ValueError on all-NaN groups and with skipna=False when any NaN; qcut raises on duplicate edges (duplicates='drop' gives fewer bins); rank(pct=True, method='max') = CUME_DIST and (rank_min-1)/(n-1) = PERCENT_RANK, default average matches neither; default quantile is linear interpolation (nearest-rank differs in 3 of 5 departments); EXPLAIN QUERY PLAN shows temp b-trees per distinct window and an index on (partition, order, tiebreak) removes the sort for one window.

## Findings kept in the text
AVG OVER an ordered window is cumulative through peers, not the group average; MAX and RANK=1 differ when a group is all NULL; NULL-salary handling differs between SQL (ranked) and pandas (NaN dropped); keep-first with NULL dates picks different rows in SQL and pandas; tie order without a tie-breaker is unspecified (a second window changed it on 3.45.1); OFFSET -1 acts as 0 and N=0 returns the top value; OFFSET pagination repeats a row where keyset does not; CUME_DIST, NTILE, PERCENT_RANK and RANK <= ceil(n/10) select different counts for "top 10%"; pandas 3 copy-on-write removes SettingWithCopyWarning; pandas all-NaN sum is 0.0 unless min_count=1.

## Not verified (hedged "not executed" in the text)
QUALIFY support (BigQuery, Snowflake, DuckDB, Teradata, Databricks), DISTINCT ON (PostgreSQL, DuckDB), FETCH FIRST WITH TIES versions, PERCENTILE_CONT availability, NULL ordering defaults in PostgreSQL and MySQL, MySQL 8.0 window support, IGNORE NULLS support, MySQL error 1093, PostgreSQL division-by-zero error, NULLS FIRST/LAST needing SQLite 3.30+ (only 3.45.1 run), deep-OFFSET slowdown (not timed), other engines' EXPLAIN and top-N optimisations. Not run: NTILE with fewer rows than buckets, RANK <= 2 vs DENSE_RANK on NULL salaries (hand-worked), row-value keyset pagination elsewhere.

## Evidence limits
No candidate-reported window-function questions were found; evidence is prep guides, public problem banks (LeetCode 176/177/184/185 known only from snippets) and the SQLite, PostgreSQL and pandas docs listed in the sources note. No source states a salary band; salary values are toy column data. Stars and "Asked at" tags are indicative.
