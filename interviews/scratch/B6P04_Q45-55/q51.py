# Q51: what a 0.5 correlation between 7-day and 90-day lifts across 60 experiments allows (illustrative)
import numpy as np
from scipy import stats
rng = np.random.default_rng(51)
r, n = 0.5, 60
z = np.arctanh(r); se = 1/np.sqrt(n-3)
lo, hi = np.tanh(z-1.96*se), np.tanh(z+1.96*se)
print("r =", r, " 95% CI via Fisher z:", round(lo, 2), "to", round(hi, 2), " R^2 =", r**2)
assert 0.27 < lo < 0.29 and 0.66 < hi < 0.68
print("p-value of r=0.5, n=60:", stats.t.sf(r*np.sqrt((n-2)/(1-r**2)), n-2)*2)
agree = 1 - np.arccos(r)/np.pi
print("P(7-day and 90-day lifts have the same sign), bivariate normal:", round(agree, 3))
assert abs(agree - 2/3) < 1e-9
# a 7-day lift one standard deviation above average
s1 = 1.0
pred_mean = r*s1; resid_sd = np.sqrt(1 - r**2)
p_pos = stats.norm.cdf(pred_mean/resid_sd)
print("given a 7-day lift of +1 sd: predicted 90-day lift", pred_mean, "sd, residual sd", round(resid_sd, 3), "-> P(90-day lift > 0) =", round(p_pos, 3))
assert 0.71 < p_pos < 0.73
# measurement noise: observed r is lower than the true r between the real effects
true_r, k = 0.7, 4000
t7, t90 = rng.multivariate_normal([0, 0], [[1, true_r], [true_r, 1]], k).T
o7 = t7 + rng.normal(0, 0.8, k); o90 = t90 + rng.normal(0, 0.8, k)   # each experiment's lift is measured with noise
print("true r between real effects", true_r, "-> observed r between measured lifts", round(np.corrcoef(o7, o90)[0, 1], 3))
assert np.corrcoef(o7, o90)[0, 1] < 0.5
# spread of observed r with 60 experiments (what luck alone does)
rs = []
for _ in range(2000):
    x, y = rng.multivariate_normal([0, 0], [[1, .5], [.5, 1]], 60).T; rs.append(np.corrcoef(x, y)[0, 1])
print("same true r=0.5, rerun with 60 new experiments: observed r in", np.round(np.percentile(rs, [5, 95]), 2), "(5th-95th pct)")
# leave-one-out prediction error of the surrogate on 60 experiments
x, y = rng.multivariate_normal([0, 0], [[1, .5], [.5, 1]], 60).T
pred = np.array([np.polyval(np.polyfit(np.delete(x, i), np.delete(y, i), 1), x[i]) for i in range(60)])
print("leave-one-out R^2 (honest out-of-sample):", round(1 - ((y-pred)**2).sum()/((y-y.mean())**2).sum(), 3))
