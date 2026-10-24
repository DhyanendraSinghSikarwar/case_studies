# Book 4 Part 5 sources (DAX advanced: filter context, time intelligence, ALL vs ALLEXCEPT, RANKX, variables)
Accessed 2026-10-24 via WebSearch (8 searches, 7 returned results, 1 rate-limited) and WebFetch (3 pages fetched). No first-hand Hyderabad/Bengaluru 2025-26 DAX interview reports were found; company attributions come only from research/interview_processes.md and are unverified there too. Sample size: about 10 prep/tutorial pages plus the internal research files. Limitation: prep sites are not employer reports, so star ratings are judgement calls.

| Source | URL | Used for | Type | Recency | Fetch status |
|---|---|---|---|---|---|
| Weekday: 50 Power BI interview questions (2026) | https://www.weekday.works/post/power-bi-interview-questions | question coverage (filter/row context, CALCULATE, ALL/ALLEXCEPT/ALLSELECTED, % of total, FILTER vs Boolean, YTD/YoY, VAR, RANKX, USERELATIONSHIP, DATESINPERIOD, Top 5 + Others); interview format (live DAX round, write 3-5 measures) | India job platform prep | 2026 | fetched (summary via fetch model) |
| Microsoft Learn RANKX | https://learn.microsoft.com/en-us/dax/rankx-function-dax | syntax, Skip default, Dense, BLANK treated as 0, decimal precision caveat | official docs | updated 2026-01 | fetched in full |
| SQLBI: ALL vs ALLSELECTED vs ALLEXCEPT vs REMOVEFILTERS | https://www.sqlbi.com/articles/all-vs-allselected-vs-allexcept-vs-removefilters/ | behaviour of each; REMOVEFILTERS alias for ALL, modifier only; REMOVEFILTERS+VALUES over ALLEXCEPT | expert article | undated | fetched (summary via fetch model) |
| Microsoft Learn time intelligence functions | https://learn.microsoft.com/dax/time-intelligence-functions-dax | date table rules, DATESYTD/SAMEPERIODLASTYEAR/TOTALYTD | official docs | undated | search snippet only |
| Microsoft Learn: calculate ranks (training module) | https://learn.microsoft.com/en-us/training/modules/dax-power-bi-iterator-functions/3-calculate-ranks | RANKX with ALL | official training | undated | search snippet only |
| Fabric community: SAMEPERIODLASTYEAR/DATESYTD thread | https://community.fabric.microsoft.com/t5/Desktop/SAMEPERIODLASTYEAR-DATESYTD-different-from-DATESYTD/m-p/600099 | prior-year YTD pitfall (future dates) for the debug question | forum | 2019 | snippet only; anecdotal |
| Fabric community: RANKX ties | https://community.fabric.microsoft.com/t5/Desktop/RANKX-Ties-Question/m-p/3676323 | ties Skip vs Dense | forum | 2024 | snippet only |
| Fabric community: Question on DAX | https://community.fabric.microsoft.com/t5/Desktop/Question-on-DAX/m-p/2782964 | context transition in YoY | forum | 2022 | snippet only |
| PracHub DAX interview questions | https://prachub.com/resources/power-bi-dax-interview-questions-filter-context-calculate-and-correct-totals | KEEPFILTERS, non-additive totals, context transition | prep site | 2026 | snippet only |
| Topmate (Sai Sarthak) DAX 100 | https://topmate.io/sai_sarthak12/2234011 | ALL/ALLEXCEPT as common questions | prep listing | undated | snippet only |
| Telegram sqlspecialist challenge | https://t.me/s/sqlspecialist/2967 | RANKX with ALL/ALLSELECTED | social | undated | snippet only |
| interviewprep.org DAX | https://interviewprep.org/dax-data-analysis-expressions-interview-questions/ | context transition definition | prep site | undated | snippet only |
| Internal: research/interview_processes.md | n/a | Deloitte USI Power BI round (RLS, optimisation, SUM vs SUMX), Wipro DAX (SUM, SUMX, DATEDIFF, AVG), ALL vs ALLEXCEPT, incremental refresh | internal research | 2025-26 | read in full for DAX lines |
| Internal: research/market_skills_2026.md and jd_sample_*.md | n/a | DAX appears in about 5-7.5% of JDs (e.g. Takeda Bengaluru, Cummins, TopGrep Blr/Hyd list DAX) so the part is trimmed to advanced practical items | internal research | 2026 | grep only |

Star reasoning
- ⭐⭐⭐: filter vs row context, ALL vs ALLEXCEPT (named in interview_processes.md and in nearly every prep list), date table, YTD, YoY, % of total, RANKX, context transition, VAR (present in Weekday list and most DAX sets; a live DAX round typically asks these measures).
- ⭐⭐: ALLSELECTED, REMOVEFILTERS, TOTALYTD, DATEADD, rolling average, running total, USERELATIONSHIP, ties, Top N, non-additive totals, debugging (listed in sources but less universal); HR measures (attrition, headcount, DATEDIFF tenure) are ⭐⭐ because Wipro reports DATEDIFF and the reader is an HR switcher.
- ⭐: KEEPFILTERS, REMOVEFILTERS+VALUES, semi-additive, FILTER performance, DAX Studio, calculation groups, visual calculations (differentiators; visual calculations is a newer feature, availability to be verified in answers).

Notes
- Gap-fill questions (not seen in any source, from standard practice): HR attrition rate, headcount at month end, DATEDIFF tenure, MTD/QTD, running total, RANKX returns 1 on every row, semi-additive closing balance, FILTER-slowness rewrite, Performance Analyzer/DAX Studio, visual calculations: 10 of 36.
- Blocked/not accessible: Glassdoor, AmbitionBox, Reddit (no result surfaced; not fetched). One search hit the rate limit.
- Unverified: exact current availability and licensing of calculation groups (Desktop/Tabular Editor) and visual calculations; check in Wave B.

## Gap-fills added after de-duplication
Four questions added to reach the target of 35 (none seen in a source list; chosen from standard DAX practice after checking Parts 3, 4, 5 and 9 headings for overlap). Behaviour checked on Microsoft Learn (accessed 2026-10-24): TOTALYTD (https://learn.microsoft.com/en-us/dax/totalytd-function-dax), ISINSCOPE (https://learn.microsoft.com/en-us/dax/isinscope-function-dax), EARLIER (https://learn.microsoft.com/en-us/dax/earlier-function-dax).
- How do you make TOTALYTD follow an Indian financial year that ends on 31 March? (stars 2) Learn confirms the optional year_end_date string such as "3/31" ("month/day" recommended, year ignored, default 31 Dec, not allowed with calendar-based time intelligence). Part 5 Q4 covers plain YTD and Part 9 Q37 covers the fiscal-year dashboard scenario, not the TOTALYTD argument.
- What does EARLIER do in a calculated column, and how can variables replace it? (stars 2) Learn describes EARLIER as mostly for calculated columns and warns of slow performance; its rank example is COUNTROWS(FILTER(...EARLIER...))+1. Not present elsewhere in Book 4.
- Write a measure for the average monthly sales in a selected year (average of monthly totals). (stars 2) Standard AVERAGEX over VALUES pattern; Part 4 covers AVERAGEX only conceptually.
- What does ISINSCOPE do, and how do you use it to show a different calculation at each level of a matrix hierarchy? (stars 1) Learn gives a SWITCH(TRUE(), ISINSCOPE(...)) percent-of-parent example. Differentiator, hence one star.
