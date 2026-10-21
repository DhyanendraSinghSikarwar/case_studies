# Book 2 — SQL | Part 12: How to Develop SQL Skills

**Target:** 20 | **Actual:** 24 | **Scope:** learning-journey interview questions plus the full zero-to-job-ready skill-development plan (roadmap, daily plan, free resources, datasets, mini-projects, self-check tests).

## Questions

### Q1 ⭐⭐⭐ 🟢 How did you learn SQL, and how long did it take you?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 How would you rate yourself in SQL out of 10, and why?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Which platforms have you practised SQL on?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Which database or tool have you used to write SQL (MySQL, PostgreSQL, SQL Server, SQLite)?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 You come from HR with no technical background. How did you learn SQL?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Walk me through a SQL project you built from start to finish.
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 How much SQL practice do you do daily, and roughly how many problems have you solved?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 In what order did you study SQL topics, and why that order?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐ 🟢 How do you stay current with SQL and data skills?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐ 🟢 Which free resources would you recommend to a SQL beginner?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐ 🟢 Which practice datasets have you worked with?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐ 🟢 How would you set up a free SQL practice environment on your own laptop?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐ 🟢 What HR questions can SQL answer that Excel struggles with?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟡 Which SQL topic did you find hardest, and how did you overcome it?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟡 How do you check that your own SQL answer is correct when no answer key exists?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 How would you prepare for a live SQL round in two weeks?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 The interview uses a different SQL dialect from the one you practised. How do you cope?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 How do you use AI assistants to learn SQL without depending on them?
<!-- ANSWER_PENDING -->

### Q19 ⭐ 🟢 Do SQL certifications help, and have you done any?
<!-- ANSWER_PENDING -->

### Q20 ⭐ 🟢 Have you shared your SQL work publicly, for example on GitHub?
<!-- ANSWER_PENDING -->

### Q21 ⭐ 🟡 How would you build a SQL portfolio project from a public dataset?
<!-- ANSWER_PENDING -->

### Q22 ⭐ 🟡 How do you know you are job-ready in SQL? What self-test would you use?
<!-- ANSWER_PENDING -->

### Q23 ⭐ 🟡 What do you do in a timed SQL test when you cannot finish all the questions?
<!-- ANSWER_PENDING -->

### Q24 ⭐ 🔴 How would you teach SQL to a non-technical colleague in four weeks?
<!-- ANSWER_PENDING -->

---

## Skill-Development Plan (final content)

Source for resources: `research/Book02_Part12_sources.md` (checked 2026-10-21). Only resources whose pages loaded are listed. "Free?" states what the page itself said; "not stated" means the page loaded but showed no price, so check before relying on it.

Market context (plan.md Section 2): SQL appears in about 54% of sampled JDs (MIS/reporting roles 44%) and in nearly all sampled interview profiles. Startups ask the hardest SQL (window functions, recursive CTEs).

### A. 12-week zero-to-job-ready roadmap (non-technical beginner)

Assumes about 2 hours a day, 6 days a week. Each week maps to Parts of Book 2. Pair with Excel basics if you are new to tables of data.

| Week | Goal | Book 2 part | Practice output | Weekly check |
|---|---|---|---|---|
| 1 | What a database, table, row, column and key are; install a practice tool; first SELECT | Part 11 (concepts, read lightly), Part 1 | 25 SELECT/WHERE/ORDER BY/DISTINCT/LIMIT queries | Quiz 1 |
| 2 | Filtering well: AND/OR/IN/BETWEEN/LIKE, NULL basics | Part 1, Part 7 (NULL section) | 30 filter queries on an employee table | |
| 3 | Aggregates, GROUP BY, HAVING | Part 2 | 30 queries (headcount by department, average salary by grade) | Quiz 2 (end of wk 3) |
| 4 | Joins: INNER and LEFT first | Part 3 | 25 joins on employees + departments + attendance | |
| 5 | RIGHT/FULL/SELF/CROSS joins; join traps (duplicates, NULLs) | Part 3 | 20 more joins incl. manager-employee self join | Quiz 3 |
| 6 | Subqueries and CTEs | Part 4 | 25 queries rewritten both ways | |
| 7 | Window functions I: ROW_NUMBER, RANK, DENSE_RANK, top-N per group | Part 5 | 25 queries (top 3 earners per department) | Quiz 4 |
| 8 | Window functions II: running totals, LAG/LEAD, moving average | Part 6 | 20 queries (month-on-month hires) | |
| 9 | CASE WHEN, strings, dates, NULL handling | Part 7 | 30 cleaning/bucketing queries (tenure bands, age bands) | Quiz 5 |
| 10 | Business scenarios: sales, HR, e-commerce, banking | Part 8 | 15 scenario queries, written from a plain-English brief | |
| 11 | Retention, cohorts, funnels, MoM growth; de-duplication, nth highest, gaps and islands, recursive CTE, optimisation basics | Parts 9, 10 | 15 hard queries; explain each aloud | Quiz 6 |
| 12 | Consolidate: database concepts, mock interviews, mini-project polish | Part 11, Part 12 | 2 timed mock tests (45 min each) + finished project on GitHub | Final test |

Rules of thumb: finish a part only when you can write its queries without looking at notes. If a quiz fails, repeat that week's practice before moving on.

### B. Daily practice plan (2 hours)

| Block | Minutes | What |
|---|---|---|
| Learn | 30 | Read/watch one concept (this week's Book 2 part or one free lesson) |
| Guided practice | 30 | Type out and run the lesson examples; change one thing and predict the result |
| Problem solving | 40 | 3 to 5 problems from a practice platform; attempt 15 min before reading any hint |
| Review | 20 | Redo one yesterday's failed problem from scratch; add it to a "mistakes log" (query, error, fix) |

Weekly: one 45-minute timed set on Saturday; Sunday off or revision of the mistakes log. If you have only 1 hour: halve each block, never skip Review.

### C. Free resources (verified loaded; free status as observed)

| Name | URL | What for | Free? |
|---|---|---|---|
| SQLBolt | https://sqlbolt.com | Short interactive lessons and exercises in the browser; week 1 to 3 | Page loaded; price not stated (appears free to use) |
| W3Schools SQL | https://www.w3schools.com/sql/ | Syntax reference and "Try it Yourself" editor | Yes (stated) |
| SQLZoo | https://sqlzoo.net | Step-by-step interactive exercises, good for joins | Yes (stated) |
| Mode SQL Tutorial (now hosted by ThoughtSpot) | https://www.thoughtspot.com/sql-tutorial (old mode.com/sql-tutorial redirects here) | Analyst-style tutorial, basic to advanced | Not stated; login requirement unverified |
| DataLemur | https://datalemur.com | Interview-style questions tagged by company; free SQL tutorial and 9-day crash course | Partly: tutorial and crash course stated free; a Premium tier exists, locked questions unverified |
| StrataScratch | https://www.stratascratch.com | Interview questions; "Comprehensive SQL" learning path | Partly: free sign-up and SQL path stated free; other features may be paid |
| HackerRank SQL | https://www.hackerrank.com/domains/sql | Easy/Medium/Hard SQL challenges, similar to online assessments | Account needed; price not stated on page |
| LeetCode Top SQL 50 | https://leetcode.com/studyplan/top-sql-50/ | Widely used SQL practice list | UNVERIFIED: page blocked (HTTP 403) to the fetch tool, so not read; open it yourself and check what needs Premium |
| SQLite | https://www.sqlite.org/download.html | Zero-setup local database (one file) | Licence page linked; public domain per general knowledge (unverified on page) |
| DB Browser for SQLite | https://sqlitebrowser.org | Point-and-click viewer/editor for SQLite files | Open source (stated); price not stated |
| DuckDB | https://duckdb.org/docs/ | Local analytics SQL that reads CSV files directly | Documentation loaded (open-source status not confirmed on fetched page) |
| PostgreSQL | https://www.postgresql.org/download/ | Full database used in many companies | Yes (open source, PostgreSQL License) |
| SQL Online IDE | https://sqliteonline.com | Run SQLite/DuckDB/PostgreSQL in the browser with no install | Page loaded; has a Pricing page, free-tier limits unverified |

Not verified at all (not listed as resources): any YouTube channel, Kaggle Learn, GeeksforGeeks, Coursera/Udemy courses.

### D. Practice datasets

| Dataset | URL | What it is | Good for | Notes |
|---|---|---|---|---|
| Chinook | https://github.com/lerocha/chinook-database | Digital media store: artists, albums, tracks, invoices, customers, employees. Scripts for SQLite, PostgreSQL, MySQL, SQL Server, others | Joins, GROUP BY, window functions | Licence file not read; customer/employee data fictitious |
| Northwind (SQLite3 port) | https://github.com/jpwhite3/northwind-SQLite3 | Classic trading-company database: orders, products, customers, employees | Joins, subqueries, business reports | MIT licence (stated) |
| AdventureWorks | https://github.com/microsoft/sql-server-samples/releases/tag/adventureworks | Microsoft sample company DB (OLTP, LT and DW versions), .bak backups and install scripts | Larger multi-table practice | Needs SQL Server to restore; heavier setup, optional |
| IBM HR Analytics Attrition (Kaggle) | https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset | HR attrition and performance data (single table) | HR projects, GROUP BY, CASE WHEN | Page title seen only; Kaggle login and licence for download unverified; load the CSV into SQLite or DuckDB |
| Self-made HR tables | (build it yourself) | employees, departments, attendance, hires, exits (50 to 200 rows) | Anything; you know the right answer | Create with CREATE TABLE/INSERT or a CSV from Excel |

### E. Five mini-projects (each ends on GitHub with a README)

| # | Project | Data | What you build | Deliverables |
|---|---|---|---|---|
| 1 | HR attrition SQL project | IBM HR attrition CSV (or self-made HR tables) in SQLite/DuckDB | 10 to 12 queries: attrition rate by department, by tenure band (CASE WHEN), by overtime; top-3 earners per department (window); average salary gap by job role | `.sql` file, one-page findings (5 bullets with numbers), README with schema and how to run |
| 2 | Sales / orders analysis | Northwind (SQLite) | Revenue by month and category, top 5 customers, repeat vs new customers, MoM growth (LAG) | Query file, a results table per question, a 3-line business recommendation |
| 3 | Music store insights | Chinook | Best-selling genres, revenue per country, customers with no purchases (LEFT JOIN), running total of invoices | Query file, written explanation of each join choice |
| 4 | Hiring funnel and cohort retention | Self-made HR tables (applicants, interviews, offers, joiners, exits) | Stage-wise conversion, time-to-hire, 3/6/12-month retention by joining month cohort | Table creation script, query file, funnel table, 150-word summary |
| 5 | Data-quality audit | Any table above with injected defects (duplicates, NULLs, bad dates) | De-duplication with ROW_NUMBER, NULL report, inconsistent-category fix, before/after counts | Audit query file, before/after table, list of rules you applied |

For every project, state: the business question, the tables used, the answer in one sentence with numbers, and one limitation.

### F. Self-check tests (milestones)

Take each closed-book, timed, on a database you did not practise on if possible. Pass = at least the stated score; below it, repeat that week's practice and retake after 3 days.

| Quiz | After week | Content | Time | Pass criteria |
|---|---|---|---|---|
| 1 | 2 | 10 queries: SELECT, WHERE, ORDER BY, DISTINCT, LIMIT, NULL filter | 25 min | 8/10 correct on first run |
| 2 | 3 | 8 queries: COUNT/SUM/AVG, GROUP BY, HAVING | 30 min | 7/8 correct; can explain WHERE vs HAVING aloud |
| 3 | 5 | 8 join queries across 3 tables incl. LEFT JOIN with NULL check and self join | 40 min | 6/8 correct; no accidental row duplication |
| 4 | 7 | 6 queries: subquery, CTE, ROW_NUMBER/RANK/DENSE_RANK top-N per group | 40 min | 5/6 correct; can state RANK vs DENSE_RANK difference |
| 5 | 9 | 8 queries: CASE WHEN, date/string functions, LAG/LEAD, running total | 45 min | 6/8 correct |
| 6 | 11 | 5 scenario queries from plain-English briefs (cohort, funnel, nth highest, de-dup, MoM) | 60 min | 4/5 correct and each explained in under 2 minutes |
| Final | 12 | Mock live round: 2 easy, 2 medium, 1 hard, speaking your thinking aloud | 45 min | 4/5 correct, every answer checked for NULLs, duplicates and ties; project walkthrough delivered in 3 minutes |

Job-ready signal: you pass the Final twice in a row on two different datasets and have at least two finished mini-projects online.
