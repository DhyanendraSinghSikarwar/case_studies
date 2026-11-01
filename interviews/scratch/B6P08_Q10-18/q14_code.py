import math
from scipy import stats

xc, nc, xt, nt = 9, 2000, 76, 38000
assert nc == 0.05 * 40000 and nt == 40000 - nc
assert xc / nc == 0.0045 and xt / nt == 0.002
diff = xc / nc - xt / nt
p = (xc + xt) / (nc + nt)
se = math.sqrt(p * (1 - p) * (1 / nc + 1 / nt))
z = diff / se
p2 = 2 * (1 - stats.norm.cdf(z))
print(f"diff {diff*100:.2f} points | pooled z {z:.2f} | two-sided p {p2:.3f}")
assert round(z, 2) == 2.37 and round(p2, 3) == 0.018
odds, pf = stats.fisher_exact([[xc, nc - xc], [xt, nt - xt]])
print(f"Fisher exact p {pf:.3f} | relative risk {(xc/nc)/(xt/nt):.2f}")
assert pf < 0.05 and round((xc / nc) / (xt / nt), 2) == 2.25
# Newcombe-style interval from Wilson intervals for each arm
def wilson(x, n, zc=1.96):
    ph = x / n; d = 1 + zc**2 / n
    c = (ph + zc**2 / (2 * n)) / d; h = zc * math.sqrt(ph * (1 - ph) / n + zc**2 / (4 * n * n)) / d
    return c - h, c + h
l1, u1 = wilson(xc, nc); l2, u2 = wilson(xt, nt)
lo = diff - math.sqrt((xc/nc - l1)**2 + (u2 - xt/nt)**2)
hi = diff + math.sqrt((u1 - xc/nc)**2 + (xt/nt - l2)**2)
print(f"95% interval for the gap: {lo*100:.2f} to {hi*100:.2f} points")
assert 0 < lo < 0.001 and 0.006 < hi < 0.007   # lower end barely clears zero
# Unpooled Wald interval disagrees with the pooled z: it includes zero
se_u = math.sqrt(xc/nc*(1-xc/nc)/nc + xt/nt*(1-xt/nt)/nt)
print(f"Wald interval: {(diff-1.96*se_u)*100:.2f} to {(diff+1.96*se_u)*100:.2f} points")
assert diff - 1.96 * se_u < 0
# Sample per arm to detect 0.2% vs 0.3% (80% power, 5% two-sided)
n_arm = (1.96 + 0.8416) ** 2 * (0.002 * 0.998 + 0.003 * 0.997) / 0.001 ** 2
print("requests per arm for 0.2% vs 0.3%:", round(n_arm))
assert 30_000 < n_arm < 50_000
# Expected canary errors if the canary were no worse: 2000 * 0.002 = 4
assert nc * xt / nt == 4.0
# Peeking: hourly looks for 6 hours inflate false alarms (independent-look approximation)
print("false-alarm chance over 6 looks at 5%:", round((1 - 0.95**6) * 100, 1), "%")
assert round((1 - 0.95**6) * 100, 1) == 26.5

# Segment case (illustrative split): segment A is 2% of traffic
segA_c, segA_t = 40, 760
a_err_c, a_err_t = 9, 4
print("segment A: canary", a_err_c, "/", segA_c, "=", round(a_err_c/segA_c*100, 1), "% vs control", a_err_t, "/", segA_t, "=", round(a_err_t/segA_t*100, 2), "%")
_, pA = stats.fisher_exact([[a_err_c, segA_c - a_err_c], [a_err_t, segA_t - a_err_t]])
rest_c, rest_t = nc - segA_c, nt - segA_t
rest_ec, rest_et = xc - a_err_c, xt - a_err_t
print("rest of traffic: canary", rest_ec, "/", rest_c, "vs control", rest_et, "/", rest_t, "=", round(rest_et/rest_t*100, 3), "%")
exp_rest = rest_c * rest_et / rest_t
print(f"segment A p {pA:.1e} | rest of traffic: canary errors 0 vs {exp_rest:.1f} expected from control rate")
assert pA < 1e-6 and rest_ec == 0 and round(exp_rest, 1) == 3.8
