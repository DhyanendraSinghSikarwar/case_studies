import math
def wil(k, n, z=1.96):
    p = k/n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return c-h, c+h
n = 100
le, he = wil(91, n); lh, hh = wil(78, n)
print(f"English 91/100: {le:.4f} to {he:.4f}")
print(f"Hindi   78/100: {lh:.4f} to {hh:.4f}")
assert 0.837 < le < 0.839 and 0.951 < he < 0.953 and 0.688 < lh < 0.690 and 0.849 < hh < 0.851
print(f"intervals overlap: {lh < he and le < hh} (overlap {hh-le:.3f})")
assert hh > le
gap = 0.91-0.78
se = math.sqrt(.91*.09/n + .78*.22/n)
z = gap/se
p = math.erfc(z/math.sqrt(2))
print(f"gap {gap*100:.0f} points, z = {z:.2f}, two-sided p = {p:.4f}")
assert round(gap*100) == 13 and 2.5 < z < 2.65 and 0.008 < p < 0.012
# Newcombe hybrid interval for difference between two independent proportions
d_lo = gap - math.sqrt((0.91-le)**2 + (hh-0.78)**2)
d_hi = gap + math.sqrt((he-0.91)**2 + (0.78-lh)**2)
print(f"Newcombe 95% CI for the gap: {d_lo*100:.1f} to {d_hi*100:.1f} points")
assert 0.028 < d_lo < 0.030 and 0.21 < d_hi < 0.23
# how much grader error could move the gap? if the Hindi grader wrongly fails 6 correct answers
for err in (0, 3, 6, 10):
    g = 0.91 - (0.78+err/100)
    print(f"if {err} of Hindi's failures are grader mistakes: gap {g*100:.0f} points")
assert abs((0.91-0.84)-0.07) < 1e-12
# paired check design: if the same 100 questions were translated, count discordant pairs (invented)
print("paired design needed: McNemar on discordant pairs, not the two marginal rates")
n5 = 1.96**2*(.91*.09+.78*.22)/0.05**2
print(f"n per language for a gap CI half-width of 5 points: {n5:.0f}")
assert 385 < n5 < 395
