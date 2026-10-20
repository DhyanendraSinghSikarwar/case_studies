"""
SYNTHETIC DATA GENERATOR - CASE STUDY 7 (Instamart-style quick-commerce demand forecasting with censored sales)
============================================================================================================
THIS DATA IS SYNTHETIC. Dark-store sales logs are confidential.

Documented context (Swiggy Instamart, via a summary of its Bytes post and a Fifth Elephant 2023 talk): dark stores deliver in
about 10-15 minutes; SKU counts of order 10^4; recorded sales are CENSORED by stock-outs; availability = share of the day
a SKU is orderable; substitution is handled by grouping SKUs (GSKU); wMAPE; evaluation should align with estimated
availability and wastage.

Simulation: 40 dark stores x 200 SKUs x 105 days. True daily demand = negative binomial with SKU base rate, store size,
weekday and festival effects, rain, promotions and slow trend. A LEGACY replenishment rule orders yesterday's stock as
"last 7 days of sales x 1.10 + 0.5". Because sales are censored by stock, that rule ratchets stock DOWN for items that
stock out (the classic censoring trap). 8% of store-SKU-days also receive a short shipment. When an SKU stocks out, 25%
of its unmet demand spills to other SKUs in its substitution group (observed sales of the mates are inflated).
Perishables (30% of SKUs) lose leftover stock to expiry (wastage).
Observed: opening stock, units sold, availability share of open hours, wasted units. Hidden truth: _true_demand.

Output: data/cs07/store_sku_days.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
START = pd.Timestamp("2026-01-05"); DAYS = 105
N_STORES, N_SKU, GSZ = 40, 200, 5
OPEN_H = 16
INTRADAY = np.array([0.02, 0.03, 0.04, 0.05, 0.05, 0.06, 0.06, 0.07, 0.07, 0.06, 0.06, 0.06, 0.07, 0.09, 0.11, 0.10]); INTRADAY /= INTRADAY.sum()
CUM = np.r_[0, np.cumsum(INTRADAY)]


def avail_from_ratio(r):
    """share of open hours the SKU is in stock when stock/demand ratio is r (<1 means stock-out), using the intraday demand profile."""
    r = np.clip(r, 0, 1); idx = np.searchsorted(CUM, r, side="right") - 1; idx = np.clip(idx, 0, OPEN_H - 1)
    frac = (r - CUM[idx]) / np.maximum(INTRADAY[idx], 1e-9); return np.where(r >= 1, 1.0, (idx + np.clip(frac, 0, 1)) / OPEN_H)


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    cat = rng.choice(["dairy", "fruit_veg", "bakery", "snacks", "beverages", "staples", "personal_care", "frozen"], N_SKU, p=[0.12, 0.14, 0.06, 0.18, 0.14, 0.14, 0.14, 0.08])
    perish = np.isin(cat, ["dairy", "fruit_veg", "bakery"]).astype(int); perish[rng.random(N_SKU) < 0.05] = 1
    base = np.exp(rng.normal(np.log(3.0), 1.0, N_SKU)) * np.where(perish == 1, 1.3, 1.0)
    gsku = np.repeat(np.arange(N_SKU // GSZ), GSZ); price = np.round(np.exp(rng.normal(np.log(90), 0.7, N_SKU)), 0)
    store_size = np.exp(rng.normal(0, 0.35, N_STORES)); affin = np.exp(rng.normal(0, 0.45, (N_STORES, N_SKU)))
    wk = np.array([0.88, 0.9, 0.93, 0.97, 1.05, 1.22, 1.12]); trend = rng.normal(0.0008, 0.0006, (N_STORES, N_SKU))
    festival = np.zeros(DAYS); festival[[30, 31, 45, 70, 71]] = [0.25, 0.15, 0.35, 0.2, 0.3]
    rain_days = rng.random(DAYS) < 0.2
    disp = 6.0                                                                                           # NB dispersion
    mean_hist = np.tile(base[None, :] * store_size[:, None] * affin, (1, 1))
    sales_hist = np.zeros((DAYS, N_STORES, N_SKU)); rows = []
    for d in range(DAYS):
        date = START + pd.Timedelta(days=d); dow = date.dayofweek
        promo = rng.random((N_STORES, N_SKU)) < 0.07
        mu = mean_hist * wk[dow] * (1 + festival[d]) * (1 + trend * d) * np.where(rain_days[d], np.where(perish[None, :] == 1, 1.05, 1.12), 1.0) * np.where(promo, 1.35, 1.0)
        dem = rng.negative_binomial(disp, disp / (disp + mu))
        if d < 7: stock = np.ceil(mu * 1.6 + 1)
        else: stock = np.ceil(sales_hist[d - 7:d].mean(0) * 1.10 + 0.5)
        short = rng.random((N_STORES, N_SKU)) < 0.08; stock = np.where(short, np.floor(stock * 0.7), stock)
        sold0 = np.minimum(dem, stock); unmet = dem - sold0
        grp_unmet = unmet.reshape(N_STORES, N_SKU // GSZ, GSZ).sum(2, keepdims=True) * np.ones((1, 1, GSZ)); grp_unmet = grp_unmet.reshape(N_STORES, N_SKU)
        spill = 0.25 * (grp_unmet - unmet) / (GSZ - 1); sold = np.minimum(sold0 + spill, stock); sold = np.floor(sold + rng.random(sold.shape) * 0.0).astype(int)
        ratio = np.where(dem > 0, stock / np.maximum(dem + (sold - sold0).clip(0), 1), 1.0); avail = avail_from_ratio(ratio)
        left = np.maximum(stock - sold, 0); wasted = np.where(perish[None, :] == 1, np.floor(left * 0.5), 0)
        sales_hist[d] = sold
        rows.append(pd.DataFrame({"date": date, "store_id": np.repeat(np.arange(N_STORES), N_SKU), "sku_id": np.tile(np.arange(N_SKU), N_STORES), "gsku_id": np.tile(gsku, N_STORES),
                                  "category": np.tile(cat, N_STORES), "perishable": np.tile(perish, N_STORES), "price_inr": np.tile(price, N_STORES), "promo": promo.ravel().astype(int),
                                  "rain": int(rain_days[d]), "festival": festival[d], "opening_stock": stock.ravel().astype(int), "units_sold": sold.ravel(), "avail_share": avail.round(3).ravel(),
                                  "wasted_units": wasted.ravel().astype(int), "_true_demand": dem.ravel()}))
    df = pd.concat(rows, ignore_index=True)
    # data-quality defects
    df.loc[df.sample(n=3000, random_state=seed).index, "avail_share"] = np.nan                          # availability logging gap
    df = pd.concat([df, df.sample(n=2000, random_state=seed + 1)], ignore_index=True)
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs07"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs07", "store_sku_days.csv.gz"), index=False)
    dd = d.drop_duplicates(["date", "store_id", "sku_id"]); print(len(dd), "rows | stock-out days", (dd.avail_share < 0.999).mean().round(3), "| mean avail", dd.avail_share.mean().round(3))
    print("sales/demand", (dd.units_sold.sum() / dd._true_demand.sum()).round(3), "| wasted share of stock (perishables)", (dd[dd.perishable == 1].wasted_units.sum() / dd[dd.perishable == 1].opening_stock.sum()).round(3))
    w = dd.assign(w=(dd.date - dd.date.min()).dt.days // 21).groupby("w").agg(sales=("units_sold", "sum"), demand=("_true_demand", "sum"), stock=("opening_stock", "sum")); print((w.sales / w.demand).round(3).to_dict(), (w.stock / w.demand).round(3).to_dict())
