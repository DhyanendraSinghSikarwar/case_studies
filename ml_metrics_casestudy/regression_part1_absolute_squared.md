# Regression Case Studies, Part 1: Absolute and Squared Error Metrics

## Table of Contents

- [Absolute Error Metrics](#absolute-error-metrics)
  - [Mean Absolute Error (MAE)](#mean-absolute-error-mae)
  - [Median Absolute Error (MedAE)](#median-absolute-error-medae)
  - [Max Error](#max-error)
- [Squared Error Metrics](#squared-error-metrics)
  - [Sum of Squared Errors (SSE / RSS)](#sum-of-squared-errors-sse--rss)
  - [Mean Squared Error (MSE)](#mean-squared-error-mse)
  - [Root Mean Squared Error (RMSE)](#root-mean-squared-error-rmse)
- [Signed Error Metric](#signed-error-metric)
  - [Mean Bias Error (MBE) [Added – not in source file]](#mean-bias-error-mbe-added--not-in-source-file)

**How to read this part:** each metric has a short explanation followed by five case studies (some where the metric is the right choice, some where it is the wrong one). A regression model predicts a number, and the "error" is the gap between the predicted and the actual number. All money is in rupees (₹); 1 lakh = 100,000 and 1 crore = 10,000,000. Every toy example is small enough to check by hand.

## Absolute Error Metrics

### Mean Absolute Error (MAE)

**1. What it measures (plain English):** The average size of the miss, ignoring direction. If a forecast is "off by 4 units on average", that sentence is the MAE. It is also called L1 error or, in some forecasting books, Mean Absolute Deviation (MAD), and it is in the same units as the thing being predicted.

`MAE = (1/n) × Σ abs(yᵢ − ŷᵢ)`

**2. Intuition:** A cricket coach measures how far each throw lands from the stumps, in centimetres, and averages the distances. A throw 20 cm wide counts exactly twice as bad as one 10 cm wide, and left or right does not matter.

**3. Benefits:**

- Easy to explain to anyone: "on average we are off by this much", in the target's own units.
- Multiply it by a cost per unit of error and you get rupees directly, when cost is proportional to the miss.
- Fairly robust to outliers (a few freak data points), because a miss of 200 counts as 200 and not as 40,000.
- Works for any real-valued target, including zeros and negatives.

**4. Limitations / Potential issues:**

- Scale-dependent: an MAE of 30 is excellent for a product selling 5,000 units and awful for one selling 100, so MAE cannot be compared across series of different size.
- Blind to bias: errors of +5, +5, +5 and of +5, −5, +5 give the same MAE.
- Hides the shape of the errors: nine small misses and one huge one can average out to the same number as ten medium misses.
- A model trained to minimise MAE aims for the median (the middle value), not the mean (the average), so on right-skewed targets (a few very large values) its totals come out too low.
- Treats a big miss as only proportionally worse, which is wrong when large misses are disproportionately costly.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Rostering pickers at a quick-commerce dark store |
| Industry / Domain | e-commerce |
| Business Problem | A quick-commerce operator staffs each shift of a neighbourhood dark store (a small warehouse serving nearby homes) with pickers who collect items for orders. Each picker too many or too few costs about ₹600 for the shift, in idle wages or in overtime and lost orders. |
| ML Translation | Target = pickers needed per shift (a small whole number); supervised regression; six months of shift history; no extreme outliers; cost is proportional to the miss. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The cost is linear: being 2 pickers off costs exactly twice as much as being 1 off, which is precisely how MAE scores errors. Multiplying MAE by ₹600 gives the rupee leakage per shift, a number the operations head understands. |
| Why other metrics are NOT suitable here | RMSE punishes a rare big miss far more than the ₹600-per-picker cost does, and its result cannot be multiplied by ₹600; MAPE (percentage error) blows up on quiet night shifts that need only 2 or 3 pickers; MedAE ignores the bad shifts that still cost real money. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Tuning to RMSE would make the model chase rare festival spikes while ordinary shifts stay mis-rostered, so daily wage leakage stays high across hundreds of stores. |
| Small numeric example | Needed pickers over 6 shifts: 12, 15, 10, 18, 14, 16; forecast: 13, 13, 11, 20, 14, 15 → absolute errors 1, 2, 1, 2, 0, 1 → sum 7 → MAE = 7/6 = 1.17 pickers → × ₹600 = about ₹700 per shift (₹4,200 over the six shifts). RMSE would be 1.35 pickers (squares 1+4+1+4+0+1 = 11; 11/6 = 1.83; square root 1.35), which has no direct rupee meaning. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Nurse-hours for a private hospital's wards |
| Industry / Domain | healthcare |
| Business Problem | A private hospital forecasts the nursing hours each ward needs per day. Every hour short is bought as agency cover and every hour spare is idle pay, both at roughly ₹450 per hour. |
| ML Translation | Target = nurse-hours needed per ward per day (continuous number); supervised regression; features are admissions, surgeries scheduled and ward type; moderate data size, no heavy tail. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Over- and under-staffing cost the same rate per hour, so total cost is proportional to total absolute error. MAE converts straight into rupees per ward-day and is easy for finance to read. |
| Why other metrics are NOT suitable here | RMSE assumes large misses cost more than their size, which is not true of hourly wages; R² (the share of variation a model explains) is a unitless score that cannot be turned into rupees; MPE (mean percentage error) or bias metrics show direction only and let over- and under-staffing cancel out. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A metric that over-weights rare surge days leaves everyday staffing sloppy; across many wards that is a steady monthly cost leak and sometimes thin cover for patients. |
| Small numeric example | Needed hours over 5 ward-days: 96, 110, 88, 120, 104; forecast: 100, 104, 92, 118, 110 → absolute errors 4, 6, 4, 2, 6 → sum 22 → MAE = 22/5 = 4.4 hours → × ₹450 = ₹1,980 per ward-day. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Dyeing batch times at a textile mill |
| Industry / Domain | manufacturing |
| Business Problem | A textile mill schedules its dye house using predicted batch duration. Each minute of mismatch either leaves an expensive machine idle or causes an overrun that delays the next lot, costing roughly ₹8 per minute. |
| ML Translation | Target = dyeing batch time in minutes; supervised regression; features are fabric type, shade depth and load weight; a few hundred batches per month; errors are small and symmetric. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Machine time is billed at a flat rate per minute, so the penalty grows in a straight line with the miss. MAE is the average number of minutes wasted per batch. |
| Why other metrics are NOT suitable here | Max Error reports one worst batch and says nothing about the daily average waste; RMSE puts extra weight on rare big misses that are not extra costly here; MAPE treats a 5-minute miss on a 60-minute batch as worse than on a 160-minute batch, though the machine cost is identical. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Picking the wrong yardstick gives a model that looks good on paper but wastes machine minutes every shift, which at mill scale adds up to lakhs per month. |
| Small numeric example | Actual minutes over 6 batches: 140, 155, 130, 160, 150, 145; forecast: 135, 160, 128, 152, 155, 150 → absolute errors 5, 5, 2, 8, 5, 5 → sum 30 → MAE = 30/6 = 5.0 minutes → × ₹8 = ₹240 over six batches, or ₹40 per batch. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Crop-insurance payout reserve across districts |
| Industry / Domain | insurance |
| Business Problem | A general insurer must set aside enough money for a monsoon season's crop-loss claims. The regulator checks that the total reserve covers the total payout, and one flood-hit district usually dwarfs all the rest. |
| ML Translation | Target = payout per district in ₹ lakh; supervised regression; strongly right-skewed (a few very large values); the team trained the model with an MAE (L1) loss. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | An MAE-trained model aims for the median district, so it predicts the typical small payout and ignores the flood district. The average error looks tolerable, but the total reserve comes out far too low. |
| Why other metrics are NOT suitable here | MedAE is even more blind to the one big district; Max Error flags the flood district but gives no total; MAPE would exaggerate errors in tiny-payout districts and still not check the sum. |
| Better alternative (if BAD fit) | Train and judge with MSE or RMSE, which aim for the mean so that district totals add up, and always report the signed total bias (MBE) next to it. |
| Business impact of choosing wrong | A reserve short by crores means the insurer cannot pay farmers on time, faces regulatory action and may need emergency capital. |
| Small numeric example | Payouts over 5 districts (₹ lakh): 8, 10, 12, 14, 106 (total 150). Median-style prediction 12 for every district → absolute errors 4, 2, 0, 2, 94 → MAE = 20.4; predicted total 60, short by ₹90 lakh. Mean-style prediction 30 → absolute errors 22, 20, 18, 16, 76 → MAE = 30.4 (worse by MAE) but predicted total 150 is exactly right, and MSE is 1,448 against 1,772. MAE prefers the wrong model. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Ranking two distributor forecasting teams by raw MAE |
| Industry / Domain | retail |
| Business Problem | A packaged-foods company wants to reward whichever of two distributor teams forecasts carton demand better. The north team handles about 5,000 cartons per week per product; the south team handles about 200. |
| ML Translation | Target = cartons sold per week per product; supervised forecasting; two series of very different scale; evaluation is a ranking of teams, not training. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MAE is in raw cartons, so it is mostly a measure of how big the business is. The big team is automatically punished and the small team automatically flattered. |
| Why other metrics are NOT suitable here | RMSE and MSE are also scale-dependent and even more distorted; MedAE and Max Error have the same unit problem; plain MPE only shows bias direction, not accuracy. |
| Better alternative (if BAD fit) | WAPE (total absolute error divided by total actual sales, a percentage) or MASE (an error measure scaled against a naive forecast), which put both teams on a common scale. |
| Business impact of choosing wrong | The bonus and the coaching effort go to the wrong team: a genuinely weak forecaster is praised and a good one is blamed. |
| Small numeric example | North: actual 5,000, 4,800, 5,200, 5,000; forecast 4,750, 5,050, 4,950, 5,250 → every miss is 250 → MAE = 250 cartons → WAPE = 1,000/20,000 = 5.0%. South: actual 200, 180, 220, 200; forecast 170, 210, 190, 230 → every miss is 30 → MAE = 30 → WAPE = 120/800 = 15.0%. MAE says south is better; WAPE says north is three times more accurate. |

**6. Quick decision rule:** Use MAE when the cost of an error grows in a straight line with its size and you want a plain "average miss in the target's units"; avoid it when comparing series of different scale, when the total must be right on a skewed target, or when big misses are disproportionately costly.

### Median Absolute Error (MedAE)

**1. What it measures (plain English):** The size of the typical miss: line up all the absolute errors from smallest to largest and take the middle one. "Half of our predictions are closer than this." It is in the target's units and is unaffected by even a handful of crazy errors.

`MedAE = median(abs(y₁ − ŷ₁), abs(y₂ − ŷ₂), ..., abs(yₙ − ŷₙ))`

**2. Intuition:** When a village asks "how long does the bus usually take?", the answer is what happens on a normal day, not the average that includes the one day a flood blocked the road. MedAE is that normal-day answer.

**3. Benefits:**

- The most outlier-proof error metric: up to half the data can be corrupted and it barely moves.
- Has a clean reading: half of all predictions land within this distance of the truth.
- Comparing it with MAE is a free diagnostic: a big gap (MAE well above MedAE) means a few bad misses are inflating the average.
- Stable in production monitoring, so one weird record does not trigger a false alarm.

**4. Limitations / Potential issues:**

- Ignores the tail completely, and the tail is sometimes where the money or the danger is.
- Cannot be used as a training loss, because it depends on one middle value and gives no signal about how to improve.
- Throws away most of the data, so it is noisier than MAE on clean data.
- Scale-dependent and blind to bias, like MAE.
- A change that fixes the worst predictions without moving the middle leaves MedAE unchanged.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Used-tractor valuation with typos in dealer listings |
| Industry / Domain | agriculture |
| Business Problem | A rural dealer network values used tractors with a model and tracks its weekly accuracy. Listings are keyed in by hand, and an occasional price typed with an extra zero corrupts the check data. |
| ML Translation | Target = resale price in ₹ thousand; supervised regression; mostly clean data with a rare data-entry outlier (a freak value); used for monitoring while cleaning is pending. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | MedAE reads the typical valuation error and ignores the single typo, so it shows the true health of the model. The MAE-to-MedAE gap also points at the dirty record. |
| Why other metrics are NOT suitable here | MAE jumps to nearly 10 times the typical miss because of one typo; RMSE is hit even harder because it squares the bad value; Max Error only tells you about the typo itself, not about the model. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | An MAE-based dashboard would send engineers to retrain a perfectly good model and delay the real fix, which is cleaning the listing data. |
| Small numeric example | Absolute errors over 6 listings (₹ thousand): 8, 12, 10, 9, 11, 540 → sorted 8, 9, 10, 11, 12, 540 → middle two are 10 and 11 → MedAE = 10.5. MAE = 590/6 = 98.3 and RMSE = 220.6 (squares sum 292,110; divided by 6 is 48,685; square root 220.6). The typical miss is ₹10.5 thousand, not ₹98 thousand. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Telling marketplace sellers when their payout will land |
| Industry / Domain | e-commerce |
| Business Problem | An online marketplace shows each seller an expected payout-settlement date. A few disputed orders take weeks, but they go through a separate dispute team. The operations dashboard should show what a normal seller experiences. |
| ML Translation | Target = days from delivery to settlement; supervised regression; most values within a few days; a rare long-tail of disputed cases handled elsewhere. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | "Half of sellers get paid within one day of the date we show" is a clear promise, and MedAE reports exactly that without being distorted by the disputed cases that have their own process. |
| Why other metrics are NOT suitable here | MAE would show a scary 3.6 days driven by one dispute; RMSE would show even more; MAPE is unstable when the true gap is a fraction of a day. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (pair it with a 90th-percentile error (the error that 90% of predictions stay below) so the dispute tail is still tracked separately). |
| Business impact of choosing wrong | A dashboard dominated by disputes sends the team firefighting the wrong problem and makes a healthy settlement model look broken to management. |
| Small numeric example | Absolute errors over 7 payouts (days): 0.5, 1, 1, 0.5, 1.5, 1, 20 → sorted 0.5, 0.5, 1, 1, 1, 1.5, 20 → the 4th value is 1 → MedAE = 1.0 day. MAE = 25.5/7 = 3.64 days, more than three times the typical experience. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Provisioning for recoveries on defaulted gold loans |
| Industry / Domain | banking |
| Business Problem | A mid-size private lender (NBFC) predicts how much it will recover on each defaulted loan to decide how much to provision (set aside). Provisioning must cover the big loans, since they hold most of the money at risk. |
| ML Translation | Target = recovery shortfall per loan in ₹ lakh; supervised regression; most loans are small, a few are very large; the tail carries the financial risk. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MedAE reports a comfortable middle-of-the-pack error and completely ignores the one large loan that was badly mispredicted, which is exactly the loan that decides the provision. |
| Why other metrics are NOT suitable here | MAE dilutes the tail by averaging; Max Error shows the single worst loan but not the broader tail; MAPE would focus on small loans where the rupee stakes are low. |
| Better alternative (if BAD fit) | RMSE (it counts big misses extra), reported with the 90th-percentile absolute error and a signed bias (MBE) check. |
| Business impact of choosing wrong | Under-provisioning for the big accounts shows up later as a surprise loss in the quarterly results, and auditors will ask why the model looked fine. |
| Small numeric example | Absolute errors over 7 loans (₹ lakh): 1, 1, 2, 2, 3, 4, 60 → MedAE = 2 (the 4th value). MAE = 73/7 = 10.4; RMSE = 22.8; the 60-lakh loan alone is 60/73 = 82% of all the error. MedAE says "2 lakh typical" while the money at risk is 60 lakh. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Predicting patient stay for bed planning |
| Industry / Domain | healthcare |
| Business Problem | A hospital predicts each admitted patient's length of stay to plan bed availability. A small group of complicated patients stay much longer than predicted and block beds for everyone behind them. |
| ML Translation | Target = length of stay in days; supervised regression; most stays are short and predictable, a minority are long and unpredictable. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MedAE describes the routine patient, who is already well predicted, and hides the long-stay patients who cause bed shortages. The error that matters sits in the tail the metric ignores. |
| Why other metrics are NOT suitable here | Max Error is set by one single patient and is too jumpy to track; MAPE is distorted by very short stays; MPE or MBE would show the direction of the error but not its size. |
| Better alternative (if BAD fit) | MAE and RMSE together with the 90th-percentile absolute error, because bed planning is driven by the large under-predictions. |
| Business impact of choosing wrong | Bed shortfalls mean cancelled elective surgeries, patients waiting in the emergency room and lost revenue, all while the dashboard says the model is accurate. |
| Small numeric example | Absolute errors over 8 patients (days): 0.5, 0.5, 0.5, 0.5, 1, 1, 6, 8 → middle two values are 0.5 and 1 → MedAE = 0.75 days. MAE = 18/8 = 2.25; RMSE = 3.59 (squares sum 103; 103/8 = 12.9; square root 3.59). Two patients carry 14 of the 18 total error days. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Wall-thickness prediction for boiler tubes |
| Industry / Domain | manufacturing |
| Business Problem | A boiler maker predicts tube wall thickness from process readings before the tube is cut and certified. A tube whose thickness is wrong by more than 1.0 mm fails a safety inspection and must be scrapped. |
| ML Translation | Target = wall thickness in mm; supervised regression; small, tightly controlled errors with occasional rare big ones; a hard tolerance exists. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MedAE looks superb because almost every tube is predicted within a fraction of a millimetre. It hides the one tube that is far outside the safe tolerance. |
| Why other metrics are NOT suitable here | MAE still buries the one bad tube inside an average; RMSE softens it by averaging; MAPE on a thin wall measurement does not map to a pass/fail limit. |
| Better alternative (if BAD fit) | Max Error checked against the 1.0 mm tolerance as a pass/fail test, because a single failure is the whole story. |
| Business impact of choosing wrong | A bad tube released into a boiler is a safety and liability risk, far costlier than the scrap value of the tube. |
| Small numeric example | Absolute errors over 7 tubes (mm): 0.1, 0.1, 0.1, 0.2, 0.2, 0.3, 2.4 → MedAE = 0.2 mm. MAE = 3.4/7 = 0.49 mm. Max Error = 2.4 mm, which is above the 1.0 mm tolerance → the model fails the safety check even though MedAE looks excellent. |

**6. Quick decision rule:** Use MedAE when you want the typical error and your data has outliers or typos you should not chase; avoid it when the tail carries the money or the safety risk, and never use it as a training objective.

### Max Error

**1. What it measures (plain English):** The single largest miss in the whole test set: the worst thing the model did. It is also called worst-case error or Chebyshev error, and it is in the target's units. Every other metric averages; this one refuses to.

`Max Error = max(abs(y₁ − ŷ₁), ..., abs(yₙ − ŷₙ))`

**2. Intuition:** A bridge engineer does not care that the average rivet is fine; she cares about the weakest rivet, because the bridge fails at its weakest point.

**3. Benefits:**

- The only metric that speaks directly to worst-case risk.
- Easy to compare with a stated tolerance, which gives a clean pass or fail.
- The fastest way to find corrupted or mislabelled rows, since the worst error usually points at a data problem.
- Cannot be averaged away by good performance elsewhere.

**4. Limitations / Potential issues:**

- Decided by one single data point, so it is very unstable and changes if the test set changes.
- Grows as the test set grows, because more rows give more chances to see an extreme value, so it is not comparable across datasets of different sizes.
- Says nothing about the bulk of the predictions.
- Extremely sensitive to a single wrong label in the test data.
- Cannot be used as a practical training loss, and is scale-dependent and blind to bias.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Soft-sensor for capsule fill weight in a pharma plant |
| Industry / Domain | healthcare (pharmaceutical manufacturing) |
| Business Problem | A drug maker predicts capsule fill weight from machine readings, to release batches without weighing every capsule. A batch whose predicted weight is more than 5 mg off the true weight breaches the quality specification and must be held back. |
| ML Translation | Target = fill weight in mg; supervised regression; small clean dataset; a hard tolerance of 5 mg is set in advance by the quality team. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The decision is pass or fail against a tolerance, and one batch beyond it is enough to fail. Max Error tests exactly that. |
| Why other metrics are NOT suitable here | MAE can look better for a model that has one dangerous miss; RMSE blends the bad batch into an average; MedAE ignores the rare large error that triggers the quality breach. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (keep MAE for ordinary model tuning). |
| Business impact of choosing wrong | Releasing a batch with an out-of-spec dose is a regulatory and patient-safety event; recalls cost crores and damage trust. |
| Small numeric example | Model A absolute errors (mg) over 6 batches: 1.2, 0.8, 2.1, 1.5, 4.2, 0.9 → MAE = 10.7/6 = 1.78, Max Error = 4.2 (passes the 5 mg limit). Model B: 0.5, 0.4, 0.6, 0.5, 0.7, 5.8 → MAE = 8.5/6 = 1.42 (looks better), Max Error = 5.8 (fails). Only Max Error picks the safe model. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Auditing digitised land-record areas against satellite estimates |
| Industry / Domain | real estate |
| Business Problem | A state land-records department digitised plot areas by hand. It trained a model to estimate plot area from satellite images, and wants to find records that were wrongly keyed, not to judge the model. |
| ML Translation | Target = plot area in square metres; supervised regression used as a data-quality detector; many records, nearly all consistent; a few suspect rows. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The worst error points straight at the most suspicious record, and the row can then be checked by a human. Here the metric is a pointer, not a score. |
| Why other metrics are NOT suitable here | MAE and RMSE spread one bad record across the whole set and do not tell you which row to open; MedAE ignores outliers by design, which is the opposite of what an audit needs. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (follow it with a look at the top five worst rows). |
| Business impact of choosing wrong | A wrongly recorded plot area leads to disputes in property registration, wrong stamp duty and court cases that run for years. |
| Small numeric example | Absolute errors over 6 plots (sq m): 12, 8, 15, 10, 9, 860 → Max Error = 860 on the last plot (registry says 1,200; satellite says 340). MedAE = 11 and MAE = 152.3. Max Error leads to the bad row; the other two do not. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Comparing delivery-time model tests of very different size |
| Industry / Domain | logistics |
| Business Problem | A courier company tested a delivery-time model on a 5-order pilot sample in one city and on a 20-order sample nationally, and a manager compared the Max Error of both to decide whether the model got worse at scale. |
| ML Translation | Target = delivery time error in minutes; supervised regression; two test sets of different size drawn from the same error pattern. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The more orders you test, the more likely you are to see one extreme case, so the maximum rises with test size even if the model is exactly as good. The comparison is unfair by construction. |
| Why other metrics are NOT suitable here | MAE is fine but ignores the tail the manager worries about; RMSE also grows with rare events and is hard to read; MedAE hides the tail completely. |
| Better alternative (if BAD fit) | A high percentile of absolute error, such as the 90th or 99th, which settles to a stable value as data grows and can be compared across test sets. |
| Business impact of choosing wrong | A good model gets rolled back, or a mediocre one approved, because of a test-size artefact, wasting weeks of engineering effort. |
| Small numeric example | Pilot absolute errors (min): 3, 5, 4, 6, 8 → Max Error = 8, 90th percentile = 7.2. National sample of 20 (min): the same five plus 4, 5, 7, 3, 6, 5, 4, 7, 6, 5, 3, 4, 6, 22, 5; its Max Error = 22 but its 90th percentile = 7.1. The Max Error nearly tripled while the 90th percentile did not move. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Picking a loan-sizing model when one income figure was mistyped |
| Industry / Domain | banking |
| Business Problem | A retail bank compared two models that predict applicant annual income (in ₹ lakh) for loan sizing, using Max Error on a six-person test set. One test record had income keyed as 48 instead of 4.8. |
| ML Translation | Target = annual income in ₹ lakh; supervised regression; tiny test set containing one label typo (a wrongly recorded true value). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Max Error is decided entirely by the typo row, so it measures the typo and not the models. It rewarded the worse model because that one happened to guess slightly closer to the wrong label. |
| Why other metrics are NOT suitable here | RMSE and MAE are also pulled badly by the typo; Max Error is the worst offender because it sees nothing else; MPE (signed percentage error) on one huge row is unstable. |
| Better alternative (if BAD fit) | Fix the mistyped label first, then compare on MAE; while the data is dirty, MedAE gives a fairer ranking. |
| Business impact of choosing wrong | The bank sizes loans with the model that is worse for 5 of 6 customers, leading to over-lending or turned-away good customers. |
| Small numeric example | Model A absolute errors (₹ lakh) over 6 applicants: 1.0, 1.1, 1.2, 1.3, 1.4, 42.5; Model B: 0.3, 0.3, 0.4, 0.4, 0.5, 43.3. Max Error: A = 42.5, B = 43.3 → Max Error picks A. MedAE: A = 1.25, B = 0.4 → B is clearly better. Excluding the typo row, MAE is A = 1.2 and B = 0.38. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Guaranteeing a portfolio of rooftop solar installations |
| Industry / Domain | energy |
| Business Problem | A rooftop solar installer promises a housing society that the combined monthly generation of eight homes will be at least 95% of the forecast. The team looked at Max Error and panicked over one shaded roof. |
| ML Translation | Target = monthly kWh generated per home; supervised regression; the contract is on the portfolio total, not on any single home. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Max Error is driven by the single shaded home and is irrelevant to a guarantee written on the total. It would trigger an alarm even though the contract is comfortably safe. |
| Why other metrics are NOT suitable here | MedAE hides the shaded home but also says nothing about the total; RMSE is also driven by the one roof; MAE alone does not tell you whether the total is over or under. |
| Better alternative (if BAD fit) | The signed total bias (MBE as a percentage of total actual) for the contract check, plus MAE for general accuracy; treat the shaded roof as a separate data issue. |
| Business impact of choosing wrong | The installer might add an unnecessary safety buffer, quote higher prices and lose the contract, or ignore the real total risk. |
| Small numeric example | Actual kWh over 8 homes: 300, 320, 280, 310, 290, 305, 315, 150 (total 2,270); signed errors (forecast minus actual): +5, −8, +6, −4, +7, −6, +3, +40. Max Error = 40 (the shaded home, which is 26.7% of its own actual). But the total forecast is 2,313, and the actual total is 2,270 / 2,313 = 98.1% of forecast, which meets the 95% guarantee. MAE = 79/8 = 9.9 kWh. |

**6. Quick decision rule:** Use Max Error when a single large miss is unacceptable and there is a written tolerance, or as a quick pointer to bad rows; avoid it for comparing models on noisy labels, across test sets of different size, or for any goal defined on totals or averages.

## Squared Error Metrics

### Sum of Squared Errors (SSE / RSS)

**1. What it measures (plain English):** The total of all the squared misses, without averaging. It is also called RSS (Residual Sum of Squares), and some books write SSR for the same thing (others use SSR for a different quantity, so always define your terms). It is the quantity that ordinary least squares regression literally minimises, and its units are the target's units squared.

`SSE = Σ (yᵢ − ŷᵢ)²`

**2. Intuition:** A tailor fitting a line through a set of pin marks on a cloth squares each gap and adds them all up; the best line is the one with the smallest total. The total itself is a building block for other measures, not something you quote to a customer.

**3. Benefits:**

- It is the exact quantity minimised by ordinary least squares, so it links directly to classical statistics.
- Adds up cleanly over rows, which makes it the base for R², F-tests and the model-comparison scores AIC and BIC.
- Perfect for comparing two models fitted on exactly the same rows.
- Helps show concentration: what share of the total squared error comes from the worst few points.

**4. Limitations / Potential issues:**

- Grows with the number of rows, so it cannot be compared across datasets of different sizes.
- Units are squared (rupees-squared), which has no meaning to a manager.
- Extremely sensitive to outliers, since one big miss squared dominates the total.
- Has no built-in sense of "good": the same SSE can be excellent or terrible depending on how much the target varies.
- The neat split of total variation into explained and unexplained parts holds only for plain least squares with an intercept.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Does a festival-week flag improve a brand's sales model? |
| Industry / Domain | marketing |
| Business Problem | A consumer-goods brand has a weekly sales model based on price. It wants to know whether adding a festival-week flag improves the model enough to justify keeping it, using the same eight weeks of data. |
| ML Translation | Target = weekly sales in ₹ lakh; two nested least-squares regression models (the second adds one feature); same 8 rows for both. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Both models are fitted on the same rows, so SSE is directly comparable, and the drop in SSE is the input to a standard F-test (a test of whether an added feature really helps). |
| Why other metrics are NOT suitable here | MAE has no matching statistical test for nested models; RMSE is just a transformed MSE and does not directly feed the F-test formula; MAPE has no least-squares theory behind it. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Keeping a useless feature clutters the model, while dropping a useful one makes the marketing team misread festival-week sales and set wrong ad budgets. |
| Small numeric example | Fitted by least squares on the same 8 weeks. Model 1 (price only) residuals (rounded): −1.51, 3.36, −3.51, 4.23, −3.64, −0.77, 8.49, −6.64 → SSE = 173.8. Model 2 (price plus festival flag) residuals: 0.78, −1.23, −1.22, 2.70, 1.72, −2.30, 0.83, −1.28 → SSE = 21.5. F = ((173.8 − 21.5)/1) / (21.5/5) = 35.4, well above the 5% cut-off of 6.6 for 1 and 5 degrees of freedom → keep the flag. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Calibrating a soil-moisture sensor for a farmers' cooperative |
| Industry / Domain | agriculture |
| Business Problem | A cooperative fits a line that turns raw sensor voltage into soil-moisture percentage for its irrigation scheduler. It has two candidate lines from the same five lab-checked readings and needs the line that fits best. |
| ML Translation | Target = lab moisture percentage; simple linear regression with one feature (voltage); five calibration points; the fit objective is least squares. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Least squares is defined as the line with the smallest SSE, and both lines are scored on the same five points. The comparison is exactly what SSE was made for. |
| Why other metrics are NOT suitable here | MAE would pick a different line and has no simple formula for the best line; Max Error would be driven by one point and ignore the rest; MedAE with five points is decided by a single value. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A poor calibration line over-irrigates or under-irrigates fields all season, wasting water and electricity or stressing crops. |
| Small numeric example | Voltage 1.0, 1.4, 1.9, 2.3, 2.9 against lab moisture 10, 15, 20, 25, 30. Least-squares line moisture = −0.113 + 10.586 × voltage gives fits 10.47, 14.71, 20.00, 24.23, 30.59 → SSE = 1.24. A hand-drawn line moisture = 10 × voltage + 0.5 gives errors +0.5, −0.5, −0.5, −1.5, −0.5 → SSE = 0.25 + 0.25 + 0.25 + 2.25 + 0.25 = 3.25. The least-squares line wins. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Comparing validation sets of two sizes for an exposure model |
| Industry / Domain | banking |
| Business Problem | A bank validates a loan exposure model on two regional clusters: one with 4 loans and one with 8. A reviewer compared the SSE of both to decide whether the model is worse in the second region. |
| ML Translation | Target = exposure at default in ₹ lakh; supervised regression; two validation sets of different size; per-loan errors are the same in both. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | SSE is a sum, so a larger set simply gives a larger number. It confuses "more loans" with "worse model". |
| Why other metrics are NOT suitable here | MAE also averages and would work but carries no squared-error theory; Max Error again grows with the number of rows; R² alone ignores how big the errors are in rupees. |
| Better alternative (if BAD fit) | MSE or RMSE, which divide by the number of rows and are therefore comparable across sets of different size. |
| Business impact of choosing wrong | A good model is flagged as failing in the larger region, triggering costly re-validation and delays in lending decisions. |
| Small numeric example | Cluster A: 4 loans, every error 2 → SSE = 4 × 4 = 16. Cluster B: 8 loans, every error 2 → SSE = 8 × 4 = 32. SSE says B is twice as bad. MSE = 16/4 = 4 and 32/8 = 4: identical, and RMSE is 2 lakh in both. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Presenting a billing forecast's error to hospital management |
| Industry / Domain | healthcare |
| Business Problem | A hospital finance team built a model to forecast the bill per admission and wants to tell the management committee how accurate it is. An analyst proposed to report SSE on the dashboard. |
| ML Translation | Target = bill per admission in ₹ thousand; supervised regression; five test admissions; the audience is non-technical. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | SSE is in "rupees-squared", which no one can picture, and it also changes simply because more admissions are included. Management cannot act on it. |
| Why other metrics are NOT suitable here | MSE shares the squared-units problem; R² is unitless but does not say how many rupees the forecast is off by; MPE shows direction only, not size. |
| Better alternative (if BAD fit) | MAE or RMSE, which are in rupees: "the forecast is off by about ₹2,400 per admission". |
| Business impact of choosing wrong | A number nobody understands gets ignored, and the forecast is either trusted blindly or rejected without evidence, affecting budgets. |
| Small numeric example | Errors over 5 admissions (₹ thousand): 2, 3, 1, 4, 2 → squares 4, 9, 1, 16, 4 → SSE = 34 (₹ thousand squared, meaningless). MAE = 12/5 = 2.4 → "about ₹2,400 per admission". RMSE = √(34/5) = √6.8 = 2.61 → "about ₹2,600". |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Judging two insurance claim models by SSE alone |
| Industry / Domain | insurance |
| Business Problem | An insurer built the same type of claim-cost model for two portfolios (a small-claims motor book and a large-claims commercial book). A reviewer said both are equally good because both have the same SSE. |
| ML Translation | Target = claim cost in ₹ lakh; supervised regression; five test policies in each portfolio; the portfolios differ greatly in how much claims vary. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | SSE has no sense of scale: the same total error is huge for a book whose claims are all similar and tiny for a book whose claims vary a lot. SSE alone cannot say whether a model is good. |
| Why other metrics are NOT suitable here | MAE, MSE and RMSE have the same missing reference point; Max Error also ignores how variable the target is; MedAE is the same. |
| Better alternative (if BAD fit) | R² (or relative squared error, RRSE), which compares the model's SSE to what simply predicting the average would give. |
| Business impact of choosing wrong | The insurer trusts a model that barely beats guessing, mis-prices one portfolio and loses money on claims. |
| Small numeric example | Portfolio P: actual 40, 50, 60, 70, 80 (total variation 1,000), every error 10 → SSE = 500 → R² = 1 − 500/1,000 = 0.50. Portfolio Q: actual 100, 200, 300, 400, 500 (total variation 100,000), every error 10 → SSE = 500 → R² = 1 − 500/100,000 = 0.995. Same SSE of 500, completely different quality. |

**6. Quick decision rule:** Use SSE when you are fitting or comparing least-squares models on the same rows, or as the raw ingredient for R², F-tests and AIC; avoid it as a headline number for people, across datasets of different size, or on its own as a verdict of "good".

### Mean Squared Error (MSE)

**1. What it measures (plain English):** The average of the squared misses. It is also called L2 loss or quadratic loss. Squaring makes big misses count far more than small ones, and the result is in squared units (rupees-squared), which is why it is mostly a training tool and why RMSE is used for reporting.

`MSE = (1/n) × Σ (yᵢ − ŷᵢ)²`

**2. Intuition:** Think of a spring: stretch it twice as far and the pull is four times as strong. MSE treats a miss the same way, so one big miss pulls the model much harder than many small ones.

**3. Benefits:**

- Smooth and easy to optimise, and it is the default training loss in most tools.
- A model trained on it aims for the mean, so totals add up correctly.
- Matches the maths of the normal (bell-curve) noise model, so classical statistical tests and R² build on it.
- Splits exactly into bias squared plus variance of the errors (how spread out they are), which tells you whether to fix an offset or the features.
- Rightly punishes large errors when large errors really are much costlier.

**4. Limitations / Potential issues:**

- Squared units cannot be read by humans: report RMSE instead.
- Extremely outlier-sensitive: a single typo can dominate the whole value and bend the trained model.
- Doubly scale-dependent: changing rupees to thousands of rupees changes MSE by a factor of a million.
- On targets that range widely (₹99 to ₹90,000), it is dominated by the expensive items and ignores the cheap ones.
- Assumes that cost grows with the square of the miss, which is often not true.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Diagnosing a consistently high tea-yield forecast |
| Industry / Domain | agriculture |
| Business Problem | A tea-estate group forecasts each estate's monthly leaf yield to plan factory procurement. The forecasts look unsettled, and the agronomy head wants to know whether to fix an offset or build better features. |
| ML Translation | Target = leaf yield in tonnes; supervised regression; five estates in a validation check; need to separate systematic error from random scatter. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | MSE splits exactly into bias squared plus the variance of the errors. This shows at once whether the error is a simple offset (fixable in a minute) or random scatter (needs better data). |
| Why other metrics are NOT suitable here | MAE cannot be split this way, so it cannot tell offset from scatter; RMSE is the same information in different units and is better for reporting than for this arithmetic; MedAE gives no split at all. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (report the RMSE of the final model for people). |
| Business impact of choosing wrong | Chasing new features for weeks when a one-line offset correction would have fixed the problem wastes data-science time and delays procurement planning. |
| Small numeric example | Errors (forecast minus actual, tonnes) over 5 estates: +3, +4, +2, +3, +4 → squares 9, 16, 4, 9, 16 = 54 → MSE = 54/5 = 10.8. Mean error = +3.2 → bias squared = 10.24 (95% of MSE). Subtract 3.2 from every forecast → errors −0.2, +0.8, −1.2, −0.2, +0.8 → MSE = 0.56. A simple offset removes almost all the error. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Scheduling penalties for a wind farm's power commitments |
| Industry / Domain | energy |
| Business Problem | A wind-farm operator commits to supplying a certain amount of power for each 15-minute block and is charged a penalty for deviating from the commitment. The penalty slabs climb faster than the size of the deviation. |
| ML Translation | Target = power output in MW per 15-minute block; supervised regression; cost approximately grows with the square of the error (an illustrative assumption of ₹1,000 × error²). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | When the cost climbs faster than the miss, one 17 MW miss is far worse than four 5 MW misses. MSE counts errors in the same way the penalty does, so lower MSE means lower expected penalty. |
| Why other metrics are NOT suitable here | MAE gives the same score to a model of steady small misses and one with a rare big miss, though their penalties differ greatly; MedAE ignores the rare big blocks that cost the most; MAPE gets unstable at low-wind blocks near zero output. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (quote RMSE for reporting). |
| Business impact of choosing wrong | A model chosen by MAE can look equal to a safer model but cost lakhs more in penalties every month. |
| Small numeric example | Model P errors over 4 blocks (MW): 5, 5, 5, 5 → MAE = 5, MSE = 25, penalty = ₹1,000 × (25 × 4) = ₹100,000. Model Q errors: 1, 1, 1, 17 → MAE = 5 (same), MSE = (1 + 1 + 1 + 289)/4 = 73, penalty = ₹1,000 × 292 = ₹292,000. MAE cannot tell them apart; MSE does. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Fuel-use model for a state bus corporation's trips |
| Industry / Domain | logistics |
| Business Problem | A state road-transport corporation models diesel use per trip, to prepare a fuel budget and to explain to the board how much of the variation the model explains. It must choose between a distance-only model and a model that adds passenger load. |
| ML Translation | Target = diesel litres per trip; supervised regression (linear); five hold-out trips shown here; the board wants R² and statistical tests. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | MSE divided by the variance of the target gives one minus R², so it ties the comparison directly to the explained-variation story the board expects, and it is the loss the linear model is trained on. |
| Why other metrics are NOT suitable here | MAE has no direct link to R² or to standard confidence intervals; MedAE with five trips is set by one value; Max Error looks at one trip only. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (convert to RMSE in litres for the board slide). |
| Business impact of choosing wrong | Adopting the weaker model leaves several lakh litres of the annual fuel budget wrongly allocated across depots. |
| Small numeric example | Actual litres over 5 trips: 40, 55, 48, 62, 50 (variance 53.6). Distance-only model forecast 44, 50, 52, 58, 46 → squared errors 16, 25, 16, 16, 16 → MSE = 89/5 = 17.8 → R² ≈ 1 − 17.8/53.6 = 0.67. With passenger load: forecast 41, 54, 49, 60, 51 → squared errors 1, 1, 1, 4, 1 → MSE = 8/5 = 1.6 → R² ≈ 0.97. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Pricing across a marketplace from ₹99 trinkets to ₹90,000 appliances |
| Industry / Domain | e-commerce |
| Business Problem | A marketplace builds a model to suggest listing prices for items ranging from ₹200 to ₹90,000. Sellers judge the suggestion by percentage: being 50% off on a ₹200 item matters to that seller as much as being 50% off on an expensive item. |
| ML Translation | Target = listing price in ₹; supervised regression; strongly right-skewed target; the business cares about relative (percentage) error across the whole range. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Squared rupee errors are dominated by the most expensive items. A model that is badly wrong on cheap items but accurate on the big one scores best, which is the opposite of what sellers want. |
| Why other metrics are NOT suitable here | RMSE has the same pull toward expensive items; MAE is better but still dominated by the high-priced items; plain MPE is only about direction. |
| Better alternative (if BAD fit) | RMSLE (error measured on the logarithm of the price, so it behaves like a percentage error), or MAPE or WAPE. |
| Business impact of choosing wrong | Cheap-item sellers (the majority) get poor price suggestions and stop using the tool, while the expensive-item segment looks falsely perfect. |
| Small numeric example | Items ₹200, 1,000, 5,000, 90,000. Model A is 10% high everywhere (220, 1,100, 5,500, 99,000) → MSE = 20,315,100. Model B is 50% high on the first three and 1% high on the last (300, 1,500, 7,500, 90,900) → MSE = 1,830,000. MSE prefers B. RMSLE: A = 0.095 and B = 0.351 → RMSLE correctly prefers A. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Hospital bill model trained on records with a keying error |
| Industry / Domain | healthcare |
| Business Problem | A hospital trains a bill-prediction model with MSE loss on past admissions. One admission was recorded as ₹12,00,000 instead of ₹12,000 because of a keying slip, and nobody noticed. |
| ML Translation | Target = bill per admission in ₹; supervised regression; one label typo in a small dataset (an outlier); MSE used both to train and to evaluate. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The single typo contributes almost the entire squared error, so the model bends itself around one wrong number and the reported MSE says nothing about everyday performance. |
| Why other metrics are NOT suitable here | RMSE has the same flaw in different units; Max Error only finds the typo; MAPE would also be swamped by the single large actual. |
| Better alternative (if BAD fit) | Fix or flag the typo first; then use a robust loss (Huber, which is gentle on outliers, or MAE) for training and MedAE or MAE for reporting. |
| Business impact of choosing wrong | The model inflates its bill estimates for ordinary patients, which distorts pre-admission quotes and insurance pre-authorisations. |
| Small numeric example | Five admissions, actual bill (₹): 12,000, 15,000, 11,000, 14,000, 1,200,000 (typo); predictions 12,500, 14,500, 11,500, 13,500, 12,500 → errors −500, +500, −500, +500, +1,187,500 → MSE = 282,031,450,000 (the typo is 99.9999% of it); RMSE = ₹531,066 and MAE = ₹237,900, though ordinary errors are ₹500. With the typo fixed to 12,000, MSE = 250,000 and RMSE = ₹500. |

**6. Quick decision rule:** Use MSE as a training loss and for bias-and-variance diagnosis when large errors are truly costlier, totals must add up and the data is clean; avoid it for reporting to non-technical people (use RMSE), for outlier-heavy data and for targets that span orders of magnitude.

### Root Mean Squared Error (RMSE)

**1. What it measures (plain English):** The square root of MSE, which brings the squared units back to normal units. Read it as the typical miss with big misses counted extra. It is always at least as large as MAE, and the gap between the two shows how uneven the errors are. It is the most widely reported regression metric.

`RMSE = √( (1/n) × Σ (yᵢ − ŷᵢ)² )`

**2. Intuition:** A school gives marks for how close a student's shots at a target land, and shots far off the board are penalised much more heavily than slightly-off ones. The final score is expressed back in centimetres.

**3. Benefits:**

- In the target's own units, so it is readable.
- Aims for the mean, so the totals add up, and it keeps all the statistical benefits of MSE.
- Penalises large errors, which is right when large errors are costly.
- If errors are roughly bell-shaped and unbiased, about 68% of predictions fall within one RMSE and about 95% within two.
- RMSE divided by MAE is a free diagnostic of how heavy the tail is.

**4. Limitations / Potential issues:**

- Dominated by outliers, so it can overstate the typical error.
- Scale-dependent: not comparable across datasets or across series of different size.
- Blind to bias, because the sign is lost.
- The 68% and 95% reading is only valid if errors are roughly bell-shaped, and people quote it without checking.
- Not a "typical error" (that is MedAE's job), and it is harder to explain than MAE.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Effort estimates for fixed-price software projects |
| Industry / Domain | IT services |
| Business Problem | An IT-services company estimates person-days for fixed-price projects. A large overrun hurts far more than its size suggests, because it triggers penalty clauses and pulls people off other projects. |
| ML Translation | Target = person-days of effort; supervised regression; small dataset of past projects; cost grows faster than linearly with the overrun. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | RMSE counts one 30-day miss as much worse than three 10-day misses, in line with how the penalty clauses and re-staffing costs behave. It is also in person-days, which managers understand. |
| Why other metrics are NOT suitable here | MAE treats a rare 30-day overrun as only proportionally bad, which understates the real cost; MedAE ignores overruns completely; MAPE underweights big projects, where an overrun costs the most rupees. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Choosing a model with the same average error but rare giant overruns exposes the firm to penalties and margin loss on its biggest contracts. |
| Small numeric example | Two estimating models, 5 projects each, both with MAE = 12 days. Model P is off by 12 on every project → RMSE = 12.0. Model Q absolute errors 10, 10, 5, 30, 5 → MAE = 60/5 = 12, RMSE = √(230) = 15.2 (squares 100 + 100 + 25 + 900 + 25 = 1,150; divided by 5 = 230). RMSE separates them; MAE does not. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Validating a cold-room temperature estimator against a reference thermometer |
| Industry / Domain | healthcare (vaccine and pharmaceutical storage) |
| Business Problem | A pharma distributor estimates cold-room temperature at hard-to-reach points from a few probes. The estimate must agree with a calibrated reference thermometer to within the stated instrument precision of 0.5 °C. |
| ML Translation | Target = temperature in °C; supervised regression; small, carefully measured validation set; errors roughly bell-shaped and unbiased. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | In metrology (the science of measurement), the standard way to express agreement is the root-mean-square difference. RMSE can be compared directly with the instrument's precision in the same unit. |
| Why other metrics are NOT suitable here | MAE is acceptable but the field and its spec sheets use RMSE; MedAE ignores occasional large drift readings; R² does not say how many degrees the estimate is off. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (also keep Max Error as a pass/fail check). |
| Business impact of choosing wrong | An estimator that is not as precise as claimed can let a vaccine lot warm up unnoticed, leading to spoiled stock worth lakhs and a risk to patients. |
| Small numeric example | Errors (°C) over 6 readings: +0.2, −0.3, +0.4, −0.1, +0.3, −0.4 → squares 0.04, 0.09, 0.16, 0.01, 0.09, 0.16 = 0.55 → MSE = 0.0917 → RMSE = 0.30 °C, within the 0.5 °C precision. MAE = 1.7/6 = 0.28 °C. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Sizing leased-line bandwidth for enterprise branches |
| Industry / Domain | telecom |
| Business Problem | A telecom operator sets aside bandwidth for the enterprise branches it serves. Too little capacity at peak causes outages and penalties, so large under-estimates are disproportionately costly. A buffer of two RMSE on top of the forecast is used. |
| ML Translation | Target = peak bandwidth in Mbps per branch link; supervised regression; moderate data; errors roughly bell-shaped after checking residual plots. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Capacity buffers are sized from the spread of the errors, and RMSE is exactly the spread of the errors around zero in Mbps. It also punishes the large shortfalls that cause outages. |
| Why other metrics are NOT suitable here | MAE underestimates the needed buffer because it does not weight the large misses; MedAE would give a buffer that fails on the biggest links; MAPE misjudges small links with low capacity. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (verify the bell-shape assumption on the residuals). |
| Business impact of choosing wrong | A buffer that is too thin causes outages and penalty payments to enterprise clients; one that is too fat wastes leased capacity that costs money every month. |
| Small numeric example | Errors (forecast minus actual, Mbps) over 5 links: +5, −10, +5, −30, +2 → squares 25, 100, 25, 900, 4 = 1,054 → MSE = 210.8 → RMSE = 14.5 Mbps (MAE = 52/5 = 10.4). Buffer = 2 × 14.5 = 29 Mbps. The 30 Mbps shortfall on link 4 just exceeds this, showing the tail is real. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Promising a delivery date to the customer |
| Industry / Domain | e-commerce |
| Business Problem | An online store must show a delivery promise per pincode. A promise that is kept 90% of the time builds trust, while one broken 4 times in 10 drives complaints and refunds. |
| ML Translation | Target = delivery days for a pincode; the decision is a high quantile (the 90th percentile), not the mean; supervised regression on past deliveries. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | RMSE rewards a model that predicts the mean, and promising the mean means being late about half the time. The question the business asks is "by what day are 90% of orders delivered", which RMSE does not answer. |
| Why other metrics are NOT suitable here | MAE targets the median, which is still late half the time; MedAE shares that problem; MAPE is also centred on typical values. |
| Better alternative (if BAD fit) | Pinball (quantile) loss at the 90th percentile, which trains and scores a model directly for the promise level. |
| Business impact of choosing wrong | Missed promises mean customer complaints, refunds, and lost repeat orders for every late parcel. |
| Small numeric example | Ten past deliveries to one pincode (days): 2, 2, 3, 3, 3, 3, 4, 4, 5, 7 → mean = 3.6, 90th percentile = 5.2. Promise 3.6 days → late on the 4, 4, 5 and 7 days = 4 of 10 (40% late). Promise 5.2 days → late only on the 7 = 1 of 10 (10% late). |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Quoting a rainfall forecast band to a crop insurer |
| Industry / Domain | insurance |
| Business Problem | A weather-index crop insurer pays farmers when rainfall falls short of a trigger. The team used the RMSE of the rainfall forecast to quote "95% of forecasts fall within two RMSE" when setting a safety buffer on the trigger. |
| ML Translation | Target = rainfall shortfall in mm per district; supervised regression; errors are mostly small with one big miss, so they are not bell-shaped. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The 68% and 95% rules only hold for bell-shaped errors. One huge miss inflates the RMSE, so the quoted band is far wider than what nearly every district actually experiences. |
| Why other metrics are NOT suitable here | MAE ignores the heavy tail the insurer must still price; Max Error is a single district; MPE shows only bias. |
| Better alternative (if BAD fit) | Empirical percentiles of the absolute error (look directly at the data), or pinball loss for the quantiles needed for the trigger. |
| Business impact of choosing wrong | A too-wide buffer makes the cover unattractive and mis-prices the premium, while quoting a false 95% claim to a regulator is a credibility problem. |
| Small numeric example | Errors (mm) over 10 districts: −4, +3, −2, +5, −3, +2, −5, +4, −3, +40 → squares sum 1,717 → MSE = 171.7 → RMSE = 13.1 mm. Two RMSE = 26.2 mm, and 9 of 10 districts fall within it (90%, not 95%). In fact 9 of 10 fall within just 5 mm. The RMSE band is more than five times wider than what nine districts need. |

**6. Quick decision rule:** Use RMSE when large errors are disproportionately costly, you want the totals to be right and the errors are not wildly outlier-dominated; avoid it when only the typical error matters, when the decision is a quantile, when errors are heavy-tailed, or when comparing across scales.

## Signed Error Metric

### Mean Bias Error (MBE) [Added – not in source file]

**1. What it measures (plain English):** The average of the signed errors, so over-predictions and under-predictions can cancel each other. It tells you whether the model is systematically too high or too low. It is also called mean error or forecast bias. Here the sign convention is prediction minus actual: **MBE above 0 means the model over-predicts on average; below 0 means it under-predicts**. (The source file's mean residual for MPE uses actual minus prediction, which flips the sign, so always state your convention.)

`MBE = (1/n) × Σ (ŷᵢ − yᵢ)`

**2. Intuition:** A kitchen scale that always reads 20 grams heavy is "biased", even if it is otherwise steady. You can see the bias only if you keep the sign of each reading instead of ignoring it, and a one-time correction fixes it.

**3. Benefits:**

- The only measure here that detects a consistent lean in one direction (systematic bias).
- Trivial to compute and in the target's units, so it converts to rupees easily.
- Directly actionable: a known bias can often be subtracted, improving every other error metric for free.
- An early warning for drift in production, since bias often changes before accuracy falls.

**4. Limitations / Potential issues:**

- Positive and negative errors cancel, so an MBE of zero does not mean the model is accurate.
- Must never be reported alone: pair it with MAE or RMSE.
- Scale-dependent: an MBE of +4 lakh means different things for a ₹2 lakh campaign and a ₹200 lakh one; use percentage bias for comparisons.
- Can hide opposite biases in different segments (regions, products) that cancel overall, so compute it by segment.
- Cannot be used as a training loss on its own, since any unbiased model, however poor, scores zero.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Power purchase planning for a town's electricity distribution |
| Industry / Domain | energy |
| Business Problem | A power distribution company (discom) buys electricity a day ahead for a town based on its demand forecast. Surplus power must be resold at a loss of about ₹1.50 per unit, so a forecast that is consistently high is expensive. |
| ML Translation | Target = daily demand in million units (MU); supervised regression; signed error = forecast minus actual; the cost depends on the direction of the error. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Every day the forecast was too high, so the error is a steady lean and not random noise. MBE exposes this and gives the exact number of surplus units bought per day. |
| Why other metrics are NOT suitable here | MAE and RMSE show the size of the miss but not that it is always in the costly direction; MedAE hides the direction; R² gives no rupee value. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (pair it with MAE for size). |
| Business impact of choosing wrong | Without a bias check the discom keeps over-buying, losing lakhs every day on distress resales that a simple correction would avoid. |
| Small numeric example | Actual MU over 5 days: 10.0, 10.4, 9.8, 10.6, 10.2; forecast: 10.5, 10.9, 10.2, 11.0, 10.6 → errors +0.5, +0.5, +0.4, +0.4, +0.4 → sum 2.2 → MBE = +0.44 MU per day (over-forecast). Cost = 0.44 million units × ₹1.50 = ₹660,000 per day. Subtract 0.44 from each forecast → errors +0.06, +0.06, −0.04, −0.04, −0.04 → MAE falls to 0.048 MU. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Under-stocking atta before the festival season |
| Industry / Domain | retail (FMCG distribution) |
| Business Problem | A wholesale distributor of packaged atta forecasts weekly orders in the run-up to a festival. Salespeople say they keep running out of stock, but accuracy reports looked fine. |
| ML Translation | Target = boxes ordered per week; supervised regression; signed error = forecast minus actual; a negative average means chronic under-forecasting. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The accuracy reports showed only size. MBE shows that the forecast leans low almost every week, which matches the stock-outs on the ground. |
| Why other metrics are NOT suitable here | MAE and RMSE gave "average miss of 9 boxes" with no direction; MedAE also has no sign; Max Error highlights only one week. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (also quote total bias as a percentage for the budget). |
| Business impact of choosing wrong | The distributor continues to run out of stock in peak weeks, losing margin and retailer trust that are hard to win back. |
| Small numeric example | Actual boxes over 6 weeks: 120, 150, 100, 180, 140, 130 (total 820); signed errors (forecast minus actual): −12, −8, +3, −15, −10, −6 → sum −48 → MBE = −8 boxes per week (under-forecast); MAE = 54/6 = 9. Total bias = −48/820 = −5.9%. At ₹800 margin per box, the net shortfall of 48 boxes is about ₹38,400 over six weeks. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Detecting drift in a flour-mill moisture sensor |
| Industry / Domain | manufacturing |
| Business Problem | A flour mill uses an online sensor to read grain moisture and compares it with periodic lab checks. The sensor seems to read a bit high, which makes the mill adjust water or drying wrongly and lose weight yield. |
| ML Translation | Target = lab moisture in %; the sensor reading is the prediction; signed error = reading minus lab value; small matched sample of six checks. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The question is whether the sensor leans in one direction, and MBE answers exactly that. Because the errors are all positive, the bias is the whole story, and the fix is a single calibration offset. |
| Why other metrics are NOT suitable here | MAE equals the bias here but would not reveal the direction if errors were mixed; RMSE gives magnitude only; Max Error looks at one check only. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A 0.7-point moisture bias on a 100-tonne batch is about 0.7 tonne of flour yield, or around ₹21,000 at ₹30,000 per tonne, every batch. |
| Small numeric example | Sensor minus lab (moisture points) over 6 checks: +0.9, +0.5, +0.8, +0.4, +1.0, +0.6 → sum 4.2 → MBE = +0.70 (sensor reads high). Subtract 0.70 → remaining errors +0.2, −0.2, +0.1, −0.3, +0.3, −0.1 → MAE drops from 0.70 to 0.20. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Judging ward bed-demand forecasts by MBE alone |
| Industry / Domain | healthcare |
| Business Problem | A hospital compares two bed-demand forecasting models and a manager suggests choosing the one with the MBE closest to zero. The models predict demand for six wards. |
| ML Translation | Target = beds needed per ward; supervised regression; signed error = forecast minus actual; over- and under-forecasts occur in different wards. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MBE lets the +8 and −8 errors cancel, so a model that is wrong by eight beds in every ward scores a perfect zero. It measures bias, not accuracy. |
| Why other metrics are NOT suitable here | Max Error would see only one ward; MedAE alone has no direction; R² hides the size in bed counts. |
| Better alternative (if BAD fit) | MAE or RMSE as the main accuracy metric, with MBE reported next to it, and bias checked ward by ward. |
| Business impact of choosing wrong | Some wards run short of beds while others sit empty, even though the report says "no bias". Patients are turned away and staff are idle. |
| Small numeric example | Model A signed errors over 6 wards: +8, −8, +6, −6, +10, −10 → MBE = 0; MAE = 48/6 = 8 beds; RMSE = 8.2. Model B: +1, −1, +1, −1, +1, −1 → MBE = 0; MAE = 1 bed. MBE rates both as perfect; MAE shows A is eight times worse. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Comparing bias across ad campaigns of very different budgets |
| Industry / Domain | marketing |
| Business Problem | A marketing team forecasts the revenue each campaign will bring and wants to see where the forecasts lean too high. One campaign is worth ₹2 lakh and another ₹200 lakh. |
| ML Translation | Target = campaign revenue in ₹ lakh; supervised regression; signed error = forecast minus actual; two campaigns of very different scale. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MBE in rupees is dominated by the large campaign, so the small campaign's serious over-forecast hardly shows up in the average. The result cannot be compared across scales. |
| Why other metrics are NOT suitable here | MAE and RMSE share the scale problem; MedAE with two campaigns is meaningless; Max Error simply highlights the big campaign. |
| Better alternative (if BAD fit) | Percentage bias (MPE-style) per campaign, with the total bias as a percentage for the portfolio. |
| Business impact of choosing wrong | The team trusts forecasts for small campaigns that are actually 30% too high, and plans spend on revenue that never arrives. |
| Small numeric example | Small campaign: actual 2, forecast 2.6 → error +0.6 lakh (+30%). Large campaign: actual 200, forecast 204 → error +4 lakh (+2%). MBE = (0.6 + 4)/2 = +2.3 lakh, which looks like the big campaign's story. Percentage bias per campaign: +30% and +2% (average +16%); total bias = 4.6/202 = +2.3%, which still hides the small campaign. |

**6. Quick decision rule:** Use MBE when you need to know whether a model leans consistently too high or too low, especially when totals matter, and always report it beside MAE or RMSE; avoid using it alone to judge accuracy, or comparing it across series of different scale.
