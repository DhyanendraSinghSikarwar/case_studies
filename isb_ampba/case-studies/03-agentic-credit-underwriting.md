# Case Study 3 — Agentic Credit Underwriting for Retail/MSME Loans (FinTech GenAI)

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
