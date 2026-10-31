# Book 3 Part 11 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 35 questions, Q1-Q35. Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
- The first four answer agents were stopped by a spend limit; their partial scratch work was pushed and a fresh set of four agents rewrote Q1-9, Q10-18, Q19-27 and Q28-35 from the frozen questions.
- Merged by heading: 35 of 35 merged, 0 skipped, 0 pending.

## Structure checks (scratch/review_scripts/check_book3.py)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q35 | pass |
| Star order and counts 14 / 15 / 6 | pass |
| Template labels in every answer | pass after one fix (Q14 output label reworded to the standard label) |
| One runnable Code program per question, `python3 -I` | pass, no failures |

## Code
SQLite 3.45.1, pandas 3.0.5, seeded data, no duckdb, no numexpr, no pyarrow. Cost proxy is VM steps via set_progress_handler; plans, page counts and step counts are deterministic. Wall-clock timings (Q2, Q14, Q23, Q29, Q30) are labelled machine-specific and vary per run.

## Findings kept in the text (premises corrected)
- Stale EXPLAIN text: same connection can print an old plan after DROP INDEX or ANALYZE; a fresh connection prints the right plan (Q10-18, Q34).
- Mismatched literal types did not break an index in the cases run (Q7); SQLite did not unify IN and EXISTS (Q8); NOT IN with NULLs returns 0 rows and the IS NOT NULL fix loses the fast path (Q9).
- `!=` never used an index (Q10, Q21); skip-scan appears only after ANALYZE (Q4, Q10).
- Index choice on averages can lose: INDEXED BY ix_type was 16x cheaper than the planner's pick (Q17); skew is invisible to sqlite_stat1 (Q18).
- VM steps do not capture I/O: covering index (Q13), partial-index write saving (Q22), index-after-load (Q23), N+1 (Q24) are argued with page counts or wall time instead.
- Fan-out inflated revenue about 4x (Q19); the unindexed correlated Q20 form is a labelled extrapolation from 500-2,000 rows.
- Q29 did not reproduce a large slowdown in SQLite; the answer says so. WITHOUT ROWID was larger with a 300-byte payload (Q31). Q34 corrects the Wave A premise (stale plan only after DROP INDEX).
- pandas: astype("int8") wraps 300 to 44 silently; category of unique strings is larger than str; query/eval not faster at 500,000 rows without numexpr; observed=False faster than True left unexplained.

## Not verified (hedged "not executed" in the text)
PostgreSQL EXPLAIN (ANALYZE, BUFFERS), MySQL EXPLAIN and hints, SQL Server plans, parameter sniffing, plan guides, partitioning and pruning rules, BigQuery clustering, Snowflake micro-partitions, Redshift keys, materialised views, MVCC and isolation anomalies, PostgreSQL 12 CTE inlining, bulk-load tools, ORM loading; a few SQLite points marked "from memory" (stat4 build option, row values since 3.15, ASCII-only NOCASE fold, automatic-index lifetime). No vendor benchmark numbers quoted.

## Evidence limits
No candidate-reported questions found; sources are SQLite, PostgreSQL, MySQL and pandas documentation plus editorial guides (see research_notes/Book3_Part11_sources.md). Unexplained results (observed=False speed, analysis_limit stat strings, stale plan cause) are stated as unexplained.
