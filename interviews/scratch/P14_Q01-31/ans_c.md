=====Q20
**Say this first (1 line):** No: the expected profit is −Rs 3.33 per play, and the variance of the winnings is about 1,389 (sd ≈ Rs 37).

**Then explain:**
- E[payout] = 100 × 1/6 = 16.67. Subtract the fee: 16.67 − 20 = −3.33 per game.
- Variance: the payout is 100 × Bernoulli(1/6), so Var = 100² × (1/6)(5/6) = 10,000 × 5/36 = 1,388.9. The fixed fee does not change variance.
- Over 1,000 plays you expect to lose about Rs 3,333, with sd ≈ 37.3 × √1000 ≈ Rs 1,179, so you are very likely to be down.
- You would play only if the fee were below Rs 16.67 (fair price), or for entertainment.

**Example:** The house edge is 3.33/20 = 16.7% of the stake, which is how casinos and lotteries make money.

**Follow-ups:**
- *What fee makes it fair?* Rs 16.67.
- *Does a risk-seeking person play?* Possibly, but that is a utility question, not an expected-value one.

**Common mistakes:** Forgetting to subtract the fee; computing variance on net winnings as if the fee added variance; using p(1−p) without the 100² factor.

=====Q21
**Say this first (1 line):** Both aces = 1/221 ≈ 0.45%; a pair = 3/51 ≈ 5.9%; second card red given first red = 25/51 ≈ 49%.

**Then explain:**
- Two aces: 4/52 × 3/51 = 12/2652 = 1/221.
- Pair (same rank): whatever the first card is, 3 of the remaining 51 match its rank: 3/51 = 1/17.
- Red given red: 25 reds remain among 51 cards: 25/51 = 0.490 (slightly below 1/2, since drawing without replacement removes one red).

**Example:** Poker: being dealt a pocket pair is 1 in 17.

**Follow-ups:**
- *With replacement?* Aces 1/169, red-given-red 1/2.
- *Are the two draws independent?* No: the first draw changes the deck.

**Common mistakes:** Using 4/52 × 4/52 (with replacement); using 1/13 for a pair; treating "pair" as needing two specific cards.

=====Q22
**Say this first (1 line):** Leverage measures how unusual a point's X values are (its potential to pull the line); Cook's distance measures how much the fit actually changes when you drop that point; a point with high leverage and a large residual is influential.

**Then explain:**
- Leverage h_ii is the diagonal of the hat matrix; it lies between 0 and 1 and averages p/n (p = number of coefficients). Flag h_ii > 2p/n (or 3p/n).
- Cook's D combines residual size and leverage. It is the overall change in fitted values when the point is removed. Flag D > 4/n (common) or D > 1 (conservative).
- High leverage with a small residual is harmless (it follows the trend); a large residual with low leverage is an outlier but moves the fit little.
- What to do: investigate first (data error? different population?). Fix a genuine error; otherwise keep it and report results with and without it, or use robust regression (Huber) / a better model. Do not delete just to improve R².

**Example/Code:** One far-out wrong point flips a slope from about 2 to about 0:
```python
import numpy as np, statsmodels.api as sm
rng = np.random.default_rng(0)
x = rng.normal(size=30); y = 1 + 2 * x + rng.normal(0, .5, 30)
x[0], y[0] = 6, -5                                # one far-out point that breaks the trend
m = sm.OLS(y, sm.add_constant(x)).fit(); inf = m.get_influence()
h, cd = inf.hat_matrix_diag, inf.cooks_distance[0]
print("leverage[0] %.2f (rule of thumb 2p/n = %.2f)" % (h[0], 2 * 2 / 30))
print("Cook D[0] %.1f, next largest %.2f (rule 4/n = %.2f)" % (cd[0], np.sort(cd)[-2], 4 / 30))
print("slope with point %.2f, without %.2f" % (m.params[1], sm.OLS(y[1:], sm.add_constant(x[1:])).fit().params[1]))
# leverage[0] 0.66 (rule of thumb 2p/n = 0.13)
# Cook D[0] 25.9, next largest 0.33 (rule 4/n = 0.13)
# slope with point 0.01, without 1.82
```

**Follow-ups:**
- *Can a point be influential without looking like an outlier in the residuals?* Yes: with high leverage the line is pulled toward it, so its residual shrinks.
- *Other measures?* DFFITS, DFBETAS (effect on one coefficient).

**Common mistakes:** Deleting every flagged point; confusing outlier (in y) with leverage (in X); using the thresholds as hard rules.

=====Q23
**Say this first (1 line):** P(A|B) and P(B|A) are different things related by Bayes; confusing them is the prosecutor's fallacy. Independent means P(A∩B) = P(A)P(B); mutually exclusive means they cannot both happen, and exclusive events (with positive probability) are actually dependent.

**Then explain:**
- Prosecutor's fallacy: "the DNA match has a 1-in-a-million chance if the suspect is innocent" is P(match | innocent). It is not P(innocent | match). In a city of 10 million people, about 10 innocent people would match, so with no other evidence P(guilty | match) ≈ 1/11.
- Link: P(A|B) = P(B|A)P(A)/P(B). You need the prior P(A) (base rate).
- Independent: knowing B does not change A. Mutually exclusive: P(A∩B) = 0. If A and B are exclusive and both possible, knowing B occurred makes A impossible, so they are dependent.

**Example:** P(a dangerous fraud | flagged) is not P(flagged | fraud); only the first matters for what an analyst should investigate, and it depends on the fraud rate.

**Follow-ups:**
- *Defender's fallacy?* Ignoring the match because "10 people would match" without considering that the match still raises the odds from 1-in-10M to 1-in-11.
- *Same as the medical test paradox?* Yes (Q3).

**Common mistakes:** Treating "independent" and "mutually exclusive" as synonyms; reading a p-value as P(hypothesis true).

=====Q24
**Say this first (1 line):** E[max of two dice] = 161/36 ≈ 4.47; for n dice use E[M] = Σ_{m=0}^{5} [1 − (m/6)^n]; for n Uniform(0,1) variables E[max] = n/(n+1).

**Then explain:**
- Use the CDF: P(M ≤ m) = (m/6)^n. For non-negative integer M, E[M] = Σ_{m≥0} P(M > m) = Σ_{m=0}^{5} [1 − (m/6)^n].
- n = 2: 6 − (0+1+4+9+16+25)/36 = 6 − 55/36 = 161/36 = 4.472.
- n = 1: 3.5; n = 3: 4.958; n = 10: 5.820. It climbs toward 6 as n grows.
- Uniform: P(M ≤ x) = x^n, density n·x^(n−1), so E[M] = ∫ x·n·x^(n−1)dx = n/(n+1). The max gets close to 1 as n grows (n = 9 gives 0.9). By symmetry E[min] = 1/(n+1).

**Example:** Max of n server latencies is what a user-facing request waits for (fan-out), and it grows with n even if each server is the same.

**Follow-ups:**
- *Distribution of the max of n uniforms?* Beta(n, 1) (see Q53).
- *Expected min of two dice?* 91/36 ≈ 2.53; check: E[max] + E[min] = 7.

**Common mistakes:** Averaging the two dice; forgetting that the CDF of the max is the product of CDFs.

=====Q25
**Say this first (1 line):** Write the count as a sum of indicator variables and add their expectations; independence is not needed. Fixed points = 1, distinct birthdays among 23 ≈ 22.32, empty bins with n balls in n bins ≈ n/e.

**Then explain:**
- Linearity of expectation: E[ΣX_i] = ΣE[X_i], always true, even for dependent events.
- Fixed points in a random permutation of n: each position is fixed with prob 1/n, so E = n × 1/n = 1 for every n.
- Distinct birthdays among n people (365 days): each day is "covered" with prob 1 − (364/365)^n, so E = 365(1 − (364/365)^n); n = 23 gives 22.32.
- Empty bins: m balls into n bins: each bin is empty with prob (1 − 1/n)^m, so E = n(1 − 1/n)^m; for m = n this is ≈ n/e ≈ 0.368n.

**Example:** Hashing 100 keys into 100 buckets leaves about 37 buckets empty.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
print("fixed points (n=10):", np.mean([(rng.permutation(10) == np.arange(10)).sum() for _ in range(100000)]))
print("distinct birthdays, 23 people:", 365 * (1 - (364 / 365) ** 23))
print("empty bins, 100 balls in 100 bins:", 100 * (1 - 1 / 100) ** 100)
# fixed points (n=10): 0.99937
# distinct birthdays, 23 people: 22.319962396220888
# empty bins, 100 balls in 100 bins: 36.60323412732292
```

**Follow-ups:**
- *Variance of fixed points?* Also 1 (the count is approximately Poisson(1)).
- *Why is this trick powerful?* It avoids computing the full distribution.

**Common mistakes:** Believing you need independence; computing the full distribution instead of using indicators.

=====Q26
**Say this first (1 line):** For a fair game, P(ruin) = 1 − i/N and the expected duration is i(N − i); with a biased coin, ruin is far more likely and the formulas use r = q/p.

**Then explain:**
- Fair coin: your wealth is a martingale, so E[final] = i. Final is 0 or N, so P(reach N) = i/N and P(ruin) = 1 − i/N.
- Duration: E[T] = i(N − i), largest when you start in the middle (N/2)².
- Biased (win prob p, q = 1 − p, r = q/p ≠ 1): P(ruin) = (r^i − r^N)/(1 − r^N); E[T] = i/(q−p) − (N/(q−p))·(1 − r^i)/(1 − r^N).
- Even a small negative edge (p = 0.45) makes ruin the overwhelming outcome; as N → ∞ with p ≤ 1/2, ruin prob → 1.

**Example:** Start with Rs 3, target Rs 10. Fair: ruin 70%, 21 bets on average. With p = 0.45: ruin 87.2%, 17.2 bets.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
def sim(i, N, p, T=20000):
    ruined = steps = 0
    for _ in range(T):
        x = i; t = 0
        while 0 < x < N: x += 1 if rng.random() < p else -1; t += 1
        ruined += (x == 0); steps += t
    return ruined / T, steps / T
i, N = 3, 10
print("fair   sim:", sim(i, N, .5), " theory:", (1 - i / N, i * (N - i)))
p = .45; q = 1 - p; r = q / p
ruin = (r ** i - r ** N) / (1 - r ** N); dur = i / (q - p) - N / (q - p) * (1 - r ** i) / (1 - r ** N)
print("p=.45  sim:", sim(i, N, p), " theory:", (ruin, dur))
# fair   sim: (0.69705, 21.1381)  theory: (0.7, 21)
# p=.45  sim: (0.87325, 17.2413)  theory: (0.8717476511872477, 17.174765118724764)
```

**Follow-ups:**
- *Casino with infinite bankroll?* The gambler with finite wealth and any edge against them is ruined with prob 1 eventually.
- *Link to Kelly?* Bet sizing to avoid ruin (Q48).

**Common mistakes:** Using the fair formulas for a biased coin; forgetting the duration formula; confusing "N" (target) with number of bets.

=====Q27
**Say this first (1 line):** A symmetric 1D walk returns to the origin with probability 1 (recurrent), starting from 0 it hits +a before −b with probability b/(a+b), and takes ab steps on average.

**Then explain:**
- P(at 0 after 2n steps) = C(2n, n)/4^n ≈ 1/√(πn): after 100 steps it is 7.96%. It shrinks, but the sum diverges, so the walk returns infinitely often.
- Hitting: it is the gambler's ruin problem: P(hit +a before −b) = b/(a+b); E[steps] = a·b.
- Spread grows like √t: after t steps the typical distance is √t, not t.
- Stock modelling: price changes as unpredictable increments is the random-walk (efficient market) idea: variance grows linearly with time, so volatility scales with √t (annual vol ≈ daily vol × √252). Real prices are better modelled with log-returns (geometric Brownian motion, prices stay positive); real markets have fat tails and volatility clustering.
- In 2D it is still recurrent; in 3 or more dimensions it is transient.

**Code:**
```python
import numpy as np, math
rng = np.random.default_rng(0); a, b, T = 3, 5, 20000
hit_up = steps = 0
for _ in range(T):
    x = t = 0
    while -b < x < a: x += 1 if rng.random() < .5 else -1; t += 1
    hit_up += (x == a); steps += t
print("P(hit +a) sim %.3f theory %.3f | E[steps] sim %.2f theory %d" % (hit_up / T, b / (a + b), steps / T, a * b))
print("P(at 0 after 100 steps) =", math.comb(100, 50) / 2 ** 100, " approx", 1 / math.sqrt(math.pi * 50))
# P(hit +a) sim 0.631 theory 0.625 | E[steps] sim 15.09 theory 15
# P(at 0 after 100 steps) = 0.07958923738717877  approx 0.07978845608028654
```

**Follow-ups:**
- *Expected return time to the origin?* Infinite, even though return is certain.
- *Does a random walk mean you cannot predict returns?* Roughly the weak-form efficient market claim; volatility can still be forecast.

**Common mistakes:** Saying the walk drifts away linearly; stating prices (rather than log prices) are a symmetric walk; confusing "returns with prob 1" with "returns quickly".

=====Q28
**Say this first (1 line):** A Markov chain moves between states where the next state depends only on the current one; its stationary distribution π solves πP = π (sum to 1), exists for any finite chain, is unique if irreducible, and the chain converges to it if it is also aperiodic.

**Then explain:**
- Transition matrix P: row i holds probabilities of going from state i, each row sums to 1.
- Find π: left eigenvector of P with eigenvalue 1 (eigenvector of Pᵀ), normalised to sum 1; or solve πP = π with Σπ = 1; or just raise P to a high power.
- Irreducible = every state can reach every other; aperiodic = no fixed cycle length (e.g. a two-state flip-flop is periodic, so it never converges but still has a stationary distribution).
- Reading π: long-run fraction of time spent in each state.

**Code:**
```python
import numpy as np
P = np.array([[.9, .1, 0], [.2, .7, .1], [.1, .2, .7]])
w, v = np.linalg.eig(P.T)                         # pi P = pi  <=>  P^T pi = pi (eigenvalue 1)
pi = np.real(v[:, np.argmin(abs(w - 1))]); pi /= pi.sum()
print("pi:", pi.round(4), " check pi@P == pi:", np.allclose(pi @ P, pi))
print("row of P^100:", np.linalg.matrix_power(P, 100)[0].round(4))
# pi: [0.6364 0.2727 0.0909]  check pi@P == pi: True
# row of P^100: [0.6364 0.2727 0.0909]
```

**Follow-ups:**
- *Speed of convergence?* Governed by the second-largest eigenvalue magnitude (spectral gap).
- *Where used?* PageRank, MCMC, user-state modelling, HMMs.

**Common mistakes:** Using the right eigenvector of P (gives all-ones); forgetting to normalise; claiming convergence for a periodic chain.

=====Q29
**Say this first (1 line):** Count transitions between states per period and normalise each row to get P; expected lifetime comes from the fundamental matrix N = (I − Q)⁻¹ where Q is the transient-to-transient block; then check the Markov assumption empirically.

**Then explain:**
- States: active, dormant, churned (absorbing: once churned, stays churned). Each user-period gives one transition observation.
- Estimate: P̂_ij = count(i → j)/count(i →). It is the maximum-likelihood estimate; add smoothing for rare transitions.
- Expected lifetime: with Q the 2×2 block among transient states (active, dormant), N = (I − Q)⁻¹ has N_ij = expected periods spent in j starting from i. Row sums give the expected time to churn. In the simulation below: 11.77 months from active (truth 11.82).
- Sanity-check Markov: (1) compare next-state distribution given (current, previous) vs given current only; if previous state matters, it is not first-order Markov (here prev=active vs prev=dormant give the same row). (2) check stationarity across cohorts/time, (3) compare the model's predicted retention curve with actual cohort retention. Common failure causes: tenure effects (hazard falls with age), user heterogeneity, seasonality.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
true = np.array([[.80, .15, .05], [.30, .50, .20], [0, 0, 1.]])   # active, dormant, churned
U, T = 5000, 12; S = np.zeros((U, T), int); cum = true.cumsum(1)
for t in range(1, T): S[:, t] = (rng.random(U)[:, None] > cum[S[:, t - 1]]).sum(1)
cnt = np.zeros((3, 3)); np.add.at(cnt, (S[:, :-1].ravel(), S[:, 1:].ravel()), 1)
P = cnt / cnt.sum(1, keepdims=True); print(P.round(3))             # estimate = row-normalised counts
Q = P[:2, :2]; N = np.linalg.inv(np.eye(2) - Q)                    # fundamental matrix
print("expected months until churn, from active: %.2f (true %.2f)" % (N[0].sum(), np.linalg.inv(np.eye(2) - true[:2, :2])[0].sum()))
prev, cur, nxt = S[:, :-2].ravel(), S[:, 1:-1].ravel(), S[:, 2:].ravel()   # Markov check
for a in (0, 1):
    m = (cur == 0) & (prev == a); print("prev=%d -> P(next | now active):" % a, (np.bincount(nxt[m], minlength=3) / m.sum()).round(3))
# [[0.799 0.15  0.051]
#  [0.298 0.505 0.197]
#  [0.    0.    1.   ]]
# expected months until churn, from active: 11.77 (true 11.82)
# prev=0 -> P(next | now active): [0.801 0.148 0.051]
# prev=1 -> P(next | now active): [0.791 0.152 0.057]
```
(The 12-month window truncates observed paths, so the estimate is slightly off; fine for a demo.)

**Follow-ups:**
- *Reactivation of churned users?* Make "churned" non-absorbing, or add a "resurrected" state.
- *Tenure dependence?* Use a semi-Markov model, or add age bucket into the state.

**Common mistakes:** Row-normalising the wrong axis; treating churned as a normal state when computing lifetime; never testing the Markov assumption.

=====Q30
**Say this first (1 line):** PageRank is the stationary distribution of a "random surfer" Markov chain: follow a random outgoing link with probability d, or jump to a random page with probability 1 − d (d = 0.85 typically); the damping makes the chain irreducible and aperiodic so a unique answer exists.

**Then explain:**
- Transition matrix: P_ij = 1/outdegree(i) if i links to j. Pages with no outlinks (dangling) are treated as linking to all pages.
- Google matrix: G = dP + (1 − d)(1/n)·11ᵀ. Every entry is positive, so the chain is irreducible and aperiodic; the Perron-Frobenius theorem gives a unique stationary vector.
- Power iteration: start with r = uniform, repeat r ← r·G (written as d·r·P + (1 − d)/n) until it stops changing. Converges at rate d per iteration, so ~30 iterations are enough for 1e-10 here. Cost per iteration O(number of links) with sparse matrices.
- d trades off fidelity to links (d → 1, slow convergence, can be dominated by traps/sinks) against uniformity (d → 0).

**Code:**
```python
import numpy as np
L = np.array([[0, 1, 1, 0], [0, 0, 1, 0], [1, 0, 0, 1], [0, 0, 1, 0]], float)   # L[i,j]=1: page i links to j
def pagerank(L, d=0.85, tol=1e-10):
    n = len(L); out = L.sum(1, keepdims=True)
    P = np.where(out > 0, L / np.where(out > 0, out, 1), 1 / n)      # dangling page -> jump anywhere
    r = np.ones(n) / n
    for it in range(1000):
        r_new = d * r @ P + (1 - d) / n                              # follow link w.p. d, teleport w.p. 1-d
        if np.abs(r_new - r).sum() < tol: return r_new, it
        r = r_new
    return r, it
r, it = pagerank(L); print(r.round(4), r.sum().round(6), "iterations:", it)
# [0.2199 0.131  0.4292 0.2199] 1.0 iterations: 31
```
Page 2 gets the most links, so the highest score.

**Follow-ups:**
- *Why not solve the eigenproblem directly?* Web-scale matrices are huge and sparse; power iteration only needs matrix-vector products.
- *Personalised PageRank?* Teleport to a chosen set of pages instead of uniform.

**Common mistakes:** Forgetting dangling nodes (the mass leaks); mixing up row/column orientation; thinking d is the probability of a random jump.

=====Q31
**Say this first (1 line):** Draw samples from each Beta posterior and compute the share of draws where B > A, plus the expected loss of each decision; this answers "how likely is B better and what do I risk" directly, which a p-value does not.

**Then explain:**
- With Beta(1,1) priors, posteriors are Beta(1+k, 1+n−k). Sample 500k from each: P(B > A) = mean(b > a).
- Expected loss of shipping B = E[max(a − b, 0)] (how much conversion you give up on average if A was actually better). Choose B if the loss is below a tolerance threshold you set (e.g. 0.1% abs).
- p-value: P(data at least this extreme | no difference). Bayesian: P(B > A | data). Different questions; the Bayesian one uses a prior and needs no null hypothesis, and the loss weighs the size of the mistakes.
- Example: A 120/1000 (12.0%), B 140/1000 (14.0%). Z-test p = 0.184: "not significant". Bayesian: P(B > A) = 0.91; expected loss shipping B ≈ 0.0006 (0.06 pp), keeping A ≈ 0.021 (2.1 pp). Same data, but the Bayesian output is more useful for deciding.
- Caution: Bayesian stopping rules are still affected by peeking if you stop on "P(B>A) > 95%" without a loss threshold/minimum sample (see Q16).

**Code:**
```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
kA, nA, kB, nB = 120, 1000, 140, 1000
a = stats.beta(1 + kA, 1 + nA - kA).rvs(500_000, random_state=1)
b = stats.beta(1 + kB, 1 + nB - kB).rvs(500_000, random_state=2)
print("P(B > A)            :", (b > a).mean().round(3))
print("expected loss ship B:", np.maximum(a - b, 0).mean().round(5))
print("expected loss keep A:", np.maximum(b - a, 0).mean().round(5))
print("p-value (z-test)    :", proportions_ztest([kB, kA], [nB, nA])[1].round(3))
# P(B > A)            : 0.908
# expected loss ship B: 0.00065
# expected loss keep A: 0.02058
# p-value (z-test)    : 0.184
```

**Follow-ups:**
- *Is P(B>A) = 0.91 the same as 1 − p/2?* Roughly (0.908 vs 0.908 here) with flat priors and large n, but not in general.
- *What threshold?* Set on business cost: ship if expected loss < the smallest effect you care about.

**Common mistakes:** Calling P(B>A) a p-value; ignoring the prior; shipping on probability alone without effect size or expected loss.
