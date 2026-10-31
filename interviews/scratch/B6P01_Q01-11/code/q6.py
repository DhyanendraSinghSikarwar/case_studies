# Q6: Android conversion drop, product bug or measurement bug? (illustrative)
import math

def z_two_prop(p1, n1, p2, n2):
    pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
    return (p2 - p1) / se

n = 400_000   # Android cart sessions per period
z = z_two_prop(0.031, n, 0.026, n)
print(f"Android conversion 3.1% -> 2.6%, n={n:,} each: z = {z:.1f}")
assert abs(z) > 10

# blended number if iOS stays 3.1% and Android is 60% of cart sessions
blended = 0.6 * 0.026 + 0.4 * 0.031
print(f"blended conversion with Android at 2.6%: {blended:.2%}")
assert round(blended, 4) == 0.0280

# Two worlds on v8.4 (per 100,000 cart sessions); backend = payment-gateway/order table
sessions = 100_000
worlds = {
    "product bug (button hard to tap)": dict(backend_orders=2600, event_orders=2600),
    "measurement bug (event not fired)": dict(backend_orders=3100, event_orders=2600),
}
print(f"{'world':36} {'event conv':>11} {'backend conv':>13}")
for name, w in worlds.items():
    print(f"{name:36} {w['event_orders']/sessions:11.1%} {w['backend_orders']/sessions:13.1%}")
prod, meas = worlds.values()
assert prod["event_orders"] == prod["backend_orders"]
assert meas["backend_orders"] / sessions == 0.031 and meas["event_orders"] / sessions == 0.026
print("Rule: event and backend both fall = product problem; only event falls = tracking problem.")
