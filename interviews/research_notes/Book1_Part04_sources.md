# Book 1 Part 04 — Sources (trees, RF, boosting, tuning, SHAP)

Date of research: 2026-10-20. WebSearch worked (US-only, snippet-level summaries; I did NOT open pages with WebFetch, so URLs below are those returned by search results). Glassdoor/AmbitionBox/Blind pages came back only as search snippets; Blind (teamblind.com/search/xgboost) and GeeksforGeeks returned no usable interview report. No Flipkart/PhonePe/Zalando/Booking-specific tree questions were found; Spotify result showed coding only; Klarna guide is credit-risk/ML/SQL generic. Evidence is thin and anecdotal; star ratings lean on repeated themes plus expert judgement.

## Evidence found (question -> source -> recency)

| Question theme | Sources (seen in search results) | Count | Recency |
|---|---|---|---|
| RF vs XGBoost (difference / why choose) | AmbitionBox Applied Cloud Computing (Apr 2024) https://www.ambitionbox.com/interviews/applied-cloud-computing-interview-questions/data-scientist ; AmbitionBox Digitas (Sep 2023) https://www.ambitionbox.com/interviews/digitaslbi-interview-questions/data-scientist ; Naukri Code360 Tredence (Aug 2021) https://www.naukri.com/code360/interview-experiences/tredence-analytics/interview-experience-aug-2021-exp-0-2-years-1557 ; Glassdoor listings https://static.glassdoor.com.br/Interview/sr-data-scientist-interview-questions-SRCH_KO0,17_IP340.htm and https://static.glassdoor.de/Interview/data-intern-interview-questions-SRCH_KO0,11_IP657.htm ; AmbitionBox Target https://www.ambitionbox.com/interviews/target-interview-questions/data-scientist ; prep guide https://prachub.com/resources/xgboost-vs-random-forest | 6+ | 2021-2025 |
| RF vs gradient boosted trees (Intuit, Amazon intern) | Glassdoor Intuit / Amazon intern entries surfaced via search (e.g. https://static-pc.glassdoor.de/Interview/Amazon-Data-Science-Intern-Interview-Questions-EI_IE6036.0,6_KO7,26_IP7.htm) | 2 | n/d |
| Extra Trees vs RF; justify model choice | Glassdoor France Amazon review (Sep 2025) https://www.glassdoor.fr/Entretien/Amazon-Entretien-E6036-RVW103354173.htm | 1 | Sep 2025 |
| RF hyperparameters | Naukri Code360 UHG (Oct 2020) https://www.naukri.com/code360/interview-experiences/uhg/interview-experience-data-scientist-oct-2020-exp-0-2-years-2-1713 | 1 | 2020 |
| Tune XGBoost hyperparameters | Naukri Code360 Walmart DS (Apr 2021) https://www.naukri.com/code360/interview-experiences/walmart/walmart-interview-experience-data-scientist-apr-2021-exp-0-2-years-1195 | 1 | 2021 |
| XGBoost vs LightGBM | Glassdoor https://static.glassdoor.com.br/Interview/sr-data-scientist-interview-questions-SRCH_KO0,17_IP292.htm ; PyData London 2022 LightGBM talk https://pydata.org/london2022/wp-content/uploads/2022/07/PyData-London-2022_-Unlocking-the-power-of-LightGBM-summarized.pdf | 2 | 2022+ |
| Single tree vs ensemble trade-offs | Dataford practice prompt https://dataford.io/questions/explain-the-trade-offs-between-using-a-single-decision-tree-versus-an-ensemble-method-like-random-forest-or-xgboost (practice prompt, not a candidate report) | 1 | n/d |
| Gradient boosting intuition | Dataford https://dataford.io/questions/walk-me-through-the-mathematical-intuition-behind-gradient-boosting-trees ; Prepfully https://prepfully.com/answers/gradient-boost ; DEV 160 DS questions https://dev.to/al_grigor/160-data-science-interview-questions-4bl3 | 3 | n/d |
| Overfitting control (CV, regularization, pruning) | Interview Query Swiggy MLE guide https://www.interviewquery.com/interview-guides/swiggy-machine-learning-engineer ; Interview Query Flipkart https://interviewquery.com/interview-guides/flipkart-machine-learning-engineer | 2 | 2025 |
| Feature importance / selection with trees | Flipkart MLE guide (above); TowardsAI XGBoost Q&A https://pub.towardsai.net/top-30-xgboost-interview-questions-and-answers-part-1-of-2-ce691a1a8af8 | 2 | n/d |
| SHAP vs importance, correlated-feature caveats | Blog https://medium.com/biased-algorithms/shap-values-vs-feature-importance-ba6b91c16319 ; Kumar et al. ICML 2020 https://proceedings.mlr.press/v119/kumar20e.html ; arXiv https://arxiv.org/pdf/2302.08160 (these are explainers/papers, not interview reports; no SHAP-specific candidate report found) | 0 interview reports | - |
| Noisy labels: bagging vs boosting, tuning difficulty | PracHub guide (above) | 1 | n/d |

Not found / blocked: Blind, GeeksforGeeks (no hits); Flipkart, PhonePe, Zalando, Booking tree-specific reports; Spotify ML questions (coding only); Swiggy Telegram/Scribd hits unverified, not used.

## Frequency decisions
- Triple-star: topics recurring across sources (RF vs XGB, RF hyperparameters, XGB tuning, XGB vs LGBM, boosting intuition, overfitting control, feature importance) plus core-syllabus staples (splits/Gini/entropy, bagging vs boosting, pruning, SHAP, missing/categorical handling) added/promoted on expert judgement because SHAP and tree basics are universal in loops even when write-ups omit them.
- Questions that were not directly seen in any source (added from expert gap-check): Q1-Q4 (basics, expert-promoted), Q16, Q17, Q22-Q24, Q27, Q29-Q35 (except Q35 feature selection, seen via Flipkart guide), Q36-Q38, Q40, Q43-Q47, Q50-Q54 and the rest of the one-star advanced set. Seen or closely supported by sources: Q5-Q15, Q18-Q21, Q25-Q26, Q28, Q35, Q39, Q41, Q42, Q48-Q49 (LightGBM talk / TowardsAI).

## AI-era changes noted
- Reports emphasise "justify why you chose this model" and project deep-dives (Amazon Sep 2025, Swiggy 2025): candidates must defend choices, not recite definitions.
- Added Q33 (LLM-generated XGBoost pipeline code review) and Q34 (tabular DL vs GBDT); expect follow-ups such as using an LLM/tabular foundation model (TabPFN-type) versus GBDT, and explaining SHAP to regulators.
- Pure-definition questions on XGBoost internals are likely lower-yield in senior loops; live coding of a split finder / from-scratch boosting appears as differentiators (added as gap-check, unverified frequency).
