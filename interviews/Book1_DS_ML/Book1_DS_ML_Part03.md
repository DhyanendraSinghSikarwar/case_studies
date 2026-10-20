# Book 1 — Part 03: Classification Metrics, Class Imbalance, Calibration, Thresholding

**Topic:** precision/recall/F1/ROC-AUC/PR-AUC/log-loss, imbalance (SMOTE, class weights, resampling), calibration, thresholding, cost-sensitive learning
**Target:** 45 questions | **Actual:** 49 questions | **Date:** 2026-10-20

### Q1 ⭐⭐⭐ 🟢 Why is accuracy a misleading metric on imbalanced data? Give a numeric example.
**Asked at:** Flipkart-type e-commerce, fintech, GCCs, analytics services (Tiger Analytics-type)
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Define precision, recall, specificity and F1 from the confusion matrix. Given TP/FP/FN/TN counts, compute them.
**Asked at:** All company types
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Precision vs recall trade-off: which would you optimise for fraud, cancer screening and a spam filter, and why?
**Asked at:** Fintech, product cos, GCCs, Europe product cos
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What is stratified splitting / stratified k-fold and why is it essential for imbalanced data?
**Asked at:** Freshers to mid-level, services, GCCs
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 What does ROC-AUC actually mean (probabilistic interpretation)? What is the AUC of a random model and of a perfectly inverted one?
**Asked at:** Product cos, GCCs, Europe
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 ROC-AUC vs PR-AUC: when would you prefer each on an imbalanced problem, and why can ROC-AUC look deceptively good?
**Asked at:** Fintech, product cos, Europe (Klarna/Booking-type)
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 How is F1 different from ROC-AUC? Can you have high AUC and low F1?
**Asked at:** Snowflake-type product cos, services
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 How do you handle class imbalance? Walk through the options and how you choose between them.
**Asked at:** Nearly all loops (product, fintech, services, GCCs)
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 How does SMOTE work and what are its limitations (high dimensions, categorical data, noise, overlapping classes)?
**Asked at:** Services, GCCs, product cos
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Where in the pipeline do you apply SMOTE or resampling? Does it touch the validation/test set? What goes wrong if you resample before the split?
**Asked at:** Services (Sigmoid-type), GCCs, product cos
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Class weights vs resampling (over/under-sampling): trade-offs, and which would you try first?
**Asked at:** Product cos, fintech, GCCs
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 How do you choose the classification threshold? Why is 0.5 arbitrary and how do you pick a better one?
**Asked at:** Fintech, product cos, Europe, quant-style
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 What is log-loss (binary cross-entropy)? Why is it preferred to accuracy for training and for comparing probabilistic models?
**Asked at:** Product cos, GCCs, Europe
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 What is model calibration and why can a model with great AUC still be badly calibrated?
**Asked at:** Fintech, ads/marketplace product cos, Europe
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Fraud model with a 0.1% positive rate: design the evaluation end to end (split strategy, metrics, threshold, what you report to the business).
**Asked at:** Fintech (PhonePe, Klarna-type), e-commerce, GCC risk teams
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 Your model reports 99% accuracy but recall on the minority class is poor. How do you debug and improve it?
**Asked at:** Postmates-type onsite, product cos, services
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 Multiclass metrics: macro vs micro vs weighted F1. When do you pick each?
**Asked at:** Services, GCCs, product cos (NLP/classification teams)
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 What is F-beta? When would you use F2 or F0.5 instead of F1?
**Asked at:** Fintech, GCCs, product cos
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 Implement precision, recall, F1 and a precision-recall curve from scratch in NumPy.
**Asked at:** Live coding at product cos, GCCs
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Platt scaling vs isotonic regression: how each works, when each is appropriate, and why you fit them on held-out data.
**Asked at:** Fintech, ads/marketplace product cos, Europe
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 How do you measure calibration? Explain reliability diagrams, ECE and Brier score, and ECE's weaknesses.
**Asked at:** Product cos, fintech, Europe
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Which model families tend to be poorly calibrated (RF, SVM, naive Bayes, boosted trees, deep nets) and why? Which are well calibrated?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Does class weighting, SMOTE or undersampling break probability calibration? How do you correct predicted probabilities back to the true base rate?
**Asked at:** Fintech, product cos, ads teams
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 What is cost-sensitive learning? How do you incorporate different FP and FN costs (loss weights, threshold shift, cost matrix)?
**Asked at:** Fintech, insurance, GCC risk, product cos
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Capacity-constrained operating point: reviewers can check 500 cases a day. How do you pick the threshold and report precision@k / recall@k?
**Asked at:** Fintech, trust & safety, quant-style (Citadel-type), product cos
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Explain lift, gain and cumulative-gain charts and the KS statistic. How do you use them for churn or marketing targeting?
**Asked at:** Telecom, BFSI, services, GCCs
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 PR-AUC: what is its random baseline, and what is the difference between average precision and trapezoidal area under the PR curve?
**Asked at:** Product cos, Europe
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Undersampling vs oversampling vs hybrid methods; what are balanced random forest and EasyEnsemble and when do they help?
**Asked at:** Product cos, services
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 MCC, balanced accuracy and Cohen's kappa: what do they fix that F1 does not?
**Asked at:** Product cos, research-leaning roles
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Precision depends on class prevalence. If the production base rate differs from validation, how do metrics change? Use Bayes to explain.
**Asked at:** Fintech, product cos, Europe
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Why can AUC be high while precision at a usable threshold is very low? Give a worked example.
**Asked at:** Fintech, product cos
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you set imbalance parameters in XGBoost/LightGBM (scale_pos_weight, is_unbalance) and what do they do to the loss and calibration?
**Asked at:** Product cos, GCCs, Kaggle-style rounds
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Should you tune the threshold on train, validation or test data? How do you avoid overfitting the threshold, and would you use one threshold per segment?
**Asked at:** Product cos, fintech
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 Log-loss vs Brier vs AUC: which do you choose when probabilities feed a downstream decision (bidding, pricing, risk scoring)?
**Asked at:** Ads/marketplace, fintech, Europe
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 Fraud/credit labels arrive late (chargebacks after 30-90 days). How does this affect training and evaluation, and how do you split the data?
**Asked at:** Fintech (PhonePe, Klarna-type), e-commerce
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 How do you compare two classifiers statistically? Bootstrap CI for AUC, DeLong test, McNemar test.
**Asked at:** Product cos, research-leaning, Europe
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 How do you extend ROC-AUC and calibration to multiclass problems (one-vs-rest, one-vs-one, macro/weighted)?
**Asked at:** Services, GCCs, product cos
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 What is focal loss and when does it help with class imbalance compared to class weights?
**Asked at:** CV/NLP-heavy product cos, deep learning teams
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🔴 Implement ROC-AUC from scratch in NumPy (rank-based, handling ties) and verify against sklearn.
**Asked at:** Live coding at product cos, Amazon/Microsoft-style
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 A product manager asks for one number to judge a classifier. How do you negotiate the metric and translate a confusion matrix into rupees/euros of business value?
**Asked at:** Product cos, senior roles, hiring-manager round
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🟡 You use an LLM as a classifier or judge to label data. How do you evaluate it (metrics, imbalance, agreement with humans, calibration)?
**Asked at:** GenAI-era loops, product cos (AI-era follow-up)
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Derive the Bayes-optimal threshold for a given cost matrix and explain why it needs calibrated probabilities.
**Asked at:** Fintech, senior roles, quant-style
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 What is partial AUC or recall at a fixed false-positive rate? When is full AUC the wrong objective?
**Asked at:** Fraud/security teams, senior roles
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 Selective classification (reject option) and conformal prediction: how do you give classifiers an abstain option or a coverage guarantee?
**Asked at:** Senior roles, healthcare/risk, Europe research-leaning teams
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 Temperature scaling: how does it work, why is it used for neural nets, and how does calibration of LLM classifiers (logprobs, verbalized confidence) differ?
**Asked at:** GenAI-era loops, senior DS/MLE (AI-era follow-up)
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 Code review: an LLM wrote a churn pipeline that applies SMOTE before train_test_split, reports accuracy, and tunes the threshold on the test set. List all the bugs and fix them.
**Asked at:** AI-code-review rounds, product cos (AI-era question)
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 Positive-unlabeled learning and noisy labels: when negatives are really unlabeled, how does that change metrics and training?
**Asked at:** Fraud/trust & safety, senior roles
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🔴 At 1:10,000 imbalance, when would you switch from supervised learning to anomaly detection or a hybrid approach?
**Asked at:** Fintech, security, senior roles, Europe
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 Fairness and thresholds: equalized odds vs group calibration; can you satisfy both? How do you handle per-group thresholds?
**Asked at:** Europe (regulated), fintech lending, senior roles
<!-- ANSWER_PENDING -->
