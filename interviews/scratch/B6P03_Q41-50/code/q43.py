# Q43: a classifier trained on LLM labels, judged by the same LLM. Illustrative simulation.
import numpy as np
rng = np.random.default_rng(43)

def make(n):
    seg = rng.choice(3, n, p=[0.70, 0.20, 0.10])         # 0 English, 1 code-mixed, 2 other
    xa = rng.normal(size=n)                               # the real signal
    y = (xa > 0).astype(int)                       # human truth
    return seg, xa, y

def llm_label(seg, xa, y):
    # LLM is mostly right, but has a systematic blind spot: in segment 1, when xa is in (0, 1.2) it says 0
    out = y.copy()
    blind = (seg == 1) & (xa > 0) & (xa < 1.2)
    out[blind] = 0
    # plus 3% random errors everywhere
    flip = rng.random(len(y)) < 0.03
    out[flip] = 1 - out[flip]
    return out

def feats(seg, xa):
    s1 = (seg == 1).astype(float)
    return np.column_stack([np.ones(len(xa)), xa, s1, s1 * xa, s1 * (xa > 0), s1 * (xa > 1.2)])

def fit_logit(X, t, iters=30):
    w = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w))
        g = X.T @ (p - t) + 1e-6 * w
        H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(len(w))
        w -= np.linalg.solve(H, g)
    return w

seg, xa, y = make(60_000); lab = llm_label(seg, xa, y)
w = fit_logit(feats(seg, xa), lab)

seg_t, xa_t, y_t = make(20_000); lab_t = llm_label(seg_t, xa_t, y_t)   # test rows with LLM labels
pred = (feats(seg_t, xa_t) @ w > 0).astype(int)

agree = (pred == lab_t).mean()
acc_true = (pred == y_t).mean()
llm_acc = (lab_t == y_t).mean()
print(f"classifier vs LLM judge agreement : {agree:.3f}")
print(f"classifier vs human truth accuracy: {acc_true:.3f}")
print(f"LLM labels vs human truth accuracy: {llm_acc:.3f}")
for s, nm in enumerate(["English", "code-mixed", "other"]):
    m = seg_t == s
    print(f"  {nm:10s} share {m.mean():.2f}  agree-with-LLM {(pred[m]==lab_t[m]).mean():.3f}  "
          f"acc-vs-truth {(pred[m]==y_t[m]).mean():.3f}  LLM-label acc {(lab_t[m]==y_t[m]).mean():.3f}")
assert agree > 0.95 and acc_true < agree - 0.02

# independent set: stratified human audit, 400 rows per segment, then reweight to population shares
n_per = 400
share = np.array([0.70, 0.20, 0.10])
est = []; 
for s in range(3):
    idx = np.where(seg_t == s)[0]; pick = rng.choice(idx, n_per, replace=False)
    acc = (lab_t[pick] == y_t[pick]).mean()
    half = 1.96 * np.sqrt(acc * (1 - acc) / n_per)
    est.append(acc); print(f"  audit seg {s}: LLM label accuracy {acc:.3f} +/- {half:.3f}")
overall = float(np.dot(share, est))
print(f"population-weighted LLM label accuracy = {overall:.3f}")
assert abs(overall - llm_acc) < 0.02
print(f"worst-case half width at n=400, p=0.5: {1.96*np.sqrt(0.25/400):.3f}")
assert round(1.96*np.sqrt(0.25/400), 3) == 0.049
