# Book 5 — Statistics & Maths for Data Analysts | Part 7: Correlation vs Causation, Regression Basics, R² 🟡

**Target:** 50 questions | **Actual:** 54 questions
**Scope:** correlation and its limits, confounders and causation, simple and multiple linear regression, interpreting coefficients, R² and adjusted R², regression diagnostics for analysts.

### Q1 ⭐⭐⭐ 🟢 What is the difference between correlation and causation?
**Asked at:** Tiger Analytics business analyst (one candidate-reported item pairing correlation vs causation with p-values, via an Interview Query search summary; not opened); also a standard prompt on practice platforms (Dataford). No other company-specific report found.
**What the interviewer is checking:** Whether you avoid the classic trap of saying "A moves with B, so A causes B".
**Say this in the interview:** "Correlation means two things move together. Causation means a change in one actually produces a change in the other. Correlation is only a clue; to claim causation I need to rule out other explanations, ideally with an experiment."
**Explain simply:**
- *Correlation* is a number that describes how two columns rise and fall together. It says nothing about why.
- *Causation* means that if you changed A on purpose, B would change as a result.
- Three things can create a correlation without causation: a hidden third factor (a *confounder*), the arrow pointing the other way (*reverse causation*), or pure coincidence.
- Randomised experiments (A/B tests) are the strongest way to prove causation.
**Worked example:** In a 300-employee dataset I simulated, training hours and engagement scores correlate at r = 0.68. But tenure drives both (long-serving people get more training and are more engaged). Once tenure is included in the model, the training effect falls from +1.73 points per hour to -0.10 (p = 0.62), meaning no real effect. The correlation was real; the causation was not. (Data is simulated, with the true training effect set to zero.)
**Likely follow-ups:**
- *How would you prove causation?* Run a randomised trial, or use careful controls and say clearly the result is suggestive.
- *Is correlation useless then?* No, it is great for prediction and for deciding what to investigate.
**Common mistakes:** Writing "X causes Y" in a report because r is high; thinking a low p-value proves causation.

### Q2 ⭐⭐⭐ 🟢 What is correlation, and what does the correlation coefficient (r) tell you?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know r's range, its sign, its strength, and that it only measures straight-line relationships.
**Say this in the interview:** "Correlation measures how strongly two numeric variables move together in a straight line. The coefficient r runs from -1 to +1: the sign shows direction, and the size shows strength. It does not show causation."
**Explain simply:**
- r = +1 means a perfect upward straight line; r = -1 a perfect downward line; r = 0 means no *straight-line* relationship.
- The closer r is to -1 or +1, the tighter the dots hug a line.
- The usual measure is *Pearson's r*, which uses the actual values (see Q23 for Spearman).
- r has no units, so you can compare it across variables.
**Formula in plain words:** r = (how much X and Y vary together) divided by (how much X varies alone times how much Y varies alone). In symbols: r = Σ(x - x̄)(y - ȳ) / √[Σ(x - x̄)² × Σ(y - ȳ)²].
**Worked example:** Ten employees with 1 to 10 years of experience and monthly salaries (in thousands) of 30, 34, 33, 40, 42, 41, 48, 50, 49, 56 give r = 0.974: very strong positive.
**Excel / Python:**
```python
import numpy as np

# Years of experience for ten employees
years_of_experience = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Monthly salary in thousands for the same ten employees
monthly_salary_thousands = [30, 34, 33, 40, 42, 41, 48, 50, 49, 56]

# Build the 2x2 correlation table, then pick the X-vs-Y cell
correlation_matrix = np.corrcoef(years_of_experience, monthly_salary_thousands)
r = correlation_matrix[0, 1]

print("r =", round(r, 3))
```
Output: `r = 0.974`. Salary rises almost in a straight line with experience. Excel: with years in A2:A11 and salaries in B2:B11, `=CORREL(A2:A11,B2:B11)` returns 0.974 (not run in Excel here; CORREL exists in all versions).
**Likely follow-ups:** *Does r = 0.9 mean 90% related?* No, r² = 0.81 is the share of variation explained (Q22).
**Common mistakes:** Reading r as a percentage; using it on curved relationships; forgetting it says nothing about cause.

### Q3 ⭐⭐⭐ 🟢 What does R-squared (R²) tell you in a regression?
**Asked at:** commonly asked; R² vs adjusted R² appears on practice platforms (Interview Query, PracHub) per the sources file. No company-specific report found.
**What the interviewer is checking:** Can you say in plain words what share of the "ups and downs" the model explains, and its limits.
**Say this in the interview:** "R-squared is the share of the variation in the outcome that the model's inputs explain. R² of 0.95 means 95% of the spread in salaries is accounted for by experience; the other 5% is down to things the model does not capture."
**Explain simply:**
- It runs from 0 (model explains nothing, no better than the average) to 1 (explains everything).
- *Variation* means how far each value sits from the overall average.
- In a simple regression with one input, R² is just r squared.
- A high R² does not prove the model is right or causal (Q25).
**Formula in plain words:** R² = 1 minus (leftover unexplained variation divided by total variation). In symbols: R² = 1 - SSE/SST.
**Worked example:** Using the 10-employee salary data (Q2): total variation SST = 638.1; the leftover after the regression line SSE = 32.62. R² = 1 - 32.62/638.1 = 0.949.
**Excel / Python:**
```python
from scipy import stats

years_of_experience = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
monthly_salary_thousands = [30, 34, 33, 40, 42, 41, 48, 50, 49, 56]

# Fit the straight line
fit = stats.linregress(years_of_experience, monthly_salary_thousands)

# linregress returns r; square it to get R-squared
r_squared = fit.rvalue ** 2

print("R-squared =", round(r_squared, 3))
```
Output: `R-squared = 0.949`. Experience explains about 95% of salary variation in this small sample. Excel: `=RSQ(B2:B11,A2:A11)` (not run in Excel here).
**Likely follow-ups:** *Can R² be negative?* Not in an ordinary fit with an intercept on the training data; it can on new data or without an intercept.
**Common mistakes:** Saying "95% accurate" (it is not accuracy); assuming high R² means good or causal.

### Q4 ⭐⭐⭐ 🟢 What is linear regression, and when would a data analyst use it?
**Asked at:** Tiger Analytics (senior candidates reported linear regression assumptions, via Glassdoor search summary; not opened). Otherwise commonly asked.
**What the interviewer is checking:** Can you describe regression in plain words and name practical uses.
**Say this in the interview:** "Linear regression fits the best straight line through the data so I can describe how an outcome changes with an input and predict it. In HR I would use it to see how salary changes with experience, or to forecast headcount cost."
**Explain simply:**
- It finds a line: outcome = starting value + (change per unit) × input.
- "Best" means the line that makes the total squared miss as small as possible (Q43).
- Use it for (1) *explaining* relationships, (2) *predicting* a number, (3) *adjusting* for other factors with multiple regression.
- It needs a numeric outcome; for yes/no outcomes like "will leave" a different method (logistic regression) is used.
**Worked example:** From the 10-employee data the line is salary = 27.4 + 2.709 × years (in thousands). Each extra year goes with about 2.7 thousand more per month. For 5 years it predicts 27.4 + 2.709 × 5 = 40.95.
**Excel / Python:**
```python
from scipy import stats

years_of_experience = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
monthly_salary_thousands = [30, 34, 33, 40, 42, 41, 48, 50, 49, 56]

# Fit the line
fit = stats.linregress(years_of_experience, monthly_salary_thousands)

# Use the line to predict salary for someone with 5 years
predicted_salary = fit.intercept + fit.slope * 5

print("slope =", round(fit.slope, 3))
print("intercept =", round(fit.intercept, 3))
print("predicted salary at 5 years =", round(predicted_salary, 2))
```
Output: `slope = 2.709`, `intercept = 27.4`, `predicted salary at 5 years = 40.95`. Excel: `=FORECAST.LINEAR(5,B2:B11,A2:A11)` (Excel 2016+; `FORECAST` in older versions; not run in Excel here).
**Likely follow-ups:** *What are its assumptions?* See Q9.
**Common mistakes:** Using it for yes/no outcomes; predicting far outside the data (Q37); reading the slope as cause.

### Q5 ⭐⭐⭐ 🟢 Give a real business example where correlation does not mean causation.
**Asked at:** commonly asked; PracHub lists an Uber confounding prompt and Dataford uses marketing examples (sources file; snippet level).
**What the interviewer is checking:** Can you produce a concrete, believable example and name the hidden factor.
**Say this in the interview:** "Employees who attend more training have higher engagement scores. But long-serving employees both get more training and are more engaged, so tenure is behind both. If I control for tenure, the training effect disappears. Training is not the cause; I would test it with a pilot."
**Explain simply:**
- Pick an example with a clear *third factor*. Classic non-HR ones: ice-cream sales and sunburn (both caused by hot weather); more ad spend in festive months and higher sales (the season drives both).
- Name the third factor, say how you would check it (control for it, or run an experiment).
- Mention the other two traps: reverse causation (Q28) and coincidence (Q19).
**Worked example:** In my simulated 300 employees, training and engagement correlate at 0.68. Tenure correlates 0.88 with training and 0.79 with engagement. With tenure in the model, the training coefficient drops from 1.73 to -0.10 (p = 0.62). Full code is in Q8.
**Likely follow-ups:** *How would you test it for real?* Randomly offer training to half of a similar group and compare engagement.
**Common mistakes:** Using a silly example you cannot defend; naming the trap but not the fix.

### Q6 ⭐⭐⭐ 🟢 What do the slope and the intercept mean in a simple linear regression equation?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you read the equation in words with units, and spot when the intercept is meaningless.
**Say this in the interview:** "The slope is how much the outcome changes for one extra unit of the input. The intercept is the predicted outcome when the input is zero, which is only meaningful if zero is a realistic value."
**Explain simply:**
- Equation: outcome = intercept + slope × input.
- *Slope*: always say it with units ("each extra year of experience goes with 2,709 more rupees per month").
- *Intercept*: the line's starting height. A fresher with 0 years is plausible here, so 27.4 thousand is a sensible starting salary; for something like "height of 0 cm" it would be nonsense.
- A negative slope means the outcome falls as the input rises.
**Worked example:** From the 10 employees: salary = 27.4 + 2.709 × years. Slope 2.709 means +2,709 rupees per extra year; intercept 27.4 means about 27,400 for zero experience (extrapolated slightly: our data starts at 1 year).
**Excel / Python:**
```python
from scipy import stats

years_of_experience = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
monthly_salary_thousands = [30, 34, 33, 40, 42, 41, 48, 50, 49, 56]

fit = stats.linregress(years_of_experience, monthly_salary_thousands)

print("Slope (thousands per extra year):", round(fit.slope, 3))
print("Intercept (thousands at 0 years):", round(fit.intercept, 3))
```
Output: `Slope: 2.709`, `Intercept: 27.4`. Excel: `=SLOPE(B2:B11,A2:A11)` and `=INTERCEPT(B2:B11,A2:A11)` (not run in Excel here).
**Likely follow-ups:** *Does slope mean cause?* Not by itself (Q1).
**Common mistakes:** Forgetting units; over-reading an intercept that lies outside the data.

### Q7 ⭐⭐⭐ 🟡 How do you interpret correlation coefficients of 0.8, -0.6 and 0.05?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Sign, strength, and caution: can you read the number sensibly without cut-offs set in stone.
**Say this in the interview:** "0.8 is a strong positive relationship, -0.6 is a moderate to strong negative one, and 0.05 is essentially no straight-line relationship. Sign gives direction, size gives strength, and I always look at a scatter plot too."
**Explain simply:**
- Common rule of thumb (varies by field): under 0.3 weak, 0.3 to 0.7 moderate, over 0.7 strong. These are guidelines, not laws.
- Square r to see shared variation: 0.8 gives 0.64 (64%), -0.6 gives 0.36 (36%), 0.05 gives 0.0025 (0.25%).
- The minus sign only means "opposite direction"; -0.6 is stronger than +0.05.
**Worked example:** HR illustrations (not computed from data): 0.8 for years of experience and salary; -0.6 for number of late arrivals and performance rating; 0.05 for employee ID number and salary.
**Excel / Python:**
```python
# The three coefficients from the question
coefficients = [0.8, -0.6, 0.05]

# Square each one to get the share of variation shared
for r in coefficients:
    print("r =", r, " shared variation =", round(r ** 2, 4))
```
Output: 0.64, 0.36, 0.0025. So r = 0.8 shares 64% of variation, while 0.05 shares a quarter of one percent.
**Likely follow-ups:** *Is 0.3 important?* Depends on sample size and context (Q45).
**Common mistakes:** Calling -0.6 "weak" because it is negative; ignoring the scatter plot; treating 0.7 as a magic line.

### Q8 ⭐⭐⭐ 🟡 What is a confounding variable? Explain it with an example.
**Asked at:** commonly asked; confounder questions with company data examples appear on practice platforms (PracHub, Uber example). No company-specific report found.
**What the interviewer is checking:** That you can define a confounder (affects both the cause and the effect) and show how to adjust for it.
**Say this in the interview:** "A confounder is a hidden third variable that influences both the thing I think is the cause and the outcome, creating a misleading link. Tenure is a good HR example: it raises training hours and engagement, so training looks effective when it may not be."
**Explain simply:**
- Confounder: related to the input *and* to the outcome, and not itself caused by the input.
- It produces a correlation that is not a real effect (or hides a real one).
- Fixes: include it in a multiple regression, compare like with like (same tenure bands), or randomise.
**Worked example:** Simulated 300 employees: training and engagement correlate at 0.68; tenure correlates 0.88 with training and 0.79 with engagement. Adjusting for tenure moves the training coefficient from 1.73 to -0.10.
**Excel / Python:**
```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Simulate 300 employees (seeded so results repeat)
rng = np.random.default_rng(1)
n = 300
tenure_years = rng.uniform(0, 15, n)

# Longer tenure means more training hours
training_hours = 2 + 0.8 * tenure_years + rng.normal(0, 2, n)

# Engagement depends on tenure only, NOT on training
engagement_score = 50 + 2 * tenure_years + rng.normal(0, 6, n)

people = pd.DataFrame({"tenure_years": tenure_years,
                       "training_hours": training_hours,
                       "engagement_score": engagement_score})

# Raw correlation looks like training works
print("training vs engagement:", round(people["training_hours"].corr(people["engagement_score"]), 2))

# Model 1: training only
inputs_without_tenure = sm.add_constant(people[["training_hours"]])
without_tenure = sm.OLS(people["engagement_score"], inputs_without_tenure).fit()

# Model 2: training plus the confounder
inputs_with_tenure = sm.add_constant(people[["training_hours", "tenure_years"]])
with_tenure = sm.OLS(people["engagement_score"], inputs_with_tenure).fit()

print("training coef alone:", round(without_tenure.params["training_hours"], 2))
print("training coef with tenure:", round(with_tenure.params["training_hours"], 2))
print("p-value with tenure:", round(with_tenure.pvalues["training_hours"], 2))
```
Output: `0.68`, `1.73`, `-0.1`, `0.62`. Once tenure is held fixed, training adds nothing.
**Likely follow-ups:** *Can you always control for it?* No, only for confounders you have measured; unmeasured ones remain a risk.
**Common mistakes:** Confusing a confounder with a mediator (Q53); controlling for a variable that sits on the causal path.

### Q9 ⭐⭐⭐ 🟡 What are the assumptions of linear regression?
**Asked at:** Tiger Analytics (senior candidates, Glassdoor search summary, not opened); Ericsson India data scientist 2020 (Naukri Code360, low relevance); Interview Query lists it as a standard prompt.
**What the interviewer is checking:** Can you list the assumptions in plain words and say how to check each.
**Say this in the interview:** "Five main ones: the relationship is roughly linear, the errors are independent, the spread of errors is constant, the errors are roughly normal, and the inputs are not too tightly correlated with each other. I check them with a scatter plot, a residual plot, and a few simple tests."
**Explain simply:**
- *Linearity*: the trend is a straight line, not a curve. Check: scatter and residual plots.
- *Independence*: one row's error does not predict another's (matters for data over time). Check: Durbin-Watson (about 2 is fine).
- *Constant spread (homoscedasticity)*: errors are equally wide at all levels of the input. Check: residual plot, Breusch-Pagan test.
- *Normal errors*: matter mainly for p-values and intervals in small samples. Check: Q-Q plot or Shapiro-Wilk test.
- *No severe multicollinearity* (multiple regression): inputs not near copies of each other (Q26).
**Worked example:** For the 12-employee model in Q10, Breusch-Pagan p = 0.40 (spread looks constant), Shapiro-Wilk p = 0.94 (normal enough), Durbin-Watson = 2.72 (rows here are not in time order, so it is not meaningful). With only 12 rows these tests have little power, so plots matter more.
**Excel / Python:**
```python
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from scipy.stats import shapiro

# 'model' and 'predictors' come from the Q10 regression
residuals = model.resid

# Equal-spread test: p above 0.05 means no evidence of unequal spread
spread_p_value = het_breuschpagan(residuals, predictors)[1]

# Normality test: p above 0.05 means no evidence against normal errors
normality_p_value = shapiro(residuals).pvalue

# Independence check: close to 2 is good
independence_statistic = durbin_watson(residuals)

print("Breusch-Pagan p:", round(spread_p_value, 2))
print("Shapiro-Wilk p:", round(normality_p_value, 2))
print("Durbin-Watson:", round(independence_statistic, 2))
```
Output: `0.4`, `0.94`, `2.72`. No test raised a red flag.
**Likely follow-ups:** *What if one fails?* Transform the variable, add a missing input, or use robust standard errors.
**Common mistakes:** Saying inputs must be normal (the errors, not the inputs); skipping plots; treating a passed test on 12 rows as proof.

### Q10 ⭐⭐⭐ 🟡 How do you interpret the coefficient of a variable in a multiple regression?
**Asked at:** commonly asked; "coefficient with p-value" appears on practice platforms (PracHub). No company-specific report found.
**What the interviewer is checking:** The key phrase "holding the other variables constant".
**Say this in the interview:** "Each coefficient is the expected change in the outcome for one extra unit of that input, holding all the other inputs in the model fixed."
**Explain simply:**
- Adding inputs changes what each coefficient means: it is now the *separate* effect after accounting for the others.
- Always state units.
- The coefficient can change a lot when you add or drop inputs (see the confounder example in Q8).
- It describes association, not cause.
**Worked example:** 12 employees: years of experience, education years, and monthly salary (thousands) give salary = -9.54 + 2.32 × years + 2.98 × education. So, comparing people with the same education, one more year of experience goes with +2.32 thousand; comparing people with the same experience, one more education year goes with +2.98 thousand. (Made-up illustrative data.)
**Excel / Python:**
```python
import pandas as pd
import statsmodels.api as sm

# Twelve employees: experience, education years, monthly salary in thousands
staff = pd.DataFrame({
    "years":     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "education": [12, 16, 12, 14, 16, 12, 14, 16, 12, 14, 16, 14],
    "salary":    [29, 41, 36, 40, 49, 40, 49, 58, 46, 56, 67, 57]})

# Inputs table, with a constant column for the intercept
predictors = sm.add_constant(staff[["years", "education"]])

# Fit the multiple regression
model = sm.OLS(staff["salary"], predictors).fit()

# Show the coefficient table
print(model.summary().tables[1])
```
Output:
```
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const         -9.5379      5.111     -1.866      0.095     -21.100       2.024
years          2.3233      0.175     13.252      0.000       1.927       2.720
education      2.9836      0.371      8.051      0.000       2.145       3.822
```
Read the `coef` column for effects. Excel: `=LINEST(C2:C13,A2:B13,TRUE,TRUE)` gives the same, but lists coefficients in reverse order (not run in Excel here).
**Likely follow-ups:** *Can I compare coefficients to see which input matters more?* Not directly when units differ (Q54).
**Common mistakes:** Omitting "holding others constant"; reading a coefficient as causal; ignoring units.

### Q11 ⭐⭐⭐ 🟡 What does the p-value of a regression coefficient tell you?
**Asked at:** Tiger Analytics business analyst (one candidate reported p-values in regression, via Interview Query summary; not opened).
**What the interviewer is checking:** Correct meaning of a p-value, not the common misreadings.
**Say this in the interview:** "It tests whether that input's true coefficient could plausibly be zero. A small p-value, below 0.05, means that if the input had no real effect, data like mine would be unlikely, so I treat the effect as statistically significant. It does not say the effect is large or causal."
**Explain simply:**
- Null hypothesis: the coefficient is 0 (the input has no linear effect, given the other inputs).
- Small p: the data are hard to explain by chance alone. Large p: the data are consistent with no effect.
- It is *not* the probability the effect is zero, and not the effect size.
- It depends on sample size: huge samples make tiny effects significant (Q29).
**Worked example:** In the Q10 table, years has p < 0.001, so experience is clearly linked to salary after accounting for education. The constant has p = 0.095; we do not usually care about it. In Q8, training has p = 0.62 after controlling for tenure: no evidence of an effect.
**Excel / Python:**
```python
# 'model' is the Q10 regression
p_values = model.pvalues

# Print each p-value, rounded to 4 places
print(p_values.round(4))
```
Output: `const 0.0949`, `years 0.0000`, `education 0.0000` (the last two are tiny: about 0.0000003 and 0.00002, so well below 0.001). Excel's Data Analysis ToolPak regression shows the same "P-value" column (not run here).
**Likely follow-ups:** *Is p = 0.049 very different from 0.051?* No; 0.05 is a convention.
**Common mistakes:** "p = 0.03 means 97% chance the effect is real"; equating significance with importance.

### Q12 ⭐⭐ 🟢 What is the difference between correlation and regression?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Both describe linear association, but regression gives an equation, handles direction, and allows prediction and multiple inputs.
**Say this in the interview:** "Correlation gives one number for how strongly two variables move together, and it is symmetric. Regression gives an equation with a clear outcome and input, so I can predict and say how much the outcome changes per unit."
**Explain simply:**
- Correlation: r, between -1 and 1, no units, X vs Y is the same as Y vs X.
- Regression: slope and intercept with units, and it matters which one is the outcome.
- They are linked: slope = r × (spread of Y / spread of X).
- Regression can add many inputs; correlation compares just two.
**Formula in plain words:** slope = correlation × (standard deviation of Y ÷ standard deviation of X).
**Worked example:** For the 10-employee data r = 0.974; slope = 0.974 × (sd of salary ÷ sd of years) = 2.709, matching the fitted slope.
**Excel / Python:**
```python
import numpy as np

years_of_experience = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
monthly_salary_thousands = [30, 34, 33, 40, 42, 41, 48, 50, 49, 56]

r = np.corrcoef(years_of_experience, monthly_salary_thousands)[0, 1]

# Sample standard deviations (ddof=1 means divide by n-1)
spread_of_salary = np.std(monthly_salary_thousands, ddof=1)
spread_of_years = np.std(years_of_experience, ddof=1)

slope_from_correlation = r * spread_of_salary / spread_of_years
print(round(slope_from_correlation, 3))
```
Output: `2.709`, the same as the regression slope.
**Likely follow-ups:** *If r is the same both ways, is the slope?* No, the slope changes if you swap X and Y.
**Common mistakes:** Treating them as unrelated, or thinking regression proves cause while correlation does not.

### Q13 ⭐⭐ 🟢 What are the dependent and independent variables in a regression? Give an HR example.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic vocabulary and choosing the outcome correctly.
**Say this in the interview:** "The dependent variable is the outcome I am trying to explain or predict. The independent variables are the inputs I use. For example, monthly salary is dependent; years of experience and education level are independent."
**Explain simply:**
- Dependent (also: outcome, target, Y): "depends on" the others.
- Independent (also: predictor, feature, X): used to explain the outcome.
- More HR examples: dependent = engagement score, independent = manager rating, workload; dependent = time to hire, independent = number of interview rounds.
- Choice follows your question, not the data: the question decides which is Y.
**Worked example:** In Q10, salary (thousands per month) is the dependent variable; years and education are independent. Together they explain 97.1% of salary variation (R² = 0.971).
**Likely follow-ups:** *Can the independent variable be a category?* Yes, via dummy variables (Q39).
**Common mistakes:** Swapping them (the slope then changes); thinking "independent" means the inputs are unrelated to each other.

### Q14 ⭐⭐ 🟢 What can a scatter plot tell you about the relationship between two variables?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you look at the data before trusting a number.
**Say this in the interview:** "A scatter plot shows direction, strength, shape, and unusual points. I always plot first, because correlation only captures straight-line patterns and a single outlier can fool it."
**Explain simply:**
- *Direction*: dots rise (positive), fall (negative), or show no tilt.
- *Strength*: tightly packed along a line (strong) or a loose cloud (weak).
- *Shape*: straight, curved, or in clumps (groups hiding in the data, e.g. departments).
- *Outliers*: far-off dots that can pull r and the slope.
- *Spread*: whether the cloud widens, which hints at unequal variance (Q41).
**Worked example:** The 10 experience-salary points rise tightly along a line (r = 0.974). The points (-3, 9), (-2, 4), (-1, 1), (0, 0), (1, 1), (2, 4), (3, 9) form a U-shape yet r = 0 (Q17): only the plot reveals the pattern.
**Excel / Python:** Excel: select both columns, Insert > Scatter chart. Python: `plt.scatter(years_of_experience, monthly_salary_thousands)` with matplotlib (not run here; no numbers to verify).
**Likely follow-ups:** *What if there are thousands of points?* Use transparency or a density plot.
**Common mistakes:** Reporting r without plotting; ignoring clusters or outliers.

### Q15 ⭐⭐ 🟢 What is the difference between positive, negative and zero correlation? Give one example of each.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic vocabulary with sensible examples.
**Say this in the interview:** "Positive means both rise together, negative means one rises as the other falls, and zero means no straight-line link. Experience and salary is positive; late arrivals and performance rating is usually negative; shoe size and salary is about zero."
**Explain simply:**
- *Positive* (r above 0): more X goes with more Y.
- *Negative* (r below 0): more X goes with less Y.
- *Zero* (r near 0): knowing X does not help guess Y in a straight line (a curved link can still exist, Q17).
- Real data are rarely exactly 0, so "near zero" is the usual wording.
**Worked example:** Positive: years of experience vs salary, r = 0.974 (computed, Q2). A perfectly decreasing set, such as 1 to 5 against 10, 8, 6, 4, 2, gives exactly -1. Examples for "late arrivals vs rating" and "shoe size vs salary" are illustrative, not computed from data.
**Excel / Python:**
```python
import numpy as np

hours_worked_per_day = [1, 2, 3, 4, 5]
tasks_left_undone = [10, 8, 6, 4, 2]

r = np.corrcoef(hours_worked_per_day, tasks_left_undone)[0, 1]
print(round(r, 2))
```
Output: `-1.0`. As hours go up, undone tasks go down in a perfect straight line.
**Likely follow-ups:** *Which is stronger, +0.2 or -0.7?* -0.7; strength is the size, direction is the sign.
**Common mistakes:** Thinking negative correlation is "bad" or weak.

### Q16 ⭐⭐ 🟢 Can a correlation coefficient be greater than 1 or less than -1?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know r is bounded, and what to suspect when a result breaks the rule.
**Say this in the interview:** "No. r always lies between -1 and +1. If I see a value outside that, there is an error in my calculation or I have printed something else, such as covariance."
**Explain simply:**
- r is covariance (how X and Y vary together) divided by both spreads, which forces the answer into the range -1 to +1 (a mathematical result called the Cauchy-Schwarz inequality).
- +1 or -1 happens only with a perfect straight line.
- Unbounded numbers like covariance or the regression slope are *not* correlations; a slope of 2.7 is fine.
**Worked example:** For X = 1 to 5 and Y = 2, 4, 6, 8, 10 (perfect line up) r = 1.0; for Y = 10, 8, 6, 4, 2, r = -1.0. Nothing can go beyond.
**Excel / Python:**
```python
import numpy as np

x_values = [1, 2, 3, 4, 5]

# A perfectly rising line and a perfectly falling line
perfect_up = [2, 4, 6, 8, 10]
perfect_down = [10, 8, 6, 4, 2]

print(round(np.corrcoef(x_values, perfect_up)[0, 1], 2))
print(round(np.corrcoef(x_values, perfect_down)[0, 1], 2))
```
Output: `1.0` and `-1.0`: the two extremes.
**Likely follow-ups:** *Can R² exceed 1?* No, it is between 0 and 1 for a standard fit.
**Common mistakes:** Mixing r with slope or covariance; getting r = 1.0000001 from rounding and calling it an error.

### Q17 ⭐⭐ 🟢 If the correlation between two variables is zero, does it mean they are unrelated?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Understanding that Pearson r captures only straight-line relationships.
**Say this in the interview:** "No. Zero correlation only means there is no straight-line relationship. A curve, such as a U-shape, can be perfectly predictable and still have r = 0, which is why I plot the data."
**Explain simply:**
- Pearson r measures *linear* association only.
- Example in HR: stress vs performance often rises, then falls (an inverted U). Performance depends on stress strongly, yet r can be close to zero.
- Conversely, independence does imply r = 0, but not the other way round.
**Worked example:** x = -3 to 3 and y = x². Every y is fully determined by x, but r = 0.0 because the left and right halves cancel.
**Excel / Python:**
```python
import numpy as np

# X runs from -3 to 3
x_values = np.array([-3, -2, -1, 0, 1, 2, 3])

# Y is X squared: a perfect U-shaped link
y_values = x_values ** 2

r = np.corrcoef(x_values, y_values)[0, 1]
print(round(r, 2))
```
Output: `0.0`. A perfect relationship, yet zero correlation.
**Likely follow-ups:** *How would you detect such a relationship?* Scatter plot, or fit a curve (add x²).
**Common mistakes:** Saying "r = 0 so drop the variable" without plotting it.

### Q18 ⭐⭐ 🟢 What is a residual in regression?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you define residual and say why analysts look at them.
**Say this in the interview:** "A residual is the actual value minus the value the model predicted: the part the model got wrong for that row. I plot residuals to check the model's assumptions and to find unusual cases."
**Explain simply:**
- Residual = actual - predicted. Positive: the person earns more than the model expects; negative: less.
- Residuals from a line with an intercept add up to zero.
- The least-squares line is chosen to make the *sum of squared residuals* as small as possible (Q43).
- Big residuals flag outliers or missing factors.
**Formula in plain words:** residual = actual value minus predicted value.
**Worked example:** Employee 3 (3 years) earns 33; the line predicts 27.4 + 2.709 × 3 = 35.53; residual = 33 - 35.53 = -2.53 (earns 2.53 thousand less than the model expects). Sum of squared residuals over all ten: 32.62.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

years_of_experience = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
monthly_salary_thousands = [30, 34, 33, 40, 42, 41, 48, 50, 49, 56]

fit = stats.linregress(years_of_experience, monthly_salary_thousands)

# Predicted salary for each employee
predicted = fit.intercept + fit.slope * np.array(years_of_experience)

# Residual = actual minus predicted
residuals = np.array(monthly_salary_thousands) - predicted

print("residuals:", residuals.round(2))
print("sum of residuals:", round(residuals.sum(), 6))
print("sum of squared residuals:", round((residuals ** 2).sum(), 2))
```
Output: residuals `-0.11 1.18 -2.53 1.76 1.05 -2.65 1.64 0.93 -2.78 1.51`; sum `0.0`; squared sum `32.62`. Excel: `=B2-(INTERCEPT($B$2:$B$11,$A$2:$A$11)+SLOPE($B$2:$B$11,$A$2:$A$11)*A2)` (not run in Excel here).
**Likely follow-ups:** *What is a residual plot?* Residuals against predicted values; you want a shapeless cloud (Q36).
**Common mistakes:** Computing predicted minus actual (flips the sign); confusing residuals (sample) with true errors (unknown).

### Q19 ⭐⭐ 🟢 What is a spurious correlation?
**Asked at:** commonly asked (no company-specific report found); spurious correlation causes (confounder, coincidence, reverse causation) appear in prep-site question sets in the sources file.
**What the interviewer is checking:** Do you know that two things can move together with no real link between them?
**Say this in the interview:** "A spurious correlation is a relationship that shows up in the numbers but is not a real cause-and-effect link. It usually comes from a hidden third factor, pure coincidence, or a small sample. Before acting, I ask what else could explain it."
**Explain simply:**
- **Correlation** means two numbers tend to rise and fall together; **spurious** means the link is misleading.
- Cause 1: a **confounder**, a hidden third factor that drives both (summer heat drives ice cream sales and also holiday travel, so resignations rise).
- Cause 2: coincidence, especially when you test many pairs; some will match by luck.
- Cause 3: both series simply trend upwards over time.
- How to guard: think of a mechanism, look for a third factor, check other time periods or groups.
**Worked example:** Monthly ice cream sales and resignations in an office both peak in summer. Their correlation is very high, but ice cream does not make people quit; the common driver is the season (resignations rise after appraisal and holiday season).
**Excel / Python:**
```python
import numpy as np

# Twelve months of made-up data: ice cream sales and resignations
ice_cream_sales = np.array([20, 25, 35, 50, 70, 90, 100, 95, 70, 45, 30, 22])
resignations = np.array([3, 3, 4, 6, 8, 11, 12, 11, 8, 5, 4, 3])

# Correlation coefficient between the two series
correlation = np.corrcoef(ice_cream_sales, resignations)[0, 1]

print("Correlation:", round(correlation, 3))
```
Output:
```
Correlation: 0.996
```
A correlation of 0.996 is almost perfect, yet the link is not causal.
**Likely follow-ups:** 1) *How do you spot one?* Ask for a mechanism and look for a confounder. 2) *How do you prove causation?* A randomised experiment, such as an A/B test.
**Common mistakes:** Trusting a high r without asking "what else moves both?"

### Q20 ⭐⭐ 🟢 What is the difference between simple and multiple linear regression?
**Asked at:** commonly asked (no company-specific report found); regression basics appear across the practice sets in the sources file.
**What the interviewer is checking:** Do you know one predictor versus several, and why several are usually more realistic?
**Say this in the interview:** "Simple regression uses one input to predict an outcome, like salary from years of experience. Multiple regression uses two or more inputs, like experience, grade and city, and shows each one's effect while holding the others fixed."
**Explain simply:**
- **Regression** fits a line (or plane) that predicts a number (the **outcome**, or dependent variable) from **predictors** (inputs, or independent variables).
- Simple: salary = a + b × experience. One slope.
- Multiple: salary = a + b1 × experience + b2 × grade + b3 × hours. One slope per predictor.
- In multiple regression, each slope means "the change in the outcome for one more unit of this input, with the other inputs held constant".
- Multiple regression is more realistic but brings new issues: multicollinearity and adjusted R².
**Formula in plain words:** Predicted outcome = starting value + (effect of input 1 × input 1) + (effect of input 2 × input 2) and so on. In symbols: y = b0 + b1x1 + b2x2 + ...
**Worked example:** Simple: attrition risk score from engagement score only. Multiple: add tenure, manager rating and commute distance; now the engagement slope is the effect of engagement among people with the same tenure, rating and commute.
**Likely follow-ups:** 1) *Is multiple always better?* No; useless predictors add noise (see adjusted R²). 2) *Can inputs be categories?* Yes, through dummy variables.
**Common mistakes:** Reading a multiple-regression slope as if the other variables did not exist.

### Q21 ⭐⭐ 🟢 Given the regression salary = 20000 + 4000 × years of experience, what salary does the model predict for 5 years, and what does the slope mean?
**Asked at:** commonly asked (no company-specific report found); slope and intercept interpretation is among the most common regression questions in the sources file.
**What the interviewer is checking:** Can you plug into the equation and explain the slope in business words?
**Say this in the interview:** "Salary at 5 years is 20,000 + 4,000 × 5 = 40,000. The slope of 4,000 means that on average each extra year of experience goes with a salary that is 4,000 higher."
**Explain simply:**
- **Intercept (20,000):** predicted salary at zero experience (a fresher).
- **Slope (4,000):** average change in salary for one more year of experience.
- Say "goes with", not "causes"; this describes a pattern in the data.
- It is a prediction (an average), not a promise for any one person.
**Formula in plain words:** Prediction = intercept + slope × the input value.
**Worked example:** 5 years: 20,000 + 4,000 × 5 = 40,000. 6 years: 44,000, which is 4,000 more.
**Excel / Python:**
```python
# Model: salary = 20000 + 4000 * years of experience
intercept = 20000
slope = 4000

# Prediction for 5 years
salary_at_5_years = intercept + slope * 5

# Prediction for 6 years, to see what one extra year does
salary_at_6_years = intercept + slope * 6

print("Predicted salary at 5 years:", salary_at_5_years)
print("Extra salary for one more year:", salary_at_6_years - salary_at_5_years)
```
Output:
```
Predicted salary at 5 years: 40000
Extra salary for one more year: 4000
```
Excel: with experience in cell A2, `=20000+4000*A2` returns 40000 when A2 is 5 (not run in Excel here).
**Likely follow-ups:** 1) *What about 40 years?* Risky, because it may be outside the data (extrapolation). 2) *What units is the slope in?* Salary units per year of experience.
**Common mistakes:** Saying the slope is the salary, or that 4,000 more experience "causes" 4,000 more pay.

### Q22 ⭐⭐ 🟢 In a simple linear regression the correlation between X and Y is 0.6. What is R²?
**Asked at:** commonly asked (no company-specific report found); a standard quick-calculation question.
**What the interviewer is checking:** Do you know that in simple regression R² equals r squared?
**Say this in the interview:** "R² is r squared, so 0.6 × 0.6 = 0.36. About 36% of the variation in Y is explained by X. This holds only for simple regression with one predictor."
**Explain simply:**
- **R²** is the share of the ups and downs in Y that the model explains.
- With one predictor, R² = r × r. The sign of r disappears, so r = -0.6 also gives 0.36.
- The other 64% is explained by things not in the model, or by randomness.
**Formula in plain words:** R² = correlation × correlation. In symbols: R² = r².
**Worked example:** If engagement score and tenure have r = 0.6, then tenure explains 36% of the variation in engagement.
**Excel / Python:**
```python
# Correlation between X and Y in a simple regression
correlation = 0.6

# In simple regression, R-squared is the correlation squared
r_squared = correlation ** 2

# A negative correlation of -0.6 gives the same R-squared
r_squared_negative = (-0.6) ** 2

print("R-squared:", round(r_squared, 2))
print("R-squared if r = -0.6:", round(r_squared_negative, 2))
```
Output:
```
R-squared: 0.36
R-squared if r = -0.6: 0.36
```
Excel: `=0.6^2` returns 0.36 (not run in Excel here).
**Likely follow-ups:** 1) *What if r = 0.3?* R² = 0.09, only 9%. 2) *Does it hold in multiple regression?* No; there R² is not a simple square of one correlation.
**Common mistakes:** Saying R² is 0.6, or 60%.

### Q23 ⭐⭐ 🟡 What is the difference between Pearson and Spearman correlation, and when do you use each?
**Asked at:** reported as a question for a statistician role on Glassdoor (candidate-reported, search summary only, not opened); commonly asked (no company-specific report found) for analyst roles.
**What the interviewer is checking:** Do you know linear versus rank-based measures and can you choose between them?
**Say this in the interview:** "Pearson measures how close the points are to a straight line. Spearman ranks the values first and measures whether one always rises with the other, even along a curve. I use Spearman for ordinal data like ratings, for outliers, or for curved but steadily rising patterns."
**Explain simply:**
- **Pearson r:** straight-line (linear) relationship; uses the actual values; sensitive to outliers.
- **Spearman rho:** uses **ranks** (1st, 2nd, 3rd...); captures any steadily rising or falling (**monotonic**) pattern; robust to outliers.
- Use Spearman for ordinal data (1-5 satisfaction), skewed data like salary, or ranked data.
- If the relationship is roughly linear and clean, both give similar answers.
**Worked example:** Salary grows slowly then explodes with experience (30, 32, 35 ... 900). It always rises, so Spearman is a perfect 1.0, but Pearson is 0.709 because the curve is not a straight line.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Years of experience and salary (in thousands) for 10 employees
years_of_experience = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
salary_in_thousands = np.array([30, 32, 35, 38, 45, 60, 90, 150, 300, 900])

# Pearson: strength of a straight-line relationship
pearson_r = stats.pearsonr(years_of_experience, salary_in_thousands)[0]

# Spearman: strength of an "always going up" relationship, based on ranks
spearman_rho = stats.spearmanr(years_of_experience, salary_in_thousands)[0]

print("Pearson r:", round(pearson_r, 3))
print("Spearman rho:", round(spearman_rho, 3))
```
Output:
```
Pearson r: 0.709
Spearman rho: 1.0
```
Pearson is 0.709 because the pattern is curved; Spearman is 1.0 because the order never breaks. Excel: Pearson is `=CORREL(A2:A11,B2:B11)`; Spearman needs the ranks first (`=RANK.AVG` in helper columns) and then CORREL on the ranks (not run in Excel here).
**Likely follow-ups:** 1) *Can you compare engagement rating with tenure?* Yes, Spearman, since ratings are ordinal. 2) *Does rho = 1 mean a straight line?* No, only that the order always agrees.
**Common mistakes:** Using Pearson on ranked survey scores; thinking Spearman checks for a straight line.

### Q24 ⭐⭐ 🟡 What is adjusted R², and why is it preferred over R² in multiple regression?
**Asked at:** commonly asked (no company-specific report found); R² versus adjusted R² appears in the regression practice pages listed in the sources file.
**What the interviewer is checking:** Do you know R² never falls when you add predictors, and that adjusted R² corrects for this?
**Say this in the interview:** "R² always goes up when I add a variable, even a useless one, so it rewards over-stuffing the model. Adjusted R² penalises each extra predictor and only rises if the variable improves the model more than chance would. So I compare models with adjusted R²."
**Explain simply:**
- **R²** = share of variation explained; it can only stay the same or increase as inputs are added.
- **Adjusted R²** reduces R² according to the number of predictors, relative to the number of rows.
- A useless predictor can push adjusted R² down.
- The gap between R² and adjusted R² grows when you have many predictors and few rows.
**Formula in plain words:** Adjusted R² = 1 minus [(1 minus R²) × (rows minus 1) ÷ (rows minus predictors minus 1)]. In symbols: 1 - (1 - R²)(n - 1)/(n - k - 1).
**Worked example:** R² = 0.80 on 40 employees. With 3 predictors adjusted R² = 0.783; with 10 predictors (same R²) it falls to 0.731. Same fit, more complexity, lower score.
**Excel / Python:**
```python
import numpy as np
import statsmodels.api as sm

# 30 employees: salary truly depends only on tenure (years in company)
random_generator = np.random.default_rng(1)
number_of_employees = 30
tenure_years = random_generator.uniform(0, 10, number_of_employees)
salary_in_thousands = 30 + 3 * tenure_years + random_generator.normal(0, 4, number_of_employees)

# Three useless columns made of pure random noise
useless_columns = random_generator.normal(size=(number_of_employees, 3))

# Model A: tenure only
model_a_inputs = sm.add_constant(tenure_years)
model_a = sm.OLS(salary_in_thousands, model_a_inputs).fit()

# Model B: tenure plus the three useless columns
model_b_inputs = sm.add_constant(np.column_stack([tenure_years, useless_columns]))
model_b = sm.OLS(salary_in_thousands, model_b_inputs).fit()

print("Model A  R2:", round(model_a.rsquared, 4), " adjusted R2:", round(model_a.rsquared_adj, 4))
print("Model B  R2:", round(model_b.rsquared, 4), " adjusted R2:", round(model_b.rsquared_adj, 4))
```
Output:
```
Model A  R2: 0.8604  adjusted R2: 0.8554
Model B  R2: 0.8673  adjusted R2: 0.8461
```
Adding three pure-noise columns raised R² (0.8604 to 0.8673) but lowered adjusted R² (0.8554 to 0.8461), correctly flagging them as useless.
**Likely follow-ups:** 1) *Can adjusted R² be negative?* Yes, for a very poor model. 2) *What else compares models?* AIC/BIC, or testing on held-out data.
**Common mistakes:** Picking the model with the highest R² regardless of the number of variables.

### Q25 ⭐⭐ 🟡 Does a high R² mean the model is good?
**Asked at:** commonly asked (no company-specific report found); R² interpretation is a frequent theme in the sources file's regression pages.
**What the interviewer is checking:** Do you know R² is not a quality stamp?
**Say this in the interview:** "No. A high R² only says the model tracks the data closely. It can come from overfitting, the wrong shape, a trend shared by both variables, or from variables that should not be used. I also check residuals, adjusted R², sense of the coefficients, and performance on new data."
**Explain simply:**
- R² can be high with a **wrong model**: a straight line through curved data can still score about 0.89.
- R² rises automatically with more predictors (**overfitting**: fitting noise, failing on new data).
- Variables that trend together over time give high R² without any real link.
- R² says nothing about causation or whether the coefficients are sensible.
- A low R² is not always bad either: human behaviour is noisy.
**Worked example:** Salary actually rises in a curve with tenure, yet a straight line gets R² = 0.887. The residuals show the miss: the line is too high in the middle band and too low at the ends.
**Excel / Python:**
```python
import numpy as np
import statsmodels.api as sm

# 80 employees: salary really rises in a CURVE with tenure, not a straight line
random_generator = np.random.default_rng(11)
tenure_years = random_generator.uniform(0, 15, 80)
salary_in_thousands = 200 + 1.5 * tenure_years ** 2 + random_generator.normal(0, 25, 80)

# Fit a straight line anyway
straight_line_model = sm.OLS(salary_in_thousands, sm.add_constant(tenure_years)).fit()

# Average residual (actual minus predicted) in three tenure bands
residuals = straight_line_model.resid
for band_start, band_end in [(0, 5), (5, 10), (10, 15)]:
    in_band = (tenure_years >= band_start) & (tenure_years < band_end)
    print("Tenure", band_start, "to", band_end, "average residual:", round(residuals[in_band].mean(), 1))

print("R-squared:", round(straight_line_model.rsquared, 3))
```
Output:
```
Tenure 0 to 5 average residual: 9.0
Tenure 5 to 10 average residual: -26.8
Tenure 10 to 15 average residual: 12.1
R-squared: 0.887
```
The high R² hides a clear pattern in the errors (positive, negative, positive), which says the straight-line shape is wrong.
**Likely follow-ups:** 1) *What would you check next?* The residual plot and out-of-sample error. 2) *Is low R² always bad?* No; it depends on the field and the purpose.
**Common mistakes:** Quoting R² alone as proof the model is accurate.

### Q26 ⭐⭐ 🟡 What is multicollinearity, and how do you detect it?
**Asked at:** commonly asked (no company-specific report found); multicollinearity and VIF appear in the practice pages and the techprep set listed in the sources file.
**What the interviewer is checking:** Do you know the problem of overlapping predictors and the VIF test?
**Say this in the interview:** "Multicollinearity is when two or more predictors are strongly correlated with each other, like age and years of experience. I detect it with a correlation matrix and the VIF, the variance inflation factor. A VIF above about 5 to 10 is a warning."
**Explain simply:**
- Predictors that carry the same information cannot be separated by the model.
- **Correlation matrix:** look for predictor pairs with correlation near +1 or -1 (say above 0.8).
- **VIF** says how much a coefficient's uncertainty is inflated because of overlap. 1 means no overlap; above 5 or 10 is a concern (rules of thumb).
- Other signs: a good overall fit but insignificant coefficients, or signs that make no sense.
- Fixes: drop or combine one of the overlapping variables.
**Worked example:** For 100 employees, age and experience have a correlation of 0.971 and VIF of 17.3 each, so one should go.
**Excel / Python:**
```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 100 employees: age and years of experience move almost together
random_generator = np.random.default_rng(3)
years_experience = random_generator.uniform(1, 15, 100)
age = 22 + years_experience + random_generator.normal(0, 1, 100)
predictors = pd.DataFrame({"years_experience": years_experience, "age": age})

# Step 1: correlation between the two predictors
print("Correlation between predictors:", round(predictors.corr().iloc[0, 1], 3))

# Step 2: VIF for each predictor (statsmodels needs a constant column added)
predictors_with_constant = sm.add_constant(predictors)
for position, column_name in enumerate(predictors_with_constant.columns):
    if column_name != "const":
        vif = variance_inflation_factor(predictors_with_constant.values, position)
        print("VIF for", column_name, "=", round(vif, 1))
```
Output:
```
Correlation between predictors: 0.971
VIF for years_experience = 17.3
VIF for age = 17.3
```
Both predictors have a VIF of 17.3, well above the usual warning level, so they overlap heavily.
**Likely follow-ups:** 1) *Does it hurt predictions?* Not much, but it hurts coefficient interpretation. 2) *How to fix?* Drop one, combine them, or use methods such as ridge (Book 9).
**Common mistakes:** Checking correlation of each predictor with the outcome rather than with each other.

### Q27 ⭐⭐ 🟡 How does multicollinearity affect regression coefficients?
**Asked at:** commonly asked (no company-specific report found); a typical follow-up to the previous question.
**What the interviewer is checking:** Do you know it makes coefficients unstable and hard to trust, not that it ruins predictions?
**Say this in the interview:** "The coefficients become unstable: their standard errors blow up, they can swing a lot with small changes in the data, and they can even flip sign. The model as a whole can still predict well, but I cannot trust the individual effects."
**Explain simply:**
- The **standard error** (the typical uncertainty in a coefficient) becomes much larger.
- Larger standard errors mean wide confidence intervals and non-significant p-values, even for important variables.
- Coefficients change a lot if you add or remove a variable or a few rows.
- Overall R² and predictions stay fine, as long as new data keeps the same overlap pattern.
**Worked example:** Salary truly rises by about 3,000 per year of experience. With experience alone the model finds 3,080 (standard error 199). Add age, which moves almost in step, and experience drops to 1,599 (standard error 817), with R² barely changing (0.71 to 0.72). Re-drawing the sample five times gives 1,999, 2,161, 1,317, 840 and 2,932.
**Excel / Python:**
```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Same data as before: salary truly depends on experience only
random_generator = np.random.default_rng(3)
years_experience = random_generator.uniform(1, 15, 100)
age = 22 + years_experience + random_generator.normal(0, 1, 100)
salary = 20000 + 3000 * years_experience + random_generator.normal(0, 8000, 100)
predictors = pd.DataFrame({"years_experience": years_experience, "age": age})

# Model with both predictors
both_model = sm.OLS(salary, sm.add_constant(predictors)).fit()

# Model with experience only
experience_model = sm.OLS(salary, sm.add_constant(predictors[["years_experience"]])).fit()

print("Both predictors: experience coef", round(both_model.params["years_experience"]),
      "| std error", round(both_model.bse["years_experience"]), "| R2", round(both_model.rsquared, 3))
print("Experience only: experience coef", round(experience_model.params["years_experience"]),
      "| std error", round(experience_model.bse["years_experience"]), "| R2", round(experience_model.rsquared, 3))

# Refit on 5 random re-draws of the employees to see how unstable the coefficient is
for draw_number in range(5):
    chosen_rows = np.random.default_rng(100 + draw_number).choice(100, 100)
    refit = sm.OLS(salary[chosen_rows], sm.add_constant(predictors.iloc[chosen_rows])).fit()
    print("Re-draw", draw_number + 1, "experience coef:", round(refit.params["years_experience"]))
```
Output:
```
Both predictors: experience coef 1599 | std error 817 | R2 0.72
Experience only: experience coef 3080 | std error 199 | R2 0.71
Re-draw 1 experience coef: 1999
Re-draw 2 experience coef: 2161
Re-draw 3 experience coef: 1317
Re-draw 4 experience coef: 840
Re-draw 5 experience coef: 2932
```
Same R², but the experience coefficient is halved, its error is four times larger, and it jumps around between re-draws: the model cannot split credit between age and experience.
**Likely follow-ups:** 1) *Is the model useless?* Not for prediction; it is for explaining effects. 2) *What would you do?* Keep only one of the overlapping variables.
**Common mistakes:** Saying multicollinearity biases or reduces R²; it mainly inflates uncertainty.

### Q28 ⭐⭐ 🟡 What is reverse causation? Give an example.
**Asked at:** commonly asked (no company-specific report found); reverse causation is listed as a cause of misleading correlation in the techprep set (search summary).
**What the interviewer is checking:** Can you see that the arrow of cause may point the other way?
**Say this in the interview:** "Reverse causation is when I assume X causes Y, but actually Y causes X. For example, employees with low engagement may attend fewer events, rather than the events lowering engagement. I look at timing and run experiments to sort out direction."
**Explain simply:**
- **Causation** means a change in one thing actually produces a change in the other.
- With reverse causation the data shows the same correlation, but the direction is wrong.
- Clues: which change came first; does the story make more sense backwards?
- Remedies: use data with timing (did X change before Y?), natural experiments, or randomised tests.
**Worked example:** Managers who spend more time in one-to-one meetings have teams with lower attrition. Maybe the meetings help, or maybe managers of stable, happy teams simply have time for meetings, while managers firefighting resignations do not. Another: people who are about to leave stop attending training, so "less training" looks like it causes attrition when intent to leave caused the drop in training.
**Likely follow-ups:** 1) *How do you test direction?* Check timing, or use an experiment. 2) *How does it differ from a confounder?* A confounder is a third factor; reverse causation flips the arrow between the two.
**Common mistakes:** Assuming the direction that fits the story the business wants.

### Q29 ⭐⭐ 🟡 What is the difference between statistical significance and practical significance of a regression coefficient?
**Asked at:** commonly asked (no company-specific report found); coefficient and p-value interpretation recurs across sources (also one Tiger Analytics BA candidate report mentions p-values in regression, via search summary).
**What the interviewer is checking:** Do you know a tiny effect can be "significant" with enough data, and that size matters too?
**Say this in the interview:** "Statistical significance says the effect is unlikely to be pure chance (small p-value). Practical significance asks whether the effect is big enough to matter for the business. With a large sample, tiny effects become significant, so I look at the size, the confidence interval and the cost or benefit."
**Explain simply:**
- **p-value:** how surprising the result would be if there were really no effect. Small means unlikely to be luck.
- Large samples make the standard error small, so even trivial slopes get tiny p-values.
- **Practical significance:** is it big enough to change a decision (money, time, people)?
- Check effect size, R², the confidence interval and the real-world cost.
**Worked example:** With 50,000 employees, each extra year of tenure adds Rs 104 to salary on a Rs 50,000 base, with p = 0.000007. Very significant, but Rs 104 is about 0.2% of salary and R² is only 0.0004, so tenure explains almost nothing; not worth a policy.
**Excel / Python:**
```python
import numpy as np
import statsmodels.api as sm

# 50,000 employees: each extra year of tenure adds only Rs 100 to salary
random_generator = np.random.default_rng(5)
tenure_years = random_generator.uniform(0, 10, 50000)
salary = 50000 + 100 * tenure_years + random_generator.normal(0, 15000, 50000)

model = sm.OLS(salary, sm.add_constant(tenure_years)).fit()

print("Slope (Rs per year):", round(model.params[1], 1))
print("p-value:", model.pvalues[1])
print("R-squared:", round(model.rsquared, 5))
```
Output:
```
Slope (Rs per year): 104.3
p-value: 6.932446935585468e-06
R-squared: 0.0004
```
The p-value is tiny, so the slope is real, but the effect and R² are so small that it hardly matters.
**Likely follow-ups:** 1) *Can it be the reverse?* Yes: a large effect in a small sample may be non-significant. 2) *What do you report?* The effect size with a confidence interval.
**Common mistakes:** Treating p < 0.05 as "important".

### Q30 ⭐⭐ 🟡 How would you explain regression output to a non-technical manager?
**Asked at:** commonly asked (no company-specific report found); an "explain to a non-technical audience" prompt appears in the sources file (Remasto practice bank).
**What the interviewer is checking:** Can you turn numbers into a plain business message and state the limits?
**Say this in the interview:** "I skip the jargon. I say what drives the outcome, by how much in practical units, how sure we are, and how much of the picture the model captures. Then I add one caution, that this shows association, not proof of cause."
**Explain simply:**
- **Slope:** "Each extra year of experience goes with about Rs 4,000 more monthly salary, other factors held equal."
- **p-value / confidence interval:** "We are fairly confident the effect is real; the likely range is Rs 3,500 to 4,500."
- **R²:** "The model explains about 70% of why salaries differ; the other 30% is things we did not measure."
- **Prediction:** "For a person with 5 years we would expect roughly Rs 40,000, give or take."
- **Limits:** only valid inside the range of the data; shows patterns, not causes.
- Use a chart (scatter plot with the line) and one recommended action.
**Worked example:** "Across 200 employees, each extra year of experience is linked to Rs 4,000 higher pay. Experience alone explains 70% of pay differences. For hiring offers within 0 to 15 years, use the line as a guide, but check grade and city too."
**Likely follow-ups:** 1) *What if the manager asks "so does experience cause the raise?"* Say it is linked, and that grade and performance may also play a part. 2) *Which number matters most?* The slope, in business units.
**Common mistakes:** Reading out coefficient tables, or saying "R² of 0.7" without explaining it.

### Q31 ⭐⭐ 🟡 Experience and salary have a correlation of 0.85 across 200 employees. What can you conclude and what can you not conclude?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured version of the correlation-versus-causation theme in the sources file.
**What the interviewer is checking:** Can you read a correlation fairly: strength, direction, sample, and its limits?
**Say this in the interview:** "I can conclude that in these 200 employees, more experienced people tend to earn more, and the relationship is strong and positive; about 72% of salary variation lines up with experience. I cannot conclude that experience causes higher salary, that it is a rule for every employee, or what happens outside this data."
**Explain simply:**
- **Can say:** strong, positive, roughly linear association; r² = 0.85 × 0.85 = 0.7225, about 72% of variation shared.
- **With 200 rows** this is very unlikely to be a fluke, so it is statistically solid.
- **Cannot say:** causation (grade, education, performance and role could drive both); the size of the raise per year (that is the slope, not r); individual predictions; outside the range of the data.
- **Cannot say** the other 28% is random; it could be role, city, skills.
- Check a scatter plot: outliers or two different groups can produce a high r.
**Worked example:** If each year added Rs 4,000 on average, r = 0.85 does not tell you that; you need the regression slope. Also, senior grades may bring both experience and pay.
**Likely follow-ups:** 1) *What would you do next?* Plot the data and fit a regression with grade and role. 2) *Is 0.85 significant?* With n = 200, yes, comfortably.
**Common mistakes:** Saying "85% of salary is due to experience" (r is not a percentage; r² is the share, and shared is not caused).

### Q32 ⭐⭐ 🟡 Employees who attended more training have lower attrition. Can you say training reduces attrition?
**Asked at:** commonly asked (no company-specific report found); confounder questions are reported with company-data examples in the sources file (Uber confounding prompt on PracHub).
**What the interviewer is checking:** Can you apply causation caution to an HR case, naming confounders and proposing a better design?
**Say this in the interview:** "Not from this data alone. It shows training and lower attrition go together. Engaged, high-performing employees may sign up for training more and are also less likely to leave, or people planning to quit may skip training. To claim causation I would compare similar employees or run a randomised pilot."
**Explain simply:**
- **Confounder:** a hidden factor (engagement, manager quality, performance, tenure) that influences both training and attrition.
- **Self-selection:** motivated people choose training; that is not the same as training working.
- **Reverse causation:** people about to leave skip training.
- Better evidence: regression controlling for tenure, grade, rating; comparing matched groups; or a randomised pilot where some teams are randomly offered training.
- Fair claim: "associated with lower attrition; may reduce it; test before big investment".
**Worked example:** Suppose 12% of trained employees left versus 25% of untrained ones. If the trained group is mostly high performers with good managers, they would leave less anyway. Randomly offering training to half of the eligible employees and comparing the two halves removes that bias.
**Likely follow-ups:** 1) *How would you test it?* A randomised pilot or a matched comparison. 2) *Would you still recommend training?* Possibly, as a low-cost pilot, while stating the evidence is only suggestive.
**Common mistakes:** Replying "yes, it works" or "no, correlation is not causation" without a constructive next step.

### Q33 ⭐⭐ 🟡 For x = 1, 2, 3, 4, 5 and y = 2, 4, 5, 4, 5, calculate the Pearson correlation coefficient.
**Asked at:** commonly asked (no company-specific report found); a standard hand-calculation question (these exact numbers are the classic textbook example).
**What the interviewer is checking:** Can you do the calculation step by step and read the answer?
**Say this in the interview:** "The means are 3 and 4. The sum of the cross-products of the gaps is 6, the sum of squared x gaps is 10 and of squared y gaps is 6. So r = 6 ÷ square root of (10 × 6) = 0.775, a strong positive correlation."
**Explain simply:**
- Step 1: mean of x = 3, mean of y = 4.
- Step 2: gaps from the mean: x gaps are -2, -1, 0, 1, 2; y gaps are -2, 0, 1, 0, 1.
- Step 3: cross-products: 4, 0, 0, 0, 2, total 6. Squared x gaps total 10; squared y gaps total 4 + 0 + 1 + 0 + 1 = 6.
- Step 4: r = 6 ÷ √(10 × 6) = 6 ÷ √60 = 0.7746.
**Formula in plain words:** r = (sum of x gap × y gap) ÷ square root of (sum of x gaps squared × sum of y gaps squared). In symbols: r = Σ(x - x̄)(y - ȳ) / √[Σ(x - x̄)² × Σ(y - ȳ)²].
**Worked example:** As years go from 1 to 5, the score tends to rise; r = 0.775 means a strong positive straight-line link; r² = 0.6, so 60% of the variation in y lines up with x.
**Excel / Python:**
```python
import numpy as np

# The five data points
x_values = np.array([1, 2, 3, 4, 5])
y_values = np.array([2, 4, 5, 4, 5])

# Step 1: averages
mean_x = x_values.mean()
mean_y = y_values.mean()

# Step 2: how far each point is from its average
x_gaps = x_values - mean_x
y_gaps = y_values - mean_y

# Step 3: add up the pieces
sum_xy = (x_gaps * y_gaps).sum()
sum_xx = (x_gaps ** 2).sum()
sum_yy = (y_gaps ** 2).sum()

# Step 4: Pearson r
pearson_r = sum_xy / np.sqrt(sum_xx * sum_yy)

print("mean_x, mean_y:", mean_x, mean_y)
print("sum_xy, sum_xx, sum_yy:", sum_xy, sum_xx, sum_yy)
print("Pearson r:", round(pearson_r, 4))
print("Check with numpy:", round(np.corrcoef(x_values, y_values)[0, 1], 4))
```
Output:
```
mean_x, mean_y: 3.0 4.0
sum_xy, sum_xx, sum_yy: 6.0 10.0 6.0
Pearson r: 0.7746
Check with numpy: 0.7746
```
Excel: with x in A2:A6 and y in B2:B6, `=CORREL(A2:A6,B2:B6)` returns 0.7746 (not run in Excel here).
**Likely follow-ups:** 1) *What is R²?* 0.6. 2) *With only 5 points, how reliable?* Not very; the sample is tiny.
**Common mistakes:** Dividing by the wrong total, or forgetting the square root.

### Q34 ⭐⭐ 🟡 For x = 1, 2, 3, 4, 5 and y = 2, 4, 5, 4, 5, calculate the regression line y = a + bx.
**Asked at:** commonly asked (no company-specific report found); the companion to the previous hand-calculation question.
**What the interviewer is checking:** Can you compute slope and intercept by hand and interpret them?
**Say this in the interview:** "The slope is 6 ÷ 10 = 0.6. The intercept is the mean of y minus slope times mean of x: 4 - 0.6 × 3 = 2.2. So y = 2.2 + 0.6x: each extra unit of x adds 0.6 to y."
**Explain simply:**
- Slope b = (sum of x gap × y gap) ÷ (sum of x gaps squared) = 6 ÷ 10 = 0.6.
- Intercept a = mean of y minus b × mean of x = 4 - 0.6 × 3 = 2.2.
- The line always passes through the point (mean of x, mean of y) = (3, 4).
- Predictions: 2.8, 3.4, 4.0, 4.6, 5.2. Residuals (actual minus predicted): -0.8, 0.6, 1.0, -0.6, -0.2, which add to zero.
**Formula in plain words:** Slope = sum of products of gaps ÷ sum of squared x gaps; intercept = mean of y minus slope × mean of x. In symbols: b = Σ(x - x̄)(y - ȳ) / Σ(x - x̄)²; a = ȳ - b x̄.
**Worked example:** Predicted y at x = 6 would be 2.2 + 0.6 × 6 = 5.8, but 6 is outside the data range, so treat with care.
**Excel / Python:**
```python
import numpy as np

# The five data points
x_values = np.array([1, 2, 3, 4, 5])
y_values = np.array([2, 4, 5, 4, 5])

# Averages
mean_x = x_values.mean()
mean_y = y_values.mean()

# Slope b = sum of (x gap * y gap) / sum of (x gap squared)
x_gaps = x_values - mean_x
y_gaps = y_values - mean_y
slope_b = (x_gaps * y_gaps).sum() / (x_gaps ** 2).sum()

# Intercept a = mean_y - slope * mean_x
intercept_a = mean_y - slope_b * mean_x

# Predictions and residuals (actual minus predicted)
predicted_y = intercept_a + slope_b * x_values
residuals = y_values - predicted_y

print("Slope b:", round(slope_b, 2))
print("Intercept a:", round(intercept_a, 2))
print("Predicted y:", predicted_y.round(1))
print("Residuals:", residuals.round(1))
print("Sum of residuals:", round(residuals.sum(), 6))
print("Check with numpy.polyfit (slope, intercept):", np.polyfit(x_values, y_values, 1).round(2))
```
Output:
```
Slope b: 0.6
Intercept a: 2.2
Predicted y: [2.8 3.4 4.  4.6 5.2]
Residuals: [-0.8  0.6  1.  -0.6 -0.2]
Sum of residuals: -0.0
Check with numpy.polyfit (slope, intercept): [0.6 2.2]
```
Excel: `=SLOPE(B2:B6,A2:A6)` returns 0.6 and `=INTERCEPT(B2:B6,A2:A6)` returns 2.2 (not run in Excel here).
**Likely follow-ups:** 1) *Check using r?* Slope = r × (sd of y ÷ sd of x) = 0.7746 × (1.2247 ÷ 1.5811) = 0.6. 2) *What is R²?* 0.6.
**Common mistakes:** Swapping x and y (regressing x on y gives a different line); forgetting the intercept.

### Q35 ⭐⭐ 🟡 How do you check whether a linear regression model is a good fit?
**Asked at:** commonly asked (no company-specific report found); regression assumptions and checks are reported for Tiger Analytics (Glassdoor reviews, search summary only) and in practice pages.
**What the interviewer is checking:** Do you go beyond R² to residuals, assumptions and out-of-sample checks?
**Say this in the interview:** "I look at several things: R² and adjusted R² for how much is explained, the typical error in real units, whether the coefficients make business sense and are significant, the residual plot for patterns, and performance on data the model has not seen."
**Explain simply:**
- **Fit measures:** R², adjusted R², and the typical error (residual standard error) in real units such as rupees.
- **Coefficients:** do signs and sizes make sense; are p-values and confidence intervals reasonable?
- **Residual checks:** random scatter around zero, roughly equal spread, roughly bell-shaped, no outliers with big influence.
- **Assumptions:** linear shape, independent rows, equal spread, errors roughly normal.
- **Validation:** split the data into a training set and a test set; compare errors.
**Worked example:** A model of salary on tenure for 80 employees gave R² = 0.897 and a typical error of about 62.7 (in thousands, on salaries running from about 300 to 900); the residual tests raised no warning, so the line is a decent fit.
**Excel / Python:**
```python
import numpy as np
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan

# 80 employees: salary (in thousands) really is a straight-line function of tenure plus noise
random_generator = np.random.default_rng(11)
tenure_years = random_generator.uniform(0, 15, 80)
salary_in_thousands = 300 + 40 * tenure_years + random_generator.normal(0, 60, 80)

# Fit the line
inputs = sm.add_constant(tenure_years)
model = sm.OLS(salary_in_thousands, inputs).fit()
residuals = model.resid

# Fit measures
print("Intercept, slope:", model.params.round(2))
print("R-squared:", round(model.rsquared, 3), "| adjusted:", round(model.rsquared_adj, 3))
print("Typical error (residual std):", round(np.sqrt(model.scale), 1))

# Residual checks (p-values above 0.05 mean no warning sign)
print("Residual normality test p-value:", round(stats.shapiro(residuals).pvalue, 3))
print("Equal-spread test p-value:", round(het_breuschpagan(residuals, inputs)[1], 3))
```
Output:
```
Intercept, slope: [300.6   40.67]
R-squared: 0.897 | adjusted: 0.895
Typical error (residual std): 62.7
Residual normality test p-value: 0.718
Equal-spread test p-value: 0.25
```
High R², a typical error that is small relative to the salary scale, and no warning from the residual tests: a good fit.
**Likely follow-ups:** 1) *Which matters most?* The residual plot and out-of-sample error. 2) *What if the plot is curved?* Add a squared term or transform the variable.
**Common mistakes:** Judging by R² alone, or never testing on new data.

### Q36 ⭐⭐ 🟡 What is a residual plot, and which patterns should worry you?
**Asked at:** commonly asked (no company-specific report found); regression diagnostics are standard follow-ups in the practice sets in the sources file.
**What the interviewer is checking:** Do you know what a healthy residual plot looks like and what warning shapes mean?
**Say this in the interview:** "A residual plot shows predicted values on the x-axis and the errors (actual minus predicted) on the y-axis. I want a shapeless cloud around zero. A curve, a funnel shape, clear groups or extreme points all mean the model has a problem."
**Explain simply:**
- **Residual** = actual minus predicted, the leftover error for each person.
- **Healthy:** random scatter around the zero line, even spread.
- **Curve (U or arch):** the relationship is not a straight line; add a curved term or transform.
- **Funnel or fan** (spread grows or shrinks): unequal spread (**heteroscedasticity**), so standard errors and p-values are unreliable; consider a log transform.
- **Clusters or a pattern over time:** missing group variable or errors that are linked across rows.
- **A few extreme points:** outliers that may pull the line.
**Worked example:** Salary on tenure. In the healthy case, the residual spread is about 58, 60 and 69 across the tenure bands. In the fan case it grows from about 19 to 36 to 69: the model is much less reliable for senior employees.
**Excel / Python:**
```python
import numpy as np
import statsmodels.api as sm

random_generator = np.random.default_rng(11)
tenure_years = random_generator.uniform(0, 15, 80)
inputs = sm.add_constant(tenure_years)

# Case 1: straight-line truth, so the residuals are healthy noise
healthy_salary = 300 + 40 * tenure_years + random_generator.normal(0, 60, 80)
healthy_residuals = sm.OLS(healthy_salary, inputs).fit().resid

# Case 2: spread grows with tenure (the "fan" or "funnel" shape)
fan_salary = 300 + 40 * tenure_years + random_generator.normal(0, 1, 80) * (5 + 6 * tenure_years)
fan_residuals = sm.OLS(fan_salary, inputs).fit().resid

# Compare the size of the residuals in three tenure bands
for band_start, band_end in [(0, 5), (5, 10), (10, 15)]:
    in_band = (tenure_years >= band_start) & (tenure_years < band_end)
    print("Tenure", band_start, "to", band_end,
          "| healthy spread:", round(healthy_residuals[in_band].std(), 1),
          "| fan spread:", round(fan_residuals[in_band].std(), 1))

# To draw the plot: plt.scatter(fitted_values, residuals); plt.axhline(0)
```
Output:
```
Tenure 0 to 5 | healthy spread: 58.2 | fan spread: 18.9
Tenure 5 to 10 | healthy spread: 59.8 | fan spread: 35.8
Tenure 10 to 15 | healthy spread: 68.9 | fan spread: 69.0
```
Healthy residuals have a similar size in each band; the fan case spreads out as tenure grows.
**Likely follow-ups:** 1) *How do you fix a funnel?* Transform the outcome (e.g. log salary) or use robust standard errors. 2) *What does a curve mean?* A straight line is the wrong shape.
**Common mistakes:** Plotting residuals against the wrong axis, or only checking that they average zero (they always do in a fitted line with an intercept).

### Q37 ⭐⭐ 🟡 What is extrapolation in regression, and why is it risky?
**Asked at:** commonly asked (no company-specific report found); a standard follow-up to "how do you use a regression line to predict".
**What the interviewer is checking:** Do you know a regression line is only trustworthy inside the range of data it was built from?
**Say this in the interview:** "Extrapolation means predicting for x-values outside the range I trained on. It is risky because I have no evidence the straight-line pattern continues out there, so I would flag it or avoid it."
**Explain simply:**
- **Interpolation** = predicting inside the observed range (e.g. 1 to 8 years of experience). Usually reasonable.
- **Extrapolation** = predicting outside it (e.g. 25 years). The line is just a straight ruler we laid over the data we saw.
- Real patterns bend, flatten or hit limits (salary bands, pay caps), but a straight line keeps climbing forever.
- Uncertainty also grows quickly the further you go from the average x.
**Worked example:** Eight employees with 1 to 8 years of experience earn 4.0 to 8.8 lakhs, and the gains shrink each year. A straight line fits well but predicts 20.76 lakhs for 25 years, more than double anyone we observed. A pay band would almost certainly cap this far lower.
**Excel / Python:**
```python
import numpy as np

# Years of experience and salary (in lakhs per year) for 8 employees we actually observed
years_of_experience = np.array([1, 2, 3, 4, 5, 6, 7, 8])
salary_in_lakhs = np.array([4.0, 5.2, 6.1, 6.9, 7.6, 8.1, 8.5, 8.8])

# Fit a straight line: salary = intercept + slope * years
slope, intercept = np.polyfit(years_of_experience, salary_in_lakhs, 1)

# Predict inside the data range (interpolation) and far outside it (extrapolation)
prediction_at_4_years = intercept + slope * 4
prediction_at_25_years = intercept + slope * 25

print("Slope (lakhs per extra year):", round(slope, 3))
print("Intercept:", round(intercept, 3))
print("Prediction at 4 years (inside data):", round(prediction_at_4_years, 2), "lakhs")
print("Prediction at 25 years (outside data):", round(prediction_at_25_years, 2), "lakhs")
print("Highest salary we actually observed:", salary_in_lakhs.max(), "lakhs")
```
Output:
```
Slope (lakhs per extra year): 0.676
Intercept: 3.857
Prediction at 4 years (inside data): 6.56 lakhs
Prediction at 25 years (outside data): 20.76 lakhs
Highest salary we actually observed: 8.8 lakhs
```
The 4-year prediction sits among real data; the 25-year prediction is far beyond anything observed, so we cannot trust it.
**Likely follow-ups:** 1) *Is a small step outside the range allowed?* Sometimes, with a clear warning and a reason to believe the pattern holds. 2) *How do you avoid the problem?* State the valid range with every model and collect data that covers the cases you need.
**Common mistakes:** Trusting a high R² as proof the line works everywhere; forgetting that the intercept at x = 0 can itself be an extrapolation (nobody has 0 years and a meaningful salary).

### Q38 ⭐⭐ 🟡 Does a strong correlation mean a steep slope?
**Asked at:** commonly asked (no company-specific report found); correlation and slope interpretation appear in nearly every regression source in research/Book05_Part07_sources.md.
**What the interviewer is checking:** Do you separate "how tightly points hug a line" (correlation) from "how steep the line is" (slope)?
**Say this in the interview:** "No. Correlation measures how consistently the points follow a line; slope measures how much y changes per unit of x. A very gentle line can have a correlation near 1, and a steep one can have a weak correlation."
**Explain simply:**
- **Correlation (r)** is a score from -1 to +1 for how tightly points cluster around a straight line. It has no units.
- **Slope** is the change in y for one extra unit of x. It carries the units of your data.
- Slope depends on the units and the spread of y; correlation does not.
- Link between them: slope = r x (spread of y / spread of x), where "spread" is the standard deviation.
**Formula in plain words:** Slope = correlation x (how spread out y is / how spread out x is). In symbols: b = r x (s_y / s_x).
**Worked example:** Using 6 employees: salary rises about 2.04 lakhs per year of experience (r = 0.998). Attendance score rises only 0.389 points per year, yet r = 0.997, almost the same tightness. A third salary set has a similar steep slope (1.914) but individuals scatter widely, so r is only 0.596.
**Excel / Python:**
```python
import numpy as np

# Years of experience for 6 employees
years_of_experience = np.array([1, 2, 3, 4, 5, 6])

# Case A: salary rises steeply with experience, with a little noise (in lakhs)
salary_steep = np.array([4.0, 6.5, 8.0, 10.6, 12.1, 14.4])

# Case B: attendance score rises only slightly, but very consistently
attendance_gentle = np.array([90.0, 90.4, 90.9, 91.2, 91.5, 92.0])

# Case C: salary rises steeply but individuals scatter a lot around the trend
salary_scattered = np.array([4.0, 14.0, 6.0, 16.0, 8.0, 19.0])

# Correlation and slope for each case
for label, outcome in [("Salary (steep)", salary_steep), ("Attendance (gentle)", attendance_gentle), ("Salary (scattered)", salary_scattered)]:
    correlation = np.corrcoef(years_of_experience, outcome)[0, 1]
    slope = np.polyfit(years_of_experience, outcome, 1)[0]
    print(label, "-> correlation:", round(correlation, 3), "| slope:", round(slope, 3))
```
Output:
```
Salary (steep) -> correlation: 0.998 | slope: 2.04
Attendance (gentle) -> correlation: 0.997 | slope: 0.389
Salary (scattered) -> correlation: 0.596 | slope: 1.914
```
Cases A and B have the same tightness but very different slopes; Case C has a steep slope but a loose fit.
**Likely follow-ups:** 1) *When are slope and correlation the same?* When x and y are both standardised (same spread), slope equals r. 2) *Which tells you "how much"?* Slope. Correlation tells you "how reliably".
**Common mistakes:** Saying "r = 0.9 so each unit of x adds 0.9 to y"; reading correlation as effect size.

### Q39 ⭐⭐ 🟡 How do you include a categorical variable such as department in a regression?
**Asked at:** commonly asked (no company-specific report found); coefficient interpretation is a staple regression question in the sources file.
**What the interviewer is checking:** Do you know regression needs numbers, and how dummy (0/1) variables and a baseline group work?
**Say this in the interview:** "I convert it into dummy variables, 0/1 columns, one per department except one that I leave out as the baseline. Each coefficient then reads as the average difference from the baseline department, holding other variables fixed."
**Explain simply:**
- A regression cannot multiply the word "Sales" by a number, so each category becomes a **dummy variable**: 1 if the person is in that department, otherwise 0.
- With k departments you make k - 1 dummies; the one left out is the **reference (baseline) group**.
- The intercept becomes the baseline group's average; each dummy coefficient is the gap from that baseline.
- Do not code departments as 1, 2, 3: that wrongly claims IT is "twice" HR.
**Worked example:** Engagement scores: HR average 8.5, Sales 6.5, IT 5.5. With HR as baseline, the model gives intercept 8.5, Sales -2.0 and IT -3.0, exactly the gaps from HR.
**Excel / Python:**
```python
import pandas as pd
import statsmodels.formula.api as smf

# 12 employees: department and engagement score (out of 10)
employees = pd.DataFrame({
    "department": ["Sales"] * 4 + ["HR"] * 4 + ["IT"] * 4,
    "engagement_score": [6, 7, 6, 7, 8, 9, 8, 9, 5, 6, 5, 6],
})

# Average engagement per department, to compare with the regression later
print(employees.groupby("department")["engagement_score"].mean())

# C(department) tells the model to turn the text column into 0/1 dummy columns
# Treatment('HR') makes HR the reference (baseline) group
model = smf.ols("engagement_score ~ C(department, Treatment('HR'))", data=employees).fit()

# Intercept = average of HR; the other rows = difference from HR
print(model.params.round(2))
```
Output:
```
department
HR       8.5
IT       5.5
Sales    6.5
Name: engagement_score, dtype: float64
Intercept                                  8.5
C(department, Treatment('HR'))[T.IT]      -3.0
C(department, Treatment('HR'))[T.Sales]   -2.0
dtype: float64
```
The regression simply reproduces the group averages as differences from HR. In Excel, add 0/1 columns by hand (e.g. `=IF(B2="Sales",1,0)`) and run Data Analysis > Regression, leaving one department out.
**Likely follow-ups:** 1) *Which baseline should I choose?* The largest or most natural group; the model fit is identical, only the reading changes. 2) *Many categories?* Group rare ones together or use methods built for high-cardinality data.
**Common mistakes:** Using 1/2/3 codes; including all k dummies with an intercept (see Q51).

### Q40 ⭐⭐ 🔴 How can you move from correlation towards causation when you only have observational data?
**Asked at:** correlation vs causation was reported for a Tiger Analytics business analyst candidate (Interview Query, via search summary, candidate-reported); this "how do you get closer to causation" version is commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you name practical ways to reduce confounding and be honest about what observational data can prove?
**Say this in the interview:** "Observational data can never fully prove causation, but I can get closer: control for confounders, compare like with like, check that the cause comes before the effect, look for a dose-response pattern, and use natural experiments or an A/B test when possible."
**Explain simply:**
- **Confounder:** a hidden third factor that drives both the cause and the effect. Control for it by adding it to the regression or comparing within groups.
- **Matching or stratifying:** compare people who are alike on the confounders (e.g. same tenure band).
- **Timing:** the cause must come before the effect; watch out for reverse causation.
- **Dose-response:** more of the cause giving more of the effect strengthens the case.
- **Better designs:** a randomised A/B test is the gold standard; otherwise use a natural experiment or difference-in-differences (comparing before/after changes between a treated and untreated group).
- Even after all this, unmeasured confounders may remain, so say "suggests", not "proves".
**Worked example:** Training hours look strongly linked to performance. But senior people attend more training and also perform better. Simulated data (true training effect 0.1 points per hour): the naive model shows 0.902 per hour, nine times too big. Controlling for tenure gives 0.066, close to the truth.
**Excel / Python:**
```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# Simulate 500 employees (fixed seed so the result repeats)
random_generator = np.random.default_rng(7)
tenure_years = random_generator.uniform(0, 10, 500)

# More senior people attend training more often AND score higher (tenure is the confounder)
training_hours = 5 + 2 * tenure_years + random_generator.normal(0, 3, 500)

# True story: training adds 0.1 points per hour; tenure adds 2 points per year
performance_score = 50 + 0.1 * training_hours + 2 * tenure_years + random_generator.normal(0, 3, 500)

employees = pd.DataFrame({"training_hours": training_hours, "tenure_years": tenure_years,
                          "performance_score": performance_score})

# Naive model: ignores tenure
naive_model = smf.ols("performance_score ~ training_hours", data=employees).fit()

# Adjusted model: holds tenure fixed
adjusted_model = smf.ols("performance_score ~ training_hours + tenure_years", data=employees).fit()

print("Training effect, naive:   ", round(naive_model.params["training_hours"], 3))
print("Training effect, adjusted:", round(adjusted_model.params["training_hours"], 3))
```
Output:
```
Training effect, naive:    0.902
Training effect, adjusted: 0.066
```
Adjusting for the confounder removed almost all of the fake effect. This only works because we measured tenure; unmeasured confounders would still bias it.
**Likely follow-ups:** 1) *What if you can run an experiment?* Randomly assign training; randomisation balances confounders automatically. 2) *Can regression prove causation?* No, it only adjusts for what you include.
**Common mistakes:** Believing "I controlled for variables, so it is causal"; controlling for a mediator or a collider (see Q53).

### Q41 ⭐ 🟡 What is heteroscedasticity, and why does it matter?
**Asked at:** commonly asked (no company-specific report found); linear regression assumptions are reported for Tiger Analytics candidates (Glassdoor, via search summary, not opened).
**What the interviewer is checking:** Do you know the constant-spread assumption and what breaks when it fails?
**Say this in the interview:** "Heteroscedasticity means the spread of the prediction errors changes across the range, for example salary varying much more among senior staff. The coefficients stay unbiased, but standard errors and p-values become unreliable, so I would use robust standard errors or transform the variable."
**Explain simply:**
- **Homoscedasticity** = errors have the same spread everywhere. **Heteroscedasticity** = the spread changes (often a fan or cone shape in the residual plot).
- Salary is a classic case: juniors cluster tightly, seniors vary a lot.
- The slope estimate is still unbiased on average, but the usual standard errors are wrong, so confidence intervals and p-values mislead.
- Spot it with a residual plot (Q36) or a test such as Breusch-Pagan, where a small p-value signals unequal spread.
- Fixes: robust (HC) standard errors, a log transform (Q52), or weighted least squares.
**Worked example:** 300 simulated employees where salary scatter grows with experience. Breusch-Pagan p = 3.54e-11, so we reject constant spread. The usual standard error of the slope (0.0592) and the robust one (0.061) are close here because the pattern is mild; the test, not the standard error gap, is what flags the problem.
**Excel / Python:**
```python
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan

# Simulate 300 employees: the higher the experience, the more salaries vary
random_generator = np.random.default_rng(11)
years_of_experience = random_generator.uniform(1, 15, 300)
noise_size = 0.5 * years_of_experience
salary_in_lakhs = 3 + 0.8 * years_of_experience + random_generator.normal(0, 1, 300) * noise_size

# Fit the straight-line model
predictors = sm.add_constant(years_of_experience)
model = sm.OLS(salary_in_lakhs, predictors).fit()

# Breusch-Pagan test: a small p-value means the spread of errors is NOT constant
test_statistic, p_value, f_statistic, f_p_value = het_breuschpagan(model.resid, predictors)
print("Breusch-Pagan p-value:", format(p_value, ".2e"))

# Compare the usual standard error of the slope with a robust one
robust_model = sm.OLS(salary_in_lakhs, predictors).fit(cov_type="HC3")
print("Slope standard error, usual: ", round(model.bse[1], 4))
print("Slope standard error, robust:", round(robust_model.bse[1], 4))
```
Output:
```
Breusch-Pagan p-value: 3.54e-11
Slope standard error, usual:  0.0592
Slope standard error, robust: 0.061
```
The test flags unequal spread; robust standard errors give a safer measure of uncertainty.
**Likely follow-ups:** 1) *Does it bias the coefficients?* No, it affects the standard errors and efficiency. 2) *How do you fix it?* Robust standard errors, log transform, or weighted regression.
**Common mistakes:** Saying it biases the slope; deleting "noisy" points instead of modelling the pattern.

### Q42 ⭐ 🟡 Why can two trending time series show a high correlation even if they are unrelated?
**Asked at:** commonly asked (no company-specific report found); a time-series version of "spurious correlation", which the sources file lists as a common topic.
**What the interviewer is checking:** Do you understand that a shared trend creates correlation (spurious correlation) and know how to remove it?
**Say this in the interview:** "If both series rise over time, they will correlate simply because both go up, not because one drives the other. I would remove the trend, for example by looking at year-on-year changes, and then check whether the relationship survives."
**Explain simply:**
- **Spurious correlation** = a strong correlation with no real link, often because of a shared third factor, here **time itself**.
- Anything that grows steadily (headcount, tea-cup sales, rent) correlates with anything else that grows.
- Fix: **differencing** (use the change from one period to the next) or detrending, then recompute.
- Related risk: random-walk series can look correlated by pure chance.
**Worked example:** Over 15 years, company headcount and canteen tea cups sold both rise steadily and are unrelated by design. Their raw correlation is 0.984. Using year-on-year changes, it falls to -0.397 (small sample noise, not a real link).
**Excel / Python:**
```python
import numpy as np

# 15 years of two unrelated numbers that both just grow over time
random_generator = np.random.default_rng(3)
year_number = np.arange(15)
company_headcount = 200 + 20 * year_number + random_generator.normal(0, 8, 15)
canteen_tea_cups_sold = 5000 + 300 * year_number + random_generator.normal(0, 150, 15)

# Correlation of the raw levels (both trend upward)
level_correlation = np.corrcoef(company_headcount, canteen_tea_cups_sold)[0, 1]

# Remove the trend by using year-on-year changes instead
headcount_change = np.diff(company_headcount)
tea_cups_change = np.diff(canteen_tea_cups_sold)
change_correlation = np.corrcoef(headcount_change, tea_cups_change)[0, 1]

print("Correlation of levels: ", round(level_correlation, 3))
print("Correlation of changes:", round(change_correlation, 3))
```
Output:
```
Correlation of levels:  0.984
Correlation of changes: -0.397
```
The near-perfect correlation of levels came from the shared upward trend; once the trend is removed, the link disappears (with only 14 changes, -0.397 is within chance).
**Likely follow-ups:** 1) *What is differencing?* Subtracting the previous value from each value. 2) *Any other fix?* Detrend by regressing on time and correlating the leftovers.
**Common mistakes:** Reporting the correlation of two trending series as evidence of a relationship.

### Q43 ⭐ 🟡 What does ordinary least squares minimise?
**Asked at:** commonly asked (no company-specific report found); a core definition in regression sources.
**What the interviewer is checking:** Do you know exactly what "best fit line" means?
**Say this in the interview:** "OLS picks the line that minimises the sum of the squared residuals, the vertical gaps between each actual point and the line."
**Explain simply:**
- A **residual** is actual value minus predicted value (the vertical gap).
- OLS squares every gap, adds them up, and chooses the intercept and slope giving the smallest total (the **sum of squared errors**, SSE).
- Squaring stops positive and negative gaps cancelling, and punishes big misses more.
- Because of squaring, one outlier can pull the line noticeably.
**Formula in plain words:** Add up (actual - predicted) squared for every person; choose the line that makes this total smallest. In symbols: minimise sum of (y_i - a - b x_i)^2.
**Worked example:** Experience x = 1 to 5 with skill ratings y = 2, 4, 5, 4, 5. The best line is y = 2.2 + 0.6x with SSE 2.4. Nudging the slope to 0.8 raises SSE to 4.6; nudging the intercept to 2.8 raises it to 4.2.
**Excel / Python:**
```python
import numpy as np

# Small dataset: x = years of experience, y = skill rating
x_values = np.array([1, 2, 3, 4, 5])
y_values = np.array([2, 4, 5, 4, 5])

# Function that adds up the squared gaps between the points and a line
def sum_of_squared_errors(intercept, slope):
    predicted_values = intercept + slope * x_values
    gaps = y_values - predicted_values
    return np.sum(gaps ** 2)

# The least squares line, found by np.polyfit
best_slope, best_intercept = np.polyfit(x_values, y_values, 1)

print("Best line: intercept", round(best_intercept, 2), "slope", round(best_slope, 2))
print("Sum of squared errors, best line:      ", round(sum_of_squared_errors(best_intercept, best_slope), 2))
print("Sum of squared errors, nudged slope:   ", round(sum_of_squared_errors(best_intercept, 0.8), 2))
print("Sum of squared errors, nudged intercept:", round(sum_of_squared_errors(2.8, best_slope), 2))
```
Output:
```
Best line: intercept 2.2 slope 0.6
Sum of squared errors, best line:       2.4
Sum of squared errors, nudged slope:    4.6
Sum of squared errors, nudged intercept: 4.2
```
Any other line gives a larger total than the OLS line. In Excel, `=SLOPE(y_range, x_range)` and `=INTERCEPT(y_range, x_range)` return the same line.
**Likely follow-ups:** 1) *Why squares, not absolute values?* Squares are smooth to optimise, have a neat formula, and penalise large errors; absolute errors resist outliers more. 2) *Does OLS minimise horizontal gaps?* No, vertical ones only.
**Common mistakes:** Saying it minimises the sum of residuals (that is always zero for OLS with an intercept).

### Q44 ⭐ 🟡 What are MAE and RMSE, and how are they different from R²?
**Asked at:** commonly asked (no company-specific report found); R-squared is cited across the sources file, error metrics are standard follow-ups.
**What the interviewer is checking:** Can you describe error in real units versus a relative fit score, and say when each is better?
**Say this in the interview:** "MAE is the average miss in the original units; RMSE is similar but punishes big misses harder; R-squared is the share of variation the model explains, with no units. I report MAE or RMSE to say how far off we are in practice."
**Explain simply:**
- **MAE (mean absolute error):** average size of the gaps, ignoring sign. Easy to explain: "off by 3 hours on average."
- **RMSE (root mean squared error):** square the gaps, average, take the square root. Larger errors count more, so it is always at least as big as MAE.
- **R-squared:** 1 minus (leftover error / error from just guessing the average). It is a share between 0 and 1 for a good model, not an error size.
- A model can have a high R² and still miss by a lot in real terms; MAE and RMSE show that.
**Formula in plain words:** MAE = average of |actual - predicted|. RMSE = square root of the average of (actual - predicted) squared. R² = 1 - (total squared errors / total squared distance from the mean).
**Worked example:** Overtime hours for 5 employees: actual 10, 12, 15, 20, 40 and predicted 11, 11, 16, 18, 30. MAE = 3.0 hours, RMSE = 4.63 hours (pulled up by the 10-hour miss), R² = 0.818.
**Excel / Python:**
```python
import numpy as np

# Actual and predicted monthly overtime hours for 5 employees
actual_hours = np.array([10, 12, 15, 20, 40])
predicted_hours = np.array([11, 11, 16, 18, 30])

# Gap between actual and predicted for each person
errors = actual_hours - predicted_hours

# MAE: average size of the gaps, ignoring direction
mean_absolute_error = np.mean(np.abs(errors))

# RMSE: square the gaps, average them, then take the square root
root_mean_squared_error = np.sqrt(np.mean(errors ** 2))

# R-squared: 1 minus (leftover error / error of just guessing the average)
sum_of_squared_errors = np.sum(errors ** 2)
total_variation = np.sum((actual_hours - actual_hours.mean()) ** 2)
r_squared = 1 - sum_of_squared_errors / total_variation

print("MAE: ", round(mean_absolute_error, 2), "hours")
print("RMSE:", round(root_mean_squared_error, 2), "hours")
print("R-squared:", round(r_squared, 3))
```
Output:
```
MAE:  3.0 hours
RMSE: 4.63 hours
R-squared: 0.818
```
On average the model misses by 3 hours, with the one big miss (40 vs 30) lifting RMSE above MAE. In Excel: `=SUMPRODUCT(ABS(A2:A6-B2:B6))/5` for MAE (actual in A, predicted in B); `=SQRT(SUMXMY2(A2:A6,B2:B6)/5)` for RMSE (not run in Excel here).
**Likely follow-ups:** 1) *When prefer RMSE?* When large errors are especially costly. 2) *When prefer MAE?* When outliers should not dominate.
**Common mistakes:** Comparing MAE across variables with different units; assuming a high R² means small errors.

### Q45 ⭐ 🟡 A correlation of 0.3 is found. How do you decide whether it is statistically significant, and how does sample size matter?
**Asked at:** p-values in regression were reported for a Tiger Analytics business analyst candidate (Interview Query, via search summary, candidate-reported); this exact framing is commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know significance depends on both the size of r and the sample size, and that significant is not the same as important?
**Say this in the interview:** "I test whether the true correlation could be zero using a t-test. With r = 0.3, it is not significant with 20 people but becomes significant at about 44 or more, because bigger samples make the same r more convincing. Significant only means unlikely to be chance, not that the link is strong."
**Explain simply:**
- **Null hypothesis:** the true correlation is 0. The **p-value** is the chance of seeing a correlation this large if it really were 0.
- The test converts r to a t value: larger r or larger n gives a larger t and a smaller p-value.
- Rule of thumb for 5% significance: r = 0.3 needs roughly n = 44 or more.
- A weak r (0.3 explains only 9% of the variation) can be "significant" with big data, so also report the size and a confidence interval.
**Formula in plain words:** t = r x square root of (n - 2) divided by square root of (1 - r squared), with n - 2 degrees of freedom.
**Worked example:** The same r = 0.3: with 20 employees p = 0.1988 (not significant); with 50, p = 0.0343 (significant at 5%); with 200, p is below 0.0001.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

observed_correlation = 0.3

# For each sample size, turn r into a t value and then into a two-sided p-value
for sample_size in [10, 20, 50, 100, 200]:
    degrees_of_freedom = sample_size - 2
    t_value = observed_correlation * np.sqrt(degrees_of_freedom) / np.sqrt(1 - observed_correlation ** 2)
    p_value = 2 * stats.t.sf(abs(t_value), degrees_of_freedom)
    print("n =", sample_size, "| t =", round(t_value, 2), "| p =", format(p_value, ".4f"))
```
Output:
```
n = 10 | t = 0.89 | p = 0.3997
n = 20 | t = 1.33 | p = 0.1988
n = 50 | t = 2.18 | p = 0.0343
n = 100 | t = 3.11 | p = 0.0024
n = 200 | t = 4.43 | p = 0.0000
```
The correlation stays 0.3 throughout; only the evidence grows with sample size. Excel: `=T.DIST.2T(ABS(t), n-2)` gives the p-value (Excel 2010+; not run in Excel here).
**Likely follow-ups:** 1) *Is r = 0.3 strong?* Weak to moderate; R² = 0.09. 2) *Better than a p-value?* A confidence interval for r.
**Common mistakes:** Saying 0.3 is "not significant" without mentioning n; treating a significant result as a big effect.

### Q46 ⭐ 🟡 How do the slope and the correlation coefficient change if you change the units of a variable, for example salary in rupees versus lakhs?
**Asked at:** commonly asked (no company-specific report found); a standard conceptual check on slope vs correlation.
**What the interviewer is checking:** Do you know slope depends on units while correlation does not?
**Say this in the interview:** "The correlation does not change at all, because it has no units. The slope changes by the same factor as the unit: salary in lakhs gives a slope 100,000 times smaller than in rupees."
**Explain simply:**
- Correlation is a unit-free score; rescaling a variable (multiplying or dividing by a positive number, or shifting it) leaves it unchanged.
- Slope = change in y per one unit of x, so if y is measured in bigger units, the slope shrinks proportionally.
- If you rescale x instead (e.g. months to years), the slope grows by that factor.
- Flipping the sign of a variable flips the sign of both r and the slope.
**Worked example:** Six employees, experience 1 to 6 years. In rupees, slope is 91,714.29 per year; in lakhs, it is 0.92 per year. Correlation is 0.9961 both times.
**Excel / Python:**
```python
import numpy as np

# Years of experience and salary in rupees for 6 employees
years_of_experience = np.array([1, 2, 3, 4, 5, 6])
salary_in_rupees = np.array([400000, 520000, 610000, 700000, 760000, 880000])

# The same salaries in lakhs (1 lakh = 100,000 rupees)
salary_in_lakhs = salary_in_rupees / 100000

for label, salary in [("Rupees", salary_in_rupees), ("Lakhs", salary_in_lakhs)]:
    correlation = np.corrcoef(years_of_experience, salary)[0, 1]
    slope = np.polyfit(years_of_experience, salary, 1)[0]
    print(label, "-> correlation:", round(correlation, 4), "| slope:", round(slope, 2))
```
Output:
```
Rupees -> correlation: 0.9961 | slope: 91714.29
Lakhs -> correlation: 0.9961 | slope: 0.92
```
Same relationship, same correlation; only the slope's units changed. In Excel, `=CORREL()` and `=SLOPE()` behave the same way.
**Likely follow-ups:** 1) *So can you compare slopes across variables?* Not directly; standardise first (see Q54). 2) *Does adding a constant change the slope?* No, only the intercept.
**Common mistakes:** Thinking a "bigger" slope in rupees means a stronger relationship.

### Q47 ⭐ 🟡 What is partial correlation or controlling for a variable?
**Asked at:** commonly asked (no company-specific report found); related to confounders, a topic the sources file reports as asked with company data examples.
**What the interviewer is checking:** Do you understand how to measure a relationship after removing the influence of a third variable?
**Say this in the interview:** "Partial correlation is the correlation between two variables after taking out the part of each that is explained by a third variable. It answers: among people of the same age, is tenure still linked to salary?"
**Explain simply:**
- Simple correlation mixes the direct link with the effect of other variables.
- To control for a variable (say age): predict tenure from age, predict salary from age, keep the leftovers (residuals), and correlate the leftovers.
- If the correlation collapses, the original link was mostly due to the third variable.
- Multiple regression does the same job: each coefficient is "holding the other variables fixed".
**Worked example:** Simulated 400 employees: age drives both tenure and salary. Tenure and salary correlate 0.819, but controlling for age the partial correlation is only 0.026, so tenure adds essentially nothing beyond age here.
**Excel / Python:**
```python
import numpy as np

# Simulate 400 employees: age drives both tenure and salary; tenure has no extra effect
random_generator = np.random.default_rng(5)
age = random_generator.uniform(22, 55, 400)
tenure_years = 0.6 * (age - 22) + random_generator.normal(0, 2, 400)
salary_in_lakhs = 3 + 0.25 * (age - 22) + random_generator.normal(0, 1.5, 400)

# Simple correlation between tenure and salary
simple_correlation = np.corrcoef(tenure_years, salary_in_lakhs)[0, 1]

# Remove the part of tenure explained by age, and the part of salary explained by age
tenure_slope, tenure_intercept = np.polyfit(age, tenure_years, 1)
tenure_leftover = tenure_years - (tenure_intercept + tenure_slope * age)
salary_slope, salary_intercept = np.polyfit(age, salary_in_lakhs, 1)
salary_leftover = salary_in_lakhs - (salary_intercept + salary_slope * age)

# Correlation of the leftovers = partial correlation, controlling for age
partial_correlation = np.corrcoef(tenure_leftover, salary_leftover)[0, 1]

print("Simple correlation (tenure, salary):", round(simple_correlation, 3))
print("Partial correlation, controlling for age:", round(partial_correlation, 3))
```
Output:
```
Simple correlation (tenure, salary): 0.819
Partial correlation, controlling for age: 0.026
```
Once age is held fixed, tenure and salary are essentially unrelated.
**Likely follow-ups:** 1) *How is it different from multiple regression?* Same idea; regression gives slopes, partial correlation gives a unit-free score. 2) *Can it prove causation?* No.
**Common mistakes:** Controlling for the wrong variable (a mediator, Q53); forgetting it only removes linear effects.

### Q48 ⭐ 🟡 What is the standard error of a regression coefficient, and how does it give a confidence interval?
**Asked at:** coefficient and p-value interpretation are reported for a Tiger Analytics business analyst candidate (via search summary); this exact question is commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the standard error measures the uncertainty of an estimated slope, and how it turns into an interval?
**Say this in the interview:** "The standard error tells me how much the estimated slope would typically vary if I repeated the study with different samples. A 95% confidence interval is the slope plus or minus about two standard errors, more precisely the critical t value times the standard error."
**Explain simply:**
- The slope from your data is an estimate; a different sample gives a slightly different slope. The **standard error (SE)** is the typical size of that wobble.
- Smaller SE (more data, less scatter, wider spread in x) means a more precise slope.
- **95% confidence interval** = slope plus or minus (critical t value x SE); the critical t is about 2 for large samples and larger for small ones.
- If the interval excludes 0, the coefficient is significant at 5%. The t statistic in the output is slope / SE.
**Formula in plain words:** Interval = slope - t x SE to slope + t x SE, where t comes from the t-table for (n - 2) degrees of freedom.
**Worked example:** Experience vs salary for 8 employees: slope 0.676 lakhs per year, SE 0.058. With 6 degrees of freedom the critical t is 2.447, giving 0.676 plus or minus 0.142, i.e. 0.535 to 0.817.
**Excel / Python:**
```python
import numpy as np
from scipy import stats
import statsmodels.api as sm

# Years of experience and salary (lakhs) for 8 employees
years_of_experience = np.array([1, 2, 3, 4, 5, 6, 7, 8])
salary_in_lakhs = np.array([4.0, 5.2, 6.1, 6.9, 7.6, 8.1, 8.5, 8.8])

# Fit the model
model = sm.OLS(salary_in_lakhs, sm.add_constant(years_of_experience)).fit()
slope = model.params[1]
standard_error = model.bse[1]

# 95% confidence interval = slope +/- (critical t value) x standard error
degrees_of_freedom = len(salary_in_lakhs) - 2
critical_t = stats.t.ppf(0.975, degrees_of_freedom)
lower_limit = slope - critical_t * standard_error
upper_limit = slope + critical_t * standard_error

print("Slope:", round(slope, 3), "| Standard error:", round(standard_error, 3))
print("Critical t (6 df):", round(critical_t, 3))
print("95% CI by hand:", round(lower_limit, 3), "to", round(upper_limit, 3))
print("95% CI from statsmodels:", model.conf_int()[1].round(3))
```
Output:
```
Slope: 0.676 | Standard error: 0.058
Critical t (6 df): 2.447
95% CI by hand: 0.535 to 0.817
95% CI from statsmodels: [0.535 0.817]
```
Our hand calculation matches the library. We are 95% confident the true gain is between 0.535 and 0.817 lakhs per year. In Excel, Data Analysis > Regression prints the SE and the lower/upper 95% columns directly (not run in Excel here).
**Likely follow-ups:** 1) *How does it relate to the p-value?* p comes from t = slope / SE. 2) *How to shrink SE?* More data, wider spread of x, less noise.
**Common mistakes:** Saying "95% chance the true slope is in this interval" for one fixed interval; confusing SE with the standard deviation of the data.

### Q49 ⭐ 🔴 What is the F-test in regression output, and how is it different from the t-test on a coefficient?
**Asked at:** commonly asked (no company-specific report found); regression output interpretation is a repeated theme in the sources file.
**What the interviewer is checking:** Do you know the F-test is about the model as a whole and t-tests are about single predictors?
**Say this in the interview:** "The F-test asks whether all the predictors together explain anything, that is, whether the model is better than just using the average. Each t-test asks whether one specific predictor adds something. With one predictor, F equals t squared."
**Explain simply:**
- **F-test (overall):** null hypothesis is that every slope is 0. A small p-value means at least one predictor matters.
- **t-test (per coefficient):** null hypothesis is that this one slope is 0, holding others fixed.
- You can see a significant F with no individually significant t when predictors overlap heavily (multicollinearity).
- With a single predictor the two tests give the same p-value.
**Worked example:** Simulated engagement data: tenure and manager rating truly matter; commute does not. The F-test gives F = 29.91, p = 9.65e-14 (the model as a whole is useful). The t-tests show tenure and manager rating are significant and commute is not (p = 0.9906).
**Excel / Python:**
```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# Simulate 100 employees: engagement depends on tenure and manager rating; commute is noise
random_generator = np.random.default_rng(21)
employees = pd.DataFrame({
    "tenure_years": random_generator.uniform(0, 10, 100),
    "manager_rating": random_generator.uniform(1, 5, 100),
    "commute_km": random_generator.uniform(1, 30, 100),
})
employees["engagement"] = (3 + 0.2 * employees["tenure_years"] + 0.5 * employees["manager_rating"]
                           + random_generator.normal(0, 1, 100))

model = smf.ols("engagement ~ tenure_years + manager_rating + commute_km", data=employees).fit()

# One F-test for the whole model, then one t-test per predictor
print("F-test: F =", round(model.fvalue, 2), "| p =", format(model.f_pvalue, ".2e"))
print("t-test p-values per predictor:")
print(model.pvalues.round(4))
```
Output:
```
F-test: F = 29.91 | p = 9.65e-14
t-test p-values per predictor:
Intercept         0.0000
tenure_years      0.0000
manager_rating    0.0000
commute_km        0.9906
dtype: float64
```
The model as a whole is useful, and only commute fails to add anything. In Excel's regression output, "Significance F" is the F-test p-value and the "P-value" column holds the t-tests.
**Likely follow-ups:** 1) *Can F be significant while no t is?* Yes, with correlated predictors. 2) *What is F, roughly?* Explained variation per predictor divided by unexplained variation per leftover degree of freedom.
**Common mistakes:** Treating a significant F as proof every predictor matters.

### Q50 ⭐ 🔴 What is autocorrelation of residuals, and when does it matter?
**Asked at:** commonly asked (no company-specific report found); a differentiator question on regression assumptions (the sources file notes assumptions are a repeated opener).
**What the interviewer is checking:** Do you know the residual-independence assumption and that it mainly bites with time-ordered data?
**Say this in the interview:** "Autocorrelation means today's residual is related to yesterday's, so the errors are not independent. It matters mostly for time series such as monthly attrition, where it makes standard errors too small and p-values too optimistic. I check it with a residual-over-time plot and the Durbin-Watson test."
**Explain simply:**
- Normally the leftover errors should look like random noise. In **autocorrelation**, a high error tends to be followed by another high error (positive autocorrelation).
- Typical cause: data ordered in time with momentum, seasonality, or a missing variable that changes slowly.
- Effect: coefficients are still unbiased, but standard errors are understated, so you may call things significant that are not.
- **Durbin-Watson** statistic: about 2 means none; well below 2 means positive autocorrelation; above 2 means negative.
- Fixes: add a lag or trend/seasonal terms, use time-series models, or robust (HAC) standard errors.
**Worked example:** 36 months of simulated attrition with errors that carry over from month to month. The Durbin-Watson is 0.55 (far below 2) and each residual correlates 0.71 with the previous month's.
**Excel / Python:**
```python
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson

# 36 months of headcount-based attrition, with leftover effects that carry over month to month
random_generator = np.random.default_rng(9)
month_number = np.arange(36)
carry_over_noise = np.zeros(36)
for month in range(1, 36):
    carry_over_noise[month] = 0.8 * carry_over_noise[month - 1] + random_generator.normal(0, 0.5)
attrition_percent = 10 + 0.05 * month_number + carry_over_noise

# Fit a straight-line trend and look at the residuals
model = sm.OLS(attrition_percent, sm.add_constant(month_number)).fit()
residuals = model.resid

# Durbin-Watson: about 2 = no autocorrelation; well below 2 = positive autocorrelation
print("Durbin-Watson:", round(durbin_watson(residuals), 2))

# Correlation of each residual with the previous month's residual
lag_one_correlation = np.corrcoef(residuals[1:], residuals[:-1])[0, 1]
print("Correlation with previous month's residual:", round(lag_one_correlation, 2))
```
Output:
```
Durbin-Watson: 0.55
Correlation with previous month's residual: 0.71
```
Both numbers say residuals are strongly linked to the previous month, so the plain p-values should not be trusted.
**Likely follow-ups:** 1) *Does it matter for survey data of different people?* Usually not, unless the order or grouping creates dependence. 2) *Does it bias the slope?* Not usually, it distorts the uncertainty.
**Common mistakes:** Applying Durbin-Watson to data with no natural order.

### Q51 ⭐ 🔴 What is the dummy variable trap?
**Asked at:** commonly asked (no company-specific report found); a differentiator on categorical variables and multicollinearity.
**What the interviewer is checking:** Do you know why you must leave one category out?
**Say this in the interview:** "If I create a 0/1 column for every category and also keep the intercept, the dummy columns add up to exactly 1 and duplicate the intercept. That is perfect multicollinearity, so the model cannot separate the effects. The fix is to drop one category as the baseline."
**Explain simply:**
- For 3 departments (HR, IT, Sales), every employee has exactly one 1 across the three dummy columns.
- So the three columns always sum to the intercept column of all 1s: one column is fully predictable from the others.
- The regression then has no unique answer (software errors out or returns arbitrary numbers).
- Fix: use k - 1 dummies, or drop the intercept (less common, harder to read).
**Worked example:** For 6 employees across 3 departments, the trap matrix has 4 columns but only 3 independent ones (rank 3). Dropping one dummy gives 3 columns, all independent.
**Excel / Python:**
```python
import numpy as np
import pandas as pd

# 6 employees across 3 departments
employees = pd.DataFrame({"department": ["Sales", "HR", "IT", "Sales", "HR", "IT"]})

# Trap: make a column for EVERY department and also add an intercept column of 1s
all_dummies = pd.get_dummies(employees["department"], dtype=int)
trap_matrix = all_dummies.copy()
trap_matrix.insert(0, "intercept", 1)

# Safe: drop one department (it becomes the baseline)
safe_dummies = pd.get_dummies(employees["department"], drop_first=True, dtype=int)
safe_matrix = safe_dummies.copy()
safe_matrix.insert(0, "intercept", 1)

# Rank = number of truly independent columns
print("Trap matrix: columns =", trap_matrix.shape[1], "| independent columns =", np.linalg.matrix_rank(trap_matrix))
print("Safe matrix: columns =", safe_matrix.shape[1], "| independent columns =", np.linalg.matrix_rank(safe_matrix))
print(trap_matrix)
```
Output:
```
Trap matrix: columns = 4 | independent columns = 3
Safe matrix: columns = 3 | independent columns = 3
   intercept  HR  IT  Sales
0          1   0   0      1
1          1   1   0      0
2          1   0   1      0
3          1   0   0      1
4          1   1   0      0
5          1   0   1      0
```
In the trap matrix, intercept = HR + IT + Sales in every row, so one column is redundant. (In pandas, `drop_first=True` drops the alphabetically first category, here HR.)
**Likely follow-ups:** 1) *Does the choice of dropped category change predictions?* No, only how coefficients read. 2) *Is it the same as multicollinearity?* It is the extreme case, perfect multicollinearity.
**Common mistakes:** Keeping all dummies plus intercept; forgetting which category is the baseline when explaining coefficients.

### Q52 ⭐ 🔴 When would you take the log of a variable in a regression, and how does it change the interpretation?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Do you know when a log helps (skewed data, percentage effects, fanning residuals) and how to read the coefficient?
**Say this in the interview:** "I take the log of a skewed, always-positive variable like salary, or when I believe effects are in percentages. In a log-salary model, a coefficient of 0.06 means about 6% higher salary per extra year rather than a fixed number of lakhs."
**Explain simply:**
- Use a log when the variable is right-skewed (salary, revenue), when relationships are multiplicative, or when residual spread grows with the level (Q41).
- **Log-level** (log y on x): a one-unit rise in x changes y by about (coefficient x 100)%, more exactly (e^coefficient - 1) x 100%.
- **Log-log** (log y on log x): the coefficient is an **elasticity**, i.e. the % change in y for a 1% change in x.
- **Level-log** (y on log x): a 1% rise in x changes y by about coefficient / 100 units.
- Logs only work for positive values; zeros need handling (e.g. log(1 + x)).
**Worked example:** 300 simulated employees where each year of experience raises salary about 6%. The plain model says +0.38 lakhs per year (fine for juniors, too small for seniors). The log model gives slope 0.0589, i.e. about 6.1% more salary per year.
**Excel / Python:**
```python
import numpy as np
import statsmodels.api as sm

# Simulate 300 employees where each extra year adds about 6% to salary (salary is right-skewed)
random_generator = np.random.default_rng(2)
years_of_experience = random_generator.uniform(0, 15, 300)
log_salary = np.log(4) + 0.06 * years_of_experience + random_generator.normal(0, 0.15, 300)
salary_in_lakhs = np.exp(log_salary)

predictors = sm.add_constant(years_of_experience)

# Model 1: plain salary (each year adds a fixed number of lakhs)
plain_model = sm.OLS(salary_in_lakhs, predictors).fit()

# Model 2: log of salary (each year multiplies salary by a fixed percentage)
log_model = sm.OLS(np.log(salary_in_lakhs), predictors).fit()

log_slope = log_model.params[1]
percent_change_per_year = (np.exp(log_slope) - 1) * 100

print("Plain model: +", round(plain_model.params[1], 3), "lakhs per year")
print("Log model slope:", round(log_slope, 4))
print("Log model: about", round(percent_change_per_year, 1), "% more salary per year")
```
Output:
```
Plain model: + 0.38 lakhs per year
Log model slope: 0.0589
Log model: about 6.1 % more salary per year
```
The log model matches how pay actually grows (by percentages). In Excel, use `=LN(B2)` for the log column and regress on it.
**Likely follow-ups:** 1) *Why not log everything?* It changes the meaning and fails on zeros or negatives. 2) *Predictions in original units?* Exponentiate, and note a small bias correction may be needed.
**Common mistakes:** Reading a log coefficient as a unit change; forgetting that the "x100 percent" shortcut is only good for small coefficients.

### Q53 ⭐ 🔴 What is the difference between a confounder, a mediator and a moderator?
**Asked at:** confounder questions are reported with company-style data examples (PracHub, Uber confounding prompt, via the sources file); the three-way contrast is commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you place a third variable correctly in the cause-and-effect story and say what to do with it?
**Say this in the interview:** "A confounder causes both the supposed cause and the effect, so I control for it. A mediator sits in between: the cause works through it, so I usually should not control for it if I want the total effect. A moderator changes the strength of the relationship, so I model it with an interaction."
**Explain simply:**
- **Confounder:** a common cause. Tenure raises both training attendance and performance, creating a fake link between training and performance. Control for it.
- **Mediator:** the mechanism. Training builds skills, and skills raise performance (training -> skills -> performance). Controlling for it hides part of the real effect.
- **Moderator:** a "depends on" variable. Training helps new joiners a lot but veterans little. Include an interaction term (training x role), or analyse the groups separately.
- A quick test: ask "does it cause both?" (confounder), "is it on the path between?" (mediator), "does the effect differ across its levels?" (moderator).
**Worked example:** Training hours vs performance for two groups. New joiners gain 0.6 points per training hour, veterans only 0.1. Role moderates the training effect.
**Excel / Python:**
```python
import numpy as np

# Moderator example: does the effect of training hours on performance depend on role?
training_hours = np.array([0, 10, 20, 30])
performance_new_joiners = np.array([60, 66, 72, 78])
performance_veterans = np.array([70, 71, 72, 73])

slope_new_joiners = np.polyfit(training_hours, performance_new_joiners, 1)[0]
slope_veterans = np.polyfit(training_hours, performance_veterans, 1)[0]

# Same predictor, different slope in each group: that is moderation
print("Points gained per training hour, new joiners:", round(slope_new_joiners, 2))
print("Points gained per training hour, veterans:   ", round(slope_veterans, 2))
```
Output:
```
Points gained per training hour, new joiners: 0.6
Points gained per training hour, veterans:    0.1
```
The slope differs by group, which is what moderation means. For the confounder case with numbers, see Q40.
**Likely follow-ups:** 1) *Can a variable be more than one type?* The role depends on your causal story, not the data alone. 2) *What is a collider?* A variable caused by both the cause and the effect; controlling for it creates a fake link.
**Common mistakes:** Controlling for a mediator and concluding the cause has no effect; mixing up confounder with moderator.

### Q54 ⭐ 🔴 Two predictors have different units. How do you judge which one matters more in the regression?
**Asked at:** commonly asked (no company-specific report found); coefficient interpretation is a staple regression topic in the sources file.
**What the interviewer is checking:** Do you know raw coefficients are not comparable across units, and how standardising fixes that?
**Say this in the interview:** "I cannot compare raw coefficients because they depend on units: rupees versus years. I standardise each variable (subtract its mean, divide by its standard deviation) and compare the standardised, or beta, coefficients, which say how many standard deviations the outcome moves per one standard deviation of the predictor."
**Explain simply:**
- A raw coefficient is "change in y per one unit of x", so a rupee-based predictor always looks tiny and a years-based one looks big.
- **Standardising** puts every variable on the same scale (standard deviations), so the coefficients become comparable.
- The bigger the absolute standardised coefficient, the more y moves per typical change in that predictor, holding the others fixed.
- Caveats: correlated predictors make the ranking unstable; "matters more" means statistical size, not business importance or causation.
**Worked example:** Simulated engagement on salary (rupees) and tenure (years). Raw: 0.00000135 points per rupee versus 0.173 per year, which looks like tenure is 100,000 times stronger. Standardised: salary 0.351 and tenure 0.444, so tenure matters somewhat more, not massively.
**Excel / Python:**
```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# Simulate 300 employees: salary in rupees (big numbers), tenure in years (small numbers)
random_generator = np.random.default_rng(4)
employees = pd.DataFrame({
    "salary_in_rupees": random_generator.normal(900000, 250000, 300),
    "tenure_years": random_generator.normal(5, 2.5, 300),
})
employees["engagement"] = (5 + 0.000001 * employees["salary_in_rupees"] + 0.15 * employees["tenure_years"]
                           + random_generator.normal(0, 0.8, 300))

# Raw coefficients: not comparable because the units differ
raw_model = smf.ols("engagement ~ salary_in_rupees + tenure_years", data=employees).fit()

# Standardise every column: subtract its average, divide by its standard deviation
standardised = (employees - employees.mean()) / employees.std()
standardised_model = smf.ols("engagement ~ salary_in_rupees + tenure_years", data=standardised).fit()

print("Raw coefficient, engagement points per extra rupee:", format(raw_model.params["salary_in_rupees"], ".8f"))
print("Raw coefficient, engagement points per extra year:  ", round(raw_model.params["tenure_years"], 3))
print("Standardised coefficients:")
print(standardised_model.params[["salary_in_rupees", "tenure_years"]].round(3))
```
Output:
```
Raw coefficient, engagement points per extra rupee: 0.00000135
Raw coefficient, engagement points per extra year:   0.173
Standardised coefficients:
salary_in_rupees    0.351
tenure_years        0.444
dtype: float64
```
On the same scale, tenure is only modestly ahead of salary. In Excel, standardise with `=STANDARDIZE(x, AVERAGE(range), STDEV.S(range))` (Excel 2010+; not run in Excel here) before running the regression.
**Likely follow-ups:** 1) *Other ways?* Drop-one comparisons of R², or permutation importance. 2) *Does standardising change the fit?* No, only the coefficient scale.
**Common mistakes:** Comparing raw coefficients or raw p-values across units; ignoring multicollinearity.
