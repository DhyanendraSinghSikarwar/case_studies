# Book 6 — Part 7: GenAI Scenarios (Hallucinations, Cost, Latency, Evaluation)

**Topic:** Scenario-based "this GenAI system is misbehaving, too slow or too expensive; what do you do" questions for Data Scientist, ML Engineer and GenAI Engineer loops: a RAG assistant answering wrongly or citing stale or irrelevant sources, measuring and reducing hallucinations, prompt-injection and data-leakage incidents, cost blow-ups from tokens, retries, long contexts and agent loops, latency budgets (time to first token, tokens per second, streaming, caching, batching), model upgrades and regression evaluation, LLM-as-judge validity and bias, offline versus online metrics, guardrails and over-refusal, agents looping or acting wrongly, fine-tune versus prompt versus RAG, vendor API versus self-host break-even, long context versus retrieval, multilingual and Indic-language quality, PII and compliance, user-feedback loops, prompt versioning and rollout, eval-set contamination, non-determinism, semantic-cache risks and small-model routing and cascades.

**Target:** 55  |  **Actual:** 55 (⭐⭐⭐ 18, ⭐⭐ 25, ⭐ 12)  |  **Date:** 2026-10-31  |  **Status:** Complete (answers merged, checked, reviewed)

**Scope note:** this part is the scenario and judgement angle on GenAI systems in production, with numbers where a cost, a latency, a rate or an interval can be computed. GenAI internals (attention, KV cache, tokenizers, decoding, fine-tuning mechanics, guardrail frameworks) belong to Book 2, MLOps tooling to Book 4, experiment theory to Book 1 Part 10 and Book 6 Part 4, model degradation in general to Book 6 Part 2; Wave B answers should cross-reference those only by checked headings. All numbers in the prompts are invented illustrative numbers in one unnamed currency unit, not data from any company; prices per million tokens are round invented figures, not any vendor's prices. Every percentage names its base in the prompt, rates are labelled as measured samples or projections where it matters, and every arithmetic claim is checked in scratch/B6P07_wavea/qs.py. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part07_sources.md). Searches returned GenAI and LLM-engineer interview guides (mostly practitioner and prep sites, some candidate-reported), RAG-debugging pages, LLM-evaluation and LLM-as-judge pages, cost, routing and semantic-cache posts, Indic tokenizer papers, PII and retention playbooks and eval-contamination material. None tied a scenario to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page for the exact framing. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

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

### Q11 ⭐⭐⭐ 🟡 A new prompt version v12 is canaried on 1,000 requests while the old version v11 serves 9,000, and JSON parse failures are 15 of 1,000 (1.5%) on v12 and 36 of 9,000 (0.4%) on v11. Compute whether the difference is larger than sampling noise, and state your rollback rule and who decides.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to prompt versioning and rollout topics in LLMOps material; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The difference of 1.1 points (1.5% versus 0.4%) is far larger than sampling noise (two-proportion z of about 4.6, p about 0.000004), so v12 is worse on parse failures and I roll it back under a rule written before the canary, which the prompt owner can trigger without asking.

**Clarifying questions:**
- Were the 1,000 requests assigned to v12 at random, or by customer, route or time of day? Non-random assignment can make v12 look worse for reasons unrelated to the prompt.
- What counts as a parse failure, and is it measured the same way on both versions? A different parser or retry logic invalidates the comparison.
- Are failures clustered, for example by one long-input customer? Repeated requests from the same user are not independent.
- What does a parse failure cost: a retry, a user-visible error, or a wrong action? It sets the rollback threshold.
- Does v12 improve anything (accuracy, cost, tone) that I should weigh against the failures?

**Approach:**
1. Compute the rates: v12 15 / 1,000 = 1.5%, v11 36 / 9,000 = 0.4%, difference +1.1 points.
2. Test the difference with a two-proportion z-test. Pooled rate = 51 / 10,000 = 0.51%. Standard error = sqrt(0.0051 x 0.9949 x (1/1,000 + 1/9,000)) = 0.0024. z = 0.011 / 0.0024 = 4.63. Cross-check with a Fisher exact test (p about 0.00009) and a count check: if v12 were as good as v11 we would expect 4 failures in 1,000, and seeing 15 or more has probability about 0.00002.
3. Check the design: random assignment, same parser, no clustering by user. Look at the 15 failures: what do they have in common (long input, a certain field, missing closing bracket)?
4. Apply the rollback rule (below). Here it fires, so route 100% back to v11.
5. Fix the prompt, add a schema or constrained output (editor knowledge: availability depends on the provider and library), add a retry with repair, and re-canary.

**Metrics:**
- Parse-failure rate = responses that fail JSON parsing / responses served, per version.
- Difference in rates with a Wilson interval for each: v12 about 0.91% to 2.46%, v11 about 0.29% to 0.55%. The intervals do not overlap.
- z = (p12 - p11) / SE with the pooled standard error.
- Guardrails (checked together): retries per request, task success, latency, cost per request.
- Impact: extra failures per day if rolled out fully. At 200,000 requests a day (invented), 1.1 points is 2,200 extra failures a day.

**Risks:**
- Peeking: checking after every few requests inflates false alarms, so I fix the checkpoints and use a stricter threshold for early looks.
- Non-independence: failures cluster by user or document type, so the real uncertainty is larger than the formula says.
- Small canary: with 1,000 requests, a rare failure type could show nothing.
- Making the rule after seeing the data tempts me to pick whatever fits.

**What the interviewer scores:**
- Strong: correct z (about 4.6) with the formula, the pooled rate and an exact-test cross-check. Weak: "1.5 is more than 0.4, so it is worse".
- Strong: a pre-agreed rollback rule with both a statistical and a size condition. Weak: "we will see how it goes".
- Strong: names a decision owner and a speed: rollback is cheap, promotion is deliberate. Weak: "the team decides".
- Strong: checks randomisation, clustering and parser parity. Weak: trusts the raw counts.

**Example:** (illustrative numbers) Rule written before the canary: check at 250, 500, 750 and 1,000 requests; roll back if z is at least 3 against v11 and the v12 rate is at least 0.5 points above the v11 rate; also roll back at once if parse failures exceed 3% in any 100 requests. A possible path: 4 failures at 250 requests (z 2.85, no action), 7 at 500 (z 3.24, rollback), 11 at 750 (z 4.05), 15 at 1,000 (z 4.63). So the rule would have fired at 500 requests. Who decides: the prompt owner (the engineer on call for this service) can roll back alone, at any time, no approval needed, because it is the low-risk move. Promoting v12 beyond the canary needs the prompt owner and the product owner, and a written note of the eval result. Weak answer: "1.5 percent versus 0.4 percent, it looks worse, let us watch it." Strong answer: "Z is 4.6, well beyond noise, v12 has about 4 times the failure odds. My rule says roll back when z is 3 or more with at least a half-point gap, so I roll back now, the owner does it on their own, and we fix the prompt and canary again."

**Code:**
```python
import math
from scipy import stats
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
k1, n1, k0, n0 = 15, 1000, 36, 9000
p1, p0 = k1/n1, k0/n0
assert (p1, p0) == (0.015, 0.004)
pp = (k1 + k0) / (n1 + n0)
se = math.sqrt(pp*(1-pp)*(1/n1 + 1/n0))
z = (p1 - p0) / se
p_two = 2*(1 - stats.norm.cdf(z))
print(f"v12 {p1:.2%} (Wilson {wilson(k1,n1)[0]:.2%} to {wilson(k1,n1)[1]:.2%}); v11 {p0:.2%} (Wilson {wilson(k0,n0)[0]:.2%} to {wilson(k0,n0)[1]:.2%})")
print(f"difference {p1-p0:+.2%}; pooled SE {se:.4f}; z = {z:.2f}; two-sided p = {p_two:.1e}")
assert round(se, 4) == 0.0024 and round(z, 2) == 4.63 and p_two < 1e-4
# Exact check: Fisher
odds, pf = stats.fisher_exact([[k1, n1-k1], [k0, n0-k0]])
print(f"Fisher exact p = {pf:.1e}; odds ratio {odds:.2f}"); assert pf < 1e-3
# If v12 were as good as v11, expected failures in 1,000 requests and chance of seeing 15 or more
exp = n1*p0; tail = stats.binom.sf(k1-1, n1, p0)
print(f"expected {exp:.1f} failures if equal; P(>=15) = {tail:.1e}"); assert round(exp, 1) == 4.0 and tail < 1e-4
# Sequential peeking: how large must the difference be after only 100 canary requests to roll back? Using z >= 3 as a stop rule
# Pre-registered rule (illustrative): checkpoints every 250 requests; roll back if z >= 3 vs v11 AND v12 rate >= 0.4% + 0.5 points
def decide(kv, nv, kb=36, nb=9000):
    p_v = kv/nv; p_b = kb/nb; pooled = (kv+kb)/(nv+nb)
    s = math.sqrt(pooled*(1-pooled)*(1/nv+1/nb)); zz = (p_v-p_b)/s if s else 0
    return round(zz, 2), (zz >= 3 and p_v - p_b >= 0.005)
for kv, nv in [(4, 250), (7, 500), (11, 750), (15, 1000)]:
    print(f"checkpoint {nv:4d}: v12 failures {kv:2d} -> z, rollback = {decide(kv, nv)}")
assert decide(15, 1000)[1] is True and decide(4, 250)[1] is False
# Extra bad outputs if v12 went to 100% of 200,000 requests/day
extra = (p1 - p0) * 200_000
print(f"extra parse failures per day at 100% rollout of 200,000/day: {extra:,.0f}"); assert round(extra) == 2200
```

**Output (my run):**
```text
v12 1.50% (Wilson 0.91% to 2.46%); v11 0.40% (Wilson 0.29% to 0.55%)
difference +1.10%; pooled SE 0.0024; z = 4.63; two-sided p = 3.6e-06
Fisher exact p = 9.0e-05; odds ratio 3.79
expected 4.0 failures if equal; P(>=15) = 1.9e-05
checkpoint  250: v12 failures  4 -> z, rollback = (2.85, False)
checkpoint  500: v12 failures  7 -> z, rollback = (3.24, True)
checkpoint  750: v12 failures 11 -> z, rollback = (4.05, True)
checkpoint 1000: v12 failures 15 -> z, rollback = (4.63, True)
extra parse failures per day at 100% rollout of 200,000/day: 2,200
```

**Follow-ups:**
- Is z of 4.6 too good to trust with only 1,000 requests? The test accounts for the sample size, and the Fisher and binomial checks agree. The bigger worry is design (non-random assignment or clustering), not size.
- What if v12 improves answer quality by 2 points? I weigh them with a cost for each failure. If a parse failure triggers a retry that costs little, a quality gain may justify it; if it breaks an action, it does not. I would fix the parse issue and keep the gain.
- How long do you canary? Until the pre-set sample is reached and across a full weekday cycle, so that day-of-week patterns are covered.

**Common mistakes:**
- Comparing percentages without a test, or running a test but ignoring the size of the difference.
- Checking continuously and stopping at the first scary number with no rule.
- Non-random canary assignment.
- Deciding the rollback rule after seeing the result.
- Nobody owns the rollback, so it waits for a meeting.

### Q12 ⭐⭐⭐ 🟡 On an extraction task a prompt scored 156 of 200 (78%) in one run and 166 of 200 (83%) in another run of the same model and prompt, because of sampling at temperature 0.7. A teammate wants to ship a new prompt that scored 83% in a single run. What is the run-to-run noise, and how do you design the comparison?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to non-determinism and temperature topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** A 5-point gap between two runs of the same prompt is the noise level, so one 83% run proves nothing; I would compare the two prompts on the same items, several runs each, and ship only if the paired gain clears the noise.

**Clarifying questions:**
- Are the 200 items the same in both runs? Why it matters: same items means a paired comparison, which is much tighter than two separate samples.
- Is the new prompt's 83% on those same 200 items? Why it matters: if not, item difficulty is mixed into the gap.
- How is a run scored (exact match, field-level, judge)? Why it matters: a judge adds its own noise on top of sampling noise.
- Do we need sampling at temperature 0.7, or is that a leftover setting? Why it matters: production settings decide which noise we must live with.
- What gain is worth the switch (cost, latency, risk)? Why it matters: sets the minimum effect size and the sample size.

**Approach:**
1. Measure the noise first. Run the OLD prompt 5 to 10 times on the same 200 items and look at the spread. Here the two runs already differ by 5 points (156 versus 166 of 200).
2. Upper bound from the binomial: one run has an SD of about 2.8 points, and the gap between two runs has an SD of about 4.0 points, so 5 points is 1.26 SD (p about 0.21).
3. Item-level noise is usually smaller, because the same items are re-asked. A toy model with a few coin-flip items gives about 1.5 points per run. The honest range is therefore roughly 1.5 to 2.8 points per run.
4. Note the teammate's 83% equals the old prompt's second run. There is no evidence of improvement yet.
5. Run both prompts k times (say 5) on the same items. Score each item as the mean over runs. Compare per item (paired).
6. Test with a paired method: McNemar or sign test on majority-vote results, or a paired bootstrap over items. Report the difference with an interval.
7. Size the set for the gain you care about. For +3 points at 80% power, about 2,788 items per prompt unpaired, about 869 paired if 10% of items disagree.
8. Decide before looking: ship if the interval for the gain excludes zero and the lower end beats the cost of switching.

**Metrics:**
- Accuracy per run = items correct / 200 items. Mean accuracy per prompt = average over runs.
- Run-to-run SD = standard deviation of accuracy across repeat runs of the same prompt.
- Paired gain = (items only new gets right, minus items only old gets right) / N, with a 95% interval.
- Flip rate = items whose answer changes between runs of the same prompt / N.
- Guardrails: parse-failure rate, latency, cost per call, and no loss on a held-out slice that matters.

**Risks:**
- Shipping a prompt picked as the best of several single runs (winner's curse: the best of many noisy runs is biased upward).
- Tuning the prompt on the same 200 items, then testing on them.
- Judge noise mistaken for model noise.
- Treating "not significant" as "no difference". The set may just be too small.

**What the interviewer scores:**
- Strong: measures noise by repeating the baseline, uses a paired design, quotes an interval and a sample size.
- Strong: notices the new 83% matches the old prompt's own 83% run.
- Weak: "83 is higher than 78, ship it", or "just set temperature 0" without testing the production setting.
- Weak: no number for the noise, no mention of the same items.

**Example:** Illustrative numbers. Old prompt: 156 and 166 of 200 in two runs. New prompt: one run of 166 of 200. Weak answer: "It is 83, the old one is 78, so we have a 5-point gain, let us ship." Strong answer: "The old prompt itself moved 5 points between runs, so a single 83 is inside the noise. I will run each prompt 5 times on the same items, compare item by item, and look at the interval. If 38 items flip to the new prompt and 22 flip to the old one, the sign test gives p of about 0.052, which is borderline, so I would collect more items before shipping."

**Code:**
```python
import math
import numpy as np
from scipy import stats

n = 200
a, b = 156, 166
pa, pb = a / n, b / n
assert (pa, pb) == (0.78, 0.83)
pbar = (a + b) / (2 * n)
se_run = math.sqrt(pbar * (1 - pbar) / n)          # binomial SD of one run's accuracy (upper bound)
se_diff = math.sqrt(2) * se_run                    # two independent runs
z = (pb - pa) / se_diff
p2 = 2 * (1 - stats.norm.cdf(z))
print(f"one-run SD (binomial upper bound) = {se_run*100:.2f} pts; SD of difference of two runs = {se_diff*100:.2f} pts")
print(f"observed gap 5.0 pts = {z:.2f} SD, two-sided p = {p2:.2f}")
assert round(se_run * 100, 1) == 2.8 and round(se_diff * 100, 1) == 4.0 and round(z, 2) == 1.26 and round(p2, 2) == 0.21

# Toy flaky-item model (invented): 150 steady-right items, 20 coin-flip items, 30 mostly-wrong items.
rng = np.random.default_rng(7)
p_item = np.array([0.98] * 150 + [0.5] * 20 + [0.05] * 30)
var_items = float((p_item * (1 - p_item)).sum())
sd_run_toy = math.sqrt(var_items) / n * 100
sd_diff_toy = math.sqrt(2) * sd_run_toy
runs = rng.random((20000, 2, n)) < p_item
acc = runs.mean(axis=2)
gap = np.abs(acc[:, 0] - acc[:, 1])
print(f"toy same-items model: mean acc {p_item.mean()*100:.1f}%, one-run SD {sd_run_toy:.2f} pts, SD of gap {sd_diff_toy:.2f} pts")
print(f"toy: share of run pairs with |gap| >= 5 pts = {np.mean(gap >= 0.05 - 1e-9)*100:.1f}%")
assert round(sd_run_toy, 1) == 1.5 and round(sd_diff_toy, 1) == 2.2
assert abs(np.mean(gap >= 0.05 - 1e-9) - 0.03) < 0.02

# Sample size for a 3-point gain at 80% power, 5% two-sided.
za, zb = 1.96, 0.84
delta, p0 = 0.03, 0.80
n_unpaired = 2 * p0 * (1 - p0) * (za + zb) ** 2 / delta ** 2
d = 0.10                                           # assumed share of items where the two prompts disagree
n_paired = ((za * math.sqrt(d) + zb * math.sqrt(d - delta ** 2)) / delta) ** 2
print(f"items needed per prompt, unpaired: {n_unpaired:.0f}; paired (10% of items disagree): {n_paired:.0f}")
assert round(n_unpaired) == 2788 and round(n_paired) == 869

# Paired McNemar-style exact test on a made-up result: 400 items, 5 runs per prompt, majority vote.
b_only, a_only = 38, 22                            # items only new right, items only old right
p_mc = stats.binomtest(b_only, b_only + a_only, 0.5).pvalue
print(f"discordant 38 vs 22 -> exact sign test p = {p_mc:.3f}")
assert round(p_mc, 3) == 0.052
```

**Output (my run):**
```
one-run SD (binomial upper bound) = 2.80 pts; SD of difference of two runs = 3.96 pts
observed gap 5.0 pts = 1.26 SD, two-sided p = 0.21
toy same-items model: mean acc 79.3%, one-run SD 1.53 pts, SD of gap 2.16 pts
toy: share of run pairs with |gap| >= 5 pts = 2.8%
items needed per prompt, unpaired: 2788; paired (10% of items disagree): 869
discordant 38 vs 22 -> exact sign test p = 0.052
```

**Follow-ups:**
- Would temperature 0 fix this? It removes most sampling noise, but it may not match production, and Book 2 Part 02 Q21 ("Is temperature 0 deterministic? What causes run-to-run differences in LLM output, and how do you get reproducibility?") covers why outputs can still vary. Test the setting you will ship.
- What if the set is only 200 items and cannot grow? Use more runs to cut sampling noise, but item-selection noise stays, so report the interval and say it is a small set.
- Majority vote or mean? Use the mean for the estimate. Majority vote is fine for the sign test, but say so.

**Common mistakes:**
- Comparing two single runs.
- Using the independent-sample formula when the items are shared (too loose) or ignoring item correlation in the other direction.
- Forgetting that the first run of each prompt is not special; picking the best run.
- Quoting a p-value without a sample size or effect size.

### Q13 ⭐⭐⭐ 🟡 Each query could stuff a 100,000-token document set into the prompt or retrieve 6,000 tokens, at an illustrative 3 per million input tokens and 20,000 queries a day. Compute the daily input cost of each approach, and say what accuracy and latency evidence you would want before choosing.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to long-context versus RAG topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Stuffing costs 6,000 a day against 360 for retrieval, a gap of 5,640 a day, so I would only stuff if tests show retrieval loses enough accuracy to be worth that gap.

**Clarifying questions:**
- Is the 100,000-token set the same on every query? Why it matters: an identical prefix can be cached at a lower rate, which changes the comparison.
- What is the model's context window and its price for long inputs? Why it matters: some limits and prices change with length.
- Are the answers found in one passage or spread across many documents? Why it matters: spread-out questions favour stuffing; single-passage questions favour retrieval.
- What is the latency target? Why it matters: long prompts take longer to process before the first token.
- How often does the document set change? Why it matters: stuffing needs no index, but caching breaks on every change.

**Approach:**
1. Compute the input cost. Stuffing: 100,000 x 20,000 = 2 billion tokens a day, at 3 per million = 6,000. Retrieval: 6,000 x 20,000 = 120 million tokens, = 360. Ratio about 16.7x.
2. Add what the prompt left out: output tokens (same in both), and the retrieval pipeline (embeddings, vector store, reranker). The saving is 5,640 a day (about 2.06 million a year, illustrative), so the pipeline must cost more than that to lose.
3. Check the cached case. If the 100k set is identical every call and cached reads cost 10% of the input rate (invented), stuffing costs 600 a day. That is still above retrieval's 360.
4. Build a labelled question set from real traffic, including multi-document questions.
5. Run both approaches, plus retrieval with a bigger top-k, on the same questions. Measure correctness, citation accuracy, and refusals.
6. Measure latency end to end: p50 and p95 time to first token and total time. Stuffing pays a long prefill; retrieval pays a retrieval hop.
7. Choose by the cheapest approach that meets the accuracy bar. Consider a hybrid: retrieve a larger slice (say 20,000 tokens) for hard questions only.

**Metrics:**
- Daily input cost = input tokens per query x queries per day x price per token.
- Accuracy = correct answers / graded questions, with an interval and a slice for multi-document questions.
- Retrieval recall@k = questions whose needed passage is in the top k / all questions.
- Latency p95 of time to first token and of total response time.
- Guardrails: citation correctness, refusal rate, cost per correct answer.

**Risks:**
- Long-context accuracy may drop for facts buried in the middle (Book 2 Part 01 Q19 covers the "lost in the middle" heading: "What is the context window, and why is the effective context often shorter than the advertised one").
- Retrieval may miss the passage and answer confidently anyway.
- Costing only input and forgetting the retrieval infrastructure.
- Evaluating on easy questions only.

**What the interviewer scores:**
- Strong: correct arithmetic, names cached stuffing as the fair comparison, asks for accuracy and latency evidence.
- Strong: cost per correct answer, not cost alone.
- Weak: "long context is always better" or "RAG is always cheaper so use it" with no test.
- Weak: ignoring latency.

**Example:** Illustrative. Retrieval answers 82% correctly at 360 a day; stuffing answers 86% at 6,000 a day. Weak: "Stuffing is more accurate, use it." Strong: "Four points of accuracy cost 5,640 a day, which is about 1,410 per accuracy point per day. I would first try retrieving 20,000 tokens or a reranker to close the gap, and stuff only the questions retrieval cannot answer."

**Code:**
```python
queries = 20_000
price = 3.0                                        # illustrative, per million input tokens
stuff, rag = 100_000, 6_000
cost = lambda tok: tok * queries * price / 1e6
c_stuff, c_rag = cost(stuff), cost(rag)
print(f"stuffing: {stuff*queries/1e9:.1f} billion tokens/day -> {c_stuff:,.0f} per day")
print(f"retrieval: {rag*queries/1e6:.0f} million tokens/day -> {c_rag:,.0f} per day")
assert c_stuff == 6000 and c_rag == 360
print(f"ratio {c_stuff/c_rag:.1f}x, gap {c_stuff-c_rag:,.0f} per day = {(c_stuff-c_rag)*365:,.0f} per year")
assert round(c_stuff / c_rag, 1) == 16.7 and (c_stuff - c_rag) * 365 == 2_058_600
# If the 100k set is identical every call and cached reads cost 10% of the input rate (invented).
c_cached = cost(stuff) * 0.10
print(f"stuffing with 100% cached prefix at 10% rate: {c_cached:,.0f} per day (still above retrieval {c_rag:,.0f})")
assert c_cached == 600 and c_cached > c_rag
# Break-even: what retrieval pipeline overhead per day would erase the saving?
print(f"retrieval overhead (embedding, vector DB, reranker) would need to exceed {c_stuff-c_rag:,.0f} per day to lose")
```

**Output (my run):**
```
stuffing: 2.0 billion tokens/day -> 6,000 per day
retrieval: 120 million tokens/day -> 360 per day
ratio 16.7x, gap 5,640 per day = 2,058,600 per year
stuffing with 100% cached prefix at 10% rate: 600 per day (still above retrieval 360)
retrieval overhead (embedding, vector DB, reranker) would need to exceed 5,640 per day to lose
```

**Follow-ups:**
- Does caching make stuffing win? Not here. At the invented 10% rate it is 600 against 360, and the cache needs an identical prefix and recent traffic. See Book 2 Part 01 Q24 ("What are prompt/prefix caching in LLM APIs, and how do they relate to the KV cache? How do you structure prompts to benefit?").
- What if answers need many documents? Use a larger retrieval budget, multi-step retrieval, or stuff for that class only.
- What about the price for very long inputs? Check the provider's current price sheet; I do not assume it is linear.

**Common mistakes:**
- Comparing cost without accuracy.
- Forgetting output tokens and pipeline costs.
- Using average questions and missing the hard multi-document ones.
- Quoting vendor limits from memory.

### Q14 ⭐⭐⭐ 🟡 A bot answers in English and Hindi. An illustrative tokenizer gives 1.3 tokens per English word and 4 per Hindi word, a 150-word answer is generated in each language, and on 200 graded answers per language correctness is 74% for Hindi against 88% for English. Compute tokens and relative output cost per answer, the absolute and relative correctness gaps, and what you would do.
**Asked at:** Indic-language and tokenizer material (an ACL Anthology LoResLM 2026 paper on informal and romanised Hindi tokenization, an arXiv study of tokenizer efficiency across the 22 official Indian languages, a HackerNoon opinion piece on the cost of building AI for Indian languages); research and commentary pages rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** A Hindi answer uses about 3.1x the output tokens of an English one (600 against 195), and Hindi is 14 points less correct (74% against 88%), a gap too big to be noise, so I would find out why and fix quality before cost.

**Clarifying questions:**
- Are the 200 Hindi and 200 English questions the same questions, translated? Why it matters: if they differ, the gap may be difficulty, not language.
- Who graded the Hindi answers, and how? Why it matters: a judge or grader weaker in Hindi can inflate the gap.
- Do users write Hindi in Devanagari, romanised Hindi, or mixed? Why it matters: each tokenizes and retrieves differently.
- Is the tokens-per-word figure measured on our tokenizer? Why it matters: the 1.3 and 4 are illustrative inputs.
- What share of traffic is Hindi? Why it matters: it sizes both the cost and the quality problem.

**Approach:**
1. Tokens per answer: English 150 x 1.3 = 195; Hindi 150 x 4 = 600. Relative output cost 600/195 = 3.08x at the same price per token.
2. Correctness gap: 74% versus 88%. Absolute gap 14 points. Relative gap 14/88 = 15.9% (Hindi is 15.9% lower than English). Error rate 26% versus 12% is 2.17x.
3. Is it real? Difference SE is 3.86 points, z = 3.63, 95% interval for the gap about 6.4 to 21.6 points. Yes.
4. Cost per correct answer is worse than cost per answer: 600/0.74 = 811 tokens versus 195/0.88 = 222, a ratio of 3.66x.
5. Diagnose the cause on paired questions: translation errors, retrieval misses in Hindi, grader bias, or genuine model weakness. Read 50 failures.
6. Fix in order of cheapness: better Hindi retrieval and prompts, few-shot Hindi examples, a different model for Hindi, shorter answers, a language-specific eval gate.
7. Track cost per correct answer by language, and put a minimum quality bar per language before launch.

**Metrics:**
- Tokens per answer = output tokens / answers, per language.
- Correctness = graded-correct answers / graded answers, per language, with a Wilson interval.
- Absolute gap = English correctness minus Hindi correctness (points). Relative gap = absolute gap / English correctness.
- Cost per correct answer = cost per answer / correctness.
- Guardrails: answer-length cap, human-audited sample of Hindi grades.

**Risks:**
- Blaming the tokenizer when the cause is retrieval or grading.
- Cutting Hindi length to save cost and losing completeness.
- Reporting only the average across languages.
- Romanised or code-mixed input missing from the test set.

**What the interviewer scores:**
- Strong: both the cost and the quality numbers, an interval, and a cause-finding plan.
- Strong: cost per correct answer and a per-language gate.
- Weak: "Hindi is just expensive, accept it", or "fine-tune a model" with no diagnosis.
- Weak: mixing up absolute and relative gaps.

**Example:** Illustrative. Weak: "Hindi is 14 percent worse and costs 3 times more." That mixes points with percent. Strong: "Hindi is 14 points lower, which is 15.9% relative to English, and errors are 2.17 times as frequent. Each Hindi answer uses 600 tokens against 195, so a correct Hindi answer costs 3.66 times as many output tokens. I would first read 50 Hindi failures to see if it is retrieval, grading or the model."

**Code:**
```python
import math
words = 150
en_tok, hi_tok = words * 1.3, words * 4
ratio = hi_tok / en_tok
print(f"tokens per answer: English {en_tok:.0f}, Hindi {hi_tok:.0f}; cost ratio {ratio:.2f}x")
assert en_tok == 195 and hi_tok == 600 and round(ratio, 2) == 3.08
n = 200
hi_ok, en_ok = 148, 176
ph, pe = hi_ok / n, en_ok / n
assert (ph, pe) == (0.74, 0.88)
gap_abs = pe - ph
print(f"absolute gap {gap_abs*100:.0f} points; relative gap {gap_abs/pe*100:.1f}% of English; error rate {1-ph:.0%} vs {1-pe:.0%} = {(1-ph)/(1-pe):.2f}x")
assert round(gap_abs * 100) == 14 and round(gap_abs / pe * 100, 1) == 15.9 and round((1 - ph) / (1 - pe), 2) == 2.17
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
for nm, k in (("Hindi", hi_ok), ("English", en_ok)):
    lo, hi = wilson(k, n); print(f"{nm} 95% Wilson interval {lo*100:.1f}% to {hi*100:.1f}%")
se = math.sqrt(ph * (1 - ph) / n + pe * (1 - pe) / n)
z = gap_abs / se
print(f"difference SE {se*100:.2f} pts, z = {z:.2f}, 95% CI of gap {(gap_abs-1.96*se)*100:.1f} to {(gap_abs+1.96*se)*100:.1f} pts")
assert round(z, 2) == 3.63 and (gap_abs - 1.96 * se) > 0
cpc_h, cpc_e = hi_tok / ph, en_tok / pe
print(f"output tokens per correct answer: Hindi {cpc_h:.1f}, English {cpc_e:.1f}, ratio {cpc_h/cpc_e:.2f}x")
assert round(cpc_h / cpc_e, 2) == 3.66
```

**Output (my run):**
```
tokens per answer: English 195, Hindi 600; cost ratio 3.08x
absolute gap 14 points; relative gap 15.9% of English; error rate 26% vs 12% = 2.17x
Hindi 95% Wilson interval 67.5% to 79.6%
English 95% Wilson interval 82.8% to 91.8%
difference SE 3.86 pts, z = 3.63, 95% CI of gap 6.4 to 21.6 pts
output tokens per correct answer: Hindi 810.8, English 221.6, ratio 3.66x
```

**Follow-ups:**
- Why does Hindi use more tokens? Tokenizers trained mostly on English split Devanagari into more pieces; Book 2 Part 02 Q1 ("Why do LLMs use subword tokenization instead of words or characters?") gives the background. Measure it on your tokenizer.
- Does a different model fix it? Possibly. Test on the same Hindi questions and compare cost per correct answer.
- What about input tokens? The same effect applies to Hindi prompts and retrieved text, so the real multiplier can be higher.

**Common mistakes:**
- Quoting "14%" for a 14-point gap.
- Ignoring the interval.
- Comparing different question sets across languages.
- Optimising token cost while quality is the bigger problem.

### Q15 ⭐⭐⭐ 🔴 An agent task is capped at 25 steps, and 600 of 20,000 tasks (3%) hit the cap while the other 19,400 average 6 steps. Compute the share of all steps spent by the capped tasks, and explain how you would find why they loop and what hard controls you would add beyond the cap.
**Asked at:** Agent cost and loop-control material (solo.io and getmaxim pages on iteration and token ceilings for agent loops, a Towards Data Science article on agent token costs, an Exponent-sourced 2026 guide that mentions a candidate-reported agent-with-RAG token-cost design prompt); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The capped 3% of tasks burn 15,000 of 131,400 steps, which is 11.4%, and probably more of the token cost because each step re-sends a longer history; I would read the capped traces, find the loop pattern, and add budgets that stop it early.

**Clarifying questions:**
- Does a step mean one model call, or one tool call? Why it matters: cost scales with model calls.
- Does each step re-send the full history? Why it matters: it makes long tasks cost much more than their step share.
- Do capped tasks end with a wrong answer, a partial answer, or a user retry? Why it matters: sets the cost of failure.
- Do any steps write to external systems? Why it matters: loops with side effects are a safety issue, not only cost.
- Is 25 a design limit or a guess? Why it matters: some tasks may legitimately need more.

**Approach:**
1. Steps: capped 600 x 25 = 15,000. Others 19,400 x 6 = 116,400. Total 131,400. Capped share = 11.4% (they are 3% of tasks).
2. Cost share is larger if history is re-sent. If each step adds equal tokens and the whole history is re-sent, a k-step task costs about k(k+1)/2 units: 325 for 25 steps against 21 for 6 steps (15.5x). Capped share of input tokens is then at most about 32%. This is a model, not a measurement; spread in the other tasks' step counts lowers it (about 29.5% in a simulation).
3. Pull the 600 traces. Cluster them: same tool called with the same arguments, a tool that keeps erroring, a plan that never converges, ambiguous user goal, a missing tool.
4. Compare with 100 normal traces to see where they diverge (first repeated step).
5. Add hard controls beyond the step cap: a token and cost budget per task, a wall-clock limit, a repeat detector (same tool and arguments hash twice), a cap per tool, a no-progress check, a circuit breaker that stops and escalates to a human or a fixed fallback answer, and idempotency or approval for any write action.
6. Fix the root cause: better tool error messages, a clearer stop condition, an "I cannot finish" action the agent can choose.
7. Alert on the capped share per day and the cost of the top 1% of tasks.

**Metrics:**
- Capped rate = tasks that hit the cap / all tasks (3.0%).
- Step share = steps in capped tasks / all steps (11.4%).
- Token cost share = input plus output tokens of capped tasks / all tokens (measured, not modelled).
- Cost per resolved task = total cost / tasks resolved.
- Guardrails: resolution rate must not fall when budgets tighten; repeated-write incidents = 0.

**Risks:**
- A tighter cap cuts off tasks that are legitimately long.
- Repeat detection misses loops that vary the arguments slightly.
- Budgets end the task but leave a half-finished write.
- Fixing the symptom: the agent loops on a missing capability.

**What the interviewer scores:**
- Strong: correct 11.4%, notices cost share differs from step share, reads traces, lists several hard controls.
- Strong: treats loops with writes as a safety matter.
- Weak: "lower the cap to 10" with no trace review.
- Weak: ignores history growth.

**Example:** Illustrative. Weak: "Only 3% of tasks hit the cap, ignore it." Strong: "Those 3% are 11.4% of steps, and if the context is re-sent each step, up to about 32% of input tokens. I would pull the 600 traces, find that most repeat one failing tool call, add a repeat detector and a per-task token budget, and make the tool return a clear error so the agent can stop."

**Code:**
```python
tasks, capped, cap, avg_other = 20_000, 600, 25, 6
other = tasks - capped
assert other == 19_400 and capped / tasks == 0.03
s_cap, s_oth = capped * cap, other * avg_other
share = s_cap / (s_cap + s_oth)
print(f"steps: capped {s_cap:,}, others {s_oth:,}, total {s_cap+s_oth:,}; capped share {share*100:.1f}%")
assert (s_cap, s_oth) == (15_000, 116_400) and round(share * 100, 1) == 11.4
# If every step re-sends the whole history (equal tokens added per step), input tokens of a k-step task ~ k(k+1)/2 units.
tri = lambda k: k * (k + 1) // 2
c_cap, c_oth = capped * tri(cap), other * tri(6)
sh2 = c_cap / (c_cap + c_oth)
print(f"history-resend model: capped task {tri(cap)} units vs 6-step task {tri(6)} units = {tri(cap)/tri(6):.1f}x")
print(f"capped share of input tokens <= {sh2*100:.1f}% (treats 'average 6' as exactly 6; spread would lower this share)")
assert (tri(25), tri(6)) == (325, 21) and round(tri(25) / tri(6), 1) == 15.5 and round(sh2 * 100, 1) == 32.4
# Convexity check: spreading steps around a mean of 6 raises others' cost, so the capped share only falls.
import numpy as np
rng = np.random.default_rng(3)
steps = rng.poisson(6, other)
steps = np.clip(steps, 1, 24)
c_oth2 = float((steps * (steps + 1) // 2).sum())
sh3 = c_cap / (c_cap + c_oth2)
print(f"with Poisson(6) spread: others' mean steps {steps.mean():.2f}, capped share {sh3*100:.1f}%")
assert sh3 < sh2
```

**Output (my run):**
```
steps: capped 15,000, others 116,400, total 131,400; capped share 11.4%
history-resend model: capped task 325 units vs 6-step task 21 units = 15.5x
capped share of input tokens <= 32.4% (treats 'average 6' as exactly 6; spread would lower this share)
with Poisson(6) spread: others' mean steps 6.00, capped share 29.5%
```

**Follow-ups:**
- How do you set the cap? From the distribution of steps in successful tasks, for example above the 99th percentile of successful runs, and review it as tasks change.
- What if the agent writes to a database in the loop? Require idempotency keys and a confirmation step, and alert on repeated identical writes.
- Is a loop always a bug? No. Some tasks are long; separate "long and progressing" from "repeating".

**Common mistakes:**
- Treating step share as cost share.
- Raising or lowering the cap without looking at traces.
- Only a step cap and no token or cost cap.
- No fallback when the budget is hit.

### Q16 ⭐⭐⭐ 🔴 A semantic cache with a similarity threshold of 0.92 serves 35% of 1,000,000 monthly calls (350,000 hits) at an illustrative 0.012 saved per hit. A human review of 400 sampled hits finds 28 wrong answers, for example a different product with a similar name. Compute the savings, the sample wrong-answer rate and the count of wrong cached answers projected if the sample is representative, and say how you would change the cache.
**Asked at:** LLM cost and routing pages (getmaxim cost and semantic-cache guides, tianpan and system-design.space pages on routing and cascades, a Towards Data Science article on saving tokens in agentic AI, a Towards AI piece on AI system-design interview patterns); practitioner material, no confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The cache saves 4,200 a month gross, but the sample says 7% of hits are wrong, about 24,500 wrong answers a month if representative, so unless a wrong answer costs under about 0.17, I would tighten the cache.

**Clarifying questions:**
- Was the sample of 400 hits random? Why it matters: a convenience sample cannot be projected.
- What is the error rate of the fresh model on the same questions? Why it matters: the cache only adds the extra errors, not all of them.
- What does a wrong answer cost (refund, ticket, trust)? Why it matters: it sets the break-even.
- Which queries are hits: FAQs or product-specific questions? Why it matters: product-specific ones carry the risk.
- Who judged "wrong", and how were disagreements handled? Why it matters: sets label quality.

**Approach:**
1. Savings: 35% of 1,000,000 = 350,000 hits x 0.012 = 4,200 a month (gross, illustrative).
2. Wrong rate: 28/400 = 7.0%, 95% Wilson interval 4.9% to 9.9%.
3. Projection: 7.0% x 350,000 = 24,500 wrong cached answers a month, range about 17,100 to 34,800. Only valid if the sample was random.
4. Break-even: 4,200 / 24,500 = 0.171 per wrong answer, which is 14.3x the saving per hit. If a wrong answer costs more than about 0.17, the cache loses money.
5. Net the baseline. If the fresh model is wrong 4% of the time on the same questions (invented), the cache adds 3 points, or 10,500 extra wrong answers.
6. Change the cache: raise the threshold, or use a per-category threshold; require entity match (product ID, version, region) before serving; cache only intents that are generic; exclude personalised or account queries; add a TTL tied to how fast content changes; add a cheap verification step on the cached answer.
7. Plot the threshold: hit share against wrong share of hits on a labelled set. A toy run shows both falling together as the threshold rises, so pick the point by cost.
8. Keep a human-reviewed sample of hits every week and alert if the wrong rate moves.

**Metrics:**
- Hit rate = cache hits / calls (35%).
- Wrong-hit rate = wrong cached answers / sampled hits (7%), with an interval.
- Extra error = wrong-hit rate minus fresh-model error rate on the same queries.
- Net saving = hits x saving per hit minus extra errors x cost per error.
- Guardrails: wrong rate by category, complaints tied to cached answers.

**Risks:**
- Similar-looking but different entities (the product-name case) return confident wrong answers.
- Stale answers after a price or policy change.
- One bad cached answer is served to many users.
- Cached answers leaking one customer's data to another.

**What the interviewer scores:**
- Strong: all three numbers, an interval, and the break-even cost per error.
- Strong: asks whether the sample was random, and nets the baseline error.
- Weak: "7% is small, the cache saves money, keep it".
- Weak: only "raise the threshold" with no entity check or measurement.

**Example:** Illustrative. Weak: "Raise the threshold to 0.97." Strong: "At 0.92, 7% of hits are wrong; I would add an entity check so a different product never matches, set a higher threshold for product questions, and re-measure on 400 fresh hits. At 0.17 break-even per wrong answer, a refund-bot error probably costs more than that, so I would be strict there."

**Code:**
```python
import math
calls, hit_share, save = 1_000_000, 0.35, 0.012
hits = int(calls * hit_share)
gross = hits * save
print(f"hits {hits:,}; gross savings {gross:,.0f} per month")
assert hits == 350_000 and round(gross) == 4200
k, n = 28, 400
p = k / n
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
lo, hi = wilson(k, n)
print(f"sample wrong rate {p:.1%}, 95% Wilson {lo:.1%} to {hi:.1%}")
print(f"projected wrong cached answers {p*hits:,.0f} (range {lo*hits:,.0f} to {hi*hits:,.0f})")
assert p == 0.07 and round(p * hits) == 24_500 and (round(lo, 3), round(hi, 3)) == (0.049, 0.099)
be = gross / (p * hits)
print(f"break-even cost of one wrong answer = {be:.3f} = {be/save:.1f}x the saving per hit")
assert round(be, 3) == 0.171 and round(be / save, 1) == 14.3
base = 0.04   # invented: error rate the fresh model would have on the same questions
print(f"if fresh answers are wrong {base:.0%} of the time, extra errors from the cache = {(p-base)*hits:,.0f}")
assert round((p - base) * hits) == 10_500
# Toy threshold sweep with invented similarity scores for hits that are right vs wrong.
import numpy as np
rng = np.random.default_rng(11)
right = np.clip(rng.normal(0.96, 0.025, 93_000), 0, 1)
wrong = np.clip(rng.normal(0.935, 0.015, 7_000), 0, 1)
prev = None
for th in (0.92, 0.94, 0.96):
    kr, kw = (right >= th).sum(), (wrong >= th).sum()
    hit, wr = (kr + kw) / 100_000, kw / (kr + kw)
    print(f"toy threshold {th}: hit share {hit:.1%}, wrong share of hits {wr:.1%}")
    if prev: assert hit < prev[0] and wr < prev[1]
    prev = (hit, wr)
```

**Output (my run):**
```
hits 350,000; gross savings 4,200 per month
sample wrong rate 7.0%, 95% Wilson 4.9% to 9.9%
projected wrong cached answers 24,500 (range 17,105 to 34,758)
break-even cost of one wrong answer = 0.171 = 14.3x the saving per hit
if fresh answers are wrong 4% of the time, extra errors from the cache = 10,500
toy threshold 0.92: hit share 93.8%, wrong share of hits 6.4%
toy threshold 0.94: hit share 75.8%, wrong share of hits 3.4%
toy threshold 0.96: hit share 46.8%, wrong share of hits 0.8%
```

**Follow-ups:**
- Is the 24,500 an exact count? No. It is a projection from a sample, with a range of roughly 17,100 to 34,800.
- Would a higher threshold fix it? It reduces wrong hits but also hit rate; the toy sweep shows both falling. Entity checks fix the specific failure better.
- How do you invalidate stale entries? TTL plus explicit purge when the source content changes.

**Common mistakes:**
- Projecting from a non-random sample.
- Counting all wrong cached answers as caused by the cache.
- Comparing savings with no cost per error.
- Ignoring the privacy risk of shared caches.

### Q17 ⭐⭐⭐ 🔴 Conversation logs store full prompts for 400 days, and a scan of 500,000 stored conversations finds phone numbers or emails in 2% of them, which is 10,000 conversations. Support staff and an analytics vendor can read the logs. What do you do now, what do you change in the logging design, and how do you handle the 10,000 existing conversations?
**Asked at:** PII and compliance material (tianpan, Kunal Ganglani, Gravitee and barkingiguana pages on logs, retention, redaction and data residency, and a vendor piece on DPDP readiness for LLM traffic); vendor and practitioner pages, not regulator guidance or an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** I would stop the exposure now by limiting who can read the logs and masking PII before storage, then shorten retention and clean the 10,000 existing conversations, with legal deciding on any notification duty.

**Clarifying questions:**
- Did the scan cover all 500,000 conversations or a sample, and how was PII detected? Why it matters: a regex misses some PII, so 10,000 is probably a floor.
- What do support staff and the vendor need? Why it matters: least access can often replace full access.
- What does the vendor contract and data-processing agreement say? Why it matters: sets what the vendor may keep and train on.
- Why 400 days? Why it matters: the retention need decides how much to keep.
- Where are the logs stored (region, backups)? Why it matters: copies and residency add scope.

**Approach:**
1. Now: restrict log access to named roles, turn on access auditing, and check who has already read or exported them. Pause the vendor feed or redact it first.
2. Tell privacy and legal today. Whether this is a reportable incident and what notice is due is their decision; I do not make legal claims here.
3. Fix at the source: redact before write (detect phone numbers, emails, ids and replace with typed tokens like PHONE), keep raw prompts out of logs by default, and store only what debugging needs.
4. Split storage: raw (short retention, tight access) and redacted (longer retention, wider access). Encrypt both.
5. Cut retention to what is justified. If volume and PII rate are constant, 30 days keeps about 37,500 conversations with about 750 containing PII, against 10,000 at 400 days.
6. Backfill: run the redaction job over the 10,000 flagged conversations, plus a second, different detector to catch what the first missed. Keep a record of what was changed.
7. Verify: sample 1,000 after redaction. Zero hits means an upper bound near 0.30% (rule of three), not zero.
8. Deletion path: be able to find and delete a person's conversations on request.

**Metrics:**
- PII rate = conversations with detected PII / conversations scanned (2.0%).
- Detector recall = PII items found / PII items present, estimated on a hand-labelled sample.
- Reader count = distinct people or systems with access to raw logs.
- Residual rate after redaction with its upper bound.
- Guardrails: debugging resolution time, no redaction that breaks the logs' usefulness.

**Risks:**
- Redaction that is incomplete (names, addresses, free-text ids).
- The vendor already holds copies.
- Over-redaction that makes logs useless, so teams bypass the system.
- Deleting evidence needed for the review.

**What the interviewer scores:**
- Strong: stop the exposure first, involve legal, fix design, handle the backlog, verify with a bounded claim.
- Strong: notes the detector's recall limit.
- Weak: "delete everything" or "ignore, 2% is small".
- Weak: claims legal conclusions.

**Example:** Illustrative. Weak: "Run a regex and delete the matches." Strong: "I would cut vendor and support access to a named few today, mask on write from the next deploy, redact the 10,000 with two detectors, and report the residual as less than about 0.3% at 95% on a 1,000 sample. Legal decides on notification."

**Code:**
```python
import math
stored, hit_rate = 500_000, 0.02
n_pii = int(stored * hit_rate)
print(f"conversations with PII: {n_pii:,}")
assert n_pii == 10_000
# Steady-state effect of shorter retention (assumes constant volume and constant PII rate).
for days in (400, 90, 30):
    kept = stored * days / 400
    print(f"retention {days:>3} days: ~{kept:,.0f} stored, ~{kept*hit_rate:,.0f} with PII")
assert stored * 30 / 400 * hit_rate == 750
# After redaction at write, check a random sample; zero hits is not zero risk.
n = 1000
rule3 = 3 / n
exact = 1 - 0.05 ** (1 / n)
print(f"0 PII hits in {n} sampled: 95% upper bound ~{rule3:.2%} (rule of three), exact {exact:.3%}")
assert round(rule3, 4) == 0.003 and round(exact, 5) == 0.00299
# A regex scan has recall below 100%: if it finds 10,000 at recall 80%, the true count is higher.
for recall in (1.0, 0.8, 0.6):
    print(f"detector recall {recall:.0%}: implied true PII conversations ~{n_pii/recall:,.0f}")
assert round(n_pii / 0.8) == 12_500
```

**Output (my run):**
```
conversations with PII: 10,000
retention 400 days: ~500,000 stored, ~10,000 with PII
retention  90 days: ~112,500 stored, ~2,250 with PII
retention  30 days: ~37,500 stored, ~750 with PII
0 PII hits in 1000 sampled: 95% upper bound ~0.30% (rule of three), exact 0.299%
detector recall 100%: implied true PII conversations ~10,000
detector recall 80%: implied true PII conversations ~12,500
detector recall 60%: implied true PII conversations ~16,667
```

**Follow-ups:**
- Can you keep raw prompts for debugging? Yes, briefly, with restricted access and automatic expiry.
- What about the vendor's copy? Check the contract, ask for deletion or confirm retention, and stop sending raw data.
- How do you prove it is fixed? Scheduled scans with a labelled recall check and an access-audit report.

**Common mistakes:**
- Trusting a regex scan as complete.
- Redacting new logs and forgetting the backlog.
- Giving legal conclusions in the interview.
- Wide access "for convenience".

### Q18 ⭐⭐⭐ 🔴 Over three releases the offline pass rate on a 1,000-question set rose from 82% to 86% (4 points absolute), but the online resolution rate moved only from 61% before the three releases to 61.5% after, on 20,000 conversations a month in each period. List the reasons the two can diverge, say which check you do first, and how you would build an online metric you trust.
**Asked at:** LLM-evaluation pages (Manning's AI model evaluation chapter and an arXiv judge-bias study listing position, verbosity and self-preference bias, Arize and Langfuse pages on offline versus online evaluation, an LLM-as-judge survey); practitioner and academic material rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The offline +4 points and the online +0.5 points disagree even after noise (the online interval tops out near +1.5), so I would first check whether the offline set matches live traffic, then build an online metric from outcomes I trust.

**Clarifying questions:**
- How was the 1,000-question set built, and was it used to tune the releases? Why it matters: tuning on it inflates the offline score.
- What does "resolution" mean online, and who decides? Why it matters: it must reflect the user's problem being solved.
- What was the online metric before and after the three releases (the prompt shows "61% then 61.5%")? Why it matters: the comparison window sets the noise.
- Does the question mix match live intents? Why it matters: a different mix dilutes or hides gains.
- Are conversations grouped by user? Why it matters: repeat users make the online interval wider.

**Approach:**
1. Noise first. Online: +0.5 points, SE 0.49, 95% interval about -0.45 to +1.45 (assuming independent conversations). Offline: +4 points, SE 1.64 unpaired, interval about 0.8 to 7.2 (a paired test is tighter).
2. The offline +4 sits above the online upper limit of +1.45, so noise alone does not explain it. With clustered users the online interval widens (about +1.85 with a design effect of 2), so it is not certain either.
3. First check: traffic mix. Re-weight the offline results by the real intent distribution. Example: 50% hard items in the set with +8 gain on hard items gives +4 offline, but with 10% hard traffic the online gain is +0.8.
4. Then check: overfitting to the set across three releases, contamination (the set leaked into prompts or training data), judge or grader mismatch with real users, and different input styles (live typos, long chats).
5. Check the online definition: a resolution metric can be moved by user behaviour, channel changes, seasonality, and escalation rules, not only answer quality.
6. Build the online metric: resolution = conversations in scope with no re-contact in 7 days and no human escalation / all in-scope conversations. Validate it against human review on a sample of 300 conversations.
7. Add a randomised holdout or A/B for each release and report the interval. Use a calibrated LLM judge only after agreement with humans is measured (Cohen's kappa) and re-checked regularly.
8. Refresh the offline set every quarter with fresh sampled traffic and keep a locked set that is never used for tuning.

**Metrics:**
- Offline pass rate = questions passed / 1,000, per intent slice and re-weighted by traffic share.
- Online resolution rate = resolved in-scope conversations / in-scope conversations, with a user-clustered interval.
- Gap = offline gain minus online gain, with an interval.
- Judge-human agreement (kappa) and audit sample size.
- Guardrails: escalation rate, complaint rate, cost per resolution.

**Risks:**
- Chasing the offline score (Goodhart's law: a metric that becomes a target stops measuring what you wanted).
- A resolution metric that counts abandoned chats as resolved.
- Concluding the releases are useless when the online test was underpowered.
- Judge drift between releases.

**What the interviewer scores:**
- Strong: quantifies noise on both sides, reweights by traffic, names a first check, defines the online metric exactly.
- Strong: notes clustering and holdouts.
- Weak: "online is noisy, trust offline" or the reverse.
- Weak: a list of reasons with no first step.

**Example:** Illustrative. Weak: "Offline is up 4 points, so the model is better, the online number is noise." Strong: "Online noise alone allows up to about +1.5, so +4 is a real gap. I would reweight offline by live intent mix, because if hard questions are 10% of traffic an 8-point gain on them is only 0.8 overall. Then I would run a holdout on the next release."

**Code:**
```python
import math
def two_prop(p1, n1, p2, n2):
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = p2 - p1
    return d, se, d / se, d - 1.96 * se, d + 1.96 * se
d, se, z, lo, hi = two_prop(0.61, 20_000, 0.615, 20_000)
print(f"online: +{d*100:.1f} pts, SE {se*100:.2f}, z {z:.2f}, 95% CI {lo*100:.2f} to {hi*100:.2f} pts (assumes independent conversations)")
assert round(se * 100, 2) == 0.49 and round(z, 2) == 1.03 and (round(lo * 100, 2), round(hi * 100, 2)) == (-0.45, 1.45)
d2, se2, z2, lo2, hi2 = two_prop(0.82, 1000, 0.86, 1000)
print(f"offline (unpaired view): +{d2*100:.0f} pts, SE {se2*100:.2f}, z {z2:.2f}, 95% CI {lo2*100:.1f} to {hi2*100:.1f} pts")
assert round(z2, 2) == 2.44 and (round(lo2 * 100, 1), round(hi2 * 100, 1)) == (0.8, 7.2)
print(f"offline +4 sits above the online upper limit +{hi*100:.2f}: {0.04 > hi}")
assert 0.04 > hi
# Mix effect: offline set 50% hard / 50% easy, gain only on hard items (+8). Online traffic is 10% hard.
gain_hard = 8.0
off = 0.5 * gain_hard; on = 0.1 * gain_hard
print(f"mix effect: offline gain {off:.1f} pts, online gain {on:.1f} pts")
assert off == 4.0 and abs(on - 0.8) < 1e-9
# Clustering: conversations come from users; a design effect of 2 inflates the online SE by sqrt(2).
deff = 2.0
print(f"with design effect {deff:.0f}: online SE {se*math.sqrt(deff)*100:.2f} pts, CI upper {(d+1.96*se*math.sqrt(deff))*100:.2f}")
assert round(se * math.sqrt(deff) * 100, 2) == 0.69
# Online sample size to see +1 point at 60% (80% power, 5% two-sided).
n_arm = 2 * 0.6 * 0.4 * (1.96 + 0.84) ** 2 / 0.01 ** 2
print(f"conversations per arm to detect +1 point at 60%: {n_arm:,.0f}")
assert round(n_arm) == 37_632
```

**Output (my run):**
```
online: +0.5 pts, SE 0.49, z 1.03, 95% CI -0.45 to 1.45 pts (assumes independent conversations)
offline (unpaired view): +4 pts, SE 1.64, z 2.44, 95% CI 0.8 to 7.2 pts
offline +4 sits above the online upper limit +1.45: True
mix effect: offline gain 4.0 pts, online gain 0.8 pts
with design effect 2: online SE 0.69 pts, CI upper 1.85
conversations per arm to detect +1 point at 60%: 37,632
```

**Follow-ups:**
- Which do you trust more? Neither alone. Online measures what users experience; offline is fast and controlled. They must reconcile.
- How big an online test? About 37,600 per arm to see +1 point at 60% (80% power), and more if users repeat.
- Can an LLM judge be the online metric? Only after checking agreement with human labels and watching it for drift.

**Common mistakes:**
- Comparing offline and online without intervals.
- A test set that has been tuned against.
- Treating conversations as independent when users repeat.
- Changing the online metric definition between releases.

### Q19 ⭐⭐ 🟢 An invoice-extraction call at temperature 0.7 returns invalid JSON on 3% of 100,000 daily calls, and at temperature 0 it does so on 0.5%. Compute the daily invalid counts at each setting, and explain what else besides lowering temperature you would do to make outputs parse reliably and what lowering it costs.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to temperature and structured-output topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Temperature 0 cuts invalid JSON from 3,000 to 500 a day, but I would not stop there: I would use schema-constrained output where available, validate every response, and retry or repair the failures.

**Clarifying questions:**
- What does "invalid" mean: not parseable, or wrong schema, or wrong values? Why it matters: each has a different fix.
- What do the failures look like (truncation, chatty prefix, trailing comma)? Why it matters: truncation needs a larger token limit, not a lower temperature.
- Does the provider support structured or schema-constrained output? Why it matters: it can remove most parse failures (provider feature, check the current docs).
- What is a failure worth (a lost invoice, a delay)? Why it matters: sets how much retry cost is acceptable.
- Is extraction quality affected by temperature? Why it matters: the cost of lowering it must be measured.

**Approach:**
1. Counts: 3% of 100,000 = 3,000 a day at 0.7; 0.5% = 500 at 0. Difference 2,500 a day.
2. Read 100 failures and bucket them. Fix the cheap causes: cut the chatty preface, raise the token limit if outputs are cut off, simplify the schema.
3. Use schema-constrained or JSON mode if the API offers it, and add one or two examples to the prompt. This is editor knowledge about provider features; verify it for your model.
4. Always validate: parse, then check against the schema (required fields, types, ranges).
5. On failure, retry once with a repair prompt that includes the parser error. If failures are tied to the input, a same-settings retry repeats them; with fully correlated failures 500 a day stay 500. If independent, one retry leaves about 2.5 a day at temperature 0 (and about 90 at 0.7) for 0.5% (or 3%) extra calls.
6. Route what still fails to a fallback (a stronger model, or a human queue).
7. Measure field accuracy, not only parse rate. Valid JSON can hold wrong values.
8. Test the cost of lowering temperature: compare field accuracy at 0 and 0.7 on a labelled set before changing.

**Metrics:**
- Parse-failure rate = responses failing the parser / responses.
- Schema-failure rate = parsed responses failing schema checks / parsed responses.
- Field accuracy = fields correct / fields labelled, on a labelled sample.
- Retry rate and cost per successful extraction.
- Guardrails: field accuracy must not fall, p95 latency including retries.

**Risks:**
- Valid JSON with wrong content hides in the "success" count.
- Retries inflate cost and latency.
- Temperature 0 may reduce quality on ambiguous invoices, and is still not guaranteed identical across calls (Book 2 Part 02 Q21 covers why).
- Constrained decoding can force a valid but wrong answer.

**What the interviewer scores:**
- Strong: counts, root-cause buckets, validation plus retry, separate parse rate from correctness.
- Strong: says what lowering temperature costs and tests it.
- Weak: "set temperature to 0" and done.
- Weak: assumes retries are independent without saying so.

**Example:** Illustrative. Weak: "I would set temperature to zero." Strong: "That takes 3,000 failures to 500 a day. Then I would turn on schema-constrained output, validate with a schema, and retry once with the error message. I would also check field accuracy at both settings on 300 labelled invoices, because valid JSON can still have a wrong total."

**Code:**
```python
calls = 100_000
inv_hot, inv_cold = calls * 0.03, calls * 0.005
print(f"invalid per day: temp 0.7 -> {inv_hot:,.0f}; temp 0 -> {inv_cold:,.0f}; difference {inv_hot-inv_cold:,.0f}")
assert (round(inv_hot), round(inv_cold)) == (3000, 500)
# Validate-and-retry. Independent retry only if the failure is not tied to the input.
for rate, label in ((0.005, "temp 0"), (0.03, "temp 0.7")):
    after = calls * rate * rate
    extra = calls * rate
    print(f"{label}: one independent retry leaves ~{after:,.1f} invalid/day, adds {extra:,.0f} extra calls ({rate:.1%} more spend)")
assert round(calls * 0.005 ** 2, 1) == 2.5 and round(calls * 0.03 ** 2) == 90
# If failures repeat on the same input (fully correlated), a same-settings retry fixes nothing.
corr = 1.0
print(f"fully correlated failures: invalid after retry = {calls*0.005*corr:,.0f}/day at temp 0")
assert calls * 0.005 * corr == 500
# Valid JSON is not correct JSON: parse rate and field accuracy are different metrics.
parsed = calls * (1 - 0.005)
field_acc = 0.94
print(f"parsed {parsed:,.0f}; if 94% of parsed outputs have all fields right: {parsed*field_acc:,.0f} fully correct")
assert round(parsed * field_acc) == 93_530
import json
def ok(s):
    try: json.loads(s); return True
    except ValueError: return False
assert ok('{"total": 12.5}') and not ok('{"total": 12.5,}') and not ok('Here is the JSON: {"total": 12.5}')
print("trailing comma and chatty prefix both fail json.loads: checked")
```

**Output (my run):**
```
invalid per day: temp 0.7 -> 3,000; temp 0 -> 500; difference 2,500
temp 0: one independent retry leaves ~2.5 invalid/day, adds 500 extra calls (0.5% more spend)
temp 0.7: one independent retry leaves ~90.0 invalid/day, adds 3,000 extra calls (3.0% more spend)
fully correlated failures: invalid after retry = 500/day at temp 0
parsed 99,500; if 94% of parsed outputs have all fields right: 93,530 fully correct
trailing comma and chatty prefix both fail json.loads: checked
```

**Follow-ups:**
- What does lowering temperature cost? Less variety, usually little loss for extraction; verify with field accuracy, and some tasks do worse with greedy output.
- Why not retry forever? Cost, latency, and correlated failures; cap at one or two retries then fall back.
- How do you spot truncation? Check the stop reason or a missing closing brace and compare against the token limit.

**Common mistakes:**
- Equating valid JSON with a correct extraction.
- Assuming temperature 0 means no failures or identical outputs.
- Retrying with identical settings on input-driven failures.
- Skipping a labelled check after changing a setting.

### Q20 ⭐⭐ 🟢 Before switching models you plan to shadow 10% of 700,000 weekly calls on the candidate at an illustrative 0.0153 per call, while the old model still answers users. Compute the weekly shadow cost, and say what you can and cannot learn from shadow traffic compared with an A/B test.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to rollout and shadow-traffic topics in LLMOps material; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Shadowing 10% costs about 1,071 a week (70,000 calls x 0.0153) and tells me how the candidate behaves on real inputs, but not how users react, so it is a filter before an A/B test, not a replacement.

**Clarifying questions:**
- Is the 0.0153 per call the candidate's real average cost? Why it matters: cost scales with output length, which can differ between models.
- Does the candidate call tools or write anywhere? Why it matters: shadow calls must never take real actions.
- Is the 10% random or stratified by intent? Why it matters: rare intents may be missed.
- What decision follows (go to a 5% canary, or full switch)? Why it matters: sets what evidence is needed.
- Can we log user data for the shadow outputs? Why it matters: privacy and retention apply to shadow logs too.

**Approach:**
1. Cost: 700,000 x 10% = 70,000 calls x 0.0153 = 1,071 a week; the full-traffic equivalent is 10,710.
2. Sample randomly, plus enough of each rare intent. Never let shadow outputs reach users or trigger actions.
3. Compare per call with the old model: format validity, length, latency, token cost, refusal rate, and disagreement.
4. Review the disagreements. If 12% disagree (invented), that is 8,400 pairs; read a random 400 and note the margin is about plus or minus 4.9 points.
5. Use shadow for rare failures too. Zero failures in 70,000 calls bounds the failure rate near 0.0043% at 95%.
6. What shadow cannot show: whether users are happier, resolve more, or come back. Users never saw the candidate's answer, and in multi-turn chats the conversation continues from the old model's replies, so later turns are not what the candidate would have faced.
7. Next step: a small live canary or A/B. To see +1 point on a 60% resolution rate you need about 37,600 conversations per arm.

**Metrics:**
- Shadow cost = shadowed calls x cost per call.
- Disagreement rate = calls where the models' answers differ materially / shadowed calls.
- Candidate win rate on disagreements = candidate better / reviewed disagreements, with an interval.
- Parse-failure rate and latency p95 for the candidate.
- Guardrails: shadow adds no user-visible latency, rate limits not hit.

**Risks:**
- Shadow calls slow the main path or hit rate limits.
- Shadow tool calls cause real side effects.
- Judging with a judge that favours its own family.
- Treating "looks fine on shadow" as proof of better user outcomes.

**What the interviewer scores:**
- Strong: correct cost, clear can and cannot list, next step to A/B with a sample size.
- Strong: side-effect and multi-turn caveats.
- Weak: "shadow is as good as an A/B test".
- Weak: no cost or sample numbers.

**Example:** Illustrative. Weak: "Shadow looked good so switch." Strong: "Shadow showed the candidate parses 99.5%, is 12% different, and wins 58% of 400 reviewed disagreements, which is not decisive at plus or minus 4.9 points. It cost 1,071 for the week. I would go to a 5% canary and watch resolution and escalation."

**Code:**
```python
import math
weekly, share, price = 700_000, 0.10, 0.0153
shadow = weekly * share
cost = shadow * price
print(f"shadow calls {shadow:,.0f}; weekly cost {cost:,.0f}; full-traffic equivalent {weekly*price:,.0f}")
assert shadow == 70_000 and round(cost) == 1071 and round(weekly * price) == 10_710
rule3 = 3 / shadow
print(f"0 failures in {shadow:,.0f} shadow calls -> 95% upper bound ~{rule3:.4%} per call (rule of three)")
assert round(rule3 * 100, 4) == 0.0043
# What an A/B test needs to see a 1-point change in a 60% resolution rate (80% power, 5% two-sided).
za, zb = 1.96, 0.84
p = 0.60
n_arm = 2 * p * (1 - p) * (za + zb) ** 2 / 0.01 ** 2
print(f"A/B needs ~{n_arm:,.0f} conversations per arm for +1 point at 60%")
assert round(n_arm) == 37_632
# Disagreement review: if models differ on 12% of shadow calls, how many are there to read?
dis = shadow * 0.12
print(f"if 12% disagree: {dis:,.0f} pairs; reviewing a random 400 gives a margin of about +-{1.96*math.sqrt(0.25/400)*100:.1f} pts on 'candidate better'")
assert dis == 8400 and round(1.96 * math.sqrt(0.25 / 400) * 100, 1) == 4.9
```

**Output (my run):**
```
shadow calls 70,000; weekly cost 1,071; full-traffic equivalent 10,710
0 failures in 70,000 shadow calls -> 95% upper bound ~0.0043% per call (rule of three)
A/B needs ~37,632 conversations per arm for +1 point at 60%
if 12% disagree: 8,400 pairs; reviewing a random 400 gives a margin of about +-4.9 pts on 'candidate better'
```

**Follow-ups:**
- Why not skip shadow? It is cheap protection against format and latency surprises before users see anything.
- Shadow or canary first? Shadow first for safety, then canary for outcomes.
- How long to shadow? Long enough to cover weekly cycles and rare intents; a week is a starting point.

**Common mistakes:**
- Letting shadow outputs have side effects.
- Using shadow to claim user satisfaction.
- Skipping rare-intent coverage.
- Forgetting shadow logs are data too.

### Q21 ⭐⭐ 🟢 A ticket classifier uses a large model at 0.004 per call for 5,000,000 calls a month. A fine-tuned small model would cost 0.0005 per call after a one-off 13,000 for labels and training (all illustrative), and scored 2 points lower in absolute accuracy on a 500-ticket test set. Compute the monthly saving and payback in months, and say what accuracy trade you would need agreed.
**Asked at:** GenAI and LLM-engineer interview guides (InterviewBit, Hyring, Let's Code, recrew, Pensero and Towards AI 2026 pages list RAG, hallucination mitigation, evaluation and cost or latency topics; one guide reports a prompt about a RAG answer that is wrong although the right document exists, and another a smaller-model-for-narrow-tasks answer pattern); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The fine-tuned small model saves 17,500 a month and pays back in about 0.74 months, but I would only switch after agreeing what the 2-point accuracy drop is worth, since 2 points is 100,000 extra errors a month.

**Clarifying questions:**
- What is the baseline accuracy, and is the 2-point drop measured on the same 500 tickets for both models? Why it matters: paired data is much tighter than two separate samples.
- What does a misclassified ticket cost (delay, rework)? Why it matters: sets the break-even.
- Are errors uniform, or concentrated on important ticket types? Why it matters: an average hides a bad slice.
- What ongoing costs are missing (re-labelling, retraining, hosting, monitoring)? Why it matters: the 13,000 is one-off only.
- Can the small model say when it is unsure? Why it matters: enables a cascade.

**Approach:**
1. Costs per month: large 5,000,000 x 0.004 = 20,000; small 5,000,000 x 0.0005 = 2,500. Saving 17,500.
2. Payback: 13,000 / 17,500 = 0.74 months, about 22 days.
3. Error price: 2 points x 5,000,000 = 100,000 extra errors a month. Break-even = 17,500 / 100,000 = 0.175 per extra error, which is 43.75x the cost of a large-model call. If a wrong routing costs more than 0.175, the switch loses money.
4. Is the 2 points even real? If accuracy were 92% and 90% (invented), the unpaired interval for the gap is about -5.5 to +1.5 points. 500 tickets is too small to decide; do a paired test on the same tickets and read the disagreements.
5. Check slices: urgent, high-value, rare categories.
6. Consider a cascade: the small model answers confident tickets, the rest go to the large one. With 20% escalated the monthly cost is 6,500 and the saving 13,500.
7. Agree a written trade: for example accuracy no more than 1 point below the large model overall and no loss on urgent tickets, with a rollback if the monthly audit breaks it.
8. Add the ongoing costs and re-run the payback.

**Metrics:**
- Monthly cost = calls x cost per call.
- Payback (months) = one-off cost / monthly saving.
- Accuracy = correct tickets / graded tickets, per slice, paired difference with an interval.
- Cost per correct ticket = monthly cost / correct tickets.
- Guardrails: urgent-ticket recall, escalation rate, audit accuracy each month.

**Risks:**
- A small average drop hides a large drop on a critical class.
- Distribution drift hits the small model faster.
- Hidden ongoing labelling and retraining costs.
- Treating an unresolved 2 points as "about the same".

**What the interviewer scores:**
- Strong: both numbers, break-even cost per error, and a paired test.
- Strong: proposes a cascade and a written accuracy agreement.
- Weak: "saves 17,500, switch now".
- Weak: ignores slices and upkeep.

**Example:** Illustrative. Weak: "It is only 2 points worse and 8 times cheaper, switch." Strong: "It saves 17,500 a month and pays back in under a month. But 2 points is 100,000 extra errors, so the switch only works if an error costs under 0.175. I would run a paired test on the same tickets, check urgent tickets separately, and escalate low-confidence ones to the big model."

**Code:**
```python
import math
calls = 5_000_000
big, small, one_off = 0.004, 0.0005, 13_000
mb, ms = calls * big, calls * small
saving = mb - ms
payback = one_off / saving
print(f"monthly: large {mb:,.0f}, small {ms:,.0f}, saving {saving:,.0f}; payback {payback:.2f} months (~{payback*30:.0f} days)")
assert (mb, ms, saving) == (20_000, 2_500, 17_500) and round(payback, 2) == 0.74
extra_err = calls * 0.02
be = saving / extra_err
print(f"2 points = {extra_err:,.0f} extra errors a month; break-even cost per extra error = {be:.3f} = {be/big:.2f}x the large call")
assert round(extra_err) == 100_000 and round(be, 3) == 0.175 and round(be / big, 2) == 43.75
# Test-set noise: assume large model 92% and small 90% on the same 500 tickets (invented).
n = 500
p1, p2 = 0.92, 0.90
se = math.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
print(f"unpaired SE {se*100:.2f} pts; CI of the -2 pt gap {(-0.02-1.96*se)*100:.1f} to {(-0.02+1.96*se)*100:.1f} pts")
assert round(se * 100, 2) == 1.81 and round((-0.02 - 1.96 * se) * 100, 1) == -5.5 and round((-0.02 + 1.96 * se) * 100, 1) == 1.5
# Cascade: small model answers, a fraction escalates to the large model.
for esc in (0.0, 0.2, 0.4):
    c = calls * small + esc * calls * big
    print(f"escalate {esc:.0%}: monthly {c:,.0f}, saving {mb-c:,.0f}")
assert calls * small + 0.2 * calls * big == 6_500
```

**Output (my run):**
```
monthly: large 20,000, small 2,500, saving 17,500; payback 0.74 months (~22 days)
2 points = 100,000 extra errors a month; break-even cost per extra error = 0.175 = 43.75x the large call
unpaired SE 1.81 pts; CI of the -2 pt gap -5.5 to 1.5 pts
escalate 0%: monthly 2,500, saving 17,500
escalate 20%: monthly 6,500, saving 13,500
escalate 40%: monthly 10,500, saving 9,500
```

**Follow-ups:**
- What if the 2 points is within noise? Collect more labelled tickets and run a paired test; do not call it safe or unsafe yet.
- Why a cascade? It keeps most of the saving and sends the hard tickets to the stronger model.
- When would you not switch? If errors are costly, the data drifts fast, or the upkeep cost removes the saving.

**Common mistakes:**
- Ignoring ongoing costs.
- Unpaired comparison on a small set.
- Averaging over slices.
- No rollback rule.

### Q22 ⭐⭐ 🟢 A request has a 4,000-token fixed prefix and 500 variable tokens at an illustrative 3 per million input tokens, with cached prefix tokens billed at 10% of that rate, over 1,000,000 calls a month. Compute the monthly input cost with no caching and with a 60% cache hit rate on the prefix, and say how you would restructure prompts to raise the hit rate.
**Asked at:** LLM cost and routing pages (getmaxim cost and semantic-cache guides, tianpan and system-design.space pages on routing and cascades, a Towards Data Science article on saving tokens in agentic AI, a Towards AI piece on AI system-design interview patterns); practitioner material, no confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Without caching the input costs 13,500 a month; with a 60% hit rate on the prefix it costs 7,020, a saving of 48%, and I would raise the hit rate by keeping the prefix identical and putting anything that changes at the end.

**Clarifying questions:**
- How does the provider define a cache hit (exact leading tokens, minimum length, time to live)? Why it matters: the details differ by provider and I would read the current docs.
- Is there a write premium on a cache miss? Why it matters: it changes the saving.
- How much time passes between calls? Why it matters: a cache entry that expires between calls never hits.
- What is in the prefix today (timestamps, user names, tool lists in changing order)? Why it matters: any change breaks the match.
- Are the 500 variable tokens really the only variable part? Why it matters: sets the maximum hit rate.

**Approach:**
1. No cache: (4,000 + 500) x 1,000,000 = 4.5 billion tokens x 3 per million = 13,500.
2. 60% hit rate on the prefix: hits 4,000 x 1,000,000 x 60% = 2.4 billion tokens at 0.3 per million = 720; misses 1.6 billion at 3 = 4,800; variable 500 million at 3 = 1,500. Total 7,020. Saving 6,480, which is 48.0%.
3. The ceiling: even at 100% hit the cost is 2,700, an 80% saving, because the 500 variable tokens are never cached.
4. Sensitivity: if misses carried an invented 1.25x write premium, the 60% case costs 8,220 (39.1% saving). Check the real terms before trusting any number.
5. Restructure for hits: static content first (system instructions, rules, fixed examples, tool definitions in a fixed order), then slowly changing context, then the user's message last. Never put timestamps, request IDs, or user names near the top.
6. Keep the prefix byte-identical: same whitespace, same ordering, same serialisation. Version prompts deliberately and ship edits in batches, not hourly.
7. Keep traffic warm enough that entries do not expire; consider grouping similar requests.
8. Track hit rate from the provider's usage fields and alert on drops after a deploy.

**Metrics:**
- Prefix hit rate = cached prefix tokens read / total prefix tokens sent.
- Effective input price = monthly input cost / input tokens sent.
- Monthly input cost = uncached tokens x price + cached tokens x price x 0.10 (+ any write premium).
- Guardrails: answer quality unchanged after reordering the prompt, p95 latency.

**Risks:**
- Reordering the prompt changes behaviour; test quality after the change.
- A hidden changing element (a date in the system prompt) drops the hit rate to near zero.
- Assuming a discount applies to all input tokens.
- Provider terms change; hard-coding assumptions.

**What the interviewer scores:**
- Strong: both costs correct, only the prefix is discounted, names the ceiling, gives concrete prompt layout rules.
- Strong: says to verify provider terms and measure the hit rate.
- Weak: applies the 10% rate to the whole prompt.
- Weak: vague "optimise the prompt".

**Example:** Illustrative. Weak: "Cache the prompt and the cost drops 90%." Strong: "Only the 4,000-token prefix is cached, so at 60% hits the bill goes from 13,500 to 7,020, and even at 100% it is 2,700. I would move the date and user name to the end of the prompt, because with the timestamp first the shared prefix was 0 tokens and with it last it was 15 of 17 in my test."

**Code:**
```python
calls = 1_000_000
prefix, var, price, disc = 4_000, 500, 3.0, 0.10         # illustrative price per million input tokens
per_m = lambda tok: tok * calls * price / 1e6
no_cache = per_m(prefix + var)
def with_hit(h, write_mult=1.0):
    hit = per_m(prefix) * h * disc
    miss = per_m(prefix) * (1 - h) * write_mult
    return hit + miss + per_m(var)
c60 = with_hit(0.6)
print(f"no cache {no_cache:,.0f}; 60% hit {c60:,.0f}; saving {no_cache-c60:,.0f} = {(no_cache-c60)/no_cache:.1%}")
assert no_cache == 13_500 and round(c60) == 7_020 and round((no_cache - c60) / no_cache, 3) == 0.48
for h in (0.0, 0.3, 0.6, 0.9, 1.0):
    print(f"hit rate {h:.0%}: {with_hit(h):,.0f}")
assert round(with_hit(1.0)) == 2_700 and round((no_cache - with_hit(1.0)) / no_cache, 2) == 0.80
c60w = with_hit(0.6, 1.25)
print(f"if misses carried an invented 1.25x write premium: 60% hit {c60w:,.0f}, saving {(no_cache-c60w)/no_cache:.1%}")
assert round(c60w) == 8_220 and round((no_cache - c60w) / no_cache, 3) == 0.391
# Prompt layout: only an identical leading run of tokens can hit.
def shared_prefix(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y: break
        n += 1
    return n
sys_p = ["SYS"] * 10 + ["RULES"] * 5
bad_a = ["t=10:01"] + sys_p + ["Q:refund"]; bad_b = ["t=10:02"] + sys_p + ["Q:order"]
good_a = sys_p + ["t=10:01", "Q:refund"]; good_b = sys_p + ["t=10:02", "Q:order"]
print("timestamp first -> shared prefix", shared_prefix(bad_a, bad_b), "of", len(bad_a), "| timestamp last ->", shared_prefix(good_a, good_b), "of", len(good_a))
assert shared_prefix(bad_a, bad_b) == 0 and shared_prefix(good_a, good_b) == 15
```

**Output (my run):**
```
no cache 13,500; 60% hit 7,020; saving 6,480 = 48.0%
hit rate 0%: 13,500
hit rate 30%: 10,260
hit rate 60%: 7,020
hit rate 90%: 3,780
hit rate 100%: 2,700
if misses carried an invented 1.25x write premium: 60% hit 8,220, saving 39.1%
timestamp first -> shared prefix 0 of 17 | timestamp last -> 15 of 17
```

**Follow-ups:**
- How is this related to the KV cache? Prefix caching reuses stored attention state for the shared leading tokens; see Book 2 Part 01 Q24 ("What are prompt/prefix caching in LLM APIs, and how do they relate to the KV cache? How do you structure prompts to benefit?").
- What if the prefix is under the provider's minimum length? Then nothing is cached; check the minimum in the docs (editor knowledge, not tested here).
- Is a higher hit rate always better? Yes for cost, but only if quality and latency stay the same.

**Common mistakes:**
- Discounting the variable part.
- Putting dynamic text first.
- Not measuring the real hit rate.
- Ignoring write premiums or expiry.

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

### Q34 ⭐⭐ 🟡 A router sends 70% of 100,000 daily queries to a small model at 0.002 per call and the rest to a large model at 0.012. The small model passes 90% of its routed queries, and the large model would have passed 94% of those same queries. Compute daily cost against sending everything to the large model, and the extra failures per day caused by routing, and say how you would validate the router.
**Asked at:** LLM cost and routing pages (getmaxim cost and semantic-cache guides, tianpan and system-design.space pages on routing and cascades, a Towards Data Science article on saving tokens in agentic AI, a Towards AI piece on AI system-design interview patterns); practitioner material, no confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The router costs 500 a day against 1,200 for all-large (saves 700, 58%), but it adds 2,800 extra failures a day, so it only pays if one failure costs the business less than 0.25 (illustrative), and I would prove that on labelled, paired data before trusting it.

**Clarifying questions:**
- What counts as a "pass", and who labels it (human, rubric, LLM judge)? The 90% and 94% mean nothing without one definition shared by both models.
- Is the 94% measured on the 70% the router picked, or on all traffic? The prompt says "those same queries", so I read it as the routed slice. The router picks easier queries, so the large model's 94% on that slice is not its pass rate overall.
- What does a failure cost: a retry, a human hand-off, a refund, a lost user? That one number decides whether 700 saved is worth 2,800 failures.
- Are costs per call fixed, or do they depend on tokens? The prompt gives flat prices per call. Real prices depend on token counts (illustrative, not vendor prices).
- Can a failed small-model answer be detected and escalated (a cascade) instead of accepted? That changes the design a lot.

**Approach:**
1. Do the arithmetic first. Small: 70,000 x 0.002 = 140. Large: 30,000 x 0.012 = 360. Total 500. All-large: 100,000 x 0.012 = 1,200. Saving 700 a day (58.3%).
2. Failures on the routed slice: small fails 10% of 70,000 = 7,000. Large would fail 6% = 4,200. Extra failures from routing: 2,800 a day, 4 points on the routed slice and 2.8% of all traffic.
3. Price the trade: 700 / 2,800 = 0.25 saved per extra failure. If a failure costs more than 0.25 (a retry, a hand-off) the router loses money. Note the small model is only 0.010 cheaper per call than the large one, so a 4-point pass gap already costs 4% x (a failure's cost) per call. Break-even per call: failure cost x 0.04 = 0.010, so failure cost = 0.25. Same answer, good check.
4. Validate the router on labelled data: sample traffic, run both models on the same queries, label both answers (paired), and report pass rate by router bucket and by query type. Use enough labels: 500 labelled answers give a 95% interval of about 87% to 92% for a 90% pass rate (see Code), so 500 cannot even confirm a 4-point gap on its own. Use paired comparison, which has much less noise.
5. Look for where the router is wrong: queries sent small that large would pass and small fails (the costly cell), and queries sent large that small would also pass (wasted money).
6. Roll out with a shadow or a small canary, a quality guardrail with an automatic fallback to all-large, and a weekly re-audit (traffic changes).
7. Consider a cascade (small first, escalate on low confidence) if confidence is trustworthy. That recovers some of the 2,800 failures at the cost of extra latency (see Q35).

**Metrics:**
- Cost per day = sum over routes of (queries routed x price per call). Saving = all-large cost minus router cost.
- Extra failures = routed queries x (large pass rate minus small pass rate), on the same queries.
- Cost per extra failure avoided = saving / extra failures (here 0.25), compared with the business cost of one failure.
- Router accuracy: of queries where the small model would fail but large would pass (the "hard" ones), the share the router sent large; and the reverse for waste.
- Guardrails: pass rate by segment (language, intent), p95 latency, escalation rate.

**Risks:**
- Averages hide segments: the small model may fail 30% on one intent and 2% on others.
- The 94% on the routed slice is not the large model's rate on the other 30%; do not extrapolate.
- Router drift: traffic mix changes and the 70% quietly moves.
- Labels from an LLM judge may favour the bigger model's style (verbosity bias).
- Optimising cost per call instead of cost per resolved task (a failed answer causes a retry, which costs again).

**What the interviewer scores:**
- Strong: gets 500 versus 1,200 and 2,800 extra failures right, and converts them into a break-even failure cost. Weak: stops at "saves 58%".
- Strong: asks for a paired, labelled validation and a sample size. Weak: "I would check accuracy" with no method.
- Strong: notes that the 94% is measured on the routed slice only. Weak: applies 94% to all traffic.
- Strong: proposes guardrail and fallback in rollout. Weak: ships router to 100%.

**Example:** (illustrative numbers) A failure that needs a human hand-off costs 4.00. Then 2,800 extra failures cost 11,200 a day against 700 saved: the router is a bad deal. If a failure only triggers a free retry costing 0.012, the router is a great deal. Weak answer: "58% cheaper, ship it." Strong answer: "Routing saves 700 a day and costs 2,800 extra failures a day, so each failure must cost under 0.25 for it to pay. For hand-off failures it does not, so I would route only the intents where the small model matches the large one, and cascade the rest."

**Code:**
```python
import math

# Illustrative numbers from the prompt (not vendor prices)
N = 100_000
share_small = 0.70
c_small, c_large = 0.002, 0.012
pass_small, pass_large_same = 0.90, 0.94

n_small = round(N * share_small)
n_large = N - n_small
cost_router = n_small * c_small + n_large * c_large
cost_all_large = N * c_large
saving = cost_all_large - cost_router
print(f"routed to small: {n_small}, to large: {n_large}")
print(f"router cost/day: {cost_router:.1f}; all-large cost/day: {cost_all_large:.1f}; saving: {saving:.1f} ({saving/cost_all_large:.1%})")
assert n_small == 70_000 and n_large == 30_000
assert round(cost_router, 6) == 500.0 and round(cost_all_large, 6) == 1200.0 and round(saving, 6) == 700.0

fail_small = n_small * (1 - pass_small)
fail_large_same = n_small * (1 - pass_large_same)
extra = fail_small - fail_large_same
print(f"failures on routed slice: small {fail_small:.0f} vs large {fail_large_same:.0f}; extra per day: {extra:.0f} ({extra/N:.1%} of all traffic)")
assert round(fail_small) == 7000 and round(fail_large_same) == 4200 and round(extra) == 2800

# What a failure must cost for the router to stop paying off
be = saving / extra
print(f"break-even cost per extra failure: {be:.2f} (saving {saving:.0f} / extra failures {extra:.0f})")
assert round(be, 2) == 0.25

# Precision of a labelled audit of the small model's routed traffic (Wilson 95%)
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
lo, hi = wilson(450, 500)
print(f"audit 450/500 passed -> Wilson 95% [{lo:.3f}, {hi:.3f}]")
assert 0.87 < lo < 0.88 and 0.92 < hi < 0.93   # +/- about 3 points, too wide to confirm a 4-point gap alone
```

**Output (my run):**
```text
routed to small: 70000, to large: 30000
router cost/day: 500.0; all-large cost/day: 1200.0; saving: 700.0 (58.3%)
failures on routed slice: small 7000 vs large 4200; extra per day: 2800 (2.8% of all traffic)
break-even cost per extra failure: 0.25 (saving 700 / extra failures 2800)
audit 450/500 passed -> Wilson 95% [0.871, 0.923]
```

**Follow-ups:**
- Which queries would you send to the small model first? Short, structured, low-risk intents (classification, extraction, FAQ) where an audit shows the small model within about a point of the large one. Keep high-stakes and long-reasoning intents on large.
- How would the router itself be built? Start with rules on intent, then a small classifier trained on the paired labels. Its own cost and latency must be counted.
- Is this the same as a cascade? No. A router decides before calling; a cascade calls small first and escalates (latency in Q35).

**Common mistakes:**
- Reporting the saving without the failure cost.
- Using the large model's accuracy on easy routed queries as its overall accuracy.
- Validating with unpaired or tiny samples, and with a judge that has never been checked against humans.
- Forgetting the cost of the router and of retries.

### Q35 ⭐⭐ 🟡 A cascade tries a small model first (0.8 seconds) and escalates to a large model (2.5 seconds) when confidence is low, and 60% of requests are accepted by the small model. Compute the mean latency of the cascade against always calling the large model, and the latency of an escalated request against a 3.0-second p95 budget, and say what that implies for the p95.
**Asked at:** LLM cost and routing pages (getmaxim cost and semantic-cache guides, tianpan and system-design.space pages on routing and cascades, a Towards Data Science article on saving tokens in agentic AI, a Towards AI piece on AI system-design interview patterns); practitioner material, no confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The cascade is faster on average (1.8 s against 2.5 s) but an escalated request takes 3.3 s, over the 3.0 s budget, and because 40% escalate, the p95 is about 3.3 s or worse: the mean improves while the tail breaks.

**Clarifying questions:**
- Is the 3.0 s budget on p95 of end-to-end latency, and measured from the user's click? The budget is on the tail, so the mean tells me little.
- Does the small model's confidence arrive only after its full answer (0.8 s), or earlier? Early exit changes the escalated path.
- Are the 0.8 s and 2.5 s medians or fixed? Real latencies vary, which pushes p95 higher.
- Does the large call start only after the small one ends (serial)? Parallel start changes both latency and cost.
- Is the answer streamed? If the user can see the small answer early, the perceived latency differs (see Q38 for a streaming trade-off).

**Approach:**
1. Mean cascade = 0.6 x 0.8 + 0.4 x (0.8 + 2.5) = 0.48 + 1.32 = 1.80 s. Always-large = 2.50 s. Mean saving 0.70 s (28%).
2. Escalated request = 0.8 + 2.5 = 3.3 s, which is 0.3 s over the 3.0 s budget. The small call is wasted time on those requests.
3. p95: 40% of requests are escalated, and 40% is far more than 5%, so the 95th percentile falls inside the escalated group. With fixed latencies p95 = 3.3 s. Always-large has p95 near 2.5 s (fixed) so on the tail, the cascade is worse than not cascading. With noise (seeded simulation, invented sigma) both exceed 3.0 s, and the cascade is worse still.
4. To protect the p95 there are three options: cut escalation under 5% (so the tail is the small model); speed up the escalated path (parallel call, smaller large model, shorter output); or loosen what the budget measures (stream the small model's answer, or a higher-latency tier for hard queries).
5. Parallel speculative variant: start both at once. Mean = 0.6 x 0.8 + 0.4 x 2.5 = 1.48 s, escalated 2.5 s. It meets the budget, but you pay for the large call on 100% of requests, so the cost saving is gone. State that trade.
6. Decide with the product: p95 under budget costs money or quality.

**Metrics:**
- Mean latency = sum over paths of (share x path latency). p95 and p99 latency measured end to end per request.
- Escalation rate = escalated requests / all requests (here 40%).
- Share of requests over budget = requests slower than 3.0 s / all requests (here 40% with fixed latencies).
- Guardrails: quality of accepted small answers (a bad accept is a silent failure), cost per request.

**Risks:**
- Quoting only the mean to a stakeholder who cares about the tail.
- Confidence thresholds drift: the escalation rate may move from 40% to 60%.
- Serial cascades add the small model's time to every hard request, so the hardest requests are slowest.
- Cost: escalated requests pay for both calls.

**What the interviewer scores:**
- Strong: computes 1.8 s, 3.3 s, and says "40% over budget, so p95 is 3.3 or worse". Weak: "mean is better, so it meets the budget".
- Strong: knows why the 5% rule matters for p95 (the tail percentile needs under 5% slow requests). Weak: averages percentiles.
- Strong: offers parallel, escalation-rate and streaming options with their cost. Weak: only "make the model faster".
- Strong: asks which latency the user feels (first token versus last). Weak: none.

**Example:** (illustrative numbers) 100 requests: 60 take 0.8 s, 40 take 3.3 s. Mean is (48 + 132) / 100 = 1.8 s. Sorted, the 95th request is 3.3 s, over the budget. Weak answer: "The mean is 1.8 s, well under 3.0 s, so we are fine." Strong answer: "Mean is 1.8 but 40 of 100 requests take 3.3 s, so p95 is 3.3 and the budget is broken. I would raise the accept rate above 95%, run the large call in parallel for risky queries, or stream."

**Code:**
```python
import numpy as np

# Illustrative numbers from the prompt
t_small, t_large, accept, budget = 0.8, 2.5, 0.60, 3.0
esc = 1 - accept

mean_cascade = accept * t_small + esc * (t_small + t_large)   # escalated pay both calls in series
print(f"mean cascade {mean_cascade:.2f} s vs always-large {t_large:.2f} s")
assert round(mean_cascade, 2) == 1.80 and round(mean_cascade - t_large, 2) == -0.70

t_esc = t_small + t_large
print(f"escalated request {t_esc:.2f} s vs budget {budget:.1f} s -> over by {t_esc - budget:.2f} s")
assert round(t_esc, 2) == 3.30 and t_esc > budget

# p95 with fixed latencies: 40% of requests take 3.3 s, so the 95th percentile sits in that group
lat = np.array([t_small] * 60 + [t_esc] * 40)
p95 = np.percentile(lat, 95)
print("p95 of cascade with fixed latencies:", round(p95, 2), "| always-large p95:", t_large)
assert round(p95, 2) == 3.30
# How rare must escalation be for the p95 to stay at 0.8 s?
print("escalation rate must be at most 5% for p95 = small-model latency")

# Same with noise (seeded, lognormal sigma 0.25 around each mean): cascade p95 is above 3.3 and above always-large
rng = np.random.default_rng(7)
n = 200_000
def ln(mu, size): return mu * rng.lognormal(-0.25**2 / 2, 0.25, size)
is_esc = rng.random(n) < esc
sim = ln(t_small, n) + np.where(is_esc, ln(t_large, n), 0.0)
sim_large = ln(t_large, n)
print(f"simulated: cascade mean {sim.mean():.2f}, p95 {np.percentile(sim, 95):.2f}; always-large mean {sim_large.mean():.2f}, p95 {np.percentile(sim_large, 95):.2f}")
assert np.percentile(sim, 95) > np.percentile(sim_large, 95) > budget   # with noise both break 3.0, the cascade more

# Speculative parallel variant: fire both at once, use small if accepted, else wait for large
par = accept * t_small + esc * t_large
print(f"parallel variant: mean {par:.2f} s, escalated latency {t_large:.2f} s (but you pay for large on 100% of requests)")
assert round(par, 2) == 1.48
```

**Output (my run):**
```text
mean cascade 1.80 s vs always-large 2.50 s
escalated request 3.30 s vs budget 3.0 s -> over by 0.30 s
p95 of cascade with fixed latencies: 3.3 | always-large p95: 2.5
escalation rate must be at most 5% for p95 = small-model latency
simulated: cascade mean 1.80, p95 4.07; always-large mean 2.50, p95 3.65
parallel variant: mean 1.48 s, escalated latency 2.50 s (but you pay for large on 100% of requests)
```

**Follow-ups:**
- What accept rate gives a p95 under 3.0 s? About 95% or more (escalation at most 5%), with fixed latencies. At 0.8 s the small model then sets the tail. Check with real latency variation.
- Is it fair that always-large also fails the budget in the noisy run? Yes: the noise (invented) puts its p95 at 3.65 s. The point is the cascade makes the tail worse, not that large is safe.
- What about cost? The cascade's cost per request adds 0.4 of a small call to the large call it already makes, so if the small model is cheap the cascade still saves on the 60%.

**Common mistakes:**
- Comparing means and ignoring the p95.
- Forgetting that an escalated request pays for both calls in time.
- Averaging p95 values across paths.
- Treating the fixed 0.8 and 2.5 s as exact in production.

### Q36 ⭐⭐ 🟡 A retrieval system answers Hindi queries, and recall at 5 is 160 of 200 Devanagari-script queries (80%) but 104 of 200 romanised queries (52%). Compute the absolute and relative gap, and say how you would diagnose and close it without hurting the Devanagari queries.
**Asked at:** Indic-language and tokenizer material (an ACL Anthology LoResLM 2026 paper on informal and romanised Hindi tokenization, an arXiv study of tokenizer efficiency across the 22 official Indian languages, a HackerNoon opinion piece on the cost of building AI for Indian languages); research and commentary pages rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The gap is 28 points absolute (80% against 52%) and 35% relative, far beyond noise at 200 queries each, so I would diagnose where romanised text breaks (tokenisation, embeddings, spelling variants) and fix it with script normalisation and hybrid retrieval, gated by a Devanagari non-regression test.

**Clarifying questions:**
- What share of live traffic is romanised? A 28-point gap on 5% of traffic and on 60% of traffic are different priorities.
- Are the documents in Devanagari, romanised or mixed? If documents are Devanagari and queries are romanised, the problem is a cross-script match.
- How were the 200 queries in each group chosen? If the romanised ones are harder topics, part of the gap is not about script. Ideally the same intents in both scripts.
- Which embedding model and tokenizer are used? A model with weak romanised-Hindi coverage splits words into many odd pieces (see Book 2 Part 02, Q17 on the token tax).
- What is "recall at 5" here: the right document in the top 5 retrieved? One definition for both groups.

**Approach:**
1. Compute the gap and its noise: 80% - 52% = 28 points; relative drop 28/80 = 35%; romanised recall is 65% of Devanagari. Wilson 95% intervals are about 74-85% and 45-59%, which do not overlap (z about 5.9 unpaired). It is real, not noise.
2. Make the comparison fair: take the same intents in both scripts (paired queries) so the gap is about script and not topic.
3. Locate the stage that fails. Inspect 50 romanised misses: does the query embedding land near the right chunk (embedding problem), does lexical search find it (spelling variants problem), is the right chunk missing from the index (corpus problem)?
4. Fix options, cheapest first: (a) normalise script at query time (transliterate romanised Hindi into Devanagari before embedding, or the other way, behind a language and script detector); (b) hybrid retrieval, adding character n-gram lexical search, which catches near spellings (the toy example in Code); (c) add a query-rewrite step with an LLM that standardises spelling; (d) a multilingual embedding model with better romanised coverage, or fine-tune on romanised pairs.
5. Do not harm Devanagari: route by script detection, keep the Devanagari path unchanged, and run both test sets on every change with a non-regression rule (for example, no more than 2 points lost, with a paired test).
6. Ship behind a flag and track recall and answer success by script online.

**Metrics:**
- Recall@5 by script = queries whose correct chunk is in the top 5 / queries in that script, with Wilson 95% interval.
- Absolute gap = recall(Devanagari) - recall(romanised); relative gap = gap / recall(Devanagari).
- Guardrails: Devanagari recall (must not drop), latency added by transliteration or rewrite, cost per query, mixed-script queries (code-mixed) as a third bucket.

**Risks:**
- Transliteration is lossy: many romanised spellings map to several Devanagari words, so an automatic step can create new errors.
- A 200-query Devanagari test set has a 95% half-width near 5.5 points, so it cannot detect a 2-point loss. Enlarge it or use paired queries.
- Mixed script and English words inside Hindi queries break a single-script rule.
- Treating the gap as a model problem when it is a data problem (the corpus has no romanised text).

**What the interviewer scores:**
- Strong: computes absolute and relative gaps, notes both intervals and the script confound. Weak: "52 is bad, retrain the model".
- Strong: separates retrieval stages and names spelling variation as the Hindi-specific issue. Weak: a generic "use a better model".
- Strong: a non-regression gate for Devanagari with an honest note on test size. Weak: tests only the romanised set.
- Strong: asks for traffic share before prioritising. Weak: none.

**Example:** (illustrative numbers) If 40% of traffic is romanised, today's blended recall is 0.6 x 80% + 0.4 x 52% = 68.8%. A fix that lifts romanised to 70% gives 0.6 x 80% + 0.4 x 70% = 76%, a gain of 7.2 points overall, as long as Devanagari stays at 80%. Weak answer: "Add romanised data and retrain." Strong answer: "The gap is 28 points, not noise. I would pair queries by intent, normalise the script before retrieval, add character n-gram search for spelling variants, and block any change that costs Devanagari recall."

**Code:**
```python
import math

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

# Illustrative numbers from the prompt
k_dev, k_rom, n = 160, 104, 200
r_dev, r_rom = k_dev / n, k_rom / n
gap = r_dev - r_rom
rel = gap / r_dev
print(f"recall@5 Devanagari {r_dev:.0%}, romanised {r_rom:.0%}; gap {gap*100:.0f} points; relative drop {rel:.0%}; romanised = {r_rom/r_dev:.0%} of Devanagari")
assert r_dev == 0.80 and r_rom == 0.52 and round(gap, 2) == 0.28 and round(rel, 2) == 0.35

# Is 28 points more than noise? (two-proportion z, unpaired)
pool = (k_dev + k_rom) / (2 * n)
z = gap / math.sqrt(pool * (1 - pool) * 2 / n)
lo_d, hi_d = wilson(k_dev, n); lo_r, hi_r = wilson(k_rom, n)
print(f"z = {z:.1f}; Wilson Devanagari [{lo_d:.3f}, {hi_d:.3f}], romanised [{lo_r:.3f}, {hi_r:.3f}]")
assert z > 5 and hi_r < lo_d   # intervals do not overlap

# Why exact-token match fails on romanised text: spelling is not standardised.
# Toy example (invented words): three common romanised spellings of the same Hindi word.
variants = ["kaise", "kaisey", "kese"]
def grams(w, n=3):
    w = f"^{w}$"
    return {w[i:i + n] for i in range(len(w) - n + 1)}
def jac(a, b): return len(a & b) / len(a | b)
exact = [[a == b for b in variants] for a in variants]
print("exact-match hits among different spellings:", sum(exact[i][j] for i in range(3) for j in range(3) if i != j))
sims = [round(jac(grams(variants[i]), grams(variants[j])), 2) for i in range(3) for j in range(i + 1, 3)]
print("char-trigram Jaccard between spellings:", sims)
assert sum(exact[i][j] for i in range(3) for j in range(3) if i != j) == 0 and max(sims) > 0.5 and min(sims) < 0.2   # n-grams rescue near spellings only

# Guardrail: Devanagari non-regression. Allow at most 2 points of loss (illustrative) on 200 queries
# would not be detectable at n = 200: the 95% half-width is about 5-6 points.
print("Devanagari half-width at n=200: %.3f" % ((hi_d - lo_d) / 2))
assert 0.05 < (hi_d - lo_d) / 2 < 0.06

# Example: blended recall if 40% of traffic is romanised (illustrative share)
blend0 = 0.6 * r_dev + 0.4 * r_rom
blend1 = 0.6 * r_dev + 0.4 * 0.70
print(f"blended recall {blend0:.3f} -> {blend1:.3f} (gain {100*(blend1-blend0):.1f} points)")
assert round(blend0, 3) == 0.688 and round(blend1, 3) == 0.76 and round(100 * (blend1 - blend0), 1) == 7.2
```

**Output (my run):**
```text
recall@5 Devanagari 80%, romanised 52%; gap 28 points; relative drop 35%; romanised = 65% of Devanagari
z = 5.9; Wilson Devanagari [0.739, 0.850], romanised [0.451, 0.588]
exact-match hits among different spellings: 0
char-trigram Jaccard between spellings: [0.57, 0.12, 0.0]
Devanagari half-width at n=200: 0.055
blended recall 0.688 -> 0.760 (gain 7.2 points)
```

**Follow-ups:**
- Why not just transliterate every document to romanised? You lose the native script users, and there is no standard romanisation. Normalise to one canonical script and keep the original for display.
- How do you test a fix with only 200 queries? Pair the queries across versions and report the discordant counts; also grow the set where the traffic is.
- Does a bigger tokenizer help? It can shorten romanised text, but the retrieval model must be trained on that text too (Book 2 Part 02, Q17).

**Common mistakes:**
- Quoting only the absolute gap, or only the relative gap.
- Fixing romanised queries and silently dropping Devanagari recall.
- Comparing two query sets of different difficulty and calling it a script effect.
- Assuming one correct romanisation exists.

### Q37 ⭐⭐ 🟡 A chat product resends the whole history on every turn, with a 1,000-token system prompt and 300 new tokens added per turn, and the input at turn t counts the system prompt plus the 300 new tokens of each of the t turns so far, including the current one. Over a 20-turn conversation compute the total input tokens sent and their cost at an illustrative 3 per million, compare with 26,000 tokens (system prompt plus only the new 300 tokens each turn, no history resent), and propose a context-management policy.
**Asked at:** LLM cost and routing pages (getmaxim cost and semantic-cache guides, tianpan and system-design.space pages on routing and cascades, a Towards Data Science article on saving tokens in agentic AI, a Towards AI piece on AI system-design interview patterns); practitioner material, no confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Resending history makes the total grow with the square of the turn count: 83,000 input tokens over 20 turns, costing 0.249 per conversation at the illustrative 3 per million, and I would cap it with a sliding window, a running summary and prefix caching.

**Clarifying questions:**
- Is the input at turn t exactly the system prompt plus the 300 new tokens of each of the t turns so far, including the current one (the prompt's rule), and are replies counted in the 300 tokens? If replies are long, the 300 is too low.
- Is the 300 the same every turn? Real turns vary, and long pasted documents dominate the bill.
- Are conversations really 20 turns, or is the tail much longer? Cost grows with the square, so the long conversations dominate the bill.
- Does the provider offer prefix caching, and at what discount and minimum length? (Book 2 Part 01, Q24 covers how prefix caching works.)
- What must the model remember: exact wording, facts the user stated, or only the task state? That sets what a summary may drop.

**Approach:**
1. Per turn: input_t = 1,000 + 300 x t. Turn 1 is 1,300, turn 10 is 4,000, turn 20 is 7,000.
2. Total = 20 x 1,000 + 300 x (1 + 2 + ... + 20) = 20,000 + 300 x 210 = 83,000 tokens. Cost = 83,000 x 3 / 1,000,000 = 0.249.
3. Compare with 26,000 as the prompt asks: if no history were resent, each turn would send the system prompt plus its own 300 new tokens, 20 x 1,300 = 26,000. The ratio is 83,000 / 26,000 = 3.19 times.
4. Growth is quadratic: 40 turns costs 286,000 tokens, 3.45 times the 20-turn conversation for twice the length.
5. Policy, in this order: (a) cache the stable prefix (system prompt and early turns); (b) keep a sliding window of recent turns, for example the last 5, which here gives 47,000 tokens (57% of full); (c) summarise older turns into a short running summary and pin key facts (name, order id, constraints) as structured memory; (d) retrieve old turns only when the user refers back; (e) trim long tool outputs and quote only the needed lines.
6. Test the policy on real conversations: answer quality with window or summary against full history, because dropping context causes wrong answers.

**Metrics:**
- Input tokens per conversation = sum over turns of input_t; cost = tokens x price per million / 1,000,000. Also tokens per resolved conversation.
- Context growth ratio = total tokens / (turns x average new tokens).
- Quality guardrail: task success and "forgot earlier instruction" rate with the policy against full history, on a labelled sample.
- Cache hit rate and effective price (illustrative: cached tokens at 10% of the input rate).

**Risks:**
- Summaries drop details (a number, a constraint), and the bot then contradicts the user.
- A moving window breaks prefix caching if the start of the prompt changes every turn; keep the stable part first and the changing part last.
- Counting only input: long replies add output tokens, billed at a higher rate.
- Averages hide long conversations, which drive the cost.

**What the interviewer scores:**
- Strong: derives the 83,000 from a sum, not a guess, and says it grows quadratically. Weak: "it is about 7,000 x 20".
- Strong: compares with a like-for-like baseline (26,000) and says 3.19 times. Weak: compares with the system prompt alone.
- Strong: lists window, summary, caching and retrieval, with a quality test. Weak: "use a bigger context window".
- Strong: ties the policy to what the model must remember. Weak: truncates blindly.

**Example:** (illustrative numbers) Turn 20 sends 7,000 tokens, of which 1,000 is the system prompt and 6,000 is the 20 turns of new tokens (the history plus the current message). With a window of the last 5 turns it sends 1,000 + 1,500 = 2,500. Over 20 turns the window policy sends 47,000 tokens against 83,000. With prefix caching on the earlier tokens at 10% of the rate, the effective tokens fall to 14,600, 18% of uncached (ignoring any cache-write charge). Weak answer: "Conversations get expensive, so I would reduce the number of turns." Strong answer: "83,000 tokens, 3.19 times the 26,000 with no history, and quadratic in turns. I would cache the prefix, keep the last five turns plus a pinned summary, and check on labelled chats that answers do not get worse."

**Code:**
```python
# Illustrative numbers from the prompt (price is illustrative, not a vendor price)
SYS, NEW, TURNS, PRICE = 1000, 300, 20, 3.0   # tokens, tokens/turn, turns, price per million input tokens

inp = [SYS + NEW * t for t in range(1, TURNS + 1)]   # system prompt + the new tokens of each of the t turns so far
total = sum(inp)
print("input at turn 1, 10, 20:", inp[0], inp[9], inp[19])
print("total input tokens:", total, "| cost:", round(total * PRICE / 1e6, 4))
assert inp[0] == 1300 and inp[9] == 4000 and inp[19] == 7000
assert total == 20 * SYS + NEW * sum(range(1, 21)) == 20_000 + 300 * 210 == 83_000
assert round(total * PRICE / 1e6, 3) == 0.249

base = TURNS * (SYS + NEW)   # no history resent: system prompt plus the turn's own 300 tokens
print(f"no-history baseline {base}; ratio {total/base:.2f}")
assert base == 26_000 and round(total / base, 2) == 3.19

# Growth is quadratic in turns
total40 = sum(SYS + NEW * t for t in range(1, 41))
print("40 turns:", total40, "tokens, x%.2f of 20 turns" % (total40 / total))
assert total40 == 40 * 1000 + 300 * 820 == 286_000 and round(total40 / total, 2) == 3.45

# Policy A: keep the system prompt plus only the last 5 turns (including the current one)
K = 5
win = sum(SYS + NEW * min(t, K) for t in range(1, TURNS + 1))
print("sliding window (last 5 turns):", win, "tokens,", f"{win/total:.0%} of full history")
assert win == 20_000 + 300 * (sum(range(1, 6)) + 15 * 5) == 47_000 and round(win / total, 2) == 0.57

# Policy B: prefix caching, previously sent tokens billed at 10% of the input rate (illustrative)
CACHE = 0.10
eff = inp[0] + sum(CACHE * inp[t - 2] + NEW for t in range(2, TURNS + 1))   # turn t re-reads turn t-1's input as prefix
eff_cost = eff * PRICE / 1e6
print(f"with prefix cache: effective tokens {eff:.0f}, cost {eff_cost:.4f} ({eff/total:.0%} of uncached)")
assert round(eff) == 14_600 and round(eff / total, 2) == 0.18

# Other numbers quoted in the text
print("20 x last turn:", 20 * inp[19], "| turn 20 with window:", SYS + NEW * K)
assert 20 * inp[19] == 140_000 and SYS + NEW * K == 2_500 and inp[19] - SYS == 6_000
```

**Output (my run):**
```text
input at turn 1, 10, 20: 1300 4000 7000
total input tokens: 83000 | cost: 0.249
no-history baseline 26000; ratio 3.19
40 turns: 286000 tokens, x3.45 of 20 turns
sliding window (last 5 turns): 47000 tokens, 57% of full history
with prefix cache: effective tokens 14600, cost 0.0438 (18% of uncached)
20 x last turn: 140000 | turn 20 with window: 2500
```

**Follow-ups:**
- Why not simply use a model with a bigger window? The window only limits what fits; you still pay for every resent token, and latency rises with prompt length.
- How do you decide the window size? Plot task success against the window size on labelled conversations and take the smallest size at which success stops improving.
- What changes if replies are long? Replies join the history, so the 300 is too low and growth is faster. Cap the stored reply or summarise it.

**Common mistakes:**
- Multiplying the last turn's input by the number of turns (7,000 x 20 = 140,000 overstates it).
- Comparing with a baseline that omits the new tokens of each turn (the system prompt alone, 20,000).
- Forgetting output tokens and tool outputs.
- Summarising without a test for dropped facts.

### Q38 ⭐⭐ 🟡 An output PII filter must see text before the user does. Answers average 400 tokens at 40 tokens per second, the filter takes 0.1 seconds per check, and you can ignore the time to first token. Compute when the first text appears if the whole answer is buffered and if it is checked in 50-token chunks, and describe the risk you accept with chunking.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to output guardrail and streaming topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Buffering the whole answer means the first text appears at 10.1 s, while checking 50-token chunks shows it at 1.35 s, and the price is that PII can straddle a chunk boundary or be shown before later context makes it a problem, so I would use a rolling window with a short hold-back.

**Clarifying questions:**
- Which PII must never be shown (phone, ID numbers, names of other customers) and which is acceptable (the user's own data)? That decides how strict the filter is.
- Is the filter rule-based (regex), a model, or both? A model filter needs more context than a 50-token chunk.
- Is the 0.1 s per check independent of chunk size? If it grows with text length, the buffered number changes.
- Does the filter run alongside generation (pipelined) or does it pause the stream? The prompt says nothing, and the finish time differs (10.1 s against 10.8 s in the Code).
- What happens when a chunk fails after earlier chunks were shown? Can the UI retract text?

**Approach:**
1. Buffered: generation takes 400 / 40 = 10 s, then one check of 0.1 s. First text at 10.1 s. For a chat UI that is far too slow, since the user sees nothing for 10 s.
2. Chunked: the first 50 tokens take 50 / 40 = 1.25 s, plus a 0.1 s check, so the first text appears at 1.35 s. Later chunks follow every 1.25 s, and the last appears at 10.1 s, the same finish as buffering, if checks run alongside generation. If each check paused generation, the end would be 8 x 0.1 = 0.8 s later, at 10.8 s.
3. The risk accepted: the filter sees only a window. A phone number split across two chunks passes both checks (demonstrated in Code with an invented number). Shown text cannot be taken back once the user has seen it. Context-dependent PII (a name that is only sensitive given the earlier sentence) can slip.
4. Mitigations: run the check on a rolling window (the previous tail plus the new chunk); hold back the last few tokens of each chunk until the next check (the Code uses 10 tokens: 40 tokens show at 1.35 s, and the held tail lags by about 1.25 s); use patterns that tolerate splits; use smaller first chunks only if latency matters; a retract and replace UI as a last resort, plus a block-and-apologise path.
5. Reduce what can leak at the source: do not put other users' PII in the prompt (redact before the model sees it), so the output filter is a second layer, not the only layer.
6. Decide per product: high-risk (medical, financial) can accept a longer first-text delay; low-risk chat should stream.

**Metrics:**
- Time to first visible text = time to generate the first chunk + check time (1.35 s here); time to last text.
- PII leak rate = answers with PII shown to a user / answers; measured on a red-team set with planted PII, with a recall target (for example, at least 99% of planted items caught, illustrative) and a Wilson interval.
- Boundary-miss rate = planted PII split across a chunk boundary that was missed / those split cases.
- False block rate (benign text withheld) as the guardrail.

**Risks:**
- Chunk-boundary misses (shown in Code).
- A retraction after text was visible is a leak already, even if the final log is clean.
- Filter latency grows with a model-based filter (0.1 s was for the prompt's filter only).
- Over-blocking frustrates users and teaches them to work around it.

**What the interviewer scores:**
- Strong: computes 10.1 s and 1.35 s and says chunking keeps the same finish time. Weak: says streaming "is faster" with no number.
- Strong: names the boundary problem and a fix (rolling window, hold-back). Weak: "just filter each chunk".
- Strong: states that visible text is irreversible, so the filter is not a substitute for input redaction. Weak: relies on the output filter alone.
- Strong: asks which PII and what the product risk is. Weak: one-size answer.

**Example:** (illustrative numbers) The answer contains the invented number "98765 43210". Chunk 1 ends "...call me on 98765", chunk 2 starts " 43210 ...". Each chunk alone has only five digits, so a ten-digit pattern passes both. A rolling check on both together catches it. Weak answer: "Stream and filter every chunk, done." Strong answer: "First text moves from 10.1 s to 1.35 s. I accept boundary risk, so I check a rolling window, hold the last tokens back, and also redact PII before it reaches the prompt."

**Code:**
```python
import re

# Illustrative numbers from the prompt (time to first token ignored)
TOK, TPS, CHECK, CHUNK = 400, 40, 0.1, 50

buffered = TOK / TPS + CHECK
chunked_first = CHUNK / TPS + CHECK
print(f"buffered: first text at {buffered:.2f} s; chunked: first text at {chunked_first:.2f} s")
assert buffered == 10.1 and chunked_first == 1.35 and round(buffered - chunked_first, 2) == 8.75

# Chunked, checks run alongside generation: when does each chunk become visible, and when does the last one?
n_chunks = TOK // CHUNK
visible = [(k * CHUNK) / TPS + CHECK for k in range(1, n_chunks + 1)]
print("chunks:", n_chunks, "| visible at (s):", [round(v, 2) for v in visible])
assert n_chunks == 8 and visible[0] == 1.35 and round(visible[-1], 2) == 10.1   # same finish time as buffered

# If checks were serial and paused generation instead: 8 x 0.1 s added
serial_total = TOK / TPS + n_chunks * CHECK
print("if each check paused generation, last text at", serial_total, "s")
assert round(serial_total, 2) == 10.8

# The risk with chunking: a fake 10-digit number split across a chunk boundary (invented data)
pii = re.compile(r"\b\d{5} ?\d{5}\b")
chunk1 = "Please call me on 98765"
chunk2 = " 43210 tomorrow morning."
per_chunk_hits = [bool(pii.search(c)) for c in (chunk1, chunk2)]
rolling_hit = bool(pii.search(chunk1 + chunk2))
print("per-chunk check finds it:", any(per_chunk_hits), "| check with held-back overlap finds it:", rolling_hit)
assert not any(per_chunk_hits) and rolling_hit

# Cost of the fix: check a rolling window (previous tail + new chunk) and show everything except the last H tokens
H = 10
first_release_tokens = CHUNK - H
tail_lag = CHUNK / TPS   # the held-back tail waits for the next chunk to arrive and be checked
print(f"first text at {chunked_first:.2f} s still, showing {first_release_tokens} tokens; the held tail lags by {tail_lag:.2f} s")
assert first_release_tokens == 40 and tail_lag == 1.25
assert TOK // 10 == 40   # checks needed with 10-token chunks (follow-up)
```

**Output (my run):**
```text
buffered: first text at 10.10 s; chunked: first text at 1.35 s
chunks: 8 | visible at (s): [1.35, 2.6, 3.85, 5.1, 6.35, 7.6, 8.85, 10.1]
if each check paused generation, last text at 10.8 s
per-chunk check finds it: False | check with held-back overlap finds it: True
first text at 1.35 s still, showing 40 tokens; the held tail lags by 1.25 s
```

**Follow-ups:**
- Why not use very small chunks? Each chunk needs a check, and smaller windows see less context, so misses rise and the check load grows (8 checks here, 40 with 10-token chunks).
- Is time to first token really ignorable? Not in production. It adds to both numbers equally here, so the 8.75 s gap stays.
- Can the model be told not to output PII? Yes, but treat that as a hint, not a control.

**Common mistakes:**
- Treating per-chunk checking as equivalent to whole-answer checking.
- Forgetting that already shown text cannot be recalled.
- Adding check time to every chunk as if generation stopped, or ignoring it altogether.
- Leaving PII in the prompt and relying on the output filter.

### Q39 ⭐⭐ 🔴 Users can upload PDFs that are added to a shared knowledge base, and a scanner flags 1,000 of 50,000 uploads (2%) as possibly containing hidden instructions. A manual review takes 5 minutes per flagged file. Compute the review hours, and explain why scanning alone is not enough and what architecture limits the damage when a poisoned document is retrieved.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to indirect prompt-injection topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The review costs 1,000 x 5 minutes = 83.3 hours, about two person-weeks, but scanning alone is not enough because the scanner misses things and the 49,000 unflagged files are never read, so I would also limit what a poisoned document can do once retrieved.

**Clarifying questions:**
- Who can upload (employees, customers, the public) and who can retrieve the documents? A shared base with anonymous uploads is the worst case.
- What can the assistant do after reading a document: only answer, or call tools (send email, issue refunds)? Tool access turns an injection from a wrong answer into an action.
- How was the scanner built (patterns, a classifier, an LLM) and what is its measured recall on known attacks? The 2% flag rate says nothing about misses.
- Is a document visible to all users once indexed, or filtered by owner or tenant? Isolation limits the blast radius.
- What is the review capacity, and what should happen to a file while it waits in the queue?

**Approach:**
1. Compute the load: 2% of 50,000 is 1,000 flagged files; at 5 minutes each that is 83.3 hours, about 2.1 weeks for one reviewer. Plan staffing, or review in priority order (by how widely the file would be retrieved).
2. Quarantine flagged files: do not index them until reviewed. Unflagged files are indexed, so also add the controls below.
3. Measure what the scanner misses. Audit a random sample of unflagged files (490 files take 40.8 hours in the Code). If the audit finds none, the "rule of three" bounds the unflagged poison rate at about 0.6% (up to about 300 files), so a clean audit bounds the risk and does not remove it. Also run red-team uploads with planted instructions to measure recall.
4. Architecture to limit the damage: treat retrieved text as data, never as instructions (clear delimiters and a system rule that documents cannot give commands, with the knowledge that this is a soft control); give the answering model no tools, or only read-only tools; put any action behind separate checks that do not read document text (allow-lists, amount limits, human approval); keep tenant or owner isolation so one upload does not reach everyone; show citations and provenance so users can see the source; filter the output for links, secrets and sensitive actions; log retrieved chunks so a bad document can be traced and removed (delete by document id).
5. Respond fast to incidents: be able to remove a document and its chunks from the index in minutes, and to find every answer that used it.
6. Retrain the scanner on caught examples and re-scan the older documents when it improves.

**Metrics:**
- Review hours = flagged files x minutes per file / 60 (83.3). Queue age: oldest unreviewed flagged file.
- Scanner recall = poisoned files flagged / all poisoned files (measured on planted and audited files); precision = truly poisoned flagged / flagged.
- Unflagged miss estimate from the random audit with an interval (rule of three if zero).
- Impact metric: tool or action attempts triggered by retrieved text per 10,000 answers, which the architecture aims to keep at zero.

**Risks:**
- The attacker adapts to the scanner; instructions can be hidden in white text, metadata, other languages or encodings.
- Reviewers get tired after hundreds of files, so review quality falls; rotate and sample-check reviewers.
- Quarantine delays legitimate uploads and annoys users.
- A false sense of safety after a clean scan.

**What the interviewer scores:**
- Strong: 83.3 hours, and the point that 49,000 files are unread. Weak: "review the flagged ones and we are safe".
- Strong: separates detection from containment (no tools, isolation, approvals). Weak: only "improve the scanner".
- Strong: measures scanner recall with planted files and an audit. Weak: trusts the flag rate.
- Strong: mentions removal and tracing of a bad document. Weak: none.

**Example:** (illustrative numbers) Suppose 100 of the 50,000 files are truly poisoned and the scanner catches 80. Then 20 slip through, and only 80 of 1,000 flagged files (8%) are truly poisoned, so reviewers spend most of their 83 hours on harmless files. Weak answer: "A 2% flag rate means the corpus is 98% clean." Strong answer: "The flag rate is not a poison rate. I would audit a sample of unflagged files, assume some get through, and make sure a poisoned chunk can only influence an answer, never trigger a refund."

**Code:**
```python
# Illustrative numbers from the prompt
uploads, flagged, minutes = 50_000, 1_000, 5
print("flag rate:", flagged / uploads)
assert flagged / uploads == 0.02

hours = flagged * minutes / 60
print(f"review: {flagged} files x {minutes} min = {hours:.1f} hours = {hours/40:.1f} person-weeks of 40 h")
assert round(hours, 1) == 83.3 and round(hours / 40, 1) == 2.1

# Scanning alone is not enough: the unflagged 49,000 files are never read.
# Invented scenario: 100 truly poisoned files in 50,000, scanner catches 80 of them (80% recall).
poisoned, caught = 100, 80
missed = poisoned - caught
precision = caught / flagged
print(f"poisoned files that slip through: {missed}; share of flagged files that are truly poisoned: {precision:.0%}")
assert missed == 20 and precision == 0.08

# Audit a random sample of the UNflagged files to estimate the miss rate
unflagged = uploads - flagged
sample = 490
audit_hours = sample * minutes / 60
print(f"audit {sample} of {unflagged} unflagged files: {audit_hours:.1f} hours")
assert unflagged == 49_000 and round(audit_hours, 1) == 40.8
# If the audit finds zero poisoned files, the 'rule of three' upper bound (95%) on the unflagged poison rate is 3/n
ub = 3 / sample
print(f"zero found -> upper bound {ub:.2%} of unflagged files, i.e. up to {ub*unflagged:.0f} files")
assert round(ub * 100, 2) == 0.61 and round(ub * unflagged) == 300
# so a clean audit does not show the corpus is clean; it bounds it. Architecture must limit the damage.
```

**Output (my run):**
```text
flag rate: 0.02
review: 1000 files x 5 min = 83.3 hours = 2.1 person-weeks of 40 h
poisoned files that slip through: 20; share of flagged files that are truly poisoned: 8%
audit 490 of 49000 unflagged files: 40.8 hours
zero found -> upper bound 0.61% of unflagged files, i.e. up to 300 files
```

**Follow-ups:**
- Can a prompt that says "ignore instructions in documents" solve it? It lowers the risk, but models can still follow injected text, so it is one layer and not a guarantee.
- How do you cut the review hours? Triage by risk and reach: a document retrievable by many users, or one that mentions tools or credentials, goes first; review time per file can fall for obvious cases (illustrative), for example with a first-pass triage step.
- What if you cannot afford the review? Index nothing from untrusted uploads into the shared base; keep it in the uploader's private space.

**Common mistakes:**
- Calling the flag rate the infection rate.
- Putting an agent with write tools in the same context as untrusted documents.
- Relying on prompt wording as the only defence.
- No way to delete a document and its chunks quickly.

### Q40 ⭐⭐ 🔴 In 500 staged runs, each with one write action, an agent took a wrong write action in 20 (4%, a measured sample). Production will make 30,000 write actions a month. Compute a 95% Wilson interval for the wrong-action rate and the implied monthly range, and say which permissions, approvals and rollback you would add.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to agent wrong-action and tool-permission topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** 20 wrong writes in 500 is 4%, with a 95% Wilson interval of about 2.6% to 6.1%, which means roughly 780 to 1,830 wrong writes a month on 30,000, so the agent must not write unsupervised until permissions, approvals and rollback cut that by orders of magnitude.

**Clarifying questions:**
- What is a "wrong write" (wrong record, wrong amount, wrong customer, a harmless typo)? Severity decides the controls, and the 4% mixes them.
- Were the staged runs drawn from the real task mix? If staging is easier or harder than production, the rate moves.
- Are the 500 runs independent (fresh state, different tasks)? The interval assumes they are.
- Are writes reversible (edit a draft) or irreversible (send money, send email)? That sets the rollback design.
- Who owns the cost of a wrong write, and what is it per incident? It turns a rate into money and into an approval rule.

**Approach:**
1. Rate and interval: 20 / 500 = 4.0%. Wilson 95%: 2.60% to 6.10% (Wald gives 2.28% to 5.72%, close here but poorer for small rates).
2. Monthly range at 30,000 writes: point 1,200; low 781; high 1,829. Say it as a range, and say that "even the optimistic end is hundreds a month".
3. Classify writes by severity and reversibility: read-only, reversible low-impact, reversible high-impact, irreversible. Treat each class separately; the 4% will not be uniform.
4. Permissions: least privilege per tool (the agent gets the narrowest scope; no delete, no bulk update; amount and record limits; separate credentials per environment).
5. Approvals: human approval for irreversible or high-value writes; a preview (diff of what will change) so the approver can decide in seconds; policy checks outside the model (rules that do not depend on the agent's judgement).
6. Rollback: log every write with before and after values and an id; make writes idempotent; use soft deletes and delayed commit (stage, then apply); a kill switch that stops all writes; a tested undo.
7. Rollout: start in shadow mode (propose writes only), then low-risk writes, widening as measured. Evidence needed: to claim under 0.1% with 95% confidence from clean runs you need about 3,000 runs with zero wrong writes (rule of three), so use production monitoring and sampled audit too.
8. Improve the agent: study the 20 failures by cause (wrong tool argument, misread record, stale state) and fix each class with validation (check ids exist and match the request).

**Metrics:**
- Wrong-write rate = writes that were wrong / total writes, Wilson 95% interval; also by severity class.
- Residual wrong writes per month after controls = writes x rate x (1 - share caught by approval and validation).
- Approval load = writes sent to humans / total writes; approver time per write; approver override rate.
- Time to detect and time to roll back a wrong write.

**Risks:**
- Staged runs are not production: the 4% can be an underestimate, because real data is messier.
- Approval fatigue: if 40% of writes need approval, people click "approve" without reading.
- Errors correlate (one bad prompt, one bad tool change), so a month can be much worse than the independent range.
- A control that depends on the same model (asking the agent to double-check itself) fails in the same way.

**What the interviewer scores:**
- Strong: interval by Wilson and the monthly range 781 to 1,829, with a statement of its assumptions. Weak: "4% of 30,000 is 1,200" with no uncertainty.
- Strong: sorts writes by severity and reversibility and applies different controls. Weak: "add a human to everything".
- Strong: designs rollback (log, before and after values, kill switch). Weak: "we will fix it if it happens".
- Strong: knows how much evidence is needed to claim a low rate (3,000 clean runs for 0.1%). Weak: "500 runs is enough".

**Example:** (illustrative numbers) A wrong write that needs a refund costs 20. At 1,200 wrong writes a month that is 24,000. With human approval catching 90% of wrong writes (invented) the residual is 120 writes, about 2,400. Weak answer: "4% error is fine, the agent is helpful." Strong answer: "That is 780 to 1,830 wrong writes a month. I would have the agent propose writes, require approval for the irreversible ones, restrict its permissions, log before and after values, and measure the real rate in shadow mode first."

**Code:**
```python
import math

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

# Illustrative numbers from the prompt
k, n, monthly = 20, 500, 30_000
p = k / n
lo, hi = wilson(k, n)
print(f"rate {p:.1%}; Wilson 95% [{lo:.2%}, {hi:.2%}]")
assert p == 0.04 and 0.0259 < lo < 0.0262 and 0.0609 < hi < 0.0612

print(f"monthly wrong writes: point {p*monthly:.0f}, range {lo*monthly:.0f} to {hi*monthly:.0f}")
assert round(p * monthly) == 1200 and 780 < lo * monthly < 783 and 1828 < hi * monthly < 1831

# Normal-approximation interval for comparison (it is similar here, but worse for small rates)
se = math.sqrt(p * (1 - p) / n)
print(f"Wald 95% [{p-1.96*se:.2%}, {p+1.96*se:.2%}]")
assert round(p - 1.96 * se, 4) == 0.0228 and round(p + 1.96 * se, 4) == 0.0572

# Even the lowest end of the interval is hundreds of wrong writes a month. Layered controls (illustrative):
approve_catch = 0.90     # human approval catches 90% of wrong writes it is shown (invented)
residual = p * monthly * (1 - approve_catch)
print(f"if approval catches 90%, residual point estimate: {residual:.0f} a month")
assert round(residual) == 120

# How many clean staged runs would you need to claim the rate is below 0.1% (rule of three)?
need = math.ceil(3 / 0.001)
print("clean runs needed for a 95% upper bound of 0.1%:", need)
assert need == 3000

# Chance of at least one wrong write in a week of 7,000 writes at the lower bound (independence assumed)
week = 7_000
print("P(at least one wrong write in a week at 2.6%):", 1 - (1 - lo) ** week)
assert 1 - (1 - lo) ** week > 0.999999

# Example numbers quoted in the text (illustrative cost of 20 per wrong write)
assert round(p * monthly) * 20 == 24_000 and round(residual) * 20 == 2_400
```

**Output (my run):**
```text
rate 4.0%; Wilson 95% [2.60%, 6.10%]
monthly wrong writes: point 1200, range 781 to 1829
Wald 95% [2.28%, 5.72%]
if approval catches 90%, residual point estimate: 120 a month
clean runs needed for a 95% upper bound of 0.1%: 3000
P(at least one wrong write in a week at 2.6%): 1.0
```

**Follow-ups:**
- Would you ship if approval catches 90%? Only for reversible, low-impact writes, with monitoring. For irreversible writes, 120 residual a month is still high, so keep a human in the loop for them or lower the rate first.
- Why Wilson and not the plain normal interval? With small rates and moderate samples Wilson stays inside 0 to 1 and has better coverage; here the two are close.
- How do you know when the controls work? Count wrong writes per 10,000 in production with sampled audits, and watch the interval narrow over weeks.

**Common mistakes:**
- Reporting a point estimate with no interval.
- Treating the staged rate as the production rate.
- Putting the verifier in the same model and context as the actor.
- Adding approvals everywhere until reviewers stop reading.

### Q41 ⭐⭐ 🔴 A user exercises a right to have personal data deleted. It sits in raw chat logs, in 3,000 of 2,000,000 chunks in a vector index, in an evaluation dataset and in 35-day rolling backups, and your internal deletion target is 30 days. Compute the share of the index affected, the gap between the target and the backup retention, and the day the last backup copy expires if the live data is deleted on day 1, and lay out a deletion plan that is honest about what cannot be erased immediately.
**Asked at:** PII and compliance material (tianpan, Kunal Ganglani, Gravitee and barkingiguana pages on logs, retention, redaction and data residency, and a vendor piece on DPDP readiness for LLM traffic); vendor and practitioner pages, not regulator guidance or an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The vector index is only 0.15% affected (3,000 of 2,000,000 chunks), and backups outlast the 30-day target by 5 days (35 against 30), with the last backup copy expiring on day 36 if live data is deleted on day 1, so I would delete from every live store quickly, verify it, and tell the user and the privacy owner honestly that backups age out later.

**Clarifying questions:**
- Which law or contract drives the request and its deadline? I do not give legal advice. The data protection officer or counsel confirms the obligation and whether the 30 days is an internal target or a legal limit.
- How is data linked to the person: a user id on every row, or only in free text? Chunks and chat text may contain the name without the id.
- Was the data used to train or fine-tune any model, or to build eval sets? Deleting a row does not remove what a model already learned.
- Can backups be restored selectively, or only whole? That decides whether a suppression list is enough.
- Is data copied elsewhere (analytics, a vendor's logs, caches, exports)? A deletion plan is only as good as the data map.

**Approach:**
1. Build a data map for this user: raw chat logs, vector index (the 3,000 chunks), evaluation dataset, backups, plus caches, analytics and the vendor API's own logs and retention.
2. Size the index work: 3,000 / 2,000,000 = 0.15% of chunks. Delete by user id (or by source document id) and also search text for chunks without the id. Many index types mark deleted vectors and remove them later, so run compaction and verify with queries that the chunks no longer return.
3. Logs: delete by user id; confirm downstream copies (warehouse, trace store).
4. Evaluation dataset: remove or redact the rows and re-export; note any model already evaluated on them.
5. Backups (35 days against a 30-day target, a 5-day gap in retention): backups are usually immutable, so you cannot edit them. Be honest: the copy expires when the last backup that held it expires. If live data is deleted on day d, the last backup copy expires on day d + 35: day 36 for deletion on day 1, and day 65 for deletion on day 30. Fix going forward: keep a suppression list of deleted user ids and re-apply deletion on any restore; and consider shortening backup retention to 30 days or less if the policy requires erasure in 30.
6. Verify and record: run checks (queries return nothing), keep a deletion record without the personal data (request id, dates, systems), and reply to the user with what was deleted and when the backups expire.
7. Prevent repeats: tag data with a user id at ingestion; avoid putting personal data into evaluation sets; minimise retention of raw logs.

**Metrics:**
- Share of index affected = chunks for the user / total chunks (0.15%).
- Time to delete per store (days from request), against the 30-day target; deletion verification pass rate = stores verified clean / stores in the data map.
- Residual exposure window = last backup expiry day minus target day (5 days between retention and target; 6 days over the target, day 36, when live data is deleted on day 1).
- Guardrails: number of restores that re-applied the suppression list; requests completed on time / all requests.

**Risks:**
- Missing a copy (cache, vendor logs, analytics) means the deletion claim is false.
- Telling the user "everything is deleted" when backups still hold the data is an honesty and compliance problem.
- A restore from backup silently brings the data back.
- Personal data inside text chunks that carry no user id is easy to miss.
- A model fine-tuned on the data may still reproduce it; that needs a separate decision with the privacy owner.

**What the interviewer scores:**
- Strong: lists every store and an action and date for each, including backups. Weak: "delete the user's rows".
- Strong: says plainly what cannot be erased immediately, and the suppression list. Weak: promises full deletion by day 30.
- Strong: sends the legal question to the privacy owner and counsel. Weak: quotes legal rules from memory.
- Strong: thinks about the index mechanics (delete, compact, verify). Weak: ignores the vector store.

**Example:** (illustrative numbers) Day 3 logs deleted, day 7 index chunks deleted and verified, day 10 evaluation rows removed. Backups are frozen: with deletion on day 1 the last copy ages out on day 36, six days after the target. Weak answer: "All deleted within 30 days, no problem." Strong answer: "Live stores are clean by day 10. Backups keep the data until day 36, so I would tell the user that, add the user to a suppression list so a restore cannot bring the data back, and ask the privacy owner whether to shorten backup retention."

**Code:**
```python
# Illustrative numbers from the prompt
chunks_total, chunks_user = 2_000_000, 3_000
share = chunks_user / chunks_total
print(f"share of index affected: {share:.2%} ({chunks_user} of {chunks_total})")
assert share == 0.0015

target, backup = 30, 35
gap = backup - target
print("backup retention minus target:", gap, "days")
assert gap == 5

# Honest timeline. Day 0 = request. Live stores are deleted on day d (d <= 30).
# Any backup taken up to day d still holds the data, and expires 35 days after it was taken.
for d in (1, 7, 30):
    last_copy_expires = d + backup
    print(f"live deletion on day {d:2d}: last backup copy expires on day {last_copy_expires} (target day {target}, over by {last_copy_expires - target})")
assert [d + backup for d in (1, 7, 30)] == [36, 42, 65]

# Plan table: store -> action -> day it is done (invented schedule, illustrative)
plan = [
    ("raw chat logs", "delete by user id, verify by query", 3),
    ("vector index", "delete 3,000 chunks by user id, compact index, verify by query", 7),
    ("evaluation dataset", "remove or redact the rows, re-export without them", 10),
    ("backups", "cannot edit; suppression list re-applied on any restore; expire by day d + 35", 36),
]
for s, a, day in plan:
    print(f"{s:20s} day {day:3d}  {a}")
within = [s for s, a, day in plan if day <= target]
outside = [s for s, a, day in plan if day > target]
assert within == ["raw chat logs", "vector index", "evaluation dataset"] and outside == ["backups"]
```

**Output (my run):**
```text
share of index affected: 0.15% (3000 of 2000000)
backup retention minus target: 5 days
live deletion on day  1: last backup copy expires on day 36 (target day 30, over by 6)
live deletion on day  7: last backup copy expires on day 42 (target day 30, over by 12)
live deletion on day 30: last backup copy expires on day 65 (target day 30, over by 35)
raw chat logs        day   3  delete by user id, verify by query
vector index         day   7  delete 3,000 chunks by user id, compact index, verify by query
evaluation dataset   day  10  remove or redact the rows, re-export without them
backups              day  36  cannot edit; suppression list re-applied on any restore; expire by day d + 35
```

**Follow-ups:**
- Can you cut the backup problem completely? Shorter retention, or encrypting per user and deleting the key (crypto-shredding), is a design choice with costs; discuss it with the privacy owner.
- What about the embeddings themselves? Embeddings can leak information about the text, so delete them with the chunk.
- What if the chunks have no user id? Search by content, ask the user for identifiers, and log what was searched.

**Common mistakes:**
- Forgetting backups, caches, vendor logs and evaluation sets.
- Saying "deleted" when the index only marked the vectors.
- Quoting legal rules from memory.
- Computing the 5-day retention gap and stopping there, without the day the last copy expires.

### Q42 ⭐⭐ 🔴 You want a regression suite to detect a drop in pass rate from 80% to 75% (5 points absolute) with 95% confidence and 80% power, using separate prompt samples for the two versions. Compute the number of prompts needed per version with the normal approximation, compare it with your 200-prompt suite, and say how scoring both versions on the same prompts would help.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to regression-suite sizing in LLM evaluation pages; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** To detect 80% to 75% with 95% confidence and 80% power on separate prompt samples I need about 1,091 prompts per version, so a 200-prompt suite (18% of that) has only about 22% power; scoring both versions on the same prompts cuts the need a lot when their outcomes are correlated.

**Clarifying questions:**
- Two-sided or one-sided? I assume two-sided at 5%, the standard choice. A one-sided test (only drops matter) needs 860 per version.
- Is 80% the true pass rate on the same prompt mix production sees? The sample size depends on the baseline (variance p x (1-p)).
- What is the smallest drop worth catching? 5 points is the prompt's choice. Halving it roughly quadruples the sample.
- How many times will I run each prompt? Repeated runs reduce sampling noise from the model but not the prompt-sampling noise (the prompts are still only 200).
- Are pass/fail labels cheap, or are humans needed? That limits the suite size.

**Approach:**
1. Formula (normal approximation, two proportions): n per group = (z_alpha/2 + z_power)^2 x (p1 x (1-p1) + p2 x (1-p2)) / d^2.
2. Numbers: z_alpha/2 = 1.960, z_power = 0.842, variance sum = 0.16 + 0.1875 = 0.3475, d = 0.05. n = (2.802)^2 x 0.3475 / 0.0025 = 1,090.x, so 1,091 per version.
3. Compare with 200: 200 / 1,091 = 18%. The power of a 200-prompt unpaired comparison for a true 5-point drop is about 22% (Code): most real 5-point drops would go unnoticed, and a "no significant change" result would be uninformative.
4. Paired design: score both versions on the same prompts. Hard prompts are hard for both, so the per-prompt outcomes are correlated, and the variance of the difference shrinks: variance = 0.3475 - 2 x rho x sqrt(0.16 x 0.1875). With the correlation rho = 0.5, 0.7, 0.9 (illustrative; measure it on a pilot) the prompts needed are 548, 330 and 113 (Code). At rho = 0 there is no gain (1,091).
5. Analyse with a paired test (McNemar: only prompts where the versions disagree count, b = pass-to-fail, c = fail-to-pass; z = (b - c) / sqrt(b + c)). A simulation (seeded, rho 0.7, 330 prompts) detects the drop in about 81% of runs, consistent with 80% power.
6. Practical suite: grow it toward a few hundred paired prompts, stratified by intent so you can read segments, with fixed seeds or temperature 0 and repeated runs for noisy tasks; add a tolerance rule (a drop of more than 3 points on the interval's upper bound triggers review).

**Metrics:**
- Pass rate = prompts passed / prompts scored, with Wilson 95% interval; difference with an interval from the paired counts.
- Power = probability that the test flags a true 5-point drop at 5% significance (22% for 200 unpaired, about 80% for 330 paired at rho 0.7).
- Discordant counts b and c per version pair.

**Risks:**
- The rho of 0.7 is invented; real correlation may be lower (a rewritten prompt may change many outcomes) and the saving shrinks.
- Normal approximation is rough near the edges and for small counts; use exact McNemar for small b + c.
- A suite that is not like production gives a precise answer to the wrong question.
- Many versions compared to the same suite inflate false alarms; choose one decision metric per release.

**What the interviewer scores:**
- Strong: gives the formula and 1,091 per version, and the power of 200 (about 22%). Weak: "200 is probably enough".
- Strong: explains why pairing helps (correlated outcomes; variance of the difference). Weak: "pairing is just better".
- Strong: states the two-sided and 95%/80% assumptions. Weak: skips them.
- Strong: includes stratification and a decision rule. Weak: only a number.

**Example:** (illustrative numbers) On a pilot of 200 paired prompts, v1 passes 160, v2 passes 150. Among the 200, 15 pass in v1 and fail in v2 (b = 15) and 5 fail in v1 and pass in v2 (c = 5). Check: 160 - 15 + 5 = 150. McNemar z = (15 - 5) / sqrt(20) = 2.24, a significant drop at 5%. Treating the same two scores as independent samples gives z about 1.2 and no significance. Weak answer: "75 against 80, 200 prompts, not significant, ship." Strong answer: "With 200 unpaired prompts the test has 22% power, so a null result means nothing. Score the same prompts and read the paired counts: 15 against 5 is a real drop."

**Code:**
```python
import math
import numpy as np
from scipy import stats

# Illustrative numbers from the prompt
p1, p2, alpha, power, n_suite = 0.80, 0.75, 0.05, 0.80, 200
d = p1 - p2
za, zb = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
var_unpaired = p1 * (1 - p1) + p2 * (1 - p2)          # variance of (x1 - x2) per prompt if independent
n_per = (za + zb) ** 2 * var_unpaired / d ** 2
print(f"z_alpha/2 = {za:.3f}, z_power = {zb:.3f}, variance sum = {var_unpaired:.4f}")
print(f"unpaired n per version = {n_per:.1f} -> {math.ceil(n_per)}; suite of {n_suite} is {n_suite/math.ceil(n_per):.0%} of that")
assert round(var_unpaired, 4) == 0.3475 and math.ceil(n_per) == 1091 and round(n_suite / 1091, 2) == 0.18

# Power of the 200-prompt suite for the same 5-point drop (unpaired, two-sided)
se200 = math.sqrt(var_unpaired / n_suite)
pw200 = stats.norm.sf(za - d / se200) + stats.norm.cdf(-za - d / se200)
print(f"power of a {n_suite}-prompt unpaired comparison: {pw200:.2f}")
assert 0.20 < pw200 < 0.25

# One-sided test (only care about drops) needs fewer
za1 = stats.norm.ppf(1 - alpha)
n_one = (za1 + zb) ** 2 * var_unpaired / d ** 2
print("one-sided n per version:", math.ceil(n_one))
assert math.ceil(n_one) == 860

# Paired: same prompts for both versions. Variance of the per-prompt difference falls with the correlation rho
# between the two versions' pass/fail on a prompt (rho is invented; measure it on a pilot).
def n_paired(rho):
    cov = rho * math.sqrt(p1 * (1 - p1) * p2 * (1 - p2))
    var = var_unpaired - 2 * cov
    return (za + zb) ** 2 * var / d ** 2
for rho in (0.0, 0.5, 0.7, 0.9):
    print(f"rho {rho}: prompts needed (paired) = {math.ceil(n_paired(rho))}")
assert math.ceil(n_paired(0.0)) == 1091 and math.ceil(n_paired(0.5)) == 548 and math.ceil(n_paired(0.7)) == 330 and math.ceil(n_paired(0.9)) == 113

# Check by simulation (seeded): paired design at rho = 0.7 with n = 330 prompts detects the drop about 80% of the time
rng = np.random.default_rng(11)
def sim_power(n, rho, reps=4000):
    cov = rho * math.sqrt(p1 * (1 - p1) * p2 * (1 - p2))
    # joint distribution of (pass_v1, pass_v2)
    p11 = p2 * 0 + (p1 * p2 + cov)
    p10 = p1 - p11; p01 = p2 - p11; p00 = 1 - p11 - p10 - p01
    cells = rng.multinomial(n, [p11, p10, p01, p00], size=reps)
    b, c = cells[:, 1], cells[:, 2]       # discordant counts
    z = (b - c) / np.sqrt(np.maximum(b + c, 1))     # McNemar z
    return float(np.mean(z > za))                    # drop detected, one direction (the other tail is negligible)
pw = sim_power(330, 0.7)
print(f"simulated power, paired, rho 0.7, n 330: {pw:.2f}")
assert 0.75 < pw < 0.86

# Example in the text: 160 and 150 passes out of 200 paired prompts, b = 15, c = 5
assert 160 - 15 + 5 == 150
z_mc = (15 - 5) / math.sqrt(15 + 5)
pool_e = (160 + 150) / 400
z_unp = (160 / 200 - 150 / 200) / math.sqrt(pool_e * (1 - pool_e) * 2 / 200)
print(f"example: McNemar z = {z_mc:.2f} (p = {2*stats.norm.sf(z_mc):.3f}); unpaired z = {z_unp:.2f} (p = {2*stats.norm.sf(z_unp):.2f})")
assert round(z_mc, 2) == 2.24 and round(z_unp, 1) == 1.2
# follow-up: a 2-point drop needs about (5/2)^2 times more prompts per version
n2 = (za + zb) ** 2 * (0.80 * 0.20 + 0.78 * 0.22) / 0.02 ** 2
print("unpaired n per version for 80% -> 78%:", math.ceil(n2))
assert 6_500 < n2 < 7_200
```

**Output (my run):**
```text
z_alpha/2 = 1.960, z_power = 0.842, variance sum = 0.3475
unpaired n per version = 1091.0 -> 1091; suite of 200 is 18% of that
power of a 200-prompt unpaired comparison: 0.22
one-sided n per version: 860
rho 0.0: prompts needed (paired) = 1091
rho 0.5: prompts needed (paired) = 548
rho 0.7: prompts needed (paired) = 330
rho 0.9: prompts needed (paired) = 113
simulated power, paired, rho 0.7, n 330: 0.81
example: McNemar z = 2.24 (p = 0.025); unpaired z = 1.20 (p = 0.23)
unpaired n per version for 80% -> 78%: 6507
```

**Follow-ups:**
- What if the drop is 2 points, not 5? The sample grows with 1 / d^2: 2.5 times smaller d needs about 6 times more prompts: 80% to 78% needs about 6,500 per version unpaired (Code). Use paired design and a bigger, targeted suite.
- Why not just run each prompt 10 times? That averages out the model's sampling noise, but the 200 prompts remain 200 draws from the real mix, so the prompt-sampling error stays.
- What do you do when you cannot reach the sample size? State the minimum detectable drop for the suite you have, and use canary traffic and online metrics as a second check.

**Common mistakes:**
- Treating 200 prompts as enough because "it is a lot of prompts".
- Using an unpaired test on paired data (loses power) or a paired test on separate samples.
- Forgetting two-sided versus one-sided.
- Reporting "no significant difference" as "no difference".

### Q43 ⭐⭐ 🔴 An LLM judge costs 0.01 per scored answer, and production makes 1,000,000 answers a month at 0.012 each. A failure mode hits 2% of answers. Compute the cost of scoring a 5% random sample, the expected number of failures in that sample, and how many answers you must score to expect at least 100 failures, and say what you would sample instead of a plain random draw.
**Asked at:** LLM-evaluation pages (Manning's AI model evaluation chapter and an arXiv judge-bias study listing position, verbosity and self-preference bias, Arize and Langfuse pages on offline versus online evaluation, an LLM-as-judge survey); practitioner and academic material rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Judging a 5% random sample costs 500 a month (about 4% of the 12,000 generation spend) and catches about 1,000 failures, but 100 failures need only about 5,000 judged answers (cost 50, and about 5,850 to be 95% sure), so I would spend the budget on targeted, weighted samples and not only on a plain random draw.

**Clarifying questions:**
- Is the 2% failure rate known or a guess? It sets every count here; if it is really 0.5%, you need four times the sample for the same number of failures.
- What is the goal: estimate the overall failure rate, find examples to fix, or alert on a rise? Each needs a different sample.
- How good is the judge (agreement with humans, bias)? A cheap judge that is wrong 15% of the time gives a biased failure count; I would calibrate it on human labels.
- Which signals exist to target (low model confidence, user thumbs-down, long answers, new intents, a flagged topic)? Targeting needs a signal that correlates with failure.
- Is 0.01 per scored answer all-in (tokens, retries, storage)? A judge call often uses long prompts.

**Approach:**
1. Cost of 5%: 1,000,000 x 5% = 50,000 answers x 0.01 = 500. Generation spend is 1,000,000 x 0.012 = 12,000, so the judge is 4.2% on top. Cheap enough to run continuously.
2. Expected failures in that sample: 50,000 x 2% = 1,000, which is plenty to estimate the rate (95% half-width about 0.12 points).
3. For at least 100 failures: 100 / 0.02 = 5,000 answers, cost 50. But 5,000 is the expectation, not a guarantee: the chance of actually seeing 100 or more is about 51%. For 95% confidence of at least 100 you need about 5,841 answers (cost about 58). This is the number to quote if someone needs the failure examples to exist.
4. Do not sample only at random. Use stratified or targeted sampling: oversample strata likely to fail (low-confidence answers, thumbs-down, new intents, long contexts, languages with weaker quality, risky topics), plus a smaller uniform sample for an unbiased overall rate. Weight each stratum by its share of traffic when estimating the total (Code, invented strata: 10% of traffic with a 12.5% failure rate and the rest 0.83%).
5. With the same 5,000 judged answers, a 50/50 split across those two strata finds about 333 failures against 100 for uniform, which gives far more examples to analyse, and the weighted estimate stays unbiased (std error 0.0018 against 0.0020, only a small gain for the overall rate).
6. Add a verifier layer: sample 100 or so judged answers each week for human review to track the judge's error, and calibrate the judge's counts with those labels.
7. Alert on the weighted rate with an interval, and on each stratum separately (a fall in one language can hide inside a good average).

**Metrics:**
- Judged failure rate = judged failures / judged answers (weighted by stratum share when sampling is unequal), with a 95% interval.
- Judge cost = judged answers x 0.01; as a share of generation spend = judge cost / (answers x 0.012).
- Failure examples collected per week (the count needed to learn something).
- Judge agreement with humans (for example, Cohen's kappa or accuracy on 100 labelled answers), measured regularly.

**Risks:**
- Judge bias (verbosity, position, self-preference) makes the counts wrong in a consistent direction.
- Targeting without weighting overstates the failure rate; always weight when strata are sampled unevenly.
- Selecting on the model's own confidence misses confident failures; keep a uniform slice to measure them.
- The 2% may move; the sample size must be recomputed.

**What the interviewer scores:**
- Strong: 500, 1,000 and 5,000 correct, and notes that 5,000 is the expectation, with about 51% chance of reaching 100. Weak: "5,000" with no uncertainty.
- Strong: proposes stratified or targeted samples with weights. Weak: "score everything" or "just 5%".
- Strong: mentions judge calibration against human labels. Weak: trusts the judge.
- Strong: relates cost to generation spend (4.2%). Weak: doesn't.

**Example:** (illustrative numbers) 5,000 judged answers drawn at random give about 100 failures: all you have to study. Drawing 2,500 from low-confidence answers (12.5% fail) and 2,500 from the rest (0.83% fail) gives about 333 failures. To report the overall rate you weight: 0.10 x (rate in the low-confidence stratum) + 0.90 x (rate in the rest). Weak answer: "Score 5% at random, it costs 500, fine." Strong answer: "Random 5% is affordable, but for finding failures I would oversample risky strata, weight the estimate, keep a small uniform slice, and calibrate the judge on human labels."

**Code:**
```python
import math
import numpy as np
from scipy import stats

# Illustrative numbers from the prompt
judge, answers, gen, rate = 0.01, 1_000_000, 0.012, 0.02
sample = 0.05 * answers
cost = sample * judge
print(f"5% sample = {sample:.0f} answers, judge cost {cost:.0f}; generation spend {answers*gen:.0f}; judge is {cost/(answers*gen):.1%} of it")
assert sample == 50_000 and round(cost) == 500 and round(answers * gen) == 12_000 and round(cost / (answers * gen), 3) == 0.042

exp_fail = sample * rate
print("expected failures in the 5% sample:", exp_fail)
assert round(exp_fail) == 1_000

n_exp = 100 / rate
print(f"to expect 100 failures: {n_exp:.0f} answers, cost {n_exp*judge:.0f}; P(actually >= 100) = {stats.binom.sf(99, int(n_exp), rate):.2f}")
assert n_exp == 5_000 and round(n_exp * judge) == 50
assert 0.50 < stats.binom.sf(99, 5000, rate) < 0.53

n = next(n for n in range(5000, 8000) if stats.binom.sf(99, n, rate) >= 0.95)
print(f"to be 95% sure of at least 100 failures: {n} answers, cost {n*judge:.1f}")
assert n == 5841

# Rate precision from a plain sample (Wilson half-width) at 5,000 and 50,000
def hw(k, m, z=1.96):
    p = k / m; d = 1 + z * z / m
    return z * math.sqrt(p * (1 - p) / m + z * z / (4 * m * m)) / d
print("95%% half-width on the rate: n=5,000 -> %.2f points; n=50,000 -> %.2f points" % (100 * hw(100, 5000), 100 * hw(1000, 50000)))
assert 0.38 < 100 * hw(100, 5000) < 0.42 and 0.11 < 100 * hw(1000, 50000) < 0.13

# Stratified sampling (invented strata): 10% of traffic is low-confidence with failure rate 12.5%, the rest 0.8333%, overall 2%
wA, rA = 0.10, 0.125
wB = 1 - wA; rB = (rate - wA * rA) / wB
assert abs(wA * rA + wB * rB - rate) < 1e-12
budget = 5_000
unif_found = budget * rate
strat_found = 2_500 * rA + 2_500 * rB
se_unif = math.sqrt(rate * (1 - rate) / budget)
se_strat = math.sqrt(wA**2 * rA * (1 - rA) / 2_500 + wB**2 * rB * (1 - rB) / 2_500)
print(f"same budget of {budget}: failures found uniform {unif_found:.0f} vs 50/50 stratified {strat_found:.0f}; std error of overall rate {se_unif:.4f} vs {se_strat:.4f}")
assert round(strat_found) == 333 and se_strat < se_unif
# the weighted estimate stays unbiased (check by simulation, seeded)
rng = np.random.default_rng(5)
est = [wA * rng.binomial(2_500, rA) / 2_500 + wB * rng.binomial(2_500, rB) / 2_500 for _ in range(4000)]
print("simulated mean of weighted estimate: %.4f, sd %.4f" % (np.mean(est), np.std(est)))
assert abs(np.mean(est) - rate) < 0.0005 and abs(np.std(est) - se_strat) < 0.0003
assert answers * judge == 10_000 and round(answers * judge / (answers * gen), 2) == 0.83
```

**Output (my run):**
```text
5% sample = 50000 answers, judge cost 500; generation spend 12000; judge is 4.2% of it
expected failures in the 5% sample: 1000.0
to expect 100 failures: 5000 answers, cost 50; P(actually >= 100) = 0.51
to be 95% sure of at least 100 failures: 5841 answers, cost 58.4
95% half-width on the rate: n=5,000 -> 0.39 points; n=50,000 -> 0.12 points
same budget of 5000: failures found uniform 100 vs 50/50 stratified 333; std error of overall rate 0.0020 vs 0.0018
simulated mean of weighted estimate: 0.0200, sd 0.0018
```

**Follow-ups:**
- Why not score 100%? It would cost 1,000,000 x 0.01 = 10,000 a month, 83% on top of the 12,000 generation spend, and add judge latency if run inline. Sampling is the cheaper default; score everything only for high-risk intents.
- How do you catch a failure mode that is only 0.1% of answers? A 5% sample has 50 of them; to see the rate properly use targeted sampling on the signals tied to that mode, or rule-based detectors on all traffic.
- What if the judge is wrong 10% of the time? Observed failure rate = true rate x sensitivity + (1 - true rate) x false-positive rate; estimate those on human labels and correct the count.

**Common mistakes:**
- Treating "expected 100" as "at least 100".
- Reporting a stratified sample's raw failure share as the production rate.
- Never checking the judge against humans.
- Sampling only thumbs-down answers (they are biased toward vocal users).

### Q44 ⭐ 🟢 On 200 prompts that contain a false premise, an assistant corrects the premise in 90 (45%) and goes along with it in the rest. After a prompt change it corrects 140 of the same 200 (70%). Compute the change in percentage points and the number of extra corrected prompts, and say why a thumbs-up signal might reward the old behaviour.
**Asked at:** Eval-contamination and feedback-bias material (a tianpan post on eval-set contamination and production leakage, an arXiv paper on contamination in closed-source LLMs, an RLHF survey and the sycophancy literature summarised in secondary pages); research and practitioner pages rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Correction of false premises rose from 45% to 70%, a gain of 25 percentage points (50 extra prompts of 200, a 56% relative rise), which is large compared with noise, but a thumbs-up signal can reward the old, agreeable behaviour, so I would judge it on labelled outcomes and not on thumbs.

**Clarifying questions:**
- Who decided that a prompt "corrects the premise", and how (human labels, a rubric, an LLM judge)? Both measurements must use the same labelling.
- Were the 200 prompts used while tuning the prompt change? If yes, the 70% is optimistic. I want a held-out set.
- Is the 200 a mix of easy and hard false premises, and does it cover the real mix? A premise like "since the 2030 Olympics" is easy to catch; subtle ones are not.
- What happens on prompts with a true premise? A prompt that corrects everything would score 100% here and be useless.
- What do users see after a correction: a short, polite fix and the answer, or a refusal to proceed?

**Approach:**
1. Compute the change: 90 / 200 = 45%, 140 / 200 = 70%. Difference 25 percentage points (not "25%"); extra corrected prompts 140 - 90 = 50; relative change 25 / 45 = 56%.
2. Check noise. Wilson 95% intervals: 38.3% to 51.9% before and 63.3% to 75.9% after; they do not overlap. Because the same 200 prompts were used, do a paired test: look at how many changed in each direction (invented split: 10 corrected before but not after, 60 the reverse; 90 - 10 + 60 = 140; McNemar z about 6). Report the real split from your run. Even unpaired, z is about 5.1.
3. Check for harm: run the same change on true-premise prompts (the model should not "correct" correct statements) and on ordinary prompts (no drop in helpfulness, no extra refusals).
4. Check generalisation: hold out a set the prompt change never saw, written by different people, and include subtle premises; 200 prompts of one style can mislead.
5. Explain the thumbs-up issue: users often prefer answers that agree with them (sycophancy), so correcting a premise can earn fewer thumbs-up, even when it is the better answer. An optimiser or dashboard that tracks thumbs would prefer the old behaviour. In the Code (invented rates: 70% thumbs-up when the answer goes along, 55% when it corrects) the thumbs-up rate falls from 63.25% to 59.5% while correction rises 25 points.
6. Decision metrics: correction rate on labelled false-premise prompts, false-correction rate on true-premise prompts, and an expert-reviewed sample of answer quality; use thumbs only as a secondary, biased signal, and look at who clicks (thumbs are given by a small, non-random share of users).

**Metrics:**
- Premise-correction rate = prompts whose answer corrects the false premise / false-premise prompts (45% and 70%).
- Change in percentage points = rate after - rate before (25); extra corrected = count after - count before (50).
- False-correction rate = true-premise prompts wrongly corrected / true-premise prompts (guardrail).
- Thumbs-up rate = thumbs-up / answers rated (with the response rate stated); judge agreement with humans on a sample.

**Risks:**
- Overfitting to the 200 prompts (the same set that guided the change).
- Over-correction: the model challenges true statements or lectures users.
- Judge bias: an LLM judge may count a hedge ("some people say...") as a correction.
- Thumbs-up bias: a feedback signal that favours agreement can pull a later fine-tune back toward sycophancy.

**What the interviewer scores:**
- Strong: 25 points and 50 extra, and distinguishes points from percent (56% relative). Weak: "25% better".
- Strong: asks for the true-premise guardrail and a held-out set. Weak: celebrates the number.
- Strong: explains why thumbs may reward agreeing (users like confirmation) and uses labelled outcomes. Weak: "thumbs-up is the user's voice, trust it".
- Strong: pairs the comparison on the same prompts. Weak: treats them as separate samples.

**Example:** (illustrative numbers) A user writes "Since Mumbai is the capital of India, how do I plan a trip to the capital?" (invented false premise). Old answer: "Great, here is a three-day plan for Mumbai..." Weak review: "User gave it a thumbs-up, so keep it." Strong review: "The old answer goes along with the premise and so it fails the correction check. The new one says 'that premise is not right' and then answers usefully. Thumbs-up is lower for it, but it is the better answer; I judge on the labelled correction rate and the true-premise guardrail."

**Code:**
```python
import math
from scipy import stats

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

# Illustrative numbers from the prompt
n, k0, k1 = 200, 90, 140
r0, r1 = k0 / n, k1 / n
print(f"corrected: {r0:.0%} -> {r1:.0%}; change {100*(r1-r0):.0f} percentage points; extra corrected prompts {k1-k0}; relative change {r1/r0-1:.0%}")
assert r0 == 0.45 and r1 == 0.70 and round(100 * (r1 - r0)) == 25 and k1 - k0 == 50

lo0, hi0 = wilson(k0, n); lo1, hi1 = wilson(k1, n)
print(f"Wilson 95%: before [{lo0:.3f}, {hi0:.3f}], after [{lo1:.3f}, {hi1:.3f}]")
assert hi0 < lo1   # intervals do not overlap

# Paired view on the same 200 prompts. Net change +50 = c - b where b = corrected before but not after, c = the reverse.
# Invented split of the discordant prompts: b = 10, c = 60.
b, c = 10, 60
assert k0 - b + c == k1 and c - b == 50
z = (c - b) / math.sqrt(b + c)
print(f"McNemar z = {z:.2f}, two-sided p = {2*stats.norm.sf(z):.1e} (b = {b}, c = {c})")
assert z > 5
# Without the paired counts, the unpaired comparison is already clear for a 25-point gain
pool = (k0 + k1) / (2 * n)
zu = (r1 - r0) / math.sqrt(pool * (1 - pool) * 2 / n)
print(f"unpaired z = {zu:.2f}")
assert zu > 5

# Why thumbs-up can reward the old behaviour. Invented rates: users thumbs-up 70% of answers that go along
# with their premise and 55% of answers that correct it.
up_agree, up_correct = 0.70, 0.55
before = r0 * up_correct + (1 - r0) * up_agree
after = r1 * up_correct + (1 - r1) * up_agree
print(f"thumbs-up rate before {before:.4f}, after {after:.4f}: change {100*(after-before):.2f} points while correction rose 25 points")
assert round(before, 4) == 0.6325 and round(after, 4) == 0.595 and after < before
```

**Output (my run):**
```text
corrected: 45% -> 70%; change 25 percentage points; extra corrected prompts 50; relative change 56%
Wilson 95%: before [0.383, 0.519], after [0.633, 0.759]
McNemar z = 5.98, two-sided p = 2.3e-09 (b = 10, c = 60)
unpaired z = 5.06
thumbs-up rate before 0.6325, after 0.5950: change -3.75 points while correction rose 25 points
```

**Follow-ups:**
- How would you stop the thumbs signal from training the model to agree? Do not use raw thumbs as a reward; weight by labelled correctness, add false-premise examples to the training or eval mix, and audit the feedback with human review.
- Is 200 prompts enough? For a 25-point change, yes; for a 3-point change, no (see Q42 for the sample size).
- What if the model corrects too often? Measure the false-correction rate on true-premise prompts and add them to the regression suite.

**Common mistakes:**
- Calling a 25-point rise "25% better".
- Testing only on the prompts used to tune the change.
- Ignoring the true-premise side of the trade.
- Treating thumbs-up as ground truth.

### Q45 ⭐ 🟢 A provider will retire the model snapshot you use in 90 days. You have a 2,000-prompt regression suite, want 3 runs per candidate to handle sampling noise, and a candidate costs an illustrative 0.0153 per call. Compute the evaluation cost for one candidate, and describe the migration plan, including what you do if the new version regresses on some prompts.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to model-upgrade and deprecation topics in LLMOps material; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened

**Say this first (1 line):** One candidate costs 2,000 x 3 x 0.0153 = 91.80 (illustrative), which is tiny next to the risk, so I would run every serious candidate on the full suite and spend my time on the plan: freeze the suite, compare prompt by prompt, canary, and keep a fallback.

**Clarifying questions:**
- Is 0.0153 the generation cost only, or does it include the judge call? If answers are scored by a model judge, each run costs more, so the number can double.
- What exactly is the "snapshot" and is the replacement named? It sets whether I test one candidate or three.
- Is the suite a sample of real traffic, or hand-written prompts? Real traffic tells me about users. Hand-written prompts tell me about known failures.
- What is the pass rule per prompt (exact match, rubric, judge)? It decides how noisy a single run is.
- Are there hard requirements (JSON format, refusal behaviour, latency, price) that can fail even when answer quality is fine?
- What is the fallback if no candidate passes by day 90 (stay on the old model through an extension, or ship a degraded feature)?

**Approach:**
1. Cost. Calls = 2,000 prompts x 3 runs = 6,000. Cost = 6,000 x 0.0153 = 91.80. Three candidates = 275.40. All numbers are illustrative.
2. Day 0 to 7: freeze the suite and the scoring rules. Record the old model's results (3 runs) as the baseline. Add 100 or so prompts from recent real traffic so the suite is not stale.
3. Day 8 to 30: run each candidate with 3 runs at the production settings. Use the majority verdict per prompt, and flag prompts that disagree across runs as flaky.
4. Compare paired, prompt by prompt. Count prompts that got worse and prompts that got better. Do not look only at the total pass rate.
5. Read every regression by hand, grouped by cause: format drift, refusals, longer or shorter answers, changed tone, a real quality loss.
6. Fix what can be fixed: edit the prompt (re-test the old model too, so the comparison stays fair), add examples, tighten the output schema. Keep a prompt version per model.
7. Day 31 to 60: shadow traffic or a small canary (for example 5% of traffic). Watch user-facing metrics and cost, not just the suite.
8. Day 61 to 75: ramp to 100% behind a flag. Keep the old model callable until the retirement date.
9. Day 76 to 90 is the buffer. Never plan to finish on day 89.

**What if the new version regresses on some prompts:**
- If the flipped prompts are few and fixable by a prompt change, fix and re-run only those prompts plus a random sample of the rest (cheap).
- If a whole category regresses, route that category to another model or keep a rule-based path, and ship the rest.
- If the regression is real and no candidate fixes it, tell the product owner early, with the list of prompts, and ask for an extension or accept a degraded feature. Do not hide it in an average.

**Metrics:**
- Paired result per prompt: pass on baseline majority and pass on candidate majority. Counts: better = fail to pass, worse = pass to fail.
- Net change = (better - worse) / 2,000. Sign test on the flipped prompts only.
- Flaky rate = prompts whose 3 runs disagree / 2,000.
- Guardrails: format-valid rate, refusal rate, latency p95, cost per call, and the pass rate on the safety and high-value slices separately.

**Risks:**
- A suite pass rate that moves by 0.5 points is inside noise for a suite this size; do not decide on it.
- The suite may not cover what users now ask. Add fresh traffic.
- Changing the prompt for the new model and comparing against an untuned old prompt gives a fake win.
- Behaviours that are not in the suite (tone, length, safety) can shift. Add a small manual review.
- Pricing or rate limits of the new model may break the budget even if quality is fine.

**What the interviewer scores:**
- Strong: computes 91.80 and says it is small, then plans around risk. Weak: stops at the number or says "the cost is high".
- Strong: paired prompt-level comparison and reading regressions. Weak: compares two overall percentages.
- Strong: a dated plan with a buffer, canary and fallback. Weak: "swap it and watch".
- Strong: knows what 3 runs do and do not do (flags flaky prompts, does not remove noise).

**Example:** Illustrative. Suite 2,000, baseline majority pass 1,640 (82.0%), candidate 1,650 (82.5%). Flipped prompts: 60 worse, 70 better. Sign test p = 0.43, so the 0.5-point gain is not evidence. Weak: "The new model scores higher, ship it." Strong: "The totals are close, but 60 prompts got worse. I will read those 60, and if they cluster in JSON output I fix the schema prompt, re-test, and canary at 5% before moving everyone."

**Code:**
```python
import random, math
random.seed(7)
prompts, runs, per_call = 2000, 3, 0.0153
calls = prompts * runs
cost = calls * per_call
print(f"calls per candidate = {calls}, cost = {cost:.2f} (illustrative units)")
assert calls == 6000 and abs(cost - 91.80) < 1e-9
print(f"3 candidates = {3*cost:.2f}; baseline re-run on same suite = {cost:.2f}")
assert abs(3*cost - 275.40) < 1e-9
# sign test on prompts whose majority-of-3 verdict flipped (invented counts)
worse, better = 60, 70
n = worse + better
def binom_two_sided(k, n):
    pm = lambda i: math.comb(n, i) / 2**n
    p = sum(pm(i) for i in range(n + 1) if pm(i) <= pm(k) + 1e-15)
    return min(1.0, p)
p = binom_two_sided(min(worse, better), n)
print(f"flipped prompts: {worse} worse, {better} better, exact sign-test p = {p:.3f}")
assert 0.4 < p < 0.5
# how noisy is one run? simulate 2000 prompts: 1700 always pass, 100 always fail, 200 flaky (pass 50%)
def run_pass_count():
    return 1700 + sum(random.random() < 0.5 for _ in range(200))
one = [run_pass_count() for _ in range(2000)]
sd = (sum((x - sum(one)/len(one))**2 for x in one) / (len(one)-1)) ** 0.5
print(f"one-run pass count sd = {sd:.1f} prompts = {sd/20:.2f} points (flaky prompts only)")
assert 6 < sd < 8.5
# flaky prompts flagged: disagree across 3 runs
flag = 1 - 2 * 0.5**3
print(f"a 50% flaky prompt shows disagreement across 3 runs with prob {flag:.2f}")
assert flag == 0.75
# at most 90 days: schedule
print("day 0-7 freeze suite; 8-30 candidates; 31-60 canary; 61-75 full ramp; 76-90 buffer")
```

**Output (my run):**
```
calls per candidate = 6000, cost = 91.80 (illustrative units)
3 candidates = 275.40; baseline re-run on same suite = 91.80
flipped prompts: 60 worse, 70 better, exact sign-test p = 0.430
one-run pass count sd = 7.1 prompts = 0.35 points (flaky prompts only)
a 50% flaky prompt shows disagreement across 3 runs with prob 0.75
day 0-7 freeze suite; 8-30 candidates; 31-60 canary; 61-75 full ramp; 76-90 buffer
```

**Follow-ups:**
- *Why 3 runs and not 1 or 10?* One run cannot separate a real regression from luck on a flaky prompt. Three gives a majority and flags disagreement, at 3x cost. Ten is rarely worth it unless the suite is small and decisions are close.
- *Can you run the cheap check first?* Yes: a 200-prompt random subset first to drop bad candidates, then the full suite on survivors.
- *What if the old model is retired earlier than promised?* Keep a second provider or a tested fallback so the feature degrades, not breaks. Related: Book 2 Part 9 Q4 ("What is LLM-as-a-judge?") for scoring if you use a judge.

**Common mistakes:**
- Comparing only the total pass rate.
- Treating one run as the truth.
- Tuning the prompt for the new model only.
- Forgetting judge cost, format and latency checks.
- Planning to finish on the last day.

### Q46 ⭐ 🟡 A judge model version is updated, and the same 300 saved answers are rescored: the mean score falls from 4.2 to 3.8 on a 5-point scale, and 90 of the 300 answers (30%) change by one point or more. How do you tell judge drift from product drift, and how do you keep a time series of scores comparable?
**Asked at:** LLM-evaluation pages (Manning's AI model evaluation chapter and an arXiv judge-bias study listing position, verbosity and self-preference bias, Arize and Langfuse pages on offline versus online evaluation, an LLM-as-judge survey); practitioner and academic material rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened

**Say this first (1 line):** The answers did not change, only the judge did, so the 0.4 drop is judge drift by construction; product drift is a separate question I answer with an anchor set, and I keep the series comparable by pinning judge versions and bridging every change.

**Clarifying questions:**
- Were the 300 answers exactly the saved ones (same text, same prompts)? If yes, product drift is ruled out for this comparison.
- Are scores integers on 1 to 5? If so, "changed by one point or more" just means "changed", and I can read the full change distribution.
- Is the judge prompt, temperature and rubric identical, with only the model version different? If the prompt also changed, I cannot say which caused it.
- Do we have human labels on part of the 300? They tell me which judge is closer to truth.
- Is the dashboard used for decisions (release gates), or only for trends? Gates need a harder fix.

**Approach:**
1. Say what the experiment shows. Same answers, two judges: mean 4.2 to 3.8, a shift of -0.4. All of that is judge change, not product change.
2. Check the size of the effect. A shift of -0.4 on 300 answers is far larger than noise if the paired changes behave like the invented ones below (95% CI -0.475 to -0.325).
3. Check judge noise. Re-run the old judge twice on the same 300 answers. If it changes only a few answers and the mean stays put, judge noise is small and the shift is a real new-judge effect.
4. Look at the shape of the change. All answers shift a bit (a harsher scale) or a subset shifts a lot (the new judge penalises something, such as length or missing citations). Read 20 of the 90 changed answers.
5. Check against humans. Have people label 100 of the 300 blind. The judge that agrees better (kappa or agreement rate) is closer to the truth; neither is "correct" by default.
6. Keep the series comparable. Pin the judge version in every record. When the judge changes: run both judges for an overlap period, rescore a fixed anchor set with both, and report a break in the series with a bridge (offset or mapping).
7. Separate product drift. Keep a frozen anchor set of answers (fixed text) scored every week: if the anchor mean moves, the judge moved. Score fresh traffic on the same judge: if fresh moves and the anchor does not, the product moved.

**Metrics:**
- Judge shift = mean(new judge score) - mean(old judge score) on identical answers, with a paired CI.
- Changed share = answers with any change / 300 = 90/300 = 30%.
- Judge test-retest = answers that differ across two runs of the same judge / 300.
- Agreement with humans = exact agreement or Cohen's kappa (see Book 2 Part 9 Q6) on a labelled subset.
- Guardrails: score by slice (length, topic, language), so a shift that hits one slice is not hidden.

**Risks:**
- Silent judge version changes at the provider. Pin versions where possible and record them; check the anchor set weekly.
- Bridging with a single offset hides a non-uniform shift (it may hit long answers more).
- Overfitting to the anchor set if the product team sees it.
- Judge bias (position, verbosity, self-preference; see Book 2 Part 9 Q5) may differ between versions.

**What the interviewer scores:**
- Strong: notes that identical answers mean the change is the judge, and gives the anchor-set design. Weak: asks whether quality really fell.
- Strong: asks for judge test-retest and a human check. Weak: trusts the newer judge because it is newer.
- Strong: version pinning, overlap period, bridge, and a marked break in the chart. Weak: continues the line as if nothing happened.
- Bonus: notices that on integer scores, 90 answers moving by exactly one point would give only -0.3, so some answers moved by two or more.

**Example:** Illustrative. Last month, old judge: 4.2. Rescoring the same 300 with the new judge: 3.8, so offset -0.4. This week's fresh traffic scored by the new judge: 3.9. Weak: "Score fell from 4.2 to 3.9, quality is down." Strong: "On the old scale this week is about 4.3, so the product is flat to slightly better; the drop is the judge. I will plot the new judge from now on with a break, and keep both scores for a month."

**Code:**
```python
import random, math
random.seed(11)
n = 300
# invented per-answer score changes that match the prompt: 210 unchanged, 90 changed
# (a) all 90 moved down: 60 by -1, 30 by -2
d = [0]*210 + [-1]*60 + [-2]*30
assert len(d) == n and sum(d) == -120
print("mean change =", sum(d)/n)
assert abs(sum(d)/n - (-0.4)) < 1e-12
changed = sum(1 for x in d if x != 0)
print("answers changed:", changed, f"({changed/n:.0%})")
assert changed == 90 and changed/n == 0.30
# minimum number of changed answers needed for a -0.4 mean if scores are integers 1..5: each answer can fall at most 4
print("min answers with a change, if each fell by at most 4:", math.ceil(120/4))
# if all 90 moved down by exactly 1, mean change would be:
print("mean change if the 90 moved down by 1 only:", -90/n)
assert -90/n == -0.3
# so a mean drop of 0.4 needs bigger moves or more than 90 answers (given integer scores)
m = sum(d)/n; sd = (sum((x-m)**2 for x in d)/(n-1))**0.5
se = sd/math.sqrt(n)
print(f"sd of paired change {sd:.3f}, 95% CI of mean shift {m-1.96*se:.3f} to {m+1.96*se:.3f}")
assert m + 1.96*se < 0
# test-retest of the OLD judge on the same 300 answers: invented, 25 answers differ by one point, balanced
d0 = [0]*275 + [1]*12 + [-1]*13
print("old judge rerun mean change:", sum(d0)/n)
assert abs(sum(d0)/n) < 0.01
# bridge: this week's product scored with the NEW judge
new_week = 3.9
offset = 3.8 - 4.2
bridged = new_week - offset
print(f"new-judge score {new_week}; on old-judge scale {bridged:.1f}; product change vs 4.2 = {bridged-4.2:+.1f}")
assert abs(bridged - 4.3) < 1e-9
print(f"naive reading: {new_week-4.2:+.1f} (looks like a drop, but it is a gain after bridging)")
```

**Output (my run):**
```
mean change = -0.4
answers changed: 90 (30%)
min answers with a change, if each fell by at most 4: 30
mean change if the 90 moved down by 1 only: -0.3
sd of paired change 0.664, 95% CI of mean shift -0.475 to -0.325
old judge rerun mean change: -0.0033333333333333335
new-judge score 3.9; on old-judge scale 4.3; product change vs 4.2 = +0.1
naive reading: -0.3 (looks like a drop, but it is a gain after bridging)
```

**Follow-ups:**
- *Which judge is right?* Neither until humans label a sample. Pick the one that agrees better and is stable on retest.
- *Can you just rescore all history with the new judge?* Often yes if cost allows and answers were saved; that is the cleanest way to keep one series. Save answers, not only scores.
- *What if you cannot keep the old judge?* Keep the frozen anchor set and human labels, and fit the bridge on them.

**Common mistakes:**
- Calling a judge change a product regression (or the reverse).
- Not saving the answer text, so history cannot be rescored.
- Not recording the judge version.
- Fixing with one offset without checking slices.
- Using the same anchor set for tuning the product.

### Q47 ⭐ 🟡 A document-QA test places the answer passage at the start, middle or end of a long context, with 100 questions in each position, and accuracy is 92%, 71% and 85% respectively. Compute overall accuracy and the middle-versus-start gap in points, and say what you would change about how retrieved passages are ordered or whether to use long context at all.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to long-context versus RAG topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened

**Say this first (1 line):** Overall accuracy is (92 + 71 + 85) / 3 = 82.7%, the middle is 21 points worse than the start, that gap is far too big for noise, so I would put the best passages first (and last), send fewer passages, and use long context only when retrieval truly cannot find the answer.

**Clarifying questions:**
- Are the 100 questions in each position the same questions moved around, or different questions? Same questions give a paired test and a cleaner result.
- How long is the context, and how many distractor passages are there? The effect depends on length and clutter.
- Which model and settings? The pattern can differ between models and versions, so I would re-test on mine rather than assume (this is a test I would run, not a general fact).
- Is accuracy graded by a judge or exact match? Grader noise adds to the spread.
- In production, where does the answer passage usually fall after retrieval and reranking? The test only matters if the real distribution looks like it.

**Approach:**
1. Overall accuracy = mean of the three, because each position has 100 questions: (92 + 71 + 85) / 3 = 82.67%. If the production mix is not equal, weight by the real mix.
2. Gap, middle versus start = 92 - 71 = 21 points.
3. Is it real? Two-proportion z = 3.97 and a 95% CI of about 10.6 to 31.4 points (unpaired approximation). Yes, it is real. Start versus end (7 points, z = 1.56, CI -1.8 to 15.8) is not separable at n = 100.
4. Change the pipeline: rerank, then put the strongest passages at the start and the second strongest at the end, and weak ones in the middle. Cut the number of passages (top 5 to 8 instead of 30).
5. Compare against long context on cost. Illustrative: 100,000 tokens at 3 per million input tokens is 0.300 per call. Retrieval with 4,000 tokens is 0.012, 25 times less.
6. Use long context only for tasks that need the whole document (summarise, cross-reference many sections) or when recall of retrieval is too low. If used, repeat the test at the real context length, and put the question and key instructions where the model attends best (test it; do not assume).
7. Re-run the same test after the change, and also test with the answer passage ranked second and third by the reranker, since in production it is not always first.

**Metrics:**
- Accuracy by position = correct answers at that position / 100.
- Position gap = accuracy(start) - accuracy(middle), in points, with a CI.
- End-to-end answer accuracy on real retrieved contexts, split by the rank of the gold passage.
- Cost per correct answer = cost per call / accuracy. Guardrail: latency and context length.

**Risks:**
- The test puts exactly one answer passage in a sea of distractors; real questions may need two passages.
- Position effects can change with model version. Treat the numbers as a regression test, not a law.
- Reordering helps only if the reranker is good; a wrong first passage is worse than a middle one.
- Cutting passages can drop recall.

**What the interviewer scores:**
- Strong: correct 82.7% and 21 points, plus a significance check. Weak: says "middle is lower" without sizes.
- Strong: a concrete reordering and fewer-passages plan, tested. Weak: "use a bigger context window".
- Strong: cost comparison between long context and retrieval. Weak: ignores cost.
- Strong: notes the 7-point start-versus-end gap is not clearly real at n = 100. Weak: calls it a U-shape as a fact.

**Example:** Illustrative. The best passage is at the start 70% of the time and at the end 30% of the time after reranking: expected accuracy 0.7 x 92% + 0.3 x 85% = 89.9%, versus 82.7% with a random spread. This is a planning number from the test, not a promise. Weak: "I would use a 1M-token model so it fits everything." Strong: "I would rerank, put the top passage first and the next last, send five passages not thirty, and keep long context for tasks that really need the whole document, because it is 25 times costlier per call in my example."

**Code:**
```python
import math
acc = {"start": 0.92, "middle": 0.71, "end": 0.85}
n = 100
overall = sum(acc.values()) / 3
print(f"overall = {overall:.4f}")
assert abs(overall - 0.826667) < 1e-5
gap = acc["start"] - acc["middle"]
print(f"start - middle gap = {gap*100:.0f} points")
assert round(gap*100) == 21
def z2(p1, p2, n1=n, n2=n):
    se = math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    return (p1-p2)/se, se
z, se = z2(0.92, 0.71)
lo, hi = gap - 1.96*se, gap + 1.96*se
print(f"gap 95% CI (unpaired normal approx): {lo*100:.1f} to {hi*100:.1f} points, z = {z:.2f}")
assert z > 3.5 and lo > 0.08
z_e, se_e = z2(0.92, 0.85)
print(f"start - end gap = 7 points, z = {z_e:.2f}, 95% CI {(0.07-1.96*se_e)*100:.1f} to {(0.07+1.96*se_e)*100:.1f}")
assert z_e < 1.96
# illustrative cost of long context vs retrieval at 3 per million input tokens
price = 3
ctx_tokens, rag_tokens = 100_000, 4_000
c_long = ctx_tokens * price / 1e6; c_rag = rag_tokens * price / 1e6
print(f"per call: long context {c_long:.3f}, retrieved passages {c_rag:.3f}, ratio {c_long/c_rag:.0f}x")
assert abs(c_long-0.30) < 1e-12 and abs(c_rag-0.012) < 1e-12 and c_long/c_rag == 25
# placing best passage first or last, with a 70/30 mix of start/end for the top passage
mix = 0.7*acc["start"] + 0.3*acc["end"]
print(f"if top passage always sits at the start or end (70/30): expected accuracy {mix:.3f}")
assert abs(mix - 0.899) < 1e-9
```

**Output (my run):**
```
overall = 0.8267
start - middle gap = 21 points
gap 95% CI (unpaired normal approx): 10.6 to 31.4 points, z = 3.97
start - end gap = 7 points, z = 1.56, 95% CI -1.8 to 15.8
per call: long context 0.300, retrieved passages 0.012, ratio 25x
if top passage always sits at the start or end (70/30): expected accuracy 0.899
```

**Follow-ups:**
- *Why not just sort passages by score?* Descending sort puts the second-best passage at position 2, which can sit in the weak zone; a first-and-last layout is a test worth running.
- *Does prompt caching change the long-context cost argument?* It cuts the cost of repeated prefixes, so re-test the comparison; see Book 2 Part 1 Q24 (prefix caching).
- *Where can I read more about this effect?* Book 2 Part 1 Q19 ("What is the context window, and why is the effective context often shorter than the advertised one?").

**Common mistakes:**
- Averaging unequal groups without weights.
- Calling a 7-point gap at n = 100 a pattern.
- Assuming the effect holds for every model.
- Ignoring cost and latency of long context.
- Putting the question first or last without testing.

### Q48 ⭐ 🟡 Median agent tasks use 20,000 tokens, and of 100,000 tasks a month, 1,000 sit in the tail at 160,000 tokens while the other 99,000 are assumed to use exactly the median. Compute the tail's share of all tokens, and the saving from a hard per-task cap of 80,000 tokens as a share of all tokens, then say what happens to the tasks that hit the cap.
**Asked at:** Agent cost and loop-control material (solo.io and getmaxim pages on iteration and token ceilings for agent loops, a Towards Data Science article on agent token costs, an Exponent-sourced 2026 guide that mentions a candidate-reported agent-with-RAG token-cost design prompt); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened

**Say this first (1 line):** The tail is 1% of tasks but 7.5% of tokens (160 million of 2,140 million), the 80,000 cap saves 3.7% of all tokens, and that saving is real only if capped tasks end cleanly (partial result, handoff) and are not simply rerun.

**Clarifying questions:**
- Is the cap counted on input plus output tokens, summed across all steps of the agent loop? That is the number that matters.
- What do the tail tasks look like: stuck loops, repeated tool errors, or genuinely large jobs? It decides whether capping loses value.
- Does the 99,000 "exactly the median" hold? Real bodies have a mean above the median, which changes the shares (see the code).
- What is the cost of a failed task (retry by the user, human handling)? That sets what a cap really saves.
- Is there already a step limit or a time limit? A token cap is the backstop.

**Approach:**
1. Total tokens = 99,000 x 20,000 + 1,000 x 160,000 = 1,980 million + 160 million = 2,140 million.
2. Tail share = 160 / 2,140 = 7.48%, from 1% of tasks.
3. With an 80,000 cap, each tail task stops at 80,000 (assuming it would have run to 160,000). Saving = 1,000 x 80,000 = 80 million = 3.74% of all tokens.
4. Check the saving assumptions. If half the capped tasks are rerun from scratch up to the cap, the saving halves to 1.87%. If all are rerun, the saving is zero.
5. Design the cap: a soft warning at 50,000 (the agent must summarise its state and decide), and a hard stop at 80,000. Also set limits on steps, repeated identical tool calls, and wall-clock time.
6. What happens at the cap: stop cleanly, return what it has with a clear message, save a checkpoint (so a person or a second pass can continue), hand off to a human if the task matters, and log the trace for review.
7. Review the capped traces weekly. If they are loops, fix the agent. If they are legitimate big jobs, raise the cap for that task type only.

**Metrics:**
- Tail share of tokens = tokens in tasks above the cap threshold / all tokens = 7.48%.
- Saving share = (tokens that would have been used - tokens used under the cap) / all tokens = 3.74%.
- Cap-hit rate = capped tasks / all tasks (1% here). Resolution after cap: resolved by handoff / capped.
- Cost per successful task, not cost per task. Guardrail: success rate on tasks that would have finished between 80,000 and 160,000.

**Risks:**
- Some tail tasks are valuable (long research, large refactors); a flat cap kills them.
- A cap with no clean ending leaves half-done side effects (writes, emails). Make actions idempotent and safe to stop.
- Users retry capped tasks, so the money comes back.
- The cap hides loops instead of fixing them.

**What the interviewer scores:**
- Strong: 7.5% and 3.7%, with a comment that these are different questions. Weak: says "the cap removes the tail" (it removes half of it).
- Strong: describes what the user sees at the cap, and how side effects are handled. Weak: "just stop it".
- Strong: asks whether the tail is waste or value. Weak: assumes all tail tasks are failures.
- Strong: cost per success as the real metric.

**Example:** Illustrative blended price of 5 per million tokens. Total 10,700 per month, the cap saves 400. Weak: "Cap at 80,000 tokens and we cut the long tasks." Strong: "The cap saves 3.7% of tokens at best. I would warn at 50,000, stop at 80,000, return a partial result with a checkpoint, and look at the capped traces, because if they are loops the real fix is in the agent."

**Code:**
```python
tasks, tail_n, tail_tok, med = 100_000, 1_000, 160_000, 20_000
body_n = tasks - tail_n
total = body_n*med + tail_n*tail_tok
tail = tail_n*tail_tok
print(f"total tokens = {total:,}, tail tokens = {tail:,}")
assert total == 2_140_000_000 and tail == 160_000_000
share = tail/total
print(f"tail share of tokens = {share:.4f} while the tail is {tail_n/tasks:.1%} of tasks")
assert round(share, 4) == 0.0748
cap = 80_000
saved = tail_n*(tail_tok - cap)
print(f"tokens saved by cap = {saved:,} = {saved/total:.4f} of all tokens")
assert saved == 80_000_000 and round(saved/total, 4) == 0.0374
# retries of capped tasks as fresh runs reduce the saving
for r in (0.0, 0.5, 1.0):
    net = saved - r*tail_n*cap
    print(f"if {r:.0%} of capped tasks are rerun from scratch up to the cap: net saving {net:,.0f} = {net/total:.4f}")
assert saved - 1.0*tail_n*cap == 0
# illustrative money at a blended 5 per million tokens
price = 5
print(f"illustrative money: total {total*price/1e6:,.0f}, saving {saved*price/1e6:,.0f}")
assert total*price/1e6 == 10_700 and saved*price/1e6 == 400
# real distributions: if the other 99,000 average 25,000 instead of exactly 20,000
total2 = body_n*25_000 + tail
print(f"if the body averages 25,000: tail share {tail/total2:.4f}, cap saving {saved/total2:.4f}")
assert round(tail/total2, 4) == 0.0607 and round(saved/total2, 4) == 0.0304
low = tail_n*(tail_tok - 40_000)
print(f"cap at 40,000 saves {low:,} = {low/total:.4f}")
assert low == 120_000_000 and round(low/total, 3) == 0.056
```

**Output (my run):**
```
total tokens = 2,140,000,000, tail tokens = 160,000,000
tail share of tokens = 0.0748 while the tail is 1.0% of tasks
tokens saved by cap = 80,000,000 = 0.0374 of all tokens
if 0% of capped tasks are rerun from scratch up to the cap: net saving 80,000,000 = 0.0374
if 50% of capped tasks are rerun from scratch up to the cap: net saving 40,000,000 = 0.0187
if 100% of capped tasks are rerun from scratch up to the cap: net saving 0 = 0.0000
illustrative money: total 10,700, saving 400
if the body averages 25,000: tail share 0.0607, cap saving 0.0304
cap at 40,000 saves 120,000,000 = 0.0561
```

**Follow-ups:**
- *Why not a lower cap such as 40,000?* It saves more on paper (1,000 x 120,000 = 120 million, 5.6%) but starts killing normal large tasks. Pick it from the success rate by token use.
- *Does the median matter?* Only as a baseline. Tokens are driven by the mean, and the tail raises the mean.
- *What about cost caps per user?* Add one as a second layer; see Q49 in this part.

**Common mistakes:**
- Confusing the tail's share of tokens (7.5%) with the saving from capping it (3.7%).
- Forgetting retries.
- No clean ending at the cap.
- Judging the cap by cost per task instead of cost per success.

### Q49 ⭐ 🟡 A feature earns 5 per user per month. Of 100,000 users, 5,000 heavy users make 1,500 calls a month and the other 95,000 make 60 calls each, at an illustrative 0.012 per call. Compute total monthly cost, the cost per heavy user, and the margin on heavy users alone, and propose pricing or limits.
**Asked at:** LLM cost and routing pages (getmaxim cost and semantic-cache guides, tianpan and system-design.space pages on routing and cascades, a Towards Data Science article on saving tokens in agentic AI, a Towards AI piece on AI system-design interview patterns); practitioner material, no confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened

**Say this first (1 line):** Total cost is 158,400 a month against 500,000 revenue, so the feature is profitable overall (68% margin), but each heavy user costs 18 and pays 5, a loss of 13 each, so I would add included calls with metered overage rather than let 5% of users eat 57% of the cost.

**Clarifying questions:**
- Is 0.012 per call the same for heavy and light users? Heavy users often send longer inputs, so their real cost may be higher.
- Is the 5 per month the only revenue, or is the feature a retention tool for a bigger plan? That changes how much loss I accept.
- What is the usage pattern of the 1,500-call users: bots, power users, or one team sharing a login? Abuse needs a different fix than pricing.
- Are heavy users also the most loyal or the most vocal? Cutting them has a cost beyond margin.
- Can the heavy calls use a cheaper model, a cache, or a smaller prompt?

**Approach:**
1. Calls = 5,000 x 1,500 + 95,000 x 60 = 7.5 million + 5.7 million = 13.2 million.
2. Total cost = 13.2 million x 0.012 = 158,400. Revenue = 100,000 x 5 = 500,000. Margin = 341,600 (68.3%). All illustrative.
3. Cost per heavy user = 1,500 x 0.012 = 18.00. Margin per heavy user = 5 - 18 = -13.00 (-260% of their revenue). Heavy users in total: -65,000.
4. Light users: cost 0.72 each, margin 4.28, total 406,600. So light users carry the heavy ones.
5. Break-even usage at a price of 5 is 5 / 0.012 = 416.7 calls a month.
6. Options (illustrative):
   - A. Include 400 calls, charge 0.02 per call above that. A heavy user then pays 5 + 1,100 x 0.02 = 27 and costs 18, margin +9.00. Light users are unchanged.
   - B. Hard cap at 400 calls: heavy cost 4.80, margin 0.20. Safe but may annoy and churn power users.
   - C. Cheaper model for calls above 400 (assume 40% cheaper): heavy cost 12.72, still a loss of 7.72, so it is a helper and not a fix.
7. Choose A, with a soft warning at 80% of the allowance, plus rate limits to stop abuse. Run it as an A/B test on new users first and watch churn.

**Metrics:**
- Margin per user = price paid - (calls x cost per call), reported by usage decile.
- Share of cost from the top 5% of users = 56.8% here.
- Gross margin = (revenue - cost) / revenue = 68.3%.
- Guardrails: churn of heavy users, upgrade rate, support tickets about limits, share of calls hitting a cap.

**Risks:**
- Heavy users may be your best advocates; a hard cap can cost more in churn than it saves.
- The 0.012 average may hide a heavier per-call cost for heavy users.
- Usage will shift once a price is visible (people may split across accounts).
- The margin looks fine overall; do not let that hide the cross-subsidy. If the heavy share grows from 5% to 10%, the loss doubles.

**What the interviewer scores:**
- Strong: three correct numbers (158,400; 18; -13) and notes the total margin is positive. Weak: "the feature loses money" (it does not, overall).
- Strong: includes calls plus overage, and tests it. Weak: "raise the price for everyone".
- Strong: asks whether per-call cost is really flat. Weak: never questions it.
- Strong: considers cost levers (cache, smaller model) as complements.

**Example:** Illustrative. Weak: "Heavy users lose us 13 each, cap them at 100 calls." Strong: "Overall we make 341,600, but the top 5% cost 57% of the spend and lose 13 each. I would include 400 calls, charge 0.02 over that, which turns a heavy user into +9, and test it before rollout."

**Code:**
```python
users, heavy, light = 100_000, 5_000, 95_000
price, per_call = 5.0, 0.012
calls = heavy*1500 + light*60
cost = calls*per_call
rev = users*price
print(f"calls = {calls:,}, cost = {cost:,.0f}, revenue = {rev:,.0f}, margin = {rev-cost:,.0f} ({(rev-cost)/rev:.1%})")
assert calls == 13_200_000 and abs(cost-158_400) < 1e-6 and rev == 500_000
h_cost = 1500*per_call; l_cost = 60*per_call
print(f"heavy user cost {h_cost:.2f}, margin {price-h_cost:.2f} ({(price-h_cost)/price:.0%} of revenue)")
print(f"light user cost {l_cost:.2f}, margin {price-l_cost:.2f}")
assert abs(h_cost-18) < 1e-9 and abs(price-h_cost+13) < 1e-9 and abs(l_cost-0.72) < 1e-9
print(f"heavy users: {heavy} x {price-h_cost:.0f} = {heavy*(price-h_cost):,.0f}; light users: {light*(price-l_cost):,.0f}")
assert abs(heavy*(price-h_cost) + 65_000) < 1e-6 and abs(light*(price-l_cost) - 406_600) < 1e-6
print(f"heavy share of calls (and cost) = {heavy*1500/calls:.1%}, share of users = {heavy/users:.0%}")
assert round(heavy*1500/calls, 3) == 0.568
be = price/per_call
print(f"break-even calls per user per month at price 5 = {be:.1f}")
assert round(be, 1) == 416.7
# option A: 400 included calls, overage 0.02 per call
inc, over = 400, 0.02
def user_margin(c):
    rev_u = price + max(0, c-inc)*over
    return rev_u - c*per_call
print(f"option A (400 included, overage 0.02): heavy margin {user_margin(1500):.2f}, light margin {user_margin(60):.2f}")
assert abs(user_margin(1500) - 9.0) < 1e-9
# option B: hard cap at 400 calls, no overage, heavy users stay at 5
print(f"option B (hard cap 400): heavy cost {400*per_call:.2f}, margin {price-400*per_call:.2f}")
assert abs(price-400*per_call-0.2) < 1e-9
# option C: route heavy usage to a model costing 40% less per call
c2 = 0.012*0.6
print(f"option C (cheaper model for calls above 400, -40% cost): heavy cost {400*per_call+1100*c2:.3f}")
assert abs(400*per_call+1100*c2 - 12.72) < 1e-9
print(f"average cost per user = {cost/users:.3f}")
assert abs(cost/users - 1.584) < 1e-9
assert abs(5 - 18 + 27 - 18 - 9 + 13) < 1e-9 and 5 + 1100*0.02 == 27
```

**Output (my run):**
```
calls = 13,200,000, cost = 158,400, revenue = 500,000, margin = 341,600 (68.3%)
heavy user cost 18.00, margin -13.00 (-260% of revenue)
light user cost 0.72, margin 4.28
heavy users: 5000 x -13 = -65,000; light users: 406,600
heavy share of calls (and cost) = 56.8%, share of users = 5%
break-even calls per user per month at price 5 = 416.7
option A (400 included, overage 0.02): heavy margin 9.00, light margin 4.28
option B (hard cap 400): heavy cost 4.80, margin 0.20
option C (cheaper model for calls above 400, -40% cost): heavy cost 12.720
average cost per user = 1.584
```

**Follow-ups:**
- *What if heavy users are bots?* Rate limit and authentication first, pricing second.
- *Why not charge everyone 20?* Light users cost 0.72; a high flat price loses them to a competitor and keeps only the heavy ones.
- *How would you reduce cost per call?* Caching and shorter prompts; see Book 2 Part 1 Q24 (prefix caching) and Book 2 Part 2 Q5 (token maths).

**Common mistakes:**
- Using the average cost per user (1.58) and missing the cross-subsidy.
- Calling the feature unprofitable from the heavy-user margin alone.
- Capping without checking who the heavy users are.
- Forgetting that behaviour changes after pricing changes.

### Q50 ⭐ 🟡 A team generates 500 synthetic test questions from its documents with an LLM, and humans review a random 100 of them and find 78 valid. Compute the sample valid rate with a 95% Wilson interval and the projected range of valid questions among the 500, and say how you would use the set.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to synthetic evaluation data topics in LLM evaluation pages; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened

**Say this first (1 line):** The valid rate is 78% with a 95% Wilson interval of about 68.9% to 85.0%, so roughly 345 to 425 of the 500 are valid (about 354 to 418 if I count the 78 already confirmed), and I would use the set as a cheap regression and smoke test, after removing invalid items, never as the headline quality number.

**Clarifying questions:**
- How were the 100 picked, truly at random from the 500? A hand-picked 100 breaks the interval.
- What did "valid" mean to the reviewers (answerable from the document, unambiguous, single correct answer)? A loose definition inflates the rate.
- Did two reviewers check, and how often did they agree? One reviewer's judgement is a noisy label.
- Which question types did the LLM make (lookup, multi-hop, numeric)? Valid rate usually differs by type.
- What will the set be used for: ranking retrieval variants, regression tests, or reporting accuracy to leadership?

**Approach:**
1. Sample rate = 78 / 100 = 0.78.
2. Wilson 95% interval: 0.689 to 0.850. (Wilson behaves better than the plain normal interval at this size.)
3. Naive projection to 500: 500 x 0.689 to 500 x 0.850 = 345 to 425 valid, so 75 to 155 invalid.
4. A better projection uses the fact that the 100 reviewed are known: 78 + 400 x (0.689 to 0.850) = 354 to 418. The sample is 20% of the whole, which also trims the true uncertainty by a factor of about 0.89.
5. Use of the set: review or auto-filter the invalid ones. Cheapest route: have people review the remaining 400 for a large set (or a second LLM filter checked on the reviewed 100) and keep only valid items.
6. Stratify by question type and report valid rate by type. Low-validity types get dropped or rewritten.
7. Use the set for comparing variants on the same questions (A versus B), where shared flaws cancel, and for regression. Do not report its accuracy as production accuracy: synthetic questions tend to reuse the document's wording, so they can be easier than real ones (state this as a risk to test, not a fact).
8. Keep a separate small set from real user logs or written by domain experts as the anchor, and compare the model's score on both. A big gap tells you how unrepresentative the synthetic set is.

**Metrics:**
- Valid rate = questions judged valid / questions reviewed = 78 / 100, with a Wilson interval.
- Reviewer agreement = share of questions where two reviewers agree (and kappa).
- Score gap = accuracy on the synthetic set - accuracy on the real-log set.
- Guardrail: coverage across documents and question types after filtering.

**Risks:**
- Selection: reviewers label the first 100 they see, not a random 100.
- The generator and the system under test are the same model family, so the questions can match what the model finds easy.
- Valid but trivial questions pass review yet do not discriminate between systems.
- Duplicates and near-duplicates inflate the set size.

**What the interviewer scores:**
- Strong: gives the interval, converts it to counts, and says what the interval does not cover (bias, definition of valid). Weak: "78% valid, so 390 valid".
- Strong: notes the 100 reviewed are part of the 500. Weak: ignores it (minor).
- Strong: a use that fits the weakness (relative comparison, regression), plus a real-log anchor. Weak: reports synthetic accuracy as quality.
- Strong: asks about reviewer agreement.

**Example:** Illustrative. 500 questions, 78 of 100 valid. Weak: "78% valid, so 390 valid questions. Ship the eval." Strong: "About 345 to 425 valid. I would filter out the invalid ones, compare retrieval variants on the same questions, and keep 100 real questions as the check that the synthetic score means something."

**Code:**
```python
import math
def wil(k, n, z=1.96):
    p = k/n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return c-h, c+h
k, n, N = 78, 100, 500
lo, hi = wil(k, n)
print(f"valid rate {k/n:.2f}, Wilson 95% {lo:.4f} to {hi:.4f}")
assert 0.688 < lo < 0.690 and 0.849 < hi < 0.851
print(f"naive projection over 500: {N*lo:.0f} to {N*hi:.0f} valid")
assert round(N*lo) == 345 and round(N*hi) == 425
rest = N - n
a, b = k + rest*lo, k + rest*hi
print(f"reviewed 100 are known: 78 + {rest} x interval = {a:.0f} to {b:.0f} valid")
assert round(a) == 354 and round(b) == 418
fpc = math.sqrt(1 - n/N)
print(f"finite-population factor on the standard error = {fpc:.3f}")
assert abs(fpc - 0.894) < 0.001
# how many more to review to halve the interval width roughly
w = hi - lo
for m in (100, 200, 400):
    l2, h2 = wil(round(0.78*m), m)
    print(f"n={m}: width {h2-l2:.3f}")
assert (wil(312, 400)[1]-wil(312, 400)[0]) < 0.6*w
# invalid questions to drop if used as a test set
print(f"expected invalid among 500: {N*(1-k/n):.0f} (range {N*(1-hi):.0f} to {N*(1-lo):.0f})")
assert round(N*(1-k/n)) == 110
```

**Output (my run):**
```
valid rate 0.78, Wilson 95% 0.6893 to 0.8500
naive projection over 500: 345 to 425 valid
reviewed 100 are known: 78 + 400 x interval = 354 to 418 valid
finite-population factor on the standard error = 0.894
n=100: width 0.161
n=200: width 0.114
n=400: width 0.081
expected invalid among 500: 110 (range 75 to 155)
```

**Follow-ups:**
- *How many more questions should we review?* With 400 reviewed in total the interval is about 8 points wide (it is 16 now). Review more if decisions depend on the count.
- *Can an LLM do the review?* As a filter yes, if checked against human labels on a sample (agreement, kappa); see Book 2 Part 9 Q6.
- *Why Wilson and not the normal interval?* Wilson stays inside 0 to 1 and covers better for moderate n and extreme rates.

**Common mistakes:**
- Using synthetic accuracy as the product's accuracy.
- Not checking randomness of the reviewed sample.
- Ignoring that the reviewed 100 are part of the 500.
- One reviewer, no agreement check.
- Keeping invalid questions in the set.

### Q51 ⭐ 🟡 A vendor API processes prompts outside the country, and a sample of 500 of the 20,000 daily prompts finds personal data in 90 of them (18%, a measured sample). Compute the projected daily count of prompts with personal data, and compare redaction, a regional endpoint, self-hosting and contractual terms, saying what you need from legal.
**Asked at:** PII and compliance material (tianpan, Kunal Ganglani, Gravitee and barkingiguana pages on logs, retention, redaction and data residency, and a vendor piece on DPDP readiness for LLM traffic); vendor and practitioner pages, not regulator guidance or an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened

**Say this first (1 line):** About 3,600 prompts a day carry personal data (18% of 20,000; the sample interval gives roughly 2,980 to 4,320), so I would redact before sending as the first control, add a regional endpoint or contract terms for what remains, and get legal to say what is allowed before choosing, because I cannot decide the legal question from engineering.

**Clarifying questions:**
- What counts as personal data in the 90 hits (names, phone numbers, account numbers, health or financial details)? Sensitive classes need stricter handling.
- Whose data is it: customers, employees, or third parties mentioned by users? It changes the legal basis.
- Which law or contract applies (country rules, sector rules, customer contracts)? This is for legal; I will not guess.
- Does the vendor store prompts, train on them, or keep logs, and for how long? Retention often matters more than transit.
- Can the product work with redacted text (replace names with tokens), or does it need the real values?
- What latency, quality and budget limits apply to each option?

**Approach:**
1. Size the exposure. 18% of 20,000 = 3,600 prompts a day, about 1.3 million a year. The 95% Wilson interval on 90 of 500 is 14.9% to 21.6%, so 2,976 to 4,322 a day.
2. Quantify the leak after redaction. Redaction is never perfect: at 95% recall, 180 prompts a day still carry personal data. At 99%, 36. Measure the real recall on a labelled sample of your own prompts.
3. Compare options:

| Option | What it fixes | Cost and limits |
|---|---|---|
| Redaction before the call | Removes most personal data from what leaves | Misses some items; may hurt answer quality; needs ongoing tuning |
| Regional endpoint at the vendor | Keeps processing in an agreed region | Depends on vendor offering; model choice and price may differ; storage and support access still need checking |
| Self-hosting | Data stays in your control | Highest cost and effort; you own security, scaling and model quality |
| Contract terms (no training, short retention, listed sub-processors, breach duty) | Sets obligations and remedies | A promise, not a technical control; needs audit and trust |

4. Recommended order: redact now (fast), add contract terms (parallel), and use a regional endpoint if it exists and passes legal review. Self-host only if the data class or volume justifies it.
5. What I need from legal: whether sending this data abroad is allowed and under what conditions; what notice or consent is required; which data classes are barred outright; the vendor contract requirements (processing terms, sub-processors, retention, deletion, breach notice); and the log retention and deletion duties for our own logs.
6. Also fix our side: do not log raw prompts longer than needed, restrict access, and set a deletion period.
7. Re-sample monthly (another 500) to check the 18% and the redaction recall.

**Metrics:**
- Personal-data prompt rate = prompts with personal data / prompts sampled = 90 / 500 = 18%, with a Wilson interval.
- Redaction recall = personal data items removed / personal data items present, on a labelled sample. Residual leak per day = 3,600 x (1 - recall).
- Answer quality with redaction versus without, on the same prompts.
- Guardrails: retention days, number of vendors and sub-processors, access-log audit results.

**Risks:**
- A sample of 500 can miss rare but serious data types (a 0.5%-rare type is missed 8.2% of the time in 500 prompts).
- Redaction can break the task (an address, a name the answer depends on).
- Regional endpoints may still send logs or support data elsewhere. Check this in writing.
- Engineering cannot settle the legal question. Do not claim compliance.

**What the interviewer scores:**
- Strong: 3,600 per day, an interval, and a residual leak after redaction. Weak: "18% is a lot".
- Strong: a table of options with the limits of each, a recommended order, and a clear list for legal. Weak: picks self-hosting immediately or says "legal will handle it".
- Strong: separates transit, storage and retention. Weak: only talks about the network path.
- Strong: does not claim legal conclusions.

**Example:** Illustrative. 20,000 prompts a day, 18% carry personal data, so 3,600. Redaction recall of 95% leaves 180 a day. Weak: "Use a regional endpoint and we are compliant." Strong: "Redact first, which cuts 3,600 to roughly 180 if recall is 95%, then ask legal whether the regional endpoint and contract terms are enough for the remaining data, and measure recall every month."

**Code:**
```python
import math
def wil(k, n, z=1.96):
    p = k/n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return c-h, c+h
daily, n, k = 20_000, 500, 90
p = k/n
lo, hi = wil(k, n)
print(f"rate {p:.3f}, Wilson 95% {lo:.4f} to {hi:.4f}")
assert p == 0.18 and 0.148 < lo < 0.150 and 0.216 < hi < 0.218
proj = daily*p
print(f"projected prompts with personal data per day = {proj:.0f} (range {daily*lo:.0f} to {daily*hi:.0f})")
assert round(proj) == 3600 and round(daily*lo) == 2976 and round(daily*hi) == 4322
print(f"per year (365 d): {proj*365:,.0f}")
assert round(proj*365) == 1_314_000
# redaction recall sensitivity
for r in (0.90, 0.95, 0.99):
    leak = proj*(1-r)
    print(f"redaction recall {r:.0%}: {leak:.0f} prompts/day still carry personal data")
assert round(proj*0.05) == 180 and round(proj*0.01) == 36 and round(proj*0.10) == 360
# sample size to see a rare class: chance that a 500 sample misses a 0.5% type
miss = (1-0.005)**500
print(f"chance a 500-prompt sample contains none of a 0.5%-rare data type = {miss:.3f}")
assert round(miss, 3) == 0.082
```

**Output (my run):**
```
rate 0.180, Wilson 95% 0.1488 to 0.2161
projected prompts with personal data per day = 3600 (range 2976 to 4322)
per year (365 d): 1,314,000
redaction recall 90%: 360 prompts/day still carry personal data
redaction recall 95%: 180 prompts/day still carry personal data
redaction recall 99%: 36 prompts/day still carry personal data
chance a 500-prompt sample contains none of a 0.5%-rare data type = 0.082
```

**Follow-ups:**
- *Can you avoid sending personal data at all?* Sometimes: replace values with placeholders, and put the real values back after the answer comes back.
- *Does self-hosting remove the issue?* It removes the third-party transfer; you still need access control, retention and deletion.
- *How do you handle logs?* Redact before logging, set a short retention, and restrict who can read them.

**Common mistakes:**
- Treating the sample rate as exact.
- Assuming redaction is perfect.
- Claiming the architecture is compliant without legal review.
- Ignoring vendor retention and our own logs.

### Q52 ⭐ 🔴 A self-hosted node costs an illustrative 20 per hour and can generate 2,000 tokens a second at full load. Compute the cost per million output tokens at 100% and at 30% utilisation, compare with an API at an illustrative 15 per million output tokens, and find the utilisation at which the node breaks even.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to vendor-API versus self-host and LLM cost material; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened

**Say this first (1 line):** The node costs 2.78 per million output tokens at full load and 9.26 at 30% utilisation, against 15 for the API, and it breaks even at 18.5% utilisation, but that is a floor, because staff, a second node for redundancy and spiky traffic push the real break-even higher.

**Clarifying questions:**
- Is the 2,000 tokens per second measured on our prompt mix and our latency target, or a benchmark peak? Throughput at full load is often higher than throughput at an acceptable latency.
- Does the 20 per hour include everything (GPU, hosting, network), or only the GPU rental?
- How much of the load is input tokens (prefill)? They use capacity too, and the API bills them separately.
- Is the self-hosted model as good for our task as the API model? A cheaper model that fails more is not cheaper.
- What is the traffic shape across the day? Average utilisation is what pays the bill.
- Do we need a second node for failover?

**Approach:**
1. Tokens per hour at 100% = 2,000 x 3,600 = 7.2 million.
2. Cost per million at 100% = 20 / 7.2 = 2.778. At 30% = 20 / (7.2 x 0.3) = 20 / 2.16 = 9.259.
3. API price 15 per million. Self-host saves 81.5% at full load and 38.3% at 30%.
4. Break-even: 20 / (7.2 x u) = 15, so u = 20 / 108 = 0.1852, which is 18.5%. Check: at 18.5% the node makes 1.333 million tokens an hour, and 20 / 1.333 = 15.
5. Stress the answer (all illustrative): with two nodes for failover and 5 an hour of staff time, hourly cost is 45 for 14.4 million tokens of capacity, so break-even rises to 20.8% of total capacity. If the traffic is 6 hours at peak and 18 hours at 20%, average utilisation is 40%, so it passes the test, with less room than 30% looks like.
6. Decide on more than cost per token: quality on our task, security, uptime, engineering time, and the option to use the API for spikes and the node for the base load.

**Metrics:**
- Cost per million output tokens = hourly cost / (tokens per second x 3,600 x utilisation / 1,000,000).
- Utilisation = tokens actually generated / tokens the node could generate at the latency target, averaged over a month.
- Break-even utilisation = hourly cost / (capacity per hour in millions x API price).
- Guardrails: p95 latency, error rate, answer quality versus the API model.

**Risks:**
- The 2,000 tokens per second is the best case. At the latency users accept, real throughput can be lower, which moves the break-even up.
- Costs that do not scale: staff, monitoring, security, upgrades.
- Utilisation falls at night and on weekends; you pay for idle time.
- The model may be worse than the API model on the task.
- The API price can fall, which shrinks the case.

**What the interviewer scores:**
- Strong: 2.78, 9.26 and 18.5% correct, and says the break-even is a floor. Weak: stops at the arithmetic, or says "self-hosting is always cheaper".
- Strong: notes that the 2,000 tokens per second is at full load, and asks what it is at the latency target.
- Strong: hybrid design (node for base load, API for peaks). Weak: all or nothing.
- Strong: counts staff and redundancy.

**Example:** Illustrative. A node serving 40% average utilisation costs 20 / (7.2 x 0.4) = 6.94 per million, less than half the API price. At 15% it would cost 18.52, more than the API. Weak: "The node costs 2.78, which is much cheaper than 15, so self-host." Strong: "That is at 100%. At our real 30% it is 9.26, so we win by about 38% before staff and failover. I would run the base load on the node and send peaks to the API."

**Code:**
```python
hourly, tps, api = 20.0, 2000, 15.0
tok_hr = tps*3600
print(f"tokens per hour at 100% = {tok_hr:,}")
assert tok_hr == 7_200_000
def cost_per_m(u): return hourly/(tok_hr*u/1e6)
for u in (1.0, 0.3):
    print(f"utilisation {u:.0%}: cost per million output tokens = {cost_per_m(u):.3f}")
assert abs(cost_per_m(1.0) - 2.7778) < 1e-3 and abs(cost_per_m(0.3) - 9.2593) < 1e-3
be = hourly/(tok_hr/1e6*api)
print(f"break-even utilisation = {be:.4f} ({be:.1%})")
assert abs(be - 0.185185) < 1e-5
assert abs(cost_per_m(be) - api) < 1e-9
print(f"saving vs API at 30%: {(1-cost_per_m(0.3)/api):.1%}; at 100%: {(1-cost_per_m(1.0)/api):.1%}")
assert round(1-cost_per_m(0.3)/api, 3) == 0.383
# add illustrative staff and redundancy overhead: node cost doubles for 2 nodes + 5 per hour of staff time
total_hr = 2*hourly + 5
be2 = total_hr/(2*tok_hr/1e6*api)
print(f"with 2 nodes and 5/hour staff: break-even utilisation (of both nodes) = {be2:.4f}")
assert abs(be2 - 45/(2*7.2*15)) < 1e-12
print(f"two nodes plus staff, each at 30% utilisation: cost per million = {total_hr/(2*tok_hr/1e6*0.3):.3f}")
# diurnal traffic: peak-provisioned, 100% at peak for 6h, 20% for 18h
avg_u = (6*1.0 + 18*0.2)/24
print(f"example average utilisation across a day = {avg_u:.3f}")
assert abs(avg_u - 0.4) < 1e-12
assert round(1-cost_per_m(1.0)/api, 3) == 0.815 and round(total_hr/(2*tok_hr/1e6*0.3), 3) == 10.417
print(f"at 40%: {cost_per_m(0.4):.2f}; at 15%: {cost_per_m(0.15):.2f}; break-even if API price halves: {hourly/(tok_hr/1e6*api/2):.3f}")
assert round(cost_per_m(0.4), 2) == 6.94 and round(cost_per_m(0.15), 2) == 18.52 and round(hourly/(tok_hr/1e6*api/2), 3) == 0.370
```

**Output (my run):**
```
tokens per hour at 100% = 7,200,000
utilisation 100%: cost per million output tokens = 2.778
utilisation 30%: cost per million output tokens = 9.259
break-even utilisation = 0.1852 (18.5%)
saving vs API at 30%: 38.3%; at 100%: 81.5%
with 2 nodes and 5/hour staff: break-even utilisation (of both nodes) = 0.2083
two nodes plus staff, each at 30% utilisation: cost per million = 10.417
example average utilisation across a day = 0.400
at 40%: 6.94; at 15%: 18.52; break-even if API price halves: 0.370
```

**Follow-ups:**
- *How do you raise utilisation?* Batch more requests, route to the node from several services, move offline jobs to quiet hours. See Book 2 Part 1 Q6 (the KV cache) for why batching is limited by memory.
- *What if the API price halves?* Break-even utilisation doubles to 37%.
- *Would you compare input tokens too?* Yes, if the API charges for input; our node pays for prefill in capacity.

**Common mistakes:**
- Using the full-load number as the operating cost.
- Leaving out staff, redundancy and idle hours.
- Comparing cost per token without comparing quality.
- Treating break-even as a target rather than a floor.

### Q53 ⭐ 🔴 English answers are graded correct on 91 of 100 test questions and Hindi answers on 78 of 100, using different graders. Compute 95% Wilson intervals for both, say whether the 13-point absolute gap looks real, and list the confounds in the comparison.
**Asked at:** Indic-language and tokenizer material (an ACL Anthology LoResLM 2026 paper on informal and romanised Hindi tokenization, an arXiv study of tokenizer efficiency across the 22 official Indian languages, a HackerNoon opinion piece on the cost of building AI for Indian languages); research and commentary pages rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened

**Say this first (1 line):** English is 91% (95% Wilson 83.8% to 95.2%) and Hindi is 78% (68.9% to 85.0%), the 13-point gap is statistically visible (z about 2.6, difference CI about 2.9 to 23 points) but too wide to size, and with different graders I cannot say the gap comes from the language, so I would fix the grading first.

**Clarifying questions:**
- Are the Hindi questions translations of the English ones, or different questions? Different questions mean different difficulty, and the gap is not a clean language effect.
- Who graded each set, and with what rubric? If graders differ in strictness, they can create or hide the whole gap.
- Is the Hindi in Devanagari, romanised, or mixed? Real users often write romanised Hindi, which models and tokenizers may handle worse.
- What did "correct" mean for free-text answers (exact string, key facts, or judge score)?
- How were the 100 questions chosen? Random from real traffic, or hand-picked?
- What decision depends on this: a launch gate, a fine-tuning budget, or a note in a report?

**Approach:**
1. Wilson intervals: English 0.838 to 0.952; Hindi 0.689 to 0.850. They overlap a little (about 1.2 points).
2. Overlap is not a test. Do the difference test: gap 13 points, standard error 5.0 points, z = 2.58, p about 0.01. Newcombe 95% CI for the gap: 2.9 to 23.0 points.
3. Say it plainly: there is a gap in these graded numbers, probably not zero, but anywhere from about 3 to 23 points is consistent with the data, and with 100 questions each we cannot be precise.
4. List the confounds (below), because the gap mixes language, grader, questions and scoring.
5. Redesign the comparison: use the same questions translated by a person (paired design), the same bilingual grader or the same judge model with a rubric validated against humans in both languages, graders blind to language, and at least 300 to 400 per language for a tighter estimate.
6. Run McNemar on the paired results: only the questions where the two languages differ matter.
7. Add slices: question type, answer length, romanised versus Devanagari input, so that I know where the loss is.

**Confounds:**
- Different graders (strictness, language skills, rubric). A few points of grader difference can explain a large part of 13.
- Different questions (difficulty, topic, ambiguity) unless they are translations.
- Translation quality (a translated question can change meaning).
- Output language of the answer, and whether code-mixed answers count.
- Script (Devanagari or romanised) and tokenization (longer token sequences for Hindi; see Book 2 Part 2 Q17 on the token tax).
- Small samples: 100 each, so an interval of about 15 points per language.
- Multiple slicing later: the more splits, the more false findings.

**Metrics:**
- Accuracy by language = correct / 100, with Wilson intervals.
- Gap = English accuracy - Hindi accuracy, with a Newcombe interval (unpaired) or a McNemar-based interval (paired).
- Grader agreement = Cohen's kappa between graders on a shared 50-item sample (see Book 2 Part 9 Q6).
- Guardrail: same-grader gap after the fix.

**Risks:**
- Reporting 13 points as "the Hindi penalty" and spending a budget on it.
- Reporting "no difference, the intervals overlap".
- A Hindi grader who is stricter or more lenient than the English one.
- Fixing the model for formal Hindi when users write romanised text.

**What the interviewer scores:**
- Strong: both intervals, a proper difference test, and the plain statement of what is and is not supported. Weak: "intervals overlap, so no difference" or "13 points, definitely worse".
- Strong: a list of confounds led by the grader difference. Weak: only sample size.
- Strong: a redesign (paired, same grader, bigger n). Weak: "get more data".
- Strong: asks about script and tokenization.

**Example:** Illustrative. If the Hindi grader was stricter and wrongly failed 6 correct answers, Hindi would be 84%, and the gap would be 7 points. Weak: "Hindi is 13 points worse, we need a Hindi fine-tune." Strong: "There is a gap, probably 3 to 23 points, but two graders and possibly different questions mean I cannot say the model is the cause. I will translate the same questions, grade them with one rubric, and use 300 per language."

**Code:**
```python
import math
def wil(k, n, z=1.96):
    p = k/n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return c-h, c+h
n = 100
le, he = wil(91, n); lh, hh = wil(78, n)
print(f"English 91/100: {le:.4f} to {he:.4f}")
print(f"Hindi   78/100: {lh:.4f} to {hh:.4f}")
assert 0.837 < le < 0.839 and 0.951 < he < 0.953 and 0.688 < lh < 0.690 and 0.849 < hh < 0.851
print(f"intervals overlap: {lh < he and le < hh} (overlap {hh-le:.3f})")
assert hh > le
gap = 0.91-0.78
se = math.sqrt(.91*.09/n + .78*.22/n)
z = gap/se
p = math.erfc(z/math.sqrt(2))
print(f"gap {gap*100:.0f} points, z = {z:.2f}, two-sided p = {p:.4f}")
assert round(gap*100) == 13 and 2.5 < z < 2.65 and 0.008 < p < 0.012
# Newcombe hybrid interval for difference between two independent proportions
d_lo = gap - math.sqrt((0.91-le)**2 + (hh-0.78)**2)
d_hi = gap + math.sqrt((he-0.91)**2 + (0.78-lh)**2)
print(f"Newcombe 95% CI for the gap: {d_lo*100:.1f} to {d_hi*100:.1f} points")
assert 0.028 < d_lo < 0.030 and 0.21 < d_hi < 0.23
# how much grader error could move the gap? if the Hindi grader wrongly fails 6 correct answers
for err in (0, 3, 6, 10):
    g = 0.91 - (0.78+err/100)
    print(f"if {err} of Hindi's failures are grader mistakes: gap {g*100:.0f} points")
assert abs((0.91-0.84)-0.07) < 1e-12
# paired check design: if the same 100 questions were translated, count discordant pairs (invented)
print("paired design needed: McNemar on discordant pairs, not the two marginal rates")
n5 = 1.96**2*(.91*.09+.78*.22)/0.05**2
print(f"n per language for a gap CI half-width of 5 points: {n5:.0f}")
assert 385 < n5 < 395
```

**Output (my run):**
```
English 91/100: 0.8377 to 0.9519
Hindi   78/100: 0.6893 to 0.8500
intervals overlap: True (overlap 0.012)
gap 13 points, z = 2.58, two-sided p = 0.0098
Newcombe 95% CI for the gap: 2.9 to 23.0 points
if 0 of Hindi's failures are grader mistakes: gap 13 points
if 3 of Hindi's failures are grader mistakes: gap 10 points
if 6 of Hindi's failures are grader mistakes: gap 7 points
if 10 of Hindi's failures are grader mistakes: gap 3 points
paired design needed: McNemar on discordant pairs, not the two marginal rates
n per language for a gap CI half-width of 5 points: 390
```

**Follow-ups:**
- *Why not just test whether the intervals overlap?* Overlapping intervals can still hide a real difference. The difference test is the one to use, and here it points to a gap.
- *How big a sample do you need?* For a 13-point gap at these rates, about 100 each gives p about 0.01 for the unpaired test. To measure it within about 5 points you need several hundred per language.
- *Can an LLM judge both languages?* Only after checking it against human labels in each language.

**Common mistakes:**
- Using overlap of intervals as the test.
- Calling the gap a language effect with different graders.
- Ignoring script and translation quality.
- Comparing percentages without the sample sizes.

### Q54 ⭐ 🔴 A jailbreak test suite of 300 attacks is run against a hardened assistant and none succeed. Compute the approximate 95% upper bound on the per-attempt success rate with the rule of three and with the exact formula, and say what you can claim to a risk committee and what you cannot.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to red-teaming and jailbreak topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened

**Say this first (1 line):** With zero successes in 300 attacks, the 95% upper bound on the per-attempt success rate is about 1.0% by the rule of three (3 / 300) and 0.994% by the exact formula, so I can say "on this attack set, probably under 1% per attempt", but not "it is safe" or "it cannot be jailbroken".

**Clarifying questions:**
- Are the 300 attacks independent, or are they variants of a few attack families? Near-duplicates give far less evidence than 300 independent attempts.
- Were the attacks written before or after hardening? If the hardening was tuned on these same attacks, the result is a training score, not a test score.
- What counts as success (any policy violation, harmful content, tool misuse)? The definition changes the rate.
- Who judged success, and how? A weak judge can miss successes.
- What is the threat model: casual users, or an attacker who tries many times and adapts?
- What risk level does the committee want to certify (for example 1 in 1,000)?

**Approach:**
1. Rule of three: with 0 events in n trials, the 95% upper bound is about 3 / n = 3 / 300 = 1.0%.
2. Exact formula: find p so that the chance of zero successes in 300 tries is 5%: (1 - p)^300 = 0.05, so p = 1 - 0.05^(1/300) = 0.00994, which is 0.994%. The rule of three is a close approximation.
3. Other versions: the two-sided Clopper-Pearson upper bound is 1.22%, and the Wilson upper bound is 1.26%. Say which one you used.
4. What I can claim: if the 300 attacks are a fair sample of the attacks we expect, and each is independent, then we have 95% confidence that the per-attempt success rate on that kind of attack is at most about 1%.
5. What I cannot claim: no vulnerability exists; the rate is zero; the system resists new attack types; the system resists an adaptive attacker. A 1% rate per attempt means a persistent attacker making 100 tries succeeds at least once with probability 63%, and with 1,000 tries almost certainly.
6. To certify 0.1% you need about 2,995 attacks with zero successes; for 0.01%, about 29,956. That is the cost of a tighter claim.
7. What I would give the committee: the bound with its assumptions, the attack categories covered, the rate by category, and a plan: continuous red teaming with fresh attacks, a held-out set that was never used to harden, monitoring in production, rate limits and layered controls (not only the model).

**Metrics:**
- Attack success rate = successful attacks / attempts, with a one-sided 95% upper bound = 1 - 0.05^(1/n) when there are 0 successes.
- Coverage = attack categories tested / categories in the threat model.
- Time to detect and fix a new successful attack.
- Guardrail: false refusal rate on benign prompts (a model can reach zero attacks by refusing everything).

**Risks:**
- The bound depends on the 300 being independent draws; 30 families times 10 variants would give an effective sample near 30 and an upper bound near 9.5%.
- Tuning on the test attacks makes the result optimistic.
- Attackers adapt; a fixed suite does not.
- Over-refusal can hide behind a low attack success rate.

**What the interviewer scores:**
- Strong: both numbers (1.0% and 0.994%), and the 63% chance over 100 tries. Weak: "zero failures, so the risk is zero".
- Strong: separates what is claimed (this suite, this confidence) from what is not. Weak: either overclaims or refuses to claim anything.
- Strong: asks about independence and whether the attacks were used for tuning.
- Strong: proposes ongoing testing and layered controls.

**Example:** Illustrative. Weak: "We ran 300 jailbreaks and none worked, so the assistant is secure." Strong: "On this suite we can say the per-attempt success rate is under about 1% with 95% confidence. That is not the same as secure: an attacker with 100 tries at 1% would succeed 63% of the time. We will add a held-out set, fresh attacks each month and production monitoring."

**Code:**
```python
import math
n = 300
rule3 = 3/n
exact = 1 - 0.05**(1/n)
print(f"rule of three: {rule3:.4f}; exact one-sided 95% upper bound: {exact:.5f}")
assert abs(rule3 - 0.01) < 1e-12 and 0.00990 < exact < 0.00997
assert abs((1-exact)**n - 0.05) < 1e-12
# two-sided 97.5% (Clopper-Pearson, 0 successes) and Wilson for comparison
cp2 = 1 - 0.025**(1/n)
z = 1.96
wil = z*z/(n+z*z)
print(f"two-sided Clopper-Pearson upper: {cp2:.4f}; Wilson upper: {wil:.4f}")
assert 0.0120 < cp2 < 0.0124 and 0.0125 < wil < 0.0128
# attempts needed to claim <= 0.1% and <= 0.01%
for t in (0.001, 0.0001):
    need = math.log(0.05)/math.log(1-t)
    print(f"attacks with zero successes needed to claim rate <= {t:.2%}: {math.ceil(need):,} (rule of three: {3/t:,.0f})")
assert math.ceil(math.log(0.05)/math.log(0.999)) == 2995 and math.ceil(math.log(0.05)/math.log(0.9999)) == 29956
# what 1% per attempt means for a persistent attacker
for tries in (10, 100, 1000):
    print(f"at 1% per attempt, chance of at least one success in {tries}: {1-0.99**tries:.4f}")
assert round(1-0.99**100, 3) == 0.634 and round(1-0.99**1000, 4) == 1.0
# even at the exact bound 0.0099 per attempt
print(f"at 0.0099 per attempt, 100 attempts: {1-(1-exact)**100:.3f}")
assert round(1-(1-exact)**100, 3) == 0.632
# if the 300 attacks were really 30 attack families x 10 near-duplicate variants (effective n ~ 30)
n_eff = 30
print(f"if effective independent attacks are 30: upper bound = {1-0.05**(1/n_eff):.3f}")
assert round(1-0.05**(1/n_eff), 3) == 0.095
# one success in 300: solve P(X<=1) = 0.05 by bisection
f = lambda p: (1-p)**n + n*p*(1-p)**(n-1) - 0.05
lo_, hi_ = 0.0, 0.1
for _ in range(100):
    mid = (lo_+hi_)/2
    if f(mid) > 0: lo_ = mid
    else: hi_ = mid
print(f"upper bound with 1 success in 300: {lo_:.5f} = {lo_*n:.2f} / n")
assert 4.6 < lo_*n < 4.8
```

**Output (my run):**
```
rule of three: 0.0100; exact one-sided 95% upper bound: 0.00994
two-sided Clopper-Pearson upper: 0.0122; Wilson upper: 0.0126
attacks with zero successes needed to claim rate <= 0.10%: 2,995 (rule of three: 3,000)
attacks with zero successes needed to claim rate <= 0.01%: 29,956 (rule of three: 30,000)
at 1% per attempt, chance of at least one success in 10: 0.0956
at 1% per attempt, chance of at least one success in 100: 0.6340
at 1% per attempt, chance of at least one success in 1000: 1.0000
at 0.0099 per attempt, 100 attempts: 0.632
if effective independent attacks are 30: upper bound = 0.095
upper bound with 1 success in 300: 0.01571 = 4.71 / n
```

**Follow-ups:**
- *Why does the rule of three work?* The exact bound solves (1 - p)^n = 0.05. For small p, ln(1 - p) is about -p, so p is about -ln(0.05) / n = 2.996 / n, which is about 3 / n.
- *What if one attack succeeds?* The bound rises (about 4.7 / n for the 95% one-sided exact bound with one event; a statistics package gives the exact figure) and you fix that attack and its family.
- *Is the bound valid against adaptive attackers?* No; it describes the sampled attack distribution.

**Common mistakes:**
- Reading zero successes as zero risk.
- Counting near-duplicate attacks as independent.
- Testing on the attacks used to harden.
- Forgetting the persistent attacker's repeated tries.
- Ignoring over-refusal.

### Q55 ⭐ 🔴 A model answers a question only if its confidence is above a threshold; at threshold 0.7 it answers 80% of questions with 92% accuracy, and at 0.9 it answers 55% with 97% accuracy (accuracy measured among answered questions). A wrong answer costs 20, a human escalation costs 4 and a correct answer costs 0, all illustrative. Compute the expected cost per question at each threshold, and say how sensitive the choice is to the wrong-answer cost.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to abstention and hallucination-reduction topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened

**Say this first (1 line):** Expected cost per question is 2.08 at threshold 0.7 and 2.13 at 0.9, so 0.7 is cheaper by only 0.05, and the choice flips when the wrong-answer cost passes about 21.05, so a 5% error in that one number reverses the decision and I would not treat it as settled.

**Clarifying questions:**
- Is the cost of 20 for a wrong answer measured (refunds, complaints, rework) or guessed? It is the number that decides the choice.
- Is the accuracy of 92% and 97% measured on enough answered questions to trust? With a few hundred, each carries a few points of error.
- Is the confidence score calibrated, so 0.7 means roughly 70% likely right? If not, thresholds do not mean what they say.
- What does an escalation really cost, and can humans handle 45% of the volume? Capacity can be the real limit.
- Do human escalations get everything right, or do they also make mistakes?
- Are some questions high stakes, where a wrong answer costs far more than 20?

**Approach:**
1. Expected cost per question = P(answer) x P(wrong | answered) x wrong cost + P(escalate) x escalation cost + correct answers x 0.
2. Threshold 0.7: answers 80%. Wrong = 0.80 x 0.08 = 0.064 per question, cost 0.064 x 20 = 1.28. Escalated = 20%, cost 0.20 x 4 = 0.80. Total = 2.08.
3. Threshold 0.9: answers 55%. Wrong = 0.55 x 0.03 = 0.0165, cost 0.33. Escalated = 45%, cost 1.80. Total = 2.13.
4. So 0.7 is cheaper by 0.05 per question (about 2.4% of 2.08).
5. Sensitivity to the wrong cost w: cost at 0.7 = 0.064w + 0.8; at 0.9 = 0.0165w + 1.8. Equal when 0.0475w = 1.0, so w = 21.05. Below that 0.7 wins; above it 0.9 wins. At w = 30 the costs are 2.72 and 2.30, so 0.9 wins by 0.42.
6. Why it is so close: the extra 25% of questions answered at 0.7 (the band between thresholds) are right 81% of the time and wrong 19%. Answering is worth it when the wrong rate is below 4 / 20 = 20%. At 19% we are almost exactly at the line.
7. Sensitivity to accuracy: if accuracy at 0.7 is really 91% (not 92%), its cost is 2.24 and 0.9 becomes better. So both inputs matter.
8. What I would do: collect the real cost of a wrong answer, put confidence intervals on the accuracies, and look at a middle threshold such as 0.8, since the cost curve is flat here. Also use different thresholds by topic: strict for high-stakes topics, looser for low-stakes ones.

**Metrics:**
- Expected cost per question = answer rate x (1 - accuracy among answered) x wrong cost + (1 - answer rate) x escalation cost.
- Coverage = answered / all questions. Selective accuracy = correct among answered / answered.
- Break-even wrong cost = (cost difference of escalations) / (difference in wrong answers per question) = 1.0 / 0.0475 = 21.05.
- Guardrails: escalation volume per day versus human capacity, wrong-answer rate by topic, calibration of the confidence score.

**Risks:**
- Confidence scores that are not calibrated; the same threshold behaves differently after a model or prompt change.
- Measured accuracies have error; a 1-point error flips the decision.
- Wrong answers are not equal: a few costly ones can dominate.
- Escalation capacity: 45% escalation might not be handleable at the assumed cost of 4.
- Users who get "I don't know" 45% of the time may stop using the product (not in the cost).

**What the interviewer scores:**
- Strong: 2.08 and 2.13 correct, with the break-even at 21.05 and the message that it is close to a tie. Weak: picks 0.9 because it has higher accuracy.
- Strong: explains the marginal band (19% wrong against a 20% line). Weak: only plugs in numbers.
- Strong: asks where the 20 comes from and about calibration. Weak: takes the inputs as facts.
- Strong: proposes thresholds by topic and tests intermediate values.

**Example:** Illustrative. At a wrong cost of 20, threshold 0.7 costs 2.08 and 0.9 costs 2.13. At 30, 0.7 costs 2.72 and 0.9 costs 2.30. Weak: "0.9 is 97% accurate, so 0.9." Strong: "The two are within 2% at a wrong cost of 20 and they cross at 21. I would first measure the true cost of a wrong answer, then maybe use 0.7 for low-stakes topics and 0.9 for high-stakes ones."

**Code:**
```python
W, E = 20.0, 4.0
def cost(ans, acc, w=W, e=E):
    wrong = ans*(1-acc)
    return wrong*w + (1-ans)*e, wrong
c7, w7 = cost(0.80, 0.92)
c9, w9 = cost(0.55, 0.97)
print(f"threshold 0.7: wrong {w7:.4f}, expected cost {c7:.4f}")
print(f"threshold 0.9: wrong {w9:.4f}, expected cost {c9:.4f}")
assert abs(w7-0.064) < 1e-12 and abs(c7-2.08) < 1e-12
assert abs(w9-0.0165) < 1e-12 and abs(c9-2.13) < 1e-12
# break-even wrong-answer cost: 0.064 w + 0.8 = 0.0165 w + 1.8
be = (1.8-0.8)/(0.064-0.0165)
print(f"break-even wrong-answer cost = {be:.2f}")
assert abs(be - 21.0526) < 1e-3
for w in (10, 15, 20, 21.05, 22, 30, 40):
    a, _ = cost(0.80, 0.92, w); b, _ = cost(0.55, 0.97, w)
    print(f"wrong-answer cost {w:>5}: t=0.7 {a:.3f}, t=0.9 {b:.3f}, cheaper: {'0.7' if a<b else '0.9'}")
assert cost(0.80,0.92,20)[0] < cost(0.55,0.97,20)[0] and cost(0.80,0.92,22)[0] > cost(0.55,0.97,22)[0]
# marginal band: questions answered at 0.7 but not at 0.9
band = 0.80-0.55
wrong_band = w7-w9
print(f"band share {band:.2f}, wrong in band {wrong_band:.4f} = {wrong_band/band:.1%} of band answers")
assert abs(wrong_band/band - 0.19) < 1e-12
print(f"answering is worth it when wrong rate < escalation/wrong cost = {E/W:.0%} (at cost 20); 4/0.19 = {4/0.19:.2f}")
assert abs(4/0.19 - be) < 1e-9
# sensitivity to accuracy at threshold 0.7: 91% instead of 92%
c7b, _ = cost(0.80, 0.91)
print(f"if accuracy at 0.7 is really 91%: cost {c7b:.3f} vs 0.9 option {c9:.3f}")
assert c7b > c9
```

**Output (my run):**
```
threshold 0.7: wrong 0.0640, expected cost 2.0800
threshold 0.9: wrong 0.0165, expected cost 2.1300
break-even wrong-answer cost = 21.05
wrong-answer cost    10: t=0.7 1.440, t=0.9 1.965, cheaper: 0.7
wrong-answer cost    15: t=0.7 1.760, t=0.9 2.047, cheaper: 0.7
wrong-answer cost    20: t=0.7 2.080, t=0.9 2.130, cheaper: 0.7
wrong-answer cost 21.05: t=0.7 2.147, t=0.9 2.147, cheaper: 0.7
wrong-answer cost    22: t=0.7 2.208, t=0.9 2.163, cheaper: 0.9
wrong-answer cost    30: t=0.7 2.720, t=0.9 2.295, cheaper: 0.9
wrong-answer cost    40: t=0.7 3.360, t=0.9 2.460, cheaper: 0.9
band share 0.25, wrong in band 0.0475 = 19.0% of band answers
answering is worth it when wrong rate < escalation/wrong cost = 20% (at cost 20); 4/0.19 = 21.05
if accuracy at 0.7 is really 91%: cost 2.240 vs 0.9 option 2.130
```

**Follow-ups:**
- *How would you pick the threshold with a continuous curve?* Compute expected cost at many thresholds on a labelled validation set, and choose the minimum, with a bootstrap interval for the cost.
- *What if wrong answers have different costs by topic?* Use a threshold per topic, or per risk class, from each topic's own cost.
- *What about the 45% escalation load?* Add a capacity constraint, or the cost of waiting time for the human queue.

**Common mistakes:**
- Choosing the highest accuracy without pricing coverage.
- Treating the wrong-answer cost as exact.
- Forgetting that accuracy is measured among answered questions only.
- Ignoring calibration and escalation capacity.

