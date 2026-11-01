# Standalone, numpy only. SYNTHETIC: no real model or reward model.
import numpy as np
rng = np.random.default_rng(0)

# ---- Part A: best-of-n on a proxy reward = true reward + noise ----
def bon_true(n, noise, hack_rate=0.0, trials=20000):
    t = rng.normal(0, 1, (trials, n))                              # true reward of each of n samples
    proxy = t + rng.normal(0, noise, (trials, n))
    if hack_rate:                                                  # a few samples "exploit" the RM: huge proxy, bad true reward
        h = rng.random((trials, n)) < hack_rate
        proxy = np.where(h, proxy + 5.0, proxy); t = np.where(h, -2.0, t)
    pick = proxy.argmax(1)
    return t[np.arange(trials), pick].mean(), proxy[np.arange(trials), pick].mean()
ns = [1, 2, 4, 8, 16, 64, 256, 1024]
print("true reward of the selected sample (mean over 20000 prompts); higher is better")
print(f"{'n':>5} | {'noise 0.3':>9} {'noise 2.0':>9} | {'noise 0.5 + 1% RM exploits':>27} (proxy of pick)")
for n in ns:
    a, b = bon_true(n, .3)[0], bon_true(n, 2.0)[0]; c, cp = bon_true(n, .5, 0.01)
    print(f"{n:5d} | {a:9.2f} {b:9.2f} | {c:14.2f} ({cp:5.2f})")

# ---- Part B: KL of the best-of-n distribution from the base, vs log n - (n-1)/n ----
def bon_kl(p, n):                      # p: base probabilities of outcomes already sorted by reward (low to high, no ties)
    F = np.cumsum(p); Fprev = np.concatenate([[0.], F[:-1]]); q = F**n - Fprev**n
    m = q > 0; return float((q[m] * np.log(q[m] / p[m])).sum()), q
print("\nKL(best-of-n || base) on a discrete toy (outcomes sorted by reward) vs the claimed bound log n - (n-1)/n")
for name, p in [("uniform over 1000", np.ones(1000) / 1000), ("random over 50", rng.dirichlet(np.ones(50))),
                ("skewed over 20", np.array([2.0 ** -i for i in range(20)]) / np.array([2.0 ** -i for i in range(20)]).sum())]:
    row = []
    for n in (2, 4, 16, 64):
        kl, q = bon_kl(p, n); assert abs(q.sum() - 1) < 1e-9
        row.append(f"n={n}: KL {kl:.3f} <= {np.log(n) - (n - 1) / n:.3f} {'ok' if kl <= np.log(n) - (n - 1) / n + 1e-12 else 'VIOLATED'}")
    print(f"  {name:18s}", " | ".join(row))
print("generation cost: n=1 -> 1x, n=16 -> 16x the samples per request (can run in parallel, so latency grows less than cost)")
