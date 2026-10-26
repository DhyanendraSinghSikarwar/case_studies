# Book 4 Part 9, Q1-Q9 answers (Wave B)

### Q1 ⭐⭐⭐ 🟢 What is a feature store and what problem does it solve? Define entity, feature, feature view (or feature group), offline store, online store and registry, and say what a feature store is not (it is not a model store, not a data warehouse replacement, not always needed). Give the honest case for and against one for a team with three models. Stand up a minimal local Feast repo (a Parquet file source, one entity, one feature view, a SQLite online store), run feast apply, and print what the registry now holds.
**Asked at:** Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs | Feature-store product docs and write-ups (Feast docs on point-in-time joins and materialize and materialize-incremental, old v0.14 and v0.16 branches; an oneuptime.com Feast late-rows post; AWS SageMaker Unified Studio feature-group docs on online and offline stores and TTL; Databricks materialized-features docs; geeksforgeeks online vs offline store page; search snippets only, not opened); vendor docs and blogs, not interview reports; MLOps and ML platform roles; Feast 0.67.0 was also run locally in this sandbox
**Say this first (1 line):** A feature store is a shared, versioned home for ML features that gives training (history, point-in-time) and serving (latest value, low latency) the same definitions.

**Then explain:**
- Vocabulary, in one breath:
  - **Entity**: the thing you key on (user, merchant, device). It has a join key such as `user_id`.
  - **Feature**: one measurable column about an entity, like `txn_count_7d`.
  - **Feature view** (feature group in other tools): a named set of features, one entity, one source, a timestamp column and a TTL.
  - **Offline store**: big history for training (Parquet, warehouse). **Online store**: latest value per key for fast lookups (SQLite here, Redis or DynamoDB in production).
  - **Registry**: the catalogue of definitions (entities, views, sources). It holds metadata, not the data.
- What it is **not**: not a model store (that is the model registry), not a warehouse replacement (the offline store usually sits on top of one), and not mandatory.
- Honest case for, with three models: yes if they share features, need low-latency online lookups, and you have been bitten by training-serving skew or by three teams re-writing the same SQL. No if everything is batch scoring, features are not shared, and a tested SQL or dbt table with a timestamp does the job. The tool is a cost: someone must run the registry, the materialisation jobs and the online store.
- Failure modes: the registry drifts from the code (forgot `apply`), the online store is empty because nobody materialised, and people treat the store as the place where features are computed. Feast does not compute features; it registers, joins and serves them.
- Evidence: Feast 0.67.0 local run below. Version and CLI details change, check current docs.

**Example:** Fraud model needs `txn_count_7d` for user 1. Offline Parquet has rows `(user 1, Jan 1, 3)`, `(user 1, Jan 2, 5)`, `(user 2, Jan 1, 1)`. After `feast apply` the registry holds one entity (`user`), one feature view (`user_stats`, TTL 30 days, two features) and one file source. No row of data is in the registry; the SQLite online table is created but empty until you materialise.

**Code:**
```bash
python3 q01_feast_apply.py /tmp/q01     # run with the Feast venv; it writes the repo, runs `feast apply`, lists the registry
```
```python
# Q1: minimal local Feast repo: Parquet source, 1 entity, 1 feature view, SQLite online store.
import subprocess, sys, textwrap, pathlib, shutil
import pandas as pd

root = pathlib.Path(sys.argv[1]); shutil.rmtree(root, ignore_errors=True)
repo = root / "repo"; repo.mkdir(parents=True)
pd.DataFrame({
    "user_id": [1, 1, 2],
    "event_ts": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-01"]),
    "txn_count_7d": [3, 5, 1],
    "avg_amount_7d": [200.0, 220.0, 90.0],
}).to_parquet(repo / "user_stats.parquet")

(repo / "feature_store.yaml").write_text(textwrap.dedent(f"""\
    project: q01demo
    provider: local
    registry: {root}/registry.db
    online_store:
      type: sqlite
      path: {root}/online.db
    offline_store:
      type: file
    entity_key_serialization_version: 3
    """))
(repo / "definitions.py").write_text(textwrap.dedent(f"""\
    from datetime import timedelta
    from feast import Entity, FeatureView, Field, FileSource
    from feast.types import Float32, Int64
    from feast.value_type import ValueType

    user = Entity(name="user", join_keys=["user_id"], value_type=ValueType.INT64)
    src = FileSource(path="{repo}/user_stats.parquet", timestamp_field="event_ts")
    user_stats = FeatureView(
        name="user_stats", entities=[user], ttl=timedelta(days=30),
        schema=[Field(name="txn_count_7d", dtype=Int64),
                Field(name="avg_amount_7d", dtype=Float32)],
        source=src)
    """))
feast = str(pathlib.Path(sys.executable).parent / "feast")
r = subprocess.run([feast, "apply"], cwd=repo, capture_output=True, text=True)
print(r.stdout.strip()); print("rc =", r.returncode, r.stderr.strip()[-300:] if r.returncode else "")

from feast import FeatureStore
fs = FeatureStore(repo_path=str(repo))
print("entities     :", [(e.name, e.join_key) for e in fs.list_entities()])
for fv in fs.list_feature_views():
    print("feature view :", fv.name, "| ttl:", fv.ttl, "| features:", [f.name + ":" + str(f.dtype) for f in fv.features],
          "| source:", type(fv.batch_source).__name__)
print("data sources :", [s.name for s in fs.list_data_sources()])
print("files created:", sorted(p.name for p in root.iterdir()))
```

**Output (my run):** Feast 0.67.0, pandas 2.3.3, Python 3.13, local provider. Real output:
```text
No project found in the repository. Using project name q01demo defined in feature_store.yaml
Applying changes for project q01demo
Created project q01demo
Created entity user
Created feature view user_stats
Created sqlite table q01demo_user_stats
rc = 0 
entities     : [('user', 'user_id')]
feature view : user_stats | ttl: 30 days, 0:00:00 | features: ['txn_count_7d:Int64', 'avg_amount_7d:Float32'] | source: FileSource
data sources : ['/tmp/claude-0/b9_q01_09/q01/repo/user_stats.parquet']
files created: ['online.db', 'registry.db', 'repo']
```
Nothing was run against a cloud store or a managed feature store (Tecton, Hopsworks, SageMaker, Vertex): not executed.

**Follow-ups:**
- *Does Feast compute my features?* No. You compute them elsewhere (SQL, Spark, a stream job) and Feast registers, joins and serves them. Some products add transformations; check current docs.
- *Where do the registry and online store live in production?* A SQL or object-store registry and Redis, DynamoDB or similar online store, per the docs of your version.
- *Is a feature store a data warehouse replacement?* No. It sits on top of the warehouse or lake and adds time-travel joins, serving and shared definitions.

**Common mistakes:**
- Saying "it stores features" without naming the two stores and the different access patterns.
- Adopting one for a single batch model.
- Forgetting that `apply` only writes definitions; the online store stays empty until `materialize`.

---

### Q2 ⭐⭐⭐ 🟢 Online store versus offline store: how are they different in access pattern (point lookup by key versus large scans by time range), storage technology (Parquet or warehouse versus Redis, DynamoDB or SQLite), latency, retention, consistency and cost? Explain how data moves between them (materialisation) and what can go wrong when they disagree. Using a local Feast repo, read the same entity from both stores and show the different shapes (a history of rows versus the latest row).
**Asked at:** Feature-store product docs and write-ups (Feast docs on point-in-time joins and materialize and materialize-incremental, old v0.14 and v0.16 branches; an oneuptime.com Feast late-rows post; AWS SageMaker Unified Studio feature-group docs on online and offline stores and TTL; Databricks materialized-features docs; geeksforgeeks online vs offline store page; search snippets only, not opened); vendor docs and blogs, not interview reports; MLOps and ML platform roles; Feast 0.67.0 was also run locally in this sandbox | Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs
**Say this first (1 line):** The offline store keeps history and is scanned by time; the online store keeps only the latest row per key and is read by key in milliseconds; materialisation copies from the first to the second.

**Then explain:**
| | Offline store | Online store |
|---|---|---|
| Access pattern | big scans, joins over a time range, as-of lookups | point lookup by entity key |
| Technology | Parquet on object storage, warehouse | Redis, DynamoDB, SQLite (local demos) |
| Latency need | seconds to hours is fine | tight request budget (milliseconds); measure it yourself |
| Retention | full history (months or years) | usually the latest value only, plus a TTL |
| Cost shape | cheap storage, pay per scan | pricey per GB (memory or provisioned reads), small data |
| Consistency | immutable history, you can re-read it | overwritten in place, eventually consistent with offline |
- Data moves by **materialisation**: a job reads a time window from offline and writes the newest row per key online. Streams can also push straight to online.
- What goes wrong when they disagree: the model trained on one value and served another (skew); a failed or late materialisation leaves stale values; a deleted source row stays online; a stream path and a batch path compute differently. Fix with one definition, a freshness check and logging what was served.
- Interview trap: do not say the online store is a cache of the offline store with the same shape. History in, latest row out.
- Check vendor limits and consistency guarantees in current docs.

**Example:** User 1 has rows Jan 1 = 3, Jan 2 = 5, Jan 3 = 8. Offline can answer "what was it at noon on Jan 2" (5). Online answers only "now" (8). A new Jan 4 row lands (13) and nobody materialises: offline as-of Jan 4 says 13, online still says 8.

**Code:**
```python
# Helper shared by the Feast demos: builds a throw-away local repo and runs `feast apply`.
import pathlib, shutil, subprocess, sys, textwrap
import pandas as pd

def make_repo(root, df, ttl_days=30, project="demo"):
    root = pathlib.Path(root); shutil.rmtree(root, ignore_errors=True)
    repo = root / "repo"; repo.mkdir(parents=True)
    df.to_parquet(repo / "user_stats.parquet")
    (repo / "feature_store.yaml").write_text(textwrap.dedent(f"""\
        project: {project}
        provider: local
        registry: {root}/registry.db
        online_store:
          type: sqlite
          path: {root}/online.db
        offline_store:
          type: file
        entity_key_serialization_version: 3
        """))
    ttl = f"timedelta(days={ttl_days})" if ttl_days else "None"
    (repo / "definitions.py").write_text(textwrap.dedent(f"""\
        from datetime import timedelta
        from feast import Entity, FeatureView, Field, FileSource
        from feast.types import Float32, Int64
        from feast.value_type import ValueType
        user = Entity(name="user", join_keys=["user_id"], value_type=ValueType.INT64)
        src = FileSource(path="{repo}/user_stats.parquet", timestamp_field="event_ts")
        user_stats = FeatureView(name="user_stats", entities=[user], ttl={ttl},
            schema=[Field(name="txn_count_7d", dtype=Int64), Field(name="avg_amount_7d", dtype=Float32)],
            source=src)
        """))
    feast = str(pathlib.Path(sys.executable).parent / "feast")
    r = subprocess.run([feast, "apply"], cwd=repo, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-500:]
    return repo

def write_rows(repo, df):
    df.to_parquet(pathlib.Path(repo) / "user_stats.parquet")

# ----- next file -----
# Q2: same entity read from the offline store (history, as-of) and the online store (latest row only).
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, __import__("pathlib").Path(__file__).parent.as_posix())
from datetime import datetime
import pandas as pd
from feast import FeatureStore
from feast_common import make_repo, write_rows

rows = pd.DataFrame({
    "user_id": [1, 1, 1, 2],
    "event_ts": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-01"]),
    "txn_count_7d": [3, 5, 8, 1],
    "avg_amount_7d": [200.0, 220.0, 260.0, 90.0],
})
repo = make_repo(sys.argv[1], rows, ttl_days=30, project="q02")
fs = FeatureStore(repo_path=str(repo))
F = ["user_stats:txn_count_7d", "user_stats:avg_amount_7d"]

print("== offline: raw history for user 1 (3 rows) ==")
print(rows[rows.user_id == 1][["user_id", "event_ts", "txn_count_7d"]].to_string(index=False))

print("\n== offline: get_historical_features, one row per (entity, label time) ==")
ent = pd.DataFrame({"user_id": [1, 1, 1], "event_timestamp": pd.to_datetime(["2026-01-01 12:00", "2026-01-02 12:00", "2026-01-03 12:00"])})
h = fs.get_historical_features(entity_df=ent, features=F).to_df().sort_values("event_timestamp")
print(h.to_string(index=False))

fs.materialize(start_date=datetime(2025, 12, 31), end_date=datetime(2026, 1, 4))
print("\n== online: get_online_features for user 1 and 2 (latest row only) ==")
o = fs.get_online_features(features=F, entity_rows=[{"user_id": 1}, {"user_id": 2}]).to_dict()
print(pd.DataFrame(o).to_string(index=False))

print("\n== disagreement: a new row lands offline on Jan 4, nobody re-materialises ==")
new = pd.concat([rows, pd.DataFrame({"user_id": [1], "event_ts": pd.to_datetime(["2026-01-04"]), "txn_count_7d": [13], "avg_amount_7d": [300.0]})])
write_rows(repo, new)
off = fs.get_historical_features(entity_df=pd.DataFrame({"user_id": [1], "event_timestamp": pd.to_datetime(["2026-01-04 12:00"])}), features=F).to_df()
on = fs.get_online_features(features=F, entity_rows=[{"user_id": 1}]).to_dict()
print("offline says txn_count_7d =", int(off.txn_count_7d.iloc[0]), "| online says txn_count_7d =", on["txn_count_7d"][0])
```

**Output (my run):** Feast 0.67.0 local (Parquet offline, SQLite online). Real output (Feast's progress banner for materialize removed):
```text
== offline: raw history for user 1 (3 rows) ==
 user_id   event_ts  txn_count_7d
       1 2026-01-01             3
       1 2026-01-02             5
       1 2026-01-03             8
== offline: get_historical_features, one row per (entity, label time) ==
 user_id           event_timestamp  txn_count_7d  avg_amount_7d
       1 2026-01-01 12:00:00+00:00             3          200.0
       1 2026-01-02 12:00:00+00:00             5          220.0
       1 2026-01-03 12:00:00+00:00             8          260.0
== online: get_online_features for user 1 and 2 (latest row only) ==
 user_id  txn_count_7d  avg_amount_7d
       1             8          260.0
       2             1           90.0
== disagreement: a new row lands offline on Jan 4, nobody re-materialises ==
offline says txn_count_7d = 13 | online says txn_count_7d = 8
```
Redis, DynamoDB or warehouse stores were not executed.

**Follow-ups:**
- *Can the online store serve history?* Not in this design; log served values or keep history offline.
- *Why not serve straight from the warehouse?* Latency and concurrency; warehouses are built for scans.
- *How do you notice they disagree?* Compare logged online values with offline recomputation on a sample and alert on the gap (Part 8 owns the monitoring side).

**Common mistakes:**
- Treating online as the system of record.
- Never checking materialisation freshness.
- Quoting latency numbers from blogs; measure on your own stack.

---

### Q3 ⭐⭐⭐ 🟢 Batch, streaming and on-demand feature computation: how do you decide for a feature like 'transactions in the last 7 days', 'seconds since the last login' and 'is the shipping country the same as the billing country'? Cover freshness needs, cost, complexity and the skew risk of each route. Simulate a rolling 7-day count recomputed daily versus hourly versus per event, and show how stale the batch value is at prediction time.
**Asked at:** Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs | Stream-processing concept sources (Databricks 2017 blog 'Event-time aggregation and watermarking in Apache Spark Structured Streaming', Databricks watermarking deep dive, a codecentric.de Spark and Flink event-time post, an oneuptime late-data post, datadriven.io streaming system design questions; search snippets only, not opened); vendor and practitioner blogs, not interview reports; data engineer and streaming roles
**Say this first (1 line):** Pick the cheapest route that still meets the freshness the model needs: batch if hours of staleness are fine, streaming if minutes matter, on-demand if the value only exists at request time.

**Then explain:**
- **Batch**: scheduled job (SQL, Spark), simplest and cheapest, easiest to backfill and keep identical to training. Cost: the value is as old as the last run.
- **Streaming**: an engine keeps rolling state per key and writes online as events arrive. Fresh, but you now run state, checkpoints, late-data handling and a second code path that must match batch (skew risk).
- **On-demand**: computed inside the request from request inputs plus stored values. Zero staleness, adds latency to the request path, and the same function must be reused offline for training.
- The three features in the question:
  - *Transactions in the last 7 days*: rolling count. Daily batch is fine for a slow-moving signal; fraud may need streaming. Decide by how much the error costs, see the simulation.
  - *Seconds since last login*: changes every second. Store the last-login timestamp and compute the difference on demand. A precomputed number is wrong the moment it is written.
  - *Shipping country equals billing country*: both inputs come in the request. On-demand, trivial, no store.
- Failure modes: batch value reused as if fresh; streaming job restarts and rebuilds state wrongly; on-demand code copied by hand into the training notebook (skew).

**Example:** Seeded events, about 3 per day for 30 days. A daily job at midnight serves the count as of the last midnight. A request at 18:00 sees a count 18 hours old. In my run the daily route was wrong on 59% of 300 requests, off by up to 5 events; hourly was wrong on 12%, off by at most 1; per-event was exact.

**Code:**
```python
# Q3: rolling 7-day count, refreshed daily vs hourly vs per event. Pure Python, seeded.
import bisect, random, statistics
H = 3600.0; DAY = 24 * H; WIN = 7 * DAY
rng = random.Random(7)

# ~3 events per day for 30 days (exponential gaps), timestamps in seconds
events, t = [], 0.0
while t < 30 * DAY:
    t += rng.expovariate(3 / DAY); events.append(t)

def count_7d(at):                      # truth: events in (at - 7d, at]
    return bisect.bisect_right(events, at) - bisect.bisect_right(events, at - WIN)

# 300 prediction requests, days 10..30
preds = sorted(rng.uniform(10 * DAY, 30 * DAY) for _ in range(300))

def run(period):                       # batch job runs every `period` seconds, serves its last output
    stale, err = [], []
    for p in preds:
        computed_at = (p // period) * period if period else p
        served = count_7d(computed_at)
        stale.append(p - computed_at); err.append(abs(served - count_7d(p)))
    return statistics.mean(stale) / H, max(stale) / H, statistics.mean(err), max(err), sum(e > 0 for e in err) / len(err)

print(f"{len(events)} events in 30 days; {len(preds)} prediction requests")
print(f"{'route':<18}{'mean stale (h)':>15}{'max stale (h)':>15}{'mean abs err':>14}{'max abs err':>13}{'share wrong':>13}")
for name, period in [("daily batch", DAY), ("hourly batch", H), ("per event/stream", 0)]:
    ms, xs, me, xe, sw = run(period)
    print(f"{name:<18}{ms:>15.2f}{xs:>15.2f}{me:>14.2f}{xe:>13d}{sw:>13.0%}")

# on-demand features: only the request has the data
def seconds_since_login(last_login_ts, now): return now - last_login_ts
def country_match(ship, bill): return int(ship == bill)
print("\non-demand examples:", seconds_since_login(1000.0, 1042.5), country_match("IN", "IN"), country_match("IN", "AE"))
```

**Output (my run):** pure-Python simulation, seed 7, no Spark, Kafka or Feast involved. The numbers are properties of this synthetic data only.
```text
100 events in 30 days; 300 prediction requests
route              mean stale (h)  max stale (h)  mean abs err  max abs err  share wrong
daily batch                 11.26          23.84          1.08            5          59%
hourly batch                 0.51           0.99          0.12            1          12%
per event/stream             0.00           0.00          0.00            0           0%

on-demand examples: 42.5 1 0
```

**Follow-ups:**
- *How do you decide the refresh period?* Measure how much model quality drops with staleness (replay history at different lags) and compare against the extra cost and complexity.
- *Can one definition serve all three routes?* Ideally yes: one function or SQL, run in batch for training and in the online path, plus a parity test (Q7).
- *What if streaming and batch disagree?* Treat batch as truth, reconcile periodically, and fix the streaming code.

**Common mistakes:**
- Going streaming because it sounds modern.
- Precomputing a time-since feature.
- Forgetting that "7 days" needs an exact boundary rule (Q7).

---

### Q4 ⭐⭐⭐ 🟢 Kafka fundamentals: broker, topic, partition, offset, replication, producer, consumer, consumer group, and why Kafka is a log and not a queue. Explain what is stored where (the log per partition, offsets in __consumer_offsets) and what retention does. No broker is available, so build a small pure-Python partitioned log with append, read-from-offset and committed offsets, run it, and say clearly that no real Kafka broker or client was run.
**Asked at:** Kafka interview question banks (golinuxcloud, dev.to hiteshchawla 'Kafka interview questions for data engineer', datavidhya, DataCamp, Simplilearn, wecreateproblems, adaface, hyring, a techinterview.org post 'Kafka interview questions that separate users from operators', a hackmd Kafka MCQ set; search snippets only, not opened); editorial question lists, not verified candidate reports; data engineer, ML platform and backend roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** Kafka is a distributed, replicated, append-only log split into partitions; consumers just remember an offset, so many groups can read the same data at their own pace and replay it until retention deletes it.

**Then explain:**
- **Broker**: a server storing partitions. **Topic**: a named stream. **Partition**: one ordered log, the unit of parallelism and of ordering. **Offset**: the position of a record inside one partition (not global).
- **Replication**: each partition has a leader and follower copies on other brokers; if the leader dies a follower takes over. Producers choose how many acknowledgements to wait for (`acks`).
- **Producer** picks the partition (hash of the key, or round robin without a key); the same key always lands on the same partition, so order per key holds. **Consumer group**: consumers sharing the work; each partition goes to one consumer in the group. Groups are independent.
- **Log, not a queue**: reading does not delete. Retention (time or size) deletes old segments, nothing else does. Offsets keep their numbers. A new group can start at the beginning, an old group can rewind. A queue deletes on ack.
- **What is stored where**: record data in the partition's log files on the brokers; committed consumer offsets in the internal topic `__consumer_offsets`.
- Failure modes: commit before processing loses records on a crash, commit after processing duplicates them; a group asking for an offset that retention already deleted gets an out-of-range error and falls back to its reset policy; no global order across partitions.
- Not executed: no broker was available, so no real Kafka broker or client ran. The code below is a **pure-Python emulation** of the log idea (crc32 for the partitioner; real Kafka's default uses murmur2). Details follow the Kafka docs; check current docs.

**Example:** Three partitions, six records keyed u1, u2, u1, u3, u1, u2. In the emulation u1 and u3 land on partition 2 (offsets 0..3 in order) and u2 on partition 0. Group "fraud" reads and commits next offsets 2 and 4. A second group "audit" starts at 0 and sees all six. Retention then drops two records on partition 2: offsets 2..4 remain, and a group asking offset 0 gets an out-of-range error.

**Code:**
```python
# Q4: PURE-PYTHON EMULATION of Kafka log semantics. No Kafka broker or Kafka client was run.
import zlib

class OffsetOutOfRange(Exception): pass

class Partition:
    def __init__(self): self.records, self.start = [], 0          # start = log start offset (moves with retention)
    def append(self, rec): self.records.append(rec); return self.start + len(self.records) - 1
    @property
    def end(self): return self.start + len(self.records)          # next offset to be written (log end offset)
    def read(self, offset, max_n=100):
        if offset < self.start or offset > self.end: raise OffsetOutOfRange(f"offset {offset}, valid {self.start}..{self.end}")
        return [(offset + i, r) for i, r in enumerate(self.records[offset - self.start: offset - self.start + max_n])]
    def truncate_before(self, new_start):                          # retention deletes OLD records, offsets keep their numbers
        drop = new_start - self.start; self.records = self.records[drop:]; self.start = new_start

class Topic:
    def __init__(self, name, n): self.name, self.parts = name, [Partition() for _ in range(n)]
    def produce(self, key, value):                                 # same key -> same partition (crc32 here; real Kafka uses murmur2)
        p = zlib.crc32(key.encode()) % len(self.parts)
        return p, self.parts[p].append((key, value))

class Broker:                                                      # holds topics and the committed offsets (__consumer_offsets analogue)
    def __init__(self): self.committed = {}                        # (group, topic, partition) -> next offset to read
class Consumer:
    def __init__(self, broker, group, topic): self.b, self.g, self.t = broker, group, topic
    def poll(self, p):
        off = self.b.committed.get((self.g, self.t.name, p), 0)
        return self.t.parts[p].read(off)
    def commit(self, p, next_offset): self.b.committed[(self.g, self.t.name, p)] = next_offset

b, topic = Broker(), Topic("payments", 3)
for i, (k, v) in enumerate([("u1", "a"), ("u2", "b"), ("u1", "c"), ("u3", "d"), ("u1", "e"), ("u2", "f")]):
    print("produce", k, v, "->", topic.produce(k, v))
print("log end offsets:", [p.end for p in topic.parts])

c = Consumer(b, "fraud", topic)
for p in range(3):
    batch = c.poll(p); print(f"group fraud reads partition {p} from committed offset:", batch)
    if batch: c.commit(p, batch[-1][0] + 1)
print("committed:", {k[2]: v for k, v in b.committed.items() if k[0] == "fraud"})
print("poll again after commit (nothing new):", [c.poll(p) for p in range(3)])

print("\nnew group 'audit' is independent, starts at 0:", sum(len(Consumer(b, 'audit', topic).poll(p)) for p in range(3)), "records")
p_u1 = zlib.crc32(b"u1") % 3
topic.produce("u1", "g"); print("after one more u1 record, fraud sees on partition", p_u1, ":", c.poll(p_u1))

print("\nretention: delete the oldest 2 records of partition", p_u1)
topic.parts[p_u1].truncate_before(2)
print("partition now holds offsets", topic.parts[p_u1].start, "..", topic.parts[p_u1].end - 1, "(offsets not renumbered)")
try: Consumer(b, "late-group", topic).poll(p_u1)
except OffsetOutOfRange as e: print("new group asking offset 0 ->", type(e).__name__, "-", e)
```

**Output (my run):** EMULATION ONLY, no Kafka broker or client was involved:
```text
produce u1 a -> (2, 0)
produce u2 b -> (0, 0)
produce u1 c -> (2, 1)
produce u3 d -> (2, 2)
produce u1 e -> (2, 3)
produce u2 f -> (0, 1)
log end offsets: [2, 0, 4]
group fraud reads partition 0 from committed offset: [(0, ('u2', 'b')), (1, ('u2', 'f'))]
group fraud reads partition 1 from committed offset: []
group fraud reads partition 2 from committed offset: [(0, ('u1', 'a')), (1, ('u1', 'c')), (2, ('u3', 'd')), (3, ('u1', 'e'))]
committed: {0: 2, 2: 4}
poll again after commit (nothing new): [[], [], []]

new group 'audit' is independent, starts at 0: 6 records
after one more u1 record, fraud sees on partition 2 : [(4, ('u1', 'g'))]

retention: delete the oldest 2 records of partition 2
partition now holds offsets 2 .. 4 (offsets not renumbered)
new group asking offset 0 -> OffsetOutOfRange - offset 0, valid 2..5
```

**Follow-ups:**
- *Why partitions?* Parallelism and ordering per key; the partition count caps parallel consumers in one group (Q10 in this part covers groups).
- *What if I need global order?* One partition (no parallelism) or order downstream by event time or a sequence number.
- *Does retention depend on consumers?* No. Slow consumers do not stop deletion; they just lose data they have not read.

**Common mistakes:**
- Calling Kafka a queue.
- Saying offsets are global across a topic.
- Forgetting that ordering holds per partition only.

---

### Q5 ⭐⭐⭐ 🟢 Spark in plain words for an ML engineer: driver and executors, partitions, tasks, stages, lazy evaluation, transformations versus actions, narrow versus wide dependencies, and what a shuffle is. Explain why nothing runs until an action. Run a local PySpark session, build a small DataFrame pipeline, show that nothing executes until an action, and read the explain() plan to find the Exchange (shuffle) node.
**Asked at:** Spark interview question banks (dev.to datadriven 'Top 12 Spark interview problems for data engineers', devgenius 'Spark Interview Question' posts, datadriven.io Spark optimization and PySpark pages, a techinterview.org 'Why your Spark job is slow' post, a Scribd PySpark crash guide; search snippets only, not opened; the search found no India-specific Spark source); editorial prep material, not verified candidate reports; data engineer and ML engineer roles
**Say this first (1 line):** Spark builds a plan from transformations and runs nothing until an action; wide transformations like groupBy cause a shuffle, shown as an Exchange node in the plan.

**Then explain:**
- **Driver** runs your program, builds the plan and schedules; **executors** run tasks on data **partitions**. A **task** is one partition's work; tasks between shuffles are grouped into a **stage**.
- **Lazy evaluation**: transformations (select, filter, withColumn, groupBy) only extend the plan. Actions (count, collect, write, show) trigger a **job**. This lets the optimiser reorder and prune the work. It also means errors and slowness show up late, at the action.
- **Narrow** dependency: an output partition needs one input partition (filter, map). **Wide**: it needs data from many (groupBy, join, orderBy, distinct). Wide means a **shuffle**: write to disk, move over the network, regroup. Shuffles are the usual cost to look for.
- Failure modes: calling `collect()` on big data blows up the driver; too few or too many shuffle partitions; recomputing the same lineage in several actions unless you cache; Python UDFs are slower than built-ins (order: built-in, Arrow or pandas UDF, plain Python UDF, check docs).
- In ML work: Spark is for building features and training sets at scale, not for per-request serving.
- Scope: Spark 4.2.0 local[2], UI off, one machine. Cluster behaviour is not executed.

**Example:** `range(1000)`, add `k = id % 5`, keep even ids with a Python filter, group by k and count and sum, order by k. Hand check: k=0 holds ids 0, 10, ..., 990, which is 100 rows with sum 49500. The plan has two Exchange nodes: a hash partitioning for groupBy and a range partitioning for orderBy. The filter counter reads 0 after building the pipeline and 1000 after `collect()`.

**Code:**
```python
# Q5: lazy evaluation and the shuffle (Exchange) node, PySpark local[2]. Own warehouse and local dir.
import sys, io, contextlib
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import BooleanType
base = sys.argv[1]
spark = (SparkSession.builder.master("local[2]").appName("q05")
         .config("spark.ui.enabled", "false").config("spark.sql.shuffle.partitions", "4")
         .config("spark.sql.adaptive.enabled", "false")
         .config("spark.local.dir", base + "/local").config("spark.sql.warehouse.dir", base + "/wh").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
print("spark", spark.version)

calls = spark.sparkContext.accumulator(0)          # counts how many rows the Python filter really saw
def keep(x): calls.add(1); return x % 2 == 0
keep_udf = F.udf(keep, BooleanType())

df = spark.range(0, 1000, numPartitions=2)                       # transformation: nothing runs
df2 = df.withColumn("k", F.col("id") % 5)                        # transformation
df3 = df2.filter(keep_udf("id"))                                 # transformation
agg = df3.groupBy("k").agg(F.count("*").alias("n"), F.sum("id").alias("s")).orderBy("k")   # wide: needs a shuffle
print("partitions of input:", df.rdd.getNumPartitions())
print("after building the pipeline, rows the filter has seen:", calls.value, "  <- nothing ran")

buf = io.StringIO()
with contextlib.redirect_stdout(buf): agg.explain()
plan = buf.getvalue()
print("\n--- explain() ---"); print(plan.strip())
print("--- lines with Exchange:", [l.strip() for l in plan.splitlines() if "Exchange" in l])

rows = agg.collect()                                              # ACTION: now it runs
print("\nafter collect(), rows the filter has seen:", calls.value)
print(rows)
spark.stop()
```

**Output (my run):** PySpark 4.2.0, openjdk 21, local[2], adaptive query execution turned off to keep the plan simple (with it on, the plan can differ); JVM log noise removed:
```text
spark 4.2.0
partitions of input: 2
after building the pipeline, rows the filter has seen: 0   <- nothing ran
--- explain() ---
== Physical Plan ==
*(4) Sort [k#1L ASC NULLS FIRST], true, 0
+- Exchange rangepartitioning(k#1L ASC NULLS FIRST, 4), ENSURE_REQUIREMENTS, [plan_id=51]
   +- *(3) HashAggregate(keys=[k#1L], functions=[count(1), sum(id#0L)])
      +- Exchange hashpartitioning(k#1L, 4), ENSURE_REQUIREMENTS, [plan_id=47]
         +- *(2) HashAggregate(keys=[k#1L], functions=[partial_count(1), partial_sum(id#0L)])
            +- *(2) Project [id#0L, (id#0L % 5) AS k#1L]
               +- *(2) Project [id#0L]
                  +- *(2) Filter pythonUDF0#9: boolean
                     +- BatchEvalPython [keep(id#0L)#2], [pythonUDF0#9]
                        +- *(1) Range (0, 1000, step=1, splits=2)
--- lines with Exchange: ['+- Exchange rangepartitioning(k#1L ASC NULLS FIRST, 4), ENSURE_REQUIREMENTS, [plan_id=51]', '+- Exchange hashpartitioning(k#1L, 4), ENSURE_REQUIREMENTS, [plan_id=47]']
after collect(), rows the filter has seen: 1000
[Row(k=0, n=100, s=49500), Row(k=1, n=100, s=50100), Row(k=2, n=100, s=49700), Row(k=3, n=100, s=50300), Row(k=4, n=100, s=49900)]
```

**Follow-ups:**
- *What does `spark.sql.shuffle.partitions` do?* Sets the number of partitions after a shuffle (I used 4 locally); too many gives tiny tasks, too few gives big skewed ones.
- *cache vs persist?* Keep a computed DataFrame for reuse; useful when several actions share an expensive lineage.
- *Why is a Python UDF slow?* Rows cross between the JVM and Python processes; prefer built-in functions.

**Common mistakes:**
- Thinking `df.filter(...)` already ran.
- Calling `collect()` on big data.
- Reading explain() bottom-up as top-down: the plan is read from the innermost (bottom) line first.

---

### Q6 ⭐⭐⭐ 🟡 Point-in-time correct joins. Explain label leakage from joining the latest feature value to old labels, the as-of rule (latest feature value with timestamp at or before the label time, optionally within a TTL), and what 'event time' versus 'created time' mean for this. Build a training set three ways on the same small data, a naive latest-value join, pandas merge_asof and a DuckDB ASOF join (and Polars join_asof), show that the naive join leaks future values, and compare with Feast get_historical_features on the same entity dataframe.
**Asked at:** Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs | Feature-store product docs and write-ups (Feast docs on point-in-time joins and materialize and materialize-incremental, old v0.14 and v0.16 branches; an oneuptime.com Feast late-rows post; AWS SageMaker Unified Studio feature-group docs on online and offline stores and TTL; Databricks materialized-features docs; geeksforgeeks online vs offline store page; search snippets only, not opened); vendor docs and blogs, not interview reports; MLOps and ML platform roles; Feast 0.67.0 was also run locally in this sandbox
**Say this first (1 line):** Join each label to the latest feature value whose timestamp is at or before the label time, optionally within a TTL, never the latest value overall.

**Then explain:**
- **Leakage**: a naive "latest value" join gives a January label a value computed in June. The model looks great offline and fails live because the future is not available at serving time.
- **As-of rule**: for label time `t` and entity `e`, take the row with the greatest `event_ts <= t`. With a TTL, ignore it if `t - event_ts > ttl`. No match means null (or a dropped row, see below).
- **Event time vs created time**: event time is when the fact became true; created (ingestion) time is when the pipeline wrote it. A row can have an old event time and a late created time. Training must reflect what was known at label time, so late rows are a subtle leak source. Feast has an optional created-timestamp column to break ties between same-event-time rows; check your version's docs.
- Tools: `pandas.merge_asof`, DuckDB `ASOF LEFT JOIN`, Polars `join_asof`, Feast `get_historical_features`. They all implement the same idea; data must be sorted by time for pandas and Polars.
- Failure modes: unsorted inputs, joining on the key without `by=`, using `>=` the wrong way round, timestamp timezone mismatch, and in Feast, rows with no valid value in the output.
- Observed in Feast 0.67.0: asked for 4 rows, got 3 back. The row for user 2 at Jan 1 (their first feature is Jan 2) was dropped, not filled with null. The as-of methods in pandas, DuckDB and Polars kept it as null. Check your version and left-merge the result onto your label table to spot dropped rows.

**Example:** User 1 features: Jan 1 = 3, Jan 3 = 5, Jan 6 = 9. Label at Jan 2 should see 3 (the Jan 3 and Jan 6 values are the future). Label at Jan 4 sees 5. The naive join gives 9 for both, so all 4 labels in my data are wrong or leaked. User 2 label at Jan 1 has no earlier feature: null.

**Code:** two files, the first in a venv with pandas, polars and duckdb, the second in the Feast venv.
```python
# Q6: four ways to build a training set from the same tiny data. Run in the misc venv (pandas, polars, duckdb).
import warnings; warnings.filterwarnings("ignore")
import duckdb, pandas as pd, polars as pl
feat = pd.DataFrame({
    "user_id": [1, 1, 1, 2, 2],
    "ts": pd.to_datetime(["2026-01-01", "2026-01-03", "2026-01-06", "2026-01-02", "2026-01-05"]),
    "txn_count_7d": [3, 5, 9, 1, 4]})
lab = pd.DataFrame({
    "user_id": [1, 1, 2, 2],
    "label_ts": pd.to_datetime(["2026-01-02", "2026-01-04", "2026-01-03", "2026-01-01"]),
    "label": [0, 1, 0, 1]}).sort_values("label_ts").reset_index(drop=True)

# 1. NAIVE: join the latest value per user, ignoring time. Leaks the future.
latest = feat.sort_values("ts").groupby("user_id", as_index=False).last()[["user_id", "txn_count_7d"]]
naive = lab.merge(latest, on="user_id", how="left")

# 2. pandas merge_asof: latest feature row with ts <= label_ts, per user.
pm = pd.merge_asof(lab, feat.sort_values("ts"), left_on="label_ts", right_on="ts", by="user_id", direction="backward")

# 3. DuckDB ASOF LEFT JOIN
con = duckdb.connect()
con.register("lab", lab); con.register("feat", feat)
dd = con.sql("""SELECT l.user_id, l.label_ts, l.label, f.txn_count_7d
                FROM lab l ASOF LEFT JOIN feat f ON l.user_id = f.user_id AND l.label_ts >= f.ts
                ORDER BY l.label_ts, l.user_id""").df()

# 4. Polars join_asof
pl_out = (pl.from_pandas(lab).sort("label_ts")
          .join_asof(pl.from_pandas(feat).sort("ts"), left_on="label_ts", right_on="ts", by="user_id")
          .to_pandas())

key = ["user_id", "label_ts"]
res = lab[key + ["label"]].sort_values(key).reset_index(drop=True)
for name, df, col in [("naive latest-value", naive, "txn_count_7d"), ("pandas merge_asof", pm, "txn_count_7d"),
                      ("duckdb ASOF", dd, "txn_count_7d"), ("polars join_asof", pl_out, "txn_count_7d")]:
    res[name] = df.sort_values(key).reset_index(drop=True)[col].astype("Float64").to_numpy()
pd.set_option("display.width", 200)
print(res.to_string(index=False))
asof = ["pandas merge_asof", "duckdb ASOF", "polars join_asof"]
print("\nthree as-of methods agree:", all(res[asof[0]].equals(res[c]) for c in asof[1:]))
leaks = res[res["naive latest-value"] != res["pandas merge_asof"]]
print("rows where naive differs from as-of (leaked or wrong):", len(leaks), "of", len(res))

# ----- next file -----
# Helper shared by the Feast demos: builds a throw-away local repo and runs `feast apply`.
import pathlib, shutil, subprocess, sys, textwrap
import pandas as pd

def make_repo(root, df, ttl_days=30, project="demo"):
    root = pathlib.Path(root); shutil.rmtree(root, ignore_errors=True)
    repo = root / "repo"; repo.mkdir(parents=True)
    df.to_parquet(repo / "user_stats.parquet")
    (repo / "feature_store.yaml").write_text(textwrap.dedent(f"""\
        project: {project}
        provider: local
        registry: {root}/registry.db
        online_store:
          type: sqlite
          path: {root}/online.db
        offline_store:
          type: file
        entity_key_serialization_version: 3
        """))
    ttl = f"timedelta(days={ttl_days})" if ttl_days else "None"
    (repo / "definitions.py").write_text(textwrap.dedent(f"""\
        from datetime import timedelta
        from feast import Entity, FeatureView, Field, FileSource
        from feast.types import Float32, Int64
        from feast.value_type import ValueType
        user = Entity(name="user", join_keys=["user_id"], value_type=ValueType.INT64)
        src = FileSource(path="{repo}/user_stats.parquet", timestamp_field="event_ts")
        user_stats = FeatureView(name="user_stats", entities=[user], ttl={ttl},
            schema=[Field(name="txn_count_7d", dtype=Int64), Field(name="avg_amount_7d", dtype=Float32)],
            source=src)
        """))
    feast = str(pathlib.Path(sys.executable).parent / "feast")
    r = subprocess.run([feast, "apply"], cwd=repo, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-500:]
    return repo

def write_rows(repo, df):
    df.to_parquet(pathlib.Path(repo) / "user_stats.parquet")

# ----- next file -----
# Q6: the same data through Feast get_historical_features. Run in the feast venv.
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, __import__("pathlib").Path(__file__).parent.as_posix())
import pandas as pd
from feast import FeatureStore
from feast_common import make_repo
feat = pd.DataFrame({
    "user_id": [1, 1, 1, 2, 2],
    "event_ts": pd.to_datetime(["2026-01-01", "2026-01-03", "2026-01-06", "2026-01-02", "2026-01-05"]),
    "txn_count_7d": [3, 5, 9, 1, 4], "avg_amount_7d": [1.0] * 5})
repo = make_repo(sys.argv[1], feat, ttl_days=30, project="q06")
fs = FeatureStore(repo_path=str(repo))
ent = pd.DataFrame({"user_id": [1, 1, 2, 2],
    "event_timestamp": pd.to_datetime(["2026-01-02", "2026-01-04", "2026-01-03", "2026-01-01"], utc=True)})
out = fs.get_historical_features(entity_df=ent, features=["user_stats:txn_count_7d"]).to_df()
print(out.sort_values(["event_timestamp", "user_id"]).to_string(index=False))
```

**Output (my run):** pandas 3.1.0, polars 2.1.0, duckdb 2.0.0; then Feast 0.67.0:
```text
 user_id   label_ts  label  naive latest-value  pandas merge_asof  duckdb ASOF  polars join_asof
       1 2026-01-02      0                 9.0                3.0          3.0               3.0
       1 2026-01-04      1                 9.0                5.0          5.0               5.0
       2 2026-01-01      1                 4.0                NaN          NaN               NaN
       2 2026-01-03      0                 4.0                1.0          1.0               1.0
three as-of methods agree: True
rows where naive differs from as-of (leaked or wrong): 4 of 4
--- Feast get_historical_features, same data ---
 user_id           event_timestamp  txn_count_7d
       1 2026-01-02 00:00:00+00:00             3
       2 2026-01-03 00:00:00+00:00             1
       1 2026-01-04 00:00:00+00:00             5
```

**Follow-ups:**
- *Is it a left join?* In SQL terms yes: every label stays, with a null if nothing earlier exists (Feast 0.67.0 dropped it in my run).
- *How do you test for leakage?* Assert `feature_ts <= label_ts` on every joined row, and compare the offline score with a time-split holdout.
- *Why not `>` instead of `>=`?* Depends on whether a value stamped exactly at label time was available then; pick a rule, document it, and use it in serving too.

**Common mistakes:**
- Joining on the key only.
- Not sorting before `merge_asof`.
- Leaving out the `by` key, so users' values mix.

---

### Q7 ⭐⭐⭐ 🟡 Training-serving skew when a feature store is involved: the usual causes (offline SQL and online code computing the same feature differently, different windows, different null handling, stale online values, features not available at serving time) and the structural fixes (one feature definition, logging served features and training on them, parity tests). Part 8 owns detecting skew in monitoring, so keep to prevention. Simulate an offline pandas rolling feature and an online incremental feature that disagree on window boundaries, and write the parity test that catches it.
**Asked at:** Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs | Feature-store product docs and write-ups (Feast docs on point-in-time joins and materialize and materialize-incremental, old v0.14 and v0.16 branches; an oneuptime.com Feast late-rows post; AWS SageMaker Unified Studio feature-group docs on online and offline stores and TTL; Databricks materialized-features docs; geeksforgeeks online vs offline store page; search snippets only, not opened); vendor docs and blogs, not interview reports; MLOps and ML platform roles; Feast 0.67.0 was also run locally in this sandbox
**Say this first (1 line):** Skew comes from two code paths computing the same feature differently, so prevent it with one definition, log what was served, and a parity test that fails when the paths disagree.

**Then explain:**
- Usual causes: offline SQL and online code with different window boundaries; different null or default handling; different time zones; stale online values; features that exist in the warehouse but not at request time; different library versions.
- Structural fixes: (1) **one feature definition** run on both paths (same code, or one engine); (2) **log the features actually served** and train on those logs; (3) **parity tests** that replay the same events through both paths and compare; (4) a freshness check on the online store.
- Part 8 owns detecting skew in monitoring; here we prevent it.
- The bug I simulate: offline pandas `rolling("7D")` uses the window (t-7d, t] (an event exactly 7 days old is out). An online deque that drops only events strictly older than 7 days keeps the boundary event, so it counts one more.
- Failure modes: events on exact boundaries are rare, so average-case tests pass and production quietly drifts; testing with random data that never hits the boundary. Build tests with whole-hour timestamps or explicit boundary cases.

**Example:** Events at hourly resolution; at an event whose time is exactly 7 days after an earlier one, offline says 21 and the buggy online code says 22. In my seeded data that happened on 3 of 60 rows. The parity test fails on the buggy code and passes once the online rule is `<= cutoff` (drop).

**Code:**
```python
# Q7: offline pandas rolling feature vs online incremental feature; the parity test that catches a window-boundary bug.
from collections import deque
import numpy as np, pandas as pd

def make_events(seed=3, n=60):
    rng = np.random.default_rng(seed)
    ts = pd.Timestamp("2026-01-01") + pd.to_timedelta(np.sort(rng.integers(0, 20 * 24, n)), unit="h")   # whole hours -> exact 7-day gaps happen
    return pd.DataFrame({"user_id": 1, "ts": ts})

def offline_count_7d(ev):
    """Training path: pandas time-based rolling, window (t-7d, t], current event included (closed='right')."""
    s = ev.set_index("ts").assign(one=1)["one"]
    return s.rolling("7D").sum().astype(int).to_numpy()

class OnlineCounter:
    """Serving path: incremental deque. BUGGY keeps an event exactly 7 days old (window [t-7d, t])."""
    def __init__(self, buggy): self.q, self.buggy = deque(), buggy
    def update(self, t):
        self.q.append(t); cut = t - pd.Timedelta(days=7)
        while self.q and (self.q[0] < cut if self.buggy else self.q[0] <= cut): self.q.popleft()
        return len(self.q)

def online_series(ev, buggy):
    c = OnlineCounter(buggy); return np.array([c.update(t) for t in ev.ts])

def parity_report(ev, buggy):
    off, on = offline_count_7d(ev), online_series(ev, buggy)
    bad = np.flatnonzero(off != on)
    return off, on, bad

def test_online_matches_offline():              # run with pytest or call directly
    ev = make_events(); off, on, bad = parity_report(ev, buggy=False)
    assert len(bad) == 0, f"{len(bad)} of {len(ev)} rows disagree, first at {ev.ts.iloc[bad[0]]}"

if __name__ == "__main__":
    ev = make_events()
    for buggy in (True, False):
        off, on, bad = parity_report(ev, buggy)
        print(f"online variant = {'inclusive boundary (buggy)' if buggy else 'exclusive boundary (fixed)'}: {len(bad)} of {len(ev)} rows disagree")
        for i in bad[:3]:
            print(f"   ts={ev.ts.iloc[i]}  offline={off[i]}  online={on[i]}")
    try: test_online_matches_offline(); print("parity test with fixed online code: PASS")
    except AssertionError as e: print("parity test FAIL:", e)
    OnlineBug = lambda: parity_report(ev, True)
    try:
        off, on, bad = OnlineBug(); assert len(bad) == 0, f"{len(bad)} rows disagree"
    except AssertionError as e: print("parity test with buggy online code: FAIL ->", e)
```

**Output (my run):** pandas 3.1.0, numpy 2.5.4; seeded; no Feast or Kafka involved:
```text
online variant = inclusive boundary (buggy): 3 of 60 rows disagree
   ts=2026-01-12 17:00:00  offline=21  online=22
   ts=2026-01-13 23:00:00  offline=17  online=18
   ts=2026-01-14 06:00:00  offline=18  online=19
online variant = exclusive boundary (fixed): 0 of 60 rows disagree
parity test with fixed online code: PASS
parity test with buggy online code: FAIL -> 3 rows disagree
```

**Follow-ups:**
- *Why not just monitor for drift?* Monitoring tells you after the fact; parity tests stop it before release.
- *What if the two paths cannot share code?* Run a shadow comparison on live traffic and a nightly recompute check.
- *Why train on logged features?* They are exactly what the model saw at serving; no recomputation difference possible.

**Common mistakes:**
- Testing only on random timestamps.
- Fixing the bug in one path only.
- Comparing floats with `==` after different aggregation orders; use a tolerance for floats, exact for counts.

---

### Q8 ⭐⭐⭐ 🟡 Materialisation and backfill: what feast materialize and materialize-incremental do, what a backfill is and how it differs from live ingestion, why jobs must be idempotent, and how overlapping windows protect against late rows. Using the local Feast repo, materialise a window, run it again and show the online value is unchanged, add a late row and show what a plain rerun does, and explain which command needs an external scheduler to track state (Part 5 owns orchestration).
**Asked at:** Feature-store product docs and write-ups (Feast docs on point-in-time joins and materialize and materialize-incremental, old v0.14 and v0.16 branches; an oneuptime.com Feast late-rows post; AWS SageMaker Unified Studio feature-group docs on online and offline stores and TTL; Databricks materialized-features docs; geeksforgeeks online vs offline store page; search snippets only, not opened); vendor docs and blogs, not interview reports; MLOps and ML platform roles; Feast 0.67.0 was also run locally in this sandbox | Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs
**Say this first (1 line):** `materialize` copies a time window from offline to online and can be re-run safely; `materialize-incremental` remembers the last end time in the registry, so a scheduler must call it, and late rows behind that mark are missed unless you re-run an overlapping window.

**Then explain:**
- `feast materialize START END`: reads rows in the window, keeps the newest per entity, writes online. Stateless: you choose the window.
- `feast materialize-incremental END`: starts from the end of the previous run per feature view (tracked in the registry) up to END. Convenient, but Feast does not schedule it. cron, Airflow or similar must call it (Part 5 owns orchestration).
- **Backfill**: re-computing or re-loading history for a past period (new feature, bug fix, late data). **Live ingestion**: the normal, recurring flow of new data. Backfills must not corrupt the live state.
- **Idempotent**: running the same window twice gives the same result. Materialise is idempotent for the same window (shown below).
- **Late rows**: a row with an event time inside a window that already ran. A plain incremental run starts after that window and never sees it. Defence: overlapping windows (re-read the last N hours each time) or a periodic explicit window.
- Edge case I observed (Feast 0.67.0, SQLite, one run): re-running an OLD window after newer data was online **overwrote** the newer online value with the older one (user 1 went from 8 to 3), and a later full-window run repaired it. So run backfills for the whole range up to now, or in order, and do not assume the online store keeps the newest by itself. Check your version and store.

**Example:** User 1 has 3 (Jan 1) and 8 (Jan 3), user 2 has 1 (Jan 2). Materialise Jan 1 to Jan 4: online {1: 8, 2: 1}. Run again: unchanged. A late row for user 3 (event Jan 2) arrives. Incremental to Jan 6 starts at Jan 4 and returns None for user 3. An explicit window Jan 1 to Jan 6 returns 7.

**Code:**
```python
# Helper shared by the Feast demos: builds a throw-away local repo and runs `feast apply`.
import pathlib, shutil, subprocess, sys, textwrap
import pandas as pd

def make_repo(root, df, ttl_days=30, project="demo"):
    root = pathlib.Path(root); shutil.rmtree(root, ignore_errors=True)
    repo = root / "repo"; repo.mkdir(parents=True)
    df.to_parquet(repo / "user_stats.parquet")
    (repo / "feature_store.yaml").write_text(textwrap.dedent(f"""\
        project: {project}
        provider: local
        registry: {root}/registry.db
        online_store:
          type: sqlite
          path: {root}/online.db
        offline_store:
          type: file
        entity_key_serialization_version: 3
        """))
    ttl = f"timedelta(days={ttl_days})" if ttl_days else "None"
    (repo / "definitions.py").write_text(textwrap.dedent(f"""\
        from datetime import timedelta
        from feast import Entity, FeatureView, Field, FileSource
        from feast.types import Float32, Int64
        from feast.value_type import ValueType
        user = Entity(name="user", join_keys=["user_id"], value_type=ValueType.INT64)
        src = FileSource(path="{repo}/user_stats.parquet", timestamp_field="event_ts")
        user_stats = FeatureView(name="user_stats", entities=[user], ttl={ttl},
            schema=[Field(name="txn_count_7d", dtype=Int64), Field(name="avg_amount_7d", dtype=Float32)],
            source=src)
        """))
    feast = str(pathlib.Path(sys.executable).parent / "feast")
    r = subprocess.run([feast, "apply"], cwd=repo, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-500:]
    return repo

def write_rows(repo, df):
    df.to_parquet(pathlib.Path(repo) / "user_stats.parquet")

# ----- next file -----
# Q8: materialize vs materialize-incremental, idempotency, late rows. Feast 0.67 local, SQLite online store.
import sys, warnings, logging, os, io, contextlib; warnings.filterwarnings("ignore")
sys.path.insert(0, __import__("pathlib").Path(__file__).parent.as_posix())
from datetime import datetime, timezone
import pandas as pd
from feast import FeatureStore
from feast_common import make_repo, write_rows
U = lambda *a: datetime(*a, tzinfo=timezone.utc)
base = pd.DataFrame({"user_id": [1, 1, 2], "event_ts": pd.to_datetime(["2026-01-01", "2026-01-03", "2026-01-02"]),
                     "txn_count_7d": [3, 8, 1], "avg_amount_7d": [1.0, 1.0, 1.0]})
repo = make_repo(sys.argv[1], base, ttl_days=30, project="q08")
fs = FeatureStore(repo_path=str(repo))
F = ["user_stats:txn_count_7d"]
def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): fn(*a, **k)
def online(*users):
    d = fs.get_online_features(features=F, entity_rows=[{"user_id": u} for u in users]).to_dict()
    return dict(zip(d["user_id"], d["txn_count_7d"]))
def intervals():
    return [(a.date().isoformat(), b.date().isoformat()) for a, b in fs.get_feature_view("user_stats").materialization_intervals]

print("1. materialize 2026-01-01 .. 2026-01-04   ->", end=" "); quiet(fs.materialize, U(2026,1,1), U(2026,1,4)); print(online(1, 2, 3))
print("2. same command again (idempotent)       ->", end=" "); quiet(fs.materialize, U(2026,1,1), U(2026,1,4)); print(online(1, 2, 3))
print("   registry intervals after plain materialize:", intervals())

print("3. replay an OLD window 01-01..01-02 after newer data is online ->", end=" ")
quiet(fs.materialize, U(2026,1,1), U(2026,1,2)); print(online(1, 2, 3))

# late row: user 3, event time Jan 2 (inside the window we already ran), arrives after the run
late = pd.concat([base, pd.DataFrame({"user_id": [3], "event_ts": pd.to_datetime(["2026-01-02"]), "txn_count_7d": [7], "avg_amount_7d": [1.0]})])
write_rows(repo, late)
print("4. late row for user 3 (event 01-02) lands")
quiet(fs.materialize_incremental, end_date=U(2026,1,6))
print("   materialize-incremental to 01-06      ->", online(3))
print("   registry intervals now:", intervals())
quiet(fs.materialize, U(2026,1,1), U(2026,1,6))
print("   explicit overlapping window 01-01..06 ->", online(1, 2, 3))
```

**Output (my run):** Feast 0.67.0 local, SQLite online store. The last line of step 3 shows the overwrite described above:
```text
1. materialize 2026-01-01 .. 2026-01-04   -> {1: 8, 2: 1, 3: None}
2. same command again (idempotent)       -> {1: 8, 2: 1, 3: None}
   registry intervals after plain materialize: [('2026-01-01', '2026-01-04'), ('2026-01-01', '2026-01-04')]
3. replay an OLD window 01-01..01-02 after newer data is online -> {1: 3, 2: 1, 3: None}
4. late row for user 3 (event 01-02) lands
   materialize-incremental to 01-06      -> {3: None}
   registry intervals now: [('2026-01-01', '2026-01-04'), ('2026-01-01', '2026-01-04'), ('2026-01-01', '2026-01-02'), ('2026-01-04', '2026-01-06')]
   explicit overlapping window 01-01..06 -> {1: 8, 2: 1, 3: 7}
```

**Follow-ups:**
- *How do you make a backfill safe?* Same window gives same result, write by key and timestamp, run it in a separate job, then verify counts and sample values.
- *How often should the overlap be?* As long as your late-data tail, measured from created vs event time gaps.
- *Streaming alternative?* Push events straight to online as they arrive; still keep the batch job as the correction path.

**Common mistakes:**
- Assuming incremental catches late rows.
- Forgetting that nothing runs the incremental command for you.
- Backfilling an old window without checking what it does to online values.

---

### Q9 ⭐⭐⭐ 🟡 TTL and feature freshness. What does a feature-view TTL mean offline (how far back an as-of lookup may reach) and online (when a value counts as stale), what happens when no value is fresh enough (null, default, error), and how do you set a freshness SLO per feature and measure it? Using the local Feast repo, request features for entities just inside and just outside the TTL and print exactly what this Feast version returns, including whether a row is dropped or filled with null.
**Asked at:** Feature-store product docs and write-ups (Feast docs on point-in-time joins and materialize and materialize-incremental, old v0.14 and v0.16 branches; an oneuptime.com Feast late-rows post; AWS SageMaker Unified Studio feature-group docs on online and offline stores and TTL; Databricks materialized-features docs; geeksforgeeks online vs offline store page; search snippets only, not opened); vendor docs and blogs, not interview reports; MLOps and ML platform roles; Feast 0.67.0 was also run locally in this sandbox | Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs
**Say this first (1 line):** TTL offline limits how far back an as-of lookup may reach; online it is meant as "how old a value may be", but check what your store really enforces, and set a freshness SLO per feature that you measure yourself.

**Then explain:**
- **Offline TTL**: a feature row older than `label_time - ttl` is not eligible. This guards against using an ancient value as if it were current.
- **Online staleness**: in principle a value older than the TTL is expired. Stores differ (Redis key expiry, DynamoDB TTL, store-side checks); check current docs for your version and store.
- **When nothing is fresh enough**: options are null, a default, an error, or fall back to a model that does not need the feature. Choose per feature and make the model trained on the same rule (missingness should appear in training too).
- **Freshness SLO**: write down for each feature "99% of served values are no older than X". Measure age = request time minus the value's event time, from logged serving values or by checking the source. Alert on breach.
- Observed in Feast 0.67.0 (local file offline, SQLite online), TTL 2 days:
  - Offline: a value exactly 2 days old was used (boundary inclusive); one 2 days and 1 minute old made the row **disappear** from the output (3 rows back for 4 requested). An entity that has no row at all came back with a null. So "outside TTL" is dropped, "unknown entity" is null here. Do not assume either; test your version.
  - Online: a 3-day-old value was **still returned** with a 2-day TTL, so I would not rely on this version and store to expire stale values at read time. I checked this on SQLite only.

**Example:** Label time Jan 10, TTL 2 days. User 1 value from Jan 9: used. User 2 from Jan 8 00:00 (exactly 2 days): used. User 3 from 1 minute earlier: row dropped. User 4 (never seen): null. For the SLO, a daily feature with SLO 26 hours passes at 1 and 24 hours of age and fails at 72.

**Code:**
```python
# Helper shared by the Feast demos: builds a throw-away local repo and runs `feast apply`.
import pathlib, shutil, subprocess, sys, textwrap
import pandas as pd

def make_repo(root, df, ttl_days=30, project="demo"):
    root = pathlib.Path(root); shutil.rmtree(root, ignore_errors=True)
    repo = root / "repo"; repo.mkdir(parents=True)
    df.to_parquet(repo / "user_stats.parquet")
    (repo / "feature_store.yaml").write_text(textwrap.dedent(f"""\
        project: {project}
        provider: local
        registry: {root}/registry.db
        online_store:
          type: sqlite
          path: {root}/online.db
        offline_store:
          type: file
        entity_key_serialization_version: 3
        """))
    ttl = f"timedelta(days={ttl_days})" if ttl_days else "None"
    (repo / "definitions.py").write_text(textwrap.dedent(f"""\
        from datetime import timedelta
        from feast import Entity, FeatureView, Field, FileSource
        from feast.types import Float32, Int64
        from feast.value_type import ValueType
        user = Entity(name="user", join_keys=["user_id"], value_type=ValueType.INT64)
        src = FileSource(path="{repo}/user_stats.parquet", timestamp_field="event_ts")
        user_stats = FeatureView(name="user_stats", entities=[user], ttl={ttl},
            schema=[Field(name="txn_count_7d", dtype=Int64), Field(name="avg_amount_7d", dtype=Float32)],
            source=src)
        """))
    feast = str(pathlib.Path(sys.executable).parent / "feast")
    r = subprocess.run([feast, "apply"], cwd=repo, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-500:]
    return repo

def write_rows(repo, df):
    df.to_parquet(pathlib.Path(repo) / "user_stats.parquet")

# ----- next file -----
# Q9: TTL offline and online in Feast 0.67 (local provider, file offline store, SQLite online store). ttl = 2 days.
import sys, warnings, io, contextlib; warnings.filterwarnings("ignore")
sys.path.insert(0, __import__("pathlib").Path(__file__).parent.as_posix())
from datetime import datetime, timedelta, timezone
import pandas as pd
from feast import FeatureStore
from feast_common import make_repo
pd.set_option("display.width", 200)
F = ["user_stats:txn_count_7d"]

# ---- offline: label time 2026-01-10 00:00; feature ages: 1 day, exactly 2 days, 2 days + 1 min, none at all
T = pd.Timestamp("2026-01-10", tz="UTC")
ages = {1: timedelta(days=1), 2: timedelta(days=2), 3: timedelta(days=2, minutes=1)}
feat = pd.DataFrame({"user_id": list(ages), "event_ts": [(T - a).tz_localize(None) for a in ages.values()],
                     "txn_count_7d": [10, 20, 30], "avg_amount_7d": [1.0] * 3})
repo = make_repo(sys.argv[1] + "/offline", feat, ttl_days=2, project="q09off")
fs = FeatureStore(repo_path=str(repo))
ent = pd.DataFrame({"user_id": [1, 2, 3, 4], "event_timestamp": [T] * 4})
out = fs.get_historical_features(entity_df=ent, features=F).to_df()
print("OFFLINE: asked for 4 users, got", len(out), "rows back")
print(out.sort_values("user_id").to_string(index=False))
print("users with no row in the output:", sorted(set(ent.user_id) - set(out.user_id)))

# ---- online: timestamps relative to the real clock so 'now' matters
now = datetime.now(timezone.utc).replace(tzinfo=None)
ages2 = {1: timedelta(hours=1), 2: timedelta(days=1), 3: timedelta(days=3)}
feat2 = pd.DataFrame({"user_id": list(ages2), "event_ts": [now - a for a in ages2.values()],
                      "txn_count_7d": [10, 20, 30], "avg_amount_7d": [1.0] * 3})
repo2 = make_repo(sys.argv[1] + "/online", feat2, ttl_days=2, project="q09on")
fs2 = FeatureStore(repo_path=str(repo2))
with contextlib.redirect_stdout(io.StringIO()):
    fs2.materialize(start_date=datetime.now(timezone.utc) - timedelta(days=10), end_date=datetime.now(timezone.utc) + timedelta(hours=1))
d = fs2.get_online_features(features=F, entity_rows=[{"user_id": u} for u in (1, 2, 3, 4)]).to_dict()
print("\nONLINE (ttl 2 days; value ages 1 hour, 1 day, 3 days, no row)")
print(pd.DataFrame(d).to_string(index=False))

# ---- freshness SLO check done by us (the online read did not enforce ttl): age of the newest source row per user
SLO = timedelta(hours=26)          # example SLO for a daily-refreshed feature: 24 h + 2 h slack
newest = feat2.groupby("user_id").event_ts.max()
age = (now - newest)
rep = pd.DataFrame({"user_id": newest.index, "age_hours": (age.dt.total_seconds() / 3600).round(1).values,
                    "within_slo": (age <= SLO).values})
print("\nFRESHNESS CHECK (SLO 26 h)"); print(rep.to_string(index=False))
```

**Output (my run):** Feast 0.67.0 local. The online ages are relative to the sandbox clock, so rerunning gives the same shape but different decimals:
```text
OFFLINE: asked for 4 users, got 3 rows back
 user_id           event_timestamp  txn_count_7d
       1 2026-01-10 00:00:00+00:00          10.0
       2 2026-01-10 00:00:00+00:00          20.0
       4 2026-01-10 00:00:00+00:00           NaN
users with no row in the output: [3]
ONLINE (ttl 2 days; value ages 1 hour, 1 day, 3 days, no row)
 user_id  txn_count_7d
       1          10.0
       2          20.0
       3          30.0
       4           NaN
FRESHNESS CHECK (SLO 26 h)
 user_id  age_hours  within_slo
       1        1.0        True
       2       24.0        True
       3       72.0       False
```

**Follow-ups:**
- *How would you enforce freshness online if the store does not?* Store the value's event time as a feature (or alongside), compare with request time in the serving code and apply the default or null rule.
- *What TTL would you pick?* A few times the refresh interval, so one missed job does not blank the feature, but short enough that stale means wrong.
- *Dropped rows vs nulls?* Prefer nulls (explicit missing); if your tool drops rows, left-merge back onto the label table.

**Common mistakes:**
- Assuming online TTL is enforced.
- Not training with the same missing-value rule used in serving.
- Setting TTL to years so it never bites.

---
