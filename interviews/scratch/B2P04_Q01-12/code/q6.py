import numpy as np
from statistics import NormalDist
rng = np.random.default_rng(0)
w = rng.normal(0, 0.02, size=(4096 * 64,))          # TOY: normal "weights"
blocks = w.reshape(-1, 64)                           # blockwise, block size 64
scale = np.abs(blocks).max(1, keepdims=True)
x = blocks / scale                                   # in [-1, 1]

# (a) uniform 4-bit: 16 evenly spaced levels in [-1, 1]
uni = np.linspace(-1, 1, 16)
# (b) quantile-style 4-bit codebook (NF4-STYLE TOY, NOT the real NF4 table):
#     levels at quantiles of a standard normal, rescaled to [-1, 1]
nd = NormalDist()
q = np.array([nd.inv_cdf(p) for p in (np.arange(16) + 0.5) / 16])
quant = q / np.abs(q).max()
def roundtrip(x, book):
    idx = np.abs(x[..., None] - book).argmin(-1)
    return book[idx]
for name, book in (("uniform 4-bit", uni), ("quantile-style 4-bit (toy)", quant)):
    deq = roundtrip(x, book) * scale
    print(f"{name:28s} MSE {np.mean((deq - blocks)**2):.3e}")
print("16 levels = 4 bits; scale per 64-block costs extra bits (what double quantization shrinks)")
print("fp32 scale overhead: %.3f bits/param" % (32 / 64))
