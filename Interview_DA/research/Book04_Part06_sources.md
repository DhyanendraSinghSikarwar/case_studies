# Book 4 Part 6 sources (visuals, slicers, drill-through, bookmarks, tooltips)
Accessed 2026-10-24. 8 web searches and 10 page fetches (9 successful, 1 returned 404). No first-hand Hyderabad/Bengaluru 2025-26 interview report specific to this topic was found; company-specific attributions below are unverified. Sample size: roughly 20 prep pages seen as search snippets, 9 Microsoft Learn pages read in full, plus the existing Power BI mentions in research/interview_processes.md.

## Official documentation (fetched in full, used for behaviour and feature facts)
| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| Drillthrough in Power BI reports | https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough | drillthrough page steps, buttons, troubleshooting (field not aggregated, must exist in source visual), cross-report requirements (same workspace, matching names/types, service only) | Microsoft Learn | updated 2026 |
| Create report bookmarks | https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-bookmarks | what a bookmark saves; Data/Display/Current page options; Selection pane; personal vs report bookmarks; limitations | Microsoft Learn | updated 2026 |
| Overview of slicers | https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicers | slicer types, slicers vs Filters pane, sync slicers, Select all inverted filter, Apply all/Clear all buttons, edit interactions, field parameters with slicers | Microsoft Learn | updated Oct 2026 |
| Create report tooltips | https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-tooltips | tooltip page set-up, tooltip fields, limitations (non-interactive, not on dashboards) | Microsoft Learn | updated 2026 |
| Conditional formatting in visuals | https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-conditional-formatting | gradient/rules/field value, colour measure, expression-based titles, NaN and DIVIDE note | Microsoft Learn | updated 2026 |
| Change how visuals interact | https://learn.microsoft.com/en-us/power-bi/create-reports/service-reports-visual-interactions | filter/highlight/none, drilling does not affect other visuals by default | Microsoft Learn | updated 2026 |
| Use drill mode | https://learn.microsoft.com/en-us/power-bi/explore-reports/end-user-drill | drill icons, next level vs expand, drill vs drillthrough | Microsoft Learn | updated 2026 |
| Format filters in reports | https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-filter | lock/hide filters, filter levels, Apply button | Microsoft Learn | updated 2026 |
| Field parameters | https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters | field parameters, limitation: cannot be drillthrough/tooltip linked fields | Microsoft Learn | updated 2026 |

Fetch that failed: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-cross-filter-highlight-visuals (404; the visual-interactions page above covers it).

## Prep and community pages (search snippets only, not fetched)
| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| Microtek / Simpliaxis / WeCreateProblems / Adaface / placementpreparation fresher lists | https://www.placementpreparation.io/blog/power-bi-interview-questions-for-freshers (others via search) | slicer vs filter, drill-through set-up, bookmarks, tooltips as standard fresher questions | prep blogs | 2024-2026, some undated |
| ZoomCharts, EPC Group, Basedash, thebricks drill pages | https://www.epcgroup.net/blog/power-bi-drill-down-drill-through-complete-guide-2026 | drill down vs drill through as frequent comparison | vendor blogs | 2025-26 |
| thebricks sync/unsync slicer guides | https://www.thebricks.com/resources/guide-how-to-unsync-slicers-in-power-bi | edit interactions None, sync pane | vendor blog | Oct 2025 |
| AmbitionBox, DataToBiz Power BI developer | https://www.ambitionbox.com/interviews/data-tobiz-interview-questions/power-bi-developer | one report (interview Mar 2024): slicer of top customers via disconnected table | candidate review (snippet) | 2024 |
| Codefinity chart-choice chapter and eduyush interview article | https://eduyush.com/blogs/interview-questions/power-bi-interview-questions | bar vs line vs pie choice logic | course/blog | undated |
| Taggd Power BI interview PDF | https://taggd.in/wp-content/uploads/2026/04/Power-BI-Interview-Questions-PDF.pdf | scenario prompts (executive dashboard, low adoption) | recruiter PDF | Apr 2026 |
| Telegram post (Bajaj Auto question list) | https://t.me/s/codingdidi?before=489 | "drilldown vs drill through" listed as asked; unofficial, answers absent | Telegram | undated, unverified |
| Existing report | research/interview_processes.md | Deloitte Power BI round, Cognizant 2022 report (slicers, filters, modelling, RLS), Wipro, Infosys, HSBC mentions | internal | 2025-26 |

Blocked or not reached: Glassdoor and AmbitionBox company pages were not fetched (search surfaced only one AmbitionBox page, snippet only); Reddit and LinkedIn posts not fetched.

## Star reasoning
- 3 stars: slicer vs filter, drill down vs drill through, filter levels, bookmarks, tooltips (all in nearly every fresher list and in the Cognizant 2022 "slicers, filters" report), plus the live build tasks (drill-through page, edit interactions, sync slicers, conditional formatting, slicer not filtering) and table vs matrix and chart choice (Power BI appears in about 40% of JDs; dashboard/reporting in most).
- 2 stars: other core visuals, filter types, hierarchies, buttons, bookmark options, report page tooltips, dynamic titles, HR build tasks (asked live often).
- 1 star: differentiators and edge cases (field parameters, cross-report drillthrough, Select all, limitations, accessibility, mobile layout).
- Difficulty is my own judgment.

## Gap-fills and uncertainty
- About 28 of 63 questions are gap-fills: not seen as a question in any source, added from standard practice and the Microsoft pages above (table vs matrix, pie/combo/scatter/line/area, hierarchy creation, Analytics pane, display units, themes, sort by column, attendance heat map, drill icons missing, attrition visuals, waterfall, custom visuals, mobile layout, accessibility, decomposition tree, blanks, show items with no data, the two red scenarios).
- "Keep all filters" on drill-through pages is a known Desktop toggle but was not described on the fetched page; verify the wording when answers are written.
- Microsoft pages are updated often and some UI names changed (Build pane, list slicer, input slicer); re-check at answer time.
- No evidence was found that these questions are asked at specific named companies beyond the generic Power BI mentions; do not attribute them to companies.
