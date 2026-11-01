import numpy as np, pandas as pd
from scipy.stats import ks_2samp, chi2_contingency, wasserstein_distance
from scipy.spatial.distance import jensenshannon

def kind_of(s, hint=None):
    if hint: return hint
    if pd.api.types.is_datetime64_any_dtype(s): return "timestamp"
    if s.dtype == bool or s.nunique() <= 2: return "binary"
    if s.dtype == object or str(s.dtype) in ("category", "str", "string"):
        return "high_card" if s.nunique() > 20 else "categorical"
    if pd.api.types.is_integer_dtype(s) and s.nunique() <= 30: return "count"
    return "numeric"

def shares(ref, cur, top=10):
    keep = ref.value_counts().index[:top]
    r = ref.where(ref.isin(keep), "OTHER").value_counts(normalize=True)
    c = cur.where(cur.isin(keep), "OTHER").value_counts(normalize=True)
    cats = r.index.union(c.index)
    return r.reindex(cats, fill_value=0).values, c.reindex(cats, fill_value=0).values

def drift(ref, cur, hint=None):
    k = kind_of(ref, hint)
    if k == "numeric":
        ks = ks_2samp(ref, cur)
        w = wasserstein_distance(ref, cur) / ref.std()        # in reference-sd units
        return k, "KS + Wasserstein/sd", f"D={ks.statistic:.3f} W={w:.3f}", ks.pvalue < 0.001 and ks.statistic >= 0.1
    if k == "count":
        w = wasserstein_distance(ref, cur) / ref.std()
        return k, "Wasserstein/sd", f"W={w:.3f}", w >= 0.1
    if k == "binary":
        t = pd.crosstab(np.r_[np.zeros(len(ref)), np.ones(len(cur))], np.r_[ref.astype(int), cur.astype(int)])
        p = chi2_contingency(t)[1]; d = abs(cur.astype(int).mean() - ref.astype(int).mean())
        return k, "rate diff + chi2", f"diff={d:.3f}", p < 0.001 and d >= 0.03
    if k == "categorical":
        r, c = shares(ref, cur)
        js = jensenshannon(r, c, base=2)
        return k, "Jensen-Shannon", f"JS={js:.3f}", js >= 0.1
    if k == "high_card":
        r, c = shares(ref, cur, top=10)
        js = jensenshannon(r, c, base=2)
        return k, "JS on top-10+OTHER", f"JS={js:.3f}", js >= 0.1
    if k == "timestamp":
        hr = lambda s: np.bincount(s.dt.hour, minlength=24) / len(s)
        js = jensenshannon(hr(ref), hr(cur), base=2)
        lag = (ref.max() - cur.max()).total_seconds() / 3600
        return k, "JS hour-of-day + max-lag", f"JS={js:.3f} lag_h={lag:.0f}", js >= 0.1 or abs(lag) >= 6

rng = np.random.default_rng(11); n = 5000
def frame(shift):
    ids = np.array([f"m{i}" for i in range(200)])
    p = np.ones(200) / 200
    if shift: p = np.r_[np.full(10, 0.05), np.full(190, 0.5 / 190)]; p /= p.sum()
    base = pd.Timestamp("2026-01-01")
    return pd.DataFrame({
        "income":    rng.lognormal(10, 0.5, n) * (1.25 if shift else 1.0),
        "channel":   rng.choice(["web", "app", "branch", "call"], n, p=[.2, .4, .2, .2] if shift else [.4, .3, .2, .1]),
        "is_new":    rng.random(n) < (0.5 if shift else 0.3),
        "merchant":  rng.choice(ids, n, p=p),
        "n_txn_7d":  rng.poisson(8 if shift else 5, n),
        "text_len":  rng.normal(120, 30, n).round() + (0 if not shift else 40),
        "event_ts":  base + pd.to_timedelta(rng.integers(0, 24 * 3600 * 7, n) + (3600 * 12 if shift else 0), unit="s")
                     - (pd.Timedelta(hours=30) if shift else pd.Timedelta(0)),
    })
ref, cur = frame(False), frame(True)
hints = {"n_txn_7d": "count", "text_len": "numeric"}
rows = []
for col in ref.columns:
    k, test, stat, flag = drift(ref[col], cur[col], hints.get(col))
    rows.append((col, k, test, stat, "DRIFT" if flag else "ok"))
print(pd.DataFrame(rows, columns=["column", "kind", "test", "statistic", "flag"]).to_string(index=False))
# control: same data compared with a fresh unshifted sample
c0 = frame(False)
print("\ncontrol (no shift) flags:", [bool(drift(ref[c], c0[c], hints.get(c))[3]) for c in ref.columns])
