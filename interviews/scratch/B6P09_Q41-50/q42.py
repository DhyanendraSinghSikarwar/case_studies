# Q42: onboarding bands (prompt numbers, illustrative)
apps, bad = 50_000, 200
auto, review = 35_000, 15_000
bad_auto = 20
bad_review = bad - bad_auto
cost_each = 60
assert auto + review == apps and abs(bad / apps - 0.004) < 1e-12 and auto / apps == 0.7

review_cost = review * cost_each
skip = bad_auto / bad
rate_auto, rate_rev = bad_auto / auto, bad_review / review
print("manual review cost:", review_cost)
print("share of bad identities that skip review:", skip)
print(f"bad rate auto-approve: {rate_auto:.4%}  review: {rate_rev:.4%}  overall: {bad/apps:.2%}")
print("review band is", round(rate_rev / rate_auto, 1), "x riskier than auto band")
assert review_cost == 900_000 and skip == 0.10
assert round(rate_auto * 100, 3) == 0.057 and round(rate_rev * 100, 2) == 1.20

# cost per bad identity found, IF review catches every bad one in its band (best case)
print("review spend per bad identity found (best case):", review_cost / bad_review)
assert review_cost / bad_review == 5_000

# moving the band edge: illustrative table, assuming (invented) the next 5,000 apps below the edge hold 8 more bad ones
extra_apps, extra_bad = 5_000, 8
new_cost = (review + extra_apps) * cost_each
marginal_cost_per_bad = extra_apps * cost_each / extra_bad
print("widen review by 5,000 apps: extra cost", extra_apps * cost_each, "extra bad caught", extra_bad,
      "cost per extra bad", marginal_cost_per_bad)
assert marginal_cost_per_bad == 37_500
print("residual skip share after widening:", (bad_auto - extra_bad) / bad)
assert (bad_auto - extra_bad) / bad == 0.06
