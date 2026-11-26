# Review: Book02_Part02 (Aggregates, GROUP BY, HAVING)

Environment: Python sqlite3 (SQLite 3.45.1), pandas 3.0.5, no DuckDB/PostgreSQL/MySQL.

## Counts
- Answers checked: 57 of 57 (Q1-Q57, headings/numbers/stars/order untouched).
- Executed OK (SQL output and pandas match the printed tables): 48 by direct SQLite run. 9 are non-SQLite SQL (Q44, Q45, Q48, Q49 main query, Q53 PERCENTILE_CONT, Q57, plus Q50 strict-engine error, Q15/Q41 vendor claims): values verified by SQLite UNION ALL / plain GROUP BY emulation or by the pandas snippet that was run; labelled "not run here".
- Answers with fixes: 14 (about 20 edits).

## Fixes
| Q | Wrong | Fix |
|---|---|---|
| 28 | Sample table had no `email` column, so the SQL could not run | Added email column and values; SQL and pandas now run and match |
| 34 | Sample table not named | Added "Table `employees`" line; re-ran, output matches |
| 42 | `VALUES ... AS t(cols)` is not valid SQLite; no pandas | Rewrote as `WITH emp(cols) AS (VALUES ...)`; ran in SQLite (4,4,3,2); added pandas |
| 43 | GREATEST and `t(x)` aliases not runnable, output credited to DuckDB (not installed) | Rewrote with SQLite scalar MAX; ran (Banana, 9, apple); GREATEST noted as not run; added pandas |
| 10 | "DuckDB says (run here)" was false | Relabelled as from memory, not run here |
| 50 | Error text attributed to a run of DuckDB | Relabelled as quoted from memory; SQLite outputs were verified |
| 19 | Garbled sentence about SQLite; all-NULL case unclear | Rewrote both |
| 44, 45, 57 | Output marked as if run; SQLite has no CUBE/ROLLUP/GROUPING | Added "not run here" note; rows rechecked via UNION ALL emulation (all match) |
| 48 | STDDEV SQL not run, not labelled | Added label; numbers match the pandas run |
| 49 | DuckDB/PostgreSQL output not labelled | Labelled not run; SQLite and pandas runs match |
| 53 | PERCENTILE_CONT output not labelled | Labelled not run; portable method and pandas run and match |
| 46 | Said HAVING without GROUP BY works in SQLite (older SQLite errors) | Added version note (3.39+, from memory) |
| 15, 41 | Oracle alias claims unqualified | Marked from memory / not run here |
| 41 | Missing pandas equivalent | Added |

## Unresolved / notes
- Missing pandas equivalent (conceptual answers, left as is): Q10, Q15, Q44 (Q44 values were checked only through SQL emulation).
- Q14 aggregate-in-WHERE error runs in SQLite: "misuse of aggregate function AVG()" confirmed.
- Q51 EXPLAIN QUERY PLAN lines confirmed exactly in SQLite 3.45.1 (SCAN vs SEARCH ... COVERING INDEX).
- Ordering: stars descending (3-star Q1-14, 2-star Q15-40, 1-star Q41-57); colours not strictly green-to-red inside the 2-star block (Q15-24 green, Q25-38 amber, Q39-40 red) and 1-star block; numbering continuous. No change made.
- Template: later answers (Q19 onward) use "Q: ... A: ..." inline follow-ups and some have no "Say this" in a list form; content present. Q39, Q40, Q41+ use blank-line layout. Not reformatted.
- Duplicates/overlap (report only): Q19/Q20/Q21 overlap Q1 and Q9 on NULL handling; Q28 overlaps Q7 (duplicate emails); Q42 notes COUNT(1) also touched in Q5; Q47 overlaps Q25 (conditional counts); Q57 overlaps Q44 (GROUPING).

## Claims labelled unverified (from memory / not run here)
Vendor alias rules (Q15, Q41, Q30), MySQL 8 no implicit sort and PostgreSQL hash grouping (Q16), DATE_TRUNC/DATETRUNC/week behaviour (Q49), STDDEV naming per vendor (Q48), CUBE/ROLLUP/GROUPING SETS support lists and versions (Q44, Q45, Q57), FILTER version numbers (Q47), ONLY_FULL_GROUP_BY default (Q10, Q50), SQLite 3.39 HAVING note (Q46), PERCENTILE_CONT availability (Q53), error texts of other engines (Q10, Q50).
- "Asked at" lines: consistent with research/Book02_Part02_sources.md (the Meesho item in Q53 is flagged anecdotal there and in the answer).
