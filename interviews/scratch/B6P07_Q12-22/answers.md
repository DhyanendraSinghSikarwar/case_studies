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

