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

