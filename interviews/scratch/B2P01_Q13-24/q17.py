import numpy as np
rng = np.random.default_rng(0)
for dk in [4, 64, 512]:
    q = rng.standard_normal((20000, dk)); k = rng.standard_normal((20000, dk))
    s = (q*k).sum(1)
    sm = lambda z: np.exp(z - z.max(-1, keepdims=True)) / np.exp(z - z.max(-1, keepdims=True)).sum(-1, keepdims=True)
    # softmax over 64 keys
    Q = rng.standard_normal((2000, dk)); K = rng.standard_normal((2000, 64, dk))
    raw = np.einsum('nd,nkd->nk', Q, K)
    print(dk, "var raw", round(s.var(),1), "var scaled", round((s/np.sqrt(dk)).var(),2),
          "| mean max softmax prob raw", round(sm(raw).max(1).mean(),3), "scaled", round(sm(raw/np.sqrt(dk)).max(1).mean(),3))
