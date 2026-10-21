# Book 2 Part 8 sources: scenario business queries (sales, HR, e-commerce, banking)

Gathered 2026-10-21 using web search only (no page fetches). Search snippets only; no full pages read. Frequency = number of separate sources naming the pattern in this sampling (small sample, not a tally of interviews).

## Sources found
| # | Source | URL | Type | What it supports |
|---|---|---|---|---|
| 1 | Interview Query, SQL questions for data analysts (2025) | https://www.interviewquery.com/p/sql-questions-data-analyst | guide [G] | scenario-style SQL screens, live tasks, take-homes |
| 2 | Analytics Vidhya, 50 SQL query interview questions (Jan 2025) | https://www.analyticsvidhya.com/blog/2025/01/sql-query-interview-questions/ | guide [G] | customers with no orders, per-department salary, month-wise revenue |
| 3 | Swiggy DA guide, Interview Query | https://www.interviewquery.com/interview-guides/swiggy-data-analyst | guide [G] | OA with SQL (window functions, GROUP BY, HAVING) |
| 4 | Flipkart DA guide, Interview Query | https://www.interviewquery.com/interview-guides/flipkart-data-analyst | guide [G] | written test with aptitude + SQL |
| 5 | Meesho DA guide, Interview Query | https://www.interviewquery.com/interview-guides/meesho-data-analyst | guide [G] | joins, window functions, aggregation |
| 6 | PhonePe DA reports, AmbitionBox (Dec 2024 report) | https://www.ambitionbox.com/interviews/phonepe-interview-questions/data-analyst | candidate reports [S] | SQL + Power BI + aptitude round |
| 7 | Amazon SQL interview questions, DataLemur | https://datalemur.com/blog/amazon-sql-interview-questions | guide [G] | BA SQL easier than BIE; product/review aggregates |
| 8 | Amazon BA interview questions, StrataScratch | https://stratascratch.com/blog/amazon-business-analyst-interview-questions | guide [G] | business-process SQL questions |
| 9 | LeetCode discussion, Amazon DA SQL (older, 2018-19 dates) | https://leetcode.com/discuss/interview-question/606844/amazon-data-analyst-sql-interview-questions | forum [S] | orders + items tables; first/second order per customer |
| 10 | Bank SQL questions (Scribd upload) | https://www.scribd.com/document/897652445/Bank-SQL-Interview-Questions-15 | user upload, unverified | balance per branch, balance above average |
| 11 | Data analyst questions deck (Scribd upload) | https://www.scribd.com/presentation/651043002/DataAnalystInterviewQuestions | user upload, unverified | final balance per account from deposits/withdrawals |
| 12 | Yardstick HR data analyst work samples | https://yardstick.team/work-samples/effective-work-sample-exercises-for-hiring-top-hr-data-analysts | hiring guide [G] | headcount by department, average tenure by rating, above-average turnover |
| 13 | OneUptime ClickHouse HR/people analytics (Mar 2026) | https://oneuptime.com/blog/post/2026-03-31-clickhouse-hr-people-analytics/markdown | tutorial [G] | monthly attrition by department, tenure bands, NULLIF guard |
| 14 | Study doc "SQL questions to solve for HR analytics" (Studocu) | https://www.studeersnel.nl/it/document/dr-apj-abdul-kalam-technical-university/data-analytics/sql-questions-to-solve-for-hr-analytics/121988855 | student doc, unverified | attrition by dept/role, tenure leavers vs stayers |
| 15 | Existing repo research | research/interview_processes.md | internal | SQL dominant (about 19 of 20 profiles); HSBC Hyderabad round on SQL + banking; PhonePe "LeetCode hard"; Meesho "moderate to tough" |

## Pattern tally (from the above, indicative)
| Pattern | Sources | Company type | Recency | Star given |
|---|---|---|---|---|
| Customers with no orders (LEFT JOIN) | 2, search results | e-com/all | 2025 | 3 |
| Revenue per category/customer, top customers | 1, 2, 9 | e-com, product | 2025 | 3 |
| Above-department-average salary / headcount by department | 2, 12 | service MNC, all | 2025 | 3 |
| Monthly revenue | 2 | all | 2025 | 3 |
| Final account balance from deposits/withdrawals | 10, 11 | banks/GCC | undated | 3 |
| Attrition rate, tenure | 12, 13, 14 | HR analytics, GCC | 2026 | 3 (HR switcher focus) |
| Orders/items, first order per customer | 9 | Amazon | old | 2 |
| Loans, dormant accounts, fraud-like bursts | 10, 15 (bank rounds) | banks | undated | 1-2, gap-filled |

## Not found / blocked
- No first-hand Swiggy/Flipkart/PhonePe/Meesho/HSBC/JPMorgan/Wells Fargo SQL question wording was retrieved; only round formats. Interview Query pages were not fetched (not opened).
- Scribd and Telegram uploads are user-made and unverified; used only as hints.
- Many questions (loans, ATM limits, overtime, leave overlap, Pareto, basket pairs) are gap-fills by the author from standard business patterns, not from a cited source.
