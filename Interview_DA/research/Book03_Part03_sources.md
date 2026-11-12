# Book 3 Part 3 sources (NumPy basics)
Accessed 2026-11-09 via WebSearch (snippet-level only). WebFetch was not used, so NO page was fetched in full. 7 searches run: 5 returned results, 2 returned a rate-limit error (too_many_requests) and their answers came from model knowledge only, so no source is cited for them. Sample size: about 80 result links, none read in full. No first-hand Hyderabad/Bengaluru 2025-26 NumPy-specific interview report was found; company attributions are unverified. Glassdoor, AmbitionBox, GfG pages appeared in results but were not opened.

| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| FACE Prep: pandas/NumPy questions for AI/ML freshers | https://faceprep.in/article/pandas-numpy-interview-questions-for-ai-ml-freshers-2026/ | screening focuses on array mechanics, computation semantics, memory (snippet) | prep blog | 2026 |
| igmguru NumPy questions | https://www.igmguru.com/blog/numpy-interview-questions | beginner/intermediate topic spread (snippet) | prep blog | 2026-04 |
| TechPrep 88 NumPy questions | https://www.techprep.app/blog/numpy-interview-questions | question breadth (snippet) | prep blog | 2026 |
| DataCamp NumPy questions | https://www.datacamp.com/blog/numpy-interview-questions | rolling mean task (snippet) | prep blog | undated |
| Interview Query NumPy questions | https://interviewquery.com/p/numpy-interview-questions | common set (snippet) | prep blog | 2025 |
| Adaface 58 NumPy questions | https://adaface.com/blog/numpy-interview-questions | broadcasting, axis, boolean indexing (snippet) | assessment vendor | 2024-09 |
| ProjectPro 30+ NumPy questions for data analysts | https://www.projectpro.io/article/numpy-interview-questions-and-answers/980 | DA-oriented list (snippet) | prep blog | undated |
| Hyring top 60 NumPy questions | https://hyring.com/jobseeker-toolkit/interview-questions/technical/numpy | state input/output shape in answers (snippet) | prep site | undated |
| Vskills, OpenGenus, singhsidhukuldeep, TheLinuxCode 2026 edition | https://thelinuxcode.com/numpy-interview-questions-with-answers-2026-edition/ | copy vs view, argmax axis, random seed (snippet) | prep blogs | 2026 |
| Algocademy / Hostman np.where guides | https://algocademy.com/blog/mastering-conditional-operations-in-python-a-comprehensive-guide-to-np-where/ | np.where, NaN comparison pitfall, np.select (snippet) | tutorials | undated |
| Tiger Analytics reports (Glassdoor, AmbitionBox, GfG, Interview Query) | https://www.geeksforgeeks.org/?p=1118860 | one report: remove duplicates using numpy or pandas; basic pandas/numpy questions (search-engine summary of snippets; pages not opened) | candidate reports | 2022-2026 |
| AskPython / Analytics Vidhya / InterviewBit DA Python lists | https://www.analyticsvidhya.com/blog/2025/07/python-interview-questions-for-data-analyst/ | NumPy sits inside general DA Python lists (snippet) | prep blogs | 2025-26 |
| Internal: research/market_skills_2026.md, interview_processes.md, jd_sample_*.md | (repo) | Python 32% of JDs; MIS 16%; no JD sample names NumPy explicitly (grep: no match); interview_processes names Python in about 10 profiles | prior research | 2026 |

Star-assignment reasoning
- Three stars: list vs array, array creation/shape, indexing, boolean filtering, aggregates, vectorised arithmetic, axis, vectorization. Every NumPy list found covers them first (inference from list prevalence, not measured frequency); Tiger Analytics report mentions basic numpy questions.
- Two stars: reshape, creation helpers, counting, unique/dedup (Tiger report), sort, broadcasting, np.where, NaN handling, view vs copy, argmax, combined conditions. Common follow-ups.
- One star: seed, stacking, flatten/ravel, cumsum/diff, sampling, nan vs None, moving average (differentiator).

Notes
- Overlap check: question_index.md has no NumPy rows (0 matches). Statistics one-liners (describe, corr) belong to Book 5 Part 11; list basics to Part 1; pandas to Parts 4-6. NumPy-in-pandas relation is limited to one conceptual question.
- Gap-fills: about 12 of 30 (HR-flavoured tasks such as hike, attendance labels, employee sample; nan vs None; combined conditions; reshape; astype) are standard-practice composites with no direct source. Target was 25; actual 30.
- Honest limitation: NumPy is rarely named in Indian DA JDs or interview reports; it is asked mostly as a basics warm-up beside pandas.
