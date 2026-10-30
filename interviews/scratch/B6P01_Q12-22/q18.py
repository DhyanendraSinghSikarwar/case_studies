# Illustrative: user shares and ARPU (Rs) by country
shares0 = {"A": 0.30, "B": 0.30, "C": 0.40}
shares1 = {"A": 0.20, "B": 0.30, "C": 0.50}
arpu0   = {"A": 200.0, "B": 100.0, "C": 55.0}
arpu1   = {"A": 210.0, "B": 105.0, "C": 61.0}
tot0 = sum(shares0[k] * arpu0[k] for k in arpu0)
tot1 = sum(shares1[k] * arpu1[k] for k in arpu1)
print(f"company ARPU {tot0:.1f} -> {tot1:.1f}")
assert round(tot0, 6) == 112 and round(tot1, 6) == 104
for k in arpu0:
    print(k, f"share {shares0[k]:.0%}->{shares1[k]:.0%}  ARPU {arpu0[k]:.0f}->{arpu1[k]:.0f} ({arpu1[k] / arpu0[k] - 1:+.1%})")
    assert arpu1[k] > arpu0[k]
d = tot1 - tot0
# Convention 1: within at OLD shares, mix at NEW ARPU
within1 = sum(shares0[k] * (arpu1[k] - arpu0[k]) for k in arpu0)
mix1 = sum((shares1[k] - shares0[k]) * arpu1[k] for k in arpu0)
# Convention 2: within at NEW shares, mix at OLD ARPU
within2 = sum(shares1[k] * (arpu1[k] - arpu0[k]) for k in arpu0)
mix2 = sum((shares1[k] - shares0[k]) * arpu0[k] for k in arpu0)
print(f"total change {d:+.1f}")
print(f"conv 1 (old-share weights): within {within1:+.1f}, mix {mix1:+.1f}, sum {within1 + mix1:+.1f}")
print(f"conv 2 (new-share weights): within {within2:+.1f}, mix {mix2:+.1f}, sum {within2 + mix2:+.1f}")
assert round(within1, 6) == 6.9 and round(mix1, 6) == -14.9
assert round(within2, 6) == 6.5 and round(mix2, 6) == -14.5
assert abs(within1 + mix1 - d) < 1e-9 and abs(within2 + mix2 - d) < 1e-9
# constant-mix ARPU: today's ARPU at last period's shares
cm = sum(shares0[k] * arpu1[k] for k in arpu0)
print(f"ARPU at old mix with new country ARPUs: {cm:.1f} (vs 112.0 last period)")
assert round(cm, 6) == 118.9
