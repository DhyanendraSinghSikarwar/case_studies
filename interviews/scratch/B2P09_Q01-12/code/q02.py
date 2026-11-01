# Toy golden-set builder: dedupe, stratify, split, leakage check, version hash. Synthetic data.
import hashlib, json, random, re
random.seed(7)

raw = [  # (query, intent) -- synthetic "production" sample
    ("how do i reset my password", "account"), ("how do I reset my password?", "account"),
    ("reset password please", "account"), ("cancel my subscription", "billing"),
    ("i want a refund for last month", "billing"), ("why was i charged twice", "billing"),
    ("refund for double charge", "billing"), ("app crashes on startup", "bug"),
    ("crash when opening settings", "bug"), ("export data to csv", "howto"),
    ("how to export my data as csv", "howto"), ("change email address", "account"),
    ("invoice for march", "billing"), ("dark mode not saving", "bug"),
    ("delete my account", "account"), ("is there an api", "howto"),
]

def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
def toks(s): return set(norm(s).split())
def jaccard(a, b): return len(a & b) / len(a | b)

# 1) near-duplicate removal (Jaccard >= 0.7 on word sets)
kept = []
for q, it in raw:
    if all(jaccard(toks(q), toks(k)) < 0.7 for k, _ in kept):
        kept.append((q, it))
print("raw:", len(raw), "after dedupe:", len(kept))

# 2) stratified view: how many per intent (spot thin strata before labelling)
from collections import Counter
print("per intent:", dict(Counter(it for _, it in kept)))

# 3) split once, deterministically, by hash of the normalised text (stable across reruns)
def bucket(q): return int(hashlib.sha256(norm(q).encode()).hexdigest(), 16) % 100
dev = [x for x in kept if bucket(x[0]) < 40]
test = [x for x in kept if bucket(x[0]) >= 40]
print("dev:", len(dev), "test:", len(test))

# 4) leakage check: golden/test queries vs few-shot examples in the prompt
few_shot = ["how to export my data as csv", "crash when opening settings"]
leaks = [q for q, _ in test + dev for f in few_shot if jaccard(toks(q), toks(f)) >= 0.7]
print("leaked into prompt examples:", sorted(set(leaks)))

# 5) version id = hash of content; changes whenever any case or label changes
def version(rows): return hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()[:8]
v1 = version(kept)
kept2 = kept + [("how do i enable 2fa", "account")]
print("version v1:", v1, "| after adding one case:", version(kept2))
