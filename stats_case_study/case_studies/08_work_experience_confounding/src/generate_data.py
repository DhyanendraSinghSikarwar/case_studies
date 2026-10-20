"""Generate the synthetic data for Case Study 08: Why did "work experience" stop mattering?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A lender pre-approves personal loans for salaried customers using an INCOME ESTIMATION
model (many applicants cannot share payslips). For 6,000 salaried customers we have the
verified monthly salary (from salary credits in bank statements) plus their profile.
The old model used work experience; the new model adds job grade, and experience
"stopped mattering". Credit Policy wants to know why, and which variables to keep.

File: data/salaried_customers.csv: 6,000 customers.
  customer_id, age, education (ordinal: Diploma < Graduate < Postgraduate < Professional),
  years_experience, years_at_current_employer, job_grade (ordinal, 1 = Executive ... 5 = Director+),
  employer_category (nominal: Large Indian corporate / MNC / Government-PSU / SME / Startup),
  metro_city (0/1), grade_available (1 = grade verified through payroll partner),
  monthly_salary (Rs, verified)

True data-generating process (causal story, log scale)
------------------------------------------------------
experience  -> promotions -> job_grade -> salary   (experience works MAINLY through grade)
education   -> job_grade and education -> salary   (qualification pay premium)
employer    -> salary  and  employer -> metro      (MNCs/startups are concentrated in metros)
tenure (years at current employer): at the SAME total experience, people who have not
             switched jobs earn less (the "switching premium" they did not collect).

latent grade = 0.17 * experience + 0.45 * education_level + employer shift + Normal(0, 0.75)
               (cut into 5 grades)
log(salary)  = 10.10 + 0.30 * grade + 0.006 * experience + 0.09 * education_level
               - 0.040 * tenure + employer effect + 0.00 * metro + Normal(0, 0.22)
employer effect (vs Large Indian corporate): MNC +0.22, Government-PSU -0.05, SME -0.18, Startup +0.08

So:
* Experience has a large TOTAL effect but a small DIRECT effect once grade is held fixed
  (grade is a MEDIATOR, not a confounder).
* Metro has NO direct effect; it looks important only because of employer type (CONFOUNDING).
* Tenure is almost uncorrelated with salary on its own, but clearly negative once
  experience is held fixed (SUPPRESSION).
* Education is masked: in this customer base, postgraduate and professional customers are
  younger (a campus-hiring campaign brought them in), so they have less experience. On its
  own, education looks unimportant; at the same experience, it matters (a variable hidden
  by a confounder).
* grade_available is unrelated to salary (payroll-partner coverage is random by design).

Run:  python case_studies/08_work_experience_confounding/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 8
N = 6_000
EDUCATION = ["Diploma", "Graduate", "Postgraduate", "Professional"]
STUDY_YEARS = np.array([3.0, 3.5, 5.5, 6.0])           # after age 18
MEAN_AGE = np.array([36.0, 35.0, 28.5, 29.5])          # campus campaign: younger postgraduates
EMPLOYERS = ["Large Indian corporate", "MNC", "Government-PSU", "SME", "Startup"]
EMPLOYER_SALARY = np.array([0.0, 0.22, -0.05, -0.18, 0.08])
EMPLOYER_GRADE = np.array([0.0, 0.10, 0.0, -0.15, 0.10])
METRO_PROB = np.array([0.55, 0.85, 0.35, 0.35, 0.90])


def generate(rng: np.random.Generator) -> pd.DataFrame:
    edu = rng.choice(4, N, p=[0.15, 0.48, 0.27, 0.10])
    emp = rng.choice(5, N, p=[0.28, 0.22, 0.15, 0.25, 0.10])
    age = np.clip(np.round(rng.normal(MEAN_AGE[edu], 6.5)), 22, 58).astype(int)
    start_age = 18 + STUDY_YEARS[edu] + rng.exponential(0.8, N)
    gap = np.where(rng.random(N) < 0.25, rng.exponential(1.5, N), 0.0)
    experience = np.clip(np.round(age - start_age - gap, 1), 0.0, None)
    # Share of the career spent at the current employer.
    tenure = np.round(experience * rng.beta(1.6, 2.2, N), 1)
    metro = (rng.random(N) < METRO_PROB[emp]).astype(int)

    latent = 0.17 * experience + 0.45 * edu + EMPLOYER_GRADE[emp] + rng.normal(0, 0.75, N)
    grade = np.digitize(latent, [1.6, 2.9, 4.2, 5.4]) + 1   # 1..5

    log_sal = (10.10 + 0.30 * grade + 0.006 * experience + 0.09 * edu - 0.040 * tenure
               + EMPLOYER_SALARY[emp] + 0.0 * metro + rng.normal(0, 0.22, N))
    salary = np.round(np.exp(log_sal), -2).astype(int)
    grade_available = (rng.random(N) < 0.6).astype(int)

    return pd.DataFrame({
        "customer_id": [f"SAL8{100000 + i}" for i in range(N)],
        "age": age,
        "education": np.array(EDUCATION)[edu],
        "years_experience": experience,
        "years_at_current_employer": tenure,
        "job_grade": grade,
        "employer_category": np.array(EMPLOYERS)[emp],
        "metro_city": metro,
        "grade_available": grade_available,
        "monthly_salary": salary,
    })


def main() -> None:
    paths = case_paths(CASE_DIR)
    df = generate(rng_for_case(CASE_NUMBER))
    df.to_csv(paths["data"] / "salaried_customers.csv", index=False)
    print(df.describe().round(2))


if __name__ == "__main__":
    main()
