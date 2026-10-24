# Book 4 Part 4 sources (DAX basics: calculated column vs measure, SUM vs SUMX, COUNT family, CALCULATE, row vs filter context)
Accessed 2026-10-24. 7 distinct web searches and 6 page fetches. Sample is small: one fully fetched India prep article, four fully fetched Microsoft Learn pages, and search snippets for the rest. No first-hand Hyderabad/Bengaluru 2025-26 interview report beyond the single Deloitte review below was found; company attributions are unverified.

| Source | URL | Used for | Type | Recency | Fetched? |
|---|---|---|---|---|---|
| Weekday: 50 Power BI interview questions (2026), DAX examples | https://www.weekday.works/post/power-bi-interview-questions | question list (calc column vs measure, row/filter context, CALCULATE, SUM vs SUMX, COUNT family, DIVIDE, FILTER vs Boolean filter, "same total in every row"); interview format (theory round, live DAX round of 3-5 measures, take-home) | India job platform prep article | 2026 | fetched in full (via summarising fetch) |
| Microsoft Learn: CALCULATE | https://learn.microsoft.com/en-us/dax/calculate-function-dax | filter rules (Boolean filters, overwrite vs add, context transition, not supported in DirectQuery calculated columns/RLS) | official docs | updated 2026-08 | fetched in full |
| Microsoft Learn: DIVIDE vs / operator | https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator | DIVIDE returns BLANK on zero/blank denominator; use / only for constant denominators | official docs | updated 2026-01 | fetched in full |
| Microsoft Learn: COUNTROWS | https://learn.microsoft.com/en-us/dax/countrows-function-dax | COUNTROWS behaviour; link to "use COUNTROWS instead of COUNT" best practice | official docs | updated 2026-01 | fetched in full (the best-practice page itself was not fetched) |
| Microsoft Learn: SUMX | https://learn.microsoft.com/en-us/dax/sumx-function-dax | iterator behaviour; "if you do not need to filter, use SUM"; ignores blanks/text | official docs | updated 2026-01 | fetched in full |
| Deloitte Bengaluru Glassdoor review (Jun 2025) | https://www.glassdoor.com.au/Interview/Deloitte-Interview-E10177265-RVW95876063.htm | reported DAX prompts: net sales from MRP/discount/net-sale columns; count unique customers across tables | candidate review (single anecdote, 3-5 yr role) | 2025 | search snippet only |
| Endjin: measures vs calculated columns | https://endjin.com/blog/measures-vs-calculated-columns-in-dax | stored-at-refresh vs query-time; model size and RAM | blog | 2022 | search snippet only |
| interviewprep.org DAX questions; Dataford "basic DAX vs SQL measures" | https://interviewprep.org/dax-data-analysis-expressions-interview-questions/ ; https://dataford.io/interview-guides/questions/basic-dax-vs-sql-measures | confirms question types exist (measure vs column, SUM vs SUMX) | prep sites | undated | search snippet only |
| prachub: Power BI DAX interview questions | https://prachub.com/resources/power-bi-dax-interview-questions-filter-context-calculate-and-correct-totals | filter context, CALCULATE, context transition, correct totals | practice site | undated | search snippet only |
| Microsoft Learn: Introduction to DAX; Context in DAX Formulas | https://learn.microsoft.com/en-us/training/modules/build-power-bi-report/4-introduction-dax | row vs filter context definitions | official docs | mixed (archived 2012 page also surfaced) | search snippet only |
| SQLBI: DIVIDE vs division operator | https://sqlbi.com/blog/marco/2014/07/24/divide-vs-division-operator-in-dax | DIVIDE rationale | expert blog | 2014 | search snippet only |
| COUNT-family comparison (Fabric community, thebricks, Microsoft DISTINCTCOUNT page) | https://learn.microsoft.com/dax/distinctcount-function-dax | COUNT/COUNTA/COUNTROWS/DISTINCTCOUNT differences | docs and community | mixed | search snippet only. One community thread contradicted documented blank handling; treat as unreliable, verify in Wave B |
| Existing research files | research/interview_processes.md, research/market_skills_2026.md, research/jd_sample_*.md | Wipro 2023 Bangalore-Rural report (DAX SUM, SUMX, DATEDIFF, AVG); Deloitte Sept 2025 Power BI round (SUM vs SUMX, RLS); Power BI in about 32.5% and DAX about 7.5% of 0-2 yr JDs | prior research | 2025-26 | read in full |

## Star reasoning
- ⭐⭐⭐: calculated column vs measure, SUM vs SUMX, COUNT family, CALCULATE, row vs filter context, and the core "write a measure" tasks. They appear in every prep list and in both company reports (Deloitte SUM vs SUMX; Wipro SUM/SUMX/AVG). The 2026 Weekday guide calls row vs filter context and CALCULATE the deciding concepts.
- ⭐⭐: iterators, context transition, CALCULATE argument behaviour, DATEDIFF tasks, net sales / unique customers tasks (Deloitte review), practical HR measures, VAR, DAX vs Excel/M comparisons.
- ⭐: errors, DirectQuery/Service/Mac limits, query view, visual calculations, housekeeping and niche write-a-measure tasks.
- Power BI is about 32.5% and DAX about 7.5% of 0-2 year JDs (market_skills_2026), so DAX depth stays modest and star 3 is kept to 17 of 75.

## Notes and limitations
- Blocked or not surfaced: Glassdoor beyond search snippets, AmbitionBox, Reddit, LinkedIn were not fetched; no Infosys/Cognizant DAX specifics found.
- Gap-fills (not seen in any source, added from standard practice and to meet the target): about 50 of 75, mostly practical measure tasks (attendance %, headcount, payroll, tenure, latest hire date), error questions, version/limit questions, and housekeeping.
- Unverified for Wave B to check against Microsoft docs: DAX authoring in Power BI Service (web model editing) and Mac limitation (Desktop is Windows-only), DISTINCTCOUNT blank handling, visual calculation and DAX query view availability and licensing, DirectQuery limits beyond CALCULATE in calculated columns/RLS.
- Part 5 boundary: ALL/ALLEXCEPT, time intelligence and RANKX excluded; only basic percent-of-total appears here.
