### Q31 ⭐⭐ 🟡 An ads click model's predicted-to-observed click ratio drifted from 1.00 to 1.12 over a quarter, meaning it over-predicts, while AUC barely moved. Explain why this matters for bidding, what might cause it (traffic mix, auction changes, feedback effects), and how you would recalibrate without retraining everything.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
**Say this first (1 line):** A 12% over-prediction means every bid built on the click probability is about 12% too high, and AUC cannot see it because AUC only checks order; I would find which segments drifted, then fix it with a small calibration layer on top of the model, not a full retrain.

**Clarifying questions:**
- Is the 1.12 an average over all traffic, or is it the same in every slice (placement, device, advertiser, country)? Why: one slice at 1.45 and the rest at 1.00 needs a different fix from a uniform 1.12.
- Is the ratio measured on the same impressions the model scored, with clicks counted the same way (click-fraud filtering, attribution window)? Why: a changed click definition looks exactly like drift.
- How does the bid use the probability: bid = value per click x pCTR, in a first-price or second-price auction, with pacing or a budget? Why: it decides how much money the 12% costs.
- Did anything change in the auction (reserve prices, new formats, new inventory, a competitor)? Why: it points to traffic mix or auction effects instead of model decay.
- When was the model last retrained, and is a calibration layer already in the serving path? Why: it tells me whether a patch is quick or needs new plumbing.

**Approach:**
1. Confirm it is real: recompute predicted/observed on matured clicks, check the click definition and logging, and look at it by day to see slow slide versus step.
2. Say why it matters: bid = value x pCTR, so a 12% too-high pCTR is a 12% too-high bid. In a first-price auction you pay it. In a second-price auction you mostly pay the rival's price, but you win extra impressions that are worth less than the price. Pacing and ROI reporting also go wrong.
3. Slice by placement, device, advertiser, country, format and score bucket. A reliability table (predicted bucket versus observed rate) shows whether the error is uniform or sits in the tail.
4. Find causes. Traffic mix: more of a segment where the model was always high. Auction change: new placements or position effects the training data never saw. Feedback effects: the model's own wins shape which impressions it sees (it only learns from impressions it bought). Click-definition or logging change.
5. Fix without full retrain. Fit a calibration layer on the log-odds of the old score using a recent matured window: an intercept first, then a slope, then per-segment or isotonic only if slices disagree and there is enough data. Ranking stays untouched (monotone), so AUC and the downstream ordering do not move.
6. Validate on a later holdout (ratio, reliability table, spend, ROI), ship behind a canary, and alert on the ratio per slice.
7. Plan the real fix: retrain on recent data with the missing features, keep the calibration layer as the quick lever for the next drift.

**Metrics:**
- Calibration ratio = sum of predicted click probabilities / number of observed clicks, over a matured window (numerator and denominator on the same impressions).
- Reliability table: for each predicted-probability bucket, mean predicted versus observed click rate. Also log loss and Brier score.
- Business guardrails: spend, cost per click, ROI (value / spend) per campaign, win rate, pacing error.
- AUC stays as the ranking check; it is not the calibration check.

**Risks:**
- Fitting the fix on too little data: with a 2% click rate, 2,000 clicks give a ratio standard error of about 2%.
- One global factor can make a mixed problem worse (see the Code block: 1.00 and 1.45 segments end up at 0.89 and 1.29).
- Feedback loop: a recalibrated model changes which impressions are won, so the calibration data shifts again.
- Fixing the symptom and never asking why a segment drifted.
- Label delay: very recent clicks are incomplete, so the ratio looks too high just from immature data.

**What the interviewer scores:**
- Strong: states that AUC measures ranking and calibration measures level, and ties 1.12 to money (bid, win rate, ROI).
- Strong: slices before fixing, and says a single factor is only right if the error is uniform.
- Strong: proposes a cheap post-hoc recalibration on a matured window plus a validation and canary, and a retrain as the later step.
- Weak: "retrain the model" as the first and only answer, or "AUC is fine so there is no problem".
- Cross-reference: Book 1 Part 3 has "What is model calibration and why can a model with great AUC still be badly calibrated?" and Book 1 Part 7 has "Does a ranker's predicted probability need to be calibrated? When does it matter (ads, blending scores, thresholds) and how do you fix it?".

**Example:** (illustrative numbers) 1,000 impressions with predicted CTR 2.0% each give 20 expected clicks; you observe 17.9, so the ratio is 20 / 17.9 = 1.12. You value a click at Rs 10 and bid pCTR x Rs 10, so you bid Rs 0.20 where the true value is about Rs 0.18. Weak answer: "AUC is the same, so the model is fine." Strong answer: "AUC checks order, not level. The bid is 12% high, so I would slice the ratio, fit an intercept on matured clicks, canary it, and keep the retrain for later."

**Code:**
```python
# Q31: ads click model over-predicts (ratio 1.12) while AUC is unchanged (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(31)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
logit = lambda p: np.log(p / (1 - p))
sig = lambda z: 1 / (1 + np.exp(-z))

N = 1_200_000
p_true = np.clip(rng.lognormal(np.log(0.02), 0.8, N), 1e-4, 0.5)   # true CTR per impression
y = (rng.random(N) < p_true).astype(int)

# Drift = a constant shift in the log-odds. Find the shift that gives predicted/observed = 1.12.
lo, hi = 0.0, 0.5
for _ in range(60):
    mid = (lo + hi) / 2
    if sig(logit(p_true) + mid).mean() / y.mean() < 1.12: lo = mid
    else: hi = mid
shift = (lo + hi) / 2
p_pred = sig(logit(p_true) + shift)
ratio = p_pred.mean() / y.mean()
print(f"shift in log-odds: {shift:.3f}   predicted/observed: {ratio:.3f}")
assert abs(ratio - 1.12) < 0.01          # observed clicks are random, so allow 0.01

# AUC does not see a monotone shift at all
a0, a1 = auc(y, p_true), auc(y, p_pred)
print(f"AUC before drift {a0:.4f}   after drift {a1:.4f}")
assert abs(a0 - a1) < 1e-12

# Why bidding cares: bid = value_per_click * pCTR. Real value of an impression = value * true CTR.
v = 10.0                                   # Rs per click (illustrative)
rival = rng.lognormal(np.log(v * 0.02), 0.8, N)   # rival bids
rival_fp = rival * 0.6                              # rivals shade too
def second_price(p_used):                  # winner pays the rival bid
    win = v * p_used > rival
    return (v * p_true[win] - rival[win]).sum(), win.sum()
def first_price(p_used):                   # winner pays its own bid
    bid = 0.6 * v * p_used; win = bid > rival_fp   # shade the bid to 60% of value
    return (v * p_true[win] - bid[win]).sum(), win.sum(), bid[win].sum()
sp_ok, w_ok = second_price(p_true); sp_bad, w_bad = second_price(p_pred)
fp_ok, _, spend_ok = first_price(p_true); fp_bad, _, spend_bad = first_price(p_pred)
print(f"second price: won {w_ok} -> {w_bad}; profit Rs {sp_ok:,.0f} -> {sp_bad:,.0f}")
print(f"first price : profit Rs {fp_ok:,.0f} -> {fp_bad:,.0f}; spend Rs {spend_ok:,.0f} -> {spend_bad:,.0f}")
assert w_bad > w_ok and sp_bad < sp_ok     # extra wins are the unprofitable ones
assert fp_bad < 0.9 * fp_ok and 0.8 < sp_bad / sp_ok < 1 and spend_bad > 1.12 * spend_ok   # you pay your own inflated bid

# Recalibrate WITHOUT retraining: fit one intercept on the log-odds of the old score
# using a recent window (first 800k impressions), then test on the rest.
fit, test = slice(0, 800_000), slice(800_000, N)
z = logit(p_pred[fit]); b = 0.0
for _ in range(25):                         # Newton steps on the intercept only
    q = sig(z + b)
    b -= (q - y[fit]).sum() / (q * (1 - q)).sum()
p_fix = sig(logit(p_pred) + b)
r_fix = p_fix[test].mean() / y[test].mean()
print(f"fitted offset {b:.3f}   ratio on holdout after fix {r_fix:.3f}")
assert abs(b + shift) < 0.06 and abs(r_fix - 1) < 0.03
assert abs(auc(y, p_fix) - a1) < 1e-12      # ranking is untouched
fp_fix, _, _ = first_price(p_fix)
print(f"first-price profit after fix (Rs): {fp_fix:,.0f}")
assert fp_fix > fp_bad

# Segment trap: overall 1.12 can hide one bad segment, and one global factor then mis-fixes both.
share = np.array([0.65, 0.35]); seg_ratio = np.array([1.00, 1.45])
pred = np.array([0.020, 0.020]); obs = pred / seg_ratio
overall = (share * pred).sum() / (share * obs).sum()
print(f"overall ratio {overall:.3f}; segment ratios {seg_ratio}")
assert abs(overall - 1.12) < 0.005
after_global = seg_ratio / overall          # divide every prediction by the overall ratio
print("after one global factor, segment ratios:", np.round(after_global, 3))
assert after_global[0] < 0.9 and after_global[1] > 1.25
```

**Output (my run):**
```text
shift in log-odds: 0.128   predicted/observed: 1.120
AUC before drift 0.7197   after drift 0.7197
second price: won 599633 -> 652488; profit Rs 141,722 -> 140,959
first price : profit Rs 94,429 -> 80,257; spend Rs 141,644 -> 167,743
fitted offset -0.118   ratio on holdout after fix 1.007
first-price profit after fix (Rs): 93,405
overall ratio 1.122; segment ratios [1.   1.45]
after one global factor, segment ratios: [0.891 1.293]
```
The text above matches this run: the 12% drift moves AUC by nothing (0.7197 both), the second-price loss is small (about 0.5%, the extra wins are near break-even), the first-price loss is large (profit down about 15%, spend up about 18%), and one fitted intercept brings the holdout ratio to 1.007.

**Follow-ups:**
- Why not just retrain? It can take days, needs fresh labels, and the same drift can come back; a calibration layer is a fast, reversible patch, and you still retrain to fix the root cause.
- Intercept, Platt (intercept plus slope) or isotonic? Intercept if the error is a uniform level shift; Platt if the error grows with the score; isotonic if the shape is irregular and you have a lot of data.
- What if the ratio is 1.00 overall but wrong by segment? Then bids are mis-priced across segments even though the total looks right; calibrate per segment or add the segment feature.

**Common mistakes:** Saying AUC fine means model fine. Dividing every prediction by 1.12 without slicing. Fitting on immature clicks. Ignoring the auction type. Forgetting the feedback loop.

### Q32 ⭐⭐ 🟡 A support-ticket triage LLM is checked weekly by humans on 400 random tickets, and accuracy went from 91% (364 of 400) to 86% (344 of 400) after a product launch. Explain whether that sample size supports calling it a real decline, what you would segment by, and how you would decide what to do next.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** Five points on 400 tickets is borderline evidence (p about 0.03, and the 95% interval runs from under 1 point to about 9 points), so I would not call it a decline yet; I would split it by ticket type and by what the launch changed, and decide from that.

**Clarifying questions:**
- Are the 400 tickets a fresh random sample each week, labelled blind by the same reviewers with the same rubric? Why: a changed reviewer or rubric moves accuracy with no change in the model.
- What did the launch change: new ticket types, new languages, a new form, a new model or prompt? Why: it separates a coverage gap from real decay.
- What does "accuracy" mean here (exact category match, priority, routing)? Why: different errors cost different amounts.
- What are the costs: a mis-routed urgent ticket versus a mis-tagged low-priority one? Why: they decide how much evidence I need before acting.
- How many weekly checks have we looked at so far? Why: the more weeks you watch, the more false alarms you will see.

**Approach:**
1. Do the arithmetic. 364/400 = 91.0% and 344/400 = 86.0%. Pooled rate 0.885, standard error 0.0226, z = 2.22, two-sided p = 0.027. The interval for the drop is about 0.6 to 9.4 points. So: probably lower, but the size is very uncertain.
2. Say what the sample can and cannot do. To catch a 5-point drop with 80% power you need about 635 tickets a week, so 400 is slightly underpowered. And with weekly checks, about 1 week in 19 shows a "significant" drop by luck alone.
3. Do not stop at the p-value. The launch is not randomised, so ask what else changed: ticket mix, language, channel, reviewers.
4. Segment: by ticket type (especially new types), language, channel, customer tier, ticket length, model or prompt version, and reviewer. Compare accuracy inside each segment before and after. Report the mix effect and the within-segment effect separately.
5. Get more labels where they matter: stratify the next sample by the suspicious segments (oversample the new types), and add a second reviewer on a subset to measure labelling agreement.
6. Decide by cost, not by p-value: if the drop sits in one new ticket type, add examples and routing rules for it; if it is broad, check the model, prompt and retrieval versions; if urgent tickets are hit, fall back to a human queue for them now.

**Metrics:**
- Accuracy = correct triage decisions / tickets reviewed, per week and per segment, with a Wilson or normal interval.
- Difference = this week minus baseline, with a 95% interval; the baseline should be several weeks, not one.
- Mix decomposition: change = sum over segments of (share x change in accuracy) + sum of (change in share x accuracy). Both parts are reported.
- Guardrails: mis-routed urgent tickets per 1,000, time to first response, reviewer agreement rate.

**Risks:**
- Calling noise a decline, or calling a real decline noise because p is above 0.05.
- Simpson-type mix: the model is the same on old tickets but the launch added a hard new type (see Code).
- Reviewer drift or a rubric change.
- A sample that is not random: easy tickets are labelled faster.
- Looking at many segments and finding one that is "significant" by chance.

**What the interviewer scores:**
- Strong: does the arithmetic out loud (z, p, interval, power) and says what it means in words.
- Strong: separates statistics from causality: the launch is not an experiment, so segment and find the mechanism.
- Strong: links the decision to costs and offers a cheap next step (more labels in the suspect segment).
- Weak: "400 is too small" with no calculation, or "p < 0.05 so it dropped" with no cause.
- Cross-reference: Book 6 Part 1 has "A daily metric is down 2% and an alert fired. The metric usually moves 1.5% day to day, with a weekend dip..." as the same noise-versus-signal question for a product metric (Q37 in Part 1).

**Example:** (illustrative numbers) Before the launch: 400 old-type tickets, 364 right (91%). After: 300 old-type tickets, 276 right (92%), and 100 tickets of a new type the launch created, 68 right (68%). Total 344 of 400 = 86%. The old types did not get worse (they went up one point). The new type is 25% of the sample at 68%, which costs 0.25 x (0.68 - 0.91) = 5.75 points, and the old types add back 0.75 x 0.01 = 0.75 points; net -5 points. Weak answer: "The model degraded 5 points, retrain it." Strong answer: "The drop is borderline by itself, but split by type it is all one new ticket category. I would add labelled examples and a rule for that category and keep watching the old types."

**Code:**
```python
# Q32: is 91% -> 86% on 400 tickets a real decline? (numbers from the prompt, rest illustrative)
import math
import numpy as np

def phi_upper(z): return 0.5 * math.erfc(z / math.sqrt(2))     # P(Z > z)

a_ok, b_ok, n = 364, 344, 400
pa, pb = a_ok / n, b_ok / n
assert (pa, pb) == (0.91, 0.86)
pool = (a_ok + b_ok) / (2 * n)
se_pool = math.sqrt(pool * (1 - pool) * (2 / n))
z = (pa - pb) / se_pool
p_two = 2 * phi_upper(z)
se_diff = math.sqrt(pa * (1 - pa) / n + pb * (1 - pb) / n)
lo, hi = (pa - pb) - 1.96 * se_diff, (pa - pb) + 1.96 * se_diff
print(f"drop {pa - pb:.3f}  z {z:.2f}  two-sided p {p_two:.4f}  95% CI for the drop [{lo:.3f}, {hi:.3f}]")
assert round(z, 2) == 2.22 and 0.02 < p_two < 0.035 and 0.004 < lo < 0.008 and 0.09 < hi < 0.10

# Power: tickets per week needed to detect a 5-point drop from 91% (80% power, 5% two-sided)
za, zb = 1.96, 0.8416
need = (za + zb) ** 2 * (pa * (1 - pa) + pb * (1 - pb)) / (pa - pb) ** 2
print(f"tickets per week for 80% power at a 5-point drop: {need:.0f}")
assert 600 < need < 700

# Weekly checking: if the true accuracy never changes (89%), how often does a week
# look 'significantly lower' than the previous week at the 5% one-sided level?
rng = np.random.default_rng(32)
weeks = 20_000
x = rng.binomial(n, 0.89, size=weeks + 1)
p = x / n
z_w = (p[:-1] - p[1:]) / np.sqrt(2 * 0.89 * 0.11 / n)
false_alarm = (z_w > 1.645).mean()
print(f"false 'decline' weeks when nothing changed: {false_alarm:.3f}  (about 1 in {1 / false_alarm:.0f} weeks)")
assert 0.03 < false_alarm < 0.07

# Mix effect: launch added a new ticket type the model never saw. Same model, same skill on old types.
before = {"old types": (400, 364)}                    # (tickets, correct)
after = {"old types": (300, 276), "new type": (100, 68)}
acc = lambda d: sum(c for _, c in d.values()) / sum(t for t, _ in d.values())
print(f"before {acc(before):.2%}  after {acc(after):.2%}")
print(f"old types: {364 / 400:.1%} -> {276 / 300:.1%}   new type: {68 / 100:.0%}   new-type share {100 / 400:.0%}")
assert acc(before) == 0.91 and acc(after) == 0.86
assert 276 / 300 == 0.92 and 68 / 100 == 0.68
# exact decomposition of the 5-point drop (reference = old accuracy 91%)
new_part = 0.25 * (0.68 - 0.91)      # new ticket type
old_part = 0.75 * (0.92 - 0.91)      # old ticket types
print(f"new type {new_part:+.4f}  old types {old_part:+.4f}  total {new_part + old_part:+.4f}")
assert abs(new_part + old_part - (0.86 - 0.91)) < 1e-12
assert abs(new_part) > 5 * abs(old_part)
```

**Output (my run):**
```text
drop 0.050  z 2.22  two-sided p 0.0267  95% CI for the drop [0.006, 0.094]
tickets per week for 80% power at a 5-point drop: 635
false 'decline' weeks when nothing changed: 0.052  (about 1 in 19 weeks)
before 91.00%  after 86.00%
old types: 91.0% -> 92.0%   new type: 68%   new-type share 25%
new type -0.0575  old types +0.0075  total -0.0500
```

**Follow-ups:**
- Would you act at p = 0.027? Not on the p-value. If the new segment is a real coverage gap, act now with a cheap, reversible step; if no cause is found, collect another week of stratified labels before a costly change.
- How do you cut the false alarms from weekly checks? Use a baseline of several weeks, a control chart or a sequential test, and require the drop to hold for two weeks or to show in a named segment.
- What if reviewers disagree 8% of the time? Then accuracy against one reviewer is noisy by itself; measure agreement, use two reviewers on a subset, and treat accuracy changes smaller than the disagreement with care.

**Common mistakes:** Calling it a decline or noise from the headline numbers alone. Ignoring that the launch changed the ticket mix. Forgetting that repeated weekly checks produce false alarms. Using one baseline week. Skipping the cost of each error type.

### Q33 ⭐⭐ 🟡 A vision model that reads documents from phone photos has lost accuracy since a popular new phone with a different camera pipeline became common among your users. Explain how you would find this from the data, estimate its size, decide between augmentation, targeted data collection and a threshold change, and monitor for the next device shift.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** I would tag every upload with its device model, show that accuracy fell only where the new phone is common, size the gap on a small human-labelled audit, and then pick the cheapest fix that holds: a threshold change now, targeted data and augmentation next.

**Clarifying questions:**
- Do we log the device model (EXIF or user agent) and image properties (resolution, blur, HDR or night mode, compression) with each upload? Why: without it the cause is a guess.
- Do we have labels for current uploads (human review, downstream corrections, user edits)? Why: accuracy by device needs ground truth, even a small audit.
- What is the cost of an error versus a manual review? Why: it decides between a higher threshold and more training data.
- How fast can we collect and label new-phone images and ship a retrain? Why: if it takes weeks, a threshold change is the stopgap.
- Is the model's confidence calibrated and logged? Why: a threshold change only works if the score separates good from bad reads.

**Approach:**
1. Find it from data. Slice accuracy (or a proxy such as confidence, field-level agreement, user corrections) by device model and week. A rising device share with a falling overall number, while old devices stay flat, is the signature (see Code).
2. Look for the mechanism: compare image statistics between phones (resolution, sharpness, noise, colour, aggressive smoothing, HDR, a new default format such as HEIC). Look at failure examples by hand.
3. Size it: audit a few hundred labelled uploads per group, take the accuracy gap with a bootstrap interval, then overall loss = share of new phone x gap. This also says what happens as the share grows.
4. Choose the fix:
   - Threshold change (stopgap, hours): raise the confidence threshold for this device so fewer bad reads auto-process; cost is more manual review (the Code run shows the trade).
   - Augmentation (days): simulate the new pipeline's look (sharpening, denoise, colour curve, compression) on existing images; cheap but only as good as the simulation.
   - Targeted data collection (weeks): get real images from the new phone, label them, and fine-tune; best accuracy, slowest. Use it when the gap is large and the device share is growing.
5. Check the fix on a held-out set from the new phone and on the old phones (no regression), then canary.
6. Monitor for the next shift: device-model share (alert when a new model passes a small share such as 5%), per-device confidence distribution, image-quality statistics, and a rolling labelled audit sample per device group.

**Metrics:**
- Accuracy by device group = correct reads / audited uploads in the group, with an interval.
- Overall loss = (share of the group) x (accuracy of old minus accuracy of group).
- Automation rate = uploads auto-processed / all uploads; accuracy of the auto-processed set; manual-review rate.
- Drift signals: device share, PSI or distance on confidence and image statistics per device.
- Guardrails: old-device accuracy (no regression), review queue time, cost per document.

**Risks:**
- Confounding: users with the new phone may differ (documents, lighting, app version), not only the camera.
- An audit with too few labels (300 per group gives a gap interval about plus or minus 5 points wide on each side, see Code).
- Augmentation that does not look like the real pipeline can raise training metrics and change nothing in production.
- Raising the threshold quietly overloads the manual queue.
- Over-fitting to one phone and missing the next.

**What the interviewer scores:**
- Strong: starts from the data (device tag, slice, share versus accuracy) and proves it is the device.
- Strong: gives the size as share x gap and says it will grow with adoption.
- Strong: ranks the fixes by speed and durability and states the cost of each.
- Weak: "retrain with more data" with no diagnosis, or no plan for the next device.
- Cross-reference: Book 4 Part 8 has "Monitoring models on unstructured data (images, text, embeddings) at the Part 8 level" for the monitoring side.

**Example:** (illustrative numbers) 5,000 uploads a week. Old phones read correctly 95% of the time; the new phone 80%. At a 30% share, overall accuracy = 0.70 x 0.95 + 0.30 x 0.80 = 90.5%, versus about 95% with no new phone, a 4.5-point loss. At a 2% share the loss is only 0.3 points, which is why nobody noticed. Weak answer: "Accuracy is down, retrain on recent data." Strong answer: "Overall dropped because the new phone share grew; old phones are flat. It is a 15-point gap on 30% of traffic. Today I raise the threshold for that device, this week I add augmentation, and I collect labelled images from the phone for the real fix."

**Code:**
```python
# Q33: document-reading model loses accuracy after a new phone becomes popular (illustrative simulation)
import numpy as np

rng = np.random.default_rng(33)
weeks = 12
share_new = np.linspace(0.02, 0.30, weeks)      # share of uploads from the new phone
per_week = 5000                                    # uploads per week
acc_old, acc_new = 0.95, 0.80                   # true accuracy by device group

# 1. Overall accuracy slides while old-phone accuracy is flat
n_new = rng.binomial(per_week, share_new)
ok_new = rng.binomial(n_new, acc_new)
ok_old = rng.binomial(per_week - n_new, acc_old)
overall = (ok_new + ok_old) / per_week
old_only = ok_old / (per_week - n_new)
print("week  new-phone share  overall  old phones")
for w in (0, 5, 11):
    print(f"{w:>4}  {share_new[w]:>14.0%}  {overall[w]:>7.1%}  {old_only[w]:>10.1%}")
assert overall[0] - overall[-1] > 0.03 and abs(old_only[0] - old_only[-1]) < 0.01

# 2. Size of the problem: audit 300 labelled uploads from each group (human-checked)
a_new = rng.binomial(1, acc_new, 300); a_old = rng.binomial(1, acc_old, 300)
boot = []
for _ in range(2000):
    boot.append(rng.choice(a_old, 300).mean() - rng.choice(a_new, 300).mean())
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"audit gap old-new {a_old.mean() - a_new.mean():.3f}, bootstrap 95% [{lo:.3f}, {hi:.3f}]")
assert 0.08 < lo and hi < 0.22
# expected loss at 30% share if nothing is done: 0.30 x gap
loss = 0.30 * (acc_old - acc_new)
print(f"overall accuracy loss at 30% share: {loss:.3f}")
assert abs(loss - 0.045) < 1e-9

# 3. Threshold change versus other fixes: confidence scores differ by device
conf_old_ok = rng.beta(8, 1.2, 20000); conf_old_bad = rng.beta(3, 3, 1000)
conf_new_ok = rng.beta(5, 1.5, 16000); conf_new_bad = rng.beta(3, 3, 4000)
def at(th, ok, bad):
    kept_ok = (ok >= th).sum(); kept_bad = (bad >= th).sum()
    auto = kept_ok + kept_bad
    return auto / (len(ok) + len(bad)), kept_ok / auto
print("new-phone uploads: threshold -> share auto-processed, accuracy of auto-processed")
for th in (0.50, 0.70, 0.85):
    share, acc = at(th, conf_new_ok, conf_new_bad)
    print(f"  {th:.2f}  {share:.1%}  {acc:.1%}")
s50, a50 = at(0.50, conf_new_ok, conf_new_bad); s85, a85 = at(0.85, conf_new_ok, conf_new_bad)
assert a85 > a50 and s85 < s50             # a higher threshold buys accuracy with more manual review
print(f"going 0.50 -> 0.85 sends {s50 - s85:.1%} more of new-phone uploads to manual review")

# 4. Monitoring: alert when a new device model passes 5% of traffic or its audited accuracy is low
first_alert = int(np.argmax(share_new > 0.05))
print(f"week the new phone crosses 5% share: {first_alert}  (share {share_new[first_alert]:.1%})")
assert share_new[first_alert] > 0.05 and share_new[first_alert - 1] <= 0.05
```

**Output (my run):**
```text
week  new-phone share  overall  old phones
   0              2%    94.7%       95.2%
   5             15%    92.3%       94.5%
  11             30%    90.2%       95.2%
audit gap old-new 0.137, bootstrap 95% [0.090, 0.190]
overall accuracy loss at 30% share: 0.045
new-phone uploads: threshold -> share auto-processed, accuracy of auto-processed
  0.50  85.1%  88.1%
  0.70  60.2%  94.3%
  0.85  29.7%  98.1%
going 0.50 -> 0.85 sends 55.5% more of new-phone uploads to manual review
week the new phone crosses 5% share: 2  (share 7.1%)
```
The run shows overall accuracy sliding from about 94.7% to 90.2% while old phones stay near 95%, an audit gap near 13.7 points (interval 9 to 19), and a threshold move from 0.50 to 0.85 sending about 55% more new-phone uploads to manual review in this simulation.

**Follow-ups:**
- The device tag is not logged. What now? Use proxies (image resolution, EXIF if kept, user-agent, app version), cluster images on simple statistics, and add the tag to the logs from today.
- Why not only augment? It only works if the simulation matches the real pipeline; always verify on real labelled images from the phone.
- How do you stop this recurring? A device-share alert, a per-device audit sample, and a standing process to collect labelled images when a new model passes a small share.

**Common mistakes:** Treating the overall average as the problem. Retraining on a random recent sample that has few new-phone images. Raising the threshold without costing the manual queue. Checking only the new device and missing regressions on old ones. No device-level monitoring afterwards.

### Q34 ⭐⭐ 🟡 A summarisation feature's human rating slipped from 4.3 to 3.9 out of 5 after a developer edited the shared prompt template to fix one customer complaint, and neither the prompt nor the model version was recorded with each output. Explain how you would find out what changed, what a frozen regression set and prompt versioning would have shown, and how to ship prompt edits safely.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** I would date the drop from rating timestamps, match it against the deploy and git history of the template, rebuild the old prompt and compare old versus new on a fixed set of inputs, and from now on version every prompt and gate every edit on a frozen regression set.

**Clarifying questions:**
- How are ratings collected (human raters, users, an LLM judge), and did the rubric or raters change? Why: a rating change is not always a quality change.
- Is the template in version control, and do we have deploy timestamps and old copies (git history, config store, cached copies)? Why: it decides whether I can rebuild the old prompt exactly.
- Is the template shared by several features or customers? Why: one customer's fix can hurt the others, which is probably what happened.
- Did the base model, retrieval or input mix change in the same weeks? Why: the prompt edit is the prime suspect, not the only one.
- Do we keep inputs and outputs (with consent) so I can replay them? Why: replay is the cleanest test.

**Approach:**
1. Check the number: 4.3 to 3.9 is a 0.4-point drop (9.3% of 4.3). With a 0.9 standard deviation per rating you need about 80 ratings per group to see it, so it is detectable on normal volumes. Confirm raters and rubric are unchanged.
2. Date it. With no version logged, find the change day from the daily mean ratings with a simple two-level fit (the Code run recovers the true day). Then match the date with deploy logs, git history of the template and the model provider's release notes.
3. Rebuild both prompts (old from history, new from the repo) and replay the same fixed inputs through both with the same model and settings. Judge both with the same raters or judge. Compare paired: same input, two prompts.
4. Break the change down: by input category, length and customer. A fix for one complaint usually helps one category and hurts the others.
5. Decide: keep the edit only for the segment that needs it (a separate template or a conditional section), or revert and fix the complaint another way.
6. What a frozen regression set and versioning would have shown: the paired drop (about -0.4 with an interval below zero), plus the category that improved (the complaint) and the four that got worse, before the edit ever shipped.
7. Ship prompt edits safely: prompts in version control; a version id and model id logged with every output; a frozen regression set (150 to 300 fixed inputs across categories, including every past complaint); a gate (mean must not drop and no category may fall more than a set amount); then a canary or A/B on a share of traffic, with a one-click rollback.

**Metrics:**
- Mean rating = sum of ratings / number of rated outputs, per day, per category, per prompt version.
- Paired change = mean over regression items of (new score minus old score), with a bootstrap interval.
- Category worst-case change = the lowest category mean change (gate on it, not just the average).
- Guardrails: length, refusal rate, format-valid rate, latency and cost per output.

**Risks:**
- Judge or rater drift looks like a prompt effect; use the same judge on both prompts and a fixed rubric.
- The regression set must be frozen and must cover the long tail; if it never includes the complaint type it cannot catch it.
- Overfitting the prompt to the regression set.
- A model-provider update at the same time hides which change caused the drop.
- Replay with different temperature or model settings.

**What the interviewer scores:**
- Strong: treats the prompt like code (version, test, gate, canary, rollback) and logs prompt and model version per output.
- Strong: uses paired comparison on fixed inputs and breaks the result down by category.
- Strong: dates the change from the data when versions are missing, and treats the date as a lead.
- Weak: "ask the developer to revert" with no measurement, or "we need more data".
- Cross-reference: Book 4 Part 8 has "LLM and GenAI monitoring, only at the boundary with Book 2" for the monitoring side.

**Example:** (illustrative numbers) Frozen set: 150 inputs, 30 each in five categories. The edit lifts the complaint-type category by 0.4 and lowers the others by 0.46, 0.91, 0.51 and 0.60 points in this simulation. Average change: -0.41, interval about -0.51 to -0.32. The gate (no category below -0.3) fails, so the edit would not ship as written. Weak answer: "Ratings dropped, revert the prompt." Strong answer: "Date the drop, replay old versus new on a fixed set, show it helps one category and hurts four, then ship a category-specific fix through the gate."

**Code:**
```python
# Q34: summary rating slipped 4.3 -> 3.9 after an unversioned prompt edit (illustrative simulation)
import numpy as np

rng = np.random.default_rng(34)
assert round(4.3 - 3.9, 1) == 0.4 and round((4.3 - 3.9) / 4.3, 3) == 0.093

# 1. No version was logged: find WHEN it changed from daily mean ratings (60 days, 40 rated per day)
days, per_day, change_day = 60, 40, 33
daily_mean = []
for d in range(days):
    mu = 4.3 if d < change_day else 3.9
    r = np.clip(np.round(rng.normal(mu, 0.9, per_day)), 1, 5)
    daily_mean.append(r.mean())
daily_mean = np.array(daily_mean)
def sse(k):  # two-level fit with a break before day k
    return ((daily_mean[:k] - daily_mean[:k].mean()) ** 2).sum() + ((daily_mean[k:] - daily_mean[k:].mean()) ** 2).sum()
best = min(range(5, days - 5), key=sse)
print(f"estimated change day {best} (true {change_day});  mean before {daily_mean[:best].mean():.2f}  after {daily_mean[best:].mean():.2f}")
assert abs(best - change_day) <= 2
# the date is only a lead: match it against deploy logs / git history of the template

# 2. Frozen regression set: 150 fixed inputs in 5 categories, same judge, old vs new prompt (paired)
cats = ["complaint-type", "short", "long", "technical", "legal"]
cat_of = np.repeat(np.arange(5), 30)
base = rng.normal(4.3, 0.5, 150)                    # item difficulty carried across prompts
effect = np.array([+0.6, -0.5, -0.9, -0.7, -0.6])   # the edit helps one case, hurts four
old = np.clip(base + rng.normal(0, 0.3, 150), 1, 5)
new = np.clip(base + effect[cat_of] + rng.normal(0, 0.3, 150), 1, 5)
diff = new - old
boot = [rng.choice(diff, 150).mean() for _ in range(4000)]
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"paired mean change {diff.mean():+.2f}  95% bootstrap [{lo:+.2f}, {hi:+.2f}]")
for c in range(5):
    print(f"  {cats[c]:15} {diff[cat_of == c].mean():+.2f}")
assert hi < 0 and diff[cat_of == 0].mean() > 0 and diff[cat_of == 2].mean() < -0.5
# average of the effects: (0.6 - 0.5 - 0.9 - 0.7 - 0.6) / 5
assert abs(effect.mean() - (-0.42)) < 1e-9

# 3. Why a frozen set beats waiting for live ratings: sample sizes for a 0.4 shift
sd = 0.9
n_live = 2 * (1.96 + 0.8416) ** 2 * sd ** 2 / 0.4 ** 2    # independent groups
sd_diff = diff.std(ddof=1)                                 # paired: only the prompt effect + noise
n_paired = (1.96 + 0.8416) ** 2 * sd_diff ** 2 / 0.4 ** 2
print(f"ratings needed for 80% power at a 0.4 shift: unpaired {n_live:.0f} per group, paired {n_paired:.0f} items")
assert n_live > 4 * n_paired

# 4. Ship gate: block a prompt version if any category drops more than 0.3 or the mean drops at all
def gate(d, cat, tol=0.3):
    worst = min(d[cat == c].mean() for c in range(5))
    return bool(d.mean() >= 0 and worst >= -tol)
print("gate passes for the edited prompt:", gate(diff, cat_of))
assert gate(diff, cat_of) is False and gate(np.zeros(150), cat_of) is True
```

**Output (my run):**
```text
estimated change day 33 (true 33);  mean before 4.20  after 3.83
paired mean change -0.41  95% bootstrap [-0.51, -0.32]
  complaint-type  +0.40
  short           -0.46
  long            -0.91
  technical       -0.51
  legal           -0.60
ratings needed for 80% power at a 0.4 shift: unpaired 79 per group, paired 17 items
gate passes for the edited prompt: False
```
In this run the break day is recovered exactly (33), the paired change is about -0.41 with an interval below zero, one category rose and four fell, and the paired design needs about 17 items to see a 0.4 shift where unpaired live ratings need about 79 per group.

**Follow-ups:**
- Nothing in history, the old prompt is lost. Reconstruct it from cached requests, logs or the last good outputs; if truly gone, write a candidate and judge it against old outputs for the same inputs.
- Is an LLM judge enough? As a gate yes if you calibrate it against human ratings on a sample and watch for judge drift; keep a small human check.
- How do you stop edits for one customer hurting others? Per-customer or per-category template sections, plus the gate across all categories.

**Common mistakes:** No version logged with the output. Comparing different inputs instead of paired replay. Looking at the average only and missing the category that rose. Treating a prompt as a config tweak. Gating on a set that does not contain the complaint types.

### Q35 ⭐⭐ 🔴 A model scored an AUC of 0.95 offline, but live AUC is 0.71. A review finds one feature was only populated after the outcome happened, so it leaked at training time but is empty at serving time. Explain how you would confirm leakage, quantify the damage, rebuild the evaluation to be point-in-time correct, and handle the live system while you fix it.
**Asked at:** Training-serving skew and offline-versus-online question pages (DesignGurus 'Grokking the AI System Design Interview', techinterview.org MLOps drift and feature-store guide, a Prachub ML-serving concept page); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** An offline AUC of 0.95 that becomes 0.71 live, with one feature that only exists after the outcome, is classic target leakage; I would prove it with timestamps and an ablation, report the honest number (about the clean-model AUC), rebuild the evaluation with point-in-time joins, and switch the live system to a clean model or a rule fallback now.

**Clarifying questions:**
- Which feature is it, and which system writes it and when? Why: the write time is the proof, and it tells me what the legitimate version of the feature would be.
- What is the prediction moment (application time, transaction time, request time)? Why: every feature must be known at that moment, and nothing else counts.
- What decisions use the score today, and at what threshold? Why: an empty feature shifts every score, so the thresholds are now wrong.
- Is there a previous model or a rule set we can fall back to, and how long does a clean retrain take? Why: it decides the interim plan.
- Which other models or features share the same source table or join? Why: leakage tends to repeat through the same pipeline.

**Approach:**
1. Confirm leakage with three checks: (a) timestamps: for each row compare the feature's write time with the prediction time (in the Code run 98% of rows are written after); (b) single-feature strength: a feature that alone has AUC 0.95 for a hard problem is suspect; (c) ablation: drop it and retrain; offline AUC falls to the live level.
2. Quantify the damage. The honest performance is the clean-model AUC (0.705 in the run), not 0.95. Also compute what the live system did wrong: with the feature empty, the old model's scores collapse (mean predicted risk 0.027 versus a true rate 0.286 here), so at the old threshold almost nothing is flagged.
3. Rebuild evaluation, point-in-time correct: join features by "latest value at or before the prediction time" (an as-of join), not "latest value ever"; split by time, not at random; run a leakage test in the pipeline (feature timestamp must not be after the prediction time).
4. Handle the live system. Immediately: roll back to the last model that did not use the feature or to a rule-based fallback; or retrain without the feature and ship it behind a shadow run; recalibrate thresholds on live outcomes because the score distribution changed. Tell the business the true number and the period of exposure.
5. Fix the cause: block the post-outcome source from the feature store for training, add the leakage check to CI, and review sibling models for the same pattern.
6. Look for a legitimate substitute: a version of the signal that exists at prediction time (for example a previous-case value, or an earlier-stage field).

**Metrics:**
- Leak rate = rows where feature write time is after prediction time / all rows.
- Single-feature AUC and the offline AUC drop when the feature is removed.
- Honest AUC = AUC of a point-in-time model on a time-based holdout, and AUC on live matured labels.
- Operational: flag rate, precision and recall at the live threshold, mean score versus observed rate.

**Risks:**
- Believing the clean offline number is already good: re-check on a time split with as-of joins; other leakage may remain.
- Imputing the missing feature (zero, median) and shipping silently, which is what made the live scores collapse.
- Fixing only this feature while the join logic that caused it stays.
- Changing the threshold on the leaky model instead of replacing it.
- Late labels: live AUC is measured on matured labels only.

**What the interviewer scores:**
- Strong: proves leakage with timestamps and ablation, not only a hunch from the AUC gap.
- Strong: separates "what we reported" from "what is true" and states the exposure window.
- Strong: gives an interim plan for the live system (rollback or fallback, thresholds) before the long fix.
- Weak: "retrain the model" without recognising the feature cannot exist at serving time.
- Cross-reference: Book 4 Part 9 has "Point-in-time correct joins. Explain label leakage from joining the latest feature value to old labels, the as-of..." for the feature-store mechanics, and Book 4 Part 1 has "Write tests that catch data leakage" for the test.

**Example:** (illustrative numbers) Offline: AUC 0.96 with the leaky feature. Without it: 0.705, the same as live (0.705 in the run). A tiny as-of join case: user 1 has feature values 100 (day 10), 200 (day 20) and 300 (day 30); the prediction is at day 22. "Latest value ever" gives 300 (a future value); as-of gives 200. Weak answer: "Retrain and hope live improves." Strong answer: "The feature is written after the outcome, so the true AUC is about 0.70. I roll back to the previous model, rebuild training with an as-of join and a time split, add a timestamp check to CI, and recalibrate thresholds."

**Code:**
```python
# Q35: a feature that exists only after the outcome leaks offline and is empty live (illustrative simulation)
import numpy as np
import pandas as pd
from scipy.stats import rankdata

rng = np.random.default_rng(35)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit_logit(X, y, l2=1e-3, steps=40):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(steps):
        p = 1 / (1 + np.exp(-Xb @ w)); g = Xb.T @ (p - y) + l2 * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + l2 * np.eye(len(w))
        w -= np.linalg.solve(H, g)
    return w
def score(w, X): return np.c_[np.ones(len(X)), X] @ w

N = 60_000
legit = rng.normal(size=(N, 3))
y = (legit @ np.array([0.9, 0.6, 0.4]) + rng.normal(0, 2.4, N) > 1.5).astype(int)
# leaky feature: written by the process that happens AFTER the outcome (e.g. a 'case closed' amount)
leak = y * rng.normal(1.0, 0.42, N) + (1 - y) * rng.normal(0.0, 0.42, N)
train, test = slice(0, 40_000), slice(40_000, N)

# 1. Offline with the leaky feature
X_all = np.c_[legit, leak]
w_all = fit_logit(X_all[train], y[train])
offline = auc(y[test], score(w_all, X_all[test]))
# 2. Live: the feature is empty (filled with 0 by the pipeline)
X_live = np.c_[legit, np.zeros(N)]
live = auc(y[test], score(w_all, X_live[test]))
# 3. Clean model, no leaky feature
w_cl = fit_logit(legit[train], y[train])
clean = auc(y[test], score(w_cl, legit[test]))
print(f"offline AUC (with leak) {offline:.3f}   live-like AUC (feature empty) {live:.3f}   clean model {clean:.3f}")
assert offline > 0.93 and 0.68 < live < 0.80 and clean > live - 0.02

# Confirm leakage: single-feature AUC, and ablation
print(f"single-feature AUC: leak {auc(y, leak):.3f}   best legit {max(auc(y, legit[:, j]) for j in range(3)):.3f}")
print(f"ablation: dropping the leaky feature changes offline AUC by {clean - offline:+.3f}")
assert auc(y, leak) > 0.85 and clean < offline - 0.15

# Time check: share of rows whose feature timestamp is after the prediction time
t_pred = rng.uniform(0, 100, N)
t_feat = np.where(rng.random(N) < 0.98, t_pred + rng.uniform(0.1, 5, N), t_pred - 1)   # 98% written later
after = (t_feat > t_pred).mean()
print(f"rows where the feature is written after the prediction time: {after:.1%}")
assert after > 0.97

# Point-in-time (as-of) join versus the leaky 'latest value' join
events = pd.DataFrame({"user": [1, 1, 1, 2, 2], "ts": [10, 20, 30, 15, 25], "val": [100, 200, 300, 50, 60]})
labels = pd.DataFrame({"user": [1, 2], "ts": [22, 20]})                       # prediction times
latest = events.sort_values("ts").groupby("user")["val"].last()               # leaky
asof = pd.merge_asof(labels.sort_values("ts"), events.sort_values("ts"), on="ts", by="user")
print("latest-value join:", latest.to_dict(), "  as-of join:", dict(zip(asof.user, asof.val)))
assert latest.to_dict() == {1: 300, 2: 60} and dict(zip(asof.user, asof.val)) == {1: 200, 2: 50}

# Live handling: the old leaky model's scores shift when the feature is empty
s_off = 1 / (1 + np.exp(-score(w_all, X_all[test]))); s_live = 1 / (1 + np.exp(-score(w_all, X_live[test])))
print(f"mean predicted risk offline {s_off.mean():.3f} vs live-like {s_live.mean():.3f}; true rate {y[test].mean():.3f}")
assert s_live.mean() < 0.5 * s_off.mean()
# decisions at the old threshold of 0.5: how many cases get flagged, and how many true cases are found
for name, s_ in (("offline", s_off), ("live-like", s_live)):
    f = s_ > 0.5
    print(f"{name:10} flagged {f.mean():.1%}  recall {(f & (y[test] == 1)).sum() / y[test].sum():.1%}")
assert (s_live > 0.5).mean() < 0.3 * (s_off > 0.5).mean()
```

**Output (my run):**
```text
offline AUC (with leak) 0.961   live-like AUC (feature empty) 0.705   clean model 0.705
single-feature AUC: leak 0.954   best legit 0.656
ablation: dropping the leaky feature changes offline AUC by -0.256
rows where the feature is written after the prediction time: 98.0%
latest-value join: {1: 300, 2: 60}   as-of join: {2: 50, 1: 200}
mean predicted risk offline 0.287 vs live-like 0.027; true rate 0.286
offline    flagged 27.2%  recall 81.3%
live-like  flagged 0.0%  recall 0.0%
```
The run shows the pattern in the prompt in a simulation: offline 0.961 and live-like 0.705, equal to the clean model; one feature with an AUC of 0.954 alone; 98% of rows where the feature is written after the prediction time; and the old model flagging 27.2% of cases offline but about none live-like.

**Follow-ups:**
- Could the live AUC still be hurt beyond the missing feature? Yes: the model gave the leaky feature most of its weight, so the other weights are not tuned for live; a clean retrain is usually better than the old model with the feature blanked.
- How do you prevent it? Event-time on every feature, as-of joins only, time-based splits, a CI check that fails if a feature timestamp is later than the label's prediction time, and a review of any feature with a suspiciously high single-feature AUC.
- Is it still useful as a signal? Only if a version exists at prediction time; otherwise drop it.

**Common mistakes:** Random train-test split on time-ordered data. "Latest value" joins. Filling the missing feature with zero and moving on. Reporting 0.95 for a month after the review. Fixing the threshold instead of the model.
