# BOOK3_EXECUTION_PLAN.md — How Book 3 (SQL + pandas, 12 parts) will be built

Follows plan.md §4 (answer template, Book 3 extras), §5 (Book 3 table), §11 (workflow) and style_guide.md. Book 1 (14/14) and Book 2 (12/12, 558 Qs) are complete. Band: Rs 30-80 LPA roles; no salary figures anywhere.

## Pipeline (same as Book 2)
1. **Wave A (one research agent per part):** research real SQL/pandas interview questions (guides, banks, LeetCode-style SQL lists, company-type write-ups), record opened vs snippet-only pages, freeze the question list in `Book3_SQL/Book3_SQL_PartNN.md` with ANSWER_PENDING, append `B3PNN-Qn` rows to question_index.md, write `research_notes/Book3_PartNN_sources.md`. Scripts: `scratch/B3PNN_wavea/build.py` (copy the Book 2 Part 12 build.py as a template: tuples (stars, emoji, text, asked-at), asserts stars sorted 3,2,1).
2. **Wave B (4 answer agents per part, each its own scratch file):** `scratch/B3PNN_Qxx-yy/answers.md`; lead merges by heading with `scratch/B3PNN_merge/merge.py` (copy of the Book 2 merge script with the file path changed).
3. **Wave C (lead):** run structure check, re-run every code block, spot-check, write `review_notes/Book3_PartNN_review.md`, update plan.md tracker and this checklist, fetch then plain push (never force).

## Book 3 answer template (extends style_guide.md)
Per question: `### Qn stars emoji text` / `**Asked at:**` / **Say this first (1 line):** / **Schema and sample data:** (SQL `CREATE TABLE` + `INSERT`, small enough to check by hand) / **SQL answer:** (standard SQL that RUNS on SQLite 3.45 via `sqlite3` in Python; note dialect differences for Postgres, MySQL, BigQuery, Snowflake as hedged text, never as claimed-run) / **pandas answer:** (runs on the installed pandas 3.0.x; the answer must assert the pandas result equals the SQL result, same rows, order stated) / **Output (my run):** (pasted from the real run) / **Edge cases:** (NULLs, ties, duplicates, empty groups, time zones) / **Then explain:** / **Follow-ups:** / **Common mistakes:**. A runnable Python block (using sqlite3 + pandas) holds both solutions with asserts so every printed result is real. Features SQLite lacks (e.g. FULL OUTER JOIN before 3.39 is fine here; PIVOT, DATE_TRUNC, QUALIFY, ARRAY functions, LATERAL, FILTER syntax variants) are shown as dialect text only or emulated, and labelled "not executed". Mandatory Example/edge-case content, honest weak results, no invented company claims.

## Part checklist (target Qs from plan.md)
| Part | Topic | Target | Wave A | Wave B | Wave C |
|---|---|---|---|---|---|
| 1 | SELECT, filtering, aggregation, GROUP BY/HAVING | 45 | ✅ (45 Qs) | ✅ | ✅ |
| 2 | Joins (all types, self, anti/semi) | 45 | ✅ (45 Qs) | ✅ | ✅ |
| 3 | Subqueries, CTEs | 40 | ✅ (40 Qs) | ✅ | ✅ |
| 4 | Window functions: ranking, top-N per group | 50 | ✅ (50 Qs) | ✅ | ✅ |
| 5 | Window functions: running totals, LAG/LEAD, moving avg | 45 | ✅ (46 Qs) | ✅ | ✅ |
| 6 | Date/time: retention, cohorts, MoM/YoY | 45 | ✅ (45 Qs) | ✅ | ✅ |
| 7 | Gaps and islands, streaks, sessionization | 40 | ✅ (40 Qs) | ✅ | ✅ |
| 8 | Funnels, conversion, DAU/MAU, product metrics | 45 | ✅ (45 Qs) | ✅ | ✅ |
| 9 | Recursive CTEs, hierarchies, graphs | 30 | ✅ (30 Qs) | ⬜ | ⬜ |
| 10 | Pivot/unpivot, string ops, NULL traps | 40 | ⬜ | ⬜ | ⬜ |
| 11 | Query optimisation, indexes, execution plans, partitioning | 35 | ⬜ | ⬜ | ⬜ |
| 12 | Company-style mixed mock sets (FAANG, fintech, e-com) | 40 | ⬜ | ⬜ | ⬜ |

## Scope boundaries
Book 1 owns statistics and ML; Book 4 owns data engineering and generic MLOps (feature stores, Kafka/Spark); Book 6 owns product/business scenarios (Book 3 Part 8 covers only the SQL of metrics, not metric design). Book 3 Part 11 stays on SQL engine behaviour (EXPLAIN on SQLite is executed; other engines are hedged). Keep parts non-overlapping: Part 4 = ranking/top-N windows, Part 5 = running aggregates and LAG/LEAD.

## Environment notes
- Python 3.13, sqlite3 (SQLite 3.45.1: window functions, CTEs, recursive CTEs, FILTER, RETURNING available), pandas 3.0.5, numpy; WebSearch and WebFetch work (some sites 403/429).
- No Postgres/MySQL/DuckDB server unless installed; check `python3 -c "import duckdb"` and say so in the note if used. Anything not executed must be labelled "not executed".
- Spend-limit interruptions: resume agents with SendMessage after the reset.

## Next step
Part 9 Wave A (recursive CTEs, hierarchies, graphs: WITH RECURSIVE syntax and termination, anchor vs recursive member, UNION vs UNION ALL, cycle detection and depth limits, employee-manager hierarchies (all reports under a manager, chain of command, levels/depth, path strings, org-size roll-ups), bill of materials/part explosion, category trees and breadcrumbs, generating number/date series (calendar spines; cross-reference Part 6), Fibonacci/factorial style toy recursion, graph reachability/connected components/shortest path on small graphs, friends-of-friends, cumulative sum reset by threshold (the state-dependent problem deferred from Part 7 Q24), running calculations that need recursion (compound interest, EWMA, depreciation), recursive CTE vs window function alternatives, performance and safety (max recursion limits per engine, infinite loops, LIMIT), adjacency list vs nested set vs materialized path vs closure table at concept level, hierarchical aggregation; SQLite supports WITH RECURSIVE so answers run; other engines' syntax (CONNECT BY in Oracle, CYCLE clause, SEARCH DEPTH/BREADTH FIRST in PostgreSQL 14+, SQL Server MAXRECURSION, MySQL cte_max_recursion_depth) hedged 'not executed'; pandas side: iterative merges/while loops, networkx not installed (check) so plain Python BFS/DFS, scipy.sparse.csgraph if installed else hand-written, groupby/transform for roll-ups, explode for paths). Then Wave B and review. Tools: copy scratch/B3P08_merge/merge.py (change part-file path and prefix); check with `python3 scratch/review_scripts/check_book3.py Book3_SQL/Book3_SQL_PartNN.md`; Wave B brief scratch/B3_brief.md plus Part notes as in earlier launch prompts (format model: Part 1-8 answers). Split Wave B into agents of about 8-10 questions and tell agents to stop and report (not retry) at a spend limit and to keep working files in their own scratch folders; if a limit stops work, wait for the user (user instruction: do not auto-continue after a limit; after a restart or an explicit 'continue', resume the stopped agents with SendMessage). Part 8 lessons: SQLite ROUND is half away from zero while Python, numpy and pandas differ (round half to even; numpy/pandas 2.675 gives 2.68, SQLite and Python 2.67); integer division truncates; rolling().nunique EXISTS in pandas 3.0.5 (Q42 premise was wrong; fixed) but only yields values at existing rows; BETWEEN on timestamp text with a bare date drops the last day; filtering a joined table in WHERE drops non-converters; the channel must be assigned by a first-touch rule or channel funnels exceed 100 percent; DAU new/returning/resurrected classes do not sum to DAU without a first_seen_late class; SELECT DISTINCT * misses retries with different timestamps and LAG 5-second dedup collapses chains; an inner join to events drops payers who were not active (GMV 1700 vs 1150); pandas pivot_table/crosstab/value_counts/groupby drop NaN keys by default and aggfunc defaults to mean; merge matches NaN to NaN; len(set(series)) counts each NaN separately; NTILE(2) is not a median; power/exp/ln exist in this SQLite build (math functions compile option) but hedge for others.
