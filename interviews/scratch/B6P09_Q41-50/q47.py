# Q47: chargebacks as noisy fraud labels (prompt numbers, illustrative)
flagged, chargebacks, friendly = 1_000, 500, 0.30
assert chargebacks / flagged == 0.5
friendly_n = round(chargebacks * friendly)
true_fraud_cb = chargebacks - friendly_n
no_cb = flagged - chargebacks
print("flagged:", flagged, "= true-fraud chargebacks", true_fraud_cb, "+ friendly-fraud chargebacks", friendly_n, "+ no chargeback", no_cb)
assert (true_fraud_cb, friendly_n, no_cb) == (350, 150, 500)
print("measured precision (chargeback rate):", chargebacks / flagged)
print("true-fraud share of flagged (30% applies to the 500):", true_fraud_cb / flagged)
assert true_fraud_cb / flagged == 0.35
# the 500 flagged with no chargeback are unobserved: some could be real fraud nobody disputed
lo = true_fraud_cb / flagged
for share_undisputed_fraud in (0.0, 0.1, 0.5, 1.0):
    p = (true_fraud_cb + share_undisputed_fraud * no_cb) / flagged
    print(f"if {share_undisputed_fraud:.0%} of the no-chargeback flags were real fraud -> true-fraud share {p:.0%}")
assert (true_fraud_cb + 1.0 * no_cb) / flagged == 0.85
print("so the true-fraud share is 35% at the minimum under this reading, up to 85% at the extreme; it is not pinned down")
# friendly fraud in the flagged set is 15% of flagged: treating them as 'fraud' customers
print("friendly-fraud customers as share of flagged:", friendly_n / flagged)
assert friendly_n / flagged == 0.15

# chargebacks count friendly disputes as fraud, so the measured precision overstates the true-fraud share by:
print("measured minus true precision (points):", round((chargebacks / flagged - true_fraud_cb / flagged) * 100))
assert round((chargebacks / flagged - true_fraud_cb / flagged) * 100) == 15
