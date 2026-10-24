# Book 2 — SQL | Part 12: How to Develop SQL Skills

**Target:** 20 | **Actual:** 24 | **Scope:** learning-journey interview questions plus the full zero-to-job-ready skill-development plan (roadmap, daily plan, free resources, datasets, mini-projects, self-check tests).

## Questions

### Q1 ⭐⭐⭐ 🟢 How did you learn SQL, and how long did it take you?
**Asked at:** commonly asked (no company-specific report found). Learning-journey questions are a standard opener in entry-level analyst interviews.
**What the interviewer is checking:** Honesty about your path, whether you practise on real problems, and whether the timeline is believable.
**Say this in the interview:** "I learned SQL by doing, not just watching. I followed a structured plan for about twelve weeks, around two hours a day: first SELECT and filters, then GROUP BY, joins, subqueries and window functions. I practised on free interactive sites and built a small HR project on my own data. I am comfortable with day-to-day analyst queries and still learning the advanced topics."
**Explain simply:**
- Give a time frame you can defend: "12 weeks at about 2 hours a day, six days a week" is the roadmap in this book (Part 12, "Skill-development plan", section A, at the end of this part). If your real timeline differs, say your real one.
- Name the order (basics, aggregates, joins, subqueries, windows) so it sounds structured, not random.
- Name one thing you built (a project) and one thing you are still weak at. Admitting a gap is safer than being caught overstating.
- "How long" is not "how good". Add one proof point: a quiz score, a mock test, a GitHub project.
**Example:** "Weeks 1-3: filtering and GROUP BY on an employee table. Weeks 4-5: joins. Weeks 6-8: CTEs and window functions. Weeks 9-12: CASE WHEN and dates, scenario queries, a mini-project and timed mock tests."
**Weak vs strong:**
- Weak: "I watched some videos and practised a bit." (no proof, no order, no time frame)
- Strong: the answer above: a time frame, an order, a project, one honest gap.
**Likely follow-ups:**
- *What was the hardest part?* See Q14.
- *Show me what you can do now.* Be ready to write a join with GROUP BY live.
**Common mistakes:** Claiming "5 years of SQL" or "advanced" when you have 3 months; saying you only watched videos; listing ten platforms you opened once.

### Q2 ⭐⭐⭐ 🟢 How would you rate yourself in SQL out of 10, and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Self-awareness. A calibrated number backed by evidence beats a high number with no proof.
**Say this in the interview:** "About 6 out of 10 for a fresher. I can write filters, GROUP BY, joins, subqueries and basic window functions like ROW_NUMBER and RANK without notes. I am slower on recursive CTEs and on query optimisation, and I am working on those. I would rather give you an honest 6 that I can prove than a 9 I cannot."
**Explain simply:**
- Rate against a visible ladder, then say which rungs you stand on:
  - 3-4: SELECT, WHERE, ORDER BY, simple GROUP BY.
  - 5-6: joins (INNER and LEFT), HAVING, subqueries, CASE WHEN, NULL handling.
  - 7: CTEs, window functions (RANK, LAG, running total), cohort-style queries.
  - 8-9: recursive CTEs, reading an execution plan, tuning, dialect differences.
- Back your number with evidence: "I scored 6 of 8 on my own joins quiz" (self-check tests in Q22).
- Never say 9 or 10 in an entry-level interview; the next question will be a hard query.
**Example:** After Week 11 of the roadmap with Quiz 6 passed (4 of 5), "6 to 7 out of 10" is defensible. After Week 5, say "5".
**Weak vs strong:**
- Weak: "10/10, I know everything." or "Maybe 2, I am just a beginner." (both unhelpful)
- Strong: a middle number, three things you can do, two things you are improving.
**Likely follow-ups:**
- *What would make it an 8?* Hard window problems, query tuning, and a year of real work data.
- *Prove it.* Offer to write a query on the spot.
**Common mistakes:** Rating yourself 9 and then freezing on a LEFT JOIN question; refusing to give a number; giving a number with no evidence.

### Q3 ⭐⭐⭐ 🟢 Which platforms have you practised SQL on?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you practised on real problems, and whether you can talk about specifics rather than just names.
**Say this in the interview:** "I started with SQLBolt and SQLZoo for the basics, used W3Schools as a syntax reference, and then moved to HackerRank SQL and DataLemur for interview-style problems. I did not just collect problems. I kept a mistakes log and redid the failed ones a day later. On DataLemur I did the free tutorial and crash course." (Only say the platforms you really used.)
**Explain simply:**
- Match the platform to the stage (details and free status in Q10):
  - Learning basics in the browser: SQLBolt, SQLZoo, W3Schools "Try it Yourself".
  - Interview-style practice: DataLemur, StrataScratch, HackerRank SQL, LeetCode Top SQL 50.
  - Your own data: SQLite or PostgreSQL on your laptop.
- Pick two or three and name something concrete from each, such as "SQLZoo's join exercises made me understand LEFT JOIN".
- Honest limits: the free status of LeetCode's list could not be verified here (the page blocked our fetch), so check what needs Premium before you plan around it. HackerRank offers account sign-up; its price was not stated on the page we read.
**Example:** "About 40 problems on SQLZoo and SQLBolt, about 100 on HackerRank, about 60 on DataLemur" is a believable split. Use your real counts.
**Weak vs strong:**
- Weak: "LeetCode, HackerRank, Codechef, everything." (a list, no detail)
- Strong: two or three platforms, what each taught you, one example problem.
**Likely follow-ups:**
- *Which problem taught you most?* Pick one with a trap (duplicates, NULLs, ties).
- *Which platform would you recommend and why?* See Q10.
**Common mistakes:** Naming a platform you only opened once; not knowing which dialect it uses; claiming a problem count you cannot back up.

### Q4 ⭐⭐⭐ 🟢 Which database or tool have you used to write SQL (MySQL, PostgreSQL, SQL Server, SQLite)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Hands-on exposure, and whether you understand that the core SQL is portable across databases.
**Say this in the interview:** "I practised mainly on SQLite because it needs no setup, and I used the same queries on browser-based editors. I know that PostgreSQL, MySQL and SQL Server differ in small things such as LIMIT versus TOP and date functions, and I keep a cheat sheet for those. I have not administered a company database, but I can adapt a query to the dialect you use."
**Explain simply:**
- A database engine is the software that stores tables and runs your queries. SQL is the language; each engine has its own dialect (small spelling differences).
- SQLite stores a whole database in one file and needs no server: the easiest start. The sample queries in this book were run on SQLite 3.45.1.
- Say only what you used. If you used only SQLite, say so and show you know the differences (Q17).
- A few differences to know: row limit is LIMIT (SQLite, PostgreSQL, MySQL), TOP (SQL Server), FETCH FIRST (standard SQL, PostgreSQL); date difference differs per engine.
**Example:** Same question, "top 3 salaries": SQLite/MySQL `LIMIT 3`, SQL Server `SELECT TOP 3`. The logic is identical.
**Weak vs strong:**
- Weak: "I use all databases." (not believable for a fresher)
- Strong: "SQLite mainly, I know where PostgreSQL/MySQL/SQL Server differ, and I can adapt."
**Likely follow-ups:**
- *Have you used a client tool?* DB Browser for SQLite is a free point-and-click viewer (open source per its site; price not stated on the page we read).
- *Which would you pick for a company?* Depends on the existing stack; PostgreSQL is free and open source.
**Common mistakes:** Claiming SQL Server experience you do not have; thinking "SQL" and "MySQL" are the same thing.

### Q5 ⭐⭐⭐ 🟢 You come from HR with no technical background. How did you learn SQL?
**Asked at:** commonly asked (no company-specific report found). Common for career-switchers; the HR background is an asset if you frame it.
**What the interviewer is checking:** Whether the switch is genuine and sustained, and whether you can translate HR knowledge into data work.
**Say this in the interview:** "In HR I worked with attrition, hiring and payroll reports in Excel, and I kept running into questions Excel handled badly, like combining several files or ranking within a department. So I taught myself SQL over about twelve weeks. I practised on my own HR-style tables, so I know the right answer to check against, and I built a small attrition project. I understand what the numbers mean, which is half the job."
**Explain simply:**
- Start from a real pain point, not "data is the future".
- Say what you did: structured plan, daily time, practice sites, one project.
- Connect to HR: attrition rate, tenure bands, time-to-hire, offer-to-join ratio, headcount by department. You already know why these matter.
- Be clear on your level: fresher in SQL, experienced in the business context.
**Example:** "I built hire, exit and department tables with 16 employees, then asked: which department has the highest attrition? (Sales, 2 of 6 = 33.3%.) Who earns more than their manager? (one person.) Seeing the answers match my manual count built my confidence."
**Weak vs strong:**
- Weak: "I have no technical background but I am a fast learner."
- Strong: the pain point, the 12-week plan, the project, the numbers, the honest gap.
**Likely follow-ups:**
- *Why leave HR?* Keep it positive: you want to work with data you currently only report on.
- *Do you need training from us?* "On your stack and data, yes; on core SQL, no."
**Common mistakes:** Apologising for your background; hiding HR experience; claiming you were an analyst when you were not.

### Q6 ⭐⭐⭐ 🟡 Walk me through a SQL project you built from start to finish.
**Asked at:** commonly asked (no company-specific report found). Project walk-throughs are reported at many companies in `interview_processes.md` (about 14 of 20 profiles mention project or resume discussion; anecdotal reports).
**What the interviewer is checking:** That you actually built something: problem, data, queries, result, limitation. They listen for your own decisions and for honesty about what you did not do.
**Say this in the interview:** "My project was an HR attrition analysis. The question was: which department loses people fastest, and does overtime or pay explain it? I built three tables (employees, departments, leave) with 16 records, wrote about ten queries, and found Sales had the highest attrition at 33.3 percent. The limitation is that it is a small practice dataset, so I treat the method as proven, not the conclusions."
**Explain simply:** Use five steps, 60 to 90 seconds in total:
- Business question: one sentence.
- Data: tables, rows, how you got them (self-made, or a public set such as IBM HR attrition from Kaggle, where login and licence were not verified).
- Method: the 2 or 3 queries that matter and why (LEFT JOIN so unassigned staff are not lost, CASE WHEN to count exits, DENSE_RANK for top earners).
- Result: one sentence with numbers.
- Limitation and next step.
**Example:** Sample data (employees table used in the project; the departments table is 10 = HR, 20 = Sales, 30 = IT):

| emp_id | name | dept_id | manager_id | hire_date | exit_date | salary | overtime |
|---|---|---|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 2019-04-01 | NULL | 90000 | N |
| 2 | Bala | 10 | 1 | 2021-06-15 | NULL | 52000 | N |
| 3 | Chitra | 10 | 1 | 2022-01-10 | 2023-09-30 | 48000 | Y |
| 4 | Dev | 20 | NULL | 2018-07-01 | NULL | 110000 | N |
| 5 | Esha | 20 | 4 | 2020-03-05 | NULL | 60000 | Y |
| 6 | Farhan | 20 | 4 | 2021-08-20 | 2024-02-29 | 58000 | Y |
| 7 | Gita | 20 | 4 | 2023-02-01 | NULL | 57000 | N |
| 8 | Hari | 20 | 4 | 2023-05-15 | 2024-06-30 | 59000 | Y |
| 9 | Isha | 30 | NULL | 2017-11-01 | NULL | 130000 | N |
| 10 | Jai | 30 | 9 | 2020-09-14 | NULL | 95000 | Y |
| 11 | Kiran | 30 | 9 | 2021-01-25 | NULL | 95000 | N |
| 12 | Lata | 30 | 9 | 2022-07-11 | 2025-01-31 | 88000 | Y |
| 13 | Manoj | 30 | 9 | 2024-03-04 | NULL | 72000 | N |
| 14 | Neha | 20 | 4 | 2024-01-08 | NULL | 112000 | N |
| 15 | Om | 10 | 1 | 2024-07-01 | NULL | 45000 | N |
| 16 | Pooja | NULL | 1 | 2024-09-01 | NULL | 50000 | N |

**SQL:** Attrition rate by department.
```sql
SELECT COALESCE(d.dept_name,'Unassigned') AS dept,
       COUNT(*) AS people_ever,
       SUM(CASE WHEN e.exit_date IS NOT NULL THEN 1 ELSE 0 END) AS exits,
       ROUND(100.0*SUM(CASE WHEN e.exit_date IS NOT NULL THEN 1 ELSE 0 END)/COUNT(*),1) AS attrition_pct
FROM employees e
LEFT JOIN departments d ON d.dept_id = e.dept_id
GROUP BY COALESCE(d.dept_name,'Unassigned')
ORDER BY attrition_pct DESC, dept;
```
**Output:**

| dept | people_ever | exits | attrition_pct |
|---|---|---|---|
| Sales | 6 | 2 | 33.3 |
| HR | 4 | 1 | 25.0 |
| IT | 5 | 1 | 20.0 |
| Unassigned | 1 | 0 | 0.0 |

**pandas equivalent:**
```python
emp = pd.read_sql_query("SELECT * FROM employees", c)
dep = pd.read_sql_query("SELECT * FROM departments", c)
m = emp.merge(dep, on="dept_id", how="left")
m["dept"] = m["dept_name"].fillna("Unassigned")
m["left"] = m["exit_date"].notna().astype(int)
g = m.groupby("dept").agg(people_ever=("emp_id","count"), exits=("left","sum")).reset_index()
g["attrition_pct"] = (100.0*g["exits"]/g["people_ever"]).round(1)
result = g.sort_values(["attrition_pct","dept"], ascending=[False,True]).reset_index(drop=True)
```
**Output:**

| dept | people_ever | exits | attrition_pct |
|---|---|---|---|
| Sales | 6 | 2 | 33.3 |
| HR | 4 | 1 | 25.0 |
| IT | 5 | 1 | 20.0 |
| Unassigned | 1 | 0 | 0.0 |

**SQL:** Top 3 salary levels per department among current staff (ties share a rank).
```sql
WITH ranked AS (
  SELECT d.dept_name, e.name, e.salary,
         DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS rnk
  FROM employees e
  JOIN departments d ON d.dept_id = e.dept_id
  WHERE e.exit_date IS NULL
)
SELECT dept_name, name, salary, rnk FROM ranked WHERE rnk <= 3 ORDER BY dept_name, rnk, name;
```
**Output:**

| dept_name | name | salary | rnk |
|---|---|---|---|
| HR | Asha | 90000 | 1 |
| HR | Bala | 52000 | 2 |
| HR | Om | 45000 | 3 |
| IT | Isha | 130000 | 1 |
| IT | Jai | 95000 | 2 |
| IT | Kiran | 95000 | 2 |
| IT | Manoj | 72000 | 3 |
| Sales | Neha | 112000 | 1 |
| Sales | Dev | 110000 | 2 |
| Sales | Esha | 60000 | 3 |

**Edge cases:** Pooja has no department. An INNER JOIN would silently drop her, so the LEFT JOIN plus COALESCE keeps her visible as "Unassigned". Jai and Kiran tie at 95,000, so DENSE_RANK shows both at level 2 and the IT list has four rows. Attrition here is exits divided by everyone who ever joined; if the interviewer wants a time-window rate (exits in a year divided by average headcount), say that definition out loud first.
**Likely follow-ups:**
- *Why LEFT JOIN?* To keep employees whose department is missing.
- *What would you do with real data?* Check duplicates and dates first (Part 10).
- *What would you recommend?* Investigate Sales exits by manager and overtime, with a note that 6 people is too few to conclude.
**Common mistakes:** Describing tools instead of questions; no numbers; presenting practice data as real company findings; being unable to explain one of your own joins.

### Q7 ⭐⭐⭐ 🟡 How much SQL practice do you do daily, and roughly how many problems have you solved?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Consistency and a believable volume. Whether your number matches your timeline.
**Say this in the interview:** "I practised about two hours a day, six days a week: thirty minutes learning, thirty guided practice, forty minutes on three to five problems, and twenty reviewing a mistakes log. Over twelve weeks that came to roughly 260 practice queries plus two timed mock tests, and I redid every failed one." (Use your own number.)
**Explain simply:**
- Daily plan (from section B of the skill plan): Learn 30 min, Guided practice 30, Problem solving 40, Review 20 = 120 min. With 1 hour: halve each block, never skip Review.
- The week-by-week problem targets in the roadmap add up as: 25+30+30+25+20+25+25+20+30+15+15 = 260 for weeks 1-11 (checked by running the sum), plus mocks in week 12.
- Quality over count: 150 problems you reviewed beat 500 you copied.
- Only quote a number you can back with a log or platform history.
**Example:** "Around 260 queries over 12 weeks, of which about 40 were hard, and I can explain any of them."
**Weak vs strong:**
- Weak: "500+ problems" with no detail (interviewers pick one and ask you to explain it).
- Strong: a modest number, a daily routine, a mistakes log, one problem you can walk through.
**Likely follow-ups:**
- *Which problem do you remember best?* Pick one with ties or NULLs.
- *Are you still practising?* Yes: a few problems a day on DataLemur or StrataScratch (free sign-up and SQL path stated free; other features may be paid).
**Common mistakes:** Inflating counts; counting reading as solving; saying "daily" without a routine; no review loop.

### Q8 ⭐⭐⭐ 🟡 In what order did you study SQL topics, and why that order?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you learned in a logical order and understand how topics build on each other.
**Say this in the interview:** "I went from simple to composed. First SELECT and filters, because everything else uses them. Then aggregates and GROUP BY, then joins, because real data lives in several tables. Then subqueries and CTEs, then window functions, then CASE WHEN and date handling, and finally business scenarios, retention and hard patterns. Each step used the previous one, so I never learned a topic without its prerequisite."
**Explain simply:**
- The order used in this book, with the reason:
  - Part 1 SELECT/WHERE/ORDER BY/DISTINCT/LIMIT: reading and filtering one table.
  - Part 2 Aggregates, GROUP BY, HAVING: summarising (headcount by department).
  - Part 3 Joins: combining tables; the biggest source of wrong answers.
  - Part 4 Subqueries and CTEs: breaking a problem into named steps.
  - Part 5-6 Window functions: ranking, running totals, LAG/LEAD; need GROUP BY and CTE understanding.
  - Part 7 CASE WHEN, NULLs, strings, dates: cleaning and bucketing. NULLs get a light intro in week 2 because they break early queries.
  - Part 8 Scenarios: sales, HR, e-commerce, banking; practise reading a brief.
  - Parts 9-10 Cohorts, funnels, de-duplication, nth highest, gaps and islands, recursive CTE, optimisation: hard patterns that startups ask.
  - Part 11 Database concepts (keys, indexes, views, ACID): read lightly in week 1, revisit in week 12.
**Example:** You cannot do "top 3 earners per department" (Part 5) without GROUP BY thinking (Part 2) and a CTE (Part 4).
**Weak vs strong:**
- Weak: "I learned whatever came up on YouTube."
- Strong: the order, with a one-line reason for each step.
**Likely follow-ups:**
- *Would you change the order?* Maybe move CASE WHEN earlier; it is useful from week 3.
- *Why not window functions first?* They need grouping and subquery ideas.
**Common mistakes:** Jumping to window functions before joins; skipping NULL handling; studying database theory first and never typing a query.

### Q9 ⭐⭐ 🟢 How do you stay current with SQL and data skills?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Ongoing curiosity, and that you do not stop learning after getting the job.
**Say this in the interview:** "I keep a small routine: a few practice problems a week on DataLemur or StrataScratch, a monthly retake of my own timed test, and I read the official PostgreSQL documentation when I meet something new. For example, the PostgreSQL docs note that version 18 added skip scan for multi-column indexes. I also check what the jobs I want ask for, since SQL appears in about half of the postings I sampled."
**Explain simply:**
- Practice: one timed set per week; log mistakes.
- Documentation: official docs are the most reliable source (PostgreSQL docs, SQLite docs). They state exact behaviour such as the order of columns in an index.
- Market check: in a pooled sample of 186 India analyst job descriptions (non-random, about plus or minus 7 points), SQL appeared in 54%, dashboards/reporting 75%, Excel 60%, communication 73%, Power BI 40%, Python 32%. So SQL stays alongside Excel and BI.
- Only claim sources you actually follow. Not verified in this book: any YouTube channel, newsletter or course catalogue.
**Example:** "Every Sunday I redo three failed problems from my mistakes log, and every month I retake a 45-minute mock."
**Weak vs strong:**
- Weak: "I read blogs and watch videos." (vague)
- Strong: a concrete weekly routine and one specific recent thing you learned.
**Likely follow-ups:**
- *Latest thing you learned?* Have one ready (for example the difference between RANK and DENSE_RANK with ties).
- *Do you follow AI tools for SQL?* See Q18.
**Common mistakes:** Naming sources you do not read; no routine; claiming you track every new database release.

### Q10 ⭐⭐ 🟢 Which free resources would you recommend to a SQL beginner?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the learning landscape and can advise honestly, including about cost.
**Say this in the interview:** "For a pure beginner I would start with SQLBolt or SQLZoo for short interactive lessons, keep W3Schools as a syntax reference, and move to DataLemur or StrataScratch for interview-style problems. I would tell them to check what is free on each site, because several have paid tiers."
**Explain simply:** Resources checked on 2026-10-21 (what the page itself stated; "price unverified" means do not assume it is free):
| Resource | Use it for | Free status as observed |
|---|---|---|
| SQLBolt (sqlbolt.com) | Short in-browser lessons, weeks 1-3 | Page loaded, no sign-up to read; price unverified (widely known free) |
| W3Schools SQL (w3schools.com/sql/) | Syntax reference, "Try it Yourself" editor | Free (stated) |
| SQLZoo (sqlzoo.net) | Step-by-step exercises, good for joins | Free (stated) |
| Mode SQL Tutorial, now at thoughtspot.com/sql-tutorial | Analyst-style tutorial | Price/login unverified |
| DataLemur (datalemur.com) | Interview-style questions, free tutorial, 9-day crash course | Tutorial and crash course stated free; a Premium tier exists; which questions are locked unverified |
| StrataScratch (stratascratch.com) | Interview questions, "Comprehensive SQL" path | "Start coding free, no credit card"; SQL path stated free; other features may be paid |
| HackerRank SQL (hackerrank.com/domains/sql) | Easy/Medium/Hard challenges like online assessments | Account sign-up offered; price unverified |
| LeetCode Top SQL 50 (leetcode.com/studyplan/top-sql-50/) | Popular practice list | UNVERIFIED: page returned HTTP 403 to our fetch; price unverified, check Premium yourself |
| SQLite (sqlite.org/download.html) | Zero-setup local database | Licence page linked; public-domain status unverified on that page |
| DB Browser for SQLite (sqlitebrowser.org) | Point-and-click viewer | Open source (stated); price not stated |
| PostgreSQL (postgresql.org/download/) | Full database used by many companies | Free, open source (stated) |
| SQL Online IDE (sqliteonline.com) | Run SQL in the browser, no install | Has a Pricing page; free-tier limits unverified |
| DuckDB (duckdb.org/docs/) | Local analytics SQL over CSV | Docs loaded; price/open-source status not confirmed on the page fetched; not used in this book's runs |

Not verified and not recommended here by name: any YouTube channel, Kaggle Learn, GeeksforGeeks, Coursera, Udemy.
**Example:** A beginner path: SQLBolt (weeks 1-3), SQLZoo joins (weeks 4-5), DataLemur crash course and free questions (weeks 6-9), HackerRank for timed practice (weeks 10-12).
**Weak vs strong:**
- Weak: "Just watch YouTube."
- Strong: a staged path with honest notes on what costs money.
**Likely follow-ups:**
- *Which is best for interviews?* Interview-style sites (DataLemur, StrataScratch, HackerRank), after the basics.
- *Is a paid course needed?* No evidence in this book that one is required; certifications were not required in any sampled job description (Q19).
**Common mistakes:** Calling every site "free" without checking; collecting resources instead of finishing one; never typing queries yourself.

### Q11 ⭐⭐ 🟢 Which practice datasets have you worked with?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you worked with realistic, multi-table data or only toy examples.
**Say this in the interview:** "I used self-made HR tables where I know the right answer, then public databases: Chinook, a music store with customers, invoices and tracks, and Northwind, a classic trading company database. For HR analysis I looked at the IBM HR attrition dataset on Kaggle." (Say only what you loaded and queried.)
**Explain simply:**
| Dataset | What it is | Good for | Notes |
|---|---|---|---|
| Chinook (github.com/lerocha/chinook-database) | Digital media store: artists, albums, tracks, invoices, customers, employees; scripts for SQLite, PostgreSQL, MySQL, SQL Server | Joins, GROUP BY, window functions | Licence file not read; data fictitious |
| Northwind SQLite3 port (github.com/jpwhite3/northwind-SQLite3) | Trading company: orders, products, customers, employees | Joins, subqueries, business reports | MIT licence (stated) |
| AdventureWorks (github.com/microsoft/sql-server-samples, adventureworks release) | Microsoft sample company, OLTP/LT/DW versions | Larger multi-table practice | Needs SQL Server to restore; heavier setup; free to download |
| IBM HR Analytics Attrition (Kaggle) | HR attrition and performance, single table | HR projects, GROUP BY, CASE WHEN | Page title only seen; Kaggle login and licence unverified; load the CSV into SQLite |
| Self-made HR tables | employees, departments, attendance, hires, exits (50 to 200 rows) | Anything; you know the right answer | Build with CREATE TABLE/INSERT or a CSV from Excel |

- Why self-made data matters: you can compute the answer by hand and compare (Q15).
- The 16-row employees table used across this book's Part 12 answers is one example (see Q6).
**Example:** Chinook question: "Which country brings the most invoice revenue?" needs customers joined to invoices, then GROUP BY country.
**Weak vs strong:**
- Weak: "I used some Kaggle data."
- Strong: dataset name, tables used, one question answered, one data problem found.
**Likely follow-ups:**
- *Biggest table you worked with?* Be honest; practice sets are small. Say you understand scale issues (indexes, Part 10-11).
- *How did you load it?* Q12 and Q21.
**Common mistakes:** Naming datasets you only downloaded; using a single flat table and calling it a database; ignoring licences.

### Q12 ⭐⭐ 🟢 How would you set up a free SQL practice environment on your own laptop?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Practical initiative: can you get from zero to a working query without help or cost?
**Say this in the interview:** "The fastest free setup is SQLite, which needs no server. I would install DB Browser for SQLite to see tables, create a database file, import a CSV, and run queries. If I need a full database, I would install PostgreSQL, which is free and open source. If I cannot install anything, there are browser tools such as SQL Online IDE, though I would check its free limits."
**Explain simply:**
- Option 1, no install at all: browser editors (W3Schools "Try it Yourself", SQL Online IDE; free-tier limits of the latter unverified).
- Option 2, easiest local: SQLite. One file is the whole database. Python already includes it: `import sqlite3`.
- Option 3, point-and-click: DB Browser for SQLite (open source per its site; price not stated).
- Option 4, industry-style: PostgreSQL from postgresql.org/download (free).
- Steps for options 2/3: create a database, create tables (CREATE TABLE), add rows (INSERT, or import a CSV), run SELECT, save the file.
- Keep your practice database in a folder with your `.sql` files so you can re-run everything.
**Example:** (run here) Check the engine from Python; the same SQL works in DB Browser's "Execute SQL" tab:
```sql
SELECT sqlite_version() AS sqlite_version;
```
**Output:**

| sqlite_version |
|---|
| 3.45.1 |

**Python skeleton to start (standard library; this exact pattern was run here):**
```python
import sqlite3
conn = sqlite3.connect("practice.db")   # creates the file if missing
conn.executescript("CREATE TABLE IF NOT EXISTS t(id INTEGER, name TEXT); INSERT INTO t VALUES (1,'Asha');")
print(conn.execute("SELECT * FROM t").fetchall())
conn.commit()
```
Command-line shortcut (SQLite shell `.import file.csv table`): standard usage, not run here.
**Edge cases:** SQLite is forgiving about data types and has no real DATE type (dates are text), so a query that works in SQLite may need a cast in PostgreSQL or SQL Server. DuckDB is not installed in this book's environment and was not used.
**Likely follow-ups:**
- *Why not install a big database first?* Setup friction kills motivation; learn SQL first.
- *How do you load an Excel file?* Save as CSV, import it (see Q21 for a Python route).
**Common mistakes:** Spending weeks on installation; installing five tools; forgetting to commit changes; saving the database file in a temporary folder.

### Q13 ⭐⭐ 🟢 What HR questions can SQL answer that Excel struggles with?
**Asked at:** commonly asked (no company-specific report found). Especially natural for HR-to-analytics switchers.
**What the interviewer is checking:** That you understand why SQL exists and can name concrete cases, not just "SQL is faster".
**Say this in the interview:** "Excel is great for one table I can eyeball. SQL is better when the question needs several tables at once, millions of rows, or something repeatable. In HR: who earns more than their manager, who has no leave record, top three earners in each department, attrition by tenure band across years. In Excel those need lookups and helper columns; in SQL it is a few lines I can rerun when the data changes."
**Explain simply:**
- Combining tables: employees + departments + leave = a join, not VLOOKUP chains.
- "Rows that have no match": employees with no leave record, applicants with no interview: an anti-join (LEFT JOIN, then keep the NULLs).
- Ranking within groups: top 3 per department needs window functions; in Excel it is a messy array formula.
- Self-comparison: employee against their own manager's row in the same table.
- Scale and repeatability: databases hold more rows than a spreadsheet comfortably handles; a saved query reruns on fresh data with no manual steps. Excel still wins for quick one-off checks and charts.
**Example:** Employees table:

| emp_id | name | dept_id | manager_id | hire_date | exit_date | salary | overtime |
|---|---|---|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 2019-04-01 | NULL | 90000 | N |
| 2 | Bala | 10 | 1 | 2021-06-15 | NULL | 52000 | N |
| 3 | Chitra | 10 | 1 | 2022-01-10 | 2023-09-30 | 48000 | Y |
| 4 | Dev | 20 | NULL | 2018-07-01 | NULL | 110000 | N |
| 5 | Esha | 20 | 4 | 2020-03-05 | NULL | 60000 | Y |
| 6 | Farhan | 20 | 4 | 2021-08-20 | 2024-02-29 | 58000 | Y |
| 7 | Gita | 20 | 4 | 2023-02-01 | NULL | 57000 | N |
| 8 | Hari | 20 | 4 | 2023-05-15 | 2024-06-30 | 59000 | Y |
| 9 | Isha | 30 | NULL | 2017-11-01 | NULL | 130000 | N |
| 10 | Jai | 30 | 9 | 2020-09-14 | NULL | 95000 | Y |
| 11 | Kiran | 30 | 9 | 2021-01-25 | NULL | 95000 | N |
| 12 | Lata | 30 | 9 | 2022-07-11 | 2025-01-31 | 88000 | Y |
| 13 | Manoj | 30 | 9 | 2024-03-04 | NULL | 72000 | N |
| 14 | Neha | 20 | 4 | 2024-01-08 | NULL | 112000 | N |
| 15 | Om | 10 | 1 | 2024-07-01 | NULL | 45000 | N |
| 16 | Pooja | NULL | 1 | 2024-09-01 | NULL | 50000 | N |

**SQL:** Who earns more than their manager (self join: the same table used twice).
```sql
SELECT e.name AS employee, e.salary, m.name AS manager, m.salary AS manager_salary
FROM employees e
JOIN employees m ON m.emp_id = e.manager_id
WHERE e.salary > m.salary;
```
**Output:**

| employee | salary | manager | manager_salary |
|---|---|---|---|
| Neha | 112000 | Dev | 110000 |

**pandas equivalent:**
```python
emp = pd.read_sql_query("SELECT * FROM employees", c)
j = emp.merge(emp, left_on="manager_id", right_on="emp_id", suffixes=("","_m"))
result = (j[j["salary"] > j["salary_m"]][["name","salary","name_m","salary_m"]]
          .rename(columns={"name":"employee","name_m":"manager","salary_m":"manager_salary"})
          .reset_index(drop=True))
```
**Output:**

| employee | salary | manager | manager_salary |
|---|---|---|---|
| Neha | 112000 | Dev | 110000 |

**SQL:** Current employees with no leave in 2026 (LEFT JOIN anti-join). Uses the 9-row `leave_log (emp_id, leave_date)` table from the Q22 kit: employees 2, 5, 10 and 11 have 2026 leave; employee 3 has one 2023 row.
```sql
SELECT e.name, e.dept_id
FROM employees e
LEFT JOIN leave_log l ON l.emp_id = e.emp_id AND l.leave_date >= '2026-01-01'
WHERE l.emp_id IS NULL AND e.exit_date IS NULL
ORDER BY e.name;
```
**Output:**

| name | dept_id |
|---|---|
| Asha | 10 |
| Dev | 20 |
| Gita | 20 |
| Isha | 30 |
| Manoj | 30 |
| Neha | 20 |
| Om | 10 |
| Pooja | NULL |

**Edge cases:** Put the date filter in the ON clause, not WHERE; in WHERE it would turn the LEFT JOIN into an inner join. Pooja (no department) is still returned because the query never touches departments. Employees with no manager (NULL manager_id) drop out of the self join, which is correct here.
**Likely follow-ups:**
- *Can Excel do it?* Yes with Power Query or formulas, but it is slower to build and harder to audit at scale.
- *When would you still use Excel?* Small data, ad-hoc checks, formatting for stakeholders.
**Common mistakes:** Saying Excel "cannot" do things; picking examples with no HR context; filtering the right-hand table in WHERE after a LEFT JOIN.

### Q14 ⭐⭐ 🟡 Which SQL topic did you find hardest, and how did you overcome it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Honest self-reflection and a real learning method, not a polished answer. Pick a topic you genuinely struggled with.
**Say this in the interview:** "Window functions, because ROW_NUMBER, RANK and DENSE_RANK look similar and I mixed them up when ties appeared. I overcame it by making a tiny table with a deliberate tie, writing all three side by side, and predicting the output before running it. After that, top-N per group stopped being scary." (If your hardest topic was joins or HAVING, say that and use the same method.)
**Explain simply:**
- Method that works for any topic: tiny data with a trap, predict, run, compare, write one sentence rule.
- The three ranking functions differ only on ties:
  - ROW_NUMBER: always 1,2,3,4. Ties broken arbitrarily unless you add a second sort key.
  - RANK: tied rows share a number, then it skips (1,2,2,4).
  - DENSE_RANK: tied rows share a number, no skip (1,2,2,3).
- "Window" = a calculation over a set of related rows without collapsing them (unlike GROUP BY).
**Example:** IT department, current staff, Jai and Kiran tied at 95,000:
**SQL:**
```sql
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
       RANK()       OVER (ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk
FROM employees
WHERE dept_id = 30 AND exit_date IS NULL
ORDER BY salary DESC, name;
```
**Output:**

| name | salary | row_num | rnk | dense_rnk |
|---|---|---|---|---|
| Isha | 130000 | 1 | 1 | 1 |
| Jai | 95000 | 2 | 2 | 2 |
| Kiran | 95000 | 3 | 2 | 2 |
| Manoj | 72000 | 4 | 4 | 3 |

**pandas equivalent:**
```python
emp = pd.read_sql_query("SELECT name, salary FROM employees WHERE dept_id=30 AND exit_date IS NULL", c)
emp = emp.sort_values(["salary","name"], ascending=[False,True]).reset_index(drop=True)
emp["row_num"] = range(1, len(emp)+1)
emp["rnk"] = emp["salary"].rank(method="min", ascending=False).astype(int)
emp["dense_rnk"] = emp["salary"].rank(method="dense", ascending=False).astype(int)
result = emp
```
**Output:**

| name | salary | row_num | rnk | dense_rnk |
|---|---|---|---|---|
| Isha | 130000 | 1 | 1 | 1 |
| Jai | 95000 | 2 | 2 | 2 |
| Kiran | 95000 | 3 | 2 | 2 |
| Manoj | 72000 | 4 | 4 | 3 |

**Edge cases:** For ROW_NUMBER, tied rows get an arbitrary order; add a tie-breaker such as emp_id if the result must be repeatable. Use DENSE_RANK for "Nth highest salary" so ties do not hide a level.
**Weak vs strong:**
- Weak: "Nothing was hard, I learned fast." (not credible)
- Strong: a named topic, the specific confusion, the method that fixed it, and proof (a quiz result).
**Likely follow-ups:**
- *Another topic still hard?* Recursive CTEs or query tuning; say what you are doing about it.
- *Which would you use for top 3 per department?* DENSE_RANK or ROW_NUMBER depending on whether ties should all be kept; ask the interviewer.
**Common mistakes:** Saying "RANK and DENSE_RANK are the same"; forgetting PARTITION BY; picking a topic you cannot explain.

### Q15 ⭐⭐ 🟡 How do you check that your own SQL answer is correct when no answer key exists?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you test your own work. Wrong-but-plausible numbers are the real danger in analytics.
**Say this in the interview:** "I never trust a query because it runs. I check it against a control total from the base table, run the same question a second way, test on a tiny table where I can compute the answer by hand, and look for the usual traps: duplicates after a join, NULLs, and ties."
**Explain simply:** Five checks:
- Control total: row count and sum from the base table before and after joins.
- Two methods: the same answer via JOIN and via EXISTS, or SQL versus a quick Excel/pandas calculation.
- Hand-check: pick two or three rows and calculate manually.
- Trap list: join duplicates, NULL in filters or joins, ties in ranking, inclusive versus exclusive date ranges, a LEFT JOIN turned into an inner join by a WHERE condition.
- Sanity: do percentages sum to about 100? Is the result plausible for the business?
**Example:** (run on the 16-employee table from Q6 and the 9-row `leave_log` table in the Q22 kit) A join to the leave table inflates and drops rows.
**SQL:**
```sql
-- WRONG: joining to leave_log repeats an employee once per leave day
SELECT SUM(e.salary) AS payroll_after_join
FROM employees e
JOIN leave_log l ON l.emp_id = e.emp_id;
```
**Output:**

| payroll_after_join |
|---|
| 617000 |

```sql
-- Control total straight from the base table
SELECT SUM(salary) AS payroll_true, COUNT(*) AS headcount FROM employees;
```
**Output:**

| payroll_true | headcount |
|---|---|
| 1221000 | 16 |

Real payroll is 1,221,000 for 16 people, but the join gave 617,000. The mismatch is the alarm: employees with several leave days are counted repeatedly, and those with none disappear. Fix: aggregate the leave table first, or use EXISTS.
**SQL:** Cross-check using two methods.
```sql
-- Same question, two methods: employees who ever took leave
SELECT (SELECT COUNT(DISTINCT e.emp_id) FROM employees e JOIN leave_log l ON l.emp_id=e.emp_id) AS method_join,
       (SELECT COUNT(*) FROM employees e WHERE EXISTS (SELECT 1 FROM leave_log l WHERE l.emp_id=e.emp_id)) AS method_exists;
```
**Output:**

| method_join | method_exists |
|---|---|
| 5 | 5 |

Both methods give 5 employees who ever took leave. Agreement raises confidence.
**Edge cases:** If a check disagrees, find the exact rows that differ (EXCEPT, or a LEFT JOIN anti-join between the two results) rather than guessing. Immature (recent) periods in cohort work often look like drops; confirm the boundary rule ("> 30" versus ">= 30") with the person who asked.
**Likely follow-ups:**
- *What if the data owner has no answer key?* Reconcile to a finance or HR report total.
- *Do you use tests in production?* Saved checks that run with the query, such as row-count assertions.
**Common mistakes:** Stopping when the query runs; not comparing totals; testing only on big data; trusting an AI-generated query unchecked (Q18).

### Q16 ⭐⭐ 🟡 How would you prepare for a live SQL round in two weeks?
**Asked at:** commonly asked (no company-specific report found). Reports in `interview_processes.md` mention live SQL screens (for example a shared-screen SQL screen in one Amazon BA report and an all-SQL manager round in one PhonePe report). Each is a single or anecdotal report; difficulty ranges from basic-medium at service MNCs to medium-hard at startups.
**What the interviewer is checking:** Whether you can prepare in a structured way under time pressure and prioritise what matters.
**Say this in the interview:** "I would spend two weeks on the topics that appear most: joins, GROUP BY with HAVING, nth highest with DENSE_RANK, top N per group, de-duplication and one cohort or running-total pattern. Each day I would do timed problems out loud, review my errors, and finish with two full mock rounds. I would also prepare a three-minute project walkthrough."
**Explain simply:** 14-day plan, 2 hours a day (assumes you already know basic SELECT; if not, follow the 12-week roadmap in the skill plan):
| Days | Focus | Book 2 | Output |
|---|---|---|---|
| 1-2 | Filters, aggregates, HAVING, NULLs | Parts 1-2, 7 | 20 queries; Quiz T1-T3 from Q22 |
| 3-4 | Joins: INNER, LEFT, self; join traps | Part 3 | 20 queries; explain each aloud |
| 5-6 | Subqueries, CTEs, ROW_NUMBER/RANK/DENSE_RANK, top N per group | Parts 4-5 | 20 queries; T5-T6 |
| 7 | Mock round 1: 5 questions, 45 minutes, speak aloud | any | Score and error log |
| 8-9 | LAG/LEAD, running totals, CASE WHEN, dates | Parts 6-7 | 15 queries; T8 |
| 10-11 | Scenarios, nth highest, de-duplication, one cohort/funnel | Parts 8-10 | 12 queries; explain aloud |
| 12 | Mock round 2 on a new dataset | any | Score and error log |
| 13 | Fix the top 5 recurring mistakes; revise dialect cheat sheet (Q17); project walkthrough | Parts 10-11 | 3-minute project speech |
| 14 | Light revision, sleep, set up the tool you will use | - | - |

**Example:** If the company's profile points to basic-medium SQL (service MNC reports), spend less time on recursive CTEs and more on joins and window basics. If it is a startup, add hard window and cohort patterns.
**Edge cases:** If you have only 3 or 4 days, do joins, GROUP BY/HAVING, DENSE_RANK, and one project story. Do not start new topics the day before.
**Likely follow-ups:**
- *What if you do not know the dialect?* Q17.
- *Do you practise speaking?* Yes: explaining each query aloud is part of the test.
**Common mistakes:** Solving new problems nonstop without reviewing mistakes; practising silently; ignoring NULLs and ties; skipping mock rounds.

### Q17 ⭐⭐ 🟡 The interview uses a different SQL dialect from the one you practised. How do you cope?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Adaptability. The core logic is the same; they want to see that you know where dialects differ and can say so.
**Say this in the interview:** "The logic of SELECT, JOIN, GROUP BY and window functions is the same everywhere. What changes is small syntax: row limits, date functions, string joining. I would say which dialect I am used to, write the logic first, and ask if the editor lets me look up the function name. If I forget, I would explain the idea and name what I would check in the docs."
**Explain simply:** Differences to know (SQLite version run here; others from general knowledge, not run here):
| Task | SQLite (run here) | PostgreSQL | MySQL | SQL Server |
|---|---|---|---|---|
| First 3 rows | `LIMIT 3` | `LIMIT 3` or `FETCH FIRST 3 ROWS ONLY` | `LIMIT 3` | `SELECT TOP 3 ...` |
| Days between dates | `julianday(b) - julianday(a)` | `b::date - a::date` (date minus date gives days) | `DATEDIFF(b, a)` | `DATEDIFF(day, a, b)` |
| Join text | `a \|\| b` | `a \|\| b` | `CONCAT(a, b)` | `a + b` or `CONCAT(a, b)` |
| Current date | `date('now')` | `CURRENT_DATE` | `CURDATE()` | `GETDATE()` |

**Example:** You practised on SQLite and the test editor is SQL Server. Write the logic first, then translate only the dialect parts: `LIMIT 3` becomes `TOP 3`, and `julianday(b) - julianday(a)` becomes `DATEDIFF(day, a, b)`. The answer is the same: Isha, 130000, 3255 days (SQLite run below).
**SQL (run on SQLite, as practised):**
```sql
SELECT name, salary,
       CAST(julianday('2026-09-30') - julianday(hire_date) AS INTEGER) AS tenure_days
FROM employees
WHERE exit_date IS NULL
ORDER BY salary DESC
LIMIT 3;
```
**Output:**

| name | salary | tenure_days |
|---|---|---|
| Isha | 130000 | 3255 |
| Neha | 112000 | 996 |
| Dev | 110000 | 3013 |

Alternatives, not run here:
```sql
-- SQL Server
SELECT TOP 3 name, salary, DATEDIFF(day, hire_date, '2026-09-30') AS tenure_days
FROM employees WHERE exit_date IS NULL ORDER BY salary DESC;
-- MySQL
SELECT name, salary, DATEDIFF('2026-09-30', hire_date) AS tenure_days
FROM employees WHERE exit_date IS NULL ORDER BY salary DESC LIMIT 3;
```
**Edge cases:** Integer division truncates in SQLite and PostgreSQL (from memory, other engines may differ); use `100.0 *` or a cast. Window functions need SQLite 3.25 or later (this book ran 3.45.1) and are available in current PostgreSQL, MySQL 8 and SQL Server (from memory).
**Likely follow-ups:**
- *Which dialect do you prefer?* The one the team uses; say you are fastest in SQLite.
- *Can you do it without window functions?* Yes, with a correlated subquery, slower and harder to read.
**Common mistakes:** Panicking; claiming you "do not know SQL" outside one dialect; silently using TOP in MySQL and not noticing the error.

### Q18 ⭐⭐ 🟡 How do you use AI assistants to learn SQL without depending on them?
**Asked at:** commonly asked (no company-specific report found). A newer question; no company-specific report found.
**What the interviewer is checking:** That you use AI as a tutor and checker, not as a crutch, and that you verify output.
**Say this in the interview:** "I use AI to explain errors, to give me practice questions, and to review a query I wrote myself. I never paste its answer without running it on a small table where I know the result. The rule is: I attempt first, then ask, then I explain the answer back in my own words. In interviews I will not have it, so I practise without it."
**Explain simply:**
- Good uses: explain an error message; "give me 5 join problems on an HR schema"; "review my query for NULL and duplicate issues"; compare two approaches.
- Bad uses: pasting the question and copying the answer; trusting syntax for a dialect you did not name.
- Safeguards: build a tiny test table; compute the expected answer by hand; run; compare (Q15).
- Timed practice and mock tests are AI-free.
**Example:** (run) A quick answer to "third highest salary in IT" looks right but fails when salaries tie. The employees table (IT: 130,000; 95,000; 95,000; 88,000; 72,000 across all IT staff):
**SQL:**
```sql
-- Typical quick answer: third highest salary in IT using LIMIT/OFFSET
SELECT salary FROM employees WHERE dept_id = 30 ORDER BY salary DESC LIMIT 1 OFFSET 2;
```
**Output:**

| salary |
|---|
| 95000 |

```sql
-- Checked answer: DENSE_RANK treats equal salaries as one level
SELECT DISTINCT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS lvl
  FROM employees WHERE dept_id = 30
) WHERE lvl = 3;
```
**Output:**

| salary |
|---|
| 88000 |

LIMIT/OFFSET returned 95,000 (the second tied row). The correct third distinct salary is 88,000. A tiny test with a tie catches it.
**Edge cases:** Ties, NULLs, and a department with fewer than 3 salaries (the second query returns no row; decide what the business wants, e.g. NULL).
**Weak vs strong:**
- Weak: "I just ask ChatGPT for the query."
- Strong: attempt first, AI for explanation and review, verify by running, practise without it.
**Likely follow-ups:**
- *Would you use AI at work?* Yes with company-approved tools, no confidential data, and always verified.
- *What did AI get wrong for you?* Have one real example ready.
**Common mistakes:** Copying without understanding; pasting private employee data into a public tool; assuming code that runs is correct.

### Q19 ⭐ 🟢 Do SQL certifications help, and have you done any?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you value proof of skill over paper, and whether you are honest about what you hold.
**Say this in the interview:** "I have not taken a SQL certificate, and I chose to spend that time building projects and timed practice, because I can show those. In the job postings I looked at, no certification was required; a few listed Tableau or Power BI certificates or the Google Data Analytics certificate as an advantage. If a certificate helped me get through a screening filter, I would consider one, but I would still prove skill with a live query."
**Explain simply:**
- Evidence from this book's research: in a pooled sample of 186 India analyst job descriptions (non-random), no analytics certification was required in any sample. Certifications appeared only as advantages: Tableau/Power BI certificate, Google Data Analytics, Microsoft Data Analyst Associate, CBAP. A SQL-specific certificate was not named in what we recorded.
- Interviews test SQL by having you write queries, so skill beats certificate.
- A certificate is useful for structure and discipline, or when you have no projects yet. Check price before enrolling; course prices were not verified in this book (Coursera and Udemy not checked).
- If you hold one, say what it taught and one thing you built after it.
**Example:** "A project on GitHub with ten queries and a README shows more than a course completion email."
**Weak vs strong:**
- Weak: "Yes, I have five certificates" and cannot answer a join question.
- Strong: honest answer, reasons, evidence of skill through projects and timed tests.
**Likely follow-ups:**
- *Would you do one if we asked?* Yes, I learn quickly and the company knows its stack best.
- *Which?* One tied to your target stack (for example Power BI) rather than random.
**Common mistakes:** Lying about certificates; collecting many without applying; saying certificates are useless.

### Q20 ⭐ 🟢 Have you shared your SQL work publicly, for example on GitHub?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Evidence of real work, communication skill (the README), and professional habits.
**Say this in the interview:** "Yes, I have two small projects on GitHub: an HR attrition analysis and a sales analysis. Each has the SQL file, a README with the business question, the schema, how to run it, and a five-line findings summary with numbers. I use synthetic or public data only, never real employee data." (Say this only once it is true; if not yet, say you are building one and describe it.)
**Explain simply:**
- A repository (repo) is a project folder stored online with a history of changes (git is the tool; GitHub is a website that hosts it).
- Minimum repo: `README.md`, `schema.sql` (tables), `queries.sql` (numbered queries with a comment stating the question), sample CSV or generator script, a results file.
- Basic git commands (standard usage, not run here): `git init`, `git add .`, `git commit -m "message"`, then push to a new GitHub repository.
- Never upload company, customer or real employee data. Use self-made tables or datasets whose licence you checked (Northwind SQLite3 port states MIT; Chinook licence file not read; Kaggle IBM HR download terms unverified).
- If you share publicly, put the project link on your resume (Book 12 covers portfolio and resume).
**Example:** README skeleton: Question; Data (source and licence); Tables; How to run (`sqlite3 hr.db < schema.sql`); Findings (5 bullets with numbers); Limitation.
**Weak vs strong:**
- Weak: "I have a GitHub account." (empty)
- Strong: a repo with a clear README and a finding with a number.
**Likely follow-ups:**
- *Which project are you proudest of?* The one where you caught a data problem.
- *What would you improve?* More data checks, a chart, a second dataset.
**Common mistakes:** Uploading confidential data; no README; copying tutorial queries without a business question; repos with only a notebook and no explanation.

### Q21 ⭐ 🟡 How would you build a SQL portfolio project from a public dataset?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** An end-to-end method: question, data, cleaning, queries, interpretation, limitation.
**Say this in the interview:** "I pick a business question first, load a public dataset into SQLite, check row counts, duplicates and NULLs, create a clean view, write ten or so queries that answer the question, and finish with five findings with numbers and one limitation. Everything goes on GitHub with a README."
**Explain simply:** Seven steps:
- 1 Question: for example "Which department loses people fastest?" or "Which months drive revenue?".
- 2 Data: a source from the datasets list (Q11). Check licence and login rules yourself where marked unverified.
- 3 Load: CSV into SQLite using pandas `to_sql` or DB Browser import (Q12).
- 4 Profile: row count, distinct keys, NULLs, date ranges.
- 5 Clean: de-duplicate, drop or flag missing values; keep a raw table and a cleaned view.
- 6 Analyse: 10 to 12 queries from basic to window functions.
- 7 Communicate: five findings with numbers, a limitation, a README.
**Example:** (run, synthetic orders CSV with one duplicate row and one missing amount) Profile first. Sample data, table `orders_raw`:

| order_id | order_date | customer | category | amount |
|---|---|---|---|---|
| 1001 | 2026-01-05 | Asha | Books | 900 |
| 1002 | 2026-01-18 | Bala | Toys | 750 |
| 1003 | 2026-02-02 | Chitra | Books | 800 |
| 1003 | 2026-02-02 | Chitra | Books | 800 |
| 1004 | 2026-02-20 | Dev | Toys | 650 |
| 1005 | 2026-03-07 | Esha | Books | 700 |
| 1006 | 2026-03-25 | Farhan | Toys | 550 |
| 1007 | 2026-03-30 | Gita | Books | NULL |

**SQL:**
```sql
SELECT COUNT(*) AS rows_raw, COUNT(DISTINCT order_id) AS distinct_orders,
       SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END) AS missing_amount
FROM orders_raw;
```
**Output:**

| rows_raw | distinct_orders | missing_amount |
|---|---|---|
| 8 | 7 | 1 |

8 rows but 7 distinct orders: one duplicate; one missing amount. Then clean and answer a question.
```sql
CREATE VIEW orders_clean AS
SELECT DISTINCT order_id, order_date, customer, category, amount
FROM orders_raw WHERE amount IS NOT NULL;

SELECT substr(order_date,1,7) AS month, COUNT(*) AS orders, SUM(amount) AS revenue
FROM orders_clean GROUP BY substr(order_date,1,7) ORDER BY month;
```
**Output:**

| month | orders | revenue |
|---|---|---|
| 2026-01 | 2 | 1650 |
| 2026-02 | 2 | 1450 |
| 2026-03 | 2 | 1250 |

**pandas equivalent:**
```python
raw = pd.read_csv("orders.csv")
cl = raw.drop_duplicates().dropna(subset=["amount"]).copy()
cl["amount"] = cl["amount"].astype(int)   # NaN made the column float; restore whole numbers
cl["month"] = cl["order_date"].str[:7]
result = cl.groupby("month").agg(orders=("order_id","count"), revenue=("amount","sum")).reset_index()
```
**Output:**

| month | orders | revenue |
|---|---|---|
| 2026-01 | 2 | 1650 |
| 2026-02 | 2 | 1450 |
| 2026-03 | 2 | 1250 |

**Edge cases:** Dropping rows with missing amounts changes totals; say how many and why. Note that `DISTINCT` removes only fully identical rows; two rows with the same order_id but different amounts need a rule (Part 10). Whole-month comparisons are unfair if the last month is incomplete.
**Likely follow-ups:**
- *How do you choose a dataset?* One where you understand the business, with at least two related tables.
- *How big?* Small is fine if your reasoning is clear.
**Common mistakes:** Starting with queries and no question; no cleaning step; a README with no numbers; using real company data.

### Q22 ⭐ 🟡 How do you know you are job-ready in SQL? What self-test would you use?
**Asked at:** commonly asked (no company-specific report found). Market context: SQL appeared in 54% of 186 sampled India analyst job descriptions (non-random sample, about plus or minus 7 points) and in about 19 of 20 company interview profiles (anecdotal reports). Core SQL is a must-have, so a self-test before applying is sensible.
**What the interviewer is checking:** Self-awareness and a method: not a feeling of readiness but evidence.
**Say this in the interview:** "I use closed-book timed tests: eight queries in 45 minutes on a dataset I did not practise on, speaking my approach aloud, and I check every answer for NULLs, duplicates and ties. I consider myself ready when I pass that test twice in a row on two different datasets and have two finished projects online."
**Explain simply:**
- Job-ready signal (from the roadmap): pass the Final test twice in a row on two different datasets and have at least two finished mini-projects online.
- Quizzes: Quiz 1 after week 2 (10 queries, 8 correct), Quiz 2 after week 3 (7 of 8), Quiz 3 week 5 (6 of 8 joins), Quiz 4 week 7 (5 of 6), Quiz 5 week 9 (6 of 8), Quiz 6 week 11 (4 of 5 scenarios), Final week 12 (4 of 5 mock round, 45 minutes). Below pass: repeat the week and retake after 3 days.
- Below is a runnable test kit. Create the database, try each question without looking, then compare with the answer key. Test database (run in any SQLite tool):
```sql
CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, dept_name TEXT);
INSERT INTO departments VALUES (10,'HR'),(20,'Sales'),(30,'IT');
CREATE TABLE employees (emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, manager_id INTEGER,
  hire_date TEXT, exit_date TEXT, salary INTEGER, overtime TEXT);
INSERT INTO employees VALUES
(1,'Asha',10,NULL,'2019-04-01',NULL,90000,'N'),
(2,'Bala',10,1,'2021-06-15',NULL,52000,'N'),
(3,'Chitra',10,1,'2022-01-10','2023-09-30',48000,'Y'),
(4,'Dev',20,NULL,'2018-07-01',NULL,110000,'N'),
(5,'Esha',20,4,'2020-03-05',NULL,60000,'Y'),
(6,'Farhan',20,4,'2021-08-20','2024-02-29',58000,'Y'),
(7,'Gita',20,4,'2023-02-01',NULL,57000,'N'),
(8,'Hari',20,4,'2023-05-15','2024-06-30',59000,'Y'),
(9,'Isha',30,NULL,'2017-11-01',NULL,130000,'N'),
(10,'Jai',30,9,'2020-09-14',NULL,95000,'Y'),
(11,'Kiran',30,9,'2021-01-25',NULL,95000,'N'),
(12,'Lata',30,9,'2022-07-11','2025-01-31',88000,'Y'),
(13,'Manoj',30,9,'2024-03-04',NULL,72000,'N'),
(14,'Neha',20,4,'2024-01-08',NULL,112000,'N'),
(15,'Om',10,1,'2024-07-01',NULL,45000,'N'),
(16,'Pooja',NULL,1,'2024-09-01',NULL,50000,'N');
CREATE TABLE leave_log (emp_id INTEGER, leave_date TEXT);
INSERT INTO leave_log VALUES (2,'2026-08-03'),(2,'2026-08-04'),(5,'2026-08-10'),(5,'2026-08-11'),(5,'2026-08-12'),(10,'2026-08-20'),(11,'2026-08-21'),(11,'2026-08-22'),(3,'2023-05-02');
```
**Self-test questions (try before reading the key):**
- T1 How many current employees are there (exit_date is NULL)? (Quiz 1)
- T2 Average salary by dept_id, rounded. What does the NULL group mean? (Quiz 2)
- T3 Department names where the average salary exceeds 70,000. (Quiz 2, HAVING)
- T4 Employees with no matching department. (Quiz 3, LEFT JOIN with NULL check)
- T5 Employees earning more than their manager. (Quiz 3, self join)
- T6 Top 2 salary levels in each department (ties shared). (Quiz 4)
- T7 Attrition percentage by department name, one decimal. (Quiz 5-6)
- T8 Hires per year, running total of hires, and change versus the previous year. (Quiz 5, window)

**Answer key (SQLite 3.45.1; every query was run):**

T1
```sql
SELECT COUNT(*) AS active_headcount FROM employees WHERE exit_date IS NULL;
```
**Output:**

| active_headcount |
|---|
| 12 |

T2 (the NULL row is Pooja, who has no department)
```sql
SELECT dept_id, ROUND(AVG(salary)) AS avg_salary FROM employees GROUP BY dept_id ORDER BY dept_id;
```
**Output:**

| dept_id | avg_salary |
|---|---|
| NULL | 50000 |
| 10 | 58750 |
| 20 | 76000 |
| 30 | 96000 |

T3
```sql
SELECT d.dept_name, ROUND(AVG(e.salary)) AS avg_salary
FROM employees e JOIN departments d ON d.dept_id = e.dept_id
GROUP BY d.dept_name HAVING AVG(e.salary) > 70000 ORDER BY d.dept_name;
```
**Output:**

| dept_name | avg_salary |
|---|---|
| IT | 96000 |
| Sales | 76000 |

T4
```sql
SELECT e.name FROM employees e LEFT JOIN departments d ON d.dept_id = e.dept_id WHERE d.dept_id IS NULL;
```
**Output:**

| name |
|---|
| Pooja |

T5
```sql
SELECT e.name AS employee, e.salary, m.name AS manager, m.salary AS manager_salary
FROM employees e
JOIN employees m ON m.emp_id = e.manager_id
WHERE e.salary > m.salary;
```
**Output:**

| employee | salary | manager | manager_salary |
|---|---|---|---|
| Neha | 112000 | Dev | 110000 |

T6
```sql
SELECT dept_id, name, salary FROM (
  SELECT dept_id, name, salary, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r
  FROM employees WHERE dept_id IS NOT NULL
) WHERE r <= 2 ORDER BY dept_id, salary DESC, name;
```
**Output:**

| dept_id | name | salary |
|---|---|---|
| 10 | Asha | 90000 |
| 10 | Bala | 52000 |
| 20 | Neha | 112000 |
| 20 | Dev | 110000 |
| 30 | Isha | 130000 |
| 30 | Jai | 95000 |
| 30 | Kiran | 95000 |

T7 (attrition = exits divided by everyone who ever joined; Pooja is excluded by the inner join, so say so)
```sql
SELECT d.dept_name,
       ROUND(100.0 * SUM(e.exit_date IS NOT NULL) / COUNT(*), 1) AS attrition_pct
FROM employees e JOIN departments d ON d.dept_id = e.dept_id
GROUP BY d.dept_name ORDER BY attrition_pct DESC, d.dept_name;
```
**Output:**

| dept_name | attrition_pct |
|---|---|
| Sales | 33.3 |
| HR | 25.0 |
| IT | 20.0 |

T8
```sql
WITH y AS (
  SELECT substr(hire_date,1,4) AS yr, COUNT(*) AS hires FROM employees GROUP BY substr(hire_date,1,4)
)
SELECT yr, hires,
       SUM(hires) OVER (ORDER BY yr) AS running_hires,
       hires - LAG(hires) OVER (ORDER BY yr) AS change_vs_prev_year
FROM y ORDER BY yr;
```
**Output:**

| yr | hires | running_hires | change_vs_prev_year |
|---|---|---|---|
| 2017 | 1 | 1 | NULL |
| 2018 | 1 | 2 | 0 |
| 2019 | 1 | 3 | 0 |
| 2020 | 2 | 5 | 1 |
| 2021 | 3 | 8 | 1 |
| 2022 | 2 | 10 | -1 |
| 2023 | 2 | 12 | 0 |
| 2024 | 4 | 16 | 2 |

**Example:** In one attempt you match the key on T1-T5, T7 and T8, but on T6 you used ROW_NUMBER, so Kiran (tied with Jai at 95,000) is missing. That is 7 of 8, and the error log says "ties: use DENSE_RANK". Repeat T6-style questions, then retake after 3 days.

**Scoring:** a query counts only if the output matches the key, including row count and ties. Explain WHERE versus HAVING and RANK versus DENSE_RANK aloud. A pass of 7 of 8 with clear explanations is a good signal; below 5, repeat Parts 2-5.
**Edge cases:** Ties (Jai and Kiran), NULL department (Pooja), a manager with no manager (NULL), and the first year of a LAG (NULL difference).
**Likely follow-ups:**
- *What if you fail?* Log each error, repeat that week's practice, retake after 3 days.
- *What next after passing?* A second dataset (Chinook or Northwind) and timed mocks.
**Common mistakes:** Judging readiness by hours studied; practising and testing on the same data; checking only that the query runs; ignoring explanation.

### Q23 ⭐ 🟡 What do you do in a timed SQL test when you cannot finish all the questions?
**Asked at:** commonly asked (no company-specific report found). Reports of online SQL assessments with several questions appear in `interview_processes.md` (for example a PhonePe online assessment with five SQL questions, one easy, two medium and two hard, and Meesho online assessments with several SQL questions); these are single or anecdotal reports.
**What the interviewer is checking:** Time management, composure, and whether partial work shows reasoning.
**Say this in the interview:** "I read all the questions first, solve the easiest and surest ones, and mark the rest. For a hard one I write the part I know, such as the joins and a clear structure, and state my assumption. A partial query with correct logic and comments earns more than a blank. I leave the last five minutes to re-check NULLs, duplicates and ties on what I submitted."
**Explain simply:**
- Minute 0-3: scan all questions; rank by difficulty and marks.
- Do easy and medium first; set a limit per question (about 10 minutes for a medium) and move on when you hit it.
- On a stuck question: write the skeleton (FROM, JOIN, WHERE), then the aggregate or window step, then comment what is missing.
- If you cannot run it, say how you would test it.
- Keep the last 5 to 10 minutes for review; do not start a new hard problem.
- Live round: think aloud and ask a clarifying question (ties? NULLs? inclusive dates?).
**Example:** Question: "Employees who earned above their department average." Skeleton, even if you run out of time: join to a CTE of department averages; comment: `-- filter salary > dept_avg; check NULL salaries`.
**Edge cases:** If the platform auto-grades only on exact output, a partial query scores zero, so order your time to secure sure points first. Check whether wrong answers are penalised.
**Likely follow-ups:**
- *Do you guess?* On auto-graded multiple choice, check the rules; for queries write your best logic.
- *Have you practised timed tests?* Yes, a weekly 45-minute timed set in the plan.
**Common mistakes:** Spending 30 minutes on one hard problem; leaving questions blank; not re-checking; panicking silently.

### Q24 ⭐ 🔴 How would you teach SQL to a non-technical colleague in four weeks?
**Asked at:** commonly asked (no company-specific report found). Occasional, usually to test communication.
**What the interviewer is checking:** Can you explain simply, structure a plan, and keep a beginner motivated?
**Say this in the interview:** "I would teach by questions the colleague already asks in their job. Week 1: reading and filtering one table. Week 2: counting and grouping. Week 3: joining tables. Week 4: a small project on their own data. Thirty to forty-five minutes a day, always typing real queries, and a short quiz at the end of each week. The rule: they type, I do not."
**Explain simply:** Four-week plan (45 min a day, 5 days a week; for an HR colleague use HR tables; maps to Book 2 Parts 1-3 and 7):
| Week | Goal | Practice | End-of-week check |
|---|---|---|---|
| 1 | A table is rows and columns; SELECT, WHERE, ORDER BY, DISTINCT, LIMIT; NULL means unknown | 20 queries on an employees table | 8 of 10 correct (Quiz 1) |
| 2 | COUNT, SUM, AVG, GROUP BY; WHERE versus HAVING; CASE WHEN for bands | 20 queries (headcount by department, average salary) | 7 of 8; explain WHERE versus HAVING aloud |
| 3 | JOIN and LEFT JOIN with departments/leave; check row counts after a join | 15 queries | 6 of 8; no accidental duplicates |
| 4 | Mini project on their own anonymised practice data: 5 questions and a one-page summary | Present findings in 5 minutes | Review: read each query aloud and say why |

- Method: explain with a real question first, then the syntax; give a worked example, then a slightly different one for them to try; make errors normal and keep a mistakes log; use free tools (SQLBolt, SQLZoo; free status in Q10).
- Check understanding by asking them to predict an output before running.
- Use the Q22 kit style for quizzes.
**Example:** (lesson 1, run) "List current Sales employees by salary" teaches SELECT, WHERE, AND and ORDER BY in one query.
**SQL:**
```sql
SELECT name, salary
FROM employees
WHERE dept_id = 20 AND exit_date IS NULL
ORDER BY salary DESC;
```
**Output:**

| name | salary |
|---|---|
| Neha | 112000 |
| Dev | 110000 |
| Esha | 60000 |
| Gita | 57000 |

**Edge cases:** Do not overload week 1 with joins; a learner who cannot read one table will drown. A colleague with no tool access can use a browser editor (free-tier limits unverified).
**Likely follow-ups:**
- *What if they fall behind?* Repeat the week; do not move on.
- *How do you know it worked?* They pass the weekly check and can explain a query without help.
**Common mistakes:** Showing slides instead of typing; starting with theory; teaching windows functions in month one; not checking understanding.


---

## Skill-development plan: from zero to job-ready SQL (12 weeks)

This is the plan the questions above refer to. It is a study design, not a research finding: the hours, problem counts and pass marks are targets to adjust, not figures from a source. Platform names and free/paid notes are in Q10; datasets are in Q11; the self-test kit is in Q22.

### A. Zero-to-job-ready roadmap (about 2 hours a day, 6 days a week)
| Week | Topics (Book 2 part) | Problem target | Check at the end |
|---|---|---|---|
| 1 | SELECT, WHERE, ORDER BY, DISTINCT, LIMIT (Part 1); skim Part 11 (keys, tables) | 25 | none |
| 2 | COUNT/SUM/AVG, GROUP BY, HAVING, a first look at NULL (Part 2) | 30 | Quiz 1: 10 queries, 8 correct |
| 3 | Consolidate aggregates and filters on the HR tables | 30 | Quiz 2: 7 of 8 |
| 4 | INNER and LEFT JOIN (Part 3) | 25 | none |
| 5 | Self join, anti-join, join traps (duplicates after a join) | 20 | Quiz 3: 6 of 8 on joins |
| 6 | Subqueries and CTEs (Part 4) | 25 | none |
| 7 | Window functions: ROW_NUMBER, RANK, DENSE_RANK (Part 5) | 25 | Quiz 4: 5 of 6 |
| 8 | LAG/LEAD, running totals (Part 6) | 20 | none |
| 9 | CASE WHEN, NULL handling, strings, dates (Part 7) | 30 | Quiz 5: 6 of 8 |
| 10 | Business scenarios: sales, HR, e-commerce, banking (Part 8) | 15 | none |
| 11 | Hard patterns: cohorts, funnels, de-duplication, nth highest (Parts 9-10) | 15 | Quiz 6: 4 of 5 scenarios |
| 12 | Revisit Part 11; two timed mock rounds; finish projects | mocks | Final: 4 of 5 in 45 minutes |

Weeks 1-11 add up to 260 problems (25+30+30+25+20+25+25+20+30+15+15, checked by running the sum). If you miss a pass mark: repeat that week and retake the quiz after 3 days. Job-ready signal: pass the Final twice in a row on two different datasets and have at least two finished mini-projects online (Q22).

### B. Daily practice plan (120 minutes)
| Block | Minutes | What you do |
|---|---|---|
| Learn | 30 | Read the Book 2 part or one interactive lesson |
| Guided practice | 30 | Re-type the worked examples, change one thing, predict the output |
| Problem solving | 40 | 3 to 5 problems alone, no hints for the first 10 minutes |
| Review | 20 | Update the mistakes log; redo yesterday's failed problem |

With 1 hour a day, halve each block and never skip Review; the roadmap then takes about 24 weeks. One day a week is rest.

### C. Free resources
See Q10 for the full table with what each site itself states about price. Stage guide: SQLBolt (weeks 1-3), SQLZoo joins (weeks 4-5), DataLemur crash course and free questions (weeks 6-9), HackerRank for timed practice (weeks 10-12). LeetCode's Top SQL 50 could not be checked here; verify what needs Premium yourself.

### D. Practice datasets
Self-made HR tables first (the 16-row `employees` table in Q6 and Q22), then Chinook or Northwind for realistic multi-table joins (Q11), then a public HR attrition CSV for a project. Check each licence yourself where Q11 says unverified.

### E. Mini-projects
| Project | Question | Data | Skills shown | Where explained |
|---|---|---|---|---|
| 1 HR attrition | Which department loses people fastest? | Self-made employees, departments, leave | LEFT JOIN, CASE WHEN, DENSE_RANK | Q6 |
| 2 Sales/orders analysis | Which months drive revenue? | Synthetic or public orders CSV | Profiling, de-duplication, GROUP BY by month | Q21 |
| 3 Chinook revenue | Which country brings the most invoice revenue? | Chinook (SQLite script) | Multi-table joins, window ranking | Q11 |

Each project: README with the question, data source and licence, tables, how to run, five findings with numbers, one limitation (Q20).

### F. Self-check tests
Six quizzes (weeks 2, 3, 5, 7, 9, 11) and a Final (week 12) use the pass marks in table A. The runnable kit with database, eight questions T1-T8 and an answer key is in Q22. Test on a dataset you did not practise on, closed book, and speak your approach aloud.
