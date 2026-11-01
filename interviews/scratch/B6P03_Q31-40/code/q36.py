import math
import numpy as np
from scipy.stats import beta, binom, fisher_exact

def cp(k, n, a=0.05):
    return (beta.ppf(a / 2, k, n - k + 1) if k > 0 else 0.0, beta.ppf(1 - a / 2, k + 1, n - k) if k < n else 1.0)
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

# 1) how uncertain is 14 of 20 and 12 of 20?
for name, k in [("new", 14), ("old", 12)]:
    lo, hi = cp(k, 20); wl, wh = wilson(k, 20)
    print(f"{name}: recall {k/20:.2f}  exact 95% CI {lo:.3f}-{hi:.3f}   Wilson {wl:.3f}-{wh:.3f}")
assert round(cp(14, 20)[0], 2) == 0.46 and round(cp(14, 20)[1], 2) == 0.88

# 2) same 20 positives for both models -> paired comparison; only discordant positives matter
# best case for the new model: it catches the 12 the old one caught plus 2 more -> b=2, c=0
b, c = 2, 0
p_exact = 2 * binom.cdf(min(b, c), b + c, 0.5)          # two-sided exact McNemar (sign test)
print("best case b=2,c=0: two-sided exact McNemar p =", p_exact)
assert p_exact == 0.5
# a more typical split: new catches 14, old 12, overlap 10 -> new-only 4, old-only 2
b, c = 4, 2
p2 = min(1.0, 2 * binom.cdf(min(b, c), b + c, 0.5))
print("overlap 10: new-only 4, old-only 2: p =", round(float(p2), 3))
# unpaired Fisher (wrong test for same rows) is also nowhere near significant
print("unpaired Fisher on 14/20 vs 12/20: p =", round(float(fisher_exact([[14, 6], [12, 8]])[1]), 3))

# 3) how many positives would you need? half-width 0.05 around recall 0.7
n_pos = math.ceil(1.96 ** 2 * 0.7 * 0.3 / 0.05 ** 2)
base = 20 / 20_000
print("positives for +-5 points on recall 0.7:", n_pos, " rows needed at the current 0.1% rate:", round(n_pos / base))
assert n_pos == 323 and round(n_pos / base) == 323_000
# detecting 0.70 vs 0.60 paired, with discordance ~25%: rough n via normal approx on b-c
# simulate: how often does a truly WORSE (0.60) model look at least as good as a 0.70 one on 20 positives?
rng = np.random.default_rng(36)
a = rng.random((200_000, 20)) < 0.70
b_ = rng.random((200_000, 20)) < 0.60
look = (a.sum(1) <= b_.sum(1)).mean()
print("P(truly worse model catches >= as many of 20) :", round(float(look), 3))
assert 0.25 < look < 0.45
# 4) fix the test set: enrich positives (stratified sampling) and reweight negatives
neg_keep = 0.05                                           # keep 5% of negatives
pos_total, neg_total = 20, 19_980
neg_rows = round(neg_total * neg_keep)
print("enriched set: rows", pos_total + neg_rows, " positive share", round(pos_total / (pos_total + neg_rows), 3), " weight on each negative", 1 / neg_keep)
# but recall CI width does not shrink: it depends on positives, not on negatives
assert cp(14, 20)[1] - cp(14, 20)[0] > 0.35
# 5) a larger positive pool: 200 positives, same 70% vs 60% -> now separable?
print("200 positives: 140 vs 120 caught, exact CIs", [tuple(round(float(x), 3) for x in cp(k, 200)) for k in (140, 120)])
