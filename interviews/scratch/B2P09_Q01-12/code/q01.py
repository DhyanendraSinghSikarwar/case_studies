# MOCK: model-level vs system-level evaluation on toy, synthetic data. No real LLM is used.
import random
random.seed(1)

# 20 synthetic test cases: each has a gold answer and the doc that contains it.
CASES = [{"id": i, "q": f"q{i}", "gold": f"ans{i}", "doc": f"doc{i}"} for i in range(20)]
CORPUS = {c["doc"]: f"The answer is {c['gold']}." for c in CASES}

def mock_retriever(q, retr_hit_rate=0.7):
    """Assumed: finds the right doc 70% of the time, otherwise a wrong doc."""
    i = int(q[1:])
    if random.random() < retr_hit_rate:
        return f"doc{i}"
    return f"doc{(i + 1) % 20}"

def mock_generator(q, context):
    """Assumed: a strong model that copies the answer from the context if present."""
    return context.split()[-1].rstrip(".")

def graded(case, out):               # deterministic grader first (cheap, exact)
    return out == case["gold"]

# MODEL eval: hand the model the gold doc. Measures generation only.
model_pass = sum(graded(c, mock_generator(c["q"], CORPUS[c["doc"]])) for c in CASES)
# SYSTEM eval: retriever + generator, as users experience it.
sys_pass = 0
for c in CASES:
    d = mock_retriever(c["q"])
    sys_pass += graded(c, mock_generator(c["q"], CORPUS[d]))
print("model eval (gold context):", model_pass, "/", len(CASES))
print("system eval (real retriever):", sys_pass, "/", len(CASES))

# Offline vs online: offline set is clean queries; online traffic has a 'typo' slice
# the offline set never sampled (assumed 30% of traffic, retrieval hit rate 0.4 there).
def online_pass(n=1000):
    ok = 0
    for _ in range(n):
        typo = random.random() < 0.3
        c = random.choice(CASES)
        d = mock_retriever(c["q"], 0.4 if typo else 0.7)
        ok += graded(c, mock_generator(c["q"], CORPUS[d]))
    return ok / n
print("online-style pass rate (assumed 30% typo traffic):", online_pass())
