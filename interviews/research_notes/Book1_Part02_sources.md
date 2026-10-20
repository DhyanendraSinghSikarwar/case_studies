# Book 1 Part 02 — Research Sources (Regression, Regularization, Feature Engineering)

Date: 2026-10-20. Tool status: WebSearch worked (US-only, aggregator-heavy). WebFetch: LeetCode Discuss returned 403; interviewquery.com returned 429; dev.to fetched fine. AmbitionBox, Glassdoor (India), Blind, GfG experience pages returned nothing relevant in search; PhonePe, Booking, Walmart/JPMC GCC specifics were not found. Most Prepfully pages are paywalled. Frequency counts below are therefore LOW-confidence; stars combine source counts with expert judgment of loop frequency.

## URLs actually seen (search results or fetched)
- S1 https://dev.to/al_grigor/160-data-science-interview-questions-4bl3 (fetched; theory bank, linear regression/regularization/feature selection sections)
- S2 https://leetcode.com/discuss/post/6740402/flipkart-data-scientist-2-interview-by-a-is2i/ (search snippet only; fetch blocked 403). Snippet: math round on logistic regression incl. loss derivation and L2 regularization; credit-risk design round.
- S3 https://www.interviewquery.com/guides/swiggy-data-scientist and https://www.interviewquery.com/interview-guides/swiggy-machine-learning-engineer (search snippets): resume project drill on feature engineering; correlation, class imbalance, logistic regression.
- S4 https://t.me/s/geekycod?after=601 (Telegram, Swiggy post, search snippet): R-squared vs adjusted R-squared; bagging vs boosting.
- S5 https://prachub.com/interview-questions/compare-how-models-respond-to-multicollinearity (snippet; C3 AI DS): multicollinearity vs Lasso/trees/boosting; Lasso instability.
- S6 https://prepfully.com/answers/regression-choice and Prepfully company pages (Segment, Coupang, Swiggy per snippet): Lasso vs Ridge choice.
- S7 https://www.scribd.com/document/575791454/ML-questions (Accenture list; snippet): why scale features for logistic regression.
- S8 https://www.interviewquery.com/p/linear-regression-interview-questions (snippet only; fetch 429)
- S9 https://dataford.io/interview-guides/zalando/applied-scientist (snippet): loss-function trade-offs in regression. Klarna guide https://www.interviewquery.com/interview-guides/klarna-data-scientist (snippet): credit-risk modeling focus.
- S10 https://www.deel.com/blog/data-scientist-interview-questions/ and https://medium.com/@coder_cat/nail-your-data-science-interview-day-4-regularization-techniques-7dae7cc71279 (snippets): regularization as standard question.
- S11 Glassdoor ZS Associates 2025 reports (e.g. https://www.glassdoor.fr/Entretien/ZS-Associates-Entretien-E115506-RVW21073937.htm; snippet): regression/confusion-matrix themes.

## Question -> sources -> frequency -> recency (found-in-sources items)
| Question theme | Sources | Count | Recency |
|---|---|---|---|
| Regularization concept, L1 vs L2, sparsity | S1, S2, S6, S10 | 4 | 2025 |
| Lasso vs Ridge choice / pick lambda | S1, S6 | 2 (S6 multi-company) | 2025 |
| Logistic regression, sigmoid, linear model? | S1, S3, S2 | 3 | 2025 |
| Logistic loss derivation, L2 in logistic | S2 | 1 (math round, Flipkart DS-2) | 2025 |
| Multicollinearity, sum-column, VIF | S1, S5 | 2 | 2025 |
| Feature scaling for linear/logistic | S1, S7 | 2 | older/2025 |
| R-squared vs adjusted R-squared | S4 | 1 (Swiggy) | recent |
| Normal equation vs GD vs SGD | S1 | 1 | 2025 |
| MSE/RMSE/MAE, loss-function trade-offs | S1, S9 | 2 | 2025 |
| Categorical handling, one-hot | S1 | 1 | 2025 |
| Feature selection (incl. L1/L2) | S1 | 1 | 2025 |
| Feature engineering project drill | S3 | 1 (stated as standard Swiggy round-1 pattern) | 2025 |
| Elastic Net / L1+L2 combined | S1 | 1 | 2025 |
| Interpretation of weights / bigger weight = important? | S1 | 1 | 2025 |
| Skewed target / price normality | S1 | 1 | 2025 |
| Lasso with correlated features | S5 | 1 | 2025 |
| Missing values, leakage in pipelines | not directly found in snippets; expert gap-check upgraded to 3-star based on universal loop frequency | 0 | - |

Items tagged "G" (gap-check, not found in sources) in the question file: all remaining questions (31 of 55); 24 questions map to the rows above (tagged S in generator).

## Star rule used
3-star: >=2 sources or universal in loops (expert-judged). 2-star: 1 source or regular strong-candidate topic. 1-star: senior/niche.

## AI-era changes noted
- Rounds increasingly begin with resume/project drill-down (feature engineering and modeling choices) rather than definitions; candidates must defend choices (S3).
- Pure definition questions (L1/L2, assumptions) still asked, but with "why / what breaks" follow-ups.
- Added: LLM-generated sklearn pipeline code review (leakage, scaler on full data) and "does feature engineering matter with embeddings" (expert gap-check; no source found).
- Scope handoffs: metrics/thresholds/imbalance -> Part 3; regression diagnostics deep dive -> Part 14; from-scratch vanilla implementations -> Part 1.
