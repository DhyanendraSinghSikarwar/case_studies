# Book 1 — Part 04: Decision Trees, Random Forest, Boosting (XGBoost / LightGBM / CatBoost), Tuning, SHAP

**Topic:** Trees, bagging, boosting, tree-model hyperparameter tuning, feature importance and SHAP
**Target:** 45 questions | **Actual:** 54 (⭐⭐⭐ 15, ⭐⭐ 28, ⭐ 11)
**Date:** 2026-10-20 | **Status:** Questions frozen, answers pending
**Note:** Source vs gap-check marking per question is in research_notes/Book1_Part04_sources.md.

---

### Q1 ⭐⭐⭐ 🟢 How does a decision tree choose where to split? Compare Gini impurity, entropy and information gain.
**Asked at:** Product cos, GCCs, analytics/consulting firms (Amazon, Indian product cos)
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Bagging vs boosting: what is the difference and how does each affect bias and variance?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What are the key hyperparameters of a Random Forest and how does each affect bias/variance?
**Asked at:** Product cos, GCCs, analytics/consulting firms (UHG-type report)
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Why does a Random Forest overfit less than a single decision tree? Explain bootstrap sampling and feature subsampling.
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What is the difference between Random Forest and XGBoost, and when would you pick each?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Intuit, Amazon, Digitas-type, Tredence, Applied Cloud Computing)
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 How do you prevent overfitting in a decision tree? Explain pre-pruning, post-pruning and cost-complexity pruning.
**Asked at:** Product cos, GCCs, analytics/consulting firms (Swiggy-type)
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Explain gradient boosting step by step. Why is it called gradient boosting?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Intuit, interview-prep banks)
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 What makes XGBoost different from classic gradient boosting (GBM)?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 How would you tune XGBoost hyperparameters? Which matter most and in what order?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Walmart)
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Compare XGBoost, LightGBM and CatBoost: speed, categorical handling, growth strategy, when to use which.
**Asked at:** Product cos, GCCs, analytics/consulting firms (Glassdoor-reported XGBoost vs LightGBM)
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 How do you control overfitting in boosting models? Where does early stopping fit in?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Swiggy/Flipkart-type)
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 How is feature importance computed in tree models (split count, gain/impurity, permutation)? What are the pitfalls?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Flipkart-type, Target)
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 What is SHAP? How does it differ from built-in feature importance (global vs local)?
**Asked at:** Product cos, GCCs, analytics/consulting firms, fintech/credit risk (Klarna-type), regulated GCCs
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 How do tree-based models handle missing values, categorical variables, outliers and unscaled features?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Single decision tree vs ensemble (Random Forest / XGBoost): what are the trade-offs?
**Asked at:** Product cos, GCCs, analytics/consulting firms (practice-prompt style)
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 Work through a small table by hand: compute Gini/entropy and pick the best split.
**Asked at:** Product cos, GCCs, analytics/consulting firms, early-career / analytics
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 How does a regression tree split and what does a leaf predict?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 What is out-of-bag (OOB) error in a Random Forest and how is it used?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 How do learning rate and number of trees trade off in boosting?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 AdaBoost vs gradient boosting: how do they differ?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Extra Trees vs Random Forest: what is different and when is Extra Trees better?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Amazon forecasting DS, Sept 2025 report)
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Why is impurity-based (MDI) importance biased, and how does permutation importance help?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 How does permutation importance behave with correlated features? What would you do about it?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 How do you handle imbalanced data in XGBoost / Random Forest (scale_pos_weight, class_weight, sampling, metric)?
**Asked at:** Product cos, GCCs, analytics/consulting firms, fintech/fraud
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Level-wise vs leaf-wise tree growth: what do they mean, and how do num_leaves and max_depth interact in LightGBM?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Grid vs random vs Bayesian (Optuna) search for tree models: which do you choose and how do you cross-validate?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Why can't tree-based models extrapolate, and what do you do when you need to?
**Asked at:** Product cos, GCCs, analytics/consulting firms, forecasting/pricing teams
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How do you read SHAP plots (summary/beeswarm, dependence, waterfall) and what decisions do they support?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 How do you handle high-cardinality categorical features with tree models? Why can one-hot encoding hurt?
**Asked at:** Product cos, GCCs, analytics/consulting firms, e-commerce/fintech
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Are Random Forest / XGBoost probabilities calibrated? How do you fix it?
**Asked at:** Product cos, GCCs, analytics/consulting firms, fintech/risk
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Code: implement a best-split finder (or a small decision tree) from scratch in NumPy.
**Asked at:** Product cos, GCCs, analytics/consulting firms (live coding)
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Code: implement a Random Forest from scratch (bootstrap + feature subsampling + voting).
**Asked at:** Product cos, GCCs, analytics/consulting firms (live coding)
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 AI-era: an LLM generated this XGBoost training pipeline. Review it and find the bugs (leakage, early stopping on test set, encoding, metrics).
**Asked at:** Product cos, GCCs, analytics/consulting firms, AI-assisted code-review rounds
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 Why do GBDTs still often beat deep learning on tabular data? When would you pick a neural net or a tabular foundation model instead?
**Asked at:** Product cos, GCCs, analytics/consulting firms, Europe product cos
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 How do you do feature selection with tree models (importance thresholds, RFE, Boruta) and what can go wrong?
**Asked at:** Product cos, GCCs, analytics/consulting firms (Flipkart MLE guide-type)
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 How would you explain a gradient boosting model's decision to a non-technical stakeholder or regulator?
**Asked at:** Product cos, GCCs, analytics/consulting firms, regulated GCCs, fintech
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 Stacking / blending vs a single Random Forest or GBM: when is an ensemble of ensembles worth it?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 How do you use learning curves and validation curves to diagnose under/overfitting in a boosted model?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🔴 Derive the XGBoost objective: second-order Taylor expansion, optimal leaf weight and the split-gain formula.
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🔴 Code: implement gradient boosting regression from scratch (squared loss) using shallow trees.
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior live coding)
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🔴 How does CatBoost avoid target leakage (ordered target statistics, ordered boosting)?
**Asked at:** Product cos, GCCs, analytics/consulting firms, Europe product cos
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🔴 What are the limitations of SHAP with correlated features? Explain path-dependent vs interventional TreeSHAP.
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🔴 Derive the variance of an average of correlated trees; why does reducing correlation between trees matter?
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior/quant-leaning)
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🟡 How are multi-class problems handled in XGBoost/LightGBM (softmax objective, one tree per class)?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🟡 What does tree depth mean for feature interactions? How do you detect interactions in a GBM?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🟡 What are DART, row subsampling and column subsampling in boosting and why use them?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟡 Why can Random Forest / XGBoost results differ between runs, and how do you make training reproducible?
**Asked at:** Product cos, GCCs, analytics/consulting firms
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🔴 Explain LightGBM's GOSS, EFB and histogram-based splitting.
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 How does XGBoost find splits: exact vs approximate vs hist; what is sparsity-aware split finding?
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 What are monotonic constraints in GBMs and when would you use them (e.g. credit scoring, pricing)?
**Asked at:** Product cos, GCCs, analytics/consulting firms, fintech/regulated
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 How do you write a custom objective in XGBoost/LightGBM (gradient and hessian)? Example: focal or asymmetric loss.
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 How do you get prediction intervals from GBMs (quantile loss, conformal prediction)?
**Asked at:** Product cos, GCCs, analytics/consulting firms (senior)
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 How do you serve tree ensembles in production: latency, model size, ONNX/Treelite, GPU, distributed training?
**Asked at:** Product cos, GCCs, analytics/consulting firms (MLE roles)
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🔴 What is the GBDT + logistic regression approach (leaf-index features) and when is it useful?
**Asked at:** Product cos, GCCs, analytics/consulting firms (ads/ranking teams)
<!-- ANSWER_PENDING -->
