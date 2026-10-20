---
name: ampba-data-sources
description: Reference loaders, cleaning rules and offline fallbacks for every dataset used in the ISB AMPBA case studies (UCI 350, 502, 144; yfinance NSE; HuggingFace Amazon Reviews 2023; synthetic simulators). Use when writing any data.py / sim.py or when a download fails.
---

# Dataset reference

All loaders: cache to `data/raw/<name>.parquet`; on second run read cache; log row counts; validate schema; provide `make_fixture(n)` for tests.

## UCI #350 — Default of Credit Card Clients (CS1)
```python
from ucimlrepo import fetch_ucirepo
d = fetch_ucirepo(id=350); df = pd.concat([d.data.features, d.data.targets], axis=1)
```
- If columns are `X1..X23, Y`: rename `X1 LIMIT_BAL, X2 SEX, X3 EDUCATION, X4 MARRIAGE, X5 AGE, X6 PAY_0, X7 PAY_2, X8 PAY_3, X9 PAY_4, X10 PAY_5, X11 PAY_6, X12..X17 BILL_AMT1..6, X18..X23 PAY_AMT1..6, Y default`.
- Clean: EDUCATION {0,5,6}→4; MARRIAGE 0→3. Expect 30,000 rows, default rate ≈ 0.221.
- Fallback: download xls from https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients (header row 1).

## UCI #502 — Online Retail II (CS5, CS6, CS7, CS8 calibration)
- `fetch_ucirepo(id=502)`; if it fails, download the zip from https://archive.ics.uci.edu/dataset/502/online+retail+ii and `pd.read_excel(path, sheet_name=None)` → concat both sheets (slow: convert once to parquet).
- Columns: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country.
- Clean: drop Invoice starting "C" (keep separately as returns), Quantity ≤ 0, Price ≤ 0, StockCode in {POST, D, M, C2, DOT, BANK CHARGES, AMAZONFEE, PADS, CRUK, ADJUST, TEST001, TEST002} or non-alphanumeric gift codes; strip Description; `revenue = Quantity*Price`.
- Expected after cleaning ≈ 1.0M lines, ≈ 5.9k customers, date range 2009-12-01 → 2011-12-09.

## UCI #144 — Statlog German Credit (CS3)
- `fetch_ucirepo(id=144)`; columns Attribute1..Attribute20 + class (1 good, 2 bad → map to bad=1).
- Decode codes A11..A202 with a dict in `codes.py` (status of checking account, credit history, purpose, savings, employment, personal status, etc. per UCI doc). Cost matrix: FN (bad predicted good) = 5, FP = 1.

## yfinance — NSE (CS4)
```python
yf.download(tickers, start="2015-01-01", auto_adjust=True, group_by="ticker", threads=True, progress=False)
```
- Tickers `SYMBOL.NS`; benchmark `^NSEI`; VIX `^INDIAVIX`. Batch 50 tickers per call, retry 3× with backoff, cache per ticker.
- Universe: `https://archives.nseindia.com/content/indices/ind_nifty500list.csv` (needs browser User-Agent header). Fallback: `config/universe_fallback.txt` (Nifty 100 symbols, create it).
- Drop tickers with < 500 rows; forward-fill max 2 days; never back-fill.

## HuggingFace — McAuley-Lab/Amazon-Reviews-2023 (CS10)
```python
from datasets import load_dataset
rev = load_dataset("McAuley-Lab/Amazon-Reviews-2023", "raw_review_Electronics", trust_remote_code=True, split="full", streaming=True)
meta = load_dataset("McAuley-Lab/Amazon-Reviews-2023", "raw_meta_Electronics", trust_remote_code=True, split="full", streaming=True)
```
- Stream and take the first N (config `n_reviews`, default 100k; tests 200). Fields: rating, title, text, asin, parent_asin, user_id, timestamp, verified_purchase, helpful_vote.
- Fallback: any CSV in `data/raw/reviews.csv` with columns (review_id, asin, rating, text, date).

## Synthetic simulators (CS2, CS3 docs, CS7 pilot, CS8, CS9)
- Single entry `generate(cfg) -> dict[str, DataFrame]`, fully seed-controlled (`np.random.default_rng(cfg.seed)`).
- Store ground truth separately (`truth.parquet` / `params.json`) and NEVER use it in features — tests must assert models don't import it.
- Write a `docs/SIMULATOR.md` explaining every distribution and parameter; state clearly the data is synthetic in README and memo.
- Add recovery tests: model-estimated parameters within tolerance of truth.
