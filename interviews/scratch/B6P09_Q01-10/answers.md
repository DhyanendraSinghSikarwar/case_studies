### Q1 ⭐⭐⭐ 🟢 Fintech: A payments app sees 1,000,000 transactions a day, of which 1,000 (0.1% of transactions, a measured monthly average) are fraud. The model blocks 2,000 transactions a day and 600 of the blocked ones are fraud. A blocked genuine customer costs 20 in support and lost goodwill, a missed fraud costs 500 and a caught fraud saves 500. Compute precision, recall and the daily cost of friction versus missed fraud, and say what else you need to know before calling this model good.
**Asked at:** Payments-fraud material (2025 SciTePress, Atlantis Press and SDMIMD papers and student projects on UPI fraud detection frame false alerts, class imbalance and retraining on confirmed fraud and false-positive reports); academic and self-published material, no interview bank for this exact framing; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Precision is 30% and recall is 60%; per day the friction costs 28,000 and the missed fraud costs 200,000, so the model saves 272,000 against no model, but I would not call it good until I know how mature the labels are, what the real cost of a blocked customer is, and how stable the base rate is.

**Clarifying questions:**
- How old are the labels? Chargebacks arrive weeks later, so the 400 missed frauds may be undercounted and recall may be lower than 60%.
- How was precision measured on the 2,000 blocks: review of every block, or a sample? It decides whether 30% is solid.
- Is "20" the whole cost of a wrongly blocked genuine customer, or does it leave out churn and lost lifetime value? The cost ratio sets the threshold.
- Is the block final, or can the customer retry or step up? A softer action changes the cost of a false positive.
- Is 0.1% stable by day, channel and merchant type? A monthly average hides bursts and attacks.

**Approach:**
1. Build the confusion table: 600 caught, 1,400 genuine blocked, 400 missed, the rest passed.
2. Precision = 600 / 2,000 = 30%. Recall = 600 / 1,000 = 60%. False positive rate = 1,400 / 999,000 = 0.14%.
3. Price it: friction = 1,400 x 20 = 28,000. Missed fraud = 400 x 500 = 200,000. Fraud saved = 600 x 500 = 300,000.
4. Compare with a baseline. No model loses 500,000 a day. The model loses 228,000. Net benefit 272,000.
5. Show the break-even: blocking pays when precision is above 20 / 520 = 3.85%. Our 30% is far above that.
6. Then ask what the 272,000 hides: label maturity, adversary adaptation, customer churn, and where the next block should sit on the score curve.

**Metrics:**
- Precision = true frauds blocked / all blocked (600 / 2,000). Recall = true frauds blocked / all fraud (600 / 1,000).
- Net value per day = fraud saved - friction cost. Cost per false positive vs per miss is the ratio 20 : 500.
- Guardrails: false positive rate by segment, share of blocked customers who return within 30 days, support contacts, approval rate, and recall on matured labels.

**Risks:**
- Recall is computed on fraud we know about. Missed fraud that has not been reported yet is not in the 1,000.
- Blocked transactions never reveal what would have happened, so precision needs reviewed outcomes, not assumptions.
- The cost of 20 is small next to a customer who leaves the app; the true ratio could be much higher than 25 to 1.
- Fraudsters move once you block them, so last month's rates drift.

**What the interviewer scores:**
- Strong: gets 30% and 60%, prices both errors, compares to the no-model baseline and gives the break-even precision. Weak: quotes accuracy (99.82%) as the headline.
- Strong: notices that recall depends on label maturity. Weak: treats 1,000 as exact.
- Strong: names a next step (tiered action, threshold by cost), not just "retrain".
- Strong: stays within the data given and labels assumptions as assumptions.

**Example:** (illustrative numbers) Of 2,000 blocks, 600 are fraud and 1,400 are genuine. Accuracy is (1,000,000 - 1,400 - 400) / 1,000,000 = 99.82%, which tells nothing because a model that never blocks scores 99.90%.
- Weak: "Accuracy is 99.82%, the model is great."
- Strong: "Precision is 30%, recall is 60%. It costs 28,000 of friction and still misses 200,000 of fraud, saving 272,000 a day against no model. Blocking only needs 3.85% precision to pay, so the question is not whether to block but whether a softer action for the 1,400 genuine customers, and a lower threshold for the 400 misses, pays more. I would also check label maturity before trusting that 60%."

**Code:**
```python
# Q1 fintech fraud: illustrative numbers from the prompt
N, fraud, blocked, tp = 1_000_000, 1000, 2000, 600
fp = blocked - tp            # genuine customers blocked
fn = fraud - tp              # fraud missed
precision, recall = tp / blocked, tp / fraud
friction = fp * 20           # support + goodwill
missed = fn * 500
saved = tp * 500
net_vs_no_model = saved - friction
fpr = fp / (N - fraud)
be_precision = 20 / (500 + 20)   # block is worth it if p*500 > (1-p)*20
ev_per_block = precision * 500 - (1 - precision) * 20
lift = precision / (fraud / N)
print(f"precision {precision:.0%}, recall {recall:.0%}, FPR {fpr:.4%}, lift over base rate {lift:.0f}x")
print(f"friction {friction:,}, missed fraud {missed:,}, fraud saved {saved:,}, net vs no model {net_vs_no_model:,}")
print(f"break-even precision {be_precision:.2%}, expected value per block {ev_per_block:.0f}")
print(f"no model loses {fraud*500:,}; with model loses {missed + friction:,}")
# day-to-day noise on the 1,000 fraud/day base rate (Poisson sd) so one day's recall is not over-read
print(f"Poisson sd of daily fraud count about {1000**0.5:.0f}")
assert (fp, fn) == (1400, 400)
assert precision == 0.30 and recall == 0.60
assert friction == 28_000 and missed == 200_000 and saved == 300_000 and net_vs_no_model == 272_000
assert round(fpr * 100, 2) == 0.14 and round(lift) == 300
assert round(be_precision * 100, 2) == 3.85 and round(ev_per_block) == 136
assert fraud * 500 == 500_000 and missed + friction == 228_000
acc = (N - fp - fn) / N
print(f"accuracy {acc:.2%} versus never-block accuracy {1 - fraud / N:.2%}")
assert round(acc * 100, 2) == 99.82 and round((1 - fraud / N) * 100, 2) == 99.90
```

**Output (my run):**
```text
precision 30%, recall 60%, FPR 0.1401%, lift over base rate 300x
friction 28,000, missed fraud 200,000, fraud saved 300,000, net vs no model 272,000
break-even precision 3.85%, expected value per block 136
no model loses 500,000; with model loses 228,000
Poisson sd of daily fraud count about 32
accuracy 99.82% versus never-block accuracy 99.90%
```

**Follow-ups:**
- What would you change first? Add a middle band (extra confirmation instead of block), then re-price with the same table.
- How do you know the 1,000 base rate? Use matured chargebacks and fraud reports, and refresh monthly; ask the fraud-operations team how complete the labels are.

**Common mistakes:** Quoting accuracy. Treating a missed fraud and a blocked customer as equal cost. Ignoring label delay. Forgetting a no-model baseline. Calling it good or bad without the cost matrix.

### Q2 ⭐⭐⭐ 🟢 E-commerce: In a search log, results at position 1 get a 12% click-through rate per impression and results at position 5 get 4%, averaged over thousands of queries (measured). A new ranker moves one product from position 5 to position 1 and its click-through rate rises from 4% to 11%. The product manager says the product became 2.75 times more relevant. How do you respond, and how would you estimate relevance separately from position?
**Asked at:** E-commerce ML material (prachub lists Shopify questions on product ranking for a marketplace, package delivery time prediction and personalised product feeds, and a CleverPrep Shopify guide lists search-ranking and embedding trade-offs; Interview Query notes e-commerce promotion and behaviour modelling); candidate-reported and prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** No: the click-through rate rose 2.75 times, but position alone is worth about 3 times (12% versus 4%), so the product did not get more relevant; I would separate relevance from position with randomised position or inverse-propensity weighting.

**Clarifying questions:**
- How many impressions sit behind the 11%? With 2,000 impressions the standard error is about 0.7 points, so 11% versus 12% is not distinguishable.
- Are the 12% and 4% averages for the same kinds of queries and products? The ranker puts good items on top, so those averages mix position with relevance.
- Is click-through rate per impression or per examined result? Impressions below the fold are not seen, so it is a seen-rate times a click-given-seen rate.
- Do we log the displayed position and the page layout (grid versus list, mobile versus desktop)? Propensities differ by layout.
- Is the goal clicks, orders or satisfaction? A click is a weak proxy for relevance (a clickbait title also clicks).

**Approach:**
1. Do the arithmetic the PM skipped: position 5 to position 1 is worth 12% / 4% = 3.0 times on average. If relevance were unchanged, we would expect 4% x 3 = 12% at position 1.
2. Observed 11% is below that. The relevance ratio is 2.75 / 3.0 = 0.92, so the best reading is "no change", maybe slightly lower, within noise.
3. Say the model: click = examined(position) x relevant. Position gives the first factor, the product gives the second.
4. Estimate examination (the propensity): run a small randomised slice where results are shuffled or pairs are swapped; the click-through rate by position there is the examination curve.
5. Then weight logged clicks by 1 / propensity, or train a click model with a position feature that is dropped (or set to a fixed position) at serving.
6. Validate with interleaving or an A/B test judged on orders and downstream satisfaction, not click-through rate.

**Metrics:**
- Click-through rate = clicks / impressions, by position. Position-adjusted relevance = click-through rate / propensity(position).
- Randomised-slice examination ratio = CTR(pos 5) / CTR(pos 1) in the shuffled traffic.
- Guardrails: orders per search, add-to-cart rate, returns, and the revenue cost of the shuffled slice (keep it small, for example 1% of traffic).

**Risks:**
- The logged 12% / 4% ratio is confounded: relevant items are ranked first. In my simulation the logged ratio is about 11.6 although the true examination ratio is 3.
- A tiny slice gives noisy propensities at deep positions; clip weights.
- Layout changes break old propensities.
- Position-adjusted clicks still reward attractive images; add a downstream signal.

**What the interviewer scores:**
- Strong: computes 12 / 4 = 3 and 11 / 12, and says "no evidence of more relevance". Weak: accepts 2.75 times.
- Strong: names position bias and an experiment to remove it (randomisation, swap, interleaving, propensity weighting). Weak: "collect more data".
- Strong: warns that the average position ratio is itself confounded. Weak: treats 3 as exact.
- Strong: gives a quantity of noise (standard error) for one product's CTR.

**Example:** (illustrative numbers)
- Weak: "CTR went from 4% to 11%, so it is 2.75 times more relevant."
- Strong: "Position 1 averages 12% and position 5 averages 4%, so moving up alone explains a 3 times lift. Expected CTR at position 1 with the same relevance is 12%, and we saw 11%. The relevance ratio is 0.92, so no sign of improvement. I would run a 1% shuffled slice to get a clean position curve and weight clicks by it."

**Code:**
```python
import numpy as np
# Part A: the prompt's arithmetic (illustrative, measured position averages)
ctr1, ctr5, new_ctr = 0.12, 0.04, 0.11
pm_claim = new_ctr / ctr5                  # product manager's ratio
pos_factor = ctr1 / ctr5                   # what position alone is worth (average)
rel_ratio = pm_claim / pos_factor          # relevance change after removing position
exp_at_1 = ctr5 * pos_factor               # CTR at position 1 if relevance were unchanged
se_n2000 = (new_ctr * (1 - new_ctr) / 2000) ** 0.5
print(f"PM ratio {pm_claim:.2f}x, position alone {pos_factor:.2f}x, relevance ratio {rel_ratio:.3f}")
print(f"expected CTR at position 1 with unchanged relevance {exp_at_1:.1%} vs observed {new_ctr:.0%}")
print(f"SE of an 11% rate on 2,000 impressions {se_n2000:.4f} (about {se_n2000*100:.1f} points)")
assert pm_claim == 2.75 and round(pos_factor, 6) == 3.0 and round(rel_ratio, 4) == 0.9167
assert round(exp_at_1, 6) == 0.12 and round(se_n2000, 4) == 0.007

# Part B: simulate a position-based click model. Click = examined(position) x relevant.
rng = np.random.default_rng(7)
exam = np.array([0.60, 0.45, 0.33, 0.25, 0.20])       # true examination by position (ratio pos1/pos5 = 3)
Q = 200_000
rel = rng.beta(2, 8, size=(Q, 5))                      # true relevance of 5 candidate products per query (mean 0.2)
# production ranker: sorts by a noisy copy of relevance, so good items land on top
order = np.argsort(-(rel + rng.normal(0, 0.05, rel.shape)), axis=1)
rel_sorted = np.take_along_axis(rel, order, axis=1)
clicks = rng.random((Q, 5)) < exam * rel_sorted
ctr_pos = clicks.mean(axis=0)
naive_ratio = ctr_pos[0] / ctr_pos[4]
# randomised experiment: shuffle the order for a small slice of traffic, so position is independent of relevance
perm = rng.permuted(rel, axis=1)
clicks_r = rng.random((Q, 5)) < exam * perm
ctr_r = clicks_r.mean(axis=0)
rand_ratio = ctr_r[0] / ctr_r[4]
print("logged CTR by position   ", np.round(ctr_pos, 4), "ratio pos1/pos5", round(naive_ratio, 2))
print("randomised CTR by position", np.round(ctr_r, 4), "ratio pos1/pos5", round(rand_ratio, 2))
# inverse-propensity-weighted relevance for one product shown only at position 5, using the randomised propensity
prop = ctr_r / ctr_r[0]                                 # examination relative to position 1
clicks_at5, shows = 400, 10_000
ips_rel_vs_pos1 = (clicks_at5 / shows) / prop[4]        # CTR it would get at position 1
print(f"propensity at pos5 relative to pos1 {prop[4]:.2f}; position-1-equivalent CTR {ips_rel_vs_pos1:.3f}")
assert abs(rand_ratio - 3.0) < 0.15          # randomisation recovers the true examination ratio
assert naive_ratio > rand_ratio + 0.5        # logged ratio is inflated because the ranker puts relevant items first
assert abs(ips_rel_vs_pos1 - 0.12) < 0.01
assert round(naive_ratio, 1) == 11.6
```

**Output (my run):**
```text
PM ratio 2.75x, position alone 3.00x, relevance ratio 0.917
expected CTR at position 1 with unchanged relevance 12.0% vs observed 11%
SE of an 11% rate on 2,000 impressions 0.0070 (about 0.7 points)
logged CTR by position    [0.207  0.1098 0.0611 0.0336 0.0179] ratio pos1/pos5 11.59
randomised CTR by position [0.1195 0.0902 0.0654 0.0504 0.0392] ratio pos1/pos5 3.05
propensity at pos5 relative to pos1 0.33; position-1-equivalent CTR 0.122
```

**Follow-ups:**
- Why not use the click-through rate at position 1 only? Because the ranker chose which items go there, so you would only learn about items already believed relevant (a feedback loop).
- Cheaper than shuffling? Swap adjacent pairs, or use interleaving; both give a smaller revenue cost than a full shuffle.

**Common mistakes:** Comparing raw click-through rates across positions. Reading a ratio from one product on a few thousand impressions. Trusting the logged position curve. Optimising clicks instead of orders.

### Q3 ⭐⭐⭐ 🟢 Healthcare: A screening model has 90% sensitivity and 95% specificity and was validated in a referral hospital where 20% of patients have the condition. It is now deployed in a community clinic where the prevalence is 1% (an assumed planning figure, not measured). For 10,000 patients in each setting, compute the true positives, false positives and positive predictive value, and say how you would explain the difference to clinic staff.
**Asked at:** Clinical-AI external-validation coverage (Fierce Healthcare, MedCity News and JAMA Internal Medicine pages on the external validation of a widely deployed sepsis model, which reported low sensitivity, a modest positive predictive value, alerts on a large share of patients and a billing-code outcome definition; a newsletter piece on local validation and tracking override patterns); published news and research, not an interview bank; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Sensitivity and specificity travel between hospitals, positive predictive value does not: at 20% prevalence the model finds 1,800 true cases with 400 false alarms (PPV 81.8%), at an assumed 1% it finds 90 with 495 false alarms (PPV 15.4%), so about 5 in 6 positives in the clinic are false.

**Clarifying questions:**
- Where does the 1% come from? It is an assumed planning figure, so I would measure it before quoting a PPV to anyone.
- Do sensitivity and specificity really hold in the clinic? Case mix is milder in a community clinic, which often lowers sensitivity; the referral hospital set is not a random sample.
- What happens after a positive: a second test, a referral, or treatment? It sets the cost of a false positive.
- Is this a rule-out tool or a rule-in tool? At 1% the strength is the negative predictive value, not the positives.
- Who owns the follow-up pathway and its capacity? 585 positives per 10,000 is a workload.

**Approach:**
1. Build the 2 x 2 table for each setting with the same sensitivity (90%) and specificity (95%).
2. Referral (20% = 2,000 sick, 8,000 healthy): TP = 1,800, FN = 200, FP = 0.05 x 8,000 = 400, TN = 7,600. PPV = 1,800 / 2,200 = 81.8%.
3. Clinic (1% = 100 sick, 9,900 healthy): TP = 90, FN = 10, FP = 0.05 x 9,900 = 495, TN = 9,405. PPV = 90 / 585 = 15.4%.
4. Cross-check with Bayes: 0.01 x 0.90 / (0.01 x 0.90 + 0.99 x 0.05) = 15.4%.
5. Say the lesson: the false positive rate applies to a much bigger healthy group, so false alarms outnumber hits.
6. Recommend: validate locally, report PPV at the local prevalence, design the follow-up pathway for 585 positives per 10,000, and agree the clinical pathway with the clinic's clinicians.

**Metrics:**
- PPV = TP / (TP + FP). NPV = TN / (TN + FN). Both depend on prevalence; sensitivity = TP / sick and specificity = TN / healthy do not.
- Number flagged per true case = (TP + FP) / TP: 1.22 in the referral setting, 6.5 in the clinic.
- Guardrails: local sensitivity (missed cases, 10 per 10,000 at 1%), follow-up capacity, patient anxiety and downstream cost.

**Risks:**
- Applying the referral PPV to the clinic overstates the model by about 5 times.
- Specificity can also shift with case mix and device, so the clinic numbers are a best case.
- An assumed 1% prevalence: if it is really 0.5% or 2%, PPV moves a lot. Show a range.
- Anchoring on "95% specific" makes staff think 95% of positives are right.

**What the interviewer scores:**
- Strong: the numbers 1,800 / 400 / 81.8% and 90 / 495 / 15.4%, done quickly and correctly. Weak: says PPV is 90% or 95% in both.
- Strong: explains prevalence in one plain sentence. Weak: only gives Bayes' formula.
- Strong: asks for local validation and the downstream pathway. Weak: "retrain the model".
- Strong: flags the 1% as assumed.

**Example:** (illustrative numbers) For staff: "Out of 10,000 people in the clinic, about 100 have it. The test finds 90 of them. But among the 9,900 healthy people it wrongly flags 495. So when it says positive, roughly 1 in 6 is right. A positive is a reason for the confirmation test, not a diagnosis. A negative is very reassuring (99.89% of negatives are healthy)."
- Weak: "The model is 90% sensitive and 95% specific, so a positive means 90% sure."
- Strong: "A positive is right 15.4% of the time here, versus 81.8% in the referral hospital, because only 1% of the clinic's patients have the condition."

**Code:**
```python
# Q3 prevalence and PPV: illustrative numbers
def table(prev, n=10_000, se=0.90, sp=0.95):
    d = round(n * prev); h = n - d
    tp = round(d * se); fn = d - tp
    fp = round(h * (1 - sp)); tn = h - fp
    return dict(sick=d, tp=tp, fn=fn, fp=fp, tn=tn, ppv=tp / (tp + fp), npv=tn / (tn + fn), pos=tp + fp)
ref, clinic = table(0.20), table(0.01)
for name, t in (("referral 20%", ref), ("clinic 1%", clinic)):
    print(f"{name}: sick {t['sick']}, TP {t['tp']}, FP {t['fp']}, FN {t['fn']}, positives {t['pos']}, PPV {t['ppv']:.1%}, NPV {t['npv']:.2%}")
print(f"patients flagged per true case found: referral {ref['pos']/ref['tp']:.2f}, clinic {clinic['pos']/clinic['tp']:.2f}")
# the same result from Bayes' rule on a single patient
p = 0.01 * 0.90 / (0.01 * 0.90 + 0.99 * 0.05)
print(f"Bayes check at 1%: {p:.1%}")
# what prevalence would be needed for a PPV of 50%?
prev50 = 0.05 / (0.90 + 0.05)  # solve prev*0.9 = (1-prev)*0.05
print(f"prevalence at which PPV = 50%: {prev50:.1%}")
assert (ref['tp'], ref['fp'], ref['fn']) == (1800, 400, 200) and round(ref['ppv'], 3) == 0.818
assert (clinic['tp'], clinic['fp'], clinic['fn']) == (90, 495, 10) and round(clinic['ppv'], 3) == 0.154
assert clinic['pos'] == 585 and ref['pos'] == 2200
assert abs(p - clinic['ppv']) < 1e-3
assert round(prev50, 4) == 0.0526 and round(ref['npv'], 4) == 0.9744 and round(clinic['npv'], 4) == 0.9989
assert round(clinic['pos'] / clinic['tp'], 1) == 6.5 and round(ref['pos'] / ref['tp'], 2) == 1.22
```

**Output (my run):**
```text
referral 20%: sick 2000, TP 1800, FP 400, FN 200, positives 2200, PPV 81.8%, NPV 97.44%
clinic 1%: sick 100, TP 90, FP 495, FN 10, positives 585, PPV 15.4%, NPV 99.89%
patients flagged per true case found: referral 1.22, clinic 6.50
Bayes check at 1%: 15.4%
prevalence at which PPV = 50%: 5.3%
```

**Follow-ups:**
- How would you raise the clinic PPV? Use a second-stage test on positives, a higher threshold (accepting lower sensitivity), or screen only a higher-risk group. Each choice goes through the clinical team.
- How do you verify prevalence? A small prospective sample with the reference standard, or the clinic's own historical case counts.

**Common mistakes:** Carrying PPV across settings. Quoting sensitivity and specificity as "accuracy". Forgetting that the 1% is assumed. Not mentioning the follow-up workload.

### Q4 ⭐⭐⭐ 🟢 Ads: A click model predicts an average click-through rate of 3.0% on 1,000,000 impressions, but 24,000 clicks were observed, an observed rate of 2.4% (a measured day). The AUC is unchanged and advertisers bid a value per click of 10, so the bid per impression is the predicted rate times 10. Compute the bid per impression with and without the error and the relative overbid, and explain why a good AUC does not protect you here and how you would fix it.
**Asked at:** Ads ML and calibration material (Dataford questions on CTR calibration and click-through rate at an ad-tech firm, AlgoMaster and Educative ad click prediction system-design pages with calibration-error checks by probability bin); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The model bids 0.30 per impression where the observed rate supports 0.24, which is a 25% overbid on the correct bid (the excess is 20% of the bid made); AUC only measures ranking, so a model that is 25% too high everywhere keeps its AUC and still burns money, and the fix is a calibration layer plus monitoring.

**Clarifying questions:**
- Is the 3.0% versus 2.4% gap uniform or does it differ by segment, placement and score bin? A uniform scale and a bin-specific error need different fixes.
- Is it one day or a trend? The prompt says a measured day; a single day can include a traffic mix shift.
- Is the auction second price or first price? Overbidding costs more under first price, where you pay what you bid.
- Does the bid use the prediction directly (value x predicted rate) or does the bidder add a shading or pacing factor? That decides how far the error flows into spend.
- How fast do labels arrive? Clicks are quick, which makes daily recalibration realistic.

**Approach:**
1. Compute the bid: 0.030 x 10 = 0.30 per impression. With the observed rate: 0.024 x 10 = 0.24.
2. Overbid = 0.30 / 0.24 - 1 = 25% (relative to the correct bid). Say the base out loud: the excess is also 20% of the 0.30 actually bid.
3. Over 1,000,000 impressions the bids sum to 300,000 versus 240,000: 60,000 of extra bid amount. That is not the extra spend: it depends on auction type and win rate.
4. Explain AUC: it depends only on the order of scores. Multiply every prediction by 1.25 or shift the logit, and AUC does not move. Bids need the level, not the order.
5. Diagnose with a reliability table: group impressions into score bins and compare mean prediction with observed click rate per bin, and by segment.
6. Fix: add a monotone calibration layer (a scale of 0.8 as a stop-gap, then isotonic or logistic recalibration on fresh data), refit daily, and alert when the ratio of observed to predicted leaves a band.

**Metrics:**
- Calibration ratio = observed clicks / predicted clicks = 24,000 / 30,000 = 0.80. Expected calibration error by score bin.
- Overbid % = bid with error / bid without error - 1.
- Guardrails: win rate, spend versus plan, cost per click against the advertiser's target, and AUC (to see calibration did not damage ranking).

**Risks:**
- Fixing the average hides bin errors: the model can be right on average and wrong in the tail where bids are large.
- Recalibrating on logged data from won auctions only is biased toward impressions you already win.
- Calibration drifts with seasons, new placements and ad formats; a one-off scale goes stale.
- Calibration fixes the level, not a broken ranking.

**What the interviewer scores:**
- Strong: 0.30, 0.24, 25% with the base stated, and that AUC cannot see it. Weak: "AUC is fine so the model is fine".
- Strong: a concrete fix (isotonic or Platt, per-segment, refreshed daily) plus monitoring. Weak: "retrain the model".
- Strong: separates the bid amount from actual spend by auction type.
- Strong: checks calibration by bin, not only the average.

**Example:** (illustrative numbers)
- Weak: "The AUC is the same, so nothing is wrong."
- Strong: "We predicted 3.0% and saw 2.4%, so we bid 0.30 where 0.24 is right, a 25% overbid. AUC ignores the level. I would multiply by 0.8 today, check the reliability table by bin, and put an isotonic layer on fresh data with an alert when observed over predicted leaves 0.95 to 1.05."

**Code:**
```python
import numpy as np
from scipy.stats import rankdata
from scipy.optimize import brentq
# Part A: prompt arithmetic (illustrative, measured day)
imps, clicks, v = 1_000_000, 24_000, 10
pred, obs = 0.030, clicks / imps
bid_pred, bid_true = pred * v, obs * v
overbid_vs_correct = bid_pred / bid_true - 1
excess_share_of_bid = (bid_pred - bid_true) / bid_pred
cal_ratio = obs / pred
print(f"observed CTR {obs:.1%}; bid per impression {bid_pred:.2f} (model) vs {bid_true:.2f} (calibrated)")
print(f"overbid {overbid_vs_correct:.0%} of the correct bid; excess is {excess_share_of_bid:.0%} of the bid made; fix factor {cal_ratio:.2f}")
print(f"sum of bids over the day: {bid_pred*imps:,.0f} vs {bid_true*imps:,.0f}, difference {(bid_pred-bid_true)*imps:,.0f} (bid amount, not spend)")
assert obs == 0.024 and round(bid_pred, 6) == 0.30 and round(bid_true, 6) == 0.24
assert round(overbid_vs_correct, 6) == 0.25 and round(excess_share_of_bid, 6) == 0.20 and round(cal_ratio, 6) == 0.8
assert round((bid_pred - bid_true) * imps) == 60_000

# Part B: a miscalibrated model with the same ranking, then a recalibration layer
rng = np.random.default_rng(11)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def sig(x): return 1 / (1 + np.exp(-x))
def logit(p): return np.log(p / (1 - p))
def day(n):
    p = rng.beta(1.2, 48.8, n)                      # true click probabilities, mean 2.4%
    y = (rng.random(n) < p).astype(int)
    return p, y
p1, y1 = day(400_000); p2, y2 = day(400_000)
shift = brentq(lambda d: sig(logit(p1) + d).mean() - 0.030, 0, 2)   # model over-predicts: mean 3.0%
s1, s2 = sig(logit(p1) + shift), sig(logit(p2) + shift)
print(f"day 2: mean prediction {s2.mean():.4f}, observed rate {y2.mean():.4f}, AUC raw {auc(y2, s2):.4f}, AUC of true p {auc(y2, p2):.4f}")
# recalibrate on day 1 with 20 quantile bins (monotone map), score day 2
edges = np.quantile(s1, np.linspace(0, 1, 21)); edges[0], edges[-1] = 0, 1
b1 = np.digitize(s1, edges[1:-1]); rate = np.array([y1[b1 == k].mean() for k in range(20)])
rate = np.maximum.accumulate(rate)                   # keep it monotone
c2 = rate[np.digitize(s2, edges[1:-1])]
def ece(p, y, k=10):
    q = np.quantile(p, np.linspace(0, 1, k + 1)); idx = np.clip(np.digitize(p, q[1:-1]), 0, k - 1)
    return sum(abs(p[idx == i].mean() - y[idx == i].mean()) * (idx == i).mean() for i in range(k))
print(f"mean prediction after recalibration {c2.mean():.4f}; ECE before {ece(s2, y2):.4f}, after {ece(c2, y2):.4f}; AUC after {auc(y2, c2):.4f}")
assert abs(s2.mean() - 0.030) < 0.001 and abs(y2.mean() - 0.024) < 0.001
assert abs(auc(y2, s2) - auc(y2, p2)) < 1e-9           # a monotone shift cannot change AUC
assert ece(c2, y2) < ece(s2, y2) / 5 and abs(c2.mean() - y2.mean()) < 0.001
assert abs(auc(y2, c2) - auc(y2, s2)) < 0.003         # binning adds a few ties, so allow a small change
```

**Output (my run):**
```text
observed CTR 2.4%; bid per impression 0.30 (model) vs 0.24 (calibrated)
overbid 25% of the correct bid; excess is 20% of the bid made; fix factor 0.80
sum of bids over the day: 300,000 vs 240,000, difference 60,000 (bid amount, not spend)
day 2: mean prediction 0.0300, observed rate 0.0239, AUC raw 0.7366, AUC of true p 0.7366
mean prediction after recalibration 0.0239; ECE before 0.0060, after 0.0005; AUC after 0.7354
```

**Follow-ups:**
- Why not just retrain? You can, but a thin calibration layer is faster and can be refreshed hourly, while the main model changes weekly.
- What if the error is only in one segment? Calibrate per segment with enough data, or add the segment to the calibration features, and keep a global fallback.

**Common mistakes:** Quoting AUC as proof of correct bids. Calling 25% and 20% the same number. Treating bid amount as spend. Calibrating once and never again. Checking only the mean.

### Q5 ⭐⭐⭐ 🟢 E-commerce: Checkout shows a delivery promise of 3 days, and in a sample of 50,000 delivered orders 44,000 (88%) arrived within the promise, which leaves 6,000 late orders. Late orders have a 30-day repeat-purchase rate of 20% against 30% for on-time orders (absolute, per customer, measured sample), a gap that is 600 repeat purchases across the 6,000 late orders. A 4-day promise would be met on an assumed 97% of orders, which is 1,500 late orders per 50,000, but checkout conversion might fall. How do you choose the promise, and what experiment would you run?
**Asked at:** E-commerce ML material (prachub lists Shopify questions on product ranking for a marketplace, package delivery time prediction and personalised product feeds, and a CleverPrep Shopify guide lists search-ranking and embedding trade-offs; Interview Query notes e-commerce promotion and behaviour modelling); candidate-reported and prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would not pick the promise from the late-order gap alone: a 4-day promise cuts late orders from 6,000 to 1,500 and, if the whole 10-point repeat gap were caused by lateness, keeps at most 450 repeat purchases per 50,000, which only pays if checkout conversion falls by less than about 0.9% relative; so I would randomise the promise and read conversion, lateness and 30-day repeat together.

**Clarifying questions:**
- Why are some orders late: warehouse, carrier, region, order size? If late orders are remote or heavy orders, their lower repeat rate is partly the customer, not the delay.
- Is the promise one number for everyone or could it vary by route and item? A per-order promise beats a global one.
- What does a late order cost beyond repeat rate: refunds, support contacts, cancellations? They belong in the margin.
- What is the baseline checkout conversion and how much traffic do we have? It decides whether we can detect a small drop.
- How is "late" defined for the 4-day option: later than 4 days, or later than the promise shown to that customer? It must be the shown promise.

**Approach:**
1. Restate the data: 6,000 of 50,000 are late at 3 days (12%). Their repeat rate is 20% versus 30%: a 10-point gap, which is 600 repeat purchases.
2. Say what the gap is not: it is observational. Late orders differ (distance, carrier, items), so only part of the 600 is caused by lateness.
3. Cost of the 4-day promise: late orders fall to 1,500 (3%), so 4,500 fewer late orders. Best case gain = 4,500 x 10 points = 450 repeat purchases; if half of the gap is causal, 225.
4. Price the other side: a longer promise may lower checkout conversion. Break-even relative drop = 450 / 50,000 = 0.9% (0.45% if half causal), counting a repeat purchase as worth one order for illustration.
5. Run an experiment: randomise customers at checkout between a 3-day and a 4-day promise (and, better, a third arm with a per-order promise from a predicted delivery-time quantile).
6. Read conversion, orders, on-time rate against the shown promise, 30-day repeat per customer, cancellations, support contacts and margin. Wait 30 days for the repeat outcome.
7. Decide with a pre-agreed margin: ship the 4-day or the per-order promise only if the conversion drop stays inside the break-even and margin is not lower.

**Metrics:**
- On-time rate = orders delivered within the promise shown / orders delivered. Repeat rate = customers with another order within 30 days / customers.
- Net effect per 50,000 orders = repeat purchases gained x value - conversion loss x value - cost of lateness.
- Guardrails: checkout conversion (relative change), cancellation rate, support contacts per order, and the share of orders where the promise is shown.

**Risks:**
- Confounding: late and on-time orders are different customers; the 450 is an upper bound.
- Conversion test power: on an invented 5% conversion, seeing a 0.9% relative drop needs about 3.7 million sessions per arm, and a 0.45% drop about 14.7 million. Use a non-inferiority margin, not a significance hunt.
- The 97% for 4 days is an assumption; measure it in the test.
- Novelty: customers may behave differently after seeing a long promise for a day.

**What the interviewer scores:**
- Strong: 12%, 1,500, 4,500, 450 and the break-even conversion drop. Weak: "pick 4 days because 97% is better than 88%".
- Strong: says the 10-point gap is correlational. Weak: treats 600 as saved by faster delivery.
- Strong: a randomised design with a 30-day outcome and guardrails. Weak: before-after comparison.
- Strong: suggests a per-order promise.

**Example:** (illustrative numbers)
- Weak: "Late orders cost us 600 repeat purchases, so promise 4 days and we win them back."
- Strong: "A 4-day promise turns 4,500 of the 6,000 late orders into on-time ones. If lateness caused the whole 10-point gap, that is 450 repeat purchases, and if only half did, 225. It pays only if checkout conversion falls by less than 0.9% relative, or 0.45%. So I would randomise the promise and read conversion, on-time rate and 30-day repeat together."

**Code:**
```python
# Q5 delivery promise: illustrative numbers from the prompt plus invented conversion inputs
orders, on_time3 = 50_000, 44_000
late3 = orders - on_time3
rep_late, rep_ok = 0.20, 0.30
gap = rep_ok - rep_late
gap_orders = late3 * gap
late4 = round(orders * (1 - 0.97))
fewer_late = late3 - late4
gain_causal = fewer_late * gap              # repeat purchases kept if the whole gap were caused by lateness
gain_half = gain_causal / 2                 # if only half the gap is caused by lateness
print(f"late at 3 days {late3} ({late3/orders:.0%}); gap {gap:.0%} -> {gap_orders:.0f} repeat purchases")
print(f"late at 4 days {late4} ({late4/orders:.0%}); fewer late orders {fewer_late}; repeat purchases gained: causal {gain_causal:.0f}, half causal {gain_half:.0f}")
# break-even drop in checkout conversion: lost orders = gained repeat purchases (a repeat counted as worth one order, illustrative)
be_causal = gain_causal / orders
be_half = gain_half / orders
print(f"break-even relative conversion drop: {be_causal:.2%} (gap fully causal), {be_half:.2%} (half causal)")
# sample size to see a drop that small on an invented 5% checkout conversion (two-sided 5%, 80% power)
p = 0.05
for rel in (be_causal, be_half):
    delta = p * rel
    n = 2 * (1.96 + 0.84) ** 2 * p * (1 - p) / delta ** 2
    print(f"detect {rel:.2%} relative drop on {p:.0%} conversion: about {n/1e6:.1f} million sessions per arm")
n_half = 2 * (1.96 + 0.84) ** 2 * p * (1 - p) / (p * be_half) ** 2
n_causal = 2 * (1.96 + 0.84) ** 2 * p * (1 - p) / (p * be_causal) ** 2
assert (late3, late4, fewer_late) == (6000, 1500, 4500)
assert round(gap, 2) == 0.10 and round(gap_orders) == 600
assert round(gain_causal) == 450 and round(gain_half) == 225
assert round(be_causal, 4) == 0.009 and round(be_half, 4) == 0.0045
assert round(n_causal / 1e6, 1) == 3.7 and round(n_half / 1e6, 1) == 14.7
```

**Output (my run):**
```text
late at 3 days 6000 (12%); gap 10% -> 600 repeat purchases
late at 4 days 1500 (3%); fewer late orders 4500; repeat purchases gained: causal 450, half causal 225
break-even relative conversion drop: 0.90% (gap fully causal), 0.45% (half causal)
detect 0.90% relative drop on 5% conversion: about 3.7 million sessions per arm
detect 0.45% relative drop on 5% conversion: about 14.7 million sessions per arm
```

**Follow-ups:**
- Could the promise vary per order? Yes: promise the 90th percentile of predicted delivery time per route and item, and measure on-time rate and conversion.
- What if the repeat window is too slow for the test? Use leading indicators (support contacts, delivery rating) and a shorter proxy, then confirm with the 30-day outcome.

**Common mistakes:** Reading an observational gap as a causal effect. Ignoring conversion. Measuring "late" against the old promise in the 4-day arm. Reading the result before the 30-day window closes. Testing on a few thousand sessions.

### Q6 ⭐⭐⭐ 🟡 Fintech: A lender gets 100,000 applications a month and 30,000 of them (30% of applications) are thin-file with no bureau score, and its model has an AUC of 0.82 on thick-file applicants but 0.66 on thin-file ones. A pilot would approve 2,000 extra thin-file applicants a month with a credit limit of 5,000 each, a profit of 1,200 per repaying customer and a loss of 4,000 per defaulter. Compute the exposure of the pilot as an upper bound (all limits fully drawn, no recovery) and the break-even default rate, and explain what data, controls and review you would use.
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The pilot's exposure is at most 2,000 x 5,000 = 10,000,000 if every limit is fully drawn with no recovery, and it breaks even at a default rate of 1,200 / (1,200 + 4,000) = 23.1%; with an AUC of only 0.66 I would run it as a capped, staged, partly randomised pilot with a hard loss budget, agreed with risk, compliance and model validation.

**Clarifying questions:**
- What default rate do thin-file customers show today, and on what definition (90 days past due within 12 months)? The break-even of 23.1% means little without the expected rate.
- Is the 4,000 loss per defaulter after partial drawing and recovery, or a gross figure? The prompt's bound uses 5,000 (the full limit), so the two numbers disagree on how much is recovered; I would ask which one finance uses.
- Which data can lift thin-file ranking (rent, utilities, bank transaction history, income verification), and is each allowed to be used? Ask compliance.
- What is the risk appetite: the maximum monthly loss the business accepts for a pilot?
- How long until outcomes mature? A 12-month default definition means the pilot reads out slowly, so which early signals does the risk team trust?

**Approach:**
1. Exposure bound: 2,000 x 5,000 = 10,000,000. If every one of the 2,000 defaulted at the stated loss, the loss is 2,000 x 4,000 = 8,000,000. Both are ceilings, not forecasts.
2. Break-even: profit when (1 - d) x 1,200 = d x 4,000, so d = 23.08%.
3. Sensitivity (monthly, illustrative): at 5% default the pilot earns 1,880,000, at 10% 1,360,000, at 20% 320,000, at 23.1% zero, at 30% it loses 720,000.
4. Say what AUC 0.66 means: weak ranking. In a simple model, the riskiest 20% of applicants hold about 37% of defaulters at AUC 0.66 against about 61% at 0.82, so the score separates thin-file risk poorly and the cut-off will leak.
5. Design the pilot: start with smaller limits (a ladder of limits that rise with good repayment), approve in randomly chosen score bands to learn about the applicants we would normally reject, cap total exposure by month, and use a control group.
6. Controls: early-warning triggers (first-payment default, early delinquency), a stop rule on a pre-agreed loss budget, a champion-challenger comparison with the current policy, and fairness checks across customer groups.
7. Review: model-risk validation of the thin-file features and the pilot design before launch, with compliance reviewing data use and customer communication.

**Metrics:**
- Exposure = approvals x limit (upper bound). Default rate = defaulters / approved at 12 months, with an early proxy such as 30-day or 60-day delinquency at month 3.
- Profit per month = approved x ((1 - d) x 1,200 - d x 4,000). Break-even d = 1,200 / 5,200.
- Guardrails: realised drawn balance versus limit, approval rate by segment, loss against budget, share of pilot customers who later get bureau files (to bring them into the main model).

**Risks:**
- Selection: approving "extra" applicants who were rejected before means no outcome history to calibrate on.
- Weak AUC makes the pilot sensitive to the cutoff; a small shift in the mix can push default toward the break-even.
- Thin-file populations can overlap with protected groups; proxies in alternative data need review.
- Early signals may not predict 12-month default; stop rules can trigger too late or too early.
- The 12-month wait: the pilot is a loan book while it runs.

**What the interviewer scores:**
- Strong: 10,000,000, 23.1%, plus the sensitivity table and a statement that both are bounds. Weak: only gives the two numbers.
- Strong: notes 8,000,000 versus 10,000,000 mismatch, or asks. Weak: does not notice.
- Strong: concrete controls (limit ladder, exposure cap, stop rule, randomised band, challenger) and owners (risk, validation, compliance). Weak: "monitor closely".
- Strong: asks compliance about data and decisions rather than asserting rules.

**Example:** (illustrative numbers)
- Weak: "Exposure is 10 million and break-even is 23%, so go."
- Strong: "Worst case balance at risk is 10 million, and the stated loss would be 8 million if everyone defaulted. Break-even is 23.1%, so at a 10% default rate we earn about 1.36 million a month, and at 30% we lose 0.72 million. With AUC 0.66, I would not trust the cutoff, so I would start with smaller limits, randomise approvals inside a band, set a loss budget with a stop rule, and have validation and compliance sign off on the data."

**Code:**
```python
from scipy.stats import norm
# Q6 thin-file pilot: illustrative numbers
apps, thin = 100_000, 30_000
pilot, limit, profit, loss = 2_000, 5_000, 1_200, 4_000
exposure = pilot * limit                     # all limits drawn, no recovery: upper bound on balances at risk
max_loss_stated = pilot * loss               # if every pilot customer defaulted at the stated loss per defaulter
be = profit / (profit + loss)                # (1-d)*profit = d*loss
def pilot_profit(d): return pilot * ((1 - d) * profit - d * loss)
print(f"thin-file share {thin/apps:.0%}; pilot is {pilot/thin:.1%} of monthly thin-file applicants")
print(f"exposure upper bound {exposure:,}; loss if all default at stated 4,000 each {max_loss_stated:,}")
print(f"break-even default rate {be:.2%}")
for d in (0.05, 0.10, 0.20, be, 0.30):
    print(f"  default rate {d:5.1%}: pilot profit per month {round(pilot_profit(d)) + 0:>12,}")
se = (0.10 * 0.90 / pilot) ** 0.5
print(f"SE of a 10% default rate on {pilot} loans: {se*100:.2f} points")
# what AUC 0.66 vs 0.82 means: share of defaulters in the worst-scored 20% (equal-variance normal scores)
def capture(auc, p_def=0.10, frac=0.20):
    # scores: good ~ N(0,1), bad ~ N(d,1). Find threshold so that the top `frac` of ALL applicants is flagged.
    d = 2 ** 0.5 * norm.ppf(auc)
    from scipy.optimize import brentq
    t = brentq(lambda t: (1 - p_def) * norm.sf(t) + p_def * norm.sf(t - d) - frac, -5, 8)
    return norm.sf(t - d)
c82, c66 = capture(0.82), capture(0.66)
print(f"defaulters caught in the riskiest 20% of applicants: AUC 0.82 -> {c82:.0%}, AUC 0.66 -> {c66:.0%} (illustrative binormal model)")
assert thin / apps == 0.30 and round(pilot / thin, 3) == 0.067
assert exposure == 10_000_000 and max_loss_stated == 8_000_000
assert round(be, 4) == 0.2308 and abs(pilot_profit(be)) < 1e-6
assert round(pilot_profit(0.05)) == 1_880_000 and round(pilot_profit(0.10)) == 1_360_000 and round(pilot_profit(0.20)) == 320_000
assert round(pilot_profit(0.30)) == -720_000 and round(se * 100, 2) == 0.67
assert c82 > c66 + 0.15
assert round(c82, 2) == 0.61 and round(c66, 2) == 0.37
```

**Output (my run):**
```text
thin-file share 30%; pilot is 6.7% of monthly thin-file applicants
exposure upper bound 10,000,000; loss if all default at stated 4,000 each 8,000,000
break-even default rate 23.08%
  default rate  5.0%: pilot profit per month    1,880,000
  default rate 10.0%: pilot profit per month    1,360,000
  default rate 20.0%: pilot profit per month      320,000
  default rate 23.1%: pilot profit per month            0
  default rate 30.0%: pilot profit per month     -720,000
SE of a 10% default rate on 2000 loans: 0.67 points
defaulters caught in the riskiest 20% of applicants: AUC 0.82 -> 61%, AUC 0.66 -> 37% (illustrative binormal model)
```

**Follow-ups:**
- How do you learn about people you would have rejected? Randomised approval in a narrow band near the cutoff, with caps (a small cost for real outcomes).
- When would you scale the pilot? When early delinquency is inside the plan on enough loans, validation agrees, and the loss budget has headroom.

**Common mistakes:** Quoting exposure as expected loss. Missing that the profit depends on the default rate, which nobody knows yet. Treating AUC 0.66 like 0.82. Skipping stop rules. Stating regulatory rules as facts.

### Q7 ⭐⭐⭐ 🟡 E-commerce: New sellers make up 8% of live listings but receive 2% of search impressions, because the ranker favours listings with a conversion history. The team wants to reserve 5% of 10,000,000 daily search impressions for exploration, where new listings are assumed to convert at 2.0% per impression against 3.0% for the normal ranking (a projection). Compute the daily orders given up by the exploration budget in absolute and relative terms, and say how you would run the exploration and judge whether it is worth it.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to cold-start in marketplace search and recommendation system-design material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Reserving 5% of 10,000,000 impressions gives up about 5,000 orders a day, 1.67% of the 300,000 the normal ranking would produce, if new listings really convert at 2.0% against 3.0%; I would pay that as an information budget, run it as a capped adaptive explore on a randomised slice, and judge it on whether the seller-side and long-run gains beat the cost.

**Clarifying questions:**
- Is the 5% in addition to the 2% new sellers already get, or does it include it? If it includes it, only 3 points are extra and the cost falls to about 3,000 orders (1.0%).
- Where does the 2.0% come from? It is a projection; at 1.5% the cost is 7,500 orders (2.5%) and at 2.5% it is 2,500 (0.83%).
- How many new listings per day and how fast do they get a first sale? It sets how deep each listing can be explored.
- Are the lost orders really lost, or does the buyer buy a similar item elsewhere on the site? Gross versus net.
- What is the goal: seller retention, catalogue breadth, or finding future winners? Each has a different success metric.

**Approach:**
1. The cost: 5% x 10,000,000 = 500,000 impressions. At 2.0% they give 10,000 orders; at the normal 3.0% they would give 15,000. Lost = 5,000 orders a day, 5,000 / 300,000 = 1.67% relative.
2. State the ambiguity: baseline orders of 300,000 assume all impressions at 3.0%; the 2% already going to new sellers makes the true baseline slightly lower (298,000 under the other reading).
3. Gross is not net: the 10,000 orders from exploration are real orders for sellers, and some lost orders are substituted by other purchases.
4. Run it as an adaptive explore, not a flat lottery: show a new listing in a limited number of impressions, update its conversion estimate with a prior, and give more to those that look good (Thompson-style sampling). A cap per listing stops waste.
5. Randomise it: explore on a random slice of queries or users, keep a holdout, and place new listings at a limited set of positions so lift can be read cleanly.
6. Judge it: cost per day (5,000 orders) against what it buys: new sellers reaching a first sale, the share of listings with an estimated conversion, the number of future winners found, and seller retention. Re-check after 4 to 8 weeks.

**Metrics:**
- Orders given up = exploration impressions x (normal rate - new-listing rate) = 500,000 x 0.01. Relative = given-up / orders at normal rate.
- Time to first sale for new listings, share of new listings with at least N impressions, seller retention at 30 days, orders from listings that graduated from exploration.
- Guardrails: orders per search, GMV per search, buyer satisfaction and return rate on explored listings, and fraud or low-quality listings in explored traffic.

**Risks:**
- Exploration impressions can include poor listings, hurting buyer experience on those searches.
- The new-listing rate (2.0%) may be wrong; a 1.5% rate raises cost by half.
- Needing about 1,911 impressions to tell a 2.0% listing from the 3.0% benchmark (illustrative variance): at that depth the budget covers only about 262 listings a day, so flat exploration is slow; adaptive allocation matters.
- Sellers may game the exploration slot with fresh listings.

**What the interviewer scores:**
- Strong: 5,000 orders, 1.67%, with the 3.0% base stated, plus the other reading (3,000, 1.0%). Weak: "it costs 5%".
- Strong: states that cost is not the same as value and names what is bought. Weak: no benefit measure.
- Strong: adaptive exploration with a cap per listing and a randomised holdout. Weak: "boost all new listings".
- Strong: labels 2.0% as a projection and shows a range.

**Example:** (illustrative numbers)
- Weak: "Exploration costs 5% of impressions, so 5% fewer orders."
- Strong: "500,000 impressions at 2.0% give 10,000 orders instead of 15,000. That is 5,000 a day, 1.67% of the 300,000 we would make, and it falls to 3,000 if the 5% includes the 2% new sellers already get. In my simulation, Thompson-style allocation gave about 26% more orders from the same exploration budget than uniform allocation and picked better listings. I would run it with caps on a randomised slice and judge it on first sales and seller retention."

**Code:**
```python
import numpy as np
# Part A: prompt arithmetic (illustrative; 2.0% new-listing rate is a projection)
imps = 10_000_000
expl = 0.05 * imps
orders_expl = expl * 0.02
orders_normal_same_imps = expl * 0.03
lost = orders_normal_same_imps - orders_expl
base_orders = imps * 0.03                    # if every impression converted at 3.0%
print(f"exploration impressions {expl:,.0f}; orders {orders_expl:,.0f} instead of {orders_normal_same_imps:,.0f}; lost {lost:,.0f} = {lost/base_orders:.2%} of {base_orders:,.0f}")
# the 2% share new sellers already get: if the 5% includes it, only 3 points are extra
extra = (0.05 - 0.02) * imps
lost_net = extra * (0.03 - 0.02)
base2 = 0.98 * imps * 0.03 + 0.02 * imps * 0.02
print(f"if 5% includes today's 2%: extra exploration {extra:,.0f} impressions, lost {lost_net:,.0f} = {lost_net/base2:.2%} of {base2:,.0f}")
for r in (0.015, 0.02, 0.025):
    print(f"  if new listings convert at {r:.1%}: lost {expl*(0.03-r):,.0f} orders/day ({expl*(0.03-r)/base_orders:.2%})")
# impressions to tell a 2.0% listing from the 3% benchmark (variance taken at 2.5%) (one-sample, 5% two-sided, 80% power)
p = 0.025; delta = 0.01
n_one = (1.96 + 0.84) ** 2 * p * (1 - p) / delta ** 2
print(f"impressions per listing to separate 2.0% from 3.0%: about {n_one:,.0f}; the budget covers {expl/n_one:,.0f} listings a day at that depth")
assert expl == 500_000 and round(orders_expl) == 10_000 and round(lost) == 5_000 and round(base_orders) == 300_000
assert round(lost / base_orders, 4) == 0.0167
assert extra == 300_000 and round(lost_net) == 3_000 and round(base2) == 298_000 and round(lost_net / base2, 4) == 0.0101
assert round(expl * 0.015) == 7_500 and round(n_one) == 1_911 and round(expl / n_one) == 262

# Part B: uniform exploration versus Thompson sampling over 2,000 new listings (invented conversion rates)
rng = np.random.default_rng(5)
L, budget, rounds = 2_000, 500_000, 20
true = rng.beta(2, 98, L)                    # mean about 2%
def run(adaptive):
    a = np.ones(L); b = np.ones(L); orders = 0
    per_round = budget // rounds
    for _ in range(rounds):
        if adaptive:
            draw = rng.beta(a, b)
            pick = rng.choice(L, size=per_round, p=draw / draw.sum())   # probability matching on a posterior draw
        else:
            pick = rng.integers(0, L, per_round)
        shows = np.bincount(pick, minlength=L)
        conv = rng.binomial(shows, true)
        a += conv; b += shows - conv; orders += conv.sum()
    top = np.argsort(-(a / (a + b)))[:200]
    return orders, true[top].mean(), true[np.argsort(-true)[:200]].mean()
o_u, q_u, best = run(False); o_t, q_t, _ = run(True)
print(f"uniform: {o_u:,} orders, mean true rate of picked top 200 {q_u:.4f}; Thompson-style: {o_t:,} orders, {q_t:.4f}; oracle top 200 {best:.4f}")
assert o_t > o_u and q_t > q_u
assert round(o_t / o_u - 1, 2) == 0.26
```

**Output (my run):**
```text
exploration impressions 500,000; orders 10,000 instead of 15,000; lost 5,000 = 1.67% of 300,000
if 5% includes today's 2%: extra exploration 300,000 impressions, lost 3,000 = 1.01% of 298,000
  if new listings convert at 1.5%: lost 7,500 orders/day (2.50%)
  if new listings convert at 2.0%: lost 5,000 orders/day (1.67%)
  if new listings convert at 2.5%: lost 2,500 orders/day (0.83%)
impressions per listing to separate 2.0% from 3.0%: about 1,911; the budget covers 262 listings a day at that depth
uniform: 10,139 orders, mean true rate of picked top 200 0.0458; Thompson-style: 12,798 orders, 0.0476; oracle top 200 0.0507
```

**Follow-ups:**
- How big is the holdout? Big enough to see 1.67% on orders per search; with a few percent of traffic this takes weeks, so read leading indicators too.
- What if sellers copy-paste listings to farm exploration? Limit exploration per seller and per product, and require quality checks.

**Common mistakes:** Treating the projection as a fact. Using one base for "relative" without saying which. Flat boosting with no cap. No measure of what exploration buys. Ignoring buyer-side experience.

### Q8 ⭐⭐⭐ 🟡 Healthcare: A ward deterioration model sees 80 real deterioration events a day and nurses can respond to at most 100 alerts a day. At the current threshold it raises 600 alerts a day and 60 of them are real events, while at a stricter threshold it raises 100 alerts and 40 are real events (per day, from a retrospective replay). Compute sensitivity and positive predictive value at both thresholds and the precision of the extra 500 alerts, then say which threshold you would recommend and who must agree.
**Asked at:** Clinical-ML deployment material (a physician-oriented dataset-shift article, an arXiv paper on what clinicians want from explainable ML, a JMIR paper on alarm fatigue and a circEWS slide deck on calibration and prevalence); research and secondary sources rather than interview banks; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The current threshold has sensitivity 75% and positive predictive value 10% but raises 600 alerts for a capacity of 100; the strict one has sensitivity 50% and PPV 40% with 100 alerts, and the extra 500 alerts are only 4% precise (20 events), so I would recommend the strict threshold for interrupting alerts plus a quiet lower tier, subject to sign-off from clinical safety, nursing and ward clinicians.

**Clarifying questions:**
- Is the stricter alert set a subset of the current one (the same score, a higher cutoff)? The 4% precision of the extra 500 assumes yes.
- What happens to the 40 events the strict threshold misses: are they caught by existing early-warning scores or clinical rounds? The real cost of a miss is what the ward does not already catch.
- How is a "real event" defined, and how much lead time do alerts give? An alert 10 minutes before an event is worth far less than one 6 hours before.
- Is the 100-alert capacity per day for the whole ward, per nurse, or per shift? It sets the real cap.
- Were the replay numbers computed on data the model never saw? A retrospective replay overstates performance when thresholds are tuned on the same period.

**Approach:**
1. Current threshold: sensitivity = 60 / 80 = 75%; PPV = 60 / 600 = 10%, so 10 alerts per event caught. It is 6 times over the capacity of 100.
2. Strict threshold: sensitivity = 40 / 80 = 50%; PPV = 40 / 100 = 40%, so 2.5 alerts per event caught. It fits the capacity.
3. Marginal view: the extra 500 alerts add 60 - 40 = 20 events, a precision of 4%. That is 25 alerts per additional event, for 25 nurse actions per additional event found.
4. What capacity means: if nurses can answer only 100 of 600 alerts in arbitrary order, they reach about 10 events (12.5% sensitivity), worse than the strict threshold's 40. If they answer in score order they get the same 40. An unmanageable alert list is not really a high-sensitivity system.
5. Recommend the strict threshold as the interrupting tier now, and show the other 500 in a non-interrupting worklist (or use them to widen observation) if the ward can afford it.
6. Before go-live: run in silent mode on live data for a few weeks, compare the 40 missed events with other detection routes, and review alert fatigue after launch.
7. Who must agree: the clinical lead and patient-safety officer (accept the risk of the missed events), ward nursing leadership (workload and escalation rules), the hospital's clinical governance or AI committee, and the compliance or regulatory-facing team on how the tool is classified.

**Metrics:**
- Sensitivity = real events alerted / real events. PPV = real events among alerts / alerts. Alerts per event caught = 1 / PPV.
- Marginal precision = extra real events / extra alerts = 20 / 500.
- Guardrails: median time from alert to action, share of alerts acted on, missed events reviewed by clinicians, response time for the top-priority alerts, and nurse-reported alert burden.

**Risks:**
- Subset assumption: if the strict alerts are not nested in the current ones, the 4% number is wrong.
- A retrospective replay is optimistic; live PPV is usually lower (alerts change behaviour, which itself changes outcomes).
- Missing 40 of 80 events a day is a large clinical cost if nothing else catches them.
- Alert fatigue: at 10% PPV nurses learn to ignore alerts, and the real events in the list are lost too.

**What the interviewer scores:**
- Strong: 75%, 10%, 50%, 40% and 4% correctly, and the capacity point (6 times over). Weak: picks "higher sensitivity" without noticing capacity.
- Strong: a recommendation with a safety net (tiers, silent mode, review of misses). Weak: "tune the threshold".
- Strong: names the owners (clinical safety, nursing, governance, compliance) and does not decide alone.
- Strong: asks about nesting and lead time.

**Example:** (illustrative numbers)
- Weak: "The current threshold catches 60 events and the strict one only 40, so keep the current one."
- Strong: "The current threshold catches 60 of 80 events but fires 600 alerts for 100 slots, so nurses will see only about 10 events if they pick at random. The strict threshold finds 40 of 80 with 100 alerts, 40% right. The extra 500 alerts are 4% right. I would start with the strict one, put the rest on a quiet worklist, and ask clinical safety to review the 40 misses."

**Code:**
```python
import numpy as np
# Q8 ward alerts: illustrative per-day replay numbers
events, cap = 80, 100
cur_alerts, cur_tp = 600, 60
str_alerts, str_tp = 100, 40
sens_c, ppv_c = cur_tp / events, cur_tp / cur_alerts
sens_s, ppv_s = str_tp / events, str_tp / str_alerts
extra_alerts, extra_tp = cur_alerts - str_alerts, cur_tp - str_tp
ppv_extra = extra_tp / extra_alerts
print(f"current: sens {sens_c:.0%}, PPV {ppv_c:.0%}, alerts per event caught {cur_alerts/cur_tp:.0f}, over capacity by {cur_alerts/cap:.0f}x")
print(f"strict : sens {sens_s:.0%}, PPV {ppv_s:.0%}, alerts per event caught {str_alerts/str_tp:.1f}")
print(f"extra {extra_alerts} alerts hold {extra_tp} events: precision {ppv_extra:.0%}; missed events {events-cur_tp} vs {events-str_tp}")
# nurses can act on 100 of the 600 current alerts. Compare in-score-order versus arbitrary order (assumes strict alerts are the top 100 of the 600)
tp_random_order = cap * cur_tp / cur_alerts
tp_score_order = str_tp
print(f"events reached with 100 responses: arbitrary order {tp_random_order:.0f} (sens {tp_random_order/events:.1%}), score order {tp_score_order} (sens {tp_score_order/events:.0%})")
# simulate: do nurses answering a random 100 of 600 behave like a threshold at 100? (seeded)
rng = np.random.default_rng(3)
hits = []
for _ in range(2000):
    flags = np.zeros(cur_alerts, bool); flags[:cur_tp] = True
    seen = rng.permutation(cur_alerts)[:cap]
    hits.append(flags[seen].sum())
print(f"simulated events reached under random response: mean {np.mean(hits):.2f}")
assert (sens_c, sens_s) == (0.75, 0.5) and (ppv_c, ppv_s) == (0.10, 0.40)
assert (extra_alerts, extra_tp) == (500, 20) and round(ppv_extra, 2) == 0.04
assert cur_alerts / cap == 6 and cur_alerts / cur_tp == 10 and str_alerts / str_tp == 2.5
assert tp_random_order == 10 and tp_score_order == 40 and events - cur_tp == 20 and events - str_tp == 40
assert abs(np.mean(hits) - 10) < 0.3
```

**Output (my run):**
```text
current: sens 75%, PPV 10%, alerts per event caught 10, over capacity by 6x
strict : sens 50%, PPV 40%, alerts per event caught 2.5
extra 500 alerts hold 20 events: precision 4%; missed events 20 vs 40
events reached with 100 responses: arbitrary order 10 (sens 12.5%), score order 40 (sens 50%)
simulated events reached under random response: mean 9.96
```

**Follow-ups:**
- How would you pick a threshold without the 100 cap? Price a missed event against a nurse action and pick where the marginal value of an alert equals its cost.
- What if the ward can add staff? Then the capacity changes and the middle threshold may be right; recompute with the new capacity and agree it with nursing.

**Common mistakes:** Choosing by sensitivity alone. Ignoring the capacity. Reading 4% precision without the subset assumption. Treating a replay as live performance. Deciding alone.

### Q9 ⭐⭐⭐ 🟡 Ads: A campaign has a daily budget of 24,000 and without pacing it spends 15,000 by 09:00 at a cost per conversion of 30, while the remaining 9,000 is spent after 09:00 at a cost per conversion of 20 (measured yesterday). Moving 6,000 of the early spend to the later period would change conversions by how many if the later cost per conversion stayed at 20, which is an optimistic upper bound? Say why that cost might not stay at 20 and how a pacing controller would use feedback.
**Asked at:** Ad-serving system-design material (techinterview.org ad serving and real-time bidding pages, a Dataford question on budget pacing and frequency capping, machinelearningatscale.com on frequency capping; feedback-controller pacing, per-user counters and credits for invalid clicks appear in the snippets); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Moving 6,000 from a cost per conversion of 30 to 20 loses 200 conversions and gains 300, so +100 (950 to 1,050, +10.5%), but that is an optimistic upper bound because 20 is an average over spend that was already won, not the price of the next 6,000; a pacing controller would steer spend by feedback and I would measure the marginal cost rather than assume it.

**Clarifying questions:**
- Is the 20 an average over all 9,000 spent after 09:00, or the price at the margin? Extra spend buys the next-best traffic, which costs more.
- Is there enough later inventory to absorb 15,000 instead of 9,000? If demand after 09:00 is limited, the budget cannot be spent.
- Is the 30 early cost per conversion driven by the first hours of expensive traffic? If the 6,000 removed was the worst early spend, we lose fewer than 200 conversions.
- Are conversions delayed? If they arrive hours or days later, yesterday's 20 and 30 are incomplete and feedback is slow.
- Does the advertiser care about total conversions or a cost target? It changes whether a rise in cost per conversion is acceptable.

**Approach:**
1. Baseline: 15,000 / 30 = 500 conversions early plus 9,000 / 20 = 450 later = 950.
2. Move 6,000: early 9,000 / 30 = 300, later 15,000 / 20 = 750, total 1,050. Net +100, +10.5%.
3. Break-even rule: moving pays only if the later marginal cost per conversion is below the early marginal cost. At 25 the gain is 240 (net +40), at 30 net zero, at 35 net -29.
4. Say why 20 may not hold: diminishing returns in the same audience, more competition for the same traffic, a different audience mix at a later hour, and the platform's learning. Also the removed early 6,000 was probably the most expensive part of the 30, which helps the case.
5. Pacing controller: choose a planned spend curve from the expected traffic and conversion value by hour; every few minutes compare actual cumulative spend with the plan; adjust the bid multiplier or the share of auctions entered (throttle) in proportion to the gap; clip changes and add a hard stop at the budget.
6. Feedback on cost per conversion is slower, so control spend fast and adjust the plan's shape slowly from measured conversion rates by hour.
7. Verify with an A/B test of pacing against no pacing on whole campaigns, reading conversions, cost per conversion and budget use.

**Metrics:**
- Conversions = spend / cost per conversion, by period. Marginal cost per conversion = extra spend / extra conversions.
- Pacing error = actual cumulative spend - planned cumulative spend; budget used = total spend / daily budget.
- Guardrails: share of budget unspent, cost per conversion against the target, and delivery of impressions and conversions by hour.

**Risks:**
- Treating an average as a marginal price; the 1,050 can turn into a loss.
- Underspend: later hours may not absorb the money (my toy model leaves 553 unspent).
- A controller can oscillate if the gain is high, and delayed conversions mean it reacts to old information.
- Early hours may convert better for some products; a flat plan is not always best.

**What the interviewer scores:**
- Strong: 950, 1,050, +100, and the break-even logic "later marginal cost must be below early marginal cost". Weak: stops at +100.
- Strong: lists specific reasons 20 will not hold. Weak: "it will be similar".
- Strong: describes a feedback loop (target curve, error, bid multiplier or throttle, clipping, stop). Weak: "spread the budget evenly".
- Strong: separates fast control (spend) from slow outcomes (conversions).

**Example:** (illustrative numbers)
- Weak: "Move 6,000 and we gain 100 conversions."
- Strong: "950 now, at most 1,050 after, but only if the next 6,000 buys at 20. If the marginal cost later is 30 we gain nothing, and at 35 we lose 29. In my toy simulation a controller that holds 9,000 by 09:00 reaches 1,023 when the cost never moves, but only 878 when cost per conversion rises with the bid, so I would test it with a holdout and read the marginal cost."

**Code:**
```python
import numpy as np
# Part A: prompt arithmetic (illustrative, measured yesterday)
early_spend, late_spend, cpa_e, cpa_l, move = 15_000, 9_000, 30, 20, 6_000
conv0 = early_spend / cpa_e + late_spend / cpa_l
lost = move / cpa_e
gained = move / cpa_l
conv1 = conv0 - lost + gained
print(f"unpaced conversions {conv0:.0f}; move {move:,}: lose {lost:.0f} at 30, gain {gained:.0f} at 20, net {gained-lost:+.0f} -> {conv1:.0f} ({(conv1/conv0-1):.1%})")
for x in (20, 25, 30, 35):
    print(f"  later marginal CPA {x}: gain {move/x:.0f}, net {move/x - lost:+.0f}")
for e in (30, 40):
    print(f"  early marginal CPA of the removed spend {e}: lose {move/e:.0f}; break-even later marginal CPA {e}")
assert conv0 == 950 and lost == 200 and gained == 300 and conv1 == 1050 and round(conv1 / conv0 - 1, 4) == 0.1053
assert round(move / 25) == 240 and round(move / 35) == 171 and move / 40 == 150 and early_spend + late_spend == 24_000

# Part B: a feedback pacing controller on an invented hourly day. Unpaced spend = 15,000 in hours 0-8 and 9,000 in hours 9-23.
budget = 24_000
base = np.array([15_000 / 9] * 9 + [9_000 / 15] * 15)
cpa_base = np.array([30.0] * 9 + [20.0] * 15)
plan = np.arange(1, 25) * budget / 24              # even-spend plan: 1,000 per hour, so 9,000 by 09:00 (6,000 moved)
def day(k_cpa, gain=0.15, k_spend=1.5):
    m = 1.0; spent = 0.0; conv = 0.0; by9 = 0.0
    for h in range(24):
        err = (plan[h] - spent) / (budget / 24)    # hours of spend we are behind plan (negative = ahead)
        m = float(np.clip(m * (1 + gain * err), 0.3, 3.0))
        s = min(base[h] * m ** k_spend, budget - spent)   # invented: spend grows as m^1.5
        c = s / (cpa_base[h] * m ** k_cpa)                # invented: CPA grows as m^k_cpa (0 = CPA never moves)
        spent += s; conv += c
        if h == 8: by9 = spent
    return by9, spent, conv
rows = {k: day(k) for k in (0.0, 0.3, 0.6, 1.0)}
for k, (b9, sp, cv) in rows.items():
    print(f"CPA elasticity {k:.1f}: spent by 09:00 {b9:,.0f}, day spend {sp:,.0f}, conversions {cv:,.0f}")
print("takeaway: the 1,050 bound needs the later CPA to stay at 20 AND the later hours to absorb 15,000; otherwise pacing can lose conversions")
assert all(8_500 < r[0] < 9_500 for r in rows.values())            # controller does hold early spend near 9,000
assert rows[0.0][2] > 950                                          # with a flat CPA, moving spend helps
assert rows[0.0][2] < 1050 + 1e-6                                  # but never above the optimistic bound
assert rows[0.0][2] > rows[0.3][2] > rows[0.6][2] > rows[1.0][2]   # a rising CPA eats the gain
assert rows[0.6][2] < 950 < 1050                                   # at this elasticity pacing loses conversions
assert round(rows[0.0][2]) == 1023 and round(rows[0.6][2]) == 878 and round(budget - rows[0.6][1]) == 553
```

**Output (my run):**
```text
unpaced conversions 950; move 6,000: lose 200 at 30, gain 300 at 20, net +100 -> 1050 (10.5%)
  later marginal CPA 20: gain 300, net +100
  later marginal CPA 25: gain 240, net +40
  later marginal CPA 30: gain 200, net +0
  later marginal CPA 35: gain 171, net -29
  early marginal CPA of the removed spend 30: lose 200; break-even later marginal CPA 30
  early marginal CPA of the removed spend 40: lose 150; break-even later marginal CPA 40
CPA elasticity 0.0: spent by 09:00 8,981, day spend 23,447, conversions 1,023
CPA elasticity 0.3: spent by 09:00 8,981, day spend 23,447, conversions 928
CPA elasticity 0.6: spent by 09:00 8,981, day spend 23,447, conversions 878
CPA elasticity 1.0: spent by 09:00 8,981, day spend 23,447, conversions 869
takeaway: the 1,050 bound needs the later CPA to stay at 20 AND the later hours to absorb 15,000; otherwise pacing can lose conversions
```

**Follow-ups:**
- Why throttle instead of raising bids? Throttling keeps cost per auction fixed but may lose good traffic; bid shading keeps reach but raises price. A mix is common, chosen by testing.
- What if conversions arrive days later? Pace on spend, forecast conversions with a lag model, and use a proxy (clicks, add-to-cart) for fast feedback.

**Common mistakes:** Using an average cost as a marginal cost. Forgetting that the budget may not be spendable later in the day. Controlling on delayed conversions only. A controller with no clipping or stop rule. Calling +10.5% a forecast.

### Q10 ⭐⭐⭐ 🟡 Fintech: A collections team can call 3,000 of 10,000 delinquent accounts a day, and the model ranks accounts by probability of payment. Among 3,000 called top-ranked accounts, 1,200 (40%) paid within 14 days, while among a random holdout of 300 top-ranked accounts that were not called, 105 (35%) paid on their own. An incremental payment is worth 8,000 and a call costs 150, so compute the incremental payments in the called group and the net value, and explain why the model should be built for the effect of calling rather than for payment probability.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to collections prioritisation and uplift modelling in credit-risk material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Calling lifted payment from 35% to 40%, so about 3,000 x 5% = 150 incremental payments, worth 1,200,000 against 450,000 of call cost, a net of 750,000; but the 300-account holdout makes the 5 points noisy (95% interval about -0.7 to +10.7 points), and the model should be built to predict the effect of a call, not the chance of payment, because high-probability payers would often pay anyway.

**Clarifying questions:**
- Was the 300-account holdout chosen at random from the same top-ranked pool and kept uncalled for the full 14 days? Without that, the 35% is not a valid comparison.
- Are there other contacts (SMS, email, app notifications) reaching the holdout? Then 35% includes other treatment.
- Does an incremental payment also include the timing effect (paying earlier) or only paying at all? Value per payment depends on it.
- Is 150 per call the full cost, including agent time and any customer complaint cost?
- Is there a contact-policy limit on the number of calls an account may receive? The collections team should say what is allowed and who owns that policy; I would ask them rather than assume.

**Approach:**
1. Called group: 3,000 x 40% = 1,200 paid. Holdout: 300 x 35% = 105 paid.
2. Uplift = 40% - 35% = 5 points. Incremental payments among the called = 3,000 x 0.05 = 150. The other 1,050 would have paid anyway.
3. Value = 150 x 8,000 = 1,200,000. Cost = 3,000 x 150 = 450,000. Net = 750,000, or 250 per call.
4. Break-even uplift = 150 / 8,000 = 1.875 points. The observed 5 points clears it, but only just once noise is shown.
5. Noise: standard error = sqrt(0.4 x 0.6 / 3,000 + 0.35 x 0.65 / 300) = 2.90 points, so 95% interval about -0.7 to +10.7 points: incremental payments from about -20 to 320, net from about -612,000 to 2,112,000. A holdout of 300 cannot confirm the gain.
6. Why model the effect: the model ranks by probability of payment, so it sends calls to accounts that pay anyway (35% do). Money is made on accounts where the call changes the outcome: the persuadables. Rank by predicted uplift = P(pay | call) - P(pay | no call).
7. How: keep a randomised holdout of 10% to 30% of the call-eligible pool permanently, train two models or an uplift model on randomised data, evaluate with an uplift or Qini curve on a random test slice, and refresh.

**Metrics:**
- Uplift = payment rate (called) - payment rate (not called). Incremental payments = called x uplift.
- Net value = incremental payments x value - calls x cost. Break-even uplift = cost per call / value per incremental payment.
- Guardrails: complaints per 1,000 calls, contact-policy breaches, payment size and timing, and the holdout's size and balance.

**Risks:**
- Small holdout: 105 of 300 can easily be 95 or 115 by chance.
- The holdout is among top-ranked accounts only, so 5 points does not say what a call does to lower-ranked ones.
- Calls change who pays when: pull-forward is not a new payment.
- Uplift models are noisy; with few accounts they can rank worse than a simple rule.

**What the interviewer scores:**
- Strong: 150, 1,200,000, 450,000, 750,000 and the break-even uplift. Weak: counts all 1,200 payments as the call's benefit.
- Strong: puts an interval on the 5 points and says 300 is small. Weak: no uncertainty.
- Strong: explains persuadables versus sure-things in plain words and says how to train on randomised data. Weak: "use a better classifier".
- Strong: asks the collections and compliance teams about contact rules.

**Example:** (illustrative numbers)
- Weak: "1,200 accounts paid, so calls earned 9.6 million."
- Strong: "35% would have paid anyway, so only 5 points, about 150 accounts, are ours. That is 1.2 million of value for 450,000 of calls, net 750,000, but the interval on 5 points is wide because the holdout has 300 accounts. In my simulation, ranking by uplift found about 3.7 times as many incremental payments as ranking by payment probability for the same 3,000 calls. I would keep a bigger permanent holdout and rank by uplift."

**Code:**
```python
import numpy as np
# Part A: prompt arithmetic (illustrative). Called 3,000 -> 40% paid; random holdout of 300 not called -> 35% paid.
nc, pc, nh, ph = 3_000, 0.40, 300, 0.35
paid_called = nc * pc
paid_hold = nh * ph
uplift = pc - ph
incr = nc * uplift
value, cost = 8_000, 150
net = incr * value - nc * cost
be_uplift = cost / value
se = (pc * (1 - pc) / nc + ph * (1 - ph) / nh) ** 0.5
lo, hi = uplift - 1.96 * se, uplift + 1.96 * se
print(f"paid called {paid_called:.0f}, paid holdout {paid_hold:.0f}; uplift {uplift:.1%}; incremental payments {incr:.0f}")
print(f"value {incr*value:,.0f} - call cost {nc*cost:,} = net {net:,.0f}; break-even uplift {be_uplift:.3%}")
print(f"SE of the 5-point gap {se*100:.2f} points; 95% interval {lo*100:.1f} to {hi*100:.1f} points -> incremental payments {nc*lo:.0f} to {nc*hi:.0f}, net {nc*lo*value-nc*cost:,.0f} to {nc*hi*value-nc*cost:,.0f}")
learn_cost = nh * uplift * value - nh * cost   # expected value given up by not calling the 300 (value of their uplift minus calls saved)
print(f"expected cost of keeping 300 uncalled: {learn_cost:,.0f}")
assert paid_called == 1200 and paid_hold == 105 and round(uplift, 6) == 0.05 and round(incr) == 150
assert round(incr * value) == 1_200_000 and nc * cost == 450_000 and round(net) == 750_000 and round(be_uplift, 5) == 0.01875
assert round(se * 100, 2) == 2.90 and lo < 0 < hi
assert round(nc * lo) == -20 and round(nc * hi) == 320 and round(learn_cost) == 75_000

# Part B: rank by P(pay) versus rank by uplift on synthetic accounts (seeded). Random calls on half the accounts give the training data.
rng = np.random.default_rng(21)
N, K = 10_000, 3_000
x1 = rng.random(N)                              # 'ability to pay' (drives baseline payment)
x2 = rng.random(N)                              # 'persuadability' (drives the effect of a call)
base_p = 0.05 + 0.75 * x1 ** 2                 # sure-things at high x1
eff = 0.30 * np.exp(-6 * (x1 - 0.35) ** 2) * x2  # calls matter most at middling x1 and high x2 (invented)
p_call = np.clip(base_p + eff, 0, 0.97)
# training data: 200,000 randomised past accounts, called with probability 0.5
M = 200_000
t1, t2 = rng.random(M), rng.random(M)
tb = 0.05 + 0.75 * t1 ** 2; te = 0.30 * np.exp(-6 * (t1 - 0.35) ** 2) * t2
tr = rng.random(M) < 0.5
pay = rng.random(M) < np.clip(tb + te * tr, 0, 0.97)
g = 10
cell = (np.minimum((t1 * g).astype(int), g - 1)) * g + np.minimum((t2 * g).astype(int), g - 1)
est_up = np.zeros(g * g); est_p = np.zeros(g * g)
for c in range(g * g):
    m = cell == c
    est_up[c] = pay[m & tr].mean() - pay[m & ~tr].mean()          # T-learner by cell
    est_p[c] = pay[m & tr].mean()                                 # what a P(pay | called) model learns
acell = (np.minimum((x1 * g).astype(int), g - 1)) * g + np.minimum((x2 * g).astype(int), g - 1)
def evaluate(score):
    top = np.argsort(-score)[:K]
    gain = (p_call[top] - base_p[top]).sum()                      # expected incremental payments (true effect)
    return gain, gain * value - K * cost
g_p, n_p = evaluate(est_p[acell]); g_u, n_u = evaluate(est_up[acell]); g_o, n_o = evaluate(eff)
print(f"call the top 3,000 ranked by P(pay): {g_p:.0f} incremental payments, net {n_p:,.0f}")
print(f"call the top 3,000 ranked by estimated uplift: {g_u:.0f} incremental payments, net {n_u:,.0f} (oracle {g_o:.0f})")
assert g_u > g_p * 1.3 and n_u > n_p
assert g_u > 0.85 * g_o
assert round(g_u / g_p, 1) == 3.7
```

**Output (my run):**
```text
paid called 1200, paid holdout 105; uplift 5.0%; incremental payments 150
value 1,200,000 - call cost 450,000 = net 750,000; break-even uplift 1.875%
SE of the 5-point gap 2.90 points; 95% interval -0.7 to 10.7 points -> incremental payments -20 to 320, net -611,996 to 2,111,996
expected cost of keeping 300 uncalled: 75,000
call the top 3,000 ranked by P(pay): 156 incremental payments, net 797,209
call the top 3,000 ranked by estimated uplift: 572 incremental payments, net 4,129,306 (oracle 584)
```

**Follow-ups:**
- What does a holdout cost? Not calling 300 accounts gives up about 15 incremental payments (120,000) and saves 45,000 of calls, an expected cost of 75,000, which is the price of knowing the truth.
- What if calls sometimes hurt (accounts that get angry)? Uplift can be negative; an uplift model finds them and stops calling them.

**Common mistakes:** Crediting all payments to the call. Ranking by P(pay) and calling it optimal. A tiny holdout and no interval. Training uplift on non-random call history. Ignoring the call cost per account.
