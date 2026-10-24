### Q1 ⭐⭐⭐ 🟡 Give your framework for a GenAI system design interview: how do you spend the first ten minutes on requirements (users, inputs and outputs, data sources and sensitivity, latency, quality bar, volume, build vs buy), when do you decide which parts are deterministic code and which need a model, and how do you then cover architecture, evaluation, failure modes, safety, cost and rollout? Show it on a one-line prompt such as 'design an assistant for our company documents'. (This is the capstone view over Parts 1-11.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
**Say this first (1 line):** Spend the first ten minutes pinning down who uses it, what data it touches and what "good" means; then split every step into code or model; only then draw the architecture, and give evaluation, failure modes, safety, cost and rollout their own named time.

**Then explain:**
- **Requirements first (about 10 of 45 minutes, my own split, ASSUMED).** Ask about: users and their permissions; inputs and outputs (chat question in, cited answer out); data sources and how sensitive they are; latency target; the quality bar (how many wrong answers are tolerable, and which wrong answers are unacceptable); volume; build vs buy. State assumptions aloud instead of waiting for answers. Prep guides I opened (a 6-step and a 7-step framework) agree on the order: clarify, estimate, architecture, deep dive, trade-offs, failure modes, evolution. They are prep guides, not candidate reports.
- **Deterministic vs model split.** Use code wherever a rule can check the output: authentication, permission filtering, parsing, citation-id checks, PII redaction. Use the model for language work (rewrite a follow-up, write the answer) and keep a code check around it. The default is a workflow, not an agent (Part 8 Q3).
- **Architecture next, kept short:** ingest, index, retrieve, rerank, generate, cite. Permissions are applied inside retrieval (Part 6 Q15), ingestion keeps stable ids and handles deletes (Part 6 Q19), retrieval is hybrid with a reranker (Part 7 Q2, Q5).
- **Then the cross-cutting five.** Evaluation: a golden set and CI gates before launch (Part 9 Q2, Q14). Failure modes and safety: abstention, injection, the lethal trifecta (Part 6 Q27, Part 11 Q9). Cost and latency: the arithmetic in Q2 of this part. Rollout: shadow, canary, kill switch (Part 11 Q6, Part 9 Q46).
- **Close with the weakest point.** Say which assumption would most change your design and how you would test it first.

**Example:** Prompt: "design an assistant for our company documents". My first questions (and the answers I would assume if not given): 2,000 employees, docs in a drive and a wiki, each person may see only some of them, answers must cite a source, 5-second first-answer target, wrong-but-confident answers are worse than "I don't know", pilot first. That already decides things: permissions force ACL-aware retrieval, citations force chunk ids, the quality bar forces abstention. The code below prints my assumed 45-minute plan (10, 4, 10, 6, 6, 5 and 4 minutes), the code-vs-model split for ten steps of this system, and a checklist score: a "boxes and arrows" answer touches 3 of my 13 areas, a framework answer 12 of 13 (I wrote both answer sets myself, so this shows what the checklist is for, not evidence that it works).

**Code:** (mock LLMs and toy data; synthetic inputs labelled in the code)
```python
# Design-round planner for "design an assistant for our company documents".
# All inputs are ASSUMED (a 45-minute round); nothing here is measured.
ROUND_MIN = 45
PLAN = [("requirements and scope", 10), ("deterministic vs model split", 4),
        ("architecture (ingest, retrieve, generate)", 10), ("evaluation", 6),
        ("failure modes and safety", 6), ("cost and latency", 5), ("rollout", 4)]
assert sum(m for _, m in PLAN) == ROUND_MIN, "plan must fill the round"

# Each step: does it need language understanding, and can code check its output?
STEPS = {
    "authenticate user":            (False, True),
    "fetch the user's permissions": (False, True),
    "filter chunks by permission":  (False, True),
    "parse PDF/wiki to text":       (False, True),
    "rewrite follow-up question":   (True,  False),
    "retrieve candidate chunks":    (True,  True),   # embeddings: learned, but recall is measurable
    "write the answer":             (True,  False),
    "check each citation id exists":(False, True),
    "decide to abstain":            (True,  True),
    "redact PII in logs":           (False, True),
}
def owner(needs_language, checkable):
    if not needs_language:
        return "code"
    return "model + code check" if checkable else "model (needs eval/judge)"
print("Time plan (ASSUMED 45 min):")
for name, m in PLAN:
    print(f"  {m:>2} min  {name}")
print("\nDeterministic vs model split:")
for s, (nl, ck) in STEPS.items():
    print(f"  {s:<32}-> {owner(nl, ck)}")

AREAS = ["users", "inputs/outputs", "data+sensitivity", "latency", "quality bar",
         "volume", "build vs buy", "architecture", "evaluation", "failure modes",
         "safety", "cost", "rollout"]
def coverage(answer_areas):
    miss = [a for a in AREAS if a not in answer_areas]
    return len(AREAS) - len(miss), miss
weak = {"architecture", "latency", "users"}                  # "boxes and arrows" answer
strong = set(AREAS) - {"build vs buy"}
for label, a in [("boxes-and-arrows answer", weak), ("framework answer", strong)]:
    got, miss = coverage(a)
    print(f"\n{label}: covers {got}/{len(AREAS)}; missing: {miss}")
# Test: the split is exhaustive and ACL steps never go to the model.
assert all(owner(*STEPS[s]) == "code" for s in ["filter chunks by permission", "authenticate user"])
print("\ntests passed")
```
**Output (my run):**
```
Time plan (ASSUMED 45 min):
  10 min  requirements and scope
   4 min  deterministic vs model split
  10 min  architecture (ingest, retrieve, generate)
   6 min  evaluation
   6 min  failure modes and safety
   5 min  cost and latency
   4 min  rollout

Deterministic vs model split:
  authenticate user               -> code
  fetch the user's permissions    -> code
  filter chunks by permission     -> code
  parse PDF/wiki to text          -> code
  rewrite follow-up question      -> model (needs eval/judge)
  retrieve candidate chunks       -> model + code check
  write the answer                -> model (needs eval/judge)
  check each citation id exists   -> code
  decide to abstain               -> model + code check
  redact PII in logs              -> code

boxes-and-arrows answer: covers 3/13; missing: ['inputs/outputs', 'data+sensitivity', 'quality bar', 'volume', 'build vs buy', 'evaluation', 'failure modes', 'safety', 'cost', 'rollout']

framework answer: covers 12/13; missing: ['build vs buy']

tests passed
```

**Follow-ups:**
- *You are cut off at minute 20. What do you drop?* Keep requirements, the code/model split and one deep dive (retrieval with permissions). Say out loud which areas you would cover next (evaluation, cost, rollout).
- *The interviewer will not answer requirements questions.* Pick numbers, label them ASSUMED, and say which one would flip the design.
- *When is no model the right answer?* When search over a well-structured source already answers it. Say that before reaching for generation.

**Common mistakes:** Drawing boxes before asking who may see what; saying "RAG" and stopping; putting permission checks in the prompt; leaving evaluation and rollout to the last 30 seconds; quoting vendor numbers as facts; never saying what you would not build.

### Q2 ⭐⭐⭐ 🟡 Back-of-envelope for a GenAI launch: 2 million monthly users, 20 per cent daily active, 6 questions each, a RAG prompt of about 3,000 input tokens and 400 output tokens. Estimate QPS and peak QPS, tokens per day, API cost or GPU count under stated assumptions, KV-cache memory and embedding or index size, and say which numbers you would verify first. (Part 6 Q32 and Q33, Part 10 Q3, Q4 and Q13 give the building blocks; prices and GPU throughput must be stated as assumptions.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
**Say this first (1 line):** About 2.4 million queries a day is roughly 28 QPS average and about 160 at the peak under my assumptions; the real cost is the 3,000 input tokens per query, and every number except the user count has to be verified first.

**Then explain:**
- **From the prompt (given):** 2M monthly users x 20% daily active = 400,000 DAU; x 6 questions = 2.4M queries/day; 2.4M / 86,400 s = 27.8 QPS average.
- **Peak QPS is an assumption, not arithmetic.** I assumed the busiest hour carries 12% of daily traffic (80 QPS) and the busiest second runs 2x the hourly average (160 QPS). Measure the real traffic shape; B2B office-hours traffic can be far spikier than consumer traffic.
- **Tokens:** 2.4M x 3,000 = 7.2B input and 2.4M x 400 = 0.96B output tokens a day. Input dominates volume, output dominates latency (generated one token at a time; Part 10 Q13 for cost per token).
- **Cost or GPUs, both under labelled assumptions.** API: placeholder prices of USD 1 and USD 4 per million input and output tokens give USD 11,040 a day, USD 4.60 per 1,000 queries. GPUs: assumed 15,000 prefill tokens/s and 2,000 decode tokens/s per GPU at 50% utilisation gives 64 + 64 = 128 GPU-equivalents at peak. These throughput figures are placeholders, not measurements (Part 10 Q3, Q4).
- **KV cache (Part 1 Q15, Part 10 Q4):** assumed Llama-style 8B shape (32 layers, 8 KV heads, head dim 128, fp16): 128 KiB per token, 0.42 GiB per 3,400-token request. Little's law (peak QPS x 8 s assumed duration) gives 1,280 concurrent requests, 531 GiB of KV across them, i.e. the cache, not the weights, is the capacity limit.
- **Index (Part 6 Q32, Q33):** assumed 3M chunks of 768 dimensions: 8.6 GiB fp32, 2.1 GiB int8, 11.2 GiB with 30% graph overhead. Small next to generation.
- **Verify first:** peak shape, real tokens per request (how many chunks do you really send?), throughput on your model and hardware, cache hit rate, and prices.

**Example:** Sensitivity from the run: doubling the peak-hour share takes 128 to 256 GPU-equivalents, doubling input tokens (6,000) gives 192, halving decode throughput gives 192. So the 3,000-token prompt and the traffic shape matter more than the index. Levers: send fewer or shorter chunks, prefix or prompt caching, a smaller model for easy queries (Q3), an answer cache. Everything above is ASSUMED except the user figures given in the question.

**Code:** (mock LLMs and toy data; synthetic inputs labelled in the code)
```python
# Back-of-envelope for the launch. User figures come from the question;
# every line marked ASSUMED is a placeholder to be replaced by your own measurement.
MAU = 2_000_000; DAU_SHARE = 0.20; Q_PER_DAU = 6
IN_TOK = 3000; OUT_TOK = 400
PEAK_HOUR_SHARE = 0.12      # ASSUMED: busiest hour carries 12% of daily traffic
BURST = 2.0                 # ASSUMED: busiest second vs hourly average
LATENCY_S = 8.0             # ASSUMED: mean request duration incl. generation
PRICE_IN, PRICE_OUT = 1.0, 4.0   # ASSUMED USD per million tokens (placeholder, not a vendor price)
PREFILL_TPS = 15000.0       # ASSUMED prefill tokens/s per GPU
DECODE_TPS = 2000.0         # ASSUMED aggregate decode tokens/s per GPU at batch
GPU_UTIL = 0.5              # ASSUMED safe utilisation
# KV cache: ASSUMED Llama-style 8B shape: 32 layers, 8 KV heads, head dim 128, fp16
LAYERS, KV_HEADS, HD, BYTES = 32, 8, 128, 2
# Index: ASSUMED 3M chunks, 768-dim, float32 vs int8, plus 30% graph overhead
CHUNKS, DIM = 3_000_000, 768

dau = MAU * DAU_SHARE
qpd = dau * Q_PER_DAU
avg_qps = qpd / 86400
peak_hour_qps = qpd * PEAK_HOUR_SHARE / 3600
peak_qps = peak_hour_qps * BURST
print(f"DAU {dau:,.0f} | queries/day {qpd:,.0f} | avg QPS {avg_qps:.1f} | peak-hour QPS {peak_hour_qps:.1f} | peak QPS {peak_qps:.1f}")
tin, tout = qpd * IN_TOK, qpd * OUT_TOK
print(f"tokens/day: input {tin/1e9:.2f}B, output {tout/1e9:.2f}B")
cost_day = tin/1e6*PRICE_IN + tout/1e6*PRICE_OUT
print(f"API cost/day at ASSUMED prices: ${cost_day:,.0f}  (${cost_day*30:,.0f}/30d, ${cost_day/qpd*1000:.2f} per 1,000 queries)")
# GPU count at peak
pre_gpu = peak_qps * IN_TOK / (PREFILL_TPS * GPU_UTIL)
dec_gpu = peak_qps * OUT_TOK / (DECODE_TPS * GPU_UTIL)
print(f"GPUs for prefill {pre_gpu:.1f}, for decode {dec_gpu:.1f} -> they share a GPU, so sum of time shares = {pre_gpu+dec_gpu:.1f}")
# Concurrency by Little's law and KV memory
conc = peak_qps * LATENCY_S
kv_per_tok = 2 * LAYERS * KV_HEADS * HD * BYTES
kv_seq = kv_per_tok * (IN_TOK + OUT_TOK)
print(f"concurrent requests at peak (Little's law) {conc:.0f}; KV/token {kv_per_tok/1024:.0f} KiB; KV/request {kv_seq/2**30:.2f} GiB; all concurrent {conc*kv_seq/2**30:.1f} GiB")
# Index
raw32 = CHUNKS*DIM*4/2**30; raw8 = CHUNKS*DIM/2**30
print(f"index vectors: fp32 {raw32:.1f} GiB, int8 {raw8:.1f} GiB; with 30% overhead fp32 {raw32*1.3:.1f} GiB")
# Embedding queries are cheap: one 20-token query vs generation
print(f"query embedding tokens/day (20 tok each): {qpd*20/1e6:.0f}M")
# Sensitivity: which assumption moves the answer most? Vary each by 2x.
def gpus(pk=PEAK_HOUR_SHARE, inn=IN_TOK, dec=DECODE_TPS):
    q = qpd*pk/3600*BURST
    return q*inn/(PREFILL_TPS*GPU_UTIL) + q*OUT_TOK/(dec*GPU_UTIL)
base = gpus()
print(f"\nbase GPU-equivalents {base:.1f}")
for nm, v in [("peak share x2", gpus(pk=PEAK_HOUR_SHARE*2)), ("input tokens x2", gpus(inn=IN_TOK*2)), ("decode throughput /2", gpus(dec=DECODE_TPS/2))]:
    print(f"  {nm:<22}-> {v:.1f}")
# test: cost identity
assert abs(cost_day - (tin*PRICE_IN + tout*PRICE_OUT)/1e6) < 1e-6
print("tests passed")
```
**Output (my run):**
```
DAU 400,000 | queries/day 2,400,000 | avg QPS 27.8 | peak-hour QPS 80.0 | peak QPS 160.0
tokens/day: input 7.20B, output 0.96B
API cost/day at ASSUMED prices: $11,040  ($331,200/30d, $4.60 per 1,000 queries)
GPUs for prefill 64.0, for decode 64.0 -> they share a GPU, so sum of time shares = 128.0
concurrent requests at peak (Little's law) 1280; KV/token 128 KiB; KV/request 0.42 GiB; all concurrent 531.2 GiB
index vectors: fp32 8.6 GiB, int8 2.1 GiB; with 30% overhead fp32 11.2 GiB
query embedding tokens/day (20 tok each): 48M

base GPU-equivalents 128.0
  peak share x2         -> 256.0
  input tokens x2       -> 192.0
  decode throughput /2  -> 192.0
tests passed
```

**Follow-ups:**
- *API or self-host?* Compare cost per million tokens at your utilisation, plus on-call and privacy (Part 10 Q18). At low or spiky volume the API usually wins; the break-even needs your own throughput measurement.
- *How does a 128 KiB-per-token KV cache change if the model has no GQA?* It multiplies by heads/KV heads (for example 4x for 32 vs 8 heads).
- *What would you cache?* Embeddings of repeated queries and the retrieval results; answers only with tenant and permission in the key (Part 10 Q28, Q5 here).

**Common mistakes:** Treating average QPS as the sizing number; forgetting that input tokens dominate cost in RAG; quoting a vendor price or GPU throughput as fact; sizing weights but not KV cache; ignoring retries and cold starts; giving one number with no range.

### Q3 ⭐⭐⭐ 🟡 Model selection, build-vs-buy and routing for a product: given a support, a coding and a document-extraction workload, how do you choose between a frontier API, a mid-size hosted model and a self-hosted small model, using your own eval set, latency, cost, data-residency and lock-in, and when do you add a router or cascade? (Part 4 Q25, Part 9 Q35, Part 10 Q18 and Q28 cover the pieces; this question is the decision across a whole product.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
**Say this first (1 line):** Choose per workload, not per product: build an eval set for each, find the cheapest model whose lower confidence bound clears the quality bar, filter by data residency, and add a cascade only where the measured savings beat the router's own cost and complexity.

**Then explain:**
- **Start from the bar.** For each workload (support, coding, extraction) define the bar and the cost of a wrong answer. Extraction with a checksum (Q7) tolerates a cheaper model; coding usually does not.
- **Run candidates on your own eval set** (Part 9 Q2, Q35). Compare the lower confidence bound, not the point estimate: with 150 items per workload the 95% interval is several points wide.
- **Constraints before price:** data residency, latency, lock-in, licence. They remove candidates; cost then ranks what is left (Part 10 Q18 for the self-host break-even, Part 4 Q25 for fine-tuned small models).
- **Router or cascade only after measuring.** A cascade runs the cheap model first and escalates on low confidence or failed validation (Part 10 Q28). It helps when most traffic is easy and the confidence signal is reliable. It costs more than it saves when the escalation rate is high, the confidence signal is weak, or the extra latency of a second call breaks the budget. RouteLLM's authors claim more than a 2x cost cut in their own setting (arXiv abstract); I do not quote figures beyond that.
- **Keep an exit.** Put a gateway in front (Part 11 Q14) and keep eval sets and prompts portable so a vendor change is a re-run, not a rewrite.

**Example:** In the toy run (MOCK models: each is a coin with an ASSUMED success rate per workload, 150 eval items each), only the frontier model clears the bars on support, coding and extraction, and with a residency rule (only mid-hosted and small-self are in-country) no model passes any workload. That is the honest result of a small eval: mid-hosted extraction scored 0.947 with a lower bound of 0.898 against a 0.90 bar, missing by 0.002. Real decisions here are: gather more eval items, relax the bar knowingly, fine-tune the small model, or negotiate residency with the vendor. The cascade for support (small first, escalate when a confidence check flags it; flagging power ASSUMED; errors of the two models assumed independent, which flatters it) escalated 23.8% of requests and cost 3.65 per 1,000 vs 12.00 for always-frontier (assumed unit costs). Real error correlation will make the quality number worse.

**Code:** (mock LLMs and toy data; synthetic inputs labelled in the code)
```python
# Eval-driven model selection with a quality bar, residency filter and a cascade.
# MOCK: "models" are Bernoulli coins whose success rates are ASSUMED (synthetic), not real model scores.
import random, math
random.seed(7)
N = 150                                    # eval items per workload (your own golden set)
MODELS = {  # name: (cost USD per 1k requests ASSUMED, latency s ASSUMED, in_country, p_by_workload ASSUMED)
    "frontier-api": (12.0, 3.0, False, {"support": .93, "coding": .90, "extract": .96}),
    "mid-hosted":   (3.0,  1.5, True,  {"support": .88, "coding": .72, "extract": .93}),
    "small-self":   (0.8,  0.6, True,  {"support": .80, "coding": .45, "extract": .91}),
}
BAR = {"support": .85, "coding": .80, "extract": .90}       # ASSUMED product quality bars

def wilson_lower(k, n, z=1.96):
    p = k/n; d = 1 + z*z/n
    c = p + z*z/(2*n); r = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return (c - r)/d
def exact_lower(k, n, alpha=0.025):       # Clopper-Pearson lower bound by bisection on the binomial tail
    def tail(p): return sum(math.comb(n, i)*p**i*(1-p)**(n-i) for i in range(k, n+1))
    lo, hi = 0.0, k/n
    for _ in range(60):
        mid = (lo+hi)/2
        if tail(mid) < alpha: lo = mid
        else: hi = mid
    return (lo+hi)/2
# Test the interval code against the exact one on a known case (k=50,n=100: both near 0.40)
assert abs(wilson_lower(50, 100) - exact_lower(50, 100)) < 0.01, (wilson_lower(50,100), exact_lower(50,100))

results = {}
for w in BAR:
    for m, (cost, lat, inc, ps) in MODELS.items():
        k = sum(random.random() < ps[w] for _ in range(N))   # run the model on N eval items
        results[(w, m)] = (k, k/N, wilson_lower(k, N))

def choose(w, need_in_country):
    ok = [(MODELS[m][0], m) for m in MODELS
          if results[(w, m)][2] >= BAR[w] and (MODELS[m][2] or not need_in_country)]
    return min(ok)[1] if ok else None
print(f"{'workload':<9}{'model':<14}{'acc':>6}{'95% low':>9}{'cost/1k':>9}  meets bar?")
for w in BAR:
    for m in MODELS:
        k, a, lo = results[(w, m)]
        print(f"{w:<9}{m:<14}{a:>6.3f}{lo:>9.3f}{MODELS[m][0]:>9.1f}  {'yes' if lo >= BAR[w] else 'no'}")
print()
for w in BAR:
    print(f"{w}: cheapest passing = {choose(w, False)} | if data must stay in-country = {choose(w, True)}")

# Cascade for support (errors of small and frontier assumed INDEPENDENT, which is optimistic): small answers; a confidence check (ASSUMED 80% recall of wrong answers, 10% false alarms)
# escalates to frontier. Compare quality/cost against always-frontier, same coin flips per item.
random.seed(11)
M = 20000; small_p = MODELS["small-self"][3]["support"]; big_p = MODELS["frontier-api"][3]["support"]
ok = esc = 0
for _ in range(M):
    small_ok = random.random() < small_p
    flag = (random.random() < .80) if not small_ok else (random.random() < .10)
    if flag:
        esc += 1; ok += random.random() < big_p
    else:
        ok += small_ok
cost = (MODELS["small-self"][0] + esc/M*MODELS["frontier-api"][0])
print(f"\ncascade (support, synthetic): quality {ok/M:.3f} vs always-frontier {big_p:.2f} | escalated {esc/M:.1%} | cost/1k {cost:.2f} vs {MODELS['frontier-api'][0]:.2f}")
assert cost < MODELS["frontier-api"][0]
print("tests passed")
```
**Output (my run):**
```
workload model            acc  95% low  cost/1k  meets bar?
support  frontier-api   0.947    0.898     12.0  yes
support  mid-hosted     0.847    0.780      3.0  no
support  small-self     0.813    0.743      0.8  no
coding   frontier-api   0.900    0.842     12.0  yes
coding   mid-hosted     0.733    0.657      3.0  no
coding   small-self     0.520    0.441      0.8  no
extract  frontier-api   0.960    0.915     12.0  yes
extract  mid-hosted     0.947    0.898      3.0  no
extract  small-self     0.947    0.898      0.8  no

support: cheapest passing = frontier-api | if data must stay in-country = None
coding: cheapest passing = frontier-api | if data must stay in-country = None
extract: cheapest passing = frontier-api | if data must stay in-country = None

cascade (support, synthetic): quality 0.941 vs always-frontier 0.93 | escalated 23.8% | cost/1k 3.65 vs 12.00
tests passed
```

**Follow-ups:**
- *Why a lower bound?* A point estimate of 0.95 on 150 items is compatible with a true rate near 0.90. The code checks the Wilson bound against an exact Clopper-Pearson bound (assert inside).
- *When do you fine-tune instead of routing?* When a narrow task has plenty of labels and a small model can meet the bar (Part 4 Q25).
- *How do you detect that the router is hurting?* Log escalations, sample both paths, and compare end quality and total cost against always-large on the same traffic.

**Common mistakes:** Choosing by leaderboard or by brand; comparing point estimates on tiny eval sets; ignoring residency until legal asks; adding a router before measuring the traffic mix; assuming independent errors in a cascade; one model for all workloads.

### Q4 ⭐⭐⭐ 🟡 Prompting vs RAG vs fine-tuning vs long context, applied: for (a) an HR-policy assistant, (b) a tone-and-format-sensitive marketing writer and (c) a claims-ticket classifier with 50,000 labelled examples, which do you pick first, what evidence would make you change, and in what order do you spend engineering effort? (Part 4 Q1, Part 6 Q13 and Part 7 Q36 give the framework; this applies it to concrete products.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
**Say this first (1 line):** HR policy: RAG with citations first. Marketing writer: prompting with examples and a style guide first. Claims classifier: a trained classifier on the 50,000 labels first, with a prompted LLM as the baseline to beat; each choice changes only if a measured failure says so.

**Then explain:**
- **The framework (Part 4 Q1, Part 6 Q13, Part 7 Q36):** prompting changes behaviour, RAG supplies knowledge that changes or is private, fine-tuning changes consistent behaviour or style at scale, long context replaces retrieval only when the corpus is small enough and the cost is acceptable.
- **(a) HR-policy assistant:** the knowledge is private, changes and needs citations, so RAG. Fine-tuning would freeze a snapshot. If the whole policy set fits the context window and volume is low, plain long context with caching is the simplest start (Part 7 Q36). Change when: retrieval recall is the failure (fix chunking and hybrid search first), or tone is the failure (add prompt rules).
- **(b) Marketing writer:** the problem is style and format, not knowledge. Start with a clear brief, a style guide and 3 to 5 good examples; add an automatic format check. Move to fine-tuning only if a rubric or A/B shows the prompt cannot hold the style, or the long style prompt is a real cost at your volume.
- **(c) Claims classifier with 50,000 labels:** a closed label set with lots of data suits a supervised model: cheap, fast, testable. Prompt an LLM first only as a baseline and to find label errors. Use the LLM for rare or new categories or as a fallback on low-confidence tickets.
- **Order of effort:** build the eval set first (Part 9 Q2), then the cheapest method that passes, then the next only against measured failures.

**Example:** Toy run (synthetic; the data and the "few-shot proxy" are mine, not a real LLM): for the claims classifier, a trained softmax model improves with data: 0.414 accuracy on 60 labelled tickets, 0.562 on 600, 0.701 on 6,000, 0.730 on 50,000 (8% label noise in training, clean test labels). The curve flattens by 6,000, so the first thing to check with 50,000 labels is label quality and the feature ceiling, not model size. The few-shot proxy (a class-mean classifier from 5 noisy examples per class) scored 0.330; a real LLM prompt could do better because it brings language knowledge, so this only shows the shape, not that prompting loses. For HR policy: if 6 of 40 policies change after training, a frozen snapshot answers 0.869 of questions correctly while lookup over live documents answers 1.000 (an upper bound, since it ignores retrieval misses).

**Code:** (mock LLMs and toy data; synthetic inputs labelled in the code)
```python
# Toy evidence for "which adaptation first". Synthetic data, numpy only. Not a benchmark.
import numpy as np
rng = np.random.default_rng(0)
# ---- (c) claims-ticket classifier: learning curve of a trained model vs a few-shot-style prototype proxy
K, V, L = 6, 300, 25            # classes, vocabulary, tokens per ticket (ASSUMED synthetic)
topic = rng.dirichlet(np.ones(V)*0.05, size=K)      # per-class word distribution (peaky)
bg = np.ones(V)/V
def make(n, mix=0.12, noise=0.08):
    y = rng.integers(0, K, n)
    X = np.zeros((n, V))
    for i, c in enumerate(y):
        p = mix*topic[c] + (1-mix)*bg
        X[i] = rng.multinomial(L, p)
    flip = rng.random(n) < noise                      # label noise in the stored labels
    y_lab = np.where(flip, rng.integers(0, K, n), y)
    return X, y, y_lab
Xte, yte, _ = make(4000, noise=0.0)
def train_softmax(X, y, epochs=300, lr=0.05, l2=1e-3):
    n = len(X); Xn = X / X.sum(1, keepdims=True) * 10          # scaled term frequencies
    W = np.zeros((V, K)); b = np.zeros(K); Y = np.eye(K)[y]
    mW = vW = np.zeros_like(W); mb = vb = np.zeros_like(b)
    for t in range(1, epochs+1):                                # Adam, full batch
        Z = Xn @ W + b; Z -= Z.max(1, keepdims=True)
        P = np.exp(Z); P /= P.sum(1, keepdims=True)
        G = (P - Y) / n
        gW = Xn.T @ G + l2*W; gb = G.sum(0)
        mW = .9*mW + .1*gW; vW = .999*vW + .001*gW**2
        mb = .9*mb + .1*gb; vb = .999*vb + .001*gb**2
        W -= lr*(mW/(1-.9**t))/(np.sqrt(vW/(1-.999**t))+1e-8)
        b -= lr*(mb/(1-.9**t))/(np.sqrt(vb/(1-.999**t))+1e-8)
    return W, b
def acc(W, b, X, y):
    return float(((X/X.sum(1, keepdims=True)*10 @ W + b).argmax(1) == y).mean())
def prototype_acc(shots):    # proxy for few-shot prompting: class mean of `shots` examples per class
    X, y, yl = make(shots*K*4)
    keep = np.concatenate([np.where(yl == c)[0][:shots] for c in range(K)])
    P = np.stack([X[keep][yl[keep] == c].mean(0) if (yl[keep] == c).any() else np.zeros(V) for c in range(K)])
    P = P/ (np.linalg.norm(P, axis=1, keepdims=True)+1e-9)
    Xn = Xte / np.linalg.norm(Xte, axis=1, keepdims=True)
    return float(((Xn @ P.T).argmax(1) == yte).mean())
print("(c) claims classifier, synthetic data, test labels clean")
print(f"  few-shot proxy (5 shots/class): acc {prototype_acc(5):.3f}")
curve = []
for n in [60, 600, 6000, 50000]:
    X, y, yl = make(n)
    W, b = train_softmax(X, yl)
    curve.append(acc(W, b, Xte, yte))
    print(f"  trained on {n:>6} labelled (8% label noise): acc {acc(W, b, Xte, yte):.3f}")
# ---- (a) HR policy: answers must follow policy changes. Snapshot (fine-tuned) vs retrieval over live docs
P = 40; changed = 0
policy = {f"p{i}": rng.integers(10, 30) for i in range(P)}       # e.g. days of leave
snapshot = dict(policy)                                           # model memorised at training time
for i in rng.choice(P, 6, replace=False):                         # 6 policies edited after training
    policy[f"p{i}"] = policy[f"p{i}"] + 5; changed += 1
qs = [f"p{rng.integers(0, P)}" for _ in range(1000)]
ft = np.mean([snapshot[q] == policy[q] for q in qs]); rag = np.mean([policy[q] == policy[q] for q in qs])
print(f"\n(a) {changed}/{P} policies edited after training: snapshot-model correct {ft:.3f}, lookup over live docs {rag:.3f}")
print("    (lookup ignores retrieval misses here; real RAG recall is below 1.0)")
assert curve == sorted(curve) and 0.7 < ft < 1.0 and rag == 1.0
print("tests passed")
```
**Output (my run):**
```
(c) claims classifier, synthetic data, test labels clean
  few-shot proxy (5 shots/class): acc 0.330
  trained on     60 labelled (8% label noise): acc 0.414
  trained on    600 labelled (8% label noise): acc 0.562
  trained on   6000 labelled (8% label noise): acc 0.701
  trained on  50000 labelled (8% label noise): acc 0.730

(a) 6/40 policies edited after training: snapshot-model correct 0.869, lookup over live docs 1.000
    (lookup ignores retrieval misses here; real RAG recall is below 1.0)
tests passed
```

**Follow-ups:**
- *What if the HR corpus is only 30 pages?* Try long context first; measure cost per question and quality against RAG (Part 7 Q36).
- *The marketing prompt is 2,000 tokens of style rules. Now what?* Compare prompt caching against a fine-tune on approved copy; fine-tune if style drift remains and volume is high.
- *Fine-tune the classifier or the LLM?* A small encoder or classic model usually first; an LLM fine-tune only if the labels need reasoning over long text (Part 4 Q43 for an extraction project).

**Common mistakes:** Fine-tuning to inject facts that change; building RAG for a 30-page corpus; skipping the baseline (a bag-of-words model) before an LLM; trusting 50,000 labels without auditing them; judging a style task by exact match; changing three things at once.

### Q5 ⭐⭐⭐ 🔴 Design an enterprise knowledge assistant over millions of documents in many systems (drive, wiki, tickets, chat) where each user may see only what they are permitted to see: connectors and ACL sync, ingestion and freshness, deletes and permission changes, hybrid retrieval with rerank, citations, evaluation, security and rollout. Focus on the integrated view: what breaks when a document's permissions change at 10:02 and a user asks at 10:03? (Part 6 Q15, Q19, Q20, Q42, Part 7 Q2 and Q5, Part 11 Q26 hold the parts; Part 6 Q50 and Part 7 Q43 are narrower designs.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
**Say this first (1 line):** At 10:03 the question is whether the system still believes the 10:02 permission, so I filter inside the search using fresh ACL metadata, re-check the surviving chunks against the source of truth, key every cache by permissions, and fail closed when the permission service is unavailable.

**Then explain:**
- **Where the old permission can still live:** (1) the ACL copied into the index at ingest time, updated by a sync that lags; (2) caches of answers or retrieval results; (3) snippets or text already shown in the conversation; (4) group membership: a user removed from a group changes many documents at once; (5) deletes that have not reached the index.
- **Filter inside the search, not after top-k.** Post-filtering returns fewer results or none when forbidden chunks outrank allowed ones (Part 6 Q15). Store principals as chunk metadata and apply them in the ANN or keyword query.
- **Separate the ACL path from the content path.** A permission change is a small metadata update, not a re-embedding. Run it on its own fast queue with a stated freshness target (an SLO) and alert on lag.
- **Query-time re-check (defence in depth).** After retrieval, ask the source system or a permission cache with a short time-to-live about the final k chunks only. It closes the sync-lag window at the cost of k lookups. If that service is down, fail closed: answer with fewer sources or refuse.
- **Cache keys include the user's principals and an ACL version** (Part 11 Q26). Deletes use tombstones and are checked at query time (Part 6 Q19, Q20).
- **Hybrid retrieval and rerank** run only on the already-filtered candidates (Part 7 Q2, Q5). Citations are chunk ids, so a rerank cannot invent a source. Test with leakage suites, not with vibes (Q39 of this part builds one).
- **Rollout:** start with one connector, shadow-check permissions against the source, and gate on zero leaks in the red-team suite (Part 6 Q42).

**Example:** Toy timeline (MOCK: word-overlap retrieval, four documents, seconds since 10:00): d1 is revoked for Alice's group at 10:02; Alice asks at 10:03. With the index ACL synced on a 5-minute lag and no re-check, Alice receives ['d1', 'd3'] and d1 leaks. With the same lag plus a source re-check she gets ['d3'] and nothing leaks. With a 30-second sync alone she also gets ['d3'] (a lagging sync is only safe if the lag is below the time to the next question, which you cannot assume). Post-filtering test: a user in group "all" only, with k=1, gets [] from post-filtering but ['d3'] from in-search filtering; at k=2 both return ['d3']. Cache test: without permissions in the key Bob receives an answer built for Alice; with (query, groups, acl_version) he does not.

**Code:** (mock LLMs and toy data; synthetic inputs labelled in the code)
```python
# Mini enterprise-RAG ACL timeline: permission revoked at 10:02:00, user asks at 10:03:00.
# Toy lexical retrieval (word overlap). Times in seconds since 10:00:00. No real systems.
DOCS = {  # doc_id: (text, groups allowed in the SOURCE system now)
    "d1": ("refund policy for travel claims", {"finance", "hr"}),
    "d2": ("salary bands for staff", {"hr"}),
    "d3": ("travel claims approval process", {"finance", "hr", "all"}),
    "d4": ("holiday calendar for staff", {"all", "hr", "finance"}),
}
USERS = {"alice": {"finance", "all"}, "bob": {"hr", "all"}}
class Source:                       # authoritative permission store
    def __init__(self): self.acl = {d: set(g) for d, (_, g) in DOCS.items()}; self.log = []
    def revoke(self, doc, group, t): self.acl[doc].discard(group); self.log.append((t, doc, group))
class Index:                        # chunk store with ACL COPIED at index time; sync lag applies
    def __init__(self, src, lag): self.src, self.lag, self.copy = src, lag, {d: set(g) for d, g in src.acl.items()}
    def sync(self, now):
        for t, d, g in self.src.log:
            if t + self.lag <= now: self.copy[d].discard(g)
    def search(self, q, groups, now, k, mode, recheck):
        self.sync(now); qw = set(q.split())
        scored = sorted(((len(qw & set(DOCS[d][0].split())), d) for d in DOCS), reverse=True)
        scored = [(s, d) for s, d in scored if s > 0]
        if mode == "post":          # top-k first, filter afterwards (wrong)
            hits = [d for s, d in scored[:k] if self.copy[d] & groups]
        else:                       # filter inside the search, then take top-k
            hits = [d for s, d in scored if self.copy[d] & groups][:k]
        if recheck:                 # defence in depth: ask the source of truth for the survivors
            hits = [d for d in hits if self.src.acl[d] & groups]
        return hits
def leaks(hits, user, src): return [d for d in hits if not (src.acl[d] & USERS[user])]
def run(mode, lag, recheck, k=2):
    src = Source(); idx = Index(src, lag)
    src.revoke("d1", "finance", t=120)            # 10:02 alice's group loses d1
    hits = idx.search("travel claims refund", USERS["alice"], now=180, k=k, mode=mode, recheck=recheck)
    return hits, leaks(hits, "alice", src)
print(f"{"design":<50}{'hits for alice at 10:03':<26}leaked")
for label, mode, lag, rc in [("filter in search, 5 min sync lag, no recheck", "in", 300, False),
                             ("filter in search, 5 min lag + source recheck", "in", 300, True),
                             ("filter in search, 30 s sync (<1 min)", "in", 30, False),
                             ("post-filter (top-k then filter), recheck", "post", 300, True)]:
    h, l = run(mode, lag, rc)
    print(f"{label:<50}{str(h):<26}{l}")
# Post-filter recall loss: alice may only see d3 and d4 for this query when d1/d2 outrank them at k=1
src = Source(); idx = Index(src, 0)
for k in (1, 2):
    ph = idx.search("refund policy travel claims", {"all"}, 0, k, "post", False)
    ih = idx.search("refund policy travel claims", {"all"}, 0, k, "in", False)
    print(f"user in group 'all' only, k={k}: post-filter -> {ph} | in-search filter -> {ih}")
# Cache: key MUST include the permission fingerprint; test it
cache = {}
def cached(q, user, version, bad=False):
    key = (q,) if bad else (q, tuple(sorted(USERS[user])), version)
    if key not in cache: cache[key] = f"answer built for {user}"
    return cache[key]
a = cached("travel", "alice", 1, bad=True); b = cached("travel", "bob", 1, bad=True)
print("\ncache without permission fingerprint: bob receives ->", b)
cache.clear(); a = cached("travel", "alice", 1); b = cached("travel", "bob", 1)
print("cache with (query, groups, acl_version) key: bob receives ->", b)
# Tests
assert run("in", 300, True)[1] == [] and run("in", 300, False)[1] == ["d1"]
assert b == "answer built for bob"
print("tests passed")
```
**Output (my run):**
```
design                                            hits for alice at 10:03   leaked
filter in search, 5 min sync lag, no recheck      ['d1', 'd3']              ['d1']
filter in search, 5 min lag + source recheck      ['d3']                    []
filter in search, 30 s sync (<1 min)              ['d3']                    []
post-filter (top-k then filter), recheck          ['d3']                    []
user in group 'all' only, k=1: post-filter -> [] | in-search filter -> ['d3']
user in group 'all' only, k=2: post-filter -> ['d3'] | in-search filter -> ['d3']

cache without permission fingerprint: bob receives -> answer built for alice
cache with (query, groups, acl_version) key: bob receives -> answer built for bob
tests passed
```

**Follow-ups:**
- *Can you afford a source re-check on every request?* For k around 5 to 10 it is a batched lookup, often against a short-lived permission cache; measure p95 added latency and set the cache time-to-live below your revocation promise.
- *A user is removed from a big group.* Index stores principals as group ids, not expanded users, so membership is resolved at query time from an identity service; no re-index.
- *What about text the user already saw?* You cannot unsee it; log it, and do not reuse it in later turns if the document is revoked (clear conversation memory entries tied to that document id).

**Common mistakes:** Applying ACLs to top-k results after search; trusting a nightly permission sync; caching answers without the user's permissions in the key; putting ACL logic in the prompt; deleting from the vector index but not from the keyword index or the cache; failing open when the permission service is down.

### Q6 ⭐⭐⭐ 🔴 Design a text-to-SQL analytics assistant for business users over a warehouse with hundreds of tables: schema retrieval and linking, a semantic layer or metric definitions, generation, validation (parse, read-only, allowlist, row and cost limits, dry run), execution, answer explanation, ambiguity handling, per-user access control, and evaluation by execution accuracy on your own questions. Why are public benchmark scores a poor guide? (Part 7 Q40 covers SQL as a tool inside RAG; this is the full product.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
**Say this first (1 line):** Treat the model as a query writer inside a controlled pipeline: retrieve only the relevant schema, resolve business terms through a semantic layer, generate, validate with a real parser and database permissions, run with limits, and measure execution accuracy on your own questions.

**Then explain:**
- **Schema retrieval and linking.** Hundreds of tables will not fit in a prompt. Retrieve the few tables and columns relevant to the question from descriptions, sample values and past queries; give the model only those.
- **Semantic layer.** Define metrics once ("revenue" = paid orders only) and let the model pick a metric rather than invent an expression. This turns many ambiguous questions into lookups.
- **Validation before execution:** parse; one SELECT only; table and column allowlist; row-level and column-level access per user; LIMIT; statement timeout; a dry run (EXPLAIN) or cost estimate. Enforce permissions in the database role or authorizer, not by string matching (Part 7 Q40 for SQL as a tool).
- **Ambiguity:** ask a clarifying question or state the definition used, because two reasonable readings can give different numbers.
- **Explanation:** show the SQL, the definition of each metric and the data's freshness; a wrong number with a confident sentence is the worst failure.
- **Evaluation:** execution accuracy (compare result sets, not SQL strings) on your own question set with your own definitions, sliced by table and question type, plus tests for blocked statements.
- **Why public benchmarks are a poor guide:** BIRD has 12,751 question-SQL pairs over 95 databases and Spider 10,181 questions over 200 (dataset sizes from the papers' abstracts). Your warehouse has hundreds of tables, your own metric definitions and dirty data. In the BIRD paper (2023) the best model reached 40.08% execution accuracy against 92.96% for humans; that is a dated figure, and later leaderboard systems and splits are not comparable, so I do not quote them.

**Example:** Toy warehouse on sqlite3 (3 tables, 5 orders), MOCK rule-based generator. Without the semantic layer "revenue" becomes SUM(amount), which counts a refunded and a cancelled order; execution accuracy on 4 questions is 2 of 4. With the layer 4 of 4, but note the circularity: the gold SQL and the layer share one definition, so this shows the mechanism (one definition for everyone), not a measured gain. The sqlite authorizer blocked a query on the employees table, a column outside the allowlist (customers.email), a DELETE and a two-statement string, and allowed customers.name. "February sales" is 320.0 gross or 280.0 paid-only: the answer must say which.

**Code:** (mock LLMs and toy data; synthetic inputs labelled in the code)
```python
# Text-to-SQL product skeleton on sqlite3 with a MOCK generator (rules, not a model).
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE orders(id INTEGER, customer_id INTEGER, amount REAL, status TEXT, region TEXT, ts TEXT);
CREATE TABLE customers(id INTEGER, name TEXT, email TEXT);
CREATE TABLE employees(id INTEGER, name TEXT, salary REAL);
INSERT INTO orders VALUES (1,1,100,'paid','north','2024-01-05'),(2,1,50,'refunded','north','2024-01-06'),
 (3,2,200,'paid','south','2024-02-01'),(4,3,80,'paid','north','2024-02-03'),(5,2,40,'cancelled','south','2024-02-09');
INSERT INTO customers VALUES (1,'Asha','a@x.test'),(2,'Ben','b@x.test'),(3,'Chen','c@x.test');
INSERT INTO employees VALUES (1,'Zed',99999);
""")
# Semantic layer: governed metric definitions, so "revenue" means one thing.
METRICS = {"revenue": "SUM(CASE WHEN status='paid' THEN amount ELSE 0 END)",
           "orders": "COUNT(*)"}
SCHEMA_DOC = {"orders": "order amount status region revenue sales", "customers": "customer name email",
              "employees": "employee salary payroll"}
def retrieve_tables(q, k=1):                 # schema retrieval: word overlap with table descriptions
    qw = set(q.lower().split())
    sc = sorted(((len(qw & set(d.split())), t) for t, d in SCHEMA_DOC.items()), reverse=True)
    return [t for s, t in sc[:k] if s > 0]
def mock_generate(q, use_semantic_layer):    # rule-based stand-in for an LLM
    ql = q.lower()
    metric = "revenue" if "revenue" in ql else "orders"
    expr = METRICS[metric] if use_semantic_layer else ("SUM(amount)" if metric == "revenue" else "COUNT(*)")
    by = " GROUP BY region" if "by region" in ql else ""
    sel = ("region, " if by else "") + expr
    return f"SELECT {sel} FROM orders{by} ORDER BY 1"
ALLOWED = {"orders": {"id", "customer_id", "amount", "status", "region", "ts"}, "customers": {"id", "name"}}
def authorizer(action, a1, a2, dbname, src):  # sqlite enforces the allowlist while PARSING (not string matching)
    if action == 21: return 0                  # SQLITE_SELECT
    if action == 20:                           # SQLITE_READ: a1=table, a2=column
        return 0 if a2 == "" or a2 in ALLOWED.get(a1, set()) else 1
    if action in (31, 33):                     # SQLITE_FUNCTION / RECURSIVE ok
        return 0
    return 1                                   # deny INSERT/UPDATE/DROP/ATTACH/PRAGMA...
def run_safely(sql, max_rows=100):
    if ";" in sql.strip().rstrip(";"): return ("blocked", "multiple statements")
    c = sqlite3.connect(":memory:"); db.backup(c); c.set_authorizer(authorizer)
    try:
        c.execute("EXPLAIN " + sql)           # dry run: parse + plan, no execution
        return ("ok", c.execute(f"SELECT * FROM ({sql.rstrip(';')}) LIMIT {max_rows}").fetchall())
    except sqlite3.Error as e:
        return ("blocked", str(e))
def exec_match(gold, pred):                    # compare result sets, order-insensitive
    return sorted(map(repr, db.execute(gold).fetchall())) == sorted(map(repr, pred))
QS = [("total revenue", "SELECT SUM(CASE WHEN status='paid' THEN amount ELSE 0 END) FROM orders"),
      ("revenue by region", "SELECT region, SUM(CASE WHEN status='paid' THEN amount ELSE 0 END) FROM orders GROUP BY region ORDER BY 1"),
      ("how many orders", "SELECT COUNT(*) FROM orders"),
      ("orders by region", "SELECT region, COUNT(*) FROM orders GROUP BY region ORDER BY 1")]
for use_sl in (False, True):
    ok = 0
    for q, gold in QS:
        st, rows = run_safely(mock_generate(q, use_sl))
        ok += st == "ok" and exec_match(gold, rows)
    print(f"semantic layer {'ON ' if use_sl else 'OFF'}: execution accuracy {ok}/{len(QS)}")
print("schema retrieval 'employee salary' ->", retrieve_tables("employee salary"), "| 'revenue by region' ->", retrieve_tables("revenue by region"))
# Validator tests
for label, sql in [("employees table", "SELECT salary FROM employees"),
                   ("customer email column", "SELECT email FROM customers"),
                   ("write attempt", "DELETE FROM orders"),
                   ("two statements", "SELECT 1; DROP TABLE orders"),
                   ("allowed column", "SELECT name FROM customers")]:
    print(f"  {label:<22}-> {run_safely(sql)[0]}")
# Ambiguity: two defensible readings of "sales last month" give different answers
a = db.execute("SELECT SUM(amount) FROM orders WHERE ts LIKE '2024-02%'").fetchone()[0]
b = db.execute("SELECT SUM(amount) FROM orders WHERE ts LIKE '2024-02%' AND status='paid'").fetchone()[0]
print(f"'February sales': gross {a} vs paid-only {b} -> ask or show the definition used")
assert run_safely("SELECT salary FROM employees")[0] == "blocked" and run_safely("DELETE FROM orders")[0] == "blocked"
print("tests passed")
```
**Output (my run):**
```
semantic layer OFF: execution accuracy 2/4
semantic layer ON : execution accuracy 4/4
schema retrieval 'employee salary' -> ['employees'] | 'revenue by region' -> ['orders']
  employees table       -> blocked
  customer email column -> blocked
  write attempt         -> blocked
  two statements        -> blocked
  allowed column        -> ok
'February sales': gross 320.0 vs paid-only 280.0 -> ask or show the definition used
tests passed
```

**Follow-ups:**
- *How do you stop a runaway query?* Statement timeout, row limit, a read replica or warehouse queue, and a cost estimate or dry run before execution.
- *How do you handle per-user access?* Run under the user's database role or inject row-level policies through views; never rely on the prompt.
- *What do you do when SQL is valid but the answer is wrong?* Log question, SQL and result; add it to the eval set with a corrected gold query; check whether the semantic layer lacks the term.

**Common mistakes:** Comparing SQL strings instead of result sets; letting the model define metrics; read-only enforced only by regex; putting the entire schema in the prompt; trusting a benchmark score for your warehouse; explaining results without the definition used.

### Q7 ⭐⭐⭐ 🔴 Design a document-extraction (IDP) pipeline for loan applications, KYC documents and invoices in an Indian bank or fintech: ingestion of scans and PDFs, OCR and layout parsing, LLM or vision-LLM extraction into a schema, rule-based cross-checks (checksums, format rules, cross-document consistency), confidence and human review queues, audit trail, PII handling, and accuracy measured per field. When does the LLM make it worse than OCR plus rules? (Part 6 Q17, Part 3 Q7, Part 9 Q32 and Part 11 Q11 are the building blocks.)
**Asked at:** BFSI and fintech GenAI teams, GCCs and product companies (company-type tag from guides and regulator material, not a candidate report)
**Say this first (1 line):** Use OCR and layout parsing to get text, let a model map it to a schema, and let deterministic rules (checksums, formats, arithmetic, cross-document checks) decide what is auto-accepted; route everything else to a human queue, with an audit trail and per-field accuracy.

**Then explain:**
- **Pipeline:** ingest scans and PDFs (virus scan, dedupe, classify document type) -> OCR and layout parsing (tables and key-value regions; Part 6 Q17) -> extraction into a typed schema (Part 3 Q7: schema validation and a bounded retry) -> validators -> confidence and review routing -> store with provenance.
- **Rules beat models where a rule exists.** 12-digit IDs carry a checksum (the Verhoeff scheme: I brute-forced it, below), PAN and IFSC have fixed formats (written from memory, check the issuer specs), invoice lines must sum to the subtotal and subtotal plus tax to the total, names must match across documents after normalisation.
- **Review queue:** anything failing a rule, any low-confidence field, and a random sample of passes for audit. Reviewers see the image crop beside the value.
- **Audit and PII:** keep the original, the extracted value, who or what changed it and when; mask PII in logs and traces, encrypt at rest, restrict reviewers (Part 11 Q11).
- **Accuracy per field, not per document:** a document is wrong if any critical field is wrong. Report precision, recall, the silent-error rate (wrong values that passed every check) and the review rate per field (Part 9 Q32).
- **When the LLM makes it worse:** on a field with no independent check, an LLM or vision-LLM can "repair" a smudged value into a clean, well-formed, wrong one. OCR gives garbage that fails a format check and gets reviewed; the LLM gives plausible text that passes.
- Regulation (data residency, retention, consent) is for compliance to confirm; I do not assert specific rules here.

**Example:** Toy run (synthetic IDs generated in the code, MOCK OCR with 5% per-character digit-letter confusions, MOCK LLM normaliser whose behaviour is ASSUMED: it always outputs digits, recovers the truth 40% of the time when the OCR was wrong, otherwise fills digits). The Verhoeff implementation was checked by brute force: 0 of 108 single-digit errors and 0 of 11 adjacent swaps pass. For the 12-digit ID with a checksum: OCR plus rules auto-accepts 74.3% correctly, 0% silent wrong, 25.8% to review; adding the LLM normaliser raises auto-correct to 85.1% and cuts review to 14.6%, at 0.25% silent wrong. For a 6-digit amount with a format check only: OCR plus rules 86.2% auto-correct, 0% silent wrong, 13.8% review; the LLM normaliser gets 91.9% auto-correct but 8.05% silent wrong and no review at all. Same model, opposite verdict, depending on whether a check exists. Caveat: my mock OCR only ever turns digits into letters, so OCR-only silent errors are 0 by construction; real OCR can also swap digit for digit.

**Code:** (mock LLMs and toy data; synthetic inputs labelled in the code)
```python
# Toy IDP: mock OCR with character confusions, rule validators (Verhoeff checksum, PAN format,
# invoice arithmetic), a mock "LLM normaliser" that always returns well-formed text, and review routing.
# All data synthetic. The 12-digit IDs below are generated here, not real identifiers.
import random, re
random.seed(3)
# ---- Verhoeff checksum (the scheme used for Indian 12-digit IDs; implemented from the public algorithm)
D = [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,0,6,7,8,9,5],[2,3,4,0,1,7,8,9,5,6],[3,4,0,1,2,8,9,5,6,7],[4,0,1,2,3,9,5,6,7,8],
     [5,9,8,7,6,0,4,3,2,1],[6,5,9,8,7,1,0,4,3,2],[7,6,5,9,8,2,1,0,4,3],[8,7,6,5,9,3,2,1,0,4],[9,8,7,6,5,4,3,2,1,0]]
P = [[0,1,2,3,4,5,6,7,8,9],[1,5,7,6,2,8,3,0,9,4],[5,8,0,3,7,9,6,1,4,2],[8,9,1,6,0,4,3,5,2,7],
     [9,4,5,3,1,2,6,8,7,0],[4,2,8,6,5,7,3,9,0,1],[2,7,9,3,8,0,6,4,1,5],[7,0,4,6,9,1,3,2,5,8]]
INV = [0,4,3,2,1,5,6,7,8,9]
def verhoeff_ok(s):
    if not (s.isdigit() and len(s) == 12): return False   # letters from OCR confusion fail format first
    c = 0
    for i, ch in enumerate(reversed(s)): c = D[c][P[i % 8][int(ch)]]
    return c == 0
def make_id(n11):
    for chk in "0123456789":
        if verhoeff_ok(n11 + chk): return n11 + chk
# brute-force check of the algorithm's known guarantees: all single-digit errors and adjacent swaps caught
base = make_id("23456789012"); assert verhoeff_ok(base)
single = sum(verhoeff_ok(base[:i] + d + base[i+1:]) for i in range(12) for d in "0123456789" if d != base[i])
swaps = sum(verhoeff_ok(base[:i] + base[i+1] + base[i] + base[i+2:]) for i in range(11) if base[i] != base[i+1])
assert single == 0 and swaps == 0, (single, swaps)
print(f"verhoeff: {single} of 108 single-digit errors and {swaps} of {sum(base[i]!=base[i+1] for i in range(11))} adjacent swaps pass the check")
PAN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")      # PAN layout from memory: check with the issuer's spec
CONF = {"0": "O", "1": "I", "5": "S", "8": "B", "2": "Z"}
def mock_ocr(text, err=0.05):                      # confusion errors, each char with prob err
    inv = {**CONF, **{v: k for k, v in CONF.items()}}
    return "".join(inv.get(c, c) if random.random() < err else c for c in text)
def mock_llm_normalise(ocr_text, true_text):       # ASSUMED behaviour: output is always digits-only (well-formed);
    if ocr_text == true_text: return ocr_text      # when the OCR was wrong it recovers the truth 40% of the time,
    if random.random() < .4: return true_text      # otherwise it fills the bad characters with plausible digits
    return "".join(c if c.isdigit() else random.choice("0123456789") for c in ocr_text)
N = 4000
ids = [make_id(random.choice("23456789") + "".join(random.choice("0123456789") for _ in range(10))) for _ in range(N)]
amounts = ["".join(random.choice("0123456789") for _ in range(6)) for _ in range(N)]   # field with NO checksum
def evaluate(values, valid, pipeline):
    correct = silent_wrong = review = 0
    for t in values:
        o = mock_ocr(t)
        v = o if pipeline == "ocr_rules" else mock_llm_normalise(o, t)
        if valid(v) and v == t: correct += 1
        elif valid(v): silent_wrong += 1               # wrong value that passes every check
        else: review += 1                              # fails a check: a human looks
    return correct/N, silent_wrong/N, review/N
for field, vals, valid in [("12-digit id (checksum)", ids, verhoeff_ok), ("6-digit amount (format only)", amounts, lambda s: s.isdigit() and len(s) == 6)]:
    for pipe in ("ocr_rules", "llm_normaliser"):
        c, s_, r = evaluate(vals, valid, pipe)
        print(f"{field:<30}{pipe:<16} auto-correct {c:.3f} | silent wrong {s_:.4f} | to human {r:.3f}")
# Invoice arithmetic cross-check and cross-document name match
def invoice_ok(lines, subtotal, tax, total): return abs(sum(lines) - subtotal) < .01 and abs(subtotal + tax - total) < .01
print("invoice ok:", invoice_ok([100, 250.5], 350.5, 63.09, 413.59), "| OCR dropped a digit:", invoice_ok([100, 250.5], 350.5, 63.09, 41.59))
def name_key(s): return sorted(re.sub(r"[^a-z ]", "", s.lower()).split())
print("name match 'Rao Asha K' vs 'ASHA K RAO':", name_key("Rao Asha K") == name_key("ASHA K RAO"))
print("PAN format ok ABCDE1234F:", bool(PAN.match("ABCDE1234F")), "| ABCDE12345:", bool(PAN.match("ABCDE12345")))
```
**Output (my run):**
```
verhoeff: 0 of 108 single-digit errors and 0 of 11 adjacent swaps pass the check
12-digit id (checksum)        ocr_rules        auto-correct 0.743 | silent wrong 0.0000 | to human 0.258
12-digit id (checksum)        llm_normaliser   auto-correct 0.851 | silent wrong 0.0025 | to human 0.146
6-digit amount (format only)  ocr_rules        auto-correct 0.862 | silent wrong 0.0000 | to human 0.138
6-digit amount (format only)  llm_normaliser   auto-correct 0.919 | silent wrong 0.0805 | to human 0.000
invoice ok: True | OCR dropped a digit: False
name match 'Rao Asha K' vs 'ASHA K RAO': True
PAN format ok ABCDE1234F: True | ABCDE12345: False
```

**Follow-ups:**
- *How do you set the confidence threshold?* On a labelled set per field: choose the lowest threshold where the silent-error rate meets the bank's tolerance, and read off the review rate it implies.
- *Why not send everything to the vision-LLM?* Cost, latency and the silent-error pattern above; use it for layouts rules cannot parse, behind the same validators.
- *What about handwritten or low-quality scans?* Expect a higher review rate; measure it by document source rather than assuming.

**Common mistakes:** Reporting document-level accuracy; letting the LLM "clean" fields that have no checksum; no review sampling of passes; logging raw ID numbers; trusting vendor straight-through-rate claims instead of measuring on your own scans; skipping cross-document checks.

### Q8 ⭐⭐⭐ 🔴 Design a real-time voice agent (phone or app) for a support use case: streaming ASR, turn-taking and barge-in, LLM with tool calls, streaming TTS, and the latency budget from the user finishing speech to first audio. Where does time go, what can overlap or be speculated, what fails on noisy telephony audio, and how do you evaluate and cap cost per minute? (Part 10 Q19 covers streaming; treat quoted per-stage millisecond figures as vendor or blog targets, not measured facts.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
**Say this first (1 line):** Latency from the end of speech to first audio is the sum of endpointing, final ASR, any tool call, the LLM's first token, the first TTS chunk and the network; you hit a conversational budget by overlapping stages, streaming everything, speculating on partial transcripts, and cancelling instantly on barge-in.

**Then explain:**
- **Pipeline:** audio in -> streaming ASR with partial results -> endpointing (decide the user is done) -> LLM with tools -> streaming TTS -> audio out. Part 10 Q19 covers streaming; Part 3 and Part 8 cover tool calling.
- **Where time goes:** the wait for silence (endpointing), ASR finalisation, any backend tool call, first-token latency, first-chunk TTS, and network buffering. I do not quote per-stage millisecond figures from blogs or vendors: they are estimates, and the page I read only reaches its totals by assuming stages overlap.
- **What can overlap or be speculated:** start the LLM on a stable partial transcript; prefetch likely tool calls; stream TTS from the first sentence fragment; keep connections warm; play a short filler while a slow tool runs.
- **Endpointing is a trade-off:** a short silence threshold feels fast but cuts people off mid-sentence; a long one feels laggy. Tune on real call audio, per language.
- **Barge-in:** detect user speech while the agent talks, stop TTS, cancel the LLM stream and drop unspoken text. Echo of the agent's own voice into the mic causes false barge-ins.
- **Noisy telephony:** narrowband phone audio, background noise, accents, code-mixing, numbers and names spoken digit by digit; confirm critical values back ("that was 4 5 2?").
- **Evaluate and cap cost:** task success, WER on your own audio (not vendor test sets), p50 and p95 turn latency, barge-in correctness, call abandonment, cost per resolved call. Cap by max call minutes or turns, with a graceful handoff.

**Example:** Simulation with ASSUMED stage medians (lognormal spread; not measurements, not vendor figures): endpoint 300 ms, ASR finalise 120, tool call 250 on half the turns, LLM first token 350, TTS first chunk 150, network 80. Sequential: p50 1,173 ms, p95 1,627 ms. With overlap (half of ASR finalisation hidden by starting on the partial, 60% of tool time hidden by prefetch): p50 1,035 ms, p95 1,404 ms. Overlap helped by about 140 ms at the median under these assumptions; the biggest single lever in my numbers is still endpointing and LLM first token. Endpointing sweep (ASSUMED pause distributions): a 200 ms threshold cuts off 64.9% of mid-sentence pauses, 400 ms 21.5%, 600 ms 7.2%, 800 ms 2.5%. Cost with placeholder prices: USD 0.0298 per minute, LLM input share 20%, so a 6-minute call is about USD 0.18; the long context in each turn is what grows with call length.

**Code:** (mock LLMs and toy data; synthetic inputs labelled in the code)
```python
# Voice-agent latency simulation. EVERY stage time below is an ASSUMED lognormal (median, spread),
# not a measurement and not a vendor or blog figure. Replace with your own traces.
import random, statistics
random.seed(5)
def ln(median_ms, sigma=0.35): return random.lognormvariate(0, sigma) * median_ms
def pct(xs, q): xs = sorted(xs); return xs[int(q*(len(xs)-1))]
def turn(overlap):
    endpoint = ln(300)          # silence wait before we decide the user finished
    asr_final = ln(120)         # finalising the transcript after endpoint
    tool = ln(250) if random.random() < .5 else 0     # half of turns call a tool/backend
    llm_ttft = ln(350)          # time to first token
    tts_first = ln(150)         # time to first audio chunk
    net = ln(80)                # network + audio buffering out
    if not overlap:
        return endpoint + asr_final + tool + llm_ttft + tts_first + net
    # overlap: start LLM on the partial transcript (speculation), hiding half of ASR finalisation;
    # speculative tool prefetch hides 60% of tool time; TTS starts at first sentence fragment (already in tts_first).
    return endpoint + 0.5*asr_final + 0.4*tool + llm_ttft + tts_first + net
N = 20000
for name, ov in [("sequential", False), ("overlapped/speculative", True)]:
    xs = [turn(ov) for _ in range(N)]
    print(f"{name:<24} p50 {pct(xs,.5):6.0f} ms | p95 {pct(xs,.95):6.0f} ms | mean {statistics.mean(xs):6.0f} ms")
# Endpointing threshold trade-off: ASSUMED pause models. Mid-sentence pauses vs end-of-turn gaps.
mid = [random.lognormvariate(0, .6) * 250 for _ in range(N)]     # pauses inside a user's turn
end_gap = [random.lognormvariate(0, .5) * 900 for _ in range(N)] # real gap before the user expects an answer
print("\nendpoint threshold (ms) -> cuts user off | added wait on real end")
for th in (200, 400, 600, 800):
    cut = sum(p > th for p in mid)/N
    print(f"  {th:>4}                  {cut:>6.1%}              {th} ms")
# Barge-in: cancel TTS + LLM when user speech detected; wasted tokens avoided
class Call:
    def __init__(s): s.tts_running = False; s.llm_tokens = 0; s.cancelled = False
    def speak(s, tokens=60): s.tts_running, s.llm_tokens = True, tokens
    def barge_in(s, after_tokens):
        if s.tts_running: s.llm_tokens = after_tokens; s.cancelled = True; s.tts_running = False
c = Call(); c.speak(60); c.barge_in(after_tokens=12)
print(f"\nbarge-in test: LLM stopped at {c.llm_tokens}/60 tokens, cancelled={c.cancelled}")
assert c.cancelled and c.llm_tokens == 12
# Cost per minute with ASSUMED unit prices (placeholders)
ASR_PER_MIN, TTS_PER_1K_CHAR, LLM_PER_M_IN, LLM_PER_M_OUT = 0.006, 0.015, 1.0, 4.0
turns_per_min = 4; in_tok = 1500; out_tok = 60; chars = 280
cost = ASR_PER_MIN + turns_per_min*(chars/1000*TTS_PER_1K_CHAR + in_tok/1e6*LLM_PER_M_IN + out_tok/1e6*LLM_PER_M_OUT)
print(f"cost/min (ASSUMED prices) ${cost:.4f}; LLM input share {turns_per_min*in_tok/1e6*LLM_PER_M_IN/cost:.0%}")
print("a 6-minute call at that rate: $%.3f; cap: hang up politely after N minutes or M turns" % (6*cost))
```
**Output (my run):**
```
sequential               p50   1173 ms | p95   1627 ms | mean   1195 ms
overlapped/speculative   p50   1035 ms | p95   1404 ms | mean   1053 ms

endpoint threshold (ms) -> cuts user off | added wait on real end
   200                   64.9%              200 ms
   400                   21.5%              400 ms
   600                    7.2%              600 ms
   800                    2.5%              800 ms

barge-in test: LLM stopped at 12/60 tokens, cancelled=True
cost/min (ASSUMED prices) $0.0298; LLM input share 20%
a 6-minute call at that rate: $0.179; cap: hang up politely after N minutes or M turns
```

**Follow-ups:**
- *How do you test barge-in?* Scripted audio with an interruption at a known offset; assert TTS stops and LLM tokens stop (the code checks the second).
- *Should the agent use a cascade or a speech-to-speech model?* Cascades are easier to debug and to put validators on; end-to-end models can cut latency but give less control. Measure both on your calls.
- *How do you cut cost per minute?* Shorter context via summarised history (Q18), a smaller model for simple turns (Q19 of this part), and caching of frequent answers.

**Common mistakes:** Quoting blog latencies as facts; measuring only mean latency; tuning the silence threshold on clean office audio; forgetting echo cancellation; no handling for tool calls that take seconds; evaluating ASR with a vendor's test set; no call-length cap.

### Q9 ⭐⭐⭐ 🔴 Design a conversational shopping and search assistant for a large e-commerce catalogue: query understanding, hybrid retrieval over products, hard constraints (price, size, stock) enforced by code rather than by the model, grounding every product claim in live catalogue data, multi-turn preference memory, ranking and personalisation, handling out-of-catalogue questions, and evaluating relevance, conversion and hallucinated claims. (Part 7 Q23, Q40 and Part 6 Q28 are the building blocks.)
**Asked at:** interview-prep guide, not a candidate report; GenAI/ML engineer and applied-scientist system-design rounds at product companies, GCCs and startups
**Say this first (1 line):** Let a model understand the request, but let code enforce price, size and stock on live catalogue data, retrieve with hybrid search, and verify every product claim against the catalogue before it reaches the user.

**Then explain:**
- **Query understanding:** the LLM turns text into structured intent (category, brand, price cap, size, sort) and a cleaned search string; code validates the structure.
- **Hybrid retrieval over products** (Part 7 Q2): lexical for model numbers and brands, embeddings for "something for a monsoon trek", fused with reciprocal-rank fusion; the query is routed between FAQ, catalogue and policy paths (Part 7 Q23).
- **Hard constraints are code, not prompt.** Filters run in the index or on live data; the model never decides if an item is in stock or under budget. Soft preferences (colour, style) are ranking features.
- **Grounding:** the answer cites SKUs, and each stated price, size, stock status or attribute is checked against the live record at answer time. Index snapshots go stale; on mismatch rewrite with live values.
- **Multi-turn memory** (Part 6 Q28): store stated preferences as structured fields with overwrite rules, not as free text; let the user see and clear them.
- **Ranking and personalisation:** relevance first, then business signals and the user's history; LLM re-ranking is limited to a short candidate list (Q26 of this part).
- **Out-of-catalogue:** say so and suggest the nearest category; never invent a product.
- **Evaluation:** relevance on labelled queries, constraint-violation rate (target zero), hallucinated-claim rate against live data, then conversion and returns in an A/B test (Part 9 Q30).

**Example:** Toy catalogue of 6 SKUs, MOCK rule-based query parser (price cap and size by regex), lexical plus hashed-embedding retrieval fused with RRF. Four constraint queries: with ranking only, 7 of the 12 returned results violated a hard constraint (price, size or stock); with code-enforced filters, 0 of 8. A grounding check caught a stale index price (claimed 1999, live 2299). Honest weakness: for "blue running shoes under 2500 size 9" the third result is white casual sneakers, because they satisfy the constraints while matching the query weakly; a filter does not replace a relevance floor, which the toy lacks. The "formal shoes" query returns two non-formal items for the same reason. A query for a laptop correctly gets "no matching product".

**Code:** (mock LLMs and toy data; synthetic inputs labelled in the code)
```python
# Mini shopping assistant: LLM parses intent (MOCKED), CODE enforces hard constraints and grounds claims
# in live catalogue data. Toy catalogue, toy lexical + hashed-bag "dense" retrieval fused with RRF.
import re, math, random, hashlib
CAT = {  # sku: (title, price, sizes_in_stock, live_stock)
 "s1": ("blue running shoes lightweight", 1999, {"8", "9"}, 5),
 "s2": ("black running shoes cushioned", 3499, {"9", "10"}, 2),
 "s3": ("blue leather formal shoes", 2799, {"7", "8"}, 0),
 "s4": ("white canvas sneakers casual", 1299, {"8", "9", "10"}, 12),
 "s5": ("blue trail running shoes grip", 2499, {"9"}, 3),
 "s6": ("running socks pack of three", 399, {"M", "L"}, 40),
}
INDEX_PRICE = {k: v[1] for k, v in CAT.items()}           # price snapshot in the search index (stale risk)
def mock_parse(q):                                        # stand-in for an LLM: text -> structured constraints
    out = {"max_price": None, "size": None, "text": q}
    m = re.search(r"under (\d+)", q); out["max_price"] = int(m.group(1)) if m else None
    m = re.search(r"size (\d+)", q); out["size"] = m.group(1) if m else None
    out["text"] = re.sub(r"(under \d+|size \d+)", "", q).strip()
    return out
def toks(s): return re.findall(r"[a-z]+", s.lower())
def lexical(q):                                           # word overlap score
    qs = set(toks(q)); return sorted(CAT, key=lambda k: -len(qs & set(toks(CAT[k][0]))))
def dense(q, dim=64):                                     # hashed bag-of-words embedding with char trigrams
    def emb(s):
        v = [0.0]*dim
        for w in toks(s):
            for i in range(max(1, len(w)-2)):
                h = int(hashlib.md5(w[i:i+3].encode()).hexdigest(), 16) % dim; v[h] += 1
        n = math.sqrt(sum(x*x for x in v)) or 1; return [x/n for x in v]
    qe = emb(q); return sorted(CAT, key=lambda k: -sum(a*b for a, b in zip(qe, emb(CAT[k][0]))))
def rrf(*rankings, k=60):
    sc = {}
    for r in rankings:
        for i, d in enumerate(r): sc[d] = sc.get(d, 0) + 1/(k+i+1)
    return sorted(sc, key=lambda d: -sc[d])
def passes(sku, c, live):                                 # HARD constraints, in code, on LIVE data
    t, price, sizes, stock = CAT[sku]
    return (c["max_price"] is None or price <= c["max_price"]) and (c["size"] is None or c["size"] in sizes) and stock > 0
def search(q, enforce=True, k=3):
    c = mock_parse(q); ranked = rrf(lexical(c["text"]), dense(c["text"]))
    return [s for s in ranked if (not enforce or passes(s, c, True))][:k], c
def violations(skus, c): return sum(not passes(s, c, True) for s in skus)
queries = ["blue running shoes under 2500 size 9", "running shoes under 2000 size 8", "casual sneakers size 10 under 1500", "formal shoes size 8 under 3000"]
for enforce in (False, True):
    v = tot = 0
    for q in queries:
        hits, c = search(q, enforce); v += violations(hits, c); tot += len(hits)
    print(f"{'code-enforced' if enforce else 'ranking only  '} constraints: {v} violating results out of {tot} returned")
print("hits for query 1:", search(queries[0])[0], "| formal shoes (s3 out of stock):", search(queries[3])[0])
# Grounding: claims in the draft answer are checked against LIVE data; price changed after indexing
CAT["s1"] = ("blue running shoes lightweight", 2299, {"8", "9"}, 5)   # live price moved from 1999 to 2299
draft = {"sku": "s1", "claimed_price": INDEX_PRICE["s1"]}
live_ok = draft["claimed_price"] == CAT[draft["sku"]][1]
print(f"grounding check: claimed {draft['claimed_price']} vs live {CAT['s1'][1]} -> {'ok' if live_ok else 'REWRITE with live price'}")
# Multi-turn memory: stated preference carries forward only while not contradicted
memory = {}
def update_memory(q):
    c = mock_parse(q)
    for k in ("max_price", "size"):
        if c[k] is not None: memory[k] = c[k]
update_memory("running shoes under 2500 size 9"); update_memory("something in blue")
print("memory after two turns:", memory)
# Out-of-catalogue: refuse to invent
def answer(q):
    hits, c = search(q)
    best_overlap = max(len(set(toks(c["text"])) & set(toks(CAT[s][0]))) for s in CAT)
    return "No matching product in the catalogue." if best_overlap == 0 or not hits else f"Top match: {hits[0]}"
print("out-of-catalogue 'laptop under 50000':", answer("laptop under 50000"))
assert violations(search(queries[0])[0], mock_parse(queries[0])) == 0 and not live_ok
print("tests passed")
```
**Output (my run):**
```
ranking only   constraints: 7 violating results out of 12 returned
code-enforced constraints: 0 violating results out of 8 returned
hits for query 1: ['s1', 's5', 's4'] | formal shoes (s3 out of stock): ['s1', 's4']
grounding check: claimed 1999 vs live 2299 -> REWRITE with live price
memory after two turns: {'max_price': 2500, 'size': '9'}
out-of-catalogue 'laptop under 50000': No matching product in the catalogue.
tests passed
```

**Follow-ups:**
- *How do you handle "cheap" or "nice"?* Map it to a sort or a price percentile, and say what was assumed; do not turn it into a hard filter silently.
- *Catalogue changes every minute.* Keep price and stock out of the embedded text; join them at query time from a live store.
- *How do you measure hallucination?* Extract claims from answers, check each against catalogue fields, and report the rate; sample for human review.

**Common mistakes:** Putting "under 2000" in the prompt and trusting it; embedding price and stock into vectors; no relevance floor after filters; using last turn's constraints after the user changed their mind; optimising click-through without checking returns and wrong claims.

### Q10 ⭐⭐⭐ 🔴 Design a customer-facing chatbot for a bank under regulatory constraints: scope (information vs transactions), grounding in approved content, no advice outside policy, authentication before account data, human handoff, PII redaction, audit logs and retention, model-risk governance, vendor and data-residency choices, red-team and rollout gates. Keep regulatory references general: which RBI and DPDP obligations would you ask compliance to confirm rather than assert? (Part 5 Q39, Part 11 Q11, Q30 and Q42 cover the building blocks.)
**Asked at:** BFSI and fintech GenAI teams, GCCs and product companies (company-type tag from guides and regulator material, not a candidate report)
**Say this first (1 line):** Make the bot a narrow, grounded assistant whose powers are limited by what tools it has, not by what the prompt says: information from approved content, account data only after authentication through authorised APIs, no transactions or advice in chat, redacted logs, a tamper-evident audit trail, human handoff, and rollout gates from red-team tests.

**Then explain:**
- **Scope:** start with information (rates, branches, how-to) from approved content; add account lookups behind authentication; keep money movement and personalised advice out of the chat tool set or behind a separate step-up flow (Part 5 Q39 for a refund-bot guardrail design).
- **Grounding and abstention:** answer only from approved, versioned content with citations; if retrieval is weak, hand off instead of guessing (Part 6 Q27).
- **Authentication tiers:** anonymous, logged in, step-up. Account data comes from the core system through an API call whose result the model summarises; the model never "remembers" it across users.
- **PII:** redact before the prompt leaves the bank's boundary and before logging (Part 11 Q11); store only what the audit needs, with a retention schedule compliance sets.
- **Audit and governance:** log prompt version, model version, sources, tool calls and handoffs; use tamper-evident storage; keep a model inventory with owners, risk tiering, change approval and periodic review (Part 11 Q30, Q42).
- **Vendor and residency choices:** where inference runs, whether prompts are retained or used for training, subprocessors, exit plan.
- **Regulatory items I would ask compliance to confirm, not assert:** how the RBI's FREE-AI framework applies (the 13 August 2025 press release I opened describes seven principles called Sutras, 26 recommendations and six pillars; I did not read the full report); applicable RBI directions on outsourcing, IT governance, customer grievance handling, and disclosure that the customer is talking to an AI; DPDP Act and Rules duties on notice, consent, purpose, retention, breach reporting and cross-border transfer (I have only secondary summaries, not the official text); record-keeping periods; whether any fraud-related or KYC flows are in scope.
- **Rollout gates:** red-team suite passes, staged exposure to employees then a small share of customers, a kill switch, and a named owner (Part 11 Q6).

**Example:** Toy control plane (MOCK keyword intent model, 3 FAQ entries). Seven hand-written cases all pass: an information question gets the approved FAQ; a transfer gets refused in chat; a balance question without login gets a login prompt; investment advice is declined; a fraud report triggers handoff; an unknown topic abstains; and a message containing a PAN and a phone number is redacted and still answered. Redaction gives "[PAN]", "[PHONE]", "[ACCT]", and its first version mislabelled the phone as an account number until I reordered the patterns (a 10-digit string is ambiguous). The audit rows contain no raw PAN; the hash-chain verifies, and after editing one past row it fails. A paraphrase the keyword model does not know ("please remit 5000 to Ravi") was routed to info: a known miss. The safety comes from the tool set having no payment tool, not from the classifier getting it right.

**Code:** (mock LLMs and toy data; synthetic inputs labelled in the code)
```python
# Bank-chatbot control plane (MOCK intent model, toy FAQ). Shows scope gating, auth tiers, grounding with
# abstention, PII redaction, human handoff and a tamper-evident audit log. Not legal or RBI guidance.
import re, hashlib, json
FAQ = {"savings account interest": "Interest is credited as per the bank's published schedule (approved FAQ #12).",
       "debit card block": "You can block a card from the app or by calling the helpline (approved FAQ #7).",
       "branch timings": "Branches are open on working days; see the branch locator (approved FAQ #3)."}
def mock_intent(msg):                                       # stand-in for an intent classifier
    m = msg.lower()
    if any(w in m for w in ("transfer", "pay ", "send money")): return "transaction"
    if any(w in m for w in ("my balance", "my statement", "my account")): return "account_data"
    if any(w in m for w in ("should i invest", "which loan is best", "guarantee")): return "advice"
    if any(w in m for w in ("complaint", "fraud", "stolen", "angry")): return "escalate"
    return "info"
PII = [(re.compile(r"\b\d{12}\b"), "[ID12]"), (re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"), "[PAN]"),
       (re.compile(r"\b[6-9]\d{9}\b"), "[PHONE]"), (re.compile(r"\b\d{9,18}\b"), "[ACCT]")]   # order matters: a 10-digit string is ambiguous
def redact(s):
    for rx, tag in PII: s = rx.sub(tag, s)
    return s
class Audit:                                                # hash-chained log: editing a past row breaks the chain
    def __init__(self): self.rows, self.prev = [], "0"*8
    def add(self, **kw):
        body = json.dumps(kw, sort_keys=True); h = hashlib.sha256((self.prev + body).encode()).hexdigest()[:8]
        self.rows.append((body, h)); self.prev = h
    def verify(self):
        p = "0"*8
        for body, h in self.rows:
            if hashlib.sha256((p + body).encode()).hexdigest()[:8] != h: return False
            p = h
        return True
def retrieve(msg):                                          # toy grounding: best word-overlap FAQ or None
    w = set(msg.lower().split()); best = max(FAQ, key=lambda k: len(w & set(k.split())))
    return best if len(w & set(best.split())) >= 2 else None
def handle(msg, session, audit):
    safe = redact(msg); intent = mock_intent(msg)
    if intent == "escalate": reply = "HANDOFF: connecting you to a human agent."
    elif intent == "advice": reply = "I can't give investment or product advice; here is how to reach an advisor."
    elif intent in ("transaction", "account_data"):
        reply = ("Please complete login in the app first." if not session["authed"] else
                 "I can't move money in chat; use the app's payment screen." if intent == "transaction" else
                 "Fetching from the core system via an authorised API (not from the model).")
    else:
        k = retrieve(msg); reply = FAQ[k] if k else "I don't have approved information on that; handing off."
    audit.add(user_text=safe, intent=intent, reply=reply[:40], authed=session["authed"])
    return intent, reply
TESTS = [("what is the savings account interest", False, "info", "approved FAQ #12"),
         ("transfer 5000 to my friend", True, "transaction", "can't move money"),
         ("what is my balance", False, "account_data", "login"),
         ("should i invest in gold", False, "advice", "can't give"),
         ("someone stole my card, fraud", False, "escalate", "HANDOFF"),
         ("tell me about crypto yield", False, "info", "don't have approved"),
         ("my PAN is ABCDE1234F and phone 9876543210 debit card block", False, "info", "FAQ #7")]
audit = Audit(); passed = 0
for msg, authed, exp_intent, exp_text in TESTS:
    intent, reply = handle(msg, {"authed": authed}, audit)
    ok = intent == exp_intent and exp_text in reply; passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {intent:<13}{reply[:60]}")
print(f"{passed}/{len(TESTS)} red-team style cases pass")
print("redaction:", redact("PAN ABCDE1234F phone 9876543210 acct 123456789012345"))
print("audit rows contain raw PAN?", any("ABCDE1234F" in b for b, _ in audit.rows), "| chain valid:", audit.verify())
audit.rows[1] = (audit.rows[1][0].replace("transaction", "info"), audit.rows[1][1])
print("after editing one past row, chain valid:", audit.verify())
# Honest miss: a paraphrase the keyword intent model does not know. Intent gating alone is not a control.
intent, reply = handle("please remit 5000 to Ravi", {"authed": True}, audit)
print(f"KNOWN MISS  'please remit 5000 to Ravi' -> intent={intent}, reply={reply[:40]!r}")
print("why it is still safe: the chat tool set has no payment tool, so even a misrouted intent cannot move money")
TOOLS = {"faq_lookup", "branch_locator"}
assert "make_payment" not in TOOLS and passed == len(TESTS)
```
**Output (my run):**
```
PASS  info         Interest is credited as per the bank's published schedule (a
PASS  transaction  I can't move money in chat; use the app's payment screen.
PASS  account_data Please complete login in the app first.
PASS  advice       I can't give investment or product advice; here is how to re
PASS  escalate     HANDOFF: connecting you to a human agent.
PASS  info         I don't have approved information on that; handing off.
PASS  info         You can block a card from the app or by calling the helpline
7/7 red-team style cases pass
redaction: PAN [PAN] phone [PHONE] acct [ACCT]
audit rows contain raw PAN? False | chain valid: True
after editing one past row, chain valid: False
KNOWN MISS  'please remit 5000 to Ravi' -> intent=info, reply="I don't have approved information on tha"
why it is still safe: the chat tool set has no payment tool, so even a misrouted intent cannot move money
```

**Follow-ups:**
- *How do you red-team it?* Maintain a suite of jailbreaks, off-scope and PII-probing prompts, run on every prompt or model change, and block release below an agreed pass rate (Part 9 Q14).
- *What do you log if redaction fails?* Treat the log store as sensitive: access controls, encryption, short retention, and an incident path (Part 11 Q11).
- *Can the bot say "you qualify for this loan"?* No; eligibility and advice go to a rules engine or a human with the bank's disclosures; the bot may explain published criteria.

**Common mistakes:** Relying on the prompt to forbid transactions; logging raw customer text; letting the model see account data it does not need; answering regulatory questions from memory; no human handoff path; treating the classifier as the control instead of the tool permissions.
