# Q29 toy data flywheel. SYNTHETIC: 50 question types; the "model" answers each type with one of two answers and may learn from feedback.
# All probabilities below are ASSUMED to show a mechanism, not measured behaviour.
import random
random.seed(4)
TYPES = 50
truth = {t: "A" for t in range(TYPES)}                       # the correct answer for every type is A
class Model:
    def __init__(self): self.pA = {t: 0.8 if t >= 10 else 0.2 for t in range(TYPES)}   # types 0-9: model mostly says wrong B (fluent but wrong)
    def answer(self, t): return "A" if random.random() < self.pA[t] else "B"
def user_feedback(t, ans):
    # ASSUMED: fluent wrong answers in "hard to verify" types 0-9 get thumbs-up MORE often than the correct but unwelcome answer; checkable types get honest feedback; 20% respond
    if random.random() > 0.2: return None
    if ans == truth[t]: return "up" if random.random() < (0.5 if t < 10 else 0.8) else "down"   # correct but unwelcome answers (e.g. "no refund") get fewer thumbs-up
    return "up" if (t < 10 and random.random() < 0.8) else "down"
def accuracy(m, ts=range(TYPES)): return sum(m.pA[t] for t in ts) / len(ts)
def round_(m, n=20000, review=0, gold=None):
    up = {t: {"A": 0, "B": 0} for t in range(TYPES)}; nfb = 0; ups = 0
    for _ in range(n):
        t = random.randrange(TYPES); a = m.answer(t); f = user_feedback(t, a)
        if f: nfb += 1; ups += f == "up"
        if f == "up": up[t][a] += 1
    # naive training: move pA toward whichever answer got more thumbs-up; "review" types get gold labels from human audit
    for t in range(TYPES):
        tot = up[t]["A"] + up[t]["B"]
        if gold and t in gold: m.pA[t] = min(0.98, m.pA[t] + 0.3); continue
        if tot >= 5: m.pA[t] = 0.5 * m.pA[t] + 0.5 * up[t]["A"] / tot
    return ups / nfb
for label, gold in [("thumbs only (no audit)", None), ("thumbs + human audit of 10 lowest-trust types", set(range(10)))]:
    m = Model(); print(label)
    print(f"  start true accuracy {accuracy(m):.3f} (types 0-9: {accuracy(m, range(10)):.3f}, types 10-49: {accuracy(m, range(10, 50)):.3f})")
    for r in range(1, 4):
        up_rate = round_(m, gold=gold); print(f"  round {r}: thumbs-up rate {up_rate:.3f}  true accuracy {accuracy(m):.3f} (types 0-9: {accuracy(m, range(10)):.3f}, types 10-49: {accuracy(m, range(10, 50)):.3f})")
