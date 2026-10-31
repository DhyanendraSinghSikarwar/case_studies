import numpy as np
# SYNTHETIC: each sampled CoT answer is correct w.p. p; wrong answers spread uniformly over 4 wrong values.
# Assumes samples are independent (real samples are correlated, so real gains are smaller).
rng = np.random.default_rng(0)
def maj_acc(p, n, trials=20000):
    correct = rng.random((trials, n)) < p
    ans = np.where(correct, 0, rng.integers(1, 5, (trials, n)))   # 0 = right answer
    counts = np.stack([(ans == v).sum(1) for v in range(5)], 1)
    # ties broken uniformly at random
    noisy = counts + rng.random(counts.shape) * 0.5
    return (noisy.argmax(1) == 0).mean()
for p in (0.4, 0.6):
    print(f"single-sample accuracy {p}")
    for n in (1, 3, 5, 11, 21, 41):
        print(f"  n={n:3d}  majority acc {maj_acc(p, n):.3f}  relative cost {n}x")
