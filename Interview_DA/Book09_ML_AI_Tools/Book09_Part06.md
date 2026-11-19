# Book 9 — Basic ML + AI Tools for Analysts | Part 6: Overfitting, Train/Test Split, Feature Engineering Basics 🟡

**Target:** 38 questions | **Actual:** 39 questions
**Scope:** overfitting and underfitting, train/validation/test splits and sklearn train_test_split, cross-validation, data leakage, and basic feature engineering (encoding, scaling, missing values, outliers, derived features) for a 0-3 year analyst.

### Q1 ⭐⭐⭐ 🟢 What is overfitting? Explain it with a simple example to a non-technical manager.
**Asked at:** commonly asked (no company-specific report found); overfitting definitions open most prep-site ML lists (PracHub, FACE Prep, Dataford style pages, seen only as search snippets, unverified as real company questions).
**What the interviewer is checking:** Whether you can explain "memorising versus learning" without jargon and name the tell-tale sign (great on old data, poor on new data).
**Say this in the interview:** "Overfitting is when a model memorises the past data, including its noise, instead of learning the real pattern. It looks excellent on the data it was trained on but does badly on new employees or customers it has never seen."
**Explain simply:**
- A **model** is a rule learned from past rows to predict something about new rows (for example, who might resign).
- Think of a student who memorises last year's question paper. Full marks on that paper, but a new paper exposes that nothing was understood.
- The model has latched onto coincidences (one odd employee who left after a Tuesday birthday) and treats them as rules.
- The sign: **training score** (on rows the model learned from) is high, **test score** (on rows it never saw) is clearly lower.
**Worked example (concept questions):** I simulated 1,000 employees (4 columns: tenure, salary, overtime, engagement; seed 3) and trained a decision tree with no limit on its size. It scored 100% on the training rows but only 64.8% on 250 unseen rows. A smaller tree (3 levels deep) scored 77.7% on training and 72.4% on unseen rows. The simpler model is the better one even though its training score is lower.
**Alternative / pitfalls:** Always judge a model on data it has not seen. A perfect training score is a warning, not a result.
**Likely follow-ups:** 1) *How do you spot it?* Compare training and test scores; a big gap is the signal. 2) *How do you fix it?* Simpler model, more data, fewer features, cross-validation (see Q14).
**Common mistakes:** Celebrating a 100% training score; explaining it with formulas to a manager; confusing it with a model that is just inaccurate everywhere (that is underfitting, Q2).

### Q2 ⭐⭐⭐ 🟢 What is underfitting, and how is it different from overfitting?
**Asked at:** commonly asked (no company-specific report found); underfitting versus overfitting appears in prep-site lists (Dataford, VitalFlux style, snippets only, unverified).
**What the interviewer is checking:** That you know the two failure modes and how the scores reveal each.
**Say this in the interview:** "Underfitting means the model is too simple to capture the real pattern, so it does poorly on both the training data and new data. Overfitting is the opposite: very good on training data, poor on new data."
**Explain simply:**
- Underfit: like predicting every employee's resignation risk using only the company average. Easy, but it ignores everything useful.
- Overfit: like memorising each employee's history. Perfect on the past, useless on new people.
- Scores tell them apart: underfit = low training and low test score; overfit = high training, low test score; good fit = both reasonably high and close.
- Causes of underfitting: too few or uninformative features, a model too simple for the pattern, or too much restriction on the model.
**Worked example (concept questions):** On the simulated attrition data from Q1, a model that always guesses the most common answer scored 54.4% on training and 51.6% on test (both poor, so it underfits). The unlimited tree scored 100% and 64.8% (overfit). The 3-level tree scored 77.7% and 72.4% (a reasonable fit).
**Alternative / pitfalls:** Compare with a naive baseline (always guess the majority). If your model barely beats it, suspect underfitting or weak features.
**Likely follow-ups:** 1) *How do you fix underfitting?* Add useful features, allow a more flexible model, reduce restrictions. 2) *Can a model do both?* Not at once, but moving from simple to complex trades one for the other (Q15).
**Common mistakes:** Saying underfitting is "low accuracy on test only"; adding complexity before checking the data has any signal.

### Q3 ⭐⭐⭐ 🟢 Why do we split data into a training set and a test set instead of evaluating the model on the data it was trained on?
**Asked at:** commonly asked (no company-specific report found); the reason for a train-test split is the opening point in most overfitting and evaluation guides (snippets only, unverified).
**What the interviewer is checking:** That you understand a model must be judged on data it has not seen, because that is what it will face in real use.
**Say this in the interview:** "A model can memorise the rows it was trained on, so its score on them is flattering. I keep some rows aside as a test set; the score on those is an honest estimate of how it will do on new employees or customers."
**Explain simply:**
- **Training set**: rows the model learns from (commonly 70-80%).
- **Test set**: rows hidden from the model until the end, used once to measure performance (commonly 20-30%).
- The question the business cares about is "how will this do next quarter?", not "how well did it remember last quarter?".
- It is like practising on past papers but being marked on a fresh paper.
**Worked example (concept questions):** Same 1,000 simulated employees as Q1, 750 for training and 250 for testing (seed 42 for the split). The unlimited tree scored 100.0% on rows it had trained on, but 64.8% on the 250 held-out rows. Reporting 100% to a manager would have been wrong by 35 points.
**Alternative / pitfalls:** With small data one split is noisy; use cross-validation (Q19). For data over time, hold out the latest months instead of random rows.
**Likely follow-ups:** 1) *What split ratio?* 80/20 or 75/25 is common; no magic number. 2) *Why a third set?* To tune choices without touching the test set (Q9).
**Common mistakes:** Reporting training accuracy; tuning the model repeatedly on the test set; splitting after doing preprocessing that learned from all rows (Q11).

### Q4 ⭐⭐⭐ 🟢 A model for predicting employee attrition has the scores below. What do they suggest, and what would you try next?
Training accuracy = 0.97, test accuracy = 0.71.
**Asked at:** commonly asked (no company-specific report found); reading a train versus test gap is a standard prompt in overfitting guides (snippets only, unverified).
**What the interviewer is checking:** Whether you read the gap (0.97 minus 0.71 = 0.26) as overfitting and propose sensible next steps.
**Say this in the interview:** "A 26-point gap says the model has memorised the training data and is overfitting. The honest number to report is 0.71. I would simplify the model, check for leakage, try cross-validation and then add useful features or more data."
**Explain simply:**
- **Accuracy** is the share of predictions that are correct. 0.97 on training, 0.71 on unseen data.
- A gap this large means the model learned noise. The 0.71 is what to expect in real use, at best.
- Before celebrating 0.71, compare with a baseline: if 70% of employees stay, "everyone stays" already scores 0.70.
- Next steps, in order: limit the model's size (for example a shallower tree), remove noisy columns, use cross-validation for a steadier estimate, then engineer better features or get more rows.
**Worked example (concept questions):** On my simulated data, limiting a tree with `min_samples_leaf=30` (each final group must hold at least 30 employees) cut the gap from 35.2 points (1.000 vs 0.648) to 9.2 points (0.784 vs 0.692), and the test score rose. The training score fell, which is the point.
**Alternative / pitfalls:** If the data is imbalanced (few leavers), accuracy hides problems; also report precision and recall. If a feature leaks the answer, the train score would be high and the test score also high, so a gap alone does not catch it.
**Likely follow-ups:** 1) *Would more data help?* Often, yes, for overfitting. 2) *What if the gap were tiny but both scores low?* That suggests underfitting.
**Common mistakes:** Reporting 0.97; making the model more complex; ignoring the baseline.

### Q5 ⭐⭐⭐ 🟢 What is feature engineering? Give three examples of features you could create for an employee attrition dataset.
**Asked at:** commonly asked (no company-specific report found); feature engineering definitions appear in Board Infinity, Hyring and InterviewBit style lists (snippets only, unverified).
**What the interviewer is checking:** Whether you can turn raw columns into signals that carry meaning for the question.
**Say this in the interview:** "Feature engineering is creating or transforming columns so the model can see patterns more easily. For attrition I would create tenure in months from the hire date, salary compared with the department median, and months since the last promotion."
**Explain simply:**
- A **feature** is an input column the model uses. Engineering means building better ones from raw data.
- Raw dates mean little to a model; the length of time between dates does.
- Ratios and comparisons add context: Rs 40,000 is low in one department and high in another.
- Counts over a window (absences in the last 6 months) capture recent behaviour.
**Worked example (concept questions):** Three employees, features computed with pandas as of 1 Jan 2025.

| tenure_months | salary_vs_dept (salary / dept median) | months_since_promotion |
|---|---|---|
| 34 | 0.80 | 21 |
| 12 | 1.04 | no promotion yet (missing) |
| 66 | 1.25 | 42 |

Employee 1 is paid 20% below the department median and has waited 21 months: a plausible attrition signal that no raw column showed directly.
**Alternative / pitfalls:** Only use information available at prediction time (see Q6). Features that proxy for gender, age or religion can raise fairness and legal concerns; discuss with HR or legal.
**Likely follow-ups:** 1) *Other examples?* Absence days in last 6 months, number of managers in 2 years, commute distance band. 2) *How do you know a feature helps?* Compare test scores with and without it.
**Common mistakes:** Creating features from after-the-event information; making hundreds of features with no reason; forgetting to handle the missing values the new features create.

### Q6 ⭐⭐⭐ 🟢 What is data leakage in a machine learning project? Give one HR or sales example.
**Asked at:** commonly asked (no company-specific report found); leakage is covered on PracHub, Dataford, Educative style pages (snippets only; some pages attribute prompts to named firms, which is unverified).
**What the interviewer is checking:** That you know leakage inflates results and can name a realistic cause.
**Say this in the interview:** "Data leakage is when the model gets information during training that it would not have at the time of a real prediction, so the test score looks great but the model fails in real use. For example, using 'exit interview completed' to predict who will resign."
**Explain simply:**
- Two common kinds: **target leakage** (a feature that is really a consequence of the answer) and **train-test contamination** (test rows influencing training, for example scaling or filling gaps using all rows before the split).
- Exit interview completed, final settlement amount, notice period start date: all exist only after someone resigns.
- Sales example: predicting whether a deal closes using "contract sent" date, which is only filled once a deal is won.
- The giveaway is an unrealistically high score.
**Worked example (concept questions):** In the simulated churn data of Q10 (1,000 customers, 455 churned), the column `account_closed_date` is filled only for churners. A depth-3 tree using it scored 100% on 200 test rows; without it, the real signals gave 67%. The 100% would vanish on live customers, because nobody has a closing date before they close.
**Alternative / pitfalls:** Ask for each feature: "Would I know this on the day I make the prediction?" Also split by time when predicting the future.
**Likely follow-ups:** 1) *How do you detect it?* Suspiciously good scores, one feature dominating importance, features with future dates. 2) *How do you prevent it?* Split first, fit preprocessing on training only, use a Pipeline (Q11).
**Common mistakes:** Confusing leakage with overfitting (leakage gives high test scores too); only checking after deployment.

### Q7 ⭐⭐⭐ 🟡 Read this code and explain what each argument does. With 1,000 rows, how many rows end up in the training and test sets?
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```
**Asked at:** commonly asked (no company-specific report found); train_test_split arguments are a staple of fresher ML screening (snippets only, unverified).
**What the interviewer is checking:** Whether you can read standard sklearn code and do the split arithmetic.
**Say this in the interview:** "It splits the rows randomly into 80% training and 20% test. `X` holds the feature columns, `y` the answer column, `test_size=0.2` sets 20% aside, and `random_state=42` fixes the shuffle so the split is repeatable. With 1,000 rows that gives 800 training and 200 test rows."
**Explain simply:**
- `X`: the input columns (features). `y`: the column to predict (target).
- `test_size=0.2`: 20% of rows go to the test set; the rest (80%) to training.
- `random_state=42`: seeds the random shuffle. Any fixed number works; 42 is just a habit.
- Returns four pieces: training features, test features, training answers, test answers, in that order.
**Sample data:** 1,000 rows, a feature column `a` and a target of 0/1.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.model_selection import train_test_split

X = pd.DataFrame({"a": range(1000)})
y = pd.Series([0, 1] * 500)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(len(X_train), len(X_test))
```
**Output:**
```
800 200
```
**What it means:** 800 rows to learn from, 200 to test on. The same call with the same data always gives the same rows.
**Alternative / pitfalls:** `train_size=0.8` is the equivalent. Add `stratify=y` when the answer is imbalanced (Q8).
**Likely follow-ups:** 1) *What if I drop random_state?* A different split each run (Q16). 2) *Is the split shuffled?* Yes by default.
**Common mistakes:** Swapping the order of the four outputs; thinking 42 means something; forgetting the split must happen before preprocessing that learns from data.

### Q8 ⭐⭐⭐ 🟡 What does stratify=y do in train_test_split, and when would you use it? Using the data below, how many leavers are in the test set?
1,000 employees, 80 of whom left (8%). Call: `train_test_split(X, y, test_size=0.25, stratify=y, random_state=1)`.
**Asked at:** commonly asked (no company-specific report found); stratify and imbalanced splits appear as follow-ups in split guides (snippets only, unverified).
**What the interviewer is checking:** That you know stratification keeps class proportions, and can compute the test count.
**Say this in the interview:** "`stratify=y` makes each part keep the same share of each answer class as the whole data. The test set has 250 employees and 8% of them, so 20, are leavers. I use it when one class is rare."
**Explain simply:**
- Without stratifying, a random split might put 12 leavers in test and 68 in training, or any other mix by luck.
- With it, the test set gets 8% leavers and the training set also gets 8%.
- Test size = 0.25 x 1,000 = 250. Leavers in test = 8% x 250 = 20. Training: 750 rows, 60 leavers.
- Most useful with rare outcomes, small data, and classification (predicting a category).
**Sample data:** 1,000 rows, 80 leavers, as in the question.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.model_selection import train_test_split

X = pd.DataFrame({"a": range(1000)})
y = pd.Series([1] * 80 + [0] * 920)   # 1 = left

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=1
)
print(len(X_test), y_test.sum(), y_train.sum())
```
**Output:**
```
250 20 60
```
**What it means:** 20 leavers in the 250 test rows and 60 in the 750 training rows: 8% in both.
**Alternative / pitfalls:** Not for time-ordered data (split by date instead). `StratifiedKFold` does the same for cross-validation.
**Likely follow-ups:** 1) *Does it fix imbalance?* No, it only keeps proportions; you still need suitable metrics (precision, recall). 2) *Can it be used for a numeric target?* Not directly.
**Common mistakes:** Forgetting `stratify=y`, so a rare class may be almost absent from test; stratifying on `X` instead of `y`.

### Q9 ⭐⭐⭐ 🟡 What is the difference between a training set, a validation set and a test set, and why is the test set kept untouched until the end?
**Asked at:** commonly asked (no company-specific report found); three-way split questions appear in evaluation guides (snippets only, unverified).
**What the interviewer is checking:** That you understand the role of each set and why the test set must stay clean.
**Say this in the interview:** "Training data teaches the model, validation data is for choosing between options such as model type or settings, and test data is used once at the end for an honest final score. If I keep tuning against the test set, it stops being unseen and my final score is optimistic."
**Explain simply:**
- **Training set**: the model learns its rules here.
- **Validation set**: used to compare choices (which features, how deep a tree). You may look at it many times.
- **Test set**: the final exam. Look once.
- Every time you adjust the model based on a score, a little of that data's information leaks into your choices. If that data is the test set, you have no clean data left to judge the result.
**Worked example (concept questions):** 1,000 rows split 60/20/20 gives 600 training, 200 validation and 200 test rows (computed with two `train_test_split` calls, the second splitting the first remainder 75/25). With small data, cross-validation (Q19) replaces the validation set.
**Alternative / pitfalls:** Reusing the test set after looking at the score and then "improving" the model is a quiet form of leakage.
**Likely follow-ups:** 1) *What if a team has tested many ideas on the test set?* Get fresh data or accept the score is optimistic. 2) *Typical sizes?* 60/20/20 or 70/15/15 are common.
**Common mistakes:** Calling validation and test the same thing; tuning on test; using validation rows to train the final model without telling anyone.

### Q10 ⭐⭐⭐ 🟡 Your churn model scores 99% on the test set. What would make you suspicious, and how would you check for leakage?
One of the features is `account_closed_date`, which is empty for customers who are still active.
**Asked at:** commonly asked (no company-specific report found); leakage-diagnosis prompts appear on PracHub and Dataford style pages (snippets only, unverified).
**What the interviewer is checking:** Whether a surprisingly high score makes you investigate rather than celebrate, and whether you can spot a column that reveals the answer.
**Say this in the interview:** "99% is too good, so I suspect leakage. `account_closed_date` is only filled once a customer has already churned, so it gives away the answer. I would check which feature dominates, cross-tab it against churn, and retrain without it."
**Explain simply:**
- Red flags: near-perfect score, one feature carrying almost all importance, a feature recorded after the outcome.
- `account_closed_date` is empty for active customers and filled for churned ones, so "has a date" equals "churned".
- Checks: cross-tabulate suspect columns with the target; look at feature importance; ask the business when each column is filled in; retrain without it and see how far the score falls.
**Sample data:** I simulated 1,000 customers (tenure, bill, support calls, churned, account_closed_date; seed 42), with 455 churners. `customers` is that table.
**Code (what you write in the interview):**
```python
# Does "has a closed date" simply equal "churned"?
print(pd.crosstab(customers["account_closed_date"].notna(),
                  customers["churned"],
                  rownames=["has_closed_date"]))
```
**Output:**
```
churned            0    1
has_closed_date          
False            545    0
True               0  455
```
**What it means:** The two are identical, so the column is the answer in disguise. A depth-3 tree using it scored 100% on test and gave it 100% of the importance; without it, the score was 67% (the honest figure).
**Alternative / pitfalls:** Not every leak is this obvious; check each feature's timing with the data owner. Also check for duplicate rows across train and test.
**Likely follow-ups:** 1) *Would you keep the column if it were useful?* Only if it is known at prediction time; it is not. 2) *What would you report?* The score without the leaking column.
**Common mistakes:** Trusting the 99% and deploying; dropping the column without understanding why; assuming leakage always shows up as a high-importance column.

### Q11 ⭐⭐⭐ 🟡 What is wrong with this code, and how would you fix it?
```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)
```
**Asked at:** commonly asked (no company-specific report found); "fit preprocessing before the split" is a classic leakage trap in prep guides (snippets only, unverified).
**What the interviewer is checking:** That you know scaling must learn its mean and spread from training rows only.
**Say this in the interview:** "The scaler is fitted on all rows, so the test rows influence the mean and spread used to scale training data. That is leakage. I would split first, fit the scaler on the training set only, then apply it to the test set. A Pipeline does this automatically."
**Explain simply:**
- **Scaling** (standardising) rewrites each value as how many standard deviations it sits from the mean, so columns with big numbers (salary) do not drown out small ones.
- The mean and standard deviation are learned from data. If they come from all rows, the test set has quietly shaped the training process.
- Fix: split, then `fit_transform` on training and plain `transform` on test.
- Also missing: `random_state`, so the split cannot be repeated.
**Sample data:** 200 simulated employees with salary and tenure columns (seed 42).
**Code (what you write in the interview):**
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
# learn the mean and spread from training rows only
X_train_scaled = scaler.fit_transform(X_train)
# reuse the same numbers on the test rows
X_test_scaled = scaler.transform(X_test)
print(scaler.mean_.round(0))
print(X.mean().round(0).values)
```
**Output:**
```
[50809.    43.]
[50952.    45.]
```
**What it means:** The training-only means differ from the all-rows means; the buggy code would have used the second set. The gap is small here but the habit matters.
**Alternative / pitfalls:** `make_pipeline(StandardScaler(), model)` with cross-validation refits the scaler inside each fold. Tree models do not need scaling, but the fix is a good habit.
**Likely follow-ups:** 1) *Does the same apply to filling missing values?* Yes (Q13). 2) *Does it matter for trees?* Scaling is not needed for them.
**Common mistakes:** Calling `fit_transform` on the test set; fitting any preprocessing before the split.

### Q12 ⭐⭐⭐ 🟡 How do you handle a categorical column such as department or city before fitting a model? Compare one-hot encoding with label encoding.
**Asked at:** commonly asked (no company-specific report found); one-hot versus label encoding is in TechInterview, TechPrep and Board Infinity style lists (snippets only, unverified).
**What the interviewer is checking:** That you know models need numbers and that numeric codes can invent a false order.
**Say this in the interview:** "Models need numbers, so I convert categories. One-hot encoding makes a 0/1 column per category and implies no order, which suits department or city. Label encoding gives each category a number, which suits tree models or a true order like Junior, Mid, Senior, but misleads linear models."
**Explain simply:**
- A **categorical column** holds labels (Sales, HR, IT), not quantities.
- **One-hot**: one new 0/1 column per category. Safe, but many categories mean many columns.
- **Label encoding**: HR=0, IT=1, Sales=2. Compact, but a linear model would think Sales is "bigger" than HR and twice IT.
- For hundreds of values (such as city), group rare ones into "Other" first.
**Sample data:** Five employees with a `department` column.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"department": ["Sales", "HR", "IT", "Sales", "HR"]})

# one-hot: one 0/1 column per department
print(pd.get_dummies(employees, columns=["department"], dtype=int))

# label encoding: one number per department (alphabetical order)
employees["department_code"] = employees["department"].astype("category").cat.codes
print(employees)
```
**Output:**
```
   department_HR  department_IT  department_Sales
0              0              0                 1
1              1              0                 0
2              0              1                 0
3              0              0                 1
4              1              0                 0
  department  department_code
0      Sales                2
1         HR                0
2         IT                1
3      Sales                2
4         HR                0
```
**What it means:** One-hot treats departments as equal groups; the codes (0, 1, 2) look like a ranking that does not exist.
**Alternative / pitfalls:** Fit the encoder on training data and reuse it on test (new categories in test need handling, for example `OneHotEncoder(handle_unknown="ignore")`, from memory, unverified on this install).
**Likely follow-ups:** 1) *Many categories?* Group rare ones, or use target encoding with care (leakage risk). 2) *Ordered categories?* Use an ordered code.
**Common mistakes:** Label-encoding department for logistic regression; one-hot encoding an ID column; encoding before the split.

### Q13 ⭐⭐⭐ 🟡 How would you handle missing values in a feature before modelling, and why should the fill values be calculated from the training data only?
**Asked at:** commonly asked (no company-specific report found); missing-value handling and training-only imputation appear in preprocessing and leakage guides (snippets only, unverified).
**What the interviewer is checking:** That you first understand why the value is missing, and that you avoid leakage when filling it.
**Say this in the interview:** "First I ask why it is missing and how much is missing. Then I fill numbers with the median, categories with the most common value or an 'Unknown' label, sometimes with a flag column saying it was missing. I calculate the fill value from the training set only, otherwise test data leaks into training."
**Explain simply:**
- Options: drop rows (only if few and random), fill with median/mean/mode, fill with "Unknown", or add a "was missing" flag.
- The **median** is the middle value; it resists outliers (a few very high salaries).
- The fill value is learned from data, just like a scaler. Learning it from all rows lets test rows shape training. Learn from training, then apply the same value to test.
- Missingness itself can carry meaning (a blank last-promotion date may mean "never promoted").
**Sample data:** Ten ages with two blanks, split 70/30 (seed 42).
**Code (what you write in the interview):**
```python
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy="median")
# learn the median from training rows only
imputer.fit(X_train)
X_train_filled = imputer.transform(X_train)
X_test_filled = imputer.transform(X_test)
print(imputer.statistics_)
```
**Output:**
```
[33.]
```
**What it means:** Training ages (excluding blanks) are 25, 52, 33, 29, 45, so the median is 33, and 33 fills blanks in both parts. The all-rows median would have been 35.5, which uses test information.
**Alternative / pitfalls:** Put the imputer in a Pipeline so each cross-validation fold learns its own value. Heavy missingness (say over half) may mean dropping the column.
**Likely follow-ups:** 1) *Mean or median?* Median if skewed. 2) *Can missing be a signal?* Yes; add a flag column.
**Common mistakes:** Filling with the mean computed on all data; dropping rows without checking how many; ignoring why data is missing.

### Q14 ⭐⭐⭐ 🟡 What practical steps can you take to reduce overfitting in a model you built as an analyst?
**Asked at:** commonly asked (no company-specific report found); remedies for overfitting are standard in PracHub, FACE Prep and VitalFlux style lists (snippets only, unverified).
**What the interviewer is checking:** Whether you have practical, analyst-level steps rather than deep-learning jargon.
**Say this in the interview:** "I would simplify the model, for example limit tree depth, remove noisy or redundant features, get more data if possible, use cross-validation to measure honestly, and check for leakage. I always judge on the test set."
**Explain simply:**
- **Simplify**: smaller or more restricted model (shallower tree, larger minimum group size).
- **Fewer, better features**: drop columns that are noise or near-duplicates.
- **More data**: harder for a model to memorise a bigger sample.
- **Cross-validation**: average over several splits so one lucky split does not fool you (Q19).
- **Regularisation** (a penalty for complexity; for example in logistic regression) and **early stopping** exist, but mention them only briefly at analyst level.
**Worked example (concept questions):** On the simulated attrition data (Q1): unlimited tree, train 1.000, test 0.648; `min_samples_leaf=30`, train 0.784, test 0.692; `max_depth=3`, train 0.777, test 0.724. Restricting the tree narrowed the gap from 35.2 to 5.3 points and raised the test score by 7.6 points.
**Alternative / pitfalls:** Over-restricting leads to underfitting (Q2). Tune using validation data or cross-validation, not the test set.
**Likely follow-ups:** 1) *Does more data always help?* It helps overfitting but not bad features. 2) *Which first?* Check for leakage and simplify.
**Common mistakes:** Adding features hoping to improve; tuning on the test set; stopping at "use regularisation" with no example.

### Q15 ⭐⭐⭐ 🟡 Explain the bias-variance trade-off in plain words. Where do an overfit model and an underfit model sit on it?
**Asked at:** commonly asked (no company-specific report found); a Glassdoor Bengaluru report for Tiger Analytics mentioned the bias-variance trade-off (a search snippet of an anonymous report, unverified).
**What the interviewer is checking:** Whether you can explain the idea intuitively and map it to under- and overfitting.
**Say this in the interview:** "Bias is error from a model being too simple and missing the pattern. Variance is error from a model being too sensitive, so it changes a lot with different training data. Simple models have high bias and low variance (underfit); very flexible models have low bias and high variance (overfit). We look for the balance."
**Explain simply:**
- **Bias**: consistently wrong in the same direction, like a scale that always reads 2 kg light.
- **Variance**: answers jump around if the training sample changes, like a scale that reads differently each time.
- Underfit model: high bias, low variance. Overfit model: low bias, high variance.
- Making the model more flexible lowers bias but raises variance; the best test score sits between.
**Worked example (concept questions):** Tree depth on the simulated attrition data (Q1; 750 train / 250 test):

| Depth | Train | Test |
|---|---|---|
| 1 | 0.717 | 0.692 |
| 3 | 0.777 | 0.724 |
| 6 | 0.867 | 0.668 |
| no limit | 1.000 | 0.648 |

Training score always rises with depth; the test score peaks near depth 3 and then falls. Depth 1 leans towards high bias; no limit towards high variance.
**Alternative / pitfalls:** The numbers are one random split; the exact peak moves with the seed, so cross-validation is safer.
**Likely follow-ups:** 1) *Can you reduce both?* More good data and better features can. 2) *Where is the best model?* At the lowest test error.
**Common mistakes:** Mixing up which one is "simple"; thinking you can eliminate both; no concrete example.

### Q16 ⭐⭐ 🟢 What does random_state do in train_test_split, and why does it matter when you share your results with a colleague?
**Asked at:** commonly asked (no company-specific report found); reproducibility of splits is a common follow-up in split guides (snippets only, unverified).
**What the interviewer is checking:** That you understand random seeds and reproducibility.
**Say this in the interview:** "`random_state` fixes the random shuffle used to split the rows. With the same number, I and my colleague get exactly the same training and test rows, so we get the same scores. Without it, the split and the scores change every run."
**Explain simply:**
- The split shuffles rows randomly; a **seed** is a starting number that makes the shuffle repeatable.
- Same data plus same `random_state` equals same split. Different number, different split.
- The value itself (42, 0, 7) has no special meaning.
- Different splits give slightly different scores; that variation is a reminder that one split is a noisy estimate.
**Sample data:** 100 rows, test size 20%.
**Code (what you write in the interview):**
```python
for seed in [42, 42, 7]:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)
    print(seed, sorted(X_test["a"])[:5])
```
**Output:**
```
42 [0, 4, 10, 12, 18]
42 [0, 4, 10, 12, 18]
7 [11, 12, 13, 15, 18]
```
**What it means:** Seed 42 twice gives identical test rows; seed 7 gives different ones.
**Alternative / pitfalls:** Models with randomness (random forest) need their own `random_state`. A model that only works with one lucky seed is fragile; check with cross-validation.
**Likely follow-ups:** 1) *Which number do I pick?* Any; fix it and do not shop for a good one. 2) *Does it affect results?* The split, yes, a little.
**Common mistakes:** Trying seeds until the score looks best; forgetting it on the model as well; not noting the seed in the report.

### Q17 ⭐⭐ 🟢 What is the difference between a feature and a target (label)? Identify both in a model that predicts whether an employee will resign within 6 months.
**Asked at:** commonly asked (no company-specific report found); basic terminology, usually asked as a warm-up (no specific source).
**What the interviewer is checking:** Whether you know the basic vocabulary and can apply it to an HR problem.
**Say this in the interview:** "Features are the input columns the model uses to make a prediction; the target, or label, is the outcome I want to predict. Here the target is 'resigned within 6 months' (yes or no), and the features include tenure, salary, engagement score and overtime hours."
**Explain simply:**
- **Feature** (also input, predictor, X): a column known when you make the prediction.
- **Target** (also label, outcome, y): the answer the model learns to predict, known for past rows only.
- Choose the target carefully: "resigned within 6 months" needs a defined time window.
- Features must be available before the outcome; "exit interview done" is not a feature (Q6).
**Sample data:**

| tenure_months | salary_k | engagement | resigned_in_6m |
|---|---|---|---|
| 8 | 38 | 4 | Yes |
| 54 | 62 | 8 | No |
| 21 | 45 | 5 | No |

The first three columns are features; `resigned_in_6m` is the target.
**What it means:** The model sees the first three columns, learns how they relate to the last, then predicts the last for new employees.
**Alternative / pitfalls:** If the target is a number (salary) the task is regression; a category (resign yes/no) is classification.
**Likely follow-ups:** 1) *Is employee ID a feature?* No, it is an identifier with no real meaning. 2) *Can the target be a feature elsewhere?* Not in the same model.
**Common mistakes:** Including the target (or a copy) among the features; unclear target window; using IDs as features.

### Q18 ⭐⭐ 🟢 Does adding more features always make a model better? Explain with an example.
**Asked at:** commonly asked (no company-specific report found); a gap-fill question about a common misconception, not a sourced report.
**What the interviewer is checking:** That you know irrelevant features add noise and invite overfitting.
**Say this in the interview:** "No. Extra features that carry no real signal give the model more chances to find accidental patterns, so it can overfit and perform worse on new data. Each feature should have a reason to be there."
**Explain simply:**
- Useful features add information; useless ones add noise.
- With limited rows, the more columns, the easier it is to memorise coincidences.
- More columns also cost time, are harder to explain to a manager, and raise the chance of including a leaking or sensitive column.
- Judge by test or cross-validation score, not by how many columns you have.
**Worked example (concept questions):** On the simulated attrition data (1,000 rows, 4 real features), a 4-level tree scored 0.808 train and 0.652 test. After adding 40 columns of pure random numbers, train went up slightly to 0.817 while test fell to 0.616. The model was "learning" from noise. (One seed; the direction is the lesson, the exact size would vary.)
**Alternative / pitfalls:** Remove features with no relationship to the target, near-duplicates (salary in two currencies), and anything unavailable at prediction time.
**Likely follow-ups:** 1) *How do you choose features?* Business logic, correlation checks, test-score comparison. 2) *Is a larger dataset an answer?* More rows help; more columns do not.
**Common mistakes:** Throwing in every column; judging by training score, which always rises with more features.

### Q19 ⭐⭐ 🟡 What is k-fold cross-validation, and why is it preferred over a single train-test split on small datasets? For 5-fold on 500 rows, how many rows are in each training and validation part?
**Asked at:** commonly asked (no company-specific report found); cross-validation is listed in evaluation guides on PracHub and Dataford style pages (snippets only, unverified).
**What the interviewer is checking:** That you understand repeated splitting to get a steadier estimate, and can do the arithmetic.
**Say this in the interview:** "K-fold cross-validation splits the data into k equal parts. Each part takes a turn as the validation set while the model trains on the other k-1 parts, then I average the k scores. It uses every row for testing once, so it is steadier than one split on small data. For 5-fold on 500 rows, each fold has 100 validation rows and 400 training rows."
**Explain simply:**
- One split can be lucky or unlucky; with 500 rows a different split may change the score noticeably.
- 5-fold: five rounds, each with 100 rows held out and 400 used to train. Every row is held out exactly once.
- Report the mean and the spread across folds (Q20).
- The cost is training the model k times, which is fine for small data.
**Sample data:** 500 rows.
**Code (what you write in the interview):**
```python
from sklearn.model_selection import KFold

kfold = KFold(n_splits=5, shuffle=True, random_state=42)
for fold, (train_rows, validation_rows) in enumerate(kfold.split(X), start=1):
    print(fold, len(train_rows), len(validation_rows))
```
**Output:**
```
1 400 100
2 400 100
3 400 100
4 400 100
5 400 100
```
**What it means:** Five rounds of 400 training rows and 100 validation rows.
**Alternative / pitfalls:** `cross_val_score(model, X, y, cv=5)` does it in one line. Use `StratifiedKFold` for imbalanced classes, and put preprocessing in a Pipeline so it is learned inside each fold. Do not shuffle time-ordered data.
**Likely follow-ups:** 1) *How to choose k?* 5 or 10 is common. 2) *Does it replace the test set?* Keep a final test set if you can.
**Common mistakes:** Scaling or filling on all data before the folds; reporting only the best fold; using it on time series without ordering.

### Q20 ⭐⭐ 🟡 Interpret these 5-fold cross-validation scores. What is the mean, and what does the spread tell you?
Fold accuracies: 0.78, 0.82, 0.80, 0.76, 0.84.
**Asked at:** commonly asked (no company-specific report found); a gap-fill question on reading CV scores (no specific source).
**What the interviewer is checking:** Whether you report both the average and its stability.
**Say this in the interview:** "The mean accuracy is 0.80 and the folds range from 0.76 to 0.84, with a standard deviation of about 0.03. So I would expect roughly 80%, give or take a few points, on new data. The spread is moderate, not alarming."
**Explain simply:**
- Mean = (0.78 + 0.82 + 0.80 + 0.76 + 0.84) / 5 = 0.80.
- **Standard deviation** (std) measures how far scores typically sit from the mean: about 0.032 here (sample std).
- A small spread means the model behaves consistently across different data slices. A large one (say 0.65 to 0.95) means results depend heavily on which rows are used.
- Compare 0.80 with a baseline (such as always predicting the majority).
**Sample data:** The five fold accuracies above.
**Code (what you write in the interview):**
```python
import numpy as np

scores = np.array([0.78, 0.82, 0.80, 0.76, 0.84])
print(scores.mean().round(3), scores.std(ddof=1).round(3), scores.min(), scores.max())
```
**Output:**
```
0.8 0.032 0.76 0.84
```
**What it means:** Report "about 80% accuracy, typically within 3 points either way". With only five folds the spread itself is a rough guide.
**Alternative / pitfalls:** `std()` in numpy defaults to the population version (0.028); `ddof=1` gives the sample version (0.032). State which you use. For imbalanced data, accuracy may hide weak recall.
**Likely follow-ups:** 1) *What if one fold is much lower?* Investigate that slice (a department, a time period). 2) *Is the mean the final test score?* No; it guides model choice, and a final test set still gives the last check.
**Common mistakes:** Quoting only the best fold; ignoring the spread; treating 0.80 as a guarantee.

### Q21 ⭐⭐ 🟡 A decision tree was trained at several depths. Which depth would you choose, and why?
| max_depth | Train accuracy | Test accuracy |
|---|---|---|
| 2 | 0.78 | 0.76 |
| 5 | 0.88 | 0.82 |
| 10 | 0.99 | 0.74 |
**Asked at:** commonly asked (no company-specific report found); reading a train vs test table is a standard item in overfitting question banks (prep sites, unverified).
**What the interviewer is checking:** That you pick by test (unseen-data) accuracy and the train-test gap, not by the highest train score.
**Say this in the interview:** "I would choose depth 5. It has the best test accuracy, 0.82, and a modest gap of 0.06. Depth 10 scores 0.99 on training but only 0.74 on test, so it has memorised the training rows."
**Explain simply:**
- **max_depth** is how many yes/no questions in a row the tree may ask. Deeper means more detail.
- **Overfitting** means the model learns the quirks of the training rows and fails on new rows. Signs: very high train score, much lower test score.
- Gap (train minus test): depth 2 is 0.02, depth 5 is 0.06, depth 10 is 0.25.
- Depth 2 is slightly **underfit** (too simple; both scores are lowish). Depth 5 is the sweet spot.
**What it means:** Report the test score (0.82) to a manager, never the train score.
**Alternative / pitfalls:** One test set is noisy; confirm the depth with cross-validation (Q19) and try depths 3, 4, 6, 7 too. Do not keep re-picking on the same test set (Q38).
**Likely follow-ups:** 1) *Other ways to stop overfitting a tree?* Set `min_samples_leaf`, prune, or use a random forest. 2) *Would you pick depth 2 for simplicity?* Only if the business values an easy-to-explain tree more than 6 points of accuracy.
**Common mistakes:** Choosing depth 10 because train accuracy is 0.99; ignoring the gap; tuning on the test set.

### Q22 ⭐⭐ 🟡 Why is scaling needed for some models and not others? Standardise a salary of 62,000 when the training mean is 50,000 and the standard deviation is 5,000.
**Asked at:** commonly asked (no company-specific report found); "which models need scaling" is a standard preprocessing item in prep-site lists (unverified).
**What the interviewer is checking:** That you know scaling matters for distance and gradient based models, and that you can compute a z-score.
**Say this in the interview:** "Models that measure distance or fit coefficients with penalties, like k-NN, k-means, logistic regression and SVM, are thrown off when one column is in lakhs and another is in years. Tree models only compare values within one column, so they do not need scaling. The z-score is (62,000 minus 50,000) divided by 5,000, which is 2.4."
**Explain simply:**
- **Standardising** turns a value into "how many standard deviations above or below the average": z = (value - mean) / standard deviation. The **standard deviation** is the typical spread around the mean.
- Needed: k-NN, k-means, SVM, regularised regression, neural networks, PCA.
- Not needed: decision trees, random forests, gradient boosting.
- The mean and standard deviation come from the **training** data only, and the same numbers are reused on test and new data.
**Code (what you write in the interview):**
```python
salary = 62000
train_mean = 50000
train_std = 5000

z_score = (salary - train_mean) / train_std
print(z_score)
```
**Output:**
```
2.4
```
**What it means:** This salary is 2.4 standard deviations above the training average, high but not extreme.
**Worked example (concept questions):** Employee A (salary 50,000, age 25), B (52,000, age 55), C (60,000, age 26). Unscaled distances: A to B is about 2,000.2 and A to C is 10,000.0, so salary alone decides and B looks "closest" despite a 30-year age gap. After standardising (salary mean 50,000 and sd 5,000; age mean 40 and sd 10; illustrative numbers) the distances are A to B 3.03 and A to C 2.00, so C is now closer, which respects age too.
**Alternative / pitfalls:** Fit the scaler on training rows only (see Q31). Min-max scaling (squeeze to 0-1) is the other option but is sensitive to outliers.
**Likely follow-ups:** 1) *Do we scale the target?* Usually not. 2) *Does scaling change a tree?* No.
**Common mistakes:** Scaling before the split; scaling one-hot columns without reason; saying all models need scaling.

### Q23 ⭐⭐ 🟡 Write pandas code to create a `tenure_months` feature from a `hire_date` column, and explain why this is usually more useful to a model than the raw date.
`df['hire_date']` holds dates as strings such as '2021-04-15'; use 2025-04-30 as the reference date.
**Asked at:** commonly asked (no company-specific report found); date-to-age features appear in feature-engineering lists (prep sites, unverified).
**What the interviewer is checking:** That you convert strings to real dates first and measure from a fixed reference date.
**Say this in the interview:** "I convert the text to datetime, subtract it from a fixed reference date, and divide days by about 30.44 to get months. Tenure is a number that means the same thing for every employee; a raw date is just a label."
**Explain simply:**
- A **feature** is a column the model uses to predict. A raw date like 2021-04-15 has no useful order for most models and cannot be compared to future employees.
- Tenure ("how long they have been here") links directly to behaviour such as attrition risk.
- Use a **fixed reference date** (here 2025-04-30), not "today", so results do not change every day and can be reproduced.
**Sample data:** four hire dates: 2021-04-15, 2023-11-01, 2025-01-20, 2019-07-31.
**Code (what you write in the interview):**
```python
import pandas as pd

df = pd.DataFrame({'hire_date': ['2021-04-15', '2023-11-01', '2025-01-20', '2019-07-31']})

reference_date = pd.Timestamp('2025-04-30')
df['hire_date'] = pd.to_datetime(df['hire_date'])

# approximate months: days divided by 30.44 (average month length)
df['tenure_months'] = ((reference_date - df['hire_date']).dt.days / 30.44).round(1)
print(df)
```
**Output:**
```
   hire_date  tenure_months
0 2021-04-15           48.5
1 2023-11-01           17.9
2 2025-01-20            3.3
3 2019-07-31           69.0
```
**What it means:** Employee 3 has been here almost six years; employee 2 is a recent joiner.
**Alternative / pitfalls:** For whole calendar months use `(ref.year - d.dt.year) * 12 + (ref.month - d.dt.month)`. Never use `datetime.now()` inside a model feature, and for leavers measure tenure up to the exit date, not today.
**Likely follow-ups:** 1) *Other date features?* Hire month, day of week, quarter. 2) *What if hire_date is missing?* Investigate; do not fill with a made-up date.
**Common mistakes:** Subtracting strings without `to_datetime`; using today's date; counting leavers' tenure to today, which leaks their outcome.

### Q24 ⭐⭐ 🟡 After one-hot encoding with drop_first=True, how many columns does this dataset have, and why do we drop one dummy column?
Columns: `department` (5 distinct values), `age`, `salary`. Target column excluded.
**Asked at:** commonly asked (no company-specific report found); the dummy variable trap is a standard encoding question in prep lists (unverified).
**What the interviewer is checking:** That you can count columns and explain the redundancy (dummy variable trap).
**Say this in the interview:** "Five departments become four dummy columns, plus age and salary, so six columns. The fifth is redundant: if a person is in none of the four, they must be in the fifth, and keeping it makes the columns perfectly dependent, which confuses linear models."
**Explain simply:**
- **One-hot encoding** turns a category into 0/1 columns, one per value (IT = 1 or 0).
- With all 5 columns, the five always add up to 1, so any one is predictable from the others. This is **perfect multicollinearity** (columns that carry the same information), and it makes linear and logistic regression coefficients unstable or undefined.
- Dropping one makes that value the **baseline**; each coefficient is then "compared with the baseline".
- Count: 5 - 1 = 4 dummies, plus age and salary = 6.
**Sample data:** six invented employees; departments HR, Sales, IT, Finance, Ops, IT (five distinct values).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    'department': ['HR', 'Sales', 'IT', 'Finance', 'Ops', 'IT'],
    'age': [29, 41, 35, 50, 27, 33],
    'salary': [45000, 60000, 70000, 80000, 38000, 66000],
})

encoded = pd.get_dummies(employees, columns=['department'], drop_first=True)
print(encoded.shape)
print(list(encoded.columns))
```
**Output:**
```
(6, 6)
['age', 'salary', 'department_HR', 'department_IT', 'department_Ops', 'department_Sales']
```
**What it means:** Six columns; `Finance` was dropped (first alphabetically) and is the baseline.
**Alternative / pitfalls:** Tree models do not need `drop_first`. In a pipeline use `OneHotEncoder(handle_unknown='ignore')` so a new department in new data does not crash it.
**Likely follow-ups:** 1) *Label encoding instead?* Wrongly implies order (HR < IT) for nominal categories. 2) *Many categories?* Group rare ones or use target encoding (Q39).
**Common mistakes:** Forgetting that age and salary stay; counting 5 dummies; encoding the target by accident.

### Q25 ⭐⭐ 🟡 How do you spot and treat outliers in a feature before modelling? Using the IQR rule, what is the upper fence below, and would a salary of 95 be flagged?
Salary in thousands: Q1 = 30, Q3 = 50.
**Asked at:** commonly asked (no company-specific report found); outlier rules (IQR, 3 standard deviations) feature in prep-site lists (unverified).
**What the interviewer is checking:** That you can apply the 1.5 x IQR rule and that you investigate before deleting.
**Say this in the interview:** "IQR is 50 minus 30, which is 20. The upper fence is 50 plus 1.5 times 20, so 80. A salary of 95 is above 80, so it is flagged. Flagged does not mean wrong: I would check whether it is a typo or a genuine senior salary before deciding."
**Explain simply:**
- **Q1 and Q3** are the 25th and 75th percentiles; **IQR** is Q3 minus Q1, the spread of the middle half of the data.
- Fences: lower = Q1 - 1.5 x IQR, upper = Q3 + 1.5 x IQR.
- Spot: box plot, histogram, IQR rule, z-score above 3.
- Treat: fix data errors; **cap** (winsorise) at the fences; log-transform (Q33); or keep them and use a robust model such as a tree. Delete only if proven wrong.
**Code (what you write in the interview):**
```python
q1, q3 = 30, 50
iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr
print(iqr, lower_fence, upper_fence, 95 > upper_fence)
```
**Output:**
```
20 0.0 80.0 True
```
**What it means:** Fences are 0 and 80 (thousand); 95 is flagged. A lower fence of 0 means no low salary can be flagged.
**Alternative / pitfalls:** The IQR rule is a screening tool, not proof. Real pay data is right-skewed, so many genuine high salaries get flagged.
**Likely follow-ups:** 1) *Why 1.5?* A convention (Tukey's rule). 2) *Outlier in the target?* Think carefully; it changes what the model learns.
**Common mistakes:** Deleting every flagged row; computing the fence after the train-test split on all data; forgetting the lower fence.

### Q26 ⭐⭐ 🟡 Only 5% of customers in your churn data actually churn, so a model that predicts 'no churn' for everyone is 95% accurate. What can you do at the data and model level to handle this imbalance?
**Asked at:** commonly asked (no company-specific report found); imbalance handling (class weights, resampling) is a standard item in prep banks (unverified).
**What the interviewer is checking:** That you know accuracy misleads here and can name practical fixes plus the right metrics.
**Say this in the interview:** "First I stop using accuracy and look at recall and precision for the churn class. Then I stratify the split, use class weights or resample the training data only, and choose the decision threshold using the business cost of missing a churner versus contacting a loyal customer."
**Explain simply:**
- **Recall** = of the real churners, how many we caught. **Precision** = of those we flagged, how many really churned.
- Data level: **stratified split** (keeps 5% in train and test), oversample churners or undersample non-churners (training data only), collect more churn examples.
- Model level: `class_weight='balanced'` (errors on churners count more), a lower probability threshold, models that suit imbalance.
- Metrics: recall, precision, F1, PR-AUC; confusion matrix.
**Sample data:** synthetic data, 4,000 customers, about 5.7% churners (seed 42), so this is an illustration only.
**Code (what you write in the interview):**
```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, precision_score, accuracy_score

X, y = make_classification(n_samples=4000, n_features=8, n_informative=4,
                           weights=[0.95], random_state=42)
# stratify keeps the 5% churn share in both parts
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42)

for weight in [None, 'balanced']:
    model = LogisticRegression(class_weight=weight, max_iter=1000)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print(weight, 'accuracy', round(accuracy_score(y_test, pred), 3),
          'recall', round(recall_score(y_test, pred), 3),
          'precision', round(precision_score(y_test, pred), 3))
print('share of churners in y:', y.mean().round(3))
```
**Output:**
```
None accuracy 0.949 recall 0.14 precision 0.8
balanced accuracy 0.709 recall 0.596 precision 0.113
share of churners in y: 0.057
```
**What it means:** The plain model has 94.9% accuracy but catches only 14% of churners. Balanced weights catch 60% at the cost of many false alarms (precision 11%) and lower accuracy. Which is better depends on the cost of a retention call versus a lost customer.
**Alternative / pitfalls:** Resample only the training data, never the test set; otherwise scores are fake. Output depends on the data seed (42).
**Likely follow-ups:** 1) *What is SMOTE?* Creating synthetic minority rows (from memory, library `imbalanced-learn`, not tested here). 2) *Which metric to report?* Recall and precision for the churn class.
**Common mistakes:** Quoting accuracy; oversampling before splitting, which copies rows into the test set.

### Q27 ⭐⭐ 🟡 Why is a random train-test split a problem for data that depends on time, such as monthly sales or monthly attrition snapshots? How would you split instead?
**Asked at:** commonly asked (no company-specific report found); time-ordered splits appear as a follow-up in overfitting and leakage prep pages (unverified).
**What the interviewer is checking:** That you see "training on the future to predict the past" as leakage and know the fix.
**Say this in the interview:** "A random split mixes future months into training, so the model has already seen the trend it is later tested on, and scores look better than real life. In practice we only ever predict forward, so I train on the older months and test on the latest ones, and use time-ordered cross-validation for tuning."
**Explain simply:**
- Neighbouring months are similar (trend, seasonality). A random test month sits between training months, so it is almost "interpolation", not forecasting.
- **Time-based split**: pick a cut-off date; everything before is training, everything after is test.
- **TimeSeriesSplit** gives several such folds, each training on the past and validating on the next block.
- Also build features (rolling averages) from past data only.
**Sample data:** 24 months of invented attrition rate (2023-01 to 2024-12), rising from 2.1 to 4.5.
**Code (what you write in the interview):**
```python
import pandas as pd

monthly = pd.DataFrame({
    'month': pd.period_range('2023-01', periods=24, freq='M'),
    'attrition_rate': [2.1, 2.3, 2.0, 2.4, 2.6, 2.5, 2.8, 2.7, 3.0, 3.1, 2.9, 3.3,
                       3.2, 3.5, 3.4, 3.6, 3.8, 3.7, 4.0, 3.9, 4.1, 4.3, 4.2, 4.5],
})

# oldest 18 months to train, latest 6 months to test
train = monthly.iloc[:18]
test = monthly.iloc[18:]
print('train:', train['month'].min(), 'to', train['month'].max())
print('test: ', test['month'].min(), 'to', test['month'].max())
```
**Output:**
```
train: 2023-01 to 2024-06
test:  2024-07 to 2024-12
```
**What it means:** The test months are strictly after the training months, which mimics real use. Note the test rates are higher than anything in training: that drift is exactly what a random split would hide.
**Alternative / pitfalls:** `TimeSeriesSplit(3)` on 12 rows gives train/test index blocks [0-2]/[3-5], [0-5]/[6-8], [0-8]/[9-11]: the training window grows and always precedes validation.
**Likely follow-ups:** 1) *Can you shuffle within the training set?* Yes, for models that ignore order. 2) *How long a test window?* Long enough to cover a business cycle you care about.
**Common mistakes:** Using `train_test_split` with shuffle on time data; computing rolling features over the whole timeline.

### Q28 ⭐⭐ 🟡 Why use an sklearn Pipeline with a scaler and a model instead of transforming the data manually?
**Asked at:** commonly asked (no company-specific report found); fit-after-split and Pipeline usage appear in leakage prep pages (unverified).
**What the interviewer is checking:** That you understand a Pipeline prevents leakage and keeps training and prediction steps identical.
**Say this in the interview:** "A Pipeline chains the scaler and the model into one object. When I fit it, the scaler learns its mean and spread from training rows only; when I predict, the same steps run automatically. That avoids leakage, avoids forgetting a step, and works safely inside cross-validation."
**Explain simply:**
- **Fit** means learn numbers from data (the scaler learns mean and spread, the model learns coefficients). **Transform** applies those learned numbers.
- Manual way: fit scaler, transform train, transform test, fit model, easy to slip and fit on everything.
- Pipeline: one `fit`, one `predict`, one object to save and ship.
- It also lets cross-validation refit the scaler inside each fold (Q31).
**Code (what you write in the interview):**
```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

X, y = make_classification(n_samples=500, n_features=6, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

pipe = make_pipeline(StandardScaler(), LogisticRegression())
pipe.fit(X_train, y_train)            # scaler learns mean/sd from training rows only
print('test accuracy:', round(pipe.score(X_test, y_test), 3))   # same scaling applied to test rows
print('cv accuracy:', cross_val_score(pipe, X_train, y_train, cv=5).round(3))
```
**Output:**
```
test accuracy: 0.84
cv accuracy: [0.88  0.893 0.88  0.92  0.947]
```
(Synthetic data, seed 42.)
**What it means:** Test accuracy is 0.84; the fold scores are in a similar range, so the process is stable.
**Alternative / pitfalls:** Use `ColumnTransformer` inside the pipeline when columns need different treatment (scale numbers, one-hot categories).
**Likely follow-ups:** 1) *Can I tune the scaler too?* Yes, via `GridSearchCV` on the pipeline. 2) *Does a pipeline help trees?* Still helps with imputing and encoding.
**Common mistakes:** Calling `fit_transform` on the test set; scaling the whole dataset before splitting.

### Q29 ⭐⭐ 🟡 A model looked good in your notebook but performs poorly after being used on new employee data. List the likely causes.
**Asked at:** commonly asked (no company-specific report found); "why does a model fail in production" is a common scenario prompt (prep sites, unverified).
**What the interviewer is checking:** A structured checklist, with leakage and shift near the top.
**Say this in the interview:** "I would check for data leakage first, then overfitting, then whether the new data differs from the training data, then data quality and definition changes. I would compare the new data's columns and ranges with the training data before blaming the algorithm."
**Explain simply:**
- **Data leakage:** the model saw information in training that is not available at prediction time (for example an exit-interview flag when predicting who will leave).
- **Overfitting:** it memorised the training data; the test set was reused or too small (Q36, Q38).
- **Distribution shift:** new employees differ (new location, new roles, post-policy change, a different year).
- **Data pipeline issues:** different column definitions, missing values, new categories, units, preprocessing not repeated identically.
- **Unrepresentative sample or label difference:** training only on people who stayed 2+ years; "attrition" defined differently now.
- **Wrong metric or threshold:** accuracy looked fine on imbalanced data.
- **Time:** random split used on time-ordered data (Q27).
**Worked example (concept questions):** An attrition model trained on 2021-22 data (mostly office staff) is used in 2025 after a large factory hiring drive. The new people have different ages, tenures and exit patterns, so the model is working outside what it learned.
**Alternative / pitfalls:** Monitor live performance and input ranges; retrain on recent data on a schedule.
**Likely follow-ups:** 1) *First thing you check?* Compare new feature distributions with training. 2) *How to prevent it?* Time-based test, pipelines, monitoring.
**Common mistakes:** Blaming "bad model" only; not checking whether labels and column definitions changed.

### Q30 ⭐⭐ 🟡 Two features, `years_at_company` and `age`, have a correlation of 0.95. How would you decide which to keep, and does it matter for prediction versus explanation?
**Asked at:** commonly asked (no company-specific report found); multicollinearity is a standard feature-selection prompt (unverified).
**What the interviewer is checking:** That you separate prediction (barely hurt) from explanation (coefficients become unreliable).
**Say this in the interview:** "They carry almost the same information. For pure prediction I could keep both with little harm, or keep the one with the stronger link to the target and simpler meaning. For explanation I would keep just one, because with both in a linear model the coefficients become unstable and I cannot say which one matters."
**Explain simply:**
- **Correlation** (-1 to 1) measures how closely two columns move together. 0.95 is very high.
- This overlap is **multicollinearity**. Predictions stay fine, but individual coefficients swing wildly with small data changes.
- How to choose: which one is more meaningful and available at prediction time; which has the higher correlation with the target; check **VIF** (variance inflation factor, high values such as above 5 or 10 signal overlap; a common rule of thumb); or let regularisation or a tree handle it.
- Trees and prediction-only models are relatively unaffected.
**Sample data:** synthetic: 200 employees where age is about 22 + years at company, salary driven by years (seed 42; correlation came out 0.97).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
years = rng.uniform(1, 20, 200)
age = 22 + years + rng.normal(0, 1.5, 200)          # age moves almost with years
salary = 20000 + 2500 * years + rng.normal(0, 4000, 200)
data = pd.DataFrame({'years_at_company': years, 'age': age, 'salary': salary})
print(data[['years_at_company', 'age']].corr().round(2).iloc[0, 1])

for seed in [1, 2, 3]:
    sample = data.sample(60, random_state=seed)
    model = LinearRegression().fit(sample[['years_at_company', 'age']], sample['salary'])
    print(seed, model.coef_.round(0), 'R2', round(model.score(sample[['years_at_company','age']], sample['salary']), 3))
```
**Output:**
```
0.97
1 [2972. -329.] R2 0.905
2 [2681. -254.] R2 0.921
3 [1999.  348.] R2 0.911
```
**What it means:** Fit quality (R2, how much of the variation is explained) stays near 0.91, but the age coefficient flips between -329 and +348 depending on the sample. Predict: fine. Explain: unreliable.
**Alternative / pitfalls:** Dropping one loses a little information; combining them (for example age at joining = age - years) can be more meaningful.
**Likely follow-ups:** 1) *What threshold is "too correlated"?* No fixed rule; 0.8-0.9 is a common warning level (rule of thumb). 2) *Does it hurt random forests?* Little for accuracy; it splits importance between the two.
**Common mistakes:** Saying you must always drop one; reading coefficients of correlated features as separate effects.

### Q31 ⭐⭐ 🔴 Why can fitting an imputer or scaler on the whole dataset before cross-validation inflate the scores, and how does a Pipeline inside cross_val_score fix it?
**Asked at:** commonly asked (no company-specific report found); the "preprocessing before the split" trap is a standard leakage prompt on prep sites (unverified).
**What the interviewer is checking:** That you understand validation rows must stay unseen, even for simple steps like means.
**Say this in the interview:** "If the imputer or scaler learns its averages from all rows, each validation fold has already influenced the numbers used to prepare the training folds, so the validation is not fully unseen. Putting them in a Pipeline passed to cross_val_score refits them on only the training part of every fold."
**Explain simply:**
- In cross-validation, each fold takes turns as the unseen validation set. Anything *learned from data* (a mean to fill blanks, a scale factor) must be learned without that fold.
- Fitting on everything first leaks a little information from validation into training: this is **data leakage**.
- The Pipeline handles the sequence: for each fold, fit imputer and scaler on the training part, transform both parts, fit the model, score the validation part.
- Honest size of the effect: for a simple imputer or scaler it is usually tiny. It is large for steps that use the target, such as feature selection or target encoding (Q39).
**Sample data:** synthetic 300 rows, 10 features, 10% of values blanked (seed 42).
**Code (what you write in the interview):**
```python
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
import numpy as np

X, y = make_classification(n_samples=300, n_features=10, random_state=42)
rng = np.random.default_rng(42)
X[rng.random(X.shape) < 0.1] = np.nan

# wrong: imputer and scaler learn from every row, including validation rows
X_prepared = StandardScaler().fit_transform(SimpleImputer().fit_transform(X))
wrong = cross_val_score(LogisticRegression(), X_prepared, y, cv=5)

# right: the Pipeline refits the imputer and scaler on the training part of each fold
pipe = make_pipeline(SimpleImputer(), StandardScaler(), LogisticRegression())
right = cross_val_score(pipe, X, y, cv=5)
print('manual prep:', wrong.mean().round(4))
print('pipeline:   ', right.mean().round(4))
```
**Output:**
```
manual prep: 0.9133
pipeline:    0.9133
```
**What it means:** Here both scores are identical to four decimals, so mean-and-scale leakage did not matter on this data. That is typical, but the habit matters: on pure noise (100 rows, 500 random columns, target random) I checked that selecting the 10 "best" columns before CV gives about 0.70 accuracy versus 0.50 inside a Pipeline. The first number is fake.
**Alternative / pitfalls:** Never claim "it always inflates a lot"; say it can, and the risk is highest with target-aware steps and small data.
**Likely follow-ups:** 1) *Does it matter for the final test set too?* Yes, fit on train, only transform test. 2) *Does Pipeline handle `GridSearchCV`?* Yes, pass the pipeline as the estimator.
**Common mistakes:** Calling `fit_transform` on the full X before `cross_val_score`; overstating the effect of scaler leakage.

### Q32 ⭐ 🟡 What does a learning curve show, and what does each pattern below suggest?
Case A: training score 0.95 and validation score 0.70, gap stays wide as rows increase. Case B: both scores plateau near 0.65.
**Asked at:** commonly asked (no company-specific report found); learning curves are a differentiator topic, not a standard opener (judgement).
**What the interviewer is checking:** That you can diagnose overfitting vs underfitting and say whether more data helps.
**Say this in the interview:** "A learning curve plots training and validation score as the training set grows. Case A, high train and low validation with a persistent gap, is overfitting (high variance): simplify the model, add regularisation, or get more data. Case B, both low and flat together, is underfitting (high bias): add better features or a more flexible model; more rows will not help."
**Explain simply:**
- **Validation score** is the score on rows held out from fitting.
- Case A: the model fits training well but does not generalise. If the validation line is still rising with more rows, more data can help; if the gap is stuck, simplify.
- Case B: the model is too simple or features are weak: it cannot even fit the training data well.
- Healthy: both lines converge at a high level.
**Sample data:** a decision tree on synthetic data (1,000 rows, seed 42), printed as training size, train score, validation score.
**Code (what you write in the interview):**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import learning_curve
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=1000, n_features=10, n_informative=4,
                           flip_y=0.1, random_state=42)
sizes, train_scores, val_scores = learning_curve(
    DecisionTreeClassifier(random_state=42), X, y,
    train_sizes=[0.2, 0.4, 0.6, 0.8, 1.0], cv=5)

for n, tr, va in zip(sizes, train_scores.mean(axis=1), val_scores.mean(axis=1)):
    print(n, round(tr, 2), round(va, 2))
```
**Output:**
```
160 1.0 0.77
320 1.0 0.77
480 1.0 0.75
640 1.0 0.77
800 1.0 0.77
```
**What it means:** An unrestricted tree scores 1.00 on training but about 0.77 on validation at every size: the Case A pattern (wide, stuck gap), so a shallower tree or regularisation is the next step, not more rows.
**Alternative / pitfalls:** Learning curves need cross-validation, so they cost time on big data. Noisy labels cap the validation score.
**Likely follow-ups:** 1) *How is it different from a validation curve?* The validation curve varies a model setting (like depth); the learning curve varies data size. 2) *Case A fixes?* Fewer features, pruning, regularisation, more data.
**Common mistakes:** Saying more data always fixes it; mixing up high bias and high variance.

### Q33 ⭐ 🟡 A salary column is heavily right-skewed. Would you transform it for a model, and how (for example log)? Which models care?
**Asked at:** commonly asked (no company-specific report found); skew and log transforms appear in preprocessing lists (prep sites, unverified).
**What the interviewer is checking:** That you know which models are sensitive to skew and can name a simple fix.
**Say this in the interview:** "It depends on the model. For linear regression, k-NN or anything distance based, a log transform often helps because a few huge salaries otherwise dominate. Tree models do not care because they only use the order of values. I would apply log1p to the feature (or the target if I am predicting salary) and remember to reverse it when reporting."
**Explain simply:**
- **Right-skewed** means most values are low with a long tail of very high ones (typical for salary).
- **Log transform** compresses the tail: 400,000 becomes a number only a little larger than 90,000's, so one huge value stops dominating.
- Care: linear and logistic regression (residual and linearity assumptions), distance models, neural nets. Do not care: decision trees, random forests, boosting.
- `log1p` is log(1 + x), safe for zeros. It does not fix negatives.
**Sample data:** ten salaries from 28,000 to 400,000.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd

salary = pd.Series([28000, 31000, 35000, 40000, 45000, 52000, 65000, 90000, 150000, 400000])
log_salary = np.log1p(salary)      # log(1 + x), safe if a value is 0

print('skew before:', round(salary.skew(), 2))
print('skew after: ', round(log_salary.skew(), 2))
```
**Output:**
```
skew before: 2.63
skew after:  1.41
```
**What it means:** Skew (0 = symmetric) fell from 2.63 to 1.41: better, though still right-leaning in this tiny sample.
**Alternative / pitfalls:** Square root, Box-Cox, or capping outliers. If you predict a log target, convert predictions back with `np.expm1`, and say that coefficients now describe percentage changes, not rupee changes.
**Likely follow-ups:** 1) *Do you transform the target too?* Sometimes, if errors grow with salary. 2) *Does scaling fix skew?* No; scaling changes units, not shape.
**Common mistakes:** Transforming for tree models "just in case"; forgetting to reverse the log; using plain `log` on zeros.

### Q34 ⭐ 🟡 What are interaction or ratio features? Create one from `salary` and `grade_midpoint`, and say why it might predict attrition better than salary alone.
**Asked at:** commonly asked (no company-specific report found); ratio features are a feature-engineering gap-fill, not tied to a company (judgement).
**What the interviewer is checking:** That you create features that capture meaning (relative pay), not just raw numbers.
**Say this in the interview:** "A ratio feature divides one column by another. Salary divided by the midpoint of the employee's pay grade, the compa-ratio, shows whether someone is paid above or below the going rate for their level. People paid at 0.8 of midpoint are more likely to feel underpaid and leave than someone at 1.1, even if the raw salary looks high."
**Explain simply:**
- **Interaction feature:** combines two columns (multiply or divide) so the model sees an effect neither shows alone.
- Raw salary 40,000 means little without grade: it is fine in one grade and low in another.
- Compa-ratio 1.0 means paid exactly at grade midpoint; below 1 is under, above 1 is over.
- It is an idea you test, not a guaranteed win: check with cross-validation (Q19).
**Sample data and code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    'salary': [40000, 52000, 75000, 60000],
    'grade_midpoint': [50000, 50000, 80000, 55000],
})

# compa-ratio: 1.0 means paid exactly at the middle of the grade
employees['compa_ratio'] = (employees['salary'] / employees['grade_midpoint']).round(2)
print(employees)
```
**Output:**
```
   salary  grade_midpoint  compa_ratio
0   40000           50000         0.80
1   52000           50000         1.04
2   75000           80000         0.94
3   60000           55000         1.09
```
**What it means:** Employee 0 earns less than employee 2 in rupees but is the more under-paid relative to grade (0.80 vs 0.94).
**Alternative / pitfalls:** Guard against zero or missing denominators. Keep raw salary and the ratio together only if you check for overlap (Q30).
**Likely follow-ups:** 1) *Other ratios in HR?* Absences per month, overtime hours / total hours, promotions per year of tenure. 2) *Do trees need this?* They can approximate it, but explicit ratios still help.
**Common mistakes:** Making many random ratios without a business reason; dividing by zero.

### Q35 ⭐ 🟡 You want to use gender, age and pincode as features in an attrition or hiring model. What risks would you raise about fairness, proxies and privacy before including them?
**Asked at:** commonly asked (no company-specific report found); a gap-fill topic for HR-analytics roles, not sourced to any company (judgement).
**What the interviewer is checking:** Judgement: that you think of people affected, law and trust, not just accuracy.
**Say this in the interview:** "Gender is a protected attribute and using it in a hiring decision is likely discriminatory. Age can also be protected and drives age bias. Pincode can act as a proxy for caste, religion, income or gender, so removing the sensitive column does not remove the bias. I would raise it with HR, legal and the data protection owner before including any of them, and test the model's results across groups."
**Explain simply:**
- **Protected attribute:** a personal trait (gender, age, religion, caste, disability) that must not drive decisions about people; the exact list depends on law and company policy.
- **Proxy:** an innocent-looking column that stands in for a protected one (pincode for community or income).
- **Historical bias:** past hiring or promotion data reflects past bias, and a model copies it.
- **Privacy:** these are personal data; collect and use only what is needed for a stated purpose, with consent or legal basis where required. Details (India's DPDP Act, GDPR) are from memory, unverified; confirm with legal or your data protection officer.
- What to do: drop unnecessary columns, test outcomes by group (selection rates, error rates), keep a human decision-maker, document the purpose, limit access.
**Worked example (concept questions):** An attrition model flags women in one pincode as "high risk" because few were promoted in the past. Managers then withhold training from them, and the prediction becomes self-fulfilling.
**Alternative / pitfalls:** Dropping gender while keeping proxies is "fairness through unawareness", which usually fails. Sometimes the sensitive column is kept only to audit fairness, not to predict.
**Likely follow-ups:** 1) *Is age OK for workforce planning?* Aggregated retirement planning is different from scoring individuals; confirm with legal. 2) *How do you test for bias?* Compare selection and error rates across groups.
**Common mistakes:** Saying "the model is objective"; ignoring proxies; using real employee data in public AI tools.

### Q36 ⭐ 🟡 What is the difference between overfitting, data leakage and train-test distribution shift? Give a one-line example of each.
**Asked at:** commonly asked (no company-specific report found); the leakage vs shift distinction is a common follow-up on prep sites (unverified).
**What the interviewer is checking:** That you keep three failure modes apart.
**Say this in the interview:** "Overfitting: the model memorises noise and shines only on training data. Leakage: the model gets information it would not have in real use, so even the test score is too good. Distribution shift: the model is fine, but new data no longer looks like the training data."
**Explain simply:**
- **Overfitting** (train high, test low): a deep tree scoring 0.99 on training and 0.74 on test.
- **Data leakage** (test also too high, then fails live): using `exit_interview_done` as a feature to predict attrition; or scaling before the split.
- **Distribution shift** (good test, poor live): a model trained on 2022 office hiring is used on 2025 factory hiring.
- Diagnosis: overfitting shows a train-test gap; leakage shows suspiciously great scores that collapse in production; shift shows a good test score and falling live accuracy while inputs have changed.
**Worked example (concept questions):** Predicting leavers: a deep tree has train 0.99 and test 0.74 (overfitting). Adding "days since last paycheck" gives test 0.97, because leavers stop receiving pay (leakage). After a merger the live accuracy drops to 0.65 as the new staff mix differs (shift). (Invented numbers for illustration.)
**Alternative / pitfalls:** They can occur together. Fixes differ: simplify the model, fix the pipeline and features, monitor and retrain.
**Likely follow-ups:** 1) *How to spot leakage?* A feature with unrealistically high importance. 2) *How to spot shift?* Compare feature distributions over time.
**Common mistakes:** Calling every poor live result "overfitting".

### Q37 ⭐ 🔴 Your attrition data has several monthly rows per employee. Why can a random row-level split leak information, and what would you use instead?
**Asked at:** commonly asked (no company-specific report found); group leakage is a differentiator topic (judgement).
**What the interviewer is checking:** That you know the unit of prediction (the employee) must not be split across train and test.
**Say this in the interview:** "Each employee's monthly rows look very alike, so with a random split the same person is in both train and test, and the model can score well just by recognising people. I would split by employee, using GroupShuffleSplit or GroupKFold with employee_id as the group, and for forecasting also keep time order."
**Explain simply:**
- Rows from one person share salary band, department, manager and the outcome.
- The model "recognises" that person in test and copies the answer, so the score is inflated: the model has not learned to generalise to new employees.
- **Group split:** all rows of an employee go either to train or to test.
- `GroupKFold` does this for cross-validation.
**Sample data:** 200 employees with 6 monthly rows each.
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GroupShuffleSplit

# 200 employees x 6 monthly rows each
rows = pd.DataFrame({'employee_id': np.repeat(np.arange(200), 6)})

train, test = train_test_split(rows, test_size=0.25, random_state=42)
shared = set(train['employee_id']) & set(test['employee_id'])
print('random split, employees in both parts:', len(shared))

splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
train_idx, test_idx = next(splitter.split(rows, groups=rows['employee_id']))
shared = set(rows.iloc[train_idx]['employee_id']) & set(rows.iloc[test_idx]['employee_id'])
print('group split, employees in both parts:', len(shared))
```
**Output:**
```
random split, employees in both parts: 163
group split, employees in both parts: 0
```
**What it means:** With a random split, 163 of the 200 employees appear on both sides. With a group split none do. In a separate check with invented employee-specific data (random forest, seed 42), the random split scored about 0.96 accuracy and the group split about 0.45 (chance level), because there was nothing real to learn.
**Alternative / pitfalls:** Or collapse to one row per employee (snapshot at a date) and predict leaving in the next 6 months. Also watch for rows after the exit date.
**Likely follow-ups:** 1) *Same issue with customers and orders?* Yes, group by customer. 2) *What about time?* Combine group and time splits where relevant.
**Common mistakes:** Using plain `KFold`; forgetting to pass `groups=`.

### Q38 ⭐ 🔴 You tune hyperparameters repeatedly and report the best score on the same test set. What is wrong, and how would you structure the data to avoid it?
**Asked at:** commonly asked (no company-specific report found); test-set reuse is a differentiator topic (judgement).
**What the interviewer is checking:** That you know the test set must be used once, at the end.
**Say this in the interview:** "Every time I pick the best setting by test score, the test set becomes part of training, so the final score is optimistic. I would split into train, validation and test, tune with validation or cross-validation on the training part, then score the test set once for the reported number."
**Explain simply:**
- **Hyperparameters** are settings you choose before training (tree depth). Trying many and keeping the best is a form of fitting.
- With enough tries, some setting looks good on the test set by luck.
- Structure: lock away a **test set** first; inside the remaining data use **cross-validation** (or a validation set) to choose settings; refit; test once.
- Optionally use **nested cross-validation** for an even more honest estimate (from memory, not run here).
**Sample data:** synthetic 600 rows, noisy labels (seed 42).
**Code (what you write in the interview):**
```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=600, n_features=20, n_informative=3,
                           flip_y=0.2, random_state=42)

# lock the test set away first; tune only on the training part
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

search = GridSearchCV(DecisionTreeClassifier(random_state=42),
                      {'max_depth': [2, 3, 4, 5, 6, 8, 10, None]}, cv=5)
search.fit(X_train, y_train)

print('best depth:', search.best_params_['max_depth'])
print('cross-validation score (tuning):', round(search.best_score_, 3))
print('final test score (used once):', round(search.score(X_test, y_test), 3))
```
**Output:**
```
best depth: 2
cross-validation score (tuning): 0.818
final test score (used once): 0.787
```
**What it means:** Report 0.787 (the one-time test score). The tuning score of 0.818 was the best of several tries and is a bit optimistic. Output depends on the seed (42).
**Alternative / pitfalls:** Small data: skip a separate validation set and rely on cross-validation. Once the final test is used and you change the model again, you need fresh data.
**Likely follow-ups:** 1) *Why not just report CV score?* It was used to pick the setting, so it is slightly optimistic. 2) *Does this matter for few tries?* Less, but the habit is right.
**Common mistakes:** Tuning and reporting on one test set; calling the validation score the "final" score.

### Q39 ⭐ 🔴 What is target (mean) encoding for a high-cardinality column such as pincode, and how can it leak the target if done carelessly?
**Asked at:** commonly asked (no company-specific report found); high-cardinality and target encoding appear in encoding prep lists (unverified).
**What the interviewer is checking:** That you know the idea and the danger that a row's own answer ends up in its feature.
**Say this in the interview:** "Target encoding replaces each category, such as a pincode, with the average target for that category, for example the attrition rate in that pincode. It avoids hundreds of dummy columns. Done carelessly, each row's own label is inside the average, especially for rare pincodes, so the model looks great on training data and fails on new data. The fix is to compute the averages out-of-fold, add smoothing, and fit only on training data."
**Explain simply:**
- **High cardinality** means a column with very many distinct values (thousands of pincodes). One-hot encoding would add thousands of columns.
- Target encoding: pincode 560001 becomes, say, 0.18 if 18% of its training employees left.
- Leak: a pincode with 2 rows, one leaver, gets 0.5 and that number partly *is* the answer for those rows.
- Fixes: compute each row's value from other folds only; **smoothing** (pull small groups toward the overall average); sklearn's `TargetEncoder` does cross-fitting internally (the class exists in sklearn 1.9.1, checked; that it cross-fits inside `fit_transform` is from memory, unverified).
**Sample data:** invented: 800 employees, 400 pincodes, and a target made of random noise, so the true predictive power is zero (seed 42).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(42)
data = pd.DataFrame({'pincode': rng.integers(0, 400, 800),   # 400 codes, ~2 rows each
                     'left': rng.integers(0, 2, 800)})        # target is pure noise
train, test = train_test_split(data, test_size=0.25, random_state=42)
train = train.copy(); test = test.copy()

# careless: each row's own target is inside its pincode average
train['naive'] = train.groupby('pincode')['left'].transform('mean')
overall = train['left'].mean()
test['naive'] = test['pincode'].map(train.groupby('pincode')['left'].mean()).fillna(overall)

# safer: encode each row using the other folds only
train['oof'] = np.nan
for fit_idx, enc_idx in KFold(5, shuffle=True, random_state=42).split(train):
    means = train.iloc[fit_idx].groupby('pincode')['left'].mean()
    train.iloc[enc_idx, train.columns.get_loc('oof')] = train.iloc[enc_idx]['pincode'].map(means).fillna(overall).values
test['oof'] = test['naive']

for col in ['naive', 'oof']:
    model = LogisticRegression().fit(train[[col]], train['left'])
    print(col, 'train acc', round(model.score(train[[col]], train['left']), 2),
          'test acc', round(model.score(test[[col]], test['left']), 2))
```
**Output:**
```
naive train acc 0.79 test acc 0.47
oof train acc 0.53 test acc 0.52
```
**What it means:** The target is pure noise, so honest accuracy is about 0.5. The careless encoding shows 0.79 on training (fake) and 0.47 on test; the out-of-fold version gives 0.53 and 0.52, which tells the truth: pincode has no signal here.
**Alternative / pitfalls:** Group rare pincodes or use region-level groups; also review fairness risk, since pincode is a proxy (Q35).
**Likely follow-ups:** 1) *Why smoothing?* Rare categories give noisy averages. 2) *Does it apply to trees?* Yes; trees can overfit it even more.
**Common mistakes:** Computing category means on the whole dataset before splitting; using the training encoding on training rows and the same on test without cross-fitting.

