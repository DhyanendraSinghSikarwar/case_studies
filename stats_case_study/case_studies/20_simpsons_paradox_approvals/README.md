# Case Study 20 — Did the New Approval Policy Reduce Approvals? Simpson's Paradox

| | |
|---|---|
| **Domain** | Credit policy: personal-loan approvals |
| **Difficulty** | Intermediate |
| **Importance** | 🟠 SHOULD GO THROUGH |
| **Techniques** | Two-proportion comparison · stratified analysis · rate/mix decomposition · direct standardisation · Mantel-Haenszel pooled odds ratio · Breslow-Day and Cochran Q tests (odds-ratio vs risk-difference scale) · logistic adjustment · causal stories (confounder vs mediator) |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

## 1. Business problem

After an April policy change, the overall approval rate fell. Leadership asks whether the new policy is too strict.

## 2. Dataset

`data/loan_applications.csv`: 27,000 applications (12,000 before, 15,000 after) with period, channel (Branch, Online, Agent), risk band (A to D) and approval.

## 3. Methods

Overall comparison · within-band comparison · decomposition into rate and mix effects · channel analysis of the mix shift · standardised rates · Mantel-Haenszel and CMH · heterogeneity tests on two scales · logistic regression · causal-story reasoning.

## 4. Key findings

| Finding | Value |
|---|---|
| Overall | 69.6% → 65.7%: −3.9 pp (95% CI −5.0 to −2.8); odds ratio 0.84 |
| Within every band | A +5.1, B +6.4, C +5.7, D +5.0 pp (all p ≤ 0.001) |
| Decomposition | rate effect +5.6 pp, mix effect −9.5 pp; share in bands C/D 24% → 40% |
| Cause of mix shift | Agent channel 11% → 45%; risk mix within each channel unchanged |
| Standardised | +5.6 pp under any fixed mix (CI about +4.6 to +6.4) |
| Mantel-Haenszel OR | 1.45 (95% CI 1.36–1.54), against crude 0.84 |
| Heterogeneity | odds-ratio scale: differs by band (Breslow-Day p < 0.001); risk-difference scale: no evidence (Cochran Q p = 0.71) |

## 5. Business recommendations

Report the standardised, band-level result (approvals up about 5.6 points at like-for-like risk) alongside the overall rate · monitor approval by risk band and channel · treat the fall as a portfolio-mix effect from the agent channel expansion · decide on risk appetite for that channel separately.

## 6. Limitations

Before/after design without a control group (other changes at the same time are possible) · risk band is assumed to be unaffected by the policy · synthetic data.

## 7. Concepts learned

Simpson's paradox is arithmetic, not error · the right comparison depends on the causal story (confounder: adjust; mediator: do not) · decomposition and standardisation · effect heterogeneity depends on the scale (odds ratio vs risk difference) · collapsed odds ratios are not averages of stratum odds ratios.

## How to reproduce

```bash
python case_studies/20_simpsons_paradox_approvals/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/20_simpsons_paradox_approvals/notebooks/01_analysis.ipynb
python case_studies/20_simpsons_paradox_approvals/src/build_presentation.py
```
