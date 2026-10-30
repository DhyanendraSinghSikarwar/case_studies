# Q26: ride-hailing discount, shared driver supply (illustrative toy model, seeded)
import numpy as np

rng = np.random.default_rng(26)
print("prompt arithmetic: rides", round(5.5 / 5.0 - 1, 3), " wait", round(4.4 / 4.0 - 1, 3))
assert abs(5.5 / 5.0 - 1 - 0.10) < 1e-9 and abs(4.4 / 4.0 - 1 - 0.10) < 1e-9

CAP_PER_RIDER = 5.25     # driver supply: rides per rider-week the whole city can serve (assumption)
BASE, DISC = 5.0, 5.5    # weekly ride requests per rider without / with the discount

def week(n, treated_share, cap_per_rider):
    """n riders in one market; requests ~ Poisson; supply is shared and rationed at random."""
    treated = rng.random(n) < treated_share
    req = rng.poisson(np.where(treated, DISC, BASE))
    cap = int(cap_per_rider * n)
    total = req.sum()
    keep = min(1.0, cap / total)                     # each request is served with the same probability
    served = rng.binomial(req, keep)
    return treated, served

# 1) user-level A/B in one market, 50/50 treated: supply covers total demand (5.25 per rider on average)
t, s = week(400_000, 0.5, CAP_PER_RIDER)
ab = s[t].mean() / s[~t].mean() - 1
print(f"user-level A/B lift: treated {s[t].mean():.2f} vs control {s[~t].mean():.2f} rides -> {ab*100:.1f}%")
assert abs(ab - 0.10) < 0.02

# 2) full rollout: everybody treated, same supply
t, s = week(400_000, 1.0, CAP_PER_RIDER)
roll = s.mean() / BASE - 1
print(f"full rollout: {s.mean():.2f} rides per rider vs 5.00 without discount -> {roll*100:.1f}% (supply caps it)")
assert 0.03 < roll < 0.07

# 3) market-level design: 20 markets, 10 get the discount for everyone, 10 do not; supply scales with market size
res = []
for m in range(20):
    treated_market = m % 2 == 0
    t, s = week(40_000, 1.0 if treated_market else 0.0, CAP_PER_RIDER)
    res.append((treated_market, s.mean()))
tm = np.mean([r for k, r in res if k]); cm = np.mean([r for k, r in res if not k])
print(f"market-level readout: treated markets {tm:.2f} vs control markets {cm:.2f} -> {(tm/cm-1)*100:.1f}%")
assert abs((tm / cm - 1) - roll) < 0.02
print("so the user-level A/B overstates the rollout effect by about", round(ab / roll, 1), "x in this toy")
