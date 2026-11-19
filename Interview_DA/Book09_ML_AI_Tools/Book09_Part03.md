# Book 9 — Basic ML + AI Tools for Analysts | Part 3: Decision Trees, Random Forest (Intuition) 🟡

**Target:** 38 questions | **Actual:** 43 questions
**Scope:** decision-tree and random-forest intuition for analysts: splits, Gini and entropy, overfitting controls, bagging, feature importance, short sklearn code, and explaining tree models to managers.

### Q1 ⭐⭐⭐ 🟢 What is a decision tree, and how would you explain one to a non-technical HR manager using an employee attrition example?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 In a decision tree, what are the root node, a decision (internal) node, a leaf node, and the depth of the tree?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is a random forest, and how is it different from a single decision tree?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 A node in an attrition tree holds 10 employees: 6 stayed and 4 left. Calculate its Gini impurity.
Gini = 1 minus the sum of squared class proportions.
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 How does a decision tree decide where to split the data at each node?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Why do decision trees overfit easily, and which sklearn settings (max_depth, min_samples_leaf) would you use to control it?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Calculate the weighted Gini impurity after this split and the Gini gain, for an attrition tree split on overtime.
Parent node: 10 employees, 5 left and 5 stayed.
Overtime = Yes: 6 employees (4 left, 2 stayed). Overtime = No: 4 employees (1 left, 3 stayed).
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 You run the code below. What does the output tell you, and what would you try next?
```python
tree = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
print(tree.score(X_train, y_train), tree.score(X_test, y_test))
# output: 1.0 0.71
```
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Using the table, which max_depth would you pick for an attrition tree, and why?
| max_depth | Train accuracy | Test accuracy |
|---|---|---|
| 2 | 0.78 | 0.76 |
| 4 | 0.85 | 0.82 |
| 6 | 0.93 | 0.81 |
| 10 | 0.99 | 0.74 |
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 How does a random forest reduce overfitting compared with one deep decision tree? Mention bootstrap samples and random feature subsets.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 How do you get feature importance from a fitted RandomForestClassifier in sklearn, and how would you present the top three features to a manager?
```python
rf = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)
```
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 For an attrition-prediction task, when would you choose a single decision tree over a random forest, and when the reverse?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐ 🟢 Calculate the entropy (base 2) of a node with 5 leavers and 5 stayers, and of a node with 8 stayers and 0 leavers. What do the two values mean?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟢 Do decision trees and random forests need feature scaling? Do they need categorical columns to be encoded in sklearn?
<!-- ANSWER_PENDING -->

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
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 Write short sklearn code to split an attrition dataset, fit a RandomForestClassifier and print test accuracy.
Assume `X` (features, all numeric) and `y` (1 = left, 0 = stayed) already exist.
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 What do the n_estimators and max_depth parameters of RandomForestClassifier control?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 Five trees in a random forest predict leave, stay, leave, leave, stay for one employee. What does the forest predict by majority vote? If the five trees give leave probabilities 0.8, 0.3, 0.6, 0.7, 0.2, what is the averaged probability?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 A manager says a random forest is a black box and refuses to trust it. What do you say?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Compare two candidate splits using weighted Gini impurity. Which one would the tree choose?
Parent node: 10 employees, 5 left and 5 stayed.
Split A (overtime): Yes = 6 (4 left, 2 stayed), No = 4 (1 left, 3 stayed).
Split B (tenure < 2 years): Yes = 5 (4 left, 1 stayed), No = 5 (1 left, 4 stayed).
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Calculate the information gain (entropy-based) of this split.
Parent: 8 employees, 4 left and 4 stayed.
Left child: 4 employees (3 left, 1 stayed). Right child: 4 employees (1 left, 3 stayed).
Use log2(0.75) = -0.415 and log2(0.25) = -2.
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 A regression tree predicts monthly store sales. Calculate the total squared error before and after splitting the six stores into {10, 12, 14} and {30, 32, 34} (sales in lakh rupees).
Stores: 10, 12, 14, 30, 32, 34. Predict each group by its mean.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 What is the difference between Gini impurity and entropy, and which one is the sklearn default?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 An attrition dataset has 950 stayers and 50 leavers. A tree that always predicts stay is 95% accurate. Why is this a problem, and how can you handle imbalance in a tree or forest?
Mention class_weight='balanced' and what you would measure instead of accuracy.
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Interpret the importance table, and say what it does not prove.
| Feature | Importance |
|---|---|
| overtime_hours | 0.42 |
| tenure_years | 0.31 |
| salary_band | 0.17 |
| department | 0.10 |
(Values from a fitted RandomForestClassifier; they sum to 1.)
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 What are the weaknesses of impurity-based feature importance, and what is permutation importance?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 What are a bootstrap sample and bagging? Roughly what fraction of rows is left out of each bootstrap sample when the dataset is large?
Hint: the chance a given row is never picked in n draws with replacement is (1 - 1/n)^n, which approaches 0.368 as n grows.
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 What does predict_proba return for a random forest, and how would you use it to list the 20% of employees most at risk of leaving?
```python
probs = rf.predict_proba(X_test)[:, 1]
```
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 A sales model is trained on stores whose monthly sales were between 50 and 100 lakh. A regression tree and a linear regression are asked to predict a store expected at 150 lakh. How do their predictions behave, and why?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 A node has 9 employees and you set min_samples_leaf=5. Can it split? What if it has 12 employees?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 What is data leakage in a tree-based attrition model? Give two examples of columns that would leak.
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you prepare categorical columns and missing values before fitting a tree in sklearn? Show a short pandas example.
```python
df = pd.read_csv('hr.csv')  # columns include department (text), salary_band (text), tenure_years (some NaN)
```
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 How does a tree split differ when the target is categorical (classification) and when it is numeric (regression)?
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 What is out-of-bag (OOB) score in a random forest, and how do you switch it on in sklearn?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 Write short code that uses GridSearchCV to tune max_depth and n_estimators of a random forest.
Candidate values: max_depth in [3, 5, 8], n_estimators in [100, 300].
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 What is the maximum number of leaves in a binary decision tree of depth 3, and why does a depth-10 tree on 500 rows nearly always overfit?
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 At a high level, how does a random forest differ from gradient boosting?
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 Should an HR attrition model use gender or age as input features? Discuss fairness and privacy for a tree-based model.
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 Find the error in this workflow and say how it affects the reported result.
```python
rf = RandomForestClassifier().fit(X, y)
print('Accuracy:', rf.score(X, y))
```
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 What is cost-complexity pruning (ccp_alpha) in a decision tree, and how does it differ from setting max_depth?
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🟡 Why can two decision trees trained on slightly different samples of the same data look very different, and why does that matter when you explain a tree to leaders?
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Why does averaging many trees reduce variance only if the trees are not too correlated, and how do random feature subsets help?
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 Your random forest has 99% train and 80% test accuracy. HR wants to use it to decide which individual employees get retention offers. How do you validate it and what do you caution them about?
<!-- ANSWER_PENDING -->
