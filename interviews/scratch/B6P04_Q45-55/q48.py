# Q48: regression to the mean in a "weakest 100 stores" pilot (illustrative simulation)
import numpy as np
rng = np.random.default_rng(48)
SIG, GROW = 0.115, 1.02                              # one-off luck sd, market-wide growth
S = 1000                                          # all stores
level = rng.lognormal(np.log(100), 0.20, S)       # each store's stable sales level
q0 = level * rng.lognormal(0, SIG, S)            # last quarter = level x one-off luck
q1 = GROW * level * rng.lognormal(0, SIG, S)     # next quarter, NO offer anywhere
weakest = np.argsort(q0)[:100]
chg = lambda idx: q1[idx].sum() / q0[idx].sum() - 1
print("no offer anywhere. all stores:", round(100*chg(np.arange(S)), 1), "%  weakest 100:", round(100*chg(weakest), 1), "%")
assert chg(weakest) > 0.08 and 0.0 < chg(np.arange(S)) < 0.04
# the pilot: true offer effect is only +1.5%
TRUE = 0.015
q1_pilot = q1.copy(); q1_pilot[weakest] *= 1 + TRUE
naive = q1_pilot[weakest].sum() / q0[weakest].sum() - 1
print("pilot reads", round(100*naive, 1), "% for the 100 weakest, true offer effect is", 100*TRUE, "%")
assert 0.09 < naive < 0.15
# redo: take the 200 weakest, randomly give the offer to 100 of them
reps, est = 2000, []
for _ in range(reps):
    lvl = rng.lognormal(np.log(100), 0.20, S)
    a = lvl * rng.lognormal(0, SIG, S); b = GROW * lvl * rng.lognormal(0, SIG, S)
    weak = np.argsort(a)[:200]; perm = rng.permutation(weak); tr, ct = perm[:100], perm[100:]
    b = b.copy(); b[tr] *= 1 + TRUE
    est.append((b[tr].sum()/a[tr].sum()) - (b[ct].sum()/a[ct].sum()))
est = np.array(est)
print("randomised among the 200 weakest: mean estimate", round(100*est.mean(), 2), "% (truth 1.5%), sd across reruns", round(100*est.std(), 2), "%")
assert abs(est.mean() - TRUE) < 0.004
