# Book 1 Part 7 sources (Power Query and Power Pivot)
Accessed 2026-10-21. 7 web searches (6 returned results, 1 rate-limited with no results) and 6 fetch attempts (3 succeeded, 3 returned HTTP 404). Search results are snippet-level summaries; only the fetched pages below were read. No first-hand Hyderabad/Bengaluru 2025-26 interview report specific to Power Query/Power Pivot was found; company attributions are unverified.

| Source | URL | Used for | Type | Recency | Fetch status |
|---|---|---|---|---|---|
| Microsoft Support: Where is Get & Transform (Power Query) | https://support.microsoft.com/en-us/office/where-is-get-transform-power-query-e9332067-8e49-46fc-97ff-f2e1bfa0cb16 | Version availability (2016+ Windows, 365, Mac via Get Data, Excel web limited, no mobile); fuzzy merge in 365 but not 2019 perpetual | official | undated | fetched in full |
| Microsoft Support: Calculated columns in Power Pivot | https://support.microsoft.com/en-au/excel/calculated-columns-in-power-pivot | Calculated column vs measure | official | undated | fetched in full |
| ExcelMojo: Query folding | https://www.excelmojo.com/query-folding-in-power-query/ | Query folding definition, what breaks it, how to check | training blog | undated | fetched in full |
| Glassdoor EY intern review (RVW96161308) | https://www.glassdoor.com/Interview/EY-Interview-E2784-RVW96161308.htm | Reported themes (Feb 2026 per search summary): transformations used, Merge vs Append, query folding, errors/nulls, Reference vs Duplicate | candidate review | 2026 | search snippet only, not fetched; single employer |
| Weekday Power BI questions 2026 and other Power BI guides (qandle, consoleflare, hipeople, DEV) | https://www.weekday.works/post/power-bi-interview-questions | Data model relationships, star schema, CALCULATE/ALL, calculated column vs measure frequency | prep sites | 2025-26 | search snippet only; Power BI-oriented, not Excel-specific |
| SumProduct: Power Pivot calculated field vs measure; RADACAD | https://sumproduct.com/blog/power-pivot-principles-calculated-field-vs-measure/ | Measure vs calculated column framing | blogs | undated | search snippet only |
| Query folding explainers (mssqltips, towardsdatascience, sumproduct) | https://www.mssqltips.com/sqlservertip/3635/query-folding-in-power-query-to-improve-performance-/ | Folding concept, conflicting views on unpivot folding | blogs/forums | undated | search snippet only |
| Glassdoor Mphasis Bengaluru review (RVW102279273) | https://www.glassdoor.com.br/Entrevista/Mphasis-Entrevista-E29275-RVW102279273.htm | One Power Query scenario question reported | candidate review | undated | search snippet only |
| Repo: research/jd_sample_hyderabad.md, jd_sample_bengaluru.md, jd_sample_mis_people.md | (local) | JD frequency: Power Query 4/47 (8.5%) Hyderabad, 2/42 (4.8%) Bengaluru, 4/32 (12.5%) MIS/people, all "good-to-have" | repo research | 2026 | read via grep |
| Repo: research/interview_processes.md, market_skills_2026.md | (local) | Wipro/Deloitte DAX topics (SUMX, ALL/ALLEXCEPT, Import vs DirectQuery); Excel 60% of JDs; DAX 5-7.5% | repo research | 2026 | read via grep |

Blocked / failed: Microsoft Support pages for "About Power Query in Excel" and "Power Pivot overview" and the calculated-columns office URL returned 404. Glassdoor/AmbitionBox/Reddit were not fetched (only snippets surfaced).

Star reasoning
- Power Query and Power Pivot are "good-to-have" in only 5-12% of JDs, so they are asked mostly in MIS/automation and BI-leaning roles. Stars are therefore relative within this part.
- 3 stars: the core "what is it / Power Query vs Power Pivot / Merge vs Append / refresh / folder combine / calculated column vs measure" set: present in every prep source and in the EY report.
- 2 stars: day-to-day cleaning steps, relationships, join kinds, errors/nulls, Reference vs Duplicate, DAX basics.
- 1 star: query folding (one source, EY), advanced DAX, parameters, privacy levels, Power BI migration, limits.

Notes
- Gap-fills (not seen in any source, written from standard practice): 41 of 64. The other 23 are backed by a theme in a source above (some via Power BI material, flagged as less Excel-specific; Import vs DirectQuery is a Power BI concept kept as a 1-star clarifier).
- Uncertain: whether unpivot folds on SQL sources (sources conflict); exact Data Model size limits (not verified, so no number is written into any question); Power Pivot availability by Excel edition (the Power Pivot overview page 404'd; answer writers must verify before stating it).
- Sample size: tiny for interview reports (one employer plus snippets); limitations apply to all star assignments.
