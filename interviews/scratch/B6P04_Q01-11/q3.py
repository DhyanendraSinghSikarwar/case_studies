import numpy as np
from scipy import stats
rng = np.random.default_rng(7)

ctr_c = 0.050
ctr_t = [0.056, 0.053, 0.051]
rel = [(t / ctr_c - 1) * 100 for t in ctr_t]
print("relative lift by week (%):", [round(r, 1) for r in rel])
assert [round(r) for r in rel] == [12, 6, 2]

# Is week 3 still distinguishable from zero? Illustrative: 100,000 users per arm per week
n = 100_000
for wk, t in enumerate(ctr_t, 1):
    pool = (t + ctr_c) / 2
    se = np.sqrt(2 * pool * (1 - pool) / n)
    d = t - ctr_c
    print(f"week {wk}: diff {d*100:.1f} pts, 95% CI {100*(d-1.96*se):.2f} to {100*(d+1.96*se):.2f}")
se3 = np.sqrt(2 * 0.0505 * 0.9495 / n)
assert (0.001 - 1.96 * se3) < 0 < (0.001 + 1.96 * se3)   # week 3 CI includes 0

# Decay shape: the gap roughly halves each week (0.6, 0.3, 0.1 points). Fit log-linear decay.
gap = np.array([0.6, 0.3, 0.1])
slope = np.polyfit([1, 2, 3], np.log(gap), 1)[0]
print(f"fitted weekly decay factor = {np.exp(slope):.2f}")
asymptote_note = "extrapolated gap in week 6 (if pure exponential decay): %.2f pts" % (0.6 * np.exp(slope) ** 5)
print(asymptote_note)

# What to quote: the week-3 estimate with its interval, not week 1
d3 = 0.001
lo, hi = d3 - 1.96 * se3, d3 + 1.96 * se3
print(f"quote: about +{d3*100:.1f} pts (+{d3/ctr_c*100:.0f}% relative), 95% CI {lo*100:.2f} to {hi*100:.2f} pts, still fading")
assert round(d3 / ctr_c * 100) == 2
