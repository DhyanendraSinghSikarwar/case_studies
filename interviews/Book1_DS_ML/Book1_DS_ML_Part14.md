# Book 1 — Part 14: Statistics Deep Dive II

**Topic:** Probability puzzles, conditional probability & Bayes, Markov chains, random walks, order statistics, regression diagnostics, Bayesian statistics, sequential testing, CUPED / variance reduction, Monte Carlo simulation
**Target:** >=50 questions  |  **Actual:** 63 (⭐⭐⭐ 20, ⭐⭐ 26, ⭐ 17)  |  **Date:** 2026-10-20
**Scope note:** Distributions, sampling, estimators, CLT, CIs, classical tests and power belong to Part 13; A/B and causal design belong to Part 10.

---

### Q1 ⭐⭐⭐ 🟢 You toss a fair coin twice: what is the probability of two heads in a row, and what is the expected number of tosses until the first head?
**Asked at:** Typical (prep sources): Swiggy DS (Prepfully); Indian product cos, GCCs; screening rounds
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Birthday problem: how many people until there is a >50% chance two share a birthday? Derive it and extend to hash collisions.
**Asked at:** Typical (prep sources): Quant firms, Amazon, Indian product cos; stats screening rounds
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 A disease affects 1% of people and a test is 99% sensitive and 95% specific. You test positive: what is the probability you have the disease? Why is the answer so low?
**Asked at:** Typical (prep sources): Most DS loops (Amazon, Flipkart, Microsoft IDC, Booking, Spotify)
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Monty Hall: should you switch doors? Prove it, then simulate it in Python.
**Asked at:** Typical (prep sources): Quant firms, product cos; listed classic in Analytics Vidhya / DataInterview
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 Expected number of rolls of a fair die until you see every face at least once (coupon collector), and how does it scale with n?
**Asked at:** Typical (prep sources): Quant puzzles, Optiver/Jane Street style, product cos (DataInterview)
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Design a spam filter from first principles using Bayes theorem: P(spam | word) given word frequencies. What assumption makes Naive Bayes work and when does it break?
**Asked at:** Likely (expert gap-check): Flipkart, Amazon, Walmart GCC, JPMC
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Expected number of fair-coin tosses until you see HH vs HT: why are they different?
**Asked at:** Typical (prep sources): Quant firms, Jane Street style, product cos
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Boy-or-girl puzzle: a family has two children and at least one is a boy: probability both are boys? What if you know the older one is a boy?
**Asked at:** Typical (prep sources): Conditional-probability classic at product cos and trading firms
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 You have a biased coin with unknown bias p: how do you simulate a fair coin? Extend it to generate 7 equally likely outcomes from a biased binary source.
**Asked at:** Typical (prep sources): Swiggy DS (Prepfully), quant firms
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 What is multicollinearity? How do you detect it (correlation matrix, VIF, condition number), what does it do to coefficients and standard errors, and how do you fix it?
**Asked at:** Typical (prep sources): Flipkart, Swiggy, Amazon India, Walmart GCC, banks/GCCs
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 List the assumptions of OLS. Which are needed for unbiased coefficients and which only for valid standard errors / confidence intervals?
**Asked at:** Typical (prep sources): Snapchat DS (PracHub), Amazon, Microsoft IDC, Indian product cos
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 What is heteroscedasticity? How do you detect it (residual plots, Breusch-Pagan, White) and fix it (robust SEs, log transform, WLS)?
**Asked at:** Typical (prep sources): Amazon India, banks/GCCs, Flipkart
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How do you read residual plots (residuals vs fitted, Q-Q, scale-location, residuals vs leverage) and what pattern signals which problem?
**Asked at:** Typical (prep sources): DS loops at product cos and consulting analytics
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Frequentist vs Bayesian: explain a 95% confidence interval vs a 95% credible interval in plain words, with a conversion-rate example.
**Asked at:** Likely (expert gap-check): Spotify, Booking, Zalando, Microsoft IDC, Amazon
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Beta-Binomial: your prior for a conversion rate is Beta(a, b) and you observe k conversions in n visits. What is the posterior, its mean, and a 95% credible interval? Show it in scipy.
**Asked at:** Likely (expert gap-check): Product cos, Europe experimentation teams (Spotify Confidence, Booking)
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 Explain CUPED: what does it do, what is the formula, why is it unbiased, and how much variance does it remove?
**Asked at:** Typical (prep sources): Microsoft, Netflix, Spotify, Booking, Amazon; senior experimentation roles
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 What is the peeking problem? Simulate how checking an A/B test daily inflates the false-positive rate, and name two valid fixes.
**Asked at:** Typical (prep sources): Spotify, Booking, Zalando, Flipkart, Swiggy experimentation roles
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 How do you estimate a probability, an integral or pi using Monte Carlo? How many simulations do you need for a given accuracy?
**Asked at:** Typical (prep sources): Quant firms; DS rounds that ask simulation answers
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🟡 Why does a Bayesian posterior depend on the prior and how do you pick one? Show how the posterior changes for an informative vs a flat prior and small vs large n.
**Asked at:** Likely (expert gap-check): Product cos, Europe experimentation teams
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐⭐ 🔴 You test positive twice on independent tests, or the test is run on a high-risk group: how do you update the posterior? Where does the independence assumption break?
**Asked at:** Likely (expert gap-check): Follow-up to the medical-test question; senior DS loops
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 A game pays Rs 100 if you roll a six and nothing otherwise; the entry fee is Rs 20. Should you play and what is the variance of your winnings?
**Asked at:** Typical (prep sources): Interview Kickstart style EV questions; Indian product cos
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 Two cards are drawn from a 52-card deck without replacement: probability both are aces, probability of a pair, probability the second card is red given the first is red?
**Asked at:** Typical (prep sources): Product cos, GCCs, quant firms
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 What are leverage and Cook's distance? How do you flag an influential point and what do you do with it?
**Asked at:** Typical (prep sources): Prepfully, PracHub question banks; Amazon, banks/GCCs
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟢 Explain P(A|B) vs P(B|A) with the prosecutor's fallacy. When are two events independent vs mutually exclusive?
**Asked at:** Typical (prep sources): Common screening question at product cos
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Expected value of the maximum of two (and of n) fair dice rolls; max of n Uniform(0,1) variables.
**Asked at:** Typical (prep sources): Quant firms (Optiver-style expected maxima)
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Use linearity of expectation: expected number of fixed points in a random permutation, expected number of distinct birthdays, expected number of empty bins.
**Asked at:** Typical (prep sources): Quant firms; probability rounds at big tech
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Gambler's ruin: you start with Rs i, bet Rs 1 on a fair coin, stop at 0 or N. What is the probability of ruin and expected duration? What changes if the coin is biased?
**Asked at:** Typical (prep sources): Optiver (random walk with absorbing barriers), Jane Street style
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Simple symmetric random walk: what is the probability of returning to the origin, expected steps to hit +a or -b, and why does it matter for stock-price modelling?
**Asked at:** Typical (prep sources): Optiver, quant-flavoured DS roles
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 What is a Markov chain? How do you find the stationary distribution of a transition matrix, and when does it exist and converge?
**Asked at:** Typical (prep sources): Jane Street style steady-state questions; Flipkart/Amazon DS theory rounds
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Model user states (active, dormant, churned) as a Markov chain: how do you estimate the transition matrix, compute expected lifetime, and sanity-check the Markov assumption?
**Asked at:** Likely (expert gap-check): Swiggy, Flipkart, PhonePe product analytics roles
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 How is PageRank a Markov chain? Explain the damping factor and implement power iteration in NumPy.
**Asked at:** Likely (expert gap-check): Search/recsys-flavoured DS and MLE loops
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Bayesian A/B test: with Beta posteriors for A and B, how do you compute P(B > A) and expected loss? How does it differ from a p-value?
**Asked at:** Likely (expert gap-check): Spotify Confidence, Booking, Zalando, Microsoft
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Give the main ways to reduce variance in an experiment metric (CUPED/regression adjustment, stratification, post-stratification, winsorizing, control variates) and when to use which.
**Asked at:** Typical (prep sources): TechPrep, PracHub variance-reduction banks; Booking, Spotify, Netflix
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you choose a CUPED covariate? Why must it be pre-experiment, what happens with new users who have no history, and does CUPED work with ratio metrics?
**Asked at:** Typical (prep sources): PracHub CUPED questions; Spotify Confidence RFP
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 Explain group sequential testing and alpha spending (Pocock, O'Brien-Fleming). Why do these boundaries control Type I error?
**Asked at:** Likely (expert gap-check): Spotify, Booking, experimentation-platform teams
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 Does multicollinearity hurt prediction? How do ridge regression and PCA regression deal with it versus dropping variables?
**Asked at:** Typical (prep sources): Prepfully multicollinearity answers; Indian product cos
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 Residuals look non-normal and right-skewed: what does it break (and not break), and when do you use a log or Box-Cox transform?
**Asked at:** Typical (prep sources): Banks/GCCs, consulting analytics, Indian product cos
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 How do you detect and handle autocorrelated residuals (Durbin-Watson, Ljung-Box)? Why does it invalidate standard errors?
**Asked at:** Likely (expert gap-check): Time-series-adjacent DS interviews; JPMC/banks
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 Break a stick at two random points: probability the three pieces form a triangle?
**Asked at:** Typical (prep sources): Classic quant geometric probability puzzle
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 You flip a coin 10 times and get 10 heads: probability the next is heads? Compare the frequentist MLE, Laplace smoothing and a Beta prior.
**Asked at:** Likely (expert gap-check): Bayesian intuition question at product cos and trading firms
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 Use the laws of total expectation and total variance: a random number of customers each spends a random amount. What are the mean and variance of total revenue?
**Asked at:** Likely (expert gap-check): Quant firms, Amazon/Flipkart theory rounds
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 Empirical Bayes shrinkage: how do you rank restaurants or products by CTR or rating when some have very few observations?
**Asked at:** Likely (expert gap-check): Swiggy, Zalando, Booking, Flipkart ranking and recsys teams
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 AI-era: an LLM benchmark shows 83/100 correct for model A vs 80/100 for model B. How do you give a credible interval and decide if A is better? How would you review an LLM-generated statistical analysis for errors?
**Asked at:** Likely (expert gap-check): 2025-2026 GenAI evaluation roles at product cos
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 Walk through statsmodels OLS output: R-squared vs adjusted R-squared, F-test, t-stats, condition number warning, Durbin-Watson, Jarque-Bera. What would you check next?
**Asked at:** Typical (prep sources): Banks/GCCs, Amazon, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 Explain MLE vs MAP vs full Bayesian inference and how L2/L1 regularization map to Gaussian/Laplace priors.
**Asked at:** Likely (expert gap-check): ML-theory rounds at product cos and Europe
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🔴 Expected number of tosses to see HHH (or HTH) using Markov chain states or martingales.
**Asked at:** Typical (prep sources): Jane Street / quant-firm style
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟢 Non-transitive dice: A beats B, B beats C, C beats A. Verify it by simulation, and compute the probability that one die beats another.
**Asked at:** Typical (prep sources): Quant puzzle sets
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 Poker hand probabilities: probability of a flush, a full house, and being dealt at least one ace in five cards.
**Asked at:** Typical (prep sources): Trading firms, card puzzle sets
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🟡 St. Petersburg paradox and Kelly criterion: why is expected value not enough for decisions? How do you size a bet with positive edge?
**Asked at:** Likely (expert gap-check): Quant firms, risk-flavoured DS roles
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🟡 Thompson sampling for a Bernoulli bandit: explain it using Beta posteriors and simulate it against epsilon-greedy.
**Asked at:** Likely (expert gap-check): Recsys/ads teams at Flipkart, Zalando, Spotify
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🟡 Winsorizing, capping and trimming outliers: how do they reduce variance and what bias do they introduce?
**Asked at:** Likely (expert gap-check): Booking, Zalando, Spotify experimentation
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🟡 Hat matrix and leverage: derive H = X(X'X)^-1 X', explain h_ii, and relate leverage to Cook's distance.
**Asked at:** Likely (expert gap-check): Stats-heavy DS roles, research scientist loops
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🟡 Frisch-Waugh-Lovell theorem: explain it and use it to interpret a coefficient in multiple regression and to see why CUPED is regression adjustment.
**Asked at:** Likely (expert gap-check): Senior DS/economist loops
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🔴 Distribution of the k-th order statistic of n Uniform(0,1) samples: derive it (Beta) and use it to get the expected median and expected range.
**Asked at:** Typical (prep sources): Quant firms, stat theory rounds
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🔴 Expected maximum of n i.i.d. Exponential(1) variables, and why it grows like log n.
**Asked at:** Typical (prep sources): Optiver (expected maxima), quant stat rounds
<!-- ANSWER_PENDING -->

### Q56 ⭐ 🔴 Secretary problem: what is the optimal stopping rule and why 1/e?
**Asked at:** Typical (prep sources): Quant puzzle sets, Jane Street style
<!-- ANSWER_PENDING -->

### Q57 ⭐ 🔴 Absorbing Markov chains: use the fundamental matrix to find expected time to absorption and absorption probabilities.
**Asked at:** Typical (prep sources): Quant firms, OR-flavoured DS roles
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🔴 Always-valid inference: explain mSPRT / confidence sequences and how they differ from group sequential designs.
**Asked at:** Likely (expert gap-check): Spotify, Netflix, experimentation-platform teams
<!-- ANSWER_PENDING -->

### Q59 ⭐ 🔴 Control variates and importance sampling in Monte Carlo: how do you estimate a rare-event probability with low variance? Show code.
**Asked at:** Typical (prep sources): Quant roles, simulation-heavy DS
<!-- ANSWER_PENDING -->

### Q60 ⭐ 🔴 Write a Metropolis-Hastings sampler from scratch in NumPy to sample a posterior. How do you diagnose convergence (trace, R-hat, ESS)?
**Asked at:** Likely (expert gap-check): Bayesian-heavy DS and research roles
<!-- ANSWER_PENDING -->

### Q61 ⭐ 🔴 Hierarchical Bayesian model / partial pooling: when do you use it, for example for store- or city-level conversion rates?
**Asked at:** Likely (expert gap-check): Swiggy, Zalando, Booking, senior roles
<!-- ANSWER_PENDING -->

### Q62 ⭐ 🔴 Delta method for ratio metrics (e.g. revenue per session) and its variance; how do you combine it with CUPED?
**Asked at:** Likely (expert gap-check): Spotify, Booking, Microsoft ExP
<!-- ANSWER_PENDING -->

### Q63 ⭐ 🔴 Heteroscedasticity-consistent standard errors (HC0-HC3) and cluster-robust SEs: when and why?
**Asked at:** Likely (expert gap-check): Economist-style DS roles, Europe
<!-- ANSWER_PENDING -->
