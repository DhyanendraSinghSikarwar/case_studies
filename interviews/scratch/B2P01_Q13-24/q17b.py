import numpy as np
rng = np.random.default_rng(0)
def softmax(z): e = np.exp(z - z.max(-1, keepdims=True)); return e / e.sum(-1, keepdims=True)
for dk in [4, 64, 512]:
    Q = rng.standard_normal((2000, dk)); K = rng.standard_normal((2000, 64, dk))
    raw = np.einsum('nd,nkd->nk', Q, K)                       # one score per (query, key)
    print(dk, round(raw.var(), 1), round((raw / np.sqrt(dk)).var(), 2),
          round(softmax(raw).max(1).mean(), 3), round(softmax(raw / np.sqrt(dk)).max(1).mean(), 3))
