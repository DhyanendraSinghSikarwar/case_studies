# TOY: attaching feedback to traces, and how response-rate bias distorts thumbs. SYNTHETIC rates, seeded.
import random
random.seed(21)
N = 50_000
TRUE_SAT = 0.80                                    # assumed true share of satisfied answers
RESP = {"happy": 0.01, "unhappy": 0.06}            # ASSUMED: unhappy users click thumbs 6x as often
traces = {}                                         # trace_id -> record
for i in range(N):
    happy = random.random() < TRUE_SAT
    traces[i] = {"happy": happy, "feedback": None}
def attach(trace_id, kind):                         # feedback event carries the trace id
    traces[trace_id]["feedback"] = kind
for i, t in traces.items():
    if random.random() < RESP["happy" if t["happy"] else "unhappy"]:
        attach(i, "up" if t["happy"] else "down")
ups = sum(t["feedback"] == "up" for t in traces.values()); downs = sum(t["feedback"] == "down" for t in traces.values())
print(f"responded: {ups+downs} of {N} ({(ups+downs)/N*100:.2f}%) | up {ups} down {downs}")
print(f"thumbs-down share among responses: {downs/(ups+downs)*100:.1f}%  vs true unhappy share {(1-TRUE_SAT)*100:.0f}%")
# inverse-probability weighting works only if the response rates are known (they usually are not)
est_up, est_down = ups / RESP["happy"], downs / RESP["unhappy"]
print(f"reweighted using the ASSUMED rates: estimated unhappy share {est_down/(est_up+est_down)*100:.1f}%")
# a trend is still useful: same bias each week, so a jump in down-rate signals change
def week(true_unhappy, n=20_000):
    d = u = 0
    for _ in range(n):
        happy = random.random() > true_unhappy
        if random.random() < RESP["happy" if happy else "unhappy"]: u += happy; d += (not happy)
    return d / max(1, d + u)
print("down share if true unhappy is 20%:", f"{week(0.20)*100:.1f}%", "| if it rises to 30%:", f"{week(0.30)*100:.1f}%")
# implicit signals as events on the same trace id
events = [("regenerate", 5), ("copy", 6), ("abandon", 7), ("edit", 6)]
print("implicit events keyed by trace:", events)
