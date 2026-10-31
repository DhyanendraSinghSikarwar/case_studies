**Say this first (1 line):** One copy of the online store is 10 million x 40 x 8 bytes = 3.2 GB, and 25,000 events a second means 125,000 events in each 5-second freshness window, so the design is a stream processor updating a keyed store.

**Clarifying questions:**
- Is the 5 seconds from event to feature visible at scoring time, and is it a p99 target? It sets the pipeline budget.
- What is the scoring latency budget and what happens on a feature miss? A default and a fallback model are needed.
- Which features are windowed counts and which are slow profile values? Slow ones do not need streaming.
- Is training done from the same feature definitions? Training-serving skew is the classic fraud failure.
- How many copies and regions are needed? The 3.2 GB is one copy only.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data and labels 5, baseline 4, features and model 10, evaluation 6, launch 6, monitoring and cost 5):**
1. Clarify and frame: authorisation-time scoring with fresh velocity features.
2. Metrics and guardrails: feature age p99, missing-feature rate, scoring p99, fraud recall at a fixed false-decline rate.
3. Data and labels: chargebacks arrive late, so label with a delay and use confirmed reports for fast signals.
4. Baseline first: rules on a few velocity counts (card used in N places in 10 minutes), then a model.
5. Pipeline and trade-offs: events into a log, a stream job updating windowed counters, a keyed online store; the same definitions write to an offline store for training. Memory: 3,200,000,000 B = 3.2 decimal GB (2.98 GiB), 3 copies with an assumed 1.5x overhead is 14.4 GB. Window: 25,000 x 5 = 125,000 events, at most 1.25% of cards touched per window. A 1-hour counter in 5-second buckets is 720 buckets per card per counter, which is why you keep a few counters, not many.
6. Evaluation: offline with point-in-time features (no leakage), then shadow scoring on live traffic to measure feature age and score agreement.
7. Launch: shadow, then a small share of traffic with a human review band, with a fail-safe if freshness slips.
8. Monitoring and cost: feature age, null rate, distribution drift against training, store memory growth, reprocessing plan for late events.

**Metrics:**
- Feature freshness = scoring time minus the last event time included in the feature, p99 (target 5 s).
- Missing-feature rate = scored events with a default feature / scored events.
- Fraud recall at a fixed review rate; false-decline rate = good transactions blocked / good transactions.

**Risks:**
- Training-serving skew when offline and online code differ.
- Late and out-of-order events change window counts.
- A hot card (a merchant test attack) skews one key.
- Memory is per copy: replication, overhead and growth multiply the 3.2 GB.

**What the interviewer scores:**
- Strong: 3.2 GB, 125,000 per window, with units and "one copy" said aloud.
- Strong: one feature definition for training and serving; point-in-time training data.
- Weak: names tools only; sizes memory without replication; leakage in training.

**Example:** Illustrative numbers. 10,000,000 x 40 x 8 = 3,200,000,000 B; 25,000 x 5 = 125,000.
- Weak: "Use Kafka and Redis, it will be real time."
- Strong: "One copy is 3.2 GB, so three copies with overhead is under 15 GB, a small store. The harder part is correctness: 125,000 events land in every window, so I need late-event handling and one definition of each feature shared by training and serving."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *Is 5 seconds a pipeline or a feature property?* Both: event-to-store lag plus the window update interval; measure it end to end.
- *What if the store is down?* Default features, a simpler fallback rule model, and an alert; decide fail-open or fail-closed with the business.

**Common mistakes:** Quoting memory for one copy as the total. Mixing GB and GiB. Training with features computed after the event. No default for a missing feature.
