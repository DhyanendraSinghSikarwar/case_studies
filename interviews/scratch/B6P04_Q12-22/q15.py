# Q15: statistically significant is not the same as worth shipping (illustrative numbers)
import numpy as np
from scipy.stats import norm

lift, lo, hi = 0.004, 0.001, 0.007          # relative lift on revenue per user and its 95% CI
se = (hi - lo) / (2 * 1.96)
z = lift / se
p = 2 * norm.sf(z)
print(f"implied SE = {se:.4%} relative, z = {z:.2f}, p = {p:.4f}")
assert abs(se - 0.0015306) < 1e-6 and 0.005 < p < 0.01          # significant, as the PM says

# Business case (all inventive units): 10M users, 100 units revenue per user per month
users, rev_pm = 10_000_000, 100.0
annual_rev = users * rev_pm * 12
cost_per_year = 40_000_000                  # build + upkeep, in the same units; finance supplies the real figure
breakeven = cost_per_year / annual_rev
print(f"annual revenue {annual_rev:,.0f}; cost {cost_per_year:,.0f}/yr; break-even lift = {breakeven:.3%}")
assert abs(breakeven - 4e7 / 1.2e10) < 1e-12

for name, l in (("low", lo), ("point", lift), ("high", hi)):
    print(f"{name:5}: lift {l:.2%} -> gain {l * annual_rev:,.0f} units/yr, net {l * annual_rev - cost_per_year:,.0f}")
assert lo * annual_rev - cost_per_year < 0 < lift * annual_rev - cost_per_year

# rough probability the true lift clears break-even (normal approximation around the estimate, flat prior)
p_clear = norm.sf((breakeven - lift) / se)
print(f"P(true lift > break-even) ~ {p_clear:.0%}")
assert 0.6 < p_clear < 0.7

# shrinkage for the winner's curse: if most ideas have lift ~ 0 +- 0.3%, the posterior mean is lower
prior_sd = 0.003
post_mean = lift * prior_sd**2 / (prior_sd**2 + se**2)
print(f"posterior mean with a N(0, 0.3%) prior = {post_mean:.3%}")
assert post_mean < lift

# how much longer would we need to cut the interval width in half? 4x the users
print("users needed for half-width CI: 4x ->", 4 * 2_000_000, "per arm")
assert abs(se / 2 - np.sqrt(se**2 / 4)) < 1e-12
print("all asserts passed")
