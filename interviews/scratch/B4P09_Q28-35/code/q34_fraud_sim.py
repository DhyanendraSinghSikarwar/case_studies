"""Q34: validate the feature-spec YAML, then simulate velocity features. CONCEPT/SIMULATION only: no Kafka, Flink, Redis or real model."""
import sys, random, yaml
from collections import deque, defaultdict

spec = yaml.safe_load(open(sys.argv[1]))

# ---- 1. spec validation
KINDS = {"velocity_count", "velocity_sum", "distinct_count", "batch_rate", "graph_batch"}
errs = []
if sum(spec["budget_split_ms"].values()) != spec["decision_budget_ms"]:
    errs.append("budget split does not add up")
for f in spec["features"]:
    if f["entity"] not in spec["entities"]: errs.append(f"{f['name']}: unknown entity")
    if f["kind"] not in KINDS: errs.append(f"{f['name']}: unknown kind")
    if f["freshness"] not in {"stream", "daily"}: errs.append(f"{f['name']}: bad freshness")
    if f["kind"].startswith("velocity") and "window" not in f: errs.append(f"{f['name']}: velocity needs window")
    if "on_missing" not in f: errs.append(f"{f['name']}: no missing-value policy")
print("spec errors:", errs or "none", "| features:", len(spec["features"]), "| budget sum:", sum(spec["budget_split_ms"].values()), "ms")

# ---- 2. velocity features over a seeded stream (event time in seconds)
rng = random.Random(11)
events = []
for i in range(40):                                  # normal traffic: 5 cards, spread over ~2 hours
    events.append((rng.randint(0, 7200), f"card{rng.randint(1, 5)}", f"dev{rng.randint(1, 5)}", round(rng.uniform(100, 2000), 2)))
for k in range(8):                                   # attack: card9 tested from 4 devices within ~50 s
    events.append((6000 + k * 7, "card9", f"devX{k % 4}", 4999.0))
events.sort()

W = {"1m": 60, "1h": 3600}
class Velocity:
    def __init__(self): self.by_card = defaultdict(deque); self.by_dev = defaultdict(deque)
    def features(self, now, card, dev, amount):
        """Compute features BEFORE adding the current txn (what a scoring request would see), then add it."""
        for dq, w in ((self.by_card[card], 3600), (self.by_dev[dev], 3600)):
            while dq and dq[0][0] <= now - w: dq.popleft()
        c = self.by_card[card]
        out = {
            "card_txn_count_1m": sum(1 for t, *_ in c if t > now - W["1m"]),
            "card_txn_count_1h": len(c),
            "card_amount_sum_1h": round(sum(a for _, a, _ in c), 2),
            "device_distinct_cards_1h": len({cd for _, cd in self.by_dev[dev]} | {card}),
        }
        c.append((now, amount, dev)); self.by_dev[dev].append((now, card))
        return out

def decide(f, missing):
    # toy rule layer sitting beside a model; thresholds are made up for the demo
    if f["card_txn_count_1m"] >= 3 or f["device_distinct_cards_1h"] >= 4: return "BLOCK"
    if f["card_txn_count_1h"] >= 5: return "REVIEW"
    return "ALLOW"

v = Velocity()
print("\n  time  card   dev    amt   n_1m n_1h  sum_1h  dev_cards  decision")
shown = 0
for now, card, dev, amt in events:
    f = v.features(now, card, dev, amt)
    d = decide(f, [])
    if card == "card9" or (shown < 3 and card != "card9"):
        shown += card != "card9"
        print(f"{now:6d} {card:6s} {dev:6s} {amt:7.0f} {f['card_txn_count_1m']:4d} {f['card_txn_count_1h']:4d} {f['card_amount_sum_1h']:8.0f} {f['device_distinct_cards_1h']:6d}     {d}")

# ---- 3. fallback when the online store cannot answer: spec default + a missing flag that is LOGGED
by_name = {f["name"]: f for f in spec["features"]}
def fetch_with_fallback(store_answer):
    row, flags = {}, {}
    for name, f in by_name.items():
        val = store_answer.get(name)
        flags[name] = val is None
        row[name] = val if val is not None else f["default"]
    return row, flags
row, flags = fetch_with_fallback({"card_txn_count_1m": 2, "card_txn_count_1h": 4})   # store lost the rest
print("\nfallback row:", row)
print("missing flags:", {k: v for k, v in flags.items() if v})
