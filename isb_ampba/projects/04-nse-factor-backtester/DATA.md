# DATA — Project 04: NSE Factor Screener & Regime-aware Backtester

Links checked on **2026-10-13/14** (`curl -s -o /dev/null -L -m 30 -A "Mozilla/5.0" -w "%{http_code}" -r 0-100 <url>`; 200/206 = reachable). The Yahoo download numbers below come from an actual run of the pipeline on the Nifty 100 on 2026-10-13.

## 1. Sources

| Need | Source | Status |
|---|---|---|
| Daily OHLCV for NSE stocks and indices | **`yfinance`** (unofficial Yahoo Finance client). PyPI: https://pypi.org/project/yfinance/ (version 1.7.0 on 2026-10-14); repo https://github.com/ranaroussi/yfinance | ✔ package and repo reachable; downloads worked on 2026-10-13 |
| Tickers | NSE symbol + `.NS` (e.g. `RELIANCE.NS`, `M&M.NS`, `BAJAJ-AUTO.NS`) | ✔ worked |
| Benchmarks | `^NSEI` (Nifty 50 price index — **no dividends**), `^INDIAVIX` (India VIX), `NIFTYBEES.NS` (Nifty 50 ETF, auto-adjusted close = total-return proxy) | ✔ worked |
| Constituent lists | https://www.niftyindices.com/IndexConstituent/ind_nifty100list.csv ✔ · `ind_nifty50list.csv` ✔ · `ind_nifty200list.csv` ✔ · `ind_nifty500list.csv` ✔ (same folder) | ✔ verified 2026-10-14 |
| Same lists, NSE archive host | https://nsearchives.nseindia.com/content/indices/ind_nifty500list.csv ✔ (the older `archives.nseindia.com/...` host answered with a browser User-Agent; always send `User-Agent: Mozilla/5.0`) | ✔ |

List columns (verified from the Nifty 100 file): `Company Name, Industry, Symbol, Series, ISIN Code` — 100 rows. Keep `Series == "EQ"` and build `yahoo = Symbol + ".NS"`.

### Download pattern that works (batches, retry, per-ticker cache)
```python
raw = yf.download(tickers, start="2015-01-01", end=None, auto_adjust=True, group_by="ticker",
                  progress=False, threads=True, timeout=30)
# raw has MultiIndex columns (ticker, field):  raw["TCS.NS"][["Open","High","Low","Close","Volume"]]
```
Rules: 20 tickers per call, up to 4 retries with exponential back-off and jitter, one parquet file per ticker (file name must replace `^` and `&`), tz-naive normalised dates, and a pause between batches. **Re-download the whole history when the cache is stale** (`auto_adjust=True` rescales past prices after every split or dividend, so appending new rows to an old cache creates a jump).

### What the real download looked like (Nifty 100 list, 2015-01-01 → 2026-10-13)
| Check | Result |
|---|---|
| Tickers returned | 100 of 100 |
| Rows per ticker | 83 to 2,899 (2,899 trading days for the full history) |
| Tickers whose first price is later than 2015-01-05 | 23 (recent listings, e.g. `JIOFIN.NS` 2023-08-21, `HYUNDAI.NS` 2024-10-22, `ETERNAL.NS` 2021-07-23, `TATACAP.NS` 2025-10-13, `VAML.NS` 2026-06-15) |
| Largest share of missing days since a ticker's first price | 1.2% |
| Largest number of zero-volume days in one ticker | 7 |
| Moves of more than ±25% in a day | 31 across all tickers (`IDEA.NS` 8, `ADANIENT.NS` 4) — check each is a real event, not a data error |
| Last date | 2026-10-13 for every ticker |

Read this as: (a) short histories are normal and your factors must tolerate `NaN` warm-up; (b) tickers get **renamed or demerged** (`ETERNAL.NS` is the former Zomato; `TMCV.NS` appears after a Tata Motors demerger) — the constituent file lists today's names only.

## 2. Optional: earnings dates and EPS surprise
`yf.Ticker(t).get_earnings_dates(limit=40)` returns announcement timestamps (in `America/New_York` — convert to `Asia/Kolkata` before taking the date) and a `Surprise(%)` column. It is flaky and sparsely populated for Indian stocks. The plan treats the `earnings_drift` factor as optional: when data is missing the factor is neutral (0), and you must say how many tickers actually had events.

## 3. Alternatives if Yahoo fails or changes
| Option | Notes |
|---|---|
| **`jugaad-data`** (PyPI 0.35.x, https://pypi.org/project/jugaad-data/ ✔) | Downloads NSE bhavcopy and historical data directly from NSE; check its docs for the current function names; unadjusted prices — you must adjust for splits/bonuses yourself |
| **`nselib`** (PyPI 2.5.x, https://pypi.org/project/nselib/ ✔) | Wrapper over NSE endpoints for capital-market data; same adjustment caveat |
| NSE reports page https://www.nseindia.com/all-reports ✔ and niftyindices historical data https://www.niftyindices.com/reports/historical-data ✔ | Manual downloads of index history / bhavcopy; scripted access is often blocked |
| Kaggle "NIFTY-50 Stock Market Data (2000–2021)" | Needs a Kaggle login; stops in 2021 — **not verified** |

If you use a source without adjustment, build the adjusted close yourself from corporate-action data or drop the affected tickers; never mix adjusted and unadjusted prices.

## 4. Pitfalls specific to this data
1. **Survivorship bias.** The constituent list is *today's* Nifty. Stocks that dropped out (or failed) are missing, so backtests look better than reality. State this in the README; it is the biggest limitation.
2. **Index vs total return.** `^NSEI` excludes dividends. Compare the strategy with the ETF proxy (`NIFTYBEES.NS`) too, and say which one you use for each claim.
3. **Adjusted prices change over time.** With `auto_adjust=True` the whole history rescales whenever a split/dividend happens, so re-download everything when refreshing.
4. **Calendar mismatches.** Index and stocks have special-session days and VIX misses a few days: reindex everything to the Nifty trading calendar; forward-fill VIX by at most 3 days; never forward-fill stock prices (missing = not tradable).
5. **Rate limiting.** Large unbatched downloads get blocked; batch, back off, cache.
6. **Ticker symbols with `&` or `-`** (`M&M.NS`, `BAJAJ-AUTO.NS`) work as they are on Yahoo but are not safe file names.
7. **Liquidity filter timing.** Use a trailing median traded value (close × volume) known at the close of day `t`; never a full-sample average.
8. **Fallback universe.** If the list download fails, keep `config/universe_fallback.txt` (whitespace-separated NSE symbols, e.g. a hand-typed Nifty 50) so the pipeline still runs.
