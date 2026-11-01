# Q5 churn: 100,000 customers, 4% churn, capacity 2,000 calls (illustrative simulation)
import numpy as np

rng = np.random.default_rng(21)
N, CAP = 100_000, 2_000
z = rng.normal(size=N)
def sig(x): return 1 / (1 + np.exp(-x))
lo, hi = -8.0, 0.0
for _ in range(60):                         # find intercept so that mean probability = 4%
    mid = (lo + hi) / 2
    if sig(mid + 1.6 * z).mean() > 0.04: hi = mid
    else: lo = mid
p = sig(lo + 1.6 * z)                       # treat p as a calibrated model score
y = (rng.random(N) < p).astype(int)
print(f"churners={y.sum()} ({y.mean():.2%}); mean score={p.mean():.4f}")
assert abs(y.sum() - 4000) < 200

def stats(flag):
    tp = (flag & (y == 1)).sum(); k = flag.sum()
    prec = tp / k if k else float('nan'); rec = tp / y.sum()
    f1 = 2 * prec * rec / (prec + rec) if tp else 0.0
    return k, tp, prec, rec, f1

# 1) default 0.5 threshold
k, tp, pr, rc, f1 = stats(p >= 0.5)
print(f"threshold 0.5     : flagged={k:6d} TP={tp:4d} precision={pr:.3f} recall={rc:.3f} F1={f1:.3f}")
assert k < CAP / 4                                   # leaves most of the capacity unused

# 2) the F1-optimal threshold ignores the 2,000 limit
ths = np.quantile(p, np.linspace(0.5, 0.999, 400))
best = max(ths, key=lambda t: stats(p >= t)[4])
k, tp, pr, rc, f1 = stats(p >= best)
print(f"F1-optimal thr {best:.3f}: flagged={k:6d} TP={tp:4d} precision={pr:.3f} recall={rc:.3f} F1={f1:.3f}")
assert k > CAP                                       # asks for more calls than the team can make

# 3) capacity rule: call the top 2,000 by score
top = np.zeros(N, bool); top[np.argsort(-p)[:CAP]] = True
k, tp, pr, rc, f1 = stats(top)
exp_tp = p[top].sum()                                # expected hits from calibrated scores
print(f"top {CAP}          : flagged={k:6d} TP={tp:4d} precision={pr:.3f} recall={rc:.3f}  expected TP from scores={exp_tp:.0f}")
print(f"max possible recall at 2,000 calls = {CAP}/{y.sum()} = {CAP/y.sum():.3f}; random 2,000 would catch {CAP*0.04:.0f}; lift={pr/0.04:.1f}")
assert k == CAP and abs(tp - exp_tp) < 60 and pr / 0.04 > 5
assert rc <= CAP / y.sum() + 1e-12

# 4) value rule with a capacity cap: contact if p*save*value > cost  (invented: save 20%, value 100, call cost 3)
save, value, cost = 0.20, 100.0, 3.0
cut = cost / (save * value)
worth = p > cut
n_worth = int(worth.sum()); n_call = min(CAP, n_worth)
order = np.argsort(-p)[:n_call]
profit = (p[order] * save * value - cost).sum()
print(f"break-even score {cut:.2f}: {n_worth} customers above it; we call {n_call}; expected profit={profit:,.0f}")
assert n_call == CAP and profit > 0
# the lowest score among the 2,000 called, i.e. the threshold the capacity implies
print(f"implied threshold of the top-{CAP} rule: {p[order].min():.3f}")
