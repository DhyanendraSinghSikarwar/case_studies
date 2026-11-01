# Book 3 Part 9 Sources & research notes (Recursive CTEs, hierarchies, graphs)

Date: 2026-10-25. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch returns a model-summarised view ("as summarised"). No candidate-reported SQL questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found or relied on; every source is documentation, a guide, a practice-site page, a forum thread or a search snippet. Final count: 30 questions (3-star 12, 2-star 11, 1-star 7). No 503s occurred on the opened pages.

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| SQLite WITH clause | https://www.sqlite.org/lang_with.html | official docs | compound select rules, UNION dedup stops cycles, UNION ALL low memory, LIMIT/OFFSET in recursive select, ORDER BY as queue order (BFS/DFS), no aggregates or windows in the recursive select, queue algorithm, 3.34 compound recursive part |
| PostgreSQL WITH queries | https://www.postgresql.org/docs/current/queries-with.html | official docs | working and intermediate table evaluation, UNION vs UNION ALL on cycles, SEARCH DEPTH/BREADTH FIRST BY ... SET, CYCLE ... SET ... USING, parent LIMIT trick (not to rely on) |
| MySQL 8.4 WITH | https://dev.mysql.com/doc/refman/8.4/en/with.html | official docs | WITH RECURSIVE required, cte_max_recursion_depth default 1000, max_execution_time and hint, LIMIT in recursive part, forbidden constructs, types fixed by anchor (CAST), Fibonacci, date series, employee path examples |
| jdsatpathy Substack | https://jdsatpathy.substack.com/p/sql-recursive-cte-interview-problem | blog | manager chain up to the CEO; no cycle guard, UNION ALL |
| DataVidhya recursive hierarchy | https://datavidhya.com/learn/sql/interview-patterns/recursive-hierarchy/ | prep lesson | reports under a manager, ancestors of a category, dependency-graph paths, depth tracking and cycle detection |
| doocs LeetCode 1270 | https://leetcode.doocs.org/en/lc/1270/ | LeetCode mirror | head = employee 1, at most 3 levels, two self-joins; not a recursive solution |

## Search results only (snippets, not opened)
- Interview lists: datadriven.io recursive-cte and advanced-sql pages, Medium 'Mastering SQL recursive CTEs', datavidhya recursive CTEs, itprotoday 'Cycling with CTEs' (path flag), a LinkedIn '300 real SQL interview questions' guide (names PwC, Deloitte, EY, KPMG, Tredence, Persistent, Accenture as targets of the guide; not a candidate report), Hello Interview and DataVidhya 'given manager' framing of 1270.
- Engines: SQL Server MAXRECURSION (mssqltips, Database Journal, Microsoft Q&A: default 100, Msg 530, 0 to 32767, 0 = unlimited, hint at the end of the outer statement, not in views or functions); Oracle hierarchical queries (docs 21c and 23: START WITH, CONNECT BY PRIOR, LEVEL, SYS_CONNECT_BY_PATH, CONNECT_BY_ISLEAF, NOCYCLE, CONNECT_BY_ISCYCLE, ORA-01436); Snowflake CONNECT BY docs (no NOCYCLE/ISCYCLE/ISLEAF).
- Storage models: Medium 'From Trees to Tables', dev.to ltree vs adjacency vs closure, oneuptime MySQL hierarchical schema, macmyths, jopr (rules of thumb only).
- Threshold reset: SQLServerCentral threads and Microsoft Q&A (no set-based form; recursive CTE as a loop; risk of the recursive running total misbehaving).
- Not found: a recursive CTE loan amortisation interview source; company-specific recursive CTE question reports. Those questions are expert additions.

## Environment checks (run)
- SQLite 3.45.1. Works: WITH RECURSIVE, group_concat, power/exp/ln (math functions compiled in). Fails: `CYCLE ... SET ... USING` and `SEARCH DEPTH FIRST` clauses (syntax error near cycle/search); `generate_series` (no such table); second reference to the CTE in the recursive member, even in a subquery (multiple recursive references).
- Python: networkx 3.6.1 installed; scipy NOT installed (ModuleNotFoundError); duckdb NOT installed. Use plain Python (heapq, deque, graphlib) as main, networkx as a check.
- Cross-references verified by heading: Part 6 Q31 (calendar table with recursive CTE, generate_series and pd.date_range); Part 7 Q24 (cumulative sum reset by flag; threshold variant deferred to Part 9); Part 7 Q31 (working-day calendar).

## Hedge list for Wave B (not verified by running, or from snippets)
- SQL Server: default MAXRECURSION 100, error 530, range 0-32767, no RECURSIVE keyword, hint not allowed in views/UDFs (snippets).
- MySQL cte_max_recursion_depth default 1000 and the forbidden constructs (opened docs, but not executed).
- PostgreSQL 14+ SEARCH and CYCLE (docs opened; the "14" version is from a snippet; not executed), generate_series (not executed).
- Oracle CONNECT BY family and NOCYCLE/ORA-01436 (snippets; not executed). Snowflake CONNECT BY limits (snippet).
- Integer overflow behaviour of factorial in SQLite (turns to float: verify by running) and in other engines (not executed).
- Storage-model costs (nested sets, closure O(n squared) worst case) are rules of thumb from blogs.
- Delete-with-CTE syntax in SQL Server and MySQL 8 (not executed).
- Timings in the performance question are machine specific; run and report.

## Question list shape
3-star (12): execution model, number/date spine, toy recursion, reports under manager, chain upward, level/path/leaf, UNION vs UNION ALL, debugging non-termination, org roll-up, BOM, degrees of separation, threshold reset. 2-star (11): category breadcrumbs, recursion vs join vs window, cycles/orphans, components, flight routes, loan/interest, EWMA/depreciation, subtree delete/move, topological order, weighted shortest path, engine portability. 1-star (7): storage models, pandas frontier merges, pandas roll-ups/explode, plain Python BFS/DFS, SQL vs pandas edge-case behaviour, performance and safety, lowest common ancestor.
