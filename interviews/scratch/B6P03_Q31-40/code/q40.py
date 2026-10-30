import numpy as np
from scipy.optimize import minimize
from scipy.stats import rankdata

rng = np.random.default_rng(40)
def auc(y, s):
    r = rankdata(s); n1 = int(y.sum()); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))
sig = lambda a: 1 / (1 + np.exp(-a))

n = 30_000
X = rng.normal(size=(n, 4)); w_true = np.array([1.2, -0.8, 0.6, 0.0])
y = (rng.random(n) < sig(X @ w_true - 1.0)).astype(int)                     # about 30% positive
# T[i][j] = P(noisy label = j | true class = i): positives are lost far more often than negatives are invented
T = np.array([[0.96, 0.04], [0.30, 0.70]])
noisy = np.where(rng.random(n) < T[y, 1], 1, 0)
print("true positive rate:", round(float(y.mean()), 3), " noisy positive rate:", round(float(noisy.mean()), 3))

# 1) estimate T from 500 trusted labels (a random 500 rows that also have a crowd label)
trusted = rng.choice(n, 500, replace=False)
yt, nt = y[trusted], noisy[trusted]
That = np.array([[np.mean(nt[yt == i] == j) for j in (0, 1)] for i in (0, 1)])
print("trusted rows: positives", int((yt == 1).sum()), " negatives", int((yt == 0).sum()))
print("estimated T:\n", np.round(That, 3), "\ntrue T:\n", T)
# how stable? re-draw 500 trusted rows 300 times
est = []
for _ in range(300):
    idx = rng.choice(n, 500, replace=False); a, b = y[idx], noisy[idx]
    est.append([b[a == 1].__eq__(0).mean(), b[a == 0].__eq__(1).mean()])
est = np.array(est)
print("sd of P(noisy=0|true=1):", round(float(est[:, 0].std()), 3), "  sd of P(noisy=1|true=0):", round(float(est[:, 1].std()), 3))
assert est[:, 0].std() > 2 * est[:, 1].std()               # the rare class is the poorly estimated one

# 2) train three logistic models: naive on noisy, forward-corrected loss with estimated T, and trusted-only
F = np.c_[X, np.ones(n)]
tr = np.arange(n) < 20_000; te = ~tr
def nll_plain(w, F, t): p = np.clip(sig(F @ w), 1e-9, 1 - 1e-9); return -np.mean(t * np.log(p) + (1 - t) * np.log(1 - p))
def nll_forward(w, F, t, Tm):
    p1 = sig(F @ w)
    q1 = np.clip(p1 * Tm[1, 1] + (1 - p1) * Tm[0, 1], 1e-9, 1 - 1e-9)    # P(noisy label = 1 | x) = sum_i P(y=i|x) T[i,1]
    return -np.mean(t * np.log(q1) + (1 - t) * np.log(1 - q1))
def run(fun, *args):
    return minimize(fun, np.zeros(F.shape[1]), args=args, method="L-BFGS-B").x
w_naive = run(nll_plain, F[tr], noisy[tr])
w_fwd = run(nll_forward, F[tr], noisy[tr], That)
w_fwd_true = run(nll_forward, F[tr], noisy[tr], T)
tt = np.intersect1d(trusted, np.where(tr)[0])
w_trust = run(nll_plain, F[trusted], y[trusted])                              # 500 clean rows only
def report(name, w):
    s = F[te] @ w
    print(f"{name:34s} AUC {auc(y[te], s):.4f}   mean predicted P(y=1) {sig(s).mean():.3f} (truth {y[te].mean():.3f})")
    return sig(s).mean()
m_n = report("naive on noisy labels", w_naive)
m_f = report("forward-corrected, T estimated", w_fwd)
m_t = report("forward-corrected, T true", w_fwd_true)
m_c = report("trusted 500 only", w_trust)
assert abs(m_f - y[te].mean()) < abs(m_n - y[te].mean())

# 3) where it breaks: (a) instance-dependent noise (hard positives lost more), (b) near-singular T
hard = X[:, 0] < 0
noisy_id = np.where(rng.random(n) < np.where(y == 1, np.where(hard, 0.55, 0.12), 0.04), 1 - y, y)
rate_hard = (noisy_id[y == 1][hard[y == 1]] == 0).mean(); rate_easy = (noisy_id[y == 1][~hard[y == 1]] == 0).mean()
print("instance-dependent noise: positives lost, hard", round(float(rate_hard), 3), " easy", round(float(rate_easy), 3))
T_glob = np.array([[0.96, 0.04], [0.30, 0.70]])
w_id = run(nll_forward, F[tr], noisy_id[tr], T_glob)
w_id_n = run(nll_plain, F[tr], noisy_id[tr])
print("instance-dependent: AUC naive", round(float(auc(y[te], F[te] @ w_id_n)), 4), " corrected with one global T", round(float(auc(y[te], F[te] @ w_id)), 4))
print("determinant of T (0 means labels carry no information):", round(float(np.linalg.det(T)), 3), " if T=[[.8,.2],[.55,.45]]:", round(float(np.linalg.det(np.array([[.8, .2], [.55, .45]]))), 3))
