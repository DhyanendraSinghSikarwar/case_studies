"""Q21: tamper-evident decision log (hash chain), reason-code stability test and a fairness slice report. Invented data, stdlib only."""
import json, hashlib, random, copy
random.seed(21)
GENESIS = "0" * 64
def h(rec_wo_hash, prev): return hashlib.sha256((prev + json.dumps(rec_wo_hash, sort_keys=True, separators=(",", ":"))).encode()).hexdigest()
class Log:
    def __init__(self): self.rows = []
    def append(self, rec):
        prev = self.rows[-1]["hash"] if self.rows else GENESIS
        self.rows.append({**rec, "prev": prev, "hash": h(rec, prev)})
    def verify(self):
        prev = GENESIS
        for i, r in enumerate(self.rows):
            body = {k: v for k, v in r.items() if k not in ("prev", "hash")}
            if r["prev"] != prev or r["hash"] != h(body, prev): return i
            prev = r["hash"]
        return None                                     # None = chain intact

# scorecard (invented): points per feature; reason codes = features that cost the most points vs a reference applicant
W = {"missed_payments": -40, "utilisation": -30, "income_stability": 25, "tenure_years": 8}
REF = {"missed_payments": 0, "utilisation": 0.2, "income_stability": 1.0, "tenure_years": 5}
BASE, CUT = 600, 560
def score(x): return BASE + sum(W[k] * (x[k] - REF[k]) for k in W)
def reasons(x, n=2):
    loss = sorted(((W[k] * (x[k] - REF[k]), k) for k in W))[:n]
    return [k for v, k in loss if v < 0]
MODEL, FEATS = "scorecard-2026.10", "fv-17"
apps = []
for i in range(400):
    g = random.choice(["A", "B"])
    x = {"missed_payments": random.choice([0, 0, 0, 1, 2, 3]), "utilisation": round(random.uniform(0.05, 0.95), 2),
         "income_stability": round(random.uniform(0.3, 1.0), 2), "tenure_years": random.randint(0, 15)}
    apps.append((f"app-{i:04d}", g, x))
log = Log()
for aid, g, x in apps:
    s = score(x)
    log.append({"app_id_hash": hashlib.sha256(("salt-demo" + aid).encode()).hexdigest()[:16],   # no raw id in the log
                "model": MODEL, "feature_set": FEATS, "score": round(s, 1), "decision": "approve" if s >= CUT else "decline",
                "reasons": reasons(x) if s < CUT else [], "override": None, "ts": f"2026-10-26T10:{i//60:02d}:{i%60:02d}Z"})
log.rows[7]["override"] = {"by": "officer-9", "to": "approve", "why": "documented income proof"}   # (legit overrides are NEW appended rows in practice)
log.rows[7]["hash"] = h({k: v for k, v in log.rows[7].items() if k not in ("prev", "hash")}, log.rows[7]["prev"])
# ^ re-hashing one row without re-chaining the next one is exactly what the verifier must catch
print("verify after in-place edit of row 7 with re-hash only that row ->", "first bad row", log.verify())
log.rows[7].pop("override"); log.rows[7]["override"] = None
log.rows[7]["hash"] = h({k: v for k, v in log.rows[7].items() if k not in ("prev", "hash")}, log.rows[7]["prev"])
assert log.verify() is None; print("restored; chain intact:", log.verify() is None, "rows:", len(log.rows))
t = copy.deepcopy(log); t.rows[100]["decision"] = "approve" if t.rows[100]["decision"] == "decline" else "decline"
print("edit decision in row 100 ->", "first bad row", t.verify())
t = copy.deepcopy(log); del t.rows[50]
print("delete row 50 ->", "first bad row", t.verify())
t = copy.deepcopy(log); t.rows[-1]["score"] += 1
print("edit the LAST row ->", "first bad row", t.verify(), "(an attacker who edits the tail and rehashes it is only caught if the head hash is anchored elsewhere)")
assert t.verify() == len(t.rows) - 1

# reason-code stability: tiny input noise should rarely change the top reason
def stable(frac_noise=0.02, trials=300):
    same = tot = 0
    for _, _, x in apps:
        if score(x) >= CUT: continue
        base = reasons(x, 1)
        for _ in range(3):
            y = {k: (v * (1 + random.uniform(-frac_noise, frac_noise)) if k in ("utilisation", "income_stability") else v) for k, v in x.items()}
            tot += 1; same += reasons(y, 1) == base
    return same / tot
print(f"top reason unchanged under +-2% noise on continuous inputs: {stable():.1%}  (release gate: >= 95%)")
# fairness slice report per release (selection rate ratio; four-fifths rule of thumb, NOT a legal test)
sel = {}
for (aid, g, x), r in zip(apps, log.rows): sel.setdefault(g, []).append(r["decision"] == "approve")
rates = {g: sum(v) / len(v) for g, v in sel.items()}
print("approval rate by slice:", {g: f"{r:.1%} (n={len(sel[g])})" for g, r in rates.items()}, " ratio low/high = %.2f" % (min(rates.values()) / max(rates.values())))
