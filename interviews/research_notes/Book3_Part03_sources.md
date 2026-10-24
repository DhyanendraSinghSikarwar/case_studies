# Book 3 Part 3 — Sources & research notes (Subqueries and CTEs)

Date: 2026-10-24. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch returns a model-summarised view ("as summarised"). No candidate-reported questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found; every source is a prep guide, practice-site lesson, documentation page or a search snippet.

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| SQLite WITH clause | https://www.sqlite.org/lang_with.html | official docs | CTE syntax and column list; MATERIALIZED / NOT MATERIALIZED hints (3.35.0, non-binding, default lets SQLite choose); multiple CTEs in one WITH; WITH on SELECT, INSERT, DELETE, UPDATE; not allowed in CREATE TRIGGER; CTE multi-reference implied, not stated as a rule |
| SQLite expressions | https://www.sqlite.org/lang_expr.html | official docs | scalar subquery = first row, NULL if empty; EXISTS 1/0 ignoring NULLs; IN / NOT IN NULL matrix and empty right side; row values; correlated re-evaluated vs uncorrelated once |
| SQLite SELECT syntax | https://www.sqlite.org/lang_select.html | official docs | excerpt truncated: alias requirement on FROM-subquery and LIMIT/OFFSET rules NOT confirmed from the page |
| PostgreSQL WITH queries | https://www.postgresql.org/docs/current/queries-with.html | official docs | materialization defaults (single-use inlined, multi-use materialised), MATERIALIZED / NOT MATERIALIZED, data-modifying CTEs. The PostgreSQL 12 version number is NOT on the page |
| PostgreSQL subquery expressions | https://www.postgresql.org/docs/current/functions-subquery.html | official docs | EXISTS, IN, NOT IN, ANY/SOME, ALL, NULL rules, empty-subquery results, error on more than one row for a scalar subquery |
| MySQL 8.4 subquery restrictions | https://dev.mysql.com/doc/refman/8.4/en/subquery-restrictions.html | official docs | cannot modify and select from same table in a subquery (error 1093 not on page), derived-table workaround, LIMIT in IN/ALL/ANY/SOME error 1235, ALL/ANY need scalar left side |
| MySQL 8.4 WITH | https://dev.mysql.com/doc/refman/8.4/en/with.html | official docs | WITH before SELECT/UPDATE/DELETE and before SELECT in INSERT; earlier CTE references only; CTE referenceable many times vs derived table once; one WITH per level |
| pandas user guide: groupby | https://pandas.pydata.org/docs/user_guide/groupby.html | official docs | transform returns same-index result, aggregate broadcast, fillna(grouped.transform('mean')); dropna=True drops NA group keys |
| pandas Comparison with SQL | https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html | official docs | isna/notna vs IS NULL; null merge keys match each other (unlike SQL); no isin or transform coverage on the page |
| datadriven.io SQL Subquery | https://datadriven.io/sql/subquery | practice-site guide | interview patterns: above average, IN, EXISTS, derived table, correlated latest per user, rewrite nested as CTE, NOT EXISTS vs NOT IN, second highest per department |
| LetsDataScience CTE vs subquery guide | https://letsdatascience.com/blog/sql-cte-vs-subquery-interview-guide | blog guide | 13 sample questions incl. above department average, anti-join, correlated-to-join rewrite, multi-CTE pipeline, funnel, CTE reuse; materialization claims (PostgreSQL multi-use materialised, single-use inlined from 12) |
| StrataScratch Understanding Subqueries | https://www.stratascratch.com/learn/comprehensive-sql/understanding-subqueries | lesson | scalar, IN, NOT IN (NULL warning), EXISTS, SELECT-list, derived table, correlated; named problems Find Above-Average Earners, Workers With The Highest Salaries, Customers with Large Orders |
| GeeksforGeeks SQL interview questions | https://www.geeksforgeeks.org/sql/sql-interview-questions/ | prep guide | has subquery (Q5), CTE (Q10), correlated subquery (Q16), EXISTS vs IN (Q17); no derived-table or nth-highest entry |

## Fetch failed / empty
- pandas DataFrameGroupBy.transform reference page: 404 (the user-guide groupby page was used instead). StrataScratch blog sql-subquery-interview-questions: 404. tryexponent subqueries-and-CTEs course page: redirects to aced.io, which returned empty content. 

## Search results only (snippets, not opened)
- tryexponent / prachub CTE-and-subquery question topic pages, a Scribd SQL optimization document, bowtiedraptor Substack SQL 9 subqueries, thedataschool.co.uk subqueries and CTEs, goodspace.ai and educative.io SQL query lists: patterns echo the opened guides (correlated per-row logic, anti-joins, multi-step CTEs).
- LeetCode problems known only from third-party list/solution snippets (GitHub mirrors, Scribd uploads): 1045 Customers Who Bought All Products (GROUP BY HAVING COUNT DISTINCT = total products), 177 Nth Highest Salary (return NULL if absent; DISTINCT ... LIMIT OFFSET), 184 Department Highest Salary. No official LeetCode page was opened (earlier parts saw 403).
- StrataScratch / DataLemur company-labelled subquery problems (Amazon, Google): the search surfaced no actual problem pages; the company link is unverified.
- India-company specifics: no subquery- or CTE-specific candidate reports found.

## Provenance of the 40 questions
- Guide-supported: scalar, IN/NOT IN NULL trap, EXISTS vs IN, correlated above-department-average, derived tables, CTE basics, CTE vs subquery, refactor nested to CTE, anti-join, correlated-to-join rewrite, percent of total, above-average customers, subquery in HAVING.
- LeetCode-style (snippets): customers who bought all products, nth highest salary, department highest salary (max-per-group ties).
- Documentation-supported: scalar many-row/zero-row behaviour, ANY/ALL semantics and empty sets, MATERIALIZED hints, MySQL 1093 and 1235 restrictions, WITH in UPDATE/DELETE, derived table vs CTE reuse, pandas transform and dropna.
- Expert gap-check only: INSERT ... SELECT archive, UPDATE/DELETE with subquery cases, top-N per group and second-highest per group via correlated count, median via LIMIT/OFFSET, earlier-average correlated query, cohort and funnel CTE scaffolding, fan-out hidden in a CTE, pandas pipe/assign translation, dialect map, empty-subquery behaviours.
- Candidate-reported: none.

## Unverified; Wave B must hedge or run
- Whether SQLite requires an alias on a FROM-subquery; LIMIT/OFFSET with expressions and LIMIT -1; UPDATE ... FROM (SQLite 3.33+ from general knowledge); behaviour of a many-row scalar subquery in SQLite (docs say first row; run it); row-value comparisons; WITH before INSERT/UPDATE/DELETE syntax in SQLite 3.45 (page gives no examples; run it); MySQL error 1093 and 1242 numbers; PostgreSQL 12 inlining version; MATERIALIZED hints in other engines; correlated-subquery decorrelation by optimisers; SQL Server, Oracle, BigQuery, Snowflake behaviours; median via PERCENTILE_CONT availability; pandas 3 copy-on-write statements, isin NaN matching, transform with NaN keys, min_count sums and expanding().mean().shift() (run on pandas 3.0.x); relational-division vacuous-truth results (run).
