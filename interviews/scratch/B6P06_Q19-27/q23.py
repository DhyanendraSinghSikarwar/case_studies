rev0, rev1 = 1_000_000, 1_120_000
u0, u1 = 50_000, 56_000
g_rev, g_u = rev1/rev0 - 1, u1/u0 - 1
a0, a1 = rev0/u0, rev1/u1
print(f"revenue {g_rev:+.1%}, users {g_u:+.1%}, revenue per user {a0:.2f} -> {a1:.2f} ({a1/a0-1:+.1%})")
assert abs(g_rev - 0.12) < 1e-12 and abs(g_u - 0.12) < 1e-12 and a0 == a1 == 20.0
# decomposition: revenue change = users effect (at old ARPU) + ARPU effect (on new users)
users_effect = (u1 - u0) * a0
arpu_effect = (a1 - a0) * u1
print(f"change {rev1-rev0:,}: from more users {users_effect:,.0f}, from higher revenue per user {arpu_effect:,.0f}")
assert users_effect + arpu_effect == rev1 - rev0 == 120_000 and arpu_effect == 0
# what if rounding hid a mix change? same totals can hide two segments moving opposite ways (illustrative)
seg0 = {"old users": (40_000, 22.0), "new users": (10_000, 12.0)}
seg1 = {"old users": (40_000, 22.0), "new users": (16_000, 14.5)}
r0 = sum(u*a for u, a in seg0.values()); r1 = sum(u*a for u, a in seg1.values())
print(f"segment illustration: revenue {r0:,.0f} -> {r1:,.0f} ({r1/r0-1:+.1%}), users {50000} -> {56000}")
assert r0 == 1_000_000 and r1 == 1_112_000
