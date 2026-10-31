# Illustrative. Translate AUC 0.80 vs 0.78 into bad rate among approved, and the fairness gap arithmetic.
from statistics import NormalDist
N = NormalDist()
gap0, gap1 = 18, 6
print("gap cut", gap0 - gap1, "points =", f"{(gap0-gap1)/gap0:.1%}")
assert gap0 - gap1 == 12 and round((gap0 - gap1) / gap0, 3) == 0.667
print("AUC drop", round(0.80 - 0.78, 2), "=", f"{0.02/0.80:.1%} relative")
assert round(0.02 / 0.80, 3) == 0.025
# Binormal: goods ~ N(0,1), bads ~ N(-d,1), AUC = Phi(d/sqrt2). Base default rate 10%, approve 60% of applicants.
def bad_rate_approved(auc, base=0.10, approve=0.60):
    d = 2 ** 0.5 * N.inv_cdf(auc)
    lo, hi = -10.0, 10.0
    for _ in range(100):                       # find cutoff c so that 60% score above c
        c = (lo + hi) / 2
        share = (1 - base) * (1 - N.cdf(c)) + base * (1 - N.cdf(c + d))
        if share > approve: lo = c
        else: hi = c
    bad_in = base * (1 - N.cdf(c + d))
    return bad_in / ((1 - base) * (1 - N.cdf(c)) + bad_in)
b80, b78 = bad_rate_approved(0.80), bad_rate_approved(0.78)
print(f"bad rate among approved: AUC 0.80 {b80:.2%}, AUC 0.78 {b78:.2%}, diff {100*(b78-b80):.2f} points")
assert round(b80, 4) == 0.0343 and round(b78, 4) == 0.0387, (b80, b78)
# Cost on 100,000 applicants, 60,000 approved, loss 2,000 per default (illustrative)
approved, loss = 60_000, 2000
extra_defaults = approved * (b78 - b80)
print(f"extra defaults {extra_defaults:.0f}, extra loss {extra_defaults*loss:,.0f}")
assert round(extra_defaults) == 266
