# Q40 quick-commerce tab: incremental orders vs cannibalisation (illustrative)
import numpy as np
rng = np.random.default_rng(40)
# deterministic hand-check
parent_before_t, parent_after_t = 600_000, 570_000   # launch cities, daily parent orders
parent_before_c, parent_after_c = 600_000, 590_000   # matched control cities (no tab yet)
quick = 80_000
did = (parent_after_t - parent_before_t) - (parent_after_c - parent_before_c)
naive_incr = quick - 30_000
incr = quick + did
print(f"naive incremental = {quick} - 30000 = {naive_incr}")
print(f"DiD parent effect = {did}; incremental = {incr}; incrementality share = {incr/quick:.1%}")
assert did == -20_000 and incr == 60_000 and naive_incr == 50_000 and incr / quick == 0.75

# seeded city-level simulation: 10 launch cities, 20 control cities, true cannibalisation 20k/day total
launch = 10; ctrl = 20
base = rng.normal(60_000, 8_000, launch + ctrl).clip(30_000)          # parent orders per city before
trend = -0.0167                                                         # market-wide drift
noise = rng.normal(0, 0.01, launch + ctrl)
after = base * (1 + trend + noise)
true_cannibal_per_city = 2_000
after[:launch] -= true_cannibal_per_city
d_city = after - base
did_pct = d_city[:launch].sum() - base[:launch].sum() * (d_city[launch:].sum() / base[launch:].sum())
# bootstrap over cities
est = []
for _ in range(2000):
    li = rng.integers(0, launch, launch); ci = rng.integers(0, ctrl, ctrl)
    bl, dl = base[:launch][li], d_city[:launch][li]
    bc, dc = base[launch:][ci], d_city[launch:][ci]
    est.append(dl.sum() - bl.sum() * dc.sum() / bc.sum())
lo, hi = np.percentile(est, [2.5, 97.5])
print(f"DiD cannibalisation estimate {did_pct:,.0f}/day (true -20,000), 95% bootstrap CI [{lo:,.0f}, {hi:,.0f}]")
naive_pre_post = d_city[:launch].sum()
print(f"naive pre/post parent change in launch cities: {naive_pre_post:,.0f}")
assert lo < -20_000 < hi
assert naive_pre_post < did_pct       # the pre/post view over-states the loss because of the market drift
