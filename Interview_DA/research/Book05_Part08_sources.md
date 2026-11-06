# Book 5 Part 8 sources (A/B testing for analysts)
Accessed 2026-11-05 via WebSearch (snippet/summary-level). All 3 WebFetch attempts (amplitude.com, datalemur.com, interviewquery.com) failed: hosts not resolvable from this session's network allowlist. So no page was fetched in full; everything below is search-result-level. No first-hand Hyderabad/Bengaluru A/B-testing interview report was found; company attributions are unverified.

| Source | URL | Used for | Type | Recency |
|---|---|---|---|---|
| Amplitude, 22 A/B testing interview questions | https://www.amplitude.com/blog/a-b-testing-interview-questions | pitfalls: practical vs statistical significance, guardrails, novelty effect (snippet only) | vendor blog | ~2022 |
| DataLemur A/B testing interview Q&A | https://datalemur.com/blog/ab-testing-interview-questions-and-answers | claim A/B questions appear in ~50% of DS interviews (unverified, snippet) | prep blog | undated |
| Interview Query, statistics and A/B testing questions | https://www.interviewquery.com/p/statistics-ab-testing-interview-questions | topic list: power, Type I/II, z vs t, A/B/n, Bayesian vs frequentist; "~60% of DS interviews" (unverified) | prep site | 2024-2025 |
| Interview Query, how to answer A/B questions | https://www.interviewquery.com/p/how-to-answer-ab-testing-interview-questions | answer structure; SRM, novelty, logging bugs, contamination | prep site | undated |
| PracHub A/B testing topic pages | https://prachub.com/topic/analytics-experimentation-interview/ab-testing | recurring patterns: sample size/duration, one vs two-sided, multiple comparisons, peeking, network effects, guardrail design | aggregator (partly paywalled) | 2026 listing |
| Dataford pitfalls and peeking lists | https://dataford.io/questions/lists/peeking-questions | peeking, SRM, novelty, interference question titles | aggregator (titles only) | undated |
| DataInterview A/B blog | https://www.datainterview.com/blog/ab-testing-interview-questions | CTR up but revenue flat; 60/40 split bug | prep site | undated |
| Statsig / MetricGate / CleanCommit sample size pages | https://statsig.com/blog/calculating-sample-sizes-for-ab-tests | sample size inputs (baseline, MDE, alpha, power), MDE squared effect | vendor blogs | 2026 for MetricGate |
| Kohavi et al. summaries (Trustworthy Online Controlled Experiments; KDD 2012) | https://courses.cs.washington.edu/courses/cse454/13wi/papers/p959-kohavi.pdf | novelty, multiple testing, underpowered tests, winner's curse (via summaries) | academic/book summaries | 2012/2020 |
| Dataford Swiggy DA guide; AmbitionBox Swiggy BA | https://dataford.io/interview-guides/swiggy/data-analyst | Swiggy/Flipkart-style metric questions (snippet; unverified for DA) | aggregator | undated |
| research/market_skills_2026.md and jd_sample_*.md (local) | n/a | A/B testing 4% of JDs pooled (8 postings), mostly Product Analyst roles | local research | 2026 |
| research/interview_processes.md (local) | n/a | stats/probability asked at Tiger Analytics, Flipkart metrics rounds; no A/B-specific reports | local research | 2026 |

Searches run: 7 (A/B Qs 2026; pitfalls SRM/peeking/novelty; Bangalore/Hyderabad experience; sample size/MDE; Flipkart/Swiggy/Amazon guardrails; Kohavi pitfalls; plus local greps). Blocked/not reached: Glassdoor, AmbitionBox, Reddit threads (only listed in results, not read), and all three fetch attempts.

Star reasoning
- Sample is generic prep content, not Indian DA loops. JD frequency is low (4%), so A/B is a differentiator mainly for Product Analyst roles. Therefore only core concepts (what/why randomise, hypotheses, design, p-value, significance, sample size, peeking, errors) get 3 stars as the minimum a statistics-aware interview can ask; operational pitfalls (SRM, novelty, power, guardrails, duration) get 2; advanced items (CUPED, Bayesian, sequential, interference, winner's curse) get 1. All star levels are judgement, not measured frequency.
- Target was 40 (cut from 50 per market_skills_2026.md); 44 written. Gap-fills beyond the sourced topic list: about 14 (HR no-show test, Swiggy-style free delivery, absolute vs relative lift, 90/10 split, when not to A/B, outliers in revenue, A/A test, ratio metrics, unit of randomisation, which-test, causal-without-randomisation, test-result worked numeric, sticky segment questions, no-significance conclusion).
