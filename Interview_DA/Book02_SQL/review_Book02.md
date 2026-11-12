# review_Book02.md — Book 2 (SQL) review summary (Wave C, plan.md Section 8.6)

Date: 2026-10-21. One reviewer per part re-executed each answer in SQLite 3.45.1 and pandas 3.0.5 (DuckDB not installed), fixed errors in place, and wrote `review/review_PartNN.md` (details per fix are there). Reviewer-reported counts are the reviewers' own and some are approximate.

## Pass criteria (plan.md 8.6)
| Check | Result |
|---|---|
| Completeness | 664 of 664 questions answered; 0 `ANSWER_PENDING` (script check) |
| Count | 664 vs target 600 (met) |
| Ordering / numbering | Continuous Q1..Qn in every part; stars descending then 🟢→🔴 (script check on headings; two reviewers noted some ⭐⭐/⭐ groups are not strictly 🟢→🔴: left as is) |
| Template fields | All 7 base fields present in all 664 (script check) |
| Duplicates | No identical question text across parts (script check). Reviewers listed intentional topical overlaps (e.g. strict funnels Part 9 Q10/Q33; day-N retention Q27/Q35; top-N Parts 5/10): kept, cross-referenced |
| Markdown | Code fences balanced; blank line after every table so following labels render (fixed in all parts) |
| Accuracy | Every runnable SQL block and pandas snippet was re-run by a reviewer; all printed outputs now match, after the fixes below |

## Per part
| Part | Answers | Reviewer: ran OK | Answers edited | Main fix types |
|---|---|---|---|---|
| 1 | 61 | 61 | 19 | wrong dialect claims (MySQL alias in WHERE, PostgreSQL FETCH PERCENT, SQL Server TABLESAMPLE), unsupported "Asked at" company claims, non-rendering tables |
| 2 | 57 | 48 + 6 labelled not-run | 14 | missing email column, DuckDB-only SQL rewritten for SQLite, false "run here" labels |
| 3 | 77 | all runnable | ~23 | missing INSERTs, missing pandas, wrong plan line order, false DuckDB claim, unsupported "Asked at" claims |
| 4 | 55 | 52 (+3 labelled not-run) | 22 | wrong example text, MySQL LIMIT-subquery claim, false DuckDB claims, 9 pandas added, missing sample tables |
| 5 | 71 | ~64 (+3 not runnable) | ~14 | 6-row sample vs 21-customer output, missing rows, wrong NULL-ordering claim, wrong version labels |
| 6 | 52 | 50 | ~30 (18 label-only) | wrong portable-median formula, SQL Server claims, pandas column mismatches |
| 7 | 60 | ~54 | 12 | wrong pandas date comparison (Q42), false DuckDB "run here" labels, unnamed sample tables |
| 8 | 74 | 73 (Q73 MEDIAN not runnable) | 18 | truncated sample tables rebuilt, weekend rows in a working-day table, undefined `today` |
| 9 | 46 | 46 | 5 | wording/claim fixes only |
| 10 | 43 | 43 | 7 | wrong row count in Q19, wrong plan in Q43, unrenderable table, invalid COUNT(DISTINCT (a,b)) |
| 11 | 44 | all runnable | 15 | missing sample data/setup, wrong error texts, Example added to Q42/Q43, pandas for Q41/Q43 |
| 12 | 24 | 24 | 13 | Example fields, wrong "7 of 8" figure, price/account claims aligned to sources; missing skill-development plan section added (roadmap, daily plan, resources, datasets, mini-projects, self-check tests) |

## Known limits (not fixed; honest status)
- **Non-SQLite dialect syntax and behaviour** (PostgreSQL, MySQL, SQL Server, Oracle, DuckDB, Snowflake, BigQuery): never executed here. All such statements are labelled "from memory / not run here" in the text; version numbers, error codes and defaults in those labels are unverified. A reviewer with those engines should spot-check.
- SQLite doc pages were unreachable (503); SQLite LIKE/optimiser statements rest on real `EXPLAIN QUERY PLAN` runs only.
- Some 20,000-row and 50,000-row generated tables (Part 3, 5, 10, 11 index/plan answers) are not printed in full; reviewers regenerated them and plans matched, but timings/row counts are illustrative, not benchmarks.
- Some sample tables were rebuilt or extended by reviewers (constructed, not sourced data).
- Pandas equivalents are absent from a minority of concept-only or non-runnable answers (listed in the part reports).
- Interview-frequency stars are editorial (see `research/Book02_PartNN_sources.md`); "Asked at" claims limited to what research files support; much of that research is search-snippet level and candidate-reported.
- Q-level overlaps and "Q: A:" follow-up layout inconsistency in Part 2 (Q19 onward) left as is.
- Beginner clarity: fully read by reviewers for the answers they edited; the rest scanned. A human read-through by a non-technical reader is still advisable.
