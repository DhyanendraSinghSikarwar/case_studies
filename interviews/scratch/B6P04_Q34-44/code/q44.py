# Q44: 8 variants vs control, best looks +4% (p = 0.02), re-test says +1.5%. Illustrative, seeded.
import numpy as np
from scipy import stats

base = 0.05
z = stats.norm.isf(0.02 / 2)
se_rel = 0.04 / z                                  # SE of the relative lift implied by +4% at p = 0.02
n_arm = 2 * base * (1 - base) / (se_rel * base) ** 2
print(f"+4% at p = 0.02 implies z = {z:.2f}, SE of relative lift {se_rel:.2%}, about {n_arm:,.0f} users per arm")
assert abs(z - 2.326) < 0.01 and 120_000 < n_arm < 135_000
print(f"Bonferroni p for 8 variants: {min(1, 0.02*8):.2f};  chance of >= 1 p<0.05 among 8 true nulls: {1-0.95**8:.1%}")
assert round(0.02 * 8, 2) == 0.16 and round(1 - 0.95 ** 8, 3) == 0.337
# does the re-test contradict the first estimate?
dz = (0.04 - 0.015) / np.sqrt(2) / se_rel
print(f"re-test +1.5% with the same SE: z for the difference {dz:.2f}; the re-test 95% CI is [{(0.015-1.96*se_rel):+.1%}, {(0.015+1.96*se_rel):+.1%}]")
assert dz < 1.5

rng = np.random.default_rng(44)
R, K, TAU = 20_000, 8, 0.015                        # true relative effects ~ N(0, 1.5%)
true = rng.normal(0, TAU, (R, K))
est = true + rng.normal(0, se_rel, (R, K))
best = est.argmax(1); idx = np.arange(R)
w_est, w_true = est[idx, best], true[idx, best]
print(f"winner: mean estimate {w_est.mean():+.2%}, mean true effect {w_true.mean():+.2%}, overstatement {w_est.mean()-w_true.mean():+.2%}")
assert w_est.mean() > w_true.mean() + 0.01
# winners that look like ours
sel = (w_est > 0.035) & (w_est < 0.045)
print(f"winners with estimate near +4%: {sel.sum()}; their mean true effect {w_true[sel].mean():+.2%}")
assert 0.0 < w_true[sel].mean() < 0.025
# empirical-Bayes shrinkage: prior variance from the 8 estimates in each experiment
shr_err, raw_err = [], []
for r in range(R):
    e = est[r]; v = max(e.var(ddof=1) - se_rel ** 2, 1e-8)
    b = v / (v + se_rel ** 2)
    post = e.mean() + b * (e - e.mean())
    shr_err.append(post[best[r]] - true[r, best[r]]); raw_err.append(e[best[r]] - true[r, best[r]])
print(f"mean error of winner: raw {np.mean(raw_err):+.2%}, shrunk {np.mean(shr_err):+.2%};  RMSE raw {np.sqrt(np.mean(np.square(raw_err))):.2%} vs shrunk {np.sqrt(np.mean(np.square(shr_err))):.2%}")
assert abs(np.mean(shr_err)) < abs(np.mean(raw_err)) / 2
# share of experiments in which the winner's re-test is >= 0 and its fresh estimate vs truth
fresh = true[idx, best] + rng.normal(0, se_rel, R)
print(f"fresh re-test of the winner: mean {fresh.mean():+.2%} (unbiased for its true effect {w_true.mean():+.2%})")
assert abs(fresh.mean() - w_true.mean()) < 0.001
