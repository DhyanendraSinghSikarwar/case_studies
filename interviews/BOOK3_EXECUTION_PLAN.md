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
| 8 | Funnels, conversion, DAU/MAU, product metrics | 45 | ✅ (45 Qs) | ⬜ | ⬜ |
| 9 | Recursive CTEs, hierarchies, graphs | 30 | ⬜ | ⬜ | ⬜ |
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
Part 8 Wave A (funnels, conversion, DAU/MAU, product metrics in SQL: funnel step conversion with ordered events and time windows, drop-off rates, strict vs loose funnel ordering, first-time vs repeated events, conversion rate by cohort/channel/experiment arm, DAU/WAU/MAU and stickiness (DAU/MAU) with fixed as-of dates, new vs returning users, activation, ARPU/ARPPU/LTV basics, GMV/AOV, repeat rate, A/B test metric tables in SQL (counts, conversion by arm; the statistics of significance belong to Book 1/Book 6), attribution (first/last touch), top-N products/categories metrics, cancellation/refund rates, SQL for 'metrics definitions' interviews; Part 6 already covers retention and cohort tables, Part 7 sessionization, Part 5 running metrics: cross-reference, do not repeat; metric design/product sense belongs to Book 6; pandas: groupby/agg, pivot_table, crosstab, value_counts(normalize), merge for funnels, nunique, cumulative funnel with isin/groupby, etc.). Then Wave B and review. Tools: copy scratch/B3P07_merge/merge.py (change part-file path and prefix); check with `python3 scratch/review_scripts/check_book3.py Book3_SQL/Book3_SQL_PartNN.md`; Wave B brief scratch/B3_brief.md plus Part notes as in earlier launch prompts (format model: Part 1-7 answers). Split Wave B into agents of about 11 questions and tell agents to stop and report (not retry) at a spend limit and to keep working files in their own scratch folders; if a limit stops work, wait for the user (user instruction: do not auto-continue after a limit). Part 7 lessons: julianday*1440 or *24 differences are not exact (30-minute gaps never equal 30; use unixepoch integer arithmetic or ROUND); julianday(date)-row_number works only on whole dates (truncate timestamps with date() first); date-minus-row_number needs dedup per (user, date) and the key must be combined with user_id; both 30-minute conventions (> vs >=) must be shown; ties on timestamp need an event_id tie-breaker (event_id must not be the INTEGER PRIMARY KEY or it aliases rowid); MAX over ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING works for interval merging; concurrency sweeps need an explicit tie order (ends before starts under half-open intervals); scalar MIN/MAX with NULL returns NULL in SQLite; naive pandas ne(shift()) treats each NaN row as its own run while SQL IS NOT merges NULL runs; single-key sort_values default kind is not stable; shift upcasts int to float64 (fill_value keeps int); rolling(3).min() on a bool Series returns float64; itertools.groupby on NaN depends on object identity; premium LeetCode problems (603, 1454) were not opened.
