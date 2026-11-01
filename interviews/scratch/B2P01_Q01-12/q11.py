import numpy as np, torch
rng = np.random.default_rng(0)
n, d, Bk = 12, 4, 4
Q, K, V = (rng.normal(size=(n, d)) for _ in range(3))
S = Q @ K.T / np.sqrt(d); P = np.exp(S - S.max(1, keepdims=True)); P /= P.sum(1, keepdims=True)
ref = P @ V
out = np.zeros((n, d))
for i in range(n):                      # one query row; stream over key blocks
    m, l, acc = -np.inf, 0.0, np.zeros(d)
    for j in range(0, n, Bk):
        s = Q[i] @ K[j:j+Bk].T / np.sqrt(d)
        m_new = max(m, s.max())
        scale = np.exp(m - m_new)       # rescale old stats to the new max
        p = np.exp(s - m_new)
        l = l*scale + p.sum(); acc = acc*scale + p @ V[j:j+Bk]; m = m_new
    out[i] = acc / l
print("tiled == standard:", np.allclose(out, ref))
t = lambda a: torch.tensor(a)[None, None]
print("== torch SDPA:", np.allclose(torch.nn.functional.scaled_dot_product_attention(t(Q), t(K), t(V)).numpy()[0, 0], ref))
