# Q35: CTR/query +5%, queries/session +8%, purchases/session flat. Illustrative, seeded.
import numpy as np
from scipy import stats

print("clicks per session ratio =", round(1.05 * 1.08, 3))
assert round(1.05 * 1.08, 3) == 1.134      # +13.4% clicks per session implied

rng = np.random.default_rng(35)
S = 200_000                                  # sessions per arm
def arm(q_mean, ctr, p_buy):
    q = rng.poisson(q_mean - 1, S) + 1       # queries per session (>=1)
    clicks = rng.binomial(q, ctr)
    buy = rng.random(S) < p_buy              # purchase does not depend on arm by construction
    first_click = (clicks > 0)
    return q, clicks, buy, first_click
qc, cc, bc, fc = arm(2.00, 0.300, 0.050)
qt, ct, bt, ft = arm(2.16, 0.315, 0.050)

print(f"queries/session  C {qc.mean():.3f}  T {qt.mean():.3f}  ({qt.mean()/qc.mean()-1:+.1%})")
ctr_c, ctr_t = cc.sum()/qc.sum(), ct.sum()/qt.sum()
print(f"CTR per query    C {ctr_c:.4f}  T {ctr_t:.4f}  ({ctr_t/ctr_c-1:+.1%})")
print(f"clicks/session   C {cc.mean():.3f}  T {ct.mean():.3f}  ({ct.mean()/cc.mean()-1:+.1%})")
assert abs(qt.mean()/qc.mean() - 1.08) < 0.01 and abs(ctr_t/ctr_c - 1.05) < 0.02

d = bt.mean() - bc.mean()
se = np.sqrt(bt.var()/S + bc.var()/S)
lo, hi = d - 1.96*se, d + 1.96*se
print(f"purchases/session diff {d*100:+.2f} pts, 95% CI [{lo*100:+.2f}, {hi*100:+.2f}] pts  = [{lo/0.05:+.1%}, {hi/0.05:+.1%}] relative")
assert lo < 0 < hi                           # flat: cannot reject zero
print(f"width of CI: +/-{1.96*se/0.05:.1%} relative -> a flat result rules out only effects bigger than that")
# extra cut: queries needed per purchase, and share of sessions with 3+ queries
print(f"queries per purchase  C {qc.sum()/bc.sum():.1f}  T {qt.sum()/bt.sum():.1f}")
print(f"sessions with 3+ queries  C {np.mean(qc>=3):.1%}  T {np.mean(qt>=3):.1%}")
assert np.mean(qt >= 3) > np.mean(qc >= 3)
