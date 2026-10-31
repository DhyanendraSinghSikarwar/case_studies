slo = 0.995
month_min = 30 * 24 * 60
budget = month_min * (1 - slo)
assert month_min == 43200 and round(budget) == 216
used_done = 70 + 95
current = 40
left = budget - used_done - current
print("budget:", round(budget), "min | used incl. current:", used_done + current, "| left:", round(left))
assert round(left) == 11 and used_done + current == 205
print("share left:", round(left / budget * 100, 1), "%")
assert round(left / budget * 100, 1) == 5.1

# Outage still going at full downtime: 1 budget minute burns per wall minute
print("budget gone at outage minute", current + round(left), "(11 more minutes)")
assert current + round(left) == 51
# Availability if the outage ends at various points (30-day window)
for extra in (0, 11, 30, 60):
    down = used_done + current + extra
    print(f"outage ends after {current + extra} min -> availability {100 * (1 - down / month_min):.3f}% (budget left {budget - down:+.0f})")
assert round(100 * (1 - (205 + 30) / month_min), 3) == 99.456
# Rolling window: the 95-minute outage leaves the window when it is >30 days old (editor reasoning)
# Burn rate of a full outage vs the sustainable rate
burn = 1 / (1 - slo)
print("burn rate of a full outage:", round(burn), "x the sustainable rate")
assert round(burn) == 200
