# Book 3 Part 09 review (Wave C)

Date: 2026-10-25. Reviewer: lead session (independent of the three answer agents). Scope: 30 questions, Q1-Q30. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (30 of 30 merged, 0 skipped, 0 pending; no spend-limit stops this part). Header status updated after the merge.

## Structure checks (scripted, scratch/review_scripts/check_book3.py)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q30 | pass |
| Star order and counts 12 / 11 / 7 | pass (matches header) |
| All template labels in every answer | pass for all 30 |
| Exactly one sqlite3 Code program per question, run standalone with `python3 -I` | 30 of 30 exit 0 |

## Code
Each program builds the data in SQLite 3.45.1, runs WITH RECURSIVE queries with cycle guards (every unguarded demo is bounded by LIMIT or a depth cap), runs pandas 3.0.5 (and networkx 3.6.1 or plain Python where relevant) and asserts SQL equals pandas. Timings in Q29 are machine-specific and printed from the run.

## Items the Wave A note listed as unverified, now run
SQLite 3.45.1: CYCLE and SEARCH are syntax errors; generate_series is "no such table"; a second reference to the recursive table gives "multiple references to recursive table" (also in a subquery), an aggregate gives "recursive aggregate queries not supported", a window gives "cannot use window functions in recursive queries", placing the recursive select first gives "circular reference"; WITH without RECURSIVE is accepted; a count to 1,000,000 ran with no default depth limit; integer overflow becomes REAL (20! integer, 21! REAL, F(93) REAL and inexact, 9223372036854775807 + 1 is REAL); CAST in the anchor does not truncate; power, exp, ln, group_concat and printf work; networkx 3.6.1 is installed (scipy and duckdb are not): connected_components, topological_generations, shortest_path, dijkstra_path (ValueError on negative loop), bellman_ford_path (NetworkXUnbounded), lowest_common_ancestor (None across trees) were run.

## Findings kept in the text
The premise that a manager loop hangs a top-down query is only true if the root is in or below the loop (Q8); depth caps terminate cycles but duplicate rows; UNION dedupes on all columns so a distance column defeats cycle protection (Q27); UNION collapses legitimate equal rows (36 vs 72); a leg cap alone returns 9 routes instead of 7; NOT IN with a NULL parent returns nothing; duplicate edges inflate mutual counts without COUNT(DISTINCT); the Q22 "tasks missing" cycle check fails when the loop is reachable from a stage-0 task; closed-form EWMA breaks from row 1978 of 2400; floored declining balance needs no recursion; ROUND(703.125,2) is 703.13 in SQLite and 703.12 in pandas; loan schedules differ by 1 paisa between unrounded and closed forms; ON DELETE CASCADE needs PRAGMA foreign_keys=ON; LIKE 'prefix%' ignores a plain index on SQLite; a 17,232-person subtree took 0.012 s with the automatic index, 0.007 s with an explicit index and 19.968 s with automatic indexing off and no index (machine-specific); a 20-level lattice produced 2,097,151 rows with UNION ALL vs 41 nodes with UNION; pandas groupby drops NaN keys and merge matches NaN keys.

## Not verified (hedged "not executed" in the text)
SQL Server (MAXRECURSION default 100, error 530, 0 unlimited, no RECURSIVE keyword, UNION ALL only, hint placement), MySQL (cte_max_recursion_depth 1000, max_execution_time, CONCAT, CAST in the anchor, error 1093), PostgreSQL (CYCLE and SEARCH from 14 per a snippet, generate_series, bigint vs numeric, statement_timeout), Oracle (CONNECT BY, NOCYCLE, CONNECT_BY_ISCYCLE, SYS_CONNECT_BY_PATH, ORA-01436, ORDER SIBLINGS BY) and Snowflake limits from snippets; nested-set and closure-table cost figures (blog rules of thumb); NetworkXNoPath on unreachable targets (documented, not run); LeetCode 1270 (from the doocs mirror: two self-joins for the head, at most 3 levels).

## Evidence limits
No candidate-reported questions were found; the Q18 and Q19 amortisation and depreciation prompts are expert additions. Six pages were opened (SQLite WITH, PostgreSQL WITH, MySQL 8.4 WITH, a manager-chain post, a hierarchy page, a LeetCode mirror). No source states a salary band. Stars and "Asked at" tags are indicative.
