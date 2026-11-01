import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

# Arithmetic from the question
apps, approved, defaults_appr = 100_000, 30_000, 1_200
rejected = apps - approved
rate_appr = defaults_appr / approved
assert rejected == 70_000 and abs(rate_appr - 0.04) < 1e-12
rate_rej = 3 * rate_appr
defaults_rej = rejected * rate_rej
pop_rate = (defaults_appr + defaults_rej) / apps
assert abs(rate_rej - 0.12) < 1e-12 and round(defaults_rej) == 8_400
assert abs(pop_rate - 0.096) < 1e-12
print("reject default (scenario):", rate_rej, "population default (scenario):", pop_rate)
# Sensitivity: the 9.6% depends on the ratio, which nobody has measured
for k in (1, 2, 3, 5):
    print("ratio", k, "-> population default", round((defaults_appr + rejected * k * rate_appr) / apps, 4))
assert round((defaults_appr + rejected * 1 * rate_appr) / apps, 4) == 0.04

# Simulation: a model fitted on approved only, then used on everyone
rng = np.random.default_rng(13)
n = 100_000
x = rng.normal(0, 1, n)                                   # risk driver; higher is riskier
true_logit = -3.2 + 0.9 * x + 0.35 * np.maximum(x, 0) ** 2   # risk accelerates in the tail
y = rng.random(n) < expit(true_logit)
approve = x < np.quantile(x, 0.30)                        # old policy approves the lowest-risk 30%
Xa = np.c_[np.ones(approve.sum()), x[approve]]
ya = y[approve].astype(float)

def nll(b):
    z = Xa @ b
    return np.sum(np.logaddexp(0, z) - ya * z)
b = minimize(nll, np.zeros(2), method="BFGS").x
pred_rej = expit(b[0] + b[1] * x[~approve])
actual_rej = y[~approve].mean()
print("approved actual default:", round(float(y[approve].mean()), 4))
print("rejects: model predicts", round(float(pred_rej.mean()), 4), "actual", round(float(actual_rej), 4))
assert pred_rej.mean() < actual_rej * 0.8                 # extrapolating a linear fit into the tail underpredicts

# Low-risk experiment: approve a small random slice of rejects near the cutoff, small limits
near = np.where(~approve)[0]
near = near[np.argsort(x[near])][:7_000]                    # the 7,000 rejects closest to the cutoff (10% of rejects)
pick = rng.choice(near, 500, replace=False)
exposure = 500 * 1_000                                       # 500 people x limit 1,000 (illustrative)
obs = y[pick].mean()
se = np.sqrt(obs * (1 - obs) / 500)
print("experiment: n=500, exposure upper bound", exposure, "observed default", round(float(obs), 3), "+/-", round(float(1.96 * se), 3))
assert exposure == 500_000
assert 1.96 * se < 0.04
