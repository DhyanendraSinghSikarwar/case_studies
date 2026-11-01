import numpy as np
# ILLUSTRATIVE toy. Each sample is right w.p. p=0.4. A verifier gives right answers score ~ N(d,1), wrong ~ N(0,1);
# best-of-n picks the highest score. d = verifier quality (0 = random, large = near-perfect).
rng = np.random.default_rng(0)
p, trials = 0.4, 20000
tokens_per_sample, price_per_M = 500, 10.0           # assumed: 500 output tokens, $10 per 1M output tokens
def best_of_n(n, d):
    right = rng.random((trials, n)) < p
    score = rng.normal(0, 1, (trials, n)) + d * right
    return right[np.arange(trials), score.argmax(1)].mean()
print(" n | cost/query($) | d=0 (useless) | d=1 | d=2 | d=4 | oracle (any right)")
for n in (1, 2, 4, 8, 16, 32):
    cost = n * tokens_per_sample * price_per_M / 1e6
    oracle = 1 - (1 - p) ** n
    print(f"{n:2d} | {cost:.4f}        | " + " | ".join(f"{best_of_n(n, d):.3f}" for d in (0, 1, 2, 4)) + f" | {oracle:.3f}")
