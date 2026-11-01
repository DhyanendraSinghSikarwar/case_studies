# Book 3 Part 2 — Sources & research notes (Joins: all types, self, anti/semi)

Date: 2026-10-24. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch returns a model-summarised view ("as summarised"). No candidate-reported questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found; every source is a prep guide, question bank, documentation page or a search snippet.

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| pandas user guide: Merge, join, concatenate and compare | https://pandas.pydata.org/docs/user_guide/merging.html | official docs (pandas 3.1.0 page) | how= left/right/outer/inner/cross; validate (MergeError; one_to_one, one_to_many shown); indicator and _merge values; suffixes default; many-to-many Cartesian product; join defaults to left on index; concat join default outer; merge_asof; compare(). The page does NOT cover NaN-key matching or dtype mismatch |
| pandas merge_asof reference | https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html | official docs | sorted ascending key requirement, by, direction (backward/forward/nearest), tolerance, allow_exact_matches |
| StrataScratch SQL join interview questions | https://www.stratascratch.com/blog/sql-join-interview-questions/ | prep guide | six problems: Comments distribution (Facebook, INNER), Highest cost orders (Amazon, LEFT), Customer orders and details (RIGHT), Arizona/California/Hawaii employees (Amazon, FULL OUTER), Difference between times (Deloitte, CROSS), provinces with more wines (non-equi). Company labels as given by the guide, not candidate reports |
| DataCamp top SQL joins interview questions | https://www.datacamp.com/blog/top-sql-joins-interview-questions | prep guide | 20 questions: join types, outer/inner/cross, self join, full vs cross, aliases, equi, ON vs USING, natural, join vs UNION, semi, anti, INTERSECT vs inner, cross join performance, conditional joins, WHERE vs ON |
| InterviewBit SQL joins interview questions | https://www.interviewbit.com/sql-joins-interview-questions/ | prep guide | join three tables, self join, one-to-many and many-to-many structure, natural, equi, non-equi, UNION vs JOIN, full vs cross, nested/correlated subquery vs join, merge/hash/nested-loop joins (concept) |
| GeeksforGeeks SQL interview questions | https://www.geeksforgeeks.org/sql/sql-interview-questions/ | prep guide | join types, CROSS vs INNER, self join, UNION vs UNION ALL; no NATURAL JOIN question |
| explainextended: LEFT JOIN / IS NULL vs NOT IN vs NOT EXISTS, nullable columns | https://explainextended.com/2010/05/27/left-join-is-null-vs-not-in-vs-not-exists-nullable-columns/ | blog (MySQL MyISAM test, old) | NOT IN is three-valued and one NULL gives zero rows; NOT EXISTS handles NULLs; fixes for NOT IN |
| MySQL 8.4 reference: JOIN | https://dev.mysql.com/doc/refman/8.4/en/join.html | official docs | LEFT/RIGHT only (no FULL OUTER JOIN shown); NATURAL = USING on all common columns; coalesced common column order; USING vs ON in SELECT *; LEFT JOIN IS NULL anti-join example. The ON-vs-WHERE trap and the UNION emulation of FULL JOIN were the summariser's general knowledge, not page text |
| SQLite SELECT syntax | https://www.sqlite.org/lang_select.html | official docs | join-operator diagram lists NATURAL, LEFT, RIGHT, FULL, INNER, CROSS; compound operators UNION, UNION ALL, INTERSECT, EXCEPT; version of RIGHT/FULL support NOT stated in the opened excerpt |

## Fetch failed
- GeeksforGeeks sql-join-interview-questions: 404. LearnSQL sql-joins-interview-questions: 404. LeetCode study plan top-sql-50: 403.

## Search results only (snippets, not opened)
- LeetCode SQL 50 join problems (third-party GitHub repo lists, not official): Basic Joins includes Students and Examinations (problem 12 in one repo); Advanced Select and Joins in one repo: The Number of Employees Which Report to Each Employee, Primary Department for Each Employee, Triangle Judgement, Consecutive Numbers, Product Price at a Given Date, Last Person to Fit in the Bus, Count Salary Categories. Employees Earning More Than Their Managers and Managers with at Least 5 Direct Reports were not confirmed in this search; they are well known LeetCode problems but their section is unverified here.
- Self-join employee/manager salary: MSDN blog, designgurus.io, dataford.io snippets (NULL manager excluded; join usually preferred to correlated subquery). One Scribd guide lists 'employees hired before managers' and a three-level hierarchy (snippet only).
- Fan and chasm traps: Coginiti glossary, Sisense docs, Holistics, Honeydew, a Substack and a Buttondown post, Varsity Tutors lesson (snippets): repeated parent rows inflate SUM, aggregate each child to a common grain before joining, COUNT DISTINCT helps counts only, SUM(DISTINCT) drops legitimate duplicates.
- NOT IN vs NOT EXISTS vs LEFT JOIN IS NULL: further explainextended posts (PostgreSQL, SQL Server) and SQL Server Central snippets: LEFT JOIN IS NULL and NOT EXISTS equivalent semantically; NOT IN differs on NULLs; plan equality in PostgreSQL and a less efficient LEFT JOIN in SQL Server per the snippets.
- ai2sql 'Interview Prep JOINs' (2026 article, eight join questions incl. anti and semi join): snippet only. DataLemur: no page returned by search.
- India-company specifics (Flipkart, Swiggy, Amazon): no join-specific candidate reports found.

## Provenance of the 45 questions
- Guide-supported: join types, ON vs WHERE, self join, cross join and cartesian risk, natural, USING vs ON, equi/non-equi, UNION vs JOIN, UNION vs UNION ALL, semi and anti joins, INTERSECT/EXCEPT, three-table joins, join performance concept, FULL JOIN problems.
- LeetCode-style (snippets): Students and Examinations, employees vs managers, Consecutive Numbers, managers with 5 reports.
- pandas-docs-supported: merge how/validate/indicator/suffixes, join vs merge vs concat, many-to-many product, merge_asof, cross merge, DataFrame.compare.
- Expert gap-check only: fan-out debugging variants, chasm trap, date-range price joins, interval overlap, snapshot comparison, calendar grid, market-basket pairs, relational division, reconciliation cases, dialect map, NaN-key and dtype-mismatch details, null-safe operators.
- Candidate-reported: none.

## Unverified; Wave B must hedge or run
- SQLite RIGHT/FULL JOIN since 3.39 (not stated on the opened page; run on 3.45 to confirm); MySQL has no FULL OUTER JOIN (MySQL 8.4 page supports this by omission); MySQL INTERSECT/EXCEPT support by version; EXCEPT vs MINUS (Oracle); PostgreSQL IS NOT DISTINCT FROM and MySQL <=>; SQLite null-safe `IS` operator (verify by running); USING semantics and qualified column rules per engine; NATURAL JOIN behaviour in SQLite (run it); ASOF JOIN existence in other engines; join algorithm names per engine; NaN keys matching each other in pandas merge and the exact errors for int vs object keys (run on pandas 3.0.x); validate error messages; behaviour of merge_asof with unsorted input. Optimiser claims about join order and index use are concept-level and hedged.
