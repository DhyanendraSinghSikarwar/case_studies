# Q29 sepsis external validation sample size and alert burden (illustrative numbers)
from math import sqrt
from scipy import stats
events_needed = 100
rate = {"hospital 2": 0.025, "hospital 3": 0.04}
for h, p in rate.items():
    n_exp = events_needed / p
    n = int(n_exp)
    while stats.binom.sf(events_needed - 1, n, p) < 0.95:
        n += 1
    print(f"{h}: rate {p:.1%}, patients for 100 expected events {n_exp:,.0f}; for a 95% chance of at least 100 events {n:,}")
assert 100 / 0.025 == 4_000 and 100 / 0.04 == 2_500
assert stats.binom.sf(99, 2_500, 0.04) < 0.55     # only about even odds at the expected count
print(f"P(>=100 events) with 2,500 patients at 4% = {stats.binom.sf(99, 2500, 0.04):.2f}")

# What do 100 events buy? 95% half-width of a sensitivity of 0.70 and of an AUC of 0.79 (Hanley-McNeil)
hw_sens = 1.96 * sqrt(0.7 * 0.3 / 100)
def auc_se(auc, npos, nneg):
    q1, q2 = auc / (2 - auc), 2 * auc**2 / (1 + auc)
    return sqrt((auc*(1-auc) + (npos-1)*(q1-auc**2) + (nneg-1)*(q2-auc**2)) / (npos*nneg))
se = auc_se(0.79, 100, 3_900)
print(f"sensitivity 0.70 on 100 events: +-{hw_sens:.3f}; AUC 0.79 with 100 events: +-{1.96*se:.3f}")
assert 0.08 < hw_sens < 0.10 and 0.04 < 1.96 * se < 0.07

# Alert burden at hospital 2 for an invented operating point (sens 0.60, spec 0.85)
sens, spec, p = 0.60, 0.85, 0.025
tp, fp = sens * p, (1 - spec) * (1 - p)
ppv = tp / (tp + fp)
alerts_per_1000 = 1000 * (tp + fp)
assert abs(ppv - 0.0930) < 1e-3 and round(alerts_per_1000) == 161
print(f"hospital 2 at sens 0.60 / spec 0.85: PPV {ppv:.1%}, alerts per 1,000 patients {alerts_per_1000:.0f}, true cases found {1000*tp:.0f} of {1000*p:.0f}")
# Calibration slope 0.6: predictions are too extreme; pull them toward the mean on the logit scale
import numpy as np
logit = lambda x: np.log(x / (1 - x)); expit = lambda z: 1 / (1 + np.exp(-z))
pred, mean_risk = 0.20, 0.025          # assume the average predicted risk equals the 2.5% event rate
adj = expit(logit(mean_risk) + 0.6 * (logit(pred) - logit(mean_risk)))
print(f"slope 0.6 pivoting at the mean: a predicted 20% risk is recalibrated to about {adj:.1%}")
assert 0.085 < adj < 0.095
