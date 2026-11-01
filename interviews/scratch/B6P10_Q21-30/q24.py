# Q24 MLOps platform sizing (illustrative)
minutes_month = 30 * 24 * 60
budget_min = (1 - 0.999) * minutes_month
assert minutes_month == 43_200 and abs(budget_min - 43.2) < 1e-9
print(f"monthly error budget at 99.9% = {budget_min:.1f} minutes per real-time service")
print(f"across 10 real-time services = {10*budget_min:.0f} service-minutes in total")

# Chained dependencies: serial availability multiplies
chain = 0.999 ** 3
assert abs(chain - 0.997003) < 1e-6
assert abs((1-chain)*minutes_month - 129.5) < 0.1
print(f"three serial 99.9% parts give {chain:.4%} -> {(1-chain)*minutes_month:.1f} min/month of downtime (3x the single budget)")

# Capacity
engineers, weeks = 4, 26
gross = engineers * weeks
focus = 0.70                     # invented: leave, meetings, on-call, support
net = gross * focus
assert gross == 104 and abs(net - 72.8) < 1e-9
print(f"gross engineer-weeks={gross}, at 70% focus={net:.1f}, per model (25) gross={gross/25:.2f}")

# Illustrative roadmap that sums to the net capacity
plan = {"foundation: registry, packaging, CI": 14,
        "real-time serving, canary, rollback": 18,
        "batch retraining pipelines": 14,
        "monitoring and SLO alerts": 10,
        "onboard 25 models (about 0.5 each)": 12,
        "buffer": 4.8}
tot = sum(plan.values())
assert abs(tot - net) < 1e-9
for k, v in plan.items():
    print(f"  {k}: {v} eng-weeks")
print(f"planned total={tot:.1f}")

# One bad deploy: how many full-outage minutes exhaust one service's budget
assert int(budget_min // 10) == 4
print(f"4 outages of 10 minutes use {40} of {budget_min:.1f} minutes")
assert round(30 / budget_min, 3) == 0.694
print(f"one 30-minute outage uses {30/budget_min:.1%} of the monthly budget")
