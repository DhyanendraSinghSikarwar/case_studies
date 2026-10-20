import json, re
RATE = {int(k): v for k, v in json.load(open("_build/rate.json")).items()}
STAR = {3: "★★★ Must-visit", 2: "★★ Good to have", 1: "★ Optional"}
ref = open("indian_ecommerce_data_science_case_studies.md", encoding="utf-8").read()
ev = {}
for k in range(1, 31):
    seg = ref.split(f"## Case Study {k} — ")[1].split("## Case Study")[0]
    m = re.search(r"\*\*Evidence Level:\*\*\s*\**\s*(Strong|Medium|Weak)", seg); ev[k] = m.group(1) if m else "ND"
rows = [f"| {k} | {STAR[RATE[k][0]]} | `{RATE[k][1]}.ipynb` | ⏳ pending | {RATE[k][2]} | {ev[k]} |" for k in range(1, 31)]
readme = """# Indian Ecommerce and Quick-Commerce Data Science: 30 Case Studies, Solved End to End

A companion to the fintech case-study project. Thirty problems that Indian ecommerce, quick-commerce, food-delivery and marketplace data-science teams actually work on, and that interviews ask about: delivery ETA, demand forecasting, recommendations and search, ads ranking, A/B testing, customer lifetime value, coupon uplift, COD return-to-origin, and more. Each case is rated **★★★ Must-visit**, **★★ Good to have** or **★ Optional** (frequency in industry and in interviews).

Each notebook follows the same structure as the fintech series: a plain-English explanation for business leaders, what the company documented vs what we simulate, hypotheses, data and data-quality checks, EDA, **statistics as the core** (assumptions, effect sizes, CIs, power, multiple testing, written observations), a short ML section, a ₹ business case with best/base/worst scenarios, recommendation and KPIs, risks and an appendix of formulas and glossary.

> ⚠️ **All outcome data is synthetic.** Company logs are confidential. Generators are calibrated to figures the cited public sources actually state. Public method detail is thin for several problems (pricing, surge fees, sale-event planning, push notifications, marketing-mix modelling): for those, the reference file says so and the notebook is an **interview-standard solution on simulated data**, not a reproduction of any company's system. See `indian_ecommerce_data_science_case_studies.md` for the sourced case write-ups with evidence levels, and `decision.md` for every sourcing and design decision.

## How to run

```bash
pip install -r requirements.txt
python -m ipykernel install --user --name fintech-cases --display-name "Python 3.12 (fintech-cases)"   # same kernel name as the fintech project
jupyter nbconvert --to notebook --execute --inplace cs01_delivery_eta_prediction.ipynb               # regenerates its data in data/
# If `jupyter` is not on PATH: python -m nbconvert --to notebook --execute --inplace <file>
```

- Random seed = 42 everywhere (independent child streams via `SeedSequence(42)` where several random processes interact).
- Each notebook writes its generator to `data/generate_*.py` and regenerates its data in `data/<case>/`.
- `_build/nbtool.py` is the authoring tool (source to notebook, execute, dump, fill written observations, verify, update this table). It is not needed to run the notebooks. `_build/research/` holds the raw research notes.

<!-- CASE-INDEX-START -->
## All 30 case studies: priority and notebook status

Stars: **★★★ Must-visit** · **★★ Good to have** · **★ Optional**.

| Case | Priority | Notebook | Status | Core technique | Public evidence |
|---|---|---|---|---|---|
""" + "\n".join(rows) + """
<!-- CASE-INDEX-END -->
"""
open("README.md", "w", encoding="utf-8").write(readme)
dec = """# Decision Log: Indian Ecommerce and Quick-Commerce Case Studies

Every sourcing, modelling and interpretation decision, in the format used in the fintech project: **Date / Case / Context / Options / Decision / Why / Assumption checks / Impact**, followed by a summary table at the end.

---

# Project-wide decisions

## D-0-01: All outcome data is synthetic

- Date: 2026-10-17
- Case: 0 (all)
- Context / question: Ecommerce, quick-commerce and food-delivery logs are confidential. Can public data replace them?
- Options considered: public datasets (Instacart, Olist, Retailrocket, Criteo, Kaggle-hosted sets: several are Kaggle-only or lack the needed fields); scraping marketplaces (terms-of-service and robots restrictions); synthetic data calibrated to documented figures.
- Decision: Synthetic data with hidden ground-truth columns (prefixed `_`), calibrated to figures the cited sources state. No Kaggle data and no scraping.
- Why: Only simulation provides both realistic messiness and a known truth against which methods can be checked.
- Assumption checks / evidence: Each notebook separates documented from simulated parameters in section 2.
- Impact if wrong / mitigation: Magnitudes are illustrative. Methods transfer; re-run on real data.

## D-0-02: Evidence levels and substitutions in the case list

- Date: 2026-10-17
- Case: 0 (all)
- Context / question: Public method detail is uneven across companies.
- Options considered: fill gaps from memory; substitute a better-documented company; mark ND.
- Decision: Research agents recorded only facts they opened, substituted better-documented companies where needed (stated in each entry), and marked everything else ND. Six cases are Weak: the notebooks for those are interview-standard problems on simulated data.
- Why: Not inventing "documented" facts.
- Assumption checks / evidence: Evidence column in the README; entries in the reference file.
- Impact if wrong / mitigation: None.

## D-0-03: Same method standards as the fintech series

- Date: 2026-10-17
- Case: 0 (all)
- Context / question: Which standards apply to every notebook?
- Options considered: ad hoc; the fintech standards.
- Decision: Seed 42; pandas, numpy, scipy, statsmodels, scikit-learn, matplotlib, seaborn (xgboost or boosting via scikit-learn); every chart titled, labelled and followed by a takeaway; observations written after execution; no hyper-parameter tuning; honest reporting of null and negative results.
- Why: Comparability and honesty.
- Assumption checks / evidence: `_build/nbtool.py verify` on every notebook.
- Impact if wrong / mitigation: None.

---

# Summary table

| ID | Case | Decision | Why |
|---|---|---|---|
| D-0-01 | 0 | All outcome data synthetic, hidden truth columns | Logs confidential; known truth for validation |
| D-0-02 | 0 | Evidence levels; substitutions; Weak cases flagged | No invented "documented" facts |
| D-0-03 | 0 | Same method standards as fintech series | Comparability and honesty |
"""
open("decision.md", "w", encoding="utf-8").write(dec)
# point nbtool at the ecommerce reference file
t = open("_build/nbtool.py", encoding="utf-8").read().replace("indian_fintech_data_science_case_studies.md", "indian_ecommerce_data_science_case_studies.md")
open("_build/nbtool.py", "w", encoding="utf-8").write(t)
print("ok", len(rows))
