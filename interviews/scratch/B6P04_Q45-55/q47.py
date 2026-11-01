# Q47: Bayesian "probability treatment is best" under daily peeking (illustrative simulation)
import numpy as np
from scipy import stats
rng = np.random.default_rng(47)
DAYS, PER_DAY, P0 = 14, 5_000, 0.05          # users per arm per day, baseline conversion
def look_probs(true_lift, sims=4000):
    pc = np.full(sims, P0); pt = pc * (1 + true_lift)
    cc = rng.binomial(PER_DAY, pc[:, None], (sims, DAYS)).cumsum(1)
    ct = rng.binomial(PER_DAY, pt[:, None], (sims, DAYS)).cumsum(1)
    n = PER_DAY * np.arange(1, DAYS + 1)
    # Beta(1,1) posteriors, normal approximation to P(p_t > p_c)
    mc, mt = (cc + 1) / (n + 2), (ct + 1) / (n + 2)
    vc, vt = mc * (1 - mc) / (n + 3), mt * (1 - mt) / (n + 3)
    return stats.norm.cdf((mt - mc) / np.sqrt(vc + vt))
# check the approximation against exact beta draws on one case
c, t, n = 250, 300, 5000
d = rng.beta(t + 1, n - t + 1, 400_000) > rng.beta(c + 1, n - c + 1, 400_000)
mc, mt = (c+1)/(n+2), (t+1)/(n+2)
approx = stats.norm.cdf((mt-mc)/np.sqrt(mc*(1-mc)/(n+3)+mt*(1-mt)/(n+3)))
print("exact vs normal-approx P(best):", round(float(d.mean()), 4), round(float(approx), 4)); assert abs(d.mean()-approx) < 0.005
null = look_probs(0.0)
ever96 = (null >= 0.96).any(1).mean()
day5 = (null[:, 4] >= 0.96).mean()
last = (null[:, -1] >= 0.96).mean()
print("A/A tests: P(best)>=96% on day 5:", round(day5, 3), "| at the planned end (day 14):", round(last, 3), "| at ANY daily look:", round(ever96, 3))
assert ever96 > 2 * last and ever96 > 0.09
# the same rule with a real +4% relative lift
alt = look_probs(0.04)
print("true +4% lift: stop-at-96% on some day 1-13 and call it a win:", round((alt[:, :13] >= .96).any(1).mean(), 3), "| win at day 14:", round((alt[:, -1] >= .96).mean(), 3))
# stopping rule that waits for whole weeks, needs P(best) high AND expected loss small
n5 = PER_DAY * 5
print("day-5 sample per arm:", n5, " day-14:", PER_DAY * 14)
safer = ((null[:, 6] >= 0.99) | (null[:, 13] >= 0.99)).mean()
print("A/A tests that cross 99% at day 7 or day 14 only:", round(safer, 3))
assert safer < ever96
