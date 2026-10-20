# DATA — Project 07: Churn Prediction + Uplift Retention

Links checked on **2026-10-13/14** (`curl -s -o /dev/null -L -m 30 -A "Mozilla/5.0" -w "%{http_code}" -r 0-100 <url>`; 200/206 = reachable). Counts below come from files that were downloaded and processed while preparing this plan.

## 1. Datasets and their roles

| Role | Dataset | Real? |
|---|---|---|
| Churn labels and features | UCI **Online Retail II** | Real transactions |
| Treatment (Track A) | A **simulated** 50/50 offer pilot on top of the real churn labels | Synthetic effect, real baseline |
| Treatment (Track B) | **Hillstrom** e-mail RCT | Real randomised experiment |
| Optional alternatives | IBM Telco churn, Criteo uplift | Real |

## 2. UCI Online Retail II (id 502)

| Item | Value |
|---|---|
| Page | https://archive.ics.uci.edu/dataset/502/online+retail+ii — ✔ reachable |
| Direct zip (≈ 45.6 MB; contains `online_retail_II.xlsx`) | https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip — ✔ downloaded |
| Official metadata (UCI API) | 1,067,371 instances; transactions of a UK-based online retailer from 2009-12-01 to 2011-12-09; DOI 10.24432/C5CG6D |
| `ucimlrepo` | `fetch_ucirepo(id=502)` also works; the xlsx route is more predictable |

### What the file contains (counted)
| Check | Value |
|---|---|
| Sheets | `Year 2009-2010` (525,461 rows) and `Year 2010-2011` (541,910 rows) = 1,067,371 |
| Columns | `Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country` |
| Date range | 2009-12-01 07:45 → 2011-12-09 12:50 |
| Missing `Customer ID` | 243,007 rows |
| Missing `Description` | 4,382 rows |
| Exact duplicate rows (all 8 columns) | 34,335 |
| Cancellation lines (`Invoice` starting with `C`) | 19,494 |
| `Quantity ≤ 0` / `Price ≤ 0` | 22,950 / 6,207 |
| Countries / customers | 43 / 5,942 |
| After the cleaning rules in PLAN M1 (sales only, with a customer ID) | 802,914 lines, 5,853 customers; ≈ 92% of lines are from the United Kingdom |

### Loading pitfalls (these will break a naive script)
1. **The Excel read takes minutes** (about 5 minutes per read in testing) — read it **once**, then work from parquet.
2. **Mixed types in three columns.** `Invoice` is an integer for most rows and a string for cancellations (`C…`); `StockCode` mixes integers and strings; `Description` mixes strings, `NaN` and a few integers. `DataFrame.to_parquet` fails with `ArrowTypeError: Expected bytes, got a 'int' object` unless you cast first:
   ```python
   tx["invoice"] = tx["invoice"].astype(str); tx["stock_code"] = tx["stock_code"].astype(str)
   tx["description"] = tx["description"].astype("string"); tx["customer_id"] = tx["customer_id"].astype("Int64")
   ```
3. **`Customer ID` is a float** in the sheet; use nullable `Int64` after dropping missing values.
4. **Duplicate lines**: 34,335 exact duplicates. The plan does not drop them (some are genuine repeated scans of the same item on one invoice); say so, or test the effect.
5. **Non-product codes** (`POST`, `D`, `M`, `BANK CHARGES`, `S`, `AMAZONFEE`, `ADJUST`, `CRUK`, …) are not merchandise; remove them from sales.
6. **Wholesalers**: many customers are wholesalers; outliers in `monetary_6m` are real (the maximum in one snapshot exceeds £140,000).
7. **Currency is GBP**; the project converts with `gbp_to_inr` from `config.yaml` (an assumption you must update).

## 3. Hillstrom e-mail marketing experiment (Track B)

| Item | Value |
|---|---|
| CSV (✔ reachable and downloaded) | http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv |
| Also via | `sklift.datasets.fetch_hillstrom()` from `scikit-uplift` (https://pypi.org/project/scikit-uplift/ ✔; check the function signature with `help`) |
| Source / design | Kevin Hillstrom, MineThatData: customers who last purchased within 12 months, randomly assigned to a Men's e-mail, a Women's e-mail or no e-mail; outcomes measured over the next 2 weeks |
| Size and columns | **64,000 rows**; `recency, history_segment, history, mens, womens, zip_code, newbie, channel, segment, visit, conversion, spend` |
| Arms (counted) | Womens E-Mail 21,387 · Mens E-Mail 21,307 · No E-Mail 21,306 |
| Outcome means (counted) | visit: Womens 15.14%, Mens 18.28%, No E-Mail 10.62%; conversion: 0.88% / 1.25% / 0.57%; spend (USD per customer): 1.08 / 1.42 / 0.65 |
| Treatment variable | `segment` (string). `w = (segment != "No E-Mail")` for "any e-mail"; or compare each e-mail with the control separately |
| Randomisation probability | about 2/3 for "any e-mail" (check: `w.mean()`); 1/3 for each single e-mail arm vs the pooled design |

What it lacks: one marketing channel for a different business; very few conversions (0.6–1.3%), so uplift estimates are noisy; no churn history; currency is USD.

## 4. Alternatives

| Dataset | Use | Link | Status |
|---|---|---|---|
| **Criteo Uplift Prediction (HF)** | Large real RCT (millions of rows) for a scale test | https://huggingface.co/datasets/criteo/criteo-uplift | page ✔ reachable; check the file list and size before downloading. The older S3 link I tried returned HTTP 404 — do not use it |
| **IBM Telco Customer Churn** | A cleaner real churn table (7,043 customers is the commonly cited size — verify after download) for the churn half only | https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv | ✔ reachable |
| UCI Online Retail (id 352) | Older, smaller retail transactions | https://archive.ics.uci.edu/dataset/352/online+retail | not verified |

## 5. Simulated pilot (Track A): rules

1. Baseline outcome = the **real** churn label; only the treatment effect is invented (document it in `docs/SIMULATOR.md`).
2. Treatment is randomised (`Bernoulli(0.5)`) with a seeded generator.
3. Ground-truth `tau_true`, `save_rate_true` and `saved` are written to the pilot table but are **never** features.
4. Because the pilot uses the churn labels of the *same* customers, use out-of-fold churn probabilities (`p0`) when building the effect.
