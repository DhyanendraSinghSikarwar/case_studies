import numpy as np

SLO = 0.99                       # SLI: share of hourly requests whose feature rows pass validation
BUDGET = 1 - SLO                 # allowed bad share = 1 %

def sli(good, bad, end, hours):
    """SLI over the last `hours` hours ending at index `end` (inclusive)."""
    lo = max(0, end - hours + 1)
    g, b = good[lo:end + 1].sum(), bad[lo:end + 1].sum()
    return g / (g + b)

def burn(good, bad, end, hours):
    return (1 - sli(good, bad, end, hours)) / BUDGET     # 1.0 = spending budget exactly at the allowed pace

rng = np.random.default_rng(26)
H = 72
total = rng.integers(900, 1100, H)
bad_rate = np.full(H, 0.004)
bad_rate[30:38] = 0.08           # upstream bug: 8 bad hours, then fixed
bad = rng.binomial(total, bad_rate); good = total - bad

LONG, SHORT, THRESH = 6, 1, 6.0  # illustrative; pick thresholds from your own budget maths
print("hour  bad%  burn1h burn6h  single(6h>=6)  two-window(6h&1h>=6)")
fired_single, fired_two = [], []
for h in range(H):
    b1, b6 = burn(good, bad, h, SHORT), burn(good, bad, h, LONG)
    s = b6 >= THRESH
    t = b6 >= THRESH and b1 >= THRESH
    fired_single.append(s); fired_two.append(t)
    if 28 <= h <= 46 and (h % 1 == 0):
        print(f"{h:4d} {100*bad[h]/total[h]:5.1f} {b1:7.1f} {b6:6.1f}  {str(s):13s}  {t}")
print("single-window alert hours:", [h for h, v in enumerate(fired_single) if v])
print("two-window alert hours   :", [h for h, v in enumerate(fired_two) if v])
print(f"whole-window check: bad share over all {H}h = {bad.sum()/total.sum():.4f}, budget {BUDGET:.4f}, budget used = {bad.sum()/total.sum()/BUDGET:.0%}")
