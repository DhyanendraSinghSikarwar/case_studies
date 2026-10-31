# Standalone, standard library only. MOCK summariser (truncates to a word budget); no LLM is called. Word count stands in for tokens.
CONTEXT = 1000                        # ASSUMED context window in "tokens" (words here)
def toks(s): return len(s.split())
def mock_summarise(text, budget): return " ".join(text.split()[:budget])     # MOCK: keeps the first `budget` words (real systems call an LLM)

docs = {f"doc{i}": " ".join(f"d{i}w{j}" for j in range(600)) for i in range(10)}      # 10 synthetic docs, 600 words each
question = "what changed across all ten documents"
print("raw total:", sum(toks(t) for t in docs.values()), "words vs context", CONTEXT, "-> does not fit")

calls = 0
def map_step(question, docs, per_doc):            # MAP: one call per document, extract/summarise with the question in mind
    global calls; out = {}
    for k, t in docs.items(): calls += 1; out[k] = f"[{k}] " + mock_summarise(t, per_doc)
    return out
def reduce_step(parts, budget):                   # REDUCE: combine; if still too big, reduce hierarchically in groups
    global calls
    level = list(parts.values())
    while sum(toks(p) for p in level) > budget:
        nxt = []
        for i in range(0, len(level), 2):
            group = " ".join(level[i:i + 2]); calls += 1; nxt.append(mock_summarise(group, max(20, toks(group) // 2)))
        level = nxt
        if len(level) == 1: break
    return " ".join(level)

reserve = 300                                     # room for system prompt, question, answer
parts = map_step(question, docs, per_doc=120)
print("after map:", sum(toks(p) for p in parts.values()), "words in", len(parts), "partial summaries")
ctx = reduce_step(parts, CONTEXT - reserve)
print("final context:", toks(ctx), "words; budget", CONTEXT - reserve, "; LLM calls (mock):", calls + 1)
assert toks(ctx) + reserve <= CONTEXT, "token budget violated"
print(f"words kept per document: {120/600:.0%} after map, {toks(ctx)/6000:.0%} of the original in the final context (the mock keeps the first words; a real map step should be question-aware)")
