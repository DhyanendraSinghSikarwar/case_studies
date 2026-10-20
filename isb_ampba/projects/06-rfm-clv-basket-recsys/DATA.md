# DATA — Project 06: RFM Segmentation, CLV, Market Basket & Recommender

Links checked on **2026-10-13/14** (`curl -s -o /dev/null -L -m 30 -A "Mozilla/5.0" -w "%{http_code}" -r 0-100 <url>`; 200/206 = reachable). All counts were computed from the real file while preparing this plan.

## 1. Primary data: UCI Online Retail II (id 502) — customer rows only

| Item | Value |
|---|---|
| Page | https://archive.ics.uci.edu/dataset/502/online+retail+ii — ✔ reachable |
| Zip (≈ 45.6 MB, contains `online_retail_II.xlsx`) | https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip — ✔ downloaded |
| Official metadata | 1,067,371 instances, 2009-12-01 → 2011-12-09, DOI 10.24432/C5CG6D |
| This project uses | **clean sales lines that have a `Customer ID`** |

### Loader (read once, then parquet)
```python
sheets = pd.read_excel(xlsx_path, sheet_name=None)             # about 5 minutes — do it ONCE
tx = pd.concat(sheets.values(), ignore_index=True)
tx.columns = ["invoice", "stock_code", "description", "quantity", "invoice_date", "unit_price", "customer_id", "country"]
tx["invoice"] = tx["invoice"].astype(str); tx["stock_code"] = tx["stock_code"].astype(str)
tx["description"] = tx["description"].astype("string")         # mixed str / NaN / int: parquet fails otherwise
tx["customer_id"] = tx["customer_id"].astype("Int64")
tx.to_parquet("data/interim/transactions.parquet", index=False)
```

### Counts from the real file
| Check | Value |
|---|---|
| Raw rows | 1,067,371 (525,461 + 541,910 over the two sheets) |
| Missing `Customer ID` | 243,007 rows (dropped for this project) |
| Cancellation lines / `Quantity ≤ 0` / `Price ≤ 0` | 19,494 / 22,950 / 6,207 |
| Exact duplicate rows | 34,335 (not dropped by this plan; decide and document) |
| **Clean sales with a customer ID** | **802,914 lines, 5,853 customers** (non-product codes `POST, D, DOT, M, BANK CHARGES, S, AMAZONFEE, ADJUST, ADJUST2, CRUK` removed) |
| Median orders per customer | 3; customers with ≥ 2 orders: 4,234 (of 5,852 with sales under the slightly wider non-product list) |
| Customers active **up to 2011-06-30** (calibration) | 5,013 |
| Customers active **after 2011-06-30** up to 2011-12-09 (holdout) | 3,366 |
| Customers present in both | 2,527 |
| Holdout spend of customer-identified sales | £4.87 million |
| Country | about 92% of lines are from the United Kingdom |
| Median distinct SKUs per invoice | 15 |

### Time splits used in this project
- **Segments / CLV:** calibration up to **2011-06-30**, holdout **2011-07-01 → 2011-12-09** (162 days).
- **Recommender:** train up to **2011-11-09**, test = purchases in the **last 30 days** (2011-11-10 → 2011-12-09).

### Pitfalls
1. Mixed dtypes break `to_parquet` (cast as above).
2. Many customers are wholesalers: monetary value is heavy-tailed (use logs; the largest customers spend more than £100,000).
3. Only ~5,000 customers: clusters and CLV deciles are noisy; avoid over-reading small segments.
4. A customer's first purchase date is the first purchase in the data, not the true acquisition date (left-censoring from 2009-12-01).
5. Items are bought repeatedly by the same customer (stock re-orders): decide whether the recommender may recommend items a customer bought before and say which you evaluated.
6. Seasonality: the holdout (July–December) contains the Q4 peak (Q4 is ~38% of annual revenue).

## 2. Similar datasets (optional second runs)

| Dataset | Use | Link | Status |
|---|---|---|---|
| UCI Online Retail (id 352) | Earlier, smaller retail transactions for CLV/segmentation | https://archive.ics.uci.edu/dataset/352/online+retail | ✔ reachable, not downloaded |
| Dunnhumby "The Complete Journey" | Households over two years with demographics and campaign history — adds campaign response for the campaign planner | https://www.dunnhumby.com/source-files/ (✔ page reachable; no login mentioned; read the terms; Kaggle mirror: https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey, login needed) | not downloaded |
| CDNOW sample (built into `lifetimes`) | Tiny, classic dataset for testing your BG/NBD code | `from lifetimes.datasets import load_cdnow_summary` (needs the library to import) | see PLAN M3 |
| Olist Brazilian e-commerce (Kaggle) | Orders and reviews, ~100k orders | https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce (login) | not downloaded |
| Instacart Market Basket | Large grocery baskets for the recommender; its Kaggle competition page returned HTTP 404 on 2026-10-14 so look for the current location yourself | **not verified** | — |
