import numpy as np
from math import sqrt, log

N, EAD, LGD = 20000, 10000, 0.5
pd_pred, defaults = 0.03, 900
pd_obs = defaults / N
el_pred = N * pd_pred * EAD * LGD
el_obs = defaults * EAD * LGD
print("observed default rate", pd_obs, "| predicted defaults", N * pd_pred, "| observed", defaults)
print("expected loss predicted", el_pred, "observed", el_obs, "shortfall", el_obs - el_pred, "=", round((el_obs - el_pred) / el_obs, 3), "of observed;", round(el_obs / el_pred, 2), "x predicted")
assert pd_obs == 0.045 and N * pd_pred == 600
assert el_pred == 3_000_000 and el_obs == 4_500_000 and el_obs - el_pred == 1_500_000

# noise check, independent defaults: sd of count under the model's own 3%
sd = sqrt(N * pd_pred * (1 - pd_pred))
z = (defaults - N * pd_pred) / sd
print("binomial sd of default count", round(sd, 1), "| z =", round(z, 1))
assert round(sd, 1) == 24.1 and round(z, 1) == 12.4
# defaults cluster (shared shocks): allow a design effect, e.g. intra-class correlation rho
for rho in (0.001, 0.005, 0.01):
    print("  pairwise default correlation rho", rho, "-> design-effect z", round(z / sqrt(1 + (N - 1) * rho), 1))
# intercept shift needed (logit scale) for the average to move from 3.0% to 4.5%
logit = lambda p: log(p / (1 - p))
shift = logit(0.045) - logit(0.03)
print("logit intercept shift", round(shift, 3))
assert round(shift, 3) == 0.421

# simulate: a model with AUC ~0.80 whose level is wrong; recalibrate the intercept; AUC does not move
rng = np.random.default_rng(34)
def auc(s, y):
    r = s.argsort().argsort() + 1
    n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
# latent score so that the model's mean PD is ~3% and AUC ~0.8
z0 = rng.normal(size=N)
def level(b):                      # find intercept so mean prob = b
    lo, hi = -12, 2
    for _ in range(60):
        mid = (lo + hi) / 2
        if (1 / (1 + np.exp(-(mid + 1.3 * z0)))).mean() > b: hi = mid
        else: lo = mid
    return mid
a_true = level(0.045); a_model = level(0.03)
p_true = 1 / (1 + np.exp(-(a_true + 1.3 * z0)))
y = (rng.random(N) < p_true).astype(int)
p_model = 1 / (1 + np.exp(-(a_model + 1.3 * z0)))
print("sim: defaults", y.sum(), "| model mean PD", round(p_model.mean(), 4), "| AUC", round(auc(p_model, y), 3))
# recalibrate on the matured outcomes: fit new intercept only (slope fixed)
a_new = level(y.mean())
p_new = 1 / (1 + np.exp(-(a_new + 1.3 * z0)))
print("after intercept recalibration: mean PD", round(p_new.mean(), 4), "| AUC", round(auc(p_new, y), 3), "| expected loss", round(p_new.sum() * EAD * LGD))
assert abs(auc(p_model, y) - auc(p_new, y)) < 1e-12
assert abs(p_new.mean() - y.mean()) < 1e-4
# calibration by band: is it a uniform shift or only some bands? (decile table)
dec = np.array_split(np.argsort(p_model), 10)
for i in (0, 4, 9):
    d = dec[i]; print(f"  decile {i+1}: predicted {p_model[d].mean():.4f} observed {y[d].mean():.4f} ratio {y[d].mean()/p_model[d].mean():.2f}")
# LGD sensitivity: the 50% is an assumption
for lgd in (0.4, 0.5, 0.6):
    print("  LGD", lgd, "-> observed-default loss", defaults * EAD * lgd, "| predicted", N * pd_pred * EAD * lgd)
assert y.sum() == 890 and round(auc(p_model, y), 3) == 0.804 and round(p_new.mean(), 4) == 0.0445
assert 2 < y[dec[0]].mean() / p_model[dec[0]].mean() < 3 and 1.2 < y[dec[9]].mean() / p_model[dec[9]].mean() < 1.5
