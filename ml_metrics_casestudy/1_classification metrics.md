# Classification Metrics — A Complete Course

*From "what is a confusion matrix" to "why PR-AUC beats ROC-AUC in fraud detection."*

**How to use this document**
- Read Parts 0–2 in order. Everything else depends on them.
- One single numeric example (100 patients) runs through the whole document, so you can compare metrics on identical data.
- Every formula symbol is spelled out.
- Python snippets assume `from sklearn.metrics import *` and `import numpy as np`.

---

## Table of Contents

| Part | Topic |
|---|---|
| 0 | Model evaluation basics |
| 1 | The confusion matrix (read this before any metric) |
| 2 | Basic metrics: Accuracy, Error Rate |
| 3 | Cell-ratio metrics: Precision, Recall, Sensitivity, Specificity, FPR, FNR, PPV, NPV |
| 4 | Combined metrics: F1, F-beta, F0.5, F2, G-Mean, Balanced Accuracy |
| 5 | Probability metrics: Log Loss, Cross Entropy, BCE, CCE, Hinge Loss |
| 6 | Ranking metrics: ROC, ROC-AUC, PR Curve, PR-AUC, Average Precision, Lift, Gain, KS |
| 7 | Calibration: Calibration Curve, Calibration Error, Brier Score |
| 8 | Multi-class: Macro, Micro, Weighted averaging |
| 9 | Multi-label: Hamming Loss, Jaccard, Subset Accuracy |
| 10 | Imbalanced data + advanced metrics: MCC, Cohen's Kappa, Youden, DOR, Dice |
| 11 | Threshold selection |
| 12 | Master comparison tables |
| 13 | "Which metric should I use?" decision tree |
| 14 | Industry case studies (+ IoU and mAP) |
| 15 | 100+ interview questions with answers |
| 16 | Cheat sheet, formula sheet, mnemonics, pitfalls |

---

# PART 0 — The Basics

## 0.1 What is Model Evaluation?

Model evaluation is **measuring how good your model's predictions are, using data the model has never seen before.**

Analogy: you teach a student from a textbook (training data). To find out whether they actually learned, you give them an exam with new questions (test data). Model evaluation is grading that exam.

Two separate questions live inside "how good is my model?":
1. **How often is it right?** → Accuracy-style metrics.
2. **When it is wrong, what kind of wrong?** → Precision / Recall style metrics.

Question 2 is the one beginners skip, and it is the one that matters in business.

## 0.2 Why do we need evaluation metrics?

Five concrete reasons:

| Reason | Explanation |
|---|---|
| **Compare models** | Logistic Regression vs XGBoost — you need one number to rank them. |
| **Tune hyperparameters** | `GridSearchCV(scoring='f1')` needs a metric to optimise. |
| **Communicate with the business** | "We catch 92% of fraud" is a metric. "The model is good" is not. |
| **Detect overfitting** | Train metric high + test metric low = overfitting. |
| **Choose a decision threshold** | A model outputs 0.63; whether that becomes "yes" or "no" is a metric-driven business decision. |

## 0.3 What happens if you use the wrong metric?

You optimise the wrong thing, and the model that looks best on paper is the worst in production. Three real failure modes:

**Failure 1 — Cancer screening optimised for Accuracy.**
Only 1% of screened patients have cancer. A model that predicts "no cancer" for everyone gets **99% accuracy** and detects **zero** cancers. Accuracy said "excellent." Reality: the model is useless and dangerous. The right metric was Recall (with a Precision floor).

**Failure 2 — Spam filter optimised for Recall.**
Recall 100% is trivially achieved by marking every email as spam. Your users lose their job offers and bank alerts. The right metric was Precision.

**Failure 3 — Credit-risk model optimised for ROC-AUC, deployed on Log Loss needs.**
ROC-AUC only measures *ranking*. The bank needed calibrated probabilities to price interest rates. A model with great AUC can have systematically wrong probabilities. The right metric was Log Loss or Brier Score.

**One-line rule:** the metric is a mathematical statement of what your business considers "a good day." Pick it *before* you train.

## 0.4 Regression metrics vs Classification metrics

| | Regression | Classification |
|---|---|---|
| **Target type** | Continuous number (price, temperature, sales) | Discrete category (spam / not spam, class A/B/C) |
| **Question asked** | "How far off am I?" | "Did I pick the right bucket?" |
| **Error meaning** | Distance | Right or wrong (and *which kind* of wrong) |
| **Typical metrics** | MAE, MSE, RMSE, R², MAPE | Accuracy, Precision, Recall, F1, ROC-AUC, Log Loss |
| **Range** | Usually 0 → ∞ (lower better) | Usually 0 → 1 (higher better), except losses |
| **Class imbalance** | Not a concept | Central problem |
| **Threshold** | Not needed | Often needed (0.5 by default) |

Key conceptual difference: in regression, being wrong by 2 is twice as bad as being wrong by 1. In classification, there is no "distance" — but different mistakes have wildly different **costs**. Missing a cancer ≠ falsely flagging a healthy person. Classification metrics exist mainly to let you weigh these two costs differently.

**Overlap warning:** metrics like **Log Loss** and **Brier Score** feel like regression metrics because they measure numeric distance — they do, but the distance is between a *predicted probability* and a 0/1 label. They belong to classification.

---

# PART 1 — The Confusion Matrix

Everything in classification is built from four numbers. Learn these four and 90% of the rest is arithmetic.

## 1.1 The four vocabulary words

Two things exist for every single row of your test data:
- **Actual (ground truth)** — what really happened. Written in the data.
- **Predicted** — what the model said.

Each can be Positive or Negative.

- **Actual Positive (AP)** — the event really happened. Patient really has the disease.
- **Actual Negative (AN)** — the event really did not happen. Patient is really healthy.
- **Predicted Positive (PP)** — the model said "yes, event."
- **Predicted Negative (PN)** — the model said "no event."

> **Crucial beginner note:** "Positive" does NOT mean "good." Positive means **the thing you are trying to detect**. Cancer is the positive class. Fraud is the positive class. Churn is the positive class. Positive is usually the *bad* thing in real life. Whoever labels the data decides which class is positive, and every metric flips if you flip that choice.

## 1.2 The four cells

Read each name as two words: **[True/False] = was the model correct?** and **[Positive/Negative] = what did the model say?**

| Cell | Model said | Reality | Meaning | Nickname |
|---|---|---|---|---|
| **TP** True Positive | Positive | Positive | Correctly caught the event | Hit |
| **TN** True Negative | Negative | Negative | Correctly ignored a non-event | Correct rejection |
| **FP** False Positive | Positive | Negative | False alarm | **Type I error** |
| **FN** False Negative | Negative | Positive | Missed event | **Type II error** |

Memory trick: the **second** word is always what the *model* said. The **first** word tells you if the model was right. `False Positive` = "model said Positive, and that was False."

## 1.3 The ASCII confusion matrix

The scikit-learn layout (rows = actual, columns = predicted):

```
                      P R E D I C T E D
                   +-----------+-----------+
                   | Negative  | Positive  |
        +----------+-----------+-----------+
        | Negative |    TN     |    FP     |   <- all Actual Negatives
 ACTUAL |          |           |(Type I)   |
        +----------+-----------+-----------+
        | Positive |    FN     |    TP     |   <- all Actual Positives
        |          |(Type II)  |           |
        +----------+-----------+-----------+
                     ^           ^
                     |           +-- all Predicted Positives
                     +-------------- all Predicted Negatives
```

Textbooks and papers often flip this so Positive is the top-left. **Always check the axis labels before reading someone else's confusion matrix.** This is the single most common source of confusion in reading papers.

Useful totals:

```
Actual Positives    = TP + FN          (also called "support" of the positive class)
Actual Negatives    = TN + FP
Predicted Positives = TP + FP
Predicted Negatives = TN + FN
Total N             = TP + TN + FP + FN
Prevalence          = (TP + FN) / N    (how common the positive class is)
```

## 1.4 The same four cells across seven real domains

This table is the most useful thing in Part 1. Notice how the *expensive* error changes column to column.

| Domain | Positive class | TP means | TN means | **FP means (false alarm)** | **FN means (miss)** | Costlier error |
|---|---|---|---|---|---|---|
| **Disease detection** | Has disease | Sick person correctly flagged → treated | Healthy person correctly cleared | Healthy person told they may be ill → anxiety, extra tests, cost | Sick person told they are fine → disease progresses, possible death | **FN** |
| **Email spam** | Is spam | Spam goes to spam folder | Real email reaches inbox | Job offer / bank OTP lands in spam → user misses it | A spam email reaches inbox → user deletes it, mild annoyance | **FP** |
| **Loan approval** (positive = will default) | Will default | Risky applicant correctly rejected | Good applicant correctly approved | Good applicant wrongly rejected → lost revenue, unfair to customer | Bad applicant wrongly approved → loan written off | Usually **FN**, but FP hurts growth |
| **Credit card fraud** | Transaction is fraud | Fraud blocked → money saved | Genuine purchase goes through | Genuine purchase blocked → angry customer, support call, possible churn | Fraud goes through → chargeback loss + reputational damage | **FN** usually, but FP volume is huge |
| **Student admission** | Will succeed / will be admitted | Strong applicant admitted | Weak applicant rejected | Weak applicant admitted → dropout, wasted seat | Strong applicant rejected → talent lost, fairness complaint | Context-dependent, often **FN** (fairness) |
| **Customer churn** | Will churn | Churner identified → retention offer sent | Loyal customer left alone | Loyal customer gets a discount they didn't need → wasted margin | Churner not identified → customer leaves silently | **FN** if CLV > discount cost |
| **Cancer detection** (histopathology) | Malignant | Tumour caught early | Benign correctly identified | Benign called malignant → possible unnecessary biopsy/surgery | Malignant called benign → treatment delayed, mortality risk | **FN**, overwhelmingly |

**The lesson to internalise:** there is no universally best metric because there is no universal answer to "is FP or FN worse?" You must answer that business question first; the metric follows.

## 1.5 THE RUNNING EXAMPLE — 100 patients, calculated by hand

We will use this exact example for every threshold-based metric in this course, so you can compare metrics apples-to-apples.

**Setup.** A hospital screens **100 people** for a disease.
- **20 people truly have the disease** (Actual Positive) → prevalence = 20%.
- **80 people are truly healthy** (Actual Negative).

The model's predictions:
- Of the 20 sick people, the model correctly flagged **15** → **TP = 15**
- The other 5 sick people were told they are healthy → **FN = 5**
- Of the 80 healthy people, the model correctly cleared **70** → **TN = 70**
- The other 10 healthy people were wrongly flagged as sick → **FP = 10**

Sanity check: 15 + 5 = 20 sick ✓ 70 + 10 = 80 healthy ✓ Total = 15+5+70+10 = 100 ✓

**Confusion matrix:**

```
                        P R E D I C T E D
                    +------------+------------+  Row
                    |  Healthy   |  Diseased  |  total
        +-----------+------------+------------+-------
        |  Healthy  |  TN = 70   |  FP = 10   |   80
 ACTUAL +-----------+------------+------------+-------
        | Diseased  |  FN =  5   |  TP = 15   |   20
        +-----------+------------+------------+-------
          Col total |     75     |     25     |  100
```

**Derived totals we will reuse constantly:**

```
Actual Positives     = TP + FN = 15 +  5 = 20
Actual Negatives     = TN + FP = 70 + 10 = 80
Predicted Positives  = TP + FP = 15 + 10 = 25
Predicted Negatives  = TN + FN = 70 +  5 = 75
Total N              = 100
Prevalence           = 20 / 100 = 0.20
```

**Reading it in plain English:** The model raised 25 alarms. Only 15 of those alarms were real, so 10 healthy people were scared for nothing. There were 20 real cases and the model found 15 of them, so 5 sick people went home undiagnosed. Hold that sentence in your head — every metric below is just one number summarising part of that sentence.

**Python — building this in code:**

```python
import numpy as np
from sklearn.metrics import confusion_matrix

# 20 diseased (label 1) then 80 healthy (label 0)
y_true = np.array([1]*20 + [0]*80)

# Of the 20 diseased: 15 predicted 1 (TP), 5 predicted 0 (FN)
# Of the 80 healthy : 10 predicted 1 (FP), 70 predicted 0 (TN)
y_pred = np.array([1]*15 + [0]*5 + [1]*10 + [0]*70)

cm = confusion_matrix(y_true, y_pred)   # rows=actual, cols=predicted, labels sorted 0,1
print(cm)
# [[70 10]
#  [ 5 15]]

tn, fp, fn, tp = cm.ravel()   # <-- memorise this order: TN, FP, FN, TP
print(tn, fp, fn, tp)          # 70 10 5 15
```

Line-by-line:
- `y_true` — the ground-truth labels. Order does not matter for metrics, only the pairing with `y_pred`.
- `y_pred` — hard 0/1 predictions, aligned index-by-index with `y_true`.
- `confusion_matrix` — returns a 2×2 array. Rows are actual classes **sorted ascending** (0 then 1), columns are predicted classes sorted ascending.
- `cm.ravel()` — flattens row-wise to `[TN, FP, FN, TP]`. This exact order is a very common interview question.

## 1.6 The three "views" of the confusion matrix

Almost every metric is a ratio taken along one of three directions. If you understand this, you never have to memorise formulas again.

```
                     PREDICTED
                  Neg        Pos
             +----------+----------+
  ACTUAL Neg |    TN    |    FP    |  --> divide by row: Specificity, FPR
             +----------+----------+
  ACTUAL Pos |    FN    |    TP    |  --> divide by row: Recall, FNR
             +----------+----------+
                  |          |
                  v          v
                 NPV      Precision      <-- divide by column
```

- **Divide along ACTUAL rows** → "of the real cases, how many did I catch?" → **Recall, Specificity, FPR, FNR**. These do **not** depend on prevalence. Good for comparing a test across populations.
- **Divide along PREDICTED columns** → "when I raise an alarm, how often am I right?" → **Precision (PPV), NPV**. These **do** depend on prevalence. Good for what the end user actually experiences.
- **Divide the diagonal by everything** → **Accuracy**.

---

# PART 2 — Basic Metrics

## 2.1 ACCURACY

### 1. Definition
The fraction of all predictions that were correct.

### 2. Intuition
It is the most natural question a human asks: *"out of everything, how often was the model right?"* It exists because it is the simplest possible summary — one number, no ambiguity, understood by any stakeholder. It solves the problem of "give me a single headline number."

Its weakness is baked into its strength: by treating every mistake as equal, it hides *which* mistakes happened.

### 3. Formula

```
              TP + TN            correct predictions
Accuracy = ----------------- = ----------------------
           TP + TN + FP + FN     total predictions
```

- **TP** = True Positives — real events correctly flagged
- **TN** = True Negatives — non-events correctly ignored
- **FP** = False Positives — false alarms
- **FN** = False Negatives — missed events
- Numerator = the diagonal of the confusion matrix = everything the model got right
- Denominator = N = every row in the test set

### 4. Manual example (running example)

```
TP = 15, TN = 70, FP = 10, FN = 5
Numerator   = TP + TN = 15 + 70 = 85
Denominator = 100
Accuracy    = 85 / 100 = 0.85  =  85%
```

### 5. Python

```python
from sklearn.metrics import accuracy_score
accuracy_score(y_true, y_pred)      # 0.85
accuracy_score(y_true, y_pred, normalize=False)   # 85  (raw count instead of fraction)
```
- `accuracy_score(a, b)` — argument order is `(y_true, y_pred)`. It is symmetric for accuracy, but **not** for precision/recall, so always keep truth first as a habit.
- `normalize=False` returns the count of correct predictions rather than the proportion.

### 6. Interpretation

| Value | Meaning |
|---|---|
| 0.40 | Worse than a coin flip on balanced data — the model may have inverted logic. Check label encoding. |
| 0.60 | Weak; barely better than guessing on balanced data. |
| 0.80 | Decent on balanced data. Meaningless on data with 80% negatives. |
| 0.95 | Looks great — **immediately ask what the class balance is.** |
| 1.00 | Almost always a bug: data leakage, target column left in features, or you evaluated on training data. |

**The most important interpretation rule:** always compare accuracy to the **majority-class baseline** (the accuracy you get by always predicting the most common class). Accuracy of 0.95 when the baseline is 0.99 means your model is *worse than doing nothing*.

### 7. Good vs bad values

| Band | Balanced data (50/50) | Imbalanced data (95/5) |
|---|---|---|
| Poor | < 0.60 | < 0.95 (below baseline) |
| Average | 0.60 – 0.75 | ≈ baseline |
| Good | 0.75 – 0.90 | Meaningfully above baseline **and** good recall |
| Excellent | > 0.90 | Do not judge on accuracy at all |

These bands are indicative only. A 0.55 accuracy stock-direction model can make millions; a 0.99 accuracy medical model can be malpractice.

### 8. Business use cases
Genuinely appropriate when classes are roughly balanced and errors cost about the same:
- **Manufacturing:** binary pass/fail on a line where defects are ~40–50% during process tuning.
- **Retail:** A/B classification of which of two equally-stocked products a customer will buy.
- **Image classification:** balanced benchmark datasets (MNIST, CIFAR-10) — this is why accuracy dominates academic vision papers.
- **Telecom:** predicting which of two equally-likely plans a customer picks.
- **Reporting layer:** almost every executive dashboard shows accuracy even when it shouldn't, because it is the only metric non-technical stakeholders intuit. Show it *alongside* the real metric.

### 9. Advantages
- Trivially easy to explain to anyone.
- Single number → easy model ranking.
- Symmetric — no need to decide which class is "positive."
- Extends to multi-class unchanged.
- Cheap to compute; no probabilities needed.

### 10. Limitations
- **Fails completely on imbalanced data** (the accuracy paradox).
- Treats FP and FN as equally costly — almost never true.
- Threshold-dependent (assumes 0.5 by default).
- Ignores prediction confidence: a 0.51 prediction and a 0.99 prediction score identically.
- Cannot distinguish two models with the same accuracy but very different error profiles.
- Not comparable across datasets with different prevalence.

### 11. Common mistakes
1. Reporting accuracy alone on a 1%-positive dataset. **The #1 beginner error in all of ML.**
2. Not comparing to the majority-class baseline.
3. Measuring on the training set and celebrating.
4. Using accuracy as the `scoring` parameter in `GridSearchCV` on imbalanced data — the search will converge to a model that predicts the majority class.
5. Confusing accuracy with precision. They are different metrics; the word "accurate" in English maps closer to precision.
6. Assuming 99% accuracy means the model is 99% reliable on the positive class.

### 12. Interview questions

**Easy — What is accuracy?**
The proportion of correct predictions out of all predictions: (TP+TN)/(TP+TN+FP+FN).

**Easy — Can accuracy be 1.0 on a real project?**
Rarely and suspiciously. It usually indicates leakage or evaluating on training data.

**Medium — Explain the accuracy paradox with numbers.**
In a dataset of 10,000 credit-card transactions with 100 frauds, a model that predicts "not fraud" always achieves 9,900/10,000 = 99% accuracy while catching 0 frauds. Recall = 0, Precision undefined, MCC = 0, Balanced Accuracy = 0.5. Accuracy is high because it is dominated by the 99% majority class.

**Medium — Two models both have 85% accuracy. How do you pick one?**
Look at their confusion matrices. If Model A has FN=1, FP=14 and Model B has FN=14, FP=1, they are radically different. Pick based on which error is costlier: A for cancer screening (few misses), B for spam filtering (few false alarms). Then compare on Recall/Precision/F-beta, and on ROC-AUC or PR-AUC for threshold-independent quality.

**Hard — Is accuracy ever the *right* metric on imbalanced data?**
Yes, in a narrow case: when the deployment decision genuinely has symmetric costs and the operational population has the same imbalance, accuracy correctly reflects expected total errors. But then you should really use expected *cost*, not accuracy. In practice, if you find yourself defending accuracy on imbalanced data, use Balanced Accuracy or MCC instead.

**Hard — Relationship between accuracy and Cohen's Kappa?**
Accuracy is observed agreement `p_o`. Kappa rescales it against the agreement expected by chance `p_e`: `κ = (p_o − p_e)/(1 − p_e)`. Kappa therefore penalises the "free" accuracy that comes from class imbalance, which is exactly accuracy's blind spot.

---

## 2.2 ERROR RATE (Misclassification Rate, 0-1 Loss)

### 1. Definition
The fraction of predictions that were wrong. The exact complement of accuracy.

### 2. Intuition
Sometimes you want to talk about failure, not success — "our error rate dropped from 8% to 5%" is a 37.5% relative improvement and sounds far more meaningful than "accuracy rose from 92% to 95%." Error rate exists mainly for that framing, and because optimisation theory prefers to *minimise* a loss.

### 3. Formula

```
              FP + FN
Error Rate = --------------------- = 1 − Accuracy
             TP + TN + FP + FN
```
- **FP + FN** = all wrong predictions of both kinds
- Denominator = N, total samples

Also called **0-1 loss**: each sample contributes loss 0 if correct and 1 if wrong; the error rate is the mean 0-1 loss.

### 4. Manual example

```
FP + FN = 10 + 5 = 15
Error Rate = 15 / 100 = 0.15 = 15%
Check: 1 − 0.85 = 0.15 ✓
```

### 5. Python

```python
from sklearn.metrics import zero_one_loss
zero_one_loss(y_true, y_pred)                    # 0.15
zero_one_loss(y_true, y_pred, normalize=False)   # 15  (count of errors)
1 - accuracy_score(y_true, y_pred)               # 0.15
```
- `zero_one_loss` is the canonical sklearn function; `normalize=False` gives the raw number of mistakes, which is what you report to operations teams ("15 files need manual review").

### 6. Interpretation
Lower is better. 0.0 = perfect, 0.5 = coin flip on balanced data, 1.0 = perfectly inverted predictions (flip your labels and you have a perfect model — a genuinely useful debugging insight).

| Value | Meaning |
|---|---|
| 0.60 | Worse than chance on balanced data → check for inverted labels |
| 0.40 | Weak |
| 0.20 | Average |
| 0.05 | Good on balanced data |
| 0.00 | Suspect leakage |

### 7. Good vs bad values
Same bands as accuracy, mirrored: Poor > 0.40, Average 0.25–0.40, Good 0.10–0.25, Excellent < 0.10 — on balanced data only.

### 8. Business use cases
- **Manufacturing / QA:** "defect escape rate," reported as a percentage of units.
- **OCR and document processing:** character error rate, word error rate — direct analogues.
- **Speech recognition:** WER (Word Error Rate) is the industry-standard metric and is exactly this idea at token level.
- **SLA contracts:** vendors are contractually bound to error rates, not accuracies.
- **Cost modelling:** number of errors × cost per error = the number the CFO cares about.

### 9. Advantages
- Intuitive for reporting improvements (relative error reduction is a meaningful number).
- Directly maps to a loss function for optimisation.
- Raw count version translates straight into headcount / cost estimates.

### 10. Limitations
Identical to accuracy's — it is the same metric. It is imbalance-blind, cost-blind, threshold-dependent, and confidence-blind.

### 11. Common mistakes
- Treating error rate as if it were a *different, better* metric than accuracy. It is not; it carries exactly the same information and the same flaws.
- Comparing error rates across datasets with different prevalence.
- Confusing error rate with **Type I error rate** (that is FPR, a different metric — see 3.5).

### 12. Interview questions

**Easy — Error rate vs accuracy?** `Error = 1 − Accuracy`. Same information.

**Medium — What is 0-1 loss and why is it not used to train models directly?**
0-1 loss assigns 1 to each wrong prediction. It is non-convex and its gradient is zero almost everywhere, so gradient descent cannot optimise it. That is precisely why we train on differentiable surrogates like Log Loss (logistic regression, neural nets) or Hinge Loss (SVMs), then *evaluate* with 0-1 loss / accuracy.

**Hard — Bayes error rate?**
The irreducible minimum error rate achievable by any classifier on a given problem, caused by genuine overlap in the class-conditional distributions (two patients with identical measurements, different outcomes). If your error rate is near the Bayes rate, more data and bigger models will not help; you need better features.

---

# PART 3 — Cell-Ratio Metrics

These eight metrics are all just "one cell divided by a row or a column." All values below come from the same running example (TP=15, FN=5, FP=10, TN=70).

## 3.1 PRECISION (= Positive Predictive Value, PPV)

### 1. Definition
Of all the samples the model **flagged as positive**, what fraction really were positive?

### 2. Intuition
Precision answers the question your *end user* asks: **"when this thing alarms, should I believe it?"**

It exists because the cost of a false alarm is often the dominant cost. Every false positive consumes a real resource: an analyst's hour, a customer's trust, a surgical biopsy, a discount voucher. Precision is the metric of **trustworthiness of alerts** and it directly controls **wasted work**.

Real-world phrasing: "Our fraud team investigates 100 flagged transactions a day. Precision 0.30 means 70 of those investigations are wild goose chases."

### 3. Formula

```
                TP                 TP
Precision = ---------- = -------------------------
             TP + FP      all Predicted Positives
```
- **TP** = correctly flagged positives
- **FP** = wrongly flagged negatives (false alarms)
- Denominator = the entire **predicted-positive column** — i.e. the model's alarm list
- Note that **TN does not appear**. Precision completely ignores the negatives you correctly left alone. This is why precision is meaningful on hugely imbalanced data where accuracy is not.

If the model predicts positive for nothing at all, the denominator is 0 and precision is undefined. sklearn returns 0.0 and issues a warning; control this with `zero_division=0` or `zero_division=1`.

### 4. Manual example

```
TP = 15, FP = 10
Predicted Positives = 15 + 10 = 25
Precision = 15 / 25 = 0.60 = 60%
```
Plain English: the model raised 25 alarms; 15 were genuine; **6 out of every 10 alarms are real, 4 are false.**

### 5. Python

```python
from sklearn.metrics import precision_score
precision_score(y_true, y_pred)                    # 0.6
precision_score(y_true, y_pred, pos_label=1)       # explicit: which class is "positive"
precision_score(y_true, y_pred, zero_division=0)   # return 0 instead of warning if no positives predicted
```
- `pos_label` — for binary problems sklearn defaults to `1`. If your labels are strings like `'fraud'/'legit'`, you **must** set `pos_label='fraud'` or you will silently measure the wrong class.
- `zero_division` — controls behaviour when the model predicts zero positives.

### 6. Interpretation

| Value | Meaning in operational terms |
|---|---|
| 0.40 | 4 of 10 alerts are real → 60% of your team's time is wasted. Rarely acceptable unless recall is critical. |
| 0.60 | 6 of 10 alerts real. Tolerable for a cheap follow-up action (send an email). |
| 0.80 | 8 of 10 real. Good for costly actions (dispatch a technician). |
| 0.95 | Almost every alert is real. Required for automated irreversible actions (auto-block a card, auto-reject a loan). |
| 1.00 | Zero false alarms — usually means the model is extremely conservative and recall is terrible. Always check recall next. |

### 7. Good vs bad values
Entirely driven by the cost of a false positive and by **prevalence**. On a 1%-positive dataset, precision of 0.30 means the model is 30× better than random guessing, which can be excellent. On a 50%-positive dataset, precision 0.30 is worse than a coin flip.

**Rule of thumb:** compare precision to prevalence. `Precision / Prevalence` is the **lift** of your model.

| Band | High-prevalence (~50%) | Low-prevalence (~1%) |
|---|---|---|
| Poor | < 0.60 | < 0.05 |
| Average | 0.60 – 0.75 | 0.05 – 0.20 |
| Good | 0.75 – 0.90 | 0.20 – 0.50 |
| Excellent | > 0.90 | > 0.50 |

### 8. Business use cases
Precision is king whenever a false positive is expensive or annoying:
- **Email spam filtering:** a legitimate email in the spam folder is far worse than a spam email in the inbox. Gmail targets very high precision.
- **Content moderation / account bans:** wrongly banning a paying user causes churn and press coverage.
- **Marketing (paid campaigns):** each contacted lead costs money; low precision burns budget.
- **Recommendation systems:** precision@k — the top 5 recommendations must be relevant or the user disengages.
- **Search ranking:** precision@10 is essentially "is page 1 useful?"
- **Insurance claim auto-approval:** falsely approving a fraudulent claim pays out real money.
- **Legal / e-discovery:** false positives mean expensive lawyer review hours.
- **Cyber security alert triage:** SOC teams drown in false positives; alert fatigue causes real attacks to be ignored.
- **Manufacturing (rejecting good units):** each false reject scraps a saleable product.

### 9. Advantages
- Directly interpretable as "trust in an alarm."
- Ignores TN, so it does not get inflated by a huge negative class → **robust to class imbalance** in the way accuracy is not.
- Maps directly to operational cost (# investigations × cost per investigation).
- Combined with recall, fully characterises performance on the positive class.

### 10. Limitations
- **Says nothing about missed cases.** A model that flags one obvious fraud and ignores 999 others has precision 1.0.
- **Depends on prevalence** — the same model has lower precision in a healthier population. So precision is not portable across populations, unlike recall/specificity.
- Undefined when nothing is predicted positive.
- Threshold-dependent: raising the threshold almost always raises precision.
- Easily gamed by being conservative.

### 11. Common mistakes
1. **Reporting precision without recall.** They are meaningless alone; always report the pair.
2. Forgetting `pos_label` with string labels → measuring precision of the wrong class.
3. Comparing precision across datasets with different prevalence and concluding one model is better.
4. Confusing precision with accuracy in conversation.
5. Confusing precision (statistics/ML) with *precision* in measurement science (= repeatability/low variance). Different concepts, same word.
6. Using `average='micro'` in multi-class and being surprised that precision = recall = accuracy.

### 12. Interview questions

**Easy — Define precision.** TP/(TP+FP): of everything predicted positive, the fraction actually positive.

**Easy — Why doesn't precision use TN?** Because it only asks about the quality of the alarms raised, not about correctly-ignored negatives.

**Medium — How do you increase precision?** Raise the decision threshold; add features that separate hard negatives; use cost-sensitive training that penalises FP more; post-filter alerts with business rules; use an ensemble/second-stage model on flagged cases. Note the cost: recall almost always drops.

**Medium — Can precision be high while the model is useless?** Yes. Predict positive for only the single most confident sample. If correct, precision = 1.0 and recall ≈ 0.

**Hard — Why does precision change when the same model is deployed in a different hospital?**
Precision depends on prevalence via Bayes' rule: `PPV = (Sens × Prev) / (Sens × Prev + (1−Spec) × (1−Prev))`. Sensitivity and specificity are intrinsic to the test; prevalence is a property of the population. Screening a low-prevalence general population instead of a high-risk referral population sharply lowers PPV even though the model is unchanged. This is the classic base-rate fallacy and a top-tier interview question.

**Hard — Precision@k vs precision?**
Precision@k restricts the calculation to the top k ranked items rather than all items above a probability threshold. It is threshold-free and matches how ranking systems are actually consumed (page 1 of search results, top 5 recommendations).

---

## 3.2 RECALL (= Sensitivity = True Positive Rate = Hit Rate = Detection Rate)

### 1. Definition
Of all the samples that **really are positive**, what fraction did the model find?

### 2. Intuition
Recall answers the question the *victim* asks: **"if I have the disease, will this test find me?"**

It exists because missing an event is often catastrophic and irreversible. A missed cancer, an undetected intrusion, an unflagged fraudulent wire transfer — these are the errors that end careers and lives. Recall is the metric of **safety and coverage**.

Note the four names. **Recall = Sensitivity = TPR = Hit Rate** are literally the same formula. ML papers say "recall," medical papers say "sensitivity," ROC-curve discussions say "TPR." Knowing this equivalence is essential for reading across fields.

### 3. Formula

```
              TP               TP
Recall = ---------- = -----------------------
          TP + FN      all Actual Positives
```
- **TP** = positives found
- **FN** = positives missed
- Denominator = the entire **actual-positive row** = the total number of real cases (the "support")
- **TN and FP do not appear.** Recall is completely independent of how many negatives exist → **recall does not change with prevalence.** This is why it is the preferred metric for characterising a diagnostic test.

### 4. Manual example

```
TP = 15, FN = 5
Actual Positives = 15 + 5 = 20
Recall = 15 / 20 = 0.75 = 75%
```
Plain English: there were 20 real cases; the model caught 15 and **missed 5**. Three out of four sick people are correctly identified; one in four is sent home undiagnosed.

### 5. Python

```python
from sklearn.metrics import recall_score
recall_score(y_true, y_pred)     # 0.75
```
- Same `pos_label` and `zero_division` arguments as precision. Recall's denominator is zero only if there are no positive samples in the test set at all — a sign of a broken split, usually fixed with `StratifiedKFold`.

### 6. Interpretation

| Value | Meaning |
|---|---|
| 0.40 | Missing 60% of real cases. Unacceptable for anything safety-critical. |
| 0.60 | Missing 40%. Might be fine for a marketing campaign, never for cancer. |
| 0.80 | Missing 1 in 5. Common real-world level for fraud models. |
| 0.95 | Missing 1 in 20. Typical target for medical screening. |
| 1.00 | Catches everything — check precision; you may simply be flagging everyone. |

### 7. Good vs bad values

| Band | General | Safety-critical (medical, aviation, fraud) |
|---|---|---|
| Poor | < 0.50 | < 0.85 |
| Average | 0.50 – 0.70 | 0.85 – 0.92 |
| Good | 0.70 – 0.85 | 0.92 – 0.98 |
| Excellent | > 0.85 | > 0.98 |

Regulators sometimes mandate minimum sensitivity for screening devices, which makes this a hard constraint rather than a target.

### 8. Business use cases
Recall is king whenever a miss is expensive or irreversible:
- **Cancer / disease screening:** missing a malignancy can be fatal. Screening tests are deliberately tuned to sensitivity > 0.95, accepting many false positives which are then resolved by a second, high-precision confirmatory test.
- **Credit card fraud detection:** an unblocked fraudulent transaction is a direct loss plus a chargeback fee.
- **Anti-money-laundering:** regulators fine banks for missed suspicious activity, not for over-reporting.
- **Predictive maintenance:** a missed impending failure destroys a turbine; a false alarm costs one inspection.
- **Cyber security intrusion detection:** one missed breach can be existential.
- **Customer churn:** a missed churner is lost lifetime value; a false positive costs one discount.
- **Recall in safety recalls (manufacturing):** missing a defective batch causes injury and litigation.
- **Loan default prediction:** a missed default is a written-off loan.
- **Resume screening for rare skills:** missing a great candidate is a real cost in a talent war.

### 9. Advantages
- Directly measures coverage of the thing you care about.
- **Independent of class balance and prevalence** → portable across populations and comparable across studies.
- Trivially interpretable to non-technical stakeholders ("we catch 3 of every 4 cases").
- Ignores TN, so imbalance does not inflate it.

### 10. Limitations
- **Trivially gamed:** predict positive for everything → recall = 1.0.
- Says nothing about false-alarm volume, i.e. nothing about cost.
- Threshold-dependent.
- Meaningless without precision alongside it.
- With very few positives in the test set, recall has enormous variance (with 10 positives, one flipped sample moves recall by 0.10). Always report the support and preferably a confidence interval.

### 11. Common mistakes
1. Maximising recall without a precision floor → an alert system nobody uses.
2. Reporting recall on a test set with 8 positive samples and treating 0.875 as precise.
3. Not realising Sensitivity, TPR, Hit Rate and Recall are the same thing, then double-counting them as separate evidence.
4. Confusing recall with specificity (recall is about positives; specificity is about negatives).
5. Assuming high recall implies high accuracy.

### 12. Interview questions

**Easy — Define recall.** TP/(TP+FN): of all real positives, the fraction detected.

**Easy — Recall vs sensitivity?** Identical. Different vocabulary from different fields.

**Medium — Precision vs recall, one sentence each.** Precision = "of my alarms, how many were real?" Recall = "of the real cases, how many did I alarm on?"

**Medium — Why is there a precision-recall trade-off?**
Both are driven by the decision threshold. Lowering the threshold flags more samples, which can only add TPs (recall up, never down) but also adds FPs (precision typically down). Raising it does the reverse. The trade-off is not a law of nature but a consequence of using one threshold on an imperfect score; a genuinely better model improves both at once, which is what PR-AUC measures.

**Hard — Your fraud model has recall 0.99 and precision 0.02. Is it useful?**
Possibly, as a *first-stage filter*. It reduces the review population enormously while retaining almost all fraud, and a second high-precision stage (rules, another model, or human review) resolves the rest. Evaluate it as part of a cascade, using the workload it creates: at 0.02 precision, catching 100 frauds means reviewing 5,000 transactions. Whether that is viable depends on review cost vs fraud loss.

**Hard — How do you improve recall without destroying precision?**
Better features (especially ones capturing the hard positives), more positive-class data or targeted augmentation, class weighting / focal loss, ensembling diverse models, and threshold tuning guided by an expected-cost curve rather than by F1. Structural fixes (better features/data) shift the whole PR curve outward; threshold tuning only slides along it.

---

## 3.3 SENSITIVITY

**Sensitivity is exactly Recall.** `Sensitivity = TP / (TP + FN) = 0.75` in our example.

It is listed separately here because you will meet it as a separate word, and because it always travels as a pair with Specificity in medicine and diagnostics.

- **Field:** medicine, epidemiology, diagnostics, psychometrics.
- **Question it answers:** "How good is this test at *detecting* the condition when it is present?"
- **Memory trick:** a **sen**sitive smoke alarm goes off at the slightest smoke → it catches everything → high sensitivity = few misses.
- **Why medicine uses the Sensitivity/Specificity pair instead of the Precision/Recall pair:** both sensitivity and specificity are **prevalence-independent**, so a test's characteristics can be published once and applied to any population. Precision (PPV) changes with prevalence, so it must be recomputed per population using Bayes' rule.

**SnNout / SpPin — the classic clinical mnemonic:**
- **SnNout:** a highly **Sn** (sensitive) test that is **N**egative rules the disease **out**. (High sensitivity → few FN → a negative result is trustworthy.)
- **SpPin:** a highly **Sp** (specific) test that is **P**ositive rules the disease **in**. (High specificity → few FP → a positive result is trustworthy.)

**Interview question (Hard) — Why not just report accuracy for a medical test?**
Because a test's accuracy depends on the prevalence in the tested population, so the same test would have different "accuracy" in every clinic. Sensitivity and specificity are intrinsic properties of the test and are therefore what regulatory submissions require.

---

## 3.4 SPECIFICITY (= True Negative Rate, TNR = Selectivity)

### 1. Definition
Of all the samples that **really are negative**, what fraction did the model correctly identify as negative?

### 2. Intuition
Specificity is recall's mirror image, applied to the negative class: **"if I am healthy, will this test correctly leave me alone?"**

It exists because harming the healthy majority has a real aggregate cost. In a screening programme of a million people with 1% prevalence, dropping specificity from 0.99 to 0.95 adds 39,600 unnecessary follow-up procedures. Specificity is the metric of **not disturbing the innocent**.

### 3. Formula

```
                    TN                TN
Specificity = ------------ = ----------------------- = 1 − FPR
                TN + FP       all Actual Negatives
```
- **TN** = negatives correctly cleared
- **FP** = negatives wrongly flagged
- Denominator = the entire **actual-negative row**
- **TP and FN do not appear** → specificity is independent of prevalence, exactly like recall.

### 4. Manual example

```
TN = 70, FP = 10
Actual Negatives = 70 + 10 = 80
Specificity = 70 / 80 = 0.875 = 87.5%
```
Plain English: of 80 healthy people, 70 were correctly told they are fine; **10 were wrongly alarmed.**

### 5. Python
There is no `specificity_score` in scikit-learn. Three ways to get it:

```python
from sklearn.metrics import confusion_matrix, recall_score
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
specificity = tn / (tn + fp)                       # 0.875

# Trick: specificity is the recall of the negative class
recall_score(y_true, y_pred, pos_label=0)          # 0.875

# Or from imbalanced-learn
# from imblearn.metrics import specificity_score
# specificity_score(y_true, y_pred)                # 0.875
```
- The `pos_label=0` trick is worth memorising: **specificity = recall with the labels flipped.** It also means anything you know about recall transfers directly.

### 6. Interpretation

| Value | Meaning |
|---|---|
| 0.40 | 60% of healthy people get false alarms — the model is essentially flagging everyone. |
| 0.60 | 40% false-alarm rate on negatives. |
| 0.80 | 1 in 5 negatives wrongly flagged. On 1M people, that is 200k false alarms. |
| 0.95 | 1 in 20 wrongly flagged. |
| 0.999 | Required for mass screening of very rare conditions. |

**Scale intuition:** with 1% prevalence and 1,000,000 people screened, specificity 0.99 still produces **9,900 false positives** versus at most 10,000 true cases — precision ≈ 0.50 at best. This is why rare-disease screening demands extreme specificity.

### 7. Good vs bad values
Poor < 0.70, Average 0.70–0.85, Good 0.85–0.95, Excellent > 0.95 — but for mass screening of rare events, anything below 0.99 may be operationally impossible.

### 8. Business use cases
- **Medical screening programmes:** paired with sensitivity in every diagnostic study and regulatory filing.
- **COVID / infectious disease testing:** a low-specificity test in a low-prevalence population produces mostly false positives, wasting quarantine capacity.
- **Drug testing / doping control:** falsely accusing a clean athlete is unacceptable → specificity is prioritised, often with confirmatory second tests.
- **Airport security secondary screening:** false positives create queues and passenger anger.
- **Banking KYC / sanctions screening:** low specificity means thousands of manual reviews of legitimate customers.
- **Manufacturing:** correctly passing good units keeps yield high.
- **Marketing suppression lists:** correctly identifying who *not* to contact.

### 9. Advantages
- Prevalence-independent → portable and publishable.
- Directly quantifies the burden imposed on the innocent majority.
- Together with sensitivity, fully describes an ROC point.
- Robust to imbalance in the sense that it does not change as prevalence shifts.

### 10. Limitations
- On heavily imbalanced data with a huge negative class, specificity is **misleadingly reassuring**: TN is enormous, so specificity stays near 1.0 even when FP vastly exceeds TP. This is exactly why ROC curves (which use specificity via FPR) mislead on imbalanced data, and PR curves (which use precision) do not.
- Ignores the positive class entirely.
- Threshold-dependent.
- Not directly available in sklearn, so people forget to report it.

### 11. Common mistakes
1. **Confusing specificity with precision.** Specificity divides by actual negatives (a row); precision divides by predicted positives (a column). On imbalanced data they diverge dramatically: our example has specificity 0.875 but precision only 0.60.
2. Reporting a specificity of 0.99 on a 1%-positive dataset as proof of a great model, without showing that FP still swamps TP.
3. Forgetting it must be computed manually in sklearn, then quietly dropping it from the report.
4. Mixing up specificity and sensitivity under time pressure in interviews.

### 12. Interview questions

**Easy — Define specificity.** TN/(TN+FP): of all real negatives, the fraction correctly identified.

**Easy — Specificity + FPR = ?** 1.

**Medium — Specificity vs precision on imbalanced data.**
With 10,000 negatives and 100 positives, suppose FP = 100, TP = 90, TN = 9,900, FN = 10. Specificity = 9,900/10,000 = 0.99 (looks excellent). Precision = 90/190 = 0.474 (mediocre). Specificity is diluted by the huge TN count; precision is not. Precision is the operationally honest number here.

**Medium — Why do screening programmes use a high-sensitivity test followed by a high-specificity test?**
Stage 1 must not miss cases (high sensitivity, accepting many FPs). Stage 2 operates on a much higher-prevalence, much smaller population, where a high-specificity confirmatory test can eliminate the false positives economically. The cascade achieves both goals at acceptable cost — neither single test could.

**Hard — Derive PPV from sensitivity, specificity and prevalence.**
```
              Sens × Prev
PPV = ---------------------------------------
      Sens × Prev + (1 − Spec) × (1 − Prev)
```
Check with our numbers: Sens=0.75, Spec=0.875, Prev=0.20 → numerator = 0.15; denominator = 0.15 + 0.125×0.80 = 0.15 + 0.10 = 0.25 → PPV = 0.60 ✓ matches the precision we computed directly.

---

## 3.5 FALSE POSITIVE RATE (FPR = Type I Error Rate = Fall-out = False Alarm Rate)

### 1. Definition
Of all the real negatives, what fraction did the model wrongly flag as positive?

### 2. Intuition
The complement of specificity, stated as a failure rather than a success. It exists because it is one of the two axes of the **ROC curve** — the x-axis. Every time you look at an ROC plot, you are looking at FPR.

Also the formal statistical **Type I error rate** (α): the rate of rejecting a true null hypothesis, where the null hypothesis is "this sample is negative."

### 3. Formula

```
          FP            FP
FPR = ---------- = ------------------- = 1 − Specificity
       FP + TN      Actual Negatives
```
- **FP** = false alarms; **TN** = correct rejections; denominator = all actual negatives.

### 4. Manual example

```
FP = 10, TN = 70
FPR = 10 / 80 = 0.125 = 12.5%
Check: 1 − 0.875 = 0.125 ✓
```
Plain English: **12.5% of healthy people were falsely alarmed.**

### 5. Python

```python
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
fpr = fp / (fp + tn)                # 0.125

# The full FPR curve across all thresholds (for ROC):
from sklearn.metrics import roc_curve
fpr_arr, tpr_arr, thresholds = roc_curve(y_true, y_scores)
```
- `roc_curve` returns FPR and TPR at every distinct threshold present in `y_scores` — this is how the ROC curve is built.

### 6. Interpretation
Lower is better. 0.0 = no false alarms; 1.0 = every negative wrongly flagged.

| Value | Meaning |
|---|---|
| 0.60 | Catastrophic false-alarm rate |
| 0.40 | Very noisy |
| 0.20 | 1 in 5 negatives falsely flagged |
| 0.05 | Standard "α = 0.05" statistical convention |
| 0.001 | Required for high-volume automated screening |

### 7. Good vs bad values
Poor > 0.20, Average 0.10–0.20, Good 0.02–0.10, Excellent < 0.02. For anything operating at internet scale (billions of events), acceptable FPR is often < 0.0001, because absolute FP counts explode.

### 8. Business use cases
- **Biometrics / face recognition:** FAR (False Accept Rate) is exactly FPR; regulators and vendors specify systems at FAR = 1e-5 or 1e-6.
- **Cyber security IDS/IPS:** FPR drives alert fatigue; SOC capacity planning is an FPR budget.
- **A/B testing and statistics:** significance level α is the FPR you agree to tolerate.
- **Radar / sonar / signal detection:** the field where ROC analysis was invented (WWII radar operators).
- **Spam filtering:** FPR = the rate at which good mail is quarantined.
- **Sanctions/AML screening:** FPR determines the manual review workload.

### 9. Advantages
- The x-axis of the ROC curve — indispensable for threshold-independent analysis.
- Prevalence-independent.
- Directly maps to absolute false-alarm volume once you know the number of negatives.
- Standard language shared with classical statistics.

### 10. Limitations
- On imbalanced data, a tiny FPR still yields a huge absolute FP count, so FPR alone understates the operational problem. (FPR = 0.001 on 10M negatives = 10,000 false alarms.)
- Ignores the positive class.
- Threshold-dependent.

### 11. Common mistakes
1. Reading a low FPR as low false-alarm *volume*. Always multiply by the number of negatives.
2. Confusing FPR with FDR (**False Discovery Rate = FP/(FP+TP) = 1 − Precision**). FPR divides by actual negatives; FDR divides by predicted positives. Multiple-testing corrections (Bonferroni controls FPR/FWER; Benjamini-Hochberg controls FDR) hinge on this distinction.
3. Confusing FPR with the overall error rate.

### 12. Interview questions

**Easy — FPR formula?** FP/(FP+TN).
**Easy — What is a Type I error?** A false positive: claiming an effect/event that isn't there.
**Medium — FPR vs FDR?** FPR = FP/(FP+TN), denominator = all true negatives. FDR = FP/(FP+TP) = 1 − Precision, denominator = all discoveries. In genomics with 20,000 genes tested, FPR 0.05 gives ~1,000 false hits; if you only found 1,050 hits total, FDR ≈ 0.95 — nearly all discoveries are false. This is why FDR control is the standard in high-throughput science.
**Hard — Why is ROC (which uses FPR) misleading for rare events?** Because FPR's denominator (all negatives) is enormous, so adding thousands of false positives barely moves FPR, and the ROC curve looks great. Precision's denominator (predicted positives) is small, so the same false positives crater precision. PR curves expose what ROC hides.

---

## 3.6 FALSE NEGATIVE RATE (FNR = Type II Error Rate = Miss Rate)

### 1. Definition
Of all the real positives, what fraction did the model miss?

### 2. Intuition
The complement of recall, stated as a failure. It exists because "we miss 25% of cases" lands with far more force in a risk meeting than "we have 75% recall." It is also the formal **Type II error rate** (β), and `1 − β = statistical power = recall`.

### 3. Formula

```
          FN            FN
FNR = ---------- = ------------------- = 1 − Recall
       FN + TP      Actual Positives
```

### 4. Manual example

```
FN = 5, TP = 15
FNR = 5 / 20 = 0.25 = 25%
Check: 1 − 0.75 = 0.25 ✓
```
Plain English: **1 in 4 sick people is missed.**

### 5. Python

```python
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
fnr = fn / (fn + tp)                          # 0.25
fnr = 1 - recall_score(y_true, y_pred)        # 0.25
```

### 6. Interpretation
Lower is better.

| Value | Meaning |
|---|---|
| 0.60 | Missing most cases — the model is barely functioning as a detector |
| 0.40 | Missing 2 in 5 |
| 0.20 | Missing 1 in 5 — typical for production fraud models |
| 0.05 | Missing 1 in 20 — typical medical screening target |
| 0.00 | Catches everything; check FPR |

### 7. Good vs bad values
Poor > 0.30, Average 0.15–0.30, Good 0.05–0.15, Excellent < 0.05. For safety-critical systems, the acceptable FNR may be set by regulation or by a formal risk assessment (e.g. ISO 26262 / IEC 62304 style hazard analysis).

### 8. Business use cases
- **Medical diagnostics:** "miss rate" is the headline safety number.
- **Aviation & industrial safety:** missed fault detection maps to a hazard probability in a safety case.
- **Fraud & AML:** missed-fraud rate × average fraud value = direct expected loss, the number that funds the ML team.
- **Quality control:** "defect escape rate" — defective units reaching customers.
- **Cyber security:** missed-intrusion rate.
- **Insurance underwriting:** missed high-risk applicants.

### 9. Advantages
- Frames performance as risk, which is how safety and compliance teams think.
- Prevalence-independent.
- Multiplies cleanly with cost-per-miss to give expected loss.

### 10. Limitations
- Ignores the negative class; must be paired with FPR.
- Threshold-dependent.
- Same high variance problem as recall when positives are few.

### 11. Common mistakes
1. Confusing FNR with FPR under pressure. Mnemonic: **FN**R is about the class you **F**ailed to **N**otice — the positives.
2. Confusing FNR with FOR (**False Omission Rate = FN/(FN+TN) = 1 − NPV**). FNR divides by actual positives; FOR divides by predicted negatives.
3. Assuming FNR + FPR = 1. They have different denominators; there is no such relationship.

### 12. Interview questions

**Easy — FNR formula?** FN/(FN+TP) = 1 − Recall.
**Easy — Type II error?** A false negative: failing to detect a real effect/event.
**Medium — Relationship between FNR and statistical power?** Power = 1 − β = 1 − FNR = Recall. A study with 80% power has an FNR of 0.20 for the effect size it was designed to detect.
**Hard — Cost-optimal threshold from FPR and FNR?**
Minimise expected cost `E[C] = C_FP × FPR × N_neg + C_FN × FNR × N_pos`. Sweep the threshold, compute both rates from `roc_curve`, evaluate E[C], and pick the argmin. The theoretically optimal operating point is where the ROC curve's slope equals `(C_FP × N_neg) / (C_FN × N_pos)` — this is the *iso-cost line* tangency condition, and it is the correct answer to "how do I choose a threshold?"

---

## 3.7 POSITIVE PREDICTIVE VALUE (PPV)

**PPV is exactly Precision.** `PPV = TP/(TP+FP) = 15/25 = 0.60`.

Listed separately because medicine and diagnostics use "PPV," while ML uses "precision," and because PPV always travels with NPV as a pair.

- **Question:** "My test came back positive. What is the probability I actually have the disease?"
- **Key property:** **prevalence-dependent.** A test with fixed sensitivity and specificity has a different PPV in every population. See the Bayes formula in 3.4.
- **Why it matters clinically:** patients care about PPV, not sensitivity. Telling a patient "this test is 99% specific" is not an answer to "do I have cancer?" The answer is the PPV, which for a rare disease may be only 10–20% even with a 99%-specific test.

**Worked base-rate example.** Disease prevalence 0.1%. Test: Sens = 0.99, Spec = 0.99. Screen 100,000 people.
```
Diseased      = 100      → TP = 99,    FN = 1
Healthy       = 99,900   → FP = 999,   TN = 98,901
PPV = 99 / (99 + 999) = 99 / 1098 = 0.090  → only 9%!
NPV = 98,901 / 98,902 = 0.99999
```
A "99% accurate" test yields a positive result that is wrong 91% of the time. **This is the single most important intuition in all of classification metrics**, and it is asked in interviews constantly.

---

## 3.8 NEGATIVE PREDICTIVE VALUE (NPV)

### 1. Definition
Of all the samples the model predicted as **negative**, what fraction really were negative?

### 2. Intuition
The mirror of precision, on the other column: **"the test says I'm fine. Can I relax?"**

It exists because clearing someone is also a decision with consequences. Sending a patient home, letting a transaction through, passing a component to assembly — each is an implicit claim, and NPV measures how often that claim is true.

### 3. Formula

```
          TN                TN
NPV = ---------- = ---------------------------
       TN + FN      all Predicted Negatives
```
- **TN** = correctly cleared; **FN** = wrongly cleared (the dangerous ones)
- Denominator = the entire **predicted-negative column**
- Like precision, NPV is **prevalence-dependent**.

### 4. Manual example

```
TN = 70, FN = 5
Predicted Negatives = 70 + 5 = 75
NPV = 70 / 75 = 0.9333 = 93.33%
```
Plain English: the model cleared 75 people; 70 were genuinely healthy; **5 were sick and were wrongly reassured.** If you get a "you're fine" from this model, there is a 6.7% chance it is wrong.

### 5. Python

```python
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
npv = tn / (tn + fn)                             # 0.9333

# Trick: NPV is the precision of the negative class
from sklearn.metrics import precision_score
precision_score(y_true, y_pred, pos_label=0)     # 0.9333
```

### 6. Interpretation

| Value | Meaning |
|---|---|
| 0.40 | A negative result is meaningless — worse than a coin flip |
| 0.60 | 4 in 10 "all clear" results are wrong |
| 0.80 | 1 in 5 cleared cases is actually positive |
| 0.95 | 1 in 20 wrongly cleared |
| 0.999 | Safe to use as a rule-out test |

### 7. Good vs bad values
On rare-disease problems NPV is almost always very high (because TN dominates), so it is only informative when prevalence is high. Poor < 0.90, Average 0.90–0.95, Good 0.95–0.99, Excellent > 0.99 in a screening context.

### 8. Business use cases
- **Rule-out medical testing:** D-dimer for pulmonary embolism is used precisely because its NPV is very high — a negative result safely rules out the condition and avoids a CT scan.
- **Insurance fast-track underwriting:** high NPV lets you auto-approve low-risk applicants without review.
- **Manufacturing:** high NPV means units passed as "good" really are good, so you can skip downstream inspection.
- **Loan pre-approval:** confidence that applicants marked "won't default" truly won't.
- **Fraud auto-approve lanes:** a very high-NPV rule lets 95% of transactions skip the scoring pipeline entirely, saving latency and cost.
- **Cancer triage:** deciding which biopsies do not need a specialist second read.

### 9. Advantages
- Measures the reliability of the "all clear," which no other common metric does.
- Together with PPV, tells the end user exactly what each possible test result means.
- Directly interpretable as a posterior probability.

### 10. Limitations
- Prevalence-dependent → not portable between populations.
- **Deceptively high on imbalanced data.** With 1% prevalence, predicting "negative" for everyone gives NPV = 0.99. So a high NPV alone proves nothing.
- Undefined when nothing is predicted negative.
- Rarely reported in ML, so people forget it exists (`classification_report` shows it, disguised as the precision of class 0).

### 11. Common mistakes
1. Celebrating NPV = 0.99 on rare-event data without noticing it is the baseline.
2. Confusing NPV with specificity (NPV divides by predicted negatives; specificity by actual negatives).
3. Not realising that the class-0 row of `classification_report` gives you NPV (precision) and specificity (recall) for free.

### 12. Interview questions

**Easy — NPV formula?** TN/(TN+FN).
**Medium — NPV vs specificity?** NPV = TN/(TN+FN), a column ratio, prevalence-dependent, answers "is my negative result trustworthy?" Specificity = TN/(TN+FP), a row ratio, prevalence-independent, answers "does the test correctly clear healthy people?"
**Medium — Which four metrics does `classification_report` give you for a binary problem, and what are they really?**
The class-1 row gives Precision (PPV) and Recall (Sensitivity). The class-0 row gives Precision-of-0 (**NPV**) and Recall-of-0 (**Specificity**). So the standard report contains all four predictive/rate metrics if you know how to read it. Excellent interview answer.
**Hard — Why is NPV nearly useless as a headline metric in fraud detection?**
Because ~99.8% of transactions are legitimate, so any model that mostly predicts "legit" will have NPV ≈ 0.998 regardless of quality. The metric has almost no dynamic range on that data. Use recall, precision, PR-AUC and expected loss instead.

## 3.9 All eight metrics on one page (running example)

```
                        P R E D I C T E D
                    +------------+------------+
        |  Healthy  |  TN = 70   |  FP = 10   |  80  ->  Specificity = 70/80 = 0.875
 ACTUAL |           |            |            |          FPR         = 10/80 = 0.125
        | Diseased  |  FN =  5   |  TP = 15   |  20  ->  Recall/Sens = 15/20 = 0.750
        +-----------+------------+------------+          FNR         =  5/20 = 0.250
                          75           25
                           |            |
                  NPV = 70/75         Precision/PPV = 15/25
                      = 0.9333            = 0.600
```

| Metric | Formula | Value | Reads as |
|---|---|---|---|
| Accuracy | (TP+TN)/N | 0.850 | 85% of all calls correct |
| Error Rate | (FP+FN)/N | 0.150 | 15% of all calls wrong |
| Precision / PPV | TP/(TP+FP) | 0.600 | 60% of alarms are real |
| Recall / Sens / TPR | TP/(TP+FN) | 0.750 | 75% of real cases caught |
| Specificity / TNR | TN/(TN+FP) | 0.875 | 87.5% of healthy correctly cleared |
| FPR | FP/(FP+TN) | 0.125 | 12.5% of healthy falsely alarmed |
| FNR | FN/(FN+TP) | 0.250 | 25% of real cases missed |
| NPV | TN/(TN+FN) | 0.933 | 93.3% of "all clear" results are right |

Notice how one single model produces numbers from 0.60 to 0.93 depending on the question asked. **This is why "how good is the model?" has no single answer.**

---

# PART 4 — Combined Metrics

Precision and recall pull in opposite directions. Combined metrics collapse them into one number so you can rank models and run automated hyperparameter search. Each one embeds a *different assumption* about how much you care about each error.

## 4.1 F1 SCORE

### 1. Definition
The harmonic mean of precision and recall.

### 2. Intuition
You need one number for `GridSearchCV`, and you refuse to let the model cheat by maximising only one side.

Why the **harmonic** mean rather than the ordinary (arithmetic) mean? Because the harmonic mean is dominated by the smaller value, so it **punishes imbalance between precision and recall**.

Compare a model with Precision = 1.0 and Recall = 0.01 (flags one obvious case, ignores everything else):
- Arithmetic mean = (1.00 + 0.01)/2 = **0.505** → looks like a mediocre-but-acceptable model. Wrong.
- Harmonic mean = 2(1.00×0.01)/(1.00+0.01) = 0.02/1.01 = **0.0198** → correctly identifies it as useless.

That single comparison is the entire justification for F1, and it is a common interview question.

### 3. Formula

```
            Precision × Recall           2 × TP
F1 = 2 × ------------------------ = ---------------------
          Precision + Recall         2×TP + FP + FN
```
- **Precision** = TP/(TP+FP)
- **Recall** = TP/(TP+FN)
- The `2 ×` in front is what makes the harmonic mean land in [0,1] rather than [0,0.5].
- The right-hand form shows the important structural fact: **TN never appears.** F1 completely ignores true negatives, which makes it usable on imbalanced data where accuracy fails. It also means F1 is **not symmetric** — swap which class you call positive and F1 changes.
- F1 = 0 if either precision or recall is 0.

### 4. Manual example

```
Precision = 15/25 = 0.60
Recall    = 15/20 = 0.75

Step 1: numerator   = 2 × (0.60 × 0.75) = 2 × 0.45 = 0.90
Step 2: denominator = 0.60 + 0.75 = 1.35
Step 3: F1 = 0.90 / 1.35 = 0.6667

Cross-check with the TP form:
  2×TP = 30
  2×TP + FP + FN = 30 + 10 + 5 = 45
  F1 = 30 / 45 = 0.6667  ✓
```
Note F1 = 0.667 sits **below** the arithmetic mean of 0.675 — the harmonic mean always does, and the gap grows as precision and recall diverge.

### 5. Python

```python
from sklearn.metrics import f1_score, classification_report
f1_score(y_true, y_pred)                       # 0.6666666666666666
print(classification_report(y_true, y_pred, digits=4))
```
Output of `classification_report`:
```
              precision    recall  f1-score   support
           0     0.9333    0.8750    0.9032        80
           1     0.6000    0.7500    0.6667        20
    accuracy                         0.8500       100
   macro avg     0.7667    0.8125    0.7849       100
weighted avg     0.8667    0.8500    0.8559       100
```
Line-by-line reading of this report — memorise this, it is the whole point of the course:
- **Row `1`** = the positive class: precision 0.60, recall 0.75, F1 0.667, and `support` 20 = the number of real positives.
- **Row `0`** = the negative class: its "precision" 0.9333 is the **NPV**; its "recall" 0.8750 is the **Specificity**.
- **`accuracy`** 0.85 = overall.
- **`macro avg`** = unweighted mean across the two rows → treats the 20-sample class as equally important as the 80-sample class.
- **`weighted avg`** = mean weighted by support → dominated by the majority class. Weighted recall always equals accuracy.

### 6. Interpretation

| Value | Meaning |
|---|---|
| 0.40 | At least one of precision/recall is poor. Look at both. |
| 0.60 | Usable, unbalanced. |
| 0.80 | Solid, reasonably balanced performance on the positive class. |
| 0.95 | Excellent. |
| 1.00 | Perfect on the positive class (FP = FN = 0). Suspect leakage. |

**Always decompose F1 back into precision and recall before believing it.** F1 = 0.667 could be P=0.60/R=0.75 or P=0.95/R=0.51 — operationally completely different systems.

### 7. Good vs bad values
Highly problem-dependent. On a 1%-positive fraud dataset, F1 = 0.45 can be a strong production model; on a balanced sentiment task, F1 = 0.45 is a failure. Compare to (a) a majority/random baseline and (b) the previous model in production.

| Band | Balanced task | Rare-event task (~1%) |
|---|---|---|
| Poor | < 0.60 | < 0.10 |
| Average | 0.60 – 0.75 | 0.10 – 0.30 |
| Good | 0.75 – 0.90 | 0.30 – 0.55 |
| Excellent | > 0.90 | > 0.55 |

### 8. Business use cases
- **Kaggle and academic benchmarks:** the default leaderboard metric for imbalanced binary and multi-class tasks.
- **NLP:** named entity recognition, relation extraction, question answering — F1 is the field standard.
- **Information retrieval:** the metric F1 was originally designed for.
- **Fraud & churn model selection:** as a screening metric when FP and FN costs are roughly comparable.
- **Medical NLP / clinical coding:** extracting diagnoses from notes.
- **E-commerce product categorisation:** thousands of imbalanced classes, macro-F1 as the target.
- **Content moderation model comparison** during development, before cost-based thresholds are set.

### 9. Advantages
- One number, so it works with `GridSearchCV`, early stopping, and leaderboards.
- Ignores TN → not inflated by class imbalance the way accuracy is.
- Penalises models that sacrifice one side of the trade-off.
- Universally understood; extends to multi-class via macro/micro/weighted averaging.

### 10. Limitations
- **Assumes FP and FN are equally costly.** They almost never are. This is F1's central flaw and the reason F-beta exists.
- **Ignores TN entirely** — a model's skill at correctly clearing negatives is invisible to F1.
- **Asymmetric:** relabelling which class is "positive" changes F1, unlike MCC or accuracy.
- Threshold-dependent — reporting F1 at the default 0.5 threshold is often meaningless for a probabilistic model.
- Not a proper scoring rule; ignores confidence.
- Harder to explain to executives than precision/recall.
- Optimising F1 has odd properties: the F1-optimal threshold depends on prevalence, so an F1-tuned threshold silently breaks when prevalence drifts.

### 11. Common mistakes
1. **Reporting F1 without precision and recall.** The whole point is lost.
2. Using F1 when the costs are clearly asymmetric — use F2 or F0.5 or expected cost instead.
3. Averaging precision and recall arithmetically and calling it F1.
4. Comparing F1 across datasets with different prevalence.
5. In multi-class, using the default `average='binary'` and getting an error, or blindly using `'weighted'` when the minority classes are the ones you care about.
6. Believing F1 is threshold-independent. It is not; PR-AUC is the threshold-independent cousin.
7. Assuming `F1 = 0.8` means "80% correct." It means nothing of the sort.

### 12. Interview questions

**Easy — What is F1?** The harmonic mean of precision and recall: 2PR/(P+R).

**Easy — Range of F1?** 0 to 1, higher better.

**Medium — Why harmonic and not arithmetic mean?** Because the harmonic mean is pulled towards the minimum, so a model with P=1.0, R=0.01 scores 0.0198 rather than 0.505. It refuses to reward one-sided models.

**Medium — When is F1 the wrong metric?**
(a) When FP and FN have very different costs → use F-beta or expected cost. (b) When you care about correctly identifying negatives → use MCC or Balanced Accuracy. (c) When you need calibrated probabilities → use Log Loss/Brier. (d) When you want threshold-independent comparison → use PR-AUC. (e) When the negative class is the interesting one → F1 will ignore it.

**Medium — Can F1 be higher than both precision and recall?** No. The harmonic mean always lies between the two values (inclusive), so `min(P,R) ≤ F1 ≤ max(P,R)`, and F1 ≤ arithmetic mean.

**Hard — F1 vs MCC. Which would you report and why?**
MCC uses all four cells and is symmetric under class swapping, so it is a more complete and more honest single-number summary; a model must do well on both classes to score highly. F1 ignores TN and is asymmetric. F1 is preferable when the negative class is genuinely uninteresting (information retrieval: nobody cares about the billions of documents correctly not-returned) and for comparability with published baselines. MCC is preferable for honest overall model comparison, especially on imbalanced data. Best practice: report both.

**Hard — Why does the F1-optimal threshold depend on prevalence?**
Because precision depends on prevalence while recall does not. As prevalence falls, achieving a given precision requires a higher threshold, so the threshold that maximises F1 rises. Consequence for production: an F1-tuned threshold must be re-tuned when the incoming class balance drifts, or performance silently degrades. This is a genuine and common production failure mode.

---

## 4.2 F-BETA SCORE

### 1. Definition
A generalised F-score with a tunable weight, β, controlling how much more you value recall relative to precision.

### 2. Intuition
F1 hard-codes "precision and recall matter equally." Reality rarely agrees. F-beta exists to let you *state your business priority as a number*.

The interpretation of β: **recall is considered β times as important as precision.**
- β = 1 → equal → F1
- β > 1 → recall matters more (β = 2 → recall 2× as important)
- β < 1 → precision matters more (β = 0.5 → precision 2× as important)
- β → 0 → F-beta → Precision
- β → ∞ → F-beta → Recall

### 3. Formula

```
                          Precision × Recall
F_β = (1 + β²) × ------------------------------------
                   (β² × Precision) + Recall
```
Equivalent cell form:
```
                (1 + β²) × TP
F_β = ------------------------------------
       (1 + β²) × TP + β² × FN + FP
```
- **β** (beta) = the weight on recall. Squared throughout because the derivation minimises a weighted harmonic distance.
- **β²** multiplies Precision in the denominator, which *increases* the denominator's sensitivity to low precision only when β is small — hence small β favours precision.
- Read the cell form to see the cost weighting directly: **FN is multiplied by β²**, so β² is literally the relative cost of a miss versus a false alarm.

**Practical rule for choosing β:** if a false negative costs `k` times as much as a false positive, use **β = √k**. Example: a missed fraud costs $500, a false alarm costs $5 → k = 100 → β = 10.

### 4. Manual example (β = 2, i.e. F2)

```
Precision = 0.60, Recall = 0.75, β = 2, β² = 4

Step 1: (1 + β²) = 5
Step 2: numerator   = 5 × (0.60 × 0.75) = 5 × 0.45 = 2.25
Step 3: denominator = (4 × 0.60) + 0.75 = 2.40 + 0.75 = 3.15
Step 4: F2 = 2.25 / 3.15 = 0.7143
```
F2 (0.714) > F1 (0.667) because our model's recall (0.75) exceeds its precision (0.60), and F2 rewards recall.

### 5. Python

```python
from sklearn.metrics import fbeta_score
fbeta_score(y_true, y_pred, beta=1)     # 0.6667  == f1_score
fbeta_score(y_true, y_pred, beta=2)     # 0.7143  recall-weighted
fbeta_score(y_true, y_pred, beta=0.5)   # 0.6250  precision-weighted

# Using it in model selection
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
f2 = make_scorer(fbeta_score, beta=2)
# GridSearchCV(model, params, scoring=f2, cv=5)
```
- `make_scorer` wraps any metric into something `GridSearchCV` can optimise. This is the standard way to make your hyperparameter search optimise the metric your business actually cares about.

### 6. Interpretation
Same 0–1 scale as F1. Interpret relative to F1: `F_β > F1` means recall exceeds precision when β>1; the *value* itself is only comparable to other F-scores with the same β.

### 7. Good vs bad values
Same bands as F1, but **never compare an F2 to an F1** — they are different metrics. Fix β once, for the whole project, before you start.

### 8. Business use cases
- **Choosing β from a cost matrix** is the main use: cost-sensitive model selection.
- **Medical screening:** β = 2 to 4.
- **Fraud, AML, intrusion detection:** β = 2 to 10.
- **Spam filtering, content bans, auto-rejections:** β = 0.5 to 0.25.
- **Kaggle competitions** occasionally specify F2 (e.g. satellite/agriculture tasks) or F0.5.
- **Recommender systems:** β < 1, since screen space is precious.

### 9. Advantages
- Encodes business priorities explicitly and defensibly.
- Single number → usable in automated search.
- Reduces to F1 at β=1, so it generalises rather than replaces.
- The `β = √(cost ratio)` rule gives a principled way to set it.

### 10. Limitations
- β is a judgement call you must justify; stakeholders will argue about it.
- Still ignores TN.
- Still threshold-dependent.
- Not comparable across different β values, which confuses reports.
- Only encodes a *ratio* of costs, not absolute costs, so it cannot tell you whether the model is worth deploying at all — for that you need expected cost in currency.

### 11. Common mistakes
1. Comparing F2 of model A with F1 of model B.
2. Choosing β arbitrarily ("2 sounds right") instead of deriving it from cost.
3. Getting the direction backwards: **β > 1 favours RECALL.** Mnemonic: *big beta, big recall.*
4. Reporting only F2 without precision/recall.

### 12. Interview questions

**Easy — What does β control?** How much more important recall is than precision.
**Easy — F-beta at β=1?** F1.
**Medium — Choose β for cancer screening and justify it.** Recall dominates: β = 2–4. If a missed cancer is judged ~10× worse than a false alarm, β = √10 ≈ 3.
**Medium — What are the limits as β→0 and β→∞?** Precision and Recall respectively.
**Hard — Derive β from a cost matrix.** With cost `C_FN` per miss and `C_FP` per false alarm, the F-beta cell form weights FN by β² and FP by 1, so matching the cost ratio requires `β² = C_FN / C_FP`, i.e. `β = √(C_FN/C_FP)`.
**Hard — Why is expected cost better than F-beta if you have a cost matrix?** Because F-beta only captures the *ratio* of costs and still excludes TN benefit. Expected cost `C_FP·FP + C_FN·FN − B_TP·TP` gives an absolute currency figure, supports a go/no-go deployment decision, and directly identifies the optimal threshold.

---

## 4.3 F0.5 SCORE (Precision-weighted)

**Definition.** F-beta with β = 0.5 → **precision is twice as important as recall.**

**Formula & manual calculation:**
```
β = 0.5, β² = 0.25, (1 + β²) = 1.25
numerator   = 1.25 × (0.60 × 0.75) = 1.25 × 0.45 = 0.5625
denominator = (0.25 × 0.60) + 0.75 = 0.15 + 0.75 = 0.90
F0.5 = 0.5625 / 0.90 = 0.6250
```
F0.5 (0.625) < F1 (0.667) < F2 (0.714) for our model, because precision (0.60) < recall (0.75). The ordering of the three F-scores instantly tells you which side of the trade-off the model favours — a nice diagnostic trick.

**Python:** `fbeta_score(y_true, y_pred, beta=0.5)` → `0.625`

**When to use:** every false positive is expensive or user-visible.
- Spam filtering (a lost legitimate email is unacceptable)
- Automated account bans / content takedowns
- Recommender top-N lists
- Paid marketing outreach (each contact costs money)
- Auto-approval / auto-rejection pipelines with no human in the loop
- Legal document review where each flagged doc costs lawyer hours

**When NOT to use:** anything safety-critical, where a miss is worse than a false alarm.

**Common mistake:** using F0.5 in fraud/medical settings by copy-pasting a notebook. Check the direction of your costs.

**Interview (Medium) — Rank F0.5, F1, F2 for a model with P=0.9, R=0.3.**
Precision dominates, so F0.5 > F1 > F2. Compute: F1 = 2(0.27)/1.2 = 0.45; F2 = 5(0.27)/(4(0.9)+0.3) = 1.35/3.9 = 0.346; F0.5 = 1.25(0.27)/(0.25(0.9)+0.3) = 0.3375/0.525 = 0.643. So 0.643 > 0.45 > 0.346 ✓

---

## 4.4 F2 SCORE (Recall-weighted)

**Definition.** F-beta with β = 2 → **recall is twice as important as precision.** Computed above: **0.7143**.

**Python:** `fbeta_score(y_true, y_pred, beta=2)` → `0.7143`

**When to use:** a miss is worse than a false alarm.
- Disease and cancer screening
- Credit card fraud, AML
- Predictive maintenance / equipment failure
- Intrusion detection
- Churn prediction (when CLV ≫ retention offer cost)
- Safety-critical defect detection
- Missing-child / emergency alerting systems

**When NOT to use:** when the false-alarm burden is the binding constraint (limited analyst capacity, user-facing notifications).

**Advantages:** shifts the automated search toward high-recall models without letting precision collapse to zero (unlike optimising recall alone).

**Limitations:** still ignores TN; still cost-ratio-only; still threshold-dependent.

**Interview (Hard) — Your F2 is high but the fraud team says the model is useless. What happened?**
F2 tolerates low precision. The model probably has recall ~0.95 and precision ~0.05, generating an alert volume far beyond the team's review capacity. F2 has no notion of capacity. Switch to a capacity-constrained metric: **precision@k** where k = daily review capacity, or **recall at fixed alert budget**, or expected cost including analyst hours. This "the metric is fine but the model is unusable" scenario is a favourite senior-level question.

---

## 4.5 G-MEAN (Geometric Mean of Sensitivity and Specificity)

### 1. Definition
The geometric mean of recall (sensitivity) and specificity.

### 2. Intuition
F1 covers the positive class but ignores TN. G-Mean asks a different question: **"is the model good at BOTH classes simultaneously?"**

Using the geometric mean means that if either class is handled badly, the score collapses — you cannot buy a good G-Mean by sacrificing the minority class. That makes it the natural metric for imbalanced problems where both classes matter.

### 3. Formula

```
G-Mean = √( Sensitivity × Specificity ) = √( Recall × TNR )
```
- **Sensitivity** = TP/(TP+FN) — performance on the positive class
- **Specificity** = TN/(TN+FP) — performance on the negative class
- The square root makes it a mean rather than a product, keeping it on a 0–1 scale.
- **G-Mean = 0 if either term is 0** — an all-negative model scores exactly 0, unlike accuracy which scores 0.99.

A multi-class variant uses the geometric mean of all per-class recalls.

### 4. Manual example

```
Sensitivity = 15/20 = 0.750
Specificity = 70/80 = 0.875

Step 1: product = 0.750 × 0.875 = 0.65625
Step 2: G-Mean  = √0.65625 = 0.8101
```
Compare with Balanced Accuracy = (0.750+0.875)/2 = 0.8125. G-Mean (0.8101) is slightly lower — the geometric mean is always ≤ the arithmetic mean, and the gap widens as the two classes diverge.

### 5. Python

```python
# Manual
import numpy as np
from sklearn.metrics import confusion_matrix
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
sens = tp/(tp+fn); spec = tn/(tn+fp)
gmean = np.sqrt(sens*spec)                # 0.8100925873009825

# Or with imbalanced-learn
# from imblearn.metrics import geometric_mean_score
# geometric_mean_score(y_true, y_pred)    # 0.81009...
```

### 6. Interpretation

| Value | Meaning |
|---|---|
| 0.00 | The model completely fails one class (e.g. predicts only the majority class) |
| 0.40 | Badly skewed toward one class |
| 0.60 | Mediocre on at least one class |
| 0.80 | Reasonable on both classes |
| 0.95 | Strong on both classes |

### 7. Good vs bad values
Poor < 0.60, Average 0.60–0.75, Good 0.75–0.90, Excellent > 0.90. Because it is much harder to score highly on G-Mean than on accuracy for imbalanced data, these bands are genuinely informative.

### 8. Business use cases
- **Imbalanced learning research** — the standard metric in the `imbalanced-learn` literature and in SMOTE/undersampling papers.
- **Fraud detection** where both blocking fraud and not annoying good customers matter.
- **Medical diagnostics** — natural fit since it uses the sensitivity/specificity pair clinicians already use.
- **Fault detection in manufacturing** with rare defects.
- **Credit scoring** — regulators care about both approving good customers and rejecting bad ones.
- **Bioinformatics** (rare-variant detection).

### 9. Advantages
- Uses all four confusion-matrix cells.
- **Immune to the accuracy paradox** — a majority-class-only model scores 0, not 0.99.
- Punishes any model that neglects a class.
- Prevalence-independent (both components are row ratios).
- Symmetric to relabelling.

### 10. Limitations
- Less familiar to stakeholders than F1 or accuracy.
- Cannot encode asymmetric costs (there is no β knob).
- Because it uses specificity, it can still look reassuring when FP count is huge in absolute terms on very imbalanced data — G-Mean does not see the FP/TP ratio the way precision does. So it is *not* a substitute for precision when review capacity is the constraint.
- Threshold-dependent.
- Not in core sklearn.

### 11. Common mistakes
1. Confusing G-Mean of (sensitivity, specificity) with G-Mean of (precision, recall) — both exist in the literature; state which you mean.
2. Using it when alert volume is the real constraint (use precision instead).
3. Assuming it is the same as Balanced Accuracy — it is the geometric rather than arithmetic mean, and it penalises imbalance more harshly.

### 12. Interview questions

**Easy — What is G-Mean?** √(Sensitivity × Specificity).
**Medium — G-Mean vs Balanced Accuracy?** Same two ingredients, different mean. Balanced Accuracy is the arithmetic mean and is more forgiving; G-Mean is the geometric mean and collapses to 0 if either class is entirely missed. Use G-Mean when you want to *forbid* neglecting a class.
**Hard — Why does G-Mean handle imbalance better than accuracy?** Accuracy weights each *sample* equally, so the majority class dominates. G-Mean weights each *class* equally by construction (each factor has its own class-specific denominator) and multiplies them, so majority-class performance cannot compensate for minority-class failure.

---

## 4.6 BALANCED ACCURACY

### 1. Definition
The unweighted average of recall computed on each class. For binary problems, the arithmetic mean of sensitivity and specificity.

### 2. Intuition
"Accuracy, but with class imbalance neutralised." It answers: **"what would my accuracy be if both classes were equally common?"**

It exists as the minimal-effort drop-in replacement for accuracy on imbalanced data — same intuition, same 0–1 scale, none of the accuracy paradox. Its key anchor: **a model that predicts one class for everything scores exactly 0.5**, no matter how imbalanced the data.

### 3. Formula

```
                        Sensitivity + Specificity
Balanced Accuracy = ------------------------------- (binary)
                                  2

                    1
                  = --- × Σ recall_i                (multi-class, K classes)
                     K
```
- **Sensitivity** = TP/(TP+FN); **Specificity** = TN/(TN+FP)
- Equivalent formulation: it is accuracy computed with **sample weights** set so that each class carries equal total weight.
- Range 0–1; **0.5 = chance level** regardless of imbalance.
- An adjusted version, `adjusted=True` in sklearn, rescales chance to 0: `(BA − 0.5)/0.5` for binary.

### 4. Manual example

```
Sensitivity = 15/20 = 0.750
Specificity = 70/80 = 0.875
Balanced Accuracy = (0.750 + 0.875) / 2 = 1.625 / 2 = 0.8125
```
Compare: plain accuracy = 0.85, balanced accuracy = 0.8125. The plain figure is inflated because 80% of the data is the easier negative class.

**The imbalance demonstration.** 10,000 transactions, 100 fraud. Model predicts "legit" for everything:
```
TP=0, FN=100, TN=9900, FP=0
Accuracy          = 9900/10000            = 0.99   <- looks superb, is useless
Sensitivity       = 0/100                 = 0.00
Specificity       = 9900/9900             = 1.00
Balanced Accuracy = (0.00 + 1.00)/2       = 0.50   <- correctly says "no skill"
```

### 5. Python

```python
from sklearn.metrics import balanced_accuracy_score
balanced_accuracy_score(y_true, y_pred)                    # 0.8125
balanced_accuracy_score(y_true, y_pred, adjusted=True)     # 0.625  (chance rescaled to 0)
```
- `adjusted=True` maps chance performance to 0.0 and perfect to 1.0, making "is this better than random?" instantly readable. For binary it equals Youden's J (see 10.5) — a nice piece of trivia: `adjusted balanced accuracy == Youden's J == 0.625` here.

### 6. Interpretation

| Value | Meaning |
|---|---|
| 0.50 | No skill — equivalent to random or single-class prediction |
| 0.60 | Weak but real signal |
| 0.75 | Decent on both classes |
| 0.85 | Good |
| 0.95 | Excellent |
| < 0.50 | Worse than chance — check for inverted labels |

The floor of 0.5 is what makes this metric so useful: **any value near 0.5 is a red flag no matter what accuracy says.**

### 7. Good vs bad values
Poor < 0.60, Average 0.60–0.72, Good 0.72–0.85, Excellent > 0.85. Unlike accuracy, these bands hold reasonably well across prevalence levels, which is the point.

### 8. Business use cases
- **Any imbalanced classification** where you want a single accuracy-like headline number that does not lie.
- **Medical diagnostics** — sensitivity/specificity averaging matches clinical thinking.
- **Rare-event prediction:** equipment failure, rare disease, fraud.
- **Multi-class problems with skewed class counts** (e.g. defect-type classification where some defects are rare) — it becomes the mean per-class recall, ensuring rare defect types are not ignored.
- **Model selection / `GridSearchCV`** as `scoring='balanced_accuracy'` — the single easiest upgrade over `scoring='accuracy'` on imbalanced data.
- **Reporting to executives** who already understand "accuracy" — you can present it with a one-sentence explanation.

### 9. Advantages
- Same intuition and scale as accuracy → trivially explainable.
- Immune to the accuracy paradox; fixed 0.5 chance baseline.
- Extends naturally to multi-class as mean per-class recall.
- Available directly in sklearn and as a `scoring` string.
- Prevalence-independent.
- Uses all four cells.

### 10. Limitations
- **Ignores precision and therefore false-alarm volume.** Recall 0.90 with 50,000 false positives can still give a high balanced accuracy. If review capacity is the constraint, this metric will mislead you — pair it with precision or PR-AUC.
- Assumes both classes are equally important, which is itself a strong assumption (the opposite error from accuracy, but still an assumption).
- Cannot express asymmetric costs.
- Threshold-dependent.
- Less standard in leaderboards than F1, so harder to compare to published numbers.

### 11. Common mistakes
1. Treating balanced accuracy as a complete solution to imbalance. It fixes the *inflation* problem, not the *precision* problem.
2. Confusing it with weighted accuracy (`weighted avg` in `classification_report`), which is the opposite — that one weights *by* support and equals plain accuracy for recall.
3. Forgetting the 0.5 floor and reporting 0.55 as if it were meaningful skill.
4. Not using `adjusted=True` when you want a clean "better than chance" reading.

### 12. Interview questions

**Easy — What is balanced accuracy?** The average of per-class recalls; for binary, (sensitivity + specificity)/2.
**Easy — What does an all-majority-class model score?** Exactly 0.5.
**Medium — Balanced accuracy vs plain accuracy on our example?** 0.8125 vs 0.85. Plain accuracy is inflated by the 80-sample negative class; balanced accuracy weights the 20 positives equally.
**Medium — Balanced accuracy vs F1 for a rare-event problem?**
Balanced accuracy measures both classes' recall and ignores false-alarm volume. F1 measures the positive class only, but does account for false alarms via precision. If your constraint is analyst capacity, F1 (or precision@k) is the better guide; if your concern is that the model not ignore the minority class at all, balanced accuracy is clearer. Report both.
**Hard — Relationship to ROC-AUC?** Balanced accuracy at a given threshold is `(TPR + 1 − FPR)/2`, which is a single point on the ROC curve. ROC-AUC is the average of that quantity's behaviour across all thresholds — specifically, `ROC-AUC = ∫TPR d(FPR)`. So balanced accuracy is a one-threshold snapshot of the ROC curve; ROC-AUC is the whole curve. Equivalently, maximising balanced accuracy over thresholds maximises Youden's J, which locates the ROC point furthest above the diagonal.

---

# PART 5 — Probability Metrics

## 5.0 Why probability metrics are fundamentally different

Everything in Parts 2–4 needed **hard 0/1 predictions**. But your model does not natively output 0 or 1 — `predict_proba` outputs numbers like 0.03, 0.47, 0.98. The 0/1 comes from applying a threshold, and that threshold is a *business decision you made*, not something the model produced.

Threshold-based metrics therefore have three problems:

1. **They throw away information.** A prediction of 0.51 and a prediction of 0.99 both become "1". A model that is *confidently right* is indistinguishable from one that is *barely right*.
2. **They confound model quality with threshold choice.** Two teams reporting F1 = 0.70 might have wildly different models evaluated at different thresholds.
3. **They cannot tell you if probabilities are trustworthy.** Many decisions need the *number*, not the label: expected loss = probability × exposure; insurance premium = probability × payout; expected revenue = probability × order value.

Probability metrics fix this by scoring the **numbers themselves**.

**Two families:**

| Family | What it measures | Metrics |
|---|---|---|
| **Proper scoring rules** | Both *discrimination* (ranking) and *calibration* (are the numbers right?) | Log Loss, Brier Score |
| **Margin losses** | How far each point sits on the correct side of a decision boundary | Hinge Loss |

**Definition — proper scoring rule:** a loss that is minimised *only* when you report your true believed probabilities. There is no way to game it by lying about your confidence. Log Loss and Brier Score are both proper; accuracy and F1 are not. This is the theoretical reason models are *trained* on Log Loss and only *evaluated* on F1.

**Key decomposition to remember (Murphy decomposition of the Brier score):**
```
Brier Score = Calibration error − Discrimination (resolution) + Uncertainty(inherent)
```
So a proper scoring rule is a *combined* measure. A model can have perfect ranking (ROC-AUC = 1.0) but terrible Log Loss if all its probabilities are systematically shifted. Conversely, fixing calibration cannot fix bad ranking.

---

## 5.1 LOG LOSS (Logarithmic Loss = Cross-Entropy Loss = Negative Log-Likelihood)

### 1. Definition
The average negative log of the probability the model assigned to the **correct** class.

### 2. Intuition
Log Loss is a **confidence-weighted punishment system.** It asks not "were you right?" but "how much probability mass did you put on the truth?"

The behaviour that defines it: **being confidently wrong is punished brutally, without limit.**
- You say 0.99 and the truth is 1 → loss = −ln(0.99) = 0.01. Almost free.
- You say 0.50 and the truth is 1 → loss = −ln(0.50) = 0.69. Moderate.
- You say 0.01 and the truth is 1 → loss = −ln(0.01) = 4.61. Painful.
- You say 0.0001 and the truth is 1 → loss = 9.21. Devastating.
- You say 0.0 and the truth is 1 → loss = **infinity**.

This asymmetry is a feature. It exists because in the real world, confident wrong statements cause disasters — a model 99.9% certain a bridge is safe, that is wrong once, is worse than a model that says 60% every time. Log Loss encodes intellectual humility as a mathematical penalty.

It also exists for a practical reason: it is **differentiable and convex**, so gradient descent works. Logistic regression, neural networks, and gradient boosting all *train* by minimising exactly this. That is why the metric and the loss function share a name.

### 3. Formula

**Binary:**
```
            1    N
Log Loss = --- × Σ  −[ yᵢ × ln(pᵢ)  +  (1 − yᵢ) × ln(1 − pᵢ) ]
            N   i=1
```
Symbol by symbol:
- **N** = number of samples
- **i** = sample index
- **yᵢ** = the true label, either exactly 0 or exactly 1
- **pᵢ** = the model's predicted probability that sample i belongs to class 1, a number in (0,1)
- **ln** = natural logarithm (base e). Using log base 2 gives the answer in bits instead of nats; sklearn uses natural log.
- **The minus sign** in front makes the whole thing positive, because ln of a number below 1 is negative.

**How the two terms switch on and off** — this is the part beginners miss:
- If **yᵢ = 1**: the second term has factor (1−1) = 0, so it vanishes. Loss = **−ln(pᵢ)**.
- If **yᵢ = 0**: the first term has factor 0, so it vanishes. Loss = **−ln(1 − pᵢ)**.

So in both cases the loss is `−ln(probability assigned to the true class)`. The two-term form is just a compact way to write "pick the right one" without an if-statement.

**Multi-class (K classes):**
```
            1    N    K
Log Loss = --- × Σ    Σ  −[ y_{i,k} × ln(p_{i,k}) ]
            N   i=1  k=1
```
- **y_{i,k}** = 1 if sample i truly belongs to class k, else 0 (one-hot encoding)
- **p_{i,k}** = predicted probability that sample i is class k, with `Σ_k p_{i,k} = 1`
- Only the true class contributes for each sample, so this again reduces to `−ln(p of true class)`.

**Range:** `[0, ∞)`. Lower is better. 0 = perfect confident predictions.
**Clipping:** sklearn clips probabilities to `[eps, 1−eps]` to avoid infinite loss from a predicted 0.0.

### 4. Manual example

Four samples (small on purpose so you can follow every step):

| i | True yᵢ | Predicted pᵢ | Prob. of the TRUE class | Loss = −ln(that) |
|---|---|---|---|---|
| 1 | 1 | 0.9 | 0.9 | −ln(0.9) = 0.1054 |
| 2 | 0 | 0.2 | 1 − 0.2 = 0.8 | −ln(0.8) = 0.2231 |
| 3 | 1 | 0.6 | 0.6 | −ln(0.6) = 0.5108 |
| 4 | 0 | 0.7 | 1 − 0.7 = 0.3 | −ln(0.3) = 1.2040 |

```
Step 1 — sample 1: y=1, so loss = −ln(0.9)       = 0.1054
Step 2 — sample 2: y=0, so loss = −ln(1−0.2)     = −ln(0.8) = 0.2231
Step 3 — sample 3: y=1, so loss = −ln(0.6)       = 0.5108
Step 4 — sample 4: y=0, so loss = −ln(1−0.7)     = −ln(0.3) = 1.2040
Step 5 — sum   = 0.1054 + 0.2231 + 0.5108 + 1.2040 = 2.0433
Step 6 — mean  = 2.0433 / 4 = 0.5108
```
**Log Loss = 0.5108.**

Read sample 4: the model said 70% chance of class 1, the truth was class 0. That single confidently-wrong prediction contributes 1.204 — **59% of the total loss** — even though it is only 25% of the samples. That is Log Loss doing its job.

**Reference point:** a model that predicts 0.5 for everything scores `−ln(0.5) = 0.6931`. **Always compare your Log Loss to 0.6931** for a balanced binary problem. Above it, your model is worse than shrugging.

The general no-skill baseline for prevalence `q` is the entropy `−[q·ln(q) + (1−q)·ln(1−q)]`. For our 20% prevalence example that is `−[0.2·ln0.2 + 0.8·ln0.8] = 0.5004`.

### 5. Python

```python
import numpy as np
from sklearn.metrics import log_loss

y_true   = np.array([1, 0, 1, 0])
y_proba  = np.array([0.9, 0.2, 0.6, 0.7])
log_loss(y_true, y_proba)                  # 0.5108256237659907

# Multi-class: pass an (N, K) matrix of probabilities that sum to 1 per row
y_true_mc  = [0, 1, 2]
y_proba_mc = [[0.8, 0.1, 0.1],
              [0.2, 0.7, 0.1],
              [0.1, 0.2, 0.7]]
log_loss(y_true_mc, y_proba_mc)            # ~0.3635

# Real workflow
# probs = model.predict_proba(X_test)[:, 1]     <- column 1 = P(class 1)
# log_loss(y_test, probs)
```
Line-by-line:
- `log_loss(y_true, y_proba)` — **`y_proba` must be probabilities, not labels.** Passing hard 0/1 labels gives a near-infinite loss (clipped to ~34.5) and is one of the most common bugs.
- For binary, pass a 1-D array of `P(class=1)`, or an (N,2) matrix.
- `predict_proba(X)[:, 1]` — column 0 is P(class 0), column 1 is P(class 1). Getting this index wrong inverts your model.
- Optional `labels=` argument is required when a fold is missing a class, or sklearn raises an error.
- Set `eps` (older versions) to control clipping.

### 6. Interpretation

Log Loss is not on a 0–1 scale, so "good" is relative. Anchors for a **balanced binary** problem:

| Value | Meaning |
|---|---|
| 0.00 | Perfect and fully confident |
| 0.10 | Extremely strong — probabilities near the truth |
| 0.30 | Strong |
| 0.50 | Decent, roughly our example |
| 0.6931 | **The "always predict 0.5" baseline — no skill** |
| 1.00 | Worse than shrugging; the model is confidently wrong often |
| 2.00+ | Badly miscalibrated or inverted — check label encoding |

Converting to something intuitive: `exp(−Log Loss)` is the **geometric mean probability assigned to the truth.** Our 0.5108 → `exp(−0.5108) = 0.60`, i.e. on average the model gave the true answer 60% probability. This is a very effective way to explain Log Loss to non-technical stakeholders.

### 7. Good vs bad values

| Band | Balanced binary | 10-class problem |
|---|---|---|
| No-skill baseline | 0.693 | ln(10) = 2.303 |
| Poor | > 0.60 | > 2.00 |
| Average | 0.45 – 0.60 | 1.00 – 2.00 |
| Good | 0.25 – 0.45 | 0.40 – 1.00 |
| Excellent | < 0.25 | < 0.40 |

**Always state the baseline alongside the number.** Log Loss out of context is uninterpretable, and this is the metric where beginners most often report a bare number that nobody can judge.

### 8. Business use cases
- **Kaggle:** the most common leaderboard metric for probabilistic binary/multi-class tasks.
- **Insurance pricing:** the premium *is* the probability times the payout, so probability accuracy is the product.
- **Credit risk (PD models):** Basel regulations require calibrated probability of default; Log Loss is a core validation metric.
- **Ad tech / CTR prediction:** bid = P(click) × value. Google and Meta optimise Log Loss directly because a 10% probability error is a 10% bidding error.
- **Weather forecasting:** the field that invented proper scoring rules.
- **Sports betting / prediction markets:** expected value calculations require honest probabilities.
- **Medical risk calculators** (e.g. 10-year cardiovascular risk) where clinicians read the percentage.
- **Any neural network or GBM training loop** — it is the objective function.
- **Insurance / lending expected-loss provisioning** under IFRS 9.

### 9. Advantages
- Uses the full information in the predicted probabilities.
- **Proper scoring rule** — cannot be gamed by misstating confidence.
- Differentiable and convex → trainable by gradient descent.
- Threshold-free: no arbitrary 0.5.
- Rewards calibration *and* discrimination together.
- Naturally handles multi-class.
- Strong theoretical grounding (equals the KL divergence between true and predicted distributions, up to a constant; equals negative log-likelihood).

### 10. Limitations
- **Unbounded and dominated by outliers.** A single confidently-wrong prediction can wreck the average. One prediction of 1e-7 on a true positive contributes ~16 to that sample's loss.
- **Undefined at exactly 0 or 1** — requires clipping, so the metric is slightly implementation-dependent.
- **Not intuitive.** "Log Loss 0.42" means nothing to a business audience without the `exp(−LL)` translation and the baseline.
- Not comparable across datasets with different class balance or different numbers of classes.
- **Sensitive to class imbalance** in the sense that the baseline shifts, so the raw number is not portable.
- Does not tell you whether the model would make good *decisions* — you still need threshold metrics for that.
- Can be minimised by a model that is well-calibrated but poorly discriminating (e.g. always predicting the base rate) more easily than beginners expect — always report ROC-AUC or PR-AUC alongside.

### 11. Common mistakes
1. **Passing hard labels instead of probabilities.** `log_loss(y_test, model.predict(X))` — wrong. Use `predict_proba`.
2. Taking the wrong column: `predict_proba(X)[:, 0]` gives P(class 0) and silently inverts everything.
3. Reporting Log Loss without the no-skill baseline, making it uninterpretable.
4. Comparing Log Loss across datasets or across binary vs multi-class problems.
5. Trying to interpret it as a percentage.
6. Not clipping in a hand-rolled implementation → `inf` or `nan`.
7. Assuming a low Log Loss means high accuracy. A model can have good average probability quality yet poor accuracy at the 0.5 threshold, especially on imbalanced data.
8. Forgetting `labels=` in cross-validation when a fold lacks a class.

### 12. Interview questions

**Easy — What is Log Loss?** The mean negative log probability assigned to the correct class; lower is better, 0 is perfect.

**Easy — What is the Log Loss of a model that predicts 0.5 for everything on a balanced problem?** `−ln(0.5) = 0.693`.

**Easy — Range of Log Loss?** 0 to infinity.

**Medium — Why does Log Loss punish confident wrong answers so heavily?** Because `−ln(p) → ∞` as `p → 0`. The log function's steepness near zero encodes the real-world principle that confident false claims are far more damaging than hedged ones. It also gives gradient descent a strong signal exactly where the model is most wrong.

**Medium — Why train on Log Loss but report F1?** Log Loss is convex and differentiable so it can be optimised by gradient descent; 0-1 loss and F1 are not (zero gradient almost everywhere). But the business decision is a hard label, so the *report* uses threshold metrics. Train on a differentiable surrogate, evaluate on the decision metric.

**Medium — Is Log Loss the same as cross-entropy?** Yes, for classification. Cross-entropy `H(y, p) = −Σ y·ln(p)` averaged over samples *is* Log Loss. "Cross-entropy" is the information-theory name, "Log Loss" the ML-evaluation name, "negative log-likelihood" the statistics name.

**Hard — Can a model have ROC-AUC 0.99 and terrible Log Loss?**
Yes, and this is the single most instructive fact about probability metrics. Suppose the model's scores perfectly rank positives above negatives, but every score is squashed into [0.45, 0.55]. ROC-AUC depends only on ordering → 0.99. Log Loss depends on the values → poor, because true positives receive only ~0.55 probability. The fix is post-hoc **calibration** (Platt scaling / isotonic regression), which changes the values without changing the order — so it improves Log Loss and Brier while leaving ROC-AUC untouched. Great answer to give.

**Hard — Why is Log Loss a "proper" scoring rule and why does that matter?**
A scoring rule is proper if the expected score is optimised only when the forecaster reports their true subjective probability. Under Log Loss, if your true belief is `q` and you report `p`, expected loss `−[q ln p + (1−q) ln(1−p)]` is minimised at `p = q`. Consequence: you cannot improve your score by exaggerating or hedging. Metrics like accuracy are improper — on a 30%-prevalence problem, reporting your honest 0.3 belief and thresholding at 0.5 always yields "negative," so accuracy rewards you for distorting probabilities toward the extremes.

**Hard — How would you handle Log Loss with extreme class imbalance?**
(a) Report the entropy baseline for that prevalence so the number is interpretable. (b) Consider class-weighted Log Loss if the minority class matters more. (c) Recognise that the metric will be dominated by the majority class and pair it with PR-AUC. (d) Beware that resampling (SMOTE/undersampling) shifts the implied prior and *destroys calibration* — if you resample for training, you must recalibrate on the original prior before reporting Log Loss. This last point separates senior candidates from junior ones.

---

## 5.2 CROSS-ENTROPY LOSS

**Cross-Entropy Loss and Log Loss are the same metric under different names.** Any distinction you see is about which field is speaking, or about whether the softmax/sigmoid is folded into the loss implementation.

### The information-theory story (why it is called "entropy")

**Entropy** `H(y) = −Σ y·log(y)` measures the inherent unpredictability of the true distribution — how many bits you need on average to encode outcomes.

**Cross-entropy** `H(y, p) = −Σ y·log(p)` measures how many bits you need if you encode using the *wrong* distribution `p` instead of the true `y`.

**KL divergence** `D_KL(y‖p) = H(y,p) − H(y)` is the excess bits wasted by using the wrong distribution.

Because `H(y)` is a constant fixed by the data, **minimising cross-entropy is exactly equivalent to minimising KL divergence** — i.e. making the model's predicted distribution as close as possible to the true one. That equivalence is the theoretical justification for training classifiers on cross-entropy, and it is a strong interview answer.

### Naming map

| Name | Used by | Notes |
|---|---|---|
| Log Loss | sklearn, Kaggle, ML evaluation | `sklearn.metrics.log_loss` |
| Cross-Entropy Loss | deep learning | `torch.nn.CrossEntropyLoss`, `keras` `categorical_crossentropy` |
| Negative Log-Likelihood (NLL) | statistics | `torch.nn.NLLLoss` (expects log-probs) |
| Logistic Loss / Logloss | logistic regression | same objective |
| Deviance (×2) | GLM / statistics | `deviance = 2 × N × LogLoss` for binomial |

### Why probability metrics are different (restated for this section)
- They score **numbers**, not labels → no threshold needed.
- They are **proper** → cannot be gamed.
- They are **differentiable** → usable as training objectives.
- They measure **calibration + discrimination** together, so they answer "can I use this probability in a formula?" — which accuracy, F1, and even ROC-AUC cannot.

### Interview questions
**Easy — Cross-entropy vs Log Loss?** The same thing; different vocabulary.
**Medium — Why does minimising cross-entropy equal minimising KL divergence?** Because `H(y,p) = H(y) + D_KL(y‖p)` and `H(y)` does not depend on the model, so it is a constant offset.
**Hard — Why use cross-entropy instead of MSE for classification?**
Three reasons. (1) **Gradient behaviour:** with a sigmoid output, MSE's gradient contains the factor `σ'(z) = σ(1−σ)`, which vanishes when the model is confidently wrong — learning stalls exactly where it is most needed. Cross-entropy's gradient with a sigmoid simplifies to `(p − y)`, which is large when the error is large. (2) **Probabilistic correctness:** cross-entropy is the negative log-likelihood of a Bernoulli/Categorical model, so minimising it is maximum likelihood estimation. MSE corresponds to a Gaussian noise assumption, which is wrong for 0/1 targets. (3) **Convexity:** cross-entropy with a linear model is convex; MSE with a sigmoid is not.

---

## 5.3 BINARY CROSS-ENTROPY (BCE)

**Definition.** Cross-entropy for a two-class problem. The single-output form of Log Loss.

**Formula**
```
BCE = −(1/N) Σ [ yᵢ·ln(pᵢ) + (1 − yᵢ)·ln(1 − pᵢ) ]
```
- One output neuron with a **sigmoid** activation: `p = 1/(1 + e^(−z))`, so `p ∈ (0,1)` is the probability of class 1.
- `P(class 0) = 1 − p` is implied, not predicted separately.

**Manual example.** Identical to 5.1 → **0.5108**.

**Python / frameworks**
```python
from sklearn.metrics import log_loss
log_loss([1,0,1,0], [0.9,0.2,0.6,0.7])          # 0.5108

# Keras
# model.compile(loss='binary_crossentropy', optimizer='adam')
# final layer: Dense(1, activation='sigmoid')

# PyTorch — two options
# nn.BCELoss()            expects probabilities (after sigmoid)
# nn.BCEWithLogitsLoss()  expects raw logits, applies sigmoid internally  <-- USE THIS
```
**Why `BCEWithLogitsLoss` and not `BCELoss`:** it fuses the sigmoid and the log into one numerically stable expression (the log-sum-exp trick), avoiding `log(0)` overflow when logits are large. Applying `sigmoid` yourself then `BCELoss` is a well-known source of `nan` losses. This is a favourite deep-learning interview question.

**When to use:** binary classification; **and multi-label classification**, where you apply BCE independently to each of L output neurons (each with its own sigmoid). This is the standard multi-label setup.

**When NOT to use:** single-label multi-class problems — use categorical cross-entropy with softmax so the probabilities sum to 1.

**Business use cases:** churn, fraud, click prediction, credit default, disease presence, sentiment (binary), multi-label image tagging.

**Common mistakes**
1. Using `sigmoid + BCELoss` instead of `BCEWithLogitsLoss` → `nan` losses.
2. Using softmax with BCE, or sigmoid with categorical cross-entropy.
3. Using BCE for single-label multi-class, allowing probabilities that sum to 1.4.
4. Forgetting `pos_weight` in `BCEWithLogitsLoss` when the data is heavily imbalanced.

**Interview (Medium) — BCE vs CCE, when to use which?**
BCE + sigmoid: one output per label, labels independent → binary or **multi-label**. CCE + softmax: outputs compete and sum to 1 → **single-label multi-class**. The deciding question is "can a sample have two labels at once?" Yes → BCE. No → CCE.

---

## 5.4 CATEGORICAL CROSS-ENTROPY (CCE)

**Definition.** Cross-entropy for single-label multi-class classification with K mutually exclusive classes.

**Formula**
```
              1    N    K
CCE = − ---  ×  Σ    Σ   y_{i,k} · ln( p_{i,k} )
              N   i=1  k=1
```
- **K** = number of classes
- **y_{i,k}** = 1 if sample i is truly class k, else 0 (one-hot vector, exactly one 1 per row)
- **p_{i,k}** = predicted probability of class k for sample i, produced by **softmax**: `p_k = e^{z_k} / Σ_j e^{z_j}`, guaranteeing `Σ_k p_{i,k} = 1`
- Because y is one-hot, all terms vanish except the true class → the loss per sample is simply `−ln(p_true class)`.

**Manual example.** Three samples, three classes (A=0, B=1, C=2):

| i | True class | p(A) | p(B) | p(C) | p(true) | −ln(p) |
|---|---|---|---|---|---|---|
| 1 | A | **0.8** | 0.1 | 0.1 | 0.8 | 0.2231 |
| 2 | B | 0.2 | **0.7** | 0.1 | 0.7 | 0.3567 |
| 3 | C | 0.1 | 0.2 | **0.7** | 0.7 | 0.3567 |

```
Sum  = 0.2231 + 0.3567 + 0.3567 = 0.9365
CCE  = 0.9365 / 3 = 0.3122
```
(Verify in sklearn: `log_loss([0,1,2], [[.8,.1,.1],[.2,.7,.1],[.1,.2,.7]])` ≈ 0.3122.)

**Baseline for K classes:** a model predicting `1/K` for everything scores `ln(K)`. For 10 classes that is 2.303; for 1000 ImageNet classes, 6.908. Always quote this baseline.

**Python**
```python
from sklearn.metrics import log_loss
log_loss([0,1,2], [[.8,.1,.1],[.2,.7,.1],[.1,.2,.7]])   # 0.3122

# Keras
# loss='categorical_crossentropy'         -> labels one-hot encoded
# loss='sparse_categorical_crossentropy'  -> labels as integers 0..K-1  (saves memory)
# final layer: Dense(K, activation='softmax')

# PyTorch
# nn.CrossEntropyLoss()   expects RAW LOGITS + integer labels; applies log_softmax internally
```
**Critical PyTorch gotcha:** `nn.CrossEntropyLoss` already includes `log_softmax`. Adding a softmax layer before it applies softmax twice, flattening your gradients and quietly ruining training. Extremely common bug and a frequent interview question.

**Categorical vs sparse categorical:** identical mathematics; the only difference is whether labels arrive one-hot (`[0,1,0]`) or as integers (`1`). Use sparse for large K to save memory.

**Interpretation:** same as Log Loss, but the baseline is `ln(K)`, not 0.693.

**Business use cases:** image classification (ImageNet), document/topic classification, intent classification in chatbots, defect-type classification in manufacturing, language modelling (next-token prediction — the loss behind every LLM, where perplexity = `exp(CCE)`), speech phoneme classification.

**Advantages:** proper scoring rule; differentiable; handles any K; softmax gives a genuine probability distribution.

**Limitations:** requires mutually exclusive classes; dominated by frequent classes under imbalance (mitigate with class weights or focal loss); one-hot encoding assumes all wrong classes are equally wrong, which ignores class hierarchy (mistaking a husky for a wolf should cost less than mistaking it for a truck — label smoothing and hierarchical losses address this).

**Interview (Medium) — What is perplexity?** `exp(cross-entropy)`. For language models it reads as "the effective number of equally-likely choices the model was deciding between." Perplexity 20 means the model was as uncertain as if choosing uniformly among 20 words. It is the standard LLM evaluation metric and is just CCE in a friendlier unit.

**Interview (Hard) — What is label smoothing and why does it help?**
Instead of a hard one-hot target, use `1 − ε` for the true class and `ε/(K−1)` for the others (typically ε = 0.1). Because cross-entropy pushes the true-class logit toward infinity to reach probability 1.0, hard targets cause overconfidence and poor calibration. Label smoothing caps the achievable confidence, which improves calibration (lower ECE) and generalisation, usually at a tiny cost in raw accuracy. It is standard in modern vision and NLP training.

---

## 5.5 HINGE LOSS

### 1. Definition
A **margin-based** loss: penalise a prediction unless it is on the correct side of the boundary *by at least a safety margin of 1*.

### 2. Intuition
Log Loss says "always be more confident." Hinge Loss says something different and more geometric: **"get it right with room to spare, then stop caring."**

Once a point is correctly classified by a comfortable margin, its loss is exactly **zero** — it contributes nothing further to training. Only the points near or across the boundary matter. Those are the **support vectors**, and that is the entire idea of a Support Vector Machine.

Why does the margin exist? Because a boundary that only barely separates the training data will misclassify slightly-shifted test data. Demanding a margin is a form of regularisation that seeks the widest possible safety corridor between classes.

### 3. Formula

```
Hinge Loss (per sample) = max( 0 , 1 − y · f(x) )

                  1    N
Average = ------- ×  Σ  max( 0 , 1 − yᵢ · f(xᵢ) )
                  N   i=1
```
Symbol by symbol:
- **y** = the true label encoded as **−1 or +1** (NOT 0/1 — this is essential and a classic source of error)
- **f(x)** = the model's **raw decision function output** (the signed distance to the hyperplane, `w·x + b`), NOT a probability. In sklearn this is `decision_function(X)`.
- **y · f(x)** = the **margin**. Positive means correctly classified; its magnitude is the confidence.
- **1** = the required margin width.
- **max(0, ·)** = the "hinge": clamps negative values to zero, producing the flat region.

Behaviour table:

| y·f(x) | Situation | Loss |
|---|---|---|
| 2.0 | Correct, comfortably beyond the margin | 0 |
| 1.0 | Correct, exactly on the margin | 0 |
| 0.5 | Correct but inside the margin | 0.5 |
| 0.0 | Exactly on the boundary | 1.0 |
| −1.0 | Wrong | 2.0 |
| −3.0 | Badly wrong | 4.0 |

Note the penalty grows **linearly**, not logarithmically-to-infinity. Hinge Loss is therefore more robust to outliers than Log Loss.

**Squared hinge** `max(0, 1 − y·f(x))²` penalises violations more sharply and is differentiable everywhere (used by `LinearSVC(loss='squared_hinge')`, the sklearn default).

### 4. Manual example

Four samples, labels in {−1, +1}:

| i | True y | f(x) | Margin y·f(x) | 1 − margin | Loss = max(0, ·) |
|---|---|---|---|---|---|
| 1 | +1 | 2.0 | +2.0 | −1.0 | **0.0** (safe) |
| 2 | +1 | 0.3 | +0.3 | 0.7 | **0.7** (correct but inside margin) |
| 3 | −1 | −1.5 | +1.5 | −0.5 | **0.0** (safe) |
| 4 | −1 | 0.8 | −0.8 | 1.8 | **1.8** (wrong) |

```
Sum  = 0.0 + 0.7 + 0.0 + 1.8 = 2.5
Mean = 2.5 / 4 = 0.625
```
**Hinge Loss = 0.625.** Samples 1 and 3 are ignored entirely — they are not support vectors. Samples 2 and 4 drive all the learning.

### 5. Python

```python
import numpy as np
from sklearn.metrics import hinge_loss
from sklearn.svm import LinearSVC

y_true    = np.array([-1, -1,  1,  1])       # note: -1/+1, not 0/1
pred_dec  = np.array([-2.0, 0.5, 0.3, 2.0])  # decision_function outputs
hinge_loss(y_true, pred_dec)                 # 0.55

# Realistic workflow
# clf = LinearSVC().fit(X_train, y_train)
# scores = clf.decision_function(X_test)     <- NOT predict_proba
# hinge_loss(y_test, scores)
```
Line-by-line:
- `hinge_loss(y_true, pred_decision)` — the second argument must be the raw decision function, not a probability and not a label.
- sklearn accepts 0/1 labels and converts internally, but the mathematics is defined on −1/+1; be explicit to avoid confusion.
- **SVMs do not natively produce probabilities.** `SVC(probability=True)` fits an extra Platt-scaling model via internal cross-validation — it is slow and its probabilities are approximate. If you need probabilities, prefer logistic regression or a GBM.

### 6. Interpretation
Lower is better. **0 means every sample is correctly classified beyond the margin** — the data is separable and the boundary has a full-width corridor.

| Value | Meaning |
|---|---|
| 0.0 | Perfect separation with full margin |
| 0.3 | Most points safe; a few inside the margin |
| 1.0 | On average, points sit right at the boundary — weak separation |
| 2.0+ | Many points on the wrong side, badly |

Note Hinge Loss is **not** on a 0–1 scale and is unbounded above.

### 7. Good vs bad values
Poor > 1.0, Average 0.5–1.0, Good 0.1–0.5, Excellent < 0.1. Because the scale depends on the magnitude of `f(x)` — which depends on feature scaling and the regularisation parameter C — hinge loss values are **only comparable between models trained on identically-scaled data.** Always standardise features before an SVM.

### 8. Business use cases
- **SVM training objective** — its primary role. Anywhere `SVC`/`LinearSVC` is used.
- **Text classification** with high-dimensional sparse TF-IDF features, where linear SVMs remain very strong and fast.
- **Bioinformatics / genomics:** small-N, huge-p problems where SVMs' margin-maximisation regularises well.
- **Image classification pre-deep-learning** (HOG + SVM pedestrian detection is still deployed in embedded systems).
- **Ranking:** RankSVM and pairwise ranking losses are hinge-based.
- **Face verification / metric learning:** triplet loss `max(0, d(a,p) − d(a,n) + margin)` is structurally a hinge loss. Modern embedding systems (FaceNet-style) are built on this idea.
- **Anomaly detection:** One-Class SVM.

### 9. Advantages
- Directly encodes **margin maximisation**, a strong regularisation principle with solid generalisation theory (VC dimension bounds).
- **Sparse solutions:** only support vectors matter, so the trained model can be compact and prediction fast.
- **More robust to outliers than Log Loss** because the penalty grows linearly, not to infinity.
- Convex → globally optimal solution for linear models.
- Works well in high dimensions with few samples.

### 10. Limitations
- **Does not produce probabilities.** No calibrated output, so it cannot be used where a probability is the product (pricing, expected value, risk).
- **Not differentiable at the hinge point** (margin = 1) → needs subgradient methods; squared hinge fixes this.
- Value is scale-dependent, so it is a poor metric for reporting or cross-project comparison.
- **Sensitive to feature scaling** — unscaled features make it meaningless.
- Only defined for binary classification natively; multi-class needs one-vs-rest, one-vs-one, or the Crammer-Singer multi-class hinge.
- Less commonly used as an *evaluation* metric than as a training objective; reviewers will expect accuracy/F1/AUC alongside.
- SVMs scale poorly to very large N (kernel SVM is roughly O(N²)–O(N³)).

### 11. Common mistakes
1. **Passing 0/1 labels** and reasoning about the mathematics incorrectly. Hinge requires −1/+1.
2. Passing `predict_proba` output instead of `decision_function`.
3. Forgetting to standardise features before an SVM.
4. Comparing hinge loss across models with different regularisation strength or scaling and drawing conclusions.
5. Assuming an SVM's `predict_proba` (via `probability=True`) is well calibrated — it is approximate and computed by an internal Platt fit.
6. Using hinge loss when the downstream decision needs a probability.

### 12. Interview questions

**Easy — What is hinge loss?** `max(0, 1 − y·f(x))` with y ∈ {−1,+1}: zero loss once a point is correctly classified beyond a margin of 1, linear penalty otherwise.

**Easy — Which algorithm uses it?** Support Vector Machines.

**Medium — Hinge Loss vs Log Loss?**

| | Hinge | Log Loss |
|---|---|---|
| Output | Decision score (no probability) | Calibrated-ish probability |
| Label encoding | −1 / +1 | 0 / 1 |
| Loss for confident correct points | Exactly 0 | Small but nonzero |
| Penalty growth for wrong points | Linear | Logarithmic → ∞ |
| Outlier robustness | Better | Worse |
| Differentiable everywhere | No (hinge kink) | Yes |
| Gives probabilities | No | Yes |
| Typical algorithm | SVM | Logistic regression, NN, GBM |

**Medium — What is a support vector, in loss terms?** A training point with **non-zero hinge loss, or zero loss but sitting exactly on the margin** — i.e. a point at or inside the margin, or misclassified. Only these points have non-zero coefficients in the dual solution, so only they define the boundary.

**Hard — Why is hinge loss more robust to outliers than log loss?**
Consider a mislabelled point deep in the wrong class, with `y·f(x) = −20`. Hinge loss contributes 21 — large but finite and linear. Log Loss with a corresponding probability near 0 for the true class contributes ~20 in log terms but its **gradient** stays large and the loss is unbounded as p→0, so the optimiser will distort the whole boundary to accommodate that one point. Hinge's gradient is constant (magnitude 1) for all violating points, so a single extreme outlier exerts no more pull than a mild one. Bounded gradient = bounded influence.

**Hard — Relate hinge loss to triplet loss in metric learning.**
Triplet loss is `max(0, d(anchor, positive) − d(anchor, negative) + α)`. It has the same hinge structure: zero cost once the negative is farther than the positive by margin α, linear penalty otherwise. Both implement "be correct with a buffer, then stop optimising," which is why both produce sparse, boundary-focused learning signals. Modern face-recognition embeddings are trained this way, so the SVM intuition transfers directly.

---

# PART 6 — Ranking Metrics (from scratch)

## 6.0 THE RANKING EXAMPLE (used for all of Part 6)

Everything in this Part needs **scores, not labels**. Here is a 20-sample dataset we will use throughout. Sorted by predicted probability, highest first.

| Rank | Score (p) | True label | |
|---|---|---|---|
| 1 | 0.95 | **1** | ✔ |
| 2 | 0.90 | **1** | ✔ |
| 3 | 0.85 | 0 | ✘ |
| 4 | 0.80 | **1** | ✔ |
| 5 | 0.75 | **1** | ✔ |
| 6 | 0.70 | 0 | ✘ |
| 7 | 0.65 | **1** | ✔ |
| 8 | 0.60 | 0 | ✘ |
| 9 | 0.55 | **1** | ✔ |
| 10 | 0.50 | 0 | ✘ |
| 11 | 0.45 | **1** | ✔ |
| 12 | 0.40 | 0 | ✘ |
| 13 | 0.35 | 0 | ✘ |
| 14 | 0.30 | **1** | ✔ |
| 15 | 0.25 | 0 | ✘ |
| 16 | 0.20 | 0 | ✘ |
| 17 | 0.15 | 0 | ✘ |
| 18 | 0.10 | 0 | ✘ |
| 19 | 0.05 | 0 | ✘ |
| 20 | 0.02 | 0 | ✘ |

**8 positives, 12 negatives.** Prevalence = 8/20 = 0.40.

```python
import numpy as np
scores = np.array([0.95,0.90,0.85,0.80,0.75,0.70,0.65,0.60,0.55,0.50,
                   0.45,0.40,0.35,0.30,0.25,0.20,0.15,0.10,0.05,0.02])
y      = np.array([1,1,0,1,1,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0])
```

## 6.1 Why ranking metrics exist

Every threshold metric (accuracy, precision, recall, F1) answers: *"how good is this model **at this one threshold**?"*

But the threshold is a business choice, and it changes. Ranking metrics answer a better question: **"how good is the model at putting positives above negatives, regardless of where I eventually draw the line?"**

This matters because:
1. You want to compare models *before* choosing a threshold.
2. Many systems never threshold at all — they rank. Search results, recommendations, a fraud analyst's daily worklist sorted by risk, a collections team calling the top 500 accounts. There is no 0.5 anywhere in those systems.
3. The threshold will be re-tuned as capacity and costs change; the model should be judged on the whole curve.

**Ranking metrics depend only on the ORDER of the scores, not their values.** Multiply every score by 0.5 and every ranking metric is unchanged, while Log Loss and Brier change completely. That is both their strength (threshold-free) and their blind spot (they cannot detect miscalibration).

---

## 6.2 ROC CURVE (Receiver Operating Characteristic)

### 1. Definition
A plot of **True Positive Rate (y-axis) against False Positive Rate (x-axis)** as the decision threshold sweeps from high to low.

### 2. Intuition & origin
The name comes from WWII radar: engineers characterised the *operating* behaviour of radar *receivers* — how well operators distinguished enemy aircraft from flocks of birds — as the alarm sensitivity dial was turned.

The intuition: **turn the sensitivity dial from "paranoid" to "trigger-happy" and trace what happens.**
- Threshold = 1.0 (never alarm): TPR = 0, FPR = 0 → bottom-left corner.
- Threshold = 0.0 (always alarm): TPR = 1, FPR = 1 → top-right corner.
- Every threshold in between gives one point.

Connecting all those points traces the curve. It exists because a single confusion matrix is one arbitrary snapshot; the ROC curve is the *complete* picture of the score's discriminative ability.

**The diagonal line** from (0,0) to (1,1) is the random classifier: to gain 10% more true positives you pay exactly 10% more false positives. Any useful model bows **above** the diagonal. A curve *below* the diagonal means your model has learned the right pattern with the sign flipped — invert the predictions and you have a good model.

### 3. Formula (the axes)
```
TPR (y-axis) = Recall      = TP / (TP + FN)     "of real positives, fraction caught"
FPR (x-axis) = 1 − Spec    = FP / (FP + TN)     "of real negatives, fraction falsely alarmed"
```
Both are **row ratios**, so both are prevalence-independent — the key structural fact that explains ROC's behaviour on imbalanced data.

### 4. Manual construction (using the 6.0 data)

Compute TPR and FPR at each threshold. `P = 8` positives, `N = 12` negatives. Predict positive if `score ≥ threshold`.

| Threshold | TP | FP | FN | TN | TPR = TP/8 | FPR = FP/12 |
|---|---|---|---|---|---|---|
| 1.00 (none flagged) | 0 | 0 | 8 | 12 | 0.000 | 0.000 |
| 0.95 | 1 | 0 | 7 | 12 | 0.125 | 0.000 |
| 0.90 | 2 | 0 | 6 | 12 | 0.250 | 0.000 |
| 0.85 | 2 | 1 | 6 | 11 | 0.250 | 0.083 |
| 0.80 | 3 | 1 | 5 | 11 | 0.375 | 0.083 |
| 0.75 | 4 | 1 | 4 | 11 | 0.500 | 0.083 |
| 0.70 | 4 | 2 | 4 | 10 | 0.500 | 0.167 |
| 0.65 | 5 | 2 | 3 | 10 | 0.625 | 0.167 |
| 0.60 | 5 | 3 | 3 | 9 | 0.625 | 0.250 |
| 0.55 | 6 | 3 | 2 | 9 | 0.750 | 0.250 |
| 0.50 | 6 | 4 | 2 | 8 | 0.750 | 0.333 |
| 0.45 | 7 | 4 | 1 | 8 | 0.875 | 0.333 |
| 0.40 | 7 | 5 | 1 | 7 | 0.875 | 0.417 |
| 0.35 | 7 | 6 | 1 | 6 | 0.875 | 0.500 |
| 0.30 | 8 | 6 | 0 | 6 | 1.000 | 0.500 |
| 0.02 (all flagged) | 8 | 12 | 0 | 0 | 1.000 | 1.000 |

**How to read this table.** Each row is one possible operating point for your deployed system. Going down the table = lowering the threshold = becoming more aggressive. Notice the shape of the movement: **TPR rises in vertical jumps when the next-ranked sample is a positive; FPR rises in horizontal jumps when it is a negative.** A perfect model would go straight up to (0,1) and then straight right.

**ASCII ROC curve** for this data:

```
 1.0 |                                    * * * * * * * *
     |                              *  <- (0.500, 1.000) at thr 0.30
 0.9 |                         *
     |                    * <- (0.333, 0.875) at thr 0.45  <-- best Youden point
 0.8 |
 T   |               *  (0.250, 0.750)
 P.7 |          *
 R   |
 0.6 |      *  (0.167, 0.625)
     |
 0.5 |   *  (0.083, 0.500)
     |  *
 0.4 |
     | *  (0.083, 0.375)
 0.3 | 
     |*  (0.000, 0.250)
 0.2 |
     |*                           . . . <- random-guess diagonal
 0.1 |*                     . . .
     |               . . .
 0.0 +------------------------------------------------
     0.0   0.1   0.2   0.3   0.4   0.5  ...       1.0
                        F P R
```

### 5. Python

```python
from sklearn.metrics import roc_curve, RocCurveDisplay
import matplotlib.pyplot as plt

fpr, tpr, thresholds = roc_curve(y, scores)
# fpr, tpr        : arrays of coordinates, one per distinct threshold
# thresholds      : the score values used; thresholds[0] = inf so the curve starts at (0,0)

plt.plot(fpr, tpr, marker='o', label='Model')
plt.plot([0,1], [0,1], 'k--', label='Random')
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Recall)')
plt.legend(); plt.show()

# One-liner from a fitted estimator
# RocCurveDisplay.from_estimator(model, X_test, y_test)
```
Line-by-line:
- `roc_curve(y_true, y_score)` — `y_score` must be a **continuous score**: `predict_proba(X)[:,1]` or `decision_function(X)`. Passing hard labels gives a degenerate 3-point curve, which is a very common bug (if your ROC looks like two straight lines, this is why).
- `thresholds[0]` is `inf` by design so the curve is anchored at the origin.
- `drop_intermediate=True` (the default) removes collinear points for plotting speed; set `False` if you need every threshold.

### 6. Interpretation
- **Closer to the top-left corner = better.** The top-left (0,1) is the perfect classifier: all positives caught, zero false alarms.
- **The shape tells you where the model is useful.** A curve that rises steeply at the very left means the model's *top-ranked* predictions are highly reliable — ideal when you can only act on a few cases. A curve that is flat at the left but climbs later means the model has no confidently-correct top predictions.
- **Crossing curves mean no universal winner.** If Model A's curve is higher at low FPR and Model B's is higher at high FPR, A is better for a precision-constrained deployment and B for a recall-constrained one. AUC can hide this by averaging — always look at the curves, not just the numbers.

### 7. Good vs bad
Judged via AUC (next section) plus visual inspection of the region you will actually operate in.

### 8. Business use cases
- **Medical diagnostics:** the standard tool for comparing tests and selecting a clinical cut-off.
- **Credit scoring:** universal in bank model validation documents.
- **Radar / sonar / signal detection:** origin domain.
- **Biometrics:** the DET curve (a log-scaled ROC variant plotting FNR vs FPR) is the industry standard for face/fingerprint systems.
- **Cyber security:** comparing IDS engines.
- **Marketing:** comparing propensity models.
- **A/B comparing any two scoring models** before threshold selection.

### 9. Advantages
- Shows **all** operating points at once — you see the whole trade-off, not one snapshot.
- **Insensitive to class balance** (both axes are row ratios), so the curve does not change if you resample the negatives. This is genuinely useful when comparing a model across populations with different prevalence.
- Lets you pick a threshold to satisfy a hard constraint ("find the threshold with FPR ≤ 0.01").
- Visual, intuitive, universally recognised.
- Enables direct comparison of models trained with different score scales.

### 10. Limitations
- **Over-optimistic on imbalanced data** — the central criticism, explained fully in 6.4.
- Uses specificity/FPR, whose denominator is the huge negative class, so it does not reflect the analyst's experience of false-alarm volume.
- Hides absolute counts. An FPR of 0.01 looks negligible but is 100,000 false alarms on 10M negatives.
- Ignores calibration entirely.
- Curve crossings make single-number comparison unsafe.
- Needs a reasonable number of positives to be stable.

### 11. Common mistakes
1. **Passing hard labels to `roc_curve`.** Produces a meaningless 3-point curve.
2. Using `predict_proba(X)[:, 0]` → an upside-down curve (AUC below 0.5).
3. Reporting only the ROC curve for a 0.1%-positive problem. Always add the PR curve.
4. Choosing the threshold "closest to the top-left corner" without considering costs — that point maximises Youden's J, which implicitly assumes FP and FN cost the same.
5. Comparing ROC curves computed on different test sets.
6. Believing an ROC curve says anything about probability quality.

### 12. Interview questions

**Easy — What are the two axes of an ROC curve?** TPR (recall) on y, FPR (1 − specificity) on x.
**Easy — What does the diagonal represent?** Random guessing.
**Medium — What does a point at (0,1) mean?** A perfect classifier at that threshold: all positives caught, no false alarms.
**Medium — Why does ROC not change when you resample the negative class?** Because both axes are ratios within their own true class. Halving the negatives halves both FP and TN, leaving FPR unchanged; TPR does not involve negatives at all.
**Hard — Two models' ROC curves cross. How do you choose?**
Identify the operating region imposed by the business — e.g. "we can review 200 alerts/day," which pins a maximum FPR. Compare the curves *only in that region*, or compute **partial AUC** restricted to the relevant FPR range (`roc_auc_score(..., max_fpr=0.1)`). Alternatively compute expected cost at each model's optimal threshold and pick the cheaper one. Reporting full AUC here would be misleading.

---

## 6.3 ROC AUC (Area Under the ROC Curve)

### 1. Definition
The area under the ROC curve — a single number from 0 to 1 summarising the whole curve.

### 2. Intuition — the probabilistic interpretation
Forget geometry. ROC-AUC has an exact, beautiful meaning:

> **ROC-AUC is the probability that a randomly chosen positive sample receives a higher score than a randomly chosen negative sample.**

- AUC = 1.0 → every positive scores above every negative. Perfect ranking.
- AUC = 0.5 → the model orders positives and negatives no better than a coin flip.
- AUC = 0.0 → every positive scores below every negative. Perfectly inverted (flip the sign → AUC 1.0).
- AUC = 0.82 → pick a random sick patient and a random healthy patient; 82% of the time the model rates the sick one as riskier.

This is why AUC is the **discrimination** metric: it measures separability of the two score distributions, with zero reference to any threshold and zero reference to the actual score values.

It is mathematically identical to the **Mann-Whitney U statistic** normalised, and closely related to the **Gini coefficient**: `Gini = 2 × AUC − 1`, which is what credit-risk teams report (Gini 0.65 ⟺ AUC 0.825).

### 3. Formula

Geometric:
```
             1
ROC-AUC = ∫    TPR d(FPR)      (area under the curve)
             0
```
Practical (trapezoidal rule over the ROC points), and the one used for hand calculation:
```
              number of (positive, negative) pairs correctly ordered + 0.5 × ties
ROC-AUC = ------------------------------------------------------------------------
                        (number of positives) × (number of negatives)
```
- **Correctly ordered pair** = the positive's score is strictly greater than the negative's.
- **Ties** count as half a win, because a tie is a coin flip.
- Denominator = total number of positive-negative pairs.

### 4. Manual example — counting pairs by hand

`P = 8`, `N = 12` → total pairs = 8 × 12 = **96**.

Negative scores: 0.85, 0.70, 0.60, 0.50, 0.40, 0.35, 0.25, 0.20, 0.15, 0.10, 0.05, 0.02

For each positive, count how many negatives it beats:

| Positive score | Negatives it beats | Count |
|---|---|---|
| 0.95 | all 12 | 12 |
| 0.90 | all 12 | 12 |
| 0.80 | all except 0.85 | 11 |
| 0.75 | all except 0.85 | 11 |
| 0.65 | all except 0.85, 0.70 | 10 |
| 0.55 | all except 0.85, 0.70, 0.60 | 9 |
| 0.45 | all except 0.85, 0.70, 0.60, 0.50 | 8 |
| 0.30 | 0.25, 0.20, 0.15, 0.10, 0.05, 0.02 | 6 |

```
Step 1 — sum the wins: 12 + 12 + 11 + 11 + 10 + 9 + 8 + 6 = 79
Step 2 — no ties, so no half-credit
Step 3 — ROC-AUC = 79 / 96 = 0.8229
```
**ROC-AUC = 0.8229.** Interpretation: pick a random positive and a random negative; 82.3% of the time the positive is scored higher. Gini = 2(0.8229) − 1 = **0.6458**.

### 5. Python

```python
from sklearn.metrics import roc_auc_score, auc, roc_curve

roc_auc_score(y, scores)                        # 0.8229166666666666

# Equivalent via the curve
fpr, tpr, _ = roc_curve(y, scores)
auc(fpr, tpr)                                   # 0.8229166666666666

# Partial AUC — only the region with FPR <= 0.2 (rescaled to [0.5, 1])
roc_auc_score(y, scores, max_fpr=0.2)

# Multi-class
# roc_auc_score(y, proba_matrix, multi_class='ovr', average='macro')
# roc_auc_score(y, proba_matrix, multi_class='ovo', average='macro')
```
Line-by-line:
- `roc_auc_score(y_true, y_score)` — **the second argument must be a score, not a label.** Passing labels gives you Balanced Accuracy in disguise, not AUC. This is the most frequent AUC bug in existence.
- `max_fpr` computes **partial AUC** — essential when you only ever operate at very low FPR (biometrics, high-volume screening).
- `multi_class='ovr'` = one-vs-rest (each class against all others); `'ovo'` = one-vs-one (all class pairs, prevalence-insensitive, the Hand & Till measure).
- `average='macro'` treats classes equally; `'weighted'` weights by support.

### 6. Interpretation

| Value | Meaning | Verdict |
|---|---|---|
| 0.50 | No discrimination — coin flip | Useless |
| 0.60 | Weak | Poor |
| 0.70 | Acceptable | Fair |
| 0.80 | Good discrimination | Good — our example, 0.823 |
| 0.90 | Excellent | Excellent |
| 0.95+ | Outstanding | Verify no leakage |
| 1.00 | Perfect | **Almost certainly leakage** |
| < 0.50 | Inverted | Flip the labels/sign — then it is good |

The 0.7 / 0.8 / 0.9 bands are the widely-cited Hosmer-Lemeshow conventions from medical statistics and are safe to quote in interviews.

**Practical warning:** AUC ≥ 0.99 on a real business problem is nearly always **target leakage** — a feature that encodes the outcome (e.g. `n_collection_calls` in a default model, or `chargeback_flag` in a fraud model). Investigate before celebrating.

### 7. Good vs bad values by domain
Domain norms differ wildly, and quoting them well is a sign of experience:

| Domain | Typical strong AUC |
|---|---|
| Credit scoring (retail) | 0.75 – 0.85 (Gini 0.50 – 0.70) |
| Churn prediction | 0.75 – 0.85 |
| Ad click-through prediction | 0.75 – 0.80 (and CTR models live or die on Log Loss, not AUC) |
| Fraud detection | 0.90 – 0.99 (but see PR-AUC caveat) |
| Medical diagnostics | 0.85 – 0.95 |
| Genomics / polygenic risk | 0.60 – 0.70 is publishable |
| Image classification | AUC not typically used |

### 8. Business use cases
- **Credit risk:** reported as Gini; a regulated, audited number in bank model validation.
- **Churn and propensity modelling:** the default model-selection metric.
- **Medical diagnostics research:** required in essentially every diagnostic-accuracy paper.
- **Kaggle:** an extremely common leaderboard metric.
- **Marketing lead scoring** where the sales team works a ranked list.
- **Insurance risk segmentation.**
- **Recommendation / CTR model comparison** during offline evaluation.
- **Model monitoring in production:** a drop in AUC over time is the standard early-warning signal for concept drift.

### 9. Advantages
- Single number, threshold-free → clean model comparison and easy automation (`scoring='roc_auc'`).
- Beautiful, communicable probabilistic interpretation.
- **Invariant to class balance** — you can compare across populations.
- **Invariant to any monotonic transformation of the scores** — so it never punishes an uncalibrated model, which is useful when you only need ranking.
- Robust and low-variance compared to threshold metrics.
- Well-understood statistical properties (equivalent to Mann-Whitney U, so significance tests like DeLong's test exist for comparing two AUCs).

### 10. Limitations
- **Over-optimistic on imbalanced data** — see 6.4. This is the big one.
- **Blind to calibration.** AUC = 0.95 says nothing about whether a predicted 0.8 means 80%.
- **Averages over thresholds you would never use.** Most of the area lies in the high-FPR region that no real deployment operates in. Partial AUC fixes this.
- Two models with identical AUC can have very different curves and very different behaviour in your operating region.
- Ignores the *magnitude* of ranking errors — a positive ranked 2nd-worst and a positive ranked worst count nearly the same.
- Cannot express asymmetric costs.
- On very small test sets, AUC has high variance and should carry a confidence interval.

### 11. Common mistakes
1. **`roc_auc_score(y_test, model.predict(X_test))`** — passing hard labels. Use `predict_proba(X)[:,1]`.
2. Reporting only ROC-AUC for a 0.1%-positive fraud problem.
3. Assuming high AUC means the probabilities are usable in a formula.
4. Comparing AUC across different test sets or time periods and treating the difference as model improvement.
5. Interpreting AUC as accuracy ("82% accurate" — no; 82% correct *pairwise ranking*).
6. Not noticing AUC < 0.5 and concluding the model is bad rather than inverted.
7. Optimising AUC when the deployment only ever acts on the top 1% (use precision@k or partial AUC).
8. In multi-class, using `'ovr'` when class prevalences differ substantially — `'ovo'` is prevalence-insensitive and often the fairer choice.

### 12. Interview questions

**Easy — What does ROC-AUC of 0.5 mean?** No discriminative ability; equivalent to random ranking.
**Easy — What does AUC = 0.3 tell you?** The model is inverted; flipping its sign gives AUC 0.7.
**Easy — Range?** 0 to 1; 0.5 = chance.

**Medium — Give the probabilistic interpretation of AUC.** The probability that a randomly chosen positive is scored higher than a randomly chosen negative.

**Medium — Is AUC affected by the decision threshold?** No — it integrates over all thresholds. That is its main selling point and also why it cannot tell you how the deployed system will behave at your chosen threshold.

**Medium — Is AUC affected by class imbalance?** The *value* is largely unaffected (both ROC axes are within-class ratios), which sounds good but is precisely the problem: it means AUC does not reflect the deteriorating precision that imbalance causes. So: "not affected, and that's the issue."

**Medium — Relationship between AUC and Gini?** `Gini = 2·AUC − 1`. Credit teams use Gini because it maps chance to 0 rather than 0.5.

**Hard — Explain why ROC-AUC is misleading for imbalanced data, with numbers.** See 6.4 — worth memorising.

**Hard — Model A has AUC 0.85, Model B has AUC 0.83. Should you deploy A?**
Not necessarily. Check: (1) Is the difference statistically significant? With a small test set, ±0.02 may be noise — use DeLong's test or bootstrap CIs. (2) Do the curves cross? B may dominate in your operating region. (3) What about PR-AUC, if the data is imbalanced? (4) What about calibration, if downstream decisions need probabilities? (5) What about latency, cost, interpretability, and regulatory explainability? AUC is one input to a deployment decision, not the decision.

**Hard — Can you have AUC 0.9 and accuracy 0.5?**
Yes. AUC depends only on ranking; accuracy depends on the threshold. If all scores are squeezed into [0.6, 0.7] with perfect ordering, a 0.5 threshold predicts positive for everything → accuracy equals prevalence, while AUC stays 0.9. The fix is threshold tuning, not retraining, and this scenario is exactly why you should never report accuracy at the default threshold for a probabilistic model.

**Hard — What is partial AUC and when do you need it?**
AUC restricted to a specified FPR range (e.g. `[0, 0.05]`), rescaled to [0.5, 1]. Needed whenever the high-FPR region is operationally irrelevant: biometric verification at FAR = 1e-5, mass screening where you can only follow up 1% of people, or SOC alerting with fixed analyst capacity. Full AUC lets a model earn credit in regions you will never use.

---

## 6.4 WHY ROC-AUC IS MISLEADING FOR IMBALANCED DATA

This section deserves its own heading because it is the most-asked conceptual question in classification-metric interviews.

### The mechanism, in one sentence
**FPR's denominator is the entire negative class.** When negatives outnumber positives 1000:1, thousands of false positives barely move FPR, so the ROC curve stays near the top-left and AUC stays high — while precision, whose denominator is only the predicted positives, collapses.

### Worked demonstration

Fraud detection. **10,000 transactions, 100 fraudulent (1%), 9,900 legitimate.**

The model flags the top **1,000** riskiest transactions, and 90 of the 100 frauds are in there.

```
TP = 90        (frauds caught)
FP = 910       (legitimate transactions flagged)
FN = 10        (frauds missed)
TN = 8,990     (legitimate correctly cleared)

TPR / Recall = 90 / 100     = 0.900   <- excellent
FPR          = 910 / 9,900  = 0.092   <- looks tiny!
Specificity  = 8,990/9,900  = 0.908
Precision    = 90 / 1,000   = 0.090   <- terrible!
```

**Look at the two numbers side by side:**

| | Value | Story it tells |
|---|---|---|
| FPR | 0.092 | "Only 9% of legitimate transactions are affected — negligible." |
| Precision | 0.090 | "91% of everything the fraud team investigates is a waste of time." |

**Same 910 false positives. Same model. Same threshold.** ROC's axis divides by 9,900 and shrugs. PR's axis divides by 1,000 and screams.

The ROC point (0.092, 0.900) sits close to the top-left → this model's ROC curve looks superb and its AUC would be ~0.95+. Its PR curve is dismal. If you only looked at ROC-AUC, you would deploy a system that generates 910 useless investigations to catch 90 frauds.

### The severity scales with imbalance

Fix recall at 0.90 and vary prevalence, holding FPR at 0.05:

| Prevalence | Positives | Negatives | TP | FP = 0.05×Neg | Precision | ROC looks... |
|---|---|---|---|---|---|---|
| 50% | 5,000 | 5,000 | 4,500 | 250 | **0.947** | great — and it is |
| 10% | 1,000 | 9,000 | 900 | 450 | **0.667** | great — mostly true |
| 1% | 100 | 9,900 | 90 | 495 | **0.154** | great — but it is a lie |
| 0.1% | 10 | 9,990 | 9 | 500 | **0.018** | great — total fiction |

**ROC-AUC is identical in all four rows** (the score distributions are unchanged; only prevalence changed). Precision falls from 0.947 to 0.018. This table is the single best answer to the interview question, because it isolates the variable.

### Why PR-AUC does not have this problem
PR-AUC uses **Precision = TP/(TP+FP)**. Both terms are counts of predicted positives, and both are small. Adding false positives directly and proportionally destroys precision. PR-AUC therefore *does* change with prevalence — which is the honest behaviour, because the operational reality changes with prevalence.

### Why PR-AUC is preferred for rare-event problems
For **fraud detection, medical diagnosis, lead scoring, anomaly detection, rare-event prediction** and similar problems, four things are true, and each favours PR-AUC:

1. **The positive class is what you care about.** Nobody is impressed that you correctly ignored 9,990 normal transactions. PR-AUC never gives credit for TN; ROC-AUC does, via specificity.
2. **False positives consume a fixed, scarce resource.** Analyst hours, biopsy slots, sales calls. Precision is directly proportional to the waste; FPR is not.
3. **The baseline is honest.** A random model's PR-AUC ≈ prevalence (0.01 for 1% fraud), so a PR-AUC of 0.35 is visibly 35× better than chance. A random model's ROC-AUC is 0.5 regardless, which gives no sense of how hard the problem is.
4. **PR curves separate models that ROC curves conflate.** Because ROC compresses the region of interest into a sliver near FPR ≈ 0, two models with very different top-of-ranking behaviour can have nearly identical ROC-AUC and very different PR-AUC.

### The honest summary — when to use which

| Situation | Use |
|---|---|
| Roughly balanced classes | ROC-AUC (or either) |
| Both classes equally interesting | ROC-AUC |
| Comparing a test across populations with different prevalence | ROC-AUC (prevalence-invariant by design) |
| Rare positive class (< ~10%) | **PR-AUC** |
| You only care about the positive class | **PR-AUC** |
| False positives consume scarce capacity | **PR-AUC**, or precision@k |
| You will act only on the top-k | **Precision@k / partial AUC** |
| Decisions need probability values | **Log Loss / Brier + calibration curve** |
| Best practice for any imbalanced problem | **Report both**, plus the PR baseline (= prevalence) |

**One-line interview answer:** "ROC-AUC divides false positives by the huge negative class, so imbalance hides them; PR-AUC divides by the small predicted-positive set, so imbalance exposes them. On rare-event problems ROC-AUC can be 0.95 while precision is 0.09."

---

## 6.5 PRECISION-RECALL CURVE

### 1. Definition
A plot of **Precision (y-axis) against Recall (x-axis)** as the threshold sweeps from high to low.

### 2. Intuition
The PR curve asks the two questions the business actually asks, together:
- x-axis: **"How many of the real cases am I catching?"** (recall / coverage)
- y-axis: **"When I raise an alarm, how often am I right?"** (precision / trust)

Read it as a **menu of deals**: "you can catch 50% of fraud at 80% precision, or 90% of fraud at 15% precision — pick one." That is a business conversation, which is why product and operations stakeholders understand PR curves better than ROC curves.

Note the direction of travel. Lowering the threshold moves you **right and generally down**: more recall, less precision. So a PR curve typically starts high-left and descends to the right, the opposite visual shape from ROC.

### 3. Formula (the axes)
```
Precision (y) = TP / (TP + FP)     "of my alarms, fraction real"
Recall    (x) = TP / (TP + FN)     "of real cases, fraction caught"
```
Neither uses TN. **The PR curve is completely blind to true negatives** — this is exactly why it does not get flattered by a huge negative class.

**The baseline.** A random classifier's PR curve is a *horizontal line at y = prevalence*. For a 1%-positive problem that line is at 0.01. **Always draw this line on your plot** — without it, a PR curve is uninterpretable, and this is the most common PR-curve reporting failure.

### 4. Manual construction (6.0 data, P = 8, N = 12, prevalence = 0.40)

| Threshold | #Flagged | TP | FP | Precision = TP/#Flagged | Recall = TP/8 |
|---|---|---|---|---|---|
| 0.95 | 1 | 1 | 0 | 1.000 | 0.125 |
| 0.90 | 2 | 2 | 0 | 1.000 | 0.250 |
| 0.85 | 3 | 2 | 1 | 0.667 | 0.250 |
| 0.80 | 4 | 3 | 1 | 0.750 | 0.375 |
| 0.75 | 5 | 4 | 1 | 0.800 | 0.500 |
| 0.70 | 6 | 4 | 2 | 0.667 | 0.500 |
| 0.65 | 7 | 5 | 2 | 0.714 | 0.625 |
| 0.60 | 8 | 5 | 3 | 0.625 | 0.625 |
| 0.55 | 9 | 6 | 3 | 0.667 | 0.750 |
| 0.50 | 10 | 6 | 4 | 0.600 | 0.750 |
| 0.45 | 11 | 7 | 4 | 0.636 | 0.875 |
| 0.40 | 12 | 7 | 5 | 0.583 | 0.875 |
| 0.35 | 13 | 7 | 6 | 0.538 | 0.875 |
| 0.30 | 14 | 8 | 6 | 0.571 | 1.000 |
| 0.02 | 20 | 8 | 12 | 0.400 | 1.000 |

**Notice the sawtooth.** Precision goes 1.000 → 0.667 → 0.750 → 0.800 → 0.667 → 0.714... It is **not monotonic**. Every time the next-ranked sample is a negative, precision drops; every time it is a positive, precision jumps back up. ROC curves are always monotonic; PR curves are jagged. This is normal and expected — do not "fix" it.

**ASCII PR curve:**

```
 1.0 |* *                    <- (0.125,1.0), (0.250,1.0): the top-ranked 2 are both positive
     |    
 0.9 |
     |         *  (0.500, 0.800)
 0.8 |     *  (0.375, 0.750)
  P  |
  r.7 |   *  (0.250,0.667)      *  (0.625,0.714)   *  (0.750,0.667)
  e  |                    *  (0.500, 0.667)
  c.6 |                              *  (0.625,0.625)   * (0.750,0.600)
     |                                                  *  (0.875,0.636)
 0.5 |                                                       *  (0.875,0.583)
     |                                                          * (1.0, 0.571)
 0.4 |- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -* (1.0, 0.400)
     |          <-- RANDOM BASELINE at y = prevalence = 0.40 -->
 0.3 |
 0.0 +-------------------------------------------------------------
     0.0    0.2     0.4      0.6      0.8      1.0
                        R E C A L L
```
The curve sits well above the 0.40 baseline across most of the recall range → the model has real skill.

### 5. Python

```python
from sklearn.metrics import precision_recall_curve, PrecisionRecallDisplay
import matplotlib.pyplot as plt

precision, recall, thresholds = precision_recall_curve(y, scores)
# NOTE: precision and recall have length len(thresholds)+1
#       The final point is forced to (recall=0, precision=1) and has NO threshold.

plt.plot(recall, precision, marker='.', label='Model')
plt.axhline(y.mean(), linestyle='--', color='k',
            label=f'Baseline (prevalence={y.mean():.2f})')
plt.xlabel('Recall'); plt.ylabel('Precision'); plt.legend(); plt.show()

# PrecisionRecallDisplay.from_estimator(model, X_test, y_test)
```
Line-by-line:
- `precision_recall_curve` returns arrays one element longer than `thresholds`; the extra anchor point `(0, 1)` is artificial. Do not treat it as a real operating point — you cannot achieve it.
- `plt.axhline(y.mean())` draws the prevalence baseline. **Do this every time.**
- The x-axis (recall) is monotonically increasing as the threshold falls; precision is not.

### 6. Interpretation
- **Closer to the top-right corner = better.** Top-right (recall 1, precision 1) is perfection.
- **The area under the curve** summarises it (PR-AUC / Average Precision, next section).
- **Where the curve falls off a cliff** is the most actionable feature: if precision holds at 0.8 until recall 0.5 and then collapses, your operating point is recall ≈ 0.5. That elbow *is* the business decision.
- **Compare to the prevalence line.** A curve hugging the baseline means no skill.

### 7. Good vs bad
Judged via PR-AUC relative to the prevalence baseline. A curve that stays above `2 × prevalence` across a useful recall range is meaningful; one that hovers at prevalence is not.

### 8. Business use cases
- **Fraud detection** — the standard curve for choosing the alerting threshold given analyst capacity.
- **Information retrieval / search** — the curve the metric was invented for.
- **Recommender systems** — precision at low recall is what the user sees.
- **Anomaly detection** — rare positives by definition.
- **Medical diagnosis with rare conditions.**
- **Lead scoring** — "how many leads must sales call to reach 60% of the buyers, and what fraction of those calls are wasted?" reads straight off the curve.
- **Content moderation** — choosing an auto-action threshold vs a human-review threshold.
- **Object detection in computer vision** — PR curves per class are the basis of mAP.

### 9. Advantages
- **Honest under class imbalance** — the headline advantage.
- Both axes are about the positive class, matching what you care about in rare-event problems.
- Directly readable as a business trade-off menu.
- Immune to inflation by a large TN count.
- Reveals threshold "cliffs" that AUC hides.

### 10. Limitations
- **Not prevalence-invariant** — you cannot compare PR curves across datasets or time periods with different prevalence. (ROC can be compared; PR cannot. This trade-off is the mirror image of ROC's flaw.)
- **Baseline moves**, so "0.6 is good" is not a portable statement.
- **Jagged / non-monotonic**, which makes visual comparison of two models harder.
- **Linear interpolation between points is wrong** — the true curve between two PR points is not a straight line, which is why sklearn computes Average Precision (a step-wise sum) rather than trapezoidal area.
- Ignores true negatives entirely — if the negative class matters, this is a blind spot.
- Unstable when positives are few (a single sample can visibly move the curve).
- Ignores calibration.

### 11. Common mistakes
1. **Not plotting the prevalence baseline.** Without it, the plot cannot be judged.
2. Using `auc(recall, precision)` (trapezoidal) instead of `average_precision_score`. Trapezoidal interpolation on a PR curve is optimistically biased — a well-known technical point that impresses interviewers.
3. Comparing PR curves computed on test sets with different prevalence (e.g. before and after downsampling negatives) — completely invalid.
4. Passing hard labels instead of scores.
5. Being confused by the sawtooth and assuming a bug.
6. Reading the artificial `(0, 1)` endpoint as an achievable operating point.
7. Reporting PR-AUC on a downsampled test set. **Never resample the test set.** Resampling training data is fine; resampling test data invalidates precision, PR-AUC, and calibration.

### 12. Interview questions

**Easy — Axes of a PR curve?** Precision on y, Recall on x.
**Easy — What is the random baseline?** A horizontal line at y = prevalence.
**Medium — Why is the PR curve jagged while ROC is smooth?** Because precision's denominator (the number of flagged items) grows by one with every threshold step, and its numerator only grows when the new item is a true positive. So precision falls on each negative and jumps on each positive. TPR and FPR are monotonic in the threshold, so ROC never decreases.
**Medium — Why is trapezoidal interpolation wrong for PR curves?** Because between two adjacent PR operating points the achievable precision does not vary linearly with recall (it follows a hyperbola-like path determined by the counts). Linear interpolation overestimates the area. Average Precision, a weighted step sum, avoids the issue.
**Hard — When would you prefer ROC over PR even on imbalanced data?**
When you need to compare the same model across populations with different prevalence — for example validating a diagnostic model in a screening clinic (0.5% prevalence) and a referral clinic (20% prevalence). ROC-AUC is prevalence-invariant, so a change in ROC-AUC signals a genuine change in discriminative power, whereas PR-AUC would change simply because prevalence changed. Also when the negative class genuinely matters, or when you need to satisfy a specificity-based regulatory constraint.

---

## 6.6 PR AUC (Area Under the Precision-Recall Curve)

### 1. Definition
The area under the precision-recall curve, summarised as a single number.

### 2. Intuition
The same role ROC-AUC plays, but for the PR curve: **one number for "how good is the ranking of the positive class, accounting for false-alarm cost?"**

### 3. Formula
Conceptually `∫₀¹ Precision d(Recall)`. In practice **do not compute it trapezoidally.** Use **Average Precision** (6.7), which is the step-wise sum sklearn provides:

```
PR-AUC ≈ Average Precision = Σₙ (Recallₙ − Recallₙ₋₁) × Precisionₙ
```

**Critical baseline:** a random model's PR-AUC ≈ **prevalence**. Not 0.5. State the baseline every single time.

### 4. Manual example
Computed in 6.7 as **0.7673** for our data, against a baseline of 0.40 → the model is ~1.9× better than random. On a 1%-prevalence problem, a PR-AUC of 0.35 would be 35× better than random, so PR-AUC values must always be read relative to prevalence.

### 5. Python

```python
from sklearn.metrics import average_precision_score, precision_recall_curve, auc

average_precision_score(y, scores)                 # 0.7673430735930736   <- USE THIS

# The trapezoidal version — biased, shown only so you recognise it in other people's code
p, r, _ = precision_recall_curve(y, scores)
auc(r, p)                                          # slightly different, optimistically biased

print(f"Baseline (prevalence) = {y.mean():.3f}")   # 0.400
```

### 6. Interpretation
Relative to prevalence, always.

| Prevalence | PR-AUC = prevalence | PR-AUC = 3× prev | PR-AUC = 0.8 |
|---|---|---|---|
| 0.50 | 0.50 = no skill | 1.00+ impossible | good |
| 0.10 | 0.10 = no skill | 0.30 = decent | excellent |
| 0.01 | 0.01 = no skill | 0.03 = real signal | outstanding |

A useful normalised version is **PR-AUC lift = PR-AUC / prevalence**, which is comparable across datasets. Lift of 1 = no skill; lift of 10 = strong.

### 7. Good vs bad values

| Band | Balanced (prev 0.5) | Rare (prev 0.01) |
|---|---|---|
| No skill | 0.50 | 0.01 |
| Poor | < 0.65 | < 0.05 |
| Average | 0.65 – 0.80 | 0.05 – 0.20 |
| Good | 0.80 – 0.90 | 0.20 – 0.45 |
| Excellent | > 0.90 | > 0.45 |

### 8. Business use cases
- **Credit card fraud** — the industry-standard offline metric.
- **Medical diagnosis of rare conditions.**
- **Lead scoring** — where only a small fraction of leads convert.
- **Anomaly / intrusion detection.**
- **Rare-event prediction:** equipment failure, rare defects, churn in a low-churn business.
- **Information retrieval and search relevance.**
- **Recommendation systems** (as MAP, see 6.7).
- **Object detection in vision** — mAP is a PR-AUC average.
- **Kaggle** — the specified metric for many imbalanced competitions.

### 9. Advantages
- **Honest under imbalance** — the reason it exists.
- Focuses entirely on the positive class.
- Threshold-free single number → usable in `GridSearchCV` (`scoring='average_precision'`).
- Much more sensitive than ROC-AUC to improvements in the top of the ranking, which is where deployments operate.

### 10. Limitations
- **Baseline depends on prevalence** → not comparable across datasets, and easy to misreport.
- Ignores true negatives.
- Higher variance than ROC-AUC, especially with few positives.
- Less familiar; you will have to explain it.
- Ignores calibration.
- Cannot encode asymmetric costs directly.

### 11. Common mistakes
1. Reporting PR-AUC **without prevalence.** The number is meaningless alone.
2. Using `auc(recall, precision)` instead of `average_precision_score`.
3. Comparing PR-AUC between a downsampled and a natural-prevalence test set.
4. Assuming a PR-AUC of 0.30 is bad. On a 1% problem it is excellent.

### 12. Interview questions
**Easy — Baseline PR-AUC for a random model?** The prevalence (positive class fraction).
**Medium — Why prefer PR-AUC over ROC-AUC for fraud?** Because precision's denominator is the small set of flagged transactions, so PR-AUC reflects the analyst's wasted-work rate, whereas FPR's denominator is the enormous legitimate population and hides it.
**Medium — Your PR-AUC is 0.25. Good or bad?** Unanswerable without prevalence. At 1% prevalence that is 25× lift — excellent. At 40% prevalence it is below chance — broken.
**Hard — Which is more sensitive to improvements at the top of the ranking, and why?** PR-AUC. Moving one false positive out of the top 100 changes precision@100 by 1 percentage point but changes FPR by 1/N_neg, which is negligible when negatives are numerous. So PR-AUC rewards exactly the improvements that matter operationally.

---

## 6.7 AVERAGE PRECISION (AP)

### 1. Definition
The precision values at each threshold where a new positive is retrieved, weighted by the increase in recall it produced. The standard, unbiased estimate of PR-AUC.

### 2. Intuition
Walk down the ranked list from the top. Every time you hit a real positive, write down the precision at that exact point. Average those numbers.

That is it. AP rewards **finding positives early**, because precision is high near the top of a good ranking. A model that puts all 8 positives in the top 8 slots has AP = 1.0. A model that scatters them scores lower even if it eventually finds them all.

Because it is defined by a step-wise sum rather than interpolation, AP avoids the optimistic bias of trapezoidal PR area.

### 3. Formula
```
AP = Σ  ( Rₙ − Rₙ₋₁ ) × Pₙ
     n
```
- **n** indexes the thresholds (equivalently, the ranked positions)
- **Rₙ** = recall at threshold n; **Rₙ₋₁** = recall at the previous threshold
- **(Rₙ − Rₙ₋₁)** = the recall gained at this step. It is `1/P_total` when the item is a positive and **0** when it is a negative — so negatives contribute nothing directly. They hurt only by depressing the precision of later positives.
- **Pₙ** = precision at threshold n

With `P_total` positives and no ties, this simplifies to the form used for hand calculation:
```
        1
AP = -------- ×  Σ  Precision at the rank of each positive
      P_total    positives
```

### 4. Manual example (6.0 data)

Walk down the ranked list. Record precision **only at the ranks where the label is 1**.

| Rank | Score | Label | TP so far | Precision = TP/rank | Counted? |
|---|---|---|---|---|---|
| 1 | 0.95 | **1** | 1 | 1/1 = **1.0000** | ✔ |
| 2 | 0.90 | **1** | 2 | 2/2 = **1.0000** | ✔ |
| 3 | 0.85 | 0 | 2 | 2/3 = 0.6667 | — |
| 4 | 0.80 | **1** | 3 | 3/4 = **0.7500** | ✔ |
| 5 | 0.75 | **1** | 4 | 4/5 = **0.8000** | ✔ |
| 6 | 0.70 | 0 | 4 | 4/6 = 0.6667 | — |
| 7 | 0.65 | **1** | 5 | 5/7 = **0.7143** | ✔ |
| 8 | 0.60 | 0 | 5 | 5/8 = 0.6250 | — |
| 9 | 0.55 | **1** | 6 | 6/9 = **0.6667** | ✔ |
| 10 | 0.50 | 0 | 6 | 6/10 = 0.6000 | — |
| 11 | 0.45 | **1** | 7 | 7/11 = **0.6364** | ✔ |
| 12 | 0.40 | 0 | 7 | 7/12 | — |
| 13 | 0.35 | 0 | 7 | 7/13 | — |
| 14 | 0.30 | **1** | 8 | 8/14 = **0.5714** | ✔ |

```
Step 1 — sum the 8 bolded precisions:
  1.0000 + 1.0000 + 0.7500 + 0.8000 + 0.7143 + 0.6667 + 0.6364 + 0.5714
= 6.1388

Step 2 — divide by the number of positives (8):
  AP = 6.1388 / 8 = 0.7674
```
**Average Precision = 0.7673** (matching sklearn to 4 decimals).

Compare: ROC-AUC = 0.8229, AP = 0.7673, prevalence = 0.40. AP is lower, as it usually is — it is the stricter metric.

### 5. Python

```python
from sklearn.metrics import average_precision_score
average_precision_score(y, scores)                       # 0.7673430735930736

# Multi-label / multi-class
# average_precision_score(Y_true, Y_score, average='macro')     # mean AP across labels = mAP
# average_precision_score(Y_true, Y_score, average='micro')     # pool all label decisions
```
- `average='macro'` across classes gives **mAP (mean Average Precision)** — the standard metric in object detection and information retrieval.
- Use `scoring='average_precision'` in `GridSearchCV` to optimise it.

### 6. Interpretation
Identical to PR-AUC: compare to prevalence. `AP = prevalence` means no skill; `AP = 1.0` means every positive is ranked above every negative.

### 7. Good vs bad
See the PR-AUC table in 6.6.

### 8. Business use cases
- **Object detection (COCO, Pascal VOC):** mAP@[.5:.95] is *the* benchmark metric.
- **Information retrieval and search:** MAP has been the standard TREC metric for decades.
- **Recommendation systems:** MAP@k measures ranking quality of the top-k list.
- **Fraud detection:** ranking risk scores for the analyst queue.
- **Face retrieval / image search.**
- **Kaggle** imbalanced competitions.

### 9. Advantages
- Unbiased estimate of PR-AUC (no interpolation artefacts).
- Rewards early retrieval of positives — matches how ranked lists are consumed.
- Single threshold-free number.
- Extends cleanly to multi-label and multi-class via mAP.

### 10. Limitations
- Prevalence-dependent baseline.
- High variance with few positives.
- Ignores TN and ignores calibration.
- Sensitive to tie handling — many identical scores (common with shallow trees) make AP unstable and implementation-dependent.

### 11. Common mistakes
1. Confusing **AP** (area under one PR curve) with **mAP** (mean of APs across classes or queries).
2. Confusing AP with `precision_score`.
3. Using trapezoidal `auc(r, p)` and calling it AP.
4. Reporting AP without prevalence.
5. In multi-label settings, using `average='micro'` and `'macro'` interchangeably — micro is dominated by frequent labels; macro treats rare labels equally.

### 12. Interview questions
**Easy — AP vs PR-AUC?** AP is the standard step-wise estimator of the area under the PR curve. In practice the terms are used interchangeably; AP is the correct computation.
**Easy — AP vs mAP?** mAP is the mean of AP over multiple classes (object detection) or multiple queries (search).
**Medium — Why does AP reward ranking positives early?** Precision at rank k is high when few negatives precede rank k. Positives near the top therefore contribute high precision values to the average; positives buried deep contribute low ones.
**Hard — What is mAP@[.5:.95] in COCO?** Average Precision computed per class at ten IoU thresholds (0.50, 0.55, …, 0.95), averaged over both thresholds and classes. Averaging over IoU thresholds rewards *localisation* precision, not just detection — a box that only loosely overlaps the object scores at IoU 0.5 but fails at 0.9.

---

## 6.8 LIFT CURVE

### 1. Definition
A plot of **Lift** (y-axis) against the fraction of the population contacted (x-axis), where lift is how many times better the model is than random targeting.

### 2. Intuition
Lift is the metric that **sells models to marketing departments**, because it answers their exact question: *"if I only have budget to contact 10% of my list, how much better is your model than picking at random?"*

Lift of 4 at the top decile means: **the top 10% selected by the model contains 4 times as many positives as a random 10% would.**

It exists because marketing, collections, and sales teams operate under a fixed capacity constraint and think in deciles, not thresholds.

### 3. Formula
```
                   Precision in the selected top-k%       (TP_k / k)
Lift at top-k% = ------------------------------------ = ---------------
                        Overall prevalence               (P_total / N)
```
Equivalently:
```
                 (fraction of all positives captured in top k%)
Lift at k% = ------------------------------------------------------
                                    k%
```
- **k%** = the fraction of the population contacted, working down the ranked list
- **TP_k** = number of positives in that top k%
- **Prevalence** = P_total/N = the hit rate of random selection
- **Lift = 1** means no better than random. Lift is unbounded above; its maximum at the top is `1/prevalence`.

### 4. Manual example (6.0 data, N = 20, P = 8, prevalence = 0.40)

By deciles (2 samples per decile):

| Top k% | # contacted | Positives found | Cumulative positives | Response rate | Lift = rate/0.40 |
|---|---|---|---|---|---|
| 10% | 2 | 2 (ranks 1,2) | 2 | 2/2 = 1.000 | **2.50** |
| 20% | 4 | 1 (rank 4) | 3 | 3/4 = 0.750 | **1.88** |
| 30% | 6 | 1 (rank 5) | 4 | 4/6 = 0.667 | **1.67** |
| 40% | 8 | 1 (rank 7) | 5 | 5/8 = 0.625 | **1.56** |
| 50% | 10 | 1 (rank 9) | 6 | 6/10 = 0.600 | **1.50** |
| 60% | 12 | 1 (rank 11) | 7 | 7/12 = 0.583 | **1.46** |
| 70% | 14 | 1 (rank 14) | 8 | 8/14 = 0.571 | **1.43** |
| 80% | 16 | 0 | 8 | 8/16 = 0.500 | **1.25** |
| 90% | 18 | 0 | 8 | 8/18 = 0.444 | **1.11** |
| 100% | 20 | 0 | 8 | 8/20 = 0.400 | **1.00** |

```
Worked check, top decile:
  Positives in top 10% = 2
  Response rate        = 2/2 = 1.00
  Prevalence           = 8/20 = 0.40
  Lift                 = 1.00 / 0.40 = 2.50
```

**ASCII lift curve:**
```
 2.5 |*
     |
 2.0 |    *
  L  |        *
  i  |            *   *
  f1.5|                    *   *
  t  |                            *
 1.0 |- - - - - - - - - - - - - - - - - -*  <- random baseline (lift = 1)
     +--------------------------------------
     10%  20%  30%  40% 50% 60% 70% 80% 90% 100%
              Population contacted
```
**Every lift curve ends at exactly 1.0** at 100% — if you contact everyone, you get the base rate by definition. A monotonically decreasing lift curve confirms the ranking is working.

### 5. Python
Not in sklearn; compute it directly (this is a genuinely useful 8-line function to know by heart):

```python
import numpy as np, pandas as pd

def lift_table(y_true, y_score, n_bins=10):
    df = pd.DataFrame({'y': y_true, 's': y_score}).sort_values('s', ascending=False)
    df['bin'] = pd.qcut(df['s'].rank(method='first', ascending=False),
                        n_bins, labels=False) + 1
    prevalence = df['y'].mean()
    out = (df.groupby('bin')
             .agg(n=('y','size'), positives=('y','sum'))
             .assign(cum_n=lambda d: d['n'].cumsum(),
                     cum_pos=lambda d: d['positives'].cumsum()))
    out['response_rate'] = out['cum_pos'] / out['cum_n']
    out['lift']          = out['response_rate'] / prevalence
    out['cum_gain']      = out['cum_pos'] / df['y'].sum()
    return out

print(lift_table(y, scores))
```
Line-by-line:
- Sort descending by score — lift is entirely about the ranking.
- `pd.qcut` on the *rank* rather than the score avoids errors when many scores are tied.
- `response_rate` is cumulative precision at that depth.
- `lift` = response rate ÷ prevalence.
- `cum_gain` is the cumulative gain used in 6.9.

### 6. Interpretation

| Top-decile lift | Meaning |
|---|---|
| 1.0 | The model adds nothing over random targeting |
| 1.5 | Weak but real |
| 2.0 – 3.0 | Solid, typical for a decent marketing model |
| 3.0 – 5.0 | Strong |
| > 5.0 | Excellent (or leakage) |

**How marketing uses it:** "Lift 3.0 at decile 1 means we can hit the same number of responders by contacting one third as many people, cutting campaign cost by 67%." That sentence is why lift exists.

### 7. Good vs bad values
Depends heavily on prevalence: the theoretical maximum lift is `1/prevalence`. For a 40%-prevalence problem the ceiling is 2.5 — and our model achieves exactly 2.5 in decile 1, i.e. **perfect** performance in the top decile. For a 1%-prevalence problem the ceiling is 100, so lifts of 10–20 are common and good.

Always report lift alongside the ceiling `1/prevalence`, or as **normalised lift = lift × prevalence**, so it can be compared across campaigns.

### 8. Business use cases
- **Direct marketing / CRM:** the classic use. Which customers to mail, email, or call.
- **Debt collections:** which accounts the limited call-centre capacity should work.
- **Insurance cross-sell / up-sell targeting.**
- **Churn retention campaigns:** which customers get the retention offer.
- **Fundraising / donor targeting.**
- **Credit card pre-approval mailings.**
- **Telecom win-back campaigns.**
- **Sales lead prioritisation.**

### 9. Advantages
- **Speaks the language of business capacity constraints** — no thresholds, just "how many can we contact?"
- Directly convertible to ROI: `profit = (positives captured × value) − (contacts × cost)`.
- Immediately understandable by non-technical stakeholders.
- Naturally handles the "we can only act on the top X%" reality that thresholds obscure.

### 10. Limitations
- Depends on prevalence, so not comparable across campaigns without normalisation.
- Depends on the chosen bin count (deciles vs percentiles give different-looking curves).
- Only meaningful for ranked-selection use cases; irrelevant when you must classify every case.
- Ignores what happens in the tail — a great top decile can coexist with a poor overall model.
- Not in sklearn, so implementations vary and comparisons across teams are error-prone.
- Ignores calibration.

### 11. Common mistakes
1. Confusing **lift** (a ratio, starts high, ends at 1.0) with **cumulative gain** (a proportion, starts near 0, ends at 1.0).
2. Not stating the decile — "lift is 3" is meaningless without "at the top decile."
3. Comparing lift across datasets with different prevalence.
4. Reporting lift computed on the training set, where it is wildly inflated.
5. Using non-cumulative (per-decile) lift and cumulative lift interchangeably. Cumulative is standard; state which you used.

### 12. Interview questions
**Easy — What does lift 2.5 at decile 1 mean?** The top 10% of the model's ranking contains 2.5× as many positives as a random 10%.
**Easy — Where does every lift curve end?** At 1.0, at 100% of the population.
**Medium — Maximum possible lift?** `1/prevalence`, achieved when all positives are ranked at the very top.
**Medium — Lift vs precision?** Lift is precision at a given depth divided by prevalence. It is precision normalised by the base rate, which makes it comparable to "doing nothing."
**Hard — How do you turn a lift curve into a campaign decision?**
Compute expected profit at each depth: `profit(k) = cum_positives(k) × value_per_conversion − k × cost_per_contact`. Pick the depth that maximises profit. The optimal depth is where the **marginal** response rate of the next decile falls below `cost_per_contact / value_per_conversion` — i.e. where the incremental decile stops paying for itself. Note this uses *marginal*, not cumulative, response rate; getting that right is the mark of someone who has actually run campaigns.

---

## 6.9 CUMULATIVE GAIN CHART (Gains Chart)

### 1. Definition
A plot of the **cumulative percentage of all positives captured** (y-axis) against the **percentage of the population contacted** (x-axis).

### 2. Intuition
Lift asks "how many times better than random?" Gain asks the complementary question: **"what fraction of all the positives have I bagged by this depth?"**

It is the more directly actionable of the two, because it answers capacity planning questions in one glance: *"to catch 80% of the churners, how many customers must we contact?"* Read across from 0.80 on the y-axis, drop down to the x-axis, and that is your answer.

### 3. Formula
```
                     cumulative positives in top k%
Cumulative Gain(k) = --------------------------------
                        total positives in dataset
```
- **Numerator** = positives found so far, going down the ranked list
- **Denominator** = all positives in the dataset
- This is exactly **recall at depth k**. A gain chart is a plot of recall versus population depth.
- Relationship to lift: `Lift(k) = Gain(k) / k`.

### 4. Manual example (from the same table in 6.8)

| Top k% | Cumulative positives | Cumulative Gain = /8 | Random baseline | Perfect model |
|---|---|---|---|---|
| 10% | 2 | 0.250 | 0.10 | 0.25 |
| 20% | 3 | 0.375 | 0.20 | 0.50 |
| 30% | 4 | 0.500 | 0.30 | 0.75 |
| 40% | 5 | 0.625 | 0.40 | 1.00 |
| 50% | 6 | 0.750 | 0.50 | 1.00 |
| 60% | 7 | 0.875 | 0.60 | 1.00 |
| 70% | 8 | 1.000 | 0.70 | 1.00 |
| 80% | 8 | 1.000 | 0.80 | 1.00 |
| 100% | 8 | 1.000 | 1.00 | 1.00 |

**Three curves always appear on a gains chart:**
- **Random (baseline):** the 45° diagonal — contact 30% of people, get 30% of positives.
- **Model:** bows above the diagonal.
- **Perfect (wizard):** rises at slope `1/prevalence` until it hits 1.0 at `k = prevalence`, then flat. Here prevalence is 0.40, so the perfect model reaches 100% gain at 40% depth.

```
 1.0 |                        M M M M M M M    <- Model reaches 100% at 70%
     |            P P P P P P P P P P P P P    <- Perfect: 100% at 40%
 0.8 |                  M              .  .
  G  |          P     M           .  .
  a.6 |        P    M        .  .
  i  |      P    M     .  .
  n.4 |    P   M   .  .
     |  P  M .  .
 0.2 | P M.  .            <- Random diagonal
     |PM .
 0.0 +--------------------------------------
     0   10  20  30  40  50  60  70  80  90 100
              % of population contacted
```
**Reading the chart for a decision:** to capture 75% of all positives, this model needs 50% of the population. Random targeting would need 75%. That saving of 25 percentage points of contact volume is the value of the model.

The area between the model curve and the diagonal, normalised by the area between the perfect curve and the diagonal, is the **Gini coefficient** — which links this chart directly back to ROC-AUC via `Gini = 2·AUC − 1`.

### 5. Python
Use the `cum_gain` column from the `lift_table` function in 6.8, or:

```python
import numpy as np
order = np.argsort(-scores)                 # rank by score, descending
y_sorted = y[order]
cum_gain = np.cumsum(y_sorted) / y.sum()    # gain at each depth
depth    = np.arange(1, len(y)+1) / len(y)  # fraction of population

import matplotlib.pyplot as plt
plt.plot(depth, cum_gain, label='Model')
plt.plot([0,1], [0,1], 'k--', label='Random')
prev = y.mean()
plt.plot([0, prev, 1], [0, 1, 1], 'g:', label='Perfect')
plt.xlabel('% population contacted'); plt.ylabel('% positives captured')
plt.legend(); plt.show()
```
- `np.argsort(-scores)` sorts descending (note the minus sign).
- `np.cumsum(y_sorted)` counts positives found as you go deeper.
- The "perfect" line is a three-point polyline through `(0,0) → (prevalence,1) → (1,1)`.

### 6. Interpretation
The higher above the diagonal, the better. The key read-offs:
- **Gain at decile 1** — the headline number (0.25 here).
- **Depth needed for 80% gain** — the capacity planning number (~55% here).
- **Where the curve flattens** — beyond that depth, contacting more people adds almost nothing.

### 7. Good vs bad
Compare gain at decile 1 to prevalence-ceilinged perfection. At prevalence 0.40 the best possible decile-1 gain is 0.25 (10%/40%), and our model achieves exactly 0.25. For a 1%-prevalence problem, decile-1 gain of 0.60 (i.e. 60% of all positives in the top 10%) would be a strong model.

### 8. Business use cases
Same as lift — marketing, collections, retention, fundraising, sales prioritisation, fraud triage capacity planning — but gains charts are preferred when the conversation is about **coverage targets** ("we must reach 90% of at-risk customers") rather than **efficiency** ("how much better than random?").

Also standard in **credit scorecard documentation** and in **insurance underwriting** for setting referral cut-offs.

### 9. Advantages
- Answers capacity questions directly and visually.
- The three-curve format (random / model / perfect) makes the model's headroom obvious.
- Links cleanly to Gini and hence to ROC-AUC.
- Understood by executives without training.

### 10. Limitations
- Prevalence-dependent shape (the perfect curve moves), so cross-dataset comparison needs care.
- Ignores false-positive cost explicitly — that must be layered on via a profit calculation.
- Only relevant for ranked-selection problems.
- Not in sklearn.
- Ignores calibration.

### 11. Common mistakes
1. Confusing the gains chart with the lift chart (gain rises to 1.0; lift falls to 1.0).
2. Omitting the "perfect model" line, which hides how much headroom remains.
3. Computing it on training data.
4. Confusing **cumulative gain** with **DCG/NDCG** (Discounted Cumulative Gain), which is a different, relevance-graded ranking metric from information retrieval.

### 12. Interview questions
**Easy — What does a gains chart show?** The cumulative fraction of positives captured as you work down the ranked population.
**Easy — What is gain at 100% depth?** Always 1.0.
**Medium — Relationship between gain and recall?** Cumulative gain at depth k *is* recall at the threshold corresponding to depth k. A gains chart is recall plotted against population depth instead of against a score threshold.
**Medium — Relationship between the gains chart and Gini/AUC?** The Gini coefficient is the area between the model curve and the diagonal divided by the area between the perfect curve and the diagonal, and `Gini = 2·ROC-AUC − 1`. So the gains chart is a business-facing rendering of the same information as the ROC curve.
**Hard — When is a gains chart more useful than a PR curve?** When capacity is expressed as population volume rather than as a probability threshold — collections teams with 500 calls a day, marketing with a 50,000-piece mailing budget, fraud teams with 8 analysts. The x-axis of a gains chart *is* the capacity variable, so the operating point can be read off directly. A PR curve's x-axis (recall) does not tell you how many items you must process.

---

## 6.10 KS STATISTIC (Kolmogorov-Smirnov)

### 1. Definition
The maximum vertical distance between the cumulative distribution functions of the scores for the positive class and the negative class. Equivalently, `max(TPR − FPR)` over all thresholds.

### 2. Intuition
KS asks: **"at the single best possible cut-off, how far apart can I pull the two classes?"**

Imagine two histograms of predicted scores — one for the positives, one for the negatives. A good model pushes them apart. KS measures the **widest separation** between their cumulative curves, and the threshold at which that occurs is a natural candidate cut-off.

It is the dominant metric in **credit risk and banking**, where scorecard documentation and regulatory submissions quote KS as a matter of convention. If you interview for a bank, expect to be asked about KS.

### 3. Formula
```
KS = max over thresholds t of | F_pos(t) − F_neg(t) |
   = max over thresholds t of ( TPR(t) − FPR(t) )
```
- **F_pos(t)** = fraction of positives with score ≥ t = **TPR(t)**
- **F_neg(t)** = fraction of negatives with score ≥ t = **FPR(t)**
- Range **0 to 1** (often reported as 0–100). 0 = the two distributions are identical (no discrimination); 1 = perfectly separated.
- **KS is exactly Youden's J** evaluated at its maximum: `J = TPR + Specificity − 1 = TPR − FPR`. So `KS = max Youden's J`, and the threshold achieving it is the "closest to top-left corner" point on the ROC curve.

### 4. Manual example (6.0 data)

Take the TPR/FPR table from 6.2 and compute the gap:

| Threshold | TPR | FPR | TPR − FPR |
|---|---|---|---|
| 0.95 | 0.125 | 0.000 | 0.125 |
| 0.90 | 0.250 | 0.000 | 0.250 |
| 0.85 | 0.250 | 0.083 | 0.167 |
| 0.80 | 0.375 | 0.083 | 0.292 |
| 0.75 | 0.500 | 0.083 | 0.417 |
| 0.70 | 0.500 | 0.167 | 0.333 |
| 0.65 | 0.625 | 0.167 | 0.458 |
| 0.60 | 0.625 | 0.250 | 0.375 |
| 0.55 | 0.750 | 0.250 | 0.500 |
| 0.50 | 0.750 | 0.333 | 0.417 |
| **0.45** | **0.875** | **0.333** | **0.542** ← **maximum** |
| 0.40 | 0.875 | 0.417 | 0.458 |
| 0.35 | 0.875 | 0.500 | 0.375 |
| 0.30 | 1.000 | 0.500 | 0.500 |

```
KS = 0.542 (or 54.2), achieved at threshold 0.45
```
At that threshold: TP = 7, FP = 4, FN = 1, TN = 8 → TPR = 7/8 = 0.875, FPR = 4/12 = 0.333, gap = 0.542. This is the model's point of maximum class separation, and is a defensible default cut-off when FP and FN costs are equal.

### 5. Python

```python
import numpy as np
from sklearn.metrics import roc_curve
from scipy.stats import ks_2samp

fpr, tpr, thr = roc_curve(y, scores)
ks       = np.max(tpr - fpr)                 # 0.5416666666666667
ks_thr   = thr[np.argmax(tpr - fpr)]         # 0.45
print(f"KS = {ks:.4f} at threshold {ks_thr}")

# Equivalent, via the two score distributions directly
ks_2samp(scores[y == 1], scores[y == 0]).statistic     # 0.5417
```
- `roc_curve` gives you every threshold, so `max(tpr - fpr)` is the whole computation.
- `ks_2samp` from scipy computes the same statistic as a two-sample test and additionally returns a p-value, which lets you test whether the separation is statistically significant.
- The threshold at the KS point is often used as the initial production cut-off in credit scorecards.

### 6. Interpretation

Banking industry conventions (worth quoting verbatim in a finance interview):

| KS (0–100) | Verdict |
|---|---|
| < 20 | The model has no useful discriminative power |
| 20 – 30 | Weak but possibly usable |
| 30 – 40 | Acceptable / typical production scorecard |
| 40 – 50 | Good — our example is 54, strong |
| 50 – 60 | Very strong |
| 60 – 75 | Excellent, and worth double-checking |
| > 75 | Almost certainly leakage or an over-fit / in-sample estimate |

### 7. Good vs bad values
A retail credit scorecard with KS 35–45 is a solidly performing production model. KS above 70 on out-of-time data is a red flag: check for a feature that encodes the outcome.

Also check **where** the KS point sits. A KS of 45 occurring at the 5th percentile of the score distribution is very different operationally from one at the 50th percentile — the former means the separation is concentrated in a tiny high-risk tail.

### 8. Business use cases
- **Credit scoring and application scorecards** — the primary discrimination metric in banking, alongside Gini.
- **Regulatory model validation** (Basel, IFRS 9 model monitoring packs).
- **Collections scoring / recovery models.**
- **Insurance underwriting risk models.**
- **Fraud model cut-off selection** where FP and FN costs are roughly comparable.
- **Model monitoring:** KS is also used in a *different* sense to detect **data drift** — comparing the score distribution today against the training distribution. Same statistic, different application; be ready to distinguish these two uses, as interviewers deliberately conflate them.

### 9. Advantages
- Single number and a **recommended threshold** in one calculation — no other metric gives you both.
- Widely accepted and expected in banking, so it is a communication asset.
- Has a formal statistical test with a p-value (`ks_2samp`).
- Intuitive geometric meaning: the biggest gap between two cumulative curves.
- Insensitive to monotonic score transformations (like all ranking metrics).

### 10. Limitations
- **Only looks at one point.** It ignores the entire rest of the curve, so two models with the same KS can behave very differently everywhere else. AUC or PR-AUC summarise the whole curve.
- **Implicitly assumes FP and FN cost the same**, since it maximises `TPR − FPR` with equal weights. If costs are asymmetric, the KS threshold is not your optimal threshold.
- Uses FPR, so it inherits **ROC's imbalance blind spot** — high KS with dreadful precision is entirely possible on rare-event data.
- The KS threshold can land in an operationally useless region (e.g. flagging 50% of the population when you can only review 2%).
- Unstable on small samples.
- Ignores calibration.

### 11. Common mistakes
1. **Using the KS threshold as the production cut-off without a cost analysis.** It is optimal only under equal misclassification costs.
2. Reporting KS alone for an imbalanced fraud problem — pair it with precision or PR-AUC.
3. Confusing the KS *model discrimination* statistic with the KS *drift detection* test. Different data, same formula.
4. Computing KS on the training set (it will be inflated) rather than out-of-time validation data.
5. Reporting KS without saying at which score/percentile it occurs.
6. Forgetting the equivalence to Youden's J and treating them as independent evidence.

### 12. Interview questions
**Easy — What is the KS statistic?** The maximum vertical gap between the cumulative score distributions of positives and negatives; equivalently `max(TPR − FPR)`.
**Easy — Range and good values?** 0 to 1 (or 0–100). In credit scoring, 30–40 is acceptable, 40+ is good.
**Medium — Relationship between KS and Youden's J?** They are the same quantity: `J = TPR − FPR`, and KS is its maximum over thresholds. The KS threshold is the ROC point furthest above the diagonal.
**Medium — Relationship between KS and AUC?** Both are derived from the ROC curve, but KS is a single point (the maximum gap) while AUC integrates the entire curve. Two models can share a KS and differ in AUC, or vice versa. Report both.
**Hard — Why is KS the banking standard rather than AUC?**
Historical and practical. Scorecards were traditionally deployed with a single hard cut-off, so a metric that simultaneously reports separation *and* identifies that cut-off was operationally convenient. KS also has a familiar statistical test attached. Regulatory reporting conventions then locked it in. Modern practice reports KS, Gini/AUC, and increasingly PR-AUC together, because KS alone is one point on a curve.
**Hard — Your model's KS is 62 in development and 28 in out-of-time validation. Diagnose.**
Severe overfitting or population/temporal drift. Checks: (1) look for leakage — a feature capturing post-outcome information (e.g. collections activity) that was available in development but behaves differently later; (2) compare feature distributions between the two periods (a per-feature KS drift test); (3) check whether the development sample was in-time and the model was selected on it; (4) check whether the definition of the target changed; (5) check for a macro regime change (a credit model built pre-recession will degrade sharply). Rebuild with out-of-time validation baked into the selection process.

---

# PART 7 — Calibration Metrics

## 7.0 Why probability calibration matters

**Discrimination** = can the model put positives above negatives? (measured by AUC)
**Calibration** = when the model says 0.70, does the event happen 70% of the time? (measured by Brier / ECE / calibration curve)

These are **independent properties.** A model can have either without the other:

| | Well calibrated | Poorly calibrated |
|---|---|---|
| **Good discrimination** | Ideal | Common — needs post-hoc calibration |
| **Poor discrimination** | Useless but honest (predicts the base rate for everyone) | Worst case |

**Why anyone should care.** Calibration matters exactly when the *number* enters a downstream calculation, not just a ranking:

- **Insurance pricing:** premium = P(claim) × expected payout + expenses. If P is 2× too high, you price yourself out of the market; 2× too low and you go insolvent. Ranking is irrelevant here.
- **Expected loss provisioning (IFRS 9 / Basel):** `Expected Loss = PD × LGD × EAD`. The probability of default is multiplied by real money. Regulators audit calibration.
- **Ad bidding:** bid = P(click) × value per click. Miscalibration means systematically over- or under-paying on every impression, at billions of impressions per day.
- **Medical decision-making:** "your 10-year cardiovascular risk is 12%" drives whether a patient starts a statin. Guidelines are written around probability thresholds, so a miscalibrated model changes treatment decisions.
- **Triage and resource allocation:** if you need to allocate 100 ICU beds across probabilities, the numbers must be comparable and meaningful.
- **Any expected-value or cost-based threshold:** the cost-optimal threshold is `t* = C_FP / (C_FP + C_FN)`. That formula is only valid if the scores are true probabilities. **Miscalibration silently invalidates your threshold choice** — an underrated point that senior interviewers look for.
- **Human trust:** clinicians and analysts learn to distrust a model whose "90% confident" is wrong half the time, and then they stop using it.

**Which models are typically miscalibrated?**

| Model | Typical calibration | Direction |
|---|---|---|
| Logistic regression | Usually well calibrated | — (it optimises Log Loss directly) |
| Neural networks (modern, large) | Poorly calibrated | **Overconfident** — pushes probabilities to 0/1 |
| Naive Bayes | Poorly calibrated | Overconfident (independence assumption compounds evidence) |
| SVM (via Platt) | Poorly calibrated | Sigmoid-shaped distortion |
| Random Forest | Poorly calibrated | **Underconfident** — averaging votes pulls probabilities toward 0.5 |
| Gradient boosting (XGBoost/LightGBM) | Reasonable but often slightly overconfident | Depends on loss and depth |
| Any model after SMOTE/undersampling | **Badly** miscalibrated | Systematically too high — the training prior no longer matches reality |

That last row is important and frequently missed: **resampling changes the base rate the model learns, so it inflates all predicted probabilities.** If you resample for training, you must recalibrate (or apply a prior-correction offset) before using the probabilities.

**How to fix calibration:** post-hoc, using a held-out calibration set.
```python
from sklearn.calibration import CalibratedClassifierCV
cal = CalibratedClassifierCV(base_model, method='sigmoid', cv=5)   # Platt scaling
cal = CalibratedClassifierCV(base_model, method='isotonic', cv=5)  # isotonic regression
```
- **`'sigmoid'` (Platt scaling):** fits a 2-parameter logistic function to the scores. Low variance, works with a few hundred samples, but can only apply a sigmoid-shaped correction.
- **`'isotonic'`:** fits a free-form monotonic step function. More flexible, corrects any monotone distortion, but needs ~1,000+ calibration samples or it overfits.
- Both are **monotonic**, so they **change Log Loss and Brier but leave ROC-AUC and PR-AUC untouched.** This is the single cleanest demonstration that calibration and discrimination are separate.
- Temperature scaling (dividing logits by a single learned scalar T) is the deep-learning standard — it is Platt scaling with one parameter, preserves accuracy exactly, and is very effective for neural networks.

---

## 7.1 CALIBRATION CURVE (Reliability Diagram)

### 1. Definition
A plot of the **observed fraction of positives** (y-axis) against the **mean predicted probability** (x-axis), computed within bins of predicted probability.

### 2. Intuition
Group all predictions where the model said "about 20%." Now check reality: did about 20% of them turn out positive? Repeat for "about 30%," "about 40%," and so on. Plot the results.

**Perfect calibration is the 45° diagonal.** Everything else is a deviation you can name and interpret:
- **Curve below the diagonal** → the model predicts higher than reality → **overconfident / over-forecasting.**
- **Curve above the diagonal** → the model predicts lower than reality → **underconfident / under-forecasting.**
- **S-shape (sigmoid), steeper than the diagonal in the middle** → typical of Random Forests and bagged models: probabilities compressed toward 0.5, i.e. underconfident at the extremes.
- **Inverse-S (flatter than the diagonal in the middle, pinned near 0 and 1)** → typical of deep neural networks and Naive Bayes: overconfident, probabilities pushed to the extremes.

### 3. Formula (per bin)
```
For bin b:
   x_b = mean of predicted probabilities of samples in bin b
   y_b = (number of actual positives in bin b) / (number of samples in bin b)
```
- **Bins** are formed either by equal width (`strategy='uniform'`, e.g. [0,0.1), [0.1,0.2), …) or equal count (`strategy='quantile'`, each bin holds the same number of samples).
- Perfect calibration means `y_b = x_b` for every bin.
- **Quantile binning is usually the better default** on skewed score distributions, because uniform bins in the high-probability region may contain almost no samples, producing wildly noisy points.

### 4. Manual example

500 predictions, uniform bins of width 0.2:

| Bin | Samples | Mean predicted (x) | Actual positives | Observed rate (y) | Diagnosis |
|---|---|---|---|---|---|
| 0.0 – 0.2 | 200 | 0.10 | 30 | 30/200 = **0.15** | Under-predicting (y > x) |
| 0.2 – 0.4 | 120 | 0.30 | 42 | 42/120 = **0.35** | Slightly under |
| 0.4 – 0.6 | 80 | 0.50 | 40 | 40/80 = **0.50** | Perfect |
| 0.6 – 0.8 | 60 | 0.70 | 36 | 36/60 = **0.60** | Over-predicting (y < x) |
| 0.8 – 1.0 | 40 | 0.90 | 28 | 28/40 = **0.70** | Badly over-predicting |

```
ASCII reliability diagram
 1.0 |                                    /  <- perfect diagonal
     |                                 /
 0.8 |                              /
  O  |                           /
  b.6 |                        /            * (0.70 pred -> 0.60 actual)
  s  |                     /                        * (0.90 pred -> 0.70 actual)
  e.4 |                  /
  r  |               / *  (0.50, 0.50)  perfect
  v.2 |     *  /  (0.30, 0.35)
  e  |  * /      (0.10, 0.15)
  d0.0 +--------------------------------------
     0.0   0.2   0.4   0.6   0.8   1.0
              Mean predicted probability
```
**Reading it:** the curve sits above the diagonal at low probabilities and below it at high probabilities — a classic **overconfident-at-the-top** pattern. This model's high-confidence predictions cannot be trusted: when it says 90%, reality is 70%. If those probabilities feed a pricing formula, you are systematically overcharging your highest-risk segment by 29%.

### 5. Python

```python
from sklearn.calibration import calibration_curve, CalibrationDisplay
import matplotlib.pyplot as plt

prob_true, prob_pred = calibration_curve(y_true, y_proba, n_bins=10,
                                         strategy='quantile')
# prob_true = observed positive rate per bin (the y values)
# prob_pred = mean predicted probability per bin (the x values)

plt.plot(prob_pred, prob_true, marker='o', label='Model')
plt.plot([0,1], [0,1], 'k--', label='Perfectly calibrated')
plt.xlabel('Mean predicted probability'); plt.ylabel('Observed fraction of positives')
plt.legend(); plt.show()

# Also plot a histogram of predicted probabilities underneath — ALWAYS do this,
# so the reader can see which bins have enough data to be meaningful.
plt.hist(y_proba, bins=20)

# One-liner comparing several models
# CalibrationDisplay.from_estimator(model, X_test, y_test, n_bins=10)
```
Line-by-line:
- `calibration_curve` returns `(prob_true, prob_pred)` **in that order** — `prob_true` is the y-axis. Swapping them is a common plotting bug.
- `n_bins=10` is conventional; fewer bins = smoother but coarser, more bins = noisier.
- `strategy='quantile'` gives equal-count bins → more stable points. `'uniform'` gives equal-width bins → easier to interpret but noisy where data is sparse.
- **Always plot the score histogram alongside.** A calibration point built from 3 samples is meaningless, and without the histogram the reader cannot tell.

### 6. Interpretation
- **On the diagonal** → calibrated, probabilities usable directly in formulas.
- **Below** → overconfident; apply temperature scaling or Platt.
- **Above** → underconfident; isotonic regression usually fixes it.
- **Wiggly / erratic** → too few samples per bin, or genuinely inconsistent calibration across the score range; reduce `n_bins` or gather more data.

### 7. Good vs bad
Judged qualitatively, plus numerically via ECE (7.2) and Brier (7.3). A production model whose calibration curve deviates from the diagonal by more than ~0.05 in bins containing meaningful volume should be recalibrated.

### 8. Business use cases
- **Insurance and actuarial pricing** — calibration by risk band is a regulatory expectation.
- **Credit risk PD models** — a "PD calibration" section is mandatory in Basel model documentation.
- **Clinical risk calculators** — published alongside the ROC curve in medical journals; a mandatory element of the TRIPOD reporting standard.
- **Weather forecasting** — reliability diagrams originated here.
- **Ad tech CTR models** — monitored continuously in production.
- **LLM / classifier confidence reporting** — deciding when to escalate to a human based on model confidence requires that confidence to mean something.
- **Model monitoring** — a drifting calibration curve is an early signal that the population has shifted even before AUC degrades.

### 9. Advantages
- **Diagnostic, not just a score.** It tells you *where* and *in which direction* the model is wrong, which a single number cannot.
- Directly actionable: the shape tells you which calibration method to apply.
- Intuitive to explain: "when we say 70%, it happens 60% of the time."
- Works for any model that produces scores.

### 10. Limitations
- **Depends on the binning choice** — different `n_bins` or strategies can make the same model look better or worse. Not a robust basis for comparison without stating the binning.
- Noisy in sparsely-populated regions, which are often the high-probability regions you care most about.
- **Visual, not a single number** → cannot be used in `GridSearchCV`. Pair with ECE or Brier.
- **Says nothing about discrimination.** A model that predicts the base rate for every sample is perfectly calibrated and completely useless. **Always report AUC alongside.** This is the essential caveat.
- Requires a decent amount of held-out data.

### 11. Common mistakes
1. **Confusing calibration with accuracy.** A perfectly calibrated model can have AUC 0.5.
2. Plotting `prob_true` on the x-axis.
3. Not plotting the score histogram, so nobody can tell which bins are trustworthy.
4. Calibrating on the training set (calibration must use held-out data, or `CalibratedClassifierCV`'s internal CV).
5. Reporting calibration after SMOTE without prior-correction, and being confused that everything is over-predicted.
6. Using uniform bins on a heavily skewed score distribution and interpreting the empty-bin noise as miscalibration.

### 12. Interview questions
**Easy — What does a calibration curve show?** Predicted probability versus observed frequency, binned.
**Easy — What does perfect calibration look like?** The 45° diagonal.
**Medium — Random Forest vs Neural Network calibration shapes?** Random Forests are typically **underconfident** (S-shaped, probabilities compressed toward 0.5, because averaging many votes rarely produces unanimity). Modern deep networks are typically **overconfident** (probabilities pushed to 0 and 1, because they are trained to near-zero loss on the training set and cross-entropy keeps pushing logits apart).
**Medium — Can a model with AUC 0.5 be perfectly calibrated?** Yes — predict the base rate for every sample. Calibration is perfect, discrimination is nil. This is why calibration must never be reported alone.
**Hard — Does calibration change ROC-AUC?** No. Platt scaling and isotonic regression are monotonic transformations, and ROC-AUC depends only on the ordering of scores. Calibration changes Log Loss, Brier, ECE, and the meaning of any fixed threshold, but not AUC or PR-AUC. Corollary: you can always calibrate a good-ranking model for free, so **poor calibration is never a reason to reject a model with good AUC** — it is a reason to add a calibration step.
**Hard — Why do neural networks become overconfident, and what fixes it?**
Cross-entropy has no stationary point until the predicted probability reaches exactly 1 for the true class, so with enough capacity the optimiser keeps inflating logit magnitudes long after the classification is correct. Combined with modern regularisation practices (BatchNorm, large models trained past zero training error), this yields confident but unreliable probabilities. Fixes: **temperature scaling** (divide logits by a scalar T fitted on validation data — cheap, preserves accuracy exactly, the standard method), **label smoothing** during training, **mixup**, **deep ensembles**, and **focal loss**. Temperature scaling is usually the first thing to try.

---

## 7.2 CALIBRATION ERROR (ECE / MCE)

### 1. Definition
- **ECE (Expected Calibration Error):** the weighted average absolute gap between predicted probability and observed frequency across bins.
- **MCE (Maximum Calibration Error):** the largest such gap in any bin.

### 2. Intuition
ECE turns the calibration curve into one number: **"on average, by how many percentage points is the model's stated confidence wrong?"** ECE = 0.07 reads as "confidence claims are off by about 7 percentage points on average."

MCE answers the worst-case question: **"in the worst bin, how wrong is the model?"** Use MCE for safety-critical systems where the worst case is what matters.

### 3. Formula
```
       B   |B_b|
ECE = Σ   ------- × | acc(B_b) − conf(B_b) |
      b=1    n

MCE = max over b of  | acc(B_b) − conf(B_b) |
```
- **B** = number of bins; **b** = bin index
- **|B_b|** = number of samples in bin b; **n** = total samples
- **|B_b|/n** = the weight of that bin — this is what makes it *Expected* calibration error; big bins matter more
- **conf(B_b)** = mean predicted probability in bin b (what the model claimed)
- **acc(B_b)** = observed fraction of positives in bin b (what actually happened)
- Range 0 to 1; **lower is better**, 0 = perfectly calibrated.

**Adaptive/quantile ECE** uses equal-count bins instead of equal-width bins and is generally preferred, because equal-width binning gives near-empty high-confidence bins enormous influence on MCE and almost none on ECE.

### 4. Manual example (using the 7.1 table, n = 500)

| Bin | \|B_b\| | Weight | conf (x) | acc (y) | \|acc − conf\| | Weight × gap |
|---|---|---|---|---|---|---|
| 0.0–0.2 | 200 | 0.40 | 0.10 | 0.15 | 0.05 | 0.0200 |
| 0.2–0.4 | 120 | 0.24 | 0.30 | 0.35 | 0.05 | 0.0120 |
| 0.4–0.6 | 80 | 0.16 | 0.50 | 0.50 | 0.00 | 0.0000 |
| 0.6–0.8 | 60 | 0.12 | 0.70 | 0.60 | 0.10 | 0.0120 |
| 0.8–1.0 | 40 | 0.08 | 0.90 | 0.70 | **0.20** | 0.0160 |
| | 500 | 1.00 | | | | **Σ = 0.0600** |

```
ECE = 0.0200 + 0.0120 + 0.0000 + 0.0120 + 0.0160 = 0.0600
MCE = max(0.05, 0.05, 0.00, 0.10, 0.20) = 0.20   (in the 0.8-1.0 bin)
```
**ECE = 0.060, MCE = 0.200.**

The contrast is instructive. ECE says "on average the model is off by 6 percentage points" — sounds acceptable. MCE says "in the highest-confidence bin it is off by 20 points" — alarming. The worst bin holds only 8% of the data, so ECE dilutes it. **If your business acts primarily on high-confidence predictions, ECE is the wrong summary and MCE (or ECE restricted to the top bins) is the right one.** That is a strong point to raise in an interview.

### 5. Python
Not in sklearn; implement it (a standard interview coding exercise):

```python
import numpy as np

def calibration_errors(y_true, y_prob, n_bins=10, strategy='uniform'):
    y_true = np.asarray(y_true); y_prob = np.asarray(y_prob)
    if strategy == 'quantile':
        edges = np.quantile(y_prob, np.linspace(0, 1, n_bins + 1))
        edges[0], edges[-1] = 0.0, 1.0
    else:
        edges = np.linspace(0.0, 1.0, n_bins + 1)

    ece, mce, n = 0.0, 0.0, len(y_true)
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (y_prob > lo) & (y_prob <= hi)
        if mask.sum() == 0:
            continue
        conf = y_prob[mask].mean()          # what the model claimed
        acc  = y_true[mask].mean()          # what actually happened
        gap  = abs(acc - conf)
        ece += (mask.sum() / n) * gap       # weighted by bin size
        mce  = max(mce, gap)                # worst case
    return ece, mce

# ece, mce = calibration_errors(y_test, model.predict_proba(X_test)[:, 1])
```
Line-by-line:
- `edges` defines the bin boundaries; quantile strategy makes bins equal-count.
- `conf` is the mean *predicted* probability in the bin; `acc` is the *actual* positive rate.
- ECE accumulates the size-weighted gap; MCE tracks the maximum.
- Empty bins are skipped, which is why uniform binning can silently ignore a whole region.

### 6. Interpretation

| ECE | Meaning |
|---|---|
| < 0.01 | Excellently calibrated |
| 0.01 – 0.03 | Well calibrated; usable in formulas |
| 0.03 – 0.07 | Moderate miscalibration; recalibrate before using the numbers |
| 0.07 – 0.15 | Poor; probabilities should not be used quantitatively |
| > 0.15 | Severe; typical of an uncalibrated deep network or a post-SMOTE model |

### 7. Good vs bad values
Target ECE < 0.02–0.03 for any system where the probability enters a calculation. For pure ranking systems, ECE is irrelevant.

### 8. Business use cases
- **Deep learning research** — the standard metric in the calibration literature; every temperature-scaling paper reports ECE.
- **Medical AI regulatory submissions** — increasingly expected alongside AUC.
- **Autonomous systems** — MCE matters because worst-case overconfidence is a safety hazard.
- **Credit risk PD calibration testing** (alongside the Hosmer-Lemeshow and binomial tests).
- **LLM confidence estimation / selective prediction** — deciding when to abstain or escalate.
- **Insurance and pricing model validation.**
- **Model monitoring dashboards** — ECE tracked over time detects population drift.

### 9. Advantages
- Reduces the calibration curve to a single, optimisable number.
- Percentage-point units are directly interpretable.
- MCE captures the worst case, which safety cases require.
- Straightforward to implement and monitor.

### 10. Limitations
- **Binning-dependent** — the reported value changes with `n_bins` and strategy, so ECE is not comparable across papers unless the binning is stated. A well-known criticism in the literature.
- **Biased estimator:** ECE systematically underestimates true calibration error with few bins and few samples.
- **Can hide compensating errors:** a bin that is +0.1 in one half and −0.1 in the other averages to 0 and looks perfect.
- **Says nothing about discrimination.** ECE = 0 for the constant base-rate predictor.
- Not a proper scoring rule (unlike Brier or Log Loss), so it can in principle be gamed.
- MCE is dominated by small bins and is therefore high-variance.

### 11. Common mistakes
1. Comparing ECE values computed with different bin counts.
2. Reporting ECE without AUC.
3. Using uniform bins with a skewed score distribution, so MCE is driven by a 4-sample bin.
4. Computing ECE on the same data used to fit the calibrator → optimistically biased.
5. Treating ECE as if it were a proper scoring rule.

### 12. Interview questions
**Easy — What is ECE?** The bin-size-weighted mean absolute gap between predicted confidence and observed accuracy.
**Easy — ECE vs MCE?** ECE is the weighted average gap; MCE is the worst single-bin gap.
**Medium — What are the weaknesses of ECE?** Binning dependence, bias with few samples, insensitivity to compensating errors within a bin, and total blindness to discrimination.
**Medium — Why report both ECE and AUC?** They measure orthogonal properties. ECE says whether the numbers mean what they claim; AUC says whether the ordering is informative. You need both to know a model is usable.
**Hard — Why is Brier score sometimes preferred over ECE?**
Brier is a **proper scoring rule** — it is minimised only by honest probabilities and cannot be gamed — and it requires no binning, so it has no arbitrary hyperparameter and no binning-induced bias. Via the Murphy decomposition it also separates into calibration and refinement/resolution components, so you get both properties from one number. ECE's advantages are interpretability in percentage points and the fact that it isolates calibration cleanly, which makes it a better *diagnostic* even if Brier is the better *score*.

---

## 7.3 BRIER SCORE

### 1. Definition
The mean squared difference between the predicted probability and the actual 0/1 outcome. Mean squared error, applied to probabilities.

### 2. Intuition
Brier asks: **"how far off were your probabilities, on average, squared?"** It is the gentler sibling of Log Loss.

The crucial behavioural difference: **Brier is bounded, Log Loss is not.** Predict 0.0 when the truth is 1 and Brier charges you exactly 1.0 — the maximum possible penalty. Log Loss charges you infinity. So Brier is far more robust to a single catastrophic prediction, and its values are always in [0,1], which makes it easier to report and compare.

Brier is a **proper scoring rule** (like Log Loss) and it measures **calibration and discrimination together**. It was invented in 1950 for weather forecast verification.

### 3. Formula

**Binary:**
```
              1    N
Brier = ---  ×  Σ  ( pᵢ − yᵢ )²
              N   i=1
```
- **N** = number of samples; **i** = sample index
- **pᵢ** = predicted probability of the positive class, in [0,1]
- **yᵢ** = actual outcome, exactly 0 or 1
- **(pᵢ − yᵢ)²** = squared error for that sample; ranges from 0 (perfect) to 1 (maximally wrong)
- Range **[0, 1]**; **lower is better**; 0 = perfect.

**Multi-class (Brier score, original multi-category form):**
```
                 1    N    K
Brier_multi = --- ×  Σ    Σ  ( p_{i,k} − y_{i,k} )²
                 N   i=1  k=1
```
- Range [0, 2] in this form, since a maximally wrong prediction contributes 1 to the true class term and 1 to the predicted class term.

**Murphy decomposition** (the reason Brier is theoretically attractive):
```
Brier = Reliability (calibration error)  −  Resolution (discrimination)  +  Uncertainty (irreducible)
```
- **Reliability** — how far the observed frequencies deviate from the predicted probabilities. Lower is better. This is calibration.
- **Resolution** — how much the model's predictions vary from the base rate in a way that tracks reality. **Higher is better** (it is subtracted). This is discrimination.
- **Uncertainty** = `prevalence × (1 − prevalence)` — the inherent variance of the outcome, which no model can reduce. It is also exactly the Brier score of the base-rate predictor.

**Brier Skill Score (BSS)** normalises against the base-rate baseline:
```
BSS = 1 − (Brier_model / Brier_baseline),   where Brier_baseline = prevalence × (1 − prevalence)
```
BSS = 1 is perfect, 0 = no better than predicting the base rate, negative = worse than the base rate. **Report BSS, not raw Brier, when you want the number to be interpretable.**

### 4. Manual example

Same four samples as the Log Loss example:

| i | True yᵢ | Predicted pᵢ | pᵢ − yᵢ | (pᵢ − yᵢ)² |
|---|---|---|---|---|
| 1 | 1 | 0.9 | −0.1 | 0.01 |
| 2 | 0 | 0.2 | +0.2 | 0.04 |
| 3 | 1 | 0.6 | −0.4 | 0.16 |
| 4 | 0 | 0.7 | +0.7 | **0.49** |

```
Step 1 — sample 1: (0.9 − 1)² = (−0.1)² = 0.01
Step 2 — sample 2: (0.2 − 0)² = ( 0.2)² = 0.04
Step 3 — sample 3: (0.6 − 1)² = (−0.4)² = 0.16
Step 4 — sample 4: (0.7 − 0)² = ( 0.7)² = 0.49
Step 5 — sum  = 0.01 + 0.04 + 0.16 + 0.49 = 0.70
Step 6 — mean = 0.70 / 4 = 0.175
```
**Brier Score = 0.175.**

Compare with Log Loss on the identical data = **0.5108**. Look at sample 4, the confidently-wrong one:
- Brier charges it **0.49** — 70% of the total, but bounded.
- Log Loss charges it **1.204** — 59% of the total, and it would head to infinity as the prediction approached 0.
That is the robustness difference in one line.

**Baseline for this data:** prevalence = 2/4 = 0.5, so `Brier_baseline = 0.5 × 0.5 = 0.25`.
```
BSS = 1 − (0.175 / 0.25) = 1 − 0.70 = 0.30
```
So the model is 30% better than predicting the base rate — a modest but real improvement.

### 5. Python

```python
from sklearn.metrics import brier_score_loss
import numpy as np

y_true  = np.array([1, 0, 1, 0])
y_proba = np.array([0.9, 0.2, 0.6, 0.7])
brier_score_loss(y_true, y_proba)                 # 0.175

# Brier Skill Score
prev = y_true.mean()
baseline = prev * (1 - prev)                      # 0.25
bss = 1 - brier_score_loss(y_true, y_proba)/baseline    # 0.30

# In GridSearchCV (note: sklearn scorers are "greater is better", hence the negative)
# GridSearchCV(model, params, scoring='neg_brier_score')
```
Line-by-line:
- `brier_score_loss(y_true, y_prob)` — pass **probabilities**, and for binary pass the probability of the positive class.
- `pos_label=` is needed if labels are not 0/1.
- `scoring='neg_brier_score'` — sklearn negates all loss metrics so that higher is always better in model selection. Forgetting the `neg_` prefix and getting a "not a valid scorer" error is a rite of passage.

### 6. Interpretation

Interpret against the baseline `prevalence × (1 − prevalence)`.

| Prevalence | Baseline Brier | "Good" Brier |
|---|---|---|
| 0.50 | 0.250 | < 0.15 |
| 0.20 | 0.160 | < 0.10 |
| 0.10 | 0.090 | < 0.06 |
| 0.01 | 0.0099 | < 0.007 |

| Raw value (balanced data) | Meaning |
|---|---|
| 0.00 | Perfect |
| 0.05 | Excellent |
| 0.10 | Good |
| 0.175 | Moderate — our example |
| 0.25 | **No skill (equals the base-rate predictor on balanced data)** |
| > 0.25 | Worse than predicting the base rate |
| 1.00 | Maximally, confidently wrong on every sample |

**Important trap:** on a 1%-prevalence problem the baseline Brier is 0.0099, so a Brier of 0.009 sounds tiny and impressive but represents almost no skill. **Never report Brier on imbalanced data without the baseline or the BSS.**

### 7. Good vs bad values
Use BSS: Poor < 0.05, Average 0.05–0.15, Good 0.15–0.35, Excellent > 0.35. BSS is comparable across prevalences in a way raw Brier is not.

### 8. Business use cases
- **Weather forecasting** — the origin and still the standard verification metric.
- **Sports and election forecasting** — FiveThirtyEight-style probabilistic forecasts are scored on Brier.
- **Prediction markets and forecasting tournaments** (Good Judgment Project, Metaculus) — Brier is the standard scoring rule for human forecasters too.
- **Clinical prediction models** — reported alongside AUC and calibration curves under the TRIPOD guidelines.
- **Insurance and actuarial model validation.**
- **Credit risk PD model validation.**
- **Any system that needs robust probability quality** where a single extreme prediction should not dominate the metric — Brier's boundedness makes it safer than Log Loss for monitoring dashboards.

### 9. Advantages
- **Bounded [0,1]** → robust to outliers, no infinities, safe for automated monitoring.
- **Proper scoring rule** → cannot be gamed by exaggerating confidence.
- **Measures calibration and discrimination together**, and the Murphy decomposition lets you separate them.
- Intuitive as "mean squared error on probabilities."
- Defined at p = 0 and p = 1, so no clipping needed (unlike Log Loss).
- Available in sklearn with a proper scorer string.

### 10. Limitations
- **Baseline depends on prevalence** → raw values are not comparable across datasets; use BSS.
- **Less sensitive than Log Loss to confidently-wrong predictions.** If confident errors are catastrophic in your domain, Log Loss's harsher penalty is the feature you want, not a bug.
- Squared error penalises small deviations more gently than Log Loss, so it provides a weaker training gradient — which is why models are trained on cross-entropy, not Brier.
- On very imbalanced data the absolute values become tiny and hard to reason about.
- Ignores threshold-based decision quality.
- The multi-class version has a different range (0–2), causing confusion.

### 11. Common mistakes
1. **Reporting raw Brier on imbalanced data without the baseline.** 0.009 looks superb and may mean nothing.
2. Passing hard labels instead of probabilities.
3. Forgetting the `neg_` prefix in `scoring='neg_brier_score'`.
4. Comparing Brier scores across datasets with different prevalence.
5. Assuming a low Brier implies good calibration specifically — it implies good *combined* calibration and discrimination; decompose it or plot the calibration curve to separate them.
6. Confusing the binary form (range 0–1) with the multi-category form (range 0–2).

### 12. Interview questions

**Easy — What is the Brier score?** The mean squared error between predicted probabilities and 0/1 outcomes.
**Easy — Range?** 0 to 1 for binary, lower is better.
**Easy — Baseline value?** `prevalence × (1 − prevalence)`; 0.25 for balanced data.

**Medium — Brier vs Log Loss?**

| | Brier | Log Loss |
|---|---|---|
| Formula | mean (p − y)² | mean −ln(p_true) |
| Range | [0, 1] | [0, ∞) |
| Penalty for p=0 when y=1 | 1.0 (bounded) | ∞ |
| Outlier robustness | High | Low |
| Proper scoring rule | Yes | Yes |
| Used as a training loss | Rarely | Almost always |
| Interpretability | MSE on probabilities | `exp(−LL)` = geometric mean prob of truth |
| Best when | Reporting, monitoring, robustness needed | Training; confident errors are catastrophic |

**Medium — Both Brier and Log Loss are proper. Why train on Log Loss?** Its gradient with respect to the logits is `(p − y)`, which stays large when the model is confidently wrong, giving strong learning signal exactly where it is needed. Brier's gradient includes an extra `σ'(z)` factor that vanishes for confident predictions, so learning stalls on the hardest examples. Log Loss is also the exact negative log-likelihood of the Bernoulli model, making its minimisation maximum-likelihood estimation.

**Hard — Explain the Murphy decomposition and why it matters.**
`Brier = Reliability − Resolution + Uncertainty`. Reliability is the calibration error (lower better). Resolution measures how far the model's predictions deviate from the base rate in a way that matches reality (higher better, and it is subtracted). Uncertainty is `p(1−p)`, the irreducible variance of the outcome. It matters because it shows that a single proper score can be *decomposed into the two properties you actually care about* — so a model can improve its Brier either by becoming better calibrated (post-hoc, cheap) or by becoming more discriminating (needs better features/data). Diagnosing which one is deficient tells you where to spend effort.

**Hard — Your Brier is 0.008 on a 1% fraud problem. Is the model good?**
Compute the baseline: `0.01 × 0.99 = 0.0099`. So `BSS = 1 − 0.008/0.0099 = 0.19` — a real but modest improvement over predicting the base rate for everyone. The raw 0.008 is almost entirely a reflection of the low prevalence, not of model skill. Report BSS, and add PR-AUC to assess whether the ranking is useful, since Brier alone will not reveal that.

---

# PART 8 — Multi-class Metrics: Macro, Micro, Weighted

## 8.0 The problem

Precision and recall are defined for **one positive class**. With 3, 10, or 1,000 classes, you get a precision and a recall **per class**. To produce a single headline number you must **average** them — and there are three different ways to average, which give different answers and encode different priorities.

**Choosing the averaging method is a value judgement, not a technical detail.** It is one of the most common multi-class interview questions.

## 8.1 THE MULTI-CLASS RUNNING EXAMPLE

Three classes, 100 samples. Rows = actual, columns = predicted.

```
                         P R E D I C T E D
                    +--------+--------+--------+  Actual
                    |   A    |   B    |   C    |  total
        +-----------+--------+--------+--------+--------
        |     A     |   40   |    5   |    5   |   50
 ACTUAL |     B     |    5   |   25   |    0   |   30
        |     C     |    5   |    5   |   10   |   20
        +-----------+--------+--------+--------+--------
         Pred total |   50   |   35   |   15   |  100
```

**Per-class cells** (one-vs-rest: for class A, "positive" = A, "negative" = B or C):

| Class | TP | FP | FN | Support (actual count) |
|---|---|---|---|---|
| A | 40 | 5 + 5 = 10 | 5 + 5 = 10 | 50 |
| B | 25 | 5 + 5 = 10 | 5 + 0 = 5 | 30 |
| C | 10 | 5 + 0 = 5 | 5 + 5 = 10 | 20 |
| **Total** | **75** | **25** | **25** | **100** |

- **TP** for a class = its diagonal cell.
- **FP** for a class = the rest of its **column** (other classes wrongly predicted as this class).
- **FN** for a class = the rest of its **row** (this class wrongly predicted as something else).
- Note `Σ FP = Σ FN = 25` always, in single-label multi-class: every error is simultaneously an FN for the true class and an FP for the predicted class. This identity is the reason micro-precision = micro-recall = accuracy.

**Per-class metrics:**

```
Class A: Precision = 40/(40+10) = 40/50 = 0.8000
         Recall    = 40/(40+10) = 40/50 = 0.8000
         F1        = 2(0.8)(0.8)/(0.8+0.8) = 0.8000

Class B: Precision = 25/(25+10) = 25/35 = 0.7143
         Recall    = 25/(25+ 5) = 25/30 = 0.8333
         F1        = 2(0.7143)(0.8333)/(0.7143+0.8333) = 1.1905/1.5476 = 0.7692

Class C: Precision = 10/(10+ 5) = 10/15 = 0.6667
         Recall    = 10/(10+10) = 10/20 = 0.5000
         F1        = 2(0.6667)(0.5)/(0.6667+0.5) = 0.6667/1.1667 = 0.5714

Accuracy = (40 + 25 + 10)/100 = 75/100 = 0.7500
```

Class C — the smallest class, 20 samples — performs worst (F1 = 0.571). **Whether your headline number reveals or hides that fact depends entirely on which averaging you choose.** That is the whole lesson.

---

## 8.2 MACRO AVERAGE

### 1. Definition
Compute the metric for each class independently, then take the **plain unweighted mean**.

### 2. Intuition
**Every class gets one vote, regardless of size.** A class with 3 samples counts exactly as much as a class with 3,000.

It exists because in many problems the rare classes are the important ones — rare disease subtypes, rare defect categories, rare fraud typologies. Macro averaging refuses to let the model coast by nailing the common classes.

### 3. Formula
```
                1    K
Macro-P = --- ×  Σ  Precisionₖ
                K   k=1

                1    K
Macro-R = --- ×  Σ  Recallₖ
                K   k=1

                 1    K
Macro-F1 = --- ×  Σ  F1ₖ         <-- mean of the per-class F1s
                 K   k=1
```
- **K** = number of classes
- **k** = class index
- No weighting by support — that is the entire point.
- **Note:** Macro-F1 is the **mean of the F1 scores**, NOT the F1 of the macro-averaged precision and recall. These differ, and confusing them is a classic error. (The latter is sometimes called F1-of-macro-averages or "macro-F1 variant 2" and appears in some older papers.)

### 4. Manual example

```
Macro-Precision = (0.8000 + 0.7143 + 0.6667) / 3 = 2.1810 / 3 = 0.7270
Macro-Recall    = (0.8000 + 0.8333 + 0.5000) / 3 = 2.1333 / 3 = 0.7111
Macro-F1        = (0.8000 + 0.7692 + 0.5714) / 3 = 2.1406 / 3 = 0.7135
```
Compare: **Accuracy = 0.7500, Macro-F1 = 0.7135.** Macro is lower because it gives the poorly-performing small class C a full one-third vote.

Cross-check on the confusion of the two macro-F1 definitions: F1 computed from macro-P and macro-R would be `2(0.7270)(0.7111)/(0.7270+0.7111) = 1.0338/1.4381 = 0.7189` — different from 0.7135. sklearn reports **0.7135** (the mean of per-class F1s).

### 5. Python

```python
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report

precision_score(y_true, y_pred, average='macro')   # 0.7270
recall_score(y_true, y_pred,    average='macro')   # 0.7111
f1_score(y_true, y_pred,        average='macro')   # 0.7135

print(classification_report(y_true, y_pred, target_names=['A','B','C'], digits=4))
```
Output:
```
              precision    recall  f1-score   support

           A     0.8000    0.8000    0.8000        50
           B     0.7143    0.8333    0.7692        30
           C     0.6667    0.5000    0.5714        20

    accuracy                         0.7500       100
   macro avg     0.7270    0.7111    0.7136       100
weighted avg     0.7476    0.7500    0.7451       100
```
- `average='macro'` — unweighted mean across classes.
- `average=None` returns the per-class array, which is what you should always inspect first.
- `labels=[...]` restricts which classes are included — useful for excluding a dominant "other"/background class from the macro average, a common and legitimate technique.
- `zero_division=0` prevents warnings when a rare class is never predicted.

### 6. Interpretation
Macro-F1 answers: **"how well does the model do on a typical CLASS?"**

A large gap between accuracy and macro-F1 is the signal to watch:
- `accuracy ≫ macro-F1` → the model is good on frequent classes and bad on rare ones. **Very common with imbalanced multi-class data.** Here: 0.75 vs 0.71, a mild version.
- `accuracy ≈ macro-F1` → performance is even across classes.
- `macro-F1 > accuracy` → unusual; typically means the model does relatively better on rare classes than frequent ones.

### 7. Good vs bad values
Compare to accuracy and to `1/K` (the random-guess baseline for macro-recall). With 3 classes, macro-recall of 0.33 is chance. Macro-F1 above ~0.70 with balanced-ish per-class values is generally solid; the key check is the *spread* of per-class F1s, not just the mean.

### 8. Business use cases
- **Rare disease subtype classification** — every subtype matters clinically regardless of frequency.
- **Manufacturing defect-type classification** — a rare but catastrophic defect type must not be ignored.
- **Fairness / bias auditing** — macro averaging across demographic groups ensures small groups are not sacrificed. This is one of the most important modern uses.
- **NLP: named entity recognition, intent classification** — macro-F1 is the standard reported metric because entity/intent frequencies are highly skewed.
- **Kaggle multi-class competitions** with imbalanced classes.
- **Species / plant / animal classification** with long-tailed distributions.
- **Sentiment analysis with a rare "neutral" class.**
- **Content moderation across many policy categories**, where rare categories (e.g. terrorism) are the highest-stakes.

### 9. Advantages
- **Gives rare classes equal weight** — prevents the model from ignoring them.
- Exposes uneven performance that accuracy hides.
- The right default for imbalanced multi-class problems.
- Simple to explain: "average performance per class."

### 10. Limitations
- **High variance when classes are tiny.** A class with 4 test samples contributes a very noisy F1 with a full 1/K vote, so macro-F1 becomes unstable. With 200 classes where 50 have fewer than 10 samples, macro-F1 is dominated by noise.
- May over-weight classes that genuinely do not matter (a junk "unknown" bucket).
- Can be misleading if some classes are inherently much harder — a low macro score might reflect problem difficulty rather than model deficiency.
- Does not reflect the overall error volume the business experiences.
- Hides the distribution: report the per-class table, not just the mean.

### 11. Common mistakes
1. **Confusing macro-F1 (mean of F1s) with F1 of the macro-averaged P and R.** Different numbers; sklearn does the former.
2. Using macro on a problem with a few near-empty classes and treating the result as reliable.
3. Reporting macro-F1 without the per-class breakdown — you lose all the diagnostic value.
4. Assuming macro-F1 is always the "correct" choice. If your business cost is proportional to sample count, weighted or micro is more appropriate.

### 12. Interview questions
**Easy — What is macro averaging?** Compute the metric per class, then take the unweighted mean.
**Medium — When should you use macro?** When all classes matter equally regardless of frequency — imbalanced multi-class problems, rare-but-important categories, fairness audits.
**Medium — Why is macro-F1 usually lower than accuracy on imbalanced data?** Because rare classes are typically harder (less training data, less signal) and macro gives them full weight, whereas accuracy weights by sample count and so is dominated by the easy majority classes.
**Hard — Macro-F1 is 0.42 and accuracy is 0.91. Diagnose.**
The model is almost certainly performing well on one or two dominant classes and poorly or not at all on the rest. Steps: (1) print `f1_score(..., average=None)` and the per-class support to identify which classes are failing; (2) check whether the failing classes are ever predicted at all (a column of zeros in the confusion matrix means the class is never predicted — a hallmark of severe imbalance); (3) inspect the confusion matrix for systematic confusions (which classes absorb the failing ones); (4) remedies: class weights (`class_weight='balanced'`), oversampling/targeted data collection for the rare classes, hierarchical or two-stage classification, merging classes that are not meaningfully distinct, or per-class threshold tuning in a one-vs-rest setup.

---

## 8.3 MICRO AVERAGE

### 1. Definition
Pool the TP, FP, and FN counts across **all** classes into global totals, then compute the metric once from those totals.

### 2. Intuition
**Every sample gets one vote, regardless of class.** Aggregate all decisions into one giant confusion matrix and compute one metric.

It exists because sometimes the right question is "how many total errors did the system make?", not "how did each class fare?" A support-ticket router that misroutes 500 tickets has caused 500 units of harm whether they came from common or rare categories.

### 3. Formula
```
                     Σₖ TPₖ
Micro-Precision = -------------------
                  Σₖ TPₖ + Σₖ FPₖ

                  Σₖ TPₖ
Micro-Recall = -------------------
               Σₖ TPₖ + Σₖ FNₖ

Micro-F1 = harmonic mean of Micro-P and Micro-R
```
- **Σₖ** = sum over all K classes.
- Note the pooling happens **before** the division. This is exactly what makes micro different from macro.

**The key identity for single-label multi-class:** because every misclassification is one FN for the true class and one FP for the predicted class, `Σ FP = Σ FN`. Therefore:
```
Micro-Precision = Micro-Recall = Micro-F1 = ACCURACY
```
**This is one of the most reliably asked multi-class interview facts.** In single-label multi-class, micro-averaging is just accuracy wearing a disguise.

(The identity does **not** hold for multi-label problems, where a sample can have several labels and `Σ FP ≠ Σ FN`. There, micro-F1 is a genuinely distinct and very useful metric.)

### 4. Manual example

```
Σ TP = 40 + 25 + 10 = 75
Σ FP = 10 + 10 +  5 = 25
Σ FN = 10 +  5 + 10 = 25

Micro-Precision = 75 / (75 + 25) = 75/100 = 0.7500
Micro-Recall    = 75 / (75 + 25) = 75/100 = 0.7500
Micro-F1        = 2(0.75)(0.75)/(0.75+0.75) = 0.7500

Accuracy        = 75/100 = 0.7500   <-- identical, as predicted
```

### 5. Python

```python
from sklearn.metrics import f1_score, precision_score, accuracy_score

f1_score(y_true, y_pred, average='micro')          # 0.75
precision_score(y_true, y_pred, average='micro')   # 0.75
accuracy_score(y_true, y_pred)                     # 0.75   <- all equal
```
- `average='micro'` — pools counts globally.
- In `classification_report`, sklearn **omits the `micro avg` row for single-label problems and shows `accuracy` instead**, precisely because they are the same number. If you see a `micro avg` row, you are looking at a multi-label report.

### 6. Interpretation
Micro-F1 answers: **"how often is the system right, per decision?"** It is dominated by the frequent classes, in direct proportion to their frequency.

### 7. Good vs bad values
Same bands and same caveats as accuracy. Compare to the majority-class baseline. On a dataset where one class holds 80% of samples, micro-F1 of 0.82 is barely above baseline.

### 8. Business use cases
- **Multi-label classification** — this is where micro-F1 genuinely shines and is the standard metric (image tagging, document topic tagging, multi-label medical coding).
- **Overall system throughput reporting:** "the router correctly handles 94% of tickets."
- **Cost accounting** when the cost per error is roughly constant regardless of class.
- **Large-scale extreme multi-label problems** (e.g. tagging products with thousands of possible attributes).
- **NLP entity extraction** at the token level, where micro-F1 counts every entity mention equally — the standard in CoNLL-style evaluation.
- **Information retrieval** across pooled queries.

### 9. Advantages
- Reflects **total error volume**, which maps directly to operational cost.
- Stable and low-variance, since it is driven by large pooled counts.
- The natural choice for multi-label problems.
- Simple to compute and explain.

### 10. Limitations
- **Completely dominated by frequent classes.** A model that ignores every rare class can still have high micro-F1.
- **Redundant with accuracy in single-label multi-class** — reporting both adds no information and signals inexperience.
- Hides per-class failures entirely.
- Wrong choice when rare classes are the important ones.

### 11. Common mistakes
1. **Reporting both accuracy and micro-F1 for a single-label problem** as though they were two pieces of evidence. They are one number.
2. Using micro on an imbalanced problem where rare classes matter, then wondering why the metric looks fine but stakeholders complain.
3. Not realising micro-F1 ≠ accuracy in multi-label settings, and mis-transferring intuition from one to the other.

### 12. Interview questions
**Easy — What is micro averaging?** Pool TP/FP/FN globally, then compute the metric once.
**Medium — Prove that micro-F1 equals accuracy in single-label multi-class.** Every misclassified sample contributes exactly one FP (to the predicted class) and one FN (to the true class), so `ΣFP = ΣFN = E` where E is the number of errors. Then micro-P = micro-R = `ΣTP/(ΣTP+E) = correct/(correct+errors) = correct/N = accuracy`. The harmonic mean of two equal values is that value, so micro-F1 = accuracy.
**Medium — Why does micro-F1 differ from accuracy in multi-label?** Because a sample can have multiple true labels and multiple predicted labels, so a single sample can generate both FPs and FNs in different quantities; `ΣFP ≠ ΣFN` in general, so micro-P ≠ micro-R.
**Hard — You have 1,000 classes with a long-tailed distribution. Which average do you report?**
All three, plus the per-class distribution. Micro/accuracy for overall throughput and cost. Macro to check rare-class performance — but be explicit that with hundreds of tiny classes macro-F1 is high-variance, so also report macro over classes with support above a stated minimum, or bucket classes into head/mid/tail and report per-bucket metrics. Weighted as a bridge between the two. Long-tail literature typically reports exactly this head/mid/tail split, and mentioning it demonstrates real familiarity.

---

## 8.4 WEIGHTED AVERAGE

### 1. Definition
Compute the metric per class, then average with each class weighted by its **support** (its number of true instances).

### 2. Intuition
A compromise: **each class's contribution is proportional to how common it is.** Unlike macro, it does not let a 3-sample class dominate; unlike micro, it is computed per class first, so the per-class structure is preserved.

It exists as the pragmatic default when you want a single number that reflects real-world class frequencies but is still built from per-class metrics.

### 3. Formula
```
                     K   nₖ
Weighted-metric = Σ   ---- × metricₖ
                    k=1  N
```
- **nₖ** = support of class k (number of true instances of class k)
- **N** = total samples = Σ nₖ
- **nₖ/N** = the weight, i.e. the class's share of the data
- Weights sum to 1.

**Two identities worth knowing:**
- **Weighted-Recall = Accuracy**, always. (Because weighted recall = `Σ (nₖ/N) × (TPₖ/nₖ) = Σ TPₖ/N = correct/N`.)
- Weighted-Precision and Weighted-F1 are **not** equal to accuracy, and weighted-F1 is not the harmonic mean of weighted-P and weighted-R — which means **weighted-F1 can fall outside the range [weighted-P, weighted-R]**, an odd property that some authors consider a defect.

### 4. Manual example

Weights: A = 50/100 = 0.50, B = 30/100 = 0.30, C = 20/100 = 0.20.

```
Weighted-Precision = (0.50 × 0.8000) + (0.30 × 0.7143) + (0.20 × 0.6667)
                   = 0.40000 + 0.21429 + 0.13333
                   = 0.74762  ->  0.7476

Weighted-Recall    = (0.50 × 0.8000) + (0.30 × 0.8333) + (0.20 × 0.5000)
                   = 0.40000 + 0.25000 + 0.10000
                   = 0.75000  ->  0.7500   == ACCURACY ✓

Weighted-F1        = (0.50 × 0.8000) + (0.30 × 0.7692) + (0.20 × 0.5714)
                   = 0.40000 + 0.23077 + 0.11429
                   = 0.74505  ->  0.7451
```

### 5. Python

```python
from sklearn.metrics import f1_score, precision_score, recall_score

precision_score(y_true, y_pred, average='weighted')   # 0.7476
recall_score(y_true, y_pred,    average='weighted')   # 0.7500  == accuracy
f1_score(y_true, y_pred,        average='weighted')   # 0.7451
```
- `average='weighted'` weights by support. This is the row labelled `weighted avg` in `classification_report`.
- Note that support is computed from `y_true`, not `y_pred`.

### 6. Interpretation
Weighted-F1 answers: **"how well does the model do on a typical SAMPLE, while still respecting per-class structure?"** It sits between macro and micro, usually closer to micro.

Our three numbers side by side:
```
Macro-F1    = 0.7135   <- rare class C penalises us; each class gets 1/3 vote
Weighted-F1 = 0.7451   <- weighted by 50/30/20
Micro-F1    = 0.7500   <- = accuracy; dominated by the frequent classes
```
**The ordering `macro < weighted < micro` is typical whenever rare classes perform worse**, which is the normal situation. Seeing that pattern is itself a diagnostic.

### 7. Good vs bad values
Similar bands to accuracy. The most informative thing is the **gap between macro and weighted** — a large gap means uneven per-class performance.

### 8. Business use cases
- **General multi-class reporting** where class frequencies mirror real-world frequencies — the pragmatic default in `classification_report`.
- **Product categorisation in e-commerce** where the frequency distribution of categories is genuinely the business's distribution.
- **Customer segmentation models.**
- **Document classification** in a corpus whose topic distribution is representative.
- **Executive summary reporting** — one number that is neither naively frequency-blind nor totally frequency-dominated.
- **Sentiment analysis** with naturally skewed sentiment distributions.

### 9. Advantages
- Reflects real-world class frequencies without being purely sample-counting.
- More stable than macro when some classes are tiny.
- The default in `classification_report`, so widely seen and understood.
- Weighted-recall equals accuracy, which is a convenient consistency check.

### 10. Limitations
- **Under-weights rare classes**, so it partially reproduces accuracy's blind spot. If rare classes are the point, use macro.
- **Weighted-F1 is not a harmonic mean of weighted-P and weighted-R**, and can lie outside their range — mathematically inelegant and occasionally confusing.
- Assumes the test-set class distribution matches production. If it does not, the weights are wrong.
- Hides per-class detail.
- Being the default, it is frequently reported without thought.

### 11. Common mistakes
1. **Using the default `weighted avg` on an imbalanced problem where the minority class is the target.** This is the most common multi-class metric error. A fraud-type classifier reporting weighted-F1 = 0.94 may be completely failing on the rare fraud types.
2. Not realising weighted-recall = accuracy.
3. Assuming weighted-F1 lies between weighted-P and weighted-R.
4. Using test-set-derived weights when the production distribution differs.

### 12. Interview questions
**Easy — What is weighted averaging?** Per-class metrics averaged with weights proportional to class support.
**Easy — Which weighted metric equals accuracy?** Weighted recall.
**Medium — Macro vs micro vs weighted, in one sentence each?** Macro: every class counts equally. Micro: every sample counts equally (= accuracy in single-label). Weighted: every class counts in proportion to its size.
**Medium — Which do you use for an imbalanced multi-class problem where rare classes matter most?** Macro, with the per-class breakdown, and per-class recall specifically if missing rare classes is the risk.
**Hard — Explain the ordering macro-F1 = 0.71 < weighted-F1 = 0.745 < micro-F1 = 0.75 for our example.**
Rare class C has the worst F1 (0.571) and the smallest support (20). Macro gives it a full 1/3 weight, so it drags the mean down most. Weighted gives it only 0.20 weight, so it drags less. Micro (= accuracy) weights every *sample* equally, so C's 20 samples influence only 20% of the calculation and its individual class-level failure is diluted further. Whenever the smallest classes are the weakest — the usual case — this ordering appears, and the size of the macro-to-micro gap quantifies how uneven the model is.

## 8.5 Multi-class averaging: decision table

| Question | Answer | Use |
|---|---|---|
| Do all classes matter equally, regardless of size? | Yes | **Macro** |
| Do you care about total error count / throughput? | Yes | **Micro** (= accuracy) |
| Should classes count in proportion to frequency? | Yes | **Weighted** |
| Are rare classes the high-stakes ones? | Yes | **Macro** + per-class recall |
| Is it a multi-label problem? | Yes | **Micro-F1** and **macro-F1** (both; they now differ meaningfully) |
| Auditing fairness across demographic groups? | Yes | **Macro** across groups + per-group breakdown |
| Long-tailed distribution with hundreds of tiny classes? | Yes | Macro over classes with sufficient support, plus **head/mid/tail** buckets |
| Just want the headline number? | — | **Weighted**, but always print `average=None` too |

**Universal rule:** whichever average you report, **always also print `average=None`** to see the per-class values. Every single-number average hides something; the per-class table is where the diagnosis lives.

---

# PART 9 — Multi-label Metrics

## 9.0 Multi-class vs multi-label

| | Multi-class | Multi-label |
|---|---|---|
| Labels per sample | Exactly one | Zero, one, or many |
| Example | "This image is a cat" (cat OR dog OR bird) | "This image contains a cat, a sofa, and a lamp" |
| Output layer | Softmax over K (sums to 1) | K independent sigmoids (each 0–1) |
| Loss | Categorical cross-entropy | Binary cross-entropy per label |
| `y` shape | `(N,)` integers | `(N, L)` binary matrix |
| Prediction | `argmax` | Threshold each label independently |

Multi-label metrics must handle **partial credit**: if the true labels are {cat, sofa, lamp} and the model predicts {cat, sofa}, that is much better than predicting {dog} but not as good as getting all three. Multi-class metrics have no way to express that.

## 9.1 THE MULTI-LABEL RUNNING EXAMPLE

3 samples, 4 possible labels (L1, L2, L3, L4):

```
             TRUE                        PREDICTED
        L1  L2  L3  L4              L1  L2  L3  L4
  s1 [  1   0   1   0  ]      s1 [  1   0   0   0  ]   <- missed L3
  s2 [  0   1   1   0  ]      s2 [  0   1   1   0  ]   <- perfect
  s3 [  1   1   0   1  ]      s3 [  1   0   0   1  ]   <- missed L2
```

```python
import numpy as np
Y_true = np.array([[1,0,1,0],
                   [0,1,1,0],
                   [1,1,0,1]])
Y_pred = np.array([[1,0,0,0],
                   [0,1,1,0],
                   [1,0,0,1]])
```
Total label slots = 3 samples × 4 labels = **12**. Mismatches: s1/L3 (1→0) and s3/L2 (1→0) → **2 wrong out of 12.**

---

## 9.2 HAMMING LOSS

### 1. Definition
The fraction of individual **label slots** that are wrong, across all samples and all labels.

### 2. Intuition
The most forgiving multi-label metric: **it grades label by label, giving full partial credit.** Getting 3 of 4 labels right on a sample earns 75%, not zero.

Named after Richard Hamming's distance between bit strings — it is literally the normalised Hamming distance between the true and predicted label matrices.

### 3. Formula
```
                    1     N    L
Hamming Loss = --------- Σ    Σ   1[ y_{i,j} ≠ ŷ_{i,j} ]
                  N × L  i=1  j=1
```
- **N** = number of samples; **L** = number of labels
- **y_{i,j}** = true value (0/1) of label j for sample i; **ŷ_{i,j}** = predicted value
- **1[·]** = indicator: 1 if the two differ, 0 if they match
- **N × L** = total number of label slots
- Range **[0, 1]**; **lower is better**; 0 = every label on every sample correct.
- `1 − Hamming Loss` = **label-based accuracy**.

For a binary single-label problem, Hamming Loss reduces exactly to the error rate.

### 4. Manual example

```
Label-by-label comparison (12 slots):

s1: true [1,0,1,0] vs pred [1,0,0,0]  ->  L1 ✓  L2 ✓  L3 ✗  L4 ✓   = 1 error
s2: true [0,1,1,0] vs pred [0,1,1,0]  ->  L1 ✓  L2 ✓  L3 ✓  L4 ✓   = 0 errors
s3: true [1,1,0,1] vs pred [1,0,0,1]  ->  L1 ✓  L2 ✗  L3 ✓  L4 ✓   = 1 error

Total errors = 2
Total slots  = 3 × 4 = 12
Hamming Loss = 2 / 12 = 0.1667
```
**Hamming Loss = 0.1667**, i.e. 16.7% of label decisions are wrong; label-based accuracy = 83.3%.

### 5. Python

```python
from sklearn.metrics import hamming_loss
hamming_loss(Y_true, Y_pred)         # 0.16666666666666666
1 - hamming_loss(Y_true, Y_pred)     # 0.8333  (label-based accuracy)
```
- Accepts binary indicator matrices of shape `(N, L)`.
- For single-label multi-class input, `hamming_loss` returns the plain error rate.

### 6. Interpretation
Lower is better.

| Value | Meaning |
|---|---|
| 0.00 | Every label decision correct |
| 0.05 | 5% of label decisions wrong — strong |
| 0.17 | Our example |
| 0.30 | Weak |
| 0.50 | Coin flip per label |

**Critical caveat — the sparsity trap.** In extreme multi-label settings (5,000 possible tags, ~4 true per document), predicting **all zeros** yields a Hamming Loss of about `4/5000 = 0.0008`, i.e. 99.92% "label accuracy," while identifying nothing at all. **Hamming Loss is nearly useless as a standalone metric on sparse label sets** — always pair it with micro/macro-F1 or Jaccard. This is the multi-label analogue of the accuracy paradox and a favourite interview trap.

### 7. Good vs bad values
Entirely dependent on label sparsity. Always compare against the trivial all-zeros baseline, which equals the **label cardinality density** (average number of true labels per sample ÷ L). Our baseline: 7 total positives / 12 slots = 0.583, so 0.167 is a genuine improvement here.

### 8. Business use cases
- **Multi-label image tagging** (photo auto-tagging).
- **Document / news topic tagging.**
- **Medical coding (ICD-10)** — a patient record maps to several diagnosis codes; partial credit is essential.
- **Product attribute tagging in e-commerce.**
- **Music genre tagging.**
- **Gene function prediction** in bioinformatics.
- **Multi-label toxicity classification** (a comment may be both threatening and obscene).

### 9. Advantages
- Simple, symmetric, and gives full partial credit.
- Treats every label independently → easy to interpret per-label.
- Fast to compute and stable.
- Reduces sensibly to error rate in the binary case.

### 10. Limitations
- **Fails badly on sparse label sets** — the all-zeros trap above.
- **Ignores label correlations.** In reality, "beach" and "sand" co-occur; Hamming treats them as unrelated.
- Treats FP and FN symmetrically, which is rarely right (missing a tag ≠ adding a wrong tag).
- Gives no credit structure per sample — a sample with 3 of 4 labels right and one with a different 3 of 4 right score identically even if one error is far more damaging.
- Not in the units stakeholders think in.

### 11. Common mistakes
1. Reporting Hamming Loss alone on a sparse multi-label problem.
2. Confusing Hamming Loss (label-level) with subset accuracy (sample-level, all-or-nothing).
3. Forgetting that lower is better (it is a *loss*).
4. Not comparing to the all-zeros baseline.

### 12. Interview questions
**Easy — What is Hamming Loss?** The fraction of individual label predictions that are wrong.
**Easy — Is higher or lower better?** Lower.
**Medium — Why is Hamming Loss misleading for extreme multi-label problems?** With thousands of labels and only a handful true per sample, predicting all zeros gets a near-zero loss. The metric is dominated by the vast majority of correctly-predicted absent labels.
**Hard — Hamming Loss vs micro-F1 for multi-label?** Hamming counts TN as successes (implicitly, via the denominator N×L), so sparse label sets inflate it. Micro-F1 pools TP/FP/FN and **excludes TN entirely**, so it cannot be gamed by predicting nothing (all-zeros gives micro-F1 = 0). For sparse multi-label problems, micro-F1 and macro-F1 are the primary metrics and Hamming Loss is at best a secondary diagnostic.

---

## 9.3 JACCARD SCORE (Intersection over Union, IoU)

### 1. Definition
The size of the intersection of the true and predicted label sets, divided by the size of their union.

### 2. Intuition
**"How much do the two sets overlap, relative to everything either of them claims?"**

Treat each sample's labels as a set. True = {cat, sofa, lamp}. Predicted = {cat, sofa, dog}. Intersection = {cat, sofa} = 2. Union = {cat, sofa, lamp, dog} = 4. Jaccard = 2/4 = 0.5.

It is stricter than Hamming because it does not get credit for correctly-absent labels: the denominator is only the union, so it never rewards you for the thousands of tags you correctly did not apply. That makes it far more honest on sparse label sets.

This is the **same metric as IoU** in computer vision, where the "sets" are pixels or bounding-box areas rather than labels.

### 3. Formula
```
                | Y ∩ Ŷ |            TP
Jaccard = ------------------ = -----------------
                | Y ∪ Ŷ |        TP + FP + FN
```
- **Y** = set of true labels; **Ŷ** = set of predicted labels
- **|Y ∩ Ŷ|** = number of labels in both = **TP**
- **|Y ∪ Ŷ|** = number of labels in either = **TP + FP + FN**
- Range [0, 1]; higher is better; 1 = exact match; 0 = no overlap.
- **TN is absent from the formula** — the source of its robustness on sparse data.

**Averaging options (multi-label):**
- `average='samples'` — Jaccard per sample, then mean across samples. The most common choice for multi-label.
- `average='macro'` — Jaccard per label, then unweighted mean.
- `average='micro'` — pool TP/FP/FN globally, then compute once.
- `average='weighted'` — per label, weighted by support.

### 4. Manual example — per-sample (`average='samples'`)

```
s1: true {L1, L3}      pred {L1}
    intersection = {L1}          -> 1
    union        = {L1, L3}      -> 2
    Jaccard      = 1/2 = 0.5000

s2: true {L2, L3}      pred {L2, L3}
    intersection = {L2, L3}      -> 2
    union        = {L2, L3}      -> 2
    Jaccard      = 2/2 = 1.0000

s3: true {L1, L2, L4}  pred {L1, L4}
    intersection = {L1, L4}      -> 2
    union        = {L1, L2, L4}  -> 3
    Jaccard      = 2/3 = 0.6667

Mean = (0.5000 + 1.0000 + 0.6667) / 3 = 2.1667 / 3 = 0.7222
```
**Jaccard (samples) = 0.7222.**

For comparison, on the **binary** running example from Part 1 (TP=15, FP=10, FN=5):
```
Jaccard = 15 / (15 + 10 + 5) = 15/30 = 0.5000
```
Note it is markedly lower than F1 (0.667) on the same data — see the relationship in 9.3.12.

### 5. Python

```python
from sklearn.metrics import jaccard_score

jaccard_score(Y_true, Y_pred, average='samples')    # 0.7222
jaccard_score(Y_true, Y_pred, average='macro')      # per-label then mean
jaccard_score(Y_true, Y_pred, average='micro')      # pooled
jaccard_score(Y_true, Y_pred, average=None)         # per-label array

# Binary case (Part 1 running example)
# jaccard_score(y_true, y_pred)                     # 0.5
```
- `average='samples'` is only valid for multi-label input.
- `zero_division` handles samples where both true and predicted label sets are empty (union = 0).

### 6. Interpretation

| Value | Meaning |
|---|---|
| 0.00 | No overlap at all |
| 0.30 | Weak overlap |
| 0.50 | Half the union is shared — our binary example |
| 0.72 | Good — our multi-label example |
| 0.90 | Excellent |
| 1.00 | Exact set match |

In computer vision, **IoU ≥ 0.5** is the conventional threshold for "this detection counts as correct" (Pascal VOC); COCO evaluates at IoU thresholds from 0.5 to 0.95 to reward precise localisation.

### 7. Good vs bad values
Poor < 0.40, Average 0.40–0.60, Good 0.60–0.80, Excellent > 0.80. For segmentation tasks, mean IoU above 0.75 is typically strong; state-of-the-art semantic segmentation on standard benchmarks sits around 0.60–0.85 mIoU depending on dataset.

### 8. Business use cases
- **Semantic segmentation** (medical imaging, autonomous driving) — mIoU is *the* metric.
- **Object detection** — IoU determines whether a predicted box matches a ground-truth box, which in turn drives mAP.
- **Multi-label document / image tagging.**
- **Recommendation set overlap** — how well the recommended set matches the set a user engaged with.
- **Medical image tumour delineation** — although Dice (9.4-adjacent, see 10.7) is more common there.
- **Entity set extraction in NLP.**
- **Duplicate / near-duplicate detection** — Jaccard similarity on shingles is the basis of MinHash and LSH.
- **Market-basket similarity in retail.**

### 9. Advantages
- **Ignores TN** → honest on sparse label sets, unlike Hamming Loss.
- Intuitive set-overlap meaning; easy to draw on a whiteboard.
- Same metric as IoU, so it transfers across ML, CV, and information retrieval.
- Gives partial credit, unlike subset accuracy.
- Symmetric in true and predicted sets.

### 10. Limitations
- **Harsher than F1** for the same predictions (see the relationship below), which can look discouraging.
- Undefined when both sets are empty (needs a convention; sklearn's `zero_division` handles it).
- Ignores label correlations.
- Treats FP and FN symmetrically.
- Averaging choice matters a lot and is easy to get wrong.
- Non-differentiable, so it cannot be used directly as a training loss (soft-IoU / Lovász-softmax surrogates exist for exactly this reason).

### 11. Common mistakes
1. Not specifying `average` in multi-label settings, or using `'micro'` when `'samples'` was intended.
2. Confusing Jaccard with Dice/F1 — they are monotonically related but numerically different.
3. Assuming IoU and Dice are interchangeable when reporting segmentation results; papers report one or the other and mixing them makes comparisons wrong.
4. Forgetting Jaccard is available for binary problems too.

### 12. Interview questions
**Easy — What is the Jaccard score?** Intersection over union of the true and predicted label sets: TP/(TP+FP+FN).
**Easy — What is IoU?** The same metric, applied to pixels or bounding-box areas in computer vision.
**Medium — Jaccard vs Hamming Loss?** Hamming counts every label slot including correctly-absent ones, so it is inflated on sparse data. Jaccard's denominator is only the union of claimed labels, so it never earns credit for absent labels and is honest on sparse data.
**Medium — Relationship between Jaccard and F1/Dice?**
```
              F1                              2J
Jaccard = -----------      and      F1 = ----------
             2 − F1                        1 + J
```
Check with our binary example: F1 = 0.6667 → `J = 0.6667/(2 − 0.6667) = 0.6667/1.3333 = 0.5` ✓. They are **monotonically related**, so they always rank models in the same order — but Jaccard is always ≤ F1 (they are equal only at 0 and 1). Knowing this closed-form relationship is a strong answer.
**Hard — Why is IoU not used directly as a training loss?** It is non-differentiable (it involves counting set intersections via hard thresholds) and its gradient is zero when the predicted and true regions do not overlap at all, which stalls learning early in training. Differentiable surrogates are used instead: **soft IoU** (replacing counts with sums of probabilities), **Dice loss**, **Lovász-softmax** (a convex surrogate to the Jaccard loss), or **GIoU/DIoU/CIoU** for bounding-box regression, which add terms that provide gradient even for non-overlapping boxes.

---

## 9.4 SUBSET ACCURACY (Exact Match Ratio)

### 1. Definition
The fraction of samples for which the **entire** predicted label set exactly matches the true label set.

### 2. Intuition
**All or nothing.** Get every label right on a sample and score 1; get 9 of 10 right and score 0.

It exists because for some tasks partial credit is genuinely meaningless. If you are auto-filling a structured form, a legal filing, or a medication order, "mostly correct" is not usable output — the whole record must be right or a human must intervene. Subset accuracy measures the fraction of cases needing **no** human touch, which is exactly the automation-rate question.

It is the **strictest** multi-label metric.

### 3. Formula
```
                        1    N
Subset Accuracy = --- ×  Σ  1[ Yᵢ = Ŷᵢ ]
                        N   i=1
```
- **1[Yᵢ = Ŷᵢ]** = 1 if the full label vector matches exactly, 0 otherwise
- **N** = number of samples
- Range [0, 1]; higher is better.
- In the single-label case, it reduces to ordinary accuracy.

### 4. Manual example

```
s1: true [1,0,1,0]  vs  pred [1,0,0,0]  ->  NOT equal  ->  0
s2: true [0,1,1,0]  vs  pred [0,1,1,0]  ->  EQUAL      ->  1
s3: true [1,1,0,1]  vs  pred [1,0,0,1]  ->  NOT equal  ->  0

Subset Accuracy = (0 + 1 + 0) / 3 = 1/3 = 0.3333
```
**Subset Accuracy = 0.3333.**

Compare all three multi-label metrics on identical predictions:
```
Hamming Loss     = 0.1667  ->  "83.3% of label decisions correct"   (most forgiving)
Jaccard (samples)= 0.7222  ->  "72.2% set overlap"                  (middle)
Subset Accuracy  = 0.3333  ->  "33.3% of samples perfect"           (strictest)
```
**Same model, same predictions, three numbers from 0.33 to 0.83.** Which one you report determines the story you tell, so the choice must follow from the business requirement, not from which looks best.

### 5. Python

```python
from sklearn.metrics import accuracy_score
accuracy_score(Y_true, Y_pred)      # 0.3333  -- for multi-label input, this IS subset accuracy
```
- **Important:** `accuracy_score` silently switches meaning based on input shape. Given a 2-D indicator matrix it computes **subset accuracy**, not label-wise accuracy. Many people report it without realising how strict it is — a very common and consequential mistake.

### 6. Interpretation

| Value | Meaning |
|---|---|
| 0.00 | No sample is perfectly labelled |
| 0.33 | 1 in 3 samples fully correct — our example |
| 0.60 | Solid for a multi-label task |
| 0.85 | Strong |
| 1.00 | Every sample perfectly labelled |

Read it as an **automation rate**: "we can fully automate 33% of cases; the remaining 67% need review."

### 7. Good vs bad values
Falls sharply as the number of labels per sample grows. If per-label accuracy is 0.95 and a sample has 10 labels, expected subset accuracy is roughly `0.95¹⁰ ≈ 0.60`; with 20 labels, `0.95²⁰ ≈ 0.36`. **So a low subset accuracy may indicate many labels rather than a poor model** — always report it alongside label cardinality and Hamming/F1.

### 8. Business use cases
- **Automated form filling / structured data extraction** — partial fills are not shippable.
- **Medical coding audits** — a claim must have exactly the right code set to be submitted.
- **Legal/compliance document tagging** where an incomplete tag set fails an audit.
- **Configuration and rules generation** — a partially correct configuration is broken.
- **Machine translation / code generation exact-match evaluation** (analogous strictness).
- **Automation-rate reporting:** "what fraction of cases require zero human intervention?" is precisely subset accuracy, and it is the number that drives cost-savings business cases.

### 9. Advantages
- Unambiguous and easy to explain.
- Directly maps to automation rate and human-in-the-loop cost.
- The right metric when partial correctness has zero value.
- No averaging choices to argue about.

### 10. Limitations
- **Extremely harsh** — no partial credit at all.
- **Degrades multiplicatively with the number of labels**, so it is not comparable across datasets with different label cardinality.
- Provides no gradient of information: it cannot distinguish "one label wrong" from "everything wrong."
- Not useful for model development or hyperparameter tuning (too coarse, and often near zero early in training).
- Ignores which labels were wrong and how badly.

### 11. Common mistakes
1. **Reporting `accuracy_score` on multi-label data without realising it is subset accuracy**, then wondering why the number is so low.
2. Comparing subset accuracy across datasets with different label counts.
3. Using it as the sole optimisation target — it gives too weak a signal.
4. Not reporting label cardinality alongside it.

### 12. Interview questions
**Easy — What is subset accuracy?** The fraction of samples whose entire predicted label set exactly matches the truth.
**Easy — What does `accuracy_score` compute on multi-label input?** Subset accuracy.
**Medium — Why is subset accuracy so low on multi-label problems?** Because errors compound: with per-label accuracy `a` and `L` labels, exact match requires all L to be right, roughly `a^L` under independence. Even 95% per-label accuracy gives only ~36% exact match at 20 labels.
**Medium — Rank Hamming Loss, Jaccard, and Subset Accuracy by strictness.** Subset accuracy (strictest) > Jaccard (middle) > 1 − Hamming Loss (most forgiving). Report all three: they answer "how many cases are perfect?", "how much do the sets overlap?", and "how many individual decisions are right?"
**Hard — Which multi-label metric would you optimise, and how would you justify it to a product manager?**
It depends on the downstream consumption. If output feeds an automated pipeline that cannot tolerate partial results, optimise **subset accuracy** and frame it as automation rate. If a human reviews and edits suggested tags, optimise **micro-F1** or **per-sample Jaccard**, since each correct suggestion saves work and each wrong one costs a click. If certain labels are high-stakes (a missed "self-harm" tag), optimise **macro-F1** or set **per-label thresholds** to hit per-label recall floors. The right answer is to instrument the actual downstream cost — review seconds saved per correct tag, cost per missed critical tag — and choose the metric whose gradient matches that cost. Then set per-label thresholds rather than a single global 0.5, because label frequencies and costs differ.

---

# PART 10 — Imbalanced Data & Advanced Metrics

## 10.0 Why accuracy is misleading on imbalanced data

The mechanism in one sentence: **accuracy is a weighted average of per-class performance, weighted by class size, so a 99%-majority class contributes 99% of the score.**

### The canonical demonstration

10,000 credit card transactions, 100 fraudulent (1%). Compare three models:

| | Model A: "always legit" | Model B: real model | Model C: "always fraud" |
|---|---|---|---|
| TP | 0 | 80 | 100 |
| FP | 0 | 400 | 9,900 |
| FN | 100 | 20 | 0 |
| TN | 9,900 | 9,500 | 0 |
| **Accuracy** | **0.9900** | 0.9580 | 0.0100 |
| Precision | undefined (0) | 0.1667 | 0.0100 |
| Recall | 0.0000 | 0.8000 | 1.0000 |
| Specificity | 1.0000 | 0.9596 | 0.0000 |
| F1 | 0.0000 | 0.2759 | 0.0198 |
| Balanced Accuracy | 0.5000 | 0.8798 | 0.5000 |
| G-Mean | 0.0000 | 0.8762 | 0.0000 |
| MCC | 0.0000 | 0.3536 | 0.0000 |
| Cohen's Kappa | 0.0000 | 0.2637 | 0.0000 |

**By accuracy, Model A (which does literally nothing) is the best model at 0.99.** Model B, the only useful model, scores *lower*.

Every other metric in the table correctly ranks B first. MCC, Kappa, and G-Mean all give the two degenerate models exactly **0.0**, which is the ideal behaviour: they refuse to award any credit for a model with no skill.

### The three failure modes accuracy creates

1. **Model selection failure.** `GridSearchCV(scoring='accuracy')` on imbalanced data converges to models that predict the majority class. The search *works correctly* — it maximises the metric you gave it. You gave it the wrong metric.
2. **Training failure.** With unweighted loss, gradient descent finds that predicting the majority class minimises average loss quickly, and the minority class gets ignored.
3. **Reporting failure.** Stakeholders approve deployment on the basis of 99% accuracy, and the model catches nothing.

### The full imbalanced-data toolkit

| Layer | Action |
|---|---|
| **Metric** | Use PR-AUC, MCC, Balanced Accuracy, G-Mean, F2 — never bare accuracy |
| **Baseline** | Always compute the majority-class and prevalence baselines and report them |
| **Threshold** | Never leave it at 0.5; tune on a cost or capacity criterion |
| **Loss** | `class_weight='balanced'`, `scale_pos_weight` in XGBoost, focal loss |
| **Data** | Targeted collection of minority examples; SMOTE/undersampling (training set only) |
| **Validation** | `StratifiedKFold`, never plain `KFold` |
| **Test set** | **Never resample it.** Precision, PR-AUC, and calibration all become invalid |
| **Calibration** | Recalibrate after any resampling, or apply a prior-shift correction |

### Which metrics work best when positives are only 1%?

| Rank | Metric | Why |
|---|---|---|
| 1 | **PR-AUC / Average Precision** | Threshold-free, ignores the huge TN mass, baseline = prevalence, sensitive to top-of-ranking quality |
| 2 | **Precision@k / Recall@k** | Matches the real constraint: you can only review k cases per day |
| 3 | **MCC** | Uses all four cells, symmetric, 0 for any degenerate model, single honest number |
| 4 | **Expected cost / expected loss in currency** | The only metric that answers "should we deploy?" |
| 5 | **F2 (or F-beta with β from the cost ratio)** | Encodes the asymmetric cost explicitly |
| 6 | **Recall at a fixed precision floor** (or vice versa) | "Recall at precision ≥ 0.30" is a clean, contract-like target |
| 7 | **Balanced Accuracy / G-Mean** | Good if the negative class also matters; immune to the paradox |
| 8 | **Brier Skill Score / Log Loss** | Only if downstream decisions need the probability values |
| — | ROC-AUC | Report it, but never alone; it will look great regardless |
| — | Accuracy | Report only alongside the majority baseline, if at all |

**The single best practice:** report a small dashboard rather than one number — **PR-AUC (with prevalence), precision and recall at the deployed threshold, MCC, and expected cost.** Any interviewer asking "what metric for 1% fraud?" is looking for exactly this multi-metric answer plus the reasoning.

---

## 10.1 MATTHEWS CORRELATION COEFFICIENT (MCC)

### 1. Definition
The Pearson correlation coefficient between the true labels and the predicted labels, treated as two binary variables. Also known as the **phi coefficient**.

### 2. Intuition
MCC is the closest thing to a **single trustworthy number** for binary classification.

Its defining property: **a model scores highly only if it does well on both classes at once.** Because it is a correlation, it ranges from −1 to +1, and — crucially — **any degenerate model (predict all-one-class) scores exactly 0**, regardless of imbalance. Accuracy gives that model 0.99; MCC gives it 0.

It exists because F1 and accuracy each have a structural blind spot (F1 ignores TN; accuracy is dominated by the majority class), and MCC has neither. It uses all four cells, is symmetric under swapping the positive and negative class, and is symmetric under swapping predictions and truth. Recent methodological literature increasingly recommends it as the default single-number metric for binary classification.

### 3. Formula
```
                   (TP × TN) − (FP × FN)
MCC = ------------------------------------------------------------
      √( (TP+FP) × (TP+FN) × (TN+FP) × (TN+FN) )
```
Symbol by symbol:
- **TP × TN** = the product of the two "correct" cells — rewards getting both classes right
- **FP × FN** = the product of the two "wrong" cells — penalises errors on both sides
- The numerator is positive when correct predictions dominate, negative when errors dominate, and **exactly zero when the model's predictions are statistically independent of the truth**
- The denominator is the geometric mean of the four marginal totals: predicted positives, actual positives, actual negatives, predicted negatives. It normalises the result to [−1, +1]
- If **any** marginal is zero (e.g. the model never predicts positive), the denominator is 0 and MCC is defined as 0 by convention — which is exactly the right answer for a degenerate model

**Range and meaning:**
- **+1** = perfect prediction
- **0** = no better than random / no correlation
- **−1** = perfectly inverted (flip the predictions for a perfect model)

**Multi-class generalisation** exists (`matthews_corrcoef` handles it) and is sometimes called the R_K statistic.

### 4. Manual example (running example: TP=15, TN=70, FP=10, FN=5)

```
Step 1 — numerator:
  TP × TN = 15 × 70 = 1050
  FP × FN = 10 ×  5 =   50
  numerator = 1050 − 50 = 1000

Step 2 — the four marginals:
  TP + FP = 15 + 10 = 25    (predicted positives)
  TP + FN = 15 +  5 = 20    (actual positives)
  TN + FP = 70 + 10 = 80    (actual negatives)
  TN + FN = 70 +  5 = 75    (predicted negatives)

Step 3 — product of marginals:
  25 × 20 = 500
  80 × 75 = 6000
  500 × 6000 = 3,000,000

Step 4 — square root:
  √3,000,000 = 1732.0508

Step 5 — divide:
  MCC = 1000 / 1732.0508 = 0.5774
```
**MCC = 0.5774.**

Compare all our single-number metrics on the same data:
```
Accuracy          = 0.8500   <- inflated by the 80 negatives
F1                = 0.6667   <- ignores the 70 TNs entirely
Balanced Accuracy = 0.8125
MCC               = 0.5774   <- the most conservative and most honest
Cohen's Kappa     = 0.5714
```
**MCC is the lowest.** That is characteristic: MCC is a demanding metric because it requires genuine correlation across the whole matrix. A model with MCC 0.58 and accuracy 0.85 is a normal, moderately-good model — do not panic at the lower number.

### 5. Python

```python
from sklearn.metrics import matthews_corrcoef
matthews_corrcoef(y_true, y_pred)     # 0.5773502691896258

# In model selection
# GridSearchCV(model, params, scoring='matthews_corrcoef', cv=5)

# Multi-class works too
# matthews_corrcoef(y_true_mc, y_pred_mc)
```
- Takes hard labels (not probabilities) — it is a threshold metric.
- Returns 0.0 rather than `nan` when a marginal is zero.
- `scoring='matthews_corrcoef'` is available as a string in `GridSearchCV`.

### 6. Interpretation

| Value | Meaning |
|---|---|
| 1.00 | Perfect |
| 0.70 | Strong relationship |
| 0.58 | Moderate — our example |
| 0.40 | Weak-to-moderate |
| 0.20 | Weak |
| 0.00 | **No relationship — the model is uninformative** |
| −0.30 | Inverted; the model has learned the pattern backwards |
| −1.00 | Perfectly inverted |

Because it is a correlation coefficient, the conventional correlation bands apply reasonably well: |r| 0.1 = small, 0.3 = medium, 0.5 = large.

### 7. Good vs bad values

| Band | Verdict |
|---|---|
| < 0.10 | No usable signal |
| 0.10 – 0.30 | Weak but sometimes valuable in hard domains (finance, genomics) |
| 0.30 – 0.50 | Moderate; typical of many real production models on hard problems |
| 0.50 – 0.70 | Good |
| > 0.70 | Strong; verify no leakage |

Note that MCC values that look "low" can be excellent in genuinely hard domains. An MCC of 0.25 on a rare-event problem where the baseline is 0 may represent enormous business value.

### 8. Business use cases
- **Bioinformatics and computational biology** — the field where MCC became standard (protein secondary structure prediction, gene finding, binding-site prediction), because those problems are severely imbalanced.
- **Any imbalanced binary problem** as the primary single-number metric: fraud, churn, rare disease, defect detection.
- **Model comparison and leaderboards** where you want one number that cannot be gamed by class-skew tricks.
- **Medical diagnostics** as a summary alongside sensitivity/specificity.
- **Cyber security** binary detection.
- **Automated model selection** — `scoring='matthews_corrcoef'` is a strong default for imbalanced binary tasks.
- **Regulatory / audit reporting** where a defensible symmetric metric is preferred.

### 9. Advantages
- **Uses all four confusion-matrix cells** — no blind spot.
- **Symmetric:** swapping which class is "positive" leaves MCC unchanged. F1 does not have this property. This means MCC does not require an arbitrary choice of which class is interesting.
- **Robust to class imbalance:** degenerate models score exactly 0.
- **Interpretable as a correlation**, with a familiar scale including a meaningful negative range.
- High MCC mathematically requires good performance on all four cells simultaneously — it cannot be gamed.
- Available in sklearn including a multi-class version.

### 10. Limitations
- **Less familiar** to business stakeholders and to many practitioners; you will have to explain it.
- **Not decomposable** — a low MCC does not tell you *which* error type is the problem. Always pair it with the confusion matrix.
- **Threshold-dependent** — it is computed on hard predictions.
- **Cannot express asymmetric costs.** MCC treats FP and FN symmetrically, so if a miss is 100× worse than a false alarm, MCC is the wrong optimisation target.
- Undefined (set to 0) when a marginal is zero, which can mask genuinely different degenerate behaviours.
- Fewer published baselines to compare against than F1 or AUC.
- High variance on small test sets.

### 11. Common mistakes
1. Passing probabilities instead of hard labels.
2. Interpreting MCC on the same scale as F1 or accuracy — MCC of 0.58 is roughly comparable to F1 of 0.67 here, not to accuracy of 0.58.
3. Reporting MCC alone without the confusion matrix, losing all diagnostic detail.
4. Using MCC when costs are strongly asymmetric.
5. Panicking at a negative MCC instead of recognising it as inverted predictions.

### 12. Interview questions

**Easy — What is MCC?** The correlation coefficient between true and predicted binary labels; range −1 to +1.
**Easy — What does MCC = 0 mean?** The predictions are statistically independent of the truth — no skill.

**Medium — MCC vs F1: which is better and why?**
MCC, generally, for a single honest summary. F1 excludes TN, so it is blind to the model's skill at correctly clearing negatives, and it is asymmetric — relabelling which class is positive changes F1 but not MCC. MCC also assigns exactly 0 to any all-one-class model, whereas F1 for an all-positive model can be substantial when prevalence is high. F1 remains preferable when the negative class is genuinely uninteresting (information retrieval) or when comparability with published F1 baselines matters. Report both.

**Medium — Why does MCC give 0 to a majority-class-only classifier?**
Because one marginal becomes zero. If the model never predicts positive, then TP = FP = 0, so `TP + FP = 0`, the denominator is 0, and MCC is defined as 0. Intuitively: predictions that are constant have zero variance, and a correlation with a constant is undefined/zero.

**Hard — Why is MCC's symmetry property important?**
Because "which class is positive" is often an arbitrary labelling convention, not a property of the problem. Two teams analysing the same churn dataset — one labelling "churned" as positive, the other labelling "retained" as positive — will report *different* F1 scores for the identical model, which makes F1 non-comparable across such conventions. MCC returns the same value either way. This matters in benchmarking, in audits, and whenever you inherit someone else's labels.

**Hard — When would you NOT use MCC?**
(1) When costs are strongly asymmetric — MCC weights FP and FN equally, so use expected cost or F-beta. (2) When you need a threshold-free comparison — use PR-AUC or ROC-AUC. (3) When the negative class is genuinely irrelevant and you want comparability with the IR literature — use F1 or MAP. (4) When you need calibrated probabilities — use Brier or Log Loss. (5) When communicating to a non-technical audience with no time for explanation — lead with precision and recall in plain language, and keep MCC as the technical backstop.

---

## 10.2 COHEN'S KAPPA

### 1. Definition
Agreement between predictions and truth, **corrected for the agreement that would occur by chance**.

### 2. Intuition
Accuracy gives you credit for lucky guesses. Kappa takes that credit away.

The core question: **"how much better than chance is this model, on a scale where chance = 0 and perfect = 1?"**

Concretely: on a 90/10 imbalanced dataset, a model that guesses randomly *in proportion to the class frequencies* will still be right about 82% of the time by pure luck. Accuracy would report 0.82 as though it were skill. Kappa subtracts that 0.82 baseline and rescales, so the model correctly scores 0.

Kappa originated in psychology to measure **inter-rater reliability** — how much two human raters agree beyond chance. In ML we treat the model as one "rater" and the ground truth as the other.

### 3. Formula
```
        p_o − p_e
κ = -----------------
         1 − p_e
```
Symbol by symbol:
- **p_o** ("observed agreement") = the proportion of samples where prediction and truth agree = **accuracy**
- **p_e** ("expected agreement") = the proportion where they would agree **by chance**, computed from the marginal distributions:
```
p_e = P(both say positive) + P(both say negative)

    = [ (TP+FP)/N × (TP+FN)/N ]  +  [ (TN+FN)/N × (TN+FP)/N ]
       \_ pred pos _/  \_ act pos _/     \_ pred neg _/  \_ act neg _/
```
- **Numerator** `p_o − p_e` = the agreement in excess of chance
- **Denominator** `1 − p_e` = the maximum possible excess agreement (perfect agreement is 1)
- So κ is the **fraction of the achievable-above-chance agreement that the model actually achieved**.

**Range:** −1 to +1 in principle (usually −1 to 1, and negative values mean worse than chance). κ = 0 means chance-level; κ = 1 means perfect.

**Weighted Kappa** (`weights='linear'` or `'quadratic'`) penalises disagreements by how far apart the categories are — essential for **ordinal** targets like star ratings or disease severity grades, where predicting 5 stars when the truth is 1 is worse than predicting 2.

### 4. Manual example (running example: TP=15, TN=70, FP=10, FN=5, N=100)

```
Step 1 — observed agreement (= accuracy):
  p_o = (TP + TN)/N = (15 + 70)/100 = 0.85

Step 2 — marginal probabilities:
  P(predicted positive) = (TP+FP)/N = 25/100 = 0.25
  P(actual    positive) = (TP+FN)/N = 20/100 = 0.20
  P(predicted negative) = (TN+FN)/N = 75/100 = 0.75
  P(actual    negative) = (TN+FP)/N = 80/100 = 0.80

Step 3 — expected agreement by chance:
  both positive by chance = 0.25 × 0.20 = 0.05
  both negative by chance = 0.75 × 0.80 = 0.60
  p_e = 0.05 + 0.60 = 0.65

Step 4 — apply the formula:
  numerator   = p_o − p_e = 0.85 − 0.65 = 0.20
  denominator = 1  − p_e  = 1.00 − 0.65 = 0.35
  κ = 0.20 / 0.35 = 0.5714
```
**Cohen's Kappa = 0.5714.**

Read it as: accuracy was 0.85, but 0.65 of that was obtainable by chance given these marginals. Of the remaining 0.35 of "real" agreement available, the model captured 0.20 — that is 57% of the achievable skill.

Note how close κ = 0.5714 is to MCC = 0.5774. They frequently agree closely, which is reassuring, and both are much more conservative than accuracy = 0.85.

### 5. Python

```python
from sklearn.metrics import cohen_kappa_score

cohen_kappa_score(y_true, y_pred)                        # 0.5714285714285714

# Ordinal targets (e.g. severity grades 0-4, star ratings 1-5)
cohen_kappa_score(y_true, y_pred, weights='quadratic')   # QWK
cohen_kappa_score(y_true, y_pred, weights='linear')

# In model selection
# GridSearchCV(model, params, scoring='cohen_kappa', cv=5)
```
- Takes hard labels.
- `weights='quadratic'` gives **Quadratic Weighted Kappa (QWK)**, the metric used in several well-known Kaggle competitions (diabetic retinopathy grading, essay scoring, insurance risk grading). It penalises errors by the *square* of the grade distance, so being off by 2 grades is 4× worse than being off by 1.
- Works for multi-class and for more than two raters via Fleiss' Kappa (not in sklearn).

### 6. Interpretation

The Landis & Koch (1977) bands are the conventional reference and are worth quoting:

| κ | Interpretation |
|---|---|
| < 0.00 | Worse than chance |
| 0.00 – 0.20 | Slight agreement |
| 0.21 – 0.40 | Fair |
| 0.41 – 0.60 | **Moderate** — our example (0.571) |
| 0.61 – 0.80 | Substantial |
| 0.81 – 1.00 | Almost perfect |

These bands are conventions, not laws, and are sometimes criticised as arbitrary — but they are what interviewers and reviewers expect.

### 7. Good vs bad values
Poor < 0.20, Average 0.20–0.40, Good 0.40–0.60, Excellent > 0.60. Note that κ above 0.8 on a real business problem is rare and worth double-checking for leakage.

A useful sanity check: κ is bounded above by a value determined by the marginals. If the model's predicted-positive rate differs greatly from the true prevalence, κ cannot reach 1 even with the best possible arrangement — so a low κ can partly reflect a **badly calibrated prediction rate**, fixable by threshold tuning.

### 8. Business use cases
- **Inter-annotator agreement** in labelling projects — the original use, and the standard way to decide whether your labels are reliable enough to model. If two human annotators only reach κ = 0.4, no model can be expected to exceed human consistency, and κ gives you that ceiling.
- **Medical grading tasks** (radiology severity, pathology grades) where the target is ordinal → QWK.
- **Automated essay scoring** — QWK is the industry-standard metric.
- **Diabetic retinopathy screening** — famous Kaggle competition scored on QWK.
- **Insurance risk-band assignment** — ordinal grades.
- **Content moderation policy grading** where categories have severity ordering.
- **Model-vs-human comparison:** "does the model agree with the expert as much as two experts agree with each other?" is answered by comparing model-vs-truth κ to human-vs-human κ. This is the most compelling way to present a medical AI result.
- **Imbalanced classification** as a chance-corrected alternative to accuracy.

### 9. Advantages
- **Chance-corrected** — removes the free credit that imbalance grants to accuracy.
- Widely accepted with established interpretation bands.
- **Handles ordinal targets** via weighting, which almost no other classification metric does.
- Extends to multi-class and to multiple raters (Fleiss' Kappa).
- Directly comparable to human inter-rater agreement, which gives a meaningful performance ceiling.

### 10. Limitations
- **The "kappa paradoxes":** κ can be low despite high accuracy when the marginals are very skewed or very asymmetric. Two confusion matrices with identical accuracy can have very different κ. This is a genuine, well-documented weakness (Feinstein & Cicchetti, 1990) and worth knowing by name.
- **Depends on the marginal distributions**, so κ is not comparable across datasets with different prevalence.
- `p_e` assumes the two raters guess **independently** according to their own marginals, which is a debatable model of chance.
- Threshold-dependent; requires hard labels.
- Cannot express asymmetric costs.
- Less intuitive than precision/recall for business audiences.
- The Landis-Koch bands are arbitrary conventions.

### 11. Common mistakes
1. Comparing κ across datasets with different prevalence.
2. Using unweighted κ for an **ordinal** target — this throws away the ordering information and understates performance. Use QWK.
3. Treating the Landis-Koch bands as absolute standards.
4. Not knowing about the kappa paradoxes and being confused when κ is low while accuracy is high.
5. Confusing Cohen's Kappa (two raters, categorical) with Fleiss' Kappa (multiple raters) or Krippendorff's Alpha (missing data, any scale).

### 12. Interview questions

**Easy — What is Cohen's Kappa?** Agreement corrected for chance: `(p_o − p_e)/(1 − p_e)`.
**Easy — What does κ = 0 mean?** The model agrees with the truth no more than chance would predict.

**Medium — Kappa vs accuracy?** Accuracy is `p_o` alone. Kappa subtracts the chance agreement `p_e` and rescales by the maximum achievable improvement. On imbalanced data `p_e` is large, so κ is much lower than accuracy — correctly so.

**Medium — Kappa vs MCC?** Both are chance-corrected, use all four cells, and range roughly −1 to +1; on our example they are 0.571 and 0.577. MCC is a true correlation coefficient and is symmetric in a stronger sense; Kappa is more established for ordinal targets (via weighting) and for inter-rater reliability. Some literature argues MCC is better behaved because it is less affected by the kappa paradoxes. In practice they usually agree, and MCC is the safer default for binary ML while weighted Kappa is the right tool for ordinal problems.

**Medium — What is QWK and when do you use it?** Quadratic Weighted Kappa: Kappa where each disagreement is penalised by the squared distance between the predicted and true categories. Use it for **ordinal** targets — severity grades, star ratings, essay scores — where being off by one grade is much less bad than being off by three.

**Hard — Explain the kappa paradox.**
Kappa can be low even when accuracy is high, and can differ sharply between two matrices with identical accuracy, because `p_e` depends on the marginals. Example: a matrix with TP=45, FN=15, FP=25, TN=15 has accuracy 0.60 and κ ≈ 0.13; another with TP=25, FN=35, FP=5, TN=35 also has accuracy 0.60 but κ ≈ 0.26. Symmetric, balanced marginals give a lower `p_e` and hence a higher κ for the same accuracy. Practical consequence: κ should not be compared across datasets or across models with very different prediction rates, and it should always be reported alongside the confusion matrix and accuracy so a reader can see the marginals. Knowing this by name marks you as having read the methodological literature.

**Hard — Human annotators agree at κ = 0.65 on your labelling task. Your model achieves κ = 0.62 against the gold labels. How do you interpret that?**
The model is performing at approximately human-expert level: its agreement with the gold standard is within noise of the agreement two experts reach with each other. This is effectively the **ceiling** for the task as labelled — you cannot reliably exceed the consistency of the labelling process itself, because the residual disagreement is genuine label noise rather than model error. The correct next steps are not more modelling but: improve the label guidelines, use multi-annotator consensus labels, or reframe the task (e.g. coarser categories) to raise the ceiling. Presenting a result this way is far more persuasive to domain experts than quoting an F1 score.

---

## 10.3 REVISITING BALANCED ACCURACY AND G-MEAN FOR IMBALANCE

Both metrics are covered in full in Parts 4.5 and 4.6. Here is the imbalance-specific comparison, because interviewers frequently ask you to distinguish them.

| | Balanced Accuracy | G-Mean |
|---|---|---|
| Formula | (Sens + Spec)/2 | √(Sens × Spec) |
| Mean type | Arithmetic | Geometric |
| Our example | 0.8125 | 0.8101 |
| All-majority model | **0.50** | **0.00** |
| Penalty for neglecting a class | Moderate | **Severe** |
| Chance baseline | 0.5 | Not fixed (0 for degenerate) |
| In sklearn | Yes | No (imbalanced-learn) |
| Best for | Accuracy-like reporting on imbalanced data | Forbidding class neglect outright |

**The key distinguishing fact:** for an all-majority-class model, balanced accuracy is 0.5 but **G-Mean is exactly 0**. If your requirement is "the model must not ignore the minority class," G-Mean enforces it more strictly, because the geometric mean is zero if any factor is zero.

**Neither metric sees false-alarm volume.** Both use specificity, whose denominator is the huge negative class. So both can look good while precision is dreadful. On a 1%-prevalence problem, always add PR-AUC or precision@k.

---

## 10.4 YOUDEN'S INDEX (Youden's J Statistic)

### 1. Definition
`J = Sensitivity + Specificity − 1`. Equivalently `J = TPR − FPR`.

### 2. Intuition
J measures **how far above the random-guess diagonal a given ROC point sits**, vertically. It answers: *"how much better than a coin flip is this specific operating point?"*

Its main practical purpose is **choosing a threshold**: the threshold that maximises J is the point on the ROC curve furthest above the diagonal, which is the classic "closest to the top-left corner" cut-off. Because it weights sensitivity and specificity equally, it is the correct choice **only when FP and FN cost the same.**

Introduced by W.J. Youden in 1950 for rating the performance of diagnostic tests.

### 3. Formula
```
J = Sensitivity + Specificity − 1
  = TPR − FPR
  = TP/(TP+FN)  +  TN/(TN+FP)  −  1
```
- Range **−1 to +1**; 0 = no better than chance; 1 = perfect.
- **Identity 1:** `J = 2 × Balanced Accuracy − 1`. So J is simply balanced accuracy rescaled so that chance = 0.
- **Identity 2:** `max over thresholds of J = KS statistic`. Youden's J at its optimum *is* the KS statistic.
- **Identity 3:** `J = adjusted balanced accuracy` (sklearn's `balanced_accuracy_score(..., adjusted=True)`).

Three metrics, one quantity — knowing this saves you from double-counting evidence and is a satisfying interview answer.

### 4. Manual example

```
Sensitivity = 15/20 = 0.750
Specificity = 70/80 = 0.875
J = 0.750 + 0.875 − 1 = 1.625 − 1 = 0.625

Cross-checks:
  J = TPR − FPR = 0.750 − 0.125 = 0.625  ✓
  J = 2 × Balanced Accuracy − 1 = 2(0.8125) − 1 = 0.625  ✓
  J = balanced_accuracy_score(y_true, y_pred, adjusted=True) = 0.625  ✓
```
**Youden's J = 0.625.**

**Using J to pick a threshold** (on the 20-sample ranking data from 6.0): the KS table in 6.10 shows `max(TPR − FPR) = 0.5417` at threshold **0.45**. That is the J-optimal threshold, and the corresponding operating point is TPR 0.875 / FPR 0.333.

### 5. Python

```python
import numpy as np
from sklearn.metrics import roc_curve, confusion_matrix, balanced_accuracy_score

# From a fixed confusion matrix
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
J = tp/(tp+fn) + tn/(tn+fp) - 1                          # 0.625
J = balanced_accuracy_score(y_true, y_pred, adjusted=True) # 0.625  (same thing)

# Finding the J-optimal threshold from scores
fpr, tpr, thr = roc_curve(y, scores)
j_scores      = tpr - fpr
best_idx      = np.argmax(j_scores)
print(f"Best J = {j_scores[best_idx]:.4f} at threshold {thr[best_idx]:.3f}")
# Best J = 0.5417 at threshold 0.450
```
- The three-line threshold-selection recipe (`roc_curve` → `tpr - fpr` → `argmax`) is worth memorising; it is a common live-coding request.

### 6. Interpretation

| J | Meaning |
|---|---|
| 0.00 | No better than chance |
| 0.20 | Weak |
| 0.40 | Moderate |
| 0.625 | Good — our example |
| 0.80 | Strong |
| 1.00 | Perfect |

Because chance is anchored at 0, J is easier to read than balanced accuracy for the question "is this model doing anything at all?"

### 7. Good vs bad values
Poor < 0.20, Average 0.20–0.40, Good 0.40–0.60, Excellent > 0.60. In diagnostics, a test with J below about 0.3 is rarely clinically useful on its own.

### 8. Business use cases
- **Diagnostic test evaluation and cut-off selection** — the original and still primary use; ubiquitous in medical literature.
- **Threshold selection for any binary classifier when FP and FN costs are comparable.**
- **Credit scoring cut-off selection** (equivalently via KS).
- **Screening programme design** — selecting the referral threshold.
- **Comparing operating points** of two models at their respective best thresholds.
- **Quality control** cut-off setting.

### 9. Advantages
- **Chance-anchored at 0**, unlike balanced accuracy.
- Gives you a **concrete threshold**, not just a score — most metrics do not.
- Uses both classes' performance.
- Prevalence-independent (both components are row ratios).
- Trivially computed from an ROC curve.
- Long-established and expected in medical contexts.

### 10. Limitations
- **Assumes FP and FN cost equally.** This is the central limitation. If a miss costs 50× a false alarm, the J-optimal threshold is far from optimal — you need the cost-weighted tangency condition instead (see 3.6 and Part 11).
- **Ignores prevalence in decision-making**, so the J-optimal threshold can produce dreadful precision on rare-event problems.
- A single point on the ROC curve — ignores the rest of the curve, so it is a poor model-comparison metric compared to AUC.
- The J-optimal threshold can be operationally impossible (flagging 40% of the population when capacity is 2%).
- Redundant with KS and adjusted balanced accuracy; reporting all three is padding.

### 11. Common mistakes
1. **Using the J-optimal threshold in production without a cost analysis.** By far the most consequential mistake here. It is the right threshold only under equal costs.
2. Reporting J, KS, and adjusted balanced accuracy as three separate pieces of evidence.
3. Applying J-based threshold selection on a rare-event problem and being surprised at 5% precision.
4. Confusing Youden's J with the Jaccard index (both sometimes abbreviated "J").

### 12. Interview questions
**Easy — What is Youden's J?** `Sensitivity + Specificity − 1`, equivalently `TPR − FPR`.
**Easy — What does J = 0 mean?** Chance-level performance.
**Medium — How is J related to KS and to balanced accuracy?** `J = 2 × BalancedAccuracy − 1`, and `KS = max over thresholds of J`. All three are the same underlying quantity, differently packaged.
**Medium — How do you use J to pick a threshold?** Compute the ROC curve, evaluate `tpr − fpr` at every threshold, and take the argmax. That is the point furthest above the diagonal.
**Hard — When is the J-optimal threshold the wrong threshold?**
Whenever misclassification costs are asymmetric or capacity is constrained. J implicitly assumes `C_FP = C_FN` and ignores prevalence. The cost-optimal threshold satisfies the tangency condition where the ROC slope equals `(C_FP × N_neg)/(C_FN × N_pos)`; equivalently, for calibrated probabilities, `t* = C_FP/(C_FP + C_FN)`. For fraud where a miss costs $500 and a review costs $5, `t* ≈ 0.01`, far below the J point. And if the fraud team can review only 200 cases a day, the binding constraint is capacity, so the correct threshold is the 200th-highest score — a quantile, not a cost calculation. Always state which regime you are in.

---

## 10.5 DIAGNOSTIC ODDS RATIO (DOR)

### 1. Definition
The ratio of the odds of a positive test result in someone who has the condition, to the odds of a positive test result in someone who does not.

### 2. Intuition
DOR compresses a whole diagnostic test into **one number that does not depend on prevalence**: *"how many times more likely is a positive result if you truly have the condition?"*

It is built from the two **likelihood ratios** that clinicians use for Bayesian bedside reasoning:
- **LR+ = Sensitivity / (1 − Specificity)** — how much a positive result raises the odds of disease
- **LR− = (1 − Sensitivity) / Specificity** — how much a negative result lowers the odds
- **DOR = LR+ / LR−**

DOR = 1 means the test is useless (a positive result is equally likely either way). Higher is better, with no upper bound.

### 3. Formula
```
        TP × TN         TP/FN       LR+
DOR = ----------- = ----------- = -------
        FP × FN         FP/TN       LR−
```
- **TP × TN** = the product of correct calls; **FP × FN** = the product of errors
- Range **0 to ∞**; **1 = no diagnostic value**; below 1 = the test is inverted
- Note the numerator and denominator are exactly the two terms in MCC's numerator — MCC is a normalised difference of these products, DOR is their ratio
- Undefined if FP = 0 or FN = 0 (add 0.5 to each cell — the Haldane-Anscombe correction — to stabilise it)

### 4. Manual example

```
TP = 15, TN = 70, FP = 10, FN = 5

Method 1 — direct:
  DOR = (TP × TN)/(FP × FN) = (15 × 70)/(10 × 5) = 1050/50 = 21.0

Method 2 — via likelihood ratios:
  Sensitivity = 0.750,  Specificity = 0.875
  LR+ = 0.750 / (1 − 0.875) = 0.750/0.125 = 6.0
  LR− = (1 − 0.750)/0.875   = 0.250/0.875 = 0.2857
  DOR = 6.0 / 0.2857 = 21.0  ✓
```
**DOR = 21.** A positive result is 21 times more likely in a diseased person than in a healthy one.

The likelihood ratios are individually very useful and clinicians prefer them:
- **LR+ = 6.0** → a positive result multiplies the pre-test odds of disease by 6.
- **LR− = 0.286** → a negative result multiplies the pre-test odds by 0.29 (a ~71% reduction in odds).

**Bayesian worked example.** Pre-test probability 20% → pre-test odds = 0.20/0.80 = 0.25.
```
Positive result: post-test odds = 0.25 × 6.0 = 1.5   -> probability = 1.5/2.5  = 0.60  (= PPV ✓)
Negative result: post-test odds = 0.25 × 0.286 = 0.0714 -> probability = 0.0714/1.0714 = 0.0667 (= 1 − NPV ✓)
```
Both match the PPV (0.60) and NPV (0.9333) computed in Part 3 — a satisfying consistency check, and a great thing to demonstrate in an interview.

### 5. Python

```python
import numpy as np
from sklearn.metrics import confusion_matrix

tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

dor = (tp * tn) / (fp * fn)                    # 21.0
sens, spec = tp/(tp+fn), tn/(tn+fp)
lr_pos = sens / (1 - spec)                     # 6.0
lr_neg = (1 - sens) / spec                     # 0.2857
dor    = lr_pos / lr_neg                       # 21.0

# Haldane-Anscombe correction for zero cells
dor_corrected = ((tp+0.5)*(tn+0.5)) / ((fp+0.5)*(fn+0.5))

# Confidence interval (log scale, since log(DOR) is approximately normal)
se_log = np.sqrt(1/tp + 1/tn + 1/fp + 1/fn)
ci = (np.exp(np.log(dor) - 1.96*se_log), np.exp(np.log(dor) + 1.96*se_log))
print(f"DOR = {dor:.1f}, 95% CI ({ci[0]:.1f}, {ci[1]:.1f})")
```
- Not available in sklearn; the four-line computation above is the whole thing.
- **Always report a confidence interval.** DOR is a ratio of products of possibly-small counts, so it is highly unstable. `log(DOR)` is approximately normal with standard error `√(1/TP + 1/TN + 1/FP + 1/FN)`, which is why the CI is computed on the log scale and exponentiated back.

### 6. Interpretation

| DOR | Meaning |
|---|---|
| 1 | The test carries **no** diagnostic information |
| 2–5 | Weak |
| 5–20 | Moderate |
| **21** | Our example — moderate-to-good |
| 20–100 | Good |
| > 100 | Excellent |
| < 1 | Inverted — flip the test |

Likelihood-ratio conventions used clinically:
- **LR+ > 10** → a positive result is strong evidence for the condition
- **LR− < 0.1** → a negative result is strong evidence against it
- LR+ between 1 and 2 or LR− between 0.5 and 1 → the result barely changes anything

### 7. Good vs bad values
Poor < 5, Average 5–20, Good 20–100, Excellent > 100. Because DOR is a product of ratios it grows very fast: a test with sensitivity and specificity both 0.99 has DOR = 9,801.

### 8. Business use cases
- **Diagnostic test accuracy meta-analyses** — DOR is the standard summary effect size, because it is a single prevalence-independent number that can be pooled across studies with different populations. This is its main reason for existing.
- **Regulatory submissions** for in-vitro diagnostic devices.
- **Clinical decision support:** likelihood ratios let a clinician update a patient's individual pre-test probability, which is genuinely how diagnosis works.
- **Screening programme comparison** across populations with different prevalence.
- **Epidemiology and biostatistics** generally.
- Occasionally in **fraud and credit** as an odds-based summary, since finance already thinks in odds (the log-odds scale is the basis of scorecard points).

### 9. Advantages
- **Prevalence-independent** → poolable across studies and populations. This is the property that makes it the meta-analysis standard.
- Single number summarising both sensitivity and specificity.
- Decomposes into LR+ and LR−, which support proper Bayesian updating of individual patient risk.
- Natural in odds-based domains (medicine, finance).
- Has well-developed statistical theory (log-normal CIs, regression models for meta-analysis).

### 10. Limitations
- **Unbounded and highly unstable** — dominated by small cells; a single FP or FN changing can move it substantially.
- **Undefined with any zero cell**, requiring a continuity correction.
- **Not intuitive** to most audiences; "DOR = 21" means nothing without explanation.
- **Loses the sensitivity/specificity trade-off:** a test with Sens 0.99/Spec 0.50 and one with Sens 0.50/Spec 0.99 can have similar DOR but completely different clinical uses (rule-out vs rule-in). **This is the most important limitation** — DOR should never be the only thing reported.
- Prevalence-independence means it tells you nothing about PPV, which is what patients care about.
- Threshold-dependent.
- Rarely used in mainstream ML, so it will need explaining.

### 11. Common mistakes
1. **Reporting DOR alone.** It must be accompanied by sensitivity and specificity, because two very different tests can share a DOR.
2. Omitting the confidence interval, given how unstable the statistic is.
3. Dividing by zero when FP or FN is 0 — apply the +0.5 correction.
4. Confusing DOR with the odds ratio from a logistic regression (a coefficient's exponentiated value), or with the relative risk. Different quantities.
5. Interpreting DOR as a probability.

### 12. Interview questions
**Easy — What is the diagnostic odds ratio?** `(TP × TN)/(FP × FN)`; the ratio of the odds of a positive test in the diseased versus the healthy.
**Easy — What DOR means the test is useless?** 1.
**Medium — What are LR+ and LR−, and why do clinicians prefer them?** `LR+ = Sens/(1−Spec)` and `LR− = (1−Sens)/Spec`. They allow Bayesian updating of an *individual* patient's pre-test odds — multiply the pre-test odds by the LR to get the post-test odds. That is directly actionable at the bedside in a way that a single summary statistic is not.
**Medium — Why is DOR used in meta-analyses?** Because it is prevalence-independent, so results from studies conducted in populations with very different disease prevalence can be pooled without confounding.
**Hard — What is DOR's biggest weakness?**
It collapses the sensitivity/specificity trade-off into one number, so it cannot distinguish a rule-out test from a rule-in test. Sens 0.95/Spec 0.60 gives DOR = (0.95/0.05)/(0.40/0.60) = 19/0.667 = 28.5; Sens 0.60/Spec 0.95 gives (0.60/0.40)/(0.05/0.95) = 1.5/0.0526 = 28.5. **Identical DOR, opposite clinical use** — the first is a screening test, the second a confirmatory test. Always report sensitivity and specificity alongside.

---

## 10.6 DICE COEFFICIENT (Sørensen-Dice, F1 for sets)

### 1. Definition
Twice the size of the intersection of two sets, divided by the sum of their sizes.

### 2. Intuition
Dice is the **set-overlap twin of the F1 score** — and in fact, for binary classification, **Dice = F1 exactly**. The two were derived independently: F1 in information retrieval, Dice in 1940s ecology (for comparing species assemblages between sites) and later adopted by medical image analysis.

The `2 ×` in the numerator exists to make a perfect match score 1: without it, identical sets of size n would give `n/2n = 0.5`.

In image segmentation, Dice answers: **"how much of the predicted region and the true region overlap, relative to their combined area?"** It is the dominant metric in medical image segmentation, where it is used to compare an algorithm's tumour or organ delineation against a radiologist's.

### 3. Formula
```
              2 × | A ∩ B |                    2 × TP
Dice = ------------------------- = -------------------------------
              | A | + | B |          2 × TP + FP + FN
```
- **A** = set of true positive elements (pixels, voxels, labels); **B** = set of predicted positive elements
- **|A ∩ B|** = the overlap = **TP**
- **|A| + |B|** = `(TP + FN) + (TP + FP)` = `2TP + FP + FN`. Note the intersection is counted **twice** in this sum, which is why the numerator needs the factor of 2.
- Range [0, 1]; 1 = perfect overlap; 0 = no overlap.
- **TN does not appear** → Dice is unaffected by the size of the background, which is exactly why it is used for segmentation, where background pixels typically outnumber the target region 1000:1.

**Relationship to Jaccard/IoU:**
```
           2J                          D
Dice = ----------      and      J = --------
          1 + J                      2 − D
```
Dice ≥ Jaccard always, with equality only at 0 and 1. They rank models identically.

**Soft Dice** (used as a training loss) replaces the counts with sums of predicted probabilities, making it differentiable:
```
                    2 × Σ pᵢ yᵢ  +  ε
Soft Dice = ------------------------------------
                Σ pᵢ + Σ yᵢ  +  ε
```
The `ε` (smoothing constant) prevents division by zero on empty masks.

### 4. Manual example

**Binary running example** (TP=15, FP=10, FN=5):
```
Step 1: 2 × TP = 2 × 15 = 30
Step 2: 2 × TP + FP + FN = 30 + 10 + 5 = 45
Step 3: Dice = 30 / 45 = 0.6667
```
**Dice = 0.6667 — identical to F1 = 0.6667.** ✓

Compare with Jaccard on the same data = 0.5000. Check the conversion: `Dice = 2(0.5)/(1+0.5) = 1.0/1.5 = 0.6667` ✓.

**Segmentation example.** A tumour occupies 1,000 pixels in the ground-truth mask; the model predicts a 1,200-pixel region; 900 pixels overlap.
```
TP = 900, FP = 1200 − 900 = 300, FN = 1000 − 900 = 100
Dice    = 2(900) / (2(900) + 300 + 100) = 1800/2200 = 0.8182
Jaccard = 900 / (900 + 300 + 100)       = 900/1300  = 0.6923
```
Note the image might contain 500,000 background pixels; **neither metric changes**, because TN is absent from both. If you used accuracy here it would be `(900 + 499,600)/501,800 = 0.9976` — meaningless.

### 5. Python

```python
import numpy as np
from sklearn.metrics import f1_score

def dice_coefficient(y_true, y_pred, eps=1e-7):
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()
    intersection = np.sum(y_true * y_pred)
    return (2.0 * intersection + eps) / (np.sum(y_true) + np.sum(y_pred) + eps)

dice_coefficient(y_true, y_pred)     # 0.6667
f1_score(y_true, y_pred)             # 0.6667   <- identical

# Soft Dice loss for training a segmentation network (PyTorch sketch)
# def soft_dice_loss(probs, targets, eps=1.0):
#     num = 2 * (probs * targets).sum(dim=(2,3)) + eps
#     den = probs.sum(dim=(2,3)) + targets.sum(dim=(2,3)) + eps
#     return 1 - (num / den).mean()
```
- `.ravel()` flattens 2-D masks so the same function works for images and label vectors.
- `eps` prevents `0/0` when both masks are empty — an important edge case in segmentation, where many slices contain no tumour at all.
- In multi-class segmentation, compute Dice per class and average (**mean Dice**), usually excluding the background class.

### 6. Interpretation

| Dice | Meaning (segmentation context) |
|---|---|
| < 0.50 | Poor overlap; often clinically unusable |
| 0.50 – 0.70 | Fair; needs manual correction |
| 0.70 – 0.80 | Good; typical of a decent automated segmentation |
| 0.80 – 0.90 | Very good; approaching inter-rater agreement for many organs |
| > 0.90 | Excellent; typically only achievable for large, well-defined structures |

**Crucial context:** two expert radiologists segmenting the same tumour typically agree at Dice 0.80–0.90. **A model reaching Dice 0.85 has effectively reached the human-agreement ceiling** — the same argument as with Cohen's Kappa in 10.2. Always report inter-rater Dice as the benchmark rather than aiming naively at 1.0.

### 7. Good vs bad values
Highly structure-dependent. Large organs (liver, lungs) routinely reach Dice > 0.95. Small or diffuse structures (small lesions, multiple sclerosis plaques, thin vessels) may only reach 0.60–0.70 even for state-of-the-art models, because a few boundary pixels are a large fraction of a small object. **Never compare Dice across different anatomical targets.**

### 8. Business use cases
- **Medical image segmentation** — the dominant metric: tumour delineation, organ-at-risk contouring for radiotherapy planning, brain lesion segmentation, cardiac chamber segmentation.
- **Radiotherapy treatment planning** — regulatory and clinical acceptance criteria are often stated as Dice thresholds.
- **Digital pathology** — nuclei and gland segmentation.
- **Satellite / remote sensing** — building footprint, road, and land-cover extraction.
- **Autonomous driving** — semantic segmentation of drivable area (though mIoU is more common there).
- **Industrial defect segmentation** — locating scratches or cracks on surfaces.
- **Ecology** — the original 1940s use, comparing species composition between sites.
- **Training loss** — soft Dice loss is standard in medical segmentation (often combined with cross-entropy) precisely because it handles the extreme foreground/background imbalance that plain cross-entropy struggles with.

### 9. Advantages
- **Ignores TN** → immune to background dominance, which is the defining problem in segmentation.
- Intuitive geometric overlap interpretation; easy to visualise.
- Identical to F1, so all F1 intuition transfers.
- **Differentiable in its soft form**, so it can be used directly as a training loss — a rare and valuable property for an overlap metric.
- Established clinical acceptance thresholds exist for many tasks.
- More forgiving than Jaccard, which makes reported numbers look reasonable while ranking models identically.

### 10. Limitations
- **Ignores the spatial nature of errors.** A prediction that misses 100 pixels scattered around the boundary and one that misses a 100-pixel solid chunk in the centre score identically, yet the second may be clinically far worse. Boundary-aware metrics (**Hausdorff distance**, **average surface distance**) are reported alongside Dice for exactly this reason.
- **Unstable for small objects.** For a 20-pixel lesion, being off by 5 pixels drops Dice to ~0.78; for a 20,000-pixel organ, being off by 5 pixels is invisible. So Dice systematically penalises small-object performance.
- **Undefined for empty masks** (both true and predicted empty) — needs a convention, and how you handle empty slices can materially change reported mean Dice. A known source of non-comparability between papers.
- Treats FP and FN symmetrically, whereas over-segmenting a tumour (safe) and under-segmenting it (dangerous) have very different clinical consequences.
- Not comparable across structures or datasets.
- Ignores calibration and confidence.

### 11. Common mistakes
1. **Comparing Dice values across different organs, lesion sizes, or datasets.** The single most common error in segmentation reporting.
2. Reporting Dice without inter-rater agreement as the ceiling.
3. Reporting Dice without a boundary metric (Hausdorff / surface distance), thereby hiding spatially catastrophic errors.
4. Inconsistent handling of empty masks (excluding them, scoring them 0, or scoring them 1) — always state the convention.
5. Confusing Dice with Jaccard/IoU when comparing to published results. Dice is always the higher number; mixing them makes a model look better or worse than it is.
6. Averaging Dice over pixels rather than over cases (**global vs per-case Dice** give different answers; per-case is standard in medical imaging, and global Dice can hide total failure on small cases).

### 12. Interview questions
**Easy — What is the Dice coefficient?** `2 × |A∩B| / (|A| + |B|)` = `2TP/(2TP+FP+FN)`.
**Easy — How does Dice relate to F1?** They are the same formula. Dice = F1 for binary classification.
**Medium — Dice vs IoU/Jaccard: which is larger and why?** Dice ≥ Jaccard always. Dice counts the intersection twice in its numerator while Jaccard's denominator counts the union once; algebraically `Dice = 2J/(1+J)`. They are monotonically related, so they rank models identically — the choice is convention only (medical imaging prefers Dice; general computer vision prefers IoU).
**Medium — Why is Dice preferred over accuracy for segmentation?** Because background pixels typically outnumber the target by orders of magnitude, so pixel accuracy is ~0.99 even for a model that predicts no foreground at all. Dice excludes TN and therefore cannot be inflated by the background.
**Hard — Why report Hausdorff distance alongside Dice?**
Dice is a *volumetric overlap* metric and is blind to the geometry of errors. A segmentation with excellent Dice can contain a small spurious island of predicted tissue far from the true structure, or can miss a thin critical extension — errors that matter enormously in radiotherapy planning, where a missed tumour margin means under-dosing, or a spurious region near the spinal cord means over-dosing an organ at risk. **Hausdorff distance** measures the worst-case boundary deviation, and **average surface distance** measures the typical deviation. Together with Dice they characterise both how much and where the model is wrong. The 95th-percentile Hausdorff distance is usually preferred over the raw maximum because the raw maximum is dominated by single outlier voxels.
**Hard — Why is soft Dice used as a loss function instead of cross-entropy for segmentation?**
Cross-entropy averages over pixels, so with 99.8% background pixels the gradient is dominated by background and the model converges to predicting empty masks. Soft Dice's denominator scales with the size of the predicted and true foreground, making the loss inherently normalised by object size, so small structures produce gradients comparable to large ones. In practice a **combined loss** (Dice + cross-entropy) is standard: cross-entropy provides stable, well-behaved gradients early in training and per-pixel calibration, while Dice provides the imbalance-robust overlap objective. Pure Dice loss can be unstable early on because the denominator is near zero when predictions are near zero.

---

## 10.7 JACCARD INDEX (as an advanced metric)

The Jaccard index is covered in full in **Part 9.3**, since its primary modern use is multi-label and segmentation evaluation. The essentials for this Part:

```
Jaccard = TP / (TP + FP + FN)
Running example: 15 / (15 + 10 + 5) = 15/30 = 0.5000
```

**Its place among the advanced metrics:**

| | Jaccard / IoU | Dice / F1 |
|---|---|---|
| Formula | TP/(TP+FP+FN) | 2TP/(2TP+FP+FN) |
| Our example | 0.5000 | 0.6667 |
| Range | [0,1] | [0,1] |
| Relationship | `J = D/(2−D)` | `D = 2J/(1+J)` |
| Always | Jaccard ≤ Dice | Dice ≥ Jaccard |
| Ranks models | Identically | Identically |
| Field convention | Computer vision, IR, multi-label | Medical imaging, NLP (as F1) |
| Uses TN | No | No |

**The one thing to remember:** they are monotonically equivalent, so no model comparison ever changes between them — but the *numbers* differ substantially, so **never mix them when citing results.** If a paper reports mIoU 0.70 and yours reports Dice 0.78, you may be reporting an identical model.

**Interview (Medium) — If Dice and Jaccard always rank models the same way, why do both exist?** Historical field convention. Jaccard (1901, plant ecology) came first; Dice/Sørensen (1945–48) independently proposed the doubled form, which was later found to coincide with the F1 score from information retrieval. Medical imaging adopted Dice; general computer vision adopted IoU. Dice is more forgiving numerically, which arguably made it more appealing for reporting clinical results. There is no mathematical reason to prefer one.

---

## 10.8 All advanced metrics on the running example

Single reference table. All values from TP=15, TN=70, FP=10, FN=5, N=100, prevalence=0.20.

| Metric | Formula | Calculation | Value |
|---|---|---|---|
| Accuracy | (TP+TN)/N | 85/100 | 0.8500 |
| Error Rate | (FP+FN)/N | 15/100 | 0.1500 |
| Precision / PPV | TP/(TP+FP) | 15/25 | 0.6000 |
| Recall / Sens / TPR | TP/(TP+FN) | 15/20 | 0.7500 |
| Specificity / TNR | TN/(TN+FP) | 70/80 | 0.8750 |
| FPR | FP/(FP+TN) | 10/80 | 0.1250 |
| FNR | FN/(FN+TP) | 5/20 | 0.2500 |
| NPV | TN/(TN+FN) | 70/75 | 0.9333 |
| F1 / Dice | 2TP/(2TP+FP+FN) | 30/45 | 0.6667 |
| F2 | 5PR/(4P+R) | 2.25/3.15 | 0.7143 |
| F0.5 | 1.25PR/(0.25P+R) | 0.5625/0.90 | 0.6250 |
| G-Mean | √(Sens×Spec) | √0.65625 | 0.8101 |
| Balanced Accuracy | (Sens+Spec)/2 | 1.625/2 | 0.8125 |
| Youden's J / adj. BA | Sens+Spec−1 | 1.625−1 | 0.6250 |
| MCC | (TP·TN−FP·FN)/√(marginals) | 1000/1732.05 | 0.5774 |
| Cohen's Kappa | (p_o−p_e)/(1−p_e) | 0.20/0.35 | 0.5714 |
| Jaccard / IoU | TP/(TP+FP+FN) | 15/30 | 0.5000 |
| DOR | (TP·TN)/(FP·FN) | 1050/50 | 21.0 |
| LR+ | Sens/(1−Spec) | 0.75/0.125 | 6.0 |
| LR− | (1−Sens)/Spec | 0.25/0.875 | 0.2857 |
| Prevalence | (TP+FN)/N | 20/100 | 0.2000 |

**The lesson of this table:** one model, one confusion matrix, twenty-one numbers ranging from 0.125 to 21. **The metric you choose is the story you tell.** Choose it from the business problem, before you train, and report a small honest dashboard rather than the single most flattering figure.

---

# PART 11 — Threshold Selection

## 11.1 Why changing the threshold changes every metric

Your model does not output a class. It outputs a **score** (a probability, usually). The class comes from a comparison:

```
if score >= threshold:  predict Positive
else:                   predict Negative
```

**The threshold is a business decision, not a model output.** The default 0.5 is a convention inherited from `predict()` implementations, not a principled choice. On imbalanced data it is almost always wrong.

**What happens mechanically when you LOWER the threshold:**
- More samples are flagged positive.
- Some newly-flagged samples are real positives → **TP increases, FN decreases** → **Recall goes UP** (it can never go down).
- Some newly-flagged samples are negatives → **FP increases, TN decreases** → **Specificity goes DOWN, FPR goes UP**.
- **Precision usually goes down** but is non-monotonic (it jumps up whenever the next-added sample happens to be a positive).

**Raising the threshold does the exact reverse.** So:

| Metric | Lower threshold | Raise threshold | Monotonic? |
|---|---|---|---|
| Recall / TPR / Sensitivity | ↑ Always increases | ↓ Always decreases | **Yes** |
| FNR | ↓ Decreases | ↑ Increases | **Yes** |
| FPR | ↑ Increases | ↓ Decreases | **Yes** |
| Specificity / TNR | ↓ Decreases | ↑ Increases | **Yes** |
| Precision / PPV | ↓ Generally decreases | ↑ Generally increases | **No** (sawtooth) |
| NPV | ↑ Generally increases | ↓ Generally decreases | No |
| Accuracy | Peaks somewhere in the middle | Peaks somewhere in the middle | No |
| F1 / F-beta | Peaks somewhere in the middle | Peaks somewhere in the middle | No |
| MCC, Kappa, Balanced Acc, G-Mean, J | Peak somewhere in the middle | Peak somewhere in the middle | No |
| **ROC-AUC, PR-AUC, AP, Log Loss, Brier** | **Unchanged** | **Unchanged** | **N/A — threshold-free** |

That last row is the most important. **Threshold tuning cannot change AUC or Log Loss.** If you need better AUC you need a better model; if you need better precision/recall balance you need a better threshold. Confusing these two levers wastes enormous amounts of time.

## 11.2 Worked threshold sweep (using the 20-sample ranking data from 6.0)

Recall the data: 8 positives, 12 negatives, prevalence 0.40.

### Threshold = 0.2 — very aggressive

Flag everything with score ≥ 0.2, i.e. the top 16 samples.
```
TP = 8   FP = 8   FN = 0   TN = 4

Precision   = 8/16  = 0.5000
Recall      = 8/8   = 1.0000
F1          = 2(0.5)(1.0)/(1.5)      = 0.6667
Specificity = 4/12  = 0.3333
FPR         = 8/12  = 0.6667
Accuracy    = (8+4)/20 = 0.6000
```
Catches every positive, but half of all alarms are false and two-thirds of the innocent are flagged.

### Threshold = 0.4

Flag the top 12 samples.
```
TP = 7   FP = 5   FN = 1   TN = 7

Precision   = 7/12  = 0.5833
Recall      = 7/8   = 0.8750
F1          = 2(0.5833)(0.875)/(1.4583) = 1.0208/1.4583 = 0.7000
Specificity = 7/12  = 0.5833
Accuracy    = (7+7)/20 = 0.7000
```
**This is the F1-optimal threshold for this data.**

### Threshold = 0.5 — the default

Flag the top 10 samples.
```
TP = 6   FP = 4   FN = 2   TN = 8

Precision   = 6/10  = 0.6000
Recall      = 6/8   = 0.7500
F1          = 2(0.6)(0.75)/(1.35)   = 0.6667
Specificity = 8/12  = 0.6667
Accuracy    = (6+8)/20 = 0.7000
```
Note that the default threshold gives a **worse F1** (0.667) than 0.4 (0.700). The default is not optimal even here.

### Threshold = 0.6

Flag the top 8 samples.
```
TP = 5   FP = 3   FN = 3   TN = 9

Precision   = 5/8   = 0.6250
Recall      = 5/8   = 0.6250
F1          = 0.6250
Specificity = 9/12  = 0.7500
Accuracy    = (5+9)/20 = 0.7000
```
The crossover point: precision = recall = F1 = 0.625.

### Threshold = 0.8 — very conservative

Flag the top 4 samples.
```
TP = 3   FP = 1   FN = 5   TN = 11

Precision   = 3/4   = 0.7500
Recall      = 3/8   = 0.3750
F1          = 2(0.75)(0.375)/(1.125) = 0.5625/1.125 = 0.5000
Specificity = 11/12 = 0.9167
Accuracy    = (3+11)/20 = 0.7000
```
Highly trustworthy alarms, but 5 of 8 real cases are missed.

### The complete sweep table

| Threshold | Flagged | TP | FP | FN | TN | **Precision** | **Recall** | F1 | Specificity | FPR | Accuracy |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **0.2** | 16 | 8 | 8 | 0 | 4 | **0.500** | **1.000** | 0.667 | 0.333 | 0.667 | 0.600 |
| **0.4** | 12 | 7 | 5 | 1 | 7 | **0.583** | **0.875** | **0.700** | 0.583 | 0.417 | 0.700 |
| **0.5** | 10 | 6 | 4 | 2 | 8 | **0.600** | **0.750** | 0.667 | 0.667 | 0.333 | 0.700 |
| **0.6** | 8 | 5 | 3 | 3 | 9 | **0.625** | **0.625** | 0.625 | 0.750 | 0.250 | 0.700 |
| **0.8** | 4 | 3 | 1 | 5 | 11 | **0.750** | **0.375** | 0.500 | 0.917 | 0.083 | 0.700 |

### Reading the table — the four lessons

**1. Precision and Recall move in opposite directions.** As the threshold rises from 0.2 to 0.8, precision climbs 0.500 → 0.750 while recall falls 1.000 → 0.375. This is the precision-recall trade-off, made concrete.

```
 1.0 |R
     | R
 0.9 |  R
     |    R                                    P
 0.8 |      R                            P
     |        R                    P
 0.7 |          R            P
     |            R    P
 0.6 |          P   R
     |      P         R
 0.5 |  P                R
     |                     R
 0.4 |                        R
     +--------------------------------------------
     0.2      0.4      0.5      0.6      0.8
                    THRESHOLD
     R = Recall (falls)      P = Precision (rises)
```

**2. F1 peaks in the middle.** F1 goes 0.667 → **0.700** → 0.667 → 0.625 → 0.500. The maximum is at threshold 0.4, not at the default 0.5. **Never assume 0.5 is F1-optimal.**

**3. Accuracy is nearly flat and therefore useless for choosing a threshold here.** It reads 0.700 at four of the five thresholds while precision and recall change dramatically. Accuracy cannot distinguish operationally different systems.

**4. Every row is a legitimate deployment.** Which one you pick depends entirely on cost:

| If your situation is… | Choose | Because |
|---|---|---|
| Cancer screening (a miss can be fatal) | **0.2** | Recall 1.00; the false positives get resolved by a confirmatory test |
| Fraud detection with a large review team | **0.4** | Recall 0.875 at acceptable precision |
| Balanced costs, no strong preference | **0.5–0.6** | Symmetric trade-off |
| Automated irreversible action (auto-block a card) | **0.8** | Precision 0.75; you cannot afford to block good customers |
| Analyst team can review only 4 cases/day | **0.8** | Capacity, not cost, is the binding constraint |

## 11.3 The four correct ways to choose a threshold

### Method 1 — Minimise expected cost (the gold standard when you have cost estimates)

```python
import numpy as np
from sklearn.metrics import roc_curve

C_FP = 5      # cost of investigating a false alarm (analyst time)
C_FN = 500    # cost of a missed fraud (loss + chargeback)

fpr, tpr, thr = roc_curve(y_true, y_scores)
n_pos, n_neg  = y_true.sum(), (1 - y_true).sum()

fp_count = fpr * n_neg
fn_count = (1 - tpr) * n_pos
cost     = C_FP * fp_count + C_FN * fn_count

best = np.argmin(cost)
print(f"Optimal threshold {thr[best]:.3f}, expected cost {cost[best]:.0f}")
```
For **calibrated** probabilities there is a closed form:
```
              C_FP
t* = -------------------
        C_FP + C_FN
```
With C_FP = 5 and C_FN = 500: `t* = 5/505 = 0.0099` — flag anything above about 1%. Note how far this is from 0.5, and note that **this formula is only valid if the model is calibrated** (Part 7). Uncalibrated scores make it meaningless.

### Method 2 — Satisfy a hard constraint

```python
# "We must catch at least 90% of fraud"
idx = np.argmax(tpr >= 0.90)
print(f"Threshold for recall>=0.90: {thr[idx]:.3f}, FPR = {fpr[idx]:.3f}")

# "Precision must be at least 0.30 or the team revolts"
from sklearn.metrics import precision_recall_curve
p, r, t = precision_recall_curve(y_true, y_scores)
ok = p[:-1] >= 0.30                    # note: p has one extra element
print(f"Best recall at precision>=0.30: {r[:-1][ok].max():.3f}")
```
This is usually the most defensible approach in a business setting, because the constraint comes from a stakeholder commitment rather than from a metric.

### Method 3 — Capacity constraint (top-k)

```python
# "The team can review 200 cases per day"
k = 200
threshold = np.sort(y_scores)[-k]      # the k-th highest score
```
When capacity is fixed, the threshold is a **quantile**, not a cost calculation. This is the reality in most alerting systems, and candidates who mention it stand out.

### Method 4 — Maximise a metric

```python
# Maximise F1 (or F2, MCC, Youden's J, ...)
from sklearn.metrics import f1_score
ts     = np.linspace(0.01, 0.99, 99)
scores_ = [f1_score(y_true, (y_scores >= t).astype(int)) for t in ts]
best_t  = ts[int(np.argmax(scores_))]

# Youden's J / KS point
best_j  = thr[np.argmax(tpr - fpr)]
```
Weakest of the four methods, because "maximise F1" is an implicit and usually unexamined cost assumption. Use it only when you genuinely have no cost or capacity information.

## 11.4 Threshold selection: rules and pitfalls

**Rules**
1. **Tune the threshold on validation data, never on test data.** Otherwise your reported metrics are optimistically biased. Threshold selection is a hyperparameter fit.
2. **Calibrate before applying a cost-based threshold.** `t* = C_FP/(C_FP + C_FN)` assumes true probabilities.
3. **Never resample the validation set used for threshold tuning** — the prevalence must match production, or precision-based constraints will be wrong.
4. **Re-tune when prevalence drifts.** The F1-optimal and cost-optimal thresholds both depend on prevalence. Monitor prevalence in production and alert on drift.
5. **Report the threshold with every threshold-based metric.** "F1 = 0.70" is incomplete; "F1 = 0.70 at threshold 0.40" is a result.
6. **In multi-class one-vs-rest, tune per-class thresholds.** A single global threshold is rarely right when class frequencies differ by orders of magnitude.

**Pitfalls**
1. Leaving the threshold at 0.5 on imbalanced data — the most common production defect in deployed classifiers.
2. Tuning the threshold on the test set and reporting the resulting metric.
3. Using the Youden/KS threshold when costs are asymmetric.
4. Using a cost-based threshold on uncalibrated scores (especially after SMOTE).
5. Tuning F1 and then being surprised when the alert volume exceeds analyst capacity — F1 has no notion of capacity.
6. Believing that threshold tuning improves the model. It moves you along the same PR curve; only better features, data, or algorithms move the curve itself.

**Interview (Hard) — How would you choose a threshold for a fraud model, end to end?**
(1) Establish costs with the business: average fraud loss per missed case, fully-loaded cost of an analyst investigation, and the customer-experience cost of a false block. (2) Establish capacity: how many alerts can be reviewed per day. (3) Calibrate the model on a held-out set that has production prevalence. (4) Compute expected cost across all thresholds and identify the cost-optimal point. (5) Check whether that point is feasible under capacity; if not, capacity binds and the threshold becomes the capacity quantile. (6) Verify the resulting precision and recall are acceptable to stakeholders and document them as the operating contract. (7) Monitor prevalence, precision, recall, and calibration in production, and re-tune on a schedule or on drift alerts. (8) Consider a **two-threshold** design: above t_high take automatic action, between t_low and t_high send to human review, below t_low ignore. This is how real fraud systems work and mentioning it demonstrates practical experience.

---

# PART 12 — Master Comparison Tables

## 12.1 Core reference table

| Metric | Purpose | Formula | Range | Best | Imbalance-sensitive? | Needs probabilities? | Threshold-dependent? |
|---|---|---|---|---|---|---|---|
| Accuracy | Overall correctness | (TP+TN)/N | 0–1 | 1 | **Yes, severely** | No | Yes |
| Error Rate | Overall wrongness | (FP+FN)/N | 0–1 | 0 | **Yes, severely** | No | Yes |
| Precision / PPV | Alarm trustworthiness | TP/(TP+FP) | 0–1 | 1 | Yes (prevalence-dependent) | No | Yes |
| Recall / Sens / TPR | Coverage of positives | TP/(TP+FN) | 0–1 | 1 | No | No | Yes |
| Specificity / TNR | Correctly clearing negatives | TN/(TN+FP) | 0–1 | 1 | No | No | Yes |
| FPR | False-alarm rate | FP/(FP+TN) | 0–1 | 0 | No | No | Yes |
| FNR | Miss rate | FN/(FN+TP) | 0–1 | 0 | No | No | Yes |
| NPV | "All clear" trustworthiness | TN/(TN+FN) | 0–1 | 1 | Yes (prevalence-dependent) | No | Yes |
| F1 / Dice | Balanced P/R summary | 2TP/(2TP+FP+FN) | 0–1 | 1 | Moderate (ignores TN) | No | Yes |
| F-beta | Weighted P/R summary | (1+β²)PR/(β²P+R) | 0–1 | 1 | Moderate | No | Yes |
| F0.5 | Precision-weighted | β=0.5 | 0–1 | 1 | Moderate | No | Yes |
| F2 | Recall-weighted | β=2 | 0–1 | 1 | Moderate | No | Yes |
| G-Mean | Both-class balance | √(Sens×Spec) | 0–1 | 1 | **No** | No | Yes |
| Balanced Accuracy | Imbalance-corrected accuracy | (Sens+Spec)/2 | 0–1 (0.5=chance) | 1 | **No** | No | Yes |
| MCC | Correlation, all 4 cells | (TP·TN−FP·FN)/√(marginals) | −1–1 | 1 | **No** | No | Yes |
| Cohen's Kappa | Chance-corrected agreement | (p_o−p_e)/(1−p_e) | −1–1 | 1 | **No** | No | Yes |
| Youden's J | Distance above ROC diagonal | Sens+Spec−1 | −1–1 | 1 | **No** | No | Yes |
| DOR | Diagnostic odds | (TP·TN)/(FP·FN) | 0–∞ (1=useless) | ∞ | **No** | No | Yes |
| Jaccard / IoU | Set overlap | TP/(TP+FP+FN) | 0–1 | 1 | Moderate (ignores TN) | No | Yes |
| Log Loss | Probability quality | −mean ln(p_true) | 0–∞ | 0 | Yes (baseline shifts) | **Yes** | **No** |
| Brier Score | Probability quality (MSE) | mean(p−y)² | 0–1 | 0 | Yes (baseline shifts) | **Yes** | **No** |
| ECE | Calibration gap | Σ w·\|acc−conf\| | 0–1 | 0 | Mildly | **Yes** | **No** |
| Hinge Loss | Margin violation | mean max(0,1−y·f) | 0–∞ | 0 | Yes | Needs decision scores | **No** |
| ROC-AUC | Ranking quality | ∫TPR d(FPR) | 0–1 (0.5=chance) | 1 | **No — and that's the flaw** | **Yes** | **No** |
| PR-AUC / AP | Ranking quality, positives | Σ(ΔR)·P | 0–1 (prev=chance) | 1 | **Yes — honestly so** | **Yes** | **No** |
| KS Statistic | Max class separation | max(TPR−FPR) | 0–1 | 1 | Partially (uses FPR) | **Yes** | Selects one |
| Lift@k | Times better than random | Precision@k / prevalence | 0–1/prev | 1/prev | Yes | **Yes** | Depth-based |
| Gain@k | Positives captured by depth k | cum. TP / total P | 0–1 | 1 | Yes | **Yes** | Depth-based |
| Hamming Loss | Wrong label slots | errors/(N×L) | 0–1 | 0 | **Yes, severely (sparse)** | No | Yes |
| Subset Accuracy | Exact label-set match | matches/N | 0–1 | 1 | Yes | No | Yes |

## 12.2 Best use case and business example

| Metric | Best use case | Business example |
|---|---|---|
| Accuracy | Balanced classes, symmetric costs | Balanced image classification benchmark |
| Error Rate | Reporting improvements, cost per error | Manufacturing defect escape rate; speech WER |
| Precision | False alarms are expensive | Spam filter (a lost job offer is unacceptable) |
| Recall | Misses are catastrophic | Cancer screening; AML suspicious-activity detection |
| Specificity | Protecting the healthy majority | Mass COVID screening in a low-prevalence population |
| FPR | Alert-fatigue budgeting | SOC intrusion detection; biometric FAR spec |
| FNR | Risk / safety cases | Missed-fraud rate × average loss = expected loss |
| NPV | Rule-out testing | D-dimer to safely exclude pulmonary embolism |
| F1 | Comparable costs, single number needed | NLP named entity recognition; Kaggle leaderboards |
| F2 | Misses cost more | Fraud detection; predictive maintenance |
| F0.5 | False alarms cost more | Auto-ban / auto-takedown pipelines |
| G-Mean | Both classes matter, imbalanced | Credit scoring; rare-defect detection |
| Balanced Accuracy | Accuracy-like reporting, imbalanced | Rare-disease diagnostics; skewed multi-class |
| MCC | Honest single number, binary | Bioinformatics; any imbalanced binary problem |
| Cohen's Kappa | Chance-corrected; ordinal via QWK | Inter-annotator agreement; retinopathy grading |
| Youden's J | Threshold selection, equal costs | Diagnostic test cut-off |
| DOR | Prevalence-independent test summary | Diagnostic accuracy meta-analysis |
| Jaccard / IoU | Set / region overlap | Object detection matching; multi-label tagging |
| Dice | Region overlap, medical imaging | Tumour segmentation for radiotherapy planning |
| Log Loss | Probabilities enter a formula | Ad CTR bidding; insurance pricing |
| Brier Score | Robust probability quality | Weather and election forecasting |
| ECE / Calibration curve | Trustworthiness of stated confidence | Clinical risk calculators; selective prediction |
| Hinge Loss | SVM training objective | High-dimensional text classification |
| ROC-AUC | Threshold-free ranking, balanced-ish | Credit scoring (as Gini); model monitoring |
| PR-AUC / AP | Threshold-free ranking, rare positives | Credit-card fraud; lead scoring; anomaly detection |
| KS | Banking convention + cut-off | Retail credit application scorecards |
| Lift / Gain | Fixed-capacity campaigns | Direct marketing; collections call lists |
| Hamming Loss | Multi-label, dense labels | Image auto-tagging |
| Subset Accuracy | Multi-label, no partial credit | Automated form filling; automation-rate reporting |

## 12.3 Advantages and limitations at a glance

| Metric | Key advantage | Key limitation |
|---|---|---|
| Accuracy | Universally understood | Fails completely on imbalanced data |
| Error Rate | Frames improvement well | Identical flaws to accuracy |
| Precision | Directly maps to wasted work | Says nothing about misses; prevalence-dependent |
| Recall | Directly maps to safety | Trivially gamed by flagging everything |
| Specificity | Prevalence-independent | Deceptively high when negatives are numerous |
| FPR | The ROC x-axis | Low FPR still means huge FP counts at scale |
| FNR | Speaks the language of risk | Ignores the negative class |
| NPV | Measures the "all clear" | ≈1 by default on rare-event data |
| F1 | One number, ignores TN | Assumes equal costs; asymmetric under class swap |
| F-beta | Encodes the cost ratio | β must be justified; still ignores TN |
| G-Mean | Zero for any degenerate model | Blind to false-alarm volume |
| Balanced Accuracy | Fixed 0.5 chance baseline | Ignores precision entirely |
| MCC | Uses all 4 cells; symmetric | Not decomposable; unfamiliar |
| Cohen's Kappa | Chance-corrected; handles ordinal | The kappa paradoxes; marginal-dependent |
| Youden's J | Gives you a threshold | Assumes equal costs |
| DOR | Poolable across populations | Cannot distinguish rule-in from rule-out tests |
| Jaccard / IoU | Ignores TN; universal overlap measure | Harsher than Dice; non-differentiable |
| Dice | Differentiable (soft form) | Blind to the spatial location of errors |
| Log Loss | Proper; trainable | Unbounded; one confident error dominates |
| Brier Score | Proper and bounded | Baseline shifts with prevalence |
| ECE | Interpretable in percentage points | Binning-dependent; ignores discrimination |
| Hinge Loss | Margin maximisation; outlier-robust | No probabilities; scale-dependent |
| ROC-AUC | Threshold-free; prevalence-invariant | Over-optimistic on rare events; ignores calibration |
| PR-AUC | Honest on rare events | Not comparable across prevalences |
| KS | One number plus a cut-off | Only a single point on the curve |
| Lift / Gain | Speaks business capacity language | Prevalence- and bin-dependent |
| Hamming Loss | Full partial credit | Near-zero on sparse label sets regardless of skill |
| Subset Accuracy | Equals the automation rate | Collapses as label count grows |

## 12.4 Which metrics move together (avoid double-counting)

Reporting these as separate evidence is padding — they are the same quantity or trivially related:

| Group | Members | Relationship |
|---|---|---|
| Same formula, different names | Recall = Sensitivity = TPR = Hit Rate | Identical |
| | Precision = PPV | Identical |
| | Specificity = TNR = Selectivity | Identical |
| | F1 = Dice = Sørensen index | Identical |
| | Log Loss = Cross-Entropy = NLL | Identical |
| Trivial complements | Accuracy + Error Rate = 1 | |
| | Recall + FNR = 1; Specificity + FPR = 1 | |
| | Precision + FDR = 1; NPV + FOR = 1 | |
| Same quantity, rescaled | Youden's J = 2·BalancedAccuracy − 1 = adjusted balanced accuracy | |
| | KS = max over thresholds of Youden's J | |
| | Gini = 2·ROC-AUC − 1 | |
| Monotonically equivalent | Dice ↔ Jaccard: `D = 2J/(1+J)` | Same model ranking |
| Identical in single-label multi-class | Micro-P = Micro-R = Micro-F1 = Accuracy = Weighted Recall | |
| Closely related in practice | MCC ≈ Cohen's Kappa (0.577 vs 0.571 in our example) | Different formulas, similar behaviour |
| Threshold-free ranking family | ROC-AUC, Gini, KS, and the ROC curve | All derived from the same TPR/FPR sweep |

**What to report instead:** pick one from each group. A strong, non-redundant binary dashboard is:
**PR-AUC (with prevalence) · ROC-AUC · Precision & Recall at the deployed threshold · MCC · Brier/Log Loss · the confusion matrix · expected cost.**

---

# PART 13 — Which Metric Should I Use? (Decision Tree)

## 13.1 The main decision tree

```
START: What kind of problem is it?
│
├── MULTI-LABEL (a sample can have several labels)?
│     │
│     ├── Partial credit has value? ──> MICRO-F1 (primary) + MACRO-F1 (rare labels)
│     │                                 + per-sample JACCARD
│     ├── Only exact matches usable? ──> SUBSET ACCURACY (= automation rate)
│     └── Dense labels, few per sample? ──> HAMMING LOSS (secondary only; never alone)
│
├── MULTI-CLASS (exactly one of K classes)?
│     │
│     ├── All classes equally important? ──> MACRO-F1 + per-class recall table
│     ├── Total error volume matters? ──> ACCURACY (= micro-F1)
│     ├── Classes matter in proportion to size? ──> WEIGHTED-F1
│     ├── Target is ORDINAL (grades, ratings)? ──> QUADRATIC WEIGHTED KAPPA
│     ├── Long tail (100s of tiny classes)? ──> MACRO-F1 over classes with
│     │                                          adequate support + head/mid/tail split
│     └── Need probabilities? ──> CATEGORICAL CROSS-ENTROPY + per-class calibration
│
└── BINARY? ──> continue below
      │
      ├── Do you need a PROBABILITY that enters a formula?
      │     (pricing, expected loss, bidding, clinical risk %)
      │     │
      │     ├── YES ──> LOG LOSS or BRIER SCORE (report BSS)
      │     │            + CALIBRATION CURVE + ECE
      │     │            + ROC-AUC to confirm discrimination
      │     │            (calibrate with Platt/isotonic/temperature if needed)
      │     └── NO ──> continue
      │
      ├── Do you consume a RANKED LIST rather than labels?
      │     (search, recommendations, an analyst worklist, a call list)
      │     │
      │     ├── Fixed capacity (top-k)? ──> PRECISION@k, RECALL@k, LIFT@k, GAIN@k
      │     ├── Rare positives? ──> PR-AUC / AVERAGE PRECISION
      │     ├── Balanced-ish? ──> ROC-AUC
      │     └── Only very low FPR matters (biometrics)? ──> PARTIAL AUC (max_fpr)
      │
      └── Do you make a hard YES/NO decision?
            │
            ├── Is the data BALANCED (roughly 40-60%)?
            │     │
            │     ├── YES ──> Are FP and FN costs similar?
            │     │            ├── YES ──> ACCURACY (+ confusion matrix) and/or MCC
            │     │            └── NO  ──> continue to the cost branch below
            │     │
            │     └── NO (imbalanced) ──> continue
            │
            ├── COST BRANCH: do you know the costs of FP and FN?
            │     │
            │     ├── YES, in currency ──> EXPECTED COST is the primary metric.
            │     │      Threshold t* = C_FP/(C_FP+C_FN) on calibrated probabilities.
            │     │      Report precision/recall at that threshold for communication.
            │     │
            │     └── ONLY THE RATIO ──> F-BETA with β = √(C_FN / C_FP)
            │              e.g. miss 100× worse than false alarm ──> β = 10
            │
            ├── Which error do you fear most?
            │     │
            │     ├── MISSES (cancer, fraud, intrusion, equipment failure)
            │     │      ──> RECALL as the headline, with a PRECISION FLOOR
            │     │      ──> F2, and PR-AUC for model selection
            │     │
            │     ├── FALSE ALARMS (spam, bans, auto-rejections, paid outreach)
            │     │      ──> PRECISION as the headline, with a RECALL FLOOR
            │     │      ──> F0.5, and PRECISION@k
            │     │
            │     └── BOTH EQUALLY
            │            ├── Positive class is the focus ──> F1 + PR-AUC
            │            └── Both classes matter ──> MCC, BALANCED ACCURACY, G-MEAN
            │
            ├── Do you need to prove the model beats CHANCE?
            │      ──> MCC or COHEN'S KAPPA (both 0 at chance)
            │      ──> BALANCED ACCURACY with adjusted=True (= Youden's J)
            │
            ├── Do you need a THRESHOLD, not a score?
            │      ├── Costs known ──> minimise expected cost
            │      ├── Capacity fixed ──> the k-th highest score (a quantile)
            │      ├── Hard constraint ──> lowest threshold meeting "recall ≥ X"
            │      └── Nothing known, equal costs ──> YOUDEN'S J / KS point
            │
            ├── Is it a CLINICAL / DIAGNOSTIC test?
            │      ──> SENSITIVITY + SPECIFICITY (prevalence-independent pair)
            │      ──> PPV + NPV for the specific target population
            │      ──> LR+ / LR− for individual Bayesian updating
            │      ──> DOR for meta-analysis; ROC-AUC for overall discrimination
            │
            ├── Is it SEGMENTATION or DETECTION (computer vision)?
            │      ──> Segmentation: DICE (medical) or mIoU (general)
            │            + HAUSDORFF / surface distance for boundary quality
            │      ──> Detection: mAP (mAP@0.5 and mAP@[.5:.95]), IoU for matching
            │
            └── AUDITING FAIRNESS across demographic groups?
                   ──> Compute recall, precision, FPR, FNR PER GROUP
                   ──> MACRO-average across groups, and report the worst group
                   ──> Report equalised-odds gaps (ΔTPR, ΔFPR) between groups
```

## 13.2 Fast lookup by scenario

| Scenario | Primary metric | Secondary | Never use alone |
|---|---|---|---|
| Balanced binary, symmetric costs | Accuracy | MCC, confusion matrix | — |
| Imbalanced binary, general | PR-AUC | MCC, precision/recall @ threshold | Accuracy, ROC-AUC |
| 1% positives, capacity-constrained | Precision@k, Recall@k | PR-AUC, expected cost | Accuracy, F1, ROC-AUC |
| Misses are catastrophic | Recall (w/ precision floor) | F2, PR-AUC | Accuracy, precision alone |
| False alarms are catastrophic | Precision (w/ recall floor) | F0.5, precision@k | Recall alone |
| Costs known in currency | Expected cost | precision/recall at t* | F1 |
| Probabilities feed a formula | Log Loss / Brier (BSS) | Calibration curve, ECE, ROC-AUC | ROC-AUC alone |
| Ranked list, rare positives | PR-AUC / AP | Lift@k, Gain@k | ROC-AUC alone |
| Ranked list, fixed campaign budget | Lift@k, Gain@k | Expected profit at depth | F1 |
| Comparing across populations | ROC-AUC, Sensitivity, Specificity | DOR | PR-AUC, precision |
| Diagnostic test evaluation | Sensitivity + Specificity | PPV/NPV for the population, LR±, ROC-AUC | Accuracy |
| Multi-class, rare classes matter | Macro-F1 | Per-class recall, confusion matrix | Weighted-F1, accuracy |
| Multi-class, ordinal target | Quadratic Weighted Kappa | Macro-MAE, confusion matrix | Accuracy |
| Multi-label, human reviews output | Micro-F1 | Macro-F1, per-sample Jaccard | Hamming Loss, subset accuracy |
| Multi-label, automation pipeline | Subset Accuracy | Micro-F1 | Hamming Loss |
| Semantic segmentation | Dice / mIoU | Hausdorff, surface distance | Pixel accuracy |
| Object detection | mAP@[.5:.95] | mAP@0.5, per-class AP | Accuracy |
| Model monitoring in production | ROC-AUC + PR-AUC drift | Prevalence drift, ECE drift, PSI | Accuracy |
| Fairness audit | Per-group recall/FPR | Macro across groups, worst-group | Aggregate accuracy |
| Label-quality assessment | Cohen's Kappa (inter-annotator) | — | — |
| SVM training | Hinge Loss | Accuracy/F1 for reporting | Hinge alone in a report |
| Kaggle competition | Whatever the host specifies | — | Anything else |

## 13.3 The three questions that determine everything

If you remember nothing else from this Part, remember these:

1. **"What decision does this model drive, and what does each kind of mistake cost?"** → determines whether you need precision, recall, F-beta, or expected cost.
2. **"Is the output consumed as a label, a ranking, or a number?"** → determines threshold metrics vs ranking metrics vs probability metrics.
3. **"How rare is the positive class?"** → determines whether accuracy and ROC-AUC are honest or misleading.

Answer those three, and the metric follows mechanically. Every wrong metric choice traces back to skipping one of them.

---

# PART 14 — Industry Case Studies

Each case follows the same structure: the problem, what the positive class is, what each error costs, the metric choice with justification, and what *not* to use.

## 14.1 Credit Card Fraud Detection

**Setup.** ~0.1–0.2% of transactions are fraudulent. Millions of transactions per day. Decisions must be made in under 100 ms.

**Positive class:** fraudulent transaction.

**Cost structure**
| Error | Consequence | Rough cost |
|---|---|---|
| **FN** (fraud goes through) | Chargeback + fraud loss + investigation | $100 – $2,000 |
| **FP** (genuine transaction blocked) | Support call, customer anger, possible churn | $5 – $50, plus lifetime-value risk |

**Metrics**
- **Primary: PR-AUC / Average Precision.** With 0.1% prevalence, ROC-AUC will read 0.97+ for a model whose precision is 3%. PR-AUC exposes that; its baseline is 0.001, so it also shows the true difficulty.
- **Operating point: Precision@k and Recall@k**, where k is the daily review capacity. This is the number the fraud team lives with.
- **Expected cost / value detection rate:** `Σ(fraud $ caught) − Σ(cost of reviews) − Σ(customer-impact cost)`. Note that fraud is usually measured in **dollars caught**, not cases caught, because fraud amounts are heavily skewed — a "$-weighted recall" is common and important.
- **Secondary: F2** (misses cost more than reviews), **MCC**, and calibration if the score feeds a risk-based authentication decision.

**Why certain metrics matter more.** The negative class is enormous, so any metric with TN in it (accuracy, specificity, ROC-AUC, NPV) is inflated to the point of uselessness. The binding constraint is analyst capacity, which is a *volume*, so metrics defined at a fixed depth (precision@k) are more actionable than metrics defined at a probability threshold.

**Do not use:** accuracy (99.9% by doing nothing), ROC-AUC alone, NPV, Hamming Loss.

**Practical notes.** Multi-threshold design is standard: auto-decline above t_high, step-up authentication (3-D Secure / OTP) in the middle band, allow below t_low. Each band needs its own precision target. Prevalence drifts constantly as fraudsters adapt, so thresholds must be re-tuned and calibration re-checked continuously.

---

## 14.2 Cancer Detection

**Setup.** Screening (low prevalence, e.g. 0.5% in a mammography programme) or diagnostic confirmation (high prevalence in a referred population). These are **different problems with different metrics**, which is the key insight.

**Positive class:** malignancy.

**Cost structure**
| Error | Consequence |
|---|---|
| **FN** (missed cancer) | Delayed treatment, worse prognosis, possible death, litigation. Effectively unbounded cost. |
| **FP** (false alarm) | Anxiety, additional imaging, possibly a biopsy — real but recoverable harm and cost |

**Metrics**
- **Primary: Sensitivity (Recall)**, typically with a regulatory or guideline floor (screening programmes commonly target sensitivity above 0.90–0.95).
- **Constraint: Specificity**, because at 0.5% prevalence and 1,000,000 women screened, specificity 0.95 produces ~49,750 false positives against at most 5,000 true cases. The programme's recall-to-biopsy budget sets the specificity floor.
- **PPV for the specific population**, because that is what the patient experiences. Compute it from sensitivity, specificity, and the local prevalence via Bayes.
- **ROC-AUC** for comparing algorithms and for publication; **partial AUC** restricted to high-sensitivity region, since only that region is clinically usable.
- **Calibration curve + Brier** if the model outputs a risk percentage that clinicians will act on.
- **Cohen's Kappa** against radiologist consensus, and the **inter-radiologist Kappa as the ceiling.**
- For segmentation of the lesion: **Dice** plus **Hausdorff distance**.

**Why certain metrics matter more.** Cost asymmetry is extreme and one-directional, so recall dominates — but the false-positive burden is what determines whether a screening programme is affordable and ethical, so specificity is a hard constraint rather than something to trade freely. The classic solution is a **cascade**: a high-sensitivity screening test followed by a high-specificity confirmatory test operating on a much higher-prevalence population.

**Do not use:** accuracy (99.5% by predicting "no cancer"), F1 at the default threshold, ROC-AUC alone without the high-sensitivity region.

---

## 14.3 Email Spam Detection

**Setup.** Roughly 50% of raw inbound email is spam, so the raw problem is nearly balanced — but the cost asymmetry is severe and runs the *opposite* way to fraud.

**Positive class:** spam.

**Cost structure**
| Error | Consequence |
|---|---|
| **FP** (legitimate mail marked spam) | User misses a job offer, an invoice, a bank OTP, a medical result. Catastrophic and invisible — the user does not know to look. |
| **FN** (spam reaches inbox) | User deletes it. Mild annoyance. |

**Metrics**
- **Primary: Precision on the spam class**, targeted extremely high (major providers operate at false-positive rates well below 0.1%).
- **F0.5**, weighting precision twice as heavily as recall.
- **FPR on legitimate mail**, reported in absolute volume as well as rate, because at billions of messages a 0.01% FPR is still hundreds of thousands of lost emails.
- **Recall** as a secondary quality measure (users notice spam getting through, but it is a lesser harm).
- **Precision at very low FPR / partial AUC** in the low-FPR region.

**Why certain metrics matter more.** This is the canonical example of precision-dominant costs, and it is worth using as the counterexample whenever someone claims "recall always matters most in ML." The asymmetry also explains the product design: borderline mail goes to a *quarantine folder* rather than being deleted, which converts a hard FP into a soft one. Metric design and product design co-evolve.

**Do not use:** recall as the headline, F2, accuracy alone.

---

## 14.4 Student Admission Prediction

**Setup.** Predicting which applicants will succeed (or which to admit). Moderately balanced, but heavily loaded with **fairness** requirements and legal exposure.

**Positive class:** will succeed / should be admitted.

**Cost structure**
| Error | Consequence |
|---|---|
| **FN** (rejecting a student who would have succeeded) | Talent lost; equity harm; reputational and potentially legal risk |
| **FP** (admitting a student who will struggle) | Dropout, wasted seat and financial aid, harm to the student |

**Metrics**
- **Per-group metrics are the primary requirement**, not the aggregate. Compute recall, precision, FPR, and FNR **separately for each demographic group** (gender, race, socioeconomic status, first-generation status, region).
- **Equalised-odds gaps:** ΔTPR and ΔFPR across groups. A model with aggregate AUC 0.85 that has TPR 0.90 for one group and 0.55 for another is not deployable regardless of its aggregate score.
- **Macro-average across groups** and **report the worst-performing group** explicitly.
- **Calibration per group** — a model can be well calibrated overall and badly miscalibrated for a subgroup, which is one of the most consequential and least-noticed failure modes.
- **Balanced Accuracy or MCC** for overall discrimination.
- **Confusion matrix per group**, always shown.

**Why certain metrics matter more.** In high-stakes allocation decisions about people, the aggregate metric is close to irrelevant; the *distribution* of errors across groups is the ethical and legal object of interest. Note also that several fairness criteria are mathematically incompatible — you generally cannot have equal calibration, equal TPR, and equal FPR simultaneously when base rates differ across groups. That impossibility result must be surfaced to stakeholders as an explicit choice, not buried.

**Do not use:** aggregate accuracy alone; any single aggregate number as the sole basis for deployment.

---

## 14.5 Lead Scoring (Sales / Marketing)

**Setup.** 1–5% of leads convert. Sales capacity is strictly fixed: a rep can make ~50 calls a day.

**Positive class:** lead will convert.

**Cost structure**
| Error | Consequence |
|---|---|
| **FP** (calling a lead who won't buy) | Wasted rep time — the scarce resource |
| **FN** (not calling a lead who would have bought) | Lost revenue (potentially large) |

**Metrics**
- **Primary: Lift@decile and Cumulative Gain.** Sales leadership thinks in "work the top 20% of the list," so these are the natively actionable metrics.
- **Precision@k** where k = daily call capacity.
- **PR-AUC** for offline model comparison (rare positives).
- **Expected profit at depth:** `cum_conversions(k) × margin − k × cost_per_call`, maximised over k. The optimum is where the **marginal** decile's conversion rate falls below `cost_per_call / margin`.
- **Calibration** if the score is used to forecast pipeline revenue — a miscalibrated score produces a miscalibrated forecast, which is worse than no forecast.

**Why certain metrics matter more.** The constraint is capacity, expressed as volume, so depth-based metrics (lift, gain, precision@k) map one-to-one onto the operational decision. F1 is nearly meaningless here because it has no notion of how many leads a rep can call.

**Do not use:** accuracy, F1, ROC-AUC alone.

---

## 14.6 Customer Churn Prediction

**Setup.** 2–20% churn depending on industry. The action is a retention offer with a known cost.

**Positive class:** will churn.

**Cost structure**
| Error | Consequence |
|---|---|
| **FN** (missed churner) | Lost customer lifetime value — often hundreds or thousands |
| **FP** (retention offer to a loyal customer) | Wasted discount margin — often tens |

Because CLV ≫ offer cost, **recall dominates**, and the cost ratio gives you β directly: if CLV = $800 and the offer costs $20, then `β = √(800/20) = √40 ≈ 6.3`.

**Metrics**
- **Primary: expected profit / net retained value**, computed as `(churners retained × CLV × uplift) − (offers sent × offer cost)`. Note the **uplift** factor: not every contacted churner is saved.
- **F-beta with β from the cost ratio** (β ≈ 4–6 in most consumer businesses).
- **Recall with a precision floor** set by the marketing budget.
- **Lift@decile** for campaign sizing.
- **PR-AUC** for model comparison.

**Why certain metrics matter more.** The sophisticated point here is that churn is fundamentally an **uplift modelling** problem, not a classification problem. You do not want to target the customers most likely to churn; you want to target those whose churn probability is most *reducible* by the offer. Some high-risk customers will leave regardless (do-not-disturbs), and some low-risk ones may be annoyed into leaving (sleeping dogs). The correct metrics are then **Qini coefficient** and **uplift curves**, not classification metrics at all. Raising this distinction is a strong differentiator in interviews.

**Do not use:** accuracy; F1 without a cost justification.

---

## 14.7 Manufacturing Defect Detection

**Setup.** Defect rate typically 0.1–2%. Very high inspection volume, often with a camera on a production line.

**Positive class:** defective unit.

**Cost structure**
| Error | Consequence |
|---|---|
| **FN** (defect ships) | Warranty claim, recall, brand damage, potential safety incident and litigation |
| **FP** (good unit rejected) | Scrap or rework cost; yield loss |

Cost ratio is usually strongly FN-dominant, but in high-margin, high-volume manufacturing the aggregate FP cost can be enormous, so both matter.

**Metrics**
- **Primary: Recall (defect detection rate)** with a specified **FPR / false-reject rate ceiling** driven by yield economics.
- **Expected cost per unit:** `FN_rate × warranty_cost + FP_rate × scrap_cost`.
- **PR-AUC** for model comparison.
- **G-Mean or Balanced Accuracy** when both yield and escape rate matter.
- **Per-defect-type Macro-F1** for multi-class defect classification — a rare but critical defect type must not be ignored, which is exactly what macro averaging enforces.
- For localisation: **Dice / IoU** on the defect mask.

**Why certain metrics matter more.** Manufacturing has hard, measurable costs on both sides, so expected cost in currency is achievable and should be the primary metric — this is one of the domains where you genuinely can do the full cost calculation. Regulatory or contractual escape-rate limits (e.g. parts-per-million defect targets in automotive) turn FNR into a hard constraint rather than an objective.

**Do not use:** accuracy; single global F1 across defect types.

---

## 14.8 Loan Default Prediction

**Setup.** 2–15% default rate depending on the portfolio. Heavily regulated, with mandatory model validation and explainability requirements.

**Positive class:** will default.

**Cost structure**
| Error | Consequence |
|---|---|
| **FN** (approving a defaulter) | Loss given default × exposure — potentially the whole principal |
| **FP** (rejecting a good applicant) | Lost interest revenue; fair-lending and reputational risk |

**Metrics**
- **Primary: KS statistic and Gini (= 2·AUC − 1).** These are the banking conventions, expected in every model validation pack and regulatory submission. Not using them will make your work look unfamiliar to the audience regardless of technical merit.
- **Calibration of PD** — mandatory. Basel and IFRS 9 require the probability of default to be accurate in absolute terms because `Expected Loss = PD × LGD × EAD` drives capital and provisioning. Report **calibration curves by rating grade**, plus binomial or Hosmer-Lemeshow tests.
- **Expected loss / risk-adjusted return** at the chosen cut-off.
- **Gains chart** for setting the approval cut-off.
- **Per-group metrics** for fair-lending compliance (ECOA / Regulation B in the US), including approval rates and adverse-impact ratios.
- **Population Stability Index (PSI)** for monitoring score drift over time.

**Why certain metrics matter more.** Two things are unusual here. First, **calibration is a regulatory requirement**, not an optimisation nicety — a well-ranking but miscalibrated model is non-compliant. Second, the audience is bank model-risk-management, so convention matters: KS, Gini, PSI, and calibration-by-grade is the expected vocabulary.

**Do not use:** accuracy; PR-AUC alone (it is fine as a supplement but will not satisfy validators expecting Gini/KS).

---

## 14.9 Recommendation Systems

**Setup.** Millions of items, a user sees 5–20. Implicit feedback (clicks) rather than explicit labels; extreme sparsity.

**Positive class:** the user will engage with the item.

**Cost structure.** Not really FP/FN — the real cost is **user attention**. A bad recommendation in a slot of five is a 20% waste of the most valuable screen real estate you have.

**Metrics**
- **Primary: Precision@k, Recall@k, and MAP@k** for k = the number of visible slots.
- **NDCG@k** (Normalised Discounted Cumulative Gain) — the standard ranking metric when relevance is graded rather than binary, and when position matters. Its discount factor encodes that slot 1 is worth far more than slot 10.
- **Hit Rate@k / Coverage** — does the user find at least one thing?
- **MRR (Mean Reciprocal Rank)** when the user needs exactly one right answer.
- **Beyond-accuracy metrics: catalogue coverage, diversity, novelty, serendipity.** A model that recommends only the top 100 most popular items can score well on precision@k while destroying long-tail discovery and, ultimately, the business.
- **Online metrics are the ground truth:** CTR, session length, conversion, retention, measured in an A/B test. **Offline metrics only serve to decide which candidates are worth testing online.**

**Why certain metrics matter more.** Position-aware, top-k metrics are essential because only the top few items are consumed. Note the notorious **offline-online gap**: offline metrics are computed on logged data collected under a *previous* policy, which creates presentation bias and makes offline improvements frequently fail to replicate online. Acknowledging that gap, and mentioning counterfactual/off-policy evaluation (inverse propensity scoring) as the mitigation, is a strong senior-level answer.

**Do not use:** accuracy, ROC-AUC over all items (dominated by the millions of trivially-irrelevant items), F1 without a k.

---

## 14.10 Search Ranking

**Setup.** A query returns a ranked list. Relevance is graded (perfect / excellent / good / fair / bad), not binary.

**Metrics**
- **NDCG@k** — the dominant metric. Graded relevance with a logarithmic positional discount.
- **MAP** — the long-standing TREC standard for binary relevance.
- **MRR** — for navigational queries where one correct answer exists.
- **Precision@1, @3, @10** — what the user actually sees.
- **Online: click-through rate, abandonment rate, time-to-first-click, query reformulation rate.**
- **Inter-annotator agreement (Cohen's Kappa) on the relevance labels**, because search relevance judgements are subjective and the label ceiling constrains everything.

**Why certain metrics matter more.** Position matters enormously (click-through on result 1 is many times that on result 5), which is exactly what NDCG's discount captures and what precision/recall do not. Graded relevance also cannot be expressed in binary metrics at all.

**Do not use:** accuracy; unpositioned precision/recall; ROC-AUC.

---

## 14.11 Face Recognition

**Setup.** Two distinct tasks with different metrics — conflating them is a common error.
- **Verification (1:1):** "is this the same person?" A binary decision on a pair.
- **Identification (1:N):** "who is this?" A ranking over a gallery.

**Cost structure (verification, e.g. phone unlock or border control)**
| Error | Consequence |
|---|---|
| **FP** = False Accept | An impostor gains access. Security breach. |
| **FN** = False Reject | The legitimate user is denied. Friction. |

**Metrics**
- **FAR (False Accept Rate) = FPR** and **FRR (False Reject Rate) = FNR**. These are the industry vocabulary.
- **TAR@FAR** — "True Accept Rate at FAR = 1e-6" is how vendors and NIST specify systems. The operating point is pinned at an extremely low FAR, so **only the far-left tail of the ROC curve matters** → use **partial AUC**, never full AUC.
- **DET curve** (Detection Error Trade-off): FRR vs FAR on log-log axes — the standard biometric plot, which magnifies exactly the low-FAR region that ROC compresses into invisibility.
- **EER (Equal Error Rate):** the point where FAR = FRR. A convenient single number, but it corresponds to an operating point no real system uses.
- **Identification: Rank-1 accuracy, Rank-5 accuracy, CMC curve** (Cumulative Match Characteristic).
- **Per-demographic-group FAR/FRR** — mandatory. NIST's demographic-differentials studies showed error rates varying by more than an order of magnitude across demographic groups for many algorithms. Reporting only aggregate numbers here is a serious ethical and legal failure.

**Why certain metrics matter more.** Operating at FAR = 1e-6 means the metric must have resolution in a region where ROC-AUC has essentially none. And because the deployment context is often security or law enforcement, subgroup error parity is a first-class requirement rather than an add-on.

**Do not use:** accuracy, full ROC-AUC, F1, aggregate-only reporting.

---

## 14.12 Object Detection — IoU and mAP

**Note on scope:** these two metrics belong primarily to **computer vision**, not to general tabular classification. They are included because they appear constantly in ML interviews and because they are built from the classification metrics already covered. If your work is tabular, you need to recognise and explain them, not necessarily compute them.

### IoU (Intersection over Union)

Already covered as the Jaccard index (9.3). In detection, the "sets" are **bounding-box areas**:

```
            area( predicted box ∩ ground-truth box )
IoU = ---------------------------------------------------
            area( predicted box ∪ ground-truth box )
```

**Its role is as a matching rule, not a score.** IoU decides whether a predicted box *counts* as a detection of a ground-truth box:
- IoU ≥ threshold (conventionally 0.5) → the prediction is a **TP**
- IoU < threshold → the prediction is an **FP**
- A ground-truth box with no matching prediction → an **FN**
- Duplicate predictions on the same object → the highest-confidence one is the TP, the rest are FPs

So IoU converts a geometric localisation problem into the familiar TP/FP/FN counts, at which point ordinary precision and recall apply.

```
     Ground truth        Prediction         IoU
  +-------------+
  |             |
  |     +-------+-----+                  overlap area
  |     |#######|     |         IoU = --------------------
  +-----+-------+     |                 combined area
        |             |
        +-------------+
```

### mAP (mean Average Precision)

**How it is computed, step by step:**
1. Fix an IoU threshold (say 0.5).
2. For a single class, sort all predicted boxes across all images by confidence.
3. Walk down the list, matching each prediction to an unmatched ground-truth box; label it TP or FP by the IoU rule.
4. Compute the precision-recall curve from that ranked list.
5. Compute **AP** = the area under that PR curve (Part 6.7).
6. Repeat for every class and take the mean → **mAP**.

**The two standard variants:**
- **mAP@0.5** (Pascal VOC style): a single IoU threshold of 0.5. Measures "did you find the object?" — lenient about box precision.
- **mAP@[.5:.95]** (COCO style): AP computed at ten IoU thresholds (0.50, 0.55, …, 0.95) and averaged. This additionally rewards **precise localisation**, since a sloppy box passes at 0.5 but fails at 0.85. COCO's headline number is this one, and it is always substantially lower than mAP@0.5 — a model might score 0.55 on mAP@[.5:.95] and 0.75 on mAP@0.5.

COCO also reports **AP_small / AP_medium / AP_large** by object size, because small-object detection is much harder and aggregate mAP hides it — the same "report the breakdown, not just the average" principle that macro-averaging embodies in tabular problems.

**Segmentation analogues:** **mask mAP** (using mask IoU instead of box IoU) for instance segmentation; **mIoU** or **Dice** for semantic segmentation.

**Why mAP is the right metric here.** A detector outputs a *ranked list of candidate boxes with confidences*, exactly like an information-retrieval system. So the natural metric is the area under a PR curve, which is AP. And because detection is inherently multi-class with wildly different class frequencies, macro-averaging across classes (the "m" in mAP) prevents common classes from dominating.

**Limitations.** mAP does not reflect any specific operating point, so it does not tell you the false-alarm rate at a deployment confidence threshold. It weights all classes equally, which may not match the application (a self-driving car cares far more about pedestrians than about potted plants). And it says nothing about latency, which is often the binding constraint in real deployments. Production reports therefore pair mAP with per-class AP, precision/recall at the deployed confidence threshold, and FPS.

**Interview (Medium) — What is mAP and how does IoU relate to it?** IoU is the matching criterion that turns box predictions into TP/FP/FN; AP is the area under the resulting precision-recall curve for one class; mAP is the mean of AP across classes. mAP@[.5:.95] averages over ten IoU thresholds to additionally reward localisation accuracy.

**Interview (Hard) — Why is mAP@[.5:.95] preferred over mAP@0.5?** Because mAP@0.5 saturates: modern detectors easily produce boxes that overlap 50% with the truth, so the metric stops discriminating between good and excellent localisation. Averaging over stricter thresholds up to 0.95 keeps the metric sensitive to box precision, which matters for downstream tasks like robotic grasping, distance estimation, and instance counting where a loose box is genuinely worse.

## 14.13 Case study summary table

| Case | Positive class | Costlier error | Primary metric | Never use |
|---|---|---|---|---|
| Credit card fraud | Fraud | FN (but FP volume binds) | PR-AUC, Precision@k, $-recall | Accuracy, ROC-AUC alone |
| Cancer detection | Malignancy | **FN** (severely) | Sensitivity w/ specificity floor | Accuracy |
| Email spam | Spam | **FP** | Precision, F0.5 | Recall alone |
| Student admission | Will succeed | Context; fairness dominates | Per-group recall/FPR, equalised odds | Aggregate accuracy |
| Lead scoring | Will convert | FP (rep time) | Lift@decile, Precision@k | Accuracy, F1 |
| Customer churn | Will churn | FN (CLV) | Expected profit, F-beta (β≈5); ideally **uplift/Qini** | Accuracy |
| Manufacturing defect | Defective | FN | Recall w/ FPR ceiling, expected cost | Accuracy |
| Loan default | Will default | FN | KS, Gini, **PD calibration** | Accuracy |
| Recommendation | Will engage | Attention waste | NDCG@k, MAP@k, Precision@k | ROC-AUC over all items |
| Search ranking | Relevant | Position errors | NDCG@k | Accuracy |
| Face verification | Same person | FP (breach) | TAR@FAR=1e-6, DET curve | Full ROC-AUC, accuracy |
| Object detection | Object present | Both | mAP@[.5:.95] | Accuracy |

**The pattern across all twelve cases:** the metric is determined by (a) the cost asymmetry, (b) whether the output is a label, a ranking, or a number, and (c) the binding operational constraint (capacity, latency, regulation, fairness). It is never determined by which metric is most familiar.

---

# PART 15 — 100+ Interview Questions with Answers

Organised by level. Questions marked ★ are the ones asked most often.

## 15.A Beginner (Q1–Q25)

**Q1. ★ What is a confusion matrix?**
A table comparing actual vs predicted classes. For binary problems it has four cells: TP (correctly flagged positives), TN (correctly ignored negatives), FP (false alarms), FN (missed cases). Every threshold-based metric is a ratio of these four numbers.

**Q2. What does `confusion_matrix(...).ravel()` return, in order?**
`(TN, FP, FN, TP)`. Rows are actual classes sorted ascending, columns predicted classes sorted ascending, then flattened row-wise.

**Q3. What is a True Positive?**
The model predicted positive and the truth was positive. Read the name as: the second word is what the model said, the first word says whether it was right.

**Q4. ★ What is a Type I error? A Type II error?**
Type I = false positive (claiming an effect that isn't there). Type II = false negative (missing a real effect).

**Q5. ★ Define accuracy.**
`(TP + TN) / (TP + TN + FP + FN)` — the fraction of all predictions that were correct.

**Q6. ★ Define precision.**
`TP / (TP + FP)` — of everything predicted positive, the fraction that really was positive. "When it alarms, how often is it right?"

**Q7. ★ Define recall.**
`TP / (TP + FN)` — of all real positives, the fraction detected. "Of the real cases, how many did we catch?"

**Q8. Define specificity.**
`TN / (TN + FP)` — of all real negatives, the fraction correctly identified as negative.

**Q9. What is the F1 score?**
The harmonic mean of precision and recall: `2PR/(P+R)`.

**Q10. ★ Why harmonic mean instead of arithmetic mean for F1?**
Because the harmonic mean is dominated by the smaller value. A model with P = 1.0 and R = 0.01 gets an arithmetic mean of 0.505 (misleadingly acceptable) but a harmonic mean of 0.0198 (correctly terrible).

**Q11. Range of F1? Of MCC? Of ROC-AUC? Of Log Loss?**
F1: 0 to 1. MCC: −1 to +1. ROC-AUC: 0 to 1 (0.5 = chance). Log Loss: 0 to ∞.

**Q12. Is higher or lower better for Log Loss, Brier, Hamming Loss, and Hinge Loss?**
Lower for all four — they are losses.

**Q13. What is the error rate?**
`(FP + FN)/N = 1 − Accuracy`. Also called the misclassification rate or 0-1 loss.

**Q14. Precision and recall in one sentence each.**
Precision: of my alarms, how many were real? Recall: of the real cases, how many did I alarm on?

**Q15. What is FPR? What is it equal to?**
`FP/(FP+TN) = 1 − Specificity`. The fraction of real negatives falsely flagged.

**Q16. What is FNR?**
`FN/(FN+TP) = 1 − Recall`. The fraction of real positives missed.

**Q17. What is NPV?**
`TN/(TN+FN)` — of everything predicted negative, the fraction genuinely negative. "Can I trust the all-clear?"

**Q18. Are recall and sensitivity the same?**
Yes. Recall = Sensitivity = True Positive Rate = Hit Rate. Different fields, same formula.

**Q19. Are precision and PPV the same?**
Yes. ML says precision; medicine says positive predictive value.

**Q20. ★ What are the two axes of an ROC curve?**
TPR (recall) on the y-axis, FPR (1 − specificity) on the x-axis.

**Q21. What does the diagonal on an ROC curve represent?**
A random classifier — every extra percentage point of TPR costs an equal percentage point of FPR.

**Q22. What does ROC-AUC = 0.5 mean? = 0.3?**
0.5 means no discriminative ability. 0.3 means the model is inverted — flip the sign and you have AUC 0.7.

**Q23. What are the axes of a Precision-Recall curve, and what is its baseline?**
Precision on y, recall on x. The random baseline is a horizontal line at y = prevalence.

**Q24. What does a probability threshold do?**
It converts a continuous score into a hard class: predict positive if score ≥ threshold. It is a business decision, not a model output; 0.5 is only a convention.

**Q25. What is class imbalance?**
When one class vastly outnumbers the other — e.g. 1% fraud, 99% legitimate. It breaks accuracy and inflates ROC-AUC.

## 15.B Intermediate (Q26–Q55)

**Q26. ★ Explain the accuracy paradox with numbers.**
With 10,000 transactions and 100 frauds, predicting "not fraud" for everything yields 9,900/10,000 = 99% accuracy while catching zero frauds. Recall = 0, MCC = 0, Balanced Accuracy = 0.5. Accuracy is dominated by the 99% majority class.

**Q27. ★ Two models both have 85% accuracy. How do you choose?**
Look at their confusion matrices. If A has FN=1/FP=14 and B has FN=14/FP=1, they are opposite systems. Choose by which error is costlier, then compare on precision/recall/F-beta and on PR-AUC or ROC-AUC for threshold-independent quality.

**Q28. ★ Why is there a precision-recall trade-off?**
Both derive from the threshold. Lowering it flags more items, which can only raise recall but usually adds false positives and lowers precision. The trade-off is a property of using one threshold on an imperfect score, not a law of nature — a better model improves both.

**Q29. Can F1 exceed both precision and recall?**
No. `min(P,R) ≤ F1 ≤ max(P,R)`, and F1 ≤ arithmetic mean.

**Q30. ★ What is F-beta and what does β control?**
`F_β = (1+β²)PR/(β²P+R)`. β is how many times more important recall is than precision. β=1 → F1; β=2 → recall twice as important; β=0.5 → precision twice as important.

**Q31. How do you pick β from costs?**
`β = √(C_FN / C_FP)`. If a miss costs 100× a false alarm, β = 10.

**Q32. Limits of F-beta as β→0 and β→∞?**
Precision and recall respectively.

**Q33. A model has P=0.9, R=0.3. Rank F0.5, F1, F2.**
F0.5 > F1 > F2 (precision dominates). Values: 0.643, 0.45, 0.346.

**Q34. ★ What is balanced accuracy and what does an all-majority model score?**
The mean of per-class recalls; for binary, (sensitivity + specificity)/2. An all-one-class model scores exactly 0.5 regardless of imbalance.

**Q35. Balanced accuracy vs G-Mean?**
Same two ingredients (sensitivity, specificity), different mean. Balanced accuracy is arithmetic and more forgiving; G-Mean is geometric and becomes 0 if either class is entirely missed.

**Q36. ★ What is MCC and why is it good?**
The correlation between true and predicted labels: `(TP·TN − FP·FN)/√((TP+FP)(TP+FN)(TN+FP)(TN+FN))`. It uses all four cells, is symmetric under class swapping, and gives exactly 0 to any degenerate model.

**Q37. ★ MCC vs F1?**
F1 ignores TN and is asymmetric (relabelling which class is positive changes it). MCC uses all four cells and is symmetric. F1 is preferable when the negative class is genuinely uninteresting or for comparability with published baselines. Report both.

**Q38. What is Cohen's Kappa?**
`(p_o − p_e)/(1 − p_e)` where p_o is observed agreement (= accuracy) and p_e is chance agreement from the marginals. It removes the free credit imbalance gives to accuracy.

**Q39. What is Quadratic Weighted Kappa and when do you use it?**
Kappa where disagreements are penalised by the squared distance between categories. Use it for **ordinal** targets — severity grades, star ratings, essay scores.

**Q40. ★ What is Log Loss?**
The mean negative log probability assigned to the true class. Lower is better; 0 is perfect; `−ln(0.5) = 0.693` is the no-skill baseline on balanced data.

**Q41. ★ Why does Log Loss punish confident wrong answers so hard?**
Because `−ln(p) → ∞` as p → 0. It encodes the principle that confident false claims are far more damaging than hedged ones, and gives gradient descent a strong signal where the model is most wrong.

**Q42. Is cross-entropy the same as Log Loss?**
Yes, for classification. Different names from information theory, ML, and statistics (NLL).

**Q43. ★ Why train on cross-entropy but report F1?**
Cross-entropy is convex and differentiable so gradient descent can minimise it; 0-1 loss and F1 have zero gradient almost everywhere. But the business decision is a hard label, so the report uses threshold metrics.

**Q44. BCE vs Categorical Cross-Entropy?**
BCE + sigmoid: one independent output per label → binary or **multi-label**. CCE + softmax: outputs compete and sum to 1 → **single-label multi-class**. Deciding question: can a sample have two labels at once?

**Q45. What is the Brier score, and its baseline?**
`mean((p − y)²)`. Baseline (predicting the base rate) is `prevalence × (1 − prevalence)`, which is 0.25 on balanced data.

**Q46. ★ Brier vs Log Loss?**
Both proper scoring rules. Brier is bounded [0,1] and robust to a single catastrophic prediction; Log Loss is unbounded and punishes confident errors without limit. Log Loss is used for training because its gradient stays large when the model is confidently wrong.

**Q47. What is the Brier Skill Score?**
`1 − Brier_model/Brier_baseline`. 1 = perfect, 0 = no better than the base rate, negative = worse.

**Q48. ★ What is hinge loss and which algorithm uses it?**
`max(0, 1 − y·f(x))` with y ∈ {−1,+1} and f(x) the raw decision score. Used by SVMs. Zero loss once a point is correctly classified beyond a margin of 1.

**Q49. What is a support vector, in loss terms?**
A training point at or inside the margin, or misclassified — i.e. one with non-zero hinge loss (or zero loss but exactly on the margin). Only these define the boundary.

**Q50. ★ Give the probabilistic interpretation of ROC-AUC.**
The probability that a randomly chosen positive is scored higher than a randomly chosen negative.

**Q51. Relationship between AUC and Gini?**
`Gini = 2·AUC − 1`. Banks report Gini because chance maps to 0.

**Q52. What is Average Precision?**
The precision at each rank where a positive is retrieved, averaged: `Σ(Rₙ − Rₙ₋₁)·Pₙ`. It is the standard unbiased estimate of PR-AUC.

**Q53. AP vs mAP?**
mAP is the mean of AP across classes (object detection) or queries (search).

**Q54. What is the KS statistic?**
`max over thresholds of (TPR − FPR)` — the maximum vertical gap between the cumulative score distributions of the two classes. Banking convention: 30–40 acceptable, 40+ good.

**Q55. What does lift 2.5 at the top decile mean, and what is the maximum possible lift?**
The top 10% contains 2.5× as many positives as a random 10%. The maximum is `1/prevalence`.

## 15.C Advanced (Q56–Q80)

**Q56. ★★ Why is ROC-AUC misleading for imbalanced data? Use numbers.**
FPR's denominator is the entire negative class. With 100 frauds among 9,900 legitimate transactions, flagging the top 1,000 (containing 90 frauds) gives FPR = 910/9,900 = 0.092 — which looks negligible — while precision is 90/1,000 = 0.090, meaning 91% of investigations are wasted. Same 910 false positives; ROC divides by 9,900 and shrugs, PR divides by 1,000 and exposes it. Crucially, ROC-AUC is *unchanged* if you vary prevalence while holding the score distributions fixed, whereas precision collapses from 0.947 at 50% prevalence to 0.018 at 0.1% prevalence.

**Q57. ★★ Why is PR-AUC preferred for fraud, rare disease, and anomaly detection?**
Four reasons: (1) it never credits true negatives, and nobody cares that you ignored 9,990 normal transactions; (2) false positives consume a fixed scarce resource, and precision is directly proportional to that waste while FPR is not; (3) its baseline equals prevalence, so it honestly reveals problem difficulty; (4) it is far more sensitive to improvements at the top of the ranking, which is the only region a capacity-constrained deployment ever uses.

**Q58. ★★ Can a model have ROC-AUC 0.99 and terrible Log Loss?**
Yes. If scores rank perfectly but are all squashed into [0.45, 0.55], AUC is 0.99 (ordering is perfect) while Log Loss is poor (true positives only receive ~0.55 probability). Fix with post-hoc calibration — Platt or isotonic — which is monotonic and therefore improves Log Loss/Brier while leaving AUC untouched.

**Q59. ★ Can a model have AUC 0.9 and accuracy 0.5?**
Yes. AUC depends only on ranking; accuracy on the threshold. If all scores sit in [0.6, 0.7] with perfect ordering, thresholding at 0.5 predicts positive for everything, so accuracy = prevalence. The fix is threshold tuning, not retraining.

**Q60. Can a model with AUC 0.5 be perfectly calibrated?**
Yes — predict the base rate for every sample. Calibration is perfect, discrimination is nil. This is why calibration must never be reported alone.

**Q61. ★ Does calibration change ROC-AUC?**
No. Platt scaling, isotonic regression, and temperature scaling are all monotonic, and AUC depends only on ordering. Corollary: poor calibration is never a reason to reject a model with good AUC — it is a reason to add a calibration step.

**Q62. ★ Why do neural networks become overconfident, and how do you fix it?**
Cross-entropy has no stationary point until the true-class probability reaches 1, so with enough capacity logit magnitudes keep inflating past the point of correct classification. Fixes: temperature scaling (divide logits by a scalar fitted on validation data — cheap, preserves accuracy exactly, the standard method), label smoothing, mixup, deep ensembles, focal loss.

**Q63. ★ What is label smoothing and why does it help?**
Replace hard one-hot targets with `1−ε` for the true class and `ε/(K−1)` elsewhere. It caps achievable confidence, which improves calibration and generalisation at a small cost in raw accuracy.

**Q64. ★★ Why does the F1-optimal threshold depend on prevalence, and what does that mean for production?**
Precision depends on prevalence; recall does not. As prevalence falls, achieving a given precision requires a higher threshold, so the F1-maximising threshold rises. In production, an F1-tuned threshold silently degrades when the incoming class balance drifts. You must monitor prevalence and re-tune.

**Q65. ★★ Derive PPV from sensitivity, specificity, and prevalence, and explain why it matters.**
`PPV = (Sens·Prev) / (Sens·Prev + (1−Spec)(1−Prev))`. It matters because sensitivity and specificity are intrinsic to the test while prevalence is a property of the population — so the same model has a different PPV in every clinic. Worked example: Sens 0.99, Spec 0.99, Prev 0.001 → PPV = 0.09. A "99% accurate" test gives a positive result that is wrong 91% of the time. This is the base-rate fallacy.

**Q66. ★ Why do screening programmes use a high-sensitivity test followed by a high-specificity test?**
Stage 1 must not miss cases, so it accepts many false positives. Stage 2 then operates on a much smaller, much higher-prevalence population, where a high-specificity confirmatory test can eliminate those false positives economically. Neither test alone could achieve both goals at acceptable cost.

**Q67. FPR vs FDR — what is the difference and why does it matter?**
FPR = FP/(FP+TN), denominator all true negatives. FDR = FP/(FP+TP) = 1 − Precision, denominator all discoveries. In genomics with 20,000 genes tested at FPR 0.05, you get ~1,000 false hits; if you found 1,050 hits total, FDR ≈ 0.95. This is why FDR control (Benjamini-Hochberg) rather than FWER control is standard in high-throughput science.

**Q68. ★ How do you choose a threshold if you know the costs?**
Minimise `E[C] = C_FP × FPR × N_neg + C_FN × FNR × N_pos` by sweeping the ROC curve. For calibrated probabilities there is a closed form: `t* = C_FP/(C_FP + C_FN)`. The geometric condition is that the ROC slope equals `(C_FP·N_neg)/(C_FN·N_pos)` — the iso-cost tangency point.

**Q69. When is the Youden/KS threshold the wrong threshold?**
Whenever costs are asymmetric or capacity is constrained. J maximises `TPR − FPR` with equal weights, implicitly assuming C_FP = C_FN and ignoring prevalence. With C_FN = $500 and C_FP = $5, `t* ≈ 0.01`, far below the J point. And if the team can review only 200 cases a day, the threshold is a capacity quantile, not a cost calculation.

**Q70. ★ Prove micro-F1 = accuracy in single-label multi-class.**
Every misclassified sample contributes exactly one FP (to the predicted class) and one FN (to the true class), so `ΣFP = ΣFN = E`. Then micro-P = micro-R = `ΣTP/(ΣTP + E) = correct/N = accuracy`, and the harmonic mean of two equal values is that value.

**Q71. Why does micro-F1 differ from accuracy in multi-label?**
Because a sample can have several true and several predicted labels, so it can generate different numbers of FPs and FNs; `ΣFP ≠ ΣFN` in general, hence micro-P ≠ micro-R.

**Q72. ★ Macro vs micro vs weighted — when do you use each?**
Macro (every class counts equally) for imbalanced multi-class where rare classes matter and for fairness audits. Micro (= accuracy in single-label) for total error volume and for multi-label. Weighted (proportional to support) for general reporting when the test distribution matches production. Always also print `average=None`.

**Q73. ★ Macro-F1 = 0.42, accuracy = 0.91. Diagnose.**
The model performs well on one or two dominant classes and poorly on the rest. Print per-class F1 and support; check for classes never predicted at all (an all-zero column in the confusion matrix); inspect systematic confusions. Remedies: class weights, targeted data collection, hierarchical classification, merging non-distinct classes, per-class thresholds.

**Q74. ★ Why is Hamming Loss misleading for extreme multi-label problems?**
With 5,000 possible labels and ~4 true per sample, predicting all zeros gives Hamming Loss ≈ 0.0008 — 99.92% "label accuracy" while identifying nothing. Use micro/macro-F1 or Jaccard, which exclude TN and give all-zeros a score of 0.

**Q75. Relationship between Dice/F1 and Jaccard/IoU?**
`D = 2J/(1+J)` and `J = D/(2−D)`. Dice ≥ Jaccard always, equal only at 0 and 1. They rank models identically, so the choice is field convention only — but never mix them when citing results.

**Q76. Why is IoU not used directly as a training loss?**
It is non-differentiable and its gradient is zero when predicted and true regions do not overlap, stalling early training. Differentiable surrogates: soft IoU, Dice loss, Lovász-softmax, and GIoU/DIoU/CIoU for boxes.

**Q77. ★ Why report Hausdorff distance alongside Dice in segmentation?**
Dice is a volumetric overlap measure and is blind to *where* errors occur. A high-Dice segmentation can contain a spurious island far from the structure, or miss a thin critical extension — errors that matter enormously in radiotherapy planning. Hausdorff (usually the 95th percentile) captures worst-case boundary deviation.

**Q78. ★ Explain the kappa paradox.**
Kappa depends on the marginals through p_e, so two confusion matrices with identical accuracy can have very different κ. Example: TP=45/FN=15/FP=25/TN=15 gives accuracy 0.60 and κ = 0.13; TP=25/FN=35/FP=5/TN=35 also gives accuracy 0.60 but κ = 0.26. Balanced, symmetric marginals lower p_e and raise κ. Consequence: κ is not comparable across datasets or across models with very different prediction rates.

**Q79. What is DOR's biggest weakness?**
It collapses the sensitivity/specificity trade-off into one number. Sens 0.95/Spec 0.60 and Sens 0.60/Spec 0.95 both give DOR = 28.5, but one is a screening (rule-out) test and the other a confirmatory (rule-in) test. Always report sensitivity and specificity alongside.

**Q80. Why is hinge loss more robust to outliers than log loss?**
For a violating point, hinge's gradient magnitude is constant (1) regardless of how badly wrong the point is, so a single extreme outlier exerts no more pull on the boundary than a mild one. Log Loss is unbounded as p → 0 with a persistently large gradient, so one mislabelled extreme point can distort the whole model. Bounded gradient = bounded influence.

## 15.D Scenario-based (Q81–Q95)

**Q81. ★★ You are building a cancer detection model. Which metric and why?**
Sensitivity (recall) as the primary objective, because a missed malignancy can be fatal and the cost is effectively unbounded, with a specificity floor set by the biopsy/follow-up capacity of the programme. Report PPV computed for the specific target population's prevalence, since that is what patients experience. Use ROC-AUC (or partial AUC restricted to the high-sensitivity region) for model comparison, calibration curves if the output is a risk percentage clinicians act on, and Cohen's Kappa against radiologist consensus with inter-radiologist Kappa as the ceiling. Never accuracy — at 0.5% prevalence, predicting "no cancer" scores 99.5%.

**Q82. ★★ Fraud model: recall 0.99, precision 0.02. Useful?**
Possibly, as a **first-stage filter** in a cascade — it retains almost all fraud while shrinking the review population. Evaluate it as part of the whole system, not alone. Quantify the workload: at 0.02 precision, catching 100 frauds means reviewing 5,000 transactions. Compare `100 × avg_fraud_loss` against `5,000 × review_cost`. If that is unaffordable, add a second-stage high-precision model or rules layer, or raise the threshold to fit capacity. Also check whether the fraud caught is $-weighted toward large losses, which can justify a low case-precision.

**Q83. ★★ Your F2 is high but the fraud team says the model is useless. What happened?**
F2 tolerates low precision, so the model probably has recall ~0.95 and precision ~0.05, generating alert volume far beyond review capacity. F2 has no notion of capacity. Switch to **precision@k** where k = daily capacity, or **recall at a fixed alert budget**, or expected cost including analyst hours. Then set the threshold from capacity rather than from a metric maximum.

**Q84. ★ Model A has AUC 0.85, Model B has 0.83. Deploy A?**
Not necessarily. Check: is the difference statistically significant (DeLong's test or bootstrap CIs)? Do the curves cross — B may dominate in your operating region? What is PR-AUC if the data is imbalanced? What about calibration if probabilities feed decisions? And latency, cost, interpretability, and regulatory explainability? AUC is one input to a deployment decision, not the decision.

**Q85. ★ Your model's KS is 62 in development and 28 out-of-time. Diagnose.**
Severe overfitting or drift. Check for target leakage (a feature carrying post-outcome information that behaved differently later); run per-feature drift tests between periods; verify the development sample was not used for model selection; confirm the target definition did not change; check for a macro regime shift. Rebuild with out-of-time validation built into selection.

**Q86. ★ Choose a metric for a spam filter and justify it against the "recall matters most" instinct.**
Precision on the spam class, targeted very high, with F0.5 as the composite. The cost asymmetry runs opposite to fraud: a lost job offer or bank OTP is catastrophic and *invisible* to the user, while a spam email in the inbox is a one-click annoyance. Report FPR in absolute volume, because at billions of messages even 0.01% is hundreds of thousands of lost emails. Product design mirrors this: quarantine rather than delete, to soften false positives.

**Q87. ★ Predicting churn where CLV is $800 and a retention offer costs $20. Metric and threshold?**
Cost ratio 40:1 favours recall, so `β = √40 ≈ 6.3` for F-beta. Better: optimise **expected net retained value** = `(churners retained × CLV × uplift) − (offers sent × offer cost)`, and set the threshold by maximising it. The sophisticated answer is that this is really an **uplift modelling** problem — you want customers whose churn probability is most *reducible*, not those most likely to churn — so Qini coefficient and uplift curves are the right metrics, not classification metrics at all.

**Q88. ★ Deploying a biometric face-verification system for phone unlock. Metrics?**
TAR@FAR — true accept rate at a fixed, very low false accept rate (typically 1e-5 or 1e-6). Use a **DET curve** on log-log axes and **partial AUC**, because full ROC-AUC has essentially no resolution in the operating region. Report FRR (user friction) at that FAR. Critically, report **FAR and FRR per demographic group**, since NIST studies found order-of-magnitude disparities across groups for many algorithms. EER is a convenient single number but corresponds to an operating point no real system uses.

**Q89. ★ A stakeholder demands "one number" for an imbalanced fraud model. What do you give them?**
Push back once, briefly, then give **expected annual cost or net savings in currency** — it is a single number, it is the number they actually care about, and it forces the cost assumptions to be explicit. If they insist on a model-quality number, give **PR-AUC with prevalence stated**, or **MCC**. Then attach a one-line dashboard: "at our threshold we catch 78% of fraud, and 1 in 4 alerts is real."

**Q90. ★ Your model is well calibrated overall but you discover it is miscalibrated for one demographic subgroup. What do you do?**
Treat it as a serious defect, since decisions made on subgroup probabilities will be systematically wrong. Steps: quantify with per-group calibration curves and ECE; check whether the subgroup is under-represented in training data; fit **group-specific calibration** (separate Platt/isotonic per group) if legally permissible, or collect more subgroup data; re-evaluate whether the threshold should differ by group and whether that is legally and ethically acceptable. Surface the fact that equal calibration, equal TPR, and equal FPR are mathematically incompatible when base rates differ, so a deliberate choice must be made and documented.

**Q91. Prevalence in production drifted from 5% to 1%. Which of your reported metrics are now wrong?**
Precision, NPV, PR-AUC, lift, gain, expected cost, the F1-optimal threshold, and calibration are all affected. Recall, specificity, FPR, FNR, ROC-AUC, and the ranking itself are not (assuming the score distributions per class are unchanged). Action: recalibrate, re-tune the threshold, and re-baseline PR-AUC against the new prevalence.

**Q92. You used SMOTE on the training set and your probabilities look far too high. Why?**
SMOTE changes the class prior the model learns, so all predicted probabilities are inflated relative to the true base rate. Fix: recalibrate on a held-out set with **natural prevalence**, or apply an explicit prior-shift correction to the log-odds. Also: never resample the validation or test set, or precision, PR-AUC, and calibration all become invalid.

**Q93. You are asked to compare your model against a competitor's published F1 of 0.72. What do you check first?**
Whether the two numbers are comparable at all: same dataset and split, same prevalence, same class designated positive (F1 is asymmetric), same threshold, and same averaging method if multi-class. Also whether their F1 was tuned on the test set. If prevalence or the positive class differs, the comparison is meaningless — reframe around PR-AUC with prevalence stated, or MCC, which is symmetric.

**Q94. Your test set has 8 positive samples. What do you tell the stakeholder about your 0.875 recall?**
That it is one correctly-classified sample away from 0.75 and one away from 1.0, so the point estimate carries almost no information. Report a confidence interval (bootstrap or Wilson), report the raw counts rather than the ratio, and either collect more positive samples, use repeated stratified cross-validation to pool estimates, or reframe the evaluation around a ranking metric computed over more data.

**Q95. Your model's offline NDCG improved 4% but the online A/B test showed no lift. Why might that be?**
The offline-online gap. Offline metrics are computed on logged data collected under the *previous* ranking policy, so they suffer presentation and position bias — items the old policy never showed have no labels. The new model may be surfacing genuinely good items that appear as negatives offline. Mitigations: off-policy/counterfactual evaluation with inverse propensity scoring, interleaving experiments, exploration data collection, and treating offline metrics only as a filter for which candidates deserve an online test.

## 15.E Coding (Q96–Q105)

**Q96. Compute all four confusion-matrix cells and derive eight metrics from scratch.**
```python
import numpy as np
from sklearn.metrics import confusion_matrix

tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
metrics = {
    'accuracy'   : (tp + tn) / (tp + tn + fp + fn),
    'precision'  : tp / (tp + fp) if tp + fp else 0.0,
    'recall'     : tp / (tp + fn) if tp + fn else 0.0,
    'specificity': tn / (tn + fp) if tn + fp else 0.0,
    'npv'        : tn / (tn + fn) if tn + fn else 0.0,
    'fpr'        : fp / (fp + tn) if fp + tn else 0.0,
    'fnr'        : fn / (fn + tp) if fn + tp else 0.0,
}
p, r = metrics['precision'], metrics['recall']
metrics['f1'] = 2 * p * r / (p + r) if p + r else 0.0
```

**Q97. Implement ROC-AUC without sklearn.**
```python
import numpy as np

def roc_auc(y_true, y_score):
    """Mann-Whitney U formulation, with 0.5 credit for ties."""
    y_true  = np.asarray(y_true)
    pos = y_score[y_true == 1]
    neg = y_score[y_true == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float('nan')
    wins  = (pos[:, None] >  neg[None, :]).sum()
    ties  = (pos[:, None] == neg[None, :]).sum()
    return (wins + 0.5 * ties) / (len(pos) * len(neg))
```
The rank-based version (`scipy.stats.rankdata`) is O(n log n) and preferable for large arrays.

**Q98. Implement Log Loss from scratch, safely.**
```python
import numpy as np

def log_loss_manual(y_true, y_prob, eps=1e-15):
    y_true = np.asarray(y_true, dtype=float)
    p = np.clip(np.asarray(y_prob, dtype=float), eps, 1 - eps)   # avoid log(0)
    return -np.mean(y_true * np.log(p) + (1 - y_true) * np.log(1 - p))
```
The `clip` is essential; without it a predicted 0.0 on a true positive gives `-inf`.

**Q99. Find the threshold that maximises F1.**
```python
import numpy as np
from sklearn.metrics import precision_recall_curve

p, r, t = precision_recall_curve(y_true, y_scores)
f1 = np.divide(2 * p * r, p + r, out=np.zeros_like(p), where=(p + r) > 0)
# p and r are one element longer than t; drop the artificial final point
best = int(np.argmax(f1[:-1]))
print(f"Best F1 {f1[best]:.4f} at threshold {t[best]:.4f}")
```

**Q100. Find the cost-optimal threshold.**
```python
import numpy as np
from sklearn.metrics import roc_curve

C_FP, C_FN = 5, 500
fpr, tpr, thr = roc_curve(y_true, y_scores)
n_pos, n_neg = y_true.sum(), len(y_true) - y_true.sum()
cost = C_FP * fpr * n_neg + C_FN * (1 - tpr) * n_pos
best = int(np.argmin(cost))
print(f"Threshold {thr[best]:.4f}, expected cost {cost[best]:,.0f}")
```

**Q101. Compute ECE and MCE.**
```python
import numpy as np

def calibration_errors(y_true, y_prob, n_bins=10):
    y_true, y_prob = np.asarray(y_true), np.asarray(y_prob)
    edges, ece, mce, n = np.linspace(0, 1, n_bins + 1), 0.0, 0.0, len(y_true)
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (y_prob > lo) & (y_prob <= hi)
        if not m.any():
            continue
        gap = abs(y_true[m].mean() - y_prob[m].mean())
        ece += (m.sum() / n) * gap
        mce = max(mce, gap)
    return ece, mce
```

**Q102. Build a lift / gain table.**
```python
import numpy as np, pandas as pd

def lift_gain(y_true, y_score, n_bins=10):
    df = pd.DataFrame({'y': y_true, 's': y_score}).sort_values('s', ascending=False)
    df['decile'] = pd.qcut(df['s'].rank(method='first', ascending=False),
                           n_bins, labels=False) + 1
    prev, total_pos = df['y'].mean(), df['y'].sum()
    out = df.groupby('decile').agg(n=('y', 'size'), pos=('y', 'sum'))
    out['cum_n'], out['cum_pos'] = out['n'].cumsum(), out['pos'].cumsum()
    out['response_rate'] = out['cum_pos'] / out['cum_n']
    out['lift']          = out['response_rate'] / prev
    out['cum_gain']      = out['cum_pos'] / total_pos
    return out
```

**Q103. Compute the KS statistic and its threshold.**
```python
import numpy as np
from sklearn.metrics import roc_curve

fpr, tpr, thr = roc_curve(y_true, y_scores)
j = tpr - fpr
i = int(np.argmax(j))
print(f"KS = {j[i]:.4f} at threshold {thr[i]:.4f}")
```

**Q104. Set up cross-validation and a grid search that optimise the right metric on imbalanced data.**
```python
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import make_scorer, fbeta_score

cv  = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)   # never plain KFold
f2  = make_scorer(fbeta_score, beta=2)

gs = GridSearchCV(
    estimator=model,
    param_grid=params,
    scoring={'f2': f2, 'pr_auc': 'average_precision', 'roc_auc': 'roc_auc'},
    refit='pr_auc',           # which metric selects the final model
    cv=cv, n_jobs=-1,
)
```
Key points: `StratifiedKFold` keeps class ratios stable across folds; multiple `scoring` entries let you inspect trade-offs; `refit` names the metric that actually chooses the model.

**Q105. Compute Dice for a segmentation mask, handling empty masks.**
```python
import numpy as np

def dice(y_true, y_pred, eps=1e-7):
    y_true, y_pred = np.asarray(y_true).ravel(), np.asarray(y_pred).ravel()
    inter = float((y_true * y_pred).sum())
    return (2 * inter + eps) / (y_true.sum() + y_pred.sum() + eps)
```
The `eps` returns ~1.0 when both masks are empty, which is the usual convention — but **state your convention**, because it materially changes mean Dice on datasets with many empty slices.

## 15.F Research / Theory (Q106–Q113)

**Q106. ★ What is a proper scoring rule, and which metrics are proper?**
A scoring rule is proper if its expected value is optimised only when the forecaster reports their true believed probability. Log Loss and Brier are proper; accuracy and F1 are not. Under Log Loss, if your belief is q and you report p, expected loss is minimised at p = q, so you cannot gain by exaggerating or hedging. Accuracy is improper: on a 30%-prevalence problem, honest reporting of 0.3 always thresholds to "negative," so accuracy rewards distorting probabilities toward the extremes.

**Q107. ★ Explain the Murphy decomposition of the Brier score.**
`Brier = Reliability − Resolution + Uncertainty`. Reliability is calibration error (lower better). Resolution measures how much predictions deviate from the base rate in a way that tracks reality (higher better; it is subtracted). Uncertainty is `p(1−p)`, the irreducible outcome variance and also the Brier score of the base-rate predictor. It matters because it shows a single proper score decomposes into the two properties you care about, telling you whether to invest in calibration (cheap, post-hoc) or discrimination (needs better features).

**Q108. Why does minimising cross-entropy equal minimising KL divergence?**
Because `H(y,p) = H(y) + D_KL(y‖p)` and `H(y)` — the entropy of the true distribution — does not depend on the model. So cross-entropy differs from KL divergence by a constant, and their minimisers coincide.

**Q109. ★ Why cross-entropy rather than MSE for classification?**
Three reasons. (1) **Gradients:** with a sigmoid output, MSE's gradient contains `σ'(z) = σ(1−σ)`, which vanishes exactly when the model is confidently wrong, stalling learning. Cross-entropy's gradient simplifies to `(p − y)`, large when the error is large. (2) **Probabilistic correctness:** cross-entropy is the negative log-likelihood of a Bernoulli/Categorical model, so minimising it is maximum likelihood. MSE assumes Gaussian noise, wrong for 0/1 targets. (3) **Convexity:** cross-entropy with a linear model is convex; MSE with a sigmoid is not.

**Q110. What is the Bayes error rate?**
The irreducible minimum error achievable by any classifier, caused by genuine overlap in the class-conditional distributions — two samples with identical features and different labels. If you are near it, more data and bigger models will not help; you need better features.

**Q111. Why is trapezoidal interpolation wrong for PR curves?**
Because between two adjacent PR operating points, achievable precision does not vary linearly with recall — it follows a path determined by the underlying counts. Linear interpolation overestimates the area. Average Precision, a weighted step sum, avoids the bias, which is why `average_precision_score` should be used rather than `auc(recall, precision)`.

**Q112. ★ What is partial AUC and when is it necessary?**
AUC restricted to a specified FPR range (e.g. [0, 0.05]) and rescaled. Necessary whenever the high-FPR region is operationally irrelevant: biometric verification at FAR 1e-6, mass screening where only 1% can be followed up, or alerting with fixed analyst capacity. Full AUC lets a model earn credit in regions you will never operate in.

**Q113. ★ Why is MCC's symmetry property theoretically important?**
Because "which class is positive" is usually an arbitrary labelling convention rather than a property of the problem. Two teams analysing the same churn data — one calling "churned" positive, the other calling "retained" positive — will report *different* F1 scores for the identical model, making F1 non-comparable across conventions. MCC is invariant to that relabelling, and also to exchanging predictions with ground truth (it is a correlation). That makes it a more defensible basis for benchmarking, auditing, and inherited-label situations.

## 15.G Business / Communication (Q114–Q123)

**Q114. ★ Explain precision and recall to a non-technical executive.**
"Imagine a fishing net. **Recall** is what fraction of the fish in the lake we caught. **Precision** is what fraction of what we pulled up was actually fish rather than rubbish. A tighter net catches less rubbish but misses more fish. Which mistake costs us more money decides how we set the net."

**Q115. ★ How do you explain that 99% accuracy is bad news?**
"1% of our transactions are fraudulent. If I wrote a program that just says 'not fraud' every single time — no model, three lines of code — it would be 99% accurate and would catch nothing. Our model needs to beat *that*, and accuracy can't tell us whether it does. What we should ask is: of the alerts we send you, how many are real, and of the real fraud out there, how much do we catch?"

**Q116. ★ How do you convert metrics into a business case?**
Translate each cell into money. `Annual benefit = (frauds caught × average loss avoided) − (alerts × investigation cost) − (false blocks × customer-impact cost)`. Compare to the status quo (current rules engine, or nothing). Present the expected annual net saving, the payback period, and a sensitivity analysis across the plausible range of the cost assumptions. Metrics are the intermediate step; currency is the deliverable.

**Q117. ★ A stakeholder asks "how accurate is the model?" How do you answer without either lying or lecturing?**
Answer the question they meant. "At the setting we're planning to use: of every 100 alerts we send you, about 24 will be real fraud, and we'll catch about 78% of all the fraud that happens. Overall we expect to save around $1.2M a year net of investigation costs. I can show you how those numbers move if you want more alerts or fewer."

**Q118. How do you justify a metric choice in a design document?**
State the decision the model drives, enumerate the error types with their costs and who bears them, state the operational constraint (capacity, latency, regulation), then name the primary metric, the constraint metrics, and the threshold-selection rule — each traced back to a specific cost or constraint. Include what you deliberately are *not* optimising and why. This makes the choice auditable and reviewable rather than a matter of taste.

**Q119. Marketing wants "the top 20% of customers." Which metrics do you report?**
Lift and cumulative gain at the 2nd decile, precision@k for k = 20% of the list, and expected campaign profit at that depth. Also show the marginal response rate by decile so they can see where contacting more people stops paying for itself. Do not lead with F1 — it has no notion of campaign size.

**Q120. Legal asks whether the model is fair. What do you produce?**
Per-group confusion matrices and per-group recall, precision, FPR, FNR, and calibration — for every protected attribute available. Report equalised-odds gaps (ΔTPR, ΔFPR), the worst-performing group explicitly, and approval-rate ratios where relevant. State clearly that equal calibration, equal TPR, and equal FPR cannot all hold simultaneously when base rates differ, so a documented choice among fairness criteria is required, and get sign-off on that choice rather than making it silently.

**Q121. Your model looks worse than the existing rules engine on accuracy but better on PR-AUC. How do you argue for it?**
Show the operating-point comparison, not the aggregate. At a matched alert volume, demonstrate that the model catches more fraud (higher recall at equal precision) or wastes less analyst time (higher precision at equal recall) — one of those must be true if PR-AUC is higher. Convert to money at that operating point. Then explain that accuracy is dominated by the 99% legitimate transactions and does not measure the thing the rules engine was built to do.

**Q122. How do you report a metric responsibly in a paper or a model card?**
State the metric, the dataset and split, the prevalence, the threshold (for threshold metrics), the averaging method (for multi-class), a confidence interval or variance across seeds/folds, the baseline (majority class, prevalence, or random), and the per-class or per-group breakdown. A bare number with none of that context is not a result.

**Q123. ★ What single practice would most improve how metrics are used in industry?**
Choosing the metric — and the threshold rule — *before* training, derived explicitly from the decision the model drives and the cost of each error type, and writing that down. Almost every metric failure in production traces to the metric having been chosen after the fact, either because it was the default or because it was the number that looked best.

---

# PART 16 — Cheat Sheet

## 16.1 One-page summary

```
+=============================================================================+
|                    THE CONFUSION MATRIX IS EVERYTHING                        |
+=============================================================================+
|                              PREDICTED                                       |
|                       Negative        Positive                               |
|            +---------+--------------+--------------+                         |
|   ACTUAL   | Negative|      TN      |   FP (I)     |  --> Specificity, FPR   |
|            +---------+--------------+--------------+                         |
|            | Positive|   FN (II)    |      TP      |  --> Recall, FNR        |
|            +---------+--------------+--------------+                         |
|                            |              |                                  |
|                           NPV         Precision                              |
+=============================================================================+

ROW ratios (divide by ACTUAL)      -> prevalence-INDEPENDENT
   Recall/Sensitivity/TPR, Specificity/TNR, FPR, FNR
COLUMN ratios (divide by PREDICTED) -> prevalence-DEPENDENT
   Precision/PPV, NPV
DIAGONAL / everything -> Accuracy

+=============================================================================+
|                      WHICH FAMILY DO YOU NEED?                               |
+=============================================================================+
| Output is a LABEL      -> threshold metrics: P, R, F-beta, MCC, Bal.Acc      |
| Output is a RANKING    -> ranking metrics : PR-AUC, ROC-AUC, Lift, NDCG@k    |
| Output is a NUMBER     -> probability     : Log Loss, Brier, ECE, calibration|
+=============================================================================+

+=============================================================================+
|                         THE THREE KEY QUESTIONS                              |
+=============================================================================+
| 1. What does each kind of mistake COST?      -> P vs R vs F-beta vs cost     |
| 2. Label, ranking, or number?                -> which family                 |
| 3. How RARE is the positive class?           -> is accuracy/ROC-AUC honest?  |
+=============================================================================+

+=============================================================================+
|                            RED FLAGS                                         |
+=============================================================================+
| Accuracy 0.99 on rare-event data     -> compare to majority baseline         |
| ROC-AUC 0.97, precision 0.05         -> report PR-AUC instead                |
| AUC = 1.00 or KS > 75                -> target leakage; investigate          |
| AUC < 0.50                           -> predictions inverted; flip them      |
| Threshold left at 0.5                -> tune it on validation data           |
| F1 reported with no threshold stated -> incomplete result                    |
| PR-AUC / Brier with no prevalence    -> uninterpretable                      |
| Log Loss with no baseline            -> uninterpretable (balanced = 0.693)   |
| Macro-F1 0.42 vs accuracy 0.91       -> rare classes are failing             |
| Metrics computed after SMOTE on TEST -> invalid; never resample the test set |
| Threshold tuned on the test set      -> optimistically biased                |
+=============================================================================+
```

## 16.2 Formula sheet

**Cell ratios**
```
Accuracy      = (TP + TN) / N                Error Rate  = (FP + FN) / N = 1 − Accuracy
Precision/PPV = TP / (TP + FP)               NPV         = TN / (TN + FN)
Recall/Sens   = TP / (TP + FN)               FNR         = FN / (FN + TP) = 1 − Recall
Specificity   = TN / (TN + FP)               FPR         = FP / (FP + TN) = 1 − Specificity
Prevalence    = (TP + FN) / N                FDR         = FP / (FP + TP) = 1 − Precision
```

**Combined**
```
F1        = 2·P·R / (P + R)          = 2TP / (2TP + FP + FN)
F_beta    = (1+β²)·P·R / (β²·P + R)  ;  β = √(C_FN / C_FP)
G-Mean    = √(Sens × Spec)
Bal. Acc  = (Sens + Spec) / 2         ;  adjusted = 2·BalAcc − 1 = Youden's J
Youden J  = Sens + Spec − 1 = TPR − FPR
Jaccard   = TP / (TP + FP + FN)
Dice      = 2TP / (2TP + FP + FN)     = F1
```

**Chance-corrected**
```
MCC   = (TP·TN − FP·FN) / √((TP+FP)(TP+FN)(TN+FP)(TN+FN))
Kappa = (p_o − p_e) / (1 − p_e)
        p_o = Accuracy
        p_e = (TP+FP)(TP+FN)/N² + (TN+FN)(TN+FP)/N²
DOR   = (TP·TN)/(FP·FN) = LR+ / LR−
LR+   = Sens/(1−Spec)     LR− = (1−Sens)/Spec
```

**Probability**
```
Log Loss = −(1/N) Σ [ y·ln(p) + (1−y)·ln(1−p) ]      baseline: −[q·ln q + (1−q)·ln(1−q)]
Brier    =  (1/N) Σ (p − y)²                          baseline: q(1−q)
BSS      = 1 − Brier_model / Brier_baseline
ECE      = Σ_b (|B_b|/N) · |acc(B_b) − conf(B_b)|
Hinge    = (1/N) Σ max(0, 1 − y·f(x))    with y ∈ {−1, +1}
```

**Ranking**
```
ROC-AUC = P(score of random positive > score of random negative)
        = (wins + 0.5·ties) / (n_pos × n_neg)
Gini    = 2·ROC-AUC − 1
AP      = Σ (Rₙ − Rₙ₋₁)·Pₙ  =  (1/P_total) Σ_positives (precision at that rank)
KS      = max over thresholds of (TPR − FPR)  =  max Youden's J
Lift@k  = Precision@k / Prevalence            Max lift = 1/Prevalence
Gain@k  = cumulative TP@k / total positives   = Recall at depth k
```

**Bayes / conversions**
```
PPV     = (Sens·Prev) / (Sens·Prev + (1−Spec)(1−Prev))
Post-test odds = Pre-test odds × LR
Dice ↔ Jaccard: D = 2J/(1+J)        J = D/(2−D)
t* (cost-optimal, calibrated)  = C_FP / (C_FP + C_FN)
Expected cost = C_FP·FP + C_FN·FN
```

**Averaging (multi-class)**
```
Macro    = (1/K) Σ_k metric_k                     (every class equal)
Micro    = metric(Σ TP, Σ FP, Σ FN)               (= accuracy in single-label)
Weighted = Σ_k (n_k/N) · metric_k                 (weighted recall = accuracy)
```

**Multi-label**
```
Hamming Loss    = wrong label slots / (N × L)
Subset Accuracy = exact label-set matches / N
Jaccard@sample  = |Y ∩ Ŷ| / |Y ∪ Ŷ|, averaged over samples
```

## 16.3 Decision flowchart (compact)

```
                        WHAT IS THE OUTPUT USED FOR?
                                    |
        +---------------------------+---------------------------+
        |                           |                           |
    A LABEL                    A RANKING                    A NUMBER
        |                           |                           |
   Imbalanced?              Fixed capacity (top-k)?      Log Loss / Brier (BSS)
    /       \                    /        \              + Calibration curve
  NO         YES              YES          NO            + ECE
   |          |                |            |            + ROC-AUC (discrimination)
Accuracy   Costs known?    Precision@k   Rare positives?  Calibrate if needed
+ MCC       /      \       Recall@k        /       \       (Platt/isotonic/temp)
        YES         NO     Lift@k       YES        NO
         |           |     Gain@k        |          |
   Expected cost  Which error         PR-AUC    ROC-AUC
   t*=C_FP/       do you fear?         AP       (partial AUC if
   (C_FP+C_FN)     /    |    \                   only low FPR matters)
                  /     |     \
             MISSES  BOTH   FALSE ALARMS
                |      |         |
             Recall   F1        Precision
             + prec.  MCC       + recall
             floor    Bal.Acc   floor
             F2       G-Mean    F0.5
             PR-AUC             Precision@k
```

## 16.4 Metric comparison — the six you will actually use

| | Accuracy | F1 | MCC | ROC-AUC | PR-AUC | Log Loss |
|---|---|---|---|---|---|---|
| Range | 0–1 | 0–1 | −1–1 | 0–1 | 0–1 | 0–∞ |
| Chance value | prevalence of majority | — | **0** | **0.5** | **prevalence** | entropy of prevalence |
| Uses TN | Yes | **No** | Yes | Yes | **No** | Yes |
| Needs threshold | Yes | Yes | Yes | **No** | **No** | **No** |
| Needs probabilities | No | No | No | Yes | Yes | Yes |
| Honest on 1% data | **No** | Partly | **Yes** | **No** | **Yes** | Partly |
| Symmetric to class swap | Yes | **No** | **Yes** | Yes | **No** | Yes |
| Sees calibration | No | No | No | **No** | **No** | **Yes** |
| Report it when | Balanced + symmetric costs | Positive class focus | Honest single number | Prevalence-invariant comparison | Rare positives | Probabilities feed a formula |

## 16.5 Memory tricks and mnemonics

**Reading the four cells**
> The **second** word is what the **model said**. The **first** word says whether it was **right**.
> "False Positive" = the model said Positive, and that was False.

**Precision vs Recall**
> **P**recision = **P**redicted positives are the denominator. (Both start with P.)
> **R**ecall = **R**eal positives are the denominator. (Both start with R.)

That one line resolves the most common confusion in the entire field.

**Precision vs Recall, in plain English**
> **Precision:** "Of the alarms I rang, how many were real?" — *quality of alarms*
> **Recall:** "Of the real cases, how many did I ring for?" — *coverage of cases*

**Which one to prioritise**
> **Precision** protects your **team's time** and your **users' trust**.
> **Recall** protects your **customers' lives** and your **company's losses**.

**Sensitivity vs Specificity (clinical)**
> **SnNout:** a highly **S**e**n**sitive test that is **N**egative rules the disease **out**.
> **SpPin:** a highly **Sp**ecific test that is **P**ositive rules the disease **in**.

**Type I vs Type II**
> **Type I** has **one** letter shape in "FP" — a **F**alse alarm. Boy who cried **wolf** (there was no wolf).
> **Type II** — the wolf ate the sheep and nobody called. A **miss**.
> Or: Type I = "I saw something that wasn't there." Type II = "II didn't see something that was."

**F-beta direction**
> **B**ig **b**eta → **b**ig **r**ecall. β = 2 favours recall; β = 0.5 favours precision.

**Threshold direction**
> **Lower** the threshold → **lower** the bar → catch **more** → **recall up, precision down.**
> **Raise** the threshold → **raise** the bar → catch **less** → **precision up, recall down.**
> Recall and threshold move in **opposite** directions. Always.

**ROC vs PR**
> **ROC** divides false positives by the **whole negative class** — a big denominator **hides** them.
> **PR** divides by the **alerts you raised** — a small denominator **exposes** them.
> Rare positives → use **PR**.

**Baselines you must never forget**
> Accuracy → the **majority class rate**
> ROC-AUC → **0.5**
> PR-AUC / AP → **prevalence**
> Balanced Accuracy / MCC / Kappa / G-Mean → **0.5 / 0 / 0 / 0**
> Log Loss (balanced) → **0.693**
> Brier → **prevalence × (1 − prevalence)**
> Lift → **1.0**

**The metric families**
> **L**abel → threshold metrics. **R**anking → AUC family. **N**umber → probability metrics.
> "**L**abels **R**equire **N**othing fancy; **N**umbers require calibration."

**Identical metrics (do not double-count)**
> Recall = Sensitivity = TPR = Hit Rate
> Precision = PPV
> Specificity = TNR
> F1 = Dice
> Log Loss = Cross-Entropy = NLL
> Micro-F1 = Accuracy = Weighted Recall (single-label multi-class)
> KS = max Youden's J; Youden's J = adjusted Balanced Accuracy; Gini = 2·AUC − 1

**The 20-word summary of the whole course**
> *There is no best metric. There is only the metric that matches what your mistakes cost.*

## 16.6 Common pitfalls — the full list

**Imbalance**
1. Reporting accuracy on rare-event data without the majority baseline.
2. Using `scoring='accuracy'` in `GridSearchCV` on imbalanced data.
3. Reporting ROC-AUC alone when positives are under ~10%.
4. Reporting PR-AUC or Brier without stating prevalence.
5. Reporting a "great" NPV (0.998) on 0.2%-prevalence data — that is the baseline.
6. Believing balanced accuracy fully solves imbalance — it ignores false-alarm volume.

**Threshold**
7. Leaving the threshold at 0.5. The most common production defect in deployed classifiers.
8. Tuning the threshold on the test set and reporting the resulting metric.
9. Using the Youden/KS threshold when costs are asymmetric.
10. Applying `t* = C_FP/(C_FP+C_FN)` to uncalibrated scores.
11. Reporting F1 without stating the threshold.
12. Not re-tuning when prevalence drifts.
13. Optimising F1 and then exceeding review capacity — F1 has no capacity term.

**Code**
14. Passing hard labels where scores are required: `roc_auc_score`, `log_loss`, `brier_score_loss`, `roc_curve`, `precision_recall_curve`, `average_precision_score`, `hinge_loss`.
15. Using `predict_proba(X)[:, 0]` instead of `[:, 1]` — inverts the model.
16. Forgetting `pos_label` with string labels.
17. Using `auc(recall, precision)` instead of `average_precision_score`.
18. Forgetting the `neg_` prefix: `scoring='neg_brier_score'`, `'neg_log_loss'`.
19. Using plain `KFold` instead of `StratifiedKFold`.
20. Not clipping probabilities in a hand-rolled Log Loss → `inf`.
21. Using `sigmoid + BCELoss` instead of `BCEWithLogitsLoss` → `nan`.
22. Adding a softmax before `nn.CrossEntropyLoss` — it already applies `log_softmax`.
23. Reading `calibration_curve` outputs in the wrong order (`prob_true` is the y-axis).
24. Not passing `labels=` to `log_loss` when a CV fold is missing a class.

**Data handling**
25. **Resampling the test or validation set.** Invalidates precision, PR-AUC, lift, calibration, and expected cost.
26. Not recalibrating after SMOTE/undersampling — probabilities come out systematically too high.
27. Evaluating on training data.
28. Target leakage — a feature encoding the outcome. Symptoms: AUC ≥ 0.99, KS > 75, F1 ≈ 1.0.
29. Reporting a metric from an 8-positive test set as a precise point estimate.

**Conceptual confusions**
30. Precision vs Accuracy.
31. Precision vs Specificity (column vs row denominator).
32. Recall vs Specificity (positives vs negatives).
33. FPR vs FDR (actual negatives vs discoveries).
34. FNR vs FOR (actual positives vs predicted negatives).
35. Error rate vs Type I error rate.
36. Macro-F1 (mean of F1s) vs F1 of macro-averaged P and R.
37. Reporting accuracy and micro-F1 as separate evidence in single-label multi-class.
38. Lift (falls to 1.0) vs cumulative gain (rises to 1.0).
39. Dice vs Jaccard when citing published results.
40. Calibration vs accuracy — a base-rate predictor is perfectly calibrated and useless.
41. Believing threshold tuning improves AUC. It does not; it moves you along the same curve.
42. Believing calibration changes AUC. It does not.
43. Confusing Cohen's Kappa (2 raters) with Fleiss' Kappa (many raters).
44. Confusing the KS discrimination statistic with the KS drift test.
45. Treating `accuracy_score` on multi-label input as label-wise accuracy — it is subset accuracy.

**Reporting**
46. Reporting F1 without precision and recall.
47. Reporting precision without recall, or vice versa.
48. Not plotting the prevalence baseline on a PR curve.
49. Not plotting the score histogram under a calibration curve.
50. Comparing metrics across test sets with different prevalence.
51. Comparing F2 to F1, or Dice to IoU, as if they were the same scale.
52. Comparing ECE values computed with different bin counts.
53. Reporting a single average without the per-class or per-group breakdown.
54. Omitting confidence intervals on small test sets.
55. Aggregate-only reporting on a problem with fairness implications.

## 16.7 The five-minute pre-deployment checklist

```
[ ] Did I choose the metric BEFORE training, from the decision and the costs?
[ ] Have I stated the prevalence of the positive class?
[ ] Have I computed the relevant baseline (majority / prevalence / 0.5 / 0.693)?
[ ] Have I looked at the confusion matrix, not just the summary numbers?
[ ] Is the threshold tuned on VALIDATION data, from cost or capacity?
[ ] Have I stated the threshold alongside every threshold-based metric?
[ ] If probabilities are used in a formula, have I checked calibration?
[ ] Is the test set at natural prevalence (never resampled)?
[ ] Have I checked for leakage (AUC ≥ 0.99? KS > 75? F1 ≈ 1.0?)
[ ] Have I reported per-class / per-group breakdowns?
[ ] Do I have a confidence interval, or variance across folds/seeds?
[ ] Can I state the expected business impact in currency?
[ ] Do I know which metric I will monitor in production, and its alert threshold?
[ ] Do I know what I will do when prevalence drifts?
```

---

# Appendix A — The complete running example, all metrics

**Setup:** 100 patients screened. 20 diseased, 80 healthy. Model: TP=15, FN=5, FP=10, TN=70.

```
                        P R E D I C T E D
                    +------------+------------+
        |  Healthy  |  TN = 70   |  FP = 10   |  80
 ACTUAL |           |            |            |
        | Diseased  |  FN =  5   |  TP = 15   |  20
        +-----------+------------+------------+
                          75           25        100
```

| Metric | Value | One-line reading |
|---|---|---|
| Prevalence | 0.2000 | 1 in 5 people is diseased |
| Accuracy | 0.8500 | 85 of 100 calls correct |
| Error Rate | 0.1500 | 15 of 100 calls wrong |
| Precision / PPV | 0.6000 | 6 of every 10 alarms are real |
| Recall / Sens / TPR | 0.7500 | 3 of every 4 real cases caught |
| Specificity / TNR | 0.8750 | 87.5% of healthy correctly cleared |
| FPR | 0.1250 | 12.5% of healthy falsely alarmed |
| FNR | 0.2500 | 1 in 4 real cases missed |
| NPV | 0.9333 | 93% of "all clear" results are right |
| F1 / Dice | 0.6667 | Balanced P/R summary |
| F2 | 0.7143 | Recall-weighted (higher, since R > P) |
| F0.5 | 0.6250 | Precision-weighted (lower, since P < R) |
| G-Mean | 0.8101 | Geometric balance of both classes |
| Balanced Accuracy | 0.8125 | Accuracy with imbalance neutralised |
| Youden's J / adj. BA | 0.6250 | Distance above the ROC diagonal |
| MCC | 0.5774 | Correlation between truth and prediction |
| Cohen's Kappa | 0.5714 | 57% of achievable above-chance agreement |
| Jaccard / IoU | 0.5000 | Half the union is shared |
| DOR | 21.0 | A positive is 21× more likely if diseased |
| LR+ | 6.0 | A positive multiplies pre-test odds by 6 |
| LR− | 0.2857 | A negative multiplies pre-test odds by 0.29 |

**Reproduce it all:**
```python
import numpy as np
from sklearn.metrics import *

y_true = np.array([1]*20 + [0]*80)
y_pred = np.array([1]*15 + [0]*5 + [1]*10 + [0]*70)

tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()   # 70 10 5 15
print(accuracy_score(y_true, y_pred),          # 0.85
      precision_score(y_true, y_pred),         # 0.60
      recall_score(y_true, y_pred),            # 0.75
      f1_score(y_true, y_pred),                # 0.6667
      fbeta_score(y_true, y_pred, beta=2),     # 0.7143
      fbeta_score(y_true, y_pred, beta=0.5),   # 0.6250
      balanced_accuracy_score(y_true, y_pred), # 0.8125
      matthews_corrcoef(y_true, y_pred),       # 0.5774
      cohen_kappa_score(y_true, y_pred),       # 0.5714
      jaccard_score(y_true, y_pred))           # 0.5000
print(tn/(tn+fp),          # specificity 0.875
      tn/(tn+fn),          # NPV         0.9333
      np.sqrt((tp/(tp+fn))*(tn/(tn+fp))),      # G-Mean 0.8101
      (tp*tn)/(fp*fn))     # DOR         21.0
```

---

# Appendix B — The ranking example, all metrics

**Setup:** 20 samples, 8 positives, prevalence 0.40. Scores from 0.95 down to 0.02 (see 6.0).

| Metric | Value |
|---|---|
| ROC-AUC | 0.8229 |
| Gini | 0.6458 |
| Average Precision / PR-AUC | 0.7673 |
| PR baseline (prevalence) | 0.4000 |
| PR-AUC lift over baseline | 1.92× |
| KS statistic | 0.5417 (at threshold 0.45) |
| Youden-optimal threshold | 0.45 |
| F1-optimal threshold | 0.40 (F1 = 0.700) |
| Lift @ decile 1 | 2.50 (= the maximum possible, 1/0.40) |
| Gain @ decile 1 | 0.250 |
| Gain @ 50% depth | 0.750 |

**Threshold sweep:**

| Threshold | Precision | Recall | F1 | Specificity | Accuracy |
|---|---|---|---|---|---|
| 0.2 | 0.500 | 1.000 | 0.667 | 0.333 | 0.600 |
| 0.4 | 0.583 | 0.875 | **0.700** | 0.583 | 0.700 |
| 0.5 | 0.600 | 0.750 | 0.667 | 0.667 | 0.700 |
| 0.6 | 0.625 | 0.625 | 0.625 | 0.750 | 0.700 |
| 0.8 | 0.750 | 0.375 | 0.500 | 0.917 | 0.700 |

**Reproduce it all:**
```python
import numpy as np
from sklearn.metrics import (roc_auc_score, average_precision_score,
                             roc_curve, f1_score)

scores = np.array([0.95,0.90,0.85,0.80,0.75,0.70,0.65,0.60,0.55,0.50,
                   0.45,0.40,0.35,0.30,0.25,0.20,0.15,0.10,0.05,0.02])
y      = np.array([1,1,0,1,1,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0])

print(roc_auc_score(y, scores))            # 0.8229
print(2*roc_auc_score(y, scores) - 1)      # Gini 0.6458
print(average_precision_score(y, scores))  # 0.7673
print(y.mean())                            # PR baseline 0.40

fpr, tpr, thr = roc_curve(y, scores)
i = int(np.argmax(tpr - fpr))
print(f"KS {(tpr-fpr)[i]:.4f} at threshold {thr[i]}")   # 0.5417 at 0.45

for t in [0.2, 0.4, 0.5, 0.6, 0.8]:
    p = (scores >= t).astype(int)
    print(t, round(f1_score(y, p), 4))
```

---

# Appendix C — The complete `classification_report`, decoded

For our binary running example:

```
              precision    recall  f1-score   support
           0     0.9333    0.8750    0.9032        80
           1     0.6000    0.7500    0.6667        20
    accuracy                         0.8500       100
   macro avg     0.7667    0.8125    0.7849       100
weighted avg     0.8667    0.8500    0.8559       100
```

**How to read every cell — this is the single most useful skill in the course:**

| Cell | What it is really called |
|---|---|
| Row `1`, precision = 0.6000 | **Precision / PPV** |
| Row `1`, recall = 0.7500 | **Recall / Sensitivity / TPR** |
| Row `1`, f1-score = 0.6667 | **F1 / Dice** |
| Row `1`, support = 20 | Number of **actual positives** |
| Row `0`, precision = 0.9333 | **NPV** (precision of the negative class) |
| Row `0`, recall = 0.8750 | **Specificity / TNR** |
| Row `0`, support = 80 | Number of **actual negatives** |
| `accuracy` = 0.8500 | Overall accuracy (= micro-F1) |
| `macro avg` recall = 0.8125 | **Balanced Accuracy** |
| `weighted avg` recall = 0.8500 | **= Accuracy**, always |

**The insight to carry away:** a standard binary `classification_report` already contains **precision, recall, specificity, NPV, F1, and balanced accuracy** — six of the eight core metrics — if you know that the class-0 row is the negative class's story. Most people read only the class-1 row and re-derive the rest by hand.

**What it does NOT contain**, and you must add yourself:
- FPR and FNR (trivially `1 − specificity` and `1 − recall`)
- MCC, Cohen's Kappa, G-Mean, Youden's J, DOR
- ROC-AUC, PR-AUC, Average Precision, KS
- Log Loss, Brier, ECE, calibration curve
- The confusion matrix itself
- The threshold used, and the prevalence

**A complete binary evaluation function:**
```python
import numpy as np
from sklearn.metrics import *

def full_report(y_true, y_pred, y_score=None, threshold=0.5):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    out = {
        'threshold'   : threshold,
        'prevalence'  : (tp + fn) / len(y_true),
        'TP': tp, 'FP': fp, 'FN': fn, 'TN': tn,
        'accuracy'    : accuracy_score(y_true, y_pred),
        'precision'   : precision_score(y_true, y_pred, zero_division=0),
        'recall'      : recall_score(y_true, y_pred, zero_division=0),
        'specificity' : tn / (tn + fp) if tn + fp else 0.0,
        'npv'         : tn / (tn + fn) if tn + fn else 0.0,
        'fpr'         : fp / (fp + tn) if fp + tn else 0.0,
        'fnr'         : fn / (fn + tp) if fn + tp else 0.0,
        'f1'          : f1_score(y_true, y_pred, zero_division=0),
        'f2'          : fbeta_score(y_true, y_pred, beta=2, zero_division=0),
        'balanced_acc': balanced_accuracy_score(y_true, y_pred),
        'mcc'         : matthews_corrcoef(y_true, y_pred),
        'kappa'       : cohen_kappa_score(y_true, y_pred),
    }
    out['g_mean']  = np.sqrt(out['recall'] * out['specificity'])
    out['youden']  = out['recall'] + out['specificity'] - 1
    if y_score is not None:
        out['roc_auc']      = roc_auc_score(y_true, y_score)
        out['gini']         = 2 * out['roc_auc'] - 1
        out['pr_auc']       = average_precision_score(y_true, y_score)
        out['pr_baseline']  = out['prevalence']
        out['log_loss']     = log_loss(y_true, y_score)
        out['brier']        = brier_score_loss(y_true, y_score)
        q = out['prevalence']
        out['brier_skill']  = 1 - out['brier'] / (q * (1 - q)) if 0 < q < 1 else np.nan
        fpr_c, tpr_c, _     = roc_curve(y_true, y_score)
        out['ks']           = float(np.max(tpr_c - fpr_c))
    return out
```

---

# Final Goal Checklist

By the end of this document you should be able to:

- [x] **Read any classification report confidently** — Appendix C decodes every cell, including the two metrics (NPV, specificity) hiding in the class-0 row.
- [x] **Understand every metric in scikit-learn** — every metric covered includes its exact sklearn call, its argument traps, and what it silently does wrong if you pass labels instead of scores.
- [x] **Decide which metric to optimise for a business problem** — Part 13's decision tree plus Part 14's twelve case studies, all reducible to three questions: what does each mistake cost, is the output a label/ranking/number, and how rare is the positive class.
- [x] **Explain every metric in a job interview** — 123 questions across seven categories in Part 15, with the most-asked marked ★.
- [x] **Compare two models correctly** — Q84 and Q93: check significance, whether the curves cross in your operating region, PR-AUC if imbalanced, calibration if probabilities matter, and comparability of prevalence, threshold, and positive-class convention.
- [x] **Choose metrics for balanced and imbalanced datasets** — Part 10.0's ranked toolkit for 1%-positive data, and the recurring rule that any metric containing TN is inflated by a large negative class.
- [x] **Understand Kaggle competition evaluation metrics** — Log Loss, F1, macro-F1, ROC-AUC, MAP@k, QWK, PR-AUC, mAP, and Dice are all covered with their baselines and pitfalls.
- [x] **Read ML research papers without confusion** — the naming maps (recall = sensitivity = TPR; F1 = Dice; Log Loss = cross-entropy = NLL; Gini = 2·AUC − 1; KS = max Youden's J), the axis-orientation warning for confusion matrices, and the mAP / IoU / partial-AUC conventions.

**The one sentence to keep:**

> **There is no best metric — only the metric that matches what your mistakes cost. Choose it before you train, state its baseline, and never report it without the confusion matrix.**
