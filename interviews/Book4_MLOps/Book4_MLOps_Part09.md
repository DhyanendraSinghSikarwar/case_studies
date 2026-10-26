# Book 4 — Part 9: Feature stores and streaming: Kafka, Spark

**Topic:** Feature stores and streaming for ML: feature store concepts (entities, feature views, online versus offline store, registry, lineage, ownership and reuse), point-in-time correct joins, training-serving skew prevention, materialisation, backfill, TTL and freshness, batch versus stream versus on-demand feature computation, Feast with Tecton, Hopsworks, SageMaker, Vertex AI and Databricks feature stores at concept level, Kafka (topics, partitions, offsets, consumer groups, ordering, delivery semantics, idempotent producers and transactions, retention and compaction, lag, schema registry and Avro, dead-letter queues, backpressure), stream processing (tumbling, sliding and session windows, event time versus processing time, watermarks, late data, state, checkpoints, Flink, Spark Structured Streaming and Kafka Streams at concept level), Spark for ML feature pipelines (partitions, shuffles, skew, broadcast joins, caching, lazy evaluation, narrow versus wide dependencies, UDF versus built-in versus pandas UDF, small files, Parquet and Delta layout), lambda and Kappa architecture, change data capture, data contracts, real-time feature serving latency, testing feature pipelines, and end-to-end design questions (card and UPI fraud features, recommender features)
**Target:** 35  |  **Actual:** 35 (⭐⭐⭐ 14, ⭐⭐ 14, ⭐ 7)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: Part 1 owns Git, pre-commit and pytest for ML code; Part 2 owns Docker; Part 3 owns Kubernetes and Helm; Part 4 owns DVC, MLflow and registry basics; Part 5 owns pipelines, scheduling and orchestration (Airflow, Prefect, Kubeflow); Part 6 owns serving mechanics, latency and error metrics, shadow, canary and rollout; Part 7 owns CI workflows and promotion gates; Part 8 owns monitoring, drift detection and alerting (this part covers skew prevention and freshness design, not drift statistics); Parts 10 and 11 own AWS, Azure and GCP services in depth; Part 12 owns cost and system design in depth; Book 1 owns ML theory; Book 2 owns LLM serving and RAG; Book 3 owns SQL window functions and pandas; Book 6 owns product and business. This part owns feature stores, Kafka and stream processing semantics, and Spark as used for ML feature pipelines.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for www.techinterview.org) and no page was opened, so every external source is a search snippet only (see research_notes/Book4_Part09_sources.md). No page was found that reports exact feature-store, Kafka or Spark questions asked by a named company at an India or global ML role, so 'Asked at' tags name source types (question banks, vendor docs, design write-ups), not verified company reports. Execution limit: pip worked through the proxy in fresh venvs under /tmp/claude-0/b9p09, so Wave B can really run on Python 3.13.17 with Java 21 (openjdk 21.0.12.1) present: feast 0.67.0 (pandas 2.3.3, pyarrow 26.0.0; local Parquet file offline store plus SQLite online store; feast apply, get_historical_features, materialize and get_online_features all ran; in this version a historical row whose only feature value is older than the TTL was dropped from the result rather than returned as null, and Entity without value_type gives a deprecation warning), pyspark 4.2.0 (local[*]; DataFrame aggregation, explain(), Structured Streaming with a file source, event-time window, watermark and memory sink all ran) with delta-spark 4.4.1 (a local Delta write and read ran, jar resolution via Maven Central worked but repos.spark-packages.org returned proxy 403 for some optional artifacts), polars 2.1.0 (join_asof), duckdb 2.0.0 (ASOF join, needs pyarrow to read Polars frames), pandas 3.1.0 (merge_asof; use pandas below 3 in the Feast env), fastavro 1.13.1 (reader and writer schema resolution), kafka-python 3.0.11 and confluent-kafka 2.16.0 (import only). The Spark Kafka connector package (spark-sql-kafka-0-10_2.13:4.2.0) resolved from Maven but there is no Kafka broker, no Redpanda, no Flink, and the docker CLI has no daemon, so all Kafka behaviour (consumer groups, offsets, delivery semantics, idempotent producers, transactions, compaction, rebalancing, Schema Registry server, Debezium) must be emulated in pure Python and labelled 'not executed' against a real broker; Flink, Kafka Streams, Tecton, Hopsworks, SageMaker Feature Store, Vertex AI Feature Store and Databricks Feature Store were not run. Timings are sandbox-only and prove nothing about clusters or managed services.

---

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

### Q10 ⭐⭐⭐ 🟡 Kafka consumer groups: how partitions are assigned to consumers in a group, why parallelism is capped by the partition count, what triggers a rebalance, eager versus cooperative rebalancing, what consumer lag is and how to read it. Simulate a range-style and a round-robin assignment for 6 partitions across 1, 3 and 8 consumers, simulate a consumer leaving, and compute lag per partition from end offsets and committed offsets in pure Python. No broker was run.
**Asked at:** Kafka interview question banks (golinuxcloud, dev.to hiteshchawla 'Kafka interview questions for data engineer', datavidhya, DataCamp, Simplilearn, wecreateproblems, adaface, hyring, a techinterview.org post 'Kafka interview questions that separate users from operators', a hackmd Kafka MCQ set; search snippets only, not opened); editorial question lists, not verified candidate reports; data engineer, ML platform and backend roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** In a group, each partition goes to exactly one consumer, so the partition count is the ceiling on parallelism, and lag (log end offset minus committed offset) tells me if the group keeps up.

**Then explain:**
- Assignment: the group coordinator (a broker) picks a group leader consumer. The leader runs the assignor and the result is sent back to every member. Range gives each consumer a contiguous slice per topic. Round-robin deals partitions out one by one. Sticky assignors try to keep what a consumer already owns.
- Cap: 6 partitions and 8 consumers means 2 consumers sit idle. More consumers than partitions only buys you failover spares. To scale past the cap you add partitions (which has an ordering cost, see Q11).
- Rebalance triggers: a consumer joins, leaves or crashes (session timeout or missed heartbeats), a consumer is too slow between polls (max poll interval), or partitions or subscriptions change.
- Eager rebalance: every member gives up all its partitions, then the group is reassigned. A stop-the-world pause for the whole group. Cooperative (incremental) rebalance: only partitions that must move are revoked, the rest keep processing. Newer Kafka versions also have a broker-driven protocol; check current docs for what your version and client default to.
- Lag per partition = log end offset - committed offset. Read it per partition, not only the total. Small and flat is fine. Growing for a long time means you are too slow. One partition far ahead of the others means a hot key or a stuck consumer.
- Failure mode: slow processing inside poll() triggers a rebalance, which makes things slower, which triggers another. A rebalance storm. Also a stuck partition shows up as lag on one partition while the total looks "ok".

**Example:** 6 partitions, 3 consumers. Range: c0 gets 0,1; c1 gets 2,3; c2 gets 4,5. Round-robin: c0 gets 0,3; c1 gets 1,4; c2 gets 2,5. c1 leaves. Eager: all 6 are revoked, then c0 gets 0,1,2 and c2 gets 3,4,5. Cooperative: c0 and c2 keep what they have and only partitions 2 and 3 move. Lag: partition 2 has end offset 300 and committed 150, so lag is 150 and it is the one to look at.

**Code:**
```python
# EMULATION in pure Python. No Kafka broker or client was run.
def range_assign(parts, consumers):
    consumers = sorted(consumers); n, m = len(parts), len(consumers)
    out, i = {c: [] for c in consumers}, 0
    for k, c in enumerate(consumers):
        take = n // m + (1 if k < n % m else 0)
        out[c] = parts[i:i + take]; i += take
    return out

def rr_assign(parts, consumers):
    consumers = sorted(consumers)
    out = {c: [] for c in consumers}
    for i, p in enumerate(parts):
        out[consumers[i % len(consumers)]].append(p)
    return out

def sticky_cooperative(prev, parts, consumers):
    """Keep what each survivor owns; give orphan partitions to the least loaded."""
    out = {c: [p for p in prev.get(c, []) if p in parts] for c in consumers}
    owned = {p for ps in out.values() for p in ps}
    for p in parts:
        if p not in owned:
            out[min(out, key=lambda c: (len(out[c]), c))].append(p)
    return out

P = list(range(6))
for n in (1, 3, 8):
    cs = [f"c{i}" for i in range(n)]
    print(f"--- {n} consumer(s), 6 partitions")
    print(" range      ", range_assign(P, cs))
    print(" round-robin", rr_assign(P, cs))
    idle = [c for c, ps in range_assign(P, cs).items() if not ps]
    print(" idle consumers:", idle)

print("--- consumer c1 leaves a group of 3 (range before, then rebalance)")
before = range_assign(P, ["c0", "c1", "c2"])
eager = range_assign(P, ["c0", "c2"])
coop = sticky_cooperative(before, P, ["c0", "c2"])
print(" before      ", before)
print(" eager after ", eager, "-> partitions revoked from everyone first:", sorted(sum(before.values(), [])))
moved = sorted(p for c in coop for p in coop[c] if p not in before.get(c, []))
print(" coop after  ", coop, "-> only moved:", moved)

print("--- lag per partition = log end offset - committed offset")
end = {0: 120, 1: 118, 2: 300, 3: 95, 4: 100, 5: 101}
committed = {0: 120, 1: 100, 2: 150, 3: 95, 4: 99, 5: 101}
lag = {p: end[p] - committed[p] for p in P}
print(" lag", lag, "total", sum(lag.values()), "max partition", max(lag, key=lag.get))
```

**Output (my run):** Pure-Python emulation. No Kafka broker or client was run. Real assignors also handle several topics and sticky ownership details this sketch skips. `kafka-consumer-groups.sh --describe` (the real lag tool) was not executed.
```text
--- 1 consumer(s), 6 partitions
 range       {'c0': [0, 1, 2, 3, 4, 5]}
 round-robin {'c0': [0, 1, 2, 3, 4, 5]}
 idle consumers: []
--- 3 consumer(s), 6 partitions
 range       {'c0': [0, 1], 'c1': [2, 3], 'c2': [4, 5]}
 round-robin {'c0': [0, 3], 'c1': [1, 4], 'c2': [2, 5]}
 idle consumers: []
--- 8 consumer(s), 6 partitions
 range       {'c0': [0], 'c1': [1], 'c2': [2], 'c3': [3], 'c4': [4], 'c5': [5], 'c6': [], 'c7': []}
 round-robin {'c0': [0], 'c1': [1], 'c2': [2], 'c3': [3], 'c4': [4], 'c5': [5], 'c6': [], 'c7': []}
 idle consumers: ['c6', 'c7']
--- consumer c1 leaves a group of 3 (range before, then rebalance)
 before       {'c0': [0, 1], 'c1': [2, 3], 'c2': [4, 5]}
 eager after  {'c0': [0, 1, 2], 'c2': [3, 4, 5]} -> partitions revoked from everyone first: [0, 1, 2, 3, 4, 5]
 coop after   {'c0': [0, 1, 2], 'c2': [4, 5, 3]} -> only moved: [2, 3]
--- lag per partition = log end offset - committed offset
 lag {0: 0, 1: 18, 2: 150, 3: 0, 4: 1, 5: 0} total 169 max partition 2
```

**Follow-ups:**
- *What does a rebalance cost?* Processing pauses for the moved partitions (all of them if eager), in-memory state may be dropped, and uncommitted work is redone. Use static membership or cooperative assignment and avoid long work inside poll.
- *Is lag in messages or time?* The tool gives messages. Also track time lag (age of the oldest unprocessed message) because 1,000 messages means different things at different rates.
- *Two groups on one topic?* Each group has its own offsets and reads everything independently.

**Common mistakes:**
- Saying "add more consumers" when consumers already equal partitions.
- Thinking two consumers in one group can share a partition. They cannot.
- Watching only total lag and missing one stuck partition.
- Committing offsets for messages not yet processed, which hides lag and loses data on a crash.

### Q11 ⭐⭐⭐ 🟡 Ordering in Kafka. What exactly is guaranteed (order within one partition only), how a message key chooses a partition, why you key by entity (user, card, device) for per-entity features, what happens to ordering when partitions are added or when a producer retries without idempotence, and how a hot key creates a hot partition. Simulate hash-mod key routing for 1000 keys, show the share of keys that move when partitions go from 6 to 8, and show a skewed key distribution in pure Python.
**Asked at:** Kafka interview question banks (golinuxcloud, dev.to hiteshchawla 'Kafka interview questions for data engineer', datavidhya, DataCamp, Simplilearn, wecreateproblems, adaface, hyring, a techinterview.org post 'Kafka interview questions that separate users from operators', a hackmd Kafka MCQ set; search snippets only, not opened); editorial question lists, not verified candidate reports; data engineer, ML platform and backend roles at IT-services firms, product companies and GCCs | Kafka exactly-once and idempotency sources (a levelup.gitconnected idempotent-producer post, a LinkedIn post on duplicate payments using idempotent producer plus idempotency key plus transactions, a Scribd outbox-pattern note, Onehouse and Confluent comparison pages stating Flink uses checkpoints and two-phase commit and Kafka uses transactions with read_committed; search snippets only, not opened; the official Apache Kafka docs were not opened); community posts and vendor pages, not interview reports; data engineer and platform roles
**Say this first (1 line):** Kafka orders messages only inside one partition, so I key by the entity (card, user, device) to put all of its events in the same partition, in order.

**Then explain:**
- Guarantee: messages with the same partition are read in the order they were appended. There is no order across partitions and none across topics.
- Key to partition: the default partitioner hashes the key bytes and takes it modulo the partition count (real Kafka uses murmur2; I used crc32 in the emulation). Same key means same partition, as long as the partition count does not change. No key means the producer spreads records (sticky or round-robin), so no per-entity order.
- Why key by entity: a per-card rolling count must see one card's events in order. If they are spread over partitions, two consumers each see half and the feature is wrong.
- Adding partitions: `hash mod 8` is not `hash mod 6`. In my run about three quarters of keys moved. Old events for a key sit in the old partition and new ones in the new partition, so a consumer can see new before old. Plan partition counts up front, or create a new topic and migrate.
- Retries: without idempotence, a failed batch is retried after a later batch already landed, so the order flips (with several requests in flight). The idempotent producer (sequence numbers per producer and partition) keeps the order. See Q16.
- Hot key: one partition gets most of the traffic, and one consumer is the bottleneck while the others idle. Fixes: salt the key when order for that entity is not needed, split the entity, or pre-aggregate before the topic.

**Example:** Card A sends events 1, 2, 3 and card B sends 1, 2. Keyed by card, A's three events are in one partition in order and B's two in another. A consumer sees A1,A2,A3 and B1,B2, though the two cards may interleave in any way. In the hot-key run, 600 of 1,000 events had one merchant key, so one partition held 687 events against a mean of about 167 (about 4 times).

**Code:**
```python
# EMULATION in pure Python. No Kafka broker or client was run.
# Real Kafka's default partitioner uses murmur2 on the key bytes; this uses zlib.crc32 as a stand-in.
import zlib, random, collections
def part(key, n): return zlib.crc32(key.encode()) % n

keys = [f"user{i}" for i in range(1000)]
moved = sum(part(k, 6) != part(k, 8) for k in keys)
print(f"keys that change partition when 6 -> 8: {moved} of 1000 ({moved/10:.1f}%)")
print("same key, same partition (6):", {part('user7', 6) for _ in range(5)})

# ordering per partition only: two keys, events interleaved; consumer reads partitions independently
events = [("A", 1), ("B", 1), ("A", 2), ("B", 2), ("A", 3)]
log = collections.defaultdict(list)
for k, seq in events: log[part(k, 6)].append((k, seq))
print("partition logs:", dict(log))

# adding partitions mid-stream: key A's later events land elsewhere
pa6, pa8 = part("A", 6), part("A", 8)
print(f"key A: partition {pa6} with 6 parts, {pa8} with 8 parts ->", "ORDER AT RISK" if pa6 != pa8 else "same")
bad = [k for k in keys if part(k, 6) != part(k, 8)][:1]
print("example key that moves:", bad, part(bad[0], 6), "->", part(bad[0], 8))

# retry without idempotence: two batches in flight (max.in.flight > 1); batch 1's first try is lost
def send(batches, fail_first_try_of, with_sequence_check):
    broker, next_seq, retry = [], 0, []
    for seq, name in enumerate(batches):                 # both sent before any ack
        if name == fail_first_try_of: retry.append((seq, name)); continue
        if with_sequence_check and seq != next_seq:      # broker expects seq 0 first: rejects out-of-order
            retry.append((seq, name)); continue
        broker.append(name); next_seq += 1
    for seq, name in retry: broker.append(name)          # client retries what failed or was rejected
    return broker
print("no idempotence      :", send(["msg1", "msg2"], "msg1", False), "(sent order msg1, msg2)")
print("sequence check (idem):", send(["msg1", "msg2"], "msg1", True))

# skew: 1000 events, 60% from one hot key
random.seed(7)
ev = ["merchant_hot"] * 600 + [f"merchant{random.randrange(200)}" for _ in range(400)]
cnt = collections.Counter(part(k, 6) for k in ev)
print("events per partition (60% hot key):", dict(sorted(cnt.items())))
print("max/mean ratio:", round(max(cnt.values()) / (len(ev) / 6), 2))
uni = collections.Counter(part(f"user{i}", 6) for i in range(1000))
print("1000 distinct keys, one event each:", dict(sorted(uni.items())))
```

**Output (my run):** Pure-Python emulation. No Kafka broker or client was run. The partitioner is crc32, not Kafka's murmur2, so the exact moved share (about 75%) will differ with real hashing but the idea does not (for 6 to 8, roughly three quarters of keys are expected to move for any good hash). The retry simulation is a simplified model of in-flight batches.
```text
keys that change partition when 6 -> 8: 746 of 1000 (74.6%)
same key, same partition (6): {0}
partition logs: {5: [('A', 1), ('A', 2), ('A', 3)], 1: [('B', 1), ('B', 2)]}
key A: partition 5 with 6 parts, 3 with 8 parts -> ORDER AT RISK
example key that moves: ['user0'] 5 -> 3
no idempotence      : ['msg2', 'msg1'] (sent order msg1, msg2)
sequence check (idem): ['msg1', 'msg2']
events per partition (60% hot key): {0: 687, 1: 58, 2: 66, 3: 72, 4: 62, 5: 55}
max/mean ratio: 4.12
1000 distinct keys, one event each: {0: 184, 1: 166, 2: 148, 3: 174, 4: 166, 5: 162}
```

**Follow-ups:**
- *Can I get a global order?* Only with one partition (no parallelism), or by ordering downstream by event time with a buffer. Usually per-entity order is enough.
- *Does consumer-group rebalancing break order?* Not within a partition, but processing may restart from the last committed offset, so you see repeats (Q12).
- *How do I handle a hot merchant?* Salt by a few buckets, aggregate partially per bucket, then merge. This gives up strict order inside that entity.

**Common mistakes:**
- Saying Kafka guarantees topic-wide order.
- Using a low-cardinality or skewed key (country, status).
- Adding partitions "to scale" on a keyed topic without thinking about moved keys.
- Using a null key and then expecting per-entity order.

### Q12 ⭐⭐⭐ 🟡 Delivery semantics: at-most-once, at-least-once and exactly-once. Explain acks, retries, the order of 'process' and 'commit offset', why commit-after-process gives duplicates and commit-before-process gives loss, and why exactly-once is really at-least-once plus idempotent or transactional effects. Simulate a consumer that crashes between processing and commit under both orders and show duplicates or loss, then add an idempotent sink keyed by (partition, offset) and show the count becomes exact. No broker was run.
**Asked at:** Kafka interview question banks (golinuxcloud, dev.to hiteshchawla 'Kafka interview questions for data engineer', datavidhya, DataCamp, Simplilearn, wecreateproblems, adaface, hyring, a techinterview.org post 'Kafka interview questions that separate users from operators', a hackmd Kafka MCQ set; search snippets only, not opened); editorial question lists, not verified candidate reports; data engineer, ML platform and backend roles at IT-services firms, product companies and GCCs | Kafka exactly-once and idempotency sources (a levelup.gitconnected idempotent-producer post, a LinkedIn post on duplicate payments using idempotent producer plus idempotency key plus transactions, a Scribd outbox-pattern note, Onehouse and Confluent comparison pages stating Flink uses checkpoints and two-phase commit and Kafka uses transactions with read_committed; search snippets only, not opened; the official Apache Kafka docs were not opened); community posts and vendor pages, not interview reports; data engineer and platform roles
**Say this first (1 line):** At-most-once means commit first and risk losing a message, at-least-once means process first then commit and risk duplicates, and "exactly-once" in practice is at-least-once plus an idempotent or transactional effect.

**Then explain:**
- Producer side: `acks=0` fire and forget, `acks=1` leader only, `acks=all` waits for the in-sync replicas. With retries on, a lost ack causes a duplicate write unless the producer is idempotent (Q16).
- Consumer side, commit after process: if the consumer crashes after the effect and before the commit, it restarts from the old offset and does the work again. Duplicate. This is the normal, safe default.
- Commit before process: if it crashes after the commit and before the effect, that message is never processed. Loss. Use only if loss is fine (metrics sampling).
- Exactly-once: you cannot stop a crash between "effect" and "commit". So you make the effect safe to repeat. An upsert keyed by (partition, offset), or a unique id, makes a replay a no-op. Kafka transactions do this for Kafka-to-Kafka work. A database or an online store outside Kafka needs its own idempotency.
- Failure mode: the idempotent key must be stable across retries. A random uuid made at processing time is not a key.

**Example:** 10 messages, crash while handling offset 4. Commit-then-process: offset 4 is committed but never applied, the sink has 9 rows and m4 is missing. Process-then-commit: m4 is applied, crash, restart replays from offset 4 and applies it again, sink has 11 rows including one duplicate. Sink keyed by (partition, offset): the replay overwrites the same key, 10 rows and nothing missing.

**Code:**
```python
# EMULATION in pure Python. No Kafka broker or client was run.
LOG = [f"m{i}" for i in range(10)]           # one partition, offsets 0..9
CRASH_AT = 4                                  # crash while handling offset 4

def run(order, sink_idempotent=False):
    committed, sink_list, sink_map = 0, [], {}
    def effect(off):
        if sink_idempotent: sink_map[("p0", off)] = LOG[off]   # upsert by (partition, offset)
        else: sink_list.append(LOG[off])                        # blind append
    for attempt in (1, 2):                    # attempt 2 = restart after crash
        off = committed                       # resume from committed offset
        while off < len(LOG):
            if order == "commit_then_process":
                committed = off + 1
                if attempt == 1 and off == CRASH_AT: break       # crash after commit, before effect
                effect(off)
            else:
                effect(off)
                if attempt == 1 and off == CRASH_AT: break       # crash after effect, before commit
                committed = off + 1
            off += 1
        if off >= len(LOG): break
    n = len(sink_map) if sink_idempotent else len(sink_list)
    seen = sorted({v for _, v in sink_map.items()}) if sink_idempotent else sink_list
    return n, seen

for order in ("commit_then_process", "process_then_commit"):
    n, seen = run(order)
    dup = len(seen) - len(set(seen)); miss = sorted(set(LOG) - set(seen))
    print(f"{order:20s} sink rows={n} duplicates={dup} missing={miss}")
n, seen = run("process_then_commit", sink_idempotent=True)
print(f"process_then_commit + idempotent sink keyed (partition, offset): rows={n} missing={sorted(set(LOG)-set(seen))}")
```

**Output (my run):** Pure-Python emulation of one partition and one crash. No Kafka broker or client was run.
```text
commit_then_process  sink rows=9 duplicates=0 missing=['m4']
process_then_commit  sink rows=11 duplicates=1 missing=[]
process_then_commit + idempotent sink keyed (partition, offset): rows=10 missing=[]
```

**Follow-ups:**
- *Is Kafka exactly-once a lie?* No, it is real inside Kafka (idempotent producer plus transactions plus read_committed). It stops at the Kafka boundary.
- *Where do I store the processed offset?* Best in the same transaction as the sink write, so effect and position move together.
- *Why not commit after every message?* Slow. Batch commits are fine if the sink is idempotent.

**Common mistakes:**
- Enabling auto-commit and not knowing it can commit before processing finishes.
- Calling a pipeline exactly-once when the sink is a plain append.
- Using the processing timestamp as the idempotency key.

### Q13 ⭐⭐⭐ 🟡 Event time versus processing time, and windows. Define tumbling, sliding and session windows, say which one fits 'transactions per card in the last hour', and explain what a watermark is, what late data is and what happens to it. Run a local Spark Structured Streaming query (file source, event-time tumbling window, 1 minute watermark, update mode, memory sink) on a few out-of-order events, print the window counts, and also compute the same three window types in plain Python on one event list.
**Asked at:** Stream-processing concept sources (Databricks 2017 blog 'Event-time aggregation and watermarking in Apache Spark Structured Streaming', Databricks watermarking deep dive, a codecentric.de Spark and Flink event-time post, an oneuptime late-data post, datadriven.io streaming system design questions; search snippets only, not opened); vendor and practitioner blogs, not interview reports; data engineer and streaming roles | Engine comparison pages (estuary.dev Spark vs Flink, conduktor.io, Onehouse 'Spark Structured Streaming vs Flink vs Kafka Streams', Confluent compare page, a DZone streaming article; search snippets only, not opened; one old Cal Poly page claiming Spark Streaming lacks exactly-once was treated as outdated); vendor blogs, partly competing claims; streaming and data platform roles
**Say this first (1 line):** Event time is when it happened, processing time is when I saw it; windows group by event time and the watermark says how long I wait for late events before I close a window and throw away the state.

**Then explain:**
- Tumbling: fixed, no overlap, one window per event. Sliding (hopping): fixed size, moves by a smaller step, an event is in several windows. Session: a window per burst of activity, closed after a gap with no events.
- "Transactions per card in the last hour" is a sliding window (or a trailing window evaluated per event). A tumbling hour gives a value that jumps at the top of the hour, which is not "last hour". For a velocity feature at prediction time, that trailing view is what you want.
- Watermark = latest event time seen minus the allowed delay. Events with a timestamp behind the watermark are late. In Spark they are dropped for the aggregation (my run). Events behind the clock but ahead of the watermark still update their old window.
- The watermark moves only as new data arrives, and Spark applies it from the next micro-batch. So late data decisions lag by one batch.
- Update mode emits only the windows that changed in this batch. Append mode would hold a window until the watermark passes it. Complete mode re-emits everything.
- Failure modes: a watermark that is too tight drops real data. Too loose keeps state for a long time. A partition with no traffic holds the watermark back. Check current Spark docs for multi-source watermark behaviour.

**Example:** Events at 10:00:10, 10:00:40, 10:01:05 arrive first. Then 10:00:55 arrives late (inside the 1-minute watermark) and 10:05:20 arrives, which moves the clock. The 10:00 window goes from 2 to 3. Then 10:00:30 arrives, now behind the watermark, and is dropped. The pure-Python version counts all 7 events with no watermark, so 10:00 has 4 there. The difference is exactly the dropped event.

**Code:**
```python
import os, sys, time, json, shutil, tempfile
from datetime import datetime, timedelta, timezone
from pyspark.sql import SparkSession, functions as F

W = tempfile.mkdtemp(prefix="q13_", dir="/tmp/claude-0/b9_q10_18")
src = os.path.join(W, "src"); os.makedirs(src)
spark = (SparkSession.builder.master("local[2]").appName("q13")
         .config("spark.ui.enabled", "false").config("spark.ui.showConsoleProgress", "false").config("spark.sql.shuffle.partitions", "2")
         .config("spark.sql.session.timeZone", "UTC")
         .config("spark.local.dir", os.path.join(W, "local")).config("spark.sql.warehouse.dir", os.path.join(W, "wh"))
         .getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

def drop(name, rows):
    with open(os.path.join(src, name), "w") as f:
        for ts, card in rows: f.write(json.dumps({"ts": ts, "card": card}) + "\n")

schema = "ts timestamp, card string"
df = spark.readStream.schema(schema).json(src)
agg = (df.withWatermark("ts", "1 minute").groupBy(F.window("ts", "1 minute")).count())
q = (agg.writeStream.outputMode("update").format("memory").queryName("win")
     .trigger(processingTime="1 second").start())

seen = 0
def show(label, wait_batches):
    global seen
    t0 = time.time()
    while time.time() - t0 < 30:
        time.sleep(0.5)
        got = [p for p in q.recentProgress if p["numInputRows"] > 0]
        if len(got) >= wait_batches: break
    time.sleep(2)                               # let the next empty batch advance the watermark
    got = [p for p in q.recentProgress if p["numInputRows"] > 0]
    p = got[-1]
    rows = spark.sql("select window.start as start, count from win").collect()
    new = rows[seen:]; seen = len(rows)
    print(f"[{label}]")
    print(f"   input rows={p['numInputRows']} max_event_time={p['eventTime'].get('max')} watermark_used={p['eventTime'].get('watermark')}")
    print("   update rows emitted this batch (window start, count):", [(r["start"].strftime("%H:%M"), r["count"]) for r in new])

drop("b1.json", [("2026-03-01T10:00:10", "c1"), ("2026-03-01T10:00:40", "c1"), ("2026-03-01T10:01:05", "c1")])
show("batch 1: three in-order events", 1)
drop("b2.json", [("2026-03-01T10:00:55", "c1"), ("2026-03-01T10:05:20", "c1")])
show("batch 2: 10:00:55 (late but inside watermark) and 10:05:20 (moves the clock)", 2)
drop("b3.json", [("2026-03-01T10:00:30", "c1"), ("2026-03-01T10:04:50", "c1")])
show("batch 3: 10:00:30 (behind watermark, dropped) and 10:04:50 (ahead of it, kept)", 3)
q.stop(); spark.stop(); shutil.rmtree(W, ignore_errors=True)

# ---- second script: q13_python_windows.py (plain Python, same events) ----
from datetime import datetime, timedelta
from collections import Counter
T = lambda s: datetime.fromisoformat("2026-03-01T" + s)
ev = sorted(T(t) for t in ["10:00:10", "10:00:40", "10:01:05", "10:00:55", "10:05:20", "10:00:30", "10:04:50"])
print("events (event-time order):", [e.strftime("%H:%M:%S") for e in ev])

# tumbling 1 min: each event in exactly one window
tum = Counter(e.replace(second=0) for e in ev)
print("tumbling 1m   :", {k.strftime("%H:%M"): v for k, v in sorted(tum.items())})

# sliding 2 min, hop 1 min: each event in 2 windows
sl = Counter()
for e in ev:
    start = e.replace(second=0)
    for k in range(2): sl[start - timedelta(minutes=k)] += 1
print("sliding 2m/1m :", {k.strftime("%H:%M") + "-" + (k + timedelta(minutes=2)).strftime("%H:%M"): v for k, v in sorted(sl.items())})

# session, gap 2 min: a new session when the gap to the previous event is >= 2 min
sess, cur = [], [ev[0]]
for e in ev[1:]:
    if e - cur[-1] >= timedelta(minutes=2): sess.append(cur); cur = [e]
    else: cur.append(e)
sess.append(cur)
print("session gap 2m:", [(s[0].strftime("%H:%M:%S"), s[-1].strftime("%H:%M:%S"), len(s)) for s in sess])

# trailing 'last hour' count evaluated at each event time (what a velocity feature wants)
print("trailing 1h at each event:", [(e.strftime("%H:%M:%S"), sum(1 for x in ev if e - timedelta(hours=1) < x <= e)) for e in ev])
```

**Output (my run):** Real run on PySpark 4.2.0, local[2], Python 3.13, OpenJDK 21 (file source, memory sink, update mode, 1 minute watermark, a 1 second trigger; sandbox only, the Spark UI was not inspected). The memory table in update mode receives the changed rows per batch, so the print shows each batch's updates. Second part is plain Python. Timings in such a loop depend on the trigger, so the batch boundaries here were forced by dropping one file at a time.
```text
[batch 1: three in-order events]
   input rows=3 max_event_time=2026-03-01T10:01:05.000Z watermark_used=1970-01-01T00:00:00.000Z
   update rows emitted this batch (window start, count): [('10:00', 2), ('10:01', 1)]
[batch 2: 10:00:55 (late but inside watermark) and 10:05:20 (moves the clock)]
   input rows=2 max_event_time=2026-03-01T10:05:20.000Z watermark_used=2026-03-01T10:00:05.000Z
   update rows emitted this batch (window start, count): [('10:00', 3), ('10:05', 1)]
[batch 3: 10:00:30 (behind watermark, dropped) and 10:04:50 (ahead of it, kept)]
   input rows=2 max_event_time=2026-03-01T10:04:50.000Z watermark_used=2026-03-01T10:04:20.000Z
   update rows emitted this batch (window start, count): [('10:04', 1)]

events (event-time order): ['10:00:10', '10:00:30', '10:00:40', '10:00:55', '10:01:05', '10:04:50', '10:05:20']
tumbling 1m   : {'10:00': 4, '10:01': 1, '10:04': 1, '10:05': 1}
sliding 2m/1m : {'09:59-10:01': 4, '10:00-10:02': 5, '10:01-10:03': 1, '10:03-10:05': 1, '10:04-10:06': 2, '10:05-10:07': 1}
session gap 2m: [('10:00:10', '10:01:05', 5), ('10:04:50', '10:05:20', 2)]
trailing 1h at each event: [('10:00:10', 1), ('10:00:30', 2), ('10:00:40', 3), ('10:00:55', 4), ('10:01:05', 5), ('10:04:50', 6), ('10:05:20', 7)]
```

**Follow-ups:**
- *Why does the watermark not drop the 10:04:50 event in batch 3?* The watermark was 10:04:20 from the previous batch, and 10:04:50 is ahead of it.
- *Which mode for writing to an online store?* Update mode with an upsert sink, guarded by event time (Q32).
- *Can I still count late events?* Send them to a side output or correct offline in batch (Q31).

**Common mistakes:**
- Windowing on processing time and calling it event time.
- Forgetting `withWatermark` and letting state grow without bound.
- Expecting late rows beyond the watermark to be corrected silently.
- Using a tumbling window for a "last N minutes" feature.

### Q14 ⭐⭐⭐ 🟡 Spark shuffles and data skew in a feature job. Explain what makes a shuffle expensive, how one hot key makes one task run far longer than the rest, how to spot it (task time spread in the Spark UI, partition row counts) and the fixes: adaptive query execution, repartitioning, salting the hot key, broadcasting the small side, filtering early. Run a local PySpark job with a deliberately skewed key, print rows per partition before and after salting, and say which skew features are version dependent. The Spark UI was not inspected.
**Asked at:** Spark interview question banks (dev.to datadriven 'Top 12 Spark interview problems for data engineers', devgenius 'Spark Interview Question' posts, datadriven.io Spark optimization and PySpark pages, a techinterview.org 'Why your Spark job is slow' post, a Scribd PySpark crash guide; search snippets only, not opened; the search found no India-specific Spark source); editorial prep material, not verified candidate reports; data engineer and ML engineer roles
**Say this first (1 line):** A shuffle moves rows across the network by key, and with a hot key one partition gets most of the rows so one task runs long while the others finish and wait.

**Then explain:**
- Shuffle cost: rows are written to disk on the map side, sent across the network, read on the reduce side, and often sorted. It is the main cost in wide operations (groupBy, join, repartition).
- Skew: hash(key) mod partitions puts every row of the hot key in one partition. The stage ends only when its slowest task ends, so total time is set by the hot partition. Memory spill or an out-of-memory error can show up there too.
- Spotting it: in the Spark UI, the stage's task-time and shuffle-read-size spread (max far above median). In code, count rows per `spark_partition_id()`. I did the second, I did not open the UI.
- Fixes: adaptive query execution (AQE) splits skewed shuffle partitions in some joins; repartition on a better key or more partitions; salt the hot key and aggregate in two steps; broadcast the small side so the big side does not shuffle; filter early to cut rows before the shuffle.
- Version dependent: AQE is on by default in recent Spark versions but its skew-join handling covers sort-merge joins, not every aggregation, and its thresholds (`skewedPartitionFactor`, `skewedPartitionThresholdInBytes`) and some newer skew features have changed across releases. Check the docs for your version. I turned AQE off to show the raw effect.
- Failure mode of salting: it only helps if the operation can be split (sums, counts). For a median or a distinct count you need another approach. Joins need the small side exploded across the salts.

**Example:** 100,000 rows, 80% for one merchant. Hash partitioning into 4 gave 85,057 / 6,647 / 3,466 / 4,830 rows, so one task did about 85% of the work. After salting the key into 8 buckets the partitions held 34,967 / 14,996 / 24,618 / 25,419. The two-stage salted aggregate gave the same top-3 as the direct groupBy.

**Code:**
```python
import os, tempfile, shutil, time
from pyspark.sql import SparkSession, functions as F
W = tempfile.mkdtemp(prefix="q14_", dir="/tmp/claude-0/b9_q10_18")
spark = (SparkSession.builder.master("local[2]").appName("q14")
         .config("spark.ui.enabled", "false").config("spark.ui.showConsoleProgress", "false")
         .config("spark.sql.shuffle.partitions", "4").config("spark.sql.adaptive.enabled", "false")
         .config("spark.local.dir", os.path.join(W, "local")).config("spark.sql.warehouse.dir", os.path.join(W, "wh"))
         .getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
print("spark", spark.version, "| AQE disabled on purpose for the demo")

# 100,000 events: 80% belong to merchant 'm_hot', the rest spread over 99 merchants (seeded, deterministic)
n = 100_000
df = (spark.range(n).withColumn("r", F.rand(42))
      .withColumn("merchant", F.when(F.col("r") < 0.8, F.lit("m_hot")).otherwise(F.concat(F.lit("m"), (F.col("id") % 99).cast("string"))))
      .withColumn("amt", F.col("id") % 50).drop("r"))

def per_part(d, label):
    rows = d.withColumn("p", F.spark_partition_id()).groupBy("p").count().orderBy("p").collect()
    print(f"{label:34s}", {r["p"]: r["count"] for r in rows})

per_part(df.repartition(4, "merchant"), "repartition by merchant (hash)")
# salting: spread the hot key over 8 salt values, aggregate partially, then combine
SALTS = 8
salted = df.withColumn("salt", (F.rand(7) * SALTS).cast("int")).withColumn("skey", F.concat_ws("#", "merchant", "salt"))
per_part(salted.repartition(4, "skey"), "repartition by merchant#salt")

t = salted.groupBy("merchant", "salt").agg(F.count("*").alias("c"), F.sum("amt").alias("s"))
two_stage = t.groupBy("merchant").agg(F.sum("c").alias("count"), F.sum("s").alias("sum_amt")).orderBy(F.desc("count")).limit(3).collect()
direct = df.groupBy("merchant").agg(F.count("*").alias("count"), F.sum("amt").alias("sum_amt")).orderBy(F.desc("count")).limit(3).collect()
print("salted two-stage top3:", [tuple(r) for r in two_stage])
print("plain groupBy   top3:", [tuple(r) for r in direct])
print("same answer:", [tuple(r) for r in two_stage] == [tuple(r) for r in direct])

# broadcast the small side of a join instead of shuffling the big skewed side
dim = spark.createDataFrame([(f"m{i}", i % 5) for i in range(99)] + [("m_hot", 9)], "merchant string, category int")
j = df.join(F.broadcast(dim), "merchant")
print("broadcast join plan has BroadcastHashJoin:", "BroadcastHashJoin" in j._jdf.queryExecution().executedPlan().toString())
print("joined rows:", j.count())
print("defaults:", {k: spark.conf.get(k) for k in ("spark.sql.adaptive.skewJoin.enabled", "spark.sql.adaptive.skewJoin.skewedPartitionFactor")})
spark.stop(); shutil.rmtree(W, ignore_errors=True)
```

**Output (my run):** Real run, PySpark 4.2.0, local[2], 4 shuffle partitions, AQE off, data generated with a fixed seed. Row counts per partition are deterministic here, but not a timing claim. Task durations and the Spark UI were not inspected. The salted partitions are still uneven because 8 salts hash into 4 partitions.
```text
spark 4.2.0 | AQE disabled on purpose for the demo
repartition by merchant (hash)     {0: 85057, 1: 6647, 2: 3466, 3: 4830}
repartition by merchant#salt       {0: 34967, 1: 14996, 2: 24618, 3: 25419}
salted two-stage top3: [('m_hot', 80060, 1961332), ('m5', 240, 5909), ('m66', 227, 5598)]
plain groupBy   top3: [('m_hot', 80060, 1961332), ('m5', 240, 5909), ('m66', 227, 5598)]
same answer: True
broadcast join plan has BroadcastHashJoin: True
joined rows: 100000
defaults: {'spark.sql.adaptive.skewJoin.enabled': 'true', 'spark.sql.adaptive.skewJoin.skewedPartitionFactor': '5.0'}
```

**Follow-ups:**
- *Why not just add partitions?* The hot key still lands in one partition, so it does not help a single hot key.
- *When do I broadcast?* When one side is small enough to fit in executor memory (default threshold is a small configured size; check your version).
- *What does AQE do for skew?* At runtime it sees map output sizes and splits a big partition in a skewed join into smaller tasks.

**Common mistakes:**
- Calling a slow job "a cluster problem" before looking at partition sizes.
- Salting without the second aggregation, which leaves wrong per-key results.
- Assuming AQE always fixes skew.
- Using `collect()` on the result to inspect it.

### Q15 ⭐⭐ 🟢 Feature registry, lineage, ownership and reuse. What metadata should a feature carry (owner, description, entity, source, transformation version, freshness SLO, tags, PII flag), how does a registry help discoverability and prevent duplicate near-identical features, and how do you deprecate or version a feature without breaking models? Query the local Feast registry from Python to list feature views, tags and owners, then show what a version bump would require.
**Asked at:** Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs | Feature-store product docs and write-ups (Feast docs on point-in-time joins and materialize and materialize-incremental, old v0.14 and v0.16 branches; an oneuptime.com Feast late-rows post; AWS SageMaker Unified Studio feature-group docs on online and offline stores and TTL; Databricks materialized-features docs; geeksforgeeks online vs offline store page; search snippets only, not opened); vendor docs and blogs, not interview reports; MLOps and ML platform roles; Feast 0.67.0 was also run locally in this sandbox
**Say this first (1 line):** The registry is the catalogue of features: who owns each one, where it comes from, what it means and how fresh it should be, so people reuse instead of rebuilding, and changes go through a new version, not an edit in place.

**Then explain:**
- Metadata each feature should carry: name, description (with window and null rules), entity, data type, source, owner (a team mailbox, not a person), transformation version, freshness SLO, PII flag, tags (team, status), and which models use it.
- Discoverability: search by tag, owner or entity before building. Feast stores tags as free-form key/values, so the PII flag and SLO are only as good as your convention. Feast does not enforce them; add a CI check.
- Duplicates: two near-identical features (`txn_count_1h` with different windows or null rules) are a skew risk. A review step on registry changes catches them.
- Lineage: Feast records source and entity per view, not full column-level lineage. Bigger lineage needs a catalogue tool. I did not run any.
- Deprecate and version: never change the meaning of a feature in place, because a trained model expects the old meaning. Add a new view (`card_velocity_v2`), mark the old one `deprecated` with `replaced_by`, keep serving both until every model has moved, then delete. Feast 0.67's `FeatureView` signature has a `version` argument; I did not exercise it, so check current docs. I used a name suffix, which works in any version.
- Failure modes: a name collision when both versions are requested together (Feast raised `FeatureNameCollisionError` when I asked for the same short name from two views; `full_feature_names=True` fixes it). Also an `apply` that silently changes a live view.

**Example:** `card_velocity_v1` (window includes the current event) is used by a live model. A fix excludes the current event. Create `card_velocity_v2`, backfill it, train the new model on it, tag v1 `deprecated`, `replaced_by: card_velocity_v2`. Both are queryable meanwhile.

**Code:**
```python
# Feast 0.67.0 (own venv, own repo under /tmp/claude-0/b9_q10_18). Registry is a local file.
import sys, os, shutil, tempfile
from datetime import datetime, timedelta, timezone
import pandas as pd
W = tempfile.mkdtemp(prefix="q15_", dir="/tmp/claude-0/b9_q10_18"); os.makedirs(W + "/data")
shutil.copy("/tmp/claude-0/b9_q10_18/feast_repo/feature_store.yaml", W); shutil.copy("/tmp/claude-0/b9_q10_18/feast_repo/defs.py", W)
os.chdir(W); sys.path.insert(0, W)
t0 = datetime(2026, 3, 1, tzinfo=timezone.utc)
pd.DataFrame({"card_id": [1, 2], "event_ts": [t0, t0], "txn_count_1h": [3, 1], "avg_amt_24h": [20.0, 5.0]}).to_parquet("data/card_stats.parquet")
import defs, feast
from feast import FeatureStore, FeatureView, Field
from feast.types import Float32, Int64
print("feast", feast.__version__)
fs = FeatureStore(".")
fs.apply([defs.card, defs.card_velocity_v1])

print("--- registry contents")
for e in fs.list_entities(): print("entity      ", e.name, "| owner:", e.owner)
for fv in fs.list_feature_views():
    print("feature view", fv.name, "| owner:", fv.owner, "| ttl:", fv.ttl, "| entities:", fv.entities)
    print("   tags:", dict(fv.tags))
    for f in fv.schema: print("   feature:", f.name, f.dtype, "|", f.description)
    print("   source:", fv.batch_source.path if hasattr(fv.batch_source, "path") else fv.batch_source)

print("--- find by tag (client-side filter)")
print([fv.name for fv in fs.list_feature_views() if fv.tags.get("team") == "fraud" and fv.tags.get("pii") == "false"])

print("--- version bump: change window semantics, new name card_velocity_v2, keep v1 for old models")
v2 = FeatureView(name="card_velocity_v2", entities=[defs.card], ttl=timedelta(days=1), source=defs.src,
    schema=[Field(name="txn_count_1h", dtype=Int64, description="Window [t-1h, t) excluding current event"),
            Field(name="avg_amt_24h", dtype=Float32)],
    owner="fraud-ml@example.com", description="Card velocity features, window fixed",
    tags={"team": "fraud", "pii": "false", "freshness_slo": "5m", "transform_version": "2", "status": "active"})
fs.apply([v2])
print([ (fv.name, fv.tags["transform_version"], fv.tags["status"]) for fv in fs.list_feature_views()])
v1 = fs.get_feature_view("card_velocity_v1"); v1.tags["status"] = "deprecated"; v1.tags["replaced_by"] = "card_velocity_v2"
fs.apply([v1])
print("after deprecating v1:", [(fv.name, fv.tags["status"]) for fv in fs.list_feature_views()])
print("(without full_feature_names=True Feast 0.67 raises FeatureNameCollisionError: same short name in two views)")
print("both still servable offline:", fs.get_historical_features(
    pd.DataFrame({"card_id": [1], "event_timestamp": [t0 + timedelta(hours=1)]}),
    features=["card_velocity_v1:txn_count_1h", "card_velocity_v2:txn_count_1h"], full_feature_names=True).to_df().to_dict("records"))
shutil.rmtree(W, ignore_errors=True)
```

**Output (my run):** Real run, Feast 0.67.0 in its own venv, local provider with a Parquet source and a file registry in a temp directory. Note that this version lists the entity column (`card_id`) in the view's schema output. The collision error mentioned above was seen in an earlier run of the same script before I added `full_feature_names=True`; its text is not in the pasted output.
```text
feast 0.67.0
--- registry contents
entity       card_id | owner: risk-platform@example.com
feature view card_velocity_v1 | owner: fraud-ml@example.com | ttl: 1 day, 0:00:00 | entities: ['card_id']
   tags: {'status': 'active', 'freshness_slo': '5m', 'team': 'fraud', 'pii': 'false', 'transform_version': '1'}
   feature: avg_amt_24h Float32 | Mean amount, last 24h
   feature: card_id Int64 | 
   feature: txn_count_1h Int64 | Transactions in last 1h, event time, window (t-1h, t]
   source: data/card_stats.parquet
--- find by tag (client-side filter)
['card_velocity_v1']
--- version bump: change window semantics, new name card_velocity_v2, keep v1 for old models
[('card_velocity_v1', '1', 'active'), ('card_velocity_v2', '2', 'active')]
after deprecating v1: [('card_velocity_v1', 'deprecated'), ('card_velocity_v2', 'active')]
(without full_feature_names=True Feast 0.67 raises FeatureNameCollisionError: same short name in two views)
both still servable offline: [{'card_id': 1, 'event_timestamp': Timestamp('2026-03-01 01:00:00+0000', tz='UTC'), 'card_velocity_v1__txn_count_1h': 3, 'card_velocity_v2__txn_count_1h': 3}]
```

**Follow-ups:**
- *Can I delete the old view straight away?* Not until you check which models and services still request it. Log which feature references each model uses.
- *Who owns a feature?* The team that maintains the pipeline and answers when it breaks.
- *Does the registry hold the data?* No. It holds definitions; the data is in the offline and online stores.

**Common mistakes:**
- Putting a person's name as owner.
- Editing a feature's logic and keeping the name.
- Tags with no convention (`PII`, `pii`, `is_pii`).
- Treating the registry as lineage when it only has source and entity.

### Q16 ⭐⭐ 🟡 Kafka idempotent producers and transactions. Explain how the broker uses producer id and sequence numbers to drop duplicates from retries, what transactional.id and read_committed add (atomic writes across partitions and consume-process-produce), and where exactly-once stops (a database or an online store outside Kafka). Simulate a lossy network with retries, count duplicates with and without a sequence-number check in pure Python, and say clearly that no broker or real client producer was run.
**Asked at:** Kafka exactly-once and idempotency sources (a levelup.gitconnected idempotent-producer post, a LinkedIn post on duplicate payments using idempotent producer plus idempotency key plus transactions, a Scribd outbox-pattern note, Onehouse and Confluent comparison pages stating Flink uses checkpoints and two-phase commit and Kafka uses transactions with read_committed; search snippets only, not opened; the official Apache Kafka docs were not opened); community posts and vendor pages, not interview reports; data engineer and platform roles | Kafka interview question banks (golinuxcloud, dev.to hiteshchawla 'Kafka interview questions for data engineer', datavidhya, DataCamp, Simplilearn, wecreateproblems, adaface, hyring, a techinterview.org post 'Kafka interview questions that separate users from operators', a hackmd Kafka MCQ set; search snippets only, not opened); editorial question lists, not verified candidate reports; data engineer, ML platform and backend roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** An idempotent producer sends a producer id and a per-partition sequence number so the broker drops retried duplicates, and transactions add all-or-nothing writes across partitions, but neither reaches a database outside Kafka.

**Then explain:**
- Problem: the producer sends, the broker writes, the ack is lost, the producer retries, and the log now has the record twice.
- Idempotence: the broker tracks the last sequence number per (producer id, partition). A sequence it has already seen is dropped (and acked). An out-of-order sequence is rejected so order holds. In recent Kafka clients this is on by default, and it relies on `acks=all`; check current docs for your client version.
- Limits: the guarantee is for one producer session (producer id). If the process restarts without a transactional id, it gets a new id, and a resend of old data is not caught.
- Transactions: a `transactional.id` survives restarts (the broker fences the old instance). The producer writes to several partitions, then commits or aborts. Consumers with `isolation.level=read_committed` see only committed records. With consume-process-produce, the input offsets are committed inside the same transaction, which gives exactly-once inside Kafka.
- Where it stops: writing to Postgres, Redis or an online store is outside the transaction. You need an idempotent upsert, an outbox, or a version guard there (Q32).
- Failure modes: a long transaction blocks read_committed consumers behind it. A hung producer holds a transaction open until the timeout.

**Example:** 1,000 messages, 20% of acks lost. Without a sequence check the log held 1,243 records (243 duplicates). With the check it held 1,000 and the broker dropped 243 retries. For transactions: t1 commits (A: x1, B: y1) and t2 aborts (A: x2, B: y2); read_committed shows only x1 and y1.

**Code:**
```python
# EMULATION in pure Python. No Kafka broker or real producer client was run.
import random
def run(n_msgs, loss_ack_p, use_seq, seed=11):
    rnd = random.Random(seed)
    log, last_seq = [], -1                    # broker side, one producer id, one partition
    dups_dropped = 0
    for seq in range(n_msgs):
        while True:                           # producer retries until it sees an ack
            # request reaches the broker (always, in this model)
            if use_seq and seq <= last_seq:
                dups_dropped += 1             # broker: already have this (pid, seq): drop, still ack
            else:
                log.append(seq); last_seq = seq
            if rnd.random() >= loss_ack_p: break   # ack arrived, producer moves on
            # else ack lost on the network: producer times out and retries the same message
    return log, dups_dropped

for use_seq in (False, True):
    log, dropped = run(1000, 0.2, use_seq)
    print(f"seq check={use_seq!s:5}: sent=1000 log_size={len(log)} duplicates={len(log)-len(set(log))} dropped_by_broker={dropped} in_order={log==sorted(log)}")

# transactions: all-or-nothing across two partitions, read_committed hides aborted data
topic = {"A": [], "B": []}                   # (value, txn_id, state)
def txn(tid, vals, commit):
    for p, v in vals: topic[p].append([v, tid, "open"])
    for p in topic:
        for rec in topic[p]:
            if rec[1] == tid: rec[2] = "committed" if commit else "aborted"
txn("t1", [("A", "x1"), ("B", "y1")], True)
txn("t2", [("A", "x2"), ("B", "y2")], False)
rc = {p: [r[0] for r in recs if r[2] == "committed"] for p, recs in topic.items()}
ru = {p: [r[0] for r in recs] for p, recs in topic.items()}
print("read_uncommitted:", ru)
print("read_committed  :", rc)
```

**Output (my run):** Pure-Python emulation with a seeded random loss. No Kafka broker or real producer client was run. The transaction part is a toy of the visibility rule only (no coordinator, no markers, no fencing).
```text
seq check=False: sent=1000 log_size=1243 duplicates=243 dropped_by_broker=0 in_order=True
seq check=True : sent=1000 log_size=1000 duplicates=0 dropped_by_broker=243 in_order=True
read_uncommitted: {'A': ['x1', 'x2'], 'B': ['y1', 'y2']}
read_committed  : {'A': ['x1'], 'B': ['y1']}
```

**Follow-ups:**
- *Does idempotence stop duplicates from my own code sending twice?* No. Two separate `send()` calls are two records. It only covers retries inside the client.
- *Cost of transactions?* Extra requests and commit markers, and read_committed latency. Use them where cross-partition atomicity matters.
- *Can I get exactly-once into a database?* Make the write idempotent or store the offset with the data in one DB transaction.

**Common mistakes:**
- Thinking idempotence gives exactly-once end to end.
- Forgetting `read_committed` on the consumer, which then sees aborted data.
- Reusing one transactional id across two live instances.

### Q17 ⭐⭐ 🟡 Kafka retention versus log compaction. Explain time and size retention, what compaction keeps (the latest value per key, tombstones delete), when you use each (event streams versus changelog or latest-state topics), and the limits of replaying from Kafka for a feature backfill. Simulate compaction on a keyed log in pure Python including a tombstone, and work out in plain arithmetic how much history a given retention window can rebuild.
**Asked at:** Kafka interview question banks (golinuxcloud, dev.to hiteshchawla 'Kafka interview questions for data engineer', datavidhya, DataCamp, Simplilearn, wecreateproblems, adaface, hyring, a techinterview.org post 'Kafka interview questions that separate users from operators', a hackmd Kafka MCQ set; search snippets only, not opened); editorial question lists, not verified candidate reports; data engineer, ML platform and backend roles at IT-services firms, product companies and GCCs | Lambda and Kappa sources (datadriven.io pipeline architecture page, techinterview.org 'Lambda and Kappa Architecture for Big Data', Materialize 'Does Kappa architecture improve on Lambda', a Netflix talk PDF on backfilling streaming pipelines in Kappa architecture hosted on microsites.databricks.com, risingwave.com; search snippets only, not opened); vendor blogs and a conference talk; data platform roles; the feature-store mapping is an expert extension
**Say this first (1 line):** Retention deletes old data by age or size, compaction keeps only the latest value per key, and neither makes Kafka a safe long-term store for a feature backfill.

**Then explain:**
- Time and size retention (`retention.ms`, `retention.bytes`): whole old segments are deleted once they pass the limit. Good for event streams where only recent data matters. Deletion is by segment, so data can live somewhat longer than the limit.
- Compaction (`cleanup.policy=compact`): the log keeps at least the last record for each key. Older values of a key are removed in the background. The topic then reads like "current state per key", which suits changelog and latest-state topics (user profile, CDC). Offsets are not renumbered, there are gaps.
- Tombstone: a record with a key and a null value means delete. It is kept for a configured time (`delete.retention.ms`), so consumers can see it, then it goes. A consumer that is offline longer than that can miss the delete.
- The active segment is not compacted, so recent duplicates remain. Compaction is not instant.
- Replay limits for a backfill: a compacted topic has lost history, so it cannot rebuild a rolling feature. A time-retention topic can only rebuild what is inside the window. A 30-day feature from a 7-day topic misses 23 days. Backfill from the lake (Parquet or Delta), then switch to the stream.
- Failure modes: a null key on a compacted topic is rejected. Tiered storage can lengthen retention, but check your distribution's docs, I did not run it.

**Example:** Keyed log: u1:a, u2:b, u1:c, u3:d, u2:null, u1:e, u4:f, u3:g. After compaction: u2 tombstone, u1:e, u4:f, u3:g. After the tombstone expires: u1:e, u3:g, u4:f, so the state table is u1=e, u3=g, u4=f. Arithmetic with assumed numbers: 7 days at 2 million events a day is 14 million events, at an assumed 500 bytes about 7 GB per replica, so 21 GB at replication factor 3 (made-up inputs, not a benchmark).

**Code:**
```python
# EMULATION in pure Python. No Kafka broker was run.
log = [(0,"u1","a"),(1,"u2","b"),(2,"u1","c"),(3,"u3","d"),(4,"u2",None),(5,"u1","e"),(6,"u4","f"),(7,"u3","g")]
# (offset, key, value); value None = tombstone
def compact(log, keep_tombstones=True):
    last = {}
    for off, k, v in log: last[k] = (off, k, v)           # latest offset per key wins
    out = sorted(last.values())
    return out if keep_tombstones else [r for r in out if r[2] is not None]
print("before :", log)
c = compact(log)
print("after compaction (tombstone for u2 still present until delete.retention):")
print("        ", c)
print("after tombstone expires:", compact(log, False))
print("latest-state table:", {k: v for _, k, v in compact(log, False)})
print("offsets are NOT renumbered:", [o for o,_,_ in c])

# time retention: events older than the window are deleted whole segments at a time
rate_per_day = 2_000_000; bytes_per_event = 500; retention_days = 7
total = rate_per_day * retention_days
print(f"\nretention {retention_days}d at {rate_per_day:,} events/day -> {total:,} events kept")
print(f"approx size one replica: {total*bytes_per_event/1e9:.1f} GB (x replication factor 3 = {3*total*bytes_per_event/1e9:.1f} GB)")
for want in (3, 7, 30, 90):
    print(f"backfill {want:>2} days of features from Kafka alone:", "possible" if want <= retention_days else "NOT possible, need the lake")
print("rolling 30-day feature needs history from day -30; with 7d retention the first 23 days are missing")
```

**Output (my run):** Pure-Python emulation. No Kafka broker was run. Rates and sizes are assumptions for arithmetic only.
```text
before : [(0, 'u1', 'a'), (1, 'u2', 'b'), (2, 'u1', 'c'), (3, 'u3', 'd'), (4, 'u2', None), (5, 'u1', 'e'), (6, 'u4', 'f'), (7, 'u3', 'g')]
after compaction (tombstone for u2 still present until delete.retention):
         [(4, 'u2', None), (5, 'u1', 'e'), (6, 'u4', 'f'), (7, 'u3', 'g')]
after tombstone expires: [(5, 'u1', 'e'), (6, 'u4', 'f'), (7, 'u3', 'g')]
latest-state table: {'u1': 'e', 'u4': 'f', 'u3': 'g'}
offsets are NOT renumbered: [4, 5, 6, 7]

retention 7d at 2,000,000 events/day -> 14,000,000 events kept
approx size one replica: 7.0 GB (x replication factor 3 = 21.0 GB)
backfill  3 days of features from Kafka alone: possible
backfill  7 days of features from Kafka alone: possible
backfill 30 days of features from Kafka alone: NOT possible, need the lake
backfill 90 days of features from Kafka alone: NOT possible, need the lake
rolling 30-day feature needs history from day -30; with 7d retention the first 23 days are missing
```

**Follow-ups:**
- *Can I use a compacted topic to bootstrap an online store?* Yes, that is a good fit: read from the start and you get the latest per key.
- *Both policies at once?* `cleanup.policy=compact,delete` exists: compact, and also delete past the retention.
- *How do I backfill 90 days?* From the lake or warehouse with the same transformation code, then hand over to the stream at a known offset or timestamp.

**Common mistakes:**
- Treating a time-retention topic as the system of record.
- Expecting compaction to delete old records right away.
- Sending a null key to a compacted topic.
- Forgetting that a compacted topic cannot rebuild windowed history.

### Q18 ⭐⭐ 🟡 Schema registry, Avro and compatibility. Why not send free-form JSON, what a schema registry stores, what backward, forward and full compatibility mean, and which changes are safe (add a field with a default, remove an optional field) versus breaking (rename, type change). Use fastavro to write a record with an old schema and read it with a newer reader schema that adds a defaulted field, then show the failure when the new field has no default. No registry server was run.
**Asked at:** Kafka interview question banks (golinuxcloud, dev.to hiteshchawla 'Kafka interview questions for data engineer', datavidhya, DataCamp, Simplilearn, wecreateproblems, adaface, hyring, a techinterview.org post 'Kafka interview questions that separate users from operators', a hackmd Kafka MCQ set; search snippets only, not opened); editorial question lists, not verified candidate reports; data engineer, ML platform and backend roles at IT-services firms, product companies and GCCs | CDC and data-contract sources (risingwave.com and oneuptime.com Debezium schema-evolution posts, a decodable.co CDC schema-evolution post, a Confluent Current 2024 session 'Data contracts in practice with Debezium and Apache Flink', a sessionize.com talk on data contracts for AI pipelines, a Skroutz AWS Big Data blog post; search snippets only, not opened; one talk statistic about AI project failure was unsourced and not used); vendor and conference material; data engineer and platform roles
**Say this first (1 line):** A schema registry stores versioned schemas and checks compatibility before a producer can publish a change, so a new field does not break consumers that are already running.

**Then explain:**
- Why not free-form JSON: no contract, so a renamed field or a type change fails in the consumer at 3 a.m. Also bigger messages. Avro adds a schema, a compact binary encoding and rules for evolution.
- What the registry stores: schemas by subject (often topic-value) with an id and a version. A message carries a small schema id, not the schema. The consumer fetches the schema by id and caches it. (From docs; no registry server was run.)
- Backward compatible: consumers on the new schema can read old data. Forward compatible: consumers on the old schema can read new data. Full: both. Check which one your registry subject is set to, and whether it checks only against the last version or all of them (transitive).
- Safe: add a field with a default, remove a field that has a default (optional). Breaking: rename a field (an add plus a remove), change a type (except allowed promotions such as int to long), or add a required field with no default.
- Failure mode: the reader needs the writer schema to decode. If you only have the new schema, old bytes decode wrongly or fail. Aliases can help with renames.
- For ML: events feed features. A silent type change corrupts a feature. Put compatibility checks in CI (Q29).

**Example:** Old schema: card, amount. Write {c1, 12.5}. A reader with a new schema adding `channel` with default "unknown" returns channel=unknown. The same reader without a default raises an error. Renaming card to card_id fails the same way (it looks like a new field without a default). Changing amount to string fails with a type mismatch. An old reader of new data simply ignores the extra field.

**Code:**
```python
# Real fastavro run. No Schema Registry server was run: compatibility is checked by the reader/writer resolution only.
import io, fastavro
from fastavro import schemaless_writer, schemaless_reader
old = {"type":"record","name":"Txn","fields":[{"name":"card","type":"string"},{"name":"amount","type":"double"}]}
new_ok = {"type":"record","name":"Txn","fields":[{"name":"card","type":"string"},{"name":"amount","type":"double"},
          {"name":"channel","type":"string","default":"unknown"}]}
new_bad = {"type":"record","name":"Txn","fields":[{"name":"card","type":"string"},{"name":"amount","type":"double"},
          {"name":"channel","type":"string"}]}
renamed = {"type":"record","name":"Txn","fields":[{"name":"card_id","type":"string"},{"name":"amount","type":"double"}]}
retyped = {"type":"record","name":"Txn","fields":[{"name":"card","type":"string"},{"name":"amount","type":"string"}]}
buf = io.BytesIO(); schemaless_writer(buf, old, {"card":"c1","amount":12.5}); data = buf.getvalue()
print("fastavro", fastavro.__version__, "| bytes written with OLD schema:", len(data))

def read(label, reader, writer=old, payload=data):
    try:
        print(f"{label:34s} ->", schemaless_reader(io.BytesIO(payload), writer, reader))
    except Exception as e:
        print(f"{label:34s} -> FAIL {type(e).__name__}: {e}")
read("new reader, field with default", new_ok)
read("new reader, field NO default", new_bad)
read("reader renamed card->card_id", renamed)
read("reader retyped amount->string", retyped)
# forward direction: new writer, old reader (old consumer ignores the extra field)
buf2 = io.BytesIO(); schemaless_writer(buf2, new_ok, {"card":"c2","amount":3.0,"channel":"upi"})
read("old reader of NEW data (forward)", old, writer=new_ok, payload=buf2.getvalue())
# reader that drops a field the writer had
only_card = {"type":"record","name":"Txn","fields":[{"name":"card","type":"string"}]}
read("reader removes amount field", only_card)
# promotion: int -> long is allowed by the Avro spec
w = {"type":"record","name":"N","fields":[{"name":"x","type":"int"}]}; r = {"type":"record","name":"N","fields":[{"name":"x","type":"long"}]}
b = io.BytesIO(); schemaless_writer(b, w, {"x": 7})
read("int -> long promotion", r, writer=w, payload=b.getvalue())
```

**Output (my run):** Real run, fastavro 1.13.1 in its own venv (schemaless write and resolution). No Schema Registry server was run, so the registry's own compatibility check API was not executed; the failures are fastavro's reader/writer resolution.
```text
fastavro 1.13.1 | bytes written with OLD schema: 11
new reader, field with default     -> {'card': 'c1', 'amount': 12.5, 'channel': 'unknown'}
new reader, field NO default       -> FAIL SchemaResolutionError: No default value for field channel in Txn
reader renamed card->card_id       -> FAIL SchemaResolutionError: No default value for field card_id in Txn
reader retyped amount->string      -> FAIL SchemaResolutionError: Schema mismatch: double is not string
old reader of NEW data (forward)   -> {'card': 'c2', 'amount': 3.0}
reader removes amount field        -> {'card': 'c1'}
int -> long promotion              -> {'x': 7}
```

**Follow-ups:**
- *Which compatibility mode do I pick?* Backward is common when consumers are upgraded first. Full is safest if you cannot control the order. Check how your registry treats the default.
- *Avro vs Protobuf vs JSON Schema?* All can work with a registry; the rules for evolution differ. Check docs.
- *How do I do a rename?* Add the new field with a default, dual-write, migrate readers, then remove the old one (expand, adapt, contract).

**Common mistakes:**
- Adding a required field with no default.
- Assuming a rename is safe.
- Reading with only the new schema and not the writer schema.
- Setting compatibility to NONE "to get unblocked".

### Q19 ⭐⭐ 🟡 Bad messages, dead-letter queues and backpressure in a streaming consumer. How do you handle a poison message (parse failure, schema mismatch, null key), when to retry with backoff versus send to a dead-letter topic, what to put in the DLQ record, and what to do when the consumer cannot keep up (lag grows, pull-based consumption, pause, scale out, drop or sample). Simulate a consumer with a bounded retry, a DLQ list and a slow processing rate in pure Python, and print lag over time.
**Asked at:** Kafka interview question banks (golinuxcloud, dev.to hiteshchawla 'Kafka interview questions for data engineer', datavidhya, DataCamp, Simplilearn, wecreateproblems, adaface, hyring, a techinterview.org post 'Kafka interview questions that separate users from operators', a hackmd Kafka MCQ set; search snippets only, not opened); editorial question lists, not verified candidate reports; data engineer, ML platform and backend roles at IT-services firms, product companies and GCCs | Stream-processing concept sources (Databricks 2017 blog 'Event-time aggregation and watermarking in Apache Spark Structured Streaming', Databricks watermarking deep dive, a codecentric.de Spark and Flink event-time post, an oneuptime late-data post, datadriven.io streaming system design questions; search snippets only, not opened); vendor and practitioner blogs, not interview reports; data engineer and streaming roles
**Say this first (1 line):** A poison message must never block the partition: retry only transient errors a few times with backoff, park everything else in a dead-letter topic with full context, commit the offset, and treat growing lag as a capacity problem you fix with pull control, scale-out or shedding.

**Then explain:**
- **Poison versus transient.** Parse failure, schema mismatch and null key will fail the same way forever, so do not retry them. Go straight to the DLQ. A sink timeout is transient, so retry a bounded number of times with backoff, then park it.
- **Why bounded.** An endless retry on one record stalls the whole partition (offsets are in order). Failure mode: lag grows, nobody is paged, and the consumer may also miss `max.poll.interval.ms` and trigger a rebalance.
- **DLQ record content.** Original topic, partition, offset, key and value as raw bytes (not re-serialised), headers, error class and message, attempt count, failure timestamp, consumer app and version, schema id if any. Without this you cannot replay or debug. A DLQ is a convention (a topic you write to), not a built-in Kafka feature. Kafka Connect has its own error-tolerance and DLQ settings for sink connectors (check current docs).
- **Backpressure in Kafka is pull-based.** The consumer asks for records, so a slow consumer does not get flooded. It just falls behind and lag grows (log end offset minus committed offset). Levers: `max.poll.records`, `pause()` and `resume()` partitions while a downstream queue drains, add consumers (useful only up to the partition count), speed up the work, or shed load (drop or sample) when freshness matters more than completeness, as for some real-time features.
- **Trade-offs.** Parking a record breaks strict per-key ordering for that key. Commit only after a record is done or parked, otherwise a crash loses it. Alert on DLQ rate and on lag trend, not just lag level.

**Example:** 80 messages arrive in an 8-tick burst, 10 per tick. One consumer pulls 4 per tick, so lag climbs by 6 every tick. At tick 6 we add a second consumer. It still falls behind (8 per tick against 10 produced) until the burst ends at tick 8, then drains by tick 13. 18 messages end in the DLQ: 9 null keys, 4 parse errors, 4 schema mismatches, 1 retries-exhausted. Three flaky messages succeeded on retry.

**Code:**
```python
# EMULATION of Kafka consumer semantics in pure Python. No broker, no Kafka client was run.
import json, random
random.seed(19)

def make_msg(i):
    r = random.random()
    if r < 0.06:  return i, b"{not json"                                   # parse failure
    if r < 0.12:  return i, json.dumps({"card": None, "amt": 5}).encode()   # null key
    if r < 0.18:  return i, json.dumps({"card": f"c{i%5}", "amt": "x"}).encode()  # schema mismatch
    return i, json.dumps({"card": f"c{i%5}", "amt": 10 + i % 7, "flaky": i % 17 == 0}).encode()

class Poison(Exception): pass          # never worth retrying
class Transient(Exception): pass       # worth retrying

def parse(raw):
    try: d = json.loads(raw)
    except ValueError as e: raise Poison(f"parse_error: {e}")
    if d.get("card") is None: raise Poison("null_key")
    if not isinstance(d.get("amt"), (int, float)): raise Poison("schema_mismatch: amt not number")
    return d

attempts = {}
def process(off, d):
    attempts[off] = attempts.get(off, 0) + 1
    if d.get("flaky") and (attempts[off] <= 2 or off == 34):   # fails twice then works; offset 34 never works
        raise Transient("sink timeout")

log, dlq, done = [], [], []
PRODUCE_PER_TICK, MAX_POLL, MAX_RETRIES, TICKS = 10, 4, 3, 14
consumers = 1
committed = 0
for tick in range(1, TICKS + 1):
    if tick <= 8:                                   # producer burst for 8 ticks
        for _ in range(PRODUCE_PER_TICK):
            log.append(make_msg(len(log)))
    if tick == 6:
        consumers = 2                               # scale out after lag alarm (same group, 2 partitions assumed)
    budget = MAX_POLL * consumers                   # pull-based: consumer only asks for what it can handle
    while budget and committed < len(log):
        off, raw = log[committed]
        try:
            d = parse(raw); 
            for _try in range(MAX_RETRIES):
                try: process(off, d); done.append(off); break
                except Transient: pass              # a real consumer sleeps with backoff here
            else:
                raise Poison("retries_exhausted")
        except Poison as e:
            dlq.append({"topic": "tx", "partition": 0, "offset": off, "error": str(e),
                        "attempts": attempts.get(off, 0), "payload": raw.decode(), "tick": tick})
        committed += 1; budget -= 1                 # commit AFTER the message is done or parked
    print(f"tick={tick:2d} consumers={consumers} produced={len(log):3d} committed={committed:3d} lag={len(log)-committed:3d} dlq={len(dlq)}")

print("processed ok:", len(done), "| in DLQ:", len(dlq), "| flaky ones that succeeded after retry:",
      sum(1 for o in done if attempts[o] > 1))
for r in dlq[:4]: print(r)
reasons = {}
for r in dlq: reasons[r["error"].split(":")[0]] = reasons.get(r["error"].split(":")[0], 0) + 1
print("DLQ by reason:", dict(sorted(reasons.items())))
```

**Output (my run):** (pure-Python EMULATION of consumer semantics; no Kafka broker or client was run; python3 -I)
```
tick= 1 consumers=1 produced= 10 committed=  4 lag=  6 dlq=0
tick= 2 consumers=1 produced= 20 committed=  8 lag= 12 dlq=1
tick= 3 consumers=1 produced= 30 committed= 12 lag= 18 dlq=1
tick= 4 consumers=1 produced= 40 committed= 16 lag= 24 dlq=2
tick= 5 consumers=1 produced= 50 committed= 20 lag= 30 dlq=3
tick= 6 consumers=2 produced= 60 committed= 28 lag= 32 dlq=4
tick= 7 consumers=2 produced= 70 committed= 36 lag= 34 dlq=5
tick= 8 consumers=2 produced= 80 committed= 44 lag= 36 dlq=8
tick= 9 consumers=2 produced= 80 committed= 52 lag= 28 dlq=9
tick=10 consumers=2 produced= 80 committed= 60 lag= 20 dlq=12
tick=11 consumers=2 produced= 80 committed= 68 lag= 12 dlq=13
tick=12 consumers=2 produced= 80 committed= 76 lag=  4 dlq=16
tick=13 consumers=2 produced= 80 committed= 80 lag=  0 dlq=18
tick=14 consumers=2 produced= 80 committed= 80 lag=  0 dlq=18
processed ok: 62 | in DLQ: 18 | flaky ones that succeeded after retry: 3
{'topic': 'tx', 'partition': 0, 'offset': 7, 'error': 'schema_mismatch: amt not number', 'attempts': 0, 'payload': '{"card": "c2", "amt": "x"}', 'tick': 2}
{'topic': 'tx', 'partition': 0, 'offset': 12, 'error': 'null_key', 'attempts': 0, 'payload': '{"card": null, "amt": 5}', 'tick': 4}
{'topic': 'tx', 'partition': 0, 'offset': 17, 'error': 'null_key', 'attempts': 0, 'payload': '{"card": null, "amt": 5}', 'tick': 5}
{'topic': 'tx', 'partition': 0, 'offset': 24, 'error': 'null_key', 'attempts': 0, 'payload': '{"card": null, "amt": 5}', 'tick': 6}
DLQ by reason: {'null_key': 9, 'parse_error': 4, 'retries_exhausted': 1, 'schema_mismatch': 4}
```

**Follow-ups:**
- *Why not just skip bad messages?* You lose data silently and cannot tell the producer team. Park and count them.
- *How do you replay the DLQ?* After the fix, a small job reads the DLQ topic and re-produces the original bytes to the source topic or a retry topic. Make processing idempotent first.
- *Lag is huge and adding consumers does not help?* Check partition count (consumers above it sit idle), hot keys, and whether the slow part is the downstream sink.

**Common mistakes:**
- Retrying parse errors forever.
- Re-serialising the message before putting it in the DLQ, so the evidence is gone.
- Committing the offset before processing finishes.
- Watching lag but not DLQ volume (a producer bug can silently park 100% of traffic).
- Believing more consumers always help (partition count is the cap).

### Q20 ⭐⭐ 🟡 Streaming rolling features with state: 'number of transactions per card in the last hour and last 24 hours'. Explain per-key state, sliding versus tumbling approximations, state size and state TTL, out-of-order events, and how the same feature is recomputed offline for training. Implement a per-key deque-based sliding window in pure Python, check it against a pandas rolling computation on a small event list (hand-checkable), and report where the two disagree and why.
**Asked at:** Stream-processing concept sources (Databricks 2017 blog 'Event-time aggregation and watermarking in Apache Spark Structured Streaming', Databricks watermarking deep dive, a codecentric.de Spark and Flink event-time post, an oneuptime late-data post, datadriven.io streaming system design questions; search snippets only, not opened); vendor and practitioner blogs, not interview reports; data engineer and streaming roles | Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs
**Say this first (1 line):** Keep a small per-card state (timestamps in a deque, or time buckets), evict old entries on every event, expire idle keys, and accept that the streaming value is "as known at that moment", so it can differ from an offline recompute that sees late events.

**Then explain:**
- **Per-key state.** Stream processors keep state keyed by card. For an exact "last 1 hour" count you store the timestamps in the window. Memory is events-in-window times number of keys. A busy card with a 24 h window makes that large.
- **Sliding versus tumbling.** Tumbling windows (fixed hour buckets) are cheap but the value jumps at the boundary and is stale. Sliding is exact but costly. The common middle path is many small buckets (for example 1 minute) summed over the window: state is bounded by buckets, error is at most one bucket.
- **State TTL.** Drop a key when it has been idle longer than the longest window. Without TTL, state grows with every card you ever saw.
- **Out-of-order events.** A deque that assumes sorted input breaks when a late event is appended at the end: eviction stops at the first fresh element and stale entries stay behind. Fix with a sorted structure plus a watermark (allowed lateness), then either update or drop very late events.
- **Offline recompute for training.** Use event time and the same window rule in pandas or SQL. Pin the boundary rule: pandas `rolling("60min")` is `(t-60, t]` by default (`closed="right"`). Be clear that offline sees late events, the stream may not have yet. Log served values to train on what the model really saw.

**Example (hand-check):** card A events at minutes 0, 20, 60, 70, then a late one at 50 (arrives after 70), then 120. Window is the 60 minutes up to and including the event time.
- At minute 60 offline sees 20, 50, 60 = 3. The stream had not yet seen 50, so it said 2.
- At minute 120 the window is (60, 120], so 70 and 120 = 2. The naive deque said 3: the late 50 sat behind 70 in the deque, so eviction stopped at 70 and the stale 50 stayed in the count. The sorted-buffer fix says 2.

**Code:**
```python
# Per-key sliding window count (last 60 minutes) in pure Python vs pandas rolling.
from collections import deque, defaultdict
import pandas as pd

# (card, minute-of-day, arrival order is list order). Event 5 (minute 50) arrives late.
events = [("A", 0), ("A", 20), ("A", 60), ("B", 10), ("A", 70), ("A", 50), ("B", 75), ("A", 120)]

# 1) streaming version: arrival order, state = deque of timestamps per key
state = defaultdict(deque)
def on_event(card, t, window=60):
    dq = state[card]
    dq.append(t)                              # naive: assumes timestamps arrive in order
    while dq and dq[0] <= t - window:         # window is (t-60, t]: an event exactly 60 min old is out
        dq.popleft()
    return len(dq)

stream = [on_event(c, t) for c, t in events]

# 2) offline version: sort by event time, pandas rolling (default closed='right' = (t-60, t])
df = pd.DataFrame(events, columns=["card", "t"])
df["arrival"] = range(len(df))
df["ts"] = pd.Timestamp("2025-01-01") + pd.to_timedelta(df["t"], unit="m")
s = df.sort_values("ts").set_index("ts").groupby("card")["arrival"].rolling("60min").count()
# rolling output is indexed by (card, ts); map back to events by (card, ts)
lookup = {(r.card, r.ts): int(r.offline_count) for r in s.reset_index().rename(columns={"arrival": "offline_count"}).itertuples()}
df["stream_count"] = stream
df["offline_count"] = [lookup[(c, ts)] for c, ts in zip(df.card, df.ts)]
df["match"] = df.stream_count == df.offline_count
print(df[["card", "t", "arrival", "stream_count", "offline_count", "match"]].to_string(index=False))
print("disagreements:", int((~df.match).sum()))

# 3) fix the deque bug: keep a sorted buffer per key (insort) so a late event cannot break eviction.
import bisect
buf = defaultdict(list)
def on_event_sorted(card, t, window=60):
    bisect.insort(buf[card], t)
    return sum(1 for x in buf[card] if t - window < x <= t)   # count as of THIS event's own time
fixed = [on_event_sorted(c, t) for c, t in events]

# reference: offline rule applied only to events that had ARRIVED by then (what a stream can know)
def as_of_arrival(i):
    c, t = events[i]
    return sum(1 for cc, tt in events[:i + 1] if cc == c and t - 60 < tt <= t)
ref = [as_of_arrival(i) for i in range(len(events))]
print("sorted-buffer :", fixed)
print("as-of-arrival :", ref, "equal:", fixed == ref)
print("offline (all) :", list(df.offline_count), "-> differs only where a late event had not arrived yet")
```

**Output (my run):** (pandas 3.1.0 in the helper venv, python3.13, `-I`)
```
card   t  arrival  stream_count  offline_count  match
   A   0        0             1              1   True
   A  20        1             2              2   True
   A  60        2             2              3  False
   B  10        3             1              1   True
   A  70        4             3              4  False
   A  50        5             4              3  False
   B  75        6             1              1   True
   A 120        7             3              2  False
disagreements: 4
sorted-buffer : [1, 2, 2, 1, 3, 3, 1, 2]
as-of-arrival : [1, 2, 2, 1, 3, 3, 1, 2] equal: True
offline (all) : [1, 2, 3, 1, 4, 3, 1, 2] -> differs only where a late event had not arrived yet
```

**Follow-ups:**
- *Where do they disagree and why?* Four rows: two are late-event timing (the stream could not know about minute 50 yet), one is the late event's own row, and one is the broken eviction at minute 120. The fixed version equals "offline restricted to events that had arrived".
- *How do you make training match serving?* Either log the served feature values, or replay the raw events through the same code in arrival order with the same watermark.
- *How do you cut state for 24 h?* Buckets of 1 to 5 minutes, or approximate sketches when exact counts are not needed.

**Common mistakes:**
- Using processing time for the window and event time offline.
- Off-by-one on the boundary (is an event exactly 60 minutes old in or out?).
- Assuming sorted input.
- No state TTL.
- Computing the offline feature with future events (leakage) that the stream never had.

### Q21 ⭐⭐ 🟡 Spark join strategies for building a training set: a large label table joined to a large feature table versus a small dimension table. Explain broadcast hash join, sort-merge join and shuffle hash join, the broadcast threshold, join hints, and how to read the physical plan. Run local PySpark with a broadcast hint and with broadcasting disabled, print both explain() plans, and say which parts depend on the Spark version.
**Asked at:** Spark interview question banks (dev.to datadriven 'Top 12 Spark interview problems for data engineers', devgenius 'Spark Interview Question' posts, datadriven.io Spark optimization and PySpark pages, a techinterview.org 'Why your Spark job is slow' post, a Scribd PySpark crash guide; search snippets only, not opened; the search found no India-specific Spark source); editorial prep material, not verified candidate reports; data engineer and ML engineer roles
**Say this first (1 line):** Broadcast the small table so nothing shuffles, sort-merge join two big tables (shuffle both sides, sort, merge), use shuffle-hash when one side is clearly smaller but too big to broadcast, and read the physical plan for `BroadcastHashJoin`, `SortMergeJoin`, `ShuffledHashJoin` and the `Exchange` nodes.

**Then explain:**
- **Broadcast hash join.** The small side is collected, sent to every executor and hashed. The big side is not shuffled. It is fastest, but a table that is too big for driver and executor memory fails the job. Spark picks it automatically below `spark.sql.autoBroadcastJoinThreshold` (default about 10 MB; check current docs) when it knows the size. A hint `broadcast(df)` forces it.
- **Sort-merge join.** The default for two large sides. Both sides are hash-partitioned on the join key (an `Exchange`), sorted, then merged. It scales and spills to disk, but the shuffle costs network and disk.
- **Shuffle hash join.** Both sides shuffled, but no sort: a hash table is built from the smaller side per partition. Use hint `SHUFFLE_HASH` when memory per partition is fine. Other hints: `MERGE`, `SHUFFLE_REPLICATE_NL`.
- **Reading the plan.** Look for the join node name, then count `Exchange` lines (each is a shuffle). `BroadcastExchange` means broadcast. Skew shows up as a few huge tasks in the Spark UI (not run here).
- **Version dependence.** I turned off adaptive query execution (AQE) so the plans are stable. In recent Spark, AQE is on by default and can switch a sort-merge join to broadcast at runtime and split skewed partitions, so your real plan may start with `AdaptiveSparkPlan`. Plan text and node details change between versions. This ran on Spark 4.2.0.
- **For a training set.** Labels with timestamps against feature history is not a plain equi-join (it is a point-in-time join). The usual pattern is to equi-join on entity and then keep the latest feature row at or before the label time, covered by the point-in-time join question earlier in this part. The join strategy question is only about the entity join and the dimension lookups.

**Example:** 20,000 label rows, 5,000 feature rows, 5 dimension rows. Dimension join with hint: `BroadcastHashJoin`, no Exchange on the big side. Same join with broadcast disabled: `SortMergeJoin` with an Exchange and a Sort on both sides. Big-by-big: sort-merge, or `ShuffledHashJoin` with the hint. Row counts are identical across strategies (20,000), as they must be.

**Code:** (`spark_common.py` is a small helper that sets local[2], UI off, 4 shuffle partitions, AQE off and a unique warehouse and local dir)
```python
# ---- file: spark_common.py ----
import os, sys, tempfile
from pyspark.sql import SparkSession

def get_spark(name, extra=None):
    os.environ["PYSPARK_PYTHON"] = sys.executable   # workers must use the venv python (has pyarrow)
    base = os.path.join("/tmp/claude-0/b9_q19_27/work", name)
    os.makedirs(base, exist_ok=True)
    b = (SparkSession.builder.master("local[2]").appName(name)
         .config("spark.ui.enabled", "false").config("spark.ui.showConsoleProgress", "false")
         .config("spark.sql.shuffle.partitions", "4")
         .config("spark.default.parallelism", "4")
         .config("spark.local.dir", os.path.join(base, "local"))
         .config("spark.sql.warehouse.dir", os.path.join(base, "warehouse"))
         .config("spark.driver.bindAddress", "127.0.0.1").config("spark.driver.host", "127.0.0.1")
         .config("spark.sql.adaptive.enabled", "false"))   # fixed plans for teaching; AQE can change them
    for k, v in (extra or {}).items(): b = b.config(k, v)
    s = b.getOrCreate(); s.sparkContext.setLogLevel("ERROR")
    return s, base

# ---- file: q21_joins.py ----
import sys; sys.path.insert(0, "/home/user/case_studies/interviews/scratch/B4P09_Q19-27/code")
from spark_common import get_spark
from pyspark.sql import functions as F
spark, _ = get_spark("q21")
print("pyspark", __import__("pyspark").__version__, "| AQE off for stable plans")

labels = spark.range(0, 20000).select((F.col("id") % 5000).alias("user_id"), (F.col("id") % 2).alias("label"))
feats  = spark.range(0, 5000).select(F.col("id").alias("user_id"), (F.col("id") * 3 % 100).alias("f_score"))
dim    = spark.createDataFrame([(i, f"seg{i%3}") for i in range(5)], ["bucket", "segment"])
labels = labels.withColumn("bucket", F.col("user_id") % 5)

def show(title, df):
    print("==", title)
    lines = df._jdf.queryExecution().executedPlan().toString().split("\n")
    for l in lines:
        if any(k in l for k in ("Join", "Exchange", "BroadcastExchange", "Sort", "Scan", "Range")):
            print(l.rstrip()[:110])

# A: large x small dim, broadcast hint
a = labels.join(F.broadcast(dim), "bucket")
show("A. large x small, broadcast() hint", a)
# B: same join, broadcast disabled and no hint
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
b = labels.join(dim, "bucket")
show("B. large x small, autoBroadcastJoinThreshold=-1", b)
# C: large x large (both sides too big to broadcast): sort-merge
c = labels.join(feats, "user_id")
show("C. large x large, broadcast off", c)
# D: shuffle hash join by hint
d = labels.join(feats.hint("shuffle_hash"), "user_id")
show("D. large x large, hint shuffle_hash", d)
print("row counts equal across strategies (A,B):", a.count() == b.count(), a.count(), "| C,D:", c.count() == d.count(), c.count())
spark.stop()
```

**Output (my run):** (PySpark 4.2.0, local[2], openjdk 21; plan lines filtered to join, Exchange, Sort, scan nodes)
```
pyspark 4.2.0 | AQE off for stable plans
== A. large x small, broadcast() hint
+- *(2) BroadcastHashJoin [bucket#8L], [bucket#6L], Inner, BuildRight, false, false
   :        +- *(2) Range (0, 20000, step=1, splits=4)
   +- BroadcastExchange HashedRelationBroadcastMode(List(input[0, bigint, false]),false), [plan_id=35]
         +- *(1) Scan ExistingRDD[bucket#6L,segment#7]
== B. large x small, autoBroadcastJoinThreshold=-1
+- *(5) SortMergeJoin [bucket#8L], [bucket#6L], Inner
   :- *(2) Sort [bucket#8L ASC NULLS FIRST], false, 0
   :  +- Exchange hashpartitioning(bucket#8L, 4), ENSURE_REQUIREMENTS, [plan_id=85]
   :              +- *(1) Range (0, 20000, step=1, splits=4)
   +- *(4) Sort [bucket#6L ASC NULLS FIRST], false, 0
      +- Exchange hashpartitioning(bucket#6L, 4), ENSURE_REQUIREMENTS, [plan_id=91]
            +- *(3) Scan ExistingRDD[bucket#6L,segment#7]
== C. large x large, broadcast off
+- *(5) SortMergeJoin [user_id#1L], [user_id#4L], Inner
   :- *(2) Sort [user_id#1L ASC NULLS FIRST], false, 0
   :  +- Exchange hashpartitioning(user_id#1L, 4), ENSURE_REQUIREMENTS, [plan_id=155]
   :              +- *(1) Range (0, 20000, step=1, splits=4)
   +- *(4) Sort [user_id#4L ASC NULLS FIRST], false, 0
      +- Exchange hashpartitioning(user_id#4L, 4), ENSURE_REQUIREMENTS, [plan_id=161]
            +- *(3) Range (0, 5000, step=1, splits=4)
== D. large x large, hint shuffle_hash
+- *(3) ShuffledHashJoin [user_id#1L], [user_id#4L], Inner, BuildRight
   :- Exchange hashpartitioning(user_id#1L, 4), ENSURE_REQUIREMENTS, [plan_id=222]
   :           +- *(1) Range (0, 20000, step=1, splits=4)
   +- Exchange hashpartitioning(user_id#4L, 4), ENSURE_REQUIREMENTS, [plan_id=225]
         +- *(2) Range (0, 5000, step=1, splits=4)
row counts equal across strategies (A,B): True 20000 | C,D: True 20000
```

**Follow-ups:**
- *Why did the small DataFrame from a Python list not auto-broadcast?* It was an RDD with no size statistics, so I used a hint. Tables read from files have size stats and can broadcast on their own.
- *The join is slow because one key has most rows?* That is skew. Options: AQE skew handling (version dependent), salting the key, or broadcasting the small side. Check current docs.
- *Why is sort-merge the default for big joins?* It can spill, so it is safer than a hash table that must fit in memory.

**Common mistakes:**
- Forcing a broadcast on a table that grows over time.
- Reading `explain()` without noticing the Exchange count.
- Forgetting that AQE changes what actually runs.
- Joining on a nullable key and losing rows (nulls never match).
- Thinking hints are guaranteed (the optimizer may ignore one that cannot apply).

### Q22 ⭐⭐ 🟡 Python UDF versus built-in function versus pandas (Arrow) UDF in a PySpark feature pipeline. Explain the JVM to Python serialisation cost, why built-ins are optimised by Catalyst and UDFs are black boxes, and when a vectorised UDF is the right tool. Run the same feature three ways on local PySpark, check the results match, show in explain() how the UDF appears in the plan, and report sandbox-only timings with an honest caveat that they prove nothing about a cluster.
**Asked at:** PySpark UDF and layout sources (Databricks blog 'Introducing Arrow UDFs for PySpark', datavidhya UDF tutorial, a DZone Spark performance article; search snippets only, not opened; the '10 to 100x slower' UDF claim and the '10 percent faster, 40 percent less memory' Arrow UDF claim are tutorial and vendor claims, not used as numbers; the search found nothing on small files or Parquet and Delta compaction, so those answers rest on Spark and Delta docs knowledge and the local run) | Spark interview question banks (dev.to datadriven 'Top 12 Spark interview problems for data engineers', devgenius 'Spark Interview Question' posts, datadriven.io Spark optimization and PySpark pages, a techinterview.org 'Why your Spark job is slow' post, a Scribd PySpark crash guide; search snippets only, not opened; the search found no India-specific Spark source); editorial prep material, not verified candidate reports; data engineer and ML engineer roles
**Say this first (1 line):** Prefer built-in functions (Catalyst optimises them and they run in the JVM), use a vectorised pandas or Arrow UDF when you need Python logic, and use a plain row-at-a-time Python UDF last, because every row crosses the JVM-Python boundary.

**Then explain:**
- **Built-ins.** Catalyst understands them: it can push filters, prune columns, fold constants and generate code. The whole thing stays inside the JVM.
- **UDFs are black boxes.** Catalyst cannot look inside, so no pushdown through them and no codegen. In the plan they appear as an `EvalPython` node.
- **The cost is serialisation.** Rows move from the JVM to a Python worker and back. The classic Python UDF does this row by row with pickle (`BatchEvalPython`). Pandas and Arrow UDFs move columnar batches (`ArrowEvalPython`), so less overhead and you can use vectorised NumPy and pandas code.
- **Version note.** In this Spark 4.2.0 run, even a plain `udf` was Arrow-optimised by default; I had to pass `useArrow=False` to get the classic row-at-a-time path. Older versions defaulted to pickle. Check your version's docs.
- **When to reach for a UDF.** A library call you cannot express with built-ins (a model score, a custom parser). Then batch it with a pandas UDF. Also null handling: you must handle `None` yourself in a UDF.

**Example:** feature `amount / (amount + 50)` over 400,000 rows. All four forms returned the same sum (180144.149674) and count (400,000). In the plan the built-in is a single `Project` expression; the UDF forms add a `BatchEvalPython` or `ArrowEvalPython` node.

**Code:**
```python
import sys, time; sys.path.insert(0, "/home/user/case_studies/interviews/scratch/B4P09_Q19-27/code")
from spark_common import get_spark
from pyspark.sql import functions as F
from pyspark.sql.functions import udf, pandas_udf
from pyspark.sql.types import DoubleType
import pandas as pd

spark, _ = get_spark("q22", {"spark.sql.execution.arrow.maxRecordsPerBatch": "10000"})
print("pyspark", __import__("pyspark").__version__, "pandas", pd.__version__)
N = 400_000
df = spark.range(N).select(F.col("id"), ((F.col("id") * 7919) % 1000 / 10.0).alias("amount"))
# Feature: log-ish squash  amount / (amount + 50)
builtin = df.withColumn("f", F.col("amount") / (F.col("amount") + F.lit(50.0)))

def _f(x): return x / (x + 50.0)
py_udf = udf(_f, DoubleType(), useArrow=False)     # classic row-at-a-time pickled Python UDF
py_arrow_udf = udf(_f, DoubleType(), useArrow=True)  # Arrow-optimised Python UDF (default in recent Spark; check your version)

@pandas_udf(DoubleType())
def vec_udf(x: pd.Series) -> pd.Series: return x / (x + 50.0)

py = df.withColumn("f", py_udf("amount"))
vec = df.withColumn("f", vec_udf("amount"))
pya = df.withColumn("f", py_arrow_udf("amount"))

def bench(label, d):
    d.agg(F.sum("f")).collect()               # warm up (JVM + Python worker start)
    ts = []
    for _ in range(5):
        t = time.perf_counter(); r = d.agg(F.sum("f").alias("s"), F.count("f").alias("n")).collect()[0]
        ts.append(time.perf_counter() - t)
    dt = sorted(ts)[2]                        # median of 5
    return label, r["s"], r["n"], dt

res = [bench("built-in", builtin), bench("python udf (row)", py), bench("python udf (arrow)", pya), bench("pandas (arrow) udf", vec)]
base = res[0][1]
for label, s, n, dt in res:
    print(f"{label:21s} sum={s:.6f} n={n} match_builtin={abs(s-base)<1e-6} median_of_5={dt:.2f}s (sandbox only)")

def plan_lines(d, keys):
    for l in d._jdf.queryExecution().executedPlan().toString().split("\n"):
        if any(k in l for k in keys): print("  ", l.strip()[:120])
print("-- plan, built-in:");   plan_lines(builtin, ("Project", "Range"))
print("-- plan, python udf:"); plan_lines(py, ("EvalPython", "Project", "Range"))
print("-- plan, python udf (arrow):"); plan_lines(pya, ("EvalPython", "Project", "Range"))
print("-- plan, pandas udf:"); plan_lines(vec, ("EvalPython", "Project", "Range"))
spark.stop()
```

**Output (my run):** (PySpark 4.2.0, pandas 2.3.3, pyarrow, local[2]; the helper `spark_common.py` is the one shown in Q21)
```
pyspark 4.2.0 pandas 2.3.3
built-in              sum=180144.149674 n=400000 match_builtin=True median_of_5=0.19s (sandbox only)
python udf (row)      sum=180144.149674 n=400000 match_builtin=True median_of_5=0.49s (sandbox only)
python udf (arrow)    sum=180144.149674 n=400000 match_builtin=True median_of_5=0.29s (sandbox only)
pandas (arrow) udf    sum=180144.149674 n=400000 match_builtin=True median_of_5=0.24s (sandbox only)
-- plan, built-in:
   *(1) Project [id#0L, amount#1, (amount#1 / (amount#1 + 50.0)) AS f#2]
   +- *(1) Project [id#0L, (cast(((id#0L * 7919) % 1000) as double) / 10.0) AS amount#1]
   +- *(1) Range (0, 400000, step=1, splits=4)
-- plan, python udf:
   *(2) Project [id#0L, amount#1, pythonUDF0#319 AS f#4]
   +- BatchEvalPython [_f(amount#1)#3], [pythonUDF0#319]
   +- *(1) Project [id#0L, (cast(((id#0L * 7919) % 1000) as double) / 10.0) AS amount#1]
   +- *(1) Range (0, 400000, step=1, splits=4)
-- plan, python udf (arrow):
   *(2) Project [id#0L, amount#1, pythonUDF0#320 AS f#8]
   +- ArrowEvalPython [_f(amount#1)#7], [pythonUDF0#320], 101
   +- *(1) Project [id#0L, (cast(((id#0L * 7919) % 1000) as double) / 10.0) AS amount#1]
   +- *(1) Range (0, 400000, step=1, splits=4)
-- plan, pandas udf:
   *(2) Project [id#0L, amount#1, pythonUDF0#321 AS f#6]
   +- ArrowEvalPython [vec_udf(amount#1)#5], [pythonUDF0#321], 200
   +- *(1) Project [id#0L, (cast(((id#0L * 7919) % 1000) as double) / 10.0) AS amount#1]
   +- *(1) Range (0, 400000, step=1, splits=4)
```

**Follow-ups:**
- *Timings?* Sandbox-only, median of 5, two cores, one machine, tiny data, JVM warm. They show the order (built-in fastest) but prove nothing about a cluster. Do not quote them.
- *Why is the pandas UDF not always the winner?* The per-batch overhead and Arrow conversion still cost something, and a simple expression is cheaper as a built-in. Gains show up when the Python body is heavy and vectorised.
- *Can I avoid Python entirely?* Yes, Spark SQL expressions, higher-order functions or a Scala/Java UDF.

**Common mistakes:**
- Writing a UDF for something `F.when`, `F.regexp_extract` or `F.expr` already does.
- A row-at-a-time UDF that calls a model per row.
- Quoting a laptop speed-up as a cluster number.
- Forgetting the Python workers need the same environment (I had to set `PYSPARK_PYTHON` to the venv Python).
- Returning a wrong or missing type, so values silently become null.

### Q23 ⭐⭐ 🟡 Parquet and Delta layout for feature data: partition columns and cardinality, partition pruning, small-files problem, file size targets, compaction (repartition, OPTIMIZE), and why a time-partitioned feature table makes point-in-time reads cheap. Run local PySpark to write the same data partitioned by day with many tiny files and again compacted, count files, and show the partition filter in the plan. If Delta OSS was available, show a Delta table's transaction log and say which version ran.
**Asked at:** PySpark UDF and layout sources (Databricks blog 'Introducing Arrow UDFs for PySpark', datavidhya UDF tutorial, a DZone Spark performance article; search snippets only, not opened; the '10 to 100x slower' UDF claim and the '10 percent faster, 40 percent less memory' Arrow UDF claim are tutorial and vendor claims, not used as numbers; the search found nothing on small files or Parquet and Delta compaction, so those answers rest on Spark and Delta docs knowledge and the local run) | Spark interview question banks (dev.to datadriven 'Top 12 Spark interview problems for data engineers', devgenius 'Spark Interview Question' posts, datadriven.io Spark optimization and PySpark pages, a techinterview.org 'Why your Spark job is slow' post, a Scribd PySpark crash guide; search snippets only, not opened; the search found no India-specific Spark source); editorial prep material, not verified candidate reports; data engineer and ML engineer roles
**Say this first (1 line):** Partition the feature table by a low-cardinality time column such as day so reads for a date range skip other folders, keep files large enough (not thousands of tiny ones), and compact regularly (repartition on write, or `OPTIMIZE` on Delta).

**Then explain:**
- **Partition column choice.** Low cardinality and used in filters: day or hour. Never a user id (millions of folders). Partition columns become folders such as `day=2025-03-04`.
- **Pruning.** A filter on the partition column shows up as `PartitionFilters` in the scan and only matching folders are listed and read. A filter on a normal column only becomes a `DataFilter` (Parquet row-group statistics may skip some data, but folders are not skipped).
- **Small files problem.** Many writer tasks each write a small file per partition. Reads pay per-file open and listing costs and metadata grows. Typical target is a few hundred MB per file (rule of thumb, check docs for your engine), but sizes depend on the workload.
- **Compaction.** Plain Parquet: rewrite with `repartition("day")` (one task per day) or `coalesce`, then swap the folder. Delta: `OPTIMIZE` rewrites small files into bigger ones as a new commit. Old files stay on disk until `VACUUM`.
- **Why time-partitioned helps point-in-time reads.** Training for label dates in a window reads only those days plus a lookback of feature days. Always filter on the partition column and keep the as-of logic in the query.
- **Trade-off.** Too many partitions with little data in each is the same small-files problem again. Late-arriving data rewrites old partitions.

**Example:** 12,000 rows over 6 days. Written from 24 tasks it made 144 files (6 days x 24 tasks). With `repartition("day")` it made 6 files. Same row count and feature sum. The Delta table: four small appends gave 12 data files and 4 log files; after `OPTIMIZE`, commit 4 had 12 `remove` actions and 1 `add`, and `DESCRIBE DETAIL` reports 1 live file (13 files on disk until vacuum).

**Code:** (two scripts, same helper as Q21 for the first)
```python
# ---- file: q23_layout.py ----
import sys, os, glob, shutil; sys.path.insert(0, "/home/user/case_studies/interviews/scratch/B4P09_Q19-27/code")
from spark_common import get_spark
from pyspark.sql import functions as F
spark, base = get_spark("q23")
print("pyspark", __import__("pyspark").__version__)
out = os.path.join(base, "feat"); shutil.rmtree(out, ignore_errors=True)

# 6 days x 2000 users, one feature value per user per day (seeded, deterministic)
df = (spark.range(12000).select((F.col("id") % 2000).alias("user_id"),
        F.expr("date_add(DATE'2025-03-01', cast(id div 2000 as int))").alias("day"),
        (F.rand(23) * 100).alias("txn_30d")))

def nfiles(path): return len(glob.glob(path + "/**/*.parquet", recursive=True))
def ndirs(path):  return len(glob.glob(path + "/day=*"))

# tiny files: 24 write tasks, each holds rows of every day -> up to 24 files per day
df.repartition(24).write.partitionBy("day").mode("overwrite").parquet(out + "_tiny")
print("tiny    : partitions(dirs)=", ndirs(out + "_tiny"), " parquet files=", nfiles(out + "_tiny"))

# compacted: shuffle by the partition column so each day lands in one task -> about 1 file per day
df.repartition("day").write.partitionBy("day").mode("overwrite").parquet(out + "_compact")
print("compact : partitions(dirs)=", ndirs(out + "_compact"), " parquet files=", nfiles(out + "_compact"))

# same answer either way
a = spark.read.parquet(out + "_tiny"); b = spark.read.parquet(out + "_compact")
print("row counts:", a.count(), b.count(), "| sum of feature equal:",
      abs(a.agg(F.sum("txn_30d")).first()[0] - b.agg(F.sum("txn_30d")).first()[0]) < 1e-6)

# partition pruning: filter on the partition column
q = b.filter(F.col("day") == "2025-03-04")
print("-- scan line for day = 2025-03-04")
for l in q._jdf.queryExecution().executedPlan().toString().split("\n"):
    if "FileScan" in l: print("  ", l.strip().split("Location:")[0][:90], "...", "PartitionFilters:", l.split("PartitionFilters:")[1].split(", PushedFilters")[0][:120])
print("rows for that day:", q.count(), "(expected 2000)")
# a filter on a NON-partition column cannot prune directories
q2 = b.filter(F.col("user_id") == 7)
for l in q2._jdf.queryExecution().executedPlan().toString().split("\n"):
    if "FileScan" in l: print("-- filter on user_id (not a partition column): PartitionFilters:", l.split("PartitionFilters:")[1].split(", PushedFilters")[0][:60], "| DataFilters:", l.split("DataFilters:")[1].split(", Format")[0])
spark.stop()

# ---- file: q23_delta.py ----
import sys, os, glob, json, shutil; sys.path.insert(0, "/home/user/case_studies/interviews/scratch/B4P09_Q19-27/code")
from pyspark.sql import SparkSession, functions as F
from delta import configure_spark_with_delta_pip
import delta
base = "/tmp/claude-0/b9_q19_27/work/q23d"; os.makedirs(base, exist_ok=True)
os.environ["PYSPARK_PYTHON"] = sys.executable
b = (SparkSession.builder.master("local[2]").appName("q23d").config("spark.ui.enabled", "false")
     .config("spark.ui.showConsoleProgress", "false").config("spark.sql.shuffle.partitions", "4")
     .config("spark.local.dir", base + "/local").config("spark.sql.warehouse.dir", base + "/wh")
     .config("spark.driver.bindAddress", "127.0.0.1").config("spark.driver.host", "127.0.0.1")
     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog"))
spark = configure_spark_with_delta_pip(b).getOrCreate(); spark.sparkContext.setLogLevel("ERROR")
print("pyspark", __import__("pyspark").__version__, "delta-spark", delta.__version__ if hasattr(delta, "__version__") else "see pip")
path = base + "/tbl"; shutil.rmtree(path, ignore_errors=True)
for i in range(4):   # four small appends = four commits of small files
    (spark.range(i * 500, (i + 1) * 500).select("id", (F.col("id") % 7).alias("f"))
          .repartition(3).write.format("delta").mode("append").save(path))
nf = lambda: len([f for f in glob.glob(path + "/*.parquet")])
print("after 4 appends: data files on disk =", nf(), "| log files =", sorted(os.path.basename(f) for f in glob.glob(path + "/_delta_log/*.json")))
spark.sql(f"OPTIMIZE delta.`{path}`").collect()
log = sorted(glob.glob(path + "/_delta_log/*.json"))[-1]
acts = [list(json.loads(l).keys())[0] for l in open(log)]
print("latest commit", os.path.basename(log), "actions:", {a: acts.count(a) for a in sorted(set(acts))})
live = spark.sql(f"DESCRIBE DETAIL delta.`{path}`").select("numFiles").first()[0]
print("live files after OPTIMIZE (numFiles) =", live, "| files still on disk (old ones await VACUUM) =", nf())
print("rows:", spark.read.format("delta").load(path).count(), "(expected 2000)")
spark.stop()
```

**Output (my run):** (PySpark 4.2.0, delta-spark 4.4.1 resolved its Delta jar through ivy at run time, local[2])
```
# ---- q23_layout.txt ----
pyspark 4.2.0
tiny    : partitions(dirs)= 6  parquet files= 144
compact : partitions(dirs)= 6  parquet files= 6
row counts: 12000 12000 | sum of feature equal: True
-- scan line for day = 2025-03-04
   +- FileScan parquet [user_id#7L,txn_30d#8,day#9] Batched: true, DataFilters: [], Format: P ... PartitionFilters:  [isnotnull(day#9), (day#9 = 2025-03-04)]
rows for that day: 2000 (expected 2000)
-- filter on user_id (not a partition column): PartitionFilters:  [] | DataFilters:  [isnotnull(user_id#7L), (user_id#7L = 7)]

# ---- q23_delta.txt ----
pyspark 4.2.0 delta-spark 4.4.1
after 4 appends: data files on disk = 12 | log files = ['00000000000000000000.json', '00000000000000000001.json', '00000000000000000002.json', '00000000000000000003.json']
latest commit 00000000000000000004.json actions: {'add': 1, 'commitInfo': 1, 'remove': 12}
live files after OPTIMIZE (numFiles) = 1 | files still on disk (old ones await VACUUM) = 13
rows: 2000 (expected 2000)
```

**Follow-ups:**
- *What does the Delta log hold?* JSON commit files with `add`, `remove` and `commitInfo` actions. That is what gives ACID commits and time travel.
- *Does OPTIMIZE delete old files?* No, it only removes them from the table version. `VACUUM` removes them physically after the retention period.
- *Partition by hour or day?* Pick by query pattern and data volume per partition. Too fine means small files.

**Common mistakes:**
- Partitioning by a high-cardinality column.
- Wrapping the partition column in a function in the filter, which can block pruning.
- Running tiny streaming micro-batches to a table and never compacting.
- Vacuuming with a retention shorter than the longest-running reader or time-travel need.
- Counting files in a folder, not in the table version (Delta keeps old files).

### Q24 ⭐⭐ 🟡 Caching, persist and partition sizing in a Spark ML feature pipeline. When does cache() help (a DataFrame reused by several actions), when does it hurt, what storage levels mean, how to choose the number of partitions (cores, data size, shuffle.partitions), and why coalesce and repartition differ. Run local PySpark, count how many times a source is read with and without cache using an accumulator or a plan check, and show partition counts before and after repartition and coalesce.
**Asked at:** Spark interview question banks (dev.to datadriven 'Top 12 Spark interview problems for data engineers', devgenius 'Spark Interview Question' posts, datadriven.io Spark optimization and PySpark pages, a techinterview.org 'Why your Spark job is slow' post, a Scribd PySpark crash guide; search snippets only, not opened; the search found no India-specific Spark source); editorial prep material, not verified candidate reports; data engineer and ML engineer roles
**Say this first (1 line):** Cache a DataFrame only when several actions reuse it and it fits memory (or memory and disk), release it when done, and size partitions to the cores and data (a few tasks per core, not too tiny) using `repartition` to rebalance (shuffle) and `coalesce` to shrink without a shuffle.

**Then explain:**
- **What cache does.** Spark is lazy: every action recomputes the lineage from the source unless the data is persisted. `cache()` or `persist()` keeps computed partitions so the second action reads them instead. It only takes effect once an action materialises it.
- **When it hurts.** Used once, or cheap to recompute, or bigger than memory: you pay memory and eviction for nothing and may slow other work. Failure mode: stale cached data when the source changed, and forgotten caches that eat executor memory. Call `unpersist()`.
- **Storage levels.** `MEMORY_ONLY` (recompute what does not fit), `MEMORY_AND_DISK` (spill the rest), `DISK_ONLY`, `_2` variants replicate, and serialised levels trade CPU for space. DataFrame `cache()` uses a memory-and-disk level.
- **Partition count.** Rule of thumb: 2 to 4 tasks per core, and partitions of manageable size (often cited as 100 to 200 MB; check docs). `spark.sql.shuffle.partitions` sets the post-shuffle count (default 200; AQE can coalesce it). Too few: no parallelism, spills. Too many: scheduling overhead and tiny files.
- **repartition versus coalesce.** `repartition(n)` does a full shuffle and balances sizes, and it can grow or shrink. `coalesce(n)` merges existing partitions without a shuffle, can only shrink, and can leave uneven sizes.

**Example:** a source of 10,000 rows with three actions. Without cache the source function ran 30,001 times (3 passes); with cache 10,001. The extra 1 in each is schema inference reading the first row for `toDF`. Partitions: range default 4, `repartition(8)` gives 8 balanced partitions of 12,500 rows, `coalesce(2)` on 4 splits gives 2 of 50,000, `coalesce(16)` stays at 8, and a `groupBy` after a shuffle follows `shuffle.partitions` = 4.

**Code:**
```python
import sys; sys.path.insert(0, "/home/user/case_studies/interviews/scratch/B4P09_Q19-27/code")
from spark_common import get_spark
from pyspark.sql import functions as F
from pyspark import StorageLevel
spark, _ = get_spark("q24")
sc = spark.sparkContext
print("pyspark", __import__("pyspark").__version__, "| cores (defaultParallelism) =", sc.defaultParallelism)

# A "source" that counts how many rows it produced, via an accumulator (counts re-computation).
def build(acc):
    def tag(r):
        acc.add(1); return (r.id, r.id % 10)
    return spark.range(10000).rdd.map(tag).toDF(["id", "k"])

def run(label, use_cache):
    acc = sc.accumulator(0)
    df = build(acc)
    if use_cache: df = df.persist(StorageLevel.MEMORY_AND_DISK)
    a1 = df.groupBy("k").count().count()           # action 1: 10 groups
    a2 = df.filter("k = 3").count()                # action 2: 1000 rows
    a3 = df.agg(F.sum("id")).first()[0]            # action 3
    print(f"{label:10s} actions=3 results=({a1},{a2},{a3}) source rows computed = {acc.value}")
    if use_cache:
        print("           storage level:", df.storageLevel, "| plan has InMemoryTableScan:",
              "InMemoryTableScan" in df.filter("k=3")._jdf.queryExecution().executedPlan().toString())
        df.unpersist()
run("no cache", False)
run("cache", True)
print("(accumulators inside transformations can over-count on task retries; fine as a teaching probe)")

# Partition sizing
df = spark.range(100000)
print("-- partition counts")
print("read default (range splits)         :", df.rdd.getNumPartitions())
r8 = df.repartition(8); print("repartition(8)                      :", r8.rdd.getNumPartitions())
c2 = r8.coalesce(2);    print("repartition(8).coalesce(2)          :", c2.rdd.getNumPartitions())
c16 = r8.coalesce(16);  print("repartition(8).coalesce(16)         :", c16.rdd.getNumPartitions(), "(coalesce cannot grow)")
g = df.withColumn("k", F.col("id") % 10).groupBy("k").count()
print("after groupBy (shuffle.partitions=4):", g.rdd.getNumPartitions())
sizes = r8.rdd.glom().map(len).collect(); print("repartition(8) rows per partition   :", sizes)
sk = df.coalesce(2).rdd.glom().map(len).collect(); print("coalesce(2) from 4 splits, rows/part:", sk)
print("-- plan nodes")
for name, d in [("repartition(8)", r8), ("coalesce(2)", df.coalesce(2))]:
    lines = [l.strip()[:70] for l in d._jdf.queryExecution().executedPlan().toString().split("\n") if "Exchange" in l or "Coalesce" in l]
    print(f"{name:15s}:", lines)
spark.stop()
```

**Output (my run):** (PySpark 4.2.0, local[2]; helper from Q21; the accumulator is a teaching probe, since task retries can over-count)
```
pyspark 4.2.0 | cores (defaultParallelism) = 4
no cache   actions=3 results=(10,1000,49995000) source rows computed = 30001
cache      actions=3 results=(10,1000,49995000) source rows computed = 10001
           storage level: Disk Memory Serialized 1x Replicated | plan has InMemoryTableScan: True
(accumulators inside transformations can over-count on task retries; fine as a teaching probe)
-- partition counts
read default (range splits)         : 4
repartition(8)                      : 8
repartition(8).coalesce(2)          : 2
repartition(8).coalesce(16)         : 8 (coalesce cannot grow)
after groupBy (shuffle.partitions=4): 4
repartition(8) rows per partition   : [12500, 12500, 12500, 12500, 12500, 12500, 12500, 12500]
coalesce(2) from 4 splits, rows/part: [50000, 50000]
-- plan nodes
repartition(8) : ['Exchange RoundRobinPartitioning(8), REPARTITION_BY_NUM, [plan_id=256]']
coalesce(2)    : ['Coalesce 2']
```

**Follow-ups:**
- *Cache or checkpoint?* Cache keeps lineage and can be lost; checkpoint writes to reliable storage and truncates lineage.
- *Why is my cached DataFrame still recomputed?* Nothing materialised it yet, or it was evicted, or you cached a different plan.
- *Why coalesce(1) before a write is risky?* It funnels all data through one task.

**Common mistakes:**
- `cache()` on everything.
- Never unpersisting.
- Expecting `coalesce` to increase partitions.
- Leaving `shuffle.partitions` at the default for tiny data (hundreds of empty tasks) or huge data (giant partitions).
- Measuring cache benefit with one action.

### Q25 ⭐⭐ 🟡 Lambda versus Kappa architecture, and what it means for features. Explain the batch layer plus speed layer plus serving layer, the two-codebase problem, Kappa's single streaming path with replay, and the practical middle ground (one transformation library, lake for backfill, stream for freshness). Say when each is appropriate and where retention limits a replay. Show the two-codebase problem by implementing one feature twice in Python, finding the disagreement on a small event list, then fixing it with one shared function.
**Asked at:** Lambda and Kappa sources (datadriven.io pipeline architecture page, techinterview.org 'Lambda and Kappa Architecture for Big Data', Materialize 'Does Kappa architecture improve on Lambda', a Netflix talk PDF on backfilling streaming pipelines in Kappa architecture hosted on microsites.databricks.com, risingwave.com; search snippets only, not opened); vendor blogs and a conference talk; data platform roles; the feature-store mapping is an expert extension | Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs
**Say this first (1 line):** Lambda runs a batch path and a speed path and merges them in serving, which gives two codebases that drift; Kappa has one streaming path and replays the log for reprocessing; in practice for features I keep one shared transformation, backfill from the lake and use the stream for freshness.

**Then explain:**
- **Lambda.** Batch layer (complete, accurate, slow), speed layer (recent, approximate, fast), serving layer merges. Good when batch accuracy rules matter. Pain: two implementations of the same logic.
- **Kappa.** Everything is a stream. To reprocess, replay the log through the new code. Simple in theory, but replay is limited by how long the log is retained and by the cost of replaying; many teams backfill from the lake instead.
- **For features.** The batch path builds training sets (offline store); the stream path fills the online store. If they are two codebases you get training-serving skew. Fix: one shared transformation function or library used by both, or a framework that runs the same definition in batch and stream (check current docs for your tool).
- **When to use which.** Lambda-ish: you need heavy batch recompute and low-latency partial values. Kappa-ish: logic is simple, events are retained or archived, one team owns it. Middle ground: shared code, lake as source of truth for backfill, stream for freshness.
- **Replay limit.** If Kafka keeps 7 days and the feature window needs 30 days, you cannot rebuild from Kafka alone. You need the lake or compacted state.

**Example:** `spend_today` per user. The batch team uses the IST business day, subtracts refunds, skips nulls. The stream team uses the UTC day and ignores refunds. On six events, user u1 on 2025-03-01 is 100 in batch and 150 in stream, and the late-evening purchase lands on a different day (20 on 03-02 versus 0). After both call one `contribution()` function, they match.

**Code:**
```python
# One feature, "spend_today per user", written twice (batch team and streaming team).
from datetime import datetime, timezone, timedelta
from collections import defaultdict

IST = timezone(timedelta(hours=5, minutes=30))
def ts(s): return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)

events = [  # (user, utc timestamp, amount, kind)
    ("u1", ts("2025-03-01T10:00:00"), 100.0, "purchase"),
    ("u1", ts("2025-03-01T20:00:00"),  50.0, "purchase"),   # 01:30 IST next day
    ("u1", ts("2025-03-01T21:00:00"),  30.0, "refund"),     # refund, stored as positive amount
    ("u2", ts("2025-03-01T09:00:00"),  None, "purchase"),   # missing amount
    ("u2", ts("2025-03-01T11:00:00"),  70.0, "purchase"),
    ("u3", ts("2025-03-02T00:30:00"),  20.0, "purchase"),
]

# --- Codebase 1: batch (analyst SQL-style): business day in IST, refunds subtract, nulls skipped
def batch_spend(events):
    out = defaultdict(float)
    for u, t, amt, kind in events:
        if amt is None: continue
        sign = -1 if kind == "refund" else 1
        out[(u, t.astimezone(IST).date().isoformat())] += sign * amt
    return dict(out)

# --- Codebase 2: streaming (engineer, per-key state): UTC day, refunds ignored, null -> 0
def stream_spend(events):
    out = defaultdict(float)
    for u, t, amt, kind in events:
        if kind == "refund": continue
        out[(u, t.date().isoformat())] += (amt or 0.0)
    return dict(out)

b, s = batch_spend(events), stream_spend(events)
print("key               batch  stream  agree")
for k in sorted(set(b) | set(s)):
    print(f"{str(k):28s} {b.get(k, 0):6.1f} {s.get(k, 0):6.1f}  {b.get(k, 0) == s.get(k, 0)}")

# --- Fix: one shared definition, imported by BOTH the batch job and the stream job
def contribution(user, t, amt, kind):
    """The single definition: (key, signed amount). IST business day, refunds subtract, null skipped."""
    if amt is None: return None
    return (user, t.astimezone(IST).date().isoformat()), (-amt if kind == "refund" else amt)

def run_batch_shared(evts):       # batch calls it over a full list
    out = defaultdict(float)
    for e in evts:
        c = contribution(*e)
        if c: out[c[0]] += c[1]
    return dict(out)

class StreamState:                # stream calls the SAME function one event at a time
    def __init__(self): self.s = defaultdict(float)
    def on_event(self, e):
        c = contribution(*e)
        if c: self.s[c[0]] += c[1]

st = StreamState()
for e in events: st.on_event(e)
print("after fix, batch == stream:", run_batch_shared(events) == dict(st.s))
print("values:", dict(sorted(st.s.items())))
```

**Output (my run):** (python3 -I, pure Python)
```
key               batch  stream  agree
('u1', '2025-03-01')          100.0  150.0  False
('u1', '2025-03-02')           20.0    0.0  False
('u2', '2025-03-01')           70.0   70.0  True
('u3', '2025-03-02')           20.0   20.0  True
after fix, batch == stream: True
values: {('u1', '2025-03-01'): 100.0, ('u1', '2025-03-02'): 20.0, ('u2', '2025-03-01'): 70.0, ('u3', '2025-03-02'): 20.0}
```

**Follow-ups:**
- *What else tends to differ?* Time zone, late-data rules, rounding, null defaults, deduplication, and the join key.
- *How do you detect drift between the two paths?* Compare batch and online values on a sample, and alert on mismatch (Part 8 covers monitoring).
- *Can Kappa do a backfill?* Yes if the retained log or an archived copy covers the period; otherwise load history from the lake into the same code path.

**Common mistakes:**
- Treating "same logic" as true because the specs read the same.
- Assuming Kafka retains everything forever.
- Merging batch and speed results without a clear cut-over time.
- Testing only the happy path (the null and refund rows are where they disagreed).

### Q26 ⭐⭐ 🟡 Change data capture (CDC) as a feature source. Compare log-based CDC (Debezium style) with query-based polling and dual writes, and explain snapshot plus stream, update and delete events (before and after images, tombstones), ordering and out-of-order events, and schema changes. Simulate a stream of insert, update and delete change events, apply them to a latest-state table and to a history table in pure Python, and show how a delete or an out-of-order update breaks a naive consumer. No Debezium or database was run.
**Asked at:** CDC and data-contract sources (risingwave.com and oneuptime.com Debezium schema-evolution posts, a decodable.co CDC schema-evolution post, a Confluent Current 2024 session 'Data contracts in practice with Debezium and Apache Flink', a sessionize.com talk on data contracts for AI pipelines, a Skroutz AWS Big Data blog post; search snippets only, not opened; one talk statistic about AI project failure was unsourced and not used); vendor and conference material; data engineer and platform roles | Kafka interview question banks (golinuxcloud, dev.to hiteshchawla 'Kafka interview questions for data engineer', datavidhya, DataCamp, Simplilearn, wecreateproblems, adaface, hyring, a techinterview.org post 'Kafka interview questions that separate users from operators', a hackmd Kafka MCQ set; search snippets only, not opened); editorial question lists, not verified candidate reports; data engineer, ML platform and backend roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** Log-based CDC reads the database's commit log and emits ordered insert, update and delete events with before and after images, so it catches deletes and every change without load on the tables, unlike polling or dual writes, but the consumer must handle ordering, deletes and schema changes.

**Then explain:**
- **Log-based (Debezium style).** Reads the write-ahead or binary log. Events carry an operation (`c` create, `u` update, `d` delete, `r` snapshot read), `before` and `after` images, and a source position such as an LSN. Low impact on the source, sees deletes and intermediate updates. Before images may need database settings (for example full replica identity in Postgres; check current docs).
- **Query-based polling.** `SELECT ... WHERE updated_at > last`. Easy, but misses deletes and intermediate states, needs an indexed timestamp, and clock and transaction timing can skip rows.
- **Dual writes.** The app writes to the DB and to Kafka. Two writes cannot be made atomic, so they diverge on failures. The outbox pattern fixes this.
- **Snapshot plus stream.** Take a consistent snapshot first (events marked `r`), then continue from the log position recorded at the snapshot start.
- **Deletes.** A delete event has `before` but a null `after`. In Kafka a tombstone (null value) usually follows so log compaction can drop the key (Debezium default; check current docs). A consumer that only handles `after` crashes or keeps the row.
- **Ordering.** Events for one key are ordered when partitioned by primary key. Across keys there is no global order. Guard with a version or LSN: apply only if newer than what you hold, and keep the version even after a delete.
- **Schema change.** A rename looks like drop plus add. Compatible changes (add column) are fine; others need an expand and contract plan.
- **As a feature source.** Latest-state table feeds the online store. History table (valid from, valid to) feeds point-in-time training. Use commit time as the valid-from, not the time you processed the event, or you leak or misdate.

**Example:** customers 1, 2, 3. Events 1 to 8 in commit order. They arrive as 1, 2, 4, 5, 3, 7, 6, 8: update 5 before update 3, and the delete (7) before an earlier update (6). The truth is `{1: platinum, 3: gold}`. The naive consumer gives `{1: gold, 3: gold, 2: gold}`: customer 1 is stuck on the older value and the deleted customer 2 is back. The LSN-guarded consumer matches the truth and is unchanged by replaying the stream twice.

**Code:**
```python
# EMULATION of Debezium-style change events. No Debezium, database or Kafka was run.
import json
def ev(lsn, op, key, before, after):
    return {"lsn": lsn, "op": op, "key": key, "before": before, "after": after}

# Source table customers(id PK, tier). Events in COMMIT order (lsn). 'r' = snapshot read.
truth_log = [
    ev(1, "r", 1, None, {"id": 1, "tier": "silver"}),      # initial snapshot
    ev(2, "r", 2, None, {"id": 2, "tier": "silver"}),
    ev(3, "u", 1, {"id": 1, "tier": "silver"}, {"id": 1, "tier": "gold"}),
    ev(4, "c", 3, None, {"id": 3, "tier": "silver"}),
    ev(5, "u", 1, {"id": 1, "tier": "gold"}, {"id": 1, "tier": "platinum"}),
    ev(6, "u", 2, {"id": 2, "tier": "silver"}, {"id": 2, "tier": "gold"}),
    ev(7, "d", 2, {"id": 2, "tier": "gold"}, None),        # delete (a tombstone message follows in Kafka)
    ev(8, "u", 3, {"id": 3, "tier": "silver"}, {"id": 3, "tier": "gold"}),
]
# What actually arrives: lsn 5 before lsn 3 (retry or two partitions), and the delete (7) before the update (6).
arrival = [truth_log[i] for i in (0, 1, 3, 4, 2, 6, 5, 7)]
print("arrival lsn order:", [e["lsn"] for e in arrival])

def naive(events, handle_deletes=True):
    state = {}
    for e in events:                                # arrival order, no version check
        if e["op"] in ("r", "c", "u"): state[e["key"]] = e["after"]["tier"]
        elif handle_deletes: state.pop(e["key"], None)
    return state

def correct(events):
    state, last_lsn, history = {}, {}, []
    for e in events:
        k = e["key"]
        if e["lsn"] <= last_lsn.get(k, -1): continue         # stale / duplicate for this key: drop it
        last_lsn[k] = e["lsn"]                                # keep lsn even after a delete (tombstone for ordering)
        if e["op"] == "d":
            state.pop(k, None)
        else:
            state[k] = e["after"]["tier"]
        history.append((k, e["lsn"], e["op"], e["after"]["tier"] if e["after"] else None))
    return state, history

def truth(events): return correct(sorted(events, key=lambda e: e["lsn"]))[0]

print("source truth    :", truth(truth_log))
print("naive, no deletes:", naive(arrival, False), "<- deleted customer 2 stays; 1 stuck on 'gold'")
print("naive, arrival   :", naive(arrival), "<- 1 stuck on 'gold'; deleted customer 2 is back (update after delete)")
st, hist = correct(arrival)
print("lsn-guarded     :", st)

# History table (SCD2-style): close the previous row when a newer version arrives.
def scd2(events):
    rows = {}   # key -> list of [tier, valid_from_lsn, valid_to_lsn]
    for e in sorted(events, key=lambda e: e["lsn"]):          # a real job orders by (key, lsn) per partition
        k = e["key"]; r = rows.setdefault(k, [])
        if r and r[-1][2] is None: r[-1][2] = e["lsn"]
        if e["op"] != "d": r.append([e["after"]["tier"], e["lsn"], None])
    return rows
for k, r in sorted(scd2(truth_log).items()): print("history", k, r)
# guard check for duplicates: replay the whole arrival stream twice, result must not change
print("idempotent under replay:", correct(arrival + arrival)[0] == st)
print("matches truth:", st == truth(truth_log))
```

**Output (my run):** (pure-Python EMULATION of change events; no Debezium, database or Kafka was run)
```
arrival lsn order: [1, 2, 4, 5, 3, 7, 6, 8]
source truth    : {1: 'platinum', 3: 'gold'}
naive, no deletes: {1: 'gold', 2: 'gold', 3: 'gold'} <- deleted customer 2 stays; 1 stuck on 'gold'
naive, arrival   : {1: 'gold', 3: 'gold', 2: 'gold'} <- 1 stuck on 'gold'; deleted customer 2 is back (update after delete)
lsn-guarded     : {1: 'platinum', 3: 'gold'}
history 1 [['silver', 1, 3], ['gold', 3, 5], ['platinum', 5, None]]
history 2 [['silver', 2, 6], ['gold', 6, 7]]
history 3 [['silver', 4, 8], ['gold', 8, None]]
idempotent under replay: True
matches truth: True
```

**Follow-ups:**
- *How do you handle a replay or duplicate?* Make the apply idempotent with the version guard (shown: replaying everything twice gives the same state).
- *Why keep the version after a delete?* Otherwise a late older update looks newer than "nothing" and resurrects the row. Real systems keep a tombstone or a soft-delete marker for a retention period.
- *What if the table has no primary key?* Debezium-style pipelines need a usable key (or a configured one) for ordering and compaction.

**Common mistakes:**
- Ignoring deletes.
- Last-write-wins by arrival time.
- Using processing time as the history validity time.
- Forgetting the snapshot-to-stream hand-off position.
- Treating a rename as the same column.

### Q27 ⭐⭐ 🟡 Real-time feature serving and the latency budget. A model endpoint has a 50 ms budget and needs 40 features across 3 entities: how do you design lookups (batch gets, one key per entity, co-located features), where do caches and defaults help, how do missing features and timeouts degrade, and what do hot keys do? Part 6 owns the serving endpoint itself. Use a local Feast SQLite online store to time single versus batched lookups, report sandbox-only numbers with caveats, and compute a simple latency budget table in Python.
**Asked at:** Feature-store product docs and write-ups (Feast docs on point-in-time joins and materialize and materialize-incremental, old v0.14 and v0.16 branches; an oneuptime.com Feast late-rows post; AWS SageMaker Unified Studio feature-group docs on online and offline stores and TTL; Databricks materialized-features docs; geeksforgeeks online vs offline store page; search snippets only, not opened); vendor docs and blogs, not interview reports; MLOps and ML platform roles; Feast 0.67.0 was also run locally in this sandbox | Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs
**Say this first (1 line):** Make the fetch one batched round trip per request (all 40 features for the 3 entities together), keep keys and features co-located, have defaults and a timeout with a fallback, cache hot keys, and agree a per-step latency budget up front.

**Then explain:**
- **Round trips are the cost.** In my local run, 40 calls of one feature each took about 6 ms; one call with all 40 features took well under 1 ms. A remote store would make each round trip a network hop, so the gap grows. Rule: one multi-get per store, not one call per feature or per entity.
- **Co-locate.** Group features that are read together into one feature view or hash per entity, so one key returns many values. Use a few entities, not 40 keys.
- **Batch requests.** Scoring many rows: one call for 50 rows was about 9 ms versus about 29 ms for 50 separate calls here (sandbox-only).
- **Missing and slow.** Missing entity returns `None`: fill a default and add a `*_missing` flag so the model can tell. Set a timeout per lookup (for example a fraction of the budget) and degrade: use defaults, a cached value or a simpler model. Count degraded requests.
- **Hot keys.** One popular merchant or device gets most of the traffic and overloads one shard or key. Use a short local cache, replicate hot keys, or pre-aggregate. In the demo a 50-entry LRU gave a 74% hit rate on skewed traffic (the skew is an assumption).
- **Budget.** Write down every step and make the sum fit with slack. Check tail latency (p99), not only the median.

**Example (budget):** 50 ms total: network 8, parsing 3, feature fetch 15, model 16, slack for tail 8 = 50. If the store needs 3 sequential round trips at an assumed 4 ms each that is 12 ms, versus 4 ms batched (assumed numbers, not measurements).

**Code:**
```python
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
```

**Output (my run):** (Feast 0.67.0, local provider, SQLite online store in its own temp repo, pandas 2.3.3; in-process, no network, timings sandbox-only and not a production estimate)
```
feast 0.67.0 pandas 2.3.3
Materializing 3 feature views from 2026-10-25 17:43:08+00:00 to 2026-10-26 17:43:08+00:00 into the sqlite online store.

user_feats:
merchant_feats:
device_feats:
features requested: 40 over 3 entities
check: values returned = 40 of 40
pattern                                                    median_ms  p90_ms   (sandbox only)
A 40 calls, 1 feature each, 1 request                           6.1      7.4
B 3 calls, one per entity, 1 request                            0.6      0.7
C 1 call, 40 features, 1 request                                0.4      0.5
D1 1 call, 40 features, 50 requests                             8.8     11.2
D2 50 calls of C (50 requests)                                 29.1     29.1
unknown merchant -> {'merchant_id': [99999], 'device_id': [3], 'user_f0': [0.6470673084259033], 'user_f1': [0.8951604962348938], 'merchant_f0': [None]}
with default + missing flag: 0.0 | merchant_missing = True
hot-key demo: 3000 requests, LRU cache of 50 merchants, hit rate = 74% (traffic skew is an assumption)

budget (ms)                                            allotted
network in+out                                           8
request parsing + validation                             3
feature fetch (all 3 entities, one batched call)        15
model inference                                         16
slack for tail / GC                                      8
sum                                                     50  (budget 50 ms, sum matches: True; slack row is the headroom)
measured in-process lookup C (median) = 0.4 ms vs allotted 15 ms (no network; a remote store adds a round trip per call)
ASSUMED remote store, 3 sequential round trips of 4 ms each: 12 ms vs one batched trip: 4 ms
```

**Follow-ups:**
- *Is SQLite representative?* No. Redis, DynamoDB or a managed store have network hops, replication and tails. Only the call-pattern lesson transfers.
- *What if features are too slow to compute online?* Precompute them (batch or stream) and only look them up, or drop the feature.
- *Where does the endpoint itself live?* Part 6 owns serving. This answer is about the feature fetch inside it.

**Common mistakes:**
- One call per feature.
- Quoting the median only.
- No default for a missing entity (the model sees NaN).
- No timeout, so one slow store call breaks the whole SLO.
- Benchmarking on localhost and promising that latency in production.

### Q28 ⭐⭐ 🔴 Flink versus Spark Structured Streaming versus Kafka Streams at concept level: processing model (record at a time versus micro-batch), state and checkpoints, event-time support, latency, exactly-once mechanism, deployment and operational weight, and when you would pick each for a feature pipeline. Run a local Spark Structured Streaming query with a checkpoint location, stop it, add data, restart, and show it resumes without reprocessing. Flink and Kafka Streams were not run, so label them not executed.
**Asked at:** Engine comparison pages (estuary.dev Spark vs Flink, conduktor.io, Onehouse 'Spark Structured Streaming vs Flink vs Kafka Streams', Confluent compare page, a DZone streaming article; search snippets only, not opened; one old Cal Poly page claiming Spark Streaming lacks exactly-once was treated as outdated); vendor blogs, partly competing claims; streaming and data platform roles | Stream-processing concept sources (Databricks 2017 blog 'Event-time aggregation and watermarking in Apache Spark Structured Streaming', Databricks watermarking deep dive, a codecentric.de Spark and Flink event-time post, an oneuptime late-data post, datadriven.io streaming system design questions; search snippets only, not opened); vendor and practitioner blogs, not interview reports; data engineer and streaming roles | Kafka exactly-once and idempotency sources (a levelup.gitconnected idempotent-producer post, a LinkedIn post on duplicate payments using idempotent producer plus idempotency key plus transactions, a Scribd outbox-pattern note, Onehouse and Confluent comparison pages stating Flink uses checkpoints and two-phase commit and Kafka uses transactions with read_committed; search snippets only, not opened; the official Apache Kafka docs were not opened); community posts and vendor pages, not interview reports; data engineer and platform roles
**Say this first (1 line):** Flink and Kafka Streams process one record at a time, Spark Structured Streaming processes small micro-batches, and all three get fault tolerance from checkpointed state, so I pick by team skills, latency need and where the data already lives, not by a slogan.

**Then explain:**
- Processing model. Flink: record at a time, long-running operators with keyed state. Kafka Streams: record at a time, a library inside your own JVM app, Kafka is the only input and output. Spark: micro-batches (a batch every trigger), and a continuous mode exists but check current docs for its limits.
- State and checkpoints. Flink takes periodic distributed snapshots of operator state. Kafka Streams keeps state in local stores (RocksDB) backed by a changelog topic in Kafka. Spark writes offsets and state to a checkpoint directory per batch. Delete or change the checkpoint and the job forgets where it was.
- Event time. All three support event-time windows and watermarks. The idea is the same: a watermark is roughly "max event time seen minus allowed lateness", and state for windows older than it is dropped. Events later than the watermark are dropped or sent to a side output, depending on engine and settings.
- Exactly-once. Flink: checkpoints plus two-phase commit sinks. Kafka Streams: Kafka transactions, read_committed on the consumer side. Spark: replayable source plus checkpointed offsets plus an idempotent or transactional sink. Each stops at the edge of its own system; an external sink (HTTP call, Redis) needs an idempotent write (see Q32).
- Latency and weight. Record at a time can reach lower latency than micro-batch, but I would not quote numbers; measure with your own data. Spark is the heaviest to run only if you do not already have Spark. Kafka Streams has no cluster to run, but scaling is tied to topic partitions. Flink needs its own cluster or a managed service.
- For a feature pipeline I would pick: Spark if the team already runs Spark or Databricks and a minute of delay is fine (and I can reuse the batch code for backfills); Flink if I need very fresh, stateful per-key features such as fraud velocity; Kafka Streams for small, Kafka-in Kafka-out enrichments owned by a service team.
- Failure modes: checkpoint dir lost or edited incompatibly (job restarts from scratch or fails on state schema change); watermark too tight (late data silently dropped); watermark too loose (state grows); using a non-idempotent sink with at-least-once replay; rebalances in Kafka Streams causing state restores.

| | Spark Structured Streaming | Flink | Kafka Streams |
|---|---|---|---|
| Model | micro-batch | record at a time | record at a time |
| Runs as | Spark app on cluster | Flink cluster or managed | library in your service |
| State | checkpoint dir (HDFS/object store/local) | snapshots to durable storage | local store plus Kafka changelog |
| Exactly-once mechanism | checkpoint + replayable source + idempotent sink | checkpoint + two-phase commit sink | Kafka transactions |
| Executed here | yes (local[2]) | not executed | not executed |

**Example:** File f1 holds users a, a, b. Run 1 gives counts a=2, b=1 as batch 0. I stop the query, drop file f2 with a, c and start again with the same checkpoint. It must read only f2: batch 1 shows a=3 (2 from restored state plus 1) and c=1, and f1 is not read again. A third start with no new files does nothing. If I delete the checkpoint, everything is read again and I get a=3, b=1, c=1 as batch 0.

**Code:**
```python
"""Q28: Spark Structured Streaming resumes from a checkpoint. Run: python q28_resume.py <workdir>"""
import json, os, sys, shutil
from pyspark.sql import SparkSession, functions as F

work = sys.argv[1]
for d in ("in", "ckpt", "out", "warehouse", "local"):
    shutil.rmtree(f"{work}/{d}", ignore_errors=True)
os.makedirs(f"{work}/in")

spark = (SparkSession.builder.master("local[2]").appName("q28")
         .config("spark.ui.enabled", "false")
         .config("spark.sql.shuffle.partitions", "2")
         .config("spark.sql.warehouse.dir", f"{work}/warehouse")
         .config("spark.local.dir", f"{work}/local")
         .getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

def drop_file(name, rows):
    with open(f"{work}/in/{name}.json", "w") as f:
        for k, v in rows:
            f.write(json.dumps({"user": k, "amount": v}) + "\n")

def process_batch(df, batch_id):
    # runs once per micro-batch; prints what THIS batch saw and the running state
    rows = sorted((r["user"], r["count"]) for r in df.collect())
    print(f"  batch_id={batch_id} updated running counts: {rows}")

def run_once(label):
    print(f"--- {label}")
    stream = (spark.readStream.schema("user string, amount int").json(f"{work}/in")
              .groupBy("user").count())
    q = (stream.writeStream.outputMode("update").foreachBatch(process_batch)
         .option("checkpointLocation", f"{work}/ckpt")
         .trigger(availableNow=True).start())
    q.awaitTermination()
    print(f"  checkpoint offsets files: {sorted(x for x in os.listdir(work + "/ckpt/offsets") if not x.startswith("."))}")

drop_file("f1", [("a", 10), ("a", 20), ("b", 5)])
run_once("run 1: file f1 (a,a,b)")
drop_file("f2", [("a", 1), ("c", 7)])
run_once("run 2 after restart: file f2 added (a,c); f1 must NOT be re-read")
run_once("run 3 after restart: no new files")
shutil.rmtree(f"{work}/ckpt")
run_once("run 4: checkpoint deleted, so everything is read again from scratch")
spark.stop()
```
```bash
cd /tmp/claude-0/b9_q28_35 && /tmp/claude-0/b9p09/spark/bin/python -I q28_resume.py /tmp/claude-0/b9_q28_35/q28 2>/dev/null
```

**Output (my run):** pyspark 4.2.0, local[2], openjdk 21, Spark UI off, 2 shuffle partitions, own warehouse and local dir. "Stop" here is the query finishing under `availableNow=True`, which is a clean stop. I did not kill -9 the process mid-batch, so crash recovery of a half-written batch is explained, not shown. Flink and Kafka Streams: not executed (no cluster or broker here).
```text
--- run 1: file f1 (a,a,b)
  batch_id=0 updated running counts: [('a', 2), ('b', 1)]
  checkpoint offsets files: ['0']
--- run 2 after restart: file f2 added (a,c); f1 must NOT be re-read
  batch_id=1 updated running counts: [('a', 3), ('c', 1)]
  checkpoint offsets files: ['0', '1']
--- run 3 after restart: no new files
  checkpoint offsets files: ['0', '1']
--- run 4: checkpoint deleted, so everything is read again from scratch
  batch_id=0 updated running counts: [('a', 3), ('b', 1), ('c', 1)]
  checkpoint offsets files: ['0']
```

**Follow-ups:**
- *Why did the count become 3 and not 1?* State for the running count lives in the checkpoint, so it was restored on restart.
- *Which engine for a 5-minute freshness feature?* Spark is enough, and I get the same code for backfill. Below seconds, look at Flink.
- *Can I change the query and keep the checkpoint?* Only some changes are safe (filters, sink options); changing stateful operators or schema usually needs a new checkpoint and a replay. Check current docs.

**Common mistakes:**
- Saying "Spark is not real streaming and has no exactly-once". That was an old claim; micro-batch with checkpoint and an idempotent sink gives exactly-once effects.
- Saying "Flink is always better". It is more to operate.
- Putting the checkpoint on local disk of a cluster that restarts.
- Reusing a checkpoint path for a different query.
- Quoting latency numbers from vendor blogs.

---

### Q29 ⭐ 🟡 Data contracts for ML feature pipelines. What goes into a contract (schema, types, semantics and units, nullability, freshness, volume, owner, change policy), who owns it (producer team) and where it is enforced (at produce time, in CI, at ingestion). Write a contract as YAML, validate sample records against it with pyyaml and pydantic, show an additive change passing and a breaking change failing, and explain how this differs from Part 8 monitoring, which only notices after the fact.
**Asked at:** CDC and data-contract sources (risingwave.com and oneuptime.com Debezium schema-evolution posts, a decodable.co CDC schema-evolution post, a Confluent Current 2024 session 'Data contracts in practice with Debezium and Apache Flink', a sessionize.com talk on data contracts for AI pipelines, a Skroutz AWS Big Data blog post; search snippets only, not opened; one talk statistic about AI project failure was unsourced and not used); vendor and conference material; data engineer and platform roles | Kafka interview question banks (golinuxcloud, dev.to hiteshchawla 'Kafka interview questions for data engineer', datavidhya, DataCamp, Simplilearn, wecreateproblems, adaface, hyring, a techinterview.org post 'Kafka interview questions that separate users from operators', a hackmd Kafka MCQ set; search snippets only, not opened); editorial question lists, not verified candidate reports; data engineer, ML platform and backend roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** A data contract is a written, versioned promise from the producer team about schema, meaning, freshness and change rules, enforced in code at the producer, in CI and at ingestion, so bad data is stopped, not just noticed later.

**Then explain:**
- What goes in. Field names and types, nullability, units and meaning (rupees, not paise), allowed values, ranges, freshness limit, expected volume, owner, consumers, and a change policy (additive only within a major version).
- Who owns it. The producer team, because they control the source. Consumers can propose, but a contract the producer does not own is just documentation.
- Where it is enforced. (1) Produce time: serializer or schema check before the record leaves. (2) CI: a compatibility check that fails a pull request that removes or retypes a field. (3) Ingestion: validate or quarantine bad records, so the feature pipeline never sees them.
- Compatible versus breaking. Adding a nullable field is compatible. Removing, renaming (looks like drop plus add), retyping, making a field nullable that consumers assumed non-null, shrinking allowed values, or adding a required field without default is breaking. Rollout path for a real break: add the new field, let consumers move, then remove (expand, adapt, contract) under a new major version.
- Versus Part 8 monitoring. Monitoring watches the data after it arrived and tells you something drifted. A contract fails before the bad data lands. You need both: the contract cannot catch a legal but shifted distribution.
- Failure modes: contract and real data drift apart because nobody enforces it; a strict "extra fields forbidden" check on the consumer side breaks on harmless additive changes (I use forbid only on the producer check; consumers should ignore unknown fields); semantic changes (units) pass a type check, so keep range checks and a changelog.

**Example:** Producer changes `amount_inr` to `amount_paise` (int). Type check alone would pass for ints. The contract diff flags "removed or renamed field amount_inr" and "new required field without default", so CI fails. Adding `merchant_category` (nullable) passes.

**Code:**
```yaml
contract: txn_events
version: 1.2.0
owner: payments-platform-team      # producer team owns it
consumers: [fraud-features, risk-reporting]
freshness_max_minutes: 15
expected_rows_per_hour: {min: 1000, max: 500000}
change_policy: additive-only-within-major   # removals/renames/type changes need a new major version
fields:
  - {name: txn_id,     type: string,   nullable: false, doc: "unique id"}
  - {name: user_id,    type: string,   nullable: false}
  - {name: amount_inr, type: float,    nullable: false, unit: INR, min: 0.01, doc: "rupees, not paise"}
  - {name: event_time, type: datetime, nullable: false, doc: "UTC, when it happened"}
  - {name: channel,    type: string,   nullable: false, allowed: [UPI, CARD, NETBANKING]}
  - {name: device_id,  type: string,   nullable: true}
```
```python
"""Q29: validate records and contract changes. Run: python3 -I q29_check.py q29_contract.yaml"""
import sys, copy, yaml
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ValidationError, create_model, Field

PYTYPE = {"string": str, "float": float, "int": int, "datetime": datetime}

def load(path):
    with open(path) as f:
        return yaml.safe_load(f)

def model_from(contract):
    """Build a pydantic model straight from the YAML so there is ONE source of truth."""
    fields = {}
    for f in contract["fields"]:
        t = PYTYPE[f["type"]]
        if "allowed" in f:
            t = Literal[tuple(f["allowed"])]
        kw = {}
        if "min" in f:
            kw["ge"] = f["min"]
        if f["nullable"]:
            fields[f["name"]] = (t | None, Field(None, **kw))
        else:
            fields[f["name"]] = (t, Field(..., **kw))
    return create_model(contract["contract"], __config__={"extra": "forbid"}, **fields)

def check_change(old, new):
    """Return a list of breaking-change reasons (empty list = compatible)."""
    problems = []
    o = {f["name"]: f for f in old["fields"]}
    n = {f["name"]: f for f in new["fields"]}
    for name, f in o.items():
        if name not in n:
            problems.append(f"removed or renamed field '{name}'")
            continue
        if n[name]["type"] != f["type"]:
            problems.append(f"type of '{name}' changed {f['type']} -> {n[name]['type']}")
        if f["nullable"] is False and n[name]["nullable"] is True:
            problems.append(f"'{name}' became nullable (consumers assumed non-null)")
        if "allowed" in f and not set(f["allowed"]) <= set(n[name].get("allowed", f["allowed"])):
            problems.append(f"'{name}' allowed values shrank")
    for name, f in n.items():
        if name not in o and f["nullable"] is False and "default" not in f:
            problems.append(f"new required field '{name}' without default")
    return problems

if __name__ == "__main__":
    c = load(sys.argv[1])
    M = model_from(c)
    good = {"txn_id": "t1", "user_id": "u1", "amount_inr": 499.0,
            "event_time": "2026-01-05T10:00:00", "channel": "UPI", "device_id": None}
    bad_records = {
        "amount in paise string": {**good, "amount_inr": "49900 paise"},
        "negative amount": {**good, "amount_inr": -5},
        "unknown channel": {**good, "channel": "WALLET"},
        "null user_id": {**good, "user_id": None},
        "extra field not in contract": {**good, "ip": "1.2.3.4"},
    }
    print("good record  ->", "PASS" if M(**good) else "?")
    for label, rec in bad_records.items():
        try:
            M(**rec); print(f"{label:28s} -> PASS (unexpected)")
        except ValidationError as e:
            errs = ", ".join(f"{'.'.join(map(str, x['loc']))}:{x['type']}" for x in e.errors())
            print(f"{label:28s} -> REJECT [{errs}]")

    additive = copy.deepcopy(c)
    additive["fields"].append({"name": "merchant_category", "type": "string", "nullable": True})
    print("\nchange A: add nullable field merchant_category ->", check_change(c, additive) or "COMPATIBLE")

    breaking = copy.deepcopy(c)
    breaking["fields"] = [f for f in breaking["fields"] if f["name"] != "amount_inr"]
    breaking["fields"].append({"name": "amount_paise", "type": "int", "nullable": False})
    print("change B: rename amount_inr -> amount_paise (int) ->")
    for p in check_change(c, breaking):
        print("   BREAKING:", p)
    sys.exit(0)
```
```bash
cd /tmp/claude-0/b9_q28_35 && python3 -I q29_check.py q29_contract.yaml
```

**Output (my run):** python3 3.13, PyYAML 6.0.1, pydantic 2.13.5. The pydantic model is built from the YAML, so there is one source of truth. Schema Registry server and Debezium: not executed; this is a plain-Python stand-in for the idea.
```text
good record  -> PASS
amount in paise string       -> REJECT [amount_inr:float_parsing]
negative amount              -> REJECT [amount_inr:greater_than_equal]
unknown channel              -> REJECT [channel:literal_error]
null user_id                 -> REJECT [user_id:string_type]
extra field not in contract  -> REJECT [ip:extra_forbidden]

change A: add nullable field merchant_category -> COMPATIBLE
change B: rename amount_inr -> amount_paise (int) ->
   BREAKING: removed or renamed field 'amount_inr'
   BREAKING: new required field 'amount_paise' without default
```

**Follow-ups:**
- *Contract versus Avro schema registry?* A registry checks structure and compatibility mode. A contract also holds meaning, freshness, owner and change policy. Use both.
- *What if the producer refuses to own it?* Start with a consumer-side ingestion check and quarantine, and escalate with the incident count it prevents.
- *Where do bad records go?* A dead-letter or quarantine table with the reason, and an alert to the owner.

**Common mistakes:**
- A YAML file nobody validates against.
- Only type checks, no units or ranges.
- No owner field.
- Treating a rename as harmless.
- Failing the whole stream on one bad record instead of quarantining it.

---

### Q30 ⭐ 🔴 Managed and open-source feature stores compared at concept level: Feast, Tecton, Hopsworks, SageMaker Feature Store, Vertex AI Feature Store and Databricks Feature Store. Compare where the offline and online stores live, who runs materialisation, streaming support, point-in-time and TTL handling, registry and governance, lock-in, and a build-versus-buy decision for a team of five. Only Feast ran locally; label every other product 'not executed' and say 'check current docs' for limits and names, which have changed over time.
**Asked at:** Feature-store product docs and write-ups (Feast docs on point-in-time joins and materialize and materialize-incremental, old v0.14 and v0.16 branches; an oneuptime.com Feast late-rows post; AWS SageMaker Unified Studio feature-group docs on online and offline stores and TTL; Databricks materialized-features docs; geeksforgeeks online vs offline store page; search snippets only, not opened); vendor docs and blogs, not interview reports; MLOps and ML platform roles; Feast 0.67.0 was also run locally in this sandbox | Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs
**Say this first (1 line):** All of these answer the same four questions (where offline lives, where online lives, who runs materialisation, who handles point-in-time and TTL); Feast gives you the pieces and you run them, managed products run more for you at the price of lock-in, and for five people I would start with the smallest thing that gives correct point-in-time data.

**Then explain:**
- Feast (open source). Offline store is pluggable (files, warehouse); online store is pluggable (SQLite for dev, a key-value store in production). You schedule materialisation yourself (cron or an orchestrator from Part 5). Point-in-time joins and TTL are built in (I ran both below). Registry is a file or SQL database. Streaming ingestion exists through push or stream-processing features; check current docs for what is stable.
- Tecton, Hopsworks: not executed. Vendor platforms that also run the transformations and materialisation, with streaming as a core feature. Hopsworks also has an open-source edition and its own online store; Tecton's ownership and packaging have changed over time. Check current docs and talk to the vendor for both.
- SageMaker Feature Store, Vertex AI Feature Store, Databricks Feature Store: not executed. Cloud-native. In general: offline copy in the cloud's own storage (S3 Parquet, BigQuery, Delta), online store managed by the cloud, TTL and access control through the cloud's own tools. Vertex and Databricks product names and architecture have been renamed or rebuilt more than once, so check current docs before quoting a limit.
- Build versus buy for five people. Ask: do I have real-time features with tight freshness? Do I have a platform engineer? Is my cloud already chosen? If everything is batch and one cloud, use the cloud's feature store or just a well-tested point-in-time join in a warehouse. If I need streaming and low-latency serving with no platform engineer, buy. Feast fits teams that want to own it and can afford the ops.
- Lock-in sits in three places: the feature definitions (DSL), the online store format, and the training-set API. Keep transformations in plain SQL or Python so they can move.
- Failure modes to ask about in any product: what happens to the online value when the TTL passes (None, as I saw), how late rows are handled, who pays for backfills, how you see which model used which feature version.

| Question | Feast | Tecton / Hopsworks | SageMaker / Vertex / Databricks |
|---|---|---|---|
| Offline store | your choice | platform-managed | cloud storage or warehouse |
| Online store | your choice | managed | managed |
| Materialisation | you schedule | platform runs it | partly managed |
| Streaming | via push/stream features, check docs | core feature | varies, check docs |
| Executed here | yes, Feast 0.67.0 | not executed | not executed |

**Example:** Feast run below. User 1 has values 3, 5, 9 on days Jan 1, 2, 4 and the view has a 3 day TTL. A request for user 1 at Jan 3 gets 5 (the Jan 4 value is in the future, ignored). A request for user 1 at Jan 10 gets no row at all: the newest value is 6 days old, older than the TTL, so it was dropped (2 rows back for 3 requested). Online after materialise: user 1 has 9, user 2 has 1, unknown user 99 has None.

**Code:**
```python
"""Q30: tiny local Feast run (file offline store + SQLite online store). Own repo dir passed as argv[1]."""
import sys, os, shutil, warnings
from datetime import datetime, timedelta
import pandas as pd
warnings.filterwarnings("ignore")

repo = sys.argv[1]
shutil.rmtree(repo, ignore_errors=True)
os.makedirs(repo + "/data")

with open(repo + "/feature_store.yaml", "w") as f:
    f.write(f"""project: q30demo
provider: local
registry: {repo}/data/registry.db
online_store:
  type: sqlite
  path: {repo}/data/online.db
offline_store:
  type: file
entity_key_serialization_version: 3
""")

pd.DataFrame({
    "user_id": [1, 1, 1, 2],
    "event_timestamp": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-04", "2026-01-01"], utc=True),
    "txn_count_7d": [3, 5, 9, 1],
}).to_parquet(repo + "/data/stats.parquet")

from feast import FeatureStore, Entity, FeatureView, Field, FileSource
from feast.types import Int64
from feast.value_type import ValueType

user = Entity(name="user", join_keys=["user_id"], value_type=ValueType.INT64)
src = FileSource(path=repo + "/data/stats.parquet", timestamp_field="event_timestamp")
fv = FeatureView(name="user_stats", entities=[user], ttl=timedelta(days=3),
                 schema=[Field(name="txn_count_7d", dtype=Int64)], source=src)

store = FeatureStore(repo_path=repo)
store.apply([user, fv])
print("registry has:", [v.name for v in store.list_feature_views()])

req = pd.DataFrame({"user_id": [1, 1, 2],
                    "event_timestamp": pd.to_datetime(["2026-01-03", "2026-01-10", "2026-01-02"], utc=True)})
hist = store.get_historical_features(entity_df=req, features=["user_stats:txn_count_7d"]).to_df()
print("historical (offline, as-of, ttl=3d):")
print(hist.sort_values(["user_id", "event_timestamp"]).to_string(index=False))

store.materialize(start_date=datetime(2025, 12, 1), end_date=datetime(2026, 1, 5))
online = store.get_online_features(features=["user_stats:txn_count_7d"],
                                   entity_rows=[{"user_id": 1}, {"user_id": 2}, {"user_id": 99}]).to_dict()
print("online (latest value materialised):", online)
```
```bash
cd /tmp/claude-0/b9_q28_35 && /tmp/claude-0/b9p09/feast/bin/python -I q30_feast_demo.py /tmp/claude-0/b9_q28_35/feast_repo
```

**Output (my run):** Feast 0.67.0, pandas 2.3.3, local provider, Parquet file offline source, SQLite online store, in a private repo directory (ANSI colour codes stripped, warnings filtered). Everything else in the table is not executed; claims about them come from docs I did not open in this run and need a check of current documentation.
```text
registry has: ['user_stats']
historical (offline, as-of, ttl=3d):
 user_id           event_timestamp  txn_count_7d
       1 2026-01-03 00:00:00+00:00             5
       2 2026-01-02 00:00:00+00:00             1
Materializing 1 feature views from 2025-12-01 00:00:00+00:00 to 2026-01-05 00:00:00+00:00 into the sqlite online store.

user_stats:
online (latest value materialised): {'user_id': [1, 2, 99], 'txn_count_7d': [9, 1, None]}
```

**Follow-ups:**
- *Do I need a feature store at all?* If you have one model, batch only, and one team, a tested as-of join in your warehouse may be enough. The store pays off when many models share features or you need online serving.
- *Why not just Redis?* Redis is only the online half. You still need the offline history, point-in-time joins and one definition for both.
- *What does materialise do?* Copies the latest value per entity from offline to online for a time window.

**Common mistakes:**
- Comparing products by vendor latency claims.
- Forgetting TTL and then silently losing training rows.
- Buying a platform for batch-only features.
- Letting the online and offline paths have two separate transformation codes.
- Quoting product limits from memory.

---

### Q31 ⭐ 🔴 Late-arriving data and corrections in a feature store. A transaction record arrives six hours late, or a source system corrects a value last week: what does a point-in-time training set built today show versus what the model saw in production at the time, what are event time, ingestion (knowledge) time and bitemporal tables, and how do you decide which to train on? Simulate a late row and a correction, build the as-of join on event time and on ingestion time, and show how the two training sets differ.
**Asked at:** Feature-store product docs and write-ups (Feast docs on point-in-time joins and materialize and materialize-incremental, old v0.14 and v0.16 branches; an oneuptime.com Feast late-rows post; AWS SageMaker Unified Studio feature-group docs on online and offline stores and TTL; Databricks materialized-features docs; geeksforgeeks online vs offline store page; search snippets only, not opened); vendor docs and blogs, not interview reports; MLOps and ML platform roles; Feast 0.67.0 was also run locally in this sandbox | Stream-processing concept sources (Databricks 2017 blog 'Event-time aggregation and watermarking in Apache Spark Structured Streaming', Databricks watermarking deep dive, a codecentric.de Spark and Flink event-time post, an oneuptime late-data post, datadriven.io streaming system design questions; search snippets only, not opened); vendor and practitioner blogs, not interview reports; data engineer and streaming roles | Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs
**Say this first (1 line):** A training set built today from event time shows what we now know, not what the model saw at prediction time, so for a faithful replay I also filter on ingestion time (the moment we learned the fact); I train on knowledge time when I want to match production and on corrected values when the correction is also what future serving will see.

**Then explain:**
- Event time is when it happened. Ingestion (knowledge) time is when our system received it. A bitemporal table keeps both, and keeps every version of a corrected fact instead of overwriting.
- Late row (6 hours late): a join on event time only will include it in a prediction made 1 hour after it happened, but production could not have had it. That is label leakage of a mild kind and a train/serve skew.
- Correction (last week): production served the old value; today's table has the new one. A set built on the newest version trains on a cleaner feature than the model will see live if corrections keep arriving late.
- How I decide. (a) Replay for evaluation or debugging: use event time plus ingest time at prediction time (what was known). (b) Training: usually the same, because the model must learn from inputs of the quality it will really get. (c) If the pipeline will soon read corrected data at serving (for example a delay you can wait for), train on the corrected one and wait the same delay at serving. (d) Labels may use fully corrected data, because the outcome truth is allowed to be late.
- Costs: you need ingest_time on every row, append-only storage, and larger tables; the cheap approximation is to log the features that were served and train on those.
- Failure modes: overwriting corrections in place (history lost, cannot replay); using processing-time in one path and event-time in the other; late rows arriving after the materialise window so the online store never gets them (use overlapping windows, check current docs for your tool).

**Example (hand-check):** user 1 has value 100 at 10:00 (known 10:05) and 500 at 12:00 that arrived at 18:00. An ask at 13:00: event-time-only join gives 500, production served 100. User 2 has 10 at 09:00, corrected to 12 a week later: an ask on Jan 2 gets 12 from event-time-only and 10 from knowledge-time, production served 10.

**Code:**
```python
"""Q31: event-time vs ingestion-time as-of joins on a late row and a correction. No randomness."""
import pandas as pd

T = pd.Timestamp
# feature log: one row per (entity, event_time, ingest_time); value = last_txn_amount
log = pd.DataFrame([
    # user 1: normal row, then a row that happened at 12:00 but arrived 6 hours late (18:00)
    (1, T("2026-01-01 10:00"), T("2026-01-01 10:05"), 100),
    (1, T("2026-01-01 12:00"), T("2026-01-01 18:00"), 500),   # LATE ROW
    # user 2: row, then a correction of the SAME event, ingested a week later
    (2, T("2026-01-01 09:00"), T("2026-01-01 09:01"), 10),
    (2, T("2026-01-01 09:00"), T("2026-01-08 08:00"), 12),    # CORRECTION (new version)
], columns=["user", "event_time", "ingest_time", "value"])

# prediction moments (what the model was asked, and when)
asks = pd.DataFrame([
    (1, T("2026-01-01 13:00")),   # 1h after the late row happened, 5h before it arrived
    (1, T("2026-01-02 09:00")),   # next day: late row is known by now
    (2, T("2026-01-02 09:00")),   # before the correction was ingested
], columns=["user", "ask_time"])

def as_of(user, ask_time, use_ingest):
    r = log[(log.user == user) & (log.event_time <= ask_time)]
    if use_ingest:                       # only rows the system KNEW at ask_time
        r = r[r.ingest_time <= ask_time]
    if r.empty:
        return None
    # latest event wins; for same event the latest ingested version wins
    return r.sort_values(["event_time", "ingest_time"]).iloc[-1].value

out = asks.copy()
out["A_event_time_only(today)"] = [as_of(u, t, False) for u, t in zip(asks.user, asks.ask_time)]
out["B_event+ingest(knowledge)"] = [as_of(u, t, True) for u, t in zip(asks.user, asks.ask_time)]
def served_in_prod(user, ask_time):
    """Replay the online store: apply rows in arrival order, keep the newest event, read at ask_time."""
    store = {}
    for r in log.sort_values("ingest_time").itertuples():
        if r.ingest_time > ask_time:
            break
        if r.user not in store or r.event_time >= store[r.user][0]:
            store[r.user] = (r.event_time, r.value)
    return store[user][1]

out["served_in_prod"] = [served_in_prod(u, t) for u, t in zip(asks.user, asks.ask_time)]
out["A_leaks"] = out["A_event_time_only(today)"] != out["served_in_prod"]
out["B_matches_prod"] = out["B_event+ingest(knowledge)"] == out["served_in_prod"]
pd.set_option("display.width", 200)
print(out.to_string(index=False))
```
```bash
/tmp/claude-0/b9p09/misc/bin/python -I q31_bitemporal.py
```

**Output (my run):** pandas 3.1.0, Python 3.13, no randomness. "served_in_prod" comes from a separate replay of an emulated online store applying rows in arrival order, not from a hardcoded answer.
```text
 user            ask_time  A_event_time_only(today)  B_event+ingest(knowledge)  served_in_prod  A_leaks  B_matches_prod
    1 2026-01-01 13:00:00                       500                        100             100     True            True
    1 2026-01-02 09:00:00                       500                        500             500    False            True
    2 2026-01-02 09:00:00                        12                         10              10     True            True
```

**Follow-ups:**
- *Does Feast do this?* Its as-of join works on event timestamps; I would store ingest time as a feature or use a snapshot approach. Check current docs.
- *Cheapest fix?* Log served features and train on the logs.
- *When is the event-time-only set fine?* When late data and corrections are rare and small, and you have measured that.

**Common mistakes:**
- Overwriting a corrected value in place.
- Confusing event time with ingestion time.
- Thinking "point-in-time correct" alone covers late data. It does not unless ingest time is used.
- Using corrected labels and corrected features together, so the model never sees realistic noise.

---

### Q32 ⭐ 🔴 End-to-end exactly-once effects for a pipeline Kafka to stream job to online store. Walk each hop (producer, broker, job, sink), say where duplicates and gaps can appear, and design idempotent upserts with a version or event-time guard so a replay or a late event cannot overwrite a newer value. Simulate failures and replays in pure Python and show the online value ends correct with the guard and wrong without it. Real Kafka, Flink or Spark exactly-once sinks were not run.
**Asked at:** Kafka exactly-once and idempotency sources (a levelup.gitconnected idempotent-producer post, a LinkedIn post on duplicate payments using idempotent producer plus idempotency key plus transactions, a Scribd outbox-pattern note, Onehouse and Confluent comparison pages stating Flink uses checkpoints and two-phase commit and Kafka uses transactions with read_committed; search snippets only, not opened; the official Apache Kafka docs were not opened); community posts and vendor pages, not interview reports; data engineer and platform roles | Engine comparison pages (estuary.dev Spark vs Flink, conduktor.io, Onehouse 'Spark Structured Streaming vs Flink vs Kafka Streams', Confluent compare page, a DZone streaming article; search snippets only, not opened; one old Cal Poly page claiming Spark Streaming lacks exactly-once was treated as outdated); vendor blogs, partly competing claims; streaming and data platform roles | Stream-processing concept sources (Databricks 2017 blog 'Event-time aggregation and watermarking in Apache Spark Structured Streaming', Databricks watermarking deep dive, a codecentric.de Spark and Flink event-time post, an oneuptime late-data post, datadriven.io streaming system design questions; search snippets only, not opened); vendor and practitioner blogs, not interview reports; data engineer and streaming roles
**Say this first (1 line):** End-to-end I cannot get exactly-once delivery, but I can get exactly-once effects by making the final write idempotent, with a per-key version check so a duplicate, a replay or an old event cannot change a newer value.

**Then explain:**
- Producer: a lost ack makes the producer retry, so the same record can land twice at different offsets. An idempotent producer fixes duplicates inside Kafka; acks=0 or a crash before send can lose a record (a gap).
- Broker: replicated log is durable if replication and min in-sync replicas are set sensibly. Offsets are per partition, ordering holds only inside a partition, so key by entity.
- Job: reads, computes, writes, then commits the offset. Crash between write and commit means the batch is processed twice (at-least-once). Commit before write means loss. Transactions or checkpoints can tie them together inside Kafka or the engine, not across an external store.
- Sink: the online store sees the duplicates. Make it idempotent: the producer stamps a per-key sequence or event version; the sink applies a record only when it is newer (last-value features) or exactly the next one (counts); duplicates are skipped and gaps raise an alert.
- Operator actions are also writers: a rewind or a backfill job can overwrite new values with old ones unless the guard is on the sink.
- Failure modes: the guard needs a trustworthy version (event time can tie or be clock-skewed, so a producer sequence is better); the guard's own state must be updated atomically with the value (one conditional write); a guard that skips gaps silently hides loss.

**Example (hand-check idea):** u2 has 4 real events. The log has duplicates, the job crashes once before committing, someone rewinds to offset 3, and a backfill replays the oldest records last. Naive store: count 13 and last amount from an old record. Guarded store: count 4 and the last amount from seq 4.

**Code:**
```python
"""Q32: PURE-PYTHON EMULATION of a Kafka-like log -> consumer job -> online store.
Not real Kafka. Failure schedule is seeded, so the run is repeatable."""
import random

rng = random.Random(7)
USERS = ["u1", "u2", "u3"]

# --- intended truth: per-user sequence of events, seq starts at 1 and is assigned by the producer
truth_events = []
seq = {u: 0 for u in USERS}
for _ in range(12):
    u = rng.choice(USERS)
    seq[u] += 1
    truth_events.append({"user": u, "seq": seq[u], "amount": rng.randint(10, 99)})

# --- hop 1: producer. Retries after a lost ack append the SAME event twice (no idempotent producer).
log = []                          # the "partition": list index = offset
for e in truth_events:
    log.append(dict(e))
    if rng.random() < 0.25:       # ack lost, producer retries -> duplicate record at a new offset
        log.append(dict(e))
print(f"intended events={len(truth_events)}  records in log={len(log)} (duplicates from producer retry={len(log) - len(truth_events)})")

# --- expected final online values
exp = {}
for e in truth_events:
    d = exp.setdefault(e["user"], {"count": 0, "last_amount": None, "seq": 0})
    d["count"] += 1; d["last_amount"] = e["amount"]; d["seq"] = e["seq"]

# --- hop 3: consumer job with an "online store" sink.
class Naive:
    def __init__(self): self.s = {}
    def apply(self, e):
        d = self.s.setdefault(e["user"], {"count": 0, "last_amount": None, "seq": 0})
        d["count"] += 1                      # non-idempotent increment
        d["last_amount"] = e["amount"]       # blind overwrite
        d["seq"] = e["seq"]

class Guarded:
    """Upsert guard: only apply the next unseen version for a key (seq == stored+1)."""
    def __init__(self): self.s = {}; self.skipped = 0; self.gaps = 0
    def apply(self, e):
        d = self.s.setdefault(e["user"], {"count": 0, "last_amount": None, "seq": 0})
        if e["seq"] <= d["seq"]:
            self.skipped += 1; return        # duplicate or older replay: ignore
        if e["seq"] > d["seq"] + 1:
            self.gaps += 1; return           # a gap: do not apply out of order, raise an alert
        d["count"] += 1; d["last_amount"] = e["amount"]; d["seq"] = e["seq"]

def run_job(sink, crash_at, rewind_to):
    """Process in batches of 5; write sink first, commit offset after (at-least-once).
    crash_at: after writing this batch number, crash BEFORE committing offset -> batch replays.
    rewind_to: at the end an operator resets the consumer to this offset to 'reprocess'."""
    committed = 0
    crashed = False
    while committed < len(log):
        batch = log[committed:committed + 5]
        for e in batch:
            sink.apply(e)
        if not crashed and committed // 5 == crash_at:
            crashed = True               # crash between sink write and offset commit
            continue                     # restart: re-read from the same committed offset
        committed += len(batch)
    # operator rewinds offsets and reprocesses everything from rewind_to
    for e in log[rewind_to:]:
        sink.apply(e)
    # a slow backfill job finishes last and replays the OLDEST records into the same store
    for e in log[:3]:
        sink.apply(e)

for name, sink in (("NAIVE (blind increment + overwrite)", Naive()), ("GUARDED (seq guard)", Guarded())):
    run_job(sink, crash_at=1, rewind_to=3)
    ok = sink.s == exp
    print(f"\n{name}: final == expected? {ok}")
    for u in USERS:
        print(f"  {u}: got {sink.s.get(u)}  expected {exp.get(u)}")
    if isinstance(sink, Guarded):
        print(f"  guard skipped {sink.skipped} duplicate/old records, gaps seen={sink.gaps}")

# --- gap detection: a record is LOST (e.g. acks=0 on a real producer); guard must alert, not silently skip
lossy = [e for e in log if not (e["user"] == "u1" and e["seq"] == 2)]
g = Guarded()
for e in lossy:
    g.apply(e)
print(f"\nLOST-RECORD case (u1 seq 2 removed from log): gaps seen={g.gaps}, u1 stuck at seq={g.s['u1']['seq']} (alert instead of wrong value)")
```
```bash
python3 -I q32_exactly_once_sim.py
```

**Output (my run):** this is a pure-Python EMULATION of a log, a consumer and a store; no Kafka broker was available, so none of this is real Kafka output. Seeded, so the numbers repeat. Real Kafka transactions, Flink and Spark exactly-once sinks: not executed.
```text
intended events=12  records in log=17 (duplicates from producer retry=5)

NAIVE (blind increment + overwrite): final == expected? False
  u1: got {'count': 19, 'last_amount': 82, 'seq': 6}  expected {'count': 6, 'last_amount': 82, 'seq': 6}
  u2: got {'count': 13, 'last_amount': 93, 'seq': 2}  expected {'count': 4, 'last_amount': 18, 'seq': 4}
  u3: got {'count': 7, 'last_amount': 64, 'seq': 2}  expected {'count': 2, 'last_amount': 64, 'seq': 2}

GUARDED (seq guard): final == expected? True
  u1: got {'count': 6, 'last_amount': 82, 'seq': 6}  expected {'count': 6, 'last_amount': 82, 'seq': 6}
  u2: got {'count': 4, 'last_amount': 18, 'seq': 4}  expected {'count': 4, 'last_amount': 18, 'seq': 4}
  u3: got {'count': 2, 'last_amount': 64, 'seq': 2}  expected {'count': 2, 'last_amount': 64, 'seq': 2}
  guard skipped 27 duplicate/old records, gaps seen=0

LOST-RECORD case (u1 seq 2 removed from log): gaps seen=6, u1 stuck at seq=1 (alert instead of wrong value)
```

**Follow-ups:**
- *Why not Kafka transactions alone?* They cover Kafka to Kafka. A write to Redis or a database sits outside, so I still need an idempotent write or an outbox.
- *Why a sequence and not the offset?* Producer retries create duplicates with different offsets, so the offset cannot identify the event.
- *Can I use event time as the version?* For last-value features usually yes, with a tie-break; for counts I prefer a sequence or an event id set.

**Common mistakes:**
- Saying "we use Kafka so it is exactly-once".
- Blind increments on a replayable stream.
- Overwriting without comparing versions.
- Not testing replay and backfill.
- Silently dropping gaps.

---

### Q33 ⭐ 🔴 Testing a feature pipeline: unit tests on transformation logic, parity tests between the offline and online path, replay or backtest tests (feed a logged event stream through the streaming code and compare with the batch result), schema tests and freshness tests. Part 1 owns pytest basics and Part 8 owns production monitoring. Write a small pytest suite for a feature function with a replay test and a deliberately seeded bug, run it, and show which test catches the bug.
**Asked at:** Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs | Lambda and Kappa sources (datadriven.io pipeline architecture page, techinterview.org 'Lambda and Kappa Architecture for Big Data', Materialize 'Does Kappa architecture improve on Lambda', a Netflix talk PDF on backfilling streaming pipelines in Kappa architecture hosted on microsites.databricks.com, risingwave.com; search snippets only, not opened); vendor blogs and a conference talk; data platform roles; the feature-store mapping is an expert extension
**Say this first (1 line):** I test a feature pipeline in layers: unit tests for the logic and its edges, a parity test that online equals offline, a replay test that feeds a logged stream (including late events) through the streaming code and compares with a batch recompute, plus schema and freshness checks; and I show which layer catches which bug.

**Then explain:**
- Unit tests: tiny hand-checked cases, especially window edges (is the boundary included?) and empty users.
- Parity test: same inputs through the online path and the offline path must give the same number. This is the guard against train/serve skew.
- Replay or backtest test: take a logged stream in arrival order (with disorder), feed the streaming code, and after every event compare with a slow, obviously correct batch recompute over the events seen so far. It catches ordering and state bugs that sorted unit tests never hit.
- Schema tests (right fields, types, no empty keys) and freshness tests (latest event not older than the limit, with a fake clock) are cheap and catch pipeline plumbing issues. Part 1 owns pytest basics; Part 8 owns live monitoring, which finds problems only after deploy.
- Failure modes: random test data without a fixed seed (flaky), a test that uses the same code for expected and actual (proves nothing), replay data that is perfectly sorted so it never exercises late events.

**Example:** two seeded bugs. `boundary`: online keeps an event exactly one hour old. `unsorted`: online state assumes events arrive in order. In the run, the edge unit test catches the first and only the replay test catches the second; sorted parity and basic unit tests stay green for it.

**Code:**
```python
# ---- feature.py
"""Feature: number of events per user in the window (now - W, now]. Two code paths: batch and online."""
import os
from bisect import bisect_right, insort
from collections import defaultdict, deque

W = 3600  # seconds
BUG = os.environ.get("FEATURE_BUG", "none")   # "none" | "boundary" | "unsorted"  (seeded bugs for the demo)

def batch_count(events, user, now):
    """Offline path: recompute from the raw log. Slow but obviously right. Oracle for tests."""
    return sum(1 for e in events if e["user"] == user and now - W < e["ts"] <= now)

class OnlineCounter:
    """Online path: incremental state per user."""
    def __init__(self):
        self.ts = defaultdict(list) if BUG != "unsorted" else defaultdict(deque)

    def update(self, e):
        if BUG == "unsorted":
            self.ts[e["user"]].append(e["ts"])      # assumes events arrive in time order
        else:
            insort(self.ts[e["user"]], e["ts"])     # tolerates out-of-order arrival

    def get(self, user, now):
        if BUG == "unsorted":
            d = self.ts[user]
            while d and d[0] <= now - W:            # evict from the left, assumes sorted
                d.popleft()
            return sum(1 for t in d if t <= now)
        lst = self.ts[user]
        lo = bisect_right(lst, now - W - (1 if BUG == "boundary" else 0))   # boundary bug: keeps t == now-W
        hi = bisect_right(lst, now)
        return hi - lo

REQUIRED = {"user": str, "ts": int, "amount": float}

def schema_errors(e):
    errs = [f"missing {k}" for k in REQUIRED if k not in e]
    errs += [f"bad type {k}" for k, t in REQUIRED.items() if k in e and not isinstance(e[k], t)]
    if isinstance(e.get("user"), str) and not e["user"]:
        errs.append("empty user")
    return errs

def freshness_ok(last_event_ts, now, max_lag=900):
    return now - last_event_ts <= max_lag

# ---- test_feature.py
import random
import pytest
from feature import W, OnlineCounter, batch_count, schema_errors, freshness_ok

def make_events(n, seed, disorder):
    rng = random.Random(seed)
    evs = [{"user": rng.choice(["a", "b", "c"]), "ts": 10_000 + i * 97 + rng.randint(0, 60), "amount": float(rng.randint(1, 500))}
           for i in range(n)]
    if disorder:   # arrival order differs from event-time order (late events)
        for i in range(0, n - 5, 5):
            evs[i], evs[i + 3] = evs[i + 3], evs[i]
    return evs

def test_unit_basic_count():
    c = OnlineCounter()
    for t in (100, 200, 300):
        c.update({"user": "a", "ts": t, "amount": 1.0})
    assert c.get("a", 300) == 3
    assert c.get("b", 300) == 0

def test_unit_window_edge_is_exclusive():
    c = OnlineCounter()
    c.update({"user": "a", "ts": 0, "amount": 1.0})
    c.update({"user": "a", "ts": 10, "amount": 1.0})
    assert c.get("a", W - 1) == 2      # time only moves forward when we query
    assert c.get("a", W) == 1          # ts=0 is exactly W old, window is (now-W, now]

def test_parity_sorted_stream():
    evs = sorted(make_events(120, 1, disorder=False), key=lambda e: e["ts"])
    c = OnlineCounter()
    for e in evs:
        c.update(e)
    for now in range(10_000, 25_000, 411):
        for u in "abc":
            assert c.get(u, now) == batch_count(evs, u, now)

def test_replay_disordered_log_matches_batch_after_every_event():
    log = make_events(120, 2, disorder=True)     # the logged stream, in ARRIVAL order
    c, seen = OnlineCounter(), []
    for e in log:
        c.update(e); seen.append(e)
        now = max(x["ts"] for x in seen)
        for u in "abc":
            assert c.get(u, now) == batch_count(seen, u, now), (u, now)

def test_schema_rejects_bad_records():
    assert schema_errors({"user": "a", "ts": 1, "amount": 2.0}) == []
    assert schema_errors({"user": "", "ts": "1", "amount": 2.0}) == ["bad type ts", "empty user"]
    assert "missing amount" in schema_errors({"user": "a", "ts": 1})

@pytest.mark.parametrize("last,now,ok", [(1000, 1500, True), (1000, 1900, True), (1000, 1901, False)])
def test_freshness(last, now, ok):
    assert freshness_ok(last, now) is ok
```
```bash
cd q33
for b in none boundary unsorted; do
  echo "=== FEATURE_BUG=$b"
  FEATURE_BUG=$b python3 -I -m pytest -q -p no:cacheprovider --rootdir=. -o pythonpath=. test_feature.py
done
```

**Output (my run):** pytest 9.1.1, Python 3.13 (output lines filtered to the summary, failing test names and the first assertion line).
```text
=== FEATURE_BUG=none
8 passed in 0.19s
=== FEATURE_BUG=boundary
E       AssertionError: assert 2 == 1
FAILED test_feature.py::test_unit_window_edge_is_exclusive - AssertionError: ...
1 failed, 7 passed in 0.15s
=== FEATURE_BUG=unsorted
E               AssertionError: ('b', 13836)
FAILED test_feature.py::test_replay_disordered_log_matches_batch_after_every_event
1 failed, 7 passed in 0.16s
```

**Follow-ups:**
- *Where do I get the logged stream?* Log raw events at the broker or sink in production, keep a small anonymised sample in the repo.
- *Is parity enough?* No. Both paths can share the same wrong definition, so keep one oracle that is written for clarity.
- *Run in CI?* Yes, fast tests every pull request, bigger backtests nightly.

**Common mistakes:**
- Only testing happy paths with sorted data.
- Using the same function as oracle and subject.
- No seed on random data.
- Checking only the final value, not after each event.
- Calling monitoring a substitute for tests.

---

### Q34 ⭐ 🔴 Design question: real-time features for a card or UPI payment fraud model with a 100 ms decision budget, in an Indian bank or payments app or a global payments company. Cover event ingestion, velocity features (counts and sums per card, device, merchant over several windows), device and graph features, an online store, batch features, delayed chargeback labels, point-in-time training data, fallbacks when features are missing, and what to log. Give a one-page whiteboard answer, a feature-spec YAML validated with pyyaml, and a pure-Python simulation of velocity features; mark every real system as concept only.
**Asked at:** System-design write-ups (a techinterview.org 'System Design Interview: Fraud Detection System' post, a manishmazumder5 substack on real-time fraud ML, a PyData Amsterdam 2026 talk abstract on Kafka, Flink and a feature store for real-time inference, one Glassdoor ML Engineer interview entry whose snippet mentions designing a real-time anomaly detection pipeline with Kafka, PyTorch and Prometheus; search snippets only, not opened; one candidate review, unverified); anecdotal and editorial material, no company-verified question; ML engineer roles at fintech, payments and product companies | Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs | Kafka interview question banks (golinuxcloud, dev.to hiteshchawla 'Kafka interview questions for data engineer', datavidhya, DataCamp, Simplilearn, wecreateproblems, adaface, hyring, a techinterview.org post 'Kafka interview questions that separate users from operators', a hackmd Kafka MCQ set; search snippets only, not opened); editorial question lists, not verified candidate reports; data engineer, ML platform and backend roles at IT-services firms, product companies and GCCs
**Say this first (1 line):** For a 100 ms fraud decision I precompute velocity features in a stream job, read them with one fast key lookup per entity, add batch features that are refreshed daily, score a model plus rules, always have a fallback for missing features, and log everything that was served so the training set can be rebuilt as of the decision time.

**Then explain (whiteboard, concept only, none of these systems ran):**
- Ingest. Payment events go to a durable log (Kafka-like), keyed by card id so one card's events stay ordered. Stream job (Flink or Spark, concept) keeps rolling windows: counts and sums per card over 1 minute, 10 minutes, 1 hour; distinct cards per device; distinct merchants per card.
- Online store. Key-value store (Redis or similar, concept) with TTL a bit longer than the longest window. Fetch card, device, merchant keys in parallel. Budget (planning, not measured): gateway 10 ms, feature fetch 30, model 20, rules 10, slack 30.
- Batch features. Merchant chargeback rate, device graph risk scores, customer tenure: computed daily offline, pushed to the same online store. Graph features (shared devices, shared beneficiaries) are expensive, so batch them, and use a small stream counter for the live part.
- Labels. Chargebacks and disputes arrive weeks late. Train only on transactions older than the label delay, treat "no dispute yet" as unknown for recent rows, and keep late-label corrections (Q31).
- Training data. Point-in-time: features as of the decision time. Best: use the feature snapshot logged at decision time, backfill new features with an as-of join.
- Fallbacks. Store timeout or missing key: use spec default plus a missing-flag feature, never crash; if the model service is down, rules only; set a hard timeout on the whole call. Never default the amount sum to a harmless-looking 0 without the flag (see output).
- Log: request id, card id, feature values, missing flags, model version, score, decision, time.
- Failure modes: attackers use many cards per device (so keep device and card views); a stream lag makes velocity features stale exactly when the attack runs (alert on feature freshness); window math differing between stream and batch code (parity test, Q33); hot merchants.

**Example (hand-check):** card9 sends 8 payments 7 seconds apart. At 6021 s it has 3 earlier payments in the last minute, so the rule blocks the 4th payment; earlier ones pass because the counts were 0, 1, 2. Feature values are computed before adding the current payment, as a real request would see them.

**Code:**
```yaml
model: upi_fraud_v3
decision_budget_ms: 100            # total; the split below is a planning budget, not a measurement
budget_split_ms: {gateway_and_parse: 10, feature_fetch: 30, model_score: 20, rules_and_decision: 10, slack: 30}
entities:
  card: {key: card_id}
  device: {key: device_id}
  merchant: {key: merchant_id}
features:
  - {name: card_txn_count_1m,   entity: card,   kind: velocity_count, window: 1m,  freshness: stream,  default: 0,    on_missing: use_default}
  - {name: card_txn_count_1h,   entity: card,   kind: velocity_count, window: 1h,  freshness: stream,  default: 0,    on_missing: use_default}
  - {name: card_amount_sum_1h,  entity: card,   kind: velocity_sum,   window: 1h,  freshness: stream,  default: 0.0,  on_missing: use_default}
  - {name: device_distinct_cards_1h, entity: device, kind: distinct_count, window: 1h, freshness: stream, default: 1, on_missing: use_default}
  - {name: merchant_chargeback_rate_90d, entity: merchant, kind: batch_rate, window: 90d, freshness: daily, default: null, on_missing: use_global_prior}
  - {name: device_graph_risk_score, entity: device, kind: graph_batch, freshness: daily, default: null, on_missing: flag_and_use_median}
labels:
  name: is_fraud_confirmed
  source: chargeback_and_dispute_feed
  delay_days_min: 30               # labels mature late; training uses rows older than this
logging: [request_id, card_id, feature_values, feature_missing_flags, model_version, score, decision, decided_at]
```
```python
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
```
```bash
python3 -I q34_fraud_sim.py q34_fraud_spec.yaml
```

**Output (my run):** PyYAML 6.0.1, Python 3.13, seeded random traffic plus a made-up attack burst. The thresholds are invented for the demo. Kafka, Flink, Redis, graph computation and a real model are concept only, not executed. Latency budget numbers are a plan, not a measurement.
```text
spec errors: none | features: 6 | budget sum: 100 ms

  time  card   dev    amt   n_1m n_1h  sum_1h  dev_cards  decision
     3 card3  dev5       678    0    0        0      1     ALLOW
    89 card1  dev4      1614    0    0        0      1     ALLOW
   160 card2  dev2       849    0    0        0      1     ALLOW
  6000 card9  devX0     4999    0    0        0      1     ALLOW
  6007 card9  devX1     4999    1    1     4999      1     ALLOW
  6014 card9  devX2     4999    2    2     9998      1     ALLOW
  6021 card9  devX3     4999    3    3    14997      1     BLOCK
  6028 card9  devX0     4999    4    4    19996      1     BLOCK
  6035 card9  devX1     4999    5    5    24995      1     BLOCK
  6042 card9  devX2     4999    6    6    29994      1     BLOCK
  6049 card9  devX3     4999    7    7    34993      1     BLOCK

fallback row: {'card_txn_count_1m': 2, 'card_txn_count_1h': 4, 'card_amount_sum_1h': 0.0, 'device_distinct_cards_1h': 1, 'merchant_chargeback_rate_90d': None, 'device_graph_risk_score': None}
missing flags: {'card_amount_sum_1h': True, 'device_distinct_cards_1h': True, 'merchant_chargeback_rate_90d': True, 'device_graph_risk_score': True}
```

**Follow-ups:**
- *Why not compute features at request time from the database?* Scanning history per request will not fit a tight budget and is hard to keep identical with training.
- *What about UPI specifics?* Add payer and payee VPA, bank handle and beneficiary-age features; I would check current regulator and network rules for what data can be used.
- *How do you measure it works?* Offline: PR curve at the review capacity on delayed labels. Online: shadow mode first, then a staged rollout with a rules-only fallback.

**Common mistakes:**
- Forgetting label delay and training on "no chargeback yet" as clean.
- Zero as a default with no missing flag.
- One window only.
- Computing features after adding the current transaction (leakage in the sim).
- No feature logging, so training cannot be rebuilt.
- Claiming the design is from a named company.

---

### Q35 ⭐ 🔴 Design question: features for a recommender at an e-commerce or video app. Separate user, item, context and session features by freshness (batch, near-real-time, per request), say where embeddings live (offline training, online store, ANN index) and what the feature store holds versus the retrieval index, how cold-start users and items are handled, how the training set is built point-in-time from impression logs, and how to avoid feedback-loop leakage. Give a whiteboard answer, a feature-view spec validated with pyyaml, and a tiny simulation of session features with expiry.
**Asked at:** Recommender design write-ups (techinterview.org 'System Design Interview: Recommendation System' and personalization-engine LLD posts, a letsdatascience.com recommendation design post, DesignGurus recommendation answer; search snippets only, not opened; latency-budget numbers in those posts are illustrative and not used); editorial prep sites, not verified candidate reports; ML engineer and recommender roles at product and e-commerce companies | Feature-store interview write-ups (techinterview.org posts 'Why feature store interviews come down to point-in-time joins' and 'What MLOps interviewers actually probe about drift and feature stores', a prachub.com 'Design a Feature Store for Offline Training and Low-Latency Online Serving' prompt, a datavidhya 'Design a Feature Store for ML Models' breakdown, Educative and DesignGurus ML system design course pages; search snippets only, not opened; WebFetch of techinterview.org failed with getaddrinfo ENOTFOUND); editorial prep sites, not verified candidate reports; MLOps, ML platform and ML engineer roles at product companies and GCCs
**Say this first (1 line):** I split features by how fast they change: user profile batch, item stats near-real-time, session features streamed with a short expiry, and context computed per request; the feature store holds the values, the vector index holds only item embeddings for retrieval, and the training set comes from logged impressions with the features that were actually served.

**Then explain (whiteboard, concept only):**
- User: batch daily (long-term interests, user embedding). Item: near-real-time (CTR over the last hour, stock status), plus batch (content embedding). Session: streamed (last few items, clicks so far) with a TTL of about the session gap. Context: per request (hour, device, surface), not stored.
- Embeddings. Learned offline. User embedding in the online store (key lookup). Item embeddings go into the ANN index for retrieval, with a copy in offline storage for ranking features. The feature store holds feature values; the index serves nearest-neighbour search. Index and model version must match (a version tag in both).
- Cold start. New user: segment default (city, device) then popular-in-context. New item: category prior, content embedding, and exploration slots until enough impressions are seen.
- Training set. Start from the impression log (not from clicks only): request id, user, item, position, time, clicked, served-feature snapshot. Reuse the snapshot; for new features, as-of join on event time (Q31).
- Feedback loop. The model only gets clicks on what it showed, and position changes click rates. Log position, keep a small random or exploration traffic slice, debias or exclude boosted slots, and never use the post-impression counts (the click itself) as a feature: the sim shows features computed before the update.
- Failure modes: session store expiry shorter than real sessions (features vanish mid-session); embeddings refreshed in the index but not in the feature store (mismatched vector spaces); popularity features amplify their own winners; stale item stock leading to unbuyable recommendations.

**Example (hand-check):** Session s1 sees i1 (t=0), i2 (t=60, i2 clicked), i3 (t=200, clicked), i4 at t=1999 (1799 s after the last write, with a 1800 s TTL: still alive, 2 clicks). At t=3799 exactly 1800 s after the last write: expired, so the model sees an empty session, treated as a new session.

**Code:**
```yaml
feature_views:
  - name: user_profile_batch
    entity: user_id
    freshness: batch_daily
    store: [offline, online]
    ttl: 7d
    features: {age_bucket: string, top_categories_30d: "list[string]", user_embedding_v5: "list[float32]"}
    cold_start: {fallback: segment_default, segment_keys: [city_tier, device_type]}
  - name: item_stats_nrt
    entity: item_id
    freshness: near_real_time_5m
    store: [offline, online]
    ttl: 1d
    features: {ctr_1h: float, view_count_1h: int, stock_status: string}
    cold_start: {fallback: category_prior, min_impressions_before_trust: 100}
  - name: session_stream
    entity: session_id
    freshness: streaming
    store: [online]                 # offline copy comes from LOGGED values, see training_set
    ttl: 30m
    features: {last_5_items: "list[string]", clicks_in_session: int, session_start_ts: timestamp}
  - name: context_request
    entity: request_id
    freshness: per_request          # computed at request time, never stored
    store: []
    features: {hour_of_day: int, device_type: string, surface: string, is_weekend: bool}
retrieval_index:                    # NOT the feature store
  kind: ann
  holds: item_embedding_v5
  rebuilt: daily
training_set:
  source: impression_log            # request_id, user_id, item_id, position, shown_ts, clicked, served_feature_snapshot
  join: logged_features_first       # reuse what was served; backfill with as-of join on event time only for new features
  exclude: [position_debias_needed, popularity_boosted_slots]
```
```python
"""Q35: validate the feature-view spec, then simulate session features with sliding expiry (pure Python; Redis-like TTL emulated)."""
import sys, re, yaml

spec = yaml.safe_load(open(sys.argv[1]))
FRESH = {"batch_daily", "near_real_time_5m", "streaming", "per_request"}
errs = []
for fv in spec["feature_views"]:
    if fv["freshness"] not in FRESH: errs.append(f"{fv['name']}: bad freshness")
    if fv["store"] and not re.fullmatch(r"\d+[mhd]", fv.get("ttl", "")): errs.append(f"{fv['name']}: stored view needs ttl like 30m")
    if not fv["store"] and "ttl" in fv: errs.append(f"{fv['name']}: per-request view has no ttl")
    if "cold_start" not in fv and fv["entity"] != "request_id" and fv["freshness"] != "streaming":
        errs.append(f"{fv['name']}: no cold start rule")
print("spec errors:", errs or "none", "| views:", [v["name"] for v in spec["feature_views"]])

UNIT = {"m": 60, "h": 3600, "d": 86400}
n, u = re.fullmatch(r"(\d+)([mhd])", next(v["ttl"] for v in spec["feature_views"] if v["name"] == "session_stream")).groups()
TTL = int(n) * UNIT[u]
print("session ttl seconds:", TTL)

class SessionStore:
    """Online store emulation: value + last_write time; read after TTL returns None (like an expired key). Sliding expiry."""
    def __init__(self): self.d = {}
    def update(self, sid, now, item, clicked):
        cur = self.get(sid, now) or {"last_5_items": [], "clicks_in_session": 0, "session_start_ts": now}
        cur["last_5_items"] = (cur["last_5_items"] + [item])[-5:]
        cur["clicks_in_session"] += int(clicked)
        self.d[sid] = (now, cur)                       # refresh expiry on every write
    def get(self, sid, now):
        if sid not in self.d: return None
        t, v = self.d[sid]
        return v if now - t < TTL else None

POP_DEFAULT = {"last_5_items": [], "clicks_in_session": 0, "session_start_ts": None}   # cold-start fallback

# (time_s, session, item, clicked)
log = [(0, "s1", "i1", 0), (60, "s1", "i2", 1), (200, "s1", "i3", 1),
       (400, "s2", "i9", 0),
       (200 + 1799, "s1", "i4", 0),                    # 1799 s after last s1 write: still alive
       (200 + 1799 + 1800, "s1", "i5", 1)]             # exactly 1800 s after the previous write: expired -> new session
st = SessionStore()
training_rows = []
print("\n  time sess item  served_features(before this impression)")
for now, sid, item, clicked in sorted(log):
    served = st.get(sid, now) or POP_DEFAULT
    print(f"{now:6d} {sid:4s} {item:4s}  {served}")
    training_rows.append({"ts": now, "session": sid, "item": item, "label": clicked, "feat_clicks": served["clicks_in_session"]})
    st.update(sid, now, item, clicked)                  # the event updates state AFTER the feature was served

print("\nlogged training rows (features are the ones served, so no leakage from the click itself):")
for r in training_rows: print(" ", r)
```
```bash
python3 -I q35_session_sim.py q35_reco_spec.yaml
```

**Output (my run):** PyYAML 6.0.1, Python 3.13. The store is a plain-Python emulation of a key-value store with sliding expiry (not Redis). Real feature stores, ANN indexes and models: not executed.
```text
spec errors: none | views: ['user_profile_batch', 'item_stats_nrt', 'session_stream', 'context_request']
session ttl seconds: 1800

  time sess item  served_features(before this impression)
     0 s1   i1    {'last_5_items': [], 'clicks_in_session': 0, 'session_start_ts': None}
    60 s1   i2    {'last_5_items': ['i1'], 'clicks_in_session': 0, 'session_start_ts': 0}
   200 s1   i3    {'last_5_items': ['i1', 'i2'], 'clicks_in_session': 1, 'session_start_ts': 0}
   400 s2   i9    {'last_5_items': [], 'clicks_in_session': 0, 'session_start_ts': None}
  1999 s1   i4    {'last_5_items': ['i1', 'i2', 'i3'], 'clicks_in_session': 2, 'session_start_ts': 0}
  3799 s1   i5    {'last_5_items': [], 'clicks_in_session': 0, 'session_start_ts': None}

logged training rows (features are the ones served, so no leakage from the click itself):
  {'ts': 0, 'session': 's1', 'item': 'i1', 'label': 0, 'feat_clicks': 0}
  {'ts': 60, 'session': 's1', 'item': 'i2', 'label': 1, 'feat_clicks': 0}
  {'ts': 200, 'session': 's1', 'item': 'i3', 'label': 1, 'feat_clicks': 1}
  {'ts': 400, 'session': 's2', 'item': 'i9', 'label': 0, 'feat_clicks': 0}
  {'ts': 1999, 'session': 's1', 'item': 'i4', 'label': 0, 'feat_clicks': 2}
  {'ts': 3799, 'session': 's1', 'item': 'i5', 'label': 1, 'feat_clicks': 0}
```

**Follow-ups:**
- *Why not put embeddings only in the feature store?* Retrieval needs nearest-neighbour search, which a key lookup cannot do.
- *How fresh must item CTR be?* As fresh as the decision it supports; start at minutes, tighten only if experiments show gain.
- *How do you know feedback leakage is under control?* Compare against a random-exposure slice and watch popularity concentration.

**Common mistakes:**
- Training on clicks only.
- Using the current click's own counters as features.
- Mixing embedding versions between index and ranker.
- No cold-start rule per view.
- One freshness for everything.

---

