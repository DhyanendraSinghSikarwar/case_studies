# Q53: provider silently updates the model two weeks into a 4-week test (illustrative)
import numpy as np
from scipy import stats
rng = np.random.default_rng(53)
print("500 prompts: 82% =", round(.82*500), "passes, 87% =", round(.87*500), "passes, difference", round(.87*500)-round(.82*500), "prompts")
assert round(.82*500) == 410 and round(.87*500) == 435
# unpaired two-proportion z (ignores that it is the same 500 prompts)
se = np.sqrt(.82*.18/500 + .87*.13/500); z = .05/se
print("unpaired z", round(z, 2), "p =", round(2*stats.norm.sf(z), 3))
# paired view: same prompts. Illustrative split of the 25 net gains: 45 fixed, 20 broken
fixed, broken = 45, 20
assert fixed - broken == 25
mc = stats.binomtest(fixed, fixed+broken, 0.5)
print("McNemar exact (45 fixed vs 20 broken): p =", round(mc.pvalue, 4))
# noise floor: same model, same suite, rerun with sampling temperature (each prompt passes with its own prob)
p_i = np.clip(rng.beta(1.2, 0.3, 500), 0, 1); p_i *= 0.82 / p_i.mean(); p_i = np.clip(p_i, 0, 1)
runs = np.array([rng.binomial(1, p_i).mean() for _ in range(2000)])
print("rerun noise on the SAME model: mean", round(runs.mean(), 3), "sd", round(runs.std(), 4), "-> 95% of reruns within +/-", round(1.96*runs.std()*np.sqrt(2), 3), "of each other")
assert 0.8 < runs.mean() < 0.84
# what the update does to the experiment readout: effect 0 in weeks 1-2, +4 points in weeks 3-4, control unchanged
N = 25_000                                    # users per arm per week
def week(eff):
    c = rng.binomial(N, 0.300)/N; t = rng.binomial(N, 0.300 + eff)/N; return t - c
effs = [week(0.0) for _ in (1, 2)] + [week(0.04) for _ in (3, 4)]
print("weekly treatment-minus-control (points):", [round(100*e, 2) for e in effs])
pooled = np.mean(effs)
print("pooled 4-week estimate:", round(100*pooled, 2), "points  | pre-update weeks:", round(100*np.mean(effs[:2]), 2), "| post-update weeks:", round(100*np.mean(effs[2:]), 2))
assert abs(np.mean(effs[:2])) < 0.01 and np.mean(effs[2:]) > 0.03 and 0.01 < pooled < 0.03
