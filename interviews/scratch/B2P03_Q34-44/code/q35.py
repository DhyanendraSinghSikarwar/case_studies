# SYNTHETIC harness: the "model" is a mock whose per-prompt accuracy is made up
# (hidden quality per paraphrase + a penalty for some example orders). It shows how
# to MEASURE sensitivity; the numbers say nothing about any real LLM.
import random, statistics, itertools

PARAPHRASES = {
    "p1 'Classify the sentiment.'":              0.86,
    "p2 'Is this review positive or negative?'": 0.82,
    "p3 'Sentiment (pos/neg):'":                 0.74,
    "p4 'Label the review. Answer pos or neg.'": 0.85,
    "p5 'What does the writer feel?'":           0.66,
}
EXAMPLES = ["ex_pos_1", "ex_pos_2", "ex_neg_1", "ex_neg_2"]

def mock_model(base_acc, example_order, rng):
    acc = base_acc
    if example_order[-1].startswith("ex_pos"):   # fake 'recency bias' toward the last label
        acc -= 0.04
    return rng.random() < acc                     # one test item: correct or not

def pass_rate(base_acc, order, n_items=200, seed=0):
    rng = random.Random(seed)
    return sum(mock_model(base_acc, order, rng) for _ in range(n_items)) / n_items

print("A) paraphrase spread (fixed example order, 200 items, seed 0)")
rates = {}
for name, acc in PARAPHRASES.items():
    rates[name] = pass_rate(acc, EXAMPLES)
    print(f"   {name:44s} {rates[name]:.3f}")
v = list(rates.values())
print(f"   min {min(v):.3f}  max {max(v):.3f}  spread {max(v)-min(v):.3f}  mean {statistics.mean(v):.3f}")

print("B) example-order sensitivity for p1 (all 24 orders)")
orders = list(itertools.permutations(EXAMPLES))
r = [pass_rate(PARAPHRASES["p1 'Classify the sentiment.'"], list(o)) for o in orders]
print(f"   min {min(r):.3f}  max {max(r):.3f}  stdev {statistics.pstdev(r):.3f}")

print("C) seed noise for p1, fixed order (10 seeds)")
s = [pass_rate(0.86, EXAMPLES, seed=k) for k in range(10)]
print(f"   min {min(s):.3f}  max {max(s):.3f}  stdev {statistics.pstdev(s):.3f}")
print("   -> only treat a prompt change as real if it beats this seed noise AND holds across paraphrases")
