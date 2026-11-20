# Book 9 — Basic ML + AI Tools for Analysts | Part 3: Decision Trees, Random Forest (Intuition) 🟡

**Target:** 38 questions | **Actual:** 43 questions
**Scope:** decision-tree and random-forest intuition for analysts: splits, Gini and entropy, overfitting controls, bagging, feature importance, short sklearn code, and explaining tree models to managers.

### Q1 ⭐⭐⭐ 🟢 What is a decision tree, and how would you explain one to a non-technical HR manager using an employee attrition example?
**Asked at:** commonly asked (no company-specific report found); decision-tree questions appear in prep-site banks and in unverified candidate reports for data roles (for example Tiger Analytics, Fractal).
**What the interviewer is checking:** Whether you can explain a model in plain words, without jargon, to a non-technical person.
**Say this in the interview:** "A decision tree is a flowchart of yes/no questions learned from past data. For attrition it might ask: does the person work overtime? Is tenure under 4 years? Each answer sends the employee down a branch until we reach a final prediction, leave or stay."
**Explain simply:**
- The tree learns the questions itself by looking at past employees whose outcome (left or stayed) is known. The outcome column is called the **label**; the columns used to guess it (tenure, overtime) are **features**.
- At each step it picks the question that separates leavers from stayers best.
- It is easy to explain because a manager can follow the path with a finger, like an HR policy flowchart.
**Sample data:** 12 employees (made-up teaching data; `left` 1 = left, 0 = stayed).

| tenure_years | overtime | left |
|---|---|---|
| 0.5 | 1 | 1 |
| 1 | 1 | 1 |
| 1.5 | 0 | 0 |
| 2 | 1 | 1 |
| 1 | 0 | 0 |
| 3 | 0 | 0 |
| 4 | 1 | 0 |
| 5 | 0 | 0 |
| 6 | 0 | 0 |
| 2 | 0 | 0 |
| 7 | 1 | 0 |
| 3.5 | 1 | 1 |

**Code (what you write in the interview):**
```python
from sklearn.tree import DecisionTreeClassifier, export_text

# employees = the 12-row table above, loaded as a pandas DataFrame
features = employees[["tenure_years", "overtime"]]
left = employees["left"]

# Keep the tree small so it stays readable
tree = DecisionTreeClassifier(max_depth=2, random_state=42)
tree.fit(features, left)

# Print the learned flowchart as text
print(export_text(tree, feature_names=list(features.columns)))
```
**Output:**
```text
|--- overtime <= 0.50
|   |--- class: 0
|--- overtime >  0.50
|   |--- tenure_years <= 3.75
|   |   |--- class: 1
|   |--- tenure_years >  3.75
|   |   |--- class: 0
```
**What it means:** In this tiny data, people without overtime stayed; people with overtime and tenure up to 3.75 years left; longer-tenure overtime workers stayed. Twelve rows is only for illustration, not evidence.
**Likely follow-ups:** 1) *Is it a prediction or an explanation?* Both loosely; it predicts, and its rules hint at patterns, but not at causes. 2) *Weakness?* A deep tree memorises the past (overfits).
**Common mistakes:** Using jargon like "recursive partitioning" with an HR audience; saying the tree proves overtime causes attrition.

### Q2 ⭐⭐⭐ 🟢 In a decision tree, what are the root node, a decision (internal) node, a leaf node, and the depth of the tree?
**Asked at:** commonly asked (no company-specific report found); root/leaf terminology is standard in prep-site question banks.
**What the interviewer is checking:** That you know the vocabulary, so you can read and discuss a tree.
**Say this in the interview:** "The root is the first question at the top, using all employees. A decision node is any later question. A leaf is the end of a branch, where the prediction is made. Depth is the number of questions you can be asked in a row along the longest path."
**Explain simply:**
- **Root node:** the top box, holds the whole dataset, asks the first question.
- **Decision (internal) node:** a box that asks a question and has branches below it.
- **Leaf node:** a box with no branches; it gives the answer (leave or stay).
- **Depth:** number of levels of questions; the root alone (no question yet) is depth 0.
**Worked example (concept question):** In the Q1 tree, "overtime <= 0.5" is the root; "tenure_years <= 3.75" is a decision node; there are 3 leaves; the longest path has 2 questions, so depth = 2 (checked in code: `get_depth()` gave 2, `get_n_leaves()` gave 3).
**Alternative / pitfalls:** Some books count the root as level 1, so state your convention. sklearn's `max_depth=2` means at most two questions in a row.
**Likely follow-ups:** 1) *Where does a tree stop growing?* When nodes are pure, or a limit like `max_depth` is hit. 2) *What is a branch?* One answer path out of a node.
**Common mistakes:** Calling every box a leaf; mixing up depth with number of nodes.

### Q3 ⭐⭐⭐ 🟢 What is a random forest, and how is it different from a single decision tree?
**Asked at:** commonly asked; "random forest vs decision tree" is reported in unverified candidate summaries for Tiger Analytics and Fractal (data-scientist roles; snippets only).
**What the interviewer is checking:** That you understand a forest is many trees voting together, and why.
**Say this in the interview:** "A random forest builds many decision trees, each on a slightly different random sample of employees and a random subset of features, then combines their votes. One tree can memorise the data; many different trees averaged are steadier on new data, at the cost of being harder to read."
**Explain simply:**
- One tree = one expert's opinion; forest = a panel of experts who each saw different files, then vote.
- Each tree is deliberately a bit different, so their individual mistakes tend to cancel out.
- For a yes/no question the forest takes the majority vote; for a number it takes the average.
- Trade-off: usually more accurate and stable, but you lose the single readable flowchart.
**Sample data:** A synthetic attrition table made up for teaching (not real HR data). Every later answer that says "synthetic attrition table" uses this generator, so you can rebuild it. `make_attrition(500)` gives 500 rows, about 22% leavers; it is split 80/20 with `train_test_split(..., test_size=0.2, random_state=42)`. Both models scored 1.0 (100%) on the 400 training rows. On the 100 unseen test rows: single unlimited tree 0.76, random forest (100 trees) 0.79.
```python
import numpy as np
import pandas as pd

def make_attrition(n_rows, seed=42, base=-1.4):
    rng = np.random.default_rng(seed)
    table = pd.DataFrame({
        'tenure_years': rng.uniform(0, 15, n_rows).round(1),
        'overtime_hours': rng.integers(0, 41, n_rows),
        'salary_band': rng.integers(1, 5, n_rows),
        'engagement_score': rng.integers(1, 6, n_rows)})
    # More overtime raises the chance of leaving; tenure, pay and engagement lower it
    score = (base + 0.12 * table['overtime_hours'] - 0.2 * table['tenure_years']
             - 0.6 * table['salary_band'] - 0.7 * (table['engagement_score'] - 3))
    chance_of_leaving = 1 / (1 + np.exp(-score))
    table['left'] = (rng.random(n_rows) < chance_of_leaving).astype(int)
    return table
```
**Worked example (concept questions):** The forest gained 3 points on unseen data (0.79 against 0.76), but with only 100 test rows that gap is noisy; report it as "about the same or slightly better", not a guaranteed win. (Exact values depend on the seed and the generator above.)
**Likely follow-ups:** 1) *Why "random"?* Random rows and random features per split. 2) *How many trees?* More is rarely harmful, just slower; 100 is the sklearn default.
**Common mistakes:** Saying a forest is "one big tree"; claiming it can never overfit.

### Q4 ⭐⭐⭐ 🟢 A node in an attrition tree holds 10 employees: 6 stayed and 4 left. Calculate its Gini impurity.
Gini = 1 minus the sum of squared class proportions.
**Asked at:** commonly asked (no company-specific report found); Gini calculation is a staple of decision-tree question banks.
**What the interviewer is checking:** Whether you can do the arithmetic and know what the number means.
**Say this in the interview:** "Proportions are 0.6 and 0.4. Gini is 1 minus (0.36 plus 0.16), which is 0.48. It is close to the maximum of 0.5 for two classes, so this node is quite mixed."
**Explain simply:**
- **Gini impurity** measures how mixed a node is: 0 means everyone is the same outcome (pure), 0.5 is the worst mix for two classes (50/50).
- Step 1: proportions: stayed 6/10 = 0.6, left 4/10 = 0.4.
- Step 2: square them: 0.36 and 0.16; add: 0.52.
- Step 3: 1 - 0.52 = **0.48** (checked by script).
**What it means:** Roughly "if I pick an employee here and guess their outcome randomly using the node's mix, I am wrong 48% of the time".
**Likely follow-ups:** 1) *Gini of a pure node?* 0. 2) *Max Gini for 2 classes?* 0.5.
**Common mistakes:** Forgetting to subtract from 1; using counts instead of proportions.

### Q5 ⭐⭐⭐ 🟡 How does a decision tree decide where to split the data at each node?
**Asked at:** commonly asked; reported (unverified, snippet-level) in Tiger Analytics and Fractal candidate summaries along with categorical vs numeric splitting.
**What the interviewer is checking:** That you know the tree tries candidate questions and keeps the one that makes groups purest.
**Say this in the interview:** "At each node the tree tries many possible questions, like tenure under 2.5 or overtime yes/no. For each, it measures how mixed the two resulting groups are, using Gini or entropy, and picks the question that reduces mixing the most. Then it repeats inside each group."
**Explain simply:**
- For a number column, it tries cut points between sorted values; for yes/no columns it tries the one split.
- Each candidate is scored by **weighted impurity** of the children (bigger groups count more).
- **Gain** = parent impurity minus weighted child impurity; the biggest gain wins.
- It is **greedy**: it picks the best split now, never looking ahead, so it can miss a better combination.
- It stops at a limit (depth, minimum leaf size) or when nodes are pure.
**Worked example (concept question):** Parent 10 employees (5 left, 5 stayed), Gini 0.50. Splitting on overtime gives weighted Gini 0.417 (gain 0.083; see Q7). A tenure split gives 0.32 (gain 0.18; see Q20), so the tree prefers tenure.
**Likely follow-ups:** 1) *Does it check every combination of questions?* No, greedy one step. 2) *Which score?* Gini by default in sklearn.
**Common mistakes:** Saying it picks the "most important column" without a scoring rule; forgetting to weight by group size.

### Q6 ⭐⭐⭐ 🟡 Why do decision trees overfit easily, and which sklearn settings (max_depth, min_samples_leaf) would you use to control it?
**Asked at:** commonly asked; "how to reduce overfitting" is reported (unverified snippets) for Tiger Analytics and Fractal.
**What the interviewer is checking:** That you understand overfitting and know concrete knobs.
**Say this in the interview:** "Left alone, a tree keeps splitting until every leaf is pure, which can mean one leaf per employee. It memorises quirks instead of patterns. I limit it with `max_depth` and `min_samples_leaf`, and pick values by checking test or cross-validation scores."
**Explain simply:**
- **Overfitting:** the model scores great on data it has seen, poorly on new data.
- Default sklearn trees have no depth limit, so they grow until training accuracy hits 100%.
- `max_depth=4`: at most 4 questions in a row.
- `min_samples_leaf=10`: every final group must contain at least 10 employees, so no rules based on 1 or 2 people.
- Other controls: `min_samples_split`, `ccp_alpha`, or use a random forest.
**Worked example (concept questions):** On the synthetic 500-row attrition data from Q3 (80/20 split), an unrestricted tree scored 1.00 train and 0.76 test. With `max_depth=5, min_samples_leaf=10` it scored 0.86 train and 0.80 test: the gap shrank from 0.24 to 0.06 and test accuracy rose by 4 points (on 100 test rows, so treat that gain as indicative, not proven).
**Alternative / pitfalls:** Choose settings with cross-validation (several train/test splits), not by peeking at one test set.
**Likely follow-ups:** 1) *Can too much limiting hurt?* Yes, underfitting (too simple). 2) *Which first?* Usually `min_samples_leaf` or `max_depth`.
**Common mistakes:** Judging only on training accuracy; setting depth so low that the tree cannot learn anything.

### Q7 ⭐⭐⭐ 🟡 Calculate the weighted Gini impurity after this split and the Gini gain, for an attrition tree split on overtime.
Parent node: 10 employees, 5 left and 5 stayed.
Overtime = Yes: 6 employees (4 left, 2 stayed). Overtime = No: 4 employees (1 left, 3 stayed).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute a split's quality step by step.
**Say this in the interview:** "Parent Gini is 0.5. Yes group: 1 - (4/6)^2 - (2/6)^2 = 0.444. No group: 1 - (1/4)^2 - (3/4)^2 = 0.375. Weighted: 0.6 times 0.444 plus 0.4 times 0.375 = 0.417. Gain is 0.5 - 0.417 = 0.083."
**Explain simply:**
- Parent Gini = 1 - 0.5^2 - 0.5^2 = 0.50.
- Overtime Yes: 0.444. Overtime No: 0.375.
- Weights: 6/10 = 0.6 and 4/10 = 0.4 (bigger group counts more).
- Weighted Gini = 0.2667 + 0.15 = **0.4167**.
- Gini gain = 0.50 - 0.4167 = **0.0833** (all values checked by script).
**What it means:** Overtime makes the groups only a little purer. A small positive gain means a weak but useful split.
**Likely follow-ups:** 1) *What would gain 0 mean?* The split does not help. 2) *Can gain be negative?* No.
**Common mistakes:** Averaging the two child Ginis without weights (gives 0.41, close here by luck); forgetting to subtract from the parent.

### Q8 ⭐⭐⭐ 🟡 You run the code below. What does the output tell you, and what would you try next?
```python
tree = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
print(tree.score(X_train, y_train), tree.score(X_test, y_test))
# output (illustrative numbers for the exercise): 1.0 0.71
```
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you spot overfitting from a train/test gap and name fixes.
**Say this in the interview:** "100% on training but 71% on test is classic overfitting: the tree memorised the training rows. I would limit the tree with `max_depth` or `min_samples_leaf`, tune with cross-validation, and try a random forest."
**Explain simply:**
- `score` here is accuracy: share of correct predictions. Train 1.0 means it got every training row right, usually by memorising.
- Test 0.71 is the honest estimate of how it behaves on new employees.
- A 29-point gap is the warning sign (a small gap is normal).
- Next steps: restrict depth or leaf size; try a random forest; check there is enough data; compare to a simple baseline (always predicting the majority class).
**What it means:** Report 0.71, not 1.0, to a manager, and check whether that beats the "always predict stay" baseline, especially if few people leave.
**Alternative / pitfalls:** If the test set is small (say 50 rows), 0.71 itself is noisy; use cross-validation.
**Likely follow-ups:** 1) *Could the train score of 1.0 ever be fine?* Only if test is also high. 2) *Could it be leakage?* Leakage would inflate test too, so here it is plain overfitting.
**Common mistakes:** Celebrating 1.0; reporting train accuracy to the business.

### Q9 ⭐⭐⭐ 🟡 Using the table, which max_depth would you pick for an attrition tree, and why?
| max_depth | Train accuracy | Test accuracy |
|---|---|---|
| 2 | 0.78 | 0.76 |
| 4 | 0.85 | 0.82 |
| 6 | 0.93 | 0.81 |
| 10 | 0.99 | 0.74 |
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you choose by test accuracy and gap, not by training accuracy.
**Say this in the interview:** "I would pick depth 4. It has the best test accuracy, 0.82, and a small train-test gap of 0.03. Beyond that, training keeps rising while test falls, which is overfitting."
**Explain simply:**
- Depth 2: simple, gap 0.02, but test only 0.76 (somewhat underfit).
- Depth 4: test peaks at 0.82; gap 0.03.
- Depth 6: test 0.81 (practically tied) but gap 0.12; more complex for no gain.
- Depth 10: train 0.99, test 0.74: memorising.
**What it means:** Depth 4 is the simplest tree that performs best on unseen data. Depths 5 and 3 were not tried, so I would check them with cross-validation before finalising.
**Alternative / pitfalls:** The tie at 4 vs 6 is within noise; prefer the simpler one.
**Likely follow-ups:** 1) *Why not depth 10?* It overfits. 2) *Is this test set reused too often?* Tuning on one test set leaks; use cross-validation.
**Common mistakes:** Picking the highest train accuracy; ignoring the gap.

### Q10 ⭐⭐⭐ 🟡 How does a random forest reduce overfitting compared with one deep decision tree? Mention bootstrap samples and random feature subsets.
**Asked at:** commonly asked; "how to reduce random forest overfitting" and "RF vs decision tree" are reported (unverified snippets) for Tiger Analytics and Fractal.
**What the interviewer is checking:** That you can link bagging and feature randomness to lower variance.
**Say this in the interview:** "Each tree trains on a bootstrap sample, meaning rows drawn at random with replacement, and each split only considers a random subset of features. That makes the trees different from each other. Averaging many different trees cancels out their individual quirks, so the forest is steadier on new data."
**Explain simply:**
- **Bootstrap sample:** pick n rows at random, with replacement (a row can appear twice or not at all).
- **Random feature subset:** at each split the tree may only choose from a few randomly picked columns, so one strong column cannot dominate every tree.
- Each tree alone may still overfit, but its errors differ from the others; voting averages them out.
- Result: lower **variance** (predictions change less if the data changes slightly).
**Alternative / pitfalls:** A forest reduces variance, not bias; if the features contain no signal, it will not help. Very deep trees in a forest can still overfit a little, so check test scores.
**Likely follow-ups:** 1) *Does more trees overfit?* Not noticeably. 2) *Why not just one big tree?* It is unstable.
**Common mistakes:** Saying the forest removes all overfitting; forgetting that the trees must differ.

### Q11 ⭐⭐⭐ 🟡 How do you get feature importance from a fitted RandomForestClassifier in sklearn, and how would you present the top three features to a manager?
```python
rf = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)
```
**Asked at:** commonly asked (no company-specific report found); importance pitfalls are covered in random-forest question banks.
**What the interviewer is checking:** That you know `feature_importances_`, and can present it without overclaiming.
**Say this in the interview:** "I read `rf.feature_importances_`, pair it with the column names, sort it and take the top three. To a manager I say these are the factors the model leaned on most, they are signals to investigate, not proven causes."
**Explain simply:**
- `feature_importances_` gives one number per column; they sum to 1. Bigger = the column reduced impurity more across the forest.
- Pair with `X_train.columns` and sort.
- Present as a short ranked list in plain words plus a caveat.
**Code (what you write in the interview):**
```python
import pandas as pd

importance = pd.Series(rf.feature_importances_, index=X_train.columns)
top_three = importance.sort_values(ascending=False).head(3)
print(top_three)
```
**What it means:** The output (not shown, as it depends on the data) is a ranked list. For a manager: "Overtime hours, tenure and engagement are the top three signals the model uses. They tell us where to look, not why people leave."
**Alternative / pitfalls:** Impurity-based importance can favour numeric or high-cardinality columns and split credit among correlated ones; see Q26 for permutation importance.
**Likely follow-ups:** 1) *Direction of effect?* Importance does not say if more overtime raises or lowers risk. 2) *Do they sum to 1?* Yes in sklearn.
**Common mistakes:** Saying "overtime causes attrition"; presenting raw decimals with no explanation.

### Q12 ⭐⭐⭐ 🟡 For an attrition-prediction task, when would you choose a single decision tree over a random forest, and when the reverse?
**Asked at:** commonly asked; tree vs forest comparison is reported (unverified snippets) for Tiger Analytics, Fractal and Flipkart business-analyst roles.
**What the interviewer is checking:** That you weigh explainability against accuracy and stability.
**Say this in the interview:** "If I must show leaders a simple rulebook, I would use a small single tree. If the goal is the best prediction and stability, I would use a random forest and explain it with feature importance."
**Explain simply:**
- **Single tree:** easy to draw, explain, even turn into policy rules; less accurate and unstable on small data.
- **Random forest:** usually more accurate, steadier, handles many features; harder to explain beyond importance charts, slower.
- Often I build both: the tree for communication, the forest as accuracy benchmark.
- Whichever I choose, I compare on test data against a simple baseline.
**Worked example (concept questions):** On the synthetic 500-row data (see Q3), the forest scored 0.79 vs 0.76 for the single tree on test rows: a modest edge, noisy at 100 rows. If that gain is tiny, the explainable tree may win.
**Likely follow-ups:** 1) *Small dataset?* Forest is still usually safer. 2) *Regulated decisions?* Lean to explainable models.
**Common mistakes:** "Forest is always better"; ignoring the explanation requirement.

### Q13 ⭐⭐ 🟢 Calculate the entropy (base 2) of a node with 5 leavers and 5 stayers, and of a node with 8 stayers and 0 leavers. What do the two values mean?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can compute entropy and read it as "mixedness".
**Say this in the interview:** "Entropy is minus the sum of p times log2 of p. The 5/5 node gives 1.0, maximum disorder. The 8/0 node gives 0, a pure node where there is no uncertainty."
**Explain simply:**
- **Entropy** measures uncertainty (how surprising the outcome of a random pick is); like Gini, lower means purer.
- 5/5: p = 0.5 and 0.5: -(0.5 x -1 + 0.5 x -1) = **1.0**.
- 8/0: p = 1 and 0: only the first term counts, 1 x log2(1) = 0, so entropy **0** (treat 0 x log 0 as 0).
**What it means:** 1.0 = a coin flip, nothing learned; 0 = certain. A good split lowers entropy in the children.
**Likely follow-ups:** 1) *Max entropy for 2 classes?* 1. 2) *Why base 2?* Measures in bits.
**Common mistakes:** Trying log of 0 and getting an error; forgetting the minus sign.

### Q14 ⭐⭐ 🟢 Do decision trees and random forests need feature scaling? Do they need categorical columns to be encoded in sklearn?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know which models need scaling, and the sklearn input rule.
**Say this in the interview:** "No scaling is needed, because a tree only asks 'is this value above a cut point', so the order matters, not the size. But in sklearn, text columns must be turned into numbers first, for example with one-hot encoding."
**Explain simply:**
- Salary in rupees vs tenure in years makes no difference to a tree (verified: multiplying all features by 1000 gave identical predictions).
- Distance-based models (k-nearest neighbours, k-means) and linear models with regularisation do need scaling.
- sklearn trees need numeric input: fitting on a text column "HR" raised `ValueError: could not convert string to float: 'HR'` in my test.
- Encoding: one-hot (`pd.get_dummies`) for unordered labels like department; ordered numbers for ordered labels like salary band.
**Alternative / pitfalls:** Some other libraries (for example LightGBM, CatBoost) handle categories natively (from memory, unverified); sklearn's own tree classes do need numbers as tested here.
**Likely follow-ups:** 1) *Does scaling hurt?* Harmless, just unnecessary. 2) *Label-encode department?* Risky; it invents an order.
**Common mistakes:** Scaling "just in case" and claiming it was needed; feeding strings directly.

### Q15 ⭐⭐ 🟢 Read the printed tree below. What does it predict for an employee with tenure 1.5 years who works overtime, and what rule did you follow?
```
|--- tenure <= 2.5
|   |--- overtime <= 0.5   (0 = No, 1 = Yes)
|   |   |--- class: stay
|   |--- overtime >  0.5
|   |   |--- class: leave
|--- tenure >  2.5
|   |--- class: stay
```
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you trace a path through a tree.
**Say this in the interview:** "Tenure 1.5 is at most 2.5, so I go to the first branch. Overtime is 1, which is greater than 0.5, so I take that branch and land on leave. The rule: tenure up to 2.5 years and works overtime, predict leave."
**Explain simply:**
- Start at the top; check tenure: 1.5 <= 2.5, true, go into the first block.
- Next question: overtime <= 0.5? Overtime is 1 (Yes), so no; take "overtime > 0.5".
- That leaf says **leave**.
- Anyone with tenure over 2.5 is predicted to stay, whatever else is true.
**What it means:** Short-tenure employees who work overtime are flagged as likely leavers.
**Likely follow-ups:** 1) *Prediction for tenure 1.5, no overtime?* Stay. 2) *Why 0.5 for yes/no?* The tree cuts between 0 and 1.
**Common mistakes:** Reading the overtime split before the tenure split; confusing the "<= 0.5" branch with Yes.

### Q16 ⭐⭐ 🟢 Write short sklearn code to split an attrition dataset, fit a RandomForestClassifier and print test accuracy.
Assume `X` (features, all numeric) and `y` (1 = left, 0 = stayed) already exist.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the standard split, fit, score routine, and keep the test set untouched.
**Say this in the interview:** "I hold out 20% of the rows as a test set, fit the forest on the other 80%, and score on the held-out rows, since that tells me how it behaves on new employees."
**Explain simply:**
- `train_test_split`: random split; `random_state=42` makes it repeatable.
- `fit`: the model learns from training rows only.
- `score`: for classifiers, accuracy on the rows you give it.
**Sample data:** First rows of `X` (the 500-row synthetic table from Q3, made up for teaching, built with `make_attrition(500)`; `X` is its four feature columns and `y` is `left`):

| tenure_years | overtime_hours | salary_band | engagement_score |
|---|---|---|---|
| 11.6 | 33 | 3 | 5 |
| 6.6 | 30 | 2 | 1 |
| 12.9 | 22 | 1 | 2 |
| 10.5 | 36 | 2 | 3 |
| 1.4 | 5 | 3 | 4 |

**Code (what you write in the interview):**
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Keep 20% of employees aside as a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Accuracy on employees the model has never seen
print("Test accuracy:", round(model.score(X_test, y_test), 3))
```
**Output:**
```text
Test accuracy: 0.79
```
**What it means:** About 79 of 100 unseen employees were classified correctly (output depends on the data and seed). Compare it with the baseline of always predicting the majority class (here 75% of test employees stayed, so 0.79 only modestly beats it), and for real data report precision and recall too (Q24).
**Likely follow-ups:** 1) *Why random_state?* Same split every run. 2) *Imbalanced classes?* Add `stratify=y`.
**Common mistakes:** Scoring on training data; forgetting the split; not setting a seed.

### Q17 ⭐⭐ 🟢 What do the n_estimators and max_depth parameters of RandomForestClassifier control?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the two most common forest knobs.
**Say this in the interview:** "`n_estimators` is how many trees are in the forest. `max_depth` is how deep each tree may grow. More trees mostly gives steadier results; limiting depth keeps each tree simpler to avoid overfitting."
**Explain simply:**
- `n_estimators=100` (the default in the version I ran): 100 trees vote. More trees = steadier but slower; gains flatten out.
- `max_depth=None` by default: trees grow until leaves are pure; setting e.g. 5 caps each tree at 5 questions deep.
- Tune `max_depth` (controls overfitting) more carefully than `n_estimators` (just needs to be large enough).
**Worked example (concept questions):** `RandomForestClassifier(n_estimators=300, max_depth=5, random_state=42)` is 300 shallow trees, each at most 5 questions deep.
**Likely follow-ups:** 1) *Does more trees overfit?* Not normally. 2) *Other knobs?* `min_samples_leaf`, `max_features`.
**Common mistakes:** Thinking `n_estimators` is the number of rows or features; believing more trees always improves accuracy.

### Q18 ⭐⭐ 🟢 Five trees in a random forest predict leave, stay, leave, leave, stay for one employee. What does the forest predict by majority vote? If the five trees give leave probabilities 0.8, 0.3, 0.6, 0.7, 0.2, what is the averaged probability?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you understand how a forest combines trees.
**Say this in the interview:** "Three votes for leave against two for stay, so the forest says leave. Averaging the probabilities: 0.8 + 0.3 + 0.6 + 0.7 + 0.2 = 2.6, divided by 5 gives 0.52."
**Explain simply:**
- Votes: leave 3, stay 2: **leave**.
- Average probability: 2.6 / 5 = **0.52** (checked by script).
- 0.52 is just above 0.5, so a 50% cut-off also says leave, but it is a close call.
**What it means:** The forest is only mildly confident; for a manager, say "about a 52% estimated chance", not "will leave".
**Alternative / pitfalls:** In sklearn, `predict_proba` averages the trees' probabilities and `predict` picks the highest averaged class (from memory of the docs, unverified here); this can differ from a strict hard vote in rare cases.
**Likely follow-ups:** 1) *Regression forest?* Average the numbers. 2) *Different threshold?* You can set e.g. 0.4 to catch more leavers.
**Common mistakes:** Treating 0.52 as certainty; averaging only the "leave" trees' numbers.

### Q19 ⭐⭐ 🟢 A manager says a random forest is a black box and refuses to trust it. What do you say?
**Asked at:** commonly asked (no company-specific report found); a stakeholder-communication gap-fill question.
**What the interviewer is checking:** Whether you can respond calmly with evidence and honest limits.
**Say this in the interview:** "That is a fair concern. We can open it up partly: feature importance shows what it relies on, and I can check it on data it has never seen, and show a simple tree or example cases next to it. If explainability matters most, I can use a smaller tree and accept a little less accuracy."
**Explain simply:**
- Agree first: you cannot read 200 trees, so scepticism is healthy.
- Offer evidence: test accuracy, comparison with a simple baseline, precision and recall.
- Offer explanation: feature importance, permutation importance (Q26), a simplified single tree, a few individual case walk-throughs.
- Offer a safety plan: use predictions to prioritise conversations, not to make final decisions about people.
- Offer a choice: a simpler tree if trust matters more than the last few points of accuracy.
**Likely follow-ups:** 1) *Is a single tree more trustworthy?* Easier to read, not automatically more accurate. 2) *What if they still refuse?* Pilot it alongside current practice.
**Common mistakes:** Getting defensive; overselling importance charts as proof of causes.

### Q20 ⭐⭐ 🟡 Compare two candidate splits using weighted Gini impurity. Which one would the tree choose?
Parent node: 10 employees, 5 left and 5 stayed.
Split A (overtime): Yes = 6 (4 left, 2 stayed), No = 4 (1 left, 3 stayed).
Split B (tenure < 2 years): Yes = 5 (4 left, 1 stayed), No = 5 (1 left, 4 stayed).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you apply the weighted-Gini rule to decide between splits.
**Say this in the interview:** "Split A weighted Gini is 0.417. Split B: each child is 1 - 0.8^2 - 0.2^2 = 0.32, so weighted is 0.32. Lower is better, so the tree picks split B, tenure under 2 years."
**Explain simply:**
- Split A: Yes 0.444 (weight 0.6) + No 0.375 (weight 0.4) = **0.417**, gain 0.083.
- Split B: both children 0.32, weights 0.5 each: **0.32**, gain 0.18.
- The tree picks the split with the largest gain, equivalently the lowest weighted impurity: **B**.
**What it means:** Tenure separates leavers from stayers more cleanly here (80% pure on each side) than overtime does.
**Likely follow-ups:** 1) *Would entropy agree?* Usually but not always. 2) *What next?* The tree splits each child again.
**Common mistakes:** Picking the split with the larger child; skipping the weights.

### Q21 ⭐⭐ 🟡 Calculate the information gain (entropy-based) of this split.
Parent: 8 employees, 4 left and 4 stayed.
Left child: 4 employees (3 left, 1 stayed). Right child: 4 employees (1 left, 3 stayed).
Use log2(0.75) = -0.415 and log2(0.25) = -2.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can compute entropy gain step by step.
**Say this in the interview:** "Parent entropy is 1. Each child has proportions 0.75 and 0.25, entropy = -(0.75 x -0.415 + 0.25 x -2) = 0.811. Both children are the same size, so weighted entropy is 0.811. Information gain = 1 - 0.811 = 0.189."
**Explain simply:**
- **Information gain** = parent entropy minus weighted child entropy (like Gini gain).
- Parent 4/4: entropy = 1.
- Child entropy: 0.75 x 0.415 = 0.311; 0.25 x 2 = 0.5; total **0.811** (script gives 0.8113).
- Weights 4/8 each: weighted 0.811.
- Gain = 1 - 0.811 = **0.189** (script: 0.1887).
**What it means:** The split recovers about 19% of one bit of uncertainty: helpful but not decisive.
**Likely follow-ups:** 1) *Could gain exceed 1?* Not for two classes. 2) *Is the right child's entropy the same as the left?* Yes, the mix is just flipped.
**Common mistakes:** Forgetting the minus sign; not weighting by child size when sizes differ.

### Q22 ⭐⭐ 🟡 A regression tree predicts monthly store sales. Calculate the total squared error before and after splitting the six stores into {10, 12, 14} and {30, 32, 34} (sales in lakh rupees).
Stores: 10, 12, 14, 30, 32, 34. Predict each group by its mean.
**Asked at:** commonly asked (no company-specific report found); the categorical-vs-numeric target split is reported (unverified snippets) for Tiger Analytics and Fractal.
**What the interviewer is checking:** That you know a regression tree predicts the group mean and splits to reduce squared error.
**Say this in the interview:** "Before the split, the prediction is the overall mean, 22, and squared errors total 616. After the split, the means are 12 and 32, and the errors total 8 plus 8, which is 16. The split removes 600 of the 616."
**Explain simply:**
- Before: mean = (10+12+14+30+32+34)/6 = 22. Errors: -12, -10, -8, 8, 10, 12; squares 144, 100, 64, 64, 100, 144; total **616**.
- After: group 1 mean 12, errors -2, 0, 2: 4 + 0 + 4 = 8. Group 2 mean 32, errors the same: 8.
- Total after = **16**.
- Reduction = 616 - 16 = 600, about 97% (all checked by script).
**What it means:** This is the regression-tree version of "purity": squared error plays the role of Gini.
**Likely follow-ups:** 1) *Prediction for a new store in the low group?* 12 lakh. 2) *Why mean?* The mean minimises squared error.
**Common mistakes:** Using absolute errors by mistake; forgetting each group has its own mean.

### Q23 ⭐⭐ 🟡 What is the difference between Gini impurity and entropy, and which one is the sklearn default?
**Asked at:** commonly asked (no company-specific report found); Gini vs entropy appears in prep-site decision-tree question banks (Analytics Vidhya, Coursera, Simplilearn; unverified).
**What the interviewer is checking:** Whether you know both are "how mixed is this group" scores and that the choice rarely matters in practice.
**Say this in the interview:** "Both measure how mixed a node is. Gini is 1 minus the sum of squared class shares; entropy uses logarithms. They almost always pick the same splits. sklearn's default is Gini."
**Explain simply:**
- A node is a group of employees at one point in the tree. Impurity is how mixed that group is: all stayers is pure (score 0), a 50/50 mix is the most mixed.
- Gini impurity = 1 minus (share of stayers squared + share of leavers squared). Its highest value for two classes is 0.5.
- Entropy = minus the sum of (share x log base 2 of share). Its highest value for two classes is 1.
- Entropy punishes mixed groups slightly harder and needs a logarithm, so it is a little slower. Gini is the default (`criterion='gini'`, verified on sklearn 1.9.1); you switch with `criterion='entropy'`.
**Worked example (concept question):** Stayer/leaver shares and their scores (computed by script):

| Node mix | Gini | Entropy |
|---|---|---|
| 50% / 50% | 0.500 | 1.000 |
| 80% / 20% | 0.320 | 0.722 |
| 95% / 5% | 0.095 | 0.286 |
| 100% / 0% | 0.000 | 0.000 |

Both fall as the group gets purer; only the scale differs.
**Alternative / pitfalls:** Do not claim one is "better". Comparing them is a tuning choice, not a fix for a bad model. Information gain (Q21) is the drop in entropy after a split.
**Likely follow-ups:** 1) *Does it change the final tree much?* Rarely; usually the same or very similar splits. 2) *Is a lower value good?* Yes, lower means purer.
**Common mistakes:** Saying entropy is the default; mixing up the maximum values (0.5 vs 1); thinking impurity is the same as error rate.

### Q24 ⭐⭐ 🟡 An attrition dataset has 950 stayers and 50 leavers. A tree that always predicts stay is 95% accurate. Why is this a problem, and how can you handle imbalance in a tree or forest?
Mention class_weight='balanced' and what you would measure instead of accuracy.
**Asked at:** commonly asked (no company-specific report found); a gap-fill topic for analyst interviews, not tied to a named company.
**What the interviewer is checking:** Whether you see that accuracy hides a useless model when one class is rare, and know the fixes.
**Say this in the interview:** "95% accuracy just reflects that 95% of people stay. The model finds none of the leavers, which is the whole point. I would use recall and precision for the leaver class, and add class_weight='balanced'."
**Explain simply:**
- Imbalance means one outcome (stay) is far more common than the other (leave). Accuracy counts all correct answers, so predicting "stay" for everyone scores 95% while catching zero leavers.
- Recall for leavers = of the people who really left, what share did we flag. Precision = of the people we flagged, what share really left. Report both, plus the F1 score (one number blending them).
- Fixes: `class_weight='balanced'` (each leaver counts more during training), use a stratified split so the test set keeps the same mix, and lower the decision cut-off using `predict_proba` (Q28).
- Other fixes: collect more leaver rows, or resample (oversample leavers or undersample stayers, on the training data only).
**Sample data:** 1,000 employees (950 stayers, 50 leavers) with `overtime_hours`, `tenure_years`, `salary_band`, `left` (synthetic, built from the Q3 generator by sampling 950 stayers and 50 leavers out of `make_attrition(3000)` with `random_state=42`). A stratified 75/25 split (`train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)`) gives 750 training rows and 250 test rows with 12 leavers.
**Code (what you write in the interview):**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score

# Same forest twice: ignoring imbalance, then weighting leavers more
plain_forest = RandomForestClassifier(min_samples_leaf=5, random_state=42)
balanced_forest = RandomForestClassifier(min_samples_leaf=5, class_weight='balanced', random_state=42)

for name, model in [('plain', plain_forest), ('balanced', balanced_forest)]:
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print(name,
          'accuracy', round((predictions == y_test).mean(), 2),
          'recall', round(recall_score(y_test, predictions), 2),
          'precision', round(precision_score(y_test, predictions, zero_division=0), 2))
```
**Output:**
```text
plain accuracy 0.95 recall 0.0 precision 0.0
balanced accuracy 0.8 recall 0.67 precision 0.15
```
**What it means:** The plain forest is 95% accurate but finds no leavers. The balanced one finds 8 of 12 leavers (recall 0.67) at the cost of accuracy and many false alarms (it flagged 54 people and only 8 really left, precision 0.15). Tell a manager the recall and precision for leavers, not accuracy. (Only 12 leavers are in the test set, so these numbers are shaky; the exact values depend on the seed.)
**Alternative / pitfalls:** `class_weight='balanced_subsample'` recomputes weights inside each tree's sample. Never oversample before splitting, or copies of the same person land in both train and test (leakage).
**Likely follow-ups:** 1) *What is the accuracy baseline here?* 95%, always predicting stay. 2) *Which metric if missing a leaver is costly?* Recall; if false alarms are costly, precision.
**Common mistakes:** Celebrating 95% accuracy; resampling before the split; not using a stratified split.

### Q25 ⭐⭐ 🟡 Interpret the importance table, and say what it does not prove.
| Feature | Importance |
|---|---|
| overtime_hours | 0.42 |
| tenure_years | 0.31 |
| salary_band | 0.17 |
| department | 0.10 |
(Values from a fitted RandomForestClassifier; they sum to 1.)
**Asked at:** commonly asked (no company-specific report found); feature-importance pitfalls appear in random-forest question banks (unverified).
**What the interviewer is checking:** Whether you read it as "what the model relied on" and refuse to turn it into cause and effect.
**Say this in the interview:** "Overtime and tenure carry most of the model's splitting power, about 73% together. But importance shows what the model used to predict, not what causes people to leave, and it does not tell the direction."
**Explain simply:**
- Feature importance is a share of how much each column helped the trees separate leavers from stayers. The four add up to 1.00 (0.42 + 0.31 + 0.17 + 0.10, checked).
- Reading: overtime_hours was used the most (42%), then tenure_years (31%), then salary_band (17%), then department (10%).
- It does not show direction: is high or low overtime linked to leaving? Plot the relationship or look at group averages.
- It does not prove cause: overtime may be a symptom (burnout, understaffing) and not the reason. Correlated columns also split the credit between them, so one can look weaker than it is.
**Alternative / pitfalls:** Check with permutation importance on test data (Q26). A low value does not mean "irrelevant" if a correlated column carries the same signal. Never say "reducing overtime will cut attrition by 42%".
**Likely follow-ups:** 1) *Does 0.10 for department mean department does not matter?* Not necessarily; it matters less for this model. 2) *How would you test cause?* A controlled pilot or an experiment, not a model.
**Common mistakes:** Reading importance as percentage effect on attrition; ignoring direction; claiming causation; ignoring that importance depends on the data and model.

### Q26 ⭐⭐ 🟡 What are the weaknesses of impurity-based feature importance, and what is permutation importance?
**Asked at:** commonly asked (no company-specific report found); the pitfalls and permutation importance appear in random-forest question banks and the sklearn docs (summary from snippets, unverified).
**What the interviewer is checking:** Whether you know the default importance can mislead and the fairer alternative.
**Say this in the interview:** "The default importance is computed on training data and favours columns with many distinct values, even random ones. Permutation importance shuffles one column on test data and measures how much the score drops, which is more honest."
**Explain simply:**
- Impurity importance (`feature_importances_`) adds up how much each column reduced impurity across all splits, measured on training data. A column that lets a tree memorize (like an ID with many unique values) gets credit even though it has no real signal.
- It also splits credit between correlated columns, and says nothing about test performance.
- Permutation importance: shuffle one column in the test set (breaking its link with the answer) and see how much the score falls. A big fall means the model truly relied on it; about zero means it did not matter.
**Sample data:** The 1,000-row synthetic table `make_attrition(1000)` (Q3 generator) with columns `overtime_hours`, `tenure_years`, `salary_band`, plus a meaningless `employee_id` added on purpose (`np.random.default_rng(0).permutation(1000)`, a shuffled list of numbers 0 to 999). Split with `test_size=0.25, random_state=42`: 750 training rows, 250 test rows.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance

model = RandomForestClassifier(random_state=42).fit(X_train, y_train)

# Built-in importance (measured on training data)
print(pd.Series(model.feature_importances_, index=X_train.columns).round(3).sort_values(ascending=False))

# Permutation importance (measured on test data)
result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
print(pd.Series(result.importances_mean, index=X_test.columns).round(3).sort_values(ascending=False))
```
**Output:**
```text
overtime_hours    0.335
tenure_years      0.290
employee_id       0.280
salary_band       0.095
dtype: float64
overtime_hours    0.049
tenure_years      0.026
salary_band       0.005
employee_id      -0.020
dtype: float64
```
**What it means:** The random `employee_id` looks like a top-three column in the built-in table (0.280, almost level with tenure) but drops to about zero (-0.020, slightly negative by chance) in permutation importance. Trust the second table. Values depend on the seed.
**Alternative / pitfalls:** Permutation importance can also understate columns that are strongly correlated with another one (shuffling one leaves the other to cover). Run it on test data, not training data.
**Likely follow-ups:** 1) *Does permutation importance prove cause?* No. 2) *What is the cost?* More computing time (one re-score per shuffle).
**Common mistakes:** Trusting the default table blindly; including ID columns as features; computing permutation importance on training data.

### Q27 ⭐⭐ 🟡 What are a bootstrap sample and bagging? Roughly what fraction of rows is left out of each bootstrap sample when the dataset is large?
Hint: the chance a given row is never picked in n draws with replacement is (1 - 1/n)^n, which approaches 0.368 as n grows.
**Asked at:** commonly asked (no company-specific report found); bagging and bootstrap are standard in bagging and random-forest question banks (Analytics Vidhya and others; unverified).
**What the interviewer is checking:** Whether you understand sampling with replacement and why some rows are always left out.
**Say this in the interview:** "A bootstrap sample draws n rows with replacement from n rows, so some repeat and about 37% are left out. Bagging trains one model on each bootstrap sample and averages them. The left-out rows are used for the out-of-bag check."
**Explain simply:**
- With replacement means after picking a row you put it back, so it can be picked again.
- Bootstrap sample: pick n rows this way from a table of n rows. Each sample has repeats and misses some rows.
- Bagging ("bootstrap aggregating"): build many models, each on its own bootstrap sample, then average their predictions (or take a majority vote). This cuts variance (how much a model changes with the data).
- Chance a given row is never picked in n draws = (1 - 1/n)^n, which settles near 0.368. So about 63% of distinct rows are in each sample and about 37% are out.
**Worked example (concept question):** Computed by script:

| n (rows) | (1 - 1/n)^n |
|---|---|
| 10 | 0.349 |
| 100 | 0.366 |
| 1,000 | 0.368 |
| 100,000 | 0.368 |

A simulated bootstrap of 1,000 employees (`np.random.default_rng(42).integers(0, 1000, 1000)`) left out 363 of them (36.3%); a different seed gives a slightly different count.
**Alternative / pitfalls:** For small datasets the fraction differs a little (0.349 at n=10). The 0.368 value is 1/e, from the same limit used in compound interest.
**Likely follow-ups:** 1) *Where do the left-out rows get used?* The out-of-bag score (Q34). 2) *Does bagging reduce bias?* Mainly it reduces variance.
**Common mistakes:** Saying the sample has no repeats; saying 37% of rows are removed from the dataset (only from that one sample); mixing up bagging with random subsets of columns.

### Q28 ⭐⭐ 🟡 What does predict_proba return for a random forest, and how would you use it to list the 20% of employees most at risk of leaving?
```python
probs = rf.predict_proba(X_test)[:, 1]
```
**Asked at:** commonly asked (no company-specific report found); a gap-fill topic for analyst interviews.
**What the interviewer is checking:** Whether you can turn model scores into a ranked action list.
**Say this in the interview:** "predict_proba returns, for each employee, the probability of each class; column 1 is the chance of leaving. For a forest it is the average vote of the trees. I take the 80th percentile as a cut-off and keep everyone at or above it."
**Explain simply:**
- Output: a table with one row per employee and one column per class (order is in `rf.classes_`, here [0, 1]). Each row sums to 1.
- For a forest, the probability is the average of the trees' predicted probabilities, roughly the share of trees voting "leave". It is a ranking score, not a guaranteed true chance.
- `[:, 1]` keeps all rows and only the "left" column.
- The top 20% = those at or above the 80th percentile of scores, then sort so the riskiest come first.
**Sample data:** The 1,000-row synthetic table `make_attrition(1000)` (Q3 generator), features `overtime_hours`, `tenure_years`, `salary_band`; 750 training and 250 test rows (`test_size=0.25, random_state=42`). `rf` is a `RandomForestClassifier(random_state=42)` fitted on the training rows. Test rows look like this:

| overtime_hours | tenure_years | salary_band |
|---|---|---|
| 1 | 5.6 | 2 |
| 7 | 4.5 | 3 |
| 7 | 0.0 | 1 |

**Code (what you write in the interview):**
```python
import numpy as np

# column 1 = probability of "left"; column 0 = probability of "stayed"
probs = rf.predict_proba(X_test)[:, 1]

# the 80th percentile is the cut-off for the top 20%
cutoff = np.percentile(probs, 80)
at_risk = X_test[probs >= cutoff].copy()
at_risk['risk'] = probs[probs >= cutoff]
print(len(at_risk), 'of', len(X_test), 'employees flagged')
print(at_risk.sort_values('risk', ascending=False).head(3).round(2))
```
**Output:**
```text
52 of 250 employees flagged
     overtime_hours  tenure_years  salary_band  risk
893              37           1.5            1  0.99
286              37           0.7            1  0.96
836              39          11.4            1  0.90
```
**What it means:** 52 of 250 employees are flagged (a few tied scores push it just over 50), riskiest first. In this test set 44% of the flagged group really left, against 24% overall (about 1.9 times the average), so the ranking is useful. Report that lift, not just the list.
**Alternative / pitfalls:** `predict` uses a 0.5 cut-off, which is a poor fit for rare outcomes; ranking by probability lets you pick the cut-off to match HR capacity. Forest probabilities can be poorly calibrated (0.8 does not mean 80% will leave).
**Likely follow-ups:** 1) *Why the 80th percentile?* It leaves 20% of scores above it. 2) *What about ties?* Several people can share a score, so the count can slightly exceed 20%.
**Common mistakes:** Using `[:, 0]` (the stay probability); sorting the wrong way; using `predict` when you need a ranking; treating scores as exact risks.

### Q29 ⭐⭐ 🟡 A sales model is trained on stores whose monthly sales were between 50 and 100 lakh. A regression tree and a linear regression are asked to predict a store expected at 150 lakh. How do their predictions behave, and why?
**Asked at:** commonly asked (no company-specific report found); extrapolation is a gap-fill topic for analyst interviews.
**What the interviewer is checking:** Whether you know trees cannot go beyond what they saw, while lines keep going.
**Say this in the interview:** "The tree gives a flat answer near the highest value it saw, because each leaf predicts an average of training rows. The linear model extends its line and gives a much bigger number, which may or may not be believable. Either way, 150 is outside the data, so I would not trust it."
**Explain simply:**
- Premise note: the question says sales between 50 and 100 lakh were the training data and then asks for a store "at 150". A model predicts sales from other columns, so I read it as: the input value (last year's monthly sales) is 150, outside the 50-100 range the model saw.
- Regression tree: each leaf predicts the average of the training stores in it. Beyond the top range everything falls into the last leaf, so the forecast stays flat (capped).
- Linear regression: fits a straight line and continues it forever. It gives a higher number, only valid if the straight-line pattern really continues.
- Forests behave like trees: they cannot extrapolate either.
**Sample data:** 60 stores with `last_year_sales` between 50 and 100 and `this_year_sales` (made-up; built with `rng = np.random.default_rng(42)`, `last = rng.uniform(50, 100, 60).round(1)`, `this_year = (5 + 1.05 * last + rng.normal(0, 4, 60)).round(1)`).

| last_year_sales | this_year_sales |
|---|---|
| 88.7 | 94.7 |
| 71.9 | 84.4 |
| 92.9 | 95.8 |
| 84.9 | 92.8 |
| 54.7 | 63.1 |

**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

X = stores[['last_year_sales']]
y = stores['this_year_sales']
tree = DecisionTreeRegressor(max_depth=3, random_state=42).fit(X, y)
line = LinearRegression().fit(X, y)

# last_year_sales values: one inside the range, then outside it
new_stores = pd.DataFrame({'last_year_sales': [100, 150]})
print('Tree  :', tree.predict(new_stores).round(1))
print('Linear:', line.predict(new_stores).round(1))
```
**Output:**
```text
Tree  : [109.2 109.2]
Linear: [109.1 161.4]
```
**What it means:** At 100 both agree (about 109). At 150 the tree is stuck at 109.2 while the line says 161.4. Neither is verified, because no store like that was in the training data.
**Alternative / pitfalls:** The fix is data: include larger stores, or say "outside the range, estimate unreliable". Do not quote a number from outside the training range without a warning.
**Likely follow-ups:** 1) *Which would you trust at 150?* Neither blindly; the line if there is a business reason the pattern is linear. 2) *Does a random forest extrapolate?* No, same flat behaviour.
**Common mistakes:** Believing a tree "predicts higher" for bigger inputs without limit; trusting a straight line far outside the data.

### Q30 ⭐⭐ 🟡 A node has 9 employees and you set min_samples_leaf=5. Can it split? What if it has 12 employees?
**Asked at:** commonly asked (no company-specific report found); a short check on understanding of tree controls.
**What the interviewer is checking:** Whether you understand that the setting is about the size of the children (leaves), not the parent.
**Say this in the interview:** "With 9 employees it cannot split: two leaves of at least 5 each would need at least 10 people. With 12 it can, for example 5 and 7 or 6 and 6."
**Explain simply:**
- `min_samples_leaf=5` means every leaf (final box at the bottom) must keep at least 5 employees after a split.
- A split makes two groups. Both must have 5 or more, so the parent needs 10 or more.
- 9 employees: the best you could do is 5 and 4, so the split is not allowed and the node stays a leaf.
- 12 employees: allowed splits are 5/7, 6/6 or 7/5 (not 4/8 or 3/9 or 2/10 or 1/11).
**Worked example (concept question):** I checked it on sklearn 1.9.1 with a toy column that separates 9 and 12 employees into a lower and upper half. With 9 employees the tree stayed a single leaf (1 leaf). With 12 it split into two leaves of 6 and 6 (3 nodes in total).
**Alternative / pitfalls:** `min_samples_split` is different: it limits whether a node may split (parent size), not the child size. A node can also stay unsplit for other reasons, such as being pure already.
**Likely follow-ups:** 1) *Why use it?* It stops tiny, memorized leaves and reduces overfitting. 2) *What value?* Often 5 to 20 for small HR datasets, tuned by cross-validation.
**Common mistakes:** Mixing it up with `min_samples_split`; saying a 9-person node can split into 5 and 4.

### Q31 ⭐⭐ 🟡 What is data leakage in a tree-based attrition model? Give two examples of columns that would leak.
**Asked at:** commonly asked (no company-specific report found); a gap-fill topic for analyst interviews.
**What the interviewer is checking:** Whether you can spot columns that carry the answer or only exist after the outcome.
**Say this in the interview:** "Leakage is when the model sees information it would not have at prediction time, so test scores look great but real performance collapses. Two examples: exit_interview_completed and last_working_day or notice_period_served."
**Explain simply:**
- Leakage means a training column contains the answer or is created after the outcome. The model learns the shortcut, not the real drivers.
- Examples that leak in attrition: `exit_interview_completed` (only leavers have one), `last_working_day` or `termination_date` (only exist for leavers), `full_and_final_settlement_paid`, or an "attrition risk flag" HR added after resignation.
- Also leakage: fitting scalers or imputers on all data before splitting, or the same person appearing in both train and test.
- Test: ask "would I know this value on the day I make the prediction?" If no, drop it.
**Worked example (concept question):** I added a column `exit_interview_done` (about 95% of leavers have it, 2% of stayers; random draws, seed 1) to `make_attrition(1000)` and used all four feature columns. Test accuracy of a random forest (`random_state=42`, 75/25 split) rose from 0.78 to 0.984. A jump like that from one column should make you suspicious, not happy.
**Alternative / pitfalls:** Check the top importance columns for anything that sounds like "after the fact". Split data by time when predicting the future (train on earlier months, test on later ones).
**Likely follow-ups:** 1) *How do you find leakage?* Suspiciously high scores and importance dominated by one odd column. 2) *Is a strong predictor always leakage?* No; it is leakage only if unavailable at prediction time.
**Common mistakes:** Keeping outcome-related columns; imputing or scaling before the split; celebrating a 98% model without questioning it.

### Q32 ⭐⭐ 🟡 How do you prepare categorical columns and missing values before fitting a tree in sklearn? Show a short pandas example.
```python
df = pd.read_csv('hr.csv')  # columns include department (text), salary_band (text), tenure_years (some NaN)
```
**Asked at:** commonly asked (no company-specific report found); data preparation is part of the model-building questions in prep guides.
**What the interviewer is checking:** Whether you can turn text into numbers sensibly and handle gaps without losing information.
**Say this in the interview:** "sklearn trees need numbers, so I map ordered text like salary band to ordered numbers, one-hot encode unordered text like department, and fill missing numbers with the median plus a flag column saying it was missing. I fit these steps on training data only."
**Explain simply:**
- Ordered categories (low, mid, high): map to 1, 2, 3. A tree can then split on "band above 1.5".
- Unordered categories (Sales, HR, IT): one-hot encoding, one 0/1 column per value (`pd.get_dummies`). Numbering them 1, 2, 3 would invent a fake order.
- Missing numbers: fill with the median (not hurt by outliers), and add a 0/1 `tenure_missing` column, because missing can itself mean something.
- Do the filling after the train/test split, using the training median, or you leak test information.
**Sample data:** `hr.csv` (6 rows, made-up):

| department | salary_band | tenure_years | left |
|---|---|---|---|
| Sales | low | 2.0 | 1 |
| HR | mid | NaN | 0 |
| IT | high | 7.5 | 0 |
| Sales | mid | 4.0 | 1 |
| IT | low | NaN | 0 |
| HR | high | 10.0 | 0 |

**Code (what you write in the interview):**
```python
import pandas as pd

df = pd.read_csv('hr.csv')

# Ordered text: map to numbers that keep the order
df['salary_band'] = df['salary_band'].map({'low': 1, 'mid': 2, 'high': 3})

# Unordered text: one 0/1 column per department
df = pd.get_dummies(df, columns=['department'], dtype=int)

# Missing numbers: flag them, then fill with the median
df['tenure_missing'] = df['tenure_years'].isna().astype(int)
df['tenure_years'] = df['tenure_years'].fillna(df['tenure_years'].median())
print(df.to_string())
```
**Output:**
```text
   salary_band  tenure_years  left  department_HR  department_IT  department_Sales  tenure_missing
0            1          2.00     1              0              0                 1               0
1            2          5.75     0              1              0                 0               1
2            3          7.50     0              0              1                 0               0
3            2          4.00     1              0              0                 1               0
4            1          5.75     0              0              1                 0               1
5            3         10.00     0              1              0                 0               0
```
**What it means:** Everything is now numeric. The two missing tenures became 5.75 (the median of 2, 4, 7.5, 10) and are flagged.
**Alternative / pitfalls:** A `SimpleImputer` and `OneHotEncoder` inside a `Pipeline` do the same safely inside cross-validation (from memory, not run here). Some newer sklearn versions let trees handle missing values natively; that varies by version (from memory, unverified).
**Likely follow-ups:** 1) *Why not label-encode department?* It invents an order that a tree may split on. 2) *Why the median?* Resistant to outliers.
**Common mistakes:** Filling missing values before the split; one-hot encoding a high-cardinality column like employee ID; numbering unordered categories.

### Q33 ⭐⭐ 🟡 How does a tree split differ when the target is categorical (classification) and when it is numeric (regression)?
**Asked at:** reported in anonymous candidate summaries for Tiger Analytics and Fractal data-scientist interviews (via search snippets, not opened; unverified); also in prep-site decision-tree banks.
**What the interviewer is checking:** Whether you know the splitting score changes from "purity" to "spread".
**Say this in the interview:** "Both look for the split that makes the two groups most uniform. For a category target the score is Gini or entropy, and each leaf predicts the majority class. For a number target the score is squared error, and each leaf predicts the average."
**Explain simply:**
- Classification tree (target: left or stayed): tries every cut, picks the one with the lowest weighted Gini or entropy (Q20, Q21). Leaf output = most common class (or class shares).
- Regression tree (target: monthly sales): tries every cut, picks the one with the lowest total squared error (sum of squared gaps from the group's average). Leaf output = the group average.
- The inputs can be numbers or categories in both cases; only the target type changes the score.
**Worked example (concept question):** Classification: a node with 10 stayers and 10 leavers has Gini 0.5. A split into (8 stayers, 2 leavers) and (2 stayers, 8 leavers) gives Gini 0.32 in both groups, so a weighted 0.32; purer, so it is a good split. Regression: six stores with sales 10, 12, 14, 30, 32, 34 lakh have average 22 and squared error 616. Splitting into {10, 12, 14} and {30, 32, 34} gives errors 8 and 8, total 16. The big drop (616 to 16) shows it is an excellent split (all computed by script).
**Alternative / pitfalls:** A regression tree's predictions are a staircase of averages, not a smooth line.
**Likely follow-ups:** 1) *What does a classification leaf return?* Majority class, and `predict_proba` gives the class shares. 2) *Can a regression tree extrapolate?* No (Q29).
**Common mistakes:** Saying regression trees use Gini; forgetting a leaf returns an average, not a class.

### Q34 ⭐⭐ 🟡 What is out-of-bag (OOB) score in a random forest, and how do you switch it on in sklearn?
**Asked at:** commonly asked (no company-specific report found); OOB appears in random-forest question banks (unverified).
**What the interviewer is checking:** Whether you know the forest can test itself on rows each tree never saw.
**Say this in the interview:** "Each tree is trained on a bootstrap sample, leaving out about 37% of rows. Those left-out rows act as a free test set for that tree. Averaging the predictions over the trees that did not see a row gives the OOB score. In sklearn you set oob_score=True and read oob_score_."
**Explain simply:**
- Each tree skips about 37% of rows (Q27). For each employee, only trees that did not train on that person vote on them.
- Compare those votes with the real answer: that is the out-of-bag accuracy, an honest estimate without a separate test set.
- Useful when data is small; still keep a proper test set for the final report.
- For classification, the default score is accuracy.
**Sample data:** The 1,000-row synthetic table `make_attrition(1000)` with `overtime_hours`, `tenure_years`, `salary_band` (750 train, 250 test rows, `random_state=42`).
**Code (what you write in the interview):**
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(oob_score=True, random_state=42)
model.fit(X_train, y_train)
print('OOB accuracy :', round(model.oob_score_, 3))
print('Test accuracy:', round(model.score(X_test, y_test), 3))
```
**Output:**
```text
OOB accuracy : 0.756
Test accuracy: 0.768
```
**What it means:** The OOB estimate (0.756) is close to the test score (0.768), so the two honest estimates agree. (The forest still scores near 100% on its own training rows, so do not quote that.) Accuracy alone is weak for rare outcomes, so also check recall (Q24).
**Alternative / pitfalls:** OOB needs `bootstrap=True` (the default) and enough trees so every row is left out at least once. It is not a replacement for cross-validation when tuning many settings.
**Likely follow-ups:** 1) *Does OOB need a validation set?* No. 2) *Why close to test accuracy?* Both are scored on rows the model did not train on.
**Common mistakes:** Forgetting `oob_score=True`; reading `oob_score_` on a fitted model that had no bootstrap; treating OOB as training accuracy.

### Q35 ⭐⭐ 🟡 Write short code that uses GridSearchCV to tune max_depth and n_estimators of a random forest.
Candidate values: max_depth in [3, 5, 8], n_estimators in [100, 300].
**Asked at:** commonly asked (no company-specific report found); hyperparameter tuning is a standard fresher ML question.
**What the interviewer is checking:** Whether you can write a clean grid search and choose a sensible score.
**Say this in the interview:** "I define the grid, run 5-fold cross-validation on the training data for each of the 6 combinations, pick the best by F1 because leavers are rare, and only then check the test set once."
**Explain simply:**
- Hyperparameters are settings you choose before training (tree depth, number of trees); the model does not learn them.
- GridSearchCV tries every combination (3 depths x 2 sizes = 6), splitting the training data into 5 parts each time (cross-validation) and averaging the scores. That is 30 fits (plus one final refit of the best combination on all training rows).
- `scoring='f1'` judges by F1, since accuracy misleads with rare leavers.
- The test set is used once at the end, never inside the search.
**Sample data:** The 1,000-row synthetic table `make_attrition(1000)` (750 train, 250 test rows, `random_state=42`).
**Code (what you write in the interview):**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

param_grid = {'max_depth': [3, 5, 8], 'n_estimators': [100, 300]}
search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring='f1')
search.fit(X_train, y_train)
print('Best settings:', search.best_params_)
print('Best CV F1   :', round(search.best_score_, 3))
print('Test F1      :', round(search.score(X_test, y_test), 3))
```
**Output:**
```text
Best settings: {'max_depth': 8, 'n_estimators': 100}
Best CV F1   : 0.424
Test F1      : 0.447
```
**What it means:** Depth 8 with 100 trees did best (cross-validated F1 0.424; test F1 0.447, so the model catches leavers only modestly). Report the test F1 once, with the caveat that small differences between combinations are noise. Outputs depend on the seed.
**Alternative / pitfalls:** `RandomizedSearchCV` samples combinations when the grid is large. The best value sitting at the edge of the grid (depth 8 is the largest) is a hint to try bigger values.
**Likely follow-ups:** 1) *Why cross-validation?* One split can be lucky. 2) *Does the grid search use the test set?* No.
**Common mistakes:** Tuning on the test set; using accuracy on imbalanced data; huge grids on tiny data.

### Q36 ⭐⭐ 🟡 What is the maximum number of leaves in a binary decision tree of depth 3, and why does a depth-10 tree on 500 rows nearly always overfit?
**Asked at:** commonly asked (no company-specific report found); overfitting of deep trees is central to every decision-tree question bank.
**What the interviewer is checking:** Whether you can reason about tree size and connect it to memorizing the data.
**Say this in the interview:** "Each level doubles the leaves, so depth 3 gives at most 2^3 = 8. Depth 10 allows up to 1,024 leaves, more than the 500 rows, so the tree can give nearly every row its own leaf and memorize noise."
**Explain simply:**
- Binary tree: each split makes 2 branches. Depth is the number of splits from the top to the bottom. Leaves at depth d = at most 2^d.
- Depth 3: 8 leaves. Depth 10: 1,024 leaves.
- With 500 rows and room for 1,024 leaves, the tree can carve out tiny groups (often 1 to 3 people) and "learn" random quirks, so it scores near-perfect on training but poorly on new data (overfitting).
**Sample data:** The 500-row synthetic table from Q3 (400 train, 100 test).
**Code (what you write in the interview):**
```python
from sklearn.tree import DecisionTreeClassifier

deep_tree = DecisionTreeClassifier(max_depth=10, random_state=42).fit(X_train, y_train)
print('Train accuracy:', round(deep_tree.score(X_train, y_train), 3))
print('Test accuracy :', round(deep_tree.score(X_test, y_test), 3))
print('Leaves:', deep_tree.get_n_leaves(), 'for', len(X_train), 'training rows')
```
**Output:**
```text
Train accuracy: 0.983
Test accuracy : 0.76
Leaves: 77 for 400 training rows
```
**What it means:** 77 leaves for 400 rows is about 5 people per leaf; train 98% vs test 76% shows the gap. The tree rarely uses all 1,024 slots, because a node stops when it is pure, but it still has plenty of room to memorize.
**Alternative / pitfalls:** "Nearly always" is a rule of thumb, not a law; on very clean data it may not overfit. Control it with `max_depth`, `min_samples_leaf` or pruning (Q40), or use a forest.
**Likely follow-ups:** 1) *How would you pick the depth?* Cross-validation. 2) *Max leaves of depth 4?* 16.
**Common mistakes:** Saying 2 x depth leaves; counting nodes instead of leaves; confusing depth with number of splits in total.

### Q37 ⭐ 🟡 At a high level, how does a random forest differ from gradient boosting?
**Asked at:** commonly asked (no company-specific report found); random forest vs other ensembles shows up in question banks and in Tiger Analytics/Fractal reported prompts on RF vs trees (unverified).
**What the interviewer is checking:** Whether you know "many independent trees averaged" vs "trees built one after another to fix errors".
**Say this in the interview:** "A random forest builds many deep trees in parallel on random samples and averages them to cut variance. Gradient boosting builds many small trees one after another, each correcting the previous trees' mistakes, which mainly cuts bias. Boosting is often more accurate but needs more careful tuning."
**Explain simply:**
- Random forest: trees are independent and similar in size; a vote or average gives the answer. Hard to break, few settings.
- Gradient boosting: each new small tree is trained on what the earlier trees got wrong. Learning rate and number of trees matter a lot.
- Forest = a committee that votes; boosting = a team where each member fixes the last one's errors.
- Boosting can overfit if left running too long; a forest is more forgiving.
**Alternative / pitfalls:** Neither is automatically better. For a first model on HR data, a forest is a safe baseline. Libraries like XGBoost and LightGBM implement boosting (from memory, unverified).
**Likely follow-ups:** 1) *Which is easier to tune?* Random forest. 2) *Which is easier to explain?* Neither; both are black boxes compared with one tree.
**Common mistakes:** Saying boosting trees run in parallel; saying forests reduce bias; calling boosting "always better".

### Q38 ⭐ 🟡 Should an HR attrition model use gender or age as input features? Discuss fairness and privacy for a tree-based model.
**Asked at:** commonly asked (no company-specific report found); a gap-fill judgement question for HR-analytics interviews.
**What the interviewer is checking:** Whether you think about fairness, law and proxies, not just accuracy.
**Say this in the interview:** "I would not use gender, and I would be very careful with age. They can create discrimination, and removing the column does not fully fix it because other columns can stand in for them. I would check the model's results across groups and involve HR and legal."
**Explain simply:**
- Protected attributes (gender, age, religion, disability, etc.) should generally not drive people decisions. Legal rules differ by country; confirm with legal or HR policy (from memory, not verified here).
- Proxies: a tree can recover gender or age from other columns, such as career gap, part-time flag, grade or tenure. Dropping the column is not enough.
- Check fairness by comparing outcomes by group: how many are flagged, and recall and precision for each group. Compare rates, not just overall accuracy.
- Privacy: collect only what you need, restrict access, anonymize for analysis, and tell people how data is used. Privacy laws such as India's DPDP Act or GDPR may apply; confirm details with IT or legal (from memory, unverified).
- Use scores to support conversations (for example, offering help), not to deny pay, promotion or hiring.
**Alternative / pitfalls:** If age or gender is kept only for auditing, keep it out of the model inputs and use it just to measure group differences afterward. Historical data can also carry past bias that the model learns.
**Likely follow-ups:** 1) *Is removing the column enough?* No, because of proxies. 2) *Who should review?* HR leadership and legal, before deployment.
**Common mistakes:** Saying "the model is objective"; dropping columns and declaring it fair; skipping group-level checks.

### Q39 ⭐ 🟡 Find the error in this workflow and say how it affects the reported result.
```python
rf = RandomForestClassifier().fit(X, y)
print('Accuracy:', rf.score(X, y))
```
**Asked at:** commonly asked (no company-specific report found); a gap-fill question, one of the classic first mistakes.
**What the interviewer is checking:** Whether you spot scoring on the same data used to train.
**Say this in the interview:** "The model is trained and scored on the same rows, so accuracy is inflated: it measures memory, not how well it predicts new employees. I would split first (stratified), fit on the training part, and report the test score."
**Explain simply:**
- A forest can memorize training rows, so the training score is near-perfect even when it knows little about new people.
- Also missing: `random_state` (results change on every run) and a baseline (always predicting stay).
- Fix: `train_test_split` with `stratify=y`, fit on training data, score on the test data (or use cross-validation).
**Sample data:** `make_attrition(1000)` with `overtime_hours`, `tenure_years`, `salary_band`; 750 train / 250 test rows, about 24% leavers.
**Code (what you write in the interview):**
```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(random_state=42).fit(X_train, y_train)
print('Train accuracy:', rf.score(X_train, y_train))
print('Test accuracy :', round(rf.score(X_test, y_test), 3))
print('Always-stay baseline', round(1 - y_test.mean(), 3))
```
**Output:**
```text
Train accuracy: 0.9933333333333333
Test accuracy : 0.768
Always-stay baseline 0.764
```
**What it means:** Training accuracy (0.993) overstates the model. The honest figure is 0.768, barely above the 0.764 you get by predicting "stay" for everyone. Report test accuracy with recall for leavers.
**Alternative / pitfalls:** For a small dataset use cross-validation. Do any scaling or filling after the split, using training data only.
**Likely follow-ups:** 1) *Why not report training accuracy?* It rewards memorizing. 2) *What is a test set?* Rows hidden from the model until the final check.
**Common mistakes:** Reporting training accuracy; tuning on the test set; no stratify on imbalanced data.

### Q40 ⭐ 🟡 What is cost-complexity pruning (ccp_alpha) in a decision tree, and how does it differ from setting max_depth?
**Asked at:** commonly asked (no company-specific report found); pruning appears in decision-tree question banks (unverified).
**What the interviewer is checking:** Whether you know pruning trims after growing, based on benefit per leaf, while max_depth stops growth early.
**Say this in the interview:** "Cost-complexity pruning grows the tree and then removes the branches that add the least accuracy per leaf; a bigger ccp_alpha prunes more. max_depth just caps the number of levels in advance, whether or not a branch is useful."
**Explain simply:**
- Overfit trees have branches that only memorize noise. Pruning cuts those.
- `ccp_alpha` is a penalty for each extra leaf. At 0, nothing is pruned. As it grows, weak branches are cut, leaving a smaller tree.
- `max_depth` limits levels everywhere equally; a useful deep branch is cut while a useless shallow one stays.
- Choose `ccp_alpha` by cross-validation (`cost_complexity_pruning_path` lists candidate values).
**Sample data:** `make_attrition(1000)` with `overtime_hours`, `tenure_years`, `salary_band`; 750 train / 250 test rows (`random_state=42`); a `DecisionTreeClassifier(ccp_alpha=..., random_state=42)` for each value. Computed:

| ccp_alpha | Leaves | Train accuracy | Test accuracy |
|---|---|---|---|
| 0 | 218 | 0.993 | 0.716 |
| 0.002 | 45 | 0.883 | 0.748 |
| 0.005 | 6 | 0.799 | 0.808 |
| 0.01 | 3 | 0.781 | 0.800 |
| 0.02 | 2 | 0.761 | 0.764 |

**What it means:** The unpruned tree has 218 leaves and test accuracy 0.716. Pruning with 0.005 cuts it to 6 leaves and raises test accuracy to 0.808; 0.02 prunes too much (2 leaves, 0.764). A `max_depth=3` tree on the same data scores 0.808 with 8 leaves. Both help; pruning is guided by how much each branch is worth. (One split of the data, so differences of a few points are noise.)
**Alternative / pitfalls:** Too large an alpha leaves a tree too simple. You can combine the two controls. Tune on training data with cross-validation, not the test set.
**Likely follow-ups:** 1) *Pre-pruning vs post-pruning?* Pre = stop early (max_depth, min_samples_leaf); post = grow then cut (ccp_alpha). 2) *What does alpha=0 mean?* No pruning.
**Common mistakes:** Thinking higher alpha grows a bigger tree; picking alpha using the test set.

### Q41 ⭐ 🟡 Why can two decision trees trained on slightly different samples of the same data look very different, and why does that matter when you explain a tree to leaders?
**Asked at:** commonly asked (no company-specific report found); single-tree high variance is a standard topic in random-forest question banks (unverified).
**What the interviewer is checking:** Whether you understand tree instability (high variance) and its communication risk.
**Say this in the interview:** "A small change in the data can change the best first split, and everything below it changes too, so trees are unstable. So I would never present one tree as 'the' rule; I would say it is one reasonable picture and show it is consistent with other checks."
**Explain simply:**
- A tree picks the best split greedily at each step. If two cut-offs are almost equally good, a few different rows tip the choice, and the branches below change.
- That is high variance: the model changes a lot when the data changes a little.
- For leaders: a tree looks like a crisp rulebook ("overtime above 28 hours leads to exit"), but the 28 could easily be 25 or 31 with a slightly different sample.
- Use trees to show broad patterns and communicate uncertainty; use a forest or other checks for stable results.
**Worked example (concept question):** I took 150 employees (`make_attrition(150)`, the Q3 generator) and resampled them three times with replacement (seeds 1, 2, 3), fitting a tree with `max_depth=2` on each.
```python
from sklearn.tree import DecisionTreeClassifier

features = ['overtime_hours', 'tenure_years', 'salary_band']
for seed in (1, 2, 3):
    sample = employees.sample(len(employees), replace=True, random_state=seed)
    tree = DecisionTreeClassifier(max_depth=2, random_state=42).fit(sample[features], sample['left'])
    used = [features[i] for i in tree.tree_.feature if i >= 0]  # -2 marks a leaf
    print(f"Sample {seed} | splits used: {used} | first cut-off: {tree.tree_.threshold[0]}")
```
```text
Sample 1 | splits used: ['overtime_hours', 'tenure_years', 'tenure_years'] | first cut-off: 28.5
Sample 2 | splits used: ['overtime_hours', 'tenure_years', 'tenure_years'] | first cut-off: 28.5
Sample 3 | splits used: ['overtime_hours', 'tenure_years', 'tenure_years'] | first cut-off: 30.5
```
The top feature stayed the same here and the first cut-off moved only a little (28.5 to 30.5 hours); the exact tenure cut-offs in the lower branches differ between samples. With noisier data or a deeper tree the changes are larger, so treat every number in a single tree as approximate.
**Alternative / pitfalls:** Averaging many trees (a forest) reduces this instability (Q42). Quote cut-offs as approximate ("roughly 20 to 30 hours").
**Likely follow-ups:** 1) *How do you reduce it?* Bagging or a forest, or limit depth. 2) *Is the tree then wrong?* Not wrong, just not unique.
**Common mistakes:** Presenting exact thresholds as facts; reading causes into a single tree.

### Q42 ⭐ 🔴 Why does averaging many trees reduce variance only if the trees are not too correlated, and how do random feature subsets help?
**Asked at:** commonly asked (no company-specific report found); feature subsets in random forests are in question banks and reported RF prompts (unverified).
**What the interviewer is checking:** Whether you know the intuition behind "averaging helps when errors differ".
**Say this in the interview:** "If trees make the same mistakes, averaging them just repeats the same mistake. Their errors cancel only when they differ. A random forest makes trees differ by giving each split a random subset of the columns, which lowers the correlation between trees and so the variance of the average."
**Explain simply:**
- Averaging many noisy guesses cancels the noise only if the noise is independent. If every guess shares the same error, the average keeps it.
- Without feature subsets, bagged trees all choose the strong column (overtime) at the top, so they look alike (highly correlated).
- With `max_features` (for example the square root of the column count for classification), each split sees only some columns, so different trees use different ones and their errors are less alike.
- Trade-off: each tree is slightly weaker, but the average is better.
**Worked example (concept question):** The variance of the average of B trees, each with variance 1 and pairwise correlation rho, is rho x 1 + (1 - rho) x 1/B (standard formula, computed for B = 100):

| Correlation rho | Variance of the average |
|---|---|
| 0 | 0.010 |
| 0.3 | 0.307 |
| 0.8 | 0.802 |
| 1 | 1.000 |

With correlation 0.8, 100 trees barely help (0.80); at 0.3 the floor is about 0.30. More trees help only until the correlation floor is reached; lowering rho is what matters.
**Alternative / pitfalls:** Too small a `max_features` makes weak trees; tune it by cross-validation. Adding more trees never hurts accuracy much, but it also does not help beyond the floor.
**Likely follow-ups:** 1) *Does bagging alone reduce correlation?* Only a little; rows differ, but the same strong columns win. 2) *Default max_features for classification?* sqrt of the number of columns (sklearn default, verified on 1.9.1).
**Common mistakes:** Believing more trees always fixes overfitting; thinking random columns make each tree better (they make trees more different).

### Q43 ⭐ 🔴 Your random forest has 99% train and 80% test accuracy. HR wants to use it to decide which individual employees get retention offers. How do you validate it and what do you caution them about?
**Asked at:** commonly asked (no company-specific report found); a gap-fill scenario combining validation and responsible use.
**What the interviewer is checking:** Whether you read the train/test gap, validate beyond accuracy, and push back on using a model for individual decisions.
**Say this in the interview:** "A 99% vs 80% gap means it memorizes training data, and 80% may barely beat predicting 'stay' for everyone. I would use stratified cross-validation, look at recall and precision for leavers and at a time-based test, check fairness by group, and tell HR the scores rank groups by risk and are not certain for any one person."
**Explain simply:**
- Overfitting: 99% train vs 80% test means it learned noise. Reduce with `min_samples_leaf`, depth limits, fewer features, and tuning by cross-validation.
- Validate: (1) baseline: compare with always predicting stay (about 76% here); (2) stratified cross-validation, not one lucky split; (3) recall, precision and a top-20% lift table, not accuracy; (4) a time-based test (train on earlier months, test on later) and a check for leaking columns (Q31); (5) fairness by group (Q38).
- Caution HR: it is a risk ranking, not a verdict. A flagged person may not leave, and an unflagged person may. Use it to prioritise conversations and support, not to cut pay or opportunities, and keep a human in the loop. Check data-protection rules with IT or legal (from memory, unverified).
- Offers have a cost: at 44% precision in the top 20% (below), 56% of offers go to people who would have stayed.
**Sample data:** `make_attrition(1000)` with `overtime_hours`, `tenure_years`, `salary_band` as `X` and `left` as `y`; 750 train / 250 test rows (`test_size=0.25, random_state=42`); about 24% leavers.
**Code (what you write in the interview):**
```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

rf = RandomForestClassifier(random_state=42)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
print('CV recall:', cross_val_score(rf, X, y, cv=cv, scoring='recall').round(2))

rf.fit(X_train, y_train)
probs = rf.predict_proba(X_test)[:, 1]
top_20 = probs >= np.percentile(probs, 80)
print('train', round(rf.score(X_train, y_train), 3), 'test', round(rf.score(X_test, y_test), 3))
print('share of top 20% who left:', round(y_test[top_20].mean(), 2), '| overall leave rate:', round(y_test.mean(), 2))
```
**Output:**
```text
CV recall: [0.4  0.42 0.35 0.3  0.38]
train 0.993 test 0.768
share of top 20% who left: 0.44 | overall leave rate: 0.24
```
**What it means:** The model finds only 30 to 42% of leavers across folds, so it misses most of them. Its ranking is still useful: the top 20% flagged group leaves at 44% against 24% overall (about 1.9 times the base rate). The honest message to HR is "good for prioritising groups, not reliable for individual decisions". (Numbers are from synthetic data; the 99% train score in the question is an exercise value.)
**Alternative / pitfalls:** Calibrate probabilities before using them as risk percentages, set the cut-off by HR capacity and the cost of an offer, and re-validate regularly as the workforce changes.
**Likely follow-ups:** 1) *Would you deploy it?* As decision support for planning, with monitoring, not for individual penalties. 2) *How would you measure impact?* A pilot with a control group.
**Common mistakes:** Trusting accuracy; deploying without a baseline; using risk scores for punitive decisions; ignoring fairness checks.

