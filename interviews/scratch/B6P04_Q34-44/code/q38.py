# Q38: satisfaction +2 points, p95 latency 1.4 -> 3.1 s, cost 0.002 -> 0.012 dollars. Illustrative, seeded.
import numpy as np

print("cost multiple:", 0.012 / 0.002, " p95 multiple:", round(3.1 / 1.4, 2))
assert round(0.012 / 0.002, 6) == 6.0 and round(3.1 / 1.4, 2) == 2.21

# break-even: extra cost per user-month vs value of +2 satisfaction points (value per point is a made-up input)
q_per_user = 20                      # queries per user per month (invented)
extra_cost = (0.012 - 0.002) * q_per_user
print(f"extra cost per user-month: {extra_cost:.2f} dollars")
assert abs(extra_cost - 0.20) < 1e-9
need_per_point = extra_cost / 2
print(f"the 2 points must be worth at least {need_per_point:.2f} dollars per point per user-month to break even")

# latency: where does a p95 jump come from? a slow path for a minority of queries
rng = np.random.default_rng(38)
n = 200_000
old = rng.lognormal(np.log(0.8), 0.35, n)
slow = rng.random(n) < 0.08                         # 8% of queries go through a slow reasoning path
new = np.where(slow, rng.lognormal(np.log(3.3), 0.25, n), rng.lognormal(np.log(0.9), 0.35, n))
for name, x in (("old", old), ("new", new)):
    print(f"{name}: p50 {np.percentile(x,50):.2f}s  p95 {np.percentile(x,95):.2f}s  mean {x.mean():.2f}s")
assert np.percentile(new, 95) > 2 * np.percentile(old, 95)
assert np.percentile(new, 50) < 1.3 * np.percentile(old, 50)

# routing: send only hard queries to the expensive model
cheap, dear = 0.002, 0.012
for share in (1.0, 0.5, 0.3, 0.2):
    blended = share * dear + (1 - share) * cheap
    print(f"share of queries on the large model {share:.0%}: blended cost {blended:.4f} dollars ({blended/cheap:.1f}x)")
assert abs((0.3 * dear + 0.7 * cheap) - 0.005) < 1e-12
