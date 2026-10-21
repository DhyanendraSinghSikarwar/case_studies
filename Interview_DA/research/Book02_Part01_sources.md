# Book 2 Part 1 — Sources (SELECT, WHERE, ORDER BY, DISTINCT, LIMIT)

Accessed 2026-10-21. Method: 6 web searches + 2 page fetches (small sample). Frequencies below are counts of how many sampled sources contain the topic, NOT true interview frequency. Stars in the part file are a judgement from these signals plus `research/interview_processes.md` (SQL basics, second/Nth highest salary are listed there as service-MNC staples).

## Sources actually retrieved
| # | Source | URL | Company type / region | Recency | Notes |
|---|---|---|---|---|---|
| S1 | Dataquest, SQL interview questions beginner to advanced (fetched) | https://www.dataquest.io/blog/sql-interview-questions-from-beginner-to-advanced/ | General prep guide | Mar 2026 | Fetch summary only |
| S2 | Interview Kickstart, SQL questions for data analysts (fetched) | https://www.interviewkickstart.com/interview-questions/sql-interview-questions-for-data-analysts | General prep guide | undated | Fetch summary only |
| S3 | CodingShuttle, SELECT and WHERE interview questions | https://www.codingshuttle.com/mock-tests/sql-for-interviews/select-and-where-interview-questions_27 | Practice set | undated | Orders 2023 / 'Completed' / sort by total_amount |
| S4 | AI2SQL SQL interview guide | https://builder.ai2sql.io/blog/sql-interview-questions | Prep blog | 2026 | Second highest salary: DISTINCT + ORDER BY + LIMIT 1 OFFSET 1 |
| S5 | Hyring, Top 65 SQL interview questions | https://hyring.com/jobseeker-toolkit/interview-questions/technical/sql | Prep blog | 2026 | DISTINCT, ORDER BY with LIMIT |
| S6 | Interview Query SQL cheat sheet | https://www.interviewquery.com/p/sql-cheat-sheet | Prep blog | 2025 | WHERE, ORDER BY |
| S7 | Glassdoor Indium Software reviews (Hyderabad/Bengaluru) | https://www.glassdoor.es/Entrevista/Indium-Software-Entrevista-E431611-RVW86286606.htm | Service/IT firm | 2026 | Anecdotal: SQL main focus (joins, group by, windows); array second-max |
| S8 | Glassdoor Infosys review (Bengaluru) | https://www.glassdoor.sg/Interview/Infosys-Interview-E7927-RVW96608711.htm | Service MNC | 2026 | Anecdotal: lots of SQL + Python |
| S9 | Glassdoor Cognizant reviews | https://clear.glassdoor.nl/Interview/Cognizant-Interview-E8014-RVW94968138.htm | Service MNC | 2025-26 | Anecdotal: SQL order of execution asked; Chennai/Delhi/Pune not Hyderabad |
| S10 | Interview Query TCS / Cognizant DA guides | https://www.interviewquery.com/interview-guides/tata-consultancy-services-data-analyst | Service MNC | 2025 | Generic: SQL and Python tested |
| S11 | Telegram repost of SQL guide (secondary, unverified) | https://t.me/s/programming_guide/3764 | Repost | undated | Execution order incl. DISTINCT; low trust |

## Topic tally (sources among S1-S6, S9, S11 that mention topic)
| Topic | Sources | Count |
|---|---|---|
| Execution order / alias in WHERE | S1, S9, S11 | 3 |
| Second / Nth highest salary (DISTINCT+ORDER BY+LIMIT/OFFSET) | S1 (3rd highest), S4, S7 (array variant, anecdotal) | 2 verified + 1 anecdote |
| SELECT+WHERE+ORDER BY (hired after year, sort salary desc) | S1, S3, S6 | 3 |
| NULL (= NULL, IS NULL, COALESCE) | S1, S2 | 2 |
| LIKE / IN / BETWEEN | S1, S2 | 2 |
| DISTINCT meaning / pitfalls | S1, S2, S5 | 3 |
| LIMIT vs TOP across dialects | S2 | 1 |
| ORDER BY multi-column | S2 | 1 |
| Ties, duplicates, dialect assumptions | model-answers page (https://macmyths.com/sql-interview-questions-with-model-answers/) | 1 |

## Limits and blocked sources
- GeeksforGeeks pages did not appear in search results; no GfG content used. Not blocked, just not returned.
- AmbitionBox search returned only an unrelated company page (Zifo); no AmbitionBox content used.
- Scribd uploads appeared in results (login/low trust); not used as evidence.
- No company-specific per-question frequency was found for Hyderabad/Bengaluru Part-1 topics; company-type labels are from Glassdoor anecdotes only. Treat all star ratings as editorial judgement. Frequency counts beyond the tallies above: unverified.
- Gap-fill (not from sources, added as important basics): three-valued logic, NOT IN with NULL, BETWEEN with timestamps, ORDER BY tie-breaking, NULL sort position, pagination, ESCAPE, WITH TIES, keyset pagination, HR-flavoured scenarios (Candidates, Attendance).
