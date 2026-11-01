# Q28: switchback, 672 half-hour periods, ~900 deliveries each (illustrative simulation, seeded)
import numpy as np

rng = np.random.default_rng(28)
P, PER_DAY, DELIV = 672, 48, 900
print("periods:", P, "deliveries:", P * DELIV, "periods per arm:", P // 2)
assert P == 14 * 48 and P * DELIV == 604_800

slot = np.arange(P) % PER_DAY                    # half-hour slot of the day
tod = 3.0 * np.sin(2 * np.pi * slot / PER_DAY)   # time-of-day pattern in delivery minutes (peak and off-peak)
SD_ORDER, SD_SHOCK, PHI = 12.0, 1.5, 0.6         # SD of one delivery; SD of a market-wide period shock; shock persistence

def shocks():
    e = np.zeros(P); e[0] = rng.normal(0, SD_SHOCK)
    for t in range(1, P): e[t] = PHI * e[t - 1] + rng.normal(0, SD_SHOCK * np.sqrt(1 - PHI**2))
    return e

def assign_day():                               # random 24/24 split of the 48 periods inside each day
    a = np.zeros(P, int)
    for d in range(14):
        a[d * PER_DAY + rng.permutation(PER_DAY)[:PER_DAY // 2]] = 1
    return a
alt = np.tile([0, 1], P // 2)                    # strict A,B,A,B...

PAR = 1.0 * (slot % 2)                           # a half-hour rhythm: e.g. orders bunch just after the hour/half-hour

def test(assign, effect=0.0):
    y = tod + PAR + shocks() + effect * assign + rng.normal(0, SD_ORDER / np.sqrt(DELIV), P)   # period mean minutes
    diff = y[assign == 1].mean() - y[assign == 0].mean()
    se_naive = SD_ORDER * np.sqrt(2 / (DELIV * P / 2))                      # z-test treating 604,800 orders as independent
    # right unit: the period; remove the slot-of-day mean, then use one difference per day (14 days) and a t-test
    ys = y.reshape(14, PER_DAY); a2 = assign.reshape(14, PER_DAY)
    res = ys - ys.mean(axis=0)
    dday = np.array([res[d][a2[d] == 1].mean() - res[d][a2[d] == 0].mean() for d in range(14)])
    t = dday.mean() / (dday.std(ddof=1) / np.sqrt(14))
    return diff, abs(diff / se_naive) > 1.96, abs(t) > 2.160                # 2.160 = t critical, 13 df

# a) under NO effect: false-positive rate of the naive order-level z-test vs the day-level period test
R = 1500
fp = np.array([test(assign_day())[1:] for _ in range(R)]).mean(axis=0)
print(f"false positives, no effect: order-level z-test {fp[0]:.3f}; day-level period test {fp[1]:.3f}")
assert fp[0] > 0.15 and 0.02 < fp[1] < 0.09
print(f"naive SE {SD_ORDER*np.sqrt(2/(DELIV*P/2)):.4f} min for the arm difference")

# b) strict alternation is aliased with any half-hour rhythm; random assignment is not
d_alt = np.array([test(alt)[0] for _ in range(300)])
d_blk = np.array([test(assign_day())[0] for _ in range(300)])
print(f"no effect, mean estimated difference: alternation {d_alt.mean():+.3f} min; day-random {d_blk.mean():+.3f} min")
assert abs(d_alt.mean()) > 0.8 and abs(d_blk.mean()) < 0.1

# c) carryover: each period keeps a share phi of the previous period's effect
tau, phi = -1.0, 0.5
est = []
for _ in range(600):
    a = assign_day()
    prev = np.r_[0, a[:-1]]
    y = tod + PAR + shocks() + tau * (a + phi * prev) + rng.normal(0, SD_ORDER / np.sqrt(DELIV), P)
    est.append(y[a == 1].mean() - y[a == 0].mean())
print(f"carryover test: true direct effect {tau}, full-rollout effect {tau*(1+phi)}, switchback estimate {np.mean(est):+.2f}")
assert abs(np.mean(est) - tau) < 0.15
