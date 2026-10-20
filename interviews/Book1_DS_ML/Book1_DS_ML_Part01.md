# Book 1 — Part 01: Stats/Probability Basics, ML Fundamentals, From-Scratch Code

**Topic:** Statistics & probability essentials, ML fundamentals (bias-variance, overfitting, CV, leakage, splits), from-scratch NumPy
**Target:** >=30 questions  |  **Actual:** 36  |  **Date:** 2026-10-20
**Lane note:** deep stats -> Parts 13-14; regression/regularization -> Part 2.

### Q1 ⭐⭐⭐ 🟢 Explain the bias-variance tradeoff. How do you diagnose which one your model suffers from (learning curves)?
**Asked at:** Flipkart, Amazon, Fractal, product cos, GCCs
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is overfitting? How do you detect it and what are your options to fix it?
**Asked at:** Swiggy, Flipkart, Amazon, Fractal, most loops
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Supervised vs unsupervised vs semi/self-supervised vs reinforcement learning: differences with one example each.
**Asked at:** Zalando, Indian services/analytics firms, screening rounds
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Why do we split data into train / validation / test? Why must the test set stay untouched until the end?
**Asked at:** Almost all companies, screening rounds
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What is cross-validation? How does k-fold work, how do you choose k, and when does it fail?
**Asked at:** Amazon, Flipkart, GCCs, Europe product cos
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 Covariance vs correlation, Pearson vs Spearman, and correlation vs causation.
**Asked at:** Amazon, Walmart GCC, analytics firms
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 What is data leakage? Give 4 real examples (target, preprocessing, temporal, group) and how you would detect it.
**Asked at:** Amazon, Klarna, Booking, PhonePe, senior loops
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Do feature scaling and missing-value imputation belong before or after the split? Which models need scaling and why?
**Asked at:** Flipkart, Swiggy, GCCs, live-coding rounds
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Walk me through how you would approach a new ML problem end to end (framing, baseline, metric, validation, iteration).
**Asked at:** Fractal, Swiggy, Zalando, Spotify, all case rounds
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Implement linear regression from scratch in NumPy (normal equation and gradient descent). What are the complexity trade-offs?
**Asked at:** Booking.com, Robinhood, Brex, Flipkart, product cos
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Implement logistic regression from scratch with gradient descent. Why clip/stabilise the sigmoid, and what happens if the learning rate is too high or low?
**Asked at:** Booking.com, Splunk, Flipkart, Amazon, MLE screens
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Implement k-means from scratch in NumPy (init, assignment, update, convergence, empty clusters).
**Asked at:** Booking.com, Splunk, Swiggy, MLE screens
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Implement k-nearest neighbours from scratch. How does choice of k and distance metric affect bias/variance, and how do you make prediction fast?
**Asked at:** Microsoft IDC, Walmart GCC, MLE screens
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Explain gradient descent: batch vs stochastic vs mini-batch, learning rate, convergence, local minima.
**Asked at:** Flipkart, Amazon, Swiggy, deep-learning-leaning loops
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 What is the difference between parameters and hyperparameters? Name examples for 3 models.
**Asked at:** Indian services/analytics firms, JPMC GCC
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 Explain the curse of dimensionality and its effect on KNN and distance-based methods.
**Asked at:** Flipkart, Amazon, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 Descriptive statistics refresher: mean vs median vs mode, variance/std, skewness; which summary would you report for skewed income data?
**Asked at:** Analytics firms, Walmart GCC, screening rounds
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 Stratified, random and cluster sampling; what is sampling bias and selection bias in training data?
**Asked at:** Amazon, Walmart, Europe product cos
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 Tell me conditional probability and Bayes' rule, then explain how Naive Bayes uses them and why 'naive'.
**Asked at:** Flipkart, Amazon, Microsoft IDC, GCCs
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Your model has 99% train accuracy and 70% validation accuracy. What do you check and change, in order?
**Asked at:** Fractal, Swiggy, PhonePe, scenario rounds
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 How do you split data for time-series, grouped (user-level) or duplicated data? Why does random k-fold leak there?
**Asked at:** Klarna, Booking, Swiggy, PhonePe
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 How do you handle missing values? Compare dropping, mean/median, model-based imputation and missing-indicator features; when is missingness informative?
**Asked at:** Flipkart, Swiggy, Walmart, analytics firms
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Grid search vs random search vs Bayesian optimisation. What is nested cross-validation and why use it?
**Asked at:** Amazon, Zalando, GCCs
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Parametric vs non-parametric models, and generative vs discriminative models: definitions and examples.
**Asked at:** Microsoft IDC, Amazon, research-leaning roles
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Why does vectorised NumPy beat Python loops? Explain broadcasting and compute pairwise Euclidean distances without a loop.
**Asked at:** MLE live-coding, Microsoft IDC, Booking
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Implement train_test_split and stratified k-fold from scratch (no sklearn). How do you guarantee reproducibility?
**Asked at:** MLE screens, GCC coding rounds
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Implement softmax and cross-entropy in NumPy in a numerically stable way (log-sum-exp).
**Asked at:** Amazon, deep-learning-leaning MLE loops
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Your model is great offline but poor in production. List the causes (train-serve skew, drift, leakage, label delay) and how to investigate.
**Asked at:** Swiggy, Flipkart, Spotify, Zalando, senior loops
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Explain interpretability vs accuracy trade-off: when would you pick a simpler model, and how do you explain a model to non-technical stakeholders?
**Asked at:** Klarna, Fractal, Walmart, JPMC GCC
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 AI-era code review: an LLM wrote this sklearn pipeline (scaler fit on all data, random split on time-ordered data, test set used for tuning). Find the bugs.
**Asked at:** AI-era loops: Meta-style, product cos, MLE live-coding rounds
<!-- ANSWER_PENDING -->

### Q31 ⭐ 🟡 Why does MSE pair with regression and cross-entropy with classification? Explain MLE vs MAP in one minute.
**Asked at:** Research-leaning roles, Amazon applied scientist
<!-- ANSWER_PENDING -->

### Q32 ⭐ 🟡 Explain bootstrap and bagging intuition: why does resampling and averaging reduce variance?
**Asked at:** Amazon, Microsoft IDC, senior loops
<!-- ANSWER_PENDING -->

### Q33 ⭐ 🟡 Write a gradient check (numerical vs analytical gradient) for your from-scratch model. Why is it useful?
**Asked at:** Deep-learning-leaning MLE loops
<!-- ANSWER_PENDING -->

### Q34 ⭐ 🟡 AI-era follow-up: how can benchmark/test contamination happen when fine-tuning or evaluating an LLM, and how is it the same as classical data leakage?
**Asked at:** GenAI-leaning DS loops, Fractal-style GenAI scenario rounds
<!-- ANSWER_PENDING -->

### Q35 ⭐ 🔴 Derive the bias-variance decomposition of expected squared error. Why is irreducible noise separate?
**Asked at:** Research-leaning roles, Amazon applied scientist
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🔴 AI-era follow-up: does bias-variance still hold for huge models (double descent)? How do you reconcile it with 'big models don't overfit'?
**Asked at:** Senior/GenAI-leaning loops, Europe research teams
<!-- ANSWER_PENDING -->
