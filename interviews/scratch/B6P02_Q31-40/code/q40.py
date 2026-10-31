# Q40: a fraud model that only learns from what it flags; random exploration slices (illustrative simulation)
import math
import numpy as np

rng = np.random.default_rng(40)
weeks, N = 12, 1_000_000
fraud_rate = 0.005
share_B = np.linspace(0.10, 0.50, weeks)          # new evasive fraud pattern grows
fp_rate = np.linspace(0.003, 0.001, weeks)        # model gets sharper on the easy cases
catch_A, catch_B = 0.92, 0.10

rows = []
for w in range(weeks):
    n_fraud = rng.binomial(N, fraud_rate)
    nB = rng.binomial(n_fraud, share_B[w]); nA = n_fraud - nB
    tpA = rng.binomial(nA, catch_A); tpB = rng.binomial(nB, catch_B)
    fp = rng.binomial(N - n_fraud, fp_rate[w])
    tp = tpA + tpB; flagged = tp + fp
    rows.append((n_fraud, tp, fp, flagged))
rows = np.array(rows)
prec = rows[:, 1] / rows[:, 3]; rec = rows[:, 1] / rows[:, 0]
print("week  apparent precision  true recall   missed fraud")
for w in (0, 5, 11):
    print(f"{w:>4}  {prec[w]:>17.1%}  {rec[w]:>11.1%}  {rows[w, 0] - rows[w, 1]:>12,}")
assert prec[-1] > prec[0] + 0.10 and rec[-1] < rec[0] - 0.25
assert (rows[-1, 0] - rows[-1, 1]) > 2 * (rows[0, 0] - rows[0, 1])

# Exploration 1: a random audit of unflagged transactions (label only, no extra fraud loss)
w = 11
unflag = N - rows[w, 3]; missed = rows[w, 0] - rows[w, 1]; p_u = missed / unflag
def n_for_rel_error(p, rel): return 1.96 ** 2 * (1 - p) / (rel ** 2 * p)
n_aud = n_for_rel_error(p_u, 0.20)
print(f"week 12 missed-fraud rate among unflagged {p_u:.4%}; audit size for +-20% relative error: {n_aud:,.0f} labels")
assert 35_000 < n_aud < 45_000
# repeat the audit many times at that size to check the claim
est = np.array([rng.binomial(round(n_aud), p_u) / round(n_aud) for _ in range(2000)])
cover = (np.abs(est - p_u) / p_u < 0.20).mean()
print(f"share of audits within +-20% of the truth: {cover:.1%}")
assert 0.93 < cover < 0.97
# recall estimate = TP / (TP + estimated missed)
rec_hat = rows[w, 1] / (rows[w, 1] + est.mean() * unflag)
print(f"recall estimate {rec_hat:.3f} vs true {rec[w]:.3f}")
assert abs(rec_hat - rec[w]) < 0.02

# Exploration 2: release a random share of flagged transactions (with a cap) to measure true precision
flagged = rows[w, 3]; tp = rows[w, 1]
n_rel = 1.96 ** 2 * prec[w] * (1 - prec[w]) / 0.05 ** 2
print(f"flagged {flagged:,}; releases needed for +-5 points on precision: {n_rel:,.0f} ({n_rel / flagged:.1%} of flagged)")
avg_loss = 3_000                                    # Rs per fraud transaction (illustrative)
cost_release = n_rel * prec[w] * avg_loss
cost_audit_review = n_aud * 20                      # Rs 20 per review (illustrative)
loss_week = missed * avg_loss
print(f"cost of releases Rs {cost_release:,.0f}; cost of audit reviews Rs {cost_audit_review:,.0f}; weekly missed-fraud loss Rs {loss_week:,.0f}")
assert (cost_release + cost_audit_review) < 0.25 * loss_week
print(f"exploration cost is {(cost_release + cost_audit_review) / loss_week:.1%} of one week of missed fraud")
