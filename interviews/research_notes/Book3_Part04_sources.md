# Book 3 Part 4 — Sources & research notes (Window functions: ranking, top-N per group)

Date: 2026-10-24. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch returns a model-summarised view ("as summarised"). No candidate-reported questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found; every source is a prep guide, practice-site page, documentation page or a search snippet.

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| SQLite window functions | https://www.sqlite.org/windowfunctions.html | official docs | 11 built-ins; windows only in result set and ORDER BY; ntile larger groups first; percent_rank and cume_dist formulas; nth_value NULL when no Nth row; default frame RANGE ... UNBOUNDED PRECEDING AND CURRENT ROW; peers; WINDOW clause position; 3.25.0 / 3.28.0 history. Does NOT say how NULLs sort in window ORDER BY |
| PostgreSQL window tutorial | https://www.postgresql.org/docs/current/tutorial-window.html | official docs | window vs GROUP BY, OVER, PARTITION BY, evaluation after WHERE/GROUP BY/HAVING, subquery pattern for top-N (row_number, pos < 3), WINDOW clause, ties numbered in unspecified order |
| pandas DataFrame.rank | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rank.html | official docs | method average/min/max/first/dense, na_option keep/top/bottom, ascending, pct example (0.625 for tied pair), float output |
| pandas qcut | https://pandas.pydata.org/docs/reference/api/pandas.qcut.html | official docs | equal-frequency bins, labels=False, duplicates raise/drop, vs cut |
| LetsDataScience window-function interview guide | https://letsdatascience.com/blog/sql-window-functions-interview-questions | blog guide | 14 sample questions: top earner per dept with ties, Nth highest (LC 177), top products per category, quartiles, top 5 percent per state, top 3 distinct salaries per dept; gotchas on ties, NTILE, QUALIFY |
| datadriven.io window-function practice problems | https://datadriven.io/sql/window-functions-practice-problems | practice-site | dedup latest per key with order_id tie-break, top-N with ties (DENSE_RANK), LAST_VALUE frame trap, share of partition; NTILE listed at 0.9 percent frequency (page says low priority); no median problem |
| techinterview.org window gotchas | https://www.techinterview.org/post/3233476114/sql-window-functions-interview-gotchas/ | blog guide | tie behaviour, RANK = 2 returning nothing, window in WHERE and QUALIFY, "aggregate, then rank", default RANGE frame; does not cover LAST_VALUE or NULL ordering |
| GeeksforGeeks SQL interview questions | https://www.geeksforgeeks.org/sql/sql-interview-questions/ | prep guide | entries: RANK vs DENSE_RANK vs ROW_NUMBER (19), window functions (54), duplicates without DISTINCT (65), delete duplicates keeping first (86); no nth-highest, top-N or NTILE entry |

## Fetch failed
- pandas DataFrameGroupBy.cumcount reference: 404 (cumcount, groupby head, nlargest keep='all' and idxmax NaN behaviour were NOT opened; Wave B must run them).

## Search results only (snippets, not opened)
- LeetCode 176, 177, 184, 185 known from Scribd uploads, hieast-bedrock.readthedocs.io (177: DISTINCT/ORDER BY/LIMIT OFFSET inside a function) and a 1point3acres forum post (185 as "no more than three higher salaries in the department"; 184 via join with MAX). No official LeetCode page opened; problem statement wording unverified.
- dataford.io top-three-paid-per-department question, notion "SQL Interview Patterns" (top N per group), risingbrain.org top-n-per-group, dbgate.io window tutorial, datavidhya, ai2sql, sqlauthority (Interview Question of the Week #156), datadriven cheat sheet: patterns echo the opened guides. One blog claims a top-per-department problem appears on DataLemur and is reported by candidates; secondhand, not verified.
- NTILE docs (Spark, Databricks, Redpanda, SelectDB) and a towardsdatascience cut/qcut article: NTILE positional with extra rows to earlier buckets in one implementation; cut equal-width, qcut equal-frequency. Not opened.
- StrataScratch and DataLemur company-labelled window problems: search surfaced no actual problem pages; company links unverified.
- India-company specifics: no window-function-specific candidate reports found.

## Provenance of the 50 questions
- Guide-supported: window vs GROUP BY, ROW_NUMBER/RANK/DENSE_RANK ties, window in WHERE, top-N per group, nth highest, department top three, dedup latest, finding duplicates, rank an aggregate, percent of group total, quartiles/NTILE, top percent per group, first/last value trap, choosing the function.
- LeetCode-style (snippets only): 176, 177, 184, 185 analogues.
- Documentation-supported: PERCENT_RANK/CUME_DIST, named windows, default frame, NTH_VALUE, NULL ordering (partly), pandas rank/qcut.
- Expert gap-check only: Nth transaction per user, rank in filtered subset, outer vs OVER ORDER BY, join fan-out before ranking, multi-criteria dedup, decile Pareto, window performance, pagination, pandas cumcount/idxmax/top-N, DISTINCT interplay, tie-rule top-N.
- Candidate-reported: none.

## Unverified; Wave B must hedge or run
- NULL ordering in SQLite window ORDER BY (run; NULLS FIRST/LAST needs 3.30+ from general knowledge) and PostgreSQL/MySQL defaults (hedge).
- QUALIFY engine list, DISTINCT ON, FETCH FIRST WITH TIES (PostgreSQL 13), PERCENTILE_CONT/DISC availability, MySQL 8.0 window support, IGNORE NULLS: hedge, not executed.
- Whether SQLite allows extending a named window inside OVER (run).
- pandas: cumcount from 0, groupby head, nlargest keep='all', idxmax with NaN/all-NaN groups, quantile default interpolation, rank with groupby and nullable ints, qcut ties and duplicates='drop' (run on pandas 3.0.x).
- NTILE vs qcut bucket differences and pandas rank(pct=True) = rank/n equivalence to CUME_DIST (method='max'): run and assert.
- LeetCode problem statements for 176/177/184/185 (wording only from snippets).
- Join-fan-out and EXPLAIN QUERY PLAN output text on SQLite 3.45 (run).
