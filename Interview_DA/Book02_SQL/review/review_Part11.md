# Review: Book02_Part11.md (Wave C)

Counts: 44 answers checked. Every SQL block with a runnable SQLite query (Q1-7, 9-12, 14, 15, 17-19, 21, 23-28, 30-32, 34, 36, 39-43) was rebuilt and run in SQLite 3.45.1. All printed outputs and EXPLAIN plans matched. The rest are concept-only or non-SQLite (Q8, 13, 16, 20, 29, 33, 35, 37, 38, 44; see below). Fixed: 14 answers. Fence count even (100), tables render.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| 3 | `emp` table not defined; Asked at too vague (Wells Fargo report names TRUNCATE vs DELETE); identity-reset claim unqualified | Added setup line; cited Wells Fargo (search snippet, lower confidence); qualified reset claim per engine (from memory) |
| 6 | SQL `COUNT(*)` unaliased but output header `n` | Added `AS n` (re-run) |
| 7 | Error text `balance>=0` vs real `balance >= 0`; durability line said "1 row" | Corrected to actual text; durability line now Asha 700, Ravi 800 (reopened file DB, run) |
| 10 | Sample data absent ("5 sales" only), so Output not reproducible; Q22 reuses it | Added INSERTs for dims and 5 fact rows; re-ran, gives printed output for Q10 and Q22 |
| 14 | Error text `salary>0` vs real `salary > 0` | Corrected |
| 15 | `acct` table undefined | Added setup comment |
| 20 | MySQL `DELIMITER` on same line as CREATE (invalid in client) | Split onto own lines (not run here) |
| 21 | Used `employees`/`departments` without setup | Added setup comment |
| 25 | Table captions came after the tables (ambiguous) | Captions moved before tables |
| 30 | Edge-case sentence garbled ("Storing ...") | Reworded |
| 36 | Asked at said no report; Wells Fargo views vs temp tables report exists | Added (lower confidence) |
| 39 | "Hyderabad-style employees" meaningless | Reworded |
| 41 | No pandas equivalent | Added, run with pandas 3.0.5 (162000 / 112000 match SQL) |
| 42 | Missing Example; sample rows only described (Output not reproducible) | Added Example with numbers and the INSERTs (run; output matches) |
| 43 | Example field mislabelled "Example (sales)" and thin; no pandas | Replaced with full Example (sales and hiring funnel); added pandas (run, same 4 rows) |

## Unresolved / report only
- pandas equivalents exist only for Q41 and Q43. Other query answers (e.g. Q4, Q10, Q17, Q23, Q26, Q34) are schema/concept demos and still lack one; adding pandas to all was not done.
- Concept answers with no SQL run (by design): Q8, 13, 16, 29, 35, 44; Q20, 33, 37, 38 give non-SQLite SQL, labelled "not run here".
- Q27, Q39, Q40 sample data (20,000 rows) is not printed; I regenerated it with my own generator and got the same plans and counts (gender 10000, city C7 23). Plans may vary with data.
- Numbering/order: stars descending then green to red is correct, Q1-Q44 continuous. No change.
- Overlap: Q3, Q17 overlap Parts 1-2 (acknowledged in text); Q10/Q22/Q43 and Q5/Q27/Q39/Q40 overlap internally by design; no action.

## Claims labelled unverified (from memory, not run here)
Engine differences: MySQL DDL auto-commit; TRUNCATE/DROP rollback by engine; identity reset; SQL Server one NULL in UNIQUE; MySQL CHECK from 8.0.16; MySQL `/` gives 2.5; default isolation levels (MySQL Repeatable Read, SQL Server Read Committed); PostgreSQL 11 procedures; PostgreSQL 18 skip scan; clustered index behaviour by engine; procedure vs function rules. "Asked at" claims limited to research/Book02_Part11_sources.md and research/interview_processes.md (Wells Fargo, Amazon BIE, Flipkart, Wipro entries all search-snippet level).
