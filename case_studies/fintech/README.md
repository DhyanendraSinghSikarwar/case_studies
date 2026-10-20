# Indian Fintech Data Science — 30 Case Studies, Solved End to End

All 30 business problems from `indian_fintech_data_science_case_studies.md`, each solved as a professional data-science team would solve them. Every notebook gives a plain-English explanation for business leaders first, then rigorous statistics (assumptions, effect sizes, CIs, power, multiple-testing control, with the observations written after execution), a short ML section, and a ₹ business case. Cases are rated **★★★ Must-visit**, **★★ Good to have** or **★ Optional** (table below and inside the reference file).

**Where to start:** the three original notebooks (Cases 1, 11, 22 below) are the most detailed. Then work through the ★★★ cases (4, 6, 8, 12, 13, 19, 20), then ★★ and ★.

| # | Original notebooks | Reference case | Audience |
|---|---|---|---|
| 1 | `01_payment_routing_success_rate.ipynb` | Case Study 1 — Juspay: dynamic gateway routing | Head of Payments |
| 2 | `02_msme_credit_scoring.ipynb` | Case Study 11 — Lendingkart: cash-flow MSME underwriting | Chief Risk Officer |
| 3 | `03_nudge_campaign_ab_test.ipynb` | Case Study 22 — Axis Bank: omnichannel nudge engine | Head of Marketing |

The other 27 notebooks are named `csNN_*.ipynb` (NN = case number in the reference file) and listed in the status table below.

> ⚠️ **All outcome data is synthetic or semi-synthetic.** Generators are calibrated to the figures documented in the reference file (documented vs simulated parameters are separated in section 2 of every notebook). Public UCI datasets are used only where they fit: German Credit as a cross-check (Case 11) and Bank Marketing as the customer-attribute base (Case 22). No result here describes the real companies' data. See `decision.md` for every sourcing decision, synthetic parameter and corrected mistake (250 entries).

## How to run

```bash
# 1. Python 3.12 with the pinned libraries
pip install -r requirements.txt

# 2. Register a kernel for this environment (the notebooks use the kernel name "fintech-cases")
python -m ipykernel install --user --name fintech-cases --display-name "Python 3.12 (fintech-cases)"

# 3. Execute any notebook top to bottom (regenerates its data in data/)
jupyter nbconvert --to notebook --execute --inplace cs02_card_decline_funnel.ipynb
# If `jupyter` is not on PATH, use: python -m nbconvert --to notebook --execute --inplace <file>
# If the kernel is slow to start ("Kernel didn't respond in 60 seconds"), add:
#   --ExecutePreprocessor.startup_timeout=600
```

- Random seed = 42 everywhere (independent child streams via `SeedSequence(42)` where several random processes interact; see `decision.md` D-0-05).
- Each notebook writes its generator to `data/generate_*.py` and regenerates its data in `data/<case>/`, so the notebook and the script cannot drift apart.
- Run time on a laptop is roughly 2–10 minutes per notebook; the slowest are Case 23 (character n-gram models, ≈ 25 minutes) and Case 26 (bootstrap on 300,000 visitors, ≈ 15 minutes). Case 22 needs `data/public/bank-full.csv`, which is included (UCI, CC BY 4.0).
- `_build/nbtool.py` is the authoring tool used to build and check the notebooks (source → notebook, execute, dump outputs, fill the written observations, verify, update this table). It is not needed to run the notebooks. `_build/src/*.src` hold the notebook sources and `_build/fills/` the written observations and decision-log entries.

<!-- CASE-INDEX-START -->
## All 30 case studies — priority and notebook status

Stars (also added to `indian_fintech_data_science_case_studies.md`): **★★★ Must-visit** · **★★ Good to have** · **★ Optional**. Every notebook follows the same 0–12 structure (executive summary → problem → documented vs simulated → hypotheses → data → DQ → EDA → statistics → ML → ₹ translation → recommendation → risks → appendix), uses seed 42, and writes its data to `data/csXX/`.

| Case | Priority | Notebook | Status | Core technique |
|---|---|---|---|---|
| 1 | ★★★ Must-visit | `01_payment_routing_success_rate.ipynb` | ✅ built & verified | Binomial SR testing, multiple testing, bandits and ₹ GMV: the core payments-DS toolkit |
| 2 | ★★ Good to have | `cs02_card_decline_funnel.ipynb` | ✅ built & verified | Funnel/stage decomposition: simple but used weekly by every payments team |
| 3 | ★★ Good to have | `cs03_foundation_model_evaluation.ipynb` | ✅ built & verified | Calibration vs ranking, fixed-alert-budget and out-of-time evaluation; the foundation model itself is hard to reproduce |
| 4 | ★★★ Must-visit | `cs04_adaptive_anomaly_alerts.ipynb` | ✅ built & verified | Seasonality-aware anomaly detection and alert-fatigue economics: every ops/risk team needs it |
| 5 | ★ Optional | `cs05_merchant_review_automation.ipynb` | ✅ built & verified | LLM-agent automation; the data-science part is measuring agreement with analysts |
| 6 | ★★★ Must-visit | `cs06_upi_p2p_fraud.ipynb` | ✅ built & verified | Label engineering + real-time imbalanced fraud classification + reinstatement-rate KPI |
| 7 | ★★ Good to have | `cs07_velocity_graph_fraud_screening.ipynb` | ✅ built & verified | Velocity and graph features, rules + anomaly scores per business line |
| 8 | ★★★ Must-visit | `cs08_mule_account_detection.ipynb` | ✅ built & verified | Textbook imbalanced classification: class weights, PR curves, thresholds → action tiers |
| 9 | ★★ Good to have | `cs09_mule_typology_alert_precision.ipynb` | ✅ built & verified | Typology-first modelling and alert precision as the headline metric |
| 10 | ★★ Good to have | `cs10_bnpl_fraud_rings_graph.ipynb` | ✅ built & verified | Graph community detection for fraud rings and the cost to good users |
| 11 | ★★★ Must-visit | `02_msme_credit_scoring.ipynb` | ✅ built & verified | Full credit-scorecard lifecycle: WoE/IV, logistic, KS/Gini, calibration, PSI, cut-offs |
| 12 | ★★★ Must-visit | `cs12_collections_bucket_scorecards.ipynb` | ✅ built & verified | Collections as resource allocation: bucket-wise PD and channel policy |
| 13 | ★★★ Must-visit | `cs13_alternate_data_credit_scoring.ipynb` | ✅ built & verified | Comparing data sources by AUC (DeLong) and reject inference for thin-file lending |
| 14 | ★★ Good to have | `cs14_segmented_underwriting.ipynb` | ✅ built & verified | Segmented models vs one global model; top/bottom bad-rate ratio |
| 15 | ★★ Good to have | `cs15_bnpl_limit_assignment.ipynb` | ✅ built & verified | Behavioural score → pre-approval and credit-limit assignment |
| 16 | ★★ Good to have | `cs16_merchant_qr_lending.ipynb` | ✅ built & verified | Merchant cash-flow capacity modelling + fuzzy KYC name matching |
| 17 | ★★ Good to have | `cs17_preapproved_pl_noninferiority.ipynb` | ✅ built & verified | Non-inferiority testing: 'same delinquency, 10 seconds instead of days' |
| 18 | ★★ Good to have | `cs18_custom_score_vs_bureau.ipynb` | ✅ built & verified | Custom score vs bureau: 'better on what metric?' (Gini, KS, bad rate at fixed approval) |
| 19 | ★★★ Must-visit | `cs19_collections_propensity_uplift.ipynb` | ✅ built & verified | Propensity vs uplift for collections: call the customers a call actually changes |
| 20 | ★★★ Must-visit | `cs20_propensity_ltv_ranking.ipynb` | ✅ built & verified | Expected-value ranking (propensity × LTV) validated by A/B tests vs random and rules |
| 21 | ★★ Good to have | `cs21_bayesian_trend_personalisation.ipynb` | ✅ built & verified | Simple Bayesian personalisation; interpretable baseline for recommenders |
| 22 | ★★★ Must-visit | `03_nudge_campaign_ab_test.ipynb` | ✅ built & verified | Causal campaign measurement: SRM, CUPED, power, heterogeneity, uplift, ROI |
| 23 | ★ Optional | `cs23_transaction_purpose_classification.ipynb` | ✅ built & verified | Transaction categorisation (text classification); a foundation for other models |
| 24 | ★ Optional | `cs24_motor_inspection_cv_validation.ipynb` | ✅ built & verified | Computer vision; the DS part is validating 'fit for purpose' accuracy and triage |
| 25 | ★ Optional | `cs25_claims_copilot_evaluation.ipynb` | ✅ built & verified | OCR + LLM decision support; the DS part is measuring productivity and agreement |
| 26 | ★★ Good to have | `cs26_chat_conversion_causal.ipynb` | ✅ built & verified | Observational vs causal channel comparison (self-selection, propensity matching) |
| 27 | ★ Optional | `cs27_call_analytics_dialler.ipynb` | ✅ built & verified | Speech analytics; the DS part is intent-frequency analysis and dialler efficiency |
| 28 | ★ Optional | `cs28_speed_to_lead.ipynb` | ✅ built & verified | Speed-to-lead: how contact delay erodes conversion; capacity-constrained routing |
| 29 | ★★ Good to have | `cs29_penny_stock_nudge_causal.ipynb` | ✅ built & verified | Pre/post vs difference-in-differences and interrupted time series |
| 30 | ★ Optional | `cs30_support_automation_resolution.ipynb` | ✅ built & verified | Intent classification + resolution rate together with CSAT |
<!-- CASE-INDEX-END -->

## Repository layout

```text
01_payment_routing_success_rate.ipynb   Case 1 (Juspay)
02_msme_credit_scoring.ipynb            Case 2 (Lendingkart)
03_nudge_campaign_ab_test.ipynb         Case 3 (Axis Bank)
decision.md                             Decision log for all three cases (+ summary table)
requirements.txt                        Pinned library versions
data/
  generate_case_1.py                    Synthetic generator: 30 days of gateway-routed payments
  generate_case_2.py                    Synthetic generator: MSME applications with a COVID-like OOT shock
  generate_case_3.py                    Semi-synthetic generator: UCI customers + randomised nudge experiment
  case1_transactions_raw.csv.gz         ~4.2 lakh payments (raw, with injected data-quality defects)
  case1_transactions_clean.csv.gz       cleaned
  case1_data_dictionary.csv
  case2_msme_applications_raw.csv       51,000 applications (raw)
  case2_msme_applications_clean.csv     cleaned (50,000 businesses)
  case2_data_dictionary.csv
  case3_nudge_experiment.csv            200,000 customers (raw, incl. SRM flag)
  case3_nudge_experiment_clean.csv      cleaned
  case3_data_dictionary.csv
  public/                               UCI Statlog German Credit + UCI Bank Marketing (CC BY 4.0)
```

## Business summary per case

### Case 1 — Payment routing (Juspay)

- **Problem:** fixed rules route 4.2 lakh payments a month across 4 gateways; 17% fail. Is any gateway truly best, and does dynamic routing beat the rules?
- **Finding:** no single best gateway. The top two are statistically tied (84.0% vs 83.9%, p = 0.66), and the winner depends on the bank (gateway × bank interaction p ≈ 10⁻¹¹⁸). A Thompson-Sampling router lifts SR from **82.7% to 83.7% (+0.91 pp, 95% CI +0.87 to +0.96)**, a 1.1% relative gain in line with Juspay's documented "up to 1.15%", worth **≈ ₹41 lakh net GMV a month** (range ₹16–60 lakh). A p-chart detects the outage within 15 minutes.
- **Recommendation:** apply 4 Holm-confirmed segment rules now, deploy the outage alarm, then run a pre-registered 14-day 50/50 A/B test (≈ 89k payments per arm, no peeking) before rolling out with a permanent holdout.

### Case 2 — MSME credit scoring (Lendingkart)

- **Problem:** score MSMEs from bank-statement, GST and bureau data; check stability after a COVID-like shock; set cut-offs and A–F buckets.
- **Finding:** cheque bounces (OR 1.50 per bounce), credit declines, low minimum balance, shrinking inflows, bureau score, vintage and Tier 3 drive default. The logistic scorecard reaches **test KS 39 / Gini 0.52**, holds in the shock (OOT KS 38.5), has clean monotonic buckets (1.3% → 27.5% bad rate), and approves **68% more** applicants than a manual policy at the same bad rate (documented: ~50%). In the shock, the score PSI is 0.15 and hospitality and transport default 26–60% above prediction.
- **Recommendation:** logistic champion (it beats untuned XGBoost by 0.026 AUC, significant), cut-off **575** (≈ ₹52 crore expected profit per 10k applications), Zero-Touch for A–B, and a shock playbook: cut-off 600 + industry overlay, triggered when PSI > 0.10.

### Case 3 — Nudge campaign A/B test (Axis Bank)

- **Problem:** prove that Diwali nudges (SMS / Email / WhatsApp / Push) *caused* BillPay and personal-loan uplift, size it in ₹, and decide where to spend.
- **Finding:** against a randomised 20% hold-out, BillPay registration rose **1.53× (95% CI 1.45–1.61)** and PL bookings **+10.3% (CI +3% to +18%)**, both matching Axis's documented 1.5× and +10%. Loan size is unchanged. Revenue rose **+₹119 per customer (CI ₹26–213), ≈ ₹1.9 crore vs ₹7.9 lakh of cost (ROI ≈ 23×, worst ≈ 3×)**. Push (app users only) and WhatsApp lead on BillPay. An SRM check caught a tracking bug that overstated Push. The 20% control gave exactly 80% power for the PL effect, so it was enough but with no margin.
- **Recommendation:** keep funding; Push for app-active customers, WhatsApp for the rest; target the top-uplift customers (the top 40% delivers 57% of the effect); keep a permanent hold-out with a daily SRM alert; validate the reallocation in the next randomised wave.

## Deviations from the brief (summary)

See the final report and `decision.md` for full reasoning.

- `jupyter nbconvert` is run as `python -m nbconvert` (identical program; Scripts folder not on PATH) with a dedicated `fintech-cases` kernel, because the machine's default kernel pointed at another project's virtualenv.
- Data is stored as CSV (`.csv.gz` for the large Case 1 file), not Parquet, to avoid adding `pyarrow`.
- `shap`, `pingouin` and `scikit-posthocs` are not used: SHAP comes from XGBoost's native `pred_contribs`, and Dunn's test is implemented directly.
- Case 2 omits the "balance-transfer triggers" feature family (too little documented detail to simulate credibly).
