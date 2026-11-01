# review_Book04.md — Book 4 (Power BI & Visualization) review summary (Wave C, plan.md Section 8.6)

Date: 2026-11-01. Answer chunks were merged into `Book04_PartNN.md`; one reviewer per part re-ran every pandas snippet (pandas 3.0.5), re-derived DAX results by hand, fixed errors in place and wrote `review/review_PartNN.md` (per-fix detail there). Reviewer counts are the reviewers' own and some are approximate.

## Pass criteria (plan.md 8.6)
| Check | Result |
|---|---|
| Completeness | 624 of 624 answered; 0 `ANSWER_PENDING` (script check) |
| Count | 624 vs target 600 (met) |
| Ordering / numbering | Continuous Q1..Qn in all 12 parts (script check) |
| Template fields | All 9 common fields present in all 624 (script check) |
| Markdown | Code fences balanced in all parts; blank line after tables |
| Accuracy | Pandas snippets re-run; printed outputs and Results now match; DAX results re-derived by hand |

## Per part
| Part | Answers | Answers fixed | Main fix types |
|---|---|---|---|
| 1 | 55 | 26 | undefined variables in snippets, wrong printed output, contradictory unverified labels |
| 2 | 61 | 35 | Q22-61 snippets rebuilt as runnable with real output, wrong M/DAX table names, contradictory null-key claims |
| 3 | 60 | ~40 | snippets rebuilt, Q47 DAX disagreed with pandas, wrong M query name |
| 4 | 75 | 24 | 9 snippets not runnable, wrong UNION row count, measure/table name clashes |
| 5 | 35 | 15 | Q18 wrong total (1,720 to 2,020), Q14/Q20/Q25 measures corrected |
| 6 | 61 | 26 | undefined variables, missing DAX definitions, wrong claims on Legend and ALL |
| 7 | 65 | 10 | Q30 sample mismatch, Build vs edit permission wording on RLS, unsupported Wipro RLS claim removed |
| 8 | 47 | 19 | Q22 wrong biggest drop, Q40 wrong claim, measure/column name clashes |
| 9 | 70 | 26 | Q13 wrong weakest stage, column names mismatched to samples, curly quotes in DAX |
| 10 | 43 | 16 | Q43 LOD fix wrong, Q13/Q42 figures wrong, Tableau menu paths |
| 11 | 27 | 14 | undefined variables, wrong printed decimals, missing labels |
| 12 | 25 | 9 | Q10 arithmetic, Q12 snippet, unlabelled claims |

## Known limits (not fixed; honest status)
- **No DAX / Power Query / Power BI engine:** every DAX, M and click-path is labelled "not run here"; results are "reproduced with pandas" only. Reviewers flagged a few rewritten measures as reasoned but unexecuted (Part 5 Q14 and Q25 alternative, Part 3 Q47).
- **Microsoft Learn and Tableau Help were unreachable in the Wave B and Wave C sessions:** no page was fetched. All version, licensing, preview/GA, menu-name and function-behaviour facts are "from memory, unverified" or "per the Wave A sources file, not re-fetched". Open items: Desktop Windows-only, refresh limits (8/48 per day, 2h/5h), F64 free-viewer threshold, deployment-pipelines licence, Copilot capacity (F2+/P1+), Q&A retirement date conflict (Feb 2027 vs Dec 2026), DISTINCTCOUNT blank handling, many-to-many service support, Tableau order of operations (Part 10 Q10 vs Q16/Q35 differ on where sets sit).
- Part 8 sources file says a Microsoft design-tips page was "fetched in full"; answers say it was unreachable and stay labelled unverified. Reconcile the sources file.
- Part 12 header says target 20 questions vs 25 actual; sources file mentions a stale 27.
- Some tables and sample data are constructed, not sourced; example figures are illustrative.
- "Asked at" limited to what research files support; much of that research is search-snippet or candidate-reported.
- Topic overlaps across parts (Top N, date tables, RLS, optimisation, folder combine) were reported by reviewers, kept and cross-referenced.
- A human read-through by a non-technical reader is still advisable.
