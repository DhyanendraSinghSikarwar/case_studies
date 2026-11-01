# Mix versus rate decomposition of a fall in mean score (illustrative segments)
seg = ["prime", "near_prime", "subprime"]
share0, mean0 = [0.40, 0.30, 0.30], [0.12, 0.30, 0.54]
share1, mean1 = [0.50, 0.30, 0.20], [0.092, 0.26, 0.48]
m0 = sum(s * m for s, m in zip(share0, mean0)); m1 = sum(s * m for s, m in zip(share1, mean1))
print(f"mean score last month {m0:.3f}, this month {m1:.3f}, change {m1-m0:+.3f}")
assert abs(m0 - 0.30) < 1e-9 and abs(m1 - 0.22) < 1e-9
mix = sum((s1 - s0) * m for s0, s1, m in zip(share0, share1, mean0))        # shares change, old means
rate = sum(s1 * (b - a) for s1, a, b in zip(share1, mean0, mean1))          # means change, new shares
print(f"mix effect {mix:+.3f} ({mix/(m1-m0):.0%}), within-segment effect {rate:+.3f} ({rate/(m1-m0):.0%})")
assert abs(mix + rate - (m1 - m0)) < 1e-12
assert abs(mix - (-0.042)) < 1e-12 and abs(rate - (-0.038)) < 1e-12
for sname, a, b in zip(seg, mean0, mean1):
    print(f"  {sname:10s} mean {a:.3f} -> {b:.3f}  ({b-a:+.3f})")
# Which segments carry the within-segment fall?
contrib = [s1 * (b - a) for s1, a, b in zip(share1, mean0, mean1)]
print("within-segment contributions:", [round(c, 3) for c in contrib])
assert all(c < 0 for c in contrib)     # fall is in every segment: points at pipeline/model/real improvement, not mix alone
print("asserts passed")
