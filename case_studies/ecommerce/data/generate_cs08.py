"""
SYNTHETIC DATA GENERATOR - CASE STUDY 8 (marketplace price elasticity and discount efficacy)
============================================================================================
THIS DATA IS SYNTHETIC. No marketplace publishes its price and unit data, and the evidence for this case is weak:
the only public source (arXiv 2005.04612, Singhania et al. 2020) is an outside academic study of public Flipkart
Summer Sale mobile-phone prices, with no sales data. Everything below is our assumption, not a company fact.

Simulation: 600 SKUs in 8 categories (75 each) x 52 weeks.
  * Each SKU has a hidden true price elasticity (category mean + SKU noise, e.g. mobiles -1.4, accessories -2.6).
  * Demand: log units = SKU level + season + sale-event traffic + elasticity * log(price / base price)
            + 0.25 * competitor price gap + AR(1) unobserved demand shock - post-promotion dip.
  * Price endogeneity: sellers raise prices after strong weeks (0.25 x last week's demand shock), match competitor
    prices (0.3), pass on supplier-cost shocks (0.8; this is the instrument), and discount in 4 sale-event weeks.
  * Post-promotion dip: a promotion pulls demand forward; the next two weeks lose part of it.
  * MRP inflation: 30% of SKUs show an inflated list price, so their displayed discount is large even with no sale.
  * A randomised price experiment: 120 SKUs, weeks 43-50, price -10% / 0% / +10% drawn at random each SKU-week.
  * Data-quality defects: duplicates, missing prices, prices in paise, negative units (returns), stock-outs.
Hidden truth columns start with "_".

Outputs: data/cs08/panel.csv.gz, data/cs08/skus.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
N_PER_CAT, T = 75, 52
EVENTS = {5: "Republic Day sale", 14: "Summer sale", 30: "Monsoon sale", 36: "Festive pre-sale"}
EXP_WEEKS = list(range(43, 51)); N_EXP = 120
CATS = [("Mobiles", -1.4, 14000, 22), ("Mobile accessories", -2.6, 600, 60), ("Apparel", -2.2, 900, 50), ("Footwear", -2.0, 1500, 40),
        ("Home & kitchen", -1.8, 1200, 35), ("Beauty", -1.7, 450, 45), ("Small appliances", -1.6, 2500, 28), ("Books & stationery", -2.4, 350, 55)]


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    S = N_PER_CAT * len(CATS); cat = np.repeat(np.arange(len(CATS)), N_PER_CAT)
    tier = rng.choice(3, S, p=[0.4, 0.4, 0.2]); eps = np.array([CATS[c][1] for c in cat]) + rng.normal(0, 0.35, S) + np.where(tier == 2, 0.35, np.where(tier == 0, -0.15, 0))
    eps = np.clip(eps, -4.5, -0.5)
    base_p = np.round(np.exp(np.log([CATS[c][2] for c in cat]) + rng.normal(0, 0.5, S)))
    infl = rng.random(S) < 0.30
    mrp = np.round(np.where(infl, base_p * (1 + rng.uniform(0.40, 0.80, S)), base_p * (1 + rng.uniform(0.05, 0.15, S))))
    rating = np.clip(rng.normal(4.0, 0.35, S), 3.0, 4.9); reviews = np.round(np.exp(rng.normal(5.0, 1.2, S)))
    a = np.log([CATS[c][3] for c in cat]) + rng.normal(0, 0.7, S) + 0.3 * (rating - 4.0)
    exp_sku = np.zeros(S, bool); exp_sku[rng.choice(S, N_EXP, replace=False)] = True
    sigma_u = 0.20; rho = 0.5
    u = np.zeros((S, T)); u[:, 0] = rng.normal(0, sigma_u, S)
    for t in range(1, T): u[:, t] = rho * u[:, t - 1] + rng.normal(0, sigma_u * np.sqrt(1 - rho ** 2), S)
    z = rng.normal(0, 0.05, (S, T)); comp = rng.normal(0, 0.05, (S, T))
    ev = np.zeros(T); boost = np.zeros(T)
    for w in EVENTS: ev[w - 1] = 1; boost[w - 1] = 0.30 + rng.normal(0, 0.03)
    season = 0.10 * np.sin(2 * np.pi * np.arange(T) / 52)
    promo = np.zeros((S, T)); part = rng.random((S, T)) < 0.70
    for t in range(T):
        if ev[t]: promo[:, t] = np.where(part[:, t], np.log(1 - rng.uniform(0.18, 0.32, S)), 0)
        else: promo[:, t] = np.where(rng.random(S) < 0.06, np.log(1 - rng.uniform(0.15, 0.30, S)), 0)
    arm = np.full((S, T), np.nan)
    for w in EXP_WEEKS: arm[exp_sku, w - 1] = rng.choice([np.log(0.9), 0.0, np.log(1.1)], exp_sku.sum())
    ulag = np.concatenate([np.zeros((S, 1)), u[:, :-1]], 1)
    m = promo + 0.8 * z + 0.3 * comp + 0.25 * ulag + rng.normal(0, 0.02, (S, T))
    isexp = ~np.isnan(arm); m = np.where(isexp, np.nan_to_num(arm), m); promo_eff = np.where(isexp, np.minimum(np.nan_to_num(arm), 0), np.where(promo < -0.10, promo, 0))
    pl1 = np.concatenate([np.zeros((S, 1)), promo_eff[:, :-1]], 1); pl2 = np.concatenate([np.zeros((S, 2)), promo_eff[:, :-2]], 1)
    dip = 0.7 * (-pl1) + 0.3 * (-pl2)
    base = a[:, None] + season[None, :] + boost[None, :] + 0.25 * comp + u
    mu = np.exp(base + eps[:, None] * m - dip); mu_cf = np.exp(base + eps[:, None] * (m - promo_eff))
    units = rng.poisson(mu * rng.gamma(40, 1 / 40, (S, T))).astype(float)
    stock = rng.random((S, T)) > 0.03; units = np.where(stock, units, np.floor(units * rng.uniform(0, 0.4, (S, T))))
    price = np.round(base_p[:, None] * np.exp(m))
    rows = pd.DataFrame({"sku_id": np.repeat(np.arange(S), T), "week": np.tile(np.arange(1, T + 1), S)})
    rows["category"] = np.repeat([CATS[c][0] for c in cat], T); rows["price_inr"] = price.ravel(); rows["mrp_inr"] = np.repeat(mrp, T)
    rows["competitor_price_inr"] = np.round(base_p[:, None] * np.exp(comp)).ravel(); rows["supplier_cost_index"] = np.round(np.exp(z), 4).ravel()
    rows["units"] = units.ravel(); rows["in_stock"] = stock.ravel().astype(int); rows["sale_event"] = np.tile(ev, S).astype(int)
    rows["event_name"] = np.tile([EVENTS.get(t + 1, "") for t in range(T)], S); rows["exp_arm"] = np.where(isexp.ravel(), np.select([arm.ravel() < -0.01, arm.ravel() > 0.01], ["cut10", "raise10"], "control"), "")
    rows["_mu"] = mu.ravel(); rows["_mu_cf"] = mu_cf.ravel(); rows["_promo_m"] = promo_eff.ravel(); rows["_u"] = u.ravel(); rows["_base_price"] = np.repeat(base_p, T); rows["_eps"] = np.repeat(eps, T)
    skus = pd.DataFrame({"sku_id": np.arange(S), "category": [CATS[c][0] for c in cat], "brand_tier": tier, "rating": np.round(rating, 1), "review_count": reviews, "in_price_experiment": exp_sku.astype(int),
                         "_true_elasticity": eps, "_base_price_inr": base_p, "_mrp_inflated": infl.astype(int)})
    # data-quality defects
    n = len(rows); miss = rng.choice(n, int(0.015 * n), replace=False); rows.loc[miss, "price_inr"] = np.nan
    pais = rng.choice(np.setdiff1d(np.arange(n), miss), int(0.003 * n), replace=False); rows.loc[pais, "price_inr"] *= 100
    neg = rng.choice(n, 20, replace=False); rows.loc[neg, "units"] = -rng.integers(1, 6, 20)
    rows = pd.concat([rows, rows.sample(n=600, random_state=seed)], ignore_index=True).sample(frac=1, random_state=seed).reset_index(drop=True)
    return rows, skus


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs08"), exist_ok=True)
    p, s = generate(); p.to_csv(os.path.join(here, "cs08", "panel.csv.gz"), index=False); s.to_csv(os.path.join(here, "cs08", "skus.csv.gz"), index=False)
    print(p.shape, s.shape, "mean units", p.units.mean().round(1), "mean true eps", s._true_elasticity.mean().round(2))
