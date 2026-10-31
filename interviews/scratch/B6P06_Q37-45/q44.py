# Q44: cost of thresholds X and Y (prompt numbers; fractions of items rounded at the end)
pos = 2000
cost_fn, cost_fp = 50, 5
def cost(recall, precision, rnd=False):
    tp = recall * pos
    fn = pos - tp
    flagged = tp / precision
    fp = flagged - tp
    if rnd: fn, fp, flagged = round(fn), round(fp), round(flagged)
    return fn, fp, flagged, fn * cost_fn + fp * cost_fp
for name, r, p in (("X", 0.60, 0.90), ("Y", 0.80, 0.70)):
    fn, fp, fl, c = cost(r, p)
    print(f"{name}: FN {fn:.0f}, FP {fp:.2f}, flagged {fl:.2f}, cost {c:,.2f}")
    fn2, fp2, fl2, c2 = cost(r, p, rnd=True)
    print(f"   rounded: FN {fn2}, FP {fp2}, flagged {fl2}, cost {c2:,}")
cx, cy = cost(0.6, 0.9)[3], cost(0.8, 0.7)[3]
assert abs(cx - 40666.67) < 0.01 and abs(cy - 23428.57) < 0.01
assert cost(0.6, 0.9, True)[3] == 40665 and cost(0.8, 0.7, True)[3] == 23430
print(f"Y is cheaper by {cx-cy:,.2f}")
# break-even miss:false-flag cost ratio r (FP cost fixed at 5)
fnx, fpx, _, _ = cost(0.6, 0.9); fny, fpy, _, _ = cost(0.8, 0.7)
r = (fpy - fpx) / (fnx - fny)
print(f"break-even FN:FP cost ratio = {r:.3f} (prompt ratio is 10)")
assert abs(r - 1.381) < 0.001 and 50 / 5 > r
print("review load: X flags", round(cost(0.6,0.9)[2]), "items, Y flags", round(cost(0.8,0.7)[2]))
