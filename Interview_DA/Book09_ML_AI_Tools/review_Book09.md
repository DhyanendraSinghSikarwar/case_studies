# Book 9 (Basic ML + AI Tools for Analysts) — Wave C review summary

Reviewed 2026-11-20, one reviewer per part (per-part reports in `review/review_PartNN.md`). Environment: Python 3.13, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, statsmodels 0.15.0, sqlite3; no web access and no live LLM or cloud calls.

## Totals
| Part | Topic | Answers checked | Answers edited | Notable fixes |
|---|---|---|---|---|
| 1 | What ML is, supervised vs unsupervised | 77 | 16 | Eight code answers used hidden "seed 42" data: seeded generators and imports added; Q30 conclusion changed (accuracy 0.74 vs 0.70 baseline); Q59, Q68 conclusions corrected |
| 2 | Linear and logistic regression | 84 | 8 | Q27, Q38, Q56 hidden-data examples replaced with runnable ones; Q45 self-contradiction fixed; Q73 overstated claim fixed |
| 3 | Decision trees, random forest | 43 | 20 | One documented generator `make_attrition(...)` added in Q3; 14 dependent answers re-run (the old text said 56% left in some answers and 24% in others) |
| 4 | Clustering, k-means, RFM | 66 | 35 | Q25 grand mean 6.8 not 7.2; Q30 and Q39 inertia values were impossible for standardised data; Q49 5.1 not 5.0; Q63 unsupported speed claim removed; shared 300-customer examples recomputed |
| 5 | Model evaluation | 87 | 15 | Nine answers with unreproducible figures corrected (for example RMSE 14.2 vs 34.8, decision-tree test accuracy 0.75 not 0.65) |
| 6 | Overfitting, train/test, feature engineering | 39 | 18 | Generator and real output added in Q1; Q15 claim softened; Q10 leakage result 60% not 67%; Q37 0.42 not 0.45 |
| 7 | Forecasting basics | 45 | 10 | Q7 six-month average 135.0 not 140.0; Q13 undefined variable fixed; Q22 false "same total error" fixed; Q30 MAE table now has code and real output |
| 8 | Attrition and churn mini-projects | 33 | 9 | Six hidden-data worked examples regenerated; Q16 `make_classification` call completed |
| 9 | GenAI for analysts | 100 | 12 | Q62 6.3% not 6.2%; hidden-script outputs reproduced or given code; tool and SQL-dialect claims labelled |
| 10 | LLM and RAG basics | 22 | 7 | Wording and plain-words glosses; Q19 prose explained |
| 11 | Cloud basics | 21 | 9 | Hidden sample data stated; missing "Explain simply" added; vendor claims labelled |
| 12 | How to develop ML/AI skills | 24 | 8 | Generator added in Q4 and figures corrected; roadmap, datasets, mini-projects, daily plan and self-check test coverage completed |
| **Total** | | **641** | **~167** | |

The recurring defect was reproducibility: many answers quoted figures from a hidden "simulated, seed 42" generator that was not in the answer, so the numbers could not be reproduced. Reviewers rebuilt a seeded generator inside the answer, re-ran every dependent snippet on the installed versions and corrected the figures, prose and, in a handful of cases, the conclusion. A few answers also had real arithmetic errors (Q25, Q30, Q39, Q49 in Part 4; Q7 in Part 7; Q62 in Part 9). Final automated check: 641 answers, continuous numbering, balanced code fences, zero `ANSWER_PENDING`, zero em dashes outside file titles.

## Still unverified (labelled in the text)
- GenAI tool features, limits and licensing (ChatGPT, Claude, Copilot), cloud vendor facts (Snowflake, BigQuery, Fabric, Synapse, AWS/Azure/GCP) and pricing are principle-only, "from memory, unverified". No LLM or cloud service was run.
- Libraries not installed here (imblearn/SMOTE, Prophet, SHAP, XGBoost, LightGBM, kmodes, k-medoids, pandera) and other-version behaviour are "from memory, unverified".
- Rules of thumb (VIF, Cook's D, McFadden, PSI, kappa bands, silhouette thresholds, token-per-word) and all legal points (DPDP Act, GDPR, four-fifths rule) are from memory, awareness only.
- "Asked at" lines rest on search snippets; most say "commonly asked (no company-specific report found)".
- Resource and dataset names (Part 12) are from memory: check the links.

## Open items for a later pass (report-only)
- Parts 1 to 8 each use their own simulated attrition or churn data, so figures differ across parts by design (each answer states its generator and seed).
- Some intentional overlap: accuracy-trap, leakage, scaling and choosing-k ideas recur across parts; privacy and RAG/temperature overlap between Parts 9 and 10; Q23 heading in Part 7 says errors "are given".
