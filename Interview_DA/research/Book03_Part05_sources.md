# Book 3 Part 5 sources (pandas: groupby, merge, pivot, apply)
Accessed 2026-11-09 via WebSearch (snippet/summary level only). No page was fetched in full (WebFetch not used). 8 searches were run: 6 returned results, 2 hit a "too_many_requests" error (the summaries returned for those two came from model knowledge, not sources, and are NOT cited as evidence). Sample size: 6 successful searches, about 90 result links, none read in full. No first-hand 2025-26 Hyderabad/Bengaluru report specific to groupby/merge was found; company attributions below are unverified beyond the snippets.

| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| GoLinuxCloud pandas interview questions | https://www.golinuxcloud.com/pandas-interview-questions/ | standard question set (snippet) | prep blog | undated |
| PracHub: pandas interview questions for data analysts (joins, GroupBy, messy data) | https://prachub.com/resources/pandas-interview-questions-for-data-analysts-joins-groupby-and-messy-data | join cardinality, groupby denominators, size vs count (snippet) | prep site | 2026 |
| PracHub: use pandas to aggregate, pivot and label | https://prachub.com/interview-questions/use-pandas-to-aggregate-pivot-and-label | merge+groupby+pivot+flag combined task (snippet) | practice question | 2026-03 |
| PapersAdda pandas interview questions 2026 | https://papersadda.com/article/pandas-interview-questions-2026/ | groupby+merge business scenarios as common live-coding (snippet; anecdotal claim) | prep blog | 2026 |
| Dataford: filtering, grouping, merging, applying functions | https://dataford.io/questions/how-would-you-explain-pandas-filtering-grouping-merging-and-applying-functions | question variety (snippet) | practice platform | undated |
| Naukri Code360 / InterviewBit / Flexiple / ConsoleFlare / Hyring / Adaface / LabEx pandas lists | https://www.naukri.com/code360/library/pandas-interview-questions | merge vs concat, merge vs join, pivot_table, loc/iloc (snippet) | question banks | 2024-2026 |
| Towards Data Science: groupby vs pivot | https://towardsdatascience.com/a-comparison-of-groupby-and-pivot-in-pythons-pandas-module-527909e78d6b | pivot vs pivot_table, groupby vs pivot_table (snippet) | blog | undated |
| Towards Data Science: apply vs map vs applymap | https://towardsdatascience.com/apply-vs-map-vs-applymap-pandas-529acdf6d744 | apply/map/applymap difference, vectorisation (snippet) | blog | undated |
| Towards Data Science: apply vs vectorized operations | https://towardsdatascience.com/efficient-pandas-apply-vs-vectorized-operations-91ca17669e84/ | apply slowness (snippet) | blog | undated |
| freeacademy: named aggregation and window patterns | https://freeacademy.ai/lessons/pandas-named-aggregation | named agg, rank, cumsum, shift within groups (snippet) | lesson | undated |
| Glassdoor: Tiger Analytics interview reviews (e.g. RVW88618677) | https://static.glassdoor.co.in/Interview/Tiger-Analytics-Interview-E717029-RVW88618677.htm | pandas data manipulation and imputation in technical round (snippet only) | candidate report | 2024-2026 |
| Glassdoor: Infosys first-round report | https://static.glassdoor.com.ar/Interview/Infosys-Interview-Questions-E7927_P44.htm | pandas basics asked (load CSV/Excel, drop empty values) (snippet only) | candidate report | undated |
| Interview Query: Tiger Analytics data analyst guide | https://interviewquery.com/interview-guides/tiger-analytics-data-analyst | Python/pandas emphasis (snippet) | guide | 2025 |
| Internal: research/market_skills_2026.md, research/interview_processes.md, research/jd_sample_*.md | (repo) | Python 32% of JDs pooled; Python mentions in ~10 company profiles | prior research | 2026 |

Star-assignment reasoning
- Three stars: groupby basics and aggregation, merge types, merge vs join vs concat, pivot_table, apply vs map, transform, top-N per group, anti join, row explosion, SettingWithCopyWarning, VLOOKUP via merge. These recur across nearly every list above and match the "groupby, merge, pivot, SQL analogy" framing. Frequency is inferred from prep sites, not measured.
- Two stars: standard follow-ups, HR-flavoured tasks (attrition, payroll, attendance) and common errors (KeyError, dtype after merge, key mismatch).
- One star: rarer or senior-leaning (merge_asof, rolling per group, cross join, observed, iterrows performance, reconciliation tasks).

Notes
- Blocked or limited: Glassdoor, GfG, AmbitionBox content seen only as search snippets; Cognizant returned nothing pandas-specific; two searches rate-limited.
- Overlap check: Book 1 Part 4 covers Excel pivot tables only; Book 2 and Book 5 have no pandas groupby/merge rows. Part 4 (select/filter/sort) and Part 6 (cleaning) topics avoided.
- Gap-fills: 83 questions vs target 70; about 30 (e.g. cross join, observed, flatten MultiIndex, HR payroll/reconciliation tasks, melt, stack/unstack) are standard-practice gap-fills without a direct source. Version-dependent API (applymap renamed DataFrame.map in pandas 2.1) is from model knowledge, unverified here.
