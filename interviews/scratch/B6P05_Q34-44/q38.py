import math
dash = 120 / 40 - 1
print(f"dashboard lift {dash:.0%}")
assert abs(dash - 2.0) < 1e-9
n = 20_000
itt = 44 - 42
join = 0.25
per_joiner = itt / join
margin_per_joiner = 0.30 * per_joiner
net_per_joiner = margin_per_joiner - 6
print(f"ITT {itt}; per joiner {per_joiner:.1f}; margin {margin_per_joiner:.1f}; after rewards {net_per_joiner:.1f}")
assert per_joiner == 8 and abs(margin_per_joiner - 2.4) < 1e-9 and abs(net_per_joiner + 3.6) < 1e-9
joiners = join * n
total = 0.30 * itt * n - 6 * joiners
print(f"quarter total: margin gain {0.30*itt*n:,.0f} - rewards {6*joiners:,.0f} = {total:,.0f}")
assert round(0.30 * itt * n) == 12_000 and round(6 * joiners) == 30_000 and round(total) == -18_000
# uncertainty, ASSUMING revenue sd 80 per customer (illustrative)
sd = 80
se = sd * math.sqrt(2 / n)
lo, hi = itt - 1.96 * se, itt + 1.96 * se
print(f"se {se:.2f}; ITT 95% CI {lo:.2f} to {hi:.2f}; per joiner {lo/join:.1f} to {hi/join:.1f}")
print(f"best-case margin per joiner {0.30*hi/join:.2f} vs reward 6")
assert 0.30 * hi / join < 6
# break-even effect per joiner
be = 6 / 0.30
print(f"break-even revenue effect per joiner {be:.0f} a quarter; dashboard-style gap was {120-40}")
assert round(be) == 20
