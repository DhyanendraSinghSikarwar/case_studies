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

### Q37 ⭐⭐ 🟡 A chat product resends the whole history on every turn, with a 1,000-token system prompt and 300 new tokens added per turn, and the input at turn t counts the system prompt plus the t-1 earlier turns. Over a 20-turn conversation compute the total input tokens sent and their cost at an illustrative 3 per million, compare with 20,000 tokens if no history were resent, and propose a context-management policy.
**Asked at:** LLM cost and routing pages (getmaxim cost and semantic-cache guides, tianpan and system-design.space pages on routing and cascades, a Towards Data Science article on saving tokens in agentic AI, a Towards AI piece on AI system-design interview patterns); practitioner material, no confirmed interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Resending history makes the total grow with the square of the turn count: 77,000 input tokens over 20 turns, costing 0.231 per conversation at the illustrative 3 per million, and I would cap it with a sliding window, a running summary and prefix caching.

**Clarifying questions:**
- Is the input at turn t exactly system prompt plus the t-1 earlier turns (the prompt's rule), and are replies counted in the 300 tokens? If replies are long, the 300 is too low.
- Does the 300 include the current user message? The prompt's formula does not add it to turn t, and I note below why that matters.
- Are conversations really 20 turns, or is the tail much longer? Cost grows with the square, so the long conversations dominate the bill.
- Does the provider offer prefix caching, and at what discount and minimum length? (Book 2 Part 01, Q24 covers how prefix caching works.)
- What must the model remember: exact wording, facts the user stated, or only the task state? That sets what a summary may drop.

**Approach:**
1. Per turn: input_t = 1,000 + 300 x (t-1). Turn 1 is 1,000, turn 10 is 3,700, turn 20 is 6,700.
2. Total = 20 x 1,000 + 300 x (0 + 1 + ... + 19) = 20,000 + 300 x 190 = 77,000 tokens. Cost = 77,000 x 3 / 1,000,000 = 0.231.
3. Compare with 20,000 as the prompt asks: 77,000 / 20,000 = 3.85 times. But 20,000 is only the system prompt repeated 20 times. If no history were resent, each turn would still send its own 300 new tokens: 20 x 1,300 = 26,000, so the like-for-like ratio is 2.96 times. State both, and say which you use. (If the current user message is also added to turn t, the total is 83,000; see the note on the prompt.)
4. Growth is quadratic: 40 turns costs 274,000 tokens, 3.56 times the 20-turn conversation for twice the length.
5. Policy, in this order: (a) cache the stable prefix (system prompt and early turns); (b) keep a sliding window of recent turns, for example the last 5, which here gives 45,500 tokens (59% of full); (c) summarise older turns into a short running summary and pin key facts (name, order id, constraints) as structured memory; (d) retrieve old turns only when the user refers back; (e) trim long tool outputs and quote only the needed lines.
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
- Strong: derives the 77,000 from a sum, not a guess, and says it grows quadratically. Weak: "it is about 6,700 x 20".
- Strong: notices the 20,000 baseline leaves out the new tokens. Weak: repeats 3.85 times without comment.
- Strong: lists window, summary, caching and retrieval, with a quality test. Weak: "use a bigger context window".
- Strong: ties the policy to what the model must remember. Weak: truncates blindly.

**Example:** (illustrative numbers) Turn 20 sends 6,700 tokens, of which 1,000 is the system prompt and 5,700 is history. With a window of 5 turns it sends 1,000 + 1,500 = 2,500. Over 20 turns the window policy sends 45,500 tokens against 77,000. With prefix caching on the earlier tokens at 10% of the rate, the effective tokens fall to 13,730, 18% of uncached (ignoring any cache-write charge). Weak answer: "Conversations get expensive, so I would reduce the number of turns." Strong answer: "77,000 tokens, quadratic in turns. I would cache the prefix, keep the last five turns plus a pinned summary, and check on labelled chats that answers do not get worse."

**Code:**
```python
# Illustrative numbers from the prompt (price is illustrative, not a vendor price)
SYS, NEW, TURNS, PRICE = 1000, 300, 20, 3.0   # tokens, tokens/turn, turns, price per million input tokens

inp = [SYS + NEW * (t - 1) for t in range(1, TURNS + 1)]   # prompt's formula: system + (t-1) earlier turns
total = sum(inp)
print("input at turn 1, 10, 20:", inp[0], inp[9], inp[19])
print("total input tokens:", total, "| cost:", round(total * PRICE / 1e6, 4))
assert inp[0] == 1000 and inp[9] == 3700 and inp[19] == 6700
assert total == 20 * SYS + NEW * sum(range(20)) == 20_000 + 300 * 190 == 77_000
assert round(total * PRICE / 1e6, 3) == 0.231

# The prompt compares with 20,000 (system prompt only). That baseline leaves out the 300 new tokens
# each turn actually has to send. Like-for-like "no history resent": system + the turn's own 300 tokens.
base_prompt = TURNS * SYS
base_fair = TURNS * (SYS + NEW)
print(f"vs prompt baseline 20,000: x{total/base_prompt:.2f}; vs like-for-like {base_fair}: x{total/base_fair:.2f}")
assert base_prompt == 20_000 and base_fair == 26_000
assert round(total / base_prompt, 2) == 3.85 and round(total / base_fair, 2) == 2.96

# Growth is quadratic in turns: doubling the conversation length
total40 = sum(SYS + NEW * (t - 1) for t in range(1, 41))
print("40 turns:", total40, "tokens, x%.2f of 20 turns" % (total40 / total))
assert total40 == 40 * 1000 + 300 * 780 and round(total40 / total, 2) == 3.56

# Policy A: keep the system prompt plus only the last 5 turns
K = 5
win = sum(SYS + NEW * min(t - 1, K) for t in range(1, TURNS + 1))
print("sliding window (last 5 turns):", win, "tokens,", f"{win/total:.0%} of full history")
assert win == 20_000 + 300 * (sum(range(1, 6)) + 14 * 5) == 45_500 and round(win / total, 2) == 0.59

# Policy B: prefix caching, previously sent tokens billed at 10% of the input rate (illustrative)
CACHE = 0.10
eff = inp[0] + sum(CACHE * inp[t - 2] + NEW for t in range(2, TURNS + 1))   # turn t re-reads input of turn t-1 as prefix
eff_cost = eff * PRICE / 1e6
print(f"with prefix cache: effective tokens {eff:.0f}, cost {eff_cost:.4f} ({eff/total:.0%} of uncached)")
assert round(eff) == 13_730 and round(eff / total, 2) == 0.18

# Other numbers quoted in the text
alt_total = sum(SYS + NEW * t for t in range(1, TURNS + 1))   # if the current message is also counted
print("if the current message is also counted:", alt_total, "| 20 x last turn:", 20 * inp[19], "| turn 20 with window:", SYS + NEW * K)
assert alt_total == 83_000 and 20 * inp[19] == 134_000 and SYS + NEW * K == 2_500 and inp[19] - SYS == 5_700
```

**Output (my run):**
```text
input at turn 1, 10, 20: 1000 3700 6700
total input tokens: 77000 | cost: 0.231
vs prompt baseline 20,000: x3.85; vs like-for-like 26000: x2.96
40 turns: 274000 tokens, x3.56 of 20 turns
sliding window (last 5 turns): 45500 tokens, 59% of full history
with prefix cache: effective tokens 13730, cost 0.0412 (18% of uncached)
if the current message is also counted: 83000 | 20 x last turn: 134000 | turn 20 with window: 2500
```

**Follow-ups:**
- Why not simply use a model with a bigger window? The window only limits what fits; you still pay for every resent token, and latency rises with prompt length.
- How do you decide the window size? Plot task success against the window size on labelled conversations and take the smallest size at which success stops improving.
- What changes if replies are long? Replies join the history, so the 300 is too low and growth is faster. Cap the stored reply or summarise it.

**Common mistakes:**
- Multiplying the last turn's input by the number of turns (6,700 x 20 = 134,000 overstates it).
- Comparing with a baseline that omits the new tokens of each turn.
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

### Q41 ⭐⭐ 🔴 A user exercises a right to have personal data deleted. It sits in raw chat logs, in 3,000 of 2,000,000 chunks in a vector index, in an evaluation dataset and in 35-day rolling backups, and your internal deletion target is 30 days. Compute the share of the index affected and the gap between the target and the backup retention, and lay out a deletion plan that is honest about what cannot be erased immediately.
**Asked at:** PII and compliance material (tianpan, Kunal Ganglani, Gravitee and barkingiguana pages on logs, retention, redaction and data residency, and a vendor piece on DPDP readiness for LLM traffic); vendor and practitioner pages, not regulator guidance or an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The vector index is only 0.15% affected (3,000 of 2,000,000 chunks), and backups outlast the 30-day target by 5 days on paper and more in practice, so I would delete from every live store quickly, verify it, and tell the user and the privacy owner honestly that backups age out later.

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
5. Backups (35 days against a 30-day target, a 5-day gap on paper): backups are usually immutable, so you cannot edit them. Be honest: the copy expires when the last backup that held it expires. If live data is deleted on day d, the last backup copy expires on day d + 35: day 36 for deletion on day 1, and day 65 for deletion on day 30. Fix going forward: keep a suppression list of deleted user ids and re-apply deletion on any restore; and consider shortening backup retention to 30 days or less if the policy requires erasure in 30.
6. Verify and record: run checks (queries return nothing), keep a deletion record without the personal data (request id, dates, systems), and reply to the user with what was deleted and when the backups expire.
7. Prevent repeats: tag data with a user id at ingestion; avoid putting personal data into evaluation sets; minimise retention of raw logs.

**Metrics:**
- Share of index affected = chunks for the user / total chunks (0.15%).
- Time to delete per store (days from request), against the 30-day target; deletion verification pass rate = stores verified clean / stores in the data map.
- Residual exposure window = last backup expiry day minus target day (5 in the prompt's simplification; at least 6 in the timeline of Code).
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
- Computing the gap as 5 days and stopping there.
