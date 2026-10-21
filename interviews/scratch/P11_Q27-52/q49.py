import numpy as np
rng = np.random.default_rng(2)
n, K = 200_000, 5
x = rng.random(n)                                             # context
true_p = np.stack([0.02 + 0.05 * x, 0.06 - 0.04 * x, np.full(n, 0.04),
                   np.full(n, 0.03), np.full(n, 0.01)], 1)    # true click prob per action
log_prob = np.array([0.1, 0.1, 0.6, 0.1, 0.1])                # logging policy favours action 2
a_log = rng.choice(K, size=n, p=log_prob)
click = rng.random(n) < true_p[np.arange(n), a_log]
a_new = np.where(x > 0.5, 1, 0)                               # candidate policy
w = (a_new == a_log) / log_prob[a_log]                        # importance weights
ips = (w * click).mean()
snips = (w * click).sum() / w.sum()
truth = true_p[np.arange(n), a_new].mean()
print(f"true {truth:.4f} | IPS {ips:.4f} | SNIPS {snips:.4f} | logged CTR (naive) {click.mean():.4f}")
