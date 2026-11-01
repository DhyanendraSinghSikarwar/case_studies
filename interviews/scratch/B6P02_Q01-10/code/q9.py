# Q9 precision fell 67% -> 50% while recall and FPR are unchanged (numbers from the prompt)
from scipy.stats import norm
N = 1_000_000
recall, fpr = 0.70, 0.0056

def confusion(pi):
    pos = N * pi; neg = N - pos
    tp = recall * pos; fp = fpr * neg
    return pos, tp, fp, tp / (tp + fp)

for pi in (0.016, 0.008):
    pos, tp, fp, prec = confusion(pi)
    print(f"fraud rate {pi:.1%}: frauds {pos:,.0f}, TP {tp:,.0f}, FP {fp:,.0f}, flagged {tp+fp:,.0f}, precision {prec:.1%}")
p0 = confusion(0.016)[3]; p1 = confusion(0.008)[3]
assert round(p0 * 100) == 67 and round(p1 * 100) == 50

# Does 'about 0.56%' FPR match 67% precision exactly?
fpr_implied = recall * 0.016 * (1 - 0.67) / (0.67 * (1 - 0.016))
print(f"FPR implied by 67% precision: {fpr_implied:.4%}")
assert abs(fpr_implied - 0.0056) < 0.00005

# To get 67% precision back at the new fraud rate, the threshold must be stricter.
# Equal-variance binormal score model (assumption), calibrated so recall 70% at FPR 0.56%:
from scipy.optimize import brentq
thr0 = norm.ppf(1 - fpr)
mu = thr0 - norm.ppf(1 - recall)
print(f"binormal separation implied: {mu:.2f}")
def recall_at(f): return 1 - norm.cdf(norm.ppf(1 - f) - mu)
pi = 0.008
def prec_at(f): return recall_at(f) * pi / (recall_at(f) * pi + f * (1 - pi))
assert abs(recall_at(fpr) - 0.70) < 1e-9 and abs(prec_at(fpr) - p1) < 1e-9
fpr_need = brentq(lambda f: prec_at(f) - 0.67, 1e-5, 0.0056)
r_new = recall_at(fpr_need)
print(f"FPR needed for 67% precision at fraud rate 0.8%: {fpr_need:.3%}; recall then {r_new:.1%}")
assert 0.0023 < fpr_need < 0.0027 and 0.56 < r_new < 0.60
tp_lost = (0.70 - r_new) * N * pi
print(f"frauds missed extra per million transactions: {tp_lost:,.0f}")
assert 800 < tp_lost < 1000

# Cost view (invented): a missed fraud costs Rs 4,000, a review costs Rs 60
for name, f in (("current threshold", fpr), ("stricter threshold", fpr_need)):
    rec = recall_at(f)
    cost = (1 - rec) * N * pi * 4000 + f * N * (1 - pi) * 60
    print(f"{name}: expected cost Rs {cost:,.0f}")
