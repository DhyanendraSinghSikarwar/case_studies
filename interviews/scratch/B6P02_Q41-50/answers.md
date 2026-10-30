### Q41 ⭐ 🔴 A classifier had a validation true-positive rate of 80% and a false-positive rate of 10%. In production without labels it flags 29% of cases as positive, where at training the positive rate was 20%. Explain how you would estimate the production prior under a label-shift assumption using the confusion-matrix approach, state the estimate, and say how you would then adjust the threshold or the model.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
**Say this first (1 line):** If only the share of positives changed, the flag rate is a known mix of the true-positive and false-positive rates, so I solve 0.29 = pi x 0.80 + (1 - pi) x 0.10 and get pi = 0.19 / 0.70 = 27.1%, then I correct the threshold for that new prior.

**Clarifying questions:**
- Are the 80% TPR and 10% FPR measured on a validation set whose positive share is the 20% training prior? Why: TPR and FPR do not depend on the prior, but only if they were measured per class.
- Is the 29% a share of cases at the same threshold as validation? Why: a different cut gives a different TPR and FPR pair.
- What changed in the world (new channel, new region, a campaign)? Why: label shift assumes only the class mix moved. If the features of each class also moved, the formula is wrong.
- How many production cases is the 29% based on? Why: it sets the width of the interval around the estimate.
- Is the score calibrated? Why: it decides whether I move the threshold with the odds correction or have to recalibrate.
- Can I get a small random labelled sample now? Why: it is the only direct check of the estimate.

**Approach:**
1. Name the assumption: label shift, meaning P(y) moves and P(x | y) does not. Then the classifier's TPR and FPR stay at 0.80 and 0.10.
2. Write the flag rate as a mix: q = pi x TPR + (1 - pi) x FPR. Solve: pi = (q - FPR) / (TPR - FPR) = (0.29 - 0.10) / 0.70 = 0.271.
3. Sanity check: at the training prior 0.20 I would expect 0.20 x 0.80 + 0.80 x 0.10 = 24% flagged. I see 29%, so the extra 5 points of flags are the shift. The 20% in the prompt is the prior, not the training flag rate, so I do not compare 29% with 20%.
4. Put an interval on it. With 10,000 cases the flag rate has a standard error of 0.45 points, and dividing by TPR - FPR = 0.70 gives about 0.65 points on the prior.
5. Adjust the decisions. For a calibrated model, multiply the odds by w = (0.271 / 0.729) / (0.20 / 0.80) = 1.49. A 0.50 cut on the adjusted probability equals a 0.40 cut on the old probability.
6. Check the assumption: if I can get even a few hundred random labels, compare the estimate with the sample, and check feature drift within each predicted class.

**Metrics:**
- Estimated prior pi = (q - FPR) / (TPR - FPR); q = flagged cases / all scored cases.
- Precision at the new prior = pi x TPR / q. Recall stays at TPR under this assumption.
- Odds multiplier w = [pi / (1 - pi)] / [pi0 / (1 - pi0)].
- Guardrails: the formula needs TPR > FPR, the interval around pi, and a check that the estimate is between 0 and 1.

**Risks:**
- The formula assumes P(x | y) is unchanged. If the false-positive rate also drifted, the estimate is biased (see the code: FPR 0.14 would give 31%).
- A noisy TPR - FPR in the denominator magnifies noise when the classifier is weak.
- Treating 29% as the new prior by itself ignores that part of the 29% is false positives.
- Moving the threshold on an uncalibrated score.

**What the interviewer scores:**
- Strong: writes the mixing equation and solves it by hand; states the label-shift assumption out loud.
- Strong: separates "estimate the prior" from "change the decision", and gives an interval.
- Strong: says what breaks the method and how to check it with a small random label sample.
- Weak: "the positive rate went from 20% to 29%", reading the flag rate as the prior.
- Weak: retrains first without asking whether the classes changed or only their mix.

**Example:** (illustrative numbers) TPR 0.80, FPR 0.10, flag rate 0.29. pi = 0.19 / 0.70 = 0.271. Precision was 0.20 x 0.80 / 0.24 = 66.7% at the old prior and is 0.271 x 0.80 / 0.29 = 74.9% now, so the model is not worse, the cases are more often positive. Weak answer: "29% are positive now." Strong answer: "About 27%, give or take a point; I would adjust the odds by 1.49 and verify on a small random labelled sample."

**Code:**
```python
# Q41: label-shift estimate (confusion-matrix / BBSE style). Illustrative numbers.
import numpy as np
tpr, fpr = 0.80, 0.10
flag_rate = 0.29          # production share flagged positive (no labels)
train_prior = 0.20

# flag_rate = pi*TPR + (1-pi)*FPR  ->  pi = (flag_rate - FPR) / (TPR - FPR)
pi = (flag_rate - fpr) / (tpr - fpr)
print(f"estimated production prior = {pi:.4f}")
assert abs(pi - 0.19/0.70) < 1e-12 and round(pi, 3) == 0.271

# naive reading would say 29% positive; flag rate at the training prior would have been:
exp_flag_train = train_prior*tpr + (1-train_prior)*fpr
print(f"expected flag rate at prior 0.20 = {exp_flag_train:.3f} (observed {flag_rate})")
assert abs(exp_flag_train - 0.24) < 1e-12

# precision before and after the shift (TPR, FPR assumed unchanged)
prec_old = train_prior*tpr/exp_flag_train
prec_new = pi*tpr/flag_rate
print(f"precision at prior 0.20 = {prec_old:.3f}, at prior {pi:.3f} = {prec_new:.3f}")
assert round(prec_old, 3) == 0.667 and round(prec_new, 3) == 0.749

# prior-odds correction for calibrated probabilities
w = (pi/(1-pi)) / (train_prior/(1-train_prior))
print(f"odds multiplier w = {w:.3f}")
assert round(w, 3) == 1.490
t_old = 0.5
# adjusted p' = p*w/(p*w+1-p); p' >= 0.5  <=>  p >= 1/(1+w)
t_equiv = 1/(1+w)
print(f"a 0.50 cut on adjusted probability = {t_equiv:.3f} on the old probability")
assert round(t_equiv, 3) == 0.402
p = t_equiv; assert abs(p*w/(p*w+1-p) - 0.5) < 1e-12

# uncertainty: n production cases, bootstrap of the flag rate
rng = np.random.default_rng(41)
n = 10_000
flags = rng.random(n) < flag_rate
boots = []
for _ in range(2000):
    fr = rng.choice(flags, n).mean()
    boots.append((fr - fpr)/(tpr - fpr))
lo, hi = np.percentile(boots, [2.5, 97.5])
print(f"n={n}: prior 95% interval ({lo:.3f}, {hi:.3f})")
se = np.sqrt(flag_rate*(1-flag_rate)/n)/(tpr-fpr)
print(f"analytic SE = {se:.4f}")
assert 0.0055 < se < 0.0075 and lo < 0.271 < hi

# check the method on simulated data where we know the truth (true prior 0.2714)
true_pi = 0.19/0.70
y = rng.random(200_000) < true_pi
pred = np.where(y, rng.random(y.size) < tpr, rng.random(y.size) < fpr)
est = (pred.mean() - fpr)/(tpr - fpr)
print(f"simulation: flag rate {pred.mean():.3f}, estimate {est:.3f}, truth {true_pi:.3f}")
assert abs(est - true_pi) < 0.01
# if the class-conditionals also moved, the estimate is wrong: FPR drifts to 0.14
pred2 = np.where(y, rng.random(y.size) < tpr, rng.random(y.size) < 0.14)
est2 = (pred2.mean() - fpr)/(tpr - fpr)
print(f"with FPR secretly 0.14 the same formula says {est2:.3f} (truth {true_pi:.3f})")
assert est2 > true_pi + 0.04
```

**Output (my run):**
```text
estimated production prior = 0.2714
expected flag rate at prior 0.20 = 0.240 (observed 0.29)
precision at prior 0.20 = 0.667, at prior 0.271 = 0.749
odds multiplier w = 1.490
a 0.50 cut on adjusted probability = 0.402 on the old probability
n=10000: prior 95% interval (0.262, 0.288)
analytic SE = 0.0065
simulation: flag rate 0.291, estimate 0.273, truth 0.271
with FPR secretly 0.14 the same formula says 0.312 (truth 0.271)
```

**Follow-ups:**
- What if the model is not calibrated? Recalibrate first on recent labels, or fit the new prior with an EM step on the scores; the odds multiplier is only right for calibrated probabilities.
- Why not retrain? Label shift changes the prior, not the relationship, so a threshold or odds correction is cheaper and reversible. See also Q9 in this part (precision fell because the fraud rate fell).

**Common mistakes:** Reading the flag rate as the prior. Forgetting that false positives are part of the 29%. No uncertainty on the estimate. Applying the method when the features themselves moved. Moving the cut on uncalibrated scores.

### Q42 ⭐ 🔴 A model's accuracy loses roughly 0.3 percentage points each week after training, each percentage point is worth about Rs 4 lakh per week, and a retrain costs Rs 6 lakh. Explain how you would model the cost of decay against the cost of retraining to choose a cadence, show the rough optimum, and name the assumptions (linear decay, constant stakes) that would break it.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
**Say this first (1 line):** Add the cost of retraining to the cost of running an ageing model, divide by the cycle length, and pick the cadence that minimises cost per week; with these numbers that is about every 3 weeks, costing roughly Rs 3.8 lakh a week.

**Clarifying questions:**
- Does a retrain restore the fresh accuracy, or does it only catch part of the drop? Why: a partial reset shifts the optimum.
- Is the Rs 6 lakh all-in (compute, review, deployment, risk of a bad release)? Why: people time and incident risk are often left out.
- Is the 0.3 pp per week measured or assumed? Why: the whole answer rests on that slope.
- Is the Rs 4 lakh per point constant through the year? Why: festival weeks multiply the stakes.
- Can retraining be automated at low marginal cost? Why: cheap retraining shortens the optimal cycle.

**Approach:**
1. Loss rate: 0.3 pp per week x Rs 4 lakh per pp = Rs 1.2 lakh per week for each week of model age. Call it k.
2. In a cycle of T weeks, week j has average age j - 0.5, so decay cost = k x (0.5 + 1.5 + ... ) = k x T^2 / 2 = 0.6 T^2.
3. Cost per cycle = 6 + 0.6 T^2. Cost per week = 6 / T + 0.6 T.
4. Minimise: the two terms are equal when T = sqrt(6 / 0.6) = sqrt(10) = 3.16 weeks. Minimum cost = 2 x sqrt(6 x 0.6) = Rs 3.79 lakh per week.
5. Round to whole weeks: 3 weeks gives 3.80, 4 weeks gives 3.90, 2 weeks gives 4.20. The curve is flat near the minimum, so 3 to 4 weeks is fine; do not argue about decimals.
6. Turn it into a rule: retrain when the accumulated loss since the last retrain reaches the retrain cost, as a trigger, rather than by the calendar alone.

**Metrics:**
- Cost per week = (retrain cost + sum of decay losses in the cycle) / T.
- Decay loss in week j = k x (j - 0.5) with k = slope in pp per week x value per pp.
- Guardrails: accuracy floor, validation pass on each retrain, and the observed decay slope tracked monthly.

**Risks:**
- Decay is rarely linear: a shock (new product, outage) causes a step, so a monitored trigger beats a fixed cadence.
- Constant stakes: festival season makes k bigger; T* scales as 1 / sqrt(k), so doubling the stakes shortens the cycle by 1.41 times (to 2.2 weeks).
- Retrain cost is not flat: a 4x cost doubles the cycle (to 6.3 weeks).
- Each retrain has a risk of a worse model; that is a cost term I have left out of the Rs 6 lakh.
- The decay slope may be an artefact of label delay (see Q28 in this part).

**What the interviewer scores:**
- Strong: writes the cost per week and solves for T analytically, then rounds.
- Strong: states the assumptions and how each moves the answer (square-root rule).
- Strong: converts the optimum into a trigger.
- Weak: "retrain weekly to be safe" with no cost comparison.
- Weak: mixes up the cost per cycle and per week.

**Example:** (illustrative numbers) Retrain every 3 weeks: cost = (6 + 1.2 x (0.5 + 1.5 + 2.5)) / 3 = (6 + 5.4) / 3 = Rs 3.80 lakh per week. Every 4 weeks: (6 + 9.6) / 4 = 3.90. Every week: 6.60. Never retraining for 26 weeks averages Rs 15.6 lakh per week. Weak answer: "retrain as often as possible". Strong answer: "About every 3 to 4 weeks, and sooner if the measured decay speeds up."

**Code:**
```python
# Q42: retrain cadence from decay cost vs retrain cost. Illustrative numbers.
import numpy as np
decay_pp_per_week = 0.3
value_per_pp = 4.0      # Rs lakh per week per percentage point
retrain_cost = 6.0      # Rs lakh per retrain

k = decay_pp_per_week*value_per_pp          # loss rate grows 1.2 lakh/week each week
print(f"loss grows by Rs {k:.1f} lakh per week, per week of age")
assert abs(k - 1.2) < 1e-12

def avg_cost(T):
    # week j of a cycle is j-0.5 weeks old on average, loss = k*(j-0.5); sum_{j=1..T} = k*T^2/2
    weeks = np.arange(1, T+1)
    decay = (k*(weeks-0.5)).sum()
    assert abs(decay - k*T*T/2) < 1e-9
    return (retrain_cost + decay)/T

for T in range(1, 9):
    print(f"retrain every {T} wk: Rs {avg_cost(T):.2f} lakh/week")
best = min(range(1, 13), key=avg_cost)
T_star = (2*retrain_cost/k)**0.5
c_star = (2*retrain_cost*k)**0.5
print(f"continuous optimum T* = sqrt(2R/k) = {T_star:.2f} weeks, cost {c_star:.2f} lakh/week")
assert best == 3 and abs(T_star - 3.162) < 0.001 and abs(c_star - 3.795) < 0.001
assert round(avg_cost(3), 2) == 3.80 and round(avg_cost(4), 2) == 3.90 and round(avg_cost(2), 2) == 4.20

# never retraining: loss grows without bound; after 26 weeks
print(f"never retrain, week 26: loss that week Rs {k*25.5:.1f} lakh; average over 26 wk Rs {k*26/2:.1f} lakh/week")
assert abs(k*26/2 - 15.6) < 1e-9

# assumption breaks: decay is not linear, e.g. a step at week 5 after a shock
def cost_step(T, step_week=5, step_pp=2.0):
    w = np.arange(1, T+1)-0.5
    loss = k*w + np.where(w > step_week, step_pp*value_per_pp, 0.0)
    return (retrain_cost + loss.sum())/T
bestS = min(range(1, 13), key=cost_step)
print("with an extra 2 pp step after week 5, best cadence (whole weeks):", bestS,
      f"cost {cost_step(bestS):.2f}")
# stakes double (e.g. festival season): value_per_pp 8 -> T* shrinks by sqrt(2)
k2 = decay_pp_per_week*8.0
print(f"stakes double: T* = {(2*retrain_cost/k2)**0.5:.2f} weeks")
assert abs((2*retrain_cost/k2)**0.5 - T_star/2**0.5) < 1e-9
# cost rises 4x if retrain costs 24: T* doubles
print(f"retrain cost 4x: T* = {(2*24/k)**0.5:.2f} weeks")
assert abs((2*24/k)**0.5 - 2*T_star) < 1e-9
# slope uncertainty: 0.2 and 0.4 pp per week
for slope in (0.2, 0.4):
    kk = slope*value_per_pp
    print(f"slope {slope} pp/week: T* = {(2*retrain_cost/kk)**0.5:.2f} weeks")
assert abs((2*retrain_cost/(0.2*4))**0.5 - 3.873) < 0.001 and abs((2*retrain_cost/(0.4*4))**0.5 - 2.739) < 0.001
```

**Output (my run):**
```text
loss grows by Rs 1.2 lakh per week, per week of age
retrain every 1 wk: Rs 6.60 lakh/week
retrain every 2 wk: Rs 4.20 lakh/week
retrain every 3 wk: Rs 3.80 lakh/week
retrain every 4 wk: Rs 3.90 lakh/week
retrain every 5 wk: Rs 4.20 lakh/week
retrain every 6 wk: Rs 4.60 lakh/week
retrain every 7 wk: Rs 5.06 lakh/week
retrain every 8 wk: Rs 5.55 lakh/week
continuous optimum T* = sqrt(2R/k) = 3.16 weeks, cost 3.79 lakh/week
never retrain, week 26: loss that week Rs 30.6 lakh; average over 26 wk Rs 15.6 lakh/week
with an extra 2 pp step after week 5, best cadence (whole weeks): 3 cost 3.80
stakes double: T* = 2.24 weeks
retrain cost 4x: T* = 6.32 weeks
slope 0.2 pp/week: T* = 3.87 weeks
slope 0.4 pp/week: T* = 2.74 weeks
```

**Follow-ups:**
- What if decay is concave (fast at first, then slows)? The optimum moves later, because early weeks cost most; fit the real curve from backtests.
- How would you handle uncertainty in the slope? Take a range such as 0.2 to 0.4 pp; T* moves by the square root of the slope: 0.2 pp gives 3.9 weeks and 0.4 pp gives 2.7 weeks, so the cadence stays between about 3 and 4 weeks.

**Common mistakes:** Forgetting the retrain cost is paid every cycle. Using end-of-cycle age instead of average age. Treating the optimum as exact. Ignoring step changes. Assuming a retrain always restores full accuracy.

### Q43 ⭐ 🔴 After a credit-scoring model was published and people learned what moves the score, applicants began gaming a few features and the score lost power. Explain this as performativity or Goodhart's law, how you would detect it, what features and monitoring are more robust, and how model transparency trades off against gaming risk.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** Once the score is used to decide things about people, people change the inputs to move the score, so the feature stops measuring what it measured (Goodhart's law); I detect it from shifts in the gameable features and a weaker link to outcomes, and I lean on features that are costly to fake.

**Clarifying questions:**
- Which features are public or easy to change, and at what cost to the applicant? Why: gameability is about cost, not visibility.
- Was the scoring logic or feature list published, or only inferred? Why: it decides how fast and how widely gaming spreads.
- Do we get outcome labels for the people who gamed? Why: without outcomes I can only see the inputs shift, not the loss of power.
- Is there a legal duty to give reasons for decisions? Why: transparency may be required, so I design around it instead of removing it.
- What does it cost the lender when the model is gamed (default loss) versus when it blocks good applicants? Why: it sets how defensive to be.

**Approach:**
1. Name it: the model is performative. Publishing it changes behaviour, so the data it later learns from is no longer the data it was built on. Goodhart: a measure that becomes a target stops being a good measure.
2. Detect from inputs: for each feature track its distribution, the share of values at "good-looking" edges, and the gap between a gameable feature and a hard-to-fake one for the same person (declared balance versus repayment history).
3. Detect from outcomes: the feature's correlation with default (or its coefficient) weakens as the cohort matures, while the score improves. A better score with worse realised defaults is the signature.
4. Respond: shift weight to features that are costly or slow to fake (verified repayment history, bureau data, cash-flow from bank statements), cap the influence of any single gameable feature, use monotone constraints and rate-of-change checks.
5. Keep a refresh rhythm and a holdout of unpublished signals, so a model that is attacked can be replaced quickly.
6. Transparency: explain reasons at the level the law needs, but not the weights; give actionable reasons that match real creditworthiness (improving them helps both sides), and use human review for edge cases.

**Metrics:**
- Per-feature PSI against the pre-publication distribution; share of applicants at a threshold edge.
- Feature-outcome link: correlation or AUC of that feature alone, by cohort month.
- Gap statistic: mean(gameable feature standardised - hard feature standardised).
- Guardrails: approval rate, default rate on matured loans, and complaint rate.

**Risks:**
- Defaults are labelled months later, so outcome evidence is slow; the input signals come first.
- Dropping a useful feature because a few people game it loses real signal.
- Hiding everything harms fairness and trust; publishing everything invites gaming.
- Tighter rules push applicants to new tricks; it is an ongoing contest.

**What the interviewer scores:**
- Strong: gives the mechanism (feedback from the score to the inputs) and both input-side and outcome-side detection.
- Strong: picks robust features by cost to fake and states the trade-off with transparency.
- Strong: notes label delay and says what to watch before labels arrive.
- Weak: "retrain on new data" (that trains on the gamed data).
- Weak: "make the model a secret", ignoring explanation duties.

**Example:** (illustrative simulation) The model's AUC for predicting default was 0.791 with two features. After 60% of applicants inflate the cheap feature, it falls to 0.705. A model on the hard-to-fake feature alone had 0.727 before and 0.730 after: weaker on day one, but it does not decay, and it wins once gaming is heavy enough. The cheap feature's mean moved from -0.01 to 1.49 and its link to default weakened (correlation -0.395 to -0.255). Weak answer: "retrain it." Strong answer: "Watch the gameable inputs and their link to outcomes, and move weight to costly-to-fake signals."

**Code:**
```python
# Q43: gaming of a published scorecard. Illustrative simulation.
import numpy as np
from scipy.optimize import minimize
from scipy.stats import rankdata
rng = np.random.default_rng(43)
n = 40_000
risk = rng.normal(size=n)                       # latent creditworthiness
default = rng.random(n) < 1/(1+np.exp(2.0 + 1.5*risk))   # higher risk value -> fewer defaults
# features: x_hard is costly to fake (repayment history), x_easy is cheap to fake (declared balance)
x_hard = risk + rng.normal(0, 1.0, n)
x_easy = risk + rng.normal(0, 0.5, n)
def feats(xh, xe): return np.column_stack([np.ones(len(xh)), xh, xe])

def fit(X, y):
    def nll(b):
        z = X@b
        return np.mean(np.logaddexp(0, z) - y*z)
    return minimize(nll, np.zeros(X.shape[1]), method="BFGS").x
def auc(score, y):   # AUC for predicting y=1
    r = rankdata(score); n1 = y.sum(); n0 = len(y)-n1
    return (r[y == 1].sum() - n1*(n1+1)/2)/(n1*n0)

b_full = fit(feats(x_hard, x_easy), default.astype(float))
b_hard = fit(feats(x_hard, np.zeros(n))[:, :2], default.astype(float))
print("weights full model (const, hard, easy):", np.round(b_full, 2))

# after publication: 60% of applicants inflate the easy feature (the model reads them as safer)
m = 40_000
risk2 = rng.normal(size=m)
d2 = rng.random(m) < 1/(1+np.exp(2.0 + 1.5*risk2))
xh2 = risk2 + rng.normal(0, 1.0, m)
xe2 = risk2 + rng.normal(0, 0.5, m)
gamers = rng.random(m) < 0.6
xe2_g = xe2 + gamers*rng.uniform(1.5, 3.5, m)    # inflation unrelated to true risk
before = auc(feats(x_hard, x_easy)@b_full, default.astype(int))
after = auc(feats(xh2, xe2_g)@b_full, d2.astype(int))
hard_only_after = auc(feats(xh2, xe2_g)[:, :2]@b_hard[:2], d2.astype(int))
hard_only_before = auc(feats(x_hard, x_easy)[:, :2]@b_hard[:2], default.astype(int))
print(f"full model AUC before {before:.3f} after gaming {after:.3f}")
print(f"hard-feature-only model AUC before {hard_only_before:.3f} after {hard_only_after:.3f}")
assert after < before - 0.03
assert hard_only_before < before        # robustness costs some power today
assert abs(hard_only_after - hard_only_before) < 0.01   # but it does not decay
assert hard_only_after > after            # and wins once gaming starts

# detection: the easy feature's distribution moves and its link to the outcome weakens
print(f"mean easy feature before {x_easy.mean():.2f}, after {xe2_g.mean():.2f}")
corr_b = np.corrcoef(x_easy, default)[0, 1]; corr_a = np.corrcoef(xe2_g, d2)[0, 1]
print(f"corr(easy, default) before {corr_b:.3f}, after {corr_a:.3f}")
assert xe2_g.mean() > x_easy.mean() + 0.5 and abs(corr_a) < abs(corr_b)
# gap between easy and hard features: gamers show easy >> hard
gap_b = (x_easy - x_hard).mean(); gap_a = (xe2_g - xh2).mean()
print(f"mean(easy - hard) before {gap_b:.2f}, after {gap_a:.2f}")
assert gap_a > gap_b + 0.5
```

**Output (my run):**
```text
weights full model (const, hard, easy): [-1.87 -0.24 -0.92]
full model AUC before 0.791 after gaming 0.705
hard-feature-only model AUC before 0.727 after 0.730
mean easy feature before -0.01, after 1.49
corr(easy, default) before -0.395, after -0.255
mean(easy - hard) before -0.00, after 1.49
```

**Follow-ups:**
- Is all gaming bad? No. If changing the feature really reduces risk (paying bills on time), gaming it helps. The problem is features that can be changed without changing risk.
- Related question in this part: Q38 (selection bias in monitoring labels) matters here too, since rejected applicants have no outcomes.

**Common mistakes:** Retraining directly on gamed data. Treating a better score as better performance. Assuming secrecy fixes it. Dropping every visible feature. Forgetting that outcomes arrive late.

### Q44 ⭐ 🔴 A shared embedding model was upgraded by the platform team, and three downstream models that consume its vectors each lost between 2 and 6 points of accuracy without any code change of their own. Explain the dependency chain problem, how you would detect it, and what versioning, contracts and canary practices the platform team should adopt.
**Asked at:** Upstream schema and silent feature-pipeline failure write-ups (Towards AI schema-migration post, RisingWave feature-pipeline observability, ActiveWizards Kafka schema-evolution post, dataexpert.io schema-drift post); practitioner posts rather than interview banks, so scenario is editor-designed; search snippets only, not opened
**Say this first (1 line):** The three models depend on the exact coordinate system of the old embedding, so a new embedding model silently changes what every input number means; I would detect it with a per-consumer regression check on a frozen set, and ask the platform team for versioned embeddings, contracts and a staged rollout.

**Clarifying questions:**
- Did the platform team replace vectors in place, or serve both versions? Why: in-place means every consumer changed on the same day.
- Did the dimension, normalisation or tokenisation change? Why: a shape change fails loudly, while a same-shape change fails silently.
- Are the three models fine-tuned on the old vectors, or do they use them as frozen inputs? Why: it decides whether a quick fix (alignment) or a retrain is needed.
- Who owns the frozen evaluation sets? Why: without consumer-owned tests, nobody sees the loss.
- Can I get a paired sample of the same items in both spaces? Why: pairs allow a cheap alignment fix.

**Approach:**
1. Frame the dependency chain: platform embedding -> feature store -> three models -> products. The platform team tested the embedding on its own benchmark and called it better. Consumers were never in that test.
2. Confirm the cause: re-score a frozen validation set using the old vectors and the new vectors, with the same model. If accuracy drops only with the new vectors, the embedding is the cause. Check the vector statistics too (norm, mean, cosine to the old vector for the same item).
3. Contain: pin the old embedding version for the three consumers (roll back the dependency, not the consumer code).
4. Repair: retrain each consumer on the new vectors, or learn a small alignment map from paired items (orthogonal Procrustes) as a bridge while retraining.
5. Prevent it: versioned embeddings with a version tag stored with every vector, side-by-side serving for a deprecation window, a compatibility contract (dimension, normalisation, a published cosine-similarity-to-previous report), and a canary with per-consumer gates.
6. Process: consumers register a frozen test with the platform team; an upgrade can only be promoted if every registered consumer stays within an agreed tolerance, for example 1 point.

**Metrics:**
- Per-consumer accuracy delta on a frozen set = accuracy(new vectors) - accuracy(old vectors).
- Mean cosine similarity between old and new vectors for the same items.
- Gate: block promotion if any consumer's delta is below -1 point.
- Guardrail: share of traffic on each embedding version.

**Risks:**
- Averaging across consumers hides one badly hit model.
- The old space may not be reproducible later if the old model is deleted; keep it.
- An alignment map only works if the new space is roughly a linear transformation of the old one.
- Mixing versions in one index is a separate failure (see Q23 in this part).

**What the interviewer scores:**
- Strong: describes this as an interface change with no interface contract.
- Strong: re-scores with old versus new vectors to isolate the cause.
- Strong: proposes consumer-owned tests, version tags and staged rollout, not "be careful".
- Weak: debugging each downstream model separately.
- Weak: blames the platform team without a process fix.

**Example:** (illustrative simulation) A consumer scores 85.6% accuracy on the old vectors. If the new space is a rotation of the old one by 0.4 (arbitrary units), the unchanged consumer scores 84.7%; at 0.8 it scores 81.7%; at 1.2 it scores 79.0%; a full re-spacing gives 67.2%. After a Procrustes alignment from 500 paired items, accuracy returns to 85.6%. This is a pure rotation, so the recovery is easy; real upgrades are not pure rotations, so alignment is a bridge only. A 1-point gate blocks the 1.2 case (drop 6.6 points) and passes the 0.4 case (drop 0.9). Weak answer: "each team should retrain." Strong answer: "Version the embedding, test each consumer before promotion, and pin until they have moved."

**Code:**
```python
# Q44: upstream embedding upgrade breaks consumers. Illustrative simulation.
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(44)
d, n = 16, 6000
Z = rng.normal(size=(n, d))                      # "true" semantic factors
w_true = rng.normal(size=d)
y = (Z@w_true + rng.normal(0, 1.0, n) > 0).astype(float)
E_old = Z + rng.normal(0, 0.3, (n, d))           # v1 embedding

from scipy.linalg import expm
def new_space(E, theta, rng):
    # v2 = v1 rotated by a random rotation of size theta (a different, equally good space)
    A = rng.normal(size=(d, d)); A = A - A.T
    A = A/np.linalg.norm(A, 2)
    return E@expm(theta*A)

def fit(X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    f = lambda b: np.mean(np.logaddexp(0, X1@b) - y*(X1@b))
    return minimize(f, np.zeros(X1.shape[1]), method="L-BFGS-B").x
def acc(b, X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    return np.mean(((X1@b) > 0) == (y == 1))

tr, te = slice(0, 4000), slice(4000, n)
b = fit(E_old[tr], y[tr])
a0 = acc(b, E_old[te], y[te])
print(f"consumer on v1 vectors: accuracy {a0:.3f}")
res = {}
for frac in (0.4, 0.8, 1.2, 3.0):
    E_new = new_space(E_old, frac, np.random.default_rng(7))
    res[frac] = acc(b, E_new[te], y[te])
    print(f"v2 = {frac} rotation, old consumer unchanged: accuracy {res[frac]:.3f}")
assert res[0.4] > res[0.8] > res[1.2] > res[3.0]      # the bigger the change, the bigger the loss
assert a0 - res[3.0] > 0.15                   # full re-spacing is near-chance
# alignment on a small paired sample (orthogonal Procrustes) recovers most of it, without retraining
E_new = new_space(E_old, 3.0, np.random.default_rng(7))
idx = slice(0, 500)
U, _, Vt = np.linalg.svd(E_new[idx].T@E_old[idx]); R = U@Vt          # maps new -> old
acc_aligned = acc(b, (E_new@R)[te], y[te])
print(f"after Procrustes alignment from 500 paired items: accuracy {acc_aligned:.3f}")
assert a0 - acc_aligned < 0.01
# canary gate: per-consumer accuracy drop vs frozen eval set, block above 1 point
gate = 0.01
for frac in (0.4, 1.2):
    E_new = new_space(E_old, frac, np.random.default_rng(7))
    drop = a0 - acc(b, E_new[te], y[te])
    print(f"gate at {gate:.0%}: rotation {frac} -> drop {drop:.3f} -> {'BLOCK' if drop > gate else 'pass'}")
```

**Output (my run):**
```text
consumer on v1 vectors: accuracy 0.856
v2 = 0.4 rotation, old consumer unchanged: accuracy 0.847
v2 = 0.8 rotation, old consumer unchanged: accuracy 0.817
v2 = 1.2 rotation, old consumer unchanged: accuracy 0.790
v2 = 3.0 rotation, old consumer unchanged: accuracy 0.672
after Procrustes alignment from 500 paired items: accuracy 0.856
gate at 1%: rotation 0.4 -> drop 0.009 -> pass
gate at 1%: rotation 1.2 -> drop 0.066 -> BLOCK
```

**Follow-ups:**
- Why not freeze embeddings forever? You can lose real quality gains; the point is controlled migration with dual serving.
- What would you put in the contract? Dimension, normalisation, version id, a changelog with similarity-to-previous, deprecation date and a named consumer list.

**Common mistakes:** Replacing vectors in place. Testing only the platform's own benchmark. No version tag on stored vectors. Rolling back consumer code that did not change. Assuming a same-shape upgrade is compatible.

### Q45 ⭐ 🔴 A team monitors an LLM app with an LLM-as-judge that scored 4.2 last month and 4.5 this month, but a human spot-check of 100 outputs shows no improvement. Explain how the judge itself can drift or be biased, how you would calibrate it against human labels, and what governance you would put around automated quality scores.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** An LLM judge is a measuring instrument that can drift and can have biases (it likes long answers, its own style, a particular position), so a score going up is not quality going up until I have checked the judge against human labels and a frozen anchor set.

**Clarifying questions:**
- Did the judge model, its prompt or its rubric change between the two months? Why: a changed instrument makes the two scores incomparable.
- Did the application's outputs change in length or style (a prompt edit, a new model)? Why: judges often reward length and fluency.
- How were the 100 human outputs sampled and how many raters scored them? Why: 100 samples are noisy and rater disagreement matters.
- Is the judge a different model family from the one being judged? Why: a judge tends to prefer its own family's style.
- What decisions hang on this score (release gate, bonus, dashboard)? Why: higher stakes need stricter governance.

**Approach:**
1. Check the human check can see a change: with a rating spread of 0.9 and 100 samples per month, the standard error of the difference is 0.127, so the 95% half-width is about 0.25. A true gain of 0.3 would be detected only about 65% of the time. So "no improvement" from 100 humans is weak evidence, not proof.
2. Check the instrument: score a frozen anchor set (same outputs, fixed rubric) every month with the same judge version. A change on the anchor set means the judge moved.
3. Check biases: regress the human score on the judge score plus suspect nuisance variables (length, position, format). A negative length coefficient means the judge over-rewards length.
4. Calibrate: build a human-labelled set of a few hundred items covering both months and all segments, with two raters and an agreement figure. Fit a mapping from judge score to human score, report correlation, and apply the length adjustment.
5. Re-estimate the change: use the adjusted judge, or a larger human sample, and report the interval.
6. Governance: pin and log the judge version and prompt, refresh the human calibration on a schedule, report the judge with its agreement figure, never use it alone for a release gate, and re-calibrate on any change of judge or application.

**Metrics:**
- Judge-human agreement: Spearman correlation, or Cohen's kappa on pass/fail, on a labelled set.
- Anchor drift = mean judge score on the frozen anchor set this month - last month.
- Length coefficient c in human = a + b x judge + c x (words - baseline).
- Adjusted change = change in the length-adjusted judge score, with an interval.
- Guardrail: the judge's score on known-bad outputs stays low.

**Risks:**
- Calibrating on last month's labels misses a bias that appears only in the new style of output.
- Using the same model as generator and judge inflates scores.
- Humans are noisy too; the human label is a reference, not the truth.
- A fixed anchor set goes stale as the product changes.

**What the interviewer scores:**
- Strong: treats the judge as an instrument and tests it with an anchor set and bias regression.
- Strong: notices that 100 human ratings have limited power, in numbers.
- Strong: sets governance (versions, schedule, never the sole gate).
- Weak: trusts the judge because it is "an LLM".
- Weak: dismisses the judge entirely instead of calibrating it.

**Example:** (illustrative simulation, same story as the prompt with different levels) True quality is flat at 3.87 to 3.89. A prompt edit makes answers 30 words longer and the judge adds 0.01 per word, so its mean rises from 4.09 to 4.34. Over 400 labelled items the judge-human Spearman is 0.81, so the judge is useful, but the length coefficient is -0.0067 per word. Length-adjusted, the judge moves from 3.89 to 3.90 (+0.01), matching the human truth (+0.01). Weak answer: "Quality improved, the judge says 4.5." Strong answer: "The judge may be rewarding length; I calibrate against humans and use an anchor set."

**Code:**
```python
# Q45: LLM-as-judge drift/bias and calibration against human labels. Illustrative simulation.
import numpy as np
from scipy.stats import spearmanr, norm
rng = np.random.default_rng(45)
n = 100  # human spot check per month

# 1) the human check on its own: can 100 ratings see a +0.3 change?
sd = 0.9
se_diff = sd*np.sqrt(2/n)
print(f"SE of a difference of two 100-sample means (sd {sd}) = {se_diff:.3f}; 95% half-width {1.96*se_diff:.3f}")
assert abs(1.96*se_diff - 0.249) < 0.001
power = 1 - norm.cdf(1.96 - 0.3/se_diff) + norm.cdf(-1.96 - 0.3/se_diff)
print(f"power to detect a true +0.3 with 100 vs 100 humans = {power:.2f}")
assert 0.6 < power < 0.7

# 2) simulate: true quality unchanged, outputs got longer, judge likes length
def month(n_out, mean_len):
    quality = np.clip(rng.normal(3.9, 0.8, n_out), 1, 5)           # what humans would say
    length = rng.normal(mean_len, 25, n_out)                          # words
    judge = np.clip(quality + 0.3 + 0.01*(length - 150) + rng.normal(0, 0.4, n_out), 1, 5)
    return quality, length, judge
q1, l1, j1 = month(5000, 150)
q2, l2, j2 = month(5000, 180)      # prompt change made answers 30 words longer
print(f"judge mean {j1.mean():.2f} -> {j2.mean():.2f}; true quality {q1.mean():.2f} -> {q2.mean():.2f}")
assert j2.mean() - j1.mean() > 0.2 and abs(q2.mean() - q1.mean()) < 0.05

# 3) calibrate: on a labelled set from BOTH months, regress human on judge and length
idx1 = rng.choice(5000, 200, replace=False); idx2 = rng.choice(5000, 200, replace=False)
H = np.concatenate([q1[idx1], q2[idx2]]); J = np.concatenate([j1[idx1], j2[idx2]]); L = np.concatenate([l1[idx1], l2[idx2]])
rho = spearmanr(H, J)[0]
print(f"Spearman(human, judge) over labelled 400 = {rho:.2f}")
X = np.column_stack([np.ones(len(H)), J, L - 150])
beta = np.linalg.lstsq(X, H, rcond=None)[0]
print(f"human ~ a + b*judge + c*(length-150): b={beta[1]:.2f}, c={beta[2]:.4f} (negative c = judge over-rewards length)")
assert beta[2] < -0.003
corr_j = X@beta
adj1 = (np.column_stack([np.ones(5000), j1, l1-150])@beta).mean()
adj2 = (np.column_stack([np.ones(5000), j2, l2-150])@beta).mean()
print(f"length-adjusted judge: {adj1:.2f} -> {adj2:.2f} (change {adj2-adj1:+.2f}); human truth change {q2.mean()-q1.mean():+.2f}")
assert abs((adj2 - adj1) - (q2.mean() - q1.mean())) < 0.08
# agreement check by band: judge >= 4.5 vs human >= 4.5 (illustrative threshold)
hi_j = J >= 4.5
print(f"judge >=4.5 share {hi_j.mean():.2f}; of those humans also >=4.5: {(H[hi_j] >= 4.5).mean():.2f}")
```

**Output (my run):**
```text
SE of a difference of two 100-sample means (sd 0.9) = 0.127; 95% half-width 0.249
power to detect a true +0.3 with 100 vs 100 humans = 0.65
judge mean 4.09 -> 4.34; true quality 3.87 -> 3.89
Spearman(human, judge) over labelled 400 = 0.81
human ~ a + b*judge + c*(length-150): b=0.86, c=-0.0067 (negative c = judge over-rewards length)
length-adjusted judge: 3.89 -> 3.90 (change +0.01); human truth change +0.01
judge >=4.5 share 0.44; of those humans also >=4.5: 0.42
```

**Follow-ups:**
- How many human labels do you need? Enough to estimate agreement within a few points; a few hundred, stratified by segment, and more when the decision is risky.
- Could you use two judges? Yes, from different families, and flag disagreement for human review; it reduces self-preference but does not remove shared biases.

**Common mistakes:** Believing the judge because the number moved. Comparing scores across judge or prompt changes. Calibrating once and never again. Ignoring length and position bias. Treating a 100-item human check as conclusive.

### Q46 ⭐ 🔴 A tool-using LLM agent's task success rate fell from 82% to 74% after a third-party tool API changed its response format, and the failure was not visible in latency or error-rate dashboards. Explain how you would trace the failing step, what regression suite and contract tests would have caught it, and how to pick between prompt fixes, parsing fixes and fallback paths.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** Latency and error dashboards only see that a call returned; they do not see that the tool's answer was read wrongly, so I trace failed runs step by step to the tool call, confirm with a contract test on the tool response, and fix the parsing layer first, not the prompt.

**Clarifying questions:**
- When did success start falling, and does it line up with the vendor's change date? Why: a step change on one date points at the API.
- What share of tasks use that tool? Why: a few points of overall drop can be a big drop on one path (here 8 points overall is 32 points on a quarter of the traffic).
- Is the tool response parsed by code, or read by the model from raw text? Why: it decides where the silent failure lives.
- Do we store full traces (prompt, tool call, tool response, final answer)? Why: without traces I cannot find the failing step.
- Does the vendor offer versioned endpoints or a changelog? Why: it decides whether I can pin the old format.

**Approach:**
1. Confirm it is real: 82% to 74% on 1,000 tasks each gives z = 4.3 (p about 0.00002), so it is not noise.
2. Slice by tool: success for tasks that call the changed tool versus those that do not. In the example the tool path fell from 76% to 44% and everything else was unchanged.
3. Trace the failing step: in failed runs, compare the tool response before and after the change date. Look for the first step where the agent's belief differs from the real response (for example price read as 0).
4. Add a contract test: a schema check on every tool response in production and in CI, with real recorded responses as fixtures. A missing key or wrong type raises an alert.
5. Pick the fix by layer: (a) parsing fix (a versioned adapter that maps the new format to the old) is the first choice because it is deterministic; (b) a prompt fix only if the model must read free text and the new format is ambiguous; (c) a fallback path (fail loudly, say "unavailable", use a cached or alternative source) while the fix ships.
6. Prevent: a regression suite of tasks that exercise each tool with recorded responses, run nightly against the live API, and track task success per tool as a dashboard metric.

**Metrics:**
- Task success rate = tasks completed correctly / tasks started, per tool path and overall.
- Tool-response validity rate = responses that pass the schema / responses received.
- Fallback rate and time to detect (days from vendor change to alert).
- Guardrails: wrong-answer rate (not just failure rate), latency, cost per task.

**Risks:**
- A lenient parser returns a default instead of failing, so the wrong answer looks like success.
- Fixing in the prompt can hide the problem and break again at the next change.
- A regression suite built on mocks does not see real vendor changes; some tests must call the live API.
- Ignoring the 75% of tasks that do not use the tool is fine for diagnosis but not for the final regression check.

**What the interviewer scores:**
- Strong: slices by tool path, so 8 points overall becomes 32 points where it happened.
- Strong: contract tests on tool responses, with fail-loud behaviour.
- Strong: orders fixes: adapter, then fallback, then prompt.
- Weak: "tune the prompt" first.
- Weak: relies on error rate and latency.

**Example:** (illustrative numbers) 1,000 tasks: 750 do not use the tool and succeed 84% (630); 250 use the tool. Before: 820 successes total, so the tool path is 190 / 250 = 76%. After: 740 total, so the tool path is 110 / 250 = 44%. The 0.25 x 32 = 8-point overall drop is all in the tool path. The new response nests the price under data and the old parser's default of 0 made it a silent wrong answer. Weak answer: "The model got worse; rewrite the prompt." Strong answer: "Slice by tool, diff the responses, add a contract test and an adapter."

**Code:**
```python
# Q46: agent success fell 82% -> 74% after a tool API format change. Illustrative numbers.
import json, numpy as np
from scipy.stats import norm
N = 1000
tool_share = 0.25
non_tool_ok = 0.84
tool_before = (0.82*N - non_tool_ok*N*(1-tool_share))/(N*tool_share)
tool_after = (0.74*N - non_tool_ok*N*(1-tool_share))/(N*tool_share)
print(f"tasks using the changed tool: {int(N*tool_share)}; success before {tool_before:.1%}, after {tool_after:.1%}")
assert round(tool_before, 3) == 0.76 and round(tool_after, 3) == 0.44
# whole drop is explained by the tool path: 0.25 * (0.76-0.44) = 0.08
assert abs(tool_share*(tool_before - tool_after) - 0.08) < 1e-9

# is 8 points on 1000 vs 1000 tasks real?
p1, p2 = 0.82, 0.74
pbar = (p1+p2)/2
z = (p1-p2)/np.sqrt(pbar*(1-pbar)*2/N)
print(f"two-proportion z = {z:.2f}, p = {2*(1-norm.cdf(z)):.5f}")
assert z > 3

# contract test: the old and new response formats
old = json.loads('{"price": 249.0, "currency": "INR", "in_stock": true}')
new = json.loads('{"data": {"price": {"amount": "249.00", "currency": "INR"}, "stock": "AVAILABLE"}}')
REQUIRED = {"price": (int, float), "currency": str, "in_stock": bool}
def check_contract(resp):
    errs = []
    for k, t in REQUIRED.items():
        if k not in resp: errs.append(f"missing {k}")
        elif not isinstance(resp[k], t): errs.append(f"{k} wrong type")
    return errs
print("old format:", check_contract(old) or "ok")
print("new format:", check_contract(new))
assert check_contract(old) == [] and len(check_contract(new)) == 3

# a lenient parse that "works" but is wrong: reading price as 0 when the key is missing
def lenient(resp): return resp.get("price", 0.0)
print("lenient parser on new format returns price", lenient(new), "(silent wrong answer, no error, no latency change)")
assert lenient(new) == 0.0

# a versioned adapter plus a fail-loud fallback
def adapter(resp):
    if "data" in resp:   # v2 format
        d = resp["data"]
        return {"price": float(d["price"]["amount"]), "currency": d["price"]["currency"], "in_stock": d["stock"] == "AVAILABLE"}
    return resp
fixed = adapter(new)
print("adapter output:", fixed)
assert check_contract(fixed) == [] and fixed["price"] == 249.0
# unknown format -> fail loudly and use the fallback path (tell the user it is unavailable)
def safe_fetch(resp):
    try: return adapter(resp) if not check_contract(adapter(resp)) else None
    except (KeyError, TypeError): return None
assert safe_fetch({"weird": 1}) is None and safe_fetch(new)["price"] == 249.0
print("unknown format -> None -> fallback path; known formats parse")
```

**Output (my run):**
```text
tasks using the changed tool: 250; success before 76.0%, after 44.0%
two-proportion z = 4.32, p = 0.00002
old format: ok
new format: ['missing price', 'missing currency', 'missing in_stock']
lenient parser on new format returns price 0.0 (silent wrong answer, no error, no latency change)
adapter output: {'price': 249.0, 'currency': 'INR', 'in_stock': True}
unknown format -> None -> fallback path; known formats parse
```

**Follow-ups:**
- What if the vendor changes a field's meaning but not its format? A schema test will not catch it; use value-level checks (ranges, known examples) and the regression suite of expected answers.
- Where do you put the contract test? At the boundary in production (validate and alert) and in CI nightly against recorded plus live responses.

**Common mistakes:** Watching only latency and errors. Parsers with silent defaults. Fixing in the prompt first. Testing against mocks only. Looking at the overall rate instead of the per-tool path.

### Q47 ⭐ 🔴 A retrained recommender showed a 3% conversion lift in week one of its A/B test, but the lift decayed to near zero by week four. Explain novelty effects, interference between buckets and cannibalised demand, how you would use a long-term holdout to settle it, and what you would tell the business about shipping.
**Asked at:** Safe-rollout and shadow/canary guides (Qwak shadow-versus-canary post, Atlan shadow-deployment page, a NerdLevelTech MLOps-interview deployment-strategies lesson, a datainterview.com safe-rollout drill); commonly reported in public MLOps guides; search snippets only, not opened
**Say this first (1 line):** A lift that fades from 3% to about zero is usually a novelty effect, sometimes compounded by bucket interference or demand that was only moved from one place to another, so I would not ship on week-one numbers and I would settle it with a long-term holdout.

**Clarifying questions:**
- What was the unit of randomisation (user, session, item)? Why: bucket interference depends on it.
- Do treatment and control share limited resources (inventory, ad slots, drivers)? Why: shared supply means treatment can steal from control.
- Is the lift fading for new and returning users alike? Why: novelty hits returning users most, because they see something new.
- Did anything else change in weeks 2 to 4 (a campaign, seasonality)? Why: a time effect can mimic decay.
- Which metric matters: conversion, revenue, or long-term retention? Why: a short-term conversion lift may cost retention.

**Approach:**
1. Plot the effect by week, with intervals. In the example: 3.0%, 2.0%, 1.0%, 0.2% relative, a steady fall. A decaying curve is the novelty signature; a flat 3% would not be.
2. Split by user age and exposure count: users seeing the new recommendations for the first time versus repeat exposure. Novelty effect shrinks with repeats.
3. Check interference: if both buckets draw on the same pool, the treatment's gain can come from control. A test can read 6.2% when the company-wide gain is 0% (see the code, with a pool of 4,000 units). Look at total sales across both arms, not the treated arm alone.
4. Check cannibalisation: a rise on recommended items matched by a fall on other items or channels. Measure total basket or total revenue, not item clicks.
5. Settle it with a long-term holdout: keep a share of users on the old recommender for 8 to 12 weeks while the rest get the new one, and compare long-run outcomes. A 5% holdout of 10 million users is 500,000 users and can detect about a 2% relative change; a 0.2% residual lift needs far more users or time.
6. Tell the business: the 3% was a launch bump; the durable lift looks small or zero. Ship only if cost is low and the holdout shows a positive, durable effect; otherwise do not claim the 3%.

**Metrics:**
- Weekly relative lift = (treatment rate / control rate) - 1, with a 95% interval, by weeks since exposure.
- Total conversions across both arms (interference check).
- Holdout comparison on long-run metric: revenue per user, 8-week retention.
- Guardrails: catalogue diversity, returns, complaints.

**Risks:**
- Peeking at week one and shipping.
- Calling it novelty when it is a seasonal change that hit both arms equally (the lift is a ratio between arms, so seasonality alone does not make it fade, but an interaction can).
- A holdout too small to see a small durable effect.
- A holdout that is costly in lost revenue (see Q48 in this part).

**What the interviewer scores:**
- Strong: names the three mechanisms and a check for each.
- Strong: uses total across arms to expose interference, and sizes the holdout with numbers.
- Strong: a clear message for the business, not just "inconclusive".
- Weak: "run the test longer" with no plan.
- Weak: ignores shared supply.

**Example:** (illustrative numbers) Baseline conversion 4.00%. Week 1: 4.12% (+3.0%). Week 4: 4.008% (+0.2%). To detect a 3% lift you need about 418,607 users per arm; for a 1% lift about 3.77 million. With 10 million users and a 5% holdout (500,000 versus 9.5 million) the smallest detectable lift is about 2%, so the holdout can confirm that the week-one 3% is gone but not a 0.2% residual. Weak answer: "It is a 3% win, ship it." Strong answer: "It decays like a novelty effect; I would hold out 5% for 8 weeks and tell the business the durable gain is unproven."

**Code:**
```python
# Q47: novelty effect, cannibalisation, long-term holdout. Illustrative numbers.
import numpy as np
from scipy.stats import norm
base = 0.040   # control conversion
lift_rel = {1: 0.030, 2: 0.020, 3: 0.010, 4: 0.002}   # observed relative lift by week
for w, l in lift_rel.items():
    print(f"week {w}: relative lift {l:.1%}  (conversion {base*(1+l):.4f} vs {base:.4f})")
assert abs(base*(1+lift_rel[1]) - 0.0412) < 1e-12

# exponential-decay fit: ratio between weeks
r = np.exp(np.diff(np.log([lift_rel[w] for w in (1, 2, 3)]))).mean()
print(f"week-over-week lift ratio (weeks 1-3) ~ {r:.2f}; week 4 predicted {0.03*r**3:.4f}")

def n_per_arm(p, rel, alpha=0.05, power=0.8):
    d = p*rel
    return int(np.ceil(2*(norm.ppf(1-alpha/2)+norm.ppf(power))**2*p*(1-p)/d**2))
n_3 = n_per_arm(base, 0.03)
n_1 = n_per_arm(base, 0.01)
print(f"users per arm to detect 3% relative lift: {n_3:,}; 1% relative lift: {n_1:,}")
assert 400_000 < n_3 < 430_000 and 3_700_000 < n_1 < 4_000_000

# holdout sizing: 10M users, 5% held out on old model gives 500k vs 9.5M
n_h, n_t = 500_000, 9_500_000
se = np.sqrt(base*(1-base)*(1/n_h + 1/n_t))
mde_rel = (norm.ppf(0.975)+norm.ppf(0.8))*se/base
print(f"5% holdout of 10M users: detectable relative lift ~ {mde_rel:.2%} (80% power)")
assert 0.018 < mde_rel < 0.021

# cannibalised demand: 1,000 units of stock a day, shared by both buckets
# treatment shows items that are in demand; it wins sales from control during the test
buyers_control_alone = 0.040*50_000        # if both buckets got the old model (50k users each)
supply = 4_000                              # units (limited)
# during the A/B test treatment takes 3% more of the same pool: control loses what treatment wins
treat_sales = buyers_control_alone*1.03
ctrl_sales = supply - treat_sales
ab_lift = treat_sales/ctrl_sales - 1
print(f"limited pool: A/B reads {ab_lift:.1%} lift; full rollout total sales stay {supply}")
assert abs(ab_lift - (2060/1940 - 1)) < 1e-9 and ab_lift > 0.06
assert treat_sales + ctrl_sales == supply
print(f"true company-wide lift from the pool: 0%, yet the test reads {ab_lift:.1%}: interference")
```

**Output (my run):**
```text
week 1: relative lift 3.0%  (conversion 0.0412 vs 0.0400)
week 2: relative lift 2.0%  (conversion 0.0408 vs 0.0400)
week 3: relative lift 1.0%  (conversion 0.0404 vs 0.0400)
week 4: relative lift 0.2%  (conversion 0.0401 vs 0.0400)
week-over-week lift ratio (weeks 1-3) ~ 0.58; week 4 predicted 0.0060
users per arm to detect 3% relative lift: 418,607; 1% relative lift: 3,767,463
5% holdout of 10M users: detectable relative lift ~ 1.99% (80% power)
limited pool: A/B reads 6.2% lift; full rollout total sales stay 4000
true company-wide lift from the pool: 0%, yet the test reads 6.2%: interference
```

**Follow-ups:**
- How long should the holdout run? Until the lift curve is flat for a few weeks, typically more than one full cycle of the user behaviour. Related ideas on novelty in onboarding are in Book 6 Part 1, Q33, and on short-term versus long-term lift in Book 6 Part 1, Q39.
- What if the holdout shows a small positive lift? Ship if the cost is low; the number to quote is the holdout's, not week one's.

**Common mistakes:** Shipping on week one. Reading the treated arm alone when supply is shared. Holdouts too small. Blaming seasonality without a check. Not saying what to do.

### Q48 ⭐ 🔴 A company keeps 2% of traffic permanently on a frozen old model so it can measure model decay and the value of retraining, but finance says this costs about 2% of the model's revenue benefit. Explain the case for and against a permanent holdout, how you would size it, and cheaper alternatives for measuring decay.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** A permanent frozen holdout is insurance that measures decay directly, and it is worth it when the model carries a lot of value; but 2% is rarely the cheapest design, so I would size it to the smallest effect I need to detect and consider a rotating or smaller holdout first.

**Clarifying questions:**
- What does "2% of the model's benefit" mean: 2% of the gain over no model, or of the gain over the frozen model? Why: the real cost is the new model's gain over the frozen one on that 2% of traffic, which is smaller.
- How big is the benefit in rupees per year? Why: it sets the budget for insurance.
- What smallest decay would change a decision (for example 2% relative)? Why: the holdout size follows from it.
- Are users sticky (the same user stays in the holdout) or do they rotate? Why: it affects fairness and what the holdout shows.
- Is there a regulatory or fairness issue in keeping some customers on an old model? Why: it can limit the design.

**Approach:**
1. Frame the trade: holdout cost is certain and small; the value is catching decay early.
2. Compute the cost properly. The holdout customers still get a working (frozen) model, so the cost is 2% x (new model gain minus frozen model gain), which is at most 2% of the total benefit. For a benefit of Rs 500 lakh a year (illustrative) the cap is Rs 10 lakh; if the new model adds 30% over the frozen one it is Rs 3 lakh.
3. Compute the value: a 10% decay in benefit that goes unseen for one quarter is Rs 500 x 0.10 x 0.25 = Rs 12.5 lakh, more than a year of holdout cost in the capped case.
4. Size it by detectability: with 20 million decisions a week and a 5% base rate, a 2% holdout (400,000 users) detects about a 1.95% relative gap in a week at 80% power; pooled over 4 weeks about 1%. A 0.5% holdout detects 3.9% weekly and about 1% after 16 weeks.
5. Cheaper alternatives: (a) a smaller holdout (0.5%) read over longer windows, (b) a rotating holdout where each user is frozen only 4 weeks, (c) periodic challenger tests (a frozen model against the current one for 2 weeks every quarter), (d) shadow scoring of the old model plus off-policy estimates, (e) delayed-label accuracy trends with proxy metrics.
6. Recommend: a small rotating holdout for the high-value model, reviewed yearly; none for low-value models.

**Metrics:**
- Holdout cost = share x (new model gain - frozen model gain).
- Smallest detectable relative gap = (z_alpha/2 + z_power) x sqrt(p(1 - p)(1/n_h + 1/n_m)) / p.
- Decay estimate = metric(current) - metric(frozen), with an interval, tracked weekly.
- Guardrails: harm to holdout users, fairness across segments, holdout contamination.

**Risks:**
- A permanently frozen model gets so stale that the comparison is no longer realistic.
- Holdout leakage (users switching devices, shared features) biases the gap towards zero.
- Pooling weeks assumes a stable gap.
- Ethical or contractual limits on treating customers differently.

**What the interviewer scores:**
- Strong: computes the real cost (the gain over the frozen model, not the whole benefit).
- Strong: sizes with power and shows the trade between share and time.
- Strong: names cheaper alternatives and a recommendation.
- Weak: "always keep a holdout" or "never, it costs money" without numbers.
- Weak: ignores that the holdout users still get a working model.

**Example:** (illustrative numbers) Benefit Rs 500 lakh a year. Holdout 2%: cost cap Rs 10 lakh, realistic Rs 3 lakh. Detectability: 1.95% relative weekly. A 0.5% holdout costs 25% as much, detects 3.9% weekly and about 1% after 16 weeks pooled. One missed 10% decay quarter costs Rs 12.5 lakh. Weak answer: "Finance is right, drop it." Strong answer: "Shrink and rotate it; the insurance is worth more than it costs."

**Code:**
```python
# Q48: permanent holdout sizing and cost. Illustrative numbers.
import numpy as np
from scipy.stats import norm
weekly_decisions = 20_000_000
p = 0.05                      # conversion on the metric we care about
for share in (0.02, 0.005, 0.01):
    n_h = weekly_decisions*share; n_m = weekly_decisions - n_h
    se = np.sqrt(p*(1-p)*(1/n_h + 1/n_m))
    mde = (norm.ppf(0.975)+norm.ppf(0.8))*se
    print(f"holdout {share:.1%}: {int(n_h):,} users/week, detectable gap {mde*100:.3f} pp = {mde/p:.2%} relative (80% power, weekly)")
n_h = weekly_decisions*0.02; n_m = weekly_decisions - n_h
mde_rel = (norm.ppf(0.975)+norm.ppf(0.8))*np.sqrt(p*(1-p)*(1/n_h+1/n_m))/p
assert 0.018 < mde_rel < 0.021
# accumulate 4 weeks: noise falls by sqrt(4)
print(f"4 weeks pooled at 2%: ~{mde_rel/2:.2%} relative")
assert abs(mde_rel/2 - 0.0098) < 0.0005

# cost: the holdout loses (new model - frozen model) benefit on 2% of traffic
annual_benefit = 500.0     # Rs lakh per year: value of the model over the "no model" baseline (Rs 5 crore)
uplift_new_over_frozen = 0.30*annual_benefit  # new model adds 30% over the frozen one after a year of drift
cost_upper = 0.02*annual_benefit
cost_real = 0.02*uplift_new_over_frozen
print(f"upper bound (frozen = no model): Rs {cost_upper:.0f} lakh/yr; realistic (frozen model keeps most value): Rs {cost_real:.0f} lakh/yr")
assert cost_upper == 10.0 and abs(cost_real - 3.0) < 1e-9

# value: a decay of 10% of benefit that goes unseen for a quarter
decay_missed = 0.10*annual_benefit*0.25
print(f"undetected 10% decay for one quarter costs Rs {decay_missed:.1f} lakh; one such quarter costs more than a year of holdout (Rs {cost_upper:.0f} lakh)")
assert abs(decay_missed - 12.5) < 1e-9 and decay_missed > cost_upper

# cheaper design: rotating 0.5% holdout, each user frozen for 4 weeks only, new users each cycle
share = 0.005
n_h = weekly_decisions*share; n_m = weekly_decisions - n_h
mde = (norm.ppf(0.975)+norm.ppf(0.8))*np.sqrt(p*(1-p)*(1/n_h+1/n_m))/p
print(f"0.5% holdout: weekly MDE {mde:.1%} relative; pooled over 16 weeks {mde/4:.1%}")
assert 0.036 < mde < 0.040 and abs(mde/4 - mde/np.sqrt(16)) < 1e-12
print("cost scales with share:", f"{0.005/0.02:.0%} of the 2% holdout cost")
assert abs(0.005/0.02 - 0.25) < 1e-12
```

**Output (my run):**
```text
holdout 2.0%: 400,000 users/week, detectable gap 0.098 pp = 1.95% relative (80% power, weekly)
holdout 0.5%: 100,000 users/week, detectable gap 0.194 pp = 3.87% relative (80% power, weekly)
holdout 1.0%: 200,000 users/week, detectable gap 0.137 pp = 2.74% relative (80% power, weekly)
4 weeks pooled at 2%: ~0.98% relative
upper bound (frozen = no model): Rs 10 lakh/yr; realistic (frozen model keeps most value): Rs 3 lakh/yr
undetected 10% decay for one quarter costs Rs 12.5 lakh; one such quarter costs more than a year of holdout (Rs 10 lakh)
0.5% holdout: weekly MDE 3.9% relative; pooled over 16 weeks 1.0%
cost scales with share: 25% of the 2% holdout cost
```

**Follow-ups:**
- When is a holdout not worth it? When the model's value is small or decay is slow and visible in cheap proxies. Related ideas appear in Book 6 Part 1, Q39 (long-term holdouts for a recommender).
- How do you keep the holdout honest? Fix assignment by hashed user ID, log exposure, and check balance (sample-ratio check) each week.

**Common mistakes:** Treating the cost as 2% of everything. Under-sizing the holdout so it cannot see the effect. Letting holdout users leak into treatment. Choosing a share without a detectable-effect target.

### Q49 ⭐ 🔴 A regulation change in payments suddenly makes most of two years of transaction history unrepresentative, and only six weeks of new-regime data exists. Explain how you would keep a risk model running, which parts of the old data you would reuse, how you would use priors, simple models or human oversight in the interim, and how you would decide when to trust a new model.
**Asked at:** No interview page located; forecast-monitoring practitioner pages (demandplanning.net MAPE and bias, John Galt Solutions, 42signals forecast-drift post) describe bias, structural breaks and MAPE blind spots, so editor-designed; search snippets only, not opened
**Say this first (1 line):** I would keep the old model running under tight guardrails and human review, build a new model on the six weeks of new-regime data (using old data only where the relationship has not changed), and promote it only when it beats the interim model by more than the noise in a six-week sample.

**Clarifying questions:**
- Which inputs and which outcomes does the regulation change (fees, limits, authentication, customer behaviour)? Why: it shows which features and relationships changed and which did not.
- How many positive events (defaults, frauds) are in the six weeks? Why: events, not rows, decide how complex a model I can fit.
- Is there a rules or policy fallback today? Why: a known fallback is the safe interim.
- How fast do outcomes mature? Why: if labels take months, six weeks of "new data" may have few labels.
- What is the cost of a wrong decision in each direction and who signs off on risk? Why: it sets how much human oversight is needed.

**Approach:**
1. Triage the data: split features into stable (their relationship with the outcome should survive the change) and regime-sensitive (fees, limits, flows the rule touched). Use domain knowledge and a test on the six weeks for each group.
2. Interim: keep the old model but add guardrails: tighter thresholds on the regime-sensitive part, human review for the middle band, daily monitoring of score mix and approval rate, and a simple rule overlay where the regulation requires one.
3. Build the new model: a simple model (logistic regression with few features) on the six weeks, optionally with a prior: start from the old coefficients and penalise only deviations (shrink toward old), or add old data at low weight.
4. Compare on held-out new-regime data, by time (train on the first four weeks, test on the last two).
5. Quantify noise: repeat the evaluation on resampled six-week samples. In my run the AUC varies by about 0.008 between samples, so I would not promote on a 0.01 gain.
6. Decide when to trust the new model: pre-agree a rule: it beats the interim model by more than twice the sample-to-sample sd on a time-held-out set, passes a segment check, runs in shadow, then ramps behind a canary. Re-train every few weeks as data accumulates and phase out the interim.

**Metrics:**
- AUC (or the business metric) on a time-held-out slice of the new regime, with a resampling interval.
- Calibration: predicted versus observed rate in the new regime, once labels mature.
- Events per feature (aim for at least 10 to 20 events per model parameter as a rough guide).
- Guardrails: approval rate, loss rate, human-review rate, segment gaps.

**Risks:**
- Pooling old and new data at equal weight pulls the model back to the old rules (naive pooling at weight 0.02 was clearly worse than new-only in my run).
- Six weeks may not cover a full cycle (month-end, festival), so seasonal patterns are missing.
- Overfitting a complex model to few events.
- Labels in new regime may still be immature (see Q28 in this part).

**What the interviewer scores:**
- Strong: separates stable from regime-sensitive features and says which old data to reuse.
- Strong: interim safety with guardrails and human oversight, plus an explicit promotion rule.
- Strong: acknowledges small-sample noise with a number.
- Weak: "retrain on everything" or "wait for more data".
- Weak: no interim plan.

**Example:** (illustrative simulation with 30 features, four of which change meaning) The old model scores AUC 0.832 on future new-regime data, a model trained on 500 new-regime rows (86 events) scores 0.910, naive pooling with a low old weight scores 0.856, and shrinking toward the old coefficients scores 0.911. So the old model is clearly stale and naive pooling is worse than new-only, but shrinking gives no clear gain in my run (30 samples: 0.906 versus 0.903, sd 0.008 and 0.006). The promotion margin is therefore twice the sd, about 0.012. Weak answer: "Wait six months for data." Strong answer: "Interim guardrails, a simple new model, shrink toward the old where stable, a pre-agreed promotion test."

**Code:**
```python
# Q49: regime change; 2 years of old data, 6 weeks of new data. Illustrative simulation.
import numpy as np
from scipy.optimize import minimize
from scipy.stats import rankdata
rng = np.random.default_rng(49)
d = 30
beta_old = rng.normal(0, 0.4, d)
beta_new = beta_old.copy()
beta_new[:4] = [1.0, -1.0, 0.8, -0.8]          # four features change meaning, 26 keep it
b0 = -3.5
def gen(n, beta):
    X = rng.normal(size=(n, d))
    y = rng.random(n) < 1/(1+np.exp(-(b0 + X@beta)))
    return X, y.astype(float)
n_old, n_new = 200_000, 500
Xo, yo = gen(n_old, beta_old)
Xn, yn = gen(n_new, beta_new)
Xt, yt = gen(100_000, beta_new)               # future new-regime data

def fit(X, y, w=None, l2=0.0, center=None):
    X1 = np.column_stack([np.ones(len(X)), X]); w = np.ones(len(y)) if w is None else w
    c = np.zeros(d+1) if center is None else center
    f = lambda b: np.sum(w*(np.logaddexp(0, X1@b) - y*(X1@b)))/w.sum() + l2*np.sum((b[1:]-c[1:])**2)
    return minimize(f, c, method="L-BFGS-B").x
def auc(b, X, y):
    s = np.column_stack([np.ones(len(X)), X])@b
    r = rankdata(s); n1 = y.sum(); n0 = len(y)-n1
    return (r[y == 1].sum() - n1*(n1+1)/2)/(n1*n0)
print(f"new-regime events in 6 weeks: {int(yn.sum())} of {n_new}")
b_old = fit(Xo, yo)
res = {"old model unchanged": auc(b_old, Xt, yt), "new data only": auc(fit(Xn, yn, l2=0.0), Xt, yt)}
res["new data only, ridge 0.01"] = auc(fit(Xn, yn, l2=0.01), Xt, yt)
for lam in (0.01, 0.03, 0.1):
    res[f"new data, shrink to old, lam {lam}"] = auc(fit(Xn, yn, l2=lam, center=b_old), Xt, yt)
X = np.vstack([Xo, Xn]); y = np.concatenate([yo, yn])
res["pooled, old weight 0.02"] = auc(fit(X, y, np.concatenate([np.full(n_old, 0.02), np.ones(n_new)])), Xt, yt)
res["oracle (true new coefficients)"] = auc(np.concatenate([[b0], beta_new]), Xt, yt)
for k, v in res.items(): print(f"{k:38s} AUC on future new-regime data = {v:.3f}")
shrink = {k: v for k, v in res.items() if "shrink" in k}
best_shrink = max(shrink.values())
assert best_shrink > res["old model unchanged"] + 0.05 and res["new data only"] > res["old model unchanged"] + 0.05
assert res["oracle (true new coefficients)"] >= best_shrink
print(f"best shrink-to-old = {best_shrink:.3f} vs new-only {res['new data only']:.3f} vs old {res['old model unchanged']:.3f}")
# six weeks is a small sample, so one fit is noisy: repeat the new-only vs shrink comparison on 15 different six-week samples
a_new, a_shr = [], []
for s in range(30):
    r = np.random.default_rng(1000+s)
    Xs = r.normal(size=(n_new, d)); ys = (r.random(n_new) < 1/(1+np.exp(-(b0 + Xs@beta_new)))).astype(float)
    a_new.append(auc(fit(Xs, ys), Xt, yt)); a_shr.append(auc(fit(Xs, ys, l2=0.03, center=b_old), Xt, yt))
print(f"30 six-week samples: new-only mean {np.mean(a_new):.3f} (sd {np.std(a_new):.3f}); shrink-to-old mean {np.mean(a_shr):.3f} (sd {np.std(a_shr):.3f})")
assert abs(np.mean(a_shr) - np.mean(a_new)) < 0.01     # no clear gain from shrinking in this run
assert res['pooled, old weight 0.02'] < res['new data only'] - 0.03   # naive pooling is clearly worse
print("promotion rule used: new model must beat the interim model by more than twice the sample-to-sample sd:", round(2*np.std(a_shr), 3))
```

**Output (my run):**
```text
new-regime events in 6 weeks: 86 of 500
old model unchanged                    AUC on future new-regime data = 0.832
new data only                          AUC on future new-regime data = 0.910
new data only, ridge 0.01              AUC on future new-regime data = 0.907
new data, shrink to old, lam 0.01      AUC on future new-regime data = 0.911
new data, shrink to old, lam 0.03      AUC on future new-regime data = 0.903
new data, shrink to old, lam 0.1       AUC on future new-regime data = 0.878
pooled, old weight 0.02                AUC on future new-regime data = 0.856
oracle (true new coefficients)         AUC on future new-regime data = 0.928
best shrink-to-old = 0.911 vs new-only 0.910 vs old 0.832
30 six-week samples: new-only mean 0.906 (sd 0.008); shrink-to-old mean 0.903 (sd 0.006)
promotion rule used: new model must beat the interim model by more than twice the sample-to-sample sd: 0.012
```

**Follow-ups:**
- When would old data help more? When more coefficients are stable and the new sample is tiny; the prior then stabilises the fit. Test it on a time-held-out slice rather than assume.
- What do you tell the business now? The interim model is less accurate than before; here is the guardrail, the expected error range and the date to review.

**Common mistakes:** Pooling old and new at equal weight. Throwing away all old data. A complex model on a few events. Promoting on a small gain. No interim plan or human oversight.

### Q50 ⭐ 🔴 A degraded model went unnoticed for three weeks and leadership wants a written account and a plan. Explain how you would structure a blameless postmortem for an ML failure, which detection and ownership gaps you would look for, how you would size the business impact, and what you would commit to as concrete monitoring and process changes.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A blameless postmortem asks why the system allowed a three-week failure to go unseen, not who caused it; I write a timeline, find the detection and ownership gaps, size the loss as a range, and commit to a few monitoring and process changes with owners and dates.

**Clarifying questions:**
- What was the root trigger (a data change, a code release, a world change)? Why: it shapes the prevention actions, but the detection gap is the bigger lesson.
- Who owned the model's health, and was it written down? Why: an unowned model has no one to be alerted.
- What alerts existed, and which fired or should have? Why: it separates "no monitor" from "monitor ignored".
- How do we know the start date of the degradation? Why: the loss estimate depends on it.
- Who reads the postmortem and what do they decide? Why: leadership needs impact and commitments, engineers need causes.

**Approach:**
1. Rules of the room: blameless; focus on conditions that let it happen; no names in the root cause.
2. Timeline: when the change happened, when metrics first moved, when each signal could have fired, when a human noticed, when it was fixed. Use logs, not memory.
3. Gaps: (a) detection: no monitor on inputs, scores or labelled metrics, or a threshold nobody read; (b) ownership: no on-call or named owner; (c) change control: the change shipped without a model owner knowing; (d) validation: no consumer test; (e) label delay: the true metric appears after weeks (see Q4 in this part).
4. Impact: attempts per day x change in catch rate x loss per case x days. In the example 1,000 attempts a day, catch rate 85% to 70% and Rs 5,000 per missed fraud over 21 days is Rs 157.5 lakh (Rs 1.575 crore). If the drop ramped in over 7 days it is Rs 131 lakh. Quote the range with the assumptions and say which costs are excluded (chargeback fees, customer harm).
5. Counterfactual: which monitor would have caught it and when (see the code: a null-rate alert on day 4, a score-mean alert on day 4, the labelled metric around day 18, a human on day 24).
6. Commitments: each with an owner, a date and a check: input and score-distribution monitors with thresholds, a labelled-metric dashboard with maturity rules, an owner and on-call, a pre-release consumer test, a runbook, and a review of the monitors after 30 days. Publish the postmortem.

**Metrics:**
- Time to detect = detection time - start of degradation; time to mitigate = fix time - detection time.
- Impact = extra missed cases x average loss per case, as a range.
- Share of incidents caught by monitors (not by humans).
- Guardrail: alert precision (alerts that were real) so new monitors do not cause alert fatigue.

**Risks:**
- A blame culture hides facts.
- Over-precise impact numbers invite challenge; give a range and method.
- Too many action items: nothing gets done.
- Commitments with no owner or date.

**What the interviewer scores:**
- Strong: timeline first, causes as conditions, and detection and ownership gaps.
- Strong: impact as a range with a formula, not a headline number.
- Strong: few, concrete, owned commitments with a measure of success.
- Weak: names a person or says "be more careful".
- Weak: no numbers, or a single exact number without assumptions.

**Example:** (illustrative numbers) Change on day 3, noticed on day 24, so 21 days undetected. Pipeline monitors would have fired on day 4 (1 day); the labelled metric needs a 14-day delay and would have shown on day 18 (15 days after the change). A null-rate monitor alone would have avoided about 20 days of loss, Rs 150 lakh. Weak answer: "The model owner should have checked." Strong answer: "We had no input monitor and no owner; adding both would have cut detection from 21 days to 1."

**Code:**
```python
# Q50: postmortem numbers: impact sizing and detection timeline. Illustrative numbers.
import numpy as np
rng = np.random.default_rng(50)
# impact: fraud model catch rate fell after a feature pipeline change
attempts_per_day = 1_000
avg_loss = 5_000           # Rs per missed fraud
catch_before, catch_after = 0.85, 0.70
days = 21
extra_missed_per_day = attempts_per_day*(catch_before - catch_after)
extra_loss = extra_missed_per_day*avg_loss*days
print(f"extra missed fraud/day {extra_missed_per_day:.0f}; extra direct loss over {days} days = Rs {extra_loss/1e5:.1f} lakh = Rs {extra_loss/1e7:.3f} crore")
assert round(extra_missed_per_day) == 150 and round(extra_loss) == 15_750_000
# counterfactual honesty: range of impact if catch_after was only reached gradually (linear ramp over 7 days)
ramp = np.concatenate([np.linspace(0, 0.15, 7), np.full(days-7, 0.15)])
loss_ramp = (ramp*attempts_per_day*avg_loss).sum()
print(f"if the drop ramped linearly over the first 7 days: Rs {loss_ramp/1e5:.1f} lakh")
assert loss_ramp < extra_loss
low, high = loss_ramp, extra_loss
print(f"quote a range: Rs {low/1e5:.0f} to {high/1e5:.0f} lakh direct loss, before chargeback fees and customer cost")

# detection timeline: which monitor would have fired when
label_delay = 14
t = np.arange(40)
shift = np.clip((t - 3)/1.0, 0, 1)      # pipeline change at day 3: null-rate jumps at once
null_rate = 0.005 + 0.15*shift + rng.normal(0, 0.002, t.size)
score_mean = 0.10 - 0.03*shift + rng.normal(0, 0.003, t.size)
catch = 0.85 - 0.15*shift + rng.normal(0, 0.01, t.size)
def first_alert(series, thr, above=True):
    idx = np.where(series > thr if above else series < thr)[0]
    return int(idx[0]) if len(idx) else None
d_null = first_alert(null_rate, 0.02)
d_score = first_alert(score_mean, 0.085, above=False)
d_label_visible = first_alert(catch, 0.80, above=False) + label_delay    # label-based metric only appears after delay
d_complaints = 24                         # analysts noticed in week 4 (illustrative)
print(f"change on day 3. null-rate alert day {d_null}; score-mean alert day {d_score}; labelled catch-rate alert day {d_label_visible}; humans noticed day {d_complaints}")
assert d_null == 4 and d_score is not None and d_score <= 5 and d_label_visible >= 17
print(f"time to detect: pipeline monitors {d_null-3} day(s); label-based {d_label_visible-3} days; actual {d_complaints-3} days")
assert d_complaints - 3 == 21
saved = (d_complaints - d_null)*ramp[-1]*attempts_per_day*avg_loss
print(f"loss avoided with a null-rate monitor: about Rs {saved/1e5:.0f} lakh")
assert abs(saved - 20*0.15*1000*5000) < 1  # 20 days x 150 x Rs 5,000 = Rs 150 lakh
```

**Output (my run):**
```text
extra missed fraud/day 150; extra direct loss over 21 days = Rs 157.5 lakh = Rs 1.575 crore
if the drop ramped linearly over the first 7 days: Rs 131.2 lakh
quote a range: Rs 131 to 158 lakh direct loss, before chargeback fees and customer cost
change on day 3. null-rate alert day 4; score-mean alert day 4; labelled catch-rate alert day 18; humans noticed day 24
time to detect: pipeline monitors 1 day(s); label-based 15 days; actual 21 days
loss avoided with a null-rate monitor: about Rs 150 lakh
```

**Follow-ups:**
- How do you avoid it being a paper exercise? Track each action to closure, test the new alerts with a drill, and review at 30 and 90 days.
- How do you size impact when labels are delayed? Use the proxy (score or catch rate on matured samples) for a first range, then update when labels mature.

**Common mistakes:** Hunting for a culprit. One exact loss figure. A long list of vague actions. No owner. Skipping the timeline. Forgetting the labelled-metric delay when judging what monitors could have caught.
