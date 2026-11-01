# Q45: unit cost model, 5 models, growth and spike, thresholds, sensitivity. Abstract units.
models = {  # monthly predictions, compute/1k, storage, transfer, monitoring, people, idle share
 "m1": dict(preds=50e6, c1k=0.8, stor=20, xfer=10, mon=5, ppl=3000, idle=0.30),
 "m2": dict(preds=5e6,  c1k=2.0, stor=5,  xfer=2,  mon=5, ppl=3000, idle=0.50),
 "m3": dict(preds=200e6,c1k=0.2, stor=40, xfer=30, mon=8, ppl=3000, idle=0.15),
 "m4": dict(preds=1e6,  c1k=5.0, stor=2,  xfer=1,  mon=5, ppl=2000, idle=0.60),
 "m5": dict(preds=20e6, c1k=1.0, stor=10, xfer=5,  mon=5, ppl=2500, idle=0.25),
}
def monthly(m, growth=0.0, mult=1.0):
    p = m["preds"] * (1 + growth) * mult
    comp = p / 1000 * m["c1k"]; comp *= 1 / (1 - m["idle"])       # idle capacity is paid, spread over used
    return comp + m["stor"] + m["xfer"] * (1 + growth) * mult + m["mon"] + m["ppl"], p
print(f"{'model':6s}{'cost/mo':>10s}{'cost per 1k preds':>20s}")
tot = 0
for k, m in models.items():
    c, p = monthly(m); tot += c; print(f"{k:6s}{c:10.1f}{c/p*1000:20.4f}")
print(f"total/month {tot:.1f}")
# forecast: 2%/month growth for 12 months, plus spike (3x for 1 month in month 6)
budget = 0; series = []
for mth in range(1, 13):
    g = 1.02 ** mth - 1; mult = 3.0 if mth == 6 else 1.0
    c = sum(monthly(m, g, mult)[0] for m in models.values()); series.append(c)
budget = sum(sum(monthly(m, 1.02 ** x - 1)[0] for m in models.values()) for x in range(1, 13))
print(f"year budget (no spike) {budget:.0f}; with spike {sum(series):.0f}; spike month {series[5]:.0f}")
alert_budget = budget / 12 * 1.15
print("budget alert threshold per month:", round(alert_budget, 1), "| anomaly rule: month > 1.5 x trailing 3-mo mean")
for mth, c in enumerate(series, 1):
    trail = sum(series[max(0, mth-4):mth-1]) / max(1, len(series[max(0, mth-4):mth-1]))
    if mth > 1 and (c > alert_budget or c > 1.5 * trail): print(f"  month {mth}: ALERT cost {c:.0f} (budget flag {c>alert_budget}, anomaly {c>1.5*trail})")
print("sensitivity of total/month to: idle +20pts / people +20% / compute/1k +50%")
def total(f): return sum(f(dict(m))[0] if False else monthly(f(dict(m)))[0] for m in models.values())
def idle_up(m): m["idle"] = min(0.9, m["idle"] + 0.2); return m
def ppl_up(m): m["ppl"] *= 1.2; return m
def c_up(m): m["c1k"] *= 1.5; return m
for n, f in [("idle", idle_up), ("people", ppl_up), ("compute/1k", c_up)]: print(f"  {n:11s} {total(f)/tot:5.3f} x base")
print("worth-its-cost: ask Book 6 owner for value per prediction, then value_per_pred > cost_per_pred")
