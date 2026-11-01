# Q46: redirect test, differential logging, zero true effect (illustrative simulation)
import numpy as np
from scipy import stats
rng = np.random.default_rng(46)
n = 100_000
chi = (93_000-96_500)**2/96_500 + (100_000-96_500)**2/96_500
print("chi-square logged treatment vs control (expected 96,500 each):", round(chi, 1), "p =", stats.chi2.sf(chi, 1))
assert 253 < chi < 255
# users have a speed type; slow users convert less and are the ones whose redirect fails
slow = rng.random(2*n) < 0.14
arm = np.r_[np.zeros(n, bool), np.ones(n, bool)]       # False control, True treatment
conv = rng.random(2*n) < np.where(slow, 0.02, 0.10)    # NO treatment effect at all
lost = arm & slow & (rng.random(2*n) < 0.5)            # half of slow treatment users never log the arrival
logged = ~lost
print("logged control", int((logged & ~arm).sum()), "logged treatment", int((logged & arm).sum()))
assert 91_500 < (logged & arm).sum() < 94_500
naive = conv[logged & arm].mean() - conv[~arm].mean()
itt = conv[arm].mean() - conv[~arm].mean()
print("naive (logged only) lift:", round(naive*100, 3), "points   ITT (everyone assigned):", round(itt*100, 3), "points")
assert naive > 0.003 and abs(itt) < 0.003
# Lee bounds: trim the control group by the lost share (monotone loss assumed)
q = ((~arm).sum() - (logged & arm).sum()) / (~arm).sum()      # share to trim
c = np.sort(conv[~arm].astype(float))
k = int(round(q * len(c)))
tmean = conv[logged & arm].mean()
upper = tmean - c[: len(c) - k].mean()    # drop the highest control outcomes: control mean falls, effect rises
lower = tmean - c[k:].mean()              # drop the lowest control outcomes: control mean rises, effect falls
print("trim share", round(q, 3), "Lee bounds on effect among always-logged:", round(lower*100, 3), "to", round(upper*100, 3), "points")
assert abs(lower) < 0.003 and upper > 0.05      # lower bound is near the true zero (up to noise); upper bound is very wide
# ITT needs treatment arrival to be measured by ASSIGNMENT: join conversion to the assignment log, not to the landing-page log
