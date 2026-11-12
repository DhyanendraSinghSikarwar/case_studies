# Review: Book02_Part10.md (Wave C)

Checker: Wave C reviewer, SQLite 3.45.1, pandas 3.0.5. Tables rebuilt from the markdown and every SQL block run.

## Counts
- Answers checked: 43 (Q1-Q43).
- Executed OK: 43. 32 matched the printed Output exactly through an automated rebuild. The other 11 were checked with hand-built scripts:
  - Q5, Q16, Q19, Q36 (DELETE and rebuild scripts, including the unsafe NULL version in Q5, the 3-pass batch in Q36 and the rebuilt tables).
  - Q7 (one-row table gives NULL, no-DISTINCT gives 90000).
  - Q21 (grid expanded to 20 rows), Q33 (guarded and unguarded recursion), Q37.
  - Q35 (UNIQUE and NOCASE behaviour), Q38 (OFFSET and keyset pages, delete case), Q43 (three queries give the same 2 rows).
- Plan answers Q8, Q9, Q10, Q15, Q27, Q28, Q39, Q40: EXPLAIN QUERY PLAN rebuilt on generated data and every plan string matched. Row counts and timings depend on the author's random data and are not reproducible (labelled machine-dependent in the text).
- pandas: all 33 snippets that have a pandas block ran without error. The printed Results match, except Q20 (variable clash, fixed below).
- Fixed: 7 edits.

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| 19 | Example said "6 clean rows, 7 in the table"; the sample data de-duplicates to 4 rows | Changed to 7 rows in the table, 4 after de-duplication |
| 43 | Plan for "correlated subquery, no index" showed an index search on ix_d, which does not exist without an index (real plan: `SCAN e2`) | Replaced with `SCAN e; CORRELATED SCALAR SUBQUERY 1; SCAN e2` |
| 20 | pandas snippet assigned `result` twice, so the gap-ranges frame overwrote the missing-numbers frame | Second frame renamed `gap_ranges` |
| 26 | The NOT EXISTS result table started in the middle of a text line and would not render | Put the table on its own lines |
| 7 | "PostgreSQL 13+" for OFFSET ... FETCH FIRST is wrong; FETCH FIRST is much older (13 added WITH TIES). From memory | Removed the version |
| 36 | `COUNT(DISTINCT (emp_id, swipe_time))` is not valid in several databases | Reworded to "distinct (emp_id, swipe_time) pairs" |
| 8 | "366 rows match" is not reproducible from the stated seed (my rebuild gave 361) | Changed to "a few hundred rows match" |

## Checks with no change
- Template fields are present throughout. Concept and design answers (Q8, Q9, Q10, Q15, Q27-Q29, Q35, Q36, Q39, Q40) have Example, Edge cases and Follow-ups. Where Sample data or pandas is absent, the answer says why.
- Q22 has no Sample data table (it generates numbers); fine.
- Order and numbering: stars descend (3, 2, 1) and difficulty goes green to red within each star group. Q1-Q43 are continuous. The header says "Target 40 / Actual 43".
- Code fences are balanced (even count) and all tables render after the Q26 fix.
- "Asked at" claims (Myntra and Infosys Glassdoor for second highest) are supported by research/Book02_Part10_sources.md. The other answers say "commonly asked".

## Unresolved / unverified
- Row counts and timings in Q8, Q10, Q27, Q28, Q38 and Q43 come from the author's generated data (seeds not reproducible exactly). Plans match; counts are not re-verified. Q38 and Q43 timings are labelled machine-dependent.
- Not run here (already labelled in the text): all PostgreSQL, MySQL and SQL Server syntax, including the Q33 CYCLE clause and Q39 INCLUDE.
- Statements marked "from memory" were left as marked: InnoDB-style behaviour, PostgreSQL 18 skip scan, MySQL error 1093, the SQL Server NULL-in-UNIQUE rule, the MAXRECURSION and cte_max_recursion_depth defaults.
- Overlap, report only: Q3/Q4/Q6/Q7/Q18 all cover Nth highest on purpose, with cross-references. Q21/Q31/Q42 are related gaps-and-islands forms. Q30 (running total) overlaps Part 6 (stated in scope); Q37 median may overlap other parts.
