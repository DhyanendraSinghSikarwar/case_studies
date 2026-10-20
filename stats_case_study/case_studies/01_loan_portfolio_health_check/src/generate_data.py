"""Generate the synthetic data for Case Study 01: Personal-loan portfolio health check.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A mid-sized Indian lender ("the Bank") has a personal-loan book of ~60,000
loans disbursed between Jan-2024 and Jun-2025. After a core-system migration,
Internal Audit re-verified a **simple random sample of 2,500 loan files** and
delivered them as an extract. The Chief Risk Officer wants a health check of the
book for the Board Risk Committee, based on that audited sample.

Two files are produced:

1. ``data/loan_audit_sample.csv``: the audited sample the analyst works with.
   It contains the data-quality problems a real extract has (duplicates,
   sentinel codes, unit errors, typos, missing values).
2. ``data/_population_answer_key.csv.gz``: the full (clean) book. **In real
   life you would never have this.** It exists only so the notebook can show
   sampling error, the Central Limit Theorem and what a 95% confidence interval
   really means, by comparing sample results with the known truth.

How each variable is generated (and why it exists)
--------------------------------------------------
disbursal_month   Month of disbursal, Jan-2024..Jun-2025, mild growth in volume.
                  Lets us check that the sample is spread over time like the book.
region            North/South/West/East with fixed shares. Used for a sample-vs-
                  book representativeness check (region mix is known from the system).
channel           Branch / Digital / DSA (direct selling agent). DSA-sourced loans
                  are riskier (well known in Indian retail lending).
employment_type   Salaried (72%) / Self-employed (28%). Self-employed income is
                  higher on average but much more variable.
customer_age      Normal(35, 8) clipped to 21-60 (lending policy age band).
monthly_income    Log-normal: money is right-skewed. Salaried median ~Rs 55k,
                  sigma 0.55; self-employed median ~Rs 60k, sigma 0.75. Small age effect.
credit_score      Bureau score 300-900. Generated as 900 - Gamma(4, 40): most
                  approved customers have high scores, a long tail to the left
                  (negative skew). 4% of applicants have no bureau history and are
                  coded -1 (about 5% of the approved book, as the score cut-off does
                  not apply to them)
                  -- a sentinel code, not a score.
loan_amount       ~ income x Lognormal(multiplier median 4.1, sigma 0.5), floored at
                  Rs 50k and capped at the Rs 15 lakh product limit. Rounded to
                  Rs 10,000, and ~35% of customers ask for a "round" amount
                  (multiple of Rs 50,000), which creates spikes, as in real data.
tenure_months     {12,18,24,36,48,60}; larger loans take longer tenures. 36 is the mode.
interest_rate     % p.a., risk-based pricing: driven by credit score, channel,
                  employment and no-hit status, plus noise. Roughly symmetric.
emi               Equated monthly instalment from the standard annuity formula.
existing_emi      Other monthly debt obligations (0 for ~30% of customers).
dti               (emi + existing_emi) / monthly_income at origination.
dpd90_12m         1 if the loan was ever 90+ days past due in its first 12 months.
                  Logistic model of score, DTI, channel, employment, no-hit and age,
                  intercept calibrated so the book-level rate is ~5.0%.

Approval filter: applicants with DTI > 0.65 or score < 650 are declined, except a
small share of policy exceptions for near-misses (DTI <= 0.80), as in real
underwriting. The book is therefore a *selected* population, not the applicant
population.

Data-quality problems injected into the audit extract only
-----------------------------------------------------------
- 6 exact duplicate rows (extract join bug)
- monthly_income missing for ~9% of self-employed and ~2% of salaried
  (income not re-verified, so missingness is NOT random)
- 4 incomes keyed as annual instead of monthly (x12)
- 5 interest rates keyed as decimals (0.155 instead of 15.5)
- 3 impossible / out-of-policy ages (3, 17, 230)

Run:  python case_studies/01_loan_portfolio_health_check/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 1
BOOK_SIZE = 60_000
SAMPLE_SIZE = 2_500
TARGET_DEFAULT_RATE = 0.050


def _annuity_emi(principal, annual_rate_pct, months):
    r = annual_rate_pct / 1200.0
    return principal * r / (1 - (1 + r) ** (-months))


def generate_applicants(rng: np.random.Generator, n: int) -> pd.DataFrame:
    months = pd.period_range("2024-01", "2025-06", freq="M")
    month_w = np.linspace(1.0, 1.4, len(months))
    df = pd.DataFrame(
        {
            "disbursal_month": rng.choice(months.astype(str), size=n, p=month_w / month_w.sum()),
            "region": rng.choice(["North", "South", "West", "East"], size=n, p=[0.30, 0.28, 0.25, 0.17]),
            "channel": rng.choice(["Branch", "Digital", "DSA"], size=n, p=[0.45, 0.35, 0.20]),
            "employment_type": rng.choice(["Salaried", "Self-employed"], size=n, p=[0.72, 0.28]),
        }
    )
    df["customer_age"] = np.clip(np.round(rng.normal(35, 8, n)), 21, 60).astype(int)

    salaried = df["employment_type"].eq("Salaried").to_numpy()
    log_median = np.where(salaried, np.log(55_000), np.log(60_000)) + 0.010 * (df["customer_age"] - 30)
    sigma = np.where(salaried, 0.55, 0.75)
    df["monthly_income"] = np.clip(np.round(np.exp(rng.normal(log_median, sigma)), -2), 15_000, None)

    score = 900 - rng.gamma(shape=4.0, scale=40.0, size=n) - 15 * df["channel"].eq("DSA")
    df["credit_score"] = np.clip(np.round(score), 300, 900).astype(int)
    no_hit = rng.random(n) < 0.04
    df.loc[no_hit, "credit_score"] = -1  # bureau "no hit" sentinel code

    multiplier = np.exp(rng.normal(np.log(4.1), 0.50, n))
    amount = np.clip(df["monthly_income"] * multiplier, 50_000, 1_500_000)
    round_ask = rng.random(n) < 0.35
    amount = np.where(round_ask, np.round(amount / 50_000) * 50_000, np.round(amount / 10_000) * 10_000)
    df["loan_amount"] = np.clip(amount, 50_000, 1_500_000).astype(int)

    small = df["loan_amount"] <= 300_000
    tenures = np.array([12, 18, 24, 36, 48, 60])
    p_small = [0.12, 0.10, 0.28, 0.34, 0.10, 0.06]
    p_large = [0.02, 0.03, 0.12, 0.36, 0.24, 0.23]
    df["tenure_months"] = np.where(small, rng.choice(tenures, n, p=p_small), rng.choice(tenures, n, p=p_large))

    eff_score = np.where(no_hit, 700, df["credit_score"])
    rate = (15.5 - 0.012 * (eff_score - 740) + 0.8 * df["channel"].eq("DSA")
            + 0.7 * (~salaried) + 1.5 * no_hit + rng.normal(0, 1.2, n))
    df["interest_rate"] = np.round(np.clip(rate, 10.5, 24.0), 2)

    df["emi"] = np.round(_annuity_emi(df["loan_amount"], df["interest_rate"], df["tenure_months"]))
    has_debt = rng.random(n) < 0.70
    df["existing_emi"] = np.round(np.where(has_debt, df["monthly_income"] * rng.beta(2, 9, n), 0), -2)
    df["dti"] = np.round((df["emi"] + df["existing_emi"]) / df["monthly_income"], 4)
    df["_no_hit"] = no_hit
    df["_eff_score"] = eff_score
    return df


def approve(rng: np.random.Generator, df: pd.DataFrame) -> pd.DataFrame:
    """Underwriting filter with a few policy exceptions: the book is a selected population."""
    fails_policy = (df["dti"] > 0.65) | ((df["credit_score"] < 650) & ~df["_no_hit"])
    # Exceptions are granted only to near-misses (DTI up to 0.80), never to extreme cases.
    exception = (rng.random(len(df)) < 0.08) & (df["dti"] <= 0.80)
    return df[~fails_policy | exception].reset_index(drop=True)


def add_default_flag(rng: np.random.Generator, df: pd.DataFrame) -> pd.DataFrame:
    linear = (-0.013 * (df["_eff_score"] - 740) + 2.4 * (df["dti"] - 0.35)
              + 0.45 * df["channel"].eq("DSA") + 0.35 * df["employment_type"].eq("Self-employed")
              + 0.50 * df["_no_hit"] + 0.30 * (df["customer_age"] < 25))
    # Calibrate the intercept so the book-level default rate equals the target (bisection).
    lo, hi = -10.0, 2.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if (1 / (1 + np.exp(-(mid + linear)))).mean() > TARGET_DEFAULT_RATE:
            hi = mid
        else:
            lo = mid
    p = 1 / (1 + np.exp(-(lo + linear)))
    df["dpd90_12m"] = (rng.random(len(df)) < p).astype(int)
    return df


def build_book(rng: np.random.Generator) -> pd.DataFrame:
    applicants = generate_applicants(rng, int(BOOK_SIZE * 1.6))
    book = approve(rng, applicants).iloc[:BOOK_SIZE].copy()
    book = add_default_flag(rng, book)
    book = book.sort_values("disbursal_month", kind="stable").reset_index(drop=True)
    book.insert(0, "loan_id", [f"PL{100000 + i}" for i in range(len(book))])
    return book.drop(columns=["_no_hit", "_eff_score"])


def draw_audit_sample(rng: np.random.Generator, book: pd.DataFrame) -> pd.DataFrame:
    """Simple random sample, done the way it is done in SQL: give every loan a U(0,1)
    random key and keep the 2,500 smallest keys. Every loan has the same chance."""
    keys = rng.uniform(0, 1, len(book))
    return book.iloc[np.argsort(keys)[:SAMPLE_SIZE]].reset_index(drop=True)


def inject_quality_issues(rng: np.random.Generator, sample: pd.DataFrame) -> pd.DataFrame:
    s = sample.copy()
    s["monthly_income"] = s["monthly_income"].astype(float)
    s["customer_age"] = s["customer_age"].astype(float)

    # Income not re-verified: missing more often for self-employed (not MCAR).
    p_miss = np.where(s["employment_type"].eq("Self-employed"), 0.09, 0.02)
    s.loc[rng.random(len(s)) < p_miss, "monthly_income"] = np.nan

    candidates = s.index[s["monthly_income"].notna()]
    annual_idx = rng.choice(candidates, 4, replace=False)
    s.loc[annual_idx, "monthly_income"] *= 12  # keyed as annual income

    rate_idx = rng.choice(s.index.difference(annual_idx), 5, replace=False)
    s.loc[rate_idx, "interest_rate"] = (s.loc[rate_idx, "interest_rate"] / 100).round(4)

    age_idx = rng.choice(s.index.difference(annual_idx.tolist() + rate_idx.tolist()), 3, replace=False)
    s.loc[age_idx, "customer_age"] = [3, 17, 230]

    dup = s.sample(6, random_state=int(rng.integers(1e9)))
    s = pd.concat([s, dup], ignore_index=True)
    order = rng.permutation(len(s))  # extracts are not sorted nicely
    return s.iloc[order].reset_index(drop=True)


def main() -> None:
    paths = case_paths(CASE_DIR)
    rng = rng_for_case(CASE_NUMBER)
    book = build_book(rng)
    sample = draw_audit_sample(rng, book)
    extract = inject_quality_issues(rng, sample)

    book.to_csv(paths["data"] / "_population_answer_key.csv.gz", index=False, compression="gzip")
    extract.to_csv(paths["data"] / "loan_audit_sample.csv", index=False)

    print(f"Book: {len(book):,} loans | default rate {book['dpd90_12m'].mean():.3%} | "
          f"mean amount {book['loan_amount'].mean():,.0f} | median {book['loan_amount'].median():,.0f}")
    print(f"Audit extract: {len(extract):,} rows (incl. duplicates)")


if __name__ == "__main__":
    main()
