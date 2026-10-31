# Q12: partner feed in miles inside a kilometre table (illustrative numbers)
import numpy as np
from scipy import stats
rng = np.random.default_rng(12)
N, NP = 500_000, 90_000
MI = 0.621371
km = rng.lognormal(np.log(5.0), 0.6, N)
partner = np.zeros(N, bool); partner[rng.choice(N, NP, replace=False)] = True
print("partner share:", f"{partner.mean():.0%}"); assert partner.sum() == NP and partner.mean() == 0.18
straight = km / rng.uniform(1.15, 1.45, N)            # straight-line distance from coordinates
reported = np.where(partner, km * MI, km)             # what the table says
minutes = 8 + 4.5 * km + rng.normal(0, 4, N)          # delivery time truth

# Step 1: find affected rows: ratio of reported distance to coordinate distance, by source
ratio = reported / straight
r_p, r_o = np.median(ratio[partner]), np.median(ratio[~partner])
print(f"median reported/straight: partner {r_p:.3f}  others {r_o:.3f}  ratio {r_p / r_o:.3f}")
assert abs(r_p / r_o - MI) < 0.01
# a row-level screen with no feed label: ratio below 0.95 flags most miles rows
flag = ratio < 1.0
print(f"row screen (ratio<1.0): catches {(flag & partner).sum() / NP:.1%} of partner rows, false alarms {(flag & ~partner).sum() / (~partner).sum():.1%} of others")

# Step 2: repair the data and verify the repair
fixed = np.where(partner, reported / MI, reported)
ks = stats.ks_2samp(fixed[partner], fixed[~partner]).statistic
ks_raw = stats.ks_2samp(reported[partner], reported[~partner]).statistic
print(f"KS partner vs others: raw {ks_raw:.3f}  after fix {ks:.3f}")
assert ks_raw > 0.3 and ks < 0.02

# Step 3: repair the model: fit a line on the broken table versus the fixed table
idx = rng.permutation(N); tr, te = idx[:400_000], idx[400_000:]
def fit(d): return np.linalg.lstsq(np.c_[np.ones(len(tr)), d[tr]], minutes[tr], rcond=None)[0]
def mae(d, w, m): return float(np.mean(np.abs(minutes[m] - (w[0] + w[1] * d[m]))))
tep = te[partner[te]]; teo = te[~partner[te]]
w_bad, w_ok = fit(reported), fit(fixed)
print(f"MAE minutes on partner rows: trained on broken {mae(reported, w_bad, tep):.2f} | fixed data {mae(fixed, w_ok, tep):.2f}")
print(f"MAE minutes on other rows:   trained on broken {mae(reported, w_bad, teo):.2f} | fixed data {mae(fixed, w_ok, teo):.2f}")
print(f"MAE overall (test):          broken {mae(reported, w_bad, te):.2f} | fixed {mae(fixed, w_ok, te):.2f}")
assert mae(fixed, w_ok, tep) < mae(reported, w_bad, tep)
print("slope per km: broken", round(w_bad[1], 2), "fixed", round(w_ok[1], 2)); assert abs(w_ok[1] - 4.5) < 0.1

# Step 4: the check that would have caught it: daily per-source median ratio against a band
def unit_check(r, src_mask, band=(0.85, 1.15), ref=None):
    m = np.median(r[src_mask]) / ref
    return round(float(m), 3), bool(not (band[0] <= m <= band[1]))
print("check partner :", unit_check(ratio, partner, ref=r_o))
print("check others  :", unit_check(ratio, ~partner, ref=r_o))
assert unit_check(ratio, partner, ref=r_o)[1] and not unit_check(ratio, ~partner, ref=r_o)[1]
