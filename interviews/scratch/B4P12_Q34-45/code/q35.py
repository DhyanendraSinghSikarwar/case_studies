# Q35: fallback decision function with rules-only mode, plus a test that the switch is exercised.
import random
random.seed(35)
RULES = lambda t: "block" if t["amount"] > 50_000 or t["country_risk"] else "allow"
def model_score(t): return 0.9 if t["amount"] > 100_000 else 0.05
def decide(t, mode="model", cls="card_present"):
    """mode: model | rules_only | model_unavailable. fail policy per class when no decision is possible."""
    if mode == "rules_only": return RULES(t), "rules"
    try:
        if mode == "model_unavailable": raise TimeoutError
        return ("block" if model_score(t) > 0.5 else "allow"), "model"
    except TimeoutError:
        # fail-open for low-value, fail-closed(step-up) for high-value / risky
        if t["amount"] > 10_000 or cls == "card_not_present": return "step_up", "fail_closed"
        return "allow", "fail_open"
def fp_rate(mode, broken=False, n=2000):
    global model_score
    saved = model_score
    if broken: model_score = lambda t: 0.9          # bad nightly feature job: every txn looks risky
    fp = 0
    for _ in range(n):
        t = {"amount": random.choice([100, 500, 30_000]), "country_risk": False}   # all genuine
        d, _ = decide(t, mode)
        fp += d == "block"
    model_score = saved
    return fp / n
# monthly drill: the switch must be exercised and must work
class Drill:
    last = None
    def run(self, month):
        t = {"amount": 60_000, "country_risk": False}
        assert decide(t, "rules_only") == ("block", "rules")
        assert decide({"amount": 100, "country_risk": False}, "model_unavailable") == ("allow", "fail_open")
        assert decide({"amount": 100, "country_risk": False}, "model_unavailable", "card_not_present") == ("step_up", "fail_closed")
        self.last = month
d = Drill()
def check_drill_freshness(today_month): 
    return d.last is not None and today_month - d.last <= 1
print("freshness before any drill:", check_drill_freshness(10))
d.run(10); print("freshness after drill in month 10:", check_drill_freshness(10))
print("freshness 3 months later:", check_drill_freshness(13), "-> page the owner")
print("false-positive rate on genuine txns: healthy model", fp_rate("model"), "| broken features", fp_rate("model", True), "| rules_only after switch", fp_rate("rules_only", True))
for t, c in [({"amount": 100}, "card_present"), ({"amount": 15_000}, "card_present"), ({"amount": 100}, "card_not_present")]:
    t["country_risk"] = False
    print(t["amount"], c, "->", decide(t, "model_unavailable", c))
# cost angle in abstract units: control cost per month vs expected loss avoided
controls = {"auto-rollback": (2, 40), "monthly drill": (1, 25), "extra region": (30, 20), "shadow rules": (4, 30)}
for k, (cost, avoided) in controls.items(): print(f"{k:14s} cost {cost:3d} avoided {avoided:3d} ratio {avoided/cost:5.1f}")
