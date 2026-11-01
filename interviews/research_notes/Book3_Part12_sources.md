# Book 3 Part 12 Sources & research notes (Company-style mixed mock sets: FAANG, fintech, e-commerce)

Date: 2026-10-26. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. Three WebSearch calls were made; every WebFetch attempt failed (getaddrinfo ENOTFOUND for letsdatascience.com and interviewquery.com), so NO page was opened. All sources below are SEARCH SNIPPET ONLY (search tool summaries). No company-reported exact question was verified; 'Asked at' tags are source types.

## Pages OPENED (WebFetch)
None (fetch failures noted above).

## Snippet-only sources (not opened)
| Source | URL | What the snippet said (as summarised by the search tool) | Used for |
|---|---|---|---|
| Interview Query, Amazon SQL interview questions | https://www.interviewquery.com/p/amazon-sql-interview-questions | phone screen basics (DATE, GROUP BY, JOIN); onsite moves to CASE, JOIN, subqueries, complex queries; leadership principles also assessed | Set F3 difficulty ramp |
| Interview Query, Google SQL interview questions | https://interviewquery.com/blog-google-sql-interview-questions | SQL in technical screen and onsite, intermediate to advanced | Set F2 |
| Interview Kickstart, Meta data engineer guide | https://interviewkickstart.com/blogs/articles/meta-data-engineer-interview | SQL and Python questions; joins, aggregations, windows, CASE, self-joins, CTEs | Set F1 |
| Glassdoor and 1point3acres thread listings (Meta DS, Amazon DS onsite, Google DS onsite) | glassdoor.com Meta Data Science interview listing; 1point3acres.com/interview/thread/1128661 and /1161683 | candidate anecdotes: SQL is one round among case, product sense, behavioural; round counts vary | the idea of a short multi-question SQL block next to other rounds (anecdotal, unverified) |
| Brex interview guide (techinterview.org) | https://www.techinterview.org/companies/brex/ | weights idempotency, reconciliation, fraud; reconciliation with late-arriving data | Set T1 Q4 reconciliation |
| DBS data analyst guide (Interview Query) | https://www.interviewquery.com/interview-guides/dbs-bank-data-analyst | last transaction per user, filtered transaction counts, date-bounded revenue shares | Set T1, T2 |
| Let's Data Science Stripe practice set | https://letsdatascience.com/problems/companies/stripe | 15 SQL problems on payment analytics and fraud detection | Set T1 fraud rule |
| Dataford transactions list | https://dataford.io/questions/lists/transactions-questions | ACID and isolation-level questions (concept; not turned into questions here) | none (noted only) |
| Let's Data Science e-commerce and marketplace SQL list | https://letsdatascience.com/blog/sql-interview-questions-ecommerce-marketplace | 15 problems on joins, CTEs, windows; repeat purchase rate; says it draws on reported candidate experiences (unverified) | Set E1, E2 |
| Dev Genius, e-commerce SQL interview | https://blog.devgenius.io/e-commerce-sql-interview-success-4b31461a86c9 | first-time versus repeat customers per day | Set T3 Q1, E1 |
| Scribd user-uploaded question sets | scribd.com/document/893663585 and others | retention cohort query, percent of orders returned, buyers with no return; unknown provenance | idea only |

## Design decisions
- Sets of 5 questions, 100 points each (warm-up 10, two middle at 20, two hard at 25), practice time budgets 41 to 48 minutes set by this book, not by any company.
- Evidence gaps: no free page found that lists real ledger-reconciliation SQL questions; reconciliation, velocity and double-entry questions are expert extensions. Isolation levels and ACID (Dataford) are left to Part 11 Q35.
- No company-specific claims are made beyond the snippets above; guides are cited as editorial.

## Cross-references verified by heading (Book3_SQL part files, checked 2026-10-26)
Part 1 Q4, Q6, Q10; Part 2 Q2, Q3, Q5, Q12, Q15, Q16, Q26, Q32, Q36, Q37, Q44; Part 3 Q3, Q14, Q35; Part 4 Q2, Q4, Q5, Q9, Q14, Q15, Q31, Q45, Q46; Part 5 Q3, Q6, Q12, Q16, Q22, Q39, Q45; Part 6 Q3, Q6, Q10, Q11, Q12, Q13, Q14, Q18, Q20, Q33, Q39; Part 7 Q6, Q7, Q8, Q11, Q12, Q16, Q26, Q28; Part 8 Q1, Q4, Q7, Q9, Q10, Q11, Q21, Q27, Q33, Q41; Part 9 Q4, Q9.

## Hedge and run list for Wave B
- Run everything on SQLite 3.45.1 and pandas 3.0.5; seed data is small and fixed, defined in each answer's own code.
- Timestamps are TEXT: RANGE frames with INTERVAL are not available in SQLite; use LAG/self join (T1 Q5), and say so. merge_asof needs sorted keys and matching dtypes.
- FULL OUTER JOIN is emulated or run (SQLite 3.45 supports it); other engines hedged, not executed.
- Time budgets and scoring are this book's own suggestions.
