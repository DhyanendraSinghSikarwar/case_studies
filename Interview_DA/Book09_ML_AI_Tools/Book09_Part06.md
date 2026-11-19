# Book 9 — Basic ML + AI Tools for Analysts | Part 6: Overfitting, Train/Test Split, Feature Engineering Basics 🟡

**Target:** 38 questions | **Actual:** 40 questions
**Scope:** overfitting and underfitting, train/validation/test splits and sklearn train_test_split, cross-validation, data leakage, and basic feature engineering (encoding, scaling, missing values, outliers, derived features) for a 0-3 year analyst.

### Q1 ⭐⭐⭐ 🟢 What is overfitting? Explain it with a simple example to a non-technical manager.
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is underfitting, and how is it different from overfitting?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Why do we split data into a training set and a test set instead of evaluating the model on the data it was trained on?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 A model for predicting employee attrition has the scores below. What do they suggest, and what would you try next?
Training accuracy = 0.97, test accuracy = 0.71.
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What is feature engineering? Give three examples of features you could create for an employee attrition dataset.
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 What is data leakage in a machine learning project? Give one HR or sales example.
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Read this code and explain what each argument does. With 1,000 rows, how many rows end up in the training and test sets?
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 What does stratify=y do in train_test_split, and when would you use it? Using the data below, how many leavers are in the test set?
1,000 employees, 80 of whom left (8%). Call: `train_test_split(X, y, test_size=0.25, stratify=y, random_state=1)`.
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 What is the difference between a training set, a validation set and a test set, and why is the test set kept untouched until the end?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Your churn model scores 99% on the test set. What would make you suspicious, and how would you check for leakage?
One of the features is `account_closed_date`, which is empty for customers who are still active.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 What is wrong with this code, and how would you fix it?
```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)
```
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 How do you handle a categorical column such as department or city before fitting a model? Compare one-hot encoding with label encoding.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How would you handle missing values in a feature before modelling, and why should the fill values be calculated from the training data only?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 What practical steps can you take to reduce overfitting in a model you built as an analyst?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Explain the bias-variance trade-off in plain words. Where do an overfit model and an underfit model sit on it?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 What does random_state do in train_test_split, and why does it matter when you share your results with a colleague?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 What is the difference between a feature and a target (label)? Identify both in a model that predicts whether an employee will resign within 6 months.
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 Does adding more features always make a model better? Explain with an example.
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 What is k-fold cross-validation, and why is it preferred over a single train-test split on small datasets? For 5-fold on 500 rows, how many rows are in each training and validation part?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Interpret these 5-fold cross-validation scores. What is the mean, and what does the spread tell you?
Fold accuracies: 0.78, 0.82, 0.80, 0.76, 0.84.
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 A decision tree was trained at several depths. Which depth would you choose, and why?
| max_depth | Train accuracy | Test accuracy |
|---|---|---|
| 2 | 0.78 | 0.76 |
| 5 | 0.88 | 0.82 |
| 10 | 0.99 | 0.74 |
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Why is scaling needed for some models and not others? Standardise a salary of 62,000 when the training mean is 50,000 and the standard deviation is 5,000.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Write pandas code to create a `tenure_months` feature from a `hire_date` column, and explain why this is usually more useful to a model than the raw date.
`df['hire_date']` holds dates as strings such as '2021-04-15'; use 2025-04-30 as the reference date.
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 After one-hot encoding with drop_first=True, how many columns does this dataset have, and why do we drop one dummy column?
Columns: `department` (5 distinct values), `age`, `salary`. Target column excluded.
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 How do you spot and treat outliers in a feature before modelling? Using the IQR rule, what is the upper fence below, and would a salary of 95 be flagged?
Salary in thousands: Q1 = 30, Q3 = 50.
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Only 5% of customers in your churn data actually churn, so a model that predicts 'no churn' for everyone is 95% accurate. What can you do at the data and model level to handle this imbalance?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Why is a random train-test split a problem for data that depends on time, such as monthly sales or monthly attrition snapshots? How would you split instead?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Why use an sklearn Pipeline with a scaler and a model instead of transforming the data manually?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 A model looked good in your notebook but performs poorly after being used on new employee data. List the likely causes.
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 What is regularisation (Ridge and Lasso) in intuitive terms, and how does it help against overfitting?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Two features, `years_at_company` and `age`, have a correlation of 0.95. How would you decide which to keep, and does it matter for prediction versus explanation?
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🔴 Why can fitting an imputer or scaler on the whole dataset before cross-validation inflate the scores, and how does a Pipeline inside cross_val_score fix it?
<!-- ANSWER_PENDING -->

### Q33 ⭐ 🟡 What does a learning curve show, and what does each pattern below suggest?
Case A: training score 0.95 and validation score 0.70, gap stays wide as rows increase. Case B: both scores plateau near 0.65.
<!-- ANSWER_PENDING -->

### Q34 ⭐ 🟡 A salary column is heavily right-skewed. Would you transform it for a model, and how (for example log)? Which models care?
<!-- ANSWER_PENDING -->

### Q35 ⭐ 🟡 What are interaction or ratio features? Create one from `salary` and `grade_midpoint`, and say why it might predict attrition better than salary alone.
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🟡 You want to use gender, age and pincode as features in an attrition or hiring model. What risks would you raise about fairness, proxies and privacy before including them?
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 What is the difference between overfitting, data leakage and train-test distribution shift? Give a one-line example of each.
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🔴 Your attrition data has several monthly rows per employee. Why can a random row-level split leak information, and what would you use instead?
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🔴 You tune hyperparameters repeatedly and report the best score on the same test set. What is wrong, and how would you structure the data to avoid it?
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🔴 What is target (mean) encoding for a high-cardinality column such as pincode, and how can it leak the target if done carelessly?
<!-- ANSWER_PENDING -->
