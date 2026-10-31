import math
from random import Random
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
n, consistent = 100, 68
lo, hi = wilson(consistent, n)
print(f"order-consistent {consistent}/{n} = {consistent/n:.0%} (95% Wilson {lo:.1%} to {hi:.1%}); flipped with order {n-consistent}")
assert round(lo, 3) == 0.583 and round(hi, 3) == 0.763
# Reference points: a judge that always says "first" is consistent 0%; one that guesses at random is consistent 50%
# Simulation (seeded): random coin flip judge, 100 pairs
r = Random(3)
cons = sum((r.random() < 0.5) == (r.random() < 0.5) for _ in range(100000))/100000
print(f"random guesser, order swapped: consistent {cons:.3f} (should be near 0.5)")
assert abs(cons - 0.5) < 0.01
kappa_like = (consistent/n - 0.5) / (1 - 0.5)
print(f"consistency above chance: {kappa_like:.2f}"); assert round(kappa_like, 2) == 0.36
# Reporting win rate. Among the 68 consistent pairs, suppose the new answer wins 45 and loses 23 (illustrative)
win, loss, flips = 45, 23, 32
assert win + loss == consistent
tie_half = (win + 0.5*flips) / n
lo_b, hi_b = win / n, (win + flips) / n
print(f"win rate, flips as half: {tie_half:.0%}; bounds if flips all lost / all won: {lo_b:.0%} to {hi_b:.0%}")
assert tie_half == 0.61 and (lo_b, hi_b) == (0.45, 0.77)
print(f"win rate among decisive pairs: {win}/{consistent} = {win/consistent:.1%}  (Wilson {wilson(win, consistent)[0]:.1%} to {wilson(win, consistent)[1]:.1%})")
assert round(win/consistent, 3) == 0.662
