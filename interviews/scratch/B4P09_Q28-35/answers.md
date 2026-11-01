# Book 4 Part 9, answers Q28-Q35 (Wave B)

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
