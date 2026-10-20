# Book 1 - Part 13: Statistics Deep Dive I (Distributions, Estimation, Inference)

**Topic:** distributions, sampling, estimators, CLT/LLN, CIs, p-values, hypothesis tests, power, multiple comparisons, bootstrap, correlation
**Target:** 50 questions
**Actual:** 61 questions
**Date:** 2026-10-20

**Scope note:** probability puzzles, Bayes, Markov chains, regression diagnostics, Bayesian stats, sequential testing, CUPED and simulation are in Part 14; A/B design and causal inference are in Part 10.

---

### Q1 ⭐⭐⭐ 🟢 Explain a p-value in plain words. What does it NOT mean?
**Asked at:** Flipkart, Amazon, Walmart, Microsoft IDC, Spotify; near-universal
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Explain Type I and Type II errors. How are they related to alpha, beta and power, and which is costlier in practice?
**Asked at:** Amazon, Flipkart, Swiggy, JPMC, Booking; near-universal
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is the difference between standard deviation and standard error?
**Asked at:** Product cos, GCCs, analytics cos
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 State the Central Limit Theorem. Why does it matter for data science, and when does it break down?
**Asked at:** Amazon, Flipkart, Microsoft IDC, Walmart, Zalando
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 How do you correctly interpret a 95% confidence interval? Why is 'there is a 95% chance the true mean lies in it' wrong?
**Asked at:** Product cos, GCCs, Europe product cos
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 One-tailed vs two-tailed tests: when do you use each and what is the cost of choosing one-tailed?
**Asked at:** Product cos, analytics cos
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 What is the difference between covariance and correlation? Why is correlation preferred for comparing relationships?
**Asked at:** Product cos, GCCs, analytics cos
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 Describe the normal distribution: properties, the 68-95-99.7 rule, z-scores and standardisation. How do you check if data is normal?
**Asked at:** Product cos, GCCs, analytics cos
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 t-test vs z-test: when do you use which? What are the assumptions of a t-test?
**Asked at:** Flipkart (reported Nov 2025), Amazon, GCCs
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Statistical significance vs practical significance: a result has p = 0.001 but a tiny effect. What do you do?
**Asked at:** Amazon, Spotify, Booking, Swiggy
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 What is statistical power and what factors affect it? How would you increase it?
**Asked at:** Amazon, Spotify, Booking, Klarna, Swiggy
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 How do you compute the required sample size for a two-proportion (conversion-rate) test? Show it in scipy/statsmodels.
**Asked at:** Amazon, Swiggy, Booking, Spotify
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 What is the multiple comparisons problem? Explain Bonferroni and Benjamini-Hochberg and when to use each.
**Asked at:** Product cos, Databricks-style teams, Europe product cos
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Explain the chi-squared test (independence and goodness of fit). What are its assumptions?
**Asked at:** Flipkart, Amazon, analytics cos, GCCs
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Parametric vs non-parametric tests: when would you use Mann-Whitney U instead of a t-test?
**Asked at:** Amazon, GCCs, product cos
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 What is the bootstrap? Explain how to get a confidence interval with it and implement it in NumPy.
**Asked at:** Google-style, Amazon, Spotify, Zalando; GCCs
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 Binomial vs Poisson: when does each apply, and when does Poisson approximate binomial?
**Asked at:** Swiggy, Flipkart, Amazon, GCCs
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 What is sampling bias? Give examples (selection, survivorship, non-response) and how you would detect and mitigate them.
**Asked at:** Product cos, GCCs, Spotify, Booking
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🟡 What makes an estimator good? Explain bias, variance, MSE, and why the sample variance divides by n-1.
**Asked at:** Product cos, GCCs, analytics cos
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐⭐ 🟡 Explain maximum likelihood estimation. Derive the MLE for a Bernoulli probability and for a normal mean and variance.
**Asked at:** Product cos, GCCs, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 What is the Law of Large Numbers and how is it different from the CLT?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 Uniform distribution: mean, variance, and how do you use it to generate samples from any distribution (inverse transform)?
**Asked at:** Product cos, GCCs, quant-leaning teams
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Exponential distribution: what is memorylessness and how does it relate to the Poisson process?
**Asked at:** Swiggy, Flipkart, Amazon, Zalando (delivery/wait-time themes)
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Paired vs independent two-sample t-test: when is each valid and what happens if you pick wrong?
**Asked at:** Product cos, GCCs, Booking
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 What is Welch's t-test and why is it usually the default over the pooled-variance t-test?
**Asked at:** Product cos, Spotify, Booking
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Explain one-way ANOVA and the F-statistic. What do you do after a significant ANOVA (post-hoc tests)?
**Asked at:** Analytics cos, GCCs, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Fisher's exact test vs chi-squared test: when do you prefer Fisher's?
**Asked at:** Analytics cos, GCCs, health/pharma-leaning teams
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How do you test for normality (Shapiro-Wilk, Q-Q plot)? Do you actually need normality for a t-test?
**Asked at:** GCCs, analytics cos, product cos
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 What is the Kolmogorov-Smirnov test? How do you use it for one-sample and two-sample comparisons (e.g., drift detection)?
**Asked at:** Product cos, fintech (PhonePe/Klarna-type), GCCs
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Explain sampling methods: simple random, stratified, cluster, systematic. When is stratified better?
**Asked at:** Analytics cos, GCCs, product cos
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Pearson vs Spearman vs Kendall correlation: when do you use each?
**Asked at:** Product cos, GCCs, analytics cos
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Can two variables have zero correlation and still be dependent? Give an example.
**Asked at:** Product cos, quant-leaning teams
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Method of Moments vs MLE: how does MoM work, and when would you prefer one?
**Asked at:** GCCs, Microsoft IDC, research-leaning teams
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How are the t, chi-squared and F distributions related? Where does each arise?
**Asked at:** GCCs, analytics cos, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 What is p-hacking? How do researchers misuse p < 0.05 and how do you guard against it?
**Asked at:** Product cos, Spotify, Booking, Amazon
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 Confidence interval for a proportion: Wald vs Wilson. Why does Wald fail for small n or extreme p?
**Asked at:** Product cos, Booking, Spotify
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 Confidence interval vs prediction interval vs tolerance interval: what is the difference?
**Asked at:** GCCs, analytics cos
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 FWER vs FDR: how do Bonferroni, Holm and Benjamini-Hochberg differ in what they control and in power?
**Asked at:** Product cos, Europe product cos
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 Your conversion rate went from 10.0% to 10.4% with 50,000 users per arm. Run the two-proportion z-test and interpret it.
**Asked at:** Swiggy, Flipkart, Amazon, PhonePe
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 Explain degrees of freedom intuitively. Why does the t-distribution depend on it?
**Asked at:** GCCs, analytics cos
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 What is effect size (Cohen's d, relative lift) and why report it alongside a p-value?
**Asked at:** Amazon, Spotify, Booking
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 What is the duality between confidence intervals and hypothesis tests?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 How do you choose the right distribution for real data: delivery time, number of orders per hour, conversion rate, order value?
**Asked at:** Swiggy, Flipkart, Zalando, Klarna
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 How do you compute a sample size to estimate a mean (or proportion) within a given margin of error?
**Asked at:** Analytics cos, survey/market-research teams, GCCs
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 Implement a two-sample (Welch) t-test from scratch in NumPy and verify against scipy.stats.ttest_ind.
**Asked at:** Live-coding rounds at product cos and GCCs
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 What is regression to the mean and the winner's curse? How do they distort the analysis of top-performing segments?
**Asked at:** Product cos, Amazon, Booking
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🔴 Revenue-per-user is heavy-tailed. Is a t-test still valid? What would you do (log transform, trimming, bootstrap, Mann-Whitney)?
**Asked at:** Amazon, Flipkart, Booking, Zalando
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 What is a permutation test? When is it preferable to a t-test and how do you implement it?
**Asked at:** Product cos, Spotify, Booking
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🟡 Wilcoxon signed-rank and Kruskal-Wallis: what do they test and what are their assumptions?
**Asked at:** Analytics cos, GCCs
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🟡 How do you estimate power by Monte Carlo simulation when no closed-form formula exists?
**Asked at:** Amazon, Spotify, Booking, senior roles
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🟡 An LLM gives you a statistical analysis (test choice, p-value, interpretation) for your data. How do you review it for errors?
**Asked at:** AI-era rounds at product cos and GCCs
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 What are consistency, efficiency and sufficiency of an estimator? State the Cramer-Rao lower bound.
**Asked at:** Research-leaning teams, Microsoft IDC, senior roles
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 What is Fisher information, and why is the MLE asymptotically normal? How do you get a standard error from it?
**Asked at:** Research-leaning teams, senior roles
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🔴 How does the delta method give a standard error for a ratio metric (e.g., revenue per session)?
**Asked at:** Amazon, Booking, Spotify, senior roles
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🔴 What exactly does the Mann-Whitney U test test? Is it a test of medians? What are the pitfalls?
**Asked at:** Senior DS roles, Amazon, Spotify
<!-- ANSWER_PENDING -->

### Q56 ⭐ 🔴 When does the bootstrap fail? What are percentile vs BCa intervals and what is the bootstrap for dependent (time-series) data?
**Asked at:** Senior DS roles, Google-style
<!-- ANSWER_PENDING -->

### Q57 ⭐ 🔴 Count data is overdispersed relative to Poisson. How do you detect it and what do you do (negative binomial, quasi-Poisson)?
**Asked at:** Swiggy, Zalando, Booking, senior roles
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🔴 How does FDR control behave under dependent tests? Explain q-values and Benjamini-Yekutieli.
**Asked at:** Senior roles, Europe product cos
<!-- ANSWER_PENDING -->

### Q59 ⭐ 🔴 What is an equivalence / non-inferiority test (TOST)? When would you use it instead of a standard test?
**Asked at:** Spotify, Booking, Klarna, senior roles
<!-- ANSWER_PENDING -->

### Q60 ⭐ 🔴 Cauchy distribution: why do the LLN and CLT fail, and what does it teach about heavy tails?
**Asked at:** Quant-leaning and senior roles
<!-- ANSWER_PENDING -->

### Q61 ⭐ 🔴 What is the design effect for clustered or correlated observations, and how does it change standard errors and sample size?
**Asked at:** Senior roles, Booking, Zalando, Swiggy
<!-- ANSWER_PENDING -->

