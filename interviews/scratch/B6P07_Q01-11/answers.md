### Q1 ⭐⭐⭐ 🟢 A RAG assistant gives wrong answers even though the right document is in the index. You audit a sample of 100 failed answers and find 55 where the correct chunk was not in the top 5 retrieved, 20 where it was in the top 5 but the model ignored it, 15 where an outdated document was retrieved instead, and 10 with other causes. Which stage do you fix first, what do you measure next, and what do you tell the product owner about a 100-answer sample?
**Asked at:** RAG-debugging pages (Latitude, Educative, Redis, Fiddler and ChatRAG pages on locating the failing stage, stale indexes, retrieval recall versus faithfulness and reranking); practitioner and vendor material rather than a confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** I fix retrieval first, because 70 of the 100 failures (55 misses plus 15 stale hits) happen before the model sees the right text, and I tell the product owner that 100 failed answers give a good ranking of causes but not a failure rate.

**Clarifying questions:**
- Were the 100 failures drawn at random from all failures, or picked from complaints? Complaints over-represent loud users and skew the cause mix.
- How do we know the "correct chunk"? Who labelled it? If the labels are wrong, the 55 is wrong.
- Is "top 5" what the model actually receives, or is there a reranker or a cut after it? It tells me which stage dropped the chunk.
- What fraction of all answers fail? Without it I cannot say how much a fix is worth in the whole product.
- Does each document carry a date or version field? Without it the 15 stale cases have no cheap fix.

**Approach:**
1. Re-check the labels on a small subset (say 20 of the 100). Fix the labelling rule before trusting any share.
2. Fix order by size and by position in the pipeline. Retrieval is upstream: if the chunk is not retrieved, no prompt change can help.
3. For the 55 misses, look at the gold chunk's rank. If it is at 6 to 20, widen the first-stage fetch to 20 and add a reranker that keeps the top 5. If it is nowhere, look at chunking, embeddings, query rewriting, or a hybrid keyword plus vector search.
4. For the 15 stale cases, add document date and version metadata, filter or boost by recency, and re-index on change. Check that the index refresh job is working.
5. Only then look at the 20 ignored-context cases: prompt layout, chunk order, a "quote the source" instruction, a faithfulness check.
6. Re-run the same labelled failures plus a fresh random sample after each fix.

**Metrics:**
- Recall@k = queries whose gold chunk is in the top k / queries with a labelled gold chunk. Measure at k = 5 and k = 20.
- Gold-chunk rank (median and 90th percentile) on the 55.
- Faithfulness = answers fully supported by the retrieved text / answers judged. Measured on the 20 and on a random sample.
- Stale-hit rate = answers that cite an outdated version / answers on versioned topics.
- End-to-end answer correctness on a fixed, random, labelled set. Guardrails: latency (a reranker adds time) and cost per query.

**Risks:**
- The sample is failures only. A fix can win on these and break answers that were passing.
- One failure can have two causes (not in top 5 and also a stale copy). The categories are a forced single choice.
- Raising k adds noise to the prompt and can make the model ignore the right chunk more often (the 20 grows).
- The reranker or metadata filter adds latency and one more thing to monitor.

**What the interviewer scores:**
- Strong: names the stage using the evidence (retrieval 70 versus generation 20) and explains why upstream goes first. Weak: "improve the prompt".
- Strong: separates the three retrieval ideas (recall, reranking, freshness). Weak: "use a better embedding model" for everything.
- Strong: says the share is among failures, gives an interval, and asks for a random sample. Weak: reads 55 as "55% of answers fail".
- Strong: ends with a re-measure plan. Weak: no definition of done.

**Example:** (illustrative numbers) 55 misses: say 33 have the gold chunk at rank 6 to 20 and 22 have it nowhere. A reranker over the top 20 plausibly rescues most of the 33 (assume 60% of the 55 overall, so 33). The 15 stale cases: a version filter fixes 80%, so 12. Together 45 of 100 failures removed. If 8% of all answers fail today, that is about 4.4% after the fix (the 8% is invented). Weak answer: "The model is hallucinating, so I will rewrite the system prompt and lower the temperature." Strong answer: "Seventy of the hundred failures are retrieval, 55 misses and 15 stale. I fix those first with a reranker over the top 20 and a version filter. The 20 ignored-context cases come second. A 55 out of 100 share has an interval of roughly 45 to 64 percent, so the order is safe, the exact number is not, and it is a share of failures, not of all answers."

**Code:**
```python
import math
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
# Illustrative audit of 100 FAILED answers (the denominator is failures, not all traffic)
audit = {"gold chunk not in top 5": 55, "in top 5, model ignored it": 20,
         "outdated doc retrieved": 15, "other": 10}
assert sum(audit.values()) == 100
for k, v in audit.items():
    lo, hi = wilson(v, 100)
    print(f"{k:28} {v:3d}%  95% Wilson {lo:.1%} to {hi:.1%}")
lo, hi = wilson(55, 100); assert round(lo, 3) == 0.452 and round(hi, 3) == 0.644
lo2, hi2 = wilson(20, 100); assert hi2 < lo   # 20% interval sits fully below the 55% interval
# retrieval-side total = miss + stale
ret = 55 + 15; print("retrieval-side causes:", ret, "of 100")
assert ret == 70
# What if the fix wins back 60% of the misses and 80% of the stale cases?
fixed = 0.6*55 + 0.8*15; print("failures removed by that fix:", fixed, "of 100")
assert fixed == 45.0
# Failure rate needs the denominator: if 8% of all answers fail, the fix moves 8% -> 8% * (1 - .45)
print(f"overall failure rate 8.0% -> {8*(1-fixed/100):.1f}%")
assert round(8*(1-fixed/100), 1) == 4.4
# Sample size to pin the miss share to +/-5 points (normal approx, worst case p=0.5)
n = math.ceil((1.96*0.5/0.05)**2); print("n for +/-5 points:", n); assert n == 385
```

**Output (my run):**
```text
gold chunk not in top 5       55%  95% Wilson 45.2% to 64.4%
in top 5, model ignored it    20%  95% Wilson 13.3% to 28.9%
outdated doc retrieved        15%  95% Wilson 9.3% to 23.3%
other                         10%  95% Wilson 5.5% to 17.4%
retrieval-side causes: 70 of 100
failures removed by that fix: 45.0 of 100
overall failure rate 8.0% -> 4.4%
n for +/-5 points: 385
```

**Follow-ups:**
- Why not fix the 20 where the model ignored the right chunk, since it is the cheapest prompt change? It can be done in parallel, but it is the smaller bucket (20 versus 70) and the interval for 20 sits wholly below the interval for 55. Retrieval first.
- How many samples do I need? About 385 for plus or minus 5 points on a share, worst case. For a failure rate I need a random sample of all traffic, not only failures.
- Does top 5 matter, or the doc? It matters because the model only sees what is passed in. Recall@5 and recall@20 tell me whether the problem is the first stage or the cut.

**Common mistakes:**
- Treating "55 of 100 failures" as "55% of answers".
- Fixing the stage that is easiest to change rather than the largest upstream one.
- Raising k without a reranker and then seeing the model ignore the right chunk.
- No labelled gold chunk, so no recall number.
- Ignoring document freshness because the index "has the document".

### Q2 ⭐⭐⭐ 🟢 A legal-summary assistant is suspected of hallucinating, and 36 of 300 randomly sampled answers contain at least one claim the source does not support. Compute the measured rate with a 95% Wilson interval, and say what the number does and does not tell you about answers outside the sample. How would you define a hallucination for the annotators, and what target would you propose?
**Asked at:** GenAI and LLM-engineer interview guides (InterviewBit, Hyring, Let's Code, recrew, Pensero and Towards AI 2026 pages list RAG, hallucination mitigation, evaluation and cost or latency topics; one guide reports a prompt about a RAG answer that is wrong although the right document exists, and another a smaller-model-for-narrow-tasks answer pattern); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The measured rate is 12% (36 of 300) with a 95% Wilson interval of about 8.8% to 16.2%, and that describes answers like the sample only if the sample was random and the annotators agree on the definition.

**Clarifying questions:**
- Random from what population: all queries last month, or only ones that passed some filter? The interval speaks only for the population sampled.
- Is the unit an answer or a claim? "At least one unsupported claim per answer" is an answer-level rate, and long answers fail more often.
- Who annotated, and how many annotators per answer? One tired annotator gives a noisy number.
- What counts as "the source"? The retrieved documents, the full case file, or the public record? It changes what "supported" means.
- What is the harm of one error? In legal text a wrong citation is worse than a loose paraphrase, so severity matters.

**Approach:**
1. Compute the rate and the Wilson interval. Wilson is better than the plain normal formula near small rates and small samples.
2. State what it covers: answers drawn the same way as the sample, at the time of the sample. Not other months, other document types or another model version.
3. Write an annotation guide (below), pilot it on 30 answers with two annotators, and compute agreement. Fix the guide where they disagree.
4. Split the 36 by type (invented fact, wrong citation, overstated certainty, missing negation) and by severity. The fix depends on the type.
5. Propose a target in two parts: a number and the evidence needed to claim it.
6. Add production monitoring: a weekly random sample plus an automatic check that every claim has a quoted span from the source.

**Metrics:**
- Unsupported-answer rate = answers with at least one unsupported claim / answers audited. Here 36 / 300 = 12%.
- Claim-level rate = unsupported claims / all claims checked. Report it too, because it is stable when answers get longer.
- Severity-weighted rate = sum of weights (minor 1, material 5, wrong-citation 10, invented) / answers audited. Weights are a business decision, written down.
- Annotator agreement (Cohen's kappa or simple percent agreement) on the pilot.
- Guardrail: the abstain rate ("I cannot find this in the source"). A model that always abstains has zero hallucinations and no value.

**Risks:**
- Non-random sample (easy questions, recent questions) so the 12% is not the real rate.
- The interval covers sampling noise only. It does not cover annotator error or a fuzzy definition.
- Goodhart: if the target is "under 5%" and the model learns to abstain or hedge, the rate falls and value falls with it.
- One annotator who is lenient or strict moves the number more than the interval suggests.

**What the interviewer scores:**
- Strong: correct interval, the unit (answer or claim) stated, and the "inside the sample only" caveat. Weak: "12%, so 12% of all answers are wrong."
- Strong: a definition annotators can apply (supported, contradicted, absent from source) with an agreement check. Weak: "I will know it when I see it."
- Strong: a target with the sample size needed to prove it. Weak: "zero hallucinations."
- Strong: mentions severity and abstention. Weak: one single rate.

**Example:** (illustrative numbers) Definition for annotators: for each factual claim in the answer, mark SUPPORTED (a span in the cited source says it), CONTRADICTED (the source says otherwise), or NOT FOUND (the source does not say it). Hallucination = any claim that is CONTRADICTED or NOT FOUND, whether or not it happens to be true in the real world. Measured: 36 of 300 = 12%, interval 8.8% to 16.2%. If those 300 are a random draw from last month's traffic, that is between about 880 and 1,620 answers per 10,000. If the average answer has 8 claims and each bad answer has exactly one bad claim, the claim-level rate is 1.5%, so report both. A target check: with 300 answers, 7 or fewer bad ones keep the upper bound at or under 5%, and 8 or more do not. To prove under 5% the audit needs, for example, at most 15 bad answers out of 500 (upper bound 4.89%). Weak answer: "It is 12 percent, so we have a 12 percent hallucination problem everywhere and I will lower the temperature." Strong answer: "The measured rate is 12 percent, plausibly 9 to 16 percent, for this sample's population. It says nothing about other document types or next month. I would define a hallucination as any claim the cited source does not support, check annotator agreement first, and propose under 5 percent on high-severity errors with the sample size to show it."

**Code:**
```python
import math
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
k, n = 36, 300
lo, hi = wilson(k, n)
print(f"rate {k/n:.1%}, 95% Wilson {lo:.1%} to {hi:.1%}")
assert k/n == 0.12 and round(lo, 3) == 0.088 and round(hi, 3) == 0.162
# Wald interval for comparison (worse near 0 or small n)
se = math.sqrt(0.12*0.88/300); print(f"Wald {0.12-1.96*se:.1%} to {0.12+1.96*se:.1%}")
# Outside the sample: expected unsupported answers per 10,000 (only if sample is random from that population)
print(f"per 10,000 answers: {lo*1e4:.0f} to {hi*1e4:.0f}")
# Answers vs claims: if an answer has ~8 claims, an answer-level 12% is a much lower claim-level rate
claims = 8
claim_rate_if_one_bad_claim = 0.12 / claims
print(f"if each bad answer has exactly 1 bad claim in {claims}: claim-level rate {claim_rate_if_one_bad_claim:.2%}")
assert round(claim_rate_if_one_bad_claim, 4) == 0.015
# Target: what observed rate lets a 300-sample audit prove <= 5%? Need the Wilson upper bound <= 5%
best = max(kk for kk in range(0, 301) if wilson(kk, 300)[1] <= 0.05)
print("max bad answers out of 300 with upper bound <= 5%:", best, "->", f"{best/300:.2%}")
assert best == 7 and wilson(7, 300)[1] <= 0.05 < wilson(8, 300)[1]
# Sample size needed to show upper bound <= 5% if the true rate is 3%
for N in (300, 500, 1000):
    kk = round(0.03*N); print(N, kk, f"upper {wilson(kk, N)[1]:.2%}")
assert wilson(9, 300)[1] > 0.05 and wilson(15, 500)[1] < 0.05 and wilson(30, 1000)[1] < 0.05
```

**Output (my run):**
```text
rate 12.0%, 95% Wilson 8.8% to 16.2%
Wald 8.3% to 15.7%
per 10,000 answers: 880 to 1617
if each bad answer has exactly 1 bad claim in 8: claim-level rate 1.50%
max bad answers out of 300 with upper bound <= 5%: 7 -> 2.33%
300 9 upper 5.60%
500 15 upper 4.89%
1000 30 upper 4.25%
```

**Follow-ups:**
- Why Wilson and not the plain normal interval? It stays inside 0 to 1 and behaves better at small rates and small n. Here the difference is small (Wald 8.3% to 15.7%), but near 2% it is large.
- Does the interval cover bias? No. Only sampling noise from a random draw.
- How do you scale the audit? Use an LLM judge for coverage, validated against human labels on a smaller sample, and keep humans on the high-severity cases.

**Common mistakes:**
- Reading the interval as covering other months, other models or other document types.
- Counting only "false in the real world" instead of "not supported by the source".
- No agreement check between annotators.
- A target of zero, or a target with no sample size to prove it.
- One blended rate, with no severity and no abstain rate.

### Q3 ⭐⭐⭐ 🟢 A support chatbot makes 50,000 calls a day, each with 2,000 input and 400 output tokens, at illustrative prices of 3 per million input tokens and 15 per million output tokens. The monthly budget was 6,000 for a 30-day month. Compute the actual monthly cost and name the first three levers you would pull, with a rough saving for each.
**Asked at:** LLM cost and routing pages (getmaxim cost and semantic-cache guides, tianpan and system-design.space pages on routing and cascades, a Towards Data Science article on saving tokens in agentic AI, a Towards AI piece on AI system-design interview patterns); practitioner material, no confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The bill is 18,000 a month, three times the 6,000 budget, and I would pull three levers in this order: cache the static prompt prefix, cap and tighten the output, and route easy calls to a cheaper model, each measured against answer quality.

**Clarifying questions:**
- Did volume or tokens per call grow, or was the budget simply wrong? It decides whether this is a bug or a planning error.
- What is in the 2,000 input tokens? If 1,500 are the same system prompt and policy text every time, caching pays; if they are retrieved and different every time, it does not.
- What quality bar must each call meet, and can I measure it? Every saving here is paid for with a possible quality loss.
- How many of the 50,000 daily calls are simple (order status, opening hours)? That sets how much I can route cheaply.
- Is a price change or a volume discount available? It is the cheapest lever and takes no engineering.

**Approach:**
1. Compute the baseline per call and the split between input and output. Here input is 2,000 x 3 / 1e6 = 0.006 and output is 400 x 15 / 1e6 = 0.006, so each is half.
2. Log token counts by call type for a week. Find the top three call types by spend.
3. Lever 1, prefix caching: put the stable text first and the changing text last, and use the provider's caching if it exists (editor knowledge: caching features and discounts differ by vendor, so I check the current docs).
4. Lever 2, output control: ask for shorter answers, set a max-tokens limit, ask for structured fields instead of prose. Output tokens cost 5x input tokens at these prices.
5. Lever 3, routing: send simple intents to a smaller model, escalate on low confidence or a failed check.
6. Re-run the quality eval after each lever. Stop when the bill is within budget and quality is within tolerance.

**Metrics:**
- Cost per call = (input tokens x input price + output tokens x output price) / 1,000,000.
- Monthly cost = cost per call x calls per day x 30.
- Cost per resolved conversation = total spend / conversations resolved without a human. This is the number that matters, not cost per call.
- Cache hit rate = cached input tokens / total input tokens.
- Guardrails: answer-correctness on a fixed eval, escalation rate to human, customer satisfaction. A saving that doubles escalations is not a saving.

**Risks:**
- Shorter answers may drop needed detail, so the customer calls back.
- A cheaper model may fail on edge cases that I did not put into the eval.
- Cache hit rates in a test are higher than in production if prompts drift or change often.
- The savings overlap, so adding them up overstates the result.

**What the interviewer scores:**
- Strong: correct arithmetic (18,000, 3x budget) and the input/output split before any lever. Weak: "use a cheaper model".
- Strong: levers ranked by saving, effort and risk, with a rough saving each. Weak: a list with no numbers.
- Strong: notes the savings overlap and that quality must be re-measured. Weak: sums the three savings and claims a 15,000 reduction.
- Strong: cost per resolved conversation. Weak: only cost per call.

**Example:** (illustrative prices and assumptions) Baseline 0.012 per call, 600 a day, 18,000 a month. Lever 1, cache a 1,500-token prefix, cached tokens at 10% of the input price, 80% hit rate: saves 4,860 a month (27%). Lever 2, output from 400 to 250 tokens: saves 3,375 (18.8%). Lever 3, route 50% of calls to a model at one fifth of the price: saves 7,200 (40%) when taken alone. Together, applied in order, the bill is 5,859 a month, a saving of 12,141, not the 15,435 you get by adding them. That is just under budget, so I would still check quality and keep a margin. Weak answer: "That is too expensive, switch to a smaller model and cache everything." Strong answer: "Eighteen thousand against six, so three times over. Half is input, half is output. I would cache the static prefix, cap the answer length, and route simple intents to a cheaper model. About 5,000, 3,400 and 7,000 each if alone, around 12,000 together because they overlap, and I would re-run the quality eval after each."

**Code:**
```python
# ILLUSTRATIVE round prices, not any vendor's prices: 3 per million input tokens, 15 per million output tokens
PIN, POUT = 3.0, 15.0
def call_cost(tin, tout, pin=PIN, pout=POUT): return (tin*pin + tout*pout) / 1e6
calls_day, days = 50_000, 30
base = call_cost(2000, 400)
month = base * calls_day * days
print(f"per call {base:.4f}; per day {base*calls_day:,.0f}; per month {month:,.0f}; budget 6,000 -> {month/6000:.1f}x")
assert round(base, 6) == 0.012 and round(month) == 18000 and month == 3*6000
print(f"input share {2000*PIN/1e6/base:.0%}, output share {400*POUT/1e6/base:.0%}")
assert 2000*PIN/1e6/base == 0.5
# Lever 1: shorter answers, 400 -> 250 output tokens
l1 = call_cost(2000, 250); s1 = (base - l1) * calls_day * days
print(f"L1 cap output at 250: saves {s1:,.0f}/month ({s1/month:.1%})"); assert round(s1) == 3375
# Lever 2: cache a static 1,500-token prefix; cached tokens at 10% of input price (illustrative), 80% hit rate
hit, cache_price = 0.8, 0.10*PIN
eff_in = 1500*(hit*cache_price + (1-hit)*PIN)/1e6 + 500*PIN/1e6
l2 = eff_in + 400*POUT/1e6; s2 = (base - l2) * calls_day * days
print(f"L2 prefix cache: saves {s2:,.0f}/month ({s2/month:.1%})"); assert round(s2) == 4860
# Lever 3: route 50% of calls to a model at one fifth of the prices
share, ratio = 0.5, 0.2
s3 = base * share * (1 - ratio) * calls_day * days
print(f"L3 route 50% to a 1/5-price model: saves {s3:,.0f}/month ({s3/month:.1%})"); assert round(s3) == 7200
# Combined (apply in order, savings overlap): L1 and L2 on all calls, then L3 on half
combo_call = (eff_in + 250*POUT/1e6)
combo = combo_call*(1 - share) * calls_day*days + combo_call*ratio*share * calls_day*days
print(f"all three together: {combo:,.0f}/month; budget 6,000"); assert round(combo) == 5859
print("single levers do not add up; sum would be", round(s1+s2+s3), "but combined saving is", round(month-combo))
assert combo < 6000 < month and (s1+s2+s3) > (month - combo)
```

**Output (my run):**
```text
per call 0.0120; per day 600; per month 18,000; budget 6,000 -> 3.0x
input share 50%, output share 50%
L1 cap output at 250: saves 3,375/month (18.8%)
L2 prefix cache: saves 4,860/month (27.0%)
L3 route 50% to a 1/5-price model: saves 7,200/month (40.0%)
all three together: 5,859/month; budget 6,000
single levers do not add up; sum would be 15435 but combined saving is 12141
```

**Follow-ups:**
- What if the savings come with a quality drop? I set a quality floor first (for example no worse than 1 point on the eval), then take savings until I reach it.
- Would a semantic cache help? It can for repeated questions, but a similar question with a different right answer gets a wrong cached reply, so I would measure the wrong-hit rate before turning it on.
- Is the price per token the whole bill? No. Retries, long conversations and tool calls add tokens, so I check total tokens per resolved conversation.

**Common mistakes:**
- Adding up the individual savings as if they were independent.
- Cutting output length without checking whether customers then need a second call.
- Forgetting that output tokens are priced 5 times input here.
- Treating illustrative prices as vendor prices.
- Optimising cost per call and not cost per resolved conversation.

### Q4 ⭐⭐⭐ 🟢 A chat feature has a time to first token of 0.8 seconds and generates 40 tokens per second, and typical answers are 300 tokens long. Users say it feels slow, and the product budget is 5 seconds end to end. Compute the time to the last token and the time to the first visible text with streaming, and say which of the two a user feels and what you would cut.
**Asked at:** GenAI and LLM-engineer interview guides (InterviewBit, Hyring, Let's Code, recrew, Pensero and Towards AI 2026 pages list RAG, hallucination mitigation, evaluation and cost or latency topics; one guide reports a prompt about a RAG answer that is wrong although the right document exists, and another a smaller-model-for-narrow-tasks answer pattern); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Time to the last token is 0.8 + 300/40 = 8.3 seconds, over the 5-second budget by 3.3, while with real streaming the first visible text appears at about 0.8 seconds; a user feels the first number as responsiveness, and I would cut answer length first.

**Clarifying questions:**
- Is streaming actually switched on in the UI, or does the page wait for the whole reply? If not, first visible text is also 8.3 seconds.
- Where is the 0.8 seconds measured: at the model server or in the user's browser? Retrieval, guardrails, queueing and network add to what the user sees.
- Is the 5-second budget about the full answer or about the first text? It decides which number I must fix.
- Does anything downstream need the full answer (JSON parse, a tool call, text to speech)? Then the last token is the real wait.
- What is the 95th percentile, not just the average? Users feel the slow tail.

**Approach:**
1. Compute both numbers: generation = 300 / 40 = 7.5 seconds, last token = 0.8 + 7.5 = 8.3 seconds, first text = 0.8 seconds (streaming).
2. Check streaming end to end, and measure from the client, with a timeline: network, gateway, retrieval, guardrail, queue, model first token, decode.
3. Fit the answer to the budget: at 40 tokens per second, 5 seconds allows (5 - 0.8) x 40 = 168 tokens. So cut the average answer from 300 to about 150, which gives 0.8 + 150/40 = 4.55 seconds.
4. Then work on speed: a smaller or faster model, shorter prompt (less prefill), speculative decoding or a faster serving setup (editor knowledge: availability depends on the provider).
5. Show progress in the UI (a typing indicator, partial results) for anything that must stay slow.

**Metrics:**
- Time to first token (TTFT) = time from user send to first token on screen. Measured at the client.
- Time to last token = time from send to the last token.
- Decode speed = output tokens / (time to last token - time to first token).
- p50 and p95 of each. Guardrails: answer quality (a shorter answer must still solve the problem) and follow-up rate.

**Risks:**
- Cutting length may cut needed content and raise follow-up questions.
- A faster model may be less accurate.
- The average hides the long answers: a p95 answer of 600 tokens takes 0.8 + 15 = 15.8 seconds.
- Streaming makes partial text visible before a guardrail has checked it.

**What the interviewer scores:**
- Strong: both numbers computed correctly (8.3 and 0.8) and a clear statement of which one the budget and the user care about. Weak: one number, or "it is just slow".
- Strong: compares levers with arithmetic (shorter answer versus faster decode versus only TTFT). Weak: "use a faster GPU".
- Strong: asks where the clock starts, since the 0.8 is not the whole pipeline. Weak: trusts the server number.
- Strong: mentions quality and tail latency. Weak: ignores them.

**Example:** (illustrative numbers) Today: 0.8 + 300/40 = 8.3 seconds. Only reducing TTFT to 0.3 gives 7.8 seconds, still far over budget. Doubling decode speed to 80 tokens per second gives 4.55 seconds, and halving the answer to 150 tokens at 40 tokens per second also gives 4.55 seconds. Both together, with TTFT 0.5, gives 2.38 seconds. As a reading check (a rule of thumb, editor knowledge, not measured here): a person reads about 4 words, roughly 5 tokens, a second, so the stream at 40 tokens per second is already faster than a reader, and 300 tokens is a minute of reading. So length is the main lever. Weak answer: "The total is 8.3 seconds, so we need a faster model." Strong answer: "Last token is 8.3 seconds, 3.3 over the budget. With streaming the user sees text at 0.8 seconds, so it should feel acceptable if streaming works. If it feels slow I check streaming and client-side TTFT first, then I cut the answer to about 150 tokens, which lands at 4.55 seconds."

**Code:**
```python
ttft, tps, tokens, budget = 0.8, 40.0, 300, 5.0
gen = tokens / tps
last = ttft + gen
print(f"generation time {gen:.2f}s; time to last token {last:.2f}s; over budget by {last-budget:.2f}s")
assert gen == 7.5 and round(last, 1) == 8.3 and round(last-budget, 1) == 3.3
print(f"first visible text: streaming {ttft:.1f}s (plus network/render), no streaming {last:.1f}s")
# What fits in 5 s at 40 tok/s?
max_tokens = (budget - ttft) * tps
print(f"max answer length inside budget at 40 tok/s: {max_tokens:.0f} tokens"); assert round(max_tokens) == 168
# Or what speed is needed for 300 tokens?
need = tokens / (budget - ttft); print(f"needed speed for 300 tokens: {need:.1f} tok/s"); assert round(need, 1) == 71.4
# Options (illustrative)
for name, t, s, n in [("shorter answer 300->150", ttft, tps, 150),
                      ("faster decode 40->80 tok/s", ttft, 80, 300),
                      ("both, TTFT 0.8->0.5", 0.5, 80, 150),
                      ("only TTFT 0.8->0.3", 0.3, 40, 300)]:
    print(f"{name:28} last token {t + n/s:.2f}s")
assert 0.8 + 150/40 == 4.55 and 0.8 + 300/80 == 4.55 and 0.5 + 150/80 == 2.375 and 0.3 + 300/40 == 7.8
# Reading speed rule of thumb (editor knowledge, not measured here): ~4 words/s, ~1.3 tokens/word -> ~5 tokens/s
read_tps = 4*1.3
print(f"reader keeps pace at ~{read_tps:.1f} tok/s; stream is {tps/read_tps:.1f}x faster; reading 300 tokens takes ~{tokens/read_tps:.0f}s")
assert round(tps/read_tps, 1) == 7.7
```

**Output (my run):**
```text
generation time 7.50s; time to last token 8.30s; over budget by 3.30s
first visible text: streaming 0.8s (plus network/render), no streaming 8.3s
max answer length inside budget at 40 tok/s: 168 tokens
needed speed for 300 tokens: 71.4 tok/s
shorter answer 300->150      last token 4.55s
faster decode 40->80 tok/s   last token 4.55s
both, TTFT 0.8->0.5          last token 2.38s
only TTFT 0.8->0.3           last token 7.80s
reader keeps pace at ~5.2 tok/s; stream is 7.7x faster; reading 300 tokens takes ~58s
```

**Follow-ups:**
- Which number does the user feel? With streaming, mostly the first text (0.8 seconds) and then the pace of reading. Without streaming or when something waits for the full answer, the last token.
- What if long answers are needed? Stream, show structure first (a summary line, then detail), and let the user stop it.
- Does a shorter prompt help? Yes, a little for TTFT (less prefill work), but it does nothing for the 7.5 seconds of decoding.

**Common mistakes:**
- Reporting only TTFT and calling the feature fast.
- Forgetting the time before the model call (retrieval, guardrails, network).
- Optimising TTFT when decode time dominates: 7.5 of the 8.3 seconds is decoding.
- Cutting length with no quality check.
- Using the average and ignoring p95.

### Q5 ⭐⭐⭐ 🟢 A safety filter sits in front of an assistant. Of 100,000 weekly queries, 2,000 are truly harmful and 98,000 are benign, and the filter blocks 1,800 of the harmful queries and 3,000 of the benign ones. Compute the block rate on benign queries, the recall on harmful queries and the share of all blocks that are correct, and say how you would tune the filter.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to guardrail and over-refusal topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Benign block rate is 3,000 / 98,000 = 3.06%, recall on harmful is 1,800 / 2,000 = 90%, and only 1,800 / 4,800 = 37.5% of blocks are correct, so the threshold should be tuned by the cost of a miss versus the cost of a wrong block, with a review band instead of a hard block in the middle.

**Clarifying questions:**
- How were the 2,000 "truly harmful" labelled, and is that count itself an estimate? Every number here depends on those labels.
- Is a block a hard refusal, or can the assistant answer safely with a warning? The cost of a wrong block depends on it.
- What is the cost of a missed harmful query versus a wrongly blocked benign one? That ratio picks the threshold.
- Are there categories (self-harm, weapons, medical) with different tolerances? One threshold for all is rarely right.
- Is the 2% harmful share stable? A change in prevalence changes precision even if the filter does not change.

**Approach:**
1. Build the confusion table: true positive 1,800, false negative 200, false positive 3,000, true negative 95,000. Check it adds to 100,000.
2. Compute three rates: benign block rate (false positive rate), recall, and precision (share of blocks that are correct).
3. Read it in plain words: for each harmful query caught, 1.67 benign users are blocked (3,000 / 1,800).
4. Plot recall against benign block rate for a range of thresholds on a labelled set (a ROC or precision-recall curve) and choose a point with an explicit cost ratio.
5. Use tiers: auto-block only at a high score, a soft response or human review in the middle band, allow below. Add per-category thresholds.
6. Review a weekly sample of blocked benign queries and of missed harmful ones, and retrain or adjust rules from them.

**Metrics:**
- Benign block rate = benign blocked / all benign = 3,000 / 98,000 = 3.06%.
- Recall (harmful caught) = harmful blocked / all harmful = 1,800 / 2,000 = 90%.
- Precision of blocks = harmful blocked / all blocked = 1,800 / 4,800 = 37.5%.
- Expected cost = misses x cost of miss + wrong blocks x cost of wrong block.
- Guardrails: user complaints and appeal rate, and the miss rate in the top-severity categories.

**Risks:**
- Precision looks bad because harmful traffic is only 2%. Even a small false positive rate on 98,000 benign queries gives many blocks.
- Optimising precision alone lets harmful queries through; optimising recall alone makes the product unusable.
- Labels for "harmful" are subjective at the edges, so the 90% has an error bar of its own.
- Attackers adapt, so a filter measured today is weaker next month.

**What the interviewer scores:**
- Strong: three correct numbers with named denominators (98,000 benign, 2,000 harmful, 4,800 blocks). Weak: one "accuracy" number (it would be 96.8%, and useless here).
- Strong: explains why precision is low (base rate) and not just that it is low. Weak: "the filter is bad".
- Strong: tunes by a stated cost ratio and shows the answer can flip. Weak: "raise the threshold" without a reason.
- Strong: tiers, categories and a review sample. Weak: one global threshold.

**Example:** (illustrative numbers) Accuracy would be (1,800 + 95,000) / 100,000 = 96.8%, which hides the problem. Three operating points: current (recall 90%, 3,000 benign blocked, 200 missed), stricter-on-benign (recall 85%, 980 benign blocked, 300 missed, precision 63.4%) and looser (recall 95%, 7,840 benign blocked, 100 missed, precision 19.5%). If one miss costs 50 wrong blocks, the looser filter is cheapest (12,840 against 13,000 and 15,980). If a miss costs only 10 wrong blocks, the stricter one wins (3,980). So I must ask for the cost ratio. Weak answer: "Accuracy is 96.8%, so the filter is good." Strong answer: "It blocks 3 percent of benign traffic, catches 90 percent of harmful queries, and only 37.5 percent of blocks are correct, because harmful traffic is 2 percent of the total. I would pick the threshold by the cost of a miss versus a wrong block, and use a review band in the middle."

**Code:**
```python
harm, benign = 2_000, 98_000
tp, fp = 1_800, 3_000
fn = harm - tp
fpr = fp / benign; recall = tp / harm; precision = tp / (tp + fp)
print(f"benign block rate {fpr:.2%}; recall {recall:.0%}; precision {precision:.1%}; missed harmful {fn}; total blocks {tp+fp}")
assert round(fpr, 4) == 0.0306 and recall == 0.9 and precision == 0.375 and fn == 200 and harm + benign == 100_000
print(f"prevalence {harm/(harm+benign):.0%}; benign users blocked per harmful caught: {fp/tp:.2f}")
assert round(fp/tp, 2) == 1.67
# Tuning: compare two illustrative operating points on the same 100,000 queries
def point(name, rec, fpr_):
    t = rec*harm; f = fpr_*benign
    print(f"{name:22} recall {rec:.0%} fpr {fpr_:.2%} blocks {t+f:,.0f} precision {t/(t+f):.1%} missed {harm-t:.0f} benign blocked {f:,.0f}")
    return t, f
point("current", 0.90, 3000/98000)
a = point("stricter on benign", 0.85, 0.01)
b = point("looser", 0.95, 0.08)
assert round(a[0]/(a[0]+a[1]), 3) == 0.634 and round(b[1]) == 7840
# Cost-weighted choice: the best point depends on the cost ratio (illustrative: one miss = 50 or 10 wrongly blocked benign queries)
pts = {"current": (0.90, 3000/98000), "stricter": (0.85, 0.01), "looser": (0.95, 0.08)}
def cost(rec, fpr_, cm): return (1-rec)*harm*cm + fpr_*benign
for cm in (50, 10):
    c = {k: round(cost(r, f, cm)) for k, (r, f) in pts.items()}
    print(f"miss costs {cm}x a wrong block:", c, "-> best:", min(c, key=c.get))
assert {k: round(cost(r, f, 50)) for k, (r, f) in pts.items()} == {"current": 13000, "stricter": 15980, "looser": 12840}
assert {k: round(cost(r, f, 10)) for k, (r, f) in pts.items()} == {"current": 5000, "stricter": 3980, "looser": 8840}
# Two-tier idea: block only above a high score; mid band goes to a soft-refuse / human review (illustrative split)
hi_tp, hi_fp = 1500, 200; mid_tp, mid_fp = 300, 2800
print(f"two-tier: auto-block {hi_tp+hi_fp} (precision {hi_tp/(hi_tp+hi_fp):.1%}); review band {mid_tp+mid_fp} (precision {mid_tp/(mid_tp+mid_fp):.1%})")
assert hi_tp + mid_tp == tp and hi_fp + mid_fp == fp and round(hi_tp/(hi_tp+hi_fp), 3) == 0.882
```

**Output (my run):**
```text
benign block rate 3.06%; recall 90%; precision 37.5%; missed harmful 200; total blocks 4800
prevalence 2%; benign users blocked per harmful caught: 1.67
current                recall 90% fpr 3.06% blocks 4,800 precision 37.5% missed 200 benign blocked 3,000
stricter on benign     recall 85% fpr 1.00% blocks 2,680 precision 63.4% missed 300 benign blocked 980
looser                 recall 95% fpr 8.00% blocks 9,740 precision 19.5% missed 100 benign blocked 7,840
miss costs 50x a wrong block: {'current': 13000, 'stricter': 15980, 'looser': 12840} -> best: looser
miss costs 10x a wrong block: {'current': 5000, 'stricter': 3980, 'looser': 8840} -> best: stricter
two-tier: auto-block 1700 (precision 88.2%); review band 3100 (precision 9.7%)
```

**Follow-ups:**
- Would you pick a recall target? Yes, per category: very high for the severe categories, lower for the mild ones, and I report the benign block rate beside it.
- How do you check the false positives cheaply? Sample 200 blocked benign queries a week, read them, and group by reason.
- What if prevalence doubles to 4%? Precision rises (more of the blocks are real harm) without any change to the filter, so I track prevalence separately.

**Common mistakes:**
- Reporting accuracy on a 2% positive class.
- Calling precision "bad filter quality" when the base rate explains most of it.
- One threshold for every harm category.
- Counting blocks without counting what they cost the benign user.
- Treating the label counts as exact.

### Q6 ⭐⭐⭐ 🟡 A support bot that can issue refunds reads customer emails, and a red team plants hidden instructions in 200 test emails. In 17 of them (8.5% of the 200, a measured sample) the bot issued a refund it should not have. What do you do in the first hour, and what structural change would you make instead of only editing the prompt?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to prompt-injection and guardrail topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** In the first hour I take the refund action out of the bot's hands (human approval or a low hard cap), check the logs for real refunds that followed the same pattern, and then fix the design so that email text can never authorise a payment, because no prompt edit makes that guarantee.

**Clarifying questions:**
- Can the bot refund any amount to any customer, or is there already a cap and an order check? It sets how bad one success is.
- Has any real refund in production followed an email with odd instructions? That decides whether this is a test finding or an incident.
- What other tools can the bot call (email, account change, data lookup)? The same hole may be open there.
- Who owns refund policy and who can approve an emergency change? I need a name before I switch anything off.
- Were the 200 test emails a mix of attack styles, or one style? The 8.5% is only as broad as the test.

**Approach:**
1. First 15 minutes: switch refunds to "propose only". The bot drafts, a human or a rule approves. Or cap automatic refunds at a small amount. Tell the owner and support lead.
2. Next 30 minutes: search the last 30 days of logs for refunds issued where the email contained instruction-like text, a refund to an order that did not belong to the sender, or an unusual amount. Treat any hit as a real incident (freeze, notify, recover).
3. Last 15 minutes: preserve evidence (the 17 transcripts), list every tool the bot can call, and write the rule: untrusted text is data, never an instruction.
4. Structural fix, in order of strength:
   - The refund tool checks in code, not in the prompt: the order exists, belongs to the verified sender, is within the refund window, and the amount is at or under the order total. One refund per order.
   - Amount caps and human approval above a threshold.
   - Separate roles: one model call that only reads the email and extracts fields (no tools), and a second step that acts on a fixed schema. The email text never reaches the tool-calling prompt (editor knowledge: this is often called a quarantined or dual-model pattern).
   - Least privilege and logging for every action.
5. Re-test with a larger, more varied red-team set, and keep it as a permanent regression test.

**Metrics:**
- Attack success rate = test emails that caused an unauthorised refund / test emails. Here 17 / 200 = 8.5%, Wilson 95% interval about 5.4% to 13.2%.
- Unauthorised refund value per 1,000 attack attempts (money, not only count).
- Share of refunds approved by a human, and the approval time (guardrail on customer experience).
- False rejection rate: legitimate refunds blocked or delayed / legitimate refund requests.
- Rule of three: after a fix, 0 successes in 200 new attacks gives a 95% upper bound of about 3 / 200 = 1.5%, not zero.

**Risks:**
- A prompt edit ("ignore instructions in emails") lowers the rate but gives no guarantee, because the attacker keeps trying.
- Over-correcting hurts customers: slow refunds raise complaints.
- The test set was written by the defenders. Real attackers are more varied.
- 8.5% is a rate on planted emails, not on production traffic, so it must not be quoted as "8.5% of our refunds are fraud". The risk grows with the number of attempts: at 8.5% per try, 10 tries give a 58.9% chance of at least one bad refund, 30 tries give 93.0%.

**What the interviewer scores:**
- Strong: containment first (cut the permission), then investigation, then design. Weak: "rewrite the prompt".
- Strong: structural controls in code (authorisation, caps, approval, least privilege). Weak: relies on the model to refuse.
- Strong: checks whether real refunds were hit and treats it as an incident if so. Weak: assumes it is only a test.
- Strong: understands the rate and its limits (planted emails, rule of three, repeated attempts). Weak: "8.5% is low enough".

**Example:** (illustrative numbers) 17 bad refunds worth 1,490 in total in the test (20 x 5, 40 x 5, 80 x 3, 150 x 2, 250, 400). Cap automatic refunds at 50: 10 of the 17 (300 in value) would still pay out, and 7 (1,190) go to a human who rejects them. Worst-case loss falls to 20% of the original. Better still, a code check that the sender owns the order would stop most of the remaining ones. Weak answer: "I will add a line to the system prompt telling the bot to ignore instructions inside emails." Strong answer: "First hour: refunds go to approval, I scan 30 days of logs, and I tell the owner. Then the permission moves out of the prompt: the refund tool checks order ownership, amount and window in code, large amounts need a person, and the model that reads emails has no tools. I keep the 200 as a regression test and add more."

**Code:**
```python
import math
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
k, n = 17, 200
lo, hi = wilson(k, n)
print(f"red-team success {k/n:.1%}, 95% Wilson {lo:.1%} to {hi:.1%}  (rate on PLANTED emails, not production)")
assert k/n == 0.085 and round(lo, 3) == 0.054 and round(hi, 3) == 0.132
# If a prompt fix gives 0 successes in 200 new test emails: rule of three upper bound (95%)
print(f"0 of 200: upper bound about 3/200 = {3/200:.1%}; Wilson upper {wilson(0, 200)[1]:.2%}")
assert 3/200 == 0.015 and round(wilson(0, 200)[1], 4) == 0.0188
# Structural controls cut the blast radius: a hard cap on refund amount and a human approval over it (illustrative)
# 17 bad refunds with illustrative amounts; auto-refunds capped at 50, anything above goes to a human
bad = [20]*5 + [40]*5 + [80]*3 + [150]*2 + [250] + [400]
assert len(bad) == k and sum(bad) == 1490
cap = 50
auto = [a for a in bad if a <= cap]; held = [a for a in bad if a > cap]
print(f"17 bad refunds total {sum(bad)}; paid automatically under cap {cap}: {sum(auto)} ({len(auto)} refunds); sent to a human: {len(held)} refunds worth {sum(held)}")
assert (len(auto), sum(auto), len(held), sum(held)) == (10, 300, 7, 1190)
print(f"worst-case loss falls from {sum(bad)} to {sum(auto)} ({sum(auto)/sum(bad):.0%}) if the human rejects the held ones")
assert round(sum(auto)/sum(bad), 2) == 0.20
# Attempts needed: if each planted email has 8.5% chance, chance an attacker gets at least one refund in m tries
for m in (1, 10, 30):
    print(f"{m:2d} attempts -> {1-(1-0.085)**m:.1%} chance of at least one bad refund")
assert round(1-(1-0.085)**30, 3) == 0.930
```

**Output (my run):**
```text
red-team success 8.5%, 95% Wilson 5.4% to 13.2%  (rate on PLANTED emails, not production)
0 of 200: upper bound about 3/200 = 1.5%; Wilson upper 1.88%
17 bad refunds total 1490; paid automatically under cap 50: 300 (10 refunds); sent to a human: 7 refunds worth 1190
worst-case loss falls from 1490 to 300 (20%) if the human rejects the held ones
 1 attempts -> 8.5% chance of at least one bad refund
10 attempts -> 58.9% chance of at least one bad refund
30 attempts -> 93.0% chance of at least one bad refund
```

**Follow-ups:**
- Can a better prompt or a classifier for injections solve it? It reduces the rate. It cannot give a guarantee, so it is a second layer behind the code checks.
- Who decides to switch the bot off? The service owner can do it on their own call in an incident. Restoring needs the owner and the risk lead to agree.
- How do you test that the fix works? A larger and varied attack set, written by someone who did not build the defences, plus the rule of three for a zero count.

**Common mistakes:**
- Fixing only the prompt and declaring success.
- Reading 8.5% as a production rate.
- Not checking production logs for real cases.
- Giving the bot a tool with more power than the task needs.
- Reporting zero failures in a small test as "zero risk".

### Q7 ⭐⭐⭐ 🟡 A provider releases a new model version, and your 500-prompt regression suite shows the pass count rising from 430 (86%) to 445 (89%). Looking prompt by prompt, 40 that passed before now fail and 55 that failed before now pass. Is this a safe upgrade, what do you examine in the 40 regressions, and what rollout do you use?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to model-upgrade and regression-evaluation topics in LLMOps material; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Not yet: the net gain of 15 prompts (+3 points) is within noise on a paired test (exact p about 0.15, interval about -0.8 to +6.8 points), 95 of 500 prompts changed result, so I would read the 40 regressions by severity and roll out in shadow then a small canary with a rollback rule.

**Clarifying questions:**
- Does the suite represent real traffic, or is it hand-picked? If it is skewed, 89% versus 86% does not carry over.
- How was each prompt graded: exact match, rubric, an LLM judge? A noisy grader creates flips by itself.
- Was sampling on, and was each prompt run once? Flips between runs of the same model tell me the noise floor.
- Which prompts are critical (safety, money, legal, formatting that breaks a parser)? One critical regression can outweigh many small gains.
- Is the old version being retired, so I have a deadline, or can I stay on it? That sets how careful the rollout must be.

**Approach:**
1. Do the table: 390 pass both, 40 lost, 55 gained, 15 fail both. Net = 55 - 40 = +15 = +3.0 points. It checks: 430 - 40 + 55 = 445.
2. Test it as paired data (McNemar), not as two independent 500-prompt rates. Only the 95 changed prompts carry information: 55 of 95 is 57.9% against 50% if there were no real difference.
3. Measure the noise: re-run the old version on the same suite. If it flips some prompts alone, part of the 95 is noise.
4. Read all 40 regressions. Group by category and severity: wrong facts, format breaks, refusals, tone, tool-call errors. Mark critical ones.
5. Decide by rule: no critical regression, no category with a clear drop, and format-break rate not worse. The overall pass rate is a secondary check.
6. Roll out: shadow (new model runs in parallel, outputs not served), then canary 5%, then 25%, then 100%, with automatic rollback on guardrails. Keep the old version pinned until the end.

**Metrics:**
- Pass rate = prompts passed / prompts in suite (445 / 500 = 89.0%).
- Paired change = (gained - lost) / n = (55 - 40) / 500 = +3.0 points.
- Churn = (lost + gained) / n = 95 / 500 = 19%.
- Critical-regression count = lost prompts tagged critical (target 0).
- Online guardrails: parse-failure rate, refusal rate, escalation to human, latency and cost per request, thumbs-down rate.

**Risks:**
- Averaging hides a rare but serious regression, for example a safety or legal prompt.
- Small suite: 500 prompts give an interval of roughly plus or minus 3 points for one pass rate alone.
- Judge or suite is tuned to the old model's style, so the new model looks worse or better for the wrong reason.
- The provider may change a model alias without notice, so tests today may not describe next month.

**What the interviewer scores:**
- Strong: uses the paired counts (40 and 55) and says the net is not clearly different from zero. Weak: "89 is more than 86, upgrade".
- Strong: reads the regressions by severity and category. Weak: reads only the average.
- Strong: measures run-to-run noise before blaming the model. Weak: assumes the suite is noise free.
- Strong: staged rollout with a rollback rule and a pinned old version. Weak: switch everything at once.

**Example:** (illustrative numbers) Suppose the 40 regressions are: 18 tone or style only, 10 shorter or less complete answers, 8 format breaks, 4 refusals on valid requests. The 8 format breaks are critical because they break the parser, and 4 more are blocked customer requests. So I keep going on the new model only if a prompt fix or a schema constraint removes the 8 format breaks. Paired result: z = (55 - 40) / sqrt(95) = 1.54, exact p about 0.15. Rollout: 1 week shadow, canary 5% of 20,000 requests a day (1,000 requests), then widen if parse failures and refusals are no worse than the old version. Weak answer: "Pass rate went up from 86% to 89%, so it is a safe upgrade." Strong answer: "Plus 15 net is not clearly different from zero on a paired test, 19 percent of prompts changed, and I care more about what the 40 are. I read them by severity, fix or block any critical ones, then shadow and canary with a rollback rule."

**Code:**
```python
import math
from scipy import stats
n = 500
before, after = 430, 445
lost, gained = 40, 55
assert before - lost + gained == after and before/n == 0.86 and after/n == 0.89
stay_pass = before - lost; stay_fail = (n - before) - gained
print(f"stay pass {stay_pass}, lost {lost}, gained {gained}, stay fail {stay_fail}; changed {lost+gained} of {n} = {(lost+gained)/n:.0%}")
assert (stay_pass, stay_fail) == (390, 15) and (lost+gained)/n == 0.19
# Paired test (McNemar): among the 95 discordant prompts, is 55 vs 40 different from 47.5 vs 47.5?
d = lost + gained
p_exact = stats.binomtest(gained, d, 0.5).pvalue
z = (gained - lost) / math.sqrt(d)
print(f"net +{gained-lost} ({(gained-lost)/n:.1%}); exact McNemar p = {p_exact:.3f}; z = {z:.2f}")
assert round(p_exact, 3) == 0.151 and round(z, 2) == 1.54
# 95% interval on the net change in pass rate (paired, normal approx)
diff = (gained - lost) / n
se = math.sqrt(((gained + lost) / n - diff**2) / n)
print(f"paired 95% CI for change in pass rate: {diff-1.96*se:+.1%} to {diff+1.96*se:+.1%}")
assert diff - 1.96*se < 0 < diff + 1.96*se
# Noise floor: if the OLD model re-run on the same 500 flips about 8% of prompts by itself (illustrative), churn of 19% is only partly new
flip = 0.08
print(f"illustrative self-flip {flip:.0%} = {flip*n:.0f} prompts; observed churn {d} prompts")
# Regression severity: weight by importance (illustrative): 8 of the 40 lost prompts are 'critical' (policy, safety, refunds)
crit_lost, crit_total = 8, 100
print(f"critical prompts failing: {crit_lost} of {crit_total} critical in the suite = {crit_lost/crit_total:.0%}; each critical regression blocks a full rollout")
assert crit_lost/crit_total == 0.08
# Canary sizing: 5% canary on 20,000 requests/day = 1,000 requests/day
print("canary requests per day at 5% of 20,000:", int(0.05*20000)); assert int(0.05*20000) == 1000
```

**Output (my run):**
```text
stay pass 390, lost 40, gained 55, stay fail 15; changed 95 of 500 = 19%
net +15 (3.0%); exact McNemar p = 0.151; z = 1.54
paired 95% CI for change in pass rate: -0.8% to +6.8%
illustrative self-flip 8% = 40 prompts; observed churn 95 prompts
critical prompts failing: 8 of 100 critical in the suite = 8%; each critical regression blocks a full rollout
canary requests per day at 5% of 20,000: 1000
```

**Follow-ups:**
- Would a bigger suite help? Yes. The interval shrinks with the square root of the number of changed prompts, and I would add real traffic samples and the failures from production.
- What if the 40 regressions are all harmless? Then the upgrade is probably acceptable on quality, but I would still do a canary because the suite is not production.
- What if the provider forces the upgrade by a date? I use the time before it to fix the prompts, and I keep a fallback (another model or a pinned snapshot, if the provider offers one).

**Common mistakes:**
- Comparing 86% and 89% as if they were independent samples.
- Ignoring the 40 because the net is positive.
- No noise floor: not re-running the old version.
- Counting all prompts as equally important.
- Full rollout with no pinned fallback.

### Q8 ⭐⭐⭐ 🟡 An LLM judge picks the better of two answers, and when you rerun 100 pairs with the answer order swapped it picks the same underlying answer in only 68 of the 100 pairs. What does this say about the judge, how do you reduce the problem, and how should the remaining disagreement be treated in the win rate you report?
**Asked at:** LLM-evaluation pages (Manning's AI model evaluation chapter and an arXiv judge-bias study listing position, verbosity and self-preference bias, Arize and Langfuse pages on offline versus online evaluation, an LLM-as-judge survey); practitioner and academic material rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** A judge that gives the same verdict in only 68 of 100 order swaps is strongly affected by position (32 flips; a coin flip would agree on about 50), so I would judge both orders, count a win only when it wins both ways, treat the flips as ties or uncertainty, and report the win rate with that range.

**Clarifying questions:**
- When the verdict flips, does the judge usually prefer the first answer or the second? A one-sided pattern is position bias; an even split looks like noise.
- Are the 32 flipped pairs close in quality? If the answers are nearly equal, flips are expected and less alarming.
- Is there a human label on a subset? I need it to know whether the 68 consistent verdicts are even correct.
- Is the judge the same model family as one of the answers being judged? Self-preference is another known bias (editor knowledge, covered in judge-bias studies).
- How will the win rate be used: ship decision, model choice, or a dashboard trend? It sets how much uncertainty I can accept.

**Approach:**
1. Compute consistency: 68 / 100 = 68%, 95% Wilson interval about 58% to 76%. Reference points: always picking the first slot is 0% consistent, random guessing about 50%, a stable judge near 100%.
2. Classify the 32 flips: always-first, always-second, or mixed. Note answer length and which side is the new model.
3. Reduce the problem: judge each pair in both orders; ask for a short reason before the verdict; use a clear rubric; try a pointwise score with a rubric as a cross-check; use a stronger or different judge; break ties with a third judge.
4. Validate against humans on a sample of 100 pairs, including some of the flipped ones. Judge accuracy on the consistent verdicts is the number that matters.
5. Report the win rate using both orders, and keep the flips visible as their own row.

**Metrics:**
- Order consistency = pairs with the same underlying winner in both orders / pairs = 68 / 100.
- Position bias = share of flipped pairs where the judge picked the first slot in both runs, minus the share where it picked the second.
- Win rate = (wins + 0.5 x ties) / pairs, where a win means winning in both orders and flipped pairs count as ties.
- Judge-human agreement on a labelled sample.
- Guardrail: the same checks per category and per answer length (verbosity bias).

**Risks:**
- A consistent judge can still be consistently wrong, so consistency is necessary, not sufficient.
- Dropping the 32 flipped pairs makes the win rate look cleaner and is biased: flipped pairs are often the close ones.
- Judge and candidate from the same family can favour their own style.
- Improving the judge prompt on the same pairs you report on overfits it.

**What the interviewer scores:**
- Strong: knows the baselines (50% for random, 0% for always-first) and puts an interval on 68. Weak: "68% is okay".
- Strong: swap order and count both, with flips as ties or bounds. Weak: runs one order.
- Strong: checks judge against human labels. Weak: trusts the judge.
- Strong: names several biases (position, length, self-preference). Weak: only position.

**Example:** (illustrative numbers) 100 pairs. 68 consistent, 32 flipped. Among the 68, the new answer wins 45 and loses 23. Counting flips as half: (45 + 16) / 100 = 61%. If all 32 flips had gone against the new answer the win rate would be 45%, and if all had gone for it, 77%. So the honest statement is "61%, between 45% and 77%, with a third of the verdicts unstable", and among decisive pairs 45 of 68 is 66.2% (interval about 54% to 76%). Weak answer: "The judge says we win 60 percent of the time, so we ship." Strong answer: "Thirty-two percent of verdicts flip when I swap the order, that is a lot of position effect. I judge both orders, count only wins in both, treat the flips as ties, report 61 percent with a 45 to 77 range, and check the judge against human labels before using it for a ship decision."

**Code:**
```python
import math
from random import Random
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
n, consistent = 100, 68
lo, hi = wilson(consistent, n)
print(f"order-consistent {consistent}/{n} = {consistent/n:.0%} (95% Wilson {lo:.1%} to {hi:.1%}); flipped with order {n-consistent}")
assert round(lo, 3) == 0.583 and round(hi, 3) == 0.763
# Reference points: a judge that always says "first" is consistent 0%; one that guesses at random is consistent 50%
# Simulation (seeded): random coin flip judge, 100 pairs
r = Random(3)
cons = sum((r.random() < 0.5) == (r.random() < 0.5) for _ in range(100000))/100000
print(f"random guesser, order swapped: consistent {cons:.3f} (should be near 0.5)")
assert abs(cons - 0.5) < 0.01
kappa_like = (consistent/n - 0.5) / (1 - 0.5)
print(f"consistency above chance: {kappa_like:.2f}"); assert round(kappa_like, 2) == 0.36
# Reporting win rate. Among the 68 consistent pairs, suppose the new answer wins 45 and loses 23 (illustrative)
win, loss, flips = 45, 23, 32
assert win + loss == consistent
tie_half = (win + 0.5*flips) / n
lo_b, hi_b = win / n, (win + flips) / n
print(f"win rate, flips as half: {tie_half:.0%}; bounds if flips all lost / all won: {lo_b:.0%} to {hi_b:.0%}")
assert tie_half == 0.61 and (lo_b, hi_b) == (0.45, 0.77)
print(f"win rate among decisive pairs: {win}/{consistent} = {win/consistent:.1%}  (Wilson {wilson(win, consistent)[0]:.1%} to {wilson(win, consistent)[1]:.1%})")
assert round(win/consistent, 3) == 0.662
```

**Output (my run):**
```text
order-consistent 68/100 = 68% (95% Wilson 58.3% to 76.3%); flipped with order 32
random guesser, order swapped: consistent 0.502 (should be near 0.5)
consistency above chance: 0.36
win rate, flips as half: 61%; bounds if flips all lost / all won: 45% to 77%
win rate among decisive pairs: 45/68 = 66.2%  (Wilson 54.3% to 76.3%)
```

**Follow-ups:**
- Is 68% bad? For a pairwise judge it is weak. Random is about 50, so 68 is only 0.36 of the way from chance to perfect (a kappa-style reading). I would want a much higher number on a clear-cut rubric before using it alone.
- Could I just drop the flipped pairs? Only if I also report how many were dropped and why. They are biased toward close calls, so dropping them overstates both clarity and effect.
- What about a stronger judge? It usually helps, but I would still measure consistency and human agreement for that judge. Version or feature claims about specific judges are editor knowledge unless tested.

**Common mistakes:**
- Running one order and trusting it.
- Dropping flipped pairs silently.
- Judging with the candidate's own model family and not checking self-preference.
- Tuning the judge on the evaluation pairs.
- Reporting a win rate with no interval or human check.

### Q9 ⭐⭐⭐ 🟡 A team proposes fine-tuning a model on 4,000 policy documents because answers about new policies are wrong. About 600 of the documents change in a typical month, a retraining run costs 2,000 and re-indexing the changed documents for retrieval costs about 300 a month, both illustrative. Compute the yearly cost of monthly retraining against monthly re-indexing, and give your recommendation with the conditions that would change it.
**Asked at:** GenAI and LLM-engineer interview guides (InterviewBit, Hyring, Let's Code, recrew, Pensero and Towards AI 2026 pages list RAG, hallucination mitigation, evaluation and cost or latency topics; one guide reports a prompt about a RAG answer that is wrong although the right document exists, and another a smaller-model-for-narrow-tasks answer pattern); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Monthly retraining costs 12 x 2,000 = 24,000 a year against 12 x 300 = 3,600 for re-indexing (6.7x, a gap of 20,400), and since the problem is changing facts, I recommend retrieval, keeping fine-tuning for style and format.

**Clarifying questions:**
- What exactly is wrong on new policies: facts, wording, or missing the new document? Facts that change belong in a store, not in weights.
- Do answers need citations and the ability to remove a retired policy? Retrieval can show the source and delete it, a fine-tuned model cannot.
- How fast must a policy change show up in answers: same day or next month? It sets how bad a retrain lag is.
- How many queries a month, and how long is the context that retrieval adds? It decides whether retrieval's token cost matters.
- Is the 2,000 per retrain the whole cost, or does it exclude data prep, evaluation and release? If those are missing, retraining is even more expensive.

**Approach:**
1. Compute: retrain 24,000 a year, re-index 3,600 a year, difference 20,400. 600 of 4,000 documents change a month, 15%, or 7,200 document updates a year.
2. Per changed document: retrain 3.33, re-index 0.50.
3. Reality check on the number: retrieval adds context tokens to every query, which the 300 does not include. At an illustrative 1,500 extra tokens at 3 per million, that is 0.0045 per query. The 1,700 monthly gap is used up at about 378,000 queries a month, and 1,000,000 queries cost 4,500 in extra tokens. So volume is the condition that can flip the cost picture.
4. Quality comparison matters more than cost: build a test set of questions about changed policies, and compare a retrieval baseline with the fine-tuned model (editor knowledge: fine-tuning is unreliable at injecting new facts and can forget old ones).
5. Recommend retrieval first. Add fine-tuning later only for what it is good at: tone, output format, a domain vocabulary, or routing.

**Metrics:**
- Yearly cost = months x cost per run. Include evaluation and release cost, not only compute.
- Freshness lag = time from policy change to correct answers (hours versus up to a month).
- Policy-answer accuracy on new-policy questions, with the source cited.
- Stale-answer rate = answers that quote a retired policy / answers on versioned policies.
- Cost per 1,000 queries including retrieval tokens.

**Risks:**
- A fine-tuned model can answer confidently with old policy text and cannot show where it came from.
- Retrieval can fetch the wrong or stale chunk if the index is not refreshed or documents are not versioned.
- Re-index cost is not constant: a re-chunking or embedding-model change re-processes all 4,000 documents.
- The cost numbers are invented, so I would present the ratio and conditions, not the exact figures.

**What the interviewer scores:**
- Strong: both yearly numbers (24,000 and 3,600) and what they leave out (retrieval tokens, evaluation). Weak: only the 20,400 gap.
- Strong: separates knowledge (retrieval) from behaviour (fine-tuning). Weak: "fine-tuning teaches the model our policies".
- Strong: states conditions that change the answer. Weak: absolute recommendation.
- Strong: proposes an eval on new-policy questions. Weak: decides on cost alone.

**Example:** (illustrative numbers) Retrain 24,000, re-index 3,600 a year. With 100,000 queries a month, retrieval tokens add 450 a month; at 1,000,000 queries they add 4,500 a month, more than the 1,700 gap, so on pure cost the picture flips at roughly 378,000 queries a month. Even so, I would not fine-tune for facts. Conditions that would change my recommendation: policies almost never change (say once a year) and answers must be fast with no retrieval step; the model must run offline at the edge; the volume is so high that the retrieval context is the main cost and an eval shows the fine-tuned model is just as accurate on new policies; or retrieval cannot reach the needed accuracy and the errors are in style, not facts. Weak answer: "Retraining is more expensive, so no." Strong answer: "Twenty-four thousand against thirty-six hundred a year, and the facts change 15 percent a month, so retrieval. The caveat is that retrieval adds tokens per query, which matters above roughly 378,000 queries a month, so I check volume and compare accuracy on new-policy questions before I decide."

**Code:**
```python
# All money figures illustrative, from the prompt
docs, changed_per_month = 4000, 600
retrain, reindex = 2000, 300
yr_retrain, yr_reindex = 12*retrain, 12*reindex
print(f"yearly: retrain {yr_retrain:,} vs re-index {yr_reindex:,}; difference {yr_retrain-yr_reindex:,}; ratio {yr_retrain/yr_reindex:.1f}x")
assert (yr_retrain, yr_reindex) == (24000, 3600) and yr_retrain - yr_reindex == 20400 and round(yr_retrain/yr_reindex, 1) == 6.7
print(f"churn: {changed_per_month/docs:.0%} of documents per month, {12*changed_per_month:,} document updates a year")
assert changed_per_month/docs == 0.15 and 12*changed_per_month == 7200
# Per-document unit cost
print(f"retrain {retrain/changed_per_month:.2f} per changed doc; re-index {reindex/changed_per_month:.2f} per changed doc")
assert round(retrain/changed_per_month, 2) == 3.33 and reindex/changed_per_month == 0.5
# The comparison is incomplete: retrieval adds input tokens to every query. Illustrative: +1,500 context tokens at 3 per million.
extra_per_query = 1500*3/1e6
be_queries = (retrain - reindex) / extra_per_query
print(f"retrieval context costs {extra_per_query:.4f} per query; the 1,700/month saving is wiped out above {be_queries:,.0f} queries/month")
assert round(extra_per_query, 4) == 0.0045 and round(be_queries) == 377778
for q in (100_000, 1_000_000):
    print(f"{q:>9,} queries/month: retrieval tokens cost {q*extra_per_query:,.0f}/month vs the 1,700 gap")
assert round(100_000*extra_per_query) == 450 and round(1_000_000*extra_per_query) == 4500
# Freshness: lag between a policy change and the model knowing it
print("lag: re-index minutes to hours; monthly retrain up to 30 days (plus eval time)")
```

**Output (my run):**
```text
yearly: retrain 24,000 vs re-index 3,600; difference 20,400; ratio 6.7x
churn: 15% of documents per month, 7,200 document updates a year
retrain 3.33 per changed doc; re-index 0.50 per changed doc
retrieval context costs 0.0045 per query; the 1,700/month saving is wiped out above 377,778 queries/month
  100,000 queries/month: retrieval tokens cost 450/month vs the 1,700 gap
1,000,000 queries/month: retrieval tokens cost 4,500/month vs the 1,700 gap
lag: re-index minutes to hours; monthly retrain up to 30 days (plus eval time)
```

**Follow-ups:**
- Could we do both? Yes: retrieval for facts and a light fine-tune for tone and format, evaluated separately.
- What if the retrieved chunk is right and the model still answers wrong? That is a generation problem (prompt, citation instruction, or a fine-tune for faithfulness), a different fix from the knowledge problem.
- How do you handle a policy that is withdrawn? Delete or expire it in the index the same day. A fine-tuned model has no such delete.

**Common mistakes:**
- Treating fine-tuning as a way to add facts that change monthly.
- Comparing only the two headline costs and ignoring retrieval tokens, evaluation and release effort.
- Forgetting a full re-index when the embedding model changes.
- Giving no conditions under which the recommendation would change.
- Quoting invented costs as real.

### Q10 ⭐⭐⭐ 🟡 A company sends 2,000 million input and 400 million output tokens a month to an API priced at illustrative 3 and 15 per million tokens. A self-hosted option costs a fixed 15,000 a month for GPUs and staff and can absorb up to twice the current volume. Compute the API bill and the break-even volume as a multiple of today's, and list the non-cost questions you would raise.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to vendor-API versus self-host and LLM cost material; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The API bill is 2,000 x 3 + 400 x 15 = 12,000 a month, the fixed self-host cost of 15,000 breaks even at 1.25 times today's volume, and before moving I would raise quality, peak capacity, staffing, security, vendor-price and lock-in questions, because the cost gap alone is small and fragile.

**Clarifying questions:**
- Is volume growing, flat or seasonal? At today's volume self-hosting costs 3,000 more a month; it only wins if volume grows by more than 25%.
- Does the self-hosted model meet the quality bar on our tasks? A cheaper bill with worse answers is not a saving.
- Is the capacity "twice current volume" sized on average or on peak traffic? Peaks decide whether it really fits.
- Does the 15,000 include on-call, security, upgrades and a spare for failure? Hidden operations cost is the usual surprise.
- Are there data-residency, privacy or contract reasons to self-host regardless of cost? Then cost is not the deciding factor.

**Approach:**
1. API bill: input 2,000 million x 3 = 6,000; output 400 million x 15 = 6,000; total 12,000 a month.
2. Break-even volume = fixed cost / API bill at today's volume = 15,000 / 12,000 = 1.25x. It is below the 2x capacity, so a window exists.
3. Show the window: at 1.25x both cost 15,000. At 2x volume the API would cost 24,000 against 15,000, a saving of 9,000. Today, self-host costs 3,000 more.
4. Sensitivity: if API prices fall 30%, the bill is 8,400 and break-even moves to 1.79x, almost at the capacity limit. The case depends on a price that the vendor controls.
5. Non-cost questions (listed below), then a pilot: run the self-hosted model on a shadow copy of real traffic and compare quality, latency and failure rate.
6. Decide on total cost of ownership over 12 to 24 months, with a trigger: self-host only when sustained volume is above, say, 1.5x for three months.

**Metrics:**
- API bill = (input tokens x input price + output tokens x output price) per month.
- Break-even multiple = fixed self-host cost / API bill at current volume.
- Cost per million tokens (blended): API 12,000 / 2,400 = 5.00; self-host 6.25 at today's volume, 3.12 at 2x.
- Utilisation = actual volume / capacity (break-even is at 62.5% of the 2x capacity).
- Guardrails: quality on a fixed eval, p95 latency, availability, and engineer hours per month.

**Risks:**
- Capacity: a box sized for 2x average volume may not cover peaks.
- Fixed cost is paid even if volume falls.
- API prices move down over time (illustrative 30% cut moves the break-even from 1.25x to 1.79x).
- Staff cost and attention: the model stack needs upgrades, security patches and monitoring.
- Quality gap: the open model may need extra prompt work or fine-tuning.

**What the interviewer scores:**
- Strong: both numbers (12,000 and 1.25x) and an honest reading (today it costs more, the window is 1.25x to 2x). Weak: "self-hosting is cheaper".
- Strong: tests sensitivity to price, volume and peaks. Weak: single-point comparison.
- Strong: a list of non-cost questions with reasons. Weak: only cost.
- Strong: a staged decision with a trigger. Weak: a one-time yes or no.

**Example:** (illustrative numbers) Blended cost per million tokens: API 5.00. Self-host 15,000 / 2,400 = 6.25 at today's volume, 3.12 at twice the volume. Non-cost questions I would raise: (1) quality on our tasks, measured on a held-out set; (2) peak-to-average traffic and what happens when capacity is full (fallback to the API?); (3) who is on call and what happens when the GPUs fail; (4) data privacy, residency and contract terms, which may favour self-hosting or the vendor; (5) the model upgrade path and how long migration takes; (6) vendor price cuts and committed-use discounts; (7) lock-in and the cost of switching back; (8) latency and context-length needs. Weak answer: "The API costs 12,000 and self-host 15,000, so stay on the API." Strong answer: "The API is 12,000 a month. Self-hosting breaks even at 1.25 times today's volume and saves up to 9,000 at twice. But a 30 percent API price cut moves break-even to 1.79 times, and I would check quality, peak capacity and the real operations cost first, so I would pilot on shadow traffic and set a volume trigger."

**Code:**
```python
PIN, POUT = 3, 15          # illustrative, per million tokens
tin, tout = 2000, 400          # millions of tokens per month
api = tin*PIN + tout*POUT
print(f"API bill: input {tin*PIN:,.0f} + output {tout*POUT:,.0f} = {api:,.0f} per month")
assert (tin*PIN, tout*POUT, api) == (6000, 6000, 12000)
fixed, cap = 15_000, 2.0
be = fixed / api
print(f"break-even volume: {fixed:,}/{api:,} = {be:.2f}x today's; capacity limit {cap:.0f}x")
assert be == 1.25 and be < cap
print(f"today: self-host costs {fixed-api:,} more than API; at 2x volume API would cost {2*api:,} vs {fixed:,} -> saves {2*api-fixed:,}")
assert fixed - api == 3000 and 2*api - fixed == 9000
# Sensitivity: API price falls 30% (illustrative)
cut = 0.30; api_cut = api*(1-cut); be_cut = fixed/api_cut
print(f"if API prices fall {cut:.0%}: bill {api_cut:,.0f}, break-even {be_cut:.2f}x (above the {cap:.0f}x capacity? {be_cut > cap})")
assert round(api_cut) == 8400 and round(be_cut, 2) == 1.79 and be_cut < cap
# Peak vs average: if peak traffic is 3x average, capacity '2x current volume' (average) may not cover peaks
avg_cap_ok = 2.0; peak_ratio = 3.0
print(f"if capacity is sized on AVERAGE volume (2x) and peak/average is {peak_ratio:.0f}x, today's peak needs {peak_ratio/avg_cap_ok:.0%} of it")
assert peak_ratio/avg_cap_ok == 1.5
# Utilisation view: self-host only wins above 1.25x; what share of the 2x capacity is that?
print(f"break-even utilisation of capacity: {be/cap:.1%}"); assert round(be/cap, 4) == 0.625
# Cost per million tokens at various volumes (blended: 2400 M tokens => 12000, 5.0 per M)
blend = api/(tin+tout); print(f"API blended price {blend:.2f} per million; self-host at 1x: {fixed/(tin+tout):.2f}, at 2x: {fixed/(2*(tin+tout)):.2f}")
assert blend == 5.0 and round(fixed/(tin+tout), 2) == 6.25 and round(fixed/(2*(tin+tout)), 2) == 3.12
```

**Output (my run):**
```text
API bill: input 6,000 + output 6,000 = 12,000 per month
break-even volume: 15,000/12,000 = 1.25x today's; capacity limit 2x
today: self-host costs 3,000 more than API; at 2x volume API would cost 24,000 vs 15,000 -> saves 9,000
if API prices fall 30%: bill 8,400, break-even 1.79x (above the 2x capacity? False)
if capacity is sized on AVERAGE volume (2x) and peak/average is 3x, today's peak needs 150% of it
break-even utilisation of capacity: 62.5%
API blended price 5.00 per million; self-host at 1x: 6.25, at 2x: 3.12
```

**Follow-ups:**
- What if volume doubles beyond capacity? Then I need a second node or hybrid: self-host the base load and spill the rest to the API.
- Would you negotiate with the vendor instead? Yes, a volume discount or committed use changes the break-even, and it takes no engineering. I compare the new break-even before building anything.
- What if quality is slightly lower? Quantify it in cost per resolved task, not per token, and decide whether routing only the easy traffic to the self-hosted model gets most of the saving.

**Common mistakes:**
- Comparing price per token and ignoring staff, spare capacity and operations.
- Assuming the vendor price stays fixed.
- Forgetting that the self-host cost is paid even at low volume.
- Sizing on average, not peak, traffic.
- Skipping a quality test on real tasks.
