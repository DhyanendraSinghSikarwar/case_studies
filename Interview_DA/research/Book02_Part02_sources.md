# Book 2 Part 2 sources: Aggregates, GROUP BY, HAVING (accessed 2026-10-21)

Method: 4 web searches + 5 page fetches. Frequency = number of distinct sources (of those listed below) where the question appears. Sample is small; stars are judged on this plus the service-MNC pattern in research/interview_processes.md (SQL "GROUP BY/HAVING" listed as a standard service-MNC question type).

## Sources
| # | Source | Type | Date | Status |
|---|---|---|---|---|
| S1 | https://learnsql.com/blog/group-by-sql-interview-questions/ | Prep guide (9 GROUP BY questions) | undated | read |
| S2 | https://in.indeed.com/career-advice/interviewing/data-analyst-sql-interview-questions | Prep guide, India | published 10 Sep 2025 | read |
| S3 | https://www.ccbp.in/blog/articles/sql-interview-questions-for-data-analyst | Prep guide, India | Dec 2024, updated Mar 2026 | read |
| S4 | https://www.stratascratch.com/blog/sql-interview-questions-for-the-data-analyst-position | Real company questions (Zillow, Postmates, Airbnb) | undated | read |
| S5 | https://www.glassdoor.com.ar/Entrevista/Meesho-Entrevista-E1503776-RVW102029329.htm | Candidate report, Meesho Bengaluru BA intern, Sep and Nov 2025 | 2025 | seen via search snippet only; anecdotal |
| S6 | https://www.glassdoor.es/Entrevista/Infosys-Entrevista-E7927-RVW98413987.htm | Candidate report, Infosys Hyderabad DA, Jul 2025 | 2025 | snippet only; anecdotal (second-highest salary question, Part 10 topic) |
| S7 | research/interview_processes.md (local) | Internal research | Oct 2026 | read grep lines |
| S8 | https://www.interviewquery.com/p/sql-group-by | Guide (WHERE vs HAVING timing) | 2025 | snippet only |
| S9 | https://www.dataquest.io/blog/data-analyst-interview-questions/ | Guide; says SQL in about 85% of DA interviews (unverified claim) | updated 24 Feb 2026 | snippet only |

## Question tally (canonical topic: sources: company type)
| Topic | Sources | Count | Company type |
|---|---|---|---|
| What is GROUP BY / purpose | S1, S2, S3 | 3 | prep guides (all types) |
| WHERE vs HAVING | S1, S2, S3, S8 | 4 | guides; service MNC pattern S7 |
| Aggregate functions list | S2, S3, S1 | 3 | guides |
| COUNT(*) vs COUNT(col) vs COUNT(DISTINCT) | S1 | 1 (S4 uses COUNT DISTINCT in a real question) | guide + product (Postmates) |
| NULLs with GROUP BY | S1 | 1 | guide |
| Find duplicates with GROUP BY/HAVING | S2, S3, S7, plus Scribd guide (found via search, not read) | 3 read | guides; service MNC S7 |
| Groups above a threshold (HAVING COUNT/SUM) | S1, S4 (Zillow avg price vs national avg) | 2 | guide + product |
| Multi-column GROUP BY | S1, S4 (Airbnb) | 2 | guide + product |
| GROUP BY extensions (ROLLUP etc.) | S1 | 1 | guide |
| Median per group | S5 | 1 | product/e-commerce, Bengaluru, Nov 2025 |
| Basic Group By and Joins | S5 | 1 | product, Bengaluru, Sep 2025 |

## Gaps and limits
- No Hyderabad-specific GROUP BY/HAVING report found. Infosys Hyderabad (S6) is general SQL only.
- GeeksforGeeks, AmbitionBox: not returned by searches; not fetched. Scribd documents appeared but are unreviewed user uploads, not used as evidence.
- Glassdoor pages are shown only as search snippets; full text not read (likely login/regional gating). Treat as anecdotal.
- Frequencies are small tallies from a few guides, not statistical measures. Questions marked beyond this (conditional aggregation, attrition rate, fan-out after joins, AVG of averages, etc.) are gap-fill from the author's judgment of standard analyst SQL practice and the HR/e-commerce framing; frequency unverified.
