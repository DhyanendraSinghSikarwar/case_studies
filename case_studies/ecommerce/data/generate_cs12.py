"""
SYNTHETIC DATA GENERATOR - CASE STUDY 12 (hierarchical, probabilistic demand forecasting; CLOVER-style)
======================================================================================================
THIS DATA IS SYNTHETIC. Supply-chain demand data of Amazon or Flipkart is confidential. CLOVER (arXiv 2307.09797)
uses six public datasets, not Amazon production data. Flipkart's Central Planning Platform is known only through a
third-party summary. Nothing here reproduces either system.

Simulation: weekly unit demand for a national retailer, 208 weeks (Jan 2022 to Dec 2025).
Hierarchy: Total (1) > Region (4) > Fulfilment centre (16) > FC x Category (96 bottom series). 117 nodes in all.
  * Level: FC size and category mix differ a lot (weekly means from about 5 to 900 units).
  * Seasonality: yearly Fourier shape per category, plus festive weeks (Republic Day sale, Big Billion Days / Diwali,
    year-end) with category-specific lifts. Category trends differ.
  * Dependence (the point of the case): the log-demand carries shared AR(1) shocks at national, region, category
    and FC level, so bottom series are positively correlated, and aggregates are NOT as noisy as independent
    series would imply (or as quiet).
  * Counts: negative binomial around exp(log-demand).
Built-in messiness: 3 FC outages (all categories reported as 0 for 2 to 3 weeks), 12 keying errors (x10), 150 duplicate rows.
Hidden truth (prefix _): true mean, shock components.

Outputs (written by the notebook): data/cs12/demand_weekly.csv.gz, data/cs12/hierarchy.csv
"""
import numpy as np
import pandas as pd

SEED = 42
START = pd.Timestamp("2022-01-03"); T = 208
REGIONS = ["North", "South", "West", "East"]
FCS = {"North": ["Delhi", "Gurugram", "Lucknow", "Ludhiana"], "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi"],
       "West": ["Mumbai", "Pune", "Ahmedabad", "Jaipur"], "East": ["Kolkata", "Patna", "Bhubaneswar", "Guwahati"]}
CATS = ["Mobiles", "Fashion", "Home & Kitchen", "Grocery & FMCG", "Beauty", "Electronics accessories"]
# (base weekly units per FC, yearly trend (log/yr), seasonal amplitude, Republic Day lift, BBD/Diwali lift, year-end lift)
CATP = {"Mobiles": (60, 0.06, 0.08, 0.15, 0.60, 0.10), "Fashion": (120, 0.10, 0.20, 0.25, 0.45, 0.20),
        "Home & Kitchen": (45, 0.08, 0.10, 0.20, 0.50, 0.05), "Grocery & FMCG": (260, 0.14, 0.05, 0.02, 0.15, 0.10),
        "Beauty": (30, 0.18, 0.12, 0.10, 0.35, 0.25), "Electronics accessories": (14, 0.04, 0.06, 0.10, 0.40, 0.08)}


def _ar1(rng, n, rho, sd):
    e = rng.normal(0, sd * np.sqrt(1 - rho ** 2), n); x = np.zeros(n); x[0] = rng.normal(0, sd)
    for i in range(1, n):
        x[i] = rho * x[i - 1] + e[i]
    return x


def festive(dates):
    wk = dates.isocalendar().week.values.astype(int)
    return {"republic": np.isin(wk, [3, 4]).astype(float), "bbd": np.isin(wk, [40, 41, 42, 43]).astype(float) * np.array([0.6, 1.0, 1.0, 0.8])[np.clip(wk - 40, 0, 3)],
            "yearend": np.isin(wk, [51, 52]).astype(float)}


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    dates = pd.date_range(START, periods=T, freq="W-MON"); t = np.arange(T); fe = festive(dates); doy = dates.dayofyear.values / 365.25
    nat = _ar1(rng, T, 0.80, 0.05); reg = {r: _ar1(rng, T, 0.75, 0.06) for r in REGIONS}; cat_sh = {c: _ar1(rng, T, 0.75, 0.07) for c in CATS}
    rows, hier = [], []
    for r in REGIONS:
        for f in FCS[r]:
            size = np.exp(rng.normal(0, 0.55)) * {"North": 1.1, "South": 1.0, "West": 1.25, "East": 0.7}[r]; fcs = _ar1(rng, T, 0.70, 0.05)
            for c in CATS:
                base, tr, amp, rl, bl, yl = CATP[c]; mixj = np.exp(rng.normal(0, 0.35)); phase = rng.uniform(0, 1)
                seas = amp * np.sin(2 * np.pi * (doy + phase * 0.15)) + 0.5 * amp * np.cos(4 * np.pi * doy)
                own = _ar1(rng, T, 0.5, 0.04)
                lm = np.log(base * size * mixj) + tr * t / 52.0 + seas + rl * fe["republic"] + bl * fe["bbd"] + yl * fe["yearend"] + nat + reg[r] + cat_sh[c] + fcs + own
                mu = np.exp(lm); theta = 25.0
                y = rng.negative_binomial(theta, theta / (theta + mu))
                rows.append(pd.DataFrame({"week": dates, "region": r, "fc": f, "category": c, "units": y, "_mu": mu}))
                hier.append((r, f, c))
    df = pd.concat(rows, ignore_index=True)
    # messiness: FC outages (reported zero for all categories), keying errors, duplicate rows
    out_specs = [("Patna", 60, 3), ("Kochi", 118, 2), ("Pune", 146, 3)]
    for fc, w0, n in out_specs:
        m = (df.fc == fc) & df.week.isin(dates[w0:w0 + n]); df.loc[m, "units"] = 0
    idx = rng.choice(np.where(df.units > 5)[0], 12, replace=False); df.loc[idx, "units"] = df.loc[idx, "units"] * 10
    dup = df.sample(150, random_state=seed); df = pd.concat([df, dup], ignore_index=True).sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return df, pd.DataFrame(hier, columns=["region", "fc", "category"])


if __name__ == "__main__":
    d, h = generate()
    print(d.shape, d.units.describe())
