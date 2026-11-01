# Book 3 Part 07 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (40 of 40 merged, 0 skipped, 0 pending; no spend-limit stops this part). Header status updated after the merge.

## Structure checks (scripted, scratch/review_scripts/check_book3.py)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40 | pass |
| Star order and counts 17 / 14 / 9 | pass (matches header) |
| All template labels in every answer | pass for all 40 |
| Exactly one sqlite3 Code program per question, run standalone with `python3 -I` | 40 of 40 exit 0 |

## Code
Each program builds the data in SQLite 3.45.1, runs the SQL (ROW_NUMBER/LAG/LEAD flags, running SUM and MAX frames, recursive CTE spines, self joins), runs pandas 3.0.5 and asserts SQL equals pandas, with fixed as-of dates and both session-timeout conventions shown where relevant. Part 7 stays on gaps and islands, streaks, sessions and intervals (ranking Part 4, running totals Part 5, retention Part 6, recursive CTEs Part 9 as a pointer).

## Items the Wave A note listed as unverified, now run (3.45.1 / 3.0.5)
MAX over ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING works (NULL on each partition's first row); recursive-CTE date spines run (39,979-day spine tested); julianday differences are exact for whole dates but never exact for timestamps (0 of 20,000 exact 30-minute pairs equal 30 under julianday*1440; unixepoch matched all 20,000); truncating julianday*1440 differed from the rounded value on 70,272 of 527,040 minute stamps; julianday(date)-row_number key equals the unixepoch/86400 key on whole dates; pandas: NaN != NaN is True, shift upcasts int to float64 (fill_value keeps int), groupby drops NaN keys unless dropna=False, rolling(3).min() is NaN for the first rows and min_periods=1 gives false runs, rolling on a bool Series returns float64, cummax inside groupby keeps datetime64 and NaT, single-key sort_values default kind is not equal to kind='stable' on tied rows (2,000 and 20,000 row tests) while multi-key sorts are, itertools.groupby run lengths match SQL and depend on object identity for NaN; FILTER works in SQLite 3.45; LAST_VALUE IGNORE NULLS is a syntax error; a window function inside another window's PARTITION BY raises "misuse of window function".

## Findings kept in the text
Duplicate rows hide real one-day gaps and invent streaks; streak keys must include user_id (cross-user collisions); streak, session and run keys need dedup and a tie-breaker; session ids stayed identical under tied timestamps while event order and the flagged row changed; concurrency peak depends on tie order (3 vs 5), default RANGE frame nets ties; ROWS frame with ties wrong; "in a row" differs for id arithmetic vs positional LEAD when ids have gaps; joins instead of IN double-count users with two qualifying streaks; filtering after ROW_NUMBER admits short runs; consecutive NULL statuses are one run with IS NOT and none with <>; SQLite bare-column MAX returns the older streak on ties like pandas idxmax; IST vs UTC day boundaries flip streaks on a one-second difference; the row-number-over-all-then-filter variant is wrong with a date key; scalar MIN/MAX with a NULL argument gives NULL; naive pandas ne(shift) makes NaN rows their own runs; the survival-style and reset-by-threshold variants are state-dependent (Part 9 pointer).

## Not verified (hedged "not executed" in the text)
PostgreSQL, MySQL, BigQuery, Snowflake and Oracle date arithmetic, generate_series, GENERATE_DATE_ARRAY, DISTINCT ON, QUALIFY, IS DISTINCT FROM vs <=>, IGNORE NULLS, TIMESTAMPDIFF truncation, EXTRACT(EPOCH), range types and exclusion constraints, parameter styles, MySQL 5.7 lacking window functions, DST and time-zone behaviour (pandas-only demo in Q39), SQLite storing julianday as integer milliseconds ("probably"); LeetCode 180, 601, 603, 1285, 1454, 2173 statements (603 and 1454 premium, pages not opened); the Dataiku >= timeout convention (sources note only).

## Evidence limits
No candidate-reported questions were found; evidence is prep guides, public problem banks, a Dataiku sessionization tutorial and an interval-merge write-up (leetcode.com returned 403 and the SQLite window page 503 in Wave A). No source states a salary band. Stars and "Asked at" tags are indicative.
