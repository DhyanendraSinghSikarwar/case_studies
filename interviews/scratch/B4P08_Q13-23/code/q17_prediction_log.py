import json, os, tempfile
import numpy as np
from pydantic import BaseModel

class PredictionLog(BaseModel):
    schema_version: int
    request_id: str
    ts: str
    model_version: str
    feature_pipeline: str
    features_raw: dict
    features_model: dict
    score: float
    prediction: int

rng = np.random.default_rng(17)
n = 1000
d = tempfile.mkdtemp()
path = os.path.join(d, "pred.jsonl")
truth = {}
with open(path, "w") as f:
    for i in range(n):
        age = int(rng.integers(21, 65)); inc = float(rng.integers(20, 200)) * 1000
        z = (age - 40) / 20 + (inc - 100000) / 100000
        p = 1 / (1 + np.exp(-z))
        rec = PredictionLog(schema_version=1, request_id=f"r{i:05d}",
              ts=f"2026-10-{1 + i // 40:02d}T10:{i % 60:02d}:00Z", model_version="7", feature_pipeline="2026.10.1",
              features_raw={"age": age, "income": inc}, features_model={"age_z": round((age - 40) / 12, 3), "income_log": round(float(np.log(inc)), 3)},
              score=round(float(p), 4), prediction=int(p >= 0.5))
        f.write(rec.model_dump_json() + "\n")
        truth[rec.request_id] = int(rng.random() < p)
print("rows written:", sum(1 for _ in open(path)), "| first line:")
print(open(path).readline().strip())
# labels arrive late: only 70% of requests have a label yet
labels = {k: v for k, v in truth.items() if int(k[1:]) % 10 < 7}
rows = [PredictionLog.model_validate_json(l) for l in open(path)]
joined = [(r, labels[r.request_id]) for r in rows if r.request_id in labels]
acc = sum(r.prediction == y for r, y in joined) / len(joined)
print(f"matured labels: {len(joined)} of {n} ({len(joined)/n:.0%}); accuracy on matured subset: {acc:.3f}")
# duplicate request ids would break the join: check
ids = [r.request_id for r in rows]
print("duplicate request ids:", len(ids) - len(set(ids)))
