# Regression Case Studies, Part 2: Percentage, Relative and Scaled Error Metrics

## Table of Contents

- [Percentage Error Metrics](#percentage-error-metrics)
  - [Mean Absolute Percentage Error (MAPE)](#mean-absolute-percentage-error-mape)
  - [Symmetric Mean Absolute Percentage Error (sMAPE)](#symmetric-mean-absolute-percentage-error-smape)
  - [Weighted Absolute Percentage Error (WAPE / WMAPE)](#weighted-absolute-percentage-error-wape--wmape)
  - [Median Absolute Percentage Error (MdAPE)](#median-absolute-percentage-error-mdape)
  - [Mean Percentage Error (MPE)](#mean-percentage-error-mpe)
- [Relative and Scaled Error Metrics](#relative-and-scaled-error-metrics)
  - [Relative Error Family (RAE, RSE, RRSE)](#relative-error-family-rae-rse-rrse)
  - [Mean Absolute Scaled Error (MASE)](#mean-absolute-scaled-error-mase)
  - [Theil's U Statistics (U1 and U2)](#theils-u-statistics-u1-and-u2)
  - [Root Mean Squared Scaled Error (RMSSE) [Added – not in source file]](#root-mean-squared-scaled-error-rmsse-added--not-in-source-file)

**How to read this part:** each metric has a short explanation, benefits, limitations, five case studies (some good fits, some bad fits) and a one-line decision rule. In the toy numbers, an outlier is one unusually extreme value, bias means errors that lean one way, and a naive forecast is the simple rule that the next value equals the last one. Percentage metrics divide by the actual value; relative and scaled metrics divide by a baseline model's error.

## Percentage Error Metrics

### Mean Absolute Percentage Error (MAPE)

**1. What it measures (plain English):** The average of the absolute percentage errors: how far off each forecast is, as a percent of the actual value, then averaged. Also called Mean Absolute Percentage Error; many teams report accuracy as 100% minus MAPE. It divides by each actual, so it needs actuals that are never zero or close to zero.

`MAPE = (100/n) × Σ abs(yᵢ − ŷᵢ) / abs(yᵢ)`

**2. Intuition:** Like a GPS saying you were 5% off the length of the trip: a 1 km miss on a 10 km trip matters, while the same 1 km miss on a 1,000 km trip hardly does. MAPE judges every miss relative to the size of what was being predicted.

**3. Benefits:**

- Unitless, so you can compare a small series with a large one and average across items.
- Instantly understood by executives ("we were 6% off"), which is why contracts and scorecards are written in it.
- Gives every item or period one equal vote, which is fair when each item has its own owner.
- Trivial to compute and explain; no benchmark model needed.

**4. Limitations / Potential issues:**

- Undefined when any actual is zero and explodes when an actual is close to zero, which is fatal for intermittent demand (many zero periods), new products and counts.
- Asymmetric: an over-forecast can cost more than 100% while an under-forecast is capped at 100%, so a model tuned on MAPE drifts low (biased downward).
- Over-weights small actuals: a 50% miss on a 2-unit item counts as much as a 50% miss on a 20,000-unit item.
- Cannot be used when the target can be negative (profit, temperature in Celsius).
- Improves automatically when you aggregate (store to region, day to month), so always state the level.
- Blind to direction: report a signed measure such as MPE alongside.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Regional quarterly revenue scorecard at a US and Canadian SaaS firm |
| Industry / Domain | Technology / SaaS (finance planning) |
| Business Problem | The finance team of a mid-size subscription-software company forecasts next-quarter revenue for six sales regions (four US, one Canada-wide, one enterprise-accounts team) and wants one plain percentage to put on the board slide. |
| ML Translation | Target: revenue per region in US$ millions (always far above zero); problem type: regression forecasting; six regions of different size; all values positive and well away from zero. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | MAPE gives each region one equal voice and says in percent how far off the plan was. Every region is large, so no actual is near zero and the main weakness of MAPE never shows up. Executives already read percentages, so nothing needs explaining. |
| Why other metrics are NOT suitable here | MAE or RMSE would report a number in dollars (for example $2M) that cannot be compared between a $20M region and a $52M region; R² says nothing about the size of the miss in business terms; WAPE is also acceptable here but hides which small region is struggling because big regions dominate it. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | If a metric in raw dollars were used, the $52M region would dominate and a 15% miss on the $20M region could go unnoticed, so its sales manager would be held to the wrong standard and hiring plans for that team would be set on bad information. |
| Small numeric example | Actual ($M): 48, 31, 36, 24, 52, 20; forecast: 50, 29, 37, 22, 49, 21. Absolute error divided by actual: 2/48 = 4.17%, 2/31 = 6.45%, 1/36 = 2.78%, 2/24 = 8.33%, 3/52 = 5.77%, 1/20 = 5.00%. Sum = 32.50%; divide by 6 → MAPE = 5.42%. Reported as accuracy ≈ 94.6%. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Weekly call volume for a health insurer's member-services line |
| Industry / Domain | Insurance (call-centre operations) |
| Business Problem | A US health insurer must book agent shifts a week ahead for its member-services phone line. Call volume sits between 11,000 and 16,000 a week and the staffing cost scales in direct proportion to volume. |
| ML Translation | Target: weekly call count in thousands (never near zero); problem type: regression / short-horizon forecasting; five test weeks; the forecast is compared with what actually arrived. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A 5% miss in volume means roughly 5% too few or too many agents, so a percentage of the actual volume maps straight onto the staffing decision. With volumes this far from zero, dividing by the actual is safe and stable, and the planning team already uses percentages. |
| Why other metrics are NOT suitable here | MAE in thousands of calls is hard to judge without knowing the typical volume; RMSE punishes the one bad week more but staffing cost is roughly linear in the miss, so that extra punishment is not needed; MASE is more rigorous but harder to explain to the operations director who just wants a percent. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Without a percentage the planners cannot tell whether a 600-call miss is routine or a crisis, so they either over-staff by a few agents every week (wasted payroll) or under-staff and let wait times and complaints rise. |
| Small numeric example | Actual (thousand calls): 12.4, 13.1, 11.8, 14.6, 15.2; forecast: 12, 13.5, 12.3, 14, 15.9. Absolute error / actual: 0.4/12.4 = 3.23%, 0.4/13.1 = 3.05%, 0.5/11.8 = 4.24%, 0.6/14.6 = 4.11%, 0.7/15.2 = 4.61%. Sum = 19.23%; divide by 5 → MAPE = 3.85%. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Monthly passengers per route at a Canadian regional airline |
| Industry / Domain | Airline / transportation |
| Business Problem | A regional airline serving small Canadian and northern US cities forecasts next month's passengers on five routes. Each route manager is judged on their own route, and routes range from about 8,000 to 36,000 passengers. |
| ML Translation | Target: monthly passengers per route (large, positive counts); problem type: regression forecasting; five routes of very different size; each route is scored separately. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Because each route manager is held accountable for their own route, an equal-weight average of percentage misses is the fair scorecard: a small route and a big route each get one vote. All volumes are in the thousands, so MAPE cannot explode. |
| Why other metrics are NOT suitable here | MAE or RMSE in passengers would let the 36,000-passenger route dominate and make small routes look flawless; WAPE would weight by volume, which suits fleet planning but not individual route accountability; sMAPE has several inconsistent definitions and adds nothing here. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A scorecard in raw passengers would hide a weak forecast on the small northern route (a 5% miss is only 400 passengers), so empty or oversold seats on thin routes would go unfixed and the airline would lose revenue on its least profitable flights. |
| Small numeric example | Actual: 8200, 15400, 36000, 22500, 11800; forecast: 8600, 14800, 37500, 21000, 12400. Absolute error / actual: 400/8200 = 4.88%, 600/15400 = 3.90%, 1500/36000 = 4.17%, 1500/22500 = 6.67%, 600/11800 = 5.08%. Sum = 24.69%; divide by 5 → MAPE = 4.94%. (WAPE would be 4.90%, weighted toward the big route.) |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Air-brake chamber spares for a US trucking fleet |
| Industry / Domain | Logistics / trucking (maintenance parts) |
| Business Problem | A long-haul trucking fleet keeps a spare part (an air-brake chamber) in its depots. Demand is intermittent, meaning many weeks have zero use and a few weeks have one to three. The planner proposes reporting forecast accuracy as MAPE. |
| ML Translation | Target: weekly units used of one slow-moving part; problem type: intermittent-demand forecasting; half of the actuals are exactly zero. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MAPE divides by the actual, so every zero week makes it undefined. Dropping those weeks leaves only three weeks to judge and hides the fact that the forecast ordered parts in every empty week. |
| Why other metrics are NOT suitable here | RMSE and MAE are in units and cannot say whether the forecast beats a simple rule; sMAPE returns 200% for any non-zero forecast made in a zero week, so it is noisy; plain R² is meaningless on a handful of tiny values. |
| Better alternative (if BAD fit) | MASE (scaled by how much the part's own demand moves week to week) or WAPE, because both stay defined when actuals are zero and need no patching. |
| Business impact of choosing wrong | The team would report a flattering figure, keep over-ordering a part that mostly sits on the shelf, and tie up cash in depots; or the report would simply fail with a divide-by-zero error and nobody would trust the forecast. |
| Small numeric example | Actual (6 weeks): 0, 2, 0, 1, 0, 3; forecast: 0.5, 1, 0.5, 1, 0.5, 2. MAPE is undefined for the 3 weeks with actual 0. If those weeks are dropped, weeks 2, 4, 6 give 50.0%, 0.0%, 33.3% → mean 27.8% (looks fine, ignores half the weeks). Better alternatives: WAPE = total error 3.5 / total actual 6 = 58.3%; MASE: training weeks 1, 0, 2, 0, 0, 1, 0, 2, 1, 0 have average week-to-week change 1.222, model MAE = 0.583, MASE = 0.48 (better than naive). |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Platelet shipments for a regional blood-supply nonprofit |
| Industry / Domain | Healthcare (blood supply) |
| Business Problem | A nonprofit blood-supply network ships platelet units to three hospitals each week. Platelets expire in days, but running short can put a patient's life at risk. The data scientist is told to tune the forecasting model by minimising MAPE. |
| ML Translation | Target: platelet units needed per hospital per week (50, 100, 150 in the toy data); problem type: regression forecasting; tuning a model against a metric. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MAPE divides by the actual, so a forecast that is too high can cost more than 100% while a forecast that is too low costs at most 100%. A model tuned on MAPE is therefore pushed to forecast low, which is the dangerous direction for blood supply. |
| Why other metrics are NOT suitable here | MAE would pick the middle forecast but ignores which direction the miss goes; RMSE is similar and also direction-blind; sMAPE flips the bias and pushes forecasts up; MPE shows direction but not size, so it is a partner metric, not a replacement. |
| Better alternative (if BAD fit) | WAPE (total error over total demand) to pick the model, with MPE or total bias reported next to it so the direction of error is always visible. |
| Business impact of choosing wrong | Chronic under-forecasting would leave the largest hospital short of platelets week after week, which risks patient safety and forces costly emergency shipments. |
| Small numeric example | Actual units for the three hospitals: 50, 100, 150. Option A always forecasts 50: percentage errors 0/50, 50/100, 100/150 = 0%, 50.0%, 66.7% → MAPE = 38.9%. Option B always forecasts 100: 50/50, 0/100, 50/150 = 100%, 0%, 33.3% → MAPE = 44.4%. MAPE prefers A, which is short by 100 units at the biggest hospital. WAPE: A = (0+50+100)/300 = 50.0%; B = (50+0+50)/300 = 33.3%, so WAPE correctly prefers B. |

**6. Quick decision rule:** Use MAPE when every actual is comfortably above zero, the audience wants a simple percentage, and each item should count equally; avoid it when actuals can be zero or tiny, when you will tune a model on it and care about under-forecasting, or when total volume matters more (use WAPE or MASE instead).

### Symmetric Mean Absolute Percentage Error (sMAPE)

**1. What it measures (plain English):** A variant of MAPE that divides by the average of the actual and the forecast instead of by the actual alone, to reduce MAPE's blow-ups near zero. Also written sMAPE or Symmetric MAPE. In the common M3 form the result lies between 0% and 200%.

`sMAPE = (100/n) × Σ abs(yᵢ − ŷᵢ) / ((abs(yᵢ) + abs(ŷᵢ)) / 2)`

**2. Intuition:** Like measuring a late arrival as a share of the average of the planned and the real trip length: it stays finite when the plan is wild, but the same one-hour slip looks bigger if you arrive early than if you arrive late, so the ruler itself leans one way.

**3. Benefits:**

- Bounded between 0% and 200%, so one terrible forecast cannot make the metric infinite.
- Defined when the actual is zero, as long as the forecast is not also zero.
- Less explosive than MAPE near zero, and unitless.
- Historically important (M3 competition), so it appears in published benchmark tables.

**4. Limitations / Potential issues:**

- Not truly symmetric: for the same absolute miss it penalises under-forecasts more, so models tuned on it drift high (the opposite of MAPE).
- At least three incompatible definitions exist (with or without halving, with or without absolute values), so always state which one you used.
- The denominator contains the forecast, so a model can lower the metric by inflating its forecast.
- Any non-zero forecast on a zero actual scores exactly 200%, regardless of size.
- Hard to explain to a business audience, and superseded by WAPE and MASE in modern practice.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Activation-forecast vendor contract at a Canadian wireless carrier |
| Industry / Domain | Telecom (contract reporting) |
| Business Problem | A Canadian wireless carrier signed a multi-year contract with a forecasting vendor that says accuracy will be reported as sMAPE (M3 competition definition, range 0 to 200%). Province-level monthly new activations are scored under it. |
| ML Translation | Target: monthly new SIM activations per province (hundreds to thousands); problem type: regression forecasting; the metric is fixed by contract and must be reproduced exactly. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The contract names one definition, the scale is bounded at 200% so one bad month cannot blow up the scorecard, and the contract history is already in sMAPE. Here the job is to reproduce an agreed number, not to pick the ideal metric. |
| Why other metrics are NOT suitable here | MAPE would give a different number and break the contract benchmark; WAPE is better statistically but is not what history was recorded in; MASE needs training data and an explanation the commercial team has not agreed to. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Switching metrics mid-contract without agreement would reset the baseline, cause disputes over vendor penalties and could void the service-level payments tied to accuracy. |
| Small numeric example | Actual: 1200, 800, 350, 2100, 150; forecast: 1100, 850, 400, 2000, 120. Average of actual and forecast: 1150, 825, 375, 2050, 135. Error / average: 100/1150 = 8.70%, 50/825 = 6.06%, 50/375 = 13.33%, 100/2050 = 4.88%, 30/135 = 22.22%. Sum = 55.19%; divide by 5 → sMAPE = 11.04% (plain MAPE would be 10.73%). |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — University forecasting lab replicating a published benchmark table |
| Industry / Domain | Education / research |
| Business Problem | A US university forecasting lab wants to show that its new method beats the baseline from earlier papers. Those papers all report sMAPE with the same definition, so the lab must report the same metric to be comparable. |
| ML Translation | Target: values of four benchmark series (toy numbers); problem type: forecasting-method comparison; goal is like-for-like comparison with published sMAPE tables. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Comparability with the literature is the whole purpose. Using the same published definition (average of actual and forecast in the denominator, range 0 to 200%) lets readers line up the new numbers beside the old ones. The lab states the definition in the paper. |
| Why other metrics are NOT suitable here | MASE is the better modern metric but earlier tables do not contain it, so there is nothing to compare against; MAPE has a different scale and cannot be lined up with the published sMAPE values; RMSE depends on the units of each series. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Reporting a different metric would make the comparison unverifiable, reviewers could reject the paper, and the lab's claim of beating the baseline could not be checked. |
| Small numeric example | Actual: 310, 280, 295, 330. New method: 300, 290, 300, 320 → sMAPE = 2.89%. Baseline: 290, 300, 285, 345 → sMAPE = 5.36%. Same definition, so the new method is better by 2.48 percentage points. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Monthly paid-claims forecast at a US property insurer |
| Industry / Domain | Insurance (cash-flow planning) |
| Business Problem | A US property insurer compares two models for monthly paid claims (US$ millions) to decide how much cash to hold. Both models miss by exactly $30M every month, but Model A runs low and Model B runs high. |
| ML Translation | Target: paid claims per month in $M; problem type: regression forecasting; two candidate models with the same size of error in opposite directions. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | sMAPE divides by the average of actual and forecast, so a forecast that is too high enlarges the denominator and gets a smaller penalty. The metric therefore prefers the padded model even though both models miss by the same amount. |
| Why other metrics are NOT suitable here | MAPE would tie them correctly but is itself asymmetric in other situations; RMSE and MAE tie them too but do not show direction; MPE shows the direction but not the size of the miss, so it needs a partner. |
| Better alternative (if BAD fit) | WAPE (or MAE) to measure size, together with MPE or total bias to show direction; the cash decision is then made knowingly rather than by a metric quirk. |
| Business impact of choosing wrong | Choosing the padded model means holding tens of millions in idle cash reserves for months and earning less on that money, all because the metric silently favoured high forecasts. |
| Small numeric example | Actual ($M): 100, 120, 80, 100. Model A (30 too low): 70, 90, 50, 70; Model B (30 too high): 130, 150, 110, 130. Both have MAE = 30. sMAPE A: 30/85, 30/105, 30/65, 30/85 = 35.3%, 28.6%, 46.2%, 35.3% → mean 36.3%. sMAPE B: 30/115, 30/135, 30/95, 30/115 = 26.1%, 22.2%, 31.6%, 26.1% → mean 26.5%. sMAPE says B is 9.8 points better. WAPE: A = 30.0%, B = 30.0% (tie, correct); total bias: A = +30.0% (low), B = -30.0% (high). |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Antivenom vial planning at a rural Canadian hospital |
| Industry / Domain | Healthcare (hospital pharmacy) |
| Business Problem | A rural hospital's pharmacy stocks antivenom vials. Most weeks use zero vials; occasionally one or two. The pharmacist wants to score two forecasting rules with sMAPE because it is bounded and handles zero actuals better than MAPE. |
| ML Translation | Target: vials used per week (mostly 0, sometimes 1 or 2); problem type: intermittent-demand forecasting; two candidate rules forecast 1 vial and 20 vials every week. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | When the actual is zero, sMAPE gives exactly 200% for any positive forecast, whether it is 1 vial or 20. The metric cannot tell a sensible forecast from an absurd one in the very weeks that dominate this series. |
| Why other metrics are NOT suitable here | MAPE is undefined on the zero weeks; MAE and RMSE do separate the two rules but give no sense of whether either beats a simple rule; MPE cannot separate them in size. |
| Better alternative (if BAD fit) | WAPE (total error over total vials used) as the simple choice, or MASE if a training history is available, because both separate the rules clearly. |
| Business impact of choosing wrong | The pharmacy could adopt the 20-vial rule, which looks nearly the same as the 1-vial rule under sMAPE, and let thousands of dollars of expensive vials expire on the shelf. |
| Small numeric example | Actual vials: 0, 0, 2, 0. Rule A forecasts 1 each week: weeks with actual 0 give 200%, actual 2 gives 1/1.5 = 66.7% → sMAPE = 166.7%. Rule B forecasts 20: 200%, 200%, 18/11 = 163.6%, 200% → sMAPE = 190.9% (almost identical to A). WAPE: A = 4/2 = 200%, B = 78/2 = 3900%, so WAPE separates them clearly. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Two vendors, two sMAPE definitions at a US freight broker |
| Industry / Domain | Logistics (freight brokerage) |
| Business Problem | A US freight brokerage runs a bake-off between two forecasting vendors for weekly shipment loads. Vendor X reports sMAPE with the M3 definition (average of actual and forecast in the denominator); Vendor Y divides by the sum without halving. Nobody notices. |
| ML Translation | Target: weekly loads per lane (toy: 200 to 400); problem type: vendor comparison on the same forecast; metric definition differs between the two reports. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | At least three published sMAPE definitions exist and they differ by a factor of two or more. The same forecast therefore looks twice as good under one formula, so a number alone cannot be compared across reports. |
| Why other metrics are NOT suitable here | MAPE has one standard definition but fails near zero; RMSE is in loads, so it is hard to compare across lanes; R² does not say how large the miss is in business terms. |
| Better alternative (if BAD fit) | WAPE or MASE, each with a single standard definition, written into the contract with the formula spelled out. |
| Business impact of choosing wrong | The broker might award a multi-year contract to the vendor who simply used the smaller-looking formula, paying for a service that is no better than the loser's. |
| Small numeric example | Same forecast, same actuals: actual 200, 250, 300, 350, 400, forecast 220, 240, 310, 330, 420. Absolute errors: 20, 10, 10, 20, 20. M3 definition (divide by average of actual and forecast): sMAPE = 5.53%. Without the halving (divide by actual plus forecast): 2.76%. A factor of two for identical forecasts. WAPE = 80/1500 = 5.33% has one definition only. |

**6. Quick decision rule:** Use sMAPE when a contract, benchmark or paper already requires it and the definition is written down; avoid it for new projects, for intermittent or zero-heavy series, or for any model you will tune on it (use WAPE or MASE instead).

### Weighted Absolute Percentage Error (WAPE / WMAPE)

**1. What it measures (plain English):** Total absolute error divided by total actual volume, as a percentage. Also called WMAPE, weighted MAPE, or the MAD/mean ratio. It is the same as MAE divided by the average actual, and is the volume-weighted version of MAPE.

`WAPE = 100 × Σ abs(yᵢ − ŷᵢ) / Σ abs(yᵢ)`

**2. Intuition:** Like asking a grocery store what share of all the food it bought was ordered wrongly, rather than asking each shelf separately: a mistake on the big pallet counts more than a mistake on one jar.

**3. Benefits:**

- Well defined when some actuals are zero, because the denominator is a total.
- Weights items by volume, which matches business cost when cost grows with units.
- Stable: one small actual cannot make it explode.
- Easy to explain as a percentage and gives the familiar accuracy figure of 100% minus WAPE.
- Easy to compute (MAE divided by mean actual) and can be weighted by revenue or margin instead of units.

**4. Limitations / Potential issues:**

- Dominated by high-volume items, so poor accuracy on the long tail of small items is invisible.
- Direction-blind: it cannot see systematic over- or under-forecasting, so pair it with MPE or total bias.
- Improves with aggregation, so always state the level (store, region, national; day, week, month).
- Not in scikit-learn; teams implement it slightly differently (units versus value weighting).
- Comparable across series only when the series are in comparable units.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Surgical-glove usage across five hospitals in a US health system |
| Industry / Domain | Healthcare (supply chain) |
| Business Problem | A US health system buys surgical gloves centrally for five hospitals. The purchasing cost is proportional to the number of cases used, and the system wants to know what share of total glove volume it forecast wrongly. |
| ML Translation | Target: monthly glove cases used per hospital (30 to 420); problem type: regression forecasting; five hospitals of different size; costs scale with volume. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | WAPE divides the total error by the total volume, so a hospital that uses 420 cases counts far more than one that uses 30. That matches how the purchasing budget behaves: a mistake on the big hospital costs more. |
| Why other metrics are NOT suitable here | MAPE gives the 30-case hospital the same weight as the 420-case hospital, so a 17% miss on a tiny site distorts the picture; RMSE is in cases and punishes single big misses, which is not how glove costs behave; R² says nothing about the size of the miss in volume terms. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using MAPE would send the buyer chasing noise at the smallest hospital while a steady 5% miss at the largest quietly leaves too few or too many boxes in the warehouse. |
| Small numeric example | Actual cases: 420, 310, 150, 90, 30; forecast: 400, 330, 140, 100, 25. Absolute errors: 20, 20, 10, 10, 5 = 65 total. Total actual = 1000. WAPE = 65/1000 = 6.5% (accuracy 93.5%). For contrast MAPE = 9.1%, inflated by the 30-case hospital. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Weekly meal counts for an airline caterer at four airports |
| Industry / Domain | Airline / aviation catering |
| Business Problem | An airline's catering contractor loads meals for flights from four airports each week. Food cost, labour and waste all scale with the number of meals, and the airline pays penalties in proportion to meals missed. |
| ML Translation | Target: weekly meals needed per airport (400 to 5,200); problem type: regression forecasting; costs proportional to meals. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Total meals wrongly planned is the quantity the contract is paid on, and WAPE says exactly that as a share of total volume. The hub dominates the total, as it should, since its misses cost the most. |
| Why other metrics are NOT suitable here | MAPE treats the 400-meal airport as equal to the 5,200-meal hub; MAE is in meals and cannot be compared across seasons with different volume; MASE needs a training history and an explanation that the catering manager does not need. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A metric that over-weights the small airport would trigger long meetings about a 20-meal miss while the hub's 200-meal miss, the one that costs real money, passes unnoticed. |
| Small numeric example | Actual meals: 5200, 3100, 900, 400; forecast: 5000, 3300, 1000, 380. Absolute errors: 200, 200, 100, 20 = 520. Total actual = 9600. WAPE = 520/9600 = 5.42%. MAPE = 6.60% (small airport has a big voice). |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Weekly case sales for a regional beverage distributor with zero-sales SKUs |
| Industry / Domain | Retail distribution (consumer goods) |
| Business Problem | A beverage distributor serving grocers in the US Midwest and Ontario forecasts weekly case sales for six products. Two products (a seasonal flavour and a discontinued label) sold nothing this week. |
| ML Translation | Target: cases sold per SKU per week (0 to 240); problem type: regression forecasting at product level; some actuals are exactly zero. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The denominator is the total of all actuals (492 cases), so zero-sales products do not break it. The metric still reads as a plain percentage that the account managers know. |
| Why other metrics are NOT suitable here | MAPE is undefined for the two zero-sales products; sMAPE gives 200% for the product forecast at 5 against actual 0, which is misleading; RMSE needs units and does not give a percentage the vendor can read. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using MAPE would require deleting the zero weeks, so the scorecard would quietly ignore products the model over-ordered, leaving unsold pallets in the warehouse. |
| Small numeric example | Actual cases: 240, 180, 60, 0, 12, 0; forecast: 250, 170, 70, 5, 10, 0. Absolute errors: 10, 10, 10, 5, 2, 0 = 37. Total actual = 492. WAPE = 37/492 = 7.52%. MAPE cannot be computed because two actuals are 0. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Framing-lumber ordering for a homebuilder's four job sites |
| Industry / Domain | Construction (homebuilding materials) |
| Business Problem | A homebuilder orders lumber packages for four job sites. Two forecasting models have the same WAPE. Model A is always 10 packages low; Model B is 10 off but alternates high and low. |
| ML Translation | Target: lumber packages needed per site per week; problem type: regression forecasting; two models with equal absolute error but different error direction. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | WAPE adds up absolute errors, so it cannot see direction. A model that is short every single week looks identical to one that errs both ways and averages out. The builder's real risk is in the direction. |
| Why other metrics are NOT suitable here | MAE and RMSE are equally direction-blind; MAPE is also blind to direction and over-weights the smaller sites; R² would call both models good and say nothing about the one that causes delays. |
| Better alternative (if BAD fit) | WAPE together with MPE or total bias (the signed version), so a model that is always low is flagged immediately. |
| Business impact of choosing wrong | Choosing Model A on a tie would leave every site waiting on lumber every week, with framing crews idle at several hundred dollars per crew-hour and the delivery date slipping. |
| Small numeric example | Actual packages: 40, 55, 30, 75. Model A: 30, 45, 20, 65; Model B: 50, 45, 40, 65. Absolute errors are 10 per site in both, total 40. WAPE = 40/200 = 20.0% for both. Total bias (sum of actual minus forecast over total actual): A = 40/200 = +20.0% (short every week); B = 0/200 = +0.0% (short at 2 sites, surplus at 2). |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Rare-disease drugs hidden behind one big seller at a Canadian specialty pharmacy |
| Industry / Domain | Retail pharmacy (healthcare) |
| Business Problem | A Canadian specialty pharmacy forecasts monthly units for four drugs: one common medicine selling about 1,000 units and three rare-disease drugs selling about 10 each. Missing a rare drug means a patient goes without. Management reports a single WAPE. |
| ML Translation | Target: units dispensed per drug per month (1,000 vs about 10); problem type: regression forecasting; one very large series and three tiny ones. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | WAPE is dominated by the high-volume drug, which has a small 5% miss. The three rare drugs, where the forecast is 70 to 90% wrong, are almost invisible in the total, but they are the ones that cause patient harm. |
| Why other metrics are NOT suitable here | MAPE would show the rare drugs but over-weights tiny values in general; MAE and RMSE are in units, so the 50-unit miss on the big drug hides the tiny drugs; a single R² on a mix like this is dominated by the large series. |
| Better alternative (if BAD fit) | WAPE reported separately by volume band (the rare-drug group gets its own number) plus a per-drug scaled metric such as MASE, so the tail is visible. |
| Business impact of choosing wrong | Patients waiting for rare medicines would go without treatment, causing complaints, emergency transfers between pharmacies and reputational damage, while the dashboard shows 93% accuracy. |
| Small numeric example | Actual units: 1000, 10, 8, 12; forecast: 950, 2, 1, 3; absolute errors: 50, 8, 7, 9 = 74. Overall WAPE = 74/1030 = 7.2% (accuracy 92.8%). Rare drugs only: 24/30 = 80% WAPE (accuracy 20%). Per-drug percentage errors: 5%, 80%, 88%, 75%. |

**6. Quick decision rule:** Use WAPE when business cost scales with volume or value, when some actuals are zero, or when you need one fair accuracy number across many items; avoid it when the small items matter as much as the big ones (add a per-item or banded metric) or when the direction of error is the main risk (add MPE).

### Median Absolute Percentage Error (MdAPE)

**1. What it measures (plain English):** The median of the absolute percentage errors: the typical percentage miss, ignoring a few very large ones. Also written MedAPE. It answers 'half of our predictions are within this percent of the truth'.

`MdAPE = 100 × median(abs(yᵢ − ŷᵢ) / abs(yᵢ))`

**2. Intuition:** Like asking what a typical commute takes by looking at the middle day, not the day a snowstorm closed the highway: one terrible day cannot change the answer.

**3. Benefits:**

- Robust to outliers (a few extreme errors) and to the occasional near-zero actual.
- Unitless and easy to say: half of predictions are within this percent.
- Hard to game or distort with a handful of bad records.
- Pairs naturally with PE10 and PE20 (share of predictions within 10% or 20%), which are very communicable.

**4. Limitations / Potential issues:**

- Hides the tail completely, and in lending, insurance and valuation the tail is where the loss is; always add the 90th or 95th percentile and the maximum.
- Ignores the size of the items: a miss on a 600-thousand-dollar item counts the same as a miss on a 20-thousand-dollar item.
- Still undefined for a zero actual (though only that one observation is dropped).
- Statistically inefficient and not usable as a training loss.
- Can make a model look better than it is if reported alone.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Used-tractor resale values for a rural dealer network in the US Midwest |
| Industry / Domain | Agriculture equipment / used-vehicle sales |
| Business Problem | A dealer network prices used tractors from auction data. Almost all tractors are ordinary models, but a few are rare collector pieces that no model can price. Dealers want to hear how accurate the price tool is for a typical tractor. |
| ML Translation | Target: resale price in US$ thousands; problem type: regression on a right-skewed target (a few very high or odd prices, called outliers); seven toy sales, one of them a rare collector tractor. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | MdAPE is the median of the percentage errors, so the one collector tractor that is 50% off cannot drag the headline number. It answers the dealer's real question: how far off is a normal tractor, as a percent? |
| Why other metrics are NOT suitable here | MAPE would jump to nearly 10% because of one tractor and mislead dealers about the typical case; RMSE and MAE are in dollars and are pulled by the expensive tractor; WAPE is also pulled by the biggest price. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A mean-based metric would show a scary number and dealers would stop trusting a tool that is accurate on 6 of 7 tractors, so the dealers would go back to guessing and leave margin on the table. |
| Small numeric example | Actual ($K): 48, 62, 35, 90, 54, 41, 120; predicted: 50, 60, 36, 88, 52, 42, 60. Percentage errors: 4.2%, 3.2%, 2.9%, 2.2%, 3.7%, 2.4%, 50.0%. Sorted: 2.2%, 2.4%, 2.9%, 3.2%, 3.7%, 4.2%, 50.0%; the middle (4th of 7) value is 3.2% → MdAPE = 3.2%. Compare MAPE = 9.8% (pulled up by the 50% miss). Always add the tail: 90th percentile = 22.5%. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Market salary benchmarks for a Canadian health authority |
| Industry / Domain | Human resources / compensation |
| Business Problem | A large Canadian health authority uses a model to benchmark market pay (C$ thousands) for seven job families. Six are ordinary clinical and admin roles; one is a chief-executive role with a rare, very high salary that the model cannot capture. |
| ML Translation | Target: market salary per role in C$ thousands; problem type: regression on a skewed target with a handful of executive outliers; seven toy roles. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | One executive record is 40% off. A mean percentage would show 8.3% and suggest the whole tool is shaky, while the median shows what HR sees for almost every role. MdAPE is the fair summary of typical accuracy. |
| Why other metrics are NOT suitable here | MAPE is inflated by the executive role; RMSE and MAE would be dominated by the one 170-thousand-dollar miss; WAPE is also pulled up by the executive salary, which is the biggest number in the data. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | If the headline number is inflated by executive pay, the compensation committee may reject a benchmark that is accurate for nearly all staff, delaying fair pay reviews for hundreds of nurses and technicians. |
| Small numeric example | Actual (C$K): 68, 72, 85, 91, 77, 80, 420; predicted: 70, 70, 83, 95, 75, 82, 250. Percentage errors: 2.9%, 2.8%, 2.4%, 4.4%, 2.6%, 2.5%, 40.5%. Sorted: 2.4%, 2.5%, 2.6%, 2.8%, 2.9%, 4.4%, 40.5%; the 4th of 7 is 2.8% → MdAPE = 2.8%. MAPE = 8.3% (inflated by the executive role). |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Typical accuracy of repair-estimate software at a US auto insurer's claim desk |
| Industry / Domain | Insurance (auto claims) |
| Business Problem | A US auto insurer's claim desk uses software to estimate collision repair cost from photos. The desk manager wants a plain statement for adjusters: how close is the estimate for a typical claim? A few claims hide extra damage or end as total losses. |
| ML Translation | Target: final repair cost in US$ per claim; problem type: regression on skewed claim severity (claim size); eight toy claims, one with hidden damage. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | For an everyday statement to adjusters, the median is the honest summary, since half of the claims are within it. A single claim that grows from hidden damage will not distort it. The manager also tracks the 90th percentile to see the tail. |
| Why other metrics are NOT suitable here | MAPE is pulled up by the one hidden-damage claim; RMSE is in dollars and dominated by the 9,800-dollar claim; MedAE says the typical miss in dollars but cannot be compared across claim sizes. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Quoting a mean-based figure would make adjusters distrust software that is within about 4% on most claims, so they would re-estimate by hand and slow every claim down. |
| Small numeric example | Actual ($): 1850, 2400, 3100, 1250, 4200, 2750, 980, 9800; estimate: 1900, 2300, 3250, 1200, 4050, 2900, 1010, 6000. Percentage errors: 2.7%, 4.2%, 4.8%, 4.0%, 3.6%, 5.5%, 3.1%, 38.8%. Sorted: 2.7%, 3.1%, 3.6%, 4.0%, 4.2%, 4.8%, 5.5%, 38.8%. With 8 claims average the 4th and 5th: (4.00% + 4.17%)/2 → MdAPE = 4.08%. MAPE = 8.32%. Share within 10%: 88% (7 of 8). |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Collateral appraisals at a US community lender |
| Industry / Domain | Banking (secured lending) |
| Business Problem | A community lender uses a model to estimate the market value of home-equity collateral. Credit staff are told the model is excellent because its median error is small. The lender loses money whenever collateral is overstated and a borrower defaults. |
| ML Translation | Target: market value of the property in US$ thousands; problem type: regression; ten toy appraisals, eight within about 5% and two overstated by 40% and 45%. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MdAPE only looks at the middle of the error distribution. The two badly overvalued properties, which are exactly where the lender loses money, do not move the median at all, so the metric hides the risk it is supposed to reveal. |
| Why other metrics are NOT suitable here | MAPE would reveal the tail but its average blends it with the good cases and over-weights small values; RMSE shows the tail but is in dollars with no benchmark; MPE shows overall direction but not the extremes. |
| Better alternative (if BAD fit) | Report MdAPE together with the 90th and 95th percentile of the percentage error and the share within 10% and within 20% (PE10, PE20), plus the maximum error, so the tail is visible. |
| Business impact of choosing wrong | The lender could extend loans against collateral that is worth 30 to 45% less than believed, with losses of hundreds of thousands of dollars on the two bad cases and tighter regulatory scrutiny. |
| Small numeric example | Actual ($K): 250, 310, 420, 275, 380, 330, 295, 360, 300, 500; model value: 255, 300, 432, 285, 370, 345, 290, 375, 420, 725. Percentage errors: 2.0%, 3.2%, 2.9%, 3.6%, 2.6%, 4.5%, 1.7%, 4.2%, 40.0%, 45.0%. MdAPE = (3.23% + 3.64%)/2 = 3.43% (looks excellent). But the 90th percentile = 40.5%, the maximum = 45%, and only 80% of values are within 10% (8 of 10). The two overstated properties alone are worth $345K more on paper than in reality. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Show-night costs for a US concert promoter |
| Industry / Domain | Entertainment / live events |
| Business Problem | A concert promoter forecasts the total cost of each show. Four are small club nights (about 20 thousand dollars) and two are arena shows (about 500 thousand dollars each). The finance director asks for the typical accuracy and gets a single MdAPE. |
| ML Translation | Target: total show cost in US$ thousands; problem type: regression on a mixed-size target; six toy shows, where the two big ones carry nearly all the money. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The median is determined by the four small shows (about 5% error). The two arena shows are 40% under-budgeted, and they hold almost all of the dollars, but the median cannot see them. The metric answers a question the finance director is not asking. |
| Why other metrics are NOT suitable here | MAPE would partly show the two big misses but still weights all six shows equally; RMSE and MAE are in dollars with no scale for comparison; MPE shows direction only. |
| Better alternative (if BAD fit) | WAPE (total error over total cost) with total bias, since the money is in the two big shows and both of their misses were under-budgets. |
| Business impact of choosing wrong | The promoter would believe its budgets are within 5% while arena shows run hundreds of thousands of dollars over, eroding profit on the shows that matter most. |
| Small numeric example | Actual cost ($K): 18, 22, 25, 20, 480, 600; forecast: 19, 21, 26, 21, 300, 350. Percentage errors: 5.6%, 4.5%, 4.0%, 5.0%, 37.5%, 41.7%. Sorted: 4.0%, 4.5%, 5.0%, 5.6%, 37.5%, 41.7% → MdAPE = (5.0% + 5.56%)/2 = 5.28%. WAPE = (1+1+1+1+180+250)/1165 = 434/1165 = 37.3%; total bias = +36.7% (driven by the two arena shows, both under-budgeted). |

**6. Quick decision rule:** Use MdAPE when you want a typical-case percentage on skewed data with a few extreme values, and you will also report the tail; avoid it when the tail or the total dollars drive the loss (use percentiles, WAPE or total bias).

### Mean Percentage Error (MPE)

**1. What it measures (plain English):** The average of the signed percentage errors; it keeps the plus and minus signs, so it measures bias (which way and by how much the forecast leans) rather than the size of errors. Also called forecast bias or percentage bias. Here error = actual minus forecast, so positive means under-forecast.

`MPE = (100/n) × Σ (yᵢ − ŷᵢ) / yᵢ`

**2. Intuition:** Like a bathroom scale that always reads two pounds light: each reading may be close, but every reading is wrong in the same direction. MPE tells you the scale leans, and by how much.

**3. Benefits:**

- The only family of metrics here that detects systematic bias.
- One line of code and directly actionable: a known bias can often be corrected by an offset.
- Aggregate version (total bias) reconciles with money totals and is what finance and regulators care about.
- An early warning for drift when tracked over time.

**4. Limitations / Potential issues:**

- Positive and negative errors cancel, so zero does not mean accurate; always report with MAE or RMSE.
- Offsetting segment biases (plus 15% in one region, minus 15% in another) cancel in the total; segment the results.
- The per-observation percentage form inherits MAPE's problems near zero; prefer total bias on mixed-size data.
- The sign convention differs between teams, so state it in every report.
- Cannot be used alone as a training loss.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Quarterly ore-output guidance at a Canadian copper miner |
| Industry / Domain | Mining / resources |
| Business Problem | A Canadian copper miner publishes quarterly output guidance (in thousand tonnes of ore) from its mine plan. Investors suspect the guidance is always a little too rosy. The planning team wants to know if it is systematically high, not just how big the misses are. |
| ML Translation | Target: quarterly ore output; problem type: forecast bias check on six past quarters; sign convention error = actual minus forecast, so a negative value means over-forecast. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | MPE keeps the sign, so consistent optimism shows up as a clear negative number. Magnitude metrics such as MAE would show size only and could not tell optimism from random error. The miner needs to know which way the guidance leans. |
| Why other metrics are NOT suitable here | MAE and RMSE report size but hide direction; MAPE and WAPE are absolute, so they also hide direction; R² would call the plan fine because it follows the pattern of output. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Without a bias check the miner keeps publishing optimistic guidance, repeatedly misses it, and loses investor trust and borrowing room, with a likely share-price drop each quarter. |
| Small numeric example | Actual (kt): 92, 88, 95, 90, 85, 87; guidance: 100, 98, 101, 97, 94, 93. Error (actual − forecast): -8, -10, -6, -7, -9, -6. Percentage errors e/y: -8.7%, -11.4%, -6.3%, -7.8%, -10.6%, -6.9% → MPE = -8.61%. Total bias = -46/537 = -8.57%. Negative means over-forecast: guidance was too high every quarter (forecast total 583 vs actual 537, a ratio of 1.086). MAE = 7.67. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Reserve adequacy by accident year at a US casualty insurer |
| Industry / Domain | Insurance (reserving) |
| Business Problem | A US casualty insurer sets aside money (reserves) for claims not yet fully paid. Regulators care whether the total reserve is adequate, not whether each claim estimate is exact. The actuaries compare reserved amounts with the final cost for five accident years. |
| ML Translation | Target: ultimate claim cost per accident year in US$ millions; problem type: aggregate bias check; sign convention error = actual minus reserved, so positive means reserves were too low. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Offsetting errors across years cancel in the total, and the total is what the balance sheet and the regulator see. Total bias tells whether the company is under-reserved overall, which a magnitude metric cannot tell. |
| Why other metrics are NOT suitable here | MAE and RMSE tell how big the misses are but not whether the company is short of money; MAPE hides direction; MdAPE ignores the larger years where the dollars are. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A persistent under-reserve discovered late means a surprise charge to earnings, a possible regulatory action and a forced capital raise. |
| Small numeric example | Actual ($M): 120, 85, 60, 45, 30; reserved: 110, 80, 58, 41, 28. Error (actual − reserved): 10, 5, 2, 4, 2, total 23. Total bias = 23/340 = +6.76% (reserves 6.76% too low overall). MPE per year averaged = +6.62%. Every year was under-reserved, so this is a pattern, not noise. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Cost model built on log-transformed hospital episode costs |
| Industry / Domain | Healthcare (hospital finance) |
| Business Problem | A US hospital's finance team predicts the cost of a care episode with a model trained on the logarithm of cost (a common trick for right-skewed money data). The budget built from its predictions keeps coming in about 10% under actual spend. |
| ML Translation | Target: episode cost in US$; problem type: regression with a log-transformed target; the exp() of the prediction is used as the dollar forecast; five toy episodes. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A model trained on logs and converted back with exp() predicts the median, not the mean, so on skewed data it is low on average. MPE flags this immediately as a steady positive value, and the fix is simple once you know the size. |
| Why other metrics are NOT suitable here | MAE and RMSE would report an error in dollars without saying it always leans low; MAPE hides direction; R² on the log scale looks excellent while the dollar budget is short. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | The hospital budget would fall millions short every year, forcing mid-year cuts or emergency borrowing, while the model scores well on every magnitude metric. |
| Small numeric example | Actual ($): 4200, 9800, 15500, 6100, 31000; predicted: 3800, 8700, 14100, 5600, 27500. Error (actual − predicted): 400, 1100, 1400, 500, 3500. e/y: 9.5%, 11.2%, 9.0%, 8.2%, 11.3% → MPE = +9.85%; total bias = 6900/66600 = +10.36%. Illustrative fix: multiply every prediction by 1.116 (total actual / total predicted) → total bias +0.0%, MPE -0.57%, and MAE falls from 1380 to 166. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Hourly wind-farm output forecast for a Canadian grid operator |
| Industry / Domain | Energy / power grid |
| Business Problem | A grid operator checks the forecast for a wind farm's output (megawatts) and sees an average error near zero. The control room concludes the forecast is excellent. In reality it swings wildly above and below actual output. |
| ML Translation | Target: hourly output in MW; problem type: forecast evaluation using only a signed metric; four toy hours with errors that are large but alternate in direction. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Errors of plus 30 and minus 30 cancel, so MPE and total bias look near zero while every hour is badly wrong. A bias metric only measures direction, never size. |
| Why other metrics are NOT suitable here | MPE and total bias are blind to size; MAE, RMSE and WAPE do show the size, and are the missing partners; R² does not say how far off each hour is. |
| Better alternative (if BAD fit) | MAE or RMSE (and WAPE for a percentage) reported next to MPE; bias metrics are never meant to be used alone. |
| Business impact of choosing wrong | Operators relying on a near-zero bias would under-schedule backup power in the hours the wind drops, and pay balancing penalties or risk supply shortfalls during the swings. |
| Small numeric example | Actual (MW): 60, 50, 80, 70; forecast: 90, 20, 100, 50. Error: -30, 30, -20, 20, total = 0. Total bias = 0.0%; MPE = +3.39%. Both look close to zero. Better partners: MAE = 25 MW, WAPE = 100/260 = 38.5% (nearly four tenths of output is wrong). |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Seller-level daily sales on a US online marketplace |
| Industry / Domain | E-commerce marketplace |
| Business Problem | A marketplace forecasts next-day units sold for five sellers. Three are tiny sellers (one to two units a day) and two are large (300 and 500 units). The team checks bias with the average of per-seller percentage errors (MPE). |
| ML Translation | Target: units sold per seller per day; problem type: bias check on mixed-size series; per-observation percentages are dominated by the tiny sellers. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Per-observation MPE divides each miss by its own tiny actual. One unit over on a one-unit seller counts as minus 100%, and it swamps the large sellers. The result points the opposite way from the real total. |
| Why other metrics are NOT suitable here | MAPE has the same near-zero weakness; sMAPE is bounded but still treats tiny sellers as equal voices; RMSE and MAE are in units and do not give direction. |
| Better alternative (if BAD fit) | Total bias (sum of errors over sum of actuals), possibly shown by seller-size band, because it is stable and reconciles with total sales. |
| Business impact of choosing wrong | The team would think it over-forecasts heavily, cut inventory and ad spend for the big sellers, and then run short, losing sales on the items that actually carry the revenue. |
| Small numeric example | Actual: 1, 1, 2, 300, 500; forecast: 2, 2, 3, 290, 470. Error (actual − forecast): -1, -1, -1, 10, 30. e/y: -100.0%, -100.0%, -50.0%, 3.3%, 6.0% → MPE = -48.1% (says strong over-forecast). Total bias = 37/804 = +4.6% (says slight under-forecast, which is what really happened in units). |

**6. Quick decision rule:** Use MPE (and total bias) when you need to know which way a forecast leans, such as inventory, reserves, budgets or monitoring drift, and always alongside a magnitude metric; avoid relying on it alone, or on the per-observation percentage form when actuals are tiny or vary hugely in size.

## Relative and Scaled Error Metrics

### Relative Error Family (RAE, RSE, RRSE)

**1. What it measures (plain English):** A family that divides the model's error by the error of a simple baseline (usually predicting the average): RAE uses absolute errors, RSE uses squared errors (and equals 1 minus R²), and RRSE is the square root of RSE. Values below 1 beat the baseline; 0 is perfect.

`RAE = Σ abs(yᵢ − ŷᵢ) / Σ abs(yᵢ − ȳ); RSE = Σ (yᵢ − ŷᵢ)² / Σ (yᵢ − ȳ)²; RRSE = √RSE`

**2. Intuition:** Like grading a student against the class-average guess: a score of 0.24 means the student's mistakes are a quarter of what you would get by always guessing the average.

**3. Benefits:**

- Unitless, so models on different targets can sit on one scoreboard.
- Easy reading: 1 minus the value is the share of baseline error removed.
- Well defined near zero, unlike MAPE.
- RSE is the same information as R², framed as unexplained variation.

**4. Limitations / Potential issues:**

- Depends on the baseline (mean or median), which must be stated.
- The average is a weak baseline for time series with trend or seasonality; use MASE for time series.
- Depends on how spread out the target is: a very homogeneous group makes any model look bad.
- RSE and RRSE inherit the outlier sensitivity of squared errors, and R²'s other weaknesses.
- Out of sample the value can exceed 1, meaning worse than the baseline.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Scrap weight per batch at a US plastic-moulding plant (RAE) |
| Industry / Domain | Manufacturing |
| Business Problem | A plastic injection-moulding plant predicts scrap weight (kg) per production batch from machine settings. Management asks how much better the model is than simply assuming every batch scraps the plant average. |
| ML Translation | Target: scrap kg per batch; problem type: cross-sectional regression (batches have no time order that matters); six toy batches; uses RAE (relative absolute error). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | RAE compares the model's total absolute error with that of a plain predict-the-average rule, so the answer is a ratio the plant manager understands. With no meaningful time order, the average is a fair baseline. |
| Why other metrics are NOT suitable here | MAE in kilograms cannot say whether 1.5 kg is good; MAPE is distorted by small batches; MASE needs a time order and a training series that this data does not have. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A metric in raw kilograms would leave management unable to tell whether the model deserves a place on the line, so the plant could either keep paying for it blindly or abandon a model that removes three quarters of the error. |
| Small numeric example | Scrap (kg): 12, 20, 8, 15, 30, 10; model: 13, 18, 9, 16, 27, 11. Model total absolute error = 9. Plant average = 15.83; baseline error = 36.67. RAE = 9/36.67 = 0.245. The model removes 75.5% of the error of the average rule. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — One scoreboard for length-of-stay and cost models in a Canadian hospital network (RRSE) |
| Industry / Domain | Healthcare (hospital analytics) |
| Business Problem | A Canadian hospital network has two models: one predicts length of stay in days, the other predicts treatment cost in thousands of dollars. The analytics lead needs one scoreboard that says which is relatively more accurate. |
| ML Translation | Target: length of stay (days) and cost (C$ thousands); problem type: two cross-sectional regressions; five toy patients each; uses RRSE (root relative squared error). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | RRSE divides the model's root-mean-square error by the spread of the target, so it is unitless and puts days and dollars on one scale. Each score reads as: our error is this fraction of the natural variation in the data. |
| Why other metrics are NOT suitable here | RMSE is in days for one model and dollars for the other, so the two cannot be compared; MAPE would favour the model with larger values; MAE has the same unit problem. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Comparing raw RMSE numbers (1.07 days vs 7.7 thousand dollars) is meaningless, so the network might spend its improvement budget on the wrong model. |
| Small numeric example | Length of stay: actual 3, 5, 8, 4, 12, predicted 3.5, 4.5, 7, 4.5, 10; Σ(error²) = 5.75, Σ(actual − mean)² = 53.2; RSE = 0.1081; RRSE = √0.1081 = 0.329. Cost: actual 18, 30, 52, 22, 95, predicted 20, 27, 45, 25, 80; Σ(error²) = 296, Σ(actual − mean)² = 4019; RSE = 0.0736; RRSE = 0.271. The cost model is relatively a little better (error is 27% of natural spread vs 33%). |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Corn-yield variation explained for a US farm cooperative (RSE) |
| Industry / Domain | Agriculture |
| Business Problem | A farm cooperative predicts corn yield (bushels per acre) for six fields from soil and weather. The board asks in plain terms: how much of the field-to-field difference in yield is the model still missing? |
| ML Translation | Target: yield per field in bushels per acre; problem type: cross-sectional regression; six toy fields; uses RSE (relative squared error), which equals 1 minus R². |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | RSE is exactly the share of yield variation the model fails to explain, so it answers the board's question directly. A value of 0.20 means the model leaves one fifth of the variation unexplained. |
| Why other metrics are NOT suitable here | RMSE in bushels is not tied to how much yields vary between fields; MAPE does not tell the board how much has been explained; R² is mathematically the same information but is framed as explained, not as missing. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Reporting only an error in bushels could lead the board to ignore a model that clears four fifths of the uncertainty, or to oversell one that clears little. |
| Small numeric example | Actual: 160, 175, 150, 190, 170, 185; predicted: 165, 170, 155, 180, 172, 178. Σ(actual − predicted)² = 228; Σ(actual − mean 171.67)² = 1133.33. RSE = 228/1133.33 = 0.2012. Check: R² = 1 − RSE = 0.7988. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Monthly deposit growth at a US regional bank (RAE) |
| Industry / Domain | Banking (treasury) |
| Business Problem | A regional bank's treasury forecasts monthly total deposits (US$ millions) in a period of steady growth. An analyst reports a good RAE against the 'predict the average' baseline and recommends deploying the model. |
| ML Translation | Target: monthly deposits; problem type: time-series forecasting with a strong upward trend; six toy test months; RAE uses the test-period average as its baseline. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | On a trending series the average is a very weak baseline because it ignores the trend, so any model that follows the trend looks good. The honest benchmark for time series is the naive last-value forecast, and this model is worse than that. |
| Why other metrics are NOT suitable here | MAE alone has no benchmark; MAPE says nothing about beating a naive rule; R² is inflated by the trend in the same way as RAE. |
| Better alternative (if BAD fit) | MASE, which scales the error by the naive last-value forecast's error on training data; here MASE is above 1, correctly saying the model should not be deployed. |
| Business impact of choosing wrong | The bank would deploy a model that is worse than saying 'next month equals this month' and make liquidity decisions on poorer forecasts, with possible costly short-term borrowing. |
| Small numeric example | Test actual ($M): 100, 110, 120, 130, 140, 150; model: 112, 98, 132, 118, 152, 138 (errors of 12 each month, alternating). Σ errors = 72. Average = 125; Σ abs(actual − average) = 90. RAE = 72/90 = 0.80 (looks like 20% better). Training 60, 70, 80, 90 has naive change of 10 per month; model MAE = 12; MASE = 1.20 (20% worse than naive). |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Tower-installation cost models in two provinces at a Canadian telecom (RRSE) |
| Industry / Domain | Telecom (network build) |
| Business Problem | A Canadian telecom has a cost model for installing cell-tower equipment in each province. Province A sites vary widely in cost; Province B sites are all very similar. Management ranks the two models by RRSE to decide where to spend retraining money. |
| ML Translation | Target: install cost per site in C$ thousands; problem type: cross-sectional regression; five toy sites per province; ranking models by relative error. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | RRSE compares the error with the natural spread of the target. In Province B almost all sites cost the same, so the spread is tiny and even a small dollar error looks large against it. RRSE therefore ranks the better-in-dollars model as the worse one. |
| Why other metrics are NOT suitable here | MAPE and WAPE would show the dollar-level picture; plain R² has the same problem as RRSE; RMSE in dollars is correct but is not a ratio. |
| Better alternative (if BAD fit) | RMSE or MAE in dollars (plus WAPE as a percentage of cost), since the budget is set in dollars per site, not in units of spread. |
| Business impact of choosing wrong | Management would send retraining budget to the Province B model, which is already within about 4% of cost, and neglect Province A, whose dollar misses are over twice as large. |
| Small numeric example | Province A: actual 40, 60, 80, 100, 120, errors 6, -10, 9, -8, 7; Σe² = 330, Σ(y−mean)² = 4000; RRSE = 0.287; RMSE = 8.12; WAPE = 10.0%. Province B: actual 78, 80, 82, 84, 86, errors 3, -3, 3, -3, 3; Σe² = 45, Σ(y−mean)² = 40; RRSE = 1.061; RMSE = 3.00; WAPE = 3.7%. RRSE ranks B worse (above 1), but its dollar error is smaller. |

**6. Quick decision rule:** Use RAE, RSE or RRSE for cross-sectional regression when you want to say how much better than predicting the average the model is, or compare models with different units (RAE for linear error, RSE or RRSE for squared error); avoid them for time series with trend (use MASE) or when the decision is in raw dollars (use RMSE or MAE).

### Mean Absolute Scaled Error (MASE)

**1. What it measures (plain English):** The model's average absolute error divided by the average absolute error of a naive forecast ('next value equals the last value') measured on the training data. Also called the Hyndman-Koehler scaled error. A value of 1 means no better than the naive rule; below 1 is better.

`MASE = MAE_test / ((1/(m−1)) × Σ abs(yₜ − yₜ₋₁)), with the denominator taken on the training series`

**2. Intuition:** Like timing a new delivery route against the old rule 'take yesterday's route': 0.75 means you arrive in three quarters of the time the old rule took, and anything above 1 means you should have kept the old rule.

**3. Benefits:**

- Defined when actuals are zero or near zero, because the denominator is one number per series.
- Has a built-in anchor at 1.0: it tells you whether the model beats the naive rule.
- Unitless and comparable across series of very different size; you can average MASE over thousands of series.
- Symmetric: no built-in preference for over- or under-forecasting.
- The seasonal version gives a fair benchmark for seasonal data.

**4. Limitations / Potential issues:**

- Needs a training series with time order, so it does not apply to cross-sectional data (use RAE instead).
- Undefined if the training series is perfectly flat, and huge if it is almost flat.
- Depends on the benchmark chosen (plain versus seasonal naive) and on the training window.
- Less familiar to managers than MAPE, so it needs one sentence of explanation.
- Direction-blind: pair with a bias measure such as MPE.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Landing-gear seal demand at a Canadian aircraft maintenance shop |
| Industry / Domain | Aviation maintenance / logistics |
| Business Problem | A maintenance shop for regional aircraft in Canada stocks landing-gear seals. Demand is lumpy: most months zero, some months one to three. Planners want to know if the forecasting model beats the simple rule 'next month equals this month'. |
| ML Translation | Target: seals used per month; problem type: intermittent-demand time-series forecasting; 12 training months and 4 test months; many actuals are exactly zero. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | MASE divides the model's error by how much the series itself jumps from month to month in the training data, so it stays defined with zeros. A value under 1 means the model beats the naive rule, which is exactly the planner's question. |
| Why other metrics are NOT suitable here | MAPE is undefined because actuals are zero; sMAPE scores any non-zero forecast on a zero month as 200%; RMSE is in seals and gives no benchmark; WAPE works but does not say whether the model beats the naive rule. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using MAPE would stop the report or drop the zero months; the shop could end up trusting a model that is worse than the naive rule, tying up cash in seals that sit on the shelf or grounding an aircraft for a missing part. |
| Small numeric example | Training months: 0, 2, 0, 0, 3, 0, 1, 0, 0, 2, 0, 1. Month-to-month changes: 2, 2, 0, 3, 3, 1, 1, 0, 2, 2, 1 → sum 17 over 11 changes → naive MAE = 1.545. Test actual 0, 2, 0, 1, forecast 0.7, 0.7, 0.7, 0.7; errors 0.7, 1.3, 0.7, 0.3 → MAE = 0.75. MASE = 0.75/1.545 = 0.485: the model removes about 51% of the naive error. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Forecast value add of analyst overrides at a US packaged-food company |
| Industry / Domain | Consumer goods / planning |
| Business Problem | A packaged-food company's planners override the statistical forecast each week with their own judgement. A new VP wants proof that the overrides help, measured against the naive rule 'next week equals last week'. |
| ML Translation | Target: weekly cases shipped for one product family (thousands); problem type: time-series forecast evaluation with three competing forecasts; 8 training weeks, 4 test weeks. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | MASE puts the statistical forecast and the human override on the same scale, with 1.0 meaning no better than the naive rule. That makes forecast value add (does each step improve on the previous one) easy to read. |
| Why other metrics are NOT suitable here | MAPE has no benchmark and favours low forecasts; RMSE is in cases and does not say if the model beats naive; U2 uses the test window for its benchmark and is more sensitive to one big miss. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Without a benchmarked metric the company keeps paying planners to adjust a forecast that they make worse, adding meetings and error. |
| Small numeric example | Training weeks: 100, 104, 98, 107, 103, 110, 105, 112; week-to-week changes 4, 6, 9, 4, 7, 5, 7 → naive MAE = 6.0. Test actual 108, 115, 109, 118. Statistical forecast 106, 112, 111, 114: errors 2, 3, 2, 4 → MAE = 2.75 → MASE = 0.458. Analyst override 112, 120, 104, 124: errors 4, 5, 5, 6 → MAE = 5.00 → MASE = 0.833. Both beat naive (below 1), but the override's MASE is 1.82 times the statistical forecast's: negative value add. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Quarterly lift-ticket revenue at a Canadian ski resort |
| Industry / Domain | Hospitality / tourism |
| Business Problem | A ski resort forecasts quarterly lift-ticket revenue (C$ millions). Revenue follows a strong yearly pattern: big winter quarters, tiny summer quarters. Management asks if the model beats last year's same-quarter figure. |
| ML Translation | Target: quarterly revenue; problem type: seasonal time-series forecasting (seasonal period of 4 quarters); 8 training quarters, 2 test quarters. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Seasonal MASE scales the error by the seasonal-naive rule (same quarter last year), a fair and tough benchmark for seasonal data. Using the plain naive rule would be flattering because summer follows winter by a huge swing. |
| Why other metrics are NOT suitable here | MAPE has no benchmark and treats the small summer quarters as equal to winter; RMSE is in dollars and hard to judge; plain (non-seasonal) MASE is easy to beat on seasonal data and would mislead. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Benchmarking against the wrong naive rule would make a mediocre model look excellent, so the resort might lock in staffing and snow-making budgets on weaker forecasts than it believes. |
| Small numeric example | Training quarters: 14, 3, 4, 11, 15, 3.5, 4.2, 11.8. Seasonal differences (this quarter minus same quarter last year): 1, 0.5, 0.2, 0.8 → seasonal naive MAE = 0.625. Test actual 16, 3.9, forecast 15.2, 3.6; errors 0.8, 0.3 → MAE = 0.55. Seasonal MASE = 0.55/0.625 = 0.88. For comparison, plain naive MAE = 6.114 gives MASE = 0.09, a falsely brilliant score. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Farmland parcel values for a US county assessor |
| Industry / Domain | Government / real estate assessment |
| Business Problem | A county assessor values six farmland parcels (US$ per acre) with a model and wants to report its accuracy. The data analyst proposes MASE because it is the 'recommended' metric. |
| ML Translation | Target: value per acre of a parcel; problem type: cross-sectional regression (parcels have no time order); six toy parcels. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MASE needs a time series, where the naive rule is 'next value equals the last value'. With parcels there is no 'last' parcel, so the denominator depends on the arbitrary order of the list. The same model gets different scores depending on how the file is sorted. |
| Why other metrics are NOT suitable here | MAPE would work but has the small-value weakness; MAE and RMSE have no benchmark; MdAPE is robust but does not benchmark against a baseline. |
| Better alternative (if BAD fit) | RAE (error compared with predicting the average parcel value), or MdAPE and WAPE for a percentage view; they need no time order. |
| Business impact of choosing wrong | A county could publish a valuation accuracy figure that changes whenever someone re-sorts the file, undermining the credibility of tax assessments and inviting appeals. |
| Small numeric example | Actual ($/acre): 5200, 6100, 4800, 7000, 5600, 6400; model: 5000, 6300, 5000, 6600, 5800, 6200; MAE = 233.3. If the list order is used as 'time', the changes between neighbours are 900, 1300, 2200, 1400, 800 → mean 1320 → pseudo-MASE = 0.18. If the same parcels are sorted by value (4800, 5200, 5600, 6100, 6400, 7000) the changes are 400, 400, 500, 300, 600 → mean 440 → pseudo-MASE = 0.53. Same model, two answers. RAE = 1400/3900 = 0.359 (stable). |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Licence-seat counts for an anchor customer of a US SaaS firm |
| Industry / Domain | Technology / SaaS (account management) |
| Business Problem | A SaaS company forecasts the number of paid licence seats at a large, stable customer. The seat count has not changed for months. Account managers want a MASE to show their model is accurate. |
| ML Translation | Target: paid seats per month; problem type: time-series forecasting on a nearly flat series; six flat training months and a short test window. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MASE divides by the naive error from training. When the training series never moves, that error is zero and MASE is undefined; if it moves by just one seat once, the denominator is tiny and any small miss looks enormous. |
| Why other metrics are NOT suitable here | MAPE works here but tells little; MAE in seats is clear and honest; WAPE gives a small clean percentage; sMAPE would also be noisy because values are tiny. |
| Better alternative (if BAD fit) | MAE in seats (plus WAPE as a percentage), reported next to a plain note that the series is flat; MASE can be added only once the series has real movement. |
| Business impact of choosing wrong | The team might report a huge MASE and spend weeks 'fixing' a model that is off by about one seat, or report nothing because the metric errors out. |
| Small numeric example | Training seats: 40, 40, 40, 40, 40, 40; naive changes are all 0 → naive MAE = 0 → MASE undefined (divide by zero). Test actual 40, 40, 42, forecast 40, 41, 41; errors 0, 1, 1 → MAE = 0.67 seats; WAPE = 2/122 = 1.64%. If training had one change (40, 40, 40, 40, 40, 41), naive MAE = 1/5 = 0.2 and MASE = 0.67/0.2 = 3.33, which wrongly says 'worse than naive' for an error under one seat. |

**6. Quick decision rule:** Use MASE for time-series forecasts, especially intermittent or many-series portfolios, when you want to know if the model beats the naive rule; avoid it for data without time order, for flat or near-flat series, or when an audience needs a simple percentage (use WAPE for that).

### Theil's U Statistics (U1 and U2)

**1. What it measures (plain English):** Two related statistics comparing a forecast with a benchmark. U2 is the model's root-mean-square error divided by the naive forecast's (below 1 is better than naive). U1 is a bounded 0-to-1 inequality coefficient that is rarely used now; always say which one you mean.

`U2 = √(Σ (yₜ − ŷₜ)²) / √(Σ (yₜ − yₜ₋₁)²); U1 = √(Σ (yₜ − ŷₜ)²) / (√(Σ yₜ²) + √(Σ ŷₜ²))`

**2. Intuition:** Like comparing your new route to work with 'drive the same way as yesterday', squaring the delays so a single three-hour jam counts much more than three ten-minute ones.

**3. Benefits:**

- U2 has a clear anchor at 1.0: below 1 beats the naive rule.
- Unitless and comparable across series.
- Squaring weights large misses heavily, matching costs that rise faster than the miss.
- Established in econometrics and finance for price and macro forecasts.

**4. Limitations / Potential issues:**

- Two incompatible statistics share the name, so say U1 or U2.
- U1 has no benchmark and depends on the level of the series.
- U2 inherits RMSE's outlier sensitivity in both top and bottom, so one spike can swing it.
- Conventional U2 uses a plain last-value benchmark and computes it on the test window, which flatters seasonal data.
- Undefined if the naive forecast is perfect, and blind to bias.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Monthly sales-tax receipts for a Canadian provincial finance ministry (U2) |
| Industry / Domain | Government finance |
| Business Problem | A provincial finance ministry forecasts monthly sales-tax receipts (C$ billions). A shortfall bigger than the contingency fund forces expensive short-term borrowing, so large misses cost disproportionately more than small ones. |
| ML Translation | Target: monthly receipts; problem type: time-series forecasting, compared with the naive rule 'this month equals last month'; 4 test months; uses Theil's U2. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | U2 compares the model's root-mean-square error with the naive rule's, so squared errors weight the big misses heavily, which matches the ministry's cost structure. A value under 1 means the model beats the naive rule. |
| Why other metrics are NOT suitable here | MASE is linear and treats a 0.5 miss as five times a 0.1 miss, not as 25 times; MAPE has no benchmark and no extra weight on big misses; RMSE alone does not say whether the model beats the naive rule. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Using a linear metric would hide the one costly large miss, and the ministry could keep a model whose biggest errors trigger borrowing at higher interest. |
| Small numeric example | Last training month 4.1. Test actual 4.2, 4, 4.5, 4.3. Model 4.15, 4.1, 4.3, 4.4: errors 0.05, -0.1, 0.2, -0.1, squares sum = 0.0625. Naive 4.1, 4.2, 4, 4.5: errors 0.1, -0.2, 0.5, -0.2, squares sum = 0.3400. RMSE model = √(0.0625/4) = 0.1250; RMSE naive = √(0.3400/4) = 0.2915. U2 = 0.429. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Raw-ingredient price forecasts for a US food manufacturer (U2) |
| Industry / Domain | Food manufacturing (procurement) |
| Business Problem | A US food maker forecasts the weekly price of a key raw ingredient (US$ per tonne) to decide when to lock in fixed-price contracts. For prices, 'next week equals this week' (a random-walk rule) is famously hard to beat, and a big miss on a contract is very costly. |
| ML Translation | Target: weekly price; problem type: financial/commodity time-series forecasting; 4 test weeks; uses Theil's U2 against the persistence (last value) rule. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | U2 asks directly if the model beats the random-walk rule in squared-error terms, which is the standard test for price forecasts. Squaring puts extra weight on large price misses, which hurt the margin most on fixed-price contracts. |
| Why other metrics are NOT suitable here | MAPE has no benchmark and does not weight big misses; MASE is linear and fine for robustness but ignores that big price errors cost disproportionately; U1 has no clear benchmark and depends on the price level. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A model that does not beat last week's price could be used to time contracts, adding purchasing cost with no information gain, and wasting the data science budget. |
| Small numeric example | Last training price 520. Test actual 540, 535, 560, 590. Model 530, 545, 545, 575: errors 10, -10, 15, 15, squares 100, 100, 225, 225 = 650. Naive 520, 540, 535, 560: errors 20, -5, 25, 30, squares sum = 1950. RMSE model = √(650/4) = 12.75; RMSE naive = √(1950/4) = 22.08. U2 = 0.577. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Weekly bunker-fuel spend for a US Gulf tug-and-barge operator (U1) |
| Industry / Domain | Marine transportation |
| Business Problem | A US Gulf-coast tug-and-barge operator forecasts weekly fuel spend (US$ millions). An analyst reports Theil's U1 of about 0.07 and calls the model excellent because U1 is between 0 and 1 and close to zero. |
| ML Translation | Target: weekly fuel spend (around 2.2); problem type: time-series forecasting; 4 test weeks; compares U1 with U2 on the same forecast. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | U1 divides by the size of the actuals and the forecasts themselves, so on a series sitting around 2 it is small no matter what. It has no benchmark, so it cannot say whether the model beats the naive rule. Here the model is actually worse than the naive rule. |
| Why other metrics are NOT suitable here | MAPE also has no benchmark; RMSE in dollars gives no baseline; MASE or U2 do give a benchmark. |
| Better alternative (if BAD fit) | Theil's U2 (or MASE), which compare against the naive rule; U2 above 1 flags the problem immediately. |
| Business impact of choosing wrong | The operator would trust a fuel forecast that is worse than 'same as last week', mis-timing fuel purchases or hedges and overspending by hundreds of thousands of dollars a year. |
| Small numeric example | Last training spend 2.2. Test actual 2.1, 2.35, 2.05, 2.4. Model 2.35, 2.1, 2.4, 2.05; naive 2.2, 2.1, 2.35, 2.05. Model errors -0.25, 0.25, -0.35, 0.35 → RMSE = 0.3041; naive errors -0.1, 0.25, -0.3, 0.35 → RMSE = 0.2669. U1 = √(0.3700) / (√19.8950 + √19.8950) = 0.068 (looks great). U2 = 0.3041/0.2669 = 1.139, which is above 1: worse than naive. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Monthly gas deliveries for a Canadian natural-gas distributor (U2) |
| Industry / Domain | Energy / utilities |
| Business Problem | A gas distributor buys gas on the spot market at a roughly constant price per unit, so costs rise in proportion to the miss. One month the model missed by 12 units because an input feed failed. The planner reports Theil's U2 and wants to scrap the model. |
| ML Translation | Target: monthly deliveries (thousand GJ); problem type: time-series forecasting that swings between 100 and 104; 6 test months; model errors of 1 except one miss of 12. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Squared errors let one large miss dominate U2, even though the model is better in five of six months and better on average. With a linear cost per unit, that extra weight on big misses does not match the business. |
| Why other metrics are NOT suitable here | MAPE has no benchmark; RMSE has the same outlier sensitivity as U2; sMAPE is not benchmarked; MdAPE would hide the one bad month entirely. |
| Better alternative (if BAD fit) | MASE, which uses absolute errors and a training-based benchmark and matches a linear cost; add the single large miss as a separate flagged event. |
| Business impact of choosing wrong | The distributor might drop a model that saves effort in most months, and go back to a manual forecast that is worse most of the time, increasing average procurement cost. |
| Small numeric example | Training: 104, 100, 104, 100, 104, 100, 104; changes are all 4 → naive MAE = 4. Test actual 100, 104, 100, 104, 100, 104; model 101, 103, 101, 103, 101, 92; model errors -1, 1, -1, 1, -1, 12; naive 104, 100, 104, 100, 104, 100, errors all ±4. RMSE model = √((149)/6) = 4.98; RMSE naive = 4.00; U2 = 1.25 (worse than naive). But MAE model = 2.83; MASE = 2.83/4 = 0.71 (better than naive). |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Quarterly reply counts for a US direct-mail marketer (U2) |
| Industry / Domain | Marketing |
| Business Problem | A US direct-mail marketer forecasts quarterly customer replies (thousands), a series with a strong repeating pattern across the four quarters. The analyst reports U2 against last quarter's value and announces the model is far better than naive. |
| ML Translation | Target: quarterly replies (pattern about 20, 8, 6, 16); problem type: seasonal time-series forecasting; 4 test quarters; conventional U2 uses the plain last-value rule. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The conventional naive rule 'same as last quarter' is a poor benchmark for a series with a four-quarter pattern, so almost any model beats it. U2 then looks superb while the real competitor, last year's same quarter, is nearly as good. |
| Why other metrics are NOT suitable here | MAPE has no benchmark; RMSE has no benchmark; plain MASE with a non-seasonal naive rule has the same flaw; U1 is not benchmarked. |
| Better alternative (if BAD fit) | Seasonal MASE (or U2 computed against the seasonal-naive rule, clearly labelled), so the model must beat last year's same quarter. |
| Business impact of choosing wrong | The marketer would overstate the model's value, cut the budget for a better seasonal benchmark and be surprised when campaign capacity planning is no better than last year's rule. |
| Small numeric example | Last training quarter 16. Test actual 21, 9, 6, 17; model 20, 8.5, 6.5, 16.5; persistence naive 16, 21, 9, 6. RMSE model = 0.661; RMSE persistence = 8.646; U2 = 0.077 (looks superb). Seasonal naive (same quarter last year) = 20, 8, 6, 16: RMSE = 0.866; ratio = 0.764, about ten times less impressive. |

**6. Quick decision rule:** Use Theil's U2 when cost grows faster than the miss, a random-walk or last-value rule is the right competitor (prices, macro series), and you want a benchmark anchored at 1; avoid it for seasonal data without a seasonal benchmark, for series with one-off spikes under a linear cost (use MASE), and never use U1 alone.

### Root Mean Squared Scaled Error (RMSSE) [Added – not in source file]

**1. What it measures (plain English):** The squared-error sibling of MASE: the model's root-mean-square error divided by the root of the mean squared change in the training series (the in-sample naive forecast's mean squared error). Used to score many series at once, as in the M5 competition's weighted version (WRMSSE). Below 1 beats the naive rule.

`RMSSE = √( ((1/n) Σ (yₜ − ŷₜ)²) / ((1/(m−1)) Σ (yₜ − yₜ₋₁)²) ), with the denominator taken on the training series`

**2. Intuition:** Like grading a new delivery route against 'repeat yesterday's route', but with a penalty that grows with the square of each delay: two-hour delays count four times as much as one-hour delays, and the grade is scaled by how erratic that route usually is.

**3. Benefits:**

- Puts series of very different size and volatility on one scale, so averaging across thousands of series is fair.
- Anchor at 1.0 (naive rule), and defined with zeros because the denominator is one number per series.
- Squared errors punish large misses, matching costs like stockouts, overflow or overcrowding.
- Can be weighted by revenue or volume to show business impact.

**4. Limitations / Potential issues:**

- Needs a training history with time order; not for cross-sectional data.
- Sensitive to outliers in both the numerator and the denominator, so a spike in the training window can inflate the denominator and flatter every model.
- Harder to explain to a business audience than WAPE or MAPE.
- Undefined for a perfectly flat training series, and unstable for near-flat ones.
- Direction-blind: pair with a bias measure.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Two forecasting vendors scored on a small and a large seller at a US online marketplace |
| Industry / Domain | E-commerce marketplace |
| Business Problem | A US online marketplace trials two forecasting vendors on two products: a niche item (about 20 units a day) and a best-seller (about 8,000 a day). It wants one fair score that does not let the best-seller swamp the niche item. |
| ML Translation | Target: daily units sold; problem type: scoring forecasts across series of very different scale; each series has its own training history; uses RMSSE per series, then the average. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | RMSSE scales each series' squared error by that series' own naive difficulty, so a miss of a few units on the niche item counts about as much as a miss of a few hundred units on the best-seller. The average across series is then fair. |
| Why other metrics are NOT suitable here | RMSE averaged across series is dominated by the best-seller; MAPE and WAPE weight differently and say nothing about beating naive; MASE is also scaled, but linear, so it does not punish the occasional large miss that causes a stockout. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Averaging raw RMSE would crown the vendor who is good on the best-seller and poor on the niche item, and the marketplace would choose the wrong vendor for most of its catalogue. |
| Small numeric example | Niche: training 18, 22, 19, 24, 20, 23, naive mean squared change = 15; test 21, 25, 22. Vendor A 17, 28, 26: RMSE 3.70, RMSSE = 3.70/√15 = 0.955; Vendor B 21, 25, 21: RMSE 0.58, RMSSE 0.149. Best-seller: naive mean squared change = 236000; Vendor A RMSE 100.0, RMSSE 0.206; Vendor B RMSE 402.1, RMSSE 0.828. Average RMSE: A 51.8, B 201.3 (A wins). Average RMSSE: A 0.580, B 0.488 (B wins; A was poor on the niche item). |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Daily ridership on one route for a Canadian city transit agency |
| Industry / Domain | Public transit |
| Business Problem | A city transit agency forecasts daily riders for a route so it can schedule extra buses. One badly under-forecast day means overcrowded buses and passengers left at stops, so big misses hurt much more than small ones. |
| ML Translation | Target: daily riders; problem type: time-series forecasting; 6 training days, 3 test days; uses RMSSE, scaled by the in-sample naive mean squared change. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Squaring gives extra weight to the big under-forecast days, matching the cost of overcrowding. Dividing by the in-sample naive error gives the anchor at 1.0: below 1 beats the rule 'tomorrow equals today'. |
| Why other metrics are NOT suitable here | MASE is linear and treats a 200-rider miss as only twice a 100-rider miss; MAPE has no benchmark and does not weight large misses; plain RMSE in riders cannot be compared with other routes. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A linear metric might rate two models equally when one of them occasionally leaves 300 passengers stranded, so the agency could keep the worse model and face complaints and lost ridership. |
| Small numeric example | Training 4200, 4350, 4100, 4500, 4400, 4600: day-to-day changes 150, 250, 400, 100, 200, squares mean = 59000, root = 242.9. Test actual 4550, 4300, 4700, forecast 4500, 4400, 4500: errors 50, −100, 200; squares 2500, 10000, 40000, mean = 17500, RMSE = 132.3. RMSSE = √(17500/59000) = 0.545 (better than naive). MASE on the same data = 0.530. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Daily milk intake across three plants of a US dairy cooperative |
| Industry / Domain | Agriculture / dairy |
| Business Problem | A dairy cooperative forecasts daily milk intake (thousand litres) at three plants of very different size. Overflow or spoilage when a plant is over-run is costly, so large misses matter, and managers want one score weighted by plant size. |
| ML Translation | Target: daily intake per plant; problem type: multi-series forecasting scored with a volume-weighted RMSSE (the idea behind the M5 competition's WRMSSE); 5 training days and 2 test days per plant. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | RMSSE puts the three plants on one scale, so the weighting is a clear business choice (here by test volume) rather than an accident of units. Squared errors reflect that a big overflow day costs more than two small misses. |
| Why other metrics are NOT suitable here | Raw RMSE is dominated by the largest plant; MAPE would weight plants equally regardless of volume; MASE scales fairly but is linear, so it understates the cost of overflow days. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Without scaling, the smallest plant's problems would be invisible and spoilage there could continue unnoticed, costing the co-op tens of thousands of dollars of milk per month. |
| Small numeric example | RMSSE per plant: Plant 1 (training 50, 52, 49, 53, 51) = 0.550; Plant 2 (training 20, 22, 19, 21, 20) = 0.667; Plant 3 (training 8, 9, 8, 10, 9) = 0.535. Test volumes 106, 44, 19 (total 169). Simple average RMSSE = 0.584; volume-weighted RMSSE = (106×0.550 + 44×0.667 + 19×0.535)/169 = 0.579. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Daily claim counts at a US homeowners insurer after a hailstorm in the training data |
| Industry / Domain | Insurance (claims operations) |
| Business Problem | A US homeowners insurer forecasts daily new claims. Its training history includes one hailstorm week with a huge claim spike. A model is declared excellent on RMSSE and approved for staffing decisions. |
| ML Translation | Target: daily claim count; problem type: time-series forecasting; training series contains one extreme spike (an outlier); 4 normal test days. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | RMSSE's denominator squares the day-to-day changes in training, so the hailstorm jump and fall (about 170 and 155 claims) dominate it. The denominator becomes huge and any model looks excellent, even one that is off by 40% on ordinary days. |
| Why other metrics are NOT suitable here | MAPE and sMAPE have no benchmark; MASE is also scaled by the spike but less severely; RMSE alone does not say if the model beats naive. |
| Better alternative (if BAD fit) | WAPE (total error over total claims) for a simple view, and RMSSE recomputed with a calm training window (storm weeks flagged and excluded) so the benchmark reflects normal days. |
| Business impact of choosing wrong | The insurer would staff to a model that is wrong by about 40% on normal days, causing long phone queues or paid idle staff, while believing it is highly accurate. |
| Small numeric example | Training 30, 28, 33, 200, 45, 31, 29, 32: naive mean squared change = 7450. Test actual 31, 29, 35, 30, forecast 45, 16, 48, 17, errors 14, 13, 13, 13 → RMSE = 13.26. RMSSE = 13.26/√7450 = 0.154 (looks superb). Without the storm days, training 30, 28, 33, 31, 29, 32 gives naive mean squared change = 9.2 and RMSSE = 4.37: worse than naive. WAPE = 53/125 = 42.4%. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Board report on branch cash withdrawals at a Canadian credit union |
| Industry / Domain | Banking (credit union) |
| Business Problem | A Canadian credit union forecasts daily cash withdrawals at a branch (C$ thousands). The board asks for a one-line accuracy statement. The analyst proposes RMSSE because it is technically rigorous. |
| ML Translation | Target: daily withdrawals; problem type: time-series forecasting; 6 training days and 3 test days; audience is non-technical board members. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | RMSSE says the root-mean-square error is a fraction of the typical day-to-day swing in training. That is correct but not something a board can act on or compare with an accuracy target. It also needs a training window to explain. |
| Why other metrics are NOT suitable here | MAPE reads as a percentage but has weaknesses; MASE has the same communication problem, though it is linear; plain RMSE in dollars gives no benchmark. |
| Better alternative (if BAD fit) | WAPE for the board ('about 97% accurate'), with MASE or RMSSE kept in the technical appendix. |
| Business impact of choosing wrong | A board unable to interpret the figure may ignore it, mis-set cash buffers, or tie executive pay to a number nobody understands. |
| Small numeric example | Training 310, 295, 320, 305, 330, 300: naive mean squared change = 520. Test actual 315, 325, 300, forecast 305, 320, 310: errors 10, 5, 10; RMSE = 8.66. RMSSE = 8.66/√520 = 0.380. Board-friendly: WAPE = 25/940 = 2.7%, i.e. about 97% accurate. |

**6. Quick decision rule:** Use RMSSE when you score many time series of different scale at once and large misses cost disproportionately; avoid it when the training window contains one-off spikes (clean it first), when the audience wants a plain percentage (use WAPE), or when a linear cost fits (use MASE).
