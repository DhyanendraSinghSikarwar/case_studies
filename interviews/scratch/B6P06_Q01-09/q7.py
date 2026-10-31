# Illustrative: once a decision exists, capacity and economics define what to build
customers, unhappy_rate = 5_000, 0.08
calls_per_week = 60                 # CSM capacity (illustrative)
cost_call, value_save, save_rate = 40, 600, 0.30
be_prec = cost_call / (value_save * save_rate)
print(f"unhappy customers ~ {customers*unhappy_rate:.0f}; break-even precision of the call list = {be_prec:.1%}")
assert customers*unhappy_rate == 400 and round(be_prec, 3) == 0.222
# random list precision = base rate; model needs lift over base
print(f"lift needed over random at top-{calls_per_week}: {be_prec/unhappy_rate:.2f}x")
assert round(be_prec/unhappy_rate, 2) == 2.78
# value per week at precision 40%
for prec in (0.08, be_prec, 0.40):
    v = calls_per_week * (prec * value_save * save_rate - cost_call)
    print(f"precision {prec:.1%}: net per week {v:,.0f}")
assert round(60*(0.4*600*0.3-40)) == 1920
