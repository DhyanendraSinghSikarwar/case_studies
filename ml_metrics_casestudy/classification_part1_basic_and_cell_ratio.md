# Classification Case Studies, Part 1: Confusion Matrix and Cell-Ratio Metrics

## Table of Contents

- [Whole-Table Metrics](#whole-table-metrics)
  - [Confusion Matrix](#confusion-matrix)
  - [Accuracy](#accuracy)
  - [Error Rate](#error-rate)
- [Alarm Quality and Coverage](#alarm-quality-and-coverage)
  - [Precision (PPV)](#precision-ppv)
  - [Recall (Sensitivity, TPR)](#recall-sensitivity-tpr)
- [Rates Built on Negatives and Misses](#rates-built-on-negatives-and-misses)
  - [Specificity (TNR)](#specificity-tnr)
  - [False Positive Rate (FPR)](#false-positive-rate-fpr)
  - [False Negative Rate (FNR)](#false-negative-rate-fnr)
  - [Negative Predictive Value (NPV)](#negative-predictive-value-npv)

**How to read this part:** every metric is built from four counts: TP (events caught), FP (false alarms), FN (events missed) and TN (non-events correctly left alone); "positive" means the thing we want to detect, not "good". Each metric has five cases, some where it fits (GOOD) and some where it misleads (BAD). Most are set in the USA and Canada, in dollars.

## Whole-Table Metrics

### Confusion Matrix

**1. What it measures (plain English):** A 2×2 table that counts every prediction by what really happened (actual) and what the model said (predicted). It is not one number but the raw material for all the others. The four cells are TP, FP, FN and TN.

`Cells: TP, FP, FN, TN; Total N = TP + FP + FN + TN; Prevalence = (TP + FN) / N`

**2. Intuition:** It is a report card that lists every kind of right and wrong answer separately, like a pharmacy tally of "correct pills", "wrong pills given" and "pills that should have been given but were not".

**3. Benefits:**

- Shows both kinds of mistake (false alarms and misses) instead of hiding them in one score.
- Lets you attach a dollar cost to each cell, so the model can be judged in business terms.
- Every other metric in this part (accuracy, precision, recall and the rest) can be read off it.
- Easy to explain: counts of real people, parcels or claims, not abstract scores.

**4. Limitations / Potential issues:**

- It describes the model at one cut-off (threshold, the score above which the model says "positive"); change the cut-off and the whole table changes.
- Raw counts depend on how big and how imbalanced (very uneven class sizes) the test set is, so tables from different populations cannot be compared directly.
- It is not a single number, so ranking many models by it is awkward.
- Reading it with the wrong axis convention (rows as predicted instead of actual) silently swaps FP and FN.
- It says nothing about how confident the model was in each prediction.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Pharmacy interaction alerts: counting the false alarms behind a "95% correct" model |
| Industry / Domain | healthcare |
| Business Problem | A Canadian hospital pharmacy wants to flag prescriptions with a dangerous drug interaction before dispensing. Pharmacists will only keep using the tool if the volume of useless alerts is tolerable. |
| ML Translation | Target: dangerous interaction (1) or not (0); binary classification; about 2.4% positives, so imbalanced; 1,000 prescriptions in the test month |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The workload and the safety question live in separate cells: 42 false alarms (FP) drive alert fatigue and 6 misses (FN) drive patient risk. Only the full table shows both at once. |
| Why other metrics are NOT suitable here | Accuracy hides the 42 useless alerts inside a big TN count; recall alone says nothing about pharmacist workload; precision alone says nothing about the 6 missed interactions. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Judging only by accuracy would approve a tool that buries pharmacists in alerts; they start clicking "ignore", and real interactions slip through. |
| Small numeric example | TP 18, FN 6, FP 42, TN 934 (N = 1,000). Accuracy = (18 + 934) / 1,000 = 95.2%, yet always saying "no interaction" scores 976 / 1,000 = 97.6%. Alerts = 18 + 42 = 60; at 1.5 minutes each = 90 minutes, of which 42 × 1.5 = 63 minutes are false alarms. Recall = 18 / 24 = 75%; precision = 18 / 60 = 30%. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Small-business loan re-verification priced cell by cell |
| Industry / Domain | banking |
| Business Problem | A mid-size Canadian lender sends some small-business loan applications for costly income re-verification. Each re-check costs $60, but an undetected falsified application costs $11,000 in write-offs. |
| ML Translation | Target: falsified income (1) or genuine (0); binary classification; 4% positives; 2,000 applications scored at one cut-off |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Because the two errors have very different prices, the manager needs the four counts to multiply by dollars: a false alarm costs $60 and a miss costs $11,000. No single ratio carries those prices. |
| Why other metrics are NOT suitable here | Accuracy treats a $60 error and an $11,000 error as equal; F1 (a blend of precision and recall) also weights them equally; precision alone ignores the expensive misses. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Picking the model with the highest accuracy would favour one that flags almost nothing, letting hundreds of thousands of dollars of bad loans through. |
| Small numeric example | TP 60, FN 20, FP 140, TN 1,780 (N = 2,000). Flagged = 60 + 140 = 200, re-check cost = 200 × $60 = $12,000; misses cost 20 × $11,000 = $220,000; total = $232,000. With no model all 80 bad loans pass: 80 × $11,000 = $880,000. Saving = $648,000. Accuracy is 92%, below the do-nothing 96%, so accuracy would call the model useless. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Two parcel-misroute detectors with the same 90% accuracy |
| Industry / Domain | logistics |
| Business Problem | A Canadian courier must choose between two models that flag parcels sent to the wrong depot. A missed misroute means a $38 reshipment; a false alarm means a $6 re-scan. |
| ML Translation | Target: misrouted (1) or correctly routed (0); binary classification; 20% positives; 200 parcels tested |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The two models have identical accuracy but opposite error patterns. Only the full table shows that Model A mostly misses misroutes while Model B mostly raises cheap false alarms. |
| Why other metrics are NOT suitable here | Accuracy cannot separate the models (both 90%); precision alone would favour Model A (85.7% vs 69.2%) and ignore its misses; recall alone ignores the false-alarm bill. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Choosing by accuracy is a coin flip that can cost 2.5 times more per 200 parcels; scaled to millions of parcels this is a large, avoidable reshipment bill. |
| Small numeric example | Model A: TP 24, FN 16, FP 4, TN 156; accuracy = 180 / 200 = 90%; cost = 16 × $38 + 4 × $6 = $608 + $24 = $632. Model B: TP 36, FN 4, FP 16, TN 144; accuracy = 180 / 200 = 90%; cost = 4 × $38 + 16 × $6 = $152 + $96 = $248. Model B is $384 cheaper. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Comparing two seller-risk models by one table at a 0.5 cut-off |
| Industry / Domain | e-commerce |
| Business Problem | A US online marketplace has a small trust team that can manually review only the 3 riskiest sellers from every 10 flagged by the model. Two candidate models are compared using each one's confusion matrix at the default 0.5 score cut-off. |
| ML Translation | Target: seller breaks marketplace rules (1) or not (0); binary classification with a ranked risk score; 3 positives in 10 sellers (toy sample) |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The table describes only one cut-off. At 0.5 the two models tie on accuracy at 70%, yet they differ hugely in how well they rank sellers. The review team actually works down a ranked list, which a single table cannot show. |
| Why other metrics are NOT suitable here | Accuracy from the same table is a tie (70% each); recall and precision at 0.5 are equally cut-off-bound (Model B flags no one, so its precision is undefined); F1 shares the same one-cut-off blind spot. |
| Better alternative (if BAD fit) | ROC-AUC (probability a random bad seller outscores a random good one) and precision at the top 3 (precision@3): they judge the ranking, matching how reviewers work, and do not depend on a chosen cut-off. |
| Business impact of choosing wrong | A tie at 0.5 could lead to picking the model that wastes the review team's limited capacity on good sellers, letting bad sellers stay live longer. |
| Small numeric example | Model A at 0.5: TP 1, FN 2, FP 1, TN 6, accuracy 70%. Model B at 0.5: TP 0, FN 3, FP 0, TN 7, accuracy 70%. Rankings: Model A top 3 contains 2 bad sellers, so precision@3 = 2 / 3 = 0.67 and ROC-AUC = 19 / 21 = 0.90; Model B top 3 contains all 3 bad sellers, so precision@3 = 3 / 3 = 1.00 and ROC-AUC = 21 / 21 = 1.00. Model B is clearly better, the single table missed it. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Raw false-alarm counts from two utility regions that look unequal but are identical |
| Industry / Domain | energy |
| Business Problem | A US electric utility runs one meter-tampering model in a large northern region and a small southern region. Management sees 120 false alarms in the north versus 15 in the south and wants to retrain the northern model. |
| ML Translation | Target: tampered meter (1) or normal (0); binary classification; very low prevalence (under 1%); different region sizes |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The raw counts in the table scale with how many meters each region has, so they cannot be compared across regions. The northern table is simply about eight times bigger. |
| Why other metrics are NOT suitable here | Raw TP/FP counts and total errors also scale with region size; accuracy is above 98% in both and hides everything; precision depends on how common tampering is in each region. |
| Better alternative (if BAD fit) | Row-normalised rates, FPR (false alarms among normal meters) and recall (caught among tampered meters): they divide by region size, so the two regions become comparable. |
| Business impact of choosing wrong | Retraining a perfectly good model costs data-science time and risks breaking it, while the real question (are both regions equally well served?) goes unanswered. |
| Small numeric example | North: TP 80, FN 20, FP 120, TN 11,880 (12,000 normal meters). South: TP 16, FN 4, FP 15, TN 1,485 (1,500 normal meters). FPR north = 120 / 12,000 = 1.0%; FPR south = 15 / 1,500 = 1.0%. Recall north = 80 / 100 = 80%; recall south = 16 / 20 = 80%. The models behave identically. |

**6. Quick decision rule:** Use the confusion matrix when you need to see both kinds of error, attach dollar costs to each cell, or compare models whose errors differ in kind; avoid relying on it alone when comparing across populations of different size or prevalence, or when the real decision cut-off is not yet fixed.

### Accuracy

**1. What it measures (plain English):** The share of all predictions that were correct. Also called overall correctness or hit ratio. It counts right answers of both kinds and divides by the total.

`Accuracy = (TP + TN) / (TP + TN + FP + FN)`

**2. Intuition:** Like a school exam score: percent of questions answered correctly, without caring which questions were easy or which mistakes were serious.

**3. Benefits:**

- Easiest metric to explain to any manager.
- One number, so it is simple to rank models.
- Needs no choice of a "positive" class.
- Works well when classes are about equal in size and mistakes cost about the same.

**4. Limitations / Potential issues:**

- Misleading on imbalanced data: a model that always says "no event" scores high (the accuracy paradox).
- Treats a false alarm and a miss as equally costly, which is rarely true.
- Depends on the cut-off and ignores how confident each prediction was.
- Not comparable across datasets with different prevalence (how common the event is).
- Always compare it with the baseline (the score of always predicting the most common class).

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Sorting maple veneer into two equally common grades |
| Industry / Domain | manufacturing |
| Business Problem | A Canadian lumber mill uses a camera to sort veneer sheets into Grade A and Grade B. The two grades are about equally common, and mis-sorting either way costs the same $12 of re-handling. |
| ML Translation | Target: Grade A (1) or Grade B (0); binary classification; 50/50 classes; 200 sheets in the test batch |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Classes are balanced and both errors cost the same, so the total number of errors is exactly what matters. Accuracy is that number, framed as a rate. |
| Why other metrics are NOT suitable here | Precision and recall each look at only one class, but here both classes matter equally; the confusion matrix adds detail but no extra decision; F1 ignores true negatives, which are half of the sheets here. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using a fancier metric would not change the model choice, only confuse the plant supervisors reading the report. |
| Small numeric example | TP 93, FN 7, FP 9, TN 91. Accuracy = (93 + 91) / 200 = 92%. Errors = 7 + 9 = 16; cost = 16 × $12 = $192 per batch. Baseline (always Grade A) is 100 / 200 = 50%, so 92% is a real gain. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Routing support tickets to billing or technical queues |
| Industry / Domain | telecom |
| Business Problem | A US mobile carrier's chat system sends each ticket either to the billing team or to the technical team. The two ticket types are equally common, and a wrong queue costs one extra 6-minute hand-off either way. |
| ML Translation | Target: billing (1) or technical (0); binary classification; 50/50 classes; 400 tickets tested |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Balanced classes and equal costs mean every wrong routing is the same size problem. The share of tickets routed right is the whole story. |
| Why other metrics are NOT suitable here | Recall for billing alone would ignore technical tickets; precision alone has the same one-sided view; log loss (a score that punishes confident wrong probabilities) is overkill when the system only needs the final queue. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | An unnecessary specialist metric adds reporting effort without changing the staffing plan. |
| Small numeric example | 348 of 400 tickets routed correctly: accuracy = 348 / 400 = 87%. Errors = 52; hand-off time = 52 × 6 = 312 minutes = 5.2 hours per 400 tickets. Baseline (always billing) = 50%. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Truck driver fatigue events that happen on 2 trips in 100 |
| Industry / Domain | logistics |
| Business Problem | A Canadian trucking firm wants to predict which trips will involve a serious driver-fatigue event so dispatchers can add a rest stop. |
| ML Translation | Target: fatigue event on trip (1) or not (0); binary classification; 2% positives, heavily imbalanced; 1,000 trips tested |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The majority class is 98% of trips. A model that never predicts a fatigue event scores 98% accuracy and prevents nothing. |
| Why other metrics are NOT suitable here | Error rate carries the same information as accuracy and has the same flaw; the always-no model also has a high NPV (share of "no event" calls that are right), so NPV cannot expose it either; plain TN counts are huge and uninformative. |
| Better alternative (if BAD fit) | Recall (share of real fatigue events caught) together with precision (share of alerts that are real), or PR-AUC (area under the precision-recall curve), because they ignore the huge TN count. |
| Business impact of choosing wrong | A fleet buys a "98% accurate" tool that catches none of the 20 events per 1,000 trips; each uncaught fatigue event is a potential accident claim. |
| Small numeric example | 1,000 trips, 20 events. Always-no: accuracy = 980 / 1,000 = 98.0%, recall = 0%. A real model: TP 14, FN 6, FP 30, TN 950; accuracy = 964 / 1,000 = 96.4% (lower!); recall = 14 / 20 = 70%; precision = 14 / 44 = 31.8%. Accuracy ranks the useless model first. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Two loan-default models that are both 100% correct but not equally useful |
| Industry / Domain | banking |
| Business Problem | A mid-size Canadian lender prices personal-loan interest premiums from the model's predicted default probability. Two models are tied on accuracy, and the team asks which to deploy. |
| ML Translation | Target: loan defaults (1) or repays (0); binary classification with predicted probabilities; 5 loans in the toy test; the output is used as a probability, not just a yes/no |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Accuracy only checks which side of 0.5 a prediction falls on. Model A says 0.40 to 0.60 for every loan (a coin flip with the right side), Model B says 0.05 to 0.92. Both score 100%. Pricing needs the probability itself, which accuracy ignores. |
| Why other metrics are NOT suitable here | Recall and precision also use the 0.5 cut-off and tie at 100%; ROC-AUC measures ranking only, not whether the probabilities are sized right for pricing; error rate is just 1 − accuracy. |
| Better alternative (if BAD fit) | Brier score (average squared gap between probability and outcome) or log loss: they reward honest, sharp probabilities, which is what pricing uses. |
| Business impact of choosing wrong | Deploying the hedging model prices good and bad borrowers almost the same, overcharging good customers and underpricing risky ones. |
| Small numeric example | Outcomes [1, 0, 1, 0, 0]. A probabilities [0.55, 0.45, 0.60, 0.40, 0.45]; B probabilities [0.92, 0.08, 0.88, 0.12, 0.05]. Accuracy: A 5 / 5 = 100%, B 5 / 5 = 100%. Brier: A = (0.2025 + 0.2025 + 0.16 + 0.16 + 0.2025) / 5 = 0.1855; B = (0.0064 + 0.0064 + 0.0144 + 0.0144 + 0.0025) / 5 = 0.0088. Loan 4 expected loss at a $10,000 default: A 0.40 × $10,000 = $4,000; B 0.12 × $10,000 = $1,200. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Hail-damaged roofs: equal accuracy, very unequal claims bills |
| Industry / Domain | insurance |
| Business Problem | After a hailstorm a US home insurer uses aerial photos to decide whether a roof is damaged. A sample of 100 roofs is 50% damaged. A damaged roof wrongly marked fine means a wrongly denied claim costing $9,000 in appeals and legal fees; an undamaged roof marked damaged costs $400 for an extra adjuster visit. |
| ML Translation | Target: roof damaged (1) or not (0); binary classification; balanced 50/50 sample; costs very unequal |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The classes are balanced, but the mistakes are not equal: a miss costs 22.5 times a false alarm. Accuracy counts them the same, so it cannot tell a cheap model from an expensive one. |
| Why other metrics are NOT suitable here | Precision ignores the expensive misses; error rate is just 1 − accuracy; F1 weights misses and false alarms equally, which is wrong when one costs 22.5 times more. |
| Better alternative (if BAD fit) | Expected cost (misses × $9,000 + false alarms × $400) or recall (share of damaged roofs correctly flagged), because the cost of a miss dominates. |
| Business impact of choosing wrong | Picking Model A on a tie in accuracy costs $60,200 more per 100 roofs, and wrongly denied homeowners are also a reputational and regulatory risk. |
| Small numeric example | Model A: TP 42, FN 8, FP 2, TN 48; accuracy = 90 / 100 = 90%; cost = 8 × $9,000 + 2 × $400 = $72,800. Model B: TP 49, FN 1, FP 9, TN 41; accuracy = 90 / 100 = 90%; cost = 1 × $9,000 + 9 × $400 = $12,600. Recall A = 42 / 50 = 84%; B = 49 / 50 = 98%. |

**6. Quick decision rule:** Use accuracy when classes are roughly balanced, both errors cost about the same and you want a simple headline; avoid it when the event is rare, when misses and false alarms have very different costs, or when predicted probabilities (not just yes/no) are used.

### Error Rate

**1. What it measures (plain English):** The share of predictions that were wrong. Also called the misclassification rate or 0-1 loss (each wrong answer scores 1, each right answer scores 0, and the average is taken). It is the exact complement of accuracy.

`Error Rate = (FP + FN) / (TP + TN + FP + FN) = 1 − Accuracy`

**2. Intuition:** It is the same exam score viewed as "percent of questions missed", which makes progress easy to state: cutting errors from 8 in 100 to 5.5 in 100 is a large relative improvement.

**3. Benefits:**

- Frames progress as a relative reduction in mistakes, which is easy to communicate.
- The raw count of errors converts directly to rework hours or dollars.
- Fits contracts and service levels (SLAs) that are written as maximum error rates.
- Same simplicity as accuracy and needs no choice of positive class.

**4. Limitations / Potential issues:**

- It carries exactly the same information as accuracy and the same flaws.
- Blind to imbalance: on rare events a useless model can have a tiny error rate.
- Treats all errors as equal, including far-off errors on ordered scales (such as 1 to 5 grades).
- Cannot be compared across datasets with different baselines (the error rate of always predicting the majority class).
- Depends on the cut-off and ignores prediction confidence.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Payroll receipt coding under a vendor contract |
| Industry / Domain | business services (payroll processing) |
| Business Problem | A US payroll processor buys software that tags employee expense receipts as "meals" or "lodging". The vendor contract promises an error rate under 6%. Each wrong tag costs $6 of manual rework. |
| ML Translation | Target: meals (1) or lodging (0); binary classification; about 50/50 classes; 2,000 receipts in the acceptance test |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Classes are balanced, each error costs the same $6, and the contract is written in error rate. The metric matches the contract and the cost. |
| Why other metrics are NOT suitable here | Accuracy carries the same information but is phrased as success, which hides the size of the improvement; precision covers only meals receipts; AUC does not map to a contractual pass/fail threshold. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Measuring a different metric than the one in the contract invites disputes over whether the vendor met the service level. |
| Small numeric example | Before retraining: 160 errors in 2,000 = 8.0% (fails the 6% limit). After: 110 errors in 2,000 = 5.5% (passes). Relative reduction = (160 − 110) / 160 = 31.25%. Per 100,000 receipts: 8,000 errors fall to 5,500; saving = 2,500 × $6 = $15,000. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Counting shelf-label errors in staff hours |
| Industry / Domain | retail |
| Business Problem | A US home-improvement retailer's audit robot checks whether each shelf price tag matches the system price. A curated audit set has equal numbers of matching and mismatching tags. Each wrong call costs a store associate 3 minutes to re-check. |
| ML Translation | Target: tag mismatches system price (1) or matches (0); binary classification; 50/50 audit set; 500 tags |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The count of errors converts straight into labour time, and with equal classes and equal re-check cost, the count is the cost. |
| Why other metrics are NOT suitable here | Recall alone ignores the time wasted on false alarms; precision alone ignores missed mismatches; MCC (a balanced single score) is harder for store managers to turn into hours. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A metric that cannot be turned into hours makes it hard to justify the robot to store operations. |
| Small numeric example | 40 wrong calls in 500 tags: error rate = 40 / 500 = 8%. Time = 40 × 3 = 120 minutes = 2 hours per 500 tags. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Water-main leak detector that is exactly as wrong as doing nothing |
| Industry / Domain | utilities |
| Business Problem | A Canadian municipal water utility scores 5,000 pipe segments for hidden leaks. Only 1% truly leak. Crews can dig up a limited number of segments. |
| ML Translation | Target: segment leaking (1) or sound (0); binary classification; 1% positives, imbalanced; 5,000 segments |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Error rate for a model that never flags anything equals the share of leaks, 1%. A real model that finds most leaks can have the same 1% error rate, so the metric cannot tell them apart. |
| Why other metrics are NOT suitable here | Accuracy is the same number flipped (99%); total errors treat a missed leak and a wasted dig as equal; specificity looks excellent for both models because most pipes are sound. |
| Better alternative (if BAD fit) | Recall (leaks found) together with precision (digs that find a leak), or PR-AUC: they focus on the rare class. |
| Business impact of choosing wrong | A tool that finds 40 of 50 leaks is dismissed as "no better than doing nothing", so leaks keep wasting treated water and damaging roads. |
| Small numeric example | Do-nothing: 50 errors / 5,000 = 1.0%. Model: TP 40, FN 10, FP 40, TN 4,910; errors = 10 + 40 = 50; error rate = 50 / 5,000 = 1.0%. Identical. But recall = 40 / 50 = 80% versus 0%, and precision = 40 / 80 = 50%. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Property condition ratings: one step off versus four steps off |
| Industry / Domain | real estate |
| Business Problem | A US mortgage appraisal firm rates property condition from photos on a 1 to 5 scale (1 best, 5 worst). A rating that is one step off is a nuisance; one that is four steps off can misprice a loan. |
| ML Translation | Target: condition class 1 to 5; ordinal multi-class classification (classes have a natural order); 6 properties in the toy sample |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Error rate only counts "right or wrong", so a one-step miss and a four-step miss both count as 1. It prefers a model with fewer but far larger misses. |
| Why other metrics are NOT suitable here | Accuracy has the same all-or-nothing view; precision and recall per class ignore the distance between classes; the confusion matrix shows distances but gives no single score. |
| Better alternative (if BAD fit) | Mean absolute grade gap (average number of steps off) or quadratic weighted kappa (agreement score that penalises big gaps more): they reward being close. |
| Business impact of choosing wrong | The firm adopts the model whose rare, huge misses put a badly deteriorated property in the "good" bucket, leading to a mispriced mortgage. |
| Small numeric example | True ratings [1, 2, 3, 4, 5, 3]. Model A predicts [2, 2, 3, 5, 5, 4]: 3 errors, each one step off; error rate = 3 / 6 = 50%; mean absolute gap = 3 / 6 = 0.5. Model B predicts [1, 2, 3, 4, 1, 1]: 2 errors, off by 4 and 2; error rate = 2 / 6 = 33.3%; mean absolute gap = 6 / 6 = 1.0. Error rate prefers B; the gap says A is twice as close. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Two direct-mail campaigns: a 5% error rate that is worse than a 12% one |
| Industry / Domain | marketing |
| Business Problem | A US direct-mail company reports error rates for its "will respond" model on two campaigns: 5% on Campaign 1 and 12% on Campaign 2. A manager concludes the model got worse. |
| ML Translation | Target: lead responds (1) or not (0); binary classification; Campaign 1 has 5% responders, Campaign 2 has 30%; 1,000 leads each |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Error rate depends on how common responders are. In Campaign 1 simply predicting "no response" already gives a 5% error rate, so 5% is no improvement; in Campaign 2 the do-nothing error is 30%, so 12% is a big gain. |
| Why other metrics are NOT suitable here | Accuracy is the same comparison flipped (95% vs 88%); raw error counts (50 vs 120) also scale with the base rate; comparing only precision ignores the missed responders. |
| Better alternative (if BAD fit) | Cohen's kappa (agreement beyond what chance would give) or recall and precision side by side: they adjust for the base rate. |
| Business impact of choosing wrong | The company scraps or retrains a model that is working very well on the harder-to-predict campaign and keeps trusting one that barely beats guessing. |
| Small numeric example | Campaign 1: TP 20, FN 30, FP 20, TN 930; error = 50 / 1,000 = 5%; do-nothing error = 5%; recall = 20 / 50 = 40%, precision = 20 / 40 = 50%; kappa = (0.95 − 0.914) / (1 − 0.914) = 0.42. Campaign 2: TP 240, FN 60, FP 60, TN 640; error = 120 / 1,000 = 12%; do-nothing error = 30%; recall = 80%, precision = 80%; kappa = (0.88 − 0.58) / (1 − 0.58) = 0.71. |

**6. Quick decision rule:** Use error rate when classes are balanced, all mistakes cost about the same and you want to talk about improvement or contractual limits; avoid it when the event is rare, when errors differ in size or cost, or when comparing across datasets with different base rates.

## Alarm Quality and Coverage

### Precision (PPV)

**1. What it measures (plain English):** Of everything the model flagged as positive, the share that really was positive. Also called Positive Predictive Value (PPV). It tells you how far to trust an alarm.

`Precision = TP / (TP + FP)`

**2. Intuition:** A fishing net that hauls in 25 things, of which 15 are fish: precision is 15 out of 25, no matter how many fish stayed in the lake.

**3. Benefits:**

- Directly measures wasted work: every false positive is an inspection, a call or a voucher spent for nothing.
- Ignores the huge pool of true negatives, so it stays informative on rare events.
- Maps straight to cost: number of alerts times cost per alert.
- Pairs with recall to describe how well the positive class is handled.

**4. Limitations / Potential issues:**

- Says nothing about missed cases: flagging one obvious event and ignoring the rest gives 100% precision.
- Depends on prevalence, so the same model has a lower precision in a population where the event is rarer.
- Undefined when the model flags nothing.
- Rises when the cut-off is raised, so it is easy to game by being very cautious.
- Should always be reported with recall.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Dispatching a truck to a cell tower that is not actually failing |
| Industry / Domain | telecom |
| Business Problem | A US wireless carrier's model flags cell sites likely to have a failing radio unit. Each flag sends a technician truck at a cost of $350, so false alarms are the main cost. |
| ML Translation | Target: site has a failing unit (1) or not (0); binary classification; low prevalence; the model's 40 daily dispatches are reviewed |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The expensive action happens only on flagged sites. Precision is exactly the fraction of those costly dispatches that find a real fault. |
| Why other metrics are NOT suitable here | Accuracy is dominated by the thousands of healthy sites; recall says nothing about the wasted trucks; specificity (share of healthy sites left alone) stays high even when most dispatches are wasted. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Low precision means a fleet of trucks driving to healthy towers and technicians losing trust in the tool. |
| Small numeric example | 40 dispatches, 28 find a real fault: precision = 28 / 40 = 70%; wasted dispatches = 12 × $350 = $4,200 per day. A model with 40% precision would find 16 real faults and waste 24 × $350 = $8,400. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Delisting suspected counterfeit products |
| Industry / Domain | e-commerce |
| Business Problem | A US online marketplace automatically removes product listings the model labels as counterfeit. A wrongly removed honest seller loses about $1,800 of sales that week and may leave the platform. |
| ML Translation | Target: listing is counterfeit (1) or genuine (0); binary classification; low prevalence; 50 listings removed in one week |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The automated action is irreversible and harmful when wrong, so the question is "when the model says counterfeit, is it right?" That is precision. |
| Why other metrics are NOT suitable here | Recall would reward removing too many listings; accuracy is swamped by millions of genuine listings; FPR (false alarms among genuine listings) looks tiny at that scale and hides the 4 harmed sellers. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Every honest seller wrongly delisted is lost revenue, a complaint and possibly a lawsuit or press story. |
| Small numeric example | 50 removed, 46 truly counterfeit: precision = 46 / 50 = 92%; honest sellers hit = 4 × $1,800 = $7,200. A model at 70% precision would remove 35 real and 15 honest: 15 × $1,800 = $27,000. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Nurse call-backs after hospital discharge |
| Industry / Domain | healthcare |
| Business Problem | A US hospital has nurses who can place 30 post-discharge check-in calls a day. The model picks which patients to call, and each call takes 25 minutes. |
| ML Translation | Target: patient will be readmitted in 30 days (1) or not (0); binary classification; moderate prevalence; the top 30 patients are called each day |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Nurse time is the limiting resource and every call to a patient who did not need it is wasted. Precision among the 30 called measures how well the scarce time is used. |
| Why other metrics are NOT suitable here | Recall depends on how many total at-risk patients exist, not on the capacity of 30 calls; accuracy is dominated by the many patients not called; AUC judges the whole ranking, not the top 30 the nurses actually work. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Hours of nurse time go to patients who were fine, while patients who needed a call do not get one. |
| Small numeric example | 30 called, 21 truly at risk: precision = 21 / 30 = 70%; wasted calls = 9 × 25 = 225 minutes = 3.75 hours. A model at 40% precision: 12 useful calls, 18 wasted = 450 minutes = 7.5 hours. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Two flagged claims, both right, 38 frauds missed |
| Industry / Domain | insurance |
| Business Problem | A US auto insurer's special investigations unit wants to find staged-accident claims. The model flags only the 2 most obvious claims, and both are confirmed as staged. |
| ML Translation | Target: claim is a staged accident (1) or genuine (0); binary classification; low prevalence; 40 staged claims hidden in the month's data |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Precision only looks at the 2 flagged claims, so it is a perfect 100%. It is silent about the 38 staged claims the model never flagged. |
| Why other metrics are NOT suitable here | Accuracy is high because genuine claims dominate; FPR is near zero and also hides the misses; specificity is near 100%. |
| Better alternative (if BAD fit) | Recall (share of staged claims found) with F1 (a blend of precision and recall) or PR-AUC, because the key business risk is the missed fraud. |
| Business impact of choosing wrong | The insurer celebrates a perfect score while 38 staged claims at $9,500 each, $361,000 in total, are paid out. |
| Small numeric example | Model 1: 2 flagged, 2 correct; precision = 100%; recall = 2 / 40 = 5%; F1 = 2 × 1.00 × 0.05 / 1.05 = 0.095; losses = 38 × $9,500 = $361,000. Model 2: 60 flagged, 33 correct; precision = 33 / 60 = 55%; recall = 33 / 40 = 82.5%; F1 = 0.66; losses = 7 × $9,500 = $66,500 plus 60 investigations at $700 = $42,000, total $108,500. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — The pharmacy model that "got worse" in rural stores while staying the same |
| Industry / Domain | retail (pharmacy chain) |
| Business Problem | A Canadian pharmacy chain built a model to flag patients likely to stop taking their medication. It was validated in city stores where 20% of patients were non-adherent. In rural stores only 5% are, and precision looks much lower. |
| ML Translation | Target: patient non-adherent (1) or adherent (0); binary classification; prevalence 20% in the city, 5% in rural stores; 1,000 patients each |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Precision depends on how common the event is in the population. The model's ability did not change, but precision fell because there are fewer true cases among the people it flags. |
| Why other metrics are NOT suitable here | Accuracy also shifts with prevalence; raw counts of TP scale with the number of patients; error rate is again prevalence-driven. |
| Better alternative (if BAD fit) | Recall (80% in both) and specificity (90% in both), which do not move with prevalence, and lift (precision divided by prevalence) to see the gain over random picking. |
| Business impact of choosing wrong | The chain abandons or rebuilds a model that works equally well, wasting analytics spend, or sets unrealistic precision targets for rural pharmacists. |
| Small numeric example | City: TP 160, FN 40, FP 80, TN 720; precision = 160 / 240 = 66.7%; recall = 160 / 200 = 80%; specificity = 720 / 800 = 90%. Rural: TP 40, FN 10, FP 95, TN 855; precision = 40 / 135 = 29.6%; recall = 40 / 50 = 80%; specificity = 855 / 950 = 90%. Lift: city = 0.667 / 0.20 = 3.3; rural = 0.296 / 0.05 = 5.9, so the model is actually more valuable in rural stores. |

**6. Quick decision rule:** Use precision when a false alarm is expensive or erodes trust and the follow-up capacity is limited; avoid it as a stand-alone score when misses matter, or when comparing populations with different prevalence.

### Recall (Sensitivity, TPR)

**1. What it measures (plain English):** Of all the real events, the share the model caught. Also called Sensitivity, True Positive Rate (TPR) or hit rate. It tells you how much of the problem the model covers.

`Recall = TP / (TP + FN)`

**2. Intuition:** A smoke detector's job is to go off when there is a fire. Recall is the share of real fires it detected, however many false alarms it also raised.

**3. Benefits:**

- Directly measures coverage of the events you care about.
- Does not change with how common the event is, so results travel across populations.
- Easy to explain: "we catch 9 of every 10 cases".
- Multiplies cleanly with the cost of a miss to give expected loss.

**4. Limitations / Potential issues:**

- Easily gamed: flag everything and recall is 100%.
- Says nothing about false-alarm volume or its cost.
- Depends on the cut-off.
- Very noisy when there are few real positives in the test set (one case more or less moves it a lot).
- Should always be shown with precision.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Overheating wheel bearings on freight cars |
| Industry / Domain | transportation and logistics |
| Business Problem | A Canadian railway uses trackside sensors and a model to flag freight-car bearings that are about to fail. A missed bearing can lead to a derailment with an expected cost of about $250,000 per miss; an unnecessary inspection costs $600. |
| ML Translation | Target: bearing will fail soon (1) or not (0); binary classification; very low prevalence; 20 real failing bearings in the test period |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The cost of one miss is hundreds of times the cost of one false alarm, so the key question is how many failing bearings the model finds. |
| Why other metrics are NOT suitable here | Accuracy is high for a model that flags almost nothing; precision rewards a cautious model that misses failures; specificity says nothing about the failures. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Choosing on precision or accuracy could leave the railway with a quiet but dangerous model, with each miss risking a derailment, injuries and shutdown of the line. |
| Small numeric example | 20 failing bearings: model catches 18, recall = 18 / 20 = 90%; misses = 2 × $250,000 = $500,000. A model with 60% recall catches 12, misses 8 × $250,000 = $2,000,000; if it also avoids an assumed 100 false-alarm inspections at $600 = $60,000, it still costs $1,500,000 more in misses. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Warning the delivery room about heavy bleeding risk |
| Industry / Domain | healthcare |
| Business Problem | A US maternity ward wants to flag mothers at high risk of severe bleeding after birth so blood products and extra staff are ready. Preparing for a patient who does not bleed costs about $150. |
| ML Translation | Target: severe postpartum bleeding (1) or not (0); binary classification; low prevalence; 50 real cases in the evaluation year |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Missing a high-risk mother can be life-threatening, while a false alarm costs a little preparation. So the main goal is catching as many true cases as possible. |
| Why other metrics are NOT suitable here | Precision at 25% would look poor but is acceptable here; accuracy is dominated by the many low-risk births; specificity can look excellent for a model that misses cases. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A model optimised for precision would stay quiet for borderline cases, and a missed case can mean a preventable death and major liability. |
| Small numeric example | 50 real cases: model flags 44 of them, recall = 44 / 50 = 88%; 6 missed. If it flagged 176 mothers in total, precision = 44 / 176 = 25% and 132 false alarms cost 132 × $150 = $19,800 of preparation, a small price for catching 44 cases. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Structuring transactions a regulator expects the bank to find |
| Industry / Domain | banking |
| Business Problem | A Canadian credit union must detect "structuring" (splitting deposits into small amounts to avoid reporting). A missed case brings a regulatory penalty of about $50,000; reviewing a false alert costs $45. |
| ML Translation | Target: account shows structuring (1) or not (0); binary classification; very low prevalence; 30 confirmed cases in the review period |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Regulators penalise missed cases much more than over-reporting, and the credit union's duty is to find them. Recall measures that duty. |
| Why other metrics are NOT suitable here | Precision would encourage fewer alerts and more misses; accuracy is meaningless when almost all accounts are clean; FPR on its own does not show how many structuring cases were found. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A model tuned to reduce analyst workload but missing cases invites penalties and reputational damage. |
| Small numeric example | 30 real cases: model finds 27, recall = 27 / 30 = 90%; misses = 3 × $50,000 = $150,000. A model with 70% recall finds 21, misses 9 × $50,000 = $450,000. Review cost for 400 false alerts = 400 × $45 = $18,000, far smaller than the extra $300,000 in penalties. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — "Flag everyone" mailing to reach every likely buyer |
| Industry / Domain | marketing (retail banking) |
| Business Problem | A US retail bank wants to find customers who will buy a home-equity line. Mailing costs $6 per customer, and each sale earns $120 in margin. A manager proposes judging the model by recall alone. |
| ML Translation | Target: customer buys (1) or not (0); binary classification; 8% positives; 10,000 customers |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Mailing everyone gives a perfect recall of 100%, because no buyer is missed, but it costs a fortune. Recall alone cannot see the cost of false alarms. |
| Why other metrics are NOT suitable here | Accuracy would be 8% for the mail-everyone plan, which is unhelpful as a profit guide; FNR (miss rate) is 0% for that plan and hides its cost; AUC does not translate to profit at a given mailing size. |
| Better alternative (if BAD fit) | Precision with a profit calculation (revenue minus mailing cost), or F1 / PR-AUC, because the mailing cost makes false alarms expensive. |
| Business impact of choosing wrong | The bank spends $60,000 to earn $96,000 instead of spending far less and earning more. |
| Small numeric example | Mail all 10,000: recall = 100%, precision = 800 / 10,000 = 8%; cost = 10,000 × $6 = $60,000; revenue = 800 × $120 = $96,000; profit = $36,000. Targeted model mails 2,000 and reaches 560 buyers: recall = 560 / 800 = 70%, precision = 560 / 2,000 = 28%; cost = $12,000; revenue = 560 × $120 = $67,200; profit = $55,200. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — A rare-skill resume matcher validated on eight candidates |
| Industry / Domain | HR tech |
| Business Problem | A US staffing firm tests a resume-matching model for a rare engineering skill. Only 8 candidates in the test set truly have it, and the model finds 7. The sales team quotes "87.5% recall" to clients. |
| ML Translation | Target: candidate has the rare skill (1) or not (0); binary classification; very few positives (8) in the test set |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | With only 8 positives, each one is worth 12.5 percentage points. Recall as a single number looks precise but is really a wide range. |
| Why other metrics are NOT suitable here | Precision has the same tiny-sample problem on the flagged side; accuracy is dominated by thousands of non-matching resumes; F1 inherits the instability of recall. |
| Better alternative (if BAD fit) | Recall reported with a confidence interval (a range of plausible true values) and more positives through repeated cross-validation or a larger test set. |
| Business impact of choosing wrong | The firm promises clients "87.5% recall" and may deliver noticeably less in practice, harming trust and possibly breaching service promises. |
| Small numeric example | 7 of 8 found: recall = 7 / 8 = 87.5%; if one more candidate is missed, 6 / 8 = 75%. A 95% Wilson interval for 7 of 8 runs from about 53% to 98%. With 70 of 80 (same 87.5%), the interval narrows to about 78% to 93%; with 700 of 800, about 85% to 90%. |

**6. Quick decision rule:** Use recall when a missed event is costly or irreversible and you need to know how much of the problem the model covers; avoid it as a stand-alone score when false alarms are costly, or when the test set has only a handful of positives.

## Rates Built on Negatives and Misses

### Specificity (TNR)

**1. What it measures (plain English):** Of all the real non-events, the share the model correctly left alone. Also called True Negative Rate (TNR) or selectivity. It is recall's mirror image for the negative class.

`Specificity = TN / (TN + FP) = 1 − FPR`

**2. Intuition:** A metal detector at a courthouse door: specificity is the share of harmless visitors who walk through without the alarm sounding.

**3. Benefits:**

- Measures how well the innocent majority is left undisturbed.
- Does not change with prevalence, so it is portable across populations.
- Together with recall (sensitivity) it fully describes how a test behaves.
- Gives a direct count of false alarms once you know the number of negatives.

**4. Limitations / Potential issues:**

- On very imbalanced data it stays near 100% even when false alarms outnumber real catches.
- Ignores the positive class completely: a model that flags nothing has 100% specificity.
- Depends on the cut-off.
- Often forgotten because common software libraries do not provide it directly.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Banned-substance screening for college athletes |
| Industry / Domain | sports administration |
| Business Problem | A US collegiate athletic conference screens athletes with a statistical model before confirmatory lab testing. Falsely accusing a clean athlete is a serious harm. |
| ML Translation | Target: athlete used a banned substance (1) or clean (0); binary classification; very low prevalence; 2,000 clean athletes in the validation group |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The principal ethical concern is the clean athletes. Specificity is exactly the share of them the model correctly clears, and it does not depend on how many dopers there are. |
| Why other metrics are NOT suitable here | Accuracy is dominated by clean athletes and hides the harm; recall (sensitivity) says nothing about clean athletes wrongly flagged; precision depends on how common doping is in the conference. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Every clean athlete wrongly flagged is a reputational injury and a potential lawsuit against the conference. |
| Small numeric example | 2,000 clean athletes: at specificity 99.5%, false flags = 2,000 × 0.005 = 10; at 99%, false flags = 2,000 × 0.01 = 20. Half a percentage point halves the number of wrongly accused athletes. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Not scrapping good brake pads |
| Industry / Domain | manufacturing |
| Business Problem | A Canadian auto-parts plant uses a camera to catch defective brake pads. A good pad wrongly rejected is scrapped, costing $85. The plant produces 4,000 good pads per shift. |
| ML Translation | Target: pad defective (1) or good (0); binary classification; low prevalence; 4,000 good pads per shift |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Yield and scrap cost are driven by how many good pads the camera lets through. Specificity states that share and converts into dollars. |
| Why other metrics are NOT suitable here | Accuracy is nearly the same as specificity here because most pads are good, and hides the defect side; recall is tracked separately for safety; precision depends on the daily defect rate and varies from shift to shift. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Ignoring specificity can silently destroy thousands of dollars of good product every shift. |
| Small numeric example | 4,000 good pads: at specificity 98%, scrapped = 4,000 × 0.02 = 80 pads = 80 × $85 = $6,800; at 99.5%, scrapped = 20 pads = $1,700. Saving = $5,100 per shift. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Name-match reviews in sanctions screening |
| Industry / Domain | banking |
| Business Problem | A US bank screens 100,000 genuine customer names a day against a sanctions list. Every false match needs a $22 manual review. |
| ML Translation | Target: name is on the sanctions list (1) or not (0); binary classification; extremely low prevalence; about 100,000 true non-matches daily |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Operations cost is driven by the share of innocent customers wrongly flagged, so the review team's workload follows from specificity times the daily volume. |
| Why other metrics are NOT suitable here | Accuracy hides everything behind the huge TN count; precision varies with how many listed names show up on a given day; recall tracks catches, not workload. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A drop of a few points of specificity can swamp the review team and delay legitimate customers. |
| Small numeric example | 100,000 genuine names: at specificity 99.5%, false matches = 500; cost = 500 × $22 = $11,000 per day. At 98%, false matches = 2,000; cost = $44,000 per day, four times higher. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Fake-account detector with 99% specificity and a flood of false alarms |
| Industry / Domain | e-commerce (cybersecurity) |
| Business Problem | A US online store scores 1,000,000 login sessions a day, of which only 200 are bot attacks. The security team wants to show leadership that the detector is "99% specific". |
| ML Translation | Target: session is a bot (1) or human (0); binary classification; 0.02% positives, extremely imbalanced; 999,800 human sessions |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The denominator is the huge human pool, so even a 1% false-alarm rate produces thousands of flagged humans, but 99% specificity still sounds excellent. |
| Why other metrics are NOT suitable here | Accuracy is above 98% and equally reassuring; ROC-AUC is also driven by the large negative pool and stays high; FPR repeats the same view as specificity. |
| Better alternative (if BAD fit) | Precision (share of flagged sessions that are real bots) and PR-AUC, which are sensitive to the number of false alarms relative to real catches. |
| Business impact of choosing wrong | Roughly 10,000 real customers a day are challenged or blocked, hurting sales and support costs, while leadership thinks the system is nearly perfect. |
| Small numeric example | Specificity 99%: false alarms = 999,800 × 0.01 = 9,998. Recall 80%: bots caught = 200 × 0.8 = 160. Precision = 160 / (160 + 9,998) = 1.6%; so about 98 of every 100 blocked sessions are real people. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Vacant-home detector that almost never bothers occupied homes |
| Industry / Domain | government (municipal by-law office) |
| Business Problem | A Canadian city by-law office wants to find derelict, vacant houses. Of 1,000 homes checked, 100 are vacant. Staff pick the model with the best specificity so that occupants are rarely bothered. |
| ML Translation | Target: home vacant (1) or occupied (0); binary classification; 10% positives; 1,000 homes, two candidate models |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Specificity ignores the positive class. Model A leaves occupants alone 99% of the time but finds only 30% of vacant homes. |
| Why other metrics are NOT suitable here | Accuracy rises for Model A simply because occupied homes dominate; precision alone favours the model that flags very few homes; recall alone would ignore the occupant burden. |
| Better alternative (if BAD fit) | Balanced accuracy (average of recall and specificity) or Youden's J (recall plus specificity minus 1), which require both classes to do well. |
| Business impact of choosing wrong | Most vacant houses remain undetected, creating fire, safety and neighbourhood blight problems the by-law office exists to prevent. |
| Small numeric example | Model A: TP 30, FN 70, FP 9, TN 891; specificity = 891 / 900 = 99%; recall = 30 / 100 = 30%; balanced accuracy = (0.30 + 0.99) / 2 = 0.645. Model B: TP 90, FN 10, FP 45, TN 855; specificity = 855 / 900 = 95%; recall = 90 / 100 = 90%; balanced accuracy = (0.90 + 0.95) / 2 = 0.925. |

**6. Quick decision rule:** Use specificity when wrongly flagging the innocent majority is the main harm and you need a prevalence-independent figure; avoid it as a stand-alone score on very imbalanced data, or whenever catching the positive class matters.

### False Positive Rate (FPR)

**1. What it measures (plain English):** Of all the real non-events, the share the model wrongly flagged. Also called the false alarm rate, fall-out or Type I error rate. It is 1 minus specificity.

`FPR = FP / (FP + TN) = 1 − Specificity`

**2. Intuition:** The share of ordinary days on which your smoke alarm goes off because of burnt toast.

**3. Benefits:**

- The horizontal axis of the ROC curve, so it is essential for threshold-free comparison.
- Does not depend on prevalence.
- Turns into an absolute false-alarm count once multiplied by the number of negatives.
- Shared language with statistics (the Type I error or significance level alpha).

**4. Limitations / Potential issues:**

- On imbalanced data, a tiny FPR can still mean a huge absolute number of false alarms.
- Ignores the positive class entirely.
- Depends on the cut-off.
- Often confused with the false discovery rate (FP divided by all flagged cases), which is a different quantity.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Face-match kiosks at a border crossing |
| Industry / Domain | travel and border services |
| Business Problem | A Canadian border agency uses face-matching kiosks. Wrongly accepting an impostor as the passport holder is a security failure, so the system is specified with a false-accept budget. |
| ML Translation | Target: faces belong to the same person (1) or not (0); binary classification; impostor comparisons are the negative class; 200,000 impostor attempts per year in a trial |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The security requirement is written as the share of impostors wrongly accepted (false accept rate, which is FPR). It is independent of how many genuine travellers pass through. |
| Why other metrics are NOT suitable here | Accuracy is dominated by genuine travellers; precision changes with the genuine-to-impostor mix on a given day; recall (genuine travellers accepted) only measures convenience, not security. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | An unspecified false-accept rate lets impostors through; a vendor could meet "99% accuracy" and still be unsafe. |
| Small numeric example | 200,000 impostor attempts: at FPR 0.00001 (1 in 100,000), false accepts = 200,000 × 0.00001 = 2; at FPR 0.001, false accepts = 200,000 × 0.001 = 200, a hundred times more. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — A hospital security team's daily false-alert budget |
| Industry / Domain | cybersecurity (hospital IT) |
| Business Problem | A US hospital system's security team can investigate at most 50 false alerts a day. Its network generates about 100,000 harmless events daily. |
| ML Translation | Target: event is malicious (1) or benign (0); binary classification; extremely low prevalence; 100,000 benign events per day |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The team's capacity is a count of false alerts, and FPR times the number of benign events gives exactly that count. It sets a clear limit on the model. |
| Why other metrics are NOT suitable here | Accuracy hides the false alerts in the enormous benign pool; precision shifts with the number of real attacks on a given day; F1 does not tell the team how many alerts they must clear. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Exceeding the alert budget causes alert fatigue, and analysts begin to ignore alerts, including real intrusions. |
| Small numeric example | Budget: 50 false alerts / 100,000 benign events = FPR 0.0005. A model at FPR 0.002 gives 100,000 × 0.002 = 200 false alerts a day, four times the capacity; the cut-off must be raised until FPR is at most 0.0005. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Experiments that "win" by luck |
| Industry / Domain | e-commerce (experimentation) |
| Business Problem | A US online retailer runs 40 website experiments in a quarter in which, unknown to the team, the change has no real effect. A "winner" declared at the 5% significance level is a false positive, and rolling it out costs $15,000 of engineering and lost sales. |
| ML Translation | Target: experiment has a real effect (1) or not (0); binary decision; the 40 experiments with no real effect are all negatives |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The significance level alpha is, by definition, the FPR of the testing procedure. Setting it sets the expected number of false winners. |
| Why other metrics are NOT suitable here | Accuracy cannot be computed without knowing the true effects; precision depends on how many real effects exist in the pipeline; recall (power) addresses missed real effects, not lucky wins. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Ignoring the false-positive rate leads to rolling out changes that do nothing, at real cost. |
| Small numeric example | At alpha 0.05: expected false winners = 40 × 0.05 = 2; cost = 2 × $15,000 = $30,000. At alpha 0.01: expected false winners = 40 × 0.01 = 0.4, about one false winner every 2.5 quarters. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — A tiny FPR across four million smart meters |
| Industry / Domain | energy |
| Business Problem | A US utility's tamper-alert model has a false positive rate of just 0.2% on its 4,000,000 untampered smart meters. Each alert triggers a $95 field visit. Of 500 truly tampered meters, it catches 400. |
| ML Translation | Target: meter tampered (1) or normal (0); binary classification; 0.0125% positives; 4,000,000 normal meters |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | 0.2% sounds negligible, but it is applied to a huge base. FPR alone says nothing about how many alerts are false, or how they compare with the real catches. |
| Why other metrics are NOT suitable here | Specificity (99.8%) repeats the same reassuring view; accuracy is above 99.7%; ROC-AUC is driven by the same huge negative pool. |
| Better alternative (if BAD fit) | Absolute false-alert count with precision (or false discovery rate), and PR-AUC, because they show the field-crew workload. |
| Business impact of choosing wrong | The utility sends crews on thousands of pointless visits and spends far more than the recovered revenue. |
| Small numeric example | False alerts = 4,000,000 × 0.002 = 8,000; cost = 8,000 × $95 = $760,000. True catches = 400; precision = 400 / (400 + 8,000) = 4.76%; so false discovery rate = 8,000 / 8,400 = 95.2%. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Compound screening: a 5% false positive rate that makes 92% of hits false |
| Industry / Domain | pharmaceutical research |
| Business Problem | A Canadian biotech lab screens 20,000 compounds for activity against a target. Only 100 are truly active. A statistician reassures the team that the test runs at a 5% false positive rate. |
| ML Translation | Target: compound truly active (1) or not (0); binary classification; 0.5% positives; 19,900 inactive compounds |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | FPR is the share of inactive compounds wrongly flagged, but the lab's question is "of the hits we follow up, how many are real?" With so few real actives, most hits are false. |
| Why other metrics are NOT suitable here | Specificity is the same 95% view; accuracy is about 95% and hides the problem; recall tells how many actives were found, not how many hits are junk. |
| Better alternative (if BAD fit) | False discovery rate (share of hits that are false, 1 minus precision) with a correction such as Benjamini-Hochberg, which controls it. |
| Business impact of choosing wrong | The lab spends follow-up experiments on about 995 false hits to find about 90 real ones, burning months and budget. |
| Small numeric example | False hits = 19,900 × 0.05 = 995. Real hits at 90% recall = 100 × 0.9 = 90. Total hits = 1,085. False discovery rate = 995 / 1,085 = 91.7%; precision = 90 / 1,085 = 8.3%. |

**6. Quick decision rule:** Use FPR when you need a prevalence-independent false-alarm budget, a ROC curve or a Type I error level; avoid it as the only measure when negatives vastly outnumber positives and the real question is how many alerts are wrong.

### False Negative Rate (FNR)

**1. What it measures (plain English):** Of all the real events, the share the model missed. Also called the miss rate or Type II error rate. It is 1 minus recall.

`FNR = FN / (FN + TP) = 1 − Recall`

**2. Intuition:** The share of real fires your smoke alarm stayed silent through. It states the same fact as recall, but as a risk.

**3. Benefits:**

- Frames performance as risk, which safety and compliance teams use.
- Does not depend on prevalence.
- Multiplies by the number of real events and the cost per miss to give expected loss.
- Easy to compare with a regulatory or contractual maximum.

**4. Limitations / Potential issues:**

- Ignores the negative class, so it must be paired with FPR.
- Can be driven to zero by flagging everything.
- Depends on the cut-off.
- Noisy when there are few real positives.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Engine blade cracks found during borescope inspection |
| Industry / Domain | aviation maintenance |
| Business Problem | A US regional airline uses an image model to spot cracks in engine blades during borescope (camera) inspections. Its safety case requires a miss rate of at most 2%. A missed crack can cost about $90,000 in blade failure and engine removal. |
| ML Translation | Target: blade cracked (1) or sound (0); binary classification; low prevalence; 200 known-cracked blades in the validation set |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The safety regulation is written as a maximum miss rate. FNR can be compared directly with the 2% limit and converted into expected loss. |
| Why other metrics are NOT suitable here | Accuracy cannot be tied to the safety limit and is dominated by sound blades; precision does not measure misses; AUC does not state a pass or fail at the chosen operating point. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A model that fails the miss-rate requirement cannot be certified, and a miss can cause an in-flight failure. |
| Small numeric example | Model A misses 3 of 200: FNR = 3 / 200 = 1.5%, passes; expected loss = 3 × $90,000 = $270,000. Model B misses 12 of 200: FNR = 12 / 200 = 6%, fails; expected loss = 12 × $90,000 = $1,080,000. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Metal fragments slipping past the packing-line X-ray |
| Industry / Domain | food manufacturing |
| Business Problem | A Canadian food processor uses an X-ray model to catch metal fragments in packs. About 2,000 contaminated packs pass the line each year. Each pack that escapes costs about $4,000 in complaints and partial recalls. |
| ML Translation | Target: pack contaminated (1) or clean (0); binary classification; low prevalence; 2,000 contaminated packs a year |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Management budgets for the number of contaminated packs that escape. FNR times 2,000 times $4,000 gives that exposure directly. |
| Why other metrics are NOT suitable here | Accuracy is dominated by clean packs; precision describes rejected packs, not escapes; specificity measures good packs kept, not contamination missed. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Contaminated food reaching shoppers means injuries, recalls and lasting brand damage. |
| Small numeric example | At FNR 2%: escapes = 2,000 × 0.02 = 40; cost = 40 × $4,000 = $160,000. At FNR 1%: escapes = 20; cost = $80,000. Halving the miss rate saves $80,000 a year. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — High-risk applicants slipping through the fast-track lane |
| Industry / Domain | insurance |
| Business Problem | A US life insurer's screening model sends high-risk applicants to full medical underwriting. About 400 high-risk applicants apply a year, and each one missed costs about $18,000 in excess claims. |
| ML Translation | Target: applicant is high risk (1) or standard (0); binary classification; low prevalence; 400 high-risk applicants a year |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The business loss depends on how many high-risk applicants are missed. FNR gives that share, which times 400 times $18,000 is the loss. |
| Why other metrics are NOT suitable here | Accuracy is dominated by standard applicants; precision says nothing about the misses; AUC does not give the cost at the working cut-off. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | An unmeasured miss rate leads to underpriced policies and excess claims year after year. |
| Small numeric example | At FNR 25%: misses = 400 × 0.25 = 100. At FNR 15%: misses = 400 × 0.15 = 60. Fewer misses = 40; saving = 40 × $18,000 = $720,000 a year. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Flagging every student gives a perfect miss rate and no help |
| Industry / Domain | education |
| Business Problem | A US university wants to reach students at risk of dropping out. Advisors can contact only 300 of its 5,000 students. A proposal says to flag all students, since then the miss rate is zero. |
| ML Translation | Target: student drops out (1) or not (0); binary classification; 8% positives (400 at-risk students); advisor capacity of 300 contacts |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Flagging everyone gives FNR 0%, but the advisors can only contact 300, so most contacts go to students who are fine. FNR does not take capacity into account. |
| Why other metrics are NOT suitable here | Accuracy for flag-all is just 8%; precision for flag-all is the same 8%; recall equals 1 minus FNR and shares the same flaw. |
| Better alternative (if BAD fit) | Recall at k and precision at k (computed on the top 300 students), because they measure what advisors can actually do. |
| Business impact of choosing wrong | Advisors reach almost no one who needs help, dropouts continue and tuition revenue is lost. |
| Small numeric example | Flag-all: FNR = 0%, but contacting any 300 students at random reaches 300 × 400 / 5,000 = 24 at-risk students. Ranked model: top 300 contains 180 at-risk students; precision@300 = 180 / 300 = 60%; recall = 180 / 400 = 45%; FNR = 220 / 400 = 55%, yet 180 at-risk students are reached, 7.5 times as many as 24. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Port container screening: a 10% miss rate and a 99.9% clean fast lane |
| Industry / Domain | logistics (port customs) |
| Business Problem | A Canadian port screens 10,000 containers with a model and releases cleared containers to a fast lane without a physical inspection. The customs manager rejects the model because its miss rate is 10%. |
| ML Translation | Target: container holds contraband (1) or not (0); binary classification; 1% positives (100 containers); 10,000 containers |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The fast-lane decision depends on what share of cleared containers is actually bad, not on what share of all bad containers was missed. FNR uses the wrong denominator for this question. |
| Why other metrics are NOT suitable here | Recall is just 1 minus FNR; accuracy hides the miss pattern; precision describes flagged containers, not cleared ones. |
| Better alternative (if BAD fit) | Negative predictive value (share of cleared containers that are truly clean), or its complement the false omission rate, because it describes the fast lane. |
| Business impact of choosing wrong | A model that would clear 9,010 containers with only 10 bad ones is wrongly rejected, and the port keeps inspecting thousands of clean containers manually. |
| Small numeric example | TP 90, FN 10, FP 900, TN 9,000. FNR = 10 / 100 = 10%. Cleared = 9,000 + 10 = 9,010. False omission rate = 10 / 9,010 = 0.11%; NPV = 9,000 / 9,010 = 99.89%. |

**6. Quick decision rule:** Use FNR when you must state or cap the share of real events that are missed, for example in a safety case or a contract; avoid it as a stand-alone score when capacity is limited, when flagging everything would trivially win, or when the decision is about what happens to cleared cases.

### Negative Predictive Value (NPV)

**1. What it measures (plain English):** Of everything the model cleared as negative, the share that really was negative. It is precision's counterpart for the "all clear" side. It tells you how far to trust a "no problem" result.

`NPV = TN / (TN + FN)`

**2. Intuition:** A building inspector who signs off 75 buildings as safe: NPV is the share of those 75 that really are safe.

**3. Benefits:**

- Measures how reliable the "all clear" decision is, which almost no other common metric does.
- Lets a team skip further checks on cleared cases when it is very high.
- Directly readable as a probability: the chance that a cleared case is truly negative.
- Pairs with PPV (precision) to say what each possible result means.

**4. Limitations / Potential issues:**

- Depends on prevalence: the same model has a lower NPV where the event is more common.
- Deceptively high on rare events: always saying "negative" gives NPV equal to the share of negatives.
- Undefined when nothing is cleared.
- Depends on the cut-off.
- Rarely reported, so it is often missed.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Sending low-risk chest-pain patients home without repeat blood tests |
| Industry / Domain | healthcare |
| Business Problem | A Canadian emergency department uses a risk model to rule out heart attack in low-risk chest-pain patients, skipping a second troponin blood test that costs $120. A wrongly cleared patient is dangerous. |
| ML Translation | Target: patient has a heart attack (1) or not (0); binary classification; low prevalence in the low-risk group; 600 patients cleared by the model |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The decision is to rely on a negative result. NPV is the probability that a patient told "all clear" truly has no heart attack. |
| Why other metrics are NOT suitable here | Specificity says how many healthy patients are cleared, not how safe a clearance is; precision describes only flagged patients; accuracy mixes both kinds of decisions. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A low NPV sends sick patients home with false reassurance; skipping the rule-out entirely wastes money on tests for the majority. |
| Small numeric example | 600 cleared patients, 3 had heart attacks: NPV = 597 / 600 = 99.5%. Savings from skipping repeat tests = 600 × $120 = $72,000; the 3 missed cases are the safety exposure to review against the target. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Auto-paying small property claims without an adjuster |
| Industry / Domain | insurance |
| Business Problem | A US property insurer wants to pay small claims (under $2,500) instantly when the model says "no problem found", skipping a $140 adjuster visit. Of the claims paid blind, some will contain an overpayment of about $1,400. |
| ML Translation | Target: claim has a problem such as overstated damage (1) or fine (0); binary classification; low prevalence in small claims; 1,000 fast-tracked claims |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The business is relying on the cleared group being clean. NPV is the share of fast-tracked claims that really are fine. |
| Why other metrics are NOT suitable here | Recall tells how many problem claims were caught overall, not how clean the fast lane is; specificity ignores the problem claims inside the lane; accuracy mixes in the flagged group. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | If NPV is lower than expected, overpayments erase the savings; if it is much higher, the insurer under-uses the fast lane. |
| Small numeric example | 1,000 fast-tracked claims, 30 problem claims: NPV = 970 / 1,000 = 97%. Overpaid = 30 × $1,400 = $42,000; adjuster visits avoided = 1,000 × $140 = $140,000; net saving = $98,000. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Skipping the burn-in test for circuit boards that pass vision inspection |
| Industry / Domain | manufacturing |
| Business Problem | A US electronics assembler skips a $4 burn-in test (a heat stress test) for boards its vision model passes. A bad board that reaches a customer costs $310 in warranty repair. |
| ML Translation | Target: board is defective (1) or good (0); binary classification; low prevalence; 5,000 boards passed by the model |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The test is skipped for the "passed" group, so the question is how clean that group is. NPV answers it and converts into a clear cost comparison. |
| Why other metrics are NOT suitable here | Recall measures defects caught overall, not the contents of the skipped group; specificity ignores the defects hiding in that group; precision is about rejected boards. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Too optimistic an NPV sends many bad boards to customers; too cautious a view keeps paying for needless burn-in tests. |
| Small numeric example | 5,000 passed boards, 25 defective: NPV = 4,975 / 5,000 = 99.5%. Burn-in saving = 5,000 × $4 = $20,000; warranty cost = 25 × $310 = $7,750; net saving = $12,250. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Crop-blight scans where "no blight" is right 99.5% of the time by default |
| Industry / Domain | agriculture |
| Business Problem | A US Midwest farm cooperative uses drone images to flag blighted fields. Only 0.5% of fields have blight. The agronomist reports an NPV of 99.5% as proof the system is trustworthy. |
| ML Translation | Target: field blighted (1) or healthy (0); binary classification; 0.5% positives; 2,000 fields in the test |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | When nearly all fields are healthy, any model that mostly says "healthy" has a very high NPV. The metric barely moves, so it cannot show whether the model works. |
| Why other metrics are NOT suitable here | Accuracy has the same problem (99.5% for do-nothing); specificity is also near 100%; error rate is under 1% for every model. |
| Better alternative (if BAD fit) | Recall (blighted fields found) and precision (flagged fields that are blighted), or PR-AUC, because they focus on the rare class. |
| Business impact of choosing wrong | A do-nothing system gets approved, blight spreads across neighbouring fields and a whole season's yield is at risk. |
| Small numeric example | Always-healthy: NPV = 1,990 / 2,000 = 99.5%; recall = 0%. Real model: TP 7, FN 3, FP 20, TN 1,970; NPV = 1,970 / 1,973 = 99.85% (almost the same); recall = 7 / 10 = 70%; precision = 7 / 27 = 25.9%. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — A bridge-deck rule-out test that fails in the oldest part of the network |
| Industry / Domain | civil infrastructure |
| Business Problem | A US state transportation agency validated a drone-based screening model on mostly newer bridges, where it ruled out hidden deck damage with a 99.5% NPV. It now plans to rely on the same "all clear" in an older region where damage is much more common. |
| ML Translation | Target: deck has hidden damage (1) or sound (0); binary classification; prevalence 2% in the validation set and 30% in the older region; 1,000 decks each |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | NPV depends on how common damage is. The model's sensitivity and specificity are unchanged, but the share of damaged decks among "all clear" decks grows sharply in the old region. |
| Why other metrics are NOT suitable here | Accuracy also shifts with prevalence; precision of the flagged group is just as population-dependent; raw TN counts scale with the number of decks. |
| Better alternative (if BAD fit) | Sensitivity (recall) and specificity, which stay fixed across regions, and then recompute NPV for the new prevalence with Bayes' rule. |
| Business impact of choosing wrong | Roughly one in eleven "cleared" old decks would actually be damaged, a serious public-safety risk if inspections are skipped. |
| Small numeric example | Sensitivity 0.80 and specificity 0.90 in both. Validation (2%): TP 16, FN 4, FP 98, TN 882; NPV = 882 / 886 = 99.5%. Older region (30%): TP 240, FN 60, FP 70, TN 630; NPV = 630 / 690 = 91.3%; 60 damaged decks per 1,000 are cleared, compared with 4. |

**6. Quick decision rule:** Use NPV when you plan to act on a negative result, such as skipping a test or paying a claim, and the event is common enough for NPV to have room to move; avoid it as a headline number on very rare events, or when moving a model to a population with different prevalence without recomputing it.
