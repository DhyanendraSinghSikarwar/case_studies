# Q10: AOV fell 15% while orders rose 9% (illustrative, orders per 1,000 base)
q1 = {"existing": (800, 600), "new": (200, 200)}    # (orders, AOV Rs)
q2 = {"existing": (760, 560), "new": (330, 170)}

def tot(q):
    o = sum(v[0] for v in q.values()); rev = sum(v[0] * v[1] for v in q.values())
    return o, rev, rev / o
o1, r1, a1 = tot(q1); o2, r2, a2 = tot(q2)
print(f"Q1: orders {o1}, GMV Rs {r1:,}, AOV Rs {a1:.0f}")
print(f"Q2: orders {o2}, GMV Rs {r2:,}, AOV Rs {a2:.1f}")
print(f"orders {o2/o1-1:+.1%}, AOV {a2/a1-1:+.1%}, GMV {r2/r1-1:+.1%}")
assert a1 == 520 and round(a2) == 442 and round(o2 / o1 - 1, 2) == 0.09
assert round(r2 / r1 - 1, 3) == -0.074

# AOV change = within-segment (price/basket) effect + mix effect
share1 = {k: v[0] / o1 for k, v in q1.items()}
share2 = {k: v[0] / o2 for k, v in q2.items()}
within = sum(share1[k] * (q2[k][1] - q1[k][1]) for k in q1)     # old mix, new AOVs
mix = sum((share2[k] - share1[k]) * q2[k][1] for k in q1)        # new share, new AOVs
print(f"within-segment effect Rs {within:+.1f}, mix effect Rs {mix:+.1f}, total Rs {within+mix:+.1f} (actual {a2-a1:+.1f})")
assert abs(within + mix - (a2 - a1)) < 1e-9
print(f"new-user share of orders: {share1['new']:.0%} -> {share2['new']:.0%}")
print(f"mix is {mix/(a2-a1):.0%} of the AOV fall")
