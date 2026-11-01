# Q45: capacity freed by automating routine work, net of review time (illustrative)
team_hours = 1000                       # analyst/DS hours per month
mix = {"routine queries and refreshes": 0.35, "boilerplate code, EDA, docs": 0.15,
       "metric definitions, experiment design, causal reads": 0.25,
       "model building, validation, monitoring": 0.20, "stakeholder advice": 0.05}
assert abs(sum(mix.values()) - 1) < 1e-9
auto_share = {"routine queries and refreshes": 0.60, "boilerplate code, EDA, docs": 0.50}
review_overhead = 0.25                  # reviewing AI output costs 25% of the time it replaces
freed = 0
for k, s in auto_share.items():
    h = team_hours * mix[k]
    saved = h * s * (1 - review_overhead)
    print(f"{k:34} {h:>5.0f} h, automate {s:.0%}, net saved {saved:6.1f} h")
    freed += saved
print(f"net hours freed = {freed:.1f} of {team_hours} = {freed/team_hours:.1%}")
assert abs(freed - (210*0.75 + 75*0.75)) < 1e-9 and abs(freed - 213.75) < 1e-9
# not 'team unnecessary': the defended work is the share that stays
defended = sum(v for k, v in mix.items() if k not in auto_share)
print(f"work not automated away: {defended:.0%} of the mix")
assert abs(defended - 0.50) < 1e-9
# reality check on unsupervised accuracy (see Q40): 74% right means 26 wrong in 100
print("wrong answers per 100 at 74% accuracy:", 100 - 74)
