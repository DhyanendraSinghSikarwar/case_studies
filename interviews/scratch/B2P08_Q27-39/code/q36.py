# TOY classifier: sorts SYNTHETIC failure traces into the three MAST category names by simple rules, then tallies.
# The rules and symptom labels are MY illustrative reading, not MAST's 14 failure modes (I do not reproduce them here).
from collections import Counter
CATEGORIES = ("system design issues", "inter-agent misalignment", "task verification")
RULES = [  # (symptom, category) first match wins
    ("two agents claim the same role", CATEGORIES[0]),
    ("no stop condition, loop continues", CATEGORIES[0]),
    ("agent ignores peer message", CATEGORIES[1]),
    ("handoff dropped required context", CATEGORIES[1]),
    ("conflicting assumptions never reconciled", CATEGORIES[1]),
    ("final answer accepted without check", CATEGORIES[2]),
    ("verifier only reads own summary", CATEGORIES[2]),
]
def classify(trace):
    for symptom, cat in RULES:
        if symptom in trace["symptoms"]: return cat
    return "unclassified"
traces = [  # synthetic, hand-written
    {"id": 1, "symptoms": ["no stop condition, loop continues"]},
    {"id": 2, "symptoms": ["handoff dropped required context", "final answer accepted without check"]},
    {"id": 3, "symptoms": ["final answer accepted without check"]},
    {"id": 4, "symptoms": ["agent ignores peer message"]},
    {"id": 5, "symptoms": ["two agents claim the same role"]},
    {"id": 6, "symptoms": ["verifier only reads own summary"]},
    {"id": 7, "symptoms": ["tool timeout"]},
    {"id": 8, "symptoms": ["conflicting assumptions never reconciled"]},
]
tally = Counter(classify(t) for t in traces)
for c in CATEGORIES + ("unclassified",): print(f"{c:26} {tally.get(c, 0)}")
# a trace with several symptoms shows why single-label rules are a simplification (trace 2 has two)
print("trace 2 labelled:", classify(traces[1]), "(a multi-label reading would also add task verification)")
assert sum(tally.values()) == len(traces) and tally["unclassified"] == 1 and tally[CATEGORIES[2]] == 2
print("tests passed")
