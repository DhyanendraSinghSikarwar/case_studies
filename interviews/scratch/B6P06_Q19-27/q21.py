import math
from scipy import stats
k, n = 12, 400
p = k / n
z = 1.959963984540054
den = 1 + z*z/n
centre = (p + z*z/(2*n)) / den
half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / den
lo, hi = centre - half, centre + half
cp_lo = stats.beta.ppf(0.025, k, n-k+1); cp_hi = stats.beta.ppf(0.975, k+1, n-k)
print(f"observed {p:.1%}; Wilson 95% {lo:.2%} to {hi:.2%}; exact (Clopper-Pearson) {cp_lo:.2%} to {cp_hi:.2%}")
assert abs(p - 0.03) < 1e-12 and 0.016 < lo < 0.018 and 0.051 < hi < 0.053
# what the interval means at an illustrative volume of 100,000 summaries a month
vol = 100_000
print(f"at {vol:,} summaries a month: expected {p*vol:,.0f} bad, plausible range {lo*vol:,.0f} to {hi*vol:,.0f}")
assert round(p*vol) == 3000
# can this sample prove the rate is under a 4% ceiling? upper bound 5.2% says no
print("upper bound under 4%?", hi < 0.04)
assert not (hi < 0.04)
# sample size so a 3% observed rate has a Wilson upper bound under 4%
def upper(k, n):
    pp = k/n; d = 1 + z*z/n
    return (pp + z*z/(2*n))/d + z*math.sqrt(pp*(1-pp)/n + z*z/(4*n*n))/d
nn = 400
while upper(round(0.03*nn), nn) >= 0.04: nn += 10
print(f"if the true rate stays 3%, about {nn} summaries are needed for an upper bound below 4%")
assert upper(round(0.03*nn), nn) < 0.04 and nn > 1000
