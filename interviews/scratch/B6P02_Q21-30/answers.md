### Q21 ⭐⭐ 🟡 A recommender's click-through rate has slid 6% over eight weeks even though its offline NDCG improved 3% at launch. Catalogue diversity in recommendations has also shrunk. Explain how a feedback loop and exposure bias could cause this, how you would check for it, and what you would change.
**Asked at:** Recommender feedback-loop and popularity-bias literature (Mansoury et al. 'Feedback Loop and Bias Amplification in Recommender Systems', a popularity-bias survey on arXiv) plus a Prachub ranking-debugging page; no public interview page for this exact prompt, so editor-designed from the literature; search snippets only, not opened
**Say this first (1 line):** If the recommender learns only from clicks on items it already showed, popular items get more exposure and more clicks, the tail starves, diversity shrinks and CTR drifts down, while an offline NDCG measured on those same logs still looks better; I would prove it with exposure data and a small random slice, then add exploration.

**Clarifying questions:**
- Is "6%" relative (5.0% to 4.7%) or six points? It sets how big the problem is, and I will assume relative.
- Is CTR per impression or per user, and did the traffic mix (new versus returning users, platform) change over the eight weeks? A mix shift can fake a slide.
- How was the offline NDCG computed? If it used clicks logged under the old ranker, it can only credit items that ranker already showed, so it is exposure-biased.
- How is "diversity" measured: share of catalogue shown, entropy of impressions, top-10 item share? I need one number to track.
- Is any traffic randomised today? Random exposure is the only unbiased evidence of how tail items really perform.
- Do users see the same items repeatedly? That adds fatigue, a second cause of a slide.

**Approach:**
1. Confirm the slide is real: CTR per impression by week, split by position, platform and user cohort, with seasonality and UI changes ruled out.
2. Measure concentration over time: distinct items shown per day, share of impressions going to the top 1% of items, normalised entropy of impression shares. Compare week 0 with week 8.
3. Test the loop directly: for items with similar quality signals (price, rating, age), compare CTR per exposure for items that got high early exposure versus low. Use position-normalised CTR so slot effects do not distort it.
4. Run a small randomised slice (illustrative 1 to 2% of requests, one slot filled by random eligible items). Compare CTR of randomised-slot items by popularity bucket. If tail items do as well per exposure as head items, the ranker is under-exposing them.
5. Check fatigue: CTR by number of prior exposures of the same item to the same user.
6. Change the system: reserve exploration slots or use Thompson-style sampling for uncertain items; train with inverse-propensity weights from logged exposure probabilities; add a diversity or coverage constraint in re-ranking; give new items a freshness boost.
7. Evaluate offline with a counterfactual estimator on randomised data, not raw logged NDCG; then run a long A/B with a permanent small holdout.

**Metrics:**
- CTR = clicks / impressions, also reported per position so slot mix does not change it.
- Coverage = distinct items shown in a day / eligible items that day.
- Top-1% share = impressions on the 1% most-shown items / all impressions.
- Normalised entropy = -sum(s_i ln s_i) / ln(N), where s_i is item i's impression share and N the number of items.
- Randomised-slot CTR by popularity bucket (head, torso, tail).
- Guardrails: orders or revenue per session, session length, latency, and the CTR cost of the exploration slice.

**Risks:**
- Exposure-biased offline evaluation: NDCG up 3% on logged data does not show a better ranker for items it never showed.
- Seasonality or catalogue changes can explain CTR without any loop.
- Exploration lowers CTR in the short run, so it needs a budget and a time horizon.
- Diversity can be gamed with irrelevant items; pair it with a relevance floor.
- A multi-week slide has more than one cause (fatigue, novelty fade, competition); do not credit it all to the loop.

**What the interviewer scores:**
- Strong: explains the loop (exposure drives clicks, clicks drive ranking) and why offline logged NDCG cannot see it. Weak: says "retrain more often".
- Strong: asks for randomised exposure data or a holdout as unbiased evidence. Weak: argues from the dashboard only.
- Strong: gives concrete concentration metrics and the fix list (exploration, IPS, diversity). Weak: "add diversity" with no measurement.
- Strong: states the cost of exploration and how to cap it.

**Example:** (illustrative) CTR goes from 5.00% to 4.70%, which is -6.0% relative. Offline NDCG goes from 0.500 to 0.515, +3.0% relative. Both are in the code. Then a toy world of 300 items, 5 slots, with a legacy popularity head start unrelated to true appeal, and an assumption that an item's appeal saturates as it is shown to the same audience. Ranking by raw clicks shows only 5 distinct items and the slate CTR falls 14.1% over the run. A ranker that keeps one slot random shows all 300 items, top-5 impression share 0.60 instead of 1.00, and its slate CTR roughly doubles because it finds better items. These are toy numbers; the saturation assumption is mine and produces the slide. Weak: "NDCG improved, so the model is better; CTR will recover." Strong: "NDCG was measured on what the old model chose to show. Show me concentration over time and a randomised slice before I touch the model."

**Code:**
```python
import numpy as np

# Part A: the prompt's arithmetic (illustrative levels)
ctr0, ctr1 = 0.0500, 0.0470
assert abs((ctr1 - ctr0) / ctr0 - (-0.06)) < 1e-9          # 6% relative slide
ndcg0, ndcg1 = 0.500, 0.515
assert abs((ndcg1 - ndcg0) / ndcg0 - 0.03) < 1e-9          # +3% relative
print("CTR 5.00% -> 4.70% = -6.0% relative; NDCG 0.500 -> 0.515 = +3.0% relative")

# Part B: toy feedback loop. Assumption (labelled): an item's appeal saturates with repeated
# exposure, p_eff = p * exp(-impressions / TAU).
rng = np.random.default_rng(21)
N, K, ROUNDS, USERS, TAU = 300, 5, 300, 200, 200000.0
true_p = rng.beta(2, 38, N)                       # mean about 5%
exam = np.array([1.0, 0.6, 0.4, 0.3, 0.2])        # position bias
head_start = rng.permutation(1.0 / np.arange(1, N + 1)) * 40  # legacy popularity, unrelated to true_p

def run(policy):
    clicks = rng.poisson(head_start).astype(float)
    imps = np.zeros(N)
    shown = set(); ctrs = []; imp_total = np.zeros(N)
    for r in range(ROUNDS):
        if policy == "popularity":
            slate = np.argsort(-clicks)[:K]
        else:                                        # rate-based, 1 of 5 slots is random exploration
            score = (clicks + 1) / (imps + 20)
            slate = list(np.argsort(-score)[:K - 1])
            rest = [i for i in range(N) if i not in slate]
            slate.append(int(rng.choice(rest)))
            slate = np.array(slate)
        p_eff = true_p[slate] * np.exp(-imp_total[slate] / TAU)
        c = rng.binomial(USERS, exam * p_eff)
        clicks[slate] += c; imps[slate] += USERS; imp_total[slate] += USERS
        shown.update(slate.tolist())
        ctrs.append((exam * p_eff).sum() / exam.sum())
    ctrs = np.array(ctrs)
    top5_share = np.sort(imp_total)[::-1][:5].sum() / imp_total.sum()
    return ctrs[:20].mean(), ctrs[-20:].mean(), len(shown), top5_share

for pol in ("popularity", "explore"):
    a, b, d, s = run(pol)
    print(f"{pol:10s} slate CTR first20={a:.4f} last20={b:.4f} ({(b-a)/a:+.1%}) distinct items shown={d} top5 impression share={s:.2f}")
    if pol == "popularity":
        pa, pb, pd, ps = a, b, d, s
    else:
        ea, eb, ed, es = a, b, d, s
assert pb < pa                  # greedy slate CTR slides
assert pd < ed                  # greedy shows fewer distinct items
assert ps > es                  # greedy concentrates impressions
assert eb > pb                  # exploring policy ends higher
print("asserts passed")
```

**Output (my run):**
```text
CTR 5.00% -> 4.70% = -6.0% relative; NDCG 0.500 -> 0.515 = +3.0% relative
popularity slate CTR first20=0.0750 last20=0.0644 (-14.1%) distinct items shown=5 top5 impression share=1.00
explore    slate CTR first20=0.0718 last20=0.1392 (+94.0%) distinct items shown=300 top5 impression share=0.60
asserts passed
```

**Follow-ups:**
- How big should the random slice be? Size it for the smallest tail-versus-head CTR gap you care about, using the two-proportion sample-size formula on impressions; typically 1 to 2% of traffic is enough because impressions are plentiful.
- Can you fix it without exploration? Partly: IPS-weighted training and diversity constraints help, but they cannot learn about items with zero exposure, so some exploration is still needed.
- How does this relate to Book 6 Part 1, Q39 ("A recommendation model refresh raised click-through rate by 5%, but catalogue diversity fell ...")? That question is about weighing a short-term CTR lift against long-term harm and setting up a holdout for the decision; this one is about why a deployed ranker slides over weeks and how to prove the loop. The long-term holdout idea carries over.

**Common mistakes:**
- Taking logged-click NDCG as proof of a better ranker.
- Blaming seasonality without checking exposure concentration.
- Adding a diversity re-ranker without measuring whether it helps CTR or revenue.
- Running exploration without a budget, or forgetting to log exposure propensities so they cannot be used later.
- Treating the 6% as points when it is relative, or the reverse.

### Q22 ⭐⭐ 🟡 A RAG support chatbot's thumbs-up rate fell from 78% to 69% in a week with no release from your team, and the LLM provider had pushed a silent model update. Explain how you would confirm the cause, what regression evidence you need from a fixed test set, and how to guard against provider-side change in future.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** A thumbs-up drop with no release on my side points to something I do not control, so I replay a fixed, versioned question set through the old and new provider behaviour, show the paired drop, and then lock the provider version and add a daily canary.

**Clarifying questions:**
- Can I pin or even see the provider's model version, and do my logs record the version string returned? Without it I cannot date the change.
- Did anything else change that week: traffic mix, new documents indexed, a UI change to the thumbs button, a marketing push? These are rival causes.
- How many votes per week, and what share of answers get a vote? Few votes or a small share means selection bias.
- Do I have a frozen test set with expected answers or rubric scores from before the change? If not, building one is step zero.
- Is the retrieval layer unchanged (same index, same prompts, same temperature)? I need to isolate the generator.

**Approach:**
1. Rule out measurement: thumbs-up rate per day around the change date, vote volume, UI changes, user mix. A step change that lines up with the provider date is the first clue.
2. Check for retrieval or data changes: same retrieved passages for the same queries, same index version, same prompt hash.
3. Replay a fixed regression set (illustrative 300 questions) through the current provider and through any pinned older snapshot or archived outputs from before the change, with the same prompts and retrieved context.
4. Compare pass/fail per question with a paired test (exact McNemar): count questions that passed before and fail now versus the reverse.
5. Read the failures: format changes, refusals, shorter answers, citation style, tone. Provider updates usually change style and refusal behaviour, not only knowledge.
6. Mitigate: pin a dated model version if the provider offers one, adjust the prompt for the new behaviour, or switch provider/version; re-run the regression set before any change goes live.
7. Guard for the future: a daily canary of fixed questions with an alert on the pass rate, a provider-change log, and an eval gate for every model or prompt update.

**Metrics:**
- Thumbs-up rate = thumbs-up votes / (thumbs-up + thumbs-down votes), plus vote rate = votes / answers shown.
- Regression pass rate = questions meeting the rubric / questions in the fixed set.
- Paired discordance: b = passed before and failed now, c = failed before and passed now; the test statistic uses b versus c only.
- Guardrails: refusal rate, average answer length, latency, cost per answer, citation validity.

**Risks:**
- Thumbs are self-selected and noisy; a changed UI or user mix can move them without any model change.
- The fixed set can be stale; it may not represent today's questions.
- You cannot rerun the "before" model if the provider has retired it. Archive outputs on a schedule so a baseline exists.
- LLM-judge scores on the regression set can drift too (see Book 6 Part 2, Q45).
- A canary with too few questions misses small drops.

**What the interviewer scores:**
- Strong: separates "users are unhappier" from "answers got worse", using a controlled replay. Weak: guesses it is the provider.
- Strong: uses a paired comparison on the same questions. Weak: compares two different samples of live traffic.
- Strong: proposes pinning, a canary and an eval gate. Weak: only suggests re-prompting.
- Strong: notes the missing model-version logging as a root gap.

**Example:** (illustrative) 3,000 votes in each week: 78% is 2,340 up, 69% is 2,070 up; the two-proportion z is 7.9, so it is not noise, but it says nothing about cause. The fixed set has 300 questions: 255 passed before (85%), 231 pass now (77%). Of the discordant pairs, 38 went pass to fail and 14 went fail to pass: 255 - 38 + 14 = 231. The exact McNemar p-value is 0.0012 and the 95% interval for the paired difference is -12.6 to -3.4 points. A daily unpaired canary of 300 questions could only see a drop of about 8 points with 80% power, so a canary needs more questions or a paired design. Weak: "The provider changed it, nothing we can do." Strong: "Here is the paired replay showing an 8-point fall on the same 300 questions; I will read the 38 regressions, then pin a version and add a canary."

**Code:**
```python
import numpy as np
from scipy import stats

# Thumbs-up: illustrative 3,000 votes per week
n = 3000
up0, up1 = round(0.78 * n), round(0.69 * n)
assert (up0, up1) == (2340, 2070)
p0, p1 = up0 / n, up1 / n
pool = (up0 + up1) / (2 * n)
z = (p0 - p1) / np.sqrt(pool * (1 - pool) * 2 / n)
print(f"thumbs-up {p0:.0%} -> {p1:.0%}, z={z:.1f}")
assert z > 6          # not noise, but says nothing about cause

# Fixed regression set: 300 questions, same questions, same prompts, pinned old vs new provider run
total = 300
pass_before = 255       # 85%
pass_after = 231        # 77%
b_lost, c_gained = 38, 14       # discordant pairs: pass->fail, fail->pass
assert pass_before - b_lost + c_gained == pass_after
assert pass_before / total == 0.85 and pass_after / total == 0.77
res = stats.binomtest(b_lost, b_lost + c_gained, 0.5)       # exact McNemar
print(f"fixed set {pass_before/total:.0%} -> {pass_after/total:.0%}; lost {b_lost}, gained {c_gained}; exact McNemar p={res.pvalue:.4f}")
assert res.pvalue < 0.01
# 95% interval for the paired difference in pass rate (normal approx on paired differences)
d = (c_gained - b_lost) / total
se = np.sqrt((b_lost + c_gained) - (b_lost - c_gained) ** 2 / total) / total
print(f"difference {d*100:+.1f} points, 95% CI [{(d-1.96*se)*100:+.1f}, {(d+1.96*se)*100:+.1f}]")
assert d + 1.96 * se < 0

# Smallest drop a daily 300-question canary can see (pass rate .85, unpaired, 80% power, alpha .05)
sd = np.sqrt(2 * 0.85 * 0.15 / 300)
mde = (1.96 + 0.84) * sd
print(f"unpaired canary of 300: minimum detectable drop about {mde*100:.1f} points")
assert 0.07 < mde < 0.09
```

**Output (my run):**
```text
thumbs-up 78% -> 69%, z=7.9
fixed set 85% -> 77%; lost 38, gained 14; exact McNemar p=0.0012
difference -8.0 points, 95% CI [-12.6, -3.4]
unpaired canary of 300: minimum detectable drop about 8.2 points
```

**Follow-ups:**
- The provider will not let you pin a version. What do you do? Keep your own regression set and canary, own a fallback provider or model path, and treat each provider change as a release that must pass your eval gate.
- Why paired and not two proportions on the replay? The same questions are used twice, so only the questions that changed state carry information; pairing gives a tighter test.
- How would you size the canary? Pick the smallest drop that matters (say 4 points), use the paired or unpaired sample-size formula, and run it daily or at provider-change signals.

**Common mistakes:**
- Declaring the provider guilty from the thumbs drop alone.
- Comparing this week's live traffic with last week's instead of replaying the same questions.
- Not logging the model version and prompt hash with every answer.
- Building a canary too small to see a 4 to 8 point change.
- Fixing the prompt before reading the failure cases.

### Q23 ⭐⭐ 🟡 Answer quality in a RAG system dropped after the team re-embedded only the newly added documents with a newer embedding model, leaving the old vectors in the same index. Retrieval hit rate on a fixed query set went from 82% to 71%. Explain why mixing embedding versions hurts, how you would verify it, and how to fix and prevent it.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** Vectors from two different embedding models live in two different geometries, so their similarity scores cannot be compared in one index; I would prove it by splitting the hit rate by old and new documents, then re-embed everything with one model (blue-green) and version the index.

**Clarifying questions:**
- Which model embeds the query today, the old one, the new one, or both? This decides which documents become unreachable.
- Do the two models have different dimensions or normalisation? A dimension mismatch would fail loudly; same dimension fails silently.
- How big is the corpus and what does a full re-embed cost and take? It decides between a full re-embed and a gradual migration.
- Is there a fixed query set with labelled relevant documents (the 82% to 71% measurement)? I need to slice it by which model embedded the answer document.
- Can the system keep two indexes side by side? That allows a safe cutover.

**Approach:**
1. Slice the hit-rate query set by the embedding version of the target document (old-embedded versus new-embedded). A mixed index shows old and new targets behaving differently.
2. Check query-side behaviour: which model embeds the query, and what are the top-1 cosine scores for old-document and new-document hits? Different score scales mean the merged ranking is biased.
3. Verify the mechanism offline: re-embed a sample of old documents with the new model and compare hit rate, or embed the same documents with both models and measure cross-model cosine (it will be near chance).
4. Fix: re-embed the whole corpus with the new model into a fresh index, build it in the background, compare hit rate on the fixed query set, then switch traffic; keep the old index for rollback.
5. Prevent: store the embedding model name and version on every vector and on the index; refuse inserts whose version differs from the index; make "model change" mean "new index"; add a retrieval hit-rate check to the deploy gate.

**Metrics:**
- Hit rate at k = queries whose labelled relevant document appears in the top k / all queries. Report by target embedding version.
- Mean reciprocal rank as a second view; mean top-1 cosine by index segment.
- Guardrails: query latency, index build cost, answer-quality score on the fixed set.

**Risks:**
- Normalising or rescaling scores per model can hide the problem without fixing it.
- Dual-querying both models and merging by raw cosine looks reasonable but ranks by score scale, not relevance.
- Partial re-embedding leaves a long tail of old vectors that are quietly unreachable.
- Re-embedding costs money and time; the fixed query set must be representative of real traffic.

**What the interviewer scores:**
- Strong: explains that embedding spaces are model-specific, so cross-model cosine is meaningless. Weak: "the new model is probably worse".
- Strong: verifies with a slice and a controlled re-embed. Weak: just reverts.
- Strong: version metadata plus blue-green index as the prevention. Weak: "tell the team to be careful".

**Example:** (illustrative toy, 2,000 documents, 400 queries, 15% of documents embedded by a new model, whose cosines sit higher because it has a large shared direction). The baseline with everything in the old model finds the target in the top 5 for 100% of queries (the toy is easy on purpose). In the mixed index: querying with the old model gives 0.91 overall but 0.00 for new-embedded targets; querying with the new model gives 0.10 overall and 0.00 for old-embedded targets; querying both and merging by raw cosine gives 0.33, because new-model cosines are larger (mean top-1 cosine 0.93 versus 0.78) and crowd out the old documents. Re-embedding everything with the new model returns 1.00. The prompt's 82% to 71% is a milder version of the same effect, probably because other signals (keyword search, a reranker) rescue part of the loss; I would not claim which. Weak: "retrieval got worse, add more documents." Strong: "Slice by embedding version, show old and new targets behave differently, rebuild one index."

**Code:**
```python
import numpy as np
rng = np.random.default_rng(23)
D, N, Q, NEW_FRAC, K = 32, 2000, 400, 0.15, 5

def unit(m): return m / np.linalg.norm(m, axis=1, keepdims=True)
latent = unit(rng.normal(size=(N, D)))
def rot():
    q, _ = np.linalg.qr(rng.normal(size=(D, D))); return q
RA, RB = rot(), rot()
common = unit(rng.normal(size=(1, D)))[0]             # model B shares a big common direction (higher cosines)
def embA(x): return unit(x @ RA + 0.05 * rng.normal(size=x.shape))
def embB(x): return unit(unit(x @ RB + 0.05 * rng.normal(size=x.shape)) + 1.5 * common)

is_new = rng.random(N) < NEW_FRAC
docA = embA(latent); docB = embB(latent)
target = rng.integers(0, N, Q)
qlat = unit(latent[target] + 0.12 * rng.normal(size=(Q, D)))
qA, qB = embA(qlat), embB(qlat)
docs_mixed = np.where(is_new[:, None], docB, docA)      # index: old docs in A, new docs in B
docs_allA = docA

def hit(scores):
    top = np.argsort(-scores, axis=1)[:, :K]
    return (top == target[:, None]).any(axis=1)

h_clean = hit(qA @ docs_allA.T)                                    # all docs and queries in model A
h_Aq = hit(qA @ docs_mixed.T)                                      # mixed index, query embedded by A
h_Bq = hit(qB @ docs_mixed.T)                                      # mixed index, query embedded by B
# dual query: score old docs with qA, new docs with qB, merge on raw cosine
s_dual = np.where(is_new[None, :], qB @ docB.T, qA @ docA.T)
h_dual = hit(s_dual)
# fix: re-embed everything with B and query with B
h_fix = hit(qB @ docB.T)
print(f"new-model share of index: {is_new.mean():.0%}")
for name, h in [("all old, A query (baseline)", h_clean), ("mixed, A query", h_Aq), ("mixed, B query", h_Bq),
                ("mixed, dual query merged by raw score", h_dual), ("all re-embedded with B", h_fix)]:
    print(f"{name:40s} hit@{K} = {h.mean():.2f}  | target old docs {h[~is_new[target]].mean():.2f}  target new docs {h[is_new[target]].mean():.2f}")
assert h_clean.mean() > 0.7
assert h_Aq.mean() < h_clean.mean() - 0.05
assert h_Bq.mean() < h_clean.mean() - 0.3
assert h_dual.mean() < h_clean.mean() - 0.03
assert abs(h_fix.mean() - h_clean.mean()) < 0.08
# the cosine between a doc and its own query is on a different scale in each space
print("mean top-1 cosine A:", round(float((qA @ docA.T).max(1).mean()), 2), " B:", round(float((qB @ docB.T).max(1).mean()), 2))
print("asserts passed")
```

**Output (my run):**
```text
new-model share of index: 14%
all old, A query (baseline)              hit@5 = 1.00  | target old docs 1.00  target new docs 1.00
mixed, A query                           hit@5 = 0.91  | target old docs 1.00  target new docs 0.00
mixed, B query                           hit@5 = 0.10  | target old docs 0.00  target new docs 1.00
mixed, dual query merged by raw score    hit@5 = 0.33  | target old docs 0.26  target new docs 1.00
all re-embedded with B                   hit@5 = 1.00  | target old docs 1.00  target new docs 1.00
mean top-1 cosine A: 0.78  B: 0.93
asserts passed
```

**Follow-ups:**
- Could you align the two spaces with a learned linear map? Sometimes approximately, but it needs paired data and loses quality; a full re-embed is the safe answer when the corpus is not huge.
- What if the corpus is huge? Migrate by shard into a new index while serving from the old, and switch only when the whole index is on one version; never mix inside one search.
- What belongs on the deploy gate? Fixed-query hit rate by segment, the embedding version tag check, and a latency check.

**Common mistakes:**
- Embedding only new documents with the new model "to save cost".
- Merging results from two indexes by raw similarity score.
- No model-version metadata, so nobody can tell which vectors are which.
- Judging only the overall hit rate and missing the old-versus-new split.
- Rebuilding the index in place with no rollback copy.

### Q24 ⭐⭐ 🟡 A demand model that had a bias of about zero now over-forecasts by 15% after a competitor cut prices and the company changed its own pricing. MAPE has risen from 11% to 18%. Explain how you would diagnose a structural break, what you would do before you can retrain on enough new data, and how you would keep the business safe in the meantime.
**Asked at:** No interview page located; forecast-monitoring practitioner pages (demandplanning.net MAPE and bias, John Galt Solutions, 42signals forecast-drift post) describe bias, structural breaks and MAPE blind spots, so editor-designed; search snippets only, not opened
**Say this first (1 line):** A bias that jumps from zero to +15% right after a price cut is a structural break, not noise, so I confirm it with bias and change-point checks, patch the forecast with a short-lag bias correction and manual overrides, and retrain once I have enough post-break weeks.

**Clarifying questions:**
- Exactly when did the competitor cut and when did we change our own price? The break date tells me how many post-break weeks exist.
- Is price an input to the model today? If not, it is blind to this cause; if yes, the new price range may be outside what it saw.
- Is the over-forecast uniform across products and regions, or concentrated where the competitor competes? It decides between one global correction and segment corrections.
- What do the forecasts drive (stock, purchase orders, markdown)? Over-forecast of 15% means excess stock, and I need its cost.
- Are there other changes in that window (promotions, stock-outs that censor demand, tracking changes)? These look like a break too.

**Approach:**
1. Separate bias from error size: report bias = sum(forecast - actual) / sum(actual) next to MAPE. Bias near 0 before, +15% after, is a level shift; MAPE alone hides its direction.
2. Locate the break: plot weekly bias, run a CUSUM or change-point check, and line the date up with the competitor and own price events.
3. Rule out data errors and stock-outs (censored demand would push actuals down and create a false over-forecast).
4. Segment: which categories and regions carry the bias? Price-sensitive segments first.
5. Interim fix before retraining: multiply the forecast by a rolling forecast-to-actual ratio from the last few matured weeks (lagged so only known actuals are used), let planners override, and widen safety-stock logic so that it is not driven by the bad point forecast.
6. Model fix: add price and competitor-price ratio as features; with only a few weeks post-break use a hierarchical or elasticity-prior approach, or train on all history with a regime indicator and interaction terms.
7. Monitor: weekly bias alert (not only MAPE), a break detector, and a rule that any pricing change notifies the forecasting team.

**Metrics:**
- Bias = (sum of forecasts - sum of actuals) / sum of actuals over a window.
- MAPE = mean over weeks of |forecast - actual| / actual (state the treatment of zero actuals).
- Tracking signal or CUSUM of percentage error for break detection.
- Business guardrails: excess stock weeks of cover, stock-out rate, markdown cost.

**Risks:**
- Retraining immediately on a few weeks can overfit noise; retraining late keeps the bias.
- A rolling correction lags a second break and can over-correct once the model is fixed.
- Stock-outs censor demand; the data can mislead.
- Price effects differ by category; one global multiplier fixes the total but not the mix.

**What the interviewer scores:**
- Strong: names bias separately from MAPE and ties the break to the price events. Weak: "retrain".
- Strong: gives an interim control that works with little data. Weak: waits for data.
- Strong: asks what the forecast decides, and sizes the business risk. Weak: only talks about the model.
- Strong: monitors bias and breaks. Weak: monitors accuracy only.

**Example:** (illustrative) Percentage errors are roughly Normal. If the spread gives a MAPE of 11% at zero bias, adding a +15% bias gives a MAPE of about 16.9%, so the prompt's move from 11% to 18% is plausible and is mostly the bias. In a 120-week simulation with the break at week 60 (demand ends up 1/1.15 of what the old pattern implies): before the break the bias is -0.9% and the MAPE 12.3%; after it the bias is +14.6% and the MAPE 17.1%. A CUSUM alarm fires at week 66, six weeks after the break. A rolling forecast-to-actual ratio lagged by two weeks brings the post-break bias to +2.9% and the MAPE to 12.5% without any retraining. Weak: "MAPE went up, retrain the model on the last month." Strong: "Bias is +15% since the price cut; I patch with a lagged ratio and overrides now and add price features once there are enough weeks."

**Code:**
```python
import numpy as np
from scipy.stats import norm

# Check the prompt: can bias 0 -> +15% and MAPE 11% -> 18% both be true?
# Percentage error e = (forecast - actual)/actual ~ Normal(mu, s). E|e| for a folded normal:
def mape_fold(mu, s): return s * np.sqrt(2 / np.pi) * np.exp(-mu**2 / (2 * s**2)) + mu * (1 - 2 * norm.cdf(-mu / s))
s = 0.11 / np.sqrt(2 / np.pi)                  # s that gives MAPE 11% at zero bias
print(f"spread giving MAPE 11% at zero bias: {s:.3f}; MAPE with +15% bias: {mape_fold(0.15, s):.3f}")
assert abs(mape_fold(0, s) - 0.11) < 1e-9 and 0.16 < mape_fold(0.15, s) < 0.19   # consistent with the prompt's 18%

# Simulation: 120 weekly points, break at week 60 (price cut; model does not see price)
rng = np.random.default_rng(24)
W, BREAK = 120, 60
actual = 1000 * (1 + 0.1 * np.sin(np.arange(W) * 2 * np.pi / 52)) * 1.0
actual[BREAK:] *= 1 / 1.15                      # demand ends up 1/1.15 of what the old pattern implies
fc = 1000 * (1 + 0.1 * np.sin(np.arange(W) * 2 * np.pi / 52)) * np.exp(rng.normal(0, s, W))
act = actual * np.exp(rng.normal(0, 0.02, W))
err = (fc - act) / act
pre, post = err[:BREAK], err[BREAK:]
print(f"before: bias {pre.mean():+.3f} MAPE {np.abs(pre).mean():.3f} | after: bias {post.mean():+.3f} MAPE {np.abs(post).mean():.3f}")

# CUSUM on the percentage error: flag when cumulative positive drift passes a limit
k, h = 0.08, 0.50
c, flag = 0.0, None
for t in range(W):
    c = max(0.0, c + err[t] - k)
    if c > h and flag is None: flag = t
print("break at week", BREAK, "| CUSUM alarm at week", flag)
assert flag is not None and BREAK <= flag <= BREAK + 6

# Interim patch: multiply forecast by a bias correction learned from the last 4 matured weeks (lag 2)
adj = fc.copy()
for t in range(BREAK, W):
    lo, hi = max(0, t - 6), t - 2
    ratio = (fc[lo:hi] / act[lo:hi]).mean()      # recent forecast-to-actual ratio
    adj[t] = fc[t] / ratio
err_adj = (adj - act) / act
print(f"after, with rolling ratio patch: bias {err_adj[BREAK:].mean():+.3f} MAPE {np.abs(err_adj[BREAK:]).mean():.3f}")
assert np.abs(err_adj[BREAK + 8:]).mean() < np.abs(post[8:]).mean()
print("asserts passed")
```

**Output (my run):**
```text
spread giving MAPE 11% at zero bias: 0.138; MAPE with +15% bias: 0.169
before: bias -0.009 MAPE 0.123 | after: bias +0.146 MAPE 0.171
break at week 60 | CUSUM alarm at week 66
after, with rolling ratio patch: bias +0.029 MAPE 0.125
asserts passed
```

**Follow-ups:**
- Why not just wait six weeks and retrain? Six weeks at +15% bias is real excess stock; the interim patch costs little and is reversible.
- How would you pick the correction window? Short enough to track the new level (4 to 6 weeks), long enough that noise does not move it; test it on past breaks and check how it behaves after the model is retrained.
- How do you know the break is price and not a stock-out? Check on-hand stock and sales per day; stock-outs show censored sales, price shows lower demand with stock available.

**Common mistakes:**
- Looking at MAPE only and missing that the error is one-sided.
- Retraining at once on too few weeks and swapping one bias for another.
- Leaving the rolling correction on after the model is fixed (double correction).
- Ignoring stock-out censoring.
- Not telling planners which forecasts are being overridden and why.

### Q25 ⭐⭐ 🟡 A payments fraud model's catch rate on confirmed fraud fell from 85% to 70% over three months while its false-positive rate stayed flat, and analysts say fraudsters changed tactics. Explain how you would confirm adversarial adaptation, why naive retraining on recent flagged cases is risky, and which layered responses you would use.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** A falling catch rate with a flat false-positive rate means fraud changed, not the model, so I show it with confirmed-fraud cohorts split by tactic, refuse to retrain only on flagged cases because they hide the new tactic, and respond in layers with random audits, rules, features and a retrain on proper labels.

**Clarifying questions:**
- How is "confirmed fraud" labelled, and how late? Chargebacks lag, so recent months are under-counted and the 70% may still move.
- Did the transaction mix or approval policy change, or was a rule that used to catch fraud removed? Those drop catch rate without any adversary.
- Is the catch rate measured at a fixed score threshold, and is the threshold unchanged?
- Which analyst signals say tactics changed: new merchant types, device patterns, small-amount probing, mule accounts?
- Is there a random audit sample today? It is the clean way to measure fraud the model never flags.

**Approach:**
1. Confirm the drop is real and not label lag: compare catch rate for equal-maturity cohorts (same days since transaction) and report a confidence interval.
2. Split confirmed fraud by "tactic" using features and analyst tags: old patterns versus new. Compute the catch rate in each.
3. Look at the score distribution of confirmed fraud: new fraud clusters just below the threshold or at low scores, and its features (new devices, merchants, amount patterns) are unlike the training data.
4. Check what stayed the same: false-positive rate flat and good-traffic distribution stable point to the fraud side moving, not the model decaying everywhere.
5. Avoid the naive retrain: a training set of recent flagged cases contains mostly the old tactic, because the new one was not flagged; unflagged new fraud is labelled legitimate unless the chargeback arrives. That reinforces the blind spot.
6. Layered response: a random audit slice for unbiased labels; fast rules and velocity or device-linking features for the new tactic; a retrain on confirmed outcomes with recency weights and the new features; consider a second model or anomaly score for novelty; keep an analyst feedback loop.
7. Monitor catch rate per tactic and per segment, not only overall, and track adversary signals (probing, reaction after each rule change).

**Metrics:**
- Catch rate (recall) = confirmed fraud cases flagged / confirmed fraud cases, by matured cohort.
- False-positive rate = legitimate transactions flagged / legitimate transactions.
- Catch rate by tactic = flagged cases of that tactic / all confirmed cases of that tactic.
- Guardrails: approval rate, customer friction (declines of good users), analyst queue size and review time.

**Risks:**
- Label delay makes the latest cohorts look better or worse than they are.
- Selection bias: labels exist mainly where the system or analysts looked.
- Adversaries adapt to each fix; rules decay.
- A new rule raises false positives and customer friction.
- A random audit costs reviewer time and lets some fraud through, by design.

**What the interviewer scores:**
- Strong: separates "fraud changed" from "model broke" with a tactic split. Weak: assumes drift and retrains.
- Strong: explains why flagged-only training data is biased. Weak: "retrain on the last three months".
- Strong: layered response with time scales (rules now, model later) and the audit slice. Weak: one fix.
- Strong: mentions label maturity. Weak: treats the 70% as final.

**Example:** (illustrative) Take 1,000 confirmed fraud cases. If the old tactic is caught 85% of the time and the new one 10%, a 70% overall catch rate needs the new tactic to be 20% of fraud: 800 old cases (680 caught) and 200 new (20 caught), 700 of 1,000. A z-test with 1,000 cases in each period gives z = 8.0 for 85% versus 70%, so the drop is not noise. Among flagged fraud, the new tactic is only 20 of 700 = 2.9%, against 20% of real fraud, and 180 new-tactic fraud cases look like normal traffic. A flagged-only retrain would learn almost nothing about the new tactic. A random audit of 2,000 transactions at a 0.5% fraud base rate finds about 10 fraud cases (12 in my seeded run), enough to start measuring the blind spot. Weak: "Retrain on the recent fraud we caught." Strong: "Split by tactic first; recent flagged cases are the cases the model already knew."

**Code:**
```python
import numpy as np
from scipy.stats import norm

# Prompt check: catch rate 85% -> 70% with flat FPR. Illustrative month: 1,000 confirmed fraud cases.
# Two tactics: old (still caught at 85%) and new (caught at 10%).
n_fraud, catch_old, catch_new = 1000, 0.85, 0.10
share_new = (0.85 - 0.70) / (catch_old - catch_new)      # mix that gives 70% overall
print(f"new-tactic share needed for 70% overall: {share_new:.2f}")
assert abs(share_new - 0.20) < 1e-12
old_n, new_n = round(n_fraud * (1 - share_new)), round(n_fraud * share_new)
caught_old, caught_new = old_n * catch_old, new_n * catch_new
caught_old, caught_new = round(caught_old), round(caught_new)
assert (old_n, new_n, caught_old, caught_new) == (800, 200, 680, 20)
overall = (caught_old + caught_new) / n_fraud
assert abs(overall - 0.70) < 1e-12
print(f"old {old_n} cases, caught {caught_old:.0f}; new {new_n} cases, caught {caught_new:.0f}; overall {overall:.0%}")

# Is the drop real? Two catch rates, 1,000 cases each (previous quarter vs this quarter)
p1, p2, n = 0.85, 0.70, 1000
pool = (p1 + p2) / 2
z = (p1 - p2) / np.sqrt(pool * (1 - pool) * 2 / n)
print(f"z for 85% -> 70% with n=1000 each: {z:.1f}")
assert z > 7

# Naive retrain on 'recent flagged cases': fraud labels only exist where we flagged (or chargebacks come later)
flagged_fraud = caught_old + caught_new
share_new_in_flagged = caught_new / flagged_fraud
print(f"new tactic is {share_new:.0%} of real fraud but {share_new_in_flagged:.1%} of flagged fraud")
assert round(share_new_in_flagged, 3) == 0.029
# the model learns the old pattern even more strongly; the 180 missed new-tactic cases look like normal traffic
missed_new = new_n - caught_new
print("new-tactic fraud labelled as legitimate in a flagged-only training set:", int(missed_new))
assert missed_new == 180

# Fix: add a random audit sample. Auditing 2,000 of 200,000 transactions (1%) at a 0.5% fraud base rate
rng = np.random.default_rng(25)
audit = rng.binomial(1, 0.005, 2000)
print("random audit finds", audit.sum(), "fraud cases in 2,000 reviewed (expected about 10)")
assert 3 <= audit.sum() <= 20
```

**Output (my run):**
```text
new-tactic share needed for 70% overall: 0.20
old 800 cases, caught 680; new 200 cases, caught 20; overall 70%
z for 85% -> 70% with n=1000 each: 8.0
new tactic is 20% of real fraud but 2.9% of flagged fraud
new-tactic fraud labelled as legitimate in a flagged-only training set: 180
random audit finds 12 fraud cases in 2,000 reviewed (expected about 10)
```

**Follow-ups:**
- Why is the FPR staying flat informative? It suggests the good-traffic score distribution did not move, so the model is not broadly miscalibrated; the missed cases are a new fraud subpopulation.
- How would you know an adversary is probing? Many small-amount attempts or new accounts testing the threshold, followed by a change in pattern after each rule or model update.
- What if fraud is also reaching you through a channel with no labels? The random audit slice and downstream signals (disputes, customer reports) are the only way to size it.

**Common mistakes:**
- Retraining on flagged-only data.
- Judging the newest cohorts before chargebacks have arrived.
- Fixing with a single rule that fraudsters route around in a week.
- Reporting only overall catch rate and missing the tactic split.
- Having no random audit, so the blind spot cannot be measured.

### Q26 ⭐⭐ 🟡 A search ranker's overall NDCG is stable, but long-tail queries (the 20% that are rare) have worsened by 8% while head queries improved. Explain how segment-level degradation can be hidden by head-query volume, how you would build a sliced evaluation and monitoring view, and what remedies exist.
**Asked at:** Recommender feedback-loop and popularity-bias literature (Mansoury et al. 'Feedback Loop and Bias Amplification in Recommender Systems', a popularity-bias survey on arXiv) plus a Prachub ranking-debugging page; no public interview page for this exact prompt, so editor-designed from the literature; search snippets only, not opened
**Say this first (1 line):** Head queries are most of the volume, so a small head gain can cancel a large tail loss in the overall number; I would report NDCG by query frequency bucket with confidence intervals, alert on the tail slice itself, and fix the tail with better candidate generation, query understanding and tail-focused training data.

**Clarifying questions:**
- Is "20%" the share of queries or of traffic? Long-tail queries are rare, so the two shares differ and the weights in the overall number depend on it.
- How is "long tail" defined (frequency in the last 30 days, a head/torso/tail cut, or a rare-term flag)? The cut decides which queries land in the slice.
- Is NDCG computed from human judgements or from clicks? Clicks on rare queries are sparse and noisy.
- What changed in the ranker: new training data, a popularity feature, a new embedding model? Tail queries often depend on semantic matching.
- What does a failed tail query cost: zero-result pages, abandonment, support contacts?

**Approach:**
1. Slice the evaluation: bucket queries by frequency (head, torso, tail), by intent, by length, by language or script, and by whether the query has results at all. Report NDCG and volume per bucket.
2. Do the weighting arithmetic: overall change = sum of (share x change). A tail drop of 8% with 20% share is a 1.6% drag on the overall, and can be hidden by a head gain.
3. Add uncertainty: with fewer tail queries per week, bootstrap confidence intervals per slice; alert on a slice only when the interval excludes zero change.
4. Diagnose: compare candidate recall (is the right item even retrieved?) versus ranking order (is it retrieved but ranked low?). Tail failures are often retrieval or vocabulary mismatch.
5. Remedies: hybrid lexical plus semantic retrieval, query rewriting and spell correction, data augmentation or synthetic queries for tail, a tail-weighted loss, a separate tail model or fallback, and click-data smoothing so popularity features do not bury rare items.
6. Operationalise: a sliced-metrics dashboard with a minimum-sample rule, a release gate that blocks a launch if a protected slice regresses beyond a set margin, and a golden set of tail queries kept fresh.

**Metrics:**
- NDCG@10 by bucket = mean over queries in the bucket of DCG@10 / ideal DCG@10.
- Volume share by bucket = queries in bucket / all queries (state if by queries or traffic).
- Zero-result rate = queries returning no result / queries; abandonment rate on tail queries.
- Guardrails: head NDCG must not fall, latency, index recall at k.

**Risks:**
- Per-query NDCG is noisy and tail slices are small; a small slice can look worse by chance.
- Changing the bucket definition after seeing the result is slice shopping.
- Click-based labels favour head queries, so the tail looks worse than it is, or better.
- A tail-specific fix can slow queries or hurt the head.

**What the interviewer scores:**
- Strong: shows the weighted-average arithmetic and why the overall metric stays flat. Weak: "the model got worse for some queries".
- Strong: uses intervals and a minimum sample per slice. Weak: reads point estimates.
- Strong: separates retrieval from ranking failure. Weak: "add more data".
- Strong: proposes a release gate on slices. Weak: only a dashboard.

**Example:** (illustrative) Head NDCG is 0.70 on 80% of queries and tail NDCG is 0.50 on 20%. A tail fall of 8% takes it to 0.46, which moves the overall by 0.2 x (-0.04) = -0.008. The head needs to rise from 0.70 to 0.71 to hide it, a gain of only 1.4%. In a seeded simulation with 10,000 queries a week and per-query NDCG sd of 0.3: overall changes -0.0050 with a 95% bootstrap interval of [-0.0121, +0.0024] (flat); head +0.0041 [-0.0038, +0.0121]; tail -0.0412 [-0.0583, -0.0248] (clearly down). Only the tail slice shows the problem. Weak: "Overall NDCG is stable, so no action." Strong: "Show me NDCG by frequency bucket with intervals; the tail can fall while the head hides it."

**Code:**
```python
import numpy as np

# Prompt arithmetic: head 80% / tail 20% of queries; tail NDCG 0.50 -> 0.46 (-8%); overall stable.
head_share, tail_share = 0.8, 0.2
tail0, tail1 = 0.50, 0.46
assert abs((tail1 - tail0) / tail0 + 0.08) < 1e-12
tail_loss = tail_share * (tail1 - tail0)               # -0.008 on overall NDCG
head_gain_needed = -tail_loss / head_share             # head must gain this much for overall to be flat
head0 = 0.70
head1 = head0 + head_gain_needed
print(f"tail drags overall by {tail_loss:+.3f}; head must rise {head0:.2f} -> {head1:.2f} ({head_gain_needed/head0:+.1%}) to hide it")
assert abs(tail_loss + 0.008) < 1e-12 and abs(head1 - 0.71) < 1e-12

# Simulation: per-query NDCG is noisy (sd 0.3). 10,000 queries per week: 8,000 head, 2,000 tail.
rng = np.random.default_rng(26)
def week(head_mean, tail_mean):
    h = np.clip(rng.normal(head_mean, 0.3, 8000), 0, 1); t = np.clip(rng.normal(tail_mean, 0.3, 2000), 0, 1)
    return h, t
h0, t0 = week(0.70, 0.50); h1, t1 = week(0.71, 0.46)
all0, all1 = np.r_[h0, t0], np.r_[h1, t1]
def diff_ci(a, b, B=2000):
    d = [rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean() for _ in range(B)]
    return np.mean(b) - np.mean(a), np.percentile(d, [2.5, 97.5])
for name, a, b in [("overall", all0, all1), ("head", h0, h1), ("tail", t0, t1)]:
    d, ci = diff_ci(a, b)
    print(f"{name:8s} change {d:+.4f}  95% bootstrap CI [{ci[0]:+.4f}, {ci[1]:+.4f}]")
d_all, ci_all = diff_ci(all0, all1)
d_tail, ci_tail = diff_ci(t0, t1)
assert ci_all[0] < 0 < ci_all[1]                       # overall: not distinguishable from flat
assert ci_tail[1] < 0                                  # tail alone: clearly down
print("asserts passed")
```

**Output (my run):**
```text
tail drags overall by -0.008; head must rise 0.70 -> 0.71 (+1.4%) to hide it
overall  change -0.0050  95% bootstrap CI [-0.0121, +0.0024]
head     change +0.0041  95% bootstrap CI [-0.0038, +0.0121]
tail     change -0.0412  95% bootstrap CI [-0.0583, -0.0248]
asserts passed
```

**Follow-ups:**
- How many tail queries do you need? For a slice mean with per-query sd of 0.3, the standard error is 0.3 / sqrt(n); with 2,000 queries it is about 0.0067, so a 0.04 change is visible, but a 0.01 change is not. Pool several weeks for smaller changes.
- Should you optimise the tail at the expense of the head? Not blindly: set a protected-slice rule, such as no head regression beyond a small margin, and weigh by business value.
- Is the tail always low value? No; in some products rare queries carry high intent, so check conversion by bucket.

**Common mistakes:**
- Trusting a single overall metric.
- Reading small-slice point estimates without intervals.
- Defining the slices after looking at the results.
- Fixing ranking when the item was never retrieved.
- Letting popularity features bury new or rare items.

### Q27 ⭐⭐ 🟡 Mean score from a credit model fell from 0.30 to 0.22 this month, but outcomes will not mature for months. Explain the competing hypotheses (a change in applicants, a pipeline bug, a model change, real risk improvement), the checks that separate them using only unlabelled data, and what you would tell the business before labels arrive.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
**Say this first (1 line):** With no outcomes yet, I split the fall in mean score into a change in who is applying and a change in score within each type of applicant, then check pipeline, model and feature health to see which part is real; I tell the business what we know, what we do not, and when labels will tell us.

**Clarifying questions:**
- Was there any change to the model, its features, the scoring service or the data feeds this month? A deployment calendar answers part of this at once.
- Did the applicant source mix change (new partner, marketing channel, product, city)? Mix is the first non-model cause.
- Did the policy upstream of the model change (pre-filters, eligibility rules, cut-offs)? It changes who reaches the model.
- Is the score a probability of default, and is it calibrated? A mean-score fall only means lower risk if calibrated.
- Do we have partial early signals (first-payment default, early delinquency)? They give a weak read before full labels.

**Approach:**
1. Rule out a plain bug: null rates, ranges, units and schema checks on every input feature; compare feature distributions to last month with PSI; check the scoring service version and that the model hash is unchanged.
2. Replay test: re-score last month's applications through the current pipeline. If scores differ, the pipeline or model changed; if not, the inputs changed.
3. Decompose the fall: segment applicants (for example prime, near-prime, subprime, or by channel) and split the change into a mix effect (shares changed) and a within-segment effect (scores moved inside a segment).
4. If it is mostly mix, check whether the new mix is plausible (marketing, partner, policy change). If within-segment, find which features moved and why (new data source, changed bureau fields, income capture).
5. Look at early indicators: first-payment default, early delinquency and application-level proxies, with caution about their power.
6. Communicate: "Mean score fell 0.08; about half is a change in applicant mix; the rest is inside segments and I am checking features. No evidence of a bug if the replay matches. Risk is unconfirmed until outcomes mature; here are the early indicators and the date to re-check." Avoid declaring that risk improved.
7. Put in place: a feature and score-drift dashboard with alerts and a rule that applicant-mix changes are announced to the model team.

**Metrics:**
- Mean score = sum of scores / number of applicants, by month and by segment.
- Mix effect = sum over segments of (share_this - share_last) x mean_last; within-segment effect = sum of share_this x (mean_this - mean_last). They add exactly to the total change.
- PSI by feature and for the score; null rate; replay score difference.
- Guardrails: approval rate, early delinquency, rejection reasons.

**Risks:**
- A lower mean score is not lower risk unless the model is calibrated and the mix is understood.
- Reweighting by observed segments assumes the segments are stable definitions.
- Early indicators are weak and biased by who was approved.
- Acting on the score (for example loosening cut-offs) before outcomes mature locks in losses.

**What the interviewer scores:**
- Strong: lists competing hypotheses and a check for each that needs no labels. Weak: "the model must be fine/broken".
- Strong: mix versus rate decomposition and a replay test. Weak: only PSI.
- Strong: honest communication that risk is unconfirmed. Weak: tells the business risk improved.
- Strong: asks about deployments and policy changes. Weak: jumps to modelling.

**Example:** (illustrative) Segments last month: prime 40% (mean score 0.12), near-prime 30% (0.30), subprime 30% (0.54), mean 0.30. This month: prime 50% (0.092), near-prime 30% (0.26), subprime 20% (0.48), mean 0.22. The change is -0.08. The mix effect is (0.10)(0.12) + 0 + (-0.10)(0.54) = -0.042, which is 52% of it; the within-segment effect is 0.5(-0.028) + 0.3(-0.04) + 0.2(-0.06) = -0.038, or 48%. All three segments' scores fell, which a mix change alone cannot explain, so something also moved inside segments: pipeline, model, feature data, or real improvement. Weak: "The score fell, so risk improved." Strong: "Half is mix; the other half is inside every segment, so I replay and check features before saying anything about risk."

**Code:**
```python
# Mix versus rate decomposition of a fall in mean score (illustrative segments)
seg = ["prime", "near_prime", "subprime"]
share0, mean0 = [0.40, 0.30, 0.30], [0.12, 0.30, 0.54]
share1, mean1 = [0.50, 0.30, 0.20], [0.092, 0.26, 0.48]
m0 = sum(s * m for s, m in zip(share0, mean0)); m1 = sum(s * m for s, m in zip(share1, mean1))
print(f"mean score last month {m0:.3f}, this month {m1:.3f}, change {m1-m0:+.3f}")
assert abs(m0 - 0.30) < 1e-9 and abs(m1 - 0.22) < 1e-9
mix = sum((s1 - s0) * m for s0, s1, m in zip(share0, share1, mean0))        # shares change, old means
rate = sum(s1 * (b - a) for s1, a, b in zip(share1, mean0, mean1))          # means change, new shares
print(f"mix effect {mix:+.3f} ({mix/(m1-m0):.0%}), within-segment effect {rate:+.3f} ({rate/(m1-m0):.0%})")
assert abs(mix + rate - (m1 - m0)) < 1e-12
assert abs(mix - (-0.042)) < 1e-12 and abs(rate - (-0.038)) < 1e-12
for sname, a, b in zip(seg, mean0, mean1):
    print(f"  {sname:10s} mean {a:.3f} -> {b:.3f}  ({b-a:+.3f})")
# Which segments carry the within-segment fall?
contrib = [s1 * (b - a) for s1, a, b in zip(share1, mean0, mean1)]
print("within-segment contributions:", [round(c, 3) for c in contrib])
assert all(c < 0 for c in contrib)     # fall is in every segment: points at pipeline/model/real improvement, not mix alone
print("asserts passed")
```

**Output (my run):**
```text
mean score last month 0.300, this month 0.220, change -0.080
mix effect -0.042 (52%), within-segment effect -0.038 (48%)
  prime      mean 0.120 -> 0.092  (-0.028)
  near_prime mean 0.300 -> 0.260  (-0.040)
  subprime   mean 0.540 -> 0.480  (-0.060)
within-segment contributions: [-0.014, -0.012, -0.012]
asserts passed
```

**Follow-ups:**
- What would a replay mismatch tell you? That the pipeline, feature data or model changed even for the same applicants, so it is not applicant mix.
- What would you say if everything checks out? That the evidence points to a mix shift and unchanged pipeline, with risk still unconfirmed until outcomes mature, and that I will track early delinquency.
- Can you decompose with continuous features instead of segments? Yes, by reweighting this month's applicants to last month's feature distribution and rescoring, which gives the within-segment part without choosing segments.

**Common mistakes:**
- Equating a lower score with lower risk.
- Skipping the replay test.
- Looking only at the overall distribution and missing the segment shift.
- Reassuring the business without saying what is unknown.
- Forgetting upstream policy or source changes.

### Q28 ⭐⭐ 🟡 A conversion model looks badly calibrated on the most recent seven days: predicted 5% against observed 1.5% for yesterday's cohort. The attribution window is seven days, so recent cohorts have not finished converting. Explain how label maturation creates this artefact, how you would restrict or adjust the evaluation, and why this matters for any alert threshold.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
**Say this first (1 line):** Yesterday's cohort has had only a fraction of its seven days to convert, so the observed rate is low by construction; I compare the model against a maturity-adjusted expectation, or only evaluate cohorts that have finished their window, and I set alerts on matured cohorts.

**Clarifying questions:**
- What is the conversion-delay curve (share of eventual conversions by day since click)? It converts "age 1 day" into an expected share of matured conversions.
- Is the attribution window fixed at seven days for every conversion, and does the model predict conversion within seven days? The label definition must match the window.
- Is the observed 1.5% the same cohort the model scored at 5%? Cohort and prediction date must match.
- Do delays vary by channel or product? A single curve may not fit all.
- How quickly do we need an alert? The answer sets whether we adjust or wait.

**Approach:**
1. Define the label as "converted within seven days of exposure" and write down that it is only complete once seven days have passed.
2. Compute calibration by cohort age (days since exposure). Recent cohorts will look over-predicted; older ones converge to the true level.
3. Estimate the delay curve from fully matured cohorts: share of conversions by day 1, 2, ... 7.
4. Evaluate recent cohorts against a maturity-adjusted prediction: expected observed rate = predicted rate x share matured at that age. Or exclude cohorts younger than seven days.
5. Alert rules: use only matured cohorts for the main calibration alert; use a separate "early read" with the maturity adjustment and a wider band; log cohort age with every metric.
6. Check the adjusted ratio is about 1.0; if not, then look for real miscalibration (traffic mix, tracking, model).

**Metrics:**
- Calibration ratio = sum of predicted conversions / sum of observed conversions, by cohort age.
- Maturity-adjusted ratio = observed rate / (predicted rate x matured share at age).
- Matured share at age d = share of eventual conversions that happen by day d.
- Guardrails: sampling noise (standard error of a rate) so alert bands reflect cohort size.

**Risks:**
- An alert on immature cohorts fires every day and trains people to ignore it.
- The delay curve shifts over time (channel change, a product change), which makes the adjustment wrong.
- Right-censored data also biases training sets: new rows have fewer positive labels.
- Adjusting too aggressively hides a real problem in recent data.

**What the interviewer scores:**
- Strong: names right-censoring / label maturation and shows the ratio converges with age. Weak: "the model is badly calibrated, recalibrate".
- Strong: gives a maturity-adjusted metric or an age cut-off. Weak: waits without a plan.
- Strong: links it to alert design and to training data. Weak: stops at diagnosis.

**Example:** (illustrative) The model predicts 5% and the true seven-day rate is 5%. If 30% of eventual conversions happen by day 1, yesterday's cohort shows 0.05 x 0.30 = 1.5%, and the naive ratio of predicted to observed is 3.33 (5 divided by 1.5). In a seeded simulation with 200,000 users per cohort the observed rate by cohort age (days 1 to 7) is 1.55%, 2.57%, 3.22%, 3.88%, 4.43%, 4.73% and 4.93%, so the predicted-to-observed ratio goes 3.23, 1.95, 1.55, 1.29, 1.13, 1.06, 1.01. Maturity-adjusted, yesterday's ratio is 1.03. The standard error of a 5% rate on a 20,000-user cohort is 0.0015, so an alert band is about plus or minus 0.003. Weak: "Predicted 5% versus 1.5% means we are 3.3 times off." Strong: "Cohort age is one day; expected observed is 1.5%, so the model is fine."

**Code:**
```python
import numpy as np
rng = np.random.default_rng(28)
TRUE_P = 0.05                                    # true 7-day conversion probability (model predicts 5%)
# Share of eventual conversions that have happened by day d after the click (illustrative delay curve)
cdf = np.array([0.30, 0.50, 0.65, 0.78, 0.88, 0.95, 1.00])    # day 1 ... day 7
N = 200_000
print("cohort age (days) | matured share | expected observed | observed (sim) | pred/obs")
rows = []
for age in range(1, 8):
    # each user converts w.p. TRUE_P within 7 days; conversion day drawn from the delay curve
    conv = rng.random(N) < TRUE_P
    u = rng.random(N)
    day = np.searchsorted(cdf, u) + 1             # day of conversion, 1..7
    seen = conv & (day <= age)
    obs = seen.mean()
    rows.append((age, cdf[age - 1], TRUE_P * cdf[age - 1], obs))
    print(f"{age:17d} | {cdf[age-1]:13.2f} | {TRUE_P*cdf[age-1]:17.4f} | {obs:14.4f} | {TRUE_P/obs:.2f}")
assert abs(rows[0][3] - 0.015) < 0.0015            # yesterday's cohort: about 1.5%
assert abs(rows[-1][3] - 0.05) < 0.0015           # fully matured: about 5%
# Prompt arithmetic: predicted 5% vs observed 1.5% would be a miscalibration of 3.33x if read naively
assert abs(0.05 / 0.015 - 3.333) < 0.001
# Maturity-adjusted calibration of age-1 cohort: observed / (pred * share matured)
adj = rows[0][3] / (0.05 * cdf[0])
print(f"maturity-adjusted ratio for yesterday's cohort: {adj:.2f} (1.00 means well calibrated)")
assert 0.9 < adj < 1.1
# Alert rule: only evaluate cohorts at least 7 days old; threshold uses sampling noise at that size
se = np.sqrt(TRUE_P * (1 - TRUE_P) / 20000)
print(f"for a 20,000-user cohort the standard error of a 5% rate is {se:.4f}; alert band about +/-{1.96*se:.4f}")
assert abs(se - 0.00154) < 0.00005
print("asserts passed")
```

**Output (my run):**
```text
cohort age (days) | matured share | expected observed | observed (sim) | pred/obs
                1 |          0.30 |            0.0150 |         0.0155 | 3.23
                2 |          0.50 |            0.0250 |         0.0257 | 1.95
                3 |          0.65 |            0.0325 |         0.0322 | 1.55
                4 |          0.78 |            0.0390 |         0.0388 | 1.29
                5 |          0.88 |            0.0440 |         0.0443 | 1.13
                6 |          0.95 |            0.0475 |         0.0473 | 1.06
                7 |          1.00 |            0.0500 |         0.0493 | 1.01
maturity-adjusted ratio for yesterday's cohort: 1.03 (1.00 means well calibrated)
for a 20,000-user cohort the standard error of a 5% rate is 0.0015; alert band about +/-0.0030
asserts passed
```

**Follow-ups:**
- How does this affect training? Recent rows have incomplete labels and look negative; train only on matured rows or use a survival or delayed-feedback model.
- What if the delay curve changes? Re-estimate it on a rolling window of matured cohorts and alert when it moves.
- Could you alert faster? Yes, with the maturity-adjusted ratio and a wider band, but label it an early read and confirm with the matured cohort.

**Common mistakes:**
- Evaluating calibration on cohorts younger than the window.
- Forgetting to log cohort age with the metric.
- Using one alert threshold for cohorts of different maturity.
- Training on immature rows labelled as negatives.
- Declaring recalibration needed before the cohort has matured.

### Q29 ⭐⭐ 🟡 Revenue loss from a degraded risk model is about Rs 2 lakh per day, a proper retrain and validation takes two weeks, and a business-rule patch could be live tomorrow but is crude. Explain how you would weigh the patch against waiting for the retrain, what you would test about the patch, and how you would retire it later.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** I put numbers on both paths: waiting costs the daily loss times the retrain days, and a patch is worth it when what it recovers, net of its own side-costs and build cost, beats that; I ship the patch only with a backtest, a shadow run, a kill switch and a sunset date.

**Clarifying questions:**
- How certain is the Rs 2 lakh a day figure, and how does it vary by day? The whole case depends on it.
- What does the patch do (extra rule, higher cut-off, manual review) and what is the side-effect, for example good customers wrongly declined?
- Can the patch be backtested on recent data before launch? A crude rule with no backtest can cost more than it saves.
- Is the retrain date firm at two weeks, or could it be faster with a reduced scope?
- Who owns the patch and who can switch it off?

**Approach:**
1. Cost of waiting = daily loss x retrain days. Here 2 lakh x 14 = Rs 28 lakh.
2. Model the patch: days it is live x (share of loss it recovers x daily loss - its daily side-cost) - build cost. Include the day or two before it is live.
3. Find the break-even recovery fraction and the sensitivity: how much must the patch recover to pay for itself, and what happens in a bad case?
4. Test the patch: backtest on the last few weeks of matured data; run it in shadow for a day or two if time allows; check segment effects and customer impact; define a rollback rule and who can use it.
5. Roll out in steps (a share of traffic first) with monitoring of loss, declines and complaints.
6. Retire it: define the exit before launch. Switch it off when the retrained model beats model plus patch on matured data, delete the code by a fixed date, and record it in the change log.
7. Do the retrain in parallel and ask whether the scope can be cut to deliver sooner.

**Metrics:**
- Net benefit of patch = (retrain days - days before live) x (loss per day x recovery fraction - side-cost per day) - build cost.
- Break-even recovery fraction = (build cost / days protected + side-cost per day) / loss per day.
- Guardrails: wrongful decline rate, approval rate, complaints, loss per day by segment.

**Risks:**
- The recovery fraction is an estimate; an untested rule may recover little and hurt customers.
- Patches become permanent and interact with the new model.
- The loss estimate may itself be wrong.
- Fast, ad hoc changes to a risk decision may bypass model-risk governance.

**What the interviewer scores:**
- Strong: quantifies both options, finds a break-even and a worst case. Weak: "patches are hacky" or "ship it".
- Strong: designs the test and the exit. Weak: no plan to remove the patch.
- Strong: respects governance (approval, audit). Weak: ignores it.

**Example:** (illustrative, Rs lakh) Waiting 14 days costs 2 x 14 = 28. A patch live from day 1 protects 13 days. If it recovers 50% of the daily loss (1.0) with a side-cost of 0.2 a day and a build cost of 1.5, the net is 13 x (1.0 - 0.2) - 1.5 = 8.9. Break-even recovery is 15.8%. At 10% recovery the patch loses 1.5; at 20% it gains 1.1; at 30%, 3.7; at 70%, 14.1. In a bad case (20% recovery, side-cost 0.4 a day) it loses 1.5. So I would ship the patch if the backtest supports recovery well above about 16% and the side-cost is controlled. Weak: "Wait for the proper retrain." Strong: "The patch pays for itself above about 16% recovery; I will backtest it, stage it, and set its sunset date."

**Code:**
```python
# Retrain-vs-patch economics (all illustrative, in Rs lakh)
loss_per_day = 2.0
retrain_days = 14
patch_live_day = 1                       # patch live after 1 day, so day 1 is unprotected
build_cost = 1.5                         # patch build and test cost
recover_frac = 0.50                      # share of the daily loss the patch removes (assumption)
side_cost = 0.2                          # extra cost per day from crude rules (e.g. wrongly declined good customers)

wait_loss = loss_per_day * retrain_days
assert wait_loss == 28.0
days_protected = retrain_days - patch_live_day
net_daily = loss_per_day * recover_frac - side_cost
benefit = days_protected * net_daily - build_cost
print(f"wait for retrain: lose {wait_loss:.1f} lakh over {retrain_days} days")
print(f"patch: protected {days_protected} days, net {net_daily:.2f} lakh/day, benefit after build cost = {benefit:.2f} lakh")
assert abs(benefit - 8.9) < 1e-9

# Break-even recovery fraction: days_protected * (loss*r - side) = build_cost
r_star = (build_cost / days_protected + side_cost) / loss_per_day
print(f"break-even recovery fraction: {r_star:.3f}")
assert abs(r_star - 0.1577) < 0.001

print("recovery  net benefit (lakh)")
for r in (0.10, 0.20, 0.30, 0.50, 0.70):
    b = days_protected * (loss_per_day * r - side_cost) - build_cost
    print(f"{r:8.0%}  {b:8.2f}")
# Worst case: patch recovers only 20% and side cost is twice as large
worst = days_protected * (loss_per_day * 0.2 - 0.4) - build_cost
print(f"worst case (20% recovery, side cost 0.4/day): {worst:.2f} lakh")
assert worst < 0
# Retirement rule: switch the patch off when the retrained model beats model+patch on matured shadow data
# (the patch is also deleted from code on a fixed date, e.g. retrain day + 7)
```

**Output (my run):**
```text
wait for retrain: lose 28.0 lakh over 14 days
patch: protected 13 days, net 0.80 lakh/day, benefit after build cost = 8.90 lakh
break-even recovery fraction: 0.158
recovery  net benefit (lakh)
     10%     -1.50
     20%      1.10
     30%      3.70
     50%      8.90
     70%     14.10
worst case (20% recovery, side cost 0.4/day): -1.50 lakh
```

**Follow-ups:**
- What if the patch has uncertain recovery? Use a range and decide on the worst case you can accept; stage the rollout to learn the real recovery in days.
- How would you shorten the retrain? Reduce scope (refit recent data on the same features), reuse the validation pipeline, and parallelise tasks.
- Who approves? The model owner and risk or compliance for decisions affecting customers, with a written change record.

**Common mistakes:**
- Shipping a patch with no backtest.
- No kill switch, owner or end date.
- Counting the patch benefit without its customer-side costs.
- Letting the patch live beside the new model unreviewed.
- Ignoring the days before the patch is live.

### Q30 ⭐⭐ 🟡 A churn model trained before a major price change now shows weaker lift, since the relationship between usage and churn seems to have changed even though input distributions look similar. Explain why this is concept drift rather than data drift, how you would confirm it with labelled data, and what training-window and feature changes you would try.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** It is concept drift when the inputs look the same but the link between inputs and churn has changed; I confirm it by comparing the fitted relationship before and after on labelled data, and I fix it with newer data, regime-aware features and a shorter or weighted training window.

**Clarifying questions:**
- When exactly was the price change, and was it for all customers or a subset? That defines the regimes and a clean before/after split.
- How long until churn labels mature after the change? It tells me how much post-change labelled data exists.
- Did the price change come with other changes (plans, bundles, competitors)? Concept drift has many possible causes.
- How is lift measured (top-decile lift, precision at a retention budget)? I need a metric for the before/after comparison.
- Is price or plan information available as a feature? A model that can see price can learn the new relationship.

**Approach:**
1. Rule out data drift: compare input distributions (means, sds, PSI) before and after; also train a classifier to tell before from after inputs; if it cannot (AUC near 0.5), inputs have not moved.
2. Confirm concept drift on labelled data: evaluate the old model on post-change data and compare with its pre-change performance; then fit a fresh model on post-change data and compare coefficients (or partial dependence) with the old one.
3. Test the change formally: the usage coefficient differs by more than its sampling error, or an interaction between usage and a post-change flag is significant.
4. Check where the relationship changed: by plan, tenure, price band. The price change may bite only some customers.
5. Try fixes in order: add price or plan features and a post-change indicator with interactions; retrain on post-change data when there is enough (otherwise combine old and new with a regime flag or recency weights); shorten the training window; consider separate models per regime.
6. Validate on a post-change time split, not a random split.
7. Monitor: labelled lift weekly once labels mature, a drift check on the model's partial dependence, and a rule that major price or product changes trigger a model review.

**Metrics:**
- Top-decile lift = churn rate in the top 10% by score / overall churn rate.
- AUC on a post-change holdout.
- Usage coefficient and its standard error before and after; PSI per input.
- Guardrails: retention-campaign cost per saved customer, calibration of predicted churn.

**Risks:**
- Few post-change labels, so new models are noisy.
- The new regime may still be settling (customers react over weeks).
- Fixing with a random-split validation hides the problem.
- Retention offers based on the old relationship waste budget.

**What the interviewer scores:**
- Strong: separates covariate (data) drift from concept drift with a test for each. Weak: "distribution changed".
- Strong: confirms with labelled data and shows the changed relationship. Weak: assumes it.
- Strong: proposes regime features and window choices with trade-offs. Weak: "retrain".
- Strong: uses a time-based validation. Weak: random split.

**Example:** (illustrative simulation) Churn depends on usage with a slope of -1.0 before the price change and about -0.2 after, with a higher base level. The estimated usage coefficients are -1.00 (plus or minus 0.03) and -0.21 (plus or minus 0.02): far outside noise. The input means and sds of both features are unchanged (0.01 and -0.01 means, sd 1.0). The old model's AUC falls from 0.753 to 0.574 and its top-decile lift from 2.55 to 1.37 on post-change data; a model refit on the new regime gets AUC 0.604 and lift 1.49 on the same test, which is about the best this noisy relationship allows. With only 3,000 post-change rows, a model fit on just those reaches 0.603, so a small amount of fresh data already recovers most of the loss in this toy. Weak: "The inputs did not change, so the model should be fine." Strong: "Inputs same, relationship different: that is concept drift, and the old model's ranking is what broke."

**Code:**
```python
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(30)

def sigmoid(z): return 1 / (1 + np.exp(-z))
def fit(X, y, it=25):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(it):
        p = sigmoid(Xb @ w); W = p * (1 - p)
        w += np.linalg.solve(Xb.T @ (Xb * W[:, None]) + 1e-6 * np.eye(len(w)), Xb.T @ (y - p))
    cov = np.linalg.inv(Xb.T @ (Xb * (sigmoid(Xb @ w) * (1 - sigmoid(Xb @ w)))[:, None]))
    return w, np.sqrt(np.diag(cov))
def pred(w, X): return sigmoid(np.c_[np.ones(len(X)), X] @ w)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def decile_lift(y, s):
    top = s >= np.quantile(s, 0.9)
    return y[top].mean() / y.mean()

def make(n, usage_slope, intercept):
    usage = rng.normal(0, 1, n); tenure = rng.normal(0, 1, n)
    p = sigmoid(intercept + usage_slope * usage - 0.3 * tenure)
    return np.c_[usage, tenure], (rng.random(n) < p).astype(float)

# Before price change: churn falls with usage (slope -1.0). After: the same usage no longer protects (slope -0.2), base level higher.
Xa, ya = make(40000, -1.0, -1.5)
Xb, yb = make(40000, -0.2, -1.0)           # input distribution identical, relationship changed
Xt, yt = make(40000, -0.2, -1.0)           # fresh post-change test data

wA, seA = fit(Xa, ya); wB, seB = fit(Xb, yb)
print("coefficient on usage: before", round(wA[1], 2), "+/-", round(1.96 * seA[1], 2), "| after", round(wB[1], 2), "+/-", round(1.96 * seB[1], 2))
assert abs(wA[1] - wB[1]) > 4 * np.hypot(seA[1], seB[1])           # difference far outside noise

# Data-drift check: the input means and sds barely move
print("input mean/sd before:", Xa.mean(0).round(2), Xa.std(0).round(2), "after:", Xb.mean(0).round(2), Xb.std(0).round(2))
assert np.abs(Xa.mean(0) - Xb.mean(0)).max() < 0.03 and np.abs(Xa.std(0) - Xb.std(0)).max() < 0.03

print(f"old model on old-regime test data: AUC {auc(ya, pred(wA, Xa)):.3f}, top-decile lift {decile_lift(ya, pred(wA, Xa)):.2f}")
print(f"old model on new-regime test data: AUC {auc(yt, pred(wA, Xt)):.3f}, top-decile lift {decile_lift(yt, pred(wA, Xt)):.2f}")
print(f"refit on new regime, same test:    AUC {auc(yt, pred(wB, Xt)):.3f}, top-decile lift {decile_lift(yt, pred(wB, Xt)):.2f}")
assert auc(yt, pred(wA, Xt)) < auc(yt, pred(wB, Xt)) - 0.02
assert decile_lift(yt, pred(wA, Xt)) < decile_lift(yt, pred(wB, Xt))

# Training-window trade-off: only 3,000 post-change rows exist; combine with old data plus a regime flag
Xn, yn = Xb[:3000], yb[:3000]
w_small, _ = fit(Xn, yn)
Xmix = np.r_[Xa[:20000], Xn]; flag = np.r_[np.zeros(20000), np.ones(3000)]
Xi = np.c_[Xmix, flag, Xmix[:, 0] * flag]
w_int, _ = fit(Xi, np.r_[ya[:20000], yn])
Xti = np.c_[Xt, np.ones(len(Xt)), Xt[:, 0]]
print(f"3,000 new rows only:               AUC {auc(yt, pred(w_small, Xt)):.3f}")
print(f"old 20,000 + new 3,000 + regime x usage: AUC {auc(yt, pred(w_int, Xti)):.3f}")
assert auc(yt, pred(w_small, Xt)) > auc(yt, pred(wA, Xt))
print("asserts passed")
```

**Output (my run):**
```text
coefficient on usage: before -1.0 +/- 0.03 | after -0.21 +/- 0.02
input mean/sd before: [ 0.01 -0.01] [1. 1.] after: [ 0.01 -0.01] [1. 1.]
old model on old-regime test data: AUC 0.753, top-decile lift 2.55
old model on new-regime test data: AUC 0.574, top-decile lift 1.37
refit on new regime, same test:    AUC 0.604, top-decile lift 1.49
3,000 new rows only:               AUC 0.603
old 20,000 + new 3,000 + regime x usage: AUC 0.603
asserts passed
```

**Follow-ups:**
- Why would the inputs look the same but churn behave differently? Because the price change altered how customers respond to usage, not how much they use.
- How much post-change data is enough? Enough to estimate the changed relationship with a small standard error; in the toy, 3,000 rows were enough, but in real data with many features it takes more. Check by learning curves.
- When would you prefer separate models by regime? When the relationship differs a lot and each regime has enough data; otherwise a shared model with regime interactions borrows strength.

**Common mistakes:**
- Calling it data drift because the PSI is small, or ignoring it because the PSI is small.
- Validating on a random split that mixes regimes.
- Retraining on a window that mostly predates the change.
- Not adding the price or plan feature.
- Waiting for a large sample when a small fresh sample already shows the change.
