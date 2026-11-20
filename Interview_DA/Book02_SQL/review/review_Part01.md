# Review: Book02_Part01.md (Wave C)

Reviewer: Wave C, Part 01. Environment: Python sqlite3 (SQLite 3.45.1), pandas 3.0.5, no duckdb.

## Counts
- Answers checked: 61 (Q1-Q61). Numbering continuous, stars descending, 🟢→🟡→🔴 within each star: correct, no change needed.
- Executed OK: 61. Every runnable SQL was rebuilt from the markdown sample tables and compared to the printed Output (all match, numeric values compared exactly). Every pandas snippet ran and matched its SQL result (Q33 and Q55 differ by design: Q33 shows the explicit-sort fix, Q55 is random).
- Answers edited: 19 (list below). No SQL, output or pandas was wrong; fixes are factual claims, markdown validity, cross-references and one example.

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| 14 | Said MySQL allows alias in WHERE (it does not; from memory); "Asked at" claimed analytics firms without support | Corrected, SQLite part marked checked, others "from memory"; Asked at reworded to the Cognizant source |
| 16 | MySQL LIMIT-expression claim unqualified | Marked from memory / not run |
| 25, 27, 35 | Tables nested inside bullets (`- \| ... \|`) do not render | Moved to standalone tables with a lead-in line |
| 25, 27 | Cross-reference Q41 for BETWEEN/time-of-day | Changed to Q42 (the actual question) |
| 26 | Output printed 80000.00 / 65000.00; real SQLite output is 80000.0 / 65000.0 | Output corrected |
| 42 | "checked in DuckDB" not reproducible here (no duckdb) | Reworded: worked out from the rule, not run |
| 47 | Example said only Rahul and Kavya match both tests; Manoj does too (output table already showed it) | Example corrected |
| 49 | "Oracle needs FROM DUAL" is not true for Oracle 23ai | Qualified (older Oracle; 23ai from memory) |
| 52 | "DuckDB accepted it" unverifiable; vague window-function sentence | Replaced with the SQLite behaviour I ran; sentence removed |
| 55 | TABLESAMPLE SYSTEM (1) shown as SQL Server syntax; "sorts them all" overstated | SQL Server form `TABLESAMPLE (1 PERCENT)`; wording softened |
| 56 | DISTINCT-list and SUM queries shown only as tables, no SQL | Added both queries (commented, run in SQLite: list fine, SUM = 200000 vs 150000) |
| 58 | Backslash-default claim unqualified | Marked from memory |
| 59 | PostgreSQL 13+ `FETCH FIRST n PERCENT` claim is wrong (PERCENT not in PostgreSQL); DuckDB claim unverifiable | PERCENT limited to Oracle 12c+ / SQL Server TOP PERCENT (from memory); DuckDB removed |
| 42-48, 51, 54, 55, 57 (11 answers) | "Asked at: service MNC / analytics firm (general SQL-basics screens)" not supported by the sources file | Changed to "commonly asked (no company-specific report found)" |

## Template completeness
All 61 answers have Asked at, interviewer check, Say this, Explain simply, Example, Likely follow-ups, Common mistakes. Query answers have sample data, SQL, output, pandas, edge cases. Concept answers (Q1, Q9, Q13, Q14, Q49, Q50) use a small runnable demo instead, as allowed. Q1/Q9/Q13/Q14 reuse the Employees table from Q2 without repeating it.

## Unresolved / notes
- Q61 asks for "LIKE or regular expression" but the run query uses SUBSTR/IN (portable); regex and SQL Server LIKE forms are described, not run (SQLite has no built-in REGEXP). Acceptable, flagged.
- Q55 output is one random run, not reproducible by design. Q33 output depends on the SQLite query plan (re-run and confirmed identical here).
- Q22-Q61 use a second Employees dataset (6 columns, names Asha/Ravi...) while Q2-Q21 use the 7-column one; consistent inside each answer, noted for the book editor.
- Overlap with other parts (report only): COUNT/DISTINCT (Q43/Q44/Q56) and WHERE vs HAVING (Q26) overlap Part 2 by design; Nth highest overlaps later DENSE_RANK parts.

## Claims labelled unverified (from memory / not run here)
Non-SQLite dialect syntax (TOP, FETCH FIRST, TABLESAMPLE, IS DISTINCT FROM, <=>, ISNULL-style variants), MySQL LIMIT/alias/trailing-space/escape behaviour, Oracle 23ai FROM-less SELECT, PostgreSQL 13 WITH TIES, ORA-01791 and PostgreSQL error text, collation defaults per database, index-use remarks. Source tallies unchanged.
