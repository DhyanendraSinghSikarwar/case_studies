### Q11 ⭐⭐⭐ 🟡 In a payments table, 0.2% of rows have an amount above 1,000,000 rupees while the median amount is 800 rupees. Some of these are genuine corporate payments and some are entry errors with extra zeros. Explain how you would tell outliers from errors, what you would do with each group and whether you would clip, drop or keep them.
**Asked at:** Data-cleaning question banks (an Educative data-science interview data-cleaning lesson, a TechPrep '82 Data Cleaning Interview Questions' page, StrataScratch 'data cleaning traps', a DataCamp cleaning checklist) covering outliers versus errors and unit mismatches; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I do not treat "big" as "wrong": I test each large amount against independent evidence (the customer's own history, the settlement ledger, the merchant type), fix or flag the ones that fail, and keep the genuine ones as real data with a flag, because clipping would erase the very corporate payments the business cares about.

**Clarifying questions:**
- Is there a second source of the amount (bank settlement ledger, invoice, card network record)? Why: an independent amount is the cleanest way to prove an entry error.
- Who makes these payments: retail users, corporates, or both, and do corporates have a customer type flag? Why: a 12 lakh payment is normal for one segment and absurd for another.
- What is the model or report for (fraud scoring, spend forecasting, a revenue number)? Why: the cost of keeping or dropping a row depends on the use.
- Does entry validation exist at the source (maximum per channel, confirmation screen)? Why: it decides whether this is a fix-once problem or a recurring one.
- How many rows are in question (here 0.2%, about 200 per 100,000) and can a person review them? Why: a few hundred rows can go to a review queue; a million cannot.

**Approach:**
1. Say what the numbers mean: median 800 rupees and 0.2% of rows above 1,000,000 means the tail is about 1,250 times the median. That alone proves nothing. A genuine corporate payment and an extra-zero typo both sit there.
2. Look for independent evidence per row, in this order: (a) ledger or settled amount disagrees with the recorded amount, (b) amount divided by the customer's own largest earlier payment (a retail customer who always paid under 20,000 and now "pays" 3,000,000 is suspicious, a corporate with earlier 4,000,000 payments is not), (c) the amount is 10, 100 or 1,000 times a plausible price for that merchant or item, (d) channel limits (a UPI-style limit would make some values impossible, check the current limit with the owner).
3. Put each large row in one of three groups: error (evidence says so), genuine (history fits), unknown (no history, no ledger). Unknown goes to a short review queue.
4. Treat each group differently. Errors: repair if the true value is recoverable (ledger value), otherwise set to missing and flag. Genuine: keep unchanged, add an `is_large_corporate` style flag so a model or report can handle them on purpose. Unknown: hold out of training until reviewed; do not guess.
5. Only after that choose a statistical treatment for what is left. For a mean-based report use the repaired data, for a linear model use a log transform or a robust loss, for trees leave the rows alone. Clip (winsorise) only as a documented modelling choice, never as a substitute for finding the errors.
6. Fix the source: add a validation rule (a confirmation step above a limit) and a monthly count of extreme values per channel.

**Metrics:**
- Error rate among large rows = rows confirmed as entry errors / rows above 1,000,000. Here 120 / 200 in the simulation below.
- Auto-rule precision = correctly auto-flagged errors / all auto-flagged rows. Recall = auto-flagged errors / all errors.
- Review-queue size = rows with no evidence either way. Keep it small enough for a person to clear.
- Effect on the headline number: mean amount before and after repair.
- Guardrail: genuine large payments must not be altered (count of genuine rows changed should be 0).

**Risks:**
- Clipping all rows above a percentile changes genuine corporate payments to a fake smaller value, and the corporate segment looks smaller than it is.
- Dropping all large rows biases the sample against corporates, so the model never learns that segment.
- An automatic rule that uses the same field that has the error (for example the amount itself) is circular.
- "Extra zeros" errors can also land below any threshold (a typed 8,000 instead of 800), so a big-value filter finds only some errors. Check the ratio to history at all sizes.
- Fixing values by dividing by 1,000 without proof makes up data. Use the ledger value or set to missing.

**What the interviewer scores:**
- Strong: separates "outlier" (real but extreme) from "error" (recorded wrong) and asks for independent evidence per row.
- Strong: three groups (error, genuine, unknown) with a different action for each, and a review queue instead of a guess.
- Strong: says clip, drop or keep is a modelling decision made after the errors are removed, and names the cost of each.
- Weak: "remove anything beyond 3 standard deviations" or "clip at the 99th percentile" with no check against evidence.
- Weak: no plan to fix the source of the errors.
- Cross-reference: Book 1 Part 2 covers the theory in "How do outliers affect linear regression and what robust options exist (winsorizing, Huber, quantile regression)?". This question is about proving which rows are errors first.

**Example:** (illustrative numbers) 100,000 rows, 200 above 1,000,000. Of these, 80 are genuine corporate payments (customers with earlier payments of 1 to 6 million) and 120 are retail customers whose amount is a real amount times 1,000 (the ledger shows the right figure). Evidence rule: ledger mismatch, or amount at least 100 times the customer's earlier maximum, so 120 rows are auto-flagged as errors and all 120 are real errors; 70 genuine rows pass the history check; 10 genuine first-time corporate rows have no history, so they go to review. Effect on the mean amount: 7,587 before repair, 3,900 after, almost double. Clipping at the 99.9th percentile (2,971,627) leaves a mean of 6,349 (still inflated, because the errors stay in the data, only some of them capped) and truncates the largest genuine payment from 7,034,373 to 2,971,627. Weak answer: "clip at the 99.9th percentile." Strong answer: "I prove the errors first with the ledger and customer history, fix those, keep the genuine large payments with a flag, and only then decide on a transform."

**Code:**
```python
# Q11: outliers vs entry errors in a payments table (illustrative numbers)
import numpy as np
rng = np.random.default_rng(11)
N = 100_000
# 99,800 ordinary retail rows, median about 800 rupees
retail = rng.lognormal(np.log(800), 1.0, 99_800)
# 80 genuine corporate payments (customers with a history of large payments)
corp_prior_max = rng.uniform(1.0e6, 6.0e6, 80)
corp_amt = corp_prior_max * rng.uniform(0.5, 1.5, 80)
corp_amt = np.maximum(corp_amt, 1.05e6)
# 120 entry errors: a retail amount typed with three extra zeros
true_small = rng.uniform(1_100, 5_000, 120)
err_amt = true_small * 1000
err_prior_max = rng.uniform(2_000, 20_000, 120)       # retail customers' own history
# the 10 corporate rows below are first-time large payers: no history to compare with
new_big = rng.choice(80, 10, replace=False)
corp_prior_max[new_big] = 0

amount = np.concatenate([retail, corp_amt, err_amt])
prior_max = np.concatenate([np.full(99_800, 5_000.0), corp_prior_max, err_prior_max])
is_error = np.concatenate([np.zeros(99_800 + 80, bool), np.ones(120, bool)])
settled = np.where(is_error & (np.arange(N) >= 99_880), amount / 1000, amount)  # bank ledger amount

big = amount > 1_000_000
print("rows > 1,000,000:", big.sum(), "share:", f"{big.mean():.3%}", " median:", round(float(np.median(amount))))
assert big.sum() == 200 and abs(np.median(amount) - 800) < 20

# Evidence 1: ledger mismatch.  Evidence 2: amount versus the customer's own largest earlier payment.
mismatch = big & (np.abs(settled - amount) / amount > 0.5)
ratio = np.where(prior_max > 0, amount / np.maximum(prior_max, 1), np.inf)
history_ok = big & (ratio <= 3)                      # in line with own history
auto_error = mismatch | (big & (prior_max > 0) & (ratio >= 100))       # far above own history, or ledger disagrees
review = big & ~auto_error & (prior_max == 0)        # no history and no mismatch: a human looks
keep = big & ~auto_error & ~review
print(f"auto-error {auto_error.sum()}  keep {keep.sum()}  review queue {review.sum()}")
tp = (auto_error & is_error).sum(); fp = (auto_error & ~is_error).sum()
print(f"auto-error rule: caught {tp} of {is_error.sum()} errors, wrongly flagged {fp} genuine")
assert auto_error.sum() == 120 and tp == 120 and fp == 0 and review.sum() == 10 and keep.sum() == 70

# Repair the errors: divide by 1000 (the ledger value) and keep a flag column
fixed = np.where(auto_error, settled, amount)
def mean_log(a): return float(np.mean(np.log1p(a)))
cap = np.quantile(amount, 0.999)
clipped = np.minimum(amount, cap)
print(f"mean amount: raw {amount.mean():,.0f}  fixed {fixed.mean():,.0f}  clipped at p99.9 ({cap:,.0f}) {clipped.mean():,.0f}")
print(f"genuine corporate rows after clip: largest {clipped[~is_error & big].max():,.0f} vs real {amount[~is_error & big].max():,.0f}")
assert 1.9 < amount.mean() / fixed.mean() < 2.0
assert clipped[~is_error & big].max() < amount[~is_error & big].max()
print("log-scale mean: raw", round(mean_log(amount), 3), "fixed", round(mean_log(fixed), 3))
```

**Output (my run):**
```text
rows > 1,000,000: 200 share: 0.200%  median: 801
auto-error 120  keep 70  review queue 10
auto-error rule: caught 120 of 120 errors, wrongly flagged 0 genuine
mean amount: raw 7,587  fixed 3,900  clipped at p99.9 (2,971,627) 6,349
genuine corporate rows after clip: largest 2,971,627 vs real 7,034,373
log-scale mean: raw 6.703 fixed 6.695
```

**Follow-ups:**
- Evidence is missing for most rows, what then? Use the ratio to the customer's own history and merchant norms to score "likely error", send the top of the list to review, and use a robust method (log scale, Huber loss, trees) for the rest. Say clearly that this is a risk judgement, not proof.
- Would you ever clip? Yes, as a model-side step after cleaning, for a method that is sensitive to extremes (a linear model on raw amounts), documented and tested by comparing validation error with and without it.

**Common mistakes:** Using a standard-deviation or percentile rule as proof of error. Treating all extreme rows the same way. Dropping rows silently. Fixing values by guessing the number of zeros. Cleaning once and not fixing the source.

### Q12 ⭐⭐⭐ 🟡 A new partner feed covers 90,000 of 500,000 rows (18%) and reports distance in miles while the rest of the table is in kilometres, and nobody noticed until the delivery-time model's error rose. Explain how you would find the affected rows, how you would repair the data and the model, and which checks would catch this next time.
**Asked at:** Data-cleaning question banks (an Educative data-science interview data-cleaning lesson, a TechPrep '82 Data Cleaning Interview Questions' page, StrataScratch 'data cleaning traps', a DataCamp cleaning checklist) covering outliers versus errors and unit mismatches; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I find the affected rows by comparing the reported distance with an independent distance (coordinates) per source, convert miles to kilometres only for the proven rows, retrain on the repaired table, and add a per-source unit check so the next feed cannot slip through.

**Clarifying questions:**
- Is there a source or feed column, and when did the partner feed start? Why: if yes, the affected rows are a filter, not a guess; the start date also says which past training data is contaminated.
- Do we have coordinates (pickup and drop) or another distance that does not depend on the partner? Why: an independent measure is how I prove the unit.
- Does the partner feed also differ in other fields (weight, time zone, currency)? Why: a unit bug is rarely alone.
- Did anyone retrain on the mixed table, and is the model already live? Why: it decides between a data fix only and a retrain plus rollback.
- Can the partner confirm the unit in writing (a data contract)? Why: I fix the data on evidence, and the confirmation closes the case.

**Approach:**
1. Size it. 90,000 of 500,000 rows is 18%. Cut the model error by source and by date: if the error rise starts when the feed starts and sits in the partner rows, the unit is the first suspect.
2. Prove it with a ratio. For every row compute reported distance divided by a reference distance (straight-line from coordinates, which does not depend on the feed). Take the median per source. For kilometres the median ratio sits near some stable value (here 1.30, the road detour); for miles it sits at 0.621 times that. A ratio between sources close to 0.6214 (1 mile = 1.609344 km) is the signature.
3. Find the rows. If a feed column exists, filter on it. If not, use a row screen on the ratio plus the date the shift started, then check the screened set against the partner's id list.
4. Repair data: multiply the partner distances by 1.609344, store both `distance_raw` and `distance_km`, record the source unit as a column, and re-run the ratio check. The KS distance between partner and other distance distributions should fall to near zero.
5. Repair the model: retrain on the fixed table and compare on a holdout split by source (partner rows and other rows). Do not just compare overall error.
6. Look back: which retrains, reports and promises used the broken field? If the model is live and the error is large, roll back to the last model trained before the feed and then redeploy the retrained one.
7. Prevent: a data contract with unit names, an automated per-source unit check (median ratio against a band of 0.85 to 1.15), and a volume and distribution check on every new feed before it is joined.

**Metrics:**
- Share affected = partner rows / all rows = 90,000 / 500,000 = 18%.
- Unit ratio for a source = median(reported / reference distance) for that source, divided by the same median for trusted sources. Alert when outside 0.85 to 1.15.
- MAE (minutes) = mean of |actual minus predicted delivery time|, reported overall and by source.
- Guardrails: the kilometre rows must not change (rows modified outside the partner set = 0); the repaired distributions match (KS statistic near 0).

**Risks:**
- Converting by a filter on distance size (say, "everything below 3") also converts genuine short trips.
- Partner feeds can change units later (a silent switch back), so a one-time fix is not enough.
- A global model with mixed units still looks fine overall: the other 82% of rows hide the damage. Always cut by source.
- Rounding: partner distances may be rounded to 0.1 mile (0.16 km), which loses precision; note this limit.
- Refitting before the repair would teach the model the partner's rows are "short trips that take long".

**What the interviewer scores:**
- Strong: uses an independent reference to prove the unit, not just a hunch, and slices the error by source.
- Strong: repairs data first, then model, and says what evidence shows the repair worked.
- Strong: puts the prevention at the contract and the pipeline (per-source check, unit column).
- Weak: retrain and hope, or a manual one-off conversion with no check.
- Weak: cannot say how to detect affected rows when there is no feed column.
- Cross-reference: Book 6 Part 2 has a production-side version, "An upstream team renamed a column and changed its type, and a default of 0 is now silently filled in where the model expects order_value in rupees". Here the object is the data table.

**Example:** (illustrative numbers) 500,000 rows, 90,000 from the partner (18%). In the simulation the partner median ratio reported/straight-line is 0.808 and the others' is 1.300; 0.808 / 1.300 = 0.621, which is 1 mile in km (0.6214). Partner distances after dividing by 0.621371 match the others (KS 0.311 before, 0.005 after). A line fitted for delivery minutes on the broken table has MAE 8.76 on partner rows versus 3.18 after the fix, and the overall MAE falls from 4.46 to 3.20. Weak answer: "Retrain with more data." Strong answer: "I prove the unit with the coordinate ratio, convert only the partner rows, check the two distributions match, and add a unit check per feed."

**Code:**
```python
# Q12: partner feed in miles inside a kilometre table (illustrative numbers)
import numpy as np
from scipy import stats
rng = np.random.default_rng(12)
N, NP = 500_000, 90_000
MI = 0.621371
km = rng.lognormal(np.log(5.0), 0.6, N)
partner = np.zeros(N, bool); partner[rng.choice(N, NP, replace=False)] = True
print("partner share:", f"{partner.mean():.0%}"); assert partner.sum() == NP and partner.mean() == 0.18
straight = km / rng.uniform(1.15, 1.45, N)            # straight-line distance from coordinates
reported = np.where(partner, km * MI, km)             # what the table says
minutes = 8 + 4.5 * km + rng.normal(0, 4, N)          # delivery time truth

# Step 1: find affected rows: ratio of reported distance to coordinate distance, by source
ratio = reported / straight
r_p, r_o = np.median(ratio[partner]), np.median(ratio[~partner])
print(f"median reported/straight: partner {r_p:.3f}  others {r_o:.3f}  ratio {r_p / r_o:.3f}")
assert abs(r_p / r_o - MI) < 0.01
# a row-level screen with no feed label: ratio below 0.95 flags most miles rows
flag = ratio < 1.0
print(f"row screen (ratio<1.0): catches {(flag & partner).sum() / NP:.1%} of partner rows, false alarms {(flag & ~partner).sum() / (~partner).sum():.1%} of others")

# Step 2: repair the data and verify the repair
fixed = np.where(partner, reported / MI, reported)
ks = stats.ks_2samp(fixed[partner], fixed[~partner]).statistic
ks_raw = stats.ks_2samp(reported[partner], reported[~partner]).statistic
print(f"KS partner vs others: raw {ks_raw:.3f}  after fix {ks:.3f}")
assert ks_raw > 0.3 and ks < 0.02

# Step 3: repair the model: fit a line on the broken table versus the fixed table
idx = rng.permutation(N); tr, te = idx[:400_000], idx[400_000:]
def fit(d): return np.linalg.lstsq(np.c_[np.ones(len(tr)), d[tr]], minutes[tr], rcond=None)[0]
def mae(d, w, m): return float(np.mean(np.abs(minutes[m] - (w[0] + w[1] * d[m]))))
tep = te[partner[te]]; teo = te[~partner[te]]
w_bad, w_ok = fit(reported), fit(fixed)
print(f"MAE minutes on partner rows: trained on broken {mae(reported, w_bad, tep):.2f} | fixed data {mae(fixed, w_ok, tep):.2f}")
print(f"MAE minutes on other rows:   trained on broken {mae(reported, w_bad, teo):.2f} | fixed data {mae(fixed, w_ok, teo):.2f}")
print(f"MAE overall (test):          broken {mae(reported, w_bad, te):.2f} | fixed {mae(fixed, w_ok, te):.2f}")
assert mae(fixed, w_ok, tep) < mae(reported, w_bad, tep)
print("slope per km: broken", round(w_bad[1], 2), "fixed", round(w_ok[1], 2)); assert abs(w_ok[1] - 4.5) < 0.1

# Step 4: the check that would have caught it: daily per-source median ratio against a band
def unit_check(r, src_mask, band=(0.85, 1.15), ref=None):
    m = np.median(r[src_mask]) / ref
    return round(float(m), 3), bool(not (band[0] <= m <= band[1]))
print("check partner :", unit_check(ratio, partner, ref=r_o))
print("check others  :", unit_check(ratio, ~partner, ref=r_o))
assert unit_check(ratio, partner, ref=r_o)[1] and not unit_check(ratio, ~partner, ref=r_o)[1]
```

**Output (my run):**
```text
partner share: 18%
median reported/straight: partner 0.808  others 1.300  ratio 0.621
row screen (ratio<1.0): catches 100.0% of partner rows, false alarms 0.0% of others
KS partner vs others: raw 0.311  after fix 0.005
MAE minutes on partner rows: trained on broken 8.76 | fixed data 3.18
MAE minutes on other rows:   trained on broken 3.52 | fixed data 3.20
MAE overall (test):          broken 4.46 | fixed 3.20
slope per km: broken 4.47 fixed 4.5
check partner : (0.621, True)
check others  : (1.0, False)
```

The row screen separates the sources perfectly here because the simulated detour factor is bounded between 1.15 and 1.45; real data overlaps more, so use the screen to build a candidate list, not as final proof.

**Follow-ups:**
- The partner will not confirm the unit. Use the independent ratio and a sample of trips with known real distances (a few hundred checked on a map); a consistent 0.62 ratio is strong evidence, and I would still record the assumption.
- The model must stay live while the data is fixed. Add the unit conversion in the serving feature step using the source id, so partner rows are converted at request time too, and confirm that online and offline distance distributions match.

**Common mistakes:** Judging by overall error only. Converting without a proof step. Repairing the data but not the stored features and past training sets. Ignoring serving-time conversion. No automated check afterwards.

### Q13 ⭐⭐⭐ 🔴 You trained a fraud model after keeping all 10,000 fraud rows and a random 10% of the 990,000 legitimate rows (99,000 rows, so 109,000 in all and a training fraud share of about 9.2%). A transaction gets a score of 0.50, and finance wants to use the scores as true probabilities for expected-loss calculations. Explain what the 0.50 means, how you would correct it to the 1% base rate, and how you would check the result.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A 0.50 from a model trained on a 10%-sampled legit set is a score on the sampled mix, so at the true 1% base rate it means about 9.1%, using p = 0.1 x 0.5 / (0.1 x 0.5 + 0.5); I check it with a calibration table on a full-population sample.

**Clarifying questions:**
- Was the 10% of legitimate rows a uniform random sample, and was it drawn before any other filtering? Why: the correction assumes sampling depends on the label only.
- Is the 1% base rate the current rate in the traffic the model will score (and by segment)? Why: the correction uses the true prior, and a drifting prior moves the answer.
- What will finance do with the number (expected loss, reserve, a threshold)? Why: it sets how accurate the probabilities must be.
- Do I have a recent, full-rate (not undersampled) validation set with matured labels? Why: that is the only honest place to check calibration.
- Any class weights on top of the sampling? Why: weights and sampling both shift the scores and must not be corrected twice.

**Approach:**
1. Do the arithmetic from the prompt: 10,000 fraud + 10% x 990,000 legit (that is 99,000) gives a training set of 109,000 rows and fraud is 10,000 / 109,000 = 9.17%. The true base rate is 10,000 / 1,000,000 = 1%.
2. Say what 0.50 means: on a training-like mix (9.2% fraud), a transaction with score 0.50 has equal odds of fraud and legit (odds 1.0). The sampling kept all fraud but only a tenth of legit, so legit is under-represented ten-fold.
3. Correct the odds. Sampling rate for legit beta = 0.1. Corrected odds = beta x raw odds = 0.1 x 1 = 0.1, so corrected probability = 0.1 / 1.1 = 0.0909. As a formula: p = beta p_s / (beta p_s + (1 - p_s)). Equivalent: subtract ln(1/beta) = 2.303 from the logit.
4. Check it. Score a full-rate validation sample, bin by corrected score, and compare mean predicted versus actual fraud rate per bin (a reliability table), plus the mean of corrected scores versus the base rate. If still off, fit a small calibration step (Platt or isotonic) on the full-rate validation data, never on the undersampled data.
5. Tell finance about limits: bins with few frauds are noisy, and the correction fixes the prior shift only, not a model that is bad in other ways.
6. Decide the threshold on the corrected scale (so "block above 5% fraud probability" means what it says).
7. Cross-reference: Book 1 Part 3 asks "Does class weighting, SMOTE or undersampling break probability calibration? How do you correct p...". This question applies it with checkable numbers.

**Metrics:**
- Training fraud share = fraud rows / training rows = 10,000 / 109,000 = 9.17%.
- Corrected probability p = beta p_s / (beta p_s + 1 - p_s), beta = legit sampling rate = 0.1.
- Calibration check: per band, mean corrected score and actual fraud rate (fraud rows / rows) on full-rate data; overall, mean corrected score versus base rate.
- Brier score or log-loss on the full-rate validation set, before and after correction.
- Guardrail: ranking metrics (AUC, PR-AUC) do not change with the correction because it is a monotone transform; if they change, something else is wrong.

**Risks:**
- Correcting twice (class weights and the formula) or not at all.
- Using the correction with the wrong beta (for example 0.01 instead of 0.1) turns a calibration fix into a new error.
- A tree ensemble may not be well calibrated even before sampling, so the formula alone may leave residual bias; check the table.
- The base rate shifts by segment and over time; a single prior is a simplification.
- Using the undersampled validation set to judge calibration will always look fine and tell you nothing.

**What the interviewer scores:**
- Strong: gets 109,000 and 9.17% right, explains the odds shift in one sentence, and gives 0.0909.
- Strong: validates on a full-rate sample with a reliability table instead of trusting the formula.
- Strong: knows ranking metrics do not change and that the threshold must be set on the corrected scale.
- Weak: "just use the score as it is" or "apply SMOTE-style rebalancing to fix it".
- Weak: corrects with the wrong direction (raising instead of lowering).

**Example:** (illustrative numbers) 10,000 fraud and 990,000 legit; keep all fraud and 10% of legit. Raw score 0.50 maps to 0.0909. In the simulation below (one feature, true model known, 1.005% fraud) the mean raw score on the full population is 6.309%, far above 1%, while the mean corrected score is 1.004%. For raw scores near 0.50 the corrected value is 0.090 and the actual fraud rate is 0.087. Weak answer: "A score of 0.50 means 50% fraud." Strong answer: "0.50 is the odds on the sampled mix; at the true prior the odds are ten times smaller, about 9%, and I confirm that on full-rate data."

**Code:**
```python
# Q13: undersampling and probability correction (illustrative numbers)
import numpy as np
rng = np.random.default_rng(13)
# arithmetic from the prompt
fraud, legit, beta = 10_000, 990_000, 0.10
kept = fraud + beta * legit
print(f"training rows {kept:,.0f}, training fraud share {fraud / kept:.2%}, true base rate {fraud / (fraud + legit):.2%}")
assert kept == 109_000 and round(fraud / kept, 3) == 0.092
def correct(ps, beta): return beta * ps / (beta * ps + (1 - ps))
p = correct(0.50, beta); print("score 0.50 ->", round(p, 4)); assert round(p, 4) == 0.0909
print("odds view: 0.50 is odds 1.0; times beta 0.1 gives odds 0.1; prob", round(0.1 / 1.1, 4))
# base-rate shift check: mean raw score level versus the 1% truth

# simulation: one feature, true model known, population with a 1% fraud rate
def sig(z): return 1 / (1 + np.exp(-z))
n = 1_000_000
x = rng.normal(size=n)
lo, hi = -10.0, 0.0
for _ in range(60):
    mid = (lo + hi) / 2
    if sig(mid + 2 * x).mean() > 0.01: hi = mid
    else: lo = mid
b0 = (lo + hi) / 2
y = rng.random(n) < sig(b0 + 2 * x)
print("simulated population fraud rate:", f"{y.mean():.3%}")
keep = y | (rng.random(n) < beta)
xs, ys = x[keep], y[keep].astype(float)
print("training rows:", keep.sum(), " fraud share:", f"{ys.mean():.2%}")
w = np.zeros(2); X = np.c_[np.ones(len(xs)), xs]
for _ in range(25):                                    # Newton / IRLS
    pr = sig(X @ w); g = X.T @ (ys - pr); H = (X * (pr * (1 - pr))[:, None]).T @ X
    w += np.linalg.solve(H, g)
print("fitted intercept", round(w[0], 3), " true intercept", round(b0, 3), " shift", round(w[0] - b0, 3), " ln(1/beta)=", round(np.log(1 / beta), 3))
assert abs((w[0] - b0) - np.log(1 / beta)) < 0.25 and abs(w[1] - 2) < 0.2
raw = sig(w[0] + w[1] * x); cor = correct(raw, beta)
print(f"mean score on the full population: raw {raw.mean():.3%}  corrected {cor.mean():.3%}  truth {y.mean():.3%}")
assert raw.mean() > 0.05 and abs(cor.mean() - y.mean()) < 0.0015
# calibration by raw-score band, full population
edges = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
print("band        n        raw_mean  corrected_mean  actual")
for a, b in zip(edges[:-1], edges[1:]):
    m = (raw >= a) & (raw < b + (1e-12 if b == 1 else 0))
    if m.sum() > 200:
        print(f"{a:.1f}-{b:.1f}  {m.sum():9,d}   {raw[m].mean():.3f}     {cor[m].mean():.3f}         {y[m].mean():.3f}")
m = (raw > 0.45) & (raw < 0.55)
print("raw scores near 0.50: corrected", round(cor[m].mean(), 3), " actual fraud rate", round(y[m].mean(), 3))
assert abs(cor[m].mean() - y[m].mean()) < 0.01 and abs(y[m].mean() - 0.0909) < 0.01
```

**Output (my run):**
```text
training rows 109,000, training fraud share 9.17%, true base rate 1.00%
score 0.50 -> 0.0909
odds view: 0.50 is odds 1.0; times beta 0.1 gives odds 0.1; prob 0.0909
simulated population fraud rate: 1.005%
training rows: 109316  fraud share: 9.20%
fitted intercept -4.102  true intercept -6.407  shift 2.305  ln(1/beta)= 2.303
mean score on the full population: raw 6.309%  corrected 1.004%  truth 1.005%
band        n        raw_mean  corrected_mean  actual
0.0-0.1    829,507   0.021     0.002         0.002
0.1-0.3    118,433   0.172     0.021         0.021
0.3-0.5     31,825   0.384     0.060         0.059
0.5-0.7     13,461   0.587     0.128         0.123
0.7-0.9      5,953   0.784     0.279         0.288
0.9-1.0        821   0.936     0.607         0.609
raw scores near 0.50: corrected 0.09  actual fraud rate 0.087
```

**Follow-ups:**
- What if finance wants the probability for a segment with a 3% base rate? Use that segment's prior: convert the model odds back to the training prior, then multiply by the new prior odds over the training prior odds. Check on that segment's labelled data.
- Does the correction change who gets flagged at a fixed top-k? No. It is monotone, so the ranking and any top-k list are unchanged. Only threshold-on-probability rules change.

**Common mistakes:** Reading the raw score as true probability. Applying the correction in the wrong direction. Validating calibration on undersampled data. Forgetting to set the threshold on the corrected scale. Correcting a model that also used class weights without tracking what each step did.

### Q14 ⭐⭐⭐ 🔴 A lender trained a default model only on the 60,000 approved applications from last year's 100,000, because the 40,000 rejected applicants never produced repayment outcomes. The model looks excellent on approved loans, but a new policy now lets in applicants who would previously have been rejected. Explain what bias this creates, what you would do about the rejected group, and how you would validate under the new policy.
**Asked at:** Delayed-label, positive-unlabelled and selection-bias literature (Bekker and Davis PU survey, an arXiv paper on PU survival data, an arXiv paper on PU data under selection bias); no interview page for the exact prompt, so editor-designed from the literature; search snippets only, not opened
**Say this first (1 line):** Training only on approved loans is selection bias: the model has never seen the risk of the people the old policy rejected, so under a looser policy it will underestimate their default, and I fix it with a small randomised exploration group, weighting, and a validation plan on the new band.

**Clarifying questions:**
- How were the 60,000 chosen: a score cut, officer judgement, or rules using fields the model does not see? Why: if the approval rule used only model features the bias is extrapolation; if it used hidden information, the bias is deeper.
- How wide is the new policy: a little looser or a big jump? Why: the further outside old approvals, the less the old data tells us.
- Can the business approve a small random slice of rejected applicants for learning? Why: it is the only direct way to get outcomes for them.
- Are there outcomes for rejected applicants elsewhere (credit bureau data on other loans they took)? Why: it gives a partial label without lending.
- What is the cost of a default versus a lost good customer? Why: it sets how much exploration is worth paying for.

**Approach:**
1. Name the bias: selection bias (sample selection on the outcome-related variable, also called reject inference). The training population is the approved 60,000 of 100,000; the new policy scores 40,000 people the model never saw.
2. Check overlap: compare the feature ranges of approved, rejected and new-policy applicants. Where the new band falls outside what the model trained on, predictions are extrapolation.
3. Get real labels for part of the rejected group. Best: a controlled exploration, approving a small random slice of rejected applicants within a risk budget, and recording the approval probability of each. Fallbacks: bureau performance on other loans (a proxy label), or the lender's own past policy changes.
4. Train with weights. Give each explored row a weight of 1 divided by its probability of being explored, so the sample stands for the whole rejected group, and fit on approved plus explored rows.
5. Avoid the cheap tricks as the main plan. Labelling every reject as "default" or "good" is wrong either way. Augmentation, parcelling and similar reject-inference methods use assumptions that cannot be tested from the approved data, so treat them as sensitivity analyses, not as truth.
6. Validate on the new policy. Backtest by band (approved, newly approved), compare predicted and actual default rates in the explored sample, and launch in steps (approve a small extra band first, watch matured outcomes) with a loss limit.
7. Remember delayed labels: repayment outcomes mature over months, so the first read is early-delinquency, not final default.

**Metrics:**
- Default rate by band = defaults / loans in that band, observed only for approved or explored loans.
- Calibration gap in the new band = mean predicted default minus actual default rate.
- AUC by band, not only overall (the approved-only AUC is computed on a narrow, range-restricted group and is optimistic).
- Exploration cost = expected extra losses on the explored group = explored loans x expected default rate x loss per default. Keep it inside a budget.
- Guardrails: losses per band against a limit, and approval share by band.

**Risks:**
- A model that "looks excellent" on approved loans has only been tested on the easy part of the population.
- Range restriction: AUC on a narrow group is lower than on a wide group, and calibration at the edge of the data can still be badly wrong.
- Unobserved selection: officers may have rejected people because of information not in the data (this is MNAR; no weighting can fix hidden causes).
- Exploration can cost real money and has fairness and legal questions: check with the risk and legal teams.
- Weights of 1 / p with small p are noisy; cap them or use a stabilised version.

**What the interviewer scores:**
- Strong: names selection bias and reject inference, and says the data cannot answer the question on its own.
- Strong: proposes a concrete way to get labels (exploration with recorded probabilities) and weights the results.
- Strong: validates on the new band and rolls out in steps.
- Weak: "use class weights" or "predict the rejected as defaults".
- Weak: trusts the offline AUC computed only on approved loans.

**Example:** (illustrative simulation) 100,000 applicants, the old policy approves the 60,000 lowest-risk ones and rejects 40,000. Default rate: 1.79% among approved, 20.82% among rejected. A logistic model on approved loans only predicts 4.88% for the next 25,000 applicants that the new policy would admit; the actual rate is 6.79%. In the riskiest 5,000 it predicts 22.41% when the actual is 78.84%. Approving a random 1,200 of the 40,000 rejected applicants (3%) and weighting those rows by 40,000 / 1,200 brings the prediction for the riskiest 5,000 to 76.32%, an error of 2.5 percentage points instead of 56.4. Weak answer: "AUC is 0.94 on approved loans, so launch." Strong answer: "The model has not seen these applicants; I get a small randomised sample of outcomes from the rejected group and launch in bands."

**Code:**
```python
# Q14: reject inference / selection bias (illustrative simulation)
import numpy as np
rng = np.random.default_rng(14)
def sig(z): return 1 / (1 + np.exp(-z))
def fit_logit(X, y, it=30):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (y - p))
    return w
def auc(s, y):
    from scipy.stats import rankdata
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

N = 100_000
risk = rng.normal(size=N)                  # higher = riskier applicant (bureau-style score, standardised)
true_logit = -3.6 + 0.8 * risk + 0.9 * np.maximum(risk, 0) ** 2   # risk climbs faster in the tail
default = rng.random(N) < sig(true_logit)
# old policy: approve the 60,000 lowest-risk applicants (rank cut)
order = np.argsort(risk); approved = np.zeros(N, bool); approved[order[:60_000]] = True
print("approved", approved.sum(), "rejected", (~approved).sum())
assert approved.sum() == 60_000 and (~approved).sum() == 40_000
print(f"default rate: approved {default[approved].mean():.2%}   rejected (unseen by the lender) {default[~approved].mean():.2%}")
X = np.c_[np.ones(N), risk, risk ** 2]   # a flexible-enough logit: intercept, risk, risk squared
w = fit_logit(X[approved], default[approved].astype(float))
pred = sig(X @ w)
print(f"approved-only model: AUC on approved {auc(pred[approved], default[approved].astype(int)):.3f}")
# new policy approves the next 25,000 lowest-risk applicants (ranks 60,000 to 85,000)
band = np.zeros(N, bool); band[order[60_000:85_000]] = True
print(f"new band: predicted default {pred[band].mean():.2%}  actual {default[band].mean():.2%}")
assert default[band].mean() > 1.3 * pred[band].mean()
# worst slice: the riskiest 5,000 of the rejected
tail = np.zeros(N, bool); tail[order[-5_000:]] = True
print(f"riskiest 5,000: predicted {pred[tail].mean():.2%}  actual {default[tail].mean():.2%}")
# fix 1: exploration: approve a random 3% of rejected applicants and observe them (1,200 loans)
rej_idx = np.flatnonzero(~approved)
explore = rng.choice(rej_idx, 1_200, replace=False)
print("exploration sample:", len(explore), "loans =", f"{len(explore) / 40_000:.0%} of rejected")
assert len(explore) == 1_200
# reweight the exploration rows by inverse sampling probability (1 / 0.03) and refit on approved + explored
use = np.r_[np.flatnonzero(approved), explore]
wt = np.r_[np.ones(60_000), np.full(len(explore), 40_000 / 1_200)]
w2 = np.zeros(3)
for _ in range(30):
    p = sig(X[use] @ w2); H = (X[use] * (wt * p * (1 - p))[:, None]).T @ X[use] + 1e-6 * np.eye(3)
    w2 += np.linalg.solve(H, X[use].T @ (wt * (default[use] - p)))
pred2 = sig(X @ w2)
print(f"with weighted exploration: new band predicted {pred2[band].mean():.2%}  actual {default[band].mean():.2%}; riskiest 5,000 predicted {pred2[tail].mean():.2%}")
err_old = abs(pred[tail].mean() - default[tail].mean()); err_new = abs(pred2[tail].mean() - default[tail].mean())
print(f"tail error (percentage points): approved-only {err_old * 100:.1f}  with exploration {err_new * 100:.1f}")
assert err_new < err_old
```

**Output (my run):**
```text
approved 60000 rejected 40000
default rate: approved 1.79%   rejected (unseen by the lender) 20.82%
approved-only model: AUC on approved 0.625
new band: predicted default 4.88%  actual 6.79%
riskiest 5,000: predicted 22.41%  actual 78.84%
exploration sample: 1200 loans = 3% of rejected
with weighted exploration: new band predicted 7.28%  actual 6.79%; riskiest 5,000 predicted 76.32%
tail error (percentage points): approved-only 56.4  with exploration 2.5
```

The "AUC on approved" line (0.625) is low because approved loans are a narrow, low-risk slice, not because the model is bad; that is the range-restriction risk named above. The simulated risk curve is steeper in the tail than a straight-line logit, which is what makes extrapolation fail here; real data may behave differently.

**Follow-ups:**
- Exploration is not allowed. Use bureau data on the rejected applicants' loans elsewhere as proxy labels, run sensitivity analysis under several assumptions about the rejected group's default rate, and launch only a small band with a loss cap.
- Does a simple "reject inference" method fix it? Sometimes it reduces the bias a little, but each method rests on an assumption the approved data cannot test. Use it to bound the answer, and still collect real outcomes.

**Common mistakes:** Reporting offline AUC on approved loans as the launch metric. Treating all rejects as defaults or as good. Not recording selection probabilities for exploration. Using one big launch instead of bands. Forgetting that outcomes arrive late.

### Q15 ⭐⭐⭐ 🔴 A feature's missing values were filled with the mean target value within each city, computed on the whole data set before the split, and offline AUC is 0.93 against 0.71 live. The author says imputation cannot leak because it only uses a single column. Explain the leak, how you would prove it with an experiment, and how imputation should be set up instead.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** It leaks, because the city mean of the target uses the label of the very row being filled (and of the test rows), so the filled value contains the answer; I prove it by running the same fill on pure-noise labels and by comparing against a fill computed on training rows only, and the fix is to compute the fill inside each training fold.

**Clarifying questions:**
- How many rows per city, and how many of the missing rows are in small cities? Why: the leak is strongest when a city has few rows, because each row's own label is a large share of its city mean.
- Was the fill computed before the split, on train and test together? Why: the prompt says whole data; that also puts test labels into the training features.
- Is the imputed column missing at random, or is missingness related to the target? Why: it changes what a fair fill is.
- What does the live pipeline use to fill missing values? Why: live rows have no label, so a target-based fill cannot be reproduced at serving time, which alone explains a gap.
- Are other target-based features (target encodings) built the same way? Why: the same bug often repeats across features.

**Approach:**
1. Explain the leak in one sentence: the fill for a row is the mean of y in its city, and that mean includes this row's own y; for a city of 10 rows, 10% of the filled value is the row's own label.
2. Show the second leak: computing the city means on the whole data before the split lets test labels flow into training features.
3. Prove it with a noise experiment. Make the label unrelated to every feature (or shuffle it), fill the way the author did, and measure AUC of the filled value. A feature built without leakage gets about 0.5; a leaking one scores well above that. Repeat after shuffling to be sure it does not depend on one draw.
4. Show the live gap: in production the label is unknown, so a target-based fill cannot run the same way. The model learned a pattern that does not exist live, and AUC falls from 0.93 towards 0.71.
5. Fix: split first. Fit every imputation inside the training fold only. For a target-based fill on training rows use out-of-fold means (smoothed toward the global mean, so small cities do not carry noise); for validation and test rows use the training-fold means. Prefer fills that do not use the target at all (median, a model on other features, plus a missing flag) unless the target-based one earns its place on honest validation.
6. Wrap it in a pipeline so the fill is part of the fitted model and cannot be fitted on all rows by mistake.
7. Cross-reference: Book 1 Part 2 asks "How do you do target encoding without leakage (out-of-fold, smoothing)?" and the same fix applies here.

**Metrics:**
- AUC of the filled value on rows where it was missing: leaky fill versus fill computed on training rows only (noise-label test; honest value is about 0.5).
- Own-label share = 1 / rows in the city (10 rows gives 10%).
- Gap = offline AUC minus live (or time-forward) AUC. Here 0.93 versus 0.71 is 0.22.
- Guardrail: after the fix, offline and honest holdout AUC should agree within a few points.

**Risks:**
- The author's argument "it only uses one column" misses that the column is the target's own summary.
- A noise-label test shows that a leak exists, not how big it is on real data; also run the corrected pipeline and see the real drop.
- Small cities make out-of-fold means noisy; without smoothing the honest fill can hurt.
- Other steps (scaling, selection, encoding) may leak the same way.

**What the interviewer scores:**
- Strong: states the self-inclusion leak and the train-test leak separately, and notes live rows have no label.
- Strong: a concrete proof experiment (noise or shuffled labels) with a number.
- Strong: the fix is fitted inside folds, with out-of-fold or smoothed means, in a pipeline.
- Weak: accepts "single column cannot leak", or just says "do it after the split" without explaining why.

**Example:** (illustrative simulation) 20,000 rows in 2,000 cities (about 10 per city), a label that is pure noise with a 10% rate, and a feature missing in 60% of rows. Among the 3,554 test rows where the feature was missing, the leaky filled value reaches AUC 0.790 on a label with no signal. The fill computed on training rows only gives 0.477, and the out-of-fold fill on training rows gives 0.498. After shuffling the labels five times the leaky AUC stays between 0.779 and 0.809, so it is the fill reading the label, not luck. Weak answer: "Imputation uses one column, so it is safe." Strong answer: "The filled value contains the row's own label; I show an AUC of 0.79 on noise, then fit the fill inside the folds."

**Code:**
```python
# Q15: target-mean imputation computed before the split leaks the label (illustrative simulation)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(15)
def auc(s, y):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
N, CITIES = 20_000, 2_000                   # about 10 rows per city
city = rng.integers(0, CITIES, N)
y = (rng.random(N) < 0.10).astype(int)      # label is pure noise: NO real signal in any column
missing = rng.random(N) < 0.60               # feature missing in 60% of rows
test = rng.random(N) < 0.30

def city_target_mean(idx_fit, idx_apply):
    s = np.bincount(city[idx_fit], weights=y[idx_fit], minlength=CITIES)
    c = np.bincount(city[idx_fit], minlength=CITIES)
    g = y[idx_fit].mean()
    m = np.where(c > 0, s / np.maximum(c, 1), g)
    return m[city[idx_apply]]

allrows = np.arange(N)
leaky = city_target_mean(allrows, allrows)                  # whole data, before the split
tr, te = np.flatnonzero(~test), np.flatnonzero(test)
clean = city_target_mean(tr, te)                            # train rows only
m_te = missing[te]
a_leaky = auc(leaky[te][m_te], y[te][m_te])
a_clean = auc(clean[m_te], y[te][m_te])
print(f"test rows with a filled value: {m_te.sum()}")
print(f"AUC of the filled value on a label with NO signal: leaky {a_leaky:.3f}   train-only fill {a_clean:.3f}")
assert a_leaky > 0.58 and abs(a_clean - 0.5) < 0.05
# permutation proof: shuffle the labels, redo the leaky fill; AUC stays high -> the fill is reading y
y_real = y.copy()
aucs = []
for _ in range(5):
    y[:] = rng.permutation(y_real)
    lk = city_target_mean(allrows, allrows)
    aucs.append(auc(lk[te][m_te], y[te][m_te]))
print("leaky AUC after shuffling labels (5 shuffles):", [round(float(a), 3) for a in aucs])
assert min(aucs) > 0.58
# why: a row's own label sits inside its city mean.  Own-label share = 1 / rows in city
n_city = np.bincount(city, minlength=CITIES)
print(f"median rows per city {np.median(n_city):.0f}; own label is {1 / np.median(n_city):.0%} of that city's mean")
# the right setup: fit the fill inside each training fold, with out-of-fold means for training rows
folds = rng.integers(0, 5, len(tr)); oof = np.zeros(len(tr))
for k in range(5):
    fit_idx, app_idx = tr[folds != k], tr[folds == k]
    oof[folds == k] = city_target_mean(fit_idx, app_idx)
a_oof = auc(oof[missing[tr]], y[tr][missing[tr]])
print(f"out-of-fold fill on training rows: AUC {a_oof:.3f}  (honest, close to 0.5)")
assert abs(a_oof - 0.5) < 0.05
```

**Output (my run):**
```text
test rows with a filled value: 3554
AUC of the filled value on a label with NO signal: leaky 0.790   train-only fill 0.477
leaky AUC after shuffling labels (5 shuffles): [0.792, 0.785, 0.794, 0.809, 0.779]
median rows per city 10; own label is 10% of that city's mean
out-of-fold fill on training rows: AUC 0.498  (honest, close to 0.5)
```

**Follow-ups:**
- Is target-based imputation ever fine? Yes, if it is computed out-of-fold, smoothed, and it still beats a plain median plus a missing flag on honest validation. Many teams skip it because it is hard to serve.
- How would you catch this in review? Ask of every feature: "could this be computed at prediction time with no label?" and run a shuffled-label check on the full pipeline.

**Common mistakes:** Fitting any imputer, scaler or encoder on the whole data before the split. Using target means without out-of-fold or smoothing. Trusting a suspiciously high offline AUC. Checking only the final model, not each feature.

### Q16 ⭐⭐⭐ 🔴 After a vendor outage, a model feature that was missing in 5% of training rows was missing in 40% of live rows for two days, and live AUC fell from 0.83 to 0.74. The model uses mean imputation without a missing flag. Explain how you would diagnose this, what you would change in training and serving to make the model robust, and how you would alert on it.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** When a feature that is missing in 5% of training rows is missing in 40% of live rows, the model is scoring a population it never trained on, so I confirm it with missingness and score-shift monitoring, expect part of the AUC loss to be unavoidable (the information is gone), and make the model robust by training with realistic random missingness and alerting on the missing rate.

**Clarifying questions:**
- Was the missingness random across users (an outage) or concentrated in a segment? Why: concentrated missingness shifts the population, random missingness mostly removes information.
- In training, was the feature missing at random or tied to the label? Why: if missingness carried label information in training, a missing flag learns that, and the outage breaks it.
- Is there a fallback source or a cached older value for the feature? Why: a stale value may beat a mean fill.
- How important is the feature (importance, ablation drop)? Why: it sets how much AUC loss is the floor.
- Are decisions made on probabilities or on ranks (thresholds, expected loss)? Why: score levels moved even if ranks did not.

**Approach:**
1. Confirm the cause from logs: missing rate by hour for this feature (5% to 40% in two days), then compare model AUC on rows with the feature present versus missing. If AUC on present rows is still 0.83 and the drop sits in the missing rows, the outage explains it.
2. Check the score distribution: mean score, and share above the threshold, by missing versus present. Mean imputation pushes outage rows to the middle, so thresholds fire differently.
3. Separate unavoidable loss from avoidable loss. Unavoidable: the feature's information is not there. Avoidable: calibration and threshold shifts caused by how the model treats missing values.
4. Training changes: add a missing indicator, and train with extra random missingness (for example drop the feature in a random 30% to 40% of training copies) so the model learns to rely on other features when it is absent. For trees, use native missing-value handling. Do not let the missing flag stand for risk in training if outages break that link.
5. Serving changes: send the true missing state to the model (do not silently fill with a stale default), use a fallback source when it exists, and route to a smaller model without the feature if the missing rate stays high.
6. Alerting: monitor the hourly missing rate per feature against its training rate with a binomial limit (about 6.9% at 2,000 requests an hour, below), page when it crosses, and also monitor mean score and share flagged.
7. Test the setup: replay the outage in staging (force 40% missing) before the next one.
8. Cross-reference: Book 6 Part 2 has "After an upstream deploy, the merchant_category feature's null rate jumped from 0.5% to 18% overnight" for the production-incident side.

**Metrics:**
- Missing rate = rows with the feature missing / rows scored, per hour, per feature.
- Alert limit = the 99.99th percentile of Binomial(requests per hour, training rate) divided by requests; at 2,000 requests and 5% it is 138 rows (6.9%).
- AUC (and mean score versus actual rate) at 5% and at 40% missing, for each model variant.
- Guardrail: calibration (mean score versus actual rate) and the share of rows flagged by the threshold.

**Risks:**
- A missing flag trained where the label is linked to missingness can hurt in an outage: in the simulation the flag model over-scores outage rows.
- Over-augmenting makes the model lean less on the feature even when it is present; check AUC at 5% missing too.
- Alerts on the average hide a segment-only outage; slice by source and region.
- Backfilling after the outage and retraining on the outage days can teach the wrong pattern; exclude or flag those days.

**What the interviewer scores:**
- Strong: separates information lost from avoidable damage (calibration, thresholds), and proves the cause with logs.
- Strong: robust training (random missingness) and a serving fallback, not only "impute better".
- Strong: a concrete alert design with a base rate and a false-alarm rate.
- Weak: "retrain on the outage data" or "just use a missing flag".
- Weak: no monitoring plan.

**Example:** (illustrative simulation, not the prompt's AUC values) In training the feature is missing for 5% of rows, 61% positive among missing versus 32.4% among present. Live, the feature goes missing at random for 40% of rows. The mean-imputation model without a flag drops from AUC 0.833 to 0.786. The model with a flag learned from training (coefficient 1.44) is worse, 0.761, and its mean score rises from 0.340 to 0.427 while the real rate is 0.341. The model trained with extra random missingness (flag coefficient 0.5) keeps 0.786 and a mean score of 0.350. So about 0.047 of AUC is information loss for every model, and the flag model adds avoidable damage. Alert design: at 2,000 requests per hour and a 5% baseline, alert above 138 missing requests (6.9%); the outage hour had 819. Weak answer: "Retrain on the new data." Strong answer: "Prove it from the missing rate, accept the information loss, fix the avoidable damage with training that expects missingness, and alert on the rate."

**Code:**
```python
# Q16: feature missingness jumps from 5% to 40% (illustrative simulation)
import numpy as np
from scipy.stats import rankdata, norm
rng = np.random.default_rng(16)
def sig(z): return 1 / (1 + np.exp(-z))
def auc(s, y):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(X, y, it=30):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (y - p))
    return w
def make(n, miss_rate, informative=False):
    x1, x2 = rng.normal(size=n), rng.normal(size=n)
    y = (rng.random(n) < sig(-1.0 + 1.0 * x1 + 1.4 * x2)).astype(float)
    if informative:      # training world: the feature is missing more often for positives (about 5% overall)
        miss = rng.random(n) < np.where(y == 1, 0.09, 0.03)
    else:                # outage world: missing at random, whatever the label
        miss = rng.random(n) < miss_rate
    return x1, x2, miss, y
def design(x1, x2, miss, mu2, flag):
    x2f = np.where(miss, mu2, x2)                       # mean imputation
    cols = [np.ones(len(x1)), x1, x2f] + ([miss.astype(float)] if flag else [])
    return np.c_[tuple(cols)]
x1, x2, m, y = make(300_000, 0, informative=True)
print(f"training: missing rate {m.mean():.1%}; positive rate when missing {y[m].mean():.1%} vs present {y[~m].mean():.1%}")
mu2 = x2[~m].mean()
# A: today's setup (mean imputation, no flag)
wA = fit(design(x1, x2, m, mu2, False), y)
# B: add a missing flag, trained on the real 5% (the flag soaks up the label link)
wB = fit(design(x1, x2, m, mu2, True), y)
# C: flag, but training copies also get extra RANDOM missingness (to about 40%), so the flag cannot stand for risk
x1c, x2c, mc, yc = np.r_[x1, x1], np.r_[x2, x2], np.r_[m, m | (rng.random(len(m)) < 0.37)], np.r_[y, y]
wC = fit(design(x1c, x2c, mc, mu2, True), yc)
print("flag coefficient: B", round(float(wB[3]), 2), " C", round(float(wC[3]), 2))
out = {}
for rate in (0.05, 0.40):
    a1, a2, am, ay = make(150_000, rate)
    row = []
    for w, f in ((wA, False), (wB, True), (wC, True)):
        sc = design(a1, a2, am, mu2, f) @ w
        row.append((auc(sc, ay), float(sig(sc).mean())))
    out[rate] = row
    print(f"live missing {rate:.0%} (random): actual rate {ay.mean():.3f} | AUC / mean score  A {row[0][0]:.3f} / {row[0][1]:.3f}   B {row[1][0]:.3f} / {row[1][1]:.3f}   C {row[2][0]:.3f} / {row[2][1]:.3f}")
assert out[0.05][0][0] - out[0.40][0][0] > 0.04          # every model loses AUC: the information really is gone
assert out[0.40][1][0] < out[0.40][2][0] - 0.01           # flag-trained-on-5% (B) is worse than the augmented model (C)
# alert: hourly missing rate against the training rate, exact binomial limit, 2,000 requests an hour
from scipy.stats import binom
n_h, p0 = 2_000, 0.05
limit = binom.ppf(0.9999, n_h, p0)                       # about 1 false alarm in 10,000 normal hours
print(f"alert when more than {int(limit)} of {n_h} hourly requests are missing ({limit / n_h:.2%})")
quiet = rng.binomial(n_h, p0, 24 * 30)
print("false alarms in 30 days (720 normal hours):", int((quiet > limit).sum()))
outage = rng.binomial(n_h, 0.40)
print(f"outage hour: {outage} missing of {n_h} -> alarm {outage > limit}")
assert limit / n_h < 0.07 and outage > limit
```

**Output (my run):**
```text
training: missing rate 5.0%; positive rate when missing 61.0% vs present 32.4%
flag coefficient: B 1.44  C 0.5
live missing 5% (random): actual rate 0.340 | AUC / mean score  A 0.833 / 0.340   B 0.828 / 0.340   C 0.833 / 0.330
live missing 40% (random): actual rate 0.341 | AUC / mean score  A 0.786 / 0.328   B 0.761 / 0.427   C 0.786 / 0.350
alert when more than 138 of 2000 hourly requests are missing (6.90%)
false alarms in 30 days (720 normal hours): 0
outage hour: 819 missing of 2000 -> alarm True
```

**Follow-ups:**
- The outage lasts weeks. Retrain with the new missing rate in the mix only if the new rate is the new normal; otherwise keep the model and route to the fallback, and re-evaluate when the vendor recovers.
- Can the model detect the outage itself? Monitor the input's missing rate and the score distribution; the model's own error is delayed because labels arrive late.

**Common mistakes:** Filling with a stale default silently. Adding a missing flag without checking whether missingness was tied to the label. Alerting only on AUC, which arrives late. Treating all AUC loss as a bug instead of lost information.

### Q17 ⭐⭐ 🟢 A data set of 60,000 rows has 300 positives (0.5%), and a tree ensemble takes two hours to train. A teammate suggests SMOTE, another suggests class weights, and a third suggests undersampling. Explain which you would try first, in what order you would compare them, and what metric you would compare them on.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would not start with any of them: I would first train a plain model with a proper metric (PR-AUC) and threshold tuning, then test class weights and undersampling because they are cheap, and try SMOTE last because it is the slowest and most error-prone, comparing all on PR-AUC across several seeds.

**Clarifying questions:**
- What decision does the score drive and what are the costs of a miss and a false alarm? Why: it picks the metric and the threshold, which matter more than the resampling.
- Are the 300 positives all from one time period or one source? Why: SMOTE interpolates between positives, and a clustered positive set gives odd synthetic points.
- How noisy are the labels? Why: SMOTE copies noise into synthetic rows.
- Do I need calibrated probabilities? Why: resampling and weights both shift probabilities and need a correction.
- Compute budget: is two hours per run a limit on how many comparisons I can afford? Why: I should compare cheap variants first.

**Approach:**
1. Fix the evaluation before the method: a stratified split (or repeated stratified folds), metric PR-AUC (average precision, whose no-skill value is the base rate, 0.5%), plus recall at the review budget. With 300 positives the metric is noisy, so use repeated folds and report the spread.
2. Baseline: the model with no rebalancing, and a tuned threshold. Rank-based metrics often change little with weights alone.
3. Class weights: nearly free, no extra rows, no leakage risk. A weight near negatives / positives (199 here) is a starting point; lower weights are worth a try.
4. Undersampling: keep all 300 positives and, say, ten negatives per positive (3,000), so the training set is 3,300 rows. This cuts training time sharply. Repeat with several random negative samples (bagging) to lose less information.
5. SMOTE: only if the above leave a gap. Apply it inside each training fold only (never before the split), tune k, and check against weights. It needs numeric, well-scaled features and gets awkward with categoricals.
6. Compare on the same folds and seeds and keep the simplest method inside the noise. If probabilities are needed, correct or recalibrate on full-rate validation data (see the calibration question below).
7. Cross-reference: Book 1 Part 3 covers the concepts in "Class weights vs resampling (over/under-sampling): trade-offs, and which would you try first?", "PR-AUC: what is its random baseline" and "Where in the pipeline do you apply SMOTE or resampling?".

**Metrics:**
- Average precision (PR-AUC) = mean of the precision at each true positive's rank. No-skill value is the positive rate, 300 / 60,000 = 0.5%.
- Recall at the review budget = true positives in the top k / all positives.
- Spread = standard deviation of the metric over seeds or folds. A difference smaller than that is not a real difference.
- Cost: training rows and wall-clock time. Guardrail: calibration if the probabilities are used.

**Risks:**
- Applying SMOTE or undersampling before the split (leakage and inflated results).
- Comparing methods on ROC-AUC or accuracy, which hide the difference.
- Differences smaller than seed noise being read as wins.
- Resampled models need probability correction.
- With 300 positives, a single holdout split is a lottery.

**What the interviewer scores:**
- Strong: metric and split first, then a cheap-to-expensive order of methods with a reason for each.
- Strong: compares over several seeds and says "no real difference" when that is what the numbers show.
- Strong: mentions time cost (3,300 rows versus 119,400) and probability calibration.
- Weak: "use SMOTE" as the first and only answer.
- Weak: evaluates on accuracy or on a balanced test set.

**Example:** (illustrative simulation, 8 seeds) 60,000 training rows and 300 positives, a test set of 60,000 rows with 300 positives (no-skill average precision about 0.005). Plain logistic model: mean AP 0.0785 (sd 0.0153); class weight 199: 0.0778; undersampling to 1:10: 0.0782; SMOTE to 1:1: 0.0778. The spread between method means is 0.0007, against a seed-to-seed standard deviation of 0.0155, so there is no real difference in this setup. Training rows: 60,000, 60,000, 3,300 and 119,400. If the two-hour run scales linearly with rows (an assumption), undersampling takes about 7 minutes and SMOTE to 1:1 about 4 hours. So the cheap method wins on cost. Weak answer: "SMOTE, it is the standard fix." Strong answer: "Metric first, then weights and undersampling because they are cheap, SMOTE last, compared over seeds."

**Code:**
```python
# Q17: SMOTE vs class weights vs undersampling on 0.5% positives (illustrative simulation)
import numpy as np
rng = np.random.default_rng(17)
def sig(z): return 1 / (1 + np.exp(-z))
def fit(X, y, wt=None, it=25, l2=1.0):
    wt = np.ones(len(y)) if wt is None else wt
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (wt * p * (1 - p))[:, None]).T @ X + l2 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (wt * (y - p)) - l2 * w)
    return w
def avg_precision(s, y):
    o = np.argsort(-s); yy = y[o]; tp = np.cumsum(yy)
    return float((tp / np.arange(1, len(yy) + 1))[yy == 1].mean())
D = 10
beta = np.r_[1.2, 0.8, 0.5, np.zeros(D - 3)]
def make(n, pos):
    X = rng.normal(size=(n, D)); X[:pos] += 1.0 * beta  # first rows are positives, shifted
    y = np.zeros(n); y[:pos] = 1
    return X, y
def smote(Xp, n_new, k=5):
    d = ((Xp[:, None, :] - Xp[None, :, :]) ** 2).sum(-1); np.fill_diagonal(d, np.inf)
    nn = np.argsort(d, 1)[:, :k]
    i = rng.integers(0, len(Xp), n_new); j = nn[i, rng.integers(0, k, n_new)]
    t = rng.random((n_new, 1)); return Xp[i] + t * (Xp[j] - Xp[i])
res = {k: [] for k in ("plain", "class weight", "undersample 1:10", "SMOTE to 1:1")}
for seed in range(8):
    Xtr, ytr = make(60_000, 300); Xte, yte = make(60_000, 300)
    A = lambda X: np.c_[np.ones(len(X)), X]
    res["plain"].append(avg_precision(A(Xte) @ fit(A(Xtr), ytr), yte))
    wt = np.where(ytr == 1, 199.0, 1.0)
    res["class weight"].append(avg_precision(A(Xte) @ fit(A(Xtr), ytr, wt), yte))
    neg = np.flatnonzero(ytr == 0); keep = np.r_[np.arange(300), rng.choice(neg, 3_000, replace=False)]
    res["undersample 1:10"].append(avg_precision(A(Xte) @ fit(A(Xtr[keep]), ytr[keep]), yte))
    Xs = np.r_[Xtr, smote(Xtr[:300], 59_400)]; ys = np.r_[ytr, np.ones(59_400)]
    res["SMOTE to 1:1"].append(avg_precision(A(Xte) @ fit(A(Xs), ys), yte))
print("test positive rate 0.50%, so a no-skill average precision is about 0.005")
print(f"{'method':18} {'mean AP':>8} {'sd over 8 seeds':>16} {'train rows':>11}")
rows = {"plain": 60_000, "class weight": 60_000, "undersample 1:10": 3_300, "SMOTE to 1:1": 119_400}
for k, v in res.items(): print(f"{k:18} {np.mean(v):8.4f} {np.std(v, ddof=1):16.4f} {rows[k]:11,d}")
# time arithmetic from the prompt (assume time grows linearly with rows; an assumption, not a measurement)
base_h = 2.0
for k in ("undersample 1:10", "SMOTE to 1:1"):
    print(f"{k}: about {base_h * rows[k] / 60_000 * 60:.0f} minutes if time is linear in rows")
assert round(base_h * 3_300 / 60_000 * 60) == 7 and round(base_h * 119_400 / 60_000) == 4
assert 60_000 * 0.005 == 300
m = {k: np.mean(v) for k, v in res.items()}
assert min(m.values()) > 10 * 0.005
spread = max(m.values()) - min(m.values()); sd = np.mean([np.std(v, ddof=1) for v in res.values()])
print(f'spread of method means {spread:.4f} versus seed-to-seed sd {sd:.4f}')
```

**Output (my run):**
```text
test positive rate 0.50%, so a no-skill average precision is about 0.005
method              mean AP  sd over 8 seeds  train rows
plain                0.0785           0.0153      60,000
class weight         0.0778           0.0153      60,000
undersample 1:10     0.0782           0.0161       3,300
SMOTE to 1:1         0.0778           0.0152     119,400
undersample 1:10: about 7 minutes if time is linear in rows
SMOTE to 1:1: about 239 minutes if time is linear in rows
spread of method means 0.0007 versus seed-to-seed sd 0.0155
```

The simulation uses a logistic model and a simple self-written SMOTE (five nearest positives, random interpolation); with a tree ensemble the numbers will differ, so run the comparison on your own model. The finding "no real difference" belongs to this simulated setup, not to all data.

**Follow-ups:**
- When would SMOTE win? Sometimes with a model that overfits tiny positive sets, such as a deep net or a very flexible tree model, in low dimensions with continuous features; test it, do not assume.
- The comparison is within noise. Pick the cheapest, then spend effort on features, label quality and the threshold.

**Common mistakes:** Resampling before the split. Using accuracy. Comparing on one seed. Treating 1:1 as the target ratio by default. Forgetting to fix probabilities after resampling.

### Q18 ⭐⭐ 🟢 Two annotators labelled 1,000 support tickets as urgent or not and agreed on 820 of them (82% raw agreement), and each marked about 30% of tickets as urgent. The team says 82% agreement is good enough. Explain what chance-adjusted agreement says here, what the disagreements suggest about the guidelines, and how you would form training labels.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** 82% raw agreement is not good enough to judge, because with 30% urgent each annotator you would agree 58% of the time by chance alone, so chance-adjusted agreement (Cohen's kappa) is 0.57, only moderate, and the 180 disagreements point to unclear guidelines.

**Clarifying questions:**
- Are "urgent" and "not urgent" defined by written criteria with examples? Why: vague criteria produce disagreement that more annotators cannot fix.
- Were both annotators trained and independent (no discussion)? Why: shared habits inflate agreement.
- Is the 30% urgent rate each annotator's own, or the real rate in the data? Why: kappa depends on prevalence.
- What is the cost of a wrong "urgent" label (missed urgent ticket versus wasted attention)? Why: it sets how much to spend on adjudication.
- Is there an expert or ground truth for a subset? Why: agreement is not accuracy; two annotators can agree and both be wrong.

**Approach:**
1. Rebuild the 2x2 table from the numbers. 1,000 tickets, each marks 300 urgent. Disagreements are 180. Both urgent = (300 + 300 - 180) / 2 = 210, each has 90 tickets the other did not mark, and both said not urgent for 610. Agreement 210 + 610 = 820.
2. Chance agreement: 0.3 x 0.3 + 0.7 x 0.7 = 0.58. Kappa = (0.82 - 0.58) / (1 - 0.58) = 0.571. That is moderate, not "good enough".
3. Look at class-specific agreement: on "urgent" the two agree on 0.70 of their combined urgent marks (2 x 210 / 600); on "not urgent" 0.87. The positive class, which matters, is where they disagree most.
4. Read the 180 disagreements (all of them, or a sample of 60 to 100) and group them: unclear rule, missing context (a ticket needs the customer's history), genuine borderline, or annotator slip. Fix the guidelines with examples and re-annotate a fresh sample to see whether kappa rises.
5. Forming labels: keep the 820 agreed rows; send the 180 disagreements to a third senior reviewer (adjudication); for a high-volume setup, use 3 annotators and majority vote. Keep a flag or soft label for borderline tickets and consider down-weighting them in training.
6. Report agreement in the model card (kappa and the by-class numbers) and use it as a ceiling for model performance: a model cannot be much better than labels that humans disagree on.

**Metrics:**
- Observed agreement p_o = agreements / tickets = 820 / 1,000 = 0.82.
- Chance agreement p_e = sum over classes of (A's share x B's share) = 0.3 x 0.3 + 0.7 x 0.7 = 0.58.
- Cohen's kappa = (p_o - p_e) / (1 - p_e) = 0.571. Add a bootstrap interval (here about 0.52 to 0.63).
- Positive-class agreement = 2 x both-positive / (A positives + B positives) = 0.70.
- Guardrail: kappa after the guideline fix on a fresh sample.

**Risks:**
- Kappa depends on prevalence: with rare classes it can be low even when raw agreement is high (a 5% urgent rate and 92% agreement gives kappa 0.158).
- Agreement is not correctness: both annotators can be wrong in the same way.
- Two annotators only: with disagreement you cannot tell which is right without a third.
- Adjudicating only disagreements ignores cases where both are wrong together.

**What the interviewer scores:**
- Strong: computes chance agreement and kappa correctly from the given numbers, and says "moderate".
- Strong: treats disagreements as information about the guidelines, not noise to average away.
- Strong: concrete label formation (adjudication or majority vote, soft labels) and keeps agreement as a quality ceiling.
- Weak: "82% is fine" or calls kappa a model metric.
- Weak: drops all disagreeing tickets without looking at them (this biases against hard cases).

**Example:** (illustrative numbers) 1,000 tickets, 820 agreements, each annotator marks 300 urgent. Table: both urgent 210, A only 90, B only 90, neither 610. Chance agreement 0.58, kappa 0.571, bootstrap 95% interval about 0.52 to 0.63. The trap in the other direction: with only 5% urgent each and 92% raw agreement, chance is 0.905 and kappa is 0.158. Weak answer: "82% agreement is above 80%, so we are fine." Strong answer: "Chance would give 58%, so kappa is 0.57; the 180 disagreements need a guideline fix and a third reviewer."

**Code:**
```python
# Q18: raw agreement versus chance-adjusted agreement (illustrative)
import numpy as np
rng = np.random.default_rng(18)
n, agree, urgent_a, urgent_b = 1_000, 820, 300, 300
# 2x2 table: both urgent x, A only a_only, B only b_only, neither
x = (urgent_a + urgent_b - (n - agree)) // 2          # both = (300+300-180)/2
a_only, b_only = urgent_a - x, urgent_b - x
neither = n - x - a_only - b_only
print("both urgent", x, " A only", a_only, " B only", b_only, " neither", neither)
assert (x, a_only, b_only, neither) == (210, 90, 90, 610) and x + neither == agree
po = agree / n
pe = (urgent_a / n) * (urgent_b / n) + (1 - urgent_a / n) * (1 - urgent_b / n)
kappa = (po - pe) / (1 - pe)
print(f"observed {po:.3f}  chance {pe:.3f}  kappa {kappa:.3f}")
assert round(pe, 2) == 0.58 and round(kappa, 3) == 0.571
# positive-class agreement: 2*both / (A urgent + B urgent)
pos_agree = 2 * x / (urgent_a + urgent_b); neg_agree = 2 * neither / ((n - urgent_a) + (n - urgent_b))
print(f"agreement on 'urgent' {pos_agree:.2f}, on 'not urgent' {neg_agree:.2f}")
assert round(pos_agree, 2) == 0.70
# bootstrap interval for kappa
cells = np.array([x, a_only, b_only, neither]); labs = np.repeat(np.arange(4), cells)
ks = []
for _ in range(2_000):
    s = rng.choice(labs, n); c = np.bincount(s, minlength=4)
    p_o = (c[0] + c[3]) / n; ua, ub = (c[0] + c[1]) / n, (c[0] + c[2]) / n
    p_e = ua * ub + (1 - ua) * (1 - ub); ks.append((p_o - p_e) / (1 - p_e))
lo, hi = np.percentile(ks, [2.5, 97.5]); print(f"bootstrap 95% interval for kappa: {lo:.2f} to {hi:.2f}")
assert lo < kappa < hi
# the trap: 5% prevalence, 92% agreement
pe2 = 0.05 ** 2 + 0.95 ** 2; k2 = (0.92 - pe2) / (1 - pe2)
print(f"5% urgent each, 92% raw agreement: chance {pe2:.3f}, kappa {k2:.3f}")
assert round(k2, 3) == 0.158
# forming labels: keep the 820 agreed rows, send the 180 disagreements to a third, senior reviewer
print("rows to adjudicate:", n - agree, f"= {(n - agree) / n:.0%} of the sample; extra labels needed: {n - agree}")
# if instead one annotator is picked at random for the 180, expected wrong labels among them is half if one is right
print("expected wrong labels if we pick a random annotator on the disagreements:", (n - agree) // 2)
```

**Output (my run):**
```text
both urgent 210  A only 90  B only 90  neither 610
observed 0.820  chance 0.580  kappa 0.571
agreement on 'urgent' 0.70, on 'not urgent' 0.87
bootstrap 95% interval for kappa: 0.52 to 0.63
5% urgent each, 92% raw agreement: chance 0.905, kappa 0.158
rows to adjudicate: 180 = 18% of the sample; extra labels needed: 180
expected wrong labels if we pick a random annotator on the disagreements: 90
```

**Follow-ups:**
- Who breaks ties? A senior reviewer or domain expert, with a short written reason that goes back into the guidelines. If the cost of a wrong label is low, a third annotator vote can do it.
- Would you use soft labels? Yes if there are many borderline tickets: use the share of annotators saying urgent as a target or as a sample weight, and test whether it helps on a trusted validation set.

**Common mistakes:** Quoting raw agreement alone. Reading kappa without prevalence. Throwing away disagreements. Treating agreement as accuracy. Changing guidelines without re-measuring.

### Q19 ⭐⭐ 🟢 A table of 200,000 rows with 1,000 positives has 4,000 rows with a missing key feature, and 600 of those 4,000 rows are positive, against 400 positives among the other 196,000 rows. A manager says to drop the 4,000 rows because they are only 2% of the data. Explain why that is risky, what the numbers imply about the missingness, and what you would do instead.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Dropping those 4,000 rows is risky because the missing group is only 2% of the rows but holds 60% of the positives, with a positive rate of 15% versus 0.2% elsewhere, so the missingness itself is a strong signal and I would keep the rows and add a missing flag.

**Clarifying questions:**
- Why is the feature missing (not collected, not applicable, a failed lookup, a customer who did not give it)? Why: the reason tells me whether missing means "risky" or just "unknown".
- Will live traffic also have this feature missing at about 2%? Why: if yes, the model must be able to score those rows; dropping them from training means it never learns them.
- Is the key feature related to the label for non-missing rows? Why: it tells me whether the feature adds anything beyond the flag.
- Did the missing share change over time? Why: a changing share means a changing process.
- What does the business do with scores on those rows? Why: they may need a separate rule or manual review.

**Approach:**
1. Do the counts: 200,000 rows and 1,000 positives; 4,000 rows missing (2.0%) hold 600 positives (60% of all positives); the other 196,000 rows hold 400 (0.204%).
2. Compare rates: 600 / 4,000 = 15.0% versus 400 / 196,000 = 0.204%, a ratio of 73.5. A chi-square test on the 2x2 table gives a huge statistic (17,250 in the run below), so this is far from chance.
3. Interpret: missingness is not random with respect to the label. It looks like MAR or MNAR (depends on something observed, or on the unobserved value or risk itself). I cannot prove which from the data alone, and either way the flag matters.
4. Show the danger of dropping: the model would train on 400 of 1,000 positives and never see the most positive-heavy group, while live traffic still contains these rows. It would score them like normal rows and miss most of the positives there.
5. Do instead: keep the rows, add `feature_missing` as a feature, fill the value in a simple way (median or model-based, fitted on training folds), or use a model that handles missing values natively. Investigate the cause with the data owner.
6. Check the alternatives on an honest, time-split holdout that also contains missing rows: dropped versus flag plus fill. Report performance separately for missing and present rows.
7. Operations: monitor the missing rate in production and decide, with the business, what happens to rows with a missing key (a rule, manual review, a separate model).

**Metrics:**
- Positive rate by group = positives / rows in the group: 15.0% versus 0.204%.
- Share of positives in the group = 600 / 1,000 = 60%; share of rows = 4,000 / 200,000 = 2%.
- AUC of the missing flag alone = (1 + TPR - FPR) / 2 with TPR = 0.60 and FPR = 3,400 / 199,000 = 0.0171, so 0.791.
- Performance on missing rows and on present rows separately, plus overall PR-AUC.

**Risks:**
- Dropping rows removes most of the signal and creates a mismatch with live traffic.
- The flag can encode a process artefact (for example a fraud team's manual step that fills the field), and then it will not hold at launch. Ask how the value is produced.
- Imputing without a flag throws away the strongest signal.
- If missingness is MNAR, no method recovers the missing value from the data alone; stay humble in claims.

**What the interviewer scores:**
- Strong: computes 15% versus 0.2%, notes 60% of positives, and concludes the missingness is informative.
- Strong: keeps the rows, adds a flag, and evaluates on missing and present groups separately.
- Strong: asks why the value is missing and whether the pattern will hold in production.
- Weak: "it's only 2%, drop it" or "fill with the mean and move on".
- Weak: calls it MCAR without testing.

**Example:** (exact numbers from the prompt) Missing group: 4,000 rows, 600 positives (15.0%). Other rows: 196,000, 400 positives (0.204%). The missing group is 2.0% of rows and 60% of positives. A flag alone has AUC 0.791. If the missing rows were scored like normal rows, the model would expect about 8.2 positives there (4,000 x 0.204%) against 600 real. Weak answer: "Drop them, they are only 2%." Strong answer: "That 2% holds 60% of the positives; I keep them, add a missing flag and find out why they are missing."

**Code:**
```python
# Q19: dropping the 2% of rows with a missing key feature (exact counts from the prompt)
import numpy as np
from scipy.stats import chi2_contingency, rankdata
rows, pos = 200_000, 1_000
mis_n, mis_pos = 4_000, 600
obs_n, obs_pos = rows - mis_n, pos - mis_pos
print("observed rows", obs_n, "observed positives", obs_pos); assert obs_n == 196_000 and obs_pos == 400
r_mis, r_obs = mis_pos / mis_n, obs_pos / obs_n
print(f"positive rate: missing {r_mis:.2%}  present {r_obs:.3%}  ratio {r_mis / r_obs:.1f}x")
assert r_mis == 0.15 and round(r_obs, 5) == 0.00204 and round(r_mis / r_obs, 1) == 73.5
print(f"rows dropped {mis_n / rows:.1%}; positives dropped {mis_pos / pos:.0%}")
assert mis_n / rows == 0.02 and mis_pos / pos == 0.6
tab = np.array([[mis_pos, mis_n - mis_pos], [obs_pos, obs_n - obs_pos]])
chi2, p, _, _ = chi2_contingency(tab, correction=False)
print(f"chi-square {chi2:,.0f}, p-value {p:.1e}")
assert p < 1e-100
# missing flag as a single feature
y = np.r_[np.ones(mis_pos), np.zeros(mis_n - mis_pos), np.ones(obs_pos), np.zeros(obs_n - obs_pos)]
flag = np.r_[np.ones(mis_n), np.zeros(obs_n)]
r = rankdata(flag); n1 = y.sum(); n0 = len(y) - n1
auc = (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
tpr, fpr = mis_pos / pos, (mis_n - mis_pos) / (rows - pos)
print(f"AUC of the missing flag alone {auc:.3f}  (TPR {tpr:.2f}, FPR {fpr:.4f}, (1+TPR-FPR)/2 = {(1 + tpr - fpr) / 2:.3f})")
assert abs(auc - (1 + tpr - fpr) / 2) < 1e-9 and auc > 0.78
# what drop does to training and what happens live: share of live positives in missing rows
print(f"after dropping, training positives {obs_pos} of {pos}; but in live traffic 4,000 per 200,000 rows still arrive with the feature missing")
# If we mean-impute and skip the flag, the model cannot tell those rows apart:
print(f"if scored like normal rows, expected positives in the missing group at the normal rate: {mis_n * r_obs:.1f} versus {mis_pos} real")
assert round(mis_n * r_obs, 1) == 8.2
```

**Output (my run):**
```text
observed rows 196000 observed positives 400
positive rate: missing 15.00%  present 0.204%  ratio 73.5x
rows dropped 2.0%; positives dropped 60%
chi-square 17,250, p-value 0.0e+00
AUC of the missing flag alone 0.791  (TPR 0.60, FPR 0.0171, (1+TPR-FPR)/2 = 0.791)
after dropping, training positives 400 of 1000; but in live traffic 4,000 per 200,000 rows still arrive with the feature missing
if scored like normal rows, expected positives in the missing group at the normal rate: 8.2 versus 600 real
```

The p-value prints as 0.0e+00 because it underflows in floating point; read it as "far smaller than 1e-100".

**Follow-ups:**
- Does a significant difference prove MNAR? No. It shows missingness is not MCAR; separating MAR from MNAR needs outside knowledge (how the field is collected) because the data cannot test it.
- What if the flag is an artefact that will disappear? Test with a time split and ask the data owner; if it will disappear, you need other features, and the launch estimate must not rely on the flag.

**Common mistakes:** Dropping rows because they are few. Imputing without a flag. Declaring MCAR. Not checking the live missing rate. Reporting one overall metric that hides the missing group.

### Q20 ⭐⭐ 🟢 In a 300,000-row table, 12,000 rows (4%) hold -999 in the age column, and the income column is stored as text with entries such as 'N/A' and 'null' next to real numbers. A quick model is already trained and works acceptably. Explain how you would find and handle these sentinel and encoding problems, and how you would check whether they affect the model.
**Asked at:** Data-cleaning question banks (an Educative data-science interview data-cleaning lesson, a TechPrep '82 Data Cleaning Interview Questions' page, StrataScratch 'data cleaning traps', a DataCamp cleaning checklist) covering outliers versus errors and unit mismatches; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** -999 and 'N/A' are missing-value codes, not data, so I find them by profiling, turn them into real missing values with flags, refit, and compare against the quick model to see what the bugs were costing.

**Clarifying questions:**
- Does the data dictionary say what -999 means (unknown, not asked, refused)? Why: the meaning decides the flag and the handling.
- Are the missing ages and incomes related to the target or to a data source? Why: informative missingness should be kept as a feature.
- Is the same pipeline used at serving time, with the same coded values? Why: the cleaning must be identical online and offline.
- Which model type is in use? Why: a linear model is damaged by -999 as a number; a tree can accidentally treat it as a separate group.
- Are there other sentinel candidates (0, 9999, '1900-01-01', 'unknown')? Why: the same habit shows up in several columns.

**Approach:**
1. Profile every column: min and max, the most frequent values, counts of values that repeat suspiciously, and a type check. A min of -999 in age, or a mean of -1.43 for a column that should be near 40, tells the story.
2. For text-typed numbers, try a numeric parse with errors turned into missing, then list the tokens that failed (value counts). Here the failures are 'N/A', 'null' and empty strings: nothing else should hide there.
3. Handle explicitly: replace sentinels and tokens with proper missing values, add a missing flag per column, and fill (median fitted on training rows) or use a model that handles missing values natively. Keep the raw column for audit.
4. Check whether missingness carries signal: the target rate among rows with missing age versus present.
5. Put the cleaning in one function used both for training and serving, with tests on a few messy rows.
6. Measure the damage: refit, compare AUC (and coefficients) between the quick model and the cleaned one on a holdout. A small difference is still worth the fix because the quick model is fragile; a large one shows hidden bias.
7. Add checks: schema type checks, an allowed range for age, a count of unparsable tokens per run, and an alert when a new token appears.

**Metrics:**
- Sentinel share = rows equal to the sentinel / rows = 12,000 / 300,000 = 4.0%.
- Unparsable share = rows that fail numeric parsing / rows (income, here 6.03% in the simulation).
- Test AUC of quick model versus cleaned model on the same holdout.
- Coefficient on age versus its true value (simulation only), and the event rate in missing versus present rows.
- Guardrail: rows changed by the cleaning that were not sentinels or known tokens = 0.

**Risks:**
- A -999 left in a numeric column drags a mean to -1.43 and ruins scaling, binning and linear fits.
- A tree model can "work" with -999 by splitting it off, so the bug stays hidden until the encoding changes.
- Filling blanks with 0 turns "unknown" into "zero income".
- Sentinels used in training may differ from those in serving.
- Dropping the 4% rows loses a group with a different event rate.

**What the interviewer scores:**
- Strong: finds the problems by profiling (min, mean, tokens) instead of waiting for model error.
- Strong: converts to real missing values, adds flags, fits the fill on training data only.
- Strong: re-trains and compares, and builds checks into the pipeline.
- Weak: "the model works, leave it."
- Weak: deletes the rows or fills with 0 without checking the effect.

**Example:** (illustrative simulation) 300,000 rows. Age has 12,000 entries of -999 (4.0%), so the mean is -1.43 against 40.14 without them. Income as text: 'N/A' 9,024 rows, 'null' 5,983, empty 3,069, in total 6.03% unparsable. The event rate is 21.3% where age is missing versus 7.7% where it is present, so missing age is informative. The quick model (text coerced, blanks as 0, -999 left in) has test AUC 0.608; the cleaned model with flags has 0.645. The age coefficient is -0.0012 in the quick model and -0.0296 in the cleaned one (true value -0.03). Weak answer: "It works acceptably, so I would not touch it." Strong answer: "I convert the codes to real missing values, add flags, refit and show the AUC and coefficient change; then I add checks."

**Code:**
```python
# Q20: -999 sentinels and text-typed income (illustrative simulation)
import numpy as np, pandas as pd
rng = np.random.default_rng(20)
from scipy.stats import rankdata
def sig(z): return 1 / (1 + np.exp(-z))
def auc(s, y):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(X, y, it=30):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (y - p))
    return w
N = 300_000
age = np.clip(rng.normal(40, 12, N), 18, 90).round()
inc = rng.lognormal(np.log(50_000), 0.5, N).round()
age_missing = np.zeros(N, bool); age_missing[rng.choice(N, 12_000, replace=False)] = True   # 4%
logit = -2.5 - 0.03 * (age - 40) - 0.6 * (inc / 50_000 - 1) + 1.2 * age_missing
y = (rng.random(N) < sig(logit)).astype(float)
df = pd.DataFrame({"age": np.where(age_missing, -999, age), "income": inc.astype(int).astype(str)})
bad = rng.random(N)
df.loc[bad < 0.03, "income"] = "N/A"; df.loc[(bad >= 0.03) & (bad < 0.05), "income"] = "null"
df.loc[(bad >= 0.05) & (bad < 0.06), "income"] = ""
# 1. find them: look at extreme values and at what refuses to parse
print("age sentinel rows:", int((df.age == -999).sum()), f"= {(df.age == -999).mean():.1%}")
assert (df.age == -999).sum() == 12_000
print("age min / mean with sentinel:", df.age.min(), round(df.age.mean(), 2), " mean without:", round(df.age[df.age != -999].mean(), 2))
parsed = pd.to_numeric(df.income, errors="coerce")
tokens = df.income[parsed.isna()].replace("", "<empty>").value_counts()
print("income tokens that failed to parse:\n" + tokens.to_string())
assert set(tokens.index) == {"N/A", "null", "<empty>"} and tokens.sum() == parsed.isna().sum()
print(f"income unparsable: {parsed.isna().mean():.2%}")
# 2. handle: explicit NaN + missing flags + median fill (fit on training rows only)
tr = rng.random(N) < 0.7; te = ~tr
age_c = df.age.where(df.age != -999)
inc_c = parsed
def design(clean):
    if clean:
        a_med, i_med = age_c[tr].median(), inc_c[tr].median()
        return np.c_[np.ones(N), age_c.fillna(a_med), inc_c.fillna(i_med) / 1e4, age_c.isna(), inc_c.isna()]
    i_fill = inc_c.fillna(0)                          # the 'quick model': text coerced, blanks to 0, -999 left in
    return np.c_[np.ones(N), df.age, i_fill / 1e4]
res = {}
for name, flag in (("quick (-999 left in)", False), ("cleaned + flags", True)):
    X = design(flag); w = fit(X[tr], y[tr]); res[name] = auc(X[te] @ w, y[te])
    print(f"{name:22} test AUC {res[name]:.3f}")
assert res["cleaned + flags"] > res["quick (-999 left in)"]
# 3. does it matter?  Compare coefficients on age
Xq = design(False); Xc = design(True)
print("age coefficient quick:", round(fit(Xq[tr], y[tr])[1], 4), " cleaned:", round(fit(Xc[tr], y[tr])[1], 4), " (truth -0.03)")
print(f"event rate: age missing {y[age_missing].mean():.1%} vs present {y[~age_missing].mean():.1%}")
assert abs(fit(Xc[tr], y[tr])[1] + 0.03) < 0.005
```

**Output (my run):**
```text
age sentinel rows: 12000 = 4.0%
age min / mean with sentinel: -999.0 -1.43  mean without: 40.14
income tokens that failed to parse:
income
N/A        9024
null       5983
<empty>    3069
income unparsable: 6.03%
quick (-999 left in)   test AUC 0.608
cleaned + flags        test AUC 0.645
age coefficient quick: -0.0012  cleaned: -0.0296  (truth -0.03)
event rate: age missing 21.3% vs present 7.7%
```

**Follow-ups:**
- Tree model, so the sentinel "works"? It still matters: the tree cannot tell -999 from a genuinely low value if the sentinel changes, scaling and linear baselines break, and a flag is clearer. Convert anyway.
- How do you stop a new sentinel next month? A schema contract with allowed ranges and a nightly check for unparsable tokens and values at the range edge, with an alert.

**Common mistakes:** Using the mean or median with the sentinel still in the column. Coercing text to numbers and filling with 0. Not adding a flag. Fitting the fill on all rows. Cleaning in training code but not in serving.
