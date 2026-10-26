import numpy as np, pandas as pd
from scipy.stats import ks_2samp

# each monitor returns True when it fires
def null_monitor(ref, cur, col="amount", max_rate=0.02):
    return cur[col].isna().mean() > max_rate
def drift_monitor(ref, cur, col="amount", alpha=0.001, min_d=0.1):
    d = ks_2samp(ref[col].dropna(), cur[col].dropna())
    return d.pvalue < alpha and d.statistic > min_d          # significant AND big enough
def range_monitor(ref, cur, col="amount", factor=3.0):
    return cur[col].max() > factor * ref[col].max()          # catches unit changes
def volume_monitor(ref, cur, min_ratio=0.7):
    return len(cur) < min_ratio * len(ref)                   # catches dropped partitions
def category_monitor(ref, cur, col="region"):
    return bool(set(ref[col].unique()) - set(cur[col].unique()))   # a known value vanished
MONITORS = {"null": null_monitor, "drift": drift_monitor, "range": range_monitor, "volume": volume_monitor, "category": category_monitor}

# fault injection
def clean_batch(rng, n=5000):
    return pd.DataFrame({"amount": rng.lognormal(3.0, 0.5, n), "region": rng.choice(list("NSEW"), n)})
def inject(df, fault, rng):
    df = df.copy()
    if fault == "null_spike": df.loc[rng.random(len(df)) < 0.10, "amount"] = np.nan
    elif fault == "unit_change": df["amount"] = df["amount"] * 100       # rupees to paise
    elif fault == "mean_shift": df["amount"] = df["amount"] * 1.25
    elif fault == "dropped_partition": df = df[df["region"] != "W"].reset_index(drop=True)
    elif fault != "none": raise ValueError(fault)
    return df
