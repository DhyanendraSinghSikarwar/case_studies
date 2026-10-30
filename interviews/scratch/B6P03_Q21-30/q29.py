# Q29 only rule-flagged transactions were reviewed: positive-unlabelled labels (illustrative simulation)
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(29)

# 1) Arithmetic from the prompt
total, reviewed, confirmed = 1_000_000, 20_000, 1_500
print(f"reviewed share {reviewed/total:.1%}; confirmed precision of the old rules {confirmed/reviewed:.1%}; unreviewed rows {total-reviewed:,}")
assert reviewed / total == 0.02 and confirmed / reviewed == 0.075 and total - reviewed == 980_000
# A random audit of 3,000 unreviewed transactions (illustrative result: 9 frauds)
audit_n, audit_hit = 3_000, 9
r = audit_hit / audit_n
hidden = r * (total - reviewed)
print(f"audit fraud rate in unreviewed {r:.2%} -> about {hidden:,.0f} hidden frauds; recall of the old rules about {confirmed/(confirmed+hidden):.1%}")
assert abs(hidden - 2_940) < 1e-6 and round(confirmed / (confirmed + hidden), 3) == 0.338
half = 1.96 * (r * (1 - r) / audit_n) ** 0.5
print(f"audit rate 95% interval about {r-half:.2%} to {r+half:.2%}")

# 2) Simulation: train on 'reviewed-and-confirmed = 1, everything else = 0' versus on the true labels
n = 400_000
x1 = rng.normal(size=n); x2 = rng.normal(size=n); x3 = rng.normal(size=n)
logit = -6.2 + 1.0 * x1 + 1.3 * x2 + 0.9 * x3
fraud = rng.random(n) < 1 / (1 + np.exp(-logit))
flagged = x1 > np.quantile(x1, 0.98)                    # old rule: top 2% on x1 only
observed = fraud & flagged                              # only flagged rows are ever confirmed
print(f"true frauds {fraud.sum()}, confirmed {observed.sum()} ({observed.sum()/fraud.sum():.1%} of all frauds); precision of rule {observed.sum()/flagged.sum():.1%}")
X = np.c_[x1, x2, x3, np.ones(n)]
def fit(y):
    f = lambda w: (np.mean(np.logaddexp(0, X @ w) - y * (X @ w)), X.T @ (1 / (1 + np.exp(-(X @ w))) - y) / n)
    return minimize(f, np.zeros(4), jac=True, method="L-BFGS-B").x
w_naive, w_true = fit(observed.astype(float)), fit(fraud.astype(float))
print("coefficients (x1, x2, x3): naive", np.round(w_naive[:3], 2), "| true labels", np.round(w_true[:3], 2))
assert w_naive[0] > 2.5 * w_true[0]          # the naive model leans on the old rule's own feature

# Honest test: a random audit of 20,000 rows labelled with the true outcome; review budget = top 2%
audit = rng.choice(n, 20_000, replace=False)
def recall_at(w, idx, y, share=0.02):
    s = X[idx] @ w; k = int(share * len(idx)); top = np.argsort(-s)[:k]
    return y[idx][top].sum() / y[idx].sum()
print(f"random audit: recall in top 2%: naive model {recall_at(w_naive, audit, fraud):.1%}, true-label model {recall_at(w_true, audit, fraud):.1%}")
# naive evaluation: only judged on observed labels (reviewed rows) looks much better
rev = np.where(flagged)[0]
s_n = X[rev] @ w_naive
print(f"naive evaluation on the reviewed rows only: share of confirmed frauds in naive top 50%: {observed[rev][np.argsort(-s_n)[:len(rev)//2]].sum()/observed[rev].sum():.1%}")
assert recall_at(w_true, audit, fraud) > recall_at(w_naive, audit, fraud) + 0.05
