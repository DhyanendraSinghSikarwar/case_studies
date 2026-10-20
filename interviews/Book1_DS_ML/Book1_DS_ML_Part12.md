# Book 1 — Part 12: NumPy / pandas / sklearn Live-Coding & AI-Code-Review Rounds

**Topic:** pandas wrangling, NumPy vectorization, sklearn Pipelines/CV, leakage bugs, from-scratch metrics, debugging and reviewing LLM-generated ML code (SQL -> Book 3, DSA -> Book 5)
**Target:** 45
**Actual:** 51
**Date:** 2026-10-20

### Q1 ⭐⭐⭐ 🟢 Given a transactions DataFrame (user_id, ts, amount, category), use groupby with named aggregation to get per-user total, mean, count and last-transaction date, then return the top 3 categories by spend for each user.
**Asked at:** Product cos, fintech, GCC; pandas live rounds (Pinterest, Bloomberg, Voleon reports)
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Write code to audit missing values in a DataFrame (count, percent, pattern by group) and impute numeric and categorical columns sensibly. Why must the imputation statistics come from the training split only?
**Asked at:** Product cos, GCC, consulting-style DS (TCS, ION reports)
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Explain and demonstrate .loc vs .iloc vs boolean masking, and fix a SettingWithCopyWarning / chained-assignment bug (df[df.a>0]['b'] = 1). What changes with copy-on-write?
**Asked at:** Product cos, GCC, general pandas rounds
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 Merge a 1M-row orders table with a customers table and the row count unexpectedly grows. Write code to find the cause (duplicate keys), prevent it (validate=, indicator=) and fix it.
**Asked at:** Product cos, e-commerce (Flipkart/Amazon style), GCC
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 This iterrows/apply(axis=1) code takes 10 minutes on 5M rows. Rewrite it vectorized (np.where / np.select / map / merge) and explain why it is faster.
**Asked at:** Product cos, Amazon India, Walmart GCC, startups
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Review this snippet: StandardScaler is fit on the full dataset before train_test_split. Identify the leakage, explain the impact, and rewrite it correctly with a Pipeline.
**Asked at:** Nearly all DS/MLE loops; Flipkart, Swiggy, JPMC GCC, Zalando, Booking
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Build an sklearn Pipeline with ColumnTransformer (median imputer + scaler for numeric; most-frequent imputer + OneHotEncoder(handle_unknown='ignore') for categorical) feeding a classifier, and evaluate it with cross_val_score.
**Asked at:** Product cos, fintech, GCC, Spotify/Zalando-type DS
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Use groupby transform vs agg vs apply: add a column with each row's group mean, z-score within group, and share of group total. When is each the right tool?
**Asked at:** Product cos, GCC, pandas live rounds
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Review this LLM-generated training script for bugs: it applies SMOTE before CV, evaluates on the training set, uses shuffled KFold on time-ordered data and reports accuracy on a 2% positive class. List and fix every issue.
**Asked at:** AI-allowed coding rounds (2026 trend); product cos, fintech
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Create 7-day and 30-day rolling mean/count features per customer from an event log without leaking future information (shift, closed='left', time-based windows).
**Asked at:** Fintech (PhonePe, Klarna), e-commerce, time-aware feature rounds
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Write code for correct cross-validation when rows are grouped (multiple rows per user) or time-ordered: use GroupKFold / TimeSeriesSplit / StratifiedGroupKFold and show how naive KFold inflates the score.
**Asked at:** Product cos, fintech, Booking/Spotify-type loops
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Implement out-of-fold target encoding for a high-cardinality categorical feature in pandas/NumPy, with smoothing, and show why naive target encoding leaks.
**Asked at:** Product cos, fintech, Kaggle-style rounds
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Implement AUC-ROC and average precision from scratch in NumPy (handle tied scores) and verify against sklearn.metrics.
**Asked at:** Product cos, GCC, ML-from-scratch coding rounds
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 A model shows 99% test accuracy. Given this broken notebook (fit_transform on test, duplicated rows across the split, an ID-like feature, a target-derived column), debug it step by step.
**Asked at:** Product cos, Microsoft IDC, GCCs, debug-this-code rounds
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Clean a messy CSV: mixed date formats, numeric columns stored as strings with currency symbols and commas, inconsistent category spellings, duplicates, and impossible values. Show your code and your checks.
**Asked at:** Product cos, GCC, live data-cleaning/take-home (Voleon, Pinterest reports)
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 Write a custom sklearn transformer (BaseEstimator, TransformerMixin) that clips outliers at train-set quantiles and works inside a Pipeline and GridSearchCV. What goes in fit vs transform?
**Asked at:** Product cos, MLE rounds, Zalando/Booking-type teams
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🔴 Compute the pairwise Euclidean distance matrix and k-NN predictions for 10k x 50 data with no Python loops, using broadcasting and the (a-b)^2 expansion. Discuss memory and numerical issues.
**Asked at:** Product cos, Amazon India, MLE rounds
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🔴 Set up hyperparameter tuning with GridSearchCV/RandomizedSearchCV over a Pipeline and explain nested CV. Write code for an unbiased estimate of generalisation performance.
**Asked at:** Product cos, GCC, senior DS
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 Reshape data: pivot_table, melt, stack/unstack and crosstab. Build a monthly cohort retention table from a signup and activity log.
**Asked at:** Product cos, growth/analytics DS (Swiggy, Spotify)
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 Find and drop duplicates keeping the latest record per entity (sort_values + drop_duplicates vs groupby.tail/idxmax) and explain the differences.
**Asked at:** Product cos, GCC, pandas live rounds
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Use pandas window-style operations per group: rank, cumsum, pct_change, lag/lead via shift, expanding and rolling aggregates. Compute 'days since previous order' and 'running spend'.
**Asked at:** Product cos, e-commerce, Amazon India
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Sessionize a clickstream: start a new session when the gap between consecutive events per user exceeds 30 minutes, using groupby, diff and cumsum.
**Asked at:** Swiggy/Flipkart/Spotify-type event data, product cos
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Load a 5 GB CSV on an 8 GB laptop: use dtypes, category, usecols, chunksize, Parquet, and compare with Polars/DuckDB. Show memory before and after.
**Asked at:** Product cos, startups, GCC
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Spot the bug: a function has a mutable default argument (def add_feature(df, cols=[])) and mutates its input DataFrame. Explain the symptom and fix it. Also show list-sharing and in-place mutation pitfalls in ML helper code.
**Asked at:** AI-code-review rounds, MLE loops
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Find the off-by-one / lookahead bug: labels are built with shift(-1) and rolling windows include the current day, so training features see the target. Fix it and add a test.
**Asked at:** Time-series/fintech loops, code-review rounds
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Implement K-fold and stratified K-fold splitting from scratch in NumPy (seeded, no leakage) and check class proportions per fold.
**Asked at:** Product cos, ML-from-scratch rounds
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Implement numerically stable softmax, log-softmax and cross-entropy in NumPy (batch-wise), and show what breaks without the max-subtraction trick.
**Asked at:** Product cos, DL-leaning MLE rounds
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Do feature selection correctly: this code runs SelectKBest on all data and then cross-validates. Show the leakage with random noise features and rewrite with a Pipeline.
**Asked at:** Product cos, healthcare/genomics-style DS, GCC
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Handle class imbalance in code: class_weight vs RandomOverSampler/SMOTE inside an imblearn Pipeline and CV folds, and explain why resampling before the split is wrong.
**Asked at:** Fintech, fraud teams (PhonePe, Klarna)
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Detect and cap outliers per group (IQR, z-score, winsorisation) in pandas and explain how doing it before the split can leak.
**Asked at:** Product cos, GCC
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Make an experiment reproducible: control random_state in splits, models and np.random.default_rng, avoid global-state bugs, and explain why results still differ across machines or with n_jobs.
**Asked at:** MLE rounds, code-review rounds
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Save and load a trained pipeline with joblib, then write an inference function that validates columns, order, dtypes and unseen categories. What breaks in production if you only pickle the model?
**Asked at:** MLE rounds, Microsoft IDC, GCCs
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Join an events table to the most recent price/feature snapshot at or before each event time (merge_asof) without lookahead.
**Asked at:** Fintech, pricing teams, Booking
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 Use cross_validate with multiple scorers, a custom scorer (F-beta or a business-cost metric via make_scorer) and return train and validation scores to diagnose overfitting.
**Asked at:** Product cos, GCC
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 Review LLM-generated pandas code that uses inplace=True, chained indexing, apply(axis=1), a hidden copy and silent dtype coercion. Point out correctness and performance bugs and rewrite it.
**Asked at:** AI-code-review rounds (2026)
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 Compute running mean, variance and moving average in NumPy efficiently (cumsum, convolve, Welford's one-pass algorithm) and discuss catastrophic cancellation.
**Asked at:** MLE rounds, product cos
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 Handle a high-cardinality categorical feature (10k levels) in sklearn: frequency encoding, hashing, OrdinalEncoder with unknown_value, native categorical support in HistGradientBoosting. Write code and compare.
**Asked at:** Product cos, e-commerce
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 Write a data-validation function for incoming scoring data (schema, ranges, null rates, PSI drift vs training) that raises clear errors before the model is called.
**Asked at:** MLE rounds, GCCs, Zalando/Booking-type teams
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🔴 Debug this 'works on my machine' sklearn notebook: results change after reordering columns, a ColumnTransformer silently drops a column (remainder), and get_feature_names_out fails. Fix it.
**Asked at:** MLE rounds, code-review rounds
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🔴 Given an LLM-written function to compute precision@k and NDCG@k, find the off-by-one, ties and empty-group bugs, fix it and write tests with known answers.
**Asked at:** Search/recsys teams, AI-code-review rounds
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🔴 Check for duplicates and near-duplicates across train/test (same user, session, image or text) and write code that splits so no entity appears in both. Quantify the score inflation.
**Asked at:** Product cos, Spotify/Booking-type DS
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🟡 Implement permutation feature importance from scratch in NumPy for any fitted estimator, with repeated shuffles and a held-out set, and compare with sklearn.inspection.
**Asked at:** Product cos, interpretability-minded teams
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🟡 Implement a non-parametric bootstrap confidence interval for a metric (e.g. AUC or median) in vectorised NumPy and state its limitations.
**Asked at:** Product cos, experimentation teams
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🟡 Write pytest unit tests for a data-processing function: pandas.testing.assert_frame_equal, edge cases (empty, all-null, duplicate keys), and a check that the transform never changes row count.
**Asked at:** MLE rounds, GCCs, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🟡 Use sparse matrices in an sklearn pipeline (OneHotEncoder sparse output, TF-IDF + numeric features via ColumnTransformer) and avoid accidentally densifying.
**Asked at:** NLP/search teams, product cos
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🟡 Explain views vs copies, strides and broadcasting rules in NumPy, then fix a bug where modifying a slice silently changes the original array.
**Asked at:** Product cos, MLE rounds
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 Implement groupby-sum/mean/count from scratch in NumPy with np.unique(return_inverse) and np.bincount, then benchmark against pandas.
**Asked at:** Product cos, MLE rounds, senior DS
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🔴 Translate a pandas pipeline to Polars (lazy) or DuckDB and explain when and why you would; what do pandas 2/3 features (Arrow dtypes, copy-on-write) change?
**Asked at:** Product cos, data-platform-minded teams
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 You may use an AI assistant in this round. Walk through how you would prompt it to write a feature pipeline, then verify it: what tests, invariants, leakage checks and baselines do you run before trusting the output?
**Asked at:** AI-allowed interviews (2026 trend per CoderPad survey as reported by PracHub/LeadDev); AI-native startups
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 Review a complete 150-line LLM-generated ML script end to end (train/test handling, CV, metric choice, threshold, seeds, logging, hidden global state) and produce a prioritised list of review comments with fixes.
**Asked at:** AI-allowed code-review rounds, senior DS/MLE
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 Use ColumnTransformer with set_output(transform='pandas'), feature names and custom column selectors to build a pipeline that survives schema evolution, and show how you would test that.
**Asked at:** Senior MLE rounds
<!-- ANSWER_PENDING -->
