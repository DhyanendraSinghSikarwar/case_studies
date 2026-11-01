# Bounded agent loop: plan -> retrieve -> judge sufficiency -> retry or answer. Everything is MOCK (no LLM, toy retriever).
# Token counts are ASSUMED per-call costs, only to show budget accounting.
import re
KB = ["The Zorbo scooter is manufactured by Zentra Motors.", "Zentra Motors is led by chief executive Mira Quill.",
      "Mira Quill was born in Port Alder.", "Refunds are accepted within 30 days of purchase."]
def toks(t): return set(re.findall(r"[a-z0-9]+", t.lower())) - {"the", "is", "by", "of", "a", "in", "was", "who", "where", "are", "within"}
def retrieve(q): 
    best = max(KB, key=lambda d: len(toks(q) & toks(d)))
    return best if toks(q) & toks(best) else None
COST = {"plan": 300, "judge": 200, "answer": 400}       # ASSUMED tokens per mock LLM call

def judge(question_needs, evidence):    # INDEPENDENT sufficiency check: rule-based, does not reuse the planner's opinion
    return all(any(n in e for e in evidence) for n in question_needs)

def run(question, needs, first_query, next_query, max_steps=4, token_budget=2500):
    evidence, tokens, q = [], 0, first_query
    for step in range(1, max_steps + 1):
        if tokens + COST["plan"] + COST["judge"] + COST["answer"] > token_budget:   # keep room to finish with an answer
            return "stop: token_budget -> answer with what we have, flagged partial", evidence, tokens, step - 1
        tokens += COST["plan"]
        doc = retrieve(q)
        if doc and doc not in evidence: evidence.append(doc)
        tokens += COST["judge"]
        if judge(needs, evidence):
            tokens += COST["answer"]
            return "stop: sufficient evidence -> answer", evidence, tokens, step
        q = next_query(evidence)                     # mock planner: pick the next hop from what we have
    return "stop: max_steps -> say 'not enough evidence'", evidence, tokens, max_steps

def hop(evidence):
    text = " ".join(evidence)
    if "Mira Quill was born" in text: return "Port Alder"
    if "Mira Quill" in text: return "Mira Quill born"
    if "Zentra Motors" in text: return "Zentra Motors chief executive"
    return "Zorbo scooter manufacturer"

runs = [
 ("simple lookup", "Refunds accepted days", ["Refunds"], "refunds accepted days", hop, 4, 2500),
 ("multi-hop", "Where was the CEO of the Zorbo maker born?", ["born in Port Alder"], "Zorbo scooter manufacturer", hop, 4, 2500),
 ("unanswerable", "What is the CEO's salary?", ["salary"], "Zentra salary", hop, 3, 2500),
 ("multi-hop, tight budget", "Where was the CEO of the Zorbo maker born?", ["born in Port Alder"], "Zorbo scooter manufacturer", hop, 4, 1500),
]
for name, qn, needs, fq, nq, ms, tb in runs:
    reason, ev, tok, steps = run(qn, needs, fq, nq, ms, tb)
    print(f"{name:24} steps={steps} tokens={tok:4} evidence={len(ev)} | {reason}")
