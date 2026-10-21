# Book 2 Part 4 (Subqueries & CTEs) - question sources

Accessed 2026-10-21. Method: 3 web searches (WebSearch is US-only, no Hyderabad/Bengaluru filter possible), 1 page fetch, plus re-use of `research/interview_processes.md`. Evidence is anonymous, candidate-reported and thin; frequency counts below are tallies of sources seen, not statistics. Questions beyond these sources were filled from standard SQL curriculum to meet the target (gap-fill, unverified as "asked").

## Evidence log
| Question / theme | Source | Company type | Recency | Notes |
|---|---|---|---|---|
| Define CTE and subquery; median per subject per class | Meesho BA intern Glassdoor review, https://fr.glassdoor.ca/Entretien/Meesho-Entretien-E1503776-RVW101235764.htm | Startup, Bengaluru | undated in snippet | Window functions also stressed |
| Subquery vs CTE (temporary result set vs nested query) | AmbitionBox Comfort Click Data Manager, https://www.ambitionbox.com/interviews/comfort-click-interview-questions/data-manager | Small firm | 2024 or earlier | |
| Correlated vs non-correlated subquery | AmbitionBox Deloitte Data Analyst page 4, https://www.ambitionbox.com/interviews/deloitte-interview-questions/data-analyst?page=4 | Consulting/service | not verified | |
| CTE, joins, window functions "mostly asked" | Infosys Glassdoor review, https://www.glassdoor.sg/Interview/Infosys-Interview-E7927-RVW96951406.htm | Service MNC | 2022 | |
| Third-highest salary (SQL order of execution) | Flipkart Glassdoor reviews, https://fr.glassdoor.ca/Entretien/Flipkart-Entretien-E300494-RVW91644973.htm | Product, Bengaluru | Mar-Jul 2025 | Scenario SQL; nth-highest itself belongs to Part 10 |
| "What is a CTE? When do you use it?"; "Give an example of a subquery" | LearnSQL guide, https://learnsql.com/blog/sql-interview-questions-for-data-analyst/ | Generic guide | undated | Only these two matched |
| Subquery vs CTE guidance; correlated vs non-correlated | Indeed India SQL guide (updated Sep 2025), https://in.indeed.com/career-advice/interviewing/data-analyst-sql-interview-questions | Generic guide | Sep 2025 | Seen in search summary only |
| Basic CTE SQL (Microsoft Hyderabad DA); CTE (Wipro 2023); CTE/stored procedures | `research/interview_processes.md` (Microsoft, Wipro entries) | GCC / service MNC | 2023-2025 | See that file for review URLs |
| Indium: SQL joins/windows/CTEs; one panel preferred "traditional" SQL over CTEs | `research/interview_processes.md` (Indium entry) | Analytics firm, Hyderabad | Jan-Jul 2026 | Useful for the CTE vs subquery readability question |
| Department-highest-salary query (Wipro Noida 2025); third-highest per department (Amazon Blr 2025) | `research/interview_processes.md` | Service MNC / GCC | 2025 | Basis for "top earner per department" subquery questions |

## Frequency read
- Subquery vs CTE and "what is a CTE": 5+ sources (Meesho, Comfort Click, Infosys, LearnSQL, Indeed) -> three star.
- Correlated subquery, department-average salary: 2-3 sources + standard curriculum -> three star.
- NOT IN / NOT EXISTS, IN vs EXISTS: standard; no direct India report found -> two star (NOT EXISTS anti-join pattern is promoted to three star as a classic "customers with no orders").
- Temp table / view / materialisation / LATERAL / relational division: gap-fill only -> one star.

## Blocked or unavailable
- Glassdoor pages returned only snippets (French/other-locale mirrors); full text not read.
- Reddit, Naukri, Indeed full pages not accessible; no 2026 Hyderabad-specific subquery report found.
- Limitation: search tool is US-only, so city targeting was by keyword only.
