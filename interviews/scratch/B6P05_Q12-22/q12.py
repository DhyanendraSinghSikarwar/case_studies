# Illustrative numbers. Surge arithmetic with a supply cap.
base_req, base_sup, base_fare = 120, 80, 10.0
def rev(req, sup, fare):
    done = min(req, sup)          # completed rides cannot exceed requests or driver capacity
    return done, done * fare
d0, r0 = rev(base_req, base_sup, base_fare)
print("base", d0, r0)
assert (d0, r0) == (80, 800)
req1, sup1, fare1 = 120 * 0.80, 80 * 1.10, 15.0
assert round(req1) == 96 and round(sup1) == 88
d1, r1 = rev(req1, sup1, fare1)
print("team case", d1, r1, f"{r1/r0-1:+.0%}")
assert (round(d1), round(r1), round(r1/r0 - 1, 2)) == (88, 1320, 0.65)   # arithmetic is right
# What could shrink it? One change at a time, then together.
cases = {
 "team case":                    (96, 88, 15.0),
 "riders drop 35% not 20%":      (78, 88, 15.0),
 "supply +0% (slow response)":   (96, 80, 15.0),
 "riders -35% and supply +0%":   (78, 80, 15.0),
}
for k, (rq, sp, f) in cases.items():
    d, r = rev(rq, sp, f)
    print(f"{k:30} rides {d:5.0f} revenue {r:7.1f} ({r/r0-1:+.0%})")
assert round(rev(78, 88, 15)[1]) == 1170 and round(rev(96, 80, 15)[1]) == 1200 and round(rev(78, 80, 15)[1]) == 1170
# Gross fare is not platform revenue. Illustrative: platform keeps 25% of the BASE fare only, drivers get the surge uplift.
take_base = 0.25 * 10.0
p0, p1 = d0 * take_base, d1 * take_base
print("platform keeps (25% of base fare):", p0, "->", p1, f"{p1/p0-1:+.0%}")
assert (p0, p1) == (200.0, 220.0)
# Break-even: how many rides can be lost before surge revenue equals base revenue at 1.5x?
be = r0 / 15.0
print(f"surge revenue = base revenue when completed rides = {be:.2f} (a {be/80-1:+.1%} change from 80)")
assert round(be, 2) == 53.33
# Implied arc elasticity in the team case: -20% requests for +50% price
print("implied elasticity of requests", round(-0.20 / 0.50, 2))
# Unfilled requests
print("unfilled requests at 1.5x", 96 - 88, "vs base", 120 - 80)
assert (96 - 88, 120 - 80) == (8, 40)
