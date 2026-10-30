# Q30 data-quality gates for a nightly load (illustrative history)
import numpy as np
rng = np.random.default_rng(30)

print(f"yesterday {3_100_000/5_000_000:.0%} of the usual 5,000,000 rows")
assert 3_100_000 / 5_000_000 == 0.62

# 60 nights of history with a weekday pattern and noise
days = 60
dow = np.arange(days) % 7
weekday_factor = np.array([1.00, 1.02, 1.03, 1.02, 1.00, 0.92, 0.90])
hist = (5_000_000 * weekday_factor[dow] * rng.normal(1, 0.012, days)).astype(int)

def expected(hist, dow_hist, d):
    same = hist[dow_hist == d][-4:]                       # last 4 same-weekday nights
    return np.median(same)

def row_gate(count, d, hist=hist, dow_hist=dow):
    exp = expected(hist, dow_hist, d); ratio = count / exp
    if ratio < 0.90: return "BLOCK", ratio
    if ratio < 0.97 or ratio > 1.10: return "WARN", ratio
    return "PASS", ratio

# False-alarm check: run the gate on each of the last 30 nights using only earlier history
res = {"PASS": 0, "WARN": 0, "BLOCK": 0}
for t in range(30, days):
    g, _ = row_gate(hist[t], dow[t], hist[:t], dow[:t]); res[g] += 1
print("gate on 30 normal nights:", res)
assert res["BLOCK"] == 0 and res["PASS"] >= 28

# Yesterday's bad load: a Wednesday-like night (dow=2) with 3.1M rows
g, ratio = row_gate(3_100_000, 2)
print(f"bad night: {g}, ratio to same-weekday median {ratio:.2f}")
assert g == "BLOCK"
# The usual std-dev style rule on the last 30 nights (no weekday adjustment)
mu, sd = hist[-30:].mean(), hist[-30:].std()
print(f"naive z-score of the bad night: {(3_100_000-mu)/sd:.1f}; but a perfectly normal Sunday (about 4,500,000 rows) already scores z = {(4_500_000-mu)/sd:.1f}")
# A 7% hole on a normal night: warn only
g2, r2 = row_gate(int(0.93 * expected(hist, dow, 3)), 3)
print(f"7% short night: {g2} (ratio {r2:.2f})")
assert g2 == "WARN"

# Other gates as a table-driven check on a batch summary
batch = {"schema_ok": True, "null_rate_key": 0.0004, "dup_key_rate": 0.0, "partition_date_ok": True, "pos_rate": 0.081, "psi_top_feature": 0.14}
rules = [("schema_ok", lambda v: v, "BLOCK"), ("partition_date_ok", lambda v: v, "BLOCK"),
         ("null_rate_key", lambda v: v < 0.001, "BLOCK"), ("dup_key_rate", lambda v: v < 0.001, "BLOCK"),
         ("pos_rate", lambda v: 0.07 <= v <= 0.09, "WARN"), ("psi_top_feature", lambda v: v < 0.10, "WARN")]
out = [(k, sev) for k, f, sev in rules if not f(batch[k])]
print("failed rules:", out)
assert out == [("psi_top_feature", "WARN")]
