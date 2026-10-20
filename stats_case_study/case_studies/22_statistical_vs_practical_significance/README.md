# Case Study 22 — Significant but Irrelevant; Non-Significant but Promising

| | |
|---|---|
| **Domain** | Product and pricing experiments |
| **Difficulty** | Intermediate |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Statistical vs practical significance · break-even effect from costs · CI against a decision threshold · p-value vs sample size · power and MDE · Bayesian probability of a worthwhile effect · value of information · Type S and Type M errors · reporting inconclusive results |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data. A teaching-only answer key (`data/answer_key_teaching_only.csv`, the true lifts) is opened only in the grading section.

## 1. Business problem

Two readouts: (A) a checkout redesign, "p = 0.0001, launch"; (B) a fee-waiver offer, "p = 0.25, drop it". Are those the right calls?

## 2. Dataset

`data/experiment_a_checkout.csv`: 28 days × 2 arms, about 3.0 million visitors. `data/experiment_b_fee_waiver.csv`: 1,200 customers (600 per arm).

## 3. Key findings

| Finding | Value |
|---|---|
| A: lift | +0.10 pp (95% CI 0.05 to 0.15), p = 0.0001, relative +2% |
| A: break-even | 0.20 pp (₹32 lakh a year cost ÷ ₹40 per extra conversion at 39 million visits); whole CI below it; net about −₹17 lakh a year |
| A: data flag | visitor split not exactly 50:50 (p = 0.004, 0.3% gap); lift fades after week 1 |
| p-value vs n | same +0.1 pp lift: typical p = 0.75 at 10,000 per arm, below 10⁻¹⁰ at 10 million |
| B: lift | +2.0 pp (95% CI −1.4 to +5.4), p = 0.25; break-even 1.33 pp |
| B: power | 21% at +2 pp; 80% power only above 4.8 pp |
| B: decision | P(lift > break-even) 65% (flat prior), 54% (weak prior) |
| Value of information | launch now ₹30 lakh · bigger test then decide ₹107 lakh · perfect information ₹123 lakh per year |
| Type M | significant pilots average 4.2 pp, 2.1 times the true +2.0 |
| Truth | A +0.10 pp (net −₹16 lakh a year) · B +2.0 pp (net +₹120 lakh a year); both CIs cover the truth; both p-values pointed the wrong way |

## 4. Business recommendations

Do not build A (a build cost below about ₹10 lakh would break even) · do not drop B: run a follow-up (4,000 per arm detects about 1.8 pp; about 7,000 per arm for the break-even lift) · state the break-even before the test · report effect, CI, break-even and power in every readout.

## 5. Limitations

Costs, margins and horizon are assumptions · the Bayesian result depends on a stated prior · one follow-up assumed in the value-of-information calculation · synthetic data.

## 6. Concepts learned

Significance answers "is it real", not "does it matter" · compare the CI to a pre-set threshold · p-values track sample size · a non-significant result needs its power and its CI · significant results from small studies are exaggerated · more data is worth buying when the plausible range spans worthless to valuable.

## How to reproduce

```bash
python case_studies/22_statistical_vs_practical_significance/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/22_statistical_vs_practical_significance/notebooks/01_analysis.ipynb
python case_studies/22_statistical_vs_practical_significance/src/build_presentation.py
```
