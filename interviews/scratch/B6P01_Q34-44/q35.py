# Q35 push cap of 3/day (illustrative segment model + seeded readout)
import numpy as np
rng = np.random.default_rng(35)
# segment: share, pushes/day now, sessions-per-push (marginal for pushes above the cap), opt-out per 100 pushes above cap
segs = {
 "new users (<14d)":   (0.15, 2.0, 0.060, 0.30),
 "regular users":      (0.55, 3.0, 0.030, 0.10),
 "heavy-notified":     (0.20, 6.0, 0.020, 0.45),
 "txn/time-sensitive": (0.10, 4.0, 0.150, 0.05),   # e.g. delivery or price alerts, cap drops useful ones
}
cap = 3
tot_lost = 0.0; tot_saved_optouts = 0.0; base_pushes = 0.0
print(f"{'segment':20}{'pushes/d':>9}{'dropped/d':>10}{'sess lost/user/d':>18}{'optouts saved/1000u/d':>23}")
for k, (sh, p, spp, oo) in segs.items():
    dropped = max(0.0, p - cap)
    lost = dropped * spp
    saved = dropped * oo / 100 * 1000
    tot_lost += sh * lost; tot_saved_optouts += sh * saved; base_pushes += sh * p
    print(f"{k:20}{p:9.1f}{dropped:10.1f}{lost:18.3f}{saved:23.2f}")
print(f"avg pushes/day now {base_pushes:.2f}; avg sessions lost per user per day {tot_lost:.4f}")
assert round(base_pushes, 2) == 3.55
assert abs(tot_lost - 0.0270) < 1e-9

# seeded readout: sessions/user/week 7-day, control vs capped; decision rule pre-registered
n = 50_000
ctrl = rng.poisson(8.0, n)
attributed_week = tot_lost * 7                 # push-attributed sessions lost per user per week
incremental_share = 0.27                      # invented: share that would not have happened anyway
print(f"push-attributed loss {attributed_week:.3f}/user/week; net after substitution {attributed_week*incremental_share:.3f}")
assert abs(attributed_week*incremental_share - 0.051) < 0.001
trt = rng.poisson(8.0 - attributed_week*incremental_share, n)
d = (trt.mean()-ctrl.mean())/ctrl.mean()
se = np.sqrt(trt.var(ddof=1)/n+ctrl.var(ddof=1)/n)/ctrl.mean()
lo, hi = d-1.96*se, d+1.96*se
print(f"sessions/user rel change {d:+.2%} CI [{lo:+.2%}, {hi:+.2%}]")
reject = lo < -0.02          # reject if the lower bound is worse than -2%
print("reject cap on sessions guardrail (lower bound < -2%):", reject)
assert not reject
