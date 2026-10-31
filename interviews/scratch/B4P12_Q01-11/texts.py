A[1]='''**Say this first (1 line):** Before I draw anything I ask what the decision is, how fast, who owns false positives and how late the labels come, then I turn the numbers into a table: 20 million a day is about 231 TPS on average and about 1,389 TPS at a 6x peak.

**Then explain:**
- Questions I ask: is the score used at authorisation time (blocking) or after the fact? What is the latency budget for the model hop? Who owns a wrongly blocked good customer? How late do chargebacks arrive? Which regulator and data-residency limits apply (check current rules and the company policy)? What happens if the model is down: fail open or fail closed?
- Three numbers I want: peak TPS, fraud rate, and the cost of a missed fraud versus a blocked good customer. Without the cost ratio I cannot choose a threshold.
- Success metrics at three levels. Model: recall at a fixed review budget, precision, PR-AUC. Service: p99 latency, error rate, availability. Business: fraud loss, false-decline rate, analyst load.
- Failure modes: peak assumed too low (ratio is a guess, ask for the real busiest minute), labels delayed so recall looks worse than it is, nobody owns false positives.
- Scoring note (10 pts, Set F Q1, 6 min): full points for asking at least four of the clarifying questions, stating assumptions out loud, and getting 231 and 1,389 right with the 6x ratio shown. Partial (5-7) for good questions but arithmetic or metrics missing. Little credit for jumping to an architecture.

**Example:** 20,000,000 / 86,400 = 231.5 TPS average. Times 6 = 1,388.9 peak. If the interviewer later says "700 TPS peak", that means either a different daily volume (about 10 million) or a different ratio. Say so and ask, do not silently switch. (Note: Set F Q2 starts from 700 TPS; at 20 million a day and 6x the arithmetic gives about 1,389, so state which input you changed.)

**Code:**
@@CODE@@

**Output (my run):**
@@OUT@@

**Follow-ups:**
- Why ask about label delay in a requirements round? Because it sets the retraining cadence and how you evaluate (Q8 of this set covers it).
- Why a peak ratio and not the average? Capacity is paid for at the peak and the p99 budget is broken at the peak.

**Common mistakes:** Starting with Kafka and boxes. Using average TPS for sizing. Giving only a model metric and no business metric. Not asking what happens when the scorer is down.
'''
A[2]='''**Say this first (1 line):** I clarify the objective first, because watch time, satisfaction and creator fairness pull in different directions; then 8 million users times 6 loads is 48 million feed requests a day, about 556 per second on average, over a 2 million item catalogue.

**Then explain:**
- Ask: what is the objective (watch time can reward clickbait; satisfaction needs surveys or proxies; creator fairness needs exposure rules)? What share of users and items are cold-start? How fresh must new items be (minutes or a day)? What is the latency budget? What does a bad recommendation cost (a skipped video versus an unsafe one)?
- Shape: candidate generation narrows 2 million items to hundreds, then ranking scores them, then re-ranking applies business rules and diversity. Stages exist because you cannot score 2 million items per request.
- Book 1 owns: model choice (two-tower, ranker loss, cold-start methods), offline metrics. Platform owns: feature stores, embedding index refresh, serving latency, A/B plumbing, rollback, logging for training.
- Failure modes: feedback loops (you only learn about what you showed), stale embeddings, peak at evening hours far above the average.
- Scoring note (10 pts, Set R Q1, 6 min): full for explicit objective trade-off, cold-start and freshness questions, correct 48M and about 556 rps, and a clear modelling-versus-platform split. Partial for a table without questions. Low if you only describe a model.

**Example:** 8,000,000 x 6 = 48,000,000 requests/day; /86,400 = 555.6 rps. If 70 percent of traffic lands in 4 evening hours (invented), the busy-hour rate is 2,333 rps, about 4x the average. Size for the busy hour.

**Code:**
@@CODE@@

**Output (my run):**
@@OUT@@

**Follow-ups:**
- Which metric do you launch on? A guardrail set plus the main metric in an A/B test, not offline AUC alone.
- Where do you put exposure logs? In the training pipeline with the served position, so you can correct position bias later.

**Common mistakes:** Treating it as only a modelling question. Forgetting cold-start. One objective with no guardrails. Sizing on the average.
'''
A[3]='''**Say this first (1 line):** For a bank credit model I ask who approves, how declines are explained, how fairness is checked, what is logged and for how long, where data may live and who validates independently, and I keep these as a requirements and controls file that a script can validate.

**Then explain:**
- Controls to ask about: approval authority (model risk committee), explainability and reasons for a decline, fairness review, audit trail and retention, data residency and where processing is allowed, third-party and cloud outsourcing rules, independent validation.
- Hedge the regulation: RBI and bank policy rules change. Say "check the RBI site and the bank's own policy"; I do not quote circular text from memory.
- Put it in YAML with an owner and an evidence artefact per control, so every row answers "who" and "show me". A pydantic model plus a coverage check turns a forgotten control into a failed validation.
- Failure modes: a control with no owner, no evidence, or a whole area missing; requirements kept in a slide deck that nobody checks.
- Scoring note (10 pts, Set C Q1, 8 min): full for covering all seven areas, giving owners and evidence, hedging regulation and running a validator that rejects an incomplete file. Partial for a list without owners. Do not invent legal text.

**Example:** The sample file has 7 controls, one per area. Removing the validation row makes the validator fail with "missing areas ['validation']".

**Code:**
@@CODE@@

**Output (my run):**
@@OUT@@

**Follow-ups:**
- Why a pydantic model? It gives typed fields and clear error messages; the coverage rule is plain Python.
- Is this compliance? No. It is a checklist structure; legal review decides what is required.

**Common mistakes:** Quoting regulations from memory. Controls with no owner. Treating the builders as the independent validators.
'''
A[4]='''**Say this first (1 line):** Tag everything with team, model and environment, allocate shared costs by usage where you can measure it and by fixed split where you cannot, show the untagged residue openly, and prove the allocations sum to the bill.

**Then explain:**
- Mandatory tags: team, model or service, environment, cost-centre. Enforce at creation time with policy (no tag, no resource).
- Shared costs (cluster, registry, feature store): by measured usage (cluster-hours, lookups) when meters exist; fixed even split for small flat things like the registry. Say which rule you used so teams can argue with it.
- Untagged residue: do not hide it. Report it as its own line, then either spread in proportion to direct cost or assign to the platform team; track it as a metric that should fall.
- Showback means report the cost, no money moves. Chargeback means the team's budget is actually debited. Start with showback until tags are above a high coverage level and teams trust the numbers, then move to chargeback.
- Failure modes: allocations that do not sum to the bill, teams gaming tags, usage meters missing for shared services.

**Example:** Abstract units. Bill 2,000 = compute 1,000 + storage 300 + shared cluster 400 + registry 50 + feature store 150 + untagged 100. Tagged direct is 1,230 of the 1,300 compute+storage, so the residue is 70 + 100 = 170, spread by direct cost. Fraud ends at 782.5, reco 709.7, forecast 281.0, credit 226.8; total 2,000.

**Code:**
@@CODE@@

**Output (my run):**
@@OUT@@

**Follow-ups:**
- When does chargeback hurt? When numbers are disputed or teams cut safety spend such as monitoring to save their budget. Keep a shared floor.
- Usage or fixed split? Usage if measured and stable; fixed when metering costs more than the item.

**Common mistakes:** No assertion that the split adds up. Ignoring untagged cost. Starting with chargeback on bad data. Quoting prices instead of units.
'''
A[5]='''**Say this first (1 line):** One replica handles 333 requests a second, peak with headroom is 910, so each zone needs 3 replicas (6 in total) so that either zone alone carries the peak at 70 percent utilisation; a split of 2 per zone would run at 105 percent after a zone loss.

**Then explain:**
- Method (see Part 6 Q15): replica capacity = threads / service time = 4 / 0.012 = 333 rps. Required capacity = peak x (1 + headroom) = 700 x 1.3 = 910. Sizing is per zone because the survivor must carry everything.
- Queue sim (M/M/c style, exponential arrivals and service, sandbox numbers only): p99 wait is nearly zero at 50 percent utilisation and climbs steeply past 85 percent. With one zone lost at 700 rps, utilisation is 0.70, simulated p99 wait is about 8 ms. Add the 12 ms service time and a typical request is near 20 ms, inside the 60 ms budget. The sim's exponential service time is pessimistic (its p99 service alone would be about 55 ms, total about 64 ms), so confirm with a real load test.
- Timeouts, retries and load shedding (Part 6 Q31): shed first low-value work such as batch re-scoring, enrichment calls and non-critical features. Never silently drop the authorisation decision: fail closed or fail open is a written policy per merchant risk tier (for example, small amounts fail open to a rules fallback; high risk fails closed). Retries need budgets or they multiply load during an outage.
- Failure modes: assuming N/2 capacity is enough, retry storms, a shared dependency (feature store) that fails both zones at once.
- Scoring note (20 pts, Set F Q2, 10 min): full for the replica arithmetic including the zone-loss check (6 pts each for per-replica capacity and zone survival), the saturation curve (5 pts), shed/never-shed policy (3 pts). Partial for sizing on the total only.

**Example:** 3 replicas x 333 = 1,000 rps per zone. Peak 700 / 1,000 = 0.70 after losing a zone. 2 per zone gives 700/667 = 1.05, saturated, queue grows without bound.

**Code:**
@@CODE@@

**Output (my run):**
@@OUT@@

**Follow-ups:**
- Why not autoscale? Autoscaling lags fraud bursts; keep a floor sized for the survivor case and autoscale above it.
- Is the sim exact? No: exponential service is a rough model; real service times are less variable, so measure with a load test.

**Common mistakes:** Dividing capacity across zones without checking survival. Using mean latency for the p99 budget. Retrying without limits. Dropping decisions with no policy.
'''
A[6]='''**Say this first (1 line):** Two stages: retrieve a few hundred candidates cheaply, then rank them with a heavier model; at 400 candidates and 900 requests a second that is 360,000 ranking calls a second, and a two-tower pre-filter down to 150 cuts it to 135,000.

**Then explain:**
- Budget (120 ms, invented): feature lookup 15, retrieval 25, ranking 55, re-ranking 15, overhead 10 = 120. Ranking gets the biggest slice, retrieval and lookups run in parallel where possible (see Part 9 Q27 for the real-time feature budget).
- Feature stores: online store (low-latency key-value) serves user and item features at request time; the offline store holds history for training and backfills; both must compute features the same way (Part 9 Q35 for recommender features).
- Levers: two-tower pre-filter (cheap dot-product to shrink candidates), caching rankings for repeat users, smaller candidate set. Batch the 400 candidates into one model call; ranking calls are batched rows, not 400 network calls.
- Quality risk: a tighter pre-filter can drop the item the ranker would have put first (recall loss at the retrieval stage cannot be recovered later). Caching serves stale results, which hurts freshness and new-item exposure. Check with an A/B test and a retrieval-recall metric.
- Scoring note (20 pts, Set R Q2, 10 min): full for a budget that sums to 120, correct 360,000, one lever with its quality risk and online/offline store placement. Partial if the arithmetic is right but the risk is missing.

**Example:** 900 x 400 = 360,000 candidate scores/s. Prefilter to 150: 135,000 (-62.5 percent). 30 percent cache hit (invented) on top: 94,500.

**Code:**
@@CODE@@

**Output (my run):**
@@OUT@@

**Follow-ups:**
- Where does re-ranking sit? After ranking: diversity, freshness boosts, creator-fairness rules, safety filters.
- How do you protect cold-start items? Reserve exploration slots in re-ranking.

**Common mistakes:** Treating candidates as 400 separate calls. Cutting candidates with no retrieval-recall check. Budget that does not sum.
'''
A[7]='''**Say this first (1 line):** A regulated credit model moves through fixed gates, each gate needs named evidence and a named signer, and the pipeline refuses to move forward if any evidence is missing or the same person signed twice.

**Then explain:**
- Gates and evidence: lineage (lineage id, data snapshot; Part 4 Q15) then development (dev report, signed by the model owner), independent validation (validation report, signed by the validator), approval (approval record from the committee; Part 8 Q41 for governance), shadow or champion-challenger period (shadow report), deployment (deploy record, release approver separate from model owner; Part 7 Q38 and Q24), monitoring (drift and performance reports) and retirement (reason and sign-off).
- Separation of duties (Part 7 Q24): the approver must not be the validator or builder; the deployer must not be the approver. The state machine enforces this in code.
- Refusal is the point: a missing field, a skipped gate or a duplicate signer returns an error and the state does not change. Tests prove each refusal.
- Failure modes: evidence stored as free text that nobody checks, a gate bypassed under delivery pressure, retirement forgotten so old models keep scoring.
- Scoring note (20 pts, Set C Q2, 10 min): full for all gates with an evidence artefact and signer each (10 pts), working refusal logic with tests (6 pts), monitoring and retirement (4 pts). Partial if the gates are listed without evidence.

**Example:** Promoting to approval with approver = validator raises "approver must differ from validator/builder" and the model stays at validation.

**Code:**
@@CODE@@

**Output (my run):**
@@OUT@@

**Follow-ups:**
- Is code enough? No. It enforces the checklist; people still decide. Store the evidence in the registry and the audit log.
- How long do you shadow? Long enough for the volume and seasonality to cover the cases; set it in policy, not in this sketch.

**Common mistakes:** Evidence as a checkbox with no artefact. One person playing every role. Forgetting retirement. A pipeline that can be skipped.
'''
A[8]='''**Say this first (1 line):** Fraud labels arrive 7 to 45 days late and come mostly from the cases analysts looked at, so a fresh model looks worse than it is until labels land; train on matured windows with point-in-time features and watch proxies in the meantime.

**Then explain:**
- Bias: only the top 0.5 percent are reviewed, so labels for frauds the model missed arrive only via chargeback; the training set reflects the old model's choices (selection bias). Fraud is 0.1 percent so classes are rare; use weights or sampling and PR metrics.
- Train on matured windows: use transactions old enough that most labels have arrived (for example older than 45 days, or older than a chosen maturity point), plus recent data with a censoring flag or down-weighting. Features are built point-in-time (Part 9 Q6, Q34) so no future leakage.
- Before labels arrive (Part 8 Q43, Q8): watch input drift, score distribution, flag rate, analyst-confirmed rate, and early proxies such as customer complaints.
- Retraining trigger (Part 5 Q30): schedule plus drift or business triggers, and a gate that the new model beats the champion on matured data.
- Sim result: with all labels on a 7-45 day delay, apparent recall (caught and labelled / all eventual frauds) is 0.000 at day 7 and 0.054 at day 14, against a true recall of 0.339. If confirmed flagged cases arrive faster than chargebacks, recall among labelled cases only looks too high (1.000 at day 7), a bias in the other direction.
- Scoring note (30 pts, Set F Q3, 12 min): full for explaining delay and selection bias (8), matured-window training with point-in-time features (8), pre-label monitoring and retrain trigger (6), the simulation and both bias directions (8). Partial for naming delay without a fix.

**Example:** First-week cohort has 56 frauds, 19 caught (0.339). At day 14 only 10 labels exist, so naive recall reads 5.4 percent.

**Code:**
@@CODE@@

**Output (my run):**
@@OUT@@

**Follow-ups:**
- How do you fix selection bias? Keep a small random-review holdout so you see frauds the model would miss, and use it for unbiased evaluation.
- Why not train on unlabelled as good? Unlabelled recent rows include real frauds not yet reported; that teaches the model to miss them.

**Common mistakes:** Evaluating on labels that have not matured. Training on analyst-reviewed rows only. Leaking future features. Retraining on a fixed calendar with no maturity rule.
'''
A[9]='''**Say this first (1 line):** Low average utilisation with a queue of waiting teams means GPUs are held, not used, so I measure held versus busy hours, then lease notebooks, share small jobs and preempt, not buy more GPUs.

**Then explain:**
- Causes: notebooks reserved by default and left idle, oversized requests (a whole GPU for a small job), no queue or preemption policy, small jobs each holding a full card, data-loading stalls that keep the GPU waiting on the CPU.
- Levers: quotas with borrowing, time-boxed leases, sharing (time-slicing or MIG where the hardware supports it; check current docs), bin-packing, scale-to-zero node pools, checkpoint-and-preempt for long jobs. Kubernetes mechanics: Part 3 Q15, Q20, Q21.
- Measure waste: GPU-hours held minus GPU-hours busy, by team and job kind, from scheduler data and GPU utilisation metrics. Report idle-held hours per team (showback).
- Failure modes: preemption without checkpointing loses work; time-slicing gives no memory isolation, so one job can hurt another; leases that are too short annoy users.
- Honest point: leasing frees capacity; utilisation percent rises only when waiting jobs use the freed hours.

**Example:** Invented 24h log, 16 GPUs: capacity 384 GPU-h, held 262, busy 81.2 (21.1 percent of capacity; 31.0 percent of held hours, the 31 percent in the prompt matches this ratio). A 4h notebook lease for notebooks under 10 percent busy reclaims 76 GPU-h (19.8 percent of capacity). If queued jobs use them at 80 percent busy, utilisation of capacity goes to 37 percent.

**Code:**
@@CODE@@

**Output (my run):**
@@OUT@@

**Follow-ups:**
- Is more utilisation always good? No; leave headroom for latency-sensitive inference and bursts.
- MIG or time-slicing? MIG isolates memory but needs supported hardware and fixed slices; time-slicing is flexible with no isolation. Check current docs.

**Common mistakes:** Buying GPUs before measuring held-versus-busy. Preempting without checkpoints. Reporting one utilisation number with no per-team view.
'''
A[10]='''**Say this first (1 line):** An unbounded queue just hides overload: it keeps every request, makes everyone wait about 30 seconds, and burns most work on callers who already gave up; a bounded queue that rejects or drops old requests keeps latency inside the timeout.

**Then explain:**
- Setup: 200 rps for 20 s then 40 rps for 100 s = 8,000 requests; workers do 80 rps, so 9,600 fit in 120 s overall but the burst overfills early. Callers time out after 2 s (invented).
- Unbounded: max depth 2,400, p99 wait 29.6 s, only 2,026 useful, 5,974 wasted on late callers. Bounded with reject (cap 160): depth 160, p99 2.0 s, 2,240 rejected, 5,718 useful, 42 wasted. Bounded with timeout and drop-oldest: p99 1.7 s, 5,760 useful, 0 wasted. Sandbox numbers from my simulation, not benchmarks.
- Choice: reject fast gives callers a clear error to retry elsewhere (Part 6 Q31 on retries and shedding). Drop-oldest favours fresh requests when stale answers are useless.
- Use a message queue and async replies when callers can wait (batch scoring, emails, long jobs) and results can be delivered later (Part 6 Q30; Part 9 Q19 on Kafka consumer lag). Not for authorisation-time decisions.
- Failure modes: retries amplify the burst; the queue limit too high means it delays rather than protects; no metric on rejects.

**Example:** Queue cap 160 at 80 rps equals 2 s of work, the same as the caller timeout, so anything still queued can finish in time.

**Code:**
@@CODE@@

**Output (my run):**
@@OUT@@

**Follow-ups:**
- How to set the bound? Service rate times the longest acceptable wait.
- What do clients see? A fast 429/503 with a retry hint and jittered backoff.

**Common mistakes:** Unbounded queues. Queue limit larger than the caller timeout. Counting throughput without separating useful from wasted work. Retrying without backoff.
'''
A[11]='''**Say this first (1 line):** A scanner finds secrets, but the fix order is: revoke and rotate first, clean history second, then block it from coming back with pre-commit and CI scans and short-lived credentials; deleting the file does nothing because the secret is still in git history and every clone.

**Then explain:**
- Scanner: regex rules for known shapes (AWS key id, URL with password, JWT-shaped tokens, private key headers) plus an entropy check on assigned values. All keys here are fake.
- Run result: it found the fake AWS key, the database URL password and the JWT signing key (by entropy). One false positive: a README placeholder ("your-api-key-goes-here-please", entropy 3.51), and a harmless base64 greeting also flagged. One miss: a password built by concatenating two strings in a history diff, which no regex sees.
- Remediation order: (1) revoke and rotate, assume it leaked; (2) rewrite history and invalidate forks, or accept that rewriting is not enough; (3) pre-commit and CI secret scanning; (4) secrets manager and short-lived credentials via roles (Part 10 Q18, Part 7 Q5, Q6, Part 2 Q9 for Docker build secrets).
- Why deleting is not a fix: the secret lives in old commits, clones, CI logs and image layers.
- Failure modes: rotating only the key but not checking logs for use, secrets baked in image layers.

**Example:** JWT signing key leaked: rotating means all tokens signed with it are invalid or forgeable until rotation, so plan token expiry and key rollover.

**Code:**
@@CODE@@

**Output (my run):**
@@OUT@@

**Follow-ups:**
- Entropy threshold? Tune it on your own repo; lower finds more, with more noise. Allowlist known placeholders.
- Is a scanner enough? No. Use it as a net; the fix is not having long-lived secrets.

**Common mistakes:** Deleting the file and moving on. Cleaning history before rotating. Trusting a scanner to catch everything. Putting secrets in env files that get committed.
'''
