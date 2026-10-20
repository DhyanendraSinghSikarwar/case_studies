"""
SYNTHETIC DATA GENERATOR - CASE STUDY 18 (Axis Bank-style in-house credit score vs generic bureau score)
=======================================================================================================
THIS DATA IS SYNTHETIC. Bank application, transaction and collections data are confidential.

Existing bank customers who applied for (or were offered) a personal loan or credit card over 18 months.
Two information sources see DIFFERENT parts of a customer's credit risk:
  * the generic BUREAU score sees repayment history across all lenders (blank / thin for some customers)
  * the bank's INTERNAL data see salary credits, balance trends, account vintage, bounces, internal
    collections history, product holdings and spending - things a bureau never sees
Target: bad = 90+ DPD within 12 months on the new product.

Calibration anchors (reference file, Case Study 18): "2,000" credit-model attributes; "More than 40%
improvement" over generic bureau models (metric ND); 66% of PL and 79% of new card sourcing via
data-driven / pre-approved programmes. Rates are our assumptions (decision.md D-18-02). Hidden truth "_".

Output: data/cs18/applications.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42


def generate(seed=SEED, n=150_000):
    rng = np.random.default_rng(seed)
    month = rng.integers(0, 18, n)
    zb = rng.normal(0, 1, n)                      # risk component visible to the bureau (cross-lender repayment)
    zi = rng.normal(0, 1, n)                      # risk component visible only in internal data (cash flow, stability)
    product = rng.choice(["personal_loan", "credit_card"], n, p=[0.45, 0.55])
    depth = rng.choice(["thick", "thin", "no_hit"], n, p=[0.68, 0.20, 0.12])
    noise_b = np.where(depth == "thick", 35, np.where(depth == "thin", 80, np.nan))
    bureau = np.where(depth == "no_hit", np.nan, np.clip(np.round(735 + 55 * zb + rng.normal(0, 1, n) * np.nan_to_num(noise_b)), 300, 900))
    salary = np.exp(rng.normal(np.log(48000), 0.55, n) + 0.12 * zi)
    sal_credit_regular = np.clip(rng.beta(6 + 2 * zi.clip(-2, 2), 2, n), 0, 1)
    bal_trend = rng.normal(0.02 * zi, 0.08, n)                                    # 6-month balance slope (share of salary)
    casa_vintage = np.clip(rng.gamma(2.2, 3.0, n) + 0.6 * zi, 0.2, 30)
    bounces_12m = rng.poisson(np.exp(-1.4 - 0.7 * zi))
    internal_dpd = rng.poisson(np.exp(-2.2 - 0.6 * zi - 0.3 * zb))
    n_products = 1 + rng.poisson(np.exp(0.2 + 0.15 * zi))
    card_spend_ratio = np.clip(rng.gamma(2, 0.12, n) * np.exp(-0.1 * zi), 0.01, 2.5)
    cash_withdraw_share = np.clip(rng.beta(2, 6, n) - 0.04 * zi, 0, 1)
    emi_to_salary = np.clip(rng.gamma(2, 0.1, n) * np.exp(-0.15 * zi - 0.1 * zb), 0, 1.5)
    age = np.clip(rng.normal(34, 8, n), 21, 65).round()
    lg = -3.25 - 0.62 * zb - 0.62 * zi + 0.2 * (product == "credit_card") + 0.6 * np.clip(emi_to_salary - 0.4, 0, None) + 0.04 * (month >= 12) * rng.normal(1, 0.2, n)
    p_bad = expit(lg); bad = (rng.random(n) < p_bad).astype(int)
    df = pd.DataFrame({"app_id": [f"A{i:07d}" for i in range(n)], "app_month": month + 1, "product": product, "bureau_depth": depth, "bureau_score": bureau,
                       "monthly_salary": np.round(salary, -2), "salary_credit_regularity": sal_credit_regular.round(3), "balance_trend_6m": bal_trend.round(4),
                       "casa_vintage_years": casa_vintage.round(1), "bounces_12m": bounces_12m, "internal_dpd_events_24m": internal_dpd, "n_products_held": n_products,
                       "card_spend_to_salary": card_spend_ratio.round(3), "cash_withdrawal_share": cash_withdraw_share.round(3), "emi_to_salary": emi_to_salary.round(3),
                       "age": age, "bad_90dpd_12m": bad, "_p_bad": p_bad, "_zb": zb, "_zi": zi})
    # data-quality defects
    df.loc[df.sample(n=600, random_state=seed).index, "bureau_score"] = 0                  # "0" sentinel for bureau timeouts
    df.loc[df.sample(frac=0.015, random_state=seed + 1).index, "balance_trend_6m"] = np.nan
    df = pd.concat([df, df.sample(n=500, random_state=seed + 2)], ignore_index=True)
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs18"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs18", "applications.csv.gz"), index=False)
    dd = d.drop_duplicates("app_id"); print(len(dd), "applications | bad rate", dd.bad_90dpd_12m.mean().round(4)); print(dd.groupby("bureau_depth").bad_90dpd_12m.mean().round(4).to_dict())
