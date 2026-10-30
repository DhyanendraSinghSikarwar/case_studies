# Q48: label-drift gate on a labelling batch. Illustrative numbers.
import math
from math import comb, sqrt
n, rate_new, rate_old, prev_batches = 10_000, 0.12, 0.08, 6
pos_new, pos_exp = int(n * rate_new), int(n * rate_old)
assert (pos_new, pos_exp) == (1200, 800)

sd = sqrt(n * rate_old * (1 - rate_old))
z = (pos_new - pos_exp) / sd
print(f"expected positives {pos_exp}, sd {sd:.1f}, observed {pos_new}, z = {z:.2f}")
assert round(sd, 1) == 27.1 and round(z, 2) == 14.74
sd_rate = sqrt(rate_old * (1 - rate_old) / n)
print(f"sampling sd of a batch rate: {sd_rate*100:.2f} points; shift is {(rate_new-rate_old)/sd_rate:.1f} sd")
# gate with a margin for real batch-to-batch wobble: use 3 x binomial sd plus 0.5 point allowance
limit = rate_old + 3 * sd_rate + 0.005
print(f"gate upper limit {limit:.4f}; batch {rate_new:.4f} trips: {rate_new > limit}")
assert rate_new > limit and 0.09 < limit < 0.095

# Real shift or guideline change? Re-send 500 gold items (previously labelled, 8% positive = 40).
gold_n, gold_pos_before = 500, 40
pos_to_neg, neg_to_pos = 4, 24                     # illustrative re-labels by the new guideline
gold_pos_after = gold_pos_before - pos_to_neg + neg_to_pos
print(f"gold positives before {gold_pos_before} ({gold_pos_before/gold_n:.0%}), after {gold_pos_after} ({gold_pos_after/gold_n:.1%})")
assert gold_pos_after == 60 and gold_pos_after / gold_n == 0.12
flips = pos_to_neg + neg_to_pos
p_sign = sum(comb(flips, k) for k in range(neg_to_pos, flips + 1)) / 2 ** flips      # one-sided
print(f"flips {flips}: {neg_to_pos} neg->pos vs {pos_to_neg} pos->neg, one-sided sign-test p = {p_sign:.2e}")
assert p_sign < 1e-3

# Second check: model scores on the batch. A calibrated model's mean score tells whether the INPUTS moved.
mean_score_new, mean_score_old = 0.081, 0.080
print(f"mean model score new {mean_score_new:.3f} vs old {mean_score_old:.3f}: inputs look the same, labels moved")
# Expected size of the shift if only the guideline changed: new positives among old negatives
extra = rate_new - rate_old
print(f"label-only shift of {extra*100:.0f} points means about {extra*n:.0f} of 10,000 rows relabelled to positive")
assert round(extra * n) == 400

# Fraction of old-negative rows that the new guideline turns positive (from the gold test)
frac = neg_to_pos / (gold_n - gold_pos_before)
print(f"gold flip rate neg->pos: {frac:.3f} ({neg_to_pos}/{gold_n - gold_pos_before})")
assert round(frac, 4) == 0.0522
