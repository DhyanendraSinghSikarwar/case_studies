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
| 1 | SELECT, filtering, aggregation, GROUP BY/HAVING | 45 | ✅ (45 Qs) | ⬜ | ⬜ |
| 2 | Joins (all types, self, anti/semi) | 45 | ⬜ | ⬜ | ⬜ |
| 3 | Subqueries, CTEs | 40 | ⬜ | ⬜ | ⬜ |
| 4 | Window functions: ranking, top-N per group | 50 | ⬜ | ⬜ | ⬜ |
| 5 | Window functions: running totals, LAG/LEAD, moving avg | 45 | ⬜ | ⬜ | ⬜ |
| 6 | Date/time: retention, cohorts, MoM/YoY | 45 | ⬜ | ⬜ | ⬜ |
| 7 | Gaps and islands, streaks, sessionization | 40 | ⬜ | ⬜ | ⬜ |
| 8 | Funnels, conversion, DAU/MAU, product metrics | 45 | ⬜ | ⬜ | ⬜ |
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
Part 1 Wave A (create `Book3_SQL/`, research SELECT/filtering/aggregation/GROUP BY/HAVING questions; see pipeline above).
