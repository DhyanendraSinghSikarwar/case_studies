# MOCK multi-hop decomposition over a tiny INVENTED knowledge base (fictional entities). Planner and reader are mocks.
import re
KB = [
 "The Zorbo scooter is manufactured by Zentra Motors.",
 "Zentra Motors is led by chief executive Mira Quill.",
 "Mira Quill was born in Port Alder.",
 "Port Alder is a harbour town known for its lighthouse.",
 "Kelvo Bikes is led by chief executive Dan Orsk.",
 "Dan Orsk was born in Hill Marrow.",
]
def toks(t): return set(re.findall(r"[a-z0-9]+", t.lower())) - {"the", "is", "by", "of", "a", "in", "was", "who", "where"}
def retrieve(q, k=2):                       # keyword-overlap retriever (toy)
    s = sorted(KB, key=lambda d: -len(toks(q) & toks(d)))
    return [d for d in s[:k] if toks(q) & toks(d)]
# MOCK reader: pulls the answer span with a pattern, as a stand-in for an LLM reading retrieved text
PATTERNS = {"maker": r"scooter is manufactured by ([A-Z][\w ]+?)\.",
            "ceo":   r"{X} is led by chief executive ([A-Z][\w ]+?)\.",
            "birth": r"{X} was born in ([A-Z][\w ]+?)\."}
def read(kind, passages, x=None):
    pat = PATTERNS[kind].replace("{X}", re.escape(x or ""))
    for p in passages:
        m = re.search(pat, p)
        if m: return m.group(1)
    return None
# MOCK planner: fixed plan for this question. Each step names what it needs from an earlier step.
Q = "Where was the chief executive of the maker of the Zorbo scooter born?"
PLAN = [("s1", "maker", "Zorbo scooter manufacturer", None),
        ("s2", "ceo",   "{s1} chief executive", "s1"),
        ("s3", "birth", "{s2} born", "s2")]

print("single-shot retrieval of the full question:", retrieve(Q, 2))
ans, calls = {}, 0
for sid, kind, template, dep in PLAN:
    x = ans[dep] if dep else None
    if dep and x is None: print(sid, "skipped: dependency failed"); ans[sid] = None; continue
    sub = template.format(**{k: v for k, v in ans.items() if v})     # hop 2 needs hop 1's bridge entity
    passages = retrieve(sub); calls += 1
    ans[sid] = read(kind, passages, x)
    print(f"{sid}: query={sub!r:38} -> {ans[sid]!r}")
print("final answer:", ans["s3"], "| retrieval calls:", calls, "(+1 planner call +1 synthesis call in a real system)")

# error propagation: if hop 1 returns the wrong bridge entity, every later hop is confidently wrong
bad = "Kelvo Bikes"
c = read("ceo", retrieve(f"{bad} chief executive"), bad); b = read("birth", retrieve(f"{c} born"), c)
print("if hop 1 were wrong ('Kelvo Bikes'):", c, "->", b, " (fluent but wrong)")
