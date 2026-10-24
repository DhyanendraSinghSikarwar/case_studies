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
Part 7 Wave A (gaps and islands, streaks, sessionization: consecutive-day login streaks via date minus ROW_NUMBER, islands of consecutive IDs/dates, gaps between ranges, longest streak per user, sessionization by inactivity timeout with LAG + running SUM of new-session flags, session duration and counts, consecutive same-status runs (run-length encoding), counting consecutive events (LeetCode 180 Consecutive Numbers, 601 Human Traffic of Stadium), overlapping/merging intervals, missing numbers/dates, state-change detection, 'at least N consecutive' filters, cumulative sum reset by condition; recursive-CTE variants as pointers to Part 9; pandas: shift/diff/cumsum grouping trick, groupby on (s != s.shift()).cumsum(), run-length with groupby().size(), merge intervals, rolling/consecutive checks, pd.Grouper not needed). Then Wave B and review. Tools: copy scratch/B3P06_merge/merge.py (change part-file path and prefix); check with `python3 scratch/review_scripts/check_book3.py Book3_SQL/Book3_SQL_PartNN.md`; Wave B brief scratch/B3_brief.md plus Part notes as in earlier launch prompts (format model: Part 1-6 answers). Split Wave B into agents of about 10-12 questions and tell agents to stop and report (not retry) at a spend limit; if a limit stops work, wait for the user (user instruction: do not auto-continue after a limit). Part 6 lessons: SQLite has no native date type (TEXT/INTEGER; use date(), strftime(), julianday(), unixepoch(), modifiers); strftime %W works but %U %V %G %g return NULL (emulate ISO year/week with date(d,'-3 days','weekday 4'), verified against isocalendar over 14,976 days); date('2024-02-30') rolls over to 2024-03-01 instead of NULL (pandas gives NaT); '+1 month' overflows (2024-01-31 gives 2024-03-02) where pandas DateOffset clips; datetime(int) without 'unixepoch' returns NULL; CAST truncates toward zero but Timedelta.dt.days floors; BETWEEN with a bare end date drops the last day's timestamps; the localtime modifier depends on the process time zone; resample('W-MON') is right-closed/right-labelled by default (use closed='left', label='left' for Monday weeks), 'M' is no longer supported ('ME'); dt.floor('MS') raises; groupby drops NaT keys by default; pandas DateOffset chaining drifts; tz_localize raises plain ValueError for ambiguous and nonexistent times; Period merged on datetime returns 0 rows silently; LAG(12) breaks with missing or duplicate months; cohort tables must mask not-yet-observed months; retention definitions (classic/cumulative/rolling) must be stated; pandas parses '2024-1-6' where SQLite strftime returns NULL. Always use fixed as-of dates.
