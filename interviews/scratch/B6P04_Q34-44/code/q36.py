# Q36: LLM support assistant, 60% -> 63% resolved. Nondeterminism, unit, clustering. Illustrative, seeded.
import numpy as np
from scipy import stats

p0, p1 = 0.60, 0.63
print(f"absolute {100*(p1-p0):.0f} points, relative {(p1/p0-1):.0%}")
assert round(p1 - p0, 2) == 0.03 and round(p1 / p0 - 1, 2) == 0.05

# sample size per arm if every conversation were independent (two-sided 5%, 80% power)
za, zb = stats.norm.ppf(0.975), stats.norm.ppf(0.80)
pbar = (p0 + p1) / 2
n_ind = 2 * pbar * (1 - pbar) * (za + zb) ** 2 / (p1 - p0) ** 2
print(f"independent conversations needed per arm: {n_ind:,.0f}")
assert 4000 < n_ind < 4400

# users have a personal resolve-propensity, and the same user retries: conversations in a user are correlated
rng = np.random.default_rng(36)
U, M = 3000, 4                      # users per arm, conversations per user
def arm(p, icc=0.2):
    a = p * (1 - icc) / icc; b = (1 - p) * (1 - icc) / icc       # Beta with intra-user correlation icc
    pu = rng.beta(a, b, U)
    y = rng.binomial(1, pu[:, None], (U, M))
    return y
yc, yt = arm(p0), arm(p1)
rc, rt = yc.mean(), yt.mean()
# naive: treat all U*M conversations as independent
se_naive = np.sqrt(rc*(1-rc)/(U*M) + rt*(1-rt)/(U*M))
# user-level: mean per user, compare users
uc, ut = yc.mean(1), yt.mean(1)
se_user = np.sqrt(uc.var(ddof=1)/U + ut.var(ddof=1)/U)
d = rt - rc
deff = (se_user / se_naive) ** 2
print(f"observed diff {d*100:+.2f} pts; naive SE {se_naive*100:.2f} pts; user-level SE {se_user*100:.2f} pts; design effect ~ {deff:.2f}")
print(f"naive z = {d/se_naive:.2f}   user-level z = {d/se_user:.2f}")
assert se_user > 1.2 * se_naive          # clustering widens the interval
rho = (deff - 1) / (M - 1)
print(f"implied intra-user correlation {rho:.2f} (built in: 0.20)")
assert 0.1 < rho < 0.3

# how much of the "same user, different answer" noise exists: same question, 5 retries, answer is right with prob q
q = 0.63
agree = q**2 + (1-q)**2
print(f"if retries were independent draws, two tries at the same question give the same outcome {agree:.0%} of the time when p(resolve)={q}")
assert round(agree, 2) == 0.53
