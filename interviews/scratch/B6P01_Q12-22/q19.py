# Toy 28-day log. Each row: (user, kind, detail)
ride_events = [
 ("u1", "ride_completed", "ok"), ("u1", "ride_completed", "ok"),
 ("u2", "app_open", ""),                          # only opened the app
 ("u3", "ride_completed", "cancel_in_20s"),       # cancelled almost at once, still logged
 ("u4", "ride_completed", "ok"),                
 ("u5", "ride_completed", "device_farm"),         # emulator / GPS-spoof pattern
 ("u6", "ride_completed", "employee_test"),
 ("u7", "ride_completed", "ok"),
]
naive_ride = {u for u, k, d in ride_events}                                  # any event
good_ride  = {u for u, k, d in ride_events if k == "ride_completed" and d == "ok"}
print("ride, any event       :", len(naive_ride))
print("ride, completed+clean :", len(good_ride), sorted(good_ride))
assert len(naive_ride) == 7 and good_ride == {"u1", "u4", "u7"}
# B2B tool: weekly active ACCOUNT = at least 2 distinct users ran a saved query or opened a shared dashboard
b2b = [
 ("acme", "u1", "run_query", "2026-10-05"), ("acme", "u2", "view_dashboard", "2026-10-06"),
 ("beta", "u3", "login", "2026-10-05"),                       # login only
 ("beta", "u3", "run_query", "2026-10-06"),                   # one user only
 ("gamma", "svc", "run_query", "2026-10-07"),                 # scheduled job, not a person
 ("gamma", "svc", "run_query", "2026-10-08"),
 ("delta", "u9", "run_query", "2026-10-07"), ("delta", "u10", "run_query", "2026-10-07"),
]
service = {"svc"}
valid = {"run_query", "view_dashboard"}
from collections import defaultdict
users = defaultdict(set)
for acct, u, act, day in b2b:
    if act in valid and u not in service:
        users[acct].add(u)
active = sorted(a for a, us in users.items() if len(us) >= 2)
print("B2B weekly active accounts (>=2 real users, key action):", active)
assert active == ["acme", "delta"]
print("accounts with any login/event:", len({a for a, *_ in b2b}))
assert len({a for a, *_ in b2b}) == 4
