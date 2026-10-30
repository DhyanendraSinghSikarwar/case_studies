# Q16: daily peeking in an A/A test, and a fix with group-sequential boundaries (simulation)
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(16)
K, reps, per_day = 14, 100_000, 500          # 14 daily looks, 500 users per arm per day
z95 = norm.ppf(0.975)

# A/A: both arms have the same distribution. Look k uses all data up to day k.
d = rng.normal(0, 1, (reps, K, 2, per_day))
cum = d.sum(axis=3).cumsum(axis=1)           # (reps, K, 2) running sums per arm
n_k = per_day * np.arange(1, K + 1)
diff = cum[:, :, 1] / n_k[None, :] - cum[:, :, 0] / n_k[None, :]
z = diff / np.sqrt(2 / n_k[None, :])

single = np.mean(np.abs(z[:, -1]) > z95)
naive = np.mean((np.abs(z) > z95).any(axis=1))
print(f"one look at day 14: false positive rate = {single:.3f}")
print(f"stop at first p<0.05 over 14 daily looks: {naive:.3f}  (about 1 in {1/naive:.1f})")
assert abs(single - 0.05) < 0.005 and 0.18 < naive < 0.28

# when do the false wins occur?
first = np.where((np.abs(z) > z95).any(axis=1), (np.abs(z) > z95).argmax(axis=1) + 1, 0)
print("share of false wins by first day (1..14):", np.round(np.bincount(first, minlength=15)[1:] / reps, 3))

# Fix 1: one constant (Pocock-style) boundary for all 14 looks
def alpha_for(boundary):
    return np.mean((np.abs(z) > boundary[None, :]).any(axis=1))

lo_c, hi_c = 2.0, 3.5
for _ in range(30):
    mid = (lo_c + hi_c) / 2
    if alpha_for(np.full(K, mid)) > 0.05: lo_c = mid
    else: hi_c = mid
c_poc = hi_c
# Fix 2: O'Brien-Fleming-style boundary c*sqrt(K/k): strict early, near 1.96 at the end
lo_c, hi_c = 1.5, 3.0
for _ in range(30):
    mid = (lo_c + hi_c) / 2
    if alpha_for(mid * np.sqrt(K / np.arange(1, K + 1))) > 0.05: lo_c = mid
    else: hi_c = mid
c_obf = hi_c
bound_obf = c_obf * np.sqrt(K / np.arange(1, K + 1))
print(f"constant boundary |z| > {c_poc:.2f} at every look -> overall alpha {alpha_for(np.full(K, c_poc)):.3f}")
print(f"OBF-style: c = {c_obf:.2f}; |z| bounds day 1 {bound_obf[0]:.2f}, day 7 {bound_obf[6]:.2f}, day 14 {bound_obf[-1]:.2f} -> overall alpha {alpha_for(bound_obf):.3f}")
assert 2.5 < c_poc < 2.9 and abs(alpha_for(np.full(K, c_poc)) - 0.05) < 0.006
assert bound_obf[-1] < 2.2 and bound_obf[0] > 6

# Power cost of the fix: true effect 0.04 sd, 14 looks, compare fixed-sample test at day 14
eff = 0.04
d2 = rng.normal(0, 1, (20_000, K, 2, per_day)); d2[:, :, 1, :] += eff
cum2 = d2.sum(axis=3).cumsum(axis=1)
diff2 = cum2[:, :, 1] / n_k[None, :] - cum2[:, :, 0] / n_k[None, :]
z2 = diff2 / np.sqrt(2 / n_k[None, :])
pw_fixed = np.mean(z2[:, -1] > z95)
pw_obf = np.mean((z2 > bound_obf[None, :]).any(axis=1))
print(f"power, effect 0.04 sd: fixed day-14 test {pw_fixed:.2f}; OBF with early stopping allowed {pw_obf:.2f}")
assert pw_obf < pw_fixed and pw_fixed - pw_obf < 0.1
print("all asserts passed")
