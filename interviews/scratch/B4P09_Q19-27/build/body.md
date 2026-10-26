@@Q19
**Say this first (1 line):** A poison message must never block the partition: retry only transient errors a few times with backoff, park everything else in a dead-letter topic with full context, commit the offset, and treat growing lag as a capacity problem you fix with pull control, scale-out or shedding.

**Then explain:**
- **Poison versus transient.** Parse failure, schema mismatch and null key will fail the same way forever, so do not retry them. Go straight to the DLQ. A sink timeout is transient, so retry a bounded number of times with backoff, then park it.
- **Why bounded.** An endless retry on one record stalls the whole partition (offsets are in order). Failure mode: lag grows, nobody is paged, and the consumer may also miss `max.poll.interval.ms` and trigger a rebalance.
- **DLQ record content.** Original topic, partition, offset, key and value as raw bytes (not re-serialised), headers, error class and message, attempt count, failure timestamp, consumer app and version, schema id if any. Without this you cannot replay or debug. A DLQ is a convention (a topic you write to), not a built-in Kafka feature. Kafka Connect has its own error-tolerance and DLQ settings for sink connectors (check current docs).
- **Backpressure in Kafka is pull-based.** The consumer asks for records, so a slow consumer does not get flooded. It just falls behind and lag grows (log end offset minus committed offset). Levers: `max.poll.records`, `pause()` and `resume()` partitions while a downstream queue drains, add consumers (useful only up to the partition count), speed up the work, or shed load (drop or sample) when freshness matters more than completeness, as for some real-time features.
- **Trade-offs.** Parking a record breaks strict per-key ordering for that key. Commit only after a record is done or parked, otherwise a crash loses it. Alert on DLQ rate and on lag trend, not just lag level.

**Example:** 80 messages arrive in an 8-tick burst, 10 per tick. One consumer pulls 4 per tick, so lag climbs by 6 every tick. At tick 6 we add a second consumer. It still falls behind (8 per tick against 10 produced) until the burst ends at tick 8, then drains by tick 13. 18 messages end in the DLQ: 9 null keys, 4 parse errors, 4 schema mismatches, 1 retries-exhausted. Three flaky messages succeeded on retry.

**Code:**
{{CODE:q19_dlq.py}}

**Output (my run):** (pure-Python EMULATION of consumer semantics; no Kafka broker or client was run; python3 -I)
{{OUT:q19.txt}}

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

@@Q20
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
{{CODE:q20_rolling.py}}

**Output (my run):** (pandas 3.1.0 in the helper venv, python3.13, `-I`)
{{OUT:q20.txt}}

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

@@Q21
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
{{CODE:spark_common.py,q21_joins.py}}

**Output (my run):** (PySpark 4.2.0, local[2], openjdk 21; plan lines filtered to join, Exchange, Sort, scan nodes)
{{OUT:q21_joins.txt}}

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

@@Q22
**Say this first (1 line):** Prefer built-in functions (Catalyst optimises them and they run in the JVM), use a vectorised pandas or Arrow UDF when you need Python logic, and use a plain row-at-a-time Python UDF last, because every row crosses the JVM-Python boundary.

**Then explain:**
- **Built-ins.** Catalyst understands them: it can push filters, prune columns, fold constants and generate code. The whole thing stays inside the JVM.
- **UDFs are black boxes.** Catalyst cannot look inside, so no pushdown through them and no codegen. In the plan they appear as an `EvalPython` node.
- **The cost is serialisation.** Rows move from the JVM to a Python worker and back. The classic Python UDF does this row by row with pickle (`BatchEvalPython`). Pandas and Arrow UDFs move columnar batches (`ArrowEvalPython`), so less overhead and you can use vectorised NumPy and pandas code.
- **Version note.** In this Spark 4.2.0 run, even a plain `udf` was Arrow-optimised by default; I had to pass `useArrow=False` to get the classic row-at-a-time path. Older versions defaulted to pickle. Check your version's docs.
- **When to reach for a UDF.** A library call you cannot express with built-ins (a model score, a custom parser). Then batch it with a pandas UDF. Also null handling: you must handle `None` yourself in a UDF.

**Example:** feature `amount / (amount + 50)` over 400,000 rows. All four forms returned the same sum (180144.149674) and count (400,000). In the plan the built-in is a single `Project` expression; the UDF forms add a `BatchEvalPython` or `ArrowEvalPython` node.

**Code:**
{{CODE:q22_udf.py}}

**Output (my run):** (PySpark 4.2.0, pandas 2.3.3, pyarrow, local[2]; the helper `spark_common.py` is the one shown in Q21)
{{OUT:q22_udf.txt}}

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

@@Q23
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
{{CODE:q23_layout.py,q23_delta.py}}

**Output (my run):** (PySpark 4.2.0, delta-spark 4.4.1 resolved its Delta jar through ivy at run time, local[2])
{{OUT:q23_layout.txt,q23_delta.txt}}

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

@@Q24
**Say this first (1 line):** Cache a DataFrame only when several actions reuse it and it fits memory (or memory and disk), release it when done, and size partitions to the cores and data (a few tasks per core, not too tiny) using `repartition` to rebalance (shuffle) and `coalesce` to shrink without a shuffle.

**Then explain:**
- **What cache does.** Spark is lazy: every action recomputes the lineage from the source unless the data is persisted. `cache()` or `persist()` keeps computed partitions so the second action reads them instead. It only takes effect once an action materialises it.
- **When it hurts.** Used once, or cheap to recompute, or bigger than memory: you pay memory and eviction for nothing and may slow other work. Failure mode: stale cached data when the source changed, and forgotten caches that eat executor memory. Call `unpersist()`.
- **Storage levels.** `MEMORY_ONLY` (recompute what does not fit), `MEMORY_AND_DISK` (spill the rest), `DISK_ONLY`, `_2` variants replicate, and serialised levels trade CPU for space. DataFrame `cache()` uses a memory-and-disk level.
- **Partition count.** Rule of thumb: 2 to 4 tasks per core, and partitions of manageable size (often cited as 100 to 200 MB; check docs). `spark.sql.shuffle.partitions` sets the post-shuffle count (default 200; AQE can coalesce it). Too few: no parallelism, spills. Too many: scheduling overhead and tiny files.
- **repartition versus coalesce.** `repartition(n)` does a full shuffle and balances sizes, and it can grow or shrink. `coalesce(n)` merges existing partitions without a shuffle, can only shrink, and can leave uneven sizes.

**Example:** a source of 10,000 rows with three actions. Without cache the source function ran 30,001 times (3 passes); with cache 10,001. The extra 1 in each is schema inference reading the first row for `toDF`. Partitions: range default 4, `repartition(8)` gives 8 balanced partitions of 12,500 rows, `coalesce(2)` on 4 splits gives 2 of 50,000, `coalesce(16)` stays at 8, and a `groupBy` after a shuffle follows `shuffle.partitions` = 4.

**Code:**
{{CODE:q24_cache.py}}

**Output (my run):** (PySpark 4.2.0, local[2]; helper from Q21; the accumulator is a teaching probe, since task retries can over-count)
{{OUT:q24_cache.txt}}

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

@@Q25
**Say this first (1 line):** Lambda runs a batch path and a speed path and merges them in serving, which gives two codebases that drift; Kappa has one streaming path and replays the log for reprocessing; in practice for features I keep one shared transformation, backfill from the lake and use the stream for freshness.

**Then explain:**
- **Lambda.** Batch layer (complete, accurate, slow), speed layer (recent, approximate, fast), serving layer merges. Good when batch accuracy rules matter. Pain: two implementations of the same logic.
- **Kappa.** Everything is a stream. To reprocess, replay the log through the new code. Simple in theory, but replay is limited by how long the log is retained and by the cost of replaying; many teams backfill from the lake instead.
- **For features.** The batch path builds training sets (offline store); the stream path fills the online store. If they are two codebases you get training-serving skew. Fix: one shared transformation function or library used by both, or a framework that runs the same definition in batch and stream (check current docs for your tool).
- **When to use which.** Lambda-ish: you need heavy batch recompute and low-latency partial values. Kappa-ish: logic is simple, events are retained or archived, one team owns it. Middle ground: shared code, lake as source of truth for backfill, stream for freshness.
- **Replay limit.** If Kafka keeps 7 days and the feature window needs 30 days, you cannot rebuild from Kafka alone. You need the lake or compacted state.

**Example:** `spend_today` per user. The batch team uses the IST business day, subtracts refunds, skips nulls. The stream team uses the UTC day and ignores refunds. On six events, user u1 on 2025-03-01 is 100 in batch and 150 in stream, and the late-evening purchase lands on a different day (20 on 03-02 versus 0). After both call one `contribution()` function, they match.

**Code:**
{{CODE:q25_two_codebases.py}}

**Output (my run):** (python3 -I, pure Python)
{{OUT:q25.txt}}

**Follow-ups:**
- *What else tends to differ?* Time zone, late-data rules, rounding, null defaults, deduplication, and the join key.
- *How do you detect drift between the two paths?* Compare batch and online values on a sample, and alert on mismatch (Part 8 covers monitoring).
- *Can Kappa do a backfill?* Yes if the retained log or an archived copy covers the period; otherwise load history from the lake into the same code path.

**Common mistakes:**
- Treating "same logic" as true because the specs read the same.
- Assuming Kafka retains everything forever.
- Merging batch and speed results without a clear cut-over time.
- Testing only the happy path (the null and refund rows are where they disagreed).

@@Q26
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
{{CODE:q26_cdc.py}}

**Output (my run):** (pure-Python EMULATION of change events; no Debezium, database or Kafka was run)
{{OUT:q26.txt}}

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

@@Q27
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
{{CODE:q27_online_lookup.py}}

**Output (my run):** (Feast 0.67.0, local provider, SQLite online store in its own temp repo, pandas 2.3.3; in-process, no network, timings sandbox-only and not a production estimate)
{{OUT:q27.txt}}

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
