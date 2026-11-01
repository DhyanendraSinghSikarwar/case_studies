# Thumbs-up fine-tuning plan. Illustrative numbers from the prompt plus an invented selection-bias demo. Seeded.
import math
import numpy as np
chats, votes, ups = 100_000, 3000, 2400
print("vote coverage", votes/chats, "thumbs-up share of votes", ups/votes)
assert votes/chats == 0.03 and ups/votes == 0.8
aud_n, aud_ok = 200, 150
rate_wrong = 1 - aud_ok/aud_n
wrong = ups * rate_wrong
print("audit wrong rate", rate_wrong, "projected wrong among 2,400:", wrong)
assert rate_wrong == 0.25 and wrong == 600
def wil(k, n, z=1.96):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h, c+h
lo, hi = wil(aud_n-aud_ok, aud_n)
print("Wilson for wrong share", round(lo, 3), round(hi, 3), "-> wrong count range", round(ups*lo), round(ups*hi))
assert round(lo, 3) == 0.195 and round(hi, 3) == 0.314 and round(ups*lo) == 468 and round(ups*hi) == 754
# Invented demo of why votes mislead: users vote up fluent/agreeable answers even when wrong.
rng = np.random.default_rng(3)
n = 100_000
correct = rng.random(n) < 0.80                              # true accuracy 80% (invented)
# Invented: confident wrong answers are upvoted slightly more often than correct plain ones (sycophancy-style bias).
up = rng.random(n) < np.where(correct, 0.020, 0.030)
print("thumbs-up wrong share in this invented world:", round((~correct[up]).mean(), 3), "vs overall wrong share", round((~correct).mean(), 3))
assert 0.24 < (~correct[up]).mean() < 0.32 and 0.19 < (~correct).mean() < 0.21
# What an audit-then-filter plan yields: keep only audited-correct examples
keep = ups * (aud_ok/aud_n)
print("examples left after verifying each (if audit rate holds):", keep)
assert keep == 1800
# Cost of auditing everything: 2,400 reviews at 1 minute each
print("review hours at 1 min each:", 2400/60)
assert 2400/60 == 40
