# Book 3 Part 03 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (40 of 40 merged, 0 skipped, 0 pending). Header status updated after the merge.

## Structure checks (scripted, scratch/review_scripts/check_book3.py)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40 | pass |
| Star order and counts 16 / 14 / 10 | pass (matches header) |
| All ten template labels in every answer | pass for all 40 |
| Exactly one sqlite3 Code program per question, run standalone with `python3 -I` | 40 of 40 exit 0 |

## Code
Each program builds the data in SQLite 3.45.1, runs the SQL, runs pandas 3.0.5 and asserts SQL equals pandas. Outputs pasted from real runs. Part 3 stays within subqueries and CTEs (no window functions or recursion; pointers to Parts 4, 5, 9 and 11).

## Items the Wave A note listed as unverified, now run (3.45.1 / 3.0.5)
Alias on a FROM-subquery not required; LIMIT/OFFSET accept expressions and subqueries, LIMIT -1 works, OFFSET without LIMIT is a syntax error, OFFSET -1 acts as 0, LIMIT NULL is a datatype mismatch; UPDATE ... FROM, WITH before UPDATE/DELETE/INSERT and INSERT ... WITH ... SELECT run; row-value comparisons work ((1,NULL)=(1,2) is NULL); a many-row scalar subquery silently returns the first row, a two-column one errors; ANY/SOME/ALL are syntax errors; MATERIALIZED and NOT MATERIALIZED parse but are not binding; pandas isin matches NaN, transform gives NaN for NaN keys (own group with dropna=False), all-NaN sums are 0.0 unless min_count=1, copy-on-write and ChainedAssignmentError behave as documented in pandas 3.

## Findings kept in the text
NOT IN NULL traps against NOT EXISTS and ~isin; > MAX differs from > ALL on NULL and empty sets; GROUP BY treating NULL email as one group in a delete-duplicates NOT IN; nth-highest LIMIT/OFFSET vs correlated form disagree at N=0; orphan product ids cause false positives in relational division; empty category makes HAVING and double NOT EXISTS disagree; tie-break needed for top-N and latest-order queries (mask, drop_duplicates and idxmax return different rows); integer division percent-of-total sums to 98; correlated subquery cost is index-dependent (1.45M VM steps without an index vs about 20K for IN/join, about 8K with an index); view vs temp table visibility across connections; pandas transform 'mean' much faster than a lambda (machine-specific timings).

## Not verified (hedged "not executed" in the text)
MySQL error numbers 1093 and 1242 (1235 is from the opened MySQL page); PostgreSQL 12 CTE inlining version; PostgreSQL and MySQL requiring derived-table aliases and erroring on many-row scalar subqueries; ANY/ALL support elsewhere; ONLY_FULL_GROUP_BY behaviour; LATERAL/APPLY and row-value support by engine; PERCENTILE_CONT availability; date-formatting function names per engine; optimiser decorrelation and CTE materialisation defaults outside SQLite; materialized views; INSERT IGNORE vs ON CONFLICT DO NOTHING by engine. Not run: isin on nullable Int64, NULL salaries in Q27, division by zero in Q30.

## Evidence limits
No candidate-reported subquery or CTE questions were found; evidence is prep guides, public problem banks and the SQLite, PostgreSQL, MySQL 8.4 and pandas docs listed in the sources note. No source states a salary band. Stars and "Asked at" tags are indicative.
