gmv, t0, t1, drop = 200e6, 0.10, 0.12, 0.08
r0 = gmv * t0
r1 = gmv * (1 - drop) * t1
print(f"revenue now {r0/1e6:.2f}m; new {r1/1e6:.2f}m ({r1/r0-1:+.1%}, {(r1-r0)/1e6:+.2f}m)")
assert abs(r0 - 20e6) < 1 and abs(r1 - 22.08e6) < 1
be_drop = 1 - t0 / t1
print(f"break-even GMV drop = 1 - 10/12 = {be_drop:.2%}; GMV at break-even {gmv*(1-be_drop)/1e6:.1f}m")
assert abs(be_drop - 1/6) < 1e-12
print(f"implied 'elasticity' of GMV to take rate: {(-drop)/(t1/t0-1):.2f}; break-even {(-be_drop)/(t1/t0-1):.2f}")
assert abs(drop / (t1 / t0 - 1) - 0.4) < 1e-12 and abs(be_drop / (t1 / t0 - 1) - 0.8333) < 1e-3
# contribution view: variable cost 2% of GMV (payment fees etc.), illustrative
v = 0.02
c0 = gmv * (t0 - v)
c1 = gmv * (1 - drop) * (t1 - v)
be2 = 1 - (t0 - v) / (t1 - v)
print(f"with variable cost {v:.0%} of GMV: contribution {c0/1e6:.1f}m -> {c1/1e6:.2f}m; break-even drop {be2:.1%}")
assert abs(be2 - 0.2) < 1e-12 and abs(c1 - 18.4e6) < 1
# table of outcomes
for d in (0.05, 0.08, 0.12, 0.167, 0.20):
    print(f"  drop {d:5.1%}: revenue {gmv*(1-d)*t1/1e6:5.2f}m")
assert gmv * (1 - 0.20) * t1 < r0 < gmv * (1 - 0.12) * t1
