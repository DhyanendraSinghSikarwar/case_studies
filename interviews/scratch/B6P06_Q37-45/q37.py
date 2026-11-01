# Q37: cost of delay versus expected loss from skipped checks (all numbers illustrative)
weekly_benefit = 25_000
weeks = 3
full_delay = weekly_benefit * weeks
assert full_delay == 75_000

# Option B: shorter, risk-ranked review: 1 week, then a capped launch (20% of traffic) for 2 weeks
review_weeks = 1
cap = 0.20
benefit_during_cap = weekly_benefit * cap * (weeks - review_weeks)
cost_B = full_delay - benefit_during_cap        # benefit not captured vs launching on day 0 ... in the 3-week window
assert benefit_during_cap == 10_000 and cost_B == 65_000

# Option C: skip checks. Break-even failure probability for an assumed loss if a defect ships
loss_if_defect = 1_000_000                       # illustrative
breakeven_p = full_delay / loss_if_defect
assert abs(breakeven_p - 0.075) < 1e-12
# if skipping raises the chance of shipping a serious defect by 10 points, expected loss:
extra_p = 0.10
exp_loss = extra_p * loss_if_defect
assert exp_loss == 100_000 and exp_loss > full_delay

print("A: full 3-week review, delay cost =", full_delay)
print("B: 1-week review + 20% capped launch, benefit captured =", benefit_during_cap, "net delay cost =", cost_B)
print("C: skip checks, break-even extra defect probability =", f"{breakeven_p:.1%}", "for loss", loss_if_defect)
print("   if skipping adds 10 points of defect risk, expected loss =", exp_loss, ">", full_delay)
