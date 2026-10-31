# Stale documents under weekly re-index; illustrative. A doc is stale from its change until the next re-index.
import numpy as np
N, changes, week = 1200, 90, 7.0
# Exact: change times uniform over the week, so the mean wait to the next re-index is half a week (Little's law: rate x time)
avg_stale = changes * 0.5
print("average stale docs", avg_stale, "share", f"{avg_stale/N:.2%}")
assert avg_stale == 45 and round(avg_stale/N, 4) == 0.0375
# Simulation: 90 distinct docs change at uniform times in each week, re-index at each week boundary
rng = np.random.default_rng(7)
weeks = 20000
t = rng.uniform(0, week, size=(weeks, changes))           # change times within the week
mean_wait = (week - t).mean()                              # days stale per changed doc
print("simulated mean days stale per changed doc", round(mean_wait, 3), "(theory 3.5)")
assert abs(mean_wait - 3.5) < 0.01
sim_avg_stale = changes * mean_wait / week                 # average count stale at a random moment
print("simulated average stale docs", round(sim_avg_stale, 2))
assert abs(sim_avg_stale - 45) < 0.1
# Worst moment: just before re-index, all 90 changed docs are stale; just after, 0
print("peak stale", changes, f"({changes/N:.2%})")
assert changes/N == 0.075
# Different schedule: daily re-index of changed docs only (hash check) -> mean wait 0.5 day
daily = changes * (0.5/7)
print("daily re-index average stale", round(daily, 2), f"({daily/N:.2%})")
assert round(daily, 2) == 6.43
# Event-driven re-index with 10-minute lag
lag_days = 10/1440
print("event-driven 10 min lag average stale", round(changes/7*lag_days, 3))
assert round(changes/7*lag_days, 3) == 0.089
