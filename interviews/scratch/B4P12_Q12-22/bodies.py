B[12] = r"""
**Say this first (1 line):** Give each role only the actions and resource ARNs its job needs, pin `iam:PassRole` to one named role and one service, and find the real usage from access reports and logs, then replay that usage against the new policy before you remove the old one.

**Then explain:**
- Three roles, three small policies. Training reads `train/` and writes `models/`. Serving only reads `models/`. The CI deploy role creates and updates endpoints and may pass only the serving role to SageMaker (Part 10 Q8 has the training policy in full).
- `iam:PassRole` on `*` is the dangerous one. Whoever can pass any role can hand a job a more powerful role. Pin the Resource to the serving role ARN and add `iam:PassedToService` as a condition. The evaluator below shows the old role passing an admin role and the new CI role failing to.
- Finding real usage without breaking jobs: pull the last-accessed or access-advisor style report, read CloudTrail-style logs for the role, then run policy simulation. Do it over a full cycle (a monthly job, a quarterly retrain), otherwise you cut a rarely used action. Check current docs for how long these reports look back and which services they cover.
- Roll out in steps: add the new policy next to the old one, add alarms on AccessDenied events, then detach the wildcard. Keep a break-glass path. Evaluation order and the three guard rails (boundary, SCP, session policy) are Part 10 Q7 and Part 10 Q30.
- Failure modes: a missing `kms:Decrypt` shows up as an S3 access error; `ListBucket` needs the bucket ARN, not the object ARN; a wildcard `Resource` copied from an example silently re-opens everything.
- What the sketch does NOT model: NotAction and NotResource, policy variables, resource policies beyond the simple cases, KMS grants and key policies, VPC endpoint policies, service-linked roles, real condition operators beyond StringEquals, StringLike and Bool, and the exact cross-account rules. It is a teaching sketch, not the real evaluator; use the provider's simulator for sign-off.

**Example:** The old role allows `s3:*`, `sagemaker:*`, `kms:*` and PassRole on `*`. Logs show the training role used 5 actions, serving 2, CI 3. The new policies cover exactly those. A serving job trying to read `train/` is now an implicit deny (missing allow). Any delete on `models/` is an explicit deny, and an explicit deny wins even over an allow-everything policy.

**Code:** (the evaluator is a copy of `scratch/B4P10_wavea/iam_eval_sketch.py`, unmodified; policies and names are invented)
@@CODE q12_least_privilege.py@@

**Output (my run):** (python3 -I, Python in the b10p10 venv; no cloud, no credentials)
@@OUT 12@@

**Follow-ups:**
- *A job fails after tightening. First move?* Read the AccessDenied event: it names the action and resource. Add exactly that, not a wildcard. Check KMS and the bucket-versus-object ARN first.
- *Why not just use a permissions boundary?* A boundary only caps. It grants nothing. It is a guard rail for delegated role creation, not a substitute for a tight identity policy.
- *How do you keep it tight over time?* Policy as code in git, review, a scheduled access-report job that flags unused actions, and a CI check that fails on `Action: *` or `PassRole` on `*`.

**Common mistakes:**
- Cutting actions based on a one-week log when a job runs monthly.
- Writing `"Resource": "*"` for PassRole "just for CI".
- Forgetting the KMS permission and blaming S3.
- Trusting the sketch for sign-off instead of the real simulator.
"""

B[13] = r"""
**Say this first (1 line):** Set RTO and RPO per asset from the business impact, pick the cheapest recovery that meets each (warm replica for serving, backup for the registry, rebuild for training), and prove it with restore drills, because an untested backup is a hope.

**Then explain:**
- Definitions: RTO is how long you can be down. RPO is how much data you can lose. Invented targets: serving 15 min, registry 4 h, training 2 days.
- Backup versus replication: replication copies mistakes too (a bad delete or a corrupt model replicates in seconds). Backups give you point-in-time. Use both for the registry: versioned artefact bucket plus a metadata DB backup.
- Per asset: *serving endpoint*: warm capacity in a second Region, image by digest, model artefact replicated; rollback as in Part 7 Q12, graceful shutdown as in Part 6 Q38. *Feature store*: online store can be rebuilt from the stream or replicated; offline tables versioned. *Registry*: backups, replicated artefact store, signed models with keys held outside the Region. *Training*: code and configs in git, rebuild elsewhere, restore the data snapshot.
- Hard to rebuild: labels (chargebacks, human reviews), feature history with point-in-time correctness, signing keys and the trust root, and the exact training data snapshot. Protect these first.
- A region failure takes down the dependencies together: the identity service, the registry, the container registry, the secret store, the DNS. Independence in the availability maths is a best case. Cross-cloud sits in Part 11 Q33.
- Restore drills: a scheduled game day that restores the registry and one model to a clean account and serves one request. Record the real time against the RTO. Failure mode: restore works but the signing key or secrets are missing.

**Example:** Three serial dependencies at 0.999, 0.995, 0.999 give 0.993011, about 302 minutes down in 30 days. If the weakest (0.995) has a cache fallback that covers 90 percent of its outages, its effective value is 0.995 + 0.005 x 0.9 = 0.9995 and the chain is 0.997502, about 108 minutes.

**Code:**
@@CODE q13_dr_availability.py@@

**Output (my run):** (python3 -I; the table values are invented design targets, the code only checks they meet the stated targets)
@@OUT 13@@

**Follow-ups:**
- *Why not multi-Region active-active for everything?* Cost and complexity. Only the serving path needs it at 15 minutes; training can wait two days.
- *What does a restore drill prove?* The time, the missing keys, the stale runbook. It is the only evidence for your RTO.
- *Is 0.997502 the real number?* No. It assumes independent failures. A shared Region or shared identity service breaks that.

**Common mistakes:**
- Treating replication as backup.
- Backing up the model but not the labels or the signing key.
- Never running a restore.
- Quoting an availability product without noting the independence assumption.
"""

B[14] = r"""
**Say this first (1 line):** Before any design I ask about the hierarchy, intermittent items, known-future inputs, cold start, the cost of stock-out versus overstock and how planners consume forecasts, and then I size it: 120 million store-SKU cells, a share of them actually ranged, 14 rows per series per day.

**Then explain:**
- Clarifying questions: hierarchy (store, SKU, region) and the level where decisions are made; intermittent items with many zero days; promotions and holidays are known-future inputs, so the platform must supply a future calendar; new SKUs with no history; stock-out cost versus overstock cost (decides a quantile target, not just a mean); who consumes the forecast and how (replenishment system, planner screen).
- Sizing: 3,000 x 40,000 = 120,000,000 cells. Not every store carries every SKU. At an invented 10 percent ranged: 12,000,000 series and 168,000,000 forecast rows a day at 14 days. At 25 percent: 30,000,000 series and 420,000,000 rows.
- Platform cost shape: one global model has the fewest things to run, version and monitor; per-group (invented 12 regions x 4 item classes = 48 models) is a middle path; per-series means 12 million models, with per-model overhead (start, load, register, monitor) dominating. It also kills registry and monitoring tooling.
- Failure modes: rows balloon downstream (storage, join, publish time); cold-start items need a fallback from similar items; a feed delay silently forecasts from stale data (Part 8 Q23).
- Scoring note (10 pts, 6 min; rubric from the part header): about 3 points for clarifying questions and stated assumptions, 3 for correct sizing (120M cells, rows per day), 2 for failure modes and the cost shape, 1 for the runnable check, 1 for a clear 60-second summary. Full marks need the ranged-share assumption said out loud; partial if you multiply 120M by 14 and ignore assortment.

**Example:** 3,000 x 40,000 = 120M. At 10 percent ranged that is 12M series. 12M x 14 = 168M rows per day. With 5.0 fixed units per fit and 0.01 units per series of work (invented), the global model costs about 120,005 units and per-series costs about 60,120,000, roughly 500 times more, almost all fixed overhead.

**Code:**
@@CODE q14_forecast_scale.py@@

**Output (my run):** (python3 -I; abstract units, not prices)
@@OUT 14@@

**Follow-ups:**
- *Why a quantile and not just a mean?* If a stock-out costs more than overstock, plan on a higher quantile. That is a business input from Book 6.
- *When would per-series models be justified?* Few, high-value series where a global model is clearly worse on a backtest. Never as the default at this scale.
- *What do you do for a new SKU?* Borrow from a similar item group until history exists, and flag it as low confidence.

**Common mistakes:**
- Assuming every store carries every SKU.
- Ignoring future inputs like promotions.
- Choosing per-series models without counting the models to operate.
"""

B[15] = r"""
**Say this first (1 line):** Run the nightly batch as freshness check, feature build, score, backtest check, publish with overrides preserved, shard it across workers, and retrain weekly with nightly rescore unless backtests show nightly retraining pays for its compute.

**Then explain:**
- Steps and gates: freshness check (Part 8 Q23 style: stop or flag stale feeds), feature build, train or rescore, backtest on the latest holdout window, publish to a staged table then rename (idempotent, as in Part 6 Q27), apply or carry over planner overrides, notify. The DAG shape is Part 5 Q9. Cost-aware runs (pinned inputs, ephemeral compute, scale down after) are Part 5 Q39.
- Compute trade: with invented 0.02 s per series to train and 0.001 s to score, full nightly retrain costs about 83 core-hours a night versus about 17 to rescore. Weekly retrain plus six rescores is about 183 core-hours a week against 583: relative 0.31.
- Evidence that justifies each: nightly retrain only if a backtest shows rolling-origin error clearly improves with daily refits (fast-moving promo data); weekly retrain if error is flat across the week. Decide on error by item class, not on one average.
- Window: 12 million series cut into 2,400 shards of uneven size. A longest-first scheduler needs 23 workers for full retrain and 5 for rescore to finish inside 4 hours including 0.3 h of fixed steps.
- Failure modes: one giant shard becomes the critical path (skew), a half-written output (use temp then rename), a late feed forecasting from yesterday, overrides lost when a rerun overwrites the table.
- Scoring note (20 pts, 10 min): about 6 for a pipeline that covers the named steps with assumptions, 6 for arithmetic that meets the 4 h window (check the worker count), 4 for failure modes and cost, 2 for the runnable check, 2 for the spoken summary. Partial: a DAG with no window arithmetic, or a worker count that ignores skew.

**Example:** Total work is 12M series x 0.021 s = 252,000 core-seconds = 70 core-hours, plus 2,400 shards x 20 s start-up = 13.3 core-hours: about 83 core-hours. Divided by 23 workers is 3.6 h, plus 0.3 h fixed steps, inside the 4 h window.

**Code:**
@@CODE q15_forecast_schedule.py@@

**Output (my run):** (python3 -I, seeded; the times and unit costs are invented inputs, not measurements)
@@OUT 15@@

**Follow-ups:**
- *Why not just add workers?* Past a point the biggest shard and fixed steps set the floor. Split big shards.
- *Rescore uses a week-old model: is that safe?* Only if the backtest shows error stays flat. Monitor error by class (Q22) and trigger an early retrain when it drifts.
- *What if the feed is late?* Do not silently forecast. Flag, use the last good features with a stale marker, tell planners.

**Common mistakes:**
- One huge job with no shards or retry.
- Overwriting outputs in place with no temp table.
- Retraining nightly because it feels safer.
- Dropping planner overrides on rerun.
"""

B[16] = r"""
**Say this first (1 line):** The platform owns the plumbing around the model call (who may call it, over which network path, how much, what is logged, which version, who pays, what happens when it fails), and Book 2 owns what is said to the model and how answers are judged.

**Then explain:**
- Platform owns: identity and single sign-on, private network path, quota and rate limits, request logging with redaction (Part 8 Q42 boundary), provider model version pinning, cost attribution by team, timeouts and fallbacks. Part 11 Q31 and Part 6 Q34 cover the cloud boundary and the serving side.
- Book 2 owns: prompt design, retrieval and grounding, answer-quality evaluation, and the in-app prompt-injection defences.
- Clarifying questions: data classes in prompts (customer data?), which provider and Region, latency target, peak requests for 5,000 employees, who approves a model version change, what the logs may keep.
- One owner per item is a rule you can check. Two owners means nobody owns it; zero owners is a gap. Failure mode: "both" for logging, then PII sits in logs for a year.
- Scoring note (10 pts, 6 min): about 3 for clarifying questions and assumptions, 3 for a correct split with every item owned once, 2 for failure modes (an item nobody owns, logs with PII), 1 for the runnable validator, 1 for a 60-second summary. Partial: a good list with shared ownership on logging or cost.

**Example:** `prompt_design` listed twice (once platform, once app) is rejected by the validator. Deleting `identity_and_sso` is rejected as a missing required item. An owner named `vendor` is rejected as unknown.

**Code:** (YAML table, then the validator; pyyaml and pydantic)
@@CODE q16_ownership.yaml yaml@@

@@CODE q16_validate.py@@

**Output (my run):** (python3 -I q16_validate.py q16_ownership.yaml; pyyaml and pydantic 2.14.1)
@@OUT 16@@

**Follow-ups:**
- *Who owns cost?* The platform measures and attributes by team key; each team owns its own usage and prompts.
- *Who owns a bad answer?* The app team (Book 2). The platform owns an outage or a leak.
- *What if the provider changes the model version?* Pin the version, test before moving, and keep a rollback route in the gateway.

**Common mistakes:**
- Blurring platform and app ownership so both skip logging redaction.
- Leaving "who approves a version change" unowned.
- Letting every team hold its own provider key.
"""

B[17] = r"""
**Say this first (1 line):** Put one gateway in front of the providers that authenticates teams, gives each a key and a daily token budget, rate-limits, redacts and logs, caches exact repeats, times out and falls back, and routes by version, and let the budget cap warn at 80 percent and block at 100.

**Then explain:**
- Per-team keys and budgets so spend is attributed and one team cannot starve the others. Rate limits protect the provider quota. Budget caps protect money.
- Logging with PII redaction before the log is written (Part 8 Q29 for the privacy tension, Part 8 Q42 for what to monitor). Redact at the gateway, not later.
- Timeouts, then fallback to a second provider or smaller model; caching of exact repeats (same team, same prompt hash); versioned routing so you can pin, canary and roll back a provider model version.
- Not here: prompts, retrieval, model internals (Book 2).
- Daily volume: requests x (input + output tokens). Support: 9,000 x 1,150 = 10.35M tokens against an 11M budget. Analytics runs at 126 percent of its budget.
- Failure modes: a cache that crosses team boundaries leaks data; a retry storm during an outage; a hard block at 100 percent on a critical team with no override path; logs that store raw prompts.
- Scoring note (20 pts, 10 min): about 6 for a gateway design covering keys, budgets, limits, logging, fallback, cache and routing with stated assumptions, 6 for correct token arithmetic and cap behaviour at 80 and 100 percent, 4 for failure modes (cross-team cache, retry storms, PII), 2 for the runnable check, 2 for a 60-second summary.

**Example:** Analytics plans 1,200 requests of 2,100 tokens: 2.52M against a 2.0M budget. In the run it was alerted when it crossed 80 percent (1.6M), then blocked with a 429 near 2.0M, overshooting by one request at most.

**Code:** (invented rates and budgets; no network, no real provider)
@@CODE q17_gateway.py@@

**Output (my run):** (python3 -I, seeded)
@@OUT 17@@

**Follow-ups:**
- *What at 100 percent for a critical team?* A documented override with approver and expiry, or route to the cheaper model, not silent unlimited spend.
- *Why cache per team?* Prompts can hold team data; a shared cache is a cross-team leak.
- *Retries during a provider outage?* Bounded, with jitter and a circuit breaker (see Q23).

**Common mistakes:**
- One shared key for all teams.
- Redacting after logging.
- Budget enforced monthly only, so one bad day burns it.
- Caching with no team or version in the key.
"""

B[18] = r"""
**Say this first (1 line):** Before choosing on-device, edge gateway or cloud I ask what must work offline, the size, latency, battery and memory limits, privacy, update cadence and how we learn about errors without uploading photos, then I size the update: 60 MB at 2 Mbps is 4 minutes ideal, 6,000 GB for the fleet.

**Then explain:**
- Questions: what must run with no signal; model size and latency limits on the lowest-end phone; battery and memory; are photos allowed to leave the device; how often the model changes; how errors reach us (aggregate counters, user-flagged samples with consent, on-device confidence histograms); when a server fallback is allowed.
- Comparison table below.
- Update arithmetic: 60 MB x 8 = 480 megabits; at 2 Mbps that is 240 s = 4.0 min ideal, 6.7 min at an invented 60 percent link efficiency. 60 MB x 100,000 = 6,000 GB per full rollout. Storage keeps a few versions only; egress dominates, so use delta patches, a CDN, Wi-Fi-only and charging-only downloads, resumable chunks.
- Failure modes: a drop mid-download without resume restarts (toy run: 1.38x bytes versus 1.01x resumable); a bad model reaching every phone at once (staged rollout, Q19); a model that outgrows low-end memory; no telemetry so errors are invisible.
- Scoring note (10 pts, 6 min): about 3 for clarifying questions and assumptions, 3 for the comparison and correct update arithmetic, 2 for failure modes and privacy, 1 for the runnable check, 1 for a 60-second summary.

| Option | Good for | Cost and limits | Privacy |
|---|---|---|---|
| On-device | offline, low latency, no per-call server cost | small model, update logistics, device variety | data stays on phone |
| Edge gateway (site box) | shared site, bigger model, some offline | hardware to run and patch | data stays on site |
| Cloud | biggest model, easy update | needs signal, per-call cost, latency | images leave device |

**Example:** 100,000 devices x 60 MB = 6,000 GB. A 25 percent delta patch is 1,500 GB and 1 minute a device at 2 Mbps. With invented 1 unit per GB sent and 1 per GB-month stored (not real prices), a full rollout is 6,000 units and five stored versions are 0.30 units a month.

**Code:**
@@CODE q18_ota.py@@

**Output (my run):** (python3 -I, seeded; abstract units; the drop model is a toy)
@@OUT 18@@

**Follow-ups:**
- *Server fallback when offline?* Queue the photo with consent and sync later; never block the inspector.
- *How do you see accuracy without photos?* Confidence histograms, user corrections, and a small consented sample.
- *Update cadence?* Only as often as accuracy gain justifies the bytes; staged rollout.

**Common mistakes:**
- Forgetting egress is the cost, not storage.
- Pushing the update over mobile data without a Wi-Fi rule.
- No rollback path on the device.
"""

B[19] = r"""
**Say this first (1 line):** Export to ONNX, quantise, check accuracy on a held-out set against a gate, measure size and latency on a reference device profile, sign the artefact, roll out in stages and keep the previous model for rollback.

**Then explain:**
- Path: train, export with dynamic axes (Part 6 Q10), dynamic int8 quantisation (Part 6 Q29), accuracy gate, device measurement, sign, staged rollout, rollback. Export failures (unsupported operators, tracing issues) are Part 6 Q42.
- My run: a small MLP on synthetic data. int8 file is 0.25 of the fp32 size, accuracy change -0.0005, prediction agreement 0.9985. The gate here is a drop of at most 0.01.
- Latency lesson: sandbox timings are noisy and say little. Two runs of this same script gave fp32 times of 5.8 ms and 20.7 ms, and int8 was slower than fp32 in one and faster in the other. Dynamic quantisation does not always speed things up, and these are sandbox CPU timings, not device numbers; measure repeated runs on the real device profile.
- Signing: a manifest with the file hash and version, signed. The demo uses an HMAC with a fake key; production uses a KMS or HSM-held key or an asymmetric signature and a public key baked into the app. The device verifies before loading. A one-bit change in the file fails verification.
- Failure modes: accuracy fine overall but worse on one slice; unsupported operator on an old runtime; a model that loads but runs out of memory on the low-end phone; unsigned models; rollout to everyone at once.
- Scoring note (20 pts, 10 min): about 6 for the packaging path with assumptions, 6 for correct size, accuracy and latency evidence with a stated gate, 4 for failure modes (slices, runtime, signing), 2 for the runnable check, 2 for the summary.

**Example:** fp32 1,291 KiB, int8 329 KiB. Accuracy 0.9395 versus 0.9390, so the drop is 0.0005, under the 0.01 gate: pass. Ship to 1 percent of devices, watch crash and latency counters, then 10, 50, 100 percent.

**Code:** (torch, onnx, onnxruntime from the b6p06 venv; versions in the output; fake HMAC key)
@@CODE q19_onnx_quant.py@@

**Output (my run):** (python3 -I; the first line is a library warning about pre-processing, harmless here)
@@OUT 19@@

**Follow-ups:**
- *Quantisation hurt one class: what now?* Per-slice gate fails; try per-channel or quantisation-aware training (Book 1), or skip it for that layer.
- *Why sign if the app store signs the app?* The model is a separate download; the signature protects that channel.
- *Rollback on a device?* Keep the last good model file and switch back on a crash-loop or health flag.

**Common mistakes:**
- Quoting sandbox timings as device latency.
- Checking only overall accuracy.
- Shipping an unsigned model file.
- Rolling out to 100 percent at once.
"""

B[20] = r"""
**Say this first (1 line):** Retraining daily on clicks the model caused teaches it its own habits, so I keep a small unpersonalised holdout, A/B test every change against it, gate retrains on checks, and roll back on the business metric (watch time) not only the offline one.

**Then explain:**
- Exposure bias and the loop (Part 8 Q33): the model only gets feedback on items it showed, so it keeps showing old winners and never learns about new or unseen items. The in-loop metric can look fine because users do click what you show.
- Clean baseline: a small slice (5 to 10 percent) gets random or non-personalised content, so clicks on it are unbiased. Use it for evaluation and for a fair A/B comparison (Part 6 Q13).
- Safe daily retrain gates (Part 7 Q10 promotion gates, Part 7 Q26 shadow and canary): data checks, an offline floor, a holdout-based check, shadow, then a canary with abort rules on watch time and latency.
- Rollback (Part 7 Q12): if offline AUC rose and watch time fell, trust the online result. Move the registry alias back to the last good model; keep the previous artefact and features available.
- Failure modes: holdout too small to read; holdout contaminated by the personalised model; retraining on a bad week; popularity lock-in; creator unfairness from a rich-get-richer loop.
- Scoring note (30 pts, 12 min): about 9 for clarifying and stated assumptions (what is the objective, how big is the holdout, what labels exist), 9 for a design with gates and rollback that fits the numbers, 6 for failure modes (loop, contamination, drift), 3 for the runnable simulation, 3 for the 60-second summary.

**Example:** In the run the main-traffic CTR stayed between about 0.43 and 0.47 for days 15 to 40, while the model's slate scored only about 0.77 of the best well-measured holdout items, and fresh items were 0 percent of main impressions versus about 25 percent of holdout impressions. The in-loop metric hid the problem; the holdout showed it.

**Code:** (numpy; catalogue churn 4 percent a day, naive model ranks by total clicks)
@@CODE q20_feedback_loop.py@@

**Output (my run):** (python3 -I in the b6p06 venv with numpy; seeded; day 5 fresh share reads 100 percent only because every item is still under 7 days old at the start)
@@OUT 20@@

**Follow-ups:**
- *Is the holdout free?* No. It costs a little engagement. Keep it small and rotate users.
- *What alert rule?* Holdout ratio below 0.8 for 5 days, or watch time down in the canary.
- *Fix for the loop itself?* Exploration, new-item boost and debiasing are modelling work in Book 1; the platform supplies the holdout and gates.

**Common mistakes:**
- Evaluating the new model on logs the old model produced.
- Using only the offline metric to promote.
- A holdout so small it cannot be read.
- No way to roll back features along with the model.
"""

B[21] = r"""
**Say this first (1 line):** Log every decision with inputs, versions, score, reason codes, overrides, who and when into an append-only hash-chained log, keep personal data minimal and encrypted, test that reason codes are stable, and produce a slice report each release.

**Then explain:**
- Per decision: a hashed applicant reference (not the raw id), model version, feature-set version, score, decision, reason codes, override with who, why and when. Overrides are new appended records, not edits. Part 8 Q29 covers the audit versus minimisation tension: log what an auditor needs, store identifiers hashed or in a separate access-controlled store, and set retention to the rule you were given (check the regulator's current text; the length is a policy decision, not a number I invent).
- Protection: encryption at rest, role-based read access, write-once storage, and the chain head hash anchored somewhere else (a separate account or a signed daily checkpoint).
- Tamper evidence: each record hashes the previous hash plus its own content. Edit, delete or reorder any record and the verifier reports the first bad row. Limit: editing and re-hashing the last row is only caught if the head hash is anchored elsewhere. It is tamper-evident, not tamper-proof.
- Reason codes: here the top points lost against a reference applicant; test stability under small input noise (100 percent unchanged in the run, gate at 95). Check the real method with legal and model-risk teams.
- Fairness slice report each release (Part 7 Q27 gate, Part 8 Q28 monitoring): approval rate by slice and the ratio; run showed 52.2 percent versus 58.5 percent, ratio 0.89. The four-fifths figure is a rule of thumb, not a legal test.
- Regulation: RBI FREE-AI (13 Aug 2025) coverage mentions board-approved policy and AI-specific audit; check the regulator's site for current text. I have not read the primary text.
- Scoring note (30 pts, 12 min): about 9 for clarifying and assumptions (retention rule, who reads logs, what a reason code must satisfy), 9 for a log design that is auditable, minimal and protected, 6 for failure modes (tail rewrite, PII in logs, unstable reasons), 3 for the runnable chain and tamper test, 3 for the summary.

**Example:** Row 7 edited and only that row re-hashed: the verifier flags row 8 (its stored prev no longer matches). Row 100's decision flipped: flagged at 100. Row 50 deleted: flagged at 50. Last row edited: flagged at 399 only because the chain head is known here.

**Code:** (invented scorecard and applicants; stdlib only)
@@CODE q21_decision_log.py@@

**Output (my run):** (python3 -I, seeded)
@@OUT 21@@

**Follow-ups:**
- *Where do you keep the head hash?* In a separate account or a signed periodic checkpoint.
- *Customer asks for erasure?* Log hashed references and keep a legal-hold rule; handle with privacy counsel.
- *Reasons changed after a release?* The stability test should have failed the gate; keep the version in each record to explain old decisions.

**Common mistakes:**
- Logging raw personal data "for audit".
- Editing records in place for an override.
- No head anchoring.
- Reason codes never tested for stability.
"""

B[22] = r"""
**Say this first (1 line):** Track WAPE and bias by hierarchy level and item class, separate model error from feed errors with freshness and volume checks, keep override history, and measure forecast value added so you only keep human review where it beats the model.

**Then explain:**
- Error by level and class: item-level WAPE (sum of absolute errors over sum of actuals) hides errors that cancel at the total. In the run the portfolio total was off by 10.1 percent while item-level WAPE by class ranged from 4.8 to 57.8 percent. Report at the level where decisions are made.
- Bias: sum of (forecast minus actual) over actuals. Negative means under-forecast. Promo items were at about -25 percent: a systematic miss, a feature problem, not noise.
- Model error versus data error: check freshness and row counts first (Part 8 Q23), then input drift (Part 8 Q8 for late labels), then model. A flat zero day from a broken feed is not a model failure.
- Override history: store the model forecast, the override, who, when and why, and the actual. Without it you cannot measure whether overrides help. Incident handling for sudden misses is Part 8 Q34.
- Forecast value added: error of the model minus error of the final forecast on the same overridden items. Positive means the human helped. Only judge FVA with enough overrides; 1 override tells you nothing (the table says so).
- Decision: automate classes where overrides do not help or are rare and the model is accurate and unbiased (fast movers); keep review where FVA is positive but fix the model cause (promo bias). Failure modes: planners override because they distrust a biased model; FVA computed after they saw the actual; small samples.
- Scoring note (30 pts, 12 min): about 9 for clarifying and assumptions (what the override rate means, level of decision), 9 for correct WAPE, bias and FVA and a defensible automate decision, 6 for failure modes (cancelling, leakage, small n), 3 for the runnable table, 3 for the summary.

**Example:** For two items with actuals 100 and 120 and forecasts 104 and 112, WAPE is (4 + 8) / 220 = 5.45 percent (an assert in the code). Promo overrides cut error from model to final by 19.5 points on 3 items: positive FVA, but the -25.5 percent bias says fix the model.

**Code:** (invented, seeded table of 50 items, 5 overridden, which is 10 percent of the invented 12 percent)
@@CODE q22_forecast_governance.py@@

**Output (my run):** (python3 -I)
@@OUT 22@@

**Follow-ups:**
- *Why WAPE and not MAPE?* MAPE blows up on zeros and tiny actuals; WAPE weights by volume.
- *Should you ban overrides?* No. Measure them, require a reason, and drop them where FVA is not positive.
- *How do you know it is the feed?* Freshness, row-count and null-rate checks fire before the error metric does.

**Common mistakes:**
- Reporting only the top-level error.
- Judging override value with 1 or 2 overrides.
- Not saving the pre-override model forecast.
- Treating a biased class as noise.
"""
