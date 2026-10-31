# TOY: gating a PR on a noisy eval. Mock model, SYNTHETIC per-item pass probabilities, seeded.
import random, math, re
random.seed(2026)
N = 60                                       # PR eval tier size
items = [random.choice([0.95, 0.9, 0.8, 0.5, 0.2]) for _ in range(N)]
def run(shift=0.0):                          # one noisy eval run (non-deterministic model)
    return [random.random() < min(1, max(0, p + shift)) for p in items]
def gate_naive(base, cand): return sum(cand) >= sum(base)          # block if score drops at all
def sign_p(b, c):
    n = b + c
    return 1.0 if n == 0 else sum(math.comb(n, k) for k in range(b, n + 1)) / 2 ** n
def gate_stat(base, cand, alpha=0.05):                              # block only if significantly worse on paired items
    b = sum(x and not y for x, y in zip(base, cand)); c = sum(y and not x for x, y in zip(base, cand))
    return sign_p(b, c) >= alpha
def rate(shift, gate, trials=2000):
    ok = 0
    for _ in range(trials):
        ok += gate(run(0.0), run(shift))
    return ok / trials
for label, shift in [("no real change", 0.0), ("real regression (-0.15 per item)", -0.15)]:
    print(f"{label:34} naive gate passes {rate(shift, gate_naive)*100:5.1f}% | paired-sign gate passes {rate(shift, gate_stat)*100:5.1f}%")
# cheap per-PR hygiene checks (all deterministic)
SECRET = re.compile(r"(sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16})")       # illustrative patterns only
def scan(text): return SECRET.findall(text)
print("secret scan on fake key:", scan("API_KEY=sk-" + "a" * 20), "| clean text:", scan("no keys here"))
def lint_prompt(t):
    problems = []
    if "{{" in t and "}}" not in t: problems.append("unclosed placeholder")
    if len(t) > 4000: problems.append("prompt over 4000 chars")
    return problems
print("prompt lint:", lint_prompt("Answer {{question"), lint_prompt("Answer {{question}}"))
