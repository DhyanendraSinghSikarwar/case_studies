# Illustrative monthly MAU in millions. 'open' = old definition, 'action' = new definition.
months = ["Apr", "May", "Jun"]
open_mau   = {"Apr": 10.00, "May": 10.05, "Jun": 10.00}
action_mau = {"Apr": 8.58,  "May": 8.64,  "Jun": 8.60}   # backfilled from raw events
# what the exec dashboard showed: old definition before the switch, new one after
shown = {"Apr": open_mau["Apr"], "May": open_mau["May"], "Jun": action_mau["Jun"]}
headline = shown["Jun"] / shown["Apr"] - 1
old_like = open_mau["Jun"] / open_mau["Apr"] - 1
new_like = action_mau["Jun"] / action_mau["Apr"] - 1
print(f"dashboard Apr->Jun         {headline:+.1%}")
print(f"old definition, like for like {old_like:+.1%}")
print(f"new definition, like for like {new_like:+.1%}")
assert round(headline, 3) == -0.140 and old_like == 0 and round(new_like, 4) == 0.0023
for m in months:
    print(m, f"action share of open users {action_mau[m] / open_mau[m]:.1%}")
assert round(action_mau["Apr"] / open_mau["Apr"], 3) == 0.858
# the definitional step is the whole drop: bridge in millions
print("bridge (M): old Apr", open_mau["Apr"], "-> definition step", round(action_mau["Apr"] - open_mau["Apr"], 2),
      "-> real change", round(action_mau["Jun"] - action_mau["Apr"], 2), "= new Jun", action_mau["Jun"])
assert abs(open_mau["Apr"] + (action_mau["Apr"] - open_mau["Apr"]) + (action_mau["Jun"] - action_mau["Apr"]) - action_mau["Jun"]) < 1e-9
