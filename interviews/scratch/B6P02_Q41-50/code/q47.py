# Q47: novelty effect, cannibalisation, long-term holdout. Illustrative numbers.
import numpy as np
from scipy.stats import norm
base = 0.040   # control conversion
lift_rel = {1: 0.030, 2: 0.020, 3: 0.010, 4: 0.002}   # observed relative lift by week
for w, l in lift_rel.items():
    print(f"week {w}: relative lift {l:.1%}  (conversion {base*(1+l):.4f} vs {base:.4f})")
assert abs(base*(1+lift_rel[1]) - 0.0412) < 1e-12

# exponential-decay fit: ratio between weeks
r = np.exp(np.diff(np.log([lift_rel[w] for w in (1, 2, 3)]))).mean()
print(f"week-over-week lift ratio (weeks 1-3) ~ {r:.2f}; week 4 predicted {0.03*r**3:.4f}")

def n_per_arm(p, rel, alpha=0.05, power=0.8):
    d = p*rel
    return int(np.ceil(2*(norm.ppf(1-alpha/2)+norm.ppf(power))**2*p*(1-p)/d**2))
n_3 = n_per_arm(base, 0.03)
n_1 = n_per_arm(base, 0.01)
print(f"users per arm to detect 3% relative lift: {n_3:,}; 1% relative lift: {n_1:,}")
assert 400_000 < n_3 < 430_000 and 3_700_000 < n_1 < 4_000_000

# holdout sizing: 10M users, 5% held out on old model gives 500k vs 9.5M
n_h, n_t = 500_000, 9_500_000
se = np.sqrt(base*(1-base)*(1/n_h + 1/n_t))
mde_rel = (norm.ppf(0.975)+norm.ppf(0.8))*se/base
print(f"5% holdout of 10M users: detectable relative lift ~ {mde_rel:.2%} (80% power)")
assert 0.018 < mde_rel < 0.021

# cannibalised demand: 1,000 units of stock a day, shared by both buckets
# treatment shows items that are in demand; it wins sales from control during the test
buyers_control_alone = 0.040*50_000        # if both buckets got the old model (50k users each)
supply = 4_000                              # units (limited)
# during the A/B test treatment takes 3% more of the same pool: control loses what treatment wins
treat_sales = buyers_control_alone*1.03
ctrl_sales = supply - treat_sales
ab_lift = treat_sales/ctrl_sales - 1
print(f"limited pool: A/B reads {ab_lift:.1%} lift; full rollout total sales stay {supply}")
assert abs(ab_lift - (2060/1940 - 1)) < 1e-9 and ab_lift > 0.06
assert treat_sales + ctrl_sales == supply
print(f"true company-wide lift from the pool: 0%, yet the test reads {ab_lift:.1%}: interference")
