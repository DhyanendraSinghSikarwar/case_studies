# Book 3 Part 01 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 45 questions, Q1-Q45. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (45 of 45 merged, 0 skipped, 0 pending). Header status updated after the merge.

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q45 | pass |
| Star order and counts 18 / 17 / 10 | pass (matches header) |
| Schema and sample data, SQL answer, pandas answer, Example, Output (my run), Edge cases present in every answer | pass for all 45 |

## Code
45 Code-block programs (one per question; each creates the data in SQLite 3.45.1, runs the SQL, runs pandas 3.0.5 and asserts the two results are equal) extracted from the final file and run standalone with `python3 -I`: all exit 0. A further 12 python fences hold short prose snippets (not standalone, not run separately). Printed outputs were pasted from real runs by the agents' build scripts.

## Premises in the question text that the runs contradicted (answers say so)
Q2 an alias in WHERE is accepted by SQLite 3.45 (also GROUP BY and HAVING); Q3 and Q17 HAVING on a non-grouped column runs silently with wrong totals in SQLite; Q18 bare columns in a grouped query run silently in SQLite (with MAX the row of the maximum, with MAX plus MIN the MIN row); Q19 COUNT(DISTINCT a, b) errors in SQLite (use a SELECT DISTINCT subquery); Q12 an ORDER BY with ties and LIMIT returns an engine-chosen row. Strict engines (PostgreSQL, MySQL with ONLY_FULL_GROUP_BY) are described from memory and marked "not executed here".

## SQL vs pandas differences found by running (kept in the text)
NaN in != and ~isin keeps rows where SQL drops UNKNOWN; isin matches NaN; groupby sum of an all-NaN group is 0 (needs min_count=1) vs NULL; pandas division by zero gives inf vs SQLite NULL; SQLite ROUND(2.5)=3 vs pandas 2.0 (half to even) and ROUND(2.675,2) differences; pandas na_position default; pivot_table(margins=True) silently dropping a NaN-product group; chained assignment error in pandas 3; observed=True default for categoricals; float summation differences (1.2000000000000002 vs 1.2); SQLite TRIM and LOWER are ASCII/space-only here vs pandas strip.

## Not verified (hedged in the text)
NULL ordering in MySQL, SQL Server, Oracle (only PostgreSQL read in Wave A); alias and ordinal support in GROUP BY and HAVING per engine; ONLY_FULL_GROUP_BY defaults; FILTER support outside SQLite and PostgreSQL; native ROLLUP, CUBE, GROUPING SETS, median and percentile functions per engine; default collations; integer-division behaviour per engine; MySQL error 1093; SQLite pre-3.39 HAVING-without-GROUP-BY behaviour; the SQLite docs page for the bare-column MAX special case (verified by running only); deep-OFFSET cost and leading-wildcard index notes (not timed). LeetCode SQL 50 section counts are snippet-level.

## Evidence limits
No candidate-reported SQL questions were found; evidence is prep guides, public problem banks and the pandas and database docs listed in the sources note. No source states a salary band. Stars and "Asked at" tags are indicative.
