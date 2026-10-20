# DATA — Project 05: Promotion Cannibalisation Engine

Links checked on **2026-10-13/14** (`curl -s -o /dev/null -L -m 30 -A "Mozilla/5.0" -w "%{http_code}" -r 0-100 <url>`; 200/206 = reachable). Every count below was computed from the real file while preparing this plan.

## 1. Primary data: UCI Online Retail II (id 502)

| Item | Value |
|---|---|
| Page | https://archive.ics.uci.edu/dataset/502/online+retail+ii — ✔ reachable |
| Direct zip (≈ 45.6 MB, contains `online_retail_II.xlsx`) | https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip — ✔ downloaded |
| What it is | All transactions of a UK-based, UK-registered online gift-ware retailer, 2009-12-01 → 2011-12-09; many customers are wholesalers. Official metadata: 1,067,371 instances, DOI 10.24432/C5CG6D |
| Cite | Chen, D. (2019). Online Retail II. UCI Machine Learning Repository |
| Currency | GBP — keep it in £ inside the engine and convert only in the memo |

### Counts from the real file
| Check | Value |
|---|---|
| Sheets | `Year 2009-2010` 525,461 rows + `Year 2010-2011` 541,910 rows = **1,067,371** |
| Columns | `Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country` |
| Missing `Customer ID` / `Description` | 243,007 / 4,382 |
| Exact duplicate rows | 34,335 |
| Cancellation lines (`Invoice` starts with `C`) | 19,494 |
| `Quantity ≤ 0` / `Price ≤ 0` | 22,950 / 6,207 |
| Non-product lines removed (`POST, D, DOT, M, BANK CHARGES, S, AMAZONFEE, ADJUST, ADJUST2, CRUK, PADS, C2, TEST001, TEST002`) | 5,824 |
| **Clean sales lines** (not a cancellation, product code, `Quantity > 0`, `Price > 0`; customer ID **not** required for this project) | **1,037,082** |
| Clean sales invoices / distinct SKUs / revenue | 39,517 / 4,903 / £20.12 million |
| Unique cleaned descriptions | 5,343 (646 SKUs have more than one description — use the most frequent) |
| Q4 (Oct–Dec) share of revenue | 38.3% — strong seasonality |
| Median distinct SKUs per invoice | 15 (36,308 of 39,517 invoices have 2+ SKUs) |
| Top 24 SKUs share of revenue | 12.7% |

### Loader (read once, then parquet)
```python
sheets = pd.read_excel(xlsx_path, sheet_name=None)            # dict of DataFrames; about 5 minutes — do it ONCE
tx = pd.concat(sheets.values(), ignore_index=True)
tx.columns = ["invoice", "stock_code", "description", "quantity", "invoice_date", "unit_price", "customer_id", "country"]
tx["invoice"] = tx["invoice"].astype(str); tx["stock_code"] = tx["stock_code"].astype(str)
tx["description"] = tx["description"].astype("string")        # mixed str / NaN / int: parquet fails without this
tx["customer_id"] = tx["customer_id"].astype("Int64")
tx.to_parquet("data/interim/transactions.parquet", index=False)
```
`ucimlrepo.fetch_ucirepo(id=502)` is an alternative that avoids the zip, but the xlsx route behaves more predictably.

### Pitfalls
1. **Mixed dtypes** in `Invoice`, `StockCode` and `Description` break `to_parquet` (error: `Expected bytes, got a 'int' object`) — cast as above.
2. **Promotions are not recorded.** The file has no promotion flag. "Promotions" must be inferred from price changes (and the price variation is limited — see §2).
3. **Wholesale price tiers.** The same SKU can sell at different prices in one week to different customers; average price (revenue/units) therefore moves with customer mix. Use the **modal unit price per SKU-week** as the list price.
4. **Returns:** cancellations are separate invoices; keep them out of demand but you may use them to net units.
5. **Missing customer IDs** (243,007 rows): fine for basket and demand analysis (invoice-level); not usable for customer-level work.
6. **Seasonality (Q4 = 38% of revenue):** include week fixed effects or Q4 dummies in every demand regression.

## 2. Is price variation enough to estimate elasticities? (measured)

Using the **modal unit price** of each SKU in each calendar week (clean sales only; 197,944 SKU-weeks; 152,841 pairs of consecutive weekly observations):

| Measure | Value |
|---|---|
| Consecutive weeks where the modal price changed by more than 1% / 5% | 31.3% / 30.3% |
| Consecutive weeks where the modal price **dropped** by more than 5% / 10% | 14.8% / 14.1% |
| SKUs with at least 5 weekly price drops of > 5% | 1,775 (831 with at least 10) |
| SKUs with ≥ 40 weeks of data **and** ≥ 5 drops | 1,584 |
| SKUs with only a single distinct price over the whole period | 556 |

So price does vary for a large block of SKUs, but changes are not randomised: a price drop may coincide with clearance, end-of-season or a change in the customer mix. A regression of log units on log price with SKU and week fixed effects gives an association; call it a **price-response estimate with caveats**, not a causal elasticity. The plan therefore (a) estimates it for SKUs that pass an identifiability filter, (b) uses priors for the rest, and (c) sweeps elasticity across a wide range in the final analysis.

## 3. Similar datasets with real promotion data (strongly recommended as a stretch/validation)

| Dataset | Why it helps | Link | Status |
|---|---|---|---|
| **Dunnhumby "Breakfast at the Frat"** | Weekly sales **and promotion flags** for 5 products in 4 categories over 156 weeks — ideal to estimate promotion lift and cannibalisation with real promo indicators | Download from https://www.dunnhumby.com/source-files/ (page ✔ reachable; no login mentioned, terms not stated on the page — read its Terms link; do not redistribute) | page verified, file not downloaded |
| **Dunnhumby "The Complete Journey"** | Household transactions over two years for 2,500 households, including promotion/coupon ("causal") data and direct-marketing history | same page; also on Kaggle: https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey (✔ reachable; Kaggle login needed to download) | not downloaded |
| UCI Online Retail (id 352) | An earlier, smaller retail dataset for a second run | https://archive.ics.uci.edu/dataset/352/online+retail ✔ | not downloaded |
| Olist Brazilian e-commerce (Kaggle) | Orders, prices, categories — no promo flags | https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce ✔ (login) | not downloaded |

If you add Dunnhumby: estimate the promotion lift of the promoted product and the **change in sibling/competitor units in promo weeks** with a regression with store and week fixed effects, then compare the cannibalisation share with the one your MNL assumes. That gives you an empirical anchor that Online Retail II cannot.
