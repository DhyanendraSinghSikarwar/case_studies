# Q32: 8% exposure, diluted ITT vs triggered analysis (illustrative simulation, seeded)
import numpy as np
from scipy import stats

rng = np.random.default_rng(32)
SHARE, ITT_REL, MU, SD = 0.08, 0.001, 20.0, 20.0
print("triggered lift implied by the prompt:", ITT_REL / SHARE * 100, "%")
assert abs(ITT_REL / SHARE - 0.0125) < 1e-12

z = stats.norm.ppf(0.975) + stats.norm.ppf(0.80)
n_trig = 2 * z**2 * SD**2 / (MU * 0.0125) ** 2
n_itt = 2 * z**2 * SD**2 / (MU * 0.001) ** 2
print(f"users per arm for 80% power: triggered analysis {n_trig:,.0f} triggered (= {n_trig/SHARE:,.0f} assigned); all-users analysis {n_itt:,.0f}; ratio {n_itt/(n_trig/SHARE):.2f}")
assert abs(n_itt / n_trig - 1 / SHARE**2) < 1e-6

# simulate 2,000 tests with 1.25M assigned users per arm; group means drawn from their exact sampling distribution
N, R = 1_250_000, 2000
def one():
    k_t, k_c = rng.binomial(N, SHARE, 2)                       # triggered users per arm
    # triggered users: control mean MU, treatment mean MU*1.0125; the other users: MU in both arms
    t_trig = rng.normal(MU * 1.0125, SD / np.sqrt(k_t)); c_trig = rng.normal(MU, SD / np.sqrt(k_c))
    t_non = rng.normal(MU, SD / np.sqrt(N - k_t)); c_non = rng.normal(MU, SD / np.sqrt(N - k_c))
    t_all = (k_t * t_trig + (N - k_t) * t_non) / N; c_all = (k_c * c_trig + (N - k_c) * c_non) / N
    se_all = SD * np.sqrt(2 / N); se_trig = SD * np.sqrt(1 / k_t + 1 / k_c)
    return (t_all - c_all) / se_all, (t_trig - c_trig) / se_trig
zs = np.array([one() for _ in range(R)])
pw = (np.abs(zs) > 1.96).mean(axis=0)
print(f"power with 1.25M assigned per arm: all-users {pw[0]:.2f}; triggered-only {pw[1]:.2f}")
assert pw[0] < 0.2 and 0.7 < pw[1] < 0.9

# the trigger rule must be symmetric. Feature does NOTHING here. Spend ~ heavy-tailed; 'treatment users who clicked the new setting' are engaged users.
M = 400_000
spend_t = rng.lognormal(2.5, 1.0, M); spend_c = rng.lognormal(2.5, 1.0, M)
asym = spend_t[spend_t > np.quantile(spend_t, 1 - SHARE)].mean() / spend_c.mean() - 1                 # treated: 'engaged', control: everybody
sym = spend_t[rng.random(M) < SHARE].mean() / spend_c[rng.random(M) < SHARE].mean() - 1               # same rule on both arms (would-have-reached)
print(f"no true effect: asymmetric trigger reads {asym*100:+.0f}%; symmetric trigger reads {sym*100:+.1f}%")
assert asym > 1.0 and abs(sym) < 0.05
