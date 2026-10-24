# Book 4 Part 9 sources (scenario tasks: build HR/sales dashboard, fix slow report, reconcile numbers)
Accessed 2026-10-24. 7 web searches run (1 returned a rate-limit error: "Power BI HR dashboard attrition headcount DAX measures"; that query's results are NOT used, only my own general knowledge, marked below) and 5 Microsoft Learn pages fetched (the fetch tool returns a summarised/converted page; the pages came back in full). No first-hand Hyderabad/Bengaluru 2025-26 interview report describing a Power BI scenario task was found; city and company attributions are unverified.

| Source | URL | Used for | Type | Recency | Fetch status |
|---|---|---|---|---|---|
| Microsoft Learn: Optimization guide for Power BI | https://learn.microsoft.com/en-us/power-bi/guidance/power-bi-optimization | slow-report checks: restrictive filters, Top N, fewer visuals, drill-through/tooltips, capacity, gateway, latency; dashboard tile caching and RLS | official docs | page updated 2026-04 | fetched in full |
| Microsoft Learn: Performance Analyzer | https://learn.microsoft.com/en-us/power-bi/create-reports/performance-analyzer | DAX query / visual display / Other durations, copy query to DAX query view, also in service edit mode | official docs | page updated 2026-07 | fetched in full |
| Microsoft Learn: Import data reduction | https://learn.microsoft.com/en-us/power-bi/guidance/import-modeling-data-reduction | remove columns/rows, summarise, data types, calculated vs Power Query columns, auto date/time, DirectQuery/composite | official docs | page updated 2026-01 | fetched in full |
| Microsoft Learn: Incremental refresh overview | https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview | RangeStart/RangeEnd, query folding need, Pro vs Premium (real-time DirectQuery partition Premium only), 2h Pro / 5h Premium refresh limits | official docs | page updated 2026-07 | fetched in full |
| Microsoft Learn: Date tables | https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables | mark as date table, validation rules (unique, no nulls, contiguous), auto date/time | official docs | page updated 2026-10 | fetched in full |
| FanRuan Power BI interview questions | https://www.fanruan.com/en/blog/power-bi-interview-questions | scenario themes: sales performance, executive dashboard, slow dashboard, inconsistent sources, schema changes, inventory alerts | vendor blog | 2026 | search snippet only |
| Techcanvass: How to optimise Power BI reports | https://businessanalyst.techcanvass.com/how-to-optimise-power-bi-reports/ | interview-style slow-report answer (Performance Analyzer first, then model/DAX/visuals) | training blog | undated | search snippet only |
| Tabular Editor: report optimization for beginners | https://tabulareditor.com/blog/power-bi-report-optimization-for-beginners | slow-report fixes | vendor blog | undated | search snippet only |
| SQLBits 2020 session "My Power BI report is slow" | https://sqlbits.com/Sessions/Event20/My_Power_BI_report_is_slow_what_should_I_do | Performance Analyzer + DAX Studio workflow | conference page | 2020 | search snippet only |
| Medium: Power BI scenario-based interview questions Part 1 | https://medium.com/@rajesh_data_ai/power-bi-scenario-based-interview-questions-part-1-fa79e58766cf | star schema multi-region sales, slow report, RLS, refresh, DAX troubleshooting | blog | undated | search snippet only |
| Microsoft Fabric Community threads on Power BI vs Excel totals | https://community.fabric.microsoft.com/t5/Power-Query/Totals-and-Percentages-in-PowerBI-do-not-match-with-Excel-Pivot/m-p/3320812/highlight/true | causes of mismatch: filter context, different formulas, date logic, data types, relationships | community forum | undated | search snippet only |
| Telegram sqlspecialist Power BI interview challenges | https://t.me/s/sqlspecialist/2962 | YoY, YTD, MTD, top N style tasks | social post | undated | search snippet only (low quality) |
| Ecosire / thebricks RLS guides | https://www.thebricks.com/resources/guide-how-to-set-row-level-security-in-power-bi | dynamic RLS with mapping table and USERPRINCIPALNAME, Build permission bypass | vendor blogs | 2025 | search snippet only |
| research/interview_processes.md (repo) | n/a | Deloitte Power BI round (RLS, optimisation, SUM vs SUMX), Wipro DAX, Cognizant RLS, Infosys, Wells Fargo Tableau | internal research file | 2025-26 | read in full (relies on Glassdoor snippets, unverified mapping) |
| research/jd_sample_*.md, market_skills_2026.md (repo) | n/a | Power BI in 32.5-45% of sampled JDs, DAX 2-7%, HR/people analytics roles, MIS/WFM reporting roles | internal research | 2026 | grep-read |

## Star reasoning
- Stars here reflect how often a scenario type is asked, since these are open tasks rather than definitions.
- 3 stars (13): "walk me through a dashboard you built", build-a-dashboard steps, KPI choice, "report is slow", Performance Analyzer, "numbers don't match", YoY, star-schema model, RLS for departments. Slow report/optimisation, RLS and project workflow are named in the Deloitte report; scenario lists in every prep source include slow dashboard and sales/performance dashboards; dashboard/reporting appears in most sampled JDs.
- 2 stars (44): common follow-on build, fix and reconcile tasks, DAX tasks (MTD/YTD, attrition, headcount), refresh/sharing failures, Mac limitation.
- 1 star (18): differentiators (DAX Studio, incremental refresh, query folding, cohort retention, what-if, paginated reports, OLS).
- Difficulty: 🟢 describe-a-process, 🟡 write a measure or debug, 🔴 multi-step design or reconciliation.

## Gap-fills
About 45 of 75 questions are not seen as questions in any source: all HR-flavoured ones (attrition, headcount waterfall, tenure, probation, payroll, overtime, attendance, hiring funnel, joiner cohort) and the Mac/shared-user/sharing items were written from standard practice for the HR career-switcher reader. The failed HR-DAX search means the HR measure designs are from my general knowledge and must be verified in Power BI Desktop at answer-writing time.

## Not accessed / limitations
- Glassdoor, AmbitionBox, Reddit, LinkedIn pages were not fetched (blocked or not surfaced); only search snippets and the repo's earlier research are used for company claims.
- Sample: 7 searches, 5 full fetches; most scenario-question evidence is blog/community level, not first-hand interview reports.
- Mac limitation and licence differences (free vs Pro/PPU/Fabric) are from general knowledge in this part, not fetched here: verify against Microsoft Learn in Wave B.
