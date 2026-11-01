import numpy as np
rng = np.random.default_rng(0)
# SYNTHETIC: true reward is a function of a 1-D feature x. Ensemble members are fit on small noisy
# data from the region x in [-1, 1] only, so they agree in-distribution and disagree far outside it.
def true_r(x): return np.sin(2 * x)
x_tr = rng.uniform(-1, 1, 40)
members = []
for k in range(8):
    idx = rng.choice(40, 40, replace=True)                     # bootstrap
    y = true_r(x_tr[idx]) + rng.normal(0, 0.15, 40)
    members.append(np.polyfit(x_tr[idx], y, 5))                # degree-5 polynomial "reward model"
for name, xs in [("in-distribution  x in [-1,1]", np.linspace(-1, 1, 50)),
                 ("shifted          x in [2,3]  ", np.linspace(2, 3, 50))]:
    preds = np.array([np.polyval(c, xs) for c in members])
    mean_err = np.abs(preds.mean(0) - true_r(xs)).mean()
    print(f"{name}: mean abs error {mean_err:7.3f} | ensemble std (disagreement) {preds.std(0).mean():8.3f}")
