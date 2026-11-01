# Router vs supervisor, counting MOCK LLM calls. Specialists and the routing/supervising policies are deterministic scripts.
SPECIALISTS = {"billing": lambda q: "billing answer", "tech": lambda q: "tech answer", "legal": lambda q: "legal answer"}
KEYWORDS = {"invoice": "billing", "charge": "billing", "error": "tech", "crash": "tech", "contract": "legal"}

def router(question):
    """1 routing call picks ONE specialist; 1 specialist call. Cannot combine."""
    calls = 1
    topics = [KEYWORDS[w] for w in question.lower().split() if w in KEYWORDS]
    pick = topics[0] if topics else "tech"
    calls += 1
    return {"answer": SPECIALISTS[pick](question), "calls": calls, "specialists": [pick]}

def supervisor(question, max_rounds=5):
    """Loop: supervisor call decides next delegation or finish; each delegation is a specialist call; final combine call."""
    needed = list(dict.fromkeys(KEYWORDS[w] for w in question.lower().split() if w in KEYWORDS)) or ["tech"]
    calls, done, parts = 0, [], []
    for _ in range(max_rounds):
        calls += 1                                   # supervisor decides
        todo = [t for t in needed if t not in done]
        if not todo: break
        t = todo[0]; parts.append(SPECIALISTS[t](question)); done.append(t); calls += 1   # delegate
    calls += 1                                       # combine the parts into one answer
    return {"answer": " + ".join(parts), "calls": calls, "specialists": done}

for q in ["my invoice has a wrong charge", "app shows an error then a crash", "wrong invoice charge and a contract dispute and an error"]:
    r, s = router(q), supervisor(q)
    print(f"{q[:48]:48} router calls={r['calls']} covers={r['specialists']} | supervisor calls={s['calls']} covers={s['specialists']}")
assert router("invoice error")["specialists"] == ["billing"] and supervisor("invoice error")["specialists"] == ["billing", "tech"]
assert supervisor("invoice charge")["calls"] > router("invoice charge")["calls"]
print("tests passed")
