### Q31 ⭐⭐ 🟡 A customer-level feature called spend_30d was computed with a window that sometimes extends up to 15 days after the prediction date, and the churn model's offline AUC is 0.91 against 0.77 live. The feature team says the window is just a rolling aggregate. Explain how you would prove the leak, how you would rebuild features with point-in-time correctness, and how you would check the rest of the feature set.
**Asked at:** Splitting and leakage guides (an arXiv paper on panel-data misuse of ML, a LetsDataScience 'science of data splitting' post, a Towards Data Science 'seven common causes of data leakage' article, an APXML recommender-splitting lesson); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A 30-day feature that reads up to 15 days after the prediction date uses the future, so I would prove it by replaying the feature from a snapshot cut at the prediction date, rebuild every feature as-of that date, and audit the rest of the feature set the same way.

**Clarifying questions:**
- What exactly is "the prediction date" and what is the label window? Why: the leak is any feature timestamp later than the prediction timestamp, so I need both clocks defined.
- How was the training table built: a daily snapshot of a feature store, or one big batch query over the full history? Why: batch queries over the full table are where centred windows and "latest value" joins sneak in.
- Is the 0.77 live number measured on the same population and label definition as the 0.91? Why: I must rule out a different cohort or label before blaming the feature.
- Who else uses spend_30d, and are other features built by the same code? Why: the same helper function probably produced other leaks.
- Is there a record of what the live system actually saw on the scoring date? Why: logged serving features are the ground truth to compare the offline table against.

**Approach:**
1. Say what the bug is. The offline spend_30d at prediction date T uses days T-14 to T+15. Live, only days up to T exist. Churners stop spending after they churn, so a window that looks forward sees "no spend" exactly for the customers who are about to churn. The model learns "low future spend means churn", which is the label itself.
2. Prove it with a replay test. Cut the raw events at T so nothing later exists, recompute the feature with the same code, and compare with the stored value. If values change, the feature used data from after T. Count the rows that change.
3. Back it up with two cheap tests. Shift the window back by 15 days: a leak collapses, real signal stays. Compare offline feature values with the logged live values on the same customers and dates.
4. Rebuild with point-in-time correctness. Every feature row gets an `as_of` timestamp. Each source event gets an event time and, if it arrives late, an ingestion time. The join rule is: event_time <= as_of (and ingestion_time <= as_of for late data). In pandas this is `merge_asof` on time, per customer. Windows are trailing only.
5. Audit all features with the same replay: truncate the data at T, recompute every feature, flag any that change. Add a screen for "too good" single-feature AUCs, which are a clue, not a proof.
6. Retrain on the rebuilt table and re-evaluate with a time split. Expect AUC to fall to near the live number. Report the old number as inflated.
7. Make it permanent: a unit test that runs the replay on a sample, a lint rule that bans centred or forward windows, and the same feature code for training and serving.

**Metrics:**
- Replay mismatch rate = rows where recomputed-from-truncated value differs from stored value / all rows. It should be 0 for every feature.
- AUC of the model with leaky vs point-in-time features, on the same time-split test set (the gap is the inflation).
- Train/serve parity: share of live logged feature values equal to the offline recomputation for the same customer and date (target above 99%).
- Guardrail: the live AUC after the fix should land near the rebuilt offline AUC, not near 0.91.

**Risks:**
- The replay only catches leaks the code can express; a label-derived column (like a "closed account" flag) passes a time replay but is still a leak. Review semantics, not only timestamps.
- Late-arriving events: a table keyed on event time can include rows that were not yet in the system at T. Use ingestion time for the as-of join.
- Rebuilding fixes only the feature; a random split of rows from the same customer can still leak (see Book 6 Part 3 Q8 "A model trained on 40,000 rows from 8,000 customers..." and Q9 "A churn model scores AUC 0.88 under a random split...").
- Declaring victory because AUC dropped: the drop is expected, not a finding of quality.

**What the interviewer scores:**
- Strong: names the mechanism (the window includes days after the prediction date, and churners go quiet) and proposes an executable proof (replay on truncated data), not an argument.
- Strong: as-of joins with event and ingestion time, trailing windows only, one code path for training and serving.
- Strong: audits the whole feature set and sets up a permanent test.
- Weak: "the rolling aggregate is fine", "just drop the feature" without proof, or "retrain with more data".
- Cross-reference: Book 1 Part 1 has "What is data leakage? Give 4 real examples (target, preprocessing, temporal, group) and how you would detect it." and Book 1 Part 6 has "How do you build lag and rolling-window features for a GBM (XGBoost/LightGBM) forecaster without leaking future information?".

**Example:** (illustrative numbers) Prediction date T = day 100. Customer A spent Rs 400, 0, 600 in her last three order days and stops buying on day 108 (she churns). Her stored spend_30d covers days 86 to 115, so it contains only the pre-day-108 spend and zero afterwards: it is low. A loyal customer B keeps buying until day 115, so his window is full. At scoring time on day 100 the live feature has no days 101 to 115 at all, so both look alike. Weak answer: "It is a rolling aggregate, it is fine." Strong answer: "Replay it with data cut at day 100. If the value changes for A and B, the window reaches past the prediction date. I would rebuild with an as-of join and re-evaluate."

**Code:**
```python
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(31)
N, D, T = 4000, 160, 100          # customers, days of history, prediction day
H = 15                            # label horizon: churn within the next 15 days

def auc(y, s):
    r = rankdata(s); n1 = int(y.sum()); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# daily spend panel: customers order on a day with prob p; churners stop on their churn day
churn = rng.random(N) < 0.15
c_day = np.where(churn, T + rng.integers(1, H + 1, N), 10**6)
p = rng.beta(3, 3, N) * np.where(churn, 0.55, 1.0)       # churners are slightly less active before
active = np.arange(D)[None, :] < c_day[:, None]
spend = rng.random((N, D)) < p[:, None]
spend = spend * rng.gamma(2.0, 250.0, (N, D)) * active
y = churn.astype(int)                                      # label: churned in (T, T+30]

# 1) the leaky feature: window [T-14, T+15] (centred on T); honest feature: window [T-29, T]
leaky = spend[:, T - 14:T + 16].sum(1)
honest = spend[:, T - 29:T + 1].sum(1)
print("spend_30d offline AUC (leaky window)     :", round(auc(y, -leaky), 3))
print("spend_30d point-in-time AUC (trailing)   :", round(auc(y, -honest), 3))

# 2) replay test: recompute the feature from data truncated at the prediction date and compare
def spend_30d_replay(data, t, window_fn):
    visible = data[:, :t + 1]                  # nothing after t exists in the snapshot
    return window_fn(visible, t)
def leaky_window(vis, t):                      # what the team computed; asks for days that do not exist yet
    return vis[:, max(0, t - 14):t + 16].sum(1)
def trailing_window(vis, t):
    return vis[:, t - 29:t + 1].sum(1)
rep_leaky = spend_30d_replay(spend, T, leaky_window)
rep_ok = spend_30d_replay(spend, T, trailing_window)
diff_leaky = np.mean(~np.isclose(rep_leaky, leaky))
diff_ok = np.mean(~np.isclose(rep_ok, honest))
print("share of rows where replay != stored, leaky:", round(diff_leaky, 3), " trailing:", diff_ok)
# rows that changed are exactly those with spend in days T+1..T+15
future_used = spend[:, T + 1:T + 16].sum(1) > 0
assert np.array_equal(~np.isclose(rep_leaky, leaky), future_used)
assert diff_ok == 0.0

# 3) shift test: push the window back by 15 days; a leak vanishes, real signal stays
shifted = spend[:, T - 29 - 15:T + 1 - 15].sum(1)
print("AUC after shifting the window 15 days back:", round(auc(y, -shifted), 3))

# 4) audit the rest of the feature set with the same replay and a suspicious-AUC screen
orders_7d = (spend[:, T - 6:T + 1] > 0).sum(1)                    # trailing, fine
last_order_gap_full = np.array([T - np.max(np.nonzero(r[:T + 1 + 15])[0], initial=0) for r in spend])  # looks 15 days ahead
last_order_gap_ok = np.array([T - np.max(np.nonzero(r[:T + 1])[0], initial=0) for r in spend])
rows = [("spend_30d", leaky, rep_leaky), ("orders_7d", orders_7d, orders_7d),
        ("days_since_last_order", last_order_gap_full, last_order_gap_ok)]
for name, stored, replay in rows:
    flag = np.mean(~np.isclose(stored, replay))
    a = max(auc(y, stored), 1 - auc(y, stored))
    print(f"{name:24s} rows changed by replay: {flag:5.3f}   single-feature AUC as stored: {a:.3f}")

assert 0.82 < auc(y, -leaky) < 0.92 and 0.72 < auc(y, -honest) < 0.82
assert auc(y, -leaky) - auc(y, -honest) > 0.06
assert abs(auc(y, -shifted) - auc(y, -honest)) < 0.03
assert diff_leaky > 0.3
```

**Output (my run):**
```text
spend_30d offline AUC (leaky window)     : 0.861
spend_30d point-in-time AUC (trailing)   : 0.782
share of rows where replay != stored, leaky: 0.948  trailing: 0.0
AUC after shifting the window 15 days back: 0.779
spend_30d                rows changed by replay: 0.948   single-feature AUC as stored: 0.861
orders_7d                rows changed by replay: 0.000   single-feature AUC as stored: 0.727
days_since_last_order    rows changed by replay: 0.948   single-feature AUC as stored: 0.948
```
The text above matches this run: the leaky window gives AUC 0.861 against 0.782 for the trailing window (the real inflation is smaller than the prompt's 0.91 vs 0.77 because the simulation is simple, the direction is the point). The replay changes 94.8% of the leaky feature's rows and 0% of the trailing feature's, and exactly the rows with spend in days T+1 to T+15 (asserted). Shifting the window 15 days back gives 0.779, which is back to the honest level. In the audit, orders_7d is clean, and days_since_last_order, which looked 15 days ahead, changes in 94.8% of rows and has a suspicious single-feature AUC of 0.948.

**Follow-ups:**
- Replay says some rows are unchanged. Is that fine? Those rows had no spend after T, so the leak did not touch them, but the code is still wrong; fix the code, not just the rows.
- How do you stop it happening again? Add the replay test to CI, keep a feature store with as-of retrieval, and log serving features so training and serving can be compared.
- The team insists the feature is "only" 15 days ahead and "only sometimes". Does the size matter? No. Any future information can inflate offline AUC, and "sometimes" means the leak is concentrated in the customers near the label event, which are the ones the model is judged on.

**Common mistakes:** Arguing from the feature's name instead of replaying it. Fixing one feature and not auditing the others. Using event time for late-arriving data. Using a random split after the fix. Treating the lower AUC as a regression instead of the true number.

### Q32 ⭐⭐ 🟡 A team has three heuristic labelling rules for spam that cover 20%, 35% and 50% of posts and often disagree where they overlap, and it has only 300 hand-labelled posts. They want to combine the rules into training labels. Explain how you would combine them, how you would estimate the accuracy of each rule, and what role the 300 hand labels should play.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
**Say this first (1 line):** I would treat each rule as a noisy voter, learn how accurate each one is from how the rules agree and disagree on the posts they share, combine them with accuracy-based weights (a label model), and use the 300 hand labels to check the result, not to fit it.

**Clarifying questions:**
- What do the rules look like (keyword lists, link counts, account age)? Why: rules built from the same signal make correlated mistakes, and the combination method assumes they do not.
- Does a rule vote on both classes or only fire for spam? Why: a one-sided rule (abstain unless spam) needs a different model of its errors.
- Were the 300 hand labels sampled at random from all posts, or picked where the rules fired or disagreed? Why: a biased hand set gives biased accuracy estimates.
- How common is spam, and is the cost of a false positive (blocking a real post) higher than a miss? Why: it sets the threshold on the final probability.
- Will the final model be a classifier trained on these labels and served on posts the rules never cover? Why: that is the real goal, and it changes how I judge success.

**Approach:**
1. Write each rule as a labelling function: it returns spam, not spam, or abstain. Build a post-by-rule matrix of votes.
2. Check coverage, overlap and conflict. Coverage 20%, 35%, 50% gives a union of about 73% if rules fire independently (1 minus 0.8 x 0.65 x 0.5). Posts no rule covers get no weak label.
3. Estimate each rule's accuracy without labels. For rules that make independent errors, the product of two rules' signed accuracies equals their average agreement: with votes as plus or minus 1, E[l_i l_j] = m_i m_j where m = 2 x accuracy - 1. Three rules give three equations and three unknowns, so each m_i is solvable. Do it on the posts where the pair both vote.
4. Combine with a label model, not a vote count: weight each rule by the log-odds of its accuracy, sum the signed votes, and turn the total into a probability. Ties and uncovered posts abstain.
5. Use the 300 hand labels as a validation set: measure the label model's accuracy and per-rule accuracy with confidence intervals, check the independence assumption (do the rules' errors correlate?), and tune the final threshold. Do not train on them only, and do not reuse them as the final test set if you tuned on them.
6. Train a normal classifier on the weak labels (use the probabilities as soft labels) so it can generalise to posts no rule covers. Judge it on a separate hand-labelled test set, not on weak labels.
7. Keep improving where it pays: label more posts where the rules conflict, and add rules for uncovered posts.

**Metrics:**
- Per-rule coverage = posts it votes on / all posts; overlap and conflict rates = posts with two or more votes (conflict: votes differ) / all posts.
- Estimated accuracy per rule, with the pair-agreement estimate compared against the hand-label estimate and its 95% interval.
- Label-model accuracy on hand labels, on the decided posts; also report the share decided (coverage).
- Final classifier: precision, recall and PR-AUC on a clean hand-labelled test set; guardrail: false-positive rate on real posts.

**Risks:**
- Correlated rules (two rules reading the same keyword): the agreement method over-counts their evidence and the weights are wrong.
- Coverage that depends on the label: a rule that only fires on obvious spam has accuracy estimates that do not transfer to hard posts.
- 300 labels spread over three rules: rule 1 fires on only about 60-75 of them, so its measured accuracy is wide (see the Code block, 0.89 to 0.99 for one rule).
- Teaching the classifier to copy the rules instead of learning the content.
- Using the same 300 posts to estimate accuracies, tune, and report the final number.

**What the interviewer scores:**
- Strong: models abstain, overlap and conflict, and explains that disagreement is the information that reveals accuracy.
- Strong: gives the pair-agreement (triplet) logic or an EM-style label model, and states the independence assumption and how to test it.
- Strong: uses the hand labels for validation and error analysis, with intervals, and keeps a separate clean test set.
- Weak: "take the majority vote" with no accuracy estimate, or "train on the 300 hand labels and ignore the rules".
- Cross-reference: Book 1 Part 3 has "You use an LLM as a classifier or judge to label data. How do you evaluate it (metrics, imbalance, agreement with humans, calibration)?" for the measuring side.

**Example:** (illustrative numbers) 1,000 posts. Rules 1 and 2 both vote on 70 posts and agree on 48 (68.6%). With votes as plus or minus 1, average product = 2 x 0.686 - 1 = 0.371, so m1 x m2 = 0.371. Suppose the other pairs give m1 x m3 = 0.22 and m2 x m3 = 0.15 (invented). Then m1 squared = 0.371 x 0.22 / 0.15 = 0.544, so m1 = 0.74 and accuracy 1 = (1 + 0.74) / 2 = 0.87. Weak answer: "majority vote of the three rules." Strong answer: "estimate each rule's accuracy from the overlap, weight by log-odds, validate on the 300 hand labels, train a classifier on the soft labels."

**Code:**
```python
import numpy as np
from scipy.stats import beta

rng = np.random.default_rng(32)
N = 20000
y = (rng.random(N) < 0.25).astype(int)            # 1 = spam, invented prevalence 25%
cover = [0.20, 0.35, 0.50]
acc = [0.90, 0.75, 0.65]                          # true accuracy of each rule where it fires (hidden from the model)
L = np.full((N, 3), -1)                           # -1 = abstain
for j in range(3):
    fires = rng.random(N) < cover[j]
    right = rng.random(N) < acc[j]
    L[:, j] = np.where(fires, np.where(right, y, 1 - y), -1)

print("coverage per rule:", [round(float((L[:, j] >= 0).mean()), 3) for j in range(3)])
union = (L >= 0).any(1)
print("posts with at least one vote:", round(float(union.mean()), 3))
assert abs(union.mean() - (1 - 0.8 * 0.65 * 0.5)) < 0.01

# agreement on overlaps (no labels needed)
def agree(i, j):
    both = (L[:, i] >= 0) & (L[:, j] >= 0)
    return both.sum(), (L[both, i] == L[both, j]).mean()
for i, j in [(0, 1), (0, 2), (1, 2)]:
    n, a = agree(i, j)
    print(f"rules {i+1},{j+1}: overlap n={n}, agree={a:.3f}")

# triplet method: with conditionally independent rules, m_i = 2*acc_i - 1 and E[l_i l_j] = m_i m_j (votes as +-1)
def m_ij(i, j):
    both = (L[:, i] >= 0) & (L[:, j] >= 0)
    return np.mean((2 * L[both, i] - 1) * (2 * L[both, j] - 1))
m = [np.sqrt(m_ij(0, 1) * m_ij(0, 2) / m_ij(1, 2)),
     np.sqrt(m_ij(0, 1) * m_ij(1, 2) / m_ij(0, 2)),
     np.sqrt(m_ij(0, 2) * m_ij(1, 2) / m_ij(0, 1))]
est = [(1 + x) / 2 for x in m]
print("estimated accuracy (no labels):", [round(float(a), 3) for a in est], " true:", acc)
assert all(abs(e - a) < 0.05 for e, a in zip(est, acc))

# combine: majority vote versus accuracy-weighted vote (weights = log-odds of estimated accuracy)
w = np.log(np.array(est) / (1 - np.array(est)))
score = np.zeros(N)
for j in range(3):
    score += np.where(L[:, j] >= 0, w[j] * (2 * L[:, j] - 1), 0.0)
mv = np.where(L >= 0, 2 * L - 1, 0).sum(1)
wv_lab = np.where(score > 0, 1, 0); mv_lab = np.where(mv > 0, 1, 0)
dec_w = union & (score != 0); dec_m = union & (mv != 0)
print("majority vote: decided", round(float(dec_m.mean()), 3), " accuracy", round(float((mv_lab[dec_m] == y[dec_m]).mean()), 3))
print("weighted vote: decided", round(float(dec_w.mean()), 3), " accuracy", round(float((wv_lab[dec_w] == y[dec_w]).mean()), 3))
accw = (wv_lab[dec_w] == y[dec_w]).mean(); accm = (mv_lab[dec_m] == y[dec_m]).mean()
common = dec_m & dec_w
am = (mv_lab[common] == y[common]).mean(); aw = (wv_lab[common] == y[common]).mean()
print("same posts both decide:", round(float(common.mean()), 3), " majority", round(float(am), 3), " weighted", round(float(aw), 3))
assert aw > am
conflict = ((L == 1).sum(1) > 0) & ((L == 0).sum(1) > 0) & dec_w
print("posts where rules vote both ways:", int(conflict.sum()), " weighted vote accuracy there:", round(float((wv_lab[conflict] == y[conflict]).mean()), 3))
assert (wv_lab[conflict] == y[conflict]).mean() > 0.6

# the 300 hand labels: how well can they measure each rule alone?
hand = rng.choice(N, 300, replace=False)
for j in range(3):
    f = hand[L[hand, j] >= 0]
    k = int((L[f, j] == y[f]).sum()); n = len(f)
    lo, hi = beta.ppf(0.025, k, n - k + 1), beta.ppf(0.975, k + 1, n - k)
    print(f"rule {j+1}: hand-labelled posts where it fires n={n}, accuracy {k/n:.2f}, 95% CI {lo:.2f}-{hi:.2f}")
# the width on rule 1 (about 60 posts) is wide: that is why the hand set validates, it does not fit the weights
n1 = int((L[hand, 0] >= 0).sum())
assert 40 <= n1 <= 80
```

**Output (my run):**
```text
coverage per rule: [0.192, 0.347, 0.495]
posts with at least one vote: 0.734
rules 1,2: overlap n=1346, agree=0.686
rules 1,3: overlap n=1854, agree=0.611
rules 2,3: overlap n=3469, agree=0.577
estimated accuracy (no labels): [0.864, 0.755, 0.652]  true: [0.9, 0.75, 0.65]
majority vote: decided 0.641  accuracy 0.761
weighted vote: decided 0.734  accuracy 0.753
same posts both decide: 0.641  majority 0.761  weighted 0.763
posts where rules vote both ways: 2232  weighted vote accuracy there: 0.707
rule 1: hand-labelled posts where it fires n=74, accuracy 0.96, 95% CI 0.89-0.99
rule 2: hand-labelled posts where it fires n=86, accuracy 0.79, 95% CI 0.69-0.87
rule 3: hand-labelled posts where it fires n=161, accuracy 0.62, 95% CI 0.54-0.70
```
The text above matches this run: coverage is 19%, 35% and 50% with 73.4% of posts voted on by at least one rule. Pair agreement on overlaps (68.6%, 61.1%, 57.7%) yields accuracy estimates of 0.864, 0.755 and 0.652 against true values of 0.90, 0.75 and 0.65, so the estimate is close but not exact (rule 1 is estimated from about 1,300 overlap posts). Weighted voting decides 73.4% of posts at 75.3% accuracy, while majority vote decides only 64.1% (ties abstain) at 76.1%; on the 64.1% both decide the two are nearly equal (76.1% vs 76.3%). So in this simulation the main gain from weights is coverage and sensible tie-breaking, not accuracy. On posts where rules vote both ways the weighted vote gets 70.7%. The 300 hand labels give wide intervals for each rule (rule 1: 74 posts, 0.89 to 0.99), which is why they validate rather than fit.

**Follow-ups:**
- What if two rules are copies of each other? Their agreement is inflated, the estimator trusts them too much; detect by checking pairwise error correlation on the hand labels and drop or merge one.
- Why not train on the 300 labels alone? 300 labels give a weak classifier and wide intervals; the rules give far more (noisy) coverage. Use both: rules to train, hand labels to measure.
- Can an LLM be one of the labelling functions? Yes, treat it as a fourth noisy voter and measure its accuracy the same way; do not let it also grade the final model (see Book 6 Part 3 Q43 "A team labelled training data with one LLM and now uses the same LLM as the judge...").

**Common mistakes:** Majority vote with no accuracy estimate. Treating abstain as "not spam". Assuming independence without checking. Spending all 300 labels on training. Reporting accuracy on weak labels as if they were truth.

### Q33 ⭐⭐ 🟡 A team has 800 real fraud cases among 400,000 transactions (0.2%) and plans to generate 50,000 synthetic fraud rows with a generative model to make the data more balanced. Explain the risks, how you would validate that the synthetic rows help rather than hurt, and why the test set must remain real data only.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
**Say this first (1 line):** Synthetic fraud rows add no new information beyond the 800 real cases, they can copy or distort them, and 50,000 of them would not even balance the data, so I would test them as an ablation inside training folds and judge everything on real, untouched test data.

**Clarifying questions:**
- How is the generator trained (GAN, VAE, diffusion, or an LLM for tabular rows), and on which of the 800 cases? Why: if it saw the cases that later land in the test set, the test is contaminated.
- Is the fraud one pattern or many (card-not-present, account takeover, mule accounts)? Why: a generator tends to average modes and can blur the rare ones.
- What does the model do with the score: rank for review, or block at a threshold? Why: the cost of false alarms decides whether a shifted score distribution matters.
- Is the 0.2% rate stable over time, and are labels delayed? Why: it affects how many real cases I can put in a time-split test set.
- Why balance at all? Why: class weights, a cost-sensitive threshold or a plain model with PR-AUC may already do the job without inventing data.

**Approach:**
1. Do the arithmetic first. 800 + 50,000 = 50,800 fraud rows against 399,200 legitimate ones is 11.3% fraud, not balanced. A 50/50 set would need 398,400 synthetic rows, about 498 copies per real case. Whatever the plan is, the ratio is set by the generator, not by information.
2. Name the risks. (a) No new information: the generator can only reshuffle what it saw in 800 rows, so the model is trained on the generator's guess about fraud. (b) Memorisation: copies or near-copies of real rows. (c) Mode collapse or smoothing: a smooth generator fills the gaps between modes with fake fraud. (d) Shifted scores and calibration: with a fraud share of 11% in training, probabilities are far above the true 0.2%. (e) Leakage into evaluation if synthetic rows are derived from the test cases.
3. Split first, by time or group. Hold out a real test set (and keep its fraud cases out of the generator). Fit the generator only on training-fold fraud.
4. Run an ablation on real data: baseline (no synthetic), class weights, undersampling, and +synthetic at several amounts (for example 0, 2,000, 10,000, 50,000). Same model, same folds, many seeds.
5. Check the synthetic rows themselves: distance to the nearest real training row (privacy and memorisation), per-feature and joint distribution versus real, and a classifier two-sample test (can a model tell synthetic from real?).
6. Report PR-AUC, recall at a fixed review budget, and precision at that budget, each with an interval, on the real test only. Fix the threshold on real validation data; correct the calibration if scores are used as probabilities.
7. Decide. Keep synthetic data only if the gain on real test data is larger than the seed-to-seed spread, and say so with the interval.

**Metrics:**
- PR-AUC (average precision) on the real test set; the baseline value is the fraud rate, about 0.002.
- Recall at a fixed alert budget = frauds caught in the top K scores / all frauds in the test set; precision at K = frauds caught / K.
- Memorisation check = share of synthetic rows closer to a real training row than a small distance threshold; leak check = the same distance to real test frauds.
- Guardrails: calibration (mean predicted rate vs observed rate on real data), alert volume, and per-segment recall.

**Risks:**
- Evaluating on a test set that contains real frauds the generator saw: scores jump (see the Code block).
- Evaluating on a mix of real and synthetic rows: the model is rewarded for recognising the generator.
- Judging one run: with a few hundred test frauds the PR-AUC moves by several points from seed to seed.
- Fixing the wrong problem: if the issue is a poor threshold, more data of the same kind does not help.
- Fraud adapts; a generator trained on last year's pattern teaches last year's pattern.

**What the interviewer scores:**
- Strong: spots that the arithmetic does not balance and says why 800 real cases cap the information.
- Strong: puts the generator inside the training fold, ablates against class weights and undersampling, and reports intervals.
- Strong: keeps the test set 100% real, time-ordered, and untouched by the generator.
- Weak: "more data is always good", or reporting accuracy or ROC-AUC on a mixed set.
- Cross-reference: Book 6 Part 3 Q2 "A colleague balanced a table of 10,000 rows (500 positives, 5%) to 50/50 with SMOTE and only then split it into train and test..." covers the split-order version of the same mistake, and Book 1 Part 3 has "How do you handle class imbalance? Walk through the options and how you choose between them."

**Example:** (illustrative numbers) 400,000 transactions, 800 fraud. Adding 50,000 synthetic fraud rows: 800 + 50,000 = 50,800 fraud of 450,000 rows = 11.3%. Each real fraud is repeated or imitated about 62 times (50,000 / 800). A model trained there scores real fraud at roughly 11% base rate, so a score of 0.3 does not mean 30%. Weak answer: "balance the data with a GAN and test on the balanced set." Strong answer: "the generator is an ablation inside training folds; I would compare it with class weights, test only on real held-out time, and report PR-AUC with an interval."

**Code:**
```python
import numpy as np

# --- the arithmetic in the prompt
real_fraud, total = 800, 400_000
synth = 50_000
legit = total - real_fraud
print("fraud share before:", round(real_fraud / total, 4))
print("fraud share after adding 50,000:", round((real_fraud + synth) / (legit + real_fraud + synth), 4))
need = legit - real_fraud
print("synthetic rows needed for 50/50:", need)
assert round((real_fraud + synth) / (total + synth), 3) == round(50_800 / 450_000, 3)
assert need == 398_400

rng = np.random.default_rng(33)
d = 4
def make(n, nf):
    X = rng.normal(size=(n, d)); y = np.zeros(n, int); y[:nf] = 1       # exactly nf frauds
    sign = np.where(rng.random(nf) < 0.5, -1.0, 1.0)                     # two fraud modes: x0 near -2.2 or +2.2
    X[:nf, 0] = sign * 2.2 + rng.normal(scale=0.6, size=nf)
    X[:nf, 1] += 1.0; X[:nf, 2] += 0.8; X[:nf, 3] += 0.6
    p = rng.permutation(n)
    return X[p], y[p]
X, y = make(400_000, 800)
print("simulated fraud cases:", int(y.sum()), "rate", round(float(y.mean()), 4))
idx = rng.permutation(len(y)); tr, te = idx[:280_000], idx[280_000:]
Xtr, ytr, Xte, yte = X[tr], y[tr], X[te], y[te]

def feats(X): return np.hstack([X, X ** 2, np.ones((len(X), 1))])
def fit(F, t, w=None, iters=25, l2=1e-3):
    w = np.ones(len(t)) if w is None else w
    b = np.zeros(F.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-F @ b)); g = F.T @ (w * (p - t)) + l2 * b
        H = (F * (w * p * (1 - p))[:, None]).T @ F + l2 * np.eye(len(b))
        b -= np.linalg.solve(H, g)
    return b
def ap(t, s):
    o = np.argsort(-s); t = t[o]; tp = np.cumsum(t)
    return float(np.sum(tp / np.arange(1, len(t) + 1) * t) / t.sum())

# generators fitted ONLY on the 560 real training frauds (the honest way), or on all frauds (the leak)
F_tr = Xtr[ytr == 1]; F_all = X[y == 1]
def gaussian_gen(src, n):
    return rng.multivariate_normal(src.mean(0), np.cov(src.T), n)
def memoriser_gen(src, n, s=0.15):
    return src[rng.integers(0, len(src), n)] + rng.normal(scale=s, size=(n, d))

from scipy.spatial import cKDTree
def run(Xs=None):
    Xa = Xtr if Xs is None else np.vstack([Xtr, Xs]); ya = ytr if Xs is None else np.r_[ytr, np.ones(len(Xs), int)]
    b = fit(feats(Xa), ya)
    lr = ap(yte, feats(Xte) @ b)
    _, nn = cKDTree(Xa).query(Xte, k=15)
    knn = ap(yte, ya[nn].mean(1) + 1e-6 * (feats(Xte) @ b > 0))
    return lr, knn
print("test fraud cases:", int(yte.sum()), "train fraud cases:", int(ytr.sum()))
res = {}
res["real only"] = run()
res["+50k gaussian (one blob)"] = run(gaussian_gen(F_tr, synth))
res["+50k memoriser (train frauds)"] = run(memoriser_gen(F_tr, synth))
res["+50k memoriser fitted on ALL frauds (leak)"] = run(memoriser_gen(F_all, synth))
print(f"{'arm':45s} {'logistic PR-AUC':>16s} {'15-NN PR-AUC':>13s}   (real test, base rate {yte.mean():.4f})")
for k, v in res.items(): print(f"{k:45s} {v[0]:16.3f} {v[1]:13.3f}")
# the leak is visible: the leaky arm beats the honest memoriser only because test frauds were copied
assert res["+50k memoriser fitted on ALL frauds (leak)"][1] > res["+50k memoriser (train frauds)"][1]
# sanity: how many of the 50,000 synthetic rows are within 0.3 of a real test fraud in the leaky arm vs honest
def near_test(Xs):
    T = Xte[yte == 1]; c = 0
    for r in Xs[:2000]: c += (np.sqrt(((T - r) ** 2).sum(1)).min() < 0.3)
    return c / 2000
print("share of synthetic rows within 0.3 of a real TEST fraud: honest", near_test(memoriser_gen(F_tr, synth)), " leaky", near_test(memoriser_gen(F_all, synth)))
assert near_test(memoriser_gen(F_all, synth)) > near_test(memoriser_gen(F_tr, synth))
# one real train fraud is copied about 50,000 / 560 times
print("copies per real training fraud:", round(synth / int(ytr.sum()), 1))
assert 80 < synth / int(ytr.sum()) < 100
gs = gaussian_gen(F_tr, synth)
print("share of real train frauds with |x0|<1:", round(float((np.abs(F_tr[:, 0]) < 1).mean()), 3), "  of gaussian synthetic rows:", round(float((np.abs(gs[:, 0]) < 1).mean()), 3))
assert (np.abs(gs[:, 0]) < 1).mean() > 5 * (np.abs(F_tr[:, 0]) < 1).mean()
```

**Output (my run):**
```text
fraud share before: 0.002
fraud share after adding 50,000: 0.1129
synthetic rows needed for 50/50: 398400
simulated fraud cases: 800 rate 0.002
test fraud cases: 253 train fraud cases: 547
arm                                            logistic PR-AUC  15-NN PR-AUC   (real test, base rate 0.0021)
real only                                                0.128         0.101
+50k gaussian (one blob)                                 0.137         0.097
+50k memoriser (train frauds)                            0.101         0.065
+50k memoriser fitted on ALL frauds (leak)               0.100         0.311
share of synthetic rows within 0.3 of a real TEST fraud: honest 0.0585  leaky 0.2235
copies per real training fraud: 91.4
share of real train frauds with |x0|<1: 0.02   of gaussian synthetic rows: 0.338
```
The text above matches this run: fraud share goes from 0.2% to 11.29% with 50,000 rows, and 398,400 rows would be needed for 50/50. In the simulation (800 frauds in two modes, 547 in train, 253 in test) a generator fitted on training fraud only gave no clear gain: logistic PR-AUC 0.128 (real only) versus 0.137 (single Gaussian) and 0.101 (copy-and-jitter), with the nearest-neighbour model going from 0.101 to 0.097 and 0.065. With one seed, differences of a few points are within noise, so I would not claim the Gaussian helped. The single Gaussian put 33.8% of synthetic rows in the gap between the two real modes (|x0| < 1) against 2.0% of real frauds, which is the fake-region risk. The leak is large: when the copy-and-jitter generator is fitted on all 800 frauds, the nearest-neighbour test PR-AUC jumps to 0.311, because 22.4% of synthetic rows sit within 0.3 of a real test fraud (5.9% in the honest version).

**Follow-ups:**
- Is synthetic data ever useful? It can help when it is built from a domain simulator or known rules that add real information (for example new attack types), or to stress-test systems; a purely learned generator from 800 rows adds little.
- How do you handle the score calibration? Train on the synthetic-augmented data if you must, then recalibrate on real validation data (prior correction, Platt or isotonic) before using scores as probabilities.
- What do you do instead? Class weights or a cost-based threshold, careful stratified or time-based splits, more real labels (active learning on borderline cases), and unsupervised or rule signals as extra features.

**Common mistakes:** Mixing synthetic rows into the test set. Fitting the generator before splitting. Believing 50,000 rows balance 400,000. Reporting accuracy. Using the inflated score as a probability. Judging on one seed.

### Q34 ⭐⭐ 🟡 On a training set of 28,000 rows, a cross-validated model strongly disagrees with the given label (confidence above 0.95) on 700 rows (2.5%), and a reviewer finds that 62 of 100 sampled flagged rows are really mislabelled. Explain how you would estimate the overall label-noise rate, how far you would trust that estimate, and whether you would drop, relabel or down-weight those rows.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** The flagged rows only give a floor on the noise rate (about 434 mislabelled rows, 1.6% of the data), because the model flags only the obvious errors, so I would audit a random sample of the unflagged rows too before I quote an overall rate, and I would relabel with human review, not delete blindly.

**Clarifying questions:**
- How were the 100 flagged rows sampled (random among the 700, or the most confident)? Why: a biased review sample biases the 62% precision.
- Is the reviewer reliable (single person, a second opinion on disputed rows)? Why: if the reviewer is noisy, "really mislabelled" is itself uncertain.
- Does the noise look class-dependent or concentrated in some segment? Why: noise that is not random changes both the estimate and the fix.
- What is the model for: ranking, or a decision with a threshold? Why: ranking is fairly robust to light noise; threshold use and calibration are not.
- Is the evaluation set clean? Why: a noisy test set caps the measurable accuracy and hides improvement.

**Approach:**
1. State what is known. 700 of 28,000 rows are flagged (2.5%). The reviewer found 62 of 100 truly mislabelled: precision of the flag is 62%, 95% interval about 52% to 72%.
2. Scale it up: 700 x 0.62 = 434 mislabelled rows among the flagged (interval about 362 to 501), which is 1.55% of 28,000. This is a lower bound on the noise rate, not the rate.
3. Estimate the rest. Draw a random sample of unflagged rows, say 300, and have them reviewed. If 9 are wrong, then 27,300 x 9/300 = 819 more, and the total is about 1,253 rows, 4.5%. Combine both pieces with intervals (stratified estimate: flagged stratum plus unflagged stratum).
4. Know why the unflagged stratum matters. A model that is confident (above 0.95) against a label will find only errors that are far from the decision boundary; mislabelled borderline rows look like ordinary hard examples. In a simulation, flagging at high confidence found only about 14% of the real noise.
5. Trust the estimate only as far as the sample: report intervals, the review protocol and the reviewer agreement, and give the noise rate by class and by segment where the sample size allows.
6. Choose the action by cost. Relabel the flagged rows through human review (best when the label can be checked). Down-weight or drop only when review is too costly, and expect about 38% of flagged rows to be valid hard cases that you would be throwing away.
7. Fix the process: look at where the noise came from (a guideline change, a vendor, a time window) and add a label-quality gate so you do not clean the same problem every quarter.

**Metrics:**
- Flag precision = reviewed-flagged rows that are truly mislabelled / reviewed-flagged rows (62/100).
- Noise rate estimate = (flagged x flag precision + unflagged x unflagged error rate) / all rows, with a 95% interval for each part.
- Flag recall (unknown directly) = flagged mislabelled rows / all mislabelled rows, estimated from the audit.
- Downstream guardrails: accuracy and calibration on a clean, reviewed test set, per-class recall, and the share of rows changed per class.

**Risks:**
- Quoting 2.5% or 1.55% as "the noise rate".
- Dropping the 38% of flagged rows that are valid hard examples; they are often the informative ones and may sit in one class or segment.
- Relabelling with the model's own prediction, which just teaches the model its current mistakes.
- Cleaning the training set while the validation set stays noisy, so you cannot see the benefit.
- Reviewer error: a 100-row review with one disagreeing reviewer can move the number a lot.

**What the interviewer scores:**
- Strong: separates "precision of the flags" from "overall noise rate" and says the flagged set gives a lower bound.
- Strong: proposes a random audit of unflagged rows and reports intervals.
- Strong: chooses relabel-with-review over blind dropping and explains the cost of each.
- Weak: "700 rows are noisy, drop them", or "62% means the data is 62% wrong".
- Cross-reference: Book 6 Part 3 Q38 "An audit of 2,000 random transactions with intensive investigation found 25 frauds..." for noise that is not random, and Book 1 Part 3 has "Positive-unlabeled learning and noisy labels: when negatives are really unlabeled, how does that change metrics and training?".

**Example:** (illustrative numbers) 28,000 rows, 700 flagged. 62 of 100 reviewed are wrong, so 434 of the 700 flagged rows are wrong and 266 are right. If you drop all 700 you lose 266 correct rows. Suppose a random 300 unflagged rows hold 9 errors (3%): that is about 819 more bad rows among 27,300 unflagged rows. The overall rate is (434 + 819) / 28,000 = 4.5%, nearly three times the 1.55% you get from the flagged rows alone. Weak answer: "2.5% are flagged, so noise is 2.5%." Strong answer: "62% precision on flags gives a floor of 1.55%; I would audit unflagged rows to get the real rate."

**Code:**
```python
import numpy as np
from scipy.stats import beta

# --- 1) the arithmetic in the prompt
N, flagged, sampled, bad = 28_000, 700, 100, 62
prec = bad / sampled
lo, hi = beta.ppf(0.025, bad, sampled - bad + 1), beta.ppf(0.975, bad + 1, sampled - bad)
print("flag precision:", prec, " 95% CI", round(lo, 3), "-", round(hi, 3))
est_bad_flagged = flagged * prec
print("mislabelled rows among the 700 flagged:", est_bad_flagged, " (CI", round(flagged * lo), "-", round(flagged * hi), ")")
print("lower bound on noise rate from flagged rows alone:", round(est_bad_flagged / N, 4))
assert est_bad_flagged == 434.0 and round(est_bad_flagged / N, 4) == 0.0155
# unflagged rows must be audited too: invented audit of 300 random unflagged rows, 9 mislabelled
unflagged = N - flagged
u_bad, u_n = 9, 300
total_bad = est_bad_flagged + unflagged * u_bad / u_n
print("with an audit of unflagged rows (9 of 300): total noise rate", round(total_bad / N, 4))
assert round(total_bad / N, 3) == round((434 + 27_300 * 0.03) / 28_000, 3)

# --- 2) simulation: why 'flagged at 0.95' misses most of the noise
rng = np.random.default_rng(34)
n = 28_000
X = rng.normal(size=(n, 3)); w_true = np.array([1.5, -1.0, 0.5])
p = 1 / (1 + np.exp(-(X @ w_true)))
y_true = (rng.random(n) < p).astype(int)
flip = np.where(y_true == 1, rng.random(n) < 0.08, rng.random(n) < 0.03)      # asymmetric noise
y_obs = np.where(flip, 1 - y_true, y_true)
print("true noise rate:", round(float(flip.mean()), 4))

def fit(F, t, iters=20, l2=1e-3):
    b = np.zeros(F.shape[1]); w = np.ones(len(t))
    for _ in range(iters):
        q = 1 / (1 + np.exp(-F @ b)); g = F.T @ (w * (q - t)) + l2 * b
        H = (F * (w * q * (1 - q))[:, None]).T @ F + l2 * np.eye(len(b)); b -= np.linalg.solve(H, g)
    return b
F = np.hstack([X, np.ones((n, 1))])
fold = rng.permutation(n) % 5
prob = np.zeros(n)
for k in range(5):                                         # cross-validated probabilities: row never in its own fit
    b = fit(F[fold != k], y_obs[fold != k]); prob[fold == k] = 1 / (1 + np.exp(-F[fold == k] @ b))
conf_other = np.where(y_obs == 1, 1 - prob, prob)          # model's confidence in the OTHER class
flag = conf_other > 0.9
tp = int((flag & flip).sum())
print("flagged:", int(flag.sum()), " flag precision:", round(tp / flag.sum(), 3), " flag recall of the noisy rows:", round(tp / flip.sum(), 3))
assert tp / flip.sum() < 0.2          # most noisy rows are not flagged

# --- 3) drop vs relabel vs down-weight, scored on clean labels of a fresh test set
Xt = rng.normal(size=(20_000, 3)); yt = (rng.random(20_000) < 1 / (1 + np.exp(-(Xt @ w_true)))).astype(int)
Ft = np.hstack([Xt, np.ones((20_000, 1))])
def acc_of(b): return float((((Ft @ b) > 0).astype(int) == yt).mean())
b_all = fit(F, y_obs)
b_drop = fit(F[~flag], y_obs[~flag])
y_rel = np.where(flag, 1 - y_obs, y_obs); b_rel = fit(F, y_rel)
print("test accuracy  noisy:", round(acc_of(b_all), 4), " drop flagged:", round(acc_of(b_drop), 4), " relabel flagged:", round(acc_of(b_rel), 4))
clean_flagged = int((flag & ~flip).sum())
print("clean rows lost by dropping:", clean_flagged, "  clean rows corrupted by relabelling:", clean_flagged)
```

**Output (my run):**
```text
flag precision: 0.62  95% CI 0.517 - 0.715
mislabelled rows among the 700 flagged: 434.0  (CI 362 - 501 )
lower bound on noise rate from flagged rows alone: 0.0155
with an audit of unflagged rows (9 of 300): total noise rate 0.0447
true noise rate: 0.0548
flagged: 340  flag precision: 0.626  flag recall of the noisy rows: 0.139
test accuracy  noisy: 0.7644  drop flagged: 0.7645  relabel flagged: 0.7645
clean rows lost by dropping: 127   clean rows corrupted by relabelling: 127
```
The text above matches this run: 62% precision, interval 51.7% to 71.5%, so about 434 bad rows (362 to 501) and a floor of 1.55%; with the invented 9-of-300 audit the total is 4.47%. In the simulation (true noise 5.5%, 5-fold cross-validated model) flagging at 0.9 confidence found 340 rows with 62.6% precision but only 13.9% of the true noisy rows, so the flagged count says little about the total. In that simulation drop, relabel and no cleaning gave the same clean-test accuracy (0.764 to 0.765), because a low-capacity linear model on balanced data is quite robust to 5% noise; the gain from cleaning shows up in evaluation labels and in flexible models that memorise noise, not here. Dropping or relabelling would have touched 127 rows that were actually correct.

**Follow-ups:**
- Would you use soft down-weighting? Yes when review is not possible: weight a row by 1 minus the estimated probability that its label is wrong, so uncertain rows count less without being deleted.
- How do you get an unbiased noise estimate cheaply? A random audit sample, stratified by class and by predicted confidence, with a second reviewer on disputed rows.
- What if the 38% valid flagged rows are one class? Then the filter is biased against that class; check the flagged share per class before acting.

**Common mistakes:** Treating the flagged share as the noise rate. Skipping the unflagged audit. Dropping valid hard examples. Relabelling with model predictions. Cleaning training data but not the test set. Reporting no intervals.

### Q35 ⭐⭐ 🟡 A 12-class ticket classifier is trained on 100,000 tickets where the biggest class holds 40% and five classes each hold under 1,000 tickets. Overall accuracy is 91% but the team says the small classes are what the business cares about. Explain which metrics and averaging you would use, how you would handle the rare classes, and how you would report results.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Accuracy of 91% is mostly the big classes, so I would report per-class precision, recall and F1, summarise with macro-averaged F1 (every class counts equally), and handle the five rare classes with stratified splits, class weights or resampling inside training, and class-specific thresholds.

**Clarifying questions:**
- Which classes matter most, and is a miss in a rare class more costly than a false alarm? Why: it decides between recall-first and precision-first per class.
- Are the five rare classes distinct from the others, or do they sit inside a hierarchy (for example sub-types of one parent)? Why: a hierarchy allows a two-stage model and merged reporting.
- Are tickets one label each, or can a ticket have several labels? Why: multi-label needs per-label thresholds and different metrics.
- Is the rare-class share going to change in production? Why: precision depends on the class mix, so a new mix changes the numbers.
- How many examples of each rare class are in the test set? Why: under 100 test examples means a very wide interval.

**Approach:**
1. Show why 91% hides the problem: always predicting the biggest class gets 40% (the 40% class), and the rare classes are 3.5% of tickets, so even getting all of them wrong costs only 3.5 points of accuracy.
2. Get the full picture: a 12x12 confusion matrix, then per-class precision, recall and F1. Look at where each rare class goes (usually into one or two big neighbours).
3. Pick the averaging on purpose. Micro-F1 equals accuracy for single-label problems, so it adds nothing. Macro-F1 is the plain mean over classes and treats a 500-ticket class like a 40,000-ticket class. Weighted-F1 follows class size, so it looks like accuracy. Report macro-F1 as the headline and per-class numbers next to it; add macro-recall over the rare classes as the business number.
4. Fix the evaluation first: stratified split (and stratified cross-validation) so every class appears in every fold; a test set with enough examples per rare class; intervals on every rare-class recall.
5. Handle the rare classes in training: class weights (or sampling) inside the training folds only; threshold or prior shift per class using validation data; more labelled examples for the rare classes (active learning on low-confidence tickets); merge classes only if the business agrees.
6. Calibrate and re-check. Class weights distort probabilities, so recalibrate if the scores are used as probabilities.
7. Report as a table: class, support, precision, recall, F1, with intervals for the rare classes, plus macro-F1 and accuracy. Say clearly which numbers are weak.

**Metrics:**
- Precision_k = TP_k / (TP_k + FP_k) (correct predictions for class k / all tickets predicted as k); recall_k = TP_k / (TP_k + FN_k); F1_k = 2 x P x R / (P + R).
- Macro-F1 = mean of F1_k over the 12 classes. Weighted-F1 = sum of support_k x F1_k / total. Micro-F1 = overall accuracy.
- Rare-class macro-recall = mean recall over the five rare classes.
- Guardrails: confusion into the biggest class, number of test examples per rare class, and the interval on each rare recall.

**Risks:**
- Reporting weighted-F1 or accuracy and believing it speaks for the rare classes.
- Class weights that raise rare recall but ruin rare precision, so the support team gets flooded.
- Rare classes with 100 or fewer test examples: a recall of 0.35 may mean 0.27 to 0.44.
- Resampling before the split (the same leak as in Book 6 Part 3 Q2).
- Rare classes that are different in kind from their look-alikes (new product names, new languages), so more weight does not fix them.

**What the interviewer scores:**
- Strong: explains macro vs weighted vs micro and why micro equals accuracy here.
- Strong: asks which rare classes matter and reports per-class numbers with intervals.
- Strong: handles rare classes in the training folds only and tunes per-class thresholds on validation.
- Weak: "91% is good", or "use SMOTE" with no metric and no split discipline.
- Cross-reference: Book 1 Part 3 has "Multiclass metrics: macro vs micro vs weighted F1. When do you pick each?" and "How do you extend ROC-AUC and calibration to multiclass problems (one-vs-rest, one-vs-one, macro/weighted)?".

**Example:** (illustrative numbers) Class sizes 40,000, 15,000, 13,000, 11,000, 9,000, 5,000, 3,500 and the five rare ones 900, 800, 700, 600, 500 (total 100,000, so the rare five are 3.5%). The big classes have recall about 0.83 to 0.94 and the rare ones 0.55, 0.50, 0.45, 0.40 and 0.35. Accuracy comes to 91.0%, macro-F1 only 0.705, and the macro-recall over the rare five is 0.45. If the rare classes are all wrong, accuracy loses at most 3.5 points. Weak answer: "91% accuracy, good enough." Strong answer: "Accuracy hides the rare classes. I would report per-class P/R/F1 and macro-F1, then fix the rare classes with stratified folds, class weights and thresholds."

**Code:**
```python
import numpy as np
from scipy.stats import beta


# 12 classes, 100,000 tickets; sizes as in the prompt (invented split of the rest)
sizes = np.array([40000, 15000, 13000, 11000, 9000, 5000, 3500, 900, 800, 700, 600, 500])
assert sizes.sum() == 100_000 and sizes[0] / sizes.sum() == 0.40 and (sizes[7:] < 1000).all() and len(sizes) == 12
recall = np.array([0.945, 0.935, 0.925, 0.915, 0.905, 0.885, 0.83, 0.55, 0.50, 0.45, 0.40, 0.35])
rng = np.random.default_rng(35)
K = 12
C = np.zeros((K, K), int)                                   # confusion matrix: rows true, cols predicted
for i in range(K):
    C[i, i] = round(sizes[i] * recall[i])
    miss = sizes[i] - C[i, i]
    w = np.array([0.5 if j == 0 else 0.5 / (K - 2) for j in range(K)]); w[i] = 0
    w = w / w.sum()
    add = np.floor(miss * w).astype(int); add[0 if i else 1] += miss - add.sum()
    C[i] += add
    assert C[i].sum() == sizes[i]
tp = np.diag(C); support = C.sum(1); predicted = C.sum(0)
prec = tp / predicted; rec = tp / support; f1 = 2 * prec * rec / (prec + rec)
acc = tp.sum() / C.sum()
print("accuracy (= micro-F1):", round(float(acc), 4))
print("macro-F1 over all 12:", round(float(f1.mean()), 3), "  weighted-F1:", round(float((f1 * support).sum() / support.sum()), 3))
print("macro recall over the 5 rare classes:", round(float(rec[7:].mean()), 3), "  rare-class share of tickets:", round(support[7:].sum() / C.sum(), 3))
for i in range(K):
    print(f"class {i+1:2d} n={support[i]:6d} precision={prec[i]:.2f} recall={rec[i]:.2f} F1={f1[i]:.2f}")
assert abs(acc - 0.91) < 0.01
assert f1.mean() < acc - 0.05
# a 'predict the biggest class' baseline
print("baseline accuracy, always predict class 1:", sizes[0] / sizes.sum())
# rare classes: how well can recall be measured? Clopper-Pearson for class 12 if the test set holds 25% of it
n12 = int(support[11] * 0.25); k12 = round(n12 * rec[11])
lo, hi = beta.ppf(0.025, k12, n12 - k12 + 1), beta.ppf(0.975, k12 + 1, n12 - k12)
print(f"class 12 test positives {n12}, recall {k12/n12:.2f}, 95% CI {lo:.2f}-{hi:.2f}")
```

**Output (my run):**
```text
accuracy (= micro-F1): 0.9102
macro-F1 over all 12: 0.705   weighted-F1: 0.912
macro recall over the 5 rare classes: 0.45   rare-class share of tickets: 0.035
class  1 n= 40000 precision=0.92 recall=0.94 F1=0.93
class  2 n= 15000 precision=0.97 recall=0.94 F1=0.95
class  3 n= 13000 precision=0.96 recall=0.93 F1=0.94
class  4 n= 11000 precision=0.95 recall=0.92 F1=0.93
class  5 n=  9000 precision=0.94 recall=0.91 F1=0.92
class  6 n=  5000 precision=0.90 recall=0.89 F1=0.89
class  7 n=  3500 precision=0.85 recall=0.83 F1=0.84
class  8 n=   900 precision=0.49 recall=0.55 F1=0.52
class  9 n=   800 precision=0.44 recall=0.50 F1=0.47
class 10 n=   700 precision=0.38 recall=0.45 F1=0.41
class 11 n=   600 precision=0.32 recall=0.40 F1=0.35
class 12 n=   500 precision=0.25 recall=0.35 F1=0.29
baseline accuracy, always predict class 1: 0.4
class 12 test positives 125, recall 0.35, 95% CI 0.27-0.44
```
The text above matches this run: accuracy 0.9102, macro-F1 0.705 and weighted-F1 0.912, so weighted-F1 repeats the accuracy story while macro-F1 shows the gap. The rare five hold 3.5% of the tickets and have a macro recall of 0.45. An always-class-1 baseline gets 0.40. For class 12 a test set with 125 examples (25% of its 500 tickets) gives recall 0.35 with a 95% interval of 0.27 to 0.44.

**Follow-ups:**
- Why not only macro-F1? It hides which class is weak and gives equal weight to a class the business may not care about; use it as the headline and keep the table.
- Class weights or oversampling? Weights are simpler and keep every row; oversampling duplicates rows and can overfit if done before the split. Try weights first, and do either inside the training folds only.
- How do you handle a class with 100 training tickets? Combine active learning, simple rule features, hierarchical grouping and maybe a retrieval or LLM-assisted first pass, and be honest about the interval.

**Common mistakes:** Reporting accuracy or weighted-F1 as the headline. Calling micro-F1 a different number from accuracy in single-label tasks. Oversampling before the split. Skipping stratification. No intervals on rare classes.

### Q36 ⭐⭐ 🟡 A test set holds 20,000 rows with only 20 positives, and the model catches 14 of them (recall 70%). The team wants to say recall is 70% and to compare it with an older model that caught 12. Explain how uncertain these figures are, how you would build the test set or compare the models, and what you would claim.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** With only 20 positives, "70% recall" really means somewhere between about 46% and 88%, and 14 versus 12 caught is no evidence the new model is better, so I would claim nothing yet and get more positives, or run a paired comparison on the same positives.

**Clarifying questions:**
- Are the 20 positives independent cases, or several rows from the same customers or events? Why: clustered positives mean the real sample size is even smaller.
- Did both models score the same 20,000 rows at the same threshold or the same alert budget? Why: only then is a paired comparison possible, and the thresholds must be comparable.
- How many positives could we get from other periods, other regions or labelling backlog? Why: the number of positives, not the number of rows, controls the precision of recall.
- Was the threshold chosen on this test set? Why: if yes, 70% is optimistic.
- What decision depends on this: a launch, a rollback, a report? Why: it sets how much evidence is enough.

**Approach:**
1. Compute the interval, not just the point. For 14 of 20, the exact (Clopper-Pearson) 95% interval is about 0.46 to 0.88; for 12 of 20 it is about 0.36 to 0.81. The two overlap almost completely.
2. Compare the models on the same positives (paired). Only positives where the two models differ matter: new-only catches (b) and old-only catches (c). Use an exact McNemar test (a sign test on b versus c). Best case, where the new model catches the old model's 12 plus 2 more, gives b = 2, c = 0 and a two-sided p-value of 0.5. A more typical split gives p near 0.7.
3. Say what the data supports: the new model is not shown to be better, and not shown to be worse. Also compare precision or false-alarm count at the same recall, since those use the 19,980 negatives and are better estimated.
4. Build a better test set: more positives. For 5 points of half-width around 70% you need about 323 positives. At a 0.1% rate that is 323,000 rows, so collect positives over a longer period, pool several time windows or regions, or label more of the backlog.
5. Enrich the test set, with care: keep all positives and a random share of negatives (say 5%), then weight each kept negative by 20 when computing precision and false-alarm rates. This shrinks the set and the labelling cost, but it does not narrow the recall interval, which depends only on the number of positives.
6. Use cross-validated or bootstrap out-of-fold scores across all data to get more positives into evaluation, and keep a time-based final check.
7. Claim carefully: "On a small test with 20 positives, the new model caught 14 and the old 12; this is not statistically distinguishable. We need about 300 positives to resolve a 10-point difference" and say what extra evidence you will gather.

**Metrics:**
- Recall = positives caught / positives (14 / 20). Report with an exact 95% interval.
- Paired comparison = counts of b (new-only) and c (old-only) caught positives, with an exact McNemar p-value, and a bootstrap interval for the difference in recall.
- False positive count or precision at the matched threshold, using the weights if negatives were subsampled.
- Guardrail: number of positives per slice; if a slice has under 30, do not report slice recall.

**Risks:**
- Choosing the winner on 2 extra catches and shipping on it.
- Using an unpaired test (Fisher) when the same rows are scored by both models, which wastes information (here Fisher gives 0.741 and McNemar 0.688 for the 4-versus-2 split, so the conclusion is the same, but with other splits they can differ).
- Tuning the threshold on the same 20 positives.
- Subsampling negatives without reweighting, so precision looks far too good.
- Treating the narrower interval from a bigger negative set as if it narrowed recall.

**What the interviewer scores:**
- Strong: states the interval (about 46% to 88%) and says the difference of 2 is within noise.
- Strong: proposes a paired test and a plan for more positives (count them, not rows).
- Strong: knows enrichment needs reweighting and does not shrink the recall interval.
- Weak: "70% beats 60%", or "add more negatives".
- Cross-reference: Book 1 Part 3 has "How do you compare two classifiers statistically? Bootstrap CI for AUC, DeLong test, McNemar test."

**Example:** (illustrative numbers) New model catches 14 of 20 (70%), old catches 12 (60%). If 10 of the positives are caught by both, then new-only = 14 - 10 = 4 and old-only = 12 - 10 = 2. Under the null each discordant case is a coin flip, so the exact two-sided p-value for 4 versus 2 is about 0.69. Even if the old model's 12 are all inside the new model's 14 (2 versus 0) the p-value is 0.5. Weak answer: "recall rose from 60% to 70%, ship it." Strong answer: "20 positives cannot tell 70% from 60%; I would pair the models, report intervals and collect about 300 positives."

**Code:**
```python
import math
import numpy as np
from scipy.stats import beta, binom, fisher_exact

def cp(k, n, a=0.05):
    return (beta.ppf(a / 2, k, n - k + 1) if k > 0 else 0.0, beta.ppf(1 - a / 2, k + 1, n - k) if k < n else 1.0)
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

# 1) how uncertain is 14 of 20 and 12 of 20?
for name, k in [("new", 14), ("old", 12)]:
    lo, hi = cp(k, 20); wl, wh = wilson(k, 20)
    print(f"{name}: recall {k/20:.2f}  exact 95% CI {lo:.3f}-{hi:.3f}   Wilson {wl:.3f}-{wh:.3f}")
assert round(cp(14, 20)[0], 2) == 0.46 and round(cp(14, 20)[1], 2) == 0.88

# 2) same 20 positives for both models -> paired comparison; only discordant positives matter
# best case for the new model: it catches the 12 the old one caught plus 2 more -> b=2, c=0
b, c = 2, 0
p_exact = 2 * binom.cdf(min(b, c), b + c, 0.5)          # two-sided exact McNemar (sign test)
print("best case b=2,c=0: two-sided exact McNemar p =", p_exact)
assert p_exact == 0.5
# a more typical split: new catches 14, old 12, overlap 10 -> new-only 4, old-only 2
b, c = 4, 2
p2 = min(1.0, 2 * binom.cdf(min(b, c), b + c, 0.5))
print("overlap 10: new-only 4, old-only 2: p =", round(float(p2), 3))
# unpaired Fisher (wrong test for same rows) is also nowhere near significant
print("unpaired Fisher on 14/20 vs 12/20: p =", round(float(fisher_exact([[14, 6], [12, 8]])[1]), 3))

# 3) how many positives would you need? half-width 0.05 around recall 0.7
n_pos = math.ceil(1.96 ** 2 * 0.7 * 0.3 / 0.05 ** 2)
base = 20 / 20_000
print("positives for +-5 points on recall 0.7:", n_pos, " rows needed at the current 0.1% rate:", round(n_pos / base))
assert n_pos == 323 and round(n_pos / base) == 323_000
# detecting 0.70 vs 0.60 paired, with discordance ~25%: rough n via normal approx on b-c
# simulate: how often does a truly WORSE (0.60) model look at least as good as a 0.70 one on 20 positives?
rng = np.random.default_rng(36)
a = rng.random((200_000, 20)) < 0.70
b_ = rng.random((200_000, 20)) < 0.60
look = (a.sum(1) <= b_.sum(1)).mean()
print("P(truly worse model catches >= as many of 20) :", round(float(look), 3))
assert 0.25 < look < 0.45
# 4) fix the test set: enrich positives (stratified sampling) and reweight negatives
neg_keep = 0.05                                           # keep 5% of negatives
pos_total, neg_total = 20, 19_980
neg_rows = round(neg_total * neg_keep)
print("enriched set: rows", pos_total + neg_rows, " positive share", round(pos_total / (pos_total + neg_rows), 3), " weight on each negative", 1 / neg_keep)
# but recall CI width does not shrink: it depends on positives, not on negatives
assert cp(14, 20)[1] - cp(14, 20)[0] > 0.35
# 5) a larger positive pool: 200 positives, same 70% vs 60% -> now separable?
print("200 positives: 140 vs 120 caught, exact CIs", [tuple(round(float(x), 3) for x in cp(k, 200)) for k in (140, 120)])
```

**Output (my run):**
```text
new: recall 0.70  exact 95% CI 0.457-0.881   Wilson 0.481-0.855
old: recall 0.60  exact 95% CI 0.361-0.809   Wilson 0.387-0.781
best case b=2,c=0: two-sided exact McNemar p = 0.5
overlap 10: new-only 4, old-only 2: p = 0.688
unpaired Fisher on 14/20 vs 12/20: p = 0.741
positives for +-5 points on recall 0.7: 323  rows needed at the current 0.1% rate: 323000
P(truly worse model catches >= as many of 20) : 0.308
enriched set: rows 1019  positive share 0.02  weight on each negative 20.0
200 positives: 140 vs 120 caught, exact CIs [(0.631, 0.763), (0.529, 0.668)]
```
The text above matches this run: the exact interval for 14 of 20 is 0.457 to 0.881 and for 12 of 20 is 0.361 to 0.809. The best case for the new model (b = 2, c = 0) gives p = 0.5, the 4-versus-2 split gives 0.688, and an unpaired Fisher test gives 0.741. About 323 positives (323,000 rows at the current 0.1% rate) are needed for a plus or minus 5-point interval at recall 0.7. In a simulation, a model with true recall 0.60 catches at least as many of 20 positives as a model with true recall 0.70 about 30.8% of the time. Enriching to 5% of negatives gives 1,019 rows with 2.0% positives and a weight of 20 per negative, but the recall interval stays as wide. With 200 positives (140 vs 120) the intervals are 0.631 to 0.763 and 0.529 to 0.668, still touching, which is why a paired test on the same rows matters.

**Follow-ups:**
- Could you bootstrap the 20? You can, but the bootstrap of 20 points is just as uncertain and tends to be too narrow at the extremes; the exact interval is safer.
- What if positives are rare and cannot be collected? Use all historical positives with cross-validation, pool windows, use a proxy label with a documented bias, and state a wide interval in the claim.
- Can I trust ROC-AUC or PR-AUC more? They also depend on the 20 positives, so the same uncertainty applies; report their bootstrap interval.

**Common mistakes:** Quoting 70% without an interval. Reading 14 versus 12 as a win. Using an unpaired test for paired data. Tuning the threshold on the test set. Subsampling negatives without weights. Confusing rows with positives.

### Q37 ⭐⭐ 🟡 A feature is missing in 15,000 of 100,000 rows (15%) and is strongly related to two other columns. The team debates median imputation, iterative model-based imputation and a tree model that handles missing values natively. Explain how you would choose between them, how you would judge imputation quality, and how you would keep imputation inside the cross-validation loop.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** I would choose by testing on the data, not by taste: mask known values in the same pattern as the real missingness, compare imputers on error and on the downstream model, add a missing-indicator, and fit every imputer inside the training folds only.

**Clarifying questions:**
- Why is the value missing: not collected, not applicable, or hidden because of the outcome? Why: it decides whether missing means "unknown" or carries signal, and whether imputing is safe.
- Does the missingness depend on other columns (the prompt says the feature is strongly related to two columns, which suggests it can be predicted from them)? Why: if so the data are plausibly missing at random given those columns, and model-based imputation works.
- Will the same missingness pattern appear at serving time, and how are missing values fed at inference? Why: an imputation that needs many other rows or the target cannot run in production.
- What model will use the feature: linear, tree boosting, neural? Why: trees can often use missing values directly, linear models need numbers.
- Is the goal prediction, or a coefficient or causal estimate? Why: for inference, multiple imputation with proper uncertainty matters; for prediction, a good point fill plus an indicator is usually enough.

**Approach:**
1. Diagnose the mechanism. Compare missing and observed rows on the other columns, and model the missing flag from those columns. If it is predictable from observed columns (as here: missing rate rises from 3% to 34% across quartiles of one column in my run), it is not completely random. Missing at random versus missing because of the value itself cannot be told apart from the data alone; that needs domain knowledge.
2. List candidates: median fill plus an indicator; regression or iterative (chained-equations style) imputation from the related columns, plus an indicator; a model that handles missing values natively (gradient-boosted trees learn which side of a split missing rows go to).
3. Judge imputation quality in two ways. Direct: hide some known values in the same pattern as the real missingness, impute, and measure the error (RMSE) against the hidden truth, and compare the distribution shape. Downstream: train the final model on each version and compare AUC or log loss on a held-out set, especially on rows that were missing.
4. Keep imputation inside the cross-validation loop. For each fold, fit the imputer on the training part only (the median, the regression coefficients), then apply it to the validation part. In scikit-learn this is a Pipeline with the imputer as the first step; the same applies to scalers and target encoders. Never use the target to impute.
5. Add a missing indicator when missingness may carry signal, and test whether it helps.
6. For uncertainty, use multiple imputation (several imputed copies, pool the results) if you need standard errors; for pure prediction a single good imputation plus an indicator is usually enough.
7. Check the serving path: the imputer is saved with the model, handles one row at a time, and has a fallback value for new missing patterns. Monitor the missing rate in production.

**Metrics:**
- Imputation RMSE = square root of the mean squared difference between imputed and true values on the masked known cells, compared with the standard deviation of the feature.
- Downstream AUC (or log loss) on a clean held-out set, overall and on rows that were missing.
- Calibration and stability: the spread of the metric across folds and seeds.
- Guardrail: the missing rate and the imputed-value distribution at serving versus training.

**Risks:**
- Fitting the imputer on all data before the split (mild for a median, severe for target-based fills).
- Using the target to impute: offline metrics rise, serving cannot do it.
- Median fill squeezes the variance and breaks the relationship with the related columns.
- Single imputation understates uncertainty for inference.
- Masking values at random when the real missingness is not random, so the quality check is too optimistic.

**What the interviewer scores:**
- Strong: asks why the value is missing and tests candidates by masking known values under a realistic pattern.
- Strong: puts the imputer inside each training fold (a Pipeline) and never uses the target.
- Strong: mentions the missing indicator and that trees can use missingness directly, with a note that the choice should still be tested.
- Weak: "always use the median" or "iterative imputation is always better".
- Cross-reference: Book 1 Part 1 has "How do you handle missing values? Compare dropping, mean/median, model-based imputation and missing-indicator features; when is missingness informative?", Book 1 Part 4 has "How do tree-based models handle missing values, categorical variables, outliers and unscaled features?", and Book 6 Part 3 Q15 "A feature's missing values were filled with the mean target value within each city..." covers the target-leak version.

**Example:** (illustrative numbers) 100,000 rows, a feature missing in 15,000 (15%). The feature has a standard deviation of 2.3 and is related to two other columns. Median fill guesses the same number for everyone, so its error on hidden values is about as large as the standard deviation (2.4 in my run). A regression from the two related columns brings the error to about 0.7. Weak answer: "median is simple and robust, use it." Strong answer: "mask some known values, compare errors and downstream AUC, keep it in the CV loop, add an indicator."

**Code:**
```python
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(37)
n = 100_000
x1 = rng.normal(size=n); x2 = rng.normal(size=n)
z = 2.0 * x1 - 1.0 * x2 + rng.normal(scale=0.7, size=n) + 3.0          # feature with missing values; strongly related to x1, x2
logit = 0.9 * (z - 3.0) + 0.5 * x1 - 0.3 * x2 - 1.0
y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
# MAR: missingness depends on x1, x2 (observed), tuned to 15%
t = -2.3 + 1.2 * x1 + 0.8 * x2
m = rng.random(n) < 1 / (1 + np.exp(-t))
print("missing share:", round(float(m.mean()), 3), " mean z when missing / observed:", round(float(z[m].mean()), 2), round(float(z[~m].mean()), 2))
assert 0.14 < m.mean() < 0.16

def auc(y, s):
    r = rankdata(s); n1 = int(y.sum()); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))
def fit(F, t, iters=20, l2=1e-3):
    b = np.zeros(F.shape[1])
    for _ in range(iters):
        q = 1 / (1 + np.exp(-F @ b)); g = F.T @ (q - t) + l2 * b
        H = (F * (q * (1 - q))[:, None]).T @ F + l2 * np.eye(len(b)); b -= np.linalg.solve(H, g)
    return b
def lin_fit(A, t): return np.linalg.lstsq(A, t, rcond=None)[0]

# imputers: each is fitted on a training part only, then applied to any part
def make_median(Xa, za, ma, ya=None):
    med = np.median(za[~ma])
    return lambda Xb, zb, mb: (np.where(mb, med, zb), mb.astype(float))
def make_regress(Xa, za, ma, ya=None):
    A = np.c_[Xa, np.ones(len(Xa))]; beta_ = lin_fit(A[~ma], za[~ma])
    return lambda Xb, zb, mb: (np.where(mb, np.c_[Xb, np.ones(len(Xb))] @ beta_, zb), mb.astype(float))
def make_leaky_target(Xa, za, ma, ya):                       # includes the TARGET in the imputation model
    A = np.c_[Xa, ya, np.ones(len(Xa))]; beta_ = lin_fit(A[~ma], za[~ma])
    return lambda Xb, zb, mb, yb: (np.where(mb, np.c_[Xb, yb, np.ones(len(Xb))] @ beta_, zb), mb.astype(float))

X = np.c_[x1, x2]
tr = np.arange(n) < 70_000; te = ~tr
res = {}
# a) imputation quality on rows where z is known: mask them under the same mechanism, impute, score RMSE
known = ~m
# hide a further share of the known values with the same MAR mechanism
msk = known & (rng.random(n) < 1 / (1 + np.exp(-(t + 0.0))))
for name, mk in [("median", make_median), ("regression", make_regress)]:
    imp = mk(X[tr], z[tr], m[tr] | msk[tr])
    zi, _ = imp(X[te], z[te], msk[te] | m[te])
    err = zi[msk[te]] - z[te][msk[te]]
    print(f"imputation RMSE on masked known values, {name:10s}: {np.sqrt((err ** 2).mean()):.3f}   (std of z {z.std():.2f})")

# b) downstream AUC, imputer fitted on the training part only
def downstream(mk, add_flag=True):
    imp = mk(X[tr], z[tr], m[tr])
    ztr, ftr = imp(X[tr], z[tr], m[tr]); zte, fte = imp(X[te], z[te], m[te])
    cols = lambda Xb, zb, fb: np.c_[Xb, zb, fb] if add_flag else np.c_[Xb, zb]
    Ftr = np.c_[cols(X[tr], ztr, ftr), np.ones(tr.sum())]; Fte = np.c_[cols(X[te], zte, fte), np.ones(te.sum())]
    b = fit(Ftr, y[tr]); sc = Fte @ b; return auc(y[te], sc), auc(y[te][m[te]], sc[m[te]])
bf = fit(np.c_[X[tr], z[tr], np.ones(tr.sum())], y[tr]); sf = np.c_[X[te], z[te], np.ones(te.sum())] @ bf
full, full_m = auc(y[te], sf), auc(y[te][m[te]], sf[m[te]])
print("AUC with z fully observed (ceiling): all test rows", round(float(full), 4), "  rows that are missing in practice", round(float(full_m), 4))
for name, mk in [("median", make_median), ("regression", make_regress)]:
    for flag in (False, True):
        a_all, a_m = downstream(mk, flag); print(f"AUC, {name:10s} flag={flag!s:5s}: all rows {a_all:.4f}   missing-rows only {a_m:.4f}")
# c) the leak: impute using the target, on both parts (fine offline, impossible at serving time)
imp = make_leaky_target(X[tr], z[tr], m[tr], y[tr])
ztr, ftr = imp(X[tr], z[tr], m[tr], y[tr]); zte, fte = imp(X[te], z[te], m[te], y[te])
b = fit(np.c_[X[tr], ztr, ftr, np.ones(tr.sum())], y[tr])
sl = np.c_[X[te], zte, fte, np.ones(te.sum())] @ b
leak_auc, leak_m = auc(y[te], sl), auc(y[te][m[te]], sl[m[te]])
print("AUC with target-aware imputation (leak): all rows", round(float(leak_auc), 4), "  missing-rows only", round(float(leak_m), 4))
assert leak_m > full_m + 0.01
# d) imputer fitted on all rows vs inside the training fold: for a label-free imputer the gap is tiny, still do it inside
imp_all = make_median(X, z, m)
zall, _ = imp_all(X, z, m)
print("median fitted on all rows:", round(float(np.median(z[~m])), 4), " fitted on train part:", round(float(np.median(z[tr & ~m])), 4))
print("MAR check: missing rate in x1 quartiles:", [round(float(m[(x1 >= lo) & (x1 < hi)].mean()), 3) for lo, hi in zip(np.quantile(x1, [0, .25, .5, .75]), np.r_[np.quantile(x1, [.25, .5, .75]), 1e9])])
```

**Output (my run):**
```text
missing share: 0.151  mean z when missing / observed: 4.07 2.82
imputation RMSE on masked known values, median    : 2.412   (std of z 2.34)
imputation RMSE on masked known values, regression: 0.694   (std of z 2.34)
AUC with z fully observed (ceiling): all test rows 0.9049   rows that are missing in practice 0.8972
AUC, median     flag=False: all rows 0.8988   missing-rows only 0.8845
AUC, median     flag=True : all rows 0.8998   missing-rows only 0.8846
AUC, regression flag=False: all rows 0.9031   missing-rows only 0.8847
AUC, regression flag=True : all rows 0.9031   missing-rows only 0.8847
AUC with target-aware imputation (leak): all rows 0.9069   missing-rows only 0.9126
median fitted on all rows: 2.8294  fitted on train part: 2.8376
MAR check: missing rate in x1 quartiles: [0.031, 0.082, 0.153, 0.336]
```
The text above matches this run: 15.1% of the rows are missing, with the missing rate rising from 3.1% to 33.6% over quartiles of x1, so the pattern is predictable from observed columns. Median imputation has an error of 2.412 (the feature's standard deviation is 2.34), regression imputation 0.694. The downstream effect on AUC is small here because the feature is nearly a function of the two other columns and the model is linear: ceiling 0.9049 with the true values, 0.8988 (median), 0.9031 (regression); on the rows that were actually missing it is 0.8972 (ceiling), 0.8845 (median) and 0.8847 (regression). The missing indicator adds almost nothing (0.8998 vs 0.8988) because this mechanism depends on observed columns only. Target-aware imputation scores 0.9126 on the missing rows, above the 0.8972 ceiling you would get with the real values, which proves it is a leak that cannot be reproduced in production. The median fitted on all rows (2.8294) versus on the training part (2.8376) differs a little, which shows why fitting inside the fold is a habit, not a big effect for a median.

**Follow-ups:**
- Will the native tree handling just win? It often does when missingness carries signal, since it learns a branch for missing, but it is not guaranteed and I could not run one here with the standard library; test it against imputed versions on the same folds.
- Why add an indicator? If the reason for missing is related to the outcome, the flag carries information that any fill removes; test it and keep it only if it helps.
- When do you need multiple imputation? When you report coefficients or intervals and need honest uncertainty; for prediction alone, it is rarely worth the cost.

**Common mistakes:** Fitting the imputer on the full data before cross-validation. Using the target to fill. Judging imputation only by its RMSE and not by the downstream metric. Hiding values at random when the real pattern is not random. Forgetting the serving path.

### Q38 ⭐⭐ 🔴 An audit of 2,000 random transactions with intensive investigation found 25 frauds, but only 20 of them carry a fraud label in the system, while the labelled fraud rate overall is 1%. Explain what kind of label noise this is, how it affects the training, the measured recall and the measured precision, and how you would estimate and handle it.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** This is one-sided, class-conditional label noise (real frauds missing a fraud label, about 20% of them), probably not random, so the model learns to treat hidden fraud as normal, measured recall looks better than the truth, measured precision looks worse, and I would fix it with an audit-based estimate and review of the unlabelled-but-suspicious cases.

**Clarifying questions:**
- How do frauds get a label today (chargebacks, rules, analyst review)? Why: it tells me which kinds of fraud are systematically missing.
- Did the audit also check the 1,975 non-fraud rows for false fraud labels, and were any of the 20 labelled rows wrong? Why: the one-sided story needs "no false positives", which I should verify.
- Was the audit sample truly random and the investigation blind to the system label? Why: a biased audit biases the 80% figure.
- How is model performance reported today, and how is the review queue chosen from the scores? Why: the same missing labels may bias both metrics and training.
- What is the business cost of an undetected fraud versus a false alert? Why: it sets how much effort goes into recovering missing labels.

**Approach:**
1. Do the audit arithmetic. 25 of 2,000 are truly fraud (1.25%); 20 carry a label (1.0%, matching the system's overall 1% labelled rate). So P(label = fraud | fraud) is 20 / 25 = 80%, with a wide 95% interval of about 59% to 93%. If none of the other 1,975 rows has a false fraud label, then P(label = fraud | not fraud) is about 0.
2. Name it. This is asymmetric, class-conditional label noise where positives are missing (a false-negative-only pattern, like positive-unlabelled data). It is probably not completely random, because the frauds nobody noticed are different from the frauds somebody did.
3. Effect on training. The model sees about 20% of the fraud as "legitimate", so it learns that hidden-fraud patterns are normal and gives them low scores. Overall prevalence is understated (1.0% versus 1.25%), probabilities are too low, and recall on the hidden kind of fraud is poor.
4. Effect on measured recall. Recall measured against labels counts only labelled frauds, which are the ones the existing process notices and the model resembles. Measured recall is therefore too high compared with the true recall (in my run, 0.277 measured versus 0.236 true).
5. Effect on measured precision. A true fraud the model flags but nobody labelled is scored as a false positive, so measured precision is too low (0.715 versus 0.763 true in my run).
6. Estimate it properly. Keep running a random investigated audit and estimate label sensitivity overall and by fraud type, channel or amount band. Do not apply one global factor: the sensitivity among the frauds the model catches (0.937 in my run) is much higher than among all frauds (0.801).
7. Handle it. For evaluation, use audited samples with weights, not the system labels alone. For training, send high-score unlabelled cases to investigation (active relabelling), treat labels as positive-unlabelled (weight unlabelled rows less or use a PU loss), add hidden-pattern detectors, and track label sensitivity as a monitored number.

**Metrics:**
- Label sensitivity = labelled frauds / true frauds in the audit (20 / 25 = 0.80), with an exact interval and by segment.
- Measured precision = flagged rows with a fraud label / flagged rows; true precision = flagged true frauds / flagged rows (needs investigation of flagged rows).
- Measured recall = flagged labelled frauds / labelled frauds; true recall = flagged true frauds / all true frauds (needs the audit).
- Guardrails: audit sample size, the labelled-fraud rate over time (a drop can be a labelling delay, not less fraud), and recall on frauds that were found late.

**Risks:**
- Reporting recall from system labels only: it rewards the model for resembling the labelling process.
- Believing precision is low and tightening the threshold, which hides real fraud.
- Applying a single correction factor such as dividing recall by 0.8.
- An audit of only 25 frauds: the sensitivity interval is wide, so be careful with segment cuts.
- Training on these labels and then evaluating on the same label source: the loop reinforces the blind spot (see also Book 6 Part 3 Q29 "Only the 20,000 of 1,000,000 transactions (2%) flagged by old rules were reviewed by investigators...").

**What the interviewer scores:**
- Strong: names it as one-sided, class-conditional (and probably not random) noise and computes 80% from the audit.
- Strong: states the direction of each bias (recall too high, precision too low, prevalence too low) and why.
- Strong: proposes a random audit, segment-level sensitivity, and review of high-score unlabelled cases, not one global fudge factor.
- Weak: "label noise is symmetric, so ignore it", or "just scale recall by 1.25".
- Cross-reference: Book 1 Part 3 has "Positive-unlabeled learning and noisy labels: when negatives are really unlabeled, how does that change metrics and training?".

**Example:** (illustrative numbers) The model flags 600 transactions. Labels say 430 of them are fraud (measured precision 71.7%). Investigators check the 170 others and find 28 more true frauds, so true precision is 458 / 600 = 76.3%. Across the whole test set there are 1,925 labelled frauds and 2,420 true frauds (labelled share 79.5%, about 80%); the model catches 430 labelled and 458 true: measured recall 430 / 1,925 = 22.3%, true recall 458 / 2,420 = 18.9%. Weak answer: "recall is 22%, precision is 72%." Strong answer: "labels miss 20% of fraud, so recall is overstated and precision understated; I need an audit-based estimate."

**Code:**
```python
import math
import numpy as np
from scipy.stats import beta

# 1) the audit arithmetic
audit, true_fraud, labelled = 2000, 25, 20
print("true fraud rate in audit:", true_fraud / audit, "  labelled fraud rate in audit:", labelled / audit)
sens = labelled / true_fraud
lo, hi = beta.ppf(0.025, labelled, true_fraud - labelled + 1), beta.ppf(0.975, labelled + 1, true_fraud - labelled)
print("label sensitivity P(label=fraud | fraud):", sens, " 95% CI", round(float(lo), 3), "-", round(float(hi), 3))
assert sens == 0.8 and true_fraud / audit == 0.0125 and labelled / audit == 0.01
# 2) simulate the consequences. Frauds come in two kinds: 'seen' (the old rules catch them, so they get labelled)
#    and 'hidden' (nobody notices them, so they are mostly unlabelled): noise is NOT random.
rng = np.random.default_rng(38)
n = 400_000
X = rng.normal(size=(n, 3))
fraud = rng.random(n) < 0.0125
hidden = fraud & (rng.random(n) < 0.25)
seen = fraud & ~hidden
X[seen, 0] += 2.5; X[seen, 1] += 1.0                  # seen frauds look like the old rules' targets
X[hidden, 2] += 2.5; X[hidden, 1] += 1.0              # hidden frauds look different
lab = np.where(seen, rng.random(n) < 0.96, np.where(hidden, rng.random(n) < 0.28, False))
print("true fraud rate:", round(float(fraud.mean()), 4), " labelled rate:", round(float(lab.mean()), 4), " label sensitivity:", round(float(lab[fraud].mean()), 3))
assert 0.76 < lab[fraud].mean() / 1 < 0.84
tr = np.arange(n) < 250_000; te = ~tr
def fit(F, t, iters=25, l2=1e-3):
    b = np.zeros(F.shape[1])
    for _ in range(iters):
        q = 1 / (1 + np.exp(-F @ b)); g = F.T @ (q - t) + l2 * b
        H = (F * (q * (1 - q))[:, None]).T @ F + l2 * np.eye(len(b)); b -= np.linalg.solve(H, g)
    return b
F = np.c_[X, X ** 2, np.ones(n)]
b = fit(F[tr], lab[tr].astype(float))
s = F[te] @ b
k = 600                                     # review capacity: flag the top 600 test rows
top = np.argsort(-s)[:k]
flag = np.zeros(te.sum(), bool); flag[top] = True
lab_te, fr_te = lab[te], fraud[te]
tp_lab = (flag & lab_te).sum(); tp_true = (flag & fr_te).sum()
print(f"flagged {k}: label-precision {tp_lab/k:.3f}  true-precision {tp_true/k:.3f}")
print(f"label-recall {tp_lab/lab_te.sum():.3f}  true-recall {tp_true/fr_te.sum():.3f}")
print("recall of hidden frauds:", round(float((flag & hidden[te]).sum() / hidden[te].sum()), 3), " recall of seen frauds:", round(float((flag & seen[te]).sum() / seen[te].sum()), 3))
assert tp_true / k > tp_lab / k                     # precision understated
assert tp_lab / lab_te.sum() > tp_true / fr_te.sum()  # recall overstated
# 3) correct the headline with the audit: recall_true = TP_true / fraud_total. Needs an audited estimate of how many are missed
# audit-based estimate on the test slice: investigate a random 2,000 of the test rows
aud = rng.choice(te.sum(), 2000, replace=False)
est_fraud_rate = fr_te[aud].mean(); est_sens = lab_te[aud][fr_te[aud]].mean() if fr_te[aud].any() else float('nan')
print("audit sample: true frauds", int(fr_te[aud].sum()), " labelled", int(lab_te[aud][fr_te[aud]].sum()), " est. sensitivity", round(float(est_sens), 2))
sens_flagged = tp_lab / tp_true
print("label sensitivity among frauds the model flagged:", round(float(sens_flagged), 3), " among all frauds:", round(float(lab_te[fr_te].mean()), 3))
assert sens_flagged > lab_te[fr_te].mean() + 0.1     # the model's catches are the easy-to-label ones, so one global factor misleads
```

**Output (my run):**
```text
true fraud rate in audit: 0.0125   labelled fraud rate in audit: 0.01
label sensitivity P(label=fraud | fraud): 0.8  95% CI 0.593 - 0.932
true fraud rate: 0.0125  labelled rate: 0.0099  label sensitivity: 0.791
flagged 600: label-precision 0.715  true-precision 0.763
label-recall 0.277  true-recall 0.236
recall of hidden frauds: 0.024  recall of seen frauds: 0.302
audit sample: true frauds 23  labelled 18  est. sensitivity 0.78
label sensitivity among frauds the model flagged: 0.937  among all frauds: 0.801
```
The text above matches this run: the audit gives 80% sensitivity with an interval of 0.593 to 0.932. In the simulation (true fraud 1.25%, labelled 0.99%, sensitivity 0.791) the top-600 flags have measured precision 0.715 versus true precision 0.763, and measured recall 0.277 versus true recall 0.236. Recall of hidden frauds is 0.024 against 0.302 for seen frauds: the model learned the labelling process. The label sensitivity among frauds the model flagged is 0.937 versus 0.801 overall, which is why one global correction factor does not work. The second audit (23 true frauds, 18 labelled, sensitivity 0.78) shows how wide a 2,000-row audit stays.

**Follow-ups:**
- Can you correct the metrics with the 80%? Only if label sensitivity is the same for the flagged and the unflagged frauds; it usually is not (0.937 versus 0.801 here), so audit the flagged rows and the unflagged rows separately.
- Is this MCAR, MAR or MNAR? The missing fraud labels depend on the kind of fraud (which the features partly describe) and on whether anyone noticed it, so it behaves like not-at-random labelling; you cannot prove that from the labels alone, which is why the random audit is needed.
- What would you change in the pipeline? Randomly investigate a small share of every score band each week, so you always have unbiased labels to evaluate and retrain on.

**Common mistakes:** Treating missing labels as true negatives. Using system labels for evaluation. Dividing recall by 0.8. Not checking for false fraud labels. Ignoring that the audit itself has a wide interval.

### Q39 ⭐⭐ 🔴 On a streaming app, users rate only about 2% of the titles they watch, the average rating among rated titles is 4.3, and a random prompt to 1,000 users gives an average of 3.6 on the titles they watched. A recommender is trained only on the observed ratings. Explain what missing-data mechanism is at work, how it distorts the model and how you would correct or evaluate for it.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** This is data missing not at random: people rate more when they loved a title, so the observed 4.3 is inflated against the 3.6 from the random prompt, and I would correct the training with weights estimated from a random-sample probe and evaluate on that probe, not on the observed ratings.

**Clarifying questions:**
- How was the random prompt delivered, and what share of prompted users answered? Why: if only some users replied, the probe has its own non-response bias.
- Does the 3.6 average cover the same titles and the same kind of users as the 4.3? Why: a gap from a different user or title mix is not the same as a gap from selection.
- Is rating a star score only, or are there other signals (watch time, completion, thumbs)? Why: implicit feedback is observed for everyone and is a better base for training.
- What does the recommender decide: the top-N list, or a predicted rating shown to users? Why: ranking and rating prediction suffer differently.
- Can we keep a small random-exposure or random-prompt stream going? Why: unbiased data is the fix that scales.

**Approach:**
1. Compute the gap. Observed mean 4.3 among rated titles versus 3.6 from a random prompt: 0.7 stars higher. With 1,000 users the sampling error of 3.6 is about 0.035 if each user gives one rating (a bit more if ratings are clustered by user), so the gap is not noise.
2. Name the mechanism. The chance of rating depends on the rating itself (people rate what they love or hate), so the data are missing not at random. Missing completely at random would give the same mean in both groups, and missing at random given observed covariates would be fixable with those covariates alone.
3. Say what it does to the model. A model trained only on observed ratings predicts too high for titles in general (a mean prediction near 4.1 in my run versus a true average near 3.6), and it ranks titles by what raters liked, not by what the average viewer would like. Titles that are watched but rarely rated look the same as unwatched ones.
4. Use the random probe as the anchor. It gives an unbiased distribution of ratings, and by comparing it with the observed distribution you can estimate how rating propensity varies with the star level, then weight observed rows by the inverse of that propensity (inverse propensity weighting).
5. Train with weights, or add a model of "was it rated" (a selection model), or use implicit feedback (watched, completed) as the main training signal, where exposure is known.
6. Evaluate on unbiased data: the random probe, a small randomised exposure test, or an online A/B test. Offline metrics on the observed ratings reward models that agree with the raters, which is the bias again.
7. Keep a standing randomised sample, and monitor the gap between observed and probe averages over time.

**Metrics:**
- Selection gap = observed mean rating - probe mean rating (4.3 - 3.6 = 0.7).
- Rating propensity by star = share of watched titles at that star level that get rated, relative to the overall rate (estimated as observed share / probe share, scaled by the overall 2%).
- Probe RMSE (or NDCG on probe items) of the model, versus RMSE on observed ratings.
- Guardrails: probe response rate, effective sample size after weighting (large weights inflate variance), and online metrics (watch time, retention).

**Risks:**
- Trusting the 4.3 or any model trained on it.
- Weights that explode: a rarely rated group gets a huge weight and the estimate gets noisy. Clip or stabilise weights.
- The probe is itself biased by non-response or by who sees the prompt.
- You cannot prove MNAR from the observed ratings alone; the random probe is the extra information that exposes it.
- Mixing up two selection steps: what users choose to watch (exposure, driven by the recommender) and what they choose to rate.

**What the interviewer scores:**
- Strong: calls it MNAR (rating depends on the rating), uses the random prompt as evidence, and explains the effect on both level and ranking.
- Strong: proposes inverse propensity weighting from a random sample, implicit feedback, and unbiased evaluation.
- Strong: notes weights need clipping and a check of effective sample size.
- Weak: "average rating is 4.3, so users like the catalogue", or "impute the missing ratings with the mean".
- Cross-reference: Book 6 Part 3 Q26 "An app sent a satisfaction survey to 250,000 users and 10,000 replied..." covers non-response bias in surveys, and Book 1 Part 7 has "Explain matrix factorization for recommendations. How is it trained (SGD vs ALS), why not treat missing entries as zeros, and what does the embedding size control?".

**Example:** (illustrative numbers) Suppose 100 watched titles with true ratings: 6 one-star, 10 two-star, 28 three-star, 30 four-star, 26 five-star (mean 3.6). People rate five-star titles 12.5 times as often as one-star ones (about 0.3% of one-star titles get rated against about 4% of five-star ones, which makes the overall rate about 2%). Rated titles then skew to four and five stars and the mean among rated titles is about 4.3. Weak answer: "the average rating is 4.3." Strong answer: "ratings are missing not at random; the random prompt says 3.6; weight by inverse propensity and evaluate on the probe."

**Code:**
```python
import numpy as np

rng = np.random.default_rng(39)
stars = np.arange(1, 6)
# true rating distribution among titles watched (invented), probability of rating given the star level (invented)
pmf = np.array([0.06, 0.10, 0.28, 0.30, 0.26]); p_rate = np.array([0.004, 0.006, 0.012, 0.025, 0.050]) * 0.81
true_mean = float((pmf * stars).sum())
rate_overall = float((pmf * p_rate).sum())
obs_pmf = pmf * p_rate / rate_overall
obs_mean = float((obs_pmf * stars).sum())
print("true mean among watched:", round(true_mean, 3), " rating rate:", round(rate_overall, 4), " mean among rated:", round(obs_mean, 3))
assert abs(true_mean - 3.6) < 0.05 and abs(rate_overall - 0.02) < 0.003 and abs(obs_mean - 4.3) < 0.05

# simulate: 200,000 users x 10 watched titles in the natural world; 1,000 users x 10 titles in the random prompt
n_nat = 2_000_000
r = rng.choice(stars, n_nat, p=pmf)
seen = rng.random(n_nat) < p_rate[r - 1]
print("natural ratings observed:", int(seen.sum()), " share:", round(float(seen.mean()), 4), " mean:", round(float(r[seen].mean()), 3))
n_probe = 10_000
rp = rng.choice(stars, n_probe, p=pmf)
print("random prompt: n =", n_probe, " mean:", round(float(rp.mean()), 3), " (se about", round(float(rp.std() / np.sqrt(n_probe)), 3), ")")

# the gap is selection, not noise: observed mean 4.3 vs probe 3.6
gap = r[seen].mean() - rp.mean()
assert gap > 0.6

# correct with inverse-propensity weights estimated from the probe: P(rated | star) is proportional to obs_pmf / probe_pmf
obs_counts = np.bincount(r[seen], minlength=6)[1:] / seen.sum()
probe_pmf = np.bincount(rp, minlength=6)[1:] / n_probe
w = probe_pmf / obs_counts                         # relative weight per star = 1 / relative propensity
ipw_mean = (w[r[seen] - 1] * r[seen]).sum() / w[r[seen] - 1].sum()
print("IPW-corrected mean of observed ratings:", round(float(ipw_mean), 3), "(probe", round(float(rp.mean()), 3), ")")
assert abs(ipw_mean - rp.mean()) < 0.05
print("weights per star (relative):", np.round(w / w[0], 2))

# a model trained on observed ratings only: item-level offset learned from observed mean; evaluate on probe
# (every title has a quality q; rating = clip(round(q + noise))); rating propensity rises with the star level
n_items = 500
q = rng.normal(3.6, 0.5, n_items)
def draw(items):
    return np.clip(np.rint(q[items] + rng.normal(0, 0.9, len(items))), 1, 5).astype(int)
watch_items = rng.integers(0, n_items, 3_000_000)
rating = draw(watch_items)
got = rng.random(len(watch_items)) < p_rate[rating - 1]
tr_i, tr_r = watch_items[got], rating[got]
mu_obs = np.array([tr_r[tr_i == i].mean() if (tr_i == i).any() else tr_r.mean() for i in range(n_items)])
probe_items = rng.integers(0, n_items, 20_000); probe_r = draw(probe_items)
pred = mu_obs[probe_items]
print("model trained on observed ratings: mean prediction on probe", round(float(pred.mean()), 3), " probe mean", round(float(probe_r.mean()), 3))
print("RMSE on observed ratings (last 20,000 rated rows, rated-only view):", round(float(np.sqrt(((mu_obs[tr_i[-20000:]] - tr_r[-20000:]) ** 2).mean())), 3),
      " RMSE on the random probe:", round(float(np.sqrt(((pred - probe_r) ** 2).mean())), 3))
assert pred.mean() - probe_r.mean() > 0.4
# fix: weight training rows by 1/propensity (star level) so training matches the probe; compare probe RMSE
probe_all = draw(rng.integers(0, n_items, 10_000))      # a random prompt, as in the scenario
pp = np.bincount(probe_all, minlength=6)[1:] / len(probe_all); oo = np.bincount(tr_r, minlength=6)[1:] / len(tr_r)
wt = (pp / oo)[tr_r - 1]                                # weights estimated from the probe, not from the hidden propensities
mu_w = np.array([(wt[tr_i == i] * tr_r[tr_i == i]).sum() / wt[tr_i == i].sum() if (tr_i == i).any() else tr_r.mean() for i in range(n_items)])
pw = mu_w[probe_items]
print("IPW model: mean prediction on probe", round(float(pw.mean()), 3), " RMSE on probe", round(float(np.sqrt(((pw - probe_r) ** 2).mean())), 3))
assert np.sqrt(((pw - probe_r) ** 2).mean()) < np.sqrt(((pred - probe_r) ** 2).mean())
```

**Output (my run):**
```text
true mean among watched: 3.6  rating rate: 0.02  mean among rated: 4.313
natural ratings observed: 40078  share: 0.02  mean: 4.308
random prompt: n = 10000  mean: 3.597  (se about 0.012 )
IPW-corrected mean of observed ratings: 3.597 (probe 3.597 )
weights per star (relative): [1.   0.7  0.34 0.17 0.08]
model trained on observed ratings: mean prediction on probe 4.075  probe mean 3.575
RMSE on observed ratings (last 20,000 rated rows, rated-only view): 0.76  RMSE on the random probe: 1.02
IPW model: mean prediction on probe 3.587  RMSE on probe 0.89
```
The text above matches this run: with the invented propensities the true mean is 3.6, the rating rate 2.0% and the mean among rated titles 4.313 (simulated 4.308). The random probe gives 3.597 (standard error about 0.012 for 10,000 ratings). Inverse propensity weights estimated from the probe bring the observed mean back to 3.597. A per-title model trained on the observed ratings predicts 4.075 on average for probe items against a probe mean of 3.575, and its RMSE is 0.76 on observed ratings but 1.02 on the random probe. With probe-estimated weights, the mean prediction is 3.587 and the probe RMSE falls to 0.89. The weighted model is better, not perfect, because each title has only a few ratings.

**Follow-ups:**
- Why not impute the missing ratings with the mean? The mean of observed ratings is biased high (4.3) and imputing it just copies the bias into the matrix; missing does not mean "average".
- Why is implicit feedback better? Watching, completing and re-watching are observed for most users, so exposure and engagement are known; they measure a different thing from stated ratings, but they are less self-selected.
- What if you have no random probe? Use a small randomised exposure test, instrumental signals such as prompt placement, or model the selection and report the result as an assumption-dependent estimate.

**Common mistakes:** Reporting 4.3 as the satisfaction level. Imputing missing ratings with the observed mean. Evaluating on the same biased ratings. Unclipped weights. Treating the probe as perfect.

### Q40 ⭐ 🔴 A team estimates that its crowd-sourced labels have asymmetric class-conditional noise: some true positives are labelled negative much more often than the reverse, and it has only 500 trusted labels. Explain how you would estimate the noise transition matrix, how you would use it to correct the loss, and where such correction breaks down.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
**Say this first (1 line):** I would estimate the 2x2 noise matrix by comparing crowd labels with the 500 trusted labels, put it into a forward-corrected loss so the model learns the true-class probabilities, and I would warn that it fixes calibration and thresholds more than ranking, and fails when the noise depends on the example.

**Clarifying questions:**
- Are the 500 trusted labels a random sample, or were they chosen (easy items, disputed items, one class)? Why: a chosen sample gives a biased matrix.
- How many of the 500 are true positives? Why: the rarer class is the one whose flip rate is estimated worst (164 positives in my run gives wide intervals).
- Do crowd workers differ a lot, and do items carry several labels? Why: with several labels per item you can estimate a confusion matrix per worker and aggregate, instead of one global matrix.
- Does noise depend on the item (blurry images, ambiguous text)? Why: a single class-level matrix assumes it does not.
- What does the model output get used for: ranking, a threshold, or probabilities? Why: it tells me whether the correction is worth the risk.

**Approach:**
1. Define the matrix. T[i][j] = P(crowd label = j | true class = i). For two classes it has two free numbers: the share of true positives labelled negative and the share of true negatives labelled positive. Rows sum to 1.
2. Estimate it from the trusted rows. Count how crowd labels fall within each trusted class: T[1][0] = true positives labelled negative / true positives. Give each cell an interval (the positive row has the fewest rows).
3. Reduce variance. If there are several crowd votes per item, fit a confusion matrix per annotator with a latent-class model (Dawid-Skene style) using the trusted labels as anchors. Or use anchor points: examples the model is very sure belong to each class can estimate T without trusted labels (needs good model calibration).
4. Correct the loss. Forward correction: let p be the model's class probabilities and q = p x T the probabilities of the noisy label; train with cross-entropy between the crowd label and q. The model then learns the clean probabilities p. Backward correction multiplies the vector of losses by the inverse of T instead (needs T invertible, can give negative losses).
5. Check it. Does the corrected model's predicted positive rate match the trusted rate? Compare the corrected model with a naive one and with a model trained on the 500 trusted rows alone, on a held-out clean test set. Also use trusted labels to fine-tune or to validate.
6. Know where it breaks (next section) and keep the trusted labels as the final judge. Prefer improving labels (a second pass on disputed items, better guidelines) where cheap.

**Metrics:**
- T[i][j] estimates with 95% intervals; the determinant of T (zero means the labels carry no information; near zero means unstable correction).
- Mean predicted positive probability versus the clean positive rate on a trusted test set (calibration).
- AUC and PR-AUC on the clean test set, plus precision and recall at the working threshold.
- Guardrails: stability of the model across different draws of the trusted set, and the size of the corrected-loss gradient (exploding values signal a bad T).

**Risks:**
- A rare positive row: with 164 true positives among 500 trusted rows, the flip rate of positives is known only to within a few points.
- Noise that depends on the example (hard positives lost more often): a single global matrix over-corrects easy items and under-corrects hard ones.
- Near-singular or wrongly estimated T: the corrected loss becomes unstable or biased.
- Trusted rows chosen non-randomly.
- Correcting the loss while the validation set is still crowd-labelled, so the benefit is invisible.

**What the interviewer scores:**
- Strong: defines T with the correct direction (true to noisy), estimates it from trusted labels with intervals, and writes the forward-corrected loss.
- Strong: says the correction mainly restores calibration and the threshold, and that ranking (AUC) barely changes.
- Strong: lists failure modes: instance-dependent noise, a poorly estimated or near-singular T, trusted-label sampling bias.
- Weak: "just remove the noisy labels" with no way to find them, or "use T without checking it".
- Cross-reference: Book 6 Part 3 Q34 "On a training set of 28,000 rows, a cross-validated model strongly disagrees with the given label..." for flagging and auditing noisy rows, and Book 1 Part 3 has "Positive-unlabeled learning and noisy labels: when negatives are really unlabeled, how does that change metrics and training?".

**Example:** (illustrative numbers) Of 500 trusted rows, 164 are positive and 336 negative. The crowd labelled 115 of the positives as positive and 49 as negative, and 326 of the negatives as negative and 10 as positive. Then T[1][0] = 49 / 164 = 0.299 and T[0][1] = 10 / 336 = 0.030. A model that outputs p = 0.60 for an item has noisy-label probability q1 = 0.60 x 0.70 + 0.40 x 0.03 = 0.432. Weak answer: "crowd labels are noisy, collect more." Strong answer: "estimate the flip rates from the trusted set, train with a forward-corrected loss, and validate on trusted labels."

**Code:**
```python
import numpy as np
from scipy.optimize import minimize
from scipy.stats import rankdata

rng = np.random.default_rng(40)
def auc(y, s):
    r = rankdata(s); n1 = int(y.sum()); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))
sig = lambda a: 1 / (1 + np.exp(-a))

n = 30_000
X = rng.normal(size=(n, 4)); w_true = np.array([1.2, -0.8, 0.6, 0.0])
y = (rng.random(n) < sig(X @ w_true - 1.0)).astype(int)                     # about 30% positive
# T[i][j] = P(noisy label = j | true class = i): positives are lost far more often than negatives are invented
T = np.array([[0.96, 0.04], [0.30, 0.70]])
noisy = np.where(rng.random(n) < T[y, 1], 1, 0)
print("true positive rate:", round(float(y.mean()), 3), " noisy positive rate:", round(float(noisy.mean()), 3))

# 1) estimate T from 500 trusted labels (a random 500 rows that also have a crowd label)
trusted = rng.choice(n, 500, replace=False)
yt, nt = y[trusted], noisy[trusted]
That = np.array([[np.mean(nt[yt == i] == j) for j in (0, 1)] for i in (0, 1)])
print("trusted rows: positives", int((yt == 1).sum()), " negatives", int((yt == 0).sum()))
print("estimated T:\n", np.round(That, 3), "\ntrue T:\n", T)
# how stable? re-draw 500 trusted rows 300 times
est = []
for _ in range(300):
    idx = rng.choice(n, 500, replace=False); a, b = y[idx], noisy[idx]
    est.append([b[a == 1].__eq__(0).mean(), b[a == 0].__eq__(1).mean()])
est = np.array(est)
print("sd of P(noisy=0|true=1):", round(float(est[:, 0].std()), 3), "  sd of P(noisy=1|true=0):", round(float(est[:, 1].std()), 3))
assert est[:, 0].std() > 2 * est[:, 1].std()               # the rare class is the poorly estimated one

# 2) train three logistic models: naive on noisy, forward-corrected loss with estimated T, and trusted-only
F = np.c_[X, np.ones(n)]
tr = np.arange(n) < 20_000; te = ~tr
def nll_plain(w, F, t): p = np.clip(sig(F @ w), 1e-9, 1 - 1e-9); return -np.mean(t * np.log(p) + (1 - t) * np.log(1 - p))
def nll_forward(w, F, t, Tm):
    p1 = sig(F @ w)
    q1 = np.clip(p1 * Tm[1, 1] + (1 - p1) * Tm[0, 1], 1e-9, 1 - 1e-9)    # P(noisy label = 1 | x) = sum_i P(y=i|x) T[i,1]
    return -np.mean(t * np.log(q1) + (1 - t) * np.log(1 - q1))
def run(fun, *args):
    return minimize(fun, np.zeros(F.shape[1]), args=args, method="L-BFGS-B").x
w_naive = run(nll_plain, F[tr], noisy[tr])
w_fwd = run(nll_forward, F[tr], noisy[tr], That)
w_fwd_true = run(nll_forward, F[tr], noisy[tr], T)
tt = np.intersect1d(trusted, np.where(tr)[0])
w_trust = run(nll_plain, F[trusted], y[trusted])                              # 500 clean rows only
def report(name, w):
    s = F[te] @ w
    print(f"{name:34s} AUC {auc(y[te], s):.4f}   mean predicted P(y=1) {sig(s).mean():.3f} (truth {y[te].mean():.3f})")
    return sig(s).mean()
m_n = report("naive on noisy labels", w_naive)
m_f = report("forward-corrected, T estimated", w_fwd)
m_t = report("forward-corrected, T true", w_fwd_true)
m_c = report("trusted 500 only", w_trust)
assert abs(m_f - y[te].mean()) < abs(m_n - y[te].mean())

# 3) where it breaks: (a) instance-dependent noise (hard positives lost more), (b) near-singular T
hard = X[:, 0] < 0
noisy_id = np.where(rng.random(n) < np.where(y == 1, np.where(hard, 0.55, 0.12), 0.04), 1 - y, y)
rate_hard = (noisy_id[y == 1][hard[y == 1]] == 0).mean(); rate_easy = (noisy_id[y == 1][~hard[y == 1]] == 0).mean()
print("instance-dependent noise: positives lost, hard", round(float(rate_hard), 3), " easy", round(float(rate_easy), 3))
T_glob = np.array([[0.96, 0.04], [0.30, 0.70]])
w_id = run(nll_forward, F[tr], noisy_id[tr], T_glob)
w_id_n = run(nll_plain, F[tr], noisy_id[tr])
print("instance-dependent: AUC naive", round(float(auc(y[te], F[te] @ w_id_n)), 4), " corrected with one global T", round(float(auc(y[te], F[te] @ w_id)), 4))
print("determinant of T (0 means labels carry no information):", round(float(np.linalg.det(T)), 3), " if T=[[.8,.2],[.55,.45]]:", round(float(np.linalg.det(np.array([[.8, .2], [.55, .45]]))), 3))
```

**Output (my run):**
```text
true positive rate: 0.329  noisy positive rate: 0.258
trusted rows: positives 164  negatives 336
estimated T:
 [[0.97  0.03 ]
 [0.299 0.701]] 
true T:
 [[0.96 0.04]
 [0.3  0.7 ]]
sd of P(noisy=0|true=1): 0.037   sd of P(noisy=1|true=0): 0.01
naive on noisy labels              AUC 0.8196   mean predicted P(y=1) 0.255 (truth 0.324)
forward-corrected, T estimated     AUC 0.8196   mean predicted P(y=1) 0.335 (truth 0.324)
forward-corrected, T true          AUC 0.8196   mean predicted P(y=1) 0.326 (truth 0.324)
trusted 500 only                   AUC 0.8188   mean predicted P(y=1) 0.310 (truth 0.324)
instance-dependent noise: positives lost, hard 0.556  easy 0.119
instance-dependent: AUC naive 0.8146  corrected with one global T 0.8137
determinant of T (0 means labels carry no information): 0.66  if T=[[.8,.2],[.55,.45]]: 0.25
```
The text above matches this run: the true positive rate is 32.9% but the crowd labels show 25.8%. The 500 trusted rows contain 164 positives and 336 negatives and give T[1][0] = 0.299 and T[0][1] = 0.03 against true 0.30 and 0.04. Across 300 redraws, the standard deviation of the positive-row flip rate is 0.037 against 0.010 for the negative row, so the rare class is the poorly known one. AUC is 0.8196 for the naive, forward-corrected (estimated T) and forward-corrected (true T) models, so ranking does not change, but the mean predicted positive probability is 0.255 for the naive model (truth 0.324), 0.335 with the estimated T and 0.326 with the true T. The model trained on the 500 trusted rows alone gets AUC 0.8188 and a mean of 0.310, which for a simple four-feature model is a serious competitor. When noise depends on the example (positives lost 0.556 of the time on hard items, 0.119 on easy ones), correcting with one global T does not help: AUC 0.8137 against 0.8146 for the naive model. The determinant of T is 0.66 here; for T = [[0.8, 0.2], [0.55, 0.45]] it is 0.25, closer to the point where labels carry no information.

**Follow-ups:**
- Forward or backward correction? Forward correction keeps the loss a valid cross-entropy and is more stable; backward correction needs the inverse of T and can produce negative loss values.
- Can you estimate T without any trusted labels? Under assumptions (anchor points, a good clean-ish model), yes, but check against the trusted labels when you have them.
- Would you rather spend the effort on cleaning? Often yes. A second review of the disputed items, or relabelling the most uncertain 1,000 rows, usually beats a clever loss when the noise is instance-dependent.

**Common mistakes:** Mixing up the direction of T (true to noisy, not noisy to true). Estimating T from a non-random trusted sample. Ignoring the interval for the rare class. Expecting AUC to rise. Using one global T for example-dependent noise. Validating on crowd labels.
