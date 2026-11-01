# Q26: promotion gate and registry audit. Plain Python, illustrative numbers; not tied to any registry product.
import random
random.seed(26)
FULL_ROWS = 4_000_000
# 41 registered versions; row counts come from the experiment-tracking run, not from the registry (the registry only has name, number, metric)
versions = []
for v in range(1, 42):
    rows = int(FULL_ROWS * random.uniform(0.9, 1.05))
    versions.append({"version": v, "metric": round(random.uniform(0.80, 0.84), 3), "rows": rows})
versions[37]["rows"] = int(FULL_ROWS * 0.05)           # version 38: the 5% sample
versions[11]["rows"] = int(FULL_ROWS * 0.01)           # version 12: a 1% smoke-test run nobody else knew about
assert versions[37]["version"] == 38 and versions[37]["rows"] == 200_000
# 1) audit: any version trained on far fewer rows than the median
rows_sorted = sorted(v["rows"] for v in versions)
median = rows_sorted[len(rows_sorted) // 2]
flagged = [v["version"] for v in versions if v["rows"] < 0.5 * median]
print(f"median training rows = {median:,}; flagged versions (below 50% of median): {flagged}")
assert flagged == [12, 38]
# 2) exposure of the mistake: two days at an illustrative 100 requests per second
exposed = 100 * 48 * 3600
print(f"requests served by version 38 in 48 hours at 100 rps: {exposed:,}")
assert exposed == 17_280_000
# 3) the promotion gate: required metadata, sanity bounds, separation of duties
REQUIRED = ["git_commit", "data_version", "train_rows", "sampling_fraction", "holdout_id", "holdout_metric", "trainer", "approver"]
def gate(meta, expected_rows=FULL_ROWS):
    errs = [f"missing {k}" for k in REQUIRED if meta.get(k) in (None, "")]
    if errs: return errs
    if meta["sampling_fraction"] < 1.0: errs.append("trained on a sample")
    if meta["train_rows"] < 0.8 * expected_rows: errs.append("train_rows below 80% of expected")
    if meta["trainer"] == meta["approver"]: errs.append("trainer cannot approve own promotion")
    return errs
good = dict(git_commit="a1b2c3", data_version="d41", train_rows=4_020_000, sampling_fraction=1.0, holdout_id="h7",
            holdout_metric=0.83, trainer="asha", approver="ravi")
v38 = dict(good, train_rows=200_000, sampling_fraction=0.05)
legacy = {"name": "m", "version": 38, "metric": 0.81}            # what the registry stores today
print("good candidate:", gate(good))
print("version 38 as it should have been recorded:", gate(v38))
print("version 38 as the registry stores it:", gate(legacy)[:3], "...", len(gate(legacy)), "missing fields")
assert gate(good) == [] and "trained on a sample" in gate(v38) and len(gate(legacy)) == 8
assert gate(dict(good, approver="asha")) == ["trainer cannot approve own promotion"]
# 4) a green metric on the old holdout is not evidence of the training data: same metric range for both
print("metric alone cannot find it: v38 metric", versions[37]["metric"], "vs median metric", sorted(v["metric"] for v in versions)[20])
assert 0.80 <= versions[37]["metric"] <= 0.84
