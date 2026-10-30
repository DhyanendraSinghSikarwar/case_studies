# Q23: price cut 20 -> 18, units 1,000 -> 1,150, unit cost 12 (illustrative numbers)
p0, p1, u0, u1, c = 20.00, 18.00, 1000, 1150, 12.00
rev0, rev1 = p0 * u0, p1 * u1
gp0, gp1 = (p0 - c) * u0, (p1 - c) * u1
print("revenue", rev0, "->", rev1, "change", rev1 - rev0, f"({(rev1/rev0-1)*100:.1f}%)")
print("gross profit", gp0, "->", gp1, "change", gp1 - gp0, f"({(gp1/gp0-1)*100:.1f}%)")
assert (rev0, rev1, gp0, gp1) == (20000.0, 20700.0, 8000.0, 6900.0)

# unit margin and the units needed just to stand still on profit
m0, m1 = p0 - c, p1 - c
be_units = gp0 / m1
print("unit margin", m0, "->", m1, f"({(m1/m0-1)*100:.0f}%); units needed to keep profit = {be_units:.1f} (+{(be_units/u0-1)*100:.1f}%)")
assert m0 == 8 and m1 == 6 and abs(be_units - 1333.33) < 0.01

# elasticity (point, using the old base) and the profit threshold p/(p-c)
e = ((u1 - u0) / u0) / ((p1 - p0) / p0)
thr = p0 / (p0 - c)
print(f"elasticity {e:.2f}; revenue rises if |e|>1, profit rises only if |e| > p/(p-c) = {thr:.2f}")
assert abs(e + 1.5) < 1e-9 and abs(thr - 2.5) < 1e-9 and abs(e) > 1 and abs(e) < thr

# sensitivity: what unit volume would make the cut profitable, and what if cost were 8?
for cost in (12.0, 8.0):
    need = (p0 - cost) * u0 / (p1 - cost)
    print(f"cost {cost}: units needed at price 18 to match old profit = {need:.0f}; actual 1,150 -> profit change {(p1-cost)*u1-(p0-cost)*u0:+.0f}")
assert (p1 - 8) * u1 - (p0 - 8) * u0 == 11500 - 12000
