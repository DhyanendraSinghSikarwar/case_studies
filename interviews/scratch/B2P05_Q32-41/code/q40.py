# Standalone, numpy only. SYNTHETIC: a linear "reward model" learned from a judge whose quality drops with task difficulty.
import numpy as np
rng = np.random.default_rng(0)
D = 10                                           # features 0..8 = real quality features, feature 9 = "style/length" (looks good, is not)
w_true = np.concatenate([rng.normal(0, 1, 9), [0.0]]); w_true /= np.linalg.norm(w_true)

def judge_labels(dx, level, systematic):         # dx = feature difference of a pair; the judge perceives truth + noise (+ style bias when hard)
    noise = [0.3, 1.0, 2.0, 4.0][level]
    seen = dx @ w_true + rng.normal(0, noise, len(dx))
    if systematic: seen += [0.0, 0.3, 1.0, 2.0][level] * dx[:, 9]       # hard task: judge leans on style because it cannot check substance
    return seen > 0

def fit_rm(dx, y, steps=1500, lr=0.5):           # logistic regression on pair differences = Bradley-Terry reward model
    w = np.zeros(D)
    for _ in range(steps):
        p = 1 / (1 + np.exp(-dx @ w)); w -= lr * dx.T @ (p - y) / len(y)
    return w

test = rng.normal(0, 1, (20000, D)); test_y = test @ w_true > 0      # clean truth, no noise
cands = rng.normal(0, 1, (4000, 8, D))                                 # best-of-8 probe: pick by RM, measure TRUE reward of pick
def evaluate(w): 
    pick = (cands @ w).argmax(1); return ((test @ w > 0) == test_y).mean(), (cands[np.arange(4000), pick] @ w_true).mean(), w[9] / np.linalg.norm(w)
print("level = task difficulty (judge noise sd 0.3 / 1 / 2 / 4); 3000 labelled pairs each; true best-of-8 reward of a random pick is 0.00")
print(f"{'':32s}{'RM acc vs truth':>16s}{'true BoN-8 reward':>19s}{'weight on style':>17s}")
for systematic in (False, True):
    for level in range(4):
        dx = rng.normal(0, 1, (3000, D)); w = fit_rm(dx, judge_labels(dx, level, systematic))
        a, b, s = evaluate(w)
        print(f"{'random noise only' if not systematic else 'noise + style bias':18s} level {level}      {a:16.3f}{b:19.3f}{s:17.2f}")
w = fit_rm(dx := rng.normal(0, 1, (30000, D)), judge_labels(dx, 3, False)); a, b, s = evaluate(w)
print(f"hard task, random noise only, 10x more labels: acc {a:.3f}, BoN-8 reward {b:.3f}, style weight {s:.2f}")
w = fit_rm(dx := rng.normal(0, 1, (30000, D)), judge_labels(dx, 3, True)); a, b, s = evaluate(w)
print(f"hard task, noise + style bias, 10x more labels: acc {a:.3f}, BoN-8 reward {b:.3f}, style weight {s:.2f}")
