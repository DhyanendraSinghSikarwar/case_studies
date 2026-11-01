# Book 3 Part 10 review (Wave C)

Date: 2026-10-25. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (40 of 40 merged, 0 skipped, 0 pending; no spend-limit stops this part). Five corrections to the Wave A sources note found by one agent (printf %.0f truncation, the (VALUES ...) AS q(col) syntax error, error-text case, TEXT-affinity conversion of ' 12', to_datetime mixed/dayfirst) were verified where checkable (printf truncation re-run by the lead) and passed to the agents still writing. The lead's own "error text is uppercase REGEXP" correction was an over-reading: SQLite echoes the function name in the case typed in the SQL, so both lowercase and uppercase appear in the answers and both are right. Header status updated after the merge.

## Structure checks (scripted, scratch/review_scripts/check_book3.py)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40 | pass |
| Star order and counts 15 / 16 / 9 | pass (matches header) |
| All template labels in every answer | pass for all 40 |
| Exactly one sqlite3 Code program per question, run standalone with `python3 -I` | 40 of 40 exit 0 |

## Code
Each program builds the data in SQLite 3.45.1, runs the SQL (CASE pivots, UNION ALL and CROSS JOIN VALUES unpivots, string functions, recursive splits, generated dynamic pivots), runs pandas 3.0.5 and asserts SQL equals pandas, or asserts the stated difference where the two intentionally disagree.

## Items the Wave A note listed as unverified, now run (3.45.1 / 3.0.5)
Missing in SQLite: regexp (unless registered per connection via create_function), split_part, reverse, lpad, char_length, PIVOT/UNPIVOT, GROUPING SETS; present: concat, concat_ws, string_agg and group_concat with ORDER BY (3.45.1), format/printf, octet_length, unhex, iif, IS DISTINCT FROM; printf('%.0f') truncates; printf comma flag works on this build (extension, hedged); group_concat(DISTINCT x, sep) is rejected; PRAGMA case_sensitive_like makes LIKE match GLOB case rules; STRICT tables accept ' 12' into INTEGER (stored 12) and reject 'x'; TRIM strips only spaces; UPPER/LOWER ASCII-only; LENGTH stops at an embedded NUL; DATE('2024-02-30') returns 2024-03-01; SQLite limits via getlimit (2000 columns, 250,000 bound parameters); pandas: str dtype default with NaN, str.title("o'neil") gives O'Neil but "they're" gives They'Re, str.count overlap behaviour, read_csv default NA markers, stack(future_stack) row counts, pivot_table/crosstab/margins NaN behaviour, to_datetime(format='mixed', dayfirst=True) flipping ISO dates, astype(str) keeping NaN in pandas 3.

## Findings kept in the text
Dynamic pivot with NOT IN alone misses NULL categories (27 vs 31); UNION collapses duplicates (5 rows vs 7); three scans vs one for UNION ALL vs CROSS JOIN VALUES; pivot totals with NULL cells (East and North NULL, West 80, plain SUM 420); pandas margins grand total 410 vs 420 because NaN-month rows drop; aggfunc='first' picks a different duplicate than MAX; naive email-validity LIKE accepts 'a@b@c.com'; three nested REPLACEs leave a double space on a 10-space run; NULL name bonus decision; division by zero is NULL in SQLite; IFNULL with 3 arguments errors; CAST round-trip check misfires on '1200'; stripping non-digits turns an extension row into a fake phone number; NBSP inside text needs a \s+ collapse; pandas Series.round(2.675) gives 2.68 while Python and SQLite give 2.67 (cause not verified); ß and İ case-folding differences; the NULL subtotal label is indistinguishable from a real NULL; reading default NA tokens ('Null', 'na', 'NAN' stay text).

## Not verified (hedged "not executed" in the text)
PIVOT/UNPIVOT (SQL Server, Oracle, Snowflake, BigQuery; UNPIVOT dropping NULLs, INCLUDE NULLS; Snowflake PIVOT ANY), PostgreSQL crosstab/tablefunc, FILTER (PostgreSQL yes, MySQL no; SQLite 3.30 date "I believe"), STRING_SPLIT, SPLIT_PART, SUBSTRING_INDEX, REGEXP_* and REGEXP_COUNT, INITCAP, LPAD/RPAD, TO_CHAR/FORMAT, TRY_CAST/SAFE_CAST, LISTAGG/STRING_AGG, GROUPING(), NULLS NOT DISTINCT (PostgreSQL 15), SQL Server unique-index NULL behaviour, Oracle treating '' as NULL, QUOTENAME/sp_executesql/EXECUTE IMMEDIATE, engine column limits, pandas 2.x astype(str) behaviour, the SQLite 3.44 release note for group_concat ORDER BY, LeetCode statements (1484, 1795, 1667, 1527, 1873 from the doocs mirror).

## Evidence limits
No candidate-reported questions were found; evidence is prep guides, public problem banks, the SQLite core function and expression docs, the pandas reshaping and text guides and a LeetCode mirror (leetcode.com not opened). No source states a salary band; salary values appear only as toy column data. Stars and "Asked at" tags are indicative.
