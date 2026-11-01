# Launch-readiness arithmetic: exact (Clopper-Pearson) bounds on failure rates, and sample sizes for 'zero failures observed'.
import math
def binom_cdf(k, n, p): return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))
def upper_bound(f, n, conf=0.95):                       # one-sided exact upper bound on the failure rate after f failures in n
    if f >= n: return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if binom_cdf(f, n, mid) > 1 - conf: lo = mid
        else: hi = mid
    return hi
def lower_bound(s, n, conf=0.95):                       # one-sided lower bound on pass rate = 1 - upper bound on failure rate
    return 1 - upper_bound(n - s, n, conf)
# checks: zero failures has the closed form 1-(1-conf)^(1/n); rule of three says about 3/n
for n in (50, 100, 150, 300):
    print(f"0 failures in {n:3d}: exact upper {upper_bound(0, n):.4f}  closed form {1-0.05**(1/n):.4f}  rule of three {3/n:.4f}")
# brute-force check of the bound for 2 failures in 40: P(X<=2 | p=bound) should equal 0.05
ub = upper_bound(2, 40); print(f"2 failures in 40: bound {ub:.4f}; P(X<=2 | p=bound) = {binom_cdf(2, 40, ub):.4f}")
need = lambda target: next(n for n in range(1, 5000) if upper_bound(0, n) <= target)
print("\ncases needed with ZERO failures to bound the failure rate:", {t: need(t) for t in (0.10, 0.05, 0.02, 0.01)})
# launch scorecard (SYNTHETIC results, assumed thresholds)
card = [("helpfulness pass (human-graded)", 182, 200, "lower", 0.85), ("grounded in cited source", 188, 200, "lower", 0.90),
        ("critical clinical error (fail count)", 1, 250, "upper", 0.02), ("red-team: harmful compliance", 2, 80, "upper", 0.05),
        ("refuses safe requests (over-refusal)", 9, 200, "upper", 0.08)]
print("\ncriterion                              result      95% bound  threshold  verdict")
for name, x, n, kind, thr in card:
    if kind == "lower":
        b = lower_bound(x, n); ok = b >= thr; print(f"{name:38} {x}/{n} pass   >= {b:.3f}   >= {thr:.2f}     {'MET' if ok else 'NOT MET'}")
    else:
        b = upper_bound(x, n); ok = b <= thr; print(f"{name:38} {x}/{n} fail   <= {b:.3f}   <= {thr:.2f}     {'MET' if ok else 'NOT MET'}")
# staged rollout: if zero critical incidents are seen at each stage, how many requests until the 95% upper bound <= 1%?
print("\nrequests with zero critical incidents needed to bound incident rate <= 1%:", need(0.01), "; <= 0.1%:", need(0.001))
