# Classification Case Studies, Part 2: Combined and Imbalance-Aware Metrics

## Table of Contents

- [Combined precision and recall scores](#combined-precision-and-recall-scores)
  - [F1 Score](#f1-score)
  - [F-beta Score (general beta)](#f-beta-score-general-beta)
  - [F0.5 Score](#f05-score)
  - [F2 Score](#f2-score)
- [Class-balanced scores for imbalanced data](#class-balanced-scores-for-imbalanced-data)
  - [G-mean](#g-mean)
  - [Balanced Accuracy](#balanced-accuracy)
  - [Matthews Correlation Coefficient (MCC)](#matthews-correlation-coefficient-mcc)
- [Chance-corrected agreement scores](#chance-corrected-agreement-scores)
  - [Cohen's Kappa](#cohens-kappa)
  - [Quadratic Weighted Kappa (QWK) [Added – not in source file]](#quadratic-weighted-kappa-qwk-added--not-in-source-file)

How to read this part: each metric follows the same six steps with five Europe and UK case studies on toy numbers; GOOD fit cases show when the metric is the right choice and BAD fit cases show where it misleads. Reminders: TP, FP, FN and TN are true positives (real cases caught), false positives (false alarms), false negatives (misses) and true negatives (correct all-clears); headings tagged Added are not in the source file.

## Combined precision and recall scores

### F1 Score

**1. What it measures (plain English):** F1 combines precision (of everything the model flagged, the share that was right) and recall (of everything real, the share the model found; also called sensitivity) into one number using the harmonic mean, a mean that is pulled towards the smaller of the two. It is also called the F-score or F-measure, and it ignores true negatives.

`F1 = 2 × Precision × Recall / (Precision + Recall) = 2×TP / (2×TP + FP + FN)`

**2. Intuition:** A hiring panel wants a shortlist with the right people (precision) without leaving out good candidates (recall). Shortlisting one obvious candidate gives perfect precision but poor recall, and the F1 mark stays very low; it is high only when both are reasonable.

**3. Benefits:**

- One number that works with automated model search and leaderboards.
- Ignores true negatives, so it is not inflated by a huge pool of easy negatives the way accuracy is on imbalanced data.
- Punishes one-sided models: precision 1.00 with recall 0.01 gives F1 = 0.020, not the 0.505 an ordinary average would give.
- Widely understood and extends to several classes through macro, micro or weighted averaging.

**4. Limitations / Potential issues:**

- Assumes a false alarm and a miss cost the same, which is rarely true; this is the reason F-beta exists.
- Ignores true negatives, so the model's skill at clearing negatives is invisible.
- Not symmetric: swapping which class is called positive changes the value, unlike MCC.
- Depends on the threshold (the score cut-off above which the model raises an alert), and the best threshold moves when the share of positives drifts.
- Always report precision and recall with it: F1 = 0.667 can be 0.60 and 0.75, or 0.95 and 0.51, which are very different systems.
- Cannot be compared across datasets with different rates of positives.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Finding duplicate citizen records in a municipal register |
| Industry / Domain | Government / municipal services |
| Business Problem | A Dutch municipality merges two population-register databases and must find records that describe the same person, so letters and benefit payments are not sent twice; a clerk checks every suggested pair by hand. |
| ML Translation | Target = pair is a true duplicate (1) or not (0); binary classification on 10,000 candidate record pairs; only 50 are real duplicates, so the data is imbalanced (one class is far rarer than the other). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A wrongly suggested pair wastes one clerk check and a missed duplicate causes one double letter, so the two errors cost about the same; F1 looks only at the duplicates and punishes a model that is weak on either precision (share of suggestions that are right) or recall (share of real duplicates found). |
| Why other metrics are NOT suitable here | Accuracy looks superb because 9,930 pairs are easy negatives (a model that flags nothing still scores 0.995); ROC-AUC (a score for how well the model ranks real positives above negatives, ignoring any cut-off) is also inflated by that huge easy-negative pool; F2 or F0.5 would wrongly say that one error type is costlier than the other. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A team trusting accuracy would approve a model that finds no duplicates, leaving about 50 double mailings and possible double benefit payments (50 × €250 = €12,500) in the register. |
| Small numeric example | TP=40, FP=20, FN=10, TN=9,930; precision = 40/60 = 0.667; recall = 40/50 = 0.800; F1 = 2×40/(2×40+20+10) = 80/110 = 0.727; accuracy = 9,970/10,000 = 0.997, while a model that flags nothing gets accuracy 9,950/10,000 = 0.995 and F1 = 0. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Routing billing-dispute tickets at a Spanish mobile operator |
| Industry / Domain | Telecom |
| Business Problem | A mobile operator receives about 1,000 support tickets in a sample week. Billing disputes must go to a small specialist team; an ordinary ticket sent there wastes specialist time, and a dispute left in the general queue is delayed and bounced later. |
| ML Translation | Target = ticket is a billing dispute (1) or not (0); binary text classification; 6% positives; predictions taken at one fixed threshold (the score cut-off above which a ticket is routed to the specialists). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Both mistakes cost roughly ten minutes of agent time, and the specialist queue is the thing the business cares about, so one balanced number for the positive class is right. |
| Why other metrics are NOT suitable here | Accuracy is 0.970 for the model but a lazy model that routes nothing already gets 0.940; F2 would over-reward catching disputes at the expense of specialist time; ROC-AUC does not tell managers how many tickets actually land on the specialist desk. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A model chosen on accuracy could leave about 60 disputes per 1,000 tickets in the wrong queue, each adding a day or two of delay and a repeat customer call. |
| Small numeric example | TP=45, FP=15, FN=15, TN=925; precision = 45/60 = 0.750; recall = 45/60 = 0.750; F1 = 2×45/(2×45+15+15) = 90/120 = 0.750; accuracy = 970/1,000 = 0.970 versus 0.940 for the do-nothing model whose F1 is 0. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Comparing two extractors of atrial fibrillation from discharge letters |
| Industry / Domain | Healthcare |
| Business Problem | A Dutch hospital builds a research registry by pulling the mention of atrial fibrillation out of free-text discharge letters. A wrongly included patient pollutes the registry and a missed patient shrinks it; the researchers say both hurt about equally. |
| ML Translation | Target = letter mentions atrial fibrillation (1) or not (0); text classification on 500 letters, 40 positive (8%); two candidate models compared at one fixed threshold. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The positives are what the registry needs, both error types matter equally, and F1 is the standard score for extraction tasks, so results can be compared with published extractors. |
| Why other metrics are NOT suitable here | Accuracy hides the 40 positives among 460 negatives; balanced accuracy (the average of recall on each class) ignores how many wrong patients flood the registry (false-alarm volume); F2 would favour recall, which is not the stated priority. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Picking model B (more patients found but only 60% precise) would put 24 wrong patients into the registry and trigger manual chart checks (24 × €15 = €360 per 500 letters) to clean it. |
| Small numeric example | Model A: TP=32, FP=8, FN=8 → precision 0.800, recall 0.800, F1(A) = 2×32/(2×32+8+8) = 64/80 = 0.800; Model B: TP=36, FP=24, FN=4 → precision 0.600, recall 0.900, F1(B) = 2×36/(2×36+24+4) = 72/100 = 0.720; F1 correctly prefers A. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Predicting wheel-bearing failures on a regional rail fleet |
| Industry / Domain | Transport / rail |
| Business Problem | A European regional rail operator uses axle-box sensor data to predict which wheel bearings will fail within 30 days. A false alarm means a depot inspection costing about €300; a missed failure can mean a derailment risk, a line closure and about €200,000 of cost. |
| ML Translation | Target = bearing fails within 30 days (1) or not (0); binary classification of about 2,000 bearings of which 40 fail (2% positives); hard yes/no alerts at a chosen threshold. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | F1 weights a miss and a false alarm equally, but here a miss is about 667 times costlier (200,000/300); two models with the identical F1 of 0.615 have very different costs, so F1 cannot tell them apart. |
| Why other metrics are NOT suitable here | Accuracy is dominated by the 1,960 healthy bearings; MCC (Matthews correlation coefficient) and balanced accuracy are also symmetric in the two error types so they share F1's blind spot; precision alone would reward a model that raises almost no alerts and misses most failures. |
| Better alternative (if BAD fit) | F-beta with a large β (β is the weight on recall; even F2 already separates the two models) or, best, expected cost in euros (the average money lost to misses and false alarms), because the cost of each error is known. |
| Business impact of choosing wrong | Choosing model A on an F1 tie costs €4,001,500 instead of €1,609,600, which is €2,391,900 more per 40 real failures, plus the safety risk of unplanned bearing failures. |
| Small numeric example | Model A: TP=20, FP=5, FN=20 (precision 0.800, recall 0.500); Model B: TP=32, FP=32, FN=8 (precision 0.500, recall 0.800); F1(A) = 2×20/(2×20+5+20) = 40/65 = 0.615 and F1(B) = 2×32/(2×32+32+8) = 64/104 = 0.615 (a tie); F2(A) = 100/(100+80+5) = 0.541, F2(B) = 160/(160+32+32) = 0.714; cost A = 20×200,000 + 5×300 = €4,001,500, cost B = 8×200,000 + 32×300 = €1,609,600. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Predicting on-time delivery slots for a UK online grocer |
| Industry / Domain | Logistics / retail |
| Business Problem | A UK online grocer predicts whether each delivery will arrive inside its promised slot (92% do) so that it can warn customers about risky ones; the planning team wants one honest score for the model. |
| ML Translation | Target = delivery on time (1, the positive class) or late (0); binary classification on 1,000 deliveries with 92% positives. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | F1 looks only at the positive class and ignores true negatives (late deliveries correctly spotted), so a model that says on time for everything scores 0.958 while knowing nothing; F1 also changes if you swap which class is called positive. |
| Why other metrics are NOT suitable here | Accuracy is 0.920 for the lazy model and precision is also 0.920, so both are fooled; recall is a perfect 1.000 for the lazy model; ROC-AUC would expose it (0.5) but says nothing about the deployed cut-off. |
| Better alternative (if BAD fit) | MCC (Matthews correlation coefficient, a correlation between truth and prediction that uses all four cells), because it gives exactly 0 to the lazy model and is unchanged when the class labels are swapped. |
| Business impact of choosing wrong | Planners would think the lazy model is nearly as good as the real one and drop the late-delivery warning tool, leaving about 80 late deliveries per 1,000 unannounced; at a £10 goodwill voucher each, that is £800 per 1,000 deliveries. |
| Small numeric example | Lazy model (on time for all): TP=920, FP=80, FN=0, TN=0; F1 = 2×920/(2×920+80+0) = 1,840/1,920 = 0.958; MCC = 0. Real model: TP=900, FP=40, FN=20, TN=40; F1 = 2×900/(2×900+40+20) = 1,800/1,860 = 0.968; MCC = (900×40 - 40×20)/√(940×920×80×60) = 35,200/64,428.6 = 0.546. F1 differs by only 0.010, MCC separates them clearly (0 versus 0.546). |

**6. Quick decision rule:** Use F1 when the positive class is what matters, the costs of a false alarm and a miss are about equal and true negatives are uninteresting; avoid it when costs are clearly unequal, when the negative class matters too, or when you need a number that does not change with the label convention.

### F-beta Score (general beta)

**1. What it measures (plain English):** F-beta is F1 with a dial: β says how many times more important recall is than precision. It is also called the generalised F-score; β = 1 gives F1, β above 1 favours recall, β below 1 favours precision, and a cost-based rule sets β = √(cost of a miss / cost of a false alarm).

`Fβ = (1 + β²) × Precision × Recall / (β² × Precision + Recall) = (1 + β²)×TP / ((1 + β²)×TP + β²×FN + FP)`

**2. Intuition:** A see-saw with precision on one side and recall on the other: β decides where the pivot sits, so a large β lets recall carry the weight and a small β lets precision carry it.

**3. Benefits:**

- Puts a business priority into one defensible number.
- The rule β = √(cost ratio) links the score to a euro cost matrix.
- Reduces to F1 at β = 1, so it generalises rather than replaces it.
- A single number that automated model search can optimise.

**4. Limitations / Potential issues:**

- β is a judgement call and stakeholders will argue about it, so derive it from costs and fix it before the project starts.
- Still ignores true negatives and still depends on the threshold.
- Values with different β are not comparable, so never compare an F2 with an F1.
- Encodes only a ratio of costs, so it cannot say whether the model is worth deploying in money terms.
- Uses hard yes or no decisions, so it says nothing about the quality of probabilities.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Choosing β for pressure-sensor leak alerts at a Nordic water utility |
| Industry / Domain | Utilities / water |
| Business Problem | A Nordic water utility's pressure sensors flag pipe segments that may be leaking. Sending a crew to a false alarm costs about €100; a missed leak wastes water and damages roads, about €4,000. |
| ML Translation | Target = pipe segment is leaking this week (1) or not (0); binary classification; 100 true leaks in the evaluation set; two candidate models; cost ratio k = 4,000/100 = 40, so β = √40 = 6.32 (β is the weight on recall; recall counts β times as much as precision). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The cost ratio is known, so β = √40 turns it directly into one score, and F-beta then picks the same model that the euro cost picks. |
| Why other metrics are NOT suitable here | F1 assumes equal costs and prefers the cheaper-looking model that misses 40 leaks; accuracy ignores the rare leaks; MCC and balanced accuracy are symmetric in the two error types and cannot encode a 40-to-1 cost ratio. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Selecting by F1 would choose model M1 at €162,000 instead of M2 at €60,000, which is €102,000 more per evaluation period. |
| Small numeric example | M1: TP=60, FP=20, FN=40; M2: TP=90, FP=200, FN=10; F1(M1) = 2×60/(2×60+20+40) = 120/180 = 0.667; F1(M2) = 2×90/(2×90+200+10) = 180/390 = 0.462; Fβ(M1) = 41×60/(41×60+40×40+20) = 2,460/4,080 = 0.603; Fβ(M2) = 41×90/(41×90+40×10+200) = 3,690/4,290 = 0.860; cost M1 = 40×4,000 + 20×100 = €162,000; cost M2 = 10×4,000 + 200×100 = €60,000; F1 picks M1 but Fβ and cost both pick M2. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Tuning a counterfeit-listing takedown tool for a French online marketplace |
| Industry / Domain | E-commerce |
| Business Problem | A French online marketplace automatically removes listings that look counterfeit. Removing a genuine seller's listing costs about €150 (compensation, support, lost trust); a counterfeit left online costs about €30 to handle later when a brand complains. |
| ML Translation | Target = listing is counterfeit (1) or genuine (0); binary classification; 100 counterfeits in the evaluation set; cost ratio k = 30/150 = 0.2, so β = √0.2 = 0.447 (a β below 1 means precision counts more than recall). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Here a false alarm is five times costlier than a miss, which is the opposite of most screening problems; F-beta with β = 0.447 encodes that and picks the cheaper model. |
| Why other metrics are NOT suitable here | F1 treats a wrong removal and a missed counterfeit as equal and picks the model that removes too many genuine listings; F2 would push in exactly the wrong direction; recall alone would reward removing every listing. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Selecting by F1 would deploy M1 at €6,600 instead of M2 at €2,700, which is €3,900 more per 100 counterfeits, and would anger genuine sellers. |
| Small numeric example | M1: TP=80, FP=40, FN=20; M2: TP=60, FP=10, FN=40; F1(M1) = 2×80/(2×80+40+20) = 160/220 = 0.727; F1(M2) = 2×60/(2×60+10+40) = 120/170 = 0.706; Fβ(M1) = 1.2×80/(1.2×80+0.2×20+40) = 96/140 = 0.686; Fβ(M2) = 1.2×60/(1.2×60+0.2×40+10) = 72/90 = 0.800; cost M1 = 20×30 + 40×150 = €6,600; cost M2 = 40×30 + 10×150 = €2,700; F1 picks M1 but Fβ and cost pick M2. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Setting β=3 for engine-vibration alerts on a Greek ferry fleet |
| Industry / Domain | Transport / maritime |
| Business Problem | A Greek ferry operator's vibration sensors predict engine faults before a sailing. A missed fault at sea costs about €90,000 (towing, cancelled sailings, passenger compensation); a precautionary inspection costs €10,000. |
| ML Translation | Target = engine develops a fault on the next sailing (1) or not (0); binary classification; 50 real faults in the evaluation set; cost ratio k = 90,000/10,000 = 9, so β = √9 = 3. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A clean cost ratio of 9 gives β = 3 exactly, and F3 follows the euro cost when ranking the two models, so the metric is both defensible to the board and easy to automate in model search. |
| Why other metrics are NOT suitable here | F1 would prefer the cautious model that misses 20 faults; accuracy is dominated by the many fault-free sailings; ROC-AUC does not say which alert threshold to run at sea. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Choosing by F1 would select M1 at €1,850,000 instead of M2 at €850,000, which is €1,000,000 more per 50 real faults, plus passengers stranded at sea. |
| Small numeric example | M1: TP=30, FP=5, FN=20; M2: TP=45, FP=40, FN=5; F1(M1) = 2×30/(2×30+5+20) = 60/85 = 0.706; F1(M2) = 2×45/(2×45+40+5) = 90/135 = 0.667; F3(M1) = 10×30/(10×30+9×20+5) = 300/485 = 0.619; F3(M2) = 10×45/(10×45+9×5+40) = 450/535 = 0.841; cost M1 = 20×90,000 + 5×10,000 = €1,850,000; cost M2 = 5×90,000 + 40×10,000 = €850,000. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Judging a meter-tampering inspection model for a Spanish energy retailer |
| Industry / Domain | Energy |
| Business Problem | A Spanish energy retailer's model flags customers whose smart-meter readings look tampered with. Each inspection visit costs €120; a confirmed tampering recovers about €900 of unbilled energy. Management asks: is the model worth switching on? |
| ML Translation | Target = meter is tampered with (1) or not (0); binary classification; 2,000 customers, 50 truly tampered (2.5%); the model flags 400 customers at its chosen threshold. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | F-beta compresses the costs into a unit-free ratio; it can say that one model is better than another but not whether the programme earns or loses euros, and this one loses money even though its scores look reasonable. |
| Why other metrics are NOT suitable here | F1 (0.178) and F2 (0.333) are also unit-free and cannot answer a go or no-go question; accuracy is 0.815 and says nothing about money; recall of 0.800 looks impressive but ignores the 360 wasted visits. |
| Better alternative (if BAD fit) | Expected cost (or net value) in euros: net = confirmed cases × €900 minus visits × €120, which also gives the best threshold directly. |
| Business impact of choosing wrong | Switching the model on because the score looks fine loses €12,000 per 2,000 customers screened; on a base of 2 million customers that scales to about €12,000,000. |
| Small numeric example | TP=40, FP=360, FN=10, TN=1,590; F2 = 5×40/(5×40+4×10+360) = 200/600 = 0.333; net value = 40×900 - 400×120 = 36,000 - 48,000 = -€12,000 compared with doing nothing (€0); a euro-based view says do not deploy at this threshold. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Pricing motor policies from claim-probability scores at a Spanish insurer |
| Industry / Domain | Insurance |
| Business Problem | A Spanish insurer feeds the model's claim probability straight into the risk part of the premium, so the probability itself must be accurate (well calibrated, meaning a stated 30% risk really means about 3 claims in 10). |
| ML Translation | Target = policyholder claims within the year (1) or not (0); the model outputs a probability for each policyholder; F-beta needs hard yes/no labels, so a threshold of 0.5 would have to be applied first. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | F-beta only sees the yes/no decision after thresholding, so two models with very different probabilities can score identically; the premium depends on the probability values, which F-beta ignores. |
| Why other metrics are NOT suitable here | F1 and F0.5 have the same blind spot; accuracy also ignores probability quality; ROC-AUC checks only the ranking of customers, not whether 0.6 means a 60% risk. |
| Better alternative (if BAD fit) | Brier score (average squared gap between probability and outcome) or log loss (a penalty that grows sharply for confident wrong probabilities), plus a calibration check. |
| Business impact of choosing wrong | Premiums built on model B would overstate every customer's risk, so safe drivers would be overcharged and would leave for competitors, while the insurer still could not price its high-risk customers accurately. |
| Small numeric example | 6 policyholders, 2 claim; Model A probabilities 0.9, 0.8, 0.2, 0.1, 0.1, 0.2; Model B 0.6, 0.55, 0.45, 0.4, 0.4, 0.45; at threshold 0.5 both predict the same labels, so F1 = F2 = 1.000 for both; Brier A = 0.025, Brier B = 0.181; log loss A = 0.164, log loss B = 0.554; average predicted risk A = 0.383, B = 0.475 against a real claim rate of 0.333; the better model is clearly A. |

**6. Quick decision rule:** Use F-beta when you can state how much costlier a miss is than a false alarm and want that in one score; avoid it when the real constraint is review capacity, when you need a go or no-go in currency, or when the probabilities themselves are used.

### F0.5 Score

**1. What it measures (plain English):** F0.5 is F-beta with β = 0.5, so precision counts twice as much as recall; it is the right lens when a false alarm is costlier than a miss. It is sometimes called the precision-weighted F-score.

`F0.5 = 1.25 × Precision × Recall / (0.25 × Precision + Recall) = 1.25×TP / (1.25×TP + 0.25×FN + FP)`

**2. Intuition:** A restaurant guide would rather print three excellent recommendations than ten where four are poor; leaving out a decent restaurant costs little, listing a bad one costs trust.

**3. Benefits:**

- Rewards models whose alerts are mostly right, which protects customers, staff time and brand trust.
- Equals the cost-based F-beta when a false alarm costs four times as much as a miss.
- Simple extension of F1 that most data teams already know.
- Comparing F0.5, F1 and F2 for one model shows which side of the trade-off it favours.

**4. Limitations / Potential issues:**

- Dangerous in safety-critical work where a miss is worse than a false alarm; copying it from a notebook built for another problem is a common mistake.
- Ignores true negatives and depends on the threshold, so models with identical rankings can score very differently.
- Cannot be compared with F1 or F2 values.
- Encodes only a cost ratio and not absolute money.
- Harder to explain to managers than precision and recall.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Phoning likely switchers for a UK energy-comparison site |
| Industry / Domain | Marketing |
| Business Problem | A UK energy-comparison website phones customers its model thinks are ready to switch supplier. An unwanted call risks a regulator complaint and costs about £8 in agent time and goodwill; a likely switcher who is not called often switches online anyway, so a miss costs about £2 of expected margin. |
| ML Translation | Target = customer will switch within 30 days (1) or not (0); binary classification; 100 genuine switchers in the evaluation set; cost ratio k = 2/8 = 0.25, so β = √0.25 = 0.5. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A false call is four times costlier than a miss, and β = 0.5 builds that exact ratio into the score, so precision gets twice the weight of recall. |
| Why other metrics are NOT suitable here | F1 treats the two errors alike and picks the model that makes 60 unwanted calls; F2 pushes the wrong way; recall alone rewards calling everybody. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Picking by F1 would choose model Y at £520 instead of model X at £180, which is £340 more per 100 switchers, plus more complaints. |
| Small numeric example | X: TP=50, FP=10, FN=50; Y: TP=80, FP=60, FN=20; F1(X) = 2×50/(2×50+10+50) = 100/160 = 0.625; F1(Y) = 2×80/(2×80+60+20) = 160/240 = 0.667; F0.5(X) = 1.25×50/(1.25×50+0.25×50+10) = 62.5/85 = 0.735; F0.5(Y) = 1.25×80/(1.25×80+0.25×20+60) = 100/165 = 0.606; cost X = 50×2 + 10×8 = £180; cost Y = 20×2 + 60×8 = £520; F0.5 picks X, which is the cheaper model. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Flagging risky clauses in contracts for a London law firm |
| Industry / Domain | Professional services / legal |
| Business Problem | A London law firm uses a model to flag risky clauses in supplier contracts for associate review. Each flagged clause costs about £80 of lawyer time to read; a risky clause that is missed is usually caught later by the partner review at about £20 extra. |
| ML Translation | Target = clause is risky (1) or not (0); binary text classification on 200 clauses, 40 truly risky; cost ratio k = 20/80 = 0.25, so β = 0.5. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Because a second review step catches most misses, the real cost is lawyer time spent on false flags, and F0.5 weights precision twice as heavily as recall. |
| Why other metrics are NOT suitable here | F2 would choose the model that floods associates with 30 false flags; accuracy is dominated by the 160 non-risky clauses; ROC-AUC ignores the actual review workload. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using F2 would choose model Y at £2,480 instead of model X at £560, which is £1,920 more per 200 clauses and a frustrated legal team. |
| Small numeric example | X: TP=28, FP=4, FN=12; Y: TP=36, FP=30, FN=4; F0.5(X) = 1.25×28/(1.25×28+0.25×12+4) = 35/42 = 0.833; F0.5(Y) = 1.25×36/(1.25×36+0.25×4+30) = 45/76 = 0.592; F2(X) = 5×28/(5×28+4×12+4) = 140/192 = 0.729; F2(Y) = 5×36/(5×36+4×4+30) = 180/226 = 0.796; cost X = 12×20 + 4×80 = £560; cost Y = 4×20 + 30×80 = £2,480; F0.5 picks X, F2 would wrongly pick Y. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Flagging hold baggage for manual search at a regional European airport |
| Industry / Domain | Transport / airports |
| Business Problem | A regional European airport scans about 10,000 hold bags a day and uses a model to send suspicious bags to a manual search; about 20 bags a day truly contain a prohibited item. A missed item is a security failure, while an extra search costs a few minutes. |
| ML Translation | Target = bag contains a prohibited item (1) or not (0); binary classification at 0.2% prevalence (a very rare positive class); two candidate models. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | F0.5 rewards precision, so it prefers a model that searches almost nothing and misses half of the prohibited items; here a miss is far worse than a false alarm, so the metric points the wrong way. |
| Why other metrics are NOT suitable here | F1 also prefers the cautious model P; accuracy is 99.8% for a model that finds nothing; precision alone rewards doing nothing even more. |
| Better alternative (if BAD fit) | F2 or a higher-β F-beta, or better, recall at a fixed daily search capacity (how many bags can staff search per day). |
| Business impact of choosing wrong | Selecting the F0.5 winner would let about 10 prohibited items per day through instead of 1, a regulatory and safety failure that no search saving can justify. |
| Small numeric example | P: TP=10, FP=1, FN=10; Q: TP=19, FP=60, FN=1; F0.5(P) = 1.25×10/(1.25×10+0.25×10+1) = 12.5/16 = 0.781; F0.5(Q) = 1.25×19/(1.25×19+0.25×1+60) = 23.75/84 = 0.283 (picks P, which misses 10 of 20); F2(P) = 5×10/(5×10+4×10+1) = 50/91 = 0.549; F2(Q) = 5×19/(5×19+4×1+60) = 95/159 = 0.597 (picks Q, which misses 1 of 20). |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Spotting adverse events in patient diaries during a European clinical trial |
| Industry / Domain | Pharma / clinical trials |
| Business Problem | A pharma sponsor of a European trial uses a text model to spot possible adverse events (side effects) in patients' e-diary entries; safety events must be reported to the regulator within strict deadlines, and a medical reviewer then checks every flag. |
| ML Translation | Target = diary entry describes an adverse event (1) or not (0); binary text classification on 300 entries, 30 true events; hard flags at one threshold. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | F0.5 prefers the model with few false flags, which here misses half of the real safety events; a missed event is a patient-safety and regulatory problem while a false flag only costs a reviewer a minute. |
| Why other metrics are NOT suitable here | F1 would pick the better model but does not weight recall enough; accuracy is dominated by the 270 non-events; MCC is symmetric so it cannot express that safety misses matter more. |
| Better alternative (if BAD fit) | F2 (or a recall target with a precision floor, for example recall of at least 0.95 with precision of at least 0.50). |
| Business impact of choosing wrong | Choosing model A would leave 15 of 30 real events unflagged, risking late safety reporting, regulator findings and, in the worst case, harm to patients. |
| Small numeric example | A: TP=15, FP=1, FN=15; B: TP=28, FP=12, FN=2; F0.5(A) = 1.25×15/(1.25×15+0.25×15+1) = 18.75/23.5 = 0.798; F0.5(B) = 1.25×28/(1.25×28+0.25×2+12) = 35/47.5 = 0.737 (picks A); F2(A) = 5×15/(5×15+4×15+1) = 75/136 = 0.551; F2(B) = 5×28/(5×28+4×2+12) = 140/160 = 0.875 (picks B). |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Ranking cross-sell leads for an Austrian insurer's call centre |
| Industry / Domain | Insurance |
| Business Problem | An Austrian insurer scores existing customers for a cross-sell call campaign. The call team will pick its own cut-off later, based on how many calls it can make that week, so the model's job is to rank the best leads first. |
| ML Translation | Target = customer buys the extra product (1) or not (0); the model outputs a score for each customer; the choice of threshold has not been made yet, so any single-threshold metric depends on an arbitrary cut-off. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | F0.5 is computed at one threshold; two models that rank customers identically get completely different F0.5 values just because one model's scores are scaled lower, so the score reflects the cut-off, not the ranking skill. |
| Why other metrics are NOT suitable here | F1 and F2 have the same threshold problem; accuracy also depends on the arbitrary cut-off; Brier score and log loss judge probability quality rather than ranking. |
| Better alternative (if BAD fit) | PR-AUC (average precision, a single number summarising precision across all cut-offs), or precision at the number of calls the team can make. |
| Business impact of choosing wrong | A team that compares models by F0.5 at 0.5 could throw away a perfectly good ranking model because its scores are low, delaying the campaign and wasting analyst time. |
| Small numeric example | 8 customers, 3 buyers; Model 1 scores 0.9, 0.8, 0.7, 0.6, 0.3, 0.2, 0.2, 0.1 (buyers at ranks 1, 2 and 4); Model 2 has the same scores multiplied by 0.5, so the ranking is identical; at threshold 0.5 Model 1 gives TP=3, FP=1, FN=0, F0.5 = 3.75/(3.75+0+1) = 0.789; Model 2 flags nobody, TP=0, F0.5 = 0; PR-AUC (average precision) is 0.917 for both. |

**6. Quick decision rule:** Use F0.5 when every false alarm is expensive or visible to customers and a miss is cheap or caught later; avoid it when a miss is serious, when the threshold has not been set yet, or when capacity rather than cost drives the decision.

### F2 Score

**1. What it measures (plain English):** F2 is F-beta with β = 2, so recall counts twice as much as precision; it suits problems where a miss is worse than a false alarm. It is sometimes called the recall-weighted F-score.

`F2 = 5 × Precision × Recall / (4 × Precision + Recall) = 5×TP / (5×TP + 4×FN + FP)`

**2. Intuition:** A lifeguard scanning the beach would rather wave at ten swimmers who are fine than overlook one in trouble; a few extra whistles are cheap compared with a missed rescue.

**3. Benefits:**

- Steers the search towards high-recall models without letting precision fall to zero, which recall alone would allow.
- Equals the cost-based F-beta when a miss costs four times as much as a false alarm.
- Easy to explain to non-technical staff as catch more, accept more false alarms.
- Works with automated search through a scoring wrapper.

**4. Limitations / Potential issues:**

- Tolerates very low precision, so it can pick a model whose alert volume the team cannot handle.
- Wrong choice when false alarms are costly, user-facing or automatic.
- Ignores true negatives and depends on the threshold.
- Encodes only a cost ratio of 4, which may not match your real costs.
- Cannot be compared with F1 or F0.5.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Rejecting vials with particles at an Irish injectable-drug plant |
| Industry / Domain | Manufacturing / pharma |
| Business Problem | An Irish plant inspects vials of injectable medicine with cameras. A vial with a particle that is shipped can trigger a batch investigation and recall worth about €8,000; a good vial wrongly rejected loses about €2,000 of product. |
| ML Translation | Target = vial contains a particle (1) or not (0); binary image classification on 5,000 vials, 50 defective; cost ratio k = 8,000/2,000 = 4, so β = 2 exactly. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A miss costs four times a false reject, which is exactly what F2 encodes (recall counts twice as much as precision, and FN is weighted by β² = 4), and F2 picks the cheaper model. |
| Why other metrics are NOT suitable here | F1 treats the two errors alike and picks the model that lets 20 bad vials through; accuracy is 99.0% even for a model that catches no defect; ROC-AUC does not choose an operating point. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Selecting by F1 would deploy model X at €170,000 instead of model Y at €130,000, which is €40,000 more per 50 defective vials, plus the regulatory exposure of shipped defects. |
| Small numeric example | X: TP=30, FP=5, FN=20; Y: TP=45, FP=45, FN=5; F1(X) = 2×30/(2×30+5+20) = 60/85 = 0.706; F1(Y) = 2×45/(2×45+45+5) = 90/140 = 0.643; F2(X) = 5×30/(5×30+4×20+5) = 150/235 = 0.638; F2(Y) = 5×45/(5×45+4×5+45) = 225/290 = 0.776; cost X = 20×8,000 + 5×2,000 = €170,000; cost Y = 5×8,000 + 45×2,000 = €130,000; F2 and the euro cost agree on Y. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Alerting carers to falls among elderly residents in rural Finland |
| Industry / Domain | Healthcare / municipal care |
| Business Problem | A rural Finnish municipality gives elderly residents a wearable that predicts a fall from movement data and alerts a home-care team. A missed fall means extra emergency care and a longer hospital stay, about €1,200; an unnecessary visit over long rural distances costs about €300. |
| ML Translation | Target = fall in the next hour (1) or not (0); binary classification on 40 real falls from a pilot; cost ratio k = 1,200/300 = 4, so β = 2. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A miss is four times costlier than a false visit, which is exactly the F2 weighting, and the model with the higher F2 is also the cheaper one. |
| Why other metrics are NOT suitable here | F1 would pick the model that misses 16 of 40 falls; accuracy is dominated by the many quiet hours; precision alone rewards a model that rarely alerts. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using F1 would deploy model X at €22,200 instead of model Y at €19,800, which is €2,400 more per 40 falls, and 12 more residents lying unattended. |
| Small numeric example | X: TP=24, FP=10, FN=16; Y: TP=36, FP=50, FN=4; F1(X) = 2×24/(2×24+10+16) = 48/74 = 0.649; F1(Y) = 2×36/(2×36+50+4) = 72/126 = 0.571; F2(X) = 5×24/(5×24+4×16+10) = 120/194 = 0.619; F2(Y) = 5×36/(5×36+4×4+50) = 180/246 = 0.732; cost X = 16×1,200 + 10×300 = €22,200; cost Y = 4×1,200 + 50×300 = €19,800. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Predicting backup-battery failure at mobile masts for a UK operator |
| Industry / Domain | Telecom |
| Business Problem | A UK mobile operator predicts which mast batteries will fail in the next 7 days. A missed failure causes an outage, service credits and an emergency call-out, about £6,000; a precautionary check costs about £1,500. |
| ML Translation | Target = battery fails within 7 days (1) or not (0); binary classification on 1,000 masts, 20 failures; cost ratio k = 6,000/1,500 = 4, so β = 2. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The miss-to-false-alarm ratio is four, so F2 captures the priority, and it ranks the higher-recall model first, matching the cost ranking. |
| Why other metrics are NOT suitable here | F1 would pick the cautious model that misses 8 of 20 failures; accuracy is dominated by the 980 healthy masts; MCC is symmetric and ignores the cost gap. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A choice by F1 would cost £57,000 instead of £48,000, which is £9,000 more per 20 failures, plus unhappy business customers during outages. |
| Small numeric example | X: TP=12, FP=6, FN=8; Y: TP=18, FP=24, FN=2; F1(X) = 2×12/(2×12+6+8) = 24/38 = 0.632; F1(Y) = 2×18/(2×18+24+2) = 36/62 = 0.581; F2(X) = 5×12/(5×12+4×8+6) = 60/98 = 0.612; F2(Y) = 5×18/(5×18+4×2+24) = 90/122 = 0.738; cost X = 8×6,000 + 6×1,500 = £57,000; cost Y = 2×6,000 + 24×1,500 = £48,000. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Prioritising mortgage-arrears calls at a Greek bank |
| Industry / Domain | Banking |
| Business Problem | A Greek bank's collections team can make about 200 outreach calls a month to mortgage customers who may miss a payment. The model is tuned to catch almost all future arrears among 2,000 watch-list accounts, 100 of which will go into arrears. |
| ML Translation | Target = account misses the next payment (1) or not (0); binary classification; 5% positives; the F2-optimal threshold flags 800 accounts. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | F2 happily accepts very low precision to gain recall, so it rewards a model that raises 800 alerts when staff can work only 200; the score looks decent while the output is unusable. |
| Why other metrics are NOT suitable here | F1 and F0.5 also ignore capacity; accuracy is dominated by the 1,900 accounts that will pay; recall alone rewards flagging everybody. |
| Better alternative (if BAD fit) | Precision at k (precision among the k highest-ranked alerts, here k = 200 calls) and recall at the same k, or expected cost including the cost per call. |
| Business impact of choosing wrong | Callers would work a random-looking 200 of 800 alerts, so most calls would hit customers who would have paid anyway, while 100 genuine arrears cases are mostly left unworked; the bank loses collections and wastes staff time. |
| Small numeric example | 800 alerts: TP=95, FP=705, FN=5; precision = 95/800 = 0.119; recall = 95/100 = 0.950; F2 = 5×95/(5×95+4×5+705) = 475/1,200 = 0.396; with capacity 200, a ranking that puts 60 true cases in the top 200 gives precision at 200 = 60/200 = 0.300 and recall at 200 = 60/100 = 0.600, which is the number the team can act on. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Auto-freezing suspected money-mule accounts at a UK digital bank |
| Industry / Domain | Banking / retail payments |
| Business Problem | A UK digital bank automatically freezes accounts that look like money-mule accounts (accounts used to pass on criminal money) with no human check first. Wrongly freezing an honest student's account costs about £200 in compensation and complaint handling; a mule account left open costs about £60. |
| ML Translation | Target = account is a mule (1) or not (0); binary classification on 1,000 accounts, 40 real mules; cost ratio k = 60/200 = 0.3, so a false freeze is the costlier error. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | F2 weights recall, so it favours the aggressive model that freezes 80 honest accounts; with no human in the loop a false alarm is the expensive mistake, and the metric points in the wrong direction. |
| Why other metrics are NOT suitable here | F1 treats the errors as equal and also leans towards the aggressive model; accuracy is dominated by honest accounts; recall alone rewards freezing everyone. |
| Better alternative (if BAD fit) | F0.5 (or an F-beta with β = √0.3 = 0.55), or expected cost in pounds. |
| Business impact of choosing wrong | Choosing the F2 winner would cost £16,120 instead of £2,560, which is £13,560 more per 1,000 accounts, plus 72 more honest customers wrongly frozen and a risk of regulator complaints. |
| Small numeric example | M1: TP=38, FP=80, FN=2; M2: TP=24, FP=8, FN=16; F2(M1) = 5×38/(5×38+4×2+80) = 190/278 = 0.683; F2(M2) = 5×24/(5×24+4×16+8) = 120/192 = 0.625 (picks M1); F0.5(M1) = 1.25×38/(1.25×38+0.25×2+80) = 47.5/128 = 0.371; F0.5(M2) = 1.25×24/(1.25×24+0.25×16+8) = 30/42 = 0.714 (picks M2); cost M1 = 2×60 + 80×200 = £16,120; cost M2 = 16×60 + 8×200 = £2,560. |

**6. Quick decision rule:** Use F2 when a miss costs about four times a false alarm and the team can handle the extra alerts; avoid it when review capacity is limited, when false alarms trigger automatic harm, or when the exact cost ratio is far from 4.

## Class-balanced scores for imbalanced data

### G-mean

**1. What it measures (plain English):** G-mean is the geometric mean (the square root of the product) of sensitivity (the share of real positives found, also called recall) and specificity (the share of real negatives correctly cleared, also called true negative rate). It is also written geometric mean score or G-measure, and it collapses to 0 if either class is completely missed.

`G-mean = √(Sensitivity × Specificity)`

**2. Intuition:** A two-legged stool is only as steady as its weaker leg: if one leg is missing the whole thing falls over, however strong the other leg is.

**3. Benefits:**

- Uses all four cells of the confusion matrix and scores a model that ignores one class at exactly 0.
- Immune to the accuracy paradox: a model that always predicts the majority class scores 0, not 0.99.
- Does not depend on how common the positive class is, because both parts are rates within one class.
- Symmetric: relabelling the classes gives the same value.

**4. Limitations / Potential issues:**

- Cannot express unequal costs, because there is no weighting dial.
- Blind to false-alarm volume: specificity hides thousands of false alarms when negatives are very common.
- With several classes, one rare class with a handful of test samples can swing the score from 0 to a high value.
- Depends on the threshold and is less familiar to managers than accuracy or F1.
- Not in core scikit-learn (it is in imbalanced-learn).

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Checking spot welds at a Polish car-parts supplier |
| Industry / Domain | Manufacturing / automotive |
| Business Problem | A Polish car-parts supplier tests 5,000 spot welds per shift with an ultrasound model; scrapping a good weld wastes parts and shipping a bad weld risks a customer line stoppage, so management insists the model must be good at both. |
| ML Translation | Target = weld is defective (1) or good (0); binary classification; 100 defective of 5,000 (2%, an imbalanced set); sensitivity (share of defective welds caught) and specificity (share of good welds correctly passed) both matter. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | G-mean multiplies sensitivity by specificity, so a model that ignores the rare defects scores exactly 0, and one that scraps good welds also gets punished; no class can be neglected. |
| Why other metrics are NOT suitable here | Accuracy prefers the lazy pass-everything model (0.980) over the real model (0.946); F1 ignores the 4,650 good welds that were passed correctly; precision alone ignores the defects that were missed. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Selecting on accuracy would deploy a model that passes every defective weld, about 100 defects per 5,000 welds reaching customers. |
| Small numeric example | Real model: TP=80, FN=20, FP=250, TN=4,650; sensitivity = 80/100 = 0.800; specificity = 4,650/4,900 = 0.949; G-mean = √(0.800 × 0.949) = 0.871; accuracy = 0.946. Lazy model (pass all): sensitivity 0, G-mean = 0, accuracy = 4,900/5,000 = 0.980. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Ranking pressure-ulcer risk on admission in a German hospital |
| Industry / Domain | Healthcare |
| Business Problem | A German hospital model predicts which newly admitted patients will develop a pressure ulcer. Missing a patient means avoidable harm; starting the prevention bundle (special mattress, repositioning every two hours) for everyone uses scarce nursing time, so both classes matter. |
| ML Translation | Target = patient develops a pressure ulcer (1) or not (0); binary classification on 2,000 admissions, 120 positives (6%); two candidate models compared at fixed thresholds. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | G-mean uses sensitivity and specificity, the pair clinicians already read, and it collapses if either class is badly served, which exposes the model that treats nearly everybody as high risk. |
| Why other metrics are NOT suitable here | Accuracy gives 0.940 to a model that predicts no ulcers at all (against 0.888 for model A); F1 ignores the true negatives that decide nursing workload; recall alone makes model B look excellent (0.950). |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Choosing model B on recall would start prevention for 1,242 of 2,000 patients, burning nursing hours and mattresses, for only 30 extra patients found. |
| Small numeric example | A: sensitivity = 84/120 = 0.700, specificity = 1,692/1,880 = 0.900, G-mean = √0.630 = 0.794; B: sensitivity = 114/120 = 0.950, specificity = 752/1,880 = 0.400, G-mean = √0.380 = 0.616; G-mean prefers A. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Screening mortgage affordability at a UK building society |
| Industry / Domain | Banking |
| Business Problem | A UK building society uses a model to decline mortgage applications that would be unaffordable. The regulator expects it to protect customers from unaffordable loans and also not to turn away borrowers who could afford them, so both mistakes are scrutinised. |
| ML Translation | Target = application would fall into serious arrears (1) or not (0); binary classification on 10,000 applications, 600 risky (6%); sensitivity and specificity are reported to the risk committee. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | G-mean is zero for the approve-everything model and rewards only models that are decent on both risky and safe applicants, matching the regulator's two-sided expectation. |
| Why other metrics are NOT suitable here | Accuracy is 0.940 for approve-everything and only 0.891 for the real model, so it prefers the useless one; F1 ignores the safe customers wrongly declined; ROC-AUC does not report performance at the operating point. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using accuracy would approve a model that declines nobody, leaving about 600 unaffordable loans per 10,000 and a conduct-risk finding. |
| Small numeric example | TP=450, FN=150, FP=940, TN=8,460; sensitivity = 450/600 = 0.750; specificity = 8,460/9,400 = 0.900; G-mean = √(0.750 × 0.900) = √0.675 = 0.822; approve-all: accuracy 0.940 but G-mean = 0. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Classifying foreign objects found on a conveyor in an Irish food plant |
| Industry / Domain | Manufacturing / food |
| Business Problem | An Irish food plant's camera model classifies foreign objects found on a conveyor as metal, plastic, wood or glass. Glass is rare, so the test set holds only 2 glass images next to 40 metal, 30 plastic and 20 wood. |
| ML Translation | Target = object type (4 classes, multi-class classification); per-class recall (share of each type correctly identified) is 0.950 for metal, 0.900 for plastic, 0.850 for wood, and 0 or 0.5 for glass depending on one image. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | G-mean is the geometric mean of all per-class recalls, so a single class with a tiny test sample controls the whole score: one image moves it from 0 to 0.776, which is noise rather than information. |
| Why other metrics are NOT suitable here | Accuracy is dominated by metal and plastic; F1 per class has the same tiny-sample noise for glass; MCC is also unstable with so few glass examples. |
| Better alternative (if BAD fit) | Balanced accuracy (the average of per-class recalls, which moves gently when one class changes) together with a per-class recall table, confidence intervals and more rare-class test images. |
| Business impact of choosing wrong | Teams would reject or accept a good model by luck of one image, delaying the line or accepting a model with unproven glass detection. |
| Small numeric example | Recalls: metal 38/40 = 0.950, plastic 27/30 = 0.900, wood 17/20 = 0.850; glass 0/2 → G-mean = (0.950×0.900×0.850×0)^(1/4) = 0.000; glass 1/2 → G-mean = (0.950×0.900×0.850×0.500)^(1/4) = 0.776; balanced accuracy moves only from 0.675 to 0.800. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Detecting sea-lice outbreaks in a Norwegian salmon farm |
| Industry / Domain | Agriculture / aquaculture |
| Business Problem | A Norwegian salmon farm predicts sea-lice outbreaks in its pens. A missed outbreak costs about €200,000 (fish welfare, lost growth, forced early harvest); an unnecessary preventive treatment costs about €5,000. |
| ML Translation | Target = outbreak in the next two weeks (1) or not (0); binary classification on 400 pen-weeks with 20 outbreaks; cost ratio k = 200,000/5,000 = 40, so the two errors are very unequal. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | G-mean treats a miss and a false alarm symmetrically (both are just one class's recall), so it prefers the model that rarely treats unnecessarily but misses 6 outbreaks; it has no weight to express a 40-to-1 cost ratio. |
| Why other metrics are NOT suitable here | F1 and MCC are symmetric too; accuracy is dominated by outbreak-free pen-weeks; balanced accuracy has the same flaw as G-mean here. |
| Better alternative (if BAD fit) | F-beta with β = √40 = 6.32, or best, expected cost in euros. |
| Business impact of choosing wrong | Selecting by G-mean would deploy X at €1,210,000 instead of Y at €770,000, which is €440,000 more per 20 outbreaks. |
| Small numeric example | X: TP=14, FN=6, FP=2, TN=378 → sensitivity 0.700, specificity 0.995, G-mean = 0.834; Y: TP=19, FN=1, FP=114, TN=266 → sensitivity 0.950, specificity 0.700, G-mean = 0.815; G-mean prefers X; cost X = 6×200,000 + 2×5,000 = €1,210,000; cost Y = 1×200,000 + 114×5,000 = €770,000; Fβ(X) = 41×14/(41×14+40×6+2) = 574/816 = 0.703; Fβ(Y) = 41×19/(41×19+40×1+114) = 779/933 = 0.835 (picks Y). |

**6. Quick decision rule:** Use G-mean when both classes matter, the data is imbalanced and you want to forbid ignoring either class; avoid it when costs are unequal, when false-alarm volume or review capacity is the constraint, or when a class has very few test examples.

### Balanced Accuracy

**1. What it measures (plain English):** Balanced accuracy is the average of the recall on each class; for two classes it is the average of sensitivity and specificity, and it answers what accuracy would be if all classes were equally common. It is also called macro-averaged recall, and a model that predicts one class for everything scores exactly 0.5 in the two-class case.

`Balanced Accuracy = (Sensitivity + Specificity) / 2`

For K classes it is the mean of the K per-class recalls, and scikit-learn's adjusted option rescales chance level to 0.

**2. Intuition:** Judging a school by the average pass rate of each year group rather than by pooled pupils: the tiny sixth-form group counts as much as the huge first year, so nobody can hide.

**3. Benefits:**

- Same idea and scale as accuracy, so it is easy to explain to executives.
- Fixed chance level of 0.5, so a value near 0.5 is an immediate warning.
- Extends naturally to several classes as the mean per-class recall.
- Available in scikit-learn and as a ready-made search score.

**4. Limitations / Potential issues:**

- Ignores precision, so a long list of false alarms can still leave a high score.
- Assumes all classes are equally important, which is itself an assumption.
- Cannot express unequal costs and treats all wrong labels alike, even when classes have an order.
- Depends on the threshold.
- Less standard in leaderboards than F1, so published numbers are harder to compare.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Classifying printed-circuit-board defects at a Slovak electronics plant |
| Industry / Domain | Manufacturing / electronics |
| Business Problem | A Slovak electronics plant classifies defective boards into four types: solder bridge, missing component, tombstoned component and cracked pad. Rare types cause the costliest field failures, so engineers want every type found. |
| ML Translation | Target = defect type (4 classes, multi-class classification); 1,000 defective boards with 700, 200, 80 and 20 per type; the metric is the average of per-class recall. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Balanced accuracy is the mean recall per class, so the 20 cracked pads count as much as the 700 solder bridges; the headline number cannot be flattered by the big classes. |
| Why other metrics are NOT suitable here | Plain accuracy is 0.868 and hides that only 8 of 20 cracked pads are found; weighted F1 is dominated by the large classes; a single precision or recall value cannot summarise four classes. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Reporting accuracy would conceal a 40% recall on the rarest, costliest defect type, which would reach customers. |
| Small numeric example | Recall per class: 630/700 = 0.900, 170/200 = 0.850, 60/80 = 0.750, 8/20 = 0.400; balanced accuracy = (0.900+0.850+0.750+0.400)/4 = 2.900/4 = 0.725; accuracy = (630+170+60+8)/1,000 = 0.868. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Tagging congested cell sites for a UK mobile operator |
| Industry / Domain | Telecom |
| Business Problem | A UK mobile operator tags cell-site hours as congested so planners can order capacity upgrades. Missing congestion hurts customer speeds, and raising needless upgrade tickets wastes engineering effort, so both matter to the planners. |
| ML Translation | Target = site-hour is congested (1) or not (0); binary classification on 5,000 site-hours, 200 congested (4%); balanced accuracy used as the search score (scoring set to balanced accuracy in model selection). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | It is a drop-in, accuracy-like number that cannot be inflated by the 96% uncongested hours, and the 0.5 floor makes an uninformative model obvious. |
| Why other metrics are NOT suitable here | Accuracy gives 0.960 to a model that never tags congestion; F1 ignores the large pool of uncongested hours; G-mean would also work but is harder to explain to planners. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A search tuned for accuracy would select a model that never flags congestion, so planners would miss every upgrade need. |
| Small numeric example | TP=150, FN=50, FP=480, TN=4,320; sensitivity = 150/200 = 0.750; specificity = 4,320/4,800 = 0.900; balanced accuracy = (0.750+0.900)/2 = 0.825; accuracy = 0.894; never-flag model: accuracy 0.960, balanced accuracy = (0+1)/2 = 0.500. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Reporting recycling-bin contamination checks to a Polish city council |
| Industry / Domain | Municipal services |
| Business Problem | A Polish city's waste company uses camera images to detect contaminated recycling bins; the monthly report goes to councillors who know the word accuracy but not F1 or MCC, and contamination is about 6% of bins. |
| ML Translation | Target = bin is contaminated (1) or clean (0); binary classification on 1,000 bins, 60 contaminated; a single headline number is needed for a non-technical audience. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Balanced accuracy can be explained in one sentence (what accuracy would be if clean and contaminated bins were equally common) and has a clear no-skill value of 0.5. |
| Why other metrics are NOT suitable here | Accuracy is 0.941, barely above the 0.940 that a model labelling every bin clean achieves, so it makes the model look useless; MCC is accurate but hard to explain; F1 ignores clean bins and takes longer to introduce. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Showing councillors accuracy alone could make them cancel a useful tool; showing the lazy model's 0.94 beside 0.941 invites the wrong conclusion. |
| Small numeric example | TP=48, FN=12, FP=47, TN=893; sensitivity = 48/60 = 0.800; specificity = 893/940 = 0.950; balanced accuracy = (0.800+0.950)/2 = 0.875; accuracy = 941/1,000 = 0.941 versus 0.940 for the all-clean model whose balanced accuracy is 0.500. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Grading complaint severity for a British online retailer |
| Industry / Domain | Retail / e-commerce |
| Business Problem | A British online retailer grades customer complaints as 1 minor, 2 major or 3 legal threat, so that legal threats reach lawyers quickly. Calling a legal threat minor is far worse than calling a major complaint minor. |
| ML Translation | Target = severity grade (3 ordered classes, ordinal classification); 12 test complaints, 4 per grade; two models. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Balanced accuracy counts every wrong grade the same, so it cannot see that model B makes distant errors (legal threat called minor) while model A only errs by one step. |
| Why other metrics are NOT suitable here | Plain accuracy and macro-F1 have the same blindness to distance; MCC is also unchanged by how far wrong a prediction is. |
| Better alternative (if BAD fit) | Quadratic weighted kappa (QWK), which punishes an error by the square of its distance between grades. |
| Business impact of choosing wrong | Choosing between the models by balanced accuracy (a tie) could deploy model B, which sends legal threats to the slow queue and invites fines or reputational damage. |
| Small numeric example | Model A errors: grade 1 called 2, grade 2 called 3, grade 3 called 2 (each one step off); Model B errors: grade 1 called 3, grade 2 called 1, grade 3 called 1 (two, one and two steps off); both have recall 3/4 per class, so balanced accuracy = 0.750 for both; QWK(A) = 0.800 and QWK(B) = 0.471. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Targeting inspections of unlicensed holiday rentals for a Spanish city council |
| Industry / Domain | Real estate / tourism / government |
| Business Problem | A Spanish city council uses a model to find unlicensed holiday rentals among 50,000 listings; about 500 are unlicensed and inspectors can visit only 300 addresses a month. |
| ML Translation | Target = listing is unlicensed (1) or licensed (0); binary classification at 1% prevalence; the council wants to know how useful the model's list will be to inspectors. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Balanced accuracy uses specificity, whose denominator is the huge licensed class, so 2,475 false alarms still give a specificity of 0.95; the score looks excellent while most flagged listings are innocent. |
| Why other metrics are NOT suitable here | Accuracy (0.950) and G-mean (0.925) share the same blind spot; ROC-AUC is also flattered by the large licensed class; F2 would reward an even longer list of alerts. |
| Better alternative (if BAD fit) | Precision at k with k = 300 inspections, and PR-AUC (area under the precision-recall curve), which see the false-alarm volume. |
| Business impact of choosing wrong | Inspectors would visit mostly licensed hosts, wasting limited visits, damaging trust in the council and leaving most unlicensed listings untouched. |
| Small numeric example | TP=450, FN=50, FP=2,475, TN=47,025; sensitivity = 450/500 = 0.900; specificity = 47,025/49,500 = 0.950; balanced accuracy = 0.925; precision = 450/2,925 = 0.154, so about 85% of flagged listings are licensed; if the best 300 contain 120 truly unlicensed listings, precision at 300 = 120/300 = 0.400 and recall at 300 = 120/500 = 0.240. |

**6. Quick decision rule:** Use balanced accuracy when you need an honest, accuracy-like headline for imbalanced data and each class deserves equal weight; avoid it when false-alarm volume, unequal costs or distances between ordered classes matter.

### Matthews Correlation Coefficient (MCC)

**1. What it measures (plain English):** MCC is the correlation between the true labels and the predicted labels, treated as two yes or no variables; it is also known as the phi coefficient. It runs from -1 (perfectly inverted) through 0 (no skill) to +1 (perfect), and it scores any all-one-class model as 0.

`MCC = (TP×TN − FP×FN) / √((TP+FP)×(TP+FN)×(TN+FP)×(TN+FN))`

**2. Intuition:** Two weather forecasters are judged by how well their forecasts move together with the real weather; a forecaster who says dry every day in a dry country never moves with the weather, so scores 0 however often they are right.

**3. Benefits:**

- Uses all four cells, so it has no blind spot for true negatives or the majority class.
- Symmetric: swapping which class is positive changes nothing, so two teams with different label conventions agree.
- Gives exactly 0 to degenerate models on imbalanced data, which makes it hard to game.
- Easy to read as a correlation, with a meaningful negative range, and available for several classes in scikit-learn.

**4. Limitations / Potential issues:**

- Less familiar to managers and needs explaining.
- Cannot tell which kind of error is the problem, so always show the confusion matrix next to it.
- Treats a false alarm and a miss as equally bad, so it is wrong when costs are very unequal.
- Depends on the threshold and needs hard labels, not probabilities.
- Noisy on small test sets, and a single value is not a plain-language answer for non-technical readers.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Calling pathogenic variants in a UK genomics lab |
| Industry / Domain | Healthcare / biotech |
| Business Problem | A UK genomics lab uses a model to call pathogenic gene variants among 20,000 candidates; only 100 are truly pathogenic. A clinical geneticist wants one number that cannot be flattered by the sea of harmless variants. |
| ML Translation | Target = variant is pathogenic (1) or not (0); binary classification at 0.5% prevalence; hard calls at one threshold. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | MCC uses all four cells, scores any all-one-class model as exactly 0, and was adopted in bioinformatics for just this kind of rare-positive problem. |
| Why other metrics are NOT suitable here | Accuracy is 0.996 while calling nothing already gets 0.995; F1 ignores the 19,840 correct benign calls; balanced accuracy and G-mean ignore how many benign variants are wrongly called pathogenic. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Reporting accuracy would let a model that finds no pathogenic variants look near perfect, leading to missed diagnoses. |
| Small numeric example | TP=70, FP=60, FN=30, TN=19,840; MCC = (70×19,840 - 60×30)/√(130×100×19,900×19,870) = 1,387,000/2,267,238.2 = 0.612; call-nothing model: accuracy 0.995, MCC = 0. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Two analytics teams scoring a returns model at a German fashion retailer |
| Industry / Domain | E-commerce |
| Business Problem | A German fashion retailer predicts which orders will be returned. The logistics team calls returned the positive class, the finance team calls kept the positive class; both report the same model but quote different F1 scores and argue. |
| ML Translation | Target = order returned (1) or kept (0); binary classification on 500 orders, 80 returned; the same predictions, only the label convention differs. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | MCC is symmetric: swapping which class is called positive does not change it, so both teams quote the same number and the argument disappears. |
| Why other metrics are NOT suitable here | F1 changes with the convention (returned: 0.667, kept: 0.927); precision and recall also swap meaning; accuracy ignores the imbalance. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Different headline numbers for the same model cause wasted meetings and a risk that the weaker-looking figure kills a good project. |
| Small numeric example | TP=60, FP=40, FN=20, TN=380 (returned positive); F1 = 2×60/(2×60+40+20) = 0.667; swapping labels gives TP=380, FP=20, FN=40, TN=60 and F1 = 2×380/(2×380+20+40) = 0.927; MCC = (60×380 - 40×20)/√(100×80×420×400) = 22,000/36,660.6 = 0.600; MCC (labels swapped) = (380×60 - 20×40)/√(400×420×80×100) = 22,000/36,660.6 = 0.600. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Tuning a wafer-defect classifier at a German chip fab |
| Industry / Domain | Manufacturing / semiconductors |
| Business Problem | A German chip fab tunes the settings of a model that flags defective wafers (4% defective); the automatic search will pick whichever setting scores best on the chosen metric. |
| ML Translation | Target = wafer defective (1) or good (0); binary classification on 1,000 wafers, 40 defective; three candidate settings scored by the search. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | MCC is a safe default for automated model search on an imbalanced binary problem: the flag-nothing setting scores 0, so the search cannot settle on it. |
| Why other metrics are NOT suitable here | Accuracy would pick C1 (flag nothing, 0.960); F1 ignores correct good-wafer calls; balanced accuracy would prefer the over-flagging C3 and ignores false-alarm volume. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A search tuned on accuracy would ship the setting that flags no defect, so all 40 defects per 1,000 wafers would move on to costly later process steps. |
| Small numeric example | C1 (flag nothing): TP=0, FP=0, FN=40, TN=960, accuracy = 0.960, MCC = 0.000; C2: TP=28, FP=30, FN=12, TN=930, accuracy = 0.958, MCC = 0.561; C3: TP=36, FP=150, FN=4, TN=810, accuracy = 0.846, MCC = 0.375; for C2, MCC = (28×930 - 30×12)/√(58×40×960×942) = 25,680/45,804.2 = 0.561; accuracy picks C1, MCC picks C2. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Flagging cracked rail segments on a freight line |
| Industry / Domain | Transport and rail infrastructure |
| Business Problem | A German freight-rail operator scans 10,000 track segments with an ultrasonic sensor and a model decides which to send for a manual check. A missed crack can lead to a derailment costing about €2,000,000; an unnecessary check costs about €400 in crew time and a short speed restriction. |
| ML Translation | Target = segment has a crack (1) or not (0); binary classification, 20 cracked segments in 10,000; cost ratio about 5,000 to 1. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MCC weighs a miss and a false alarm equally, so it prefers the model that has few false alarms but misses half of the cracks; with a cost ratio this extreme the right model is the high-recall one. |
| Why other metrics are NOT suitable here | Accuracy is above 0.99 for both models; F1 is symmetric as well; balanced accuracy also treats the two error types equally. |
| Better alternative (if BAD fit) | F-beta with a large β (about 71, the square root of the 5,000 cost ratio) or, best, expected cost in euros. |
| Business impact of choosing wrong | Choosing model A on MCC would cost €20,000,800 instead of €2,024,000, which is €17,976,800 more per 10,000 segments, in derailment and repair risk. |
| Small numeric example | A: TP=10, FP=2, FN=10, TN=9,978; B: TP=19, FP=60, FN=1, TN=9,920; MCC(A) = (10×9,978 - 2×10)/√(12×20×9,980×9,988) = 99,760/154,671.5 = 0.645; MCC(B) = (19×9,920 - 60×1)/√(79×20×9,980×9,921) = 188,420/395,522.8 = 0.476 (MCC prefers A); cost A = 10×2,000,000 + 2×400 = €20,000,800; cost B = 1×2,000,000 + 60×400 = €2,024,000. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Targeting damp-and-mould inspections for a London borough's housing team |
| Industry / Domain | Real estate / social housing |
| Business Problem | A London borough's housing managers use a model to choose which of 400 council flats to inspect for serious damp. They are not technical and ask: how many of the flats we visit really have a problem, and how many problem flats do we miss? |
| ML Translation | Target = flat has serious damp (1) or not (0); binary classification on 400 flats, 50 with serious damp (12.5%); hard flags at one threshold. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MCC is a sound technical summary but a single correlation value is not a plain-language answer; the managers' questions are exactly precision and recall. |
| Why other metrics are NOT suitable here | Accuracy (0.930) hides the missed flats; F1 mixes both answers into one number; balanced accuracy still does not say how many visits are wasted. |
| Better alternative (if BAD fit) | Precision and recall stated in plain words, with MCC kept as a technical backup. |
| Business impact of choosing wrong | A manager shown only MCC = 0.68 cannot plan inspector visits or explain the programme to councillors, and may reject a useful tool or approve it without understanding its limits. |
| Small numeric example | TP=36, FP=14, FN=14, TN=336; MCC = (36×336 - 14×14)/√(50×50×350×350) = 11,900/17,500.0 = 0.680; precision = 36/50 = 0.720 (of 50 flats visited, 36 truly have damp); recall = 36/50 = 0.720 (36 of 50 damp flats are found, 14 are missed). |

**6. Quick decision rule:** Use MCC when you want one honest, label-convention-free number for an imbalanced binary problem; avoid it when costs are strongly unequal, when you need threshold-free comparison, or when you must speak to a non-technical audience in plain terms.

## Chance-corrected agreement scores

### Cohen's Kappa

**1. What it measures (plain English):** Cohen's kappa (κ) measures agreement between two raters, or between a model and the truth, after removing the agreement that would happen by chance. It is also called the kappa statistic; 0 means no better than chance and 1 means perfect agreement.

`κ = (p_o − p_e) / (1 − p_e)`

Here `p_o` is the observed agreement (the accuracy) and `p_e` is the agreement expected by chance, calculated from each rater's own yes and no rates.

**2. Intuition:** In a true or false quiz a guesser gets about half right; kappa gives credit only for marks above what random guessing would earn, scaled by the room left above that guessing level.

**3. Benefits:**

- Chance-corrected, so it takes away the free credit that imbalance gives to accuracy.
- Standard way to check whether human labels are reliable and what ceiling a model can reach.
- Extends to several classes and, with weights, to ordered classes.
- Lets you compare a model with human experts on the same scale.

**4. Limitations / Potential issues:**

- Depends on how common each class is, so the same model quality gives different kappa in different datasets (the kappa paradox).
- Can be low despite high accuracy when the classes are very uneven.
- Unweighted kappa ignores the order of ordered classes, so use weighted kappa for ratings and grades.
- Needs hard labels, cannot express unequal costs, and the Landis and Koch bands are conventions rather than laws.
- Less intuitive for business readers than precision and recall.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Checking label reliability between two contract annotators at a Dutch legal-tech company |
| Industry / Domain | Professional services / legal |
| Business Problem | A Dutch legal-tech company has two annotators label 200 contracts for the presence of a change-of-control clause. Before paying for a model, the product owner asks whether the human labels are reliable enough to learn from. |
| ML Translation | Not a model score at all: two human raters give yes or no labels; Cohen's kappa measures agreement beyond chance (p_o is the observed agreement, p_e the agreement expected by chance from each rater's yes-rate). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Kappa removes the agreement the two raters would reach by luck alone, which matters because both say no to most contracts; it also tells the team how good a model could possibly be (about as good as the humans agree with each other). |
| Why other metrics are NOT suitable here | Raw agreement (0.880) is inflated by the many no-no pairs; F1 needs one rater to be treated as truth, which is not the case here; accuracy suffers from the same chance-agreement inflation. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using raw agreement could lead the team to trust unreliable labels and train a model on noise, wasting a modelling budget. |
| Small numeric example | Both yes = 30, rater 1 yes and rater 2 no = 10, rater 1 no and rater 2 yes = 14, both no = 146 (N=200); p_o = (30+146)/200 = 0.880; p_e = 0.200×0.220 + 0.800×0.780 = 0.044 + 0.624 = 0.668; κ = (0.880 - 0.668)/(1 - 0.668) = 0.212/0.332 = 0.639; reading: substantial agreement (0.61 to 0.80 band), so the labels are usable. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Comparing a skin-image model with two dermatologists at a Danish hospital |
| Industry / Domain | Healthcare |
| Business Problem | A Danish hospital tests a model that marks skin-lesion images as urgent or routine referral. The clinical board wants to know whether the model agrees with the expert consensus as well as two dermatologists agree with each other. |
| ML Translation | Target = urgent (1) or routine (0) on 100 images; two comparisons: dermatologist 1 against dermatologist 2, and the model against the consensus label. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Kappa puts human-versus-human and model-versus-expert agreement on the same chance-corrected scale, so the board can say the model performs at human level; the human kappa is also the realistic ceiling. |
| Why other metrics are NOT suitable here | F1 and accuracy cannot be computed for human-versus-human because neither dermatologist is the truth; MCC would work but kappa is the language of the clinical reliability literature; ROC-AUC ignores the operating decision. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Without a human benchmark the board might demand impossible performance, rejecting a model that is as consistent as the experts, or accept a weak one on the strength of a high accuracy. |
| Small numeric example | Humans: both urgent 20, 8, 7, both routine 65 → p_o = (20+65)/100 = 0.850; p_e = 0.280×0.270 + 0.720×0.730 = 0.076 + 0.526 = 0.601; κ = (0.850 - 0.601)/(1 - 0.601) = 0.249/0.399 = 0.624. Model against consensus: TP=19, FP=9, FN=6, TN=66 → p_o = (19+66)/100 = 0.850; p_e = 0.280×0.250 + 0.720×0.750 = 0.070 + 0.540 = 0.610; κ = (0.850 - 0.610)/(1 - 0.610) = 0.240/0.390 = 0.615. The two kappas are within 0.01, so the model performs at about expert level. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Triaging customs declarations by goods type at a European port |
| Industry / Domain | Logistics / customs |
| Business Problem | A European port customs office uses a model to assign declarations to a goods group (food, electronics, textiles) so that the right inspection team receives each one; 70% of declarations are food. |
| ML Translation | Target = goods group (3 unordered classes, multi-class classification); 100 declarations with 70 food, 20 electronics, 10 textiles; model prediction compared with the officer's final label. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Kappa generalises to several classes and removes the free credit a model gets for always guessing the big class; it is a single honest agreement score between model and officer. |
| Why other metrics are NOT suitable here | Accuracy is 0.840 but a model that always says food already gets 0.700; F1 needs a per-class average and choices about weighting; MCC works but kappa is the familiar agreement measure for officers and auditors. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Reporting accuracy would overstate skill, because 0.70 of it comes free from always guessing food, and could hide that the small electronics and textiles groups are routed badly. |
| Small numeric example | Correct counts 62+15+7 = 84 of 100, p_o = 0.840; row totals 70, 20, 10 and column totals 66, 22, 12; p_e = 0.70×0.66 + 0.20×0.22 + 0.10×0.12 = 0.462 + 0.044 + 0.012 = 0.518; κ = (0.840 - 0.518)/(1 - 0.518) = 0.322/0.482 = 0.668; always-food model: p_o = 0.700, p_e = 0.700, κ = 0. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Grading roof damage for a Danish home insurer |
| Industry / Domain | Insurance |
| Business Problem | A Danish home insurer grades storm-damaged roofs from 1 (minor) to 4 (total) to decide the repair budget. Calling a total loss grade 1 is far worse than calling a grade 3 as grade 4. |
| ML Translation | Target = damage grade (4 ordered classes, ordinal classification); 16 test claims, 4 per grade; two models with the same number of correct grades. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Plain kappa counts all disagreements equally, so it gives the same score to a model that is always one grade off and to one that sometimes swaps the extremes. |
| Why other metrics are NOT suitable here | Accuracy and MCC share the same blindness to distance; macro-F1 does too; linear weighted kappa is better but punishes big errors less sharply than quadratic. |
| Better alternative (if BAD fit) | Quadratic weighted kappa (QWK), which punishes an error by the square of the grade distance. |
| Business impact of choosing wrong | Choosing between the models on plain kappa (a tie) could deploy model B, which would sometimes pay a total-loss claim as minor damage or reserve a total-loss budget for a minor claim. |
| Small numeric example | Model A: 4 errors, each one grade off; Model B: grade 1 called 4, grade 2 called 3, grade 3 called 2, grade 4 called 1 (distances 3, 1, 1, 3); accuracy 12/16 = 0.750 for both; p_e = 4×(0.25×0.25) = 0.250; kappa = (0.750 - 0.250)/(1 - 0.250) = 0.667 for both; QWK(A) = 0.900, QWK(B) = 0.500. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Comparing a shelf-gap model across stores in Germany and Poland |
| Industry / Domain | Retail |
| Business Problem | A European grocery chain compares one shelf-gap (out-of-stock) detection model across stores. Store X in Germany has gaps on half of its checked shelf slots; store Y in Poland has gaps on only 5%, and the head office wants to rank stores by model quality. |
| ML Translation | Target = shelf slot is out of stock (1) or not (0); binary classification; same model, sensitivity 0.900 and specificity 0.900 in both stores; 100 slots checked in store X and 200 in store Y. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Kappa depends on how common the positive class is, so the same model quality gives very different kappa values in stores with different out-of-stock rates; kappa measures the model together with the store's prevalence. |
| Why other metrics are NOT suitable here | Accuracy is identical (0.900) and hides the issue; MCC is also affected by prevalence; F1 and precision change strongly with prevalence as well. |
| Better alternative (if BAD fit) | Sensitivity and specificity per store (they do not depend on prevalence), shown beside each store's out-of-stock rate. |
| Business impact of choosing wrong | Head office would conclude that the model is far worse in Poland and could cut investment there, even though the model performs the same in both stores. |
| Small numeric example | Store X: TP=45, FP=5, FN=5, TN=45; p_o = (45+45)/100 = 0.900; p_e = 0.500×0.500 + 0.500×0.500 = 0.250 + 0.250 = 0.500; κ = (0.900 - 0.500)/(1 - 0.500) = 0.400/0.500 = 0.800. Store Y: TP=9, FP=19, FN=1, TN=171; p_o = (9+171)/200 = 0.900; p_e = 0.140×0.050 + 0.860×0.950 = 0.007 + 0.817 = 0.824; κ = (0.900 - 0.824)/(1 - 0.824) = 0.076/0.176 = 0.432. Both have accuracy 0.900 and sensitivity and specificity of 0.900, yet kappa is 0.800 against 0.432. |

**6. Quick decision rule:** Use Cohen's kappa for inter-rater reliability, model-versus-expert agreement and chance-corrected scoring of nominal classes; avoid it when classes are ordered, when you compare datasets with different class rates, or when costs are unequal.

### Quadratic Weighted Kappa (QWK) [Added – not in source file]

**1. What it measures (plain English):** QWK is Cohen's kappa for ordered classes such as 1 to 5 ratings, grades or severity levels: it punishes a disagreement by the square of how far apart the two grades are, so being three grades off is nine times worse than being one grade off. It is also called quadratic kappa or kappa with quadratic weights, and it is chance-corrected like ordinary kappa.

`κ_w = 1 − Σ(w_ij × O_ij) / Σ(w_ij × E_ij)`

Here k is the number of grades, `w_ij = (i − j)² / (k − 1)²` is the penalty for true grade i and predicted grade j, `O_ij` is the number of items observed in that cell, and `E_ij = (row total i × column total j) / N` is the number expected by chance; for 4 grades the weights for a distance of 0, 1, 2 and 3 grades are 0, 1/9, 4/9 and 1.

**2. Intuition:** A diving judge's score: being one point off the panel is forgivable, being five points off is a scandal, and a judge who just copies the most common score does not get credit for agreeing with the crowd.

**3. Benefits:**

- Gives partial credit for near misses and heavy penalties for big misses, which is how ratings and grades are judged.
- Chance-corrected, so lazy guessing of the common grade earns nothing.
- Available in scikit-learn with the quadratic weights option, and the standard score in essay-marking and retinopathy-grading competitions.
- Values near 1 mean strong agreement with the reference grades, and near 0 mean agreement no better than chance.

**4. Limitations / Potential issues:**

- Only meaningful when the classes have a real order and roughly equal gaps; for unordered classes the numbering changes the score.
- Symmetric: it cannot show that under-grading is worse than over-grading.
- Depends on how common each grade is, so it is not comparable across datasets with different grade mixes.
- Squaring makes it dominated by a few large misses and noisy on small samples.
- Needs hard grades, and is harder to explain to managers than accuracy.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Scoring short exam answers 0 to 3 for a UK exam board |
| Industry / Domain | Education |
| Business Problem | A UK exam board wants a model to mark short written answers on a 0 to 3 scale, to be checked against the grades given by senior examiners; being one mark away is acceptable, being three marks away is not. |
| ML Translation | Target = mark 0, 1, 2 or 3 (4 ordered classes, ordinal classification); 12 test answers; examiner mark compared with model mark using quadratic weights w = (distance)² / 9. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | QWK gives partial credit for near misses and heavy penalties for large misses, which matches how an exam board judges marking quality, and it is chance-corrected. |
| Why other metrics are NOT suitable here | Accuracy (0.667) gives a one-mark miss the same penalty as a three-mark miss; plain kappa (0.538) also ignores distance; mean absolute error does not correct for chance agreement. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using accuracy would treat a model that marks a 3 as 0 as no worse than one that marks a 3 as 2, putting unfair marks in front of students. |
| Small numeric example | 4 of 12 answers differ, each by exactly one mark; observed weighted disagreement = 4 × (1/9) = 0.444; expected disagreement by chance (from the marginals) = 2.519; QWK = 1 - 0.444/2.519 = 0.824; accuracy = 0.667; plain kappa = 0.538. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Matching internal credit grades for small firms at a French bank |
| Industry / Domain | Banking |
| Business Problem | A French bank wants a model to assign small-business customers an internal credit grade from 1 (safest) to 5 (riskiest), in line with the grade set by its credit committee. Capital and pricing depend on the grade, so being two grades off is much more costly than one. |
| ML Translation | Target = grade 1 to 5 (5 ordered classes, ordinal classification); 10 test firms; weights w = (distance)² / 16; two models with the same accuracy. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | QWK separates a model whose misses are near the committee's grade from one with large misses, and its quadratic weights match how pricing and capital errors grow with grade distance. |
| Why other metrics are NOT suitable here | Accuracy gives both models 0.700; plain kappa ignores distance; macro-F1 ignores order; mean absolute error ignores chance agreement and cannot be compared across grade distributions. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using accuracy would not distinguish a model that is one grade off from a model that mis-prices by two grades, which means loans priced and capitalised wrongly. |
| Small numeric example | Model A: 3 errors, each one grade off, sum of squared distances = 3, observed = 3/16 = 0.188, expected = 2.062, QWK = 0.909; Model B: 3 errors, each two grades off, sum of squared distances = 12, observed = 12/16 = 0.750, expected = 1.600, QWK = 0.531; accuracy is 0.700 for both. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Grading diabetic eye disease from retina photos at a German hospital |
| Industry / Domain | Healthcare |
| Business Problem | A German hospital wants a model to grade retina photographs from 0 (no disease) to 4 (proliferative disease) as the ophthalmologists do. Missing sight-threatening disease by calling grade 4 as grade 0 is much worse than calling grade 1 as grade 2. |
| ML Translation | Target = grade 0 to 4 (5 ordered classes, ordinal classification); 10 test photos; weights w = (distance)² / 16; two models each with 7 of 10 grades correct. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A big miss such as 4 called 0 is punished 16 times as hard as a one-grade miss, so QWK reflects the clinical risk, and it is the established metric for this grading task. |
| Why other metrics are NOT suitable here | Accuracy cannot tell the two models apart (0.700 each); plain kappa treats all errors alike; macro-F1 ignores the ordering of grades. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Choosing on accuracy could deploy a model that sends a patient with severe disease home as healthy, risking blindness and legal liability. |
| Small numeric example | Model A: 3 errors, each one grade off, sum of squared distances = 3, observed = 3/16 = 0.188, expected = 2.388, QWK = 0.921; Model B: errors of one, one and four grades (grade 4 called 0), sum of squared distances = 18, observed = 18/16 = 1.125, expected = 1.950, QWK = 0.423. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Classifying parcel damage types at a Belgian logistics hub |
| Industry / Domain | Logistics |
| Business Problem | A Belgian parcel hub classifies damaged parcels as crushed, wet, torn or missing label, to send each to the right claims team. The four types have no natural order; the numbers 1 to 4 are just codes in the database. |
| ML Translation | Target = damage type (4 unordered classes, nominal multi-class classification); 12 test parcels; the same predictions scored under two different code assignments. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | QWK assumes that code 1 is closer to code 2 than to code 4; with unordered classes this invents distances, so the score depends on an arbitrary numbering of the types. |
| Why other metrics are NOT suitable here | Accuracy is unaffected but ignores chance agreement; macro-F1 is unaffected by coding but ignores chance; MCC also works for several classes and does not depend on codes. |
| Better alternative (if BAD fit) | Plain (unweighted) Cohen's kappa, or multi-class MCC, which give the same value under any coding. |
| Business impact of choosing wrong | A team could pick the model that happens to score better under the current database coding, then lose that advantage when the codes are renumbered. |
| Small numeric example | Coding 1: crushed=1, wet=2, torn=3, missing label=4 gives QWK = 0.619; coding 2: crushed=1, torn=2, label=3, wet=4 gives QWK = 0.903 on exactly the same predictions; plain kappa is 0.664 under both codings. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Grading fire risk in residential tower blocks for a UK housing association |
| Industry / Domain | Real estate / housing safety |
| Business Problem | A UK housing association uses a model to grade tower blocks from 1 (lowest) to 5 (highest) fire risk to schedule remedial work. Under-grading a block delays fixes and costs about €12,000 per grade of exposure; over-grading triggers an unneeded survey of about €1,500 per grade. |
| ML Translation | Target = fire-risk grade 1 to 5 (5 ordered classes, ordinal classification); 10 test blocks; weights w = (distance)² / 16; the model U only under-grades and the model O only over-grades, with mirror-image errors. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | QWK is symmetric: a block graded two grades too low counts the same as one graded two grades too high, so it cannot reflect that under-grading is eight times costlier. |
| Why other metrics are NOT suitable here | Accuracy (0.700 each) and plain kappa are symmetric as well; macro-F1 ignores order; mean absolute error is symmetric and ignores chance agreement. |
| Better alternative (if BAD fit) | A cost-weighted score using an asymmetric cost matrix in euros (or recall on the highest grades), with QWK as a secondary check. |
| Business impact of choosing wrong | Choosing between U and O on QWK (a tie) could select U, which would cost €48,000 instead of €6,000, which is €42,000 more per 10 blocks and leaves blocks under-protected. |
| Small numeric example | Model U: 3 errors (one, two, one grade too low), total 4 grades under; Model O: 3 errors (two, one, one grade too high), total 4 grades over; QWK(U) = 1 - 0.375/0.750 = 0.500; QWK(O) = 1 - 0.375/0.750 = 0.500; cost U = 4×12,000 = €48,000; cost O = 4×1,500 = €6,000. |

**6. Quick decision rule:** Use QWK when the target is an ordered grade, rating or severity level and bigger misses should hurt more; avoid it when classes have no order, when under-grading and over-grading cost different amounts, or when the problem is plain two-class detection.
