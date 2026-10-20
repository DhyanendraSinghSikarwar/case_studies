"""
SYNTHETIC DATA GENERATOR - CASE STUDY 11 (Myntra-style cold-start demand forecasting for new fashion items)
===========================================================================================================
THIS DATA IS SYNTHETIC. Myntra's style-level sales are confidential.

Documented context (Singh, Gupta, Jha, Rajan, Myntra Designs, arXiv 1907.01960, 2019): about 1 million styles listed at any
time; five article types (Shirts, Casual Shoes, Kurtas, Tops, Tshirts); weekly style sales; series of 4 to 104 weeks;
attributes (colour, material ...), merchandising (discount deviation from brand/platform average, list-page visibility
ratio, days to/from promotions), time (style age, trend, three Fourier seasonality terms), cannibalisation (styles listed
per week, per brand, in similar price ranges). Split by launch date (train = first-year launches, validation = next 6
months, test = following 6 months). Test wMAPE of the naive baseline was about 1.0 and of the best XGBoost 0.51 to 0.60.

Simulation (a calibrated stand-in, NOT the paper's data):
  * 9,000 styles across the five article types launched over 104 weeks; each lives 4 to 26 weeks; calendar of 130 weeks.
  * log-demand = type level + brand + colour (with a slow random-walk colour trend) + material + pattern + price band
    + hidden style quality + Fourier seasonality + launch hype and age decay + discount-deviation effect + visibility effect
    + promotion-week effect - cannibalisation (styles listed in the same type and price band, and by the same brand).
  * Visibility depends on the hidden quality (the platform shows what sells), so a naive driver analysis is biased.
  * Weekly units = Poisson(mu * Gamma noise), i.e. overdispersed counts.
Hidden truth columns are prefixed "_": _quality (style), _mu (true expected weekly units).
Built-in data defects: duplicate weekly rows, missing visibility and discount, messy colour labels, bulk-order outliers,
sales dated before launch, negative net sales (returns).

Outputs: data/cs11/styles.csv.gz, data/cs11/weekly_sales.csv.gz, data/cs11/promo_weeks.csv
"""
import os
import numpy as np
import pandas as pd

SEED = 42
N_STYLES, WEEKS, LAUNCH_WEEKS = 9_000, 130, 104
TYPES = ["Shirts", "Casual Shoes", "Kurtas", "Tops", "Tshirts"]
SHARE = [0.22, 0.12, 0.18, 0.20, 0.28]
BASE = [11.0, 8.0, 9.0, 10.0, 13.0]       # typical weekly units level per type (before effects)
COLOURS = ["black", "white", "navy blue", "red", "olive", "maroon", "grey", "beige", "pink", "mustard", "teal", "brown"]
MATERIALS = ["cotton", "polyester", "linen", "denim", "rayon", "synthetic"]
PATTERNS = ["solid", "striped", "printed", "checked", "embroidered"]


def promo_calendar():
    """Weeks (0-129) with a platform sale event: the end-of-season sale weeks and the festive sale each year."""
    woy = np.arange(WEEKS) % 52
    return np.where(np.isin(woy, [1, 2, 25, 26, 40, 41, 42, 49]))[0]


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    ptype = rng.choice(len(TYPES), N_STYLES, p=SHARE)
    brand = rng.integers(0, 40, N_STYLES); tier_of_brand = rng.choice(3, 40, p=[0.4, 0.4, 0.2])
    tier = tier_of_brand[brand]; band = np.clip(tier + rng.choice([-1, 0, 0, 1], N_STYLES), 0, 2)
    colour = rng.integers(0, len(COLOURS), N_STYLES); material = rng.integers(0, len(MATERIALS), N_STYLES); pattern = rng.integers(0, len(PATTERNS), N_STYLES)
    price = np.round(np.exp(rng.normal(np.log([600, 1400, 900, 700, 550])[ptype] * np.array([0.65, 1.0, 1.7])[band], 0.25)), -1)
    launch = rng.integers(0, LAUNCH_WEEKS, N_STYLES)
    life = 4 + np.minimum(22, rng.geometric(0.11, N_STYLES) - 1)
    quality = rng.normal(0, 0.65, N_STYLES)
    # effects
    brand_eff = rng.normal(0, 0.30, 40) + np.array([-0.15, 0.05, 0.25])[tier_of_brand]
    col_eff = rng.normal(0, 0.22, len(COLOURS)); col_type = rng.normal(0, 0.12, (len(TYPES), len(COLOURS)))
    mat_eff = rng.normal(0, 0.18, len(MATERIALS)); pat_eff = rng.normal(0, 0.14, len(PATTERNS)); band_eff = np.array([0.15, 0.0, -0.25])
    walk = np.cumsum(rng.normal(0, 0.035, (len(COLOURS), WEEKS)), axis=1)             # slow colour trend drift
    fcoef = rng.normal(0, 0.12, (len(TYPES), 3, 2))
    promo = promo_calendar()
    # expand to the style-week panel
    sid = np.repeat(np.arange(N_STYLES), life); age = np.concatenate([np.arange(l) for l in life]); week = launch[sid] + age
    keep = week < WEEKS; sid, age, week = sid[keep], age[keep], week[keep]
    pt, bd, br, cl = ptype[sid], band[sid], brand[sid], colour[sid]
    # cannibalisation counts
    cnt = np.zeros((len(TYPES), 3, WEEKS)); np.add.at(cnt, (pt, bd, week), 1)
    cnt_b = np.zeros((40, WEEKS)); np.add.at(cnt_b, (br, week), 1)
    n_tb, n_br = cnt[pt, bd, week], cnt_b[br, week]
    # merchandising
    is_promo = np.isin(week, promo)
    disc = rng.normal(0, 7.0, len(sid)) + 9.0 * is_promo + 2.5 * np.exp(-age / 3.0)       # percentage-point deviation
    vis = np.exp(0.40 * quality[sid] + 0.28 * rng.normal(size=len(sid)) - 0.02 * age)
    vis = vis / vis.mean()
    f = np.zeros(len(sid)); woy = 2 * np.pi * (week % 52) / 52
    for h in range(3): f += fcoef[pt, h, 0] * np.sin((h + 1) * woy) + fcoef[pt, h, 1] * np.cos((h + 1) * woy)
    eta = (np.log(np.array(BASE))[pt] + brand_eff[br] + col_eff[cl] + col_type[pt, cl] + walk[cl, week] + mat_eff[material[sid]] + pat_eff[pattern[sid]] + band_eff[bd]
           + quality[sid] + f + 0.45 * np.exp(-age / 2.5) - 0.045 * age + 0.022 * disc + 0.50 * np.log(np.maximum(vis, 0.05)) + 0.22 * is_promo
           - 0.14 * np.log(n_tb / 25.0) - 0.06 * np.log(np.maximum(n_br, 1)))
    mu = np.exp(eta)
    units = rng.poisson(mu * rng.gamma(5.0, 1 / 5.0, len(sid)))
    panel = pd.DataFrame({"style_id": sid, "week": week, "units_sold": units, "discount_dev_pp": np.round(disc, 1), "visibility_ratio": np.round(vis, 3), "_mu": np.round(mu, 3)})
    styles = pd.DataFrame({"style_id": np.arange(N_STYLES), "article_type": np.array(TYPES)[ptype], "brand_id": brand, "brand_tier": np.array(["value", "mid", "premium"])[tier],
                           "price_band": np.array(["low", "mid", "high"])[band], "list_price_inr": price, "colour": np.array(COLOURS)[colour], "material": np.array(MATERIALS)[material],
                           "pattern": np.array(PATTERNS)[pattern], "launch_week": launch, "_quality": np.round(quality, 3)})
    # ---- data-quality defects ----
    out = rng.choice(len(panel), 40, replace=False); panel.loc[out, "units_sold"] = (panel.loc[out, "units_sold"] + 5) * 25
    neg = rng.choice(len(panel), 30, replace=False); panel.loc[neg, "units_sold"] = -rng.integers(1, 6, 30)
    early = rng.choice(np.where(launch[panel.style_id.values] >= 3)[0], 60, replace=False); sid_e = panel.loc[early, "style_id"].values
    panel.loc[early, "week"] = np.maximum(launch[sid_e] - rng.integers(1, 4, 60), 0)
    panel["visibility_ratio"] = panel["visibility_ratio"].mask(rng.random(len(panel)) < 0.025)
    panel["discount_dev_pp"] = panel["discount_dev_pp"].mask(rng.random(len(panel)) < 0.010)
    dup = panel.iloc[rng.choice(len(panel), 1500, replace=False)]
    panel = pd.concat([panel, dup], ignore_index=True).sample(frac=1.0, random_state=seed).reset_index(drop=True)
    messy = rng.random(N_STYLES) < 0.04; styles.loc[messy, "colour"] = styles.loc[messy, "colour"].str.title() + " "
    return styles, panel


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs11"), exist_ok=True)
    s, p = generate(); s.to_csv(os.path.join(here, "cs11", "styles.csv.gz"), index=False); p.to_csv(os.path.join(here, "cs11", "weekly_sales.csv.gz"), index=False)
    pd.DataFrame({"week": promo_calendar()}).to_csv(os.path.join(here, "cs11", "promo_weeks.csv"), index=False)
    q = p.drop_duplicates(["style_id", "week"]); q = q[(q.units_sold >= 0) & (q.units_sold < 1000)]
    print(len(s), "styles |", len(p), "rows | mean weekly units", round(q.units_sold.mean(), 2), "| median", q.units_sold.median(), "| p99", q.units_sold.quantile(0.99))
    ok = q.merge(s[["style_id", "launch_week"]], on="style_id"); tr = ok[ok.launch_week < 52]; te = ok[ok.launch_week >= 78]
    mt = tr.units_sold.mean(); print("naive wMAPE (train-mean) on test:", round(np.abs(te.units_sold - mt).sum() / te.units_sold.sum(), 3), "| oracle (true mu) wMAPE:", round(np.abs(te.units_sold - te._mu).sum() / te.units_sold.sum(), 3))
