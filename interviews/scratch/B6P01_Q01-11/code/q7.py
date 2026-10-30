# Q7: DAU +5% but total time -8% (illustrative, minutes per day)
before_dau, before_min = 1_000_000, 30.0
total_before = before_dau * before_min
print(f"before: DAU {before_dau:,}, avg {before_min} min, total {total_before/1e6:.1f}M min")

existing_dau, existing_min = 1_000_000, 27.0     # existing users spend a bit less
new_dau, new_min = 50_000, 12.0                  # new/returning light users
dau_after = existing_dau + new_dau
total_after = existing_dau * existing_min + new_dau * new_min
print(f"after:  DAU {dau_after:,}, total {total_after/1e6:.1f}M min")
print(f"DAU {dau_after/before_dau-1:+.1%}, total time {total_after/total_before-1:+.1%}, "
      f"avg per DAU {total_after/dau_after:.2f} min ({total_after/dau_after/before_min-1:+.1%})")
assert round(dau_after / before_dau - 1, 4) == 0.05
assert round(total_after / total_before - 1, 3) == -0.08
assert round(total_after / dau_after, 2) == 26.29

# split of the change in total time
effect_existing = existing_dau * (existing_min - before_min)
effect_new = new_dau * new_min
print(f"existing users: {effect_existing/1e6:+.1f}M min; new users: {effect_new/1e6:+.1f}M min")
assert effect_existing == -3_000_000 and effect_new == 600_000
print("The whole loss sits in existing users; the new users add a little.")
