# Review Part 09 (Book 9 Part 9: GenAI for analysts), Wave C

File: Book09_ML_AI_Tools/Book09_Part09.md (edited in place; headings, numbers, stars, order untouched).

## Counts
- Answers checked: 100 of 100 (all six template lines present in every answer: Asked at, checking, Say this, Explain simply, follow-ups, mistakes).
- Code blocks run: 28 Python/SQL answer blocks (about 24 answers with runnable code), plus the new Q31 block; all executed on Python 3.13, pandas 3.0.5, numpy 2.5.3, statsmodels 0.15.0, SQLite 3.53.1. Prompts/templates/notes shown as text were read, not run (no LLM calls made).
- Answers with a defect or changed: 12 (1 wrong number, 1 missing script, 10 clarity/honesty/hidden-data edits).
- Code fences balanced (144 markers after edits); no em dashes in answer text (only the part-title line); table followed by blank line.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q62 | Answer B said 6.2% for 12/190; correct is 6.32% (Q90 agrees) | Changed to "6.3% (12 / 190 = 6.32%)" |
| Q31 | Output from a hidden script (seed 42) with no code shown | Added the toy-softmax script (scores 2.0/1.0/0.2); re-ran, output reproduces exactly; states seed dependence and toy status |
| Q73 | Probabilities quoted without the scores used | Stated scores 2.0, 1.0, 0.5 (recomputed: 63/23/14 and 48/29/23, 99% at 0.2) |
| Q49 | "7 invented employees" not given | Listed the 7 rows; re-ran the SQL on them: output identical to the pasted one |
| Q14 | Code had no comments, packed imports | Added comments, split imports; output unchanged (7 vs true 5) |
| Q20 | Dialect claim in "Say this" unlabelled | Labelled "from memory, unverified" for PostgreSQL/MySQL; SQLite behaviour confirmed by run |
| Q54, Q59, Q64, Q68, Q58 | Code used `connection`, `sales`, `products`, `sample` with no stated source | Added one-line comments saying which invented table/DB is assumed; rebuilt matching data and re-ran |
| Q100 | Infosys GenAI report stated without caveat | Added "single anecdote; role not confirmed as data analyst" (matches research/interview_processes.md line 41) |

## Verified by recomputation (no change needed)
Q14 (7 vs 5 rows), Q20 (HR 50000 bare-column row; fixed 50000/30000/60000), Q25 (changes 15/-7/22; 12.5/-5.2/17.2%; total 533), Q26 (bands, years), Q27 (300/320/80; 700), Q30 (75,000 tokens, ~2,100 rows), Q36 (3/3/3), Q37 (3 pp; 40/150=27%), Q42 (0.4 vs 0.2, ratio 0.5), Q45 (mean 65,000, median 55,000), Q50 (350/400 vs 150/200/None; totals 750 and 350), Q51 (AI [4,6] vs fixed [2,6]; window version agrees), Q52 (error text "no such column"), Q53 (1000/1240/240; 100000 vs 124000), Q54 (empty EXCEPTs), Q57 (51/60=85%, Wilson 74-92%, crosstab sums to 60, diagonal 51), Q58 (6 to 5 rows; dayfirst=True turns 2024-03-01 into 3 Jan; "hr".title() = "Hr"), Q59 (SCAN then SEARCH USING INDEX), Q60 (0.90/0.92 = 0.978), Q64 (4 to 8 rows, 1,000,000), Q68 (1600/101400 vs 1800/101200; 200/1800 = 11%), Q80 (75%, Wilson 53-89%), Q82 (mean 4.2, median 3.0, premise flaw correctly flagged), Q83 (seed-42 table identical), Q84 (valid flags identical; \d unicode and $ newline claims true), Q85 (180/80/100/56%/160), Q90 (6.32/6.15/6.0), Q91 (A and C [2,3], B []), Q96 (120/100, 20.0%, 16.7%).

## Honesty review
- No answer claims an LLM, Copilot or cloud service was run; every prompt is labelled "text, not run". Tool, licensing, DPDP/GDPR, token-size and dialect facts are labelled "from memory, unverified" with a confirm-with-IT/legal line.
- "Asked at" entries all say "commonly asked (no company-specific report found)" or cite prep-site/PracHub items marked unverified; Q76 and Q100 figures match Book09_Part09_sources.md and interview_processes.md.
- Personal-experience answers (Q19) are explicitly templates ("replace with your own real story").

## Unresolved / report only
- Q49 SQL was tested only in SQLite (uses FILTER and a recursive date CTE); PostgreSQL version (generate_series) is from memory, unverified, as the answer says.
- Q53, Q54, Q57, Q58, Q59, Q64, Q68 still depend on rebuilt (not pasted) invented data; counts and shape match, but Q59's SUM (320.0) cannot be reproduced without the original rows (plan shape verified).
- Ordering: stars/difficulty order appears consistent (3-star block Q1-Q70, 2-star Q29-Q70 interleaved by difficulty, 1-star Q71-Q100); Q1-Q28 mix emoji 🟢/🟡/🔴 in order. No reorder needed.
- Overlap: Q8/Q9/Q22/Q26/Q40/Q93 (privacy) and Q4/Q78/Q99 (hallucination) overlap within the part; Q79/Q72/Q73 touch Part 10 (RAG, tokens, temperature) by design; Q14/Q50/Q53/Q96 overlap on join fan-out; Q80/Q57 on Wilson interval. Not changed.

## Left unverified (cannot be checked here)
Copilot/ChatGPT/Claude features, limits, licensing and data handling; DPDP Act and GDPR details; token-per-word rule of thumb; MySQL/PostgreSQL/SQL Server syntax claims; EXPLAIN ANALYZE in PostgreSQL; DAX behaviour (Q64, Q69 unrun); prompt-injection defence status.
