# Book 3 Part 9 sources (EDA end-to-end tasks, live-coding style)
Accessed 2026-11-09 via WebSearch (snippet-level only). WebFetch was not used; NO page was fetched in full. Sample size: 8 searches attempted, 6 returned results (about 100 result links), 2 hit a rate limit (HR attrition case study; groupby/merge "first 5 minutes") and were re-run with narrower queries (merge/groupby India; IBM HR attrition EDA). Limitations: results are mostly prep blogs and anonymous review snippets; no first-hand Hyderabad/Bengaluru take-home report was found; Glassdoor/AmbitionBox/GfG pages appeared in results but were not opened. Company attributions are unverified.

| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| Glassdoor Pivigo question: "use pandas on basic data set and do exploratory data analysis" | https://www.glassdoor.es/Entrevista/Difference-between-continuous-and-discrete-random-variables-use-pandas-on-basic-data-set-and-do-exploratory-data-analysis-QTN_7681308.htm | EDA-with-pandas is asked as a live task (snippet) | candidate report | undated |
| PracHub: perform EDA and diagnose data quality | https://prachub.com/coding-questions/perform-eda-and-diagnose-data-quality | data-quality EDA task wording (snippet) | practice platform | undated |
| PracHub: pandas questions for analysts, joins, groupby, messy data | https://prachub.com/resources/pandas-interview-questions-for-data-analysts-joins-groupby-and-messy-data | merge row-count checks, groupby, messy data (snippet) | prep blog | undated |
| TechPrep: 74 EDA interview questions | https://www.techprep.app/blog/exploratory-data-analysis-interview-questions | EDA topic list (snippet) | prep blog | 2026 |
| PapersAdda pandas interview questions 2026 | https://papersadda.com/article/pandas-interview-questions-2026/ | topics; its "most reported" claim is unsourced, not relied on | prep blog | 2026 |
| InterviewBit Python for data analyst | https://www.interviewbit.com/python-interview-questions-for-data-analyst/ | question variety (snippet) | prep blog | 2024-25 |
| Analytics Vidhya 60 Python questions for DA | https://www.analyticsvidhya.com/blog/2025/07/python-interview-questions-for-data-analyst/ | analyst-level Python list (snippet) | blog | 2025 |
| Interview Query Python for DA | https://www.interviewquery.com/p/python-data-science-interview-questions | live coding and take-home formats (snippet) | prep guide | 2025 |
| Reddit snapshot (mirror) | https://reddit.sentinel-team.org/posts/1s4v4ad/snapshots/2026-04-03T16%3A30%3A40.408652Z | pandas appears in take-homes and live coding (snippet) | forum mirror | 2026-04 |
| Glassdoor Tiger Analytics reviews (Bengaluru Jun 2024; Hyderabad Feb 2024) | https://static.glassdoor.co.in/Interview/Tiger-Analytics-Interview-E717029-RVW88618677.htm | DataFrame question; mean imputation and pandas data manipulation reported (snippet) | candidate reports | 2024 |
| Tiger Analytics AmbitionBox / GfG / Board Infinity | https://www.geeksforgeeks.org/?p=1118860 | online test with 2 Python coding questions, pandas at intermediate level (snippet) | candidate reports | 2022-26 |
| Glassdoor Tredence Bengaluru review | https://clear.glassdoor.nl/Interview/Tredence-Interview-E1141078-RVW80289783.htm | lists and dicts, no pandas take-home (snippet) | candidate report | undated |
| Dataford: explain pandas filtering, grouping, merging | https://dataford.io/questions/how-would-you-explain-pandas-filtering-grouping-merging-and-applying-functions | explain-plus-code format (snippet) | practice platform | undated |
| GoLinuxCloud / Flexiple / Adaface pandas questions | https://www.golinuxcloud.com/pandas-interview-questions/ | merge validate=, performance (snippet) | prep blogs | 2024-26 |
| IBM HR Attrition EDA notebooks (mljar, GitHub, rcilino, justin-castillo) | https://justin-castillo.github.io/ibm-employee-attrition/notebooks/01_eda.html | 1,470 rows, about 16% attrition, standard EDA flow for HR practice data (snippet) | public notebooks | undated |
| Internal: research/interview_processes.md, research/jd_sample_*.md, research/market_skills_2026.md | (repo) | Python in 32% of JDs pooled; Python/pandas in Tiger Analytics, Accenture, Deloitte, Amazon, HSBC reports | prior research | 2026 |

Star-assignment reasoning
- Three stars: open-ended "first steps on an unseen file", load/inspect, attrition rate, group comparisons, duplicates, missing values, merge checks and presenting findings. These match the live-EDA pattern in the Pivigo/PracHub snippets and the Tiger Analytics pandas reports. Inference, not measured frequency.
- Two stars: standard follow-ups (correlation, bands, outliers, common errors, charts, quality checks). One star: differentiators (reproducibility, auto-EDA tools, risk score, large-file handling beyond basics).

Notes
- Blocked or unverified: Glassdoor, AmbitionBox, GfG not opened; Cognizant and Infosys searches returned nothing Python-specific; no Hyderabad take-home detail.
- Overlap check: Book 5 Part 11 owns describe/corr/t-test/IQR one-liners; Part 9 here uses them only inside end-to-end tasks. Book 2 owns the pandas-merge mapping.
- Gap-fills: about 18 questions (e.g. cohort retention, reconciliation, risk score, chunked reading, causation caveat, reproducibility) are standard-practice composites with no direct source. Target was 50.
