import numpy as np
rng = np.random.default_rng(0)
def rope(x, pos, base=10000.0):
    d = x.shape[-1]; th = base ** (-np.arange(0, d, 2)/d)
    a = pos*th; c, s = np.cos(a), np.sin(a)
    x1, x2 = x[0::2], x[1::2]
    out = np.empty_like(x); out[0::2] = x1*c - x2*s; out[1::2] = x1*s + x2*c
    return out
q, k = rng.normal(size=8), rng.normal(size=8)
for m, n in [(3, 1), (13, 11), (1003, 1001)]:      # same offset m-n = 2
    print(m, n, round(float(rope(q, m) @ rope(k, n)), 6))
print("different offset:", round(float(rope(q, 5) @ rope(k, 1)), 6))
# sinusoidal
def sinus(T, d):
    pos = np.arange(T)[:, None]; i = np.arange(0, d, 2)[None]
    pe = np.zeros((T, d)); pe[:, 0::2] = np.sin(pos/10000**(i/d)); pe[:, 1::2] = np.cos(pos/10000**(i/d)); return pe
print(sinus(4, 8).round(2)[1])
