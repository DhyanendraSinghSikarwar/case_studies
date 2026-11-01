# Validate a MOCK judge against SYNTHETIC human labels: agreement, kappa, TPR, TNR,
# dev/test split, and a kappa check against an independent pair-counting computation.
import random, itertools
random.seed(5)

def make(n, p_pass=0.85, tpr=0.9, tnr=0.7):   # ASSUMED prevalence and judge error rates
    rows = []
    for _ in range(n):
        h = random.random() < p_pass
        j = (random.random() < tpr) if h else (random.random() > tnr)
        rows.append((h, j))
    return rows
data = make(400)
random.shuffle(data)
train, dev, test = data[:60], data[60:230], data[230:]     # 15% / 42.5% / 42.5%
print("split sizes:", len(train), len(dev), len(test), "(train = few-shot/prompt examples)")

def stats(rows):
    tp = sum(h and j for h, j in rows); tn = sum((not h) and (not j) for h, j in rows)
    fp = sum((not h) and j for h, j in rows); fn = sum(h and (not j) for h, j in rows)
    n = len(rows); po = (tp + tn) / n
    pe = ((tp + fn) * (tp + fp) + (fp + tn) * (fn + tn)) / n**2
    return dict(n=n, agree=po, kappa=(po - pe) / (1 - pe), tpr=tp / (tp + fn), tnr=tn / (tn + fp))

def kappa_pairs(rows):                 # independent check: chance agreement by explicit enumeration
    H = [h for h, _ in rows]; J = [j for _, j in rows]; n = len(rows)
    po = sum(h == j for h, j in rows) / n
    pe = sum(a == b for a, b in itertools.product(H, J)) / n**2   # P(random human label == random judge label)
    return (po - pe) / (1 - pe)

for name, rows in (("dev", dev), ("test", test)):
    s = stats(rows)
    print(f"{name}: n={s['n']} agree={s['agree']:.2f} kappa={s['kappa']:.2f} TPR={s['tpr']:.2f} TNR={s['tnr']:.2f}")
assert abs(stats(test)["kappa"] - kappa_pairs(test)) < 1e-12
print("kappa matches independent computation: OK")

# Raw agreement hides the weak class: a judge that always says PASS on this data
always = [(h, True) for h, _ in test]
s = stats(always); print(f"always-PASS judge on test: agree={s['agree']:.2f} kappa={s['kappa']:.2f} TNR={s['tnr']:.2f}")

# Correct the judge's observed pass rate with TPR/TNR from DEV, evaluate on TEST (Rogan-Gladen)
d = stats(dev); print("human-negative cases in dev:", sum(not h for h, _ in dev), "| in test:", sum(not h for h, _ in test))
obs = sum(j for _, j in test) / len(test); true = sum(h for h, _ in test) / len(test)
corr = (obs + d["tnr"] - 1) / (d["tpr"] + d["tnr"] - 1)
print(f"test pass rate: human {true:.3f}, judge raw {obs:.3f}, judge corrected {corr:.3f}")
