# Q21 triage sizing (all numbers illustrative; the 2% is a sample estimate)
from statistics import NormalDist
N = NormalDist()
consults, urgent_rate, recall_target, cap = 30_000, 0.02, 0.95, 3_000
urgent = round(consults * urgent_rate)
must_catch = round(urgent * recall_target)
min_precision = must_catch / cap
assert urgent == 600 and must_catch == 570 and min_precision == 0.19
print(f"urgent/day={urgent}, true urgent in flags >= {must_catch}, min precision at a full queue = {min_precision:.0%}")

# Flag rate and the false-positive room inside the queue
flag_rate = cap / consults
fp_room = cap - must_catch
non_urgent = consults - urgent
max_fpr = fp_room / non_urgent
assert flag_rate == 0.10 and fp_room == 2_430 and abs(max_fpr - 0.08265) < 1e-4
print(f"flag rate={flag_rate:.0%}, false flags allowed={fp_room}, max false-positive rate={max_fpr:.2%}")

# Model assumption (equal-variance binormal scores): what separation does that need?
d = N.inv_cdf(recall_target) + N.inv_cdf(1 - max_fpr)
auc = N.cdf(d / 2 ** 0.5)
assert abs(d - 3.03) < 0.01 and abs(auc - 0.984) < 0.002
print(f"needed d'={d:.2f}, implied AUC={auc:.3f} (binormal assumption, a rough guide only)")

# The 2% is a sample. Suppose (invented) the audit had 1,000 consults.
n_audit = 1_000
se = (urgent_rate * (1 - urgent_rate) / n_audit) ** 0.5
lo, hi = urgent_rate - 1.96 * se, urgent_rate + 1.96 * se
u_lo, u_hi = consults * lo, consults * hi
p_lo, p_hi = recall_target * u_lo / cap, recall_target * u_hi / cap
assert abs(se - 0.004427) < 1e-5 and round(u_lo) == 340 and round(u_hi) == 860
assert abs(p_lo - 0.1077) < 1e-3 and abs(p_hi - 0.2724) < 1e-3
print(f"2% +/- {1.96*se:.2%} -> urgent {u_lo:.0f}..{u_hi:.0f}/day -> min precision {p_lo:.1%}..{p_hi:.1%}")
# If urgency were 3% instead of 2%
hits3 = consults * 0.03 * recall_target
assert round(hits3) == 855 and abs(hits3 / cap - 0.285) < 1e-9
print(f"if urgency is 3%: hits needed={hits3:.0f}, precision floor={hits3/cap:.1%}")
