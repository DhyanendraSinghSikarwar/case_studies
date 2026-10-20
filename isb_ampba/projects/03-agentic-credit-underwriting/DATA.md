# DATA — Project 03: Agentic Credit Underwriting

Links checked on **2026-10-13** with `curl -s -o /dev/null -L -m 30 -A "Mozilla/5.0" -w "%{http_code}" -r 0-100 <url>` (200/206 = reachable). The German Credit file was downloaded and counted (1,000 lines, 21 space-separated fields per line).

This project uses **two kinds of data**:

1. **Real structured data** — UCI Statlog (German Credit): the applicants' attributes and the good/bad label.
2. **Synthetic documents** — bank statement CSV, application form text and bureau summary text, generated *from* each real applicant's attributes. No public dataset has real bank statements with loan outcomes (they are personal data), so this part is synthetic by necessity. Say so in the README and the memo.

---

## 1. Primary source: Statlog (German Credit Data), UCI id 144

| Item | Value |
|---|---|
| What it is | 1,000 loan applicants of a German bank (1994), 20 attributes, label good/bad. Donor: Hans Hofmann, Univ. Hamburg |
| Rows / columns | 1,000 × (20 features + class). 700 good, 300 bad (class 1 = good, 2 = bad) |
| Cost matrix (official) | Predicting *good* for an actual *bad* costs **5**; predicting *bad* for an actual *good* costs **1**. This gives the theoretical cut-off `P(bad) = 1/(1+5) = 0.167` |
| Licence | CC BY 4.0 (stated on the UCI page — confirm on the page when you cite it) |

| Purpose | URL | Status |
|---|---|---|
| Dataset page | https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data | ✔ verified 2026-10-13 |
| Zip (contains `german.data`, `german.data-numeric`, `german.doc`) | https://archive.ics.uci.edu/static/public/144/statlog+german+credit+data.zip | ✔ verified 2026-10-13 (downloaded) |
| OpenML copy `credit-g` (ARFF, with readable labels) | https://www.openml.org/data/v1/download/31/credit-g.arff | ✔ verified 2026-10-13 |
| `ucimlrepo` | https://pypi.org/project/ucimlrepo/ | ✔ verified 2026-10-13 |

### Loader (what `src/uw/data.py` does)
`german.data` is plain text, **space-separated, no header**, 21 fields per line. Read it with `sep=r"\s+"` and assign column names from the code book below.

```python
import io, zipfile, requests, pandas as pd
from uw.codes import COLUMNS            # see §2

URL = "https://archive.ics.uci.edu/static/public/144/statlog+german+credit+data.zip"
r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=120); r.raise_for_status()
with zipfile.ZipFile(io.BytesIO(r.content)) as z, z.open("german.data") as f:
    df = pd.read_csv(f, sep=r"\s+", header=None, names=COLUMNS)
df["bad"] = (df["label"] == 2).astype(int)
assert df.shape == (1000, 22) and df["bad"].sum() == 300
```
With `ucimlrepo` the features arrive as `Attribute1…Attribute20` and the target as `class`; rename them to `COLUMNS` and check the order against the first row of `german.data` (`A11 6 A34 A43 1169 A65 A75 4 A93 A101 4 A121 67 A143 A152 2 A173 1 A192 A201 1` — checking status A11, duration 6, history A34, purpose A43, amount 1169, …, age 67 … label 1).

### Pitfalls
1. **Codes are strings like `A11`.** Keep them as categoricals; decode to text only for documents and the CAM.
2. **Currency is Deutsche Marks (DM) in 1994.** The plan converts to INR with an *illustrative* `dm_to_inr = 45` (an assumption, not a market quote) so that loan sizes look like Indian retail/MSME loans. Put it in `config.yaml`.
3. **Protected/proxy attributes:** `personal_status_sex` (encodes sex and marital status) and `foreign_worker` must **not** be model inputs. Keep them in the data for the document generator and for a fairness audit.
4. **`installment_rate` (values 1–4)** is documented by UCI only as "installment rate in percentage of disposable income" (numerical, 1–4). The exact band edges are not stated there, so the mid-point ratios in `codes.py` (higher band = heavier burden) are *assumptions* of this project. Check the direction yourself: compare `default rate` by `installment_rate` in the data before relying on it.
5. **Only 1,000 rows.** Never tune on the hold-out 200; use stratified 5-fold CV on the 800 development rows.
6. **Label direction:** class 2 = bad. Map to `bad = 1` once, at load.

---

## 2. Code book (`src/uw/codes.py`)

Write this file exactly; every agent uses it. The attribute meanings follow `german.doc` in the zip — read that file once and check the codes below against it.

```python
COLUMNS = ["checking_status", "duration_months", "credit_history", "purpose", "credit_amount", "savings",
           "employment_since", "installment_rate", "personal_status_sex", "other_debtors", "residence_since",
           "property", "age", "other_installment_plans", "housing", "n_existing_credits", "job",
           "n_dependents", "telephone", "foreign_worker", "label"]
NUMERIC = ["duration_months", "credit_amount", "installment_rate", "residence_since", "age",
           "n_existing_credits", "n_dependents"]
CATEGORICAL = [c for c in COLUMNS if c not in NUMERIC and c != "label"]

CODES = {
 "checking_status": {"A11": "overdrawn (<0 DM)", "A12": "0-200 DM", "A13": ">=200 DM", "A14": "no checking account"},
 "credit_history": {"A30": "no credits taken / all paid duly", "A31": "all credits at this bank paid duly",
                    "A32": "existing credits paid duly till now", "A33": "delay in paying in the past",
                    "A34": "critical account / other credits elsewhere"},
 "purpose": {"A40": "car (new)", "A41": "car (used)", "A42": "furniture/equipment", "A43": "radio/television",
             "A44": "domestic appliances", "A45": "repairs", "A46": "education", "A47": "vacation",
             "A48": "retraining", "A49": "business", "A410": "others"},
 "savings": {"A61": "<100 DM", "A62": "100-500 DM", "A63": "500-1000 DM", "A64": ">=1000 DM", "A65": "unknown / no savings"},
 "employment_since": {"A71": "unemployed", "A72": "<1 year", "A73": "1-4 years", "A74": "4-7 years", "A75": ">=7 years"},
 "personal_status_sex": {"A91": "male divorced/separated", "A92": "female divorced/separated/married",
                         "A93": "male single", "A94": "male married/widowed", "A95": "female single"},
 "other_debtors": {"A101": "none", "A102": "co-applicant", "A103": "guarantor"},
 "property": {"A121": "real estate", "A122": "savings agreement / life insurance", "A123": "car or other",
              "A124": "unknown / no property"},
 "other_installment_plans": {"A141": "bank", "A142": "stores", "A143": "none"},
 "housing": {"A151": "rent", "A152": "own", "A153": "for free"},
 "job": {"A171": "unemployed / unskilled non-resident", "A172": "unskilled resident",
         "A173": "skilled employee / official", "A174": "management / self-employed / highly qualified"},
 "telephone": {"A191": "none", "A192": "yes"},
 "foreign_worker": {"A201": "yes", "A202": "no"},
}
REVERSE = {col: {v: k for k, v in m.items()} for col, m in CODES.items()}     # label -> code, used by the intake parser

EXCLUDED_FROM_MODEL = ["personal_status_sex", "foreign_worker"]
MODEL_NUMERIC = list(NUMERIC)
MODEL_CATEGORICAL = [c for c in CATEGORICAL if c not in EXCLUDED_FROM_MODEL]

# installment_rate 1..4 is an ordinal burden band; mid-point EMI/income ratio per band is an ASSUMPTION
INSTALLMENT_BAND_RATIO = {1: 0.15, 2: 0.225, 3: 0.30, 4: 0.40}
INSTALLMENT_BAND_EDGES = [0.1875, 0.2625, 0.35]      # ratio -> band 1..4 (midpoints between the above)

def ratio_to_band(ratio: float) -> int:
    return 1 + sum(ratio > e for e in INSTALLMENT_BAND_EDGES)
```
Every label string in `CODES[col]` must be unique within a column (the intake parser reverses the mapping) — assert it in a test.

---

## 3. Synthetic documents: design rules

Generated by `src/uw/docs_gen.py` (full code in PLAN.md M1). Rules that keep the exercise honest:

| Rule | Why |
|---|---|
| Documents are derived from the real attributes (amount, tenure, instalment band, existing credits, savings, checking status, housing, history) plus **seeded** noise (`np.random.default_rng(seed * 100_003 + idx)` per applicant) | Re-running gives identical documents |
| The `label` is **never** written into a document | Otherwise the agents could read the answer |
| Misrepresentation (income inflation, undisclosed EMI, age mismatch) is injected with a label-dependent probability: `inject_rate_bad = 0.18`, `inject_rate_good = 0.06` (overall ≈ 9.6%, matches the spec's "about 10%") | These two numbers are **assumptions** (people who later default misstate more often). Sweep them in M4 and state it in the memo |
| A separate `truth.csv` stores what was injected and the true income/EMI/age | Used only by the evaluation harness; no agent imports it |
| Income is backed out as `proposed EMI / mid-point of the instalment-rate band` (floor ₹15,000) | Ties documents to a real German Credit attribute |
| 6 monthly statements ending at `as_of = 2026-09-30` with salary (or UPI receipts for MSME), refunds and self-transfers (must not count as income), NACH EMI debits, rent, spending, ECS bounce charges (Poisson, rate depends on checking status and credit history) | Gives the statement agent something real to parse |

Statement CSV columns: `date, narration, debit, credit, balance`. Application and bureau texts are `Key: value` lines (regex-parsable).

### What the documents lack
Real documents are messy (PDF scans, inconsistent narrations, multiple accounts). These are clean text. If you want a harder variant, add OCR-like noise and alternative narration styles as a stretch goal.

---

## 4. Similar, alternative and fallback data

| Dataset | Use | Link (verified 2026-10-13) | Caveat |
|---|---|---|---|
| **South German Credit (UCI 573)** | A corrected, cleaner re-encoding of the same bank's data (original has coding errors); use as a robustness check on the PD model | Page: https://archive.ics.uci.edu/dataset/573/south+german+credit+update ✔ · Zip: https://archive.ics.uci.edu/static/public/573/south+german+credit+update.zip ✔ | Different column coding — map it yourself; do not mix with `codes.py` |
| **German Credit on OpenML (`credit-g`)** | Fallback if UCI is down; already has readable labels | https://www.openml.org/data/v1/download/31/credit-g.arff ✔ | Column names differ (`checking_status`, `credit_history`, …); class is `good`/`bad` |
| **Give Me Some Credit / Home Credit / LendingClub** | Bigger real PD models for a stretch "PD model trained on 100k+ rows" | See [Project 01 DATA.md §4](../01-credit-risk-scorecard/DATA.md) (links verified there) | Not MSME; different schema |
| **US SBA 7(a) loans (MSME-like, with charge-off outcomes)** | Real small-business loan outcomes for an MSME stretch | The data.sba.gov dataset page I tried returned 404 on 2026-10-13, so **not verified**. Search "SBA 7(a) 504 FOIA data" on https://data.sba.gov and check the current URL by hand | US data, not India; large files |
| **Policy documents for the RAG agent** | The policy in `config/credit_policy.md` is written for this project (illustrative, 15 rules). For a realistic stretch, load a public regulator document (for example RBI master directions on digital lending/credit) into the same index | Find the current document on https://www.rbi.org.in and test the URL yourself; **not verified** | Long documents need a real chunker and embeddings (backend `st`) |
| **LLM free tier** | Real (non-mock) CAM narrative and intake cross-check | Groq console: https://console.groq.com — confirm current models and limits at https://console.groq.com/docs/rate-limits before relying on any number | Free tiers change |

## 5. Licence note
UCI #144 is CC BY 4.0: cite *Hofmann, H. (1994). Statlog (German Credit Data). UCI Machine Learning Repository.* Synthetic documents and the policy file are your own work; label them synthetic/illustrative in the repo.
