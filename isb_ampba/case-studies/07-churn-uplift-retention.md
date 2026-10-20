# Case Study 7 — Churn Prediction + Uplift-based Retention (E-commerce / Subscription)

**Reference repo:** [R9 akash-sood97/partner-retention-system](https://github.com/akash-sood97/partner-retention-system) — "ISB AMPBA"; churn AUC ≈ 0.75, cost-optimal thresholds, uplift targeting from randomised pilot captures ₹1.17M of ₹1.33M ceiling while risk-only targeting loses ₹33k.

### 7.1 Business problem
Retention budget is wasted on customers who would stay anyway or who cannot be saved. Predict churn **and** who responds to an offer; target by expected incremental profit.

- **KPIs:** churn AUC ≥ 0.75; Qini coefficient > 0; incremental profit of uplift policy > risk-only policy > random.

### 7.2 Data
- Base: UCI Online Retail II (id=502). Churn label: active customer (≥ 2 orders in previous 6 months) with **no purchase in next 90 days** after snapshot date. Build 3 monthly snapshots (2011-03-01, 04-01, 05-01) for training, 2011-08-01 for test.
- Treatment simulation (`src/churnx/pilot.py`): randomised 50/50 offer to test cohort; true heterogeneous effect function of features (e.g., price-sensitive mid-frequency customers respond; Champions don't; Hibernating rarely) + noise; seed-controlled. Documented as synthetic.

### 7.3 Modules (`PKG=churnx`)
```
src/churnx/
  snapshot.py    build_features(asof): RFM, inter-purchase time mean/std, trend in spend (last 3m vs prior 3m),
                 n_returns, category breadth, country, days since first purchase; label(asof, horizon=90)
  models.py      logit, RF, XGBoost, LightGBM; calibration; SHAP
  threshold.py   cost-optimal threshold: offer_cost, CLV_saved, success prob -> maximise expected profit
  pilot.py       simulated RCT with heterogeneous treatment effects; ground-truth tau stored
  uplift.py      T-learner, S-learner, X-learner (causalml or scikit-uplift), class-transformation;
                 Qini/uplift curves; AUUC
  policy.py      6 policies: random, all, risk-top-k, CLV-top-k, uplift-top-k, profit-optimal (tau*CLV - cost > 0);
                 compare vs perfect-hindsight oracle
  survival.py    optional: Kaplan-Meier & Cox PH (lifelines) for time-to-churn
app/streamlit_app.py
```

### 7.4 Method
1. Snapshots, label rate per snapshot; leakage check (features strictly before asof).
2. Train on stacked training snapshots, test on later snapshot (temporal validation).
3. Cost-optimal threshold & lift chart.
4. Pilot + uplift models; Qini curves; recovered tau correlation vs ground truth.
5. Policy comparison table in ₹ and as % of oracle.

### 7.5 Acceptance criteria
- [ ] Temporal split; `test_features_before_asof`.
- [ ] Policy table with oracle ceiling; uplift policy ≥ 70% of oracle.
- [ ] Memo: why "target highest-risk" can lose money.

### 7.6 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 7 "Churn Prediction + Uplift Retention" per spec. PKG=churnx. Data UCI id=502 + simulated RCT.
Follow the policy-comparison framing of github.com/akash-sood97/partner-retention-system.
Milestones: M1 snapshots+labels, M2 churn models+threshold, M3 pilot+uplift, M4 policy comparison, M5 app/memo/CI.
[PASTE SECTION 7.1–7.5 HERE]
```
