import math
n = 300
rule3 = 3/n
exact = 1 - 0.05**(1/n)
print(f"rule of three: {rule3:.4f}; exact one-sided 95% upper bound: {exact:.5f}")
assert abs(rule3 - 0.01) < 1e-12 and 0.00990 < exact < 0.00997
assert abs((1-exact)**n - 0.05) < 1e-12
# two-sided 97.5% (Clopper-Pearson, 0 successes) and Wilson for comparison
cp2 = 1 - 0.025**(1/n)
z = 1.96
wil = z*z/(n+z*z)
print(f"two-sided Clopper-Pearson upper: {cp2:.4f}; Wilson upper: {wil:.4f}")
assert 0.0120 < cp2 < 0.0124 and 0.0125 < wil < 0.0128
# attempts needed to claim <= 0.1% and <= 0.01%
for t in (0.001, 0.0001):
    need = math.log(0.05)/math.log(1-t)
    print(f"attacks with zero successes needed to claim rate <= {t:.2%}: {math.ceil(need):,} (rule of three: {3/t:,.0f})")
assert math.ceil(math.log(0.05)/math.log(0.999)) == 2995 and math.ceil(math.log(0.05)/math.log(0.9999)) == 29956
# what 1% per attempt means for a persistent attacker
for tries in (10, 100, 1000):
    print(f"at 1% per attempt, chance of at least one success in {tries}: {1-0.99**tries:.4f}")
assert round(1-0.99**100, 3) == 0.634 and round(1-0.99**1000, 4) == 1.0
# even at the exact bound 0.0099 per attempt
print(f"at 0.0099 per attempt, 100 attempts: {1-(1-exact)**100:.3f}")
assert round(1-(1-exact)**100, 3) == 0.632
# if the 300 attacks were really 30 attack families x 10 near-duplicate variants (effective n ~ 30)
n_eff = 30
print(f"if effective independent attacks are 30: upper bound = {1-0.05**(1/n_eff):.3f}")
assert round(1-0.05**(1/n_eff), 3) == 0.095
# one success in 300: solve P(X<=1) = 0.05 by bisection
f = lambda p: (1-p)**n + n*p*(1-p)**(n-1) - 0.05
lo_, hi_ = 0.0, 0.1
for _ in range(100):
    mid = (lo_+hi_)/2
    if f(mid) > 0: lo_ = mid
    else: hi_ = mid
print(f"upper bound with 1 success in 300: {lo_:.5f} = {lo_*n:.2f} / n")
assert 4.6 < lo_*n < 4.8
