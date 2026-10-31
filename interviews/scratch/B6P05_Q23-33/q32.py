# Q32: lead-time demand and safety stock (illustrative)
import numpy as np
mu, sd, L, z = 50.0, 10.0, 4, 1.645
sd_L = sd * np.sqrt(L)
ss = z * sd_L
mean_L = mu * L
rop = mean_L + ss
print(f"lead-time demand mean {mean_L:.0f}, sd {sd_L:.1f}; safety stock {ss:.2f}; reorder point {rop:.2f}")
assert sd_L == 20.0 and abs(ss - 32.9) < 1e-9 and abs(rop - 232.9) < 1e-9

rng = np.random.default_rng(32)
N = 400_000
d = rng.normal(mu, sd, (N, L)).sum(axis=1)
print("simulated cycle service level at ROP 232.9 with independent days:", round((d <= rop).mean(), 4))
assert abs((d <= rop).mean() - 0.95) < 0.003

# positively autocorrelated days (AR(1), rho=0.3), same daily mean and sd
rho = 0.3
e = rng.normal(0, 1, (N, L))
x = np.zeros((N, L)); x[:, 0] = e[:, 0]
for t in range(1, L):
    x[:, t] = rho * x[:, t-1] + np.sqrt(1 - rho**2) * e[:, t]
dd = (mu + sd * x).sum(axis=1)
var_formula = sd**2 * (L + 2 * sum((L - k) * rho**k for k in range(1, L)))
print(f"rho=0.3: simulated sd {dd.std():.2f}, formula {np.sqrt(var_formula):.2f} (independence said 20.0)")
print("service level at the same ROP:", round((dd <= rop).mean(), 4), "; safety stock needed for 95%:", round(z * np.sqrt(var_formula), 1))
assert abs(dd.std() - np.sqrt(var_formula)) < 0.2 and (dd <= rop).mean() < 0.95 - 0.01
assert abs(z * np.sqrt(var_formula) - 41.0) < 0.2

# lead time itself varies (mean 4, sd 1 day), independent days
sd_Lt = 1.0
var2 = L * sd**2 + mu**2 * sd_Lt**2
print(f"with lead-time sd 1 day: sd of lead-time demand {np.sqrt(var2):.1f}; safety stock {z*np.sqrt(var2):.1f}")
assert abs(np.sqrt(var2) - np.sqrt(400 + 2500)) < 1e-9 and z * np.sqrt(var2) > 85
