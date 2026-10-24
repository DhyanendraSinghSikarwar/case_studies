import numpy as np
def sinpe(n, d):
    pos = np.arange(n)[:, None]
    w = 1.0 / 10000 ** (np.arange(0, d, 2) / d)       # one frequency per sin/cos pair
    pe = np.zeros((n, d))
    pe[:, 0::2] = np.sin(pos * w)
    pe[:, 1::2] = np.cos(pos * w)
    return pe, w
d, k = 16, 5
pe, w = sinpe(200, d)
# 1) PE(p+k) = R_k PE(p), R_k block-diagonal rotation that does not depend on p
def rot(k):
    R = np.zeros((d, d))
    for i, wi in enumerate(w):
        c, s = np.cos(k*wi), np.sin(k*wi)
        R[2*i:2*i+2, 2*i:2*i+2] = [[c, s], [-s, c]]
    return R
R = rot(k)
err = max(np.abs(R @ pe[p] - pe[p+k]).max() for p in range(0, 150, 7))
print("max |R_k PE(p) - PE(p+k)| over p:", err)
# 2) dot product PE(p).PE(p+k) = sum_i cos(k w_i): depends only on k
dots = [pe[p] @ pe[p+k] for p in (0, 10, 50, 120)]
print("dots for p=0,10,50,120:", np.round(dots, 6), " formula:", round(np.cos(k*w).sum(), 6))
# 3) the dot product decays with distance but is not monotonic
print("PE(0).PE(k) for k=0,1,5,20,100:", np.round([pe[0]@pe[j] for j in (0,1,5,20,100)], 2))
# 4) positions beyond training length are still defined, but never seen
pe2,_ = sinpe(5000, 64); print("PE norm^2 (d=64) pos 0 and 4000:", round(pe2[0]@pe2[0],3), round(pe2[4000]@pe2[4000],3))
