# Q43: overall 50/50 passes SRM but iOS and Android are lopsided. Illustrative, seeded.
import numpy as np
from scipy import stats

ctl = {"iOS": 20_000, "Android": 30_000}
trt = {"iOS": 16_000, "Android": 34_000}
nc, nt = sum(ctl.values()), sum(trt.values())
print("users per arm: control", nc, " treatment", nt)
assert nc == 50_000 and nt == 50_000

def srm(c, t):
    exp = (c + t) / 2
    chi = (c - exp) ** 2 / exp + (t - exp) ** 2 / exp
    return chi, stats.chi2.sf(chi, 1)

print("overall: chi2 = %.1f p = %.3f" % srm(nc, nt))
for p in ctl:
    chi, pv = srm(ctl[p], trt[p])
    print(f"{p}: {ctl[p]} vs {trt[p]}  chi2 = {chi:.1f}  p = {pv:.2e}")
assert srm(nc, nt)[0] == 0
assert round(srm(20_000, 16_000)[0], 1) == 444.4 and round(srm(30_000, 34_000)[0], 1) == 250.0

# the real question: is platform mix the same in the two arms?
table = np.array([[20_000, 30_000], [16_000, 34_000]])
chi, p, dof, _ = stats.chi2_contingency(table, correction=False)
print(f"platform x arm independence: chi2 = {chi:.1f}, dof {dof}, p = {p:.1e}; iOS share control {20/50:.0%} vs treatment {16/50:.0%}")
assert round(chi, 1) == 694.4

# what it does to the pooled metric even if treatment does nothing: iOS converts 8%, Android 4% in BOTH arms
rate = {"iOS": 0.08, "Android": 0.04}
pc = sum(ctl[k] * rate[k] for k in ctl) / nc
pt = sum(trt[k] * rate[k] for k in trt) / nt
print(f"true effect 0, pooled conversion control {pc:.2%} vs treatment {pt:.2%}: fake change {pt-pc:+.2%} points ({pt/pc-1:+.1%} relative)")
assert round(pc, 4) == 0.056 and round(pt, 4) == 0.0528
se = np.sqrt(pc*(1-pc)/nc + pt*(1-pt)/nt)
print(f"z for that fake change = {(pt-pc)/se:.1f}")
assert 2.0 < abs((pt - pc) / se) < 2.5
# a platform-adjusted comparison (stratified) removes the compositional part
