

### R1 Experimentation / switchback
(a) Calibrate to: Cabify example interval 53 min (alternatives 58, 112, 29); Flipkart 2012 routed 10% of traffic to a new design; sample unit equals the interval, so n is the number of intervals not trips; washout drops early-window data (Cabify). No lift figures are public.
(b) Expected techniques: power/MDE and sample size, SRM check, CUPED variance reduction, guardrail metrics, multiple testing correction, sequential testing, switchback with cluster-robust errors, carryover/washout.
(c) Very common.

### R2 LTV / segmentation
(a) Swiggy: 350+ pre-first-order features; MLP with 3 shared hidden layers; parameters 363,000 to 135,000; Spearman above 0.75; diagonal coverage 70% to 80%; many users have zero orders in 30 days (heavy zero inflation, skewed tail).
(b) Expected: RFM scoring, k-means on RFM, BG/NBD plus Gamma-Gamma, zero-inflated/hurdle regression, gradient boosting on 90-day value, Gini/decile lift, calibration.
(c) Very common.

### R3 Membership
(a) Zomato Gold relaunch Jan 2023 at Rs 149 for 3 months; 9 lakh members in a month (company claim); Flipkart Plus Silver 15 and Gold 25 transactions in 365 days; SuperCoin 1 or 2 per Rs 100, caps 50 per month and 15 per order. Unverified snippet figures (Gold about 30% to 40% of food GOV, about 60% frequency uplift) should be labelled as such if used.
(b) Expected: selection-bias handling (PSM, DiD, synthetic control), holdout/ramp, survival/churn modelling, contribution-margin economics, breakeven analysis.
(c) Common.

### R4 Coupons / budget allocation
(a) Meituan: 200+ features; AUC 0.891; PCOC 0.971 to 0.982; City B price x CVR 2.15 vs 2.09 (+2.8%); PID keeps price within about 1% of target (vs about 3% without); 50 ms decision latency.
(b) Expected: uplift modelling (T-learner, X-learner, causal forest), calibration, constrained optimisation / Lagrangian knapsack, cannibalisation analysis, A/B with budget guardrails.
(c) Very common.

### R5 Push / CRM
(a) Meesho: roughly 20 to 30 notifications per day; uninstalls unaffected; retention "stayed strong"; content, volume and time of day personalised. No percentages public.
(b) Expected: send-time optimisation (per-user open-hour histograms, contextual bandits), uplift on notification, frequency capping and fatigue/unsubscribe survival analysis, long-run holdouts.
(c) Very common.

### R6 Attribution / MMM
(a) Honasa: MMM plus geo-lift; no numbers public. Use only qualitative framing; simulation parameters (adstock, saturation) must be assumed and labelled as assumed.
(b) Expected: Bayesian MMM with adstock and Hill saturation, geo-experiment/difference-in-differences or synthetic control for incrementality, calibration of MMM using lift tests, MTA vs MMM trade-offs, last-click bias.
(c) Common.
