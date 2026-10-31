import math
calls, hit_share, save = 1_000_000, 0.35, 0.012
hits = int(calls * hit_share)
gross = hits * save
print(f"hits {hits:,}; gross savings {gross:,.0f} per month")
assert hits == 350_000 and round(gross) == 4200
k, n = 28, 400
p = k / n
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
lo, hi = wilson(k, n)
print(f"sample wrong rate {p:.1%}, 95% Wilson {lo:.1%} to {hi:.1%}")
print(f"projected wrong cached answers {p*hits:,.0f} (range {lo*hits:,.0f} to {hi*hits:,.0f})")
assert p == 0.07 and round(p * hits) == 24_500 and (round(lo, 3), round(hi, 3)) == (0.049, 0.099)
be = gross / (p * hits)
print(f"break-even cost of one wrong answer = {be:.3f} = {be/save:.1f}x the saving per hit")
assert round(be, 3) == 0.171 and round(be / save, 1) == 14.3
base = 0.04   # invented: error rate the fresh model would have on the same questions
print(f"if fresh answers are wrong {base:.0%} of the time, extra errors from the cache = {(p-base)*hits:,.0f}")
assert round((p - base) * hits) == 10_500
# Toy threshold sweep with invented similarity scores for hits that are right vs wrong.
import numpy as np
rng = np.random.default_rng(11)
right = np.clip(rng.normal(0.96, 0.025, 93_000), 0, 1)
wrong = np.clip(rng.normal(0.935, 0.015, 7_000), 0, 1)
prev = None
for th in (0.92, 0.94, 0.96):
    kr, kw = (right >= th).sum(), (wrong >= th).sum()
    hit, wr = (kr + kw) / 100_000, kw / (kr + kw)
    print(f"toy threshold {th}: hit share {hit:.1%}, wrong share of hits {wr:.1%}")
    if prev: assert hit < prev[0] and wr < prev[1]
    prev = (hit, wr)
