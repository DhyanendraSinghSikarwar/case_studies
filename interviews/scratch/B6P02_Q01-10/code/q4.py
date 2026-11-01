# Q4 monitoring a fraud model with no labels for 45-60 days (illustrative numbers)
import numpy as np
rng = np.random.default_rng(4)

def psi(ref, cur, bins=10):
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1)); edges[0], edges[-1] = -np.inf, np.inf
    r = np.histogram(ref, edges)[0] / len(ref); c = np.histogram(cur, edges)[0] / len(cur)
    r = np.clip(r, 1e-4, None); c = np.clip(c, 1e-4, None)
    return float(np.sum((c - r) * np.log(c / r)))

# Reference: week-1 scores. Current: same MEAN score, but spread into two clumps.
ref = rng.beta(2, 18, 100_000)                      # mean ~0.10
ref_mean = ref.mean()
cur = np.where(rng.random(100_000) < 0.5, rng.beta(1.5, 40, 100_000), rng.beta(4, 12, 100_000))
cur = cur * (ref_mean / cur.mean())                # force same mean
thr = 0.40
print(f"mean score ref {ref.mean():.3f} vs now {cur.mean():.3f}")
print(f"approval rate (score < {thr}) ref {(ref<thr).mean():.2%} vs now {(cur<thr).mean():.2%}")
p = psi(ref, cur)
print(f"score PSI = {p:.3f}")
assert abs(ref.mean() - cur.mean()) < 0.002          # dashboard mean looks normal
assert abs((ref < thr).mean() - (cur < thr).mean()) < 0.01   # approval rate looks normal
assert p > 0.25                                       # the distribution test still sees it

# Label maturity: chargeback delay uniform 45-60 days after the transaction
delay = rng.integers(45, 61, 200_000)
for age in [14, 30, 45, 50, 60]:
    print(f"fraction of a cohort labelled at age {age:>2} days: {(delay <= age).mean():.2f}")
assert (delay <= 44).sum() == 0 and (delay <= 60).mean() == 1.0
# a week of launch traffic (days 0-6) is fully labelled only after day 6 + 60
print("first fully labelled week of traffic: day", 6 + 60)

# Fast proxy: share of flagged transactions confirmed as fraud by an analyst within 3 days
flagged = 2_000
for confirm_rate, name in [(0.60, "launch week"), (0.45, "week 3")]:
    k = rng.binomial(flagged, confirm_rate)
    se = (confirm_rate * (1 - confirm_rate) / flagged) ** 0.5
    print(f"{name}: confirmed {k}/{flagged} = {k/flagged:.1%} (SE {se*100:.1f} pts)")
assert (0.60 - 0.45) / ((0.6*0.4/2000 + 0.45*0.55/2000) ** 0.5) > 8   # a 15-pt fall is far outside noise
