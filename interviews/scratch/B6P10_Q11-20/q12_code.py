import math

# Prompt arithmetic: true fraud rate 0.2% (assumption), chargeback maturity 60% at day 30, 90% at day 90
true_rate = 0.002
mat = {30: 0.60, 90: 0.90}
apparent = {d: true_rate * m for d, m in mat.items()}
assert abs(apparent[30] - 0.0012) < 1e-12 and abs(apparent[90] - 0.0018) < 1e-12
for d in (30, 90):
    print(f"window aged {d} days: apparent fraud rate {apparent[d]:.4%} (true {true_rate:.2%}), understated by {1 - mat[d]:.0%}")

# Maturity correction: divide the observed rate by the maturity share (valid only if the delay profile is stable)
for d in (30, 90):
    assert abs(apparent[d] / mat[d] - true_rate) < 1e-12
print("corrected estimate from either window:", apparent[30] / mat[30])

# Label-lag trade-off for monthly retraining: freshest data with at least 90% matured labels is 90 days old
lag_days, retrain_days = 90, 30
print("training rows end", lag_days, "days before today; model is", lag_days + retrain_days // 2,
      "days behind on average between retrains")
assert lag_days + retrain_days // 2 == 105

# How many transactions to see enough frauds? Poisson relative error of a count c is about 1/sqrt(c)
target_frauds = 400                                # relative standard error 5%, about +-10% at 95%
assert abs(1 / math.sqrt(target_frauds) - 0.05) < 1e-12
tx_90 = target_frauds / apparent[90]               # transactions in a 90-day-old window
tx_30 = target_frauds / apparent[30]
print("transactions needed for 400 observed frauds: 90-day-old window", round(tx_90), "| 30-day-old window", round(tx_30))
assert round(tx_90) == 222_222 and round(tx_30) == 333_333
# The 12-week launch fits: 12 weeks = 84 days < 90 days, so the first model cannot use fully matured labels from its own traffic
assert 12 * 7 == 84 < 90
