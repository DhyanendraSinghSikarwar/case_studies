import math
p0, p1, u0, u1, cost = 10.0, 11.0, 5000, 4600, 6.0
dp = p1 / p0 - 1
du = u1 / u0 - 1
e_simple = du / dp
e_arc = ((u1 - u0) / ((u1 + u0) / 2)) / ((p1 - p0) / ((p1 + p0) / 2))
print(f"price {dp:+.1%}, units {du:+.1%}, simple elasticity {e_simple:.2f}, midpoint elasticity {e_arc:.3f}")
assert abs(dp - 0.10) < 1e-12 and abs(du + 0.08) < 1e-12 and abs(e_simple + 0.8) < 1e-12
assert abs(e_arc + 0.875) < 0.001
r0, r1 = p0 * u0, p1 * u1
g0, g1 = (p0 - cost) * u0, (p1 - cost) * u1
print(f"revenue {r0:,.0f} -> {r1:,.0f} ({r1-r0:+,.0f}); gross profit {g0:,.0f} -> {g1:,.0f} ({g1-g0:+,.0f}, {g1/g0-1:+.1%})")
assert (r0, r1, g0, g1) == (50000, 50600, 20000, 23000)
# break-evens: how far can units fall before the rise stops paying?
be_rev = r0 / p1                 # units at which revenue is unchanged
be_gp = g0 / (p1 - cost)         # units at which gross profit is unchanged
print(f"revenue break-even units {be_rev:,.0f} ({be_rev/u0-1:+.1%}); profit break-even units {be_gp:,.0f} ({be_gp/u0-1:+.1%})")
assert abs(be_gp - 4000) < 1e-9 and abs(be_rev / u0 - 1 + 1/11) < 1e-9
# how many stores to see an 8% unit change? (illustrative: 100 units/store/week, sd 25, 80% power, 5% two-sided)
from scipy import stats
mu, sd, eff = 100.0, 25.0, 0.08 * 100.0
n = 2 * ((stats.norm.isf(0.025) + stats.norm.isf(0.2)) * sd / eff) ** 2
print(f"stores per arm to detect -8% units: {math.ceil(n)}")
assert math.ceil(n) == 154
# price test result if the truth were a 20% drop: profit falls
g_bad = (p1 - cost) * u0 * 0.8
print(f"if units had fallen 20% (profit-neutral): gross profit {g_bad:,.0f} vs {g0:,.0f} before")
assert g_bad == 20000.0
