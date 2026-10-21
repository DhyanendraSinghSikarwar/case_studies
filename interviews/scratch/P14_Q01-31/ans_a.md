=====Q1
**Say this first (1 line):** P(two heads) = 1/4, and the expected number of tosses until the first head is 2.

**Then explain:**
- Tosses are independent, so P(HH) = 1/2 × 1/2 = 1/4.
- "Tosses until first head" is a geometric random variable with p = 1/2, so E = 1/p = 2.
- Quick derivation (first-step analysis): E = 1 + (1/2)·0 + (1/2)·E. You always toss once; with prob 1/2 you are done, with prob 1/2 you are back where you started. Solve: E = 2.

**Example:** A payment succeeds 20% of the time on each retry. Expected attempts until first success = 1/0.2 = 5.

**Follow-ups:**
- *Variance?* (1 − p)/p² = 2 for a fair coin.
- *Biased coin?* E = 1/p; P(two heads) = p².

**Common mistakes:** Answering 1 or 3 for the expectation; confusing "number of tosses until first head" (mean 2) with "number of tails before first head" (mean 1).

=====Q2
**Say this first (1 line):** 23 people give just over a 50% chance (50.7%) of a shared birthday, and in general you need about 1.18·√N draws from N possibilities.

**Then explain:**
- Easier to count "no match": P(no match) = (365/365)(364/365)…((365−n+1)/365).
- Use 1 − x ≈ e^(−x): P(no match) ≈ exp(−n(n−1)/(2·365)). Set it to 1/2, so n² ≈ 2·365·ln 2, and n ≈ 1.1774·√365 ≈ 22.5, so n = 23.
- Why so small? There are n(n−1)/2 pairs, about 253 pairs for n = 23, and each has a 1/365 chance. Pairs grow quadratically, not linearly.
- Hash collisions: with a d-bit hash (N = 2^d values) a collision is likely after about 1.18·2^(d/2) items. This is the "birthday bound": halve the bits.

**Example:** 32-bit hash: ~77,000 items already give a 50% collision chance. 64-bit: ~5×10⁹. 128-bit: ~2×10¹⁹, so collisions are not a practical concern.

**Code:**
```python
import numpy as np
n = 1
while 1 - np.prod(1 - np.arange(n) / 365) < 0.5: n += 1
print(n, 1 - np.prod(1 - np.arange(n) / 365))
for bits in (32, 64, 128): print(bits, 1.1774 * 2 ** (bits / 2))
# 23 0.5072972343239854
# 32 77162.0864
# 64 5056894494.3104
# 128 2.1719196472385626e+19
```

**Follow-ups:**
- *Chance at 57 people?* About 99%.
- *Where does it matter in DS?* Hash-based IDs, bucketing and feature hashing (collisions in hashed feature space), UUID/ID-generation, A/B bucket collisions.

**Common mistakes:** Answering 183 (365/2); computing the chance that someone shares *your* birthday (that needs ~253 people); forgetting the pairs argument.

=====Q3
**Say this first (1 line):** About 17% (1 in 6), because the disease is rare, so false positives from the many healthy people swamp the true positives.

**Then explain:**
- Bayes: P(D|+) = P(+|D)P(D) / [P(+|D)P(D) + P(+|¬D)P(¬D)] = 0.99·0.01 / (0.99·0.01 + 0.05·0.99) = 0.0099/0.0594 ≈ 0.167.
- Specificity 95% means a 5% false-positive rate (1 − 0.95), not 1%.
- Think in counts per 10,000 people: 100 sick, of whom 99 test positive; 9,900 healthy, of whom 495 test positive. So 99 of 594 positives are truly sick = 16.7%.
- The prior (base rate) matters as much as the test accuracy. Intuition fails because we only look at sensitivity.

**Example:** Same logic for fraud detection: if 0.1% of transactions are fraud, even a 99%-accurate model flags mostly legitimate ones. This is why precision, not accuracy, is the metric on imbalanced data.

**Follow-ups:**
- *How to raise it?* Higher specificity, or test only high-risk people (higher prior), or repeat the test (see Q19).
- *What if prevalence were 20%?* P = 0.99·0.2/(0.99·0.2 + 0.05·0.8) = 83%.

**Common mistakes:** Reporting 99% (confusing P(+|D) with P(D|+)); using 1 − 0.95 on the wrong population; ignoring the base rate.

=====Q4
**Say this first (1 line):** Yes, always switch: switching wins 2/3 of the time, staying wins 1/3.

**Then explain:**
- Your first pick is the car with prob 1/3. Monty then opens a goat door, which does not change that 1/3.
- So the remaining closed door holds the car with prob 2/3 (all the probability your pick did *not* have).
- Case view: if you picked the car (1/3), switching loses. If you picked a goat (2/3), Monty must reveal the other goat, so switching wins. Switching wins iff your first pick was wrong = 2/3.
- Key assumption: Monty knows where the car is and always opens a goat door. If he opened randomly and happened to reveal a goat, switching and staying would be 50/50.

**Example:** With 100 doors, you pick one, Monty opens 98 goats: the other door has a 99% chance. Makes the intuition obvious.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0); N = 100_000
car, pick = rng.integers(0, 3, N), rng.integers(0, 3, N)
print("stay", (pick == car).mean(), "switch", (pick != car).mean())  # switching wins iff first pick was wrong
# stay 0.33168 switch 0.66832
```

**Follow-ups:**
- *Why is "50/50" wrong?* Monty's action is informed by the car's location, so the two remaining doors are not symmetric.
- *Bayes proof?* P(car behind 3 | you pick 1, Monty opens 2) = (1·1/3)/(1/2·1/3 + 1·1/3 + 0) = 2/3.

**Common mistakes:** Saying 50/50; ignoring that the host's choice is constrained.

=====Q5
**Say this first (1 line):** For a 6-sided die it is 14.7 rolls; in general n·H_n ≈ n·ln n + 0.577n, which is O(n log n).

**Then explain:**
- Split into stages. With k faces already seen, the chance a roll is new is (n−k)/n, so the wait is geometric with mean n/(n−k).
- Add the stages: E = n/n + n/(n−1) + … + n/1 = n(1 + 1/2 + … + 1/n) = n·H_n.
- For n = 6: 6(1 + 1/2 + 1/3 + 1/4 + 1/5 + 1/6) = 14.7. The last face alone costs 6 rolls on average.
- Scaling: H_n ≈ ln n + 0.5772 (Euler-Mascheroni constant), so E ≈ n ln n + 0.577n. n = 100 gives 518.7, n = 1000 gives 7485.

**Example:** How many random samples until you have seen all 1,000 distinct classes? About 7,500, i.e. 7.5× the number of classes. Relevant for coverage in sampling, random testing, and "collect all tokens" problems.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
def rolls_until_all(n):
    seen, t = set(), 0
    while len(seen) < n: seen.add(rng.integers(n)); t += 1
    return t
print(np.mean([rolls_until_all(6) for _ in range(20000)]), 6 * sum(1 / k for k in range(1, 7)))
# 14.70125 14.700000000000001
```

**Follow-ups:**
- *Variance?* Dominated by the last stages; sd is about n·π/√6.
- *Tail?* The chance you still miss a face after n(ln n + c) rolls is about 1 − exp(−e^(−c)).

**Common mistakes:** Answering 6 or 6·ln 6; forgetting that the stages have different success probabilities.

=====Q6
**Say this first (1 line):** Apply Bayes to the words, assume words are independent given the class, and multiply per-word likelihoods; that independence assumption is what makes it "naive" and tractable.

**Then explain:**
- Bayes: P(spam | words) ∝ P(spam) · ∏ P(word_i | spam). Compare it with the same quantity for ham and normalise.
- Training is just counting: P(word | spam) = (count of word in spam + 1)/(total spam words + V). The +1 is Laplace smoothing so an unseen word does not zero the product.
- Use log-probabilities in code to avoid underflow when multiplying hundreds of small numbers.
- Why it works: without independence you would need a joint distribution over 2^V word combinations. With it you only need V numbers per class. Even when it is wrong, the ranking of classes is often right.
- When it breaks: correlated features (e.g. "New" and "York" counted twice, so probabilities become over-confident and badly calibrated), features that interact, and tiny/imbalanced data. It is a good baseline, but do not trust its probabilities.

**Example:** Message "free prize meeting": "free" and "prize" push to spam, "meeting" pushes to ham; the product decides.

**Code:**
```python
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
docs = ["win free prize now", "free money win", "meeting at noon", "lunch meeting tomorrow", "free lunch offer now", "project update meeting"]
y = np.array([1, 1, 0, 0, 1, 0])                  # 1 = spam
cv = CountVectorizer(); X = cv.fit_transform(docs)
nb = MultinomialNB(alpha=1).fit(X, y)             # alpha=1 -> Laplace smoothing
print("P(ham), P(spam):", nb.predict_proba(cv.transform(["free prize meeting"]))[0].round(3))
# P(ham), P(spam): [0.394 0.606]
```

**Follow-ups:**
- *Why is it still competitive?* Low variance, so it works with little data; the decision (argmax) is robust even if probabilities are not.
- *Fix the calibration?* Calibrate (Platt/isotonic) or move to logistic regression, which handles correlated features.

**Common mistakes:** Forgetting smoothing; multiplying raw probabilities (underflow); claiming the features must truly be independent; trusting the predicted probabilities.

=====Q7
**Say this first (1 line):** HH takes 6 tosses on average and HT only 4, because after a miss HT can reuse the toss but HH cannot.

**Then explain:**
- Use states. For HT: start (a), have an H (b). a = 1 + ½b + ½a; b = 1 + ½·0 + ½b. So b = 2, a = 2 + b = 4.
- For HH: after an H, a T sends you back to the start: b = 1 + ½·0 + ½a, a = 2 + b. Solve: b = 4, a = 6.
- Intuition: in HT, after an H, a failed attempt (another H) still leaves you in "have an H". In HH, a failed attempt (T) resets you to zero. HH overlaps with itself, so its occurrences are clumpy and the first one comes later.
- Both patterns appear at the same long-run rate (1 in 4 positions), but the *waiting time* differs. A pattern with self-overlap has a longer wait.

**Example:** Equivalent to why runs of identical results "feel" rarer: HH takes longer to show up than HT in a coin sequence.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
def wait(pattern):
    s = []
    while s[-2:] != pattern: s.append(int(rng.integers(2)))
    return len(s)
print("HH", np.mean([wait([1, 1]) for _ in range(20000)]), "HT", np.mean([wait([1, 0]) for _ in range(20000)]))
# HH 6.00405 HT 3.9885
```

**Follow-ups:**
- *Which appears first, HH or HT?* 50-50 by symmetry: after the first H, next toss decides.
- *What about HHH?* 14 (see Q45).

**Common mistakes:** Saying both are 4 because "each has probability 1/4"; not setting up the state equations.

=====Q8
**Say this first (1 line):** 1/3 if you only know "at least one is a boy", and 1/2 if you know the older one is a boy.

**Then explain:**
- Equally likely families: BB, BG, GB, GG.
- "At least one boy" removes GG, leaving BB, BG, GB. Only BB has two boys: 1/3.
- "Older is a boy" leaves BB and BG: 1/2.
- The difference is *how* you learned the information. "At least one" is a statement about the set; "the older one" picks a specific child, which makes the other child independent.

**Example:** You meet a parent with a boy walking beside them (picked a specific child): the other child is 50% boy. You are told "at least one is a boy" by a survey: 1/3.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
k = rng.integers(0, 2, (1_000_000, 2))            # 1 = boy
print((k[k.sum(1) >= 1].sum(1) == 2).mean(), (k[k[:, 0] == 1][:, 1] == 1).mean())
# 0.3332280265373126 0.499601292651194
```

**Follow-ups:**
- *"At least one boy born on a Tuesday"?* 13/27 ≈ 0.48: more specific information moves it toward 1/2.

**Common mistakes:** Answering 1/2 for the first case; treating BG and GB as the same outcome.

=====Q9
**Say this first (1 line):** Use von Neumann's trick: toss twice, HT means 1, TH means 0, and discard HH/TT and repeat; this gives a perfectly fair bit for any unknown p.

**Then explain:**
- P(HT) = p(1−p) = P(TH), so conditional on getting a mixed pair, each is equally likely. The unknown p cancels.
- Cost: each pair succeeds with prob 2p(1−p), so on average you need 1/(p(1−p)) tosses per fair bit (6.25 tosses for p = 0.8).
- For 7 equally likely outcomes: generate 3 fair bits (values 0-7); if you get 7, reject and redo. That is rejection sampling and every kept value has prob 1/7. Expected 8/7 rounds.
- Do not use "mod 7" on 3 bits (0 and 7 both map to 0), which biases the result.

**Example:** Pick a uniformly random one of 7 engineers for an on-call rota using only a flaky bit source.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(1)
def fair_bit(p):                      # von Neumann: toss twice, HT -> 1, TH -> 0, else retry
    while True:
        a, b = rng.random() < p, rng.random() < p
        if a != b: return int(a)
def uniform7(p):                      # 3 fair bits -> 0..7, reject 7
    while True:
        v = 4 * fair_bit(p) + 2 * fair_bit(p) + fair_bit(p)
        if v < 7: return v
print(np.round(np.bincount([uniform7(0.8) for _ in range(14000)]) / 14000, 3))
# [0.136 0.141 0.148 0.143 0.14  0.147 0.144]   (each ~1/7 = 0.143)
```

**Follow-ups:**
- *Can you be more efficient?* Yes, Elias/Peres extraction reuses the discarded pairs and gets closer to the entropy limit H(p) bits per toss.
- *Why 2^k outcomes needed?* A fair choice among 7 needs rejection, since 7 does not divide a power of 2.

**Common mistakes:** Trying to estimate p first; using modulo; not noticing that HH/TT pairs must be discarded, not counted.
