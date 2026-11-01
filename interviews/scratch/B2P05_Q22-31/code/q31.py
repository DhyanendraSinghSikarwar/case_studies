import numpy as np
rng = np.random.default_rng(7)
def kappa(a, b):
    a, b = np.asarray(a), np.asarray(b); labs = np.unique(np.r_[a, b])
    po = np.mean(a == b)
    pe = sum(np.mean(a == l) * np.mean(b == l) for l in labs)
    return (po - pe) / (1 - pe)
# hand-computed: 10 items, A: 7 "A-wins" 3 "B-wins"; B: 6 and 4; agree on 5 A and 2 B -> po=0.7
# pe = 0.7*0.6 + 0.3*0.4 = 0.54 ; kappa = (0.7-0.54)/(1-0.54) = 0.3478
a = ["A"]*7 + ["B"]*3
b = ["A"]*5 + ["B"]*2 + ["A"]*1 + ["B"]*2
print("kappa:", round(kappa(a, b), 4), "(hand: 0.3478)")
# SYNTHETIC: noise caps reward-model accuracy. Linear RM on 2-D features, Bradley-Terry-style pairs.
d, n = 10, 4000
w_true = rng.standard_normal(d)
def pairs(n):
    x = rng.standard_normal((n, d))                  # feature difference chosen - rejected
    clean = (x @ w_true > 0).astype(float)           # true preference direction
    return x, clean
xtr, ytr_clean = pairs(n); xte, yte_clean = pairs(20000)
def fit(x, y, steps=300, lr=0.5):
    w = np.zeros(d)
    for _ in range(steps):
        p = 1/(1+np.exp(-x@w)); w -= lr * x.T @ (p - y) / len(y)
    return w
print("train flip rate | acc vs TRUE labels | acc vs NOISY test labels")
for flip in [0.0, 0.1, 0.2, 0.3, 0.4]:
    f = rng.random(n) < flip
    ytr = np.where(f, 1 - ytr_clean, ytr_clean)
    w = fit(xtr, ytr)
    pred = (xte @ w > 0)
    noisy_te = np.where(rng.random(len(yte_clean)) < flip, 1 - yte_clean, yte_clean)
    print(f"   {flip:.1f}        |      {np.mean(pred==yte_clean):.3f}         |   {np.mean(pred==noisy_te):.3f}")
# majority vote of 3 annotators each wrong 20% of the time (independent)
e = 0.2; maj = 3*e**2*(1-e) + e**3
print("3-vote majority error:", round(maj, 3), "vs single", e)
# label-smoothed BT/logistic loss: target eps instead of 0 for flipped-risk labels
def smoothed_loss(margin, eps):   # margin = r_chosen - r_rejected
    p = 1/(1+np.exp(-margin)); return -((1-eps)*np.log(p) + eps*np.log(1-p))
print("loss at margin 5 (confident):  eps=0:", round(float(smoothed_loss(5,0)),4), " eps=0.1:", round(float(smoothed_loss(5,0.1)),4))
print("loss at margin 0.5:            eps=0:", round(float(smoothed_loss(0.5,0)),4), " eps=0.1:", round(float(smoothed_loss(0.5,0.1)),4))
