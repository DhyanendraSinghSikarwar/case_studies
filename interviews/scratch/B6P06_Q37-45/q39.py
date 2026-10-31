# Q39: honest ROI range for a 1.8M/yr team (illustrative)
cost = 1_800_000
claimed = 3_000_000
shared_share = 0.40
shared = claimed * shared_share
sole = claimed - shared
assert abs(shared - 1_200_000) < 1e-6 and abs(sole - 1_800_000) < 1e-6
def roi(b): return (b - cost) / cost
rows = [("claimed (everything)", claimed),
        ("sole only (floor)", sole),
        ("sole + half of shared", sole + 0.5 * shared)]
for name, b in rows:
    print(f"{name:24} benefit {b:>10,.0f}  net {b-cost:>10,.0f}  ROI {roi(b):6.1%}")
assert roi(claimed) > 0.66 and roi(claimed) < 0.67
assert roi(sole) == 0
assert abs(roi(sole + 0.5 * shared) - 1/3) < 1e-9
# how much of the shared 1.2M must we be credited to reach 25% ROI?
need = cost * 1.25 - sole
print(f"credit needed from shared pool for 25% ROI = {need:,.0f} of {shared:,.0f} ({need/shared:.0%})")
assert abs(need - 450_000) < 1e-6
