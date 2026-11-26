# Book 3 Part 7 sources (dates and time series in pandas)
Accessed 2026-11-09 via WebSearch (snippet-level only; WebFetch was not used). 6 searches returned results; 4 further searches hit a rate limit (too_many_requests) and returned no links (their answers were model knowledge, not sources). Sample size: about 100 result links, none read in full. No first-hand Hyderabad/Bengaluru 2025-26 report of a pandas datetime question was found; company attributions are unverified. Glassdoor, AmbitionBox and GfG were not reachable as primary pages.

| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| AskPython 50 pandas interview questions | https://www.askpython.com/?p=65508 | pandas datetime appears in 2026 question lists (snippet) | prep blog | 2026 |
| StrataScratch: datetime features in DS interviews | https://www.stratascratch.com/blog/how-i-use-datetime-features-in-python-in-data-science-interviews | datetime manipulation frequently asked (snippet) | prep blog | undated |
| Coursera pandas interview questions (India) | https://www.coursera.org/in/articles/pandas-interview-questions | date_range, time zones, resampling as talking points (snippet) | course article | undated |
| Educative: Dates Manipulation (DA interview prep pandas) | https://www.educative.io/courses/data-analytics-interview-prep-pandas/x1JvQ3vmo33 | to_datetime, date parts, date_range, resample (snippet) | course | undated |
| Naukri Code360 pandas questions | https://www.naukri.com/code360/library/pandas-interview-questions | Timedelta question (snippet) | prep site | undated |
| Hyring pandas questions | https://hyring.com/jobseeker-toolkit/interview-questions/technical/pandas | interviewers look for date handling (snippet) | hiring guide | undated |
| Udemy pandas interview practice test | https://www.udemy.com/course/pandas-interview-questions-practice-test/ | resampling, shift/lag, rolling in practice sets (snippet) | course | 2026-04 |
| Analytics Vidhya 60 Python questions for DA | https://www.analyticsvidhya.com/blog/2025/07/python-interview-questions-for-data-analyst/ | DA-level Python list (snippet) | blog | 2025-07 |
| pandas docs: Series.resample, pct_change | https://pandas.pydata.org/docs/reference/api/pandas.Series.resample.html | resample vs groupby, asfreq, pct_change behaviour (snippet) | official docs | current |
| Telegram @pythonanalyst scenario posts | https://t.me/s/pythonanalyst/1343 | month-wise sales, MoM growth scenario (snippet; informal) | channel | undated |
| Internal: research/interview_processes.md (Amazon Hyderabad basic pandas; Accenture, Deloitte, HSBC, Tiger Analytics Python mentions), research/jd_sample_*.md | (repo) | Python expected in DA JDs; datetime not named specifically | prior research | 2026 |

Star-assignment reasoning
- Three stars: parse to datetime, .dt parts, date differences/tenure, monthly totals, MoM growth, rolling average, resample vs groupby: they recur across every list and match the HR/sales tasks interviewers set. Inference from list frequency, not a measured count.
- Two stars: filtering, indexing, shift, formats, gaps, quarter/FY, common errors. One star: time zones, epoch, Period, asfreq, closed/label, train-test split (differentiators).

Notes
- Gap-fills: about 18 questions (HR attrition, financial year, last-90-days, busday_count, consecutive-event gaps, year-over-year) are standard-practice composites with no direct source. Target was 40.
- Overlap checked against question_index.md: B2P6Q38 (pandas equivalents of cumsum/shift/rolling) and B5P11Q15 (moving average in pandas) are adjacent; Part 7 questions are standalone date-focused, kept.
