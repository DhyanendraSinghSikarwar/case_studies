"""Q17: gateway budget cap, exact-repeat cache, PII redaction and provider fallback (invented numbers, no network)."""
import random, re, hashlib
random.seed(17)
TEAMS = {  # team: (requests/day, avg input tokens, avg output tokens, daily token budget)
  "support":  (9000, 900, 250, 11_000_000),
  "hr-bot":   (2500, 700, 200, 3_000_000),
  "analytics": (1200, 1500, 600, 2_000_000),
}
print("hand-check daily token volume = requests * (in+out)")
for t, (n, i, o, b) in TEAMS.items():
    vol = n * (i + o)
    print(f"{t:10s} {n:6d} x {i+o:5d} = {vol:>10,d} tokens/day  budget {b:>10,d}  ratio {vol/b:.0%}")
assert 9000 * 1150 == 10_350_000

PII = [(re.compile(r"\b\d{10}\b"), "<PHONE>"), (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "<EMAIL>"), (re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"), "<PAN>")]
def redact(s):
    for rx, tag in PII: s = rx.sub(tag, s)
    return s

class Gateway:
    def __init__(self, budgets, primary_ok=lambda: True):
        self.budget, self.used, self.cache, self.log, self.alerted = dict(budgets), {t: 0 for t in budgets}, {}, [], set()
        self.primary_ok = primary_ok
        self.served = {"primary": 0, "fallback": 0, "cache": 0, "blocked": 0}
    def call(self, team, prompt, in_tok, out_tok):
        key = (team, hashlib.sha256(prompt.encode()).hexdigest())
        if key in self.cache:                       # exact repeat: no provider tokens spent
            self.served["cache"] += 1; return "cache"
        pct = self.used[team] / self.budget[team]
        if pct >= 1.0:
            self.served["blocked"] += 1; return "blocked(429 budget)"
        route = "primary" if self.primary_ok() else "fallback"   # timeout / outage -> smaller model
        self.used[team] += in_tok + out_tok
        if self.used[team] >= 0.8 * self.budget[team] and team not in self.alerted:
            self.alerted.add(team); self.log.append(f"ALERT 80% budget: {team} at request #{sum(self.served.values())+1}")
        self.served[route] += 1
        self.cache[key] = True
        self.log.append(redact(f"{team} {route} {prompt[:40]}"))
        return route

# 1) one day of traffic with the invented rates (analytics runs hot: 1.3x its plan)
gw = Gateway({t: v[3] for t, v in TEAMS.items()})
reqs = []
for t, (n, i, o, b) in TEAMS.items():
    n = int(n * (1.3 if t == "analytics" else 1.0))
    for k in range(n):
        reqs.append((t, f"q{random.randint(0, 40000 if t=='support' else 10**6)} from {t}", int(random.gauss(i, i*0.2)), int(random.gauss(o, o*0.2))))
random.shuffle(reqs)
first100 = {}
for t, p, i, o in reqs:
    r = gw.call(t, p, i, o)
    if r.startswith("blocked") and t not in first100: first100[t] = gw.served["blocked"]
print("\nserved:", gw.served)
for t in TEAMS: print(f"{t:10s} used {gw.used[t]:>11,d} / {gw.budget[t]:>11,d} = {gw.used[t]/gw.budget[t]:.0%}")
print("\n".join(l for l in gw.log if l.startswith("ALERT")))
assert gw.used["analytics"] <= gw.budget["analytics"] + 4000   # cap overshoots by at most one request
assert "analytics" in gw.alerted and "analytics" in first100   # alerted at 80%, blocked at 100%
print("redaction check:", redact("call 9876543210 or a.b@corp.in PAN ABCDE1234F"))
# 2) provider down for part of the day -> fallback route
down = {"on": False}
g2 = Gateway({"support": 10**9}, primary_ok=lambda: not down["on"])
for k in range(100):
    down["on"] = 40 <= k < 70
    g2.call("support", f"unique {k}", 900, 250)
print("outage drill (30 of 100 requests while primary down):", g2.served)
