# Book 1 — Part 03: Classification Metrics, Class Imbalance, Calibration, Thresholding

**Topic:** precision/recall/F1/ROC-AUC/PR-AUC/log-loss, imbalance (SMOTE, class weights, resampling), calibration, thresholding, cost-sensitive learning
**Target:** 45 questions | **Actual:** 48 questions (⭐⭐⭐ 17, ⭐⭐ 21, ⭐ 10) | **Date:** 2026-10-20

> Dedupe pass: removed 1 cross-part duplicate(s); renumbered Q1–Q48.

---

### Q1 ⭐⭐⭐ 🟢 Why is accuracy a misleading metric on imbalanced data? Give a numeric example.
**Asked at:** Flipkart-type e-commerce, fintech, GCCs, analytics services (Tiger Analytics-type)
**Say this first (1 line):** Accuracy counts all mistakes equally, so when 99% of rows are negative, a model that never predicts positive scores 99% and catches nothing.

**Then explain:**
- Accuracy = (TP+TN)/all. It is dominated by the majority class, so it hides the failure on the class we actually care about.
- The rare class is usually the costly one (fraud, churn, disease), so we need metrics that look at it directly: recall, precision, PR-AUC, F1.
- Accuracy is only fine when classes are roughly balanced and both errors cost about the same.

**Example:** 1,000 transactions, 10 fraud. A "predict not-fraud always" model gets 990/1000 = 99% accuracy, but recall = 0/10 = 0%. The model is useless, yet the accuracy looks great.

**Code:**
```python
import numpy as np
y = np.array([1]*10 + [0]*990); pred = np.zeros(1000, int)
print((y == pred).mean(), ((pred == 1) & (y == 1)).sum() / y.sum())  # 0.99 0.0
```

**Follow-ups:**
- *What is the baseline to beat?* The majority-class rate (here 99%), plus a PR-AUC baseline equal to the prevalence.
- *What would you report instead?* Confusion matrix, precision, recall at the chosen threshold, and PR-AUC.

**Common mistakes:** Quoting accuracy without the base rate; forgetting that "dummy classifier" accuracy is the number to compare against.

### Q2 ⭐⭐⭐ 🟢 Define precision, recall, specificity and F1 from the confusion matrix. Given TP/FP/FN/TN counts, compute them.
**Asked at:** All company types
**Say this first (1 line):** Precision = of the cases I flagged, how many were right; recall = of the real positives, how many I caught; specificity = of the real negatives, how many I left alone; F1 = harmonic mean of precision and recall.

**Then explain:**
| Metric | Formula | Plain meaning |
|---|---|---|
| Precision | TP / (TP+FP) | How clean are my alerts |
| Recall (sensitivity, TPR) | TP / (TP+FN) | How many positives I catch |
| Specificity (TNR) | TN / (TN+FP) | How many negatives I correctly clear |
| F1 | 2PR / (P+R) | Single number; punishes a weak side because it is a harmonic mean |

- F1 ignores TN entirely, which is useful on imbalanced data.

**Example:** TP=80, FP=40, FN=20, TN=860 (1,000 cases).
- Precision = 80/120 = 0.667; recall = 80/100 = 0.80; specificity = 860/900 = 0.956.
- F1 = 2(0.667)(0.8)/(1.467) = 0.727. Accuracy = 940/1000 = 0.94, which flatters the model.

**Code:**
```python
TP, FP, FN, TN = 80, 40, 20, 860
p = TP/(TP+FP); r = TP/(TP+FN); s = TN/(TN+FP)
print(p, r, s, 2*p*r/(p+r))  # 0.667 0.8 0.956 0.727
```

**Follow-ups:**
- *Why harmonic mean?* It is dominated by the smaller value, so you cannot hide a recall of 0.1 behind a precision of 1.0 (arithmetic mean would give 0.55; F1 gives 0.18).
- *Which of these depend on prevalence?* Precision does; recall and specificity do not.

**Common mistakes:** Swapping precision and recall; computing "specificity" as FP rate; not defining which class is positive.

### Q3 ⭐⭐⭐ 🟢 Precision vs recall trade-off: which would you optimise for fraud, cancer screening and a spam filter, and why?
**Asked at:** Fintech, product cos, GCCs, Europe product cos
**Say this first (1 line):** It depends on which error costs more: cancer screening favours recall, spam filtering favours precision, and fraud needs a balance set by review capacity and loss per miss.

**Then explain:**
| Use case | Costly error | Optimise | Why |
|---|---|---|---|
| Cancer screening | Missing a cancer (FN) | Recall | A false alarm leads to a follow-up test; a miss can cost a life. Confirm with a second, more specific test |
| Spam filter | Blocking a real email (FP) | Precision | Losing a job offer is worse than seeing one spam |
| Fraud | Both | Recall at a precision the ops team can afford | Missed fraud loses money, but too many false blocks annoy customers and overload reviewers |

- You can trade one for the other by moving the threshold; the real decision is the cost ratio and capacity, not the metric name.
- Often a two-stage design works: high-recall first stage, then a precise second stage or human review.

**Example:** Fraud: average loss per miss Rs 8,000, cost of a manual review Rs 100. A review is worth it if P(fraud) > 100/8000 = 1.25%, so you accept very low precision and lean to recall.

**Follow-ups:**
- *What if reviewers are capped?* Pick the threshold that fills capacity (precision@k).
- *Which metric do you quote for screening?* Sensitivity at a fixed specificity.

**Common mistakes:** Saying "always maximise recall" with no cost for false alarms; ignoring that precision depends on base rate.

### Q4 ⭐⭐⭐ 🟢 What is stratified splitting / stratified k-fold and why is it essential for imbalanced data?
**Asked at:** Freshers to mid-level, services, GCCs
**Say this first (1 line):** Stratified splitting keeps the class ratio the same in every train/validation/test fold, so rare positives are spread evenly instead of by luck.

**Then explain:**
- With a random split and 2% positives, one fold can get 1 positive and another 8, which makes metrics noisy and sometimes undefined (a fold with zero positives has no recall or AUC).
- Stratified k-fold splits each class separately, then merges, so each fold has about the same prevalence.
- Use `train_test_split(..., stratify=y)` for the hold-out split too.
- It does not fix leakage: for grouped data (same customer many rows) use `StratifiedGroupKFold`; for time data use time-based splits.

**Example:** 1,000 rows, 24 positives, 5 folds.

**Code:**
```python
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold
rng = np.random.default_rng(0); y = (rng.random(1000) < 0.02).astype(int); X = np.zeros((1000, 1))
for cv in (KFold(5, shuffle=True, random_state=0), StratifiedKFold(5, shuffle=True, random_state=0)):
    print([int(y[te].sum()) for _, te in cv.split(X, y)])
# KFold:  [5, 1, 8, 4, 6]   Stratified: [4, 5, 5, 5, 5]
```

**Follow-ups:**
- *Stratify for regression?* Bin the target and stratify on bins.
- *Does stratification change the training distribution?* No, it only keeps it consistent; resampling is separate.

**Common mistakes:** Using plain KFold on imbalanced data; stratifying but then leaking via duplicate customers; stratifying a time series.

### Q5 ⭐⭐⭐ 🟡 What does ROC-AUC actually mean (probabilistic interpretation)? What is the AUC of a random model and of a perfectly inverted one?
**Asked at:** Product cos, GCCs, Europe
**Say this first (1 line):** ROC-AUC is the probability that a randomly chosen positive gets a higher score than a randomly chosen negative; random = 0.5, perfectly inverted = 0.

**Then explain:**
- It is a ranking metric: it cares about the order of scores, not their values, and not any threshold.
- Equivalent to the Mann-Whitney U statistic; ties count as half.
- AUC = 0.5 means no ranking skill (random guess, or a constant score). AUC < 0.5 means the model ranks backwards; flipping the score gives 1 - AUC. A perfectly inverted model has AUC = 0 (flip it and you have a perfect model).
- It is invariant to any monotonic transform of the scores, so it says nothing about calibration.

**Example:** If AUC = 0.78, then if I pick one fraud and one genuine transaction at random, 78% of the time the fraud has the higher score.

**Code:**
```python
import numpy as np
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0); y = (rng.random(2000) < 0.1).astype(int); s = rng.normal(size=2000) + 1.2*y
pos, neg = s[y == 1], s[y == 0]
pairwise = (pos[:, None] > neg[None, :]).mean() + 0.5*(pos[:, None] == neg[None, :]).mean()
print(pairwise, roc_auc_score(y, s), roc_auc_score(y, -s))  # 0.7803 0.7803 0.2197
```

**Follow-ups:**
- *AUC of 0.3?* The model is informative but reversed; negate the scores to get 0.7.
- *Does AUC depend on prevalence?* No, because it compares positives only against negatives.

**Common mistakes:** Saying AUC is "accuracy across thresholds"; claiming AUC is 0 for a random model; thinking AUC measures probability quality.

### Q6 ⭐⭐⭐ 🟡 ROC-AUC vs PR-AUC: when would you prefer each on an imbalanced problem, and why can ROC-AUC look deceptively good?
**Asked at:** Fintech, product cos, Europe (Klarna/Booking-type)
**Say this first (1 line):** On heavily imbalanced data I prefer PR-AUC because it focuses on the positive class and shows precision, while ROC-AUC can look great even when most alerts are false.

**Then explain:**
- ROC plots TPR vs FPR. FPR = FP / (all negatives). With a huge negative class, thousands of false positives still give a tiny FPR, so the ROC curve stays near the top-left.
- PR plots precision vs recall; precision uses FP directly, so false positives are not diluted by the number of negatives.
- PR-AUC's random baseline is the prevalence (not 0.5), so compare to that.
- Use ROC-AUC when classes are balanced or you care about both classes equally; use PR-AUC when the positive class is rare and the positive predictions are what you act on.

**Example:** 1% positives, 100,000 rows, scores with ROC-AUC 0.92. Average precision is only 0.26 (baseline 0.01). At a threshold with recall 0.84, there are ~15,800 false positives for ~830 true positives, so precision is 5%.

**Code:**
```python
import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score
rng = np.random.default_rng(0); y = (rng.random(100000) < 0.01).astype(int); s = rng.normal(size=100000) + 2.0*y
print(roc_auc_score(y, s), average_precision_score(y, s))  # ~0.92, ~0.26
```

**Follow-ups:**
- *Is PR-AUC always better?* No; it is not comparable across datasets with different prevalence, and it is noisier with few positives.
- *Is ROC-AUC then useless?* No, it is stable across prevalence, so good for comparing rankers.

**Common mistakes:** Saying "ROC-AUC is wrong for imbalance" (it is not wrong, just less sensitive to FP); forgetting PR baseline = prevalence.

### Q7 ⭐⭐⭐ 🟡 How is F1 different from ROC-AUC? Can you have high AUC and low F1?
**Asked at:** Snowflake-type product cos, services
**Say this first (1 line):** AUC measures ranking quality across all thresholds; F1 measures one chosen threshold, so yes, you can have high AUC and low F1 if the threshold is badly placed or the positive class is rare.

**Then explain:**
| | ROC-AUC | F1 |
|---|---|---|
| Needs a threshold | No | Yes |
| Input | Scores | Hard labels |
| Uses TN | Yes (via FPR) | No |
| Sensitive to prevalence | Barely | Strongly (via precision) |

- High AUC says positives tend to score above negatives; it does not say where to cut.
- With a rare positive class, even a good ranker produces many false positives at any recall level, so precision, and hence F1, is low.
- Fix: tune the threshold on validation data; report PR-AUC alongside.

**Example:** Scores with ROC-AUC 0.92 and 1% positives. At threshold 1.0: recall 0.84, precision 0.05, F1 0.094. At threshold 2.0: recall 0.48, precision 0.17, F1 0.25. Same model, F1 changes 2.5x with the threshold.

**Code:**
```python
import numpy as np
from sklearn.metrics import roc_auc_score, f1_score
rng = np.random.default_rng(0); y = (rng.random(100000) < 0.01).astype(int); s = rng.normal(size=100000) + 2.0*y
print(round(roc_auc_score(y, s), 3), [round(f1_score(y, s > t), 3) for t in (1.0, 2.0)])  # 0.92 [0.094, 0.249]
```

**Follow-ups:**
- *Can you have high F1 and low AUC?* Rarely; it is possible if F1 is measured at one lucky threshold, or the model is good only in one region of scores.
- *Which one for model selection?* AUC/PR-AUC to compare models, F1 (or cost) to evaluate the deployed threshold.

**Common mistakes:** Calling AUC a "threshold-averaged F1"; reporting AUC only and ignoring whether any usable operating point exists.

### Q8 ⭐⭐⭐ 🟡 How do you handle class imbalance? Walk through the options and how you choose between them.
**Asked at:** Nearly all loops (product, fintech, services, GCCs)
**Say this first (1 line):** First fix the metric and the split, then try class weights and threshold tuning, and only then resampling or collecting more data; I choose by validation PR-AUC and business cost.

**Then explain:**
1. **Metric and split first:** stratified CV, PR-AUC/recall@precision, not accuracy. Many "imbalance problems" are really metric problems.
2. **Threshold tuning:** move the cut-off off 0.5. Cheap, no retraining, often most of the gain.
3. **Class weights / cost-sensitive loss:** `class_weight="balanced"`, `scale_pos_weight` in XGBoost. No data changes.
4. **Resampling:** random undersampling (fast, loses data), oversampling (duplicates, overfits), SMOTE (synthetic points, risky in high-d or categorical).
5. **Algorithmic:** tree ensembles with balanced bootstrap (BalancedRandomForest), focal loss for deep nets, anomaly detection when positives are extremely rare.
6. **Data:** more minority labels, better features, active learning. Usually the biggest win.
- Note: weights/resampling shift predicted probabilities, so recalibrate if you use probabilities.

**Example (synthetic data, 3% positives, 10,000 rows, run):** Plain logistic regression AP = 0.222; with `class_weight="balanced"` AP = 0.225; SMOTE 0.225. The ranking quality is the same, because reweighting mostly shifts the threshold and the probabilities, not the order. So the cheaper fix, threshold tuning, was enough.

**Code:**
```python
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
rng = np.random.default_rng(0); n = 10000
y = (rng.random(n) < 0.03).astype(int); X = rng.normal(size=(n, 10)); X[:, :4] += 0.7 * y[:, None]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
m0 = LogisticRegression(max_iter=1000)
m1 = LogisticRegression(max_iter=1000, class_weight="balanced")
m2 = Pipeline([("smote", SMOTE(random_state=0)), ("lr", LogisticRegression(max_iter=1000))])
for m in (m0, m1, m2):
    print(round(average_precision_score(yte, m.fit(Xtr, ytr).predict_proba(Xte)[:, 1]), 3))  # 0.222 0.225 0.225
```

**Follow-ups:**
- *Do you always rebalance?* No; strong learners like gradient boosting often work well on imbalance when you tune the threshold.
- *Which do you try first?* Threshold + class weights.

**Common mistakes:** Resampling the test set; jumping to SMOTE as the default; judging with accuracy; not recalibrating afterwards.

### Q9 ⭐⭐⭐ 🟡 How does SMOTE work and what are its limitations (high dimensions, categorical data, noise, overlapping classes)?
**Asked at:** Services, GCCs, product cos
**Say this first (1 line):** SMOTE creates synthetic minority points by interpolating between a minority sample and one of its nearest minority neighbours; it works on dense numeric data and fails on high-dimensional, categorical or noisy overlapping data.

**Then explain:**
- Algorithm: pick a minority point x, pick one of its k nearest minority neighbours x', make a new point x + λ(x' - x) with λ ~ U(0,1). Repeat until the desired ratio.
- **High dimensions:** distances become uninformative, so "neighbours" are not truly close and the synthetic points land in meaningless regions.
- **Categorical data:** interpolation of one-hot codes makes no sense; use SMOTENC / SMOTEN, or avoid.
- **Noise and overlap:** SMOTE also copies noisy minority points and bridges into the majority region, blurring the boundary. Variants: Borderline-SMOTE, SMOTE+Tomek/ENN cleaning.
- It only fills the convex hull of existing minority points; it adds no new information.

**Example:** With 30 minority points in 2-D, generating 100 new points yields points lying on line segments between existing ones, all inside the original bounding box.

**Code:**
```python
import numpy as np
from sklearn.neighbors import NearestNeighbors
def smote(X_min, n_new, k=5, seed=0):
    rng = np.random.default_rng(seed)
    idx = NearestNeighbors(n_neighbors=k+1).fit(X_min).kneighbors(X_min, return_distance=False)[:, 1:]
    base = rng.integers(0, len(X_min), n_new)
    nbr = idx[base, rng.integers(0, k, n_new)]
    lam = rng.random((n_new, 1))
    return X_min[base] + lam * (X_min[nbr] - X_min[base])
Xm = np.random.default_rng(1).normal(size=(30, 2)); print(smote(Xm, 100).shape)  # (100, 2)
```

**Follow-ups:**
- *Does SMOTE help tree models?* Often little; boosting with class weights/threshold is usually as good.
- *Does it fix calibration?* No, it distorts it.

**Common mistakes:** Applying it before the split; using it on categorical/ID-like features; trusting it as a cure for too few positives.

### Q10 ⭐⭐⭐ 🟡 Where in the pipeline do you apply SMOTE or resampling? Does it touch the validation/test set? What goes wrong if you resample before the split?
**Asked at:** Services (Sigmoid-type), GCCs, product cos
**Say this first (1 line):** Resample only the training data, inside each cross-validation fold; validation and test sets must keep the real class distribution and never see synthetic points.

**Then explain:**
- Correct order: split first (stratified), then resample the training part only, then fit.
- If you resample before the split, synthetic or duplicated copies of the same minority point land in both train and validation. The model has effectively seen the validation rows, so scores are inflated (data leakage).
- Also the validation distribution no longer matches production, so precision and calibration are wrong.
- Implement with `imblearn.pipeline.Pipeline` so resampling happens only in `fit`, within each fold. The plain sklearn Pipeline does not support samplers.
- The same rule applies to scaling, imputation, feature selection.

**Example (synthetic data, 3% positives, 10,000 rows, random forest, 5-fold CV, average precision; run):** SMOTE before CV gives 0.996 (leaked); SMOTE inside the pipeline gives 0.111. The first number is fantasy.

**Code:**
```python
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
rng = np.random.default_rng(0); n = 10000
y = (rng.random(n) < 0.03).astype(int); X = rng.normal(size=(n, 10)); X[:, :4] += 0.7 * y[:, None]
rf = RandomForestClassifier(100, random_state=0, n_jobs=-1)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
Xr, yr = SMOTE(random_state=0).fit_resample(X, y)            # WRONG: resample before CV
print(cross_val_score(rf, Xr, yr, cv=cv, scoring="average_precision").mean())   # ~0.996 (leaked)
pipe = Pipeline([("smote", SMOTE(random_state=0)), ("rf", rf)])
print(cross_val_score(pipe, X, y, cv=cv, scoring="average_precision").mean())   # ~0.111 (honest)
```

**Follow-ups:**
- *Do you resample the test set?* Never.
- *How to spot the leak?* Validation score is far higher than a no-resampling baseline and collapses in production.

**Common mistakes:** `X_res, y_res = SMOTE().fit_resample(X, y)` then `cross_val_score`; tuning hyperparameters on a resampled validation set.

### Q11 ⭐⭐⭐ 🟡 Class weights vs resampling (over/under-sampling): trade-offs, and which would you try first?
**Asked at:** Product cos, fintech, GCCs
**Say this first (1 line):** I try class weights first because they are one line, use all the data and add no synthetic noise; I move to resampling only if weights do not help or training is too slow.

**Then explain:**
| | Class weights | Undersampling | Oversampling / SMOTE |
|---|---|---|---|
| Data changed | No | Drops majority rows | Duplicates / adds synthetic rows |
| Information lost | None | Yes | None (but nothing new added) |
| Overfitting risk | Low | Low | Higher (duplicates), SMOTE can blur boundary |
| Speed | Same | Faster | Slower |
| Calibration | Shifted | Shifted | Shifted |

- Class weight w on the minority multiplies its loss, which is mathematically close to oversampling by factor w, without storing copies.
- Undersampling is attractive at very large scale (billions of negatives) and in ensembles (EasyEnsemble) so each model sees different negatives.
- Not all models support weights (some KNN-style methods); then resample.
- In all cases, evaluate on untouched data and recalibrate if you need probabilities.

**Example (the 3%-positive synthetic data from Q8):** weights vs SMOTE gave AP 0.225 vs 0.225, a tie, so choose the simpler weights.

**Code:**
```python
from xgboost import XGBClassifier
neg, pos = 9700, 300                     # counts in the training data
model = XGBClassifier(scale_pos_weight=neg/pos, eval_metric="aucpr")   # not executed here; xgboost API usage only
```

**Follow-ups:**
- *Is weight = neg/pos always best?* No, it is a starting point; tune it as a hyperparameter.
- *When does undersampling beat weights?* Huge data where training cost dominates.

**Common mistakes:** Combining heavy weights and SMOTE (double correction); forgetting that both distort probabilities.

### Q12 ⭐⭐⭐ 🟡 How do you choose the classification threshold? Why is 0.5 arbitrary and how do you pick a better one?
**Asked at:** Fintech, product cos, Europe, quant-style
**Say this first (1 line):** 0.5 is only right when classes are balanced and both errors cost the same; I choose the threshold on validation data to optimise a business objective (cost, F1, or recall at a precision floor).

**Then explain:**
- The model outputs a score; the threshold is a separate decision. With 3% positives, scores rarely exceed 0.5, so 0.5 gives almost no positives.
- Ways to pick it:
  - Maximise F1 (or F-beta) over the PR curve thresholds.
  - Minimise expected cost: with calibrated probabilities, flag if p > C_FP / (C_FP + C_FN).
  - Business constraint: highest recall subject to precision >= X, or flag the top-k within review capacity.
  - Youden's J (TPR - FPR) for balanced-cost screening.
- Choose on validation data (or via CV out-of-fold predictions), then report on a separate test set. Re-check when base rate drifts.

**Example (synthetic, 3% positives, balanced logistic regression, run):** On the validation set, best-F1 threshold = 0.89, F1 = 0.379 vs F1 = 0.202 at 0.5. On a separate test set the same threshold gives F1 0.390 vs 0.210 at 0.5: the gain holds. (Here the test number came out slightly higher than validation; with few positives the gap can go either way, so do not read much into it.)

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve, f1_score
rng = np.random.default_rng(0); n = 30000
y = (rng.random(n) < 0.03).astype(int); X = rng.normal(size=(n, 10)); X[:, :4] += 0.9 * y[:, None]
tr, va, te = slice(0, 15000), slice(15000, 22500), slice(22500, 30000)
m = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X[tr], y[tr])
scores_val, scores_te = m.predict_proba(X[va])[:, 1], m.predict_proba(X[te])[:, 1]; y_val, y_te = y[va], y[te]
p, r, t = precision_recall_curve(y_val, scores_val)
f1 = 2*p*r / (p + r + 1e-12)
best_t = t[f1[:-1].argmax()]          # last p,r point has no threshold
print(best_t, f1[:-1].max(), f1_score(y_val, scores_val > 0.5), f1_score(y_te, scores_te > best_t), f1_score(y_te, scores_te > 0.5))
# 0.89 0.379 0.202 0.390 0.210
```

**Follow-ups:**
- *Why not tune on test?* It leaks; the reported metric becomes optimistic.
- *Does a threshold depend on calibration?* Cost-based thresholds need calibrated probabilities; F1-based ones do not.

**Common mistakes:** Leaving 0.5; tuning on the test set; picking a threshold once and never revisiting it after prevalence shifts.

### Q13 ⭐⭐⭐ 🟡 What is log-loss (binary cross-entropy)? Why is it preferred to accuracy for training and for comparing probabilistic models?
**Asked at:** Product cos, GCCs, Europe
**Say this first (1 line):** Log-loss is the average negative log of the probability the model gave to the true class; it rewards honest, confident-and-right probabilities and punishes confident-and-wrong ones very hard.

**Then explain:**
- Formula: `-(1/n) Σ [ y log p + (1-y) log(1-p) ]`. It is the negative log-likelihood of a Bernoulli model, so logistic regression trains on it directly.
- It is a proper scoring rule: expected loss is minimised only by reporting the true probability, so it encourages calibrated outputs.
- It is smooth and differentiable, giving usable gradients; accuracy is a step function with zero gradient almost everywhere.
- It uses probabilities, not just labels, so it separates a model that says 0.51 from one that says 0.99 when both are "correct".
- Weakness: very sensitive to outliers (one confident error), so clip probabilities (e.g. 1e-15).

**Example:** True label 1. Predicting 0.01 costs -ln(0.01) = 4.6; predicting 0.4 costs 0.92. Accuracy treats both as just "wrong".

**Code:**
```python
import numpy as np
from sklearn.metrics import log_loss
def logloss(y, p, eps=1e-15):
    p = np.clip(p, eps, 1 - eps); return -np.mean(y*np.log(p) + (1 - y)*np.log(1 - p))
y = np.array([1, 0, 1, 1, 0]); p = np.array([.9, .2, .6, .99, .5])
print(round(logloss(y, p), 4), round(log_loss(y, p), 4))  # 0.3085 0.3085
```

**Follow-ups:**
- *Baseline value?* Predicting the prior gives the entropy; on balanced data that is ln 2 = 0.693.
- *Log-loss vs Brier?* Log-loss punishes confident errors much more; Brier is bounded.

**Common mistakes:** Forgetting to clip (infinite loss); comparing log-loss across datasets with different base rates; using it as a ranking metric.

### Q14 ⭐⭐⭐ 🟡 What is model calibration and why can a model with great AUC still be badly calibrated?
**Asked at:** Fintech, ads/marketplace product cos, Europe
**Say this first (1 line):** A model is calibrated when its predicted probabilities match reality (of cases scored 0.3, about 30% are positive); AUC only checks ranking, so a monotone distortion of scores keeps AUC while ruining the probabilities.

**Then explain:**
- AUC is unchanged by any strictly increasing transform of scores. Squaring, power-transforming, or stretching probabilities keeps the order, so AUC stays the same.
- Calibration is about the values: it needs `P(y=1 | score = s) = s`.
- Why it matters: expected-value decisions (bidding, pricing, risk limits, thresholds from costs) multiply probability by money, so wrong values mean wrong decisions.
- Common causes: class weighting/resampling, tree ensembles and SVMs, overfitted deep nets, distribution shift.
- Fix post-hoc with Platt scaling or isotonic regression on held-out data.

**Example:** Same ranking, different probabilities: with true rate 10%, the original scores average 0.157 and Brier 0.074; after `p**0.3` the scores average 0.53 and Brier 0.260. AUC is 0.8496 for both.

**Code:**
```python
import numpy as np
from sklearn.metrics import roc_auc_score, brier_score_loss
rng = np.random.default_rng(0); y = (rng.random(20000) < 0.1).astype(int)
z = rng.normal(size=20000) + 1.5*y; p = 1/(1 + np.exp(-(z - 2.2))); p_bad = p**0.3
print(roc_auc_score(y, p), roc_auc_score(y, p_bad))          # identical
print(brier_score_loss(y, p), brier_score_loss(y, p_bad))    # 0.074 vs 0.260
```

**Follow-ups:**
- *How do you check it?* Reliability diagram, ECE, Brier score.
- *Does calibration change AUC?* Platt scaling keeps it exactly; isotonic can change it slightly (ties).

**Common mistakes:** Treating `predict_proba` as probability by default; calibrating on training data; reporting only AUC for a decision system.

### Q15 ⭐⭐⭐ 🟡 Fraud model with a 0.1% positive rate: design the evaluation end to end (split strategy, metrics, threshold, what you report to the business).
**Asked at:** Fintech (PhonePe, Klarna-type), e-commerce, GCC risk teams
**Say this first (1 line):** Split by time, judge with PR-AUC and recall at a fixed review budget or precision, choose the threshold on a validation window by expected cost, and report money caught, alert volume and precision, not accuracy.

**Then explain:**
- **Split:** out-of-time (train on older months, validate on next, test on latest) because fraud drifts and labels arrive late. Keep same customer/card in one side (group split). Never shuffle across time.
- **Sample size:** 0.1% means 1 fraud per 1,000. A test set of 1M rows has ~1,000 frauds; with fewer positives the metrics are very noisy, so give bootstrap confidence intervals.
- **Metrics:** PR-AUC (baseline 0.001), recall at a precision floor or at top-k, precision@k. ROC-AUC is secondary (looks high easily). Avoid accuracy.
- **Threshold:** from cost (loss per missed fraud vs review cost + customer friction) or review capacity, set on validation, frozen on test.
- **Report to business:** frauds caught (Rs value), false-alert rate per 1,000 transactions, reviewer load, comparison to the current rules, and how it moves with drift.
- **Monitoring:** feature and score drift, delayed-label recall, recalibration.

**Example (illustrative numbers, not measured):** 1M test transactions, 1,000 frauds, 2,000 alerts/day budget equivalent. At that budget the model catches 600 frauds (recall 60%) with 30% precision: that is the sentence the business wants.

**Follow-ups:**
- *Would you undersample negatives?* For training maybe; never for evaluation, and re-correct probabilities.
- *Why not ROC-AUC?* With 99.9% negatives, FPR stays tiny even when alerts are mostly wrong.

**Common mistakes:** Random split; measuring on resampled data; no confidence intervals; ignoring label delay.

### Q16 ⭐⭐⭐ 🟡 Your model reports 99% accuracy but recall on the minority class is poor. How do you debug and improve it?
**Asked at:** Postmates-type onsite, product cos, services
**Say this first (1 line):** 99% accuracy with poor minority recall means the model is mostly predicting the majority class; I would look at the confusion matrix, move the threshold, then try class weights, better features and more minority data.

**Then explain (in order):**
1. Check the base rate: if the majority is 99%, 99% accuracy equals the dummy baseline. Switch metrics to recall, precision, PR-AUC.
2. Confirm it is a ranking problem or a threshold problem: if PR-AUC/AUC is decent but recall at 0.5 is low, just lower the threshold.
3. Look at errors: are missed positives a specific segment or noisy labels?
4. Imbalance handling: class weights/`scale_pos_weight`, resampling inside CV, balanced bagging.
5. Features and data: add signals that separate the minority; get more minority examples; check label quality and leakage.
6. Model: try gradient boosting; tune for PR-AUC; recalibrate if using probabilities.
7. Validate with stratified/out-of-time CV and report precision too, since recall alone can be gamed.

**Example (hand-built illustration):** 1,000 rows, 10 positives, model catches 1 (recall 10%), accuracy 99.1%. Lowering the threshold lifts recall to 60% at 25% precision, with accuracy 97.8%: accuracy fell, usefulness rose.

**Code:**
```python
# not executed: skeleton; assumes y_val and scores from your own validation set
from sklearn.metrics import classification_report, precision_recall_curve
print(classification_report(y_val, (scores >= 0.5).astype(int)))
p, r, t = precision_recall_curve(y_val, scores)   # pick t with required recall
```

**Follow-ups:**
- *What if nothing helps?* The signal may be too weak; get better data, or reframe (anomaly detection, rules + model).
- *Does accuracy dropping worry you?* No; it is not the objective.

**Common mistakes:** Jumping straight to SMOTE; reporting only recall; tuning on the test set.

### Q17 ⭐⭐⭐ 🟡 Multiclass metrics: macro vs micro vs weighted F1. When do you pick each?
**Asked at:** Services, GCCs, product cos (NLP/classification teams)
**Say this first (1 line):** Macro-F1 averages per-class F1 equally, so it shows rare-class performance; micro pools all decisions (equals accuracy in single-label multiclass); weighted averages by class size, so it hides rare classes.

**Then explain:**
| Average | How | Use when |
|---|---|---|
| Macro | mean of per-class F1 | Every class matters equally; imbalanced data |
| Micro | pool TP/FP/FN over all classes, then F1 | Overall correctness; = accuracy for single-label |
| Weighted | per-class F1 weighted by support | Want a per-class view that reflects the real mix |

- Macro is the strictest; one bad rare class pulls it down.
- Micro and weighted are dominated by big classes.
- Report macro-F1 plus a per-class table.

**Example:** 100 samples: 90 class A, 8 class B, 2 class C. Predictions: 94 correct (A 88, B 6, C 0). Micro-F1 = 0.94, weighted = 0.93, macro = 0.57, because class C gets F1 = 0.

**Code:**
```python
import numpy as np
from sklearn.metrics import f1_score
yt = np.array([0]*90 + [1]*8 + [2]*2); yp = np.array([0]*88 + [1]*2 + [1]*6 + [0]*2 + [0]*2)
print([round(f1_score(yt, yp, average=a), 3) for a in ("micro", "macro", "weighted")])  # [0.94, 0.572, 0.93]
```

**Follow-ups:**
- *Micro-F1 vs accuracy?* Identical for single-label multiclass; differs in multilabel.
- *Which for an imbalanced product catalogue?* Macro, plus per-class recall.

**Common mistakes:** Quoting weighted-F1 and thinking rare classes are fine; confusing micro with macro.

### Q18 ⭐⭐ 🟢 What is F-beta? When would you use F2 or F0.5 instead of F1?
**Asked at:** Fintech, GCCs, product cos
**Say this first (1 line):** F-beta is the weighted harmonic mean of precision and recall where recall counts beta times as much as precision; F2 favours recall, F0.5 favours precision.

**Then explain:**
- Formula: `F_β = (1+β²) · P · R / (β²·P + R)`. β=1 gives F1.
- F2 (β=2): use when misses cost more than false alarms (screening, fraud, safety).
- F0.5 (β=0.5): use when false alarms cost more (spam blocking, content takedown, alert fatigue).
- It still ignores TN and does not replace a cost model, but is a quick way to encode asymmetry.

**Example:** P = 0.5, R = 0.9 gives F0.5 = 0.549, F1 = 0.643, F2 = 0.776. High recall is rewarded most by F2.

**Code:**
```python
from sklearn.metrics import fbeta_score
P, R = 0.5, 0.9
print([round((1+b*b)*P*R/(b*b*P+R), 3) for b in (0.5, 1, 2)])  # [0.549, 0.643, 0.776]
# fbeta_score(y_true, y_pred, beta=2)
```

**Follow-ups:**
- *Is beta chosen arbitrarily?* It should reflect the cost ratio; otherwise just minimise expected cost.
- *Does tuning the threshold for F2 move it down or up?* Down (more positives flagged).

**Common mistakes:** Swapping which of F2/F0.5 favours recall; using F-beta when explicit costs are known.

### Q19 ⭐⭐ 🟢 Implement precision, recall, F1 and a precision-recall curve from scratch in NumPy.
**Asked at:** Live coding at product cos, GCCs
**Say this first (1 line):** Sort by score descending, take cumulative TP and FP at each distinct threshold, then precision = TP/(TP+FP) and recall = TP/total positives.

**Then explain:**
- Precision, recall, F1 for fixed labels are three counts.
- For the curve, one pass after sorting gives every threshold in O(n log n).
- Collapse tied scores into a single point (take the last index of each tie group), otherwise the curve is wrong.
- Average precision = sum of (recall step) x precision, which matches sklearn's `average_precision_score`.

**Example:** 5,000 scores (5% positives, scores rounded to 1 decimal so there are many ties). My `ap` gives 0.340601, identical to sklearn. At threshold `s > 1`, `prf` gives precision 0.198, recall 0.676, F1 0.307, also identical to sklearn.

**Code:**
```python
import numpy as np
def prf(y, p):
    tp = ((p == 1) & (y == 1)).sum(); fp = ((p == 1) & (y == 0)).sum(); fn = ((p == 0) & (y == 1)).sum()
    pr = tp/(tp+fp) if tp+fp else 0.0; rc = tp/(tp+fn) if tp+fn else 0.0
    return pr, rc, (2*pr*rc/(pr+rc) if pr+rc else 0.0)
def pr_curve(y, s):
    o = np.argsort(-s, kind="stable"); y, s = y[o], s[o]
    tp = np.cumsum(y); fp = np.cumsum(1 - y)
    last = np.r_[np.diff(s) != 0, True]            # one point per distinct threshold
    tp, fp, th = tp[last], fp[last], s[last]
    return tp/(tp+fp), tp/y.sum(), th
def ap(y, s):
    p, r, _ = pr_curve(y, s); return np.sum(np.diff(np.r_[0, r]) * p)
rng = np.random.default_rng(0); y = (rng.random(5000) < 0.05).astype(int); s = np.round(rng.normal(size=5000) + 1.5*y, 1)
print(round(ap(y, s), 6), prf(y, (s > 1).astype(int)))
# 0.340601 (0.198, 0.676, 0.307): AP matches sklearn.metrics.average_precision_score; prf matches precision_recall_fscore_support
```

**Follow-ups:**
- *Why not trapezoid for PR-AUC?* Linear interpolation between PR points is too optimistic; AP uses step sums.
- *Edge cases?* No predicted positives (precision undefined, return 0 with a warning), no positives in y.

**Common mistakes:** Not handling ties; dividing by zero; sorting ascending; forgetting recall starts at 0 for the step sum.

### Q20 ⭐⭐ 🟡 Platt scaling vs isotonic regression: how each works, when each is appropriate, and why you fit them on held-out data.
**Asked at:** Fintech, ads/marketplace product cos, Europe
**Say this first (1 line):** Both learn a small mapping from the model's raw score to a true probability using held-out data: Platt fits a sigmoid (2 parameters), isotonic fits a monotone step function (non-parametric).

**Then explain:**
| | Platt scaling | Isotonic regression |
|---|---|---|
| Form | `σ(a·s + b)`, logistic regression on the score | Monotone non-decreasing staircase |
| Data needed | Little (hundreds) | More (thousands+), else overfits |
| Fits | Sigmoid-shaped distortion (SVM, boosting) | Any monotone distortion (RF, NB) |
| Effect on AUC | Unchanged | Can create ties, small change |

- **Why held-out:** the model has already fit the training data, so its training scores are over-confident; calibrating on them learns the wrong mapping. Use a separate calibration set or cross-fitting (`CalibratedClassifierCV`).
- Calibrating keeps the model; it only remaps outputs.

**Example (synthetic, 11% positives, naive Bayes with a correlated feature pair, run):** raw Brier 0.0694, ECE 0.024; Platt Brier 0.0670, ECE 0.007; isotonic Brier 0.0672, ECE 0.005. AUC is 0.886 raw and with Platt (unchanged), 0.8856 with isotonic.

**Code:**
```python
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss
rng = np.random.default_rng(0); n = 30000
y = (rng.random(n) < 0.11).astype(int); X = rng.normal(size=(n, 10)); X[:, :4] += 0.9 * y[:, None]
X[:, 4] = X[:, 0] + 0.3*rng.normal(size=n)                    # correlated feature breaks NB independence
tr, ca, te = slice(0, 15000), slice(15000, 22500), slice(22500, 30000)
nb = GaussianNB().fit(X[tr], y[tr])
p_cal, p_test = nb.predict_proba(X[ca])[:, 1], nb.predict_proba(X[te])[:, 1]; y_cal, y_test = y[ca], y[te]
logit = lambda p: np.log(np.clip(p, 1e-6, 1-1e-6) / (1 - np.clip(p, 1e-6, 1-1e-6)))
platt = LogisticRegression().fit(logit(p_cal).reshape(-1, 1), y_cal)
iso = IsotonicRegression(out_of_bounds="clip").fit(p_cal, y_cal)
p_platt = platt.predict_proba(logit(p_test).reshape(-1, 1))[:, 1]; p_iso = iso.predict(p_test)
print([round(brier_score_loss(y_test, q), 4) for q in (p_test, p_platt, p_iso)])  # [0.0694, 0.067, 0.0672]
```

**Follow-ups:**
- *Small calibration set?* Platt (or temperature scaling for deep nets).
- *Multiclass?* Temperature scaling or one-vs-rest calibration.

**Common mistakes:** Calibrating on the training set; using isotonic with tiny data; checking calibration on the same set used to fit it.

### Q21 ⭐⭐ 🟡 How do you measure calibration? Explain reliability diagrams, ECE and Brier score, and ECE's weaknesses.
**Asked at:** Product cos, fintech, Europe
**Say this first (1 line):** I check calibration with a reliability diagram (predicted vs actual rate per bin), summarise it with ECE, and score probability quality overall with the Brier score.

**Then explain:**
- **Reliability diagram:** bin predictions (e.g. 10 bins), plot mean predicted probability (x) vs observed positive rate (y). The diagonal is perfect; below it means over-confident.
- **ECE:** `Σ (n_b/n) · |acc_b - conf_b|`, the weighted average gap per bin.
- **Brier score:** mean of `(p - y)²`. Lower is better. It mixes calibration and sharpness (discrimination), so it is a proper scoring rule.
- **ECE weaknesses:** depends on the number and type of bins (equal-width vs equal-mass); noisy and biased with few samples; only the top-label gap in multiclass; ignores sharpness (predicting the base rate everywhere gets ECE near 0); not a proper scoring rule, so it cannot be optimised alone.
- Use quantile bins for skewed scores, report confidence intervals.

**Example (synthetic, 30k rows, 11% positives, 7,500-row test set, run):** Logistic regression: AUC 0.896, Brier 0.0639, ECE 0.005. Naive Bayes: AUC 0.886, Brier 0.0694, ECE 0.024, so it ranks almost as well but gives clearly worse probabilities. The same data and `ece` function are used in Q20.

**Code:**
```python
import numpy as np
def ece(y, p, bins=10):
    b = np.minimum((p * bins).astype(int), bins - 1); e = 0.0
    for k in range(bins):
        m = b == k
        if m.any(): e += m.mean() * abs(y[m].mean() - p[m].mean())
    return e
# from sklearn.calibration import calibration_curve; calibration_curve(y, p, n_bins=10, strategy="quantile")
```

**Follow-ups:**
- *Why not ECE alone?* A constant prior prediction is well calibrated but useless; pair it with AUC/Brier.
- *Brier decomposition?* Reliability - resolution + uncertainty.

**Common mistakes:** Judging calibration on training data; equal-width bins with almost all scores in one bin; comparing ECE across different bin settings.

### Q22 ⭐⭐ 🟡 Which model families tend to be poorly calibrated (RF, SVM, naive Bayes, boosted trees, deep nets) and why? Which are well calibrated?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** Logistic regression is usually well calibrated because it optimises log-loss directly; naive Bayes, SVMs, random forests, boosted trees and big neural nets are typically miscalibrated, each in its own way.

**Then explain:**
| Model | Typical pattern | Why |
|---|---|---|
| Logistic regression | Good | Trained on log-loss (proper scoring rule) |
| Naive Bayes | Too extreme (near 0/1) | Independence assumption multiplies correlated evidence |
| SVM | Not probabilities at all (margins) | Hinge loss; needs Platt scaling |
| Random forest | Under-confident, pushed away from 0 and 1 | Averaging many trees pulls scores to the middle |
| Boosted trees (AdaBoost, early GBM) | Sigmoid-shaped distortion, similar | Focus on margin; log-loss GBM is better calibrated |
| Deep nets | Over-confident | Overfit log-loss, large capacity, no regularisation (Guo et al. 2017); fix with temperature scaling |

- Calibrated or not, ranking (AUC) can still be good; recalibrate on held-out data if probabilities matter.
- It is an empirical tendency, not a law: always measure.

**Example (the 30k-row synthetic data of Q20/Q21, run):** ECE on the test set: logistic regression 0.005, random forest 0.013, naive Bayes 0.024. The RF distortion was mild on this easy data, so measure rather than assume; Platt or isotonic only trimmed RF's ECE to about 0.010 to 0.012, while for naive Bayes they cut it from 0.024 to 0.005 to 0.007 (Q20).

**Follow-ups:**
- *Why is RF under-confident?* A tree leaf can give 0 or 1, but averaging across trees that disagree rarely yields exactly 0 or 1.
- *Fix for deep nets?* Temperature scaling: divide logits by a learned T on validation data.

**Common mistakes:** Saying all tree models are miscalibrated; treating SVM scores as probabilities; calibrating without held-out data.

### Q23 ⭐⭐ 🟡 Does class weighting, SMOTE or undersampling break probability calibration? How do you correct predicted probabilities back to the true base rate?
**Asked at:** Fintech, product cos, ads teams
**Say this first (1 line):** Yes, all three shift predicted probabilities upward because the model thinks positives are more common than they are; ranking stays fine, and I correct the odds back with a prior-shift formula or recalibrate on untouched data.

**Then explain:**
- Training on a distribution with positive rate π_s while production has π means the model learns the wrong prior.
- Correction (prior shift): `odds_true = odds_model × [π/(1-π)] / [π_s/(1-π_s)]`, then `p = odds/(1+odds)`.
- For class_weight="balanced" or SMOTE to 50/50: π_s = 0.5, so multiply odds by π/(1-π).
- For undersampling negatives with keep-rate β: `p = β·p_s / (β·p_s - p_s + 1)`.
- Weights and SMOTE are only approximately equivalent to this; safest is to recalibrate (Platt/isotonic) on a validation set with the real class ratio.
- Thresholds based on ranking (top-k, F1 on real validation) do not need correction, but cost-based ones do.

**Example (synthetic, true rate 11%, run):** Balanced logistic regression predicts a mean of 0.31 (ECE 0.200, Brier 0.128). After correcting the odds by 0.112/0.888, the mean is 0.111, ECE 0.006 and Brier 0.064. AUC is 0.8963 before and after.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(0); n = 30000
y = (rng.random(n) < 0.11).astype(int); X = rng.normal(size=(n, 10)); X[:, :4] += 0.9 * y[:, None]; X[:, 4] = X[:, 0] + 0.3*rng.normal(size=n)   # same data as Q20
def correct_prior(p, pi_true, pi_train=0.5):
    odds = p / (1 - p) * (pi_true / (1 - pi_true)) / (pi_train / (1 - pi_train))
    return odds / (1 + odds)
mb = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X[:15000], y[:15000])
pb = mb.predict_proba(X[22500:])[:, 1]
print(pb.mean(), correct_prior(pb, y[:15000].mean()).mean(), y[22500:].mean())   # ~0.31 ~0.111 ~0.110
```

**Follow-ups:**
- *Does it change AUC?* No, the transform is monotone.
- *When do you not bother?* If you only use ranking or a threshold tuned on real validation data.

**Common mistakes:** Using inflated probabilities for expected-loss decisions; correcting and then calibrating again on the same resampled data; forgetting the validation set must keep the real prevalence.

### Q24 ⭐⭐ 🟡 What is cost-sensitive learning? How do you incorporate different FP and FN costs (loss weights, threshold shift, cost matrix)?
**Asked at:** Fintech, insurance, GCC risk, product cos
**Say this first (1 line):** Cost-sensitive learning builds the different costs of FP and FN into training or decisions; the simplest and often best way is to train a calibrated model and shift the threshold to `C_FP / (C_FP + C_FN)`.

**Then explain:**
- **Threshold shift:** with calibrated p, predict positive if `p·C_FN > (1-p)·C_FP`, i.e. `p > C_FP/(C_FP + C_FN)`. With C_FN = 20 x C_FP, t = 1/21 = 0.048.
- **Loss/sample weights:** weight positives by C_FN and negatives by C_FP in the loss (`class_weight`, `sample_weight`, `scale_pos_weight`). Changes the learned model; probabilities get distorted.
- **Cost matrix:** full matrix (incl. TP and TN costs/benefits), choose the action with minimum expected cost; needed for multiclass or per-case amounts (loss depends on transaction value, so use `sample_weight=amount`).
- Evaluate with total expected cost on held-out data, not accuracy.

**Example (synthetic, 6% positives, 6,000 test rows with 371 positives, run):** C_FP = 1, C_FN = 20. Total cost at 0.5: 5,762. At the theoretical threshold 0.048: 2,561. Best grid threshold 0.06: 2,459. Flagging nobody costs 7,420. Almost all the gain came from the threshold shift.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(0); n = 18000
y = (rng.random(n) < 0.06).astype(int); X = rng.normal(size=(n, 10)); X[:, :4] += 0.9 * y[:, None]
m = LogisticRegression(max_iter=1000).fit(X[:12000], y[:12000])
y_val, p_val = y[12000:], m.predict_proba(X[12000:])[:, 1]
cfp, cfn = 1, 20
t = cfp / (cfp + cfn)
def cost(y, p, th): pr = p > th; return ((pr & (y == 0)).sum() * cfp + ((~pr) & (y == 1)).sum() * cfn)
grid = np.linspace(0.02, 0.9, 89); best = grid[np.argmin([cost(y_val, p_val, g) for g in grid])]
print(cost(y_val, p_val, 0.5), cost(y_val, p_val, t), best, cost(y_val, p_val, best))   # 5762 2561 0.06 2459
```

**Follow-ups:**
- *Why does the threshold formula need calibration?* It treats p as a real probability.
- *Costs uncertain?* Sweep the ratio and show a cost curve; pick a robust region.

**Common mistakes:** Using 0.5 with asymmetric costs; reweighting and then also shifting the threshold (double count); ignoring variable per-case costs.

### Q25 ⭐⭐ 🟡 Capacity-constrained operating point: reviewers can check 500 cases a day. How do you pick the threshold and report precision@k / recall@k?
**Asked at:** Fintech, trust & safety, quant-style (Citadel-type), product cos
**Say this first (1 line):** I rank cases by score, take the top 500 per day, and report precision@500 and recall@500 on a validation set that has the real daily volume and base rate; the threshold is simply the score of the 500th case.

**Then explain:**
- Capacity is a hard constraint, so the metric is precision@k (how many of the 500 are truly bad) and recall@k (what share of all bad cases we catch).
- Do not fix a probability threshold like 0.5. Fix k, because daily volume moves. Use a fraction (top 1.2% of scored cases) or a score cut calibrated on recent days, and monitor it.
- Precision@k and recall@k are linked: `recall@k = precision@k × k / total_positives`. Both depend on the base rate, so evaluate on a time-based split at production prevalence.
- If cases have different value (amount at risk), rank by expected loss `p × amount`, not `p`.
- Spare capacity: if precision at the 500th case is still above break-even (`C_FP/(C_FP+C_FN)`), ask for more reviewers. If it is below, review fewer.

**Example (synthetic, run):** 10,000 cases, 603 positives (6.0%). Top 500 by a logistic model: precision@500 = 0.382, recall@500 = 0.317. The score cut-off is about 0.26. Random review would give precision 0.06, so lift is about 6.3.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
def at_k(y, p, k):
    top = np.argsort(-p)[:k]
    return y[top].mean(), y[top].sum() / y.sum(), p[top[-1]]   # precision@k, recall@k, cutoff
rng = np.random.default_rng(0); n = 20000
y = (rng.random(n) < 0.06).astype(int); X = rng.normal(size=(n, 6)); X[:, :3] += 0.9 * y[:, None]
m = LogisticRegression(max_iter=1000).fit(X[:10000], y[:10000])
yv, pv = y[10000:], m.predict_proba(X[10000:])[:, 1]
print(at_k(yv, pv, 500))   # (0.382, 0.317, 0.264)
```

**Follow-ups:**
- *Volume doubles tomorrow?* Keep k fixed, so the cut-off score rises. Or use a percentile rule if reviewers scale.
- *Ties at the cut-off?* Break ties randomly or by amount, and document it.

**Common mistakes:** Quoting precision/recall at 0.5; computing @k on a balanced or resampled set; ignoring that case value differs; using one day's cut-off forever.

### Q26 ⭐⭐ 🟡 Explain lift, gain and cumulative-gain charts and the KS statistic. How do you use them for churn or marketing targeting?
**Asked at:** Telecom, BFSI, services, GCCs
**Say this first (1 line):** Sort customers by score, cut them into deciles, and ask how many of the real churners sit in the top deciles versus a random pick; that is gain and lift, and KS is the biggest gap between the churner and non-churner score distributions.

**Then explain:**
- **Gain (cumulative gain):** % of all positives captured in the top x% of customers. Top 10% holding 65% of churners means gain = 0.65.
- **Lift:** gain divided by x, or precision in the top x% divided by overall base rate. Lift 6.5 at decile 1 means 6.5 times better than random.
- **Gain chart** rises above the diagonal (random); **lift chart** starts high and falls to 1 at 100%.
- **KS:** max over thresholds of `TPR - FPR` (equal to the max gap between the two cumulative score distributions). Banks like it; it is a single operating-point-free summary, 0 to 1.
- Business use: pick the cut-off where marginal cost of the offer equals marginal retention value. Stop contacting once lift in the next decile drops near the break-even lift.

**Example (synthetic churn data, base rate 6.2%, 6,000 test rows, run):** Decile 1: gain 0.612, lift 6.1. Top 2 deciles: gain 0.774. Top 5: 0.954. KS = 0.63. If a retention offer costs ₹200 and a saved customer is worth ₹3,000 (assuming every contacted churner is saved, to keep the arithmetic simple), contact while precision in the decile is above 6.7%, which is lift above about 1.08 here. Decile lifts are 6.1, 1.6, 0.86, so only the top 2 deciles clear the bar; stop after decile 2.

**Code:**
```python
import numpy as np, pandas as pd
from scipy.stats import ks_2samp
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(0); n = 18000
yy = (rng.random(n) < 0.06).astype(int); X = rng.normal(size=(n, 10)); X[:, :4] += 0.9 * yy[:, None]
m = LogisticRegression(max_iter=1000).fit(X[:12000], yy[:12000])
y, p = yy[12000:], m.predict_proba(X[12000:])[:, 1]
def gain_lift(y, p, bins=10):
    d = pd.DataFrame({"y": y, "p": p}).sort_values("p", ascending=False)
    d["dec"] = np.arange(len(d)) * bins // len(d) + 1
    g = d.groupby("dec").y.agg(["sum", "mean"])
    g["gain"] = g["sum"].cumsum() / d.y.sum()
    g["lift"] = g["mean"] / d.y.mean()
    return g
print(gain_lift(y, p).round(3).head(3))     # gain 0.612 0.774 0.860 ; lift 6.12 1.62 0.86
ks = ks_2samp(p[y == 1], p[y == 0]).statistic    # 0.63
```

**Follow-ups:**
- *Lift vs uplift?* Lift ranks by churn risk. Uplift models rank by who is changed by the offer; sure-things and lost causes waste money.
- *Does KS depend on base rate?* No, it uses class-conditional distributions, so it is stable under prevalence change.

**Common mistakes:** Computing lift on training data; reading KS as business value; targeting highest-risk customers who would not respond to the offer; deciles with ties giving uneven sizes.

### Q27 ⭐⭐ 🟡 PR-AUC: what is its random baseline, and what is the difference between average precision and trapezoidal area under the PR curve?
**Asked at:** Product cos, Europe
**Say this first (1 line):** The random baseline of PR-AUC is the prevalence (positive rate), not 0.5; and average precision is a step-wise sum, while the trapezoid rule interpolates linearly between PR points and is too optimistic.

**Then explain:**
- Random scores give precision equal to the base rate at every recall, so PR-AUC ≈ prevalence. At 1% positives, 0.05 is five times better than random.
- **Average precision (AP):** `Σ (R_n − R_{n−1}) · P_n`. Precision at each threshold, weighted by the recall step. No interpolation. This is sklearn's `average_precision_score`.
- **Trapezoid (`auc(recall, precision)`):** straight lines between points. PR curves are not linear between points (when you add one more positive precision jumps, when you add a negative it drops), so linear interpolation is biased, usually upward.
- PR-AUC is not comparable across datasets with different prevalence; ROC-AUC is better for that.
- Use PR when positives are rare and you care about positives; ROC can look fine because TN count is huge.

**Example:** y=[0,0,1,1], scores=[0.1,0.4,0.35,0.8]: AP = 0.833, trapezoid = 0.792. On the 6.2% churn data of Q26 (6,000 rows): AP 0.479, trapezoid 0.478, AP of random scores 0.058 vs base rate 0.062. With many points the gap is small; with few points it matters.

**Code:**
```python
from sklearn.metrics import average_precision_score, precision_recall_curve, auc
y, s = [0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]          # the 4-point example above
p, r, _ = precision_recall_curve(y, s)
print(average_precision_score(y, s), auc(r, p))      # 0.833 0.792
```

**Follow-ups:**
- *Why not ROC for imbalance?* FPR divides by a huge number of negatives, so thousands of false alarms barely move it.
- *Can I average PR curves across folds?* Report AP per fold with mean and std; do not interpolate curves.

**Common mistakes:** Saying baseline is 0.5; comparing AP across different base rates; using trapezoid on PR curves and reporting it as AP.

### Q28 ⭐⭐ 🟡 Undersampling vs oversampling vs hybrid methods; what are balanced random forest and EasyEnsemble and when do they help?
**Asked at:** Product cos, services
**Say this first (1 line):** Undersampling throws away majority rows, oversampling duplicates or synthesises minority rows, and balanced RF and EasyEnsemble undersample inside an ensemble so no majority data is permanently lost; they can help recall a little but they wreck calibration, and a plain strong model with the right metric is often just as good.

**Then explain:**
- **Undersampling:** fast, but you lose information. Good when there are millions of negatives.
- **Oversampling (random, SMOTE):** keeps all data but can overfit to duplicates; SMOTE interpolates between minority neighbours, which fails with noisy, high-dimensional or categorical data. Resample only inside training folds.
- **Hybrid** (SMOTE + Tomek links or ENN): oversample, then clean overlapping points at the boundary.
- **Balanced RF:** each tree is trained on a bootstrap in which the majority is undersampled to match the minority. Many trees see different negatives.
- **EasyEnsemble:** train many AdaBoost models, each on all positives plus a different random negative subset; average them.
- They help when the minority class is small and recall matters. They add no new information.
- Probabilities become inflated (the model believes prevalence is about 50%), so recalibrate.

**Example (synthetic, 20,000 rows, 2.4% positives, 8,000 test rows, run):** Plain random forest: AUC 0.893, AP 0.435, mean predicted probability 0.027. Balanced RF: AUC 0.908, AP 0.338, mean p 0.221. EasyEnsemble: AUC 0.909, AP 0.425, mean p 0.415. Resampling raised AUC slightly but did not beat the plain forest on AP, and inflated mean probabilities 8 to 15 times (true rate 2.3%).

**Code:**
```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score
from imblearn.ensemble import BalancedRandomForestClassifier, EasyEnsembleClassifier
rng = np.random.default_rng(0); n = 20000
y = (rng.random(n) < 0.024).astype(int); X = rng.normal(size=(n, 10)); X[:, :4] += 1.0 * y[:, None]
Xtr, Xte, ytr, yte = X[:12000], X[12000:], y[:12000], y[12000:]
for nm, m in (("RF", RandomForestClassifier(300, random_state=0, n_jobs=-1)),
              ("BRF", BalancedRandomForestClassifier(n_estimators=300, random_state=0, n_jobs=-1)),
              ("EE", EasyEnsembleClassifier(n_estimators=20, random_state=0))):
    p = m.fit(Xtr, ytr).predict_proba(Xte)[:, 1]
    print(nm, round(roc_auc_score(yte, p), 3), round(average_precision_score(yte, p), 3), round(p.mean(), 3))
# RF 0.893 0.435 0.027 / BRF 0.908 0.338 0.221 / EE 0.909 0.425 0.415   (imblearn pipelines resample only the training part of each CV fold)
```

**Follow-ups:**
- *Why does AP drop with balancing?* Each tree sees few negatives, so there are more false positives at the top of the ranking.
- *What first?* Better features, class weights or threshold tuning, then resampling if needed.

**Common mistakes:** SMOTE before the split; evaluating on resampled data; using the inflated probabilities as real; assuming balancing always helps.

### Q29 ⭐⭐ 🟡 MCC, balanced accuracy and Cohen's kappa: what do they fix that F1 does not?
**Asked at:** Product cos, research-leaning roles
**Say this first (1 line):** All three use the whole confusion matrix (MCC, kappa) or both class recalls (balanced accuracy), so they cannot be gamed by predicting the majority class; F1 ignores true negatives and can look great for a useless model.

**Then explain:**
- **F1** = harmonic mean of precision and recall of the positive class only. It is asymmetric and changes if you swap which class is "positive".
- **Balanced accuracy** = (TPR + TNR) / 2. Gives both classes equal weight. 0.5 means no skill.
- **MCC** = correlation between predictions and labels, from -1 to +1, using TP, TN, FP, FN. High only if the model does well on all four cells. Symmetric.
- **Cohen's kappa** = agreement beyond chance: `(p_o - p_e)/(1 - p_e)`. Corrects accuracy for the agreement you would get by chance given class frequencies.
- They are still threshold metrics: they say nothing about probabilities or costs.

**Example:** Data is 95% positive and the model predicts all positive. F1 = 0.974, looks great. MCC = 0, balanced accuracy = 0.5. On the 6.2% churn data of Q26 at threshold 0.3 (run): accuracy 0.942, F1 0.491, MCC 0.461, balanced accuracy 0.715, kappa 0.460.

**Code:**
```python
import numpy as np
from sklearn.metrics import f1_score, matthews_corrcoef, balanced_accuracy_score, cohen_kappa_score
y = np.array([1]*95 + [0]*5); pred = np.ones(100, int)       # 95% positive, model says "all positive"
print(f1_score(y, pred), matthews_corrcoef(y, pred), balanced_accuracy_score(y, pred), cohen_kappa_score(y, pred))
# 0.974 0.0 0.5 0.0
# on real scores: pred = (p > 0.3).astype(int), then the same four functions
```

**Follow-ups:**
- *Why not just use one?* Business metrics (cost, precision@k) are better; these are quick sanity checks.
- *Kappa for multiclass?* Yes; weighted kappa for ordinal labels, also used for annotator agreement.

**Common mistakes:** Reporting accuracy or F1 alone on imbalanced data; forgetting these still depend on the threshold; comparing kappa across datasets with different prevalence.

### Q30 ⭐⭐ 🟡 Precision depends on class prevalence. If the production base rate differs from validation, how do metrics change? Use Bayes to explain.
**Asked at:** Fintech, product cos, Europe
**Say this first (1 line):** TPR and FPR do not depend on prevalence, but precision does, because `precision = TPR·π / (TPR·π + FPR·(1-π))`; if production has a lower base rate than validation, precision falls even though the model is unchanged.

**Then explain:**
- Bayes: `P(y=1 | flagged) = P(flagged | y=1)·π / [P(flagged | y=1)·π + P(flagged | y=0)·(1-π)]`. The first term is sensitivity (TPR), the second is FPR.
- Prior-independent: TPR, TNR, ROC-AUC, KS. Prior-dependent: precision, F1, accuracy, PR-AUC, lift, calibration.
- Equivalent odds form: `PPV odds = (TPR/FPR) × π/(1-π)`. TPR/FPR is the positive likelihood ratio.
- If you rebalanced validation data (50/50), recompute precision with the true π from TPR and FPR, or reweight the validation rows.
- Prevalence also drifts over time, so track it and refresh thresholds.

**Example:** Sensitivity 0.90, specificity 0.95 (FPR 0.05). At π = 5%: precision = 0.045 / (0.045 + 0.0475) = 0.486. At π = 0.5%: 0.0045 / (0.0045 + 0.04975) = 0.083. Same model, precision drops from 49% to 8%.

**Code:**
```python
def ppv(tpr, fpr, pi): return tpr * pi / (tpr * pi + fpr * (1 - pi))
ppv(0.9, 0.05, 0.05), ppv(0.9, 0.05, 0.005)   # 0.486, 0.083
```

**Follow-ups:**
- *Does AUC change?* No. Precision-based metrics and calibration do.
- *How to estimate production precision before launch?* Use the true prevalence with measured TPR/FPR, or label a random production sample.

**Common mistakes:** Quoting precision from a balanced test set as if it holds in production; forgetting calibration shifts with prevalence; thinking a drop in precision means the model degraded.

### Q31 ⭐⭐ 🟡 Why can AUC be high while precision at a usable threshold is very low? Give a worked example.
**Asked at:** Fintech, product cos
**Say this first (1 line):** AUC measures ranking over all thresholds, and when negatives are huge in number a tiny false-positive rate still produces far more false alarms than true hits, so precision at any usable threshold is low.

**Then explain:**
- AUC = probability a random positive is ranked above a random negative. It never looks at how many negatives there are.
- Precision = TP / (TP + FP). FP = FPR × N_neg, which is large when N_neg is huge.
- So with prevalence 0.1%, an FPR of 5% means about 50 false alarms per true case caught.
- Fix: look at PR curve, precision@k, recall at a very low FPR (e.g. 0.1%), or partial AUC.

**Example:** 1,000,000 transactions, 0.1% fraud = 1,000 frauds, 999,000 legit. A model with AUC about 0.95 gives, at one threshold, TPR 0.80 and FPR 0.05. TP = 800. FP = 0.05 × 999,000 = 49,950. Precision = 800 / 50,750 = 1.6%. To reach 50% precision you would need FPR of about 0.08% (TP 800, FP 800), which a 0.95-AUC model may not give at that recall.

**Code:**
```python
tp = 0.80 * 1_000; fp = 0.05 * 999_000
print(tp / (tp + fp))   # 0.0158
```

**Follow-ups:**
- *Is AUC wrong then?* No, it is right about ranking; it is the wrong summary for an operating point at low prevalence.
- *What would you report?* AP, precision and recall at the review capacity, and alert volume per day.

**Common mistakes:** Presenting AUC 0.95 to business as "95% good"; ignoring alert volume; not stating prevalence next to precision.

### Q32 ⭐⭐ 🟡 Should you tune the threshold on train, validation or test data? How do you avoid overfitting the threshold, and would you use one threshold per segment?
**Asked at:** Product cos, fintech
**Say this first (1 line):** Tune the threshold on validation data (or out-of-fold predictions), never on train and never on test; the test set is used once to report the metric at the already-chosen threshold.

**Then explain:**
- **Train:** model has seen these labels, scores are overconfident, threshold will be wrong.
- **Validation / out-of-fold:** right place. Use cross-validated predictions so the threshold uses all labelled data.
- **Test:** only for the final, unbiased estimate. Tuning on it makes the reported number optimistic.
- Reduce threshold overfitting: pick a threshold on a smooth region (the cost curve is flat near the optimum), use bootstrap to see its spread, or use the theory value `C_FP/(C_FP+C_FN)` with calibrated probabilities; fix k for capacity-based rules.
- **Per segment:** only if segments have different base rates or costs and enough data in each. Calibrated probabilities with one cost-based threshold already adapt to prevalence. Per-segment thresholds multiply the variance and may raise fairness or governance issues; shrink them toward the global one if used.
- Time-based data: tune on a later validation window, not random rows.

**Example (synthetic, 6% positives, C_FP = 1, C_FN = 20, run):** On 8,000 development rows, the out-of-fold best threshold is 0.05 (cost 406 per 1,000 rows); a bootstrap puts it between 0.05 and 0.06, close to the theory value 1/21 = 0.048. On 4,000 untouched test rows the cost is 428 per 1,000 at 0.05 and 433 at the theory value. A small step up from out-of-fold, no surprise, so no leakage.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
rng = np.random.default_rng(0); n = 12000
y = (rng.random(n) < 0.06).astype(int); X = rng.normal(size=(n, 10)); X[:, :4] += 0.9 * y[:, None]
Xd, yd, Xt, yt = X[:8000], y[:8000], X[8000:], y[8000:]
model = LogisticRegression(max_iter=1000)
cfp, cfn = 1, 20
def cost(y, p, th): pr = p > th; return ((pr & (y == 0)).sum() * cfp + ((~pr) & (y == 1)).sum() * cfn)
oof = cross_val_predict(model, Xd, yd, cv=StratifiedKFold(5, shuffle=True, random_state=0), method="predict_proba")[:, 1]
grid = np.linspace(0.02, 0.9, 89)
best = grid[np.argmin([cost(yd, oof, g) for g in grid])]
pt = model.fit(Xd, yd).predict_proba(Xt)[:, 1]          # test touched once, at the chosen threshold
print(best, cost(yd, oof, best) / 8, cost(yt, pt, best) / 4)   # 0.05 405.75 427.75 (cost per 1,000 rows)
```

**Follow-ups:**
- *Test set gets reused?* Then it is a validation set; keep a fresh holdout or time-forward data.
- *Different thresholds by country?* Check calibration per segment first; if calibrated, a common threshold is usually fine.

**Common mistakes:** Picking the threshold on test, then reporting test F1; maximising F1 on a tiny validation set; separate thresholds for tiny segments; ignoring drift.

### Q33 ⭐⭐ 🟡 Log-loss vs Brier vs AUC: which do you choose when probabilities feed a downstream decision (bidding, pricing, risk scoring)?
**Asked at:** Ads/marketplace, fintech, Europe
**Say this first (1 line):** When the probability itself is used in a formula (bid = p × value, price, expected loss), I choose log-loss or Brier, which are proper scoring rules that reward calibrated probabilities, and keep AUC only as a ranking diagnostic.

**Then explain:**
- **AUC:** ranking only. Any monotone transformation of scores leaves it unchanged, so it cannot detect probabilities that are off by 3x.
- **Log-loss:** `-mean[y log p + (1-y) log(1-p)]`. Proper, heavily punishes confident mistakes. Good for bidding/pricing where tail errors are costly. Sensitive to p near 0 or 1, so clip.
- **Brier:** `mean (p - y)^2`. Proper, bounded, robust to extreme errors; decomposes into calibration + refinement.
- Also check calibration curve / ECE, and track the metric by segment, as an overall number can hide bias.
- Final judge is the downstream business metric (revenue, cost) on a holdout or A/B test.

**Example (synthetic, 10% positives, run):** Same logistic model, scores `p` and a monotone distortion `p^0.3`. AUC is 0.8964 for both. Log-loss: 0.208 vs 0.481. Brier: 0.060 vs 0.152. Only the proper scores see the miscalibration; bidding with the distorted one would overpay.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, log_loss, brier_score_loss
rng = np.random.default_rng(0); n = 20000
y = (rng.random(n) < 0.10).astype(int); X = rng.normal(size=(n, 8)); X[:, :4] += 0.9 * y[:, None]
m = LogisticRegression(max_iter=1000).fit(X[:10000], y[:10000]); yt = y[10000:]; p = m.predict_proba(X[10000:])[:, 1]
for s in (p, p**0.3):
    print(round(roc_auc_score(yt, s), 4), round(log_loss(yt, s), 3), round(brier_score_loss(yt, s), 3))
# 0.8964 0.208 0.06 / 0.8964 0.481 0.152
```

**Follow-ups:**
- *Log-loss or Brier?* Log-loss when rare-event probabilities matter (tails); Brier when you want robust and interpretable.
- *Low-prevalence data, small Brier looks good?* Compare against the baseline `π(1-π)` (Brier skill score).

**Common mistakes:** Choosing the model by AUC and then using raw scores as probabilities; reporting log-loss without clipping; ignoring that resampling changes calibration.

### Q34 ⭐⭐ 🟡 Fraud/credit labels arrive late (chargebacks after 30-90 days). How does this affect training and evaluation, and how do you split the data?
**Asked at:** Fintech (PhonePe, Klarna-type), e-commerce
**Say this first (1 line):** Recent rows are not fully labelled yet, so I split by time, leave a gap equal to the label maturity window before the test period, and treat "not yet confirmed fraud" as unknown, not as good.

**Then explain:**
- **Problem:** a transaction from 10 days ago may be labelled 0 only because no chargeback has arrived yet. Recent positive rates are underestimated (label censoring), and the model learns "recent = safe".
- **Split:** train on data older than `T - maturity` (say 90 days), validate/test on later periods whose labels are mature. Never random split.
- **Gap:** exclude rows between train end and test start so features/labels from the same event don't cross.
- **Training set:** keep only matured rows, or use survival/delay-aware labels, or give recent rows weights.
- **Evaluation:** report metrics on mature cohorts; for fresher feedback use early proxies (reviewer decisions, disputes, 30-day rate with later-adjusted estimates).
- **Production:** the deployed model is always trained on stale labels, so monitor drift and retrain on a schedule.

**Example (illustrative):** Maturity 90 days. To test in March, train on data up to the end of November, drop December, and tune on January. If you included December rows labelled today, the fraud rate there looks 30% lower than the truth.

**Code:**
```python
# not executed: skeleton; assumes a DataFrame df with event_ts and label_available_at columns
import pandas as pd
cut = pd.Timestamp("2026-06-30"); gap = pd.Timedelta(days=90)
train = df[df.event_ts < cut - gap]
valid = df[(df.event_ts >= cut) & (df.event_ts < cut + pd.Timedelta(days=30))]
# label_available_at <= snapshot date for every row in train/valid
```

**Follow-ups:**
- *Can you use the unmatured rows?* Yes for unsupervised drift checks, or with a delayed-feedback model that predicts the chance a label is still coming.
- *Why a gap?* Rows near the boundary have incomplete labels and correlated entities.

**Common mistakes:** Random k-fold; treating pending labels as negatives; evaluating on the last two weeks; leaking later information into features.

### Q35 ⭐⭐ 🟡 How do you compare two classifiers statistically? Bootstrap CI for AUC, DeLong test, McNemar test.
**Asked at:** Product cos, research-leaning, Europe
**Say this first (1 line):** Because both models are scored on the same test set, I use paired methods: a paired bootstrap CI for the AUC difference, DeLong for a fast analytic test of correlated AUCs, and McNemar for the labels at a fixed threshold.

**Then explain:**
- **Bootstrap CI:** resample test rows with replacement, compute `AUC_B - AUC_A` each time, take 2.5 and 97.5 percentiles. If the interval excludes 0, the difference is likely real. Paired = same resample for both models.
- **DeLong:** uses the U-statistic structure of AUC to estimate the covariance between two AUCs from the same data; gives a z-test. Fast, no resampling.
- **McNemar:** looks only at rows where the two models disagree: b = A right/B wrong, c = A wrong/B right; `chi2 = (|b-c|-1)^2/(b+c)`. Use for accuracy/error comparison at a threshold; use the exact binomial test when b+c is small.
- Do not use unpaired tests; do not use plain t-tests on fold scores (they are correlated).
- Statistical significance is not business significance; also state the effect size.

**Example (synthetic data with an interaction that a linear model misses, 3,000 test rows, 16% positives, run):** Logistic AUC 0.693, gradient boosting 0.861. Paired bootstrap difference 0.167, 95% CI [0.140, 0.190]. McNemar at 0.5: b = 49 (only logistic right), c = 153 (only boosting right), chi2 = 52.5, p ~ 4e-13. Both say boosting is better. (DeLong is the analytic version of the AUC test and would agree; I have not quoted its number here.)

**Code:**
```python
import numpy as np
from scipy.stats import chi2
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0); n = 9000
X = rng.normal(size=(n, 6)); z = 1.0*X[:, 0] + 2.0*X[:, 1]*X[:, 2] + 1.5*(X[:, 3] > 0.5) - 3.2
y = (rng.random(n) < 1/(1 + np.exp(-z))).astype(int)
la = LogisticRegression(max_iter=1000).fit(X[:6000], y[:6000]); gb = GradientBoostingClassifier(random_state=0).fit(X[:6000], y[:6000])
pa, pb = la.predict_proba(X[6000:])[:, 1], gb.predict_proba(X[6000:])[:, 1]; y = y[6000:]
d = []
for _ in range(1000):
    i = rng.integers(0, len(y), len(y))
    if 0 < y[i].sum() < len(y):
        d.append(roc_auc_score(y[i], pb[i]) - roc_auc_score(y[i], pa[i]))
print(np.percentile(d, [2.5, 97.5]))                 # about [0.140, 0.190]
ca, cb = (pa > .5) == y, (pb > .5) == y
b, c = int((ca & ~cb).sum()), int((~ca & cb).sum())  # 49, 153
print(b, c, chi2.sf((abs(b-c)-1)**2/(b+c), 1))        # statsmodels.stats.contingency_tables.mcnemar also works
```

**Follow-ups:**
- *Several models?* Correct for multiple comparisons or use a Friedman/Nemenyi-style procedure.
- *Why bootstrap rows, not folds?* More resampling units; for grouped data bootstrap whole groups.

**Common mistakes:** Comparing two separate CIs for overlap; ignoring pairing; testing many models on the same test set; calling a 0.002 AUC gap "significant" without business meaning.

### Q36 ⭐⭐ 🟡 How do you extend ROC-AUC and calibration to multiclass problems (one-vs-rest, one-vs-one, macro/weighted)?
**Asked at:** Services, GCCs, product cos
**Say this first (1 line):** For multiclass I compute one-vs-rest (class k against all others) or one-vs-one (every pair of classes) ROC-AUC and average them, macro (equal weight per class) or weighted (by class frequency); for calibration I use multiclass log-loss/Brier and per-class reliability curves.

**Then explain:**
- **OvR:** K binary AUCs using `P(class k)` as the score. Simple, depends on class prevalence in the "rest" group.
- **OvO:** K(K-1)/2 pairwise AUCs, less sensitive to imbalance (Hand & Till). More pairs to compute.
- **Macro:** treats rare classes equally, which shows weak classes. **Weighted:** reflects class mix and hides weak minority classes.
- **Calibration:** top-label calibration (confidence vs accuracy) or classwise reliability curves; fix with temperature scaling or one-vs-rest isotonic plus renormalising.
- In sklearn pass `multi_class="ovr"` or `"ovo"` with predict_proba (rows summing to 1).

**Example (synthetic, 4 classes 70/20/7/3%, logistic regression, run):** Per-class OvR AUC: 0.895, 0.908, 0.844, 0.866. Macro OvR 0.878, weighted OvR 0.893, macro OvO 0.830, weighted OvO 0.868. Log-loss 0.539. The weak 7% class is visible mainly in the macro averages and the per-class list.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, log_loss
rng = np.random.default_rng(0); n = 12000
y = rng.choice(4, n, p=[.70, .20, .07, .03]); X = rng.normal(size=(n, 6))
for k in range(4): X[y == k, k] += [1.5, 1.5, 0.8, 1.2][k]
model = LogisticRegression(max_iter=1000).fit(X[:8000], y[:8000]); Xte, yte = X[8000:], y[8000:]
P = model.predict_proba(Xte)
print(roc_auc_score(yte, P, multi_class="ovr", average="macro"))      # 0.878
print(roc_auc_score(yte, P, multi_class="ovo", average="weighted"))   # 0.868
print(log_loss(yte, P))                                               # 0.539
```

**Follow-ups:**
- *Which average to report?* Macro for fairness across classes, plus per-class table.
- *Why OvO?* It is not affected by how big the "rest" class is.

**Common mistakes:** Passing hard labels to roc_auc_score; reporting weighted average only; assuming binary calibration plots extend directly; averaging scores that are not probabilities.

### Q37 ⭐⭐ 🟡 What is focal loss and when does it help with class imbalance compared to class weights?
**Asked at:** CV/NLP-heavy product cos, deep learning teams
**Say this first (1 line):** Focal loss multiplies cross-entropy by `(1 - p_t)^γ` so easy, well-classified examples contribute almost nothing and the gradient is dominated by hard examples; it helps when a flood of easy negatives drowns the signal, as in object detection, and it is not the same as class weights.

**Then explain:**
- `FL = -α_t (1 - p_t)^γ log(p_t)`, where `p_t` is the probability of the true class. γ = 0 gives cross-entropy; γ = 2 is typical (RetinaNet).
- A negative with p_t = 0.99 has its loss cut by 10,000x (γ = 2), a hard one at p_t = 0.5 by only 4x.
- **Class weights** rescale by class, regardless of difficulty. **Focal** rescales by difficulty, regardless of class. α in focal loss adds class weighting.
- Helps: dense detection with 1:1000 foreground/background, deep nets on noisy easy-negative data. Often little gain on tabular GBMs.
- Side effect: predicted probabilities are not calibrated (under-confident/spread); recalibrate if you use p.

**Example (synthetic, 10% positives, logistic regression trained with NumPy/SciPy L-BFGS, 10,000 test rows, run):** BCE: AUC 0.8964, AP 0.580, mean p 0.103 (base rate 0.100). Focal γ=2 (no α): AUC 0.8964, AP 0.580, mean p 0.238. Weighted BCE (positive weight 9): AUC 0.8963, AP 0.579, mean p 0.303. The ranking is the same; focal and weights both inflate probabilities.

**Code:**
```python
import numpy as np
from scipy.optimize import minimize
from sklearn.metrics import roc_auc_score
def focal_loss(p, y, gamma=2.0, alpha=0.25):
    p = np.clip(p, 1e-9, 1 - 1e-9)
    pt = np.where(y == 1, p, 1 - p)
    at = np.where(y == 1, alpha, 1 - alpha)
    return -(at * (1 - pt) ** gamma * np.log(pt)).mean()
print(focal_loss(np.array([.9, .1, .5]), np.array([1, 0, 1])))   # 0.0148 (easy cases contribute almost nothing)
# Training a logistic model with it: analytic gradient dL/dz = s * (1-pt)^g * (g*pt*log(pt) - (1-pt)), s = +1 for y=1, -1 for y=0
rng = np.random.default_rng(0); n = 20000
y = (rng.random(n) < 0.10).astype(int); X = rng.normal(size=(n, 8)); X[:, :4] += 0.9 * y[:, None]
Xb = np.c_[np.ones(n), X]; tr, te = slice(0, 10000), slice(10000, 20000)
sig = lambda z: 1 / (1 + np.exp(-np.clip(z, -500, 500)))
def fit(gamma=0.0, w1=1.0):
    A, t = Xb[tr], y[tr]
    def f(b):
        p = np.clip(sig(A @ b), 1e-12, 1 - 1e-12); pt = np.where(t == 1, p, 1 - p); w = np.where(t == 1, w1, 1.0)
        s = np.where(t == 1, 1.0, -1.0)
        return -(w * (1 - pt) ** gamma * np.log(pt)).mean(), A.T @ (w * s * (1 - pt) ** gamma * (gamma * pt * np.log(pt) - (1 - pt))) / len(t)
    return minimize(f, np.zeros(A.shape[1]), jac=True, method="L-BFGS-B").x
for nm, kw in (("BCE", {}), ("focal g=2", dict(gamma=2.0)), ("weighted w=9", dict(w1=9.0))):
    p = sig(Xb[te] @ fit(**kw)); print(nm, round(roc_auc_score(y[te], p), 4), round(p.mean(), 3))   # mean p 0.103 / 0.238 / 0.303
```

**Follow-ups:**
- *Does focal loss fix imbalance for tabular data?* Rarely beyond threshold tuning and GBM weights; test it.
- *How to pick γ?* Cross-validate (0, 1, 2, 5).

**Common mistakes:** Thinking it is a drop-in better class weight; using focal probabilities for cost decisions without recalibration; copying α=0.25 blindly.

### Q38 ⭐⭐ 🔴 Implement ROC-AUC from scratch in NumPy (rank-based, handling ties) and verify against sklearn.
**Asked at:** Live coding at product cos, Amazon/Microsoft-style
**Say this first (1 line):** AUC equals the Mann-Whitney U statistic: rank all scores (average ranks for ties), sum the ranks of the positives, subtract `n1(n1+1)/2`, and divide by `n1·n0`; it is O(n log n) from the sort.

**Then explain:**
- AUC = P(score of random positive > score of random negative) + 0.5 × P(tie).
- Ranks: smallest score gets rank 1; tied scores get the average of their ranks. This handles ties exactly as sklearn does.
- Formula: `AUC = (R_pos - n1(n1+1)/2) / (n1 · n0)`, where R_pos is the sum of positive ranks.
- Brute-force pair counting is O(n1·n0), too slow for big data.
- Edge case: if only one class is present, AUC is undefined.

**Example:** y=[0,1,0,1], scores=[0.5,0.5,0.1,0.9]. Pairs: (pos 0.5 vs neg 0.5) tie = 0.5; (0.5 vs 0.1) = 1; (0.9 vs 0.5) = 1; (0.9 vs 0.1) = 1. AUC = 3.5/4 = 0.875. Both my function and sklearn give 0.875. On 500 random rows with 444 duplicate scores, both give 0.72656.

**Code:**
```python
import numpy as np
from scipy.stats import rankdata
from sklearn.metrics import roc_auc_score

def auc_np(y, s):
    y = np.asarray(y); r = rankdata(s)          # average ranks for ties
    n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: raise ValueError("need both classes")
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

rng = np.random.default_rng(0)
y = rng.integers(0, 2, 500); s = np.round(rng.normal(y, 1), 1)   # many ties
print(auc_np(y, s), roc_auc_score(y, s))   # 0.7265616161616162 both
```

**Follow-ups:**
- *Without scipy?* Sort, then compute average ranks with a loop over tie groups (`np.unique` with `return_inverse`, `bincount`).
- *Complexity?* O(n log n). Memory O(n).

**Common mistakes:** Using ordinal ranks (argsort of argsort) so ties are broken arbitrarily; forgetting the n1(n1+1)/2 term; O(n²) loops; not handling single-class input.

### Q39 ⭐ 🟡 A product manager asks for one number to judge a classifier. How do you negotiate the metric and translate a confusion matrix into rupees/euros of business value?
**Asked at:** Product cos, senior roles, hiring-manager round
**Say this first (1 line):** I would not give one abstract metric; I would ask what decision the model drives, put a rupee or euro value on each cell of the confusion matrix, and use expected value per 1,000 cases at the chosen threshold as the headline, with precision and recall as supporting numbers.

**Then explain:**
- **Step 1:** ask the PM what action follows a positive (call, block, review) and its cost; and what a missed case costs.
- **Step 2:** build a value matrix: TP benefit, FP cost, FN cost, TN usually 0. Include capacity and uncertainty in the numbers.
- **Step 3:** choose the threshold that maximises expected value (`p > C_FP / (C_FP + C_FN)` for calibrated p), then report precision, recall, alerts per day.
- **Step 4:** show a sensitivity range (costs +/- 30%) so the PM sees how stable the choice is.
- Keep a guardrail metric (complaints, false-block rate) as a constraint.
- AUC and F1 remain model-selection tools, not business metrics.

**Example (hand-computed, assumed numbers):** Retention offer to 10,000 customers: TP 300, FP 700, FN 200, TN 8,800. Offer costs ₹200 per contact; a saved customer is worth ₹3,000 and the offer works 40% of the time (₹1,200 expected). Value = 300 × (1,200 − 200) − 700 × 200 = ₹300,000 − ₹140,000 = ₹160,000, or ₹16 per customer scored. FN has no cash cost here but is an opportunity loss, which I mention explicitly.

**Code:**
```python
tp, fp, fn, tn = 300, 700, 200, 8800
value = tp * (0.4 * 3000 - 200) - fp * 200       # 160000 = Rs 16 per customer scored
print(value, value / (tp + fp + fn + tn))        # 160000 16.0
```

**Follow-ups:**
- *PM insists on accuracy?* Show that "predict nobody" gets 95% accuracy and ₹0 value.
- *Costs unknown?* Sweep the cost ratio and pick a robust threshold; confirm with an A/B test.

**Common mistakes:** Treating FP and FN as equal; leaving out capacity; presenting rupee value without stating assumptions; assuming the offer always works.

### Q40 ⭐ 🟡 You use an LLM as a classifier or judge to label data. How do you evaluate it (metrics, imbalance, agreement with humans, calibration)?
**Asked at:** GenAI-era loops, product cos (AI-era follow-up)
**Say this first (1 line):** I treat the LLM like any classifier: build a human-labelled golden set that keeps the real class mix, measure precision, recall and per-class metrics with confidence intervals, check agreement with humans using Cohen's kappa against the human-human ceiling, and test calibration and bias.

**Then explain:**
- **Golden set:** a few hundred to thousands of examples, labelled by at least two humans, with disagreements adjudicated. Stratify so rare classes have enough samples; keep a separate set for prompt tuning and a frozen test set.
- **Metrics:** per-class precision/recall/F1, confusion matrix, PR-AUC if you have scores. With imbalance, never report accuracy only. Bootstrap CIs.
- **Agreement:** Cohen's kappa (LLM vs human) compared with human-human kappa. LLM agreement below human-human agreement means the task or rubric is ambiguous.
- **Calibration:** verbalised confidence and logprobs are often overconfident; check a reliability curve and recalibrate on the golden set.
- **Judge biases:** position bias (prefers first answer), verbosity bias, self-preference; test by swapping order and varying length, and use temperature 0 with multiple runs for stability.
- Re-run on prompt or model version change; use human spot checks in production.

**Example (hand-built):** 200 items, human labels vs LLM labels: 85% agreement but kappa only 0.70. Here both the humans and the LLM label half the items positive, so chance agreement is 50% and kappa = (0.85 - 0.50) / (1 - 0.50) = 0.70. If humans agree with each other at kappa 0.78 (an assumed figure), the LLM is fairly close to the human ceiling.

**Code:**
```python
import numpy as np
from sklearn.metrics import cohen_kappa_score, classification_report
human = np.array([1]*100 + [0]*100); llm = human.copy()
llm[:15] = 0; llm[100:115] = 1                    # 30 disagreements, 50/50 marginals kept
print((human == llm).mean(), cohen_kappa_score(human, llm))   # 0.85 0.7
print(classification_report(human, llm))
```

**Follow-ups:**
- *LLM labels as training data?* Check label noise per class first; noisy labels bias both training and metrics.
- *Prompt tuned on the test set?* Then the number is optimistic; keep a frozen holdout.

**Common mistakes:** Judging with no human labels; using the same examples for prompt tuning and reporting; trusting verbalised confidence; ignoring position bias in pairwise judges.

### Q41 ⭐ 🔴 Derive the Bayes-optimal threshold for a given cost matrix and explain why it needs calibrated probabilities.
**Asked at:** Fintech, senior roles, quant-style
**Say this first (1 line):** Predict positive when the expected cost of predicting positive is lower than predicting negative; solving for p gives `t* = (C_FP - C_TN) / [(C_FP - C_TN) + (C_FN - C_TP)]`, which is only right if p is the true probability.

**Then explain:**
- Let p = P(y=1 | x). Expected cost of predicting 1: `(1-p)·C_FP + p·C_TP`. Predicting 0: `p·C_FN + (1-p)·C_TN`.
- Predict 1 when `(1-p)C_FP + pC_TP < pC_FN + (1-p)C_TN`.
- Rearranging: `p (C_FN - C_TP) > (1-p)(C_FP - C_TN)`, so `p > (C_FP - C_TN) / [(C_FP - C_TN) + (C_FN - C_TP)]`.
- With C_TP = C_TN = 0: `t* = C_FP / (C_FP + C_FN)`. Equivalent odds form: `p/(1-p) > C_FP/C_FN`.
- Calibration: the rule multiplies p by costs. If p is 3x too high, you flag too many; ranking-only quality (AUC) does not help. Without calibrated p, tune the threshold empirically on validation.
- Correct costs must be relative to the baseline (use regret: only costs that differ across actions matter).

**Example:** C_FP = 1, C_FN = 20: t* = 1/21 = 0.0476. A transaction with p = 0.06 is flagged. If the model is inflated 3x, a true 0.02 appears as 0.06 and gets flagged wrongly.

**Code:**
```python
def t_star(cfp, cfn, ctp=0, ctn=0): return (cfp - ctn) / ((cfp - ctn) + (cfn - ctp))
t_star(1, 20)   # 0.0476
```

**Follow-ups:**
- *Reward for TP?* Include it as negative C_TP.
- *Multiclass?* Pick the class with min expected cost: `argmin_a Σ_k p_k C(a, k)`.

**Common mistakes:** Using 0.5; applying the formula to resampled or uncalibrated scores; including sunk costs; forgetting a model's probabilities depend on the training prior.

### Q42 ⭐ 🔴 What is partial AUC or recall at a fixed false-positive rate? When is full AUC the wrong objective?
**Asked at:** Fraud/security teams, senior roles
**Say this first (1 line):** Partial AUC is the area under the ROC curve only up to a small false-positive rate (say 1%); I use it, or recall at a fixed FPR, when only the low-FPR corner of the curve is operationally usable, because full AUC also rewards performance at FPRs you would never deploy.

**Then explain:**
- Full AUC gives equal weight to all FPRs, including FPR 50%, which in fraud or security means millions of false alarms.
- **Partial AUC:** `∫_0^f TPR d(FPR)`. sklearn's `roc_auc_score(max_fpr=f)` returns the McClish-standardised value (0.5 = chance, 1 = perfect).
- **Recall at fixed FPR:** simpler to explain: "we catch 33% of fraud at 1% false-alarm rate."
- Two models with similar AUC can differ a lot in the low-FPR region, so train/tune for that region (e.g. top-heavy losses, weighting hard negatives).
- Estimates at tiny FPR are noisy; need enough positives and negatives; give bootstrap CIs.
- Also consider precision@k when capacity is fixed.

**Example (synthetic, 1.3% positives, 201 test positives, run):** Logistic regression: AUC 0.767, TPR at 1% FPR 0.378, standardised pAUC (FPR ≤ 1%) 0.672. Random forest: AUC 0.786, TPR at 1% FPR 0.373, pAUC 0.673. Full AUC says the forest is clearly better (+0.02), but in the corner where we would actually operate they are the same. With only 201 positives the low-FPR estimates are noisy (a few cases move TPR by a point), so put a bootstrap CI on them.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, roc_curve
rng = np.random.default_rng(0); n = 30000
y = (rng.random(n) < 0.013).astype(int); X = rng.normal(size=(n, 8))
X[:, :3] += 0.4 * y[:, None]; X[:, 3] += 4.0 * y * (X[:, 4] > 0.5)
tr, te = slice(0, 15000), slice(15000, 30000)
for nm, m in (("LR", LogisticRegression(max_iter=1000)), ("RF", RandomForestClassifier(200, min_samples_leaf=5, random_state=0, n_jobs=-1))):
    s = m.fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]; yt = y[te]
    fpr, tpr, _ = roc_curve(yt, s)
    print(nm, round(roc_auc_score(yt, s), 3), round(np.interp(0.01, fpr, tpr), 3), round(roc_auc_score(yt, s, max_fpr=0.01), 3))
# LR 0.767 0.378 0.672 / RF 0.786 0.373 0.673
```

**Follow-ups:**
- *Is pAUC the same as AUC/100?* No; it is rescaled so 0.5 means random.
- *Alternative?* Precision@k or recall at a fixed alert budget.

**Common mistakes:** Choosing by full AUC when the operating FPR is tiny; reporting TPR at an FPR with only a handful of negatives behind it; forgetting the standardisation.

### Q43 ⭐ 🔴 Selective classification (reject option) and conformal prediction: how do you give classifiers an abstain option or a coverage guarantee?
**Asked at:** Senior roles, healthcare/risk, Europe research-leaning teams
**Say this first (1 line):** Selective classification lets the model abstain on low-confidence cases and trade coverage for accuracy; conformal prediction wraps any model so its prediction sets contain the true label with a chosen probability (e.g. 90%), assuming exchangeable data.

**Then explain:**
- **Reject option:** abstain if `max p < τ`; send to a human. Plot **risk-coverage curve**: error rate vs fraction of cases answered. Pick τ from the cost of abstaining vs erring. Needs reasonably calibrated confidence.
- **Split conformal (classification):** hold out a calibration set; score `s = 1 − p(true class)`; take the `⌈(n+1)(1−α)⌉/n` quantile q; the prediction set is `{k : 1 − p_k ≤ q}`. Guarantee: coverage ≥ 1−α on average, for any model, under exchangeability.
- Set size is the uncertainty signal: size 1 means confident, size 0 or ≥ 2 means abstain or escalate.
- The guarantee is marginal, not per-class or per-segment; for imbalance use class-conditional conformal.
- Breaks under distribution shift.

**Example (synthetic, 3 classes 50/30/20%, overlapping, α = 0.1, 4,000 test rows, run):** Conformal threshold q = 0.808 gave 90.3% coverage on test and average set size 1.62. Selective version of the same model: accuracy 0.713 on all cases, 0.765 at 82% coverage, 0.834 at 57% coverage, 0.906 at 36% coverage (answering only the most confident cases).

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(0); n = 12000
y = rng.choice(3, n, p=[.5, .3, .2]); X = rng.normal(size=(n, 5))
for k in range(3): X[y == k, k] += 1.2
model = LogisticRegression(max_iter=1000).fit(X[:4000], y[:4000])
Xcal, ycal, Xtest, ytest = X[4000:8000], y[4000:8000], X[8000:], y[8000:]
Pc = model.predict_proba(Xcal); sc = 1 - Pc[np.arange(len(ycal)), ycal]
n = len(sc); q = np.quantile(sc, np.ceil((n + 1) * 0.9) / n, method="higher")
sets = (1 - model.predict_proba(Xtest)) <= q     # boolean matrix: label in set
print(q, sets[np.arange(len(ytest)), ytest].mean(), sets.sum(1).mean())   # 0.808 0.903 1.62
```

**Follow-ups:**
- *Is conformal calibration?* No; it guarantees coverage, not probability accuracy.
- *Cost of abstention?* Human review cost vs the cost of an error.

**Common mistakes:** Calibrating conformal on training data; claiming conditional coverage; ignoring shift; using uncalibrated scores for the reject threshold.

### Q44 ⭐ 🔴 Temperature scaling: how does it work, why is it used for neural nets, and how does calibration of LLM classifiers (logprobs, verbalized confidence) differ?
**Asked at:** GenAI-era loops, senior DS/MLE (AI-era follow-up)
**Say this first (1 line):** Temperature scaling divides the logits by one learned number T before the softmax, fitted on a validation set by minimising log-loss; it fixes the overconfidence of modern neural nets without changing their accuracy or ranking.

**Then explain:**
- `p = softmax(z / T)`. T > 1 softens (less confident); T < 1 sharpens. One parameter, so it hardly overfits a small validation set.
- Argmax does not change, so accuracy and AUC stay identical; log-loss, Brier and ECE improve (Guo et al. 2017 showed modern deep nets are overconfident).
- Why nets: large capacity and training to near-zero training loss push logits large.
- Limits: it assumes miscalibration is uniform; for non-uniform shapes use Platt, isotonic or vector scaling. Must be re-fitted after distribution shift.
- **LLM classifiers:** token **logprobs** of the label token can be used as probabilities (and temperature-scaled), but RLHF/instruction tuning often makes them overconfident. **Verbalised confidence** ("I'm 90% sure") is coarse, clustered at round numbers, and usually overconfident; calibrate it with a held-out labelled set, or use self-consistency (agreement across samples). Closed APIs may not expose logprobs.

**Example (synthetic, run):** Weakly regularised logistic regression overfit on 300 rows with 40 features (5 useful): fitted T = 1.81. Test log-loss 0.641 to 0.545; AUC 0.8051 before and after (unchanged).

**Code:**
```python
import numpy as np
from scipy.optimize import minimize_scalar
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
rng = np.random.default_rng(0); n = 1300
X = rng.normal(size=(n, 40)); w = np.zeros(40); w[:5] = 1.0; y = (rng.random(n) < 1/(1 + np.exp(-(X @ w)))).astype(int)
Xtr, ytr, Xv, yv, Xte, yte = X[:300], y[:300], X[300:800], y[300:800], X[800:], y[800:]
m = LogisticRegression(C=100, max_iter=5000).fit(Xtr, ytr)
sig = lambda z: 1 / (1 + np.exp(-np.clip(z, -500, 500)))
zv, z_test = m.decision_function(Xv), m.decision_function(Xte)
T = minimize_scalar(lambda T: log_loss(yv, sig(zv / T)), bounds=(0.1, 20), method="bounded").x
p_test = sig(z_test / T)    # binary case; use softmax(z / T) for multiclass
print(T, log_loss(yte, sig(z_test)), log_loss(yte, p_test), roc_auc_score(yte, p_test))   # 1.81 0.641 0.545 0.805
```

**Follow-ups:**
- *Why not retrain with label smoothing?* That also helps; temperature scaling is a post-hoc one-parameter fix.
- *LLM calibration check?* Reliability diagram on labelled data, per prompt version.

**Common mistakes:** Fitting T on training data; expecting it to improve accuracy; assuming verbalised confidence is calibrated; forgetting to refit after fine-tuning or drift.

### Q45 ⭐ 🔴 Code review: an LLM wrote a churn pipeline that applies SMOTE before train_test_split, reports accuracy, and tunes the threshold on the test set. List all the bugs and fix them.
**Asked at:** AI-code-review rounds, product cos (AI-era question)
**Say this first (1 line):** Four bugs: SMOTE before the split leaks synthetic copies of test points into training, accuracy is meaningless at this imbalance, the threshold is tuned on the test set, and the evaluation set is resampled so it no longer reflects reality.

**Buggy snippet:**
```python
# not executed as-is: a code-review fragment (imports/data are those of the fixed code below); the run is reported in the Example
X_res, y_res = SMOTE().fit_resample(X, y)                  # bug 1
Xtr, Xte, ytr, yte = train_test_split(X_res, y_res)        # test is now synthetic/balanced
clf = LogisticRegression().fit(Xtr, ytr)
p = clf.predict_proba(Xte)[:, 1]
best_t = max(np.linspace(0, 1, 101), key=lambda t: f1_score(yte, p > t))   # bug 3
print(accuracy_score(yte, p > best_t))                     # bug 2
```

**Then explain (bugs):**
- **Resampling before the split:** synthetic points are interpolations of real ones, so near-copies land in both train and test, which inflates scores. Also the test set no longer has the true prevalence.
- **Accuracy:** with about 9% positives, "predict all zero" scores about 91%.
- **Threshold on test:** the reported number is optimistic; tune on out-of-fold predictions.
- **Not stratified, no random_state:** split can have different positive rates; results are not reproducible.
- **SMOTE inflates probabilities:** if probabilities are used, they need recalibration.
- Missing: no baseline, no CIs, no time-based split if there is a time dimension (churn has one), possible customer-ID leakage if a customer appears twice.

**Fixed code (standalone, with a synthetic dataset standing in for the churn data):**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_predict, StratifiedKFold
from sklearn.metrics import f1_score, average_precision_score
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
rng = np.random.default_rng(0); n = 10000
y = (rng.random(n) < 0.09).astype(int); X = rng.normal(size=(n, 10)); X[:, :4] += 0.7 * y[:, None]
pipe = Pipeline([("smote", SMOTE(random_state=0)), ("clf", LogisticRegression(max_iter=2000))])
Xd, Xtest, yd, ytest = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
oof = cross_val_predict(pipe, Xd, yd, cv=StratifiedKFold(5, shuffle=True, random_state=0), method="predict_proba")[:, 1]
t = max(np.linspace(.05, .95, 91), key=lambda g: f1_score(yd, oof > g))
pipe.fit(Xd, yd); pt = pipe.predict_proba(Xtest)[:, 1]      # test used once
print(t, f1_score(ytest, pt > t), average_precision_score(ytest, pt))   # 0.76 0.407 0.349
```

**Example (run, synthetic data with 9.4% positives in the full set and in the stratified test split):** Buggy pipeline: accuracy 0.77, recall 0.89 and F1 0.79 on a resampled, balanced test set (the buggy snippet's imports and data as in the fixed code). Fixed pipeline on a real-prevalence test set: threshold 0.76, F1 0.407, precision 0.370, recall 0.452, AP 0.349. Always-negative accuracy on the real test set is 0.906, so the buggy accuracy of 0.77 is not even comparable, and the buggy F1 of 0.79 is nearly double the honest 0.41.

**Follow-ups:**
- *Is the fixed F1 "worse"?* It is honest. The buggy number measured a different, easier problem.
- *Better than SMOTE?* Try class weights and threshold tuning first.

**Common mistakes:** Believing any preprocessing "fit" step is safe before the split; tuning many things on the same test set; reporting accuracy.

### Q46 ⭐ 🔴 Positive-unlabeled learning and noisy labels: when negatives are really unlabeled, how does that change metrics and training?
**Asked at:** Fraud/trust & safety, senior roles
**Say this first (1 line):** In PU learning you only have confirmed positives and an unlabeled pool that mixes positives and negatives, so treating unlabeled as negative biases everything: probabilities are too low, precision looks too low, and recall is overstated; I either estimate the label frequency (Elkan-Noto) or use PU-aware risk estimators.

**Then explain:**
- **Setting:** s = 1 means labelled positive; y is unknown. A classifier trained on s versus not-s estimates `P(s=1|x) = c · P(y=1|x)`, where c = label frequency (chance a true positive is labelled), assuming labels are selected at random (SCAR).
- **Elkan-Noto:** estimate c as the mean prediction on held-out labelled positives, then `P(y=1|x) = P(s=1|x) / c`. Ranking is unchanged, only scale.
- **Other methods:** unbiased/non-negative PU risk with a known class prior; bagging PU; spy method for reliable negatives.
- **Metrics:** precision measured against s understates real precision (unlabelled positives counted as FP). AUC against s is lower than AUC against y. Use a clean labelled sample or class prior estimates.
- **Noisy labels (general):** loss correction, small-loss selection, co-teaching, robust losses (MAE, symmetric CE), relabel a clean subset. Check if noise depends on class or features.
- SCAR often fails (only easy cases get labelled), which biases c.

**Example (synthetic, run):** 10,000 rows, true prevalence 21%, only 30% of positives labelled (labelled prevalence 6.3%). Fitted c = 0.222 (true 0.3; it is biased low because the classes overlap a little, so a labelled positive does not get P(y=1|x) = 1). Corrected mean probability 0.210 vs true prevalence 0.204 on the hold-out rows. AUC against s = 0.904 vs 0.991 against true y.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0); n = 10000
y = (rng.random(n) < 0.21).astype(int); X = rng.normal(size=(n, 6)); X[:, :3] += 2.0 * y[:, None]
s = y * (rng.random(n) < 0.3)                                   # only 30% of positives are labelled
a, hold = np.arange(n) < 7000, np.arange(n) >= 7000
Xa, sa, Xhold, shold, Xnew = X[a], s[a], X[hold], s[hold], X[hold]
g = LogisticRegression(max_iter=2000).fit(Xa, sa)               # labelled vs unlabelled
c = g.predict_proba(Xhold[shold == 1])[:, 1].mean()             # label frequency
p_pos = np.clip(g.predict_proba(Xnew)[:, 1] / c, 0, 1)
print(c, p_pos.mean(), y[hold].mean(), roc_auc_score(s[hold], p_pos), roc_auc_score(y[hold], p_pos))   # 0.222 0.210 0.204 0.904 0.991
```

**Follow-ups:**
- *Prevalence from PU?* `mean(s)/c`.
- *Fraud: unlabeled = no chargeback yet?* That is PU plus delayed labels; handle both.

**Common mistakes:** Calling unlabelled "negative" and reporting precision; assuming SCAR without checking; no clean evaluation sample.

### Q47 ⭐ 🔴 At 1:10,000 imbalance, when would you switch from supervised learning to anomaly detection or a hybrid approach?
**Asked at:** Fintech, security, senior roles, Europe
**Say this first (1 line):** I stay with supervised learning while I have enough labelled positives that look alike; I move to anomaly detection when positives are too few or keep changing form (new attack types), and in practice I use a hybrid: unsupervised scores and rules as features or a second-stage filter into a supervised model.

**Then explain:**
- **Supervised works when:** hundreds or thousands of positives, labels trusted, patterns stable. Use class weights, GBMs, top-k evaluation.
- **At 1:10,000 with 100 total positives:** you have too little to learn the positive class, and positives may be heterogeneous. Anomaly detection (Isolation Forest, autoencoder reconstruction error, one-class SVM, density/Mahalanobis) models "normal" and flags deviation.
- **Anomaly caveats:** anomalous is not the same as fraud; it needs good features and gives many false alarms; no direct use of labels; hard to tune and evaluate.
- **Hybrid:** (1) rules + anomaly score as features in a supervised model; (2) anomaly detector as first-stage filter for review, with feedback labels feeding a supervised model; (3) semi-supervised, training normal data plus few labelled anomalies.
- **Evaluate** with the few labelled positives (PR-AUC, recall at fixed alert budget), plus a time-forward split.
- Collect more labels: active learning on the top anomalies.

**Example (illustrative scenario):** New payments product, 3 confirmed frauds in 1M transactions: Isolation Forest on velocity features sends the top 0.1% (1,000/day) to analysts. After 6 months you have 400 labelled frauds, so a GBM with the anomaly score as a feature takes over.

**Code:**
```python
import numpy as np
from sklearn.ensemble import IsolationForest
rng = np.random.default_rng(0)
X_normal = rng.normal(size=(5000, 5)); X_new = np.vstack([rng.normal(size=(5, 5)), rng.normal(5, 1, size=(5, 5))])  # 5 normal, 5 outliers
iso = IsolationForest(n_estimators=300, contamination="auto", random_state=0).fit(X_normal)
score = -iso.score_samples(X_new)      # higher = more anomalous: about 0.40 for the normal rows, 0.74 for the outliers
```

**Follow-ups:**
- *How do you choose a threshold?* Alert budget and analyst capacity.
- *Why not SMOTE?* With 100 heterogeneous positives, synthetic points mostly add noise.

**Common mistakes:** Equating anomaly with fraud; not using labels at all once they exist; evaluating with accuracy; no feedback loop.

### Q48 ⭐ 🔴 Fairness and thresholds: equalized odds vs group calibration; can you satisfy both? How do you handle per-group thresholds?
**Asked at:** Europe (regulated), fintech lending, senior roles
**Say this first (1 line):** Equalized odds asks for equal TPR and FPR across groups, group calibration asks that a score means the same probability in every group; when base rates differ and the model is not perfect, you cannot satisfy both (Kleinberg et al.; Chouldechova), so you choose based on the harm and the law.

**Then explain:**
- **Equalized odds:** `P(ŷ=1 | y, g)` the same for all groups g. Equal opportunity is the TPR-only version.
- **Calibration within groups / predictive parity:** `P(y=1 | score, g)` equal across groups; equal PPV at a threshold.
- **Impossibility:** with different prevalences and an imperfect classifier, equal TPR/FPR forces unequal PPV. If prevalence is equal or the classifier is perfect, both can hold.
- **Per-group thresholds:** can equalise TPR or FPR but may be illegal (disparate treatment) in some jurisdictions and in lending; legal review needed. Alternatives: better features and data, in-processing constraints, post-processing, or one calibrated score with a single threshold plus monitoring.
- Document choices, report per-group metrics with CIs, and handle small groups carefully.

**Example (simulated, run):** Group A prevalence 29%, group B 10%. Same score distribution given class and threshold 0.5. TPR: 0.764 vs 0.792, FPR: 0.225 vs 0.226 (equalized odds holds approximately). PPV: 0.580 vs 0.284. Calibration by group fails, because the same score means different risk in B.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
grp = rng.choice(["A", "B"], 40000); y = (rng.random(40000) < np.where(grp == "A", 0.29, 0.10)).astype(int)
s = np.clip(rng.normal(0.35 + 0.3*y, 0.2), 0, 1); t = 0.5     # same score distribution given class in both groups
groups = ["A", "B"]
for g in groups:
    m = grp == g; pr = s[m] > t
    print(g, y[m].mean(), pr[y[m] == 1].mean(), pr[y[m] == 0].mean(), y[m][pr].mean())  # base, TPR, FPR, PPV
```

**Follow-ups:**
- *Which should a bank choose?* Often calibration (score = true risk) for pricing; for screening harms, equal opportunity. It is a policy decision.
- *Sensitive attribute unavailable?* Proxies; audit using it at evaluation time where permitted.

**Common mistakes:** Claiming a model is "fair" using one metric; per-group thresholds without legal review; ignoring base rate differences; small subgroups with noisy estimates.
