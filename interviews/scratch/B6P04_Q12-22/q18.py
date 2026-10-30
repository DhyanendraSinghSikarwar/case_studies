# Q18: SRM from a crash on older phones and the '+2% per logged user' (illustrative simulation)
import numpy as np
from scipy.stats import chisquare

# 1) SRM test on the observed counts
obs = np.array([495_000, 505_000])
exp = np.array([500_000, 500_000])
chi2, p = chisquare(obs, exp)
print(f"chi-square = {chi2:.0f}, p = {p:.1e}")
assert round(chi2) == 100 and p < 1e-20

# 2) Largest bias that dropping f of the arm can create: survivors vs the whole arm
#    survivor mean / whole-arm mean = (1 - f*r)/(1 - f), where r = mean of dropped users / overall mean
assigned_c = 505_000
logged_t = 495_000
f = (assigned_c - logged_t) / assigned_c       # assumes both arms were assigned 505,000
print(f"share of treatment users missing (if assigned 505,000 each): {f:.2%}")
print(f"maximum possible inflation (dropped users engage 0): {f/(1-f):+.2%}")
assert abs(f - 0.0198) < 0.0001 and abs(f/(1-f) - 0.0202) < 0.0002
f_small = 5_000 / 500_000                       # if each arm was assigned 500,000
print(f"if only 5,000 were missing of 500,000: max inflation {f_small/(1-f_small):+.2%}")
assert f_small / (1 - f_small) < 0.0102

# 3) Simulation: true treatment effect is ZERO; dropped users are older-phone users who engage less
rng = np.random.default_rng(18)
n = 505_000
def make_arm(drop):
    old = rng.random(n) < 0.0198                       # older phones
    base = rng.gamma(2.0, 5.0, n)                      # engagement per user, mean 10
    eng = np.where(old, base * 0.05, base)             # older-phone users engage at 5% of normal
    keep = ~(old & drop)                               # in treatment their sessions never log
    return eng, keep
ec, kc = make_arm(False)
et, kt = make_arm(True)
print(f"logged users: control {kc.sum():,}, treatment {kt.sum():,}")
naive = et[kt].mean() / ec[kc].mean() - 1
itt = et.mean() / ec.mean() - 1     # all assigned users, missing sessions counted as the engagement they have (0 if lost)
et_itt = np.where(kt, et, 0.0)
itt_zero = et_itt.mean() / ec.mean() - 1
print(f"naive per logged user lift = {naive:+.2%} (true effect 0)")
print(f"analysis on ALL assigned users, lost users counted as zero: {itt_zero:+.2%}")
se_rel = np.sqrt(et[kt].var()/kt.sum() + ec[kc].var()/kc.sum()) / ec[kc].mean()
print(f"sampling noise (1 SE) of that lift = {se_rel:.2%}")
assert se_rel < 0.002
assert 0.015 < naive < 0.022 and abs(itt_zero) < 0.01
print("all asserts passed")
