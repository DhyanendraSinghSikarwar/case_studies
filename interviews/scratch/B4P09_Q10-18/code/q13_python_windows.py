from datetime import datetime, timedelta
from collections import Counter
T = lambda s: datetime.fromisoformat("2026-03-01T" + s)
ev = sorted(T(t) for t in ["10:00:10", "10:00:40", "10:01:05", "10:00:55", "10:05:20", "10:00:30", "10:04:50"])
print("events (event-time order):", [e.strftime("%H:%M:%S") for e in ev])

# tumbling 1 min: each event in exactly one window
tum = Counter(e.replace(second=0) for e in ev)
print("tumbling 1m   :", {k.strftime("%H:%M"): v for k, v in sorted(tum.items())})

# sliding 2 min, hop 1 min: each event in 2 windows
sl = Counter()
for e in ev:
    start = e.replace(second=0)
    for k in range(2): sl[start - timedelta(minutes=k)] += 1
print("sliding 2m/1m :", {k.strftime("%H:%M") + "-" + (k + timedelta(minutes=2)).strftime("%H:%M"): v for k, v in sorted(sl.items())})

# session, gap 2 min: a new session when the gap to the previous event is >= 2 min
sess, cur = [], [ev[0]]
for e in ev[1:]:
    if e - cur[-1] >= timedelta(minutes=2): sess.append(cur); cur = [e]
    else: cur.append(e)
sess.append(cur)
print("session gap 2m:", [(s[0].strftime("%H:%M:%S"), s[-1].strftime("%H:%M:%S"), len(s)) for s in sess])

# trailing 'last hour' count evaluated at each event time (what a velocity feature wants)
print("trailing 1h at each event:", [(e.strftime("%H:%M:%S"), sum(1 for x in ev if e - timedelta(hours=1) < x <= e)) for e in ev])
