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
4. So 0.7 is cheaper by 0.05 per question (2.3%).
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
