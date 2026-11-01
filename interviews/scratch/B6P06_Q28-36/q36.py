# Illustrative: 100,000 cases, 1% base rate.
N, base = 100_000, 0.01
pos = int(N * base); neg = N - pos
assert pos == 1000 and neg == 99_000
def report(name, tp, fp):
    fn, tn = pos - tp, neg - fp
    acc = (tp + tn) / N
    rec = tp / pos
    prec = tp / (tp + fp) if tp + fp else float("nan")
    print(f"{name:22} TP {tp:4} FP {fp:5} FN {fn:4} acc {acc:.3f} recall {rec:.2f} precision {prec:.2f}")
    return acc, rec, prec
a0, r0, _ = report("predict none", 0, 0)
a1, r1, p1 = report("model (700 TP, 700 FP)", 700, 700)
assert a0 == 0.99 and r0 == 0 and a1 == 0.99 and r1 == 0.70 and p1 == 0.50
# lift over base rate
print("precision lift over base rate:", p1 / base)
assert round(p1 / base) == 50
# Cost-based view: review costs 5 per flag, a caught event saves 200, a missed one costs 200 (illustrative)
def value(tp, fp, review=5, save=200):
    return tp * save - (tp + fp) * review
print("value none:", value(0, 0), " value model:", value(700, 700), " 'perfect 99% acc' that flags 100 only:", value(100, 0))
assert value(700, 700) == 700 * 200 - 1400 * 5 == 133_000
