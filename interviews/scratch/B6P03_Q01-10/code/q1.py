# Q1 fraud 0.1%: accuracy cannot tell a good model from a bad one (illustrative numbers)
import numpy as np
from scipy.stats import beta

N, P = 2_000_000, 2_000
Nn = N - P
assert P / N == 0.001
base_acc = Nn / N
print(f"flag-nothing accuracy: {base_acc:.4f}")
assert abs(base_acc - 0.999) < 1e-12

def report(name, tp, fp):
    fn = P - tp; tn = Nn - fp
    assert tp + fp + fn + tn == N
    acc = (tp + tn) / N
    prec = tp / (tp + fp) if tp + fp else float('nan')
    rec = tp / P
    print(f"{name:34s} errors={fp+fn:5d} acc={acc:.4f} precision={prec:.3f} recall={rec:.3f}")
    return acc, prec, rec

# Two very different models, both with accuracy 99.8% (4,000 errors out of 2,000,000)
accA, precA, recA = report("A: catches 1,500, 3,500 false alarms", 1500, 3500)
accB, precB, recB = report("B: catches 0, 2,000 false alarms", 0, 2000)
assert abs(accA - 0.998) < 1e-9 and abs(accB - 0.998) < 1e-9
assert recB == 0 and recA == 0.75 and abs(precA - 0.3) < 1e-9

# PR-AUC baseline for a no-skill model equals the prevalence
print(f"no-skill precision at any recall = {P/N:.4f}; model A is {precA/(P/N):.0f}x better than random flagging")
assert round(precA / (P / N)) == 300

# How many frauds does a random test slice hold, and how wide is the recall interval?
for frac in (0.20, 0.05):
    pos = int(P * frac)
    lo, hi = beta.ppf(0.025, int(0.75*pos), pos - int(0.75*pos) + 1), beta.ppf(0.975, int(0.75*pos) + 1, pos - int(0.75*pos))
    print(f"test slice {frac:.0%}: {pos} frauds, recall 0.75 has 95% interval [{lo:.3f}, {hi:.3f}]")
    if frac == 0.20: assert (hi - lo) < 0.10 and pos == 400
    else: assert (hi - lo) > 0.15 and pos == 100
