# Q28: take rate 12% -> 15% (illustrative, millions)
gmv_top, gmv_oth, tr0, tr1 = 40.0, 60.0, 0.12, 0.15
rev0 = tr0 * (gmv_top + gmv_oth)
top1, oth1 = gmv_top * (1 - 0.25), gmv_oth * (1 - 0.03)
rev1 = tr1 * (top1 + oth1)
print(f"before: GMV {gmv_top+gmv_oth:.1f}, revenue {rev0:.2f}")
print(f"after: top {top1:.1f}, others {oth1:.1f}, GMV {top1+oth1:.1f} ({(top1+oth1)/100-1:+.1%}), revenue {rev1:.3f} ({rev1/rev0-1:+.2%})")
assert abs(rev0 - 12.0) < 1e-9 and top1 == 30.0 and abs(oth1 - 58.2) < 1e-9 and abs(rev1 - 13.23) < 1e-9

# break-even top-seller loss (others -3%) for revenue to stay at 12.0
x = 1 - (rev0 / tr1 - oth1) / gmv_top
print(f"revenue is flat if top-seller GMV falls {x:.1%} (others -3%)")
assert abs(x - 0.455) < 1e-3
# break-even uniform GMV loss
u = 1 - rev0 / (tr1 * 100)
print(f"or if GMV falls {u:.0%} across everyone")
assert abs(u - 0.20) < 1e-9

# sensitivity of revenue to the top-seller loss
for loss in (0.25, 0.35, 0.455, 0.60):
    r = tr1 * (gmv_top * (1 - loss) + oth1)
    print(f"  top sellers -{loss:.1%}: revenue {r:.2f} ({r/rev0-1:+.1%})")
assert tr1 * (gmv_top * (1 - 0.60) + oth1) < rev0

# if top-seller loss also drags other sellers' GMV (buyers who came for the top sellers leave): others -3% -> -15%
r2 = tr1 * (top1 + gmv_oth * 0.85)
print(f"top -25% and others -15%: revenue {r2:.2f} ({r2/rev0-1:+.1%})")
assert abs(r2 - 0.15 * (30 + 51)) < 1e-9 and r2 > rev0
# share of take from top sellers, and the margin they keep
print(f"top sellers pay {tr0*gmv_top:.2f} of 12.00 now ({tr0*gmv_top/rev0:.0%}) and {tr1*top1:.2f} of {rev1:.2f} after ({tr1*top1/rev1:.0%})")
