# Q28 toy agent-assist simulation. EVERYTHING is synthetic and ASSUMED: suggestion quality, agent behaviour, handle-time model.
import random, difflib, statistics as st
random.seed(21)
def make_cases(n=4000):
    cs = []
    for _ in range(n):
        good = random.random() < 0.7                                     # ASSUMED: 70% of suggestions are right
        conf = min(1, max(0, random.gauss(0.75 if good else 0.55, 0.15)))   # confidence weakly informative
        cs.append((good, conf))
    return cs
def agent_action(good, shown, bias):
    if not shown: return "write"
    if good: return "accept" if random.random() < 0.6 else "edit"
    # wrong suggestion: a careful agent rewrites; automation bias makes some accept it as is
    return "accept" if random.random() < bias else random.choice(["edit", "write"])
def simulate(cs, silent_below, bias):
    ht, wrong_sent = [], 0
    for good, conf in cs:
        shown = conf >= silent_below
        a = agent_action(good, shown, bias)
        t = {"write": 180, "edit": 110, "accept": 60}[a] + random.gauss(0, 10)   # ASSUMED seconds per action
        if not shown: t = 180 + random.gauss(0, 10)
        ht.append(t)
        if shown and not good and a == "accept": wrong_sent += 1
    return st.mean(ht), wrong_sent
cs = make_cases()
print("bias = chance an agent accepts a WRONG suggestion unchanged (ASSUMED)")
print("silence<  bias   mean_handle_s  wrong_replies_sent(out of 4000)  suggestions_shown")
for sil in (0.0, 0.5, 0.65, 0.8):
    for bias in (0.1, 0.4):
        m, w = simulate(cs, sil, bias); shown = sum(1 for _, c in cs if c >= sil)
        print(f"{sil:7.2f} {bias:5.1f} {m:14.1f} {w:30d} {shown:20d}")
# edit distance as a free label: similarity between suggestion and what the agent finally sent
sug = "Your refund will arrive in 5 to 7 working days."
sent = "Your refund will arrive in 3 to 5 working days."
print("edit similarity (difflib ratio):", round(difflib.SequenceMatcher(None, sug, sent).ratio(), 3), "-> label: small edit, but the edit was a FACT change")
print("caveat: a high similarity can hide the one wrong number; log which spans changed")
