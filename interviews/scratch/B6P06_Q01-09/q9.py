import math
from scipy import stats
n, p0, d = 400, 0.05, 0.005
se = math.sqrt(2*p0*(1-p0)/n)
print(f"SE of difference {se*100:.2f} pp; effect/SE = {d/se:.2f}")
assert abs(se - 0.0154) < 1e-4 and round(d/se, 2) == 0.32
z = stats.norm.isf(0.025)
power = stats.norm.sf(z - d/se) + stats.norm.cdf(-z - d/se)
print(f"power per week at n=400 per arm: {power:.1%}")
assert 0.05 < power < 0.07
# sample size for 80% power, 5.0% vs 5.5%
p1 = p0 + d
var = p0*(1-p0) + p1*(1-p1)
need = (z + stats.norm.isf(0.2))**2 * var / d**2
weeks = need / n
print(f"per arm needed: {math.ceil(need):,}; weeks at 400 per arm per week: {weeks:.0f}")
assert math.ceil(need) == 31_231 and round(weeks) == 78
# smallest detectable effect (80% power) at 4 weeks and 12 weeks
for w in (1, 4, 12):
    s = math.sqrt(2*p0*(1-p0)/(n*w))
    print(f"{w} weeks: MDE {(z + stats.norm.isf(0.2))*s*100:.1f} pp")
assert round((z + stats.norm.isf(0.2))*math.sqrt(2*p0*(1-p0)/n)*100, 1) == 4.3
