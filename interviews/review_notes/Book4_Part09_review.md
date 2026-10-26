# Book 4 Part 9 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 35 questions, Q1-Q35 (feature stores, Kafka, stream processing, Spark for ML feature pipelines). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-9, Q10-18, Q19-27, Q28-35; merged by heading: 35 of 35 merged, 0 skipped, 0 pending. No spend-limit stops. Each agent used its own Feast repo, SQLite online store, Spark warehouse and checkpoint dirs.

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q35; star order and counts 14 / 14 / 7 | pass |
| All 7 template labels present and in order; code fences balanced | pass for all 35 |

The lead did not re-run the scripts (they span several venvs and Spark/Feast state); pasted outputs come from each agent's real runs, with ANSI codes and JVM log noise stripped; code and outputs are in each agent's `code/` and `out/` folders. Timings are sandbox-only medians and differ on a re-run.

## What really ran (Feast 0.67.0 on pandas 2.3.3; PySpark 4.2.0 local[2] on openjdk 21; delta-spark 4.4.1; polars 2.1.0; duckdb 2.0.0; fastavro 1.13.1; pandas 3.1.0; pytest 9.1.1)
Feast: `feast apply`, `get_historical_features`, `materialize`, `get_online_features` on a Parquet source and SQLite online store; registry query, tags, owners. Spark: groupBy and `explain()`, join-strategy plans, skew demo with salting, UDF forms, caching with an accumulator, partition counts, Structured Streaming with event-time window, watermark, memory sink and a checkpoint restart, Delta write/read and OPTIMIZE. Point-in-time joins in pandas, polars and DuckDB. Pure-Python emulations: partitions and offsets, consumer groups, delivery semantics, DLQ and backpressure, CDC with LSN guard, sequence-guarded store, Redis-like session store.

## Findings kept in the text (observed in these versions)
- Feast: replaying an old materialize window overwrote a newer online value (8 to 3) until a later full-window run repaired it; `materialize-incremental` missed a late row; a row just outside the TTL is dropped offline (3 rows back for 4 requested); on SQLite a 3-day-old value was still returned online with a 2-day TTL; Feast dropped a label row with no earlier feature value where pandas/DuckDB/polars gave a null; the same short feature name in two views raises FeatureNameCollisionError (`full_feature_names=True` fixes it).
- Spark Structured Streaming dropped a late event (window stayed at 3 where plain Python counted 4); one hot key put 85,057 of 100,000 rows into one partition and salting evened it out; a plain `udf` is already Arrow-optimised in 4.2.0.
- A naive CDC consumer resurrects a deleted row; an LSN-guarded one survives replay. Event-time-only joins leak late rows and corrections; filtering on ingestion time matches an online-store replay.
- Online serving: one call with all features is far cheaper than one call per feature (sandbox timings only).

## Not executed
Any real Kafka broker or client (all Kafka behaviour is a labelled pure-Python emulation; the partitioner uses crc32, not Kafka's murmur2), Debezium, Schema Registry server, Flink, Kafka Streams, Tecton, Hopsworks, SageMaker/Vertex/Databricks feature stores, Redis/DynamoDB stores, the Spark UI, `kafka-consumer-groups.sh`, any lineage tool, Feast's `version` argument (check current docs). A "stop" in the Spark checkpoint demo is a clean availableNow finish, not a kill -9.

## Hedged ("check current docs")
Product-specific claims for Tecton, Hopsworks, managed stores and engine comparisons come from memory or snippet-only sources. Spark plan details depend on version and AQE settings. The Q34 latency budget and Q27 allotments are labelled plans or assumptions, not measurements. No benchmark, price or salary numbers.

## Evidence limits
No candidate-reported questions found; the one WebFetch failed, so every source is a snippet. No India-specific Spark/Kafka sources were found. See research_notes/Book4_Part09_sources.md.
