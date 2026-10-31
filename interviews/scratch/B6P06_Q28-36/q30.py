# Illustrative: how long a degraded feed runs under different alert setups. 9 days = 216 hours.
days = 9
hours = days * 24
assert hours == 216
# Alert on feed null-rate, checked every N hours, pages after 2 consecutive breaches.
def detect_hours(check_every, breaches=2):
    return check_every * breaches
for name, every in (("no alert (found by a user)", None), ("daily check", 24), ("hourly check", 1), ("15-min check", 0.25)):
    if every is None:
        h = hours
    else:
        h = detect_hours(every)
    print(f"{name:28} detected after {h:6.2f} h, bad hours avoided {hours-h:6.2f} of {hours}")
assert detect_hours(1) == 2 and detect_hours(24) == 48
# Illustrative cost: 4,000 decisions per day, 3% extra wrong decisions while degraded, 20 per wrong decision
decisions_per_day, extra_wrong, cost = 4000, 0.03, 20
per_day = decisions_per_day * extra_wrong * cost
print(f"cost per degraded day {per_day:.0f}; 9 days {per_day*9:.0f}; 2 hours {per_day*2/24:.0f}")
assert per_day == 2400 and per_day * 9 == 21600 and round(per_day * 2 / 24) == 200
# Ownership table: first page goes to the owner of the thing that broke
owners = {"input feed null/late": "data-eng on-call", "serving latency/errors": "platform on-call",
          "score or label drift, quality": "model owner (DS)", "business KPI off": "product owner"}
for k, v in owners.items(): print(f"{k:32} -> {v}")
assert len(owners) == 4
