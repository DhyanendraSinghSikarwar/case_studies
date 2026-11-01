import random, math
random.seed(7)
prompts, runs, per_call = 2000, 3, 0.0153
calls = prompts * runs
cost = calls * per_call
print(f"calls per candidate = {calls}, cost = {cost:.2f} (illustrative units)")
assert calls == 6000 and abs(cost - 91.80) < 1e-9
print(f"3 candidates = {3*cost:.2f}; baseline re-run on same suite = {cost:.2f}")
assert abs(3*cost - 275.40) < 1e-9
# sign test on prompts whose majority-of-3 verdict flipped (invented counts)
worse, better = 60, 70
n = worse + better
def binom_two_sided(k, n):
    pm = lambda i: math.comb(n, i) / 2**n
    p = sum(pm(i) for i in range(n + 1) if pm(i) <= pm(k) + 1e-15)
    return min(1.0, p)
p = binom_two_sided(min(worse, better), n)
print(f"flipped prompts: {worse} worse, {better} better, exact sign-test p = {p:.3f}")
assert 0.4 < p < 0.5
# how noisy is one run? simulate 2000 prompts: 1700 always pass, 100 always fail, 200 flaky (pass 50%)
def run_pass_count():
    return 1700 + sum(random.random() < 0.5 for _ in range(200))
one = [run_pass_count() for _ in range(2000)]
sd = (sum((x - sum(one)/len(one))**2 for x in one) / (len(one)-1)) ** 0.5
print(f"one-run pass count sd = {sd:.1f} prompts = {sd/20:.2f} points (flaky prompts only)")
assert 6 < sd < 8.5
# flaky prompts flagged: disagree across 3 runs
flag = 1 - 2 * 0.5**3
print(f"a 50% flaky prompt shows disagreement across 3 runs with prob {flag:.2f}")
assert flag == 0.75
# at most 90 days: schedule
print("day 0-7 freeze suite; 8-30 candidates; 31-60 canary; 61-75 full ramp; 76-90 buffer")
