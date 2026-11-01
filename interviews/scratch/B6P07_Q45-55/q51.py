import math
def wil(k, n, z=1.96):
    p = k/n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return c-h, c+h
daily, n, k = 20_000, 500, 90
p = k/n
lo, hi = wil(k, n)
print(f"rate {p:.3f}, Wilson 95% {lo:.4f} to {hi:.4f}")
assert p == 0.18 and 0.148 < lo < 0.150 and 0.216 < hi < 0.218
proj = daily*p
print(f"projected prompts with personal data per day = {proj:.0f} (range {daily*lo:.0f} to {daily*hi:.0f})")
assert round(proj) == 3600 and round(daily*lo) == 2976 and round(daily*hi) == 4322
print(f"per year (365 d): {proj*365:,.0f}")
assert round(proj*365) == 1_314_000
# redaction recall sensitivity
for r in (0.90, 0.95, 0.99):
    leak = proj*(1-r)
    print(f"redaction recall {r:.0%}: {leak:.0f} prompts/day still carry personal data")
assert round(proj*0.05) == 180 and round(proj*0.01) == 36 and round(proj*0.10) == 360
# sample size to see a rare class: chance that a 500 sample misses a 0.5% type
miss = (1-0.005)**500
print(f"chance a 500-prompt sample contains none of a 0.5%-rare data type = {miss:.3f}")
assert round(miss, 3) == 0.082
