# Book 4 Part 2 sources (Power Query transformations in Power BI)
Accessed 2026-10-24. 8 web searches run (snippet-level results only) and 8 pages fetched in full via WebFetch (7 returned content, 1 returned 404). No first-hand Hyderabad/Bengaluru 2025-26 interview report specific to Power Query was found; company attributions are unverified. Sample size: 8 searches, about 60 result links seen, 7 pages read in full, plus the existing research files below.

## Fetched in full (official Microsoft Learn)
| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| Query evaluation and query folding | https://learn.microsoft.com/en-us/power-query/query-folding-basics | folding definition, full/partial/no folding, CSV/Excel do not fold, View Native Query availability, steps can be reordered | official docs | updated 2026-08 |
| Incremental refresh overview | https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview | RangeStart/RangeEnd (reserved, case-sensitive, date/time), manual filter steps, folding needed, Pro and Premium support, 2h/5h refresh limits | official docs | updated 2026-07 |
| Power Query best practices | https://learn.microsoft.com/en-us/power-query/best-practices | filter early, expensive steps last, correct data types, profiling tools, parameters, custom functions, extract previous, resilient transformations | official docs | 2026-08 |
| Error handling (try/otherwise/catch) | https://learn.microsoft.com/en-us/power-query/error-handling | try otherwise, catch, error record fields | official docs | 2025-07 |
| Unpivot columns | https://learn.microsoft.com/en-us/power-query/unpivot-column | three unpivot options and refresh behaviour with new columns | official docs | 2025-07 |
| Merge queries overview | https://learn.microsoft.com/en-us/power-query/merge-queries-overview | six join kinds, same data type needed, multi-column keys, expand/aggregate, fuzzy matching only for text | official docs | 2026-04 |
| Data Privacy Firewall | https://learn.microsoft.com/en-us/power-query/data-privacy-firewall | privacy levels compatibility, Formula.Firewall errors, Ignore privacy levels option | official docs | updated 2026-08 |
| Folder connector | https://learn.microsoft.com/en-us/power-query/connectors/folder | Combine & Transform, sample file drives structure, same structure needed, filter files first | official docs | updated 2026-10 |

Fetch that failed: https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-privacy-levels (HTTP 404; privacy content taken from the Data Privacy Firewall page instead).

## Search results (snippet only, pages not fetched)
| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| FanRuan Power BI interview questions | https://www.fanruan.com/en/blog/power-bi-interview-questions | DA scope: Power Query, measures, data preparation | prep blog | 2026 |
| KORE1 Power BI developer interview article | https://www.kore1.com/power-bi-developer-interview-questions/ | "where does each Power Query step execute" (folding) | recruiter blog | Oct 2026 |
| Simpliaxis Power BI interview Q&A | https://www.simpliaxis.com/resources/power-bi-interview-questions-and-answers | currency-conversion scenario, folding + performance pairing | training site | 2026 |
| Glassdoor EY intern review | https://www.glassdoor.sg/Interview/EY-Interview-E2784-RVW96161308.htm | scheduled vs incremental refresh asked (one anecdote, content not detailed) | interview review | undated in snippet |
| Glassdoor Power BI question listing | https://static-pc.glassdoor.fr/Interview/power-bi-interview-questions-SRCH_KO0,8_IP57.htm | "What is query folding, how can we identify whether a query is folded" | crowd listing | undated |
| RADACAD Append vs Merge | https://radacad.com/append-vs-merge-in-power-bi-and-power-query/ | merge adds columns, append adds rows, same columns for append | expert blog | undated |
| Pragmatic Works PL-300 merge vs append | https://pragmaticworks.com/blog/preparing-to-pass-pl-300-certification-exam-merging-vs.-appending-queries-in-power-bi | merge/append as core exam topic | training blog | undated |
| GeeksforGeeks merge and append | https://geeksforgeeks.org/merge-and-append-queries-in-power-bi | join vs UNION ALL analogy | prep site | undated |
| Towards Data Science: duplicate vs reference | https://towardsdatascience.com/the-difference-between-duplicate-and-reference-in-power-query/ | reference vs duplicate, circular-reference limit | blog | undated |
| Fabric Community query folding thread | https://community.fabric.microsoft.com/t5/Desktop/Query-Folding-Transformation/m-p/4245897 | custom columns and cross-source merges can break folding | forum | 2024 |
| Fabric Community Table.Buffer thread | https://community.fabric.microsoft.com/t5/Desktop/How-do-I-buffer-my-table-in-Power-Query/m-p/778124 | Table.Buffer with sort + distinct (forum workaround, not official) | forum | undated |
| Adaface Power BI interview questions | https://adaface.com/blog/power-bi-interview-questions | incremental vs full refresh, multi-source cleaning, data privacy questions | vendor blog | undated |
| RADACAD combine sheets | https://radacad.com/combine-multiple-or-all-sheets-from-an-excel-file-into-a-power-bi-solution-using-power-query-dynamically | combine sheets/files technique | expert blog | undated |
| Parallels / AceCloud Power BI on Mac | https://www.parallels.com/blogs/power-bi-on-mac/ | Desktop (incl. Power Query Editor) is Windows-only; vendor pages, not Microsoft | vendor blog | undated |
| Zero To Mastery, Imarticus, Jaro, Analytics Vidhya lists | https://zerotomastery.io/blog/power-bi-interview-questions-and-answers/ | generic list: M language, referencing vs duplicating, error handling, remove duplicates | prep blogs | 2024-26 |

## Existing repo research used
- research/interview_processes.md: Deloitte USI Hyderabad Power BI round (RLS, optimisation, SUM vs SUMX), Wipro (DAX), Infosys, Cognizant, Microsoft, HSBC: Power BI appears; none of the reports name Power Query specifically. Anecdotes only.
- research/jd_sample_*.md and research/market_skills_2026.md: Power Query appears as a good-to-have in about 4.8% (Bengaluru) and 8.5% (Hyderabad) of sampled JDs (e.g. StatusNeo Junior Power BI Analyst, Nova Technologies, EBG Group, PwC USI); Power BI 32.5% of 40-JD sample, 40% pooled.

## Star reasoning
- ⭐⭐⭐: concepts every Power BI interview touches and every source list repeats (what Power Query is, merge vs append, join kinds, remove duplicates, data types, nulls, cleaning, Load vs Transform, folder combine, query folding which Glassdoor/KORE1/Simpliaxis all raise, Power Query vs DAX column). Power Query is a stated skill in JDs, but at low frequency, so only core items get three stars.
- ⭐⭐: common practical tasks and difference questions (unpivot, reference vs duplicate, parameters, errors, performance, anti join, locale dates, latest record per employee).
- ⭐: differentiators for 8-10 LPA or developer-leaning roles (fuzzy match, custom functions, RangeStart/RangeEnd, privacy levels/firewall, native query, Table.Buffer, dataflows, Mac limitation).

## Notes and limitations
- Glassdoor, AmbitionBox, Reddit and LinkedIn firsthand reports: not surfaced by search or not fetched; no Power Query-specific company report verified.
- Gap-fills (not seen in any source, written from standard practice and HR scenarios): about 38 of 63, mainly the practical "how would you do X" items (tenure band, attendance unpivot, missing-from-attendance anti join, latest record per employee, department-name cleaning, locale dates, Fill Down, Group By, Column Quality tools, Query Dependencies, Column From Examples, staging structure, resilient column-name handling).
- Unverified specifics to confirm before Wave B answers: exact menu names in current Power BI Desktop builds (Transform data, Enable load, Using Locale), the "column profiling based on entire data set" option, DirectQuery limits on transformations (deliberately not asked), and that dataflow privacy levels are unavailable (stated on the Data Privacy Firewall page).
- Boundary choices: incremental refresh policy setup and gateways belong to Part 7; query-folding-driven report performance scenarios belong to Part 9; relationships and star schema to Part 3.
