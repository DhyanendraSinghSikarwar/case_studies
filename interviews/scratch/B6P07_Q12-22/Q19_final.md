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

