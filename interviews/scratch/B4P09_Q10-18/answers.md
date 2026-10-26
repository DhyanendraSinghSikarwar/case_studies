# Book 4 Part 9, Q10-Q18 answers (Wave B)

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

