# Case Study 02 — Do Higher Earners Default Less?

| | |
|---|---|
| **Domain** | Retail lending: credit risk policy |
| **Difficulty** | Beginner |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Joint / marginal / conditional probability · independence · confusion of the inverse · Student vs Welch t-test · t-test on logs · Mann-Whitney U · bootstrap median difference · chi-square test of independence · trend test · Cramér's V · risk difference / risk ratio / odds ratio · policy simulation with bootstrap and sensitivity analysis |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

---

## 1. Business problem

The current personal-loan policy requires a verified monthly income of at least **₹20,000**. The Head of Risk Policy
writes:

> *"Our collections team keeps telling us that low-income customers are the problem. I'd like to raise the
> minimum income to ₹30,000 from next quarter. Before I take this to the Credit Committee, can you confirm from
> data that higher earners default less, tell me by how much, and tell me whether raising the floor is worth it?"*

## 2. Business questions

1. Is the default rate higher for lower-income customers?
2. How different are the incomes of defaulters and repayers?
3. Is the relationship real, or could it be chance?
4. How big is the effect, in business terms?
5. Would a ₹30,000 floor create value?

## 3. Dataset

`data/loan_performance_2024.csv`: **6,000 personal loans** disbursed in 2024, each observed for 12 months (5,941 after
excluding 59 loans with missing or zero income).

| Variable | Type | Notes |
|---|---|---|
| `loan_id` | ID | |
| `city_tier` | Categorical | Metro / Tier-2 / Tier-3 |
| `employment_type` | Categorical | Salaried / Self-employed |
| `monthly_income` | Numeric (₹) | Right-skewed; 7 zeros (= "not captured") and 52 blanks |
| `credit_score` | Numeric | Correlated with income (ρ ≈ 0.40) |
| `loan_amount` | Numeric (₹) | Used for the financial impact |
| `dti` | Ratio | Correlated with income (ρ ≈ −0.38) |
| `defaulted` | Binary | **Target**: 90+ DPD within 12 months (6.9%) |

Generation logic, including the true data-generating model and why income is linked to default both directly and
through score and DTI, is in [`src/generate_data.py`](src/generate_data.py).

## 4. Statistical questions

| Business question | Statistical question |
|---|---|
| Do low earners default more? | Is P(default \| income band) the same in every band? |
| How different are incomes? | Do the income distributions differ? In means, in typical (geometric-mean) values, in ranks? |
| Real or chance? | Are income band and default independent? |
| How big? | Risk difference, risk ratio, Cramér's V, ratio of geometric means, probability of superiority |
| Is the floor worth it? | Expected net value of excluding < ₹30k loans, with bootstrap CI and sensitivity to LGD and margin |

## 5. Methods (and why)

| Method | Why | Rejected alternative |
|---|---|---|
| Contingency-table probabilities | The business question is a conditional probability; the belief came from the inverse | — |
| **Welch's t-test** | Means differ in variance (ratio ≈ 2.7) and group sizes are very unequal | Student's t: pooled SE is wrong here (≈ 50% too large) |
| **t-test on log income** | Gives "typical income is X% lower", a natural ratio for money | — |
| **Mann-Whitney U** | Robust rank comparison with an intuitive effect size | Treating it as a "median test" (it is not, since the shapes differ) |
| **Chi-square test of independence** + trend test | Band × default table; all expected counts ≥ 48; bands are ordered | Fisher's exact (unnecessary with large counts) |
| Risk ratio / difference / odds ratio | Absolute and relative effects for the Committee | Reporting p-values only |
| Policy simulation + bootstrap + sensitivity grid | Turns the association into a decision; tests the assumptions | Deciding from the risk ratio alone |

## 6. Key findings

| Finding | Estimate (95% CI) |
|---|---|
| Default rate by income band | 13.8% (₹20–25k) → 9.1% → 6.0% → 3.8% → 2.0% (≥ ₹100k) |
| Chi-square test of independence | χ² = 116, df = 4, p ≈ 4 × 10⁻²⁴; Cramér's V = 0.14 (modest strength) |
| Mean income gap (defaulted − repaid) | −₹17,400 (−₹19,900 to −₹14,800); Welch t = −13.2 |
| Typical (geometric-mean) income ratio | 0.74 (0.70 to 0.78): defaulters' typical income is 26% lower |
| P(random defaulter out-earns random repayer) | 0.34 (Mann-Whitney p < 0.001) |
| Below vs above ₹30k | 13.0% vs 5.0%; risk ratio 2.6 (2.1–3.1); risk difference 8 pp |
| Inverse probabilities | P(default \| < ₹30k) = 13% but P(< ₹30k \| default) = 43% |
| ₹30k floor on the 2024 cohort | 175 defaults avoided vs 1,171 good customers lost (≈ 7 : 1); **net ≈ −₹0.29 crore** (−₹0.48 to −₹0.08 crore) |
| Break-even | The floor pays only if the lifetime margin on good loans is below ≈ 9.5% (base LGD 65%) |
| Confounding flag | Within credit-score bands the income gradient is flatter, so income partly proxies score and DTI |

## 7. Business recommendations

1. **Keep the ₹20,000 floor**: do not raise it to ₹30,000 on current evidence. This is *conditional on the margin*.
   If Finance confirms a lifetime margin below ~9.5%, re-examine.
2. Use income through **risk-based pricing, loan sizing or tenure**, not a hard exclusion.
3. Build a **multivariable risk model** (income + score + DTI + employment) before adding any income rule.
4. Correct the framing "most defaulters are low-income" → "most low-income customers repay (87%)".

## 8. Limitations

- Approved loans only: nothing can be said about applicants below ₹20k (reject-inference problem).
- Income is confounded with credit score and DTI; estimates are total associations.
- LGD and margin are book-wide assumptions; the decision is sensitive to the margin.
- Static counterfactual (excluded customers vanish, nothing else changes); one cohort; synthetic data.

## 9. Concepts learned

Joint, marginal and conditional probability · independence · confusion of the inverse · Bayes' theorem (preview) ·
Student vs Welch t-test · Welch-Satterthwaite df · Brown-Forsythe/Levene test · log-scale comparison and geometric
means · Mann-Whitney U and its estimand · probability of superiority · rank-biserial correlation · bootstrap CI for
median difference · chi-square test of independence · expected counts · standardised residuals · chi-square
distribution · Cramér's V · trend test · risk difference / ratio · odds ratio · confirmatory vs exploratory ·
statistical evidence vs policy value · sensitivity analysis · selection bias · confounding (preview).

## How to reproduce

```bash
python case_studies/02_income_and_default/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/02_income_and_default/notebooks/01_analysis.ipynb
python case_studies/02_income_and_default/src/build_presentation.py
```
