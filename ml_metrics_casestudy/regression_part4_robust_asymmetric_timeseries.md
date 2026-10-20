# Regression Case Studies, Part 4: Robust, Asymmetric, Deviance and Time-Series Metrics

## Table of Contents

- [Robust, Asymmetric and Tolerance-Band Losses](#robust-asymmetric-and-tolerance-band-losses)
  - [Huber Loss](#huber-loss)
  - [Log-cosh Loss](#log-cosh-loss)
  - [Quantile Loss (Pinball Loss)](#quantile-loss-pinball-loss)
  - [Epsilon-insensitive Loss](#epsilon-insensitive-loss)
  - [Tukey's Biweight Loss](#tukeys-biweight-loss)
- [Monitoring, Aggregation, Deviance and Direction Metrics](#monitoring-aggregation-deviance-and-direction-metrics)
  - [Tracking Signal](#tracking-signal)
  - [Multi-output Regression Averaging](#multi-output-regression-averaging)
  - [Tweedie / Poisson / Gamma Deviance [Added – not in source file]](#tweedie--poisson--gamma-deviance-added--not-in-source-file)
  - [Mean Directional Accuracy (MDA) [Added – not in source file]](#mean-directional-accuracy-mda-added--not-in-source-file)

**How to read this part:** each metric below has a short explanation, then five case studies (a mix of good and bad fits) set mostly in East and Southeast Asia. Every number in the toy examples was recomputed in Python. A "loss" is the score a model is trained to reduce; a "metric" is the score used to report results. Several metrics here are mainly losses.

## Robust, Asymmetric and Tolerance-Band Losses

### Huber Loss

**1. What it measures (plain English):** Huber loss charges small errors by their square (like MSE) and large errors by their size only (like MAE). The switch point δ ("delta") is set in the units of the target. Beyond δ an error is treated as a possible outlier (an unusually extreme record that does not follow the pattern of the rest), so it can pull the model only by a capped amount. Aliases: smooth L1 loss (when δ = 1), robust regression loss.

`Huber(e) = ½·e² if abs(e) ≤ δ, otherwise δ·(abs(e) − ½·δ), where e = y − ŷ; the loss is the mean over all rows`

**2. Intuition:** A teacher marks a quiz. A small slip loses marks in proportion to how far off the answer is, but one absurd answer is capped at a fixed penalty instead of ruining the whole grade.

**3. Benefits:**

- Smooth near zero, so training converges cleanly (unlike MAE, which has a sharp corner at zero).
- The pull of any single record is capped at δ (its "gradient", the push on the model, is clipped), so one extreme record cannot dominate.
- δ can be set from a business fact: the error size beyond which extra error stops costing proportionally more.
- Available in most libraries (scikit-learn, XGBoost, LightGBM, PyTorch, TensorFlow).

**4. Limitations / Potential issues:**

- δ must be chosen and depends on the scale of the target; a δ tuned in rupiah is meaningless in thousands of rupiah.
- The loss value mixes two units and is not interpretable; report MAE and RMSE for results.
- It is symmetric: it cannot express that being too low costs more than being too high.
- Extreme points are down-weighted, not ignored, so it is not fully robust; and its predictions are not a clean mean or median, so totals do not add up exactly.
- If δ is larger than the biggest error, it silently becomes plain MSE.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — The wafer etch model and the broken sensor |
| Industry / Domain | Manufacturing (semiconductor fab, South Korea) |
| Business Problem | A fab predicts etched layer thickness from chamber sensor readings so engineers can tune the recipe. A few records are spikes from a failed sensor, not real process behaviour. |
| ML Translation | Target: etch thickness error in nm; regression; most errors are within 4 nm and one record is a 60 nm sensor spike; train with Huber at δ = 5 nm (the largest error engineers still treat proportionally). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The squared part keeps learning precise on normal wafers; the linear part caps the spike's pull at 5 nm instead of 60 nm. |
| Why other metrics are NOT suitable here | MSE: the 60 nm spike supplies almost all of the loss and drags the recipe; MAE: not smooth at zero, so fine-tuning near the optimum is slow; Tukey biweight: would ignore the spike but is non-convex and needs a careful start, which is overkill for occasional spikes. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A recipe nudged to fit a broken sensor can push whole lots of wafers out of spec; scrapping a lot costs far more than repairing the sensor. |
| Small numeric example | Errors (nm): 2, −3, 4, −2, 60; δ = 5. Huber: 0.5×4 = 2; 0.5×9 = 4.5; 0.5×16 = 8; 0.5×4 = 2; spike 5×(60 − 2.5) = 287.5; sum 304; mean 60.8. Half-MSE = (4+9+16+4+3600)/5/2 = 363.3. Pull of the spike on the model: 60 under MSE, 5 under Huber (12 times smaller). |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Fare quotes with GPS glitches |
| Industry / Domain | Transport (ride-hailing, Indonesia) |
| Business Problem | A ride-hailing app in Jakarta predicts the fare of each trip. A few trips carry a GPS jump that creates a fake very long distance and a huge fare. |
| ML Translation | Target: fare in thousand rupiah; regression; 7 normal trips with errors under 5 and 1 glitch trip with error 80; Huber with δ = 10 (a fare error above Rp 10,000 is simply "wrong" to a rider whether it is 10,000 or 80,000). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Normal trips are fitted precisely, while the glitch trip pulls by at most 10 no matter how big the glitch is. |
| Why other metrics are NOT suitable here | MSE: the glitch trip makes the model overprice ordinary trips; MAE: robust but non-smooth, so convergence is slower and noisier; log-cosh: its switch point is fixed near an error of 1, so on this scale it behaves like MAE and offers no tunable threshold. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Overpriced quotes on normal trips push riders to cancel and rival apps, and underpriced ones cost driver earnings. |
| Small numeric example | Errors: 3, −2, 4, −5, 1, −3, 2, 80; δ = 10. Huber mean = 98.0 (outlier charge 10×(80 − 5) = 750); MAE = 12.5; half-MSE = 404.25. If the glitch were 800 instead of 80, Huber's charge rises to 7,950 but its pull stays capped at 10, while MSE's pull would grow from 80 to 800. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Coffee price forecasts after a storm shock |
| Industry / Domain | Agriculture (commodity trading, Vietnam) |
| Business Problem | A coffee cooperative in the Central Highlands predicts the daily green-bean purchase price per kg. One storm-shock day produced a price swing the model cannot foresee, and the cooperative re-prices contracts above a fixed gap anyway. |
| ML Translation | Target: price in VND per kg; regression; 5 days, four with errors under 800 and one storm day with error 5,000; Huber with δ = 1,000 VND per kg taken from the contract re-pricing rule. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | δ has a business meaning: beyond a 1,000 VND gap the contract is re-priced, so extra error does not cost proportionally more. |
| Why other metrics are NOT suitable here | MSE: one storm day would dominate the fit; MAE: ignores the useful fact that small errors are worth tracking closely and is non-smooth; quantile loss: the cost here is symmetric, so an asymmetric loss adds nothing. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A model bent by one storm day mis-prices the normal days and the cooperative either overpays farmers or loses the buyers' orders. |
| Small numeric example | Errors (VND/kg): 400, −600, 800, −300, 5,000; δ = 1,000. Huber: 80,000 + 180,000 + 320,000 + 45,000 + 1,000×(5,000 − 500) = 4,500,000; sum 5,125,000; mean 1,025,000. Half-MSE = 26,250,000/5/2 = 2,625,000, so Huber charges 61% less. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Packers per shift when short staff costs six times more |
| Industry / Domain | E-commerce (fulfilment centre, Vietnam) |
| Business Problem | A fulfilment centre in Ho Chi Minh City plans how many packers to roster per shift. A missing packer costs 300 thousand VND (overtime and late-parcel penalties); an idle packer costs 50 thousand VND. |
| ML Translation | Target: packers needed per shift; regression; 7 shifts (18, 20, 21, 22, 23, 25, 30); the planner proposes a Huber loss with δ = 3 to handle the busy outlier shift. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Huber handles outliers but is symmetric: it aims near the typical value (about 22) and treats short and long errors alike, so it cannot know that shortage is six times worse. |
| Why other metrics are NOT suitable here | MSE and MAE: also symmetric, so they would also staff near the average; log-cosh: symmetric as well; epsilon-insensitive loss: a symmetric tolerance band with no cost direction. |
| Better alternative (if BAD fit) | Quantile (pinball) loss with τ = 300/(300+50) = 0.857, because the right answer is a high percentile of demand, not a central value. |
| Business impact of choosing wrong | Chronic under-rostering means overtime and late parcels on one shift in three. |
| Small numeric example | Huber fit ≈ 22 packers: short 12 packers × 300 = 3,600 plus idle 7 × 50 = 350, total 3,950 thousand VND. Quantile fit (τ = 0.857) = 25 packers: short 5 × 300 = 1,500 plus idle 21 × 50 = 1,050, total 2,550. Quantile saves 1,400 (35%). |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Choosing a champion model by its Huber score |
| Industry / Domain | Banking (credit-limit forecasting, Japan) |
| Business Problem | A bank's model-risk team must pick a champion between two credit-limit forecasting models and wants to compare them on one headline number: the Huber loss. |
| ML Translation | Target: balance error in thousand yen on 6 accounts; Model A has five errors of 1 and one of 30; Model B has six errors of 6; the Huber score is used as a reported metric. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Huber is a training objective: its value mixes units and depends on δ, so the model ranking flips just by changing δ. |
| Why other metrics are NOT suitable here | Log-cosh: also a mixed-unit training loss with a fixed switch point; Tukey biweight: its value is capped and tells a committee even less; quantile loss: a different target (a percentile), not a general accuracy score. |
| Better alternative (if BAD fit) | Report MAE and RMSE (both in yen, with no δ to argue about), and use Huber only to train. |
| Business impact of choosing wrong | A committee may sign off the model that is worse at its own tolerance for large misses, leaving the bank exposed to big limit errors. |
| Small numeric example | Huber at δ = 1: A = (5×0.5 + 29.5)/6 = 5.33, B = 5.50, so A wins. At δ = 5: A = 23.33, B = 17.50, so B wins. MAE: A 5.83, B 6.00 (A wins). RMSE: A 12.28, B 6.00 (B wins). The ranking depends on the choice, so the committee must see MAE and RMSE. |

**6. Quick decision rule:** Use Huber loss when the data has occasional extreme or wrongly recorded values and you want smooth, stable training with a threshold you can justify in business terms; avoid it when costs are asymmetric, when you need a headline metric to report, or when the extreme values are real and drive the money.

### Log-cosh Loss

**1. What it measures (plain English):** Log-cosh loss takes the logarithm of the hyperbolic cosine of each error. For small errors it behaves like half the squared error, and for large errors like the absolute error minus about 0.693. It is smooth everywhere and has no δ to tune, but its switch point is fixed near an error of 1 unit. Aliases: logcosh; its parameterised cousin is pseudo-Huber loss.

`LogCosh = (1/n) × Σ log(cosh(yᵢ − ŷᵢ))`

**2. Intuition:** A dimmer switch instead of an on/off switch: Huber flips from squared to linear at one exact error size, while log-cosh slides smoothly between the two around an error of 1 unit.

**3. Benefits:**

- No threshold to tune in its plain form.
- Smooth in every order (twice differentiable), which suits boosting libraries that use curvature (second-order information) to choose splits.
- Its push on the model is capped automatically below 1 (the gradient is tanh of the error), so one extreme record cannot dominate.
- Convex, so training has a single best answer for linear models.

**4. Limitations / Potential issues:**

- The switch point is fixed near an error of 1, so on large-valued targets it silently becomes MAE and on tiny-valued targets it becomes MSE; scale the target first or use pseudo-Huber with a δ.
- The loss value is not interpretable; report MAE and RMSE.
- Naive code overflows for errors above about 710; use a stable form.
- Still symmetric, and extreme points keep a maximum (not zero) influence.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Vibration scores on a Japanese machining line |
| Industry / Domain | Manufacturing (precision machining, Japan) |
| Business Problem | A machine-tool plant predicts a standardised vibration score for each cutting cycle to schedule tool changes; an occasional sensor knock creates a spike. |
| ML Translation | Target: vibration score already standardised (mean 0, spread 1); regression with a neural network; errors mostly between −0.4 and 0.3, plus one spike of 3.0. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Errors live on the scale of 1, exactly where log-cosh switches from squared to linear, so it is smooth near zero and capped for the spike with no δ to tune. |
| Why other metrics are NOT suitable here | MSE: the spike would supply most of the loss; MAE: non-smooth at zero, so late-stage fine-tuning of the network is noisier; Huber: works too, but needs a δ choice that adds nothing on an already standardised target. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Chasing knocks makes the model flag healthy tools for replacement, wasting tool cost and machine downtime. |
| Small numeric example | Errors: 0.2, −0.4, 0.3, −0.1, 3.0. Log-cosh values: 0.0199, 0.0780, 0.0443, 0.0050, 2.3093; mean 0.491. Half-MSE = (0.02+0.08+0.045+0.005+4.5)/5 = 0.93. The spike's push is tanh(3.0) = 0.995 versus 3.0 under squared error (5 times a normal record versus 15 times). |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Boosted trees on standardised basket values |
| Industry / Domain | E-commerce (super-app, South Korea) |
| Business Problem | A super-app predicts each order's basket value (standardised) with gradient-boosted trees that use curvature to pick splits; a few bulk corporate orders are extreme. |
| ML Translation | Target: z-scored basket value; regression with second-order boosting; heavy right tail from bulk orders; a loss with a smooth curvature is needed. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Log-cosh has a smoothly changing curvature, so the tree-splitting calculations stay stable, and its capped push tames the bulk orders. |
| Why other metrics are NOT suitable here | Huber: its curvature jumps from 1 to 0 at the switch point, which unsettles second-order split finding; MAE: has no curvature at all, so second-order boosting cannot use it; MSE: bulk orders would dominate the splits. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | An unstable loss gives a noisy basket forecast that misguides promotion budgets. |
| Small numeric example | Curvature at error 0.9 and 1.1: Huber (δ = 1) gives 1 then 0, an abrupt jump. Log-cosh gives 0.487 then 0.359, a smooth change (curvature = 1 − tanh²(e)). At error 0 it is 1.0 and at error 3 it is 0.0099. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Motorbike auction prices in raw rupiah |
| Industry / Domain | Banking (motorbike financing, Indonesia) |
| Business Problem | A lender predicts the auction price of repossessed motorbikes in full rupiah to set loan recovery targets. |
| ML Translation | Target: price in rupiah (values in the millions); regression; errors of hundreds of thousands, one of 2.5 million; log-cosh used on the raw target. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Every error is far above 1, so log-cosh never uses its squared region: it equals MAE minus 0.693, giving no smoothness benefit and no robustness knob. |
| Why other metrics are NOT suitable here | MSE: one 2.5 million error would dominate; plain MAE: honest but non-smooth; quantile loss: not needed since cost is symmetric here. |
| Better alternative (if BAD fit) | Huber or pseudo-Huber with δ near 500,000 rupiah, or standardise the target first so errors become order 1. |
| Business impact of choosing wrong | The team believes it trained a smooth robust model but gets MAE behaviour, wasting tuning time and leaving recovery targets less stable. |
| Small numeric example | Errors (rupiah): 400,000; −250,000; 300,000; −350,000; 2,500,000. MAE = 760,000; log-cosh = 759,999.31 = MAE − 0.693. After dividing by 1,032,763 the errors become 0.39, −0.24, 0.29, −0.34, 2.42, and log-cosh values become 0.07, 0.03, 0.04, 0.06, 1.74, in its useful range. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Promising transit days when late costs eight times more |
| Industry / Domain | Logistics (freight forwarding, China) |
| Business Problem | A freight forwarder quotes factory-to-port transit days to exporters. A late day costs ¥800 in penalties; an early day costs ¥100 in storage. |
| ML Translation | Target: transit days; regression; 7 past shipments (10, 11, 12, 12, 13, 14, 18); a log-cosh model learns a typical value of about 12 days. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Log-cosh is symmetric: it promises the typical time, so the forwarder is late on roughly 3 of 7 shipments. |
| Why other metrics are NOT suitable here | MSE and MAE: also target the centre, with the same flaw; Huber: only handles outliers, not direction; epsilon-insensitive loss: a symmetric tolerance band that ignores the cost ratio. |
| Better alternative (if BAD fit) | Quantile loss with τ = 800/(800+100) = 0.889, promising a high percentile of transit days. |
| Business impact of choosing wrong | Late penalties pile up on a promise that is broken nearly half the time. |
| Small numeric example | Promise 12 days: late days (13→1, 14→2, 18→6) = 9, ×¥800 = 7,200; early days 3 × ¥100 = 300; total ¥7,500. Promise 18 days (top quantile on 7 shipments): no late days; early days 36 × ¥100 = ¥3,600. The quantile promise cuts cost by 52%. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Packet-loss fractions are too small for log-cosh |
| Industry / Domain | Telecom (network operations, Thailand) |
| Business Problem | A telecom operator predicts packet-loss as a fraction (0.002 to 0.005 per cell site) and wants to be robust to an occasional measurement spike of 0.08. |
| ML Translation | Target: packet-loss fraction between 0 and 1; regression; errors of 0.002 to 0.005 plus one spike of 0.08; log-cosh chosen for robustness. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | All errors are far below 1, so log-cosh stays in its squared region and behaves exactly like MSE: the spike keeps its full 20 times pull. |
| Why other metrics are NOT suitable here | MSE: no protection from the spike; MAE: robust but non-smooth; Tukey biweight: would ignore the spike but needs careful starting values and a tuned cut-off. |
| Better alternative (if BAD fit) | Huber or pseudo-Huber with δ = 0.01, or rescale the target to percentage points so errors are order 1. |
| Business impact of choosing wrong | Spikes distort the model, triggering false capacity upgrades at healthy cell sites. |
| Small numeric example | Errors: 0.004, −0.003, 0.005, −0.002, 0.08. Log-cosh mean = 0.000645; half-MSE = 0.000645 (identical). Pull of the spike relative to a 0.004 error: log-cosh tanh(0.08)/tanh(0.004) = 20.0 times, same as MSE. Huber with δ = 0.01 caps it at 0.01/0.004 = 2.5 times. |

**6. Quick decision rule:** Use log-cosh when the target is standardised (typical errors near 1) and you want a smooth robust loss with no threshold, especially with curvature-based optimisers; avoid it on raw large- or small-valued targets, when costs are asymmetric, or when you need a reportable metric.

### Quantile Loss (Pinball Loss)

**1. What it measures (plain English):** Quantile loss charges different prices for predicting too low and too high. For a target quantile τ ("tau", between 0 and 1) a miss on the low side costs τ per unit and a miss on the high side costs 1 − τ per unit. A model trained on it predicts the value the actual outcome stays below τ of the time (a percentile: τ = 0.9 is the 90th percentile). Aliases: pinball loss, quantile regression loss.

`Pinball_τ = (1/n) × Σ max(τ·(yᵢ − ŷᵢ), (τ − 1)·(yᵢ − ŷᵢ));  τ* = C_under / (C_under + C_over)`

**2. Intuition:** Leaving for the airport. Arriving early costs a little waiting time; missing the flight costs a ticket. So you do not leave at the average travel time; you leave with a generous buffer, a high percentile of the trip.

**3. Benefits:**

- Encodes unequal costs directly; no symmetric loss can do this.
- τ can be derived from costs: τ = cost of being too low divided by (cost too low + cost too high), the classic "newsvendor" (stocking) rule.
- Two models (for example τ = 0.05 and 0.95) give a prediction interval with no assumption about the shape of the errors.
- Robust, since it is a weighted absolute error.

**4. Limitations / Potential issues:**

- One model per quantile; the quantiles can cross (a 5th percentile above the 95th) unless sorted or constrained.
- High or low quantiles (above 0.99) need a lot of data, because very few records sit in the tail.
- Quantiles do not add up: the sum of the 90th percentiles of parts is not the 90th percentile of the total.
- Loss values cannot be compared across different τ; always check coverage (the share of actuals below the prediction should be about τ).

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Quoting berth-ready time when a late vessel costs nine times more |
| Industry / Domain | Logistics (container terminal, Singapore) |
| Business Problem | A terminal quotes shipping lines the time a vessel will wait before a berth is ready. A late berth costs S$900 per hour in waiting charges; an idle berth hour costs S$100. |
| ML Translation | Target: waiting hours; regression; 5 past calls (6, 8, 9, 10, 14); τ = 900/(900+100) = 0.9. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The cost ratio is nine to one, so the quote should be the 90th percentile; pinball loss at τ = 0.9 trains exactly that. |
| Why other metrics are NOT suitable here | MAE: treats early and late equally and would prefer the median quote, which is the more expensive one here; MSE: targets the mean, with the same flaw; Huber: handles outliers but not direction. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Median quotes mean frequent late berths and waiting charges, and strained relations with shipping lines. |
| Small numeric example | Quote A = 9 h (median), quote B = 13 h. Pinball at 0.9: A errors (−3, −1, 0, +1, +5) charge 0.3+0.1+0+0.9+4.5 = 5.8, mean 1.16; B errors (−7, −5, −4, −3, +1): 0.7+0.5+0.4+0.3+0.9 = 2.8, mean 0.56. Cost: A = 6 late h × 900 + 4 early h × 100 = S$5,800; B = 1 × 900 + 19 × 100 = S$2,800. MAE says A is better (2.0 against 4.0) but A costs double. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Rice-ball batches where waste costs more than a missed sale |
| Industry / Domain | Retail (convenience stores, Japan) |
| Business Problem | A convenience-store chain decides how many fresh rice balls to make each morning. A missed sale loses ¥120 of margin; a leftover ball costs ¥200 in waste. |
| ML Translation | Target: units demanded per day; regression; 7 days (38, 40, 41, 43, 45, 47, 52); τ = 120/(120+200) = 0.375, a low quantile. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Waste is costlier than a missed sale, so the best batch is below the average; a low τ trains exactly that. |
| Why other metrics are NOT suitable here | MAE: aims at the median (43) and over-produces; MSE: aims at the mean (about 44) and over-produces more; Huber: robust but symmetric. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Daily over-production adds up to waste across hundreds of stores. |
| Small numeric example | Batch 41 (the 0.375 quantile): short 2+4+6+11 = 23 × 120 = 2,760; leftover 3+1 = 4 × 200 = 800; total ¥3,560. Batch 43 (median): ¥3,800. Batch 44 (about the mean): short 12 × 120 = 1,440, leftover 14 × 200 = 2,800, total ¥4,240. Quantile batch is 16% cheaper than the mean batch. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Server capacity for flash-sale evenings |
| Industry / Domain | Technology (super-app platform, Vietnam) |
| Business Problem | A super-app must reserve server capacity before flash-sale evenings. Unserved load costs 95 million VND per thousand requests per second per evening (an outage); idle capacity costs 5 million. |
| ML Translation | Target: peak load in thousand requests per second; regression; toy sample of 5 evenings (120, 135, 150, 160, 210); τ = 95/100 = 0.95. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | An outage is 19 times costlier than idle capacity, so capacity should cover a very high percentile of load, not the average (with real data, use hundreds of evenings; five toy days cannot truly support a 95th percentile). |
| Why other metrics are NOT suitable here | MSE: provisions for the mean load and is overloaded on the biggest evenings; MAE: provisions for the median, the same flaw; R-squared: a score of fit that says nothing about the cost of being short. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Average-based capacity fails on exactly the days with most customers, costing sales and trust. |
| Small numeric example | Provision 155 (the mean): short (160−155) + (210−155) = 60 × 95 = 5,700; idle 35+20+5 = 60 × 5 = 300; cost 6,000. Provision 210 (top of the sample): idle 90+75+60+50 = 275 × 5 = 1,375. Pinball at 0.95: 12.0 against 2.75. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Adding up the 90th percentiles of two estates |
| Industry / Domain | Agriculture (palm-oil estates, Indonesia) |
| Business Problem | A palm-oil group wants to plan mill capacity for the combined harvest of two estates and adds the two estates' 90th-percentile harvest forecasts to get the group's 90th percentile. |
| ML Translation | Target: harvest in tonnes; each estate has 10 equally likely outcomes (A: 60 to 150, B: 120 to 210, steps of 10), independent of each other; quantile loss at τ = 0.9 per estate, then summed. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Quantiles do not add. It is unlikely that both estates have a great harvest together, so the sum of the two 90th percentiles overstates the group's 90th percentile. |
| Why other metrics are NOT suitable here | MSE or MAE on estate forecasts: sums of means do add, but they give no safety margin; Huber: no percentile meaning; WAPE: reports accuracy, not a capacity level. |
| Better alternative (if BAD fit) | Train a quantile model directly on the group total, or simulate the joint distribution of the estates and read off its 90th percentile. |
| Business impact of choosing wrong | Mill capacity and trucking are over-booked every season, a permanent cost for no extra safety. |
| Small numeric example | P90 of A = 140; P90 of B = 200; sum = 340. All 100 combinations of A and B give a total P90 of 320 (mean total 270). The 340 figure is really the 97th percentile, so it over-reserves by 20 tonnes (6%). |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — The 99.9th percentile of ICU demand from eight weeks of data |
| Industry / Domain | Healthcare (hospital capacity planning, Singapore) |
| Business Problem | A hospital wants the number of ICU beds that will be enough on 999 weeks in 1,000 and trains a quantile model at τ = 0.999 on only eight weeks of peak occupancy. |
| ML Translation | Target: weekly peak ICU beds occupied; regression; 8 weeks (22, 25, 27, 28, 30, 31, 33, 36). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | With 8 points, any τ above 7/8 = 0.875 can only return the largest observed value, so the "99.9th percentile" is simply last year's worst week. |
| Why other metrics are NOT suitable here | MAE: gives the median, far too low for a safety target; MSE: gives the mean, the same flaw; Huber: no tail meaning. |
| Better alternative (if BAD fit) | Extreme-value statistics (fit a tail curve to the biggest weeks) or a simulation or queueing model, with many more weeks of data. |
| Business impact of choosing wrong | The hospital believes it has a rigorous safety level when it only copied one past peak; a rarer surge finds it without beds. |
| Small numeric example | τ = 0.5 gives 28; τ = 0.875 gives 33; τ = 0.9, 0.99 and 0.999 all give 36 (the maximum). The three "different" safety levels are the same number, so the data cannot support them. |

**6. Quick decision rule:** Use quantile loss when being too low and too high cost different amounts, or when you need a percentile or a prediction interval; avoid it for very extreme percentiles with little data, and never add percentiles up a hierarchy.

### Epsilon-insensitive Loss

**1. What it measures (plain English):** Epsilon-insensitive loss charges nothing for errors smaller than a tolerance ε ("epsilon") and charges the excess beyond ε in proportion. It is the loss used by Support Vector Regression (SVR). Only records outside the tolerance band (the "support vectors") shape the model. Aliases: ε-insensitive loss, SVR loss.

`EpsLoss = (1/n) × Σ max(0, abs(yᵢ − ŷᵢ) − ε)`

**2. Intuition:** A machinist's tolerance. A part within ±5 micrometres of spec passes with no penalty; only the part outside the tolerance is rejected, and it is rejected by how far it is out.

**3. Benefits:**

- Encodes a real tolerance: errors that make no practical difference cost nothing.
- Produces compact (sparse) models, because only support vectors matter.
- Linear beyond the band, so it is robust to outliers.
- Convex, with a single best answer.

**4. Limitations / Potential issues:**

- ε must be chosen on the scale of the target; scale the target before using SVR.
- Records inside the tube give no learning signal; a wide ε can leave only a handful of records teaching the model.
- Kernel SVR is slow on large data (roughly n² to n³).
- The loss value is not interpretable, and the model gives no probabilities or intervals.
- Symmetric, so it cannot encode a higher cost for one direction.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Bearing diameters inside a ±5 micrometre tolerance |
| Industry / Domain | Manufacturing (precision bearings, Japan) |
| Business Problem | A bearing maker uses a surrogate model to predict the ground diameter of each part before final inspection. Anything within ±5 micrometres of the model is treated as in spec. |
| ML Translation | Target: diameter deviation in micrometres; regression with SVR; 6 parts with errors (2, −3, 4, −1, 9, −7); ε = 5 from the engineering drawing. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The tolerance is a real physical fact, so charging for errors inside it measures something nobody cares about. |
| Why other metrics are NOT suitable here | MAE: charges every micrometre even inside tolerance, so the model chases noise; MSE: even more, and it explodes on rare large misses; Huber: smooth but has no zero-cost zone. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A model that chases within-tolerance noise is slower and larger, and its extra complexity adds cost without improving parts. |
| Small numeric example | Errors: 2, −3, 4, −1, 9, −7; ε = 5. Charges: 0, 0, 0, 0, 4, 2; sum 6; loss = 6/6 = 1.0. MAE = 26/6 = 4.33. Only 2 of 6 parts (33%) shape the model. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Kitchen prep-time estimates with a five-minute grace |
| Industry / Domain | Logistics (instant delivery, China) |
| Business Problem | An instant-delivery platform predicts restaurant prep time to dispatch riders. A rider who arrives within five minutes of the food being ready waits without any real cost. |
| ML Translation | Target: prep time error in minutes; regression with SVR; 6 orders with errors (1, −4, 3, −2, 8, −10); ε = 5 minutes. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Within five minutes there is no operational difference, so only the larger misses should drive the model. |
| Why other metrics are NOT suitable here | MAE: charges small harmless errors the same as the useful signal; MSE: lets one 10-minute miss dominate; quantile loss: not needed, since the grace window is symmetric. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Dispatch rules tuned to noise inside the window waste rider time without improving on-time delivery. |
| Small numeric example | Errors: 1, −4, 3, −2, 8, −10; ε = 5. Charges: 0, 0, 0, 0, 3, 5; sum 8; loss = 8/6 = 1.33. MAE = 28/6 = 4.67. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — A free band on a rice cargo where every dollar counts |
| Industry / Domain | Agriculture (rice export trading, Vietnam) |
| Business Problem | A rice exporter forecasts the price per tonne for 50,000-tonne cargoes, and the team copies a tolerance of 5 USD per tonne from another project. |
| ML Translation | Target: price in USD per tonne; regression; 6 forecasts with errors (2, −3, 4, −1, 3, −2); epsilon-insensitive loss with ε = 5. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | There is no real tolerance: each dollar on 50,000 tonnes is real money, yet the loss reports a perfect zero. |
| Why other metrics are NOT suitable here | Huber: designed for outliers, not exactness of small errors; log-cosh: scale issues and not interpretable in dollars; MAPE: hides the cargo size in percentages. |
| Better alternative (if BAD fit) | MAE (or RMSE) in USD per tonne, converted into dollars per cargo. |
| Business impact of choosing wrong | The model appears perfect while mis-pricing every cargo by a few dollars a tonne, which is real money on each shipment. |
| Small numeric example | Errors: 2, −3, 4, −1, 3, −2; ε = 5: every charge is 0, loss = 0.0. MAE = 15/6 = 2.5 USD per tonne; × 50,000 tonnes = USD 125,000 per cargo. RMSE = 2.68. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — A tolerance so wide that one patient teaches the model |
| Industry / Domain | Healthcare (hospital stays, South Korea) |
| Business Problem | A hospital predicts length of stay in days for bed planning, and sets ε = 3 days "to ignore small differences". |
| ML Translation | Target: days of stay; regression with SVR; 8 patients with errors (0.5, −1, 1.5, −0.5, 1, −1.5, 0.8, 6). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | With ε = 3, only the 6-day miss lies outside the tube, so one patient out of eight teaches the model and the rest give no signal. |
| Why other metrics are NOT suitable here | MSE: dominated by the one 6-day case; Huber: robust, but has no zero zone; quantile loss: the cost here is not clearly asymmetric. |
| Better alternative (if BAD fit) | Huber or MAE so that every patient teaches the model, or an ε set from a real operational tolerance such as 1 day. |
| Business impact of choosing wrong | Bed forecasts rest on a single data point, so wards are mis-staffed. |
| Small numeric example | ε = 3: charges all 0 except 6 − 3 = 3; loss = 3/8 = 0.375; 1 of 8 patients (12.5%) contributes. ε = 1: charges 0.5, 0.5 and 5 only; loss = 6/8 = 0.75; 3 of 8 contribute. MAE = 12.8/8 = 1.6. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Kernel SVR on forty million payments a day |
| Industry / Domain | Fintech (mobile payments, China) |
| Business Problem | A payments app wants to predict transaction fees per merchant from a day of 40 million transactions and proposes kernel SVR for its tolerance band. |
| ML Translation | Target: fee in yuan; regression; 40 million rows per day; kernel SVR with an epsilon-insensitive loss. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Kernel SVR needs a table comparing every record with every other, which is impossible at this size, however good the loss is. |
| Why other metrics are NOT suitable here | MSE and MAE: fine to compute at scale, but are not the issue; quantile loss: not needed unless costs are asymmetric; log-cosh: scale-sensitive on raw fees. |
| Better alternative (if BAD fit) | Gradient boosting with a Huber loss, or a linear model with the same epsilon-insensitive loss (LinearSVR) that scales to millions of rows. |
| Business impact of choosing wrong | The training job never finishes, wasting weeks of engineering time and delaying fee forecasts. |
| Small numeric example | n = 40,000,000. The kernel table has n × n = 1.6 × 10^15 entries; at 8 bytes each that is 1.6 × 10^15 × 8 = 12.8 × 10^15 bytes, about 12.8 petabytes. |

**6. Quick decision rule:** Use epsilon-insensitive loss when there is a genuine tolerance below which errors do not matter and the data is small or medium sized; avoid it when every unit of error costs money, when ε would leave very few records teaching the model, or when the data is huge.

### Tukey's Biweight Loss

**1. What it measures (plain English):** Tukey's biweight (bisquare) loss is squared for small errors, flattens as errors grow and is completely flat beyond a cut-off c, so a wildly wrong record gets zero pull on the model. It is a "redescending" loss: influence rises, then falls back to zero. It is typically used when some records are plain mistakes, not just rare. Aliases: biweight loss, bisquare loss.

`Tukey_c(e) = (c²/6)·(1 − (1 − (e/c)²)³) if abs(e) ≤ c, otherwise c²/6;  c is commonly 4.685 × a robust measure of spread`

**2. Intuition:** A panel of judges throws out any score that is obviously impossible, rather than just capping its weight. Reasonable scores count; a score of 270 on a ten-point scale counts for nothing.

**3. Benefits:**

- The strongest protection against gross errors (typos, sensor failures, unit mix-ups): their influence drops to exactly zero.
- Behaves like MSE for normal records, so it is efficient when the data is clean.
- Can survive a large share of bad records (a high "breakdown point").

**4. Limitations / Potential issues:**

- Not convex: there are several "best answers" (local minima), so the result depends on the starting point; usually start from a Huber or median fit.
- It can reject real extreme records (catastrophes, peak days), which is dangerous if the tail is real.
- The cut-off c must be tuned and depends on the target's scale; rarely available in mainstream machine-learning libraries.
- If every record is beyond c, the training signal vanishes (zero slope); the loss value is not interpretable.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Truck weights with a slipped decimal point |
| Industry / Domain | Logistics (port weighbridge, Vietnam) |
| Business Problem | A port's model predicts the weight of each loaded truck from the declared cargo. A few weighbridge entries contain a misplaced decimal and show hundreds of tonnes too much. |
| ML Translation | Target: truck load in tonnes; regression; errors (0.4, −0.3, 0.5, −0.2, 0.3) and one gross error of +270; robust spread 0.5 t, so c = 4.685 × 0.5 = 2.34 t. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The 270 t record is a typing mistake, not a truck; Tukey gives it exactly zero influence and uses the clean records normally (start the fit from a median or Huber estimate). |
| Why other metrics are NOT suitable here | Huber: the typo still pulls with its full capped force (0.675 per record), more than any normal record; MSE: the typo would wreck the fit; MAE: robust to the typo but non-smooth, and discards fine precision on the clean trucks. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Weight forecasts bent by typos mis-bill customers and cause overloaded-truck penalties. |
| Small numeric example | Tukey charges: 0.078, 0.044, 0.119, 0.020, 0.044 and for 270 exactly c²/6 = 0.915; mean 0.203. Huber (δ = 0.675) charges 182.0 for the 270 record, and 1,822.3 if the typo were 2,700; Tukey still charges 0.915. Its pull on the fit is 0 under Tukey and 0.675 under Huber. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Two dead thermocouples in a reflow oven |
| Industry / Domain | Manufacturing (circuit-board assembly, China) |
| Business Problem | A circuit-board plant estimates the typical temperature offset of its reflow oven from 8 readings; two thermocouples failed and wrote values over 1,000 °C. |
| ML Translation | Target: temperature offset in °C; robust location estimate; readings (3, −2, 4, −3, 2, −4, 1,190, 1,230); c = 14 °C; start from the median. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The two failures are sensor faults (25% of the data), not oven behaviour; Tukey rejects them fully. |
| Why other metrics are NOT suitable here | Huber: each failure still pulls by δ, leaving a visible bias; MSE or the mean: dragged to 302.5 °C; MAE or the median: robust, but less efficient on clean readings. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A biased oven offset leads to wrong profile corrections and cold solder joints that fail in the field. |
| Small numeric example | Clean readings average (3−2+4−3+2−4)/6 = 0.0. Mean of all 8 = 302.5; median = 2.5; Huber (δ = 4) estimate = 1.75; Tukey (c = 14) estimate = 0.0. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Throwing away the 12.12 sale day |
| Industry / Domain | E-commerce (mega-sale planning, Indonesia) |
| Business Problem | A marketplace estimates daily order volume to size warehouses. The 12.12 mega-sale day is 2.8 times normal volume, and the team removes it as an "outlier" using Tukey. |
| ML Translation | Target: orders in thousands per day; location estimate; 6 normal days (100, 104, 98, 102, 96, 101) and one sale day (280); Tukey with c = 12. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The sale day is real and exactly the day capacity must be built for; Tukey treats it as a mistake and gives it no weight. |
| Why other metrics are NOT suitable here | Huber with a small δ: also down-weights the sale day; MAE: aims at the median and ignores the peak; epsilon-insensitive loss: has no peak sensitivity. |
| Better alternative (if BAD fit) | MSE or a high quantile (τ = 0.95) with a sale-day flag as a feature, so the peaks are modelled, not rejected. |
| Business impact of choosing wrong | Warehouses are sized for 100 thousand orders on a 280 thousand day, causing late parcels and refunds on the most visible day of the year. |
| Small numeric example | Tukey (c = 12) baseline = 100.2; Huber (δ = 6) = 101.2; Huber (δ = 100) = 116.8; mean = 125.9. The 0.95 quantile of the 7 days = 280. Using the Tukey baseline leaves a gap of about 180 thousand orders on sale day. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Island hotels in two price worlds |
| Industry / Domain | Hospitality (hotel pricing, Thailand) |
| Business Problem | A hotel group estimates a typical nightly rate for a new island from 6 comparable properties: three budget guesthouses and three luxury resorts. |
| ML Translation | Target: rate in USD; location estimate; values (40, 42, 44, 180, 184, 188); Tukey with c = 12. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Tukey's loss has two separate best answers, one per cluster, and the answer depends on the starting point; from the overall average every record is out of reach and the slope is zero. |
| Why other metrics are NOT suitable here | MSE: gives a rate of 113 that matches no property; MAE or median: lands between the clusters at 112; Huber: also averages across clusters. |
| Better alternative (if BAD fit) | Segment the properties first (budget versus luxury, a class feature), then fit a Huber model inside each segment. |
| Business impact of choosing wrong | The pricing model prices the island for the wrong market, or flips between runs depending on the starting value. |
| Small numeric example | Loss at 43 = 77.2; at 184 = 86.3 (two local minima); at the average 113 all 6 records are beyond c, loss = 6 × 24 = 144 and the slope is 0 (stuck). Starting at 43 ends at 42; starting at 184 stays at 184. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Ignoring the earthquake claim |
| Industry / Domain | Insurance (property reinsurance, Japan) |
| Business Problem | A reinsurer sets a typical claim reserve per region for 5 regions; one region had a genuine large earthquake claim. |
| ML Translation | Target: claim in million yen; location estimate; values (10, 12, 9, 11, 95); Tukey with c = 15, start at the median. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The 95 million claim is a real, rare event that drives the total payout; Tukey classes it as an error and rejects it. |
| Why other metrics are NOT suitable here | Huber: down-weights the big claim so totals are too low; MAE or median: aims at 11, ignoring the tail; epsilon-insensitive loss: no tail sensitivity. |
| Better alternative (if BAD fit) | MSE or a mean-based deviance (Gamma) for expected totals, plus a high quantile or extreme-value model for capital. |
| Business impact of choosing wrong | Reserves miss the biggest claims, so the insurer is short of money in the exact event it exists to cover. |
| Small numeric example | Mean = 27.4, so 5 regions need 137. Tukey estimate = 10.5, so 5 regions = 52.5; Huber (δ = 3) = 11.25, so 56.25. Shortfall under Tukey = 137 − 52.5 = 84.5 million yen. |

**6. Quick decision rule:** Use Tukey's biweight when part of the data is plainly wrong (typos, dead sensors, unit mix-ups) and you can start from a Huber or median fit; avoid it when extreme values are real events, when the data has several genuine groups, or when you need a convex loss.

## Monitoring, Aggregation, Deviance and Direction Metrics

### Tracking Signal

**1. What it measures (plain English):** The tracking signal adds up a forecast's signed errors over time (actual minus forecast) and divides by the mean absolute deviation (MAD, the average size of the errors regardless of sign). Random errors cancel out and the signal stays near zero; a steady bias piles up and the signal drifts out of its control limits, conventionally ±4 (strict) to ±6 (loose). Aliases: cumulative forecast error ratio, RSFE/MAD.

`Tracking Signal = Σ(yₜ − ŷₜ) / MAD`

**2. Intuition:** A bathroom scale that reads a little light. One weighing looks fine, but if you add up the daily differences from a trusted scale, the total drifts steadily one way and tells you something is wrong.

**3. Benefits:**

- Catches a small, persistent bias much sooner than looking at the error of each period.
- Cheap to compute on a stream, and one threshold works across items of different volume, since it is scale-free.
- The sign tells you the direction at once: positive means under-forecasting, negative means over-forecasting.
- A long-standing standard in demand planning, so it needs little explanation.

**4. Limitations / Potential issues:**

- It detects only bias, not accuracy: huge errors that alternate in sign give a signal near zero.
- The plain cumulative version remembers old errors, so reset it after a fix, or use the smoothed version.
- The signal can never exceed the number of periods n in size, so a limit of 4 cannot fire on a series with fewer than 5 observations.
- With thousands of items, a fixed limit will raise many false alarms by chance; tier the limits by item importance.
- The MAD is noisy on short or intermittent (mostly zero) series.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Phone-case forecasts that drift low |
| Industry / Domain | Retail (consumer electronics accessories, China) |
| Business Problem | An electronics retailer forecasts weekly units for thousands of phone-case SKUs. A rising trend is not captured, and planners want an automatic alert for the drifting ones. |
| ML Translation | Target: weekly units; forecast monitoring; 6 weeks of actuals (200, 208, 206, 222, 230, 239) against forecasts (197, 203, 208, 216, 223, 231); alert limit ±4. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Each weekly miss looks small, but they point the same way, and the tracking signal accumulates them until the item crosses the limit. |
| Why other metrics are NOT suitable here | MAPE: stays near 2%, so nothing looks wrong; MAE: shows size of misses but not that they are all in one direction; R-squared: judges fit to the mean, not a forecast drifting off its trend. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Without an alert the drift continues for weeks, causing stock-outs on the fastest-growing cases. |
| Small numeric example | Errors: +3, +5, −2, +6, +7, +8; cumulative 3, 8, 6, 12, 19, 27; running MAD 3.00, 4.00, 3.33, 4.00, 4.60, 5.17; signal 1.00, 2.00, 1.80, 3.00, 4.13, 5.23. Alert at week 5 (4.13). At week 5 the MAPE is only 2.12% and MAE is 4.6. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Rental forecasts for e-scooter districts |
| Industry / Domain | Transport (shared e-scooters, South Korea) |
| Business Problem | A Seoul e-scooter operator forecasts hourly rentals per district and wants a lightweight monitor that runs on a live stream. |
| ML Translation | Target: rentals per hour; smoothed tracking signal with α = 0.2 (weight on the newest error), start values E = 0 and MAD = 4; errors (+4, −2, +5, +7, +7, +5); alert when the ratio exceeds 0.5. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The smoothed version needs only two stored numbers per district, stays within −1 to +1 and fires when errors lean one way. |
| Why other metrics are NOT suitable here | MAE: does not carry direction; MPE or bias percentage: works, but is noisy on low-volume districts, and gives no ready alert threshold; RMSE: hides the sign. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Scooters are not repositioned in time, causing missed rentals in the districts where demand is rising. |
| Small numeric example | Smoothed error E = 0.2×e + 0.8×previous; smoothed MAD likewise. Week 1: E 0.80, MAD 4.00, ratio 0.20. Week 2: 0.24, 3.60, 0.07. Week 3: 1.19, 3.88, 0.31. Week 4: 2.35, 4.50, 0.52 (alert). Week 5: 0.66. Week 6: 0.72. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Photoresist orders after a line is retired |
| Industry / Domain | Manufacturing (semiconductor materials, South Korea) |
| Business Problem | A fab forecasts weekly photoresist use (litres) to order stock. One line has been phased down but the forecast has not caught up. |
| ML Translation | Target: litres per week; forecast monitoring; 8 weeks of actuals (50, 48, 47, 44, 42, 41, 38, 37) against forecasts (52, 52, 45, 50, 49, 48, 46, 45); limit ±4. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The forecast is above actual in 7 of 8 weeks; the negative signal shows over-forecasting and an inventory pile-up before the shelves fill. |
| Why other metrics are NOT suitable here | MAE: reports the size but not that it is always on one side; MASE: judges accuracy against a naive forecast, not bias direction; RMSE: gives no alert rule. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Over-ordering of expensive, short-shelf-life chemicals is written off. |
| Small numeric example | Errors: −2, −4, +2, −6, −7, −7, −8, −8; cumulative −2, −6, −4, −10, −17, −24, −32, −40; running MAD 2.00, 3.00, 2.67, 3.50, 4.20, 4.67, 5.14, 5.50; signal −1.00, −2.00, −1.50, −2.86, −4.05, −5.14, −6.22, −7.27. Alert at week 5 (−4.05), when 17 litres had been over-ordered. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Shrimp orders that miss high then low |
| Industry / Domain | Agriculture (seafood exports, Vietnam) |
| Business Problem | A shrimp exporter relies on a tracking signal alone to certify that its weekly order forecast is good. |
| ML Translation | Target: tonnes ordered per week; 6 weeks of actuals (400, 410, 395, 405, 420, 400) against forecasts (350, 460, 350, 453, 368, 449); errors alternate +50 and −50. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The errors cancel, so the tracking signal says "perfect" while every week is wrong by about 12%. It only measures bias, not accuracy. |
| Why other metrics are NOT suitable here | MPE: also cancels to near zero; plain tracking signal: same flaw; R-squared: weak guide on a flat series. |
| Better alternative (if BAD fit) | MASE or WAPE for accuracy, with the tracking signal kept only as the bias add-on. |
| Business impact of choosing wrong | Plants alternately over-buy shrimp and run short, and the "bias" dashboard stays green throughout. |
| Small numeric example | Errors: +50, −50, +45, −48, +52, −49; cumulative 50, 0, 45, −3, 49, 0; signal 1.00, 0.00, 0.93, −0.06, 1.00, 0.00 (never near 4). MAE = 49 tonnes; WAPE = 294/2,430 = 12.1%; a naive "same as last week" error is 14 tonnes, so MASE ≈ 3.5. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — A three-week-old subscription bundle |
| Industry / Domain | Fintech (super-app subscriptions, Thailand) |
| Business Problem | A super-app launches a new subscription bundle and applies a ±4 tracking-signal alert after only three weeks of data. |
| ML Translation | Target: weekly sign-ups; 3 weeks of actuals (100, 110, 120) against forecasts (60, 66, 72); every error is positive. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | The signal can never be larger than the number of weeks; with 3 weeks it caps at 3, so the ±4 limit cannot fire even though the forecast is 40% too low every week. |
| Why other metrics are NOT suitable here | MAD alone: too noisy on 3 points; MAPE: shows the miss but has no alert rule; R-squared: undefined in practice with 3 points. |
| Better alternative (if BAD fit) | Percentage bias (MPE or total bias) with a simple alert (for example more than 15% off for two weeks), and a naive baseline comparison until history builds up. |
| Business impact of choosing wrong | A badly under-forecast launch is not flagged, so the team under-staffs onboarding while sign-ups surge. |
| Small numeric example | Errors: +40, +44, +48; cumulative 40, 84, 132; MAD 40, 42, 44; signal 1, 2, 3 (never above 3). MPE = (40/100 + 44/110 + 48/120)/3 = 40%. |

**6. Quick decision rule:** Use the tracking signal to monitor many forecasts for a creeping one-sided bias, paired with an accuracy metric; avoid it as the only quality check, on very short or mostly-zero series, or without resetting after a fix.

### Multi-output Regression Averaging

**1. What it measures (plain English):** When one model predicts several targets at once, you must decide how to combine the per-target scores into one number. The options (scikit-learn's multioutput setting) are raw_values (no averaging, one score per target), uniform_average (a simple mean), variance_weighted (R-squared only; targets with larger spread count more) and custom weights. Aliases: macro versus weighted averaging across targets.

`Combined score = Σ wⱼ × scoreⱼ;  uniform wⱼ = 1/m;  variance-weighted wⱼ = Var(yⱼ) / Σ Var(y)`

**2. Intuition:** A school report card. Always read each subject's mark first. A simple average treats all subjects equally; weighting by "marks out of" lets the longest exam decide the grade.

**3. Benefits:**

- raw_values shows every target, so no weak one is hidden.
- uniform_average on scale-free scores (such as R-squared) gives each target an equal vote.
- Custom weights let you encode which target matters most to the business.
- Normalising each target first lets scale-dependent errors be compared and averaged.

**4. Limitations / Potential issues:**

- Never average MSE, RMSE or MAE across targets measured in different units: the biggest-unit target dominates.
- variance_weighted R-squared is dominated by the highest-variance target and can hide a failing one.
- One averaged number can hide a target with a negative R-squared (worse than guessing the mean).
- Custom weights are a judgement call and must be agreed with the business.
- Targets that are coordinates of one object, or that must add up, need extra metrics.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Battery cells: capacity looks fine, resistance fails |
| Industry / Domain | Manufacturing (EV battery cells, South Korea) |
| Business Problem | A cell maker predicts two quality properties per cell from process data: capacity (Ah) and internal resistance (milliohm). |
| ML Translation | Aggregation chosen: raw_values (per-target R-squared) first. Targets: capacity [48.2, 49.1, 50.3, 47.5, 49.9, 48.8] and resistance [1.10, 0.95, 1.30, 1.20, 1.05, 1.15]; predictions capacity [48.0, 49.3, 50.1, 47.8, 49.6, 49.0], resistance [1.12, 1.18, 1.02, 1.05, 1.20, 0.98]. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Printing each target first exposes that resistance is predicted worse than a plain average would do, which any single average would hide. |
| Why other metrics are NOT suitable here | variance_weighted R-squared: dominated by capacity (variance 0.906 against 0.012) and reports 0.90; uniform_average: hides which target is bad in one −0.43; averaged MSE: mixes Ah squared with milliohm squared. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A single "0.90" would let a model with useless resistance prediction ship, passing bad cells to car makers. |
| Small numeric example | R-squared per target: capacity 0.937; resistance −1.788. Variance-weighted = (0.937×0.9056 + (−1.788)×0.0123)/(0.9056+0.0123) = 0.901. Uniform = (0.937 − 1.788)/2 = −0.425. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Port performance: three equally important gauges |
| Industry / Domain | Logistics (container port, Singapore) |
| Business Problem | A port model predicts for each vessel call the crane moves per hour, dwell hours and yard utilisation percentage; the port treats the three as equally important. |
| ML Translation | Aggregation chosen: raw_values first, then uniform_average of R-squared. Actual moves [28, 31, 26, 33, 30], dwell [36, 30, 44, 27, 33], yard % [71, 78, 66, 83, 75]; predicted moves [29, 30, 27, 31, 30], dwell [35, 33, 40, 30, 31], yard % [72, 74, 69, 80, 76]. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | R-squared is unit-free, so averaging it with equal votes is fair; the raw values confirm no target is failing. |
| Why other metrics are NOT suitable here | Averaged MSE: mixes squared moves, squared hours and squared percentage points (1.4, 7.8, 7.2 average 5.47, a meaningless number); variance_weighted: lets the high-variance targets outvote crane moves; MAE per target: informative but cannot be summarised. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A scale-dominated score could hide that crane-move forecasts are weaker, upsetting berth plans. |
| Small numeric example | R-squared per target: 0.760, 0.771, 0.787; uniform_average = (0.760+0.771+0.787)/3 = 0.773; variance_weighted = 0.777. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Fare and pickup wait weighted by business priority |
| Industry / Domain | Transport (ride-hailing, Indonesia) |
| Business Problem | A ride-hailing app predicts the fare (thousand rupiah) and the rider's pickup wait (minutes). Management says fare accuracy is worth about 70% of the value and wait about 30%. |
| ML Translation | Aggregation chosen: raw_values first, then custom weights (0.7 and 0.3) on R-squared. Six trips; fare actual [45, 62, 38, 80, 55, 70], predicted [47, 60, 39, 78, 57, 69]; wait actual [4.0, 6.5, 3.0, 8.0, 5.0, 7.0], predicted [5.5, 4.5, 4.0, 6.0, 6.0, 5.5]. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Custom weights express the agreed business priority openly, and per-target R-squared is unit-free. |
| Why other metrics are NOT suitable here | variance_weighted: erases the wait target (variance 3.0 against 203.6) and reports 0.97; uniform_average: gives wait a 50% vote the business did not agree to; averaged MSE: mixes squared rupiah and squared minutes. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Equal or variance-driven weights would steer model selection away from what the business values. |
| Small numeric example | R-squared per target: fare 0.985, wait 0.204. Custom = 0.7×0.985 + 0.3×0.204 = 0.751. Uniform = 0.594. Variance-weighted = 0.974. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Averaging yen errors with star-rating errors |
| Industry / Domain | E-commerce (online marketplace, Japan) |
| Business Problem | A marketplace predicts each product's price (yen) and its average star rating, and reports one averaged MSE across both outputs. |
| ML Translation | Aggregation chosen: uniform_average of MSE (the wrong choice). Four products; price actual [12000, 8500, 15000, 9800], predicted [12400, 8200, 14500, 10300]; rating actual [4.2, 3.8, 4.6, 3.1], predicted [3.4, 4.5, 3.7, 4.0]. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MSE is in squared units: yen squared swamps stars squared, so the average is really just the price error. |
| Why other metrics are NOT suitable here | variance_weighted R-squared: also dominated by price; plain RMSE average: same unit clash; MAE average: mixes yen and stars. |
| Better alternative (if BAD fit) | raw_values first, then an average of normalised error (RMSE divided by each target's standard deviation) or a uniform average of R-squared. |
| Business impact of choosing wrong | The team cannot see that the rating model is poor, so a bad rating predictor reaches the product pages. |
| Small numeric example | MSE per target: price 187,500; rating 0.6875; average 93,750.34. A perfect rating model would make it 93,750.00, a change of 0.34, invisible. Normalised RMSE: price 0.176; rating 1.497 (worse than guessing the average), mean 0.836. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Claim cost drowns out processing time |
| Industry / Domain | Insurance (motor claims, Thailand) |
| Business Problem | A Thai motor insurer predicts claim cost (baht) and days to process the claim, and reports variance-weighted R-squared as the headline. |
| ML Translation | Aggregation chosen: variance_weighted R-squared (the wrong choice). Five claims; cost actual [40000, 250000, 12000, 90000, 600000], predicted [45000, 240000, 15000, 80000, 590000]; days actual [5, 9, 6, 4, 8], predicted [7, 6, 7, 7, 5]. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Claim cost has a spread billions of times larger than processing days, so the weighted score equals the cost R-squared and the days target is erased. |
| Why other metrics are NOT suitable here | Averaged MSE: mixes baht squared and days squared; averaged MAE: the same unit clash; uniform_average on RMSE: unit mixing again. |
| Better alternative (if BAD fit) | raw_values, then uniform_average (or custom weights) of R-squared, so the days target has a voice. |
| Business impact of choosing wrong | Customer-service staffing is planned from a processing-time model that is worse than a guess. |
| Small numeric example | Variance: cost 4.71×10^10, days 3.44. R-squared: cost 0.9986, days −0.860. Variance-weighted = 0.9986; uniform_average = (0.9986 − 0.860)/2 = 0.069. |

**6. Quick decision rule:** Always print per-target scores first, then average only scale-free scores (R-squared or normalised errors) with the weighting you can justify; avoid averaging raw MSE, RMSE or MAE across targets in different units, and avoid variance weighting when a small-variance target matters.

### Tweedie / Poisson / Gamma Deviance [Added – not in source file]

**1. What it measures (plain English):** Deviance scores a forecast by how "surprising" the actual values are under a chosen shape of randomness, instead of by plain distance. It suits targets that are counts (0, 1, 2, ...) or positive and right-skewed (claim amounts, spending). Errors are judged relative to the size of the prediction: missing by 3 when you expected 1 is much worse than missing by 3 when you expected 100. Here y is the actual value and μ ("mu") the predicted mean. Aliases: Poisson deviance, Gamma deviance, Tweedie deviance, mean deviance.

Poisson deviance (for counts): `D = 2 × mean[y·ln(y/μ) − (y − μ)]`, where the first term is 0 when y = 0.

Gamma deviance (for strictly positive amounts): `D = 2 × mean[(y − μ)/μ − ln(y/μ)]`

Tweedie deviance with power p (p not 0, 1 or 2): `D = 2 × mean[y^(2−p)/((1−p)(2−p)) − y·μ^(1−p)/(1−p) + μ^(2−p)/(2−p)]`

The power p is a dial for the kind of randomness: p = 0 is ordinary squared error; p = 1 is Poisson (counts); a value between 1 and 2 (for example 1.5) fits data with many exact zeros plus right-skewed positive amounts, such as insurance claims or spending per customer; p = 2 is Gamma (positive amounts where the spread grows with the level, so the same percentage miss costs the same); p = 3 is for even more skewed data. The higher p is, the more the score cares about percentage error and the less about the biggest rows.

**2. Intuition:** Judging runners by percentage time difference. Being 3 seconds slower in a 100 m sprint is a disaster, while 3 seconds in a marathon is nothing. Deviance judges an error by what is typical for that row.

**3. Benefits:**

- Matches the real shape of counts and skewed amounts, so models trained on it are usually better calibrated (their averages are closer to the truth) than squared-error models.
- Treats the same percentage miss equally for small and large rows, so a few huge rows do not dominate.
- Handles exact zeros (Poisson and Tweedie with p between 1 and 2).
- Built into scikit-learn, XGBoost, LightGBM and generalised linear models.

**4. Limitations / Potential issues:**

- Needs the right target type: Poisson needs y of 0 or more; Gamma needs y strictly above 0; a negative y breaks it.
- The score is not in business units and is hard to explain; use MAE or WAPE for reporting.
- The power p must be chosen (often by cross-validation), and predictions must be positive.
- It assumes the spread grows with the level; real counts are often more spread out than Poisson allows (overdispersion).

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Orders per hour at a quick-commerce dark store |
| Industry / Domain | E-commerce (quick commerce, Indonesia) |
| Business Problem | A dark store in Jakarta forecasts how many orders of one item arrive in each hour to plan picker shifts; most hours have 0 to 4 orders. |
| ML Translation | Target: order count per hour; count regression with Poisson deviance; 5 hours with actual counts (0, 2, 1, 4, 9) and predicted means (1, 2, 2, 3, 6). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The target is a small count, so Poisson deviance cares about error relative to the expected count. |
| Why other metrics are NOT suitable here | MSE: treats an error of 3 at a mean of 1 the same as at a mean of 100; MAPE: undefined when the actual count is 0; RMSE: same problem as MSE and driven by the 9-order hour. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A squared-error model under-reacts to quiet-hour mistakes and over-reacts to busy hours, giving too many or too few pickers. |
| Small numeric example | Per-hour Poisson deviance: 2.00, 0.00, 0.61, 0.30, 1.30; mean 0.84; MSE = 2.4. Same miss of 3: actual 4 against 1 expected gives 5.09; actual 103 against 100 gives 0.09; MSE scores both 9. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Medical claim sizes, where a 20% miss is a 20% miss |
| Industry / Domain | Insurance (medical expense cover, Japan) |
| Business Problem | An insurer predicts the size of each medical claim to price cover. Claims are positive and heavily right-skewed. |
| ML Translation | Target: claim amount in thousand yen; positive skewed regression with Gamma deviance; 5 claims, actual (60, 150, 80, 400, 1,200), predicted (70, 130, 85, 360, 1,000). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Gamma deviance is based on relative error, so the percentage miss counts the same on a small claim and a large one. |
| Why other metrics are NOT suitable here | MSE: dominated by the single 1,200 claim (95% of the total); MAE: also dominated by big claims and not scale-free; RMSLE: treats ratios symmetrically but is not matched to the cost of claims in yen. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A squared-error model is tuned to a few huge claims, so premiums for ordinary policies are mispriced. |
| Small numeric example | Gamma deviance per claim: 0.0226, 0.0215, 0.0036, 0.0115, 0.0354; mean 0.0189 (the 1,200 claim is 37% of the total). MSE = (100+400+25+1,600+40,000)/5 = 8,425 (the 1,200 claim is 95%). Scale check: 100 vs 80 and 1,000 vs 800 both give 0.0537; MSE gives 400 and 40,000. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Monthly spend per user, mostly zeros |
| Industry / Domain | Fintech and marketing (super-app, Indonesia) |
| Business Problem | A super-app predicts each user's in-app spend next month; most users spend nothing and a few spend a lot. |
| ML Translation | Target: monthly spend in thousand rupiah, exactly 0 for many users, positive skewed otherwise; Tweedie deviance with p = 1.5; 5 users, actual (0, 0, 0, 35, 120), predicted (5, 8, 10, 40, 90). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | p = 1.5 handles exact zeros and the skewed positive part together, and it penalises predicting spend for users who spend nothing. |
| Why other metrics are NOT suitable here | Gamma deviance (p = 2): impossible because y = 0; MSE: 81% of the loss comes from the single 120 user; MAPE: undefined for zero spend. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Marketing offers go to users who will not spend, wasting incentive budget. |
| Small numeric example | Tweedie p = 1.5 deviance per user: 8.94, 11.31, 12.65, 0.11, 0.91; mean 6.78. MSE = (25+64+100+25+900)/5 = 222.8 (the 120 user is 81%). Poisson (p = 1) mean = 11.14; Gamma (p = 2) cannot be computed. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Voyage profit that can be negative |
| Industry / Domain | Logistics (container shipping, Singapore) |
| Business Problem | A shipping line predicts profit per voyage in USD million, and chooses Gamma deviance because profits look skewed. |
| ML Translation | Target: profit in USD million, which can be negative; regression; 3 voyages, actual (2.4, −0.8, 1.5), predicted (2.0, 0.5, 1.8). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Gamma deviance uses ln(y/μ), which does not exist for a negative y; the library refuses to compute it. |
| Why other metrics are NOT suitable here | Poisson deviance: also needs y of 0 or more; MAPE: unstable around small profits; RMSLE: needs non-negative values. |
| Better alternative (if BAD fit) | MAE and RMSE in USD million, or Huber loss for training. |
| Business impact of choosing wrong | Loss-making voyages are silently dropped or crash the pipeline, hiding the voyages that matter most. |
| Small numeric example | y = −0.8 gives ln(−0.8/0.5), undefined. Alternative: absolute errors 0.4, 1.3, 0.3; MAE = 2.0/3 = 0.667; RMSE = sqrt((0.16+1.69+0.09)/3) = 0.804 USD million. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Telling call-centre managers about deviance |
| Industry / Domain | Telecom (customer service, Thailand) |
| Business Problem | A telecom call centre compares two models of calls per half-hour and wants to show floor managers one accuracy number. |
| ML Translation | Target: calls per half-hour; count regression; actual (120, 95, 140, 180, 110); Model A (110, 100, 150, 160, 115); Model B (125, 90, 135, 185, 100); Poisson deviance proposed as the reported figure. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Deviance ranks the models correctly, but "0.35" means nothing to a manager; it suits training, not reporting. |
| Why other metrics are NOT suitable here | RMSE: sensitive to single bad half-hours; MAPE: acceptable but inflates quiet periods; deviance itself: not in calls or percentages. |
| Better alternative (if BAD fit) | MAE (calls) and WAPE (percentage of total calls) for reporting, with deviance kept for training. |
| Business impact of choosing wrong | Managers cannot judge whether a model is good enough to staff by, so they ignore it. |
| Small numeric example | Poisson deviance: A 0.888, B 0.353. MAE: A 10.0 calls, B 6.0 calls. WAPE: A = 50/645 = 7.75%, B = 30/645 = 4.65%. |

**6. Quick decision rule:** Use Poisson deviance for counts, Gamma deviance for strictly positive skewed amounts and Tweedie (p between 1 and 2) for amounts with many zeros, mainly as the training objective; avoid it when the target can be negative, or when you need an error figure that managers read in real units.

### Mean Directional Accuracy (MDA) [Added – not in source file]

**1. What it measures (plain English):** MDA is the share of periods in which the forecast gets the direction of change right: up or down compared with the last actual value. It ignores how big the move is. Aliases: directional accuracy, hit rate, direction hit ratio.

`MDA = (1/(n−1)) × Σ 1[sign(yₜ − yₜ₋₁) = sign(ŷₜ − yₜ₋₁)]`

Here 1[...] is 1 when the two directions match and 0 when they do not; 50% is no better than a coin toss.

**2. Intuition:** A weather forecaster asked only "will tomorrow be warmer than today?" She is scored on yes or no, not on the number of degrees.

**3. Benefits:**

- Matches decisions that depend on direction: buy or sell, raise or cut, wait or act.
- Simple to explain and not affected by the scale or units of the target.
- Not distorted by a few huge errors.

**4. Limitations / Potential issues:**

- Ignores the size of the move: many tiny correct calls can outweigh one large missed move.
- Flat periods (no change) are ambiguous: sign 0 can be counted as wrong or skipped, and the score changes.
- A model that always predicts "up" scores well in a rising market; compare with the share of up moves.
- Says nothing about accuracy of the level, so pair it with MAE or a profit measure.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Convert the dollars now or wait a day |
| Industry / Domain | Manufacturing (export treasury, South Korea) |
| Business Problem | An exporter receives dollars and decides each day whether to convert to won now or wait, based on whether the won is expected to weaken (dollar rising) or strengthen tomorrow. |
| ML Translation | Target: USD/KRW rate; one-step forecast; actuals (1300, 1306, 1302, 1310, 1308, 1315), forecasts for days 2 to 6 (1305, 1307, 1303, 1309, 1312). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The decision is binary (wait or convert), so the question that matters is whether the forecast points the right way. |
| Why other metrics are NOT suitable here | MAE: a small average miss says nothing about whether you waited correctly; RMSE: the same; MAPE: tiny percentages that hide the decision quality. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Converting just before a favourable move costs money on every large receipt. |
| Small numeric example | Actual directions (days 2 to 6): up, down, up, down, up. Forecast directions against the previous actual: up, up, up, down, up. Matches 4 of 5, so MDA = 80%. MAE = (1+5+7+1+3)/5 = 3.4 won. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — The palm-oil model with the lower error that loses money |
| Industry / Domain | Agriculture (palm-oil trading, Indonesia) |
| Business Problem | A palm-oil trader goes long or short each week on the benchmark futures price (MYR per tonne), choosing between two forecast models. |
| ML Translation | Target: weekly futures price; actuals (3900, 3940, 3920, 3980, 4010, 3990, 4050); Model A forecasts (3898, 3938, 3918, 3982, 4012, 3988), Model B (3990, 3880, 4090, 4100, 3920, 4150) for weeks 2 to 7. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The trade follows the forecast's direction, so MDA tracks what pays; MAE picks the wrong model. |
| Why other metrics are NOT suitable here | MAE and RMSE: Model A has the lower error but is wrong about the direction in 4 of 6 weeks; MAPE: the same flaw; R-squared: dominated by the level of a trending price. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Trading on the lower-error model loses money every week it is wrong about direction. |
| Small numeric example | Model A: MAE 39.0, direction right 2 of 6 (33%); trading 1 tonne long or short each week gains −40+20−60+30−20−60 = −130 MYR. Model B: MAE 76.7, direction right 6 of 6 (100%); gain +40+20+60+30+20+60 = +230 MYR. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Raise or cut the ad rate card |
| Industry / Domain | Marketing (short-video advertising, China) |
| Business Problem | A short-video platform's ad sales team decides each week whether to raise or cut its rate card, based on whether bookings are forecast to rise or fall. |
| ML Translation | Target: weekly ad bookings in million yuan; actuals (820, 860, 845, 900, 930, 910); forecasts for weeks 2 to 6 (855, 840, 890, 940, 935). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The action (raise or cut) depends only on the direction of the booking trend. |
| Why other metrics are NOT suitable here | MAE: a small error does not show whether the right action was chosen; RMSE: the same; MAPE: all percentages are small. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Cutting rates in a rising week gives away revenue; raising them in a falling week loses advertisers. |
| Small numeric example | Actual directions: up, down, up, up, down. Forecast directions: up, down, up, up, up (935 against 930). Matches 4 of 5, so MDA = 80%. MAE = (5+5+10+10+25)/5 = 11 million yuan. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Four small calls right, one big call wrong |
| Industry / Domain | Banking (bond desk, Japan) |
| Business Problem | A regional bank's treasury trades on a forecast of daily changes in government bond yields, and reports MDA as the model's quality. |
| ML Translation | Target: daily yield change in basis points; actual changes (+1, −1, +2, −1, −25); predicted directions (up, down, up, down, up). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | MDA counts every day equally, so four small correct calls hide one wrong call on a day with a 25 basis point move. |
| Why other metrics are NOT suitable here | MAE: shows the size of the miss but not the profit effect; hit rate (MDA): the flaw itself; MAPE: unstable around tiny changes. |
| Better alternative (if BAD fit) | A magnitude-weighted directional score or the trading profit and loss, reported next to MAE. |
| Business impact of choosing wrong | The desk keeps a model that is right 80% of the time and loses on the one day that matters. |
| Small numeric example | MDA = 4/5 = 80%. Profit from following the direction: +1 +1 +2 +1 −25 = −20 basis points. Magnitude-weighted accuracy = (1+1+2+1)/(1+1+2+1+25) = 5/30 = 16.7%. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Administered fuel prices that rarely move |
| Industry / Domain | Energy (retail fuel pricing, Vietnam) |
| Business Problem | A fuel retailer forecasts a regulated pump-price index that is adjusted only on some weeks; on the others it stays unchanged. |
| ML Translation | Target: price index; actuals (100, 100, 102, 102, 100, 100, 103); forecasts for weeks 2 to 7 (100.1, 101.5, 101.9, 100.5, 100.1, 102.5); actual changes (0, +2, 0, −2, 0, +3). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | In unchanged weeks the actual direction is "flat", which a forecast of +0.1 can never match, so the score punishes a near-perfect forecast. |
| Why other metrics are NOT suitable here | Strict MDA: 50%, because flat weeks count as wrong; MDA that skips flat weeks: 100%, which hides the missed flat calls; MAPE: fine, but says nothing about direction. |
| Better alternative (if BAD fit) | MAE for size, plus a three-way up, flat or down accuracy with a small dead zone (changes under 0.5 count as flat). |
| Business impact of choosing wrong | The team throws away a model that is almost exactly right, or trusts it for the wrong reason. |
| Small numeric example | Actual signs: flat, up, flat, down, flat, up; forecast signs: up, up, down, down, up, up; 3 of 6 match, MDA = 50%. Skipping flat weeks: 3 of 3 = 100%. With a dead zone of 0.5: forecast signs flat, up, flat, down, flat, up; 6 of 6 = 100%. MAE = (0.1+0.5+0.1+0.5+0.1+0.5)/6 = 0.30. |

**6. Quick decision rule:** Use MDA when the decision depends only on whether the series goes up or down (buy or sell, raise or cut, wait or act); avoid it when the size of the move drives the money, when many periods are flat, or as the only metric without a magnitude check.
