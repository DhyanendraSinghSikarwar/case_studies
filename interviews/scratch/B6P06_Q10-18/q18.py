# Q18: launch plan under a 4-week deadline (illustrative value model)
launch_w, backlog_w, integ_w = 4, 6, 1
auc = {"none": 0.74, "proxy": 0.77, "real": 0.80}
print("gap to real feature:", backlog_w - launch_w, "weeks (+", integ_w, "week to integrate) -> real live at week", backlog_w + integ_w)
assert backlog_w - launch_w == 2
# share of the possible lift (0.74 -> 0.80) the proxy gives
share = (auc["proxy"] - auc["none"]) / (auc["real"] - auc["none"])
print("proxy delivers", round(share, 2), "of the AUC lift")
assert round(share, 2) == 0.50
# assumption: weekly value proportional to (AUC - 0.5); full model worth 100/week (invented)
def v(a): return 100 * (a - 0.5) / (auc["real"] - 0.5)
for k in auc: print(" weekly value", k, round(v(auc[k]), 1))
H = 12   # horizon in weeks
# plan A: wait for real feature, launch week 7
A = (H - (backlog_w + integ_w)) * v(auc["real"])
# plan B: launch proxy week 4, swap in real at week 7
B = (backlog_w + integ_w - launch_w) * v(auc["proxy"]) + (H - (backlog_w + integ_w)) * v(auc["real"])
# plan C: launch week 4 with neither
C = (backlog_w + integ_w - launch_w) * v(auc["none"]) + (H - (backlog_w + integ_w)) * v(auc["real"])
print("12-week value: A wait", round(A), "| B proxy then real", round(B), "| C no feature then real", round(C))
assert round(A) == 500 and round(B) == 770 and round(C) == 740
# AUC differences are noisy: if two AUCs are from 5,000 positives and negatives each, SE about 0.004
import math
n1 = n0 = 5000; a = 0.77
q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
se = math.sqrt((a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n0 - 1) * (q2 - a * a)) / (n1 * n0))
print("approx SE of one AUC at 0.77, 5,000+5,000:", round(se, 4))
assert se < 0.01
