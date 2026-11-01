# Q23 referral programme unit economics (illustrative numbers)
reward_each_side = 100            # Rs per side, paid on qualification
qualified_pairs = 1250            # referred users who met the qualifying rule
abusive = 250                     # flagged as self-referral / fake / device-sharing
genuine = qualified_pairs - abusive
reward_cost = qualified_pairs * 2 * reward_each_side   # paid before detection
d90_active_rate = 0.35            # genuine referred users active on day 90
incrementality = 0.60             # share who would NOT have joined without the offer (holdout estimate)
margin_per_retained_90d = 1500    # Rs contribution per retained user over 90 days (assumed)

d90_active = genuine * d90_active_rate
incremental_active = d90_active * incrementality
cost_per_incr_active = reward_cost / incremental_active
net_contribution = incremental_active * margin_per_retained_90d
ratio = net_contribution / reward_cost

print("genuine referred users:", genuine)
print("reward cost (Rs):", reward_cost)
print("abuse share of qualified:", abusive / qualified_pairs)
print("D90-active genuine:", d90_active)
print("incremental D90-active:", incremental_active)
print("cost per incremental D90-active (Rs):", round(cost_per_incr_active, 1))
print("net contribution (Rs):", net_contribution)
print("contribution per Rs of reward:", round(ratio, 3))

assert genuine == 1000 and reward_cost == 250000
assert abusive / qualified_pairs == 0.2
assert round(d90_active) == 350 and round(incremental_active) == 210
assert round(cost_per_incr_active, 1) == 1190.5
assert net_contribution == 315000 and round(ratio, 2) == 1.26
# naive view that finance would reject: cost per qualified user ignores abuse, retention, incrementality
print("naive cost per qualified pair (Rs):", reward_cost / qualified_pairs)
assert reward_cost / qualified_pairs == 200
