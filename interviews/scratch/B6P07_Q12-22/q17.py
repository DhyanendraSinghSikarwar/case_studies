import math
stored, hit_rate = 500_000, 0.02
n_pii = int(stored * hit_rate)
print(f"conversations with PII: {n_pii:,}")
assert n_pii == 10_000
# Steady-state effect of shorter retention (assumes constant volume and constant PII rate).
for days in (400, 90, 30):
    kept = stored * days / 400
    print(f"retention {days:>3} days: ~{kept:,.0f} stored, ~{kept*hit_rate:,.0f} with PII")
assert stored * 30 / 400 * hit_rate == 750
# After redaction at write, check a random sample; zero hits is not zero risk.
n = 1000
rule3 = 3 / n
exact = 1 - 0.05 ** (1 / n)
print(f"0 PII hits in {n} sampled: 95% upper bound ~{rule3:.2%} (rule of three), exact {exact:.3%}")
assert round(rule3, 4) == 0.003 and round(exact, 5) == 0.00299
# A regex scan has recall below 100%: if it finds 10,000 at recall 80%, the true count is higher.
for recall in (1.0, 0.8, 0.6):
    print(f"detector recall {recall:.0%}: implied true PII conversations ~{n_pii/recall:,.0f}")
assert round(n_pii / 0.8) == 12_500
