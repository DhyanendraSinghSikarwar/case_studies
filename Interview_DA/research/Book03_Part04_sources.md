# Book 3 Part 4 sources (pandas: read, select, filter, sort)
Accessed 2026-11-09 via WebSearch (snippet-level only). WebFetch was not used; no page was read in full. 9 searches run: 6 returned results, 3 returned a rate-limit error (no results; their summaries were model-knowledge only and are NOT cited as sources). Sample size: about 100 result links across 6 searches, none read in full. No first-hand Hyderabad/Bengaluru 2025-26 report of pandas read/select/filter questions was found; company attributions beyond those below are unverified.

| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| AskPython 50 pandas interview questions | https://www.askpython.com/?p=65508 | common pandas question set (snippet) | prep blog | 2026 |
| GoLinuxCloud pandas interview questions | https://www.golinuxcloud.com/pandas-interview-questions/ | screens centre on groupby, merge, missing data; check row counts (snippet) | prep blog | undated |
| InterviewBit python/pandas questions for data analyst | https://www.interviewbit.com/python-interview-questions-for-data-analyst/ | basic/experienced/coding split (snippet) | prep site | undated |
| DataCamp top pandas interview questions | https://www.datacamp.com/blog/top-python-pandas-interview-questions-and-answers | loc vs iloc, read_csv, filtering (snippet) | prep blog | updated Dec 2025 |
| Analytics Vidhya 60 Python questions for data analyst | https://www.analyticsvidhya.com/blog/2025/07/python-interview-questions-for-data-analyst/ | DA-level Python/pandas basics (snippet) | prep blog | 2025-07 |
| Interview Kickstart pandas interview questions | https://interviewkickstart.com/blog/interview-questions/pandas-interview-questions | coding-style tasks such as sorting DataFrames (snippet) | prep blog | undated |
| Glassdoor: Data Analyst Intern interview (Jar, India) | https://static.glassdoor.de/Interview/data-analyst-intern-interview-questions-SRCH_KO0,19_IP120.htm | live-coding round with screen share (snippet) | candidate report | undated |
| Adaface pandas interview questions | https://adaface.com/blog/pandas-interview-questions | Series vs DataFrame as early question; new column from conditions (snippet) | assessment vendor | undated |
| Board Infinity: Tiger Analytics data analyst guide | https://discuss.boardinfinity.com/t/tiger-analytics-data-analyst-interview-questions-experience-guide/23664 | "be fluent with pandas for data wrangling" (snippet) | candidate report | undated |
| Glassdoor Tiger Analytics report | https://static.glassdoor.co.in/Interview/Tiger-Analytics-Interview-E717029-RVW88618677.htm | opening question "what is a dataframe in pandas" (snippet, as relayed by search summary) | candidate report | undated |
| pandas docs: DataFrame.nlargest | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.nlargest.html | nlargest vs sort_values().head() (snippet) | official docs | current |
| Lerner Python: nlargest vs sort_values | https://lernerpython.com/2026/01/15/pandas-nlargest-finding-top-rows-faster-than-sort-values/ | same comparison (snippet) | blog | 2026-01 |
| OneUptime: Fix SettingWithCopyWarning | https://oneuptime.com/blog/post/2026-01-25-fix-settingwithcopywarning-pandas/markdown | pandas 3.0 Copy-on-Write removes the warning (snippet) | blog | 2026-01 |
| PDEP-7 Copy-on-Write | https://pandas.pydata.org/pdeps/0007-copy-on-write.html | CoW background (snippet) | pandas proposal | current |
| Internal: research/interview_processes.md, research/market_skills_2026.md, research/jd_sample_*.md | (repo) | Python in 35% of the 0-2 yr JD sample; basic Python/pandas in service-MNC and analytics-firm reports (Infosys, Tiger Analytics, JPMorgan Hyderabad, HSBC Hyderabad) | prior research | 2026 |

Star-assignment reasoning
- Three stars: read_csv, head/info/shape, column selection, loc vs iloc, boolean filtering (including & vs and), sorting, new column, SettingWithCopyWarning, KeyError. These recur in every pandas guide above and match the fresher-level Tiger Analytics/Board Infinity reports. Inference from guides, not a measured frequency.
- Two stars: isin, str filters, query, index handling, read_csv options, saving, np.where, nlargest, common read errors. Frequent follow-ups in the guides.
- One star: at/iat, MultiIndex, chunks, categorical sorting, where/mask, Copy-on-Write in pandas 3.0, memory. Differentiators.

Notes
- Blocked or unreachable: Glassdoor/AmbitionBox/GfG/Reddit full pages not fetched; Cognizant and Infosys searches returned no pandas-specific questions. A Reddit/MIS-focused search hit the rate limit.
- Overlap check: question_index.md rows for Books 1, 2, 4, 5 reviewed by grep for pandas; Book 5 Part 11 owns describe, value_counts percentage, fillna, groupby mean; Book 2 owns merge/cumsum equivalents. None repeated here.
- Gap-fills: about 35 of the 75 questions (e.g. usecols, chunks, idxmax, transpose, where/mask, memory, display options, reorder columns) are standard-practice composites without a direct source. Target was 70.
