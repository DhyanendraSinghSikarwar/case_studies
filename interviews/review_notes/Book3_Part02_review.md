# Book 3 Part 02 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 45 questions, Q1-Q45. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (45 of 45 merged, 0 skipped, 0 pending). Header status updated after the merge.

## Structure checks (scripted, scratch/review_scripts/check_book3.py)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q45 | pass |
| Star order and counts 18 / 17 / 10 | pass (matches header) |
| Say this first, Schema and sample data, SQL answer, pandas answer, Example, Output (my run), Edge cases, Then explain, Follow-ups, Common mistakes in every answer | pass for all 45 |
| Exactly one sqlite3 Code program per question, run standalone with `python3 -I` | 45 of 45 exit 0 |

## Code
Each program builds the data in SQLite 3.45.1, runs the SQL, runs pandas 3.0.5 and asserts SQL equals pandas. Printed outputs were pasted from real runs by the agents' build scripts.

## Findings from running (kept in the text)
Fan-out totals (140 vs 70 true; SUM(DISTINCT) wrong the other way; 570 vs 350 in the revenue-doubling example); NATURAL JOIN coincidences (1 row, then 0, then cross join with no shared column); NOT IN NULL trap vs pandas ~isin; UNION collapsing a duplicate so LEFT JOIN UNION RIGHT JOIN gives 5 rows vs 6 for FULL JOIN; EXCEPT treating NULLs as equal while NOT EXISTS does not; BETWEEN with an open valid_to losing current rows and overlaps duplicating orders; merge_asof ignoring an upper bound and returning one row for duplicate quote timestamps; pandas merge matching NaN keys, isin matching NaN, groupby dropping NaN keys, all-NaN sums 0 without min_count=1; dtype mismatch errors (int64 vs str raises, int64 vs float64 merges, stray spaces silently fail); SQLite type affinity (TEXT joins INTEGER, 1 = '1' is 0, CAST of garbage gives 0); SQLite rejects INTERSECT ALL, MINUS, <=>, LATERAL and ASOF JOIN; DataFrame.compare showing NaN for unchanged cells.

## Not verified (hedged "not executed" in the text)
MySQL lacking FULL OUTER JOIN (supported by omission on the MySQL 8.4 page) and INTERSECT/EXCEPT since 8.0.31; SQLite adding RIGHT/FULL JOIN in 3.39 (only 3.45.1 run); Oracle MINUS and EXCEPT support; Snowflake MINUS; SQL Server lacking USING/NATURAL JOIN and using CROSS APPLY; LATERAL support per engine; native ASOF JOIN in DuckDB, Snowflake and ClickHouse; PostgreSQL integer = text errors vs MySQL silent conversion; cloud warehouses not enforcing primary keys; optimiser join-order and hash/merge-join behaviour; performance claims (nothing benchmarked); LeetCode section placement of employee-manager problems.

## Evidence limits
No candidate-reported join questions were found; evidence is prep guides, problem banks, the pandas merge docs and the SQLite and MySQL 8.4 pages listed in the sources note. No source states a salary band; salary values appear only as toy column data. Stars and "Asked at" tags are indicative.
