# ISB AMPBA — Top 10 Case Studies: Build Plan for Claude Code

> **Purpose:** A build specification that Claude Code can execute project-by-project to produce 10 portfolio-grade, AMPBA-style analytics/AI projects in FinTech, E-commerce and GenAI.
> **Prepared:** 13 Oct 2026 · **Basis:** ISB AMPBA curriculum + public GitHub repos of AMPBA students/alumni (links verified by fetching each page).

---

## 0. How to use this file with Claude Code

1. Create an empty folder per project (e.g. `~/ampba/01-credit-risk-scorecard`).
2. Copy **Section 2 (Global Standards)** into that folder as `CLAUDE.md`.
3. Paste the project's **"Claude Code kickoff prompt"** (the code block at the end of each case study) into Claude Code.
4. Let it build milestone-by-milestone (M1 → M5). After each milestone run `make test` and `make run`.
5. Check the **Acceptance criteria** checklist before moving on.

Recommended order (easy → hard): 1 → 5 → 6 → 7 → 2 → 8 → 4 → 9 → 3 → 10.

---

## 1. How ISB AMPBA structures projects (the "systematic plan")

### 1.1 Curriculum map (source: isb.edu AMPBA curriculum page)

| Stage | Courses | Skill used in these case studies |
|---|---|---|
| Bootcamp | Python, R, SQL, Linear Algebra | Data loading, SQL/DuckDB |
| Foundation Term | Probability, Descriptive Stats (R), Data Collection & Pre-processing, Data Visualization | EDA, cleaning, charts |
| Core | Statistical Analysis 1, Big Data Management, Optimization, Data Engineering | Pipelines, LP/MIP |
| Advanced | Supervised ML 1–2, Unsupervised ML 1–2, Stat Analysis 2, Adv. Optimization & Simulation, Deep Learning, Forecasting, NLP, Network & Graph Analytics, Contemporary Tech (GenAI) | Models, forecasting, LLM agents |
| Application | Digital & Social Media, Supply Chain & Retail, Marketing & Customer, Applications of AI, Pricing & Demand, Financial Analytics | Domain framing |
| Experiential | **Foundation Project (FP)** + **Industry-sponsored Capstone** | Every case below |

### 1.2 Capstone mechanics (source: isb.edu AMPBA Applied Learning page)

- Teams of 3–4; sponsor gives problem statement + sample data.
- Teams **bid** with approach & methodology.
- ~450–500 person-hours over ~3 months; faculty mentor + client mentor.
- **Two formal reviews** (mid-review, final) by client, faculty and programme office.
- Deliverable: final report on the developed model; optional pilot on live data, then refinement.
- Past capstone themes: branch-location econometrics (banking), security price prediction (finance), insurance fraud, telecom fraud on big data, customer profiling & market basket, product auto-classification, freight optimisation, drug-interaction detection.

### 1.3 Lifecycle every project below follows (CRISP-ML(Q), as used in AMPBA repos)

| Phase | Output artifact | Review gate |
|---|---|---|
| P1 Business understanding | `docs/PROBLEM_STATEMENT.md` (objective, KPI, constraints, success criteria) | Bid / proposal |
| P2 Data understanding | `notebooks/01_eda.ipynb`, `reports/data_quality.md` | — |
| P3 Data preparation | `src/data.py`, `src/features.py`, validated parquet in `data/processed/` | — |
| P4 Modelling | `src/models.py`, model registry in `models/` | **Mid-review** |
| P5 Evaluation | `outputs/metrics.json`, `figures/`, business-metric translation | — |
| P6 Deployment | Streamlit app / FastAPI, Dockerfile | **Final review** |
| P7 Monitoring & memo | `src/monitor.py` (drift), `docs/DECISION_MEMO.md` (1 page, ₹ impact) | Sponsor sign-off |

Pattern seen across the strongest AMPBA repos (Akash Sood, Abhinav, Siddharth Kolli): **every number in the memo is reproducible by one command**, results stored in `outputs/summary.json`, assumptions swept rather than fixed, and limitations stated.

---

## 2. Global standards (save as `CLAUDE.md` in every project)

```markdown
# CLAUDE.md — AMPBA project conventions

## Stack
- Python 3.11; pandas, numpy, scikit-learn, xgboost, lightgbm, shap, statsmodels,
  scipy, pulp (HiGHS), matplotlib, plotly, streamlit, fastapi, pydantic, pytest, ruff.
- LLM work: langchain-core / langgraph; provider via env var LLM_PROVIDER in {groq, openai, mock}.
  Default = mock (deterministic, offline) so everything runs without API keys.
- Data access: ucimlrepo, yfinance, datasets (HuggingFace). Cache raw downloads in data/raw/.

## Repo layout (mandatory)
.
├── CLAUDE.md
├── README.md                # problem, data, method, results table, how to run, limits
├── Makefile                 # setup, data, train, evaluate, app, test, all
├── requirements.txt         # pinned versions
├── Dockerfile
├── .github/workflows/ci.yml # ruff + pytest on push
├── config/config.yaml       # all paths, seeds, hyper-params, business assumptions
├── data/{raw,interim,processed}/   (gitignored except small samples)
├── notebooks/               # 01_eda, 02_features, 03_models (thin; call src/)
├── src/<package>/           # all logic; notebooks import from here
├── analysis/run_analysis.py # regenerates every figure + outputs/summary.json
├── outputs/                 # csv, summary.json, metrics.json
├── figures/                 # png charts referenced by README/memo
├── models/                  # serialized models (joblib)
├── app/                     # streamlit_app.py (and api.py if FastAPI)
├── tests/                   # pytest; unit + one end-to-end smoke test
└── docs/                    # PROBLEM_STATEMENT.md, DECISION_MEMO.md, MODEL_CARD.md

## Rules
1. Seed everything (config.seed = 42). Results must be reproducible.
2. No logic in notebooks; notebooks only call src functions.
3. Every function: type hints + docstring. Use logging, not print.
4. Validate data with explicit asserts/pandera schema in src/<pkg>/validate.py.
5. Time-based or group-based splits where leakage is possible; never random-split time series.
6. Always report a naive baseline next to the model.
7. Translate model metrics into a business metric (₹ / % / hours saved) in DECISION_MEMO.md.
8. Business assumptions live in config.yaml and are swept in a sensitivity analysis.
9. `make all` must run end-to-end on a laptop in < 15 minutes (use sampling flags if needed).
10. Tests: >= 10 unit tests; tests must run offline (use fixtures/ synthetic data, LLM mock).
11. Write MODEL_CARD.md: intended use, data, metrics, fairness check, limitations.
12. After each milestone: run `make test`, update README results table, commit.
```

### 2.1 Standard Makefile (Claude Code should create this in each project)

```makefile
PY=python
setup:      ; pip install -r requirements.txt
data:       ; $(PY) -m src.$(PKG).data
train:      ; $(PY) -m src.$(PKG).train
evaluate:   ; $(PY) analysis/run_analysis.py
app:        ; streamlit run app/streamlit_app.py
test:       ; pytest -q
lint:       ; ruff check .
all: data train evaluate test
```

### 2.2 Standard LLM wrapper (used in projects 2, 3, 9, 10)

```python
# src/<pkg>/llm.py
class LLM:
    """provider in {'mock','groq','openai'} from env LLM_PROVIDER (default 'mock').
    .complete(system: str, user: str, schema: type[BaseModel] | None) -> str | BaseModel
    mock returns deterministic templated output built from the input (for tests/offline).
    groq: model from env GROQ_MODEL (default 'llama-3.3-70b-versatile'); openai: OPENAI_MODEL (default 'gpt-4o-mini').
    Retries 3x with exponential backoff; logs token usage to outputs/llm_usage.csv."""
```

---

## 3. Alumni / student reference repositories (all fetched & verified)

| # | Repo | Owner (AMPBA evidence) | Domain | What to borrow |
|---|---|---|---|---|
| R1 | [credit-risk-scorecard](https://github.com/Abhinav19-isb/credit-risk-scorecard) | Abhinav Srivastava — README: "Analytics & Credit Risk \| ISB AMPBA" | FinTech | Scorecard, SHAP, Streamlit, CI layout |
| R2 | [ISB_AMPBA_Capstone…Deloitte Anomaly Detection using GenAI](https://github.com/adarshb3/ISB_AMPBA_Capstone-Project_Deloitte--Anomaly-Detection-in-Business-Processes-using-Generative-AI) | Adarsh Balan — "ISB Capstone Project with Deloitte" | Fraud / Audit | KNN anomaly + KRIs + LLM agent, Mage ETL, Postgres |
| R3 | [Predicting_Credit_Card_Approvals](https://github.com/RishabhBansal2409/Predicting_Credit_Card_Approvals) | Rishabh Bansal — bio: AMPBA, ISB | FinTech | Baseline logistic regression |
| R4 | [CR (Credit Underwriting System)](https://github.com/anmolisb/CR) | anmolisb (AMPBA 2026S capstone owner) | FinTech GenAI | agents/ orchestrator/ prompts/ layout |
| R5 | [Stock2026 (Stock-Algo)](https://github.com/anmolisb/Stock2026) | anmolisb | Capital markets | NSE screener, regime filter, backtest |
| R6 | [Escalant_SurveyProgramming](https://github.com/anmolisb/Escalant_SurveyProgramming) | "Capstone Project \|\| ISB AMPBA 2026S" (sponsor Escalent) | GenAI agents | LangGraph multi-agent, eval harness, milestones |
| R7 | [promotion-cannibalisation-engine](https://github.com/akash-sood97/promotion-cannibalisation-engine) | Akash Sood — "ISB AMPBA" | E-commerce | Choice model, cannibalisation, decision memo |
| R8 | [two-sided-pricing-engine](https://github.com/akash-sood97/two-sided-pricing-engine) | Akash Sood — "ISB AMPBA" | Marketplace pricing | Two-sided demand, robustness draws |
| R9 | [partner-retention-system](https://github.com/akash-sood97/partner-retention-system) | Akash Sood — "ISB AMPBA" | Churn / uplift | Cost-optimal threshold, uplift targeting |
| R10 | [supply-serviceability-capstone](https://github.com/akash-sood97/supply-serviceability-capstone) | Akash Sood — "ISB AMPBA" | Quick-commerce ops | Forecast + MIP lever mix |
| R11 | [distribution-network-design](https://github.com/akash-sood97/distribution-network-design) | "Team project, ISB AMPBA, 2026" | Supply chain | PuLP/HiGHS vs heuristic, Flask |
| R12 | [AMPBA-Capstone-PharmaTrace](https://github.com/Siddharth0711/AMPBA-Capstone-PharmaTrace) | "ISB AMPBA Capstone \| Sponsor: Innodatatics" | Healthcare supply chain | ABC-FSN, expiry risk RF, LP |
| R13 | [Foundation-Project-2](https://github.com/Siddharth0711/Foundation-Project-2) | Siddharth Kolli | Forecasting | Holt-Winters/SARIMAX/Prophet/LSTM, P5-P95 bands |
| R14 | [Electricity-price-prediction](https://github.com/Siddharth0711/Electricity-price-prediction) | Siddharth Kolli | Energy trading | CRISP-ML(Q), FastAPI, Render |
| R15 | [speech-emotion-recognition](https://github.com/akash-sood97/speech-emotion-recognition) | "Team project, ISB AMPBA 2026" | Deep learning | Speaker-held-out eval |
| R16 | [Sentiment_Analysis_of_Customer_Reviews](https://github.com/RishabhBansal2409/Sentiment_Analysis_of_Customer_Reviews) | Rishabh Bansal | NLP / E-com | Scraping + sentiment + Shiny |
| R17 | [Recommendation_Engine](https://github.com/RishabhBansal2409/Recommendation_Engine) | Rishabh Bansal | E-commerce | User/item CF (surprise) |
| R18 | [Natural_Language_Processing__Chatbot](https://github.com/RishabhBansal2409/Natural_Language_Processing__Chatbot) | Rishabh Bansal | NLP | Intent classification bot |
| R19 | [ISB_AMPBA (course archive)](https://github.com/AkshayEswaran/ISB_AMPBA) | Akshay Eswaran | All courses | Term-wise course folder structure |

> Note: Few AMPBA capstones are public (most sponsor data is confidential). LinkedIn profiles could not be scraped; GitHub profile bios/READMEs were used as evidence. Profiles worth browsing manually (logged-in): `github.com/akash-sood97`, `github.com/Siddharth0711`, `github.com/anmolisb`, `github.com/adarshb3`, `github.com/RishabhBansal2409`.

---

## 4. The Top 10 case studies — overview

| # | Case study | Domain | AMPBA courses | Reference repos | Dataset | Difficulty |
|---|---|---|---|---|---|---|
| 1 | Credit Risk Scorecard & Limit Engine | FinTech lending | Supervised ML, Financial Analytics | R1, R3 | UCI #350 (30k cards) | ★★ |
| 2 | Expense (T&E) Fraud Detection + GenAI Audit Copilot | FinTech / Audit (Deloitte-style) | Unsupervised ML, Data Eng., GenAI | R2 | Synthetic generator w/ labelled injected fraud | ★★★ |
| 3 | Agentic Credit Underwriting (MSME/Retail loans) | FinTech GenAI | Contemporary Tech, Supervised ML | R4, R6 | UCI #144 German Credit + synthetic docs | ★★★★ |
| 4 | NSE Factor Screener & Regime-aware Backtester | Capital markets | Financial Analytics, Forecasting | R5 | yfinance NSE prices | ★★★ |
| 5 | Promotion Cannibalisation Engine | E-commerce pricing | Pricing & Demand, Retail | R7 | UCI #502 Online Retail II | ★★★ |
| 6 | RFM Segmentation, Market Basket & Recommender | E-commerce marketing | Unsupervised ML, Marketing | R17, ISB "Customer Profiling & MBA" | UCI #502 | ★★ |
| 7 | Churn Prediction + Uplift-based Retention | E-commerce / Subscription | Supervised ML, Marketing | R9 | UCI #502 (derived churn) | ★★★ |
| 8 | Two-sided Marketplace Dynamic Pricing | Quick-commerce / Gig | Pricing, Optimization | R8 | Synthetic, calibrated on UCI #502 | ★★★★ |
| 9 | Dark-store Demand Forecasting & Serviceability Optimiser | Quick-commerce supply chain | Forecasting, Optimization | R10, R11, R13 | Synthetic hub×SKU×week generator | ★★★★ |
| 10 | Review Intelligence: Aspect Sentiment + RAG Copilot | E-commerce GenAI / NLP | NLP, Applications of AI | R16, R18, R6 | HF Amazon-Reviews-2023 | ★★★★ |

---
## Case Study 1 — Credit Risk Scorecard & Credit-Limit Engine (FinTech)

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

---

## Case Study 2 — Expense (T&E) Fraud Detection + GenAI Audit Copilot (FinTech / Audit)

**Reference repo:** [R2 adarshb3 — ISB AMPBA Capstone with Deloitte: Anomaly Detection in Business Processes using Generative AI](https://github.com/adarshb3/ISB_AMPBA_Capstone-Project_Deloitte--Anomaly-Detection-in-Business-Processes-using-Generative-AI) (KNN anomaly + rule KRIs + LangChain agent + Mage ETL + Postgres + Tableau). This rebuild adds a **labelled synthetic generator** so precision/recall can actually be measured (the original reports none).

### 2.1 Business problem
Internal audit reviews < 5% of travel & expense (T&E) claims manually. Build a system that ranks every claim by fraud risk, explains why, and produces an auditor-ready action plan.

- **KPIs:** Precision@top-5% ≥ 0.60, Recall of fraud ₹ value in top-10% ≥ 0.70, auditor hours saved.

### 2.2 Data — synthetic generator (`src/tne/generate.py`)
Generate 12 months, 1,500 employees, ~120k claim lines, seed-controlled:
- Tables: `employees(emp_id, grade, dept, cost_center, manager_id, city, join_date)`, `claims(claim_id, emp_id, date, category{airfare,hotel,meals,taxi,mileage,misc}, merchant, city, amount_inr, receipt_flag, submitted_at, approved_by, approved_at, description)`, `policy(grade, category, daily_limit_inr)`.
- Inject 8 fraud schemes at ~3% of claims with label `fraud_type`:
  1. Duplicate claim (same amount/merchant ±2 days) 2. Split transactions just under limit 3. Weekend/holiday meals without travel 4. Amount just below receipt threshold (₹499 at ₹500) 5. Personal merchant categories (jewellery, liquor) 6. Mileage inflation vs city distance 7. Self/peer approval collusion (approver = manager ring) 8. Round-number amounts at high frequency.
- Write to DuckDB `data/tne.duckdb` (Postgres optional via docker-compose).

### 2.3 Modules (`PKG=tne`)
```
src/tne/
  generate.py   synthetic data + ground-truth labels
  etl.py        DuckDB SQL: clean, join policy, derive claim-level & employee-month features
  kri.py        12 rule-based Key Risk Indicators (one per scheme + over-limit, late submission,
                approval < 5 min); each returns flag + severity 1-5 + evidence string
  features.py   amount z-score within (grade,category,city); Benford first-digit deviation per emp;
                claims/day; weekend ratio; just-below-limit ratio; approver-concentration (HHI)
  anomaly.py    IsolationForest, KNN distance (pyod), LOF, Autoencoder(optional);
                rank-average ensemble -> anomaly_score
  graph.py      networkx employee-approver graph; detect reciprocal approvals & dense rings
  risk.py       final_risk = w1*anomaly + w2*KRI_severity + w3*graph_flag (weights in config,
                tuned on 20% labelled validation)
  copilot.py    LLM agent (LLM wrapper, mock default). Tools: sql_query(duckdb), get_claim(id),
                get_employee_profile(id), kri_explain(id). Outputs pydantic AuditFinding
                {claim_id, risk_level, schemes[], evidence[], recommended_action, ₹_at_risk}
  report.py     auditor pack: top-N cases -> markdown/HTML + CSV
app/streamlit_app.py
```

### 2.4 Method
1. Generate data → EDA on spend by category/grade.
2. KRIs alone → baseline precision@k.
3. Unsupervised ensemble → precision@k, recall@k, PR-AUC vs labels.
4. Combined risk score; weight tuning on validation slice.
5. Per-scheme recall table (which schemes rules catch vs ML catches).
6. Copilot: natural-language Q&A ("show split transactions in Sales above ₹50k in Q2") → SQL → answer + citations to claim_ids. Guardrail: SQL read-only, row cap 500.
7. Business translation: ₹ recovered if top-5% audited vs random 5%.

### 2.5 App
Tabs: **Risk queue** (sortable, filters) · **Claim drill-down** (KRI evidence, SHAP-like contribution, LLM finding) · **Network view** (pyvis ring graph) · **Ask the auditor copilot** (chat) · **Executive dashboard** (₹ at risk by dept/scheme).

### 2.6 Acceptance criteria
- [ ] Generator reproducible; label prevalence 2.5–3.5%.
- [ ] Ensemble beats KRI-only on PR-AUC; precision@5% ≥ 0.60.
- [ ] Copilot returns valid `AuditFinding` JSON in mock mode; SQL injection test blocked (DROP/UPDATE rejected).
- [ ] Memo: ₹ at risk detected, hours saved assuming 15 min/claim review.

### 2.7 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 2 "T&E Fraud Detection + GenAI Audit Copilot" per spec. PKG=tne.
Inspired by github.com/adarshb3/ISB_AMPBA_Capstone-Project_Deloitte--Anomaly-Detection-in-Business-Processes-using-Generative-AI
but use the synthetic labelled generator so precision/recall are measurable. DuckDB storage, LLM_PROVIDER=mock default.
Build M1 generator+ETL, M2 KRIs, M3 anomaly ensemble+graph, M4 copilot, M5 app+memo+CI.
[PASTE SECTION 2.1–2.6 HERE]
```

---

## Case Study 3 — Agentic Credit Underwriting for Retail/MSME Loans (FinTech GenAI)

**Reference repos:** [R4 anmolisb/CR — Credit Underwriting System](https://github.com/anmolisb/CR) (agents/, orchestrator/, prompts/, evaluation/ layout) · [R6 anmolisb/Escalant_SurveyProgramming — ISB AMPBA 2026S capstone](https://github.com/anmolisb/Escalant_SurveyProgramming) (LangGraph multi-agent + evaluation harness pattern) · [R1](https://github.com/Abhinav19-isb/credit-risk-scorecard) for the PD model.

### 3.1 Business problem
A lender's credit officers spend ~45 min per file reading applications, bank statements and bureau summaries. Build a multi-agent system that produces a **credit appraisal memo (CAM)** with decision, limit, pricing and conditions — human-in-the-loop for final approval.

- **KPIs:** decision agreement with ground truth ≥ 80%; cost-weighted error (bad approved costs 5×) lower than PD-model-alone; CAM generated < 60s; 100% of policy rules cited.

### 3.2 Data
- Structured: UCI Statlog German Credit — https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data — 1,000 applicants, 20 attributes, target good/bad, official 5:1 cost matrix. `fetch_ucirepo(id=144)`; decode A11..A202 codes to readable labels via a mapping dict in `src/uw/codes.py`.
- Unstructured (synthetic, `src/uw/docs_gen.py`): for each applicant generate (a) 6-month bank-statement CSV consistent with income/obligations, (b) application form text, (c) bureau summary text; inject 10% inconsistencies (stated income ≠ statement credits, undisclosed EMIs).
- Policy: `config/credit_policy.md` — 15 rules (FOIR ≤ 50%, age 21–65, min vintage, max exposure, bounce count ≤ 2 in 6m, etc.).

### 3.3 Architecture (LangGraph, `PKG=uw`)
```
src/uw/
  state.py         pydantic UnderwritingState (applicant, docs, extracted, ratios, pd, flags, decision, cam)
  agents/
    intake.py      parse docs -> structured fields (LLM + regex fallback)
    statement.py   cash-flow analytics: avg monthly credit, EMI detection, bounce count, FOIR
    verify.py      cross-check stated vs observed; fraud/inconsistency flags
    risk_model.py  calls PD model (LogReg + XGB trained on German Credit, cost-sensitive threshold)
    policy.py      RAG over credit_policy.md (sentence-transformers + FAISS); returns rule hits w/ citations
    decision.py    combines PD, policy hits, flags -> APPROVE / REFER / DECLINE, limit, rate = base + risk premium
    cam_writer.py  writes CAM markdown (sections: summary, applicant, financials, risks, mitigants, decision, conditions)
  graph.py         StateGraph: intake -> statement -> verify -> risk_model -> policy -> decision -> cam_writer;
                   conditional edge: if verify.critical_flags -> REFER (human review node)
  evaluation/
    harness.py     runs 200 held-out applicants; metrics: accuracy, cost-weighted loss, refer rate,
                   rule-citation coverage, hallucination check (every number in CAM must exist in state)
  api.py           FastAPI POST /underwrite -> CAM json
app/streamlit_app.py  upload/choose applicant -> live agent trace -> CAM -> approve/override with reason (logged)
```

### 3.4 Method
1. Train PD model; choose threshold minimising 5:1 cost (baseline).
2. Build agents one by one with unit tests on fixtures; mock LLM must make the whole graph run offline.
3. Evaluation harness compares: PD-only vs PD+policy vs full agentic (with verification) on cost-weighted loss.
4. Faithfulness check: regex all numbers in CAM, assert present in state (fail = hallucination).
5. Human override log → `outputs/overrides.csv` for later retraining.

### 3.5 Acceptance criteria
- [ ] Graph runs end-to-end in mock mode in tests.
- [ ] Full agentic cost-weighted loss < PD-only on held-out set.
- [ ] Inconsistency recall ≥ 85% on injected cases.
- [ ] 0 hallucinated numbers in 200 CAMs (mock) and report rate for real LLM.

### 3.6 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 3 "Agentic Credit Underwriting" per spec. PKG=uw. LangGraph + FastAPI + Streamlit.
Data: ucimlrepo id=144 + synthetic documents generator. LLM_PROVIDER=mock default; groq/openai optional.
Mirror the agents/ orchestrator/ evaluation/ structure of github.com/anmolisb/CR and the eval-harness discipline of
github.com/anmolisb/Escalant_SurveyProgramming. Milestones: M1 data+PD model, M2 statement & verify agents,
M3 policy RAG + decision, M4 CAM writer + graph + harness, M5 API/app/memo/CI.
[PASTE SECTION 3.1–3.5 HERE]
```

---
## Case Study 4 — NSE Factor Screener & Regime-aware Backtester (Capital Markets)

**Reference repo:** [R5 anmolisb/Stock2026 (Stock-Algo)](https://github.com/anmolisb/Stock2026) — 9-factor scoring of Nifty-500, regime filter (Nifty > 200-DMA, India VIX < 22), post-earnings drift entry, 5-layer exits, paper trading. ISB capstone theme reference: "Prediction of Future Security Prices".

### 4.1 Business problem
A retail-focused wealth/PMS desk wants a transparent, rules + ML swing-trading model on NSE stocks, with honest backtests (no look-ahead, survivorship noted, costs included).

- **KPIs (out-of-sample 2023-01 → latest):** CAGR > Nifty 50 TRI, Sharpe ≥ 1.0, max drawdown ≤ 20%, turnover-adjusted after 0.25% round-trip cost + 0.1% slippage.

### 4.2 Data
- Prices: `yfinance` daily OHLCV, tickers with `.NS` suffix; benchmark `^NSEI`; volatility `^INDIAVIX`. Period 2015-01-01 → today. Cache parquet per ticker.
- Universe: Nifty 500 list CSV `https://archives.nseindia.com/content/indices/ind_nifty500list.csv`. **Fallback** (if blocked): hard-coded Nifty 100 symbols list in `config/universe_fallback.txt`.
- Fundamentals (optional): `yf.Ticker(t).quarterly_financials` for earnings dates/surprise; skip gracefully if missing.

### 4.3 Modules (`PKG=quant`)
```
src/quant/
  data.py        download_prices(universe, start, end) with retry + cache; adjust for splits (auto_adjust=True)
  universe.py    load_universe(); liquidity filter (median 60d traded value > ₹10 Cr)
  factors.py     9 factors, each cross-sectionally z-scored daily:
                 mom_12_1, mom_3m, rel_strength_vs_nifty, dist_from_52w_high, low_vol_60d,
                 volume_surge_20d, rsi_14, trend (close>50DMA>200DMA), earnings_drift (if data)
  regime.py      risk_on = Nifty>200DMA and VIX<22 (thresholds in config); regime-switching via 2-state HMM (hmmlearn) as alternative
  signals.py     composite = weighted z-score (weights: equal | IC-weighted rolling 252d);
                 entry rules: top-N composite, trend ok, risk_on; ML variant: LightGBM ranking 20d fwd return
  portfolio.py   N=15 positions, equal or inverse-vol weights, max 20% per sector, weekly rebalance
  exits.py       5 layers: initial stop 2×ATR, trailing stop, time stop 30d, rank decay (falls out of top 50), regime off
  backtest.py    event-driven daily loop (vectorbt optional); costs & slippage; no look-ahead (signals at t close, trade t+1 open)
  metrics.py     CAGR, vol, Sharpe, Sortino, Calmar, max DD, hit rate, avg win/loss, turnover, IC/IR per factor
  walkforward.py rolling train 3y / test 1y for ML variant; purged + embargoed CV
  paper.py       daily run -> today's watchlist & orders CSV (no broker integration; Kite stub only)
app/streamlit_app.py
```

### 4.4 Method
1. Download & cache; data quality report (missing days, zero volume).
2. Factor research: IC, quintile spread returns, decay; correlation of factors.
3. Rules strategy backtest vs Nifty buy-and-hold.
4. ML ranking variant with walk-forward; compare.
5. Robustness: parameter sweep (N, stop multiple, rebalance freq) heatmap; bootstrap of monthly returns → Sharpe CI; Monte-Carlo trade shuffles.
6. Explicit limitations: survivorship bias (current constituents), no corporate actions beyond yfinance adjustment.

### 4.5 App
Tabs: **Today's screen** (ranked table + factor bars) · **Backtest** (equity curve vs Nifty, drawdown, monthly heatmap) · **Factor lab** (IC charts) · **Regime** (Nifty, VIX, risk-on shading) · **Stock drill-down** (chart with entries/exits).

### 4.6 Acceptance criteria
- [ ] `test_no_lookahead`: shifting future prices does not change past signals.
- [ ] Costs applied on every trade; turnover reported.
- [ ] Out-of-sample metrics table for rules & ML vs benchmark in README.
- [ ] Disclaimer: research only, not investment advice.

### 4.7 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 4 "NSE Factor Screener & Regime-aware Backtester" per spec. PKG=quant.
Reference design: github.com/anmolisb/Stock2026. yfinance data with caching and fallback universe.
Milestones: M1 data+universe, M2 factors+IC research, M3 rules backtest+exits+regime, M4 ML walk-forward+robustness,
M5 app, memo, CI. Enforce no look-ahead with a unit test.
[PASTE SECTION 4.1–4.6 HERE]
```

---

## Case Study 5 — Promotion Cannibalisation Engine (E-commerce Pricing)

**Reference repo:** [R7 akash-sood97/promotion-cannibalisation-engine](https://github.com/akash-sood97/promotion-cannibalisation-engine) — "ISB AMPBA"; on UCI Online Retail II shows the dashboard-preferred promo looks profitable in 86% of conditions but is profitable for the whole family in only 11%.

### 5.1 Business problem
Category managers judge promotions by the promoted SKU's uplift. Build an engine that scores a discount on **family net contribution** = incremental margin − subsidy on baseline units − margin lost on cannibalised siblings + basket pull (halo).

- **KPIs:** % of proposed promos correctly classified profitable/unprofitable vs simulation truth; ₹/£ net contribution per promo; break-even elasticity.

### 5.2 Data
- UCI Online Retail II — https://archive.ics.uci.edu/dataset/502/online+retail+ii — ~1M lines, UK online retailer, 2009-12 → 2011-12. Load via `fetch_ucirepo(id=502)`; if unavailable, download the xlsx from the UCI page (two sheets) with `pd.read_excel(sheet_name=None)`.
- Clean: drop cancellations (Invoice starts with "C"), Quantity ≤ 0, Price ≤ 0, non-product StockCodes (POST, M, DOT, BANK CHARGES, etc.), missing Customer ID kept for basket analysis only.

### 5.3 Modules (`PKG=promo`)
```
src/promo/
  data.py        load_clean(); weekly SKU panel (units, avg price, revenue, n_baskets)
  catalog.py     product families: TF-IDF on Description + agglomerative clustering, plus
                 co-purchase substitution check (substitutes rarely co-occur in a basket); manual override CSV
  baskets.py     association rules (mlxtend FP-Growth) -> lift/confidence; halo pull per SKU
  demand.py      (a) log-log elasticity regression per SKU with week FE where price varies;
                 (b) MNL/nested-logit choice model per family calibrated to shares (outside option = no purchase)
  engine.py      score_promo(sku, discount, params) -> {direct_uplift, subsidy_cost, cannibalised_margin,
                 halo_margin, family_net}; break_even_elasticity(sku, discount)
  sweep.py       Latin-hypercube sweep over elasticity [-1,-6], substitution share [0,0.8], margin [25%,55%],
                 halo discount [0,1] -> % conditions profitable (promoted-only vs family)
  optimise.py    pick best discount ∈ {0,5,10,15,20,25%} per family under budget constraint (pulp)
  viz.py         waterfall chart of contribution, tornado sensitivity, heatmaps
analysis/run_analysis.py  -> outputs/summary.json, figures/*.png, docs/DECISION_MEMO.md numbers
app/streamlit_app.py
```

### 5.4 Method
1. EDA: top families, price variation availability, seasonality (Q4 peak).
2. Build families; validate with low co-purchase rate among members.
3. Estimate elasticities where identifiable; otherwise priors + sweep (state this honestly).
4. Choice model → cannibalisation share; basket rules → halo.
5. Score a reference promotion (10% off) for 24 top SKUs; waterfall.
6. Sweep; report % profitable promoted-only vs family-net; break-even elasticity distribution.
7. Optimiser recommends promo calendar for next 8 weeks under discount budget.

### 5.5 App
Pick SKU + discount → waterfall (direct, subsidy, cannibalisation, halo, net) · sensitivity sliders · family view · recommended promo plan.

### 5.6 Acceptance criteria
- [ ] Engine identity test: family_net = direct − subsidy − cannibalised + halo (±1e-6).
- [ ] Sweep ≥ 1,000 draws; results reproducible with seed.
- [ ] Memo reports: reference promo family net, % profitable both views, break-even multiplier.

### 5.7 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 5 "Promotion Cannibalisation Engine" per spec. PKG=promo.
Data: UCI Online Retail II (id=502). Reproduce and extend github.com/akash-sood97/promotion-cannibalisation-engine
(add elasticity estimation where price varies, promo optimiser, Streamlit app).
Milestones: M1 data+families, M2 baskets+demand, M3 engine+sweep, M4 optimiser, M5 app/memo/CI.
[PASTE SECTION 5.1–5.6 HERE]
```

---

## Case Study 6 — Customer Segmentation (RFM + CLV), Market Basket & Recommender (E-commerce Marketing)

**Reference repos:** [R17 RishabhBansal2409/Recommendation_Engine](https://github.com/RishabhBansal2409/Recommendation_Engine) (user/item CF) · ISB capstone title "Customer Profiling & Market Basket Analysis" (AMPBA Applied Learning page) · [R7](https://github.com/akash-sood97/promotion-cannibalisation-engine) for basket rules on the same data.

### 6.1 Business problem
CRM team needs (a) actionable segments, (b) 12-month CLV per customer, (c) cross-sell bundles, (d) personalised top-10 product recommendations for email campaigns.

- **KPIs:** silhouette ≥ 0.35 for segments; CLV MAE vs holdout spend; Recommender HitRate@10 and NDCG@10 beating popularity baseline by ≥ 30%.

### 6.2 Data
UCI Online Retail II (id=502), rows with Customer ID only. Calibration period up to 2011-06-30, holdout 2011-07-01 → 2011-12-09.

### 6.3 Modules (`PKG=crm`)
```
src/crm/
  data.py        clean (as Case 5) + customer-level table
  rfm.py         recency, frequency, monetary, tenure, avg basket, n_categories; quintile RFM codes;
                 named segments (Champions, Loyal, At-Risk, Hibernating, New, Big-spenders)
  cluster.py     log+scale; KMeans k=2..10 (elbow, silhouette), GMM, HDBSCAN comparison; profile table
  clv.py         lifetimes BG/NBD + Gamma-Gamma on calibration; predict holdout purchases & spend;
                 baseline = historical avg; metrics MAE, Spearman
  basket.py      FP-Growth (mlxtend) min_support tuned; rules filtered lift>3, conf>0.3; bundle candidates
  recsys.py      baselines: popularity, item-item cosine CF; models: implicit ALS (implicit lib), LightFM optional;
                 time-based split (last 30 days per user as test); HitRate@10, NDCG@10, coverage
  campaign.py    segment × action matrix (win-back, upsell, loyalty) with expected ₹ uplift assumptions
app/streamlit_app.py
```

### 6.4 Method
1. RFM + rule segments → cluster segments; compare & name.
2. CLV with BG/NBD/GG; calibration plot; top-decile CLV share.
3. Market basket rules → top 20 bundles with lift.
4. Recommender: baselines vs ALS; tune factors/regularisation; evaluate.
5. Campaign plan per segment with budget and expected ROI.

### 6.5 App
Segment explorer (2D UMAP plot, profile cards) · Customer 360 (RFM, CLV, recommendations) · Bundle finder · Campaign planner.

### 6.6 Acceptance criteria
- [ ] Time-based splits; no holdout leakage into CLV/recsys.
- [ ] Recsys beats popularity on NDCG@10 by ≥ 30%.
- [ ] Memo: segment sizes, revenue share, CLV top-decile share, campaign ROI table.

### 6.7 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 6 "RFM Segmentation, CLV, Market Basket & Recommender" per spec. PKG=crm.
Data UCI id=502. Extend github.com/RishabhBansal2409/Recommendation_Engine with implicit ALS and proper time split.
Milestones: M1 data+RFM, M2 clustering, M3 CLV, M4 basket+recsys, M5 campaign/app/memo/CI.
[PASTE SECTION 6.1–6.6 HERE]
```

---
## Case Study 7 — Churn Prediction + Uplift-based Retention (E-commerce / Subscription)

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

---

## Case Study 8 — Two-sided Marketplace Dynamic Pricing (Quick-commerce / Gig platforms)

**Reference repo:** [R8 akash-sood97/two-sided-pricing-engine](https://github.com/akash-sood97/two-sided-pricing-engine) — "ISB AMPBA"; two-sided demand (customer elasticity + partner drop-off), per-segment optimiser with ₹220 partner pay floor and 90% fulfilment target; +7.1% contribution vs +3.2% for demand-only pricing; holdout, placebo and 400-draw robustness.

### 8.1 Business problem
A home-services / quick-commerce platform sets customer price **and** partner payout per (city × service × time-slot). Raising price lowers demand; lowering payout lowers partner acceptance → unfulfilled orders. Maximise contribution subject to fulfilment ≥ 90% and payout floor.

- **KPIs:** contribution uplift vs current pricing; fulfilment rate; partner earnings per hour.

### 8.2 Data — simulator (`src/mkt/sim.py`)
- 6 cities × 5 services × 4 time-slots × 52 weeks; segment-level base demand with seasonality.
- Customer demand: `D = D0 * (p/p0)^ε_c`, ε_c segment-specific drawn from priors whose mean is **calibrated** from Online Retail II price-quantity regressions (reuse Case 5 `demand.py`; note this calibration is an analogy).
- Partner supply: acceptance prob `A = sigmoid(α + β*(payout - reservation_wage))`; partner churn weekly if earnings < threshold.
- Historical log: random price experiments (±10%) on 20% of segment-weeks to allow estimation.

### 8.3 Modules (`PKG=mkt`)
```
src/mkt/
  sim.py         generate history + ground-truth parameters
  estimate.py    customer elasticity via log-log with segment FE on experiment rows; partner acceptance via logistic regression
  optimise.py    per segment grid/convex search over (price, payout) maximising
                 contribution = D(p)*min(1, A(w)*capacity/D)*(p - w - var_cost) s.t. fulfil>=0.9, w>=220
  policies.py    current (static), demand-only (ignores supply), two-sided (ours)
  validate.py    temporal holdout (last 12 weeks), placebo test (shuffled prices -> no gain), 400 posterior draws of params
  explorer/      optional stlite static page
app/streamlit_app.py  segment selector, price & payout sliders, live demand/fulfilment/contribution surface (plotly 3D/heatmap)
```

### 8.4 Acceptance criteria
- [ ] Estimated elasticities within ±20% of simulator truth (recovery test).
- [ ] Two-sided policy > demand-only > static on holdout contribution with fulfilment ≥ 90%.
- [ ] Robustness: % of 400 draws where two-sided wins ≥ 80%.

### 8.5 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 8 "Two-sided Marketplace Dynamic Pricing" per spec. PKG=mkt.
Follow github.com/akash-sood97/two-sided-pricing-engine; simulator with known truth so parameter recovery is testable.
Milestones: M1 simulator, M2 estimation+recovery tests, M3 optimiser+policies, M4 validation (holdout/placebo/draws), M5 app/memo/CI.
[PASTE SECTION 8.1–8.4 HERE]
```

---

## Case Study 9 — Dark-store Demand Forecasting & Serviceability Optimiser (Quick-commerce Supply Chain)

**Reference repos:** [R10 akash-sood97/supply-serviceability-capstone](https://github.com/akash-sood97/supply-serviceability-capstone) (count forecast + MIP lever mix; hub-weeks at 95% service 74% → 100%, contribution ₹2.74M → ₹3.88M) · [R11 akash-sood97/distribution-network-design](https://github.com/akash-sood97/distribution-network-design) (PuLP/HiGHS vs heuristic) · [R13 Siddharth0711/Foundation-Project-2](https://github.com/Siddharth0711/Foundation-Project-2) (Holt-Winters/SARIMAX/Prophet/LSTM + P5/P50/P95) · [R12 Siddharth0711/AMPBA-Capstone-PharmaTrace](https://github.com/Siddharth0711/AMPBA-Capstone-PharmaTrace) (ABC-FSN + LP). ISB capstone theme: "Freight Optimization through Analytical Model".

### 9.1 Business problem
A 10-minute-delivery company runs 12 dark stores × 4 categories. Forecast weekly orders with uncertainty, then choose the cheapest mix of levers — add riders, rebalance riders across stores, surge price, cap intake, extend radius — to hold 95% on-time serviceability.

- **KPIs:** forecast WAPE beats seasonal-naive by ≥ 15%; P90 coverage 85–95%; % store-weeks meeting 95% SLA; ₹ contribution.

### 9.2 Data — generator (`src/qc/sim.py`)
Store × category × day for 2 years: trend, weekly + annual seasonality, Indian festival spikes (Diwali, Holi, IPL weekends via calendar CSV), weather shocks, promotions; rider capacity, rider cost/hour, order margin. Seeded. Provide real-data hook: `load_external(path)` expecting same schema.

### 9.3 Modules (`PKG=qc`)
```
src/qc/
  sim.py         generator + festival calendar
  features.py    lags, rolling means, calendar & festival flags, promo flag
  forecast.py    seasonal-naive, ETS/Holt-Winters, SARIMAX, Prophet, LightGBM global model (quantile 0.1/0.5/0.9),
                 optional N-BEATS/TFT via darts; rolling-origin backtest 8 folds
  reconcile.py   hierarchical reconciliation store->city (MinT via statsforecast/hierarchicalforecast) optional
  abc_fsn.py     ABC (value) × FSN (velocity) classification of SKUs for stocking policy
  inventory.py   safety stock = z*σ_LT*√LT; reorder point; service-level vs holding-cost curve
  optimise.py    MIP (pulp+HiGHS): decision vars riders_added[s,w], transfers[s,s',w], surge[s,w]∈levels, cap[s,w];
                 constraint served >= 0.95*demand_P90; minimise cost - margin; heuristic baseline (greedy + local search)
  evaluate.py    run plan against 200 simulated demand paths -> SLA attainment distribution
app/streamlit_app.py  forecast fan charts, lever plan table, map of stores (pydeck), what-if sliders (SLA target, rider cost)
```

### 9.4 Acceptance criteria
- [ ] Rolling-origin backtest table (WAPE, MASE, pinball loss) per model; best beats seasonal-naive ≥ 15%.
- [ ] MIP solution vs heuristic gap reported; MIP solves < 60 s.
- [ ] SLA attainment across 200 paths reported (mean & P10).
- [ ] Memo: lever mix, ₹ cost, SLA before/after.

### 9.5 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 9 "Dark-store Demand Forecasting & Serviceability Optimiser" per spec. PKG=qc.
Combine ideas from github.com/akash-sood97/supply-serviceability-capstone, github.com/akash-sood97/distribution-network-design
and github.com/Siddharth0711/Foundation-Project-2. Milestones: M1 generator, M2 forecasting backtest, M3 inventory/ABC-FSN,
M4 MIP + heuristic + simulation eval, M5 app/memo/CI.
[PASTE SECTION 9.1–9.4 HERE]
```

---

## Case Study 10 — Review Intelligence: Aspect Sentiment + RAG Copilot (E-commerce GenAI / NLP)

**Reference repos:** [R16 RishabhBansal2409/Sentiment_Analysis_of_Customer_Reviews](https://github.com/RishabhBansal2409/Sentiment_Analysis_of_Customer_Reviews) (scrape + sentiment + Shiny) · [R18 RishabhBansal2409/Natural_Language_Processing__Chatbot](https://github.com/RishabhBansal2409/Natural_Language_Processing__Chatbot) (intent bot) · [R6 anmolisb/Escalant_SurveyProgramming](https://github.com/anmolisb/Escalant_SurveyProgramming) (LangGraph agents + evaluation harness, ISB AMPBA 2026S). ISB capstone theme: "Auto-classification of Products into Categories".

### 10.1 Business problem
Product & CX teams can't read 100k+ reviews. Build: (a) aspect-based sentiment (battery, delivery, quality, price, packaging…), (b) emerging-issue alerts, (c) a grounded RAG copilot answering "Why are 2-star reviews rising for SKU X?" with citations.

- **KPIs:** sentiment macro-F1 ≥ 0.80 (3-class); aspect extraction F1 ≥ 0.70 on 300 hand/LLM-labelled reviews; RAG faithfulness ≥ 0.85 & answer relevancy ≥ 0.80 (RAGAS or own LLM-judge); p95 latency < 5 s.

### 10.2 Data
- HuggingFace `McAuley-Lab/Amazon-Reviews-2023` — https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023 — use categories `Electronics` or `Cell_Phones_and_Accessories`; sample 100k reviews + item metadata (`raw_review_*`, `raw_meta_*` configs, `trust_remote_code=True`). Fallback: Flipkart product reviews CSV placed in `data/raw/` by the user.
- Labels: star rating → sentiment (1–2 neg, 3 neu, 4–5 pos); aspect gold set: 300 reviews labelled via LLM then human-verified (store in `data/gold/aspects.jsonl`).

### 10.3 Modules (`PKG=revai`)
```
src/revai/
  data.py         load sample, clean, language filter, dedupe, PII scrub (emails/phones regex)
  sentiment.py    baselines TF-IDF+LogReg, VADER; transformer fine-tune (distilbert-base-uncased, 2 epochs, HF Trainer);
                  report macro-F1, confusion matrix
  aspects.py      aspect taxonomy per category (config); (a) zero-shot NLI (facebook/bart-large-mnli) or
                  (b) LLM structured extraction -> [{aspect, sentiment, span}]; evaluate on gold
  topics.py       BERTopic on negative reviews; monthly topic trends
  alerts.py       emerging issue = aspect-negative share z-score > 3 vs trailing 8 weeks per SKU
  classify.py     product auto-categorisation from title+description (embeddings + LogReg) — ISB capstone theme
  rag/
    index.py      chunk reviews (by review) + metadata (asin, rating, date); embeddings bge-small-en-v1.5; FAISS or Chroma
    retrieve.py   hybrid BM25 + dense, metadata filters (asin, date range, rating), rerank (bge-reranker-base, optional)
    graph.py      LangGraph: route(question) -> {sql_stats tool over DuckDB aggregates | rag_retrieve} -> answer with [review_id] citations
                  -> self-check node (claims supported by retrieved text?) -> final
    eval.py       50-question test set (auto-generated + curated) -> faithfulness, relevancy, citation precision
  api.py          FastAPI /ask, /aspects/{asin}, /alerts
app/streamlit_app.py  SKU dashboard (aspect sentiment bars, trend lines, alerts), review explorer, copilot chat with citations
```

### 10.4 Method
1. Sample & clean; EDA (rating distribution, length, verified purchase).
2. Sentiment baselines → transformer; error analysis on neutral class.
3. Aspect extraction + evaluation; aspect × month heatmaps.
4. BERTopic + alerting backtest (did alerts precede rating drops?).
5. RAG build + evaluation harness; compare dense vs hybrid vs hybrid+rerank.
6. Cost/latency table per LLM provider; mock mode for tests.

### 10.5 Acceptance criteria
- [ ] Transformer beats TF-IDF baseline on macro-F1.
- [ ] RAG eval table for 3 retrieval configs; every answer has ≥ 1 valid citation.
- [ ] Pipeline runs on 20k sample in < 15 min on CPU (flag `--full` for 100k / GPU).
- [ ] Memo: top 5 issues for chosen category with ₹/rating impact estimate.

### 10.6 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 10 "Review Intelligence: Aspect Sentiment + RAG Copilot" per spec. PKG=revai.
Data: HF McAuley-Lab/Amazon-Reviews-2023 (Electronics sample). LLM_PROVIDER=mock default.
Extend github.com/RishabhBansal2409/Sentiment_Analysis_of_Customer_Reviews; use LangGraph + eval-harness discipline of
github.com/anmolisb/Escalant_SurveyProgramming. Milestones: M1 data+sentiment, M2 aspects+topics+alerts,
M3 RAG index+graph, M4 RAG eval, M5 API/app/memo/CI.
[PASTE SECTION 10.1–10.5 HERE]
```

---

## 5. Portfolio packaging (after all 10)

| Item | Spec |
|---|---|
| GitHub | One repo per case (`ampba-01-credit-scorecard` …) + a `ampba-portfolio` index README with results table & GIFs |
| Deployment | Streamlit Community Cloud or HuggingFace Spaces (mock LLM mode for public demos) |
| Each README | Problem → Data → Approach diagram (mermaid) → Results table (baseline vs model) → Business impact (₹) → Limitations → How to run |
| Decision memo | 1 page, written for a CXO: recommendation, ₹ impact, risks, next steps |
| Review decks | Mid-review (P1–P4) and Final (P5–P7), 10 slides each, mirrors ISB's two formal reviews |
| LinkedIn post | 150 words + 1 chart + repo link, tagged #ISB #AMPBA |

## 6. Suggested 12-week schedule (mirrors ~3-month capstone, ~10 h/week)

| Week | Work |
|---|---|
| 1 | Setup template (Section 2), CS1 |
| 2 | CS5, CS6 |
| 3 | CS7 |
| 4–5 | CS2 |
| 6 | CS8 |
| 7 | CS4 |
| 8–9 | CS9 |
| 10–11 | CS3, CS10 |
| 12 | Portfolio packaging, deployments, posts |

## 7. Sources

- ISB AMPBA curriculum: https://www.isb.edu/programmes/advanced-management-programmes/ampba/curriculum
- ISB AMPBA Applied Learning (capstone process & past titles): https://www.isb.edu/programmes/advanced-management-programmes/ampba/programme-overview/applied-learning
- Reference repos R1–R19 in Section 3.
- Datasets: UCI #350, #502, #144; HuggingFace McAuley-Lab/Amazon-Reviews-2023; yfinance / NSE index constituents.
