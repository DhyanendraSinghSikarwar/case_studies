# Book 1 - Part 10: A/B Testing, Causal Inference & Experimentation (Question List)

**Topic:** experiment design, metrics, randomization units, SRM, novelty, interference, multiple testing, peeking, switchback, DiD, propensity scores, IV, RDD, uplift, observational vs experimental, ambiguous results, GenAI experimentation.
**Target:** 50  |  **Actual:** 58  (3-star 19, 2-star 27, 1-star 12)  |  **Date:** 2026-10-20
**Scope note:** power/sample-size derivations, sequential testing, CUPED, variance reduction and Bayesian stats are owned by Parts 13-14; questions here are interview-use level only.
**Status:** Phase 1 (questions only, answers pending).

### Q1 ⭐⭐⭐ 🟢 Walk me through how you would design an A/B test end to end (hypothesis, metrics, unit, sample size, duration, decision rule).
**Asked at:** Product cos, Flipkart, Swiggy, Spotify, Booking, Zalando, GCCs
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is an A/B test and when should you NOT run one?
**Asked at:** Product cos, Amazon, Microsoft IDC, Booking
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 How do you choose the primary metric, guardrail metrics and secondary metrics for an experiment? Give an example.
**Asked at:** Spotify, Zalando, Swiggy, Flipkart, PhonePe
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What is the randomization unit? How do you choose between user-, session-, device-, request- and cluster-level randomization?
**Asked at:** Booking, Spotify, Uber-style marketplaces, Amazon
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 How do you decide how long to run an experiment and how many users you need? (interview-level: which inputs drive sample size; derivations are in Part 13)
**Asked at:** All product cos, Zalando, Swiggy, Flipkart
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 What is a Sample Ratio Mismatch (SRM)? How do you detect it and what are the common causes?
**Asked at:** Microsoft, Spotify, Booking, Zalando, product cos
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 The A/B test shows a significant lift but the PM wants to stop the test after 3 days. What is wrong with peeking and what do you do?
**Asked at:** Product cos, Zalando, Swiggy, Amazon
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 What is the novelty effect and the primacy effect? How do you detect them and what do you do about them?
**Asked at:** Zalando, Spotify, Booking, product cos
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 You track 20 metrics (or 10 variants) in one test and one is significant at p=0.04. What is the multiple-testing problem and how do you handle it (Bonferroni, BH/FDR)?
**Asked at:** Zalando, Amazon, Flipkart, product cos
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 What is Simpson's paradox? Give an A/B-test example where the variant wins overall but loses in every segment.
**Asked at:** FAANG-style loops, product cos
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Explain correlation vs causation. How would you establish causality for the claim 'users who use feature X retain better'?
**Asked at:** Spotify, Booking, product cos, Swiggy
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Explain network effects / interference (SUTVA violation). How do you run experiments on a social product or a two-sided marketplace?
**Asked at:** Uber, Swiggy, Zomato, Booking, Spotify, LinkedIn-style
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 The test shows the primary metric up but revenue (or a guardrail) down or flat. How do you interpret and decide?
**Asked at:** Product cos, Swiggy, Flipkart, Zalando
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 What do you do when the A/B test result is statistically insignificant? Can you conclude there is no effect?
**Asked at:** Product cos, GCCs, Amazon
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Statistical vs practical significance: how do you read the confidence interval of the lift and make a ship / no-ship call?
**Asked at:** Amazon, Spotify, Zalando, Flipkart
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 A metric (conversion, orders) dropped after a launch. How would you investigate whether it is real, caused by the launch, or a data issue?
**Asked at:** Swiggy, Flipkart, PhonePe, Amazon, Meta-style
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 AI-era: How would you A/B test an LLM-powered feature (chatbot, summarisation, copilot)? Which metrics (task success, edit/retry rate, latency, token cost, LLM-judge score) and which randomization unit?
**Asked at:** GenAI product teams, Microsoft IDC, Amazon, Spotify, Zalando, Indian product cos
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 Observational vs experimental data: what are confounders and how do you control for them? When would you trust an observational estimate?
**Asked at:** Product cos, Spotify, Booking, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🔴 You cannot randomize (e.g., a pricing change, a regional launch). What are your options for estimating the causal effect?
**Asked at:** Booking, Spotify, Swiggy, Uber, Zalando, Amazon
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 Which statistical test do you use for conversion-rate metrics vs continuous metrics like revenue per user? Explain the two-proportion z-test setup.
**Asked at:** Product cos, GCCs, Amazon India
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 What is A/A testing and why would you run one?
**Asked at:** Microsoft, Booking, Zalando, product cos
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 Compare how you would test a feature with 5 variants (A/B/n): what changes in analysis, sample size and decision?
**Asked at:** Zalando, product cos
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 A product manager says 'the cohort that used the feature has 30% higher retention, so ship it to everyone.' Respond.
**Asked at:** Product cos, Swiggy, Flipkart, Booking
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 What is a holdout / long-term holdout group and why would a company keep one?
**Asked at:** Booking, Spotify, Amazon, ads and growth teams
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 How do you handle outliers and heavy-tailed metrics (revenue, watch time) in an A/B test?
**Asked at:** Flipkart, Swiggy, Amazon, Spotify
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 How do you measure the effect when only some assigned users actually received the treatment? (intent-to-treat vs per-protocol, non-compliance, triggered analysis)
**Asked at:** Microsoft, Booking, Spotify, ads teams
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Ratio metrics (CTR, revenue per session) and per-session vs per-user analysis: what goes wrong with the variance and how do you fix it (delta method)?
**Asked at:** Booking, Microsoft, Amazon, Spotify
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Explain difference-in-differences. What is the parallel-trends assumption and how do you test it?
**Asked at:** Booking, Spotify, Swiggy, Uber, Zalando, Amazon
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 What is a switchback (time-based) experiment? When is it used and what are its pitfalls (carryover, time-of-day effects)?
**Asked at:** Uber, DoorDash-style, Swiggy, Zomato, Booking
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Explain propensity score matching / weighting. When would you use it and how do you check it worked (balance, overlap)?
**Asked at:** Product cos, healthcare and fintech GCCs, Spotify
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 What is Instrumental Variables (IV)? Explain the relevance and exclusion assumptions with an example.
**Asked at:** Booking, Spotify, Amazon, research-leaning DS roles
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Explain Regression Discontinuity Design with an example. What are its assumptions and limits?
**Asked at:** Booking, Spotify, fintech lending teams, Amazon
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 What is uplift modelling? How is it different from a normal propensity/response model?
**Asked at:** Flipkart, Swiggy, PhonePe, fintech, marketing DS
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you evaluate an uplift model offline (Qini curve, AUUC) and online?
**Asked at:** Marketing DS, fintech, Swiggy, Flipkart
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 Explain Average Treatment Effect (ATE), CATE and the potential-outcomes framework. What is the fundamental problem of causal inference?
**Asked at:** Spotify, Booking, Amazon, causal-leaning DS roles
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 What assumptions are needed to estimate causal effects from observational data (SUTVA, unconfoundedness, positivity)?
**Asked at:** Spotify, Booking, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 How would you design an experiment for a marketplace where both buyers/riders and sellers/drivers are affected (a new pricing or dispatch algorithm)?
**Asked at:** Uber, Swiggy, Zomato, Flipkart, Ola, Booking
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 How would you test a new recommendation or ranking algorithm online? Which metrics and what pitfalls (position bias, interleaving)?
**Asked at:** Spotify, Flipkart, Zalando, Netflix-style, Booking
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 How would you A/B test a price change or discount? What are the risks (cannibalization, fairness, price anchoring)?
**Asked at:** Flipkart, Swiggy, Booking, Zalando, Amazon
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 How do you run experiments for a feature with a long-term outcome (retention, LTV) when you cannot wait months? (surrogate metrics, holdouts)
**Asked at:** Spotify, Booking, Netflix-style, Swiggy
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 What is a multi-armed bandit? When would you prefer it to a classic A/B test and what do you lose?
**Asked at:** Booking, Spotify, Zalando, ad-tech
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 Explain selection bias and survivorship bias with experiment or observational examples.
**Asked at:** Product cos, GCCs, FAANG-style
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 A marketing campaign has already run. How do you estimate its incrementality?
**Asked at:** Swiggy, Flipkart, PhonePe, Zalando, Amazon India
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 How would you design and read a geo / city-level experiment when user-level randomization is not possible? (synthetic control, matched markets)
**Asked at:** Swiggy, Uber, Booking, Spotify, ad measurement teams
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 AI-era: Offline LLM evals look better but the online A/B shows no gain or a drop. How do you reconcile and decide?
**Asked at:** GenAI product teams, Microsoft IDC, product cos
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 AI-era: How would you measure the causal impact of AI-assistant adoption on productivity when users self-select into using it?
**Asked at:** Microsoft IDC, GCCs, research-leaning DS roles
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟡 Explain heterogeneous treatment effects: how do you find which segments benefit, and what are the dangers of post-hoc subgroup analysis?
**Asked at:** Spotify, Booking, Amazon, marketing DS
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 What are interaction effects between concurrent experiments and how do mature platforms avoid them (layers, orthogonal hashing)?
**Asked at:** Google-style, Booking, Spotify, Microsoft
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 Explain synthetic control. How is it different from difference-in-differences?
**Asked at:** Booking, Spotify, Uber, research-leaning DS roles
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 What is CUPED / variance reduction? (interview-level only: why it works, when it fails; full treatment in Part 14)
**Asked at:** Spotify, Booking, Microsoft, Zalando
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 How does an interleaving experiment work and why is it more sensitive than A/B for ranking?
**Asked at:** Spotify, Booking, search and recsys teams
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 How do you handle interference with cluster-randomised or graph-cluster experiments? What is the bias-variance tradeoff of cluster size?
**Asked at:** LinkedIn-style, Uber, Spotify, Swiggy
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 Explain double machine learning, causal forests and meta-learners (S-, T-, X-learner) at a high level. When would you use them?
**Asked at:** Research-leaning DS, Booking, Amazon, Uber
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🔴 How would you debug an experiment platform whose results look wrong (SRM, logging loss, bucketing collisions, carryover between experiments)?
**Asked at:** Microsoft, Booking, Spotify, Netflix-style
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🔴 How do you quantify the cumulative impact of many launched experiments (the sum of wins exceeds the real lift)? What is the winner's curse?
**Asked at:** Booking, Spotify, Zalando, growth teams
<!-- ANSWER_PENDING -->

### Q56 ⭐ 🔴 Explain the Bayesian vs frequentist stance for A/B decisions at interview level (when would you pick each?). Deep dive is in Part 14.
**Asked at:** Booking, Spotify, Zalando, startups
<!-- ANSWER_PENDING -->

### Q57 ⭐ 🔴 AI-era: How do you handle a test where the treatment is non-deterministic or changes mid-test (LLM feature, silent provider model updates)?
**Asked at:** GenAI product teams, AI-era loops
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🔴 AI-era: How do you validate an LLM-as-judge metric before using it as an experiment outcome (bias, agreement with humans, variance)?
**Asked at:** GenAI teams, AI-era loops
<!-- ANSWER_PENDING -->
