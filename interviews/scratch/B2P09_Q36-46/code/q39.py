# Cohen's kappa + TPR/TNR for an LLM judge vs a human labeller. 1 = "good/pass", 0 = "bad/fail". Human = reference.
import random
def confusion(h, j):
    tp = sum(1 for x, y in zip(h, j) if x == 1 and y == 1); tn = sum(1 for x, y in zip(h, j) if x == 0 and y == 0)
    fp = sum(1 for x, y in zip(h, j) if x == 0 and y == 1); fn = sum(1 for x, y in zip(h, j) if x == 1 and y == 0)
    return tp, tn, fp, fn
def kappa(h, j):
    n = len(h); po = sum(x == y for x, y in zip(h, j)) / n
    pe = sum((sum(1 for x in h if x == c) / n) * (sum(1 for y in j if y == c) / n) for c in (0, 1))
    return (po - pe) / (1 - pe) if pe < 1 else float('nan')
def report(name, h, j):
    tp, tn, fp, fn = confusion(h, j)
    print(f"{name:34} n={len(h):3d} acc={(tp+tn)/len(h):.3f} TPR={tp/(tp+fn):.3f} TNR={tn/(tn+fp):.3f} kappa={kappa(h, j):.3f}")
# 1) hand-check: counts tp=15 tn=20 fp=5 fn=10 -> po=0.7, pe=0.5, kappa=0.4
h = [1]*15 + [0]*20 + [0]*5 + [1]*10; j = [1]*15 + [0]*20 + [1]*5 + [0]*10
report("hand-check (expect kappa 0.400)", h, j)
# 2) perfect and chance-level
report("identical labels", h, h)
random.seed(4)
rnd = [random.randint(0, 1) for _ in h]
report("random judge", h, rnd)
# 3) imbalanced data: 90% of outputs are good. A lazy judge that always says "pass" looks accurate.
random.seed(9)
hh = [1 if random.random() < 0.9 else 0 for _ in range(200)]
report("always-pass judge (90% good)", hh, [1]*200)
# a real-ish judge: catches 60% of bad, 95% of good
jj = [(1 if random.random() < 0.95 else 0) if x == 1 else (1 if random.random() < 0.4 else 0) for x in hh]
report("judge: TPR~.95, TNR~.60", hh, jj)
# 4) uncertainty: bootstrap CI for kappa on the 200 items
r = random.Random(1); ks = []
for _ in range(2000):
    idx = [r.randrange(200) for _ in range(200)]
    hb = [hh[i] for i in idx]; jb = [jj[i] for i in idx]
    k = kappa(hb, jb)
    if k == k: ks.append(k)
ks.sort(); print(f"bootstrap 95% CI for kappa of the realistic judge: [{ks[int(.025*len(ks))]:.3f}, {ks[int(.975*len(ks))-1]:.3f}]  (only {sum(1 for x in hh if x==0)} bad items drive TNR)")
