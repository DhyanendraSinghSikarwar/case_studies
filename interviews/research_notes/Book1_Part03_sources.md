# Book 1 Part 03 - Research sources (classification metrics, imbalance, calibration, thresholding)
Date: 2026-10-20. Method: WebSearch (worked; US-only, standard mode, 6 queries). Only search-result snippets were seen; I did NOT open pages with WebFetch, so the claims below rest on result summaries. Glassdoor, AmbitionBox, LeetCode Discuss, Blind, GeeksforGeeks were searched by name but returned NO first-hand 2025-26 reports for Flipkart/Swiggy/PhonePe/Amazon India/Microsoft IDC/Walmart/JPMC/Spotify/Zalando/Booking/Klarna. Company tags in the book are therefore company TYPES/plausible fits, not confirmed reports, except where noted below.

## Sources actually seen (URLs from search results)
- https://www.techinterview.org/post/3233474426/ai-ml-interview-model-evaluation-metrics-precision-recall-f1-auc-roc-confusion-matrix-cross-validation-bias-variance/ (metrics; AUC-PR expected for imbalanced)
- https://www.techinterview.org/post/3233460032/handling-imbalanced-datasets-in-machine-learning/ (imbalance, threshold lowering)
- https://codemia.io/practice/debug-a-model-with-class-imbalance-6 (Postmates onsite, dated Oct 25 2025: debug poor recall on imbalanced model)
- https://dataford.io/questions/how-would-you-decide-whether-to-use-roc-auc-or-precision-recall-auc-for-an-imbalanced-problem-at-saint-gobain ; .../explain-the-difference-between-roc-auc-and-precision-recall-auc-for-fraud-detection-at-chime ; .../what-are-the-pros-and-cons-of-using-auc-roc-versus-precision-recall-auc-for-highly-imbalanced-datasets ; .../how-do-you-deal-with-class-imbalance-in-your-datasets (ROC vs PR AUC, imbalance)
- https://prachub.com/interview-questions/choose-between-precision-and-recall-for-a-classification-decision (Citadel-tagged: operating point from error costs, capacity, calibration)
- https://prachub.com/coding-questions/compute-precisionrecall-curve-on-imbalanced-data (coding PR curve)
- https://static.glassdoor.com.mx/Interview/sr-data-scientist-interview-questions-SRCH_KO0,17_IP34.htm (Tiger Analytics imbalanced dataset; Snowflake F1 vs ROC-AUC)
- Glassdoor thread (2024 Sigmoid interview: does SMOTE increase test sample size) - cited in search summary, thread URL not shown to me.
- https://www.educative.io/blog/data-science-interview-questions-and-answers , https://jobrise.io/en/blog/data-scientist-interview-questions-and-answers-2026/ , https://www.deel.com/blog/data-scientist-interview-questions/ , https://tealhq.com/career-paths/machine-learning-scientist-interview-questions (generic 2025-26 guides)
- https://www.preprints.org/manuscript/202510.0958/v1 (Oct 2025 fraud preprint: ROC-AUC masks cost asymmetry; MCC/F2 suggested)
- https://arxiv.org/pdf/2509.23665 (calibration, Platt vs isotonic, ECE+Brier); https://www.kdnuggets.com/a-deep-dive-into-calibration-of-language-models-platt-scaling-isotonic-regression-temperature-scaling (LLM calibration); https://metricgate.com/docs/calibration-error-metrics/ (ECE caveats)
- https://towardsdatascience.com/why-accuracy-isnt-everything-precision-and-recall-simply-explained-25bc093c7cda/ (threshold effects)

## Question -> evidence -> frequency (Q numbers per Part03 file)
Frequency = number of distinct sources seen mentioning the topic (low counts reflect limited search access, not true rarity).
| Q | Topic | Evidence | Freq | Recency | Origin |
|---|---|---|---|---|---|
| 1 | accuracy misleading | techinterview, TDS, deel, educative, dataford | 5+ | 2025-26 | found |
| 2,3 | P/R/F1, trade-off | techinterview, deel, prachub, jobrise | 4+ | 2025-26 | found |
| 6 | ROC vs PR AUC | 3 dataford, techinterview, preprint | 5 | 2025-26 | found |
| 7 | F1 vs ROC-AUC | Glassdoor Snowflake | 1 | n/a | found |
| 8,11 | imbalance options, weights | dataford, techinterview, Glassdoor Tiger, educative | 5 | 2025-26 | found |
| 9,10 | SMOTE, leakage | Glassdoor Sigmoid 2024, guides | 3 | 2024-26 | found |
| 12 | threshold | techinterview, TDS, prachub | 3 | 2025 | found |
| 16 | 99% acc, poor recall | Codemia/Postmates Oct 2025 | 1 | Oct 2025 | found |
| 15 | fraud eval design | dataford fraud evaluation, preprint | 2 | 2025 | found |
| 14,20,21 | calibration, Platt/isotonic, ECE | arXiv 2509.23665, kdnuggets, metricgate (concept pages, not interview reports) | 3 | 2024-26 | found (concept) |
| 25 | capacity operating point | prachub Citadel | 1 | n/a | found |
| 19,39 | from-scratch PR curve / AUC | prachub coding | 1 | n/a | found (19); 39 added |
| 29,41,45,46 etc. | MCC; LLM-era items | preprint (MCC/F2); kdnuggets (LLM calibration) | 1-2 | 2025-26 | partly found |
All other questions (4,5,13,17,18,22-24,26-28,30-38,40,42-44,47-49) were ADDED from expert gap-check (standard topics in loops at these levels but not surfaced by the limited search). Stars were assigned from source frequency plus expert judgement of loop prevalence.

## AI-era changes noted
- LLM-as-classifier/judge evaluation, LLM calibration (logprobs, verbalized confidence, temperature scaling) now appear in senior and GenAI-adjacent loops (Q41, Q45).
- AI-code-review rounds: candidates asked to spot SMOTE-before-split, accuracy on imbalanced data, threshold tuned on test (Q46).
- Metric choice is trending towards MCC/F2/PR-AUC and cost-based evaluation over ROC-AUC alone (Oct 2025 preprint).
- Gaps: no India-company (Flipkart, Swiggy, PhonePe, Amazon IN, MS IDC, Walmart, JPMC) or Europe (Spotify, Zalando, Booking, Klarna) first-hand reports found; Wave B/Book 7 live research should fill these.
