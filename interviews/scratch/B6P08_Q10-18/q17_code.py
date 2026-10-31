nodes_burst, nodes_base, hours, cost = 40, 6, 72, 3
extra_nodes = nodes_burst - nodes_base
extra = extra_nodes * hours * cost
total = nodes_burst * hours * cost
base = nodes_base * hours * cost
print("extra nodes", extra_nodes, "| extra cost", extra, "| total", total, "| baseline", base)
assert extra_nodes == 34 and extra == 7344 and total == 8640 and base == 1296 and total - base == extra
print("overspend vs baseline:", round(extra / base, 1), "x the baseline cost for those 72 hours")
assert round(extra / base, 1) == 5.7
# Peak need, illustrative: burst needed 40 nodes for 2 hours; after that load needs 8 nodes
need_hours_burst, need_after = 2, 8
fair = nodes_burst * need_hours_burst * cost + need_after * (hours - need_hours_burst) * cost
print("fair cost with working scale-down:", fair, "| waste:", total - fair)
assert fair == 240 + 1680 and total - fair == 6720
# A cost alert at 2x baseline node-hours would have fired after 4 hours of the plateau
alert_after = 4
caught = extra_nodes * alert_after * cost
print("extra cost if the alert fired after 4 h:", caught, f"({caught/extra*100:.1f}% of the real overspend)")
assert caught == 408 and round(caught / extra * 100, 1) == 5.6
# Scale-down policy: stabilisation window and max step
n, steps, wait_min = 40, 0, 0
floor = 8
while n > floor:
    n = max(floor, n - max(2, int(n * 0.2)))   # remove 20% (at least 2) per step
    steps += 1; wait_min += 10                  # 10-minute stabilisation between steps
print("steps to reach", floor, "nodes:", steps, "| minutes:", wait_min)
assert steps == 8 and wait_min == 80
