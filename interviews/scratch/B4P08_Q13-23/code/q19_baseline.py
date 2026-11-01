import numpy as np, pandas as pd
from scipy.stats import ks_2samp
rng = np.random.default_rng(19)
days = pd.date_range("2026-01-01", periods=84, freq="D")   # 12 weeks
rows = []
for d in days:
    n = 400
    weekend = d.dayofweek >= 5
    # weekend traffic: higher basket value; no real drift anywhere
    x = rng.normal(1500 if weekend else 1000, 300, n)
    rows.append(pd.DataFrame({"date": d, "dow": d.dayofweek, "amt": x}))
df = pd.concat(rows, ignore_index=True)
ref_days = df[df.date < "2026-02-01"]          # first 4 weeks
test_days = df[df.date >= "2026-02-01"]
def alerts(baseline_fn):
    hits, total = 0, 0
    for d, g in test_days.groupby("date"):
        ref = baseline_fn(d)
        p = ks_2samp(ref.amt, g.amt).pvalue
        hits += p < 0.01; total += 1
    return hits, total
# 1) baseline = the previous calendar day (rolling): flips at weekend edges
roll = lambda d: df[df.date == d - pd.Timedelta(days=1)]
# 2) baseline = a single fixed Saturday (what a careless 'golden day' looks like)
sat = df[df.date == pd.Timestamp("2026-01-03")]
fixed_sat = lambda d: sat
# 3) baseline = same weekday in the reference window
matched = lambda d: ref_days[ref_days.dow == d.dayofweek]
for name, fn in [("previous day (rolling)", roll), ("one fixed Saturday", fixed_sat), ("day-of-week matched", matched)]:
    h, t = alerts(fn)
    print(f"{name:24s} alerts {h:2d} of {t} days (nothing really changed)")
# weekday batch vs weekend reference, shown directly
wk = df[df.date == "2026-02-10"]; we = df[df.date == "2026-01-03"]
print("Tue batch vs Saturday reference: KS p =", f"{ks_2samp(we.amt, wk.amt).pvalue:.2e}")
