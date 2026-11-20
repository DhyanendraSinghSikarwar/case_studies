# Book 5 Part 11 sources (Stats in Excel & Python)
Accessed 2026-11-05 via WebSearch (snippet-level only). WebFetch of analyticsvidhya.com and support.microsoft.com failed (host not in the session's allowed network domains), so NO page was fetched in full. 7 searches were attempted; 2 returned a rate-limit error and 1 further search was run; 6 returned usable results. No first-hand Hyderabad/Bengaluru report of Excel/Python statistics questions was found; company attributions are unverified and none are made.

| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| Analytics Vidhya 50+ Excel interview questions | https://www.analyticsvidhya.com/blog/2024/01/comprehensive-guide-to-excel-interview-questions/ | Excel function-level question types (snippet) | prep blog | updated 6 Jan 2026 |
| Interview Query Excel DA questions | https://interviewquery.com/p/excel-data-analyst-questions | Excel DA question set (title/snippet only) | prep guide | undated |
| Minova junior DA guide | https://www.minova.ai/blog/interview/junior-data-analyst-interview-questions-complete-guide | Essentials list (lookup, IF, SUMIF) | prep blog | Nov 2025 |
| Jobdexo 2026 DA guide | https://jobdexo.com/blog/top-25-data-analyst-interview-questions-with-answers-2026-guide-2026 | General DA question mix | prep blog | 2026 |
| Scribd Excel FAQ uploads | https://www.scribd.com/document/866454332/Excel-Interview-FAQS | COUNT vs COUNTA vs COUNTBLANK; FORECAST/TREND | user upload (weak) | undated |
| Medium pandas cheat sheet for DAs | https://medium.com/@shirley_peng/the-python-pandas-interview-cheat-sheet-for-data-analysts-347f65479c86 | describe(), corr(), groupby questions | blog | undated |
| GoLinuxCloud / Adaface / Hyring pandas question lists | https://www.golinuxcloud.com/pandas-interview-questions/ | groupby, corr, select_dtypes, VIF | prep sites | undated |
| Analytics Vidhya 60 Python DA questions | https://www.analyticsvidhya.com/blog/2025/07/python-interview-questions-for-data-analyst/ | Python DA question set (snippet only) | prep blog | July 2025 |
| CASRAI Excel statistics functions | https://casrai.org/guides/excel-statistics-functions | STDEV.S (n-1) vs STDEV.P; FORECAST.LINEAR | reference | undated |
| Microsoft statistical functions reference | https://support.microsoft.com/en-us/excel/statistical-functions-reference | PERCENTILE.INC/EXC, QUARTILE, CORREL names (snippet) | official docs | undated |
| AmbitionBox Data Analyst question bank | https://ambitionbox.com/profiles/data-analyst/interview-questions?page=2 | Python library and VLOOKUP-style questions; no stats-function items seen | candidate-reported | page updated 2 Mar 2025 |
| Glassdoor DataBeat review (Hyderabad-tagged) | https://www.glassdoor.co.uk/Interview/DataBeat-Interview-E3301042-RVW102633903.htm | one report: about 80% SQL, 20% Python | candidate-reported (snippet) | undated |
| Goskills / Noble Desktop ToolPak guides | https://goskills.com/Excel/Resources/Excel-data-analysis-toolpak | ToolPak descriptive stats, regression, t-test types | tutorial | undated |
| numpy vs pandas std (Gorelik; SO mirror) | https://gorelik.net/2017/11/06/numpy-vs-pandas-functions-that-look-the-same-share-the-same-code-but-behave-differently | np.std ddof=0 vs pandas ddof=1; NaN handling | blog | 2017 |
| Telegram dataanalystinterview | https://t.me/s/dataanalystinterview/731 | junior DA question flavour (Excel cleaning, Python report automation), snippet | community channel | undated |

Notes
- Sample size: about 7 usable search result sets, all snippet-level. Limitation: sources are generic prep material; evidence that these specific function questions are asked in Hyd/Blr loops is weak. Blocked/not surfaced: Glassdoor/AmbitionBox full pages, Reddit, LinkedIn (not fetched).
- Two scipy/ToolPak searches failed with rate limits; their content (ttest_ind equal_var, chi2_contingency, ToolPak) comes from standard practice, unverified here.
- Star reasoning: 3 stars for the functions every Excel/pandas analyst interview touches (mean/median/mode, describe, COUNT family, groupby, STDEV.S vs P, correlation), supported by the generic guides. 2 stars for percentiles, outliers, missing values, pivot, regression, t-test, chi-square, CI: stats is named in 20% of the 40 JDs (market_skills_2026.md) and Accenture Bangalore reported "basic statistics" (interview_processes.md). 1 star for distribution functions, covariance, skew, sampling, forecast.
- Gap-fills: about 20 of 34 questions come from standard practice rather than a named source (all 1-star items, the inferential-test, CI, regression and outlier items, ddof and z-score).
