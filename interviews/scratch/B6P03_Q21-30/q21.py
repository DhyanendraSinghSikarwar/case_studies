# Q21 sensor spike: error or real event? (illustrative numbers)
import numpy as np
rng = np.random.default_rng(21)

machines, hours = 1200, 1
step_s = 10                                   # one reading every 10 s
n = hours * 3600 // step_s                    # 360 readings per machine
base = rng.normal(60, 8, size=(machines, 1)) + rng.normal(0, 1.0, size=(machines, n))
base = np.clip(base, 20, 90)
spike_machines = [101, 640, 1033]
k = 6                                         # about a minute = 6 readings
for m in spike_machines:
    base[m, 100:100 + k] = 850.0
assert len(spike_machines) / machines == 0.0025          # 0.25% of machines
bad = (base > 90).sum()
print("spike rows:", bad, "of", base.size, f"= {bad/base.size:.5%} of rows")
assert bad == 18

# 1) Percentile winsorising: clip at the 99th percentile of all readings
p99 = np.percentile(base, 99)
clipped = np.minimum(base, p99)
changed_good = ((base != clipped) & (base <= 90)).sum()
print(f"p99 = {p99:.1f} C; winsorising also alters {changed_good} GOOD rows ({changed_good/base.size:.2%})")
assert changed_good > 3000
# 850 does become ~p99, so the spike is hidden and the evidence is gone
assert clipped[101, 100] == p99

# 2) Effect of the spike on a 1-hour mean and max feature for a spiked machine
m = 101
print(f"hourly mean raw {base[m].mean():.1f}, clipped {clipped[m].mean():.1f}; hourly max raw {base[m].max():.0f}")
assert base[m].max() == 850

# 3) Triage rule: a physical-plausibility check, not a statistical one
MAX_SLEW = 5.0        # C per second the process can physically change (illustrative)
def triage(series, other_sensor_delta):
    """series: 10 s readings around the event; other_sensor_delta: change on a second sensor (e.g. motor current %)."""
    jump = np.abs(np.diff(series)).max() / step_s
    impossible_slew = jump > MAX_SLEW
    corroborated = abs(other_sensor_delta) > 10
    if impossible_slew and not corroborated:
        return "error (likely sensor/gateway)"
    if corroborated and not impossible_slew:
        return "real event"
    return "unclear: escalate to plant owner"
s = base[101, 95:115]
print("jump rate", round(np.abs(np.diff(s)).max() / step_s, 1), "C/s")
print("no corroboration  ->", triage(s, 0.5))
print("motor current +40% ->", triage(s, 40))
assert triage(s, 0.5).startswith("error")
assert triage(s, 40).startswith("unclear")
# a real overheating event ramps up smoothly and other sensors move with it
ramp = np.concatenate([np.linspace(60, 850, 60), np.full(10, 850.0)])  # 60 readings of 10 s: ~10 min ramp
print("ramp, current +40% ->", triage(ramp, 40))
assert triage(ramp, 40) == "real event"
