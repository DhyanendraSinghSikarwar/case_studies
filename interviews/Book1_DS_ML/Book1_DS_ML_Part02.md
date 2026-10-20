# Book 1 — Part 02: Linear/Logistic Regression, Regularization (L1/L2/Elastic Net), Feature Engineering

**Topic:** Linear and logistic regression, regularization, feature engineering
**Target:** >=45 questions | **Actual:** 55 questions | **Date:** 2026-10-20
**Status:** Phase 1 (questions only, answers pending)

---

### Q1 ⭐⭐⭐ 🟢 Why can't we use linear regression for a classification problem? Why logistic regression instead?
**Asked at:** Flipkart, Swiggy, GCCs, startups
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What are the assumptions of linear regression, and what happens to the model if each is violated? (interview-level)
**Asked at:** Product cos, GCCs, consulting (ZS, Accenture), Europe
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is logistic regression? Is it a linear model, and what do the sigmoid and log-odds do?
**Asked at:** Swiggy, Flipkart, Klarna, GCCs
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What is regularization and why do we need it? How does it relate to bias-variance?
**Asked at:** All company types
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 L1 vs L2 regularization: how do they differ, and why does L1 give sparse weights while L2 only shrinks?
**Asked at:** Flipkart, Swiggy, Amazon, Europe product cos
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 What is the difference between R-squared and adjusted R-squared? Can R-squared be negative?
**Asked at:** Swiggy, consulting/analytics, GCCs
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 How do you interpret the coefficients of a linear regression and of a logistic regression (odds ratio)? If one weight is larger, is that feature more important?
**Asked at:** Product cos, fintech, GCCs
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 What is multicollinearity? How does it affect linear regression, how do you detect it (VIF), and how do you fix it?
**Asked at:** Product cos, GCCs, C3 AI-type, Europe
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Derive the logistic regression loss (MLE / log loss) and its gradient. Why not use MSE for logistic regression?
**Asked at:** Flipkart (DS-2 math round), Amazon, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Does feature scaling matter for linear regression, logistic regression and regularized models? When can you skip it?
**Asked at:** Accenture-type lists, product cos, Swiggy
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 How do you handle categorical variables for linear/logistic models? One-hot vs ordinal vs target/frequency encoding, and the dummy-variable trap.
**Asked at:** Flipkart, Swiggy, Amazon, Europe
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 How do you choose between Lasso and Ridge for a given problem, and how do you pick the regularization strength (CV)?
**Asked at:** Swiggy, Segment/Coupang-type, product cos
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How do you handle missing values in a feature pipeline? Compare drop, mean/median, model-based, missing-indicator flags.
**Asked at:** All company types
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 What is data leakage in feature engineering and preprocessing (scaling, imputation, target encoding)? How do you prevent it with pipelines?
**Asked at:** Product cos, fintech, Klarna, Amazon
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Walk me through feature engineering on a project you did. Which features moved the metric and how did you validate them?
**Asked at:** Swiggy, Flipkart, Zalando, PhonePe, all resume-drill rounds
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 What feature-selection methods do you know (filter, wrapper, embedded)? Is feature selection important for linear models, and can L1/L2 do it?
**Asked at:** Product cos, GCCs, consulting
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 How do you solve linear regression: normal equation vs gradient descent (batch/SGD/mini-batch)? When do you prefer which?
**Asked at:** Amazon, Microsoft IDC, Flipkart, consulting
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 Which regression error metric would you choose: MSE, RMSE, MAE, Huber, MAPE? How does the choice affect the model with outliers?
**Asked at:** Zalando, product cos, GCCs
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 What is Elastic Net, and when would you use it over Lasso or Ridge?
**Asked at:** Product cos, GCCs, Europe
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 What is the dummy variable trap, and how does drop-first/intercept handling resolve it?
**Asked at:** Consulting, GCCs, analytics roles
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 Why does regularization not usually penalize the intercept, and why must features be standardized before applying a penalty?
**Asked at:** Product cos, Amazon
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 Normalization vs standardization vs robust scaling: which to use when, and how do outliers affect each?
**Asked at:** Product cos, GCCs, startups
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 If one column is the sum of two others (or the sum plus noise), what happens to a linear model and to its Ridge/Lasso version?
**Asked at:** Grigorev-style theory banks, product cos
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Why does Ridge fix the singular XtX problem? Write the closed-form Ridge solution and explain shrinkage.
**Asked at:** Amazon, Microsoft IDC, research-leaning roles
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 How does L2 regularization appear in logistic regression (sklearn's C parameter, MAP view)? How does it change the gradient?
**Asked at:** Flipkart (DS-2 math round), Amazon, fintech
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 How do you choose lambda in practice (LassoCV/RidgeCV, one-standard-error rule, regularization path) and what do you do if CV curves are flat?
**Asked at:** Product cos, Europe
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Logistic regression decision boundary is linear. How do you capture non-linearity (interactions, polynomial features, splines, binning)?
**Asked at:** Product cos, fintech, GCCs
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How do outliers affect linear regression and what robust options exist (winsorizing, Huber, quantile regression)?
**Asked at:** Product cos, GCCs, consulting
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Target is right-skewed (e.g., price, delivery time). Do you log-transform it? How do you interpret results and avoid back-transform bias?
**Asked at:** Swiggy, Flipkart, Zalando, pricing/ETA teams
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 How do you handle high-cardinality categoricals (city, pincode, SKU, user ID)? Compare target encoding, frequency encoding, hashing, embeddings, grouping rare levels.
**Asked at:** Flipkart, Swiggy, Zalando, PhonePe, Booking
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 How do you do target encoding without leakage (out-of-fold, smoothing)? Why does naive target encoding overfit?
**Asked at:** Product cos, Kaggle-style rounds, fintech
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you engineer features from timestamps and recency/frequency data (cyclical encoding, lags, rolling aggregates, RFM)?
**Asked at:** Swiggy, Flipkart, PhonePe, Klarna, fintech
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Multiclass logistic regression: softmax vs one-vs-rest, and how the loss and gradients change.
**Asked at:** Amazon, Microsoft IDC, GCCs
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 Why is logistic regression still widely used in industry (CTR, credit scoring, baseline)? When do you pick it over a tree ensemble?
**Asked at:** Fintech (Klarna, PhonePe), ads, GCCs
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 How do you compute feature importance for linear/logistic models (standardized coefficients, permutation importance) and what can go wrong with correlated features?
**Asked at:** Product cos, GCCs, Europe
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 A coefficient's sign flips or becomes insignificant after adding a variable. What are the possible reasons (collinearity, confounding, omitted variable)?
**Asked at:** Consulting, product cos, Europe
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 How do you build and evaluate a text-feature baseline (bag-of-words/TF-IDF + logistic regression)? What regularization works for sparse high-dimensional input?
**Asked at:** Product cos, search/e-commerce
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 Training-serving skew for features: how do you ensure the same transformations run offline and online?
**Asked at:** Product cos, MLE roles, Amazon
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 AI-era: an LLM generated this sklearn pipeline (scaler fit on full data, target encoding before split, p-value-based feature dropping). Review it and list the bugs.
**Asked at:** AI-era code-review rounds, product cos, GCCs
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🔴 How does Lasso behave with correlated features, and how do Elastic Net or stability selection address it?
**Asked at:** Product cos, C3 AI-type, research-leaning roles
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🔴 Explain L1 and L2 as Bayesian priors (Laplace vs Gaussian) and give the geometric (constraint-region) intuition.
**Asked at:** Amazon, Microsoft IDC, Europe research-leaning
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🔴 What is perfect (quasi-)separation in logistic regression? What happens to the coefficients and how do you fix it?
**Asked at:** Fintech, GCCs, statistics-heavy roles
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🔴 How do you do Weight of Evidence binning and Information Value for logistic scorecards, and what are the pitfalls?
**Asked at:** Klarna, JPMC, Amex, fintech GCCs
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🟢 How do linear models treat ordinal, nominal and binary features differently from tree models?
**Asked at:** GCCs, analytics roles
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🟡 What is p > n (high-dimensional) regression, why does OLS fail, and what are your options?
**Asked at:** Research-leaning, genomics/health, Europe
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🟡 Poisson, Tweedie and Gamma GLMs: when would you use them instead of OLS (counts, claims, ETA, demand)?
**Asked at:** Insurance, delivery/ETA, pricing, Booking
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟡 What is quantile regression and when is it preferred to OLS (SLA, ETA P90, pricing)?
**Asked at:** Swiggy, Uber-style, Booking, Europe
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 Feature crosses and hashing at scale in linear CTR models: why do ads systems still use them?
**Asked at:** Ads teams, Flipkart, Amazon, Spotify
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🟡 Principal-component regression vs Ridge vs PLS: when would you choose each?
**Asked at:** Research-leaning, GCC analytics
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🟡 Does feature engineering still matter in the LLM/embeddings era? How would you use embeddings as features in a regularized linear model?
**Asked at:** AI-era DS loops, Spotify, Zalando, Klarna
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🟡 How do you do inference (p-values, CIs) after Lasso selection, and why are naive p-values invalid?
**Asked at:** Statistics-heavy roles, Europe research
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🟡 Generalized Additive Models and monotonic constraints as interpretable alternatives to plain logistic regression in credit/insurance.
**Asked at:** Fintech, regulated GCCs, Klarna
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 Implement coordinate-descent Lasso (soft-thresholding) in NumPy and explain why it yields exact zeros.
**Asked at:** Research-leaning, Amazon applied science
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🔴 Derive the bias and variance of the Ridge estimator and show how shrinkage trades bias for variance.
**Asked at:** Research-leaning, Amazon applied science, Europe
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🔴 Marginal effects in logistic regression: why is a coefficient not a constant change in probability, and how do you report average marginal effects?
**Asked at:** Economics-flavoured DS roles, Europe, consulting
<!-- ANSWER_PENDING -->
