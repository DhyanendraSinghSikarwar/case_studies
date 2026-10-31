# Q21 model inventory and validation capacity (illustrative numbers)
total, high, capacity = 120, 18, 24
others = total - high
spare = capacity - high            # validations left after the yearly high-risk cycle
years_all_full = others / spare
assert others == 102 and spare == 6 and years_all_full == 17.0
print(f"other models={others}, spare full validations/yr={spare}, years for one pass={years_all_full:.0f}")

# What if the other 102 are split into medium (24) and low (78) tiers?
# Illustrative cadence: medium = full validation every 3 years, low = light review every year
# (a light review costs 0.1 of a full validation, an invented ratio)
medium, low = 24, 78
med_load = medium / 3                    # 8 full validations/yr
low_load = low * 0.1                     # 7.8 full-validation equivalents/yr
need = high + med_load + low_load
assert med_load == 8.0 and abs(low_load - 7.8) < 1e-9 and abs(need - 33.8) < 1e-9
print(f"tiered load = {need:.1f} full-validation equivalents vs capacity {capacity}")
gap = need - capacity
assert abs(gap - 9.8) < 1e-9
print(f"gap = {gap:.1f} -> options: more staff, longer medium cycle, or fewer high-risk models")

# Longer medium cycle (every 4 years) and low light review at 0.05
need2 = high + medium / 4 + low * 0.05
assert abs(need2 - 27.9) < 1e-9
print(f"with medium every 4y and low at 0.05: {need2:.1f} (still above {capacity})")
