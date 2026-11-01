# Feast local provider + SQLite online store, own repo dir. Timings are sandbox-only, in-process, no network.
import os, sys, time, random, statistics, warnings, shutil
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from datetime import datetime, timedelta, timezone

REPO = "/tmp/claude-0/b9_q19_27/feast_repo"
shutil.rmtree(REPO, ignore_errors=True); os.makedirs(REPO + "/data")
NF = {"user": 20, "merchant": 12, "device": 8}     # 40 features over 3 entities
N_ENT = 2000
open(REPO + "/feature_store.yaml", "w").write("""project: latency_demo
registry: data/registry.db
provider: local
online_store:
  type: sqlite
  path: data/online.db
offline_store:
  type: file
entity_key_serialization_version: 3
""")
open(REPO + "/defs.py", "w").write(f"""
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Float32
NF = {NF!r}
ents = {{k: Entity(name=k + "_id", join_keys=[k + "_id"], value_type=ValueType.INT64) for k in NF}}
fvs = []
for k, n in NF.items():
    src = FileSource(path=f"data/{{k}}.parquet", timestamp_field="event_ts")
    fvs.append(FeatureView(name=k + "_feats", entities=[ents[k]], ttl=timedelta(days=3650),
        schema=[Field(name=f"{{k}}_f{{i}}", dtype=Float32) for i in range(n)], source=src))
""")
rng = np.random.default_rng(27); random.seed(27)
now = datetime.now(timezone.utc).replace(microsecond=0)
for k, n in NF.items():
    df = pd.DataFrame(rng.random((N_ENT, n)).astype("float32"), columns=[f"{k}_f{i}" for i in range(n)])
    df.insert(0, f"{k}_id", np.arange(N_ENT)); df["event_ts"] = now - timedelta(hours=1)
    df.to_parquet(f"{REPO}/data/{k}.parquet")

os.chdir(REPO); sys.path.insert(0, REPO)
import feast, defs
from feast import FeatureStore
print("feast", feast.__version__, "pandas", pd.__version__)
fs = FeatureStore(REPO)
fs.apply(list(defs.ents.values()) + defs.fvs)
fs.materialize(now - timedelta(days=1), now)
refs = [f"{k}_feats:{k}_f{i}" for k, n in NF.items() for i in range(n)]
print("features requested:", len(refs), "over", len(NF), "entities")
chk = fs.get_online_features(features=refs, entity_rows=[{"user_id": 5, "merchant_id": 35, "device_id": 65}]).to_dict()
print("check: values returned =", sum(1 for k, v in chk.items() if k.endswith(tuple("0123456789")) and v[0] is not None), "of", len(refs))

def timeit(fn, reps=30):
    fn()                                         # warm up
    ts = []
    for _ in range(reps):
        t = time.perf_counter(); fn(); ts.append((time.perf_counter() - t) * 1000)
    ts.sort(); return statistics.median(ts), ts[int(0.9 * (len(ts) - 1))]

def row(i): return {"user_id": i, "merchant_id": (i * 7) % N_ENT, "device_id": (i * 13) % N_ENT}

# A: worst pattern - one call per feature (40 calls for ONE request)
def a(): [fs.get_online_features(features=[r], entity_rows=[row(5)]) for r in refs]
# B: one call per entity type (3 calls)
def b(): [fs.get_online_features(features=[r for r in refs if r.startswith(k)], entity_rows=[row(5)]) for k in NF]
# C: one call, all 40 features, the three entity ids in one row
def c(): fs.get_online_features(features=refs, entity_rows=[row(5)])
# D: batch scoring 50 requests in ONE call vs 50 calls of C
rows50 = [row(i) for i in range(50)]
def d1(): fs.get_online_features(features=refs, entity_rows=rows50)
def d2(): [fs.get_online_features(features=refs, entity_rows=[r]) for r in rows50]

print(f"{'pattern':58s} median_ms  p90_ms   (sandbox only)")
res = {}
for label, fn, reps in [("A 40 calls, 1 feature each, 1 request", a, 5), ("B 3 calls, one per entity, 1 request", b, 15),
                        ("C 1 call, 40 features, 1 request", c, 30), ("D1 1 call, 40 features, 50 requests", d1, 10),
                        ("D2 50 calls of C (50 requests)", d2, 3)]:
    res[label[:2].strip()] = timeit(fn, reps); m, p = res[label[:2].strip()]
    print(f"{label:58s} {m:8.1f} {p:8.1f}")

# missing entity and defaults
out = fs.get_online_features(features=refs[:2] + [refs[20]], entity_rows=[{"user_id": 1, "merchant_id": 99999, "device_id": 3}]).to_dict()
print("unknown merchant ->", {k: v for k, v in out.items() if k != "user_id"})
DEFAULTS = {"merchant_f0": 0.0}
v = out["merchant_f0"][0]; print("with default + missing flag:", (DEFAULTS["merchant_f0"] if v is None else v), "| merchant_missing =", v is None)

# hot keys with a tiny in-process cache (seeded Zipf-like traffic)
from collections import OrderedDict
keys = [min(int(x), N_ENT - 1) for x in rng.zipf(1.3, 3000)]
cache, hits, cap = OrderedDict(), 0, 50
for k_ in keys:
    if k_ in cache: hits += 1; cache.move_to_end(k_)
    else:
        cache[k_] = 1
        if len(cache) > cap: cache.popitem(last=False)
print(f"hot-key demo: 3000 requests, LRU cache of {cap} merchants, hit rate = {hits/3000:.0%} (traffic skew is an assumption)")

# latency budget (planning arithmetic; the allocation numbers are ASSUMPTIONS, not measurements)
budget = {"network in+out": 8, "request parsing + validation": 3, "feature fetch (all 3 entities, one batched call)": 15,
          "model inference": 16, "slack for tail / GC": 8}
total = 50; used = sum(budget.values())
print("\nbudget (ms)                                            allotted")
for k_, v_ in budget.items(): print(f"{k_:52s} {v_:5d}")
print(f"{'sum':52s} {used:5d}  (budget {total} ms, sum matches: {used == total}; slack row is the headroom)")
m_c = res["C"][0]
print(f"measured in-process lookup C (median) = {m_c:.1f} ms vs allotted 15 ms (no network; a remote store adds a round trip per call)")
print("ASSUMED remote store, 3 sequential round trips of 4 ms each:", 3 * 4, "ms vs one batched trip:", 4, "ms")
