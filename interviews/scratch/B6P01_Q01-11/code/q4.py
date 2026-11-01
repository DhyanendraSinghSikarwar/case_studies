# Q4: DAU/MAU 0.30 -> 0.26 with MAU flat at 20M (illustrative)
mau = 20.0                       # million
dau_before, dau_after = 0.30 * mau, 0.26 * mau
print(f"DAU before {dau_before:.1f}M after {dau_after:.1f}M change {dau_after/dau_before-1:.1%}")
assert round(dau_before, 1) == 6.0 and round(dau_after, 1) == 5.2

days = 30
# DAU = sum over users of active days / days in window
before_avg_days = 9.0
print(f"before: avg active days per MAU = {before_avg_days} -> DAU {mau*before_avg_days/days:.2f}M")
assert abs(mau * before_avg_days / days - 6.0) < 1e-9

# H1: everyone is a bit less frequent
h1_days = 7.8
dau_h1 = mau * h1_days / days
print(f"H1 less frequent: avg days {h1_days} -> DAU {dau_h1:.2f}M, stickiness {dau_h1/mau:.2f}")
assert abs(dau_h1 - 5.2) < 1e-9

# H2: 3M core users left, 3M one-visit users arrived (paid installs, bots, reactivations)
core, junk = 17.0, 3.0
dau_h2 = (core * 9.0 + junk * 1.0) / days
print(f"H2 low-intent mix: MAU {core+junk:.0f}M, DAU {dau_h2:.2f}M, stickiness {dau_h2/(core+junk):.2f}")
assert abs(dau_h2 - 5.2) < 1e-9 and core + junk == mau
print("Same DAU, same MAU, same ratio: the ratio alone cannot tell H1 from H2.")
print("Cut: distribution of active days per user, by cohort age and channel.")
