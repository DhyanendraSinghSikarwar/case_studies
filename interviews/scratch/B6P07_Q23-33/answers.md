### Q23 ⭐⭐ 🟢 A system prompt grew from 800 to 3,500 tokens over ten small edits, and the service makes 2,000,000 calls a month at an illustrative 3 per million input tokens. Compute the extra monthly input cost caused by the growth, and describe how you would version, review and trim the prompt without breaking behaviour.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to prompt versioning and prompt-length topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The growth adds 2,700 tokens a call, which is 5.4 billion tokens and about 16,200 extra a month at 3 per million (illustrative), and I would version the prompt like code, trim it with a regression suite as the safety net, and cache the stable part.

**Clarifying questions:**
- Is the 3,500 all static system prompt, or does it include per-request content? Only the static prefix can be cached or trimmed safely.
- Does the provider discount repeated prefixes, and by how much? That decides whether trimming or caching gives the bigger saving.
- Is there a regression suite today? Without one, no trim is safe.
- Does extra length also add latency (time to first token)? Cost is not the only price of a long prompt.
- Who owns the prompt? Ten small edits by ten people is the root cause.

**Approach:**
1. Check the arithmetic. Extra tokens per call = 3,500 - 800 = 2,700. Per month = 2,700 x 2,000,000 = 5.4 billion. Cost = 5,400 million / 1 million x 3 = 16,200. The old prompt cost 4,800 a month and the new one costs 21,000, 4.4 times more.
2. Put the prompt in version control with an id, an owner and a changelog. One change per commit, each linked to the failure it fixed.
3. Build a regression suite first: representative inputs plus the cases each edit was meant to fix. Run it on every change, and compare pass rates with a paired comparison, not one headline number.
4. Trim by ablation: remove one block at a time and re-run. Keep a block only if its removal hurts a case. Look for repeated rules, contradictions, old examples and rules the model follows anyway.
5. Move rarely needed instructions out of the always-on prompt (load by intent or retrieve them), and put the stable text at the front so prefix caching can work (see Book 2 Part 3 Q36 and Book 2 Part 1 Q24).
6. Roll out as a canary with a rollback rule, and add a prompt-length budget check in review so it cannot creep again.

**Metrics:**
- Prompt tokens per call (static prefix and total), monthly input cost = tokens per call x calls / 1e6 x price.
- Regression pass rate, with paired counts: cases that flipped pass to fail versus fail to pass.
- Guardrails: latency to first token, refusal rate, format-error rate, and the pass rate on the cases tied to each removed rule.

**Risks:**
- Removing a block that looked redundant but fixed a rare failure. The suite only protects what it covers.
- Trimming for cost and silently changing tone or safety behaviour.
- Cache savings depend on the provider rules and on keeping the prefix byte-identical. Editing the front of the prompt busts the cache.
- Counting only input tokens. Longer prompts can also cause longer answers.

**What the interviewer scores:**
- Strong: gets 16,200 right and says it is illustrative. Weak: forgets that all 2,000,000 calls pay the extra 2,700.
- Strong: tests before trimming (suite, ablation, paired comparison). Weak: "I will rewrite it shorter" with no evidence.
- Strong: treats the prompt as versioned code with an owner. Weak: leaves it as a shared text box.
- Strong: mentions caching and moving rules out of the prompt, not only deleting words.

**Example:** (illustrative prices and volumes) Weak: "The prompt got longer, so it costs more. I will shorten it." Strong: "Ten edits added 2,700 tokens a call. On 2 million calls at 3 per million that is 16,200 a month. I would run the regression suite, remove one block at a time, and keep what the suite needs. Trimming to 1,500 tokens would save 12,000. If 80% of the prefix hits a cache at a tenth of the price, the extra cost falls to about 4,500 even without trimming. Prices here are illustrative, not any vendor's."

**Code:**
```python
# Illustrative prices and volumes (not vendor prices). Prompt-growth cost and a caching sensitivity.
calls, price_in = 2_000_000, 3.0           # calls per month, price per million input tokens
old, new = 800, 3500
extra_tokens_per_call = new - old
extra_tokens = extra_tokens_per_call * calls
extra_cost = extra_tokens / 1e6 * price_in
old_cost = old * calls / 1e6 * price_in
new_cost = new * calls / 1e6 * price_in
print("extra tokens per call", extra_tokens_per_call, "extra tokens per month", extra_tokens)
print("old prompt cost", old_cost, "new prompt cost", new_cost, "extra", extra_cost)
assert extra_tokens_per_call == 2700 and extra_tokens == 5_400_000_000
assert old_cost == 4800 and new_cost == 21000 and extra_cost == 16200
assert round(new / old, 3) == 4.375
# Sensitivity: trim back to 1,500 tokens
trim = 1500
saved = (new - trim) * calls / 1e6 * price_in
print("trim to", trim, "saves", saved, "per month; remaining extra", (trim - old) * calls / 1e6 * price_in)
assert saved == 12000 and (trim - old) * calls / 1e6 * price_in == 4200
# Sensitivity: if the stable prefix is cached at an illustrative 10% of the input rate with an 80% hit rate
hit, disc = 0.8, 0.10
eff = (1 - hit) + hit * disc               # effective fraction of full price paid on the prefix
print("effective price fraction", round(eff, 2), "extra cost with caching", round(extra_cost * eff, 1))
assert round(eff, 2) == 0.28 and round(extra_cost * eff, 1) == 4536.0
```

**Output (my run):**
```text
extra tokens per call 2700 extra tokens per month 5400000000
old prompt cost 4800.0 new prompt cost 21000.0 extra 16200.0
trim to 1500 saves 12000.0 per month; remaining extra 4200.0
effective price fraction 0.28 extra cost with caching 4536.0
```

**Follow-ups:**
- How do you stop it growing again? A token budget in CI, an owner in code review, and each edit linked to a test case.
- What if trimming lowers a quality metric by one point? Check the paired flips and the interval. If it is real, weigh it against the saving (see Q31 for the same trade-off).

**Common mistakes:**
- Computing the extra on one call and not on the monthly volume.
- Trimming with no regression suite.
- Editing the front of the prompt and breaking the cache.
- Ignoring that long prompts add latency.

### Q24 ⭐⭐ 🟢 An assistant that cites sources is audited on 150 citations: 120 exist and support the claim, 15 exist but do not support it, and 15 point to documents that do not exist. Compute the share of each outcome, and say how you would reduce fabricated and unsupported citations and track them over time.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to grounding and citation topics in RAG-debugging pages; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** 80% of citations are good, 10% exist but do not support the claim, and 10% are fabricated, so one in five citations is bad, and the two bad kinds need different fixes and different tracking.

**Clarifying questions:**
- How was the 150 sampled: random across all answers, or from flagged ones? Only a random sample gives shares for the whole product.
- What counts as "supports"? Who judged it, with what rubric, and did two reviewers agree?
- Is the citation a link, a quote or a document id? That decides how a fabricated one can be caught.
- Are the 15 fabricated ones fake urls or fake ids inside our own index? The second is a pipeline bug.
- How much does a wrong citation cost the user (legal, medical, casual)? It sets the target.

**Approach:**
1. Shares: 120/150 = 80%, 15/150 = 10%, 15/150 = 10%. They add to 150. Bad citations = 30 = 20%. A 95% Wilson interval on each 10% is about 6.2% to 15.8%, so with 150 audited do not claim the two 10%s are different.
2. Fix fabricated first, because it is the cheapest: stop the model inventing identifiers. Give it only retrieved document ids, ask it to cite by id, and verify every id and quote against the retrieved set in code. Drop or flag anything that does not resolve.
3. Fix unsupported next, which is harder: check each claim against the cited passage (a quote-match check, an entailment or judge check, or both). Rewrite or remove claims the passage does not support. Let the assistant say "I could not find a source."
4. Improve upstream: better retrieval so the right passage is available, and chunks small enough that the cited span is visible.
5. Track over time: a monthly random audit of fixed size, plus an automatic daily check for the resolver-visible kind on all traffic, plus a judge calibrated on human labels for the support check (see Q33).

**Metrics:**
- Fabricated rate = citations that do not resolve / citations audited.
- Unsupported rate = citations that resolve but do not support the claim / citations audited.
- Supported rate = supported citations / citations audited. (Define the unit, citation or answer, and keep it fixed.)
- Guardrails: coverage (share of claims that carry a citation), abstention rate, answer helpfulness. A system can reach zero bad citations by citing nothing.

**Risks:**
- A resolver check only catches fabricated ones, here 15 of the 30 bad citations, half. It misses unsupported ones.
- Judge-based support checks have their own bias and need human calibration.
- Optimising citation precision alone can push the model to cite only easy claims.
- A 150-citation audit has wide intervals (about plus or minus 5 points), so small changes are noise.

**What the interviewer scores:**
- Strong: separates fabricated from unsupported and fixes each differently. Weak: one number called "hallucination".
- Strong: gives intervals and sample-size awareness. Weak: treats 10% versus 10% as meaningful.
- Strong: automatic check on all traffic plus a human audit sample. Weak: audit once and stop.
- Strong: watches coverage and abstention. Weak: celebrates zero bad citations.

**Example:** (illustrative numbers) Weak: "20% of citations are wrong, I would tell the model to be more careful." Strong: "10% are fake and 10% do not support the claim. I would make the model cite retrieved ids only and verify each id in code, which should take fabricated close to zero. For the unsupported 10% I would add a claim-versus-passage check and an option to say no source found. I would audit a random 300 citations a month, because 150 gives plus or minus about 5 points, and track coverage so we do not win by citing less."

**Code:**
```python
# Citation audit: shares of each outcome, Wilson intervals, and a simple projection (illustrative).
import math
def wil(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
n = 150
ok, unsup, fab = 120, 15, 15
assert ok + unsup + fab == n
for name, k in [("supported", ok), ("exists but unsupported", unsup), ("fabricated", fab)]:
    lo, hi = wil(k, n)
    print(f"{name}: {k}/{n} = {k/n:.1%}, 95% Wilson {lo:.1%} to {hi:.1%}")
assert ok/n == 0.8 and unsup/n == 0.1 and fab/n == 0.1
lo, hi = wil(15, 150)
assert round(lo, 3) == 0.062 and round(hi, 3) == 0.158, (lo, hi)
# Resolver check alone catches only the fabricated kind: share of bad citations it can see
bad = unsup + fab
print("bad citations", bad, "share of citations", bad/n, "resolver-visible share of bad", fab/bad)
assert bad == 30 and bad/n == 0.2 and fab/bad == 0.5
# Illustrative target: after a fix, fabricated 15 -> 0 by resolver filter, unsupported 15 -> 9 by claim check
after_ok = n - 0 - 9
print("after fix (illustrative): supported", after_ok, f"{after_ok/n:.0%}", "bad", 9, f"{9/n:.0%}")
assert after_ok == 141 and 9/n == 0.06
# Sample size to see 5% vs 10% unsupported-rate with a 95% half-width of about 2.5 points
n_need = math.ceil(1.96**2 * 0.05*0.95 / 0.025**2)
print("n for half-width 2.5 points at p=0.05:", n_need)
assert n_need == 292
```

**Output (my run):**
```text
supported: 120/150 = 80.0%, 95% Wilson 72.9% to 85.6%
exists but unsupported: 15/150 = 10.0%, 95% Wilson 6.2% to 15.8%
fabricated: 15/150 = 10.0%, 95% Wilson 6.2% to 15.8%
bad citations 30 share of citations 0.2 resolver-visible share of bad 0.5
after fix (illustrative): supported 141 94% bad 9 6%
n for half-width 2.5 points at p=0.05: 292
```

**Follow-ups:**
- Can a citation be correct yet the answer wrong? Yes. The source may be wrong or misread. Citation checks are necessary, not sufficient.
- How do you audit cheaply? Judge plus a human sample, with the judge checked against humans first (kappa, see Q33).

**Common mistakes:**
- Merging fabricated and unsupported into one "hallucination" rate.
- Fixing only with prompts, with no verification in code.
- Reading small differences on 150 items as real.
- Ignoring coverage and abstention.

### Q25 ⭐⭐ 🟢 A client times out on 8% of 100,000 daily calls (8,000 calls) and retries up to 3 times, resending the full 3,000-token prompt each time, billed at an illustrative 3 per million input tokens even for timed-out calls. Compute the extra daily cost if every one of those calls succeeds on its first retry, and the upper bound if all 3 retries are used by every one, and say what you would change.
**Asked at:** LLM cost and routing pages (getmaxim cost and semantic-cache guides, tianpan and system-design.space pages on routing and cascades, a Towards Data Science article on saving tokens in agentic AI, a Towards AI piece on AI system-design interview patterns); practitioner material, no confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Each retry round on the 8,000 timed-out calls costs 72 a day (illustrative), so the extra is 72 if all succeed on the first retry and at most 216 if every one uses all 3 retries, on a base of 900, which is plus 8% and plus 24%.

**Clarifying questions:**
- Does the provider really bill timed-out or cancelled calls, and for how many tokens? The prompt says yes. Check real billing, because some bill input regardless and some only what was processed.
- Is the timeout client-side only? If the server still finishes, a retry doubles the work and the cost.
- Why are 8% timing out: the provider, our network, or a timeout set too low? The cure depends on it.
- Are retries idempotent, and do they use the same prompt? Duplicates can also cause duplicate actions.
- Is output billed on timed-out calls too? The prompt counts input only.

**Approach:**
1. Tokens per retry round: 8,000 x 3,000 = 24 million. Cost = 24 x 3 = 72 a day. First retry succeeding: extra 72. All 3 retries used by all 8,000: 3 x 72 = 216. Baseline first attempts: 100,000 x 3,000 = 300 million tokens = 900 a day. So plus 8% and plus 24% on input cost. Input only, output ignored.
2. The 216 is an upper bound on retries sent, not a forecast. A realistic number is between: if each retry times out again half the time, the expected extra is 126.
3. Fix the cause: find out why 8% time out (long prompts, slow region, low timeout). Raise the timeout if the work completes later, or shorten the prompt.
4. Make retries cheap and safe: exponential backoff with jitter, a retry budget (for example no more than 10% extra traffic), a circuit breaker, and an idempotency key.
5. Use streaming and a first-token timeout, so a slow call is cut early and a stuck one is not billed in full.
6. Fall back to a smaller or different model on the second retry instead of resending the same heavy call to the same place.

**Metrics:**
- Retry amplification = total calls sent / original calls (1.08 for one round on 8%).
- Timeout rate = timed-out calls / calls sent, by region, prompt size and hour.
- Wasted spend per day = tokens billed on calls that returned nothing x price.
- Guardrails: end-to-end success rate, p95 latency, and duplicate-action rate.

**Risks:**
- Retry storms: when the provider is slow, retries add load and cause more timeouts.
- Non-idempotent tool calls repeated on retry.
- Aggressive retry budgets turn a slow period into visible failures.
- The 8% may be correlated (one region, one bad hour), so the independence assumption is wrong.

**What the interviewer scores:**
- Strong: both numbers, 72 and 216, with the base for scale. Weak: multiplies by 100,000 instead of 8,000.
- Strong: points out that 216 is a ceiling and gives a realistic estimate. Weak: presents it as the forecast.
- Strong: backoff, budget, circuit breaker, idempotency. Weak: "retry less".
- Strong: asks why they time out. Weak: only tunes the retry count.

**Example:** (illustrative price) Weak: "8,000 timeouts at 3 per million is cheap, ignore it." Strong: "Each retry round resends 24 million tokens, 72 a day. Best case 72 extra, worst case 216, which is 24% on input. The real fix is the 8%: I would look at region and prompt length, add jittered backoff with a retry budget, and fall back to a lighter model on the second retry."

**Code:**
```python
# Retry cost. Illustrative price: 3 per million input tokens; timed-out calls are billed (stated assumption).
calls, rate, prompt, retries = 100_000, 0.08, 3000, 3
price = 3.0
timeouts = round(calls * rate)
tok_per_round = timeouts * prompt
cost_round = tok_per_round / 1e6 * price
base_cost = calls * prompt / 1e6 * price
print("timeouts", timeouts, "tokens per retry round", tok_per_round, "cost per retry round", cost_round)
print("baseline first-attempt daily input cost", base_cost)
low = cost_round * 1
high = cost_round * retries
print("extra if every timeout succeeds on retry 1:", low, f"({low/base_cost:.0%} of base)")
print("extra upper bound if all 3 retries used:", high, f"({high/base_cost:.0%} of base)")
assert timeouts == 8000 and tok_per_round == 24_000_000
assert cost_round == 72 and base_cost == 900 and low == 72 and high == 216
assert round(low/base_cost, 3) == 0.08 and round(high/base_cost, 3) == 0.24
# Expected under a more realistic mix (illustrative): each retry times out again with prob q
q = 0.5
exp_attempts = sum(q**i for i in range(retries))      # retries sent per original timeout, stops on success
exp_extra = timeouts * exp_attempts * prompt / 1e6 * price
print("expected extra with q=0.5 re-timeout chance:", round(exp_extra, 1), "attempts/timeout", exp_attempts)
assert exp_attempts == 1.75 and round(exp_extra, 1) == 126.0
# Monthly (30 days) for the upper bound
print("30-day upper bound", high * 30)
assert high * 30 == 6480
```

**Output (my run):**
```text
timeouts 8000 tokens per retry round 24000000 cost per retry round 72.0
baseline first-attempt daily input cost 900.0
extra if every timeout succeeds on retry 1: 72.0 (8% of base)
extra upper bound if all 3 retries used: 216.0 (24% of base)
expected extra with q=0.5 re-timeout chance: 126.0 attempts/timeout 1.75
30-day upper bound 6480.0
```

**Follow-ups:**
- What if the provider does not bill timed-out calls? Then the cost is just latency and the extra is near zero, but check the invoice.
- What if output is billed too? Add output tokens times the output price for each retry. Rerun the same formula.

**Common mistakes:**
- Applying retries to all 100,000 calls instead of the 8,000.
- Treating the upper bound as expected cost.
- Retrying with no backoff.
- Forgetting idempotency for calls that trigger actions.

### Q26 ⭐⭐ 🟡 An internal policy assistant re-indexes its 1,200 documents once a week, and about 90 documents change in a typical week at random times. Compute the average number of documents that are stale at a random moment, as a count and as a share of the index, and say how you would guarantee freshness for the documents that matter most.
**Asked at:** RAG-debugging pages (Latitude, Educative, Redis, Fiddler and ChatRAG pages on locating the failing stage, stale indexes, retrieval recall versus faithfulness and reranking); practitioner and vendor material rather than a confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** On average 45 documents are stale at any moment, which is 3.75% of the index, because a changed document waits half a week on average for the next re-index, and I would make the important documents event-driven so they are never stale for long.

**Clarifying questions:**
- Do changes arrive uniformly through the week? The half-week average assumes they do. Bursts on Friday would raise it.
- Is the 90 a count of distinct documents? A document edited twice is stale once, not twice.
- How long does the weekly re-index run? Documents are stale until it finishes, not until it starts.
- Which documents matter most (policy that affects pay, legal, safety)? Freshness targets should differ by tier.
- Can the source system send change events or a modified-time? That decides polling versus push.

**Approach:**
1. Average stale count = changes per week x average wait. Wait is uniform from 0 to 7 days, so 3.5 days, half a week. 90 x 0.5 = 45. As a share: 45 / 1,200 = 3.75%. (A rate-times-time argument, Little's law; I checked it by simulation.)
2. The peak is not 45. It is 90 (7.5%) just before the re-index, and 0 just after.
3. For important documents, do not wait for the batch: subscribe to change events (or poll modified-time every few minutes), re-chunk and re-embed only the changed document, and swap it in atomically.
4. For everything else, move from weekly full re-index to a daily or hourly incremental job that uses a content hash to skip unchanged files. Daily cuts the average to about 6.4 stale documents (0.54%).
5. Tell the user: show "last updated" in answers, include the document date, and add a freshness check on answers about policies.
6. Handle deletes and replaced versions: remove old chunks so a stale chunk cannot outrank the new one.

**Metrics:**
- Staleness of a document = time between source change and index update. Report mean, p95 and max by tier.
- Stale share = documents whose indexed version differs from source / documents in index, measured by sampling or a daily hash compare.
- Guardrails: re-index cost, index consistency errors (half-updated documents) and answer accuracy on recently changed policies.

**Risks:**
- Partial updates (some chunks new, some old) give mixed answers.
- Old versions kept in the index and retrieved ahead of the new one.
- Event-driven pipelines silently miss events, so keep a nightly reconciliation by hash.
- Averaging hides the damage: a stale policy document matters far more than a stale FAQ.

**What the interviewer scores:**
- Strong: 45 and 3.75% with a one-line reason (half a week x 90). Weak: says 90 or 7.5%.
- Strong: separates average, peak and importance. Weak: treats all documents alike.
- Strong: event-driven for critical documents plus nightly reconciliation. Weak: "re-index more often" only.
- Strong: handles deletes and versions. Weak: only adds new content.

**Example:** (illustrative) Weak: "90 documents are stale, 7.5%, so we need daily re-indexing for all." Strong: "At a random moment about 45 are stale, 3.75%, with a peak of 90 before the batch. A policy that changes on Tuesday is wrong for up to 5 days. I would push the top-tier documents through a change event with a target of minutes, move the rest to a daily hash-based job, and run a nightly reconciliation to catch missed events."

**Code:**
```python
# Stale documents under weekly re-index; illustrative. A doc is stale from its change until the next re-index.
import numpy as np
N, changes, week = 1200, 90, 7.0
# Exact: change times uniform over the week, so the mean wait to the next re-index is half a week (Little's law: rate x time)
avg_stale = changes * 0.5
print("average stale docs", avg_stale, "share", f"{avg_stale/N:.2%}")
assert avg_stale == 45 and round(avg_stale/N, 4) == 0.0375
# Simulation: 90 distinct docs change at uniform times in each week, re-index at each week boundary
rng = np.random.default_rng(7)
weeks = 20000
t = rng.uniform(0, week, size=(weeks, changes))           # change times within the week
mean_wait = (week - t).mean()                              # days stale per changed doc
print("simulated mean days stale per changed doc", round(mean_wait, 3), "(theory 3.5)")
assert abs(mean_wait - 3.5) < 0.01
sim_avg_stale = changes * mean_wait / week                 # average count stale at a random moment
print("simulated average stale docs", round(sim_avg_stale, 2))
assert abs(sim_avg_stale - 45) < 0.1
# Worst moment: just before re-index, all 90 changed docs are stale; just after, 0
print("peak stale", changes, f"({changes/N:.2%})")
assert changes/N == 0.075
# Different schedule: daily re-index of changed docs only (hash check) -> mean wait 0.5 day
daily = changes * (0.5/7)
print("daily re-index average stale", round(daily, 2), f"({daily/N:.2%})")
assert round(daily, 2) == 6.43
# Event-driven re-index with 10-minute lag
lag_days = 10/1440
print("event-driven 10 min lag average stale", round(changes/7*lag_days, 3))
assert round(changes/7*lag_days, 3) == 0.089
```

**Output (my run):**
```text
average stale docs 45.0 share 3.75%
simulated mean days stale per changed doc 3.502 (theory 3.5)
simulated average stale docs 45.02
peak stale 90 (7.50%)
daily re-index average stale 6.43 (0.54%)
event-driven 10 min lag average stale 0.089
```

**Follow-ups:**
- What if changes cluster on Fridays? Then more documents wait longer and the average rises above 45. Measure with real change times.
- How do you prove the index is fresh? Compare content hashes of source and index daily and alert on mismatch.

**Common mistakes:**
- Using the peak (90) as the average.
- Forgetting that a re-index run takes time.
- Re-embedding the whole corpus when only a few documents changed.
- Leaving old versions in the index.

### Q27 ⭐⭐ 🟡 A retrieval stage reaches recall at 5 of 62% on 300 labelled queries (186 queries), and adding a reranker lifts it to 74% (222 queries) while adding 120 ms to a path that already takes 900 ms against a 1,200 ms budget. Is the 12-point absolute gain worth it, and what else do you check before shipping the reranker?
**Asked at:** RAG-debugging pages (Latitude, Educative, Redis, Fiddler and ChatRAG pages on locating the failing stage, stale indexes, retrieval recall versus faithfulness and reranking); practitioner and vendor material rather than a confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** A 12-point gain in recall at 5 (62% to 74%, 36 more queries of 300) is large enough to be probably real, and 120 ms fits the budget on paper (1,020 of 1,200 ms), but I would ship only after checking the tail latency, the paired gains and losses, and whether answers actually get better.

**Clarifying questions:**
- Is the 900 ms a mean or a p95? Budgets are about the tail, and a rerank step often has a heavier tail than its average.
- Are the same 300 queries used before and after, and were they used to tune the reranker? If yes, the gain is optimistic.
- How many candidates does the reranker score? Cost and latency grow with that number.
- Does recall at 5 lead to better final answers? The user sees answers, not recall.
- Does the reranker run on our hardware or via an API (cost per call, rate limits)?

**Approach:**
1. Check the numbers. 186/300 = 62%, 222/300 = 74%. The gain is 12 points absolute and 36 queries, 19.4% relative. Per 1,000 queries that is 120 more with the right chunk in the top 5.
2. Is it noise? Unpaired, the standard error is about 3.8 points, so the 95% interval for the gain is roughly 4.6 to 19.4 points. A paired view is better: count queries the reranker rescued and queries it lost. The net is +36, but 42 rescued and 6 lost is a different story from 80 rescued and 44 lost: both are significant, but the second hurts 44 queries and needs a look at what they have in common (the counts here are illustrative, the prompt gives only the net).
3. Latency: 900 + 120 = 1,020 ms, 180 ms under the budget, and the reranker adds 13.3%. Measure p95 and p99 with the reranker under load. If 900 ms is a mean, the tail may already exceed 1,200.
4. Check the end-to-end effect: faithfulness and answer correctness on the same queries, with the final model, not only retrieval recall.
5. Check slices: short queries, long queries, rare topics and Hindi or romanised queries. A reranker can help on average and hurt a segment.
6. Ship behind a flag as a canary, watch latency, answer quality and cost, and keep a one-switch rollback.

**Metrics:**
- Recall at 5 = queries with a relevant chunk in the top 5 / queries evaluated.
- Paired counts: rescued (miss to hit), lost (hit to miss), net.
- Latency p50, p95, p99 of the retrieval path, and the budget headroom.
- End-to-end: answer correctness and faithfulness. Guardrails: cost per query, timeouts, error rate of the reranker.

**Risks:**
- Gain measured on a set used to choose the reranker (overfit).
- Tail latency breach even though the average fits.
- Better recall at 5 does not help if the model ignores the chunk.
- Added dependency and failure mode, so decide the behaviour when the reranker times out (fall back to unranked results).

**What the interviewer scores:**
- Strong: separates absolute and relative gain, and asks for paired counts. Weak: says "12 points, ship it".
- Strong: questions whether 900 ms is a mean or a tail. Weak: just subtracts 1,020 from 1,200.
- Strong: asks for end-to-end answer quality. Weak: stops at recall.
- Strong: slices, canary and fallback. Weak: no rollout plan.

**Example:** (illustrative) Weak: "Recall went up 12 points and 1,020 is under 1,200, so yes." Strong: "36 more queries hit, which is real at this size if rescues far outnumber losses. I need the paired counts, p95 latency with the reranker, and answer correctness end to end. If p95 is 1,150 or more I would shrink the candidate count or use a smaller reranker. Then a canary with a fallback to no rerank."

**Code:**
```python
# Reranker: gain, intervals, and a paired test on ILLUSTRATIVE discordant counts. Seeded.
import math
from scipy.stats import binomtest
n = 300
a, b = 186, 222
print("recall@5", a/n, b/n, "gain points", (b-a)/n*100, "relative", round((b-a)/a, 3))
assert a/n == 0.62 and b/n == 0.74 and b - a == 36 and round((b-a)/a, 3) == 0.194
def wil(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h, c+h
print("Wilson before", [round(x, 3) for x in wil(a, n)], "after", [round(x, 3) for x in wil(b, n)])
# Unpaired difference interval (conservative; the paired one is usually tighter)
se = math.sqrt(.62*.38/n + .74*.26/n)
print("unpaired SE", round(se, 4), "95% interval for gain", round(.12-1.96*se, 3), round(.12+1.96*se, 3))
assert round(se, 4) == 0.0378 and round(.12-1.96*se, 3) == 0.046
# Paired: net +36 = rescued - lost. Illustrative: 42 rescued, 6 lost (exact sign test)
rescued, lost = 42, 6
assert rescued - lost == 36
p = binomtest(rescued, rescued+lost, 0.5).pvalue
print("exact McNemar p (illustrative 42 vs 6):", f"{p:.2e}")
assert p < 1e-6
# Worst plausible split with the same net: 80 rescued, 44 lost -> still net 36, test weaker but still small p, yet 44 users get worse
p2 = binomtest(80, 124, 0.5).pvalue
print("exact McNemar p (80 vs 44):", round(p2, 4))
assert 0.001 < p2 < 0.002
# Latency
base, add, budget = 900, 120, 1200
total = base + add
print("latency", total, "headroom", budget-total, "added share", round(add/base, 3))
assert total == 1020 and budget - total == 180 and round(add/base, 3) == 0.133
# If 900 is a mean and p95 is 1.4x mean (illustrative), p95 after = 1.4*900+120*? ; flag the budget risk
p95_after = 1.4*base + 1.5*add
print("illustrative p95 after (rerank p95 1.5x)", p95_after, "vs budget", budget)
assert p95_after == 1440 > budget
# per 1,000 queries
print("extra queries with the right chunk in top 5 per 1,000:", round(1000*(b-a)/n))
assert round(1000*(b-a)/n) == 120
```

**Output (my run):**
```text
recall@5 0.62 0.74 gain points 12.0 relative 0.194
Wilson before [0.564, 0.673] after [0.688, 0.786]
unpaired SE 0.0378 95% interval for gain 0.046 0.194
exact McNemar p (illustrative 42 vs 6): 1.01e-07
exact McNemar p (80 vs 44): 0.0016
latency 1020 headroom 180 added share 0.133
illustrative p95 after (rerank p95 1.5x) 1440.0 vs budget 1200
extra queries with the right chunk in top 5 per 1,000: 120
```

**Follow-ups:**
- How do you cut the 120 ms? Rerank fewer candidates, use a smaller or distilled reranker, batch on GPU, or run it in parallel with other work.
- When is a 2-point gain worth it? When the cost is small and the interval clears zero, and the gain survives end to end.

**Common mistakes:**
- Calling 12 points "12%".
- Judging the budget on mean latency.
- Evaluating on the set used for tuning.
- Skipping end-to-end answer checks.

### Q28 ⭐⭐ 🟡 A GPU serves one request at 50 tokens per second per user, 42 at batch size 4, 35 at batch size 8 and 25 at batch size 16, and the product needs at least 30 tokens per second per user. Compute aggregate throughput at each batch size, choose the batch size, and compute the cost per million output tokens at an illustrative 2.5 per GPU-hour for your choice.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to batching and throughput topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Aggregate throughput is 50, 168, 280 and 400 tokens per second at batch 1, 4, 8 and 16, batch 16 breaks the 30 tokens per second per user rule (it gives 25), so I choose batch 8, which costs about 2.48 per million output tokens at an illustrative 2.5 per GPU-hour.

**Clarifying questions:**
- Is 30 tokens per second a hard floor or an average? A p95 floor at peak is a stricter test than a mean.
- Do the measured speeds hold with real prompt lengths and with prefill from other users in the batch? Long prompts slow everyone.
- Is the GPU busy all hour, or does traffic leave it idle? Idle time raises the real cost.
- Is there a batch between 8 and 16 we can measure? Batch 10 or 12 might still meet 30 and be cheaper.
- Does the product need low time to first token too? Large batches can hurt that.

**Approach:**
1. Aggregate throughput = batch size x per-user speed: 1 x 50 = 50, 4 x 42 = 168, 8 x 35 = 280, 16 x 25 = 400 tokens per second.
2. Apply the product rule first. Per-user speed must be at least 30. Batch 16 gives 25, so it is out. Batches 1, 4, 8 pass.
3. Among those that pass, pick the highest throughput, because cost per token falls as throughput rises. That is batch 8, at 280 tokens per second and a 5 tokens per second margin (14%).
4. Cost per million output tokens = GPU price per hour / (tokens per second x 3,600 / 1,000,000). At batch 8: 2.5 / (280 x 3,600 / 1e6) = 2.5 / 1.008 = about 2.48. Batch 1 would be 13.89 and batch 4 4.13.
5. Real cost is higher if the GPU is idle. At 50% busy the same batch costs 4.96. Utilisation matters as much as batch size.
6. Test intermediate batch sizes and real traffic. Add an autoscaling rule on queue depth so a spike does not push users below 30.

**Metrics:**
- Per-user decode speed (tokens per second per request), at p50 and p5 (the slow tail).
- Aggregate throughput = sum of tokens per second across requests.
- Cost per million output tokens = hourly price / (throughput x 3,600 / 1e6) / utilisation.
- Guardrails: time to first token, queue wait, and error rate.

**Risks:**
- The table is a single measurement. Real mixes of prompt lengths change it.
- Choosing 8 leaves only 5 tokens per second of margin, so a busier mix may breach 30.
- Cost depends on utilisation. Quoting the full-utilisation cost is optimistic.
- Input (prefill) cost and cost of the GPU being reserved are not in this figure.

**What the interviewer scores:**
- Strong: computes throughput as batch x per-user speed and applies the constraint before optimising. Weak: picks 16 for the highest throughput.
- Strong: converts to cost per million with the 3,600 and 1e6 steps. Weak: wrong units.
- Strong: raises utilisation and intermediate batch sizes. Weak: treats the table as final.
- Strong: mentions margin and tail. Weak: ignores the 5 tokens per second margin.

**Example:** (illustrative) Weak: "Batch 16 gives 400 tokens per second, the most, so use it." Strong: "Batch 16 gives each user 25, under the 30 floor. Batch 8 gives 280 tokens per second and 35 per user. That is about 1.0 million tokens an hour on a 2.5 GPU-hour, so around 2.48 per million at full use, and about 5 at half use. I would measure batch 10 and 12 before settling."

**Code:**
```python
# Batching: throughput and cost per million output tokens. Illustrative GPU price 2.5 per GPU-hour.
per_user = {1: 50, 4: 42, 8: 35, 16: 25}
need, gpu_hr = 30, 2.5
rows = {}
for bs, tps in per_user.items():
    agg = bs * tps
    cost = gpu_hr / (agg * 3600 / 1e6)
    ok = tps >= need
    rows[bs] = (agg, cost, ok)
    print(f"batch {bs:2d}: per-user {tps}, aggregate {agg} tok/s, cost/M tokens {cost:.2f}, meets 30? {ok}")
assert [rows[b][0] for b in (1, 4, 8, 16)] == [50, 168, 280, 400]
assert [rows[b][2] for b in (1, 4, 8, 16)] == [True, True, True, False]
best = max((b for b in rows if rows[b][2]), key=lambda b: rows[b][0])
print("choice", best)
assert best == 8
assert round(rows[8][1], 2) == 2.48 and round(rows[16][1], 2) == 1.74 and round(rows[1][1], 2) == 13.89
# Utilisation sensitivity (illustrative): GPU busy only 50% of the hour
for u in (1.0, 0.5, 0.3):
    c = gpu_hr / (280 * 3600 * u / 1e6)
    print(f"utilisation {u:.0%}: cost/M tokens {c:.2f}")
assert round(gpu_hr / (280*3600*0.5/1e6), 2) == 4.96
# Headroom: batch 8 gives 35 vs need 30 -> 5 tok/s margin (14%)
print("margin", 35 - 30, f"{(35-30)/35:.1%} of per-user speed")
assert round(5/35, 3) == 0.143
```

**Output (my run):**
```text
batch  1: per-user 50, aggregate 50 tok/s, cost/M tokens 13.89, meets 30? True
batch  4: per-user 42, aggregate 168 tok/s, cost/M tokens 4.13, meets 30? True
batch  8: per-user 35, aggregate 280 tok/s, cost/M tokens 2.48, meets 30? True
batch 16: per-user 25, aggregate 400 tok/s, cost/M tokens 1.74, meets 30? False
choice 8
utilisation 100%: cost/M tokens 2.48
utilisation 50%: cost/M tokens 4.96
utilisation 30%: cost/M tokens 8.27
margin 5 14.3% of per-user speed
```

**Follow-ups:**
- Why does per-user speed fall as batch grows? The GPU shares compute and memory bandwidth, and attention over every user's cache costs more (see Book 2 Part 1 Q32 on batching and arithmetic intensity).
- How do you serve both fast and cheap tiers? Different batch limits per tier, or separate pools.

**Common mistakes:**
- Choosing the batch with the highest aggregate throughput without the speed floor.
- Mixing up per-hour and per-second.
- Quoting full-utilisation cost as the real cost.
- Forgetting prefill and time to first token.

### Q29 ⭐⭐ 🟡 A RAG request runs input moderation (100 ms), retrieval (250 ms), reranking (150 ms) and then model time to first token (400 ms) one after another, and the time-to-first-token budget is 700 ms. Compute the current time to first token and its value if moderation runs in parallel with retrieval, and say what else you would cut.
**Asked at:** GenAI and LLM-engineer interview guides (InterviewBit, Hyring, Let's Code, recrew, Pensero and Towards AI 2026 pages list RAG, hallucination mitigation, evaluation and cost or latency topics; one guide reports a prompt about a RAG answer that is wrong although the right document exists, and another a smaller-model-for-narrow-tasks answer pattern); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Time to first token is 900 ms today, running moderation in parallel with retrieval gives 800 ms, which is still 100 ms over the 700 ms budget, so I need another 100 ms from reranking, retrieval or the model step.

**Clarifying questions:**
- Are these means or p95 numbers? The budget is for the tail, and parallel steps take the max of their tails, so sum-of-means misleads.
- Must moderation finish before the model sees the text, or only before the user sees the answer? That decides how far it can move off the critical path.
- Is time to first token measured from the request arriving or from the model call? Network and queue time may be missing.
- How much does the reranker add for its 150 ms, and how many candidates does it score?
- Is the model step 400 ms dominated by prompt length (prefill)? Then trimming context cuts it.

**Approach:**
1. Current: 100 + 250 + 150 + 400 = 900 ms. Over budget by 200.
2. Moderation checks the user's input, and retrieval also needs only the input, so they can run at the same time. Parallel stage time = max(100, 250) = 250. New total: 250 + 150 + 400 = 800 ms. The saving equals the moderation time, 100 ms, and we are still 100 ms over.
3. Moderation is not the bottleneck any more. Running it alongside retrieval and rerank gives 800 too, because retrieval plus rerank (400 ms) is the longer path. Gate the answer on the moderation result (hold the first token if it flags), not the start of retrieval.
4. Cut 100 ms or more more from the critical path, which is retrieval, rerank and model. Options (illustrative): a cheaper rerank (150 ms to 60 ms, for example fewer candidates) gets 710 ms, which is still 10 over; adding a retrieval trim (250 to 200) gets 660 ms; a shorter prompt cutting model time to first token from 400 to 320 gets 720 ms alone.
5. Other levers: cache the retrieval results for repeated queries, use a smaller reranker, a smaller or faster model for the first token, speculative start (begin model prefill on the system prompt while retrieval runs), and a regional deployment close to users.
6. Check that each cut does not cost quality (see Q27), then measure p95 in production, not on a quiet laptop.

**Metrics:**
- Time to first token, p50 and p95, split by stage (a per-stage trace).
- Critical-path length = longest chain of dependent stages.
- Quality guardrails: retrieval recall at 5, answer correctness, moderation recall (blocks of harmful input).
- Cost per query and the share of queries that skip an optional stage.

**Risks:**
- Parallel moderation means retrieval work is wasted when moderation blocks. Acceptable if blocks are rare.
- Cutting the reranker or context can lower answer quality.
- p95 of a max of two stages is above both means, so the 800 may really be 850 or more.
- Holding the first token for moderation reintroduces its delay if moderation is slow.

**What the interviewer scores:**
- Strong: computes 900, then 800, and says plainly it still misses 700. Weak: claims parallelism fixes it.
- Strong: critical-path thinking (max of parallel branches). Weak: subtracts without understanding.
- Strong: names several concrete cuts and their quality cost. Weak: "use a faster model".
- Strong: asks for a trace and p95. Weak: optimises on averages.

**Example:** (illustrative) Weak: "Run moderation in parallel and we are fine." Strong: "Sequential is 900. In parallel the moderation step disappears from the path, so 250 + 150 + 400 = 800, which is 100 over. I would reduce the reranker's candidate list and trim the prompt so model prefill drops. Together that gets to about 660 to 720 on paper, then I would check recall and p95."

**Code:**
```python
# TTFT budget: sequential versus parallel moderation. Illustrative stage times in ms.
mod, ret, rer, ttft_model, budget = 100, 250, 150, 400, 700
seq = mod + ret + rer + ttft_model
par = max(mod, ret) + rer + ttft_model
print("sequential", seq, "over budget by", seq - budget)
print("moderation parallel with retrieval", par, "over budget by", par - budget)
assert seq == 900 and par == 800 and par - budget == 100 and seq - par == mod
# Critical path: moderation also fully off the path (runs alongside retrieval+rerank), nothing changes
par_all = max(mod, ret + rer) + ttft_model
print("moderation alongside retrieval+rerank", par_all)
assert par_all == 800
# Options to reach 700 (illustrative cuts)
opts = {
 "rerank over fewer candidates (150 -> 60)": par - (150 - 60),
 "rerank 150 -> 60 and retrieval 250 -> 200": par - (150 - 60) - 50,
 "smaller prompt cuts TTFT 400 -> 320": par - 80,
 "skip rerank for easy queries (150 -> 0 on 40% of queries), mean": par - 0.4 * 150,
}
for k, v in opts.items():
    print(f"{k}: {v:.0f}")
assert opts["rerank over fewer candidates (150 -> 60)"] == 710
assert opts["rerank 150 -> 60 and retrieval 250 -> 200"] == 660
assert opts["smaller prompt cuts TTFT 400 -> 320"] == 720
assert opts["skip rerank for easy queries (150 -> 0 on 40% of queries), mean"] == 740
# Cut needed
print("cut needed after parallelising:", par - budget)
```

**Output (my run):**
```text
sequential 900 over budget by 200
moderation parallel with retrieval 800 over budget by 100
moderation alongside retrieval+rerank 800
rerank over fewer candidates (150 -> 60): 710
rerank 150 -> 60 and retrieval 250 -> 200: 660
smaller prompt cuts TTFT 400 -> 320: 720
skip rerank for easy queries (150 -> 0 on 40% of queries), mean: 740
cut needed after parallelising: 100
```

**Follow-ups:**
- Is the first token the right target? For chat, yes: streaming means users feel time to first token more than total time.
- What if moderation is a hard legal requirement before retrieval? Then keep it first but make it much faster with a small classifier or a rules pre-check.

**Common mistakes:**
- Adding stage times that actually run in parallel.
- Forgetting that the saving from parallelism equals the shorter branch only.
- Reading means as the budget.
- Cutting a stage without checking quality.

### Q30 ⭐⭐ 🟡 Only 3,000 of 100,000 weekly chats get a vote, and 2,400 of those votes (80%) are thumbs-up. An audit of 200 randomly chosen thumbs-up answers finds 150 correct (75%), and a teammate wants to fine-tune on all thumbs-up answers. Compute how many wrong answers the 2,400 would contain if the audit rate held, and explain what is wrong with the plan.
**Asked at:** Eval-contamination and feedback-bias material (a tianpan post on eval-set contamination and production leakage, an arXiv paper on contamination in closed-source LLMs, an RLHF survey and the sycophancy literature summarised in secondary pages); research and practitioner pages rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** If the audit rate holds, about 600 of the 2,400 thumbs-up answers are wrong (25%, plausibly 470 to 750), and fine-tuning on them teaches the model its own mistakes, using a tiny, self-selected and biased 3% of chats.

**Clarifying questions:**
- How were the 200 audited answers chosen? Random from the 2,400 is assumed. If not random, the 25% is not reliable.
- What did the audit count as correct, and who judged it? A thumbs-up is a feeling; correctness needs a rubric.
- Who votes? A 3% sample of users who chose to click may differ from everyone else (power users, annoyed users).
- What would the fine-tune be for (style, accuracy, safety)? Thumbs-up may suit tone but not facts.
- Is there any ground truth we can use (resolved tickets, human agent answers, verified documents)?

**Approach:**
1. Compute the damage. Wrong share = 1 - 150/200 = 25%. Wrong among 2,400 = 2,400 x 0.25 = 600. The 95% Wilson interval on 25% with n=200 is about 19.5% to 31.4%, so roughly 468 to 754 wrong examples.
2. Say what is wrong with the plan: (a) a quarter of the training set is wrong, (b) only 3% of chats vote and the voters chose to vote (selection bias), (c) 80% thumbs-up means the set has few hard cases and no negatives, (d) users tend to reward fluent, agreeable answers (sycophancy), so the model learns to please rather than to be right, and (e) the votes may reflect speed or tone, not facts.
3. Do not fine-tune on raw thumbs. Treat votes as a weak signal for finding candidates, not as labels.
4. Build a verified set: sample, have reviewers or a checked source label correctness, and keep only verified-good answers (about 1,800 if the audit rate holds, after about 40 reviewer-hours at one minute each). Add verified failures with corrected answers.
5. Use a held-out, human-labelled evaluation set that is never used in training (see Q32 on contamination).
6. If using preference data, build pairs from verified outcomes, and watch for the model getting longer and more agreeable.

**Metrics:**
- Label noise rate = wrong examples in the training set / examples in the training set (here 25% estimated, with an interval).
- Vote coverage = votes / chats (3%), and thumbs-up share = up votes / votes (80%).
- After training: correctness on a clean held-out set, plus sycophancy checks (does it agree with false premises) and length.
- Guardrails: refusal rate, user satisfaction by segment.

**Risks:**
- Training on 25% wrong answers can bake in errors and raise confidence in them.
- Feedback loops: the model's outputs become the next training data, so errors compound.
- The voters are not the users. Rare user groups are invisible.
- Review cost: checking all 2,400 is real work, so plan the budget.

**What the interviewer scores:**
- Strong: computes 600 and gives an interval. Weak: says 25% without the count, or says 150.
- Strong: names selection bias (3% coverage), label noise and sycophancy. Weak: only "thumbs-up is noisy".
- Strong: proposes verified labels, held-out eval and staged rollout. Weak: "just filter by confidence".
- Strong: does not rubbish the signal, uses it to find candidates. Weak: dismisses feedback entirely.

**Example:** (illustrative numbers) Weak: "Thumbs-up means good, fine-tune on all 2,400." Strong: "The audit says 25% wrong, so about 600 wrong examples, and between roughly 470 and 750 given 200 audited. Also only 3% of chats vote, and agreeable answers get upvoted. I would audit and keep only verified-good answers, about 1,800, add corrected failures, and evaluate on a separate clean set."

**Code:**
```python
# Thumbs-up fine-tuning plan. Illustrative numbers from the prompt plus an invented selection-bias demo. Seeded.
import math
import numpy as np
chats, votes, ups = 100_000, 3000, 2400
print("vote coverage", votes/chats, "thumbs-up share of votes", ups/votes)
assert votes/chats == 0.03 and ups/votes == 0.8
aud_n, aud_ok = 200, 150
rate_wrong = 1 - aud_ok/aud_n
wrong = ups * rate_wrong
print("audit wrong rate", rate_wrong, "projected wrong among 2,400:", wrong)
assert rate_wrong == 0.25 and wrong == 600
def wil(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h, c+h
lo, hi = wil(aud_n-aud_ok, aud_n)
print("Wilson for wrong share", round(lo, 3), round(hi, 3), "-> wrong count range", round(ups*lo), round(ups*hi))
assert round(lo, 3) == 0.195 and round(hi, 3) == 0.314 and round(ups*lo) == 468 and round(ups*hi) == 754
# Invented demo of why votes mislead: users vote up fluent/agreeable answers even when wrong.
rng = np.random.default_rng(3)
n = 100_000
correct = rng.random(n) < 0.80                              # true accuracy 80% (invented)
# Invented: confident wrong answers are upvoted slightly more often than correct plain ones (sycophancy-style bias).
up = rng.random(n) < np.where(correct, 0.020, 0.030)
print("thumbs-up wrong share in this invented world:", round((~correct[up]).mean(), 3), "vs overall wrong share", round((~correct).mean(), 3))
assert 0.24 < (~correct[up]).mean() < 0.32 and 0.19 < (~correct).mean() < 0.21
# What an audit-then-filter plan yields: keep only audited-correct examples
keep = ups * (aud_ok/aud_n)
print("examples left after verifying each (if audit rate holds):", keep)
assert keep == 1800
# Cost of auditing everything: 2,400 reviews at 1 minute each
print("review hours at 1 min each:", 2400/60)
assert 2400/60 == 40
```

**Output (my run):**
```text
vote coverage 0.03 thumbs-up share of votes 0.8
audit wrong rate 0.25 projected wrong among 2,400: 600.0
Wilson for wrong share 0.195 0.314 -> wrong count range 468 754
thumbs-up wrong share in this invented world: 0.296 vs overall wrong share 0.2
examples left after verifying each (if audit rate holds): 1800.0
review hours at 1 min each: 40.0
```

**Follow-ups:**
- Is thumbs-down more useful? Often yes for finding failures, but it is also self-selected and sparse.
- Could you weight votes by user trust? Yes, but you still need a verified sample to measure the noise.

**Common mistakes:**
- Treating a thumbs-up as a correctness label.
- Applying the 25% to the 100,000 chats or the 3,000 votes instead of the 2,400.
- Training and evaluating on the same feedback data.
- Ignoring that the voting 3% is not a random sample of users.

### Q31 ⭐⭐ 🟡 A new model version prices both input and output tokens at 1.5 times the old version but writes answers that are 30% shorter than the old length (400 down to 280 tokens). A call has 2,000 input tokens, and old prices are an illustrative 3 and 15 per million. Compute old and new cost per call and the relative change, and say how you weigh it against a measured 2-point absolute gain in resolution rate.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to model-upgrade cost and quality trade-off topics in LLMOps material; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The call goes from 0.0120 to 0.0153, which is 27.5% more expensive even though answers are 30% shorter, and whether to switch depends on what a resolved case is worth: the extra 0.0033 per call buys 2 more resolutions per 100, which is 0.165 per extra resolution (illustrative).

**Clarifying questions:**
- Is the 2-point gain measured with an interval, on a large paired set? A 2-point gain on 500 prompts is within noise.
- What is a resolution worth (saved human handling, retained customer)? Without a value, the trade-off cannot be decided.
- Does the 30% shorter answer lose useful content or hurt satisfaction? Shorter is not always better.
- Does the new model change the number of tool calls or retries per conversation? Cost per call is not always cost per conversation.
- Are the old and new price multipliers 1.5 on both input and output? The prompt says so.

**Approach:**
1. Old cost per call: input 2,000 x 3 / 1e6 = 0.006, output 400 x 15 / 1e6 = 0.006, total 0.012.
2. New cost: input 2,000 x 4.5 / 1e6 = 0.009, output 280 x 22.5 / 1e6 = 0.0063, total 0.0153. Change = +0.0033, +27.5%. The 1.5x price is cut by the 0.7x output length for output (1.05x), but input stays at 1.5x, and input is half the bill.
3. Per million calls a month: 12,000 versus 15,300, so +3,300.
4. Convert to cost per extra resolution: 0.0033 / 0.02 = 0.165 per extra resolved case. Compare with what a resolution is worth. If a human-handled ticket costs about 2.0 (illustrative), the switch nets about +36.7 per 1,000 calls.
5. Do not use cost per resolved case alone. It would be cheaper to switch only if baseline resolution were below about 7.3%, which no real product has. Cost per resolution rises, but net value can still rise.
6. Validate the gain: paired evaluation with an interval, quality by segment, and an online canary with resolution rate and user ratings. Also consider routing: use the new model only where it helps.

**Metrics:**
- Cost per call = input tokens x input price + output tokens x output price.
- Resolution rate = resolved conversations / conversations (define "resolved" and keep it fixed).
- Incremental cost per extra resolution = change in cost per call / change in resolution rate.
- Guardrails: p95 latency, escalation rate, user satisfaction and answer length.

**Risks:**
- The 2-point gain may be noise or specific to the eval set.
- Shorter answers may reduce satisfaction while raising the "resolved" flag.
- Using cost per call and quality in separate meetings. They must be one table.
- Price and length can move again with the next version.

**What the interviewer scores:**
- Strong: both costs and the percentage change, with the input-versus-output split. Weak: says "30% shorter, 1.5x price, so about 5% more" (wrong).
- Strong: turns the quality gain into cost per extra resolution. Weak: compares 27.5% with 2 points directly.
- Strong: asks for the value of a resolution and an interval on 2 points. Weak: decides on price alone.
- Strong: proposes routing or a canary. Weak: all-or-nothing.

**Example:** (illustrative prices) Weak: "The answers are shorter so it will cost less, upgrade." Strong: "Cost per call goes from 0.0120 to 0.0153, plus 27.5%, because input is half the bill and rises 50%. The 2-point gain costs 0.165 per extra resolution. If a human-handled ticket costs more than that, it is worth it, provided the gain holds on a paired test with an interval."

**Code:**
```python
# Model upgrade: cost per call and cost per resolution. Illustrative prices (3 in, 15 out per million), not vendor prices.
pin, pout = 3.0, 15.0
tin, told, tnew = 2000, 400, 280
assert round(1 - tnew/told, 2) == 0.30
old = tin*pin/1e6 + told*pout/1e6
new = tin*pin*1.5/1e6 + tnew*pout*1.5/1e6
print("old per call", round(old, 6), "new per call", round(new, 6), "change", f"{new/old-1:+.1%}", "abs", round(new-old, 6))
assert round(old, 6) == 0.012 and round(new, 6) == 0.0153 and round(new/old-1, 3) == 0.275
# Per 1,000,000 calls a month
print("monthly per 1M calls: old", old*1e6, "new", new*1e6)
assert round(old*1e6) == 12000 and round(new*1e6) == 15300
# Split: input unchanged in tokens, so input cost +50%; output cost = 1.5 x 0.7 = 1.05
print("input part", 0.006, "->", 0.009, "output part", 0.006, "->", round(280*22.5/1e6, 6))
assert round(280*22.5/1e6, 6) == 0.0063
# Incremental cost per extra resolved case: extra cost per call / extra resolution rate
dc, dr = new-old, 0.02
print("extra cost per extra resolved case", round(dc/dr, 3))
assert round(dc/dr, 3) == 0.165
# Cost per resolved case for a few illustrative baseline resolution rates
for r in (0.40, 0.60, 0.80):
    print(f"baseline {r:.0%}: old {old/r:.5f} new {new/(r+dr):.5f} per resolved")
# The new model is cheaper per resolved case only if baseline resolution is below this:
r_star = dr*old/dc
print("break-even baseline resolution rate", round(r_star, 4))
assert round(r_star, 4) == 0.0727
# Worth it if an extra resolution saves more than 0.165. Illustrative human cost per ticket 2.0 -> yes
print("net per 1,000 calls at human cost 2.0 per resolution:", round(1000*(dr*2.0 - dc), 2))
assert round(1000*(dr*2.0 - dc), 2) == 36.7
```

**Output (my run):**
```text
old per call 0.012 new per call 0.0153 change +27.5% abs 0.0033
monthly per 1M calls: old 12000.0 new 15300.0
input part 0.006 -> 0.009 output part 0.006 -> 0.0063
extra cost per extra resolved case 0.165
baseline 40%: old 0.03000 new 0.03643 per resolved
baseline 60%: old 0.02000 new 0.02468 per resolved
baseline 80%: old 0.01500 new 0.01866 per resolved
break-even baseline resolution rate 0.0727
net per 1,000 calls at human cost 2.0 per resolution: 36.7
```

**Follow-ups:**
- Could you keep the old model for easy queries? Yes, a router that sends hard cases to the new model captures most of the gain at lower cost. Validate it as in the routing question (Q34).
- What if the gain is not significant? Do not pay 27.5% for noise. Get more data or keep the old model.

**Common mistakes:**
- Applying the 30% reduction to the whole bill.
- Comparing percentage cost with absolute points.
- Calling cost per resolved case "worse" and stopping, with no value of a resolution.
- Skipping the paired comparison and interval.

### Q32 ⭐⭐ 🟡 A 300-question golden set drawn from production logs scores 94% (282 correct), but 120 of the questions were later copied into few-shot examples and fine-tuning data. On those 120 the model got 117 right, and on the 180 untouched questions it got 165. Compute the score on each part, and say what you report and how you rebuild the set.
**Asked at:** Eval-contamination and feedback-bias material (a tianpan post on eval-set contamination and production leakage, an arXiv paper on contamination in closed-source LLMs, an RLHF survey and the sycophancy literature summarised in secondary pages); research and practitioner pages rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The honest score is 91.7% (165 of 180) on the questions the model has not seen, not the 94% headline, because on the 120 copied questions it scores 97.5% (117 of 120), which partly measures memory.

**Clarifying questions:**
- How were the 120 chosen for few-shot and fine-tuning? If they were the hard or failing ones, the clean 180 is easier than the whole set and 91.7% is itself optimistic.
- Are there near-duplicates of the 180 in the training data (rephrased questions, same ticket)? Exact-match checks miss those.
- Is the golden set the only evaluation? Anything tuned against it stops being a test.
- How often do we reuse this set across releases? Each reuse leaks more.
- Does production traffic look like the 180, the 120, or neither?

**Approach:**
1. Check the arithmetic: 117 + 165 = 282, and 282 / 300 = 94%. Contaminated part 117/120 = 97.5%. Clean part 165/180 = 91.67%. The gap is 5.8 points.
2. Report the clean score as the headline with its interval (Wilson 95%, about 86.7% to 94.9% with n = 180). Report the blended 94% only as a footnote labelled contaminated. Do not average the two.
3. The gap is suggestive, not proven: a Fisher exact test gives p of about 0.046 on these counts, borderline. Still, the direction is what you would expect from leakage, and the safe move is to stop trusting the 120.
4. Rebuild: draw a new set from production logs after the training-data cutoff, remove exact and near-duplicates against all training and few-shot data (embedding similarity plus manual check), and freeze it with restricted access.
5. Size it: about 450 questions gives plus or minus 2.5 points at a 92% rate. Stratify by topic and difficulty.
6. Process: keep a separate dev set for prompt tuning and a locked test set for release decisions, refresh the test set on a schedule, and log which examples ever entered training.

**Metrics:**
- Clean accuracy = correct on never-seen questions / never-seen questions (165/180 = 91.7%).
- Contamination share = questions copied into training or prompts / questions in the set (120/300 = 40%).
- Gap = contaminated accuracy - clean accuracy (5.8 points).
- Guardrails: near-duplicate rate between eval and training, and per-topic accuracy on the clean set.

**Risks:**
- Choosing which examples to copy based on failures makes the clean subset unrepresentative.
- Near-duplicates survive a naive dedupe.
- A rebuilt set contaminates again if it is reused for tuning.
- An overly small clean set gives wide intervals (180 gives about plus or minus 4 points).

**What the interviewer scores:**
- Strong: both sub-scores and the clean score as the headline. Weak: reports 94%.
- Strong: asks how the 120 were chosen (selection bias) and mentions near-duplicates. Weak: assumes the clean part is perfectly representative.
- Strong: fresh, deduplicated, access-controlled set with a size justification. Weak: "add more questions".
- Strong: separates dev and test sets. Weak: one set for everything.

**Example:** (illustrative) Weak: "We scored 94% on the golden set, ship it." Strong: "The 94% mixes 120 questions the model was trained or prompted on, scoring 97.5%, with 180 it has not seen, scoring 91.7%. I would report 91.7% with an interval of roughly 87 to 95, and rebuild a 450-question set from recent logs after removing near-duplicates of any training data."

**Code:**
```python
# Contaminated golden set. Numbers from the prompt; Wilson intervals and a Fisher test are computed.
import math
from scipy.stats import fisher_exact
def wil(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h, c+h
tot_n, tot_k = 300, 282
c_n, c_k = 120, 117
u_n, u_k = 180, 165
assert c_k + u_k == tot_k and c_n + u_n == tot_n
print("blended", tot_k/tot_n)
print("contaminated", c_k, c_n, c_k/c_n, [round(x, 3) for x in wil(c_k, c_n)])
print("clean", u_k, u_n, round(u_k/u_n, 4), [round(x, 3) for x in wil(u_k, u_n)])
assert tot_k/tot_n == 0.94 and c_k/c_n == 0.975 and round(u_k/u_n, 4) == 0.9167
lo, hi = wil(u_k, u_n)
assert round(lo, 3) == 0.867 and round(hi, 3) == 0.949, (lo, hi)
gap = c_k/c_n - u_k/u_n
print("gap points", round(100*gap, 2))
assert round(100*gap, 2) == 5.83
odds, p = fisher_exact([[c_k, c_n-c_k], [u_k, u_n-u_k]])
print("Fisher exact p for the gap", round(p, 3))
assert 0.04 < p < 0.05       # borderline with these counts
# Weight check: if production mix were 100% clean-like, headline would be the clean rate
print("clean-only headline", f"{u_k/u_n:.1%}", "vs 94.0% blended: overstated by", round(100*(tot_k/tot_n - u_k/u_n), 2), "points")
assert round(100*(tot_k/tot_n - u_k/u_n), 2) == 2.33
# Size of a rebuilt set for a +/-2.5 point interval at p about 0.92
n_need = math.ceil(1.96**2 * 0.92*0.08 / 0.025**2)
print("rebuilt set size for +/-2.5 points at 92%:", n_need)
assert n_need == 453
```

**Output (my run):**
```text
blended 0.94
contaminated 117 120 0.975 [0.929, 0.991]
clean 165 180 0.9167 [0.867, 0.949]
gap points 5.83
Fisher exact p for the gap 0.046
clean-only headline 91.7% vs 94.0% blended: overstated by 2.33 points
rebuilt set size for +/-2.5 points at 92%: 453
```

**Follow-ups:**
- Can you still use the 120? Yes, as a regression check that the model has not forgotten what it was taught, not as a quality estimate.
- How do you detect contamination when you do not control the training data? Compare accuracy on older versus newly written questions, and check for memorised wording (paraphrase tests).

**Common mistakes:**
- Reporting the blended score.
- Assuming the clean subset is unbiased.
- Using exact-match dedupe only.
- Tuning prompts against the final test set.

### Q33 ⭐⭐ 🟡 A pass/fail LLM judge is compared with human labels on 200 outputs: both pass on 110, both fail on 50, the judge passes and the human fails on 30, and the judge fails and the human passes on 10. Compute raw agreement, the judge's pass rate against the human pass rate, and Cohen's kappa, and say whether you would trust the judge to gate releases.
**Asked at:** LLM-evaluation pages (Manning's AI model evaluation chapter and an arXiv judge-bias study listing position, verbosity and self-preference bias, Arize and Langfuse pages on offline versus online evaluation, an LLM-as-judge survey); practitioner and academic material rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Raw agreement is 80%, but the judge passes 70% against the humans' 60%, kappa is about 0.57 (moderate), and the judge passes 37.5% of outputs that humans fail, so I would use it to screen and to track trends, not as the only release gate.

**Clarifying questions:**
- How were the 200 chosen, and how many humans labelled them? One rater is not ground truth. Two raters with their own agreement are better.
- What is the rubric, and is the judge given the same one? Different instructions create fake disagreement.
- What does a bad release cost? A false pass that ships a wrong answer to customers is worse than a false fail that costs a review.
- Is the mix of the 200 like production? Kappa depends on the pass rate, so a different mix changes it.
- Which model is the judge, and is it also the model being judged? Self-preference bias would show up as extra passes.

**Approach:**
1. Raw agreement = (110 + 50) / 200 = 80%.
2. Pass rates: judge (110 + 30) / 200 = 70%, humans (110 + 10) / 200 = 60%. The judge is 10 points more generous.
3. Kappa: chance agreement = 0.7 x 0.6 + 0.3 x 0.4 = 0.54. Kappa = (0.80 - 0.54) / (1 - 0.54) = 0.565. A seeded bootstrap gives about 0.44 to 0.68 for a 95% interval, so it is moderate and not tight.
4. Error structure matters more than the single number. Given the human says pass, the judge agrees 91.7% of the time (110/120). Given the human says fail, the judge catches only 62.5% (50/80) and wrongly passes 37.5% (30/80).
5. For gating, that false-pass rate is the problem. On 1,000 outputs with 40% truly bad, about 150 bad ones would pass (illustrative mix).
6. How to improve it and use it: read the 30 false passes and the 10 false fails to find the pattern (often length or style), tighten the rubric, use a stronger judge or pairwise and swapped-order comparisons, calibrate with a threshold, and re-check on a fresh sample. Until then use the judge as a first filter, send borderline and judge-pass samples to humans, and gate on a human-checked sample.

**Metrics:**
- Agreement = matching labels / items (80%).
- Cohen's kappa = (observed agreement - chance agreement) / (1 - chance agreement) (0.565).
- False-pass rate = judge pass among human-fail / human-fail (30/80 = 37.5%). False-fail rate = judge fail among human-pass / human-pass (10/120 = 8.3%).
- Guardrails: judge drift (re-audit monthly), bias by length and by answer position.

**Risks:**
- A generous judge hides regressions and approves bad releases.
- Raw agreement looks high (80%) partly because passes dominate. Kappa corrects for that.
- Human labels have their own error, so the judge may be better than the table says.
- Prompt or model changes on the judge side shift scores silently.

**What the interviewer scores:**
- Strong: gets 80%, 70% versus 60% and kappa 0.57 right, and explains chance agreement. Weak: stops at "80% agreement is good".
- Strong: looks at the direction of the errors (false passes). Weak: treats all disagreements as equal.
- Strong: decision with conditions (screen yes, sole gate no, human sample). Weak: yes or no without reasoning.
- Strong: mentions biases (length, position, self-preference) and re-calibration. Weak: assumes the judge is stable.

**Example:** (illustrative counts) Weak: "80% agreement, so the judge is fine to gate releases." Strong: "Agreement is 80% but kappa is 0.57, and the judge passes 70% against humans' 60%. It lets through 30 of 80 truly bad outputs, 37.5%. I would use it to rank and screen, send a random sample of its passes to humans, and fix the rubric from the 30 false passes before I let it block or approve a release alone."

**Code:**
```python
# Judge versus human: agreement, rates, kappa, bootstrap interval. Seeded.
import numpy as np
bp, bf, jp_hf, jf_hp = 110, 50, 30, 10
n = bp + bf + jp_hf + jf_hp
assert n == 200
agree = (bp + bf) / n
judge_pass = (bp + jp_hf) / n
human_pass = (bp + jf_hp) / n
pe = judge_pass*human_pass + (1-judge_pass)*(1-human_pass)
kappa = (agree - pe) / (1 - pe)
print("agreement", agree, "judge pass", judge_pass, "human pass", human_pass)
print("chance agreement", round(pe, 4), "kappa", round(kappa, 4))
assert agree == 0.8 and judge_pass == 0.7 and human_pass == 0.6
assert round(pe, 2) == 0.54 and round(kappa, 3) == 0.565
# Error structure
sens = bp / (bp + jf_hp)           # judge passes when human passes
spec = bf / (bf + jp_hf)           # judge fails when human fails
false_pass = jp_hf / (bf + jp_hf)  # judge passes a human-fail output
prec = bp / (bp + jp_hf)           # of judge passes, share human also passes
print("judge pass given human pass", round(sens, 3), "judge fail given human fail", spec, "false-pass rate", false_pass, "precision of judge pass", round(prec, 3))
assert round(sens, 3) == 0.917 and spec == 0.625 and false_pass == 0.375 and round(prec, 3) == 0.786
# Gating risk: of 1,000 outputs with 60% truly good, how many bad ones does the judge pass (illustrative)
bad_passed = 1000 * 0.4 * false_pass
print("bad outputs passed per 1,000 (40% truly bad):", bad_passed)
assert bad_passed == 150
# Bootstrap interval for kappa
rng = np.random.default_rng(11)
cells = np.array([bp, bf, jp_hf, jf_hp])
def k(c):
    c = np.asarray(c, float); nn = c.sum()
    a = (c[0]+c[1])/nn; jp = (c[0]+c[2])/nn; hp = (c[0]+c[3])/nn
    pe = jp*hp + (1-jp)*(1-hp)
    return (a-pe)/(1-pe)
ks = [k(rng.multinomial(n, cells/n)) for _ in range(5000)]
lo, hi = np.percentile(ks, [2.5, 97.5])
print("bootstrap 95% interval for kappa", round(lo, 3), round(hi, 3))
assert 0.43 < lo < 0.50 and 0.64 < hi < 0.70
# Judge net bias: passes 10 points more than humans
print("judge minus human pass rate", round(judge_pass - human_pass, 2))
assert round(judge_pass - human_pass, 2) == 0.10
```

**Output (my run):**
```text
agreement 0.8 judge pass 0.7 human pass 0.6
chance agreement 0.54 kappa 0.5652
judge pass given human pass 0.917 judge fail given human fail 0.625 false-pass rate 0.375 precision of judge pass 0.786
bad outputs passed per 1,000 (40% truly bad): 150.0
bootstrap 95% interval for kappa 0.443 0.68
judge minus human pass rate 0.1
```

**Follow-ups:**
- What kappa would you accept? There is no universal cutoff. Decide from the false-pass cost and the human-human kappa on the same task.
- How do you stop judge drift? Keep a fixed human-labelled anchor set, re-score it on every judge or prompt change and alert when agreement or false-pass rate moves.

**Common mistakes:**
- Reporting raw agreement only.
- Ignoring that the judge is more lenient than humans.
- Treating human labels as perfect.
- Using the same model to generate and to judge.
