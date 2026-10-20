# Regression Case Studies, Part 5: Probabilistic Forecast and Model-Selection Metrics

## Table of Contents

- [Scoring the whole probability forecast](#scoring-the-whole-probability-forecast)
  - [Gaussian Negative Log-Likelihood (NLL)](#gaussian-negative-log-likelihood-nll)
  - [Continuous Ranked Probability Score (CRPS)](#continuous-ranked-probability-score-crps)
- [Checking intervals and calibration](#checking-intervals-and-calibration)
  - [PICP and MPIW](#picp-and-mpiw)
  - [Interval Score and Winkler Score](#interval-score-and-winkler-score)
  - [PIT Histogram](#pit-histogram)
- [Choosing between models](#choosing-between-models)
  - [AIC](#aic)
  - [AICc](#aicc)
  - [BIC (SIC / SBC)](#bic-sic--sbc)
  - [Mallows' Cp](#mallows-cp)
  - [PRESS and Cross-Validated Error](#press-and-cross-validated-error)

**How to read this part:** each metric below has a short explanation, benefits, limitations and five case studies, some where the metric is a good fit and some where it is not. The first two groups score forecasts that carry uncertainty (whole distributions, ranges and calibration). The third group chooses between models. Every number in the toy examples was recomputed with Python.

## Scoring the whole probability forecast

### Gaussian Negative Log-Likelihood (NLL)

**1. What it measures (plain English):** The negative log of the probability density (how much likelihood) the model assigns to what really happened, averaged over cases, when the forecast is a bell curve with a predicted mean and spread. Lower is better. It punishes confident misses very hard and also punishes needless uncertainty. Also called Gaussian log loss; the likelihood is how plausible the actual data is under the forecast.

`NLL = (1/n) × Σ [ 0.5 × ln(2π σᵢ²) + (yᵢ − μᵢ)² / (2σᵢ²) ]`

**2. Intuition:** Think of a weather presenter who must give a best guess and a margin of error. If she says 'exactly 30 degrees' and it is 36, she looks foolish; if she says 'between 0 and 60 degrees' she is safe but useless. NLL scores her on both honesty and sharpness together.

**3. Benefits:**

- A proper scoring rule (a score that can only be minimised by stating your true belief, so it cannot be gamed).
- Scores accuracy and uncertainty in one number, and handles spread that changes from case to case (heteroscedastic noise).
- Smooth, so it is the standard training loss for models that predict a mean and a spread (neural nets, NGBoost, Gaussian processes).
- With a constant spread it reduces to MSE, so it extends the familiar case instead of replacing it.
- Works with other families (Student-t, Gamma, Poisson) when the Gaussian is wrong, and doubles as an anomaly score.

**4. Limitations / Potential issues:**

- Assumes a Gaussian shape; skewed, bounded or multi-peaked targets give badly wrong tails.
- Unbounded and dominated by outliers (rare extreme cases): one confident miss can swamp the average.
- Numerically fragile: a spread near zero sends the loss towards minus infinity, so the spread must be clamped or predicted on the log scale.
- Hard to interpret: it depends on the target's units, can be negative, and is not comparable across datasets. Always compare with a baseline such as a constant Gaussian.
- Needs a model that outputs uncertainty, and a single network captures only noise in the data, not its own ignorance far from the training data.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Sizing cash float for mobile-money agents of very different sizes |
| Industry / Domain | banking (mobile money, East Africa) |
| Business Problem | A mobile-money operator must decide how much cash to place with each village agent tomorrow. Small kiosks have steady cash-outs; large trading-centre agents swing widely. Too little cash strands customers; too much locks up money. |
| ML Translation | Target = next-day cash-out in KES thousand per agent; probabilistic regression; the model outputs a mean and a standard deviation (spread) per agent; trained with Gaussian NLL; heteroscedastic (the noise level differs by agent); a few hundred thousand agent-days. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | NLL scores the whole forecast (mean and spread) and rewards a small spread only when the forecast is accurate. It is smooth, so the network can be trained on it directly, and it teaches the model that big agents are noisier than small ones. |
| Why other metrics are NOT suitable here | MAE or RMSE only check the mean and ignore the spread, so they cannot tell if the model knows which agents are risky. PICP (share of actuals inside the range) cannot be trained by gradient descent. CRPS is a fine reporting score but NLL is the standard training objective for a mean-and-spread model. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | If agents are scored with a single flat spread, big agents run out of cash (angry customers, lost fees) while small agents hold idle cash that earns nothing. |
| Small numeric example | 3 agents, actual cash-out y = 48, 210, 95; predicted mean = 50, 190, 100; per-agent spread = 5, 25, 10. NLL for each = 0.5×ln(2π×σ²) + (y−μ)²/(2σ²) = 2.608, 4.458, 3.347; mean = 3.471. A flat spread of 15 for everyone gives mean NLL = 3.945. The agent-specific spreads win by 0.474 nats (units of log-likelihood). |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Tuning a kriging model of gold grade for a pit design |
| Industry / Domain | mining (Australia) |
| Business Problem | A mine planner estimates ore grade between drill holes. The pit design depends on how sure the estimate is, not just the estimate. Two settings of the geostatistical (kriging, a Gaussian-process) model give the same grade estimates but different uncertainty. |
| ML Translation | Target = gold grade in grams per tonne for each block; probabilistic regression with Gaussian predictive distribution; the likelihood of held-out drill samples is the tuning score; small, spatially clustered data. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Gaussian-process hyperparameters are normally chosen by likelihood, and NLL on held-out blocks is the same idea. It separates two settings that have identical point accuracy but different honesty about uncertainty. |
| Why other metrics are NOT suitable here | RMSE is identical for the two settings, so it cannot choose between them. MAE has the same blind spot. R-squared also only sees the mean. Coverage (PICP) needs far more samples than 4 blocks to be stable. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Picking the over-confident setting makes the planner believe the grade is known to ±0.1 g/t, so the pit wall is cut too tight and waste rock is mined as ore or ore is left behind, costing millions per bench. |
| Small numeric example | 4 blocks, actual y = 2.1, 0.8, 3.4, 1.2 g/t; both settings predict 2.0, 1.0, 3.0, 1.1 (RMSE 0.235 for both). Setting A spreads = 0.2, 0.3, 0.5, 0.2 gives NLL = -0.565, -0.063, 0.546, -0.565; mean -0.162. Setting B spread 0.1 everywhere gives -0.884, 0.616, 6.616, -0.884; mean 1.366. A wins; NLL can be negative and that is normal. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Flagging faulty district water meters by surprise score |
| Industry / Domain | utilities (water, Middle East) |
| Business Problem | A desalinated-water utility reads thousands of district meters each night. A broken or bypassed meter shows an odd reading, but each meter has its own normal day-to-day swing. The team wants a ranked list of suspicious readings. |
| ML Translation | Target = nightly flow reading in cubic metres per meter; the model predicts mean and spread per meter; the per-reading NLL is used as a surprise (anomaly) score; unlabelled data. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A reading that is far from the mean in units of that meter's own spread gets a very high NLL, while a noisy meter is allowed a bigger swing. The same score that trained the model doubles as the alarm, and it ranks severity. |
| Why other metrics are NOT suitable here | Absolute error would flag a naturally noisy meter just as hard as a stable one. PICP only says inside or outside the range, so a small miss and a huge miss look the same. RMSE averages everything into one number and cannot point at a single reading. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A flat error threshold sends crews to noisy but healthy meters and misses a real bypass on a stable one, so water is lost unbilled for weeks. |
| Small numeric example | 4 readings, actual y = 41, 39, 44, 18; predicted mean = 40, 40, 42, 40; spread = 3, 3, 4, 3. z-scores = 0.33, -0.33, 0.50, -7.33. NLL per reading = 2.07, 2.07, 2.43, 28.91. The fourth reading scores 28.9, about 13 times the normal level, so it tops the inspection list. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Gaussian spread for flood claim sizes with one giant claim |
| Industry / Domain | insurance (property, New Zealand) |
| Business Problem | An insurer wants a probability forecast of the size of each flood claim to set reinsurance cover. Most claims are small, but a few are huge. |
| ML Translation | Target = claim size in NZD thousand; positive and strongly right-skewed (long tail to the upper side); heavy-tailed; a Gaussian mean-and-spread model is proposed and scored by Gaussian NLL. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | A Gaussian puts probability on negative claims and has thin tails. A single huge claim then produces a gigantic NLL, because the penalty grows with the square of the miss measured in spreads, so one observation dominates the average. |
| Why other metrics are NOT suitable here | RMSE would also be driven by the 120 claim and says nothing about spread. MAPE breaks on tiny claims. PICP with Gaussian ranges would under-cover the tail without telling how bad. R-squared hides the shape problem entirely. |
| Better alternative (if BAD fit) | Use NLL with the right family (log-normal or Gamma, which fit positive skewed data) or CRPS computed from simulated samples. Both are proper scores that tolerate the tail better. |
| Business impact of choosing wrong | The Gaussian model understates the chance of a very large claim, so reinsurance is bought too thin and one bad flood season eats the capital reserve. |
| Small numeric example | 5 claims = 4, 6, 7, 9, 120. Gaussian fit: mean 29.2, spread 45.4; NLL = 5.235; it also gives 26.0% chance of a negative claim, which is impossible. A log-normal fit gives NLL = 4.033 (lower is better). A confident Gaussian (mean 6, spread 3) hit by the 120 claim scores NLL = 724.0 for that single claim. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Reporting loan-loss forecast quality to a bank board |
| Industry / Domain | banking (Gulf lender) |
| Business Problem | The risk committee of a Gulf lender asks one question: can we trust the forecast ranges for quarterly loan losses? The model team proposes to report average Gaussian NLL as the answer. |
| ML Translation | Target = quarterly loss per portfolio in SAR million; probabilistic regression (mean and spread); audience is non-technical; the metric is for communication, not training. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | NLL has awkward units, can be negative, and shifts whenever the unit of the target changes, so a board cannot say whether 4.0 is good. It also hides whether the ranges are too narrow or too wide. |
| Why other metrics are NOT suitable here | RMSE says nothing about the ranges. R-squared ignores uncertainty. NLL on its own needs a baseline model before it means anything. |
| Better alternative (if BAD fit) | Report PICP (share of actuals inside the 90% range) together with MPIW (average range width), plus CRPS in SAR million. Everyone understands '3 of 4 actuals fell inside, ranges 62 wide'. |
| Business impact of choosing wrong | The board either rejects a good model because the number looks strange, or approves a weak one because a lower-looking number seemed better, which affects provisioning. |
| Small numeric example | 4 portfolios, y = 120, 150, 90, 230; mean = 110, 160, 95, 170; spread = 15, 20, 10, 30. Mean NLL in SAR million = 4.389; the same forecasts in SAR thousand give 11.297. The gap of 6.908 equals ln(1000) = 6.908, so the number changed with the unit alone. Coverage metrics do not change: 90% ranges (mean ± 1.645×spread) contain 3 of 4 actuals, PICP = 0.75, MPIW = 61.7. |

**6. Quick decision rule:** Use Gaussian NLL when you train or compare models that output a mean and a spread and the errors are roughly bell-shaped; avoid it when the target is skewed or heavy-tailed, or when you must report quality to non-technical readers (use CRPS, PICP and MPIW instead).

### Continuous Ranked Probability Score (CRPS)

**1. What it measures (plain English):** The area between the forecast's cumulative probability curve and the step that jumps at the actual value. It scores a whole probability forecast (a spread of possible outcomes) in the units of the target, and for a single-number forecast it equals the absolute error. Also called the continuous ranked probability score; lower is better.

`CRPS(F, y) = ∫ (F(x) − 1(x ≥ y))² dx`

`CRPS for Normal(μ, σ) = σ × [ z × (2Φ(z) − 1) + 2φ(z) − 1/√π ], with z = (y − μ)/σ`

**2. Intuition:** Imagine marking a dartboard where the dart is the real outcome and your forecast is a cloud of possible landing spots. CRPS measures how far, on average, the cloud sits from the dart, and gives credit if the cloud is tight around where the dart lands.

**3. Benefits:**

- A proper score that rewards both accuracy and honest, sharp uncertainty.
- In the same units as the target, and equal to MAE for single-number forecasts, so probabilistic and point models can be compared directly.
- Bounded growth: a confident miss gives a large but finite penalty, so it is safer than NLL for monitoring.
- Works with any forecast shape, including simulated samples (ensembles) and quantile forecasts; has a skill-score form against a baseline.
- Well established in weather, energy and hydrology verification.

**4. Limitations / Potential issues:**

- Not built into scikit-learn; you need a small library or your own code.
- Scale-dependent: values from different targets cannot be compared, so use a skill score.
- Less sensitive to the extreme tails than NLL, so it can under-penalise tail failures; add threshold-weighted CRPS or quantile losses when the tail is the decision.
- The simple ensemble formula costs time that grows with the square of the ensemble size.
- Harder to explain to non-technical readers than a coverage percentage, and an average can hide a weak segment.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Does the heat-risk forecast beat the single-number forecast |
| Industry / Domain | agriculture (wheat, Australia) |
| Business Problem | A wheat grower decides on irrigation and harvest timing from next-week maximum temperatures. The weather service sells both a single-number forecast and a probabilistic one at a higher price. Is the dearer product worth it? |
| ML Translation | Target = daily maximum temperature in °C; probabilistic regression (mean and spread) versus a point forecast with the same mean; the comparison must be on one scale. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | CRPS is in the units of the target (°C) and equals the absolute error when the forecast is a single number. So a probabilistic CRPS below the point forecast's MAE proves the extra uncertainty information adds value. |
| Why other metrics are NOT suitable here | NLL cannot be compared with a point model at all (a point forecast has infinite NLL). PICP and MPIW need a range, which the point forecast lacks. RMSE and MAE ignore the spread of the probabilistic product. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Paying for a probabilistic product that does not beat the point forecast wastes subscription money; the reverse, dropping a better product, leaves frost or heat-stress surprises unplanned. |
| Small numeric example | 3 days, actual y = 31, 36, 28 °C; both products predict mean 32, 33, 30. Point forecast MAE = (1+3+2)/3 = 2.00 °C. Probabilistic product with spreads 1.5, 3, 2 has CRPS = 0.607, 1.807, 1.205; mean = 1.206 °C. Since 1.21 < 2.00, the spread information helps. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Scoring a simulation-based room-night forecast for a coastal resort |
| Industry / Domain | tourism (Red Sea resort, Middle East) |
| Business Problem | A resort group runs a simulation that produces 5 possible values for rooms sold tomorrow. Revenue managers want a score that works directly on these samples, without forcing a bell curve on them. |
| ML Translation | Target = rooms sold per night; the forecast is an ensemble (a set of simulated outcomes), not a formula; probabilistic regression scored per night and averaged. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The ensemble form of CRPS needs only the samples: it rewards samples that are close to the truth and, through a subtracted spread term, rewards a tight ensemble. No distribution has to be assumed. |
| Why other metrics are NOT suitable here | Gaussian NLL needs a mean and a spread and assumes a bell curve, which a simulation set may not follow. PICP and MPIW need an interval and ignore how far a miss is. MAE of the ensemble mean throws away the spread. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Scoring only the ensemble mean hides a simulator that is over-confident, so the resort overbooks or leaves rooms empty with false certainty. |
| Small numeric example | Night 1: actual 96, ensemble 80, 90, 95, 100, 110. Term 1 (mean distance to truth) = (16+6+1+4+14)/5 = 8.20; term 2 (half the mean pairwise gap) = 5.60; CRPS = 8.20 − 5.60 = 2.60. Night 2: actual 95, ensemble 70, 72, 75, 78, 80 is tight but wrong: 20.00 − 2.08 = 17.92. Mean CRPS = 10.26 rooms; night 2 shows the cost of confident error. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Proving skill of a solar mini-grid output forecast to a donor |
| Industry / Domain | energy (solar mini-grid, East Africa) |
| Business Problem | A village solar mini-grid in Tanzania uses a probabilistic forecast to decide when to run the diesel back-up. The donor funding the project asks for one number that shows the forecast is better than just quoting last year's typical range. |
| ML Translation | Target = daily solar output in kWh; probabilistic regression; baseline = the long-run (climatology) distribution of output; the score must be in kWh. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | CRPS is in kWh and can be turned into a skill score, 1 − CRPS model / CRPS baseline, where 1 is perfect and 0 means no better than the typical range. It is robust, so one cloudy outlier day cannot ruin it. |
| Why other metrics are NOT suitable here | NLL is unbounded, so the cloudy day dominates and the number is hard to explain to a donor. PICP and MPIW need two numbers and do not give a skill percentage. RMSE ignores the spread. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Without a skill score the grid may keep paying for a forecast service that is no better than a calendar average, or the donor may cut funding for a model that is in fact good. |
| Small numeric example | 4 days, actual y = 118, 95, 130, 60 kWh. Model (means 115, 100, 125, 70; spreads 8, 10, 9, 15) has mean CRPS = 3.72 kWh. Baseline (always mean 100, spread 25) has mean CRPS = 15.70 kWh. Skill = 1 − 3.72/15.70 = 0.763, so the model removes about 76% of the baseline error. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Tailings pond overflow risk where only the extreme tail matters |
| Industry / Domain | mining (copper, Latin America) |
| Business Problem | A copper mine in the Andes must keep its tailings pond below a safety level after a freak storm. The decision is made on the 99th percentile of the water level, not on the typical level. |
| ML Translation | Target = pond level in cm above the design mark; probabilistic regression; heavy right tail; the decision depends on one extreme quantile (the value the level should exceed only 1 time in 100). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | CRPS averages the whole distribution, and a badly wrong far tail contributes only a little because it compares cumulative probabilities. Two forecasts that differ enormously in tail safety get CRPS values that look similar. |
| Why other metrics are NOT suitable here | RMSE and MAE ignore the tail. PICP at 90% says nothing about the 99th percentile. Plain Gaussian NLL punishes the tail but assumes a bell curve and is unbounded. |
| Better alternative (if BAD fit) | Pinball loss (the quantile score) at the 0.99 level, or threshold-weighted CRPS, which puts weight on the high-water region. It scores exactly the quantile that triggers the pumping decision. |
| Business impact of choosing wrong | A tail-blind score can pick the forecast that under-states storm risk, so pumps are not started in time and the pond spills, with environmental fines and shut-down. |
| Small numeric example | Actual level 160. Forecast A: mean 100, spread 10 (99th percentile 123.3). Forecast B: mean 100, spread 30 (99th percentile 169.8). CRPS: A 54.4, B 43.6, a ratio of only 1.25. Pinball loss at 0.99: A 36.37, B 0.098, a ratio of about 371 times. The tail score exposes what CRPS blurs. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Vaccine stock set at the 95th percentile of weekly demand |
| Industry / Domain | healthcare (public vaccine distribution, Latin America) |
| Business Problem | A regional health ministry stocks each clinic cluster to the 95th percentile of forecast weekly demand, so that a stock-out happens in about 1 week in 20. Two forecasting models are on trial. |
| ML Translation | Target = weekly doses needed (hundreds); probabilistic regression; the only output used is the 95% quantile; the cost of shortage and waste is asymmetric. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | CRPS spreads its attention over all quantiles, including the middle of the distribution that the stocking rule never uses. It can prefer the model that is better overall but worse at the one quantile that sets stock. |
| Why other metrics are NOT suitable here | RMSE and MAE judge the middle, not the 95th percentile. PICP at 90% checks a different pair of quantiles. NLL also rewards the whole shape, not the stocking quantile. |
| Better alternative (if BAD fit) | Pinball loss at tau = 0.95 (the quantile loss), which is exactly the cost-weighted error of the 95th-percentile stock level. |
| Business impact of choosing wrong | Picking the model with the better overall CRPS leaves more clinics out of vaccine in the weeks that matter, with outbreaks and emergency air freight. |
| Small numeric example | 4 weeks, actual demand y = 100, 120, 95, 150. Model A CRPS = 10.42, Model B CRPS = 13.85, so CRPS prefers A. At the 95% stock level, A stocks 117, 134, 129, 140 and is short by 10.3 doses in total with 65 left over; B stocks 172, 119, 152, 167 and is short by 0.6 with 146 left over. Pinball loss at 0.95 = (0.95×shortage + 0.05×leftover)/4: A = 3.26, B = 1.96, so the right score prefers B. |

**6. Quick decision rule:** Use CRPS when you need one robust, in-units score for a full probability forecast, or to compare a probabilistic model with a point model; avoid it when the decision depends on one tail quantile (use pinball loss) or when you only need to show stakeholders hit rates (use PICP and MPIW).

## Checking intervals and calibration

### PICP and MPIW

**1. What it measures (plain English):** Two numbers for interval forecasts. PICP is the share of actual values that fall inside the predicted range (coverage), and it should match the promised level, for example 90%. MPIW is the average width of the ranges, so lower means sharper. Always report them as a pair.

`PICP = (1/n) × Σ 1(Lᵢ ≤ yᵢ ≤ Uᵢ)`

`MPIW = (1/n) × Σ (Uᵢ − Lᵢ)`

**2. Intuition:** Think of a bus timetable that says 'arrives between 8:00 and 8:20'. PICP asks how often the bus really arrives in that window; MPIW asks how long the window is. A window of 'any time today' is always right and useless, so you need both numbers.

**3. Benefits:**

- Instantly understandable by non-technical readers: 'our 90% range held 89% of the time and is 58 wide'.
- PICP has an exact target (the promised level), so it is easy to judge and to monitor week by week.
- No assumption about the shape of the forecast; works for quantile, bootstrap, Bayesian and conformal (calibrated by held-out residuals) intervals.
- Cheap, stable and ideal for production monitoring and for reliability curves at several levels (50%, 80%, 90%).
- Coverage by segment pinpoints where ranges fail.

**4. Limitations / Potential issues:**

- Neither is a proper score and each alone is gameable (infinite ranges give perfect PICP; zero-width ranges give perfect MPIW).
- PICP is average (marginal) coverage: a model can hit 90% overall while badly under-covering an important segment.
- PICP counts hits only and ignores how far outside the misses are; the Interval Score fixes this.
- Noisy on small test sets: the sampling error of a hit rate is about sqrt(p(1−p)/n), 3 points at n = 100 for 90%.
- MPIW depends on the units of the target; normalise it by the range or spread before comparing datasets. Neither says anything about the point forecast's accuracy.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Promising a 90% collections range to a microfinance treasury |
| Industry / Domain | banking (microfinance, Latin America) |
| Business Problem | A microfinance lender in Peru must tell its treasury each month how much cash will come in from loan repayments per branch, as a range it is 90% sure about. Treasury borrows short-term to cover any gap below the range. |
| ML Translation | Target = monthly repayments per branch in PEN thousand; probabilistic regression delivering a lower and upper bound; both coverage (PICP) and average width (MPIW) are tracked; one prediction per branch. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | PICP checks the promise ('90% of actuals inside') and MPIW shows what the promise costs in vagueness. Together they say whether the ranges are honest and whether they are narrow enough to be useful for borrowing decisions. |
| Why other metrics are NOT suitable here | RMSE and MAE judge only the middle forecast, not the range. NLL and CRPS are proper scores but treasury cannot read them. Interval Score mixes width and misses into one number, which hides which of the two to fix. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Ranges that are too narrow leave treasury short and forced into expensive emergency loans; ranges that are too wide make it borrow and hold idle cash all month. |
| Small numeric example | 8 branches; actuals = 410, 380, 455, 520, 390, 470, 600, 430; ranges lower = 380, 350, 400, 470, 350, 420, 500, 390, upper = 450, 420, 490, 560, 430, 510, 570, 470. Inside: 7 of 8 (branch 7 actual 600 is above 570). PICP = 7/8 = 0.875 versus the 0.90 target; widths = 70, 70, 90, 90, 80, 90, 70, 80; MPIW = 80 PEN thousand. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Choosing the sharper of two equally honest pumping-demand ranges |
| Industry / Domain | utilities (water, Jordan and Gulf region) |
| Business Problem | A water utility schedules night-time pumping from a 90% range of next-day demand. Two vendor models both claim to be well calibrated. Pumping to the top of a wider range wastes electricity. |
| ML Translation | Target = daily demand in megalitres; interval forecasts from two models; first check coverage (PICP) on held-out days, then compare width (MPIW) between models that pass; same test days for both. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Once both models cover about the promised share, the narrower one is the more useful. PICP confirms honesty and MPIW ranks sharpness, the textbook rule 'be as sharp as possible, subject to being calibrated'. |
| Why other metrics are NOT suitable here | RMSE of the central forecast cannot see the range. CRPS would work but the operations team wants plain megalitre widths. Interval Score is a fine single number but here the coverage check and the width are both easy to read and give the same decision. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Choosing the wider model makes the utility over-pump every night, wasting electricity and desalinated water; choosing a model with hidden under-coverage causes night shortages. |
| Small numeric example | 8 test days, actuals = 62, 58, 71, 66, 110, 59, 64, 75 ML. Model A ranges width 40: inside 7 of 8, PICP = 0.875, MPIW = 40. Model B ranges width 28: inside 7 of 8, PICP = 0.875, MPIW = 28. Both miss the 110 day; B is 30% narrower, so B wins. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Weekly coverage alarm on the berth waiting-time promise |
| Industry / Domain | logistics (container port, Latin America) |
| Business Problem | A container terminal promises shipping lines a 90% waiting-time window for each arriving vessel. Operations wants an early alarm if the promise stops being true, for example after a crane breakdown or a change in vessel mix. |
| ML Translation | Target = vessel waiting time in hours; interval forecast already in production; the weekly hit rate of the window (PICP) over about 40 vessels is monitored; drift detection rather than model training. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | PICP has an exact target (0.90), is trivial to compute each week and means something to a port manager. The binomial noise of a hit rate is known, so an alarm line can be set from it. |
| Why other metrics are NOT suitable here | NLL and CRPS react to change but have no natural alarm level. MAE of the central forecast can stay flat while the ranges quietly become too narrow. PIT histograms need hundreds of vessels, more than a week provides. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Without a coverage alarm the terminal keeps quoting windows it no longer meets, which triggers demurrage disputes and penalty payments to shipping lines. |
| Small numeric example | Weekly hits out of 40 vessels = 36, 35, 33, 30, so PICP = 0.900, 0.875, 0.825, 0.750. Noise at p = 0.9, n = 40: sqrt(0.9×0.1/40) = 0.0474. Week 4: (0.90 − 0.750)/0.0474 = 3.16 noise units below target, beyond a 3-unit alarm line, so investigate. Week 3 at 1.58 units below is only a watch. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Dairy export price ranges that hit 90% but miss the crash by a mile |
| Industry / Domain | agriculture (dairy trade, New Zealand) |
| Business Problem | A dairy cooperative publishes 90% ranges for the monthly export price index to its farmers. Last year the ranges held 9 months out of 10, but the one miss was a price spike that blew the cooperative's hedging budget. |
| ML Translation | Target = monthly price index; interval forecasts for 10 months; the metric used is PICP (with MPIW); the cost of a miss grows with how far the price lands outside the range. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | PICP only counts hits and misses, so missing by 1 point and missing by 47 points look identical. A model can score a perfect 0.90 while one catastrophic miss drives the loss. MPIW says nothing about misses. |
| Why other metrics are NOT suitable here | RMSE would show the spike but mixes it with the central forecast. MAE under-weights it. Coverage by month needs more data than 10 points. |
| Better alternative (if BAD fit) | Interval Score (Winkler score): width plus 20 times the distance outside the range for a 90% interval. It charges for the size of the miss and is a proper score, so it can be optimised. |
| Business impact of choosing wrong | The cooperative believes its ranges are reliable because the hit rate is 90%, under-hedges, and a price spike is paid out of farmer payouts. |
| Small numeric example | 10 months; both models have 6-wide ranges and 9 hits, so PICP = 0.90 and MPIW = 6.0 for both. Model 1 missed the 150 month by 150 − 103 = 47; Model 2 missed it by 150 − 149 = 1. Interval Score for Model 1 = (9×6 + 6 + 20×47)/10 = 100.0; Model 2 = (9×6 + 6 + 20×1)/10 = 8.0. PICP cannot tell them apart; the Interval Score says Model 2 is 12.5 times better. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Picking a courier-delivery window vendor by hit rate alone |
| Industry / Domain | e-commerce (last-mile delivery, Africa) |
| Business Problem | An online marketplace in Lagos buys a delivery-time range model from a vendor. The procurement team scores bids by PICP only: 'which range contains the delivery time most often?' |
| ML Translation | Target = delivery time in minutes; interval forecasts (90%); two vendors scored on 10 test deliveries; the metric used is PICP alone, with no width check. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | PICP alone is trivially gamed: a range of '10 to 250 minutes' contains almost everything and tells the customer nothing. Hit rate rewards vague ranges. |
| Why other metrics are NOT suitable here | RMSE of the central time ignores the range. NLL needs a mean and spread the vendor may not supply. Plain MPIW alone would reward zero-width ranges. |
| Better alternative (if BAD fit) | Interval Score (width plus a heavy charge for distance outside), or PICP together with MPIW. Both make the vendor pay for vagueness. |
| Business impact of choosing wrong | The marketplace picks the useless wide-range vendor, shows customers 'delivery in 10 to 250 minutes', and loses orders to rivals who give a usable window. |
| Small numeric example | 10 deliveries. Vendor X: width 240, PICP = 1.0, MPIW = 240. Vendor Y: width 90, one miss (140 vs upper bound 135), PICP = 0.9, MPIW = 90. PICP picks X. Interval Score at 90%: X = 240; Y = (9×90 + 90 + 20×5)/10 = 100, so Y is clearly better. |

**6. Quick decision rule:** Use PICP with MPIW when you must communicate or monitor promised ranges and need a plain hit rate plus a width; avoid PICP alone, and avoid both when you need a single proper score to rank or train models (use the Interval Score or CRPS).

### Interval Score and Winkler Score

**1. What it measures (plain English):** A single proper score for an interval forecast. It charges for the width of the range and adds a heavy penalty, 2/alpha times the distance, whenever the actual value lands outside. For a 90% range alpha is 0.10, so the penalty is 20 times the miss. Also called the Winkler score; the average is the mean interval score.

`IS = (U − L) + (2/α) × (L − y) × 1(y < L) + (2/α) × (y − U) × 1(y > U)`

**2. Intuition:** Imagine a caterer quoting a price range for a wedding. A very wide range costs her credibility (width), and if the final bill lands outside the range she must pay a penalty that grows with the gap. The best strategy is a range that is as narrow as honesty allows.

**3. Benefits:**

- Proper: with the factor 2/alpha it cannot be gamed, so it is safe to use for model selection and training.
- Combines width and coverage into one number and penalises misses by how far they land outside, unlike PICP.
- In the units of the target and easy to split into width, under-shoot and over-shoot parts for diagnosis.
- Has a scaled version (MSIS) for series of different size and a multi-interval version (WIS) that approximates CRPS.
- Used in major forecasting competitions and public-health forecasting hubs.

**4. Limitations / Potential issues:**

- Scale-dependent, so raw values are not comparable across series; scale by a naive error (MSIS).
- The penalty multiplier is large (20 times for 90%, 40 times for 95%), so one big miss can dominate the average.
- You must pick alpha, and scores at different alpha levels cannot be compared.
- Hard to explain to non-technical readers; pair it with PICP and MPIW for communication.
- Only sees the two interval end points, not the shape of the distribution between them.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Choosing between two 90% ranges for monthly remittance inflows |
| Industry / Domain | banking (money-transfer liquidity, West Africa) |
| Business Problem | A money-transfer operator in Ghana keeps a cash buffer to pay out incoming remittances. Two forecasting vendors supply 90% ranges for monthly inflow; one is wide and safe, the other narrower with a small miss. |
| ML Translation | Target = monthly inflow in GHS million; interval forecasts at the 90% level (alpha = 0.10); 5 test months; choose the vendor by one proper score. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The Interval Score adds the width to a charge of 20 times the distance outside the range. It prefers the narrower vendor whose single miss was tiny and rejects a range that is simply too vague, so it handles the trade-off that PICP cannot. |
| Why other metrics are NOT suitable here | PICP alone picks the wide vendor (100% hits) although it is vague. MPIW alone picks any narrow vendor even if it misses badly. RMSE of the central forecast ignores the ranges that set the buffer size. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Choosing the wider vendor ties up extra cash in the buffer every month; choosing a vendor with big misses means payouts fail on peak days and customers go to rivals. |
| Small numeric example | 5 months, actuals = 52, 48, 60, 55, 70. Vendor A: width 14, all inside, PICP = 1.0, Interval Score = 14.0. Vendor B: width 8, last month 70 vs upper bound 69 (miss by 1): scores = 8, 8, 8, 8, 28; mean = 12.0, PICP = 0.8. B wins (12.0 versus 14.0) despite lower coverage. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Diagnosing why weekly emergency-department ranges keep failing |
| Industry / Domain | healthcare (hospital emergency department, New Zealand) |
| Business Problem | A hospital plans nurse rosters from an 80% range of weekly emergency-department arrivals. The ranges look fine most weeks but staff are overrun in surge weeks. The team wants to know whether to widen all ranges or fix something specific. |
| ML Translation | Target = weekly arrivals; 80% interval forecasts (alpha = 0.20, so the penalty multiplier is 2/0.20 = 10); 6 weeks; the score is split into width, under-shoot and over-shoot parts. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The Interval Score splits into a width part and a miss part. If most of the score comes from misses on the high side, the intervals are too tight in surge weeks, and the fix is a model that widens when demand is volatile, not a blanket widening. |
| Why other metrics are NOT suitable here | PICP says 5 of 6 hit but not how bad the miss was. MPIW shows width only. RMSE of the central forecast cannot tell whether the problem is the centre or the range. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Widening every range blindly overstaffs every ordinary week and costs rostering money; ignoring the surge-week misses leaves the department understaffed when it matters. |
| Small numeric example | 6 weeks, actuals = 310, 295, 350, 330, 420, 305. Ranges lower = 285, 270, 300, 305, 330, 280, upper = 345, 330, 380, 365, 390, 340. Per-week scores = 60, 60, 80, 60, 360, 60. Average width = 63.3, average over-shoot penalty = 50.0 (week 5: 420 − 390 = 30, ×10 = 300; 300/6 = 50), under-shoot = 0.0. Total = 113.3; 44% of the score is the surge-week miss, so fix the high side. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Comparing range quality for a city cluster and a rural cluster of base stations |
| Industry / Domain | telecom (mobile network traffic, Middle East) |
| Business Problem | A mobile operator forecasts weekly data volume with 90% ranges for a large city cluster and a small rural cluster. Management wants to know which cluster's forecasting is worse, but the volumes differ by a factor of 20. |
| ML Translation | Target = weekly data volume in terabytes; 90% interval forecasts for two series of very different size; the raw Interval Score is divided by the naive one-step error from history (the scaled version, MSIS). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | The raw Interval Score is in terabytes, so the big cluster always looks worse. Dividing by the average week-to-week change of each series (a naive yardstick) puts both on one scale, so the comparison is fair. |
| Why other metrics are NOT suitable here | Raw Interval Score is not comparable across scales. MAPE is not defined for ranges. PICP ignores the size of misses and cannot rank the two series by severity. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Comparing raw scores sends the engineering budget to the city cluster although its forecasts are relatively fine, while the rural cluster's weaker forecasting is left alone. |
| Small numeric example | City cluster: mean Interval Score = 386.7 TB; naive step error from history 1000, 1300, 1150, 1400, 1250 = 212.5; scaled = 1.82. Rural cluster: mean Interval Score = 19.0 TB; naive step error from 55, 62, 70, 58, 66 = 8.75; scaled = 2.17. Raw scores say the city is 20 times worse; scaled scores say the rural cluster is slightly worse (2.17 versus 1.82). |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — SMS to smallholders about days until the planting rains |
| Industry / Domain | agriculture (extension service, Malawi) |
| Business Problem | An agricultural extension service texts farmers a range for the number of days until planting rains start. Farmers need a message they can understand and trust. |
| ML Translation | Target = days until rain onset per district; 90% ranges; the audience is smallholder farmers and field officers with no statistics background. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | An Interval Score such as 19.8 days has no meaning for a farmer or a field officer. The score is right for ranking models inside the data team but cannot be explained in an SMS. |
| Why other metrics are NOT suitable here | RMSE is also abstract. NLL and CRPS need a statistics background. A single Interval Score cannot be read as a promise. |
| Better alternative (if BAD fit) | Report PICP and MPIW in plain words: 'in 4 of 5 districts the rain started inside our range; ranges are 3.8 days wide on average'. Keep the Interval Score for internal model selection. |
| Business impact of choosing wrong | Farmers who cannot understand how reliable the message is either ignore it or over-trust it, and plant too early; failed seedlings mean lost seed and a lost season. |
| Small numeric example | 5 districts, actual days = 6, 9, 5, 14, 7; ranges lower = 4, 5, 4, 6, 5, upper = 8, 9, 7, 10, 9. Mean Interval Score = 19.8 (district 4 missed by 4 days: 4 + 20×4 = 84 in that district alone). Plain-language version: PICP = 4/5 = 0.8, MPIW = 3.8 days. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Cyclone loss forecasts where the reinsurer needs the whole shape |
| Industry / Domain | insurance (reinsurance, Australia) |
| Business Problem | A reinsurer models next season's cyclone losses. Its capital model needs the full spread of possible losses, not just one 90% range. Two models give the same 90% range but disagree about the middle of the distribution. |
| ML Translation | Target = seasonal insured loss in AUD hundred million; quantile forecasts at several levels; the downstream capital model uses the whole distribution. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | A single 90% Interval Score only looks at the 5th and 95th percentiles, so two forecasts with the same outer range score identically even though the central 50% range, which drives expected claims, is very different. |
| Why other metrics are NOT suitable here | PICP and MPIW at 90% also ignore the middle. RMSE of the median ignores the range. NLL assumes a bell shape the cyclone losses do not have. |
| Better alternative (if BAD fit) | Weighted Interval Score over several nested intervals (it approximates CRPS) or CRPS from the full quantile set. |
| Business impact of choosing wrong | The reinsurer picks the model with the fatter middle, overstates expected claims and mis-prices treaties, or the reverse and under-reserves. |
| Small numeric example | Actual loss = 55. Both models have the 90% range (20, 80): Interval Score = 60 for both. The 50% range is (40, 60) for A and (30, 70) for B: scores 20 and 40. With median 50, Weighted Interval Score = (0.5×abs(55−50) + 0.05×60 + 0.25×50% score)/2.5: A = (2.5 + 3 + 0.25×20)/2.5 = 4.20, B = (2.5 + 3 + 0.25×40)/2.5 = 6.20. The 90% score alone saw no difference between the two models. |

**6. Quick decision rule:** Use the Interval Score when you need one proper number to compare or tune interval forecasts, especially when big misses are costly; avoid it for audiences who need plain hit rates (use PICP and MPIW) or when the whole distribution matters (use CRPS or WIS).

### PIT Histogram

**1. What it measures (plain English):** The histogram of the forecast's cumulative probability at each actual value (the probability integral transform). If the forecast distributions are honest these values are spread evenly between 0 and 1. The shape shows whether forecasts are biased, too narrow (over-confident) or too wide. For ensembles the same idea is the rank histogram.

`pᵢ = F̂ᵢ(yᵢ); for a Normal forecast pᵢ = Φ((yᵢ − μᵢ)/σᵢ)`

**2. Intuition:** Imagine a weather presenter who says '30% chance of rain' every time. Over many days, rain should occur on about 30% of those days. A PIT histogram checks this for every probability level at once: if reality keeps landing in the extremes of her forecast, she is over-confident.

**3. Benefits:**

- The most informative calibration diagnostic: one picture separates bias, over-confidence and under-confidence.
- Works for any predictive distribution, parametric or ensemble, with no shape assumption.
- Has a clear target (uniform) and compact monitoring numbers: mean 0.5 and variance 1/12.
- Transfers intuition from the classification calibration curve.
- Tells you which fix to apply: debias the centre or widen the ranges.

**4. Limitations / Potential issues:**

- Needs a few hundred observations; on small test sets it is just noise.
- Appearance depends on the number of bins.
- Shows only average (marginal) calibration; opposite failures in different segments can cancel out, so check by segment.
- Necessary but not sufficient: a forecast that always quotes the historical distribution has a perfect PIT and no skill, so pair it with CRPS or NLL.
- A visual tool: it cannot be trained on directly, and it needs a full predictive distribution (not a point forecast).

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Rank histogram for crosswind-gust ensemble forecasts at a regional airport |
| Industry / Domain | aviation (airport weather, Australia) |
| Business Problem | An airport weather team uses a 4-member ensemble of crosswind-gust forecasts to decide runway changes. Pilots complain that real gusts often fall outside the whole ensemble. The team needs to know whether the ensemble is too tight or biased. |
| ML Translation | Target = peak crosswind gust in knots; ensemble forecast (4 members); rank of the observation among the members (the discrete form of PIT) is collected each day; the shape of the histogram is read. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A rank histogram shows where reality lands within the ensemble. Many observations below the lowest or above the highest member give a U shape, a clear sign that the ensemble is over-confident (too tight), while a slope would show bias. |
| Why other metrics are NOT suitable here | RMSE of the ensemble mean cannot tell tight from biased. CRPS says how good the forecast is overall but not why. PICP at one level gives one point of the picture, not the shape. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | An over-confident ensemble makes the airport trust forecasts that are too tight, leading to late runway changes, diversions and delays for flights. |
| Small numeric example | 6 days, 4-member ensembles; ranks of the observation (0 = below all members, 4 = above all) = 0, 4, 4, 0, 4, 4. Counts for ranks 0 to 4 = 2, 0, 0, 0, 4. A calibrated ensemble would give about 1.2 per rank; here all observations sit at the two extremes, a U shape. (Six days is only a toy; use hundreds of days in practice.) |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Control chart on the PIT mean and spread of a monthly loss-forecast model |
| Industry / Domain | banking (retail lending, South Africa) |
| Business Problem | A bank's loan-loss forecasting model outputs a mean and a spread for each portfolio every month. The model-risk team wants two dashboard numbers that raise an alarm when the forecasts drift away from reality. |
| ML Translation | Target = monthly loss per portfolio; Gaussian predictive distribution; the PIT value (the forecast's cumulative probability at the actual) is computed for each portfolio; its mean and variance are tracked month by month. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | If the forecasts are calibrated the PIT values are spread evenly between 0 and 1: mean 0.5 and variance 1/12 = 0.083. A mean above 0.5 means actual losses land high in the forecast (the model under-forecasts); a variance above 0.083 means over-confidence. Two numbers, two different fixes. |
| Why other metrics are NOT suitable here | PICP at 90% falls in both situations and cannot say whether the centre or the width is wrong. RMSE is flat when the spread alone is wrong. NLL moves but gives no direction to act in. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Without the diagnosis the team would widen ranges when the real problem is a low-biased centre, wasting weeks and leaving under-provisioning in place. |
| Small numeric example | 10 portfolios per month. Month 1 z-scores (actual minus forecast mean, in spreads) = -1.5, -0.5, 0.3, 1.2, -0.2, 1.6, -1.1, 0.1, 0.9, -0.8 give PIT mean 0.49, variance 0.091. Month 2 z-scores = 0.6, 1.3, 0.9, 1.8, 0.2, 1.1, 0.4, 1.5, 0.8, 2.1 give PIT mean 0.82, variance 0.016. Target 0.50 and 0.083. Month 2 mean of 0.82 says actual losses are landing high, so the model under-forecasts and the centre needs fixing. (Ten points is a toy; real dashboards use hundreds.) |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Two salmon-weight forecasts that are both perfectly calibrated |
| Industry / Domain | agriculture (salmon farming, Chile) |
| Business Problem | A salmon farm compares two harvest-weight forecasts per pen: a model that simply quotes the farm-wide historical spread for every pen, and a model that uses each pen's feed and water data. The data team proposes choosing by whichever PIT histogram looks flatter. |
| ML Translation | Target = average harvest weight per pen (kg); probabilistic regression; model A is the unconditional (climatological) distribution; model B is conditional on pen data; compared over a large simulated set. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | A flat PIT histogram only proves calibration (honesty). The 'just quote history' forecast is perfectly calibrated and has no skill, so both models look equally good. PIT cannot measure sharpness. |
| Why other metrics are NOT suitable here | Looking at RMSE alone ignores the spread. PICP at one level also only checks honesty. Gaussian NLL would work too but is harder to explain; the issue is that a calibration check cannot rank skill. |
| Better alternative (if BAD fit) | CRPS (or NLL) as the ranking score, with PIT kept as a side check. CRPS rewards the sharper, equally calibrated forecast. |
| Business impact of choosing wrong | The farm picks the model with no information about individual pens, so feed and harvest planning get no benefit from the pen data it paid to collect. |
| Small numeric example | In a simulation of 400,000 pens with true noise spread 10 kg: model A (spread 14.1, history only) has PIT mean 0.500, variance 0.0834; model B (spread 10, uses pen data) has PIT mean 0.500, variance 0.0834; both match 0.5 and 0.0833. CRPS: A = 7.98 kg, B = 5.64 kg, a 29% improvement that PIT cannot see. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — A PIT histogram from only 30 weeks of blood-bank demand |
| Industry / Domain | healthcare (hospital blood bank, New Zealand) |
| Business Problem | A hospital blood bank has run a new probabilistic demand model for 30 weeks and wants to know if it is calibrated. An analyst draws a histogram of the 30 PIT values. |
| ML Translation | Target = weekly units of red cells needed; probabilistic regression; only 30 held-out weeks; a 5-bin PIT histogram and a 90% range check are considered. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | With 30 points a PIT histogram is ragged even for a perfectly calibrated model, so nobody can read a shape from it. Random scatter looks like U shapes or humps. |
| Why other metrics are NOT suitable here | A formal KS test on 30 points has little power to find real problems. RMSE gives no information about calibration. NLL on 30 points is also noisy. |
| Better alternative (if BAD fit) | Wait for hundreds of weeks, or in the meantime report PICP with an exact binomial confidence interval (Wilson interval) at one or two levels, which states the uncertainty about the hit rate. |
| Business impact of choosing wrong | Reacting to the ragged shape, the team retunes a model that was fine (wasted work, lost trust), or declares a miscalibrated model fine because the histogram looked flat. |
| Small numeric example | I generated 30 PIT values from a perfectly uniform source and counted them in 5 equal bins: counts = 6, 6, 5, 3, 10 (expected 6 each; the last bin has 10). A chi-square test gives p = 0.36, no evidence of a problem. With PICP: 25 of 30 inside = 0.833; Wilson 95% interval 0.664 to 0.927 contains 0.90, so 'not proven different from 90%'. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Point-forecast sales model for a Gulf fashion retailer |
| Industry / Domain | retail (fashion, Gulf region) |
| Business Problem | A fashion retailer's gradient-boosted model gives one forecast number per store. Management now wants to know how much to trust it and asks whether a PIT histogram can be drawn. |
| ML Translation | Target = weekly store sales in AED thousand; the model outputs a single value, no distribution; held-out residuals (actual minus forecast) are available. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | PIT needs a predictive distribution to evaluate at each actual value. A point model has none, so there is nothing to transform. |
| Why other metrics are NOT suitable here | CRPS and NLL also need a distribution. The Interval Score needs a range. RMSE and MAE can be computed but say nothing about uncertainty or calibration. |
| Better alternative (if BAD fit) | Wrap the point model in split-conformal prediction: use calibration residuals to build ranges, then check coverage with PICP and width with MPIW. After that, PIT-style checks are possible if a full distribution is produced. |
| Business impact of choosing wrong | Management would trust the single number as exact and plan stock around it, so stock-outs or markdowns follow when the real swing is larger than assumed. |
| Small numeric example | 9 calibration residuals (absolute) = 4, 7, 3, 9, 5, 6, 12, 2, 8. For an 80% range take the 8th smallest of the 9 (rank = ceil((9+1)×0.8)) = 9. Range = forecast ± 9. On 5 new weeks: actual = 105, 92, 130, 88, 100, forecast = 100, 95, 115, 90, 104; inside = 4 of 5, PICP = 0.80, MPIW = 18. |

**6. Quick decision rule:** Use the PIT histogram to diagnose why probabilistic forecasts are miscalibrated (bias versus over- or under-confidence) when you have hundreds of cases and a full predictive distribution; avoid it to rank models, on small samples, or for point forecasts.

## Choosing between models

### AIC

**1. What it measures (plain English):** A score for choosing between statistical models: how well the model fits the data, minus a charge of 2 for every estimated parameter, so that extra complexity must earn its place. Lower is better and only differences between models fitted to the same data matter. It estimates which model will predict new data best.

`AIC = 2k − 2 ln L̂`

**2. Intuition:** Think of hiring staff for a shop. A new employee (a parameter) should add more sales than their wage. AIC charges every extra parameter a fixed wage of 2 and keeps only those who earn it, so you do not end up with a huge payroll that merely looks busy.

**3. Benefits:**

- Estimates out-of-sample accuracy without holding data out, which is valuable when data is scarce or refitting is expensive.
- Asymptotically equivalent to leave-one-out cross-validation (it behaves like repeated hold-one-out testing when n is large).
- Cheap: one fit and one formula; works for non-nested models fitted to the same data.
- Akaike weights turn differences into model-support percentages for model averaging.
- Standard in time-series order selection, GLMs, ecology and actuarial work.

**4. Limitations / Potential issues:**

- Needs a likelihood and a clear parameter count; not valid for random forests, boosted trees or neural networks.
- Assumes the likelihood family is right (for OLS: bell-shaped, equal-variance, independent errors).
- Biased for small samples; use AICc when n/k is below about 40.
- Not consistent: even with unlimited data it keeps a small chance of choosing an over-large model.
- Absolute values are meaningless; do not compare across software, sample sizes or transformed targets (without a Jacobian correction).

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — How many seasonal waves does a wildlife-park gate need |
| Industry / Domain | tourism (national park, East Africa) |
| Business Problem | A park authority models daily visitors at a gate over two years using sine and cosine seasonal terms (harmonics). More terms always fit the past better, so it needs a rule for when to stop. |
| ML Translation | Target = daily visitor count; linear regression with 0 to 4 pairs of harmonic terms (parameter count k = 2, 4, 6, 8, 10 including intercept and error variance); n = 730 days; errors roughly bell-shaped. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | AIC adds a charge of 2 per parameter to the fit, so extra waves must pay for themselves. With 730 days and at most 10 parameters, the sample is large relative to k (730/10 = 73, above the usual 40), so plain AIC is reliable and no hold-out data is needed. |
| Why other metrics are NOT suitable here | In-sample R-squared or RMSE always prefer the biggest model. BIC would also work but is stricter and targets the 'true' model, not forecasting accuracy. Cross-validation is valid but needs repeated refits and a careful time split. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Picking by in-sample fit adds waves that chase noise and give wobbly forecasts, so rangers and gate staff are rostered for crowds that never come. |
| Small numeric example | n = 730; residual sum of squares (RSS) for 0 to 4 harmonic pairs = 4.20, 2.50, 1.72, 1.713, 1.708 million. AIC = n×ln(RSS/n) + 2k + n×(1+ln 2π), giving 8395.7, 8020.9, 7751.9, 7753.0, 7754.8. Differences from the best: 643.7, 269.0, 0.0, 1.0, 2.9; Akaike weights = 0.000, 0.000, 0.545, 0.327, 0.128. Two pairs (k = 6) wins; the extra waves cut RSS by under 1% and cost 2 each. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Rainfall model versus temperature model for smallholder maize yield |
| Industry / Domain | agriculture (smallholder maize survey, Kenya) |
| Business Problem | An agricultural research group has 400 farm-season records and three rival explanations of maize yield: a rainfall curve, a temperature line, and rainfall plus fertiliser. The models are not versions of each other, so a standard nested test cannot compare them. |
| ML Translation | Target = yield in kg per hectare; three regression models with different predictors (k = 4, 3, 5); same 400 rows; AIC compares them on one scale. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | AIC compares models that are not nested, using only the fit and the parameter count, on the same data. Akaike weights then express how much each rival is supported, instead of an arbitrary yes or no. |
| Why other metrics are NOT suitable here | An F-test (a significance test for nested models) cannot compare non-nested models. Adjusted R-squared is cruder in its penalty and gives no weights. A hold-out test works but wastes data when only 400 records exist. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Choosing a rainfall-only story when fertiliser also matters sends extension officers out with advice that explains less of the yield gap, so farmers see poorer returns. |
| Small numeric example | n = 400; RSS = 40300, 44000, 39000; k = 4, 3, 5 for rainfall, temperature, rainfall plus fertiliser. AIC = 2988.2, 3021.3, 2977.1; differences = 11.1, 44.3, 0.0; Akaike weights = 0.004, 0.000, 0.996. Rainfall plus fertiliser wins; temperature is 44 units worse, so it has essentially no support. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Poisson versus negative binomial for motor claim counts |
| Industry / Domain | insurance (motor, Brazil) |
| Business Problem | An insurer models the number of claims per policy-year for 2,000 policies. Claim counts have more spread than a Poisson allows (some drivers claim repeatedly). Three count-model families are candidates. |
| ML Translation | Target = number of claims per policy; count regression; three likelihood models (Poisson, negative binomial, zero-inflated Poisson) with k = 5, 6, 10 parameters; AIC computed straight from the log-likelihood. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | AIC works for any model that has a likelihood, not only the bell-shaped regression, and can compare different distribution families fitted to the same counts. The parameter count is clear and the sample is large (2,000 against 10). |
| Why other metrics are NOT suitable here | RMSE of predicted counts ignores how well the distribution of counts is described, which drives premium pricing. R-squared is not meaningful for count likelihoods. Hold-out log-likelihood would work but throws away data. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A Poisson model understates the chance of multiple claims, so heavy claimants are under-priced and the portfolio loses money on exactly those drivers. |
| Small numeric example | Log-likelihoods = -1052.3, -1021.8, -1019.5; k = 5, 6, 10. AIC = 2k − 2×logL = 2114.6, 2055.6, 2059.0; differences = 59.0, 0.0, 3.4; weights = 0.000, 0.846, 0.154. Negative binomial wins by 59 over Poisson; the zero-inflated model is only 3.4 behind, so keep it as a close second. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Ridge model versus random forest for used-tractor resale values |
| Industry / Domain | retail (used farm machinery, Argentina) |
| Business Problem | A tractor dealer network prices used machines in 500 sales. The data team compares a ridge-regression model with a random forest (hundreds of decision trees averaged) and wants to use AIC to choose. |
| ML Translation | Target = resale value; regression; 500 rows; the random forest has no likelihood and no clear parameter count (leaves, trees, splits?). |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | AIC needs a likelihood and a well-defined number of parameters k. A forest fits its training data almost perfectly, and whatever k is plugged in decides the answer, so the ranking is arbitrary. |
| Why other metrics are NOT suitable here | BIC has the same problem. Adjusted R-squared also assumes a linear model. In-sample RMSE favours the forest because it memorises the training data. |
| Better alternative (if BAD fit) | K-fold cross-validated RMSE, which measures real out-of-sample error for any model with no k needed. |
| Business impact of choosing wrong | Choosing by an arbitrary k either sends a worse model into dealer pricing or rejects a better one, so used tractors are mis-priced across the network. |
| Small numeric example | n = 500. Ridge: in-sample RMSE 7.0 (RSS = 24500), k = 14, AIC = 3393. Forest: in-sample RMSE 2.5 (RSS = 3125); AIC with k = 14 is 2363 (forest wins), with k = 1,500 is 5335 (ridge wins). The answer flips with an undefined k. Cross-validated RMSE: ridge 7.3, forest 6.4, which picks the forest without needing k. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Raw versus log scale defect counts in a brake-part factory |
| Industry / Domain | manufacturing (auto parts, Mexico) |
| Business Problem | A plant engineer fits one model for defects per batch and another for the logarithm of defects per batch, then compares their AIC values to pick the better one. |
| ML Translation | Target = defects per batch (about 90 on average) in 50 batches; model R fits raw defects, model L fits ln(defects); the AIC of each is calculated from its own residuals on its own scale. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | AIC is built from the likelihood of the target, so a model of ln(y) and a model of y describe different quantities. The log model's residuals are tiny numbers, so it wins by default. Comparing them requires a Jacobian correction (adding 2 times the sum of ln y). |
| Why other metrics are NOT suitable here | BIC and Mallows' Cp have the same flaw. RMSE on different scales is not comparable either. |
| Better alternative (if BAD fit) | Convert the log-model's predictions back to the raw scale and compare cross-validated RMSE there, or apply the Jacobian correction to the AIC before comparing. |
| Business impact of choosing wrong | The plant adopts the model that only looked better because of the scale, and its defect forecasts for scheduling inspections are wrong by tens of units per batch. |
| Small numeric example | n = 50, k = 4 each. Raw model RSS = 62,500: AIC = 506.4. Log model RSS = 10: AIC = 69.4, so the naive comparison says log wins by 437. Correction: add 2×50×4.5 (mean ln y = 4.5) = 450, giving 519.4. Now the raw model wins by 13.0. |

**6. Quick decision rule:** Use AIC to choose among likelihood-based models fitted to the same data when prediction is the goal and n/k is large; avoid it for tree ensembles or neural nets, for small n/k (use AICc) or when comparing different target transformations.

### AICc

**1. What it measures (plain English):** AIC with an extra correction for small samples. It adds 2k(k+1)/(n−k−1) to AIC, which is large when the number of parameters is a big share of the number of observations and disappears as n grows. Use it whenever n/k is below about 40. Lower is better.

`AICc = AIC + 2k(k+1)/(n − k − 1)`

**2. Intuition:** AIC is a taxi meter that charges 2 per extra passenger. With a small cab (few data points) the real cost of an extra passenger is much higher, so AICc raises the fare steeply as the cab fills up and refuses bookings when every seat is taken.

**3. Benefits:**

- Fixes AIC's tendency to over-fit when the sample is small relative to the number of parameters.
- Converges to AIC when n is large, so it is a safe default at any size.
- One fit, no hold-out data needed; ideal for short time series and pilot studies.
- Keeps Akaike weights and model-averaging tools.
- Common default in ecology, short-series ARIMA selection and other small-sample fields.

**4. Limitations / Potential issues:**

- Undefined when n − k − 1 is zero or negative (as many parameters as data).
- Still needs a likelihood and a parameter count, so not for trees or neural nets.
- Derived for linear-Gaussian models; the correction is only approximate for other families.
- Adds nothing when n is huge, and does not tell you whether prediction or explanation is the goal.
- Same comparison rules as AIC: same data, same n, same convention, no transformed targets.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Pilot study of 14 rural water kiosks in Zambia |
| Industry / Domain | utilities (rural water kiosks, Southern Africa) |
| Business Problem | A rural water programme has 14 pilot kiosks and wants to know which of several revenue models (1, 2, 3 or 5 predictors such as population, distance and tariff) is supported. More data will arrive only next year. |
| ML Translation | Target = monthly kiosk revenue in ZMW; regression with k = 3, 4, 5, 7 parameters; only n = 14 observations, so n/k is about 2 to 5, far below 40. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | AIC is optimistic when n is small and tends to pick too many predictors. AICc adds the correction 2k(k+1)/(n−k−1), which is large here, and protects against over-fitting the 14 kiosks. |
| Why other metrics are NOT suitable here | Plain AIC picks a bigger model than the data can support. In-sample R-squared always picks the biggest. BIC has no small-sample correction either and was designed for large n. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | An over-fitted revenue model produces confident but wrong predictions for the next 100 kiosks, so funds are directed to sites that will not pay their running costs. |
| Small numeric example | n = 14; RSS = 3000, 1450, 1250, 1180; k = 3, 4, 5, 7. AIC = 120.9, 112.7, 112.6, 115.8 (3 predictors best by 0.08). AICc = AIC + 2k(k+1)/(n−k−1) = 123.3, 117.1, 120.1, 134.5; the corrections are 2.4, 4.4, 7.5, 18.7. AICc picks the 2-predictor model; the 5-predictor one is 17.3 worse. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Choosing the memory length for 20 years of vineyard harvests |
| Industry / Domain | agriculture (wine grapes, New Zealand) |
| Business Problem | A vineyard group has only 20 annual harvest totals and wants to choose how many past years an autoregressive model (AR, today depends on the last p years) should use for planning cellar capacity. |
| ML Translation | Target = annual harvest tonnes; AR(0), AR(1), AR(2), AR(4) with k = 2, 3, 4, 6 parameters; n = 20 yearly values. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | With 20 points and up to 6 parameters, AIC rewards the longest memory, which is a classic small-sample trap. AICc penalises it enough to prefer the short memory that a 20-year record can support. |
| Why other metrics are NOT suitable here | Plain AIC prefers AR(4). Cross-validation with only 20 points leaves tiny training sets and noisy estimates. BIC does not correct for small samples. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Choosing AR(4) fits the noise of two decades and then mis-forecasts harvests, leaving cellars short of tank space or paying for capacity that is not needed. |
| Small numeric example | n = 20; RSS = 8000, 4100, 3600, 2500; k = 2, 3, 4, 6. AIC = 180.6, 169.2, 168.6, 165.3, so AIC picks AR(4). AICc = 181.3, 170.7, 171.3, 171.8, so AICc picks AR(1), with AR(2) 0.57 behind. Correction for AR(4): 2×6×7/(20−6−1) = 6.46. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Quoting build hours from 16 past boat builds |
| Industry / Domain | manufacturing (boat building, New Zealand) |
| Business Problem | A small boat builder has 16 finished builds and wants a quoting formula for labour hours. It can use 1, 3 or 5 size and finish variables. A bad choice means mis-quoted jobs. |
| ML Translation | Target = build hours; regression with k = 3, 5, 7 parameters; n = 16 records. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | A very small record needs the small-sample correction. AICc penalises the 5-variable model hard (correction of 2×7×8/8 = 14), steering the builder to the simplest formula that the data supports. |
| Why other metrics are NOT suitable here | Plain AIC prefers the 5-variable model. Adjusted R-squared penalises only lightly. A hold-out test on 16 builds would leave 3 or 4 test jobs, far too few. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | An over-complicated formula looks accurate on past builds but mis-quotes new orders, so the yard either loses jobs by quoting high or loses money by quoting low. |
| Small numeric example | n = 16; RSS = 2600, 1700, 1250; k = 3, 5, 7. AIC = 132.9, 130.1, 129.1 (5-variable model best). AICc = 134.9, 136.1, 143.1, so the 1-variable model wins; the 3-variable one is 1.2 behind and the 5-variable one 8.3 behind. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Nine months of clinic data and six candidate predictors |
| Industry / Domain | healthcare (rural clinic, Malawi) |
| Business Problem | A rural clinic wants to explain monthly patient visits from six factors (rainfall, market day, season and others) using only 9 months of records. |
| ML Translation | Target = monthly visits; regression; n = 9; the full model with 6 predictors has k = 8 parameters, so n − k − 1 = 0. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | AICc divides by n − k − 1, which is zero for the full model (undefined) and tiny for large models. There is no real information in 9 rows to compare so many models. |
| Why other metrics are NOT suitable here | Plain AIC will happily choose the full 6-predictor model. BIC and Cp need a trustworthy error estimate from the full model, which does not exist here. In-sample R-squared is 0.99 and useless. |
| Better alternative (if BAD fit) | Leave-one-out cross-validation (PRESS), or a simple model fixed by clinical knowledge, or a regularised model; and collect more months. |
| Business impact of choosing wrong | The clinic would build staffing plans on a model that fits 9 numbers perfectly and predicts the next month badly. |
| Small numeric example | Simulated 9 months where only predictor 1 matters. 1-predictor model: RSS = 5.15, AIC = 26.5, AICc = 31.3; 5-predictor model: AIC = 25.2, AICc = 137.2 (correction 2×7×8/1 = 112); 6-predictor model: k = 8, n−k−1 = 0, AICc undefined. In-sample R-squared for 6 predictors = 0.995, but leave-one-out R-squared = 1 − PRESS/SST = -1.59; for 1 predictor it is 0.86. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Customer-spend model on 200,000 telecom accounts |
| Industry / Domain | telecom (mobile operator, Nigeria) |
| Business Problem | A mobile operator compares an 8-parameter and a 12-parameter model of monthly customer spend on 200,000 accounts. An analyst insists on AICc because 'it is safer than AIC'. |
| ML Translation | Target = monthly spend in NGN; regression; n = 200,000; n/k is about 20,000, far above 40. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | With so much data the AICc correction is about 0.001, so AICc equals AIC and adds nothing. The real question is not small-sample bias but what the model is for: prediction or explanation. |
| Why other metrics are NOT suitable here | Plain AIC gives the same answer. Adjusted R-squared is too lenient at this n. Cross-validated RMSE is what directly measures prediction. |
| Better alternative (if BAD fit) | BIC if a parsimonious, explainable model is the goal; cross-validated RMSE if prediction is the goal. AICc is only a safe default, not a decision tool, at this n. |
| Business impact of choosing wrong | No money is lost by using AICc, but time is spent on a check that cannot change the decision, while the real choice (explain versus predict) is left unmade. |
| Small numeric example | n = 200,000; RSS = 4.0 million (k = 8) and 3.9 million (k = 12). AIC difference = 5055.562; AICc difference = 5055.561. Correction for k = 12: 2×12×13/(200,000−13) = 0.00156. No ranking change. |

**6. Quick decision rule:** Use AICc when n/k is below about 40, for short series and pilot studies where over-fitting is the main risk; avoid it when n is huge (it equals AIC), when n is not much larger than k (use cross-validation or a simpler model), or for models with no likelihood.

### BIC (SIC / SBC)

**1. What it measures (plain English):** A model-choice score like AIC, but each extra parameter costs k×ln(n) instead of 2, so it penalises complexity more heavily as the dataset grows. It approximates which model is most likely to be the true one. Also called SIC or SBC (Schwarz criterion). Lower is better and only differences matter.

`BIC = k × ln(n) − 2 ln L̂`

**2. Intuition:** AIC is an interviewer who forgives a few unnecessary skills on a CV. BIC is a stricter one: the bigger the pool of applicants (the sample), the higher the bar for every extra skill, until only the essential ones are listed.

**3. Benefits:**

- Consistent: if the true model is among the candidates, it is chosen with probability approaching 1 as n grows.
- Favours smaller, more stable and more explainable models, which suits regulation and reporting.
- Differences approximate log Bayes factors, giving a probability interpretation (BIC weights).
- Cheap: one fit per model; the standard way to choose the number of components in Gaussian mixture models.
- Resists the large-sample tendency to keep trivial effects.

**4. Limitations / Potential issues:**

- Assumes the true model is among the candidates, which is almost never exactly true.
- Often under-fits when the goal is prediction with many weak but real effects.
- Needs a likelihood and a parameter count; not usable for trees or neural networks.
- Not comparable across different n, software or transformed targets; no small-sample correction.
- The implied prior is arbitrary, and all parameters are charged equally.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — How many types of mobile-money agent are there |
| Industry / Domain | banking (mobile-money agent segmentation, East Africa) |
| Business Problem | A mobile-money operator wants to group 1,000 agents by monthly transaction volume into types (small rural, mid-size town, large trading hub) to design different support and pricing. It needs to decide how many groups to use. |
| ML Translation | Unsupervised density model (Gaussian mixture) of transaction volume; K = 1 to 4 components with k = 3K − 1 = 2, 5, 8, 11 parameters; n = 1,000 agents; BIC chooses K. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | More components always raise the likelihood, so likelihood alone would pick the most groups. BIC charges k×ln(n) = 6.9 per parameter at n = 1,000, so it stops at the number of groups that the data clearly supports, which also keeps the segments explainable to the business. |
| Why other metrics are NOT suitable here | In-sample likelihood always picks the maximum K. AIC charges only 2 per parameter and picks 4 groups, one more than BIC. Predictive error (RMSE) does not exist for unsupervised clustering. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Too many groups produces segments that are nearly identical; the operator builds and maintains separate pricing and support plans for them, increasing cost with no gain. |
| Small numeric example | n = 1,000, ln(n) = 6.908; log-likelihoods = -3400, -3250, -3228, -3222; k = 2, 5, 8, 11. AIC = 6804.0, 6510.0, 6472.0, 6466.0 (picks K = 4). BIC = k×ln(n) − 2×logL = 6813.8, 6534.5, 6511.3, 6520.0 (picks K = 3). K = 4 is 8.7 worse by BIC. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — A regulator-friendly pricing model for funeral cover |
| Industry / Domain | insurance (funeral cover, South Africa) |
| Business Problem | An insurer's pricing model must be explained to the regulator, which dislikes long variable lists. The firm has 20,000 policies and models with 4, 8 or 12 rating factors. |
| ML Translation | Target = claim cost per policy; regression with k = 6, 10, 14 parameters; n = 20,000; the goal is a small defensible variable set, not the last drop of accuracy. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | At n = 20,000 BIC charges ln(n) = 9.9 per parameter versus 2 for AIC. It keeps the 8-factor model and rejects the last 4 factors, which improve the fit by only 0.1%, giving a smaller model that is easier to defend. |
| Why other metrics are NOT suitable here | AIC picks the 12-factor model (the extra factors help slightly). In-sample R-squared always rises. Cross-validated RMSE would also be nearly identical, so it does not help the explainability decision. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A bloated rating model invites regulator challenge and creates unfair-looking price differences that customers and the regulator question. |
| Small numeric example | n = 20,000, ln(n) = 9.903; RSS = 5,000,000, 4,900,000, 4,895,100; k = 6, 10, 14. AIC = 167198.8, 166802.7, 166790.7 (picks 12 factors by 12.0). BIC = 167246.2, 166881.7, 166901.3 (picks 8 factors; the 12-factor model is 19.6 worse). The last 4 factors lower RSS by only 0.10%. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Memory length of a river-flow model for a hydrology agency |
| Industry / Domain | environment and utilities (river hydrology, Colombia) |
| Business Problem | A national hydrology agency models daily river flow with an autoregressive model (today depends on the last p days). The model feeds flood warnings, so the agency wants a stable, simple one rather than one that keeps changing as data is added. |
| ML Translation | Target = daily flow; AR(1) to AR(4) with k = 3, 4, 5, 6 parameters; n = 3,000 days; goal is to find the real memory length. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | BIC is consistent: with lots of data and a true short memory it settles on the right order. Here AR(3) wins, and AR(4) is rejected firmly (6.8 worse), while AIC cannot rule AR(4) out (0.75 worse). |
| Why other metrics are NOT suitable here | AIC leaves AR(4) as an almost equal competitor. In-sample error always favours the longest memory. Cross-validated error is also fine, but the agency wants the principled, reproducible rule that BIC gives. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | An over-long memory makes the warning model unstable from one season to the next, so flood alerts fluctuate and downstream communities lose trust. |
| Small numeric example | n = 3,000, ln(n) = 8.006; RSS = 2.80, 2.45, 2.40, 2.399 million; k = 3, 4, 5, 6. AIC differences from the best = 458.45, 59.86, 0.00, 0.75. BIC differences = 446.44, 53.85, 0.00, 6.76. Both pick AR(3); BIC puts AR(4) 6.76 behind (strong evidence against) while AIC gap is only 0.75. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Predicting used-car auction prices with many small effects |
| Industry / Domain | automotive (used-car resale, Gulf region) |
| Business Problem | A used-car dealer group in the Gulf has 240 auction records and wants to forecast the hammer price. The dataset has 12 candidate features; many have small but real effects (mileage, trim, colour, service history, and so on). |
| ML Translation | Target = auction price in AED thousand; regression with 5 versus 12 features (k = 7 and 14); n = 240; the goal is prediction accuracy on new cars. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | BIC aims at the single true model and charges 5.5 per parameter at n = 240, so it throws away weak but genuine predictors. For forecasting this under-fits, while AIC and cross-validation target prediction. |
| Why other metrics are NOT suitable here | In-sample R-squared always prefers more variables. Mallows' Cp would behave like AIC. A p-value filter is arbitrary and ignores prediction. |
| Better alternative (if BAD fit) | AIC or, better, k-fold cross-validated RMSE, which measures real prediction error and keeps weak real signals. |
| Business impact of choosing wrong | Pricing with the shrunk model leaves systematic errors of about 0.8 thousand AED per car; across thousands of auction decisions that is real margin. |
| Small numeric example | n = 240, ln(n) = 5.481; RSS = 43,200 (5 features, k = 7) and 38,128 (12 features, k = 14). AIC = 1941.4, 1925.4 (picks 12 features); BIC = 1965.8, 1974.2 (picks 5 features). Cross-validated RMSE (5-fold): 5 features 14.1, 12 features 13.3, so the model BIC rejected predicts better. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Comparing salary models fitted on different sets of employees |
| Industry / Domain | HR (compensation analytics, Gulf bank) |
| Business Problem | A bank's HR analytics team compares two salary models. Model A (3 predictors) uses all 120 employees. Model B adds a performance rating that exists for only 90 of them, so it is fitted on 90 rows. They compare the two BIC values. |
| ML Translation | Target = monthly salary in AED thousand; regression; Model A n = 120, k = 5; Model B n = 90, k = 6; BIC computed separately for each. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | BIC (like AIC) is a likelihood summed over the observations, so a model fitted on fewer rows has a smaller likelihood term and a smaller BIC for that reason alone. The two numbers are not on the same footing. |
| Why other metrics are NOT suitable here | AIC and AICc have the same flaw. RMSE on different rows compares different employees. Adjusted R-squared is also computed on different samples. |
| Better alternative (if BAD fit) | Refit Model A on the same 90 employees and compare BIC on identical rows, or compare cross-validated RMSE on a common set of rows. |
| Business impact of choosing wrong | The bank adopts the more complex model on a false signal and builds pay-equity adjustments on a variable that does not improve prediction. |
| Small numeric example | Model A on 120 rows (RSS 12,000, k = 5): BIC = 917.1. Model B on 90 rows (RSS 8,280, k = 6): BIC = 689.4, so B looks better by 227.7. Refit A on the same 90 rows (RSS 8,500, k = 5): BIC = 687.2, so A wins by 2.1. |

**6. Quick decision rule:** Use BIC when you want a small, explainable, stable model or to choose the number of clusters or mixture components with plenty of data; avoid it when the goal is pure prediction, when models have no likelihood, or when the models are fitted to different rows.

### Mallows' Cp

**1. What it measures (plain English):** A score for choosing a subset of predictors in a linear regression. It compares the subset's error with the noise level of the full model, adjusted for the number of parameters. A good subset has Cp close to its parameter count p, and you choose the smallest subset that achieves this.

`Cp = RSS_p / σ̂²_full − n + 2p`

**2. Intuition:** Imagine packing for a trip. The full suitcase (full model) shows how much stuff you could take. Cp asks how much a smaller bag loses, measured against the weight of the full case. If the loss is no more than the expected weight of the bag itself, you packed light without leaving out anything important.

**3. Benefits:**

- Gives an easy target (Cp close to p) and a plot of Cp against p that makes the choice visual.
- Designed specifically for choosing subsets in linear regression; standard in best-subset tools (leaps, regsubsets).
- For Gaussian linear models it picks the same model as AIC, a reassuring cross-check.
- Cheap: only needs each subset's RSS and one variance estimate from the full model.
- Directly shows bias from omitted variables (Cp much larger than p).

**4. Limitations / Potential issues:**

- Needs a trustworthy full model to estimate noise variance; breaks when the full model has nearly as many parameters as rows or is misspecified.
- Only defined for linear models; no meaning for trees, forests or neural networks.
- No small-sample correction, and unusable when there are more predictors than observations.
- Largely superseded by AIC, AICc and cross-validation in modern practice.
- Cp values fluctuate in small samples; the target Cp ≈ p is approximate.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Choosing feed and weather factors for milk yield per cow |
| Industry / Domain | agriculture (dairy, New Zealand) |
| Business Problem | A dairy research farm has 40 herd-season records and 5 candidate explanations of milk yield (pasture cover, rainfall, supplement feed and others). It wants the smallest set of factors that does not leave important ones out. |
| ML Translation | Target = milk solids per cow; linear regression; all subsets of 5 candidate predictors; the full model has 6 parameters with intercept and a reliable error variance from 34 degrees of freedom; n = 40. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Cp compares each subset's error with the noise level of the full model. A subset with Cp close to its parameter count p has no important omitted variables, so you take the smallest such subset. With 40 rows and 5 candidates the full-model variance is trustworthy. |
| Why other metrics are NOT suitable here | R-squared always rises with more variables. AIC picks the same subsets in this linear-Gaussian setting, so it is an equal alternative, not a better one. Cross-validation works but needs many refits across all subsets. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Dropping a real factor biases feeding advice for every herd; keeping useless factors costs the farm measurement effort and makes the model fragile. |
| Small numeric example | n = 40, RSS of the full model = 1,260 on 34 degrees of freedom, so noise variance = 37.06. Cp = RSS/variance − n + 2p. p = 2: 71.9 (far above 2, factors missing); p = 3: 6.5; p = 4: 3.9 (below 4, no evidence of bias); p = 5: 4.8. Choose p = 4 (3 factors), the smallest with Cp at or below p. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Picking cement additives that drive 28-day strength |
| Industry / Domain | manufacturing (cement plant, Egypt) |
| Business Problem | A cement plant has 50 test batches and 6 candidate additive and process factors for 28-day strength. The lab wants a lean recipe model that does not miss a key additive. |
| ML Translation | Target = compressive strength in MPa; linear regression; best-subset search over 6 candidates; full-model variance estimated from 43 degrees of freedom; n = 50. |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Best-subset search with Cp is a classic quality-lab tool: each subset is judged against the full model's noise, and the lab picks the smallest subset whose Cp is near p. The sample is large compared with the number of candidates. |
| Why other metrics are NOT suitable here | R-squared never penalises extra factors. Adjusted R-squared is a cruder trade-off. BIC would tend to pick fewer additives, which may drop a small but real effect the plant wants to keep. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | A recipe that omits a real additive gives batches that miss the strength grade (rejected product), while one with extra factors adds testing cost. |
| Small numeric example | n = 50, full model RSS = 880 on 43 degrees of freedom, variance = 20.47. Cp = 81.0, 26.9, 6.9, 5.2 for p = 2, 3, 4, 5 (RSS = 2,600, 1,450, 1,000, 925). p = 4 gives 6.9, still above 4 (some bias); p = 5 gives 5.2, close to 5. Choose p = 5 (4 additives). |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Twelve hotel-months and nine candidate predictors |
| Industry / Domain | tourism (hotel chain, Gulf region) |
| Business Problem | A hotel chain has 12 hotel-month records and 9 candidate drivers of occupancy (events, flights, price and so on). An analyst wants to use Mallows' Cp to find the best small model. |
| ML Translation | Target = occupancy rate; linear regression; n = 12; the full 9-predictor model has 12 − 10 = 2 degrees of freedom left, so its error variance rests on 2 numbers. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Cp measures every subset against the full model's variance. With only 2 degrees of freedom that variance estimate is wildly unstable, so Cp swings from 'terrible' to 'fine' for the same subset. |
| Why other metrics are NOT suitable here | AICc is undefined or huge for big models at this n. In-sample R-squared is about 1 for the full model. Plain AIC would choose the full model. |
| Better alternative (if BAD fit) | Leave-one-out cross-validation (PRESS), which needs no full-model variance, or a simple model chosen by hotel knowledge; and gather more months. |
| Business impact of choosing wrong | The chain either keeps a model that over-fits 12 data points and mis-staffs hotels, or throws away a good one because Cp looked bad by luck. |
| Small numeric example | Suppose a 1-predictor subset has RSS = 10 (true noise variance 1, p = 2). The full-model variance estimate on 2 degrees of freedom can fall anywhere from 0.051 to 3.00 times the truth (5th to 95th percentile). Cp = 10/variance − 12 + 4 = 2.0 if the estimate is exact, but 187 if it is 0.051 and -4.7 if it is 3.00. In a simulated dataset, leave-one-out PRESS = 15.1 for the 1-predictor model versus 167.2 for the full model, giving a clear verdict. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Random forest for delivery fuel use on a fleet |
| Industry / Domain | logistics (trucking, Brazil) |
| Business Problem | A haulage company has a random forest predicting fuel use per trip on 200 trips. An analyst wants to use Mallows' Cp to decide how complex the forest should be. |
| ML Translation | Target = litres per trip; non-linear tree ensemble; no explicit parameter count; the noise variance of 15 is borrowed from a linear model. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Cp is defined for linear models where p is the number of coefficients. A random forest has no such p (trees? leaves? effective parameters?), and the result depends entirely on the number plugged in. |
| Why other metrics are NOT suitable here | AIC and BIC need a likelihood and parameter count, so they fail in the same way. Adjusted R-squared is also linear-model only. |
| Better alternative (if BAD fit) | K-fold cross-validated RMSE, which works for any model and measures real error. |
| Business impact of choosing wrong | A made-up p leads to a forest tuned to look good on paper; trip fuel budgets are then wrong and drivers and dispatchers lose trust in the tool. |
| Small numeric example | n = 200, RSS = 3,000, variance 15: Cp = RSS/variance − n + 2p = 200 − 200 + 2p. With p = 3 this is 6; with p = 300 it is 600. The model has not changed, only the guess for p. Cross-validated RMSE has no such free choice. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Office-rent model where distance to transit is curved |
| Industry / Domain | real estate (commercial offices, South Africa) |
| Business Problem | A property firm models office rent per square metre across suburbs with a straight-line regression, then applies Cp using the full straight-line model as the benchmark. The true effect of distance to a transit hub is curved. |
| ML Translation | Target = rent in ZAR per square metre; linear regression with 5 candidate predictors; n = 40; the full linear model misses the curvature, so its leftover error is inflated. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Cp assumes the full model is right apart from random noise. If the full model is misspecified, its error variance is inflated and every subset looks unbiased, so Cp reports 'no problem' when the model is clearly wrong. |
| Why other metrics are NOT suitable here | AIC and BIC share the assumption that the model family is right. R-squared does not check curvature either. |
| Better alternative (if BAD fit) | Residual diagnostics plus cross-validated RMSE, with a quadratic distance term added; then compare subsets again with Cp or AIC. |
| Business impact of choosing wrong | The firm trusts a straight-line rent model that is off by tens of rand per square metre in the suburbs near transit, so leases are mispriced on exactly the best-located buildings. |
| Small numeric example | Full straight-line model: RSS = 2,040 on 34 degrees of freedom, variance = 60. A 2-predictor subset (p = 3) with RSS = 2,220 has Cp = 2,220/60 − 40 + 6 = 3.0, equal to p, so it looks fine. With the curve added the noise variance falls to 10, and the same subset's Cp = 2,220/10 − 40 + 6 = 188, showing heavy bias. |

**6. Quick decision rule:** Use Mallows' Cp for best-subset selection in linear regression when n is comfortably larger than the number of candidate predictors; avoid it when the full model is unreliable, the model is not linear, or you have more predictors than rows (use cross-validation).

### PRESS and Cross-Validated Error

**1. What it measures (plain English):** PRESS is the total squared error when every observation is predicted by a model fitted without it (leave-one-out cross-validation). Cross-validated RMSE or MAE does the same with k folds and any metric. Both measure the real out-of-sample error instead of estimating it from a formula. Predicted R-squared is 1 − PRESS/SST.

`PRESS = Σ (yᵢ − ŷ₍₋ᵢ₎)² = Σ (eᵢ / (1 − hᵢᵢ))²`

`Predicted R² = 1 − PRESS / SST`

**2. Intuition:** A driving instructor does not judge a student on the road he practised a hundred times. She puts him on a new road and sees how he drives. Cross-validation does the same with data: each fold plays the new road.

**3. Benefits:**

- Assumption-free: needs no likelihood, no parameter count and no distribution shape.
- Works for any model (linear, trees, deep nets) and any metric, including business-specific ones.
- Directly estimates generalisation error; the gap between training error and cross-validated error measures over-fitting.
- The fold-to-fold spread shows how reliable the estimate is, and the splitter can respect time, groups or space.
- For linear models PRESS comes from one fit through the leverage shortcut.

**4. Limitations / Potential issues:**

- Costs k refits (n refits for leave-one-out) and more for tuning.
- Noisy on small datasets; repeat the folds and report the spread.
- Leakage is easy and silent: preprocessing outside the pipeline, shuffled folds on time series, ungrouped folds on repeated customers.
- Slightly pessimistic (each fold trains on less data), and optimistic if the same folds are used to pick the best of many models; use nested cross-validation.
- Tells you how large the error is but not why; residual checks are still needed.

**5. Case Studies:**

| Field | Details |
|---|---|
| Case # / Title | Case 1 — Eight cassava batches and one oddly hot drying run |
| Industry / Domain | manufacturing (food processing, Ghana) |
| Business Problem | A cassava-flour mill has 8 batches linking drying temperature to moisture removed. One batch was dried at 110 degrees, far hotter than the others. The manager asks if a straight-line model can be trusted for setting dryer temperature. |
| ML Translation | Target = moisture removed (percentage points); simple linear regression on temperature; n = 8; one point is an outlier in x (a high-leverage point, one that pulls the fitted line strongly). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | PRESS (leave-one-out squared error) predicts every batch from a fit that excludes it, and for linear models the hat-matrix shortcut gives this from one fit. The hot batch has leverage 0.94, so without it the prediction is way off, which in-sample fit hides. |
| Why other metrics are NOT suitable here | In-sample R-squared (0.76) looks acceptable. RMSE on training data is blind to leverage. AIC would treat the one hot batch like any other and would not expose the extrapolation risk. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Believing the in-sample fit, the mill sets dryer temperatures from a line that is carried by one extreme batch, so flour moisture drifts out of spec and lots are rejected or sold at discount. |
| Small numeric example | n = 8; SST = 104.07; SSE = 25.15; in-sample R-squared = 0.758. Leverages = 0.20, 0.18, 0.16, 0.14, 0.13, 0.13, 0.13, 0.94 (the hot batch has 0.941). Leave-one-out residual = e/(1−h): hot batch = -1.21/(1−0.941) = -20.60. PRESS = 457.7 (checked by refitting 8 times); predicted R-squared = 1 − PRESS/SST = -3.40, worse than predicting the mean. |

| Field | Details |
|---|---|
| Case # / Title | Case 2 — Backtesting monthly order forecasts for a Cairo online marketplace |
| Industry / Domain | e-commerce (online marketplace, Egypt) |
| Business Problem | An online marketplace forecasts monthly order volume to book warehouse space. Orders grow every month. The team must estimate the real error of a straight-line trend model before signing a lease. |
| ML Translation | Target = monthly orders in thousands; 18 months of data; time-ordered; model refitted each time on the past and tested on the next 3 months (expanding-window cross-validation, never training on the future). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Cross-validation with a time-respecting split measures what the business will experience: forecasting forward from the past. Shuffled folds would let the model see future months and understate the error. |
| Why other metrics are NOT suitable here | In-sample RMSE flatters a model that fits the past. A single hold-out of 3 months is noisy; three expanding folds also show how error grows with horizon. AIC is not designed for forward-looking error on a growing series. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Leaky shuffled validation reports an error of 9 thousand orders when the real figure is near 15 and rising, so the marketplace books too little warehouse space for a growing business and misses deliveries. |
| Small numeric example | 18 months growing about 6% per month; straight-line trend model. Expanding-window folds (train 9, 12, 15 months; test the next 3): RMSE = 8.6, 13.1, 22.5; mean = 14.7, standard deviation across folds = 7.1. Shuffled 3-fold cross-validation (not allowed here) gives 9.4, 7.5, 11.1, mean 9.3, which is too optimistic. The honest error is rising: 8.6 to 22.5. |

| Field | Details |
|---|---|
| Case # / Title | Case 3 — Hospital length-of-stay models compared with patient-grouped folds |
| Industry / Domain | healthcare (hospital admissions, Saudi Arabia) |
| Business Problem | A hospital group compares a ridge model and a gradient-boosted model for predicting length of stay. Some patients appear in the data many times (repeat admissions). Bed planners need a fair estimate of how the models will do on new patients. |
| ML Translation | Target = length of stay in days; regression; models of different families (no shared likelihood); 3 folds in which all admissions of one patient stay in the same fold (grouped cross-validation). |
| Verdict | ✅ GOOD fit |
| Why this metric works / fails | Cross-validation works for any model family and any metric. Grouping the folds by patient prevents a patient's earlier admissions from helping to predict their later ones, so the score is honest about new patients. The spread across folds shows how stable the comparison is. |
| Why other metrics are NOT suitable here | AIC and BIC cannot compare a ridge model with boosted trees (no common likelihood or parameter count). In-sample RMSE favours the more flexible boosted model. A single split is noisy. |
| Better alternative (if BAD fit) | Not needed – this metric is the right choice |
| Business impact of choosing wrong | Ordinary folds put the same patient in training and test, hiding over-fit; the hospital would deploy a model whose real error is about 0.8 days higher and plan beds from it. |
| Small numeric example | Fold RMSE (days), grouped by patient: ridge = 2.31, 2.40, 2.28, mean 2.33, spread 0.06; boosted = 2.05, 2.30, 2.12, mean 2.16, spread 0.13. Boosted wins by 0.17 days, bigger than the spread. Ungrouped folds would show the boosted model at 1.40, 1.35, 1.45 (mean 1.40), a false improvement of 0.76 days. |

| Field | Details |
|---|---|
| Case # / Title | Case 4 — Five-fold cross-validation of a huge route-time deep network |
| Industry / Domain | logistics (delivery routing, Saudi Arabia) |
| Business Problem | A delivery platform trains a deep neural network on 60 million past trips to predict trip duration. One training run takes 18 hours on the cluster. A colleague insists on 5-fold cross-validation before launch. |
| ML Translation | Target = trip duration in minutes; deep regression; 60 million rows; time-ordered; the final model is judged on a recent period. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Cross-validation needs k refits. At 18 hours per fit that is 90 hours of cluster time for an estimate that a single large hold-out already provides to three decimals. With millions of test rows the noise in the score is tiny. |
| Why other metrics are NOT suitable here | AIC and BIC cannot be used for a neural network. In-sample RMSE is optimistic. Shuffled folds would also leak across time. |
| Better alternative (if BAD fit) | A single out-of-time validation set (for example the most recent 10% of trips) plus a final untouched test set. |
| Business impact of choosing wrong | Spending nearly 4 days of cluster time delays the launch and blocks other teams, while adding no useful accuracy to the estimate. |
| Small numeric example | 5 folds × 18 hours = 90 hours versus 1 × 18 = 18 hours. With a hold-out of 6,000,000 trips and error about 4.2 minutes, the standard error of the RMSE is about 4.2/sqrt(2×6,000,000) = 0.0012 minutes, already negligible. |

| Field | Details |
|---|---|
| Case # / Title | Case 5 — Reporting the best of six tuned configurations as the expected error |
| Industry / Domain | forestry (log-price forecasting, New Zealand) |
| Business Problem | A forestry exporter tunes six model configurations for log price using 5-fold cross-validation and reports the best cross-validated RMSE to its bank as the expected forecast error. |
| ML Translation | Target = export log price (NZD per tonne); regression; six configurations, all in truth equally good (true RMSE 45.0); selection by minimum cross-validated RMSE. |
| Verdict | ❌ BAD fit |
| Why this metric works / fails | Cross-validated error is an estimate with noise. Picking the minimum of several noisy estimates is optimistically biased, because the winner is partly the luckiest. The reported number is not the expected error on new data. |
| Why other metrics are NOT suitable here | Reporting in-sample RMSE is even more optimistic. A single hold-out can be noisy too. AIC cannot be used for all model types. |
| Better alternative (if BAD fit) | Nested cross-validation (an outer loop to estimate error, an inner loop to tune), or a final test set touched only once after the model is chosen. |
| Business impact of choosing wrong | The bank approves a facility on a forecast error of 40 when real error is 45, so margins are over-estimated and covenants are breached. |
| Small numeric example | Six configurations, all with true RMSE 45.0 but noisy cross-validated estimates = 43.0, 44.5, 50.0, 47.0, 40.1, 45.0. The winner reports 40.1. A fresh test set gives 44.5 for the chosen model, so the optimism is 4.4 (about 10%). |

**6. Quick decision rule:** Use PRESS or cross-validated error as the default way to compare models and tune settings, with a split that matches the data (time, groups, space); avoid it when refits are prohibitively expensive on huge data (use one large out-of-time hold-out), or when the same folds were already used to choose the model (use nested validation or a final test set).
