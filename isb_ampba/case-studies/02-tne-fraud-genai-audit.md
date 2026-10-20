# Case Study 2 — Expense (T&E) Fraud Detection + GenAI Audit Copilot (FinTech / Audit)

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
