# Case Study 10 — Modelling Insurance Claim Cost

| | |
|---|---|
| **Domain** | Health insurance: claim-cost pricing and reserving |
| **Difficulty** | Intermediate–Advanced |
| **Importance** | 🟠 SHOULD GO THROUGH |
| **Techniques** | Four-panel regression diagnostics · Cook's distance and business-rule checks · Breusch-Pagan, RESET, Jarque-Bera · HC3 robust SEs · Box-Cox profile likelihood · square-root and log transforms · mean-variance power law · component-plus-residual plots · centred polynomial terms · smearing estimator · gamma GLM with log link · quantile residuals · expected value of a capped gamma · simulated reserve range |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

## 1. Business problem

The Appointed Actuary needs a claim-cost model for pricing and for reserving ~1,500 open claims. The team's
regression on raw ₹ explains little and predicts negative costs; a later log model under-reserved.

## 2. Dataset

`data/health_claims.csv`: 6,000 settled hospitalisation claims. Columns: age, procedure category (nominal, 7), room
type (ordinal, 4), hospital type (nominal, 3), pre-authorised length of stay, smoker, diabetic, sum insured, claim
amount. In the generator ([`src/generate_data.py`](src/generate_data.py)), costs are gamma-distributed with
multiplicative effects, capped at the sum insured; 6 claims were keyed in paise (×100).

## 3. Methods

Model A: OLS on raw ₹ with diagnostics → Cook's distance and the sum-insured rule find the errors → HC3 SEs → Box-Cox
profile and sqrt/log comparison → mean-variance slope → component-plus-residual plots (log LOS, centred age²) →
Model B: log-OLS with smearing → Model C: gamma GLM (log link), with the cap applied via E[min(Y, sum insured)] →
holdout comparison on 1,500 claims → reserve simulation with coefficient and claim uncertainty.

## 4. Key findings

| Finding | Value |
|---|---|
| Data errors | 6 claims above the sum insured: the 6 largest Cook's distances (0.004–0.83) |
| Model A (raw ₹, clean) | R² 0.46; 96 negative predictions; Breusch-Pagan, RESET and Jarque-Bera all p < 0.001 |
| HC3 vs classical SE | up to ~1.5× larger for cardiac, oncology, suite |
| Box-Cox | λ = 0.15 (95% CI 0.13–0.17): log scale (gamma-like data sit between log and cube root) |
| Mean-variance slope | 1.94 → variance ∝ mean² → gamma; estimated shape 2.56 (CV 0.63) |
| Functional form | log(LOS) and centred age² improve fit (age² F = 66, p < 0.001) |
| Smearing factor | 1.23: naive exp() under-predicts the mean by 19% |
| Gamma effects | cardiac +175%, oncology +205%, suite +57%, non-network +10%, diabetic +7%, smoker +6% |
| Holdout total (₹18.67 Cr actual) | naive log −14.4% · raw OLS +4.7% · smeared +5.1% · gamma +4.6% · **gamma + cap −0.1%** |
| Reserve | best estimate ₹18.66 Cr; 90% range ₹18.07–19.27 Cr; 99.5th percentile ₹19.66 Cr |

## 5. Business recommendations

Adopt the gamma GLM with the sum-insured cap for pricing and reserving · reserve ≈ ₹18.7 crore with the simulated range
as the basis for the risk margin · retire the raw-₹ model · never use exp(log prediction) as a mean · reject claim
amounts above the sum insured at load time.

## 6. Limitations

Gamma tail may be too light for real catastrophic claims · fitted on capped data · no inflation or IBNR · associations,
not causes · synthetic data.

## 7. Concepts learned

What each diagnostic plot and test checks · tests vs plots at large n · data error vs genuine extreme · robust SEs fix
inference, not the model · Box-Cox and what λ tells you · variance-mean power law → choice of distribution · partial
residual plots · centring polynomials · retransformation bias and smearing · GLMs separate link and distribution ·
quantile residuals · capped outcomes · uncertainty of a total vs a single claim.

## How to reproduce

```bash
python case_studies/10_insurance_claim_cost/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/10_insurance_claim_cost/notebooks/01_analysis.ipynb
python case_studies/10_insurance_claim_cost/src/build_presentation.py
```
