# SYNTHETIC simulation: majority vote of N agents, independent vs correlated errors. Not real model data.
# Correlation model: with probability rho the agents share ONE common draw (a shared blind spot, as if from the same base model),
# otherwise each draws independently. Every agent is correct with probability p marginally.
import numpy as np
rng = np.random.default_rng(0)
def vote_accuracy(n_agents, p, rho, trials=40000):
    shared = rng.random(trials) < rho                      # trials where agents copy the same draw
    common = rng.random(trials) < p
    indep = rng.random((trials, n_agents)) < p
    correct = np.where(shared[:, None], common[:, None], indep)
    return float(np.mean(correct.sum(1) * 2 > n_agents))   # strict majority correct (use odd N)
p = 0.7
print(f"single agent accuracy p = {p}")
print("N   rho=0.0  rho=0.5  rho=0.9")
rows = {}
for n in (1, 3, 5, 9, 15):
    rows[n] = [vote_accuracy(n, p, r) for r in (0.0, 0.5, 0.9)]
    print(f"{n:<3} " + "  ".join(f"{a:.3f}  " for a in rows[n]))
assert abs(rows[1][0] - p) < 0.02 and rows[15][0] > 0.93            # independent: big gain
assert rows[15][2] < p + 0.06 and rows[15][1] < rows[15][0]         # correlated: benefit mostly gone
assert abs(rows[9][2] - rows[15][2]) < 0.03                         # diminishing: more agents barely help
print("tests passed")
