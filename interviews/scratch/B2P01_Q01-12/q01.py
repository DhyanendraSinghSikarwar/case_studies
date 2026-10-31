import numpy as np
rng = np.random.default_rng(0)
n, d_model, d_k = 4, 8, 4            # 4 tokens
X  = rng.normal(size=(n, d_model))
Wq, Wk, Wv = (rng.normal(size=(d_model, d_k)) for _ in range(3))
Q, K, V = X @ Wq, X @ Wk, X @ Wv     # (n, d_k) each
scores = Q @ K.T / np.sqrt(d_k)      # (n, n): token i vs token j
w = np.exp(scores - scores.max(-1, keepdims=True))
w /= w.sum(-1, keepdims=True)        # softmax over keys, each row sums to 1
out = w @ V                          # (n, d_k): weighted mix of values
print(scores.shape, w.sum(-1).round(3), out.shape)
print(w.round(2))
