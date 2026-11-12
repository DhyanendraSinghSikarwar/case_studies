# Book 3 Part 6 sources (pandas data cleaning: missing values, duplicates, types, outliers)
Accessed 2026-11-09 via WebSearch (snippet-level only; WebFetch not used). 8 searches run: 6 returned results, 2 failed with a rate-limit error (SettingWithCopyWarning; Hyderabad/Bengaluru fillna/dropna), so those topics rest on general knowledge, not sources. NO page was fetched in full. Sample size: about 100 result links, none read in full. No first-hand Hyderabad/Bengaluru 2025-26 report of pandas cleaning questions was found; company attributions are unverified. Glassdoor/Scribd pages appeared in results but were not opened.

| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| techprep: 82 Data Cleaning Interview Questions (2026) | https://www.techprep.app/blog/data-cleaning-interview-questions | missing/duplicate/outlier themes, "diagnose before fix" (snippet) | prep blog | 2026 |
| techprep: 77 Outlier Detection Interview Questions (2026) | https://www.techprep.app/blog/outlier-detection-interview-questions | IQR, z-score, remove/cap/transform (snippet) | prep blog | 2026 |
| Glassdoor: "write a Python function that detects outliers using the IQR method" (QTN 8257344) | https://clear.glassdoor.nl/Interview/They-asked-me-to-write-a-Python-function-that-detects-outliers-in-a-dataset-using-the-IQR-method-I-had-to-explain-the-logi-QTN_8257344.htm | one candidate-reported IQR coding question (snippet only; company not confirmed) | candidate report | undated |
| Dataford: handle missing values/outliers in pandas | https://dataford.io/questions/how-do-you-handle-missing-data-or-outliers-in-a-dataset-using-pandas | question wording (snippet) | practice platform | undated |
| Analytics Vidhya: 60 Python interview questions for data analyst | https://www.analyticsvidhya.com/blog/2025/07/python-interview-questions-for-data-analyst/ | common pandas topics (snippet) | prep blog | 2025 |
| Flexiple / igmGuru / vskills pandas interview lists | https://flexiple.com/pandas/interview-questions | duplicated/drop_duplicates, groupby fill, category dtype, astype vs to_numeric (snippet) | prep blogs | undated |
| Tiger Analytics DA guide (Interview Query) and Glassdoor reports | https://interviewquery.com/interview-guides/tiger-analytics-data-analyst | pandas listed as likely topic; one 2024 candidate report mentions mean imputation and pandas manipulation (snippet) | guide / candidate reports | 2024-2025 |
| Cognizant DA guide (Interview Query) | https://interviewquery.com/interview-guides/cognizant-technology-solutions-data-analyst | pandas among topics (aggregated, sparse; snippet) | guide | undated |
| pandas docs: to_numeric | https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html | errors='raise'/'coerce' behaviour (snippet) | official docs | current |
| growai.in: Data Cleaning with Python Pandas 2026 for Indian analysts | https://growai.in/data-cleaning-python-pandas-2026/ | claims drop_duplicates, fillna, astype, merge most tested (vendor blog; claim unverified) | vendor blog | 2026 |
| nareshit: Python questions data analytics interviews | https://nareshit.com/blogs/python-questions-data-analytics-interviews-guide | cleaning-reasoning emphasis, keep-latest-record task (snippet) | training blog | undated |
| Educative: Clean the Employee Survey Data | https://www.educative.io/courses/learn-data-science/coding-exercise-clean-the-employee-survey-data | HR-flavoured cleaning exercise model (snippet) | course exercise | undated |
| Internal: research/market_skills_2026.md, research/interview_processes.md, research/jd_sample_*.md | (repo) | Python in 35% of 0-2 year JDs (14 of 40; plan.md "majority" claim not supported); Python mentioned in JD samples | prior research | 2026 |

Star-assignment reasoning
- Three stars: detect/count missing values, dropna vs fillna, drop_duplicates, astype/to_numeric, IQR outliers, keep-latest-record, SettingWithCopyWarning, cleaning workflow: these appear in nearly every pandas question list and the techprep/Dataford/AV snippets. Inference from list frequency, not a measured interview frequency.
- Two stars: variants and practical tasks (ffill, groupby fill, string cleaning, z-score, clip, categories). One star: niche or senior (Copy-on-Write, pipe, memory downcasting, fuzzy duplicates, validation).

Notes
- Blocked or unreachable: Glassdoor, AmbitionBox, GfG, Reddit not opened; rate limit hit on 2 searches.
- Gap-fills: about 25 of 63 questions (HR-flavoured tasks such as attendance check-out, payroll currency, department names, employee ID keep-latest; plus niche items) have no direct source and are standard-practice composites. Target was 60.
- Overlap check: Book 5 Part 2 owns the concepts (IQR, outlier handling decision, z-score); here they are pandas coding questions only. Book 1 Part 5 owns Excel duplicates; Book 2 owns SQL NULL handling.
