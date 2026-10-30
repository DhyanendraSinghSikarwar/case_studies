import numpy as np
from scipy.stats import norm

# Prompt check: catch rate 85% -> 70% with flat FPR. Illustrative month: 1,000 confirmed fraud cases.
# Two tactics: old (still caught at 85%) and new (caught at 10%).
n_fraud, catch_old, catch_new = 1000, 0.85, 0.10
share_new = (0.85 - 0.70) / (catch_old - catch_new)      # mix that gives 70% overall
print(f"new-tactic share needed for 70% overall: {share_new:.2f}")
assert abs(share_new - 0.20) < 1e-12
old_n, new_n = round(n_fraud * (1 - share_new)), round(n_fraud * share_new)
caught_old, caught_new = old_n * catch_old, new_n * catch_new
caught_old, caught_new = round(caught_old), round(caught_new)
assert (old_n, new_n, caught_old, caught_new) == (800, 200, 680, 20)
overall = (caught_old + caught_new) / n_fraud
assert abs(overall - 0.70) < 1e-12
print(f"old {old_n} cases, caught {caught_old:.0f}; new {new_n} cases, caught {caught_new:.0f}; overall {overall:.0%}")

# Is the drop real? Two catch rates, 1,000 cases each (previous quarter vs this quarter)
p1, p2, n = 0.85, 0.70, 1000
pool = (p1 + p2) / 2
z = (p1 - p2) / np.sqrt(pool * (1 - pool) * 2 / n)
print(f"z for 85% -> 70% with n=1000 each: {z:.1f}")
assert z > 7

# Naive retrain on 'recent flagged cases': fraud labels only exist where we flagged (or chargebacks come later)
flagged_fraud = caught_old + caught_new
share_new_in_flagged = caught_new / flagged_fraud
print(f"new tactic is {share_new:.0%} of real fraud but {share_new_in_flagged:.1%} of flagged fraud")
assert round(share_new_in_flagged, 3) == 0.029
# the model learns the old pattern even more strongly; the 180 missed new-tactic cases look like normal traffic
missed_new = new_n - caught_new
print("new-tactic fraud labelled as legitimate in a flagged-only training set:", int(missed_new))
assert missed_new == 180

# Fix: add a random audit sample. Auditing 2,000 of 200,000 transactions (1%) at a 0.5% fraud base rate
rng = np.random.default_rng(25)
audit = rng.binomial(1, 0.005, 2000)
print("random audit finds", audit.sum(), "fraud cases in 2,000 reviewed (expected about 10)")
assert 3 <= audit.sum() <= 20
