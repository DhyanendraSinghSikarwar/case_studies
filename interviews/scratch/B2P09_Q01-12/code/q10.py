# Why a benchmark score is not a product eval: two toy demonstrations on SYNTHETIC models.
import random
random.seed(4)

# 1) Ranking flips when the task mix changes. Skill = pass rate per task type (ASSUMED numbers).
skills = {"model_X": {"math_mcq": 0.90, "code": 0.70, "support_chat": 0.60, "extraction": 0.70},
          "model_Y": {"math_mcq": 0.80, "code": 0.70, "support_chat": 0.80, "extraction": 0.85}}
bench_mix   = {"math_mcq": 0.7, "code": 0.3, "support_chat": 0.0, "extraction": 0.0}   # what the benchmark tests
product_mix = {"math_mcq": 0.0, "code": 0.1, "support_chat": 0.6, "extraction": 0.3}   # what our users do
for name, mix in (("benchmark mix", bench_mix), ("product mix", product_mix)):
    sc = {m: sum(mix[t] * v for t, v in s.items()) for m, s in skills.items()}
    print(f"{name:14s}", {m: round(v, 3) for m, v in sc.items()}, "winner:", max(sc, key=sc.get))

# 2) Format sensitivity: a mock multiple-choice model that knows 50% of answers (assumed) and
#    otherwise guesses with a bias toward letter A (assumed 40% A, 20% each other).
def run(correct_slot_fn, n=20000):
    ok = 0
    for _ in range(n):
        gold = correct_slot_fn()
        if random.random() < 0.5: pick = gold
        else: pick = random.choices("ABCD", [0.4, 0.2, 0.2, 0.2])[0]
        ok += pick == gold
    return ok / n
print("accuracy, gold always listed as A:", round(run(lambda: "A"), 3))
print("accuracy, gold in random slot    :", round(run(lambda: random.choice("ABCD")), 3))
