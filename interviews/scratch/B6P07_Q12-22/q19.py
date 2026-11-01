calls = 100_000
inv_hot, inv_cold = calls * 0.03, calls * 0.005
print(f"invalid per day: temp 0.7 -> {inv_hot:,.0f}; temp 0 -> {inv_cold:,.0f}; difference {inv_hot-inv_cold:,.0f}")
assert (round(inv_hot), round(inv_cold)) == (3000, 500)
# Validate-and-retry. Independent retry only if the failure is not tied to the input.
for rate, label in ((0.005, "temp 0"), (0.03, "temp 0.7")):
    after = calls * rate * rate
    extra = calls * rate
    print(f"{label}: one independent retry leaves ~{after:,.1f} invalid/day, adds {extra:,.0f} extra calls ({rate:.1%} more spend)")
assert round(calls * 0.005 ** 2, 1) == 2.5 and round(calls * 0.03 ** 2) == 90
# If failures repeat on the same input (fully correlated), a same-settings retry fixes nothing.
corr = 1.0
print(f"fully correlated failures: invalid after retry = {calls*0.005*corr:,.0f}/day at temp 0")
assert calls * 0.005 * corr == 500
# Valid JSON is not correct JSON: parse rate and field accuracy are different metrics.
parsed = calls * (1 - 0.005)
field_acc = 0.94
print(f"parsed {parsed:,.0f}; if 94% of parsed outputs have all fields right: {parsed*field_acc:,.0f} fully correct")
assert round(parsed * field_acc) == 93_530
import json
def ok(s):
    try: json.loads(s); return True
    except ValueError: return False
assert ok('{"total": 12.5}') and not ok('{"total": 12.5,}') and not ok('Here is the JSON: {"total": 12.5}')
print("trailing comma and chatty prefix both fail json.loads: checked")
