# Q45: three creatives, 2,000 impressions each. Prompt numbers + Thompson-style allocation (seeded).
import math
import numpy as np
n = 2000
clicks = {"A": 40, "B": 50, "C": 46}
rates = {k: v / n for k, v in clicks.items()}
print("rates:", rates)
assert rates == {"A": 0.02, "B": 0.025, "C": 0.023}
se_B = math.sqrt(0.025 * 0.975 / n)
print("SE of B's own rate (points):", round(se_B * 100, 3))
assert round(se_B * 100, 2) == 0.35

# the comparison that matters is the DIFFERENCE, whose SE is larger than B's own SE
def se_diff(p, q): return math.sqrt(p * (1 - p) / n + q * (1 - q) / n)
for other in ("A", "C"):
    d = rates["B"] - rates[other]; s = se_diff(rates["B"], rates[other])
    print(f"B - {other}: diff {d*100:.2f} pts, SE {s*100:.3f} pts, z {d/s:.2f}, 95% CI [{(d-1.96*s)*100:.2f}, {(d+1.96*s)*100:.2f}] pts")
dBA = rates["B"] - rates["A"]; sBA = se_diff(rates["B"], rates["A"])
assert abs(dBA / sBA) < 1.96            # B vs A is not significant at 5% two-sided
assert round(sBA * 100, 2) == 0.47

# Beta(1+clicks, 1+misses) posteriors; probability each creative is the best, and allocation by that probability
rng = np.random.default_rng(5)
draws = np.column_stack([rng.beta(1 + c, 1 + n - c, 200_000) for c in clicks.values()])
best = np.bincount(draws.argmax(1), minlength=3) / len(draws)
print("P(best) A, B, C:", best.round(3))
assert best[1] == best.max() and best[1] < 0.7      # B leads but is far from certain
next_day = 30_000
alloc = (best * next_day).round().astype(int)
print("next-day split of 30,000 impressions:", {k: int(v) for k, v in zip("ABC", alloc)})
assert alloc.sum() in (next_day - 1, next_day, next_day + 1)

# fatigue: invented decay. B's CTR falls 3% (relative) per day of exposure to the same users
days = np.arange(0, 15)
ctr_B = 0.025 * 0.97 ** days
cross = int(np.argmax(ctr_B < 0.020))
print("B with 3%/day fatigue (invented), day 0 / 7 / 14:", ctr_B[[0, 7, 14]].round(4))
print("B drops below A's 2.0% on day", cross)
assert cross == 8 and ctr_B[7] > 0.020
