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

