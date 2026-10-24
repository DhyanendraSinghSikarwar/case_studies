# Building a judge you can trust, on SYNTHETIC data with MOCK judges: calibration, bias tests, ensemble, drift.
import random
rng = random.Random(8)
def make_items(n):                                    # human label = ground truth (1 = good); answer length is independent of quality
    return [{"good": int(rng.random() < 0.6), "words": rng.choice([40, 80, 160])} for _ in range(n)]
def judge(item, tpr=0.9, tnr=0.8, len_bias=0.0, pos_bias=0.0, first=True):
    p = tpr if item["good"] else 1 - tnr
    p += len_bias * (item["words"] - 80) / 80 + (pos_bias if first else -pos_bias)
    return int(rng.random() < min(max(p, 0), 1))
def metrics(items, preds):
    tp = sum(1 for i, p in zip(items, preds) if i["good"] and p); fn = sum(1 for i, p in zip(items, preds) if i["good"] and not p)
    tn = sum(1 for i, p in zip(items, preds) if not i["good"] and not p); fp = sum(1 for i, p in zip(items, preds) if not i["good"] and p)
    n = len(items); po = (tp + tn) / n
    pe = ((tp + fn) / n) * ((tp + fp) / n) + ((tn + fp) / n) * ((tn + fn) / n)
    return tp / (tp + fn), tn / (tn + fp), (po - pe) / (1 - pe)
calib = make_items(300); dev, test = calib[:100], calib[100:]            # dev: tune the rubric; test: report once
J1 = lambda it: judge(it, len_bias=0.12, pos_bias=0.0)                  # judge A: has a length bias (assumed)
tpr, tnr, k = metrics(test, [J1(i) for i in test]); print(f"judge A on held-out calibration test (n={len(test)}): TPR {tpr:.3f} TNR {tnr:.3f} kappa {k:.3f}")
# bias test 1: pad the same answers with fluff (+80 words), human label unchanged
padded = [dict(i, words=i["words"] + 80) for i in test]
print("length probe: pass rate on original", round(sum(J1(i) for i in test) / len(test), 3), "-> padded", round(sum(J1(i) for i in padded) / len(test), 3), "(should not move)")
# bias test 2: position swap for a pairwise judge (mock: pos_bias 0.1 toward slot A)
flips = sum(judge(i, pos_bias=0.1, first=True) != judge(i, pos_bias=0.1, first=False) for i in test) / len(test)
print("position probe: verdict flips when order is swapped:", round(flips, 3))
# ensemble of 3 judges with independent errors (different 'model families', assumed), majority vote
J2 = lambda it: judge(it, len_bias=0.0); J3 = lambda it: judge(it, tpr=0.88, tnr=0.85)
def ens(it): return int(J1(it) + J2(it) + J3(it) >= 2)
for name, f in [("judge A", J1), ("judge B", J2), ("judge C", J3), ("majority of 3", ens)]:
    t, n_, kk = metrics(test, [f(i) for i in test]); print(f"  {name:14} TPR {t:.3f} TNR {n_:.3f} kappa {kk:.3f}")
# drift: weekly anchor set of 60 human-labelled items; the judge backend changes at week 6 (assumed: TNR falls 0.8 -> 0.55)
print("\nweek  kappa on 60 anchor items   alert (kappa < 0.45)")
for wk in range(1, 11):
    anchor = make_items(60); tnr_w = 0.8 if wk < 6 else 0.55
    _, _, kw = metrics(anchor, [judge(i, tnr=tnr_w) for i in anchor]); print(f"{wk:4d}  {kw:6.3f}                    {'ALERT' if kw < 0.45 else '-'}")
