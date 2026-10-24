# Review: Book 2 Part 12 (How to Develop SQL Skills)

Reviewer: Wave C. Engine: SQLite 3.45.1, pandas 3.0.5. Scratch: `.../scratchpad/C_Part12` (r.py, o.py).

## Counts
- Answers checked: 24. Query answers executed: Q6, Q12, Q13, Q14, Q15, Q17, Q18, Q21, Q22 (T1-T8), Q24; all SQL outputs matched the printed Output. pandas snippets run: Q6, Q13, Q14 (match SQL), Q21 (matched after fix).
- Answers fixed: 13 (plus one appended section). rerun.json showed only harness limits for Part 12 (no tables parsed); not relied on.
- Sources check: all free/price claims in Q3, Q4, Q7, Q10, Q11, Q12, Q20 match research/Book02_Part12_sources.md, except the one HackerRank wording below. Market figures (186 JDs; SQL 54%, Excel 60%, etc.), "19 of 20" and "14 of 20" profile counts, PhonePe/Amazon/Meesho reports match market_skills_2026.md and interview_processes.md.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Part | Style guide Sec. 7 items roadmap, daily plan, mini-projects absent as sections; Q1, Q7, Q16, Q22 referred to a nonexistent "section A/B" | Appended "Skill-development plan" (A roadmap, B daily plan, C resources, D datasets, E mini-projects, F self-tests). Weeks 1-11 targets sum to 260 (run); quiz schedule matches Q22 |
| Q1 | Pointed to missing section A; Example skipped CASE WHEN/dates | Pointer fixed; Example now matches roadmap |
| Q2 | "7 of 8 on joins quiz" contradicted Quiz 3 (6 of 8) | Changed to 6 of 8 |
| Q3, Q10 | "HackerRank needs an account" overstated source ("sign-up offered") | Reworded |
| Q6 | departments table not shown (query needs it) | Added mapping 10 HR, 20 Sales, 30 IT |
| Q12, Q15, Q18, Q21, Q24 | Example field labelled "Example (run...)" so not recognised as Example | Relabelled "**Example:** (run ...)" |
| Q13 | leave_log table not shown | Added description and pointer to Q22 kit |
| Q15 | leave_log not shown | Pointer to Q22 kit added |
| Q17 | No Example | Added (SQLite to SQL Server translation, Isha 3255 days) |
| Q21 | No sample data for orders_raw; pandas printed revenue as float (1650.0) vs integer SQL output | Added 8-row sample table (verified: 8 rows, 7 distinct, 1 NULL); added astype(int) |
| Q22 | No Example | Added (7 of 8 with a ROW_NUMBER tie error on T6) |

## Unresolved / unverified
- Template: Q1-Q5, Q7-Q10 etc. have no Sample data/SQL (conceptual answers; fine). Q23 has no runnable query (skeleton only, by design).
- Not run here (labelled in text): PostgreSQL, MySQL, SQL Server syntax in Q4, Q17; git commands and sqlite3 `.import` in Q12, Q20.
- Unverified (labelled in text): LeetCode Top SQL 50 price (HTTP 403), SQLBolt/Mode/HackerRank/SQL Online price, DuckDB, Kaggle IBM HR licence, Chinook licence.
- Roadmap hours, problem targets and pass marks are study design targets, stated as such.
- Ordering: stars descending and green-yellow-red order correct within each star band; numbering Q1-Q24 continuous. No change made.
- Overlap (report only): Q14 and Q18 repeat RANK/DENSE_RANK ideas from Part 5; Q16 and Q17 overlap with dialect notes in other parts.
- Markdown: code fences balanced; tables well formed.
