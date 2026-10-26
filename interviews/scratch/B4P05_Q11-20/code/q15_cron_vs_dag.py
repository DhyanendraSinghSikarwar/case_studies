"""Before: cron-style script. After: tiny orchestrator with order, state, retries, skip-done, audit log.
Deterministic simulation: the 'train' step fails on its first attempt only."""
import json
import tempfile
from pathlib import Path

# ---------- BEFORE: weekly cron script ----------
def cron_script(env):
    print("[cron] start")
    steps = ["extract", "build_features", "train", "evaluate", "register"]
    for s in steps:
        if s == "train" and env["train_fail_budget"] > 0:
            env["train_fail_budget"] -= 1
            print("[cron] train crashed -> script dies; next run is next week; nobody is told")
            return False
        if s == "register":
            env["models_registered"] += 1
        print(f"[cron] {s} ok")
    return True


env = {"train_fail_budget": 1, "models_registered": 0}
print("--- cron week 1"); cron_script(env)
print("--- cron week 2"); cron_script(env)
print("models registered after 2 weeks:", env["models_registered"], "(one week of stale model, no alert)\n")


# ---------- AFTER: same steps, as a DAG with state ----------
class Run:
    def __init__(self, state_dir, fail_budget):
        self.state = Path(state_dir) / "state.json"
        self.audit = []
        self.fail_budget = fail_budget
        self.registered = 0

    def done(self):
        return json.loads(self.state.read_text()) if self.state.exists() else {}

    def mark(self, step):
        d = self.done(); d[step] = "success"; self.state.write_text(json.dumps(d))

    def call(self, step):
        if step == "train" and self.fail_budget > 0:
            self.fail_budget -= 1
            raise RuntimeError("GPU node preempted")
        if step == "register":
            self.registered += 1

    def run(self, dag, retries=2):
        for step, deps in dag:                       # list is already in dependency order
            assert all(d in self.done() for d in deps), f"{step}: upstream not done"
            if step in self.done():
                self.audit.append(f"{step}: skipped (already success)"); continue
            for attempt in range(1, retries + 2):
                try:
                    self.call(step); self.mark(step)
                    self.audit.append(f"{step}: success (attempt {attempt})"); break
                except RuntimeError as e:
                    self.audit.append(f"{step}: attempt {attempt} failed: {e}")
            else:
                self.audit.append(f"ALERT: {step} failed after {retries + 1} attempts"); return False
        return True


DAG = [("extract", []), ("build_features", ["extract"]), ("train", ["build_features"]),
       ("evaluate", ["train"]), ("register", ["evaluate"])]
with tempfile.TemporaryDirectory() as d:
    r = Run(d, fail_budget=1)
    print("--- orchestrated run, train fails once"); ok = r.run(DAG)
    print("\n".join(r.audit)); print("run ok:", ok, "| registered:", r.registered)
    r.audit.clear()
    print("--- same run again (rerun / duplicate trigger)"); r.run(DAG)
    print("\n".join(r.audit)); print("registered after rerun:", r.registered)
with tempfile.TemporaryDirectory() as d:
    r = Run(d, fail_budget=5)
    print("--- permanent failure"); ok = r.run(DAG)
    print("\n".join(r.audit[-4:])); print("run ok:", ok, "| registered:", r.registered)
