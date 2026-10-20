# Case Study 1 — Credit Risk Scorecard & Credit-Limit Engine (FinTech)

**Reference repos:** [R1 Abhinav19-isb/credit-risk-scorecard](https://github.com/Abhinav19-isb/credit-risk-scorecard) (AUC 0.783, KS 0.424 on same data — the benchmark to beat) · [R3 RishabhBansal2409/Predicting_Credit_Card_Approvals](https://github.com/RishabhBansal2409/Predicting_Credit_Card_Approvals)

### 1.1 Business problem
A card issuer (NBFC/bank) wants to (a) predict next-month default, (b) convert PD into a 300–900 bureau-style score with risk bands, (c) set approve/decline cut-off and credit-limit actions that maximise expected profit.

- **Primary KPI:** expected portfolio profit (₹) at the chosen cut-off.
- **Model KPIs:** ROC-AUC ≥ 0.78, KS ≥ 0.42, Gini ≥ 0.56, Brier ≤ 0.14, calibration slope 0.9–1.1.

### 1.2 Data
- UCI "Default of Credit Card Clients" — https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients — 30,000 rows, 23 features, ~22% default.
- Load: `from ucimlrepo import fetch_ucirepo; d = fetch_ucirepo(id=350)`. Cache to `data/raw/uci350.parquet`.
- Rename if columns come as X1..X23: `X1 LIMIT_BAL, X2 SEX, X3 EDUCATION, X4 MARRIAGE, X5 AGE, X6..X11 PAY_0,PAY_2..PAY_6, X12..X17 BILL_AMT1..6, X18..X23 PAY_AMT1..6`, target `Y → default`.
- Cleaning: map EDUCATION {0,5,6}→4 ("others"); MARRIAGE 0→3; amounts are NT$ — convert to ₹ via `config.fx_ntd_inr` (default 2.6) only for business outputs.

### 1.3 Folder & modules (`PKG=credit`)
```
src/credit/
  data.py        load_raw(), clean(df)->df, split(df)-> train/valid/test (60/20/20 stratified, seed)
  validate.py    schema checks (ranges, nulls, target in {0,1})
  features.py    utilisation_i = BILL_AMT_i/LIMIT_BAL; pay_ratio_i = PAY_AMT_i/BILL_AMT_{i+1};
                 max_delay, n_months_delayed, delay_trend (slope of PAY_* over 6m),
                 bill_growth, avg_util, util_volatility
  woe.py         monotonic binning (optbinning OptimalBinning), WOE transform, IV table
  models.py      fit_logit_scorecard(woe_X,y); fit_xgb(X,y) with Optuna 30 trials;
                 fit_lgbm; calibrate (isotonic on valid)
  scorecard.py   pd_to_score(p, base=600, odds=50, pdo=20, clip=(300,900)); points table per bin;
                 bands A..F with PD ranges
  evaluate.py    auc, gini, ks, brier, calibration curve, lift/decile table, PSI(train vs test)
  economics.py   EL = PD*LGD*EAD; profit(cutoff) = Σ approved [(1-PD)*margin*EAD - PD*LGD*EAD];
                 find_optimal_cutoff(); limit_action(score_band) -> {increase, hold, decrease, decline}
  fairness.py    approval-rate & AUC by SEX and AGE bucket; disparate-impact ratio
  explain.py     SHAP global summary + per-customer reason codes (top-4 adverse factors)
  monitor.py     PSI/CSI per feature, score drift alert if PSI>0.2
  train.py       orchestration -> models/*.joblib, outputs/metrics.json
app/streamlit_app.py
```

### 1.4 Method (step-by-step)
1. EDA: default rate by PAY_0, LIMIT_BAL decile, EDUCATION; correlation heat-map; save 6 figures.
2. Baseline: logistic regression on raw features (report AUC).
3. Scorecard: IV filter (keep IV ≥ 0.02), WOE logistic, points table → `outputs/scorecard_points.csv`.
4. Challenger: XGBoost + LightGBM on engineered features; isotonic calibration.
5. Champion selection on valid AUC; final numbers on test only once.
6. Economics: assumptions in config (`margin=0.18`, `LGD=0.65`, `EAD=LIMIT_BAL*avg_util`); sweep cutoff 0.05–0.6; sensitivity heatmap LGD × margin.
7. Fairness & explainability: reason codes like "High utilisation (82%)", "2 months delayed".
8. Monitoring: simulate drift by shifting test LIMIT_BAL −20% and show PSI alert.

### 1.5 App (Streamlit, 4 tabs)
- **Score a customer:** form → PD, score, band, top-4 reason codes, limit action.
- **Portfolio:** score distribution, band table, approval rate vs bad rate curve.
- **Cut-off simulator:** sliders for LGD/margin → profit curve, optimal cutoff.
- **Model health:** PSI table, calibration plot.

### 1.6 Milestones
- M1 data + validation + EDA · M2 scorecard · M3 ML challenger + SHAP · M4 economics + fairness · M5 app, memo, CI.

### 1.7 Acceptance criteria
- [ ] `make all` passes; `outputs/metrics.json` has auc/gini/ks/brier for logit, scorecard, xgb, lgbm.
- [ ] Champion test AUC ≥ 0.78 and KS ≥ 0.42.
- [ ] Scorecard points table sums reproduce score within ±1 point.
- [ ] `DECISION_MEMO.md` states optimal cutoff, approval %, bad rate %, ₹ profit vs approve-all.
- [ ] ≥ 10 tests incl. `test_pd_to_score_monotonic`, `test_woe_monotonic`, `test_no_target_leakage`.

### 1.8 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 1 "Credit Risk Scorecard & Credit-Limit Engine" exactly per the spec below.
PKG=credit. Use ucimlrepo id=350. Follow the module list, method steps, app tabs and acceptance criteria.
Work milestone by milestone (M1..M5); after each, run `make test`, update README results table, and summarise.
Benchmark to beat: Abhinav19-isb/credit-risk-scorecard (AUC 0.783, KS 0.424).
[PASTE SECTION 1.1–1.7 HERE]
```
