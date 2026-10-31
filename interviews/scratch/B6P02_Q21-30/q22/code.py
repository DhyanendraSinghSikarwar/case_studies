import numpy as np
from scipy import stats

# Thumbs-up: illustrative 3,000 votes per week
n = 3000
up0, up1 = round(0.78 * n), round(0.69 * n)
assert (up0, up1) == (2340, 2070)
p0, p1 = up0 / n, up1 / n
pool = (up0 + up1) / (2 * n)
z = (p0 - p1) / np.sqrt(pool * (1 - pool) * 2 / n)
print(f"thumbs-up {p0:.0%} -> {p1:.0%}, z={z:.1f}")
assert z > 6          # not noise, but says nothing about cause

# Fixed regression set: 300 questions, same questions, same prompts, pinned old vs new provider run
total = 300
pass_before = 255       # 85%
pass_after = 231        # 77%
b_lost, c_gained = 38, 14       # discordant pairs: pass->fail, fail->pass
assert pass_before - b_lost + c_gained == pass_after
assert pass_before / total == 0.85 and pass_after / total == 0.77
res = stats.binomtest(b_lost, b_lost + c_gained, 0.5)       # exact McNemar
print(f"fixed set {pass_before/total:.0%} -> {pass_after/total:.0%}; lost {b_lost}, gained {c_gained}; exact McNemar p={res.pvalue:.4f}")
assert res.pvalue < 0.01
# 95% interval for the paired difference in pass rate (normal approx on paired differences)
d = (c_gained - b_lost) / total
se = np.sqrt((b_lost + c_gained) - (b_lost - c_gained) ** 2 / total) / total
print(f"difference {d*100:+.1f} points, 95% CI [{(d-1.96*se)*100:+.1f}, {(d+1.96*se)*100:+.1f}]")
assert d + 1.96 * se < 0

# Smallest drop a daily 300-question canary can see (pass rate .85, unpaired, 80% power, alpha .05)
sd = np.sqrt(2 * 0.85 * 0.15 / 300)
mde = (1.96 + 0.84) * sd
print(f"unpaired canary of 300: minimum detectable drop about {mde*100:.1f} points")
assert 0.07 < mde < 0.09
