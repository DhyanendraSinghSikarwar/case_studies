# TOY: evaluating a guardrail in shadow mode. Scores come from a mock detector with SYNTHETIC score distributions.
import math, random
def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 1.0)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)
# closed-form check: 0 successes in 10 -> upper bound z^2/(n+z^2)
assert abs(wilson(0, 10)[1] - 1.96**2 / (10 + 1.96**2)) < 1e-12
# brute-force check: Wilson bounds are the p where the score-test z equals +-1.96; bisect and compare
def bisect_bound(k, n, upper):
    lo, hi = (k / n, 1.0) if upper else (0.0, k / n)
    f = lambda p: (k / n - p) / math.sqrt(p * (1 - p) / n)
    for _ in range(100):
        mid = (lo + hi) / 2
        if upper: lo, hi = (mid, hi) if f(mid) > -1.96 else (lo, mid)
        else: lo, hi = (lo, mid) if f(mid) < 1.96 else (mid, hi)
    return mid
w = wilson(7, 40); assert abs(w[0] - bisect_bound(7, 40, False)) < 1e-6 and abs(w[1] - bisect_bound(7, 40, True)) < 1e-6
print("wilson checks passed (closed form and bisection)")

rng = random.Random(11)
def clip(x): return max(0.0, min(1.0, x))
# synthetic traffic: label 1 = attack. score ~ noisy; "new family" attacks score lower (attackers adapted)
benign = [(clip(rng.gauss(0.25, 0.15)), 0, "benign") for _ in range(2000)]
old_att = [(clip(rng.gauss(0.75, 0.15)), 1, "known-family") for _ in range(100)]
new_att = [(clip(rng.gauss(0.50, 0.15)), 1, "new-family") for _ in range(100)]
def metrics(rows, thr):
    tp = sum(1 for s, y, _ in rows if y and s >= thr); fn = sum(1 for s, y, _ in rows if y and s < thr)
    fp = sum(1 for s, y, _ in rows if not y and s >= thr); tn = sum(1 for s, y, _ in rows if not y and s < thr)
    return tp, fn, fp, tn
print("threshold | blocked benign (FP rate, 95% Wilson) | recall known | recall new-family | benign blocked per 10k requests")
for thr in [0.4, 0.5, 0.6, 0.7]:
    tp, fn, fp, tn = metrics(benign + old_att, thr); lo, hi = wilson(fp, fp + tn)
    r_old = metrics(old_att, thr)[0] / len(old_att); r_new = metrics(new_att, thr)[0] / len(new_att)
    print(f"  {thr:.1f}    | {fp:4d}/{fp+tn} = {fp/(fp+tn):.3f} [{lo:.3f},{hi:.3f}] | {r_old:.2f} | {r_new:.2f} | {fp/(fp+tn)*1e4:7.0f}")
# cost-weighted choice: assumed costs (SYNTHETIC): a blocked legit user costs 1 unit, a missed attack costs 50 units
COST_FP, COST_FN = 1, 50
rows = benign + old_att + new_att
best = min((COST_FP * metrics(rows, t / 100)[2] + COST_FN * metrics(rows, t / 100)[1], t / 100) for t in range(10, 91, 5))
print("threshold minimising assumed cost (FP=1, FN=50) on this mixed set:", best[1], "cost", best[0])
# shadow mode: log would-block decisions, no enforcement; review a sample of would-blocks to estimate precision of the block
thr = 0.6; would_block = [r for r in benign + old_att if r[0] >= thr]
sample = rng.sample(would_block, min(30, len(would_block)))
true_att = sum(y for _, y, _ in sample)
print(f"shadow mode at thr {thr}: {len(would_block)} would-blocks; human review of {len(sample)} sampled -> {true_att} real attacks (precision estimate {true_att/len(sample):.2f})")
tp, fn, fp, tn = metrics(benign + old_att, thr); print(f"  true precision on the full labelled set: {tp/(tp+fp):.2f} (shadow sample is a noisy estimate)")
# drift: weekly recall on a stream where attackers shift from known to new families
print("week | share new-family | recall at thr 0.6")
for wk, share in enumerate([0.0, 0.2, 0.5, 0.8]):
    att = [rng.choice(old_att) if rng.random() > share else rng.choice(new_att) for _ in range(100)]
    print(f"  {wk}  | {share:.1f} | {metrics(att, 0.6)[0] / 100:.2f}")
