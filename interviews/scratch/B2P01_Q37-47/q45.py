import numpy as np
# Speculative decoding: expected tokens produced per target-model forward pass,
# if each drafted token is accepted independently with prob a (simplifying assumption), k drafted tokens
def expected(a, k): return (1 - a**(k+1)) / (1 - a)
for a in (0.5, 0.7, 0.9):
    print(f"a={a}:", {k: round(expected(a, k), 2) for k in (1, 2, 4, 8)})
# quick Monte-Carlo check of the formula
rng = np.random.default_rng(0); a, k = 0.7, 4
def one():
    n = 0
    while n < k and rng.random() < a: n += 1
    return n + 1                    # accepted drafts + 1 token from the target (correction or bonus)
print("MC a=0.7,k=4:", np.mean([one() for _ in range(200000)]).round(3), "formula:", round(expected(a, k), 3))
