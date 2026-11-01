cost_dl, cost_gb = 12_000, 1_500
month = cost_dl - cost_gb
print("extra serving cost:", month, "a month,", month*12, "a year")
assert month == 10_500 and month*12 == 126_000
# misroute reduction needed to pay for it (illustrative volumes and cost)
tasks, cost_mis = 1_000_000, 4.0
need = month / cost_mis
print(f"need {need:,.0f} fewer misroutes a month = {need/tasks:.3%} of {tasks:,} tasks")
assert need == 2625 and round(need/tasks, 5) == 0.00263
# with a different cost per misroute
for c in (1.0, 4.0, 20.0):
    print(f"cost per misroute {c}: need {month/c/tasks:.3%} error-rate reduction")
assert round(month/20/tasks, 6) == 0.000525
