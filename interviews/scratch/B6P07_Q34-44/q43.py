import math
import numpy as np
from scipy import stats

# Illustrative numbers from the prompt
judge, answers, gen, rate = 0.01, 1_000_000, 0.012, 0.02
sample = 0.05 * answers
cost = sample * judge
print(f"5% sample = {sample:.0f} answers, judge cost {cost:.0f}; generation spend {answers*gen:.0f}; judge is {cost/(answers*gen):.1%} of it")
assert sample == 50_000 and round(cost) == 500 and round(answers * gen) == 12_000 and round(cost / (answers * gen), 3) == 0.042

exp_fail = sample * rate
print("expected failures in the 5% sample:", exp_fail)
assert round(exp_fail) == 1_000

n_exp = 100 / rate
print(f"to expect 100 failures: {n_exp:.0f} answers, cost {n_exp*judge:.0f}; P(actually >= 100) = {stats.binom.sf(99, int(n_exp), rate):.2f}")
assert n_exp == 5_000 and round(n_exp * judge) == 50
assert 0.50 < stats.binom.sf(99, 5000, rate) < 0.53

n = next(n for n in range(5000, 8000) if stats.binom.sf(99, n, rate) >= 0.95)
print(f"to be 95% sure of at least 100 failures: {n} answers, cost {n*judge:.1f}")
assert n == 5841

# Rate precision from a plain sample (Wilson half-width) at 5,000 and 50,000
def hw(k, m, z=1.96):
    p = k / m; d = 1 + z * z / m
    return z * math.sqrt(p * (1 - p) / m + z * z / (4 * m * m)) / d
print("95%% half-width on the rate: n=5,000 -> %.2f points; n=50,000 -> %.2f points" % (100 * hw(100, 5000), 100 * hw(1000, 50000)))
assert 0.38 < 100 * hw(100, 5000) < 0.42 and 0.11 < 100 * hw(1000, 50000) < 0.13

# Stratified sampling (invented strata): 10% of traffic is low-confidence with failure rate 12.5%, the rest 0.8333%, overall 2%
wA, rA = 0.10, 0.125
wB = 1 - wA; rB = (rate - wA * rA) / wB
assert abs(wA * rA + wB * rB - rate) < 1e-12
budget = 5_000
unif_found = budget * rate
strat_found = 2_500 * rA + 2_500 * rB
se_unif = math.sqrt(rate * (1 - rate) / budget)
se_strat = math.sqrt(wA**2 * rA * (1 - rA) / 2_500 + wB**2 * rB * (1 - rB) / 2_500)
print(f"same budget of {budget}: failures found uniform {unif_found:.0f} vs 50/50 stratified {strat_found:.0f}; std error of overall rate {se_unif:.4f} vs {se_strat:.4f}")
assert round(strat_found) == 333 and se_strat < se_unif
# the weighted estimate stays unbiased (check by simulation, seeded)
rng = np.random.default_rng(5)
est = [wA * rng.binomial(2_500, rA) / 2_500 + wB * rng.binomial(2_500, rB) / 2_500 for _ in range(4000)]
print("simulated mean of weighted estimate: %.4f, sd %.4f" % (np.mean(est), np.std(est)))
assert abs(np.mean(est) - rate) < 0.0005 and abs(np.std(est) - se_strat) < 0.0003
assert answers * judge == 10_000 and round(answers * judge / (answers * gen), 2) == 0.83
