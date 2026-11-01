import numpy as np
rng = np.random.default_rng(21)

conv_c, conv_t = 0.0800, 0.0816
aov_c, aov_t = 50.00, 48.50
print("conversion relative change %:", round((conv_t / conv_c - 1) * 100, 2))
print("AOV relative change %:", round((aov_t / aov_c - 1) * 100, 2))
rpv_c, rpv_t = conv_c * aov_c, conv_t * aov_t
print(f"revenue per visitor: control {rpv_c:.4f}, treatment {rpv_t:.4f}, change {(rpv_t/rpv_c-1)*100:.2f}%")
assert round((conv_t / conv_c - 1) * 100, 2) == 2.0
assert round((aov_t / aov_c - 1) * 100, 2) == -3.0
assert round(rpv_t, 4) == 3.9576 and round((rpv_t / rpv_c - 1) * 100, 2) == -1.06

# Simulate a test: 2,000,000 visitors per arm, lognormal order values (sd about 40), with a fixed seed
n = 2_000_000
def arm(conv, aov, n):
    buy = rng.random(n) < conv
    sigma = 0.7
    mu = np.log(aov) - sigma ** 2 / 2
    val = np.where(buy, rng.lognormal(mu, sigma, n), 0.0)
    return buy, val
bc, vc = arm(conv_c, aov_c, n)
bt, vt = arm(conv_t, aov_t, n)

def diff_ci(a, b):
    d = b.mean() - a.mean()
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return d, d - 1.96 * se, d + 1.96 * se, d / se
d, lo, hi, z = diff_ci(bc.astype(float), bt.astype(float))
print(f"conversion diff {d*100:.3f} pts, z = {z:.2f}")
assert z > 1.96
d, lo, hi, z = diff_ci(vc[bc], vt[bt])
print(f"AOV diff {d:.2f}, z = {z:.2f}")
assert z < -1.96
d, lo, hi, z = diff_ci(vc, vt)
print(f"revenue per visitor diff {d:.3f} (95% CI {lo:.3f} to {hi:.3f}), z = {z:.2f}")
rel = d / vc.mean()
print(f"relative change in revenue per visitor: {rel*100:.2f}%")
assert d < 0 and -0.03 < rel < 0.0
