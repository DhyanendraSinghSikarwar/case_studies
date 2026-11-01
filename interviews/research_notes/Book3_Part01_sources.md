# Book 3 Part 1 — Sources & research notes (SELECT, filtering, aggregation, GROUP BY/HAVING)

Date: 2026-10-24. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch returns a model-summarised view ("as summarised"). No candidate-reported questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found for this topic; every source is a prep guide, question bank, documentation page or a search snippet.

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| pandas: Comparison with SQL | https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html | official docs | SELECT/WHERE/GROUP BY/JOIN/UNION/LIMIT sections; isna/notna for IS NULL; size() = COUNT(*), count() = non-null per column; head and nlargest(...).tail for LIMIT/OFFSET; no HAVING section and no as_index mention; join warning that NaN keys match each other |
| pandas DataFrame.groupby reference | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html | official docs | as_index=True default; dropna=True default drops NaN keys; observed default True since 3.0.0; sort=True default |
| GeeksforGeeks SQL interview questions | https://www.geeksforgeeks.org/sql/sql-interview-questions/ | prep guide | WHERE vs HAVING, NULL, COUNT(column) vs COUNT(*), COALESCE, CASE, aggregates, GROUP BY, removing duplicates; no order-of-execution question |
| StrataScratch SQL interview questions guide | https://www.stratascratch.com/blog/sql-interview-questions-you-must-prepare-the-ultimate-guide/ | prep guide | company-labelled bank items: Credit Karma submission types (HAVING COUNT(DISTINCT)), Postmates customer average orders, Zillow cities HAVING vs average, Uber NULL revenue, Facebook NULLs in GROUP/ORDER BY (as listed by the guide, not candidate reports) |
| LearnSQL GROUP BY interview questions | https://learnsql.com/blog/group-by-sql-interview-questions/ | prep guide | WHERE vs HAVING, COUNT variants, NULLs form one group, missing GROUP BY column, ROLLUP/CUBE/GROUPING SETS |
| DEV Community: 5 SQL questions that trip beginners | https://dev.to/juhi_singhal_7d7fb8634472/5-sql-interview-questions-that-trip-up-beginners-5cmi | blog | WHERE vs HAVING, = NULL returns nothing |
| ai2sql aggregate functions interview prep | https://builder.ai2sql.io/blog/sql-aggregate-functions-interview | vendor blog | COUNT variants, MySQL ONLY_FULL_GROUP_BY, AVG with NULLs, SUM(DISTINCT), integer AVG truncation, GROUP BY 1 fragility |
| Karina data scientist newsletter | https://karina-datascientist.beehiiv.com/p/sql-interview-questions-they-actually-ask-and-how-to-answer-them | newsletter | WHERE vs HAVING, COUNT(*) vs COUNT(col), execution order line (bonus tip); later topics (joins, windows) belong to other parts |
| SQLite NULL handling | https://www.sqlite.org/nulls.html | official docs | NULLs indistinct for DISTINCT/UNION; CASE WHEN NULL gives ELSE; page does not document NULL sort order or aggregate results |
| PostgreSQL ORDER BY docs | https://www.postgresql.org/docs/current/queries-order.html | official docs | NULLs sort as if larger: NULLS LAST for ASC, NULLS FIRST for DESC |

## Fetch failed
- DataLemur blog sql-interview-questions: 404. Interview Query sql-interview-questions: 429. GitHub SQL-50 repo page: opened but listed only PDFs, no problem names.

## Search results only (snippets, not opened)
- LeetCode SQL 50 study plan (via GitHub repos and Scribd outlines): sections Select, Basic Aggregate Functions, Sorting and Grouping; problem names seen: Recyclable and Low Fat Products, Find Customer Referee, Big Countries, Article Views I, Invalid Tweets, Classes More Than 5 Students (GROUP BY ... HAVING COUNT), Number of Unique Subjects Taught by Each Teacher, User Activity for the Past 30 Days I, Product Sales Analysis III, Customers Who Bought All Products. The official LeetCode page was not opened; section counts (5, 8, 7) are from a snippet.
- NOT IN with NULL: jOOQ manual, pgvet rules, Microsoft Q&A, SQLServerCentral, DEV (pawsql) snippets: any NULL in the subquery makes the predicate UNKNOWN; fix with NOT EXISTS or filtering NULLs.
- Pandas dropna default versus SQL NULL group: pandas docs snippets and Informix/LearnSQL snippets (NULLs form one group).
- India company context: Glassdoor Flipkart interview pages, Interview Query Flipkart and Swiggy guides, growai.in 2026 analyst guide: SQL rounds, self join and window items, execution order mentioned by one candidate; nothing confirming Part 1 topics per company. The '40 per cent of round time' figure in one guide is unverified and not used.
- Global bank snippets: TryExponent top 25 SQL data science questions, DataDriven.io SQL interview markdown, KDnuggets FAANG SQL patterns, StrataScratch aggregate-functions guide: conditional aggregation, basic aggregation with WHERE before GROUP BY; claims about company sourcing not verified.

## Provenance of the 45 questions
- Guide-supported: SELECT *, execution order, WHERE vs HAVING, COUNT variants, NULL logic, COALESCE, duplicates, GROUP BY rules and errors, CASE, DISTINCT, ROLLUP, AVG/NULL traps, HAVING COUNT(DISTINCT) pattern.
- pandas-docs-supported: SQL-to-pandas translation, size vs count, groupby defaults (as_index, dropna, observed, sort), isna masks, LIMIT/OFFSET equivalents.
- Expert gap-check only: SQLite bare-column special case, median emulation, collation/whitespace, float money, null-safe equality, distinct users per day, mini data-cleaning case, BETWEEN timestamp trap, empty-set aggregates, frequency table, ordering questions where the guides are thin.
- Candidate-reported: none.

## Unverified; Wave B must hedge or run
- NULL sort order in MySQL, SQL Server, Oracle (not opened); ILIKE, DATE_TRUNC, ROLLUP syntax, FILTER support outside SQLite and PostgreSQL, TOP / FETCH FIRST, alias reuse in GROUP BY/HAVING by engine, MySQL default collation and ONLY_FULL_GROUP_BY defaults, SQLite bare-column behaviour with MAX (verify by running), COUNT(DISTINCT a, b) support, row-value comparison support. pandas 3 behaviours (copy-on-write, sum of empty/all-NaN, nlargest keep) must be confirmed by running.
