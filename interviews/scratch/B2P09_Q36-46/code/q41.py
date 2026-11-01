# Six bugs in an LLM-written eval script, each shown with its effect on MOCK data (synthetic), then fixed.
import math, random
rng = random.Random(0)
print("1) few-shot examples drawn from the test set")
test = list(range(200))                                 # 200 test questions
def model_correct(q, shots): return True if q in shots else rng.random() < 0.5   # mock model copies any answer it has seen in the prompt
shots_bad = rng.sample(test, 40)                        # BUG: shots come from the test set
acc_bad = sum(model_correct(q, shots_bad) for q in test) / 200
dev = list(range(1000, 1100)); shots_ok = rng.sample(dev, 40)       # FIX: shots from a separate dev pool, assert disjoint
assert not set(shots_ok) & set(test)
acc_ok = sum(model_correct(q, shots_ok) for q in test) / 200
print(f"   buggy accuracy {acc_bad:.3f}   fixed {acc_ok:.3f}   (mock model truly answers ~50% of unseen questions)")
print("2) naive pass@k: 1-(1-c/n)^k vs unbiased 1-C(n-c,k)/C(n,k)")
n, k, p = 10, 5, 0.3                                    # per-sample success probability p (assumed), n samples, report pass@5
def unbiased(n, c, k): return 1.0 if n - c < k else 1 - math.comb(n - c, k) / math.comb(n, k)
def naive(n, c, k): return 1 - (1 - c / n) ** k
pmf = [math.comb(n, c) * p ** c * (1 - p) ** (n - c) for c in range(n + 1)]
E_naive = sum(w * naive(n, c, k) for c, w in enumerate(pmf)); E_unb = sum(w * unbiased(n, c, k) for c, w in enumerate(pmf))
print(f"   true pass@{k} = {1-(1-p)**k:.4f}   E[naive] = {E_naive:.4f}   E[unbiased] = {E_unb:.4f}")
print("3) no position swap in a pairwise judge (mock judge prefers slot A 65% of the time when quality is equal)")
def judge(first, second): return "A" if rng.random() < 0.65 else "B"   # equal-quality systems: pure position bias
one_order = sum(judge("X", "Y") == "A" for _ in range(1000)) / 1000      # BUG: X always in slot A
both = sum((judge("X", "Y") == "A") + (judge("Y", "X") == "B") for _ in range(500)) / 1000   # FIX: half each way
print(f"   X win rate, X always first {one_order:.3f}   with order swap {both:.3f}   (truth 0.500, 1000 judgements each)")
print("4) mean score with no interval (20 items, scores 1-5, synthetic)")
s1 = [rng.choice([3, 4, 4, 5, 2]) for _ in range(20)]; s2 = [min(5, max(1, x + rng.choice([-1, 0, 0, 1]))) for x in s1]
d = [a - b for a, b in zip(s1, s2)]; bs = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(5000))
print(f"   mean A {sum(s1)/20:.2f} vs B {sum(s2)/20:.2f}; paired diff {sum(d)/20:+.2f}, 95% CI [{bs[125]:+.2f}, {bs[4874]:+.2f}] -> do not claim a win if it spans 0")
print("5) same model generates and judges (mock judge adds +0.6 to its own family's outputs)")
true_q = [rng.gauss(3.5, 0.6) for _ in range(200)]      # both systems have identical true quality
own = sum(q + 0.6 + rng.gauss(0, .3) for q in true_q) / 200; other = sum(q + rng.gauss(0, .3) for q in true_q) / 200
print(f"   judge scores own-family system {own:.2f} vs equal-quality other system {other:.2f}; FIX: judge from a different family, or check by swapping judges")
print("6) temperature > 0 and a single run (mock model, true accuracy 0.70, 30 items)")
def one_run(): return sum(rng.random() < 0.70 for _ in range(30)) / 30
singles = [one_run() for _ in range(8)]; mu = sum(singles) / 8; sd = (sum((x - mu) ** 2 for x in singles) / 7) ** .5
print(f"   8 single runs: min {min(singles):.3f} max {max(singles):.3f}; mean {mu:.3f} sd {sd:.3f}  -> a lone run can differ by several points; FIX: repeat trials, report mean and spread")
