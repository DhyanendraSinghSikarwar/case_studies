# DATA — Project 08: Two-sided Marketplace Dynamic Pricing

Links checked on **2026-10-13/14** (`curl -s -o /dev/null -L -m 30 -A "Mozilla/5.0" -w "%{http_code}" -r 0-100 <url>`; 200/206 = reachable). Every number labelled "measured" below was computed from the real file while preparing this plan (DuckDB reading the Parquet over HTTP).

## 1. Why two data sources

| | Real data (NYC TLC for-hire trips) | Simulator (you write it) |
|---|---|---|
| Has rider price **and** driver pay per trip | ✔ | ✔ |
| Randomised price / payout experiments | ✘ — price moves with demand (surge) | ✔ — ±10% randomised on 20% of segment-weeks |
| Known true elasticity and acceptance curve | ✘ | ✔ — so you can test that estimation recovers the truth |
| Role | **Calibrate** the simulator's shape and show the identification problem | **Contract path**: estimate, optimise and validate |

**Say this in the README:** the real data cannot identify price elasticity because high prices and high demand occur together (surge). The measured within-zone correlation of log trip counts with log fare-per-mile is positive (≈ 0.57 median across 244 zones, below), the opposite sign of a demand curve. That is exactly why the project estimates elasticity from *randomised* price experiments in the simulator.

## 2. Real data: NYC TLC High-Volume For-Hire Vehicle (HVFHV) trip records

| Item | Value |
|---|---|
| Publisher | NYC Taxi & Limousine Commission — page https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page ✔ reachable. Check the licence/terms on that page before redistributing; do not commit the raw files |
| File pattern (one file per month) | `https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_YYYY-MM.parquet` ✔ reachable for 2023-01. (The old `s3.amazonaws.com/nyc-tlc/...` path returned HTTP 403 — do not use it) |
| Zone lookup | https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv ✔ reachable |
| Size | One month ≈ 0.5 GB Parquet. January 2023: **18,479,031 trips**, 1 row group, 262 pickup zones |
| Companies in the file | `HV0003` (13,580,152 trips) and `HV0005` (4,898,879 trips) in 2023-01 (measured) — TLC's codes for Uber and Lyft; confirm against the TLC data dictionary linked from the page above |

### Verified schema (read from the Parquet footer of the 2023-01 file)
`hvfhs_license_num, dispatching_base_num, originating_base_num, request_datetime, on_scene_datetime, pickup_datetime, dropoff_datetime, PULocationID, DOLocationID, trip_miles (double), trip_time (int64, seconds), base_passenger_fare (double), tolls, bcf, sales_tax, congestion_surcharge, airport_fee, tips, driver_pay (double), shared_request_flag, shared_match_flag, access_a_ride_flag, wav_request_flag, wav_match_flag`.

The two columns that make this a two-sided dataset: **`base_passenger_fare`** (what the rider paid before taxes, tolls and tips) and **`driver_pay`** (what the driver earned, which includes tips and incentives).

### Read it without downloading 0.5 GB (DuckDB, column-pruned over HTTP)
```python
import duckdb
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_2023-01.parquet"
con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs;")
con.execute(f"""CREATE TABLE t AS
    SELECT hvfhs_license_num lic, pickup_datetime pu, PULocationID z, trip_miles mi,
           base_passenger_fare fare, driver_pay pay
    FROM read_parquet('{url}')""")          # transfers only these columns; took about 40 s in testing
```
If your network blocks it, download once with `curl -L -o C:\ampba_data\08\fhvhv_2023-01.parquet <url>` (resumable with `-C -`) and replace the URL with the local path. Keep the file **outside OneDrive** (`data_dir` in `config.yaml`).

### What was measured on 2023-01 (use as simulator calibration; recompute in M1)
Slots: morning 06–10, afternoon 11–15, evening 16–21, night 22–05 (by `pickup_datetime` hour), trips with `base_passenger_fare > 0`, `driver_pay > 0`, `trip_miles > 0`.

| Quantity | Measured |
|---|---|
| Share of trips by slot | morning **0.2014**, afternoon **0.2266**, evening **0.3424**, night **0.2296** |
| Median rider fare / driver pay / fare per mile | $16.28 / $12.81 / $5.49 |
| Median fare per mile by slot | morning 5.47, afternoon 5.73, evening 5.72, night 4.95 (USD per mile) |
| Take rate `1 − driver_pay / base_passenger_fare` | quantiles 5/25/50/75/95% = −0.09 / 0.13 / **0.23** / 0.31 / 0.42; by company median 0.23 (HV0003) and 0.24 (HV0005) |
| Rows with `driver_pay ≤ 0` / `base_passenger_fare ≤ 0` / `trip_miles ≤ 0` | 290,812 / 13,538 / 3,741 (drop them before computing ratios) |
| Zone-hour panel | 186,442 zone-hours (trips with ≥ 0.5 mile) |
| Within-zone correlation of log(trips) with log(fare per mile) | median **0.57** across 244 zones (10th–90th percentile 0.33–0.73) — **positive**, i.e. surge pricing, not a demand curve |
| Correlation of fare and driver pay | 0.955 |

Cautions: the take rate has fat tails (the mean is distorted: tips and incentives are inside `driver_pay`), so use medians and quantiles; one month of New York ride-hailing is an analogy for an Indian home-services platform, not a measurement of it.

## 3. Simulator calibration table (contract path)

Write these into `config/config.yaml` and describe every row in `docs/SIMULATOR.md`. **All are assumptions** (the right-hand column says what anchors them). Currency is ₹.

| Parameter | Value | Anchor |
|---|---|---|
| Segments | 6 cities × 5 services × 4 time-slots = 120; 52 weeks | master plan |
| Cities | Mumbai, Delhi NCR, Bengaluru, Hyderabad, Pune, Chennai | master plan |
| `city_demand_mult` | 1.30, 1.25, 1.20, 0.95, 0.80, 0.75 | assumption |
| `city_price_idx` | 1.12, 1.10, 1.10, 1.00, 0.96, 0.94 | assumption |
| Services | cleaning, plumbing, electrician, salon_at_home, ac_service | master plan ("5 services") |
| `service_p0` (list price ₹) | 499, 399, 399, 899, 699 | assumption |
| `service_d0` (weekly base requests per segment before city/slot) | 900, 500, 550, 600, 450 | assumption |
| Slot weights (relative demand by slot) | morning 0.2014, afternoon 0.2266, evening 0.3424, night 0.2296 (×4 inside the code so the mean is 1; night then × `night_factor` 0.45 because home services are quiet at night) | **TLC measured** (shape only) |
| Elasticity `ε` (log-log demand slope) | mean **−3.2**, service shifts [0, +0.5, +0.5, −0.4, −0.2], city sd 0.15, slot sd 0.10, segment sd 0.15, clipped to [−4.5, −1.2] | **assumption.** The master plan says to calibrate from an Online Retail II price–quantity regression (Project 05). Naive regressions on that file give small or even positive slopes (confounding), which would make the pricing problem degenerate (profit-maximising price is unbounded when `|ε| ≤ 1`), so −3.2 is a deliberate "price-sensitive consumer service" prior. Run the Online Retail II regression as a documented sensitivity, not as the source |
| Take rate (platform's share of the price) | mean 0.35, sd 0.03, clipped [0.15, 0.45]; `w0 = (1 − take) × p0` | assumption. TLC ride-hailing median take is ≈ 0.23; home-services platforms typically keep more. Sweep 0.23 in M4 |
| Variable cost per job | `0.06 × p0 + ₹15` | assumption |
| Weekly demand noise | lognormal(−σ²/2, σ = 0.06) | assumption |
| Seasonality | `1 + 0.15 sin(2π (week − phase)/52)` × festival bump `1 + 0.25 exp(−½((week − 43)/1.5)²)` | assumption |
| Partner capacity | `cap0 = k × d0`, `k ~ U(0.95, 1.35)`; a partner does 8 jobs/week, `n0 = cap0 / 8` | assumption |
| Partner acceptance | `A = sigmoid(α + β (payout − reservation))`, α = 0.5, β = 0.018 per ₹, reservation = 0.55 × p0 × (1 + N(0, 0.04)) | assumption (shape: logistic, as the master plan specifies) |
| Partner churn per week | 0.02 base, +0.06 if weekly earnings per partner < 0.65 × `w0 × 8`; recruitment 3% of `n0` per week | assumption |
| Experiments | 20% of segment-weeks, price ×(1 ± 0.10) and payout ×(1 ± 0.10) randomised independently | master plan |
| Business | payout floor ₹220; fulfilment target 90% (+2% buffer); partner earnings must stay ≥ 95% of static; price multiplier bounds [0.85, 1.25]; payout bounds [0.90, 1.25] | master plan + assumption |
| Holdout | last 12 of 52 weeks | master plan |

## 4. Alternatives and fallbacks

| Dataset | Use | Link | Caveat |
|---|---|---|---|
| Other months of HVFHV | More data for the descriptive analysis (e.g. a Jan vs Jul comparison) | same URL pattern with another `YYYY-MM` — only 2023-01 was verified | Each file ≈ 0.5 GB |
| TLC yellow/green taxi | Fares but no separate driver pay | https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page | Not two-sided |
| Uber/Lyft Boston cab rides (Kaggle) | Has surge multiplier and price per ride | Kaggle — login required, **not verified** | One city, 2018, no driver pay |
| Online Retail II (UCI #502) | Optional elasticity-prior analogy | https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip ✔ | Wholesale gift-ware; naive elasticities are confounded |

## 5. Pitfalls
- Using `driver_pay` as a clean "payout": it includes tips and incentives; negative take rates exist.
- Treating the TLC price–demand correlation as an elasticity (it is surge).
- Loading all columns of an 18-million-row Parquet into pandas (several GB) — select columns first.
- Letting the simulator's `truth` leak into estimation: keep `truth` in a separate folder and never import `make_truth` in `estimate.py`.
