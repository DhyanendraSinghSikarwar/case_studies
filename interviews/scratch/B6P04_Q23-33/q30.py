# Q30: existing users -3% in week 1, new users +4%: primacy or real harm? (illustrative simulation, seeded)
import numpy as np
from scipy import stats, optimize

rng = np.random.default_rng(30)
print("prompt: 10.0 -> 9.7 is", round(9.7 / 10.0 - 1, 3), "; blended week-1 effect if both groups have the same baseline:", round(0.8 * -3 + 0.2 * 4, 2), "%")
assert abs(9.7 / 10.0 - 1 + 0.03) < 1e-9 and abs(0.8 * -3 + 0.2 * 4 - -1.6) < 1e-9

# Story A (primacy): effect on existing users starts at -6% and fades with time constant tau days towards -0.5%
e0, einf = -0.06, -0.005
days = np.arange(1, 8)
f = lambda tau: np.mean(einf + (e0 - einf) * np.exp(-days / tau)) - (-0.03)
tau = optimize.brentq(f, 0.5, 50)
print(f"tau chosen so the week-1 average is -3%: {tau:.2f} days")
assert abs(f(tau)) < 1e-9
eff_A = lambda d: einf + (e0 - einf) * np.exp(-d / tau)
eff_B = lambda d: np.full_like(d, -0.03, dtype=float)       # Story B (real harm): constant -3%

def daily_effects(eff, n=40000, D=28, base=10.0, sd=6.0):
    """per-day difference in mean sessions per user between arms, with simulation noise."""
    d = np.arange(1, D + 1)
    se = sd * np.sqrt(2 / n)
    return d, base * eff(d) + rng.normal(0, se, D), se

def slope_test(d, y):
    r = stats.linregress(d[:14], y[:14])               # use first 14 exposure days
    return r.slope, r.pvalue
for name, eff in (("A primacy", eff_A), ("B real harm", eff_B)):
    d, y, se = daily_effects(eff)
    s, p = slope_test(d, y)
    wk = [y[i:i + 7].mean() / 10 * 100 for i in (0, 7, 14, 21)]
    print(f"{name:11s}: weekly effect % = {[round(float(w),2) for w in wk]}; slope over days 1-14 = {s:+.4f} sessions/day (p={p:.3f})")
    if name.startswith("A"): wkA, pA = wk, p
    else: wkB, pB = wk, p
assert wkA[0] < -2.5 and wkA[3] > -1.0 and pA < 0.05 and abs(wkB[3] + 3) < 1 and pB > 0.05
# new users have no habit to disrupt: their effect is a cleaner read of the steady state
print("blended week-1 effect with a 20% new-user share is read at", round(0.8 * -3 + 0.2 * 4, 1), "% while the steady state may differ")
n_need = 2 * (1.96 + 0.84) ** 2 * 6.0 ** 2 / 0.3 ** 2
print(f"users per arm to see a 3% (0.3 sessions) drop in ONE week's per-user average if sd is 6: about {n_need:,.0f}; we have 40,000, so the weekly readings above are well powered")
assert 6000 < n_need < 6600
