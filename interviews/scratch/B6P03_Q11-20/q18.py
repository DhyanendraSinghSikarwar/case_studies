# Q18: raw agreement versus chance-adjusted agreement (illustrative)
import numpy as np
rng = np.random.default_rng(18)
n, agree, urgent_a, urgent_b = 1_000, 820, 300, 300
# 2x2 table: both urgent x, A only a_only, B only b_only, neither
x = (urgent_a + urgent_b - (n - agree)) // 2          # both = (300+300-180)/2
a_only, b_only = urgent_a - x, urgent_b - x
neither = n - x - a_only - b_only
print("both urgent", x, " A only", a_only, " B only", b_only, " neither", neither)
assert (x, a_only, b_only, neither) == (210, 90, 90, 610) and x + neither == agree
po = agree / n
pe = (urgent_a / n) * (urgent_b / n) + (1 - urgent_a / n) * (1 - urgent_b / n)
kappa = (po - pe) / (1 - pe)
print(f"observed {po:.3f}  chance {pe:.3f}  kappa {kappa:.3f}")
assert round(pe, 2) == 0.58 and round(kappa, 3) == 0.571
# positive-class agreement: 2*both / (A urgent + B urgent)
pos_agree = 2 * x / (urgent_a + urgent_b); neg_agree = 2 * neither / ((n - urgent_a) + (n - urgent_b))
print(f"agreement on 'urgent' {pos_agree:.2f}, on 'not urgent' {neg_agree:.2f}")
assert round(pos_agree, 2) == 0.70
# bootstrap interval for kappa
cells = np.array([x, a_only, b_only, neither]); labs = np.repeat(np.arange(4), cells)
ks = []
for _ in range(2_000):
    s = rng.choice(labs, n); c = np.bincount(s, minlength=4)
    p_o = (c[0] + c[3]) / n; ua, ub = (c[0] + c[1]) / n, (c[0] + c[2]) / n
    p_e = ua * ub + (1 - ua) * (1 - ub); ks.append((p_o - p_e) / (1 - p_e))
lo, hi = np.percentile(ks, [2.5, 97.5]); print(f"bootstrap 95% interval for kappa: {lo:.2f} to {hi:.2f}")
assert lo < kappa < hi
# the trap: 5% prevalence, 92% agreement
pe2 = 0.05 ** 2 + 0.95 ** 2; k2 = (0.92 - pe2) / (1 - pe2)
print(f"5% urgent each, 92% raw agreement: chance {pe2:.3f}, kappa {k2:.3f}")
assert round(k2, 3) == 0.158
# forming labels: keep the 820 agreed rows, send the 180 disagreements to a third, senior reviewer
print("rows to adjudicate:", n - agree, f"= {(n - agree) / n:.0%} of the sample; extra labels needed: {n - agree}")
# if instead one annotator is picked at random for the 180, expected wrong labels among them is half if one is right
print("expected wrong labels if we pick a random annotator on the disagreements:", (n - agree) // 2)
