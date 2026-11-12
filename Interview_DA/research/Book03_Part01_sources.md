# Book 3 Part 1 sources (Python basics: variables, types, lists, dicts, loops, functions)
Accessed 2026-11-09 via WebSearch (snippet-level only; WebFetch not used, so NO page was fetched in full). 9 search calls were made; 6 returned results, 3 hit "too_many_requests" rate limits (loops, functions/lambda, Infosys/Cognizant/Wipro; their text was general knowledge only and is NOT cited as a source). Glassdoor and AmbitionBox pages appeared only as search-result titles/snippets. Sample size: 6 successful searches, about 100 links, none read in full. Company attributions below are unverified single anecdotes.

| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| Dataquest Python interview questions | https://www.dataquest.io/blog/python-interview-questions/ | lists, dicts, comprehensions, shallow vs deep copy as core DA topics (snippet) | prep blog | 2026-03 |
| Codebasics top 10 Python questions for DA 2026 | https://codebasics.io/blog/top-10-python-interview-questions-for-data-analyst-roles-in-2026 | scenario-style questions beyond definitions (snippet) | prep blog | 2026 |
| Analytics Vidhya 60 Python questions for DA | https://www.analyticsvidhya.com/blog/2025/07/python-interview-questions-for-data-analyst/ | topic breadth (title/snippet only) | prep blog | 2025-07 |
| IIT Kanpur EICTA Python basics for DA | https://eicta.iitk.ac.in/knowledge-hub/data-analytics/python-basics-interview-questions-for-data-analyst/ | existence of basics list (title only) | course site | undated |
| Glassdoor: list vs tuple (TCS) | https://www.glassdoor.com/Interview/What-is-the-difference-between-a-list-and-a-tuple-in-Python-QTN_8404256.htm | list vs tuple asked at TCS (snippet; July 2025 per summary) | candidate report | 2025 |
| Glassdoor: list vs tuple (Capgemini) | https://www.glassdoor.ca/Interview/What-is-the-difference-between-a-list-and-a-tuple-in-Python-QTN_8070681.htm | same at Capgemini (snippet) | candidate report | undated |
| Kiran Academy Python questions | https://thekiranacademy.com/python-interview-questions | tuple-containing-list follow-up (snippet) | academy blog | 2026 |
| Glassdoor: Indium Software (Hyderabad) | https://www.glassdoor.es/Entrevista/Indium-Software-Entrevista-E431611-RVW99708972.htm | "basic python codes (prime, arrays, strings)", lists/tuples, SQL joins; Sep 2025 (snippet; mapping from search summary) | candidate report | 2025-09 |
| Glassdoor: DataBeat (Hyderabad) | https://www.glassdoor.com.au/Interview/DataBeat-Interview-E3301042-RVW103511981.htm | about 80% SQL / 20% Python basics (snippet; one of several DataBeat reviews) | candidate report | 2025-26 |
| Glassdoor: Saras Analytics (Bengaluru) | https://www.glassdoor.ca/Interview/Saras-Analytics-Interview-Questions-E3239033.htm | joins, Python and DSA problems, Apr 2025 (snippet) | candidate reports | 2025 |
| Glassdoor: Anonymous Bengaluru DA | https://clear.glassdoor.nl/Interview/Anonymous-Interview-E5182641-RVW94174891.htm | 40-minute screen: basic SQL plus pandas, Jan 2025 (snippet) | candidate report | 2025-01 |
| Glassdoor: Deliveroo mutable default argument | https://www.glassdoor.ca/Interview/What-problem-could-occur-is-an-empty-list-is-used-as-default-argument-to-a-python-function-QTN_5794240.htm | mutable default argument asked in interviews (snippet; not India, not DA) | candidate report | undated |
| Toptal 51 Python questions; DEV Community mutable default article | https://www.toptal.com/developers/python/interview-questions ; https://dev.to/ameer_abdullah_68d48c8496/why-python-developers-fail-default-mutable-argument-questions-in-interviews-mhj | mutable default trap and the None fix (snippet) | blogs | undated |
| Dataford / DataDriven frequency-count practice | https://dataford.io/questions/count-frequencies-in-a-list-python ; https://datadriven.io/learn/py_pattern_dict_manipulation_beginner | dict/Counter frequency tasks are a standard coding-round pattern (snippet) | practice platforms | undated |
| Naukri MIS executive guide; Hirist MIS list; Tech Mahindra Glassdoor report | https://w10.naukri.com/mailers/2019/upload/sep/mis-executive-interview-guide.pdf ; https://www.hirist.tech/blog/top-25-mis-executive-interview-questions-and-answers/ ; https://www.glassdoor.sg/Interview/Tech-Mahindra-Interview-E135932-RVW96909788.htm | MIS roles are Excel/SQL/VBA first; Python only occasionally (a Tech Mahindra report mentions Python code and rating SQL/Python 1-10) (snippet) | guides/report | 2019-2026 |
| Internal: research/market_skills_2026.md | (repo) | Python in 35% of 40 JDs in 0-2 yr sample ("Common", not near-universal) | prior research | 2026 |
| Internal: research/interview_processes.md | (repo) | basic Python in Infosys, Accenture, Deloitte, JPMorgan, HSBC, Amazon (pandas/numpy), Tiger Analytics (duplicate frequency, strings/lists), Fractal (4 Python/R test questions), LatentView (OOP basics) | prior research | 2026 |
| Internal: research/jd_sample_*.md | (repo) | Python in 0-3 yr JDs (Indium, Newton School, Razorpay, Thermo Fisher Data Analyst I, Hire Daily, Perceptive Analytics) | prior research | 2025-26 |

Star-assignment reasoning
- Three stars: topics reported repeatedly across sources and by 2025 candidate reports (list vs tuple at TCS/Capgemini/Indium; dict counting; comprehensions; functions/lambda; loops; sorting; copy semantics) plus core data types, which every basics screen touches.
- Two stars: standard follow-ups and common traps (mutable default, args/kwargs, scope, zip/enumerate, Counter/defaultdict, set operations, second-highest-value tasks).
- One star: lower-frequency differentiators (decorators, closures, recursion, float precision, generators) and fundamentals asked mainly of freshers in low-bar screens.
- Stars are inference from snippet-level evidence, not measured frequencies.

Notes
- Blocked or limited: Glassdoor, AmbitionBox, GfG appeared only as snippets (no full-page fetch attempted); 3 searches rate-limited. Fewer than 6 distinct successful searches would have required stopping; exactly 6 succeeded, with the topics loops, functions/lambda and company-specific lists answered only from general knowledge (flagged as unverified).
- No first-hand Hyderabad/Bengaluru report with a verbatim Python-basics question list was found; India-specific evidence is the few Glassdoor snippets above.
- Overlap check: Book 3 Part 2 (strings), Part 10 (reverse string, palindrome, basic OOP), Book 5 Part 11 (describe, groupby stats) and Book 2 pandas-equivalent rows were avoided; Part 1 keeps to pure Python types, lists, dicts, loops, functions.
- Gap-fills: about 30 questions (e.g. attendance summary, hiring-funnel drop-off, tenure band function, attrition-rate function, float precision, closures, generators, set operations on HR IDs, vectorised vs loop) are standard-practice or HR-flavoured composites with no direct source. Target was 70.
