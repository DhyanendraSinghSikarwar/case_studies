# Book 1 Part 12 — Sources & Research Notes (2026-10-20)

## Search status
WebSearch worked (4 queries, standard mode). Results were thin and mostly generic. AmbitionBox and GeeksforGeeks interview experiences did NOT surface; no Flipkart/Swiggy/PhonePe/Zalando/Spotify/Klarna-specific reports found. WebFetch was not used (no page opened in full); everything below is from search-result snippets only. Company attributions in the question list for those names are therefore expert-judgement, not sourced, and are labelled as "types" in spirit. Question frequency counts are low-n and anecdotal.

## Sources actually seen (search results)
| Source | URL | What it supports |
|---|---|---|
| Glassdoor, Pinterest interview (2025) | https://www.glassdoor.com.ar/Entrevista/Pinterest-Entrevista-E503467-RVW92047729.htm | Live coding: SQL, then pandas data manipulation, then case |
| Glassdoor, Bloomberg Princeton (Nov 2025) | https://fr.glassdoor.ch/Entretien/Bloomberg-Entretien-E3096-RVW101892925.htm | Technical round answering questions on a dataset with pandas |
| Glassdoor, TCS (2026) | https://www.glassdoor.com.mx/Entrevista/Tata-Consultancy-Services-Entrevista-E13461-RVW94075303.htm | SQL, NumPy, pandas, sklearn, matplotlib basics |
| PracHub, Voleon DS live coding (Apr 2026) | https://prachub.com/interview-experiences/voleon-data-scientist-live-coding-interview-focused-on-pandas-a623c31b38 | Live pandas manipulation; unclear polish expectations |
| PracHub, Voleon MLE time-series pipeline screen (2026) | https://prachub.com/interview-experiences/voleon-machine-learning-engineer-interview-experience-a-time-series-pipeline-coding-screen | 90-min ~5-task pipeline; suspected feature leakage |
| Glassdoor, ION Group (2025) | https://www.glassdoor.co.uk/Interview/ION-Group-Interview-E1923000-RVW99170901.htm | Supervised-learning basics + some pandas methods |
| tradinginterview.com sklearn workflow | https://www.tradinginterview.com/courses/machine-learning/lessons/the-scikit-learn-workflow/ | Pipeline as main leakage defence; noise -> fake 72% accuracy demo |
| GoLinuxCloud pandas interview guide | https://www.golinuxcloud.com/pandas-interview-questions/ | groupby vs transform, merge row explosion, vectorization vs apply, messy CSV cleaning |
| Dataford leakage question | https://dataford.io/questions/how-do-you-detect-and-mitigate-data-leakage-in-your-training-pipeline-at-st-engineering | Leakage detection is an asked question (no answer detail) |
| PracHub AI-assisted coding guide | https://prachub.com/resources/ai-assisted-coding-interviews-how-to-prepare-without-letting-ai-take-over | AI code looks right but has subtle bugs; verify, do not re-prompt until tests pass |
| Substack, AI-assisted coding interviews 2026 | https://pawankjha.substack.com/p/ai-assisted-coding-interviews-a-complete | Patterns for AI-allowed interviews (vendor/blog, unverified stats) |
| LeadDev, LLM tools in interviews | https://leaddev.com/hiring/what-ai-has-offer-using-llm-tools-interviews | AI use in interviews; catching AI mistakes as signal |

## Theme -> sources -> frequency (anecdotal, source count)
| Theme | Sources | Freq | Recency |
|---|---|---|---|
| pandas wrangling live round (groupby, merge, cleaning) | Pinterest, Bloomberg, Voleon, TCS, ION, GoLinuxCloud | 6 | 2025-2026 |
| Leakage / Pipeline correctness | Voleon MLE, tradinginterview, Dataford | 3 | 2025-2026 |
| sklearn/NumPy basics | TCS, ION | 2 | 2025-2026 |
| AI-allowed rounds: review/verify LLM code | PracHub, Substack, LeadDev | 3 | 2026 |
| Vectorisation vs apply, merge explosion | GoLinuxCloud | 1 | 2025 |

Star assignment: pandas wrangling, leakage and Pipeline/CV, vectorisation and AI-code-review ranked top (multiple sources + universal in loops); the rest are expert-judged. NumPy-from-scratch rated lower than pandas because reports say NumPy appears less often.

## AI-era changes noted
- 2026: reportedly ~46% of surveyed hiring leaders allow AI in technical rounds, ~34% ban it (CoderPad State of Tech Hiring 2026, as relayed by a PracHub-style secondary source; unverified).
- When AI is allowed, spotting and fixing AI mistakes (leakage, wrong CV, edge cases) and verification discipline are scored. Hence the review-LLM-code and verify-AI-output questions.
- Live pandas rounds still bar-raise via SQL -> pandas -> case structure.

## Question origin (merged; theme found in sources vs added from expert gap-check)
| Q | Stars | Origin |
|---|---|---|
| Q1 | ⭐⭐⭐ | theme found in sources |
| Q2 | ⭐⭐⭐ | theme found in sources |
| Q3 | ⭐⭐⭐ | theme found in sources |
| Q4 | ⭐⭐⭐ | theme found in sources |
| Q5 | ⭐⭐⭐ | theme found in sources |
| Q6 | ⭐⭐⭐ | theme found in sources |
| Q7 | ⭐⭐⭐ | theme found in sources |
| Q8 | ⭐⭐⭐ | theme found in sources |
| Q9 | ⭐⭐⭐ | theme found in sources |
| Q10 | ⭐⭐⭐ | theme found in sources |
| Q11 | ⭐⭐⭐ | theme found in sources |
| Q12 | ⭐⭐⭐ | theme found in sources |
| Q13 | ⭐⭐⭐ | theme found in sources |
| Q14 | ⭐⭐⭐ | theme found in sources |
| Q15 | ⭐⭐⭐ | theme found in sources |
| Q16 | ⭐⭐⭐ | theme found in sources |
| Q17 | ⭐⭐⭐ | theme found in sources |
| Q18 | ⭐⭐⭐ | theme found in sources |
| Q19 | ⭐⭐ | added from expert gap-check |
| Q20 | ⭐⭐ | added from expert gap-check |
| Q21 | ⭐⭐ | theme found in sources |
| Q22 | ⭐⭐ | added from expert gap-check |
| Q23 | ⭐⭐ | added from expert gap-check |
| Q24 | ⭐⭐ | added from expert gap-check |
| Q25 | ⭐⭐ | added from expert gap-check |
| Q26 | ⭐⭐ | added from expert gap-check |
| Q27 | ⭐⭐ | added from expert gap-check |
| Q28 | ⭐⭐ | added from expert gap-check |
| Q29 | ⭐⭐ | added from expert gap-check |
| Q30 | ⭐⭐ | added from expert gap-check |
| Q31 | ⭐⭐ | added from expert gap-check |
| Q32 | ⭐⭐ | added from expert gap-check |
| Q33 | ⭐⭐ | added from expert gap-check |
| Q34 | ⭐⭐ | added from expert gap-check |
| Q35 | ⭐⭐ | theme found in sources |
| Q36 | ⭐⭐ | added from expert gap-check |
| Q37 | ⭐⭐ | added from expert gap-check |
| Q38 | ⭐⭐ | added from expert gap-check |
| Q39 | ⭐⭐ | added from expert gap-check |
| Q40 | ⭐⭐ | added from expert gap-check |
| Q41 | ⭐⭐ | added from expert gap-check |
| Q42 | ⭐ | added from expert gap-check |
| Q43 | ⭐ | added from expert gap-check |
| Q44 | ⭐ | added from expert gap-check |
| Q45 | ⭐ | added from expert gap-check |
| Q46 | ⭐ | added from expert gap-check |
| Q47 | ⭐ | added from expert gap-check |
| Q48 | ⭐ | added from expert gap-check |
| Q49 | ⭐ | theme found in sources |
| Q50 | ⭐ | theme found in sources |
| Q51 | ⭐ | added from expert gap-check |