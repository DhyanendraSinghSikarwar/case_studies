# Book 6 — Part 9: Domain Sets (Fintech, E-commerce, Healthcare, Ads)

**Topic:** Domain-specific scenarios that only make sense inside one industry, for Data Scientist and ML Engineer loops. Fintech: credit scoring and thin-file applicants, reject inference, cutoff and profit trade-offs, payments fraud and step-up friction, KYC and AML alert triage, collections prioritisation, chargeback label noise, explainability for lenders, PD calibration and model-risk governance in general terms. E-commerce: search position bias, zero-result queries, cold-start sellers, censored demand and pricing cannibalisation, delivery promise, cart abandonment, fake reviews, size recommendation and returns, catalogue quality, seller trust and recommendation diversity. Healthcare: prevalence shift and positive predictive value, alarm fatigue and thresholds, clinician override and trust, label agreement, scanner and site bias, multi-hospital validation, consent and re-identification, LLM documentation audits, treatment-contaminated labels and change control. Ads: CTR calibration and bids, budget pacing, invalid traffic, signal loss and noisy reporting, frequency capping, cold-start campaigns, lookalike incrementality, delayed conversions, first-price bidding, geo lift versus last-click and creative selection.

**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 16, ⭐⭐ 23, ⭐ 11; Fintech 13, E-commerce 13, Healthcare 12, Ads 12)  |  **Date:** 2026-10-31  |  **Status:** Complete (answers merged, checked, reviewed)

**Scope note:** this part is the domain angle: each scenario combines metrics, modelling, risk and (where relevant) compliance in the setting of one industry, with numbers that can be reproduced in code (base rates, positive predictive value, cost matrices, calibration, incrementality). General metric drops, degradation, imbalance, experiments, business cases, stakeholder trade-offs, GenAI and MLOps incidents belong to Book 6 Parts 1 to 8; Wave B answers should cross-reference those only by checked headings. All numbers in the prompts are invented illustrative numbers, not data from any company, and money is in one unnamed currency unit. Every percentage names its base and says relative or absolute where it matters, rates are labelled as measured samples or projections, and every arithmetic claim is checked in scratch/B6P09_wavea/qs.py. Anything touching law, regulation or clinical rules is framed as a question for compliance, the privacy officer or the regulatory team, and no legal or regulatory claim is made as fact. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part09_sources.md). Searches returned fintech and credit-scoring prep guides and reject-inference pages, UPI-fraud papers, e-commerce company question lists, fake-review items, clinical-AI validation coverage and ad-tech question pages. None tied a scenario to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page for the exact framing. Search coverage was thin for KYC and AML, collections, delivery promise, demand forecasting, size recommendation, device bias, invalid traffic and signal loss. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

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

### Q4 ⭐⭐⭐ 🟢 Ads: A click model predicts an average click-through rate of 3.0% on 1,000,000 impressions, but 24,000 clicks were observed, an observed rate of 2.4% (a measured day). The AUC is unchanged and advertisers bid a value per click of 10, so the bid per impression is the predicted rate times 10. Compute the bid per impression with and without the error and the relative overbid compared with the calibrated bid, and explain why a good AUC does not protect you here and how you would fix it.
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

### Q6 ⭐⭐⭐ 🟡 Fintech: A lender gets 100,000 applications a month and 30,000 of them (30% of applications) are thin-file with no bureau score, and its model has an AUC of 0.82 on thick-file applicants but 0.66 on thin-file ones. A pilot would approve 2,000 extra thin-file applicants a month with a credit limit of 5,000 each, a profit of 1,200 per repaying customer and a loss of 4,000 per defaulter. Compute the exposure of the pilot as an upper bound on balances at risk (all limits fully drawn, no recovery) and the break-even default rate, and explain what data, controls and review you would use.
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The pilot's exposure is at most 2,000 x 5,000 = 10,000,000 if every limit is fully drawn with no recovery, and it breaks even at a default rate of 1,200 / (1,200 + 4,000) = 23.1%; with an AUC of only 0.66 I would run it as a capped, staged, partly randomised pilot with a hard loss budget, agreed with risk, compliance and model validation.

**Clarifying questions:**
- What default rate do thin-file customers show today, and on what definition (90 days past due within 12 months)? The break-even of 23.1% means little without the expected rate.
- Is the 4,000 loss per defaulter after partial drawing and recovery, or a gross figure? The balances-at-risk bound assumes no recovery and the 8,000,000 maximum loss uses the stated 4,000, so I would ask finance how much is drawn and recovered.
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

### Q7 ⭐⭐⭐ 🟡 E-commerce: New sellers make up 8% of live listings but receive 2% of search impressions, because the ranker favours listings with a conversion history. The team wants to reserve 5% of 10,000,000 daily search impressions for exploration, in addition to the 2% they already get, where new listings are assumed to convert at 2.0% per impression against 3.0% for the normal ranking (a projection). Compute the daily orders given up by the exploration budget in absolute and relative terms, and say how you would run the exploration and judge whether it is worth it.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to cold-start in marketplace search and recommendation system-design material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Reserving 5% of 10,000,000 impressions gives up about 5,000 orders a day, 1.67% of the 300,000 the normal ranking would produce, if new listings really convert at 2.0% against 3.0%; I would pay that as an information budget, run it as a capped adaptive explore on a randomised slice, and judge it on whether the seller-side and long-run gains beat the cost.

**Clarifying questions:**
- Does exploration keep the existing 2% for new sellers? The prompt says the 5% is in addition, so the full 500,000 impressions are extra; I would still confirm how it is logged.
- Where does the 2.0% come from? It is a projection; at 1.5% the cost is 7,500 orders (2.5%) and at 2.5% it is 2,500 (0.83%).
- How many new listings per day and how fast do they get a first sale? It sets how deep each listing can be explored.
- Are the lost orders really lost, or does the buyer buy a similar item elsewhere on the site? Gross versus net.
- What is the goal: seller retention, catalogue breadth, or finding future winners? Each has a different success metric.

**Approach:**
1. The cost: 5% x 10,000,000 = 500,000 impressions. At 2.0% they give 10,000 orders; at the normal 3.0% they would give 15,000. Lost = 5,000 orders a day, 5,000 / 300,000 = 1.67% relative.
2. State the base: 300,000 orders assumes all 10,000,000 impressions convert at 3.0%; the true baseline is slightly lower because the 2% already going to new sellers converts less.
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
- Strong: 5,000 orders, 1.67%, with the 3.0% base stated. Weak: "it costs 5%".
- Strong: states that cost is not the same as value and names what is bought. Weak: no benefit measure.
- Strong: adaptive exploration with a cap per listing and a randomised holdout. Weak: "boost all new listings".
- Strong: labels 2.0% as a projection and shows a range.

**Example:** (illustrative numbers)
- Weak: "Exploration costs 5% of impressions, so 5% fewer orders."
- Strong: "500,000 impressions at 2.0% give 10,000 orders instead of 15,000. That is 5,000 a day, 1.67% of the 300,000 we would make. In my simulation, Thompson-style allocation gave about 26% more orders from the same exploration budget than uniform allocation and picked better listings. I would run it with caps on a randomised slice and judge it on first sales and seller retention."

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

### Q8 ⭐⭐⭐ 🟡 Healthcare: A ward deterioration model sees 80 real deterioration events a day and nurses can respond to at most 100 alerts a day. At the current threshold it raises 600 alerts a day and 60 of them are real events, while at a stricter threshold it raises 100 alerts and 40 are real events (per day, from a retrospective replay, with the stricter alerts a subset of the current alerts). Compute sensitivity and positive predictive value at both thresholds and the precision of the extra 500 alerts, then say which threshold you would recommend and who must agree.
**Asked at:** Clinical-ML deployment material (a physician-oriented dataset-shift article, an arXiv paper on what clinicians want from explainable ML, a JMIR paper on alarm fatigue and a circEWS slide deck on calibration and prevalence); research and secondary sources rather than interview banks; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The current threshold has sensitivity 75% and positive predictive value 10% but raises 600 alerts for a capacity of 100; the strict one has sensitivity 50% and PPV 40% with 100 alerts, and the extra 500 alerts are only 4% precise (20 events), so I would recommend the strict threshold for interrupting alerts plus a quiet lower tier, subject to sign-off from clinical safety, nursing and ward clinicians.

**Clarifying questions:**
- The prompt makes the stricter alerts a subset of the current ones (same score, higher cutoff); is that how the replay was run? The 4% precision of the extra 500 depends on it.
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
- The 4% number holds only because the strict alerts are a subset of the current ones; a different model would change it.
- A retrospective replay is optimistic; live PPV is usually lower (alerts change behaviour, which itself changes outcomes).
- Missing 40 of 80 events a day is a large clinical cost if nothing else catches them.
- Alert fatigue: at 10% PPV nurses learn to ignore alerts, and the real events in the list are lost too.

**What the interviewer scores:**
- Strong: 75%, 10%, 50%, 40% and 4% correctly, and the capacity point (6 times over). Weak: picks "higher sensitivity" without noticing capacity.
- Strong: a recommendation with a safety net (tiers, silent mode, review of misses). Weak: "tune the threshold".
- Strong: names the owners (clinical safety, nursing, governance, compliance) and does not decide alone.
- Strong: asks about lead time and how the replay was run.

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

**Common mistakes:** Choosing by sensitivity alone. Ignoring the capacity. Reading 4% precision without remembering it relies on nested thresholds. Treating a replay as live performance. Deciding alone.

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

### Q10 ⭐⭐⭐ 🟡 Fintech: A collections team can call 3,000 of 10,000 delinquent accounts a day, and the model ranks accounts by probability of payment. Among 3,000 called top-ranked accounts, 1,200 (40%) paid within 14 days, while among a random holdout of 300 top-ranked accounts that were not called, 105 (35%, a small holdout) paid on their own. An incremental payment is worth 8,000 and a call costs 150, so compute the incremental payments in the called group and the net value, and explain why the model should be built for the effect of calling rather than for payment probability.
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

### Q11 ⭐⭐⭐ 🟡 Healthcare: In a pilot, 1,000 high-risk alerts were raised and clinicians overrode 700 of them. Of the 700 overridden alerts, 35 were followed by a deterioration event, and of the 300 acted-on alerts, 90 were followed by one (counts from a measured pilot). Compute the share of all alerts followed by an event and the share of alert-followed events that were in acted-on alerts, and explain why you should not conclude that clinicians are simply right or wrong, and what you would do about trust.
**Asked at:** Clinical-ML deployment material (a physician-oriented dataset-shift article, an arXiv paper on what clinicians want from explainable ML, a JMIR paper on alarm fatigue and a circEWS slide deck on calibration and prevalence); research and secondary sources rather than interview banks; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** 12.5% of alerts were followed by an event and 72% of alert-followed events sat in acted-on alerts, but override versus event is confounded by selection and by treatment, so I would not call clinicians right or wrong; I would compare within risk strata, read the overridden cases with clinicians, and fix the alert itself.

**Clarifying questions:**
- What counts as an event, and over what window (6, 12, 24 hours)? A longer window makes every rate larger and blurs cause.
- What does "acted on" mean (a documented intervention, a call, a bedside review)? If it is not logged, "acted" is partly inferred.
- Are there events with no alert at all? The 72% is among alert-followed events; events the model missed are not in these counts, so track them separately.
- Did clinicians see the risk score or a reason? An override with no information about why is hard to learn from.
- Is there a fixed threshold, or do some wards get different alerts? Alert volume per nurse drives overrides.

**Approach:**
1. Do the arithmetic. 90 + 35 = 125 events in 1,000 alerts, so 12.5% of alerts were followed by an event. 90 / 125 = 72% of alert-followed events were in acted-on alerts. Event rate was 30% in acted alerts and 5% in overridden ones.
2. Say what these do not show. Clinicians choose which alerts to act on, so acted alerts are the sicker-looking ones (selection). Acting also tries to prevent the event, so the 30% is already after treatment (contamination). Both push in opposite directions. The 5% in overridden alerts may be clinicians correctly spotting false alarms, or luck.
3. Compare like with like. Group alerts by model risk band, vital signs and ward. Within a band, compare event rate for acted versus overridden. If overridden alerts in the same band have the same event rate as acted ones, the override looks like noise. If they are clearly lower, clinicians add information the model lacks.
4. Review a sample. Have clinicians read 35 overridden alerts followed by an event (the possible misses) and a random 35 of the 665 that were not (the correct overrides). Tag the reasons: already on treatment, known patient condition, wrong patient context, alert too late.
5. Fix trust on three fronts. Show a short reason with each alert. Cut volume (see the alert-burden maths; ask the clinical safety owner for a workable alert budget). Close the loop: give each ward a monthly view of alerts, overrides and outcomes, and let them challenge it.
6. Governance. Any threshold change goes through the clinical safety group and the ward leads. Keep override reasons as a structured field, not free text only.

**Metrics:**
- Alert event rate = alerts followed by an event / all alerts = 125 / 1,000 = 12.5%.
- Share of alert-followed events in acted alerts = 90 / 125 = 72%.
- Event rate by action = events / alerts in that group: acted 30%, overridden 5%.
- Within-band event rate by action (the fair comparison); override rate by ward and by hour.
- Guardrails: events with no alert (the model's misses), time from alert to action, and alerts per nurse per shift.

**Risks:**
- Reading "overridden alerts rarely had an event" as "the model is wrong". It could mean clinicians were right, or that acting was not needed.
- Reading "acted alerts often had an event" as "clinicians act on the right ones". Acting may have prevented some events, which hides model value.
- Sample size: 35 events among 700 gives a wide interval, so small differences between wards are noise.
- Training the next model on "event after alert" as the label inflates the harm of treatment: treated patients look healthier.

**What the interviewer scores:**
- Strong: gets 12.5% and 72%, and reads the 72% as a share of alert-followed events.
- Strong: names selection and treatment contamination, and proposes a within-band comparison.
- Strong: treats trust as a product problem (reasons, volume, feedback loop), with the clinical owner deciding.
- Weak: "clinicians override 70% so the model is bad", or "events were low in overrides so clinicians are right".

**Example:** Illustrative, using the question's counts. Weak versus strong:
- Weak: "Seventy per cent were overridden and only 5% of those had events, so clinicians are right and we should lower the alert count."
- Strong: "12.5% of alerts were followed by an event, and 72% of those events were in alerts that were acted on. The 30% versus 5% gap mixes two things: clinicians pick the sicker-looking patients, and acting may prevent the event. So I would compare within risk bands, have two clinicians read the 35 overridden-then-event cases, and agree an alert budget and a reason field with the clinical safety lead before touching the threshold."

**Code:**
```python
import numpy as np

# Pilot counts (measured, from the question)
alerts, overridden, acted = 1000, 700, 300
ev_over, ev_acted = 35, 90
assert overridden + acted == alerts
ev_all = ev_over + ev_acted
share_alerts_with_event = ev_all / alerts
share_events_in_acted = ev_acted / ev_all
rate_over, rate_acted = ev_over / overridden, ev_acted / acted
assert ev_all == 125 and share_alerts_with_event == 0.125
assert round(share_events_in_acted, 3) == 0.72
assert rate_over == 0.05 and rate_acted == 0.30
print("alerts followed by an event:", share_alerts_with_event)
print("events (among alerted) that were in acted-on alerts:", round(share_events_in_acted, 3))
print("event rate overridden / acted:", rate_over, rate_acted)

# Two-proportion z (large-sample): is 30% vs 5% a real gap? Yes, but it is not the question.
p = ev_all / alerts
se = np.sqrt(p * (1 - p) * (1 / overridden + 1 / acted))
z = (rate_acted - rate_over) / se
assert z > 10
print("z for acted vs overridden event rate:", round(float(z), 1))

# Why the gap does not say who is right: a simulation with an illustrative skilled clinician.
# Latent risk r; clinician sees r plus noise and acts if the signal is high; acting cuts events by 40%.
rng = np.random.default_rng(11)
n = 1000
r = rng.beta(2, 8, n)                      # latent true risk, mean 0.2
sees = r + rng.normal(0, 0.08, n)
act = sees > np.quantile(sees, 0.70)       # clinicians act on the top 30% by their own read
prevented = rng.random(n) < 0.40
event = (rng.random(n) < r) & ~(act & prevented)
print("sim: acted share", act.mean(), "event rate acted", round(float(event[act].mean()), 3),
      "overridden", round(float(event[~act].mean()), 3))
no_action_acted = (rng.random(n) < r)[act].mean()
print("sim: acted-group event rate had nobody acted (untreated risk):", round(float(no_action_acted), 3))
assert event[act].mean() > event[~act].mean()      # acted group looks worse even though clinicians are skilled
assert no_action_acted > event[act].mean()   # acting lowered events in the acted group
```

**Output (my run):**
```
alerts followed by an event: 0.125
events (among alerted) that were in acted-on alerts: 0.72
event rate overridden / acted: 0.05 0.3
z for acted vs overridden event rate: 11.0
sim: acted share 0.3 event rate acted 0.207 overridden 0.133
sim: acted-group event rate had nobody acted (untreated risk): 0.353
```

**Follow-ups:**
- Can you measure the model's value if clinicians act on the alerts? Only partly. A randomised or staggered rollout (some wards with alerts, some without) gives the effect of the whole system; ask the clinical research and safety teams whether and how that is allowed.
- What if overrides are mostly at night? That points to workload or context; look at alerts per nurse per hour and at time-of-day thresholds with the ward leads.
- What label would you train on next? A label that does not depend on treatment, such as a physiology-based deterioration definition, or use methods that account for treatment; discuss with the clinical owner.

**Common mistakes:**
- Dividing events by 700 or 300 and calling the result "accuracy".
- Quoting 72% as the share of all deterioration events when missed events are unknown.
- Ignoring that treated patients are the ones the model flagged most strongly.
- Pushing a threshold change without the clinicians who carry the alerts.

### Q12 ⭐⭐⭐ 🟡 Ads: A publisher sends 2,000,000 clicks in a day and 200,000 of them (10% of clicks) are later classified as invalid, with the advertiser credited back for them after 3 days. The conversion rate per click is 2.0% for valid clicks and 0% for invalid clicks, so the measured blended rate is 1.8% (rates from a measured sample). Explain how training the click and conversion models on the raw clicks distorts bids, how you would handle the 3-day delay in labels, and what you would tell the publisher account team.
**Asked at:** Ad-serving system-design material (techinterview.org ad serving and real-time bidding pages, a Dataford question on budget pacing and frequency capping, machinelearningatscale.com on frequency capping; feedback-controller pacing, per-user counters and credits for invalid clicks appear in the snippets); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Raw clicks mix real users with invalid traffic, so a model trained on them learns a blended conversion rate of 1.8% instead of the 2.0% on valid clicks, and it learns a publisher's invalid share as if it were user behaviour; I would train on valid-only labels that have matured past the 3-day delay and tell the account team which numbers are provisional.

**Clarifying questions:**
- Is the credit complete and automatic (as stated), including for late flags? It confirms the bid should use the valid rate of 2.0%.
- Is the invalid flag a rule, a vendor score or manual review? Late, model-based flags change over time and need versioning.
- Does the 3-day delay apply to the invalid label only, or also to conversions (which usually arrive later)? Both censor the newest data.
- Does the invalid share differ by publisher, placement or hour? A shared share is a small bias; a varying share distorts ranking between publishers.
- What is the value per conversion and the bidding rule? We need it to price the bias.

**Approach:**
1. Do the arithmetic. 10% invalid, conversion 2.0% on valid, 0% on invalid: blended = 0.9 x 2.0% = 1.8%. With an illustrative value of 50 per conversion, the raw bid per click is 0.90 and the valid-only bid is 1.00, a 10% underbid.
2. Say which direction the bias goes. Invalid clicks are credited back, so we effectively pay only for valid ones and the right value of a click is the valid rate (2.0%). A raw-trained model underbids by 10% on average. Sensitivity in one line: if they were not credited, the blended 1.8% would be the value of what we pay for.
3. Publisher differences matter more than the average. A publisher with 2% invalid shows 1.96%, one with 30% shows 1.4%, with the same real users. The raw model punishes the second publisher for traffic quality, which is acceptable if you are billed for it and wrong if you are credited.
4. Handle the delay. A click from today has no invalid flag yet, so it looks valid and unconverted when it is invalid. Recent days therefore show a lower conversion rate than matured days (in the run, 1.71% versus 1.96% on the same traffic mix). Train on matured clicks only (age at least 3 days, plus the conversion window), or train two models: P(invalid) from matured data, and P(convert | valid).
5. Combine at serving. Expected value per click = P(valid) x P(convert | valid) x value, where P(valid) comes from a publisher and placement model. Use a conservative P(valid) for new sources.
6. Tell the account team plainly: figures from the last 3 days are provisional and usually revised; we will report valid-only conversion rate, invalid share by publisher, and the credit amount; and publishers with a high invalid share may see lower bids until their traffic matures. Route any contract or billing wording through the commercial and legal owners.

**Metrics:**
- Invalid share = invalid clicks / all clicks = 200,000 / 2,000,000 = 10%.
- Valid CVR = conversions on valid clicks / valid clicks (2.0% in the sample); blended CVR = conversions / all clicks (1.8%).
- Label maturity: share of clicks older than 3 days whose flag is final; revision rate = clicks whose label changes after first being scored.
- Calibration by publisher on matured data: predicted conversions / actual conversions per decile.
- Guardrails: spend per valid conversion, credits received per week, bid change versus last week by publisher.

**Risks:**
- Training on the newest days: the recent label bias makes the model underbid just when traffic is shifting.
- Dropping unflagged recent clicks removes the very traffic whose quality is unknown, so a new bad source looks fine until day 3.
- A model that learns "publisher B converts less" when the cause is invalid traffic will keep underbidding after the publisher cleans up.
- Sample rates (2.0%, 10%) are from a sample; check their interval before quoting them to a publisher.

**What the interviewer scores:**
- Strong: derives 1.8% from 90% x 2.0% and links the bid error to the credit-back treatment.
- Strong: names label delay as a censoring problem and trains on matured data or models the flag.
- Strong: separates invalid-traffic share (a source property) from user conversion behaviour.
- Weak: "just remove the bots"; ignoring the delay; saying the bias is always 10% for every publisher.

**Example:** Illustrative numbers, value 50 per conversion. Weak versus strong:
- Weak: "I would filter out invalid clicks and retrain on the full data."
- Strong: "On raw clicks the model sees 1.8% and bids 0.90; the valid-only rate is 2.0%, so bid 1.00, since invalid clicks are credited back. The last 3 days are not yet flagged, so I train on matured clicks, and I model the chance a click is valid per publisher. I would tell the account team that recent numbers are provisional and that bids on a high-invalid publisher will be lower until its flags settle."

**Code:**
```python
import numpy as np

clicks, invalid = 2_000_000, 200_000
cvr_valid, cvr_invalid = 0.02, 0.0
share_invalid = invalid / clicks
blended = (1 - share_invalid) * cvr_valid + share_invalid * cvr_invalid
assert share_invalid == 0.10
assert abs(blended - 0.018) < 1e-12
print("blended CVR:", round(blended, 4))

# Bids per click if value per conversion is 50 (illustrative)
value = 50
bid_raw, bid_valid = blended * value, cvr_valid * value
assert abs(bid_raw - 0.90) < 1e-9 and abs(bid_valid - 1.00) < 1e-9
print("bid raw vs valid-only:", round(bid_raw, 2), round(bid_valid, 2), "underbid", round(1 - bid_raw / bid_valid, 3))
assert abs((1 - bid_raw / bid_valid) - 0.10) < 1e-9

# Heterogeneity: two publishers, same valid CVR, different invalid share
for name, inv in [("pub A", 0.02), ("pub B", 0.30)]:
    b = (1 - inv) * cvr_valid
    print(name, "invalid", inv, "raw CVR", round(b, 4))
assert abs((1 - 0.30) * 0.02 - 0.014) < 1e-12

# Delay: classification arrives 3 days after the click. Naive training on the last days
# treats unclassified invalid clicks as valid (or drops them), so labels differ by age.
rng = np.random.default_rng(12)
days, per_day, delay = 10, 20_000, 3
day = np.repeat(np.arange(days), per_day)
is_invalid = rng.random(day.size) < share_invalid
conv = (~is_invalid) & (rng.random(day.size) < cvr_valid)
age = days - 1 - day                                   # 0 = today
known_invalid = is_invalid & (age >= delay)            # invalid label only known after 3 days
recent = age < delay
cvr_recent_naive = conv[recent].mean()                 # all recent clicks, invalid not yet flagged
cvr_recent_true_valid = conv[recent & ~is_invalid].mean()
cvr_old_valid = conv[~recent & ~known_invalid].mean()  # matured: invalid removed
print("recent days, invalid still unflagged:", round(float(cvr_recent_naive), 4))
print("recent days, true valid only:", round(float(cvr_recent_true_valid), 4))
print("matured days, invalid removed:", round(float(cvr_old_valid), 4))
assert abs(cvr_recent_naive - 0.018) < 0.002
assert abs(cvr_old_valid - 0.02) < 0.002
assert cvr_recent_naive < cvr_old_valid               # same traffic, different apparent CVR by label age

# Fix 1: train on matured clicks only (age >= delay). Fix 2: model P(invalid) and weight.
p_valid = 1 - share_invalid
corrected = cvr_recent_naive / p_valid
print("recent naive / P(valid):", round(float(corrected), 4))
assert abs(corrected - 0.02) < 0.003
```

**Output (my run):**
```
blended CVR: 0.018
bid raw vs valid-only: 0.9 1.0 underbid 0.1
pub A invalid 0.02 raw CVR 0.0196
pub B invalid 0.3 raw CVR 0.014
recent days, invalid still unflagged: 0.0171
recent days, true valid only: 0.019
matured days, invalid removed: 0.0196
recent naive / P(valid): 0.019
```

**Follow-ups:**
- How would you use the unflagged recent data? Add a P(invalid) model trained on matured clicks and weight recent clicks by predicted P(valid); do not treat them as clean.
- What if the flag rule changes mid-quarter? Version the rule, retrain per version, and re-score history so training labels are consistent.
- What if conversions also arrive late? Use a delayed-feedback approach (train only on clicks older than the conversion window, or model the delay); the general method is the same.

**Common mistakes:**
- Training on the most recent days and treating missing flags as "valid".
- Assuming the bias is the same for every publisher.
- Reporting 1.8% to the publisher as their conversion quality without separating invalid share.
- Using the blended rate for the bid when invalid clicks are credited back.

### Q13 ⭐⭐⭐ 🔴 Fintech: A lender approved 30,000 of 100,000 applicants last year (30%) and 1,200 of the approved (4%) defaulted within 12 months, measured on matured outcomes. A new model is trained only on the approved applicants and the 70,000 rejected applicants have no outcome. If rejects defaulted at 3 times the approved rate, the population default rate would be 9.6%, which is one scenario and not a measurement. Explain the bias, the reject-inference options and their limits, and what low-risk experiment would give you real outcomes on rejects.
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Training on approved applicants only teaches the model about the people the old policy liked, so it is biased and overconfident on the 70,000 rejects; reject inference can narrow the gap but not close it, and the clean fix is a small, capped, randomised approval of near-cutoff rejects to get real outcomes.

**Clarifying questions:**
- How were approvals decided: a score cutoff, rules, manual overrides? A deterministic rule on observed features is much easier to correct than a human override on unobserved information.
- Were defaults on rejects ever observed elsewhere, for example through a credit bureau record of loans they took at another lender? Whether we may use that is a question for compliance and the privacy team.
- Is the 12-month default definition fixed? A different window changes the 4% and the scenario.
- What is the downside budget: how much loss are we willing to carry for learning? It sizes the experiment.
- Which decisions will the new model drive: approve, limit, price? Each needs a different part of the risk range.

**Approach:**
1. State the arithmetic. Approved: 30,000 (30%), 1,200 defaults, 4%. If rejects defaulted at 3 times that, 12% of 70,000 = 8,400 defaults, and the population rate = (1,200 + 8,400) / 100,000 = 9.6%. That is one scenario: the ratio is not measured. With a ratio of 1 the population rate is 4%, with 5 it is 15.2% (see the run).
2. Explain the bias. The approved set is truncated on the old score, so the model sees only the low-risk end. Two consequences: its measured AUC and bad rate are for approved customers, not applicants, and it extrapolates into a region it has never seen. In the simulation a linear fit on approved applicants predicts a 6.0% default for rejects when the real rate is 10.9%.
3. List the reject-inference options and their limits. Treat rejects as bad: crude, inflates risk. Extrapolation or parcelling (score rejects with the approved-trained model and assign outcomes by band): assumes the thing you are trying to learn, so it adds no information. Augmentation or reweighting by approval probability: fixes bias only if approval depended on observed variables (a missing-at-random assumption). Use of outside outcomes (bureau data on rejects): helps if allowed and relevant. All of these need testing on a period where outcomes are known; none replaces data.
4. Run the low-risk experiment. For a small random share of near-cutoff rejects (not the riskiest), approve with a small limit and a cap on total exposure. Randomisation makes the outcomes unbiased for that band. In the run: 500 people at a limit of 1,000 is an upper bound of 500,000 of exposure and gives about +/- 1.2 points of default-rate precision at a 1.8% observed rate (illustrative).
5. Get approvals for the experiment from credit risk and compliance (fairness review, any rule on random approvals is for them to say). Pre-agree a stop rule on cumulative losses.
6. Use the results: refit on approved plus the experiment (weight the experiment by 1 / probability of selection), re-check calibration on the experimental band, and re-run the cutoff analysis. Do not extrapolate beyond the band you sampled.

**Metrics:**
- Default rate = defaults within 12 months / accounts opened, for matured cohorts only.
- Calibration by score band on the experimental slice: predicted defaults / observed defaults.
- Population AUC on a fair holdout (approved plus experimental slice, weighted), not approved-only AUC.
- Experiment guardrails: exposure = accounts x limit (upper bound, all drawn, no recovery); realised loss versus pre-agreed cap.

**Risks:**
- Treating 9.6% as the answer. It is one scenario from an assumed ratio of 3.
- The experiment covers only near-cutoff rejects; it says little about the worst 50,000.
- Selection by hidden information (an underwriter's note) cannot be corrected by reweighting on model features.
- Economic conditions change between the matured cohort and today, so a cohort result may not transfer.

**What the interviewer scores:**
- Strong: computes 9.6% and says it is one scenario with a sensitivity range.
- Strong: names truncation and extrapolation, and says inference methods rest on assumptions they cannot test alone.
- Strong: proposes a bounded, randomised exploration with a loss cap and compliance sign-off.
- Weak: "label rejects as bad" or "use the model to label rejects" without noting the circularity.

**Example:** Illustrative. Weak versus strong:
- Weak: "I would score the rejects with the model and use those as labels."
- Strong: "Scoring the rejects with a model trained on approvals just returns what the model already believes. The 9.6% is a scenario from an assumed ratio of 3; at a ratio of 1 it is 4% and at 5 it is 15.2%. I would approve a small random slice of near-cutoff rejects at a low limit, cap the total exposure at 500,000 for 500 people, and agree the design with credit risk and compliance first. Then I would refit using weights and check calibration on that slice."

**Code:**
```python
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

# Arithmetic from the question
apps, approved, defaults_appr = 100_000, 30_000, 1_200
rejected = apps - approved
rate_appr = defaults_appr / approved
assert rejected == 70_000 and abs(rate_appr - 0.04) < 1e-12
rate_rej = 3 * rate_appr
defaults_rej = rejected * rate_rej
pop_rate = (defaults_appr + defaults_rej) / apps
assert abs(rate_rej - 0.12) < 1e-12 and round(defaults_rej) == 8_400
assert abs(pop_rate - 0.096) < 1e-12
print("reject default (scenario):", rate_rej, "population default (scenario):", pop_rate)
# Sensitivity: the 9.6% depends on the ratio, which nobody has measured
for k in (1, 2, 3, 5):
    print("ratio", k, "-> population default", round((defaults_appr + rejected * k * rate_appr) / apps, 4))
assert round((defaults_appr + rejected * 1 * rate_appr) / apps, 4) == 0.04

# Simulation: a model fitted on approved only, then used on everyone
rng = np.random.default_rng(13)
n = 100_000
x = rng.normal(0, 1, n)                                   # risk driver; higher is riskier
true_logit = -3.2 + 0.9 * x + 0.35 * np.maximum(x, 0) ** 2   # risk accelerates in the tail
y = rng.random(n) < expit(true_logit)
approve = x < np.quantile(x, 0.30)                        # old policy approves the lowest-risk 30%
Xa = np.c_[np.ones(approve.sum()), x[approve]]
ya = y[approve].astype(float)

def nll(b):
    z = Xa @ b
    return np.sum(np.logaddexp(0, z) - ya * z)
b = minimize(nll, np.zeros(2), method="BFGS").x
pred_rej = expit(b[0] + b[1] * x[~approve])
actual_rej = y[~approve].mean()
print("approved actual default:", round(float(y[approve].mean()), 4))
print("rejects: model predicts", round(float(pred_rej.mean()), 4), "actual", round(float(actual_rej), 4))
assert pred_rej.mean() < actual_rej * 0.8                 # extrapolating a linear fit into the tail underpredicts

# Low-risk experiment: approve a small random slice of rejects near the cutoff, small limits
near = np.where(~approve)[0]
near = near[np.argsort(x[near])][:7_000]                    # the 7,000 rejects closest to the cutoff (10% of rejects)
pick = rng.choice(near, 500, replace=False)
exposure = 500 * 1_000                                       # 500 people x limit 1,000 (illustrative)
obs = y[pick].mean()
se = np.sqrt(obs * (1 - obs) / 500)
print("experiment: n=500, exposure upper bound", exposure, "observed default", round(float(obs), 3), "+/-", round(float(1.96 * se), 3))
assert exposure == 500_000
assert 1.96 * se < 0.04
```

**Output (my run):**
```
reject default (scenario): 0.12 population default (scenario): 0.096
ratio 1 -> population default 0.04
ratio 2 -> population default 0.068
ratio 3 -> population default 0.096
ratio 5 -> population default 0.152
approved actual default: 0.0145
rejects: model predicts 0.0599 actual 0.1088
experiment: n=500, exposure upper bound 500000 observed default 0.018 +/- 0.012
```

**Follow-ups:**
- Can you validate a reject-inference method? Only on a setting where you know the outcomes, for example a period where the cutoff was temporarily relaxed, or the experimental slice; otherwise you cannot.
- What if the experiment is not allowed? Use the approved data with a conservative, monotone model, do not extrapolate the cutoff downward, and monitor early-arrears on any new approvals.
- Does the bias affect fairness reviews? Yes, the group mix of rejects is unobserved; raise it with the compliance and model-risk teams.

**Common mistakes:**
- Reporting approved-only AUC as the model's AUC.
- Treating the 3x ratio as a measured fact.
- Running the experiment on the riskiest rejects, or with no loss cap.
- Reweighting on features when approval used information the model does not have.

### Q14 ⭐⭐⭐ 🔴 E-commerce: A product's selling window runs from 08:00 to 22:00 (14 hours) and it sold out at 18:00 on 5 of the last 7 days with 400 units sold on each of those days, while on the other 2 days it sold 560 and 540. A forecast trained on sales averages 443 units a day and next week's stock is planned from it. Assuming flat hourly demand, which is an assumption to test, estimate the uncensored daily demand on the stock-out days and the 7-day average, and explain how you would model demand from censored sales and handle a price change in the same week.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to censored demand and stock-outs in forecasting and pricing material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Sales are not demand when the shelf is empty: on the 5 stock-out days, 400 units in 10 hours implies about 560 for the full 14 hours, so true average demand is about 557 a day, not the 443 the forecast uses, and I would model demand with a censored likelihood and handle the price change as a separate effect.

**Clarifying questions:**
- Is stock-out time recorded per unit (a timestamp of the last sale and of availability), or only inferred from daily totals? Exact hours-in-stock is the key input.
- Was the product the only variant, or could customers switch to a substitute when it sold out? Substitution moves demand elsewhere.
- Was the price constant, and was it promoted on the sell-out days? A promotion explains both fast sell-out and high demand.
- Is the hourly demand shape known (for example from a similar product)? The flat assumption can be tested.
- What does the forecast drive: reorder quantity, markdown, or safety stock? The cost of overstock versus lost sales sets how much the 114-unit gap matters.

**Approach:**
1. Do the arithmetic. Stock-out at 18:00 means 10 open hours (08:00 to 18:00), so 400 / 10 = 40 units an hour and 40 x 14 = 560 for the day. The 7-day demand is (5 x 560 + 560 + 540) / 7 = 557.1; the sales average is (5 x 400 + 560 + 540) / 7 = 442.9. The forecast understates by about 20.5%.
2. Test the flat-hour assumption. The two non-stock-out days give 40.0 and 38.6 units an hour, which is consistent with 40 but does not show the shape within a day. If the last 4 hours are twice as busy, demand is 720 on a day with the same 400 sold by 18:00, so flat extrapolation says 560 and understates by 160 (see the run). Use intraday sales on non-stock-out days to estimate the hourly profile.
3. Model with censoring. Treat each day's sales as min(demand, stock). Fit demand with a likelihood that, for a censored day, contributes P(demand at least stock) and for an uncensored day the density. Use hours-in-stock as exposure in a Poisson or negative-binomial hourly model, with day-of-week, price, promotion and season terms.
4. Be careful with only 7 days. With 2 uncensored days, a censored-normal fit in the run gives mean 550 but an overconfident sd of 10; do not trust that sd. Pool across similar products or weeks (hierarchical model) to stabilise it.
5. Price change in the same week. Price and stock-out are confounded (a price cut sells out sooner). Estimate price elasticity from a model with price as a covariate and the censored likelihood, using only in-stock hours, and compare same hours across price levels. If you can, run a randomised price test across stores or customers, and flag cannibalisation of substitutes.
6. Use the forecast properly. Forecast demand, not sales; then choose stock by the newsvendor logic (cost of an unsold unit versus a lost sale), using a quantile of demand rather than the mean.

**Metrics:**
- Uncensored demand = units sold / open hours before stock-out x selling hours (560 on a stock-out day).
- Censoring rate = days with stock-out / days (5 of 7 = 71%).
- Forecast bias = (forecast - demand estimate) / demand estimate on days with a stock-out, and a lost-sales estimate = demand estimate - sales.
- Service level = share of days with no stock-out; guardrails: overstock cost and markdown rate.

**Risks:**
- Flat hourly demand is wrong for most products; an evening peak makes the estimate too low, a morning peak too high.
- Shoppers may leave the site on an out-of-stock page, so demand after the stock-out is lower than the early-hours rate would suggest, or they buy a substitute.
- Planning stock from the 443 average repeats the stock-out and trains the next forecast on even more censored data.
- A price change with a stock-out in the same week cannot be separated with 7 days of data.

**What the interviewer scores:**
- Strong: gets 560, 557 and the 20.5% gap, and labels flat demand as an assumption.
- Strong: names censoring, a likelihood that handles it, and exposure (hours in stock).
- Strong: separates the price effect and mentions substitution and the newsvendor decision.
- Weak: "average the sales" or "just fill in the missing hours with the mean".

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Average sales are 443, so I will plan 443 plus a safety margin."
- Strong: "On stock-out days we sold 40 an hour for 10 hours, so with flat demand that is 560 a day, and the true weekly average is about 557, around 20% above what the forecast uses. I would test the flat assumption on intraday data, fit demand with a censored likelihood using hours in stock, and plan stock at a high quantile, because a lost sale and an unsold unit have different costs."

**Code:**
```python
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

hours = 14                                   # 08:00 to 22:00
sold_out_at = 18 - 8                         # hours open before sell-out
assert sold_out_at == 10
rate_per_hour = 400 / sold_out_at
uncensored = rate_per_hour * hours
assert rate_per_hour == 40 and uncensored == 560
daily = [400] * 5 + [560, 540]
avg_sales = sum(daily) / 7
avg_demand = (5 * uncensored + 560 + 540) / 7
gap = 1 - avg_sales / avg_demand
print("avg sales:", round(avg_sales, 1), "avg uncensored demand:", round(avg_demand, 1), "understatement:", round(gap, 3))
assert round(avg_sales) == 443 and round(avg_demand, 1) == 557.1 and round(gap, 3) == 0.205
print("hourly rate on non-sellout days:", round(560 / 14, 1), round(540 / 14, 1))

# Test of the flat-hours assumption with a simulated evening peak
profile = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2], float)   # last 4 hours twice as busy (illustrative)
profile /= profile.sum()
total = 720                                  # illustrative true demand; 10/18 of it falls in the first 10 hours
cum = np.cumsum(profile * total)
k = int(np.argmax(cum >= 400 - 1e-9))        # index of the hour in which the stock of 400 runs out
print("peak case: stock-out after hour", k + 1, "of 14; true demand", total)
flat_est = 400 / (k + 1) * hours
print("flat extrapolation from the stock-out hour:", round(flat_est, 1))
assert (k + 1) == 10 and flat_est == 560 and flat_est < total   # evening peak: flat rule understates (560 vs 720)

# Censored model on daily data: normal demand, stock 400 on 5 days (censored), 2 uncensored days
y = np.array(daily, float); cens = np.array([True] * 5 + [False] * 2)
def nll(p):
    mu, ls = p; s = np.exp(ls)
    ll = norm.logpdf(y[~cens], mu, s).sum() + norm.logsf(400, mu, s) * cens.sum()
    return -ll
fit = minimize(nll, [450.0, np.log(80.0)], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-9, "maxiter": 5000})
mu, s = fit.x[0], float(np.exp(fit.x[1]))
print("censored-normal fit on 7 days: mean", round(float(mu), 1), "sd", round(s, 1))
assert mu > avg_sales
assert abs(mu - 550) < 1 and s < 15      # with 2 uncensored days the fit is overconfident: do not trust this sd
```

**Output (my run):**
```
avg sales: 442.9 avg uncensored demand: 557.1 understatement: 0.205
hourly rate on non-sellout days: 40.0 38.6
peak case: stock-out after hour 10 of 14; true demand 720
flat extrapolation from the stock-out hour: 560.0
censored-normal fit on 7 days: mean 550.0 sd 10.0
```

**Follow-ups:**
- What if the product sells out before 08:00 of the next day's restock? Then the day's window is shorter; use actual open and stock hours as exposure.
- How would you check the flat assumption without intraday data? You cannot fully; ask engineering for hourly order logs and check a similar product that did not sell out.
- How would you size the stock? Pick the quantile of demand where the cost of the next unit unsold equals the margin lost per unit missed; the mean is rarely right.

**Common mistakes:**
- Using sales as demand.
- Filling the stock-out hours with zeros or dropping those days.
- Ignoring that a price change and a stock-out occurred together.
- Trusting a variance estimated from two uncensored days.

### Q15 ⭐⭐⭐ 🔴 Healthcare: Two radiologists independently labelled the same 1,000 scans: both marked 150 as abnormal, both marked 750 as normal, reader A alone marked 60 as abnormal and reader B alone marked 40. The raw agreement is 90%, but the team plans to train on reader A's labels as ground truth and to quote accuracy against them. Compute Cohen's kappa, explain what it implies for the model's ceiling and evaluation, and describe how you would build a better reference standard.
**Asked at:** Clinical-ML deployment material (a physician-oriented dataset-shift article, an arXiv paper on what clinicians want from explainable ML, a JMIR paper on alarm fatigue and a circEWS slide deck on calibration and prevalence); research and secondary sources rather than interview banks; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Kappa is about 0.69, not 90%: raw agreement looks high because 79% to 81% of scans are normal, so the readers agree by chance a lot; reader A is a noisy reference, so I would build an adjudicated or outcome-based reference standard and report accuracy against that.

**Clarifying questions:**
- Were the readers blinded to each other, and to clinical history? Non-independent readers inflate agreement.
- What is the clinical task (any abnormal finding, one specific finding)? The label definition drives what disagreement means.
- Is there an outcome truth available (biopsy, follow-up imaging, clinical course)? That is a better reference than any reader.
- How were the 1,000 scans sampled? If they are enriched for abnormal, kappa and prevalence are not those of the clinic.
- What are the readers' experience levels and the site? A reference should reflect the intended users.

**Approach:**
1. Compute agreement. Matrix: both abnormal 150, both normal 750, A-only 60, B-only 40. Observed agreement = 900 / 1,000 = 0.90. A calls 210 abnormal and B 190. Chance agreement = 0.21 x 0.19 + 0.79 x 0.81 = 0.6798. Kappa = (0.90 - 0.6798) / (1 - 0.6798) = 0.688. A bootstrap interval in the run is about 0.63 to 0.74.
2. Read it correctly. Kappa near 0.69 is moderate to substantial agreement on a common scale; the thresholds are conventions, not rules. Specific agreement is more informative: positive agreement 0.75 (when one reader says abnormal, the other agrees 75% of the time) and negative agreement 0.94.
3. Say what it implies for the ceiling. If A's labels are noisy, a model cannot be reliably better than A as measured against A. In an illustrative model with 20% prevalence and readers of 90% sensitivity and 96% specificity, even a perfect model scores only about 0.947 accuracy against reader A, and two readers agree about 90% of the time (see the run). A model that is more accurate than A will look worse than it is.
4. Beware accuracy as a headline. Everything-normal scores 79% accuracy against A. Report sensitivity, specificity and positive predictive value at the intended prevalence, with intervals.
5. Build a better reference. Options in order of strength: outcome truth (pathology or follow-up), then adjudication (a third senior reader resolves the 100 disagreements, or a panel), then a consensus of three or more readers. Keep the disagreement cases as a separate set: they show where the model and humans differ.
6. Evaluate with the uncertainty. Report model versus adjudicated reference, plus model versus each reader, and compare the model's agreement with a reader to reader-reader agreement (a model agreeing with A at kappa 0.7 is performing at human level, not 70% of the way).

**Metrics:**
- Observed agreement = (both abnormal + both normal) / all = 0.90.
- Kappa = (observed - chance) / (1 - chance) = 0.688; positive and negative specific agreement = 0.75 and 0.94.
- Model sensitivity, specificity and PPV against the adjudicated reference, each with a confidence interval, and calibration at the clinic's prevalence.
- Guardrails: label-noise estimate per class, and model-reader kappa compared with reader-reader kappa.

**Risks:**
- Training on A's labels teaches the model A's habits, including bias; the model inherits A's miss rate.
- Quoting accuracy against A as accuracy in the clinic.
- Adjudicating only disagreements makes the reference depend on the readers' disagreement pattern; spot-check some agreed cases.
- Kappa depends on prevalence, so it is not comparable across sites with different mixes.

**What the interviewer scores:**
- Strong: computes kappa 0.69 with chance agreement shown, and quotes positive agreement.
- Strong: explains the ceiling and why a better-than-A model looks worse.
- Strong: proposes an adjudicated or outcome-based reference and reports against it with intervals.
- Weak: "90% agreement is great, so use A as ground truth".

**Example:** Using the question's counts. Weak versus strong:
- Weak: "The readers agree 90% of the time, so reader A's labels are reliable and we can report accuracy against them."
- Strong: "Agreement is 90% but chance alone gives 68%, so kappa is about 0.69, and when one reader says abnormal the other agrees only 75% of the time. A model cannot be shown better than A against A's own labels, and an all-normal model already scores 79%. I would have a third reader adjudicate the 100 disagreements, or use pathology or follow-up where it exists, and report sensitivity, specificity and PPV with intervals."

**Code:**
```python
import numpy as np

both_abn, both_norm, a_only, b_only = 150, 750, 60, 40
n = both_abn + both_norm + a_only + b_only
assert n == 1000
po = (both_abn + both_norm) / n
a_abn, b_abn = both_abn + a_only, both_abn + b_only
assert po == 0.90 and a_abn == 210 and b_abn == 190
pe = (a_abn / n) * (b_abn / n) + (1 - a_abn / n) * (1 - b_abn / n)
kappa = (po - pe) / (1 - pe)
assert abs(pe - 0.6798) < 1e-9 and abs(kappa - 0.6877) < 5e-4
print("raw agreement", po, "chance agreement", round(pe, 4), "kappa", round(kappa, 4))
pos_agree = 2 * both_abn / (a_abn + b_abn)
neg_agree = 2 * both_norm / (2 * both_norm + a_only + b_only)
print("positive agreement", round(pos_agree, 3), "negative agreement", round(neg_agree, 3))
assert round(pos_agree, 3) == 0.75
# Baseline: a model that says everything is normal scores this against A
print("all-normal accuracy vs reader A:", 1 - a_abn / n)
assert abs((1 - a_abn / n) - 0.79) < 1e-12

# Bootstrap interval for kappa (seeded)
rng = np.random.default_rng(15)
cells = np.array([both_abn, a_only, b_only, both_norm])
def kap(c):
    t = c.sum(); o = (c[0] + c[3]) / t
    a = (c[0] + c[1]) / t; b = (c[0] + c[2]) / t
    e = a * b + (1 - a) * (1 - b)
    return (o - e) / (1 - e)
bs = [kap(rng.multinomial(n, cells / n)) for _ in range(4000)]
lo, hi = np.percentile(bs, [2.5, 97.5])
print("bootstrap 95% interval for kappa:", round(float(lo), 3), round(float(hi), 3))
assert lo < kappa < hi

# Why accuracy against A has a ceiling. Illustrative generative model: prevalence 20%, readers independent given truth.
prev, sens, spec = 0.20, 0.90, 0.96
def reader_accuracy(): return prev * sens + (1 - prev) * spec
acc_A = reader_accuracy()
# a perfect model (equals truth) scored against reader A has accuracy = reader A's accuracy
truth = rng.random(200_000) < prev
ra = np.where(truth, rng.random(truth.size) < sens, rng.random(truth.size) > spec)
rb = np.where(truth, rng.random(truth.size) < sens, rng.random(truth.size) > spec)
print("sim: perfect model accuracy vs A:", round(float((truth == ra).mean()), 3), "reader A vs B agreement:", round(float((ra == rb).mean()), 3))
assert abs((truth == ra).mean() - acc_A) < 0.003
assert (truth == ra).mean() < 1.0 and abs((ra == rb).mean() - 0.90) < 0.02
```

**Output (my run):**
```
raw agreement 0.9 chance agreement 0.6798 kappa 0.6877
positive agreement 0.75 negative agreement 0.938
all-normal accuracy vs reader A: 0.79
bootstrap 95% interval for kappa: 0.628 0.742
sim: perfect model accuracy vs A: 0.947 reader A vs B agreement: 0.902
```

**Follow-ups:**
- How many readers do you need? Three gives a majority vote and shows which cases are contested; more adds cost with diminishing gain. Ask the clinical lead.
- Does a high kappa mean the labels are correct? No; readers can share a bias. Only outcomes can show that.
- How do you present the model's performance? Against the adjudicated reference with intervals, and next to reader performance on the same scans.

**Common mistakes:**
- Treating raw agreement as reliability.
- Calling one reader "ground truth".
- Forgetting prevalence when interpreting kappa or accuracy.
- Reporting no uncertainty on 1,000 scans, 210 of them abnormal.

### Q16 ⭐⭐⭐ 🔴 Ads: After a platform privacy change, 60% of users allow tracking and reported attributed conversions fell from 10,000 to 7,000 a day (30% lower, relative to 10,000), while first-party total orders stayed flat at 25,000 a day. Scaling the 7,000 by 1 divided by 0.6 gives about 11,667, which is 16.7% above the earlier 10,000. Explain why the naive scale-up is probably wrong, how you would estimate true conversions and recalibrate the bidding model, and which checks you would run.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to privacy changes, consent and signal loss in ads measurement; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The scale-up to 11,667 implies conversions grew 16.7% while first-party orders were flat, so it is probably wrong: users who allow tracking are not a random 60%, and the old 10,000 was never the truth either; I would estimate true conversions with a calibrated first-party anchor and a holdout test, then recalibrate the bid model to that.

**Clarifying questions:**
- What did "attributed" mean before and after (a click-through only, view-through, platform-modelled credit)? The platform may have changed its method, not only the data.
- Is the 60% consent share stable across days and segments? A moving share breaks any single scale factor.
- Do I have first-party orders by source, and a way to tie some of them to ad exposure (logged-in users, coupon codes, surveys)? These are the anchors.
- Is there any holdout or geo test running? It gives an unbiased incrementality baseline.
- What does the bid model predict and from what labels? It decides what needs recalibration.

**Approach:**
1. Do the arithmetic. 7,000 / 10,000 means a 30% drop; 7,000 / 0.6 = 11,667, which is 16.7% above 10,000.
2. Show why it is suspicious. First-party total orders are flat at 25,000 a day. Reported attribution covered 10,000 / 25,000 = 40% of orders before and 7,000 / 25,000 = 28% after. A scale-up that lands above the old figure claims advertising delivered more conversions the day privacy changed, with nothing else moving. The more likely story is a mix: consenting users convert differently from non-consenting ones, and the platform may fill some gaps with modelled credit. In the run, retention of 70% against a consent share of 60% implies consenters were 16.7% more attributable, which is exactly the 16.7% error.
3. Estimate true conversions properly. Use a first-party anchor: total orders by day, and orders from segments where exposure can be linked for all users (logged-in customers, coupon codes), to measure what share of true conversions the new reporting sees. Then divide by that share, per segment. In a simulation with consenters converting 1.4 times as often, the naive scale-up overstates by about 12%, while the logged-in-segment ratio is within 1%.
4. Validate with experiments. Run a geo holdout or randomised holdout (ask the measurement and platform teams what is allowed) to get incremental conversions independent of tracking; compare with the reconstructed number. Use marketing mix modelling only as a slow cross-check.
5. Recalibrate bidding. The bid model learned from labels that were 40% of orders; now labels are 28%. Do not simply retrain on the new, thinner labels. Add a calibration layer that maps predicted probability to estimated true conversion rate, fitted on the anchored estimate, and refit weekly with a stability guard on the bid change.
6. Checks: consent share by day and segment, ratio of attributed to first-party orders over time, an A/A comparison, sensitivity of the estimate to the anchor assumption, and a before/after comparison on a campaign with no change.

**Metrics:**
- Attributed share = attributed conversions / first-party orders (40% before, 28% after).
- Visible share = conversions seen by new reporting / true conversions in the anchor segment; true estimate = reported / visible share.
- Calibration = predicted conversions / estimated true conversions by decile; aim near 1 after the fix.
- Guardrails: spend change per day, cost per estimated true conversion, and bid change cap.

**Risks:**
- The anchor segment (logged-in users) may differ from everyone, so the estimate carries that bias; report a range.
- Assuming the old 10,000 was complete; it included its own gaps and modelled credit.
- Retraining on 28% labels without correction lowers bids and loses auctions for no reason.
- Treating consent as exogenous: whoever clicks "allow" may behave differently, which is the whole problem.
- Any rule about what data may be used under the new consent state is a question for the privacy and legal teams.

**What the interviewer scores:**
- Strong: computes 30%, 11,667 and 16.7%, and uses the flat 25,000 orders to challenge the scale-up.
- Strong: names consent selection and a first-party anchor, and states what the anchor assumes.
- Strong: proposes a holdout for incrementality and a calibration layer instead of naive retraining.
- Weak: "divide by 0.6", or "conversions fell 30%, so performance fell 30%".

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Only 60% allow tracking, so I scale up 7,000 by 1 over 0.6 and get 11,667."
- Strong: "That says conversions rose 16.7% on a day when first-party orders did not move, so it is wrong. Reporting kept 70% of volume with 60% consent, which suggests consenters convert more. I would anchor on first-party orders and a segment where we see everyone, measure the visible share, and check it with a geo holdout. Then I would add a calibration layer to the bid model and cap day-to-day bid changes."

**Code:**
```python
import numpy as np

before, after, consent, orders = 10_000, 7_000, 0.60, 25_000
drop = 1 - after / before
naive = after / consent
assert abs(drop - 0.30) < 1e-12 and round(naive) == 11_667
print("drop", drop, "naive scale-up", round(naive), "vs before", round(naive / before - 1, 3))
assert round(naive / before - 1, 3) == 0.167

# What the numbers say: first-party orders are flat, so true conversions did not rise 16.7%.
cov_before, cov_after = before / orders, after / orders
print("attributed share of orders before/after:", cov_before, cov_after)
assert cov_before == 0.40 and cov_after == 0.28
# Proportional loss would give 6,000 (60% of 10,000); we see 7,000, so reporting kept 70% of volume.
implied_factor = (after / before) / consent
print("observed retention / consent share =", round(implied_factor, 3))
assert round(implied_factor, 3) == 1.167       # consenters appear to convert 16.7% more often (or modelled credit fills the gap)

# Calibration scalar for the bid model: attributed conversions per order dropped 40% -> 28%.
# If the bid model predicts P(conversion) learned on old labels, its predictions are now ~30% too high
# relative to the new reported labels, but NOT too high relative to true conversions.
true_per_day = orders * cov_before            # assumption: old attribution was ~complete (test with a holdout!)
print("if old reporting was complete, true attributed-eligible conversions/day ~", true_per_day)
assert true_per_day == 10_000

# Simulation: consenters differ from non-consenters
rng = np.random.default_rng(16)
n = 200_000
consent_flag = rng.random(n) < consent
rate = np.where(consent_flag, 0.0467, 0.0333)    # consenters convert 1.4x more (illustrative)
conv = rng.random(n) < rate
true_total = conv.sum(); seen = conv[consent_flag].sum()
scaled = seen / consent
print("sim: true", true_total, "seen", seen, "naive scaled", round(scaled), "ratio", round(scaled / true_total, 3))
assert scaled > 1.1 * true_total               # naive scale-up overstates when consenters are better converters
# Fix with a stratified ratio: calibrate on a segment where outcomes are known for everyone (first-party logged-in users)
logged = rng.random(n) < 0.3
ratio = conv[logged & consent_flag].sum() / conv[logged].sum()   # share of true conversions visible among logged-in
est = seen / ratio
print("sim: estimate scaled by visible share in logged-in segment", round(est), "true", true_total)
assert abs(est / true_total - 1) < 0.05
```

**Output (my run):**
```
drop 0.30000000000000004 naive scale-up 11667 vs before 0.167
attributed share of orders before/after: 0.4 0.28
observed retention / consent share = 1.167
if old reporting was complete, true attributed-eligible conversions/day ~ 10000.0
sim: true 8168 seen 5482 naive scaled 9137 ratio 1.119
sim: estimate scaled by visible share in logged-in segment 8201 true 8168
```

**Follow-ups:**
- What if no first-party anchor exists? Use a holdout or geo experiment as the anchor, and mark all figures as ranges.
- Should you use the modelled conversions the platform reports? Treat them as an input to be validated against your holdout, not as truth; ask the platform team how they are produced.
- How often do you recalibrate? Weekly at first, with an alert when the visible share moves more than a set band.

**Common mistakes:**
- Scaling by consent share alone.
- Believing the old reporting was complete.
- Retraining directly on the thin labels.
- Changing bids by a large step in one day.

### Q17 ⭐⭐ 🟢 Fintech: A lender can set one of three cutoffs on a score. Cutoff A approves 40,000 of 100,000 applicants with a bad rate of 2% of approved, cutoff B approves 55,000 with 3.5% and cutoff C approves 70,000 with 6% (bad rates are projections). A good customer yields a profit of 1,000 and a bad one a loss of 6,000, so compute the total profit at each cutoff, the bad rate of the extra applicants between cutoffs and the break-even bad rate, then say which cutoff you would pick and what you would check first.
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would pick cutoff B: total profit is 41.5 million against 34.4 million for A and 40.6 million for C, because the extra applicants from A to B have a 7.5% bad rate (below the 14.3% break-even) and the extra from B to C have 15.2% (above it), and first I would check that those bad rates are calibrated on a recent, out-of-time sample.

**Clarifying questions:**
- Are the bad rates projections from a model, and how were they validated (out-of-time, reject-inference-free)? Everything below depends on them.
- Is the profit of 1,000 per good customer and the loss of 6,000 per bad customer net of funding cost, servicing and recoveries, and over what horizon? The break-even rate depends on this ratio.
- Is there a capital or exposure limit that caps the approvals? It might rule out C regardless of profit.
- Will the bad rate of the marginal band hold when the economy changes? The marginal customers are the most sensitive.
- Does the choice need fair-lending or model-risk review before changing the cutoff? That is a question for compliance and the model-risk team.

**Approach:**
1. Set up the economics. Break-even bad rate = 1,000 / (1,000 + 6,000) = 14.3%: a customer is worth taking if the chance of bad is below that.
2. Compute profit at each cutoff. Profit = (approved - bad) x 1,000 - bad x 6,000. A: 800 bad, profit 34,400,000. B: 1,925 bad, profit 41,525,000. C: 4,200 bad, profit 40,600,000 (illustrative currency units, undiscounted).
3. Use marginal bands, not averages. A to B adds 15,000 applicants and 1,125 bad, a marginal bad rate of 7.5%, profit +7,125,000. B to C adds 15,000 and 2,275 bad, 15.2%, profit -925,000. The overall bad rates of 3.5% and 6% hide that the C band is worse than break-even.
4. Test the sensitivity. If every bad rate is 20% higher, B is still best (38.8 million). At 50% higher B is still best. At double, A wins (28.8 million against 28.05 million). So B is robust to moderate error but not to a doubling.
5. Check first: that the projected rates hold on recent data. Backtest the score on the latest matured cohort, look at calibration in the 40,000 to 55,000 band in particular, and check drift since training. The B to C margin (15.2% versus 14.3%) is thin, so small error flips it.
6. Decide and monitor. Choose B, with a staged ramp (approve in tranches, watch early-arrears), and a trigger to tighten if the band's bad rate passes a pre-agreed level, say 10% (agree it with risk).

**Metrics:**
- Bad rate = accounts bad within the horizon / accounts approved, matured only.
- Marginal bad rate of a band = extra bad / extra approved.
- Profit = good x 1,000 - bad x 6,000, with a stated horizon and discounting.
- Guardrails: early-arrears rate of the new band, concentration of exposure, calibration error by band.

**Risks:**
- Projected bad rates carry model error; the marginal band is the least reliable.
- One profit figure per applicant ignores heterogeneity (limits, price, product).
- Selection: customers near the cutoff may behave differently than the model assumes (see reject inference).
- Profit-maximising cutoffs may conflict with fairness and capital constraints; neither is in the numbers.

**What the interviewer scores:**
- Strong: computes 34.4, 41.5 and 40.6 million and the 14.3% break-even.
- Strong: uses marginal bands (7.5% and 15.2%), explaining why averages mislead.
- Strong: runs a sensitivity and names validation of the projected bad rates as the first check.
- Weak: picks the lowest bad rate (A) or the largest volume (C), or compares average rates to break-even.

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "A has the lowest bad rate, so choose A. Or C because it approves the most."
- Strong: "I compute profit at each: 34.4, 41.5 and 40.6 million. Break-even is 14.3% bad. The 15,000 extra people from A to B have a 7.5% bad rate and add 7.1 million; the next 15,000 have 15.2% and lose 0.9 million. So B. Before committing I would backtest the score's calibration in that band on a recent cohort, because B beats A even at a 50% worse bad rate but loses to A at double."

**Code:**
```python
from fractions import Fraction as F

good_profit, bad_loss = 1000, 6000
cuts = {"A": (40_000, F(2, 100)), "B": (55_000, F(35, 1000)), "C": (70_000, F(6, 100))}
be = F(good_profit, good_profit + bad_loss)
print("break-even bad rate:", float(be))
assert abs(float(be) - 0.142857) < 1e-5

def profit(n, r):
    bad = n * r
    return (n - bad) * good_profit - bad * bad_loss
P, BAD = {}, {}
for k, (n, r) in cuts.items():
    BAD[k] = n * r
    P[k] = profit(n, r)
    print(k, "approved", n, "bad", int(BAD[k]), "profit", int(P[k]))
assert (int(BAD["A"]), int(BAD["B"]), int(BAD["C"])) == (800, 1925, 4200)
assert (int(P["A"]), int(P["B"]), int(P["C"])) == (34_400_000, 41_525_000, 40_600_000)

# Marginal bands
for a, b in (("A", "B"), ("B", "C")):
    extra = cuts[b][0] - cuts[a][0]
    xbad = BAD[b] - BAD[a]
    xr = xbad / extra
    delta = P[b] - P[a]
    print(a, "->", b, "extra", extra, "extra bad", int(xbad), "marginal bad rate", round(float(xr), 4), "profit change", int(delta))
    assert delta == (extra - xbad) * good_profit - xbad * bad_loss
    assert (xr < be) == (delta > 0)
assert round(float((BAD["B"] - BAD["A"]) / 15_000), 3) == 0.075
assert round(float((BAD["C"] - BAD["B"]) / 15_000), 4) == 0.1517

# Sensitivity: multiply every bad rate by a factor
best = {}
for f in (F(1), F(12, 10), F(15, 10), F(2)):
    pr = {k: profit(n, r * f) for k, (n, r) in cuts.items()}
    best[float(f)] = max(pr, key=pr.get)
    print("bad rates x", float(f), "best cutoff", best[float(f)], {k: int(v) for k, v in pr.items()})
assert best[1.0] == "B" and best[2.0] == "A"
# How far can the A->B band bad rate rise before B is worse than A?
print("A->B band can rise from 7.5% to", round(float(be), 4), "before the extra applicants lose money")
```

**Output (my run):**
```
break-even bad rate: 0.14285714285714285
A approved 40000 bad 800 profit 34400000
B approved 55000 bad 1925 profit 41525000
C approved 70000 bad 4200 profit 40600000
A -> B extra 15000 extra bad 1125 marginal bad rate 0.075 profit change 7125000
B -> C extra 15000 extra bad 2275 marginal bad rate 0.1517 profit change -925000
bad rates x 1.0 best cutoff B {'A': 34400000, 'B': 41525000, 'C': 40600000}
bad rates x 1.2 best cutoff B {'A': 33280000, 'B': 38830000, 'C': 34720000}
bad rates x 1.5 best cutoff B {'A': 31600000, 'B': 34787500, 'C': 25900000}
bad rates x 2.0 best cutoff A {'A': 28800000, 'B': 28050000, 'C': 11200000}
A->B band can rise from 7.5% to 0.1429 before the extra applicants lose money
```

**Follow-ups:**
- What if the extra band's bad rate is uncertain by +/- 3 points? B to C at 15.2% could be 12% to 18%, so C is a coin flip; stay at B and gather data.
- How would you add capital cost? Subtract a per-account cost from the good-customer profit, which lowers the break-even bad rate.
- Could you price instead of rejecting? Yes, higher rates on the riskier band can lift profit, subject to the pricing and fair-lending rules, which are for the compliance team to specify.

**Common mistakes:**
- Comparing average bad rates to the break-even instead of the marginal rate.
- Ignoring that the rates are projections.
- Forgetting the cost of 6,000 versus the profit of 1,000 asymmetry (a bad customer costs 6 good ones).
- Not checking constraints beyond profit.

### Q18 ⭐⭐ 🟢 E-commerce: An audit team hand-labelled a random sample of 500 reviews and found 60 fake (12%, a sample estimate). A classifier flagged 150 of the same 500 reviews and 54 of the flagged ones were fake. Compute its precision and recall on this sample and an approximate 95% interval for the true fake share using the normal approximation, and say what you would do with the flagged reviews before taking them down.
**Asked at:** Marketplace-trust material (a prachub Amazon fake-review question on detection signals and impact metrics, an Interview Query fake-review prompt and DoorDash and Thumbtack data scientist guides on marketplace analytics); prep-site material and one estimate-based news item, no confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** On this sample the classifier has precision 36% and recall 90%, and the fake share is about 12% (9.2% to 14.8%), so I would not take down flagged reviews automatically: two in three flagged reviews are genuine; I would use the flags to prioritise human review and graded actions.

**Clarifying questions:**
- Was the 500 a simple random sample, and were the auditors blind to the classifier flags? Otherwise the audit labels are biased toward the model.
- What is the audit's own reliability (two auditors, agreement)? 60 fake labels are only as good as the labelling.
- What is the action on a flag: removal, hiding, a badge, a lower rank? Cost of a wrong action differs for each.
- Which threshold gave 150 flags, and can it be moved? A higher threshold trades recall for precision.
- Is the 12% the same in all categories and for new versus old products? One sample may hide big differences.

**Approach:**
1. Compute from the sample. Precision = 54 / 150 = 36%. Recall = 54 / 60 = 90%. The classifier flags 150 / 500 = 30% of reviews while only 12% are fake.
2. Interval for the fake share. p = 60 / 500 = 0.12, standard error = sqrt(0.12 x 0.88 / 500) = 0.0145, so 0.12 +/- 1.96 x 0.0145 gives 9.2% to 14.8%. The normal approximation is fine here because both 60 and 440 are well above 10.
3. Add intervals for precision and recall. With only 150 flagged and 60 fake, precision is 29% to 44% and recall 80% to 95% (Wilson intervals in the run). The recall interval is wide because only 60 fakes were in the sample.
4. Spell out what a blanket takedown does. Scaled to an illustrative 1,000,000 reviews: 300,000 flagged, of which 192,000 would be genuine, and about 12,000 fake reviews would still be missed. That is a lot of wrongly removed customers' content.
5. Use the flags in tiers. Rank by score; send the top slice (higher precision) to human reviewers, with extra signals (account age, device, burst patterns, text similarity); auto-act only above a threshold where audited precision is high; for the middle, use reversible actions (lower weight in the rating, no removal) and an appeal path.
6. Keep auditing. Draw a fresh random sample each month for the base rate, and a stratified sample by score band to measure precision per band, so thresholds can be set from data.

**Metrics:**
- Precision = flagged and fake / flagged = 54 / 150 = 36%.
- Recall = flagged and fake / fake = 54 / 60 = 90%.
- Fake share = fake / sampled reviews = 12% with a 95% interval of 9.2% to 14.8%.
- Guardrails: wrongly removed genuine reviews (appeals upheld), reviewer agreement, time to action, and effect on seller ratings.

**Risks:**
- The audit sample is small for recall (60 positives).
- Fraudsters adapt; a stable precision today may fall.
- Auditors who see the model flag may anchor on it.
- Removing genuine reviews harms honest sellers and shoppers.
- Any rule on how reviews may be removed or disclosed is for the trust and legal teams to specify.

**What the interviewer scores:**
- Strong: gets 36%, 90% and 9.2% to 14.8%, and notes how the interval is built.
- Strong: sees that precision, not recall, makes automatic takedown unsafe, and quantifies it.
- Strong: proposes tiers, human review, appeals and ongoing random audits.
- Weak: "recall is 90% so it is great", or removing everything flagged.

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Ninety per cent recall is excellent, so I would remove all flagged reviews."
- Strong: "Of 150 flagged, 54 are fake, so precision is 36%. At a million reviews that would remove about 192,000 genuine ones. Fake share is 12%, with a 95% interval of 9.2% to 14.8%. I would send the highest-scoring flags to human review with extra signals, only auto-act where audited precision is high, and keep a monthly random audit so the threshold rests on measured numbers."

**Code:**
```python
import numpy as np

n, fake, flagged, tp = 500, 60, 150, 54
precision, recall = tp / flagged, tp / fake
assert precision == 0.36 and recall == 0.90
p = fake / n
se = np.sqrt(p * (1 - p) / n)
lo, hi = p - 1.96 * se, p + 1.96 * se
assert p == 0.12 and abs(se - 0.014532) < 1e-5
assert round(lo, 3) == 0.092 and round(hi, 3) == 0.148
assert n * p >= 10 and n * (1 - p) >= 10          # normal approximation is reasonable
print("fake share", p, "95% interval", round(float(lo), 3), round(float(hi), 3))
print("precision", precision, "recall", recall, "flag rate", flagged / n)

def wilson(k, m, z=1.96):
    ph = k / m
    c = (ph + z * z / (2 * m)) / (1 + z * z / m)
    h = z * np.sqrt(ph * (1 - ph) / m + z * z / (4 * m * m)) / (1 + z * z / m)
    return c - h, c + h
pl, ph_ = wilson(tp, flagged); rl, rh = wilson(tp, fake)
print("precision 95% (Wilson)", round(float(pl), 3), round(float(ph_), 3))
print("recall 95% (Wilson)", round(float(rl), 3), round(float(rh), 3))
assert pl < precision < ph_ and rl < recall < rh

# Cost of a blanket takedown of flagged reviews, scaled to an illustrative 1,000,000 reviews
reviews = 1_000_000
flag_n = reviews * flagged / n
wrong = flag_n * (1 - precision)
print("flagged", int(flag_n), "genuine reviews taken down", int(wrong), "fake reviews missed", round(reviews * 0.12 * (1 - recall)))
assert int(flag_n) == 300_000 and int(wrong) == 192_000

# Review queue: if humans check flagged reviews, how many fake per 100 checked vs random review?
print("fake per 100 reviews checked: flagged", 100 * precision, "random", 100 * p)
assert 100 * precision == 36 and abs(100 * precision / (100 * p) - 3.0) < 1e-9     # 3x lift over random
```

**Output (my run):**
```
fake share 0.12 95% interval 0.092 0.148
precision 0.36 recall 0.9 flag rate 0.3
precision 95% (Wilson) 0.288 0.439
recall 95% (Wilson) 0.799 0.953
flagged 300000 genuine reviews taken down 192000 fake reviews missed 12000
fake per 100 reviews checked: flagged 36.0 random 12.0
```

**Follow-ups:**
- How big an audit sample do you need? For a 95% interval of +/- 1 point at 12%, about 4,060 reviews (1.96^2 x 0.12 x 0.88 / 0.01^2), more for per-category estimates.
- How would you raise precision? Raise the threshold, add features, or require agreement from a second model; recall will fall, so measure both.
- Why a Wilson interval for precision? It behaves better than the simple normal one when the proportion is far from 0.5 or the sample is small.

**Common mistakes:**
- Reading recall alone.
- Assuming the 12% is exact.
- Taking down flagged reviews with no review or appeal.
- Using flagged-only data to estimate the fake share.

### Q19 ⭐⭐ 🟢 Healthcare: A model was trained on 120,000 patient records and 15,000 patients (12.5% of the records) later withdrew consent for research use. Retraining from scratch takes 3 days of compute plus a clinical re-validation, and the product team asks whether the deployed model can keep running. What do you tell them, what questions do you take to the privacy and compliance teams, and how would you design the pipeline so withdrawals are cheap to honour next time?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to consent withdrawal and data lineage in health-data privacy material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Whether the deployed model may keep running is not my call or the product team's: I would tell them it is a question for the privacy and compliance teams, bring them the facts they need (which records, which models, what retraining costs), prepare the retrain without the 15,000 patients now, and build a consent ledger so the next withdrawal is a filter, not a project.

**Clarifying questions:**
- What exactly was consented to, and what does withdrawal cover: future use, deletion of the raw records, or also models and derived data? That wording is for the privacy officer and legal to interpret.
- Does the model contain identifiable information (could it memorise records), or only aggregate patterns? It affects the risk discussion; I would ask the privacy team how they treat it.
- Where else do the 15,000 patients' data live: feature tables, embeddings, validation sets, logs, backups, vendors? We need an inventory.
- Is the 12.5% a one-off or a trend? A trend changes how we design the pipeline.
- Does the clinical safety side tolerate running the current model while the retrain is validated, or is switching it off safer for patients? That is for the clinical owner to decide.

**Approach:**
1. Do the arithmetic. 15,000 / 120,000 = 12.5%, so 105,000 records remain. The retrain is 3 days of compute plus a clinical re-validation; that is the cost of compliance, not a reason to delay the question.
2. Tell product plainly: I cannot say it is fine or not. I will take the options to privacy, compliance and the clinical owner this week, and give them a decision memo: (a) keep running until a retrained model is validated, with a stated end date; (b) switch to the previous model if one was trained without these patients; (c) pause the service. Each has a patient-safety cost and a privacy position; they choose.
3. Do the technical work in parallel. Start the retrain on the 105,000 now, in a staging area, so no time is lost whatever the decision is. Compare it with the current model on the validation set (also with withdrawn patients removed) to measure the performance change; with 87.5% of the data, a small change is plausible but must be measured.
4. Answer the data-side questions. List all copies and derived artefacts of the 15,000 patients' data, and the model versions trained on them. Questions to take to privacy and compliance: what must be deleted and by when, whether trained models count, what to tell clinicians and patients, what to record as evidence, and whether past analyses stay valid.
5. Design for cheap withdrawals. Keep a consent ledger (patient, purpose, status, effective date). Build the training table by joining that ledger at build time, record the manifest hash of each training set in the model registry, and keep lineage from raw data to features to model. A withdrawal then triggers a filter and a scheduled retrain, not an investigation.
6. Plan the retrain cadence. Retrain on a fixed schedule (for example monthly or quarterly) so that withdrawals are absorbed in routine releases, with the validation pack automated. Sharding the training data can reduce retrain work for rare withdrawals, but not for a batch like this (see the run).

**Metrics:**
- Withdrawn share = withdrawn records / training records = 12.5%.
- Time to honour = time from withdrawal request to the first deployed model without that patient (target set with the privacy team).
- Lineage coverage = records with consent status and lineage / all records (target 100%).
- Retrain performance delta = metric(retrained) - metric(current) on the same validation set, with an interval.
- Guardrails: no withdrawn id in any training manifest (checked by test), and clinical validation sign-off before release.

**Risks:**
- Assuming that removing rows from a table also removes their influence on a trained model; whether that is acceptable is a policy question.
- Missed copies: validation sets, exports and backups still containing the patients.
- Retraining quickly without re-validation, which trades a privacy risk for a safety risk.
- Hard-coding the answer ("keep running") when the rule might say otherwise.

**What the interviewer scores:**
- Strong: separates decisions (privacy, compliance, clinical) from the engineering work, and says so without stating rules as facts.
- Strong: gets 12.5% and 105,000, starts the retrain in parallel and measures the performance change.
- Strong: proposes a consent ledger joined at build time, manifest hashes and lineage.
- Weak: "it is fine, the model is anonymous", or "we must shut it down" with no questions asked.

**Example:** Illustrative. Weak versus strong:
- Weak: "The model does not store patient data, so it can keep running. I would just remove them next time."
- Strong: "I cannot decide that; the privacy and compliance teams and the clinical owner do. I will give them the options and the facts: 15,000 of 120,000 records, 12.5%, a 3-day retrain plus validation, and an inventory of every copy. I start the retrain on the 105,000 records now so we lose no time, and I will build a consent ledger joined at training time so a withdrawal is a filter and a scheduled retrain."

**Code:**
```python
import hashlib
import numpy as np

total, withdrawn = 120_000, 15_000
share = withdrawn / total
remaining = total - withdrawn
assert share == 0.125 and remaining == 105_000
print("withdrawn share", share, "remaining records", remaining)

# Consent ledger joined at training-table build time
rng = np.random.default_rng(19)
ids = np.arange(total)
w_ids = rng.choice(ids, withdrawn, replace=False)
status = np.full(total, "active", dtype=object)
status[w_ids] = "withdrawn"
train_ids = ids[status == "active"]
assert train_ids.size == remaining and not np.isin(train_ids, w_ids).any()

def manifest_hash(a):
    return hashlib.sha256(np.sort(a).tobytes()).hexdigest()[:12]
print("old manifest", manifest_hash(ids), "new manifest", manifest_hash(train_ids))
assert manifest_hash(ids) != manifest_hash(train_ids)

# Sharded training (K shards, each model trained on one shard): how many shards must be retrained?
K = 20
def expected_shards_touched(w, K=K):
    return K * (1 - (1 - 1 / K) ** w)
for w in (1, 10, 100, 15_000):
    print("withdrawals", w, "expected shards to retrain of", K, ":", round(expected_shards_touched(w), 2))
assert round(expected_shards_touched(1), 2) == 1.0
assert round(expected_shards_touched(10), 2) == 8.03
assert round(expected_shards_touched(15_000), 2) == 20.0   # a 12.5% batch touches every shard: sharding gives no saving

# Cost of waiting: retrain is 3 days compute; if withdrawals arrive weekly and we batch them
retrain_days = 3
batch_weekly_share = withdrawn / total / 52
print("if the same share arrived evenly over a year, weekly share:", round(batch_weekly_share * 100, 3), "%")
assert retrain_days == 3 and round(batch_weekly_share * 100, 3) == 0.24
```

**Output (my run):**
```
withdrawn share 0.125 remaining records 105000
old manifest be0eeae2d5b5 new manifest 4a77392a8266
withdrawals 1 expected shards to retrain of 20 : 1.0
withdrawals 10 expected shards to retrain of 20 : 8.03
withdrawals 100 expected shards to retrain of 20 : 19.88
withdrawals 15000 expected shards to retrain of 20 : 20.0
if the same share arrived evenly over a year, weekly share: 0.24 %
```

**Follow-ups:**
- Can you "unlearn" instead of retraining? Approximate unlearning methods exist in the research literature (editor knowledge, not tested here); whether any is acceptable is a question for privacy and compliance, and validation is still needed.
- What if the retrained model is clearly worse? Report the delta to the clinical owner; options include more data from consented sources, or accepting a shorter-lived model; they decide.
- What do you log for audit? The ledger entry, the manifest hash of each training set, the model version, and the date of the deployed model that excludes the patient.

**Common mistakes:**
- Treating a privacy question as an engineering call.
- Deleting rows but leaving copies in features, validation sets or backups.
- Not recording which model was trained on which manifest.
- Planning for one withdrawal, not for a flow of them.

### Q20 ⭐⭐ 🟢 Ads: For a retail campaign, the measured incremental conversion probability per user from the 1st, 2nd, 3rd and 4th impression in a week is 0.50%, 0.30%, 0.15% and 0.05%. A conversion is worth 20 and each impression costs 0.05. Compute the net value of each impression and the best weekly cap, and explain how you would check that these incremental numbers are causal.
**Asked at:** Ad-serving system-design material (techinterview.org ad serving and real-time bidding pages, a Dataford question on budget pacing and frequency capping, machinelearningatscale.com on frequency capping; feedback-controller pacing, per-user counters and credits for invalid clicks appear in the snippets); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The net value per impression is +0.05, +0.01, -0.02 and -0.04, so the best weekly cap is 2 (cumulative net 0.06 per user), but the second impression clears break-even by only 0.05 points, so I would confirm the numbers with a randomised frequency test before setting the cap.

**Clarifying questions:**
- How were the incremental probabilities measured: randomised holdout, ghost ads, or observational attribution? Only the first two are causal.
- Is a conversion worth a flat 20, or does value vary by customer? Variable value changes the break-even per user.
- Is the 0.05 cost an average? Costs may differ by placement or auction, and later impressions may be cheaper.
- Are the probabilities conditional on a user reaching that impression? Users who reach the 4th are a selected group.
- Within what window is the conversion counted (the same week, 7 or 30 days)? A longer window changes later impressions' value.

**Approach:**
1. Compute net value per impression = incremental probability x 20 - 0.05. First: 0.005 x 20 = 0.10, minus 0.05 = +0.05. Second: 0.003 x 20 = 0.06, so +0.01. Third: 0.0015 x 20 = 0.03, so -0.02. Fourth: 0.0005 x 20 = 0.01, so -0.04.
2. Choose the cap by the cumulative sum, which is 0.05, 0.06, 0.04, 0.00 per user for caps 1 to 4. The maximum is at cap 2. Equivalent rule: keep adding impressions while incremental probability exceeds cost / value = 0.05 / 20 = 0.25%. The first two impressions (0.50% and 0.30%) pass; the third (0.15%) does not.
3. Note how thin the margin is. The second impression is at 0.30% against a 0.25% threshold, so if its true effect is 17% lower it is worth nothing. Treat cap 2 as the best estimate, not a certainty. Cap 1 loses only 0.01 per user compared with cap 2, so there is a cheap fallback.
4. Check causality. The numbers should come from randomisation: assign users at random to cap 1, 2, 3 and 4 (or to a holdout), then incremental probability of the k-th impression = conversion rate under cap k minus under cap k-1. Observational comparisons are confounded: heavy-exposure users are more active and more likely to buy anyway. In a simulation with zero ad effect, users who saw 4 impressions converted at 0.83% against 0.38% for 1 and 0.28% for 0 (see the run).
5. Size the test. To separate 0.30% from 0.25% at a 1% baseline conversion takes about 620,000 users per arm (80% power, 5% two-sided, illustrative); to see the full 0.30-point effect takes about 17,000 per arm. If that is too large, test cap 1 versus cap 2 first and use the confidence interval to decide.
6. Implement and monitor. Enforce the cap with a per-user counter (including across devices where identity allows), watch spend, reach and conversions, and revisit when creative, season or audience changes; repeat the test periodically.

**Metrics:**
- Incremental probability of impression k = P(convert | cap k) - P(convert | cap k-1), from randomised arms.
- Net value per impression = incremental probability x value - cost per impression; cumulative net per user by cap.
- Break-even incremental probability = cost / value = 0.25%.
- Guardrails: reach (share of target users with at least one impression), total conversions, and spend per incremental conversion.

**Risks:**
- Confounding by user intent if the numbers are observational.
- Selection: the effect of a fourth impression is measured on those the auction reached.
- A flat value of 20 hides the mix of customers; a higher-value customer may justify a higher cap.
- Cross-device counting misses impressions, so the cap is enforced loosely.
- Cap interacts with creative fatigue and the auction; a result for one campaign may not carry over.

**What the interviewer scores:**
- Strong: gets +0.05, +0.01, -0.02, -0.04, cap 2, and the 0.25% break-even rule.
- Strong: points out the margin is thin and sets up a randomised test, with a sample-size estimate.
- Strong: explains why exposure-level comparisons are confounded.
- Weak: choosing the cap by conversion rate alone, or taking the observational lift as causal.

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Conversion keeps rising with each impression, so I would cap at 4."
- Strong: "Break-even is 0.25%, so only the first two impressions pay: +0.05 and +0.01 net, then -0.02 and -0.04. Cap 2 gives 0.06 per user. The second impression is only just above break-even, so I would run a randomised test across cap levels with several hundred thousand users per arm, because comparing heavy and light viewers measures their intent, not the ads."

**Code:**
```python
from fractions import Fraction as F
import numpy as np

inc = [F(5, 1000), F(3, 1000), F(15, 10000), F(5, 10000)]   # 0.50%, 0.30%, 0.15%, 0.05%
value, cost = 20, F(5, 100)
net = [p * value - cost for p in inc]
print("net value per impression:", [float(x) for x in net])
assert [float(x) for x in net] == [0.05, 0.01, -0.02, -0.04]
cum, run = [], F(0)
for x in net:
    run += x; cum.append(run)
print("cumulative net per user by cap 1..4:", [float(x) for x in cum])
assert [float(x) for x in cum] == [0.05, 0.06, 0.04, 0.0]
best = max(range(4), key=lambda i: cum[i]) + 1
assert best == 2
breakeven = cost / value
print("break-even incremental probability per impression:", float(breakeven))
assert float(breakeven) == 0.0025
# Margin: impression 2 clears break-even by 0.05 points; how far can its true probability fall?
margin = float(inc[1] - breakeven)
print("impression 2 margin over break-even (probability points):", round(margin * 100, 3))
assert round(margin * 100, 3) == 0.05

# Sample size to tell 0.30% from 0.25% in a two-arm randomised comparison (cap 2 vs cap 1 arms)
# Both arms convert at roughly 1% (illustrative baseline), so the variance per user is ~ p(1-p).
p0 = 0.010
za, zb = 1.96, 0.84
delta = 0.0005
n_per_arm = 2 * (za + zb) ** 2 * p0 * (1 - p0) / delta ** 2
print("users per arm to detect a 0.05-point gap at 1% baseline (80% power):", round(n_per_arm))
assert 600_000 < n_per_arm < 650_000
# And to detect the full 0.30-point effect of the 2nd impression versus zero
n_full = 2 * (za + zb) ** 2 * p0 * (1 - p0) / 0.003 ** 2
print("users per arm to detect the 0.30-point effect:", round(n_full))
assert 15_000 < n_full < 20_000

# Selection check: users who reach 4 impressions are more active. Illustrative simulation.
rng = np.random.default_rng(20)
n = 400_000
activity = rng.gamma(2, 0.5, n)                 # latent intent, mean 1
imps = np.minimum(rng.poisson(1.2 * activity), 4)
base = 0.004 * activity                        # conversion without ads depends on intent
conv = rng.random(n) < base                    # zero true ad effect
r1 = conv[imps == 1].mean(); r4 = conv[imps == 4].mean(); r0 = conv[imps == 0].mean()
print("sim with ZERO ad effect: conversion rate by impressions seen 0/1/4:", round(float(r0), 4), round(float(r1), 4), round(float(r4), 4))
assert r4 > r1 > r0                             # observational 'dose-response' appears without any causal effect
```

**Output (my run):**
```
net value per impression: [0.05, 0.01, -0.02, -0.04]
cumulative net per user by cap 1..4: [0.05, 0.06, 0.04, 0.0]
break-even incremental probability per impression: 0.0025
impression 2 margin over break-even (probability points): 0.05
users per arm to detect a 0.05-point gap at 1% baseline (80% power): 620928
users per arm to detect the 0.30-point effect: 17248
sim with ZERO ad effect: conversion rate by impressions seen 0/1/4: 0.0028 0.0038 0.0083
```

**Follow-ups:**
- What if impression costs fall for later impressions? Recompute net value with the actual cost per impression; the rule is the same (incremental probability times value above cost).
- What if conversion value varies by user? Set caps per segment, using the expected value for that segment.
- Is a cap per week the right unit? Test a per-day cap and a spacing rule too; the effect of the second impression may depend on gap.

**Common mistakes:**
- Using total conversion rate by exposure count as incremental.
- Forgetting the cost term, so every impression looks positive.
- Ignoring the 0.05-point margin of the second impression.
- Treating a cap as a purely statistical choice, not a spend and reach decision.

### Q21 ⭐⭐ 🟢 Fintech: A bank has 120 models in its inventory and 18 of them are in the high-risk tier. The independent validation team can complete 24 full validations a year and each high-risk model needs one every year. Compute how many validations remain for the other 102 models and how many years one pass over them would take, and say how you would tier models, trigger early reviews and use lighter-weight monitoring, leaving rules to compliance.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to model risk governance in general terms (tiering, validation capacity); related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** 18 of the 24 yearly validations go to the high-risk tier, so 6 are left for the other 102 models, and one full pass over them would take 102 / 6 = 17 years, which is why I tier by risk and use lighter monitoring instead of validating everything fully.

**Clarifying questions:**
- How does the bank define "high risk" today (materiality, customer impact, use in decisions)? It decides whether 18 is the right number or an artefact of the definition.
- What counts as a "full validation" and is there a cheaper lighter review? Without it the capacity maths is all-or-nothing.
- Are the 120 models independent, or do many share data, features or a vendor? Shared components can be validated once and reused.
- Which models changed recently or have known issues? That drives early reviews.
- Who owns the tiering policy and the review cadence? I will propose, compliance and model risk approve (rules are theirs, I would ask them what is mandatory).

**Approach:**
1. Do the arithmetic out loud: 120 - 18 = 102 other models; 24 - 18 = 6 spare validations; 102 / 6 = 17 years. That is not workable, so full validation of everything cannot be the plan.
2. Tier by a score of materiality (money or customers touched), complexity and opacity, data and vendor dependence, and how fast the world changes. Three or four tiers, written down, reviewed yearly.
3. Give each tier a cadence and depth. High: full validation yearly. Medium: full every few years plus a yearly light review. Low: light checklist plus automated monitoring only.
4. Define early-review triggers: a material model or data change, drift or performance alarms, a rise in overrides or complaints, a new use of the model, an incident, a vendor change.
5. Lighter monitoring for the lower tiers: input drift, output distribution, back-test of performance when labels arrive, data-quality checks, and an owner attestation. These are dashboards and tests, not new validations.
6. Show leadership the capacity table. If the tiered load still exceeds 24, say so and name the levers (staff, cadence, retire models, reduce the high-risk count by fixing the definition honestly).
7. Take the proposal to compliance and the model-risk owner. Ask them which cadences and documents are mandatory; I do not state them as facts.

**Metrics:**
- Validation capacity load = (sum of validations per year across tiers, in full-validation equivalents) / 24.
- Coverage = models reviewed within their tier cadence / models in inventory (target 100% for high).
- Backlog age = median days overdue for reviews past due.
- Trigger-to-review time = days from a trigger firing to the review starting.
- Guardrail: findings per validation by tier. If low-tier light reviews find nothing ever, the checks may be too weak; if they find a lot, the tier is wrong.

**Risks:**
- A "light review" becomes a rubber stamp. Sample some for a full re-check.
- Tiers gamed downward to save effort. Tier by an agreed score, not by who owns the model.
- Monitoring alerts nobody reads. Give each alert an owner and a response time.
- The capacity gap hidden by optimistic ratios (the light-review cost of 0.1 is invented; measure it).

**What the interviewer scores:**
- Strong: gets 102, 6 and 17 years fast, then moves to tiering and triggers instead of "hire more people". Weak: stops at the arithmetic or says "validate all of them slowly".
- Strong: separates what the data scientist proposes from what compliance mandates. Weak: invents regulatory rules.
- Strong: monitoring that is concrete (drift, back-test, overrides). Weak: "we will keep an eye on it".
- Strong: shows a capacity table with explicit assumptions. Weak: no numbers after the first calculation.

**Example:** With the invented split of 24 medium models (full every 3 years) and 78 low models (light review each year at 0.1 of a full validation), the load is 18 + 8 + 7.8 = 33.8 full-validation equivalents against 24 available. So even tiering does not fit, and I would say so.
- Weak: "We have 24 a year and 120 models, so we validate 24 each year and rotate." (Leaves 17 years of coverage and the high tier still takes 18 of the 24.)
- Strong: "Six slots are left for 102 models, 17 years for one pass. So I tier, give low-risk models a light yearly review, add triggers for early review, and bring the remaining gap of about 10 equivalents to the model-risk owner with options. Which cadences are mandatory is for compliance to confirm."

**Code:**
```python
# Q21 model inventory and validation capacity (illustrative numbers)
total, high, capacity = 120, 18, 24
others = total - high
spare = capacity - high            # validations left after the yearly high-risk cycle
years_all_full = others / spare
assert others == 102 and spare == 6 and years_all_full == 17.0
print(f"other models={others}, spare full validations/yr={spare}, years for one pass={years_all_full:.0f}")

# What if the other 102 are split into medium (24) and low (78) tiers?
# Illustrative cadence: medium = full validation every 3 years, low = light review every year
# (a light review costs 0.1 of a full validation, an invented ratio)
medium, low = 24, 78
med_load = medium / 3                    # 8 full validations/yr
low_load = low * 0.1                     # 7.8 full-validation equivalents/yr
need = high + med_load + low_load
assert med_load == 8.0 and abs(low_load - 7.8) < 1e-9 and abs(need - 33.8) < 1e-9
print(f"tiered load = {need:.1f} full-validation equivalents vs capacity {capacity}")
gap = need - capacity
assert abs(gap - 9.8) < 1e-9
print(f"gap = {gap:.1f} -> options: more staff, longer medium cycle, or fewer high-risk models")

# Longer medium cycle (every 4 years) and low light review at 0.05
need2 = high + medium / 4 + low * 0.05
assert abs(need2 - 27.9) < 1e-9
print(f"with medium every 4y and low at 0.05: {need2:.1f} (still above {capacity})")
```

**Output (my run):**
```text
other models=102, spare full validations/yr=6, years for one pass=17
tiered load = 33.8 full-validation equivalents vs capacity 24
gap = 9.8 -> options: more staff, longer medium cycle, or fewer high-risk models
with medium every 4y and low at 0.05: 27.9 (still above 24)
```

**Follow-ups:**
- What if all 18 high-risk models need a deeper validation than 1 slot each? Then fewer than 6 are spare, and I must cut scope or add capacity; I would not squeeze the high tier.
- How do you prevent models escaping the inventory? Procurement and deployment gates that require an inventory entry before go-live; ask the governance team how it is enforced today.
- Who validates the monitoring itself? A short periodic check by the validation team that alerts fire on known drifted data.

**Common mistakes:** Treating all models the same. Forgetting that 24 - 18 leaves only 6. Stating regulatory cadences as facts. Ignoring that light reviews also cost time. No early-review triggers.

### Q22 ⭐⭐ 🟢 E-commerce: Of 100,000 apparel orders, 12,000 (12%) are returned for size reasons, and a size widget (use was voluntary) was used on 20,000 orders: the size-return rate is 8% for widget orders and 13% for the 80,000 others (measured). The team claims that rolling the widget out would close the 5-point gap on all 80,000 other orders and save 150 per avoided return. Compute that claimed saving and explain why it is probably overstated and how you would test it.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to size recommendation and returns in fashion e-commerce material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The claim is 80,000 x 5 points = 4,000 avoided returns x 150 = 600,000, but it is probably overstated because widget users chose to use it and not everyone will, so I would run a randomised test before banking it.

**Clarifying questions:**
- Use is voluntary, so the 8% group is self-selected. Is there any variation in who sees the widget that I could use as a natural experiment?
- Is the 150 per avoided return a full cost (shipping both ways, handling, resale loss) or just shipping? It sets the value, and the number could be lower or higher.
- Are returns "for size reasons" coded by the customer or by an agent? Reason codes are noisy and a widget can change how people pick a reason.
- Does the widget change conversion (people buying less when told the fit is bad)? A lower return rate bought with lost sales is not a pure saving.
- Which categories and brands have widget coverage? Fit data may exist only for some products.

**Approach:**
1. Check the base: 20,000 x 8% = 1,600 and 80,000 x 13% = 10,400 give 12,000 returns, 12% of 100,000. The numbers are consistent.
2. Reproduce the claim: 5 points x 80,000 = 4,000 returns avoided x 150 = 600,000.
3. Name why it is too high: selection (engaged, careful shoppers use the widget and would return less anyway), a take-up below 100% (today only 20% use it), and the effect varying by category.
4. Show an adjusted number with stated assumptions, for example 20% use and a 2-point causal effect among users gives 320 avoided and 48,000. Say clearly that it is an illustration.
5. Test: randomise who is shown the widget (for example 50/50 at the session or user level, or by product page), keep the intent-to-treat comparison, and measure size-return rate per order.
6. Add guardrails: conversion, total return rate (all reasons), exchanges, and revenue per visitor.
7. Roll out in stages if the lift holds and report the number with an interval, not a point.

**Metrics:**
- Size-return rate = orders returned for size reasons / orders delivered, per arm.
- Intent-to-treat effect = rate in the widget-shown arm minus rate in the control arm, over everyone assigned.
- Net saving = avoided returns x cost per return minus lost margin from conversion change minus widget cost.
- Guardrails: conversion rate, total return rate, customer complaints, time to checkout.
- Count orders, not sessions, for the return denominator.

**Risks:**
- Comparing widget and non-widget orders and calling the gap an effect (selection bias).
- Assuming 100% take-up.
- Return reasons recoded after widget launch.
- Novelty: the effect fades after the first weeks.
- Fit data coverage uneven: gains concentrate in a few categories.

**What the interviewer scores:**
- Strong: gets 600,000 first, then says why it is an upper bound and names selection. Weak: only the arithmetic, or "the number is wrong" with no reason.
- Strong: proposes randomisation and says what is compared. Weak: "do an A/B test" without unit or metric.
- Strong: includes take-up and guardrails (conversion). Weak: ignores that fewer returns may mean fewer sales.
- Strong: labels the adjusted number as an assumption. Weak: presents an invented 2 points as a finding.

**Example:** 12,000 returns, 1,600 from widget users and 10,400 from the rest. Claim 4,000 x 150 = 600,000. Suppose only 20% of the other orders would use it and only 2 points of the gap is real: 80,000 x 0.2 x 0.02 = 320 avoided, 48,000 saved (illustrative). A test detecting 13% to 12% needs about 17,200 orders per arm (17,165 computed).
- Weak: "Widget users return 5 points less, so roll it out and save 600,000."
- Strong: "That 600,000 assumes everyone uses it and that the gap is all causal. Users chose it, so I would randomise exposure, read the intent-to-treat effect on size returns and check conversion, and then size the saving from the measured effect."

**Code:**
```python
# Q22 size widget claim (illustrative numbers)
orders, ret = 100_000, 12_000
w_n, o_n = 20_000, 80_000
w_rate, o_rate = 0.08, 0.13
w_ret, o_ret = w_n * w_rate, o_n * o_rate
assert w_ret == 1_600 and o_ret == 10_400 and w_ret + o_ret == ret
assert ret / orders == 0.12 and w_n + o_n == orders

gap_pts = o_rate - w_rate
avoided_claim = o_n * gap_pts
saving_claim = avoided_claim * 150
assert abs(gap_pts - 0.05) < 1e-12 and round(avoided_claim) == 4_000 and round(saving_claim) == 600_000
print(f"claimed: {avoided_claim:.0f} avoided returns, saving {saving_claim:,.0f}")

# Haircut 1: only some of the 80,000 will use the widget (today 20%)
use = w_n / orders
assert use == 0.2
# Haircut 2: only part of the 5-point gap is causal (invented: 2 points among users)
causal = 0.02
avoided_adj = o_n * use * causal
saving_adj = avoided_adj * 150
assert round(avoided_adj) == 320 and round(saving_adj) == 48_000
print(f"adjusted (20% use, 2-pt causal effect among users): {avoided_adj:.0f} avoided, saving {saving_adj:,.0f}")

# Selection story: if widget users were already lower-return, gap with zero causal effect
# Invented: engaged shoppers return 8% by themselves, others 13%: widget does nothing.
print(f"gap with zero causal effect is still {gap_pts*100:.0f} points in that world")

# Sample size for a randomized test to detect a 1-point drop from 13% (alpha 0.05, power 0.8), per arm
from statistics import NormalDist
z = NormalDist().inv_cdf
p1, p2 = 0.13, 0.12
n = (z(0.975) + z(0.8)) ** 2 * (p1*(1-p1) + p2*(1-p2)) / (p1 - p2) ** 2
assert 17_000 < n < 18_000
print(f"orders per arm to detect 13% -> 12%: {n:,.0f}")
```

**Output (my run):**
```text
claimed: 4000 avoided returns, saving 600,000
adjusted (20% use, 2-pt causal effect among users): 320 avoided, saving 48,000
gap with zero causal effect is still 5 points in that world
orders per arm to detect 13% -> 12%: 17,165
```

**Follow-ups:**
- What if you cannot randomise? Use a staggered rollout by product or region with a difference-in-differences read, and say the assumptions are weaker.
- Why intent-to-treat and not only widget users in the treated arm? Because users within the arm self-select again; assignment is the only random part.
- What about the 13% in the other group? It is the baseline you compare to the control arm, not a target.

**Common mistakes:** Multiplying the gap by all remaining orders. Treating users who chose the widget as a control. Forgetting take-up and conversion. Using sessions as the denominator.

### Q23 ⭐⭐ 🟡 Fintech: A monitoring system raises 10,000 alerts a month and analysts confirm 300 of them as suspicious (3%), with capacity to review 6,000 alerts. A model splits the alerts into three buckets: the top 3,000 alerts hold 270 confirmed cases, the middle 3,000 hold 24 and the bottom 4,000 hold 6 (retrospective counts from a month in which all 10,000 alerts were reviewed). Compute the confirmed rate in each bucket and the share of confirmed cases found by reviewing the top two buckets, and explain what you would propose for the bottom bucket given that compliance owns any decision to stop reviewing alerts.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to KYC and AML alert triage in fintech material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The top bucket is 9.0% confirmed, the middle 0.8% and the bottom 0.15%, and the top two buckets (6,000 alerts, exactly the review capacity) hold 294 of 300 confirmed cases, 98%; for the bottom 4,000 I would propose a lighter-touch process and a sampled audit, and leave the decision to stop reviewing to compliance.

**Clarifying questions:**
- Given all 10,000 alerts were reviewed last month, how stable is the split month to month? Retrospective labels on a fully reviewed month are clean, but a prospective shadow run is the real test.
- What does "confirmed suspicious" mean: a filed report, an analyst opinion or a closed case? Label definition changes the rates.
- Is the model's score computed from the same signals that triggered the alert? If so, it may just be re-ranking rules.
- What is the cost of a missed case, and who owns it? I do not decide that, compliance does.
- How stable is the mix month to month? A split learned on one month can drift.

**Approach:**
1. Compute rates: 270 / 3,000 = 9.0%, 24 / 3,000 = 0.8%, 6 / 4,000 = 0.15%. Overall 300 / 10,000 = 3.0%.
2. Share found by the top two buckets: (270 + 24) / 300 = 98% using 6,000 reviews. Random order would find about 180.
3. Be honest about the 6 cases in the bottom bucket: 2% of confirmed cases. Whether they are material is a compliance question, not a modelling one.
4. Propose for the bottom bucket (as a proposal, not a decision): keep the alerts, route them to a faster lower-touch review or batch review, and audit a random sample every month.
5. Know the sample's limit: a 5% sample is 200 alerts with an expected 0.3 cases. You cannot track a 0.15% rate with that. Use a larger sample or a rolling quarter, or examine the 6 missed cases qualitatively.
6. Ask compliance in writing: may any alert class go unreviewed, with what sampling and sign-off, and what evidence they need (rates with intervals, the missed cases described).
7. Prospective check: run the model ranking in shadow for a few months so the numbers are not only retrospective, and re-validate the cut-offs.

**Metrics:**
- Confirmed rate per bucket = confirmed alerts / alerts in the bucket.
- Capture at capacity = confirmed in reviewed buckets / all confirmed (98%).
- Missed share = confirmed in unreviewed buckets / all confirmed (2% if bottom skipped).
- Review hours per confirmed case, per bucket.
- Guardrails: time-to-review for the top bucket, severity of missed cases, a shadow sample's confirmed rate by bucket.

**Risks:**
- Retrospective selection: if reviewed alerts were prioritised by the old rules, the bottom bucket was reviewed less thoroughly.
- Adversaries learn the pattern and aim at the "safe" bucket.
- Concept drift: the 0.15% is a month, not a law.
- Treating the model as the control. Compliance owns the control; the model supports prioritisation.

**What the interviewer scores:**
- Strong: all three rates and 98% right, plus "capacity equals the top two buckets". Weak: only accuracy-style talk.
- Strong: proposes sampling and low-touch review, defers the stop decision to compliance. Weak: "just drop the bottom 4,000".
- Strong: notes the sample-size problem of auditing a 0.15% bucket. Weak: "audit 5% and see".
- Strong: asks how retrospective labels were obtained. Weak: takes the counts at face value.

**Example:** 10,000 alerts, 300 confirmed. Top: 270 / 3,000 = 9%. Middle: 24 / 3,000 = 0.8%. Bottom: 6 / 4,000 = 0.15%. 294 / 300 = 98% found in 6,000 reviews. To see even one case in a random pull from the bottom bucket with 95% probability you need about 2,000 alerts.
- Weak: "98% recall, so we can stop reviewing the bottom bucket."
- Strong: "Reviewing the top two buckets catches 98% of confirmed cases with the capacity we have. I would not switch the bottom off myself: I would propose batch review and a monthly sample, show compliance the missed-case descriptions and rates with intervals, and let them decide."

**Code:**
```python
# Q23 alert triage buckets (illustrative, retrospective counts)
b = {"top": (3_000, 270), "middle": (3_000, 24), "bottom": (4_000, 6)}
total_alerts = sum(n for n, _ in b.values())
total_conf = sum(c for _, c in b.values())
assert total_alerts == 10_000 and total_conf == 300
rate = {k: c / n for k, (n, c) in b.items()}
assert round(rate["top"], 4) == 0.09 and round(rate["middle"], 4) == 0.008 and round(rate["bottom"], 5) == 0.0015
print({k: f"{v:.2%}" for k, v in rate.items()}, f"overall {total_conf/total_alerts:.1%}")

top2 = b["top"][1] + b["middle"][1]
share = top2 / total_conf
assert top2 == 294 and share == 0.98
print(f"top two buckets: 6,000 alerts, {top2} of {total_conf} confirmed = {share:.0%}")
print(f"missed if bottom never reviewed: {b['bottom'][1]} cases ({b['bottom'][1]/total_conf:.0%})")

# Lift versus random review of 6,000 alerts
random_found = 6_000 * (total_conf / total_alerts)
assert random_found == 180
print(f"random order would find ~{random_found:.0f}; model finds {top2}")

# Sampling the bottom bucket: how many to read to expect to see >=1 case with 95% probability at 0.15%?
import math
n95 = math.log(0.05) / math.log(1 - rate["bottom"])
assert 1_990 < n95 < 2_010
print(f"alerts to sample for 95% chance of seeing one case at 0.15%: {n95:,.0f}")
# A 5% monthly sample of the bottom bucket
sample = 0.05 * 4_000
exp_cases = sample * rate["bottom"]
assert sample == 200 and abs(exp_cases - 0.3) < 1e-9
print(f"5% sample = {sample:.0f} alerts, expected cases {exp_cases:.1f}: far too few to track the rate monthly")
```

**Output (my run):**
```text
{'top': '9.00%', 'middle': '0.80%', 'bottom': '0.15%'} overall 3.0%
top two buckets: 6,000 alerts, 294 of 300 confirmed = 98%
missed if bottom never reviewed: 6 cases (2%)
random order would find ~180; model finds 294
alerts to sample for 95% chance of seeing one case at 0.15%: 1,996
5% sample = 200 alerts, expected cases 0.3: far too few to track the rate monthly
```

**Follow-ups:**
- Why not move the bucket edge instead? You can, but the middle bucket still holds 24 cases; edges follow cost and capacity, and I would show the marginal cases per extra 1,000 reviews.
- How would you improve the model? Features from entity history and network links, and label the ones analysts rated "borderline" rather than binary only.
- What if analysts' capacity falls to 4,000? Then the top bucket plus 1,000 of the middle; show the capture curve.

**Common mistakes:** Calling 98% "recall of fraud" when it is recall of confirmed alerts in last month's data. Forgetting that the overall base rate is 3%. Dropping a bucket without compliance. Assuming 5% sampling measures a 0.15% rate.

### Q24 ⭐⭐ 🟡 E-commerce: In a randomised test, 10,000 cart abandoners received a reminder with a 10% discount code and 6.0% purchased, against 5.0% of 10,000 randomly held-out abandoners, and the average order value is 800 with a 25% margin before any discount. Compute the incremental orders per 10,000 abandoners, then compare the margin on them with the discount given if we assume all 600 purchasing recipients use the code. What would you change about the offer and the targeting?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to cart abandonment and discount incrementality in e-commerce material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The reminder created 600 - 500 = 100 extra orders per 10,000, worth 100 x 200 = 20,000 of margin, but if all 600 buyers use the 80 discount that costs 48,000, so the offer loses about 28,000 per 10,000 abandoners.

**Clarifying questions:**
- How many buyers actually redeem the code? The prompt assumes all 600 use it, which is the worst case for cost; redemption below 100% changes the answer (the net is -28,000 at 100% and -4,000 at 50%, and only turns positive below about 42% redemption).
- Are the 800 order value and 25% margin the same for incremental buyers as for baseline buyers? Discount-driven buyers may buy smaller baskets.
- Does the reminder alone (without a code) already lift purchase? The test mixes reminder and discount, so I cannot separate them.
- Is there a long-run effect: do buyers learn to abandon and wait for a code? One 30-day window may miss it.
- Is 25% margin before discount including shipping and payment fees? It sets the break-even.

**Approach:**
1. Incremental orders: 6.0% - 5.0% = 1.0 points x 10,000 = 100. Check the lift is not noise: z is about 3.1 on 10,000 per arm, so it is unlikely to be chance (I report the z and the setup, not a claim beyond it).
2. Margin on incremental orders: 100 x 800 x 25% = 20,000.
3. Discount given if all 600 purchasers use the code: 600 x 80 = 48,000. Net: -28,000 per 10,000.
4. Name the mechanism: 500 of the 600 buyers would have bought anyway, so most of the discount subsidises people who needed no incentive.
5. Break-even: with all buyers redeeming, I need about 333 incremental orders per 10,000 (8.3% purchase rate versus 5.0%), over three times the observed lift.
6. Change the offer: test a smaller discount, a reminder without a code, free shipping or a time-limited code, and a code that applies only to a threshold basket.
7. Change the targeting: hold out or skip high-propensity abandoners (those most likely to buy anyway), and give the code only to the middle group using an uplift model trained on this randomised data.
8. Re-test with three arms (no reminder, reminder only, reminder with code) so the discount's own incremental effect is measured.

**Metrics:**
- Incremental orders per 10,000 = purchases in treated minus purchases in holdout, same denominator.
- Incremental margin = incremental orders x AOV x margin rate.
- Discount cost = redeemed codes x discount amount, including codes redeemed by baseline buyers.
- Net per 10,000 = incremental margin - discount cost.
- Guardrails: AOV, return rate, repeat purchase in 60 days, unsubscribe rate.

**Risks:**
- Redemption below 100% makes the offer look better; measure it, do not assume.
- Margin for incremental orders may be lower than 25%.
- Training buyers to wait for codes.
- Targeting on past redemption only reinforces who already buys.
- Window too short: a pull-forward from later purchases would make incremental look larger than the true effect.

**What the interviewer scores:**
- Strong: 100 orders, 20,000, 48,000, net -28,000, all hand-checkable. Weak: "6% beats 5%, so it works."
- Strong: points out the 500 baseline buyers receive the discount. Weak: calls the code a "cost of acquisition" and stops.
- Strong: proposes a three-arm test and uplift targeting. Weak: "make the discount smaller" with no test.
- Strong: asks about redemption rate. Weak: assumes 100%.

**Example:** Per 10,000: 600 treated buyers vs 500 held out. Margin on 100 extra orders = 20,000. Discount if all 600 redeem = 48,000. With 50% redemption (illustrative) the discount is 24,000 and the net is -4,000; 70% gives 33,600 and -13,600. The same 100 extra orders only pay for the discount if redemption is below 41.7% (20,000 / 48,000).
- Weak: "The test is significant, so send the code to everyone."
- Strong: "The lift is real but small: 100 orders is 20,000 of margin against up to 48,000 of discount, because 500 of the 600 buyers would have bought anyway. I would test a reminder without a code and a smaller offer, and aim the code at people with the highest uplift."

**Code:**
```python
# Q24 cart reminder with 10% code (illustrative numbers)
from math import sqrt
n = 10_000
t_buy, c_buy = 600, 500
assert t_buy / n == 0.06 and c_buy / n == 0.05
incr = t_buy - c_buy
assert incr == 100
aov, margin = 800, 0.25
unit_margin = aov * margin
assert unit_margin == 200
incr_margin = incr * unit_margin
assert incr_margin == 20_000
disc_each = 0.10 * aov
discount_all = t_buy * disc_each
assert disc_each == 80 and discount_all == 48_000
net = incr_margin - discount_all
assert net == -28_000
print(f"incremental orders {incr}, margin on them {incr_margin:,.0f}, discount if all 600 use code {discount_all:,.0f}, net {net:,.0f}")

# Is 6.0% vs 5.0% a real lift? two-proportion z
p = (t_buy + c_buy) / (2 * n)
se = sqrt(p * (1 - p) * 2 / n)
z = (0.06 - 0.05) / se
assert 3.0 < z < 3.2
print(f"z = {z:.2f}")

# Break-even incremental orders x with all buyers using the code: x*200 = (500+x)*80
x = 500 * disc_each / (unit_margin - disc_each)
assert abs(x - 333.333) < 0.01
print(f"break-even incremental orders per 10,000: {x:.0f} (purchase rate {(500+x)/n:.2%} vs 5.00% baseline)")

# Net per 10,000 if only a share of purchasers redeem (invented redemption rates)
for r in (1.0, 0.7, 0.5):
    cost = r * t_buy * disc_each
    print(f"redemption {r:.0%}: discount {cost:,.0f}, net {incr_margin - cost:,.0f}")
assert incr_margin - 0.5 * t_buy * disc_each == -4_000
be = incr_margin / (t_buy * disc_each)
assert abs(be - 0.41667) < 1e-4
print(f"break-even redemption (same 100 extra orders): {be:.1%}")
# Smaller offer: 5% off with the same 100 incremental (only if lift held, a big if)
small = 0.05 * aov * t_buy
print(f"5% code, same lift, 100% redemption: discount {small:,.0f}, net {incr_margin - small:,.0f}")
assert small == 24_000 and incr_margin - small == -4_000
```

**Output (my run):**
```text
incremental orders 100, margin on them 20,000, discount if all 600 use code 48,000, net -28,000
z = 3.10
break-even incremental orders per 10,000: 333 (purchase rate 8.33% vs 5.00% baseline)
redemption 100%: discount 48,000, net -28,000
redemption 70%: discount 33,600, net -13,600
redemption 50%: discount 24,000, net -4,000
break-even redemption (same 100 extra orders): 41.7%
5% code, same lift, 100% redemption: discount 24,000, net -4,000
```

**Follow-ups:**
- What if the discount is a fixed 80 off a minimum basket of 1,000? It filters to bigger baskets, but it still goes to baseline buyers; test it.
- How do you pick the targeting group? Fit an uplift model on the randomised arms, check the lift by decile on a holdout, send to the deciles with positive net.
- Is a 10-point discount ever worth it? Yes if the incremental orders carry enough margin or lifetime value; that is an assumption to test, not to presume.

**Common mistakes:** Treating all 600 buyers as incremental. Ignoring that baseline buyers redeem the code. Counting the discount only on the 100 incremental orders and forgetting that the 500 baseline buyers redeem it too. Reading significance as profitability.

### Q25 ⭐⭐ 🟡 Healthcare: A chest X-ray model is tested on 10,000 images, 8,000 from scanner A and 2,000 from scanner B, with 10% of images abnormal in both groups. At the deployed threshold its sensitivity is 88% on scanner A and 71% on scanner B (measured). Compute the overall sensitivity and the abnormal scans missed in each group, and say how you would investigate the gap and what you would do before the hospital adds a third scanner model.
**Asked at:** Clinical-ML deployment material (a physician-oriented dataset-shift article, an arXiv paper on what clinicians want from explainable ML, a JMIR paper on alarm fatigue and a circEWS slide deck on calibration and prevalence); research and secondary sources rather than interview banks; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Overall sensitivity is 846 of 1,000 abnormal scans, 84.6%, but that hides 96 missed on scanner A and 58 on scanner B, so scanner B misses 29% of its abnormal cases against 12% on A, and I would not let a third scanner in until it has its own validation.

**Clarifying questions:**
- Is the threshold the same for both scanners, and where was it tuned? If it was tuned on scanner A, B is just off-operating-point.
- Are the 2,000 scanner B images from the same patients, wards and indications as A? A different case mix would fake or hide a gap.
- Who labelled the images and how (radiologist read, follow-up)? Label quality may differ by scanner.
- Was scanner B represented in training? If not, it is a domain shift problem.
- What is the clinical cost of a miss versus a false alert, and who owns the decision to use the tool on B? Ask the clinical safety team.

**Approach:**
1. Compute abnormal counts: 800 on A (10% of 8,000) and 200 on B (10% of 2,000).
2. True positives: 704 (A) + 142 (B) = 846, so overall sensitivity is 84.6%. Missed: 96 + 58 = 154.
3. B is 20% of images but 38% of misses (58 / 154).
4. Is the gap real? 200 abnormal cases is a small sample, but the 95% Wilson intervals (about 64.4-76.8% for B and 85.6-90.1% for A) do not overlap, and the gap has z of about 5. I would treat it as real and investigate.
5. Investigate: sensitivity versus threshold per scanner (ROC per scanner), case-mix check (finding type and size, view, patient factors), image properties (contrast, resolution, post-processing), label audit, and what B images look like in the model's embedding space.
6. Quick mitigations: scanner-specific threshold only if it keeps false alerts acceptable, and fine-tuning or augmentation on B images, then re-test on unseen B data.
7. Before the third scanner: a pre-deployment checklist. Silent-mode run on that scanner's images with radiologist reads; at least about 250 abnormal cases for a plus-or-minus 5 point sensitivity interval (about 2,460 images at 10% abnormal); a scanner-level monitor after go-live. Hospital governance decides the go/no-go.

**Metrics:**
- Sensitivity per scanner = abnormal scans flagged / abnormal scans, by scanner.
- Specificity or false-alert rate per scanner (the threshold trade-off needs both).
- Miss count per 1,000 scans per scanner.
- Subgroup sensitivity by finding type and by size.
- Guardrails: alert rate per scanner, radiologist override rate, time to read.

**Risks:**
- A scanner-specific threshold boosts sensitivity but raises false alerts and workload.
- Scanner B may stand in for a site or population effect, not the hardware.
- Over-fitting to B's 200 positives.
- Silent drift when a scanner is upgraded or its protocol changes.
- Reporting only the pooled 84.6%.

**What the interviewer scores:**
- Strong: 846, 154, 96 and 58 right, and the "38% of misses from 20% of images" point. Weak: only the overall number.
- Strong: separates case mix, labels, threshold and image properties. Weak: "retrain with more data".
- Strong: asks for specificity too. Weak: raises sensitivity without cost.
- Strong: a concrete pre-deployment plan for scanner three with a sample size. Weak: "monitor after".

**Example:** 800 abnormal on A, 88% caught: 704 found, 96 missed. 200 abnormal on B, 71% caught: 142 found, 58 missed. Pooled 846 / 1,000 = 84.6%. If B matched A, 34 more of its abnormal scans would be caught.
- Weak: "Overall sensitivity is 85%, so it is fine."
- Strong: "Overall is 84.6%, but B misses 29% of abnormal scans, 58 of 154 misses from a fifth of the images. I would look at the threshold per scanner, case mix and labels, and require a silent-mode validation on any new scanner before it goes live."

**Code:**
```python
# Q25 chest X-ray scanner gap (illustrative numbers)
from math import sqrt
nA, nB, prev = 8_000, 2_000, 0.10
posA, posB = nA * prev, nB * prev
assert posA == 800 and posB == 200 and nA + nB == 10_000
sA, sB = 0.88, 0.71
tpA, tpB = posA * sA, posB * sB
missA, missB = posA - tpA, posB - tpB
assert round(tpA) == 704 and round(tpB) == 142 and round(missA) == 96 and round(missB) == 58
overall = (tpA + tpB) / (posA + posB)
assert abs(overall - 0.846) < 1e-9
print(f"overall sensitivity {overall:.1%}; missed A={missA:.0f} B={missB:.0f}; B share of misses {missB/(missA+missB):.0%} with 20% of images")

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
loA, hiA = wilson(tpA, posA); loB, hiB = wilson(tpB, posB)
assert hiB < loA   # intervals do not overlap
print(f"A {loA:.1%}-{hiA:.1%}, B {loB:.1%}-{hiB:.1%}")
se = sqrt(sA*(1-sA)/posA + sB*(1-sB)/posB)
z = (sA - sB) / se
assert 4.9 < z < 5.1
print(f"gap 17 points, z={z:.1f}")

# If B had A's sensitivity it would miss this many fewer
extra = posB * (sA - sB)
assert round(extra) == 34
print(f"abnormal scans on B that A-level sensitivity would have caught: {extra:.0f}")

# Abnormal cases needed to estimate sensitivity of the new scanner within +-5 points (95%), assume 0.8
need_pos = 1.96**2 * 0.8 * 0.2 / 0.05**2
images = need_pos / prev
assert 245 < need_pos < 247 and 2_450 < images < 2_470
print(f"abnormal cases needed {need_pos:.0f} -> about {images:,.0f} images at 10% abnormal")
```

**Output (my run):**
```text
overall sensitivity 84.6%; missed A=96 B=58; B share of misses 38% with 20% of images
A 85.6%-90.1%, B 64.4%-76.8%
gap 17 points, z=5.0
abnormal scans on B that A-level sensitivity would have caught: 34
abnormal cases needed 246 -> about 2,459 images at 10% abnormal
```

**Follow-ups:**
- Can you just set a lower threshold for B? Possibly, but check false alerts for B first; it moves along the ROC curve and does not fix a weaker model.
- How do you monitor after go-live? Alert rate and positive rate by scanner against the validation baseline, plus a sampled radiologist audit.
- What if B and A have different patient populations? Then adjust or stratify; scanner and population effects are confounded unless you compare the same case type.

**Common mistakes:** Reporting pooled sensitivity only. Reporting accuracy at a 10% prevalence. Concluding scanner B is the cause with no case-mix check. Tuning a threshold on the test set. Forgetting false alerts.

### Q26 ⭐⭐ 🟡 Ads: A new campaign has 500 impressions and 2 clicks, a raw click rate of 0.4%. The platform has no history for the advertiser and the category's average click rate is 1.5%, which you treat as a prior worth 200 impressions. Compute the prior-shrunk estimate, explain why the raw number should not drive the bid, and describe an exploration plan with a stopping rule and a cap on spend.
**Asked at:** Ads ML and calibration material (Dataford questions on CTR calibration and click-through rate at an ad-tech firm, AlgoMaster and Educative ad click prediction system-design pages with calibration-error checks by probability bin); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The shrunk click rate is (2 + 3) / (500 + 200) = 0.71%, not the raw 0.40%, because 2 clicks is almost no evidence, and I would bid on the shrunk estimate while exploring with a capped budget and a written stopping rule.

**Clarifying questions:**
- What is the campaign optimising for: clicks, or a conversion behind the click? If conversion, the click rate is only the first factor in value per impression.
- How was 1.5% chosen: average of the whole category, or of similar advertisers, formats and placements? A prior from the wrong group misleads, and "worth 200 impressions" is a choice, not a fact.
- Is the creative new or one the platform has seen elsewhere? A known creative needs less exploration.
- What is the budget and the cost per thousand impressions? They set how many impressions I can afford to learn from.
- Who bears the spend risk, the advertiser or the platform? It decides how strict the cap must be.

**Approach:**
1. Shrink: prior of 1.5% x 200 = 3 pseudo-clicks in 200 pseudo-impressions, i.e. a Beta(3, 197). Posterior mean is (2 + 3) / (500 + 200) = 5 / 700 = 0.714%.
2. Show the uncertainty: the posterior 90% interval is about 0.28% to 1.30%. Even with the prior, we do not know the rate within a factor of four.
3. Say why the raw 0.4% should not drive the bid: with 2 clicks, one more or one fewer click moves it by 50%. Bid on the expected value, which uses the posterior, and do not let a lucky or unlucky start lock the campaign in or out.
4. Calibration point: bid is roughly predicted click rate x value per click. If the predicted rate is too low the campaign starves; too high and we overspend. A check by probability bin is the later test.
5. Exploration plan: give the new campaign a small guaranteed exposure (for example 3,000 impressions), use Thompson-style sampling from the posterior to allocate beyond that, and update in batches of 500.
6. Stopping rule written before launch: stop exploring and either scale or drop when the posterior probability that the click rate is below 1.0% exceeds 90% (drop) or falls under 5% (scale), or when the cap is reached.
7. Cap: a hard spend limit (illustratively 60 at 20 per thousand impressions, i.e. 3,000 impressions). Review at the cap, do not auto-extend.
8. Handle the prior's weight as a parameter: show the shrunk rate for weights of 100, 200 and 400 impressions and see whether the decision changes.

**Metrics:**
- Shrunk CTR = (clicks + prior_ctr x prior_n) / (impressions + prior_n).
- Posterior probability that CTR is below a business threshold.
- Spend to date versus cap, and cost per click realised.
- Calibration: predicted versus observed click rate by probability bin once there is volume.
- Guardrails: invalid-click credits and frequency per user.

**Risks:**
- A prior that is too strong hides a great new advertiser; too weak lets noise move bids.
- Exploration overspend: always cap by money, not by time.
- Click fraud or accidental clicks inflating the early rate.
- Position and placement effects: new campaigns often get worse slots, which lowers the rate.
- A single category average hides sub-segments.

**What the interviewer scores:**
- Strong: 0.714% shown as (2+3)/(500+200) and an interval. Weak: "0.4%, so bid low" or "just use 1.5%".
- Strong: explains why 2 clicks is noise, with numbers. Weak: says "sample is small" and nothing else.
- Strong: exploration with a stop rule and a money cap. Weak: "run it for a week".
- Strong: asks how the prior was built. Weak: treats 1.5% as truth.

**Example:** 2 clicks in 500 impressions. The posterior mean is 0.714% and the 90% interval is about 0.28% to 1.30%; the chance the true rate is under the 1.5% category average is about 98% (illustrative prior). With a cap of 60 at 20 per thousand impressions, 3,000 impressions are affordable.
- Weak: "It is only 0.4%, so we should not bid on it."
- Strong: "Raw is 0.4% on two clicks. Blending with the category prior gives 0.71% with a wide range, so I bid on 0.71%, give it a small capped exploration budget, and decide at the stop rule: below 1% with 90% confidence we drop it, otherwise we scale."

**Code:**
```python
# Q26 new campaign CTR with a prior worth 200 impressions (illustrative numbers)
import numpy as np
from scipy import stats
imps, clicks = 500, 2
raw = clicks / imps
prior_ctr, prior_n = 0.015, 200
a0, b0 = prior_ctr * prior_n, (1 - prior_ctr) * prior_n      # Beta(3, 197)
assert abs(a0 - 3) < 1e-9 and abs(b0 - 197) < 1e-9
post_mean = (clicks + a0) / (imps + prior_n)
assert abs(raw - 0.004) < 1e-12 and abs(post_mean - 5 / 700) < 1e-12
print(f"raw {raw:.3%}, shrunk {post_mean:.3%}  (= (2+3)/(500+200) = 5/700)")

# Uncertainty: 90% credible intervals
a1, b1 = a0 + clicks, b0 + imps - clicks
lo, hi = stats.beta.ppf([0.05, 0.95], a1, b1)
print(f"posterior 90% interval {lo:.2%} to {hi:.2%}")
assert 0.0027 < lo < 0.0030 and 0.0129 < hi < 0.0132
# raw-only (flat prior) interval is wider
rlo, rhi = stats.beta.ppf([0.05, 0.95], clicks + .5, imps - clicks + .5)
assert rlo < lo and rhi < hi   # raw-only data sit lower and are not narrower
print(f"raw-only (Jeffreys) 90% interval {rlo:.2%} to {rhi:.2%}")
p_below = stats.beta.cdf(0.015, a1, b1)
print(f"P(true CTR < category average 1.5%) = {p_below:.3f}")
assert 0.97 < p_below < 0.99

# Exploration plan: spend cap and stopping rule (invented cost: 20 per 1,000 impressions)
cpm, cap = 20.0, 60.0
max_imps = int(cap / cpm * 1000)
assert max_imps == 3_000
print(f"cap {cap:.0f} buys {max_imps} impressions at CPM {cpm:.0f}")
# Expected course if the true CTR is 0.7% (seeded simulation, batches of 500)
rng = np.random.default_rng(7)
true = 0.007
a, b = a1, b1
n_new = 0
while n_new < max_imps:
    k = rng.binomial(500, true); a += k; b += 500 - k; n_new += 500
    p_low = stats.beta.cdf(0.010, a, b)      # stop (drop) if probably below 1.0%
    if p_low > 0.90 or p_low < 0.05:
        break
print(f"stopped after {n_new} new impressions, posterior mean {a/(a+b):.3%}, P(CTR<1.0%)={p_low:.2f}, spent {n_new*cpm/1000:.0f}")
assert n_new <= max_imps and n_new * cpm / 1000 <= cap
```

**Output (my run):**
```text
raw 0.400%, shrunk 0.714%  (= (2+3)/(500+200) = 5/700)
posterior 90% interval 0.28% to 1.30%
raw-only (Jeffreys) 90% interval 0.11% to 1.10%
P(true CTR < category average 1.5%) = 0.979
cap 60 buys 3000 impressions at CPM 20
stopped after 2500 new impressions, posterior mean 0.750%, P(CTR<1.0%)=0.94, spent 50
```

**Follow-ups:**
- What if the advertiser already ran elsewhere? Use their history as part of the prior, with a discount for the new channel.
- How do you choose the prior weight? From how much real campaigns in the category vary (the prior spread), not by feel; fit on past campaigns' counts.
- What about conversions arriving late? Click rate learns quickly; for conversions, model delay or the early read will look worse than it is.

**Common mistakes:** Using the raw rate. Using the category average as truth. No spend cap. Stopping on a fixed time rather than evidence. Forgetting that the prior's weight is an assumption.

### Q27 ⭐⭐ 🟡 Fintech: In one day of 1,000,000 transactions a model sends 2,000 to a block band, 18,000 to a step-up band (an extra confirmation) and lets 980,000 pass, with measured fraud counts of 1,200 in the block band, 600 in the step-up band and 200 in the pass band. Assume blocking stops every fraud in its band, the step-up stops 80% of fraud in its band and 10% of the 17,400 genuine customers in the step-up band abandon. The fraud counts in the block band come from review and customer reports. Compute the fraud stopped, the fraud that still gets through, the genuine customers blocked and the genuine customers lost at step-up, and discuss how you would set the band edges.
**Asked at:** Payments-fraud material (2025 SciTePress, Atlantis Press and SDMIMD papers and student projects on UPI fraud detection frame false alerts, class imbalance and retraining on confirmed fraud and false-positive reports); academic and self-published material, no interview bank for this exact framing; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Of 2,000 frauds the bands stop 1,200 + 480 = 1,680 (84%), 320 get through (120 past step-up, 200 in the pass band), 800 genuine customers are blocked and 1,740 genuine customers are lost at step-up; I would set the edges by cost per band, not by a round score.

**Clarifying questions:**
- How were the fraud counts in each band measured? Blocked transactions never produce a chargeback, and the prompt says the block-band counts come from review and customer reports. How complete is that review? Missed fraud there would move the table.
- The 10% abandonment applies to the 17,400 genuine customers, giving 1,740. Does it also apply to fraudsters who give up? That would only raise fraud stopped.
- What does a missed fraud cost on average, and what does a blocked or lost genuine customer cost (support, churn, lost margin)? The edges depend on this ratio.
- Is step-up capacity limited (OTP delivery, call centre)? Capacity can cap the band size.
- Do fraudsters adapt to the step-up (for example pass it with stolen devices)? The 80% is an assumption to monitor.

**Approach:**
1. Total fraud: 1,200 + 600 + 200 = 2,000 in 1,000,000 transactions (0.2%).
2. Stopped: block stops all 1,200; step-up stops 80% of 600 = 480. Total 1,680, 84% of fraud.
3. Fraud through: 600 - 480 = 120 past step-up, plus 200 in the pass band = 320.
4. Genuine customers hit: block band 2,000 - 1,200 = 800 blocked. Step-up band 18,000 - 600 = 17,400 genuine, of whom 10% abandon = 1,740 lost.
5. Band quality: block band is 60% fraud; step-up band is 3.33%; pass band is 0.02%. Step-up costs 1,740 lost customers to stop 480 frauds, about 3.6 per fraud stopped.
6. Set edges from costs: block when the fraud probability times the loss exceeds the cost of a wrong block; step-up when 80% of the loss avoided exceeds the friction plus abandonment cost. With invented costs (2,500 per fraud, 150 per false block, about 55 per step-up genuine customer) the break-evens are about 5.7% for block and 2.7% for step-up. Both are illustrative.
7. Because the block band is at 60%, the block edge could move down toward the step-up band, as long as the calibration holds; check by sliding the edge and reading the bands' observed fraud rates on held-out days.
8. Validate: calibrated probabilities (reliability by bin), stable by merchant type and hour, a small random holdout (a share of transactions passed with silent scoring) so labels are not only from what the policy allowed.
9. Ask the fraud policy and compliance owners what limits there are on blocking and customer communication; I do not state them.

**Metrics:**
- Fraud stopped rate = fraud stopped / all fraud (84%).
- Fraud loss through = amount of fraud passing (count 320, weight by amount).
- False-positive customers = genuine blocked (800) and genuine lost at step-up (1,740) per day.
- Step-up pass rate and abandonment rate by cohort.
- Guardrails: approval rate, complaint rate, call-centre load.

**Risks:**
- Labels in the block band are censored: confirmed fraud is only known if someone checks.
- The 80% stop rate and 10% abandonment are assumptions that change with the step-up method.
- Fraud shifting from the block band to the step-up or pass band once fraudsters learn.
- Counting by transaction when loss is by amount: a few big frauds in the pass band matter more.
- Edges tuned on one day (counts of 200 and 600 are small).

**What the interviewer scores:**
- Strong: 1,680, 320, 800 and 1,740, shown with the 17,400. Weak: applies 10% to all 18,000 or leaves out the 120.
- Strong: sets edges with a cost ratio and break-even probability. Weak: "pick a threshold at the elbow".
- Strong: flags that blocked-band labels are censored. Weak: trusts "measured" counts without question.
- Strong: includes a holdout to keep learning. Weak: retrains only on outcomes the policy allowed.

**Example:** 2,000 fraud, 1,680 stopped, 320 through. Block band: 800 genuine blocked (60% precision). Step-up band: 17,400 genuine, 1,740 lost, 480 fraud stopped. With the invented costs the break-even fraud probability is about 5.7% for block and 2.7% for step-up.
- Weak: "We stop 84% of fraud, so the model is good."
- Strong: "84% stopped, 320 through, but 2,540 genuine customers were hurt, 800 blocked and 1,740 lost at step-up. I would pick the edges from the cost of a missed fraud versus a lost customer, check calibration by band and keep a small silent holdout so my labels are not biased."

**Code:**
```python
# Q27 fraud bands (illustrative numbers, one day)
total = 1_000_000
band = {"block": (2_000, 1_200), "step": (18_000, 600), "pass": (980_000, 200)}
assert sum(n for n, _ in band.values()) == total
fraud = sum(f for _, f in band.values())
assert fraud == 2_000
stop_block = band["block"][1]
stop_step = 0.8 * band["step"][1]
stopped = stop_block + stop_step
assert stop_step == 480 and stopped == 1_680
through = fraud - stopped
assert through == 320
# of which: 120 pass step-up, 200 in pass band
assert band["step"][1] - stop_step == 120
gen = {k: n - f for k, (n, f) in band.items()}
assert gen == {"block": 800, "step": 17_400, "pass": 979_800}
lost_step = 0.10 * gen["step"]
assert lost_step == 1_740
print(f"fraud total {fraud}, stopped {stopped:.0f} ({stopped/fraud:.0%}), through {through:.0f}")
print(f"genuine blocked {gen['block']}, genuine lost at step-up {lost_step:.0f}")
for k, (n, f) in band.items():
    print(f"{k:5} flagged {n:>7} fraud {f:>5} fraud rate {f/n:.2%}")
assert round(1_200/2_000, 2) == 0.60 and round(600/18_000, 4) == 0.0333

# Choosing the edges: expected cost per 1,000 in a band, invented costs
loss_per_fraud = 2_500      # average loss if fraud gets through
block_fp = 150              # cost of a wrongly blocked genuine customer (care, lost sale, churn)
step_fp = 0.10 * 400        # 10% abandon x 400 lost margin (invented), per genuine customer stepped up
step_cost = 15              # friction cost per step-up customer
def block_gain(p):          # benefit minus cost of blocking one txn with fraud probability p
    return p * loss_per_fraud - (1 - p) * block_fp
def step_gain(p):
    return p * 0.8 * loss_per_fraud - (1 - p) * step_fp - step_cost
print(f"block band (p=60%): gain per txn {block_gain(0.6):,.0f}")
print(f"step band (p=3.33%): gain per txn {step_gain(600/18_000):,.1f}")
# break-even fraud probabilities
p_block = block_fp / (loss_per_fraud + block_fp)
p_step = (step_fp + step_cost) / (0.8 * loss_per_fraud + step_fp)
print(f"break-even p: block above {p_block:.1%}, step-up above {p_step:.2%}")
assert abs(p_block - 0.0566) < 1e-3 and abs(p_step - 0.0269) < 1e-3
assert block_gain(0.6) > 0 and step_gain(600/18_000) > 0
```

**Output (my run):**
```text
fraud total 2000, stopped 1680 (84%), through 320
genuine blocked 800, genuine lost at step-up 1740
block flagged    2000 fraud  1200 fraud rate 60.00%
step  flagged   18000 fraud   600 fraud rate 3.33%
pass  flagged  980000 fraud   200 fraud rate 0.02%
block band (p=60%): gain per txn 1,440
step band (p=3.33%): gain per txn 13.0
break-even p: block above 5.7%, step-up above 2.70%
```

**Follow-ups:**
- Why not step up everything? 980,000 genuine customers would face friction to catch 200 frauds; the cost dominates.
- What if step-up capacity is 10,000 a day? Shrink the band to the top 10,000 by score and recompute the table; lower fraud stopped.
- How would you set the pass edge? Where the marginal fraud probability equals the break-even for step-up, checked per segment.

**Common mistakes:** Counting all 18,000 as genuine. Omitting the 200 frauds in the pass band. Judging a band by recall only. Forgetting censored labels. Reporting counts without amounts.

### Q28 ⭐⭐ 🟡 E-commerce: 400,000 of 2,000,000 listings (20%) lack a colour attribute. A model can fill it, with a measured accuracy of 97% on a 1,000-item audit for the 280,000 listings where its confidence is at least 0.9 and 78% on a 1,000-item audit for the other 120,000. Compute the expected wrong colours when filling only the confident ones and when filling all, treating the audit accuracies as projections, and say how you would decide, given that wrong colours drive returns.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to catalogue attribute quality and extraction in e-commerce material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Filling only the 280,000 confident listings gives about 8,400 wrong colours (3% of 280,000), filling all 400,000 gives about 34,800 (8,400 plus 26,400 from the other 120,000 at 22% wrong), so I would fill the confident ones, send the rest to review or leave them blank, and decide the cut-off from the cost of a wrong colour.

**Clarifying questions:**
- What does a wrong colour cost (return rate, refund, trust), and what does a correct one earn (search visibility, filter use)? The break-even accuracy depends on this ratio.
- Is a missing colour harmful today, or just invisible to colour filters? A blank is not a wrong answer.
- How was the 1,000-item audit sampled (random within each group, or from popular items)? A biased audit moves the projection.
- Is the 97% the same across categories (multi-colour items, patterns, white vs cream)? A single number can hide a bad category.
- Can fills be shown as "suggested" or labelled by source, and can sellers correct them?

**Approach:**
1. Wrong when filling the confident group: 280,000 x (1 - 0.97) = 8,400.
2. Wrong when filling everything: 8,400 + 120,000 x (1 - 0.78) = 8,400 + 26,400 = 34,800.
3. Say these are projections from two 1,000-item audits. The 95% half-widths are about 1.1 points for the 97% group (so about 5,400 to 11,400 wrong) and about 2.6 points for the 78% group (about 23,300 to 29,500 wrong). I would carry the ranges, not point values.
4. The marginal decision: the extra 120,000 fills add 26,400 wrong and 93,600 right. If a wrong colour costs five times what a right colour earns (invented), the break-even accuracy is 5 / (1 + 5) = 83.3%, so the 97% group passes and the 78% group fails.
5. Options for the 120,000: leave blank, route to human or seller confirmation, show as "suggested" with a lower confidence flag, or use a second model or the product image plus title agreement as an extra gate.
6. Pick the confidence cut-off by a sweep: accuracy and volume by confidence bin, from a fresh audit, not from the model's own scores alone.
7. Monitor after launch: sampled audits per category, return rate by filled-versus-seller-entered colour, and seller corrections.
8. Phase it: fill the confident listings first, then measure returns with a holdout of listings that stay blank.

**Metrics:**
- Fill rate = listings with a colour / all listings (rises from 80% to 94% by filling the confident group).
- Precision of fills = correct fills / fills, by confidence bin and category.
- Wrong fills per 1,000 listings and their return-rate impact.
- Net value = right fills x B - wrong fills x C.
- Guardrails: colour-related return rate, seller disputes, search click-through on colour filters.

**Risks:**
- Confidence scores not calibrated, so 0.9 means different accuracy in different categories.
- Audit accuracy on a 1,000 sample is noisy and may not match the live mix.
- Wrong colours cluster in categories where colour matters most (fashion).
- Feedback loop: filled colours become training labels.
- Value assumptions (B and C) are guesses.

**What the interviewer scores:**
- Strong: 8,400 and 34,800 with the 26,400 explained. Weak: "97% and 78%, average them".
- Strong: calls the figures projections and gives the audit's uncertainty. Weak: treats 3% as exact.
- Strong: decides by cost of wrong versus value of right, with a break-even accuracy. Weak: "fill everything for coverage".
- Strong: offers human review or labelled suggestions for the uncertain group. Weak: only fill or not fill.

**Example:** 400,000 missing. Confident 280,000 at 97%: 271,600 right, 8,400 wrong. The rest 120,000 at 78%: 93,600 right, 26,400 wrong. If a wrong fill costs 5 and a right fill earns 1 (invented), the confident group nets +0.82 per fill and the rest nets -0.32 per fill.
- Weak: "Overall accuracy would be about 91%, good enough, fill them all."
- Strong: "Filling all gives about 34,800 wrong colours against 8,400 for the confident group. The extra 120,000 are 22% wrong, and wrong colours cause returns, so I would hold them for review, and decide the cut-off with a fresh audit and a cost ratio."

**Code:**
```python
# Q28 colour attribute filling (illustrative numbers; audit accuracies treated as projections)
from math import sqrt
total, missing = 2_000_000, 400_000
assert missing / total == 0.20
conf_n, low_n = 280_000, 120_000
assert conf_n + low_n == missing
acc_c, acc_l = 0.97, 0.78
wrong_c = conf_n * (1 - acc_c)
wrong_l = low_n * (1 - acc_l)
assert round(wrong_c) == 8_400 and round(wrong_l) == 26_400 and round(wrong_c + wrong_l) == 34_800
print(f"fill confident only: {wrong_c:,.0f} wrong of {conf_n:,}; fill all: {wrong_c+wrong_l:,.0f} wrong of {missing:,}")
print(f"the extra {low_n:,} fills add {wrong_l:,.0f} wrong ({1-acc_l:.0%} wrong) and {low_n-wrong_l:,.0f} right")

# Audit uncertainty: 1,000 items per audit, 95% normal-approx half-width
def hw(p, n=1000): return 1.96 * sqrt(p * (1 - p) / n)
hc, hl = hw(acc_c), hw(acc_l)
print(f"audit half-widths: confident +-{hc:.1%} -> wrong range {conf_n*(1-acc_c-hc):,.0f} to {conf_n*(1-acc_c+hc):,.0f}; "
      f"rest +-{hl:.1%} -> {low_n*(1-acc_l-hl):,.0f} to {low_n*(1-acc_l+hl):,.0f}")
assert 0.010 < hc < 0.012 and 0.025 < hl < 0.027

# Decision: fill only where accuracy exceeds C/(B+C). Invented values: benefit of a right fill B=1, cost of a wrong fill C=5
B, C = 1.0, 5.0
be = C / (B + C)
assert abs(be - 5/6) < 1e-12
for name, a in (("confident", acc_c), ("rest", acc_l)):
    gain = a * B - (1 - a) * C
    print(f"{name}: accuracy {a:.0%}, net value per fill {gain:+.2f} (break-even accuracy {be:.1%})")
assert 0.97 * B - 0.03 * C > 0 and 0.78 * B - 0.22 * C < 0
# Human review of the rest: what accuracy after review if a reviewer fixes 80% of its errors (invented)?
fixed = low_n * (1 - acc_l) * 0.8
print(f"review of the rest at 80% error catch: wrong falls from {wrong_l:,.0f} to {wrong_l-fixed:,.0f}")
assert round(wrong_l - fixed) == 5_280
```

**Output (my run):**
```text
fill confident only: 8,400 wrong of 280,000; fill all: 34,800 wrong of 400,000
the extra 120,000 fills add 26,400 wrong (22% wrong) and 93,600 right
audit half-widths: confident +-1.1% -> wrong range 5,440 to 11,360; rest +-2.6% -> 23,319 to 29,481
confident: accuracy 97%, net value per fill +0.82 (break-even accuracy 83.3%)
rest: accuracy 78%, net value per fill -0.32 (break-even accuracy 83.3%)
review of the rest at 80% error catch: wrong falls from 26,400 to 5,280
```

**Follow-ups:**
- How big should the audit be? For half-width of 1 point at 97% you need about 1,100 per group; at 78% about 6,600. Compute from p(1-p) and the target width.
- What if the model is confident but wrong in one category? Report accuracy per category and set category-specific thresholds or exclusions.
- Can you use seller feedback? Yes, as a signal and for labels, but beware selection: only some sellers correct.

**Common mistakes:** Mixing the two audits into one blended accuracy. Calling projections facts. Ignoring that a blank is cheaper than a wrong value. Using the model's confidence without an audit. Ignoring category differences.

### Q29 ⭐⭐ 🟡 Healthcare: A sepsis model was built at hospital 1 with an AUC of 0.88 and external tests give an AUC of 0.79 at hospital 2 and 0.84 at hospital 3, with a calibration slope of 0.6 at hospital 2 (1.0 is ideal). The sepsis rate is 4% at hospital 3 and 2.5% at hospital 2, and your team wants at least 100 expected events at each site before trusting its numbers. Compute the minimum patients needed per site and describe a rollout plan with local recalibration, monitoring and stop rules.
**Asked at:** Clinical-AI external-validation coverage (Fierce Healthcare, MedCity News and JAMA Internal Medicine pages on the external validation of a widely deployed sepsis model, which reported low sensitivity, a modest positive predictive value, alerts on a large share of patients and a billing-code outcome definition; a newsletter piece on local validation and tracking override patterns); published news and research, not an interview bank; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** At 100 expected events you need 100 / 0.04 = 2,500 patients at hospital 3 and 100 / 0.025 = 4,000 at hospital 2, but that is only about even odds of actually reaching 100, so I would plan for roughly 2,900 and 4,700, then roll out in silent mode with local recalibration, monitoring and written stop rules.

**Clarifying questions:**
- How is "sepsis" defined at each site (clinical criteria, billing code, treatment trigger)? Different definitions can explain part of the AUC drop and the 4% versus 2.5% rate.
- Which patients are in scope (all admissions, emergency department, wards)? The denominator changes the rate and the alert burden.
- Who acts on an alert and how many alerts per shift can they handle? It sets the threshold.
- Are the 100 events counted per patient or per episode? Repeat episodes inflate events.
- Who signs off a clinical deployment (clinical safety, a governance committee)? I propose, they decide; I ask them what review is required.

**Approach:**
1. Minimum patients for an expected 100 events: hospital 3 is 100 / 0.04 = 2,500; hospital 2 is 100 / 0.025 = 4,000.
2. The prompt asks for 100 expected events, so 2,500 and 4,000 are the answer. State the stricter option too: with 2,500 patients at 4% the chance of at least 100 events is about 51%. For a 95% chance, plan for about 2,916 (hospital 3) and 4,671 (hospital 2).
3. Say what 100 events buys: sensitivity of 0.70 is known only within about plus-or-minus 9 points, and an AUC of 0.79 within about plus-or-minus 5 points. Treat it as a floor for checking calibration, not as a precise estimate.
4. Read the shifts: AUC 0.88 to 0.79 means worse ranking at hospital 2; slope 0.6 means predicted risks are too extreme (high predictions are overstated), so the same score does not mean the same risk. Hospital 3 at 0.84 is a smaller drop.
5. Recalibrate locally first: fit an intercept and slope on the first local data (a logistic recalibration), check calibration by bin, and set the threshold from the local alert capacity.
6. Silent mode first: score patients, show nothing, collect outcomes. Then limited go-live on selected wards with clinician review of alerts.
7. Monitor: weekly alerts per 1,000 patients, PPV against the local label, sensitivity on a sampled chart review, calibration slope by month, and override and ignore rates.
8. Stop rules (agreed in advance with clinical owners): pause if the alert rate or PPV leaves an agreed band for a set period, if calibration slope falls outside an agreed range, if the data feed breaks, or if a safety event is linked to an alert. Resume only after review.

**Metrics:**
- Events per site = patients with the outcome / patients in scope; the denominator in the sample-size maths.
- AUC and calibration slope and intercept per site, each with an interval.
- PPV and alerts per 1,000 patients at the chosen threshold.
- Sensitivity from audited events (including those the model missed).
- Guardrails: time to antibiotics (as a process measure), override rate, alert fatigue signals.

**Risks:**
- A billing-code outcome can lag and miss early cases; the label may reward coding, not clinical sepsis.
- Treatment contamination: clinicians acting on alerts change the outcomes the model learns from later.
- With 100 events the intervals are wide; do not over-read differences between sites.
- Recalibration fixes risk levels but not a weaker ranking.
- Alert burden: at a plausible operating point, 161 alerts per 1,000 patients with PPV about 9% is a lot.

**What the interviewer scores:**
- Strong: 2,500 and 4,000 right, and offers the 95%-chance figures as a stricter option. Weak: stops at the division or adds the two numbers.
- Strong: reads calibration slope 0.6 correctly (too extreme). Weak: reads only AUC.
- Strong: concrete stop rules and silent mode before go-live. Weak: "monitor drift".
- Strong: says clinical owners decide. Weak: states what a regulator requires.

**Example:** Hospital 3 expects 100 events in 2,500 patients, about 2,900 for a 95% chance. Hospital 2 needs 4,000, about 4,700. At hospital 2 with an invented operating point (sensitivity 0.60, specificity 0.85) PPV is 9.3% and 161 of every 1,000 patients alert. A predicted 20% risk would be about 9.1% after slope recalibration.
- Weak: "AUC 0.79 is fine, deploy and watch."
- Strong: "I need about 4,000 patients at hospital 2 and 2,500 at hospital 3 for 100 expected events, and more for safety. I run silent mode, recalibrate locally since the slope is 0.6, set the threshold on alert capacity, and agree stop rules with the clinical owners first."

**Code:**
```python
# Q29 sepsis external validation sample size and alert burden (illustrative numbers)
from math import sqrt
from scipy import stats
events_needed = 100
rate = {"hospital 2": 0.025, "hospital 3": 0.04}
for h, p in rate.items():
    n_exp = events_needed / p
    n = int(n_exp)
    while stats.binom.sf(events_needed - 1, n, p) < 0.95:
        n += 1
    print(f"{h}: rate {p:.1%}, patients for 100 expected events {n_exp:,.0f}; for a 95% chance of at least 100 events {n:,}")
assert 100 / 0.025 == 4_000 and 100 / 0.04 == 2_500
assert stats.binom.sf(99, 2_500, 0.04) < 0.55     # only about even odds at the expected count
print(f"P(>=100 events) with 2,500 patients at 4% = {stats.binom.sf(99, 2500, 0.04):.2f}")

# What do 100 events buy? 95% half-width of a sensitivity of 0.70 and of an AUC of 0.79 (Hanley-McNeil)
hw_sens = 1.96 * sqrt(0.7 * 0.3 / 100)
def auc_se(auc, npos, nneg):
    q1, q2 = auc / (2 - auc), 2 * auc**2 / (1 + auc)
    return sqrt((auc*(1-auc) + (npos-1)*(q1-auc**2) + (nneg-1)*(q2-auc**2)) / (npos*nneg))
se = auc_se(0.79, 100, 3_900)
print(f"sensitivity 0.70 on 100 events: +-{hw_sens:.3f}; AUC 0.79 with 100 events: +-{1.96*se:.3f}")
assert 0.08 < hw_sens < 0.10 and 0.04 < 1.96 * se < 0.07

# Alert burden at hospital 2 for an invented operating point (sens 0.60, spec 0.85)
sens, spec, p = 0.60, 0.85, 0.025
tp, fp = sens * p, (1 - spec) * (1 - p)
ppv = tp / (tp + fp)
alerts_per_1000 = 1000 * (tp + fp)
assert abs(ppv - 0.0930) < 1e-3 and round(alerts_per_1000) == 161
print(f"hospital 2 at sens 0.60 / spec 0.85: PPV {ppv:.1%}, alerts per 1,000 patients {alerts_per_1000:.0f}, true cases found {1000*tp:.0f} of {1000*p:.0f}")
# Calibration slope 0.6: predictions are too extreme; pull them toward the mean on the logit scale
import numpy as np
logit = lambda x: np.log(x / (1 - x)); expit = lambda z: 1 / (1 + np.exp(-z))
pred, mean_risk = 0.20, 0.025          # assume the average predicted risk equals the 2.5% event rate
adj = expit(logit(mean_risk) + 0.6 * (logit(pred) - logit(mean_risk)))
print(f"slope 0.6 pivoting at the mean: a predicted 20% risk is recalibrated to about {adj:.1%}")
assert 0.085 < adj < 0.095
```

**Output (my run):**
```text
hospital 2: rate 2.5%, patients for 100 expected events 4,000; for a 95% chance of at least 100 events 4,671
hospital 3: rate 4.0%, patients for 100 expected events 2,500; for a 95% chance of at least 100 events 2,916
P(>=100 events) with 2,500 patients at 4% = 0.51
sensitivity 0.70 on 100 events: +-0.090; AUC 0.79 with 100 events: +-0.053
hospital 2 at sens 0.60 / spec 0.85: PPV 9.3%, alerts per 1,000 patients 161, true cases found 15 of 25
slope 0.6 pivoting at the mean: a predicted 20% risk is recalibrated to about 9.1%
```

**Follow-ups:**
- Why 100 events? It is a common rule of thumb in the validation literature (editor knowledge, not checked here); more are better and the interval width is the real target.
- What if the sites' definitions differ? Re-label a sample of charts with one definition and compare.
- How do you handle the calibration slope without enough data? Pool a few months of silent-mode data, and keep the intercept and slope as monitored parameters.

**Common mistakes:** Dividing 100 by the rate and stopping. Treating AUC as the only metric. Deploying without local calibration. Using a billing code as truth without checking. No pre-agreed stop rules.

### Q30 ⭐⭐ 🟡 Ads: A lookalike audience built from 10,000 past converters was shown ads, reaching 500,000 users of whom 0.80% converted (4,000), while a group of 500,000 similar users, held out at random from the same lookalike audience before serving, saw none and 0.70% of them converted (3,500). The platform report attributes all 4,000 conversions to the campaign, which spent 40,000. Compute the reported and the incremental cost per conversion, and explain what the gap means and how you would improve the audience and the test.
**Asked at:** Ads measurement material (an eMarketer 2026 FAQ separating incrementality, multi-touch attribution and marketing mix modelling, Google ads-measurement data scientist postings asking for causal inference and attribution work, a Dataford incremental-lift question, a Remerge incrementality write-up); job postings and prep material rather than a confirmed interview round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The platform reports 40,000 / 4,000 = 10 per conversion, but only 4,000 - 3,500 = 500 conversions are incremental, so the incremental cost is 40,000 / 500 = 80, eight times higher, because 87.5% of the reported conversions would have happened anyway.

**Clarifying questions:**
- Was the held-out group drawn at random from the same lookalike audience before ads were served? The prompt says it was, and the result depends on that, so I would confirm it in the data (pre-period balance).
- Did the held-out group see other ads from the same advertiser or channel? That changes what "no exposure" means.
- What counts as a conversion and over what window? A long window picks up more organic conversions in both arms.
- What is a conversion worth (first order value, lifetime value)? Cost per conversion only means something against value.
- Does the audience exclude existing customers? Lookalikes built from converters often include people already converting.

**Approach:**
1. Reported cost per conversion: 40,000 / 4,000 = 10.
2. Incremental conversions: 4,000 - 3,500 = 500 (0.80% minus 0.70% is 0.10 points on 500,000 users). Incremental cost: 40,000 / 500 = 80.
3. Meaning of the gap: the platform credits every conversion among exposed users, including those who would have converted anyway. The audience was built from people who convert, so its natural conversion rate is high (0.70% with no ads).
4. Is the lift real? The 95% interval on incremental conversions is about 331 to 669, so the cost per incremental conversion is roughly 60 to 121. The lift is clearly above zero (z about 5.8) but the cost is uncertain by a factor of two. I report the range, not only 80.
5. Improve the audience: exclude existing customers and recent converters, target by predicted uplift (who converts because of the ad) rather than by similarity to converters, and test different seed sets and sizes.
6. Improve the test: randomise at the user level from the same audience before serving, use a holdout or ghost-ad or public service announcement control so exposure is comparable, pre-register the window and the metric, and check balance on pre-period behaviour.
7. Size the test from the effect you care about: detecting 0.80% versus 0.70% needs about 117,000 users per arm, so 500,000 per arm is ample for that lift; a lift half as large would need about four times more users.
8. Judge by incremental return: incremental conversions x value / spend, compared with other channels and with the margin, and keep a standing small holdout.

**Metrics:**
- Reported cost per conversion = spend / platform-attributed conversions (10).
- Incremental conversions = exposed-group conversions - holdout conversions, with equal group sizes (500).
- Cost per incremental conversion = spend / incremental conversions (80), with an interval.
- Relative lift = (0.80% - 0.70%) / 0.70% = 14.3%.
- Guardrails: reach and frequency, conversion window, balance of pre-period conversion rates between arms.

**Risks:**
- A non-random holdout makes the lift meaningless.
- Contamination: holdout users still see the advertiser elsewhere, understating the lift.
- Conversion windows or attribution differences between the platform and the test.
- Winner's curse if you pick the best of many audiences from one test.
- Applying 80 to a different audience or season.

**What the interviewer scores:**
- Strong: 10, 500 and 80 and the 87.5% anyway share, all hand-checkable. Weak: "incremental is lower" with no number.
- Strong: asks whether the holdout was randomised from the same audience. Weak: assumes it was.
- Strong: gives an interval and notes cost is uncertain. Weak: quotes 80 as precise.
- Strong: improves audience through uplift, exclusions and a standing holdout. Weak: "make the audience bigger".

**Example:** 4,000 exposed conversions against 3,500 in the holdout. Reported cost 40,000 / 4,000 = 10. Incremental cost 40,000 / 500 = 80. If the true incremental count is 331 to 669 the cost is about 121 to 60.
- Weak: "10 per conversion is great, scale it."
- Strong: "Ten is the platform's attributed number. The holdout shows 500 extra conversions, so it is 80 per incremental conversion, and the interval is roughly 60 to 121. Whether that is good depends on conversion value, so I would compare it to margin, exclude existing customers and test an uplift-targeted audience against this one."

**Code:**
```python
# Q30 lookalike campaign: reported vs incremental cost per conversion (illustrative numbers)
from math import sqrt
n_t = n_c = 500_000
conv_t, conv_c = 4_000, 3_500
assert conv_t / n_t == 0.008 and conv_c / n_c == 0.007
spend = 40_000
reported = spend / conv_t
assert reported == 10.0
incr = conv_t - conv_c
assert incr == 500
incr_cost = spend / incr
assert incr_cost == 80.0
print(f"reported cost per conversion {reported:.0f}; incremental {incr_cost:.0f}; ratio {incr_cost/reported:.0f}x")
print(f"share of reported conversions that would have happened anyway: {conv_c/conv_t:.1%}")
assert conv_c / conv_t == 0.875

# Interval on the lift (two-proportion, unpooled SE)
p_t, p_c = conv_t / n_t, conv_c / n_c
se = sqrt(p_t*(1-p_t)/n_t + p_c*(1-p_c)/n_c)
lo, hi = (p_t - p_c) - 1.96*se, (p_t - p_c) + 1.96*se
inc_lo, inc_hi = lo * n_t, hi * n_t
print(f"incremental conversions 95% interval {inc_lo:.0f} to {inc_hi:.0f}; cost per incremental {spend/inc_hi:.0f} to {spend/inc_lo:.0f}")
assert 325 < inc_lo < 335 and 665 < inc_hi < 675
z = (p_t - p_c) / sqrt((p_t+p_c)/2 * (1-(p_t+p_c)/2) * 2 / n_t)
assert 5.5 < z < 6.0
print(f"z = {z:.1f}")

# Relative lift and what a better audience could do (invented): same spend, same reach, lift doubles
rel = (p_t - p_c) / p_c
assert abs(rel - 1/7) < 1e-9
print(f"relative lift {rel:.1%}")
better = spend / 1000
print(f"if lift were 1,000 incremental conversions at the same spend: cost per incremental {better:.0f}")
assert better == 40.0

# Holdout sizing: control needed to detect a 0.1-point lift on a 0.7% base, per arm (alpha .05, power .8)
from statistics import NormalDist
zz = NormalDist().inv_cdf
n = (zz(.975)+zz(.8))**2 * (0.008*0.992 + 0.007*0.993) / 0.001**2
print(f"users per arm to detect 0.80% vs 0.70%: {n:,.0f}")
assert 100_000 < n < 120_000
```

**Output (my run):**
```text
reported cost per conversion 10; incremental 80; ratio 8x
share of reported conversions that would have happened anyway: 87.5%
incremental conversions 95% interval 331 to 669; cost per incremental 60 to 121
z = 5.8
relative lift 14.3%
if lift were 1,000 incremental conversions at the same spend: cost per incremental 40
users per arm to detect 0.80% vs 0.70%: 116,846
```

**Follow-ups:**
- What if the platform will not give you a holdout? Use a geo test or a conversion-lift study offered by the platform, and say the control is less clean.
- Is the platform's number wrong? It answers a different question (conversions after exposure); both numbers can be correct for their own definition.
- How do you combine this with attribution and mix models? Use the experiment to calibrate them; the experiment is the anchor for the incremental effect on this campaign.

**Common mistakes:** Quoting platform-attributed cost as the return. Treating the holdout as valid without checking randomisation. Ignoring the uncertainty of a difference of two proportions. Choosing the audience by similarity to converters only.

### Q31 ⭐⭐ 🟡 Fintech: A credit model declined an applicant and the lender must give up to 4 plain-language reasons. Income and employment tenure have a correlation of 0.85, so their attribution scores flip between two retrains, and for 30 of 100 reviewed declines (30% of the sample) the top reason differs between retrains. How would you produce stable reasons, validate them, and decide what to ask compliance about the wording?
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Correlated features make per-feature attributions unstable, so I would explain the decline in stable reason groups (income and tenure as one "income and job stability" reason), average attributions over many retrains, test the stability on declines before launch, and ask compliance whether the wording and grouping are acceptable.

**Clarifying questions:**
- Do the reasons have to reflect the real drivers of this model, or can they be mapped from a simpler scorecard? It decides whether grouping is enough or we need a different model form.
- Which wording is fixed by compliance (a reason-code library) and which can I change? It tells me where I can group features.
- Is the flip between two retrains, or between two runs on the same model? Retrain instability is a data issue; same-model instability is a method issue (for example sampling in the attribution).
- How was the 30 of 100 chosen (the first 100 declines, or random)? A sample of 100 gives a wide range.
- Are the 4 reasons ranked or just a set? A ranked list needs stable order; a set only needs stable membership.

**Approach:**
1. Size the problem. 30 of 100 is a sample. The 95% Wilson interval is about 22% to 40%, so the true flip rate is probably between a fifth and two fifths. Also measure the overlap of the whole 4-reason set, not only the top reason.
2. Find the cause. With a correlation of 0.85 the model can put credit on income or on tenure almost interchangeably. Check the spread of the two coefficients across bootstrap retrains: they move in opposite directions (negative correlation between the two coefficients).
3. Group correlated features into one reason group before ranking (income + tenure = "income and employment stability"). Rank groups, not single features.
4. Average attributions over many bootstrap retrains (bagging) and use the average for the reason, so one retrain does not decide the wording.
5. Map each group to a fixed reason code with plain wording written with compliance, so the text cannot change between retrains.
6. Validate: (a) stability: top-reason flip rate and 4-reason set overlap across retrains on a fixed set of reviewed declines; (b) fidelity: if you remove the named reason feature(s), does the score move in the right direction (counterfactual check); (c) human review: a reviewer reads 100 declines and says whether each reason is sensible for that applicant.
7. Put a stability gate in the retrain pipeline: do not promote a retrain if the flip rate on the reference declines is above an agreed limit.
8. Ask compliance (and legal, via the usual route) about: the exact reason wording, whether grouped reasons are acceptable, how many reasons and in what order, how reasons must relate to the model, and how long reason mappings must be kept. I do not assert any rule; I bring the evidence and ask.

**Metrics:**
- Top-reason flip rate = declines whose top reason differs between retrain A and B / declines reviewed (here 30 / 100 in the prompt).
- Set overlap = mean over declines of |A ∩ B| / |A ∪ B| for the 4-reason sets (Jaccard).
- Fidelity = share of declines where removing the cited feature group lowers risk (counterfactual check).
- Guardrails: model discrimination (AUC) must not fall when we regularise or group; reason coverage (declines with at least one valid reason).

**Risks:**
- Ranking by coefficient times deviation on a correlated pair is arbitrary; two retrains can both be "right".
- Grouping can hide a driver the applicant could act on (income versus tenure advice differs).
- Averaging over retrains gives stable but possibly less faithful reasons for a single model; document which model the reasons explain.
- Plain-language wording that sounds stable may still imply something untrue; get it reviewed.
- The 100-decline sample may not cover thin-file applicants.

**What the interviewer scores:**
- Strong: names correlated features as the cause, sizes the 30 of 100 with an interval, and proposes grouping plus averaging with a measured result.
- Strong: separates stability from fidelity and tests both.
- Strong: asks compliance about wording and does not state regulations as facts.
- Weak: "use SHAP" with no stability check; "drop one of the two features" without checking AUC; quoting legal rules from memory.

**Example:** Illustrative numbers, from the run below. A logistic model on 1,500 simulated applicants, income and tenure correlated at about 0.85, reasons for 100 highest-risk applicants from two bootstrap retrains.
- Raw top reason differs for 47 of 100 (the prompt's 30 of 100 is the same kind of number); grouped income and tenure: 12 of 100; bagged (60 resamples each): 17 of 100.
- Weak: "Income is the top reason for most people, we ship the SHAP output."
- Strong: "On 100 declines the top reason changes in 30, so the true rate could be 22% to 40%. Income and tenure are correlated at 0.85, so I would report them as one reason group and average over retrains. In my test that cut the flip rate from 47 to 12 of 100, and grouping changes only the explanation, so AUC is untouched. I would ask compliance to approve the group wording."

**Code:**
```python
import numpy as np

rng = np.random.default_rng(31)
names = ["income", "tenure", "debt_ratio", "utilisation", "inquiries", "file_age"]
n, p = 1500, len(names)
cov = np.eye(p)
cov[0, 1] = cov[1, 0] = 0.85            # income and tenure correlated at 0.85
X = rng.multivariate_normal(np.zeros(p), cov, size=n)
beta_true = np.array([-0.45, -0.45, 0.50, 0.40, 0.25, -0.20])
pd_true = 1 / (1 + np.exp(-(-2.0 + X @ beta_true)))
y = (rng.random(n) < pd_true).astype(float)
print("sample corr(income, tenure) =", round(np.corrcoef(X[:, 0], X[:, 1])[0, 1], 3))
assert abs(np.corrcoef(X[:, 0], X[:, 1])[0, 1] - 0.85) < 0.03

def fit(Xb, yb, l2=1e-3, it=25):
    A = np.c_[np.ones(len(Xb)), Xb]
    w = np.zeros(A.shape[1])
    for _ in range(it):                     # IRLS (Newton) for logistic regression
        mu = 1 / (1 + np.exp(-(A @ w)))
        W = mu * (1 - mu)
        H = A.T @ (A * W[:, None]) + l2 * np.eye(A.shape[1])
        w = w + np.linalg.solve(H, A.T @ (yb - mu) - l2 * w)
    return w

def retrain(seed):
    r = np.random.default_rng(seed)
    idx = r.integers(0, n, n)               # a retrain = a fresh resample of the same population
    return fit(X[idx], y[idx])

# 100 reviewed declines: the 100 highest-risk applicants under the reference model
w_ref = fit(X, y)
risk = np.c_[np.ones(n), X] @ w_ref
dec = np.argsort(-risk)[:100]
mu_x = X.mean(0)

def contrib(w, rows):                       # linear-logit attribution: coef * (x - mean)
    return w[1:] * (X[rows] - mu_x)

def top(w, rows, groups=None):
    c = contrib(w, rows)
    if groups is not None:
        c = np.c_[[c[:, g].sum(1) for g in groups]].T
    return c.argmax(1), np.argsort(-c, 1)[:, :4]

wa, wb = retrain(1), retrain(2)
ta, sa = top(wa, dec); tb, sb = top(wb, dec)
flip = int((ta != tb).sum())
print("raw top reason differs between two retrains:", flip, "of 100")
jac = np.mean([len(set(a) & set(b)) / len(set(a) | set(b)) for a, b in zip(sa, sb)])
print("mean Jaccard overlap of the 4-reason sets (raw):", round(jac, 3))

groups = [[0, 1], [2], [3], [4], [5]]       # income+tenure merged into one reason group
ga, _ = top(wa, dec, groups); gb, _ = top(wb, dec, groups)
gflip = int((ga != gb).sum())
print("grouped (income+tenure = one reason) top reason differs:", gflip, "of 100")

def bagged(seed0, B=60):
    return np.mean([retrain(seed0 + b) for b in range(B)], axis=0)
ba, bb = bagged(1000), bagged(2000)
tba, _ = top(ba, dec); tbb, _ = top(bb, dec)
bflip = int((tba != tbb).sum())
print("bagged coefficients (60 resamples each), raw top reason differs:", bflip, "of 100")

# validation numbers: how big is 30 of 100? Wilson interval for the prompt's sample
def wilson(k, m, z=1.96):
    ph = k / m; d = 1 + z * z / m
    c = (ph + z * z / (2 * m)) / d
    h = z * np.sqrt(ph * (1 - ph) / m + z * z / (4 * m * m)) / d
    return c - h, c + h
lo, hi = wilson(30, 100)
print("prompt: 30 of 100 =", 30 / 100, "| 95% Wilson interval", round(lo, 3), "to", round(hi, 3))
assert 30 / 100 == 0.3 and 0.21 < lo < 0.22 and 0.39 < hi < 0.40
print("coefficient sd across 60 resamples (income, tenure):",
      np.round(np.std([retrain(5000 + b)[1:3] for b in range(60)], axis=0), 3))
corr_ab = np.corrcoef(np.array([retrain(5000 + b)[1:3] for b in range(60)]).T)[0, 1]
print("corr of income and tenure coefficient across resamples:", round(corr_ab, 3))
print("true coefficients", dict(zip(names, beta_true.tolist())))
assert flip == 47 and gflip == 12 and bflip == 17 and round(jac, 3) == 0.884
assert gflip < flip and bflip < flip
assert corr_ab < -0.7
```

**Output (my run):**
```
sample corr(income, tenure) = 0.857
raw top reason differs between two retrains: 47 of 100
mean Jaccard overlap of the 4-reason sets (raw): 0.884
grouped (income+tenure = one reason) top reason differs: 12 of 100
bagged coefficients (60 resamples each), raw top reason differs: 17 of 100
prompt: 30 of 100 = 0.3 | 95% Wilson interval 0.219 to 0.396
coefficient sd across 60 resamples (income, tenure): [0.169 0.154]
corr of income and tenure coefficient across resamples: -0.819
true coefficients {'income': -0.45, 'tenure': -0.45, 'debt_ratio': 0.5, 'utilisation': 0.4, 'inquiries': 0.25, 'file_age': -0.2}
```

**Follow-ups:**
- *Why not just drop tenure?* You lose information and AUC may fall; test it. Also the applicant loses an accurate reason. Grouping keeps both.
- *Could a monotone or scorecard model make this easier?* Often yes: constrained or additive models give fixed point contributions. Test AUC cost against reason stability.
- *How do you handle the reviewer who says the reason is wrong for this person?* Counterfactual check plus a log; repeated complaints become a test case in the stability gate.

**Common mistakes:**
- Treating one retrain's ranking as the truth.
- Reporting a flip rate from 100 declines with no interval.
- Grouping features without checking that the group wording is accurate for each member.
- Quoting legal requirements as facts instead of asking compliance.

### Q32 ⭐⭐ 🟡 E-commerce: A seller-risk model flags 1,000 sellers for review, an audit of 100 randomly chosen flagged sellers confirmed 40 as fraudulent (40%, a sample), and investigators can review 200 sellers a week. Estimate the fraudulent sellers among the 1,000 flagged as a projection, the weeks to clear the queue, and the number expected in the first week if the queue is reviewed in random order. How would you order the queue instead?
**Asked at:** Marketplace-trust material (a prachub Amazon fake-review question on detection signals and impact metrics, an Interview Query fake-review prompt and DoorDash and Thumbtack data scientist guides on marketplace analytics); prep-site material and one estimate-based news item, no confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** About 400 of the 1,000 flagged sellers are fraudulent as a projection (the audit is a sample, so roughly 300 to 500), the queue takes 5 weeks at 200 a week, and random order finds about 80 in week 1; I would order by expected fraud harm per review, not at random.

**Clarifying questions:**
- Was the audit of 100 truly random among the 1,000 flagged, and who judged "fraudulent" (the same investigators)? A non-random or inconsistent audit breaks the 40%.
- Do I have the model score for each audited seller? It lets me measure how precision changes with score.
- How long does fraud keep costing us while a seller waits (daily losses, buyer harm)? It sets the value of speed.
- Can a review be cheap (auto-triage) for some sellers? Review time per seller may differ.
- What is the action on a confirmed seller (suspend, hold funds, ask for documents), and what is the cost of wrongly suspending a good seller? It sets the cost of false positives.

**Approach:**
1. Compute the projection and its range. 40 of 100 is 40%, so 0.40 x 1,000 = 400 fraudulent among the flagged. A 95% interval on 40 of 100 is 30.4% to 49.6%, so 304 to 496 sellers.
2. Weeks to clear: 1,000 / 200 = 5 weeks.
3. Random order, week 1: 200 reviews x 40% = 80 fraudulent expected (hypergeometric, standard deviation about 6.2). If the true number is 304 or 496 the week-1 mean is 60.8 or 99.2.
4. Better order: rank by expected harm avoided per review minute = P(fraud) x exposure (money at risk, buyers affected, growth rate of sales) / expected review time. Use the model score only after checking it is calibrated on the audited sample.
5. Use the audit to calibrate: tabulate fraud rate by score band. With an invented split (high band 21 of 30, middle 13 of 35, low 6 of 35) the high band is 70% and reviewing it first gives 140 expected in week 1 instead of 80.
6. Keep a random slice of each week's review (for example 10%) so the model is evaluated on a fair sample and the labels do not become biased.
7. Fast actions for the top of the queue (hold payouts or limit listings pending review) can reduce damage before the investigator arrives; ask the trust and policy team what actions are allowed.
8. Re-score the queue daily as new signals arrive; the order is not fixed for 5 weeks.

**Metrics:**
- Precision of review = confirmed fraud / sellers reviewed.
- Fraud found per investigator-hour, and expected loss prevented per week (sum of P(fraud) x exposure for reviewed sellers).
- Time to action for confirmed fraud (median days from flag to action).
- Guardrails: false-suspension rate (good sellers actioned / sellers actioned), appeals overturned, and fraud rate in the random slice.

**Risks:**
- Projection from 100 audits has a wide range, about +/- 10 points.
- Ordering by score only finds what the model already likes; sellers it misses are never audited (keep the random slice).
- If fraudsters adapt to the order, the top band becomes less pure.
- Optimising fraud counts alone can starve large exposure sellers; use harm, not count.

**What the interviewer scores:**
- Strong: 400, 5 weeks, 80 in week 1, and says "sample, projection, range".
- Strong: orders by expected harm per review and keeps a random audit slice.
- Strong: separates fraud count from money at risk.
- Weak: "review in order of arrival"; no mention of uncertainty; ignores false suspensions.

**Example:** Illustrative numbers. In the run below the projection is 400 (304 to 496), 5 weeks, 80 expected in week 1 under random order and 140 when the high-score band goes first. Ordering by probability times exposure finds fewer fraudsters in week 1 (about 110 versus 140 in my simulated exposures) but stops about 440,000 of expected loss instead of about 246,000.
- Weak: "We have 400 frauds, so we need 2 weeks of work."
- Strong: "The audit suggests about 400, plausibly 300 to 500. At 200 reviews a week that is 5 weeks, and random order finds about 80 in week 1. I would rank by fraud probability times money at risk per review minute, and keep a random 10% slice so the model stays honest."

**Code:**
```python
import numpy as np
from math import comb, sqrt

flagged, audited, fraud_s, cap = 1000, 100, 40, 200
p = fraud_s / audited
proj = flagged * p
weeks = flagged / cap
print("sample rate", p, "| projected fraudulent among flagged", proj, "| weeks to clear", weeks)
assert p == 0.4 and proj == 400 and weeks == 5

# uncertainty on the 40 of 100 (the audit is a sample)
z = 1.96
se = sqrt(p * (1 - p) / audited)
lo, hi = p - z * se, p + z * se
fpc = sqrt((flagged - audited) / (flagged - 1))
se2 = se * fpc
print("normal 95% interval:", round(lo, 3), "to", round(hi, 3), "-> sellers", round(lo * flagged), "to", round(hi * flagged),
      "| with finite-population correction", round((p - z * se2) * flagged), "to", round((p + z * se2) * flagged))
assert round(lo * flagged) == 304 and round(hi * flagged) == 496

# random review order: first week = 200 reviewed out of 1000 with K fraudulent (hypergeometric)
K = 400
mean1 = cap * K / flagged
sd1 = sqrt(cap * (K / flagged) * (1 - K / flagged) * (flagged - cap) / (flagged - 1))
print("week 1, random order: mean", mean1, "sd", round(sd1, 2))
assert mean1 == 80 and round(sd1, 2) == 6.20
for Kx in (304, 496):
    print("  if true K =", Kx, "-> week-1 mean", cap * Kx / flagged)

# ordering by score: invented audit table, 100 audited sellers split by model-score tertile
tiers = {"high score": (30, 21), "mid score": (35, 13), "low score": (35, 6)}   # (audited, fraud)
assert sum(a for a, f in tiers.values()) == 100 and sum(f for a, f in tiers.values()) == 40
rates = {k: f / a for k, (a, f) in tiers.items()}
print({k: round(v, 3) for k, v in rates.items()})
# project to 1000 flagged in the same tier shares (audited share = 30/35/35 percent)
size = {k: a * 10 for k, (a, f) in tiers.items()}
fr = {k: size[k] * rates[k] for k in tiers}
print("tier sizes", size, "| projected fraud", {k: round(v) for k, v in fr.items()}, "total", round(sum(fr.values())))
assert abs(sum(fr.values()) - 400) < 1e-9
# week 1 by score order: all 200 from high tier (300 sellers) + nothing else needed
wk1_score = cap * rates["high score"]
print("week 1 reviewing the high tier first: expected fraud found", wk1_score, "vs random", mean1)
assert wk1_score == 140
# value-ordered: add dollars at risk per seller (invented) -> expected loss per reviewer-hour
rng = np.random.default_rng(32)
exposure = rng.lognormal(7, 1, flagged)               # invented exposure per seller
pr = np.concatenate([np.full(300, .70), np.full(350, .3714), np.full(350, .1714)])
rng.shuffle(pr)
by_p = np.argsort(-pr)[:cap]
by_ev = np.argsort(-(pr * exposure))[:cap]
print("week-1 expected fraud caught: by probability", round(pr[by_p].sum(), 1), "| by probability x exposure", round(pr[by_ev].sum(), 1))
print("week-1 expected loss stopped: by probability", round((pr * exposure)[by_p].sum()), "| by probability x exposure", round((pr * exposure)[by_ev].sum()))
assert (pr * exposure)[by_ev].sum() >= (pr * exposure)[by_p].sum()
assert pr[by_p].sum() >= pr[by_ev].sum()
```

**Output (my run):**
```
sample rate 0.4 | projected fraudulent among flagged 400.0 | weeks to clear 5.0
normal 95% interval: 0.304 to 0.496 -> sellers 304 to 496 | with finite-population correction 309 to 491
week 1, random order: mean 80.0 sd 6.2
  if true K = 304 -> week-1 mean 60.8
  if true K = 496 -> week-1 mean 99.2
{'high score': 0.7, 'mid score': 0.371, 'low score': 0.171}
tier sizes {'high score': 300, 'mid score': 350, 'low score': 350} | projected fraud {'high score': 210, 'mid score': 130, 'low score': 60} total 400
week 1 reviewing the high tier first: expected fraud found 140.0 vs random 80.0
week-1 expected fraud caught: by probability 140.0 | by probability x exposure 109.7
week-1 expected loss stopped: by probability 245534 | by probability x exposure 440302
```

**Follow-ups:**
- *Is the 40% the precision of the model?* Only for the flagged group at the audit threshold; it tells nothing about unflagged sellers.
- *What if two weeks of delay matters a lot?* Add a time-decay weight, or take low-effort holds on the top band at once.
- *How do you get labels without bias if you only review the top?* The random slice plus periodic reviews of the unflagged.

**Common mistakes:**
- Saying "400 are fraudulent" as a fact.
- Reviewing in random order because it is "fair".
- Optimising count rather than harm.
- Forgetting the cost of wrongly acting on honest sellers.

### Q33 ⭐⭐ 🟡 Healthcare: An LLM drafts discharge summaries and two clinicians audited 200 of them, finding 14 with an omitted medication (7%) and 6 with an invented detail (3%), measured on that sample. Clinicians must sign every summary and say drafting saves 4 of the usual 10 minutes. Explain how you would define and measure harm, what audited error rate you would want to see before wider rollout, and what you would ask the clinical safety and compliance teams.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to LLM clinical documentation audit in 2025-2026 health-AI material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** I would define harm by clinical severity and by whether the error reached the patient record after the clinician signed, measure it with a blinded severity-graded audit compared with human-written summaries, and let clinical safety set the pass rate before wider rollout; 7% and 3% on 200 are samples with wide ranges.

**Clarifying questions:**
- What is the baseline: how often do human-written summaries omit a medication? It sets whether 7% is better or worse than today.
- Were the two clinicians blinded to source (human or LLM), and how often did they agree? Agreement shows whether the labels are reliable.
- Can one summary have both errors, and which medicines were missing? The 14 and the 6 may overlap, so any-error is between 7% and 10%.
- Did the reviewing clinicians use the same checking time as they will in production? A careful audit is slower than a busy ward sign-off.
- Who owns the decision (clinical safety officer, not the data team)? It decides who sets the threshold.

**Approach:**
1. State what the sample shows. 14 of 200 is 7.0% (95% Wilson 4.2% to 11.4%); 6 of 200 is 3.0% (1.4% to 6.4%). The "4 of 10 minutes" saving is what clinicians say; I treat it as a claim and measure it.
2. Define harm in tiers with clinical safety: omitted medication by drug class and by whether it matters (for example a stopped or new high-risk drug versus a minor supplement), invented detail by whether it changes a decision, and "reached the record" after sign-off versus caught in review. Weights belong to clinicians, not to me.
3. Measure per summary and per medication: errors / medications in the source (a per-medication denominator), and summaries with any error / summaries audited (per-summary).
4. Audit design: random sample stratified by ward and complexity, two blinded reviewers, adjudication of disagreements, human-written summaries mixed in as a baseline.
5. Rollout bar: ask clinical safety for the target. Show them what is testable: with zero errors seen, 299 clean audited summaries are needed to show the true rate is below 1% with 95% confidence, 149 for 2% and 59 for 5% (one-sided). Any error found raises the number. To pin a 7% rate within +/-1 point takes about 2,500 audits.
6. Staged rollout: shadow mode (draft not shown), then one ward with 100% audit, then widen; stop rules agreed in advance (any severe omission reaching the record pauses the rollout).
7. Product guards: show the medication list from the source side by side with the draft, flag medicines that appear in the record but not the draft, and make the clinician confirm the medication section explicitly.
8. Ask clinical safety and compliance (via their processes): who is accountable for a signed summary, how errors are reported and logged, patient-data handling for the drafting service, and what must be disclosed to patients. I make no claims about the rules.

**Metrics:**
- Medication omission rate (per summary) = summaries with at least one omitted medication / audited summaries (14 / 200).
- Per-medication omission rate = omitted medications / medications in the source (needs a count I do not have in the prompt).
- Invention rate = summaries with an invented detail / audited summaries (6 / 200), split by severity.
- Reached-the-record rate = errors still present after sign-off / audited summaries.
- Net time saved = (usual minutes - drafted-plus-review minutes) / usual minutes; compare with the claimed 4 of 10 (40%).
- Guardrails: reviewer agreement (kappa), error rate by ward and patient complexity.

**Risks:**
- Automation bias: clinicians sign what looks fluent, so signing is not a safety net by itself.
- Time saving can vanish if careful checking takes the saved minutes (4 saved minus 3 extra checking minutes leaves 1 minute, or 10%, in my illustration).
- Errors cluster in complex patients; an average hides them.
- Audit reviewers may be less careful after the first 50.

**What the interviewer scores:**
- Strong: severity-weighted harm, "reached the record" distinction, and a human baseline.
- Strong: honest about sample size and uses interval or zero-error sample sizes.
- Strong: hands the pass-rate decision to clinical safety and asks questions instead of asserting rules.
- Weak: "7% is low, ship"; "accuracy of the LLM" with no harm definition; claims about regulation.

**Example:** Illustrative numbers from the run. With the prompt's 200 audits: 7% omission (4.2% to 11.4%), 3% invention (1.4% to 6.4%). If signing clinicians catch 90% of errors, about 70 omissions and 30 inventions per 10,000 summaries reach the record; at a 50% catch rate, 350 and 150.
- Weak: "Only 3% hallucinate, and clinicians sign everything, so it is safe."
- Strong: "7% omission and 3% invention are samples with wide ranges. I would grade by severity, count what survives sign-off, compare with human summaries, and ask clinical safety for the rollout bar. To show under 1% with zero errors I would need about 300 clean audits."

**Code:**
```python
import math

def wilson(k, n, z=1.96):
    ph = k / n; d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

n = 200
for name, k in (("omitted medication", 14), ("invented detail", 6)):
    lo, hi = wilson(k, n)
    print(f"{name}: {k}/{n} = {k/n:.3f} | 95% Wilson {lo:.3f} to {hi:.3f}")
assert 14 / n == 0.07 and 6 / n == 0.03
lo14, hi14 = wilson(14, n); lo6, hi6 = wilson(6, n)
assert round(lo14, 3) == 0.042 and round(hi14, 3) == 0.114 and round(lo6, 3) == 0.014 and round(hi6, 3) == 0.064

# the two error types may overlap: summaries with any error is between 14 and 20 of 200
print("any error: between", 14 / n, "and", 20 / n, "(overlap unknown)")
assert 14 / n == 0.07 and 20 / n == 0.10

# zero-error audit sizes: how many clean summaries to show the true rate is below a target (95% one-sided)
for target in (0.05, 0.02, 0.01):
    m = math.ceil(math.log(0.05) / math.log(1 - target))
    print(f"target rate below {target:.0%}: need {m} audited summaries with zero errors (rule of three: 3/{target} = {3/target:.0f})")
assert math.ceil(math.log(0.05) / math.log(0.99)) == 299
assert math.ceil(math.log(0.05) / math.log(0.98)) == 149
assert math.ceil(math.log(0.05) / math.log(0.95)) == 59

# with the observed 7%, how big an audit to pin the rate within +-1 point?
m = math.ceil(1.96 ** 2 * 0.07 * 0.93 / 0.01 ** 2)
print("audit size for +-1 point at p=7%:", m)
assert m == 2501

# severity-weighted harm (invented weights and severity mix, to be set by clinical safety)
w = {"omitted: high-risk drug": 10, "omitted: other": 2, "invented: any": 5}
mix_omit_high = 0.2                      # assumption: 20% of omissions involve a high-risk drug
per_summary = 0.07 * (mix_omit_high * w["omitted: high-risk drug"] + (1 - mix_omit_high) * w["omitted: other"]) + 0.03 * w["invented: any"]
print("severity-weighted harm points per summary:", round(per_summary, 3))
assert round(per_summary, 3) == 0.402
# per 10,000 summaries: errors that reach the patient depend on clinician catch rate
for catch in (0.9, 0.5):
    reach_omit = 10000 * 0.07 * (1 - catch); reach_inv = 10000 * 0.03 * (1 - catch)
    print(f"if signing clinicians catch {catch:.0%} of errors: reaching the record per 10,000 summaries: omissions {reach_omit:.0f}, inventions {reach_inv:.0f}")
assert round(10000 * 0.07 * 0.1) == 70 and round(10000 * 0.07 * 0.5) == 350 and round(10000 * 0.03 * 0.5) == 150

# time: drafting 'saves 4 of 10 min' is a clinician statement, not measured; review time eats it
saved = 4 / 10
print("claimed saving", saved, "= 4 of 10 minutes; if careful checking costs 3 extra minutes the net saving is", 4 - 3, "minutes (", (4 - 3) / 10, ")")
assert (4 - 3) / 10 == 0.1
```

**Output (my run):**
```
omitted medication: 14/200 = 0.070 | 95% Wilson 0.042 to 0.114
invented detail: 6/200 = 0.030 | 95% Wilson 0.014 to 0.064
any error: between 0.07 and 0.1 (overlap unknown)
target rate below 5%: need 59 audited summaries with zero errors (rule of three: 3/0.05 = 60)
target rate below 2%: need 149 audited summaries with zero errors (rule of three: 3/0.02 = 150)
target rate below 1%: need 299 audited summaries with zero errors (rule of three: 3/0.01 = 300)
audit size for +-1 point at p=7%: 2501
severity-weighted harm points per summary: 0.402
if signing clinicians catch 90% of errors: reaching the record per 10,000 summaries: omissions 70, inventions 30
if signing clinicians catch 50% of errors: reaching the record per 10,000 summaries: omissions 350, inventions 150
claimed saving 0.4 = 4 of 10 minutes; if careful checking costs 3 extra minutes the net saving is 1 minutes ( 0.1 )
```

**Follow-ups:**
- *Is a lower error rate than humans enough?* Possibly not alone; different error types (fluent inventions) can be worse. Safety decides.
- *Why a per-medication denominator?* A summary with 15 medicines has more chances to miss one.
- *What if time savings are real but errors rise on complex patients?* Restrict to simple cases first.

**Common mistakes:**
- Treating the clinician signature as the safeguard.
- Reporting 7% and 3% as population rates without intervals.
- Adding 7% and 3% to get 10% (overlap unknown).
- Setting the acceptable threshold in the data team.

### Q34 ⭐⭐ 🔴 Fintech: A credit model's average predicted 12-month default probability is 3.0% across a portfolio of 20,000 loans, but 900 of them defaulted (4.5%, matured outcomes) while the AUC is unchanged at 0.80. Exposure is 10,000 per loan and the loss given default is assumed to be 50%. Compute the expected loss predicted, the loss from observed defaults at the assumed loss given default, and the shortfall, and explain the possible causes, whether you would recalibrate or rebuild, and how this goes through model governance.
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Predicted loss is 3,000,000 and the loss from observed defaults at the assumed 50% is 4,500,000, a shortfall of 1,500,000 (observed is 1.5 times predicted); ranking is intact (AUC 0.80), so this is a level problem, and I would first diagnose the cause, then recalibrate under model-governance sign-off unless the miss differs by segment.

**Clarifying questions:**
- Is the 4.5% measured on the same 12-month window and the same default definition used in training? A changed definition makes a model look wrong without being wrong.
- Is the portfolio mix the same as in development (new products, channels, score bands)? A mix shift changes the average PD even if the model is fine.
- Were macro conditions different this year? One year is one draw of the economy, so a common shock can move all defaults together.
- Is the 50% loss given default a policy number or something we have observed on recoveries? The loss figures use it only as an input, so realised recoveries should be checked separately.
- What does the model feed (approval cut-off, pricing, provisioning)? It sets urgency and who has to sign off.

**Approach:**
1. Do the arithmetic. Predicted defaults = 20,000 x 3.0% = 600; observed 900 (4.5%). Expected loss predicted = 20,000 x 0.03 x 10,000 x 0.5 = 3,000,000. Loss from observed defaults at the assumed LGD = 900 x 10,000 x 0.5 = 4,500,000. Shortfall = 1,500,000 (33.3% of observed, observed is 1.5x predicted).
2. Is it noise? If defaults were independent, the standard deviation of the count at 3% is about 24, so 900 is about 12 standard deviations above 600. But defaults are not independent. With a small pairwise default correlation of 0.001 the gap is only about 2.7 design-effect units, so a common economic shock is plausible. Do not call it noise and do not call it proof of a broken model.
3. Check calibration by score band and by segment, not only the average. Plot predicted versus observed default rate by decile and by product and vintage.
4. List causes and test each: macro shock, mix shift towards riskier applicants, drift in a key feature, changed default or label definition, data pipeline change, selection effect from approvals (reject inference), seasoning (young loans default later), underwriting policy changes.
5. Decide. If the ratio is similar across bands (a level shift) and AUC holds, recalibrate: fit a new intercept (and maybe a slope) on recent matured outcomes; in a simulation with an AUC of about 0.80 recalibration leaves AUC unchanged. If some segments are far off, or a key feature drifted, rebuild or add segment-specific calibration.
6. Governance: this is a model-risk event. Write up the issue, the evidence and the proposed fix; the model validation function reviews, the owner approves, and the change is logged with before and after metrics. Ask the risk, finance and governance teams about provisioning impact, thresholds for when a recalibration needs formal approval, and documentation; I do not state the rules.
7. Interim: use a conservative overlay or tighter cut-off if the business agrees, and monitor monthly.
8. Monitoring afterwards: predicted versus observed by band monthly, population stability on key features, and a trigger (for example a ratio outside an agreed band for two quarters).

**Metrics:**
- Calibration ratio = observed default rate / mean predicted PD = 4.5% / 3.0% = 1.5.
- Expected loss = sum over loans of PD x EAD x LGD; observed-default loss = defaults x EAD x LGD at the assumed LGD (not realised losses).
- Calibration by band = observed / predicted per decile.
- Discrimination: AUC (0.80 before and after recalibration).
- Guardrails: approval rate, provisioning change, stability of ranking after recalibration.

**Risks:**
- Recalibrating on one bad year bakes the shock in; use a long-run anchor or overlay.
- A single intercept shift will not fix band-specific errors (in my simulation the ratio was 2.4 in the safest decile and 1.35 in the riskiest under a pure logit shift).
- LGD is assumed; the 4,500,000 is not a realised loss.
- Immature loans can understate defaults; confirm outcomes are matured.

**What the interviewer scores:**
- Strong: gets 3.0M, 4.5M and 1.5M, and states LGD is an assumption.
- Strong: separates ranking (AUC) from level (calibration) and checks by band.
- Strong: gives a decision rule between recalibrating and rebuilding, and a governance path.
- Weak: "AUC is fine so the model is fine"; "retrain from scratch immediately"; legal claims.

**Example:** Illustrative numbers from the run. A simulated model with AUC about 0.80 and mean PD 3.0% faced 890 defaults; after an intercept recalibration its mean PD was 4.45% and AUC stayed 0.804, with expected loss 4,450,000.
- Weak: "The model underpredicts, so we need a new model."
- Strong: "Expected loss is 3.0M predicted against 4.5M from observed defaults at an assumed 50% LGD. AUC is unchanged, so ranking works; the level is off by a factor of 1.5. I would check by decile and by vintage, recalibrate if the miss is a level shift, and take it through model validation with the finance and risk teams."

**Code:**
```python
import numpy as np
from math import sqrt, log

N, EAD, LGD = 20000, 10000, 0.5
pd_pred, defaults = 0.03, 900
pd_obs = defaults / N
el_pred = N * pd_pred * EAD * LGD
el_obs = defaults * EAD * LGD
print("observed default rate", pd_obs, "| predicted defaults", N * pd_pred, "| observed", defaults)
print("expected loss predicted", el_pred, "observed", el_obs, "shortfall", el_obs - el_pred, "=", round((el_obs - el_pred) / el_obs, 3), "of observed;", round(el_obs / el_pred, 2), "x predicted")
assert pd_obs == 0.045 and N * pd_pred == 600
assert el_pred == 3_000_000 and el_obs == 4_500_000 and el_obs - el_pred == 1_500_000

# noise check, independent defaults: sd of count under the model's own 3%
sd = sqrt(N * pd_pred * (1 - pd_pred))
z = (defaults - N * pd_pred) / sd
print("binomial sd of default count", round(sd, 1), "| z =", round(z, 1))
assert round(sd, 1) == 24.1 and round(z, 1) == 12.4
# defaults cluster (shared shocks): allow a design effect, e.g. intra-class correlation rho
for rho in (0.001, 0.005, 0.01):
    print("  pairwise default correlation rho", rho, "-> design-effect z", round(z / sqrt(1 + (N - 1) * rho), 1))
# intercept shift needed (logit scale) for the average to move from 3.0% to 4.5%
logit = lambda p: log(p / (1 - p))
shift = logit(0.045) - logit(0.03)
print("logit intercept shift", round(shift, 3))
assert round(shift, 3) == 0.421

# simulate: a model with AUC ~0.80 whose level is wrong; recalibrate the intercept; AUC does not move
rng = np.random.default_rng(34)
def auc(s, y):
    r = s.argsort().argsort() + 1
    n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
# latent score so that the model's mean PD is ~3% and AUC ~0.8
z0 = rng.normal(size=N)
def level(b):                      # find intercept so mean prob = b
    lo, hi = -12, 2
    for _ in range(60):
        mid = (lo + hi) / 2
        if (1 / (1 + np.exp(-(mid + 1.3 * z0)))).mean() > b: hi = mid
        else: lo = mid
    return mid
a_true = level(0.045); a_model = level(0.03)
p_true = 1 / (1 + np.exp(-(a_true + 1.3 * z0)))
y = (rng.random(N) < p_true).astype(int)
p_model = 1 / (1 + np.exp(-(a_model + 1.3 * z0)))
print("sim: defaults", y.sum(), "| model mean PD", round(p_model.mean(), 4), "| AUC", round(auc(p_model, y), 3))
# recalibrate on the matured outcomes: fit new intercept only (slope fixed)
a_new = level(y.mean())
p_new = 1 / (1 + np.exp(-(a_new + 1.3 * z0)))
print("after intercept recalibration: mean PD", round(p_new.mean(), 4), "| AUC", round(auc(p_new, y), 3), "| expected loss", round(p_new.sum() * EAD * LGD))
assert abs(auc(p_model, y) - auc(p_new, y)) < 1e-12
assert abs(p_new.mean() - y.mean()) < 1e-4
# calibration by band: is it a uniform shift or only some bands? (decile table)
dec = np.array_split(np.argsort(p_model), 10)
for i in (0, 4, 9):
    d = dec[i]; print(f"  decile {i+1}: predicted {p_model[d].mean():.4f} observed {y[d].mean():.4f} ratio {y[d].mean()/p_model[d].mean():.2f}")
# LGD sensitivity: the 50% is an assumption
for lgd in (0.4, 0.5, 0.6):
    print("  LGD", lgd, "-> observed-default loss", defaults * EAD * lgd, "| predicted", N * pd_pred * EAD * lgd)
assert y.sum() == 890 and round(auc(p_model, y), 3) == 0.804 and round(p_new.mean(), 4) == 0.0445
assert 2 < y[dec[0]].mean() / p_model[dec[0]].mean() < 3 and 1.2 < y[dec[9]].mean() / p_model[dec[9]].mean() < 1.5
```

**Output (my run):**
```
observed default rate 0.045 | predicted defaults 600.0 | observed 900
expected loss predicted 3000000.0 observed 4500000.0 shortfall 1500000.0 = 0.333 of observed; 1.5 x predicted
binomial sd of default count 24.1 | z = 12.4
  pairwise default correlation rho 0.001 -> design-effect z 2.7
  pairwise default correlation rho 0.005 -> design-effect z 1.2
  pairwise default correlation rho 0.01 -> design-effect z 0.9
logit intercept shift 0.421
sim: defaults 890 | model mean PD 0.03 | AUC 0.804
after intercept recalibration: mean PD 0.0445 | AUC 0.804 | expected loss 4450000
  decile 1: predicted 0.0017 observed 0.0040 ratio 2.37
  decile 5: predicted 0.0123 observed 0.0210 ratio 1.70
  decile 10: predicted 0.1374 observed 0.1855 ratio 1.35
  LGD 0.4 -> observed-default loss 3600000.0 | predicted 2400000.0
  LGD 0.5 -> observed-default loss 4500000.0 | predicted 3000000.0
  LGD 0.6 -> observed-default loss 5400000.0 | predicted 3600000.0
```

**Follow-ups:**
- *How would you tell macro from model failure?* Compare with peer portfolios or lenders, check the same-vintage behaviour across segments, and see whether the miss is uniform across bands.
- *Is a 1.5x miss bad if provisioning already covers it?* Ask finance and risk; it still needs documenting and monitoring.
- *Would you also recalibrate LGD?* Check realised recoveries separately; do not hide a PD miss inside an LGD change.
- See also Book 6 Part 2, Q14 (a classifier with stable AUC 0.82 whose probabilities have drifted) for the generic recalibration-versus-retrain argument.

**Common mistakes:**
- Calling the observed-default loss "the realised loss" when LGD is assumed.
- Declaring significance without a design effect for correlated defaults.
- Recalibrating without checking bands or segments.
- Skipping the governance step.

### Q35 ⭐⭐ 🔴 E-commerce: A price test cut the price by 10% on 1,000 items from 500 to 450 and daily units on those items rose 20% relative, from 100,000 to 120,000, while 4,000 close substitute items fell 5% relative, from 240,000 to 228,000 units a day at an unchanged price of 500 (projections from a pilot). Compute the item-level and the whole-category change in revenue per day, and explain how you would design the test to capture cannibalisation.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to price tests with substitution and interference in marketplace material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Item-level revenue rises 4,000,000 a day (+8%), but the substitutes lose 6,000,000, so the whole category falls 2,000,000 a day (-1.2%); the price cut mostly moves demand from neighbours to the discounted items, so I would test at the category level.

**Clarifying questions:**
- Are these numbers from a randomised pilot or a before/after comparison? Without randomisation the 20% and 5% could include trends and seasonality.
- Is the objective revenue, units or margin? The answer flips with unit cost (see the margin view below).
- Which items count as substitutes, and how was that list built? A wrong list hides or invents cannibalisation.
- Is there a time effect (promotion novelty, pull-forward of purchases)? A short pilot overstates a lasting lift.
- Is any inventory or fee affected by the price cut? Costs outside revenue change the decision.

**Approach:**
1. Item level. Revenue before = 100,000 x 500 = 50,000,000; after = 120,000 x 450 = 54,000,000; change +4,000,000 (+8.0%). Decomposition: -5,000,000 from the price cut on old units (100,000 x -50), +9,000,000 from the extra 20,000 units at 450.
2. Substitutes: 240,000 x 500 = 120,000,000 before, 228,000 x 500 = 114,000,000 after, change -6,000,000 (-5.0%).
3. Whole category: before 170,000,000, after 168,000,000: -2,000,000 per day (-1.18%). Units rose by 8,000 (20,000 extra on the test items minus 12,000 lost on substitutes), so units grew while revenue fell.
4. Cannibalisation share: 12,000 of the 20,000 extra units, 60%, came from substitutes. Elasticities: own -2.0, cross +0.5 (a 10% cut moved the substitutes 5% the other way).
5. Break-even: the category is revenue-neutral only if substitutes lose 8,000 units or fewer (3.3% of their units, instead of 5%).
6. Margin view (invented unit cost of 300): margin falls from 68,000,000 to 63,600,000, a loss of 4,400,000 per day, worse than the revenue figure.
7. Design to capture cannibalisation: randomise at the level where substitutes live (category, brand-by-region, or cluster of similar items), not the item. Measure outcome at the cluster level. In my toy model item-level randomisation (half the items cut) shows a +23.5% treated-versus-control lift, while cutting every item gives +3.2%, because the control items lose 9.1% of their own baseline.
8. Other designs: geo or time-based switchback tests; holdout clusters; track category total and a long window for pull-forward.

**Metrics:**
- Item-level revenue change = (units after x price after) - (units before x price before) for test items.
- Category revenue (and margin) change = test items + substitutes (+ any other affected items).
- Cannibalisation rate = units lost on substitutes / extra units on test items (60%).
- Guardrails: margin per day, conversion, returns, stock-outs, long-window repeat purchase.

**Risks:**
- Item-level randomisation shares customers between arms, so the estimate is biased (interference).
- A pilot's relative moves may not hold at scale; competitors may respond.
- Revenue can rise while margin falls.
- Substitute lists are subjective; some losses may be in non-listed items.

**What the interviewer scores:**
- Strong: computes +4M, -6M, -2M correctly and states units versus revenue.
- Strong: gives the cannibalisation share and asks about margin.
- Strong: randomises at cluster or category level and measures category totals.
- Weak: reports only the +8% item lift; ignores interference in the test design.

**Example:** Illustrative numbers from the run. Item level +4,000,000, substitutes -6,000,000, category -2,000,000 per day; 60% of the extra units are taken from neighbours.
- Weak: "The test lifted units 20% and revenue 8%, so we roll out."
- Strong: "Test items gain 4 million a day, but substitutes lose 6 million, so the category loses 2 million. Of the extra 20,000 units, 12,000 came from neighbours. I would re-run at the category level with a holdout and look at margin, not just revenue."

**Code:**
```python
items_n, subs_n = 1000, 4000
p0, p1, ps = 500, 450, 500
u0, u1 = 100_000, 120_000
s0, s1 = 240_000, 228_000
assert p1 == p0 * 0.9 and u1 == u0 * 1.2 and s1 == s0 * 0.95
rev_i0, rev_i1 = u0 * p0, u1 * p1
rev_s0, rev_s1 = s0 * ps, s1 * ps
d_i, d_s = rev_i1 - rev_i0, rev_s1 - rev_s0
print("test items revenue/day", rev_i0, "->", rev_i1, "change", d_i, f"({d_i/rev_i0:+.1%})")
print("substitutes revenue/day", rev_s0, "->", rev_s1, "change", d_s, f"({d_s/rev_s0:+.1%})")
print("category change", d_i + d_s, f"({(d_i+d_s)/(rev_i0+rev_s0):+.2%} of {rev_i0+rev_s0})")
assert d_i == 4_000_000 and d_s == -6_000_000 and d_i + d_s == -2_000_000
assert rev_i0 + rev_s0 == 170_000_000 and rev_i1 + rev_s1 == 168_000_000
# decomposition of the item-level change
price_effect = u0 * (p1 - p0)            # old units at the new price
volume_effect = (u1 - u0) * p1           # extra units at the new price
print("price effect on old units", price_effect, "| revenue from extra units", volume_effect)
assert price_effect == -5_000_000 and volume_effect == 9_000_000 and price_effect + volume_effect == d_i
# units
extra, lost = u1 - u0, s0 - s1
print("extra units on test items", extra, "| units lost on substitutes", lost, "| share of extra units that is cannibalised", lost / extra, "| net category units", extra - lost)
assert extra == 20000 and lost == 12000 and lost / extra == 0.6 and extra - lost == 8000
elas = (u1 / u0 - 1) / (p1 / p0 - 1)
cross = (s1 / s0 - 1) / (p1 / p0 - 1)
print("own elasticity", round(elas, 2), "| cross elasticity", round(cross, 2))
assert round(elas, 2) == -2.0 and round(cross, 2) == 0.5
# break-even: what substitute loss makes the category revenue-neutral?
lost_even = d_i / ps
print("category revenue-neutral if substitutes lose", lost_even, "units/day (", round(lost_even / s0 * 100, 2), "% of their units )")
assert lost_even == 8000
# margin view: invented unit cost 300 (illustrative)
c = 300
m0 = u0 * (p0 - c) + s0 * (ps - c)
m1 = u1 * (p1 - c) + s1 * (ps - c)
print("margin/day at unit cost", c, ":", m0, "->", m1, "change", m1 - m0)
assert (m1 - m0) == -4_400_000

# why item-level randomisation overstates: toy logit-share category (invented), half the items get -10%
e, eta = 2.0, 0.3                     # item share elasticity, category elasticity to the price index
def category(frac_treated, n=2000, Q0=200_000):
    w_t, w_c = 0.9 ** (-e), 1.0
    nt = int(n * frac_treated); nc = n - nt
    W = nt * w_t + nc * w_c
    pidx = (nt * 0.9 + nc * 1.0) / n   # simple average price index
    Q = Q0 * pidx ** (-eta)
    ut = Q * w_t / W if nt else 0; uc = Q * w_c / W if nc else 0
    return nt, nc, ut, uc, Q
nt, nc, ut, uc, Q = category(0.5)
base_u = 200_000 / 2000
print("item-randomised: treated item units", round(ut, 1), "control item units", round(uc, 1), "baseline", base_u)
naive = ut / uc - 1
print("naive treated-vs-control unit lift", round(naive, 3))
nt2, nc2, ut2, uc2, Q2 = category(1.0)
true_all = Q2 / 200_000 - 1
print("true category unit lift if every item were cut by 10%", round(true_all, 3), "| control items vs their own baseline", round(uc / base_u - 1, 3))
assert round(naive, 3) == 0.235 and round(true_all, 3) == 0.032 and uc / base_u - 1 < 0
```

**Output (my run):**
```
test items revenue/day 50000000 -> 54000000 change 4000000 (+8.0%)
substitutes revenue/day 120000000 -> 114000000 change -6000000 (-5.0%)
category change -2000000 (-1.18% of 170000000)
price effect on old units -5000000 | revenue from extra units 9000000
extra units on test items 20000 | units lost on substitutes 12000 | share of extra units that is cannibalised 0.6 | net category units 8000
own elasticity -2.0 | cross elasticity 0.5
category revenue-neutral if substitutes lose 8000.0 units/day ( 3.33 % of their units )
margin/day at unit cost 300 : 68000000 -> 63600000 change -4400000
item-randomised: treated item units 112.2 control item units 90.9 baseline 100.0
naive treated-vs-control unit lift 0.235
true category unit lift if every item were cut by 10% 0.032 | control items vs their own baseline -0.091
```

**Follow-ups:**
- *What if the substitute drop is only 3%?* Substitutes lose 3,600,000 and the category is +400,000; the break-even is 3.3%, so the decision is close and needs a proper interval.
- *Is a switchback test enough?* It handles shared customers over time but needs washout between periods because of pull-forward.
- See also Book 6 Part 1, Q40 (a new tab grows while the parent tab loses orders) for the same cannibalisation logic in orders.

**Common mistakes:**
- Reading item lift as category lift.
- Randomising at item level when items substitute.
- Using revenue when the goal is margin.
- Treating the pilot as a forecast.

### Q36 ⭐⭐ 🔴 Healthcare: A deterioration alert model was trained on labels of ICU transfer within 24 hours. After launch, transfers fell from 1,000 to 800 per 20,000 admissions (5.0% to 4.0%, absolute) and the measured positive predictive value of alerts is 18% in live use against 30% in a retrospective replay at the same alert volume of about 1,000 alerts per 20,000 admissions. Explain how effective alerts can look like false positives, why monitoring against the original label can mislead, and how you would evaluate and retrain safely.
**Asked at:** Clinical-ML deployment material (a physician-oriented dataset-shift article, an arXiv paper on what clinicians want from explainable ML, a JMIR paper on alarm fatigue and a circEWS slide deck on calibration and prevalence); research and secondary sources rather than interview banks; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** If clinicians act on the alerts, the patients most likely to be transferred are the ones the alert helps, so the label "ICU transfer within 24 hours" is not generated by the same process that trained the model; an effective alert looks like a false positive, so I would not judge or retrain on that label alone.

**Clarifying questions:**
- Is the replay volume really about 1,000 alerts per 20,000 admissions, and is live volume the same? The hand-check depends on it.
- What do clinicians do after an alert (review, extra monitoring, early treatment, escalation)? That is the intervention that changes the outcome.
- Did anything else change at launch (staffing, a rapid-response team, case mix, season)? Transfers fell 1,000 to 800 and other causes can contribute.
- Is there a record of alert response (acknowledged, action taken)? It lets me separate treated from untreated alerts.
- Is a holdout or silent period possible, and who approves it (ethics, clinical safety)? It decides how well I can measure the effect.

**Approach:**
1. Get the numbers straight. Transfers fell from 1,000 to 800 per 20,000: 5.0% to 4.0%, a 1.0 point absolute fall, 20% relative.
2. Hand-check with the stated volume of about 1,000 alerts (illustrative numbers): replay PPV 30% = 300 true positives, live 18% = 180, so 120 fewer. If every missing true positive were a patient the alert helped, 120 of the 200 fewer transfers is explained by alerts and 80 by other changes.
3. Prevalence alone does not explain the drop. Keep sensitivity at 30% and the replay false-positive rate; at 4.0% prevalence PPV would be about 25.3%, not 18%.
4. Simulate the mechanism: in my run alerts cut transfer risk by 45% (invented) for alerted patients; the same model had replay PPV 12.0% and live PPV 7.2%, while the untreated deterioration rate among alerted patients was 12.8%. The alerts worked and the PPV fell.
5. Why monitoring against the original label misleads: PPV, recall and calibration measured on "transfer" fall when alerts work. A dashboard would say the model is degrading and prompt a retrain.
6. A naive retrain on live labels makes it worse: the model learns that patients who look like those who were alerted rarely transfer. In my run, at the same probability cut, the alert share fell from 5.12% to 2.44% and mean predicted risk fell from 5.02% to 4.72%.
7. Safer evaluation: (a) define outcomes that survive treatment (deterioration events, rapid response calls, death, ICU transfer or critical intervention as a composite); (b) record whether the alert was acted on and when; (c) compare alerted versus matched non-alerted patients, or use a staged rollout, or a randomised or silent comparison group if clinical safety and ethics approve; (d) use the pre-launch period and the silent mode as the training source.
8. Retrain only with treatment-aware labels (for example the composite, or labels from patients with no alert action) and keep the alert threshold fixed or reviewed by clinicians; check alert burden per nurse and alarm fatigue.

**Metrics:**
- PPV = alerts followed by the outcome / alerts (18% live, 30% replay).
- Composite deterioration rate per 1,000 admissions, split by alerted and not alerted.
- Alert volume per ward per day, time-to-action, acknowledgement rate.
- Recall against the composite outcome; calibration by risk band on untreated patients.
- Guardrails: alarm fatigue (override rate), missed deteriorations, length of stay.

**Risks:**
- The label depends on the response; retraining on it creates a feedback loop.
- Randomised withholding of an alert is an ethics question; ask clinical safety and the ethics process.
- Other changes at launch can explain part of the fall in transfers.
- A model that works can be switched off because the dashboard says PPV is low.

**What the interviewer scores:**
- Strong: names treatment-contaminated labels and shows that PPV falls when alerts work.
- Strong: separates prevalence from the intervention effect with numbers.
- Strong: proposes an outcome that survives treatment and a safe evaluation design with ethics review.
- Weak: "retrain on the new data"; "PPV fell so the model is worse"; ignoring the clinical process.

**Example:** Illustrative numbers from the run. With 1,000 alerts, PPV 30% to 18% means 120 fewer true positives; prevalence alone would give PPV about 25.3%.
- Weak: "PPV fell from 30% to 18%, so the model drifted; retrain on last month."
- Strong: "Transfers also fell 20% relative. If nurses acted on alerts, the alerted patients who improved now count as false positives. Prevalence alone would take PPV to about 25%, so the rest looks like treatment. I would track a composite outcome, compare alerted and matched unalerted patients, and retrain only with treatment-aware labels."

**Code:**
```python
import numpy as np

# prompt arithmetic
adm, t0, t1 = 20000, 1000, 800
print("transfer rate", t0 / adm, "->", t1 / adm, "| absolute", round((t0 - t1) / adm, 3), "| relative", (t0 - t1) / t0)
assert t0 / adm == 0.05 and t1 / adm == 0.04 and (t0 - t1) / t0 == 0.2

# Illustrative hand-check: assume 1,000 alerts per 20,000 admissions (the prompt gives PPV, not volume)
V = 1000
tp_replay, tp_live = 0.30 * V, 0.18 * V
print("true positives among alerts: replay", tp_replay, "live", tp_live, "| missing", tp_replay - tp_live)
assert tp_replay == 300 and tp_live == 180 and tp_replay - tp_live == 120
print("recall vs transfers: replay", tp_replay / t0, "live", tp_live / t1)
assert tp_replay / t0 == 0.3 and tp_live / t1 == 0.225
# if alerts prevented X transfers among alerted patients and nothing else changed: X = 120 of the 200 fewer transfers
print("transfers fewer in total", t0 - t1, "| of which alert-saved if PPV drop is all treatment", tp_replay - tp_live, "| the other", (t0 - t1) - (tp_replay - tp_live), "from other causes or non-alerted")
assert (t0 - t1) - (tp_replay - tp_live) == 80

# prevalence alone (same sensitivity 30% and same false-positive rate as replay)
sens = tp_replay / t0
fpr = (V - tp_replay) / (adm - t0)
tp_p = sens * t1; fp_p = fpr * (adm - t1)
print("prevalence-only PPV", round(tp_p / (tp_p + fp_p), 3), "| alert volume would be", round(tp_p + fp_p))
assert round(tp_p / (tp_p + fp_p), 3) == 0.253

# simulation: alerts change outcomes, so the label (ICU transfer) understates true deterioration
rng = np.random.default_rng(36)
def make(n):
    r = rng.beta(1.0, 19, n)                       # latent risk of deterioration w/o intervention
    X = np.c_[np.log(r / (1 - r)) + rng.normal(0, 1.0, n), rng.normal(size=n)]   # noisy vital-sign score + noise
    return r, X
def fit(X, y, it=30):
    A = np.c_[np.ones(len(X)), X]; w = np.zeros(3)
    for _ in range(it):
        mu = 1 / (1 + np.exp(-(A @ w))); W = mu * (1 - mu)
        w += np.linalg.solve(A.T @ (A * W[:, None]) + 1e-6 * np.eye(3), A.T @ (y - mu))
    return w
score = lambda w, X: np.c_[np.ones(len(X)), X] @ w
n = 200_000
r0, X0 = make(n); y0 = (rng.random(n) < r0).astype(float)          # pre-launch labels
w1 = fit(X0, y0)
rep = 0.05
thr = np.quantile(score(w1, X0), 1 - rep)
alert0 = score(w1, X0) >= thr
print("replay: alert share", round(alert0.mean(), 3), "| PPV", round(y0[alert0].mean(), 3), "| prevalence", round(y0.mean(), 4))
eff = 0.45                                         # invented: intervention cuts transfer risk 45% (relative) when alerted
r1, X1 = make(n); a1 = score(w1, X1) >= thr
p1 = r1 * np.where(a1, 1 - eff, 1.0)
y1 = (rng.random(n) < p1).astype(float)
print("live  : alert share", round(a1.mean(), 3), "| PPV", round(y1[a1].mean(), 3), "| prevalence", round(y1.mean(), 4))
tp_live_ = y1[a1].mean()
print("true deterioration rate among alerted (untreated risk)", round(r1[a1].mean(), 3))
assert y1[a1].mean() < y0[alert0].mean() and y1.mean() < y0.mean()
# naive retrain on live labels: the model learns "alerted-looking patients rarely transfer"
w2 = fit(X1, y1)
sig = lambda z: 1 / (1 + np.exp(-z))
p_cut = sig(thr)                                   # the probability cut the original model used
share_orig = (sig(score(w1, X1)) >= p_cut).mean()
share_naive = (sig(score(w2, X1)) >= p_cut).mean()
print("alert share at the same probability cut: original", round(share_orig, 4), "| naive retrain on live labels", round(share_naive, 4))
print("mean predicted risk: original", round(sig(score(w1, X1)).mean(), 4), "| naive retrain", round(sig(score(w2, X1)).mean(), 4), "| mean untreated risk", round(r1.mean(), 4), "| observed live rate", round(y1.mean(), 4))
print("coefficients original", np.round(w1, 3), "naive retrain", np.round(w2, 3))
assert share_naive < share_orig
assert round(y0[alert0].mean(), 3) == 0.12 and round(y1[a1].mean(), 3) == 0.072
assert round(share_orig, 4) == 0.0512 and round(share_naive, 4) == 0.0244
```

**Output (my run):**
```
transfer rate 0.05 -> 0.04 | absolute 0.01 | relative 0.2
true positives among alerts: replay 300.0 live 180.0 | missing 120.0
recall vs transfers: replay 0.3 live 0.225
transfers fewer in total 200 | of which alert-saved if PPV drop is all treatment 120.0 | the other 80.0 from other causes or non-alerted
prevalence-only PPV 0.253 | alert volume would be 947
replay: alert share 0.05 | PPV 0.12 | prevalence 0.0501
live  : alert share 0.051 | PPV 0.072 | prevalence 0.0472
true deterioration rate among alerted (untreated risk) 0.128
alert share at the same probability cut: original 0.0512 | naive retrain on live labels 0.0244
mean predicted risk: original 0.0502 | naive retrain 0.0472 | mean untreated risk 0.0501 | observed live rate 0.0472
coefficients original [-1.579  0.453  0.014] naive retrain [-1.819  0.387 -0.009]
```

**Follow-ups:**
- *How would you measure the benefit of the alerts?* Compare the composite outcome in matched or staged groups; ask clinical safety about a holdout.
- *Could the fall in transfers be a worse miss instead?* Yes: patients may deteriorate and die on the ward without transfer. Track deaths and the composite outcome, not only transfers.
- See also Book 6 Part 3, Q23 (a rare-disease screen where PPV depends on prevalence) for the base-rate arithmetic.

**Common mistakes:**
- Reading PPV on a treated outcome as model quality.
- Retraining on the contaminated label.
- Ignoring that a positive intervention changes the labels.
- Assuming the whole PPV drop is prevalence (it is not, by the arithmetic).

### Q37 ⭐⭐ 🔴 Ads: Conversions arrive late, and the share of eventual conversions already observed is 50% for clicks 0 days old, 70% at 1 day, 80% at 2, 90% at 3, 95% at 4, 98% at 5 and 100% at 6 days. A conversion model is retrained daily on the last 7 days of clicks (ages 0 to 6 days, equal click volume per age), labelling unconverted clicks as negative. Compute the average share of conversions observed across those 7 ages and the relative underestimate of the conversion rate, and describe a delayed-feedback fix.
**Asked at:** Ads ML and calibration material (Dataford questions on CTR calibration and click-through rate at an ad-tech firm, AlgoMaster and Educative ad click prediction system-design pages with calibration-error checks by probability bin); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Averaged over ages 0 to 6 the labels have seen 83.3% of eventual conversions, so the conversion rate learned is about 16.7% too low; I would fix it with a delayed-feedback model or a maturity correction, not by pretending unconverted young clicks are negatives.

**Clarifying questions:**
- Is the delay curve stable by campaign, product and day of week? A single curve is only a first approximation.
- Is the model used for bidding or ranking? Bidding needs calibrated probabilities; ranking needs order only.
- Do we get conversion events with the click ID, and how late do corrections or refunds arrive? It sets what "100% at 6 days" means.
- Are clicks equal in volume per age? The 83.3% needs equal volume; with unequal volume use a weighted average.
- How often can we retrain, and how fresh must the model be? Waiting for maturity costs freshness.

**Approach:**
1. The arithmetic: (50 + 70 + 80 + 90 + 95 + 98 + 100) / 7 = 583 / 7 = 83.29%. The relative underestimate of the conversion rate is 1 - 0.8329 = 16.7% (a true 5.0% looks like 4.16%).
2. The bias is not uniform: age-0 clicks show only half their eventual conversions (a 5% true rate looks like 2.5%), while age-6 clicks are complete. A model that sees age as a feature may learn "new clicks convert less".
3. In my simulation (200,000 clicks per age, true rate 5%), the naive training rate was 4.18% (about 0.84 of the true rate); the by-age naive rates ran from 2.53% at age 0 to 4.93% at age 6.
4. Fix A, wait: train only on clicks aged 6 days or more. Unbiased (4.93% in the run) but uses one-seventh of the clicks here and the model is a week stale.
5. Fix B, correct by maturity: divide each age bucket's conversions by the share observed at that age (the curve), estimated from older cohorts. In the run the corrected rate was 5.03%.
6. Fix C, delayed-feedback model: model P(conversion eventually) and the delay distribution separately; the observed label at age a is conversion times "delay <= a". With the curve known, the maximum-likelihood rate in my run was 4.99%. Chapelle's delayed-feedback model is the usual reference (editor knowledge; not run here).
7. Practical production rules: keep the age of the click as a training feature only if it is removed at serving time; use fresh data with corrected weights; monitor calibration on matured cohorts only (see Book 6 Part 2, Q28, on label maturation and calibration on the last seven days).
8. Report both numbers: the raw rate on young cohorts will always look low and should not trigger an alert.

**Metrics:**
- Observed share at age a = conversions seen by age a / eventual conversions (50%, 70%, ... 100%).
- Average maturity = mean of those shares over the training window = 83.29%.
- Relative underestimate = 1 - average maturity = 16.7%.
- Calibration on matured cohorts = predicted conversions / observed conversions after 6 days.
- Guardrails: freshness lag, bid error, spend efficiency.

**Risks:**
- The delay curve is itself estimated and can drift (a promotion, a payment outage).
- Late conversions that are refunded or corrected change eventual counts.
- Dividing by a small share (age 0, 50%) amplifies noise.
- Importance weights can produce huge variance; clip them.

**What the interviewer scores:**
- Strong: 83.3% and 16.7%, and the fact that age 0 is the worst.
- Strong: names the unconverted-as-negative bias, and offers wait, correct and delayed-feedback options with trade-offs.
- Strong: evaluates calibration on matured data only.
- Weak: "use more data"; "retrain more often"; no mention of delay.

**Example:** Illustrative numbers from the run. True rate 5.0%; naive training rate 4.18% (ratio 0.84); corrected 5.03%; maximum-likelihood 4.99%.
- Weak: "The conversion rate looks lower this week, so the model should predict lower."
- Strong: "Our 7-day window has only about 83% of eventual conversions, so training labels understate the rate by about 17%, and 50% of conversions are missing for the newest clicks. I would divide by the observed share per age or fit a delayed-feedback model, and I would check calibration on clicks older than 6 days."

**Code:**
```python
import numpy as np

F = np.array([0.50, 0.70, 0.80, 0.90, 0.95, 0.98, 1.00])
ages = np.arange(7)
avg = F.mean()
print("sum of shares", round(F.sum(), 2), "| average observed share", round(avg, 4), "| relative underestimate", round(1 - avg, 4))
assert round(F.sum(), 2) == 5.83 and round(avg, 4) == 0.8329 and round(1 - avg, 4) == 0.1671

# simulate: true conversion rate 5%, delay distribution implied by F; labels as seen at training time
rng = np.random.default_rng(37)
clicks_per_age, cvr = 200_000, 0.05
inc = np.diff(np.r_[0, F])                           # share of eventual conversions arriving on each delay day
obs_conv = np.zeros(7); true_conv = np.zeros(7)
for a in ages:
    conv = rng.random(clicks_per_age) < cvr
    # delay day d with probability inc[d] (d = 0..6); observed if d <= age
    d = rng.choice(7, size=clicks_per_age, p=inc)
    true_conv[a] = conv.sum()
    obs_conv[a] = (conv & (d <= a)).sum()
naive = obs_conv.sum() / (7 * clicks_per_age)
print("true rate", round(true_conv.sum() / (7 * clicks_per_age), 4), "| naive training rate", round(naive, 4), "| ratio", round(naive / cvr, 3))
assert abs(naive / cvr - avg) < 0.01
# fix A: train only on mature clicks (age 6): unbiased but only 1/7 of the volume and a week stale
print("mature-only (age 6) rate", round(obs_conv[6] / clicks_per_age, 4), "| rows used", clicks_per_age, "of", 7 * clicks_per_age)
# fix B: inverse-maturity correction per age bucket (estimating F from older cohorts, known here)
corr = (obs_conv / F).sum() / (7 * clicks_per_age)
print("rate after dividing each age bucket by its observed share", round(corr, 4))
assert abs(corr - cvr) < 0.003
# per-age naive rates: shows where the bias sits
print("naive rate by age", np.round(obs_conv / clicks_per_age, 4))
# fix C: label-time correction on click-level probabilities: p_true ~= p_seen / F(age)  (calibration intuition)
print("age-0 clicks look like", round(0.5 * cvr, 4), "instead of", cvr, "-> a model that ignores age learns", round(avg * cvr, 4), "on average")
assert round(avg * cvr, 4) == 0.0416
# a delayed-feedback style model: P(conv seen at age a) = p * F(a); fit p by maximum likelihood on (age, seen)
seen = []; ag = []
for a in ages:
    conv = rng.random(clicks_per_age) < cvr
    d = rng.choice(7, size=clicks_per_age, p=inc)
    seen.append(conv & (d <= a)); ag.append(np.full(clicks_per_age, a))
seen = np.concatenate(seen); ag = np.concatenate(ag)
grid = np.linspace(0.02, 0.08, 601)
ll = [(seen * np.log(p * F[ag]) + (~seen) * np.log(1 - p * F[ag])).sum() for p in grid]
p_hat = grid[int(np.argmax(ll))]
print("maximum-likelihood p with known F(age):", round(p_hat, 4))
assert abs(p_hat - cvr) < 0.002
```

**Output (my run):**
```
sum of shares 5.83 | average observed share 0.8329 | relative underestimate 0.1671
true rate 0.0502 | naive training rate 0.0418 | ratio 0.837
mature-only (age 6) rate 0.0493 | rows used 200000 of 1400000
rate after dividing each age bucket by its observed share 0.0503
naive rate by age [0.0253 0.0356 0.0396 0.0461 0.0476 0.0494 0.0493]
age-0 clicks look like 0.025 instead of 0.05 -> a model that ignores age learns 0.0416 on average
maximum-likelihood p with known F(age): 0.0499
```

**Follow-ups:**
- *What if the window is 14 days?* Average maturity rises (more complete days), but the freshness cost rises too.
- *Does the bias affect ranking?* Only if the bias differs by campaign or age mix, which it often does.
- *Why not just wait 6 days?* Fine when freshness is not important; ads usually need fresher models.

**Common mistakes:**
- Treating all unconverted clicks as true negatives.
- Averaging maturity with unequal click volume per age.
- Alerting on young-cohort calibration.
- Using the age as a feature at serving time.

### Q38 ⭐⭐ 🔴 Ads: After an exchange moves from second-price to first-price auctions, an impression is worth 10 to you. From logged auctions your estimated win probability is 20% at a bid of 4, 45% at 6, 60% at 7, 75% at 8, 88% at 9 and 95% at 10 (estimates). Under first price you pay your bid when you win, so compute the expected surplus (value minus bid, times win probability) at each bid, name the best bid and explain how you would break the tie, estimate the win curve and spot when it breaks.
**Asked at:** Ad-serving system-design material (techinterview.org ad serving and real-time bidding pages, a Dataford question on budget pacing and frequency capping, machinelearningatscale.com on frequency capping; feedback-controller pacing, per-user counters and credits for invalid clicks appear in the snippets); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Expected surplus at bids 4, 6, 7, 8, 9, 10 is 1.20, 1.80, 1.80, 1.50, 0.88 and 0.00, so bids 6 and 7 tie at 1.80 per auction; I would break the tie by what the campaign is short of (budget favours 6, volume favours 7), and I would keep re-estimating the win curve because it moves.

**Clarifying questions:**
- Is the budget the binding constraint, or is there a delivery commitment (a minimum number of impressions)? It decides the tie.
- Does the exchange tell us the winning price or minimum bid to win? It determines whether the win curve is censored.
- How many logged auctions sit behind each of the six estimates? With few auctions each point carries a wide range.
- Is the value of 10 per impression certain and the same on every impression? Value uncertainty changes how much to shade.
- How fast do competitors adapt after the change to first price? It sets how often the curve must be refit.

**Approach:**
1. Compute surplus = (10 - bid) x win probability: bid 4: 6 x 0.20 = 1.20; 6: 4 x 0.45 = 1.80; 7: 3 x 0.60 = 1.80; 8: 2 x 0.75 = 1.50; 9: 1 x 0.88 = 0.88; 10: 0 x 0.95 = 0.
2. Name the best bid: 6 and 7 tie at 1.80 per auction, which is 1,800 per 1,000 auctions either way.
3. Break the tie with the next constraint. Spend per auction is 6 x 0.45 = 2.70 at a bid of 6 and 7 x 0.60 = 4.20 at 7. Going from 6 to 7 buys 0.15 more win probability for 1.50 more spend, a marginal 10 per extra win (7 x 0.60 - 6 x 0.45 = 1.5, divided by 0.15), exactly the value, so it adds no surplus. If budget is binding, bid 6 (surplus per unit of spend is 0.667 versus 0.429) and use the saved spend elsewhere. If there is a volume commitment or a learning phase, bid 7 gets 600 wins per 1,000 auctions instead of 450 at no loss of surplus.
4. Do not trust the grid to the cent. The ranges at 400 auctions per point are about +/- 0.05 in win probability, which is +/- 0.20 in surplus at a bid of 6 and +/- 0.14 at 7. The tie is inside the noise. A linear guess at 6.5 gives 1.84 but that is an untested interpolation.
5. Estimate the win curve from logs: for every auction record bid, win or loss, and (if available) the winning price; fit a monotone curve (isotonic or a logistic on bid or log bid), or a censored model if only wins reveal prices. Add a small randomised bid perturbation so the curve is identified across the range you may use.
6. Spot when it breaks: compare predicted win rate with live win rate by bid bucket every day. In the run a competitor shift of one unit right makes the old 7 win like the old 6 (60% predicted, 45% live): z = -6.1 on 400 auctions. After such a shift the best bid on the shifted curve is 7 with surplus 1.35.
7. Rules for retraining: refit when the gap exceeds an agreed number of standard errors for several buckets, and always after an exchange rule change.
8. Guardrails: never bid above value (10), keep the budget pacing in view, and log the bids so the next curve can be estimated.

**Metrics:**
- Expected surplus per auction = (value - bid) x P(win | bid).
- Win rate by bid bucket, predicted versus live; spend per win; effective cost per impression won.
- Surplus per 1,000 auctions and per unit of spend.
- Guardrails: delivery against commitment, budget exhaustion time, curve gap (live minus predicted).

**Risks:**
- The win curve is estimated, not known; the best bid is a guess with an error bar.
- Censoring: if you only learn the clearing price on wins, extrapolation below your lowest logged bid is unsupported.
- Competitors change their bidding in response to yours.
- Paying your bid means any overestimate of the win curve costs money directly.
- Value per impression varies; one value for all impressions is a simplification.

**What the interviewer scores:**
- Strong: gets the six surplus numbers and sees the tie at 6 and 7.
- Strong: breaks the tie with budget versus volume and shows the marginal cost of 10 per extra win.
- Strong: explains how to estimate a censored win curve and how to detect a break.
- Weak: "bid your value" (a second-price habit); a single best bid with no uncertainty.

**Example:** Illustrative numbers from the run. Surplus 1.20, 1.80, 1.80, 1.50, 0.88, 0.00; per 1,000 auctions a bid of 6 wins 450, spends 2,700 and earns surplus 1,800; a bid of 7 wins 600, spends 4,200 and earns 1,800.
- Weak: "Bid 10, it is worth ten."
- Strong: "In first price I pay my bid, so I shade. Surplus peaks at 1.80 for both 6 and 7. Going to 7 buys 150 extra wins per 1,000 for 1,500 extra spend, 10 each, so no surplus gain. With a budget limit I bid 6; with a delivery target I bid 7. I will check the win curve daily and refit when it moves."

**Code:**
```python
from fractions import Fraction as Fr
import numpy as np

V = 10
win = {4: Fr(20, 100), 6: Fr(45, 100), 7: Fr(60, 100), 8: Fr(75, 100), 9: Fr(88, 100), 10: Fr(95, 100)}
surplus = {b: (V - b) * w for b, w in win.items()}
spend = {b: b * w for b, w in win.items()}
for b in win:
    print(f"bid {b:>2}: win {float(win[b]):.2f} | surplus {float(surplus[b]):.2f} | expected spend per auction {float(spend[b]):.2f} | surplus per unit spend {float(surplus[b]/spend[b]):.3f}")
best = max(surplus.values())
tied = [b for b, s in surplus.items() if s == best]
print("best surplus", float(best), "at bids", tied)
assert best == Fr(18, 10) and tied == [6, 7]
assert surplus[4] == Fr(6, 5) and surplus[8] == Fr(3, 2) and surplus[9] == Fr(22, 25) and surplus[10] == 0
# tie: the step from 6 to 7 buys 0.15 more win probability for 1.5 more spend per auction and adds zero surplus
dw = win[7] - win[6]; ds = spend[7] - spend[6]
print("6 -> 7: extra win prob", float(dw), "| extra spend per auction", float(ds), "| extra surplus", float(surplus[7] - surplus[6]))
assert dw == Fr(3, 20) and ds == Fr(3, 2)
# marginal cost per extra win: (7*0.6 - 6*0.45)/(0.6-0.45) = 10 -> equals the value, so zero surplus
print("marginal cost per extra win going 6 -> 7:", float(ds / dw))
assert ds / dw == 10
# volume view: 1,000 auctions
for b in (6, 7):
    print(f"1,000 auctions at bid {b}: wins {float(win[b]*1000):.0f}, spend {float(spend[b]*1000):.0f}, surplus {float(surplus[b]*1000):.0f}")
# interpolation is a guess, not data: linear win curve between 6 and 7 gives bid 6.5
w65 = (win[6] + win[7]) / 2
print("linear-interpolated bid 6.5:", float(w65), "surplus", float((V - Fr(13, 2)) * w65), "(untested; depends on the curve shape between the points)")
assert (V - Fr(13, 2)) * w65 == Fr(14700, 8000)
# estimating the win curve with noise: how uncertain is each estimate with n logged auctions near the bid?
rng = np.random.default_rng(38)
n = 400
for b in (6, 7):
    p = float(win[b]); se = (p * (1 - p) / n) ** 0.5
    print(f"bid {b}: with {n} auctions per point, win prob {p:.2f} +- {1.96*se:.3f}; surplus +- {1.96*se*(V-b):.3f}")
# drift alarm: a competitor shifts the curve right by 1 unit, so the old bid 7 now wins like the old bid 6
pred = float(win[7]); actual = float(win[6])
z = (actual - pred) / (pred * (1 - pred) / n) ** 0.5
print("bid 7 predicted win", pred, "live win", actual, "| z with", n, "live auctions:", round(z, 1))
assert round(z, 1) == -6.1
# what the shift does to the best bid: shifted curve, same value 10
sh = {b + 1: w for b, w in win.items()}              # bids 5, 7, 8, 9, 10, 11 carry the old win rates
sh_s = {b: (V - b) * w for b, w in sh.items() if b <= V}
print("shifted-curve surplus by bid:", {b: float(s_) for b, s_ in sh_s.items()})
print("best shifted bids:", [b for b, s_ in sh_s.items() if s_ == max(sh_s.values())], "with surplus", float(max(sh_s.values())))
assert max(sh_s.values()) == Fr(27, 20) and [b for b, s_ in sh_s.items() if s_ == Fr(27, 20)] == [7]
```

**Output (my run):**
```
bid  4: win 0.20 | surplus 1.20 | expected spend per auction 0.80 | surplus per unit spend 1.500
bid  6: win 0.45 | surplus 1.80 | expected spend per auction 2.70 | surplus per unit spend 0.667
bid  7: win 0.60 | surplus 1.80 | expected spend per auction 4.20 | surplus per unit spend 0.429
bid  8: win 0.75 | surplus 1.50 | expected spend per auction 6.00 | surplus per unit spend 0.250
bid  9: win 0.88 | surplus 0.88 | expected spend per auction 7.92 | surplus per unit spend 0.111
bid 10: win 0.95 | surplus 0.00 | expected spend per auction 9.50 | surplus per unit spend 0.000
best surplus 1.8 at bids [6, 7]
6 -> 7: extra win prob 0.15 | extra spend per auction 1.5 | extra surplus 0.0
marginal cost per extra win going 6 -> 7: 10.0
1,000 auctions at bid 6: wins 450, spend 2700, surplus 1800
1,000 auctions at bid 7: wins 600, spend 4200, surplus 1800
linear-interpolated bid 6.5: 0.525 surplus 1.8375 (untested; depends on the curve shape between the points)
bid 6: with 400 auctions per point, win prob 0.45 +- 0.049; surplus +- 0.195
bid 7: with 400 auctions per point, win prob 0.60 +- 0.048; surplus +- 0.144
bid 7 predicted win 0.6 live win 0.45 | z with 400 live auctions: -6.1
shifted-curve surplus by bid: {5: 1.0, 7: 1.35, 8: 1.2, 9: 0.75, 10: 0.0}
best shifted bids: [7] with surplus 1.35
```

**Follow-ups:**
- *What if the value is uncertain?* Shade on the expected value, and consider a conservative multiplier until the value model is calibrated.
- *Would you change the bid per impression?* Yes, bid is a function of predicted value and the win curve per segment.
- *Is there a bid between 6 and 7 that beats both?* Possibly, but it is not in the data; test it through randomised bid perturbation.

**Common mistakes:**
- Bidding value in first price.
- Treating a tie as a result and ignoring budget or volume.
- Extrapolating the win curve outside logged bids.
- Not monitoring the curve after the format change.

### Q39 ⭐⭐ 🔴 Ads: Total sales are 100,000,000 over a test period spread evenly across 50 regions, and last-click attribution credits online video with 1,000,000 of them (1% of sales). A geo test paused video in 10 randomly chosen regions and sales there were 4% lower than the kept regions' with-video level of 2,000,000 per region. Project the whole-country sales attributable to video if the effect is uniform, compare it with the last-click credit, and explain the assumptions and what a 10-region test can and cannot tell you.
**Asked at:** Ads measurement material (an eMarketer 2026 FAQ separating incrementality, multi-touch attribution and marketing mix modelling, Google ads-measurement data scientist postings asking for causal inference and attribution work, a Dataford incremental-lift question, a Remerge incrementality write-up); job postings and prep material rather than a confirmed interview round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** If the 4% drop is uniform, video drives about 4,000,000 of the 100,000,000 sales (4%), four times the 1,000,000 that last-click credits; this is a projection from 10 regions, so I would report a range and the assumptions, not a point.

**Clarifying questions:**
- Is the 100,000,000 the with-video level in all 50 regions? The prompt fixes the 4% against the kept regions' 2,000,000 each; as a share of the no-video level the same gap is 4.17%.
- How were the 10 regions chosen, and were pre-period sales compared? Random choice helps, but 10 of 50 can still be unbalanced.
- How long was the pause, and how long do video effects last? A short test misses lagged effects.
- Do regions leak (people travel, national media, shared online audiences)? Leakage shrinks the measured gap.
- What did video cost in the period? Incremental sales alone do not say whether it paid.

**Approach:**
1. The arithmetic. Each region sells 100,000,000 / 50 = 2,000,000. A 4% drop is 80,000 per paused region, 800,000 for the 10 regions, and scaled to 50 regions 4,000,000. The observed total in the test was 99,200,000.
2. Compare with last click: 4,000,000 / 1,000,000 = 4.0 times; video is 4% of sales on this projection versus 1% credited.
3. Put a range on it with an invented noise level (relative sales noise per region after matching): with 2% noise the 95% interval for the effect is 2.6% to 5.4% (2.6M to 5.4M), at 3% it is 1.9% to 6.1%, and at 6% it is -0.2% to 8.2%, which includes zero. So the point estimate is far less informative than it looks when regions are noisy.
4. Improve the estimate: compare each region with its own pre-period (difference-in-differences) or use matched regions or synthetic controls. In my simulation of 4,000 random assignments with a true 4%, comparing levels gave a standard deviation of 16.8 points (regions differ in size), while comparing with each region's pre-period gave 1.1 points and only 0.45% of assignments came out below 1%.
5. Assumptions to state: uniform effect across regions; no spillover; stable effect over time; the 40 control regions kept normal spend; no other channel changed; the effect measured at the current spend level.
6. What a 10-region test can tell you: the average incremental effect of switching video off at the current spend, with a range. What it cannot: the shape of diminishing returns (it is an on/off test), effects by region type, long-run brand effects, interaction with other channels, or the return per unit of spend.
7. Use it: calibrate the attribution model or the marketing-mix model with the test result (a lift test as a prior); rerun with more regions, more spend levels (a dose test) or a longer window.
8. Report: incremental sales, range, cost, and incremental return, and say that last click and lift measure different things (see Book 6 Part 5, Q11 on reported versus incremental return on ad spend).

**Metrics:**
- Lift = 1 - (sales in paused regions / counterfactual sales) = 4% (paused regions sell 96% of the kept level).
- Incremental sales = lift x total sales with video = 0.04 x 100,000,000 = 4,000,000.
- Ratio to last click = incremental / credited = 4.0.
- Incremental return = incremental sales (or margin) / video spend (spend not given in the prompt).
- Guardrails: pre-period balance between arms, spillover check using neighbouring regions, test duration.

**Risks:**
- Noise: 10 regions is a small test; a 3% regional noise gives a 4% effect with a 1.9% to 6.1% range, and 6% noise makes it inconclusive.
- Random assignment can still leave unbalanced regions; use pre-period matching.
- Spillover and national media bias the gap towards zero.
- The effect at one spend level does not extend to doubling or halving spend.
- Last click and lift may both be right about different things (assist versus incremental).

**What the interviewer scores:**
- Strong: 4,000,000 versus 1,000,000, with the base stated and a range.
- Strong: pre-period adjustment and the fact that 10 regions cannot give a response curve.
- Strong: lists assumptions (uniform, no spillover, short horizon).
- Weak: "video is worth 4x last click" as fact; no uncertainty; ignores cost.

**Example:** Illustrative numbers from the run. 800,000 lost in 10 regions scales to 4,000,000; at region-level noise of 3% the 95% range is 1.9M to 6.1M.
- Weak: "Last click says 1 million, the test says 4 million, so last click is wrong."
- Strong: "If the 4% is uniform, video is about 4 million of sales, four times last click. With 10 regions the range could be roughly 2 to 6 million, so I would compare against the regions' own history, check for spillover, and weigh it against video spend. It tells me about on versus off at this spend, not the return of one more unit."

**Code:**
```python
import numpy as np
from math import sqrt

total, regions, lastclick = 100_000_000, 50, 1_000_000
per_region = total / regions
drop = 0.04
print("sales per region", per_region, "| last-click share", lastclick / total)
assert per_region == 2_000_000 and lastclick / total == 0.01
# reading A: with-video sales are the base (kept regions); paused regions sell 96% of that
inc_A = total * drop
print("A: incremental sales if 4% of with-video sales:", inc_A, "| vs last-click", inc_A / lastclick, "x")
assert inc_A == 4_000_000 and inc_A / lastclick == 4.0
# base check: the 100,000,000 is the with-video level in every region; paused regions then sell 96% of 2,000,000
observed = 40 * per_region + 10 * per_region * 0.96
print("observed total in the test period", observed, "| counterfactual with video everywhere", total, "| incremental", total - observed, "(this is the 10 paused regions only)")
print("incremental as a share of the no-video level:", round(total / (total * 0.96) - 1, 4))
assert observed == 99_200_000 and round(total / (total * 0.96) - 1, 4) == 0.0417
# the 4% measured on 10 regions: projection to 50 assumes uniform effect
print("10 paused regions lost", 10 * per_region * drop, "in the test period; scaled x5 =", 5 * 10 * per_region * drop)
assert 10 * per_region * drop == 800_000 and 5 * 10 * per_region * drop == 4_000_000
# uncertainty (invented): region-level relative noise sd after matching on pre-period
for sd in (0.02, 0.03, 0.06):
    se = sd * sqrt(1 / 10 + 1 / 40)
    lo, hi = drop - 1.96 * se, drop + 1.96 * se
    print(f"region-level sd {sd:.0%}: se {se:.4f} | 95% interval {lo:.3%} to {hi:.3%} -> {lo*total:,.0f} to {hi*total:,.0f} | z {drop/se:.1f}")
assert round(0.03 * sqrt(0.125), 4) == 0.0106
# when does the interval reach the last-click 1%? credit 1,000,000 = 1% of sales
# simulate random 10-of-50 assignments: unadjusted vs pre-period-adjusted estimate
rng = np.random.default_rng(39)
size = rng.lognormal(0, 0.5, regions); size = size / size.mean() * per_region        # unequal regions
pre = size * np.exp(rng.normal(0, 0.03, regions))
true_eff = 0.04
est_raw, est_adj = [], []
for _ in range(4000):
    t = rng.permutation(regions)[:10]; c = np.setdiff1d(np.arange(regions), t)
    post = pre * np.exp(rng.normal(0, 0.03, regions)) * (1 - true_eff * np.isin(np.arange(regions), t))
    ratio_t = post[t].sum() / pre[t].sum(); ratio_c = post[c].sum() / pre[c].sum()
    est_adj.append(1 - ratio_t / ratio_c)                                              # change vs own pre-period
    est_raw.append(1 - post[t].mean() / post[c].mean())                                # levels only
est_raw, est_adj = np.array(est_raw), np.array(est_adj)
print("simulated 4,000 random assignments, true effect 4%:")
print("  level comparison: mean", round(est_raw.mean(), 4), "sd", round(est_raw.std(), 4))
print("  versus-own-pre-period: mean", round(est_adj.mean(), 4), "sd", round(est_adj.std(), 4))
assert est_adj.std() < est_raw.std() and abs(est_adj.mean() - 0.04) < 0.003
# share of assignments in which the estimate is below the last-click 1% credit level
print("share of assignments with estimated effect below 1%:", round((est_adj < 0.01).mean(), 4), "(adjusted) |", round((est_raw < 0.01).mean(), 4), "(unadjusted)")
```

**Output (my run):**
```
sales per region 2000000.0 | last-click share 0.01
A: incremental sales if 4% of with-video sales: 4000000.0 | vs last-click 4.0 x
observed total in the test period 99200000.0 | counterfactual with video everywhere 100000000 | incremental 800000.0 (this is the 10 paused regions only)
incremental as a share of the no-video level: 0.0417
10 paused regions lost 800000.0 in the test period; scaled x5 = 4000000.0
region-level sd 2%: se 0.0071 | 95% interval 2.614% to 5.386% -> 2,614,071 to 5,385,929 | z 5.7
region-level sd 3%: se 0.0106 | 95% interval 1.921% to 6.079% -> 1,921,106 to 6,078,894 | z 3.8
region-level sd 6%: se 0.0212 | 95% interval -0.158% to 8.158% -> -157,788 to 8,157,788 | z 1.9
simulated 4,000 random assignments, true effect 4%:
  level comparison: mean 0.0373 sd 0.1683
  versus-own-pre-period: mean 0.0399 sd 0.0114
share of assignments with estimated effect below 1%: 0.0045 (adjusted) | 0.412 (unadjusted)
```

**Follow-ups:**
- *Why might last click undercount video?* It credits the final touch, and video often creates demand that later converts through search or direct.
- *Could the true effect be bigger than the test?* Yes if spillover leaks sales into the kept regions; no if the paused regions got other media.
- *What next?* A larger, longer test with matched pairs, or varying spend levels to get a response curve.

**Common mistakes:**
- Treating the 4% as exact.
- Comparing regional levels without the pre-period.
- Using one on/off test to set the budget.
- Ignoring cost.

### Q40 ⭐ 🟢 E-commerce: 6% of 1,000,000 daily searches return no results, which is 60,000 searches, and a manual review of 500 of those found 200 (40%) were spelling or synonym problems and 100 (20%) were products the catalogue genuinely lacks. Estimate the daily searches in each of those two groups as projections, and explain what you would build first, how you would measure its effect, and how you would pass the missing-product signal to sellers.
**Asked at:** E-commerce ML material (prachub lists Shopify questions on product ranking for a marketplace, package delivery time prediction and personalised product feeds, and a CleverPrep Shopify guide lists search-ranking and embedding trade-offs; Interview Query notes e-commerce promotion and behaviour modelling); candidate-reported and prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** About 24,000 of the 60,000 zero-result searches a day are spelling or synonym problems and about 12,000 are products the catalogue lacks (projections from a 500-search review); I would build spelling and synonym handling first because it is the largest fixable group, measure it with an A/B test on those searches, and give sellers an aggregated, privacy-safe demand report for the missing products.

**Clarifying questions:**
- Were the 500 searches sampled at random from the 60,000 searches, or from distinct queries? Sampling searches weights head queries correctly; sampling queries does not.
- What are the other 200 (40%): filters too narrow, out of stock, ambiguous, junk? That group is as large as the spelling group and may be cheap to fix.
- How does the current search handle typos and synonyms (any correction, stemming, a synonym list)? It sets how much is new.
- Can a search that returns results still be bad? Fixing zero results should not just replace "no results" with irrelevant results.
- Which sellers can add listings, and is there a policy team for restricted items? It shapes what we can pass on.

**Approach:**
1. Projections: 6% x 1,000,000 = 60,000 zero-result searches. Spelling or synonym: 200 / 500 = 40% x 60,000 = 24,000 a day (95% range about 21,400 to 26,600). Genuinely missing: 100 / 500 = 20% x 60,000 = 12,000 a day (range about 9,900 to 14,100). Other: 40% = 24,000.
2. Build first: query understanding for spelling and synonyms. Start from logs: zero-result queries that users reformulate within the session into a query with clicks give pairs (typo to fixed query, trainers to sneakers). Combine with a vocabulary-based corrector. In a small test, string similarity fixed "runing shoes", "wireles headphones" and "fone charger" but could not fix "kettlebell" (missing) or "trainers" (a synonym), so synonyms need a separate dictionary or learned model.
3. Roll out safely: auto-correct only above a confidence threshold, otherwise show "did you mean"; always keep the user's original query visible.
4. Size the benefit: fixing half the spelling group puts 12,000 searches a day back to having results and lowers the zero-result rate from 6.0% to 4.8%; fixing 80% gives 4.08%.
5. Measure with an A/B test on searches that would have returned zero results: randomise users, compare search-to-click, add-to-cart and orders per search, revenue per search. Zero-result rate alone is a vanity metric because a correction that returns junk lowers it too.
6. Guardrails: relevance judged by a labelled sample of corrected searches (wrong correction rate), reformulation rate, latency, and bounce or exit rate.
7. Missing-product signal for sellers: normalise and cluster the 12,000-a-day group by intent, publish only terms searched by at least K distinct users (K = 20 in my toy example, which kept three terms and dropped two small ones, one of them a one-user term that looked like a person's name), exclude personal or sensitive queries and prohibited items, and verify the product is truly missing (not out of stock or mis-categorised).
8. Present to sellers as weekly demand gaps: term cluster, searches per day, trend, and the category. Check with the trust and policy team and legal or privacy about what can be shown to sellers. Measure the effect by gaps filled and sales on newly listed items.

**Metrics:**
- Zero-result rate = searches with no results / all searches (6%).
- Recovered searches = zero-result searches that now return results and get a click / zero-result searches.
- Search-to-click rate and orders per search on the treated group; revenue per search.
- Wrong-correction rate = corrections judged irrelevant / corrections shown.
- Seller side: gaps published, gaps filled, sales on filled gaps.

**Risks:**
- Auto-correcting a rare, correct word into a common one (a brand name) hurts users.
- Sampling searches versus queries changes the shares.
- The missing-product group may include illegal, restricted or irrelevant demand.
- Small counts in seller reports can expose individual users.
- 500 reviewed searches are a sample; ranges are about +/- 4 points.

**What the interviewer scores:**
- Strong: 24,000 and 12,000, labelled projections, and notices the other 24,000.
- Strong: builds query understanding first, with confidence thresholds and an A/B test on the affected searches.
- Strong: measures revenue or conversion, not only the zero-result rate; privacy threshold for the seller report.
- Weak: "build a bigger index"; "reduce the zero-result rate" as the only goal.

**Example:** Illustrative numbers from the run. 60,000 zero-result searches; 24,000 spelling or synonym, 12,000 missing, 24,000 other. Fixing half the spelling group moves the zero-result rate from 6.0% to 4.8%.
- Weak: "We should add more products so people find results."
- Strong: "About 24,000 a day are typos or synonyms and 12,000 are real catalogue gaps, so I would build spelling and synonym handling first, with a confidence threshold, and A/B test on those searches measuring orders per search. For the 12,000 I would send sellers a weekly list of terms searched by at least 20 users, after the policy team checks the list."

**Code:**
```python
import difflib
import numpy as np
from math import sqrt
from collections import Counter

searches, zr = 1_000_000, 0.06
zero = searches * zr
n, spell_k, missing_k = 500, 200, 100
print("zero-result searches/day", zero)
assert zero == 60_000
sp, mi = spell_k / n, missing_k / n
oth = 1 - sp - mi
proj = {"spelling/synonym": zero * sp, "genuinely missing": zero * mi, "other": zero * oth}
print({k: round(v) for k, v in proj.items()}, "| other share", round(oth, 2))
assert proj["spelling/synonym"] == 24_000 and proj["genuinely missing"] == 12_000 and round(proj["other"]) == 24_000
for name, k in (("spelling/synonym", spell_k), ("missing", missing_k)):
    p = k / n; se = sqrt(p * (1 - p) / n)
    print(f"{name}: share {p:.0%} +- {1.96*se:.3f} -> searches/day {zero*(p-1.96*se):,.0f} to {zero*(p+1.96*se):,.0f}")
assert round(zero * (0.4 - 1.96 * sqrt(0.4 * 0.6 / 500))) == 21424
# effect of fixing a share of the spelling group
for fix in (0.5, 0.8):
    fixed = proj["spelling/synonym"] * fix
    print(f"fix {fix:.0%} of the spelling group -> {fixed:,.0f} searches now return results; zero-result rate {(zero-fixed)/searches:.2%}")
assert (zero - 12_000) / searches == 0.048 and (zero - 19_200) / searches == 0.0408
# a correction that helps nobody if it is wrong: precision matters. Toy vocabulary + difflib
vocab = ["running shoes", "wireless headphones", "phone charger", "yoga mat", "water bottle", "laptop stand"]
queries = ["runing shoes", "wireles headphones", "fone charger", "yoga mat", "kettlebell", "lap top stand", "trainers"]
for q in queries:
    m = difflib.get_close_matches(q, vocab, n=1, cutoff=0.8)
    print(f"{q!r:24} -> {m[0] if m else None}")
fixed = [q for q in queries if difflib.get_close_matches(q, vocab, n=1, cutoff=0.8)]
assert "runing shoes" in fixed and "fone charger" in fixed and "kettlebell" not in fixed and "trainers" not in fixed   # string similarity cannot fix a synonym or a missing product
# missing-product signal with a privacy threshold: count distinct users, publish only if >= k
rng = np.random.default_rng(40)
terms = ["kettlebell 16kg", "cast iron dutch oven", "left handed scissors", "rare vinyl X", "jane doe address"]
log = []
for t, cnt, users in (("kettlebell 16kg", 900, 600), ("cast iron dutch oven", 400, 250), ("left handed scissors", 120, 90), ("rare vinyl X", 15, 4), ("jane doe address", 6, 1)):
    uids = rng.integers(0, users, cnt)
    log += [(t, int(u)) for u in uids]
cnt = Counter(t for t, u in log); du = {t: len({u for tt, u in log if tt == t}) for t in cnt}
K = 20
pub = [t for t in cnt if du[t] >= K]
print({t: (cnt[t], du[t]) for t in cnt})
print("published to sellers (>= 20 distinct users):", pub)
assert "jane doe address" not in pub and "rare vinyl X" not in pub and len(pub) == 3
```

**Output (my run):**
```
zero-result searches/day 60000.0
{'spelling/synonym': 24000, 'genuinely missing': 12000, 'other': 24000} | other share 0.4
spelling/synonym: share 40% +- 0.043 -> searches/day 21,424 to 26,576
missing: share 20% +- 0.035 -> searches/day 9,896 to 14,104
fix 50% of the spelling group -> 12,000 searches now return results; zero-result rate 4.80%
fix 80% of the spelling group -> 19,200 searches now return results; zero-result rate 4.08%
'runing shoes'           -> running shoes
'wireles headphones'     -> wireless headphones
'fone charger'           -> phone charger
'yoga mat'               -> yoga mat
'kettlebell'             -> None
'lap top stand'          -> laptop stand
'trainers'               -> None
{'kettlebell 16kg': (900, 460), 'cast iron dutch oven': (400, 210), 'left handed scissors': (120, 71), 'rare vinyl X': (15, 4), 'jane doe address': (6, 1)}
published to sellers (>= 20 distinct users): ['kettlebell 16kg', 'cast iron dutch oven', 'left handed scissors']
```

**Follow-ups:**
- *Why not use a language model for every query?* It may help synonyms, but latency, cost and wrong corrections need an A/B test; start with logs and a dictionary.
- *How do you handle the 40% other?* Sample and classify them; filters and stock issues may need product changes rather than ML.
- *What if sellers game the demand report?* Use distinct users, a minimum history and a review step.

**Common mistakes:**
- Reporting shares from 500 searches as exact.
- Celebrating a lower zero-result rate without checking relevance.
- Publishing rare queries.
- Treating missing products and typos as the same problem.

### Q41 ⭐ 🟢 Healthcare: A research extract of 50,000 patient records is prepared for a partner, with age in years, a 3-digit postcode area and sex as the only quasi-identifiers. Counting shows 4,000 distinct combinations of these three fields and 600 combinations appear exactly once. Compute the share of records that are unique on these fields and explain why it matters, what generalisation or suppression you would try, and which questions go to the privacy officer before anything is shared.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to de-identification and re-identification risk in health-data sharing material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** 600 of 50,000 records are unique on age, postcode area and sex, so 1.2% of people can be singled out by those three fields alone; I would generalise first, suppress what is left, and send the residual questions to the privacy officer.

**Clarifying questions:**
- Who receives the data and under what agreement? It sets how much re-identification risk the business will accept.
- What other datasets could the partner link to (voter-type lists, their own customer files)? Uniqueness only hurts if someone can link.
- Which analyses does the partner really need (exact age? small-area geography)? That decides how much I can coarsen.
- Are there other fields in the extract that act as identifiers (admission date, rare diagnosis, free text)? The prompt names only three; the real list is usually longer.
- Is the 4,000 combinations count over the whole extract or per site? A base mix-up changes the answer.

**Approach:**
1. Get the base right. Unique records are 600 out of 50,000 = 1.2%. The 15% figure (600 of 4,000 combinations) is a share of combinations, not of people.
2. Look at the full group-size distribution, not only singletons. A record in a group of 2 or 3 is also weakly protected. Report the share of records in groups smaller than k (for example 5).
3. Generalise: age to 5- or 10-year bands, 3-digit area to a coarser area, and top-code old ages. Re-run the counts after each step and keep the utility cost in view.
4. Suppress or drop the few records that stay in small groups, or withhold rare categories.
5. Re-count on the final file and also test against the other fields that might identify (the three are not the whole story).
6. Document the choices and take the residual risk question to the privacy officer before anything leaves.

**Metrics:**
- Unique share = records in groups of size 1 / total records = 600 / 50,000 = 1.2%.
- Share of records in groups smaller than k = records in groups with size less than k / total records.
- Minimum group size after treatment (the k you actually achieved).
- Utility guardrail: how much do the partner's key estimates (age distribution, regional rates) move after generalisation?

**Risks:**
- Sample uniqueness is not population uniqueness. A record unique in this extract may be common in the population (safer) or the extract may be a near-census of a small region (riskier).
- Other fields can break k-anonymity even when these three are fine.
- Over-generalising can destroy the research value; under-generalising can expose people.
- Linkage risk changes over time as new datasets appear.

**What the interviewer scores:**
- Strong: computes 1.2% on the right base, separates it from 15%, proposes a measurable k target and a utility check, and names open questions for the privacy officer.
- Strong: says unique on three fields does not mean identified; it depends on who can link.
- Weak: says "anonymised, so fine", or "remove names and we are done".
- Weak: makes legal claims ("this breaches the law") instead of asking the privacy or compliance team.

**Example:** (illustrative numbers from the prompt) 50,000 records, 4,000 combinations, 600 singletons.
- Unique records: 600 / 50,000 = 1.2%. The other 49,400 records sit in 3,400 combinations, average group about 14.5.
- Weak answer: "Only 1.2%, so it is basically safe, we can share it."
- Strong answer: "1.2% are unique on these three fields, which is 600 real people who could be matched by anyone holding age, area and sex. I would band age, coarsen the area, drop what stays below a group size of 5, re-count, and ask the privacy officer which linkage sources and which residual risk are acceptable before we send anything."

**Code:**
```python
# Q41: uniqueness on quasi-identifiers (prompt numbers) + a synthetic generalisation demo (invented data)
import numpy as np
from collections import Counter

records, combos, singles = 50_000, 4_000, 600
print("share of RECORDS unique   :", singles / records)        # what the question asks
print("share of COMBINATIONS that are unique:", singles / combos)  # a different base, easy to confuse
rest_records, rest_combos = records - singles, combos - singles
print("other records / combos     :", rest_records, rest_combos, "avg group", round(rest_records / rest_combos, 2))
assert singles / records == 0.012 and singles / combos == 0.15
assert rest_records == 49_400 and rest_combos == 3_400

# Synthetic illustration only (NOT the prompt's data): how banding changes uniqueness and k.
rng = np.random.default_rng(7)
n = 50_000
age = np.clip(rng.normal(52, 18, n).round(), 0, 99).astype(int)
area = rng.zipf(1.6, n) % 400            # 3-digit-like area codes, skewed: a few big, many tiny
sex = rng.integers(0, 2, n)

def stats(keys):
    c = Counter(keys)
    sizes = np.array(list(c.values()))
    smallest = min(sizes)
    uniq = int((sizes == 1).sum())
    k5_fail = int(sizes[sizes < 5].sum())   # records sitting in groups smaller than 5
    return len(c), uniq, uniq / n, k5_fail / n, smallest

raw = stats(zip(age, area, sex))
band = stats(zip(age // 10, area, sex))               # 10-year bands
band2 = stats(zip(age // 10, area // 10, sex))        # plus coarser area (2-digit style)
for name, s in [("raw age/area/sex", raw), ("10y age band", band), ("10y band + coarser area", band2)]:
    print(f"{name:26} combos={s[0]:5d} unique_records={s[1]:5d} unique_share={s[2]:.3f} share_in_groups_lt5={s[3]:.3f}")
assert raw[2] > band[2] > band2[2] or band[2] >= band2[2] and raw[2] > band2[2]
assert band2[3] < raw[3]
# suppression: drop the records still in groups smaller than 5 and re-check
keys = list(zip(age // 10, area // 10, sex))
c = Counter(keys)
kept = [k for k in keys if c[k] >= 5]
c2 = Counter(kept)
print("after suppressing small groups: records kept", len(kept), "min group", min(c2.values()))
assert min(c2.values()) >= 5
```

**Output (my run):**
```text
share of RECORDS unique   : 0.012
share of COMBINATIONS that are unique: 0.15
other records / combos     : 49400 3400 avg group 14.53
raw age/area/sex           combos= 7855 unique_records= 4809 unique_share=0.096 share_in_groups_lt5=0.184
10y age band               combos= 2923 unique_records= 1450 unique_share=0.029 share_in_groups_lt5=0.074
10y band + coarser area    combos=  654 unique_records=  120 unique_share=0.002 share_in_groups_lt5=0.014
after suppressing small groups: records kept 49294 min group 5
```

The synthetic part uses invented data to show the direction (banding lowers uniqueness, suppression guarantees a minimum group size); it does not reproduce the prompt's 4,000 and 600.

**Follow-ups:**
- Is k-anonymity enough? No. It ignores what the group members share (a group of 5 all with the same diagnosis still leaks it). Ask the privacy officer about further checks.
- What if the partner insists on exact ages? Offer a controlled-access environment instead of a file, and ask the privacy and legal teams what terms apply.

**Common mistakes:** Quoting 15% as the unique share of people. Checking only singletons. Treating three named fields as the full identifier list. Stating legal conclusions as facts.

### Q42 ⭐ 🟡 Fintech: Of 50,000 monthly onboarding applications, 0.4% (200) are synthetic or stolen identities, a retrospective estimate. A document-and-face score auto-approves 35,000 applications (70%) and sends 15,000 to manual review at 60 each, and the auto-approve band contains 20 of the 200 bad identities. Compute the manual review cost, the share of bad identities that skip review, and the bad-identity rate in each band, and describe how you would revisit the band edge while leaving the risk appetite to the business and compliance.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to KYC identity verification triage in fintech onboarding material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Manual review costs 15,000 x 60 = 900,000 a month, 10% of the bad identities (20 of 200) skip review, and the bad rate is about 0.057% in auto-approve versus 1.2% in review, so I would price the band edge by the cost of each extra bad identity caught and let the business and compliance set the appetite.

**Clarifying questions:**
- How was the 200 estimated (retrospective investigation, later chargebacks, a sample)? It is an estimate and bad identities that were never discovered are missing, so 10% skipping review is a floor-ish guess.
- Does manual review catch every bad identity it sees? If not, the real leakage is bigger than 10%.
- What does one missed bad identity cost (loss, downstream fraud, investigation)? Without it I cannot find the edge.
- Is there a capacity limit on reviewers? A fixed team forces the edge, regardless of cost per case.
- Are there step-up options between auto-approve and manual review (extra document, liveness retry)? They shrink the review pile cheaply.

**Approach:**
1. Compute the three numbers from counts: cost, skip share, band rates.
2. Rank applications by score and plot bad rate by score decile, to see how sharply risk falls near the edge.
3. Price the edge: extra review cost for the next slice of applications divided by the extra bad identities it would catch. That is the marginal cost per bad caught.
4. Compare with the business's own cost of a missed bad identity. Move the edge only while marginal cost per catch is below that cost. The business and compliance own the risk appetite; I supply the curve.
5. Add cheap step-up checks inside the review band to cut volume.
6. Re-estimate after labels mature, because the 200 is a retrospective estimate and the bad count in the auto band is the least certain number.

**Metrics:**
- Review cost = reviewed applications x cost per review = 15,000 x 60 = 900,000.
- Skip share = bad identities in auto-approve / all bad identities = 20 / 200 = 10%.
- Band bad rate = bad identities in the band / applications in the band: auto 20 / 35,000 = 0.057%, review 180 / 15,000 = 1.2%.
- Marginal cost per extra bad caught when widening the review band.
- Guardrails: approval time, false-reject rate for genuine applicants, reviewer queue age.

**Risks:**
- The 20 in the auto band is an estimate of discovered cases; undiscovered ones raise the skip share.
- Reviewers also miss cases, so review is not a perfect filter.
- Pushing the edge to catch more can raise friction for genuine applicants.
- Fraudsters adapt to the score, so today's band rates will not hold.

**What the interviewer scores:**
- Strong: gets 900,000, 10%, 0.057% and 1.2% right, and says the 200 and the 20 are estimates.
- Strong: frames the edge as marginal cost per bad caught against the cost of a miss, and leaves appetite to the business and compliance.
- Weak: reports only the average 0.4% bad rate.
- Weak: picks a threshold by AUC or accuracy with no cost.

**Example:** (illustrative) Widen review by 5,000 applications (extra 300,000) and suppose that slice holds 8 bad identities. That is 37,500 per extra bad caught. If one miss costs the business 10,000, widening is not worth it; if a miss costs 100,000, it is.
- Weak: "Send more to review to be safe."
- Strong: "The first 15,000 reviewed cost 5,000 per bad found at best. The next slice costs 37,500 per catch. I will show that to the business and let them decide whether a miss costs more than that."

**Code:**
```python
# Q42: onboarding bands (prompt numbers, illustrative)
apps, bad = 50_000, 200
auto, review = 35_000, 15_000
bad_auto = 20
bad_review = bad - bad_auto
cost_each = 60
assert auto + review == apps and abs(bad / apps - 0.004) < 1e-12 and auto / apps == 0.7

review_cost = review * cost_each
skip = bad_auto / bad
rate_auto, rate_rev = bad_auto / auto, bad_review / review
print("manual review cost:", review_cost)
print("share of bad identities that skip review:", skip)
print(f"bad rate auto-approve: {rate_auto:.4%}  review: {rate_rev:.4%}  overall: {bad/apps:.2%}")
print("review band is", round(rate_rev / rate_auto, 1), "x riskier than auto band")
assert review_cost == 900_000 and skip == 0.10
assert round(rate_auto * 100, 3) == 0.057 and round(rate_rev * 100, 2) == 1.20

# cost per bad identity found, IF review catches every bad one in its band (best case)
print("review spend per bad identity found (best case):", review_cost / bad_review)
assert review_cost / bad_review == 5_000

# moving the band edge: illustrative table, assuming (invented) the next 5,000 apps below the edge hold 8 more bad ones
extra_apps, extra_bad = 5_000, 8
new_cost = (review + extra_apps) * cost_each
marginal_cost_per_bad = extra_apps * cost_each / extra_bad
print("widen review by 5,000 apps: extra cost", extra_apps * cost_each, "extra bad caught", extra_bad,
      "cost per extra bad", marginal_cost_per_bad)
assert marginal_cost_per_bad == 37_500
print("residual skip share after widening:", (bad_auto - extra_bad) / bad)
assert (bad_auto - extra_bad) / bad == 0.06
```

**Output (my run):**
```text
manual review cost: 900000
share of bad identities that skip review: 0.1
bad rate auto-approve: 0.0571%  review: 1.2000%  overall: 0.40%
review band is 21.0 x riskier than auto band
review spend per bad identity found (best case): 5000.0
widen review by 5,000 apps: extra cost 300000 extra bad caught 8 cost per extra bad 37500.0
residual skip share after widening: 0.06
```

The widening slice (5,000 applications, 8 bad) is an invented assumption to show the calculation.

**Follow-ups:**
- Why not use the 0.4% overall rate? It hides that risk is 21 times higher in the review band than in the auto band, which is the point of the score.
- How do you check the score is still good later? Track the bad rate by band as labels mature, and watch score drift.

**Common mistakes:** Treating the retrospective 200 as exact. Assuming review catches everything. Setting the edge to hit a review budget without checking the cost of a miss. Deciding risk appetite yourself.

### Q43 ⭐ 🟡 E-commerce: A new recommender raised homepage click-through from 4.00% to 4.24% (a 6% relative rise, 0.24 points absolute, measured in an A/B test), while GMV per user fell from 500.0 to 497.5 (0.5% relative) and the share of impressions on long-tail items fell from 30% to 18% (absolute points). Explain the possible mechanism, which further metrics you would inspect, and how you would decide whether to ship.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to recommendation diversity and long-tail exposure in e-commerce material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** CTR rose 0.24 points (6% relative) while GMV per user fell 0.5% and long-tail exposure fell 12 points (30% to 18%, a 40% relative drop), so the recommender probably learned to show popular, clicky items; I would not ship on CTR, and I first need the confidence interval on GMV before calling the 0.5% a real loss.

**Clarifying questions:**
- How many users and impressions per arm, and what is the spread of GMV per user? The prompt gives no variance, so I cannot say if the 0.5% drop is real or noise.
- How long did the test run? Novelty lifts CTR early; GMV and returns lag.
- What is GMV measured on (same session, 7 days, 28 days)? Click gains may convert later or never.
- Is the long-tail share by impressions or by sales? Seller and catalogue health depend on sales.
- What does the business weight: short-term GMV, seller diversity, margin? That decides the guardrails.

**Approach:**
1. Treat CTR as a proxy, not the goal. Check the primary metric (GMV or orders per user) with a confidence interval.
2. Mechanism: the model optimised clicks, so it shifted impressions to popular, attractive-looking items (head items click more). Clicks rose, but fewer clicks led to basket value, and tail discovery fell.
3. Decompose: click-to-add-to-cart rate, add-to-cart-to-purchase, average order value, items per order, return rate, margin, and new-item and new-seller exposure.
4. Segment: new versus returning users, categories, heavy users. A CTR gain that is confined to one segment can hide a loss in another.
5. Decide with a pre-agreed rule: ship only if GMV per user is not worse than a stated margin and the long-tail guardrail holds. Otherwise iterate (add a conversion or diversity term to the objective) and retest.
6. Consider a holdback after launch to watch long-run effects.

**Metrics:**
- CTR = clicks / impressions. GMV per user = total order value / users in the arm. Long-tail share = impressions on long-tail items / all impressions (absolute points).
- Conversion per click = orders / clicks. Average order value = GMV / orders.
- Guardrails: return rate, margin per user, seller concentration, session length and repeat visits.

**Risks:**
- Reading a 0.5% GMV change as real or as nothing without a confidence interval.
- Novelty effect inflating CTR.
- Tail starvation: sellers of tail items lose traffic and may leave, harming the catalogue later.
- Feedback loop: less tail exposure gives less tail data, so the model favours the head even more.

**What the interviewer scores:**
- Strong: sees CTR as a proxy, offers a mechanism (head bias), names the metrics to decompose, and wants uncertainty on GMV before deciding.
- Strong: sets a ship rule with a guardrail and a margin.
- Weak: "CTR is up 6%, ship it."
- Weak: "GMV is down so it is bad" with no interval.

**Example:** (illustrative; the prompt gives no sample size) With 200,000 users per arm and a GMV sd of 2,000 per user, the GMV difference is -2.5 with a standard error of 6.3, so z is about -0.4 and the 95% interval is roughly -3.0% to +2.0%. That does not show a loss, but it does not rule out a 2.5% loss. Detecting a 0.5% change would need about 10 million users per arm.
- Weak: "GMV fell 0.5%, so the model is bad." (or) "CTR rose 6%, so it is good."
- Strong: "CTR is a proxy. GMV moved the wrong way and tail share dropped 12 points. I need the interval on GMV; if it is under-powered I will say so and not ship on CTR. I will break down click-to-order and order value, and ship only if GMV is not worse than our margin and the tail guardrail holds."

**Code:**
```python
# Q43: recommender, CTR up, GMV down. Prompt numbers + INVENTED sample sizes / variance (the prompt gives none).
import math
ctr0, ctr1 = 0.0400, 0.0424
print("CTR abs diff pts:", round((ctr1 - ctr0) * 100, 2), " relative:", round(ctr1 / ctr0 - 1, 4))
assert round((ctr1 - ctr0) * 100, 2) == 0.24 and round(ctr1 / ctr0 - 1, 4) == 0.06
g0, g1 = 500.0, 497.5
print("GMV/user rel change:", round(g1 / g0 - 1, 4))
assert round(g1 / g0 - 1, 4) == -0.005
lt0, lt1 = 0.30, 0.18
print("long-tail share: abs pts", round((lt1 - lt0) * 100), " relative", round(lt1 / lt0 - 1, 2))
assert round((lt1 - lt0) * 100) == -12 and round(lt1 / lt0 - 1, 2) == -0.40

# invented: 2,000,000 impressions per arm
imp = 2_000_000
se_ctr = math.sqrt(ctr0 * (1 - ctr0) / imp + ctr1 * (1 - ctr1) / imp)
z_ctr = (ctr1 - ctr0) / se_ctr
print("CTR z (2M impressions/arm, invented):", round(z_ctr, 1))
assert z_ctr > 10

# invented: 200,000 users per arm, per-user GMV sd 2,000 (heavy-tailed)
users, sd = 200_000, 2_000.0
se_g = sd * math.sqrt(2 / users)
d = g1 - g0
lo, hi = d - 1.96 * se_g, d + 1.96 * se_g
print(f"GMV diff {d} se {se_g:.2f} z {d/se_g:.2f} 95% CI [{lo:.1f}, {hi:.1f}] = [{lo/g0:.2%}, {hi/g0:.2%}]")
assert abs(d / se_g) < 1.96            # with these inputs the GMV drop is not distinguishable from zero
assert lo / g0 < -0.025                # but a 2.5% loss is not ruled out

# users per arm needed to detect a 0.5% GMV change (80% power, 5% two-sided)
delta = 0.005 * g0
n_needed = 2 * ((1.96 + 0.8416) ** 2) * sd ** 2 / delta ** 2
print("users per arm to detect 0.5% GMV change:", round(n_needed))
assert 9_900_000 < n_needed < 10_100_000
```

**Output (my run):**
```text
CTR abs diff pts: 0.24  relative: 0.06
GMV/user rel change: -0.005
long-tail share: abs pts -12  relative -0.4
CTR z (2M impressions/arm, invented): 12.1
GMV diff -2.5 se 6.32 z -0.40 95% CI [-14.9, 9.9] = [-2.98%, 1.98%]
users per arm to detect 0.5% GMV change: 10046672
```

**Follow-ups:**
- Would you ship if GMV were flat but tail share fell? Only if the business accepts the seller-diversity cost; otherwise add a diversity or exposure constraint.
- How do you fix it? Optimise a blended objective (expected purchase value, not clicks) and add exposure floors for the tail.

**Common mistakes:** Calling the 0.5% drop significant or irrelevant without a variance. Mixing relative and absolute points on the long-tail share. Ignoring novelty effects. Judging by CTR alone.

### Q44 ⭐ 🟡 Healthcare: A deterioration model uses a feature 'lactate was measured' because clinicians order the test when they are worried. At hospital A the test is ordered for 60% of patients and the model's AUC is 0.85, while at hospital B it is ordered for 20% and the AUC is 0.74 (both measured, on different patient populations). Explain why the feature transports poorly, how to treat informative missingness across sites, and what you would validate before the model runs at hospital B.
**Asked at:** Clinical-AI external-validation coverage (Fierce Healthcare, MedCity News and JAMA Internal Medicine pages on the external validation of a widely deployed sepsis model, which reported low sensitivity, a modest positive predictive value, alerts on a large share of patients and a billing-code outcome definition; a newsletter piece on local validation and tracking override patterns); published news and research, not an interview bank; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** "Lactate was measured" is a record of a clinician's worry, not of the patient, so its meaning and its frequency change with each hospital's ordering habits; I would stop treating it as a plain feature, test the model with and without it at hospital B, and not switch it on until B's own validation passes.

**Clarifying questions:**
- The two AUCs are on different patient populations, so the 0.85 versus 0.74 gap mixes feature effects with case mix and prevalence. Do the outcome definition and prediction time also match? I cannot blame the feature alone.
- How does hospital B decide to order lactate (protocol, sepsis pathway, cost, lab turnaround)? It tells me what "ordered" means there.
- What is the prediction time? If lactate is ordered after the worry already began, the model uses the clinician's judgement as input and may be copying it.
- What action does the alert trigger? If it only helps clinicians who were already worried, the added value is small.
- What do B's data hold: enough events to validate locally?

**Approach:**
1. Name the problem: informative missingness. Whether the value exists carries signal about the label, and that signal depends on local practice. The model learned A's ordering behaviour as if it were physiology.
2. Separate two effects of the feature: the measured value (physiology, transports reasonably) and the "was ordered" flag (behaviour, transports badly).
3. Run ablations at both sites: full model, model without the ordered flag, model without lactate at all, and a model where lactate is only used when ordered. Compare AUC and, more importantly, sensitivity at a fixed alert rate and calibration.
4. Check performance in subgroups at B: ordered versus not ordered. If the model is much weaker where lactate is absent, that is where B's patients mostly sit (80% there).
5. Options: drop the flag and keep the value; build site-specific models or recalibrate; add features that do not depend on ordering (vitals trends, nursing notes timing); or use a protocol-driven version at B.
6. Validate prospectively at B (silent mode) with its own thresholds before any alert is live.

**Metrics:**
- AUC (probability a random event patient scores above a random non-event patient) at each site, with confidence intervals.
- Sensitivity and PPV at the same alert rate (for example top 5% flagged per day). AUC alone hides alert burden.
- Calibration (observed versus predicted risk by decile) at B.
- Subgroup AUC: lactate ordered versus not.
- Guardrail: alerts per 100 patient-days per ward.

**Risks:**
- Learned behaviour shortcuts: the model reads worry, so it adds little for patients no one is worried about, which is exactly where early warning matters.
- Feedback: if the model changes ordering behaviour, the feature's meaning shifts again (the model's own deployment changes its inputs).
- A different outcome definition or timing between sites can create part of the gap.
- Retraining on B may not help, because the information is simply not collected for 80% of patients (see the simulation).

**What the interviewer scores:**
- Strong: explains the flag as clinician behaviour, separates value from flag, proposes ablations and a site-level silent validation.
- Strong: points out that 0.85 versus 0.74 is not a clean test of the feature.
- Weak: "impute the missing lactate with the mean and move on".
- Weak: "just retrain on hospital B", with no thought about what B does not measure.

**Example:** (illustrative) Hospital A orders lactate for 60% of patients, hospital B for 20%. A model trained at A scores 0.85 at A and 0.74 at B (the prompt's numbers, measured on different patient populations).
- Weak: "The model is overfit; retrain it."
- Strong: "At B most patients have no lactate, so the model loses its strongest input and the ordered flag means something different there. I will compare full, no-flag and no-lactate versions at B, check sensitivity at a fixed alert rate and calibration, and run it silently before any live alert."

**Code:**
```python
# Q44: informative missingness across sites. SYNTHETIC simulation (invented), plus the prompt's two AUCs.
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(11)

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def make(n, order_rate):
    sev = rng.normal(size=n)                                  # true latent severity
    y = (rng.random(n) < 1 / (1 + np.exp(-(1.6 * sev - 3.0)))).astype(int)   # deterioration
    vit = sev + rng.normal(0, 1.5, n)                         # vitals-based signal, always present
    worry = sev + rng.normal(0, 0.7, n)                       # clinician worry
    thr = np.quantile(worry, 1 - order_rate)
    ordered = (worry > thr).astype(float)
    lact = (sev + rng.normal(0, 0.5, n)) * ordered            # value only if ordered
    return y, np.c_[vit, ordered, lact]

def fit(X, y, it=30):
    X1 = np.c_[np.ones(len(X)), X]; b = np.zeros(X1.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-X1 @ b)); W = p * (1 - p)
        b += np.linalg.solve(X1.T @ (X1 * W[:, None]) + 1e-6 * np.eye(len(b)), X1.T @ (y - p))
    return b
def score(b, X): return np.c_[np.ones(len(X)), X] @ b

N = 200_000
yA, XA = make(N, 0.60); yA2, XA2 = make(N, 0.60); yB, XB = make(N, 0.20)
print("ordering rate A / B:", XA[:, 1].mean().round(2), XB[:, 1].mean().round(2))
assert abs(XA[:, 1].mean() - 0.6) < 0.01 and abs(XB[:, 1].mean() - 0.2) < 0.01
b = fit(XA, yA)
a_a, a_b = auc(yA2, score(b, XA2)), auc(yB, score(b, XB))
print("model trained at A: AUC at A", round(a_a, 3), " AUC at B", round(a_b, 3), " (prompt: 0.85 vs 0.74, measured, different patients)")
assert a_a > a_b
# retrain at B, or drop the ordering-driven lactate features: what does each buy?
yB1, XB1 = make(N, 0.20); yB2, XB2 = make(N, 0.20)
bB = fit(XB1, yB1)
print("trained at B, AUC at B:", round(auc(yB2, score(bB, XB2)), 3))
bV = fit(XA[:, :1], yA)
print("vitals only (no lactate feature) at A / at B:", round(auc(yA2, score(bV, XA2[:, :1])), 3), round(auc(yB, score(bV, XB[:, :1])), 3))
assert abs(auc(yA2, score(bV, XA2[:, :1])) - auc(yB, score(bV, XB[:, :1]))) < 0.02   # stable but weaker
print("lactate only when ordered; AUC among ordered at B:", round(auc(yB[XB[:, 1] == 1], score(b, XB[XB[:, 1] == 1])), 3),
      " among not ordered:", round(auc(yB[XB[:, 1] == 0], score(b, XB[XB[:, 1] == 0])), 3))
```

**Output (my run):**
```text
ordering rate A / B: 0.6 0.2
model trained at A: AUC at A 0.807  AUC at B 0.768  (prompt: 0.85 vs 0.74, measured, different patients)
trained at B, AUC at B: 0.765
vitals only (no lactate feature) at A / at B: 0.694 0.696
lactate only when ordered; AUC among ordered at B: 0.717  among not ordered: 0.653
```

This is a synthetic simulation (invented severity, ordering and outcome model), not the prompt's data; it does not reproduce 0.85 and 0.74. It shows three things: AUC falls when lactate is ordered less (0.807 to 0.768), retraining at the low-ordering site did not recover it (0.765, because the information is not collected), and the vitals-only model is stable across sites but weaker (about 0.69).

**Follow-ups:**
- Can you impute the missing lactate? Imputing from the other features adds nothing the model did not have; the "not measured" state itself carries information, so treat it as its own category or avoid the flag.
- How do you know the model is not just copying the clinician? Compare against a baseline that uses only the ordered flag, and check performance before any worry-driven test.

**Common mistakes:** Blaming the AUC gap entirely on the feature. Imputing and forgetting that missing is informative. Retraining at B and assuming recovery. Validating only on A.

### Q45 ⭐ 🟡 Ads: Three creatives were each shown 2,000 times and got 40, 50 and 46 clicks, which are rates of 2.0%, 2.5% and 2.3%. The standard error of creative B's own rate is about 0.35 points (the square root of 0.025 times 0.975 over 2,000), while the standard error of the difference between B and A is about 0.47 points. How would you decide how to split the next day's impressions, why might you not simply pick B, and how would you handle creative fatigue?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to creative selection with bandits in ads system-design material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** B leads at 2.5% but its own standard error is about 0.35 points and the gap that matters, B minus A, has a standard error of about 0.47 points (z about 1.07), so nothing is settled; I would split traffic by the probability each creative is best (about 8%, 61%, 31%), so B gets most of tomorrow but A and C keep getting data, and I would plan for fatigue.

**Clarifying questions:**
- Is the 2,000 impressions each from the same time window and audience? Different hours or audiences make the rates not comparable.
- What is the goal metric: clicks, conversions, or value? A creative can win on clicks and lose on conversions.
- How many impressions will the next day have and how many creatives can we add? It fixes how much exploring we can afford.
- How fast do users repeat? Frequency decides fatigue.
- Is there a minimum exposure rule (brand or contract)? It limits how far we can concentrate.

**Approach:**
1. Compare the differences, not the single rates. The 0.35-point standard error is B's own; the B minus A standard error (about 0.47 points, as the prompt states) is sqrt(0.025 x 0.975 / 2000 + 0.02 x 0.98 / 2000) = 0.47 points, so the 0.5-point lead is z about 1.07, inside noise. B minus C is z about 0.41.
2. Treat it as a bandit problem: keep a Beta posterior per creative (1 + clicks, 1 + non-clicks) and allocate impressions in proportion to the probability each one is best (Thompson-style).
3. Keep a floor of exploration (for example at least 5% per arm) so a good creative with bad early luck can recover and fatigue is noticed.
4. Why not simply pick B? A 61% chance of being best means a 39% chance it is not; the cost of exploring a day is small compared to locking in the wrong creative.
5. Fatigue: track CTR by creative age and by frequency per user. Rotate in new creatives, cap frequency, and let the posterior use a recency window (discount old data) so a fading creative loses allocation.
6. Check the goal metric downstream (conversion) once enough data exists.

**Metrics:**
- CTR = clicks / impressions per creative; difference with its standard error sqrt(p1(1-p1)/n1 + p2(1-p2)/n2).
- P(best) per creative from the posterior; expected regret (clicks lost versus always showing the true best).
- Fatigue: CTR by days of exposure and by user frequency bucket.
- Guardrails: frequency per user, conversion rate, spend pacing.

**Risks:**
- Peeking and early stopping: picking B on day one inflates false wins.
- Novelty: new creatives start high and decay.
- Non-stationarity: day-of-week and audience shifts move all CTRs together.
- Clicks that do not convert (clickbait creatives).

**What the interviewer scores:**
- Strong: notices the standard error of the difference is larger than B's own, gives the 0.47 and z about 1.07, and moves to a bandit with exploration.
- Strong: raises fatigue with a concrete tracking plan.
- Weak: "B has the highest rate, send everything to B."
- Weak: "run a fixed A/B/C test for two weeks and do nothing until then" with no thought for the cost of waiting.

**Example:** (illustrative, the prompt's counts) Posteriors give P(best) of about A 0.08, B 0.61, C 0.31. For 30,000 impressions tomorrow that is about 2,480 / 18,289 / 9,231.
- Weak: "B won, 2.5% beats 2.0%."
- Strong: "B is ahead, but B minus A is 0.5 points with a standard error of 0.47, so I cannot call it. I will give B about 60% of tomorrow, keep the others in play, and watch CTR by creative age because fatigue will erode B."

**Code:**
```python
# Q45: three creatives, 2,000 impressions each. Prompt numbers + Thompson-style allocation (seeded).
import math
import numpy as np
n = 2000
clicks = {"A": 40, "B": 50, "C": 46}
rates = {k: v / n for k, v in clicks.items()}
print("rates:", rates)
assert rates == {"A": 0.02, "B": 0.025, "C": 0.023}
se_B = math.sqrt(0.025 * 0.975 / n)
print("SE of B's own rate (points):", round(se_B * 100, 3))
assert round(se_B * 100, 2) == 0.35

# the comparison that matters is the DIFFERENCE, whose SE is larger than B's own SE
def se_diff(p, q): return math.sqrt(p * (1 - p) / n + q * (1 - q) / n)
for other in ("A", "C"):
    d = rates["B"] - rates[other]; s = se_diff(rates["B"], rates[other])
    print(f"B - {other}: diff {d*100:.2f} pts, SE {s*100:.3f} pts, z {d/s:.2f}, 95% CI [{(d-1.96*s)*100:.2f}, {(d+1.96*s)*100:.2f}] pts")
dBA = rates["B"] - rates["A"]; sBA = se_diff(rates["B"], rates["A"])
assert abs(dBA / sBA) < 1.96            # B vs A is not significant at 5% two-sided
assert round(sBA * 100, 2) == 0.47

# Beta(1+clicks, 1+misses) posteriors; probability each creative is the best, and allocation by that probability
rng = np.random.default_rng(5)
draws = np.column_stack([rng.beta(1 + c, 1 + n - c, 200_000) for c in clicks.values()])
best = np.bincount(draws.argmax(1), minlength=3) / len(draws)
print("P(best) A, B, C:", best.round(3))
assert best[1] == best.max() and best[1] < 0.7      # B leads but is far from certain
next_day = 30_000
alloc = (best * next_day).round().astype(int)
print("next-day split of 30,000 impressions:", {k: int(v) for k, v in zip("ABC", alloc)})
assert alloc.sum() in (next_day - 1, next_day, next_day + 1)

# fatigue: invented decay. B's CTR falls 3% (relative) per day of exposure to the same users
days = np.arange(0, 15)
ctr_B = 0.025 * 0.97 ** days
cross = int(np.argmax(ctr_B < 0.020))
print("B with 3%/day fatigue (invented), day 0 / 7 / 14:", ctr_B[[0, 7, 14]].round(4))
print("B drops below A's 2.0% on day", cross)
assert cross == 8 and ctr_B[7] > 0.020
```

**Output (my run):**
```text
rates: {'A': 0.02, 'B': 0.025, 'C': 0.023}
SE of B's own rate (points): 0.349
B - A: diff 0.50 pts, SE 0.469 pts, z 1.07, 95% CI [-0.42, 1.42] pts
B - C: diff 0.20 pts, SE 0.484 pts, z 0.41, 95% CI [-0.75, 1.15] pts
P(best) A, B, C: [0.083 0.61  0.308]
next-day split of 30,000 impressions: {'A': 2480, 'B': 18289, 'C': 9231}
B with 3%/day fatigue (invented), day 0 / 7 / 14: [0.025  0.0202 0.0163]
B drops below A's 2.0% on day 8
```

The 3% per day fatigue rate is invented, only to show the mechanics.

**Follow-ups:**
- Why not a classic A/B/C test? It is fine if you can afford to wait; a bandit lowers the cost of showing weaker creatives while learning.
- What if rates are very low? The normal approximation is poor; use the Beta posterior directly, as above.

**Common mistakes:** Using one creative's standard error to judge a difference. Picking the top rate after one day. Forgetting multiple comparisons across three creatives. Ignoring fatigue and day-of-week effects.

### Q46 ⭐ 🟡 Fintech: For thin-file applicants, adding a phone-usage feature set lifts AUC from 0.66 to 0.71 (0.05 absolute, measured among the 70% of applicants who have the features, on a back-test of matured loans that covers approved applicants only) and the features exist for 70% of applicants. Explain what you would check for stability, gaming, proxy risk for protected traits and consent, what the lender should ask compliance, and how you would roll the features out.
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The 0.05 AUC lift (0.66 to 0.71) is a back-test number on matured loans for the 70% of applicants who have the features, so the lift across all thin-file applicants is smaller (about 0.03 in my simulation); before rollout I would test stability and gaming, ask compliance about proxy risk and consent, and ship in stages with monitoring.

**Clarifying questions:**
- The 0.05 is measured among the 70% with features only, so the overall lift across all thin-file applicants is diluted by the 30% who have nothing new. What does the lender want quoted?
- Who are the 70% (who granted permission, who owns an app-capable phone)? Coverage that depends on consent or device is itself a selected group.
- The back-test covers approved applicants only (as the prompt says). How would we learn about rejected applicants who were never observed?
- What exactly are the phone-usage features (call patterns, app lists, recharge behaviour)? That decides the proxy and gaming risk.
- Does the model make decisions or only support a manual underwriter? It changes how strict the explainability need is; ask compliance.

**Approach:**
1. Pin down the lift: compute AUC old versus new on the covered group, on the uncovered group, and overall. Quote the overall number to the business.
2. Stability: split the back-test by vintage (month of application), device type and region; check the lift in each and calculate the feature drift (PSI) month to month. A lift that exists in one vintage only is a warning.
3. Gaming: ask which features an applicant can change cheaply (install apps, top up before applying). Test sensitivity by changing the feature in a copy of the data and watching the score; prefer slow-moving aggregates over single-day values.
4. Proxy risk: check whether the features track protected traits (gender, religion, region, caste, age) directly or through a correlated pattern. Measure score and approval gaps by group where the lender is allowed to hold that data, and ask the compliance and legal teams what is permitted. Do not state rules as facts.
5. Consent: confirm with compliance and the privacy team what applicants agreed to, how long data can be stored, and how withdrawal is handled. The 70% may shrink if consent is withdrawn.
6. Rollout: shadow scoring first, then a small live slice with a champion-challenger split, a cap on exposure, and checkpoints on early default signals, approval rate by group and coverage.

**Metrics:**
- AUC = probability a random defaulter scores higher than a random non-defaulter, reported for covered, uncovered and all applicants with intervals.
- Calibration: predicted versus observed default by decile, per vintage.
- PSI per feature, month to month (a common rule of thumb flags values above 0.1 for review, an editor-knowledge convention, not a standard).
- Approval-rate and default-rate gaps by group (where measurable and allowed).
- Guardrails: share of applicants scored by the new features, early delinquency in the live slice.

**Risks:**
- Selection: matured loans exclude rejected applicants, so the back-test overstates or misstates the lift on the real applicant pool.
- Gaming and concept drift: behaviour changes once people know the features matter.
- Proxy discrimination hiding behind a neutral-looking feature.
- Consent and data-retention problems that remove the features later.
- Inconsistent treatment: applicants without the features are scored by the old model, so two similar people can get different outcomes.

**What the interviewer scores:**
- Strong: notices the 0.05 is not the overall lift, flags selection bias in matured loans, and gives a staged rollout with monitoring.
- Strong: asks compliance rather than asserting what is legal.
- Weak: "AUC went up 0.05, ship it".
- Weak: reasons only about model accuracy, nothing on consent, gaming or proxies.

**Example:** (illustrative simulation) With a 70% coverage and 10% default rate, a lift from 0.66 to 0.71 on covered applicants becomes 0.664 to 0.698 overall, a lift of 0.034.
- Weak: "The new features lift AUC by 0.05, so we should use them."
- Strong: "The 0.05 is for applicants who have the features. Across all thin-file applicants it is nearer 0.03, and it was measured only on loans we approved. I would check it by vintage, test how easily it can be gamed, ask compliance about proxies and consent, and start with a shadow run and a small champion-challenger slice."

**Code:**
```python
# Q46: where does a 0.05 AUC lift apply when features exist for 70%? Synthetic (binormal scores, invented).
import numpy as np
from scipy.stats import norm, rankdata
rng = np.random.default_rng(3)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
sep = lambda a: np.sqrt(2) * norm.ppf(a)        # binormal separation for a target AUC, unit variances
d0, d1 = sep(0.66), sep(0.71)
n, bad_rate, cover = 400_000, 0.10, 0.70
y = (rng.random(n) < bad_rate).astype(int)
has = rng.random(n) < cover
base = d0 * y + rng.normal(size=n)
new = np.where(has, d1 * y + rng.normal(size=n), base)       # uncovered applicants keep the old score
print("AUC base overall      :", round(auc(y, base), 3))
print("AUC new, covered only :", round(auc(y[has], new[has]), 3), " (base on same group:", round(auc(y[has], base[has]), 3), ")")
print("AUC new, overall      :", round(auc(y, new), 3))
lift_overall = auc(y, new) - auc(y, base)
print("overall lift:", round(lift_overall, 3), "vs 0.05 on the covered group")
assert abs(auc(y[has], new[has]) - 0.71) < 0.01 and abs(auc(y, base) - 0.66) < 0.01
assert 0.015 < lift_overall < 0.045      # diluted: well under 0.05

# stability: population stability index of one feature between build month and a later month (invented shift)
def psi(a, b, bins=10):
    edges = np.quantile(a, np.linspace(0, 1, bins + 1)); edges[0], edges[-1] = -np.inf, np.inf
    pa = np.histogram(a, edges)[0] / len(a); pb = np.histogram(b, edges)[0] / len(b)
    pa, pb = np.clip(pa, 1e-6, None), np.clip(pb, 1e-6, None)
    return float(((pb - pa) * np.log(pb / pa)).sum())
f0 = rng.normal(0, 1, 50_000); f_same = rng.normal(0, 1, 50_000); f_shift = rng.normal(0.4, 1.2, 50_000)
print("PSI same:", round(psi(f0, f_same), 4), " PSI shifted:", round(psi(f0, f_shift), 3))
assert psi(f0, f_same) < 0.01 and psi(f0, f_shift) > 0.1
```

**Output (my run):**
```text
AUC base overall      : 0.664
AUC new, covered only : 0.712  (base on same group: 0.664 )
AUC new, overall      : 0.698
overall lift: 0.034 vs 0.05 on the covered group
PSI same: 0.0001  PSI shifted: 0.159
```

This is a binormal simulation with invented parameters; the exact diluted lift depends on how scores are combined, so treat 0.034 as one illustration, not a rule.

**Follow-ups:**
- How do you handle the rejected applicants? Reject inference is contested; a safer route is a small random-approval or champion-challenger slice, if the business accepts the cost; ask risk and compliance.
- What if the lift disappears in the newest vintage? Pause the rollout and investigate drift or gaming before widening.

**Common mistakes:** Quoting the covered-group lift as the overall lift. Back-testing only on approved loans without saying so. Ignoring gaming. Treating compliance questions as the modeller's to answer.

### Q47 ⭐ 🔴 Fintech: A fraud model's flagged transactions have a chargeback 50% of the time (500 of 1,000 flagged, measured), but an audit finds 30% of chargebacks are friendly fraud, where the genuine cardholder disputes a purchase they made. Compute the minimum share of flagged transactions that are true fraud (treating the 500 flags without a chargeback as not fraud) if the 30% applies to the 500 flagged chargebacks, and explain how label noise from chargebacks affects training, evaluation and customer treatment.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to chargeback labels and friendly fraud in payments material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** If 30% of the 500 chargebacks are friendly fraud, then 350 of the 1,000 flagged transactions are true fraud, a 35% minimum share (treating the 500 no-chargeback flags as not fraud), not the 50% the chargeback rate suggests, and it is only a floor because the 500 flagged transactions with no chargeback are unobserved, not known to be clean.

**Clarifying questions:**
- Were flagged transactions blocked or only reviewed? A blocked transaction cannot produce a chargeback, so the labels for blocked cases do not exist; this is a selective-label problem.
- Was the 30% audit rate measured on a random sample of the 500 or on a convenient subset? It is only as good as that sample, and it has an error bar.
- How long after the transaction do chargebacks arrive (label delay)? Recent flagged transactions look cleaner than they are.
- What does friendly fraud cost the merchant? It is a real loss even though the cardholder is not a criminal; treatment differs, the loss does not.
- Which team owns customer treatment (declines, account closure)? Treating a genuine customer as a fraudster has a cost of its own.

**Approach:**
1. Do the arithmetic: 500 x 0.30 = 150 friendly fraud, 350 true-fraud chargebacks, 500 with no chargeback. True fraud share of flagged = 350 / 1,000 = 35%, assuming the 500 no-chargeback flags had none (the minimum). If some of them were undisputed fraud, the share is higher (40% at 10%, up to 85% at the extreme).
2. Separate three labels in the data: confirmed true fraud (investigated or card-present evidence), friendly fraud (customer made the purchase), and unknown. Do not collapse them into one "chargeback = fraud" label.
3. Training: noisy positive labels teach the model to flag customers who dispute often, not only criminals. Use cleaner labels where possible (investigation outcomes, device and delivery evidence), down-weight uncertain labels, and consider a separate friendly-fraud model.
4. Evaluation: report precision against the cleaned labels, with the range for the unobserved part. Evaluate on a delayed, matured window. Keep a random holdout of unblocked or lightly reviewed transactions to learn the real rate, if the business accepts the cost.
5. Customer treatment: a friendly-fraud flag should lead to a different action (evidence collection, dispute representation) than a stolen-card flag (block, call the cardholder). Ask the policy and legal teams before closing accounts based on a dispute pattern.

**Metrics:**
- Measured precision = flagged with chargeback / flagged = 500 / 1,000 = 50%.
- True-fraud share = (chargebacks that are genuine fraud) / flagged = 350 / 1,000 = 35% at the minimum.
- Friendly-fraud share of flagged = 150 / 1,000 = 15%.
- Guardrails: false-decline rate of genuine customers, label delay, share of flags that were blocked (so unlabeled).

**Risks:**
- The 35% is a floor under a strong assumption; the true figure is not identified without a sample of the no-chargeback flags.
- Selective labels: the model only learns from transactions it let through or that were disputed.
- Friendly-fraud customers are real customers; harsh treatment may lose good business.
- Chargeback reason codes and the audit process change over time, so the 30% will drift.

**What the interviewer scores:**
- Strong: gets 350 and 35%, says it is a floor, and splits labels into true fraud, friendly fraud and unknown.
- Strong: gives different customer treatments for friendly versus true fraud, and asks the policy team.
- Weak: "precision is 50%".
- Weak: treats chargeback as ground truth for training and evaluation.

**Example:** (illustrative) 1,000 flagged: 350 true-fraud chargebacks, 150 friendly-fraud chargebacks, 500 no chargeback.
- Weak: "Half of what we flag is fraud, so the model is good."
- Strong: "Half are disputed, but 150 of those are friendly fraud, so true fraud is 350, 35%, at minimum. The other 500 are unknown, not clean. I would label friendly fraud separately, evaluate on a matured window with a random sample for the unknown part, and treat the two groups differently."

**Code:**
```python
# Q47: chargebacks as noisy fraud labels (prompt numbers, illustrative)
flagged, chargebacks, friendly = 1_000, 500, 0.30
assert chargebacks / flagged == 0.5
friendly_n = round(chargebacks * friendly)
true_fraud_cb = chargebacks - friendly_n
no_cb = flagged - chargebacks
print("flagged:", flagged, "= true-fraud chargebacks", true_fraud_cb, "+ friendly-fraud chargebacks", friendly_n, "+ no chargeback", no_cb)
assert (true_fraud_cb, friendly_n, no_cb) == (350, 150, 500)
print("measured precision (chargeback rate):", chargebacks / flagged)
print("true-fraud share of flagged (30% applies to the 500):", true_fraud_cb / flagged)
assert true_fraud_cb / flagged == 0.35
# the 500 flagged with no chargeback are unobserved: some could be real fraud nobody disputed
lo = true_fraud_cb / flagged
for share_undisputed_fraud in (0.0, 0.1, 0.5, 1.0):
    p = (true_fraud_cb + share_undisputed_fraud * no_cb) / flagged
    print(f"if {share_undisputed_fraud:.0%} of the no-chargeback flags were real fraud -> true-fraud share {p:.0%}")
assert (true_fraud_cb + 1.0 * no_cb) / flagged == 0.85
print("so the true-fraud share is 35% at the minimum under this reading, up to 85% at the extreme; it is not pinned down")
# friendly fraud in the flagged set is 15% of flagged: treating them as 'fraud' customers
print("friendly-fraud customers as share of flagged:", friendly_n / flagged)
assert friendly_n / flagged == 0.15

# chargebacks count friendly disputes as fraud, so the measured precision overstates the true-fraud share by:
print("measured minus true precision (points):", round((chargebacks / flagged - true_fraud_cb / flagged) * 100))
assert round((chargebacks / flagged - true_fraud_cb / flagged) * 100) == 15
```

**Output (my run):**
```text
flagged: 1000 = true-fraud chargebacks 350 + friendly-fraud chargebacks 150 + no chargeback 500
measured precision (chargeback rate): 0.5
true-fraud share of flagged (30% applies to the 500): 0.35
if 0% of the no-chargeback flags were real fraud -> true-fraud share 35%
if 10% of the no-chargeback flags were real fraud -> true-fraud share 40%
if 50% of the no-chargeback flags were real fraud -> true-fraud share 60%
if 100% of the no-chargeback flags were real fraud -> true-fraud share 85%
so the true-fraud share is 35% at the minimum under this reading, up to 85% at the extreme; it is not pinned down
friendly-fraud customers as share of flagged: 0.15
measured minus true precision (points): 15
```

**Follow-ups:**
- Does label noise always hurt? Random noise lowers accuracy but often leaves the ranking usable; systematic noise (friendly fraud correlates with certain customers) biases the model.
- How do you get cleaner labels cheaply? Sample and investigate a fixed number of disputes per week, and use delivery, device and login evidence.

**Common mistakes:** Quoting the chargeback rate as precision. Treating the 500 non-chargebacks as non-fraud. Using one label for training and for customer action. Forgetting label delay.

### Q48 ⭐ 🔴 E-commerce: 20,000 of 2,000,000 customers (1%) are flagged as serial returners and account for 48,000 of 400,000 returns (12% of returns), while a review of 200 flagged customers found 150 (75%, a sample) were abusing the policy and 50 were legitimate heavy buyers. Estimate the abusers among the 20,000 as a projection, and discuss how to act, how to evaluate it without being unfair to the other 25%, and what you would ask the policy and legal teams.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to return abuse and marketplace trust in e-commerce material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** If the reviewed 200 were a random sample, 75% abusing projects to about 15,000 abusers and 5,000 legitimate heavy buyers among the 20,000 flagged (a projection, with a 95% range of roughly 13,700 to 16,100 abusers), so I would act with graded friction, not bans, and measure harm to the 25% explicitly.

**Clarifying questions:**
- How were the 200 chosen: random from the 20,000, or the highest-scored? Only a random sample supports a projection; a top-scored sample overstates the abuse rate.
- Who judged "abusing" and by what written criteria? The 75% is a reviewer's call, so I want the rule and a second reviewer on a subset.
- What is a return worth: refund cost, shipping, restocking, resale loss? Without it I cannot price an action.
- What actions are on the table (extra checks, shorter windows, restocking fee, refusing returns, account limits)? Each has a different harm if it lands on a legitimate buyer.
- Do the flagged customers also spend a lot? A heavy buyer with high return rates can still be profitable.

**Approach:**
1. Size it: flagged are 1% of customers and 12% of returns; 2.4 returns per flagged customer against 0.18 for others, 13.5 times as many.
2. Project with an interval: 150 of 200 is 75%; the 95% Wilson interval is about 68.6% to 80.5%. On 20,000 that is 15,000 abusers (13,700 to 16,100) and 5,000 legitimate (3,900 to 6,300). Say it is a projection from a sample, not a count.
3. Estimate what is not in the picture: abusers who are not flagged (recall). The sample says nothing about them.
4. Act proportionally: start with low-harm steps for everyone flagged (a note on policy, a return-reason prompt, a check on item condition), and keep stronger steps (restocking fee, account limit) for those with repeated, evidence-based abuse.
5. Evaluate fairly: run a randomised holdout inside the flagged group (some get the action, some do not). Measure return cost, abuse rate, but also customer churn, complaints, orders and GMV for the legitimate heavy buyers. Report outcomes for the legitimate 25% separately.
6. Give an appeal route and review the rule on a schedule.

**Metrics:**
- Abuse share (sample) = confirmed abusers in the reviewed sample / reviewed = 150 / 200 = 75%.
- Projected abusers = abuse share x flagged customers = 0.75 x 20,000 = 15,000.
- Harm rate = legitimate customers who received a restrictive action / legitimate customers flagged.
- Net value per flagged customer = P(abuser) x saving per correct action - P(legitimate) x cost per wrong action.
- Guardrails: repeat purchase rate, complaints, GMV of flagged legitimate buyers.

**Risks:**
- Bias in the sample (non-random 200) or in the reviewers' criteria.
- Disproportionate impact on customer groups (for example, by region or by category such as clothing where returns are normal); check the flag by group and ask the policy and legal teams.
- A one-size action lands on 5,000 loyal customers.
- Abusers adapt (new accounts), so the flag decays.

**What the interviewer scores:**
- Strong: labels 15,000 as a projection with an interval, and gives a break-even abuse share for each action.
- Strong: proposes graded actions, a randomised evaluation and harm tracking for the 25%.
- Strong: leaves what is permitted and what the policy should say to policy and legal teams.
- Weak: "75% are abusers, block them all."
- Weak: treats 15,000 as a measured count.

**Example:** (illustrative, invented per-customer costs) A restrictive action saves 25 per abuser and costs 40 per wrongly hit legitimate buyer. At 75% abuse the expected net is 0.75 x 25 - 0.25 x 40 = 8.75 per flagged customer. Break-even is 40 / 65 = 61.5% abusing, which the lower end of the interval (68.6%) still clears. A harsher action that costs 100 per wrong hit would need 80% abusing and would not clear it.
- Weak: "Three quarters abuse the policy, so cut them off."
- Strong: "150 of 200 is 75%, which projects to about 15,000, with a range of 13,700 to 16,100, if the 200 were random. 5,000 are loyal heavy buyers. I will start with light friction, run a holdout, track harm to the legitimate group, and check the policy and legal teams before any account-level action."

**Code:**
```python
# Q48: serial returners (prompt numbers, illustrative)
import math
cust, flagged_n, returns, flagged_ret = 2_000_000, 20_000, 400_000, 48_000
assert flagged_n / cust == 0.01 and flagged_ret / returns == 0.12
print("returns per flagged customer:", flagged_ret / flagged_n, " per other customer:", round((returns - flagged_ret) / (cust - flagged_n), 3))
assert flagged_ret / flagged_n == 2.4
print("ratio:", round((flagged_ret / flagged_n) / ((returns - flagged_ret) / (cust - flagged_n)), 1))

k, n = 150, 200
p = k / n
print("sample share abusing:", p, " legitimate:", 1 - p)
proj = p * flagged_n
print("projected abusers among 20,000:", proj, " projected legitimate heavy buyers:", flagged_n - proj)
assert proj == 15_000 and flagged_n - proj == 5_000

def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h
lo, hi = wilson(k, n)
print(f"95% Wilson interval for the share: [{lo:.3f}, {hi:.3f}] -> abusers [{lo*flagged_n:,.0f}, {hi*flagged_n:,.0f}], legitimate [{(1-hi)*flagged_n:,.0f}, {(1-lo)*flagged_n:,.0f}]")
assert 0.68 < lo < 0.70 and 0.80 < hi < 0.81
# only valid if the 200 were a random draw from the 20,000; a top-scored 200 would overstate
# action example (invented): friction (e.g. return-window check) for flagged; cost of wrongly hitting a legit heavy buyer
legit = flagged_n - proj
cost_wrong, saving_right = 40, 25      # invented per-customer figures
print("expected net per flagged customer (invented):", p * saving_right - (1 - p) * cost_wrong)
assert p * saving_right - (1 - p) * cost_wrong == 8.75
print("breakeven abusing share:", cost_wrong / (cost_wrong + saving_right))
assert round(cost_wrong / (cost_wrong + saving_right), 3) == 0.615
```

**Output (my run):**
```text
returns per flagged customer: 2.4  per other customer: 0.178
ratio: 13.5
sample share abusing: 0.75  legitimate: 0.25
projected abusers among 20,000: 15000.0  projected legitimate heavy buyers: 5000.0
95% Wilson interval for the share: [0.686, 0.805] -> abusers [13,713, 16,098], legitimate [3,902, 6,287]
expected net per flagged customer (invented): 8.75
breakeven abusing share: 0.6153846153846154
```

The 25 and 40 per-customer figures are invented to show the break-even calculation.

**Follow-ups:**
- How do you improve the flag? Use the reviewed labels to train a model on abuse versus legitimate heavy buying (return reasons, item condition, timing) rather than raw return count.
- What about the abusers you miss? Sample unflagged customers with high returns for review to estimate recall.

**Common mistakes:** Calling a sample share a population fact. Using return count alone as the signal. Taking one action for all flagged customers. Ignoring harm to legitimate buyers. Making policy or legal claims as facts.

### Q49 ⭐ 🔴 Healthcare: A deployed model's sensitivity was 0.82 on its locked test set. A retrained version shows 0.80 on the same set with 400 positives, a standard error of about 0.02 for the new sensitivity alone (the square root of 0.8 times 0.2 over 400), and the team wants to ship it because its calibration is better. The comparison is paired on the same patients: the old model caught 20 positives that the new one missed, and the new one caught 12 that the old one missed. How do you decide whether this is acceptable, what margin and evidence would you pre-specify, and what would you ask the regulatory team about classifying the change?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to model updates and change control in clinical AI, regulatory humility; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Better calibration does not pay for lost sensitivity, so I would not accept 0.80 versus 0.82 on a "looks close" basis; I would compute the paired difference (8 fewer true positives out of 400) with a pre-specified non-inferiority margin, and use the stated discordant pairs (20 and 12) for the paired standard error of 0.014, not the 0.02 for the new model alone.

**Clarifying questions:**
- What does a missed positive cost clinically, and who sets the acceptable sensitivity loss? The margin is a clinical decision, not a statistical one.
- The discordant pairs are given: the old model caught 20 positives the new one missed, the new caught 12 the old one missed. Is the test set also used for threshold tuning? The paired standard error uses these counts.
- Was the threshold chosen on this locked test set? If the set was reused for tuning, the 0.80 and 0.82 are optimistic.
- Is the comparison at the same alert rate or the same threshold? Sensitivity depends on it; a better-calibrated model may sit at a different operating point.
- Does the retrained model change anything else (inputs, intended use)? It decides how the change is classified.

**Approach:**
1. Do the arithmetic: old catches 0.82 x 400 = 328, new catches 320, difference -8, which is -2.0 points.
2. Use the paired comparison. Here b = 20 (only the old model catches) and c = 12 (only the new model catches), so c - b = -8. The paired standard error is sqrt(b + c - (c - b)^2 / 400) / 400. With the stated 32 discordant pairs it is 0.014 (CI about -4.8 to +0.8 points); with more discordance (112 pairs) it would be 0.026.
3. Pre-specify a non-inferiority margin before looking (for example, 3 points of sensitivity, set by clinicians) and the rule: ship only if the lower confidence bound of the difference is above minus the margin. With the numbers here and a 3-point margin, the lower bound is below -3 points in every scenario I tried, so non-inferiority is not shown.
4. Check at matched operating points: sensitivity at the same specificity or alert rate, plus the net benefit or decision-curve view. If calibration improved, show which decisions improve and by how much.
5. Check subgroups (sex, age bands, site) for sensitivity drops hidden in the average.
6. Plan more evidence if needed: more positives (about 550 positives for a 3-point margin at 80% power, if true sensitivities are equal and 8% of positives are discordant, illustrative) or prospective silent running.
7. Ask the regulatory and quality teams how this change is classified and what documentation and monitoring it needs. I do not assert the answer.

**Metrics:**
- Sensitivity = true positives / positives = 320 / 400 = 0.80 (new), 328 / 400 = 0.82 (old).
- Paired difference with CI, using discordant pairs b and c.
- Specificity or alert rate at the same threshold, calibration slope and intercept, subgroup sensitivity.
- Guardrails: false-alarm burden, missed-case count per 1,000 patients.

**Risks:**
- Treating overlapping individual error bars as a test (the 0.02 for one model alone invites this).
- Margin chosen after seeing the data.
- Re-using a locked set many times: it stops being locked.
- Better calibration with lower sensitivity at the chosen threshold means a different trade-off, not a free improvement.

**What the interviewer scores:**
- Strong: states the paired design, uses the stated discordant counts, computes a CI for the difference and uses a pre-set margin.
- Strong: separates calibration from sensitivity, checks matched operating points, and asks the regulatory team about classification.
- Weak: "0.80 is within one standard error of 0.82, so they are the same".
- Weak: "calibration is better, ship it".

**Example:** (the prompt's discordant counts; the 3-point margin is illustrative) The old model alone catches 20 positives and the new alone catches 12. The difference is -2.0 points, SE 1.41 points, 95% CI -4.8 to +0.8. With a 3-point margin the one-sided lower bound is about -4.3, below -3, so we cannot claim non-inferiority yet.
- Weak: "0.80 versus 0.82 is within noise; it is calibrated better, ship it."
- Strong: "That is 8 fewer true positives of 400. The 0.02 error is for one model; the comparison is paired, so I need the discordant pairs. With 20 and 12 the CI is -4.8 to +0.8 points, and against a pre-set 3-point margin I cannot show non-inferiority. I would compare at the same alert rate, look at subgroups, collect more evidence, and ask the regulatory team how the change is classified."

**Code:**
```python
# Q49: paired sensitivity comparison (prompt numbers + INVENTED discordant counts)
import math
n = 400
old_tp, new_tp = round(0.82 * n), round(0.80 * n)
print("true positives old/new:", old_tp, new_tp, " difference:", new_tp - old_tp)
assert (old_tp, new_tp) == (328, 320)
se_new_alone = math.sqrt(0.8 * 0.2 / n)
print("SE of the new sensitivity alone:", se_new_alone)
assert abs(se_new_alone - 0.02) < 1e-12
# Unpaired (wrong for a paired design): SE of difference if the two were independent
se_unpaired = math.sqrt(0.82 * 0.18 / n + 0.8 * 0.2 / n)
print("unpaired SE of difference (not appropriate):", round(se_unpaired, 4))

# Paired: c = positives only the new model catches, b = only the old model catches; c - b = -8
margin = 0.03   # illustrative non-inferiority margin, absolute sensitivity points; clinicians must set it
print("margin:", margin)
for b, c in [(12, 4), (20, 12), (40, 32), (60, 52)]:
    assert c - b == -8
    d = (c - b) / n
    se = math.sqrt(b + c - (c - b) ** 2 / n) / n          # paired SE for a difference in proportions
    lo, hi = d - 1.96 * se, d + 1.96 * se
    lo1 = d - 1.645 * se                                      # one-sided 95% lower bound for non-inferiority
    print(f"discordant b={b:2d} c={c:2d}: diff {d:+.3f} SE {se:.4f} 95% CI [{lo:+.3f}, {hi:+.3f}] one-sided lower {lo1:+.3f} non-inferior at 0.03? {lo1 > -margin}; at 0.05? {lo1 > -0.05}")
# with b=20, c=12 (invented): lower bound below -0.03 -> cannot claim non-inferiority
b, c = 20, 12
se = math.sqrt(b + c - (c - b) ** 2 / n) / n
assert (-8 / n) - 1.645 * se < -margin
# sample needed: positives for a non-inferiority test if the true difference is 0, discordant rate 8% (invented)
disc = 0.08
n_pos = ((1.645 + 0.8416) ** 2) * disc / (margin ** 2)       # one-sided alpha 0.05, 80% power, true diff 0
print("positives needed (true diff 0, discordance 8%, margin 3 pts):", math.ceil(n_pos))
assert math.ceil(n_pos) == 550
```

**Output (my run):**
```text
true positives old/new: 328 320  difference: -8
SE of the new sensitivity alone: 0.02
unpaired SE of difference (not appropriate): 0.0277
margin: 0.03
discordant b=12 c= 4: diff -0.020 SE 0.0099 95% CI [-0.040, -0.000] one-sided lower -0.036 non-inferior at 0.03? False; at 0.05? True
discordant b=20 c=12: diff -0.020 SE 0.0141 95% CI [-0.048, +0.008] one-sided lower -0.043 non-inferior at 0.03? False; at 0.05? True
discordant b=40 c=32: diff -0.020 SE 0.0212 95% CI [-0.062, +0.022] one-sided lower -0.055 non-inferior at 0.03? False; at 0.05? False
discordant b=60 c=52: diff -0.020 SE 0.0264 95% CI [-0.072, +0.032] one-sided lower -0.063 non-inferior at 0.03? False; at 0.05? False
positives needed (true diff 0, discordance 8%, margin 3 pts): 550
```

The 20 and 12 are the prompt's discordant counts; the other discordance scenarios in the code, the 8% rate and the 3- and 5-point margins are invented for illustration; the clinical team sets the real margin.

**Follow-ups:**
- Why not just use the unpaired SE? It ignores that both models score the same patients, so it is too wide here or too narrow elsewhere depending on discordance; use McNemar-type paired methods.
- What if the margin is 5 points? In two of my four scenarios the bound clears -5 points; the margin must come from the clinical side before the data are seen.

**Common mistakes:** Comparing two numbers with a single-model SE. Picking the margin after the result. Accepting a calibration gain as a substitute for sensitivity. Reusing the locked test set. Stating regulatory conclusions as facts.

### Q50 ⭐ 🔴 Ads: A privacy-preserving report gives per-campaign daily conversion counts with random noise of standard deviation 5 added to each count, independently each day. A small campaign has about 8 true conversions a day. Compute the noise as a share of the daily count and as a share of a 7-day total of 56 (the noise standard deviation grows with the square root of 7), and explain how you would still optimise bids and judge that campaign.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to noisy aggregated conversion reporting in privacy-preserving ads measurement; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The noise standard deviation of 5 is 62.5% of a typical daily count of 8, and the 7-day noise (5 x sqrt(7), about 13.2) is still 23.6% of the 56 total, so I would never bid on one campaign's daily number; I would aggregate over days, pool similar campaigns, shrink toward a group estimate and keep exploring with small, bounded bid changes.

**Clarifying questions:**
- Is the noise added by the platform for privacy, and is the noise level fixed or does it depend on how many queries we run? Ask the platform or privacy team; if each extra query costs privacy budget, repeated slicing is not free.
- Do we have any other signal that is not noised (clicks, spend, our own server-side counts)? Cleaner proxies help a lot for small campaigns.
- How fast must bids react (hourly, daily)? It sets how much data we can pool.
- Are there many similar small campaigns we can group (same product, geography)? Pooling cuts noise by about the square root of the group size.
- What is the cost of a wrong bid on a small campaign? It sets how cautious the updates should be.

**Approach:**
1. Compute the noise share: daily 5 / 8 = 62.5%; 7-day sd = 5 x sqrt(7) = 13.2, which is 13.2 / 56 = 23.6% of the total.
2. Add the other noise: true conversions themselves vary (Poisson, sd about sqrt(56) = 7.5 over 7 days), so the combined uncertainty is about 15.2, or 27% of the total.
3. Aggregate over time: noise falls with the square root of days, but it only reaches 10% of the total after about 39 days (noise alone); that is too slow for daily bidding, so time pooling alone is not enough.
4. Pool across campaigns: group similar small campaigns, estimate a shared conversion rate, and shrink each campaign's reading toward it (a hierarchical or empirical-Bayes estimate). A campaign with a total of 70 against a group mean of 56 is estimated at about 65 here (illustrative).
5. Use the spend and click side, which is not noised, to estimate conversion rate as conversions per click with a prior, and bid on expected value with uncertainty.
6. Bid with caution: small steps, exploration budget, caps on change per day, and a rule that only moves a bid when the posterior says the direction is probable (for example, over 80%).
7. Judge the campaign on a longer window and on pooled evidence; do not pause or scale it on a single week.

**Metrics:**
- Noise share = noise sd / true count: daily 5 / 8 = 62.5%; 7-day 13.2 / 56 = 23.6%.
- Posterior mean and interval for conversion rate or CPA (cost per acquisition) per campaign.
- Calibration check using any campaign with exact internal counts: reported versus true.
- Guardrails: spend variance, bid change per day, share of campaigns under a minimum evidence level.

**Risks:**
- Reacting to noise: raising or cutting bids on pure randomness (the winner's-curse effect on a small campaign).
- Negative or zero reported counts cause naive CPA calculations to break (about 8% of daily reports would be negative in my simulation).
- Over-pooling hides a campaign that really differs.
- Treating the privacy noise as a bug to be filtered out; ask the platform team what is allowed.

**What the interviewer scores:**
- Strong: gets 62.5% and 23.6%, notes the sqrt(7) scaling, and adds the Poisson variation of the true count.
- Strong: proposes pooling and shrinkage, uses less-noisy proxies, and states what evidence is needed to act.
- Weak: "average over a few days and bid on it".
- Weak: "ignore the noise, it averages out" without saying how many days.

**Example:** (illustrative) Small campaign, true mean 8 a day. Reported 7-day total 70 against a group mean of 56 with a combined sd of 15.2.
- Weak: "70 conversions, up 25%, raise the bid."
- Strong: "The 7-day noise alone is about 24% of the total, and with natural variation it is 27%. 70 is within a standard deviation of 56. My shrunk estimate is about 65, so I would make a small bid step and keep watching, and only scale when the pooled evidence is clear."

**Code:**
```python
# Q50: noisy conversion counts (prompt numbers; true-conversion Poisson variation and pooling are illustrative)
import math
import numpy as np
sd_day, mean_day = 5.0, 8
print("noise sd / daily count:", sd_day / mean_day)
assert sd_day / mean_day == 0.625
sd7 = sd_day * math.sqrt(7)
print("7-day noise sd:", round(sd7, 2), " as share of 56:", round(sd7 / 56, 4))
assert mean_day * 7 == 56 and round(sd7, 2) == 13.23 and round(sd7 / 56, 3) == 0.236

# true conversions also vary (Poisson, invented): add that variance
pois7 = math.sqrt(56)
tot = math.sqrt(56 + sd7 ** 2)
print("Poisson sd of true 7-day total:", round(pois7, 2), " combined sd with noise:", round(tot, 2), " share:", round(tot / 56, 3))
assert round(tot / 56, 3) == 0.271

# days to get noise (alone) to 10% of the total: 5*sqrt(n)/(8n) = 0.1
n_days = (sd_day / (mean_day * 0.1)) ** 2
print("days for noise alone to reach 10%:", round(n_days, 1))
assert round(n_days, 1) == 39.1

# simulate: reported 7-day totals, noise can even go negative per day
rng = np.random.default_rng(2)
true = rng.poisson(8, size=(100_000, 7))
rep = true + rng.normal(0, 5, size=true.shape)
print("share of reported daily counts that are negative:", round((rep < 0).mean(), 3))
assert 0.03 < (rep < 0).mean() < 0.10
tot_rep, tot_true = rep.sum(1), true.sum(1)
print("sd of (reported - true) 7-day total:", round((tot_rep - tot_true).std(), 2))
assert abs((tot_rep - tot_true).std() - 13.23) < 0.3

# pooling: 20 similar small campaigns (invented). Pooled daily sd of the mean across campaigns:
k = 20
print("noise sd on the average daily count across 20 campaigns, one day:", round(5 / math.sqrt(k), 2), "vs mean 8 ->", round(5 / math.sqrt(k) / 8, 3))
assert round(5 / math.sqrt(k) / 8, 3) == 0.14

# shrinkage: posterior mean for a campaign with a 7-day reported total, prior from the pool (invented prior mean 56, sd 20)
prior_mu, prior_sd = 56.0, 20.0
obs = 70.0                                   # a reported total (invented)
w = prior_sd ** 2 / (prior_sd ** 2 + tot ** 2)
post = prior_mu + w * (obs - prior_mu)
print("weight on the campaign's own reading:", round(w, 2), " shrunk estimate:", round(post, 1), "(reported", obs, ")")
assert 0.6 < w < 0.7 and 64 < post < 66
```

**Output (my run):**
```text
noise sd / daily count: 0.625
7-day noise sd: 13.23  as share of 56: 0.2362
Poisson sd of true 7-day total: 7.48  combined sd with noise: 15.2  share: 0.271
days for noise alone to reach 10%: 39.1
share of reported daily counts that are negative: 0.08
sd of (reported - true) 7-day total: 13.18
noise sd on the average daily count across 20 campaigns, one day: 1.12 vs mean 8 -> 0.14
weight on the campaign's own reading: 0.63  shrunk estimate: 64.9 (reported 70.0 )
```

The Poisson variation, the 20-campaign pool, the group prior (mean 56, sd 20) and the reported total of 70 are invented illustrations. The noise figures from the prompt (62.5%, 13.2, 23.6%) are exact arithmetic.

**Follow-ups:**
- Why not just wait 39 days? Too slow for bidding, and conversion rates drift over that time; pooling across campaigns is faster.
- How would you check the noise really has sd 5? Compare against any exact count you hold, and see the spread of reported minus true.

**Common mistakes:** Judging noise against the daily count when the decision uses a weekly total (or the other way round). Forgetting that the true count itself varies. Treating negative reported counts as valid. Acting on one campaign's week.

