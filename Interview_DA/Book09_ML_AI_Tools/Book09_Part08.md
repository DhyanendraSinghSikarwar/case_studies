# Book 9 — Basic ML + AI Tools for Analysts | Part 8: Attrition Prediction and Churn Mini-Projects 🟡🔴

**Target:** 30 questions | **Actual:** 33 questions
**Scope:** HR-friendly attrition and churn mini-projects: framing the target, leakage, imbalance, metrics on small confusion matrices, threshold and cost thinking, sklearn/statsmodels snippets, explaining scores to HR, fairness and privacy, and defending a portfolio project.

### Q1 ⭐⭐⭐ 🟢 You are asked to build an attrition prediction model for an HR team from raw HRIS data. Walk me through the steps from the business question to handing the result over.
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 How would you define the target variable for an employee attrition model, and why does it matter whether you include voluntary and involuntary exits together?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Your model gives an employee an attrition risk score of 0.72. How would you explain to an HR head what that number does and does not mean?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Why is accuracy a misleading metric for an attrition model?
Data: 1,000 employees, 150 left in the next 12 months. A model predicts "stays" for everyone. Compute its accuracy, recall for leavers and precision for leavers.
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 Compute precision, recall and F1 for the leaver class and say which one matters more for an HR stay-interview programme.
Data (confusion matrix, leaver = positive): TP = 30, FP = 20, FN = 30, TN = 920.
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 What is data leakage in an attrition model? Name three columns in an HR file that could leak the outcome.
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 What is wrong with this workflow, and how would you fix it?
```python
X_res, y_res = SMOTE().fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
```
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 How do you read a logistic regression coefficient in an attrition model when you explain it to HR?
Data: coefficient for OverTime = Yes is 0.90 (other variables held constant). Use e^0.90 ≈ 2.46. State what the odds ratio means and what it does not mean.
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Leavers are about 15% of your attrition dataset. List the ways you can handle this imbalance and say which you would try first.
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 HR can hold stay-interviews with only 50 employees this quarter. How do you turn the model's scores into that list, and how do you pick the cut-off?
Data: 1,000 employees scored; the top 50 by score contain 20 actual leavers; 150 employees leave in total.
Compute precision at 50 and the share of all leavers captured.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 The model shows that employees with low satisfaction scores are more likely to leave. Can HR conclude that raising satisfaction will cut attrition? Explain.
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 A recruiter says: "I built a churn model on the Telco dataset with 80% accuracy." As the interviewer, what follow-up questions would you ask, and how should a candidate answer them?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐ 🟢 Which features would you engineer for an attrition model beyond the raw columns in an HRIS export? Give four with a reason each.
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟢 How is a customer churn mini-project the same as, and different from, an employee attrition mini-project?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 Would you start with logistic regression or a random forest for an HR attrition model, and why?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 Write the short code to split an attrition dataset into train and test sets and fit a logistic regression, keeping the leaver share equal in both sets.
Data: a pandas DataFrame `df` with numeric features and a 0/1 column `Attrition`.
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 An e-commerce company has no subscriptions. How would you define a churned customer for a churn model?
Data (days between orders for one customer): 12, 20, 15, 30, 18. Suggest an inactivity window and justify it from these gaps.
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 Two attrition models are tested on the same 1,000 employees. Which would you give to HR for stay interviews, and why?
Data: Model A precision 0.50, recall 0.60. Model B precision 0.70, recall 0.30. Total leavers = 150. Compute how many leavers each model catches and how many people each flags.
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 Estimate the net value of an attrition model with the figures below, and state which assumptions the answer depends on.
Data (illustrative): model flags 40 employees, 24 of them are real leavers. A stay interview costs 5,000 per person. It retains 20% of true leavers. Replacing a leaver costs 400,000.
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Should you split attrition data randomly or by time? Explain with an example of what can go wrong with a random split.
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Why would you use stratified k-fold cross-validation for a churn or attrition model?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Write a scikit-learn pipeline that one-hot encodes the categorical columns, scales the numeric columns and fits a class-weighted logistic regression.
Data: `cat_cols = ["Department", "JobRole"]`, `num_cols = ["Age", "MonthlyIncome", "YearsAtCompany"]`.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 A random forest ranks MonthlyIncome as the most important feature for attrition. What cautions would you give before presenting this to HR?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Read this statsmodels output and tell the manager which findings you would act on and which you would treat carefully.
Data (logit, 1,470 rows): OverTime[Yes] coef 1.10, p < 0.001; YearsSinceLastPromotion coef 0.05, p = 0.30; JobSatisfaction coef -0.30, p = 0.002.
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Churn is very rare in a month. How does a customer who joined last month and has not yet cancelled create a labelling problem, and how would you handle it?
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Build a decile lift table by hand: what is the lift of the top decile, and what does it tell the marketing team?
Data: 1,000 customers, 100 churners overall. The top 100 by model score contain 40 churners.
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 The same attrition mini-project idea can predict offer dropouts in a hiring funnel. Describe the target, three features and one risk of that project.
<!-- ANSWER_PENDING -->

### Q28 ⭐ 🟡 Your model's recall for leavers differs by gender. Compute the gap and say how you would handle it before the model is used.
Data: Group A has 50 leavers, model catches 40. Group B has 50 leavers, model catches 20.
<!-- ANSWER_PENDING -->

### Q29 ⭐ 🔴 Should HR use individual attrition risk scores to decide who gets promotions or training? Discuss fairness, consent and privacy, including proxy variables.
<!-- ANSWER_PENDING -->

### Q30 ⭐ 🔴 You removed gender from the features, yet the model's flags still differ by gender. How can that happen and what would you check?
<!-- ANSWER_PENDING -->

### Q31 ⭐ 🔴 A model says 0.30 for a group of 100 similar employees but only 10 of them leave. What does that tell you about calibration, and does it matter for HR?
<!-- ANSWER_PENDING -->

### Q32 ⭐ 🔴 Six months after deployment, attrition jumps after a pay-policy change and the model's precision falls. How would you detect and respond to this drift?
<!-- ANSWER_PENDING -->

### Q33 ⭐ 🔴 A 200-person company has only 12 leavers in three years and wants an attrition model. What do you advise?
<!-- ANSWER_PENDING -->
