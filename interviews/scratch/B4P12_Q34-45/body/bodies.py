B = {}
B[34] = """**Say this first (1 line):** This team is at level 0 on every dimension; I would not buy a platform, I would fix one gap per quarter, starting with the registry because nothing else can be audited without it.

**Then explain:**
- Google-style levels (as widely described, check the original): level 0 manual, level 1 pipeline automation and continuous training, level 2 CI/CD for the pipeline itself. The Microsoft-style five-level view is only known to me secondhand, so I use it as a vocabulary (ad hoc, repeatable, automated, measured, optimised), not as a standard.
- Assessment: notebook training = level 0, manual deploys = level 0, spreadsheet monitoring = level 0, shared-folder registry = level 0. Roadmap: Q1 registry plus a reproducible training script plus a first test (Part 4, Part 1), Q2 one CI deploy job (Part 7 Q9) plus three automated monitoring checks (Part 8 Q2) plus data versioning. Pipelines (Part 5) come after, when the script already works from one command.
- Leading indicators beat lagging ones: share of prod models with a registered version, minutes to reproduce last month's model, manual deploys per month, time to detect a bad input.
- Failure modes: scoring the team once and never again; buying Kubeflow or a feature store at level 0; metrics that people game (counting registered models that nobody deploys from).
- Scoring note [Not a timed set]: full marks need a concrete smallest step per quarter with an indicator; partial for a list of tools with no order.

**Example:** My invented rubric scores six dimensions 0 to 2, so the maximum is 12. Level 1 starts at half the points (6 of 12). Each roadmap step lifts one dimension from 0 to 1. After six steps the score is 6/12 and the level flips from 0 to 1, as the output shows. No step needs new infrastructure beyond a tracker and one CI job.

**Code:** run with `python3 -I q34.py`. Rubric weights and thresholds are invented for the interview.
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *When do you stop?* When the next gap costs more than the incidents it prevents; maturity is a means, not a goal.
- *Is level 2 needed everywhere?* No. A quarterly batch model rarely needs continuous training.
- *How do you get buy-in?* Tie each step to a named pain (late detection, unreproducible model) with its indicator.

**Common mistakes:**
- Treating a maturity level as a target for all models.
- Starting with tools rather than the pain.
- No indicator, so nobody can say the quarter worked.
"""
B[35] = """**Say this first (1 line):** First stop the bleeding with a rollback or a rules-only fallback, then diagnose; decide fail-open or fail-closed per transaction class ahead of time, and prove the switch works by drilling it every month.

**Then explain:**
- Detect (Part 8 Q43): an alert on the false-positive proxy (block rate, step-up rate, complaint calls) against a baseline for that hour; a tripled block rate should page, not wait for the morning report.
- Contain (Part 7 Q12): roll back the nightly feature job or flip to the rules-only mode. Prefer the one that is already tested; a mode never drilled is a gamble at 02:10.
- Diagnose: compare feature distributions before and after the job change, check schema and late-arriving data, and training-serving skew (Part 9 Q7, Part 9 Q31). Look first at what changed, not at what looks odd.
- Fail-open versus fail-closed per class: low-value card-present may fail open (allow), high-value or card-not-present should fail to step-up authentication. State the loss trade-off and who signed it off.
- Communicate: one incident channel, an owner, a status line every 30 minutes, a note to the fraud-ops and customer-support leads. Blameless follow-ups: add a canary on the feature job, a schema contract, a drill calendar.
- Cost angle (abstract units): cheap controls with a big avoided loss win (rollback, drill, shadow rules); a second region for this one failure is poor value.
- Scoring note [Set F, Q4 of 4, 12 min, 40 pts] per the part rubric: about 12 pts for clarifying and stated assumptions (what is the fraud and block baseline, who owns false positives), 12 for a timeline that actually contains and fixes it, 8 for failure modes and cost, 4 for the runnable check, 4 for the 60-second summary. Partial: a diagnosis list with no containment order.

**Example:** At 02:10 the block rate on genuine transactions goes from near zero to all of them because a feature now arrives as a constant. Step one: switch to rules-only. In my toy run, rules-only gives 0.0 false positives on the same genuine traffic, while the broken model gives 1.0. A 100 transaction with the model down is allowed (fail-open); a 15,000 one is stepped-up (fail-closed).

**Code:** run with `python3 -I q35.py`. Toy rules and scores; sandbox only.
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *Why drill monthly?* Fallback code rots; the drill is the test that it still works, and the freshness check pages the owner when it lapses.
- *Who decides fail-open?* Risk and the business owner, written down in advance, not the on-call engineer at night.
- *Rollback or fallback first?* Whichever is already tested and fastest; both are in the runbook.

**Common mistakes:**
- Debugging the model while the bad decisions continue.
- One global fail policy for all transaction types.
- A fallback nobody has run since it was written.
"""
B[36] = """**Say this first (1 line):** At 10x the first things to break are usually feature-store reads and logging volume, so I cache, precompute and shrink before buying more GPUs, and I go back to product for candidate count and refresh frequency when the cost curve stays steep.

**Then explain:**
- What breaks first: hot keys and read throughput on the feature store (Part 9 Q35), then ranking compute per request (candidates times model cost), then embedding refresh time, then log volume and its storage. In my toy model the feature reads dominate.
- Levers: cache popular feature reads, precompute user and item embeddings on a schedule, shrink the candidate set (500 to 200), sample logs but keep full logs for a trace percentage.
- Test before launch (Part 6 Q16): replay a load profile at 10x in staging, watch tail latency and saturation, and repeat the test after each lever. Autoscaling limits and quotas (Part 3 Q36) must be checked too.
- Keep cost per thousand requests flat: report it as a metric with a target, review per release.
- Stop optimising when the next saving hurts relevance; then negotiate: fewer candidates, slower refresh for cold users, smaller feed page. Numbers in this model are invented abstract units.
- Failure modes: cache hit rate collapsing after a catalogue refresh, stale embeddings after a skipped refresh, logging so heavy it becomes the top cost.
- Scoring note [Set R, Q4 of 4, 12 min, 40 pts]: about 12 for stated assumptions and a bottleneck order, 12 for levers that fit the numbers, 8 for failure and cost trade-offs, 4 for the model, 4 for the summary. Partial: only 'add more GPUs'.

**Example:** My model charges 20 feature reads per request. At 10x with a naive setup the cost per 1k requests is 1.36 times today (extra shard overhead, invented). A 60 percent cache hit rate cuts reads by 60 percent, cutting candidates from 500 to 200 cuts ranking cost by 60 percent. The final line is 0.55 of today's cost per 1k.

**Code:** run with `python3 -I q36.py`. All unit costs are invented abstract units, not prices.
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *Which input is the model most sensitive to?* Feature read cost (+50 percent gives 1.465x), so that is where to spend effort first.
- *Why not just scale out?* Cost per request would rise, and some stores have hot-key limits that scale-out does not fix.
- *What do you tell product?* The cost of each extra candidate and each refresh, so they choose.

**Common mistakes:**
- Optimising the model when logs or reads dominate.
- Load-testing only the ranker, not the feature store.
- Quoting a single average cost with no sensitivity.
"""
B[37] = """**Say this first (1 line):** I present one governed path from data zone to decommissioning, and I answer the examiner with evidence I can produce on demand: reason codes for a decline, a tamper-evident change log, and a signed independent validation.

**Then explain:**
- Design in order: restricted data zone with residency tags and customer-managed encryption keys; feature store with single definitions (Part 4 Q25 style lineage); training that records data hash, code commit and seed; independent validation in a separate team; registry with approvals (Part 4 Q29); deployment behind authentication on a private network; monitoring; an append-only audit log; a retirement checklist. Cloud depth is in Part 10 Q39 and Part 11 Q35. Regulatory points (RBI model-risk and localisation expectations) are from adviser summaries: check the regulator's site and current law.
- Probe 1, why declined: store reason codes with each decision and the model and feature versions; I show the top negative contributors. Probe 2, who changed prod last quarter: query the hash-chained promotion log and show the chain verifies. Probe 3, independent validation: show the signed validation memo from a person outside the build team, linked to the model version.
- Failure modes: reasons not stored at decision time, registry edits outside the log, validator who reports to the builder, a retired model still scoring.
- Scoring note [Set C, Q4 of 4, 15 min, 40 pts]: about 12 for scoping assumptions (who the examiner is, which decisions are covered), 12 for a design with the controls, 8 for failures and residency, 4 for the table check, 4 for the summary. Partial: architecture drawn, but no evidence for the probes.

**Example:** Each asset in the table must name a control and the evidence that proves it. The checker fails a row with no evidence, such as 'shadow notebook copy'. The chain probe shows two promotions in my toy log; after I edit one record, verification returns False.

**Code:** run with `python3 -I q37.py`. Rows and logs are invented.
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *Is a hash chain enough for audit?* It shows tampering, not who is trusted; anchor the head hash somewhere the platform team cannot write.
- *How do you explain a complex model?* Reason codes from an approved method plus a documented limitation, agreed with validation.
- *Decommissioning?* Revoke keys, delete endpoints, archive artefacts per retention policy.

**Common mistakes:**
- Evidence assembled after the examiner asks.
- Same person builds and signs off.
- Forgetting the retired model.
"""
B[38] = """**Say this first (1 line):** I tier the series, spend compute where stock-out cost is high, and judge each cost-cut policy on expected extra stock-out cost, not forecast error alone.

**Then explain:**
- Tiering: A items (fast-moving, high value) keep the best model and frequent retraining; B items retrain less often; the long tail uses a cheap or global model. Reference Part 5 Q39 for orchestration at this scale and Part 6 Q43 for batch serving.
- Other levers: reuse a global model across series, sample series for backtests, warm-start instead of training from scratch, skip retraining when drift checks pass.
- Measurement: backtest each policy on stock-out and holding cost, per tier. The 40 percent target is checked on compute, the harm on the cost of misses.
- Failure modes: the long tail sums to a big revenue share, new items with no history, promotions and seasonality breaking a skipped retrain.
- Scoring note [Set D, Q4 of 4, 12 min, 40 pts]: about 12 for assumptions (tier shares, service-level target), 12 for policies that meet the target, 8 for risks, 4 for the table, 4 for the summary. Partial: cost cut with no harm measurement.

**Example:** Invented table: 2,000 A, 8,000 B, 40,000 C series; every series costs 10 units a run, 4 runs a month, so 2,000,000 units. P2 moves only the tail to a cheap model: it saves 68 percent and adds a small stock-out cost (4,000 units, mostly in the tail). P1 saves 50 percent but adds 18,400 because it also slows the A items. P3 saves 82 percent for 8,200 extra. All three clear 40 percent, so I pick the one with the smallest harm: P2. Compute and stock-out units must be converted by finance before comparing them in one currency; here they stay abstract.

**Code:** run with `python3 -I q38.py`. Everything is invented.
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *What if leadership insists on more than 40 percent?* Show the marginal stock-out cost per extra point saved; P3 is the next step.
- *How do you detect harm after launch?* Track stock-outs per tier with an alert against the backtest.
- *New products?* Keep them in the high tier until they have history.

**Common mistakes:**
- Cutting uniformly across all series.
- Judging by MAPE only.
- No rollback path for the policy.
"""
B[39] = """**Say this first (1 line):** I assume the model can be tricked, so the platform limits what a tricked model can reach: user identity on retrieval, narrow tool scopes, redaction and egress limits, and an audit trail with an owner for every threat.

**Then explain:**
- Threats (Book 2 owns injection technique; OWASP LLM Top 10 2025 entries as summarised by commentators, check the current list): prompt injection through retrieved HR text, over-broad tool permission, exfiltration through logs and answers, cross-user retrieval leak, key theft, supply-chain risk in models and libraries.
- Controls: identity-propagated retrieval so the search filters by the caller's groups; the ticket tool can only create tickets, with the user's identity; output filtering and an egress allow-list; redaction before logging; short-lived keys in a secret manager; pinned and scanned dependencies. See Part 10 Q42 and Part 11 Q31 for the cloud mechanics.
- Failure modes: an ACL filter applied after ranking instead of before, logs that keep full prompts, a tool with a write scope 'just in case'.
- Scoring note [Set L, Q4 of 4, 12 min, 40 pts]: about 12 for scoping and assumptions, 12 for a table where each threat has a control, 8 for residual risk and cost, 4 for the check, 4 for the summary. Partial: controls listed with no owner.

**Example:** Documents d1 (HR only), d2 (everyone), d3 (payroll). An HR user should retrieve d1 and d2, never d3; the test asserts exactly that. A row with an empty control and owner is rejected by the validator.

**Code:** run with `python3 -I q39.py`. Table and ACL data are invented.
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *Can you filter injection out?* Not reliably; design so success of the injection has limited reach.
- *Who owns each row?* One named team, reviewed quarterly.
- *Hosted model data use?* Check the provider's current terms and retention settings.

**Common mistakes:**
- One shared service identity for all users.
- Relying on the system prompt as a security control.
- Threat list without owners.
"""
B[40] = """**Say this first (1 line):** Anything shipped to a device can be extracted, so I protect the update channel with signatures, keep high-value models on the server, and rate-limit the fallback API per attested device.

**Then explain:**
- Model protection and its limits: obfuscation and encryption slow an attacker but the model must be decrypted to run; hardware key stores raise the bar; a model whose theft is costly stays server-side. Be honest: no on-device scheme is unbreakable.
- Update channel: sign a manifest holding the version and the file hash with a private key held in a key service; the app ships only the public key. See Part 7 Q32 for model signing in CI and Part 6 Q39 for edge deployment.
- App attestation (concept only, check platform docs): the platform vouches that the request comes from a genuine app on a genuine device; use it to gate the fallback API with per-device quotas.
- Cost: telemetry and updates across 100,000 devices; delta updates and sampling cut traffic.
- Failure modes: replay of an old valid manifest (rollback attack), key leakage, a cloned app burning the fallback budget.
- Scoring note [Set E, Q4 of 4, 12 min, 40 pts]: about 12 for threat assumptions, 12 for a layered design, 8 for limits and cost, 4 for the signature check, 4 for the summary. Partial: 'encrypt the model' as the only answer.

**Example:** A good manifest is accepted. A model file with one extra byte is rejected by the hash. An edited manifest (version changed) is rejected by the signature. An old valid manifest still verifies, so the app must also require a version above the installed one. The key here is generated in memory for the demo (a fake key, not a real one).

**Code:** run with `python3 -I q40.py` (uses the `cryptography` package, version 50.0.1 here; HMAC from the standard library works if you share a secret, but then devices can forge).
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *HMAC or Ed25519?* Ed25519: devices hold only the public key, so they cannot forge updates.
- *Can you stop extraction?* No, only raise cost; watermark outputs and monitor API abuse.
- *Telemetry cost?* Sample, batch, compress; send aggregates.

**Common mistakes:**
- Embedding the signing key in the app.
- Verifying the signature but not the version.
- Unlimited fallback API per install.
"""
B[41] = """**Say this first (1 line):** I decide by capabilities, team size, compliance fit and exit cost first, then compare three-year relative cost with sensitivity, and pilot the managed option on one real model before committing.

**Then explain:**
- Framework: required capabilities (registry, pipelines, serving, monitoring), team size and skills, lock-in (Part 11 Q32), compliance and residency fit (Part 10, Part 11), total cost including upgrades, on-call and people time, an exit plan, and what would change the decision.
- Cost shape in my toy model: build has low per-model cost but high people cost; managed has higher per-model cost and low people cost; buy adds a licence. With few models and a small team, managed wins; with many models, build overtakes.
- Failure modes: counting build cost without maintenance and on-call, ignoring that the platform team is also a product team, picking a tool the compliance team cannot approve.
- Pilot first: one model end to end on the managed platform, measuring time to first deploy, audit evidence available and team hours.
- Scoring note [Not a timed set]: full marks need criteria plus a computed comparison with sensitivity; partial for a pros-and-cons list.

**Example:** Read the output: at 20 models and 4 people, build is cheapest in the toy numbers (81.0 vs 84.5); at 8 people managed wins. At 400 models build wins at every team size shown. No real prices were used; all values are abstract units.

**Code:** run with `python3 -I q41.py`.
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *What changes your mind?* A region or compliance restriction, a big jump in model count, or a vendor price change (check current terms).
- *Exit plan?* Keep artefacts and metadata in open formats and test an export.
- *Hybrid?* Managed training and registry with your own serving is common; check lock-in per layer.

**Common mistakes:**
- Comparing licence cost with engineer time only.
- No sensitivity analysis.
- Ignoring on-call.
"""
B[42] = """**Say this first (1 line):** Measure what is actually read and by whom, delete the unused first, declare the undeclared consumers before touching anything they depend on, and add tests so deletion cannot silently break a model.

**Then explain:**
- Audit measures: feature read counts by consumer, features with no reader, consumers not in the declared list, config files per pipeline, pipeline stages with no owner, last retrain date. Ideas follow Hidden Technical Debt in ML Systems (Part 1 Q39); I did not open the paper here, so I describe them in my own words.
- Prioritise by risk times cost: an undeclared consumer on a critical feature is high risk; 600 unused features are low risk but cost storage and compute.
- Delete order: unused features first (in batches, with a one-release grace period), then duplicate config, then glue code; never delete a feature with an undeclared reader until the reader is declared.
- Protect: golden-set prediction test before and after each deletion, a data contract per feature, a retrain drill so the model is no longer one nobody dares retrain.
- Scoring note [Not a timed set]: full marks need a risk-ordered plan and the regression guard; partial for a general 'clean up' list.

**Example:** 20 invented features: 8 are read by someone, 12 are unused. Feature f003 is read by `promo_svc`, which is not a declared consumer, and f011 is read by two undeclared consumers. Deleting f003 would have broken promo_svc silently.

**Code:** run with `python3 -I q42.py`.
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *How do you find undeclared consumers?* Read logs or access logs on the store, not documentation.
- *Retrain fear?* Retrain in shadow, compare to the golden set, then promote.
- *Where to start?* Where an outage would hurt most.

**Common mistakes:**
- Deleting by name or guess.
- No grace period.
- Fixing code but leaving the lineage table stale.
"""
B[43] = """**Say this first (1 line):** I pick the design by the loss I can accept: active-active loses least but costs headroom and needs a residency check, active-passive is cheaper but slower to recover, per-region independent has no stale state but no cover for a region's users.

**Then explain:**
- Active-passive: warm standby, async replication; recovery time includes detection and switch (Part 11 Q33 for cross-cloud and Region concepts, Part 6 Q38 for serving rollout). Stale window equals replication lag.
- Active-active: both Regions serve; the failed Region's half sees errors until health checks react; features replicated asynchronously.
- Per-Region independent: no cross-Region state so no lag, but a Region loss takes its users down unless traffic can move.
- State: feature store replication and its lag (Part 9 Q32), registry artefacts copied ahead of time, decision log per Region with a merge for audit. Residency may forbid replicating some data to another Region; check the law and your policy.
- Test failover on a schedule; a plan never exercised is not a plan. Idle capacity is the cost of the faster designs.
- Scoring note [Not a timed set]: full marks need the three designs, the numbers from the simulation and the residency caveat; partial for a table with no consistency discussion.

**Example:** At 200 decisions per second: with 150 s to detect and switch, active-passive loses 30,000 requests (200 x 150); active-active loses 3,000; per-Region independent loses half the traffic for the assumed 1 hour outage (360,000) because no one covers the failed Region. Stale windows come from lag, with seeded jitter.

**Code:** run with `python3 -I q43.py`. The model is a hand-made simplification with invented timings, sandbox only.
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *Fail-open during failover?* Same per-class rule as the fraud incident.
- *Why keep decision logs per Region?* Residency and independence; merge later for audit.
- *How often to test?* Per quarter at least; more often for critical services.

**Common mistakes:**
- Assuming replication is instant.
- Forgetting the registry and secrets in the DR Region.
- Never running the failover.
"""
B[44] = """**Say this first (1 line):** I give each agent its own identity with the smallest scopes, make write actions go through human approval, and enforce those limits in the platform, not in the prompt.

**Then explain:**
- Boundary: per-agent identity and scopes (Part 10 Q3, Part 10 Q8), human approval for write actions, sandboxed code execution, egress allow-lists, secrets never placed in the model context, rate and spend limits, audit logs of every tool call (Part 11 Q31 for the other clouds' equivalents).
- Technique of injection is Book 2; here I only assume the agent may be steered, so its credentials cannot do harm.
- Failure modes: one shared service identity for all agents, tools with wildcard actions, a secret pasted into a prompt or a log, approval fatigue (users click yes always).
- Evaluator limits: my sketch handles allow, deny, wildcards, boundaries, SCPs and session policies; it does not model NotAction, policy variables or all cross-account rules. Check current docs and use a real policy simulator for production.
- Scoring note [Not a timed set]: full marks need identities, approval, egress and audit plus a demonstrated denial; partial for 'be careful with prompts'.

**Example:** The read-only agent role can GetItem but PutItem is denied (nothing allows it). After approval a separate role may PutItem. DeleteItem is denied for both because the boundary does not include it; an explicit deny guard beats even a broad allow.

**Code:** run with `cd code && python3 -I q44.py`; it imports an unmodified copy of `scratch/B4P10_wavea/iam_eval_sketch.py` kept next to it. Account id and table are fake.
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *Who approves?* The data owner for that action; log approver and request.
- *Spend limit?* A per-agent budget with a hard stop and an alert.
- *Sandbox?* No network except the allow-list, short-lived, no host mounts.

**Common mistakes:**
- Wildcard tool permissions.
- Approval that cannot be audited.
- Putting secrets in context.
"""
B[45] = """**Say this first (1 line):** Cost per prediction is compute (including the idle share) plus storage, transfer, monitoring and people time divided by predictions; I forecast it with growth and a spike, alert on both budget and anomaly, and leave value to the Book 6 owner.

**Then explain:**
- Inputs per model: predictions, compute per thousand, idle share, storage, transfer, monitoring, people. Idle capacity is paid and spread over used predictions (Part 10 Q44 for cost levers on AWS, Part 8 Q39 for the monitoring cost).
- Low-volume models look expensive per prediction because fixed costs dominate (m4 in my run); that is a signal, not an error.
- Alerts: a budget threshold (monthly budget plus a margin) catches slow creep; an anomaly rule (against a trailing mean) catches spikes early.
- 'Is it worth it?': ask the product owner for value per prediction or per outcome (Book 6), then compare. The platform team supplies cost, not value.
- Failure modes: allocating shared platform cost unfairly, forgetting people time, forecasting growth with no spike case.
- Scoring note [Not a timed set]: full marks need the unit-cost build-up, forecast and sensitivity; partial for a single average.

**Example:** Five invented models. Cost per 1k predictions ranges from 0.25 (m3, high volume) to 14.5 (m4, 1 million predictions a month). A 3x spike in month 6 trips both alerts. Sensitivity: compute rate +50 percent gives 1.461x total, idle +20 points gives 1.412x, people +20 percent only 1.015x.

**Code:** run with `python3 -I q45.py`. All figures are invented abstract units, no prices.
```python
{{CODE}}```

**Output (my run):**
```
{{OUT}}```

**Follow-ups:**
- *Showback or chargeback?* Start with showback to build trust; chargeback needs agreed tagging.
- *Biggest lever?* Idle share: raising utilisation often beats model tweaks.
- *Budget with uncertainty?* Give a base and a spike case, not one number.

**Common mistakes:**
- Excluding people and idle cost.
- One alert type.
- Platform inventing the value numbers.
"""
