import numpy as np
def alibi_slopes(H):            # geometric sequence for H a power of 2: 2^(-8/H * h), h=1..H
    return np.array([2 ** (-8 * (h + 1) / H) for h in range(H)])
print("slopes H=8:", alibi_slopes(8))
T = 5
i = np.arange(T)[:, None]; j = np.arange(T)[None, :]
bias = -alibi_slopes(8)[0] * (i - j).clip(min=0)       # head 0 slope=0.5, causal part only
print(bias)
# effect: with identical raw scores, attention to a token far away is damped by exp(-m*dist)
for m in alibi_slopes(8)[[0, 3, 7]]:
    dist = np.array([1, 16, 128, 1024]); print(f"slope {m:.5f}: exp(-m*dist) =", np.round(np.exp(-m * dist), 4))
