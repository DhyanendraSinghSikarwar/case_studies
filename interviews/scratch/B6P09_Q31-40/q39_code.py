import numpy as np
from math import sqrt

total, regions, lastclick = 100_000_000, 50, 1_000_000
per_region = total / regions
drop = 0.04
print("sales per region", per_region, "| last-click share", lastclick / total)
assert per_region == 2_000_000 and lastclick / total == 0.01
# reading A: with-video sales are the base (kept regions); paused regions sell 96% of that
inc_A = total * drop
print("A: incremental sales if 4% of with-video sales:", inc_A, "| vs last-click", inc_A / lastclick, "x")
assert inc_A == 4_000_000 and inc_A / lastclick == 4.0
# base check: the 100,000,000 is the with-video level in every region; paused regions then sell 96% of 2,000,000
observed = 40 * per_region + 10 * per_region * 0.96
print("observed total in the test period", observed, "| counterfactual with video everywhere", total, "| incremental", total - observed, "(this is the 10 paused regions only)")
print("incremental as a share of the no-video level:", round(total / (total * 0.96) - 1, 4))
assert observed == 99_200_000 and round(total / (total * 0.96) - 1, 4) == 0.0417
# the 4% measured on 10 regions: projection to 50 assumes uniform effect
print("10 paused regions lost", 10 * per_region * drop, "in the test period; scaled x5 =", 5 * 10 * per_region * drop)
assert 10 * per_region * drop == 800_000 and 5 * 10 * per_region * drop == 4_000_000
# uncertainty (invented): region-level relative noise sd after matching on pre-period
for sd in (0.02, 0.03, 0.06):
    se = sd * sqrt(1 / 10 + 1 / 40)
    lo, hi = drop - 1.96 * se, drop + 1.96 * se
    print(f"region-level sd {sd:.0%}: se {se:.4f} | 95% interval {lo:.3%} to {hi:.3%} -> {lo*total:,.0f} to {hi*total:,.0f} | z {drop/se:.1f}")
assert round(0.03 * sqrt(0.125), 4) == 0.0106
# when does the interval reach the last-click 1%? credit 1,000,000 = 1% of sales
# simulate random 10-of-50 assignments: unadjusted vs pre-period-adjusted estimate
rng = np.random.default_rng(39)
size = rng.lognormal(0, 0.5, regions); size = size / size.mean() * per_region        # unequal regions
pre = size * np.exp(rng.normal(0, 0.03, regions))
true_eff = 0.04
est_raw, est_adj = [], []
for _ in range(4000):
    t = rng.permutation(regions)[:10]; c = np.setdiff1d(np.arange(regions), t)
    post = pre * np.exp(rng.normal(0, 0.03, regions)) * (1 - true_eff * np.isin(np.arange(regions), t))
    ratio_t = post[t].sum() / pre[t].sum(); ratio_c = post[c].sum() / pre[c].sum()
    est_adj.append(1 - ratio_t / ratio_c)                                              # change vs own pre-period
    est_raw.append(1 - post[t].mean() / post[c].mean())                                # levels only
est_raw, est_adj = np.array(est_raw), np.array(est_adj)
print("simulated 4,000 random assignments, true effect 4%:")
print("  level comparison: mean", round(est_raw.mean(), 4), "sd", round(est_raw.std(), 4))
print("  versus-own-pre-period: mean", round(est_adj.mean(), 4), "sd", round(est_adj.std(), 4))
assert est_adj.std() < est_raw.std() and abs(est_adj.mean() - 0.04) < 0.003
# share of assignments in which the estimate is below the last-click 1% credit level
print("share of assignments with estimated effect below 1%:", round((est_adj < 0.01).mean(), 4), "(adjusted) |", round((est_raw < 0.01).mean(), 4), "(unadjusted)")
