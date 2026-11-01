# Q43 leading indicator for 90-day retention (illustrative simulation)
import numpy as np
from scipy import stats
rng = np.random.default_rng(43)
# (a) user-level: does early activity predict D90 retention in historical cohorts?
n = 40_000
habit = rng.normal(0, 1, n)
d7_days = np.clip(np.round(3 + 1.5*habit + rng.normal(0, 1, n)), 0, 7)     # active days in first 7
p90 = 1/(1+np.exp(-(-1.0 + 0.9*habit)))
d90 = rng.random(n) < p90
def auc(score, y):
    r = stats.rankdata(score); n1 = y.sum(); n0 = len(y)-n1
    return (r[y].sum() - n1*(n1+1)/2)/(n1*n0)
a = auc(d7_days, d90)
print(f"user-level AUC of 'active days in week 1' for D90 retention: {a:.3f}")
assert 0.62 < a < 0.78

# (b) experiment-level: 12 past launches, early effect on the indicator vs the later 90-day retention effect
k = 12
early = rng.normal(0.02, 0.03, k)                  # lift in share with >=4 active days in week 1 (points)
true90 = 0.25*early + rng.normal(0, 0.004, k)      # real 90-day effect (points)
obs90 = true90 + rng.normal(0, 0.002, k)           # measured with noise
res = stats.linregress(early, obs90)
print(f"across {k} past launches: slope {res.slope:.2f}, R^2 {res.rvalue**2:.2f}")
# prediction interval for a new feature with an early lift of 0.03
x0 = 0.03
resid = obs90 - (res.intercept + res.slope*early)
s = np.sqrt((resid**2).sum()/(k-2))
sxx = ((early-early.mean())**2).sum()
se_pred = s*np.sqrt(1 + 1/k + (x0-early.mean())**2/sxx)
t = stats.t.ppf(0.975, k-2)
pred = res.intercept + res.slope*x0
print(f"predicted D90 lift for early lift 0.03: {pred:.4f}  95% PI [{pred-t*se_pred:.4f}, {pred+t*se_pred:.4f}]")
assert pred - t*se_pred < pred < pred + t*se_pred
print("PI width in points:", round(2*t*se_pred*100, 2))
# (c) the trap: observational user-level link says nothing about causal effect of THIS feature (selection)
# users who adopt the feature are higher-habit; naive adopter vs non-adopter gap overstates
adopt = rng.random(n) < 1/(1+np.exp(-(habit-0.5)))
gap = d90[adopt].mean() - d90[~adopt].mean()
print(f"naive adopter vs non-adopter D90 gap {gap:.3f} with zero true feature effect in this simulation")
assert gap > 0.10
