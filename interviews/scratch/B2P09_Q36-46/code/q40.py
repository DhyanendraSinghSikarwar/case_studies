# Mini eval harness with a MOCK LLM: loader -> runner (cached) -> graders -> repeated trials -> report with CIs.
import hashlib, io, json, random, re
DATA = "\n".join(json.dumps(x) for x in [   # toy JSONL "file" (synthetic)
    {"id": f"q{i}", "question": f"What is {a} + {b}?", "answer": str(a + b)} for i, (a, b) in enumerate((2 + i * 7 % 41, 3 + i * 11 % 37) for i in range(30))])
def load(fp): return [json.loads(l) for l in fp if l.strip()]
class MockLLM:
    """Stands in for an API. Output depends on (model, prompt, trial) via a hash seed; strength = P(correct); verbose models add chatter."""
    def __init__(self, name, strength, verbose=False): self.name, self.strength, self.verbose, self.calls = name, strength, verbose, 0
    def complete(self, prompt, trial):
        self.calls += 1
        seed = int(hashlib.sha256(f"{self.name}|{prompt}|{trial}".encode()).hexdigest()[:8], 16)
        r = random.Random(seed); a, b = map(int, re.findall(r"\d+", prompt))
        val = a + b if r.random() < self.strength else a + b + r.choice([-1, 1, 10])
        return f"The answer is {val}." if self.verbose else str(val)
class Cache:
    def __init__(self): self.d, self.hits = {}, 0
    def get(self, model, prompt, trial, fn):
        k = hashlib.sha256(json.dumps([model.name, prompt, trial]).encode()).hexdigest()
        if k in self.d: self.hits += 1
        else: self.d[k] = fn()
        return self.d[k]
def g_exact(out, ex): return float(out.strip() == ex["answer"])
def g_contains(out, ex): return float(re.search(rf"(?<!\d){re.escape(ex['answer'])}(?!\d)", out) is not None)
GRADERS = {"exact": g_exact, "contains_number": g_contains}
def evaluate(model, data, cache, trials=3):
    res = {g: [[0.0] * trials for _ in data] for g in GRADERS}          # res[grader][case][trial]
    for i, ex in enumerate(data):
        for t in range(trials):
            out = cache.get(model, ex["question"], t, lambda: model.complete(ex["question"], t))
            for g, fn in GRADERS.items(): res[g][i][t] = fn(out, ex)
    return res
def case_means(m): return [sum(r) / len(r) for r in m]
def ci(vals, B=4000, seed=0):                      # bootstrap over CASES (trials of a case are not independent)
    r = random.Random(seed); n = len(vals)
    s = sorted(sum(vals[r.randrange(n)] for _ in range(n)) / n for _ in range(B))
    return sum(vals) / n, s[int(.025 * B)], s[int(.975 * B) - 1]
data = load(io.StringIO(DATA)); cache = Cache()
print("cases loaded:", len(data))
models = [MockLLM("small", 0.70, verbose=True), MockLLM("large", 0.85, verbose=True)]
results = {}
for m in models:
    results[m.name] = evaluate(m, data, cache)
    for g in GRADERS:
        mean, lo, hi = ci(case_means(results[m.name][g]))
        print(f"{m.name:6} grader={g:16} accuracy {mean:.3f}  95% CI [{lo:.3f}, {hi:.3f}]")
print("model calls:", {m.name: m.calls for m in models}, "cache hits:", cache.hits)
for m in models: evaluate(m, data, cache)                                  # rerun: everything should come from cache
print("after rerun   calls:", {m.name: m.calls for m in models}, "cache hits:", cache.hits)
d = [a - b for a, b in zip(case_means(results["large"]["contains_number"]), case_means(results["small"]["contains_number"]))]
mean, lo, hi = ci(d)
print(f"paired difference large-small (contains_number) {mean:+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]")
print("note: 'exact' grader scores the verbose models near 0 -- a grader bug, not a model fact:", round(ci(case_means(results['large']['exact']))[0], 3))
