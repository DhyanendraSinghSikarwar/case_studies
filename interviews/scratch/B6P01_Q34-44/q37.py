# Q37 down 2% vs noise: same-weekday baseline vs naive rules (illustrative simulation)
import numpy as np
rng = np.random.default_rng(37)
dow = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 0.93, 0.90])   # Mon..Sun weekend dip
days = 7 * 60
t = np.arange(days)
level = 100_000 * (1 + 0.0002 * t)
y = level * dow[t % 7] * (1 + rng.normal(0, 0.015, days))    # 1.5% noise sd

# naive rule A: today vs yesterday, alert if down more than 2%
# naive rule B: today vs mean of previous 7 days, alert if down more than 2%
# good rule: today vs same weekday over previous 6 weeks, alert if z < -3
fireA = np.zeros(days, bool); fireB = np.zeros(days, bool)
for i in range(60, days):
    fireA[i] = y[i] / y[i-1] - 1 < -0.02
    fireB[i] = y[i] / y[i-7:i].mean() - 1 < -0.02
# simpler, transparent baseline: same weekday, last 6 weeks, scaled by the level growth over those weeks
fireC = np.zeros(days, bool); z_all = np.full(days, np.nan)
for i in range(60, days):
    base = y[[i - 7*k for k in range(1, 7)]]
    mu = base.mean(); sd = base.std(ddof=1)
    z = (y[i] - mu) / (sd * np.sqrt(1 + 1/6))
    z_all[i] = z; fireC[i] = z < -3
rng_idx = np.arange(60, days)
names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
print("alert rate by weekday (percent of days), naive A | naive B | same-weekday z<-3")
for d_ in range(7):
    m = (rng_idx % 7 == d_)
    print(f"{names[d_]}: {fireA[rng_idx][m].mean()*100:5.1f} | {fireB[rng_idx][m].mean()*100:5.1f} | {fireC[rng_idx][m].mean()*100:5.1f}")
print(f"overall: {fireA[rng_idx].mean()*100:.1f}% | {fireB[rng_idx].mean()*100:.1f}% | {fireC[rng_idx].mean()*100:.1f}%")
# the pure noise arithmetic for a 2% drop
from scipy.stats import norm
z2 = -0.02 / (0.015 * np.sqrt(1 + 1/6))
print(f"z for a -2% day with 1.5% sd and a 6-week baseline: {z2:.2f}, one-sided p = {norm.cdf(z2):.3f}")
from scipy.stats import t as tdist
print(f"with only 6 baseline points the z=-3 tail is a t(5) tail: P(t<-3) = {tdist.cdf(-3,5):.3f} (normal says {norm.cdf(-3):.4f})")
assert abs(tdist.cdf(-3,5)-0.015)<0.001
assert abs(z2 + 1.23) < 0.01 and 0.10 < norm.cdf(z2) < 0.12
assert fireA[rng_idx].mean() > 0.10 and fireC[rng_idx].mean() < 0.03
