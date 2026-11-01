# Q44: cost of thresholds X and Y (prompt numbers)
pos = 2000
cost_fn, cost_fp = 50, 5
def cost(recall, precision, rnd=False):
    tp = recall * pos
    fn = pos - tp
    flagged = tp / precision
    fp = flagged - tp
    if rnd: fn, fp, flagged = round(fn), round(fp), round(flagged)
    return fn, fp, flagged, fn * cost_fn + fp * cost_fp
for name, r, p in (("X", 0.60, 0.80), ("Y", 0.75, 0.75)):
    fn, fp, fl, c = cost(r, p)
    print(f"{name}: FN {fn:.0f}, FP {fp:.2f}, flagged {fl:.2f}, cost {c:,.2f}")
cx, cy = cost(0.6, 0.8)[3], cost(0.75, 0.75)[3]
assert cost(0.6, 0.8)[:3] == (800, 300, 1500) and cx == 41_500
assert cost(0.75, 0.75)[:3] == (500, 500, 2000) and cy == 27_500
print(f"Y is cheaper by {cx-cy:,.0f}")
# break-even miss:false-flag cost ratio r (FP cost fixed at 5)
fnx, fpx, _, _ = cost(0.6, 0.8); fny, fpy, _, _ = cost(0.75, 0.75)
r = (fpy - fpx) / (fnx - fny)
print(f"break-even FN:FP cost ratio = {r:.3f} (prompt ratio is 10)")
assert abs(r - 2/3) < 1e-9 and 50 / 5 > r
print("review load: X flags", round(cost(0.6,0.8)[2]), "items, Y flags", round(cost(0.75,0.75)[2]))
# sensitivity: if a false flag cost 100 and a miss 50 (ratio 0.5), X wins
def total(fn, fp, cfn, cfp): return fn*cfn + fp*cfp
assert total(800, 300, 50, 100) == 70_000 and total(500, 500, 50, 100) == 75_000
print("false flag 100, miss 50: X", total(800,300,50,100), "Y", total(500,500,50,100))
