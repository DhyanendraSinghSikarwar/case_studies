# Q20: why week-over-week PSI stays quiet while AUC decays. Synthetic, seeded, illustrative.
import numpy as np
from scipy.stats import norm
rng = np.random.default_rng(20)
N, BINS, WEEKS = 50_000, 10, 26
def psi(ref, cur, edges):
    r = np.histogram(np.clip(ref, edges[0], edges[-1]), edges)[0] / len(ref)
    c = np.histogram(np.clip(cur, edges[0], edges[-1]), edges)[0] / len(cur)
    r, c = np.clip(r, 1e-6, None), np.clip(c, 1e-6, None)
    return float(np.sum((c - r) * np.log(c / r)))
def edges_of(x):
    e = np.quantile(x, np.linspace(0, 1, BINS + 1)); e[0], e[-1] = -np.inf, np.inf
    return e
def auc(y, s):                       # Mann-Whitney with ranks (no ties for continuous scores)
    r = s.argsort().argsort() + 1
    n1 = y.sum(); n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
# --- Mechanism A: slow covariate drift, mean +0.03 sd per week
weeks_A = [rng.normal(0.03 * w, 1, N) for w in range(WEEKS + 1)]
wow = [psi(weeks_A[w-1], weeks_A[w], edges_of(weeks_A[w-1])) for w in range(1, WEEKS + 1)]
e0 = edges_of(weeks_A[0])
vs0 = [psi(weeks_A[0], weeks_A[w], e0) for w in range(1, WEEKS + 1)]
first_vs0_01 = next(w for w, v in enumerate(vs0, 1) if v > 0.10)
first_vs0_025 = next(w for w, v in enumerate(vs0, 1) if v > 0.25)
print(f"A: max week-over-week PSI = {max(wow):.4f} (never above 0.03: {max(wow) < 0.03})")
print(f"A: PSI against fixed week-0 reference: week 4 = {vs0[3]:.3f}, week 26 = {vs0[-1]:.3f}; passes 0.10 at week {first_vs0_01}, 0.25 at week {first_vs0_025}")
# --- Mechanism B: concept drift, inputs barely move. x | y ~ N(d_t * y, 1)
d0, d1 = np.sqrt(2) * norm.ppf(0.84), np.sqrt(2) * norm.ppf(0.78)      # binormal separation for AUC 0.84 and 0.78
M = 20_000
def week_B(w):
    d = d0 + (d1 - d0) * w / (WEEKS - 1)
    y = (rng.random(M) < 0.3).astype(int)
    return y, rng.normal(d * y, 1)
data = [week_B(w) for w in range(WEEKS)]
wowB = [psi(data[w-1][1], data[w][1], edges_of(data[w-1][1])) for w in range(1, WEEKS)]
vs0B = [psi(data[0][1], data[w][1], edges_of(data[0][1])) for w in range(1, WEEKS)]
aucs = [auc(y, x) for y, x in data]
print(f"B: max week-over-week PSI = {max(wowB):.4f}; max PSI against fixed week-0 = {max(vs0B):.4f} (both below 0.03)")
print(f"B: labelled AUC week 1 = {aucs[0]:.3f}, week 26 = {aucs[-1]:.3f}")
# noise of one weekly AUC at 20,000 rows, and of a 4-week pooled AUC
reps = [auc(*week_B(0)) for _ in range(40)]
sd = np.std(reps)
pool = []
for _ in range(15):
    ys, xs = zip(*[week_B(0) for _ in range(4)]); pool.append(auc(np.concatenate(ys), np.concatenate(xs)))
sd4 = np.std(pool)
print(f"AUC sampling sd: one week (20,000 rows) = {sd:.4f}; four pooled weeks (80,000 rows) = {sd4:.4f}")
# detection: alert when 4-week rolling labelled AUC is 0.03 below the launch AUC
launch = np.mean(aucs[:4])
roll = [np.mean(aucs[w-3:w+1]) for w in range(3, WEEKS)]
alert_week = next(w + 3 + 1 for w, a in enumerate(roll) if a < launch - 0.03)
print(f"labelled-AUC alert (4-week mean 0.03 below launch {launch:.3f}) fires in week {alert_week} of 26")
# asserts for every number quoted in the text
assert max(wow) < 0.03 and max(wowB) < 0.03 and max(vs0B) < 0.03
assert max(wow) < 0.002 and min(wow) > 0.0003
assert vs0[-1] > 0.25 and first_vs0_01 == 11 and first_vs0_025 == 18
assert abs(aucs[0] - 0.84) < 0.01 and abs(aucs[-1] - 0.78) < 0.01
assert sd < 0.006 and sd4 < sd
assert alert_week == 18 and first_vs0_01 < alert_week
assert round(0.84 - 0.78, 2) == 0.06
