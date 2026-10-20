# DATA — Project 01: Credit Risk Scorecard & Limit Engine

All links below were checked on **2026-10-13** with
`curl -s -o /dev/null -L -m 30 -A "Mozilla/5.0" -w "%{http_code}" -r 0-100 <url>` (200 or 206 = reachable).
Row counts and value counts in section 3 come from a file I downloaded and counted myself, not from memory.

---

## 1. Primary source: UCI "Default of Credit Card Clients" (id 350)

| Item | Value |
|---|---|
| What it is | Real card-level data from one Taiwanese issuer, April–September 2005 (UCI documentation: repayment status, bill and payment amounts for April–September 2005). Target = default in the *next* month after the last observed month. |
| Authors | I-Cheng Yeh and Che-hui Lien. Paper: *The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients*, Expert Systems with Applications, 2009, DOI 10.1016/j.eswa.2007.12.020 |
| Dataset DOI | 10.24432/C55S3H |
| Licence | **CC BY 4.0** (stated on the UCI dataset page). Attribute the authors in your README. |
| Size | 30,000 rows x 23 features + target (UCI metadata: 30000 instances, 23 features, no missing values) |
| Currency | New Taiwan dollars (NT$). The plan converts to INR with `fx_ntd_inr` only for business outputs. |

**Links**

| Purpose | URL | Status |
|---|---|---|
| Dataset page | https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients | ✔ verified 2026-10-13 |
| Short dataset page | https://archive.ics.uci.edu/dataset/350 | ✔ verified 2026-10-13 |
| Direct zip (contains one `.xls`, 5,539,328 bytes unzipped; zip is 5.5 MB) | https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip | ✔ verified 2026-10-13 (downloaded and opened) |
| `ucimlrepo` package | https://pypi.org/project/ucimlrepo/ | ✔ verified 2026-10-13 |

### Loader code

Primary route (what the master plan asks for), with an automatic fallback to the direct zip because the `ucimlrepo` API is occasionally slow or down. This is the same code as `src/credit/data.py` in PLAN.md.

```python
import io, zipfile
import pandas as pd
import requests

UCI_ZIP = "https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip"

def from_ucimlrepo() -> pd.DataFrame:
    from ucimlrepo import fetch_ucirepo
    d = fetch_ucirepo(id=350)
    X, y = d.data.features.copy(), d.data.targets.copy()      # ID is the index column, so it is not in X
    print(list(X.columns)[:3], list(y.columns))                # expect ['X1', 'X2', 'X3'] ['Y']
    X.columns = (["LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE"]
                 + ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]
                 + [f"BILL_AMT{i}" for i in range(1, 7)] + [f"PAY_AMT{i}" for i in range(1, 7)])
    X["default"] = y.iloc[:, 0].to_numpy()
    return X

def from_zip() -> pd.DataFrame:
    r = requests.get(UCI_ZIP, headers={"User-Agent": "Mozilla/5.0"}, timeout=120)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        name = [n for n in z.namelist() if n.lower().endswith(".xls")][0]
        df = pd.read_excel(z.open(name), header=1)             # row 0 = X1..X23,Y ; row 1 = real names ; needs xlrd
    return df.drop(columns=["ID"]).rename(columns={"default payment next month": "default"})
```

`pip install xlrd` is required for the `.xls` route (`pandas` cannot read legacy `.xls` without it). Cache the result once as `data/raw/uci350.parquet` (needs `pyarrow`).

### Schema (24 columns in the file: ID + 23 features + target)

| Column (file name) | UCI code | Meaning | Observed range / values |
|---|---|---|---|
| `ID` | — | Row id | 1..30000, unique. Drop it. |
| `LIMIT_BAL` | X1 | Credit limit incl. family supplementary credit (NT$) | 10,000 – 1,000,000 |
| `SEX` | X2 | 1 = male, 2 = female | 11,888 male / 18,112 female |
| `EDUCATION` | X3 | 1 grad school, 2 university, 3 high school, 4 others | 0:14, 1:10,585, 2:14,030, 3:4,917, 4:123, 5:280, 6:51 (0, 5, 6 are **undocumented**) |
| `MARRIAGE` | X4 | 1 married, 2 single, 3 others | 0:54 (undocumented), 1:13,659, 2:15,964, 3:323 |
| `AGE` | X5 | Years | 21 – 79 |
| `PAY_0` | X6 | Repayment status **September** (most recent) | -2..8 |
| `PAY_2` … `PAY_6` | X7–X11 | Repayment status August … April | -2..8 |
| `BILL_AMT1` … `BILL_AMT6` | X12–X17 | Bill statement amount, September … April (NT$) | can be negative |
| `PAY_AMT1` … `PAY_AMT6` | X18–X23 | Amount paid in September … April (NT$) | 0 – 1,684,259 |
| `default payment next month` | Y | 1 = defaulted next month | 0: 23,364 / 1: 6,636 |

Month alignment matters: `BILL_AMT1` and `PAY_AMT1` are September. The payment you make in September settles the **August** bill, so the right ratio is `PAY_AMT_i / BILL_AMT_{i+1}`.

---

## 2. What the numbers should look like after loading

Run these checks in `src/credit/validate.py` (PLAN.md M1 has the code). **All values below were counted on the downloaded file.**

| Check | Expected |
|---|---|
| `df.shape` after dropping `ID` | `(30000, 24)` |
| Nulls | 0 |
| `ID` unique | True |
| Default rate | 6,636 / 30,000 = **22.12%** |
| `PAY_0` value counts | -2: 2,759; -1: 5,686; 0: 14,737; 1: 3,688; 2: 2,667; 3: 322; 4: 76; 5: 26; 6: 11; 7: 9; 8: 19 |
| Rows with a negative `BILL_AMT1` | 590 |
| Rows with a negative bill in *any* of the six months | 1,930 (credit balances; **keep them**, do not drop) |
| Exact duplicate rows ignoring `ID` | 35 (reference repo R1 drops them; this plan keeps them and says so — dropping 35 rows changes nothing material, but pick one and write it down) |
| After a 60/20/20 stratified split with `random_state=42` (sklearn `train_test_split` twice, see PLAN.md) | train 18,000 rows / 3,982 defaults; valid 6,000 / 1,327; test 6,000 / 1,327 (22.12% in each) |

If your split counts differ by one or two defaults, a different scikit-learn version is the likely reason; the sizes (18,000 / 6,000 / 6,000) must be exact.

---

## 3. Pitfalls specific to this file

1. **`PAY_0` has no `PAY_1`.** The column jumps from `PAY_0` to `PAY_2`. Do not "fix" it by renaming unless you rename consistently everywhere (the plan keeps the original names).
2. **`PAY_*` codes -2 and 0 are not in the UCI documentation** (which lists only -1 = paid duly, 1..9 = months late). Common reading: -2 = no consumption, -1 = paid in full, 0 = paid the minimum / revolving. Treat anything ≤ 0 as "not late" when you count delays; do not treat the column as a clean ordinal number in a linear model without checking the default rate per code (-2 and 0 have lower default rates than 1).
3. **Undocumented category codes**: `EDUCATION` 0/5/6 and `MARRIAGE` 0. The master plan maps EDUCATION {0,5,6} → 4 and MARRIAGE 0 → 3. Do it in `clean()` and test it.
4. **The first data row of the `.xls` is a code row** (`X1 … X23, Y`). `pd.read_excel(..., header=1)` is required; with the default `header=0` every column becomes `object`.
5. **Target name has spaces** (`default payment next month`). Rename once, at load.
6. **Negative bills are real** (customer overpaid). `utilisation = BILL_AMT / LIMIT_BAL` can be negative; clip only where a feature definition says so.
7. **Random split ≠ out-of-time.** The file has no calendar column beyond the six months, so you cannot do an out-of-time split. State this as a limitation. (`ID` shows no strong trend in default rate across the file — five equal chunks range from 20.3% to 24.3% — but do not use it as a feature.)
8. **`ucimlrepo` returns `X1..X23` and `Y`**, not the real names, and `ID` is dropped as the index column. Rename immediately and assert the column list.
9. **`fetch_ucirepo` needs the internet each call.** Cache to parquet and read the parquet afterwards, so tests and CI never hit the network.
10. **Do not commit `data/raw/`.** The file is CC BY 4.0 so redistribution is allowed, but the plan's `.gitignore` keeps raw data out; commit only the 1,500-row test fixture.

---

## 4. Similar, alternative and fallback datasets

| Dataset | How to use it here | Access (verified 2026-10-13) | What it lacks |
|---|---|---|---|
| **Same data, OpenML mirror** (OpenML id 42477, `default-of-credit-card-clients`, licence listed as CC0; 30,000 instances, 24 features; classes 23,364 / 6,636) | **Fallback** when UCI is down. `sklearn.datasets.fetch_openml(data_id=42477, as_frame=True)` | ARFF: https://www.openml.org/data/v1/download/21854402/default-of-credit-card-clients.arff ✔ verified; metadata: https://www.openml.org/api/v1/json/data/42477 ✔ verified | Same data, so no new information. Column names on OpenML differ (check `df.columns` first). |
| **Same data, Hugging Face mirror** (`scikit-learn/credit-card-clients`, one CSV `UCI_Credit_Card.csv`, licence cc0-1.0 on the card) | Second fallback; plain CSV | https://huggingface.co/datasets/scikit-learn/credit-card-clients ✔ verified; file: https://huggingface.co/datasets/scikit-learn/credit-card-clients/resolve/main/UCI_Credit_Card.csv ✔ verified | Column names follow the Kaggle version (`default.payment.next.month`, `PAY_0`, `ID`). I did not download this file, so check the header before relying on it. |
| **Give Me Some Credit** (OpenML id 46929; 150,000 rows, 11 columns, 10,026 positives = 6.7%; 33,655 missing values: `MonthlyIncome` 29,731 and `NumberOfDependents` 3,924; licence "Public"; original Kaggle 2011 competition) | **External validation / second portfolio.** Run the same WOE → logit scorecard code on it to show the pipeline is not tuned to Taiwan data; report AUC separately and do **not** mix it with the Taiwan test metrics. Also useful for a PSI demonstration (score the GMSC population with a Taiwan-trained model, expect a huge PSI, which proves the monitor works). | ARFF (7.2 MB): https://www.openml.org/data/v1/download/22125240/GiveMeSomeCredit.arff ✔ verified (downloaded and counted); `fetch_openml(data_id=46929, as_frame=True)` | Different features (no 6-month history), different definition (serious delinquency in 2 years), US consumer population, 2011. Sentinel codes 96/98 appear in the "times past due" columns, and `DebtRatio` has absurd values (up to 329,664 when income is missing). Target is the first column. |
| **Statlog German Credit** (UCI 144 / OpenML 31 `credit-g`, 1,000 rows, 700 good / 300 bad) | Tiny sanity set for unit tests only; the master plan's project 03 uses it. Do not use for project 01 results. | OpenML: https://www.openml.org/data/v1/download/31/credit-g.arff ✔ verified | Too small for monotonic WOE stability; 1994 Germany. |
| **Home Credit Default Risk** (Hugging Face mirror `mohameddhameem/home-credit-default-risk`, licence apache-2.0 on the HF card; original is a Kaggle competition with its own rules) | **Stretch goal**: a much richer application + bureau + instalment-history dataset to practise multi-table feature engineering. | Card: https://huggingface.co/datasets/mohameddhameem/home-credit-default-risk ✔ verified; example file (57 MB parquet): https://huggingface.co/datasets/mohameddhameem/home-credit-default-risk/resolve/main/application_train_dated/train-00000-of-00001.parquet ✔ verified (range request) | Hundreds of MB across tables; third-party mirror, so check the competition terms before redistributing anything. I did not download it. |
| **LendingClub accepted loans 2007–2018** (HF `codesignal/lending-club-loan-accepted`, one 1.68 GB CSV, licence cc0-1.0 on the card) | **Stretch goal / calibration**: real interest rates by grade and real charge-off outcomes to sanity-check the `margin` and `LGD` assumptions in `config.yaml` (e.g. compare average `int_rate` by `grade`, and `recoveries` vs `funded_amnt` on charged-off loans). | Card: https://huggingface.co/datasets/codesignal/lending-club-loan-accepted ✔ verified; file: https://huggingface.co/datasets/codesignal/lending-club-loan-accepted/resolve/main/accepted_2007_to_2018Q4.csv ✔ verified (range request; I read only the header row, which starts `id,member_id,loan_amnt,funded_amnt,...,int_rate,installment,grade,...,annual_inc,...,loan_status,...,recoveries`). **Stream it, do not download 1.7 GB**: `pd.read_csv(url, nrows=200_000, usecols=[...])`. | US unsecured instalment loans, not revolving cards; no monthly repayment history. Use only to bracket assumptions, not to train. |

### Where the economic assumptions come from (be honest in the README)

`margin = 0.18`, `LGD = 0.65`, `EAD = LIMIT_BAL x avg_util` and the NT$ → INR rate are **assumptions from the master plan**, not facts in the Taiwan data. The dataset has no interest income, fees, recoveries or loss amounts. That is exactly why the plan sweeps LGD x margin in a sensitivity table. If you want an external anchor for LGD, use the LendingClub fields above on charged-off loans (loss = `funded_amnt` minus `recoveries`), and say it is a US instalment-loan proxy.

---

## 5. Licence and citation note

- UCI #350: CC BY 4.0. Cite Yeh & Lien (2009) and the DOI above; say "Taiwan, 2005" in the README.
- OpenML mirrors and the HF mirrors carry their own licence labels (CC0 / "Public" / Apache-2.0 / CC0). Those labels are copied from the mirror pages; they do not override the original owners' terms.
- Never commit raw Kaggle-derived files (Give Me Some Credit, Home Credit) to a public repo; download them in the notebook instead.
