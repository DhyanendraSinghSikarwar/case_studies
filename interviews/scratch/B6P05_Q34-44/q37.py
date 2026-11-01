mix = {"Basic": 0.50, "Standard": 0.35, "Premium": 0.15}
price = {"Basic": 5, "Standard": 8, "Premium": 12}
cost = {"Basic": 3.0, "Standard": 4.5, "Premium": 8.0}
m = {k: price[k] - cost[k] for k in mix}
assert m == {"Basic": 2.0, "Standard": 3.5, "Premium": 4.0}
before = sum(mix[k] * m[k] for k in mix)
basic = mix["Basic"] + 0.35 * 0.60
prem = mix["Premium"] + 0.35 * 0.30
cancel = 0.35 * 0.10
after = basic * m["Basic"] + prem * m["Premium"]
rev_b = sum(mix[k] * price[k] for k in mix)
rev_a = basic * 5 + prem * 12
print(f"blended margin before {before:.3f}; after {after:.3f}; change {after-before:+.3f} ({after/before-1:+.1%})")
print(f"mix after: Basic {basic:.3f}, Premium {prem:.3f}, cancelled {cancel:.3f}")
print(f"revenue per original customer {rev_b:.3f} -> {rev_a:.3f}")
assert abs(before - 2.825) < 1e-9 and abs(after - 2.44) < 1e-9
assert abs(basic - 0.71) < 1e-9 and abs(prem - 0.255) < 1e-9 and abs(cancel - 0.035) < 1e-9
assert abs(basic + prem + cancel - 1) < 1e-9
# what Premium take-up would break even if cancel stays at 10%
# move share s to Premium, 0.9-s to Basic
for s in (0.30, 0.40, 0.50, 0.60):
    a = (0.50 + 0.35 * (0.9 - s)) * 2 + (0.15 + 0.35 * s) * 4
    print(f"  Standard->Premium share {s:.0%}: margin {a:.3f}")
s_be = None
for i in range(0, 901):
    s = i / 1000
    a = (0.50 + 0.35 * (0.9 - s)) * 2 + (0.15 + 0.35 * s) * 4
    if a >= before: s_be = s; break
print(f"break-even Premium share (cancel 10%): {s_be}")
assert s_be == 0.85
print("so 85% of Standard customers (not 30%) would have to trade up to Premium")
