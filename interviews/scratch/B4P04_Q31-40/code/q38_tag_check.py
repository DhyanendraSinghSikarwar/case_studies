"""Flag runs missing mandatory tags / badly formed tags. usage: python -I q38_tag_check.py TRACKING_URI
In production this would run as a nightly job and post to chat; here it just prints."""
import re, sys, mlflow
from mlflow.tracking import MlflowClient

REQUIRED = {                      # tag -> regex it must match
    "git_sha":  r"[0-9a-f]{7,40}",
    "data_hash": r"[0-9a-f]{8,64}",
    "owner":    r"[a-z][a-z0-9._-]+",
    "project":  r"[a-z][a-z0-9-]+",
}
NAME_RULE = r"[a-z0-9-]+/[a-z0-9-]+/[a-z0-9-]+"       # team/project/purpose

def check(run, exp_name):
    problems = []
    if not re.fullmatch(NAME_RULE, exp_name): problems.append(f"experiment name '{exp_name}' is not team/project/purpose")
    for k, pat in REQUIRED.items():
        v = run.data.tags.get(k)
        if v is None: problems.append(f"missing {k}")
        elif not re.fullmatch(pat, v): problems.append(f"bad {k}='{v}'")
    return problems

mlflow.set_tracking_uri(sys.argv[1]); c = MlflowClient(); bad = total = 0
for e in c.search_experiments():
    for r in c.search_runs([e.experiment_id]):
        total += 1; p = check(r, e.name)
        if p: bad += 1; print(f"FAIL run={r.info.run_id[:8]} owner={r.data.tags.get('owner','?')}: " + "; ".join(p))
        else: print(f"ok   run={r.info.run_id[:8]}")
print(f"{bad} of {total} runs fail the policy"); sys.exit(1 if bad else 0)
