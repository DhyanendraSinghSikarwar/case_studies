# MOCK toy prompt search. The scorer is a made-up function, not an LLM: each candidate has a
# hidden true accuracy; scoring on a dataset just samples correct/incorrect from it.
import random, itertools

INSTRUCTIONS = ["Classify the ticket.", "You are an expert triager. Pick one label.",
                "Answer with the label only.", "Think carefully, then give the label.",
                "Label the ticket: billing, bug or feature."]
DEMO_SETS = {0: 0.00, 2: 0.03, 4: 0.05, 8: 0.05}       # few-shot demos: made-up gain, saturating

def true_acc(instr_i, k):                                # hidden "ground truth" of the mock
    base = [0.70, 0.72, 0.74, 0.71, 0.75][instr_i]
    return base + DEMO_SETS[k]

def mock_score(candidate, n_items, seed):                # what the optimiser can observe
    rng = random.Random(f"{candidate}-{seed}")
    p = true_acc(*candidate)
    return sum(rng.random() < p for _ in range(n_items)) / n_items

candidates = list(itertools.product(range(len(INSTRUCTIONS)), DEMO_SETS))
print("search space:", len(candidates), "candidates")

for dev_n in (20, 200):
    dev = {c: mock_score(c, dev_n, seed="dev") for c in candidates}     # optimiser sees only this
    best = max(dev, key=dev.get)
    held = mock_score(best, 5000, seed="heldout")                       # fresh data
    oracle = max(candidates, key=lambda c: true_acc(*c))
    print(f"dev set {dev_n:3d}: picked {best} dev {dev[best]:.3f} -> held-out {held:.3f} "
          f"(gap {dev[best]-held:+.3f}); truly best {oracle} at {true_acc(*oracle):.3f}")
