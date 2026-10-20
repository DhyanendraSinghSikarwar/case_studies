# Book 1 Part 10 - Sources (A/B testing, causal inference, experimentation)

Date: 2026-10-20. Method: WebSearch (worked; results summaries only) + WebFetch (all 3 attempts on interviewquery.com / datainterview.com returned HTTP 429, so those pages were NOT opened; only search-result summaries/snippets were used). No Glassdoor/AmbitionBox/Blind/LeetCode Discuss pages were opened; search surfaced almost no India company-specific (Flipkart, PhonePe, Amazon India, Microsoft IDC) or Klarna experience reports. Frequency counts below = number of distinct sources/search summaries that mention the topic, so they are indicative, not rigorous.

## Sources actually seen in search results
- https://www.interviewquery.com/p/statistics-ab-testing-interview-questions (Top 60 Statistics & A/B Testing, 2025; search-result summary only)
- https://datalemur.com/blog/ab-testing-interview-questions-and-answers
- https://www.amplitude.com/blog/a-b-testing-interview-questions (22 Qs)
- https://www.kdnuggets.com/2021/04/ab-testing-7-common-questions-answers-data-science-interviews-1.html (older, 2021)
- https://www.stratascratch.com/blog/ab-testing-data-science-interviews-guide (appeared as stratascratch A/B guide)
- https://www.datainterview.com/blog/ab-testing-interview-questions and /causal-inference-interview-questions
- https://futureproductanalyst.substack.com/p/how-to-passing-the-ab-test-interview
- https://codemia.io/practice/explain-causal-inference-with-an-example-27 (Spotify technical screen) and -6 (Booking.com phone screen)
- https://prachub.com/categories/analytics-and-experimentation (question bank; titles only)
- https://prachub.com/resources/sample-ratio-mismatch-interview-questions-diagnose-assignment-logging-and-filtering-errors
- https://dataford.io/questions/what-are-common-experimentation-pitfalls-such-as-novelty-effect-network-interference-and-sample-ratio-mismatch
- https://dataford.io/interview-guides/zalando/data-scientist, /product-analyst, /applied-scientist (3rd-party claim: experimentation in ~92% of loops, causal inference ~75%; unverified)
- https://www.interviewquery.com/interview-guides/swiggy-data-scientist (A/B Testing ~21 tagged Qs) ; https://www.interviewquery.com/interview-guides/flipkart-research-scientist (A/B ~24 tagged Qs)
- https://www.naukri.com/code360/interview-experiences/swiggy (Swiggy campus 2021: SQL + A/B testing asked; dated)
- https://www.cleverprep.com/companies/booking-com/data-scientist
- https://bookdown.org/madinterviewllc/Product-Data-Science-Interview-The-Bar-to-Get-Hired/ab.html
- https://www.kdnuggets.com/the-most-common-statistical-traps-in-faang-interviews (Simpson's paradox)
- https://confidence.spotify.com/glossary/sample-ratio-mismatch.md ; https://lukasvermeer.nl/srm/docs/causes/ ; Microsoft Research SRM taxonomy
- AI-era: https://statsig.com/blog/llm-optimization-online-experimentation ; https://atlan.com/know/ab-testing-llm-applications/ ; https://traceloop.com/blog/the-definitive-guide-to-a-b-testing-llm-models-in-production ; https://tianpan.co/blog/2026-04-19-ab-testing-llm-features-non-deterministic (practitioner blogs, not interview reports)

## Question -> sources -> frequency -> recency
| Topic | Sources mentioning | Freq | Recency |
|---|---|---|---|
| End-to-end A/B design, duration/sample size, metrics | Interview Query, DataLemur, Amplitude, Data Interview, Dataford Zalando, Substack, Swiggy/Flipkart guides | 8+ | 2025-26 |
| SRM | PracHub, Dataford, Spotify Confidence, Vermeer, Microsoft | 5 | 2025-26 |
| Novelty, peeking, network effects/interference | Dataford, Codemia (Spotify/Booking), Interview Query, Substack, Zalando guide | 5 | 2025-26 |
| Multiple testing | Interview Query, Amplitude, DataLemur, Dataford | 4 | 2025 |
| Simpson's paradox | KDnuggets, PracHub, Madinterview | 3 | 2025 |
| Causal inference / confounding / SUTVA | Codemia (Spotify, Booking), Data Interview, Dataford | 4 | 2025-26 |
| Switchback, quasi-experiments, bandits, long-term vs short-term | Codemia (Booking) | 1-2 | 2025-26 |
| DiD, PSM, IV, RDD, uplift, synthetic control | No dedicated source found in my searches; added by expert gap-check (standard in Booking/Spotify/Uber/Amazon causal loops) | 0 found | n/a |
| Primary metric up, revenue flat (guardrails); metric investigation | Substack, Data Interview, Swiggy case study (Naukri) | 3 | 2021-26 |
| LLM-feature experimentation | Statsig, Atlan, Traceloop, tianpan.co | 4 (blogs, not interviews) | 2025-26 |

Gap-check additions (not found in sources): Q22 (A/B/n), Q26 (ITT/non-compliance), Q27 (ratio metrics/delta method), Q34 (uplift Qini evaluation), Q46 (AI-assistant productivity causal), Q48 (concurrent-experiment interactions), Q51 (interleaving), Q52 (cluster randomisation), Q55 (winner's curse), Q58 (LLM-judge validation). Plus all DiD/IV/RDD/uplift/PSM/synthetic-control questions are rated from expert judgement as no source explicitly covered them (star ratings lowered accordingly except where Booking/Spotify use them heavily).

## AI-era changes noted
- Experimentation questions now include LLM/GenAI feature tests: non-deterministic treatment, silent provider model updates, per-user vs per-request randomization, behavioural proxy metrics (edit/retry/copy rate), LLM-as-judge validity, offline-eval vs online-A/B gaps, token cost/latency as guardrails.
- Question sites report A/B testing in roughly half of product DS loops (aggregator claim; unverified). Interviewers push past textbook into messy cases (peeking stakeholders, metric up but revenue flat, interference).
- Dropped/declining: pure formula recitation; emphasis shifts to judgement and diagnosis.
