# Illustrative numbers, million. Difference-in-differences style counterfactual.
last, this = 20.0, 23.0
growth_all = this / last - 1
comp = 0.11
expected = last * (1 + comp)
lift = this - expected
print(f"raw growth {growth_all:.1%}, expected {expected:.1f}, campaign {lift:.2f}")
assert round(growth_all, 2) == 0.15 and round(expected, 1) == 22.2 and round(lift, 2) == 0.80
raw_gain = this - last                    # what the CEO credits
share = lift / raw_gain
print(f"CEO credits {raw_gain:.1f}; campaign share {share:.1%}; the other {raw_gain-lift:.1f} would have happened anyway")
assert raw_gain == 3.0 and round(share, 3) == 0.267
# Sensitivity: the comparison growth is itself uncertain.
for g in (0.09, 0.11, 0.13):
    print(f"comparison growth {g:.0%}: campaign = {this - last*(1+g):.2f}")
assert round(this - last*1.09, 2) == 1.20 and round(this - last*1.13, 2) == 0.40
# Break-even growth where the campaign is worth nothing, and where the CEO is right
print("campaign = 0 if comparison grew", f"{this/last-1:.0%}")
# Does it pay? Illustrative cost 0.5 and 30% margin on the incremental sales.
margin, cost = 0.30, 0.5
print(f"incremental margin {lift*margin:.2f} vs cost {cost}: net {lift*margin-cost:.2f}")
assert round(lift*margin - cost, 2) == -0.26
print(f"CEO view of margin: {raw_gain*margin:.2f} vs cost {cost}: net {raw_gain*margin-cost:.2f}")
assert round(raw_gain*margin - cost, 2) == 0.40
