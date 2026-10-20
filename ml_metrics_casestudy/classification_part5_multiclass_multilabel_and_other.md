# Classification Case Studies, Part 5: Multi-Class, Multi-Label and Other Metrics

## Table of Contents

- [Averaging Methods for Multi-Class Problems](#averaging-methods-for-multi-class-problems)
  - [Macro Average](#macro-average)
  - [Micro Average](#micro-average)
  - [Weighted Average](#weighted-average)
- [Multi-Label Metrics](#multi-label-metrics)
  - [Hamming Loss](#hamming-loss)
  - [Jaccard Score (also called Jaccard Index or IoU)](#jaccard-score-also-called-jaccard-index-or-iou)
  - [Subset Accuracy (exact match ratio)](#subset-accuracy-exact-match-ratio)
- [Threshold, Odds and Overlap Metrics](#threshold-odds-and-overlap-metrics)
  - [Youden's J Statistic](#youdens-j-statistic)
  - [Diagnostic Odds Ratio (DOR)](#diagnostic-odds-ratio-dor)
  - [Dice Coefficient (Sørensen-Dice)](#dice-coefficient-sørensen-dice)
- [Ranking-Style Multi-Class Metrics](#ranking-style-multi-class-metrics)
  - [Top-K Accuracy [Added – not in source file]](#top-k-accuracy-added--not-in-source-file)

How to read this part: each metric has a plain-English definition, a real-life analogy, benefits, limitations and five case tables (a mix of GOOD and BAD fits), followed by a one-line decision rule. Throughout, precision means "of the cases the model flagged, how many were right", recall (also called sensitivity) means "of the real cases, how many the model found", and F1 is the balance of the two. All numbers in the case tables are small toy examples, so you can check the arithmetic by hand.

## Averaging Methods for Multi-Class Problems

### Macro Average

**1. What it measures (plain English):** When a model sorts items into several classes (for example three triage levels), you get one precision, recall or F1 score per class. The macro average takes the plain, unweighted mean of those per-class scores, so every class gets one equal vote no matter how many examples it has. It is also called macro-averaging, and macro-F1 is its most common form.

`Macro-F1 = (1/K) × Σ F1ₖ` where K is the number of classes and F1ₖ is the F1 of class k.

**2. Intuition:** A head teacher reports the average mark of each subject, not of each pupil. The tiny art class counts exactly as much as the huge maths class, so nobody can hide a weak subject behind a big one.

**3. Benefits:**

- Gives rare classes the same weight as common ones, so a model cannot look good by ignoring them.
- Exposes uneven performance that plain accuracy hides.
- Easy to explain: "the average performance of a typical class".
- Works well for fairness audits, where each group (not each person) should count equally.

**4. Limitations / Potential issues:**

- Unstable when some classes are tiny: a class with 2 test examples carries the same vote as a class with 2,000, so one lucky or unlucky example moves the headline.
- Over-weights classes that do not matter to the business (for example a junk "other" bucket).
- Does not reflect the total number of errors the business actually pays for.
- A single mean hides the spread, so always print the per-class table beside it.
- Macro-F1 is the mean of the per-class F1 values, not the F1 of the macro precision and macro recall; mixing the two gives slightly different numbers.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — The nurse line that almost never spots an emergency |
| Industry / Domain | Healthcare |
| Business Problem | A telehealth nurse line serving rural Kenya sorts each caller's symptom notes into Self-care, Clinic visit or Emergency referral. Emergencies are only 5 in every 100 calls, but a missed one can be fatal. |
| ML Translation | Target = triage level (3 classes, one label per call); multi-class classification; imbalanced data (imbalanced = some classes are far rarer than others), split 80 / 15 / 5; the rarest class is the highest-stakes one. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Macro gives the 5 emergency calls the same vote as the 80 self-care calls, so a model that quietly ignores emergencies cannot hide behind the easy majority. |
| Why other metrics are NOT suitable here | Accuracy rewards the 80 easy self-care calls and hides weak emergency detection; micro-F1 equals accuracy in a one-label-per-item problem, so it has the same blind spot; weighted-F1 gives emergencies only 5% of the weight, so it still dilutes them. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Reporting accuracy would show a comfortable 87% and a green light while 4 of every 5 emergencies are sent home or to a clinic; the cost is delayed care, deaths and liability for the service. |
| Small numeric example | 100 calls. Self-care: 76 of 80 found, precision 76/83 = 0.916, recall 0.95, F1 0.9325. Clinic: 10 of 15, precision 10/15 = 0.667, recall 0.667, F1 0.667. Emergency: 1 of 5, precision 1/2 = 0.5, recall 0.2, F1 0.2857. Accuracy = (76+10+1)/100 = 0.87; weighted-F1 = 0.860; macro-F1 = (0.9325+0.6667+0.2857)/3 = 0.628; macro-recall = (0.95+0.667+0.2)/3 = 0.606. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Haul-road cameras and the rare person in the danger zone |
| Industry / Domain | Mining safety |
| Business Problem | A Western Australian iron-ore site uses haul-road cameras whose software labels each alert as Missing hard-hat (60 alerts), Vehicle too close (30) or Person in exclusion zone (10). The safety manager wants one number to decide whether human spotters can be reduced. |
| ML Translation | Target = alert type (3 classes); multi-class classification; skewed class sizes where the rarest class (person in exclusion zone) is the most dangerous. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Macro-F1 puts the weakest class, with F1 of only 0.57, in plain view instead of letting the 60 easy hard-hat alerts bury it. |
| Why other metrics are NOT suitable here | Accuracy (0.84) and weighted-F1 (0.84) are dominated by hard-hat alerts; micro-F1 is identical to accuracy here; a single overall recall would not show which alert type is failing. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Trusting 0.84 could lead to spotters being removed while 4 in 10 people-in-zone events are mislabelled; the cost is a possible fatality, a regulator shutdown and weeks of lost haulage. |
| Small numeric example | Rows = actual, columns = predicted. Hard-hat 60: 54, 4, 2; Vehicle 30: 3, 24, 3; Zone 10: 1, 3, 6. Per-class F1 = 0.9153, 0.7869, 0.5714. Macro-F1 = (0.9153+0.7869+0.5714)/3 = 2.2736/3 = 0.758; accuracy = 84/100 = 0.84; zone recall = 6/10 = 0.60. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — A loan model that works for Spanish speakers and less for everyone else |
| Industry / Domain | Banking |
| Business Problem | A mid-size Peruvian lender wants to audit whether its approval model finds creditworthy applicants equally well across three language groups: Spanish, Quechua and Aymara speakers. Regulators ask for one fairness number. |
| ML Translation | Target = approve / decline; binary classifier evaluated per group; the metric is recall (share of creditworthy applicants approved) for each group, then averaged across groups; group sizes are very unequal. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Averaging per-group recall with equal weights makes a small group count as much as the large one, which is exactly the fairness question being asked. |
| Why other metrics are NOT suitable here | Overall (pooled) recall is dominated by the largest group and hides gaps; accuracy ignores which applicants are wrongly declined; weighted averaging by group size would repeat the same dominance. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A pooled number of 0.85 would pass the audit while Aymara speakers get recall of only 0.50; the cost is regulator action, reputational damage and lending income lost from good borrowers who were turned away. |
| Small numeric example | Creditworthy applicants approved: Spanish 720 of 800 = 0.90; Quechua 105 of 150 = 0.70; Aymara 25 of 50 = 0.50. Pooled recall = 850/1000 = 0.85; macro-recall = (0.90+0.70+0.50)/3 = 0.70. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — The 400-code tariff classifier and the two-parcel class |
| Industry / Domain | Logistics (customs) |
| Business Problem | A Gulf-state customs authority's model assigns each declared parcel to one of 400 tariff headings. About 150 headings have fewer than 5 parcels in the test set, and management wants a single score each month. |
| ML Translation | Target = tariff heading (400 classes); multi-class classification with a long tail (a few huge classes, many tiny ones); very small support in many classes. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Each tiny class carries a full 1/400 vote, and its F1 jumps wildly with one parcel, so the headline moves with luck rather than with model quality. |
| Why other metrics are NOT suitable here | Plain accuracy ignores the tail entirely; per-class recall for a 2-parcel class is just as noisy; micro-F1 is again accuracy in disguise. |
| Better alternative (if BAD fit) | Macro-F1 computed only over classes with a stated minimum support (say at least 30 test parcels), plus head / middle / tail bucket reporting, and weighted-F1 for the overall headline; this keeps rare classes visible without letting noise drive the number. |
| Business impact of choosing wrong | The team wastes weeks chasing score swings that are pure noise, or wrongly declares the model failed or passed, delaying parcel clearance and risking duty leakage. |
| Small numeric example | Toy version with 5 classes: four classes of 250 parcels each with F1 = 0.90, and one tiny class of 2 parcels. If the tiny class finds 1 of 2 with no false alarms, F1 = 0.667 and macro-F1 = (4×0.90+0.667)/5 = 0.853. If it finds both, F1 = 1.0 and macro-F1 = (3.6+1.0)/5 = 0.920. One parcel moves macro-F1 by 0.067. Weighted-F1 over 1,002 parcels moves only from 0.8995 to 0.9002. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — The municipal request router where every misroute costs the same |
| Industry / Domain | Public services |
| Business Problem | A Colombian city council routes citizen requests to four departments: Permits (600 per month), Utilities billing (300), Noise (80) and Rare special cases (20). Every misrouted request costs about COP 12,000 in rework, whatever the department. |
| ML Translation | Target = department (4 classes, one label per request); multi-class classification; imbalanced; cost per error is flat across classes. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Macro-F1 values one fix in the tiny class far more than one fix in a big class, although both save exactly the same money, so it points the team at the wrong priorities. |
| Why other metrics are NOT suitable here | Per-class recall alone gives four numbers and no total; weighted-F1 is close but adds a needless averaging step; macro-precision ignores the cost of missed requests. |
| Better alternative (if BAD fit) | Micro-average (which equals accuracy for one label per item), reported with the total misroute count and money cost, because cost per error is flat; keep the per-class table only for diagnosis. |
| Business impact of choosing wrong | Months of effort could go into the rarest class because macro-F1 rewards it, while the cheaper bulk of errors in Permits and Utilities stays untouched; the rework bill barely moves. |
| Small numeric example | Base: 64 misroutes (accuracy 0.936) costing 64 × 12,000 = COP 768,000; macro-F1 0.781. Fix 6 errors in the rare class: 58 misroutes, accuracy 0.942, macro-F1 0.836 (up 0.055). Fix 6 errors in Permits instead: 58 misroutes, accuracy 0.942, macro-F1 0.789 (up 0.008). Both fixes save 6 × 12,000 = COP 72,000, yet macro-F1 rates them very differently. |

**6. Quick decision rule:** Use macro average when every class matters equally regardless of size (rare but critical classes, fairness audits across groups) and each class has enough test examples; avoid it when classes have very few examples, when a junk bucket would drag the mean, or when every error costs the same and total errors are what the business pays for.

### Micro Average

**1. What it measures (plain English):** The micro average adds up all the hits and misses from every class into one big pool and then calculates precision, recall or F1 once. Every individual decision gets one equal vote. For one-label-per-item problems it is exactly the same as accuracy; for multi-label problems (where one item can carry several tags at once) it is a distinct and very useful number.

`Micro-P = ΣTPₖ / (ΣTPₖ + ΣFPₖ)` and `Micro-R = ΣTPₖ / (ΣTPₖ + ΣFNₖ)`, with Micro-F1 the balance of the two.

**2. Intuition:** A shop owner who ignores which aisle a mistake happened in and simply counts the total number of wrong items handed over the counter. Each wrong item costs the same, so the total is what matters.

**3. Benefits:**

- Reflects total error volume, which maps straight to operating cost when each error costs about the same.
- Stable, because it is built from large pooled counts.
- The natural headline for multi-label problems and for entity extraction.
- Simple to compute and explain.

**4. Limitations / Potential issues:**

- Dominated by the biggest classes; a model that ignores every rare class can still score high.
- Identical to accuracy when each item has exactly one label, so reporting both adds no information.
- Hides per-class failures completely.
- Wrong choice when the rare classes are the important ones.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Tagging mobile-money complaints with more than one issue |
| Industry / Domain | Telecom (mobile money) |
| Business Problem | A Nigerian mobile-money provider auto-tags each support ticket with any of three issue labels: Failed transfer, Wrong debit and Account lock. One ticket can carry two labels, and agents review every tag, so each tag decision costs about the same agent time. |
| ML Translation | Target = set of labels per ticket; multi-label classification (each label is an independent yes / no decision); thousands of tickets; label counts are uneven. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Pooling all tag decisions gives a stable score that matches the agents' workload, and in multi-label data micro-F1 is a genuinely different number from accuracy because false alarms and misses are counted separately. |
| Why other metrics are NOT suitable here | Subset accuracy (all tags on a ticket exactly right) is too harsh for tags that agents review; Hamming loss is inflated by the many labels correctly absent; macro-F1 lets the small Account lock label swing the headline although agents care about the total tag workload. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using macro-F1 or subset accuracy would send the team to chase a small label or to reject a model that already saves agent time; the cost is wasted engineering weeks and delayed rollout. |
| Small numeric example | Per label (TP, FP, FN): Failed transfer 120, 20, 30; Wrong debit 60, 15, 15; Account lock 20, 10, 10. Pooled: TP = 200, FP = 45, FN = 55. Micro-P = 200/245 = 0.816; micro-R = 200/255 = 0.784; micro-F1 = 0.80. Macro-F1 = (0.828+0.800+0.667)/3 = 0.765. Note FP (45) is not equal to FN (55), so micro-F1 is not accuracy here. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Counting wrong bays at a parcel sorting hub |
| Industry / Domain | Logistics |
| Business Problem | A New Zealand parcel hub uses a model to send each parcel to one of 5 outbound bays. A parcel in the wrong bay costs NZ$3.50 to re-sort, whichever bay it was meant for. |
| ML Translation | Target = correct bay (5 classes, one label per parcel); multi-class classification; flat cost per error; high volume. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Because every error costs the same, the pooled error count is exactly the business question, and micro-average (which here equals accuracy) answers it directly. |
| Why other metrics are NOT suitable here | Macro-F1 would give a small bay with only a handful of parcels the same weight as the busiest bay although each misroute costs the same; weighted-F1 is nearly the same number with extra steps; per-class precision gives five numbers and no total. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Optimising macro-F1 could pull effort towards a tiny bay and leave the main re-sorting bill untouched; the loss is wasted effort and avoidable re-sort labour. |
| Small numeric example | 200 parcels, 184 in the right bay. Pooled TP = 184, FP = 16, FN = 16. Micro-P = 184/200 = 0.92; micro-R = 0.92; micro-F1 = 0.92 = accuracy. Re-sort cost = 16 × NZ$3.50 = NZ$56. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Pulling parties, dates and amounts out of Arabic contracts |
| Industry / Domain | Legal / courts |
| Business Problem | A Gulf commercial court extracts entity mentions (party names, dates, amounts) from filed contracts to pre-fill case files. A clerk corrects every wrong or missing mention, and each correction takes about the same time. |
| ML Translation | Target = entity mentions found in the text; extraction scored as matched / spurious / missed mentions; pooled counts across entity types; no meaningful negative class. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Each mention is one unit of clerk work, so pooling TP, FP and FN across entity types gives a score tied to correction effort, which is the standard way extraction is judged. |
| Why other metrics are NOT suitable here | Accuracy is meaningless because the thousands of ordinary words are not entities and would inflate it; macro-F1 lets the small Amount type dominate; subset accuracy per document is too harsh when clerks edit mentions one by one. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A score inflated by ordinary words would hide a model that still forces heavy manual correction; the cost is clerk hours and slower case registration. |
| Small numeric example | Party (TP, FP, FN) = 40, 4, 6; Date = 25, 2, 5; Amount = 15, 4, 9. Pooled TP = 80, FP = 10, FN = 20. Micro-P = 80/90 = 0.889; micro-R = 80/100 = 0.80; micro-F1 = 0.842. Per-type F1 = 0.889, 0.877, 0.698, so macro-F1 = 0.821. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — The packhouse that never saw the fruit-fly damage |
| Industry / Domain | Agriculture (export fruit packing) |
| Business Problem | A Chilean fruit packhouse grades each fruit as Good, Blemished or Fruit-fly damage. Fruit-fly damage is only 1% of fruit but one infested piece can get a whole export consignment rejected. |
| ML Translation | Target = grade (3 classes, one label per fruit); multi-class classification; heavily imbalanced (940 / 50 / 10 per 1,000); the rarest class is the costliest. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Micro (accuracy) lets the 940 good fruit set the score, so a model that never spots a single infested fruit still looks excellent. |
| Why other metrics are NOT suitable here | Weighted-F1 also follows the big classes; overall precision hides that no infested fruit is flagged; a single pooled recall has the same weakness. |
| Better alternative (if BAD fit) | Macro-recall (or macro-F1) together with the per-class recall of Fruit-fly damage, because missing that class is the real risk. |
| Business impact of choosing wrong | Shipping infested fruit means a rejected consignment, fumigation or destruction costs and possible loss of the buyer's trust, far larger than the saving from a clean-looking score. |
| Small numeric example | 1,000 fruit. Good 940: 935, 5, 0 predicted as Good, Blemished, Fruit-fly. Blemished 50: 5, 43, 2. Fruit-fly 10: 7, 3, 0. Micro = accuracy = (935+43+0)/1000 = 0.978. Fruit-fly recall = 0/10 = 0. Macro-recall = (0.9947+0.86+0.0)/3 = 0.618. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Three "83%" numbers that are really one |
| Industry / Domain | Insurance |
| Business Problem | A South African short-term insurer routes claim documents into Motor, Property and Liability queues. The monthly report shows accuracy, micro-F1 and weighted recall as if they were three separate confirmations that the model is ready to run without human checks. |
| ML Translation | Target = claim type (3 classes, one label per document); single-label multi-class classification; Liability is small but its claims are the most expensive. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | For one label per item, micro-F1 is exactly accuracy, so it adds no evidence, and it still hides the weak small class. |
| Why other metrics are NOT suitable here | Accuracy and weighted recall are the same number again; weighted-F1 gives Liability only 10% of the weight; micro-precision is also identical to accuracy. |
| Better alternative (if BAD fit) | Report accuracy once for overall throughput, and add macro-F1 plus the per-class table so Liability performance is visible. |
| Business impact of choosing wrong | Management could approve automatic routing for Liability claims, the costliest queue, on the strength of three duplicate numbers, and misrouted large claims would delay settlements and raise complaint costs. |
| Small numeric example | 100 documents. Motor 60: 54, 4, 2; Property 30: 3, 24, 3; Liability 10: 2, 3, 5. Accuracy = 83/100 = 0.83; micro-F1 = 0.83; weighted recall = 0.83; macro-F1 = (0.9076+0.7869+0.5000)/3 = 0.732; Liability F1 = 0.50. |

**6. Quick decision rule:** Use micro average when every individual decision costs about the same, for multi-label problems and for entity extraction; avoid it when rare classes are the high-stakes ones or when you would report it next to accuracy on a one-label-per-item problem, where it is the same number.

### Weighted Average

**1. What it measures (plain English):** The weighted average calculates the score for each class and then averages them, but gives each class a weight equal to its share of the real cases. Bigger classes count more, smaller classes less. It is the row labelled "weighted avg" in most classification reports, and also called the support-weighted average (support = the number of real examples of a class).

`Weighted-F1 = Σ (nₖ / N) × F1ₖ` where nₖ is the support of class k and N is the total number of examples.

**2. Intuition:** A national exam board that reports the overall pass rate of schools weighted by how many pupils each school has, so a big city school counts more than a tiny village school but every school's own result still feeds in.

**3. Benefits:**

- Reflects real-world class frequencies while still being built from per-class scores.
- More stable than macro when some classes are tiny.
- Weighted recall always equals accuracy, a handy consistency check.
- Familiar default in reports, so readers already know how to read it.

**4. Limitations / Potential issues:**

- Under-weights rare classes, so it partly repeats accuracy's blind spot.
- Weighted-F1 is not the balance of weighted precision and weighted recall and can fall outside their range, which can confuse readers.
- Assumes the test set has the same class mix as real life; if the mix changes, the weights are wrong.
- Hides per-class detail.
- Because it is the default, it is often reported without thought.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Sorting new listings on a Latin American online marketplace |
| Industry / Domain | E-commerce |
| Business Problem | A Latin American online marketplace automatically files new seller listings into Electronics, Fashion and Home. The category mix of listings is stable and mirrors real traffic, and leadership wants one number to track each quarter. |
| ML Translation | Target = category (3 classes, one label per listing); multi-class classification; moderately imbalanced (500 / 350 / 150 per 1,000); test mix matches production. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Because the test mix equals the real listing mix, weighting each category by its share gives a number that tracks what sellers actually experience. |
| Why other metrics are NOT suitable here | Macro-F1 would give the smallest category (15% of listings) the same vote as the largest; accuracy has no per-category view to show which one drags; micro-F1 is accuracy again. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (print the per-category table beside it) |
| Business impact of choosing wrong | Using macro-F1 could send effort to the small Home category and leave the big Electronics errors, which affect far more sellers and searches, unfixed. |
| Small numeric example | Per-class F1: Electronics 0.93 (500), Fashion 0.90 (350), Home 0.85 (150). Weighted-F1 = (500×0.93+350×0.90+150×0.85)/1000 = (465+315+127.5)/1000 = 0.9075. Macro-F1 = (0.93+0.90+0.85)/3 = 0.893. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Sizing call-centre staff by the intents callers really have |
| Industry / Domain | Telecom |
| Business Problem | A Moroccan telecom operator classifies each call into Billing (600 calls), Network issue (300) or Plan change (100) to plan agent rosters. Staffing follows call volume, so the executive dashboard needs a volume-faithful score. |
| ML Translation | Target = intent (3 classes, one label per call); multi-class classification; skewed class sizes; evaluation mix equals the real call mix. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Weights follow call volume, which is what drives staffing, and weighted recall equals accuracy, giving a built-in consistency check. |
| Why other metrics are NOT suitable here | Macro-F1 would let the 10% Plan change intent count for a third of the score in a volume-driven decision; accuracy alone cannot show which intent is weak; micro-F1 duplicates accuracy. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (print the per-class table beside it) |
| Business impact of choosing wrong | A score that ignores volume could misdirect improvement work, leaving the biggest call types mis-tagged and rosters mis-sized, with idle agents or long queues as the result. |
| Small numeric example | 1,000 calls. Billing 600: 560, 25, 15; Network 300: 20, 260, 20; Plan 100: 10, 15, 75. Per-class F1 = 0.941, 0.867, 0.714. Weighted recall = accuracy = 895/1000 = 0.895; weighted-F1 = 0.896; macro-F1 = 0.841. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Telling bedrooms from kitchens in property listing photos |
| Industry / Domain | Real estate |
| Business Problem | An Australian property portal labels each listing photo as Bedroom, Bathroom, Kitchen or Exterior to drive search filters. The share of each room type in uploaded photos is stable from month to month. |
| ML Translation | Target = room type (4 classes, one label per photo); multi-class classification; mildly imbalanced (400 / 250 / 200 / 150 per 1,000); production mix equals test mix. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The class mix is genuine and stable, so a frequency-weighted score tells the portal how often a user sees a mislabelled photo. |
| Why other metrics are NOT suitable here | Macro-F1 gives Exterior (15% of photos) the same vote as Bedroom (40%); accuracy shows no per-room breakdown; log loss judges the quality of probabilities, not the labels users see. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (print the per-class table beside it) |
| Business impact of choosing wrong | Over-reacting to a small room type wastes data-labelling budget, while a real drop on common rooms would hurt search results seen by most users. |
| Small numeric example | Per-class F1: Bedroom 0.94 (400), Bathroom 0.91 (250), Kitchen 0.95 (200), Exterior 0.89 (150). Weighted-F1 = (376+227.5+190+133.5)/1000 = 0.927. Macro-F1 = (0.94+0.91+0.95+0.89)/4 = 0.9225. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — The 0.91 score that never caught a forged ID |
| Industry / Domain | Banking (mobile lending) |
| Business Problem | A Kenyan mobile lender classifies each declined application by reason: Low income (700 per 1,000), Thin credit file (270) or Forged ID (30). Spotting forged IDs is the whole point, because those are the loans that are never repaid. |
| ML Translation | Target = decline reason (3 classes, one label per application); multi-class classification; the rare class (Forged ID) is the one that matters. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The two common classes carry 97% of the weight, so a model that never finds a single forged ID still scores a very high weighted-F1. |
| Why other metrics are NOT suitable here | Accuracy and micro-F1 have the same blind spot; weighted precision follows the big classes; the overall mean hides the zero for the forged-ID class. |
| Better alternative (if BAD fit) | Macro-F1 together with the per-class recall for Forged ID, so the rare class cannot be averaged away. |
| Business impact of choosing wrong | Every forged-ID loan that gets through is a write-off; at an assumed KES 15,000 per loan, 30 missed forgeries cost KES 450,000 per 1,000 declines reviewed. |
| Small numeric example | F1 per class: Low income 0.95 (700), Thin file 0.90 (270), Forged ID 0.00 (30). Weighted-F1 = (665+243+0)/1000 = 0.908. Macro-F1 = (0.95+0.90+0.00)/3 = 0.617. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — A crop-disease score earned in the rainy season |
| Industry / Domain | Agriculture |
| Business Problem | A Nigerian agri-tech start-up built a leaf-photo classifier (Healthy, Leaf blight, Rust) and scored it on a rainy-season test set. It will now be used in the dry season, when the disease mix is very different. |
| ML Translation | Target = leaf condition (3 classes); multi-class classification; class mix shifts between the test set and production (a distribution shift), so test-set support is no longer the real mix. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Weighted-F1 uses the test-set class shares as weights, so it measures performance on a world that no longer exists. |
| Why other metrics are NOT suitable here | Accuracy and micro-F1 inherit the same wrong mix; macro-F1 ignores the mix but ignores the volumes as well; a single overall recall has the same flaw. |
| Better alternative (if BAD fit) | Per-class F1 re-weighted by the expected production mix (or macro-F1 plus the per-class table), so the number reflects the season it will be used in. |
| Business impact of choosing wrong | Extension officers would trust a 0.895 score while real dry-season performance is nearer 0.77, so farmers get wrong advice on blight and waste money on sprays or lose crop. |
| Small numeric example | Per-class F1: Healthy 0.95, Leaf blight 0.60, Rust 0.85. Rainy test mix 700 / 100 / 200: weighted-F1 = (665+60+170)/1000 = 0.895. Dry-season mix 300 / 450 / 250: weighted-F1 = (285+270+212.5)/1000 = 0.7675. |

**6. Quick decision rule:** Use weighted average when the test set mirrors real-life class frequencies and you want one volume-faithful headline built from per-class scores; avoid it when the rare classes are the target, or when the production class mix differs from the test mix.

## Multi-Label Metrics

### Hamming Loss

**1. What it measures (plain English):** In a multi-label problem each item can carry several tags at once, so every item has a yes / no decision for every possible tag. Hamming loss is the share of all those individual tag decisions that are wrong. Lower is better, and 1 minus Hamming loss is the label-by-label accuracy.

`Hamming Loss = (1/(N × L)) × Σᵢ Σⱼ 1[yᵢⱼ ≠ ŷᵢⱼ]` where N is the number of items, L the number of possible tags, and the bracket is 1 when the true and predicted value differ.

**2. Intuition:** A teacher marking a form with many tick boxes per question, giving or taking a mark per box. Getting 5 of 6 boxes right still earns most of the marks.

**3. Benefits:**

- Gives full partial credit, so a nearly right tag set is not treated as a total failure.
- Simple, symmetric and easy to explain as "share of tag decisions wrong".
- Fast to compute and stable.
- Reduces to the ordinary error rate for a single yes / no label.

**4. Limitations / Potential issues:**

- Fails on sparse label sets (thousands of possible tags, only a few true per item): predicting no tags at all gives a near-perfect score.
- Treats a missed tag and a wrong extra tag as equally bad, which is rarely true in business.
- Ignores relationships between tags.
- Always compare it with the all-zeros baseline (the loss you get by predicting no tags), otherwise the number is hard to judge.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Tagging amenities in hotel photos for a Mexican booking site |
| Industry / Domain | Tourism |
| Business Problem | A Mexican hotel-booking site tags each hotel photo with any of 8 amenities (pool, gym, sea view, and so on). About half of the amenities appear in a typical photo, and a partner hotel can fix a wrong tag with one click. |
| ML Translation | Target = 8 yes / no amenity labels per photo; multi-label classification; fairly dense labels (about 47% of label slots are positive). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Labels are dense, so correctly absent tags do not swamp the score, and each wrong tag is one small, equal-cost correction, which is exactly what Hamming loss counts. |
| Why other metrics are NOT suitable here | Subset accuracy would call 2 of 4 photos failures although 94% of tag decisions are right; micro-F1 is fine but harder to explain to hotel partners; accuracy per photo is not defined without an all-or-nothing rule. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Judging by exact match would reject a model that already saves most of the manual tagging; the cost is staff time spent tagging by hand and delayed listings. |
| Small numeric example | 4 photos × 8 tags = 32 label slots. Errors: one missed tag on photo 1 and one extra tag on photo 3 = 2 wrong. Hamming loss = 2/32 = 0.0625; label accuracy = 0.9375. All-zeros baseline = 15 true tags / 32 = 0.469, so 0.0625 is a real improvement. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Topic tags on telehealth chats for Egyptian nurses |
| Industry / Domain | Healthcare |
| Business Problem | An Egyptian telehealth service tags each chat transcript with up to 6 topics (fever, cough, medication question, and so on) so a nurse can open the right protocol. The nurse verifies every tag anyway, so a wrong tag and a missing tag cost about the same few seconds. |
| ML Translation | Target = 6 yes / no topic labels per chat; multi-label classification; moderately dense labels (about 46% of label slots are positive). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Because the reviewer checks every tag, the cost really is per tag decision and symmetric, so the share of wrong tag decisions maps straight to review effort. |
| Why other metrics are NOT suitable here | Subset accuracy (0.50 here) hides that 92% of tag decisions are right; Jaccard needs per-chat set sizes and is harder to turn into review minutes; macro-F1 would let rare topics swing the score. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Misjudging the tagger could either block a tool that saves nurse time or approve one that adds review work; both mean slower consultations. |
| Small numeric example | 4 chats × 6 tags = 24 slots. One extra tag on chat 2 and one missed tag on chat 3 = 2 wrong. Hamming loss = 2/24 = 0.0833; label accuracy = 0.9167. All-zeros baseline = 11/24 = 0.458. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Marking damaged panels in accident photos |
| Industry / Domain | Insurance |
| Business Problem | A Brazilian car insurer's model marks which of 6 body panels (bumper, door, bonnet and so on) are damaged in a claim photo. The adjuster uses the marks to pre-fill the repair estimate, and each panel decision affects the estimate by a similar amount. |
| ML Translation | Target = 6 yes / no panel labels per photo; multi-label classification; fairly dense labels (about 43% of slots positive). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Each panel decision moves the estimate about equally, so the share of wrong panel decisions is a direct measure of how much the adjuster must correct. |
| Why other metrics are NOT suitable here | Subset accuracy (0.60 here) treats a photo with one wrong panel like a total miss; micro-F1 pools decisions but is less direct for an estimate built panel by panel; accuracy per photo cannot give partial credit. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | An over-strict metric could lead to the tool being dropped, and adjusters would redo all estimates manually, adding days to claim settlement. |
| Small numeric example | 5 photos × 6 panels = 30 slots. Photo 2 has one extra panel marked; photo 4 has one panel missed = 2 wrong. Hamming loss = 2/30 = 0.0667; label accuracy = 0.933. All-zeros baseline = 13/30 = 0.433. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Three thousand legal-topic tags per court judgment |
| Industry / Domain | Legal / courts |
| Business Problem | A Chilean court-records office tags each judgment with legal topics from a list of 3,000 possible tags; a judgment typically carries about 4 true tags. Researchers search by tag. |
| ML Translation | Target = 3,000 yes / no tag labels per judgment; extreme multi-label classification; very sparse labels (4 of 3,000 positive per document, about 0.13%). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Almost every label slot is a correctly absent tag, so predicting no tags at all gets a near-zero loss while finding nothing. |
| Why other metrics are NOT suitable here | Accuracy has the same flaw; subset accuracy is near zero for every realistic model so it cannot guide tuning; macro-F1 is unstable when thousands of tags have only a few examples. |
| Better alternative (if BAD fit) | Micro-F1 or per-document Jaccard, which ignore correctly absent tags, so predicting nothing scores 0. |
| Business impact of choosing wrong | A search index built on a tagger that finds almost no real tags would return nothing useful for legal researchers, while the report claimed 99.9% accuracy. |
| Small numeric example | One judgment, 4 true tags out of 3,000. Predict nothing: Hamming loss = 4/3,000 = 0.0013 (label accuracy 99.87%). A model finding 1 of 4 with no wrong tags: loss = 3/3,000 = 0.0010. Better alternative: for that model, recall = 1/4 and Jaccard = 1/4 = 0.25, F1 = 0.40; the predict-nothing version scores 0. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — The refinery inspection tagger that misses gas leaks |
| Industry / Domain | Energy |
| Business Problem | A Gulf oil refinery tags each inspection report with up to 6 hazard labels, one of which is Gas leak. A missed gas-leak tag can delay a shutdown, while an unneeded extra tag costs a supervisor a minute. |
| ML Translation | Target = 6 yes / no hazard labels per report; multi-label classification; unequal costs between labels and between error types. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Hamming loss weighs a missed gas leak and a harmless extra tag equally, so two very different models can get the identical score. |
| Why other metrics are NOT suitable here | Subset accuracy cannot tell one wrong tag from many; Jaccard is symmetric in the same way; accuracy per label repeats the problem. |
| Better alternative (if BAD fit) | Per-label recall for Gas leak (with a minimum floor), plus macro-F1 across hazard labels, so a missed critical tag is visible. |
| Business impact of choosing wrong | An undetected gas leak risks fire, injury and an unplanned shutdown costing far more than any number of unneeded tags. |
| Small numeric example | 5 reports × 6 labels = 30 slots, Gas leak true in 3 reports. Model A misses 2 of those 3 leaks: Hamming = 2/30 = 0.0667; Gas leak recall = 1/3 = 0.33. Model B adds 2 harmless extra tags but finds all 3 leaks: Hamming = 2/30 = 0.0667; Gas leak recall = 3/3 = 1.00. Same Hamming loss, very different safety. |

**6. Quick decision rule:** Use Hamming loss when labels are reasonably dense, every tag decision costs about the same, and you want a simple per-tag error rate; avoid it when label sets are sparse (check the all-zeros baseline) or when some tags are far more critical than others.

### Jaccard Score (also called Jaccard Index or IoU)

**1. What it measures (plain English):** For each item, Jaccard compares the set of true labels with the set of predicted labels and divides what they share by everything either of them contains. It is also called the Jaccard index or intersection over union (IoU); in image work the "sets" are areas of pixels. Correctly absent labels earn no credit, which makes it honest on sparse data.

`Jaccard = TP / (TP + FP + FN)` where TP are items in both sets, FP are predicted but not true, and FN are true but not predicted.

**2. Intuition:** Two friends compare shopping lists. The Jaccard score is the number of items on both lists divided by the number of different items on either list; shops neither of them visited do not matter.

**3. Benefits:**

- Ignores true negatives, so it is not inflated when most labels or pixels are absent.
- Gives partial credit, unlike exact match.
- Intuitive overlap meaning; the same metric as IoU in computer vision.
- Ranks models exactly like F1 / Dice, so no information is lost by choosing it.

**4. Limitations / Potential issues:**

- Harsher than F1 for the same predictions, which can look discouraging.
- Undefined when both sets are empty, so a convention is needed.
- Treats a missed item and a wrong extra item as equally bad.
- Several averaging options (per item, per label, pooled) give different answers.
- Not directly usable as a training loss because it is not differentiable.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Outlining smallholder plots from satellite images |
| Industry / Domain | Agriculture (agri-tech) |
| Business Problem | An East African crop-insurance agri-tech outlines each smallholder plot from satellite images to price cover and check claims. A predicted outline counts as a match only if its overlap with the surveyed outline (IoU) is at least 0.5. |
| ML Translation | Target = plot area (pixel mask) per plot; image segmentation scored per plot; the plot covers a tiny share of each image so background dominates. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | IoU measures how well the shapes overlap and ignores the huge area of non-plot land, and the 0.5 rule is the standard way to decide a plot was found. |
| Why other metrics are NOT suitable here | Pixel accuracy is inflated by the empty land around plots; Hamming loss would count every correct background pixel as a success; Dice ranks models the same but the 0.5 IoU match rule is the usual convention for finding objects. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Pixel accuracy would call poor outlines excellent, so insurers would price on wrong plot sizes and mis-settle claims. |
| Small numeric example | Four plots, pixels (TP, FP, FN): 720, 180, 80 gives 720/980 = 0.735; 300, 100, 100 gives 300/500 = 0.600; 150, 250, 150 gives 150/550 = 0.273; 500, 50, 50 gives 500/600 = 0.833. Mean IoU = 0.610; 3 of 4 plots reach 0.5. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Judging next-basket suggestions for a grocery delivery app |
| Industry / Domain | E-commerce |
| Business Problem | A Nigerian grocery delivery app suggests 5 items per customer for the next order. The team wants to know how well the suggested set matches the set the customer actually bought, among thousands of products. |
| ML Translation | Target = set of products bought; multi-label (set) prediction per customer; tiny sets inside a catalogue of thousands of products (sparse). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Jaccard scores the overlap of the suggested and bought sets and ignores the thousands of products that were neither suggested nor bought. |
| Why other metrics are NOT suitable here | Hamming loss would be above 99% for any model because absent products dominate; subset accuracy would give most customers zero; precision at 5 alone ignores bought items that were never suggested. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A metric that rewards doing nothing would hide poor suggestions, leading to lower basket value and customers who stop trusting the suggestions. |
| Small numeric example | Customer 1: 5 suggested, 4 bought, 3 shared, 6 in the union gives 3/6 = 0.500. Customer 2: 4 shared, 7 in union gives 0.571. Customer 3: 5 shared of 5 gives 1.000. Customer 4: 0 shared, 7 in union gives 0.000. Mean Jaccard = (0.5+0.571+1.0+0.0)/4 = 0.518. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Reading skills off CVs for a Gulf recruitment platform |
| Industry / Domain | HR |
| Business Problem | A Gulf recruitment platform tags each CV with skills from a list of 800 possible skills; a typical CV has about 5 true skills. Recruiters search by skill tag. |
| ML Translation | Target = set of skills per CV; multi-label classification; extremely sparse labels (about 5 of 800 positive). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Jaccard counts only skills named in either set, so it reflects how well the predicted skill list matches the real one, with no credit for the hundreds of absent skills. |
| Why other metrics are NOT suitable here | Hamming loss looks superb (above 99.7%) even for a poor tagger; subset accuracy is harsh when one skill is off; accuracy per CV has the same inflation problem as Hamming. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A tagger that looks 99.7% accurate but misses a third of the skills would hide strong candidates from recruiter searches. |
| Small numeric example | Three CVs. CV 1: 4 shared, union 7 gives 0.571. CV 2: 4 of 4 gives 1.000. CV 3: 4 shared, union 7 gives 0.571. Mean Jaccard = 0.714. Hamming loss = 6 wrong / (3 × 800) = 0.0025 (99.75% accurate); predicting no skills gives 15/2,400 = 0.00625 and Jaccard 0. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Mapping a bushfire so evacuation orders go out on time |
| Industry / Domain | Public safety (emergency management) |
| Business Problem | A state emergency service maps the burning area from aerial images to decide which towns get evacuation orders. Leaving a burning area unmapped is far more dangerous than warning an area that turns out to be safe. |
| ML Translation | Target = burning area (pixel mask, measured in hectares); image segmentation; asymmetric costs (missing fire is much worse than over-warning). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Jaccard treats a missed hectare and a falsely mapped hectare as the same, so a map that under-warns can score the same as a safe one. |
| Why other metrics are NOT suitable here | Pixel accuracy is inflated by the unburned land; Dice has the same symmetry; F1 is also symmetric in misses and false alarms. |
| Better alternative (if BAD fit) | Recall of the burning area, with F2 (which counts a miss more heavily than a false alarm) as a summary, so misses are punished. |
| Business impact of choosing wrong | An under-mapped fire front can leave residents without an evacuation order, with risk to life and property; over-warning only costs disruption. |
| Small numeric example | True fire 1,000 ha. Map A covers 800 ha, all inside the fire: TP 800, FP 0, FN 200, Jaccard = 800/1,000 = 0.80, recall 0.80, F2 = 0.833. Map B covers 1,250 ha including the whole fire: TP 1,000, FP 250, FN 0, Jaccard = 1,000/1,250 = 0.80, recall 1.00, F2 = 0.952. Identical Jaccard, but A leaves 200 ha unwarned. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Matching medicine charts in a New Zealand aged-care home |
| Industry / Domain | Healthcare |
| Business Problem | A New Zealand aged-care group auto-builds each resident's list of medicines to dispense from prescriptions. A missing or extra medicine is a medication error and the chart must be exactly right before a pharmacist signs off. |
| ML Translation | Target = set of medicines per resident; multi-label (set) prediction; any single mismatch makes the chart unusable. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Mean Jaccard gives partial credit, so charts with one wrong medicine still score 0.67 to 0.75 and the average looks comfortable. |
| Why other metrics are NOT suitable here | Hamming loss is even more forgiving; micro-F1 pools decisions and hides which charts are wrong; per-label recall ignores extra medicines. |
| Better alternative (if BAD fit) | Subset accuracy (exact match), read as the share of charts that need no pharmacist correction. |
| Business impact of choosing wrong | A dispensing error can harm a resident and trigger incident reports and review; a mean score of 0.88 would hide that 2 of 5 charts are wrong. |
| Small numeric example | 5 residents. Resident 2 is missing paracetamol: 3/4 = 0.75. Resident 3 has an extra aspirin: 2/3 = 0.667. Others exact: 1.0 each. Mean Jaccard = (1+0.75+0.667+1+1)/5 = 0.883. Subset accuracy = 3/5 = 0.60. |

**6. Quick decision rule:** Use Jaccard when label sets are sparse or when comparing shapes or areas, and partial overlap deserves partial credit; avoid it when misses are far costlier than false alarms or when the whole set must be exactly right.

### Subset Accuracy (exact match ratio)

**1. What it measures (plain English):** Subset accuracy is the share of items for which the entire predicted label set exactly matches the true set. One wrong or missing label and the item scores zero. It is also called the exact match ratio, and it is what scikit-learn's accuracy score computes on multi-label data.

`Subset Accuracy = (1/N) × Σᵢ 1[Yᵢ = Ŷᵢ]` where the bracket is 1 only if the complete predicted set equals the complete true set.

**2. Intuition:** A pharmacist checking a prescription basket: either the whole basket is exactly right and goes out, or it goes back to be redone.

**3. Benefits:**

- Maps directly to an automation rate: the share of cases needing no human touch.
- Unambiguous and easy to explain.
- Right when partial correctness has no value.
- No averaging choices to argue about.

**4. Limitations / Potential issues:**

- Extremely harsh: no partial credit at all.
- Falls quickly as the number of labels per item grows, so it cannot be compared across datasets with different label counts.
- Cannot tell one wrong label from all labels wrong, so it is a poor guide when tuning a model.
- Ignores which labels were wrong and how badly.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Auto-approving prior authorisations with the exact procedure codes |
| Industry / Domain | Insurance (health) |
| Business Problem | A Brazilian health insurer's model proposes the full set of procedure codes for each prior-authorisation request. A request with a missing or extra code is rejected by the payment system and goes to a manual desk costing BRL 40 per request. |
| ML Translation | Target = set of procedure codes per request; multi-label (set) prediction; the whole set must match for straight-through processing. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Because partially right code sets are rejected anyway, the share of exactly right requests is the straight-through processing rate, which drives the savings case. |
| Why other metrics are NOT suitable here | Jaccard (0.83) and Hamming loss would suggest most work is automated when only 60% is; micro-F1 pools codes and hides which requests fail; per-code recall ignores extra codes. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A partial-credit metric would overstate savings by about a third, so the business case would miss target and manual-desk staffing would be underestimated. |
| Small numeric example | 5 requests. Request 3 true codes D, E, F but predicted D, E: not equal. Request 5 true code I but predicted I, J: not equal. Other 3 exact. Subset accuracy = 3/5 = 0.60. Mean Jaccard = (1+1+0.667+1+0.5)/5 = 0.833. Manual cost = 2 × BRL 40 = BRL 80. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — The right document checklist for each bank applicant |
| Industry / Domain | Banking |
| Business Problem | A Gulf bank's onboarding model picks, for each applicant, the exact list of documents to request (ID, proof of address, salary letter, and so on). A missing or extra document means the applicant is contacted again, costing about AED 150 and often the customer. |
| ML Translation | Target = set of required documents per applicant; multi-label (set) prediction; the full list must be right to avoid a second contact. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The share of applicants whose checklist is exactly right is the share who complete onboarding in one pass, which is the business target. |
| Why other metrics are NOT suitable here | Hamming loss counts a checklist that is one document off as 90% right although the customer is bounced; micro-F1 and Jaccard give the same kind of partial credit. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A forgiving metric would approve a model that triggers repeat contacts for a third of applicants, raising cost and abandonment. |
| Small numeric example | 6 applicants, 4 with an exactly right checklist: subset accuracy = 4/6 = 0.667. The 2 others each cost AED 150 to re-contact: 2 × 150 = AED 300 per 6 applicants. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Twenty-five product attributes for a Latin American online shop |
| Industry / Domain | E-commerce |
| Business Problem | A Latin American online shop tags each product with 25 yes / no attributes (organic, gluten-free, and so on) and a team reports exact-match accuracy to leadership. |
| ML Translation | Target = 25 yes / no attribute labels per product; multi-label classification; many labels per item, so errors compound. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | With many labels, one slip anywhere zeros the product, so a low score can come from the label count rather than a weak model. |
| Why other metrics are NOT suitable here | Accuracy per product is the same exact-match number; Jaccard alone does not reveal per-tag error rate; macro-F1 focuses on rare attributes. |
| Better alternative (if BAD fit) | Hamming loss or micro-F1 for model quality, with subset accuracy kept only as a separate automation KPI reported with the label count. |
| Business impact of choosing wrong | Leadership could cancel a model that gets 96% of tags right, losing the savings, or spend heavily on over-tuning to lift a number that is capped by the label count. |
| Small numeric example | Per-tag accuracy 0.96 with 25 independent tags: expected subset accuracy = 0.96^25 = 0.360, while Hamming loss = 0.04. With only 5 tags the same model scores 0.96^5 = 0.815. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Does the news-tag suggester save editor time |
| Industry / Domain | Media |
| Business Problem | A Kenyan news publisher shows editors suggested tags for each article; editors keep the right ones, delete the wrong ones and add any that are missing. Each correct suggestion saves about 6 seconds and each wrong one costs about 4 seconds to delete. |
| ML Translation | Target = set of topic tags per article; multi-label classification; a human edits the suggestions, so partial credit has real value. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Only 1 of 5 articles is an exact match, so subset accuracy is 0.20 and calls the tool a failure although it saves editor time on almost every article. |
| Why other metrics are NOT suitable here | Hamming loss is inflated if the tag list is long; accuracy per article is exact match again; macro-F1 over-weights rare tags that editors rarely use. |
| Better alternative (if BAD fit) | Micro-F1 or mean per-article Jaccard, which reward each correct tag the way editors experience it. |
| Business impact of choosing wrong | Rejecting the tool on a harsh metric would forfeit real editor time savings across every article published. |
| Small numeric example | 5 articles: exact match on 1 only, subset accuracy = 0.20. Mean Jaccard = (1+0.667+0.667+0.8+0.667)/5 = 0.76. Pooled: TP 13, FP 3, FN 1, so micro-F1 = 26/30 = 0.867. Time saved = 13 × 6 − 3 × 4 = 66 seconds. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Comparing two pole-defect taggers that both score zero |
| Industry / Domain | Energy (power utility) |
| Business Problem | An Australian power utility tags defects (5 possible types) on photos of power poles. Two candidate models are being compared during development, and the team uses exact-match accuracy as the tuning score. |
| ML Translation | Target = 5 yes / no defect labels per pole; multi-label classification; model selection during development needs a score that moves when the model improves. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Subset accuracy cannot tell one wrong label from all wrong, so a nearly right model and a useless one tie at zero. |
| Why other metrics are NOT suitable here | Accuracy per pole is the same exact-match score; only a score with partial credit can show progress; a precision-only view would ignore missed defects. |
| Better alternative (if BAD fit) | Hamming loss and mean per-pole Jaccard (or micro-F1), which move whenever any label improves. |
| Business impact of choosing wrong | The team could discard the better model or tune blind, wasting weeks and delaying a tool that cuts costly field inspections. |
| Small numeric example | 4 poles, true defects [1,1,0,1,0] each. Model A gets exactly 1 label wrong on every pole; model B gets 4 of 5 labels wrong on every pole. Subset accuracy: A = 0, B = 0. Hamming loss: A = 4/20 = 0.20, B = 16/20 = 0.80. Mean Jaccard: A = 0.6875, B = 0.00. |

**6. Quick decision rule:** Use subset accuracy when a partly right label set is worthless and you need the share of cases needing no human touch, and report the label count beside it; avoid it for model tuning, for long label lists, or when humans edit the suggestions.

## Threshold, Odds and Overlap Metrics

### Youden's J Statistic

**1. What it measures (plain English):** Youden's J adds sensitivity (the share of real positives the model catches) and specificity (the share of real negatives it correctly clears) and subtracts 1. It equals the true positive rate minus the false positive rate. A value of 0 is no better than a coin flip and 1 is perfect, and the cut-off score that maximises J is a popular way to pick a decision threshold (the score above which the model raises an alert).

`J = Sensitivity + Specificity − 1`

**2. Intuition:** A bouncer choosing how strict the ID check should be. The best setting turns away the most under-age guests while refusing the fewest adults, with both kinds of error counted as equally bad.

**3. Benefits:**

- Gives a concrete threshold, not only a score.
- Uses both classes' performance and is not affected by how common the positive class is.
- Chance level is fixed at 0, so it is easy to read.
- Simple to compute from the table of true and false positive rates at each threshold.

**4. Limitations / Potential issues:**

- Assumes a false alarm and a miss cost the same; if they do not, the J-best threshold is wrong.
- Ignores prevalence (how common the positive class is), so on rare events the J-best threshold can give very low precision.
- Ignores operational capacity: it may flag far more cases than a team can handle.
- A single operating point, so a poor way to compare whole models (a ranking measure such as AUC is better).
- Mathematically the same as adjusted balanced accuracy and the best KS statistic, so reporting all three adds nothing.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Setting the ripeness cut-off on a mango packhouse sensor |
| Industry / Domain | Agriculture (export packhouse) |
| Business Problem | A Kenyan mango packhouse uses a ripeness sensor score to decide which mangoes are export-ready. Shipping a not-ready mango means a rejection fee; downgrading a ready mango to the local market loses about the same margin. |
| ML Translation | Target = export-ready yes / no; binary classification with a score; both classes about equally common; roughly equal cost of the two errors. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | With equal error costs and fairly balanced classes, the threshold that maximises J is a sound and easy-to-justify cut-off. |
| Why other metrics are NOT suitable here | Accuracy ignores which error is made and shifts with class mix; F1 ignores true negatives (not-ready mangoes correctly held back), which matter equally here; AUC gives no threshold at all. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A poorly placed cut-off means either rejected export consignments or good mangoes sold cheaply, each costing money on every pallet. |
| Small numeric example | 10 mangoes (6 ready, 4 not). At score 0.61: caught 5 of 6 (sensitivity 0.833), 1 not-ready flagged ready, so specificity = 3/4 = 0.75. J = 0.833 + 0.75 − 1 = 0.583. Other cut-offs: 0.80 gives J = 0.50; 0.55 gives J = 0.333; 0.43 gives J = 0.50. Best cut-off = 0.61. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Choosing the pass mark on a graduate assessment |
| Industry / Domain | HR |
| Business Problem | A Nigerian employer tests graduate applicants and wants a pass mark that best separates people who turned out to succeed after 12 months from those who did not. Hiring a person who fails and rejecting one who would have succeeded are judged to cost about the same. |
| ML Translation | Target = successful at 12 months yes / no; binary classification using the test score; a threshold must be picked; roughly symmetric costs. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The aim is the cut-off that separates the two groups best, with neither error favoured, which is the J criterion. |
| Why other metrics are NOT suitable here | Precision (success rate among hires) ignores strong people rejected; F1 ignores correctly rejected candidates; accuracy shifts with the success rate in the applicant pool. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A too-high mark rejects capable graduates and a too-low one lets in weak hires, both costing recruitment fees and retraining. |
| Small numeric example | 8 applicants (5 succeeded, 3 did not). Pass mark 66: 4 of 5 successes pass (sensitivity 0.80), 1 of 3 failures passes, so specificity = 2/3 = 0.667. J = 0.80 + 0.667 − 1 = 0.467. Pass mark 85 gives J = 0.40; pass mark 50 gives J = 0.333. Best = 66. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — A remittance screen where a miss costs 100 times a false alarm |
| Industry / Domain | Banking (remittances) |
| Business Problem | A money-transfer operator scores each cross-border transfer for money-laundering risk. A manual review of a clean transfer costs about USD 5; an undetected suspicious transfer costs about USD 500 in fines and clean-up. |
| ML Translation | Target = suspicious yes / no; binary classification with a score; rare positives; very unequal error costs. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | J gives a miss and a false alarm equal weight, so it picks a cut-off that lets a suspicious transfer through rather than paying for a few extra reviews. |
| Why other metrics are NOT suitable here | Accuracy is dominated by clean transfers; F1 also treats misses and false alarms symmetrically; AUC gives no threshold. |
| Better alternative (if BAD fit) | Choose the cut-off that minimises total expected cost (for calibrated probabilities the best cut-off is about cost of a false alarm divided by the sum of both costs), then report sensitivity and specificity there. |
| Business impact of choosing wrong | Following J here would cost about 25 times more than the cost-based cut-off in this toy case, and in real life means regulatory fines and reputational harm. |
| Small numeric example | 12 transfers, 3 suspicious. Cut-off 0.85: J = 0.667 − 0 = 0.667 (best J), 1 miss, 0 false alarms, cost = 1 × 500 = USD 500. Cut-off 0.35: J = 1.0 − 0.444 = 0.556, 0 misses, 4 false alarms, cost = 4 × 5 = USD 20. The J-best cut-off costs 25 times more. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Fifty inspectors and a threshold that flags 673 containers |
| Industry / Domain | Government (border biosecurity) |
| Business Problem | A Pacific-region biosecurity agency scores about 5,000 arriving containers a day for pest risk, of which about 100 are truly risky. Inspectors can physically open only 50 containers a day. |
| ML Translation | Target = risky container yes / no; binary classification with a score; rare positives (2%); a hard daily capacity of 50 inspections. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | J picks a cut-off with no regard for capacity, so it flags far more containers than can be opened. |
| Why other metrics are NOT suitable here | Accuracy is about 98% for predicting nothing; F1 ignores capacity; AUC gives a whole-ranking score but no daily cut-off. |
| Better alternative (if BAD fit) | Precision at K (and recall at K) with K = 50, i.e. open the 50 highest-scored containers and measure how many are truly risky. |
| Business impact of choosing wrong | Pests slip through while inspectors open containers picked almost at random from a long list, risking costly outbreaks for farms and exporters. |
| Small numeric example | At the J-best cut-off: sensitivity 0.85, false positive rate 0.12, so J = 0.73. Flagged = 85 true + 0.12 × 4,900 = 588 false = 673. Opening 50 at random from those finds about 50 × 85/673 = 6.3 risky containers. Ranking by score and opening the top 50 (assuming precision 0.60 there) finds about 30. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Hunting meter tampering with a threshold that wastes 96% of visits |
| Industry / Domain | Energy (electricity distribution) |
| Business Problem | An Egyptian electricity distributor scores 10,000 customer meters for tampering; about 100 (1%) are truly tampered. A field visit costs EGP 400. |
| ML Translation | Target = tampered yes / no; binary classification with a score; rare positives (1%); precision matters because every flag costs a visit. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | J ignores how rare the positives are, so a cut-off that looks balanced between sensitivity and specificity still produces mostly false alarms. |
| Why other metrics are NOT suitable here | Accuracy is 99% for predicting nothing; AUC says nothing about visits per find; specificity alone ignores missed tampering. |
| Better alternative (if BAD fit) | Precision-recall analysis and precision at the visit budget, choosing the threshold from visit cost against recovered revenue. |
| Business impact of choosing wrong | Thousands of wasted visits per round, with the real cost per detected case far above the value of the electricity recovered. |
| Small numeric example | At the J-best cut-off: sensitivity 0.80, false positive rate 0.20, J = 0.60. Flagged = 80 true + 0.20 × 9,900 = 1,980 false = 2,060 meters. Precision = 80/2,060 = 0.039. Cost = 2,060 × 400 = EGP 824,000, or EGP 10,300 per detected case. |

**6. Quick decision rule:** Use Youden's J to pick a cut-off when false alarms and misses cost about the same and classes are not extremely rare; avoid it when costs are unequal, when inspection capacity is limited, or when positives are very rare and precision matters.

### Diagnostic Odds Ratio (DOR)

**1. What it measures (plain English):** The diagnostic odds ratio compares the odds of a positive test result in people who truly have the condition with the odds of a positive result in people who do not. It squeezes sensitivity and specificity into one number that does not depend on how common the condition is (its prevalence). A DOR of 1 means the test is useless, and higher is better.

`DOR = (TP × TN) / (FP × FN)`, which also equals LR+ / LR−.

**2. Intuition:** Two weather forecasters: how many times more likely is the forecaster to say "rain" on a day that turns out rainy than on a dry day, however often it rains in this city?

**3. Benefits:**

- Does not depend on prevalence, so results can be pooled across populations.
- One number that summarises sensitivity and specificity together.
- Breaks down into likelihood ratios (LR+ and LR−) that support updating an individual's risk.
- Well-developed statistics, including confidence intervals on the log scale.

**4. Limitations / Potential issues:**

- Unbounded and unstable when any cell count is small; undefined when FP or FN is zero (a continuity correction such as adding 0.5 to each cell is used).
- Cannot tell a rule-out test from a rule-in test: two tests with opposite strengths can share the same DOR.
- Says nothing about precision (PPV) in a real population, which is what many decision makers need.
- Not intuitive for managers.
- Threshold dependent; always report a confidence interval and sensitivity and specificity beside it.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Pooling a malaria rapid test across two Tanzanian districts |
| Industry / Domain | Healthcare |
| Business Problem | A national health programme wants to know whether a malaria rapid test works equally well in a high-malaria district and a low-malaria district before pooling both districts' results. |
| ML Translation | Target = infected yes / no; binary test result; two populations with very different prevalence (40% versus 5%); comparison of test quality, not of local predictive value. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The DOR is identical in both districts although prevalence differs eightfold, which is the prevalence-free comparison needed for pooling. |
| Why other metrics are NOT suitable here | Precision (PPV) is 0.85 in one district and 0.31 in the other, so it would wrongly suggest the test works worse in the low-prevalence district; accuracy and F1 also move with prevalence. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Judging by precision could wrongly withdraw a good test from low-prevalence districts, leaving cases undiagnosed. |
| Small numeric example | District A (1,000 people, 40% infected): TP 340, FN 60, TN 540, FP 60. DOR = (340 × 540)/(60 × 60) = 183,600/3,600 = 51. District B (2,000 people, 5% infected): TP 85, FN 15, TN 1,710, FP 190. DOR = (85 × 1,710)/(190 × 15) = 145,350/2,850 = 51. PPV: A = 340/400 = 0.85; B = 85/275 = 0.31. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — One scorecard, two borrower segments with different default rates |
| Industry / Domain | Banking |
| Business Problem | A Colombian lender uses one scorecard flag for salaried borrowers (default rate 4%) and informal-sector borrowers (default rate 20%), and the risk team wants to know whether it separates good from bad equally well in both segments. |
| ML Translation | Target = default yes / no; binary classification at a fixed cut-off; two segments with very different base rates; the question is separation power, not hit rate. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | DOR is the same in both segments, showing the scorecard separates equally well even though the segments' default rates differ fivefold. |
| Why other metrics are NOT suitable here | Precision is 0.23 versus 0.64 and would wrongly suggest poor quality in the salaried segment; accuracy and F1 depend on the default rate; the default rate itself says nothing about separation. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Judging by precision could lead the bank to rebuild a scorecard that works fine, or to set wrong segment cut-offs. |
| Small numeric example | Salaried (1,000 loans, 40 defaults): TP 28, FN 12, FP 96, TN 864. DOR = (28 × 864)/(96 × 12) = 24,192/1,152 = 21. Informal (1,000 loans, 200 defaults): TP 140, FN 60, FP 80, TN 720. DOR = (140 × 720)/(80 × 60) = 100,800/4,800 = 21. Precision: 28/124 = 0.23 versus 140/220 = 0.64. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Two impairment screens with the same score and opposite jobs |
| Industry / Domain | Mining (occupational health) |
| Business Problem | A Western Australian mine is choosing between two on-site drug and alcohol screens for 1,000 workers (about 5% impaired). One is very sensitive but flags many healthy workers; the other rarely wrongly flags anyone but misses many impaired workers. |
| ML Translation | Target = impaired yes / no; binary test; low prevalence; the two tests have different sensitivity and specificity but the same DOR. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | DOR collapses the sensitivity and specificity trade-off into one number, so it cannot tell a screening (rule-out) test from a confirmatory (rule-in) test. |
| Why other metrics are NOT suitable here | Accuracy is dominated by non-impaired workers; AUC is not defined for a single fixed-result test; a single F1 hides which error dominates. |
| Better alternative (if BAD fit) | Report sensitivity and specificity (or LR+ and LR−) and the precision (PPV) at 5% prevalence, then choose the test by its job. |
| Business impact of choosing wrong | Picking the wrong test type either stands down hundreds of healthy workers or lets impaired workers on to site, risking injury and lost production. |
| Small numeric example | Test A (sensitivity 0.98, specificity 0.50): TP 49, FN 1, FP 475, TN 475. DOR = (49 × 475)/(475 × 1) = 49. Test B (sensitivity 0.50, specificity 0.98): TP 25, FN 25, FP 19, TN 931. DOR = (25 × 931)/(19 × 25) = 49. PPV: A = 49/524 = 0.09; B = 25/44 = 0.57. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — A pest-detection pilot with 40 trays and one empty cell |
| Industry / Domain | Agriculture (horticulture) |
| Business Problem | A New Zealand kiwifruit grower pilots a camera that flags trays carrying a quarantine pest. The pilot checks only 40 trays and the camera missed none of the 8 infested trays. |
| ML Translation | Target = infested tray yes / no; binary classification; very small sample; a zero count among the misses. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | With zero misses, DOR divides by zero, and any correction gives a huge, unstable number that one more miss would cut in half. |
| Why other metrics are NOT suitable here | Accuracy hides the small sample; F1 gives no uncertainty range; AUC needs scores and more data. |
| Better alternative (if BAD fit) | Report sensitivity and specificity with exact confidence intervals, which show how little 8 infested trays can prove. |
| Business impact of choosing wrong | Quoting a DOR above 200 could convince the grower to roll out an unproven camera across all orchards, risking missed pests and export problems. |
| Small numeric example | TP 8, FN 0, FP 2, TN 30: DOR = (8 × 30)/(2 × 0), undefined. With +0.5 correction: (8.5 × 30.5)/(2.5 × 0.5) = 259.25/1.25 = 207.4. If one more tray had been missed (TP 7, FN 1): (7 × 30)/(2 × 1) = 105. Better: sensitivity 8/8 = 1.00 with 95% confidence interval 0.63 to 1.00; specificity 30/32 = 0.94, interval 0.79 to 0.99. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — A dental-billing audit tool sold on its odds ratio |
| Industry / Domain | Insurance (health) |
| Business Problem | A Gulf health insurer is pitched an audit tool for wasteful dental billing, where about 1% of 10,000 monthly claims are truly wasteful. The vendor quotes only a diagnostic odds ratio. An audit of one claim costs AED 300. |
| ML Translation | Target = wasteful claim yes / no; binary classification at a fixed cut-off; rare positives; the buyer cares about audit cost per recovered case. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | DOR ignores prevalence by design, but the insurer's costs depend on prevalence, so a high-sounding DOR hides a very low hit rate. |
| Why other metrics are NOT suitable here | Accuracy is about 99% for flagging nothing; AUC says nothing about cost per audit; sensitivity alone ignores wasted audits. |
| Better alternative (if BAD fit) | Precision (PPV) at the real 1% prevalence and cost per recovered case, with sensitivity and specificity shown alongside. |
| Business impact of choosing wrong | Buying on a DOR of 76 means paying for audits where 86% of flagged claims are fine, so audit spend outruns recoveries. |
| Small numeric example | Sensitivity 0.80, specificity 0.95: DOR = (80 × 9,405)/(495 × 20) = 752,400/9,900 = 76. Per 10,000 claims: 100 wasteful, TP = 80, FP = 0.05 × 9,900 = 495. Precision = 80/575 = 0.139. Audits = 575 × AED 300 = AED 172,500, or AED 2,156 per recovered case. |

**6. Quick decision rule:** Use the diagnostic odds ratio when comparing or pooling tests across populations with different prevalence, always with sensitivity, specificity and a confidence interval; avoid it for deployment decisions, small samples, and when precision in a real population or rule-in versus rule-out matters.

### Dice Coefficient (Sørensen-Dice)

**1. What it measures (plain English):** Dice is twice the overlap between the predicted and true region (or set) divided by the total size of both. It is also called the Sørensen-Dice coefficient or Dice similarity coefficient, and for yes / no classification it is exactly the F1 score. It ignores true negatives, so a huge empty background cannot flatter it.

`Dice = 2 × TP / (2 × TP + FP + FN)`

**2. Intuition:** Two people trace the same outline on tracing paper. Dice measures how much the two traces overlap, counting the shared part from both sides so a perfect match scores 1.

**3. Benefits:**

- Not inflated by a large background (true negatives are absent).
- Intuitive overlap meaning and the same value as F1.
- Standard in medical and industrial image segmentation.
- Has a differentiable "soft" version used as a training loss.
- More forgiving than Jaccard while ranking models identically.

**4. Limitations / Potential issues:**

- Blind to the location of errors: scattered edge errors and a missed solid chunk can score the same.
- Treats a missed area and an over-drawn area as equally bad.
- Unstable for very small objects, where a few pixels change the score a lot.
- Undefined when both masks are empty, so the convention used for empty images changes the average.
- Not comparable across different targets or datasets; do not mix with Jaccard values.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Measuring coffee rust on a leaf photo |
| Industry / Domain | Agriculture |
| Business Problem | A Colombian coffee cooperative photographs leaves and outlines the rust-infected area to score disease severity. Healthy leaf area is the vast majority of every picture. |
| ML Translation | Target = infected pixel yes / no; image segmentation; strong imbalance between background and lesion pixels. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Dice scores only the overlap of the predicted and true lesion, so the large healthy area cannot hide a weak outline. |
| Why other metrics are NOT suitable here | Pixel accuracy looks excellent even for a poor outline; Hamming-style per-pixel error does the same; AUC says nothing about outline overlap. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A flattering accuracy would hide wrong severity scores, so farms spray too early or too late. |
| Small numeric example | Leaf of 5,000 pixels; true lesion 400, predicted 440, overlap 360. TP 360, FP 80, FN 40, TN 4,520. Dice = 720/(720+120) = 0.857; Jaccard = 360/480 = 0.75; pixel accuracy = (360+4,520)/5,000 = 0.976. Predicting no lesion: accuracy 0.92 but Dice 0. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Counting building footprints in an informal settlement |
| Industry / Domain | Real estate (urban planning) |
| Business Problem | An East African city planning office maps building footprints in informal settlements from satellite tiles to plan water and drainage. Buildings cover only a few percent of each tile. |
| ML Translation | Target = building pixel yes / no; image segmentation scored per tile; heavy background. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Per-tile Dice measures building overlap regardless of how much empty land surrounds it, and averaging over tiles stops big tiles from hiding bad small ones. |
| Why other metrics are NOT suitable here | Pixel accuracy is 94% even for predicting no buildings; Hamming loss behaves the same way; recall alone ignores falsely drawn buildings. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Under-estimating built-up area means pipes and drains are planned for fewer people than live there. |
| Small numeric example | Tile 1 (100,000 px): TP 4,800, FP 700, FN 1,200, so Dice = 9,600/11,500 = 0.835 while pixel accuracy = 0.981 (and 0.94 for no buildings). Tile 2: TP 300, FP 50, FN 100: Dice = 600/750 = 0.80. Tile 3: TP 2,000, FP 500, FN 400: Dice = 4,000/4,900 = 0.816. Mean Dice = 0.817. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Finding hairline cracks on a dam wall |
| Industry / Domain | Construction (infrastructure inspection) |
| Business Problem | A Brazilian hydropower operator uses drone photos of a concrete dam face to outline cracks. A crack covers a tiny fraction of each photo, and the same score is used as a training objective. |
| ML Translation | Target = crack pixel yes / no; image segmentation; extreme imbalance (crack of 200 pixels in a 512 × 512 image). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Dice measures overlap with the thin crack and, in its soft form, can be used directly as the training loss so the model is not rewarded for predicting only background. |
| Why other metrics are NOT suitable here | Pixel accuracy is 99.9% for an all-background model; plain cross-entropy loss is dominated by background pixels; recall alone ignores falsely drawn cracks. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A model trained on pixel accuracy would learn to find no cracks, and the operator would miss early warning signs of structural damage. |
| Small numeric example | Image of 512 × 512 = 262,144 pixels; true crack 200 px, predicted 180 px, overlap 150. TP 150, FP 30, FN 50. Dice = 300/380 = 0.789; Jaccard = 150/230 = 0.652. Predicting no crack: pixel accuracy = 1 − 200/262,144 = 0.9992, Dice = 0. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Radiotherapy contours with the same Dice and different dangers |
| Industry / Domain | Healthcare |
| Business Problem | A Brazilian public cancer centre compares two automatic tumour outlines used to plan radiotherapy. Under-covering the tumour edge under-doses the tumour, and a stray region near the spinal cord over-doses a sensitive organ. |
| ML Translation | Target = tumour voxel yes / no (a voxel is a 3-D pixel); 3-D segmentation; the location and direction of errors matter clinically. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Dice measures only how much overlaps, not where the errors are or whether they are misses or over-drawing. |
| Why other metrics are NOT suitable here | Accuracy is inflated by background voxels; Jaccard has the same location-blindness; F1 is the same number as Dice. |
| Better alternative (if BAD fit) | Dice together with sensitivity (recall) and the 95th-percentile Hausdorff distance (the near-worst boundary gap), so misplaced errors show up. |
| Business impact of choosing wrong | Choosing the second outline could under-dose part of the tumour and over-dose a critical organ, causing treatment failure or injury. |
| Small numeric example | True tumour 1,000 voxels. Both outlines: TP 900, FP 100, FN 100, so Dice = 1,800/2,000 = 0.90 and sensitivity 0.90. Outline A: errors form a thin rim, worst gap about 1 mm (assumed). Outline B: the missed 100 voxels are a solid chunk of the margin and the 100 extra voxels sit near the spinal cord, worst gap about 12 mm (assumed). |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Solar-farm hot-spot images where most pictures are empty |
| Industry / Domain | Energy (solar) |
| Business Problem | A Chilean solar operator flies drones over panels and uses a model to outline hot spots. Many images contain no hot spot at all, and the team must report one mean score. |
| ML Translation | Target = hot-spot pixel yes / no per image; image segmentation; many images with an empty true mask. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | When both the true and predicted masks are empty, Dice is 0/0, and whether those images count as 1, 0 or are skipped changes the mean score completely. |
| Why other metrics are NOT suitable here | Pixel accuracy is dominated by empty background; Jaccard has the same empty-image problem; Hamming loss behaves like pixel accuracy. |
| Better alternative (if BAD fit) | Image-level sensitivity and specificity for the question "is there a hot spot?", plus Dice on images that do contain one, with the rule stated. |
| Business impact of choosing wrong | A score that depends on how empty images are counted can make a mediocre model look excellent, or vice versa, leading to wrong decisions about inspection crews. |
| Small numeric example | 5 images: 3 with hot spots, Dice 0.8, 0.7, 0.9; 2 empty and correctly predicted empty. Empty counted as 1: (2.4+2)/5 = 0.88. Empty skipped: 2.4/3 = 0.80. Empty counted as 0: 2.4/5 = 0.48. The same model gets 0.48, 0.80 or 0.88. |

**6. Quick decision rule:** Use Dice when judging how well a predicted region or set overlaps the true one and the background is huge, and state how empty images are handled; avoid it when the position or direction of errors matters, for tiny objects, or when you need to compare across different targets.

## Ranking-Style Multi-Class Metrics

### Top-K Accuracy [Added – not in source file]

**1. What it measures (plain English):** Top-K accuracy counts a prediction as correct if the true class is anywhere among the K classes the model scored highest. With K = 1 it is ordinary accuracy; with K = 3 the model gets credit if the right answer is in its top three guesses. It is also called top-k hit rate and is common when there are many classes or several plausible answers.

`Top-K Accuracy = (1/N) × Σᵢ 1[true class of item i is among the K highest-scored classes]`

**2. Intuition:** A spell-checker offering three suggestions. If the word you meant is anywhere in those three, you are happy; it does not matter whether it was first, second or third.

**3. Benefits:**

- Matches products that show a short list and let a human pick.
- Fair when classes are similar or truly ambiguous, so the top guess alone is too harsh.
- Simple to compute and explain.
- Standard for problems with many classes (large image or product catalogues).

**4. Limitations / Potential issues:**

- Depends entirely on K: a larger K always gives a higher score, so K must match what the user really sees.
- Meaningless when K is a large share of the classes: random guessing already scores K divided by the number of classes.
- Ignores the order inside the top K, so a first-place and a third-place answer count the same (rank-aware measures such as mean reciprocal rank do not have this weakness).
- Hides weak top-1 performance, which matters whenever the system acts on its single best guess.
- Needs model scores, not only labels, and says nothing about whether the scores are well calibrated.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — A symptom checker that shows nurses three possible conditions |
| Industry / Domain | Healthcare |
| Business Problem | A Nigerian telehealth app lists the 3 most likely conditions for each patient's symptoms on the clinician's screen; the clinician makes the call. Many conditions share symptoms, so the single best guess is often not the final answer. |
| ML Translation | Target = condition (many classes, one true label per patient); multi-class scoring; the model outputs a ranked list and the screen shows the top 3. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The clinician sees exactly 3 options, so the share of cases where the true condition is among them is exactly the share where the screen helps. |
| Why other metrics are NOT suitable here | Top-1 accuracy is too harsh because look-alike conditions often swap places; macro-F1 needs a single predicted label per patient; rank-aware measures such as mean reciprocal rank are useful too, but top-3 mirrors what is displayed. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Judging by top-1 would reject a tool that puts the right condition in front of the clinician in two of three cases, losing a useful second opinion. |
| Small numeric example | 6 patients; rank of the true condition in the model list: 1, 3, 2, 5, 1, 4. Top-1 = 2/6 = 0.333; top-3 = 4/6 = 0.667; top-5 = 6/6 = 1.00. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — A pest photo app that offers three candidates to the farmer |
| Industry / Domain | Agriculture |
| Business Problem | An agricultural extension service in Uganda lets farmers photograph a pest and shows the 3 most likely pests with treatment advice; the farmer or extension officer picks the match. Several pests look alike in photos. |
| ML Translation | Target = pest species (many classes); image classification with ranked scores; the user interface displays 3 candidates. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The user chooses among the displayed candidates, so being in the top 3 is what makes the right advice reachable. |
| Why other metrics are NOT suitable here | Top-1 accuracy ignores the human-in-the-loop choice and understates usefulness; macro-F1 needs one label per photo; log loss measures score quality, not what the farmer sees. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Underrating the app could stop a service that gets farmers to the right treatment in most cases, and crops are lost to the wrong or delayed spray. |
| Small numeric example | 8 photos; rank of the true pest: 1, 2, 1, 4, 3, 1, 2, 7. Top-1 = 3/8 = 0.375; top-3 = 6/8 = 0.75; top-5 = 7/8 = 0.875. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Suggesting case-type codes to registry clerks |
| Industry / Domain | Legal / courts |
| Business Problem | A South African court registry has 120 case-type codes. When a clerk registers a filing, the system suggests 5 codes, and searching the full list takes about 45 seconds while picking from the suggestions takes about 10 seconds. |
| ML Translation | Target = case-type code (120 classes); multi-class classification with ranked scores; the interface shows the top 5. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The clerk sees 5 suggestions, so the share of filings whose code is among them directly sets the average time saved. |
| Why other metrics are NOT suitable here | Top-1 accuracy undervalues a list the clerk scans in seconds; macro-F1 over 120 classes is noisy and not what the screen shows; accuracy at K = 1 would hide most of the time saved. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Dropping the tool on a low top-1 score would keep clerks searching a 120-code list for every filing, slowing registrations and growing backlogs. |
| Small numeric example | 10 filings; rank of the true code: 1, 3, 1, 2, 6, 1, 4, 12, 2, 1. Top-1 = 4/10 = 0.40; top-5 = 8/10 = 0.80. Average clerk time = (8 × 10 + 2 × (10 + 45))/10 = 190/10 = 19 seconds, against 45 seconds without suggestions. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Fully automatic parcel routing that acts on the first guess |
| Industry / Domain | Logistics |
| Business Problem | An Australian courier's sorting line reads each parcel label and sends it automatically down one of 12 lanes with no human check; the system always acts on its single highest-scored lane. |
| ML Translation | Target = destination lane (12 classes); multi-class classification; the system must commit to one answer, so only the top guess matters. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Top-3 accuracy credits the model when the right lane is second or third, but the machine never gets to use the second or third choice. |
| Why other metrics are NOT suitable here | Weighted-F1 over lanes hides which lanes fail; macro-F1 over-weights small lanes; per-lane precision gives many numbers and no total. |
| Better alternative (if BAD fit) | Top-1 accuracy (with per-lane recall), plus a confidence cut-off that sends uncertain parcels to a human. |
| Business impact of choosing wrong | A reported 96% looks safe but 30 in every 100 parcels would be misrouted, each costing a re-sort and a late delivery. |
| Small numeric example | 1,000 parcels: top-3 accuracy 0.96 but top-1 accuracy 0.70. Misrouted = 1,000 × (1 − 0.70) = 300 parcels; at AUD 6 per re-sort = 300 × 6 = AUD 1,800 per 1,000 parcels. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Why a failed mobile-money payment has only five possible reasons |
| Industry / Domain | Telecom (mobile money) |
| Business Problem | A mobile-money provider in East Africa classifies each failed payment into one of only 5 failure reasons (low balance, network timeout, wrong PIN and so on) and the team reports top-3 accuracy to look better. |
| ML Translation | Target = failure reason (5 classes, one true label per failed payment); multi-class classification; K is a large share of the number of classes. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | With K = 3 out of 5 classes, a random guesser already lands the true class in its top 3 six times in ten, so the score cannot show real skill. |
| Why other metrics are NOT suitable here | Weighted-F1 is fine for volume but hides rare reasons; accuracy at K = 3 is the flawed number; log loss measures probabilities rather than what customer support sees. |
| Better alternative (if BAD fit) | Top-1 accuracy compared with the 20% chance rate (and macro-F1 for rare reasons), since with 5 classes the first guess is what customer support acts on. |
| Business impact of choosing wrong | Support would trust an 0.80 headline while in 7 of 10 cases the first suggested reason is wrong, producing wrong advice to customers and repeat calls. |
| Small numeric example | 10 failed payments; rank of the true reason: 1, 2, 4, 3, 1, 2, 5, 3, 2, 1. Top-3 = 8/10 = 0.80, but pure chance gives 3/5 = 0.60. Top-1 = 3/10 = 0.30 against chance 1/5 = 0.20. |

**6. Quick decision rule:** Use top-K accuracy when the product shows K options and a human picks, or when many classes are genuinely look-alike, and set K to what the screen really displays; avoid it when the system must act on one answer, when K is a large share of the classes, or when the order within the list matters.
