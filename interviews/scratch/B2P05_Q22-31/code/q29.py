import numpy as np
rng = np.random.default_rng(5)
# SYNTHETIC scores for two categories with different difficulty.
def make(n_pos, n_neg, a, b):
    return np.r_[rng.beta(*a, n_pos), rng.beta(*b, n_neg)], np.r_[np.ones(n_pos), np.zeros(n_neg)]
data = {"self_harm": make(150, 3000, (6,2), (1.5,7)),
        "weapons":   make(80, 3000, (4,2), (2,6))}
def prf(s, y, t):
    p = s >= t; tp=(p&(y==1)).sum(); fp=(p&(y==0)).sum(); fn=(~p&(y==1)).sum()
    return tp/max(tp+fp,1), tp/(tp+fn), fp, fn
C_FN, C_FP = 50.0, 1.0      # ASSUMED costs: a miss is 50x worse than a false alarm
ts = np.linspace(0.05, 0.95, 91)
for cat, (s, y) in data.items():
    costs = [C_FN*prf(s,y,t)[3] + C_FP*prf(s,y,t)[2] for t in ts]
    t_best = ts[int(np.argmin(costs))]
    p, r, fp, fn = prf(s, y, t_best)
    p5, r5, fp5, fn5 = prf(s, y, 0.5)
    print(f"{cat:10s} best t={t_best:.2f} P={p:.2f} R={r:.2f} cost={C_FN*fn+C_FP*fp:7.1f} | at t=0.5: P={p5:.2f} R={r5:.2f} cost={C_FN*fn5+C_FP*fp5:7.1f}")
