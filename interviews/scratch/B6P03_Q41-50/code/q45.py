# Q45: a missing value whose meaning changed after a consent change. Illustrative numbers.
import math
U = 2_000_000
before, after = 0.08, 0.30
assert int(U * before) == 160_000 and int(U * after) == 600_000
extra = int(U * after) - int(U * before)
print(f"extra missing users: {extra:,}  ({after-before:.0%} of users)")
assert extra == 440_000

# Before: every missing last_login is a user who really has not logged in (or a tracking gap tied to inactivity).
# Illustrative churn rates: overall 10%, missing group 40%.
overall = 0.10; q_inactive = 0.40
q_present = (overall - before * q_inactive) / (1 - before)
print(f"churn among users WITH last_login (before): {q_present:.4f}")
assert round(q_present, 4) == 0.0739

# After: the same 8% truly inactive users, plus 22% who simply declined tracking and behave like present users.
consent_miss = after - before
q_missing_after = (before * q_inactive + consent_miss * q_present) / after
print(f"churn among missing (after): {q_missing_after:.4f}")
assert round(q_missing_after, 3) == 0.161
check_overall = after * q_missing_after + (1 - after) * q_present
assert abs(check_overall - overall) < 1e-12        # overall churn is unchanged by construction

# Old model is a lookup: missing -> 0.40, present -> q_present.
exp_pred_churners = after * U * q_inactive
actual_churners_missing = after * U * q_missing_after
print(f"missing users scored at 0.40: predicted churners {exp_pred_churners:,.0f} vs actual {actual_churners_missing:,.0f}")
assert round(exp_pred_churners) == 240_000 and round(actual_churners_missing) == 96_522

def logloss(groups):
    # groups: list of (share, true_rate, predicted_rate)
    return -sum(s * (t * math.log(p) + (1 - t) * math.log(1 - p)) for s, t, p in groups)

old = logloss([(after, q_missing_after, q_inactive), (1 - after, q_present, q_present)])
# fixed model uses the consent flag: [missing and consented -> inactive], [missing, declined -> like present], [present]
fixed = logloss([(before, q_inactive, q_inactive), (consent_miss, q_present, q_present), (1 - after, q_present, q_present)])
best_possible = logloss([(after, q_missing_after, q_missing_after), (1 - after, q_present, q_present)])
print(f"log loss after the change  old model: {old:.4f}   with consent flag: {fixed:.4f}")
assert fixed < old
# Note: with consent flag known, 'fixed' beats the model that only sees missing/present
print(f"log loss of a model that only sees 'missing' but is recalibrated: {best_possible:.4f}")
assert fixed < best_possible < old
