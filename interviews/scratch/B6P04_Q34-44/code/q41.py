# Q41: synthetic control, 1 treated + 15 donors, 8 pre weeks, placebo-in-space test. Illustrative, seeded.
import numpy as np
from scipy.optimize import minimize

U, PRE, POST = 16, 8, 8
print("smallest possible placebo p-value with 16 units: 1/16 =", round(1 / 16, 4))
assert round(1 / 16, 4) == 0.0625          # cannot reach 0.05 however large the gap

def synth_gap(Y, i, pre):
    """Fit non-negative weights summing to 1 on the other units, return gap series (unit i minus synthetic), in % of own level."""
    others = [j for j in range(Y.shape[0]) if j != i]
    X = Y[others][:, :pre].T; y = Y[i, :pre]
    k = len(others)
    f = lambda w: np.sum((X @ w - y) ** 2)
    res = minimize(f, np.full(k, 1 / k), method="SLSQP", bounds=[(0, 1)] * k,
                   constraints={"type": "eq", "fun": lambda w: w.sum() - 1}, options={"maxiter": 200})
    w = res.x
    return (Y[i] - w @ Y[others]) / Y[i, :pre].mean()

def one_world(rng, effect):
    t = np.arange(PRE + POST)
    common = 100 * (1 + 0.004 * t + 0.02 * np.sin(t / 2.0))
    load1 = rng.normal(0, 1, U); load2 = rng.normal(0, 1, U)
    f2 = np.cumsum(rng.normal(0, 0.6, PRE + POST))
    Y = common[None, :] * (1 + 0.04 * load1[:, None] * (t[None, :] - 4) / 8 + 0.01 * load2[:, None] * f2[None, :] / 2)
    Y = Y * (1 + rng.normal(0, 0.022, Y.shape))            # weekly noise
    Y[0, PRE:] *= (1 + effect)                                # unit 0 is the launch country
    return Y

def ratios(Y):
    out = []
    for i in range(U):
        g = synth_gap(Y, i, PRE)
        pre = np.sqrt(np.mean(g[:PRE] ** 2)); post = np.sqrt(np.mean(g[PRE:] ** 2))
        out.append((pre, post, post / pre, g[PRE:].mean()))
    return np.array(out)

rng = np.random.default_rng(41)
Y = one_world(rng, 0.025)
r = ratios(Y)
rank = int((r[:, 2] >= r[0, 2]).sum())
print(f"launch country: pre-RMSPE {r[0,0]*100:.2f}%  mean post gap {r[0,3]*100:+.2f}%  post/pre ratio {r[0,2]:.1f}")
print(f"placebo countries: median pre-RMSPE {np.median(r[1:,0])*100:.2f}%, largest |mean post gap| {np.abs(r[1:,3]).max()*100:.2f}%")
print(f"rank of the launch ratio among 16: {rank}  -> placebo p = {rank}/16 = {rank/16:.3f}")
assert rank / 16 >= 0.0625

# how often would a real +2.5% effect even rank first, and how often does a zero effect rank first? (80 worlds each)
for eff in (0.025, 0.0):
    firsts = 0; sims = 80; gaps = []
    for s in range(sims):
        rr = ratios(one_world(np.random.default_rng(1000 + s), eff))
        firsts += int(rr[0, 2] >= rr[1:, 2].max()); gaps.append(rr[0, 3])
    print(f"true effect {eff:+.1%}: launch country has the top ratio in {firsts}/{sims} worlds ({firsts/sims:.0%}); mean estimated gap {np.mean(gaps)*100:+.2f}%")
    if eff == 0.0:
        assert firsts / sims < 0.2             # near 1/16 = 6%
