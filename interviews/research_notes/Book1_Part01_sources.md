# Book 1 Part 01 — Research Sources
Date: 2026-10-20. Method: WebSearch (worked; results are snippet/summary level). WebFetch was NOT used, so no page was opened in full; Glassdoor/AmbitionBox/GfG/Blind/LeetCode Discuss did not surface candidate-level ML-fundamentals reports for this topic. Frequency counts below = number of distinct sources seen mentioning the topic; they are low-resolution, so stars also rely on expert judgement.

## Sources actually seen in search results
- Interview Query Flipkart DS guide: https://www.interviewquery.com/guides/flipkart-data-scientist (paywalled; says candidates reported logistic regression, bias-variance, overfitting/underfitting)
- Interview Query Swiggy MLE guide: https://www.interviewquery.com/interview-guides/swiggy-machine-learning-engineer (overfitting; CV, regularization, pruning)
- Codemia practice pages (k-means / logistic regression from scratch): https://codemia.io/practice/implement-k-means-from-scratch-8 , https://codemia.io/practice/implement-logistic-regression-from-scratch-8 (tagged Booking.com MLE screen Sep 2025, Splunk MLE Mar 2026, Brex, Robinhood; titles sometimes mismatched)
- Let's Data Science: https://letsdatascience.com/blog/python-machine-learning-interview-questions (NumPy logistic regression, np.clip, learning rate, k-means convergence)
- Interview Query Zalando DA guide: https://www.interviewquery.com/interview-guides/zalando-data-analyst (supervised vs unsupervised); Klarna DS guide: https://www.interviewquery.com/interview-guides/klarna-data-scientist (ML + SQL + Python, no concrete questions visible)
- Interview Query Amazon DS guide: https://interviewquery.com/interview-guides/Amazon-Data-Scientist ; Glassdoor Amazon senior DS, Mumbai, Mar 2026: https://www.glassdoor.ca/Interview/Amazon-Interview-E6036-RVW3337793.htm (ML concepts, model choice, evaluation, case study)
- Glassdoor Fractal reviews: https://www.glassdoor.fr/Entretien/Fractal-Entretien-E270403-RVW18472105.htm (ML algos, model selection, metrics, feature engineering), https://www.glassdoor.com.ar/Entrevista/Fractal-Entrevista-E270403-RVW33168695.htm (GenAI scenarios)
- General prep: https://dev.to/al_grigor/160-data-science-interview-questions-4bl3 ; https://www.deel.com/blog/data-scientist-interview-questions/ ; https://lemon.io/interview-questions/machine-learning ; https://simplilearn.com/data-science-interview-questions-article ; https://www.upwork.com/hire/data-scientists/interview-questions/ ; https://dev.to/itdaksh_education/top-50-data-science-interview-questions-in-2026-what-each-tests-and-how-to-answer-strongly-n9a
- AI-era: https://www.techinterview.org/post/3233474925/ml-engineer-interview-post-llm-era/ ; https://www.kore1.com/data-scientist-interview-questions/ ; https://datavidhya.com/learn/de-interview-prep/the-2026-landscape/what-changed-in-2026/ ; https://prachub.com/interview-experiences/c3-ai-data-scientist-interview-experience-the-coding-round-did-not-match-earlier-reports

## Question -> evidence -> frequency (sources seen) -> recency
| Question topic | Evidence | Freq | Recency |
|---|---|---|---|
| Bias-variance | Flipkart IQ, general prep lists, Fractal | 4+ | 2025-26 |
| Overfitting detect/fix | Swiggy IQ, Flipkart IQ, general lists | 4+ | 2025-26 |
| Cross-validation | general lists, Swiggy IQ | 3 | 2025 |
| Data leakage | general guides (target-aware features, scaling on train only) | 2 | 2025 |
| Supervised vs unsupervised | Zalando IQ, general lists | 3 | 2025 |
| Logistic regression from scratch | Codemia (Booking, Splunk, Robinhood), LDS blog | 3 | Sep 2025-Mar 2026 |
| k-means from scratch | Codemia (Booking, Splunk), LDS blog | 3 | Sep 2025-Mar 2026 |
| Linear regression / KNN from scratch | LDS blog, Codemia (Brex) | 2 | 2025-26 |
| Model selection / evaluation / feature eng. | Amazon Glassdoor Mar 2026, Fractal | 2 | 2026 |
| Gradient descent / LR effects | LDS blog | 1 | 2025 |
| Others (sampling, Bayes, missing values, CV for time series, etc.) | general prep lists; expert gap-check | 1-2 | - |

## Added from expert gap-check (not directly found in sources)
Correlation vs causation, feature scaling placement, end-to-end approach, parameters vs hyperparameters, curse of dimensionality, descriptive stats, sampling bias, Bayes/Naive Bayes, time-series/group splits, missing values, nested CV, parametric/generative, vectorization/broadcasting, train_test_split & stratified CV from scratch, stable softmax/cross-entropy, offline-online gap, interpretability trade-off, MSE/MLE/MAP, bootstrap/bagging, gradient check, bias-variance derivation. AI-era items (LLM code review of leaky pipeline, double descent, benchmark contamination) are expert additions informed by the AI-era sources above.

## AI-era changes noted
- Classical algorithm derivations carry less weight but fundamentals/coding still asked (techinterview.org). Interviews lean to applied judgment, project walkthroughs, GenAI scenarios (Fractal).
- AI-assistant policy varies: some firms ban, others grade prompting and verification (datavidhya; DE-focused, directional only).

## Gaps / limitations
No AmbitionBox, GfG, Blind, LeetCode Discuss, Spotify, PhonePe, Walmart, Microsoft IDC pages surfaced. "Asked at" tags for those are indicative expert estimates, not verified reports.
