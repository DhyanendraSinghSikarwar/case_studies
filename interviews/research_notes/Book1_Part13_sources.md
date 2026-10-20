# Book 1 Part 13 - Research sources (Statistics deep dive I)

Date: 2026-10-20. WebSearch worked (US-only, standard mode, 5 queries). WebFetch was not used, so pages below were seen as search results/snippets only, not opened in full. No company-specific question banks for PhonePe, Spotify, Zalando, Booking or Klarna surfaced; those "Asked at" tags for Europe/PhonePe are topic-based inference, not confirmed. Glassdoor/Blind/AmbitionBox pages are largely login- or search-limited.

## URLs actually seen in search results
- https://tryexponent.com/blog/data-science-interview-questions (2025 DS guide: p-value, CI, errors)
- https://www.guvi.in/blog/data-analyst-interview-questions-and-answers/ (says Amazon/Flipkart/Swiggy stats rounds cover hypothesis testing, A/B, distributions; generic)
- https://www.analyticsvidhya.com/blog/2026/02/probability-and-statistics-interview-questions/ (Feb 2026; CLT, p-value, Type I/II, power)
- https://nikhilpentapalli.substack.com/p/common-statistics-interview-questions
- https://www.techinterview.org/post/3233477272/statistics-questions-quant-data-science-interviews/
- https://pwskills.com/blog/data-science-statistics-interview-questions/
- https://towardsdatascience.com/5-statistical-concepts-you-need-to-know-before-your-next-data-science-interview
- https://codemia.io/practice/explain-p-value-with-an-example-23
- https://codemia.io/practice/explain-multiple-testing-correction-with-an-example-14 (HashiCorp/Databricks-tagged)
- https://prachub.com/companies/google/positions/data-scientist/categories/statistics-and-math (bootstrap/variance question)
- https://datainterview.com/blog/statistics-interview-questions
- https://www.tryexponent.com/courses/data-science/statistics-experimentation-questions/statistics-experimentation-intro
- https://clear.glassdoor.nl/Interview/Flipkart-Interview-E300494-RVW10756044.htm (Flipkart, Nov 2025: "what is p-test and t-test?")
- https://www.tryexponent.com/guides/walmart-data-scientist-interview/experiences (Walmart; probability/distributions generic)
- https://www.glassdoor.co.uk/Interview/Kabbage-Interview-E606681-RVW3502936.htm (bootstrapping question)

## Question -> sources -> frequency -> recency
Frequency = number of distinct sources/reports seen touching the topic (low counts because only snippets were visible); star rating also reflects expert judgement of loop prevalence.

| Question | Sources | Freq | Recency |
|---|---|---|---|
| p-value meaning/misreading | tryexponent, AV, pwskills, codemia, guvi | 5+ | 2025-Feb 2026 |
| Type I/II, power | tryexponent, AV, pwskills, techinterview | 4+ | 2025-2026 |
| CLT | AV, TDS, techinterview | 3+ | 2026 |
| CI vs prediction interval | tryexponent | 1+ | 2025 |
| t-test / p-test | Flipkart Glassdoor, pwskills | 2 | Nov 2025 |
| Power, sample size | AV, tryexponent | 2+ | 2025-2026 |
| Multiple testing (Bonferroni/FDR) | codemia (x2), datainterview | 3 | 2025 |
| Bootstrap | PracHub Google, Glassdoor Kabbage | 2 | 2025 |
| Mann-Whitney, KS, Shapiro, Fisher, ANOVA, MLE, MoM, delta method, TOST | none specific seen | 0 | Added from expert gap-check |

## Added from expert gap-check (not directly found in sources)
Welch t-test, Wilson CI, duality of CI/tests, distribution selection, MoM vs MLE, Fisher information/Cramer-Rao, permutation test, delta method, Mann-Whitney pitfalls, bootstrap failure/BCa, overdispersion, Monte Carlo power, FDR under dependence, TOST, Cauchy, design effect, winner's curse, heavy-tailed revenue metric, t-test from scratch, LLM-output review (21 of 61 questions flagged "E" in generation).

## AI-era changes
- Live-coding variants: implement t-test/bootstrap/permutation test from NumPy and cross-check with scipy.
- "Review an LLM's statistical analysis" (wrong test choice, p-value misinterpretation, peeking) is an emerging follow-up (expert expectation, not source-confirmed).
- LLMs commonly misstate CI interpretation and ignore multiple comparisons; interviewers probe judgement over formula recall.
