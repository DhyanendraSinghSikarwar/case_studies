import math
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
k, n = 36, 300
lo, hi = wilson(k, n)
print(f"rate {k/n:.1%}, 95% Wilson {lo:.1%} to {hi:.1%}")
assert k/n == 0.12 and round(lo, 3) == 0.088 and round(hi, 3) == 0.162
# Wald interval for comparison (worse near 0 or small n)
se = math.sqrt(0.12*0.88/300); print(f"Wald {0.12-1.96*se:.1%} to {0.12+1.96*se:.1%}")
# Outside the sample: expected unsupported answers per 10,000 (only if sample is random from that population)
print(f"per 10,000 answers: {lo*1e4:.0f} to {hi*1e4:.0f}")
# Answers vs claims: if an answer has ~8 claims, an answer-level 12% is a much lower claim-level rate
claims = 8
claim_rate_if_one_bad_claim = 0.12 / claims
print(f"if each bad answer has exactly 1 bad claim in {claims}: claim-level rate {claim_rate_if_one_bad_claim:.2%}")
assert round(claim_rate_if_one_bad_claim, 4) == 0.015
# Target: what observed rate lets a 300-sample audit prove <= 5%? Need the Wilson upper bound <= 5%
best = max(kk for kk in range(0, 301) if wilson(kk, 300)[1] <= 0.05)
print("max bad answers out of 300 with upper bound <= 5%:", best, "->", f"{best/300:.2%}")
assert best == 7 and wilson(7, 300)[1] <= 0.05 < wilson(8, 300)[1]
# Sample size needed to show upper bound <= 5% if the true rate is 3%
for N in (300, 500, 1000):
    kk = round(0.03*N); print(N, kk, f"upper {wilson(kk, N)[1]:.2%}")
assert wilson(9, 300)[1] > 0.05 and wilson(15, 500)[1] < 0.05 and wilson(30, 1000)[1] < 0.05
