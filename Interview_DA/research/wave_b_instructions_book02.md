# Wave B instructions — Book 2 (SQL) answers

You are answering a frozen question range. Read `plan.md` (Sections 4, 5, 8.5), `style_guide.md`, then this file.

## Who you write for
A non-technical HR professional switching to data analytics. Plain words. Every technical term explained the first time you use it in an answer. Sound like a confident candidate speaking in an interview, not a textbook. Use HR examples (employees, departments, salaries, attendance, attrition, hiring) where natural, otherwise sales/orders.

## What you produce
- Read your assigned question range from `Book02_SQL/Book02_PartNN.md` (read-only: do NOT edit that file).
- Write ONE chunk file: `Book02_SQL/answers_chunks/B02P<NN>_Q<from>-<to>.md` (create folder if missing). It contains, for each question in your range IN ORDER, the exact heading line copied unchanged from the part file (`### Q<n> ⭐⭐⭐ 🟢 <question>`) followed by the full answer. Never renumber, reorder, drop or rewrite questions. No other text in the file besides the answers (no preamble).
- Do not touch any other file. Scratchpad is shared with other agents: use a private subfolder for temp files.

## Answer template (every question)
```
### Q<n> ⭐⭐⭐ 🟢 <question — copied exactly>
**Asked at:** <company types, e.g. service MNC / GCC / analytics firm / product / startup — only claim what research supports; otherwise write "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1–2 plain-spoken lines the candidate can say out loud>
**Explain simply:**
- 2–5 bullets, jargon explained
**Example:** <real-life/HR-friendly example with numbers>
**Sample data:** <small table(s) in Markdown, 4–8 rows — only for query questions; concept questions may use a tiny example instead>
**SQL:**
```sql
-- query (standard SQL; say which dialect if it differs)
```
**Output:** <the REAL output table from running it>
**pandas equivalent:**
```python
# code
```
**Edge cases:** NULLs, duplicates, ties, empty results — whatever matters for this question
**Likely follow-ups:** 1–3 with short answers
**Common mistakes:** <what beginners get wrong>
```
- Pure concept questions (no query to write): omit Sample data / Output / pandas, but include a small runnable SQL demonstration when it helps. Keep the other fields.
- Dialect differences (MySQL vs PostgreSQL vs SQL Server vs SQLite) must be stated where syntax differs (LIMIT vs TOP vs FETCH FIRST, DATEDIFF, string concat, etc.).
- Length: about 200–450 words per answer; shorter for easy concept questions. Be concise: tables and bullets, no filler.

## Verification (mandatory)
- Run EVERY SQL query you write on the sample data using Python's `sqlite3` (SQLite 3.49: supports window functions, CTEs, recursive CTEs, FILTER) or DuckDB (`import duckdb`, v1.5). Run python with `python -I script.py` from your private scratch subfolder. For non-SQLite dialect-only syntax (TOP, DATEDIFF, STRING_AGG variants, etc.) show it as a labelled alternative and say "not run here"; the main query must be the one you ran.
- Run every pandas snippet (pandas 2.3.3) and paste the real output; make the pandas result match the SQL result.
- The Output table in your answer must be the actual result of running the code, not hand-written. Prefer building each answer from a script that executes the query and prints the table so the pasted output is exact.
- If a question's premise is wrong or ambiguous, say so in the answer and answer the sensible version.
- Never invent company-specific claims, statistics or sources. Do not cite sources you did not read.

## Reporting
Final reply: chunk file path, number of answers written, any questions where you changed the premise, and anything you could not verify. Keep it short.

## Addendum (lessons from batch 1)
- Scratch folder: create a folder named after YOUR chunk id (e.g. `scratchpad\B02P05_Q1-18`) and use only that. Other agents run at the same time; never write to or run files in a folder you did not create.
- Run scripts with plain `python script.py` (NOT `python -I`: it hides the installed pandas/duckdb). pandas and duckdb are already installed; do NOT `pip install` anything.
- "Asked at": write "commonly asked (no company-specific report found)" unless `research/Book02_PartNN_sources.md` or `research/interview_processes.md` supports a specific claim; then cite only that.
- Dialect/version facts you did not run or read in documentation: label "not run here / from memory" so the review wave can verify them.
- Put CREATE TABLE / CREATE INDEX statements inside the SQL code block, not in a label above it.
