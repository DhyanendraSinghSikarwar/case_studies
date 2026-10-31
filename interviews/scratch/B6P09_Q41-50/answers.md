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

### Q44 ⭐ 🟡 Healthcare: A deterioration model uses a feature 'lactate was measured' because clinicians order the test when they are worried. At hospital A the test is ordered for 60% of patients and the model's AUC is 0.85, while at hospital B it is ordered for 20% and the AUC is 0.74 (both measured). Explain why the feature transports poorly, how to treat informative missingness across sites, and what you would validate before the model runs at hospital B.
**Asked at:** Clinical-AI external-validation coverage (Fierce Healthcare, MedCity News and JAMA Internal Medicine pages on the external validation of a widely deployed sepsis model, which reported low sensitivity, a modest positive predictive value, alerts on a large share of patients and a billing-code outcome definition; a newsletter piece on local validation and tracking override patterns); published news and research, not an interview bank; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** "Lactate was measured" is a record of a clinician's worry, not of the patient, so its meaning and its frequency change with each hospital's ordering habits; I would stop treating it as a plain feature, test the model with and without it at hospital B, and not switch it on until B's own validation passes.

**Clarifying questions:**
- Are the two AUCs on comparable patients (same ward types, same outcome definition, same prediction time)? A 0.85 versus 0.74 gap mixes feature effects with case mix and prevalence, so I cannot blame the feature alone.
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

**Example:** (illustrative) Hospital A orders lactate for 60% of patients, hospital B for 20%. A model trained at A scores 0.85 at A and 0.74 at B (the prompt's numbers).
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

### Q45 ⭐ 🟡 Ads: Three creatives were each shown 2,000 times and got 40, 50 and 46 clicks, which are rates of 2.0%, 2.5% and 2.3%. The standard error of creative B's own rate is about 0.35 points (the square root of 0.025 times 0.975 over 2,000). How would you decide how to split the next day's impressions, why might you not simply pick B, and how would you handle creative fatigue?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to creative selection with bandits in ads system-design material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** B leads at 2.5% but its own standard error is about 0.35 points and the gap that matters, B minus A, has a standard error of about 0.47 points (z about 1.07), so nothing is settled; I would split traffic by the probability each creative is best (about 8%, 61%, 31%), so B gets most of tomorrow but A and C keep getting data, and I would plan for fatigue.

**Clarifying questions:**
- Is the 2,000 impressions each from the same time window and audience? Different hours or audiences make the rates not comparable.
- What is the goal metric: clicks, conversions, or value? A creative can win on clicks and lose on conversions.
- How many impressions will the next day have and how many creatives can we add? It fixes how much exploring we can afford.
- How fast do users repeat? Frequency decides fatigue.
- Is there a minimum exposure rule (brand or contract)? It limits how far we can concentrate.

**Approach:**
1. Compare the differences, not the single rates. The prompt's 0.35-point standard error is B's own; the B minus A standard error is sqrt(0.025 x 0.975 / 2000 + 0.02 x 0.98 / 2000) = 0.47 points, so the 0.5-point lead is z about 1.07, inside noise. B minus C is z about 0.41.
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

### Q46 ⭐ 🟡 Fintech: For thin-file applicants, adding a phone-usage feature set lifts AUC from 0.66 to 0.71 (0.05 absolute, measured on a back-test of matured loans) and the features exist for 70% of applicants. Explain what you would check for stability, gaming, proxy risk for protected traits and consent, what the lender should ask compliance, and how you would roll the features out.
**Asked at:** Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The 0.05 AUC lift (0.66 to 0.71) is a back-test number on matured loans for the 70% of applicants who have the features, so the lift across all thin-file applicants is smaller (about 0.03 in my simulation); before rollout I would test stability and gaming, ask compliance about proxy risk and consent, and ship in stages with monitoring.

**Clarifying questions:**
- Is the 0.05 measured on the 70% with features only, or on everyone? The overall lift is diluted by the 30% who have nothing new.
- Who are the 70% (who granted permission, who owns an app-capable phone)? Coverage that depends on consent or device is itself a selected group.
- Matured loans are only people who were approved before. How is the back-test corrected for applicants who were rejected and never observed?
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

### Q47 ⭐ 🔴 Fintech: A fraud model's flagged transactions have a chargeback 50% of the time (500 of 1,000 flagged, measured), but an audit finds 30% of chargebacks are friendly fraud, where the genuine cardholder disputes a purchase they made. Compute the share of flagged transactions that are true fraud if the 30% applies to the 500 flagged chargebacks, and explain how label noise from chargebacks affects training, evaluation and customer treatment.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to chargeback labels and friendly fraud in payments material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** If 30% of the 500 chargebacks are friendly fraud, then 350 of the 1,000 flagged transactions are true fraud, a 35% share, not the 50% the chargeback rate suggests, and that 35% is a floor because the 500 flagged transactions with no chargeback are unobserved, not known to be clean.

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

### Q49 ⭐ 🔴 Healthcare: A deployed model's sensitivity was 0.82 on its locked test set. A retrained version shows 0.80 on the same set with 400 positives, a standard error of about 0.02 for the new sensitivity alone (the square root of 0.8 times 0.2 over 400), and the team wants to ship it because its calibration is better. The comparison is paired on the same patients. How do you decide whether this is acceptable, what margin and evidence would you pre-specify, and what would you ask the regulatory team about classifying the change?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to model updates and change control in clinical AI, regulatory humility; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Better calibration does not pay for lost sensitivity, so I would not accept 0.80 versus 0.82 on a "looks close" basis; I would compute the paired difference (8 fewer true positives out of 400) with a pre-specified non-inferiority margin, and note that the 0.02 standard error in the prompt is for the new model alone, not for the paired difference.

**Clarifying questions:**
- What does a missed positive cost clinically, and who sets the acceptable sensitivity loss? The margin is a clinical decision, not a statistical one.
- How many patients does the new model catch that the old one missed, and vice versa (the discordant pairs)? The paired standard error depends on them, and the prompt does not give them.
- Was the threshold chosen on this locked test set? If the set was reused for tuning, the 0.80 and 0.82 are optimistic.
- Is the comparison at the same alert rate or the same threshold? Sensitivity depends on it; a better-calibrated model may sit at a different operating point.
- Does the retrained model change anything else (inputs, intended use)? It decides how the change is classified.

**Approach:**
1. Do the arithmetic: old catches 0.82 x 400 = 328, new catches 320, difference -8, which is -2.0 points.
2. Use the paired comparison. Let b be positives only the old model catches and c positives only the new model catches, with c - b = -8. The paired standard error is sqrt(b + c - (c - b)^2 / 400) / 400. It depends on b + c: with 32 discordant pairs it is 0.014 (the CI for the difference is about -4.8 to +0.8 points); with 112 it is 0.026.
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
- Treating overlapping individual error bars as a test (the prompt's 0.02 alone invites this).
- Margin chosen after seeing the data.
- Re-using a locked set many times: it stops being locked.
- Better calibration with lower sensitivity at the chosen threshold means a different trade-off, not a free improvement.

**What the interviewer scores:**
- Strong: states the paired design, asks for discordant counts, computes a CI for the difference and uses a pre-set margin.
- Strong: separates calibration from sensitivity, checks matched operating points, and asks the regulatory team about classification.
- Weak: "0.80 is within one standard error of 0.82, so they are the same".
- Weak: "calibration is better, ship it".

**Example:** (illustrative; discordant counts invented, c - b = -8 as the prompt requires) Suppose the old model alone catches 20 positives and the new alone catches 12. The difference is -2.0 points, SE 1.41 points, 95% CI -4.8 to +0.8. With a 3-point margin the one-sided lower bound is about -4.3, below -3, so we cannot claim non-inferiority yet.
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

The discordant counts and the 3- and 5-point margins are invented for illustration; the clinical team sets the real margin.

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

