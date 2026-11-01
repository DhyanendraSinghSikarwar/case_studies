import numpy as np
# Illustrative numbers.
ch = {"search": dict(cac=80.0, margin=10.0, churn=0.08), "referral": dict(cac=30.0, margin=9.0, churn=0.05)}
for k, v in ch.items():
    v["ltv"] = v["margin"] / v["churn"]; v["ratio"] = v["ltv"] / v["cac"]
    v["payback"] = v["cac"] / v["margin"]
    print(f"{k:9} LTV {v['ltv']:6.1f}  LTV/CAC {v['ratio']:.2f}  simple payback {v['payback']:.1f} months")
assert (ch["search"]["ltv"], round(ch["search"]["ratio"], 4)) == (125.0, 1.5625)
assert (ch["referral"]["ltv"], ch["referral"]["ratio"]) == (180.0, 6.0)
# Churn from 3 months of data is noisy. Illustrative exposure: 1,000 searched-acquired and 400 referral customers,
# observed for 3 months each (about 2,800 and 1,100 active customer-months after churn).
rng = np.random.default_rng(7)
def churn_interval(p, months, n=100_000):
    # events ~ Binomial(months, p); churn estimate = events/months; parametric bootstrap
    ev = rng.binomial(months, p, size=n) / months
    return np.percentile(ev[ev > 0], [2.5, 97.5])
exp = {"search": 2800, "referral": 1100}
res = {}
for k, v in ch.items():
    lo, hi = churn_interval(v["churn"], exp[k])
    res[k] = (lo, hi, v["margin"] / hi / v["cac"], v["margin"] / lo / v["cac"])
    print(f"{k:9} churn 95% band {lo:.3%}-{hi:.3%}  LTV/CAC band {res[k][2]:.2f}-{res[k][3]:.2f}")
# Even at the worst referral and best search ends, referral ratio stays well above search ratio
assert res["referral"][2] > res["search"][3]
# Bigger risk than noise: 3 months of data say nothing about month 12. Check a churn that falls with tenure.
# Same 3-month average of 8% but hazard 12% early, 5% later: early-month churn can mislead LTV either way.
early, late = 0.12, 0.05
surv, ltv = 1.0, 0.0
for m in range(1, 241):
    ltv += surv * 10.0
    surv *= (1 - (early if m <= 6 else late))
print(f"search LTV with churn 12% for 6 months then 5%: {ltv:.1f} (vs 125.0 constant)")
assert round(ltv, 1) == 137.5
# Marginal CAC: if the next referral customer costs 60 (referral pool is finite), referral ratio:
print("referral LTV/CAC if marginal CAC rises to 60:", round(180 / 60, 2))
assert round(180 / 60, 2) == 3.0
