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

