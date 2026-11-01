B = {}
B[12] = """**Say this first (1 line):** Model output is untrusted input to whatever consumes it: if you paste it into HTML, SQL, a shell or a markdown renderer without treating it like user input, an attacker who influences the model (often through a retrieved document) gets XSS, injection or silent data theft, so you encode for the sink, allowlist what can leave, and never auto-execute.

**Then explain:**
- **Why it happens:** the model is steered by text from users, documents and tools, so its output can carry attacker-chosen content. OWASP's 2025 list names this risk "Improper Output Handling" (LLM05, per the OWASP page I opened). The bug is in the downstream code that trusts the output, not in the model.
- **One rule, per sink:** HTML gets escaped, SQL gets parameters, shell gets an argv list plus an allowlist, URLs get an allowlist, structured fields get a schema. Same discipline as for user input.
- **Exfiltration through markdown (general technique, from memory, check current write-ups):** an injected instruction tells the model to emit an image link whose URL carries private data in the query string. The chat UI fetches the image automatically, so the data leaves with no click. Links need a click, so they are weaker but still work with social engineering.
- **Controls for rendering:** render model text as plain text or escape it; allowlist image and link hosts; strip images or proxy them through your own server that drops query strings; show the real URL before a click; set a Content-Security-Policy so the page cannot load images from unknown hosts (defence in depth).
- **Controls for actions:** structured outputs validated against a schema, enum values for actions, parameterised queries, argv lists, a human confirmation for anything with side effects, and no auto-execution of model-written code outside a sandbox (Part 8 Q41).
- **Honest limit:** these are deterministic and strong at the sink, but you must find every sink. A filter on one rendering path does not protect the email export or the Slack bot that reuses the same text.

**Example:** (toy, hard-coded outputs) a summary contains an `<img onerror=...>` tag. Pasted raw into a div it would execute in a browser; after `html.escape` it shows as inert text. A model-chosen value `nobody' OR '1'='1` returned 2 rows (every user) through string concatenation and 0 rows through a parameterised query. A reply with an image pointing at an attacker host with a 24-character query string was rewritten to "[image removed]"; an image from the allowlisted CDN passed.

**Code:** (run with `python3 -I`; stdlib only; defensive toy with hard-coded strings, no LLM)
```python
{{CODE12}}```
**Output (my run):**
```
{{OUT12}}```

**Follow-ups:**
- *Is escaping enough for the markdown image case?* No. Escaping HTML does not stop a legitimate markdown image from being fetched; you need a URL allowlist or an image proxy.
- *Why not just ask the model not to emit such links?* That is a probabilistic defence against an attacker who writes the instruction; the sink control is deterministic. See Part 11 Q10 for the layering.
- *How does this relate to the lethal trifecta?* Image rendering is an external-communication channel; see Part 11 Q9.

**Common mistakes:** treating model output as trusted because "we wrote the prompt"; escaping for HTML but forgetting the markdown renderer; allowlisting a domain that hosts user content (open redirects, upload hosts); `shell=True` with model text; letting the model output the SQL text instead of the parameters; testing only the happy-path renderer.
"""
B[13] = """**Say this first (1 line):** Log raw token counts per call (fresh input, cached input, output, reasoning), store the price-table version used, compute cost in decimal from a versioned table, tag every row with tenant, feature and prompt version, and reconcile the total against the provider invoice on a schedule.

**Then explain:**
- **Record counts, not dollars, as the source of truth.** Prices change; token counts do not. Store `input`, `cached_input`, `output`, `reasoning`, model id, latency, and a price-table version, so you can recompute history. Langfuse and Helicone docs describe usage and cost tracking as a feature (vendor docs, as I read them); the exact fields differ by tool, so check the one you use.
- **Four buckets price differently.** Fresh input, cached input (usually cheaper), output, and reasoning tokens. Whether reasoning tokens are billed at the output rate is provider-specific: I assumed yes in the toy, check the live terms.
- **Versioned price table:** key by model and effective date; pick the latest row on or before the request date. Never overwrite a price row.
- **Attribution tags:** tenant, feature, prompt version, environment. Cost per prompt version is what lets you see that a prompt change raised spend (Part 11 Q41).
- **Latency alongside cost:** time to first token and total time, per span, so you can see the cost-latency trade-off per feature.
- **Reconciliation:** your sum will not match the invoice exactly (retries counted by the provider, calls that bypassed your wrapper, rounding, taxes, price changes). Set a tolerance, alert when the gap exceeds it, and investigate by day and model.
- **Use Decimal or integer micro-units for money,** not floats, so sums are exact.

**Example:** (SYNTHETIC prices, per 1M tokens: June table input 0.80, cached 0.08, output 3.20) one request with 5,000 input tokens of which 4,000 cached, 400 output and 1,200 reasoning costs (1,000 x 0.80 + 4,000 x 0.08 + 1,600 x 3.20) / 1M = $0.006240. The same request priced with the old January table would be higher, which is why the table version is stored. Pricing every token at the output rate would overstate the June rows about 3.2x ($0.052960 vs $0.016480).

**Code:** (run with `python3 -I`; stdlib only; synthetic prices and requests)
```python
{{CODE13}}```
**Output (my run):**
```
{{OUT13}}```

**Follow-ups:**
- *Why not take cost from the provider response?* Some responses carry usage only, and you still need your own tags and a cross-check. Use provider usage fields for counts and your table for price.
- *How do you handle streaming that is cut off?* Record what you received and mark the row partial; reconcile later with the invoice. From memory, check how your provider bills aborted streams.
- *Self-hosted?* Different problem: Part 10 Q13.

**Common mistakes:** floats for money; one flat price per token; forgetting cached or reasoning tokens; no price-table version so history silently re-prices when you edit a constant; missing tags so cost cannot be attributed; never reconciling.
"""
B[14] = """**Say this first (1 line):** An LLM gateway is a thin service between your apps and model providers that centralises keys, routing, retries and fallbacks, rate limits, budgets, caching and logging, so those concerns are solved once; the price is an extra hop, a new single point of failure and a store of everyone's prompts that you must protect.

**Then explain:**
- **What it does:** one API shape for several providers; holds provider keys so apps never see them; routes by model, tenant or cost; retries with backoff and falls back to another provider; enforces per-tenant rate limits and budgets; caches; logs usage and cost; calls guardrail hooks. Helicone's gateway docs list routing, failover, caching and custom rate limits (vendor docs as I read them; budgets were not discussed on the page I opened).
- **Risks:**
  - *Latency:* one more network hop plus its own processing.
  - *Single point of failure:* if the gateway is down, every feature is down. Run several instances, health-check them, and decide whether apps may bypass it in an emergency.
  - *Data honeypot:* it sees every prompt and response, so it needs access control, masking in logs, short retention and a tight blast radius.
  - *Lowest common denominator:* provider-specific features (tools, caching controls, structured output modes) may not pass through cleanly.
- **Correctness details that bite:** cache keys must include tenant and model (and anything else that changes the answer), or one tenant is served another's cached reply; fallback models behave differently (Part 11 Q15); budget checks need estimate-then-reconcile (Part 11 Q16, Q36).
- **Build vs buy:** buy or adopt open source when you need routing and logging quickly and requirements are standard; build when you have special tenancy, data-residency or compliance needs, or the gateway becomes core platform. Either way, treat it as security-critical infrastructure. A small team often starts with a library plus a shared wrapper and graduates to a service when several teams need the same controls.

**Example:** (toy, mock providers) provider A times out twice (first try and one retry), so the gateway falls back to B and answers; the same prompt from the same tenant is then a cache hit; the same prompt from another tenant is not served that cached answer; a tenant whose budget (6 units, synthetic) is already spent is blocked before any provider call. Final counts: provider A called 3 times, B once, 2 cache entries.

**Code:** (run with `python3 -I`; stdlib only; mock providers, no network)
```python
{{CODE14}}```
**Output (my run):**
```
{{OUT14}}```

**Follow-ups:**
- *How do you avoid the gateway being the single point of failure?* Multiple instances behind a load balancer, short timeouts, health checks, and a documented break-glass path; fail open or closed per feature depending on risk.
- *Does the gateway replace app-level guardrails?* No; it can host hooks, but the app still owns output handling (Part 11 Q12).
- *Where does semantic caching fit?* Part 10 Q28.

**Common mistakes:** a cache key without tenant or model; logging full prompts at the gateway with no masking; retries inside both the app and the gateway (multiplied attempts); assuming fallbacks are free; building it before knowing which three controls you actually need.
"""
B[15] = """**Say this first (1 line):** Treat the provider as an unreliable network dependency: set timeouts, retry only safe or idempotent calls with exponential backoff plus jitter, honour Retry-After on 429, trip a circuit breaker when failures pile up, fall back deliberately (and test the fallback model), and degrade gracefully when nothing works.

**Then explain:**
- **Timeouts:** set connect and total timeouts, and for streaming a time-to-first-token and idle timeout. A call with no timeout can hold a worker forever.
- **Retries:** retry timeouts, 429 and 5xx; do not retry 400-class client errors. Exponential backoff with full jitter spreads retries out; without jitter, clients that failed together retry together. Cap attempts and total time, and have only one layer doing retries (app or gateway, not both).
- **429 and Retry-After:** when the server says how long to wait (the HTTP Retry-After header, from memory, check your provider), use it instead of guessing.
- **Idempotency:** a retried completion is harmless, a retried tool call (send email, charge card) is not. Use idempotency keys for side effects, and keep model calls and tool calls under separate retry rules (Part 11 Q38 has this bug class).
- **Circuit breaker:** after N consecutive failures stop calling for a cooldown, then let one probe through (half-open). It protects the provider from you and your users from long waits.
- **Fallback:** a second model or provider keeps the feature alive but may format differently, follow instructions differently, have a smaller context or different safety behaviour. Keep a tested prompt per fallback and monitor fallback rate and quality.
- **Graceful degradation:** cached answer, shorter answer, a simpler model, a queue with a later notification, or an honest error message.

**Example:** (SYNTHETIC simulation, seeded) 200 clients all get a 429 at t=0 against a server that serves 40 requests per second. Without jitter they retry in synchronised waves: 200 requests in slots 0 and 2, then 160 in slot 6, 760 requests sent in total, and 160 of 200 finished within 40 s. With full jitter the load spreads out (200, 200, 84, 47, 53, 7, ...), 624 requests were sent and all 200 finished. The breaker run: over 14 ticks with the provider down until tick 9, 6 calls went through and 8 were short-circuited. A fallback that wraps its JSON in prose fails a strict `json.loads` that the primary passes.

**Code:** (run with `python3 -I`; stdlib only; simulated server, seeded)
```python
{{CODE15}}```
**Output (my run):**
```
{{OUT15}}```

**Follow-ups:**
- *Why jitter on a single client?* A single client does not need it; a fleet does, because correlated retries are a load spike.
- *Retry a timed-out completion?* Usually safe for a pure completion but you may pay twice for tokens; not safe if the call triggered tools.
- *Fallback quality?* Run your eval set on the fallback model in CI and alert when traffic shifts to it.

**Common mistakes:** retrying everything including 400s; no cap on attempts or time; retries at every layer; ignoring Retry-After; no jitter; a fallback nobody has tested; retrying non-idempotent tool calls; a breaker that never half-opens.
"""
B[16] = """**Say this first (1 line):** Give each tenant (and optionally user) a budget enforced before the call with a reservation, warn at a soft limit, block at a hard limit, cap what one request can spend, and report spend back by tenant and feature, so a scripted flood cannot turn into an unbounded bill (denial of wallet).

**Then explain:**
- **Denial of wallet:** OWASP's 2025 list covers this under Unbounded Consumption (LLM10): abusive volume or very long requests drive cost, not just availability.
- **Layers:** per-request limits (max input size, `max_tokens`, tool-call and loop caps), per-user and per-tenant rate limits (token bucket for bursts, see Part 11 Q36), and a periodic budget (daily or monthly) with a reserve-then-reconcile ledger.
- **Soft vs hard:** soft limit (say 80 percent) alerts the tenant and your team and may degrade to a cheaper model; hard limit blocks or requires approval. Enterprise customers often get a hard limit with a grace buffer and a human contact instead of a surprise outage.
- **Alerts before spikes:** alert on the burn rate (spend per hour against the budget), not only on crossing a threshold.
- **Showback vs chargeback:** showback reports each team or tenant's spend without billing it; chargeback bills it. Both need the tags from Part 11 Q13.
- **Free tiers and signups:** cap spend per anonymous or new account; abuse is cheapest there.
- **Fairness while serving** is a different layer: Part 10 Q49.

**Example:** (SYNTHETIC cents, scripted traffic) a tenant with a 1000-cent monthly budget sends 200 normal requests at 3 cents: 600 spent, no alert. A flooded tenant sends 2000 requests at 40 cents: the soft alert fires at 800, the hard cap blocks 1975 of 2000, and spend stops at 1000. Without the cap the same flood would cost 80,000 cents. Another tenant is unaffected. A reservation of 30 refunded to 12 after the call finished.

**Code:** (run with `python3 -I`; stdlib only; synthetic money units)
```python
{{CODE16}}```
**Output (my run):**
```
{{OUT16}}```

**Follow-ups:**
- *Do you block or degrade at the limit?* Depends on the contract: degrade to a cheaper model for paying tenants, block free ones.
- *Estimates are wrong, then?* Reserve the maximum (input size plus `max_tokens`), then refund after the call.
- *Agent loops?* Add a per-task step and cost cap, not just a per-request one (Part 8).

**Common mistakes:** checking the budget after the call; only a monthly limit with no per-request cap; a shared pool so one tenant starves others; an alert on spend with no one on the hook; counting only output tokens; no limit for free accounts.
"""
B[17] = """**Say this first (1 line):** Pin to a dated model snapshot, never to a moving alias like "latest", because a silent upgrade changes behaviour with no code change; then treat every provider change as a planned migration with a regression suite, a canary and a runbook.

**Then explain:**
- **Why aliases are risky:** the string stays the same while the model behind it changes, so output format, refusals, tone, cost and latency can shift overnight. Your prompts were tuned against one behaviour.
- **Pinning:** configure an explicit dated model id per environment, enforce it in code review or CI (a lint that rejects alias names), and log the model id returned by the provider on each trace.
- **Deprecations:** providers retire snapshots on their own schedule (check the live deprecation page; I quote no dates). Track retirement dates in a calendar, start migration with a lead time, and have a rollback model.
- **Migration runbook:** run the regression and safety suites on the candidate, compare paired results, canary a small slice, compare cost and latency as well as quality, then roll out gradually with a way back (Part 11 Q6 for rollout; Part 9 Q14 for gate design).
- **Statistics:** small suites are noisy. A paired exact sign test on the items where old and new disagree tells you whether a drop is distinguishable from noise.
- **Contract and process:** ask for notice periods and stable-version commitments where you can, keep a second provider warmed for critical features, and keep an owner for each model dependency.
- **Detection of silent updates** is Part 9 Q43; this answer is change management.

**Example:** (toy, SYNTHETIC) `acme-large-latest` and `acme-large` are flagged as unpinned by a dated-suffix rule; `acme-large-2026-03-01` passes and, with an invented retirement date, has 100 days left. On 60 synthetic regression cases the old model passed 47 and the new 41; the new was worse on 11 items and better on 5, one-sided sign-test p = 0.1051. That is a 6-case drop that is not significant at this size, which is the honest outcome: you either need more cases or you accept the uncertainty and canary. The sign-test formula matched a brute-force enumeration for four cases.

**Code:** (run with `python3 -I`; stdlib only; synthetic data)
```python
{{CODE17}}```
**Output (my run):**
```
{{OUT17}}```

**Follow-ups:**
- *If pinned snapshots retire, are you not forced to migrate anyway?* Yes, but on your schedule, with evals, not as a surprise.
- *Is pinning enough?* No: the same snapshot can still vary run to run, and the provider's infrastructure can change; keep monitoring (Part 11 Q3, Q4).
- *Open-weights models?* You control the weights and version them like any artefact, but then you own serving (Part 10).

**Common mistakes:** "latest" in production; pinning in one service but not another; no regression suite so every upgrade is a guess; judging a model swap on a handful of examples; ignoring cost and latency changes; discovering the retirement date after it passed.
"""
B[18] = """**Say this first (1 line):** Put fast, deterministic checks on every PR (unit tests with a mocked model, prompt lint, schema checks, secret scan, a small eval tier), push expensive and noisy work to nightly (full evals, red-team set, cost regression), and gate merges on a statistical rule, not on one noisy score.

**Then explain:**
- **Every PR (minutes, cheap):**
  - unit tests with a mocked model (parsing, routing, retries, tool schemas);
  - prompt lint (unclosed placeholders, length, forbidden strings) and schema or contract checks on structured outputs;
  - secret scanning and dependency checks;
  - a small eval tier (tens of cases) against the real or a cheap model, run only when prompts, models or retrieval code change.
- **Nightly or on release (slower, costlier):** full eval suite, red-team and injection regression set (Part 11 Q44), cost and latency regression against a baseline, and a check that pinned models are still available.
- **Gating non-deterministic results:** a naive "score must not drop" rule fails on noise; use paired comparison on the same items, several samples per item if affordable, and block only when the drop is significant or exceeds a margin. Part 9 Q14 owns gate design; this answer is the pipeline shape.
- **Trade-off:** a statistical gate has low power on a small tier, so it catches big regressions and lets small ones through. Say that out loud, and let nightly catch the rest.
- **Make failures debuggable:** upload the failing cases and traces as CI artefacts, pin the seed where the provider allows it, and keep a quarantine list for flaky cases instead of deleting them.
- **Mocked tests never call the network;** live evals need keys, budgets and a cost cap in CI.

**Example:** (toy, mock model, SYNTHETIC per-item pass probabilities, 60 items, 2000 simulated PRs per row) with no real change, a naive "block if the score drops at all" gate let the PR through only 53.7 percent of the time (it falsely blocked 46.3 percent); a paired exact sign-test gate at alpha 0.05 passed 96.0 percent. With a real regression (every item's pass probability lowered by 0.15), the naive gate passed it 2.6 percent of the time and the sign-test gate 43.2 percent: it let a real regression through more than half of the time at this size, so it is a bounded false-alarm rule, not a detector of everything.

**Code:** (run with `python3 -I`; stdlib only; mock model, seeded)
```python
{{CODE18}}```
**Output (my run):**
```
{{OUT18}}```

**Follow-ups:**
- *Why not a fixed threshold like 90 percent?* Because the baseline moves with the model and the suite; compare against the baseline on the same items.
- *How do you keep CI cost down?* Run the eval tier only on relevant path changes, use a cheaper judge for the PR tier, cache results keyed by prompt and input hash.
- *LLM judge in CI?* Mock it in unit tests, use it live only in the eval tier (Part 9).

**Common mistakes:** live model calls in unit tests (slow and flaky); one run, one number; deleting flaky cases; the red-team set only run at launch; no cost regression so a prompt change doubles tokens unnoticed; secrets in CI logs.
"""
B[19] = """**Say this first (1 line):** Keep all errors, low-score and flagged traces and a random slice of the rest using tail sampling (decided after the trace finishes), keep prompt text for the shortest time you can justify, and make deletion work across every store that copied the conversation.

**Then explain:**
- **Head vs tail:** head sampling decides at the start (say 5 percent), cheap but blind to outcomes, so it throws away most errors. Tail sampling buffers the trace and decides at the end using errors, latency, low scores, guardrail hits, and a base random rate. It costs buffering memory and needs a collector that sees complete traces.
- **Per-tenant rules:** raise the rate for new tenants or a new prompt version, lower it for high-volume steady ones, and honour tenant contracts that forbid storing content at all.
- **Two retention tiers:** keep cheap metadata (ids, token counts, latency, status, scores) longer, and prompt and response text much shorter, or masked. The numbers are your policy and legal advice, not a technical constant.
- **Deletion requests:** you need a way to find a user's data: store a keyed hash or pseudonymous id on every record, and run deletion across traces, eval sets, caches, vector stores, analytics and exports. Backups and provider-side copies need a documented policy. A hashed id is still personal data in many regimes; defer to counsel (Part 11 Q11).
- **Do not copy production traces into eval sets** without masking and a retention plan; that is where deletion most often fails.
- **Vendor support for sampling and masking** was not confirmed in my sources (the Langfuse overview page I opened did not cover it); check the tool's live docs.

**Example:** (SYNTHETIC, 100,000 traces: 1 percent errors, 2 percent of the rest low-scored) head sampling at 5 percent kept 4,988 traces and only 63 of 985 errors and 95 of 1,923 low-score traces. Tail sampling (all errors, all low-score, plus 5 percent random) kept 7,677 traces (7.7 percent) and all 985 and 1,923. For 2.7 percentage points more storage you keep every trace you would want to debug. A retention sweep with a 30-day TTL removed 71 of 100 daily full-text rows. A deletion for user u1 removed rows from the traces store and the eval set, and left the other user's data.

**Code:** (run with `python3 -I`; stdlib only; synthetic traces, seeded)
```python
{{CODE19}}```
**Output (my run):**
```
{{OUT19}}```

**Follow-ups:**
- *Does tail sampling bias your metrics?* Yes; keep the sampling decision and rate on each kept trace so you can re-weight, and compute headline rates from unsampled counters.
- *What if you cannot store prompts at all?* Store hashes, lengths, template version and scores (Part 11 Q1).
- *Can you delete from a provider's logs?* Depends on the provider and plan; check the live terms.

**Common mistakes:** head-sampling errors away; keeping full text forever; no user id on records so deletion is impossible; deleting from the primary store but not the eval set or cache; computing rates only from sampled data; PII in span attributes.
"""
B[20] = """**Say this first (1 line):** Log each feedback event with the trace id it refers to (explicit thumbs and edits, implicit regenerate, copy and abandon), treat it as a biased, sparse signal, and use it to find traces for review, grow the eval set and watch trends, not as a direct quality score.

**Then explain:**
- **Attaching to traces:** return the trace id to the client with each answer; the thumbs, edit or regenerate event posts that id. LangSmith and Phoenix docs describe annotations and feedback on traces (vendor docs as I read them); the schema is yours either way.
- **Signals:** thumbs (explicit, rare), edit distance when a user rewrites a draft (rich), regenerate (often "not good enough"), copy or accept (weak positive), abandon or rephrase within a minute (weak negative), escalation to a human.
- **Biases:** low response rate; unhappy users click more, so the thumbs-down share overstates dissatisfaction; power users dominate; position and UI effects; implicit signals are ambiguous (copy can mean useful or just saving evidence).
- **Use it for:** triage queues (down-voted traces to human review), mining failing cases into the eval set (with masking, Part 11 Q19), per-prompt-version trend comparison, and alerts on a sudden change in the down-rate.
- **Do not use it for:** an absolute satisfaction figure, or training data without review and consent.
- **Treat feedback text as untrusted:** it can contain PII and injection attempts.

**Example:** (SYNTHETIC; assumed true unhappy share 20 percent; assumed click rates 1 percent for happy and 6 percent for unhappy users; 50,000 traces) 975 users responded (1.95 percent): 393 up, 582 down. The thumbs-down share was 59.7 percent against a true unhappy share of 20 percent. Re-weighting with the assumed rates recovers 19.8 percent, but real click rates are unknown, so that fix is not available in practice. The trend is still useful: if the true unhappy share rises from 20 to 30 percent the observed down share moves from 61.4 to 72.4 percent, so a jump is visible even though the level is wrong.

**Code:** (run with `python3 -I`; stdlib only; synthetic users and assumed rates)
```python
{{CODE20}}```
**Output (my run):**
```
{{OUT20}}```

**Follow-ups:**
- *How do you get unbiased quality?* Sample traces at random and judge them with humans or a validated judge (Part 9), and use feedback to prioritise, not to measure.
- *Edits as labels?* Strong, but only for the fields users change; treat as a preference pair after review.
- *Alerting?* Alert on change against a rolling baseline per segment, with a minimum count.

**Common mistakes:** reading thumbs share as the satisfaction rate; no trace id on the event; optimising prompts against clicks and drifting toward sycophancy; training on feedback without review; ignoring that feedback comes mostly from a small user group.
"""
B[21] = """**Say this first (1 line):** Run an LLM incident like any production incident, with severity levels, reversible first-hour actions you rehearsed (flag off, prompt label back, pin the previous model, tighten a guardrail), traces frozen as evidence, clear communication, and a blameless review that ends with a new eval case so it cannot silently recur.

**Then explain:**
- **Severity (example scheme, adapt it):** Sev 1 harmful or data-leaking output or full outage; Sev 2 major quality or cost regression for many users; Sev 3 limited or cosmetic. Severity drives who is paged and how often you update stakeholders.
- **Detect:** alert rules on error rate, cost per request, refusal and guardrail-trigger rate, format failures and user feedback (Part 11 Q3).
- **First hour, in order of reversibility:** stop the bleeding (feature flag or kill switch for tools or the whole feature); roll back the last change (prompt label, config, model pin; Part 11 Q5, Q6); tighten a guardrail or lower tool privileges; only then debug. Every action is logged with who and when.
- **Evidence:** copy the affected traces into a frozen store with a content hash before retention deletes them, keep the prompt version, model id and retrieved documents, and restrict access because traces contain user data.
- **Security incidents add:** rotate any key that may have been exposed (Part 11 Q29), check logs for the same pattern across tenants, and involve security and legal early; breach-notification duties are for counsel to judge.
- **Communicate:** one incident channel, a named lead, short timestamped updates, and an honest customer message that says what happened and what changed.
- **Review:** blameless, written, with a timeline, contributing factors, and action items with owners; the key output is a regression case in the eval or security suite (Part 11 Q44).

**Example:** (toy, mock data) the error rate per minute is 1, 1, 2, 9, 11, 12 percent; a rule "above 5 percent for 3 consecutive minutes" pages on-call. The responder sets the `use_tools` flag to false and moves the `production` prompt label from v2 back to v1; both actions are written to an audit list. Five suspect traces are frozen with a content hash. The new eval case keeps the failing input with the email masked as `<EMAIL>` and an expectation about tool use.

**Code:** (run with `python3 -I`; stdlib only; in-memory mock, no real flag service)
```python
{{CODE21}}```
**Output (my run):**
```
{{OUT21}}```

**Follow-ups:**
- *What if the cause is the provider?* Switch to the pinned previous model or the fallback (tested), post status, and capture the model id and timestamps for the provider ticket.
- *Who can flip the kill switch?* On-call engineers, without a code deploy, with an audit trail.
- *Is a wrong answer an incident?* A single wrong answer is a bug; a pattern, or one with safety, legal or data impact, is an incident.

**Common mistakes:** debugging before mitigating; a rollback that needs a full deploy; traces deleted by TTL before anyone looked; no audit of who changed what; blame instead of fixes; closing the incident without a regression test.
"""
B[22] = """**Say this first (1 line):** A jailbreak is the user talking the model out of its rules; prompt injection is third-party text in the context (a document, a tool result) giving the model instructions; in logs you separate them by where the instruction text came from, and you test both with the same attack families and report attack success rate with an interval.

**Then explain:**
- **Distinguish by source (Part 5 Q9 and Q35 have the theory):** an override attempt in the user turn is a jailbreak attempt; the same kind of text inside retrieved content or a tool result is an injection attempt. This needs logs that tag each context segment with its source, so log that. In real traffic one attacker can do both and the boundary is blurry; the label is for triage, not for proof.
- **Attack families to test:** role-play and persona framing, instruction override, encoded or obfuscated text, multi-turn escalation, and indirect injection through documents, email, web pages and tool outputs. Use a curated suite and an automated one (Part 9 Q29, Part 11 Q28).
- **Repeat offenders:** Anthropic's guidance mentions responding to users who repeatedly trigger screens (docs as read on 2026-10-24): a ladder of warn, throttle, review, suspend, with human review before a ban so you do not punish a curious or confused user.
- **Attack success rate (ASR) over time:** fix a versioned attack set, run it each release, count successes out of attempts, and report an interval, since a small set gives wide error bars. Track new real-world attempts separately from the fixed set, and keep the fixed set from being the only thing you optimise for.
- **Honest limit of log heuristics:** keyword rules miss role-play stories and encodings, and fire on benign text that merely mentions the phrase; they are for triage and counting.

**Example:** (SYNTHETIC hand-labelled log lines, heuristic labeller) on 9 lines the heuristic agreed with my label on 6. It flagged a benign question that quotes the phrase "ignore previous instructions" (false positive), and it missed a role-play story request and a base64-encoded override (misses). That is a tiny set and shows limits, not accuracy. ASR intervals (Wilson, 95 percent, SYNTHETIC counts): 3 of 40 gives [0.026, 0.199]; 9 of 40 gives [0.123, 0.375], so 7.5 percent versus 22.5 percent on 40 attacks each overlap only partly and a small suite cannot resolve small changes; 0 of 10 gives [0.000, 0.278], so zero successes in 10 does not mean safe. The Wilson formula matched an independent bisection inversion.

**Code:** (run with `python3 -I`; stdlib only; defensive toy, no attack payload kit, benign placeholder phrases)
```python
{{CODE22}}```
**Output (my run):**
```
{{OUT22}}```

**Follow-ups:**
- *Can you stop jailbreaks with a keyword list?* No; it is one cheap layer (Part 11 Q10, Q35).
- *How do you avoid overfitting to your attack suite?* Hold out a private set, add fresh attacks from red-teaming and logs, rotate (Part 11 Q44).
- *What do you log?* Source tags per segment, guardrail verdicts, user and tenant ids, with the PII rules from Part 11 Q11.

**Common mistakes:** calling every attack a jailbreak and missing the indirect path; no source tags in logs; banning users from one keyword hit; reporting ASR as one number with no n; treating 0 failures in a few tries as safe; testing only English single-turn prompts.
"""
