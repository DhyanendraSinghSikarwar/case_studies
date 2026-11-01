from math import sqrt, exp
# Illustrative mixture: 20% 'core' users who return on 60% of days forever; 80% casual who fade out (decay 5 days)
core, p_core = 0.20, 0.60
casual, p_cas, tau = 0.80, 0.50, 5.0
def classic(day):            # opened the app ON day N
    return core * p_core + casual * p_cas * exp(-day / tau)
def bracket(day):            # opened ANY day in N..N+6
    return core * (1 - (1 - p_core) ** 7) + casual * (1 - (1 - p_cas * exp(-day / tau)) ** 7)
print("day  classic  7-day-bracket")
for d in (1, 7, 14, 30, 60, 90):
    print(f"{d:>3}  {classic(d):6.1%}  {bracket(d):6.1%}")
assert round(classic(30), 3) == 0.121 and round(classic(90), 3) == 0.120
assert round(bracket(30), 3) == 0.207 and round(bracket(60), 3) == 0.200
print(f"plateau classic {core * p_core:.1%}, bracket {core * (1 - 0.4 ** 7):.1%}")
assert round(core * p_core, 3) == 0.12 and round(core * (1 - 0.4 ** 7), 3) == 0.200
# sampling noise on a 12% number
for n in (1_000, 10_000):
    h = 1.96 * sqrt(0.12 * 0.88 / n)
    print(f"n={n:>6}: 12% +/- {h * 100:.1f} pts")
assert round(1.96 * sqrt(0.12 * 0.88 / 1000) * 100, 1) == 2.0
assert round(1.96 * sqrt(0.12 * 0.88 / 10000) * 100, 1) == 0.6
# a curve that never flattens: no core group
def no_core(day): return 0.5 * exp(-day / 20)
print("no-core curve day 30/60/90:", [f"{no_core(d):.1%}" for d in (30, 60, 90)])
assert no_core(90) < no_core(60) < no_core(30)
