# Contaminated golden set. Numbers from the prompt; Wilson intervals and a Fisher test are computed.
import math
from scipy.stats import fisher_exact
def wil(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h, c+h
tot_n, tot_k = 300, 282
c_n, c_k = 120, 117
u_n, u_k = 180, 165
assert c_k + u_k == tot_k and c_n + u_n == tot_n
print("blended", tot_k/tot_n)
print("contaminated", c_k, c_n, c_k/c_n, [round(x, 3) for x in wil(c_k, c_n)])
print("clean", u_k, u_n, round(u_k/u_n, 4), [round(x, 3) for x in wil(u_k, u_n)])
assert tot_k/tot_n == 0.94 and c_k/c_n == 0.975 and round(u_k/u_n, 4) == 0.9167
lo, hi = wil(u_k, u_n)
assert round(lo, 3) == 0.867 and round(hi, 3) == 0.949, (lo, hi)
gap = c_k/c_n - u_k/u_n
print("gap points", round(100*gap, 2))
assert round(100*gap, 2) == 5.83
odds, p = fisher_exact([[c_k, c_n-c_k], [u_k, u_n-u_k]])
print("Fisher exact p for the gap", round(p, 3))
assert 0.04 < p < 0.05       # borderline with these counts
# Weight check: if production mix were 100% clean-like, headline would be the clean rate
print("clean-only headline", f"{u_k/u_n:.1%}", "vs 94.0% blended: overstated by", round(100*(tot_k/tot_n - u_k/u_n), 2), "points")
assert round(100*(tot_k/tot_n - u_k/u_n), 2) == 2.33
# Size of a rebuilt set for a +/-2.5 point interval at p about 0.92
n_need = math.ceil(1.96**2 * 0.92*0.08 / 0.025**2)
print("rebuilt set size for +/-2.5 points at 92%:", n_need)
assert n_need == 453
