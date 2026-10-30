# Q33: 12 shipped +1% experiments vs a +5.5% holdout (illustrative simulation, seeded)
import numpy as np

rng = np.random.default_rng(33)
print("compounded sum of twelve +1%:", round(1.01**12 - 1, 4), "; log-points:", round(12 * np.log(1.01), 4), "vs holdout", round(np.log(1.055), 4))
assert abs(1.01**12 - 1 - 0.1268) < 5e-4
print(f"holdout shows {np.log(1.055)/(12*np.log(1.01))*100:.0f}% of the compounded promise")

# Reason 1: winner's curse. 600 candidate ideas, true lifts mostly small; each test has noise; ship only significant wins.
K, SE = 600, 0.003
true = rng.normal(0.0030, 0.0045, K)
meas = true + rng.normal(0, SE, K)
ship = meas / SE > 1.96
print(f"shipped {ship.sum()} of {K}: average MEASURED lift {meas[ship].mean()*100:.2f}%, average TRUE lift {true[ship].mean()*100:.2f}%")
assert meas[ship].mean() > true[ship].mean() + 0.001 and 0.008 < meas[ship].mean() < 0.012

# Reason 2 and 3 (illustrative factors, to be measured not assumed): novelty fades; overlapping tests cannibalise each other.
true_each = true[ship].mean(); persist = 0.75; overlap = 0.90
per = true_each * persist * overlap
cum = (1 + per) ** 12 - 1
print(f"illustrative chain: {true_each*100:.2f}% true x {persist} still there after novelty x {overlap} after overlap = {per*100:.3f}% each; twelve compounded = {cum*100:.1f}%")
assert 0.045 < cum < 0.065

# Reason 4: the holdout has its own noise. 5% holdout of 10M users, revenue per user CV = 3
N_H, N_L, CV = 500_000, 9_500_000, 3.0
se_rel = CV * np.sqrt(1 / N_H + 1 / N_L)
lo, hi = 1.055 - 1.96 * se_rel * 1.055, 1.055 + 1.96 * se_rel * 1.055
print(f"holdout 5.5% has SE {se_rel*100:.2f} points; 95% CI about {100*(lo-1):.1f}% to {100*(hi-1):.1f}%; 12.7% is far outside")
assert hi - 1 < 0.08
