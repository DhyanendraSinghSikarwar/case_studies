"""
SYNTHETIC DATA GENERATOR - CASE STUDY 13 (alternate-data credit scoring for thin-file millennials)
================================================================================================
THIS DATA IS SYNTHETIC. The study's lender data is private (SSRN 3507827).

150,000 small-ticket loan applications (Jan 2023 - Dec 2024) from young, thin-file applicants with
four feature families: bureau, "deep financial" (income, employment, existing EMIs), mobile/social
footprint (installed apps, social logins, OS) and deep call-log features. A historical approval
policy (bureau + income) approves ~65%; outcomes exist ONLY for approved loans in the observed data.
Because this is a simulation we also keep the hidden outcome of DENIED applicants, which lets the
notebook validate reject-inference methods - something real data never allows.

Calibration anchors (reference file, Case Study 13): 417,578 applications, 272,931 approved (65.4%);
loans Rs 10k-200k, 15-180 days, average Rs 22,174; average CIBIL 634; default ~13.5%; AUCs bureau 59%,
footprint 60.4%, footprint + call logs 66%, deep mobile 74% vs deep financial 59%; Facebook login 27%,
LinkedIn 2.1%. Loadings are tuned to reproduce that ordering (decision.md D-13-02).

Output: data/cs13/applications.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
N = 150_000


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    qb, qf, qc, qs = (rng.normal(0, 1, N) for _ in range(4))     # latent: bureau-, footprint-, call-, financial-related
    app_date = pd.Timestamp("2023-01-01") + pd.to_timedelta(rng.integers(0, 730, N), unit="D")
    age = np.clip(np.round(rng.normal(28, 4.5, N)), 21, 45)
    thin = rng.random(N) < 0.22
    bureau = np.where(thin, np.nan, np.clip(np.round(634 + 55 * (0.75 * qb + 0.66 * rng.normal(0, 1, N))), 300, 900))
    income = np.round(np.exp(np.log(28_000) + 0.35 * (0.4 * qs + 0.92 * rng.normal(0, 1, N))), -2)
    emp = rng.choice(["salaried", "self-employed", "gig/freelance"], N, p=[0.62, 0.23, 0.15])
    existing_emi = np.round(np.clip(income * rng.beta(1.2, 6, N) * (1 - 0.15 * qs), 0, None), -2)
    # mobile / social footprint
    ios = rng.random(N) < expit(-2.1 + 0.5 * qf + 0.25 * np.log(income / 28_000))
    fb = rng.random(N) < expit(-1.0 + 0.10 * qf)
    li = rng.random(N) < expit(-4.2 + 0.75 * qf)
    n_fin_apps = rng.poisson(np.exp(0.8 + 0.15 * qf))
    n_loan_apps = rng.poisson(np.exp(0.4 - 0.45 * qf))
    dating = rng.random(N) < expit(-2.0 - 0.15 * qf)
    n_ecom = rng.poisson(np.exp(1.2 + 0.05 * qf))
    n_travel = rng.poisson(np.exp(-0.2 + 0.35 * qf))
    n_contacts = rng.poisson(np.exp(5.6 + 0.10 * qf + 0.2 * rng.normal(0, 1, N)))
    n_sms = rng.poisson(np.exp(4.0 - 0.05 * qf))
    # deep call logs
    out_min = np.round(np.exp(np.log(600) + 0.40 * qc + 0.5 * rng.normal(0, 1, N)))
    missed_ratio = np.round(np.clip(expit(-1.3 - 0.55 * qc + 0.4 * rng.normal(0, 1, N)), 0, 1), 3)
    distinct_called = rng.poisson(np.exp(3.4 + 0.25 * qc))
    night_share = np.round(np.clip(expit(-2.4 - 0.35 * qc + 0.4 * rng.normal(0, 1, N)), 0, 1), 3)
    amount = np.clip(np.round(np.exp(rng.normal(np.log(17_000), 0.6, N)), -2), 10_000, 200_000)
    tenure = rng.choice([15, 30, 60, 90, 120, 180], N, p=[0.10, 0.30, 0.20, 0.20, 0.10, 0.10])
    # true default (observed only if approved)
    z = (-2.20 - 0.50 * qb - 0.35 * qs - 0.60 * qf - 0.85 * qc + 0.25 * thin + 0.15 * (tenure >= 120)
         + 0.20 * np.log(amount / 17_000) + 0.4 * rng.normal(0, 1, N))
    default_true = (rng.random(N) < expit(z)).astype(int)
    # historical approval policy: bureau + income (it never saw the phone data)
    approve = np.where(thin, income >= 30_000, (bureau >= 590) & (income >= 18_000))
    approve = approve | (rng.random(N) < 0.05)                              # manual overrides
    df = pd.DataFrame({
        "application_id": [f"AP{i:07d}" for i in range(1, N + 1)], "application_date": app_date, "age": age,
        "bureau_score": bureau, "monthly_income_inr": income, "employment": emp, "existing_emi_inr": existing_emi,
        "loan_amount_inr": amount, "tenure_days": tenure,
        "os_ios": ios.astype(int), "facebook_login": fb.astype(int), "linkedin_login": li.astype(int),
        "n_financial_apps": n_fin_apps, "n_other_loan_apps": n_loan_apps, "has_dating_app": dating.astype(int),
        "n_ecommerce_apps": n_ecom, "n_travel_apps": n_travel, "n_contacts": n_contacts, "n_sms_30d": n_sms,
        "outgoing_call_minutes_30d": out_min, "missed_call_ratio": missed_ratio, "distinct_numbers_called_30d": distinct_called,
        "night_call_share": night_share,
        "approved": approve.astype(int),
        "defaulted": np.where(approve, default_true, np.nan),                  # observed label
        "_default_if_funded": default_true,                                    # hidden truth (simulation only)
    }).sort_values("application_date").reset_index(drop=True)
    # data-quality issues
    df.loc[df.sample(n=1500, random_state=seed).index, ["outgoing_call_minutes_30d", "missed_call_ratio", "distinct_numbers_called_30d", "night_call_share"]] = np.nan  # call-log permission denied
    df.loc[df.sample(n=60, random_state=seed + 1).index, "monthly_income_inr"] = 9_999_999        # placeholder income
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs13"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs13", "applications.csv.gz"), index=False)
    print(len(d), "approval", round(d.approved.mean(), 3), "default among approved", round(d.defaulted.mean(), 3),
          "avg bureau", round(d.bureau_score.mean(), 1), "true default denied", round(d.loc[d.approved == 0, "_default_if_funded"].mean(), 3))
