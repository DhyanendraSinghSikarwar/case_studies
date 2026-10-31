extra_ms = 80 - 25
pen = extra_ms / 10 * 0.3
print(f"extra latency {extra_ms} ms -> conversion penalty {pen:.2f}%")
assert extra_ms == 55 and round(pen, 2) == 1.65
net_add = 1.2 - pen
net_mul = (1.012 * (1 - pen/100) - 1) * 100
print(f"net (additive) {net_add:+.2f}%, net (compounded) {net_mul:+.2f}%")
assert round(net_add, 2) == -0.45 and round(net_mul, 2) == -0.47
# break-even latency for A
be_ms = 25 + 1.2 / 0.3 * 10
print(f"A breaks even at p95 {be_ms:.0f} ms")
assert be_ms == 65
# A tuned down to the 50 ms budget, keeping its CTR gain
net_50 = 1.2 - (50 - 25) / 10 * 0.3
print(f"A at 50 ms: {net_50:+.2f}%")
assert round(net_50, 2) == 0.45
# if only 60% of the CTR gain turns into conversions (illustrative pass-through)
net_pt = 0.6 * 1.2 - pen
print(f"with 60% CTR pass-through: {net_pt:+.2f}%")
assert round(net_pt, 2) == -0.93
