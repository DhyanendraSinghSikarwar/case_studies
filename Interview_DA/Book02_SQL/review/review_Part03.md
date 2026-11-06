# Review: Book 2 Part 03 (Joins) - Wave C

Environment: Python sqlite3 (SQLite 3.45.1), pandas 3.0.5, no duckdb. Scratch: scratchpad/C_Part03 (h.py runs SQL, pd1.py runs pandas).

## Counts
- Answers checked: 77 of 77 (headings, numbers, stars and order untouched).
- SQL executed in SQLite and output compared by script: all answers with runnable SQL matched (Q1-Q7, Q9-Q10, Q12-Q64, Q68-Q69, Q71-Q77). Checked by hand run: Q8, Q11 (3 test cases: 10/0, 10/5, 50/50), Q19, Q75 (query C), Q77 (ON version); plan lines of Q65, Q66, Q70 re-run on 3.45.1. Q67 not run here (LATERAL not in SQLite). Conceptual answers with no query (none besides plan demos) skipped.
- pandas snippets run (pandas 3.0.5) and compared with the printed output: every snippet matches (Q30 matches as the empty "no rows" result; Q52 matched when columns are typed as stated).
- Answers edited: 23 (details below). No wrong output tables found apart from the plan-line items below.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q2, Q6, Q7, Q8, Q11 | Missing "pandas equivalent" (template) | Added short snippets, each run and matched to the SQL result |
| Q8 | SQL created tables but never inserted rows, so the printed output could not come from the code | Added the INSERT statements (output now reproduced) |
| Q52 | Result depends on column types that were not stated | Added a note: employees.emp_no INTEGER, payroll.emp_no TEXT (verified: naive join returns 3 rows, cleaned join 4; with untyped columns the naive join returns 0) |
| Q61-Q64, Q67-Q69, Q71-Q77 | Table labels and tables with no blank line before them (43 places), which can fail to render in some Markdown engines | Inserted blank lines only (no content change) |
| Q65 | Said "SQLite 3.49" | Changed to 3.45.1 (plans re-run, unchanged) |
| Q66 | "After indexes" plan lines in wrong order | Re-ran on 3.45.1: SEARCH e first, then SEARCH d (also with 200 rows); lines swapped |
| Q70 | Third plan said COVERING INDEX; real plan is "SEARCH p USING INDEX ix_pay_lower (<expr>=?)" | Removed COVERING |
| Q67 | Claimed "run here in DuckDB 1.5" (DuckDB is not installed; claim unsupported). Also "SQL Server / Oracle equivalent" used TOP, which Oracle lacks | Relabelled "not run here" (result checked by hand and via pandas); split SQL Server TOP from Oracle FETCH FIRST |
| Q77 | Claimed DuckDB behaviour was checked; second query's output had no label | Now "only SQLite 3.45.1 run; others from memory"; added "Output (ON version)" label (output verified by run) |
| Q31 | "qualifying USING column not allowed in some PostgreSQL versions" (inaccurate) | Reworded: Oracle rejects it, PostgreSQL/MySQL accept (from memory) |
| Q75 | Vague "older MySQL brackets" claim | Replaced with neutral advice, labelled from memory |
| Q29 | Dialect claim unlabelled | Marked "from memory" for PostgreSQL/SQL Server |
| Q21, Q25, Q37, Q38, Q39 | "Asked at" added frequency claims not in sources | Removed unsupported parentheticals |
| Q24 | "Deloitte report ... and set operations" - sources only support inner vs outer | Removed "set operations" |

## Unresolved / notes
- Not run here (syntax checked by reading only): PostgreSQL, MySQL, SQL Server, Oracle, DuckDB specifics, e.g. IS NOT DISTINCT FROM, <=>, LATERAL/APPLY, generate_series, Hash/Merge join nodes. They are already labelled "not run here" in the text, or now are.
- Claims in Q77 about USING coalescing in PostgreSQL/DuckDB: from memory.
- Q65: "SQLite only does nested loops; MySQL 8 hash joins" etc.: from memory.
- Q1 pandas comment says emp, dept; other answers use table names directly. Fine, but variable names vary across the part.
- Asked-at lines other than "commonly asked" (Q22, Q23, Q24, Q27, Q34) match research/Book02_Part03_sources.md (single anonymous reports, search snippets only).

## Ordering, numbering, overlap (report only)
- Stars descending, then green/yellow/red: correct. Numbering Q1-Q77 continuous. Code fences balanced (even count).
- Overlap inside the part: Q3/Q4/Q6 and Q5/Q6 cover similar ground; Q38/Q39/Q12 (anti join) and Q16/Q49/Q61/Q74 (fan-out) deliberately repeat the topic with different angles. Q60 (recursive CTE) and Q69 (date spine, recursive CTE) likely overlap with the CTE part (Book02 Part with recursive queries) - dedupe pass should confirm.
