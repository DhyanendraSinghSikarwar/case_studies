import os, tempfile, warnings, logging
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
import numpy as np, pandas as pd, whylogs as why
from whylogs.viz.drift.column_drift_algorithms import calculate_drift_scores

rng = np.random.default_rng(39)
def batch(n, mean, scale=1.0):
    return pd.DataFrame({"amount": rng.lognormal(mean, 0.5 * scale, n),
                         "age": rng.normal(40, 10, n),
                         "channel_code": rng.choice([0, 1, 2], n, p=[.5, .3, .2])})  # ints on purpose: string columns hit an np.unicode_ error on numpy 2 here
ref = batch(50000, 3.0)
days = [batch(50000, 3.0), batch(50000, 3.0), batch(50000, 3.3)]   # day 3 amount shifted
print("whylogs", why.__version__, "| pandas", pd.__version__)
ref_view = why.log(ref).view()
views = [why.log(d).view() for d in days]
merged = views[0]
for v in views[1:]: merged = merged.merge(v)
print("merged rows (count of amount):", merged.get_column("amount").get_metric("counts").n.value)
for name, tgt in [("day1", views[0]), ("day3", views[2]), ("merged 3 days", merged)]:
    s = calculate_drift_scores(target_view=tgt, reference_view=ref_view, with_thresholds=True)
    print(f"{name:14s}", {k: (round(v["statistic"], 3), v["algorithm"], v["drift_category"]) for k, v in s.items() if v})
raw = sum(d.memory_usage(deep=True).sum() for d in days)
d = tempfile.mkdtemp(); p = os.path.join(d, "merged.bin"); merged.write(p)
print("raw bytes in memory (3 days):", int(raw), "| merged profile file bytes:", os.path.getsize(p), "| ratio raw/profile: %.0f" % (raw / os.path.getsize(p)))
