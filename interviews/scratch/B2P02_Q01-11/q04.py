import numpy as np
def softmax(z): e = np.exp(z - z.max()); return e / e.sum()
logits = np.array([4.0, 3.0, 2.0, 1.0, 0.0, -1.0])
for T in [0.5, 1.0, 2.0]:
    print("T", T, np.round(softmax(logits / T), 3))
def top_k(p, k):
    q = np.zeros_like(p); i = np.argsort(-p)[:k]; q[i] = p[i]; return q / q.sum()
def top_p(p, tp):
    o = np.argsort(-p); c = np.cumsum(p[o]); n = np.searchsorted(c, tp) + 1  # smallest set with mass >= tp
    q = np.zeros_like(p); q[o[:n]] = p[o[:n]]; return q / q.sum()
p = softmax(logits)
print("p      ", np.round(p, 3))
print("top-k=3", np.round(top_k(p, 3), 3))
print("top-p=.9", np.round(top_p(p, 0.9), 3), "kept", int((top_p(p,0.9)>0).sum()))
flat = softmax(np.array([1.0,0.9,0.8,0.7,0.6,0.5]))
print("flat p ", np.round(flat,3), "top-p .9 keeps", int((top_p(flat,0.9)>0).sum()), "top-k 3 keeps", 3)
