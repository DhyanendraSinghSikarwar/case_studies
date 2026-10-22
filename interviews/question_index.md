# question_index.md
Canonical questions per book. Wave A agents: check this BEFORE adding a question (avoid cross-part duplicates); append only your own rows.

## Book 1 — DS / ML Technical
| Q-ID | Part | Canonical question |
|---|---|---|
| B1P01-Q1 | 1 | Explain the bias-variance tradeoff. How do you diagnose which one your model suffers from (learning curves)? |
| B1P01-Q2 | 1 | What is overfitting? How do you detect it and what are your options to fix it? |
| B1P01-Q3 | 1 | Supervised vs unsupervised vs semi/self-supervised vs reinforcement learning: differences with one example each. |
| B1P01-Q4 | 1 | Why do we split data into train / validation / test? Why must the test set stay untouched until the end? |
| B1P01-Q5 | 1 | What is cross-validation? How does k-fold work, how do you choose k, and when does it fail? |
| B1P01-Q6 | 1 | Covariance vs correlation, Pearson vs Spearman, and correlation vs causation. |
| B1P01-Q7 | 1 | What is data leakage? Give 4 real examples (target, preprocessing, temporal, group) and how you would detect it. |
| B1P01-Q8 | 1 | Do feature scaling and missing-value imputation belong before or after the split? Which models need scaling and why? |
| B1P01-Q9 | 1 | Walk me through how you would approach a new ML problem end to end (framing, baseline, metric, validation, iteration). |
| B1P01-Q10 | 1 | Implement linear regression from scratch in NumPy (normal equation and gradient descent). What are the complexity trade-offs? |
| B1P01-Q11 | 1 | Implement logistic regression from scratch with gradient descent. Why clip/stabilise the sigmoid, and what happens if the learning rate is too high or low? |
| B1P01-Q12 | 1 | Implement k-means from scratch in NumPy (init, assignment, update, convergence, empty clusters). |
| B1P01-Q13 | 1 | Implement k-nearest neighbours from scratch. How does choice of k and distance metric affect bias/variance, and how do you make prediction fast? |
| B1P01-Q14 | 1 | Explain gradient descent: batch vs stochastic vs mini-batch, learning rate, convergence, local minima. |
| B1P01-Q15 | 1 | What is the difference between parameters and hyperparameters? Name examples for 3 models. |
| B1P01-Q16 | 1 | Explain the curse of dimensionality and its effect on KNN and distance-based methods. |
| B1P01-Q17 | 1 | Descriptive statistics refresher: mean vs median vs mode, variance/std, skewness; which summary would you report for skewed income data? |
| B1P01-Q18 | 1 | Stratified, random and cluster sampling; what is sampling bias and selection bias in training data? |
| B1P01-Q19 | 1 | Tell me conditional probability and Bayes' rule, then explain how Naive Bayes uses them and why 'naive'. |
| B1P01-Q20 | 1 | Your model has 99% train accuracy and 70% validation accuracy. What do you check and change, in order? |
| B1P01-Q21 | 1 | How do you split data for time-series, grouped (user-level) or duplicated data? Why does random k-fold leak there? |
| B1P01-Q22 | 1 | How do you handle missing values? Compare dropping, mean/median, model-based imputation and missing-indicator features; when is missingness informative? |
| B1P01-Q23 | 1 | Grid search vs random search vs Bayesian optimisation. What is nested cross-validation and why use it? |
| B1P01-Q24 | 1 | Parametric vs non-parametric models, and generative vs discriminative models: definitions and examples. |
| B1P01-Q25 | 1 | Why does vectorised NumPy beat Python loops? Explain broadcasting and compute pairwise Euclidean distances without a loop. |
| B1P01-Q26 | 1 | Implement train_test_split and stratified k-fold from scratch (no sklearn). How do you guarantee reproducibility? |
| B1P01-Q27 | 1 | Implement softmax and cross-entropy in NumPy in a numerically stable way (log-sum-exp). |
| B1P01-Q28 | 1 | Your model is great offline but poor in production. List the causes (train-serve skew, drift, leakage, label delay) and how to investigate. |
| B1P01-Q29 | 1 | Explain interpretability vs accuracy trade-off: when would you pick a simpler model, and how do you explain a model to non-technical stakeholders? |
| B1P01-Q30 | 1 | AI-era code review: an LLM wrote this sklearn pipeline (scaler fit on all data, random split on time-ordered data, test set used for tuning). Find the bugs. |
| B1P01-Q31 | 1 | Why does MSE pair with regression and cross-entropy with classification? Explain MLE vs MAP in one minute. |
| B1P01-Q32 | 1 | Explain bootstrap and bagging intuition: why does resampling and averaging reduce variance? |
| B1P01-Q33 | 1 | Write a gradient check (numerical vs analytical gradient) for your from-scratch model. Why is it useful? |
| B1P01-Q34 | 1 | AI-era follow-up: how can benchmark/test contamination happen when fine-tuning or evaluating an LLM, and how is it the same as classical data leakage? |
| B1P01-Q35 | 1 | Derive the bias-variance decomposition of expected squared error. Why is irreducible noise separate? |
| B1P02-Q1 | 2 | Why can't we use linear regression for a classification problem? Why logistic regression instead? |
| B1P02-Q2 | 2 | What are the assumptions of linear regression, and what happens to the model if each is violated? (interview-level) |
| B1P02-Q3 | 2 | What is logistic regression? Is it a linear model, and what do the sigmoid and log-odds do? |
| B1P02-Q4 | 2 | What is regularization and why do we need it? How does it relate to bias-variance? |
| B1P02-Q5 | 2 | L1 vs L2 regularization: how do they differ, and why does L1 give sparse weights while L2 only shrinks? |
| B1P02-Q6 | 2 | What is the difference between R-squared and adjusted R-squared? Can R-squared be negative? |
| B1P02-Q7 | 2 | How do you interpret the coefficients of a linear regression and of a logistic regression (odds ratio)? If one weight is larger, is that feature more important? |
| B1P02-Q8 | 2 | What is multicollinearity? How does it affect linear regression, how do you detect it (VIF), and how do you fix it? |
| B1P02-Q9 | 2 | Derive the logistic regression loss (MLE / log loss) and its gradient. Why not use MSE for logistic regression? |
| B1P02-Q10 | 2 | How do you handle categorical variables for linear/logistic models? One-hot vs ordinal vs target/frequency encoding, and the dummy-variable trap. |
| B1P02-Q11 | 2 | How do you choose between Lasso and Ridge for a given problem, and how do you pick the regularization strength (CV)? |
| B1P02-Q12 | 2 | Walk me through feature engineering on a project you did. Which features moved the metric and how did you validate them? |
| B1P02-Q13 | 2 | What feature-selection methods do you know (filter, wrapper, embedded)? Is feature selection important for linear models, and can L1/L2 do it? |
| B1P02-Q14 | 2 | How do you solve linear regression: normal equation vs gradient descent (batch/SGD/mini-batch)? When do you prefer which? |
| B1P02-Q15 | 2 | Which regression error metric would you choose: MSE, RMSE, MAE, Huber, MAPE? How does the choice affect the model with outliers? |
| B1P02-Q16 | 2 | What is Elastic Net, and when would you use it over Lasso or Ridge? |
| B1P02-Q17 | 2 | What is the dummy variable trap, and how does drop-first/intercept handling resolve it? |
| B1P02-Q18 | 2 | Why does regularization not usually penalize the intercept, and why must features be standardized before applying a penalty? |
| B1P02-Q19 | 2 | Normalization vs standardization vs robust scaling: which to use when, and how do outliers affect each? |
| B1P02-Q20 | 2 | If one column is the sum of two others (or the sum plus noise), what happens to a linear model and to its Ridge/Lasso version? |
| B1P02-Q21 | 2 | Why does Ridge fix the singular XtX problem? Write the closed-form Ridge solution and explain shrinkage. |
| B1P02-Q22 | 2 | How does L2 regularization appear in logistic regression (sklearn's C parameter, MAP view)? How does it change the gradient? |
| B1P02-Q23 | 2 | How do you choose lambda in practice (LassoCV/RidgeCV, one-standard-error rule, regularization path) and what do you do if CV curves are flat? |
| B1P02-Q24 | 2 | Logistic regression decision boundary is linear. How do you capture non-linearity (interactions, polynomial features, splines, binning)? |
| B1P02-Q25 | 2 | How do outliers affect linear regression and what robust options exist (winsorizing, Huber, quantile regression)? |
| B1P02-Q26 | 2 | Target is right-skewed (e.g., price, delivery time). Do you log-transform it? How do you interpret results and avoid back-transform bias? |
| B1P02-Q27 | 2 | How do you handle high-cardinality categoricals (city, pincode, SKU, user ID)? Compare target encoding, frequency encoding, hashing, embeddings, grouping rare levels. |
| B1P02-Q28 | 2 | How do you do target encoding without leakage (out-of-fold, smoothing)? Why does naive target encoding overfit? |
| B1P02-Q29 | 2 | How do you engineer features from timestamps and recency/frequency data (cyclical encoding, lags, rolling aggregates, RFM)? |
| B1P02-Q30 | 2 | Multiclass logistic regression: softmax vs one-vs-rest, and how the loss and gradients change. |
| B1P02-Q31 | 2 | Why is logistic regression still widely used in industry (CTR, credit scoring, baseline)? When do you pick it over a tree ensemble? |
| B1P02-Q32 | 2 | How do you compute feature importance for linear/logistic models (standardized coefficients, permutation importance) and what can go wrong with correlated features? |
| B1P02-Q33 | 2 | A coefficient's sign flips or becomes insignificant after adding a variable. What are the possible reasons (collinearity, confounding, omitted variable)? |
| B1P02-Q34 | 2 | How do you build and evaluate a text-feature baseline (bag-of-words/TF-IDF + logistic regression)? What regularization works for sparse high-dimensional input? |
| B1P02-Q35 | 2 | Training-serving skew for features: how do you ensure the same transformations run offline and online? |
| B1P02-Q36 | 2 | AI-era: an LLM generated this sklearn pipeline (scaler fit on full data, target encoding before split, p-value-based feature dropping). Review it and list the bugs. |
| B1P02-Q37 | 2 | How does Lasso behave with correlated features, and how do Elastic Net or stability selection address it? |
| B1P02-Q38 | 2 | What is perfect (quasi-)separation in logistic regression? What happens to the coefficients and how do you fix it? |
| B1P02-Q39 | 2 | How do you do Weight of Evidence binning and Information Value for logistic scorecards, and what are the pitfalls? |
| B1P02-Q40 | 2 | How do linear models treat ordinal, nominal and binary features differently from tree models? |
| B1P02-Q41 | 2 | What is p > n (high-dimensional) regression, why does OLS fail, and what are your options? |
| B1P02-Q42 | 2 | Poisson, Tweedie and Gamma GLMs: when would you use them instead of OLS (counts, claims, ETA, demand)? |
| B1P02-Q43 | 2 | What is quantile regression and when is it preferred to OLS (SLA, ETA P90, pricing)? |
| B1P02-Q44 | 2 | Feature crosses and hashing at scale in linear CTR models: why do ads systems still use them? |
| B1P02-Q45 | 2 | Principal-component regression vs Ridge vs PLS: when would you choose each? |
| B1P02-Q46 | 2 | Does feature engineering still matter in the LLM/embeddings era? How would you use embeddings as features in a regularized linear model? |
| B1P02-Q47 | 2 | How do you do inference (p-values, CIs) after Lasso selection, and why are naive p-values invalid? |
| B1P02-Q48 | 2 | Generalized Additive Models and monotonic constraints as interpretable alternatives to plain logistic regression in credit/insurance. |
| B1P02-Q49 | 2 | Implement coordinate-descent Lasso (soft-thresholding) in NumPy and explain why it yields exact zeros. |
| B1P02-Q50 | 2 | Derive the bias and variance of the Ridge estimator and show how shrinkage trades bias for variance. |
| B1P02-Q51 | 2 | Marginal effects in logistic regression: why is a coefficient not a constant change in probability, and how do you report average marginal effects? |
| B1P03-Q1 | 3 | Why is accuracy a misleading metric on imbalanced data? Give a numeric example. |
| B1P03-Q2 | 3 | Define precision, recall, specificity and F1 from the confusion matrix. Given TP/FP/FN/TN counts, compute them. |
| B1P03-Q3 | 3 | Precision vs recall trade-off: which would you optimise for fraud, cancer screening and a spam filter, and why? |
| B1P03-Q4 | 3 | What is stratified splitting / stratified k-fold and why is it essential for imbalanced data? |
| B1P03-Q5 | 3 | What does ROC-AUC actually mean (probabilistic interpretation)? What is the AUC of a random model and of a perfectly inverted one? |
| B1P03-Q6 | 3 | ROC-AUC vs PR-AUC: when would you prefer each on an imbalanced problem, and why can ROC-AUC look deceptively good? |
| B1P03-Q7 | 3 | How is F1 different from ROC-AUC? Can you have high AUC and low F1? |
| B1P03-Q8 | 3 | How do you handle class imbalance? Walk through the options and how you choose between them. |
| B1P03-Q9 | 3 | How does SMOTE work and what are its limitations (high dimensions, categorical data, noise, overlapping classes)? |
| B1P03-Q10 | 3 | Where in the pipeline do you apply SMOTE or resampling? Does it touch the validation/test set? What goes wrong if you resample before the split? |
| B1P03-Q11 | 3 | Class weights vs resampling (over/under-sampling): trade-offs, and which would you try first? |
| B1P03-Q12 | 3 | How do you choose the classification threshold? Why is 0.5 arbitrary and how do you pick a better one? |
| B1P03-Q13 | 3 | What is log-loss (binary cross-entropy)? Why is it preferred to accuracy for training and for comparing probabilistic models? |
| B1P03-Q14 | 3 | What is model calibration and why can a model with great AUC still be badly calibrated? |
| B1P03-Q15 | 3 | Fraud model with a 0.1% positive rate: design the evaluation end to end (split strategy, metrics, threshold, what you report to the business). |
| B1P03-Q16 | 3 | Your model reports 99% accuracy but recall on the minority class is poor. How do you debug and improve it? |
| B1P03-Q17 | 3 | Multiclass metrics: macro vs micro vs weighted F1. When do you pick each? |
| B1P03-Q18 | 3 | What is F-beta? When would you use F2 or F0.5 instead of F1? |
| B1P03-Q19 | 3 | Implement precision, recall, F1 and a precision-recall curve from scratch in NumPy. |
| B1P03-Q20 | 3 | Platt scaling vs isotonic regression: how each works, when each is appropriate, and why you fit them on held-out data. |
| B1P03-Q21 | 3 | How do you measure calibration? Explain reliability diagrams, ECE and Brier score, and ECE's weaknesses. |
| B1P03-Q22 | 3 | Which model families tend to be poorly calibrated (RF, SVM, naive Bayes, boosted trees, deep nets) and why? Which are well calibrated? |
| B1P03-Q23 | 3 | Does class weighting, SMOTE or undersampling break probability calibration? How do you correct predicted probabilities back to the true base rate? |
| B1P03-Q24 | 3 | What is cost-sensitive learning? How do you incorporate different FP and FN costs (loss weights, threshold shift, cost matrix)? |
| B1P03-Q25 | 3 | Capacity-constrained operating point: reviewers can check 500 cases a day. How do you pick the threshold and report precision@k / recall@k? |
| B1P03-Q26 | 3 | Explain lift, gain and cumulative-gain charts and the KS statistic. How do you use them for churn or marketing targeting? |
| B1P03-Q27 | 3 | PR-AUC: what is its random baseline, and what is the difference between average precision and trapezoidal area under the PR curve? |
| B1P03-Q28 | 3 | Undersampling vs oversampling vs hybrid methods; what are balanced random forest and EasyEnsemble and when do they help? |
| B1P03-Q29 | 3 | MCC, balanced accuracy and Cohen's kappa: what do they fix that F1 does not? |
| B1P03-Q30 | 3 | Precision depends on class prevalence. If the production base rate differs from validation, how do metrics change? Use Bayes to explain. |
| B1P03-Q31 | 3 | Why can AUC be high while precision at a usable threshold is very low? Give a worked example. |
| B1P03-Q32 | 3 | Should you tune the threshold on train, validation or test data? How do you avoid overfitting the threshold, and would you use one threshold per segment? |
| B1P03-Q33 | 3 | Log-loss vs Brier vs AUC: which do you choose when probabilities feed a downstream decision (bidding, pricing, risk scoring)? |
| B1P03-Q34 | 3 | Fraud/credit labels arrive late (chargebacks after 30-90 days). How does this affect training and evaluation, and how do you split the data? |
| B1P03-Q35 | 3 | How do you compare two classifiers statistically? Bootstrap CI for AUC, DeLong test, McNemar test. |
| B1P03-Q36 | 3 | How do you extend ROC-AUC and calibration to multiclass problems (one-vs-rest, one-vs-one, macro/weighted)? |
| B1P03-Q37 | 3 | What is focal loss and when does it help with class imbalance compared to class weights? |
| B1P03-Q38 | 3 | Implement ROC-AUC from scratch in NumPy (rank-based, handling ties) and verify against sklearn. |
| B1P03-Q39 | 3 | A product manager asks for one number to judge a classifier. How do you negotiate the metric and translate a confusion matrix into rupees/euros of business value? |
| B1P03-Q40 | 3 | You use an LLM as a classifier or judge to label data. How do you evaluate it (metrics, imbalance, agreement with humans, calibration)? |
| B1P03-Q41 | 3 | Derive the Bayes-optimal threshold for a given cost matrix and explain why it needs calibrated probabilities. |
| B1P03-Q42 | 3 | What is partial AUC or recall at a fixed false-positive rate? When is full AUC the wrong objective? |
| B1P03-Q43 | 3 | Selective classification (reject option) and conformal prediction: how do you give classifiers an abstain option or a coverage guarantee? |
| B1P03-Q44 | 3 | Temperature scaling: how does it work, why is it used for neural nets, and how does calibration of LLM classifiers (logprobs, verbalized confidence) differ? |
| B1P03-Q45 | 3 | Code review: an LLM wrote a churn pipeline that applies SMOTE before train_test_split, reports accuracy, and tunes the threshold on the test set. List all the bugs and fix them. |
| B1P03-Q46 | 3 | Positive-unlabeled learning and noisy labels: when negatives are really unlabeled, how does that change metrics and training? |
| B1P03-Q47 | 3 | At 1:10,000 imbalance, when would you switch from supervised learning to anomaly detection or a hybrid approach? |
| B1P03-Q48 | 3 | Fairness and thresholds: equalized odds vs group calibration; can you satisfy both? How do you handle per-group thresholds? |
| B1P04-Q1 | 4 | How does a decision tree choose where to split? Compare Gini impurity, entropy and information gain. |
| B1P04-Q2 | 4 | Bagging vs boosting: what is the difference and how does each affect bias and variance? |
| B1P04-Q3 | 4 | What are the key hyperparameters of a Random Forest and how does each affect bias/variance? |
| B1P04-Q4 | 4 | Why does a Random Forest overfit less than a single decision tree? Explain bootstrap sampling and feature subsampling. |
| B1P04-Q5 | 4 | What is the difference between Random Forest and XGBoost, and when would you pick each? |
| B1P04-Q6 | 4 | How do you prevent overfitting in a decision tree? Explain pre-pruning, post-pruning and cost-complexity pruning. |
| B1P04-Q7 | 4 | Explain gradient boosting step by step. Why is it called gradient boosting? |
| B1P04-Q8 | 4 | What makes XGBoost different from classic gradient boosting (GBM)? |
| B1P04-Q9 | 4 | How would you tune XGBoost hyperparameters? Which matter most and in what order? |
| B1P04-Q10 | 4 | Compare XGBoost, LightGBM and CatBoost: speed, categorical handling, growth strategy, when to use which. |
| B1P04-Q11 | 4 | How do you control overfitting in boosting models? Where does early stopping fit in? |
| B1P04-Q12 | 4 | How is feature importance computed in tree models (split count, gain/impurity, permutation)? What are the pitfalls? |
| B1P04-Q13 | 4 | What is SHAP? How does it differ from built-in feature importance (global vs local)? |
| B1P04-Q14 | 4 | How do tree-based models handle missing values, categorical variables, outliers and unscaled features? |
| B1P04-Q15 | 4 | Single decision tree vs ensemble (Random Forest / XGBoost): what are the trade-offs? |
| B1P04-Q16 | 4 | Work through a small table by hand: compute Gini/entropy and pick the best split. |
| B1P04-Q17 | 4 | How does a regression tree split and what does a leaf predict? |
| B1P04-Q18 | 4 | What is out-of-bag (OOB) error in a Random Forest and how is it used? |
| B1P04-Q19 | 4 | How do learning rate and number of trees trade off in boosting? |
| B1P04-Q20 | 4 | AdaBoost vs gradient boosting: how do they differ? |
| B1P04-Q21 | 4 | Extra Trees vs Random Forest: what is different and when is Extra Trees better? |
| B1P04-Q22 | 4 | Why is impurity-based (MDI) importance biased, and how does permutation importance help? |
| B1P04-Q23 | 4 | How does permutation importance behave with correlated features? What would you do about it? |
| B1P04-Q24 | 4 | How do you handle imbalanced data in XGBoost / Random Forest (scale_pos_weight, class_weight, sampling, metric)? |
| B1P04-Q25 | 4 | Level-wise vs leaf-wise tree growth: what do they mean, and how do num_leaves and max_depth interact in LightGBM? |
| B1P04-Q26 | 4 | Grid vs random vs Bayesian (Optuna) search for tree models: which do you choose and how do you cross-validate? |
| B1P04-Q27 | 4 | Why can't tree-based models extrapolate, and what do you do when you need to? |
| B1P04-Q28 | 4 | How do you read SHAP plots (summary/beeswarm, dependence, waterfall) and what decisions do they support? |
| B1P04-Q29 | 4 | How do you handle high-cardinality categorical features with tree models? Why can one-hot encoding hurt? |
| B1P04-Q30 | 4 | Code: implement a best-split finder (or a small decision tree) from scratch in NumPy. |
| B1P04-Q31 | 4 | Code: implement a Random Forest from scratch (bootstrap + feature subsampling + voting). |
| B1P04-Q32 | 4 | AI-era: an LLM generated this XGBoost training pipeline. Review it and find the bugs (leakage, early stopping on test set, encoding, metrics). |
| B1P04-Q33 | 4 | Why do GBDTs still often beat deep learning on tabular data? When would you pick a neural net or a tabular foundation model instead? |
| B1P04-Q34 | 4 | How do you do feature selection with tree models (importance thresholds, RFE, Boruta) and what can go wrong? |
| B1P04-Q35 | 4 | How would you explain a gradient boosting model's decision to a non-technical stakeholder or regulator? |
| B1P04-Q36 | 4 | Stacking / blending vs a single Random Forest or GBM: when is an ensemble of ensembles worth it? |
| B1P04-Q37 | 4 | How do you use learning curves and validation curves to diagnose under/overfitting in a boosted model? |
| B1P04-Q38 | 4 | Derive the XGBoost objective: second-order Taylor expansion, optimal leaf weight and the split-gain formula. |
| B1P04-Q39 | 4 | Code: implement gradient boosting regression from scratch (squared loss) using shallow trees. |
| B1P04-Q40 | 4 | How does CatBoost avoid target leakage (ordered target statistics, ordered boosting)? |
| B1P04-Q41 | 4 | What are the limitations of SHAP with correlated features? Explain path-dependent vs interventional TreeSHAP. |
| B1P04-Q42 | 4 | Derive the variance of an average of correlated trees; why does reducing correlation between trees matter? |
| B1P04-Q43 | 4 | How are multi-class problems handled in XGBoost/LightGBM (softmax objective, one tree per class)? |
| B1P04-Q44 | 4 | What does tree depth mean for feature interactions? How do you detect interactions in a GBM? |
| B1P04-Q45 | 4 | What are DART, row subsampling and column subsampling in boosting and why use them? |
| B1P04-Q46 | 4 | Why can Random Forest / XGBoost results differ between runs, and how do you make training reproducible? |
| B1P04-Q47 | 4 | Explain LightGBM's GOSS, EFB and histogram-based splitting. |
| B1P04-Q48 | 4 | How does XGBoost find splits: exact vs approximate vs hist; what is sparsity-aware split finding? |
| B1P04-Q49 | 4 | What are monotonic constraints in GBMs and when would you use them (e.g. credit scoring, pricing)? |
| B1P04-Q50 | 4 | How do you write a custom objective in XGBoost/LightGBM (gradient and hessian)? Example: focal or asymmetric loss. |
| B1P04-Q51 | 4 | How do you get prediction intervals from GBMs (quantile loss, conformal prediction)? |
| B1P04-Q52 | 4 | How do you serve tree ensembles in production: latency, model size, ONNX/Treelite, GPU, distributed training? |
| B1P04-Q53 | 4 | What is the GBDT + logistic regression approach (leaf-index features) and when is it useful? |
| B1P05-Q1 | 5 | Explain the k-means algorithm. What objective does it minimise and why does it converge? |
| B1P05-Q2 | 5 | How do you choose the number of clusters k? (elbow, silhouette, gap statistic, business constraints) |
| B1P05-Q3 | 5 | What is PCA, how does it work, and when would you use it? |
| B1P05-Q4 | 5 | PCA vs t-SNE vs UMAP: what does each preserve, and when do you use which? |
| B1P05-Q5 | 5 | What are the assumptions and failure modes of k-means? When does it give bad clusters? |
| B1P05-Q6 | 5 | How does DBSCAN work? What do eps and minPts mean and how do you tune them? When is it better than k-means? |
| B1P05-Q7 | 5 | How does Isolation Forest detect anomalies, and why do anomalies get isolated in fewer splits? |
| B1P05-Q8 | 5 | How do you evaluate a clustering when there are no labels? |
| B1P05-Q9 | 5 | Case: segment customers for an e-commerce / food-delivery app. Walk through features, scaling, algorithm, validation, and how the business uses it. |
| B1P05-Q10 | 5 | Why must you scale features before k-means or PCA? How do you handle categorical or mixed-type features? |
| B1P05-Q11 | 5 | How do you decide how many principal components to keep? (explained variance, scree, cross-validation) |
| B1P05-Q12 | 5 | You have no labels and must detect anomalies (fraud, bad orders, sensor faults). How do you choose a method, set a threshold, and evaluate it? |
| B1P05-Q13 | 5 | Explain hierarchical (agglomerative) clustering: linkage types, dendrogram, and how you cut it. |
| B1P05-Q14 | 5 | What is the curse of dimensionality and how does it affect distance-based methods like k-means, DBSCAN and kNN? |
| B1P05-Q15 | 5 | Gaussian Mixture Models and the EM algorithm: how do they work and how do they differ from k-means (soft vs hard assignment)? |
| B1P05-Q16 | 5 | Explain the silhouette score: how it is computed, how to read it, and its limitations. |
| B1P05-Q17 | 5 | How does k-means++ initialisation work, and why does initialisation matter (local minima, n_init)? |
| B1P05-Q18 | 5 | What is Local Outlier Factor (LOF)? How does it differ from Isolation Forest, and when would you pick each? |
| B1P05-Q19 | 5 | How can an autoencoder be used for anomaly detection? How do you set the threshold and what can go wrong? |
| B1P05-Q20 | 5 | What is the relationship between PCA and k-means? |
| B1P05-Q21 | 5 | How can PCA be used for anomaly detection (reconstruction error, Mahalanobis distance in PC space)? |
| B1P05-Q22 | 5 | How does t-SNE work, what does perplexity do, and what are the traps when reading a t-SNE plot? |
| B1P05-Q23 | 5 | How does UMAP differ from t-SNE (speed, global structure, reproducibility)? Can you cluster on UMAP output? |
| B1P05-Q24 | 5 | Statistical outlier detection (z-score, IQR, MAD): when does each work and when does it fail? |
| B1P05-Q25 | 5 | How do outliers affect k-means and PCA, and how do you make them robust (k-medoids, robust scaling, trimming)? |
| B1P05-Q26 | 5 | PCA vs feature selection: does PCA help a supervised model, and what do you lose in interpretability? |
| B1P05-Q27 | 5 | How do you cluster high-dimensional data such as text or user embeddings? (reduce then cluster, cosine distance, HDBSCAN, BERTopic) |
| B1P05-Q28 | 5 | How do you evaluate an anomaly detector with very few labels? (precision@k, PR-AUC, contamination parameter, analyst feedback) |
| B1P05-Q29 | 5 | HDBSCAN vs DBSCAN: how does it handle varying density, and what are its main hyperparameters? |
| B1P05-Q30 | 5 | How do you check that clusters are stable and reproducible, and how do you deploy a segmentation and monitor it for drift? |
| B1P05-Q31 | 5 | External clustering metrics when ground truth exists: ARI, NMI, purity, V-measure. When are they appropriate? |
| B1P05-Q32 | 5 | Anomaly detection on business metrics (daily orders, payment success rate): how do you handle seasonality and trend, and avoid alert fatigue? |
| B1P05-Q33 | 5 | SVD vs PCA: how are they related, and when do you use Truncated SVD (sparse matrices, LSA)? |
| B1P05-Q34 | 5 | Derive PCA: show that principal components are eigenvectors of the covariance matrix, and relate it to SVD. |
| B1P05-Q35 | 5 | Implement PCA from scratch in NumPy and verify it against sklearn. |
| B1P05-Q36 | 5 | One-Class SVM vs Isolation Forest vs LOF: how do they compare in assumptions, scale and tuning? |
| B1P05-Q37 | 5 | LLM code review: this LLM-generated clustering/PCA pipeline looks fine but has bugs. Spot them (scaler or PCA fit on all data, leakage, t-SNE used for clustering, wrong k, no random_state). |
| B1P05-Q38 | 5 | GenAI follow-up: how would you use an LLM to name or interpret clusters, and how do you validate that the labels are correct? |
| B1P05-Q39 | 5 | Show that Lloyd's k-means iterations never increase the objective. Why is it only a local optimum, and what is its link to EM? |
| B1P05-Q40 | 5 | Spectral clustering: how does it work and when does it beat k-means? |
| B1P05-Q41 | 5 | Kernel PCA, probabilistic PCA, ICA and NMF: how do they differ from PCA and when would you use them? |
| B1P05-Q42 | 5 | Model selection for GMM: BIC/AIC, covariance types, and degenerate (singular) components. |
| B1P05-Q43 | 5 | How would you explain why a particular point was flagged as an anomaly (SHAP on Isolation Forest, feature-wise reconstruction error)? |
| B1P05-Q44 | 5 | Deep anomaly detection: VAE, Deep SVDD, GAN-based methods. When are they worth it over Isolation Forest? |
| B1P05-Q45 | 5 | Scale: how do you cluster 100M users (mini-batch k-means, FAISS, approximate nearest neighbours, sampling then assign)? Why does DBSCAN scale badly? |
| B1P05-Q46 | 5 | Anomaly detection under drift and feedback loops: how do you handle changing normal behaviour, adversaries adapting (fraud), and labels coming only from flagged cases? |
| B1P06-Q1 | 6 | What is stationarity, why does it matter for time series models, and how do you test and fix non-stationarity (ADF, KPSS)? |
| B1P06-Q2 | 6 | What are the components of a time series (trend, seasonality, cyclic, noise) and how do additive vs multiplicative decomposition differ? |
| B1P06-Q3 | 6 | Why is a random train/test split wrong for time series, and how should you split the data? |
| B1P06-Q4 | 6 | How would you explain time series forecasting to a non-technical stakeholder? |
| B1P06-Q5 | 6 | Which baselines would you build first (naive, seasonal naive, moving average) and why do they matter? |
| B1P06-Q6 | 6 | What is differencing, how do you choose d, and what goes wrong with over-differencing? |
| B1P06-Q7 | 6 | How do you read ACF and PACF plots to choose p and q for an ARIMA model? |
| B1P06-Q8 | 6 | Explain ARIMA(p,d,q). How do you select orders (AIC/BIC, auto_arima) and what are its assumptions and limits? |
| B1P06-Q9 | 6 | What is walk-forward validation / backtesting? Compare expanding vs rolling window and explain how you pick horizon and folds. |
| B1P06-Q10 | 6 | How do you build lag and rolling-window features for a GBM (XGBoost/LightGBM) forecaster without leaking future information? |
| B1P06-Q11 | 6 | Which forecast metric would you choose (MAE, RMSE, MAPE, sMAPE, MASE, WAPE) and why? Why is MAPE huge for low-volume items? |
| B1P06-Q12 | 6 | ARIMA vs Prophet vs GBM with lag features vs deep learning: how do you choose the model for a given problem? |
| B1P06-Q13 | 6 | How do you model holidays, promotions and other external regressors (exogenous variables) in a forecast? |
| B1P06-Q14 | 6 | How do you handle missing timestamps, missing values and outliers in a time series before modelling? |
| B1P06-Q15 | 6 | How do you forecast multiple steps ahead (recursive, direct, multi-output)? What are the trade-offs? |
| B1P06-Q16 | 6 | Design an end-to-end demand/sales forecasting solution: data, features, model, validation, deployment, monitoring. |
| B1P06-Q17 | 6 | What is the difference between white noise and a random walk, and why does it matter for forecasting? |
| B1P06-Q18 | 6 | Explain AR, MA and ARMA models. What does each term capture intuitively? |
| B1P06-Q19 | 6 | How do you do cross-validation with sklearn TimeSeriesSplit? What does the gap parameter do and when would you add it? |
| B1P06-Q20 | 6 | How does SARIMA handle seasonality, and how do you pick seasonal orders (P,D,Q,m)? What about multiple seasonalities? |
| B1P06-Q21 | 6 | Explain exponential smoothing (SES, Holt, Holt-Winters/ETS). When is it better than ARIMA? |
| B1P06-Q22 | 6 | How does Prophet work (trend, seasonality, holidays, changepoints), and what are its strengths and weaknesses? |
| B1P06-Q23 | 6 | How do you encode calendar features for ML forecasters (day-of-week, month, Fourier terms, cyclical sin/cos) and which works best? |
| B1P06-Q24 | 6 | When do you use a log or Box-Cox transform in forecasting, and how do you back-transform correctly? |
| B1P06-Q25 | 6 | How do you diagnose a fitted forecasting model using residuals (Ljung-Box, residual ACF, normality)? |
| B1P06-Q26 | 6 | How do you produce prediction intervals / uncertainty ranges (analytic, bootstrap, quantile regression), and what do you do when intervals miss too many actuals? |
| B1P06-Q27 | 6 | Global vs local models: how do you forecast thousands of related series, and when do you pick one global GBM/DL model over per-series models? |
| B1P06-Q28 | 6 | Why does a demand forecast under-forecast after stockouts, and how do you handle censored (sales != demand) data? |
| B1P06-Q29 | 6 | How do you forecast a new product or new store with no history (cold start)? |
| B1P06-Q30 | 6 | How do you forecast intermittent / lumpy demand? Explain Croston, SBA, TSB and which metrics to use. |
| B1P06-Q31 | 6 | When would you use LSTM/GRU/1D-CNN for forecasting instead of GBM, and why do deep models often fail to beat strong baselines? |
| B1P06-Q32 | 6 | How do you monitor a deployed forecast model and decide retraining frequency? |
| B1P06-Q33 | 6 | One-step-ahead forecasts look good but 12-step-ahead forecasts fail. What are the likely causes? |
| B1P06-Q34 | 6 | A useful feature (e.g. weather, ad spend) is not known at forecast time. How do you handle it without leakage? |
| B1P06-Q35 | 6 | How do you handle structural breaks, regime shifts (COVID, pricing change) and concept drift in forecasting? |
| B1P06-Q36 | 6 | A deep model beats the baseline in training but not in backtesting. What do you do? |
| B1P06-Q37 | 6 | How do you pick a forecast loss when over- and under-forecasting have different costs (bias, tracking signal, quantile/newsvendor)? |
| B1P06-Q38 | 6 | How does late-arriving or revised recent data affect forecasting, and how do you evaluate with data vintages? |
| B1P06-Q39 | 6 | A promotion changes the demand pattern. How do you separate baseline demand from promo uplift and forecast it? |
| B1P06-Q40 | 6 | Why does autocorrelation in residuals break OLS regression assumptions, and what is spurious regression? |
| B1P06-Q41 | 6 | What is forecast combination/ensembling and why does averaging models often beat the best single model? |
| B1P06-Q42 | 6 | What is hierarchical forecasting? Explain bottom-up, top-down and MinT reconciliation, and what to do when store forecasts do not sum to the region forecast. |
| B1P06-Q43 | 6 | How do you tune hyperparameters of a forecasting model (e.g. LightGBM, Prophet) with time-aware CV without overfitting to the backtest? |
| B1P06-Q44 | 6 | Implement from scratch in NumPy: moving average, simple exponential smoothing, ACF, and seasonal-naive forecast. |
| B1P06-Q45 | 6 | AI-era: review this LLM-generated forecasting code. Spot leakage (shuffled split, scaler fit on all data, future-rolling features) and other bugs. |
| B1P06-Q46 | 6 | Which probabilistic forecast metrics do you use (pinball loss, CRPS, coverage, interval width) and how do you evaluate quantile forecasts? |
| B1P06-Q47 | 6 | What is conformal prediction for time series, and why do standard conformal guarantees break under autocorrelation? |
| B1P06-Q48 | 6 | Compare modern deep forecasters: DeepAR, N-BEATS, Temporal Fusion Transformer, PatchTST. When are they worth it? |
| B1P06-Q49 | 6 | AI-era: What are time-series foundation models (Chronos, TimesFM, Moirai)? When do you use zero-shot vs fine-tune vs a tuned LightGBM? |
| B1P06-Q50 | 6 | AI-era: Can you prompt an LLM to forecast numbers? What works, what fails, and how would you evaluate it? |
| B1P06-Q51 | 6 | Explain VAR, Granger causality and cointegration. When is each appropriate? |
| B1P06-Q52 | 6 | What is a state-space model / Kalman filter and how does it relate to exponential smoothing and ARIMA? |
| B1P06-Q53 | 6 | What is GARCH / volatility modelling and when do you model variance instead of the mean? |
| B1P06-Q54 | 6 | How would you use Bayesian structural time series / counterfactual forecasting to estimate the impact of an intervention (CausalImpact)? |
| B1P07-Q1 | 7 | Explain collaborative filtering. User-based vs item-based: how do they differ, and which scales better and why? |
| B1P07-Q2 | 7 | Explicit vs implicit feedback: what is the difference, and how does your modelling and loss function change for implicit data (clicks, views, purchases)? |
| B1P07-Q3 | 7 | What is the cold-start problem? How do you handle a new user, a new item, and a brand-new platform? |
| B1P07-Q4 | 7 | Why do large recommenders use a two-stage pipeline (candidate generation then ranking)? What does each stage optimise, and what metric does each care about? |
| B1P07-Q5 | 7 | Define precision@k, recall@k, MRR, MAP and NDCG. When would you pick each one? |
| B1P07-Q6 | 7 | Compute NDCG@k by hand for a small ranked list, then write it in NumPy. Why the log discount, and how do you handle ideal-DCG = 0 and ties? |
| B1P07-Q7 | 7 | Explain matrix factorization for recommendations. How is it trained (SGD vs ALS), why not treat missing entries as zeros, and what does the embedding size control? |
| B1P07-Q8 | 7 | Content-based vs collaborative vs hybrid recommenders: strengths, weaknesses, and when would you choose each? |
| B1P07-Q9 | 7 | Explain the two-tower model: architecture, training objective and negatives, and how it is served (precomputed item embeddings + ANN). |
| B1P07-Q10 | 7 | Offline NDCG/AUC improved but the A/B test got worse (or flat). What could explain it and how do you debug? |
| B1P07-Q11 | 7 | What is popularity bias and how do feedback loops form in recommenders? How would you detect and reduce them? |
| B1P07-Q12 | 7 | What is position bias in click data? How does it corrupt a ranker trained on clicks, and how do you correct it (propensity weighting, position feature dropped at serving, randomisation)? |
| B1P07-Q13 | 7 | How do you split data and evaluate a recommender offline? Why is a random split wrong, and where can data leakage creep in (e.g. features using future purchases)? |
| B1P07-Q14 | 7 | How do you sample negatives for implicit-feedback training (random, popularity-based, hard negatives, in-batch)? What are the trade-offs? |
| B1P07-Q15 | 7 | Walk through how you would build a recommender for an e-commerce / food-delivery / music app: data, labels, candidate sources, ranker features, metrics. (Full end-to-end design belongs to Part 11; answer at model level here.) |
| B1P07-Q16 | 7 | Cosine similarity vs dot product vs Euclidean distance for embeddings: when do they give different rankings, and why normalise? |
| B1P07-Q17 | 7 | Why is RMSE a poor metric for top-N recommendation on implicit data? What should you use instead? |
| B1P07-Q18 | 7 | Pointwise vs pairwise vs listwise learning-to-rank: how do the losses differ and when would you use each? |
| B1P07-Q19 | 7 | Explain LambdaRank and LambdaMART. How do you train a ranker in XGBoost/LightGBM (query groups, objective, eval metric)? |
| B1P07-Q20 | 7 | How does approximate nearest neighbour search work? Compare HNSW, IVF-PQ and ScaNN/FAISS indexes on recall, latency, memory and updates. |
| B1P07-Q21 | 7 | Exploration vs exploitation in recommenders: epsilon-greedy, UCB, Thompson sampling. How would you inject exploration for new items? |
| B1P07-Q22 | 7 | How do you add diversity, novelty, serendipity and freshness to a ranked list? Explain MMR/DPP re-ranking and how you would measure it. |
| B1P07-Q23 | 7 | Your system predicts click, add-to-cart, purchase and dwell time. How do you combine multiple objectives into one ranking (scalarisation, multi-task learning, constraints)? |
| B1P07-Q24 | 7 | CTR is up but retention or long-term satisfaction is falling (clickbait ranks high). What is going on and what do you change? |
| B1P07-Q25 | 7 | Compare SVD, truncated SVD, ALS, NMF and SVD++ for recommendations. What do user/item bias terms and regularisation do? |
| B1P07-Q26 | 7 | Search relevance: TF-IDF vs BM25 vs dense retrieval vs hybrid search. When does each fail? |
| B1P07-Q27 | 7 | How do you evaluate a search/ranking system online and offline: relevance labels, click models, interleaving, A/B tests? |
| B1P07-Q28 | 7 | How are item embeddings learned (item2vec/prod2vec, session co-occurrence)? What are the pitfalls (popularity, window size, sparse items)? |
| B1P07-Q29 | 7 | In-batch negatives in two-tower training bias the model towards popular items. How do logQ correction or mixed negative sampling fix it? |
| B1P07-Q30 | 7 | Wide & Deep, DeepFM, DLRM: why do ranking models need explicit feature crosses and how do these architectures provide them? |
| B1P07-Q31 | 7 | Sequential and session-based recommendation: Markov chains, GRU4Rec, SASRec/BERT4Rec. When do they beat matrix factorization? |
| B1P07-Q32 | 7 | Selection bias and counterfactual evaluation: explain inverse propensity scoring for offline evaluation of a new ranker and its variance problem (clipping, doubly robust). |
| B1P07-Q33 | 7 | Does a ranker's predicted probability need to be calibrated? When does it matter (ads, blending scores, thresholds) and how do you fix it? |
| B1P07-Q34 | 7 | How do you meet a latency budget (e.g. 100 ms) in a recsys: cascaded ranking, caching, precomputation, feature-freshness tiers? What do you inspect when latency spikes? |
| B1P07-Q35 | 7 | Implement item-based collaborative filtering (cosine similarity on a sparse user-item matrix) with NumPy/pandas and produce top-N recommendations. |
| B1P07-Q36 | 7 | Implement matrix factorization with SGD from scratch in NumPy (bias terms, L2, train/val RMSE). How would you adapt it to implicit feedback? |
| B1P07-Q37 | 7 | Bi-encoder vs cross-encoder: how do they differ for retrieval vs reranking, and why is a cross-encoder only used on a shortlist? |
| B1P07-Q38 | 7 | How can LLMs or pretrained text/image embeddings help cold start and item representation? What is generative retrieval with semantic IDs? |
| B1P07-Q39 | 7 | Can you use an LLM as a judge to label search/recommendation relevance? What biases and validation steps do you need? |
| B1P07-Q40 | 7 | How do you measure and improve fairness and exposure for small creators or sellers? How do you stop sellers spamming metadata to game the ranker? |
| B1P07-Q41 | 7 | A recommendation reveals a sensitive inference about a user. What privacy, explainability and guardrail changes would you make? |
| B1P07-Q42 | 7 | How do you measure the causal impact of recommendations on engagement (not just correlation)? Discuss holdouts, uplift and incrementality. |
| B1P07-Q43 | 7 | Design LLM-based reranking for top-k candidates: pointwise vs listwise prompting, cost and latency, distillation into a small ranker, and failure modes (position bias, reward hacking by preserving order). |
| B1P07-Q44 | 7 | Unbiased learning-to-rank from click logs: how do you estimate position propensities, and how does Unbiased LambdaMART use them? |
| B1P07-Q45 | 7 | Contextual bandits for recommendation (LinUCB, Thompson sampling) and off-policy evaluation. When would you use a bandit instead of a supervised ranker? |
| B1P07-Q46 | 7 | Why is NDCG not directly optimisable by gradient descent, and how do lambda gradients get around that? |
| B1P07-Q47 | 7 | Graph-based recommenders: random walks, PinSage, LightGCN. When are they worth the complexity? |
| B1P07-Q48 | 7 | Recommending in a two-sided marketplace (customer / restaurant / delivery partner, or job seeker / recruiter): how do you balance stakeholders and capacity constraints? |
| B1P07-Q49 | 7 | Embedding and index operations: how do you refresh embeddings, version two-tower models, avoid mismatches between towers and the ANN index, and roll back? |
| B1P08-Q1 | 8 | Explain backpropagation in simple terms. How does the chain rule give gradients for each layer? |
| B1P08-Q2 | 8 | Why do neural networks need non-linear activation functions? Compare sigmoid, tanh and ReLU. |
| B1P08-Q3 | 8 | What is overfitting in a neural network and which regularization techniques do you know (L2, dropout, early stopping, augmentation)? |
| B1P08-Q4 | 8 | How does dropout work, and what changes between training and inference (inverted dropout scaling)? |
| B1P08-Q5 | 8 | Batch, mini-batch and stochastic gradient descent: differences, and what does momentum add? |
| B1P08-Q6 | 8 | In PyTorch, why do you call optimizer.zero_grad()? What do model.train(), model.eval() and torch.no_grad() each do? |
| B1P08-Q7 | 8 | What are vanishing and exploding gradients? Why do they happen and how do you fix them? |
| B1P08-Q8 | 8 | Compare MSE, binary cross-entropy and categorical cross-entropy. Why is cross-entropy preferred for classification? |
| B1P08-Q9 | 8 | Compare batch norm and layer norm: how each is computed, when each works, trade-offs. |
| B1P08-Q10 | 8 | Explain how Adam works. Why is it the default and when would you prefer SGD with momentum? |
| B1P08-Q11 | 8 | Write a clean PyTorch training loop from scratch (zero_grad, forward, loss, backward, step) with validation. |
| B1P08-Q12 | 8 | How do you initialize weights? Explain Xavier/Glorot vs He initialization and why zero init fails. |
| B1P08-Q13 | 8 | Your training loss is not decreasing. How do you debug it, step by step? |
| B1P08-Q14 | 8 | How does learning rate affect training? Explain schedulers (step, cosine, warmup) and how you would choose one. |
| B1P08-Q15 | 8 | What is the difference between Adam and AdamW? Why is decoupled weight decay better than L2 inside Adam? |
| B1P08-Q16 | 8 | How do you read training vs validation loss curves to diagnose overfitting, underfitting or a bug? |
| B1P08-Q17 | 8 | Why should you never initialize all weights to the same value (symmetry breaking)? |
| B1P08-Q18 | 8 | How do you save and load PyTorch models (state_dict vs full model) and resume training? |
| B1P08-Q19 | 8 | What is the softmax function and why is it computed with the log-sum-exp trick? Why feed logits to CrossEntropyLoss? |
| B1P08-Q20 | 8 | Write a custom PyTorch Dataset and DataLoader for tabular or text data. What do num_workers, collate_fn and shuffle do? |
| B1P08-Q21 | 8 | Write a custom nn.Module. What do __init__ vs forward do, and how are parameters registered? |
| B1P08-Q22 | 8 | Explain CNNs: convolution, stride, padding, pooling, parameter sharing. Why do they suit images? |
| B1P08-Q23 | 8 | Given an input shape and layer config, compute the output shape and parameter count of a conv layer. |
| B1P08-Q24 | 8 | How do RNNs work and what is backpropagation through time? Why do they struggle with long sequences? |
| B1P08-Q25 | 8 | Explain LSTM gates and how they mitigate vanishing gradients. How does GRU differ? |
| B1P08-Q26 | 8 | What are residual (skip) connections and why do they let you train much deeper networks? |
| B1P08-Q27 | 8 | What is gradient clipping, when do you need it, and norm vs value clipping? |
| B1P08-Q28 | 8 | How does batch size affect convergence and generalization? What is the linear learning-rate scaling rule? |
| B1P08-Q29 | 8 | How would you handle class imbalance in a neural network (weighted loss, focal loss, sampling)? |
| B1P08-Q30 | 8 | What is early stopping and how do you implement it with checkpointing in PyTorch? |
| B1P08-Q31 | 8 | Explain L2 regularization vs weight decay, and when they are equivalent. |
| B1P08-Q32 | 8 | Sigmoid vs softmax output heads: binary, multi-class and multi-label setups and matching losses. |
| B1P08-Q33 | 8 | What is the dead ReLU problem? Compare Leaky ReLU, ELU, GELU and Swish. |
| B1P08-Q34 | 8 | Your loss becomes NaN or spikes mid-training. What are the likely causes and fixes? |
| B1P08-Q35 | 8 | When would you use a neural net versus gradient-boosted trees for tabular data? |
| B1P08-Q36 | 8 | How do embedding layers work for high-cardinality categorical features in tabular deep learning? |
| B1P08-Q37 | 8 | How do you tune hyperparameters for a neural net (random vs grid vs Bayesian), and which matter most? |
| B1P08-Q38 | 8 | How do you make PyTorch experiments reproducible (seeds, determinism, DataLoader workers)? |
| B1P08-Q39 | 8 | Explain transfer learning and fine-tuning: which layers do you freeze and what learning rates do you use? |
| B1P08-Q40 | 8 | Explain mixed precision training and common reasons for GPU out-of-memory errors; how do you reduce memory? |
| B1P08-Q41 | 8 | Here is LLM-generated PyTorch training code. Find the bugs (missing zero_grad, eval mode, softmax before CE, data leakage, wrong device). |
| B1P08-Q42 | 8 | What does universal approximation say, and why do we still use deep rather than wide networks? |
| B1P08-Q43 | 8 | Implement a 2-layer MLP with forward and backward pass in NumPy (no frameworks). |
| B1P08-Q44 | 8 | How does PyTorch autograd work? Explain the computational graph, requires_grad, detach and retain_graph. |
| B1P08-Q45 | 8 | What is the difference between DataParallel and DistributedDataParallel, and when do you need multi-GPU training? |
| B1P08-Q46 | 8 | Derive the gradient of softmax followed by cross-entropy with respect to the logits. |
| B1P08-Q47 | 8 | What are one-cycle and cosine annealing schedules and how do you find a good learning rate (LR range test)? |
| B1P08-Q48 | 8 | A GenAI assistant suggests a huge architecture for a 5k-row tabular problem. How do you decide model size and sanity-check the suggestion? |
| B1P08-Q49 | 8 | Why might Adam generalize worse than SGD with momentum? Discuss sharp vs flat minima. |
| B1P08-Q50 | 8 | Explain bias correction in Adam and why the first steps would be off without it. |
| B1P08-Q51 | 8 | Implement a tiny autograd engine (micrograd-style) with add, multiply, tanh and a backward pass. |
| B1P08-Q52 | 8 | Why does batch norm behave differently at inference (running statistics)? What breaks at small batch sizes and what are GroupNorm/RMSNorm alternatives? |
| B1P08-Q53 | 8 | How does gradient checkpointing trade compute for memory, and how do you estimate training memory for a model? |
| B1P08-Q54 | 8 | What is double descent and how does overparameterization square with classical bias-variance thinking? |
| B1P08-Q55 | 8 | What are knowledge distillation, pruning and quantization, and when would you use each for serving? |
| B1P08-Q56 | 8 | How do you handle variable-length sequences in PyTorch (padding, masking, pack_padded_sequence)? |
| B1P08-Q57 | 8 | How does LSTM cell-state gradient flow work mathematically, and what is the role of the forget-gate bias initialization? |
| B1P08-Q58 | 8 | Explain autoencoders and VAEs at a basic level: what is the loss and what is the reparameterization trick? |
| B1P09-Q1 | 9 | How does TF-IDF work, and what are its limitations compared with embeddings? |
| B1P09-Q2 | 9 | Bag-of-Words vs TF-IDF vs word embeddings: when would you use each? |
| B1P09-Q3 | 9 | Word2Vec vs GloVe vs FastText: how do they differ, and how are they trained? |
| B1P09-Q4 | 9 | What is IoU, and how is it used in object detection? |
| B1P09-Q5 | 9 | How do you handle overfitting when training a CNN on a small image dataset (augmentation, regularization, early stopping)? |
| B1P09-Q6 | 9 | How do you build a text classifier end to end (TF-IDF + logistic regression baseline up to a fine-tuned transformer)? How do you choose between them? |
| B1P09-Q7 | 9 | What is the difference between static (Word2Vec) and contextual (BERT) embeddings? |
| B1P09-Q8 | 9 | Explain self-attention and the transformer architecture. Why did transformers replace RNNs/LSTMs? |
| B1P09-Q9 | 9 | What is BERT, how is it pretrained (MLM, NSP), and how do you fine-tune it for classification? |
| B1P09-Q10 | 9 | Explain transfer learning in CNNs. When do you freeze layers versus fine-tune the whole network? |
| B1P09-Q11 | 9 | Explain how a CNN works: convolution, stride, padding, pooling, receptive field, parameter sharing. |
| B1P09-Q12 | 9 | What is mAP in object detection, and how is it computed (precision-recall curve, AP per class, IoU thresholds)? |
| B1P09-Q13 | 9 | When would you pick an LLM (prompting) over a classic NLP model (TF-IDF/BERT classifier) for a text task? Discuss cost, latency, accuracy, data and maintenance. |
| B1P09-Q14 | 9 | Prompting vs RAG vs fine-tuning: how do you decide? (framing only; depth is in Book 2) |
| B1P09-Q15 | 9 | Text preprocessing pipeline: tokenization, stop words, stemming vs lemmatization. When should you skip them? |
| B1P09-Q16 | 9 | Which evaluation metrics do you use for text classification (precision/recall/F1, macro vs micro), and why? |
| B1P09-Q17 | 9 | What are the common image augmentation techniques, and when can augmentation hurt? |
| B1P09-Q18 | 9 | What is perplexity, and what does it tell you about a language model? |
| B1P09-Q19 | 9 | How do you get a sentence or document embedding, and how would you use embeddings for semantic search (cosine similarity, ANN index)? |
| B1P09-Q20 | 9 | What is NER? How would you build and evaluate a NER system (BiLSTM-CRF vs BERT; entity-level F1)? |
| B1P09-Q21 | 9 | Why does the transformer use positional encoding, and how does multi-head attention help? |
| B1P09-Q22 | 9 | Compare CNN architectures: LeNet, AlexNet, VGG, ResNet, Inception, EfficientNet. Why do skip connections help? |
| B1P09-Q23 | 9 | BLEU vs ROUGE vs BERTScore: what do they measure and what are their weaknesses? |
| B1P09-Q24 | 9 | How do you handle class imbalance in text or image classification? |
| B1P09-Q25 | 9 | Object detection vs semantic vs instance segmentation: differences, and typical models (YOLO, Faster R-CNN, U-Net, Mask R-CNN). |
| B1P09-Q26 | 9 | Explain batch normalization and dropout in CNNs. Where do you place them and why? |
| B1P09-Q27 | 9 | How do you handle out-of-vocabulary words and misspellings? Explain subword tokenization (BPE/WordPiece). |
| B1P09-Q28 | 9 | How do you deal with long documents when BERT has a 512-token limit? |
| B1P09-Q29 | 9 | How would you build a text classifier with very few labelled examples (zero-shot, few-shot, SetFit, weak labelling, active learning)? |
| B1P09-Q30 | 9 | How do you evaluate an LLM-based classifier or extractor in a classical DS workflow, and what can go wrong (non-determinism, leakage, prompt sensitivity)? |
| B1P09-Q31 | 9 | How would you detect and handle drift in a production NLP model (e.g. new slang, new product names)? |
| B1P09-Q32 | 9 | What is Non-Max Suppression, and how do anchor boxes work? Anchor-based vs anchor-free detectors. |
| B1P09-Q33 | 9 | What is the Vision Transformer (ViT)? How does it differ from a CNN, and when does each win? |
| B1P09-Q34 | 9 | Walk through a design for an image classification system with limited labelled data and a latency budget on edge devices. |
| B1P09-Q35 | 9 | Why does a vision model trained in one domain fail in another? How do you diagnose and fix the domain shift? |
| B1P09-Q36 | 9 | What is the vanishing gradient problem in RNNs, and how do LSTM/GRU gates address it? |
| B1P09-Q37 | 9 | Topic modelling: explain LDA and when you would use it over clustering embeddings (e.g. BERTopic). |
| B1P09-Q38 | 9 | Cosine similarity vs Euclidean vs dot product for embeddings: when does each apply? |
| B1P09-Q39 | 9 | Fine-tuning basics: full fine-tuning vs adapters/LoRA vs feature extraction. What goes wrong with catastrophic forgetting or a bad learning rate? |
| B1P09-Q40 | 9 | How do you reduce hallucination and measure factuality when an LLM is part of a DS pipeline? |
| B1P09-Q41 | 9 | What is Grad-CAM, and how do you explain a CNN or transformer prediction? |
| B1P09-Q42 | 9 | Dice coefficient vs IoU vs pixel accuracy for segmentation: when is each used? |
| B1P09-Q43 | 9 | How do you deal with noisy or ambiguous labels in image or text datasets (inter-annotator agreement, label cleaning)? |
| B1P09-Q44 | 9 | Sequence-to-sequence basics: what are the encoder-decoder, teacher forcing and beam search? |
| B1P09-Q45 | 9 | Explain contrastive learning / sentence-transformers and how a bi-encoder differs from a cross-encoder (reranking). |
| B1P09-Q46 | 9 | Multilingual and code-mixed text (Hinglish): how would you approach classification or search? |
| B1P09-Q47 | 9 | How do you choose between a distilled small model and a large model for production text inference (quantization, ONNX, latency, cost)? |
| B1P09-Q48 | 9 | How do you check for bias and PII/privacy issues when training on text or image data? |
| B1P09-Q49 | 9 | Explain the O(n^2) attention cost problem and approaches to mitigate it (sparse, linear, Flash attention) at a high level. |
| B1P09-Q50 | 9 | What is self-supervised pretraining for vision (SimCLR, MAE, CLIP)? How would you use CLIP for zero-shot image search? |
| B1P09-Q51 | 9 | Design an embedding-based product search system (text + image) for an e-commerce catalogue: indexing, retrieval, evaluation, cold start. |
| B1P09-Q52 | 9 | Explain OCR / document-understanding pipelines (e.g. invoices, KYC) and how you would evaluate them. |
| B1P10-Q1 | 10 | Walk me through how you would design an A/B test end to end (hypothesis, metrics, unit, sample size, duration, decision rule). |
| B1P10-Q2 | 10 | What is an A/B test and when should you NOT run one? |
| B1P10-Q3 | 10 | How do you choose the primary metric, guardrail metrics and secondary metrics for an experiment? Give an example. |
| B1P10-Q4 | 10 | What is the randomization unit? How do you choose between user-, session-, device-, request- and cluster-level randomization? |
| B1P10-Q5 | 10 | How do you decide how long to run an experiment and how many users you need? (interview-level: which inputs drive sample size; derivations are in Part 13) |
| B1P10-Q6 | 10 | What is a Sample Ratio Mismatch (SRM)? How do you detect it and what are the common causes? |
| B1P10-Q7 | 10 | The A/B test shows a significant lift but the PM wants to stop the test after 3 days. What is wrong with peeking and what do you do? |
| B1P10-Q8 | 10 | What is the novelty effect and the primacy effect? How do you detect them and what do you do about them? |
| B1P10-Q9 | 10 | You track 20 metrics (or 10 variants) in one test and one is significant at p=0.04. What is the multiple-testing problem and how do you handle it (Bonferroni, BH/FDR)? |
| B1P10-Q10 | 10 | What is Simpson's paradox? Give an A/B-test example where the variant wins overall but loses in every segment. |
| B1P10-Q11 | 10 | Explain correlation vs causation. How would you establish causality for the claim 'users who use feature X retain better'? |
| B1P10-Q12 | 10 | Explain network effects / interference (SUTVA violation). How do you run experiments on a social product or a two-sided marketplace? |
| B1P10-Q13 | 10 | The test shows the primary metric up but revenue (or a guardrail) down or flat. How do you interpret and decide? |
| B1P10-Q14 | 10 | What do you do when the A/B test result is statistically insignificant? Can you conclude there is no effect? |
| B1P10-Q15 | 10 | Statistical vs practical significance: how do you read the confidence interval of the lift and make a ship / no-ship call? |
| B1P10-Q16 | 10 | A metric (conversion, orders) dropped after a launch. How would you investigate whether it is real, caused by the launch, or a data issue? |
| B1P10-Q17 | 10 | AI-era: How would you A/B test an LLM-powered feature (chatbot, summarisation, copilot)? Which metrics (task success, edit/retry rate, latency, token cost, LLM-judge score) and which randomization unit? |
| B1P10-Q18 | 10 | Observational vs experimental data: what are confounders and how do you control for them? When would you trust an observational estimate? |
| B1P10-Q19 | 10 | You cannot randomize (e.g., a pricing change, a regional launch). What are your options for estimating the causal effect? |
| B1P10-Q20 | 10 | Which statistical test do you use for conversion-rate metrics vs continuous metrics like revenue per user? Explain the two-proportion z-test setup. |
| B1P10-Q21 | 10 | What is A/A testing and why would you run one? |
| B1P10-Q22 | 10 | Compare how you would test a feature with 5 variants (A/B/n): what changes in analysis, sample size and decision? |
| B1P10-Q23 | 10 | A product manager says 'the cohort that used the feature has 30% higher retention, so ship it to everyone.' Respond. |
| B1P10-Q24 | 10 | What is a holdout / long-term holdout group and why would a company keep one? |
| B1P10-Q25 | 10 | How do you handle outliers and heavy-tailed metrics (revenue, watch time) in an A/B test? |
| B1P10-Q26 | 10 | How do you measure the effect when only some assigned users actually received the treatment? (intent-to-treat vs per-protocol, non-compliance, triggered analysis) |
| B1P10-Q27 | 10 | Ratio metrics (CTR, revenue per session) and per-session vs per-user analysis: what goes wrong with the variance and how do you fix it (delta method)? |
| B1P10-Q28 | 10 | Explain difference-in-differences. What is the parallel-trends assumption and how do you test it? |
| B1P10-Q29 | 10 | What is a switchback (time-based) experiment? When is it used and what are its pitfalls (carryover, time-of-day effects)? |
| B1P10-Q30 | 10 | Explain propensity score matching / weighting. When would you use it and how do you check it worked (balance, overlap)? |
| B1P10-Q31 | 10 | What is Instrumental Variables (IV)? Explain the relevance and exclusion assumptions with an example. |
| B1P10-Q32 | 10 | Explain Regression Discontinuity Design with an example. What are its assumptions and limits? |
| B1P10-Q33 | 10 | What is uplift modelling? How is it different from a normal propensity/response model? |
| B1P10-Q34 | 10 | How do you evaluate an uplift model offline (Qini curve, AUUC) and online? |
| B1P10-Q35 | 10 | Explain Average Treatment Effect (ATE), CATE and the potential-outcomes framework. What is the fundamental problem of causal inference? |
| B1P10-Q36 | 10 | What assumptions are needed to estimate causal effects from observational data (SUTVA, unconfoundedness, positivity)? |
| B1P10-Q37 | 10 | How would you design an experiment for a marketplace where both buyers/riders and sellers/drivers are affected (a new pricing or dispatch algorithm)? |
| B1P10-Q38 | 10 | How would you test a new recommendation or ranking algorithm online? Which metrics and what pitfalls (position bias, interleaving)? |
| B1P10-Q39 | 10 | How would you A/B test a price change or discount? What are the risks (cannibalization, fairness, price anchoring)? |
| B1P10-Q40 | 10 | How do you run experiments for a feature with a long-term outcome (retention, LTV) when you cannot wait months? (surrogate metrics, holdouts) |
| B1P10-Q41 | 10 | What is a multi-armed bandit? When would you prefer it to a classic A/B test and what do you lose? |
| B1P10-Q42 | 10 | Explain selection bias and survivorship bias with experiment or observational examples. |
| B1P10-Q43 | 10 | A marketing campaign has already run. How do you estimate its incrementality? |
| B1P10-Q44 | 10 | How would you design and read a geo / city-level experiment when user-level randomization is not possible? (synthetic control, matched markets) |
| B1P10-Q45 | 10 | AI-era: Offline LLM evals look better but the online A/B shows no gain or a drop. How do you reconcile and decide? |
| B1P10-Q46 | 10 | AI-era: How would you measure the causal impact of AI-assistant adoption on productivity when users self-select into using it? |
| B1P10-Q47 | 10 | Explain heterogeneous treatment effects: how do you find which segments benefit, and what are the dangers of post-hoc subgroup analysis? |
| B1P10-Q48 | 10 | What are interaction effects between concurrent experiments and how do mature platforms avoid them (layers, orthogonal hashing)? |
| B1P10-Q49 | 10 | Explain synthetic control. How is it different from difference-in-differences? |
| B1P10-Q50 | 10 | How does an interleaving experiment work and why is it more sensitive than A/B for ranking? |
| B1P10-Q51 | 10 | How do you handle interference with cluster-randomised or graph-cluster experiments? What is the bias-variance tradeoff of cluster size? |
| B1P10-Q52 | 10 | Explain double machine learning, causal forests and meta-learners (S-, T-, X-learner) at a high level. When would you use them? |
| B1P10-Q53 | 10 | How would you debug an experiment platform whose results look wrong (SRM, logging loss, bucketing collisions, carryover between experiments)? |
| B1P10-Q54 | 10 | How do you quantify the cumulative impact of many launched experiments (the sum of wins exceeds the real lift)? What is the winner's curse? |
| B1P10-Q55 | 10 | AI-era: How do you handle a test where the treatment is non-deterministic or changes mid-test (LLM feature, silent provider model updates)? |
| B1P10-Q56 | 10 | AI-era: How do you validate an LLM-as-judge metric before using it as an experiment outcome (bias, agreement with humans, variance)? |
| B1P11-Q1 | 11 | Walk me through your end-to-end framework for any ML system design question (requirements to monitoring). |
| B1P11-Q2 | 11 | A product manager says 'reduce fraud' (or 'reduce churn'). How do you turn that vague ask into a well-defined ML problem with a success metric? |
| B1P11-Q3 | 11 | Batch vs real-time (online) inference: how do you decide for a given use case? |
| B1P11-Q4 | 11 | Design a fraud detection system for UPI / card payments. |
| B1P11-Q5 | 11 | Design a news-feed / social-media feed ranking system. |
| B1P11-Q6 | 11 | Design a recommendation system for an e-commerce home page at scale. |
| B1P11-Q7 | 11 | Design an ETA prediction system for food or grocery delivery. |
| B1P11-Q8 | 11 | Design a customer churn prediction and retention system. |
| B1P11-Q9 | 11 | Design a demand forecasting system for a retailer or quick-commerce platform. |
| B1P11-Q10 | 11 | Design a credit risk / loan default scoring system. |
| B1P11-Q11 | 11 | Design an ad click-through rate (CTR) prediction system. |
| B1P11-Q12 | 11 | Design a search ranking system for an e-commerce site. |
| B1P11-Q13 | 11 | How do you choose offline metrics and online metrics for an ML system, and what do you do when they disagree? |
| B1P11-Q14 | 11 | How do you handle the cold-start problem (new users, new items) in a production system? |
| B1P11-Q15 | 11 | What is training-serving skew and how do you prevent it? |
| B1P11-Q16 | 11 | How would you monitor an ML model in production and decide when to retrain? |
| B1P11-Q17 | 11 | What are feedback loops and selection bias in deployed ML systems, and how do you mitigate them? |
| B1P11-Q18 | 11 | Walk through how you would prevent data leakage when building training data for a time-dependent system. |
| B1P11-Q19 | 11 | When should you not use ML at all? How do you decide between rules, heuristics and a model? |
| B1P11-Q20 | 11 | Do a back-of-envelope estimate of QPS, storage and latency budget for a ranking or fraud system. |
| B1P11-Q21 | 11 | Design a dynamic / surge pricing system. |
| B1P11-Q22 | 11 | Design a notification / push system that decides what to send, to whom and when. |
| B1P11-Q23 | 11 | Design a content moderation or spam / abuse detection system. |
| B1P11-Q24 | 11 | Design an anomaly detection system for business or payment metrics. |
| B1P11-Q25 | 11 | Design a model to predict cash-on-delivery order cancellations or return-to-origin (RTO) in Indian e-commerce. |
| B1P11-Q26 | 11 | Design a product-return prediction system for a fashion marketplace. |
| B1P11-Q27 | 11 | Design a customer lifetime value (LTV) prediction system. |
| B1P11-Q28 | 11 | Design a lead scoring / propensity-to-buy model for sales or lending. |
| B1P11-Q29 | 11 | Design a Spotify-style personalised playlist / 'because you watched' recommender. |
| B1P11-Q30 | 11 | Design a restaurant / dish ranking system for a food-delivery app. |
| B1P11-Q31 | 11 | Design a customer-support ticket routing and prioritisation system. |
| B1P11-Q32 | 11 | How do you design real-time velocity and aggregate features for fraud, and where do they live (feature store)? |
| B1P11-Q33 | 11 | How do you handle concept drift and adversaries adapting in a fraud system? |
| B1P11-Q34 | 11 | How do you roll out a new model safely (shadow, canary, A/B) and decide to ramp up? |
| B1P11-Q35 | 11 | How do you reduce inference cost and latency (cascade models, distillation, caching, quantisation) without losing quality? |
| B1P11-Q36 | 11 | How do you incorporate exploration vs exploitation (bandits) into a recommender or notification system? |
| B1P11-Q37 | 11 | How do you design a human-in-the-loop review queue for fraud or moderation and use analyst feedback as labels? |
| B1P11-Q38 | 11 | How do you ensure explainability and regulatory compliance (RBI, GDPR, EU AI Act) in a credit or fraud model? |
| B1P11-Q39 | 11 | AI-era: when would you use an LLM inside a classic ML system (classification, feature extraction, explanations) versus a trained classifier or embedding model? |
| B1P11-Q40 | 11 | AI-era: how do embeddings, two-tower models and vector search change retrieval in search and recommendation systems? |
| B1P11-Q41 | 11 | Design a delivery-partner / driver assignment (matching) system. |
| B1P11-Q42 | 11 | Design a hierarchical demand-forecasting system for 100k+ SKU-store combinations with promotions and stock-outs. |
| B1P11-Q43 | 11 | Design a 'people you may know' / friend recommendation system. |
| B1P11-Q44 | 11 | Design a search autocomplete / query suggestion system. |
| B1P11-Q45 | 11 | How would you decide between one global model and per-country / per-segment models across markets? |
| B1P11-Q46 | 11 | How do you design for privacy and data minimisation (DPDP Act, GDPR) in a personalisation system? |
| B1P11-Q47 | 11 | AI-era: you are handed an AI-generated ML system design or architecture doc. What red flags do you look for in review? |
| B1P11-Q48 | 11 | Design a system that handles delayed conversion feedback (ads / lending) when labels arrive days or weeks late. |
| B1P11-Q49 | 11 | How do you correct position bias and evaluate a ranker offline using logged data (counterfactual evaluation)? |
| B1P11-Q50 | 11 | Design a multi-objective ranking system balancing engagement, revenue, creator fairness and integrity. |
| B1P11-Q51 | 11 | Design a fairness and bias audit process for a credit-scoring model. |
| B1P11-Q52 | 11 | Design an inventory replenishment system for dark stores combining forecasting and optimisation. |
| B1P12-Q1 | 12 | Given a transactions DataFrame (user_id, ts, amount, category), use groupby with named aggregation to get per-user total, mean, count and last-transaction date, then return the top 3 categories by spend for each user. |
| B1P12-Q2 | 12 | Write code to audit missing values in a DataFrame (count, percent, pattern by group) and impute numeric and categorical columns sensibly. Why must the imputation statistics come from the training split only? |
| B1P12-Q3 | 12 | Explain and demonstrate .loc vs .iloc vs boolean masking, and fix a SettingWithCopyWarning / chained-assignment bug (df[df.a>0]['b'] = 1). What changes with copy-on-write? |
| B1P12-Q4 | 12 | Merge a 1M-row orders table with a customers table and the row count unexpectedly grows. Write code to find the cause (duplicate keys), prevent it (validate=, indicator=) and fix it. |
| B1P12-Q5 | 12 | This iterrows/apply(axis=1) code takes 10 minutes on 5M rows. Rewrite it vectorized (np.where / np.select / map / merge) and explain why it is faster. |
| B1P12-Q6 | 12 | Review this snippet: StandardScaler is fit on the full dataset before train_test_split. Identify the leakage, explain the impact, and rewrite it correctly with a Pipeline. |
| B1P12-Q7 | 12 | Build an sklearn Pipeline with ColumnTransformer (median imputer + scaler for numeric; most-frequent imputer + OneHotEncoder(handle_unknown='ignore') for categorical) feeding a classifier, and evaluate it with cross_val_score. |
| B1P12-Q8 | 12 | Use groupby transform vs agg vs apply: add a column with each row's group mean, z-score within group, and share of group total. When is each the right tool? |
| B1P12-Q9 | 12 | Review this LLM-generated training script for bugs: it applies SMOTE before CV, evaluates on the training set, uses shuffled KFold on time-ordered data and reports accuracy on a 2% positive class. List and fix every issue. |
| B1P12-Q10 | 12 | Create 7-day and 30-day rolling mean/count features per customer from an event log without leaking future information (shift, closed='left', time-based windows). |
| B1P12-Q11 | 12 | Write code for correct cross-validation when rows are grouped (multiple rows per user) or time-ordered: use GroupKFold / TimeSeriesSplit / StratifiedGroupKFold and show how naive KFold inflates the score. |
| B1P12-Q12 | 12 | Implement out-of-fold target encoding for a high-cardinality categorical feature in pandas/NumPy, with smoothing, and show why naive target encoding leaks. |
| B1P12-Q13 | 12 | Implement AUC-ROC and average precision from scratch in NumPy (handle tied scores) and verify against sklearn.metrics. |
| B1P12-Q14 | 12 | A model shows 99% test accuracy. Given this broken notebook (fit_transform on test, duplicated rows across the split, an ID-like feature, a target-derived column), debug it step by step. |
| B1P12-Q15 | 12 | Clean a messy CSV: mixed date formats, numeric columns stored as strings with currency symbols and commas, inconsistent category spellings, duplicates, and impossible values. Show your code and your checks. |
| B1P12-Q16 | 12 | Write a custom sklearn transformer (BaseEstimator, TransformerMixin) that clips outliers at train-set quantiles and works inside a Pipeline and GridSearchCV. What goes in fit vs transform? |
| B1P12-Q17 | 12 | Compute the pairwise Euclidean distance matrix and k-NN predictions for 10k x 50 data with no Python loops, using broadcasting and the (a-b)^2 expansion. Discuss memory and numerical issues. |
| B1P12-Q18 | 12 | Set up hyperparameter tuning with GridSearchCV/RandomizedSearchCV over a Pipeline and explain nested CV. Write code for an unbiased estimate of generalisation performance. |
| B1P12-Q19 | 12 | Reshape data: pivot_table, melt, stack/unstack and crosstab. Build a monthly cohort retention table from a signup and activity log. |
| B1P12-Q20 | 12 | Find and drop duplicates keeping the latest record per entity (sort_values + drop_duplicates vs groupby.tail/idxmax) and explain the differences. |
| B1P12-Q21 | 12 | Use pandas window-style operations per group: rank, cumsum, pct_change, lag/lead via shift, expanding and rolling aggregates. Compute 'days since previous order' and 'running spend'. |
| B1P12-Q22 | 12 | Sessionize a clickstream: start a new session when the gap between consecutive events per user exceeds 30 minutes, using groupby, diff and cumsum. |
| B1P12-Q23 | 12 | Load a 5 GB CSV on an 8 GB laptop: use dtypes, category, usecols, chunksize, Parquet, and compare with Polars/DuckDB. Show memory before and after. |
| B1P12-Q24 | 12 | Spot the bug: a function has a mutable default argument (def add_feature(df, cols=[])) and mutates its input DataFrame. Explain the symptom and fix it. Also show list-sharing and in-place mutation pitfalls in ML helper code. |
| B1P12-Q25 | 12 | Find the off-by-one / lookahead bug: labels are built with shift(-1) and rolling windows include the current day, so training features see the target. Fix it and add a test. |
| B1P12-Q26 | 12 | Implement K-fold and stratified K-fold splitting from scratch in NumPy (seeded, no leakage) and check class proportions per fold. |
| B1P12-Q27 | 12 | Implement numerically stable softmax, log-softmax and cross-entropy in NumPy (batch-wise), and show what breaks without the max-subtraction trick. |
| B1P12-Q28 | 12 | Do feature selection correctly: this code runs SelectKBest on all data and then cross-validates. Show the leakage with random noise features and rewrite with a Pipeline. |
| B1P12-Q29 | 12 | Handle class imbalance in code: class_weight vs RandomOverSampler/SMOTE inside an imblearn Pipeline and CV folds, and explain why resampling before the split is wrong. |
| B1P12-Q30 | 12 | Detect and cap outliers per group (IQR, z-score, winsorisation) in pandas and explain how doing it before the split can leak. |
| B1P12-Q31 | 12 | Make an experiment reproducible: control random_state in splits, models and np.random.default_rng, avoid global-state bugs, and explain why results still differ across machines or with n_jobs. |
| B1P12-Q32 | 12 | Save and load a trained pipeline with joblib, then write an inference function that validates columns, order, dtypes and unseen categories. What breaks in production if you only pickle the model? |
| B1P12-Q33 | 12 | Join an events table to the most recent price/feature snapshot at or before each event time (merge_asof) without lookahead. |
| B1P12-Q34 | 12 | Use cross_validate with multiple scorers, a custom scorer (F-beta or a business-cost metric via make_scorer) and return train and validation scores to diagnose overfitting. |
| B1P12-Q35 | 12 | Review LLM-generated pandas code that uses inplace=True, chained indexing, apply(axis=1), a hidden copy and silent dtype coercion. Point out correctness and performance bugs and rewrite it. |
| B1P12-Q36 | 12 | Compute running mean, variance and moving average in NumPy efficiently (cumsum, convolve, Welford's one-pass algorithm) and discuss catastrophic cancellation. |
| B1P12-Q37 | 12 | Handle a high-cardinality categorical feature (10k levels) in sklearn: frequency encoding, hashing, OrdinalEncoder with unknown_value, native categorical support in HistGradientBoosting. Write code and compare. |
| B1P12-Q38 | 12 | Write a data-validation function for incoming scoring data (schema, ranges, null rates, PSI drift vs training) that raises clear errors before the model is called. |
| B1P12-Q39 | 12 | Debug this 'works on my machine' sklearn notebook: results change after reordering columns, a ColumnTransformer silently drops a column (remainder), and get_feature_names_out fails. Fix it. |
| B1P12-Q40 | 12 | Given an LLM-written function to compute precision@k and NDCG@k, find the off-by-one, ties and empty-group bugs, fix it and write tests with known answers. |
| B1P12-Q41 | 12 | Check for duplicates and near-duplicates across train/test (same user, session, image or text) and write code that splits so no entity appears in both. Quantify the score inflation. |
| B1P12-Q42 | 12 | Implement permutation feature importance from scratch in NumPy for any fitted estimator, with repeated shuffles and a held-out set, and compare with sklearn.inspection. |
| B1P12-Q43 | 12 | Implement a non-parametric bootstrap confidence interval for a metric (e.g. AUC or median) in vectorised NumPy and state its limitations. |
| B1P12-Q44 | 12 | Write pytest unit tests for a data-processing function: pandas.testing.assert_frame_equal, edge cases (empty, all-null, duplicate keys), and a check that the transform never changes row count. |
| B1P12-Q45 | 12 | Use sparse matrices in an sklearn pipeline (OneHotEncoder sparse output, TF-IDF + numeric features via ColumnTransformer) and avoid accidentally densifying. |
| B1P12-Q46 | 12 | Explain views vs copies, strides and broadcasting rules in NumPy, then fix a bug where modifying a slice silently changes the original array. |
| B1P12-Q47 | 12 | Implement groupby-sum/mean/count from scratch in NumPy with np.unique(return_inverse) and np.bincount, then benchmark against pandas. |
| B1P12-Q48 | 12 | Translate a pandas pipeline to Polars (lazy) or DuckDB and explain when and why you would; what do pandas 2/3 features (Arrow dtypes, copy-on-write) change? |
| B1P12-Q49 | 12 | You may use an AI assistant in this round. Walk through how you would prompt it to write a feature pipeline, then verify it: what tests, invariants, leakage checks and baselines do you run before trusting the output? |
| B1P12-Q50 | 12 | Review a complete 150-line LLM-generated ML script end to end (train/test handling, CV, metric choice, threshold, seeds, logging, hidden global state) and produce a prioritised list of review comments with fixes. |
| B1P12-Q51 | 12 | Use ColumnTransformer with set_output(transform='pandas'), feature names and custom column selectors to build a pipeline that survives schema evolution, and show how you would test that. |
| B1P13-Q1 | 13 | Explain a p-value in plain words. What does it NOT mean? |
| B1P13-Q2 | 13 | Explain Type I and Type II errors. How are they related to alpha, beta and power, and which is costlier in practice? |
| B1P13-Q3 | 13 | What is the difference between standard deviation and standard error? |
| B1P13-Q4 | 13 | State the Central Limit Theorem. Why does it matter for data science, and when does it break down? |
| B1P13-Q5 | 13 | How do you correctly interpret a 95% confidence interval? Why is 'there is a 95% chance the true mean lies in it' wrong? |
| B1P13-Q6 | 13 | One-tailed vs two-tailed tests: when do you use each and what is the cost of choosing one-tailed? |
| B1P13-Q7 | 13 | What is the difference between covariance and correlation? Why is correlation preferred for comparing relationships? |
| B1P13-Q8 | 13 | Describe the normal distribution: properties, the 68-95-99.7 rule, z-scores and standardisation. How do you check if data is normal? |
| B1P13-Q9 | 13 | t-test vs z-test: when do you use which? What are the assumptions of a t-test? |
| B1P13-Q10 | 13 | Statistical significance vs practical significance: a result has p = 0.001 but a tiny effect. What do you do? |
| B1P13-Q11 | 13 | What is statistical power and what factors affect it? How would you increase it? |
| B1P13-Q12 | 13 | How do you compute the required sample size for a two-proportion (conversion-rate) test? Show it in scipy/statsmodels. |
| B1P13-Q13 | 13 | What is the multiple comparisons problem? Explain Bonferroni and Benjamini-Hochberg and when to use each. |
| B1P13-Q14 | 13 | Explain the chi-squared test (independence and goodness of fit). What are its assumptions? |
| B1P13-Q15 | 13 | Parametric vs non-parametric tests: when would you use Mann-Whitney U instead of a t-test? |
| B1P13-Q16 | 13 | What is the bootstrap? Explain how to get a confidence interval with it and implement it in NumPy. |
| B1P13-Q17 | 13 | Binomial vs Poisson: when does each apply, and when does Poisson approximate binomial? |
| B1P13-Q18 | 13 | What is sampling bias? Give examples (selection, survivorship, non-response) and how you would detect and mitigate them. |
| B1P13-Q19 | 13 | What makes an estimator good? Explain bias, variance, MSE, and why the sample variance divides by n-1. |
| B1P13-Q20 | 13 | Explain maximum likelihood estimation. Derive the MLE for a Bernoulli probability and for a normal mean and variance. |
| B1P13-Q21 | 13 | What is the Law of Large Numbers and how is it different from the CLT? |
| B1P13-Q22 | 13 | Uniform distribution: mean, variance, and how do you use it to generate samples from any distribution (inverse transform)? |
| B1P13-Q23 | 13 | Exponential distribution: what is memorylessness and how does it relate to the Poisson process? |
| B1P13-Q24 | 13 | Paired vs independent two-sample t-test: when is each valid and what happens if you pick wrong? |
| B1P13-Q25 | 13 | What is Welch's t-test and why is it usually the default over the pooled-variance t-test? |
| B1P13-Q26 | 13 | Explain one-way ANOVA and the F-statistic. What do you do after a significant ANOVA (post-hoc tests)? |
| B1P13-Q27 | 13 | Fisher's exact test vs chi-squared test: when do you prefer Fisher's? |
| B1P13-Q28 | 13 | How do you test for normality (Shapiro-Wilk, Q-Q plot)? Do you actually need normality for a t-test? |
| B1P13-Q29 | 13 | What is the Kolmogorov-Smirnov test? How do you use it for one-sample and two-sample comparisons (e.g., drift detection)? |
| B1P13-Q30 | 13 | Explain sampling methods: simple random, stratified, cluster, systematic. When is stratified better? |
| B1P13-Q31 | 13 | Pearson vs Spearman vs Kendall correlation: when do you use each? |
| B1P13-Q32 | 13 | Can two variables have zero correlation and still be dependent? Give an example. |
| B1P13-Q33 | 13 | Method of Moments vs MLE: how does MoM work, and when would you prefer one? |
| B1P13-Q34 | 13 | How are the t, chi-squared and F distributions related? Where does each arise? |
| B1P13-Q35 | 13 | What is p-hacking? How do researchers misuse p < 0.05 and how do you guard against it? |
| B1P13-Q36 | 13 | Confidence interval for a proportion: Wald vs Wilson. Why does Wald fail for small n or extreme p? |
| B1P13-Q37 | 13 | Confidence interval vs prediction interval vs tolerance interval: what is the difference? |
| B1P13-Q38 | 13 | FWER vs FDR: how do Bonferroni, Holm and Benjamini-Hochberg differ in what they control and in power? |
| B1P13-Q39 | 13 | Your conversion rate went from 10.0% to 10.4% with 50,000 users per arm. Run the two-proportion z-test and interpret it. |
| B1P13-Q40 | 13 | Explain degrees of freedom intuitively. Why does the t-distribution depend on it? |
| B1P13-Q41 | 13 | What is effect size (Cohen's d, relative lift) and why report it alongside a p-value? |
| B1P13-Q42 | 13 | What is the duality between confidence intervals and hypothesis tests? |
| B1P13-Q43 | 13 | How do you choose the right distribution for real data: delivery time, number of orders per hour, conversion rate, order value? |
| B1P13-Q44 | 13 | How do you compute a sample size to estimate a mean (or proportion) within a given margin of error? |
| B1P13-Q45 | 13 | Implement a two-sample (Welch) t-test from scratch in NumPy and verify against scipy.stats.ttest_ind. |
| B1P13-Q46 | 13 | What is regression to the mean and the winner's curse? How do they distort the analysis of top-performing segments? |
| B1P13-Q47 | 13 | Revenue-per-user is heavy-tailed. Is a t-test still valid? What would you do (log transform, trimming, bootstrap, Mann-Whitney)? |
| B1P13-Q48 | 13 | What is a permutation test? When is it preferable to a t-test and how do you implement it? |
| B1P13-Q49 | 13 | Wilcoxon signed-rank and Kruskal-Wallis: what do they test and what are their assumptions? |
| B1P13-Q50 | 13 | How do you estimate power by Monte Carlo simulation when no closed-form formula exists? |
| B1P13-Q51 | 13 | An LLM gives you a statistical analysis (test choice, p-value, interpretation) for your data. How do you review it for errors? |
| B1P13-Q52 | 13 | What are consistency, efficiency and sufficiency of an estimator? State the Cramer-Rao lower bound. |
| B1P13-Q53 | 13 | What is Fisher information, and why is the MLE asymptotically normal? How do you get a standard error from it? |
| B1P13-Q54 | 13 | How does the delta method give a standard error for a ratio metric (e.g., revenue per session)? |
| B1P13-Q55 | 13 | What exactly does the Mann-Whitney U test test? Is it a test of medians? What are the pitfalls? |
| B1P13-Q56 | 13 | When does the bootstrap fail? What are percentile vs BCa intervals and what is the bootstrap for dependent (time-series) data? |
| B1P13-Q57 | 13 | Count data is overdispersed relative to Poisson. How do you detect it and what do you do (negative binomial, quasi-Poisson)? |
| B1P13-Q58 | 13 | How does FDR control behave under dependent tests? Explain q-values and Benjamini-Yekutieli. |
| B1P13-Q59 | 13 | What is an equivalence / non-inferiority test (TOST)? When would you use it instead of a standard test? |
| B1P13-Q60 | 13 | Cauchy distribution: why do the LLN and CLT fail, and what does it teach about heavy tails? |
| B1P13-Q61 | 13 | What is the design effect for clustered or correlated observations, and how does it change standard errors and sample size? |
| B1P14-Q1 | 14 | You toss a fair coin twice: what is the probability of two heads in a row, and what is the expected number of tosses until the first head? |
| B1P14-Q2 | 14 | Birthday problem: how many people until there is a >50% chance two share a birthday? Derive it and extend to hash collisions. |
| B1P14-Q3 | 14 | A disease affects 1% of people and a test is 99% sensitive and 95% specific. You test positive: what is the probability you have the disease? Why is the answer so low? |
| B1P14-Q4 | 14 | Monty Hall: should you switch doors? Prove it, then simulate it in Python. |
| B1P14-Q5 | 14 | Expected number of rolls of a fair die until you see every face at least once (coupon collector), and how does it scale with n? |
| B1P14-Q6 | 14 | Design a spam filter from first principles using Bayes theorem: P(spam | word) given word frequencies. What assumption makes Naive Bayes work and when does it break? |
| B1P14-Q7 | 14 | Expected number of fair-coin tosses until you see HH vs HT: why are they different? |
| B1P14-Q8 | 14 | Boy-or-girl puzzle: a family has two children and at least one is a boy: probability both are boys? What if you know the older one is a boy? |
| B1P14-Q9 | 14 | You have a biased coin with unknown bias p: how do you simulate a fair coin? Extend it to generate 7 equally likely outcomes from a biased binary source. |
| B1P14-Q10 | 14 | List the assumptions of OLS. Which are needed for unbiased coefficients and which only for valid standard errors / confidence intervals? |
| B1P14-Q11 | 14 | What is heteroscedasticity? How do you detect it (residual plots, Breusch-Pagan, White) and fix it (robust SEs, log transform, WLS)? |
| B1P14-Q12 | 14 | How do you read residual plots (residuals vs fitted, Q-Q, scale-location, residuals vs leverage) and what pattern signals which problem? |
| B1P14-Q13 | 14 | Frequentist vs Bayesian: explain a 95% confidence interval vs a 95% credible interval in plain words, with a conversion-rate example. |
| B1P14-Q14 | 14 | Beta-Binomial: your prior for a conversion rate is Beta(a, b) and you observe k conversions in n visits. What is the posterior, its mean, and a 95% credible interval? Show it in scipy. |
| B1P14-Q15 | 14 | Explain CUPED: what does it do, what is the formula, why is it unbiased, and how much variance does it remove? |
| B1P14-Q16 | 14 | What is the peeking problem? Simulate how checking an A/B test daily inflates the false-positive rate, and name two valid fixes. |
| B1P14-Q17 | 14 | How do you estimate a probability, an integral or pi using Monte Carlo? How many simulations do you need for a given accuracy? |
| B1P14-Q18 | 14 | Why does a Bayesian posterior depend on the prior and how do you pick one? Show how the posterior changes for an informative vs a flat prior and small vs large n. |
| B1P14-Q19 | 14 | You test positive twice on independent tests, or the test is run on a high-risk group: how do you update the posterior? Where does the independence assumption break? |
| B1P14-Q20 | 14 | A game pays Rs 100 if you roll a six and nothing otherwise; the entry fee is Rs 20. Should you play and what is the variance of your winnings? |
| B1P14-Q21 | 14 | Two cards are drawn from a 52-card deck without replacement: probability both are aces, probability of a pair, probability the second card is red given the first is red? |
| B1P14-Q22 | 14 | What are leverage and Cook's distance? How do you flag an influential point and what do you do with it? |
| B1P14-Q23 | 14 | Explain P(A|B) vs P(B|A) with the prosecutor's fallacy. When are two events independent vs mutually exclusive? |
| B1P14-Q24 | 14 | Expected value of the maximum of two (and of n) fair dice rolls; max of n Uniform(0,1) variables. |
| B1P14-Q25 | 14 | Use linearity of expectation: expected number of fixed points in a random permutation, expected number of distinct birthdays, expected number of empty bins. |
| B1P14-Q26 | 14 | Gambler's ruin: you start with Rs i, bet Rs 1 on a fair coin, stop at 0 or N. What is the probability of ruin and expected duration? What changes if the coin is biased? |
| B1P14-Q27 | 14 | Simple symmetric random walk: what is the probability of returning to the origin, expected steps to hit +a or -b, and why does it matter for stock-price modelling? |
| B1P14-Q28 | 14 | What is a Markov chain? How do you find the stationary distribution of a transition matrix, and when does it exist and converge? |
| B1P14-Q29 | 14 | Model user states (active, dormant, churned) as a Markov chain: how do you estimate the transition matrix, compute expected lifetime, and sanity-check the Markov assumption? |
| B1P14-Q30 | 14 | How is PageRank a Markov chain? Explain the damping factor and implement power iteration in NumPy. |
| B1P14-Q31 | 14 | Bayesian A/B test: with Beta posteriors for A and B, how do you compute P(B > A) and expected loss? How does it differ from a p-value? |
| B1P14-Q32 | 14 | Give the main ways to reduce variance in an experiment metric (CUPED/regression adjustment, stratification, post-stratification, winsorizing, control variates) and when to use which. |
| B1P14-Q33 | 14 | How do you choose a CUPED covariate? Why must it be pre-experiment, what happens with new users who have no history, and does CUPED work with ratio metrics? |
| B1P14-Q34 | 14 | Explain group sequential testing and alpha spending (Pocock, O'Brien-Fleming). Why do these boundaries control Type I error? |
| B1P14-Q35 | 14 | Does multicollinearity hurt prediction? How do ridge regression and PCA regression deal with it versus dropping variables? |
| B1P14-Q36 | 14 | Residuals look non-normal and right-skewed: what does it break (and not break), and when do you use a log or Box-Cox transform? |
| B1P14-Q37 | 14 | How do you detect and handle autocorrelated residuals (Durbin-Watson, Ljung-Box)? Why does it invalidate standard errors? |
| B1P14-Q38 | 14 | Break a stick at two random points: probability the three pieces form a triangle? |
| B1P14-Q39 | 14 | You flip a coin 10 times and get 10 heads: probability the next is heads? Compare the frequentist MLE, Laplace smoothing and a Beta prior. |
| B1P14-Q40 | 14 | Use the laws of total expectation and total variance: a random number of customers each spends a random amount. What are the mean and variance of total revenue? |
| B1P14-Q41 | 14 | Empirical Bayes shrinkage: how do you rank restaurants or products by CTR or rating when some have very few observations? |
| B1P14-Q42 | 14 | AI-era: an LLM benchmark shows 83/100 correct for model A vs 80/100 for model B. How do you give a credible interval and decide if A is better? How would you review an LLM-generated statistical analysis for errors? |
| B1P14-Q43 | 14 | Walk through statsmodels OLS output: R-squared vs adjusted R-squared, F-test, t-stats, condition number warning, Durbin-Watson, Jarque-Bera. What would you check next? |
| B1P14-Q44 | 14 | Explain MLE vs MAP vs full Bayesian inference and how L2/L1 regularization map to Gaussian/Laplace priors. |
| B1P14-Q45 | 14 | Expected number of tosses to see HHH (or HTH) using Markov chain states or martingales. |
| B1P14-Q46 | 14 | Non-transitive dice: A beats B, B beats C, C beats A. Verify it by simulation, and compute the probability that one die beats another. |
| B1P14-Q47 | 14 | Poker hand probabilities: probability of a flush, a full house, and being dealt at least one ace in five cards. |
| B1P14-Q48 | 14 | St. Petersburg paradox and Kelly criterion: why is expected value not enough for decisions? How do you size a bet with positive edge? |
| B1P14-Q49 | 14 | Thompson sampling for a Bernoulli bandit: explain it using Beta posteriors and simulate it against epsilon-greedy. |
| B1P14-Q50 | 14 | Winsorizing, capping and trimming outliers: how do they reduce variance and what bias do they introduce? |
| B1P14-Q51 | 14 | Hat matrix and leverage: derive H = X(X'X)^-1 X', explain h_ii, and relate leverage to Cook's distance. |
| B1P14-Q52 | 14 | Frisch-Waugh-Lovell theorem: explain it and use it to interpret a coefficient in multiple regression and to see why CUPED is regression adjustment. |
| B1P14-Q53 | 14 | Distribution of the k-th order statistic of n Uniform(0,1) samples: derive it (Beta) and use it to get the expected median and expected range. |
| B1P14-Q54 | 14 | Expected maximum of n i.i.d. Exponential(1) variables, and why it grows like log n. |
| B1P14-Q55 | 14 | Secretary problem: what is the optimal stopping rule and why 1/e? |
| B1P14-Q56 | 14 | Absorbing Markov chains: use the fundamental matrix to find expected time to absorption and absorption probabilities. |
| B1P14-Q57 | 14 | Always-valid inference: explain mSPRT / confidence sequences and how they differ from group sequential designs. |
| B1P14-Q58 | 14 | Control variates and importance sampling in Monte Carlo: how do you estimate a rare-event probability with low variance? Show code. |
| B1P14-Q59 | 14 | Write a Metropolis-Hastings sampler from scratch in NumPy to sample a posterior. How do you diagnose convergence (trace, R-hat, ESS)? |
| B1P14-Q60 | 14 | Hierarchical Bayesian model / partial pooling: when do you use it, for example for store- or city-level conversion rates? |
| B1P14-Q61 | 14 | Delta method for ratio metrics (e.g. revenue per session) and its variance; how do you combine it with CUPED? |
| B1P14-Q62 | 14 | Heteroscedasticity-consistent standard errors (HC0-HC3) and cluster-robust SEs: when and why? |

## Book 2 — GenAI / LLM / RAG / Agentic AI
| Q-ID | Part | Canonical question |
|---|---|---|
| B2P01-Q1 | 1 | Explain self-attention step by step (Q, K, V, scaled dot-product, softmax). What does each of Q, K and V represent? |
| B2P01-Q2 | 1 | Why did transformers replace RNNs/LSTMs? What are the remaining drawbacks of transformers? |
| B2P01-Q3 | 1 | What is multi-head attention? Why use several heads instead of one big head, and what are the tensor shapes and cost? |
| B2P01-Q4 | 1 | Encoder-only vs decoder-only vs encoder-decoder models: how do they differ, with examples and when to use each? |
| B2P01-Q5 | 1 | What is the causal mask? Why can training be parallel over all tokens while generation is sequential? |
| B2P01-Q6 | 1 | What is the KV cache, why does it speed up generation, and how does its memory grow? |
| B2P01-Q7 | 1 | Prefill vs decode: what happens in each phase, and why is decode memory-bandwidth-bound while prefill is compute-bound? |
| B2P01-Q8 | 1 | Why does a transformer need positional information? Compare sinusoidal, learned and rotary (RoPE) encodings. |
| B2P01-Q9 | 1 | Why is self-attention O(n^2), and how do you cope with long sequences? |
| B2P01-Q10 | 1 | What are multi-query (MQA) and grouped-query attention (GQA)? How do they shrink the KV cache and what do they cost? |
| B2P01-Q11 | 1 | What is FlashAttention? Does it change the result, and why is it faster? |
| B2P01-Q12 | 1 | Walk through a transformer block: residual connections, normalisation, feed-forward network. Pre-LN vs post-LN? |
| B2P01-Q13 | 1 | Code: implement causal scaled dot-product (multi-head) self-attention from scratch in PyTorch or NumPy. |
| B2P01-Q14 | 1 | Walk through one forward pass of a decoder-only LLM, from text to next-token probabilities. |
| B2P01-Q15 | 1 | Live maths: estimate parameter count and KV-cache memory for a Llama-style model (layers, heads, head dim, context, batch). |
| B2P01-Q16 | 1 | BERT vs GPT: pretraining objectives, attention pattern, typical uses. Why did decoder-only models come to dominate? |
| B2P01-Q17 | 1 | Why do we divide attention scores by sqrt(d_k)? Give the variance argument. |
| B2P01-Q18 | 1 | How does RoPE work, and how do position interpolation, NTK-aware scaling and YaRN extend context length? |
| B2P01-Q19 | 1 | What is the context window, and why is the effective context often shorter than the advertised one ("lost in the middle")? |
| B2P01-Q20 | 1 | LayerNorm vs RMSNorm: what changes and why do modern LLMs prefer RMSNorm? |
| B2P01-Q21 | 1 | What does the feed-forward network do in a transformer? Explain GELU vs SwiGLU/gated FFNs and where most parameters live. |
| B2P01-Q22 | 1 | What is cross-attention, where is it used (T5, Whisper, diffusion, multimodal) and how does it differ from self-attention? |
| B2P01-Q23 | 1 | Which levers reduce KV-cache memory (GQA, quantised cache, sliding window, eviction)? Compare their trade-offs. |
| B2P01-Q24 | 1 | What are prompt/prefix caching in LLM APIs, and how do they relate to the KV cache? How do you structure prompts to benefit? |
| B2P01-Q25 | 1 | Explain input embeddings, the unembedding (LM head) layer and weight tying. How does vocabulary size affect model size and cost? |
| B2P01-Q26 | 1 | Where do a transformer's parameters live (attention vs FFN vs embeddings)? How is head dimension chosen? |
| B2P01-Q27 | 1 | Transformers vs state-space models (Mamba), linear attention and hybrid architectures: when would you pick each? |
| B2P01-Q28 | 1 | Do attention weights explain a model's output? What are induction heads and how do they relate to in-context learning? |
| B2P01-Q29 | 1 | What are sliding-window, local and sparse attention? What are attention sinks and why do they matter for streaming? |
| B2P01-Q30 | 1 | What breaks when you go from 8k to 128k–1M context (compute, memory, quality)? What is ring attention / sequence parallelism at a high level? |
| B2P01-Q31 | 1 | How do multimodal LLMs ingest images (ViT patches, projector, cross-attention vs token concatenation)? |
| B2P01-Q32 | 1 | Use arithmetic intensity (roofline thinking) to explain why batching helps decode throughput and when it stops helping. |
| B2P01-Q33 | 1 | What is Multi-head Latent Attention (MLA, as in DeepSeek)? How does it compress the KV cache versus GQA? |
| B2P01-Q34 | 1 | Explain Mixture-of-Experts layers: routing, load balancing, active vs total parameters, and the serving trade-offs. |
| B2P01-Q35 | 1 | Code: write a decoding loop with a KV cache and verify it matches the no-cache output. |
| B2P01-Q36 | 1 | Explain transformers to a non-technical stakeholder in two minutes. |
| B2P01-Q37 | 1 | Derive the sinusoidal positional encoding and its relative-position property. Why is it rarely used in modern LLMs? |
| B2P01-Q38 | 1 | ALiBi vs RoPE: how does each handle length extrapolation? |
| B2P01-Q39 | 1 | What architectural choices do modern open LLMs (Llama, Qwen, DeepSeek) make: RMSNorm, SwiGLU, RoPE, GQA, no biases, tied embeddings? Why? |
| B2P01-Q40 | 1 | Do attention heads specialise? What does head pruning or head ablation tell you? |
| B2P01-Q41 | 1 | AI code review: this LLM-written attention snippet has bugs (softmax dim, missing mask, missing scaling, wrong reshape). Find and fix them. |
| B2P01-Q42 | 1 | Code: implement rotary position embeddings (RoPE) and show that scores depend on relative position. |
| B2P01-Q43 | 1 | Derive FlashAttention's online softmax and explain how tiling reduces HBM reads/writes. |
| B2P01-Q44 | 1 | What stability tricks do large transformers use (pre-norm, QK-norm, logit soft-capping, z-loss, warmup)? Why do loss spikes happen? |
| B2P01-Q45 | 1 | What is multi-token prediction, and how does it relate to speculative decoding? |
| B2P01-Q46 | 1 | Diffusion language models vs autoregressive LLMs: how do they differ, and what are the trade-offs? |
| B2P01-Q47 | 1 | Design question: choose the architecture and attention variant for a 32k-context, low-latency chat model that must run on one GPU. |
| B2P02-Q1 | 2 | Why do LLMs use subword tokenization instead of words or characters? Compare BPE, WordPiece and Unigram/SentencePiece. |
| B2P02-Q2 | 2 | Greedy decoding vs sampling vs beam search: how does each choose the next token, and when would you use which? |
| B2P02-Q3 | 2 | What is the pretraining objective of a decoder-only LLM? Write the next-token cross-entropy loss and explain the label shift. |
| B2P02-Q4 | 2 | Explain temperature, top-k and top-p (nucleus) sampling. What does each do to the distribution and what are sensible values? |
| B2P02-Q5 | 2 | Token maths: how many tokens is 1,000 words, why do code, JSON and non-English text cost more, and how would you cut token spend? |
| B2P02-Q6 | 2 | Why do LLMs struggle with counting letters ("strawberry"), arithmetic and string reversal? What does tokenization have to do with it? |
| B2P02-Q7 | 2 | What is perplexity? How does it relate to cross-entropy loss, and why can't you compare it across models with different tokenizers? |
| B2P02-Q8 | 2 | Pretraining vs continued pretraining vs fine-tuning: what changes in data, objective, cost and risk, and when do you choose each? |
| B2P02-Q9 | 2 | Walk through a pretraining data pipeline: sources, cleaning, quality filtering, language ID, PII/toxicity filtering, deduplication and mixing. |
| B2P02-Q10 | 2 | What are LLM scaling laws? What do loss versus parameters, data and compute look like, and what can you do with them? |
| B2P02-Q11 | 2 | What did Chinchilla find? Use C ~ 6ND to work out the compute-optimal model size and token count for a given budget. |
| B2P02-Q12 | 2 | Code: implement a byte-pair-encoding tokenizer (train, encode, decode) with deterministic tie-breaking, and show a round trip. |
| B2P02-Q13 | 2 | Code: implement temperature, top-k and top-p sampling from a logits vector, and verify it empirically. |
| B2P02-Q14 | 2 | How do you choose a tokenizer vocabulary size? Discuss sequence length, embedding/softmax cost, rare-token under-training and multilingual coverage. |
| B2P02-Q15 | 2 | What is byte-level BPE, why does it remove out-of-vocabulary tokens, and what are its trade-offs (UTF-8, byte fallback)? |
| B2P02-Q16 | 2 | What are special tokens (BOS, EOS, PAD, role/chat tokens) and chat templates? What breaks if the template or padding side is wrong? |
| B2P02-Q17 | 2 | Why do Indian and other low-resource languages cost more tokens (the "token tax")? What can you do about it? |
| B2P02-Q18 | 2 | What are glitch or under-trained tokens, why do they exist, and how would you detect them? |
| B2P02-Q19 | 2 | What are min-p and typical sampling, and in what order should samplers (penalties, temperature, truncation) be applied? |
| B2P02-Q20 | 2 | Why do LLMs repeat themselves, and how do repetition, frequency and presence penalties work? When do penalties hurt (code, JSON)? |
| B2P02-Q21 | 2 | Is temperature 0 deterministic? What causes run-to-run differences in LLM output, and how do you get reproducibility? |
| B2P02-Q22 | 2 | How does generation stop? Explain EOS, stop sequences, max tokens, finish reasons, truncation and streaming. |
| B2P02-Q23 | 2 | What are logprobs? How can you use token log-probabilities for confidence, classification and calibration, and what is logit bias? |
| B2P02-Q24 | 2 | Beam search in detail: length normalisation, cost in compute and KV memory, and why it works for translation but not open-ended chat. |
| B2P02-Q25 | 2 | How do you deduplicate a pretraining corpus (exact vs near-duplicate, MinHash/LSH)? Why does it matter? |
| B2P02-Q26 | 2 | What does a standard LLM pretraining optimisation recipe look like (AdamW settings, warmup, cosine or WSD decay, weight decay, gradient clipping), and why each piece? |
| B2P02-Q27 | 2 | Why is bf16 preferred over fp16 for LLM pretraining? Cover exponent range vs mantissa, fp32 master weights and optimizer states, which ops stay in fp32, and what FP8 changes. |
| B2P02-Q28 | 2 | How do you choose batch size in LLM pretraining (tokens per step, gradient accumulation, critical batch size, learning-rate scaling)? |
| B2P02-Q29 | 2 | How do you read a pretraining loss curve? What do spikes, divergence, plateaus and a train/validation gap tell you, and what would you do? |
| B2P02-Q30 | 2 | How do you decontaminate a pretraining corpus against benchmarks (n-gram overlap, canary strings, dynamic test sets) and detect contamination in a finished model? |
| B2P02-Q31 | 2 | Why do LLMs memorise and regurgitate training data? What makes it worse, and how do you reduce privacy and copyright risk? |
| B2P02-Q32 | 2 | Why do modern models train far beyond the Chinchilla-optimal token count (e.g. an 8B model on ~15T tokens)? What is inference-aware scaling? |
| B2P02-Q33 | 2 | Estimate the cost of pretraining a 7B model on 2T tokens: FLOPs, GPU-hours, model FLOPs utilisation (MFU) and rough dollars. |
| B2P02-Q34 | 2 | Live maths: how much GPU memory does training a 7B model need (weights, gradients, Adam states, activations)? Explain data, tensor and pipeline parallelism and ZeRO/FSDP at a high level. |
| B2P02-Q35 | 2 | AI code review: this LLM-written sampling function has bugs (top-p off-by-one, wrong order of temperature and softmax, no renormalisation, mutated logits). Find and fix them. |
| B2P02-Q36 | 2 | How would you extend a tokenizer and model to a new domain or language (new tokens, embedding initialisation, continued pretraining)? What goes wrong? |
| B2P02-Q37 | 2 | Tokenizer-free and byte-level models (ByT5, byte-latent transformers) and digit tokenisation choices: what are the trade-offs? |
| B2P02-Q38 | 2 | Data mixtures, curriculum, annealing and synthetic data in pretraining: what helps, and what is model collapse? |
| B2P02-Q39 | 2 | How many epochs over the same data are acceptable? What do data-constrained scaling results say about repeating data? |
| B2P02-Q40 | 2 | Are emergent abilities real or an artefact of the metric? How would you test it? |
| B2P02-Q41 | 2 | What are the limits and critiques of scaling laws (fit uncertainty, extrapolation risk, the data wall, test-time compute)? |
| B2P02-Q42 | 2 | Decoding-time methods to improve quality: self-consistency, contrastive decoding and DoLa. How do they work and what do they cost? |
| B2P02-Q43 | 2 | Test-time compute: best-of-n, majority voting and long chain-of-thought sampling. How do cost, latency and accuracy trade off? |
| B2P02-Q44 | 2 | Design question: choose decoding settings and stop rules for four products (code completion, support chat, creative writing, data extraction) and defend them. |
| B2P03-Q1 | 3 | What are zero-shot, one-shot and few-shot prompting? Why do examples often beat a longer description, and how do you pick them? |
| B2P03-Q2 | 3 | System, user and assistant messages: what is each role for, what goes where, and what happens when instructions conflict? |
| B2P03-Q3 | 3 | What is chain-of-thought prompting? When does it help, what does it cost in latency and tokens, and when does it hurt? |
| B2P03-Q4 | 3 | How do you structure a complex prompt (sections, delimiters or XML tags, ordering, where to put key instructions, what to do when a condition is not met)? |
| B2P03-Q5 | 3 | How do you design prompts to reduce hallucinations (grounding, permission to say "I don't know", citations, temperature)? What are the limits of prompting here? |
| B2P03-Q6 | 3 | How do you iterate on a prompt systematically? How do you know a prompt change did not make things worse (golden set, one change at a time, regression runs)? |
| B2P03-Q7 | 3 | How do you get reliable JSON from an LLM? Compare prompt-only, JSON mode, schema-based structured outputs, function calling and constrained decoding. |
| B2P03-Q8 | 3 | Explain function calling end to end: tool definitions, the model emitting a call, your code executing it, returning the result, and the final answer. |
| B2P03-Q9 | 3 | How do you design good tool or function definitions (names, descriptions, parameter schemas, enums, how many tools)? |
| B2P03-Q10 | 3 | Your agent returns valid JSON but the numbers are sometimes wrong. Where do you look first? Why is valid not the same as correct? |
| B2P03-Q11 | 3 | Code: implement a function-calling loop against a mocked model: parse the call, validate arguments, execute, return the result, with a maximum number of steps. |
| B2P03-Q12 | 3 | Code: validate LLM JSON output against a schema, repair or retry with a bounded budget, and fail closed when retries run out. |
| B2P03-Q13 | 3 | How do you select and order few-shot examples (coverage, label balance, recency bias, dynamic selection by retrieval)? |
| B2P03-Q14 | 3 | Zero-shot CoT, few-shot CoT, self-consistency and reasoning models: when does explicit "think step by step" prompting help, and when is it counter-productive? |
| B2P03-Q15 | 3 | What is ReAct prompting (thought, action, observation) and how does it differ from plain chain-of-thought? |
| B2P03-Q16 | 3 | Task decomposition and prompt chaining versus one big prompt: when do you split, and how do you choose the decomposition? |
| B2P03-Q17 | 3 | How should a prompt handle ambiguity and missing information (fallback behaviour, clarifying questions, defaults, missing tool parameters)? |
| B2P03-Q18 | 3 | What is context engineering? How do you decide what goes into the context window, and how do you manage long-running conversations (rolling summary vs retrieval)? |
| B2P03-Q19 | 3 | Does role or persona prompting ("you are an expert...") help? How do you control tone and style reliably? |
| B2P03-Q20 | 3 | Negative constraints and instruction following: why do "do not" instructions fail, how do you resolve conflicting instructions, and what works better? |
| B2P03-Q21 | 3 | How do you control output length and format (explicit specs, examples, stop sequences, max tokens)? What goes wrong with truncation? |
| B2P03-Q22 | 3 | What does constrained decoding do at the logit level? How does a schema become a grammar or state machine, and what does it guarantee and not guarantee? |
| B2P03-Q23 | 3 | What does a provider's strict structured-output mode require of your JSON schema (additionalProperties, required fields, optional fields), and what are the limits of the supported schema subset? |
| B2P03-Q24 | 3 | Does forcing a structured format hurt answer quality? How do field order and a free-text reasoning field help? |
| B2P03-Q25 | 3 | What are the tool_choice options (auto, required, forced function, none, allowed tools) and when do you use each? |
| B2P03-Q26 | 3 | Parallel tool calls: when can the model make several calls in one turn, how do you return results, and when do you disable it? |
| B2P03-Q27 | 3 | What are the common tool-calling failure modes (wrong tool, hallucinated arguments, unnecessary calls, loops, timeouts) and how do you debug them? |
| B2P03-Q28 | 3 | Retries, idempotency and side effects in tool calls: how do you avoid duplicate refunds or double writes, and when do you require human approval? |
| B2P03-Q29 | 3 | How should tool results and errors be returned to the model (compact structured errors, truncating large results, untrusted content)? |
| B2P03-Q30 | 3 | What happens when an agent has too many tools? Discuss selection accuracy, the token cost of tool definitions, grouping and tool search or deferred loading. |
| B2P03-Q31 | 3 | JSON mode vs structured outputs vs function calling vs prompt-only: how do they differ in guarantees, and when would you pick each? |
| B2P03-Q32 | 3 | How do you evaluate prompts (metrics by task type, rubrics for subjective outputs)? What are the limits of LLM-as-judge for this? |
| B2P03-Q33 | 3 | How do you version, test and roll out prompts in production (prompt store, canary, A/B, rollback)? Where should prompts live? |
| B2P03-Q34 | 3 | What is prompt injection (direct vs indirect), why do prompt-only defences fall short, and what structural defences help (separation, least privilege)? |
| B2P03-Q35 | 3 | How sensitive are LLMs to prompt wording, format and example order, and how do you test a prompt's robustness? |
| B2P03-Q36 | 3 | How do you cut cost and latency through prompt design (shorter prompts, caching-friendly structure, smaller models, routing)? |
| B2P03-Q37 | 3 | AI code review: this LLM-written tool-calling loop has bugs (no step limit, wrong tool_use_id, unvalidated arguments, ignored stop reason or parallel calls, swallowed exceptions). Find and fix them. |
| B2P03-Q38 | 3 | Design a reliability stack for an agent that issues refunds or changes account settings (schema validation, business rules, retries, approval, idempotency, audit). |
| B2P03-Q39 | 3 | When would you choose not to force a strict schema on a model, and what do you do instead? |
| B2P03-Q40 | 3 | A schema is generated per request and grammar compilation is slow. How do you keep p99 latency acceptable? |
| B2P03-Q41 | 3 | Design the prompts, tools, guardrails, escalation and evaluation for a production customer-support assistant. |
| B2P03-Q42 | 3 | Automatic prompt optimisation (DSPy-style compilation, meta-prompting, search over prompts): how does it work and when is it worth it? |
| B2P03-Q43 | 3 | How does prompting a reasoning model differ from prompting a standard chat model (reasoning effort or budget, less hand-holding, no step-by-step instructions)? |
| B2P03-Q44 | 3 | How would you evaluate tool use: tool-selection accuracy, argument accuracy, multi-turn calls, public function-calling benchmarks, and an in-house eval set? |
| B2P04-Q1 | 4 | Prompting vs RAG vs fine-tuning: what is your decision framework, and in what order do you try the adaptation methods? |
| B2P04-Q2 | 4 | What is supervised fine-tuning (instruction tuning)? What does it teach a model, what does it not teach, and what is the training loss? |
| B2P04-Q3 | 4 | What is LoRA and how does it work? Why is it parameter-efficient, and what stays frozen? |
| B2P04-Q4 | 4 | How do you choose LoRA's rank, alpha and dropout? What does the alpha/r scaling do? |
| B2P04-Q5 | 4 | Which modules should LoRA target (query/value only vs all linear layers including the MLP), and why? |
| B2P04-Q6 | 4 | What is QLoRA? Explain NF4, double quantization and paged optimizers, and where precision matters during training. |
| B2P04-Q7 | 4 | Memory maths: how much GPU memory does full fine-tuning, LoRA and QLoRA need for a 7B or 13B model, and can you fine-tune a 13B model on one 40 GB GPU? |
| B2P04-Q8 | 4 | What is catastrophic forgetting in fine-tuning? How do you detect it, and how do you mitigate it? |
| B2P04-Q9 | 4 | How do you evaluate a fine-tuned model before shipping (task metric, general-capability regression, human or LLM judging)? |
| B2P04-Q10 | 4 | How much data do you need for SFT, and what matters more, quality or quantity? How do you build and clean the dataset? |
| B2P04-Q11 | 4 | In SFT, why do we mask prompt tokens from the loss (train on completions or assistant turns only)? How do label shifting, the ignore index and packing interact? |
| B2P04-Q12 | 4 | Why do chat templates and the EOS token matter in fine-tuning? What breaks when training and inference templates differ? |
| B2P04-Q13 | 4 | How do you merge a LoRA adapter into the base model? Why does a merged LoRA add no latency, why can't a QLoRA adapter be merged directly, and when would you keep adapters separate? |
| B2P04-Q14 | 4 | Code: implement a LoRA linear layer from scratch in PyTorch (frozen weight, A and B initialisation, alpha/r scaling, merge) and verify it against W + BA. |
| B2P04-Q15 | 4 | Code: implement the SFT loss with prompt masking in PyTorch (shifted labels, ignore index) and check it against F.cross_entropy. |
| B2P04-Q16 | 4 | Full fine-tuning vs parameter-efficient fine-tuning: when is full fine-tuning justified, and how do learning rates differ? |
| B2P04-Q17 | 4 | What hyperparameters matter in SFT (learning rate, epochs, batch size, warmup, scheduler, max length), and how do you recognise overfitting? |
| B2P04-Q18 | 4 | Compare PEFT methods: adapters, prefix tuning, prompt tuning, IA3 and LoRA. When would you use each? |
| B2P04-Q19 | 4 | What do LoRA variants change (rsLoRA, DoRA, LoRA+, LoftQ initialisation)? When are they worth trying? |
| B2P04-Q20 | 4 | Does a higher LoRA rank always help? What limits capacity, and how do you decide when LoRA is not enough? |
| B2P04-Q21 | 4 | How do you create instruction data: human-written, synthetic from a stronger model, self-instruct? What are the quality and licensing risks? |
| B2P04-Q22 | 4 | What is knowledge distillation? Explain teacher and student, soft targets, temperature and the combined KL plus cross-entropy loss. |
| B2P04-Q23 | 4 | How does distillation work for LLMs: logit-level (white-box) vs sequence-level or response distillation (black-box)? Does the student need the teacher's tokenizer? |
| B2P04-Q24 | 4 | Forward vs reverse KL in LLM distillation (MiniLLM): what is the difference, and what does on-policy distillation fix? |
| B2P04-Q25 | 4 | When do you fine-tune a small model instead of calling a large API model? Work through a cost, latency, privacy and quality break-even. |
| B2P04-Q26 | 4 | For classification or extraction, would you fine-tune an LLM with SFT, add a classification head, or use a small encoder? How do you choose? |
| B2P04-Q27 | 4 | How do you mix tasks and general data in SFT (data mixtures, ordering, replay of general data), and what goes wrong with a narrow dataset? |
| B2P04-Q28 | 4 | How do you fine-tune for structured output or tool calling (dataset format, loss on tool calls, evaluation)? How does it relate to prompting for the same? |
| B2P04-Q29 | 4 | Continued pretraining vs SFT for a new domain or language: when do you need continued pretraining before SFT? |
| B2P04-Q30 | 4 | What does SFT overfitting look like (train vs validation loss, memorisation, narrow style), and what are your defences (early stopping, fewer epochs, regularisation, data)? |
| B2P04-Q31 | 4 | What training-efficiency settings matter in practice (sequence packing, padding-free batches, gradient checkpointing, gradient accumulation, bf16), and what do they cost? |
| B2P04-Q32 | 4 | How do you serve fine-tuned models: merged weights vs multi-LoRA serving, adapter swapping and versioning? |
| B2P04-Q33 | 4 | Hosted fine-tuning APIs vs self-hosted fine-tuning: what are the trade-offs in control, data privacy, cost and lock-in? |
| B2P04-Q34 | 4 | How do you keep PII and benchmark contamination out of fine-tuning data (deduplication, held-out sets, filtering)? |
| B2P04-Q35 | 4 | A fine-tune did not learn or got worse. Walk through your debugging checklist (template, masking, learning rate, data, evaluation). |
| B2P04-Q36 | 4 | Should you fine-tune a base or an instruct/chat checkpoint? What are the trade-offs? |
| B2P04-Q37 | 4 | AI code review: this LLM-written LoRA/SFT training script has bugs (unshifted or unmasked labels, wrong learning rate, merging in 4-bit, dropout left on at eval, wrong target modules). Find and fix them. |
| B2P04-Q38 | 4 | Why does low-rank adaptation work? Derive the parameter count, the identity initialisation, and the effective scaling of the update. |
| B2P04-Q39 | 4 | Chain-of-thought and rationale distillation: how do you distil reasoning from a stronger model, and what are the limits and risks? |
| B2P04-Q40 | 4 | What is the superficial alignment hypothesis (LIMA)? What evidence supports it, and what are its critiques and implications for data curation? |
| B2P04-Q41 | 4 | How do multi-adapter composition and model merging work (weighted adapters, task arithmetic, TIES-style merging), and what are the risks? |
| B2P04-Q42 | 4 | Design question: plan a fine-tune of a 13B-70B model on limited GPUs (QLoRA, gradient checkpointing, sharding), including how you validate the plan before spending the compute. |
| B2P04-Q43 | 4 | Design question: build an end-to-end fine-tuning project for a support-ticket extraction task (data, training, evaluation gates, regression checks, rollout and rollback). |
| B2P04-Q44 | 4 | Can fine-tuning inject new facts? Why does it often fail compared with retrieval, and what does the evidence say? |
| B2P04-Q45 | 4 | What are the pitfalls of distillation (capacity gap, exposure bias, evaluation, teacher licensing terms), and when does it fail? |
| B2P04-Q46 | 4 | How do you handle sequential or continual fine-tuning without forgetting (replay, per-task adapters, EWC-style regularisation, merging)? |
| B2P04-Q47 | 4 | What is rejection-sampling fine-tuning or self-improvement (RFT, STaR-style): how do you bootstrap SFT data from a model's own verified samples, and what can go wrong? |
| B2P05-Q1 | 5 | What is RLHF? Walk through the pipeline (SFT, reward model, policy optimisation) and explain why a base LLM needs it. |
| B2P05-Q2 | 5 | What is the KL penalty in RLHF, why is it needed, and what does the beta coefficient trade off? |
| B2P05-Q3 | 5 | What is reward hacking? Give examples (length bias, sycophancy) and the standard mitigations. |
| B2P05-Q4 | 5 | DPO vs PPO-based RLHF: how does DPO work, what does it remove, and when would you pick each? |
| B2P05-Q5 | 5 | How is a reward model trained? Explain preference pairs, the Bradley-Terry loss and the architecture. |
| B2P05-Q6 | 5 | Code: implement the DPO loss in PyTorch (log-probability ratios against a reference model, beta, implicit rewards) and test it on toy tensors. |
| B2P05-Q7 | 5 | How do you collect high-quality preference data (guidelines, annotator agreement, pair sampling, AI feedback)? |
| B2P05-Q8 | 5 | What are the guardrail layers in an LLM application (input rails, output rails, dialog or topic control, retrieval and tool checks)? |
| B2P05-Q9 | 5 | Jailbreaks vs prompt injection: what attack families exist and how do you defend in depth? |
| B2P05-Q10 | 5 | How do you evaluate a post-trained or aligned model (helpfulness, harmlessness, regressions, pairwise human or model judging, win rate)? |
| B2P05-Q11 | 5 | Your model started refusing benign requests after a safety-training round. What do you investigate and how do you fix it? |
| B2P05-Q12 | 5 | Code: implement PPO's clipped surrogate objective and the KL-regularised reward in PyTorch and check it on toy tensors. |
| B2P05-Q13 | 5 | PPO inside RLHF: policy, value head, advantages and GAE, clipping, and why four models (policy, reference, reward, value) are in memory. |
| B2P05-Q14 | 5 | What are Constitutional AI and RLAIF? How do the two phases work, and what are the benefits and risks of AI feedback? |
| B2P05-Q15 | 5 | DPO in more detail: the reference model, beta, the implicit reward, data requirements and known failure modes. |
| B2P05-Q16 | 5 | What do IPO, KTO, ORPO and SimPO change relative to DPO, and when would you consider them? |
| B2P05-Q17 | 5 | How do reward models fail (overfitting, distribution shift, length bias, over-optimisation), and what do ensembles and process reward models offer? |
| B2P05-Q18 | 5 | What is sycophancy? Why does RLHF encourage it, and how do you measure and reduce it? |
| B2P05-Q19 | 5 | What causes length bias and verbosity in aligned models, and how do you measure and mitigate it? |
| B2P05-Q20 | 5 | What are GRPO and RLVR? How does a group-relative advantage replace the critic, and what are the weaknesses of verifiable rewards? |
| B2P05-Q21 | 5 | How are reasoning models post-trained (RL on verifiable tasks, test-time compute), and how does that differ from preference-based RLHF? |
| B2P05-Q22 | 5 | How do you balance helpfulness and harmlessness in safety training? What is the alignment tax and how do you limit it? |
| B2P05-Q23 | 5 | How do you run a red-team exercise (manual vs automated, coverage, attack success rate, fixing what you find)? |
| B2P05-Q24 | 5 | How do safety-classifier guardrails (Llama Guard style) work for inputs and outputs: taxonomy, thresholds, latency and limits? |
| B2P05-Q25 | 5 | What do guardrail frameworks such as NeMo Guardrails provide (self-check rails, dialog flows, third-party integrations), and when would you use a framework instead of custom checks? |
| B2P05-Q26 | 5 | Guardrails vs alignment: what does each handle, why do you need both, and what does defence in depth look like? |
| B2P05-Q27 | 5 | How do you build output-side guardrails for PII, secrets and toxicity (regex, NER, classifier) and what are the trade-offs? |
| B2P05-Q28 | 5 | What do guardrails cost in latency and money, and how do you reduce it (cheap checks first, parallel rails, streaming, caching)? |
| B2P05-Q29 | 5 | How do you measure guardrail quality (precision and recall per category, thresholds, cost of false positives vs false negatives, evaluation set design)? |
| B2P05-Q30 | 5 | Online vs offline preference optimisation: DPO on a fixed dataset, iterative or online DPO, and PPO. Why does on-policy data matter? |
| B2P05-Q31 | 5 | How do you handle annotator disagreement and label noise in preference data (inter-annotator agreement, adjudication, noise-robust training)? |
| B2P05-Q32 | 5 | How do you evaluate a reward model itself (held-out preference accuracy, agreement with humans, best-of-n probes)? |
| B2P05-Q33 | 5 | AI code review: this LLM-written DPO/PPO training snippet has bugs (loss sign, reference model gradients, summed vs averaged log-probabilities, KL direction, missing clipping). Find and fix them. |
| B2P05-Q34 | 5 | Best-of-n with a reward model vs RL fine-tuning: what are the cost, quality and over-optimisation trade-offs? |
| B2P05-Q35 | 5 | Why do jailbreaks work (competing objectives, mismatched generalisation), and what are the main families (role-play, obfuscation, multi-turn, multimodal)? |
| B2P05-Q36 | 5 | Derive DPO from the KL-regularised reward-maximisation objective: the optimal policy, the reward reparameterisation and the final loss. |
| B2P05-Q37 | 5 | Design question: build the post-training pipeline for a coding model (SFT data, preference data from execution tests, RLVR, evaluation, safety). |
| B2P05-Q38 | 5 | Design question: build a preference-data collection platform with quality control (guidelines, redundancy, adjudication, audits, throughput). |
| B2P05-Q39 | 5 | Design question: guardrail architecture for a customer-facing assistant that can issue refunds (rails, approvals, escalation, logging, red-team gates). |
| B2P05-Q40 | 5 | What is scalable oversight, and why does preference-based RLHF struggle on tasks humans cannot easily judge? |
| B2P05-Q41 | 5 | What are the engineering challenges of distributed PPO for LLMs (generation vs training throughput, four models, staleness), and how do teams address them? |
