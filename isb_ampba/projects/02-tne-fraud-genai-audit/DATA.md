# DATA — Project 02: T&E Expense Fraud Detection + GenAI Audit Copilot

Links checked on **2026-10-13** (`curl -s -o /dev/null -L -m 30 -A "Mozilla/5.0" -w "%{http_code}" -r 0-100 <url>`; 200/206 = reachable). The two council files below were downloaded and inspected; the counts are from those files.

**There is no public dataset of expense claims with fraud labels** (employee expense data is personal and confidential). So this project uses two data tracks:

| Track | Data | Why |
|---|---|---|
| **A — contract path** | A **synthetic labelled generator** (you write it in M1) with 8 injected fraud schemes | Only way to *measure* precision/recall and per-scheme recall |
| **B — realism check** | **Real, unlabelled** UK council procurement-card (p-card) spend files | Shows the pipeline runs on messy real transactions; you can only read the top-ranked items, not score them |

Say this clearly in the README. Never report precision/recall for Track B.

---

## 1. Track A — synthetic generator (design contract)

Config (`config/config.yaml`):

```yaml
seed: 42
paths: {raw: data/raw, interim: data/interim, processed: data/processed, outputs: outputs, figures: figures, models: models, duckdb: data/tne.duckdb}
generator:
  n_employees: 1500
  start_date: "2024-01-01"
  end_date: "2024-12-31"
  fraud_target: 0.030            # share of fraudulent claim lines (acceptance: 2.5% - 3.5%)
  n_rings: 3
  ring_size: 4
  receipt_threshold_inr: 500
  mileage_rate_inr_per_km: 12
  holidays: ["2024-01-26", "2024-03-25", "2024-08-15", "2024-10-02", "2024-11-01", "2024-12-25"]
business:
  minutes_per_claim_review: 15
  audit_budget_frac: 0.05
  auditor_cost_inr_per_hour: 800
  recovery_rate: 0.80            # share of confirmed fraud value actually recovered (assumption)
risk: {w_anomaly: 0.4, w_kri: 0.4, w_graph: 0.2}     # starting weights; tuned on a validation slice in M3
```

Tables written to DuckDB (`data/tne.duckdb`): `employees(emp_id, grade, dept, cost_center, manager_id, city, join_date)`, `policy(grade, category, daily_limit_inr)`, `claims(claim_id, emp_id, date, category, merchant, city, amount_inr, receipt_flag, submitted_at, approved_by, approved_at, description, trip_id, distance_km)`, and `labels(claim_id, is_fraud, fraud_type)`.

**Rules that keep the exercise honest**
1. Fraud labels live only in `labels`. No feature, KRI or model may read it (test this).
2. `claim_id` is assigned **after** shuffling, so ID order carries no information.
3. About 60% of fraud lines are *added* rows and 40% *edit* honest rows (mileage and round-number schemes), so fraud is not simply "extra rows".
4. Fraudsters are disjoint per scheme; 3 collusion rings of 4 employees approve each other's padded claims within minutes.
5. About 2% of honest claims are approved by the manager's manager (skip-level), so "approver ≠ manager" is not a perfect fraud signal.
6. All amounts and distances are assumptions chosen to be plausible (Indian city names, INR limits by grade); they are **not** calibrated to a real company.

The 8 schemes: 1 duplicate claim (same merchant+amount within 0–2 days of an honest claim); 2 split transactions (2–3 claims each under the daily limit, sum above it); 3 weekend/holiday meals with no trip; 4 amounts just under the receipt threshold (₹460–499) with no receipt; 5 personal merchants (jewellery/liquor) in business categories; 6 mileage inflation (claimed km 2.2–3.5× the city norm); 7 approval collusion rings; 8 round-number amounts at high frequency.

## 2. Track B — real UK council procurement-card spend (Peterborough City Council)

| Item | Value |
|---|---|
| Publisher / listing | Peterborough City Council via data.gov.uk: https://www.data.gov.uk/dataset/peterborough-city-council-government-procurement-card-transactions — ✔ page fetched 2026-10-13 (lists 36 quarterly workbooks) |
| Licence | Check the licence on the data.gov.uk page before redistributing (UK local-authority transparency data is commonly Open Government Licence, but verify). Do not commit the raw files; download in code |
| Format | `.xlsx` (labelled "CSV" on the listing, but the files are Excel workbooks) |
| Example files | `https://data.cambridgeshireinsight.org.uk/sites/default/files/Pcard%20Spend%20Q1%20FY%2023-24%20%28Apr-Jun%29.xlsx` ✔ reachable · `...Pcard%20Spend%20Q2%20FY%2023-24%20%28Jul-Sept%29.xlsx` ✔ reachable |
| Currency | **Pounds sterling.** The pipeline keeps the column name `amount_inr` for convenience — say so, and never present these as rupees |

### What the files actually contain (inspected)
Workbook sheet **`Data`**, five columns: `Date Posted`, `Original Amount`, `Merchant`, `Category`, `Service Area/Directorate`. (Other sheets in these workbooks are older raw extracts that include cardholder names — do not use them.)

| File | Rows | Dates | Amount range / median | Notes |
|---|---|---|---|---|
| Q1 FY23-24 (Apr–Jun) | 1,234 | 2023-04-04 → 2023-07-03 | −£941.39 … £6,289.20 / £127.34 | 191 refunds (negative amounts); 189 merchants; categories led by ACCOMMODATION (696), RETAIL (258); 132 amounts in £450–£499.99; 122 groups of identical (date, amount, merchant) |
| Q2 FY23-24 (Jul–Sep) | 893 | 2023-07-04 → 2023-10-02 | −£1,000 … £5,000 / £82.70 | 147 refunds; category spelled both `ACCOMMODATION` and `ACCOMODATION` — normalise; 47 amounts in £450–£499.99 |

Loader and mapping (this is `src/tne/realdata.py` in PLAN.md M3b):
```python
raw = pd.read_excel(path, sheet_name="Data", usecols=["Date Posted", "Original Amount", "Merchant", "Category", "Service Area/Directorate"])
```
Needs `openpyxl` (`pip install openpyxl`). `Service Area/Directorate` is used as a **proxy for the employee** because there is no cardholder ID in this sheet.

### What the real data lacks (be explicit)
No employee, grade, manager, approver, receipt flag, submission time, trip ID or fraud labels. So only the unsupervised half (features from amount, merchant, date, category; IsolationForest/KNN/LOF) and a keyword KRI can run. Many "anomalies" will be legitimate (a £5,000 hotel block-booking). Treat the output as a review queue.

## 3. Similar or alternative datasets (verify before use)

| Dataset | Use | Link | Caveat |
|---|---|---|---|
| Other UK council p-card / spend-over-£500 files | More real transactions; Wigan, Sunderland, Oxford, York also publish | Search results on 2026-10-13 listed Sunderland (https://www.sunderland.gov.uk/card-transactions), Wigan (blocks scripted fetches, HTTP 403) and York (https://data.yorkopendata.org/dataset/government-procurement-card-data); **not individually verified** | Column names differ per council |
| Credit-card payment fraud (ULB), IEEE-CIS, PaySim | Practise anomaly metrics (PR-AUC, precision@k) on labelled data | Kaggle pages need a login; **not verified** | Payment fraud, not expense fraud — different features and no approval chain |
| Benford's-law practice sets | Test your first-digit feature | Use any large real amount column (for instance the p-card files) | Small samples give noisy Benford statistics (the plan requires ≥ 20 claims per employee) |

## 4. Pitfalls
- `pandas.read_excel` on `.xlsx` needs `openpyxl`; on the council files read only sheet `Data`.
- Negative amounts are refunds; do not treat them as fraud and do not log-transform them without `abs()`.
- Merchant strings contain store numbers (`Travelodge Gb0000`); normalise (lowercase, strip digits and punctuation) before counting duplicates.
- Fit unsupervised detectors on a **sample** (the generator makes ~100k+ rows; KNN/LOF on all rows is slow).
- Do not let the synthetic generator's tell-tale artefacts become the model: shuffle before assigning IDs, include honest round amounts and honest skip-level approvals.
