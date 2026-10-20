# Classification Case Studies, Part 4: Ranking and Curve-Based Metrics

## Table of Contents

- [ROC and AUC Family](#roc-and-auc-family)
  - [ROC Curve](#roc-curve)
  - [ROC-AUC](#roc-auc)
  - [Precision-Recall Curve](#precision-recall-curve)
  - [PR-AUC](#pr-auc)
  - [Average Precision (AP)](#average-precision-ap)
- [Targeting and Capacity Metrics](#targeting-and-capacity-metrics)
  - [Lift (Lift Curve and Lift at Decile)](#lift-lift-curve-and-lift-at-decile)
  - [Cumulative Gain (Gains Chart)](#cumulative-gain-gains-chart)
- [Scorecard and Separation Metrics](#scorecard-and-separation-metrics)
  - [KS Statistic](#ks-statistic)
  - [Gini Coefficient [Added – not in source file]](#gini-coefficient-added--not-in-source-file)

**How to read this part:** every metric here judges a model by how well it _orders_ cases from most to least likely positive, not by one fixed yes/no cut-off (the "threshold"). Each metric has five real-world cases, some where it is the right tool and some where it misleads. "Positive" means the case we are hunting for (a fraud, a defect, a buyer); "prevalence" means the share of cases that are truly positive; "imbalanced" means positives are rare.

## ROC and AUC Family

### ROC Curve

**1. What it measures (plain English):** The ROC curve (Receiver Operating Characteristic curve) draws, for every possible cut-off, the share of real positives you catch (true positive rate, also called recall or sensitivity) against the share of real negatives you wrongly flag (false positive rate, which is 1 minus specificity). It shows the whole trade-off menu in one picture instead of one snapshot.

`TPR = TP / (TP + FN)` on the y-axis and `FPR = FP / (FP + TN)` on the x-axis

**2. Intuition:** Think of a smoke alarm with a sensitivity dial. Turn it from "never ring" to "ring at everything" and note, at each setting, how many real fires it caught and how many burnt-toast false alarms it raised. The curve is the record of that dial turn; the diagonal line is an alarm that rings at random.

**3. Benefits:**

- Shows every operating point at once, so you can pick a cut-off that satisfies a hard limit such as "no more than 2% false alarms".
- Both axes are ratios inside their own true class, so the curve does not move when the share of positives changes. This makes it fair for comparing a model across populations.
- Easy for non-technical people to read: closer to the top-left corner is better.
- Lets you compare models whose scores are on different scales.

**4. Limitations / Potential issues:**

- Over-optimistic on imbalanced data: the false positive rate divides by the huge negative class, so thousands of false alarms look tiny.
- Hides absolute counts: a false positive rate of 1% sounds negligible but is 10,000 false alarms among a million negatives.
- Says nothing about calibration (whether a score of 0.8 really means 80% chance).
- The top-left point maximises TPR minus FPR, which silently assumes a miss and a false alarm cost the same.
- Curves can cross, so no single model wins everywhere; you must look at the region you will actually use.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — The Wafer Line That Can Only Stop So Often |
| Industry / Domain | Manufacturing |
| Business Problem | A Korean memory-chip fab screens wafers after etching. Every flagged wafer pauses a tool for re-inspection, so engineers accept flagging at most 10% of good wafers but want to catch as many defective wafers as possible. Two candidate models are being compared. |
| ML Translation | Target: wafer defective (1) or good (0); binary classification with a continuous risk score; test batch of 10 defective and 20 good wafers; the false-alarm limit is a hard business constraint. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The business gave a ceiling on false alarms, and the ROC curve lets you read the best catch rate at exactly that ceiling for each model, even though the two curves cross. |
| Why other metrics are NOT suitable here | Accuracy at one threshold hides the false-alarm limit and the trade-off; F1 mixes precision and recall and ignores the stated FPR cap; a single ROC-AUC number averages over regions the fab will never use, and the curves cross. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Picking the weaker model at the 10% limit lets about one more defective wafer in every ten flow on to packaging, where scrapping it costs far more than catching it at inspection. |
| Small numeric example | Model A (TP, FP) at three cut-offs: (6,1), (7,2), (9,4) → TPR 0.60, 0.70, 0.90 and FPR 1/20=0.05, 2/20=0.10, 4/20=0.20. Model B: (5,1), (8,2), (9,3) → TPR 0.50, 0.80, 0.90 and FPR 0.05, 0.10, 0.15. At the FPR cap of 0.10: A catches 0.70, B catches 0.80 → choose B. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — One X-ray Reader, Two Very Different Clinics |
| Industry / Domain | Healthcare |
| Business Problem | A Thai hospital network deploys the same AI chest X-ray triage tool in a district screening clinic (about 5% of patients have tuberculosis) and in a provincial referral hospital (about 20%). The medical director asks whether the tool works equally well in both places. |
| ML Translation | Target: tuberculosis present (1) or not (0); binary classification score; two populations with different prevalence; question is about discriminative ability, not about local workload. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Both ROC axes are ratios inside the sick group and inside the healthy group, so the curve is identical in both clinics when the tool has the same discriminative power. A change in the curve would signal a real change in the tool. |
| Why other metrics are NOT suitable here | Precision and the precision-recall curve move with prevalence, so they would wrongly suggest the tool changed; accuracy is mostly the healthy majority; F1 also depends on prevalence. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Judging by precision would make the network retrain or abandon a tool that is fine in the screening clinic, or trust it blindly in the referral hospital, wasting AI budget and clinician trust. |
| Small numeric example | Same operating point in both: TPR 0.85, FPR 0.10. Clinic A: 100 sick, 1,900 healthy → TP 85, FP 190, precision 85/275=0.31. Clinic B: 100 sick, 400 healthy → TP 85, FP 40, precision 85/125=0.68. ROC point (0.10, 0.85) is the same; precision looks very different. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Face Check at the Wallet Door |
| Industry / Domain | Banking (digital payments) |
| Business Problem | A Singapore e-wallet verifies selfies at sign-up. Policy says no more than 2% of genuine customers may be wrongly blocked, but the security team wants to stop as many impostor attempts as possible. They must choose a score cut-off. |
| ML Translation | Target: impostor attempt (1) versus genuine customer (0); binary classification from a face-match score; 50 impostor attempts and 950 genuine users in the test set; constraint is on the false positive rate. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The policy is literally a point on the x-axis (FPR 2%). The ROC curve shows the best catch rate you can buy at that point and what it costs to go beyond it. |
| Why other metrics are NOT suitable here | Accuracy rewards accepting everybody (95% of attempts are genuine); precision at one cut-off does not show the FPR policy; a single ROC-AUC value cannot enforce a cap. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Ignoring the cap would either block thousands of genuine sign-ups (lost customers, complaints, regulator attention) or let impostors open accounts used for mule transfers. |
| Small numeric example | Cut-offs (TP, FP): (40,5), (44,19), (48,95). TPR = 0.80, 0.88, 0.96 (out of 50); FPR = 5/950=0.005, 19/950=0.02, 95/950=0.10. The 2% cap allows the second cut-off: 44 of 50 impostors caught, 19 genuine users blocked. The third cut-off breaks policy (95 blocked). |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Hunting Fake Driver Accounts in a Sea of Real Ones |
| Industry / Domain | Logistics (ride-hailing) |
| Business Problem | A Vietnamese ride-hailing platform wants to catch fake driver accounts (stolen identities, rented profiles). Only about 0.2% of 100,000 accounts are fake, and a small trust-and-safety team must manually review every flagged account. |
| ML Translation | Target: fake account (1) or real (0); heavily imbalanced binary classification (200 positives, 99,800 negatives); the real cost driver is the number of reviews wasted on real drivers. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | At TPR 0.90 and FPR 0.02 the ROC point looks superb (near the top-left), but 2% of 99,800 real accounts is almost 2,000 false alarms. The curve divides by the huge negative group and hides the reviewers' real workload. |
| Why other metrics are NOT suitable here | Accuracy is 99.8% by flagging nobody; ROC-AUC inherits the same blind spot; F1 at a single cut-off lacks the full trade-off. |
| Better alternative (if BAD fit) | Precision-recall curve (with the prevalence baseline line at 0.002), because precision divides by the flagged accounts and shows the wasted reviews directly. |
| Business impact of choosing wrong | Investigators spend roughly 92 of every 100 reviews on genuine drivers, who are temporarily locked out and lose a day of income, while real fraud rings wait in the queue. |
| Small numeric example | Fake = 200, real = 99,800. TPR 0.90 → TP = 180. FPR 0.02 → FP = 0.02 × 99,800 = 1,996. Flagged = 2,176. ROC point (0.02, 0.90) looks excellent; precision = 180/2,176 = 0.083, versus a 0.002 baseline. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — The Fall Alert That Should Err on the Side of Waking the Nurse |
| Industry / Domain | Healthcare (elderly care) |
| Business Problem | A Japanese nursing-home operator uses bed-sensor data to predict falls. A missed fall means a hospital stay costing about ¥400,000; a false alert costs about ¥3,000 of staff time. Management plans to use the ROC point closest to the top-left corner as the cut-off. |
| ML Translation | Target: fall in the next window (1) or not (0); binary classification score; 10 falls among 200 alert windows (190 non-falls); costs of the two error types are very unequal. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The top-left point maximises TPR minus FPR, which treats a miss and a false alarm as equal. Here a miss is worth about 133 false alarms, so the geometric best point is not the cheapest point. |
| Why other metrics are NOT suitable here | Accuracy ignores the cost gap; ROC-AUC says nothing about which cut-off to use; precision alone ignores that missed falls are the expensive error. |
| Better alternative (if BAD fit) | Expected-cost analysis: total cost = misses × ¥400,000 + false alerts × ¥3,000 at each cut-off, and pick the cheapest. |
| Business impact of choosing wrong | The "best-looking" cut-off lets extra falls through; each avoidable fall is a injured resident, a hospital bill and possible liability. |
| Small numeric example | Cut-off 1: TP 8, FP 8 → TPR 0.80, FPR 8/190=0.042, gap 0.758 (the top-left winner). Cost = 2 × ¥400,000 + 8 × ¥3,000 = ¥824,000. Cut-off 2: TP 9, FP 38 → TPR 0.90, FPR 0.20, gap 0.70. Cost = 1 × ¥400,000 + 38 × ¥3,000 = ¥514,000. The cut-off with the lower gap is ¥310,000 cheaper. |

**6. Quick decision rule:** Use the ROC curve when you must compare models before a cut-off is chosen, when a limit on false alarms is fixed, or when comparing across populations with different prevalence; avoid it when positives are very rare and false alarms use scarce capacity (use the precision-recall curve) or when the two error costs differ a lot (use an expected-cost analysis).

### ROC-AUC

**1. What it measures (plain English):** ROC-AUC (also written AUC, AUROC, or "area under the ROC curve") is one number from 0 to 1 summarising the whole ROC curve. Its exact meaning: the chance that a randomly picked positive gets a higher score than a randomly picked negative. 0.5 is a coin flip, 1.0 is perfect ordering.

`ROC-AUC = (correctly ordered positive-negative pairs + 0.5 × tied pairs) / (number of positives × number of negatives)`

**2. Intuition:** Imagine a school quiz where you pick one student who studied and one who did not, and ask who scored higher. ROC-AUC is how often the "studied" student wins over many such pairings. It only cares about who is ahead, not by how much.

**3. Benefits:**

- One number, no threshold needed, so model comparison and automated tuning are easy.
- Easy to explain: "the model ranks a random positive above a random negative this often".
- Unaffected by changes in prevalence and by any order-preserving transformation of the scores, so it never punishes an uncalibrated model.
- Standard for monitoring: a drop over time is an early warning of drift (the world changing under the model).

**4. Limitations / Potential issues:**

- Misleading on imbalanced data: false positives are divided by the enormous negative class, so AUC can be 0.95 while precision is below 10%. A model can look great on this number and still bury analysts in false alarms.
- Blind to calibration: a high AUC does not mean predicted probabilities are usable as real probabilities.
- Averages over regions nobody operates in; when only the top of the list is used, partial AUC or precision at k is more honest.
- Cannot express unequal error costs, and has high variance on small test sets.
- Two models with identical AUC can behave very differently in the region you use.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Picking the Upgrade-Propensity Model Before the Campaign Is Sized |
| Industry / Domain | Telecom |
| Business Problem | An Indonesian mobile operator wants to find subscribers likely to move to a 5G plan. Roughly a third of the base upgrades eventually, the campaign size is not yet decided, and the data team must choose between two candidate models. |
| ML Translation | Target: upgraded within 90 days (1) or not (0); binary classification producing a score; moderate class balance; the choice must hold for any later campaign size. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Classes are not rare, both kinds of ordering error matter, and the cut-off is unknown. AUC rates the whole ranking and is stable, so it is a fair way to pick the better model first. |
| Why other metrics are NOT suitable here | Accuracy and F1 depend on a cut-off that has not been chosen; log loss rewards good probabilities while the team only needs the ranking; KS looks at only one point of the curve. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | The weaker model would send 5G offers to the wrong subscribers, wasting SMS and call-centre budget and annoying customers who will never upgrade. |
| Small numeric example | 4 upgraders and 4 non-upgraders → 16 pairs. Model A scores: upgraders 0.9, 0.7, 0.6, 0.4; non-upgraders 0.8, 0.5, 0.3, 0.2 → correct pairs 12 → AUC 12/16 = 0.75. Model B: upgraders 0.8, 0.65, 0.5, 0.45; non-upgraders 0.7, 0.6, 0.55, 0.3 → correct pairs 9 → AUC 9/16 = 0.56. Choose A. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — The Quarterly Parcel-Risk Health Check |
| Industry / Domain | Logistics (parcel delivery) |
| Business Problem | A Thai parcel carrier monitors a model that scores each parcel for the risk of a failed delivery attempt, every quarter. Operations wants a single, stable number that shows whether the model still separates risky parcels from safe ones, even though monsoon and festival seasons change the share of failed deliveries. |
| ML Translation | Target: delivery attempt fails (1) or succeeds (0); binary classification score; same model scored on a new quarter each time; prevalence drifts with the season. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | AUC does not move just because the failure rate rises or falls, so a fall in AUC points to real loss of ranking power rather than a shifting season. |
| Why other metrics are NOT suitable here | Accuracy and precision move with the failure rate; KS reports a single point and is noisier; log loss mixes calibration drift with ranking drift, so a change is hard to diagnose. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A drifting model keeps sending risky parcels down the normal route and holding back safe ones for months before complaints reveal it, so early detection saves re-delivery costs. |
| Small numeric example | Quarter 1 (4 failed, 4 delivered, 16 pairs): 14 correct pairs → AUC 0.875. Quarter 3: 10 correct pairs → AUC 0.625. A fall of 0.25 triggers a model review. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — The Merchant Collusion Rings Nobody Could Find |
| Industry / Domain | Payments (super-app) |
| Business Problem | A Chinese super-app wants to flag merchants taking part in collusion rings that fake sales to farm cashback. Only about 0.1% of 20,000 merchants are in a ring, and risk analysts can read only a short list. |
| ML Translation | Target: merchant in a collusion ring (1) or not (0); extremely imbalanced binary classification (20 positives, 19,980 negatives); cost driven by analyst time on false alarms. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | A model at TPR 0.90 and FPR 0.05 has an excellent-looking ROC picture (AUC in the 0.9s is plausible), yet 5% of 19,980 clean merchants is about 1,000 false alarms. AUC does not show this. |
| Why other metrics are NOT suitable here | Accuracy is 99.9% by flagging nobody; the ROC curve shares the same blind spot; the KS statistic uses the same FPR axis. |
| Better alternative (if BAD fit) | PR-AUC / Average Precision with the 0.001 baseline, plus precision at the analysts' list size. |
| Business impact of choosing wrong | Analysts chase about 1,017 merchants to find 18 rings (98% wasted) while honest merchants have payouts frozen, and the cashback leak continues. |
| Small numeric example | TP = 0.90 × 20 = 18. FP = 0.05 × 19,980 = 999. Flagged = 1,017. ROC point (0.05, 0.90) looks near the top-left. Precision = 18/1,017 = 0.018, only 18 times the 0.001 baseline and mostly noise. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Two Counterfeit Detectors With the Same Score and Different Mornings |
| Industry / Domain | E-commerce |
| Business Problem | A Vietnamese online marketplace has reviewers who check only the top 3 listings of a risk-ranked list each morning for counterfeit goods. Two models have the same ROC-AUC, so the team wants to know which one to deploy. |
| ML Translation | Target: counterfeit listing (1) or genuine (0); binary classification from a risk score; 12 test listings with 3 counterfeits; only the top of the ranking is used. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | AUC averages over the whole list, including positions reviewers never read. Two very different top-of-list behaviours can share one AUC. |
| Why other metrics are NOT suitable here | Accuracy needs a cut-off; the ROC curve repeats the same averaging; a single KS value shows nothing about the top 3. |
| Better alternative (if BAD fit) | Precision at k (k = reviewer capacity = 3), or Average Precision, which rewards finding positives early. |
| Business impact of choosing wrong | The wrong model leaves counterfeits live on the site for another day, risking buyer complaints, refunds and brand-owner disputes. |
| Small numeric example | 9 genuine + 3 counterfeit = 27 pairs. Model X has counterfeits at ranks 1, 2, 9; Model Y at ranks 3, 4, 5. Both AUC = 21/27 = 0.78. Precision at 3: X = 2/3 = 0.67, Y = 1/3 = 0.33. Average Precision: X 0.78, Y 0.48. If reviewers could check 5, Y would win (3/5 versus 2/5): the capacity decides. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Pricing Motor Cover From Probabilities That Are Half Right |
| Industry / Domain | Insurance |
| Business Problem | A Japanese non-life insurer wants to set premiums from each policyholder's predicted claim probability. Two models rank customers identically but one produces probabilities that are half the size of the other. |
| ML Translation | Target: at least one claim this year (1) or not (0); the output is used as a probability inside a pricing formula, so calibration (whether predicted chances match real frequencies) matters. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | AUC depends only on order, so it cannot tell a model whose probabilities are right from one whose probabilities are halved. |
| Why other metrics are NOT suitable here | Accuracy at a cut-off ignores the probability level; KS and the ROC curve are also order-only; precision and recall at a threshold do not test pricing accuracy. |
| Better alternative (if BAD fit) | Brier score or log loss together with a calibration curve, because they punish wrong probability levels. |
| Business impact of choosing wrong | Premiums built on halved probabilities collect roughly half the needed money, which turns into underwriting losses. |
| Small numeric example | 6 policyholders, claims 1,1,0,1,0,0 (3 claims). Model A probabilities 0.8, 0.7, 0.5, 0.4, 0.3, 0.2 (sum 2.9); Model B = A / 2 (sum 1.45). Both AUC = 8/9 = 0.89. Brier score: A = 0.145, B = 0.253. At ¥500,000 per claim: actual claim cost ¥1.5M; A expects ¥1.45M; B expects ¥0.73M. |

**6. Quick decision rule:** Use ROC-AUC when you need a threshold-free ranking quality number, classes are not extremely rare, and you monitor or compare models over time; avoid it when positives are rare and false alarms are costly, when only the top of the list is used, or when predicted probabilities must be correct.

### Precision-Recall Curve

**1. What it measures (plain English):** The precision-recall (PR) curve plots precision (of the cases flagged, the share that are real) against recall (of all real cases, the share caught) as the cut-off moves from strict to loose. Also called the PR curve. It ignores true negatives completely.

`Precision = TP / (TP + FP)` on the y-axis and `Recall = TP / (TP + FN)` on the x-axis

**2. Intuition:** It is a menu of deals: "catch 40% of the bad cases and be right 95% of the time, or catch 80% and be right only 57% of the time". Operations managers can pick a row by deciding how many wrong alerts they can live with.

**3. Benefits:**

- Honest on imbalanced data, because the false alarm count is compared against the flagged items, not against millions of negatives.
- Reads directly as a business trade-off between coverage and wasted effort.
- Shows "cliffs" where precision collapses, which are natural operating points.
- Comes with a clear baseline: a random model sits at a horizontal line at the prevalence.

**4. Limitations / Potential issues:**

- Not comparable across datasets with different prevalence, because the baseline moves.
- The curve is jagged (precision falls on every false positive and jumps on every true positive); this is normal, not a bug.
- Ignores true negatives, so it is a poor choice when the negative class matters too.
- Linear interpolation between points is wrong; use step-wise summaries such as Average Precision.
- Unstable when there are few positives, and must never be computed on a test set whose negatives were removed.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Opening Only 100 Containers a Day |
| Industry / Domain | Logistics (customs) |
| Business Problem | A Chinese port screens 2,000 import containers a day. About 40 (2%) hold misdeclared goods, but officers can physically open at most 100. The customs chief wants to know how much she catches and how much effort is wasted at that capacity. |
| ML Translation | Target: misdeclared container (1) or compliant (0); imbalanced binary classification (prevalence 0.02); risk score ranking; operating point fixed by officer capacity. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Precision at the capacity line tells her how many of the 100 opened boxes will be worth opening, and recall tells her how many bad boxes she catches. The baseline of 0.02 shows how much better than random the model is. |
| Why other metrics are NOT suitable here | ROC curve: at 100 flagged the FPR is only 0.033, which hides that 64 of 100 opened boxes are clean; accuracy is 98% by flagging nothing; ROC-AUC is a single number with no capacity view. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Misjudging precision means officers open boxes in vain, slowing legitimate trade, while actual smuggling slips through. |
| Small numeric example | 40 bad containers. Flag 50 → 30 bad found: precision 30/50 = 0.60, recall 30/40 = 0.75. Flag 100 → 36 found: precision 0.36, recall 0.90. Flag 200 → 39 found: precision 0.195, recall 0.975. Random baseline 0.02, so at capacity the model is 0.36/0.02 = 18 times better. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Two Thresholds for One Short-Video Feed |
| Industry / Domain | Media (social platform) |
| Business Problem | A Chinese short-video platform must decide two thresholds: one for automatic removal (very high confidence) and a lower one that sends clips to human moderators. About 5% of 10,000 clips in a review window violate policy. |
| ML Translation | Target: policy-violating video (1) or fine (0); imbalanced binary classification; both thresholds are read off the same score. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The PR curve shows exactly how precision (risk of wrongly deleting) and recall (violations left online) trade off, so the team can choose a strict point for deletion and a looser one for review. |
| Why other metrics are NOT suitable here | Accuracy is about 95% by doing nothing; ROC-AUC averages away the two specific operating points; F1 gives only one blended number, but there are two different decisions. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A loose auto-delete threshold removes legitimate creators' videos and triggers appeals; a strict review threshold lets harmful content spread. |
| Small numeric example | 500 violating clips. Auto-remove point: flag 210, TP 200 → precision 200/210 = 0.95, recall 200/500 = 0.40. Review point: flag 700, TP 400 → precision 400/700 = 0.57, recall 0.80. The extra 490 clips reviewed find 200 more violators (marginal precision 200/490 = 0.41). Baseline 0.05. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Which 100 Transformers Get a Visit This Month |
| Industry / Domain | Energy |
| Business Problem | A Singapore power-grid operator has field crews that can inspect 100 of its 5,000 distribution transformers each month. About 50 (1%) fail within a year. It needs to show how much failure risk the crews can address. |
| ML Translation | Target: failure within 12 months (1) or not (0); rare-event binary classification (prevalence 0.01); risk score used to prioritise visits. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The PR curve reads like a work plan: "inspect N units, find this many failures, waste this many visits", all against the 1% random baseline. |
| Why other metrics are NOT suitable here | Accuracy is 99% by flagging nothing; ROC-AUC rewards correctly ignoring 4,950 healthy units; a single precision value at one threshold hides the cost of larger crews. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Crews visit healthy transformers while a failing one causes a neighbourhood outage and a regulatory fine. |
| Small numeric example | 50 failing units. Flag 40 → 25 hits: precision 0.625, recall 0.50. Flag 100 → 40 hits: precision 0.40, recall 0.80 (40 times the 0.01 baseline). Flag 400 → 48 hits: precision 0.12, recall 0.96. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Comparing a Dengue Model Between Java and Papua |
| Industry / Domain | Healthcare (public health) |
| Business Problem | An Indonesian provincial health office wants to know whether its dengue-risk screening model works as well in Java (about 2% of screened people are infected) as in Papua (about 20%), so it compares PR curves from the two regions. |
| ML Translation | Target: infected (1) or not (0); same model on two populations with different prevalence; question is whether discriminative ability differs. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Precision depends on prevalence, so the PR curve shifts between regions even when the model is identical. It would wrongly say the model is much worse in Java. |
| Why other metrics are NOT suitable here | Plain precision and F1 have the same prevalence dependence; accuracy mixes prevalence with skill; PR-AUC would also differ for the same reason. |
| Better alternative (if BAD fit) | ROC curve / ROC-AUC, which is stable across prevalence and shows genuine differences in discrimination. |
| Business impact of choosing wrong | The office could withdraw a perfectly good tool from Java or over-invest in retraining, wasting scarce public-health budget. |
| Small numeric example | Same performance: TPR 0.80, FPR 0.10. Java: 200 infected, 9,800 not → TP 160, FP 980, precision 160/1,140 = 0.14. Papua: 2,000 infected, 8,000 not → TP 1,600, FP 800, precision 1,600/2,400 = 0.67. The ROC point is (0.10, 0.80) in both. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — The Lender Whose Test Set Was "Balanced" |
| Industry / Domain | Banking |
| Business Problem | A Chinese consumer lender trains a default model and, to save compute, throws away most good borrowers from the test file so that it is 50/50. It then reports an impressive PR curve to the credit committee. |
| ML Translation | Target: default (1) or not (0); true prevalence about 1% (100 defaulters among 10,000), but the evaluation set was resampled to 50% prevalence. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Precision uses the number of false positives directly, so deleting negatives from the test set deletes false positives and inflates the whole curve. The curve describes a population that does not exist. |
| Why other metrics are NOT suitable here | Accuracy on the resampled set is equally misleading; F1 inherits the precision inflation; ROC-AUC would survive resampling but would not show the real alert burden. |
| Better alternative (if BAD fit) | Compute the PR curve on a test set with natural prevalence (resampling is acceptable for training only), or re-weight the negatives back to their true share. |
| Business impact of choosing wrong | The committee budgets collections staff for a hit rate that is about seven times too high, so the real campaign disappoints. |
| Small numeric example | Real test file: 100 defaulters, 9,900 good. TPR 0.80, FPR 0.05 → TP 80, FP 0.05 × 9,900 = 495 → precision 80/575 = 0.14. After cutting good borrowers to 100: FP = 0.05 × 100 = 5 → precision 80/85 = 0.94. |

**6. Quick decision rule:** Use the precision-recall curve when positives are rare, you care about wasted work, and you can read the result against the true prevalence baseline; avoid it for comparing across populations with different prevalence, on resampled test sets, or when true negatives matter.

### PR-AUC

**1. What it measures (plain English):** PR-AUC is the area under the precision-recall curve: one number summarising how well a model ranks the rare class while keeping false alarms low. In practice it is computed as Average Precision, not by trapezoids. A random model scores about the prevalence, not 0.5.

`PR-AUC ≈ Σ (Recallₙ − Recallₙ₋₁) × Precisionₙ`

**2. Intuition:** It is a report card for a talent scout. A good scout's early picks are mostly stars, so precision stays high while the list grows. The score is the average hit rate across the list, but the pass mark is the share of stars in the whole pool, not 50%.

**3. Benefits:**

- Honest under imbalance and focused entirely on the positive class.
- Much more sensitive than ROC-AUC to improvements at the top of the ranking, where deployments act.
- Threshold-free, so it fits model selection and automated tuning.
- Has an interpretable baseline (the prevalence), so "PR-AUC 0.30" can be judged properly.

**4. Limitations / Potential issues:**

- The baseline depends on prevalence, so raw values cannot be compared across datasets or periods.
- Ignores true negatives and calibration.
- Higher variance than ROC-AUC, especially with few positives.
- Averages over all recall levels, including ones a regulator or business may never accept.
- Less familiar to managers, so it must be explained with the baseline.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Staged Collisions Hidden Among Honest Claims |
| Industry / Domain | Insurance |
| Business Problem | A Korean motor insurer wants to rank incoming accident claims so investigators see likely staged collisions first. Only about 1.5% of claims are staged, and the team needs one number to compare models. |
| ML Translation | Target: staged claim (1) or genuine (0); rare-event binary classification; the ranked list is worked from the top. The toy list below uses 20 claims with 2 staged for clarity. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | PR-AUC rewards putting staged claims near the top and is read against the tiny baseline, so even a modest-looking score shows real skill. |
| Why other metrics are NOT suitable here | ROC-AUC looks excellent even when half of the top picks are wrong; accuracy is above 98% by approving everything; F1 at one threshold ignores the ordering across the list. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Investigators work through large piles of honest claims, delaying legitimate payouts, while staged-collision rings keep collecting. |
| Small numeric example | 20 claims, 2 staged, at ranks 1 and 4. Precision at those ranks: 1/1 = 1.0 and 2/4 = 0.5. PR-AUC (Average Precision) = (1.0 + 0.5)/2 = 0.75. Baseline = 2/20 = 0.10, so 7.5 times better than random. ROC-AUC = 34/36 = 0.94. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Two Weld-Inspection Models With Almost the Same ROC-AUC |
| Industry / Domain | Manufacturing |
| Business Problem | A Thai auto-parts supplier inspects weld images; about 12% are defective in the test batch and the line can re-check only the top of the list. Two models have close ROC-AUC, and the plant manager asks which to install. |
| ML Translation | Target: defective weld (1) or sound (0); binary classification; 25 test welds, 3 defective; the ranking order of the top few matters. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | PR-AUC separates the two models clearly because it punishes models that bury defects below many sound welds, which ROC-AUC barely notices. |
| Why other metrics are NOT suitable here | ROC-AUC differs by only 0.03 and would suggest a near tie; accuracy needs a threshold; KS shows a single point and hides where defects sit in the ranking. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Installing the weaker model sends defective welds into vehicle assemblies, with recall costs and warranty claims. |
| Small numeric example | Model P puts defects at ranks 1, 2, 13; Model Q at ranks 5, 6, 7 (22 sound welds). ROC-AUC: P = 56/66 = 0.85, Q = 54/66 = 0.82. PR-AUC: P = (1/1 + 2/2 + 3/13)/3 = 0.74; Q = (1/5 + 2/6 + 3/7)/3 = 0.32. Baseline 3/25 = 0.12. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Which Aging Buildings Does the Fire Inspector Visit First |
| Industry / Domain | Real estate (building safety) |
| Business Problem | A Japanese city fire department ranks 40 older apartment buildings by the chance of a serious fire-safety violation so inspectors visit the riskiest first. About 10% have serious violations. |
| ML Translation | Target: serious violation found (1) or not (0); imbalanced binary classification; ranked inspection list; positives are the important class. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The department cares how early the violating buildings appear in the list, and PR-AUC measures exactly this against a clear baseline. |
| Why other metrics are NOT suitable here | Accuracy is 90% for declaring all buildings safe; ROC-AUC credits the many correctly ignored safe buildings; precision at one cut-off does not show how the list improves with more visits. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A badly ranked list sends inspectors to safe buildings while a hazardous one waits, raising the risk of fire casualties. |
| Small numeric example | 40 buildings, 4 violating, at ranks 2, 5, 9, 20. Precisions: 1/2 = 0.50, 2/5 = 0.40, 3/9 = 0.33, 4/20 = 0.20. PR-AUC = (0.50 + 0.40 + 0.33 + 0.20)/4 = 0.36. Baseline 4/40 = 0.10, so about 3.6 times random. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — The Dashboard That Said Quality Fell |
| Industry / Domain | E-commerce |
| Business Problem | A Chinese e-commerce platform's fake-review model scored PR-AUC 0.60 last quarter and 0.35 this quarter. Leadership concludes the model has degraded, but the share of fake reviews also fell from 10% to 3% after a policy change. |
| ML Translation | Target: fake review (1) or genuine (0); binary classification; two quarters with different prevalence; question is whether ranking skill changed. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Raw PR-AUC moves with prevalence, so the lower number is partly just fewer fakes to find. The raw values are not comparable. |
| Why other metrics are NOT suitable here | Accuracy and F1 also move with prevalence; precision at a fixed threshold has the same problem; log loss mixes calibration shifts with ranking skill. |
| Better alternative (if BAD fit) | PR-AUC lift (PR-AUC divided by prevalence), or ROC-AUC, which is stable across prevalence. |
| Business impact of choosing wrong | The team would spend a quarter retraining a model that actually improved, delaying other trust-and-safety work. |
| Small numeric example | Last quarter 0.60 / 0.10 = 6.0 times random. This quarter 0.35 / 0.03 = 11.7 times random. Relative to chance the model nearly doubled its skill, even though the raw number fell. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Wafer Lots That Must Be Cleared of Every Defect |
| Industry / Domain | Manufacturing (semiconductors) |
| Business Problem | A South Korean chip fab ships wafer lots to an automotive customer whose contract says at least 95% of defective wafers must be pulled before shipping. Engineers re-inspect wafers in score order. With only 4 truly defective wafers among 20 flagged, meeting the contract means catching all 4. Two models are compared with PR-AUC. |
| ML Translation | Target: wafer is defective (1) or good (0); binary classification; business requirement is a fixed recall of at least 95%, with cost measured in wafers re-inspected. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | PR-AUC averages over all recall levels, including low recall that the customer will never accept. It prefers Model A, which finds three defective wafers instantly but buries the fourth. |
| Why other metrics are NOT suitable here | ROC-AUC ignores the re-inspection workload; F1 at one cut-off may not reach the recall requirement; accuracy is dominated by the many good wafers. |
| Better alternative (if BAD fit) | Precision (or number of wafers re-inspected) at the required recall of 95% or higher. |
| Business impact of choosing wrong | Engineers re-inspect twice as many wafers as necessary, which slows the line, or a defective wafer ships and the fab faces a recall claim. |
| Small numeric example | Defective wafers at ranks: A = 1, 2, 3, 16; B = 2, 4, 6, 8. PR-AUC: A = (1 + 1 + 1 + 4/16)/4 = 0.81; B = (1/2 + 2/4 + 3/6 + 4/8)/4 = 0.50. To reach 100% recall: A needs 16 wafers re-inspected (precision 0.25); B needs 8 (precision 0.50). B is better for the actual rule. |

**6. Quick decision rule:** Use PR-AUC when positives are rare, you act on the top of the ranking, and you can state the prevalence baseline beside the number; avoid it for comparing across periods or populations with different prevalence, or when the business demands a fixed recall level.

### Average Precision (AP)

**1. What it measures (plain English):** Average Precision (AP) walks down the ranked list, records the precision each time it meets a real positive, and averages those values. It is the standard, unbiased way of computing PR-AUC. The mean of AP over many classes or queries is called mAP (mean Average Precision).

`AP = (1 / number of positives) × Σ precision at the rank of each positive`

**2. Intuition:** It is like grading a search engine's result page. Each time a useful result appears, you note what fraction of the results so far were useful, then average over all useful results. A page that puts useful results first scores higher than one that buries them.

**3. Benefits:**

- Rewards finding positives early, which matches how ranked lists are consumed.
- Avoids the optimistic bias of trapezoid-based areas on the PR curve.
- Extends naturally to many queries or classes through mAP.
- A single, threshold-free number that can be used to tune models.

**4. Limitations / Potential issues:**

- The baseline equals prevalence, so values are not comparable across datasets.
- Many tied scores (common with shallow trees) make AP unstable and implementation dependent.
- Treats relevance as yes or no; it cannot reward a more relevant result above a slightly relevant one.
- Ignores true negatives and calibration, and has high variance with few positives.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Judging a Marketplace Search Box Across Queries |
| Industry / Domain | E-commerce |
| Business Problem | A Japanese online marketplace wants one quality number for its search ranking across many queries, because shoppers rarely look past the first few results. |
| ML Translation | For each query: relevant listing (1) or not (0), ranked by a relevance score; metric computed per query and averaged (mAP). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | AP gives credit for placing relevant listings early, and averaging it across queries (mAP) gives the standard search-quality number. |
| Why other metrics are NOT suitable here | Precision at 10 ignores the order within the top 10; ROC-AUC is swamped by the huge number of irrelevant listings; accuracy is meaningless with a handful of relevant results. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A poorly ranked search sends shoppers to irrelevant listings, lowering conversions and seller satisfaction. |
| Small numeric example | Query "rice cooker": relevant at ranks 1 and 3 → AP = (1/1 + 2/3)/2 = 0.83. Query "school bag": relevant at ranks 2, 4, 6 → AP = (1/2 + 2/4 + 3/6)/3 = 0.50. mAP = (0.83 + 0.50)/2 = 0.67. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — The Radiologist Who Reads From the Top of the Worklist |
| Industry / Domain | Healthcare |
| Business Problem | A Chinese hospital group ranks the morning's chest X-rays so that the radiologist reads suspected urgent findings first (for example a collapsed lung). Two prioritisation models are compared. |
| ML Translation | Target: urgent finding (1) or routine (0); ranked worklist; 10 scans with 3 urgent; what matters is how early urgent scans appear. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The radiologist works down the list, so delay for each urgent scan depends on its position. AP rewards early positions directly. |
| Why other metrics are NOT suitable here | ROC-AUC treats a position-4 and a position-10 error almost alike; accuracy needs a cut-off the radiologist does not use; recall alone ignores ordering. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | An urgent scan read late delays treatment and may cause a preventable emergency. |
| Small numeric example | Model A: urgent scans at ranks 1, 2, 4 → AP = (1 + 1 + 3/4)/3 = 0.92. Model B: urgent at ranks 3, 5, 6 → AP = (1/3 + 2/5 + 3/6)/3 = 0.41. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Ranking Applicants Who Will Survive Probation |
| Industry / Domain | HR |
| Business Problem | A Singapore recruiter shortlists applicants for a sales role and wants candidates who will pass the 6-month probation to appear near the top of the shortlist. About 3 of every 10 applicants pass. |
| ML Translation | Target: passes probation (1) or not (0); ranked list of 10 candidates with 3 positives; the hiring manager reads from the top. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | AP measures how early the likely successes appear in the shortlist, which is what the hiring manager experiences. |
| Why other metrics are NOT suitable here | Accuracy needs a cut-off the manager does not apply; the ROC curve shows overall separation but not early placement; precision at one fixed size misses the order within it. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Interview time goes to weak candidates, roles stay open longer, and strong candidates accept other offers. |
| Small numeric example | Model P: positives at ranks 1, 2, 5 → AP = (1 + 1 + 3/5)/3 = 0.87. Model Q: ranks 3, 4, 5 → AP = (1/3 + 2/4 + 3/5)/3 = 0.48. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — The Shallow Tree That Gives Only Three Scores |
| Industry / Domain | Manufacturing |
| Business Problem | A Vietnamese electronics assembly plant tests circuit boards with a very simple decision tree that outputs just three score levels (high, medium, low). Management wants one AP number to compare it with the current system. |
| ML Translation | Target: defective board (1) or good (0); 12 boards, 3 defective; scores have many ties (groups of boards with identical scores). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | When scores are tied, the order inside each tied group is arbitrary, so AP depends on how the software breaks ties and can vary a lot. |
| Why other metrics are NOT suitable here | Plain accuracy needs a cut-off; AP implementations differ in handling ties; threshold-free numbers are fragile when only three thresholds exist. |
| Better alternative (if BAD fit) | Report precision and recall at each of the three real score levels (or use a model with continuous scores); ROC-AUC with its half-credit for ties is steadier. |
| Business impact of choosing wrong | A lucky tie order could make an inferior model look best and get installed, increasing defective boards shipped. |
| Small numeric example | High group (4 boards, 2 defective), medium group (4 boards, 1 defective), low group (4 boards, 0). Best tie order: defects first → AP = (1 + 1 + 3/5)/3 = 0.87. Worst tie order: defects last → AP = (1/3 + 2/4 + 3/8)/3 = 0.40. A tie-grouping tool reports 0.46. The same model scores 0.40 to 0.87. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — The Top Slot Went to a Weakly Relevant Show |
| Industry / Domain | Media (video streaming) |
| Business Problem | A Korean streaming service ranks shows on the home screen. Editors grade each show for a viewer as 0 (irrelevant), 1 (somewhat relevant) or 3 (highly relevant). They need a metric that knows the difference. |
| ML Translation | Graded relevance (0, 1, 3) on a ranked list of 4 shows; the goal is to put the best show first. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | AP only sees relevant versus not relevant. It cannot tell that a highly relevant show deserves a higher position than a somewhat relevant one. |
| Why other metrics are NOT suitable here | Precision at k treats all relevant items equally; ROC-AUC ignores positions and grades; accuracy cannot rank. |
| Better alternative (if BAD fit) | NDCG (normalised discounted cumulative gain), which rewards putting the highest grades first. |
| Business impact of choosing wrong | The home screen leads with a mediocre show, lowering watch time and subscriber satisfaction. |
| Small numeric example | List X has grades 1, 3, 0, 0; List Y has 3, 1, 0, 0. Both have relevant items at ranks 1 and 2, so AP = 1.00 for both. NDCG@4 (gain 2^grade − 1, discount log2(rank + 1)): X = 5.42/7.63 = 0.71; Y = 7.63/7.63 = 1.00. |

**6. Quick decision rule:** Use Average Precision when the ranked list is read from the top and relevance is yes or no, and when scores are mostly distinct; avoid it when scores have many ties or when relevance has grades (use NDCG).

## Targeting and Capacity Metrics

### Lift (Lift Curve and Lift at Decile)

**1. What it measures (plain English):** Lift says how many times better the model is than random selection at a given depth of the ranked list; "at decile 1" means the top 10%. It is the hit rate in the selected top slice divided by the overall hit rate. The lift curve plots this for every depth and always ends at 1.0 at 100%.

`Lift at top k% = (positives in top k% / customers in top k%) / (total positives / total customers)`

**2. Intuition:** Fishing with a fish finder: in a random spot one cast in twenty gets a bite, but at the spots the finder points to, one in five does. The finder gives a lift of 4 because those spots are four times better than random.

**3. Benefits:**

- Speaks the language of budget: "if we can only contact 10%, how much better than random are we?"
- Converts directly to money: responders captured × value − contacts × cost.
- Easy for marketing and collections managers to understand.
- Needs no cut-off, only a capacity.

**4. Limitations / Potential issues:**

- Depends on prevalence (the maximum lift is 1 divided by prevalence), so lifts are not comparable across campaigns without normalising.
- Depends on how many bins are used (deciles versus percentiles).
- Meaningful only when you pick a top slice; useless when every case must be decided.
- Says nothing about cause and effect: it finds people likely to respond, not people changed by the contact.
- Not in common libraries, so definitions vary between teams.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Sending Coupons to the Best 10% of a Super-App's Users |
| Industry / Domain | Marketing |
| Business Problem | A Chinese super-app has a coupon budget for 1,000 of its 10,000 users. About 5% would buy anyway in the campaign window, and the marketer wants to know how much the model helps in the top 10%. |
| ML Translation | Target: purchase after the message (1) or not (0); ranked list by propensity; capacity fixed at the top decile. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The campaign is a fixed-capacity selection, so lift at decile 1 is the exact answer to the marketer's question, and it converts straight into profit. |
| Why other metrics are NOT suitable here | Accuracy is meaningless for a ranking task; ROC-AUC does not say what happens in the top 10%; precision alone has no baseline for comparison. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A random selection earns nothing after message costs, while a model-led selection earns a clear profit. |
| Small numeric example | Overall rate 5%. Top decile: 1,000 users, 200 buy → 20% → lift = 0.20 / 0.05 = 4.0. Random decile: 50 buyers. Profit at ¥40 margin per purchase and ¥2 per message: random = 50 × 40 − 1,000 × 2 = ¥0; model = 200 × 40 − 1,000 × 2 = ¥6,000. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Which Overdue Motorbike Loans Get a Collector's Visit |
| Industry / Domain | Banking (consumer finance) |
| Business Problem | An Indonesian motorbike-finance company has 5,000 overdue accounts. About 1,000 would slide into default without intervention. Collectors can visit 1,000 accounts a week at IDR 80,000 per visit, and a rescued account is worth IDR 1,000,000. |
| ML Translation | Target: account would roll into default (1) or not (0); ranked list; capacity 20% of the list; positives are 20% of accounts. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Lift ties the ranking directly to visiting capacity, and the marginal response rate of the next slice decides whether to add more collectors. |
| Why other metrics are NOT suitable here | Accuracy depends on a cut-off nobody applies; ROC-AUC averages over depths the team cannot afford; F1 at one cut-off ignores the capacity plan. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Collectors visit accounts that would have paid anyway, while the truly risky ones roll into default and become write-offs. |
| Small numeric example | Top 20% (1,000 accounts): 500 at-risk → rate 0.50, lift = 0.50 / 0.20 = 2.5 (random would find 200). Break-even marginal rate = 80,000 / 1,000,000 = 0.08. Next 1,000 accounts: 250 at-risk → 0.25 (above 0.08, worth it); the following 1,000: 150 → 0.15 (still above 0.08). |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — A Loyalty SMS for a Vietnamese Supermarket Chain's Best Prospects |
| Industry / Domain | Retail |
| Business Problem | A Vietnamese supermarket chain has 8,000 loyalty members and can afford an SMS offer for the best 10% (800) of them. About 4% of members normally buy the featured product line. |
| ML Translation | Target: buys the product line within 2 weeks (1) or not (0); ranked members; the cumulative lift at deciles guides how far to extend the SMS list. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Lift at 10%, 20% and 30% shows how quickly the benefit decays as the list grows, so the marketing team can decide the right size of the offer. |
| Why other metrics are NOT suitable here | Accuracy is 96% by predicting nobody buys; ROC-AUC says nothing about the top 10%; log loss measures probability quality, not the benefit of a slice. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Messaging all members wastes SMS spend and trains customers to ignore offers. |
| Small numeric example | Base rate 320 / 8,000 = 4%. Top 10% (800): 96 buyers → 12% → lift 3.0. Top 20% (1,600): 150 buyers → 9.4% → lift 2.3. Top 30% (2,400): 190 buyers → 7.9% → lift 2.0. Extra response from the second slice: 54 / 800 = 6.8%. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Comparing Two Telecom Campaigns by Their Lift |
| Industry / Domain | Telecom |
| Business Problem | A Thai telecom company ran two campaigns: Campaign A (a rare add-on, 2% take-up) with top-decile lift 6.0, and Campaign B (a popular data pack, 30% take-up) with top-decile lift 2.5. The VP says model A is better because 6 beats 2.5. |
| ML Translation | Two ranking models on different prevalence; the question is which model separates its audience better. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Maximum possible lift is 1 divided by prevalence, so a lift of 6 against a ceiling of 50 is weak, while 2.5 against a ceiling of 3.33 is nearly perfect. Raw lift hides the ceiling. |
| Why other metrics are NOT suitable here | Raw response rate is also prevalence dependent; accuracy depends on a cut-off; ROC-AUC would be comparable but does not speak in campaign terms. |
| Better alternative (if BAD fit) | Lift as a share of its ceiling (or the gains chart against the perfect curve), or ROC-AUC. |
| Business impact of choosing wrong | The company would copy a mediocre modelling approach for all campaigns and underfund the model that is nearly perfect. |
| Small numeric example | Campaign A: ceiling = 1 / 0.02 = 50; 6.0 / 50 = 12% of the maximum. Campaign B: ceiling = 1 / 0.30 = 3.33; 2.5 / 3.33 = 75% of the maximum. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — The Voucher That Went to Customers Who Would Have Bought Anyway |
| Industry / Domain | E-commerce (cosmetics) |
| Business Problem | A Korean cosmetics retailer targets the top decile (1,000 customers) by purchase propensity with a ₩5,000 voucher per buyer. The model shows a lift of 4.0, but management suspects these loyal customers would have bought anyway. |
| ML Translation | Target is purchase probability, but the business needs the incremental effect of the voucher (treated versus untreated). Overall purchase rate 6%; a holdout of untouched top-decile customers exists. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Lift measures who is likely to buy, not whom the voucher changes. The top decile is full of "sure things". |
| Why other metrics are NOT suitable here | ROC-AUC and PR-AUC also measure propensity, not cause and effect; accuracy ignores treatment; gains charts also reward finding likely buyers. |
| Better alternative (if BAD fit) | Uplift modelling with a Qini curve, which ranks customers by the expected extra purchases caused by the voucher. |
| Business impact of choosing wrong | The retailer gives away discounts to customers who would have paid full price, turning a campaign with high apparent lift into a loss. |
| Small numeric example | Top decile: 24% buy when contacted, 21% buy when left alone → 3 extra points = 30 incremental buyers × ₩12,000 margin = ₩360,000; voucher cost 240 × ₩5,000 = ₩1,200,000 → net −₩840,000. A "persuadable" group of 1,000 (12% treated versus 4% control, lift only 12% / 6% = 2.0): 80 incremental × ₩12,000 = ₩960,000 − 120 × ₩5,000 = ₩600,000 → net +₩360,000. |

**6. Quick decision rule:** Use lift when you can act on a fixed top slice of a ranked list and the question is "how much better than random?"; avoid it for cross-campaign comparison without the ceiling (1 divided by prevalence), when every case must be classified, or when you need causal impact (use uplift).

### Cumulative Gain (Gains Chart)

**1. What it measures (plain English):** The cumulative gain chart (gains chart) plots the share of all positives captured (y-axis) against the share of the population contacted or inspected (x-axis) when working down the ranked list. It is recall measured against depth, with a random diagonal and a perfect curve for reference.

`Cumulative Gain at k% = positives in top k% / total positives`

**2. Intuition:** It is a tax-collector's route map: "if I visit the first 20% of houses on my ranked list, what fraction of all the overdue bills will I collect?" The straighter the line, the more the list is no better than a random walk through town.

**3. Benefits:**

- Answers capacity questions at a glance: "how much of the population must we process to reach 80% of the positives?"
- The three-curve format (random, model, perfect) shows how much room is left.
- Links to the Gini coefficient and hence to ROC-AUC.
- Executives understand it without training.

**4. Limitations / Potential issues:**

- The shape depends on prevalence, so charts from different datasets are not directly comparable.
- Ignores the cost of false positives; money must be added via a profit calculation.
- Coarse bins (deciles) can hide what happens in a very small top slice.
- Only for ranked-selection problems; and a chart computed on training data is over-optimistic.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Phone Calls to Patients Before They Bounce Back |
| Industry / Domain | Healthcare |
| Business Problem | A Singapore hospital discharges 200 patients a week; about 40 (20%) are readmitted within 30 days. Nurses can phone 60 patients (30%) a week for a follow-up call, and the head of nursing asks how many future readmissions the model lets them reach. |
| ML Translation | Target: readmitted within 30 days (1) or not (0); ranked list; capacity fixed at 30% of discharges. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The x-axis is the nurses' capacity and the y-axis is the share of the readmissions reached, so the answer is read straight from the chart. |
| Why other metrics are NOT suitable here | Accuracy needs a cut-off the nurses do not use; the PR curve has recall on the x-axis, not the number of calls; ROC-AUC does not give the answer for a 30% capacity. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Weak coverage means preventable readmissions occur (bed costs and penalties), while strong coverage justifies funding more nurse time. |
| Small numeric example | Top 30% (60 patients) contains 28 of the 40 readmissions → gain 28 / 40 = 0.70. Random calling reaches 0.30 × 40 = 12. A perfect model would reach all 40 (the 60 calls exceed 40). |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Auditing Returns That Under-Report Income |
| Industry / Domain | Government (tax administration) |
| Business Problem | A Japanese tax office has 10,000 small-business returns, of which about 500 under-report income. Auditors can handle 2,000 audits this year and the director wants to know how coverage grows with more audits. |
| ML Translation | Target: under-reported return (1) or compliant (0); ranked list of returns; positives are 5% of the population; capacity defined by audit count. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The audit plan is a population-depth decision, and the gains chart shows what share of non-compliance is covered at each depth. |
| Why other metrics are NOT suitable here | ROC-AUC does not say how many audits are needed; accuracy is 95% by auditing nobody; precision at one cut-off does not show how coverage scales with audits. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Underestimating coverage wastes audit hours on compliant firms; overestimating it leaves hidden tax gaps uncollected. |
| Small numeric example | Top 20% (2,000 returns) contains 300 of the 500 → gain 0.60 (random: 100 cases). At 40% depth (4,000 audits) gain is 0.80 (400 cases); random would need 8,000 audits to reach the same 80%. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Setting the Underwriting Referral Cut-off |
| Industry / Domain | Insurance |
| Business Problem | A Korean life insurer lets a risk model score 10,000 applications and refers the riskiest to human underwriters. Management wants referral to capture at least 80% of high-risk applications while keeping underwriter workload as low as possible. |
| ML Translation | Target: high-risk application (1) or standard (0); ranked list; objective expressed as a coverage target (80% of positives). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The business gave a coverage target, and the gains chart converts that directly into a referral volume. |
| Why other metrics are NOT suitable here | PR curve axes do not show how many applications to refer; ROC curve shows rates but not volume; accuracy is not tied to the coverage target. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Referring too few lets high-risk policies through underpriced; referring too many slows approvals and loses customers to faster competitors. |
| Small numeric example | Gain at depth 10%, 20%, 30%, 40%, 50%: 0.35, 0.55, 0.70, 0.80, 0.87. Gain 0.80 is reached at 40% depth, so refer 4,000 of 10,000 applications. Random referral would need 8,000. Saving = 4,000 reviews. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Rejecting the Worst 40% Because It Catches 80% of Defaults |
| Industry / Domain | Banking |
| Business Problem | A Vietnamese bank examines 1,000 loan applicants, of whom 100 would default. The credit head wants to reject the riskiest 40% because the gains chart shows that this catches 80% of defaulters. A default loses VND 40 million, while a good loan earns VND 6 million. |
| ML Translation | Target: default (1) or repay (0); ranked list; the decision has asymmetric money outcomes for both errors. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The gains chart shows only the positives captured and ignores the good customers lost along the way. Maximising coverage is not the same as maximising profit. |
| Why other metrics are NOT suitable here | Lift also ignores the cost of lost customers; ROC-AUC has no cost information; accuracy treats both errors equally. |
| Better alternative (if BAD fit) | A profit (expected-value) curve: savings from avoided defaults minus income lost from rejected good customers at each depth. |
| Business impact of choosing wrong | The bank rejects far too many creditworthy applicants, giving up millions in interest income for a coverage number. |
| Small numeric example | Reject worst 40% (400 applicants): 80 defaulters avoided = 80 × 40 = VND 3,200 million saved; 320 good borrowers lost = 320 × 6 = VND 1,920 million; net +1,280 million. Reject worst 20% (200): 60 defaulters avoided = 2,400 million; 140 good lost = 840 million; net +1,560 million, which is better. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Ten Meter Thieves in Ten Thousand Households |
| Industry / Domain | Energy |
| Business Problem | A Thai electricity utility believes about 10 of its 10,000 monitored meters are tampered with. Field teams can inspect only 20 meters a week. The analyst presents a gains chart that shows 90% of thieves caught in the top 10%. |
| ML Translation | Target: tampered meter (1) or normal (0); extremely rare (prevalence 0.001); the real capacity is 0.2% of the population, far finer than a decile. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Deciles are too coarse: the 90% figure is for 1,000 meters, far more than the teams can visit. The chart hides what happens in the top 20. |
| Why other metrics are NOT suitable here | A decile-based lift also hides it; ROC-AUC rewards ignoring the normal meters; accuracy is 99.9% by inspecting none. |
| Better alternative (if BAD fit) | Precision at k with k = 20 (or lift at a very fine depth such as the top 0.2%). |
| Business impact of choosing wrong | Management expects 9 of 10 thieves caught but crews find only a few per week, leaving revenue losses largely untouched. |
| Small numeric example | Top 10% (1,000 meters): 9 thieves → gain 0.90. Top 20 meters: 4 thieves → gain 4 / 10 = 0.40 and precision 4 / 20 = 0.20. Random picking would find 20 × 0.001 = 0.02 thieves, so lift at 20 = 0.20 / 0.001 = 200. |

**6. Quick decision rule:** Use the cumulative gain chart when the target is a coverage level or capacity expressed as a share of the population; avoid it when money per error matters (use a profit curve), when the capacity is a tiny fraction of the population (use precision at k), or when comparing across prevalences.

## Scorecard and Separation Metrics

### KS Statistic

**1. What it measures (plain English):** The Kolmogorov-Smirnov (KS) statistic is the largest vertical gap between the cumulative score distributions of positives and negatives. It equals the maximum of TPR minus FPR, also known as the best Youden's J. It reports both how well the classes are separated and the cut-off where they separate most.

`KS = max over cut-offs of (TPR − FPR)`

**2. Intuition:** Picture two queues of people walking up a staircase of scores, one queue of defaulters and one of good borrowers. KS is the biggest distance between the two queues at any single step. The step where they are furthest apart is the natural place to draw a line.

**3. Benefits:**

- Gives a single number and a suggested cut-off at once.
- Widely expected in banking and credit-model documentation.
- Simple geometric meaning and a formal statistical test.
- Insensitive to order-preserving changes of the score.

**4. Limitations / Potential issues:**

- Looks at one point only; two models with the same KS can differ everywhere else.
- Assumes false positives and false negatives cost the same.
- Uses FPR, so it shares ROC's imbalance blind spot: high KS with poor precision on rare events.
- The KS cut-off may flag far more cases than the team can handle.
- Unstable on small samples, and inflated on development data.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — The SME Scorecard Package for the Central Bank |
| Industry / Domain | Banking |
| Business Problem | A Vietnamese bank builds a scorecard for small-business loans. Its validation pack must report a separation statistic and a proposed cut-off in the standard form the regulator expects. |
| ML Translation | Target: default (1) or repay (0); higher score means higher risk; binary classification on an out-of-time validation sample (toy: 6 defaulters and 8 non-defaulters). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | KS is the convention in credit scorecard documentation and delivers a number and a starting cut-off in one step. |
| Why other metrics are NOT suitable here | ROC-AUC summarises but gives no cut-off; accuracy depends on an arbitrary cut-off and on the default rate; log loss measures probability quality, not separation. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A pack without the expected statistic delays model approval, and a poor cut-off causes either too many rejections or too many bad loans. |
| Small numeric example | Defaulter scores 0.9, 0.8, 0.75, 0.6, 0.5, 0.3; non-defaulters 0.7, 0.55, 0.4, 0.35, 0.25, 0.2, 0.15, 0.1. Cut-off 0.5: TP = 5, FP = 2 → TPR = 5/6 = 0.83, FPR = 2/8 = 0.25 → gap 0.58. No other cut-off beats this → KS = 0.58 (58 on the 0 to 100 scale). |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Approving Buy-Now-Pay-Later Orders With Similar Costs for Each Mistake |
| Industry / Domain | Banking (fintech) |
| Business Problem | A Singapore buy-now-pay-later app needs an approval cut-off. Declining a good customer loses about S$30 of margin; approving a defaulter loses about S$35. The two errors are roughly equally costly. |
| ML Translation | Target: default on the instalment plan (1) or pays (0); binary classification score; 100 defaulters and 900 good customers in the test set; costs of errors about equal. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | KS maximises TPR minus FPR, which is the right objective when both errors cost about the same, and it returns the cut-off directly. |
| Why other metrics are NOT suitable here | Accuracy is dominated by the 90% good customers; precision alone ignores missed defaulters; ROC-AUC does not name a cut-off. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A poorly placed cut-off turns away good customers or lets defaulters through, each costing about S$30 to S$35 per case. |
| Small numeric example | Three cut-offs, (TPR, FPR): (0.50, 0.10) → gap 0.40; (0.70, 0.20) → gap 0.50; (0.85, 0.40) → gap 0.45. KS = 0.50 at the second cut-off, which approves with 70% of defaulters caught and 20% of good customers declined. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Fake Rental Listings in a Haystack |
| Industry / Domain | Real estate |
| Business Problem | A Chinese rental platform wants to flag fake listings (bait-and-switch prices). About 0.5% of 10,000 new listings are fake, and a three-person team reviews flagged listings by hand. The data team reports KS 0.70 and proposes flagging at the KS cut-off. |
| ML Translation | Target: fake listing (1) or genuine (0); rare-event binary classification (50 positives, 9,950 negatives); human review capacity is small. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | KS uses FPR, which divides by the large genuine class. A KS of 0.70 can come with a flagged list in which almost all listings are genuine. |
| Why other metrics are NOT suitable here | Accuracy is 99.5% by flagging nothing; ROC-AUC has the same denominator problem; the ROC curve hides precision for the same reason. |
| Better alternative (if BAD fit) | Precision-recall curve (or PR-AUC) with precision at the reviewers' daily capacity. |
| Business impact of choosing wrong | The review team is flooded with genuine listings, real fakes remain online, and tenants lose deposits to scams. |
| Small numeric example | KS cut-off: TPR 0.90, FPR 0.20 → KS = 0.70. TP = 0.90 × 50 = 45; FP = 0.20 × 9,950 = 1,990; flagged = 2,035. Precision = 45 / 2,035 = 0.022 (baseline 0.005). |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — The Battery Cell That Must Never Slip Through |
| Industry / Domain | Manufacturing |
| Business Problem | A Korean battery plant tests 10,000 cells; about 100 have an internal fault that can cause fires. A missed faulty cell costs about ₩50 million (recall, fire risk); rejecting a good cell costs about ₩20,000. Engineers want to use the KS cut-off. |
| ML Translation | Target: faulty cell (1) or good (0); binary classification; very unequal error costs (a miss is about 2,500 times a false rejection). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | KS weights a miss and a false rejection equally, so it picks a cut-off that is statistically neat but ignores that misses are astronomically more expensive. |
| Why other metrics are NOT suitable here | Accuracy is 99% for passing everything; ROC-AUC gives no cut-off; F1 treats errors symmetrically. |
| Better alternative (if BAD fit) | Expected-cost analysis, picking the cut-off that minimises misses × ₩50 million + false rejections × ₩20,000. |
| Business impact of choosing wrong | A handful of missed faulty cells can cost hundreds of millions in recalls and safety incidents, more than the savings from rejecting fewer good cells. |
| Small numeric example | KS cut-off: TPR 0.85, FPR 0.10 → gap 0.75. Misses = 15, false rejections = 0.10 × 9,900 = 990. Cost = 15 × 50 million + 990 × 0.02 million = ₩769.8 million. Lower cut-off: TPR 0.98, FPR 0.25 → gap 0.73. Misses = 2, false rejections = 2,475. Cost = 100 + 49.5 = ₩149.5 million. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Burnout Model Tested on a Pilot of Twelve Employees |
| Industry / Domain | HR |
| Business Problem | A Singapore firm pilots a model for staff who will resign within six months, using 12 employees of whom 3 left. The pilot reports a KS value and the leadership wants to decide on rollout based on it. |
| ML Translation | Target: resigned (1) or stayed (0); binary classification with 3 positives and 9 negatives; the statistic is a single maximum and therefore sensitive to individual cases. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | KS is one maximum over the data, so a change in one person's score can move it a lot. With 3 leavers it is not stable enough to base a decision on. |
| Why other metrics are NOT suitable here | Accuracy is equally volatile and depends on a cut-off; ROC-AUC also moves but averages across all pairs; precision at a cut-off shifts by whole people. |
| Better alternative (if BAD fit) | Report the metric with a bootstrap confidence interval, and gather more leavers before deciding; AUC with its interval gives a steadier picture. |
| Business impact of choosing wrong | The firm may roll out a model on the basis of a lucky number, then harass the wrong staff with retention talks, or drop a model that is actually fine. |
| Small numeric example | Leaver scores 0.9, 0.7, 0.4; stayer scores 0.8, 0.6, 0.5, 0.35, 0.3, 0.2, 0.15, 0.1, 0.05 → KS = 0.67. If one leaver's score were 0.85 instead of 0.4 → KS = 0.89. If it were 0.12 → KS = 0.56. One employee swings KS by 0.22 to 0.11. |

**6. Quick decision rule:** Use KS when you need a separation number and a cut-off in one step, the two error costs are similar, and the sample is large (typical in credit scorecards); avoid it when positives are rare and false alarms matter, when error costs are very unequal, or when data is small.

### Gini Coefficient [Added – not in source file]

**1. What it measures (plain English):** The Gini coefficient (also called the accuracy ratio or Somers' D in credit risk) rescales ROC-AUC so that a random model scores 0 and a perfect model scores 1. It is the credit-scoring and insurance favourite, and it is also the area between the model's gains curve and the diagonal divided by the same area for the perfect curve.

`Gini = 2 × AUC − 1`

**2. Intuition:** It is like measuring how far a runner is ahead of the pack. AUC measures from the floor (0.5 for a random runner); Gini measures from the starting line, so "no advantage" is 0 and "wins every race" is 1.

**3. Benefits:**

- Zero means no skill, which is more intuitive than 0.5.
- Standard in banking and insurance, so teams, validators and regulators speak the same language.
- Inherits AUC's stability and independence from thresholds and prevalence.
- Easy to track over time and to set monitoring rules, for example "investigate if Gini falls by more than 0.08".

**4. Limitations / Potential issues:**

- Contains exactly the same information as AUC, so it is not extra evidence.
- Has the same blind spot on rare events: a high Gini can sit beside very poor precision.
- Blind to calibration: it cannot tell whether predicted probabilities are correct.
- Name confusion: "Gini" also means the income-inequality index and the decision-tree impurity measure; always say "model Gini" or "accuracy ratio".
- Not well defined for more than two classes without a convention.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Validating a New Retail Scorecard Against the Old One |
| Industry / Domain | Banking |
| Business Problem | A Japanese regional bank's model-validation team must show senior risk managers whether a new retail-loan scorecard separates good and bad borrowers better than the existing one. The bank's policy documents are all written in Gini. |
| ML Translation | Target: default (1) or repay (0); binary classification score; a toy test of 4 defaulters and 5 good borrowers (20 pairs). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Gini is the bank's house language and rescales AUC so that "no skill" is zero, which makes improvements easy to compare. |
| Why other metrics are NOT suitable here | Accuracy depends on a cut-off and the default rate; KS reports a single point; log loss measures probability quality rather than separation. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Approving a scorecard that is not truly better, or rejecting one that is, changes loss rates across the whole loan book. |
| Small numeric example | New scorecard: 17 of 20 pairs correctly ordered → AUC = 17/20 = 0.85 → Gini = 2 × 0.85 − 1 = 0.70. Old scorecard: 15 of 20 → AUC = 0.75 → Gini = 0.50. Improvement = 0.20. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Two Motor-Rating Models Competing for Next Year's Tariff |
| Industry / Domain | Insurance |
| Business Problem | A Korean auto insurer has two candidate rating models that rank policyholders by claim risk. The pricing committee wants a single comparison number used throughout the industry. |
| ML Translation | Target: at least one claim (1) or none (0); ranking score; toy test with 5 claimants and 6 non-claimants (30 pairs); ties count as half a win. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Gini is the insurance standard for how well a rating model separates high-risk from low-risk customers, and handles ties by half credit. |
| Why other metrics are NOT suitable here | Accuracy depends on a cut-off nobody uses in pricing; KS reports only a single point; the PR curve moves with the claim frequency. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A tariff built on the weaker ranking underprices risky drivers and overprices safe ones, who then leave for competitors. |
| Small numeric example | Model X: 24 wins, 2 ties, 4 losses out of 30 pairs → AUC = (24 + 1)/30 = 0.83 → Gini = 0.67. Model Y: 21 wins, 3 ties, 6 losses → AUC = (21 + 1.5)/30 = 0.75 → Gini = 0.50. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Monthly Gini Watch on a Device-Instalment Scorecard |
| Industry / Domain | Telecom |
| Business Problem | A Vietnamese mobile operator sells phones on instalment plans using a scorecard. The risk team tracks a monthly number and has a rule that a drop of more than 0.08 from the baseline triggers a model review. |
| ML Translation | Target: missed two or more instalments (1) or not (0); same model scored on each month's new customers; need a stable monitoring statistic. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Gini is stable against changes in the default rate, so a fall indicates the scorecard is losing ranking power rather than reacting to the economy. |
| Why other metrics are NOT suitable here | Accuracy and precision move with the default rate; KS is noisier because it uses one point; log loss blends calibration drift with ranking drift. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Missing the decay lets handsets go to customers who never pay, which is a direct hardware loss. |
| Small numeric example | Baseline Gini 0.62 (AUC 0.81). March 0.58 (AUC 0.79): drop 0.04, no action. May 0.49 (AUC 0.745): drop 0.13 > 0.08 → model review is triggered. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — The Newborn Screening Test With a Gini of 0.96 |
| Industry / Domain | Healthcare |
| Business Problem | A Chinese hospital group tests newborns for a rare metabolic disorder (about 50 in 100,000). The vendor proudly reports a Gini of 0.96 and the hospital plans to treat every positive test as nearly certain. |
| ML Translation | Target: affected (1) or healthy (0); extremely rare (prevalence 0.05%); the value that matters to families and doctors is the chance that a positive test is real. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Gini is a rescaled AUC and shares its blind spot: false positives are divided by almost 100,000 healthy babies, so a handful of percent look trivial even when they swamp the real cases. |
| Why other metrics are NOT suitable here | Accuracy is 99.95% by calling everyone healthy; KS and the ROC curve share the denominator problem; AUC itself is the same number rescaled. |
| Better alternative (if BAD fit) | Precision (positive predictive value) and the precision-recall curve at the chosen cut-off, against a 0.0005 baseline. |
| Business impact of choosing wrong | Families of healthy babies receive frightening false positives and need invasive follow-up tests, while doctors lose trust in the screen. |
| Small numeric example | 100,000 newborns, 50 affected. Gini 0.96 → AUC 0.98. At TPR 0.90, FPR 0.02: TP = 45; FP = 0.02 × 99,950 = 1,999. Precision = 45 / 2,044 = 0.022, so 98% of positive tests are false alarms. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Provisioning for Expected Loss on Rating Grades |
| Industry / Domain | Banking (regulatory provisioning) |
| Business Problem | An Indonesian bank assigns customers to three rating grades and must calculate expected credit loss (the money to set aside for future loan losses) under IFRS 9 accounting rules. It has two rating models with the same Gini but different default-probability scales. |
| ML Translation | Target: default (1) or not (0); the model output is a probability of default (PD) that goes straight into a loss formula, so calibration is critical. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Gini depends only on the order of customers, so scaling all PDs up by a factor of three leaves Gini unchanged while the provision triples. |
| Why other metrics are NOT suitable here | AUC and KS are order-only too; accuracy at a cut-off ignores the PD level; a single precision figure does not describe PD accuracy. |
| Better alternative (if BAD fit) | Calibration checks: Brier score or log loss, plus a comparison of predicted and observed default rates per grade. |
| Business impact of choosing wrong | The bank sets aside far too much capital (idle money) or, in the opposite direction, too little, which a regulator would treat as an under-provision. |
| Small numeric example | Three grades with PDs of 1%, 4%, 12%, each with IDR 1,000 billion exposure and 50% loss given default. Model A expected loss = 0.5 × 1,000 × (0.01 + 0.04 + 0.12) = IDR 85 billion, matching the observed rates. Model B PDs are 3%, 12%, 36%: 0.5 × 1,000 × (0.03 + 0.12 + 0.36) = IDR 255 billion. Both have the same Gini. |

**6. Quick decision rule:** Use Gini when you work in credit scoring or insurance, want the AUC information on a zero-to-one scale, and need to monitor ranking power over time; avoid it as the only metric for rare events, for probability or provisioning use, and for audiences who would confuse it with inequality indices.
