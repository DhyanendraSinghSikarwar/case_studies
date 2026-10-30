# Q9: mix change or regression? D7 retention by channel (illustrative)
ret_organic, ret_paid = 0.30, 0.10
cohorts = {"old (typical)": 0.50, "W1": 0.40, "W2": 0.35, "W3": 0.20}   # organic share of signups
size = 10_000
print(f"{'cohort':14} {'organic':>8} {'paid':>6} {'blended D7':>11}")
blend = {}
for k, s in cohorts.items():
    blend[k] = s * ret_organic + (1 - s) * ret_paid
    print(f"{k:14} {s:8.0%} {1-s:6.0%} {blend[k]:11.1%}")
assert [round(blend[k], 3) for k in ["old (typical)", "W1", "W2", "W3"]] == [0.20, 0.18, 0.17, 0.14]

# Standardise to the old mix: within-channel retention weighted by 50/50
std = 0.5 * ret_organic + 0.5 * ret_paid
print(f"W3 standardised to old mix: {std:.1%}  (unchanged -> mix explains the whole drop)")
assert round(std, 3) == 0.20

# Regression world: same W3 mix, but each channel got worse
reg_org, reg_paid = 0.26, 0.085
reg_blend = 0.20 * reg_org + 0.80 * reg_paid
reg_std = 0.5 * reg_org + 0.5 * reg_paid
print(f"regression world W3: blended {reg_blend:.1%}, standardised {reg_std:.1%}")
assert round(reg_blend, 3) == 0.120 and round(reg_std, 4) == 0.1725
print(f"total fall {reg_blend - 0.20:+.2%}: within-channel {reg_std - 0.20:+.2%}, mix {reg_blend - reg_std:+.2%}")

# Noise check: is 14% vs 20% outside sampling error for n=10,000 signups?
se = (0.17 * 0.83 / size) ** 0.5
print(f"standard error of a ~17% rate with n={size:,}: {se:.2%}; the 6-point gap is about {0.06/se:.0f} se")
assert 0.06 / se > 10
