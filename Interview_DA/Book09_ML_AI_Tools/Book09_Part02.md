# Book 9 — Basic ML + AI Tools for Analysts | Part 2: Linear and Logistic Regression (Intuition + sklearn) 🟢🟡

**Target:** 85 questions | **Actual:** 84 questions
**Scope:** fitting linear and logistic regression with sklearn/statsmodels, coefficients as an analyst explains them, predicting, odds and probabilities, classification with logistic regression, data preparation, regularisation basics and the prediction-versus-explanation distinction (statistics theory and R-squared are in Book 5).

### Q1 ⭐⭐⭐ 🟢 What is the difference between linear regression and logistic regression?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 When would you use linear regression and when would you use logistic regression? Give one HR example of each.
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Why is logistic regression called a classification algorithm even though its name says regression?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What does the sigmoid (logistic) function do in logistic regression, and what range of values does it output?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 Write the sklearn code to fit a linear regression that predicts salary from years of experience using a pandas DataFrame, and then predict the salary for 6 years of experience.
`df` has columns `experience` (years) and `salary` (rupees per month).
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 After fitting LinearRegression in sklearn, what do `model.coef_` and `model.intercept_` tell you, and what salary does the model predict for 4 years of experience?
`model.coef_ = [3500]`, `model.intercept_ = 18000`; X is years of experience, y is monthly salary in rupees.
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 How would you explain a fitted linear regression model to a non-technical HR manager in two sentences?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 A logistic regression model gives an employee a probability of 0.72 of leaving. What does that number mean, and what class does the model predict at the default threshold?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟢 Why is plain linear regression a poor choice when the outcome is yes/no, such as whether an employee leaves?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟢 What is the difference between `predict()` and `predict_proba()` in sklearn's LogisticRegression?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟢 In an attrition dataset, which columns would you treat as the target and which as features, and why?
Columns: `employee_id`, `age`, `tenure_years`, `overtime_hours`, `department`, `last_hike_pct`, `left_company` (1 = left, 0 = stayed).
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟢 What data preparation steps do you do in pandas before fitting a regression model in sklearn?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How do you interpret a logistic regression coefficient, and what is the odds ratio for a coefficient of 0.7 on the variable `works_overtime`?
Use e^0.7 ≈ 2.01.
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 What does `model.score(X_test, y_test)` return for LinearRegression, and what does it return for LogisticRegression?
```python
model = LinearRegression().fit(X_train, y_train)
print(model.score(X_test, y_test))
```
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 A logistic regression has intercept -2 and a coefficient of 0.5 on `overtime_hours_per_week`. What is the predicted probability of leaving for an employee with 3 overtime hours?
Use p = 1 / (1 + e^(-z)); e^0.5 ≈ 1.6487.
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 How do probability, odds and log-odds relate? Convert a probability of 0.8 to odds, and odds of 1.5 to a probability.
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 How do you handle a categorical variable such as `department` before fitting LinearRegression or LogisticRegression in sklearn?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 Your attrition model predicts 'stayed' for every employee and gets 95% accuracy. Why can that happen, and what would you try in a logistic regression?
Data: 1,000 employees, 950 stayed, 50 left.
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🟡 Do you need to scale the features before fitting linear regression and logistic regression in sklearn?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐⭐ 🟡 How do you choose a classification threshold other than 0.5 for a logistic regression model, and why would you?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐⭐ 🟡 Where is the decision boundary of a logistic regression model, and at what value of x does the model predict a probability of exactly 0.5?
z = -4 + 0.8 × x, where x is overtime hours per week.
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐⭐ 🟡 Using the multiple regression below, what monthly salary does the model predict for an employee with 3 years of experience and 20 training hours?
Intercept = 15,000; coefficient on `experience` = 3,200 per year; coefficient on `training_hours` = 150 per hour.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐⭐ 🟡 What is the difference between building a model to predict and building one to explain, and how does it change what you look at?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐⭐ 🟡 For the fitted line y = 10 + 2x and the data below, calculate the predicted values, the residuals and the sum of squared errors.
x = 1, 2, 3; actual y = 13, 13, 17.
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐⭐ 🟡 Walk through the sklearn steps to build a simple attrition model with logistic regression, from a DataFrame to a prediction for a new employee.
Assume `df` has a numeric target `left_company` and a few numeric features.
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐⭐ 🔴 A logistic regression coefficient says employees with a higher last salary hike are more likely to leave. What do you do before reporting this?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐⭐ 🔴 One of your features is `exit_interview_done`. Your model reaches 99% accuracy. What is the problem, and how do you fix it?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟢 What does the least squares line mean in simple terms, and how does sklearn find it?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟢 What does the intercept mean in a logistic regression model?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟢 Can linear regression predict impossible values such as a negative salary or a probability above 1? Show an example.
Fitted line: attrition_score = -0.1 + 0.15 × overtime_hours. Predict for 0 and for 9 hours.
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟢 For each of the following targets, say whether you would use linear regression or logistic regression, or neither, and why.
(a) monthly salary, (b) left company yes/no, (c) number of leaves taken, (d) days to fill a vacancy, (e) performance rating high/low.
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟢 What does it mean to 'train' or 'fit' a model, and what is the difference between a parameter and a feature?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟢 How does one extreme outlier change a fitted regression line? Use the data below.
x = 1, 2, 3, 4 with y = 2, 4, 6, 8, then add the point x = 5, y = 30. State whether the slope goes up or down and roughly why.
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟢 What does an odds ratio of 1, of 2 and of 0.5 mean in a logistic regression?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟢 Why does 'linear' regression still fit with an x-squared term? What does 'linear' refer to?
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟢 Why does sklearn raise 'Expected 2D array, got 1D array instead' and how do you fix it?
```python
X = df['experience']
LinearRegression().fit(X, y)
```
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟢 How do you plot predicted versus actual values to check a regression model, and what pattern tells you the model is good?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 Why can the intercept of a regression sometimes be meaningless? Give an example.
Model: salary = a + b × age, trained on employees aged 22 to 58.
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 An attrition logistic regression has a coefficient of -0.2 per year of tenure. What is the odds ratio for 5 extra years of tenure?
Use e^-1.0 ≈ 0.368.
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 How would you add a squared term to capture a curved relationship in sklearn?
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 How do you deal with missing values before fitting a regression in sklearn?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 What is regularisation in intuitive terms, and how do Ridge and Lasso differ?
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 What would you conclude if Lasso shrinks the coefficient of a variable exactly to zero?
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 What does `class_weight='balanced'` do in LogisticRegression, and when would you use it?
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 What is the intuition behind how linear regression and logistic regression are fitted (least squares versus maximum likelihood or log loss)?
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 What does the parameter C mean in sklearn's LogisticRegression, and is regularisation applied by default?
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟡 Calculate the odds ratio of leaving for overtime versus no-overtime employees from the table below.
Overtime group: 100 employees, 30 left. No-overtime group: 100 employees, 10 left.
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟡 How does sklearn's LogisticRegression handle a target with three classes, such as three exit reasons?
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🟡 Write the code to predict the probability of leaving for one new employee with a fitted model, and say how you read the output.
Features used in training: `tenure_years`, `overtime_hours`. New employee: 2 years tenure, 10 overtime hours.
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🟡 A manager asks for the top drivers of attrition from your logistic regression. How do you rank the variables fairly?
<!-- ANSWER_PENDING -->

### Q51 ⭐⭐ 🟡 What does a dummy variable coefficient mean in the model below?
salary = 40,000 + 3,000 × experience - 2,500 × department_Sales, with HR as the reference department. Interpret -2,500.
<!-- ANSWER_PENDING -->

### Q52 ⭐⭐ 🟡 Can the test-set R² be negative, and what does it mean if it is?
<!-- ANSWER_PENDING -->

### Q53 ⭐⭐ 🟡 Why would you use `stratify=y` in train_test_split for an attrition dataset?
<!-- ANSWER_PENDING -->

### Q54 ⭐⭐ 🟡 How do you read the coef, std err, P>|z| and confidence interval columns in a statsmodels logistic regression summary?
One row: `overtime  coef 0.70  std err 0.20  z 3.50  P>|z| 0.000  [0.025 0.308  0.975 1.092]`.
<!-- ANSWER_PENDING -->

### Q55 ⭐⭐ 🟡 What is an interaction term, and when would you add one in a regression?
<!-- ANSWER_PENDING -->

### Q56 ⭐⭐ 🟡 Why do we not rely on R² for logistic regression, and what do people use instead?
<!-- ANSWER_PENDING -->

### Q57 ⭐⭐ 🟡 When would you use statsmodels instead of sklearn for a regression, and when sklearn?
<!-- ANSWER_PENDING -->

### Q58 ⭐⭐ 🟡 For which model setting would a false negative be costlier than a false positive, and how would that change your threshold?
Illustrative costs: missing a leaver costs Rs 4,00,000 in rehiring; a wasted retention call costs Rs 2,000. Compute the break-even probability.
<!-- ANSWER_PENDING -->

### Q59 ⭐⭐ 🔴 What is calibration for a logistic regression model, and how would you check that '30% risk' really means about 30 in 100?
<!-- ANSWER_PENDING -->

### Q60 ⭐⭐ 🔴 What is perfect separation in logistic regression, what warning signs do you see, and what do you do?
<!-- ANSWER_PENDING -->

### Q61 ⭐ 🟢 Where can an analyst fit a regression without Python, for example in Excel, and how does that compare with sklearn?
<!-- ANSWER_PENDING -->

### Q62 ⭐ 🟢 What is a baseline model, and why compare your regression against predicting the average?
Illustrative: salaries 30, 40, 50, 60 thousand. What does the mean-only model predict, and what is its RMSE?
<!-- ANSWER_PENDING -->

### Q63 ⭐ 🟢 A model said 0.72 chance of leaving but the employee stayed. Was the model wrong?
<!-- ANSWER_PENDING -->

### Q64 ⭐ 🟢 How is a regression model different from a rule such as 'flag anyone with more than 3 absences' for attrition risk?
<!-- ANSWER_PENDING -->

### Q65 ⭐ 🟡 What is a sklearn Pipeline and why would you use one for regression?
<!-- ANSWER_PENDING -->

### Q66 ⭐ 🟡 What is a linear probability model, and why do analysts still sometimes use it?
<!-- ANSWER_PENDING -->

### Q67 ⭐ 🟡 Why is logistic regression often a good first model in business, including banks and HR teams?
<!-- ANSWER_PENDING -->

### Q68 ⭐ 🟡 For an HR audience, how would you compare logistic regression with a decision tree on interpretability?
<!-- ANSWER_PENDING -->

### Q69 ⭐ 🟡 Should you include gender or age in an attrition or pay regression? Discuss fairness and privacy.
<!-- ANSWER_PENDING -->

### Q70 ⭐ 🟡 If you log-transform salary as the target, how do you turn predictions back into rupees and how does interpretation change?
<!-- ANSWER_PENDING -->

### Q71 ⭐ 🟡 What are influential points and leverage, and how do you spot one in a regression?
<!-- ANSWER_PENDING -->

### Q72 ⭐ 🟡 Why is an odds ratio not the same as a risk ratio, and when does the difference matter?
<!-- ANSWER_PENDING -->

### Q73 ⭐ 🟡 What is gradient descent in one minute, and does LinearRegression in sklearn use it?
<!-- ANSWER_PENDING -->

### Q74 ⭐ 🟡 How would you report a logistic regression to management using predicted probabilities instead of odds ratios?
Illustrative model: baseline probability 10% for no overtime, odds ratio 3.0 for overtime. Compute the probability for overtime employees.
<!-- ANSWER_PENDING -->

### Q75 ⭐ 🟡 What is an elastic net, and when might it beat Ridge or Lasso alone?
<!-- ANSWER_PENDING -->

### Q76 ⭐ 🟡 How do you check a logistic regression model for multicollinearity, and does it matter if you only want predictions?
<!-- ANSWER_PENDING -->

### Q77 ⭐ 🟡 What does `max_iter` do in LogisticRegression, and what does a ConvergenceWarning tell you?
<!-- ANSWER_PENDING -->

### Q78 ⭐ 🔴 What is Poisson regression, and when would you use it for a count target such as leaves taken per employee?
<!-- ANSWER_PENDING -->

### Q79 ⭐ 🔴 What is the difference between a coefficient and a marginal effect (change in probability) in logistic regression, and why does the effect vary by employee?
<!-- ANSWER_PENDING -->

### Q80 ⭐ 🔴 What happens in linear regression when you have more features than rows, and what do you do?
<!-- ANSWER_PENDING -->

### Q81 ⭐ 🔴 How would you detect and handle data leakage caused by time, for example using future information in a churn model?
<!-- ANSWER_PENDING -->

### Q82 ⭐ 🔴 What is the learning rate in gradient-based fitting of logistic regression, and what goes wrong if it is too big?
<!-- ANSWER_PENDING -->

### Q83 ⭐ 🔴 Your logistic regression is accurate on training data but poor on new months. List causes and your first three checks.
<!-- ANSWER_PENDING -->

### Q84 ⭐ 🔴 How would you compare two logistic regression models, one with 5 features and one with 12, to decide which to deploy?
<!-- ANSWER_PENDING -->
