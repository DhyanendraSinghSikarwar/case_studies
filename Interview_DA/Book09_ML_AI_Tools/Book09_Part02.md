# Book 9 — Basic ML + AI Tools for Analysts | Part 2: Linear and Logistic Regression (Intuition + sklearn) 🟢🟡

**Target:** 85 questions | **Actual:** 84 questions
**Scope:** fitting linear and logistic regression with sklearn/statsmodels, coefficients as an analyst explains them, predicting, odds and probabilities, classification with logistic regression, data preparation, regularisation basics and the prediction-versus-explanation distinction (statistics theory and R-squared are in Book 5).

### Q1 ⭐⭐⭐ 🟢 What is the difference between linear regression and logistic regression?
**Asked at:** commonly asked (no company-specific report found); prep-site banks and anonymous fresher reports list it (unverified, snippet-level).
**What the interviewer is checking:** Whether you know what each one predicts (a number versus a yes/no probability).
**Say this in the interview:** "Linear regression predicts a number, like salary. Logistic regression predicts the probability of a yes/no outcome, like whether an employee leaves, and we turn that probability into a class using a cut-off."
**Explain simply:**
- The target (the thing you predict) is a continuous number in linear regression, such as monthly salary or days absent.
- The target is a category with two values in logistic regression, such as left (1) or stayed (0).
- Linear regression draws a straight line through the data. Logistic regression bends that line into an S-shape so the output stays between 0 and 1.
- Both are simple, explainable models, which is why analysts use them first.
**Alternative / pitfalls:** Despite the shared word "regression", they are not interchangeable. Using linear regression on a yes/no target gives values below 0 or above 1 (see Q9).
**Likely follow-ups:** 1) *Do both use a straight-line formula?* Yes, both start from a weighted sum of features; logistic then squeezes it through the sigmoid. 2) *Which one for attrition?* Logistic.
**Common mistakes:** Saying logistic regression predicts a number "between 0 and 1" and stopping there, without saying it is a probability used for classification.

### Q2 ⭐⭐⭐ 🟢 When would you use linear regression and when would you use logistic regression? Give one HR example of each.
**Asked at:** commonly asked (no company-specific report found); "when to use classification over regression" is reported for Fractal-type rounds (unverified, snippet-level).
**What the interviewer is checking:** That you choose the model from the type of target, and can give a realistic example.
**Say this in the interview:** "I look at what I am predicting. If it is an amount, like salary for a given experience, I use linear regression. If it is a yes/no, like will this employee resign in 12 months, I use logistic regression."
**Explain simply:**
- Linear example: predict monthly salary from years of experience and grade, so the target is a rupee amount.
- Logistic example: predict whether a new joiner leaves within a year (1 = left, 0 = stayed) from overtime, hike and tenure.
- Rule of thumb: number target means regression; two-category target means classification.
- Features (the input columns) can be numbers in both cases.
**Alternative / pitfalls:** If the target is a count (number of leaves taken) or has more than two classes, other models fit better; mention that you would check, but do not go deep.
**Likely follow-ups:** 1) *Can the same data serve both?* Yes: salary as a number (linear), or "salary above 50,000: yes/no" (logistic), but turning a number into yes/no throws information away. 2) *Which is more useful to a manager?* The one that matches the decision: a budget needs amounts, a retention plan needs a who-is-at-risk list.
**Common mistakes:** Picking by the features instead of the target; using logistic regression for a numeric target.

### Q3 ⭐⭐⭐ 🟢 Why is logistic regression called a classification algorithm even though its name says regression?
**Asked at:** commonly asked (no company-specific report found); listed in several prep-site question banks (unverified).
**What the interviewer is checking:** That you understand the model outputs a probability and a threshold turns it into a class.
**Say this in the interview:** "Inside, it does regression: it estimates a probability, a number. But we use that probability to put each employee in a class, say 'will leave' if it is 0.5 or more, so in practice we use it for classification. The name is historical."
**Explain simply:**
- Step 1: it combines the features into one score, like linear regression does.
- Step 2: the sigmoid function turns that score into a probability between 0 and 1.
- Step 3: a threshold (0.5 by default in sklearn's `predict()`) turns the probability into class 0 or 1.
- The "regression" part is estimating the probability; the "classification" part is the cut-off.
**Alternative / pitfalls:** You can keep the probability and never apply a cut-off, for example to rank employees by risk. That is often more useful than a hard yes/no.
**Likely follow-ups:** 1) *Can you change the 0.5?* Yes (see Q20). 2) *Is it only for two classes?* Basic form is two classes; extensions exist for more.
**Common mistakes:** Saying "it is a regression, so it predicts numbers" or forgetting the threshold step.

### Q4 ⭐⭐⭐ 🟢 What does the sigmoid (logistic) function do in logistic regression, and what range of values does it output?
**Asked at:** commonly asked (no company-specific report found); sigmoid is a standard item in logistic regression question banks (unverified).
**What the interviewer is checking:** That you know it squeezes any number into the range 0 to 1, and can say why that matters.
**Say this in the interview:** "The sigmoid takes any score, from very negative to very positive, and converts it into a value between 0 and 1, so we can read it as a probability. A score of 0 gives exactly 0.5."
**Explain simply:**
- Formula: p = 1 / (1 + e^(-z)), where z is the weighted sum of features and e is about 2.718.
- Big negative z gives p near 0; big positive z gives p near 1; z = 0 gives 0.5.
- The output never reaches exactly 0 or 1, and the curve is S-shaped: it changes fastest around 0.5.
**Code (what you write in the interview):**
```python
import numpy as np

scores = np.array([-6, -2, 0, 2, 6])
probabilities = 1 / (1 + np.exp(-scores))
print(probabilities.round(4))
```
**Output:**
```text
[0.0025 0.1192 0.5    0.8808 0.9975]
```
**What it means:** Whatever the score, the result stays between 0 and 1, and a score of 0 means a coin-flip 50%.
**Likely follow-ups:** 1) *What is z?* The intercept plus each coefficient times its feature value. 2) *Why not just clip a straight line at 0 and 1?* The sigmoid is smooth and gives a proper probability model that can be fitted.
**Common mistakes:** Saying the output is a percentage already (it is a proportion, 0.72 not 72); saying it can exceed 1.

### Q5 ⭐⭐⭐ 🟢 Write the sklearn code to fit a linear regression that predicts salary from years of experience using a pandas DataFrame, and then predict the salary for 6 years of experience.
`df` has columns `experience` (years) and `salary` (rupees per month).
**Asked at:** commonly asked (no company-specific report found); implementation-style questions appear in analyst question banks (unverified).
**What the interviewer is checking:** That you can write fit and predict correctly, including the 2-D shape of X.
**Say this in the interview:** "I put experience in X as a one-column table, salary in y, create LinearRegression, call fit, and then predict on a new one-row table with the same column name."
**Explain simply:**
- Features (X) are the inputs; the label or target (y) is what we predict.
- `X = df[["experience"]]` uses double brackets so X is a table, which sklearn needs, not a single column.
- `fit` learns the line from the data; `predict` applies it to new data.
**Sample data:** six employees (my own illustrative numbers, since the question gives none).

| experience | salary |
|---|---|
| 1 | 25000 |
| 2 | 29000 |
| 3 | 33000 |
| 5 | 40000 |
| 7 | 46000 |
| 10 | 58000 |

**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.DataFrame({
    "experience": [1, 2, 3, 5, 7, 10],
    "salary": [25000, 29000, 33000, 40000, 46000, 58000],
})

# Features go in a table (double brackets), the target in a single column
X = df[["experience"]]
y = df["salary"]

model = LinearRegression()
model.fit(X, y)

# New data must have the same column name as X
new_employee = pd.DataFrame({"experience": [6]})
print(model.predict(new_employee))
print(model.coef_, model.intercept_)
```
**Output:**
```text
[43290.69767442]
[3593.02325581] 21732.558139534885
```
**What it means:** For 6 years of experience the model predicts about Rs 43,291 a month. Each extra year adds about Rs 3,593, starting from about Rs 21,733 at zero years.
**Alternative / pitfalls:** Passing a plain list such as `model.predict([[6]])` also works, but a named DataFrame keeps the column names consistent with training and is safer. Do not predict far outside the 1 to 10 year range you trained on (extrapolation).
**Likely follow-ups:** 1) *Why double brackets?* sklearn wants a 2-D table of features. 2) *Is this prediction exact?* No, it is an estimate; real salaries vary around the line.
**Common mistakes:** `X = df["experience"]` (a 1-D column raises an error); fitting on the whole dataset and calling that the final test (see Q14).

### Q6 ⭐⭐⭐ 🟢 After fitting LinearRegression in sklearn, what do `model.coef_` and `model.intercept_` tell you, and what salary does the model predict for 4 years of experience?
`model.coef_ = [3500]`, `model.intercept_ = 18000`; X is years of experience, y is monthly salary in rupees.
**Asked at:** commonly asked (no company-specific report found); coef_/intercept_ questions appear in sklearn-angle banks (unverified).
**What the interviewer is checking:** That you read the slope and intercept in plain words and can do the arithmetic.
**Say this in the interview:** "The coefficient is the slope: each extra year of experience adds Rs 3,500 a month on average. The intercept is the predicted salary at zero years, Rs 18,000. For 4 years: 18,000 + 3,500 x 4 = Rs 32,000."
**Explain simply:**
- `coef_` is an array with one number per feature; here there is one feature, so one number.
- `intercept_` is where the line crosses the y-axis, the prediction when every feature is 0.
- Prediction = intercept + coefficient x feature value.
**Code (what you write in the interview):**
```python
intercept = 18000
coefficient = 3500
years_of_experience = 4
print(intercept + coefficient * years_of_experience)
```
**Output:**
```text
32000
```
**What it means:** A person with 4 years of experience is predicted to earn Rs 32,000 a month, on average.
**Alternative / pitfalls:** The intercept may not be meaningful on its own (nobody has a real zero-experience profile in some datasets). "Adds Rs 3,500" is an association in this data, not proof that experience causes the pay rise.
**Likely follow-ups:** 1) *What if there are two features?* `coef_` has two numbers, one per feature, in column order. 2) *Units?* Coefficient is rupees per year, the same units as y per unit of X.
**Common mistakes:** Forgetting the intercept (answering 14,000); calling the coefficient a percentage.

### Q7 ⭐⭐⭐ 🟢 How would you explain a fitted linear regression model to a non-technical HR manager in two sentences?
**Asked at:** commonly asked (no company-specific report found); communication of models is a common analyst-round theme (unverified).
**What the interviewer is checking:** Whether you can drop jargon and give a business meaning plus an honest limit.
**Say this in the interview:** "In our data, each extra year of experience goes with about Rs 3,600 more monthly salary, starting from roughly Rs 21,700 for a new joiner. It is an average pattern from past employees, so individual salaries will differ and it should guide, not decide, pay."
**Explain simply:**
- Sentence 1: the pattern in plain units (the slope and the starting point).
- Sentence 2: the limit: it is an average, based on past data, and shows association, not cause.
- Use the numbers from Q5 as the model: slope 3,593 and intercept 21,733, rounded.
- Avoid words like coefficient, residual and R-squared unless asked.
**Alternative / pitfalls:** Add one concrete example ("for 6 years, about Rs 43,300") if the manager seems unsure. Do not say "experience causes higher pay".
**Likely follow-ups:** 1) *How accurate is it?* Report an error size in rupees on test data, not just R-squared. 2) *Can we use it to set offers?* As a reference only; check fairness and context.
**Common mistakes:** Reading out the equation; promising the prediction is exact.

### Q8 ⭐⭐⭐ 🟢 A logistic regression model gives an employee a probability of 0.72 of leaving. What does that number mean, and what class does the model predict at the default threshold?
**Asked at:** commonly asked (no company-specific report found); probability-versus-class questions are standard in logistic regression banks (unverified).
**What the interviewer is checking:** That you read it as a probability and know the default cut-off is 0.5.
**Say this in the interview:** "It means the model estimates a 72% chance that this employee leaves, based on patterns in past employees with similar profiles. Since 0.72 is above the default 0.5 threshold, `predict()` returns class 1, 'will leave'."
**Explain simply:**
- 0.72 is a probability: roughly, among 100 employees who look like this one, about 72 are expected to leave.
- It is not a certainty; 28% is the chance of staying.
- Default threshold is 0.5: 0.5 or more gives class 1, below gives class 0.
- In odds terms: 0.72 / 0.28 is about 2.57 to 1 in favour of leaving.
**Alternative / pitfalls:** The model is only as good as its calibration (whether "72%" really behaves like 72% in practice). Check this before quoting percentages to managers.
**Likely follow-ups:** 1) *Was the model wrong if the person stays?* Not necessarily; a 72% chance still leaves a 28% chance of staying, so about 28 in 100 such employees stay. 2) *Would you act at 0.72?* Depends on cost of a retention conversation versus cost of attrition.
**Common mistakes:** Saying "the employee will leave with 72% certainty" or "72% of the employee's time"; forgetting the threshold can be changed.

### Q9 ⭐⭐⭐ 🟢 Why is plain linear regression a poor choice when the outcome is yes/no, such as whether an employee leaves?
**Asked at:** commonly asked (no company-specific report found); "why not linear for yes/no" is reported in sklearn-angle banks (unverified).
**What the interviewer is checking:** That you know the straight line is not limited to 0 to 1 and the errors do not behave.
**Say this in the interview:** "A straight line keeps going up or down, so it can predict 1.3 or minus 0.2 for a yes/no outcome, which are not valid probabilities. Logistic regression is built to stay between 0 and 1."
**Explain simply:**
- The target only takes values 0 and 1, but a line can output any number, such as 1.3 or -0.2.
- The real relationship usually flattens near 0 and 1 (an S-shape), not a straight line.
- The errors are not spread evenly, which breaks the assumptions behind the usual statistics.
- Linear regression on 0/1 can still rank people roughly, but you cannot trust its numbers as probabilities.
**Alternative / pitfalls:** For a quick rough look, a "linear probability model" is sometimes used by economists, but as an analyst, say logistic is the safer default.
**Likely follow-ups:** 1) *Show it?* See Q30 in this part for an example with impossible values. 2) *What would you use?* Logistic regression.
**Common mistakes:** Saying "linear regression cannot be run on 0/1 data" (it runs, it just gives poor, out-of-range answers).

### Q10 ⭐⭐⭐ 🟢 What is the difference between `predict()` and `predict_proba()` in sklearn's LogisticRegression?
**Asked at:** commonly asked (no company-specific report found); predict versus predict_proba appears in sklearn-angle banks (unverified).
**What the interviewer is checking:** That you know one gives the class and the other gives the probabilities.
**Say this in the interview:** "`predict()` returns the final class, 0 or 1, using the 0.5 cut-off. `predict_proba()` returns the probability of each class, so I can rank employees or choose my own threshold."
**Explain simply:**
- `predict()` gives one label per row (0 = stayed, 1 = left).
- `predict_proba()` gives two columns per row: probability of class 0, then class 1. They add to 1.
- The column order follows `model.classes_`, here `[0 1]`, so column 1 is the chance of leaving.
**Sample data:** twelve employees (illustrative): overtime hours per week and whether they left.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LogisticRegression

employees = pd.DataFrame({
    "overtime_hours": [0, 2, 4, 6, 8, 10, 3, 5, 9, 1, 7, 12],
    "left_company":   [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1],
})
X = employees[["overtime_hours"]]
y = employees["left_company"]
model = LogisticRegression().fit(X, y)

new_employees = pd.DataFrame({"overtime_hours": [5, 11]})
print(model.predict(new_employees))
print(model.predict_proba(new_employees).round(3))
print(model.classes_)
```
**Output:**
```text
[0 1]
[[0.58  0.42 ]
 [0.031 0.969]]
[0 1]
```
**What it means:** At 5 overtime hours the chance of leaving is 42%, so the class is 0 (stay); at 11 hours it is about 97%, so class 1 (leave).
**Alternative / pitfalls:** `predict()` is just `predict_proba()` with a 0.5 cut-off, so to use another threshold, work from `predict_proba()[:, 1]`.
**Likely follow-ups:** 1) *Which column is "leave"?* Column 1, the class labelled 1; check `classes_`. 2) *Do rows sum to 1?* Yes.
**Common mistakes:** Reading the first column as the chance of leaving; using `predict()` and then trying to rank people (it only has two values).

### Q11 ⭐⭐⭐ 🟢 In an attrition dataset, which columns would you treat as the target and which as features, and why?
Columns: `employee_id`, `age`, `tenure_years`, `overtime_hours`, `department`, `last_hike_pct`, `left_company` (1 = left, 0 = stayed).
**Asked at:** commonly asked (no company-specific report found); target-versus-features setup is a basic ML screen question (unverified).
**What the interviewer is checking:** That you separate the outcome from inputs, drop the ID, and think about what is known at prediction time.
**Say this in the interview:** "The target is `left_company`, because that is what we want to predict. Features are age, tenure, overtime, department and last hike. I would leave out `employee_id`, since it is just a label and carries no real pattern."
**Explain simply:**
- Target (label): the outcome, `left_company`, a yes/no.
- Features: `age`, `tenure_years`, `overtime_hours`, `last_hike_pct` (numbers) and `department` (a category that needs encoding, see Q17).
- Drop `employee_id`: it is unique per person, so a model could memorise it without learning anything useful.
- Check each feature is known before the person leaves (no information from after the exit).
**Alternative / pitfalls:** `age` can raise fairness questions; ask HR or legal whether it may be used. Any column created after the exit, such as an exit interview date, is leakage (see Q27).
**Likely follow-ups:** 1) *Is department a number?* No; convert it to 0/1 columns first. 2) *Would you include a salary column?* Yes if it exists, but check for overlap with `last_hike_pct`.
**Common mistakes:** Using `employee_id` as a feature; including a column that only exists after the person has left.

### Q12 ⭐⭐⭐ 🟢 What data preparation steps do you do in pandas before fitting a regression model in sklearn?
**Asked at:** commonly asked (no company-specific report found); data preparation is a core part of analyst ML questions (unverified).
**What the interviewer is checking:** That you know sklearn needs clean, numeric, complete data and a clear X/y split.
**Say this in the interview:** "I remove duplicates, handle missing values, turn text categories into 0/1 columns, drop ID columns, and split into features X and target y. After that I split into train and test sets before fitting."
**Explain simply:**
- Duplicates and obvious errors: remove or fix them.
- Missing values: sklearn's regression models stop with an error on them, so fill (for example with the median) or drop.
- Categories: convert with `pd.get_dummies` (Q17).
- IDs and leaky columns: remove.
- Then train/test split with `random_state=42` so you can check the model on unseen rows.
**Sample data:** six rows with one duplicate and one missing tenure value.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee_id": [1, 2, 2, 3, 4, 5],
    "tenure_years": [2, 5, 5, None, 8, 1],
    "department": ["HR", "IT", "IT", "Sales", "IT", "HR"],
    "left_company": [0, 1, 1, 0, 0, 1],
})

# 1. Remove duplicate rows
employees = employees.drop_duplicates()

# 2. Fill missing numbers (median is safe against outliers)
employees["tenure_years"] = employees["tenure_years"].fillna(employees["tenure_years"].median())

# 3. Turn text categories into 0/1 columns
employees = pd.get_dummies(employees, columns=["department"], drop_first=True, dtype=int)

# 4. Split into features (X) and target (y), leaving the ID out
X = employees.drop(columns=["employee_id", "left_company"])
y = employees["left_company"]
print(X)
```
**Output:**
```text
   tenure_years  department_IT  department_Sales
0           2.0              0                 0
1           5.0              1                 0
3           3.5              0                 1
4           8.0              1                 0
5           1.0              0                 0
```
**What it means:** The duplicate row is gone, the missing tenure became 3.5 (the median of 2, 5, 8 and 1), and department is now numeric.
**Alternative / pitfalls:** Compute the median from the training rows only; filling using the whole dataset leaks test information. Also check that the missing values are not meaningful in themselves.
**Likely follow-ups:** 1) *Why fill rather than drop?* Dropping loses rows; but if very few are missing, dropping is fine. 2) *Do you scale?* Not required for plain regression (Q19).
**Common mistakes:** Leaving text columns in X; leaving `employee_id` in X; doing the preparation after the split inconsistently on train and test.

### Q13 ⭐⭐⭐ 🟡 How do you interpret a logistic regression coefficient, and what is the odds ratio for a coefficient of 0.7 on the variable `works_overtime`?
Use e^0.7 ≈ 2.01.
**Asked at:** commonly asked (no company-specific report found); odds ratio from a coefficient is a staple in logistic regression banks (unverified).
**What the interviewer is checking:** That you convert the coefficient with e^coef and describe it as odds, not probability.
**Say this in the interview:** "The coefficient is a change in log-odds. Exponentiating it gives the odds ratio: e^0.7 is about 2.01, so employees who work overtime have roughly double the odds of leaving, holding the other features fixed."
**Explain simply:**
- Positive coefficient: the feature raises the odds of the outcome; negative lowers them; zero means no effect.
- Odds ratio = e^coefficient. Above 1 means higher odds, below 1 means lower odds.
- `works_overtime` is a yes/no (1/0) variable, so the ratio compares overtime workers with the others.
- Odds are not probability: "2 times the odds" does not mean "2 times the chance".
**Worked example (concept):** If the odds of leaving without overtime are 0.25 (a 20% chance), the odds with overtime are 0.25 x 2.01 = 0.50, which is a 33% chance. So the odds doubled, but the probability went from 20% to 33%, not 40%. (Calculated by hand; e^0.7 = 2.0138.)
**Alternative / pitfalls:** For a numeric feature, the odds ratio is per one-unit increase, for example per extra overtime hour. Feature scale matters when comparing coefficients.
**Likely follow-ups:** 1) *Negative coefficient of -0.7?* Odds ratio 1/2.01 = 0.50, about half the odds. 2) *Is this causal?* No, association only.
**Common mistakes:** Saying "overtime doubles the probability"; reading the raw coefficient as a probability change.

### Q14 ⭐⭐⭐ 🟡 What does `model.score(X_test, y_test)` return for LinearRegression, and what does it return for LogisticRegression?
```python
model = LinearRegression().fit(X_train, y_train)
print(model.score(X_test, y_test))
```
**Asked at:** commonly asked (no company-specific report found); a known sklearn trap, mentioned in implementation-style banks (unverified).
**What the interviewer is checking:** That you know `score` means different metrics for different models.
**Say this in the interview:** "For LinearRegression, `score` returns R-squared on the test data, the share of variation in y that the model explains. For LogisticRegression it returns accuracy, the share of test rows classified correctly."
**Explain simply:**
- Same method name, different meaning, because each sklearn model picks a default metric.
- R-squared: 1 is perfect; 0 means no better than always guessing the average; it can even go negative on test data.
- Accuracy: from 0 to 1; can be misleading when one class is rare (Q18).
- Always compute it on the test set, not the training rows.
**Sample data:** twenty employees (illustrative): overtime hours, whether they left, and salary. With a 30% test split there are only 6 test rows, so the numbers below are noisy and for demonstration only.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split

employees = pd.DataFrame({
    "overtime_hours": [0,1,2,3,4,5,6,7,8,9,10,11,12,2,4,6,8,10,1,5],
    "left_company":   [0,0,0,0,0,1,0,0,1,1,1,1,1,0,0,1,0,1,0,0],
    "salary": [52000,50000,51000,48000,47000,45000,46000,43000,44000,41000,
               40000,42000,38000,49000,48500,44500,43500,41500,50500,46500],
})
X = employees[["overtime_hours"]]

# Linear regression: predict salary, score is R-squared
X_train, X_test, y_train, y_test = train_test_split(X, employees["salary"], test_size=0.3, random_state=42)
print(LinearRegression().fit(X_train, y_train).score(X_test, y_test))

# Logistic regression: predict left_company, score is accuracy
X_train, X_test, y_train, y_test = train_test_split(X, employees["left_company"], test_size=0.3, random_state=42)
print(LogisticRegression().fit(X_train, y_train).score(X_test, y_test))
```
**Output:**
```text
0.9442269618794576
0.5
```
**What it means:** The salary model explains about 94% of the variation in the 6 test salaries; the attrition model got 3 of 6 test employees right (accuracy 0.5). With so few test rows, neither number is reliable.
**Alternative / pitfalls:** For a manager, report an error in rupees (mean absolute error) for linear, and precision and recall for logistic, instead of the bare `score`.
**Likely follow-ups:** 1) *Is accuracy enough for attrition?* No, see Q18. 2) *Can R-squared be negative?* Yes, on test data, when the model is worse than the average.
**Common mistakes:** Assuming `score` is always accuracy; scoring on the training data and reporting that.

### Q15 ⭐⭐⭐ 🟡 A logistic regression has intercept -2 and a coefficient of 0.5 on `overtime_hours_per_week`. What is the predicted probability of leaving for an employee with 3 overtime hours?
Use p = 1 / (1 + e^(-z)); e^0.5 ≈ 1.6487.
**Asked at:** commonly asked (no company-specific report found); hand calculation with the sigmoid is a typical fresher question (unverified).
**What the interviewer is checking:** That you compute z first, then apply the sigmoid correctly.
**Say this in the interview:** "First z = -2 + 0.5 x 3 = -0.5. Then p = 1 / (1 + e^0.5) = 1 / (1 + 1.6487) = about 0.378, so a 37.8% chance of leaving."
**Explain simply:**
- Step 1: z = intercept + coefficient x feature = -2 + 1.5 = -0.5.
- Step 2: e^(-z) = e^0.5 = 1.6487.
- Step 3: p = 1 / 2.6487 = 0.3775.
- Below 0.5, so at the default threshold the class is 0 (stays).
**Code (what you write in the interview):**
```python
import numpy as np

intercept = -2
coefficient = 0.5
overtime_hours = 3

z = intercept + coefficient * overtime_hours
probability = 1 / (1 + np.exp(-z))
print(z, round(probability, 4))
```
**Output:**
```text
-0.5 0.3775
```
**What it means:** This employee has about a 37.8% chance of leaving; at a 0.5 cut-off they are predicted to stay.
**Alternative / pitfalls:** A sign slip is the usual trap: z is -0.5, so the exponent is +0.5 in the denominator.
**Likely follow-ups:** 1) *At what overtime is p = 0.5?* When z = 0: 4 hours (see Q21 for the idea). 2) *At 6 hours?* z = 1, p = 0.731.
**Common mistakes:** Forgetting the intercept; computing e^(-0.5) wrongly or using 1/e instead of 1/(1+e).

### Q16 ⭐⭐⭐ 🟡 How do probability, odds and log-odds relate? Convert a probability of 0.8 to odds, and odds of 1.5 to a probability.
**Asked at:** commonly asked (no company-specific report found); odds and log-odds conversion is standard in logistic regression banks (unverified).
**What the interviewer is checking:** That you know the formulas and can convert both ways.
**Say this in the interview:** "Odds are probability divided by one minus probability; log-odds is the natural log of the odds. So 0.8 gives odds of 0.8 / 0.2 = 4, and odds of 1.5 give a probability of 1.5 / (1 + 1.5) = 0.6."
**Explain simply:**
- Odds = p / (1 - p): "how many times more likely to happen than not". 0.8 means 4 to 1.
- Probability from odds = odds / (1 + odds).
- Log-odds = ln(odds). Logistic regression is a straight-line model on the log-odds scale.
- Log-odds of 0 means odds of 1 and probability of 0.5.
**Code (what you write in the interview):**
```python
import numpy as np

probability = 0.8
odds = probability / (1 - probability)
print(round(odds, 2), round(np.log(odds), 3))

odds = 1.5
probability = odds / (1 + odds)
print(probability, round(np.log(odds), 3))
```
**Output:**
```text
4.0 1.386
0.6 0.405
```
**What it means:** A probability of 0.8 is odds of 4 (log-odds 1.386); odds of 1.5 correspond to a probability of 0.6.
**Alternative / pitfalls:** Odds can go from 0 to infinity, log-odds from minus to plus infinity, which is why a straight line can model log-odds.
**Likely follow-ups:** 1) *Odds of 1?* Probability 0.5. 2) *Why use log-odds?* So the formula can be a normal weighted sum.
**Common mistakes:** Treating odds and probability as the same; dividing by p instead of (1 - p).

### Q17 ⭐⭐⭐ 🟡 How do you handle a categorical variable such as `department` before fitting LinearRegression or LogisticRegression in sklearn?
**Asked at:** commonly asked (no company-specific report found); categorical encoding is a standard analyst-ML question (unverified).
**What the interviewer is checking:** That you know models need numbers, and that you use dummy (one-hot) columns, not 1, 2, 3 codes.
**Say this in the interview:** "I convert it to dummy variables with `pd.get_dummies`: one 0/1 column per department, dropping one as the reference group to avoid duplication. I would not just label HR as 1, IT as 2, Sales as 3, because that invents an order."
**Explain simply:**
- Dummy variable: a 0/1 column that says "is this employee in IT?".
- `drop_first=True` drops one category (here HR) so the remaining columns are read against it. Without that, the columns add up to 1 and repeat the intercept's job (the "dummy variable trap").
- Coefficients are then differences from the dropped group, other features held fixed.
**Sample data:** twelve employees (illustrative) with overtime, department and whether they left.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LogisticRegression

employees = pd.DataFrame({
    "overtime_hours": [2, 8, 10, 1, 9, 3, 12, 4, 7, 0, 11, 5],
    "department": ["HR","Sales","Sales","IT","Sales","HR","IT","IT","HR","HR","Sales","IT"],
    "left_company": [0,1,1,0,1,0,1,0,0,0,1,1],
})

# One 0/1 column per department; drop_first removes the redundant one
X = pd.get_dummies(employees[["overtime_hours", "department"]],
                   columns=["department"], drop_first=True, dtype=int)
print(X.head(4))

model = LogisticRegression().fit(X, employees["left_company"])
print(pd.Series(model.coef_[0], index=X.columns).round(2))
```
**Output:**
```text
   overtime_hours  department_IT  department_Sales
0               2              0                 0
1               8              0                 1
2              10              0                 1
3               1              1                 0
overtime_hours      0.74
department_IT       0.41
department_Sales    0.33
dtype: float64
```
**What it means:** HR is the reference group (both department columns are 0). The IT and Sales coefficients are their log-odds difference from HR; with only 12 rows these are illustrative, not findings.
**Alternative / pitfalls:** `OneHotEncoder` inside a pipeline does the same job and is safer when new data may contain unseen departments. Sklearn's LogisticRegression applies mild regularisation by default, so coefficients are slightly shrunk.
**Likely follow-ups:** 1) *Why not 1, 2, 3?* The model would treat Sales as three times HR. 2) *Many categories?* Group rare ones or use another approach.
**Common mistakes:** Label-encoding nominal categories; forgetting to apply the same dummy columns to new data.

### Q18 ⭐⭐⭐ 🟡 Your attrition model predicts 'stayed' for every employee and gets 95% accuracy. Why can that happen, and what would you try in a logistic regression?
Data: 1,000 employees, 950 stayed, 50 left.
**Asked at:** commonly asked (no company-specific report found); the accuracy trap and class_weight are reported in ML banks (unverified).
**What the interviewer is checking:** That you recognise class imbalance and know accuracy is the wrong yardstick here.
**Say this in the interview:** "Only 5% of employees left, so always guessing 'stayed' is right 95% of the time while catching zero leavers. I would look at recall and precision, try `class_weight='balanced'`, and choose a threshold to suit the business."
**Explain simply:**
- Class imbalance: one outcome (stayed) is far more common than the other (left).
- Accuracy = correct predictions / all predictions, so it rewards ignoring the rare class.
- Recall = of the people who really left, how many did we catch? Precision = of those we flagged, how many really left?
- `class_weight='balanced'` makes mistakes on the rare class count more during fitting. Other options: lower the threshold (Q20), collect more leaver data.
**Sample data:** simulated 1,000 employees (950 stayed, 50 left) where leavers work more overtime; 30% held out as test (300 rows, 15 leavers).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Simulated data: 1,000 employees, 50 left, leavers work more overtime
rng = np.random.default_rng(42)
left_company = np.array([0] * 950 + [1] * 50)
overtime_hours = np.where(left_company == 1, rng.normal(9, 3, 1000), rng.normal(5, 3, 1000)).clip(0)
X = pd.DataFrame({"overtime_hours": overtime_hours})
y = pd.Series(left_company)

# stratify keeps the same 5% leavers in train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

for weight in [None, "balanced"]:
    model = LogisticRegression(class_weight=weight).fit(X_train, y_train)
    predicted = model.predict(X_test)
    print(weight,
          "accuracy", round(accuracy_score(y_test, predicted), 3),
          "recall", round(recall_score(y_test, predicted), 3),
          "precision", round(precision_score(y_test, predicted), 3))
```
**Output:**
```text
None accuracy 0.957 recall 0.2 precision 0.75
balanced accuracy 0.813 recall 0.733 precision 0.175
```
**What it means:** The plain model has high accuracy but catches only 20% of leavers. The balanced model catches 73% of leavers, at the cost of flagging many stayers (precision 0.175) and lower accuracy. Report recall and precision, not accuracy; the right balance depends on what a retention conversation costs. (Output depends on the simulated data and seed 42; the all-"stayed" baseline is exactly 0.95.)
**Alternative / pitfalls:** Always compare with the all-"stayed" baseline of 95%. Never use accuracy alone on an imbalanced target; do not rebalance the test set.
**Likely follow-ups:** 1) *Why stratify?* So train and test keep the same share of leavers. 2) *What number to give the manager?* "We catch about 7 in 10 leavers, but only about 1 in 6 flagged people actually leaves."
**Common mistakes:** Celebrating 95% accuracy; judging the model on training data.

### Q19 ⭐⭐⭐ 🟡 Do you need to scale the features before fitting linear regression and logistic regression in sklearn?
**Asked at:** commonly asked (no company-specific report found); scaling questions appear in ML question banks (unverified).
**What the interviewer is checking:** That you know plain linear regression does not need scaling, but regularised models and coefficient comparison do.
**Say this in the interview:** "For plain LinearRegression, no: the predictions are the same either way. For LogisticRegression, sklearn applies regularisation by default, which is sensitive to feature scale, so scaling is a good idea, and it also makes coefficients comparable."
**Explain simply:**
- Scaling means putting features on a similar range, for example `StandardScaler` (subtract the mean, divide by the standard deviation).
- Ordinary least squares: scaling changes the coefficients' size but not the predictions.
- Regularisation (a penalty that keeps coefficients small) treats big-scale features like salary differently from small ones like years, so scale first. LogisticRegression regularises by default (`C=1.0`).
- After scaling, a coefficient means "per one standard deviation", so it is no longer "per year" or "per rupee".
**Sample data:** the six employees from Q5.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

employees = pd.DataFrame({
    "experience": [1, 2, 3, 5, 7, 10],
    "salary": [25000, 29000, 33000, 40000, 46000, 58000],
})
new_employee = pd.DataFrame({"experience": [6]})

# Without scaling
plain_model = LinearRegression().fit(employees[["experience"]], employees["salary"])
print(plain_model.predict(new_employee), plain_model.coef_)

# With scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(employees[["experience"]])
scaled_model = LinearRegression().fit(X_scaled, employees["salary"])
print(scaled_model.predict(scaler.transform(new_employee)), scaled_model.coef_)
```
**Output:**
```text
[43290.69767442] [3593.02325581]
[43290.69767442] [11106.77563995]
```
**What it means:** The prediction is identical (about Rs 43,291). Only the coefficient changed, from Rs 3,593 per year to Rs 11,107 per standard deviation of experience.
**Alternative / pitfalls:** Fit the scaler on the training data only and reuse it on test data, otherwise information leaks. In a Pipeline this happens automatically. Tree models do not need scaling.
**Likely follow-ups:** 1) *Why scale for logistic?* The regularisation penalty depends on coefficient size, so feature scale affects the fit. 2) *Do dummy 0/1 columns need scaling?* Usually not.
**Common mistakes:** Saying "always scale" or "never scale"; scaling before the train/test split using all rows.

### Q20 ⭐⭐⭐ 🟡 How do you choose a classification threshold other than 0.5 for a logistic regression model, and why would you?
**Asked at:** commonly asked (no company-specific report found); threshold choice is listed in imbalance-related banks (unverified).
**What the interviewer is checking:** That you tie the threshold to business cost and use `predict_proba`, not the default.
**Say this in the interview:** "0.5 is just a default. I take the predicted probabilities, try several thresholds, and look at precision and recall at each. I pick the one that fits the cost: if missing a leaver is costly, I lower the threshold to catch more of them."
**Explain simply:**
- Lower threshold: flag more people, catch more real leavers (higher recall) but more false alarms (lower precision).
- Higher threshold: flag fewer, more certain people (higher precision) but miss more leavers.
- Why change it: with a rare outcome the model rarely reaches 0.5, so few people get flagged.
- Choose using a validation set, not the data used to fit, and tie it to capacity (for example HR can hold 50 retention conversations).
**Sample data:** simulated 400 employees, about 15% leave, with leavers working more overtime. (Thresholds are shown on the training data for brevity; in practice use a separate validation set.)
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

# Simulated data: 400 employees, about 15% leave
rng = np.random.default_rng(42)
left_company = (rng.random(400) < 0.15).astype(int)
overtime_hours = np.where(left_company == 1, rng.normal(9, 3, 400), rng.normal(5, 3, 400)).clip(0)
X = pd.DataFrame({"overtime_hours": overtime_hours})
y = pd.Series(left_company)

model = LogisticRegression().fit(X, y)
probability_of_leaving = model.predict_proba(X)[:, 1]

for threshold in [0.5, 0.3, 0.2]:
    flagged = (probability_of_leaving >= threshold).astype(int)
    print("threshold", threshold,
          "flagged", flagged.sum(),
          "precision", round(precision_score(y, flagged), 2),
          "recall", round(recall_score(y, flagged), 2))
print("actual leavers:", y.sum())
```
**Output:**
```text
threshold 0.5 flagged 25 precision 0.68 recall 0.25
threshold 0.3 flagged 75 precision 0.47 recall 0.51
threshold 0.2 flagged 116 precision 0.41 recall 0.71
actual leavers: 68
```
**What it means:** At 0.5 we flag only 25 people and catch a quarter of the 68 leavers. At 0.2 we flag 116 and catch 71%, but only 41% of those flagged really leave. Tell the manager the trade-off and let cost decide. (Output depends on the simulated data and seed 42.)
**Alternative / pitfalls:** A precision-recall curve (`precision_recall_curve`) shows all thresholds at once. Thresholds are a business choice, not a statistical one.
**Likely follow-ups:** 1) *Does changing the threshold change the model?* No, same probabilities, different cut-off. 2) *How to pick?* Compare cost of a missed leaver with cost of an unnecessary retention conversation.
**Common mistakes:** Tuning the threshold on the test set; sticking to 0.5 without thinking.

### Q21 ⭐⭐⭐ 🟡 Where is the decision boundary of a logistic regression model, and at what value of x does the model predict a probability of exactly 0.5?
z = -4 + 0.8 × x, where x is overtime hours per week.
**Asked at:** commonly asked (no company-specific report found); decision boundary is a standard logistic regression concept question (unverified).
**What the interviewer is checking:** That you know the boundary is where z = 0 (probability 0.5) and can solve for x.
**Say this in the interview:** "The boundary is where the probability is 0.5, which is where z = 0. So -4 + 0.8x = 0, which gives x = 5 hours. Above 5 overtime hours the model predicts 'leave', below 5 'stay', at the default threshold."
**Explain simply:**
- Sigmoid of 0 is 0.5, so the boundary is where the score z is exactly 0.
- Solve: 0.8x = 4, so x = 4 / 0.8 = 5.
- With one feature the boundary is a single point; with two it is a line; with more it is a flat surface.
- If the threshold is not 0.5, the boundary moves (for a 0.3 threshold, solve z = ln(0.3 / 0.7) instead of 0).
**Code (what you write in the interview):**
```python
import numpy as np

for overtime_hours in [3, 5, 7]:
    z = -4 + 0.8 * overtime_hours
    probability = 1 / (1 + np.exp(-z))
    print(overtime_hours, round(z, 2), round(probability, 3))
```
**Output:**
```text
3 -1.6 0.168
5 0.0 0.5
7 1.6 0.832
```
**What it means:** At 5 overtime hours the model is exactly undecided (0.5); at 3 hours there is a 17% chance of leaving and at 7 hours 83%.
**Alternative / pitfalls:** In general the boundary is x = -intercept / coefficient, here 4 / 0.8 = 5. The boundary only separates predictions; real employees near it are close calls.
**Likely follow-ups:** 1) *What if the coefficient were negative?* The classes flip sides of the boundary. 2) *Is the boundary a straight line?* Yes for plain logistic regression with the original features.
**Common mistakes:** Solving for probability = 0 or 1 instead of 0.5; losing the sign of the intercept.

### Q22 ⭐⭐⭐ 🟡 Using the multiple regression below, what monthly salary does the model predict for an employee with 3 years of experience and 20 training hours?
Intercept = 15,000; coefficient on `experience` = 3,200 per year; coefficient on `training_hours` = 150 per hour.
**Asked at:** commonly asked (no company-specific report found); "predict from a fitted equation" is a standard fresher-level regression task in prep-site question banks (unverified).
**What the interviewer is checking:** That you can read a regression equation and plug values in without mixing up the intercept and the coefficients.
**Say this in the interview:** "A multiple regression is just an equation: intercept plus each coefficient times its value. So 15,000 + 3,200 x 3 + 150 x 20 = 27,600 a month."
**Explain simply:**
- The intercept (15,000) is the prediction when every feature is 0.
- Each coefficient says how much the prediction moves for one extra unit of that feature, holding the other features fixed.
- Experience adds 3,200 x 3 = 9,600; training adds 150 x 20 = 3,000; 15,000 + 9,600 + 3,000 = 27,600.
**Code (what you write in the interview):**
```python
# Plug the values into the model equation
intercept = 15000
experience_years = 3
training_hours = 20

predicted_salary = intercept + 3200 * experience_years + 150 * training_hours
print(predicted_salary)
```
**Output:**
```text
27600
```
**What it means:** The model predicts a monthly salary of 27,600 for this profile. It is an average expectation, not a promise for one person.
**Alternative / pitfalls:** With a fitted sklearn model you would call `model.predict(new_row)` instead of typing the equation. Do not predict far outside the experience range the model was trained on.
**Likely follow-ups:** 1) *What if training hours rise by 10?* Salary rises by 150 x 10 = 1,500, other things equal. 2) *Is 150 per hour a cause?* Not necessarily; it is an association in the data.
**Common mistakes:** Forgetting the intercept; multiplying the coefficients together instead of by the feature values; mixing yearly and monthly units.

### Q23 ⭐⭐⭐ 🟡 What is the difference between building a model to predict and building one to explain, and how does it change what you look at?
**Asked at:** commonly asked (no company-specific report found); a standard "prediction vs inference" conceptual question in prep-site banks (unverified).
**What the interviewer is checking:** Whether you know that the goal decides which numbers matter.
**Say this in the interview:** "If I want to predict, I care about accuracy on new data. If I want to explain, I care about what each variable does, so I look at coefficients, their uncertainty and whether the story makes sense. Often I need both, but I say which one the manager really wants."
**Explain simply:**
- Predict: the aim is good guesses for people the model has not seen (for example, who is likely to leave next quarter). You look at test-set performance (error, accuracy, precision and recall) and ignore whether each variable is "meaningful".
- Explain: the aim is to understand drivers (for example, does overtime go with attrition after allowing for tenure?). You look at coefficient signs and sizes, confidence intervals, and whether variables overlap with each other.
- A model can predict well and explain badly (a black box), or explain neatly and predict poorly.
- Explaining carefully still gives associations, not proof of cause.
**Worked example:** An HR head asks "who will leave?" (predict): you rank employees by risk and report test recall. She then asks "why?" (explain): you report that overtime hours have an odds ratio above 1 and tenure below 1, with intervals, and note these are patterns, not proven causes.
**Alternative / pitfalls:** Chasing a tiny accuracy gain with a complicated model can make it impossible to explain to HR; chasing "significant" coefficients on a model that fails on new data is just as bad.
**Likely follow-ups:** 1) *Which tool for each?* Often sklearn for prediction, statsmodels for explanation (see Q57). 2) *Does a high R-squared mean you explained attrition?* No.
**Common mistakes:** Reading predictive feature importance as cause; reporting only training accuracy; not asking what the decision is.

### Q24 ⭐⭐⭐ 🟡 For the fitted line y = 10 + 2x and the data below, calculate the predicted values, the residuals and the sum of squared errors.
x = 1, 2, 3; actual y = 13, 13, 17.
**Asked at:** commonly asked (no company-specific report found); small hand-calculation tasks like this are common in regression question banks (unverified).
**What the interviewer is checking:** That you know a residual is actual minus predicted, and that the sum of squared errors is the thing least squares tries to make small.
**Say this in the interview:** "Predictions are 12, 14, 16. Residuals, actual minus predicted, are 1, -1 and 1. Squared they are 1, 1, 1, so the sum of squared errors is 3."
**Explain simply:**
- Predicted value: put each x into 10 + 2x (x=1 gives 12, x=2 gives 14, x=3 gives 16).
- Residual: how far off the prediction is, actual minus predicted. Positive means the model guessed too low.
- Squaring removes the sign (so misses do not cancel out) and punishes big misses more.
- Sum of squared errors (SSE): add up the squared residuals. Smaller means the line fits the points better.
**Sample data:**

| x | actual y | predicted | residual | squared |
|---|---|---|---|---|
| 1 | 13 | 12 | 1 | 1 |
| 2 | 13 | 14 | -1 | 1 |
| 3 | 17 | 16 | 1 | 1 |

**Code (what you write in the interview):**
```python
import numpy as np

x = np.array([1, 2, 3])
actual_y = np.array([13, 13, 17])

# Predictions from the fitted line y = 10 + 2x
predicted_y = 10 + 2 * x

# Residual = actual minus predicted
residuals = actual_y - predicted_y

# Sum of squared errors
sse = (residuals ** 2).sum()

print("Predicted:", predicted_y)
print("Residuals:", residuals)
print("SSE:", sse)
```
**Output:**
```text
Predicted: [12 14 16]
Residuals: [ 1 -1  1]
SSE: 3
```
**What it means:** The line misses each point by 1 unit and its total squared error is 3. A better line would have a smaller SSE (see Q28, where the least squares line reaches 2.67).
**Likely follow-ups:** 1) *Why square?* So positives and negatives do not cancel, and large errors count more. 2) *Do residuals add to zero?* For the true least squares line they do; for this line they sum to 1, which hints it is not the best line.
**Common mistakes:** Predicted minus actual (sign flips); forgetting to square before adding; averaging instead of summing.

### Q25 ⭐⭐⭐ 🟡 Walk through the sklearn steps to build a simple attrition model with logistic regression, from a DataFrame to a prediction for a new employee.
Assume `df` has a numeric target `left_company` and a few numeric features.
**Asked at:** commonly asked (no company-specific report found); implementation questions for analyst roles appear in prep-site banks (unverified).
**What the interviewer is checking:** That you know the standard workflow: features and target, split, fit, evaluate, predict, and that you keep test data unseen.
**Say this in the interview:** "I split the DataFrame into features X and target y, hold out a test set, fit LogisticRegression on the training part, check accuracy and better metrics on the test part, then call predict_proba on a one-row DataFrame for the new employee."
**Explain simply:**
- Features (X) are the input columns; the target (y) is what we want to predict (1 = left, 0 = stayed).
- Fit means letting the model learn its coefficients from the training rows.
- The test set is a hidden slice used only to check the model on people it has not seen.
- `stratify=y` keeps the same share of leavers in both slices (see Q53).
- predict gives the class (0 or 1); predict_proba gives the probability of leaving.
**Sample data:** 20 made-up employees with `tenure_years`, `overtime_hours` and `left_company` (built inside the code below).
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Small made-up attrition data
df = pd.DataFrame({
    'tenure_years':    [0.5, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 1, 2, 0.8, 3.5, 9, 1.2, 6, 2.5, 0.6, 5],
    'overtime_hours':  [12, 10, 9, 8, 2, 3, 1, 0, 2, 1, 11, 7, 14, 4, 0, 9, 3, 6, 13, 2],
    'left_company':    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0],
})

# Step 1: split into features (inputs) and target (what we predict)
X = df[['tenure_years', 'overtime_hours']]
y = df['left_company']

# Step 2: hold back a test set to check the model on unseen people
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

# Step 3: fit the model on the training data only
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 4: check accuracy on the test set
print("Test accuracy:", round(accuracy_score(y_test, model.predict(X_test)), 2))

# Step 5: predict for a new employee (1 year tenure, 10 overtime hours)
new_employee = pd.DataFrame({'tenure_years': [1], 'overtime_hours': [10]})
print("Predicted class:", model.predict(new_employee)[0])
print("Probability of leaving:", model.predict_proba(new_employee)[0, 1].round(3))
```
**Output:** (random_state=42)
```text
Test accuracy: 0.67
Predicted class: 1
Probability of leaving: 0.907
```
**What it means:** The model gives this new employee about a 91% chance of leaving, so it predicts class 1 (leaves). The test accuracy of 0.67 comes from only 6 test rows, so it is shaky; with real data you would use far more rows and also check precision and recall.
**Alternative / pitfalls:** Accuracy alone can mislead when few people leave (Q18). Fitting the model on all rows before splitting leaks information.
**Likely follow-ups:** 1) *Why a one-row DataFrame?* sklearn expects a table with the same column names as training. 2) *Why not accuracy only?* Class imbalance (Q18).
**Common mistakes:** Fitting on the test set; passing a plain list instead of a 2D table; including columns that are only known after the person leaves (Q27).

### Q26 ⭐⭐⭐ 🔴 A logistic regression coefficient says employees with a higher last salary hike are more likely to leave. What do you do before reporting this?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question in this book written to test judgement, not a sourced company report.
**What the interviewer is checking:** That you do not report a surprising sign blindly; you look for data issues, confounding and reverse causation.
**Say this in the interview:** "I would not report it yet. A positive hike coefficient is counter-intuitive, so I would check the data, check who gets hikes, and test whether it holds after controlling for performance, tenure and role. It may be that hikes were given to people already at risk, in which case the hike is a symptom, not a cause."
**Explain simply:**
- Check the data first: units (percent or rupees), missing values, outliers, and that the hike is not recorded after the person resigned (that would be leakage, see Q27).
- Think about who gets large hikes: top performers (who also get poached) or people given a counter-offer to stop them leaving. Performance is then a hidden third factor (a confounder).
- Reverse causation: managers may give a hike because they fear the person will leave, so risk causes the hike, not the other way round.
- Check stability: add performance rating, tenure and role to the model; look at the confidence interval; compare leaving rates by hike band.
- Report as an association with caveats; do not tell HR that "hikes cause people to leave".
**Worked example:** Suppose 100 people got a hike above 10% and 30 left (30%), while 100 got a smaller hike and 10 left (10%). A model sees "bigger hike, more leaving". But if the big hikes were mostly counter-offers to people who had already resigned, the hike did not cause the exit. (Illustrative numbers, not real data.)
**Alternative / pitfalls:** Compare against what you know of the policy by asking HR how hikes are decided; a quick split by performance band often reveals the confounder.
**Likely follow-ups:** 1) *Could the model still be useful for prediction?* Yes, if the hike was known before the decision to leave; but explain it carefully. 2) *How do you prove cause?* Only with an experiment or a careful causal design, not with this coefficient alone.
**Common mistakes:** Telling HR to cut hikes; ignoring timing of the variable; trusting one coefficient without checking its interval.

### Q27 ⭐⭐⭐ 🔴 One of your features is `exit_interview_done`. Your model reaches 99% accuracy. What is the problem, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question on data leakage, not a sourced company report.
**What the interviewer is checking:** That you recognise data leakage: a feature that would not be known at prediction time.
**Say this in the interview:** "That is leakage. An exit interview only happens after someone has decided to leave, so the feature gives away the answer. I would drop it, refit, and expect a lower but honest accuracy."
**Explain simply:**
- Leakage means the model sees information that, in real use, would not exist yet. It looks brilliant in testing and fails when deployed.
- Ask for every feature: "would I know this on the day I make the prediction?" For `exit_interview_done` the answer is no.
- Fix: remove the feature (and any similar ones, such as final settlement date or notice period served), rebuild the dataset as of a past date, and rerun.
- A suspiciously perfect score (99%) is itself a warning sign.
**Sample data:** 500 illustrative employees, about a third leave; only leavers have an exit interview, so `exit_interview_done` equals the answer (built inside the code).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Illustrative data: 500 employees, about a third leave, leavers work more overtime
rng = np.random.default_rng(42)
left_company = (rng.random(500) < 0.33).astype(int)
employees = pd.DataFrame({
    "overtime_hours": np.where(left_company == 1, rng.normal(10, 4, 500), rng.normal(7, 4, 500)),
    "tenure_years": rng.uniform(0, 10, 500),
    # Leak: the exit interview only happens after someone has left
    "exit_interview_done": left_company,
})

for features in (["overtime_hours", "tenure_years", "exit_interview_done"],
                 ["overtime_hours", "tenure_years"]):
    X_train, X_test, y_train, y_test = train_test_split(
        employees[features], left_company, test_size=0.3, random_state=42, stratify=left_company)
    model = LogisticRegression().fit(X_train, y_train)
    print(len(features), "features | test accuracy:", round(model.score(X_test, y_test), 2),
          "| largest coefficient:", round(np.abs(model.coef_[0]).max(), 1))
print("Always-'stayed' baseline accuracy:", round(1 - left_company.mean(), 2))
```
**Output:** (seed 42; simulated data)
```text
3 features | test accuracy: 1.0 | largest coefficient: 6.3
2 features | test accuracy: 0.69 | largest coefficient: 0.1
Always-'stayed' baseline accuracy: 0.65
```
**What it means:** With the leaking column the model is perfect (1.0) and that one coefficient is huge (6.3). Without it, accuracy drops to 0.69, only a little above the 0.65 you get by always guessing "stayed", which is the honest picture of what overtime and tenure can do here.
**Alternative / pitfalls:** Other common leaks: using the full data to scale or impute before splitting, features recorded after the outcome, and duplicates across train and test.
**Likely follow-ups:** 1) *How do you spot leakage?* Near-perfect score, one dominant coefficient, or a feature that is only filled for one class. 2) *How do you prevent it?* Define the prediction date and use only data available before it.
**Common mistakes:** Celebrating 99%; dropping the feature but keeping its close relatives; checking only accuracy.

### Q28 ⭐⭐ 🟢 What does the least squares line mean in simple terms, and how does sklearn find it?
**Asked at:** commonly asked (no company-specific report found); appears in prep-site regression question banks (unverified).
**What the interviewer is checking:** That you know "best fit" means smallest total squared miss, and that you can say it without heavy maths.
**Say this in the interview:** "It is the straight line that makes the total of the squared gaps between the actual points and the line as small as possible. sklearn's LinearRegression finds it directly with a formula (linear algebra), no guessing needed."
**Explain simply:**
- Draw any line through the points; each point is some distance above or below it (the residual, see Q24).
- Square each distance and add them up: the sum of squared errors (SSE).
- The least squares line is the one line with the smallest SSE. No other straight line does better.
- sklearn solves this exactly using a matrix formula; you only call `fit`. (Other tools can reach the same line by repeated small improvements, called gradient descent.)
**Sample data:** Same three points as Q24: x = 1, 2, 3 and y = 13, 13, 17.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

# Three employees: x = years of experience, y = actual value from Q24
data = pd.DataFrame({'x': [1, 2, 3], 'y': [13, 13, 17]})

# Fit the least squares line
model = LinearRegression()
model.fit(data[['x']], data['y'])

# Sum of squared errors for the fitted line
residuals = data['y'] - model.predict(data[['x']])
sse = (residuals ** 2).sum()

print("Intercept:", round(model.intercept_, 2))
print("Slope:", round(model.coef_[0], 2))
print("SSE:", round(sse, 2))
```
**Output:**
```text
Intercept: 10.33
Slope: 2.0
SSE: 2.67
```
**What it means:** The best line is y = 10.33 + 2x, with a total squared error of 2.67, lower than the 3 from the rough line y = 10 + 2x in Q24.
**Likely follow-ups:** 1) *Why not minimise absolute errors?* Squares are easier to solve exactly and are standard, but they react strongly to outliers (Q32). 2) *Is the line always the truth?* No, it is the best straight-line summary of the sample.
**Common mistakes:** Saying it minimises the number of points missed; thinking the line must pass through the points; forgetting that it needs a straight-line pattern.

### Q29 ⭐⭐ 🟢 What does the intercept mean in a logistic regression model?
**Asked at:** commonly asked (no company-specific report found); an intercept/coefficient meaning question in prep-site banks (unverified).
**What the interviewer is checking:** That you know the intercept is on the log-odds scale and is the baseline when all features are zero.
**Say this in the interview:** "The intercept is the log-odds of the outcome when every feature is zero. I convert it to a probability to explain it, but it is only meaningful if zero is a realistic value for the features."
**Explain simply:**
- Logistic regression works on log-odds (the log of the odds; odds = chance of leaving divided by chance of staying).
- Intercept = starting log-odds before any feature adds or subtracts anything.
- To read it: probability = 1 / (1 + e^(-intercept)).
- If zero is not realistic (zero tenure and zero salary, say), the intercept is just an adjustment, not something to present.
**Worked example:** An intercept of -2 means a baseline log-odds of -2, which is a probability of 1 / (1 + e^2) = 0.119, about 12% chance of leaving for someone with all features at 0 (for example 0 overtime hours, if features are overtime and tenure measured from 0).
**Code (what you write in the interview):**
```python
import numpy as np

intercept = -2
# With every feature at 0 the model's log-odds equal the intercept
log_odds = intercept
probability = 1 / (1 + np.exp(-log_odds))
print(round(probability, 3))
```
**Output:**
```text
0.119
```
**What it means:** The baseline chance of leaving is about 12% when all features are zero.
**Alternative / pitfalls:** If you centre features (subtract the average), the intercept becomes the log-odds for an average employee, which is easier to explain. With `class_weight='balanced'` the intercept shifts too.
**Likely follow-ups:** 1) *Can the intercept be negative?* Yes, it simply means a baseline probability below 50%. 2) *Is it the overall attrition rate?* Not unless all features are zero or centred.
**Common mistakes:** Reading the intercept as a probability directly; presenting it when zero is impossible.

### Q30 ⭐⭐ 🟢 Can linear regression predict impossible values such as a negative salary or a probability above 1? Show an example.
Fitted line: attrition_score = -0.1 + 0.15 × overtime_hours. Predict for 0 and for 9 hours.
**Asked at:** commonly asked (no company-specific report found); the "why not linear regression for yes/no" idea appears in many prep-site banks (unverified).
**What the interviewer is checking:** That you understand a straight line has no ceiling or floor, so it can leave the 0 to 1 range.
**Say this in the interview:** "Yes. A straight line keeps going. At 0 overtime this line predicts -0.1, and at 9 hours it predicts 1.25. A probability cannot be negative or above 1, which is why we use logistic regression for yes/no outcomes."
**Explain simply:**
- Linear regression adds up terms with no limits, so the prediction can be any number.
- For a probability (0 to 1), this gives nonsense like -0.1 or 1.25.
- The same happens with salary: a line fitted to young employees can predict a negative salary far outside the data.
- Logistic regression squeezes the answer through the sigmoid so it always stays between 0 and 1.
**Code (what you write in the interview):**
```python
# Fitted line from the question
def attrition_score(overtime_hours):
    return -0.1 + 0.15 * overtime_hours

print(round(attrition_score(0), 2))
print(round(attrition_score(9), 2))
```
**Output:**
```text
-0.1
1.25
```
**What it means:** The model gives a "probability" of -10% at 0 hours and 125% at 9 hours, both impossible. Use logistic regression instead.
**Alternative / pitfalls:** You could clip predictions to 0 and 1, but that hides the problem and the line is still a poor fit for a yes/no outcome.
**Likely follow-ups:** 1) *Does this make linear regression wrong for salary?* No, salary is a number; just stay within the data range. 2) *At what hours does the score reach 1?* 7.33 hours (1.1 / 0.15).
**Common mistakes:** Treating the score as a valid probability; extrapolating beyond the data.

### Q31 ⭐⭐ 🟢 For each of the following targets, say whether you would use linear regression or logistic regression, or neither, and why.
(a) monthly salary, (b) left company yes/no, (c) number of leaves taken, (d) days to fill a vacancy, (e) performance rating high/low.
**Asked at:** commonly asked (no company-specific report found); "when to use classification over regression" is a reported theme in aggregator snippets (unverified).
**What the interviewer is checking:** That you match the model to the type of outcome: a number, a two-way category, or a count.
**Say this in the interview:** "Salary and days to fill are numbers, so linear regression. Left yes/no and high/low rating are two categories, so logistic regression. Number of leaves is a count, which linear regression can approximate, but a count model (Poisson) is the proper tool."
**Explain simply:**
- (a) Monthly salary: continuous number, so linear regression.
- (b) Left company yes/no: two categories, so logistic regression.
- (c) Number of leaves taken: whole-number counts that cannot go below 0. Linear regression is a rough fit; a count model such as Poisson regression is better (from memory, unverified for the library details, but the principle is standard). If the counts are large and well spread, a linear model is often acceptable for a quick analysis.
- (d) Days to fill a vacancy: a positive number, so linear regression; if it is very skewed, consider modelling the log of the days.
- (e) Performance rating high/low: two categories, so logistic regression. (If the rating had three or more ordered levels, you would need a multi-class or ordinal model.)
**Alternative / pitfalls:** Check what the outcome really is. A 1 to 5 rating treated as a number is a judgement call; and time-to-event questions (how long until someone leaves) need survival methods rather than either model.
**Likely follow-ups:** 1) *What about three exit reasons?* Multi-class logistic regression (Q48). 2) *Can you code a yes/no as 0 and 1 and use linear regression?* You can, but predictions can fall outside 0 to 1 (Q30).
**Common mistakes:** Calling a model "regression" and assuming it predicts numbers; forcing counts or ordered ratings into the wrong model without saying so.

### Q32 ⭐⭐ 🟢 How does one extreme outlier change a fitted regression line? Use the data below.
x = 1, 2, 3, 4 with y = 2, 4, 6, 8, then add the point x = 5, y = 30. State whether the slope goes up or down and roughly why.
**Asked at:** commonly asked (no company-specific report found); outlier sensitivity of regression is a common concept check (unverified).
**What the interviewer is checking:** That you know least squares is pulled hard by extreme points, and can show it with numbers.
**Say this in the interview:** "The slope goes up. Without the outlier the line is perfect with slope 2. With the point (5, 30) the slope jumps to 6, because squaring a huge miss makes the line tilt toward that point to reduce it."
**Explain simply:**
- The original four points lie exactly on y = 2x, so slope 2 and intercept 0.
- The new point sits far above where the line would put it (it would predict 10, but the actual is 30).
- Least squares squares errors, so one huge miss dominates, and the line tilts up to reduce it.
- A point at the far end of x (high leverage) has the most pull.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

hours = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [2, 4, 6, 8]})
with_outlier = pd.concat([hours, pd.DataFrame({'x': [5], 'y': [30]})], ignore_index=True)

before = LinearRegression().fit(hours[['x']], hours['y'])
after = LinearRegression().fit(with_outlier[['x']], with_outlier['y'])

print("Before: slope", round(before.coef_[0], 2), "intercept", round(before.intercept_, 2))
print("After:  slope", round(after.coef_[0], 2), "intercept", round(after.intercept_, 2))
```
**Output:**
```text
Before: slope 2.0 intercept 0.0
After:  slope 6.0 intercept -8.0
```
**What it means:** One point out of five tripled the slope (2 to 6) and moved the intercept from 0 to -8, so the line no longer describes the other four points well.
**Alternative / pitfalls:** First check whether the point is a typo (for example a payroll entry with an extra zero). If it is real, report results with and without it, or use a method less sensitive to outliers (from memory, unverified: robust or quantile regression).
**Likely follow-ups:** 1) *Do you delete it?* Only with a reason; investigate first. 2) *Would the intercept move too?* Yes, as shown (0 to -8).
**Common mistakes:** Deleting outliers just because they hurt the fit; not checking for data-entry errors.

### Q33 ⭐⭐ 🟢 What does an odds ratio of 1, of 2 and of 0.5 mean in a logistic regression?
**Asked at:** commonly asked (no company-specific report found); odds ratio interpretation is in nearly every logistic regression question bank (unverified).
**What the interviewer is checking:** That you can read an odds ratio as a multiplier on the odds, not as a probability.
**Say this in the interview:** "The odds ratio is the factor the odds of the outcome are multiplied by when the variable goes up by one unit. 1 means no effect, 2 means the odds double, 0.5 means the odds are halved."
**Explain simply:**
- Odds = chance of leaving divided by chance of staying (a 20% chance is odds of 0.25).
- Odds ratio = e raised to the coefficient. A coefficient of 0 gives an odds ratio of 1.
- Above 1: more likely to leave. Below 1: less likely. Exactly 1: no association.
- It is about odds, not probability, so "double the odds" does not mean "double the chance".
**Worked example:** Start with a 20% chance of leaving (odds 0.25). Odds ratio 1 keeps odds at 0.25 (chance 20%). Odds ratio 2 makes the odds 0.5, which is a chance of 0.5 / 1.5 = 33.3%. Odds ratio 0.5 makes the odds 0.125, a chance of 0.125 / 1.125 = 11.1%.
**Alternative / pitfalls:** When the outcome is rare, the odds ratio is close to the risk ratio; when it is common, they differ a lot.
**Likely follow-ups:** 1) *How do you get it from sklearn?* `np.exp(model.coef_)`. 2) *What odds ratio goes with a coefficient of -0.69?* About 0.5.
**Common mistakes:** Saying "twice as likely" for an odds ratio of 2; forgetting it applies per one unit of the variable.

### Q34 ⭐⭐ 🟢 Why does 'linear' regression still fit with an x-squared term? What does 'linear' refer to?
**Asked at:** commonly asked (no company-specific report found); a standard conceptual check in regression banks (unverified).
**What the interviewer is checking:** That "linear" means linear in the coefficients, not a straight line in x.
**Say this in the interview:** "Linear means the prediction is built by adding up coefficients times features. If I create a column x squared, the model is still a sum of coefficient times column, so it is still linear regression, and it can draw a curve."
**Explain simply:**
- The model is: intercept + b1 x column1 + b2 x column2. The coefficients b1 and b2 are only multiplied and added.
- A new column `age_squared` is just another column to the model; it does not know it came from age.
- The result is a curved line in age, but a straight (linear) relationship in the columns the model sees.
- Useful when the effect flattens or bends, such as salary against age.
**Sample data:** 8 made-up employees, salary in thousands, rising with age then flattening.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

# Made-up data: pay rises with age at first, then flattens
employees = pd.DataFrame({'age': [22, 26, 30, 34, 38, 42, 46, 50],
                          'salary': [30, 42, 52, 59, 63, 65, 65.5, 65]})

# Add the squared term as an ordinary new column
employees['age_squared'] = employees['age'] ** 2

X = employees[['age', 'age_squared']]
model = LinearRegression().fit(X, employees['salary'])

print("Coefficients (age, age_squared):", model.coef_.round(3))
print("Intercept:", round(model.intercept_, 2))
print("R-squared:", round(model.score(X, employees['salary']), 3))
```
**Output:**
```text
Coefficients (age, age_squared): [ 6.256 -0.07 ]
Intercept: -73.25
R-squared: 0.998
```
**What it means:** The negative squared coefficient bends the line downward, so pay rises quickly then levels off. The fit is very close (R-squared 0.998), though on 8 made-up points that is not a real result.
**Alternative / pitfalls:** Too many powers can overfit (Q40). Do not predict far outside the age range.
**Likely follow-ups:** 1) *Is logistic regression linear?* Linear in log-odds. 2) *Can you also use log of x?* Yes, same idea.
**Common mistakes:** Thinking "linear" means the plot must be a straight line; interpreting `age` and `age_squared` coefficients separately.

### Q35 ⭐⭐ 🟢 Why does sklearn raise 'Expected 2D array, got 1D array instead' and how do you fix it?
```python
X = df['experience']
LinearRegression().fit(X, y)
```
**Asked at:** commonly asked (no company-specific report found); one of the most common beginner sklearn errors.
**What the interviewer is checking:** That you know sklearn wants features as a table (rows by columns), even for one feature.
**Say this in the interview:** "`df['experience']` is a single column, a 1D Series. sklearn expects a 2D table of rows and feature columns. The fix is double brackets, `df[['experience']]`, which keeps it as a one-column table."
**Explain simply:**
- sklearn needs X shaped as (number of rows, number of features). One feature still needs a second dimension of size 1.
- Single brackets give a Series (1D); double brackets give a DataFrame (2D).
- With a NumPy array the fix is `X.reshape(-1, 1)`.
- y can stay 1D.
- Wording of the message depends on the input and the sklearn version: with a NumPy array on the installed version (1.9.1) it reads "Expected 2D array, got 1D array instead"; with a pandas Series it reads "Expected a 2-dimensional container but got pandas.Series instead".
**Sample data:** 4 employees with `experience` (years) and `salary`.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.DataFrame({'experience': [1, 2, 3, 4], 'salary': [30, 35, 41, 44]})
y = df['salary']

# Double square brackets keep X as a table (2D): rows by columns
X = df[['experience']]
model = LinearRegression().fit(X, y)
print(model.coef_)
```
**Output:**
```text
[4.8]
```
**What it means:** The error is gone and the model learns that each extra year adds about 4.8 (thousand) to salary.
**Alternative / pitfalls:** `df['experience'].values.reshape(-1, 1)` also works. For prediction, use the same shape: `model.predict(pd.DataFrame({'experience': [6]}))`.
**Likely follow-ups:** 1) *Why does sklearn insist on 2D?* It is built for several features, so one feature is just a table with one column. 2) *What does -1 in reshape mean?* "Work out this size for me".
**Common mistakes:** Using single brackets for X; reshaping y instead of X; predicting with a bare number instead of a table.

### Q36 ⭐⭐ 🟢 How do you fit a multiple linear regression in sklearn with several feature columns, and where do you find each coefficient?
```python
features = ['experience', 'training_hours', 'age']
```
**Asked at:** commonly asked (no company-specific report found); sklearn `coef_` and `intercept_` questions appear in implementation banks (unverified).
**What the interviewer is checking:** That you can select several columns, fit, and match each coefficient to its feature name.
**Say this in the interview:** "I put the feature columns in X, the salary in y, fit LinearRegression, then read `model.coef_`, which lists one number per feature in the same order as the columns, plus `model.intercept_`."
**Explain simply:**
- `df[features]` gives a table with all feature columns, which is already the 2D shape sklearn wants.
- `coef_` is an array in the same order as your feature list; zip them with the names so you do not mix them up.
- Each coefficient is the change in salary for one more unit of that feature, holding the others fixed.
- If features move together (age and experience), individual coefficients become unstable and can even show an odd sign.
**Sample data:** 8 made-up employees (built in the code); salary in thousands.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

employees = pd.DataFrame({
    'experience':     [1, 2, 3, 5, 6, 8, 10, 12],
    'training_hours': [10, 25, 15, 30, 20, 40, 35, 45],
    'age':            [23, 25, 28, 30, 33, 35, 40, 44],
    'salary':         [32, 38, 42, 55, 56, 70, 75, 88],
})

features = ['experience', 'training_hours', 'age']
X = employees[features]
y = employees['salary']

model = LinearRegression()
model.fit(X, y)

# Pair each feature name with its coefficient
for name, coefficient in zip(features, model.coef_):
    print(name, round(coefficient, 2))
print("intercept", round(model.intercept_, 2))
```
**Output:**
```text
experience 5.62
training_hours 0.19
age -0.63
intercept 39.03
```
**What it means:** Each extra year of experience goes with about 5.6 more salary units, other things equal. The negative age coefficient is odd; age and experience move together here, so that coefficient is not reliable (the data is tiny and made up).
**Alternative / pitfalls:** `pd.Series(model.coef_, index=features)` gives a labelled result in one line. Use statsmodels if you need p-values and intervals (Q57).
**Likely follow-ups:** 1) *Do coefficients depend on units?* Yes; compare after scaling (Q19, Q50). 2) *What if two features are almost the same?* Drop one or combine them.
**Common mistakes:** Reading `coef_` without matching names; comparing coefficient sizes across different units.

### Q37 ⭐⭐ 🟢 How do you plot predicted versus actual values to check a regression model, and what pattern tells you the model is good?
**Asked at:** commonly asked (no company-specific report found); a diagnostic-plot question seen in regression practice banks (unverified).
**What the interviewer is checking:** That you evaluate on test data and know what a good scatter looks like.
**Say this in the interview:** "I scatter actual values on one axis and predicted on the other for the test set, and draw the 45-degree line. Points tightly around the line mean good predictions. A curve, a fan shape or a few far-off points show problems."
**Explain simply:**
- Each dot is one employee: actual salary across, predicted salary up.
- A perfect model puts every dot on the diagonal line (predicted = actual).
- Good: dots close to the line, evenly above and below, across the whole range.
- Bad: dots bending away in a curve (needs a curved term, Q40), spreading wider at high values, or clearly above or below at one end (the model is biased there).
- Use test data, since training data always looks better.
**Sample data:** 12 made-up employees (experience in years, salary in thousands), split with `random_state=42`.
**Code (what you write in the interview):**
```python
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

employees = pd.DataFrame({
    'experience': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'salary':     [31, 36, 40, 47, 49, 56, 58, 66, 67, 75, 76, 84],
})
X = employees[['experience']]
y = employees['salary']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

model = LinearRegression().fit(X_train, y_train)
predicted = model.predict(X_test)

# Points near the diagonal line mean good predictions
plt.scatter(y_test, predicted)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='grey')
plt.xlabel('Actual salary')
plt.ylabel('Predicted salary')
plt.show()

print("Test R-squared:", round(model.score(X_test, y_test), 3))
```
**Output:** (the plot shows the 4 test points hugging the grey diagonal; the figure itself is not reproduced here)
```text
Test R-squared: 0.987
```
**What it means:** The points sit very close to the diagonal and the test R-squared is 0.987, so on this made-up data the line predicts well. With only 4 test points, do not oversell it to a manager; say the sample is small.
**Alternative / pitfalls:** A residual plot (residual against predicted) shows the same story: you want a random cloud around zero with no pattern.
**Likely follow-ups:** 1) *Why test data?* Training data flatters the model. 2) *Is high R-squared enough?* No, look at the pattern too.
**Common mistakes:** Plotting only training data; swapping axes (harmless but confusing); forgetting the reference line.

### Q38 ⭐⭐ 🟡 Why can the intercept of a regression sometimes be meaningless? Give an example.
Model: salary = a + b × age, trained on employees aged 22 to 58.
**Asked at:** commonly asked (no company-specific report found); a common interpretation check (unverified).
**What the interviewer is checking:** That you notice the intercept refers to x = 0, which may be outside the data.
**Say this in the interview:** "The intercept is the prediction when age is 0. Our employees are 22 to 58, so age 0 is far outside the data and the number has no real-world meaning. It is just where the line crosses the axis."
**Explain simply:**
- Intercept = prediction when every feature is zero.
- If zero is not a realistic or observed value (age 0, tenure 0 with no one at 0, height 0), predicting there is extrapolation, so the intercept is only a mathematical anchor.
- It can look odd, even negative, and that is fine; the slope is what matters for interpretation.
- Fix for readability: centre the variable (use age minus 40) so the intercept becomes the salary at age 40.
**Worked example:** Five made-up employees aged 22, 30, 40, 50 and 58 earn 47,000, 55,000, 68,000, 80,000 and 89,000 a month. The fitted line (checked with `np.polyfit`) has a slope of about 1,186 per year of age and an intercept of about 20,347. The 20,347 is the "salary at age 0", which is nonsense; "about 1,186 more per year of age" is useful. After centring (age minus 40) the intercept becomes about 67,800, the predicted salary at age 40, which is a sensible number.
**Alternative / pitfalls:** The intercept still matters for correct predictions; never drop it from the equation. If x = 0 is meaningful (zero overtime hours), the intercept is interpretable.
**Likely follow-ups:** 1) *Should you remove the intercept?* No, that forces the line through zero and usually distorts the fit. 2) *How do you get a meaningful one?* Centre the variable.
**Common mistakes:** Presenting "salary at age 0" in a report; predicting outside the training range.

### Q39 ⭐⭐ 🟡 An attrition logistic regression has a coefficient of -0.2 per year of tenure. What is the odds ratio for 5 extra years of tenure?
Use e^-1.0 ≈ 0.368.
**Asked at:** commonly asked (no company-specific report found); odds-ratio calculation tasks are common in logistic regression banks (unverified).
**What the interviewer is checking:** That you multiply the coefficient by the number of years before exponentiating.
**Say this in the interview:** "Five years is 5 times -0.2, which is -1.0 on the log-odds scale. The odds ratio is e^-1.0, about 0.368. So five extra years of tenure cut the odds of leaving to about 37% of what they were, a reduction of about 63%."
**Explain simply:**
- Coefficients add up on the log-odds scale: 5 years x -0.2 = -1.0.
- Exponentiate to turn log-odds into an odds ratio: e^-1.0 = 0.368.
- Equivalent check: the one-year odds ratio is e^-0.2 = 0.819, and 0.819^5 = 0.368 (odds ratios multiply).
- An odds ratio below 1 means lower odds of leaving.
**Code (what you write in the interview):**
```python
import numpy as np

coefficient_per_year = -0.2
extra_years = 5

# Log-odds change over 5 years, then convert to an odds ratio
log_odds_change = coefficient_per_year * extra_years
odds_ratio = np.exp(log_odds_change)
print(round(log_odds_change, 2), round(odds_ratio, 3))
```
**Output:**
```text
-1.0 0.368
```
**What it means:** The odds of leaving are about 37% as high for someone with 5 more years of tenure, other factors held equal. That is odds, not probability.
**Alternative / pitfalls:** Do not compute e^-0.2 x 5 (that gives 4.09 which is wrong); multiply first, then exponentiate. This is a linear effect on log-odds, assumed the same across the whole tenure range.
**Likely follow-ups:** 1) *Is it a 63% drop in probability?* No, in odds. 2) *What if the coefficient were +0.2?* Odds ratio e^1.0 = 2.72 for 5 years.
**Common mistakes:** Exponentiating then multiplying by 5; saying "37% less likely" instead of "odds are 37% of before".

### Q40 ⭐⭐ 🟡 How would you add a squared term to capture a curved relationship in sklearn?
**Asked at:** commonly asked (no company-specific report found); polynomial features appear in implementation banks (unverified).
**What the interviewer is checking:** That you know a squared term is just an extra column, and that you can build it with pandas or `PolynomialFeatures`.
**Say this in the interview:** "I add a column x squared, either directly in pandas or with sklearn's PolynomialFeatures, and fit the same LinearRegression. I compare test performance with the straight line so I do not overfit."
**Explain simply:**
- Why: if the effect bends (salary rises with age then flattens), a straight line misses it.
- How: new column = x squared; fit linear regression on x and x squared together (see Q34 for why this is still "linear").
- `PolynomialFeatures(degree=2, include_bias=False)` builds the extra column(s) for you; `include_bias=False` avoids adding a constant column since the model already has an intercept.
- Keep the degree low (2 or 3); high degrees chase noise.
**Sample data:** Same 8 made-up age and salary rows as Q34.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

employees = pd.DataFrame({'age': [22, 26, 30, 34, 38, 42, 46, 50],
                          'salary': [30, 42, 52, 59, 63, 65, 65.5, 65]})
X = employees[['age']]
y = employees['salary']

# Straight line for comparison
straight_line = LinearRegression().fit(X, y)

# Add age squared as a new column, then fit as usual
X_curved = PolynomialFeatures(degree=2, include_bias=False).fit_transform(X)
curved_line = LinearRegression().fit(X_curved, y)

print("Straight line R-squared:", round(straight_line.score(X, y), 3))
print("Curved R-squared:", round(curved_line.score(X_curved, y), 3))
```
**Output:**
```text
Straight line R-squared: 0.82
Curved R-squared: 0.998
```
**What it means:** The curved model explains almost all the variation (0.998 against 0.82) because the pattern genuinely bends. These are training-set scores on 8 points; check on test data before trusting it.
**Alternative / pitfalls:** The simple pandas way is `employees['age_squared'] = employees['age'] ** 2`. Squared terms can be wild outside the data range, and with age they may predict falling pay at very high ages.
**Likely follow-ups:** 1) *How do you decide the degree?* Compare test error. 2) *Does scaling matter?* Large powers get huge; scaling or centring helps.
**Common mistakes:** Adding the square but dropping the original `age`; using a high degree; judging by training R-squared only.

### Q41 ⭐⭐ 🟡 How do you deal with missing values before fitting a regression in sklearn?
**Asked at:** commonly asked (no company-specific report found); data preparation is a recurring theme in analyst banks (unverified).
**What the interviewer is checking:** That you know sklearn's LinearRegression and LogisticRegression will not accept missing values, and that you choose a sensible, leak-free fix.
**Say this in the interview:** "First I check how many are missing and why. Then I either drop rows if very few, or fill them, for example with the median using SimpleImputer, learned from the training data only. I may also add a flag column saying the value was missing."
**Explain simply:**
- These sklearn models raise an error on NaN (blank) values, so you must deal with them first.
- Drop rows: fine when few are missing and missing at random; otherwise you lose data or bias it.
- Fill (impute): median for skewed numbers like salary, mean for symmetric, most frequent for categories.
- Fit the imputer on training data only, then apply it to test data, so test information does not leak in.
- Ask why it is missing: a blank "last hike" may mean "never got one", which is information.
**Sample data:** 8 made-up employees with one blank experience and one blank training_hours.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression

employees = pd.DataFrame({
    'experience': [1, 2, 3, None, 6, 8, 10, 12],
    'training_hours': [10, 25, None, 30, 20, 40, 35, 45],
    'salary': [32, 38, 42, 55, 56, 70, 75, 88],
})
print(employees.isna().sum())

X = employees[['experience', 'training_hours']]
y = employees['salary']

# Fill gaps with the median of each column (learned from training data in a real project)
imputer = SimpleImputer(strategy='median')
X_filled = imputer.fit_transform(X)

model = LinearRegression().fit(X_filled, y)
print("Coefficients:", model.coef_.round(2))
```
**Output:**
```text
experience        1
training_hours    1
salary            0
dtype: int64
Coefficients: [4.67 0.14]
```
**What it means:** One blank in each feature column was filled with that column's median, so all 8 rows could be used. In a real project you would split first and fit the imputer on the training rows only.
**Alternative / pitfalls:** `employees.dropna()` removes incomplete rows (here 2 of 8, a big loss). Filling with the average can shrink real variation; if many values are missing, say so in the report.
**Likely follow-ups:** 1) *Mean or median?* Median is safer with outliers. 2) *Why fit the imputer on training data only?* To avoid leakage.
**Common mistakes:** Imputing before the split; filling a missing target; treating 0 or 999 placeholders as real numbers.

### Q42 ⭐⭐ 🟡 What is regularisation in intuitive terms, and how do Ridge and Lasso differ?
**Asked at:** commonly asked (no company-specific report found); Ridge and Lasso questions appear in ML-round banks and blog guides (unverified).
**What the interviewer is checking:** That you can explain regularisation as a penalty against over-complicated models and name the key difference between Ridge and Lasso.
**Say this in the interview:** "Regularisation adds a penalty for large coefficients, which stops the model from chasing noise and overfitting. Ridge shrinks all coefficients smoothly toward zero; Lasso can push some exactly to zero, so it also drops variables."
**Explain simply:**
- Overfit means the model memorises the training data (including noise) and does worse on new data.
- Regularisation says: "fit well, but keep the coefficients small". A bigger penalty (`alpha` in sklearn) means a simpler model.
- Ridge (L2 penalty, from memory the standard name): shrinks coefficients but keeps all variables; good when many features overlap.
- Lasso (L1 penalty): shrinks some coefficients to exactly zero, so it acts as built-in variable selection.
- Scale the features first, otherwise the penalty treats big-unit variables unfairly.
**Sample data:** 10 made-up employees; `shoe_size` is a deliberately useless feature.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler

employees = pd.DataFrame({
    'experience':     [1, 2, 3, 5, 6, 8, 10, 12, 4, 7],
    'age':            [23, 25, 28, 30, 33, 35, 40, 44, 27, 34],
    'training_hours': [10, 25, 15, 30, 20, 40, 35, 45, 12, 22],
    'shoe_size':      [7, 9, 8, 7, 9, 8, 7, 9, 8, 7],
    'salary':         [32, 38, 42, 55, 56, 70, 75, 88, 45, 62],
})
features = ['experience', 'age', 'training_hours', 'shoe_size']
# Scale first so the penalty treats every feature fairly
X = StandardScaler().fit_transform(employees[features])
y = employees['salary']

results = pd.DataFrame({
    'plain':  LinearRegression().fit(X, y).coef_,
    'ridge':  Ridge(alpha=1).fit(X, y).coef_,
    'lasso':  Lasso(alpha=1).fit(X, y).coef_,
}, index=features)
print(results.round(2))
```
**Output:**
```text
                plain  ridge  lasso
experience      15.30   7.13  14.17
age             -0.63   6.11   0.00
training_hours   2.52   3.48   1.90
shoe_size       -0.23  -0.44  -0.00
```
**What it means:** Plain regression gives a strange negative age effect because age and experience overlap. Ridge shares the credit between them (7.1 and 6.1). Lasso keeps experience and training hours and sets age and shoe size to zero. (Coefficients are per one standard deviation of each feature, since the data was scaled.)
**Alternative / pitfalls:** The penalty strength alpha should be chosen by cross-validation (from memory, unverified: `RidgeCV` and `LassoCV` exist in sklearn). When two variables are highly correlated, Lasso may arbitrarily keep one, so "zero" does not mean "useless" (Q43).
**Likely follow-ups:** 1) *What does alpha = 0 give?* Ordinary regression. 2) *Why scale first?* The penalty depends on coefficient size, which depends on units.
**Common mistakes:** Forgetting to scale; picking alpha by training score; saying Lasso proves a variable is irrelevant.

### Q43 ⭐⭐ 🟡 What would you conclude if Lasso shrinks the coefficient of a variable exactly to zero?
**Asked at:** commonly asked (no company-specific report found); regularisation (ridge/lasso) appears in prep-site banks (unverified).
**What the interviewer is checking:** Whether you know Lasso does feature selection, and whether you avoid over-claiming what a zero means.
**Say this in the interview:** "Lasso has decided that variable adds little once the others are in the model, so it removed it. It does not prove the variable is useless on its own, because a correlated variable may have taken over its job, and the result depends on the penalty strength."
**Explain simply:**
- Lasso (a regression with a penalty that punishes large coefficients, which are the numbers that say how much each variable moves the prediction) can push weak coefficients all the way to exactly zero. Ridge only makes them small.
- A zero means "dropped from the model at this penalty strength", so Lasso doubles as a variable-selection tool.
- If two variables carry the same information (age and tenure), Lasso tends to keep one and zero the other; the dropped one may still matter in real life.
- A bigger penalty (`alpha`, the penalty strength) drops more variables; a smaller one drops fewer.
**Sample data:** 200 illustrative employees; salary truly depends on tenure only. `age` and `shoe_size` are noise.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler

# Illustrative data: salary really depends on tenure only; age and shoe_size are noise
rng = np.random.default_rng(42)
employees = pd.DataFrame({
    "tenure_years": rng.uniform(0, 10, 200),
    "age": rng.uniform(22, 55, 200),
    "shoe_size": rng.normal(8, 1, 200),
})
salary = 20000 + 3000 * employees["tenure_years"] + rng.normal(0, 3000, 200)

# Put features on the same scale first, because Lasso penalises coefficient size
X_scaled = StandardScaler().fit_transform(employees)

lasso = Lasso(alpha=1000).fit(X_scaled, salary)
print(pd.Series(lasso.coef_, index=employees.columns).round(1))
```
**Output:**
```text
tenure_years    7584.7
age                0.0
shoe_size          0.0
dtype: float64
```
**What it means:** Lasso kept tenure and removed the two noise variables. The coefficients are per one standard deviation (a typical spread of the variable), because we scaled the data.
**Alternative / pitfalls:** The zero depends on `alpha`; choose it by cross-validation (repeated train/validation splits). Always scale first, otherwise variables measured in big units are punished unfairly. Never say "age has no effect"; say "age added nothing to this model".
**Likely follow-ups:** 1) *Lasso or Ridge?* Lasso when you want a shorter list of variables; Ridge when many correlated variables each matter a little. 2) *Is a non-zero coefficient proof of importance?* No, it is only what the model kept.
**Common mistakes:** Treating a zero as "no relationship"; forgetting to scale; not mentioning the penalty strength.

### Q44 ⭐⭐ 🟡 What does `class_weight='balanced'` do in LogisticRegression, and when would you use it?
**Asked at:** commonly asked (no company-specific report found); class imbalance and `class_weight` appear in prep-site banks (unverified).
**What the interviewer is checking:** Whether you understand imbalance and the trade-off: more leavers caught, but more false alarms and distorted probabilities.
**Say this in the interview:** "It makes each mistake on the rare class count more during fitting, so the model stops ignoring leavers. I would use it when the rare group matters, and I would judge it on recall and precision, not accuracy."
**Explain simply:**
- Imbalance means one outcome is rare (most employees stay). A model can score high accuracy by predicting "stays" for everyone.
- `balanced` gives each class a weight = total rows / (2 x rows in that class). Rare class gets a big weight, common class a small one.
- Recall = share of real leavers we catch. Precision = share of flagged people who really leave.
- Trade-off: recall goes up, precision goes down, and predicted probabilities become too high (no longer true chances).
**Sample data:** Illustrative 2,000 employees, about 19% leave; 1,500 in training with 287 leavers, so the weights are 1500/(2 x 1213) = 0.62 for stayers and 1500/(2 x 287) = 2.61 for leavers.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score

# Illustrative data: about 19% of 2,000 employees leave
rng = np.random.default_rng(42)
employees = pd.DataFrame({
    "overtime_hours": rng.normal(10, 4, 2000),
    "tenure_years": rng.uniform(0, 10, 2000),
})
risk = -3.2 + 0.2 * employees["overtime_hours"] - 0.1 * employees["tenure_years"]
left = (rng.random(2000) < 1 / (1 + np.exp(-risk))).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    employees, left, test_size=0.25, stratify=left, random_state=42)

for weight in [None, "balanced"]:
    model = LogisticRegression(class_weight=weight).fit(X_train, y_train)
    predicted = model.predict(X_test)
    print(weight,
          "recall:", round(recall_score(y_test, predicted), 2),
          "precision:", round(precision_score(y_test, predicted), 2),
          "flagged:", predicted.sum())
```
**Output:**
```text
None recall: 0.06 precision: 0.46 flagged: 13
balanced recall: 0.59 precision: 0.3 flagged: 188
```
**What it means:** Without weights the model flags only 13 people and catches 6% of the 95 real leavers. With `balanced` it catches 59% but flags 188 people and 30% of them are right. Report recall and precision together, and ask whether HR can afford the extra calls.
**Alternative / pitfalls:** Lowering the decision threshold gives a similar effect without distorting probabilities (see Q58 and Q59). If you need honest probabilities, avoid `balanced` or recalibrate afterwards.
**Likely follow-ups:** 1) *Does it fix a weak model?* No, it only moves the trade-off. 2) *Alternatives?* Threshold tuning, collecting more leaver data.
**Common mistakes:** Judging by accuracy; reading probabilities from a `balanced` model as real chances; applying weights to the test set.

### Q45 ⭐⭐ 🟡 What is the intuition behind how linear regression and logistic regression are fitted (least squares versus maximum likelihood or log loss)?
**Asked at:** commonly asked (no company-specific report found); "maths of logistic regression" is reported for Tiger Analytics in snippets (unverified).
**What the interviewer is checking:** That you can describe "fitting" as picking the coefficients that make the mistakes smallest, in plain words.
**Say this in the interview:** "Linear regression picks the line that makes the squared gaps between actual and predicted values as small as possible. Logistic regression picks the coefficients that give the actual outcomes the highest probability, which is the same as minimising log loss."
**Explain simply:**
- Fitting means trying coefficient values and keeping the set with the lowest "badness score".
- Linear regression: badness = sum of squared errors (gap between actual and predicted, squared so misses in both directions count and big misses count more). The best line has a direct formula.
- Logistic regression: the outcome is 0/1, so squared gaps are a poor fit. Instead it asks "how likely was the data we saw?" (maximum likelihood). Log loss is that idea turned into a penalty: confident wrong answers are punished heavily.
- Logistic regression has no direct formula; the computer improves the coefficients step by step until they stop changing.
**Worked example (concept):** Five points x = 1..5, y = 2, 4, 5, 4, 6. The least squares line is y = 1.8 + 0.8x with squared error 2.4; a flatter line with the same intercept 1.8 but slope 0.5 has squared error 7.35, so it is worse. For five employees where 1 means left (0, 0, 1, 0, 1), predicted probabilities 0.2, 0.3, 0.6, 0.4, 0.7 give a log loss of 0.39; saying 0.5 for everyone gives 0.69. Lower is better.
**Alternative / pitfalls:** Least squares on a 0/1 target is the linear probability model (Q66) and can predict below 0 or above 1.
**Likely follow-ups:** 1) *Why squares?* They penalise large misses and give a clean formula. 2) *What is gradient descent?* Taking repeated small steps downhill on the badness score.
**Common mistakes:** Saying logistic regression minimises squared error; thinking it has a closed-form formula.

### Q46 ⭐⭐ 🟡 What does the parameter C mean in sklearn's LogisticRegression, and is regularisation applied by default?
**Asked at:** commonly asked (no company-specific report found); "logistic regression parameter tuning" is reported for Tiger Analytics in snippets (unverified); C as inverse regularisation appears in sklearn tutorials.
**What the interviewer is checking:** That you know C works backwards (small C = stronger penalty) and that a penalty is on by default.
**Say this in the interview:** "C is the inverse of the penalty strength. Small C means strong regularisation and smaller coefficients; large C means weak regularisation. Yes, sklearn applies an L2 (ridge-style) penalty by default with C = 1.0, which surprises people who expect plain logistic regression."
**Explain simply:**
- Regularisation (a penalty on large coefficients to reduce overfitting, meaning memorising noise) is switched on by default.
- Default checked on the installed sklearn 1.9.1: `C=1.0`, L2 penalty (`l1_ratio=0.0`, the setting that means pure L2).
- In 1.9.1 the old `penalty` argument is deprecated (a warning appears if you set it); use `l1_ratio` and `C` instead. This version detail is verified here only; other versions are from memory, unverified.
- Because of the penalty, scale your features first, otherwise variables in big units are penalised unfairly.
**Sample data:** Illustrative 2,000 employees (overtime, tenure) with about 19% leavers.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Illustrative data: leaving depends on overtime and tenure
rng = np.random.default_rng(42)
employees = pd.DataFrame({
    "overtime_hours": rng.normal(10, 4, 2000),
    "tenure_years": rng.uniform(0, 10, 2000),
})
risk = -3.2 + 0.2 * employees["overtime_hours"] - 0.1 * employees["tenure_years"]
left = (rng.random(2000) < 1 / (1 + np.exp(-risk))).astype(int)

X_scaled = StandardScaler().fit_transform(employees)

# Small C = strong penalty, large C = weak penalty; default is C=1.0
for C in [0.001, 1, 1000]:
    model = LogisticRegression(C=C).fit(X_scaled, left)
    print("C =", C, "coefficients:", model.coef_.round(2))
```
**Output:**
```text
C = 0.001 coefficients: [[ 0.18 -0.05]]
C = 1 coefficients: [[ 0.84 -0.2 ]]
C = 1000 coefficients: [[ 0.85 -0.2 ]]
```
**What it means:** A tiny C squeezes the coefficients toward zero; C = 1 and C = 1000 are almost the same here because the data is large and has few variables, so the penalty barely matters.
**Alternative / pitfalls:** Choose C by cross-validation (`LogisticRegressionCV`). Do not compare coefficients with a statsmodels fit without noting that statsmodels has no penalty by default.
**Likely follow-ups:** 1) *How do I switch it off?* Use a very large C (the `penalty=None` route is deprecated in 1.9.1). 2) *Lasso-style?* Use `l1_ratio=1` with a solver that supports it (from memory, unverified for solver names).
**Common mistakes:** Thinking big C means more regularisation; not scaling; believing sklearn gives plain unpenalised results.

### Q47 ⭐⭐ 🟡 Calculate the odds ratio of leaving for overtime versus no-overtime employees from the table below.
Overtime group: 100 employees, 30 left. No-overtime group: 100 employees, 10 left.
**Asked at:** commonly asked (no company-specific report found); odds-ratio calculation is a standard item in logistic regression banks (unverified).
**What the interviewer is checking:** That you use odds (left divided by stayed), not probabilities, and can say what the ratio means.
**Say this in the interview:** "Odds for overtime are 30 to 70, which is 0.43. Odds for no overtime are 10 to 90, which is 0.11. The odds ratio is 3.86: the odds of leaving are about 3.9 times higher with overtime. The risk ratio is 3.0, so I would be careful not to say 'three times as likely' for the odds ratio."
**Explain simply:**
- Probability = left / total. Odds = left / stayed.
- Odds ratio = odds in group A divided by odds in group B. Above 1 means higher odds in group A.
- Odds ratio exceeds risk ratio when the outcome is not rare (30% here is not rare).
**Sample data:**

| Group | Employees | Left | Stayed |
|---|---|---|---|
| Overtime | 100 | 30 | 70 |
| No overtime | 100 | 10 | 90 |

**Code (what you write in the interview):**
```python
# Odds = left / stayed in each group
odds_overtime = 30 / 70
odds_no_overtime = 10 / 90

odds_ratio = odds_overtime / odds_no_overtime
risk_ratio = (30 / 100) / (10 / 100)

print("Odds (overtime):", round(odds_overtime, 3))
print("Odds (no overtime):", round(odds_no_overtime, 3))
print("Odds ratio:", round(odds_ratio, 2))
print("Risk ratio:", round(risk_ratio, 2))
```
**Output:**
```text
Odds (overtime): 0.429
Odds (no overtime): 0.111
Odds ratio: 3.86
Risk ratio: 3.0
```
**What it means:** Overtime employees have about 3.9 times the odds of leaving. In plain terms for a manager: 30% leave with overtime against 10% without, which is 3 times the risk.
**Alternative / pitfalls:** Cross-multiplication gives the same answer: (30 x 90) / (70 x 10) = 2700 / 700 = 3.86. This is a raw comparison; it does not control for tenure or pay, and it is not proof that overtime causes leaving.
**Likely follow-ups:** 1) *Odds ratio of 1?* No difference. 2) *Link to logistic regression?* The model's coefficient is the log of an odds ratio (Q54).
**Common mistakes:** Dividing probabilities and calling it the odds ratio; reading the odds ratio as "times more likely".

### Q48 ⭐⭐ 🟡 How does sklearn's LogisticRegression handle a target with three classes, such as three exit reasons?
**Asked at:** commonly asked (no company-specific report found); multiclass handling appears in sklearn-focused banks (unverified).
**What the interviewer is checking:** That you know it works out of the box and returns one probability per class that adds to 1.
**Say this in the interview:** "You just call `fit` with the three-label column. In the current sklearn it fits one model that gives a probability for each class (the multinomial or softmax approach), one set of coefficients per class, and the probabilities add up to 1. `predict` picks the class with the highest probability."
**Explain simply:**
- Two classes give one row of coefficients; three classes give three rows (one per class).
- `predict_proba` returns one column per class, ordered as in `model.classes_` (alphabetical).
- Checked on sklearn 1.9.1: the old `multi_class` argument is not in the signature any more. How older versions behaved is from memory, unverified.
- Business use: predicting which reason (pay, manager, career) a leaver will give, to target actions.
**Sample data:** 300 illustrative leavers with `salary_gap` and `manager_rating`; reason is pay, manager or career.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Illustrative data: three exit reasons
rng = np.random.default_rng(42)
leavers = pd.DataFrame({
    "salary_gap": rng.normal(0, 1, 300),
    "manager_rating": rng.normal(3, 1, 300),
})
exit_reason = np.where(leavers["salary_gap"] < -0.5, "pay",
              np.where(leavers["manager_rating"] < 2.5, "manager", "career"))

model = LogisticRegression().fit(leavers, exit_reason)
print(model.classes_)
print("coef_ shape:", model.coef_.shape)

# One probability per reason; each row adds up to 1
probabilities = model.predict_proba(leavers.iloc[:2])
print(probabilities.round(2))
print(probabilities.sum(axis=1))
```
**Output:**
```text
['career' 'manager' 'pay']
coef_ shape: (3, 2)
[[1.   0.   0.  ]
 [0.   0.08 0.92]]
[1. 1.]
```
**What it means:** There are three coefficient rows (three reasons, two features). The first employee is almost surely "career"; the second is 92% "pay".
**Alternative / pitfalls:** One-vs-rest (a separate yes/no model per class) is the older alternative. Classes with very few examples get unreliable probabilities.
**Likely follow-ups:** 1) *How do you score it?* Per-class precision and recall, or a confusion matrix. 2) *Order of columns?* Same as `model.classes_`.
**Common mistakes:** Assuming the order of the columns is the order of appearance; expecting a single coefficient per feature.

### Q49 ⭐⭐ 🟡 Write the code to predict the probability of leaving for one new employee with a fitted model, and say how you read the output.
Features used in training: `tenure_years`, `overtime_hours`. New employee: 2 years tenure, 10 overtime hours.
**Asked at:** commonly asked (no company-specific report found); `predict` versus `predict_proba` is a common implementation question in sklearn banks (unverified).
**What the interviewer is checking:** That you build the new row with the same columns, use `predict_proba`, and pick the right column.
**Say this in the interview:** "I put the new employee in a one-row table with the same column names and order, call `predict_proba`, and take the second column, because column 1 is the probability of class 1, which is leaving. Here it is about 43%."
**Explain simply:**
- `predict_proba` returns two numbers per row: probability of class 0 (stays) and class 1 (leaves), in the order of `model.classes_`.
- `predict` only gives the label, using a 0.5 cut-off.
- Column order and names must match training.
**Sample data:** Illustrative training set of 500 employees (random seed 42) with `tenure_years` and `overtime_hours`; about 43% of them left.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Illustrative training data (500 employees); left = 1 means the employee left
rng = np.random.default_rng(42)
employees = pd.DataFrame({
    "tenure_years": rng.uniform(0, 10, 500),
    "overtime_hours": rng.uniform(0, 30, 500),
})
risk = -1 - 0.25 * employees["tenure_years"] + 0.12 * employees["overtime_hours"]
left = (rng.random(500) < 1 / (1 + np.exp(-risk))).astype(int)

model = LogisticRegression().fit(employees, left)

# Same column names and order as in training
new_employee = pd.DataFrame({"tenure_years": [2], "overtime_hours": [10]})

print(model.classes_)
print(model.predict_proba(new_employee).round(3))
print(model.predict(new_employee))
```
**Output:**
```text
[0 1]
[[0.567 0.433]]
[0]
```
**What it means:** The model gives this employee a 43.3% chance of leaving and 56.7% of staying; the label is 0 (stays) because 43% is below 0.5. For a manager: "roughly 4 in 10 employees like this leave", and 0.5 is only a default cut-off.
**Alternative / pitfalls:** For a business decision use the probability and a cost-based threshold (Q58), not the 0.5 label. Passing a bare list `[[2, 10]]` works but hides column order mistakes.
**Likely follow-ups:** 1) *Why not 0.5?* The costs of errors are unequal. 2) *Is 43% a true chance?* Only if the model is calibrated (Q59).
**Common mistakes:** Reading column 0 as the leave probability; wrong column order; calling `predict` and reporting it as a probability.

### Q50 ⭐⭐ 🟡 A manager asks for the top drivers of attrition from your logistic regression. How do you rank the variables fairly?
**Asked at:** commonly asked (no company-specific report found); feature importance from a linear model is a common follow-up in ML rounds (unverified).
**What the interviewer is checking:** That you know raw coefficients depend on units and that you standardise before ranking, with caution about causation.
**Say this in the interview:** "I would not rank raw coefficients because overtime in hours and tenure in years have different scales. I standardise the variables so each coefficient means 'per one standard deviation', then rank by size and report odds ratios. I would also say this describes the model's pattern, not proven causes."
**Explain simply:**
- A standard deviation is the typical spread of a variable. Standardising puts every variable on that same yardstick.
- Then a bigger absolute coefficient means a stronger pull on the odds of leaving. The sign says the direction.
- Odds ratio = e raised to the coefficient: above 1 raises the odds of leaving, below 1 lowers them.
- Check that variables are not heavily correlated, otherwise credit is split unpredictably.
**Sample data:** Illustrative 500 employees; tenure 0-10 years, overtime 0-30 hours.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Illustrative data: tenure is measured in years (0-10), overtime in hours (0-30)
rng = np.random.default_rng(42)
employees = pd.DataFrame({
    "tenure_years": rng.uniform(0, 10, 500),
    "overtime_hours": rng.uniform(0, 30, 500),
})
risk = -1 - 0.25 * employees["tenure_years"] + 0.12 * employees["overtime_hours"]
left = (rng.random(500) < 1 / (1 + np.exp(-risk))).astype(int)

# Raw coefficients: not comparable, because the units differ
raw_model = LogisticRegression().fit(employees, left)
print("raw:\n", pd.Series(raw_model.coef_[0], index=employees.columns).round(2))

# Standardise so every variable is "per 1 standard deviation", then compare
X_scaled = StandardScaler().fit_transform(employees)
scaled_model = LogisticRegression().fit(X_scaled, left)
print("standardised:\n", pd.Series(scaled_model.coef_[0], index=employees.columns).round(2))
print("odds ratios:\n", pd.Series(np.exp(scaled_model.coef_[0]), index=employees.columns).round(2))
```
**Output:**
```text
raw:
 tenure_years     -0.23
overtime_hours    0.12
dtype: float64
standardised:
 tenure_years     -0.65
overtime_hours    1.05
dtype: float64
odds ratios:
 tenure_years      0.52
overtime_hours    2.85
dtype: float64
```
**What it means:** The raw numbers make tenure look bigger than overtime (0.23 against 0.12) only because of units; on a fair scale overtime is the bigger driver. A one standard deviation rise in overtime multiplies the odds of leaving by 2.85; a one standard deviation rise in tenure multiplies them by 0.52 (lowers them).
**Alternative / pitfalls:** Permutation importance (shuffle a variable and see how much accuracy drops) works for any model. A driver in a model is an association, not a cause. Note that the penalty (Q46) is on by default, so scaling also matters for the fit itself.
**Likely follow-ups:** 1) *Does it show causes?* No. 2) *Correlated variables?* Rankings become unstable; check correlations first.
**Common mistakes:** Ranking raw coefficients; ignoring the sign; calling drivers causes.

### Q51 ⭐⭐ 🟡 What does a dummy variable coefficient mean in the model below?
salary = 40,000 + 3,000 × experience - 2,500 × department_Sales, with HR as the reference department. Interpret -2,500.
**Asked at:** commonly asked (no company-specific report found); reference-category interpretation appears in odds-ratio and regression tutorials (UCLA OARC, bookdown) in the sources.
**What the interviewer is checking:** That you say "compared with the reference group, holding other variables the same".
**Say this in the interview:** "Sales employees earn on average Rs 2,500 less than HR employees with the same experience. HR is the reference group, so the coefficient is always a comparison against HR."
**Explain simply:**
- A dummy variable is a 0/1 column: `department_Sales` = 1 for Sales, 0 for everyone else.
- One department is left out as the reference (here HR). Each dummy compares its group to that reference.
- "Holding experience the same" means we compare people at the same experience level.
- Check: at 5 years of experience, an HR employee is predicted at 40,000 + 3,000 x 5 = 55,000 and a Sales employee at 55,000 - 2,500 = 52,500.
**Worked example:** HR with 5 years: 55,000. Sales with 5 years: 52,500. The gap of 2,500 is the same at any experience level (the model assumes the same slope for both).
**Alternative / pitfalls:** The sign flips if you choose a different reference department. The currency unit is not stated in the question; read it as 2,500 in the same units as salary. If experience effects differ by department, add an interaction (Q55). A gap is an association, not proof of discrimination or causes.
**Likely follow-ups:** 1) *Why drop one category?* Otherwise the dummies add up to a constant and the model cannot separate them (the dummy variable trap). 2) *What if the model is logistic?* Then the coefficient is a change in log-odds; exponentiate for an odds ratio.
**Common mistakes:** Forgetting the reference group; saying "Sales earn 2,500 less than everyone"; leaving out "holding experience constant".

### Q52 ⭐⭐ 🟡 Can the test-set R² be negative, and what does it mean if it is?
**Asked at:** commonly asked (no company-specific report found); R-squared pitfalls are standard in regression banks (unverified).
**What the interviewer is checking:** That you know R² on new data compares you with "predict the average", and can be worse than that.
**Say this in the interview:** "Yes. On test data R² can be negative, and it means the model predicts worse than simply guessing the average of the target. It is a sign of overfitting, a wrong model, or a test set that differs from training."
**Explain simply:**
- R² = 1 - (model's squared error / squared error of always predicting the average). On training data with an intercept it cannot go below 0. On test data it can.
- Negative: the model's errors are larger than the baseline's (Q62).
- Typical causes: too many variables for too few rows (overfitting, memorising noise), leakage-free but unstable fit, or a shift between train and test periods.
**Sample data:** 30 illustrative employees, 15 pure-noise features, noise target. Half used to train.
**Code (what you write in the interview):**
```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Illustrative: 30 employees, 15 features that are pure noise, target is noise too
rng = np.random.default_rng(42)
X = rng.normal(0, 1, (30, 15))
y = rng.normal(0, 1, 30)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
model = LinearRegression().fit(X_train, y_train)

print("train R2:", round(r2_score(y_train, model.predict(X_train)), 2))
print("test R2:", round(r2_score(y_test, model.predict(X_test)), 2))
```
**Output:**
```text
train R2: 1.0
test R2: -80.07
```
**What it means:** The model fits the 15 training rows perfectly (15 variables, 15 rows) but is far worse than guessing the average on new rows. Tell a manager: "it looks perfect on old data and fails on new data, so do not use it".
**Alternative / pitfalls:** The output depends on the seed; the size is extreme because the example is built to overfit. Fix by fewer variables, more rows, regularisation (Q42) or a simpler model.
**Likely follow-ups:** 1) *Can training R² be negative?* Not with an intercept in ordinary least squares. 2) *What do you do?* Compare against the mean baseline and simplify.
**Common mistakes:** Saying R² must lie between 0 and 1; judging a model on training R² only.

### Q53 ⭐⭐ 🟡 Why would you use `stratify=y` in train_test_split for an attrition dataset?
**Asked at:** commonly asked (no company-specific report found); stratified splitting appears in imbalance discussions in prep banks (unverified).
**What the interviewer is checking:** That you know random splits can distort a rare class and `stratify` keeps proportions.
**Say this in the interview:** "Attrition is a minority outcome. A random split can put too few or too many leavers in the test set by chance. `stratify=y` keeps the same leaver percentage in both train and test, so the evaluation is stable and fair."
**Explain simply:**
- Stratified means each part keeps the same mix of classes as the whole data.
- With 10% leavers, both train and test will have about 10% leavers.
- It matters most when the rare class is small, because a few more or fewer leavers swings recall and precision.
- Stratify on the target `y` (and not on the features).
**Sample data:** 1,000 illustrative employees, 100 leavers (10%); a 20% test set should hold 20 leavers.
**Code (what you write in the interview):**
```python
import numpy as np
from sklearn.model_selection import train_test_split

# Illustrative: 1,000 employees, 100 leavers (10%)
left = np.array([1] * 100 + [0] * 900)
employees = np.arange(1000).reshape(-1, 1)

# Leavers landing in the 200-row test set, for 5 different random splits
for stratify in [None, left]:
    leavers_in_test = []
    for seed in range(5):
        _, _, _, y_test = train_test_split(
            employees, left, test_size=0.2, stratify=stratify, random_state=seed)
        leavers_in_test.append(int(y_test.sum()))
    print("stratified" if stratify is not None else "plain", leavers_in_test)
```
**Output:**
```text
plain [15, 20, 15, 26, 19]
stratified [20, 20, 20, 20, 20]
```
**What it means:** A plain split gave between 15 and 26 leavers in the test set, so recall would jump around. The stratified split gave exactly 20 every time.
**Alternative / pitfalls:** For small data use stratified cross-validation (`StratifiedKFold`). Stratifying does not fix imbalance, it only keeps it consistent. For time-ordered data, split by date instead.
**Likely follow-ups:** 1) *Does it help the model?* No, it makes the evaluation reliable. 2) *Other uses?* Any imbalanced classification such as fraud or no-shows.
**Common mistakes:** Forgetting it; stratifying on a feature; using a random split for time-based data.

### Q54 ⭐⭐ 🟡 How do you read the coef, std err, P>|z| and confidence interval columns in a statsmodels logistic regression summary?
One row: `overtime  coef 0.70  std err 0.20  z 3.50  P>|z| 0.000  [0.025 0.308  0.975 1.092]`.
**Asked at:** commonly asked (no company-specific report found); reading a statsmodels summary is a common implementation topic (unverified).
**What the interviewer is checking:** That you turn each column into a plain statement and convert the coefficient into an odds ratio.
**Say this in the interview:** "The coefficient 0.70 is the change in log-odds of leaving for overtime versus none. Exponentiated, that is an odds ratio of 2.0: about double the odds. The standard error says how uncertain that estimate is. The p-value is below 0.001, and the interval is clear of zero, so overtime is a statistically significant factor; the odds-ratio interval is roughly 1.4 to 3.0."
**Explain simply:**
- **coef**: change in log-odds per unit of the variable (here overtime yes versus no). Exponentiate to read it as an odds ratio.
- **std err**: how much the estimate would wobble across samples; smaller is more precise.
- **z**: coef divided by std err = 0.70 / 0.20 = 3.5, how many standard errors away from zero.
- **P>|z|**: the chance of a result this extreme if there were truly no effect. Here about 0.0005, shown as 0.000.
- **[0.025, 0.975]**: the 95% confidence interval (a range of plausible values) for the coefficient: 0.70 plus or minus 1.96 x 0.20 gives 0.308 to 1.092. Because it excludes 0, the effect is significant.
**Code (what you write in the interview):**
```python
import numpy as np

coef, std_err = 0.70, 0.20
ci_low, ci_high = 0.308, 1.092

print("Odds ratio:", round(np.exp(coef), 2))
print("95% CI for odds ratio:", round(np.exp(ci_low), 2), "to", round(np.exp(ci_high), 2))
print("z:", round(coef / std_err, 2))
```
**Output:**
```text
Odds ratio: 2.01
95% CI for odds ratio: 1.36 to 2.98
z: 3.5
```
**What it means:** Overtime roughly doubles the odds of leaving, and the plausible range is about 1.4 to 3.0 times.
**Alternative / pitfalls:** Statistically significant does not mean large or causal. The interval is for the coefficient; exponentiate both ends for the odds ratio. A significant p-value with a huge sample can still be a trivial effect.
**Likely follow-ups:** 1) *What if the interval includes 0?* The effect is not clearly different from none (for odds ratios: includes 1). 2) *Does sklearn give p-values?* No (Q57).
**Common mistakes:** Reading the coef as a probability change; saying p = 0.000 means "zero chance"; forgetting to exponentiate.

### Q55 ⭐⭐ 🟡 What is an interaction term, and when would you add one in a regression?
**Asked at:** commonly asked (no company-specific report found); interactions appear in regression bank questions (unverified).
**What the interviewer is checking:** That you understand "the effect of one variable depends on another", and can read the coefficient.
**Say this in the interview:** "An interaction term is two variables multiplied together. I add one when the effect of one variable changes depending on another, for example overtime hurting retention much more for new joiners than for veterans."
**Explain simply:**
- Without interaction the model assumes overtime adds the same risk for everyone.
- With an interaction column (overtime x new_joiner), the model adds an extra amount only when both are 1.
- Add one when business sense or a group comparison suggests the effect differs by group, and keep the model explainable.
**Sample data:** Illustrative average leave risk (%) by group (400 employees):

| Overtime | New joiner | Average risk |
|---|---|---|
| 0 | 0 | 10.1 |
| 0 | 1 | 12.6 |
| 1 | 0 | 15.0 |
| 1 | 1 | 37.9 |

**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Illustrative: leave risk (%) is high only when overtime AND new joiner combine
rng = np.random.default_rng(42)
employees = pd.DataFrame({
    "overtime": rng.integers(0, 2, 400),
    "new_joiner": rng.integers(0, 2, 400),
})
risk_pct = (10 + 5 * employees["overtime"] + 3 * employees["new_joiner"]
            + 20 * employees["overtime"] * employees["new_joiner"]
            + rng.normal(0, 2, 400))

# Interaction term = the two columns multiplied
employees["overtime_x_new_joiner"] = employees["overtime"] * employees["new_joiner"]

model = LinearRegression().fit(employees, risk_pct)
print(pd.Series(model.coef_, index=employees.columns).round(1))
print("intercept:", round(model.intercept_, 1))
```
**Output:**
```text
overtime                  5.0
new_joiner                2.6
overtime_x_new_joiner    20.3
dtype: float64
intercept: 10.1
```
**What it means:** Overtime adds about 5 points of risk for experienced staff, but 5 + 20.3 = 25.3 points for new joiners. A model without the interaction would give one "average" effect (about 16 points) and be wrong for both groups.
**Alternative / pitfalls:** Tree models find interactions automatically. Too many interactions overfit and become hard to explain. Keep the main effects in the model alongside the interaction.
**Likely follow-ups:** 1) *How to find them?* Group averages and plots first. 2) *Interpret a logistic interaction?* On the log-odds scale; explain with predicted probabilities.
**Common mistakes:** Adding the product without the main effects; interpreting the main effect alone when an interaction exists.

### Q56 ⭐⭐ 🟡 Why do we not rely on R² for logistic regression, and what do people use instead?
**Asked at:** commonly asked (no company-specific report found); evaluation of classifiers is covered in logistic regression banks (unverified).
**What the interviewer is checking:** That you know R² is built for continuous targets and that you can name classification metrics.
**Say this in the interview:** "R² measures how much of the variation in a number you explain. A 0/1 outcome has no meaningful spread of that kind, so R² is misleading. I use log loss, AUC, and precision and recall at a chosen threshold, and a pseudo R² such as McFadden's if someone wants a single fit number."
**Explain simply:**
- The target is 0 or 1, but the prediction is a probability, so "squared distance" behaves oddly and stays low even for a good model.
- **Log loss**: penalises confident wrong probabilities; lower is better.
- **AUC**: chance that a random leaver gets a higher score than a random stayer (0.5 is guessing, 1.0 is perfect).
- **Precision and recall** (Q44) at the threshold you will really use.
- **Pseudo R² (McFadden)**: 1 minus the model's log-likelihood divided by that of a no-variable model; 0.2-0.4 is often described as good (a rule of thumb from memory, unverified).
**Sample data:** 1,000 illustrative employees, two features, about 25% leave (built inside the code).
**Code (what you write in the interview):**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score, r2_score

# Illustrative data: 1,000 employees, two features, about 25% leave
rng = np.random.default_rng(42)
features = rng.normal(size=(1000, 2))
risk = -1.2 + 0.8 * features[:, 0] + 0.5 * features[:, 1]
left = (rng.random(1000) < 1 / (1 + np.exp(-risk))).astype(int)

predicted = LogisticRegression().fit(features, left).predict_proba(features)[:, 1]
no_variable_loss = log_loss(left, np.full(1000, left.mean()))
model_loss = log_loss(left, predicted)

print("Ordinary R2 on probabilities:", round(r2_score(left, predicted), 2))
print("McFadden pseudo R2:", round(1 - model_loss / no_variable_loss, 2))
print("Log loss: model", round(model_loss, 2), "| always the average rate", round(no_variable_loss, 2))
print("AUC:", round(roc_auc_score(left, predicted), 2))
```
**Output:** (seed 42; simulated data, scored on the training rows for brevity)
```text
Ordinary R2 on probabilities: 0.1
McFadden pseudo R2: 0.09
Log loss: model 0.51 | always the average rate 0.56
AUC: 0.7
```
**What it means:** The model beats the "average rate for everyone" baseline (log loss 0.51 against 0.56) and ranks leavers above stayers 70% of the time (AUC 0.70). The R-squared style numbers look small (0.09 to 0.10) even though the model is useful, which is why they are a poor headline. Report AUC and the precision/recall trade-off, ideally on held-out data.
**Alternative / pitfalls:** Accuracy is misleading when the outcome is rare. Always evaluate on held-out data (Q53).
**Likely follow-ups:** 1) *Which one to tell a manager?* Recall and precision at the chosen threshold, in counts of people. 2) *Brier score?* Mean squared gap of probability from outcome; it also checks calibration (Q59).
**Common mistakes:** Reporting R² for a classifier; reporting only accuracy; comparing pseudo R² with ordinary R².

### Q57 ⭐⭐ 🟡 When would you use statsmodels instead of sklearn for a regression, and when sklearn?
**Asked at:** commonly asked (no company-specific report found); the sklearn versus statsmodels split is a common practical question (unverified).
**What the interviewer is checking:** That you choose by purpose: explaining and testing versus predicting and validating.
**Say this in the interview:** "I use statsmodels when I want to explain: it gives coefficients with standard errors, p-values and confidence intervals in one summary. I use sklearn when I want to predict: it has train/test splitting, pipelines, regularisation and cross-validation built in."
**Explain simply:**
- **statsmodels**: statistics-style output (`summary()`), no regularisation by default, you add the constant (intercept) yourself with `sm.add_constant`.
- **sklearn**: prediction-style workflow, regularised by default for logistic regression (Q46), no p-values.
- The same data can give slightly different coefficients because of that default penalty.
- Both are fine for a simple model; the choice is about what the audience needs.
**Worked example:** HR asks "does overtime significantly raise attrition, and by how much?" Use statsmodels: an odds ratio of 2.0 with a 95% interval. HR asks "score every employee monthly and check it on held-out data?" Use sklearn with a Pipeline (Q65).
**Alternative / pitfalls:** Use both: explore with statsmodels, productionise with sklearn. Do not mix up their coefficient meanings without checking the penalty and scaling. Version-specific details are from memory, unverified.
**Likely follow-ups:** 1) *How to get p-values in sklearn?* Not built in; use statsmodels or bootstrapping. 2) *Why the intercept?* statsmodels does not add one automatically.
**Common mistakes:** Forgetting `add_constant`; comparing coefficients across the two without noting the penalty; using p-values as a prediction-quality measure.

### Q58 ⭐⭐ 🟡 For which model setting would a false negative be costlier than a false positive, and how would that change your threshold?
Illustrative costs: missing a leaver costs Rs 4,00,000 in rehiring; a wasted retention call costs Rs 2,000. Compute the break-even probability.
**Asked at:** commonly asked (no company-specific report found); threshold choice and cost of errors appear in classification banks (unverified).
**What the interviewer is checking:** That you tie the threshold to business costs rather than the default 0.5.
**Say this in the interview:** "Attrition of key staff, fraud, or disease screening: a false negative (missing a real leaver) costs far more than a false positive (an unneeded call). So I lower the threshold. With these costs the break-even is about 0.5%: act on anyone whose predicted risk is above that."
**Explain simply:**
- False negative: the model says "will stay" but the employee leaves. False positive: the model says "will leave" but the employee stays.
- Act when expected loss from ignoring is bigger than the cost of acting: p x 4,00,000 > (1 - p) x 2,000.
- Solving: p > 2,000 / (4,00,000 + 2,000) = about 0.00498, roughly 0.5%.
**Code (what you write in the interview):**
```python
cost_missed_leaver = 400000    # false negative: rehiring cost
cost_wasted_call = 2000        # false positive: needless retention call

# Act when: p * cost_missed_leaver > (1 - p) * cost_wasted_call
break_even = cost_wasted_call / (cost_missed_leaver + cost_wasted_call)
print("Break-even probability:", round(break_even, 5))
print("As a percentage:", round(break_even * 100, 2))
```
**Output:**
```text
Break-even probability: 0.00498
As a percentage: 0.5
```
**What it means:** On cost alone you would call almost everyone. In reality a call does not always retain the person and HR time is limited, so treat 0.5% as the mathematical floor and set a practical threshold by checking how many people each threshold flags.
**Alternative / pitfalls:** The simple formula assumes the call always saves the leaver and that probabilities are well calibrated (Q59). A real rule would include the success rate of the retention action (for example if only 20% of calls work, the benefit is 20% of 4,00,000). Where false positives are costlier (for example firing decisions), raise the threshold.
**Likely follow-ups:** 1) *Where do the costs come from?* Finance and HR estimates, as ranges. 2) *How do you choose in practice?* Plot cost against threshold.
**Common mistakes:** Using 0.5 by default; ignoring the capacity limit; treating costs as exact.

### Q59 ⭐⭐ 🔴 What is calibration for a logistic regression model, and how would you check that '30% risk' really means about 30 in 100?
**Asked at:** commonly asked (no company-specific report found); calibration appears in advanced ML-round banks (unverified).
**What the interviewer is checking:** That you separate ranking ability (AUC) from honest probabilities, and know the simple check.
**Say this in the interview:** "Calibration means predicted probabilities match real frequencies. To check it, I group employees into risk bands, and compare the average predicted risk with the actual leaving rate in each band. If the 30% band really has about 30 leavers per 100, it is calibrated."
**Explain simply:**
- A model can rank people well but still say 30% when the real rate is 15%.
- Method: sort held-out employees by predicted risk, cut into 5 or 10 equal groups, compare average prediction with the real rate. Plot predicted against actual; the ideal is a straight diagonal.
- Brier score (average squared gap between probability and outcome, lower is better) summarises probability quality.
- Plain logistic regression is usually reasonably calibrated; `class_weight='balanced'` (Q44) distorts it.
**Sample data:** 5,000 illustrative employees, three features, about 20% leavers; 40% held out for testing.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss

# Illustrative data: 5,000 employees, three features, about 20% leave
rng = np.random.default_rng(42)
features = rng.normal(0, 1, (5000, 3))
risk = -1.2 + 1.2 * features[:, 0] + 0.8 * features[:, 1] - 0.5 * features[:, 2]
left = (rng.random(5000) < 1 / (1 + np.exp(-risk))).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    features, left, test_size=0.4, stratify=left, random_state=42)

for weight in [None, "balanced"]:
    model = LogisticRegression(class_weight=weight).fit(X_train, y_train)
    predicted_risk = model.predict_proba(X_test)[:, 1]

    # Group employees into 5 equal-sized risk bands, compare predicted vs actual
    actual_rate, average_predicted = calibration_curve(
        y_test, predicted_risk, n_bins=5, strategy="quantile")
    table = pd.DataFrame({"avg_predicted": average_predicted.round(2),
                          "actual_rate": actual_rate.round(2)})
    print("class_weight =", weight)
    print(table)
    print("Brier score:", round(brier_score_loss(y_test, predicted_risk), 3))
```
**Output:**
```text
class_weight = None
   avg_predicted  actual_rate
0           0.04         0.05
1           0.11         0.10
2           0.22         0.26
3           0.39         0.40
4           0.68         0.70
Brier score: 0.152
class_weight = balanced
   avg_predicted  actual_rate
0           0.09         0.05
1           0.23         0.09
2           0.40         0.26
3           0.59         0.40
4           0.82         0.71
Brier score: 0.169
```
**What it means:** The plain model is well calibrated: in the band predicted at 0.39, 40% really left. The balanced model overstates risk (it says 0.40 where the real rate is 0.26). Tell a manager: "when the model says about 40%, about 4 in 10 leave" only for the plain model.
**Alternative / pitfalls:** If miscalibrated, recalibrate with `CalibratedClassifierCV` (Platt scaling or isotonic; from memory, unverified details). Use held-out data; small bands are noisy.
**Likely follow-ups:** 1) *Does good AUC imply good calibration?* No. 2) *When does it matter?* When you use the probability itself (costs, headcount forecasts).
**Common mistakes:** Checking on training data; using too few rows per band; trusting probabilities from a `balanced` model.

### Q60 ⭐⭐ 🔴 What is perfect separation in logistic regression, what warning signs do you see, and what do you do?
**Asked at:** commonly asked (no company-specific report found); perfect separation is a known ML-round topic (unverified).
**What the interviewer is checking:** That you recognise a too-good-to-be-true model and know the causes and fixes.
**Say this in the interview:** "Perfect separation means a variable, or a combination, splits leavers and stayers exactly. The model then tries to make coefficients infinite. Signs are huge coefficients, huge standard errors, convergence warnings, and perfect accuracy. I would first check for leakage, then regularise, combine categories, or get more data."
**Explain simply:**
- Example: every employee with more than 10 overtime hours left, every other stayed. The model can always get a better fit by making the slope steeper, so the maximum-likelihood fit never settles.
- Warning signs: coefficients in the tens or hundreds, enormous standard errors, a "perfect separation" or convergence warning in statsmodels, near 100% accuracy.
- Common causes: leakage (a column that includes the outcome, such as an exit-interview flag), tiny datasets, a rare category (a department with one employee).
- What to do: remove leaked columns; merge rare categories; add regularisation (a smaller C in sklearn, Q46); collect more data.
**Sample data:** 10 illustrative employees; overtime 2 to 20 hours; leavers are exactly those above 10 hours.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Illustrative: leaving starts exactly above 10 overtime hours
employees = pd.DataFrame({
    "overtime_hours": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
    "left":           [0, 0, 0, 0, 0,  1,  1,  1,  1,  1],
})

for C in [1.0, 1_000_000]:
    model = LogisticRegression(C=C).fit(employees[["overtime_hours"]], employees["left"])
    print("C =", C, "coef:", model.coef_.round(2), "intercept:", model.intercept_.round(2))
```
**Output:**
```text
C = 1.0 coef: [[0.96]] intercept: [-10.61]
C = 1000000 coef: [[9.36]] intercept: [-102.64]
```
**What it means:** With almost no penalty the coefficient balloons (9.36 and growing as C grows); with the default penalty it stays modest. In a separate check on this same data, statsmodels `Logit` raised a `PerfectSeparationWarning` and a convergence warning, and gave a coefficient of about 19 with a standard error of about 10,826 (statsmodels 0.15.0, verified here). Do not report that coefficient or its odds ratio.
**Alternative / pitfalls:** The sklearn default penalty hides the problem rather than solving it, so you must still ask why the data separates. In real HR data, perfect separation usually means leakage, not insight.
**Likely follow-ups:** 1) *Is a perfect model good news?* Almost never; suspect leakage. 2) *Which fix first?* Check for leakage, then more data or regularisation.
**Common mistakes:** Celebrating 100% accuracy; reporting giant odds ratios; ignoring warnings.

### Q61 ⭐ 🟢 Where can an analyst fit a regression without Python, for example in Excel, and how does that compare with sklearn?
**Asked at:** commonly asked (no company-specific report found); tool-choice questions appear in analyst rounds (unverified).
**What the interviewer is checking:** That you know simple regression is available in everyday tools and know when to move to Python.
**Say this in the interview:** "In Excel I can use the `LINEST` function, a chart trendline, or the Data Analysis ToolPak regression tool for linear regression. It is fine for a quick, one-off model. I move to sklearn or statsmodels when I need train/test checks, logistic regression, many variables, or a repeatable process."
**Explain simply:**
- **Excel (from memory, unverified; not run here)**: `=LINEST(known_ys, known_xs, TRUE, TRUE)` returns slope, intercept and fit statistics; `SLOPE`, `INTERCEPT` and `RSQ` give single values; a scatter chart trendline shows the line and R²; the ToolPak gives a full regression table. Check the exact steps in your version of Excel.
- **Other no-code options (from memory, unverified)**: Power BI and BI tools offer trendlines; Google Sheets has `LINEST`; check the vendor documentation.
- **Python**: reproducible script, train/test splits, regularisation, logistic regression, pipelines, thousands of rows easily.
- Both give the same line for the same simple data.
**Sample data:** Six employees: tenure 1-6 years, salary 32,000 to 52,000.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

employees = pd.DataFrame({
    "tenure_years": [1, 2, 3, 4, 5, 6],
    "salary": [32000, 35000, 41000, 44000, 50000, 52000],
})

model = LinearRegression().fit(employees[["tenure_years"]], employees["salary"])
print("slope:", round(model.coef_[0], 1))
print("intercept:", round(model.intercept_, 1))
print("R2:", round(model.score(employees[["tenure_years"]], employees["salary"]), 3))
```
**Output:**
```text
slope: 4228.6
intercept: 27533.3
R2: 0.986
```
**What it means:** Each extra year of tenure goes with about Rs 4,229 higher salary, and tenure explains 98.6% of the variation in this tiny sample. Excel's `SLOPE` and `INTERCEPT` should return the same two numbers (not run in Excel here).
**Alternative / pitfalls:** Excel handles linear regression easily but logistic regression needs add-ins or workarounds. Manual spreadsheet models are hard to audit and repeat.
**Likely follow-ups:** 1) *Why not Excel always?* Repeatability, scale and validation. 2) *Is a trendline R² a test score?* No, it is training fit.
**Common mistakes:** Believing a trendline equals a validated model; overwriting data in a manual workbook.

### Q62 ⭐ 🟢 What is a baseline model, and why compare your regression against predicting the average?
Illustrative: salaries 30, 40, 50, 60 thousand. What does the mean-only model predict, and what is its RMSE?
**Asked at:** commonly asked (no company-specific report found); baseline comparison is a standard modelling-discipline question (unverified).
**What the interviewer is checking:** That you never judge a model in isolation and that you can compute RMSE by hand.
**Say this in the interview:** "A baseline is the simplest sensible prediction, such as always predicting the average. If my model cannot beat it, it adds no value. Here the mean is 45 thousand and the RMSE is about 11.18 thousand."
**Explain simply:**
- Mean-only model: predict 45 (the average of 30, 40, 50, 60) for everyone.
- RMSE (root mean squared error): square each miss, average them, take the square root; it is a typical miss in the same unit as the target.
- Misses are -15, -5, +5, +15; squares 225, 25, 25, 225; average 125; square root 11.18.
- Any regression must have a lower error than 11.18 to be useful. For classification the baseline is "predict the majority class" or the overall leaver rate.
**Code (what you write in the interview):**
```python
import numpy as np

salaries = np.array([30, 40, 50, 60])  # in thousands

# Baseline model: predict the average salary for everyone
baseline_prediction = salaries.mean()
rmse = np.sqrt(np.mean((salaries - baseline_prediction) ** 2))

print("Baseline prediction:", baseline_prediction)
print("Baseline RMSE:", round(rmse, 2))
```
**Output:**
```text
Baseline prediction: 45.0
Baseline RMSE: 11.18
```
**What it means:** Always guessing 45 thousand is off by about 11 thousand on average. A regression that gets an RMSE of, say, 4 thousand is a real improvement; one at 11 is not.
**Alternative / pitfalls:** The baseline R² is 0 by definition, which links to Q52 (negative R²). Other baselines: last month's value, or the manager's rule of thumb.
**Likely follow-ups:** 1) *Baseline for attrition?* "Nobody leaves" gives high accuracy, so use recall and precision. 2) *What if the model barely beats the baseline?* Keep it simple or stop.
**Common mistakes:** Reporting an RMSE without a reference point; forgetting the root; comparing on training data only.

### Q63 ⭐ 🟢 A model said 0.72 chance of leaving but the employee stayed. Was the model wrong?
**Asked at:** commonly asked (no company-specific report found); this is a judgement question to test probability thinking (unverified).
**What the interviewer is checking:** That you understand a probability is not a prediction of one fixed outcome.
**Say this in the interview:** "Not necessarily. A 0.72 chance also means a 0.28 chance of staying, which is common. One case cannot judge the model. I would look at all employees scored around 0.72: if about 72 in 100 left, the model is calibrated and this person was among the 28 who stayed."
**Explain simply:**
- A probability describes a group: of 100 employees with a 72% score, we expect about 72 to leave and 28 to stay.
- Judging the model needs many cases: compare predicted risk with the real rate (calibration, Q59) and measure AUC or log loss.
- This one case gets a penalty (Brier 0.518, log loss 1.27), but a single penalty means little.
- The stayer may also be a retention success if HR acted on the flag. Then the "miss" is a good outcome.
**Code (what you write in the interview):**
```python
import numpy as np

predicted_risk = 0.72
brier = (predicted_risk - 0) ** 2          # employee stayed (actual = 0)
log_loss = -np.log(1 - predicted_risk)     # penalty for this one case
print("Brier:", round(brier, 3), "log loss:", round(log_loss, 2))
print("Chance of staying the model gave:", round(1 - predicted_risk, 2))
```
**Output:**
```text
Brier: 0.518 log loss: 1.27
Chance of staying the model gave: 0.28
```
**What it means:** The model gave this employee a 28% chance of staying, so staying was not surprising. Say to a manager: "the model is about groups, not individuals; check it across many people".
**Alternative / pitfalls:** If employees scored 0.72 stay far more often than 28%, the model is miscalibrated and needs fixing. Beware that acting on predictions changes the outcomes you later measure.
**Likely follow-ups:** 1) *When is a model wrong?* When predictions across many cases disagree with the real rates. 2) *Would 0.99 and a stay be worse?* Yes, a much larger penalty.
**Common mistakes:** Judging a probabilistic model by one case; treating 0.72 as a promise; ignoring that HR may have intervened.

### Q64 ⭐ 🟢 How is a regression model different from a rule such as 'flag anyone with more than 3 absences' for attrition risk?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you see that a model learns weights from data and gives a graded risk, while a rule is a fixed guess.
**Say this in the interview:** "A rule is a single cut-off someone chose by hand, so it treats 4 absences and 14 the same and ignores everything else. A regression learns from past leavers how much each factor matters and gives each person a probability, so I can rank people and combine absences, overtime and tenure."
**Explain simply:**
- A *feature* is an input column (absences); the *label* is what we predict (left or stayed).
- The rule uses one feature and one cut-off. The model weighs several features together and learns the weights from history.
- The model gives a probability (0 to 1), so you can pick the top 50 people for HR to talk to, instead of an all-or-nothing flag.
- The rule is easy to explain, so it is a fair baseline. A model must beat it on data it has not seen before it is worth the effort.
**Sample data:** 500 simulated employees: `absences`, `overtime_hours`, `tenure_years`, `left` (1 = left).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

rng = np.random.default_rng(42)
n = 500
employees = pd.DataFrame({
    "absences": rng.poisson(3, n),
    "overtime_hours": rng.normal(10, 4, n).round(1),
    "tenure_years": rng.uniform(0.5, 10, n).round(1),
})
risk = -2.5 + 0.25 * employees["absences"] + 0.12 * employees["overtime_hours"] - 0.2 * employees["tenure_years"]
employees["left"] = (rng.random(n) < 1 / (1 + np.exp(-risk))).astype(int)

# The rule: flag anyone with more than 3 absences
rule_flag = (employees["absences"] > 3).astype(int)
print("Rule   precision:", round(precision_score(employees["left"], rule_flag), 2),
      "recall:", round(recall_score(employees["left"], rule_flag), 2))

# The model: a probability for each employee
X = employees[["absences", "overtime_hours", "tenure_years"]]
model = LogisticRegression(max_iter=1000).fit(X, employees["left"])
employees["risk_probability"] = model.predict_proba(X)[:, 1]
same_size = employees.nlargest(rule_flag.sum(), "risk_probability")
print("Rule flags", rule_flag.sum(), "people; the model's top", rule_flag.sum(), "leave rate:", round(same_size["left"].mean(), 2))
print("Rule flagged group leave rate:", round(employees.loc[rule_flag == 1, "left"].mean(), 2))
print("Overall leave rate:", round(employees["left"].mean(), 2))
print(employees.loc[[0,1,2],["absences","overtime_hours","tenure_years","risk_probability"]].round(2))
print(pd.Series(model.coef_[0], index=X.columns).round(2))
```
**Output:**
```text
Rule   precision: 0.31 recall: 0.52
Rule flags 187 people; the model's top 187 leave rate: 0.37
Rule flagged group leave rate: 0.31
Overall leave rate: 0.22
   absences  overtime_hours  tenure_years  risk_probability
0         4             7.8           6.1              0.17
1         4            10.1           7.9              0.15
2         5             9.0           4.1              0.31
absences          0.25
overtime_hours    0.11
tenure_years     -0.21
dtype: float64
```
**What it means:** The rule flags 187 people but only 31% of them leave (22% leave overall). Picking the same number of people by model probability finds 37% leavers. Employees 0 and 1 have the same absences but different risk, because overtime and tenure also count.
**Alternative / pitfalls:** Compare on a test set the model has not seen; I scored on the training data here only to show the idea. Also remember that a high-risk score is not a cause.
**Likely follow-ups:** 1) *Is the rule ever better?* Yes, when it is simple, trusted and nearly as accurate. 2) *Which would you give a manager?* The model's ranking, with the top reasons shown in plain words.
**Common mistakes:** Saying the model is "always more accurate" without testing; judging the rule or model on the same data used to build it.

### Q65 ⭐ 🟡 What is a sklearn Pipeline and why would you use one for regression?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know a Pipeline chains preparation and model so the same steps run on train and test, and that it prevents leakage.
**Say this in the interview:** "A Pipeline bundles the cleaning steps (fill blanks, scale, encode text) and the model into one object. I fit it only on training data, and it applies exactly the same steps to new data, so nothing from the test set leaks into the preparation."
**Explain simply:**
- *Fit* means "learn from data". An imputer learns the median, a scaler learns mean and spread, an encoder learns the categories.
- Without a Pipeline, it is easy to learn these from the whole dataset, so the test rows quietly influence training (leakage).
- One `.fit` and one `.predict` also make the model easy to save and reuse on next month's data.
- `ColumnTransformer` applies different steps to number columns and text columns.
**Sample data:** 300 simulated employees with `experience_years` (some blank), `department` and `salary`.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

rng = np.random.default_rng(42)
n = 300
employees = pd.DataFrame({
    "experience_years": rng.uniform(0, 15, n).round(1),
    "department": rng.choice(["HR", "Sales", "IT"], n),
})
employees.loc[rng.choice(n, 20, replace=False), "experience_years"] = np.nan
dept_bonus = employees["department"].map({"HR": 0, "Sales": 5000, "IT": 12000})
salary = 30000 + 3000 * employees["experience_years"].fillna(7) + dept_bonus + rng.normal(0, 4000, n)

X_train, X_test, y_train, y_test = train_test_split(employees, salary, test_size=0.2, random_state=42)

prep = ColumnTransformer([
    ("numbers", Pipeline([("fill", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), ["experience_years"]),
    ("text", OneHotEncoder(handle_unknown="ignore"), ["department"]),
])
pipe = Pipeline([("prep", prep), ("model", LinearRegression())])
pipe.fit(X_train, y_train)
predictions = pipe.predict(X_test)
print("Test MAE (rupees):", round(mean_absolute_error(y_test, predictions)))
new_hire = pd.DataFrame({"experience_years": [np.nan], "department": ["Finance"]})
print("New hire with missing experience and unseen department:", round(pipe.predict(new_hire)[0]))
```
**Output:**
```text
Test MAE (rupees): 3368
New hire with missing experience and unseen department: 56965
```
**What it means:** The model is off by about 3,400 rupees on average on unseen rows. The new hire has a blank experience and an unknown department, and the pipeline still predicts, because the median fill and `handle_unknown="ignore"` run automatically.
**Alternative / pitfalls:** Scaling is not needed for plain linear regression to predict well, but it helps when you compare coefficients or add Ridge or Lasso. Cross-validating the whole pipeline keeps each fold clean.
**Likely follow-ups:** 1) *Where is leakage without a Pipeline?* Scaling or filling blanks on all data before splitting. 2) *How do you see steps?* `pipe.named_steps`.
**Common mistakes:** Calling `fit_transform` on the test set; forgetting to handle categories not seen in training.

### Q66 ⭐ 🟡 What is a linear probability model, and why do analysts still sometimes use it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the weakness (probabilities outside 0 to 1) and the reasons it is still used.
**Say this in the interview:** "A linear probability model is ordinary linear regression with a 0/1 target. The coefficient reads directly as a change in probability, which managers like. The weakness is that it can predict below 0 or above 1, so I use it for quick, readable effects and logistic regression when I need real probabilities."
**Explain simply:**
- Target is 1 (left) or 0 (stayed); the model fits a straight line through those points.
- Coefficient 0.042 means "each extra overtime hour adds 4.2 percentage points", the same everywhere.
- Real probabilities cannot leave 0 to 1, and the straight line does not respect that at the extremes.
- Analysts, especially in economics, still use it because it is simple, and its average effects are often close to logistic ones for typical values.
**Sample data:** 400 simulated employees: `overtime_hours` (0 to 30) and `left`.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression

rng = np.random.default_rng(42)
n = 400
employees = pd.DataFrame({"overtime_hours": rng.uniform(0, 30, n).round(1)})
p = 1 / (1 + np.exp(-(-4 + 0.25 * employees["overtime_hours"])))
employees["left"] = (rng.random(n) < p).astype(int)

X = employees[["overtime_hours"]]
lpm = LinearRegression().fit(X, employees["left"])
logit = LogisticRegression(max_iter=1000).fit(X, employees["left"])

print("LPM: each extra overtime hour changes probability by", round(lpm.coef_[0], 3))
extremes = pd.DataFrame({"overtime_hours": [0, 15, 30, 45]})
print(pd.DataFrame({
    "overtime_hours": extremes["overtime_hours"],
    "lpm": lpm.predict(extremes).round(2),
    "logistic": logit.predict_proba(extremes)[:, 1].round(2),
}))
```
**Output:**
```text
LPM: each extra overtime hour changes probability by 0.042
   overtime_hours   lpm  logistic
0               0 -0.15      0.01
1              15  0.49      0.47
2              30  1.13      0.99
3              45  1.76      1.00
```
**What it means:** At 0 hours the line predicts -15% and at 30 hours 113%, which is impossible. Logistic stays between 0 and 1. In the middle (15 hours) the two agree (0.49 vs 0.47).
**Alternative / pitfalls:** Errors are not equally spread (heteroscedastic), so use robust standard errors if you report p-values.
**Likely follow-ups:** 1) *Can you clip predictions?* Yes but that is a patch. 2) *When do you prefer logistic?* When predictions near 0 or 1 matter.
**Common mistakes:** Treating predictions as valid probabilities; using it with strong effects and a wide range of inputs.

### Q67 ⭐ 🟡 Why is logistic regression often a good first model in business, including banks and HR teams?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can justify a simple model in business terms (explainable, fast, strong baseline).
**Say this in the interview:** "Logistic regression gives a probability, each coefficient has a clear direction, it trains quickly, and it is hard to overfit with few features. Banks and HR teams must explain decisions to regulators and managers, so a transparent baseline is valuable. Fancier models must beat it to earn a place."
**Explain simply:**
- Each number says whether a factor pushes risk up or down; exponentiating gives an *odds ratio* (a multiplier on the odds).
- It works with modest data and can be checked and audited line by line.
- It is a *baseline*: a simple first model that sets the bar any complex model must clear.
- In regulated settings (credit decisions, hiring), being able to explain a decision matters; this is a general principle, so confirm specific rules with your compliance team.
**Sample data:** 600 simulated employees with `overtime` (0/1), `tenure_years`, `late_marks`, `left`.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(42)
n = 600
employees = pd.DataFrame({
    "overtime": rng.integers(0, 2, n),
    "tenure_years": rng.uniform(0.5, 10, n).round(1),
    "late_marks": rng.poisson(2, n),
})
score = -1.5 + 1.1 * employees["overtime"] - 0.25 * employees["tenure_years"] + 0.2 * employees["late_marks"]
employees["left"] = (rng.random(n) < 1 / (1 + np.exp(-score))).astype(int)

X = employees[["overtime", "tenure_years", "late_marks"]]
model = LogisticRegression(max_iter=1000).fit(X, employees["left"])
odds_ratios = pd.Series(np.exp(model.coef_[0]), index=X.columns).round(2)
print(odds_ratios)
```
**Output:**
```text
overtime        3.20
tenure_years    0.81
late_marks      1.21
dtype: float64
```
**What it means:** Overtime multiplies the odds of leaving by about 3.2; each extra year of tenure lowers them (x0.81); each late mark raises them (x1.21), holding the others fixed.
**Alternative / pitfalls:** It assumes a straight-line effect on log-odds, so it can miss interactions unless you add them. Do not claim the effects are causes.
**Likely follow-ups:** 1) *When would you move on?* If a tree-based model is clearly better on held-out data. 2) *How do you check it?* Test-set AUC and calibration.
**Common mistakes:** Reading odds ratios as "times more likely"; skipping the baseline and jumping to a complex model.

### Q68 ⭐ 🟡 For an HR audience, how would you compare logistic regression with a decision tree on interpretability?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can compare "one number per factor" with "if-then rules" in language HR understands.
**Say this in the interview:** "Logistic regression gives one number per factor, the same effect for everyone, which is compact but needs a bit of statistics to read. A decision tree reads as if-then rules such as 'tenure under 5 years and overtime, then higher risk', which managers grasp instantly, but a deep tree is unstable and overfits."
**Explain simply:**
- Logistic: one *odds ratio* (multiplier on the odds) per feature; effects add up smoothly.
- Tree: splits the staff into groups; each leaf shows the leave rate for that group.
- A small tree is very readable; a big tree is not, and it can change a lot if the data changes slightly.
- Interpretability of a tree depends on depth: keep it 2 to 4 levels.
**Sample data:** 800 simulated employees; 75% train, 25% test.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(42)
n = 800
employees = pd.DataFrame({
    "overtime": rng.integers(0, 2, n),
    "tenure_years": rng.uniform(0.5, 10, n).round(1),
    "late_marks": rng.poisson(2, n),
})
score = -1.5 + 1.1 * employees["overtime"] - 0.25 * employees["tenure_years"] + 0.2 * employees["late_marks"]
employees["left"] = (rng.random(n) < 1 / (1 + np.exp(-score))).astype(int)
features = ["overtime", "tenure_years", "late_marks"]
X_train, X_test, y_train, y_test = train_test_split(employees[features], employees["left"], test_size=0.25, random_state=42)

logit = LogisticRegression(max_iter=1000).fit(X_train, y_train)
print(pd.Series(np.exp(logit.coef_[0]), index=features).round(2))
tree = DecisionTreeClassifier(max_depth=2, random_state=42).fit(X_train, y_train)
print(export_text(tree, feature_names=features, show_weights=True))
print("Test accuracy: logistic", round(logit.score(X_test, y_test), 3), "| tree", round(tree.score(X_test, y_test), 3))
```
**Output:**
```text
overtime        2.76
tenure_years    0.77
late_marks      1.20
dtype: float64
|--- tenure_years <= 4.85
|   |--- overtime <= 0.50
|   |   |--- weights: [121.00, 20.00] class: 0
|   |--- overtime >  0.50
|   |   |--- weights: [91.00, 46.00] class: 0
|--- tenure_years >  4.85
|   |--- tenure_years <= 7.55
|   |   |--- weights: [137.00, 20.00] class: 0
|   |--- tenure_years >  7.55
|   |   |--- weights: [160.00, 5.00] class: 0

Test accuracy: logistic 0.775 | tree 0.77
```
**What it means:** Both reach about 77% accuracy. The tree's worst group (tenure up to 4.85 years with overtime) has 46 leavers out of 137, a 34% leave rate. Every leaf still says "class 0" (stay), because leavers are the minority; read the weights, not just the class.
**Alternative / pitfalls:** Accuracy hides this; for attrition use a probability and a ranking metric. A tree also splits on thresholds you can quote ("under 4.85 years").
**Likely follow-ups:** 1) *Which would you show the CHRO?* A shallow tree picture plus the logistic odds ratios. 2) *Why not a deep tree?* It memorises noise.
**Common mistakes:** Calling a deep tree "interpretable"; reading tree class labels instead of leaf rates.

### Q69 ⭐ 🟡 Should you include gender or age in an attrition or pay regression? Discuss fairness and privacy.
**Asked at:** commonly asked (no company-specific report found); a judgement-based fairness question.
**What the interviewer is checking:** Whether you think about fairness, legality, privacy and purpose before adding sensitive columns.
**Say this in the interview:** "It depends on purpose. For a pay-equity audit I need gender in the model to measure the gap. For a model that decides who gets an opportunity, I would not use gender or age as inputs, and I would check that other columns are not acting as stand-ins for them. I would also confirm legal and privacy rules with HR, legal and IT."
**Explain simply:**
- A *protected attribute* is a trait such as gender, age, religion, caste; using it to make decisions can be unfair and unlawful in many places.
- Removing the column is not enough: a *proxy* (a column that reveals it, like grade or career gap) lets the model learn the same bias.
- Past data may already contain bias (for example women promoted less); a model trained on it repeats it.
- Privacy: collect only what you need, restrict access, anonymise where possible. Privacy law (for example India's DPDP Act, GDPR) is from memory, unverified; confirm with legal.
**Sample data:** 1,000 simulated employees where `grade` is lower for women (built into the simulation).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

rng = np.random.default_rng(42)
n = 1000
employees = pd.DataFrame({
    "gender": rng.integers(0, 2, n),       # 1 = woman (used only to audit)
    "tenure_years": rng.uniform(0.5, 10, n),
})
# Historic pattern: women in this data were promoted less, so show lower "grade"
employees["grade"] = (3 + 0.3 * employees["tenure_years"] - 0.8 * employees["gender"] + rng.normal(0, 0.5, n)).round(1)
employees["overtime_hours"] = rng.normal(10, 4, n)

# Proxy check: can the other columns guess gender even though gender is removed?
others = employees[["tenure_years", "grade", "overtime_hours"]]
proxy_auc = cross_val_score(LogisticRegression(max_iter=1000), others, employees["gender"], cv=5, scoring="roc_auc").mean()
print("AUC of guessing gender from the remaining features:", round(proxy_auc, 2), "(0.5 = cannot guess)")
```
**Output:**
```text
AUC of guessing gender from the remaining features: 0.87 (0.5 = cannot guess)
```
**What it means:** Even with gender removed, the remaining columns guess it with AUC 0.87, so the model could still treat men and women differently. Audit results by group.
**Alternative / pitfalls:** For a pay model, include gender to estimate the gap, but do not use it to set pay. Report group-wise error rates and let a human review.
**Likely follow-ups:** 1) *How do you check fairness?* Compare error rates and predicted risk by group. 2) *Is age ever fine?* As a control in an analysis, not as a decision input; check the local law.
**Common mistakes:** Believing that dropping the column solves it; ignoring consent and data-minimisation.

### Q70 ⭐ 🟡 If you log-transform salary as the target, how do you turn predictions back into rupees and how does interpretation change?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can undo a log transform correctly and read coefficients as percentages.
**Say this in the interview:** "I predict in log units, then take `exp()` to get rupees. The coefficient becomes a percentage change: exp(coef) minus 1. One caveat: exp of the average log is slightly below the average salary, so I can multiply by a smearing factor, the average of exp(residual), to correct it."
**Explain simply:**
- Salary is skewed (a few very high values), so we model `log(salary)`, which is closer to a bell shape.
- Coefficient 0.058 on the log scale means about 6% more salary per extra year (not 0.058 rupees).
- Back-transform with `np.exp(prediction)`; this gives a typical (median-like) salary, not the average.
- The smearing factor (Duan's smearing) corrects most of that gap.
**Sample data:** 300 simulated employees; `experience_years` and `salary` (rupees).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
n = 300
employees = pd.DataFrame({"experience_years": rng.uniform(0, 15, n)})
employees["salary"] = 300000 * np.exp(0.06 * employees["experience_years"] + rng.normal(0, 0.25, n))

X = employees[["experience_years"]]
model = LinearRegression().fit(X, np.log(employees["salary"]))

# Coefficient on the log scale -> percentage change
print("Coefficient:", round(model.coef_[0], 4), "=> about", round((np.exp(model.coef_[0]) - 1) * 100, 1), "% more salary per year")

# Predict in log units, then convert back with exp
new_employee = pd.DataFrame({"experience_years": [5]})
log_prediction = model.predict(new_employee)[0]
print("Naive rupee prediction:", round(np.exp(log_prediction)))

# Smearing: scale by the average of exp(residual) to fix the downward bias
residuals = np.log(employees["salary"]) - model.predict(X)
smearing_factor = np.exp(residuals).mean()
print("Smearing factor:", round(smearing_factor, 3))
print("Adjusted rupee prediction:", round(np.exp(log_prediction) * smearing_factor))
print("Actual average salary of staff with 4.5 to 5.5 years:", round(employees.loc[employees["experience_years"].between(4.5, 5.5), "salary"].mean()))
```
**Output:**
```text
Coefficient: 0.0579 => about 6.0 % more salary per year
Naive rupee prediction: 405308
Smearing factor: 1.032
Adjusted rupee prediction: 418194
Actual average salary of staff with 4.5 to 5.5 years: 421929
```
**What it means:** Each year adds about 6%. For 5 years the naive prediction is Rs 405,308 and the smearing-adjusted one Rs 418,194, closer to the real average of Rs 421,929 for that group.
**Alternative / pitfalls:** Report the percentage, not raw log numbers. Do not compare MAE or R-squared on the log scale with the rupee scale; convert first. It fails if salary can be zero.
**Likely follow-ups:** 1) *Why log salary?* Skew and effects that are percentages. 2) *Log of the feature too?* Then the coefficient is an elasticity.
**Common mistakes:** Forgetting `exp`; saying the coefficient is in rupees; reading 0.058 as 0.058%.

### Q71 ⭐ 🟡 What are influential points and leverage, and how do you spot one in a regression?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you separate "unusual x" (leverage) from "pulls the line" (influence), and can name a diagnostic.
**Say this in the interview:** "Leverage means an unusual input value, like an employee with 25 years of experience when most have under 10. An influential point is one that actually changes the fitted line. I look at Cook's distance: a large value means that removing the point changes the result a lot. I check it, understand it, and never delete it just because it is inconvenient."
**Explain simply:**
- An outlier has an unusual *y* (target); a leverage point has an unusual *x* (input); an influential point is one the model depends on.
- High leverage plus an off-trend y is the dangerous mix.
- *Cook's distance* combines both into one number per row; a common rule of thumb is to look at values above 4 divided by the number of rows.
**Sample data:** 50 simulated employees plus one with 25 years of experience and Rs 9 lakh salary.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

rng = np.random.default_rng(42)
n = 50
employees = pd.DataFrame({"experience_years": rng.uniform(1, 10, n)})
employees["salary_lakh"] = 3 + 0.8 * employees["experience_years"] + rng.normal(0, 0.6, n)
# Add one unusual employee: 25 years of experience, low pay
employees.loc[n] = [25, 9]

X = sm.add_constant(employees[["experience_years"]])
fit = sm.OLS(employees["salary_lakh"], X).fit()
influence = fit.get_influence()

employees["leverage"] = influence.hat_matrix_diag
employees["cooks_d"] = influence.cooks_distance[0]
print(employees.nlargest(3, "cooks_d").round(2))
print("Rule of thumb for Cook's D:", round(4 / len(employees), 2))
print("Slope with the point:", round(fit.params["experience_years"], 3))
without = sm.OLS(employees["salary_lakh"][:-1], X[:-1]).fit()
print("Slope without the point:", round(without.params["experience_years"], 3))
```
**Output:**
```text
    experience_years  salary_lakh  leverage  cooks_d
50             25.00         9.00      0.54    26.31
4               1.85         3.60      0.05     0.06
11              9.34        11.05      0.03     0.04
Rule of thumb for Cook's D: 0.08
Slope with the point: 0.416
Slope without the point: 0.808
```
**What it means:** One row has Cook's D of 26, far above the 0.08 rule of thumb, and it cuts the slope from 0.81 to 0.42 lakh per year. First check whether it is a data error; if real, report results with and without it.
**Alternative / pitfalls:** A plot of residuals against leverage shows the same. Robust regression is an option. Do not drop points silently.
**Likely follow-ups:** 1) *Delete it?* Only if it is an error or outside the population. 2) *What else?* Report both versions.
**Common mistakes:** Confusing outlier with influential point; removing points only to improve R-squared.

### Q72 ⭐ 🟡 Why is an odds ratio not the same as a risk ratio, and when does the difference matter?
**Asked at:** commonly asked (no company-specific report found); odds ratio versus risk is a commonly noted trap in tutorials.
**What the interviewer is checking:** Whether you avoid saying "3 times more likely" for an odds ratio.
**Say this in the interview:** "Risk is a probability: leavers divided by everyone. Odds are leavers divided by stayers. An odds ratio compares odds, a risk ratio compares probabilities. They are close only when the outcome is rare. For common outcomes like 30% attrition, the odds ratio overstates the risk ratio."
**Explain simply:**
- Overtime group: 30 leave, 70 stay. Normal group: 10 leave, 90 stay.
- Risk: 30% vs 10%, so the risk ratio is 3.0. Odds: 30/70 vs 10/90, so the odds ratio is 3.86.
- Logistic regression reports odds ratios, so "overtime has an odds ratio of 3.86" must not be told as "3.86 times as likely".
**Code (what you write in the interview):**
```python
import pandas as pd

# Attrition by overtime: rows are groups, columns are outcomes
left_overtime, stayed_overtime = 30, 70    # 100 employees with overtime
left_normal, stayed_normal = 10, 90        # 100 employees without overtime

risk_overtime = left_overtime / (left_overtime + stayed_overtime)
risk_normal = left_normal / (left_normal + stayed_normal)
odds_overtime = left_overtime / stayed_overtime
odds_normal = left_normal / stayed_normal

print("Risk ratio:", round(risk_overtime / risk_normal, 2))
print("Odds ratio:", round(odds_overtime / odds_normal, 2))

# Same odds ratio, rare outcome: risks are tiny, so OR is close to RR
left_a, left_b = 3, 1
print("Rare case risk ratio:", round((left_a / 100) / (left_b / 100), 2))
print("Rare case odds ratio:", round((left_a / (100 - left_a)) / (left_b / (100 - left_b)), 2))
```
**Output:**
```text
Risk ratio: 3.0
Odds ratio: 3.86
Rare case risk ratio: 3.0
Rare case odds ratio: 3.06
```
**What it means:** With 30% attrition the odds ratio (3.86) is clearly bigger than the risk ratio (3.0). With rare events (3 vs 1 in 100) they are almost the same (3.06 vs 3.0).
**Alternative / pitfalls:** To get risk ratios, report predicted probabilities, or use a model with a log link. When the outcome is common, always translate to probabilities for managers.
**Likely follow-ups:** 1) *When is OR about equal to RR?* Rare outcomes, roughly under 10%. 2) *What would you tell management?* "30% vs 10% leave."
**Common mistakes:** Saying "3.86 times more likely"; using the odds ratio for a common outcome.

### Q73 ⭐ 🟡 What is gradient descent in one minute, and does LinearRegression in sklearn use it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand "step downhill on the error" and know that sklearn's LinearRegression does not need it.
**Say this in the interview:** "Gradient descent starts with a guess for the line, measures the error, and nudges the numbers a small step in the direction that reduces the error, repeating until it stops improving. sklearn's LinearRegression does not use it; it solves least squares directly with linear algebra. Gradient descent is used when no direct solution exists, as in neural nets; for logistic regression some solvers use gradient-style steps."
**Explain simply:**
- Picture walking downhill in fog: feel the slope, take a step, repeat.
- The step size is the *learning rate*.
- For straight-line regression, a direct formula gives the exact best answer, so both methods agree.
- I checked the installed sklearn source: LinearRegression calls `scipy.linalg.lstsq` (a direct least-squares solver).
**Sample data:** 8 employees, experience 1 to 8 years, salary 3.5 to 7.2 lakh.
**Code (what you write in the interview):**
```python
import numpy as np
from sklearn.linear_model import LinearRegression

experience = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
salary_lakh = np.array([3.5, 4.1, 4.4, 5.2, 5.4, 6.1, 6.4, 7.2])

# Gradient descent for salary = intercept + slope * experience
intercept, slope = 0.0, 0.0
learning_rate = 0.02
for step in range(20000):
    error = (intercept + slope * experience) - salary_lakh
    intercept -= learning_rate * error.mean()
    slope -= learning_rate * (error * experience).mean()
print("Gradient descent:", round(intercept, 3), round(slope, 3))

model = LinearRegression().fit(experience.reshape(-1, 1), salary_lakh)
print("sklearn LinearRegression:", round(model.intercept_, 3), round(model.coef_[0], 3))
```
**Output:**
```text
Gradient descent: 3.0 0.508
sklearn LinearRegression: 3.0 0.508
```
**What it means:** The slow, step-by-step method lands on the same line (3.0 + 0.508 per year) as sklearn's direct answer.
**Alternative / pitfalls:** SGDRegressor and SGDClassifier in sklearn do use gradient steps. Scale the features first or the steps behave badly.
**Likely follow-ups:** 1) *What is the learning rate?* Step size. 2) *Why use it at all?* Huge data or models without a formula.
**Common mistakes:** Saying LinearRegression runs gradient descent; skipping feature scaling.

### Q74 ⭐ 🟡 How would you report a logistic regression to management using predicted probabilities instead of odds ratios?
Illustrative model: baseline probability 10% for no overtime, odds ratio 3.0 for overtime. Compute the probability for overtime employees.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can convert odds ratios into probabilities that a manager understands.
**Say this in the interview:** "I convert probability to odds, multiply by the odds ratio, and convert back. A 10% baseline is odds of 0.111; times 3 gives 0.333; that is a 25% probability. So I tell management: about 10% of staff without overtime leave versus about 25% with overtime."
**Explain simply:**
- Odds = p divided by (1 minus p). Probability = odds divided by (1 plus odds).
- Odds ratio 3 does not mean probability triples: 10% becomes 25%, a risk ratio of 2.5.
- The same odds ratio gives different jumps from different starting points, so always state the baseline.
**Code (what you write in the interview):**
```python
baseline_probability = 0.10
odds_ratio = 3.0

baseline_odds = baseline_probability / (1 - baseline_probability)
overtime_odds = baseline_odds * odds_ratio
overtime_probability = overtime_odds / (1 + overtime_odds)

print("Baseline odds:", round(baseline_odds, 3))
print("Overtime odds:", round(overtime_odds, 3))
print("Overtime probability:", round(overtime_probability, 3))
print("Risk ratio:", round(overtime_probability / baseline_probability, 2))

# The same odds ratio from a different starting point
for baseline in [0.02, 0.10, 0.30, 0.60]:
    odds = baseline / (1 - baseline) * odds_ratio
    print(baseline, "->", round(odds / (1 + odds), 3))
```
**Output:**
```text
Baseline odds: 0.111
Overtime odds: 0.333
Overtime probability: 0.25
Risk ratio: 2.5
0.02 -> 0.058
0.1 -> 0.25
0.3 -> 0.563
0.6 -> 0.818
```
**What it means:** Overtime employees have a 25% leave probability (versus 10%), a 15 point increase. From a 2% baseline, the same odds ratio only gives 5.8%; from 60% it gives 81.8%.
**Alternative / pitfalls:** In a fitted model, use `predict_proba` for typical employee profiles, and show a small table of "no overtime vs overtime".
**Likely follow-ups:** 1) *Why not just show the odds ratio?* Managers misread it. 2) *What is the absolute effect?* 15 percentage points here.
**Common mistakes:** Multiplying the probability by 3 (giving 30%); omitting the baseline.

### Q75 ⭐ 🟡 What is an elastic net, and when might it beat Ridge or Lasso alone?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know it blends the Ridge and Lasso penalties and handles groups of correlated features.
**Say this in the interview:** "Ridge shrinks all coefficients and keeps every feature. Lasso shrinks some to exactly zero, so it selects features, but with a group of near-duplicate features it tends to pick one arbitrarily. Elastic net mixes both penalties: it can drop useless features and still share weight across correlated ones. I let cross-validation choose the strength and the mix."
**Explain simply:**
- A *penalty* discourages big coefficients, reducing overfitting (memorising noise).
- `l1_ratio` in sklearn sets the mix: 1 is Lasso, close to 0 is Ridge.
- It tends to help when features are correlated, such as base pay, gross pay and CTC, plus many useless columns.
**Sample data:** 150 simulated rows; three near-duplicate pay columns and 7 noise columns; target depends on pay.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNetCV, LassoCV, RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(42)
n = 150
base = rng.normal(size=n)
# Three near-duplicate pay-related features, plus noise features
X = pd.DataFrame({
    "base_pay": base + rng.normal(0, 0.1, n),
    "gross_pay": base + rng.normal(0, 0.1, n),
    "ctc": base + rng.normal(0, 0.1, n),
    **{f"noise_{i}": rng.normal(size=n) for i in range(1, 8)},
})
y = 3 * base + rng.normal(0, 1, n)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

models = {
    "Ridge": make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-2, 2, 30))),
    "Lasso": make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=42)),
    "ElasticNet": make_pipeline(StandardScaler(), ElasticNetCV(l1_ratio=[0.2, 0.5, 0.8], cv=5, random_state=42)),
}
for name, model in models.items():
    model.fit(X_train, y_train)
    coefficients = pd.Series(model[-1].coef_, index=X.columns).round(2)
    print(name, "| test R2:", round(model.score(X_test, y_test), 3))
    print("  pay features:", coefficients[["base_pay", "gross_pay", "ctc"]].tolist(),
          "| noise features kept:", int((coefficients.filter(like="noise") != 0).sum()))
```
**Output:**
```text
Ridge | test R2: 0.861
  pay features: [0.81, 0.84, 0.82] | noise features kept: 7
Lasso | test R2: 0.876
  pay features: [0.62, 0.99, 0.77] | noise features kept: 0
ElasticNet | test R2: 0.874
  pay features: [0.74, 0.83, 0.78] | noise features kept: 0
```
**What it means:** Ridge keeps all 7 noise columns; Lasso and elastic net drop all of them. Lasso weights the three pay columns unevenly (0.62, 0.99, 0.77) while elastic net spreads them more evenly (0.74, 0.83, 0.78). On this small sample the test R-squared is almost the same for Lasso and elastic net (0.876 vs 0.874), so the gain here is stability, not accuracy.
**Alternative / pitfalls:** Scale features first. Do not claim elastic net always wins; compare by cross-validation.
**Likely follow-ups:** 1) *What if all features matter?* Ridge. 2) *What if only a few matter?* Lasso.
**Common mistakes:** Forgetting to scale; tuning on the test set.

### Q76 ⭐ 🟡 How do you check a logistic regression model for multicollinearity, and does it matter if you only want predictions?
**Asked at:** commonly asked (no company-specific report found); multicollinearity and VIF appear in common question banks.
**What the interviewer is checking:** That you can detect it (VIF, correlations) and know it hurts interpretation more than prediction.
**Say this in the interview:** "Multicollinearity means two inputs carry nearly the same information, like age and tenure. I check correlations and VIF (variance inflation factor); above about 5 to 10 is a warning. For pure prediction it usually does not matter, but the coefficients become unstable and hard to interpret, so if I explain drivers I drop or combine one."
**Explain simply:**
- VIF says how much a coefficient's uncertainty is inflated because that feature can be predicted from the others. 1 means none.
- With correlated inputs, the model cannot tell which one deserves the credit, so the coefficients swing.
- Predictions stay fine if new data keeps the same correlation pattern.
**Sample data:** 500 simulated employees; `tenure_years` is closely tied to `age`.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

rng = np.random.default_rng(42)
n = 500
age = rng.uniform(22, 58, n)
employees = pd.DataFrame({
    "age": age,
    "tenure_years": (age - 22) * 0.7 + rng.normal(0, 1.5, n),
    "overtime_hours": rng.normal(10, 4, n),
})
score = -1 + 0.1 * employees["overtime_hours"] - 0.1 * employees["tenure_years"]
employees["left"] = (rng.random(n) < 1 / (1 + np.exp(-score))).astype(int)

X = sm.add_constant(employees[["age", "tenure_years", "overtime_hours"]])
vif = pd.Series([variance_inflation_factor(X.values, i) for i in range(1, X.shape[1])],
                index=["age", "tenure_years", "overtime_hours"]).round(1)
print(vif)

# Dropping age: coefficients on the other features become stabler
for features in (["age", "tenure_years", "overtime_hours"], ["tenure_years", "overtime_hours"]):
    fit = sm.Logit(employees["left"], sm.add_constant(employees[features])).fit(disp=0)
    print(features, "-> tenure coef", round(fit.params["tenure_years"], 3), "std err", round(fit.bse["tenure_years"], 3))
```
**Output:**
```text
age               23.1
tenure_years      23.1
overtime_hours     1.0
dtype: float64
['age', 'tenure_years', 'overtime_hours'] -> tenure coef -0.118 std err 0.073
['tenure_years', 'overtime_hours'] -> tenure coef -0.117 std err 0.017
```
**What it means:** Age and tenure have VIF 23. With both in, the tenure coefficient has a standard error of 0.073; drop age and it falls to 0.017, with the same coefficient (-0.12). The estimate was not wrong, just shaky.
**Alternative / pitfalls:** Ridge or Lasso handle it for prediction. Do not drop a feature just for a high VIF if it matters for the business question; combine instead.
**Likely follow-ups:** 1) *Does it reduce accuracy?* Usually not. 2) *Dummy variables?* Drop one category to avoid perfect collinearity.
**Common mistakes:** Saying it always breaks predictions; dropping the wrong variable.

### Q77 ⭐ 🟡 What does `max_iter` do in LogisticRegression, and what does a ConvergenceWarning tell you?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the solver is iterative and what to do when it stops early.
**Say this in the interview:** "LogisticRegression finds its coefficients in repeated steps, and `max_iter` is the maximum number of steps, 100 by default. A ConvergenceWarning means it hit that limit before settling, so the coefficients may not be final. First I scale the features; if the warning remains, I raise `max_iter`."
**Explain simply:**
- The solver (default `lbfgs`) improves the numbers step by step until changes become tiny.
- Features on very different scales (salary in lakhs versus hours) make the steps slow.
- Scaling usually fixes it; a larger `max_iter` is the second fix; a stronger penalty (smaller `C`) also helps.
- Ignoring the warning risks wrong coefficients.
**Sample data:** 500 simulated employees: annual salary (about 720,000), overtime hours, experience months, `left`.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)
n = 500
employees = pd.DataFrame({
    "annual_salary": rng.normal(720000, 180000, n),
    "overtime_hours": rng.normal(10, 4, n),
    "experience_months": rng.uniform(6, 120, n),
})
risk = 5 * (0.15 * (employees["overtime_hours"] - 10)
            - 0.0000015 * (employees["annual_salary"] - 720000)
            + 0.01 * (employees["experience_months"] - 60))
rng = np.random.default_rng(1)
left = (rng.random(n) < 1 / (1 + np.exp(-risk))).astype(int)

# Raw features on very different scales: the solver runs out of its 100 steps
model = LogisticRegression()
model.fit(employees, left)
print("Iterations used:", model.n_iter_[0], "of", model.max_iter)

# Fix: put features on a similar scale first
scaled_model = make_pipeline(StandardScaler(), LogisticRegression())
scaled_model.fit(employees, left)
print("Scaled: iterations used:", scaled_model[-1].n_iter_[0])
```
**Output:**
```text
Iterations used: 100 of 100
Scaled: iterations used: 7
```
**What it means:** On raw columns it used all 100 steps and sklearn printed a ConvergenceWarning (on the error stream, not shown above). After scaling it settled in 7 steps. (This warning depends on the data and seed; many datasets converge without it.)
**Alternative / pitfalls:** Check `n_iter_` to see steps used. Very perfectly separable data can also fail to settle.
**Likely follow-ups:** 1) *Is raising max_iter always safe?* It treats the symptom, scaling treats the cause. 2) *Other solvers?* Yes, e.g. `liblinear`, `saga`.
**Common mistakes:** Hiding the warning; setting `max_iter` huge without scaling.

### Q78 ⭐ 🔴 What is Poisson regression, and when would you use it for a count target such as leaves taken per employee?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** Whether you pick the right model for counts and know the mean-equals-variance assumption.
**Say this in the interview:** "Poisson regression is for non-negative whole-number counts, like leaves taken in a year. It models the log of the expected count, so coefficients are multipliers: a rate ratio of 1.65 means 65% more leaves. It assumes the variance roughly equals the mean; if the variance is much larger (overdispersion), I switch to negative binomial."
**Explain simply:**
- Plain linear regression can predict negative leaves; Poisson cannot.
- exp(coefficient) is the *rate ratio*, the multiplier on the expected count.
- Check mean versus variance of the counts; a big gap signals overdispersion.
- If employees are observed for different lengths of time, include an exposure or offset (months worked).
**Sample data:** 400 simulated employees: `age`, `night_shift` (0/1), `leaves_taken`.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

rng = np.random.default_rng(42)
n = 400
employees = pd.DataFrame({
    "age": rng.integers(22, 58, n),
    "night_shift": rng.integers(0, 2, n),
})
expected_leaves = np.exp(0.8 + 0.01 * (employees["age"] - 40) + 0.4 * employees["night_shift"])
employees["leaves_taken"] = rng.poisson(expected_leaves)

fit = smf.glm("leaves_taken ~ age + night_shift", data=employees, family=sm.families.Poisson()).fit()
print(fit.params.round(3))
print("Rate ratio for night shift:", round(np.exp(fit.params["night_shift"]), 2))
print("Mean:", round(employees["leaves_taken"].mean(), 2), "Variance:", round(employees["leaves_taken"].var(), 2))
print("Predicted leaves for a 40-year-old on night shift:",
      round(fit.predict(pd.DataFrame({"age": [40], "night_shift": [1]}))[0], 2))
```
**Output:**
```text
Intercept      0.257
age            0.013
night_shift    0.498
dtype: float64
Rate ratio for night shift: 1.65
Mean: 2.87 Variance: 3.46
Predicted leaves for a 40-year-old on night shift: 3.51
```
**What it means:** Night-shift staff take about 1.65 times as many leaves (about 65% more), other things equal. A 40-year-old on night shift is expected to take 3.5 leaves. Mean 2.87 against variance 3.46 is only mildly overdispersed.
**Alternative / pitfalls:** Excess zeros need zero-inflated models (from memory). Counts per employee with different tenure need an offset.
**Likely follow-ups:** 1) *Why not linear regression?* Negative predictions, wrong error shape. 2) *Which if variance is too big?* Negative binomial.
**Common mistakes:** Using it for rates without exposure; ignoring overdispersion.

### Q79 ⭐ 🔴 What is the difference between a coefficient and a marginal effect (change in probability) in logistic regression, and why does the effect vary by employee?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** Whether you know the coefficient is on log-odds while the change in probability depends on where you start.
**Say this in the interview:** "The coefficient is the effect on log-odds, which is the same for everyone. The marginal effect is the change in probability for a small increase in the feature, and it equals the coefficient times p times (1 minus p), so it is largest for people near 50% risk and small for those near 0% or 100%. I report the average marginal effect."
**Explain simply:**
- The probability curve is S-shaped: steep in the middle, flat at the ends.
- So one extra overtime hour moves a 50% employee a lot, and a 5% employee only a little.
- The *average marginal effect* averages that over all employees: one number in percentage points.
**Sample data:** 800 simulated employees: `overtime_hours`, `tenure_years`, `left`.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

rng = np.random.default_rng(42)
n = 800
employees = pd.DataFrame({
    "overtime_hours": rng.normal(10, 4, n),
    "tenure_years": rng.uniform(0.5, 10, n),
})
score = -2.2 + 0.18 * employees["overtime_hours"] - 0.3 * employees["tenure_years"]
employees["left"] = (rng.random(n) < 1 / (1 + np.exp(-score))).astype(int)

X = sm.add_constant(employees[["overtime_hours", "tenure_years"]])
fit = sm.Logit(employees["left"], X).fit(disp=0)
print("Coefficient on overtime (log-odds):", round(fit.params["overtime_hours"], 3))

# Average marginal effect: change in probability per extra overtime hour, averaged over everyone
print(fit.get_margeff().summary_frame().round(4))

# The effect differs by employee
probability = fit.predict(X)
effect_per_person = fit.params["overtime_hours"] * probability * (1 - probability)
print("Smallest, average, largest effect:", effect_per_person.min().round(4), effect_per_person.mean().round(4), effect_per_person.max().round(4))
for p in (0.05, 0.50, 0.95):
    print("Baseline probability", p, "-> effect of one more hour:", round(fit.params["overtime_hours"] * p * (1 - p), 4))
```
**Output:**
```text
Coefficient on overtime (log-odds): 0.203
                 dy/dx  Std. Err.  ...  Conf. Int. Low  Cont. Int. Hi.
overtime_hours  0.0226     0.0031  ...          0.0166          0.0286
tenure_years   -0.0421     0.0045  ...         -0.0509         -0.0333

[2 rows x 6 columns]
Smallest, average, largest effect: 0.0004 0.0226 0.0506
Baseline probability 0.05 -> effect of one more hour: 0.0096
Baseline probability 0.5 -> effect of one more hour: 0.0506
Baseline probability 0.95 -> effect of one more hour: 0.0096
```
**What it means:** The coefficient is 0.203 (log-odds), but on average one more overtime hour adds about 2.3 percentage points to leave probability. It ranges from 0.04 points for the safest to 5.1 points for people at 50% risk. At a baseline of 5% or 95%, it is about 1 point.
**Alternative / pitfalls:** You can also report the marginal effect at typical profiles. In a linear model, the coefficient and the marginal effect are the same.
**Likely follow-ups:** 1) *Why does it vary?* The S-curve. 2) *Max effect?* At p = 0.5, a quarter of the coefficient.
**Common mistakes:** Quoting the coefficient as a percentage-point change.

### Q80 ⭐ 🔴 What happens in linear regression when you have more features than rows, and what do you do?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know many columns and few rows lets the model memorise, and the fixes.
**Say this in the interview:** "With more features than rows, plain least squares has infinite exact solutions. It fits the training data perfectly (R-squared 1.0) by memorising noise and predicts badly on new data. I fix it by regularising (Ridge or Lasso), selecting or reducing features, or getting more data, and I always judge on a held-out test set."
**Explain simply:**
- 100 features and 30 rows: the model can match every training row exactly, even with random columns.
- *Overfitting* means high training score but poor performance on new data.
- Ridge shrinks coefficients; Lasso switches many off; both restrict the model.
- Other options: domain-based feature selection, PCA, or collect more rows.
**Sample data:** 30 training rows, 100 features, 100 test rows; only 2 features truly matter.
**Code (what you write in the interview):**
```python
import numpy as np
from sklearn.linear_model import Lasso, LinearRegression, Ridge

rng = np.random.default_rng(42)
n_rows, n_features = 30, 100
X = rng.normal(size=(n_rows + 100, n_features))
y = 2 * X[:, 0] - 1.5 * X[:, 1] + rng.normal(0, 1, n_rows + 100)
X_train, y_train = X[:n_rows], y[:n_rows]
X_test, y_test = X[n_rows:], y[n_rows:]

plain = LinearRegression().fit(X_train, y_train)
print("Plain regression: train R2", round(plain.score(X_train, y_train), 3), "test R2", round(plain.score(X_test, y_test), 3))

ridge = Ridge(alpha=10).fit(X_train, y_train)
print("Ridge:            train R2", round(ridge.score(X_train, y_train), 3), "test R2", round(ridge.score(X_test, y_test), 3))

# Lasso also switches off most features (useful when only a few matter)
lasso = Lasso(alpha=0.3).fit(X_train, y_train)
print("Lasso:            train R2", round(lasso.score(X_train, y_train), 3), "test R2", round(lasso.score(X_test, y_test), 3),
      "| features kept:", int((lasso.coef_ != 0).sum()))
```
**Output:**
```text
Plain regression: train R2 1.0 test R2 0.104
Ridge:            train R2 0.986 test R2 0.134
Lasso:            train R2 0.861 test R2 0.799 | features kept: 8
```
**What it means:** Plain regression scores 1.0 on training but only 0.10 on new rows. Lasso keeps 8 features and scores 0.80 on new rows. Ridge helps little here (0.13) because most coefficients still stay nonzero.
**Alternative / pitfalls:** Choose alpha with cross-validation rather than by hand (the values here were picked for illustration).
**Likely follow-ups:** 1) *Does sklearn raise an error?* No, it returns a solution. 2) *Which regulariser?* Lasso if few features matter.
**Common mistakes:** Trusting the training R-squared; adding more columns to "improve" the fit.

### Q81 ⭐ 🔴 How would you detect and handle data leakage caused by time, for example using future information in a churn model?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** That you respect time: train on the past, test on the future, and only use information available at prediction time.
**Say this in the interview:** "Time leakage means the model sees information from after the prediction moment, for example a cancellation-call count recorded after the customer left. It gives a suspiciously great test score and fails live. I ask for each feature, 'would I know this on the day I predict?', split train and test by date, and be suspicious of any score that looks too good."
**Explain simply:**
- Predicting churn next month: features must be known at the end of this month.
- A random split mixes future and past rows, which can flatter the model; split by date instead.
- Red flags: a single feature with huge importance, test scores far above what is plausible.
- Fix: remove the feature, rebuild features as of a snapshot date, use a time-based or rolling validation.
**Sample data:** 3,000 simulated customers with a snapshot month, order and app activity, and one leaky column recorded after the churn.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(42)
n = 3000
customers = pd.DataFrame({
    "snapshot_month": rng.integers(1, 13, n),
    "orders_last_3m": rng.poisson(4, n),
    "app_sessions": rng.poisson(10, n),
})
churn_score = -1 - 0.2 * customers["orders_last_3m"] + 0.02 * (10 - customers["app_sessions"]) + rng.normal(0, 0.5, n)
customers["churned"] = (rng.random(n) < 1 / (1 + np.exp(-churn_score))).astype(int)
# Leaky feature: support ticket count recorded AFTER the customer already cancelled
customers["cancel_calls_next_month"] = customers["churned"] * rng.poisson(2, n) + rng.poisson(0.1, n)

def evaluate(features, split):
    train, test = split
    model = LogisticRegression(max_iter=1000).fit(train[features], train["churned"])
    return round(roc_auc_score(test["churned"], model.predict_proba(test[features])[:, 1]), 3)

time_split = (customers[customers["snapshot_month"] <= 9], customers[customers["snapshot_month"] > 9])

clean = ["orders_last_3m", "app_sessions"]
leaky = clean + ["cancel_calls_next_month"]
print("AUC with leaky feature :", evaluate(leaky, time_split))
print("AUC without leaky feature:", evaluate(clean, time_split))
```
**Output:**
```text
AUC with leaky feature : 0.929
AUC without leaky feature: 0.58
```
**What it means:** With the leaky feature the AUC looks excellent (0.93); without it, the honest AUC is 0.58. Report the honest one.
**Alternative / pitfalls:** Also watch for leakage from targets encoded into features, and from fitting scalers on all data. Your first evidence is a too-good score.
**Likely follow-ups:** 1) *Example in HR?* Exit-interview scores used to predict attrition. 2) *Validation method?* Train on early months, test on later ones.
**Common mistakes:** Random splits on time data; blaming the model instead of checking features.

### Q82 ⭐ 🔴 What is the learning rate in gradient-based fitting of logistic regression, and what goes wrong if it is too big?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** That you understand the step size in gradient descent and the trade-off.
**Say this in the interview:** "The learning rate is the size of each step the optimiser takes while improving the coefficients. Too small and it is painfully slow; too large and it overshoots the best point, bouncing around or getting worse. sklearn's LogisticRegression default solver has no learning rate to set; it is in SGDClassifier as `eta0`, and in deep-learning tools."
**Explain simply:**
- Walking downhill: tiny steps take forever; giant leaps jump over the valley.
- Log loss is the error measure for logistic regression: lower is better.
- Feature scaling makes one learning rate work for all features.
**Sample data:** 8 employees, one scaled overtime feature and `left`; 200 steps per run.
**Code (what you write in the interview):**
```python
import numpy as np

# Tiny logistic regression by gradient descent: one feature (overtime hours, scaled), one coefficient
overtime = np.array([-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0])
left = np.array([0, 0, 0, 0, 1, 0, 1, 1])

def fit(learning_rate, steps=200):
    weight, bias = 0.0, 0.0
    for step in range(steps):
        probability = 1 / (1 + np.exp(-(weight * overtime + bias)))
        weight -= learning_rate * ((probability - left) * overtime).mean()
        bias -= learning_rate * (probability - left).mean()
    probability = np.clip(1 / (1 + np.exp(-(weight * overtime + bias))), 1e-9, 1 - 1e-9)
    loss = -(left * np.log(probability) + (1 - left) * np.log(1 - probability)).mean()
    return round(float(weight), 2), round(float(loss), 3)

for learning_rate in [0.01, 0.5, 5, 500]:
    print("learning rate", learning_rate, "-> weight, log loss:", fit(learning_rate))
```
**Output:**
```text
learning rate 0.01 -> weight, log loss: (0.56, 0.505)
learning rate 0.5 -> weight, log loss: (2.45, 0.312)
learning rate 5 -> weight, log loss: (2.52, 0.312)
learning rate 500 -> weight, log loss: (93.86, 5.181)
```
**What it means:** At 0.01, 200 steps are not enough (loss 0.505). At 0.5 and 5 the fit reaches the best loss (0.312). At 500 the coefficient is thrown to 93.9 and the loss is 5.18, much worse: it diverged.
**Alternative / pitfalls:** Use a decaying learning rate or adaptive optimisers (from memory). Check the loss curve falls smoothly. I confirmed `eta0` exists in `SGDClassifier`.
**Likely follow-ups:** 1) *How do you choose it?* Try values on a log scale and watch the loss. 2) *Convergence warning?* Often scale or step issues.
**Common mistakes:** Assuming bigger is faster; not scaling features.

### Q83 ⭐ 🔴 Your logistic regression is accurate on training data but poor on new months. List causes and your first three checks.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A calm diagnostic order: overfitting, drift, leakage, process change.
**Say this in the interview:** "Good on training and poor on new months means it learned something that does not hold later. My causes: overfitting, leakage in training, drift (customers or policies changed), a data pipeline change, or label delay. My first three checks: one, compare train, validation and recent-month scores; two, check by month whether performance or the input distribution shifted; three, review features for leakage and for changed definitions."
**Explain simply:**
- *Overfitting*: too many features for the data, memorised noise.
- *Drift*: the world changed, so old patterns stop working (a new discount policy, a new hiring mix).
- *Leakage*: training used information not available at prediction time.
- *Data issue*: a column changed meaning or has more blanks.
- Check each month on its own, because one pooled score hides the drop.
**Sample data:** 4,000 simulated customers over 8 months; a policy change from month 7 stops discounts protecting customers.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(42)
n = 4000
customers = pd.DataFrame({
    "month": np.repeat(np.arange(1, 9), n // 8),
    "orders_last_3m": rng.poisson(4, n),
    "discount_used": rng.integers(0, 2, n),
})
# From month 7 a new policy: discounts stop protecting customers from churn
effect = np.where(customers["month"] <= 6, -1.2, 0.0)
score = 0.2 - 0.25 * customers["orders_last_3m"] + effect * customers["discount_used"]
customers["churned"] = (rng.random(n) < 1 / (1 + np.exp(-score))).astype(int)

features = ["orders_last_3m", "discount_used"]
train = customers[customers["month"] <= 5]
model = LogisticRegression(max_iter=1000).fit(train[features], train["churned"])

# Check 1: score each month separately, not one pooled number
for month in range(1, 9):
    rows = customers[customers["month"] == month]
    auc = roc_auc_score(rows["churned"], model.predict_proba(rows[features])[:, 1])
    print("month", month, "AUC:", round(auc, 3), "| predicted churn:", round(model.predict_proba(rows[features])[:, 1].mean(), 3),
          "| actual churn:", round(rows["churned"].mean(), 3))
```
**Output:**
```text
month 1 AUC: 0.721 | predicted churn: 0.225 | actual churn: 0.226
month 2 AUC: 0.729 | predicted churn: 0.22 | actual churn: 0.198
month 3 AUC: 0.713 | predicted churn: 0.217 | actual churn: 0.22
month 4 AUC: 0.659 | predicted churn: 0.217 | actual churn: 0.22
month 5 AUC: 0.685 | predicted churn: 0.223 | actual churn: 0.238
month 6 AUC: 0.715 | predicted churn: 0.227 | actual churn: 0.244
month 7 AUC: 0.562 | predicted churn: 0.225 | actual churn: 0.316
month 8 AUC: 0.583 | predicted churn: 0.219 | actual churn: 0.324
```
**What it means:** AUC is about 0.66 to 0.73 in months 1 to 6, then falls to 0.56 and 0.58. The model predicts about 22% churn, but actual churn rises to 32%. That is drift, not bad luck, so refit on recent data and monitor monthly.
**Alternative / pitfalls:** Do not just retrain blindly; first find what changed. Keep a time-based test set.
**Likely follow-ups:** 1) *Overfit or drift?* Overfit shows in train vs validation; drift shows in time. 2) *Fix?* Simplify, remove leaks, retrain, monitor.
**Common mistakes:** Reporting one overall metric; retraining before diagnosing.

### Q84 ⭐ 🔴 How would you compare two logistic regression models, one with 5 features and one with 12, to decide which to deploy?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you compare on unseen data and prefer the simpler model unless the bigger one clearly wins.
**Say this in the interview:** "I compare both with cross-validation on the same folds, using the metric that matches the business goal such as AUC, and look at the spread, not just the average. I also look at AIC, which penalises extra features, and at stability, explainability and cost to maintain. If the 12-feature model is not clearly better, I deploy the 5-feature one."
**Explain simply:**
- *Cross-validation* splits the data into folds, trains on some and tests on the rest, rotating so every row is tested once.
- More features always improve training scores, so training score is not a fair comparison.
- *AIC* (lower is better) trades fit against number of features.
- Also compare on a later time period and check calibration (do predicted 20% match actual 20%?).
**Sample data:** 1,500 simulated employees, 12 features, only the first 5 really matter.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)
n = 1500
employees = pd.DataFrame(rng.normal(size=(n, 12)), columns=[f"f{i}" for i in range(1, 13)])
score = -1.2 + 0.9 * employees["f1"] - 0.7 * employees["f2"] + 0.5 * employees["f3"] + 0.3 * employees["f4"] - 0.3 * employees["f5"] + 0.05 * employees["f6"]
employees["left"] = (rng.random(n) < 1 / (1 + np.exp(-score))).astype(int)

small = [f"f{i}" for i in range(1, 6)]
large = [f"f{i}" for i in range(1, 13)]
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for name, features in [("5 features", small), ("12 features", large)]:
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    auc = cross_val_score(model, employees[features], employees["left"], cv=cv, scoring="roc_auc")
    aic = sm.Logit(employees["left"], sm.add_constant(employees[features])).fit(disp=0).aic
    print(name, "| CV AUC mean:", round(auc.mean(), 3), "std:", round(auc.std(), 3), "| AIC:", round(aic, 1))
```
**Output:**
```text
5 features | CV AUC mean: 0.762 std: 0.012 | AIC: 1510.8
12 features | CV AUC mean: 0.755 std: 0.011 | AIC: 1522.8
```
**What it means:** The 5-feature model is slightly better on both (AUC 0.762 vs 0.755; AIC 1510.8 vs 1522.8), and the AUC gap is smaller than one fold spread. Report: "Deploy the simpler model; the extra 7 features add no measurable value."
**Alternative / pitfalls:** If the larger model wins only slightly, choose by simplicity and data quality. Never choose using the test set repeatedly. Check performance by month before deployment.
**Likely follow-ups:** 1) *Why not pick the highest training score?* It rewards overfitting. 2) *Other metrics?* Recall at a fixed alert budget, calibration.
**Common mistakes:** Comparing on training data; picking by a 0.001 difference.

