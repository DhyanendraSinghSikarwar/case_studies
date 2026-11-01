# Q3: 02:10 page, fraud approval rate 92% -> 71%. Illustrative numbers.
import math

n, base, now = 2000, 0.92, 0.71
fewer = round(n * base) - round(n * now)
assert round(n * base) == 1840 and round(n * now) == 1420 and fewer == 420

# noise check: how big is normal window-to-window wobble?
se = math.sqrt(base * (1 - base) / n)
z = (base - now) / se
print(f"binomial SE of a {n}-request window = {se*100:.2f} points; the drop is {z:.0f} SE, so this is NOT sampling noise")
assert 0.5 < se * 100 < 0.7 and z > 30

# detection delay: rule = two consecutive 5-minute windows below 85% (illustrative); drop starts 02:00
start_min, window, needed = 0, 5, 2
detect_min = start_min + window * needed        # first time two full bad windows exist
print("detection delay (minutes):", detect_min, "-> page at 02:%02d" % detect_min)
assert detect_min == 10

# exposure while we work: 5-min windows of 420 fewer approvals
per_window = fewer
first_15_after_page = 3 * per_window
per_hour = 12 * per_window
print("fewer approvals: first 15 min after page =", first_15_after_page, "| per hour =", per_hour)
assert first_15_after_page == 1260 and per_hour == 5040

# triage step 3: break the drop down by segment (invented counts). Find where it lives.
seg = {  # name: (requests, approvals_before, approvals_now)
    "device_score present": (1200, 1104, 1104),
    "device_score null":    (800,   736,  316),
}
assert sum(v[0] for v in seg.values()) == 2000 and sum(v[2] for v in seg.values()) == 1420
drop_by = {k: v[1] - v[2] for k, v in seg.items()}
share = drop_by["device_score null"] / sum(drop_by.values())
print("drop by segment:", drop_by, "| share in null-segment =", share)
assert drop_by["device_score null"] == 420 and share == 1.0
print("null segment approval now:", round(316 / 800, 3), "(was", 736 / 800, ")")
assert round(316 / 800, 3) == 0.395

# escalation rule as code (thresholds illustrative)
def escalate(minutes_since_page, cause_found, approval_now, falling, wrong_declines_est):
    if approval_now < 0.80 and not cause_found and minutes_since_page >= 10: return "WAKE model owner + data owner"
    if wrong_declines_est > 5000: return "WAKE business owner (customer harm)"
    if cause_found and falling: return "WAKE owner of the broken dependency"
    return "continue solo, update channel every 10 min"
print(escalate(10, False, 0.71, True, 1260))
print(escalate(5, False, 0.71, True, 600))
assert escalate(10, False, 0.71, True, 1260).startswith("WAKE model owner")
assert escalate(5, False, 0.71, True, 600).startswith("continue")
