# Q42: what the leaked AUC would have promised vs the real one (binormal model, illustrative)
from scipy.stats import norm
def d_prime(auc): return 2**0.5 * norm.ppf(auc)
def prec_recall_top(auc, prev, frac):
    d = d_prime(auc)
    # find threshold c so that flagged share = frac: prev*(1-Phi(c-d)) + (1-prev)*(1-Phi(c)) = frac
    lo, hi = -10, 10
    for _ in range(200):
        c = (lo + hi) / 2
        share = prev * norm.sf(c - d) + (1 - prev) * norm.sf(c)
        if share > frac: lo = c
        else: hi = c
    tp = prev * norm.sf(c - d)
    return tp / frac, tp / prev
prev, frac = 0.10, 0.10
for auc in (0.91, 0.78):
    p, r = prec_recall_top(auc, prev, frac)
    print(f"AUC {auc}: reviewing top 10% of customers -> precision {p:.1%}, recall {r:.1%}")
p91, r91 = prec_recall_top(0.91, prev, frac)
p78, r78 = prec_recall_top(0.78, prev, frac)
assert p91 > p78 and r91 > r78
cust = 100_000
print("per 100,000 customers, positives caught in the top 10%:",
      round(cust*prev*r91), "promised vs", round(cust*prev*r78), "real")
print("shortfall =", round(cust*prev*(r91-r78)), "positives")
