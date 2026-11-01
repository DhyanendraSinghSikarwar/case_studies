# Skeleton of a multi-team eval platform core (in-memory, mock grader). Shows: content-hash versioning, runs, CI gate, budget, review queue.
import hashlib, json, random
def vhash(obj): return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:8]
class Registry:                                              # immutable, content-addressed artifacts: datasets, prompts, graders
    def __init__(self): self.items = {}
    def put(self, kind, name, content):
        v = vhash(content); self.items[(kind, name, v)] = content; return f"{name}@{v}"
    def get(self, kind, ref):
        name, v = ref.split("@"); return self.items[(kind, name, v)]
reg = Registry(); runs = []
ds = reg.put("dataset", "support_qa", [{"id": i, "q": f"q{i}", "label": i % 3 != 0} for i in range(60)])
ds_same = reg.put("dataset", "support_qa", [{"id": i, "q": f"q{i}", "label": i % 3 != 0} for i in range(60)])
ds_v2 = reg.put("dataset", "support_qa", [{"id": i, "q": f"q{i}", "label": i % 3 != 0} for i in range(61)])
print("same content -> same version:", ds == ds_same, "| one case added -> new version:", ds != ds_v2, f"({ds}, {ds_v2})")
pr1 = reg.put("prompt", "answer", {"template": "Answer briefly: {q}"}); pr2 = reg.put("prompt", "answer", {"template": "Answer briefly and cite: {q}"})
gr = reg.put("grader", "correct", {"type": "mock_judge", "rubric": "pass if correct"})
class Budget:
    def __init__(self, usd): self.left = usd
    def charge(self, usd):
        if usd > self.left: raise RuntimeError("budget exceeded")
        self.left -= usd
def run_eval(team, prompt_ref, dataset_ref, grader_ref, skill, budget, cost_per_call=0.002, seed=0):
    rnd = random.Random(vhash([prompt_ref, dataset_ref, seed])); rows = []
    for case in reg.get("dataset", dataset_ref):
        budget.charge(cost_per_call * 2)                     # one generation + one judge call (assumed prices, not real)
        ok = rnd.random() < skill; rows.append({"id": case["id"], "pass": ok, "judge_conf": round(rnd.random(), 2)})
    rec = {"run_id": f"run{len(runs)+1}", "team": team, "prompt": prompt_ref, "dataset": dataset_ref, "grader": grader_ref,
           "score": sum(r["pass"] for r in rows) / len(rows), "rows": rows}
    runs.append(rec); return rec
def ci_gate(base, cand, max_drop=0.03):
    pairs = [(a["pass"], b["pass"]) for a, b in zip(base["rows"], cand["rows"])]
    b = sum(1 for x, y in pairs if x and not y); c = sum(1 for x, y in pairs if y and not x)
    drop = base["score"] - cand["score"]
    return {"score_drop": round(drop, 3), "regressed_cases": b, "improved_cases": c, "decision": "BLOCK" if drop > max_drop else "PASS"}
bud = Budget(0.60)
base = run_eval("support", pr1, ds, gr, 0.80, bud)
cand = run_eval("support", pr2, ds, gr, 0.70, bud)
print("baseline", base["run_id"], round(base["score"], 3), "| candidate", cand["run_id"], round(cand["score"], 3), "| budget left $", round(bud.left, 3))
print("CI gate:", ci_gate(base, cand))
print("run record links:", {k: cand[k] for k in ("prompt", "dataset", "grader")})
queue = sorted(cand["rows"], key=lambda r: abs(r["judge_conf"] - 0.5))[:5]       # review the cases the judge is least sure about
print("human review queue (id, judge_conf):", [(r["id"], r["judge_conf"]) for r in queue])
tiny = Budget(0.05)
try: run_eval("growth", pr1, ds, gr, 0.8, tiny)
except RuntimeError as e: print("per-team budget stops the run:", e, "| left $", round(tiny.left, 3))
