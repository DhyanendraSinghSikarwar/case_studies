# Regression Case Studies, Part 3: Log-Based and Goodness-of-Fit Metrics

## Table of Contents

- [Log-Based Error Metrics](#log-based-error-metrics)
  - [RMSLE (Root Mean Squared Logarithmic Error)](#rmsle-root-mean-squared-logarithmic-error)
  - [MSLE (Mean Squared Logarithmic Error)](#msle-mean-squared-logarithmic-error)
  - [Log Accuracy Ratio and Median Symmetric Accuracy (MdSA)](#log-accuracy-ratio-and-median-symmetric-accuracy-mdsa)
- [Variance-Explained Metrics](#variance-explained-metrics)
  - [R² (Coefficient of Determination)](#r²-coefficient-of-determination)
  - [Adjusted R²](#adjusted-r²)
  - [Explained Variance Score](#explained-variance-score)
- [Correlation and Agreement Metrics](#correlation-and-agreement-metrics)
  - [Pearson Correlation (r)](#pearson-correlation-r)
  - [Spearman Correlation (ρ)](#spearman-correlation-ρ)
  - [Concordance Correlation Coefficient (CCC, Lin's CCC)](#concordance-correlation-coefficient-ccc-lins-ccc)

**How to read this part:** each metric starts with a short plain-English explanation, then five real-style business cases (some where the metric is the right choice, some where it is the wrong one). Each case ends with a small toy calculation you can check by hand. Most scenarios are set in Europe and the UK, so money is in euros or pounds.

## Log-Based Error Metrics

### RMSLE (Root Mean Squared Logarithmic Error)

**1. What it measures (plain English):** RMSLE measures the typical size of your miss in _ratio_ terms rather than in raw units, so a 10% miss on a small item counts about the same as a 10% miss on a large one. It takes the log of every actual and predicted value (after adding 1, so zeros are allowed), then computes the usual root-mean-square error on those logs. Also called root mean squared log error.

`RMSLE = sqrt((1/n) × Σ (ln(1 + yᵢ) − ln(1 + ŷᵢ))²)`

**2. Intuition:** Think of judging a marathon runner and a sprinter by percentage of their personal best rather than by seconds: being 5% slow means the same thing to both, even though the raw seconds differ hugely.

**3. Benefits:**

- Measures relative error, so it works when the target spans orders of magnitude (for example 20 units to 4,000 units).
- Much less dominated by a few huge values than RMSE (an outlier is a single extreme value that distorts an average).
- Accepts zeros thanks to the "+1" shift, unlike MAPE.
- Penalises under-prediction more than over-prediction for the same absolute miss, which suits cases where running short is the costly mistake.
- Approximately unitless: exp(RMSLE) − 1 reads as a typical percentage miss (for example 0.093 means about 9.8%).

**4. Limitations / Potential issues:**

- Needs non-negative actuals and predictions; a negative value gives "not a number" and a model that predicts small negatives must be clipped.
- Unusable for targets that can go negative (profit, price spreads, temperature).
- The asymmetry is a defect if over-prediction is the expensive mistake (perishable stock, over-provisioned capacity).
- The "+1" shift distorts small counts (0 to 5), so it is not a clean relative error there.
- Training on log values and converting back gives the median, so totals come out biased low if you need sums to reconcile.
- Raw values such as 0.26 mean little to managers until translated with exp(RMSLE) − 1.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Opening stock for a new-season knitwear launch |
| Industry / Domain | e-commerce (fashion) |
| Business Problem | A UK online fashion retailer must decide the opening stock of every new-season item before launch, from niche items selling tens of units to bestsellers selling thousands; running out of a niche item hurts the brand as much as running out of a bestseller. |
| ML Translation | Target = units sold in the first four weeks per item; regression; positive, right-skewed (a few very large values, many small ones) whole numbers spanning two orders of magnitude; model trained on log1p of units. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Every item is judged by its percentage miss, so the 20-unit item counts as much as the 4,000-unit item; logs squeeze the bestsellers so they cannot drown the rest; the extra penalty on under-prediction matches the stock-out worry. |
| Why other metrics are NOT suitable here | RMSE would be set almost entirely by the few bestsellers and ignore the niche range; MAE has the same large-item bias in a gentler form; MAPE explodes for tiny items and rewards under-forecasting because a low forecast can never be more than 100% wrong. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Tuning on RMSE steers the team to perfect the few bestsellers while most items in the range are bought wrongly, leaving cash tied up in unsold stock that needs end-of-season markdowns. |
| Small numeric example | Actual units 20, 150, 800, 4,000; forecast 30, 120, 900, 3,200 → RMSE: errors +10, −30, +100, −800; mean square (100 + 900 + 10,000 + 640,000) / 4 = 162,750; RMSE = 403 units, and 98% of the squared error is the 4,000-unit item → RMSLE: squared log gaps 0.152, 0.049, 0.014, 0.050; mean 0.0661; root = 0.257 → exp(0.257) − 1 ≈ 29% typical miss, and the 20-unit item (50% too high) supplies 57% of the score versus about 0.02% under RMSE. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Reserving open commercial property claims |
| Industry / Domain | insurance |
| Business Problem | A mid-size European commercial insurer must set aside cash (a reserve) for each open property claim, from small water-damage claims of about €1,500 to large fires of €250,000; reserving too little is the dangerous mistake. |
| ML Translation | Target = final settled claim cost in euros; regression; strictly positive, heavily right-skewed; a few very large claims; model trained on log1p of cost. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The reserving question is "how many percent off are we, claim by claim", which is a ratio question; for the same euro miss, RMSLE charges more when the reserve was too low, which is the direction the regulator cares about. |
| Why other metrics are NOT suitable here | RMSE is controlled by the handful of giant claims and says almost nothing about the small ones; MAPE caps under-reserving at 100% error and so flatters models that reserve too low; MAE reports a euro figure that is meaningless across a €1,500 to €250,000 range. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A metric that flatters low reserves leads to a shortfall in solvency capital and a restated profit; a metric that ignores small claims leaves thousands of claims systematically mis-reserved. |
| Small numeric example | Actual claims €1,500; €8,000; €40,000; €250,000; forecast €1,200; €9,500; €31,000; €210,000 → log gaps +0.223, −0.172, +0.255, +0.174 → squares sum 0.1746; mean 0.0437; root = 0.209 → exp(0.209) − 1 ≈ 23% typical miss; RMSE = €20,514 with 95% of the squared error from the €250,000 claim → asymmetry check: actual €40,000, forecast €31,000 (€9,000 low) gap 0.255 versus forecast €49,000 (€9,000 high) gap 0.203, so the low miss is charged 26% more. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Sizing platforms from yearly station passengers |
| Industry / Domain | transport (rail infrastructure) |
| Business Problem | A national rail infrastructure planner estimates yearly passengers for each station, from small rural halts of about 3 thousand to major hubs of 25 million, to decide staffing and platform upgrades. |
| ML Translation | Target = yearly passengers in thousands; regression; positive and extremely skewed across four orders of magnitude; hundreds of stations. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A planner cares about getting every station roughly right in percentage terms; RMSLE gives each station a fair voice and turns the result into one portable "typical percentage miss" number. |
| Why other metrics are NOT suitable here | RMSE is decided by a handful of hubs, so the halts are invisible; R² would look excellent because the hub variance dominates the total, hiding bad halt forecasts; MAPE is unstable for the smallest halts. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Judging on RMSE or R² could approve a model that is 30% off at dozens of small stations, causing under-sized shelters and staffing at the places where growth is fastest. |
| Small numeric example | Actual (thousand passengers) 3; 45; 800; 25,000; forecast 4; 38; 880; 21,000 → log gaps −0.223, +0.165, −0.095, +0.174 → squares sum 0.1165; mean 0.0291; root = 0.171 → exp(0.171) − 1 ≈ 18.6% typical miss → RMSE = 2,000 thousand, with 99.96% of the squared error from the hub, and R² = 0.965 looks excellent despite a 33% miss at the halt. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Day-ahead power prices that dip below zero |
| Industry / Domain | energy (wind generation) |
| Business Problem | The trading desk of a Danish wind-farm operator forecasts next-day power prices in euros per megawatt-hour (€/MWh) to decide when to sell and when to switch turbines off; in windy, low-demand hours the price can be negative. |
| ML Translation | Target = hourly day-ahead price in €/MWh; regression; continuous and able to go negative; spikes in both directions. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The log of a negative number does not exist, so RMSLE cannot be computed for exactly the days the desk cares about most; clipping negatives to zero would hide them rather than score them. |
| Why other metrics are NOT suitable here | MAPE breaks near zero prices and is undefined at exactly zero; MSLE and RMSLE share the same negative-value problem; R² says nothing about the size of the euro miss the desk will actually lose. |
| Better alternative (if BAD fit) | MAE (and RMSE) in €/MWh: they work for negative values, are in the desk's own money units, and show directly how far off the forecast is on a negative-price day. |
| Business impact of choosing wrong | A model never scored on negative-price hours may not warn the desk to curtail; a 100 MW farm left running for one hour at −€15 pays about 100 × €15 = €1,500 for that hour alone. |
| Small numeric example | Actual €/MWh −15; 8; 45; 90; 140; forecast −5; 12; 40; 100; 120 → RMSLE: day 1 needs ln(1 + (−15)) = ln(−14), which does not exist, so the result is "not a number" → MAE: absolute errors 10, 4, 5, 10, 20; sum 49; 49 / 5 = 9.8 €/MWh; RMSE = 11.3 €/MWh, and both include the negative day. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Ordering short-life biologic vials for hospitals |
| Industry / Domain | pharma (distribution) |
| Business Problem | A Dutch pharmaceutical wholesaler orders temperature-sensitive biologic vials with a 14-day shelf life; an expired vial is a €400 write-off, while a shortage is fixed by a €60 emergency courier per vial. |
| ML Translation | Target = vials needed per hospital per week; regression on non-negative whole numbers with a clear cost for each direction of error. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | RMSLE charges more for under-prediction than over-prediction of the same size, which nudges the model to over-order, and here over-ordering is the expensive direction. |
| Why other metrics are NOT suitable here | RMSE and MAE treat a vial too many and a vial too few as equal, which does not match a 6.7 to 1 cost ratio; MAPE also favours low forecasts; R² ignores costs entirely. |
| Better alternative (if BAD fit) | A cost-weighted absolute error, which is the pinball (quantile) loss at the 13% quantile because 60 / (60 + 400) ≈ 0.13: it charges each vial in the costly direction about 6.7 times more, matching the real money. |
| Business impact of choosing wrong | Systematically ordering too many vials turns into write-offs of €400 each; a hospital that over-orders by 50 vials a week loses €20,000 a week in expired stock. |
| Small numeric example | Actual need 100 vials → forecast 150 (50 too high): log gap ln(101/151) = −0.402, cost 50 × €400 = €20,000 → forecast 50 (50 too low): log gap ln(101/51) = +0.683, cost 50 × €60 = €3,000 → RMSLE rates the shortage 1.7 times worse while money says the surplus is 6.7 times worse → pinball loss at 0.13: surplus 0.87 × 50 = 43.5, shortage 0.13 × 50 = 6.5, ratio 6.7 matching the costs. |

**6. Quick decision rule:** Use RMSLE when the target is positive, right-skewed, spans orders of magnitude, and a percentage miss is what matters (ideally with running short as the worse failure); avoid it when the target can be negative, when over-prediction is the expensive error, or when sums must reconcile.

### MSLE (Mean Squared Logarithmic Error)

**1. What it measures (plain English):** MSLE is RMSLE before the square root: the average of the squared gaps between the logs of the actual and predicted values (after adding 1). It ranks models exactly like RMSLE but is in squared log units, which is hard to read. It is mainly used as a training loss or a model-selection score. Also called mean squared log error.

`MSLE = (1/n) × Σ (ln(1 + yᵢ) − ln(1 + ŷᵢ))²`

**2. Intuition:** MSLE is the raw "points scored" total that a judge adds up behind the scenes; RMSLE is the tidy final mark you actually announce to the audience.

**3. Benefits:**

- Smooth and easy to optimise, so it works directly as a training objective (for example in gradient-boosted trees).
- Gives every item a fair voice, whatever its size.
- Same ranking of models as RMSLE, with no extra computation.
- Available as a ready-made scoring option in common libraries.

**4. Limitations / Potential issues:**

- Squared log units are not interpretable; a manager cannot read 0.0156.
- Same restrictions as RMSLE: no negative values, and small counts are distorted by the "+1".
- Predicts closer to the median than the mean, so totals can be biased low.
- Penalises under-prediction more, which is wrong when over-stocking is the costly error.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Training a depot parcel-volume model |
| Industry / Domain | logistics |
| Business Problem | A pan-European parcel carrier trains a gradient-boosted model (many small decision trees added one after another) to forecast next-day parcels per depot, from small town depots of 50 parcels to hubs of 5,000 and more. |
| ML Translation | Target = parcels per depot per day; regression; positive, right-skewed counts in the tens to thousands; MSLE used as the training loss. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | As a loss, MSLE makes a 10% miss cost almost the same at every depot size, so the model learns the small depots as seriously as the hubs; it is smooth, so training is stable. |
| Why other metrics are NOT suitable here | Plain squared error as a loss lets the biggest depots dominate training; absolute error as a loss ignores relative size too; MAPE as a loss is lopsided and unstable for small depots. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A model trained on squared error would be tuned for the hubs and would mis-staff small depots, causing late deliveries in towns that have the least spare capacity. |
| Small numeric example | Actual parcels 50, 500, 5,000; forecast 10% high: 55, 550, 5,500 → squared log gaps 0.0087, 0.0090, 0.0091; MSLE = 0.0090, every depot counts almost equally → squared errors 25; 2,500; 250,000; MSE = 84,175, with 99% of it from the biggest depot. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Choosing a model for district waste collection rounds |
| Industry / Domain | public sector (municipal waste services) |
| Business Problem | A city council compares two candidate models that forecast weekly household waste in tonnes for districts that range from a small rural ward to a dense city centre, to size collection rounds. |
| ML Translation | Target = weekly tonnes per district; regression; positive and spanning two to three orders of magnitude; model selection through cross-validation scored with negative MSLE. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The council wants every district's round sized within a few percent, so the better model is the one with smaller percentage misses everywhere, which is what MSLE rewards. |
| Why other metrics are NOT suitable here | MSE and RMSE would pick the model that is best for the city centre even if the rural ward is badly mis-sized; MAE has the same flaw; R² hides how big the misses are for small districts. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Picking the wrong model sends a half-empty lorry to some wards and an overflowing one to others, raising fuel cost and complaint counts. |
| Small numeric example | Actual tonnes 12, 90, 640, 4,100; model A forecasts 20, 100, 700, 4,000 (relative misses +67%, +11%, +9%, −2%); model B forecasts 13, 80, 560, 4,500 (+8%, −11%, −13%, +10%) → MSE: A = 3,441, B = 41,625, so MSE picks A → MSLE: A = 0.0624, B = 0.0114, so MSLE picks B, which is within about 13% everywhere. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Explaining roaming-revenue accuracy to the finance director |
| Industry / Domain | telecom |
| Business Problem | A European mobile operator forecasts monthly roaming revenue per country and the finance director asks "how wrong are we, in plain words?" before approving the forecast for the board pack. |
| ML Translation | Target = monthly roaming revenue in €k per country; regression; positive and skewed across countries of very different size. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MSLE is in squared log units, so a value such as 0.0156 means nothing to a finance director; it is fine for training but poor for reporting. |
| Why other metrics are NOT suitable here | RMSE in euros is dominated by the biggest country; MAE also hides the small markets; plain R² gives no sense of the size of the miss. |
| Better alternative (if BAD fit) | RMSLE translated with exp(RMSLE) − 1 into a typical percentage miss, or MAPE when there are no zeros: both are statements a director can act on. |
| Business impact of choosing wrong | An uninterpretable number leads to either blind approval or an unnecessary rebuild; in the board pack it can cause the wrong forecast confidence to be quoted to investors. |
| Small numeric example | Actual €k 400; 2,500; 9,000; 30,000; forecast 360; 2,900; 8,000; 34,000 → squared log gaps 0.0110, 0.0220, 0.0139, 0.0157; MSLE = 0.0156 (meaningless to a director) → RMSLE = 0.125 → exp(0.125) − 1 ≈ 13.3% typical miss → MAPE: 10%, 16%, 11.1%, 13.3%; mean 12.6%. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Branch profit forecasts with loss-making branches |
| Industry / Domain | banking |
| Business Problem | A regional bank forecasts next-quarter net profit per branch in €k; several branches make a loss, and head office wants to know which ones to review. |
| ML Translation | Target = quarterly net profit in €k; regression; continuous, can be negative; small sample of branches. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The log of a negative profit does not exist, so MSLE cannot score the loss-making branches; dropping or clipping them would remove the cases head office cares about most. |
| Why other metrics are NOT suitable here | MAPE breaks near zero profit and gives huge values for a break-even branch; RMSLE and MSLE share the negative-value problem; R² alone does not show the euro size of the miss. |
| Better alternative (if BAD fit) | MAE and RMSE in €k, which handle negatives and express misses in money, plus a signed average error to check for bias. |
| Business impact of choosing wrong | A loss-making branch whose forecast was never scored may be left unreviewed for another quarter, costing the bank the loss it could have cut. |
| Small numeric example | Actual €k −120; 30; 80; 200; forecast −90; 40; 70; 260 → MSLE: ln(1 + (−120)) = ln(−119) does not exist, so no result → MAE: absolute errors 30, 10, 10, 60; sum 110; 110 / 4 = 27.5 €k; RMSE = 34.3 €k, with the loss-making branch included. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Annual water bills that must add up to revenue |
| Industry / Domain | utilities (water) |
| Business Problem | A UK water company predicts each customer's annual bill in pounds with a model trained on log values, and finance needs the sum of predicted bills to match expected revenue. |
| ML Translation | Target = annual bill in £ per customer; regression; positive and right-skewed; predictions come from converting the log-scale output back to pounds. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MSLE looks excellent because each bill is only about 5% to 17% low, but converting back from logs gives the median, so every bill is a little low and the total is clearly short. |
| Why other metrics are NOT suitable here | RMSLE and MSLE hide the total shortfall; MAPE shows only an average percentage and not the sum; R² can stay high while the sum is off. |
| Better alternative (if BAD fit) | A Gamma or Tweedie deviance with a log link (it models the mean directly), plus a signed percentage error on the total to check reconciliation. |
| Business impact of choosing wrong | A revenue plan built from the predicted total is short by about 11%; on a £500 million annual billing base that is a £57 million hole in the budget. |
| Small numeric example | Actual £200; 400; 800; 1,600; 3,200 (total £6,200); forecast £190; 330; 790; 1,380; 2,800 (total £5,490) → MSLE = 0.0158, which looks excellent → total error (5,490 − 6,200) / 6,200 = −11.5%, a £710 shortfall on five customers; MAE = £142. |

**6. Quick decision rule:** Use MSLE as a training loss or tuning score when relative error matters on a positive, right-skewed target; avoid it as a reporting number for managers, for targets that can be negative, or when totals must reconcile.

### Log Accuracy Ratio and Median Symmetric Accuracy (MdSA)

**1. What it measures (plain English):** The log accuracy ratio is ln(predicted / actual): positive when you over-predict, negative when you under-predict, and exactly symmetric (doubling gives +0.693, halving gives −0.693). MdSA takes the median of its absolute values and turns it back into a percentage ("the typical prediction is within X% of the truth"). SSPB (Symmetric Signed Percentage Bias) keeps the sign to show whether you lean high or low.

`L = ln(ŷ/y)`

`MdSA = 100 × (exp(median(abs(ln(ŷᵢ/yᵢ)))) − 1)`

`SSPB = 100 × sign(M) × (exp(abs(M)) − 1), where M = median(ln(ŷᵢ/yᵢ))`

**2. Intuition:** It is like measuring how many "zoom steps" off a map is: zooming in 2× and zooming out 2× are the same distance in opposite directions.

**3. Benefits:**

- Genuinely symmetric: over- and under-prediction by the same factor get the same size of penalty (MAPE is not symmetric).
- Median-based, so a few bad rows do not spoil the typical-case figure.
- Unbounded in both directions, so there is no artificial cap on how wrong a forecast can be.
- Reads as a percentage after exponentiating, and pairs with SSPB for a matching bias figure.

**4. Limitations / Potential issues:**

- Needs strictly positive actuals and predictions; there is no "+1" rescue, so zeros break it.
- Unfamiliar outside a few scientific fields and not in mainstream libraries, so you must define it.
- The median hides the tail: a few large misses (even ones worth a lot of money) are invisible, so report a high quantile or a total-based metric beside it.
- The exponentiating step confuses people on first sight.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Forecasting river flow at flood-warning gauges (uses MdSA) |
| Industry / Domain | public sector (environmental monitoring) |
| Business Problem | A national environment agency forecasts peak river flow in cubic metres per second at gauge stations from small tributaries to large rivers, to trigger flood warnings; both false alarms and missed floods have a cost. |
| ML Translation | Target = peak river flow (m³/s); regression; strictly positive, spanning more than one order of magnitude; the metric used is MdSA. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Flow forecasts are naturally judged by ratio, a forecast of half is as bad as a forecast of double, and MdSA treats them alike; the median gives the typical gauge, and a separate tail check can cover rare big floods. |
| Why other metrics are NOT suitable here | MAPE punishes over-forecasts harder than under-forecasts, which would quietly bias the model towards missing floods; RMSE is set by the biggest rivers; plain MAE in m³/s cannot compare a tributary with a major river. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A metric that favours low forecasts risks missed flood warnings; one that favours high forecasts causes false alarms and costly unnecessary evacuations. |
| Small numeric example | Actual m³/s 250; 800; 1,500; 2,600; 4,200; 9,000; forecast 270; 720; 1,650; 2,400; 4,600; 7,000 → absolute log ratios 0.077, 0.105, 0.095, 0.080, 0.091, 0.251; sorted 0.077, 0.080, 0.091, 0.095, 0.105, 0.251; median = (0.091 + 0.095) / 2 = 0.0931 → MdSA = exp(0.0931) − 1 ≈ 9.8%; SSPB = −0.15%, so no real lean; MAPE = 11.2%; the 9,000 m³/s river was forecast 22% low, a tail case the median does not show. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Are valuers over-valuing office rents? (uses the log accuracy ratio and SSPB) |
| Industry / Domain | real estate (commercial property) |
| Business Problem | A European property lender compares valuers' estimated rents with the rents actually achieved on newly let offices, to see whether valuers lean high; loans are set as a share of the valuation. |
| ML Translation | Target = achieved annual rent in €/m²; compare estimate with actual; strictly positive and wide-ranging; uses the log ratio ln(estimate / actual) and SSPB for direction. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A ratio-based measure tells the lender "valuers are about 10% high" regardless of whether the rent is €90 or €450, and the sign tells it the direction; median-based SSPB is not thrown off by one odd letting. |
| Why other metrics are NOT suitable here | Mean percentage error is not symmetric (a valuation twice the rent looks like +100%, half looks like −50%); mean error in €/m² is dominated by prime central offices; RMSLE gives size but not direction. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | If the lender lends 70% of valuation and valuations are 10% too high, the effective loan-to-value is really 0.70 × 1.10 = 77%, leaving less cushion than the lender thinks. |
| Small numeric example | Achieved rent €/m² 120; 200; 310; 450; 90; valuation 138; 220; 340; 495; 99 → log ratios +0.140, +0.095, +0.092, +0.095, +0.095; median 0.0953 → SSPB = exp(0.0953) − 1 = +10.0% (valuers lean 10% high); MdSA also 10.0% → symmetry check: doubling gives +0.693 and halving gives −0.693, while MAPE gives 100% and 50%. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Monthly data traffic per mobile mast with two corrupted feeds (uses MdSA) |
| Industry / Domain | telecom |
| Business Problem | A European mobile operator forecasts monthly data traffic in terabytes for each mast, to plan upgrades; two masts have faulty data feeds that produce wild forecasts, and planners want the typical mast judged fairly. |
| ML Translation | Target = monthly traffic in TB per mast; regression; strictly positive and skewed; two entries with corrupted records that act as outliers. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Because it uses the median, five good masts decide the figure (MdSA 7.3%) instead of two broken ones, and the corrupted masts are flagged separately by their huge log ratios (+0.69 and −2.41). |
| Why other metrics are NOT suitable here | MAPE is pulled up to 32% by the two bad rows (100% and 91% errors); RMSE is dominated by the 400 TB mast; RMSLE, being a mean of squares, is inflated by the two corrupted rows. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (but also list the two flagged masts for data repair) |
| Business impact of choosing wrong | A mean-based score would tell planners that the model is 30% to 60% off and could stop a perfectly good model from being used for upgrade planning. |
| Small numeric example | Actual TB 12; 35; 60; 110; 180; 260; 400; forecast 13; 33; 64; 118; 171; 520; 36 → absolute log ratios 0.080, 0.059, 0.065, 0.070, 0.051, 0.693, 2.408; sorted 0.051, 0.059, 0.065, 0.070, 0.080, 0.693, 2.408; median (the 4th of 7) = 0.0702 → MdSA = exp(0.0702) − 1 ≈ 7.3% → MAPE = 32.0%. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Replacement bus services on rail lines with many zero days (uses MdSA) |
| Industry / Domain | transport (rail operations) |
| Business Problem | A UK rail operator forecasts how many replacement bus services each line will need per day during engineering works; on many line-days no replacement is needed at all. |
| ML Translation | Target = replacement bus services per line per day; regression on small non-negative counts with many exact zeros. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The ratio ŷ/y divides by zero when the actual is zero and the log of zero does not exist, so MdSA cannot score the quiet days; dropping them would hide the model's habit of ordering buses that are not needed. |
| Why other metrics are NOT suitable here | MAPE also divides by zero; RMSLE with its "+1" shift distorts small counts; MdAPE has the same divide-by-zero problem. |
| Better alternative (if BAD fit) | WAPE (total absolute error divided by total actual), which is stable with zeros, or MASE when comparing against a simple rule such as "same as last week". |
| Business impact of choosing wrong | Every unneeded replacement bus booked costs money (assume €450 a service); three needless services in the example is €1,350 that a zero-blind metric never sees. |
| Small numeric example | Actual services 0; 0; 3; 12; 25; 0; 8; forecast 1; 0; 4; 10; 30; 2; 7 → MdSA: three of the seven actuals are zero, so ln(ŷ/0) is undefined and the metric cannot be computed → WAPE: absolute errors 1, 0, 1, 2, 5, 2, 1; sum 12; total actual 48; 12 / 48 = 25%. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Capital projects where one big overrun hides in the median (uses MdSA) |
| Industry / Domain | public sector (municipal infrastructure) |
| Business Problem | A city council forecasts the final cost of its capital projects, six of which are small and one is a major bridge refurbishment; the finance committee needs to know whether the capital budget will hold. |
| ML Translation | Target = final project cost in €m; regression; strictly positive and very skewed; a handful of projects with one dominant project. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MdSA reports the typical project, and five of six are close, so it reads about 4%; but the budget is driven by the single large project that was forecast 30% too low, which the median does not see. |
| Why other metrics are NOT suitable here | MAPE counts every project equally and gives an average percentage with no link to the total budget; RMSLE shrinks the large project's weight through the log; MAE gives no relative comparison between projects. |
| Better alternative (if BAD fit) | WAPE and the signed percentage error on the total budget (both are weighted by euros), with a high quantile of the log ratio beside MdSA to expose tail projects. |
| Business impact of choosing wrong | The committee approves the budget thinking the forecast is "4% accurate" when it is €8.9m short, which then has to be found from reserves or other services. |
| Small numeric example | Actual €m 2.0; 3.5; 1.2; 4.0; 2.5; 30.0 (total 43.2); forecast 2.1; 3.4; 1.25; 4.15; 2.4; 21.0 (total 34.3) → absolute log ratios 0.049, 0.029, 0.041, 0.037, 0.041, 0.357; sorted 0.029, 0.037, 0.041, 0.041, 0.049, 0.357; median = 0.0408 → MdSA ≈ 4.2% → WAPE: absolute errors sum 9.5; 9.5 / 43.2 = 22.0%, and the total is €8.9m low. |

**6. Quick decision rule:** Use MdSA (with SSPB for direction) when all values are strictly positive and you want a genuinely symmetric, outlier-proof "typical percentage miss"; avoid it when zeros exist, when totals in money matter, or when the tail is the real risk.

## Variance-Explained Metrics

### R² (Coefficient of Determination)

**1. What it measures (plain English):** R² says how much better your model is than a lazy baseline that always predicts the average. 1 means perfect, 0 means no better than the average, and below 0 means worse than the average (possible on new data). Often described as "percent of variation explained".

`R² = 1 − Σ(yᵢ − ŷᵢ)² / Σ(yᵢ − ȳ)²`

**2. Intuition:** Imagine a forecaster who always says "tomorrow will be the average day". R² is the share of that forecaster's mistakes that you managed to remove.

**3. Benefits:**

- Unitless, so it can compare targets measured in different units.
- Anchored at 0, so it has a built-in "is this model worth having?" answer.
- Easy to explain ("the model explains 88% of the variation").
- Negative values are a useful red flag for broken models.

**4. Limitations / Potential issues:**

- In-sample R² never falls when features are added, even random noise, so it cannot choose between models (see Adjusted R²).
- Says nothing about bias (consistently too high or too low) on new data, and nothing about whether the shape of the model is right.
- A few extreme points (an outlier is one extreme value) can dominate it.
- Depends on the spread of the target: a group with a narrow range of values shows a low R² for the same errors.
- For time series, the average is a very weak baseline, so R² looks flattering.
- Not comparable across different transformations of the target (raw versus log).

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Calibrating a UV spectrometer for drug potency |
| Industry / Domain | pharma (quality control laboratory) |
| Business Problem | A pharmaceutical quality lab in Ireland fits a calibration line that turns spectrometer readings into drug concentration (mg/L) using six standard solutions of known strength; the line must be trusted before batches are released. |
| ML Translation | Target = known concentration in mg/L; regression; a straight-line fit on a controlled, low-noise measurement with six points. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | In a clean, controlled linear calibration the question is "how much of the variation in concentration does the reading explain", and R² answers it directly with an anchored scale; lab procedures commonly set an R² acceptance level (often about 0.99 or above). |
| Why other metrics are NOT suitable here | RMSE alone is in mg/L with no built-in benchmark for "good enough"; MAPE blows up on the smallest standards; Pearson r would not reveal an offset or slope error (although for an in-sample straight-line fit it equals the square root of R²). |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A calibration accepted without a proper fit check can release a batch with the wrong strength, causing recalls and regulator action; an unnecessarily strict check delays release. |
| Small numeric example | Known 2, 4, 6, 8, 10, 12 mg/L; predicted 2.1, 3.9, 6.2, 7.8, 10.1, 11.9 → residual squares 0.01, 0.01, 0.04, 0.04, 0.01, 0.01; sum 0.12 → mean 7; squared distances from the mean 25, 9, 1, 1, 9, 25; sum 70 → R² = 1 − 0.12 / 70 = 0.9983. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Does the loss-given-default model beat the portfolio average? |
| Industry / Domain | banking |
| Business Problem | A European retail bank models loss given default (the share of the loan lost after a borrower defaults) and the risk committee asks whether the model adds anything over simply assigning every defaulted loan the portfolio average. |
| ML Translation | Target = loss given default in percent; regression on a very noisy outcome; judged on a held-out sample (data the model never saw during fitting). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | R² compares the model with the "always the average" rule, which is exactly the committee's question; a modest positive value on held-out data is a real success in this noisy field, and a negative value would be an immediate warning. |
| Why other metrics are NOT suitable here | MAE or RMSE alone have no built-in comparison with the average rule; MAPE explodes for loans with near-zero loss; Pearson r would not show that the model is badly scaled. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | If the model does not beat the average, provisions set with it are no better than a flat rate, yet the bank pays the cost of running and validating a complex model. |
| Small numeric example | Actual loss % 10, 25, 40, 55, 70, 85 (mean 47.5; squared distances sum 3,937.5); model 35, 25, 60, 35, 55, 60 → errors −25, 0, −20, 20, 15, 25; squares sum 2,275 → R² = 1 − 2,275 / 3,937.5 = 0.422, so the model removes 42% of the average-rule error; MAE = 17.5 points. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — How much of paper strength do the line sensors explain? |
| Industry / Domain | manufacturing (paper) |
| Business Problem | A Swedish paper mill predicts the tensile strength of finished reels from line sensors and asks how much of the reel-to-reel variation the sensors explain, to decide whether to cut slow laboratory strength tests. |
| ML Translation | Target = tensile index in Nm/g; regression; continuous, moderate noise, well spread target values; evaluated on eight held-out reels. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The decision is about "share of variation explained", the target is well spread and not dominated by one point, and the process is controlled, which is where R² is easy to read and trust. |
| Why other metrics are NOT suitable here | MAE and RMSE are in Nm/g with no yardstick for whether that is good; MAPE is fine here but says nothing about variation explained; MdAPE hides the few reels that matter for quality complaints. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Dropping lab tests on a model that explains too little lets weak reels reach customers (returns and complaints), while keeping tests for a model that explains most of the variation wastes lab time. |
| Small numeric example | Actual 52, 58, 61, 66, 70, 75, 79, 84 (mean 68.125; squared distances sum 838.875); predicted 55, 57, 64, 63, 72, 72, 82, 81 → errors −3, 1, −3, 3, −2, 3, −3, 3; squares sum 59 → R² = 1 − 59 / 838.875 = 0.930, so sensors explain 93% of strength variation; MAE = 2.6 Nm/g. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Comparing the repair-cost model across two vehicle segments |
| Industry / Domain | insurance (motor) |
| Business Problem | A European motor insurer sees a lower R² for fleet-leasing sedans (repair costs tightly clustered) than for mixed commercial vehicles (costs widely spread) and wants to decide which segment needs model work. |
| ML Translation | Target = repair cost per claim in €; regression run separately in two segments with very different spreads of the target. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | R² divides by the spread of the target within each segment, so the same euro error looks bad where values are bunched together and great where they are widely spread; it says nothing about which segment the model really handles worse. |
| Why other metrics are NOT suitable here | RMSE alone is in euros and is the same in both segments, which is fair but gives no sense of relative size; Pearson r has the same spread problem as R²; explained variance does too. |
| Better alternative (if BAD fit) | WAPE (total absolute error divided by total actual) or MAE per segment, which compare errors on the same euro or percentage scale regardless of how spread out the target is. |
| Business impact of choosing wrong | The analytics team spends a quarter "fixing" the sedan segment where the model is already as accurate as elsewhere, while real problems wait. |
| Small numeric example | Sedans actual €2,200–2,400 (mean 2,300; spread sum of squares 25,000); commercial vehicles actual €800–4,500 (mean 2,460; 8,412,000); in both the errors are ±€40, squares sum 8,000 → R² sedans = 1 − 8,000 / 25,000 = 0.68; R² commercial = 1 − 8,000 / 8,412,000 = 0.999 → WAPE: sedans 200 / 11,500 = 1.74%; commercial 200 / 12,300 = 1.63%, so the two are nearly identical. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Weekly ticket revenue during a growth phase |
| Industry / Domain | transport (passenger rail) |
| Business Problem | A UK train operator forecasts weekly ticket revenue in £m during a period of steady growth, and the board is shown R² as the headline accuracy number. |
| ML Translation | Target = weekly revenue in £m; time-series regression with a strong upward trend; ten weeks of data. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | With a steady trend the weekly values are far from the long-run average, so "beating the average" is trivial and R² looks high even for a model that is worse than just copying last week's figure. |
| Why other metrics are NOT suitable here | RMSE and MAE give a size of miss but no comparison with a simple rule; Pearson r is also high for any trending model; MAPE has no built-in benchmark either. |
| Better alternative (if BAD fit) | MASE (the model's error divided by the error of the "same as last week" rule): a value above 1 shows straight away that the model is worse than copying last week. |
| Business impact of choosing wrong | The operator staffs and orders on a model that is worse than a simple spreadsheet rule, and the board is told it is "85% accurate". |
| Small numeric example | Revenue £m 10, 11, …, 19 (mean 14.5; squared distances sum 82.5); model misses by exactly 1.1 each week → squares 10 × 1.21 = 12.1; R² = 1 − 12.1 / 82.5 = 0.853 looks strong → naive "last week" rule: weekly rise 1.0, so its MAE = 1.0 → MASE = model MAE 1.1 / 1.0 = 1.1, so the model is worse than copying last week. |

**6. Quick decision rule:** Use R² on held-out data for a controlled, well-spread target when you want to know whether the model beats the average and by how much; avoid it for comparing segments with different spreads, for trending time series, for model selection by in-sample fit, or as the only accuracy number.

### Adjusted R²

**1. What it measures (plain English):** Adjusted R² is R² with a penalty for each extra predictor, so adding a useless variable can make it go down. It is meant for choosing between linear models that have different numbers of predictors, fitted on the same data. It uses n, the number of rows, and p, the number of predictors (not counting the intercept).

`Adjusted R² = 1 − (1 − R²) × (n − 1) / (n − p − 1)`

**2. Intuition:** It is like a restaurant bill that adds a service charge for every extra dish you order: a dish must be good enough to pay for its own charge, otherwise the final value drops.

**3. Benefits:**

- Fixes R²'s flaw: it can fall when a feature adds less than a random variable would.
- Trivial to compute from R², n and p, and reported by standard statistics software.
- The gap between R² and adjusted R² is a free warning that there are too many predictors for the number of rows.
- Keeps R²'s easy "share of variation explained" reading.

**4. Limitations / Potential issues:**

- Only works for models where the number of parameters is clear (linear and similar); not for random forests, boosted trees or neural nets.
- A weak penalty: it keeps a variable whenever its partial F-statistic exceeds about 1, which is lenient compared with AIC or BIC.
- Meaningful only in-sample; reporting it on a test set is a category error.
- Not a replacement for cross-validation (testing on several held-out slices of the data).
- Can be negative, and is undefined when n is no larger than p + 1.
- Inherits R²'s weaknesses: outliers, bias blindness, dependence on spread.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Should "number of windows" stay in the repair-cost model? |
| Industry / Domain | real estate (social housing) |
| Business Problem | A UK housing association models annual repair cost per home in pounds from property features across 40 homes, and an analyst proposes adding a fourth feature, "number of windows", because R² went up slightly. |
| ML Translation | Target = annual repair cost in £; ordinary linear regression; small sample (n = 40) with three predictors versus four. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | With few rows and a linear model, the penalty is exactly what is needed: the new feature raises R² a little but not enough to pay for the lost degree of freedom (the cost of estimating one more number from limited data), so adjusted R² falls and says to drop it. |
| Why other metrics are NOT suitable here | Plain R² can only go up when a predictor is added, so it would always support keeping the feature; in-sample RMSE also always falls; cross-validation on only 40 rows is very noisy. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Keeping junk variables makes the model look better than it is, so repair budgets are set with false confidence and the model gets worse on next year's homes. |
| Small numeric example | Model A: n = 40, p = 3, R² = 0.700 → adjusted = 1 − 0.300 × 39/36 = 1 − 0.325 = 0.675 → Model B (add windows): p = 4, R² = 0.704 → adjusted = 1 − 0.296 × 39/35 = 1 − 0.330 = 0.670, which is lower, so drop the feature. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Does performance rating earn its place in a pay-equity model? |
| Industry / Domain | HR |
| Business Problem | The HR team of a European retail chain models base salary from role, tenure, grade and location for 60 roles, and wants to know whether adding "performance rating" really explains pay or just inflates the fit. |
| ML Translation | Target = base salary in €; explainable linear regression kept deliberately simple for an equal-pay review; n = 60. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The model must stay a transparent linear one; adjusted R² gives a quick, widely understood check on whether a new factor explains more than chance, and here it rises, so the factor earns its place. |
| Why other metrics are NOT suitable here | R² always rises, so it cannot separate a real factor from a noise factor; AIC or BIC are valid but harder to explain to a pay-equity committee; RMSE in euros has no complexity penalty. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Wrongly dropping a real pay factor would make unexplained pay gaps look bigger, which could trigger an unnecessary adjustment budget or legal exposure. |
| Small numeric example | Before: n = 60, p = 4, R² = 0.71 → adjusted = 1 − 0.29 × 59/55 = 1 − 0.311 = 0.689 → After adding rating: p = 5, R² = 0.76 → adjusted = 1 − 0.24 × 59/54 = 1 − 0.262 = 0.738, which is higher, so keep it. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Ten pilot batches and six process variables |
| Industry / Domain | pharma (manufacturing) |
| Business Problem | A pharmaceutical plant has only 10 pilot batches and fits a linear model of tablet hardness with six process variables before scaling up production. |
| ML Translation | Target = tablet hardness; linear regression with n = 10 and p = 6, leaving just three residual degrees of freedom. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The R² looks impressive but with so many predictors for so few rows it is mostly an illusion; the large gap between R² and adjusted R² is the free alarm that the model is over-parameterised (too many knobs for the data). |
| Why other metrics are NOT suitable here | R² alone gives a falsely comfortable 0.90; RMSE in-sample is also optimistic; a proper held-out test is impossible with only 10 batches. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Scaling up on a model that only fits the pilot batches by chance can mean failed full-size batches costing tens of thousands of euros each. |
| Small numeric example | n = 10, p = 6, R² = 0.90 → degrees of freedom n − p − 1 = 3; adjusted = 1 − 0.10 × 9/3 = 1 − 0.30 = 0.70 → the 0.20 gap is a warning to cut variables or collect more batches. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — A boosted-tree wind-power model with thousands of effective parameters |
| Industry / Domain | energy (wind generation) |
| Business Problem | A Danish wind-farm operator fits a gradient-boosted tree model (300 trees) on 2,000 hourly rows with 12 inputs to predict turbine output, and an analyst reports adjusted R² to prove it is not overfitted. |
| ML Translation | Target = hourly turbine output in MW; regression; tree ensemble with a flexible, hard-to-count complexity. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The formula needs a parameter count p, but a tree ensemble's real complexity comes from trees, depth and learning rate, not from the number of inputs; using p = 12 gives a penalty of almost nothing. |
| Why other metrics are NOT suitable here | In-sample R² is just as overoptimistic; RMSE on training data also hides overfitting; AIC and BIC need a likelihood and a parameter count, which have the same problem. |
| Better alternative (if BAD fit) | Cross-validated R² (or RMSE on held-out data), which measures generalisation directly without counting parameters. |
| Business impact of choosing wrong | The model is declared safe and used to bid energy in the day-ahead market; when it really explains only about 71% of variation, forecast misses cause imbalance penalties. |
| Small numeric example | Training R² = 0.99, n = 2,000, p = 12 → adjusted = 1 − 0.01 × 1,999/1,987 = 0.990, which looks perfect → five-fold cross-validated R² = 0.71, 0.68, 0.74, 0.69, 0.72; mean 0.708. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — A junk variable passes the adjusted R² test |
| Industry / Domain | tourism (ski resorts) |
| Business Problem | An Alpine tour operator regresses seasonal revenue for 25 ski resorts on three predictors and tests adding a fourth (social-media posts per week), with adjusted R² as the only gate. |
| ML Translation | Target = seasonal revenue in €m; linear regression; n = 25; candidate variable is likely noise. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The penalty is lenient: the new variable's partial F-statistic is 1.43 (above 1), so adjusted R² goes up and says "keep", although the stricter BIC and AIC criteria say the model got slightly worse. |
| Why other metrics are NOT suitable here | Plain R² always rises, so it is worse as a gate; RMSE in-sample always falls; MAE has no complexity penalty either. |
| Better alternative (if BAD fit) | BIC or AIC (stricter complexity penalties) or leave-one-out cross-validation, which tests the model on resorts it has not seen. |
| Business impact of choosing wrong | The pricing model carries a noise variable, so next season's resort revenue forecasts drift and sales targets are set on false relationships. |
| Small numeric example | n = 25, total variation 1,000; model A: p = 3, residual sum of squares 300 → R² = 0.700, adjusted = 1 − (300/21) / (1,000/24) = 0.657 → model B: p = 4, residual 280 → R² = 0.720, adjusted = 1 − (280/20) / (1,000/24) = 0.664 (up, "keep") → but BIC = n × ln(RSS/n) + ln(n) × (parameters incl. intercept): A = 75.00, B = 76.49 (higher is worse), so BIC says drop; AIC (A 70.12, B 70.40) agrees. |

**6. Quick decision rule:** Use adjusted R² to compare linear models of different sizes fitted on the same data, and to flag over-parameterisation through the gap to R²; avoid it for trees, boosted models or neural nets, on test sets, and as the only guard against overfitting.

### Explained Variance Score

**1. What it measures (plain English):** Explained variance score is like R², but it ignores any constant bias in the predictions: it asks how much of the target's ups and downs the model captured, even if the whole forecast sits too high or too low. It is never lower than R², and the gap between the two equals the squared bias divided by the target's variance. Often shortened to EVS.

`EVS = 1 − Var(y − ŷ) / Var(y)`

**2. Intuition:** Think of a bathroom scale that always reads 2 kg too heavy: it perfectly captures who is heavier than whom, so it "explains the variation" well, but its readings are still wrong until you fix the offset.

**3. Benefits:**

- Separates the model's ability to follow the shape of the target from its calibration (whether the level is right).
- The gap between EVS and R² is a free, exact diagnostic of bias.
- Unitless and anchored like R², and available in common libraries.
- Useful when a downstream step will remove a constant offset anyway.

**4. Limitations / Potential issues:**

- Ignores bias completely, so a model that is uniformly 1,000 units low can score about 1.0.
- Often confused with R² and reported as if they were the same.
- Inherits R²'s sensitivity to outliers and to the spread of the target.
- Rarely the right headline metric; best used beside R² as a diagnostic.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Did converting back from logs leave the spend model biased? |
| Industry / Domain | energy (retail supply) |
| Business Problem | A UK energy retailer predicts each customer's annual spend in pounds with a model trained on log values and then converted back, and analysts want to know whether the conversion left a systematic bias. |
| ML Translation | Target = annual spend in £; regression; right-skewed target; predictions from exp of the log-scale model output. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | EVS ignores bias while R² charges for it, so the gap EVS − R² isolates exactly how much of the error is a simple offset; here the gap is 0.0137, a clear sign of mild bias worth correcting. |
| Why other metrics are NOT suitable here | R² alone cannot tell shape error from bias; MAE gives a size of miss but not its cause; RMSLE cannot see the bias because it hides it in the log scale. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (as a diagnostic beside R²) |
| Business impact of choosing wrong | Missing the bias means every revenue forecast built on the sum of customer predictions is low; here predicted total £7,990 versus actual £8,600, 7.1% short. |
| Small numeric example | Actual spend £600; 900; 1,400; 2,200; 3,500; predicted 560; 850; 1,330; 2,000; 3,250 → residuals 40, 50, 70, 200, 250; mean 122; Var(y) = 1,085,600 → R² = 0.9795; EVS = 0.9932; gap = 0.0137 = 122² / 1,085,600 → multiply predictions by 8,600 / 7,990 = 1.076 and R² rises to 0.9994. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — A coating-thickness soft sensor with a weekly offset correction |
| Industry / Domain | manufacturing (automotive parts) |
| Business Problem | A Slovak car-parts plant estimates coating thickness in micrometres from line speed and oven temperature; the lab recalibrates a fixed offset every week, so engineers want to know whether the sensor tracks the real ups and downs. |
| ML Translation | Target = coating thickness in µm; regression on process variables; a constant offset is removed downstream. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Because the offset is fixed by recalibration, what matters is whether the model follows the variation, and EVS scores exactly that without being punished for the offset that the weekly step will remove. |
| Why other metrics are NOT suitable here | R² would be unfairly low (about 0.49) and could reject a sensor that is fine after recalibration; MAE of about 4.8 µm mostly measures the offset, not the tracking; Pearson r would miss a slope error that EVS would catch. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (check R² after the offset is removed to confirm) |
| Business impact of choosing wrong | Rejecting a good sensor means keeping slow lab thickness checks on every shift; accepting a sensor that does not track shape would let bad coating through. |
| Small numeric example | Actual µm 20, 24, 28, 32, 36, 40 (variance 46.67); predicted 14.5, 19.5, 22.5, 27.5, 31.5, 35.5 → residuals 5.5, 4.5, 5.5, 4.5, 4.5, 4.5; mean 4.83 → R² = 0.495, EVS = 0.995 → after subtracting 4.83 from every residual, R² = 0.995, confirming the sensor is good apart from the offset. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — A fuel model that is a flat 1,000 litres low |
| Industry / Domain | logistics (road haulage) |
| Business Problem | A UK haulier forecasts daily diesel use in litres to buy fuel in advance, and the data team reports EVS as the headline accuracy figure. |
| ML Translation | Target = daily diesel use in litres; regression; the model is uniformly 1,000 litres below the actual. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | EVS ignores a constant offset, so a model that is wrong by the same amount every day scores a perfect 1.0 even though the fuel budget is wrong every single day. |
| Why other metrics are NOT suitable here | RMSE and MAE do show the offset but give no comparison with the spread of the target; MAPE shows a percentage but not the direction; correlation is again 1.0 and blind to the offset. |
| Better alternative (if BAD fit) | R² plus MAE and a signed average error (bias): R² charges for the offset, and MAE and bias show it in litres and pounds. |
| Business impact of choosing wrong | At £1.60 a litre, being 1,000 litres short each day is £1,600 a day, about £584,000 a year of unplanned spot-price fuel purchases. |
| Small numeric example | Actual litres 8,000; 9,000; 10,000; 11,000; 12,000; forecast each 1,000 lower → residuals all 1,000, variance of residuals 0 → EVS = 1 − 0 / 2,000,000 = 1.00 → R² = 1 − 5,000,000 / 10,000,000 = 0.50; MAE = 1,000 litres. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — An infusion-dose model that adds a constant 8 mg |
| Industry / Domain | healthcare (hospital pharmacy) |
| Business Problem | A hospital pharmacy in Germany tests a model that suggests infusion doses in milligrams, and the validation report quotes EVS because "it measures how well the model follows patient needs". |
| ML Translation | Target = prescribed dose in mg; regression; the model adds a constant 8 mg to every patient. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | A constant overdose is a pure offset, so EVS reads a perfect 1.0, yet every patient receives too much, which is a safety problem rather than a statistics detail. |
| Why other metrics are NOT suitable here | R² still reads a comforting 0.86 and hides how large the overdose is in milligrams; MAPE averages away the fact that the smallest patient is overdosed by 20%; correlation is also 1.0. |
| Better alternative (if BAD fit) | MAE, signed average error (bias) and the maximum error in mg: they show the size and direction of the overdose in clinical units. |
| Business impact of choosing wrong | Systematic overdosing creates patient harm, adverse-event reports and regulatory trouble that no variance score would have warned about. |
| Small numeric example | Prescribed mg 40, 55, 70, 85, 100; model 48, 63, 78, 93, 108 → residuals all −8; variance of residuals 0 → EVS = 1.00 → R² = 1 − 320 / 2,250 = 0.858; MAE = 8 mg, which is 20% of the smallest dose and 8% of the largest. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Repair-cost reserves after a parts-price jump |
| Industry / Domain | insurance (motor claims) |
| Business Problem | After parts prices rise 15%, a European motor insurer re-checks its repair-cost model; the ranking of claims is unchanged but every prediction is now 15% too low. |
| ML Translation | Target = repair cost per claim in €; regression; a shift in the level (price inflation) after the model was trained. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | EVS stays near 1 (0.98) because the shape of the costs is intact, which tells the insurer the model "still works", while reserves are 15% short. |
| Why other metrics are NOT suitable here | Pearson r stays near 1 for the same reason; Spearman rank correlation is exactly 1 and totally blind to the shift; MAE would show the euro miss but not that it is one-directional. |
| Better alternative (if BAD fit) | R² (it falls to 0.80) together with a signed percentage error on the total, which shows the 15% shortfall and points to a simple recalibration. |
| Business impact of choosing wrong | Reserves that are 15% short are discovered only when claims settle, forcing an unplanned top-up from capital. |
| Small numeric example | Actual cost €1,000; 1,500; 2,000; 2,500; 3,000 (total 10,000); predicted 0.85 × each (total 8,500) → Var(y) = 500,000 and residual variance 11,250 → EVS = 1 − 11,250 / 500,000 = 0.9775 → R² = 1 − 101,250 / 500,000 = 0.7975 → total shortfall €1,500, which is 15%. |

**6. Quick decision rule:** Use EVS as a diagnostic beside R² (its gap shows bias) or when a constant offset will be removed downstream anyway; avoid it as the only or headline accuracy metric where the level of the prediction matters.

## Correlation and Agreement Metrics

### Pearson Correlation (r)

**1. What it measures (plain English):** Pearson correlation measures how closely two sets of numbers move together along a straight line, from −1 (perfect opposite) through 0 (no straight-line link) to +1 (perfect together). It says nothing about whether predictions are correct in size: a model that predicts twice the true value has r = 1. Also called the Pearson correlation coefficient.

`r = Σ(yᵢ − ȳ)(ŷᵢ − mean(ŷ)) / sqrt(Σ(yᵢ − ȳ)² × Σ(ŷᵢ − mean(ŷ))²)`

**2. Intuition:** It is like checking whether two runners keep pace with each other along a road without caring whether they are running the same distance.

**3. Benefits:**

- Unitless, quick, and universally understood.
- Isolates whether two things move together from whether they are on the same scale.
- Excellent for screening candidate features against a target.
- Works when two measures are in different units (an index versus a physical quantity).

**4. Limitations / Potential issues:**

- Blind to scale and offset errors, so it cannot be used as an accuracy metric (ŷ = 2y gives r = 1).
- Sensitive to outliers: one extreme pair can create or destroy a high correlation.
- Only detects straight-line relationships; a strong curved relationship can give r near 0.
- Squared r is often mislabelled as R² and flatters accuracy.
- Undefined when either series is constant.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Screening sensors against weld strength |
| Industry / Domain | manufacturing (automotive) |
| Business Problem | A German automotive supplier has 30 sensor readings per weld and wants a quick shortlist of the ones linearly linked to weld strength before building any model. |
| ML Translation | Target = weld strength in kN; feature screening by the straight-line correlation of each sensor with the target; a few hundred welds. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | No prediction exists yet, so there are no errors to measure; Pearson r gives a fast, comparable straight-line strength for each sensor, and a linear model will use exactly that kind of relationship. |
| Why other metrics are NOT suitable here | RMSE and R² need predictions from a fitted model, which is the step the screen is meant to guide; Spearman is a fair alternative but ignores magnitudes; mutual information is heavier to compute and harder to explain to process engineers. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Missing a strongly linked sensor means a weaker model and more scrap welds; chasing weak sensors wastes engineering time. |
| Small numeric example | Strength kN 310, 325, 340, 350, 365, 380 (mean 345; sum of squares 3,300); clamp pressure 55, 58, 63, 66, 70, 75 (mean 64.5; sum of squares 277.5; cross-product sum 955) → r = 955 / sqrt(3,300 × 277.5) = 0.998 → coolant flow 22, 35, 18, 30, 25, 20 (mean 25; sum of squares 208; cross-product sum −210) → r = −210 / sqrt(3,300 × 208) = −0.25, so clamp pressure is the one to keep. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Does a cheap irradiance index track solar-park output? |
| Industry / Domain | energy (solar) |
| Business Problem | A Spanish solar-park operator wants to know whether a free satellite irradiance index follows daily measured output closely enough to use later in a forecast; scaling it to MWh will be fitted afterwards. |
| ML Translation | Target = daily output in MWh; the index is on a different unit scale (0 to about 4); exploratory check of straight-line linkage on six days. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The two series are in different units, so only the strength of their straight-line link is meaningful at this stage; r is exactly the right question and is scale-free. |
| Why other metrics are NOT suitable here | RMSE, MAE and R² compare values in the same unit, so on the raw index they are meaningless (R² of the raw index is −6.1); CCC requires both series on the same scale; MAPE has the same unit problem. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (then fit the scaling line and judge the fitted forecast with RMSE or R²) |
| Business impact of choosing wrong | Rejecting a good free index means paying for commercial irradiance data; judging by raw-unit RMSE would reject it for the wrong reason. |
| Small numeric example | Output MWh 120, 180, 250, 310, 380, 450 (sum of squares 76,283); index 0.9, 1.4, 1.9, 2.4, 3.0, 3.5 (sum of squares 4.788; cross-product sum 604.2) → r = 604.2 / sqrt(76,283 × 4.788) = 0.9997 → fitted line MWh ≈ 126.2 × index + 6.2 puts the index on the right scale. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — A savings model that reports per month instead of per year |
| Industry / Domain | real estate (energy-efficiency retrofits) |
| Business Problem | A European green-loan provider's model predicts the yearly energy saving in euros from insulating a home; the reviewer sees r = 1.00 and signs it off, but a coding slip makes the model output monthly instead of yearly values. |
| ML Translation | Target = yearly saving in €; regression; the predictions are exactly one twelfth of the true value. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Pearson r does not change when predictions are rescaled, so a model that is wrong by a factor of 12 still scores a perfect 1.00. |
| Why other metrics are NOT suitable here | Spearman rank correlation is also exactly 1.0 and just as blind; explained variance score also barely notices a pure rescale in the right-hand direction (the large offset is hidden in part); MAPE shows the 92% miss but is not a goodness-of-fit summary. |
| Better alternative (if BAD fit) | R² (it falls far below 0) and RMSE or MAE in euros, which charge for scale errors. |
| Business impact of choosing wrong | Homeowners are told they would save a twelfth of the real amount, so green-loan uptake collapses and the provider's retrofit targets are missed. |
| Small numeric example | Actual yearly saving €240, 360, 480, 600, 720; model output 20, 30, 40, 50, 60 → r = 1.000 → residuals 220, 330, 440, 550, 660; MAE = €440; RMSE = €467; R² = 1 − 1,090,000 / 144,000 = −6.56, which exposes the problem. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Hospital waiting times with one extreme day |
| Industry / Domain | healthcare (hospital operations) |
| Business Problem | A UK hospital trust predicts A&E waiting time in minutes for patients on six reference days; one day with a bed shortage had a very long wait, and the report quotes r for model quality. |
| ML Translation | Target = waiting time in minutes; regression; five ordinary days (30 to 70 minutes) and one extreme day (400 minutes) acting as an outlier. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Pearson r is dominated by the one extreme day that the model got right (380 versus 400), producing r = 0.97, while on the five ordinary days the model has no useful link to reality (r = −0.47 without the extreme day). |
| Why other metrics are NOT suitable here | R² is inflated by the same extreme point (0.94); RMSE is also dominated by large days but at least shows the minute-size error; MAPE is dominated by the shortest waits. |
| Better alternative (if BAD fit) | Spearman rank correlation (0.14 here) and MAE or median absolute error in minutes, which expose the poor performance on ordinary days. |
| Business impact of choosing wrong | Managers rely on a model that cannot predict normal days, so staff rotas are misplaced on 5 of 6 days; a 30-minute average miss on waits of 30 to 70 minutes is a very large error for patients. |
| Small numeric example | Actual minutes 30, 45, 50, 60, 70, 400; predicted 95, 60, 30, 85, 45, 380 → r = 91,429 / sqrt(102,421 × 86,671) = 0.970 → Spearman ρ = 0.14 → absolute errors 65, 15, 20, 25, 25, 20; MAE = 28.3 minutes; median 22.5 minutes; MAE on the five ordinary days = 30.0 minutes. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Hotel bookings that rise and then fall with heat |
| Industry / Domain | tourism (hospitality) |
| Business Problem | A Greek island hotel group checks whether daily peak temperature relates to bookings; bookings peak at pleasant 25 °C and drop in both cold and extreme heat. |
| ML Translation | Target = bookings per 100 rooms; relationship with temperature is an inverted U (rises then falls), over seven temperature levels. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Pearson r only sees straight-line relationships, and a symmetric hump has no straight-line trend, so r is exactly 0 even though temperature almost completely determines bookings. |
| Why other metrics are NOT suitable here | Spearman rank correlation is also 0 because the relationship is not one-directional; MAE and RMSE need a model to score; plain R² of a straight-line fit would also be 0. |
| Better alternative (if BAD fit) | A scatter plot plus a flexible model (for example a quadratic curve), or a measure that detects any relationship such as mutual information or distance correlation. |
| Business impact of choosing wrong | Revenue managers conclude "temperature does not matter", drop it from the pricing model, and miss both the 40 °C heat-wave dip and the best pricing window around 25 °C. |
| Small numeric example | Temperature °C 10, 15, 20, 25, 30, 35, 40; bookings 20, 50, 80, 90, 80, 50, 20 → cross-product sum = 0 → r = 0.00; Spearman ρ = 0.00 → a quadratic fit has R² = 0.98. |

**6. Quick decision rule:** Use Pearson r for screening features, for checking straight-line co-movement when units differ, or for exploratory analysis; avoid it as an accuracy metric, when outliers or curved relationships are present, or when the scale of the predictions matters.

### Spearman Correlation (ρ)

**1. What it measures (plain English):** Spearman correlation measures whether two sets of numbers put things in the same order, ignoring the actual sizes. It is Pearson correlation computed on the ranks (1st, 2nd, 3rd and so on), so it is unaffected by outliers and by any consistently increasing distortion of the values. Also called Spearman rank correlation or rho; in quantitative finance it is known as the Information Coefficient.

`ρ = Pearson r computed on rank(y) and rank(ŷ)`

`ρ = 1 − 6 × Σdᵢ² / (n × (n² − 1))`, where dᵢ is the rank difference and there are no ties

**2. Intuition:** It is like comparing two critics' top-ten film lists: you only care whether they put the films in the same order, not whether one gives scores out of 5 and the other out of 100.

**3. Benefits:**

- Directly measures ranking quality, which is what many real systems use.
- Robust to outliers and to curved-but-consistently-rising relationships.
- Works across different units and scales, since only the order counts.
- Cheap to compute and easy to explain.

**4. Limitations / Potential issues:**

- Ignores the size of errors completely: a near-miss and a huge miss look the same if the order is kept.
- Cannot detect scale or offset problems: predictions that are wildly off in size can still give ρ = 1.
- Looks at the whole list equally, so it can be high even when the top few (the ones you act on) are wrong.
- Sensitive to many tied values.
- Undefined if either series is constant; and a non-monotonic (up then down) relationship gives ρ near 0.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Ranking stocks for the monthly portfolio |
| Industry / Domain | banking (asset management) |
| Business Problem | A European asset manager's model predicts next-month returns for eight stocks, and the portfolio buys the highest-ranked and avoids the lowest; the predicted size of each return is never used for position sizing. |
| ML Translation | Target = next-month return in percent; regression whose output is used only to rank; cross-sectional ranking each month. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Only the order is used, so the right question is "did the model put the winners above the losers", which Spearman (the Information Coefficient) measures directly; magnitude errors are irrelevant to the decision. |
| Why other metrics are NOT suitable here | RMSE and R² punish the model for exaggerated return sizes that are never used (R² is −2.57 in the example); Pearson r is dragged by extreme values; MAE penalises scale differences that do not affect the ranking. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (also check stability across months and the top-bucket return) |
| Business impact of choosing wrong | Judging the model on RMSE would reject a useful ranking signal or push the team to tune for return size rather than order, reducing portfolio returns. |
| Small numeric example | Actual % 2.1, −1.5, 0.8, 3.2, −0.4, 1.1, −2.3, 0.2 → ranks 7, 2, 5, 8, 3, 6, 1, 4; predicted % 4, −2, −1, 9, −3, 6, −5, 2 → ranks 6, 3, 4, 8, 2, 7, 1, 5 → rank differences 1, −1, 1, 0, 1, −1, 0, −1; squares sum 6 → ρ = 1 − 6 × 6 / (8 × 63) = 0.929 (real signals are far weaker, often 0.03 to 0.06). |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Deciding which insurance claims the senior handler sees first |
| Industry / Domain | insurance |
| Business Problem | An insurer's claims team scores each new claim with a predicted final cost so that the senior handler works the most expensive claims first; the queue order is all that is used. |
| ML Translation | Target = final claim cost in €k; regression whose prediction is used only to sort a queue; seven new claims. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The queue only needs the order of claims by cost to be right, so how well the predicted ranking matches the true ranking is the correct test. |
| Why other metrics are NOT suitable here | RMSE and MAE count euro errors that never affect the queue; R² (0.90 here) mixes in size accuracy; MAPE is unstable for very small claims. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (add a top-k check on the biggest claims) |
| Business impact of choosing wrong | A wrong metric could cause a good ranking model to be rejected for poor euro accuracy, and large claims sit in the queue longer, adding cost through delayed fraud and leakage checks. |
| Small numeric example | Actual €k 12, 85, 30, 160, 45, 8, 70 → ranks 2, 6, 3, 7, 4, 1, 5; predicted 20, 60, 25, 140, 50, 10, 95 → ranks 2, 5, 3, 7, 4, 1, 6 → rank differences 0, 1, 0, 0, 0, 0, −1; squares sum 2 → ρ = 1 − 6 × 2 / (7 × 48) = 0.964. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Ranking restaurants for food-safety inspection |
| Industry / Domain | public sector (municipal food safety) |
| Business Problem | A city council's model gives each restaurant a risk score from 0 to 100, and inspectors visit the highest scores first; the score is checked against the demerit points inspectors later record. |
| ML Translation | Prediction = risk score 0 to 100; outcome = inspector demerit points; two different units; six restaurants. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The score and the demerit points are on different scales, so only the agreement of the order makes sense; Spearman checks exactly that. |
| Why other metrics are NOT suitable here | RMSE and MAE cannot be computed meaningfully because the units differ; R² has the same problem; Pearson r assumes a straight-line relationship that the two scales may not share. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | If the order is wrong, inspectors visit safe premises while risky kitchens wait, increasing the chance of a food-poisoning outbreak and the legal exposure that follows. |
| Small numeric example | Risk score 82, 35, 64, 18, 50, 91 → ranks 5, 2, 4, 1, 3, 6; demerit points 21, 9, 12, 2, 6, 25 → ranks 5, 3, 4, 1, 2, 6 → rank differences 0, −1, 0, 0, 1, 0; squares sum 2 → ρ = 1 − 6 × 2 / (6 × 35) = 0.943. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Water-use predictions used to calculate bills |
| Industry / Domain | utilities (water) |
| Business Problem | A European water utility predicts yearly water use in cubic metres for commercial customers to set provisional bills, and the analyst reports a perfect rank correlation. |
| ML Translation | Target = yearly use in m³; regression; the predictions are compressed (a rising but badly flattened curve) and are used as billing quantities. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Any consistently rising distortion leaves the order unchanged, so ρ stays at 1.00 even when the big customers are predicted at a fraction of their true use; the bill depends on the size, not the order. |
| Why other metrics are NOT suitable here | Pearson r would be high but not perfect, still hiding the miss; explained variance ignores the level of the compression only partly; MAPE shows the error but not the total shortfall. |
| Better alternative (if BAD fit) | R², MAE and the signed total error (bias), which charge for the size of the miss and show the shortfall in cubic metres and euros. |
| Business impact of choosing wrong | Provisional bills are far too low and the utility must send large catch-up bills later, damaging customer relationships and cash flow; at €2.00 per m³ the example is under-billed by €4,380. |
| Small numeric example | Actual m³ 100, 200, 400, 800, 1,600 (total 3,100); predicted 100, 150, 190, 220, 250 (total 910) → ρ = 1.00 (same order) → errors 0, 50, 210, 580, 1,350; MAE = 438 m³; R² = −0.48; the total shortfall is 2,190 m³ × €2.00 = €4,380. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Picking the top two customers for a costly campaign |
| Industry / Domain | banking (retail) |
| Business Problem | A Dutch bank can afford to phone only the two customers (out of ten) with the highest expected spend on a new product, and a manager notes that the model's rank correlation is a healthy 0.77. |
| ML Translation | Target = customer spend in €; regression used to choose the top two; ten customers. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Spearman weighs the whole list equally, so decent agreement in the middle and bottom can hide the fact that the two customers actually chosen are not the best ones. |
| Why other metrics are NOT suitable here | Pearson r has the same blind spot; R² and RMSE focus on size accuracy across all customers rather than the top few; MAE does the same. |
| Better alternative (if BAD fit) | Precision at k (how many of the chosen top k really are in the true top k) or the mean actual spend of the chosen top k, compared with the best possible and the average. |
| Business impact of choosing wrong | The campaign budget is spent on customers who are not the best prospects; here the chosen pair average €575 against €850 for the true best two. |
| Small numeric example | Actual spend € 900, 800, 700, 650, 600, 500, 400, 300, 200, 100 (customers A to J); predicted ranks 3, 4, 5, 1, 6, 2, 7, 8, 9, 10 → rank differences 2, 2, 2, 3, 1, 4, 0, 0, 0, 0; squares sum 38 → ρ = 1 − 6 × 38 / 990 = 0.770 → the model's top two are customers D and F (spend 650 and 500), mean €575 versus €850 for the true top two and €515 for a random pair on average; precision at 2 = 0 of 2. |

**6. Quick decision rule:** Use Spearman when only the order of predictions is used (rankings, queues, screening) or when units differ; avoid it when the size of the prediction is used (billing, pricing, budgets) or when only the top few picks matter.

### Concordance Correlation Coefficient (CCC, Lin's CCC)

**1. What it measures (plain English):** CCC measures agreement, not just association: do the points fall on the 45-degree line where predicted equals actual? It is lowered by weak correlation, by a bias (average too high or low), and by a mismatch in spread. It equals Pearson r multiplied by a correction factor for bias and spread. Also called Lin's CCC.

`CCC = 2 × Cov(y, ŷ) / (Var(y) + Var(ŷ) + (mean(y) − mean(ŷ))²)`

**2. Intuition:** Two clocks can tick in perfect step with each other and still show different times. Pearson checks the ticking; CCC checks that both clocks also show the same time.

**3. Benefits:**

- Penalises bias and scale mismatch that Pearson r ignores.
- Splits into precision (r) and accuracy (a bias-correction factor), so you can see which one is wrong.
- Bounded between −1 and +1 and unitless; the standard in method-comparison studies.
- Easy to explain to anyone who knows Cohen's Kappa (the agreement measure for categories).

**4. Limitations / Potential issues:**

- Not in the mainstream machine-learning libraries; you must implement it, and versions differ slightly (population versus sample variance).
- Dominated by large values when the data is heavily skewed, so it is a poor guide to relative error.
- Needs both measures on the same scale and in the same units.
- Sensitive to the range of the data, so it is not comparable across groups with different spreads.
- One number does not say whether the problem is bias or spread; check the decomposition.
- The strict clinical bands (for example above 0.99 for almost perfect) are too harsh for typical machine-learning tasks.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Can a point-of-care haemoglobin device replace the lab analyser? |
| Industry / Domain | healthcare (diagnostics) |
| Business Problem | A European hospital group tests a handheld device that gives haemoglobin in g/dL from a finger prick, to see whether it agrees closely enough with the central lab analyser to replace it. |
| ML Translation | Paired measurements of the same eight samples: lab reference (y) and device reading (ŷ), both in g/dL; an agreement study. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The claim is "the device agrees with the lab", not "the device moves with the lab"; CCC catches the device's consistent upward offset that a correlation coefficient would ignore. |
| Why other metrics are NOT suitable here | Pearson r gives 0.999 and would wrongly call the device excellent; MAE has no accepted threshold and ignores how spread out the samples are; a Bland-Altman plot is a useful companion but is a chart rather than one summary number. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice (report it with a Bland-Altman plot) |
| Business impact of choosing wrong | Approving a device that reads 0.8 g/dL high could hide mild anaemia in patients, leading to missed treatment. |
| Small numeric example | Lab g/dL 9.1, 10.4, 11.8, 12.6, 13.5, 14.2, 15.0, 16.1 (mean 12.84; variance 4.832); device 9.9, 11.1, 12.5, 13.5, 14.2, 15.1, 15.7, 16.8 (mean 13.60; variance 4.803); covariance 4.814 → CCC = 2 × 4.814 / (4.832 + 4.803 + 0.581) = 9.628 / 10.216 = 0.942, with 0.581 = (12.84 − 13.60)² → Pearson r = 0.999; the gap comes from the 0.76 g/dL offset. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Approving a smart meter against a reference meter |
| Industry / Domain | energy (grid operation) |
| Business Problem | A grid operator tests a new smart electricity meter against a calibrated reference meter on a test bench at six load levels, to decide whether to roll it out. |
| ML Translation | Paired readings in kWh: reference (y) and new meter (ŷ), same units; agreement study with six load levels. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Regulators want agreement with the reference, not just co-movement; CCC correctly gives a very high score here because the readings fall almost exactly on the 45-degree line. |
| Why other metrics are NOT suitable here | Pearson r is also high (0.9998) but would be just as high for a meter that reads double, so it cannot prove agreement; R² against the identity line is similar but has no tradition in method-comparison reporting; MAPE depends on the size of each reading. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A wrong approval metric could put millions of meters that mis-bill in customers' homes, with regulator fines and refunds. |
| Small numeric example | Reference kWh 120, 240, 360, 480, 600, 720 (mean 420; variance 42,000); new meter 123, 236, 365, 476, 606, 715 (mean 420.17; variance 41,641); covariance 41,810 → CCC = 2 × 41,810 / (42,000 + 41,641 + 0.03) = 83,620 / 83,641 = 0.9997; mean absolute difference 4.5 kWh. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Are two surveyors' repair estimates interchangeable? |
| Industry / Domain | real estate (property insurance) |
| Business Problem | A property insurer has two flood-damage surveyors estimating repair cost for the same six homes, and wants to know whether the two can be used interchangeably when one is on leave. |
| ML Translation | Paired continuous estimates in €k from two raters; agreement between raters; same units. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Interchangeability means the pairs sit on the 45-degree line, which is what CCC measures; it is the continuous counterpart of Cohen's Kappa for inter-rater agreement. |
| Why other metrics are NOT suitable here | Pearson r would not notice if one surveyor were consistently higher; MAE is useful but gives no scale-free summary; Spearman only checks the order of the jobs, not the euro amounts. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | If the surveyors disagree by a consistent amount, claimants get different settlements depending on who visits, which causes complaints and appeals. |
| Small numeric example | Surveyor A €k 12, 18, 25, 31, 40, 55 (mean 30.17; variance 203.14); surveyor B 13, 17, 27, 30, 43, 50 (mean 30.00; variance 172.67); covariance 184.5 → CCC = 2 × 184.5 / (203.14 + 172.67 + 0.03) = 369 / 375.84 = 0.982; Pearson r = 0.985. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — A candidate-score model on a different scale from the panel |
| Industry / Domain | HR |
| Business Problem | An HR team compares a screening model's candidate score (0 to 1) with the interview panel's score (0 to 100) to see whether the model can shortlist candidates in the same order. |
| ML Translation | Paired scores for five candidates on different scales; the model is used only to build a shortlist order. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | CCC assumes the two measures are on the same scale, so it reads about 0.00 even though the model puts the candidates in exactly the same order as the panel; it answers an agreement question nobody asked. |
| Why other metrics are NOT suitable here | Pearson r is 0.99 and would be acceptable but ignores order; RMSE and MAE cannot compare 0-to-1 scores with 0-to-100 scores; R² has the same problem. |
| Better alternative (if BAD fit) | Spearman rank correlation (1.00 here), since only the shortlist order matters. |
| Business impact of choosing wrong | A good screening model is rejected, so recruiters keep reading hundreds of CVs by hand, costing time and delaying hires. |
| Small numeric example | Panel score 40, 55, 62, 70, 85 (mean 62.4; variance 225.04); model score 0.30, 0.42, 0.50, 0.58, 0.80 (mean 0.52; variance 0.0282); covariance 2.492 → CCC = 2 × 2.492 / (225.04 + 0.0282 + 3,829.1) = 4.984 / 4,054.2 = 0.0012 → Spearman ρ = 1.00, Pearson r = 0.99. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — SME loan-size forecasts with one giant loan |
| Industry / Domain | banking (SME lending) |
| Business Problem | A European bank forecasts the size of each SME loan application in €k; five are small loans and one is a very large corporate-style loan, and the report quotes CCC. |
| ML Translation | Target = loan size in €k; regression; extremely skewed, with one value about 40 times the others. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | CCC works on raw squared deviations, so the one giant loan, which the model gets nearly right, decides the result (0.9995), while the five small loans are 38% to 75% off. |
| Why other metrics are NOT suitable here | Pearson r (0.9997) and R² suffer the same domination by the giant loan; MAE and RMSE in euros are also set by the single big loan; MdAPE and RMSLE focus on relative error instead. |
| Better alternative (if BAD fit) | RMSLE (or MdAPE) for relative error across loan sizes, perhaps with CCC on the log scale if agreement is needed. |
| Business impact of choosing wrong | The model is declared "99.95% concordant" and used to plan funding for typical SME loans, where the forecasts miss by about 40%, so liquidity planning is wrong for most of the portfolio. |
| Small numeric example | Actual €k 20, 35, 50, 80, 120, 3,000; forecast 35, 20, 80, 50, 75, 3,050 → CCC = 2 × 1,224,190 / (1,200,737 + 1,248,772 + 0.69) = 0.9995 → relative errors 75%, 43%, 60%, 38%, 38%, 1.7%; median 40.2% → CCC without the giant loan = 0.54; RMSLE = 0.452 (about 57% typical miss). |

**6. Quick decision rule:** Use CCC when you must show that two measurements on the same scale agree (method comparison, inter-rater checks, model versus gold standard); avoid it when only order matters, when the scales differ, or when the target is heavily skewed and relative error is the question.
