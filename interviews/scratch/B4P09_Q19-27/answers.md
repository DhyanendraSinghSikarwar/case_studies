# Book 4 Part 9, Q19-Q27 answers (Wave B)

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
