import math
# Illustrative numbers.
apps, approved = 50_000, 20_000
declined = apps - approved
print("approval rate", approved / apps, "declined", declined)
assert approved / apps == 0.40 and declined == 30_000
pilot, defaults = 2000, 360
p = defaults / pilot
earn, lose = 150.0, 600.0
profit = (1 - p) * earn - p * lose
print(f"pilot default rate {p:.1%}, expected profit per loan {profit:+.2f}, pilot total {profit*pilot:+,.0f}")
assert p == 0.18 and round(profit, 2) == 15.00
# Break-even PD for this loan economics
be = earn / (earn + lose)
print(f"break-even PD {be:.1%}")
assert be == 0.2
# Normal and Wilson intervals
se = math.sqrt(p * (1 - p) / pilot)
lo, hi = p - 1.96 * se, p + 1.96 * se
z = 1.96
c = (p + z*z/(2*pilot)) / (1 + z*z/pilot)
h = z * math.sqrt(p*(1-p)/pilot + z*z/(4*pilot**2)) / (1 + z*z/pilot)
wlo, whi = c - h, c + h
print(f"normal 95%: {lo:.2%}-{hi:.2%}; Wilson 95%: {wlo:.2%}-{whi:.2%}")
assert round(lo, 3) == 0.163 and round(hi, 3) == 0.197
def prof(q): return (1 - q) * earn - q * lose
print(f"profit per loan at interval ends: {prof(hi):+.2f} to {prof(lo):+.2f}")
assert round(prof(hi), 2) == 2.37 and round(prof(lo), 2) == 27.63
# Model predicted 8% for them. Is 18% different?
zscore = (p - 0.08) / math.sqrt(0.08 * 0.92 / pilot)
print(f"z versus the model's 8%: {zscore:.1f}")
assert zscore > 10
# Blended default rate if declined pool behaves like the pilot
blend = (approved * 0.06 + declined * p) / apps
print(f"all applicants default rate: {blend:.1%}  (approved-only view said 6.0%)")
assert round(blend, 3) == 0.132
# Reject inference weights from the random pilot: each pilot loan stands for declined/pilot loans
w = declined / pilot
print("weight per pilot loan:", w)
assert w == 15
# Effective sample size cost of weighting: pilot is only 2,000 rows
print("training rows: 20,000 approved (weight 1) + 2,000 pilot (weight 15 = represents 30,000)")
# The 15 is before funding, servicing and collection costs. Illustrative 20 per loan of such costs flips the sign.
print("profit per loan after an illustrative 20 of funding+servicing cost:", round(profit - 20, 2))
assert round(profit - 20, 2) == -5.00
