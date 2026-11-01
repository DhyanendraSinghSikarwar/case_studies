# Q10 chargebacks arrive up to 60 days late: recent weeks look cleaner than they are (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(10)
def sig(x): return 1 / (1 + np.exp(-x))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(A, y, iters=25):
    b = np.zeros(A.shape[1])
    for _ in range(iters):
        p = sig(A @ b); g = A.T @ (p - y); H = (A * (p * (1 - p))[:, None]).T @ A + 1e-6 * np.eye(len(b))
        b -= np.linalg.solve(H, g)
    return b

DAYS, PER_DAY, MAXD = 210, 2_000, 60
day = np.repeat(np.arange(DAYS), PER_DAY); n = len(day)            # day 0 oldest, day 209 = today
X = rng.normal(size=(n, 3))
true_fraud = rng.random(n) < sig(-5.45 + X @ np.array([1.0, 0.7, 0.4]))
true_fraud = true_fraud.astype(int)
# Chargeback delay in days: confirmed fraud shows up by age a with probability (a/60)^2.3 for a <= 60 (late-heavy, invented)
delay = MAXD * rng.random(n) ** (1 / 2.3)
age = DAYS - 1 - day
label_seen = (true_fraud == 1) & (delay <= age)                     # fraud confirmed so far
y_obs = label_seen.astype(int)

recent = age < 60; older = age >= 60
print(f"true fraud rate, last 60 days={true_fraud[recent].mean():.3%}; older={true_fraud[older].mean():.3%}")
print(f"observed rate:  last 60 days={y_obs[recent].mean():.3%}; older (fully matured)={y_obs[older].mean():.3%}")
assert abs(y_obs[older].mean() - true_fraud[older].mean()) < 1e-12     # nothing is pending after 60 days
assert 0.0024 < y_obs[recent].mean() < 0.0036 and 0.009 < y_obs[older].mean() < 0.0112

# Labelled-as-clean frauds inside a 'last three months' training window
win = age < 90
missed = (true_fraud[win] == 1) & (y_obs[win] == 0)
print(f"last-90-day window: true frauds={true_fraud[win].sum()}, labelled positive={y_obs[win].sum()}, hidden as 'good'={missed.sum()} ({missed.sum()/true_fraud[win].sum():.0%} of frauds)")
assert missed.sum() / true_fraud[win].sum() > 0.4

# Maturity curve by age band and a maturity-adjusted estimate of the recent rate
bands = [(0, 15), (15, 30), (30, 45), (45, 60), (60, 90)]
print("age band (days) | observed rate | share of final labels seen")
for lo, hi in bands:
    m = (age >= lo) & (age < hi)
    print(f"  {lo:2d}-{hi:2d}          | {y_obs[m].mean():.3%}        | {min(y_obs[m].mean() / true_fraud[older].mean(), 1):.0%}")
mat = np.clip((age[recent] / MAXD) ** 2.3, 0, 1).mean()             # average share of labels already in for the last 60 days
adj = y_obs[recent].mean() / mat
print(f"average maturity of last-60-day rows={mat:.2f}; maturity-adjusted rate={adj:.3%} (vs matured {y_obs[older].mean():.3%})")
assert abs(adj - y_obs[older].mean()) < 0.0015

# Train two models: (A) last 90 days as labelled today, (B) only rows aged 60-150 days (fully matured)
A = np.c_[np.ones(n), X]
old_win = (age >= 60) & (age < 150)
test = (age >= 150)                                                  # older, fully matured, evaluation window
bA = fit(A[win], y_obs[win]); bB = fit(A[old_win], y_obs[old_win])
for name, b in (("A: last 90 days, labels as they are", bA), ("B: matured rows aged 60-150 days   ", bB)):
    p = sig(A[test] @ b)
    print(f"{name}: matured-test AUC={auc(y_obs[test], p):.3f}; mean predicted={p.mean():.4f} vs observed {y_obs[test].mean():.4f}")
pA = sig(A[test] @ bA); pB = sig(A[test] @ bB)
assert pA.mean() < 0.6 * y_obs[test].mean() and abs(pB.mean() - y_obs[test].mean()) < 0.002
