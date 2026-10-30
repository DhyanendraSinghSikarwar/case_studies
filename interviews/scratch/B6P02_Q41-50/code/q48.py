# Q48: permanent holdout sizing and cost. Illustrative numbers.
import numpy as np
from scipy.stats import norm
weekly_decisions = 20_000_000
p = 0.05                      # conversion on the metric we care about
for share in (0.02, 0.005, 0.01):
    n_h = weekly_decisions*share; n_m = weekly_decisions - n_h
    se = np.sqrt(p*(1-p)*(1/n_h + 1/n_m))
    mde = (norm.ppf(0.975)+norm.ppf(0.8))*se
    print(f"holdout {share:.1%}: {int(n_h):,} users/week, detectable gap {mde*100:.3f} pp = {mde/p:.2%} relative (80% power, weekly)")
n_h = weekly_decisions*0.02; n_m = weekly_decisions - n_h
mde_rel = (norm.ppf(0.975)+norm.ppf(0.8))*np.sqrt(p*(1-p)*(1/n_h+1/n_m))/p
assert 0.018 < mde_rel < 0.021
# accumulate 4 weeks: noise falls by sqrt(4)
print(f"4 weeks pooled at 2%: ~{mde_rel/2:.2%} relative")
assert abs(mde_rel/2 - 0.0098) < 0.0005

# cost: the holdout loses (new model - frozen model) benefit on 2% of traffic
annual_benefit = 500.0     # Rs lakh per year: value of the model over the "no model" baseline (Rs 5 crore)
uplift_new_over_frozen = 0.30*annual_benefit  # new model adds 30% over the frozen one after a year of drift
cost_upper = 0.02*annual_benefit
cost_real = 0.02*uplift_new_over_frozen
print(f"upper bound (frozen = no model): Rs {cost_upper:.0f} lakh/yr; realistic (frozen model keeps most value): Rs {cost_real:.0f} lakh/yr")
assert cost_upper == 10.0 and abs(cost_real - 3.0) < 1e-9

# value: a decay of 10% of benefit that goes unseen for a quarter
decay_missed = 0.10*annual_benefit*0.25
print(f"undetected 10% decay for one quarter costs Rs {decay_missed:.1f} lakh; one such quarter costs more than a year of holdout (Rs {cost_upper:.0f} lakh)")
assert abs(decay_missed - 12.5) < 1e-9 and decay_missed > cost_upper

# cheaper design: rotating 0.5% holdout, each user frozen for 4 weeks only, new users each cycle
share = 0.005
n_h = weekly_decisions*share; n_m = weekly_decisions - n_h
mde = (norm.ppf(0.975)+norm.ppf(0.8))*np.sqrt(p*(1-p)*(1/n_h+1/n_m))/p
print(f"0.5% holdout: weekly MDE {mde:.1%} relative; pooled over 16 weeks {mde/4:.1%}")
assert 0.036 < mde < 0.040 and abs(mde/4 - mde/np.sqrt(16)) < 1e-12
print("cost scales with share:", f"{0.005/0.02:.0%} of the 2% holdout cost")
assert abs(0.005/0.02 - 0.25) < 1e-12
