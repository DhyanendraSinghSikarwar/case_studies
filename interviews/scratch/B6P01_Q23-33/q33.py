# Q33 onboarding flow: day-1 up 4 pts, day-30 unchanged (illustrative numbers)
import math
n = 20_000                                       # users per arm
days = [1, 3, 7, 14, 30]
control = [0.40, 0.28, 0.20, 0.15, 0.12]
treat = [0.44, 0.30, 0.21, 0.155, 0.12]

def ci_diff(p1, p0, n):
    d = p1 - p0
    se = math.sqrt(p1 * (1 - p1) / n + p0 * (1 - p0) / n)
    return d, d - 1.96 * se, d + 1.96 * se

print("day  control treat  diff(pts)  95% CI (pts)")
rows = {}
for dday, c, t in zip(days, control, treat):
    d, lo, hi = ci_diff(t, c, n)
    rows[dday] = (d, lo, hi)
    print(f"{dday:>3}  {c:.3f}   {t:.3f}  {d*100:6.2f}    [{lo*100:5.2f}, {hi*100:5.2f}]")
d1, lo1, hi1 = rows[1]
d30, lo30, hi30 = rows[30]
assert round(d1 * 100, 2) == 4.0 and lo1 > 0
assert d30 == 0 and lo30 < 0 < hi30
print("day-30 half-width (pts):", round((hi30 - d30) * 100, 2))
assert round((hi30 - d30) * 100, 2) == 0.64
# diffs shrink with time -> consistent with a transient effect
diffs = [rows[d][0] for d in days]
assert all(a >= b for a, b in zip(diffs, diffs[1:]))
# users per arm needed to detect a 1-point day-30 gain (80% power, alpha 0.05, p=0.12)
z_a, z_b = 1.96, 0.8416
p0, p1 = 0.12, 0.13
n_need = ((z_a + z_b) ** 2 * (p0 * (1 - p0) + p1 * (1 - p1))) / (p1 - p0) ** 2
print("users per arm to detect +1 pt at day 30:", math.ceil(n_need))
assert math.ceil(n_need) == 17_166
