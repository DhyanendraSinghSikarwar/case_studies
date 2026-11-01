# TOY: model extraction. Victim = logistic model on 10 numeric features (synthetic). Attacker fits a surrogate from query answers.
import numpy as np
rng = np.random.default_rng(5)
d = 10; w_true = rng.normal(size=d); b_true = 0.3
victim_p = lambda X: 1 / (1 + np.exp(-(X @ w_true + b_true)))
Xtest = rng.normal(size=(5000, d)); ytest = victim_p(Xtest) > 0.5
def fit_logreg(X, y, steps=3000, lr=0.5):                  # attacker trains on hard labels or soft targets
    w = np.zeros(X.shape[1]); b = 0.0
    for _ in range(steps):
        p = 1 / (1 + np.exp(-(X @ w + b))); g = p - y
        w -= lr * (X.T @ g) / len(y); b -= lr * g.mean()
    return w, b
def agree(w, b): return float(np.mean(((Xtest @ w + b) > 0) == ytest))
print("queries | label-only agreement | full-probability agreement | rounded-to-1-decimal prob agreement")
for n in [20, 50, 200, 1000]:
    X = rng.normal(size=(n, d)); p = victim_p(X)
    a_lab = agree(*fit_logreg(X, (p > 0.5).astype(float)))
    # with probabilities the attacker can regress on the logit directly (closed-form least squares)
    def logit_fit(pp):
        pp = np.clip(pp, 1e-3, 1 - 1e-3); A = np.c_[X, np.ones(n)]; sol = np.linalg.lstsq(A, np.log(pp / (1 - pp)), rcond=None)[0]; return sol[:-1], sol[-1]
    a_prob = agree(*logit_fit(p)); a_round = agree(*logit_fit(np.round(p, 1)))
    print(f"{n:6d}  | {a_lab:.3f} | {a_prob:.3f} | {a_round:.3f}")
# detection toy: per-client features over a window of 1000 requests; scrapers = high rate, almost no repeated prompts, systematic coverage
def window(kind, r):
    if kind == "normal":  prompts = r.integers(0, 40, 60)            # few requests, repeats common
    else:                 prompts = np.arange(1000)                    # 1000 distinct prompts, one pass
    return len(prompts), len(set(prompts.tolist())) / len(prompts)
r = np.random.default_rng(1)
for kind in ["normal", "scraper"]:
    n, uniq = window(kind, r); print(f"{kind:8} requests/window={n:4d} distinct-ratio={uniq:.2f} flag={n > 300 and uniq > 0.9}")
print("evasion: a scraper using 20 accounts at 50 requests each has rate", 50, "and is not flagged by this per-client rule.")
