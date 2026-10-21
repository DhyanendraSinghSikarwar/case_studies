# Book 1 Part 11 (ML System Design) - Research Notes

Date: 2026-10-20. Researcher: Wave A agent.

## Method and honesty statement
- WebSearch worked (7 queries, standard mode). WebFetch was NOT used: every URL below was seen only as a search-result link plus the search tool's summary. No page was opened in full, so counts are "mentions seen in search results", not verified interview tallies.
- Direct first-person 2025-26 ML-system-design reports for Flipkart, Swiggy, PhonePe, Zalando were NOT found (searches returned coding/machine-coding rounds, generic guides). No LeetCode Discuss ML-design thread surfaced; Blind and Glassdoor links appeared but were not opened.
- Most sources are prep-site guides (commercial), so frequency is weak evidence. Roughly 39 of 53 questions come from the expert gap-check (G) and rest are supported by at least one seen source (S). Star ratings therefore lean on expert judgement of how common each prompt is in DS/MLE loops.

## Sources seen (search results only)
1. https://www.educative.io/courses/grokking-the-machine-learning-system-design-interview/the-6-step-ml-sd-framework - 6-step framework; fraud detection for payments as worked prompt.
2. https://www.interviewquery.com/interview-guides/doordash-machine-learning-engineer - DoorDash guide (2026): ETA, batching, ranking, fraud, incentives; 3-6 week loop.
3. https://www.tryexponent.com/courses/ml-system-design/mlsd-model-selection - Exponent course; titles include ETA for maps, fraud model, ranking model (titles only).
4. https://dev.to/stack_overflowed/ml-system-design-interview-questions-what-companies-really-ask-4j3c - fraud (millisecond latency, FN vs FP), common prompts.
5. https://machinelearningatscale.com/blog/ml-system-design-interview-guide/ (March 2025) - feed ranking as retrieval + ranking, ~200 ms latency target.
6. https://www.jointaro.com/interviews/companies/spotify/experiences/machine-learning-engineer-london-england-april-1-2025-no-offer-positive-3dcc19df/ - Spotify MLE London, April 2025: case studies on designing a recommender, predicting active users, ranking popular artists per country.
7. https://www.interviewquery.com/interview-guides/spotify-machine-learning-engineer ; https://www.interviewquery.com/interview-guides/bookingcom-machine-learning-engineer ; https://www.interviewquery.com/interview-guides/klarna-ml-engineer - company guides (Klarna: end-to-end ML system design, deployment; Booking: system design round, May 2023 Glassdoor).
8. https://www.interviewquery.com/interview-guides/swiggy-machine-learning-engineer ; https://www.interviewquery.com/interview-guides/flipkart-machine-learning-engineer - generic ML + applied statistics/business scenarios.
9. https://www.designgurus.io/answers/detail/what-to-expect-in-the-swiggy-system-design-interview - Swiggy senior design: order flow, delivery-partner assignment, tracking, catalog (software system design, not ML-specific).
10. https://www.interviewquery.com/p/pricing-case-study-questions - pricing case framing (goal, unit of change, constraint; geo/switchback tests).
11. https://dataford.io/questions/we-want-to-change-our-pricing-model-at-evenup-how-do-you-model-the-potential-impact-on-churn-and-arr-using-historical-data - churn/pricing practice prompt.
12. Glassdoor Bain senior data scientist report (retail store-level sales forecasting case, July 2024), seen via https://static.glassdoor.it/Interview/sr-data-scientist-interview-questions-SRCH_KO0,17_IP316.htm (listing page; exact review not isolated).
13. https://www.interviewquery.com/guides/amazon-ml-engineer ; https://www.interviewquery.com/interview-guides/Amazon-Machine-Learning-Engineer (2026) - Amazon loop: 2 coding, 2 system design, 1 behavioural; ranking/recsys/fraud systems.
14. https://www.teamblind.com/post/applied-scientist-interview-amazon-4udsobcp - L5 applied scientist onsite incl. ML system design; L4 may skip.
15. https://www.1point3acres.com/interview/thread/1020600 and https://www.1point3acres.com/interview/thread/1089688 - Amazon applied scientist / Spotify MLE onsite threads (listed, not opened).
16. https://igotanoffer.com/en/advice/machine-learning-system-design-interview - general ML design guide.
17. https://www.glassdoor.fr/Entretien/Amazon-Entretien-E6036-RVW96811930.htm - Amazon review, real-time product recommendation engine round (2026 per search summary).

## Question -> evidence -> frequency -> recency
Frequency = number of distinct seen sources supporting the prompt type (weak signal). "Gap" = added from expert gap-check, no source seen.

| Canonical question (Part 11) | Sources (numbers above) | Freq | Recency | Origin |
|---|---|---|---|---|
| ML design framework | 1, 5, 16 | 3 | 2025 | Found |
| Fraud detection (UPI/card) | 1, 2, 3, 4, 13 | 5 | 2025-26 | Found (UPI angle added) |
| Feed ranking | 5 | 1 | Mar 2025 | Found |
| E-commerce recsys at scale | 6, 13, 17 | 3 | 2025-26 | Found |
| ETA prediction | 2, 3 | 2 | 2026 | Found |
| Churn | 11 (+ company guides) | 1-2 | 2025 | Found |
| Demand forecasting | 12 | 1 | Jul 2024 | Found |
| Search ranking | 2, 3 | 2 | 2026 | Found |
| Dynamic pricing | 10 | 1 | 2025 | Found |
| Cold start; monitoring/retraining; multi-stage architecture; Spotify-style recommender; LLM inside ML system | 6, 13, 1, 5 (partial) | 1-2 | 2025-26 | Found (partial) |
| Credit risk, CTR, notifications, offline/online metrics, skew, feedback loops, leakage, batch vs real-time, rules vs ML, QPS estimate, all other design prompts, cost/latency, bandits, HITL, compliance, fairness, privacy, global vs local models, delayed feedback, position bias, multi-objective, dark-store replenishment, AI-doc review, embeddings/vector search | none seen | 0 | n/a | Gap-check (added) |

## AI-era changes noted
- 2026 Glassdoor summaries for Amazon say rounds are more practical and LLM-flavoured than classic LeetCode; Blind notes L4 may skip ML design.
- Interviewers increasingly add "where would an LLM or embeddings fit and why not a classic model" follow-ups; added 3 AI-era questions (LLM inside classic system, embeddings/two-tower retrieval, reviewing AI-generated design docs). GenAI system design itself is deferred to Book 2; MLOps tooling to Book 4.
- Guides emphasise 6-step structure (scope, data, model, offline/online eval, deploy, monitor); answers should follow it.

## Gaps / suggestions
- Re-run searches with Glassdoor/AmbitionBox/Blind pages fetched directly (not done) to firm up India-company frequencies.
- Zalando: no results at all.
