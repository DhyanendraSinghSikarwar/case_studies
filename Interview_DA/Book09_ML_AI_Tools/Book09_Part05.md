# Book 9 — Basic ML + AI Tools for Analysts | Part 5: Model Evaluation (Accuracy, Precision, Recall, Confusion Matrix, RMSE) 🟡

**Target:** 80 questions | **Actual:** 87 questions
**Scope:** accuracy, precision, recall, F1, confusion matrix, thresholds and class imbalance, RMSE/MAE/MAPE, reading sklearn and statsmodels evaluation output, and explaining model quality to non-technical stakeholders.

### Q1 ⭐⭐⭐ 🟢 What is a confusion matrix, and what do the four cells TP, FP, FN and TN mean for a binary classification model?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 How is accuracy defined, and how do you calculate it from a confusion matrix?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is precision, in plain words, and what is its formula?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What is recall (also called sensitivity), in plain words, and what is its formula?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 Explain the difference between precision and recall to a non-technical HR manager using an employee attrition model as the example.
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 Why can accuracy be a misleading metric, especially when one class is rare?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 A model for fraud detection gives you a confusion matrix. Explain its components and how you would choose between optimising precision or recall.
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 What do sensitivity and specificity mean, and how do they relate to recall and the confusion matrix?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟢 What is RMSE, and why is it easier to explain to a business user than MSE?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟢 An attrition model flags employees who may resign. Would you prioritise precision or recall, and why?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟢 What is the F1 score, and when would you report it instead of accuracy?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟢 How do you decide whether to use classification metrics (accuracy, precision, recall) or regression metrics (RMSE, MAE) for a problem?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟢 Accuracy calculation: using the confusion matrix below, what is the accuracy of the model?
TP = 40, FP = 10, FN = 20, TN = 130
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟢 A model predicts that no employee will leave. Of 1,000 employees, 950 stay and 50 leave. What are the accuracy and the recall for the 'leaves' class, and what does this tell you?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Precision calculation: an attrition model produced the matrix below. What is its precision for the 'leaves' class, and what does that figure mean for the HR team acting on the flags?
TP = 24, FP = 16, FN = 6, TN = 154
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 Recall calculation: of 60 employees who actually resigned, the model flagged 45 of them. It also flagged 30 employees who stayed. What is the recall, and what is the precision?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 F1 calculation: a model has precision 0.80 and recall 0.50. What is its F1 score, and why is it lower than the simple average of the two?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 RMSE calculation: compute the RMSE from the five predictions below.
Actual monthly sales (lakh): 100, 120, 90, 110, 130
Predicted: 110, 115, 100, 100, 120
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🟡 MAE calculation: using the same five predictions below, what is the MAE, and how would you say it to a sales head?
Actual monthly sales (lakh): 100, 120, 90, 110, 130
Predicted: 110, 115, 100, 100, 120
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐⭐ 🟡 What is the difference between RMSE and MAE, and when would you report each?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐⭐ 🟡 Code reading: what confusion matrix does this code print, and what are the precision and recall?
```python
from sklearn.metrics import confusion_matrix
y_true = [1,0,1,1,0,0,1,0,0,0]
y_pred = [1,0,0,1,0,1,1,0,0,0]
print(confusion_matrix(y_true, y_pred))
```
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐⭐ 🟡 Accuracy paradox: a card-fraud model is tested on 10,000 transactions of which 100 are fraud. It flags 150 transactions, 60 of them truly fraud. Calculate accuracy, precision and recall, and say whether you would call this model good.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐⭐ 🟡 How does lowering the classification threshold from 0.5 to 0.3 change the number of false positives, false negatives, precision and recall?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐⭐ 🟡 Your manager asks 'how accurate is the churn model?' How do you answer in a way that is honest and useful, rather than quoting one accuracy number?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐⭐ 🟡 Cost-based choice: a missed leaver (FN) costs about Rs 50,000 in replacement; a wasted retention call (FP) costs Rs 2,000. Using the counts below, which model has the lower total error cost, and by how much?
Model A: FN = 10, FP = 40
Model B: FN = 20, FP = 10
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐⭐ 🟡 Code reading: in scikit-learn, in what order does confusion_matrix(y_true, y_pred).ravel() return its four values, and how would you unpack them to compute recall?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐⭐ 🟡 Two analysts report 'model accuracy' for the same attrition data and get 0.92 and 0.81. Name three reasons the numbers might differ legitimately.
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟢 What is specificity (true negative rate), and how is it calculated from a confusion matrix?
TP = 30, FN = 20, TN = 180, FP = 20
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟢 What is the false positive rate, and why does a screening team care about it?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟢 What is MAE (mean absolute error), and what are its units?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟢 What is MSE, and why do we square the errors instead of just averaging them?
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟢 What is a baseline model, and why should you compare a new model against one before reporting its metric?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟢 What is the difference between a false positive and a false negative? Give one example each from a hiring-screening model.
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟢 What does a residual mean in a regression model, and how is it linked to RMSE?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟢 What is the difference between precision and accuracy in model evaluation (not in measurement)?
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟢 What does an ROC curve show, and what do AUC values of 0.5 and 1.0 mean?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟢 Which single metric would you not report alone for a rare-event model, and what would you add to it?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟢 What does 'test-set performance' mean, and why do we report metrics on it rather than on training data?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟢 What is the difference between a metric (like recall) and a loss function used when a model is trained?
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟢 If a regression model's RMSE is 8 and the target is monthly salary in thousands of rupees, how do you read it?
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 Hiring screen: a resume-screening model shortlists 50 of 500 applicants; 30 shortlisted are actually suitable, and 60 suitable applicants exist in total. What are its precision and recall?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 Threshold calculation: using the scores below, compute precision and recall at a threshold of 0.5 and again at 0.3.
Scores: 0.90, 0.70, 0.55, 0.40, 0.35, 0.10
Actual (1 = leaves): 1, 1, 0, 1, 0, 0
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 Outliers: the errors of a sales model on five months are shown below. Compute MAE and RMSE and explain why they differ.
Absolute errors: 2, 2, 2, 2, 12
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 Baseline vs model: compute the RMSE of the model and of a baseline that always predicts the mean of the actuals. Is the model worthwhile?
Actual: 10, 20, 30, 40
Model predictions: 12, 18, 33, 38
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 Precision at top K: HR can only call 20 employees. The model's top 20 contains 14 actual leavers, and 40 employees leave in total. What are precision@20 and recall@20?
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 Model comparison: Model A has precision 0.30 and recall 0.90; Model B has precision 0.80 and recall 0.60. Which would you choose for a retention campaign with a small budget, and which if the company can afford to call everyone at risk?
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟡 Multi-class reading: given the confusion matrix below (rows = actual, columns = predicted), what is the overall accuracy and the precision for class B?
Classes A, B, C
Row A: 50, 5, 5
Row B: 10, 30, 10
Row C: 0, 10, 40
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟡 What is the difference between macro-averaged and weighted-averaged recall in a classification report, and which would you use for an imbalanced set of ticket categories?
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🟡 Code reading: what does this print, and what is wrong with the idea of using it as the only evaluation?
```python
from sklearn.metrics import accuracy_score
import numpy as np
y_true = np.array([0,0,0,0,0,0,0,0,1,1])
y_pred = np.zeros(10)
print(accuracy_score(y_true, y_pred))
```
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🟡 Code task: write short code that applies a 0.3 threshold to model.predict_proba(X_test)[:, 1] and prints the confusion matrix and recall.
<!-- ANSWER_PENDING -->

### Q51 ⭐⭐ 🟡 Code task: use sklearn to report RMSE and MAE for y_test and y_pred, and say which function names you would use in a recent scikit-learn version.
<!-- ANSWER_PENDING -->

### Q52 ⭐⭐ 🟡 Code reading: what does cross_val_score(model, X, y, cv=5, scoring='recall') return, and why choose recall as the scoring?
<!-- ANSWER_PENDING -->

### Q53 ⭐⭐ 🟡 MAPE calculation: compute the MAPE for the four predictions below and say when MAPE becomes unreliable.
Actual: 200, 100, 50, 400
Predicted: 180, 110, 60, 380
<!-- ANSWER_PENDING -->

### Q54 ⭐⭐ 🟡 What is k-fold cross-validation, and why does it give a steadier estimate of a metric than a single train/test split?
<!-- ANSWER_PENDING -->

### Q55 ⭐⭐ 🟡 A model has R-squared 0.90 but its RMSE is Rs 40,000 on salaries that range from Rs 30,000 to Rs 60,000. How do you explain this to a manager, and what do you report?
<!-- ANSWER_PENDING -->

### Q56 ⭐⭐ 🟡 What is the precision-recall trade-off, and what do you do when HR wants both to be high?
<!-- ANSWER_PENDING -->

### Q57 ⭐⭐ 🟡 Always-positive model: 10% of customers churn, and a model flags every customer as a churner. What are its recall, precision and F1?
<!-- ANSWER_PENDING -->

### Q58 ⭐⭐ 🟡 A random guesser flags employees as 'will leave' with probability 0.2 in a dataset where 20% really leave. What precision and recall do you expect, and why does this matter as a benchmark?
<!-- ANSWER_PENDING -->

### Q59 ⭐⭐ 🟡 Your test set has only 20 rows and accuracy is 85%. Why should you be cautious, and what would you do?
<!-- ANSWER_PENDING -->

### Q60 ⭐⭐ 🟡 Code reading: how do you build a confusion matrix from two pandas columns with pd.crosstab, and what do the rows and columns represent?
<!-- ANSWER_PENDING -->

### Q61 ⭐⭐ 🟡 How would you read a scikit-learn classification_report for a three-class model, and which columns would you look at first?
<!-- ANSWER_PENDING -->

### Q62 ⭐⭐ 🟡 Code reading: a statsmodels OLS result is used as below. What does this measure, and why is it optimistic as a report of model quality?
```python
import numpy as np, statsmodels.api as sm
model = sm.OLS(y, sm.add_constant(X)).fit()
rmse = np.sqrt(np.mean(model.resid ** 2))
```
<!-- ANSWER_PENDING -->

### Q63 ⭐⭐ 🟡 What is the difference between in-sample RMSE and out-of-sample RMSE, and which one do you give to a stakeholder?
<!-- ANSWER_PENDING -->

### Q64 ⭐⭐ 🟡 Which regression metric would you pick when over-predicting and under-predicting inventory carry very different costs, and how would you handle that?
<!-- ANSWER_PENDING -->

### Q65 ⭐⭐ 🔴 Macro recall: using the 3-class matrix below (rows = actual), calculate the macro-averaged recall.
Row A: 50, 5, 5
Row B: 10, 30, 10
Row C: 0, 10, 40
<!-- ANSWER_PENDING -->

### Q66 ⭐⭐ 🔴 Your attrition model shows 96% recall on the test set, which is far above anything in the earlier versions. What would you suspect, and what would you check before reporting it?
<!-- ANSWER_PENDING -->

### Q67 ⭐⭐ 🔴 A model's recall is 60% overall, but 80% for men and 40% for women in the test data. How do you investigate and report this, and what are the risks of acting on the model?
<!-- ANSWER_PENDING -->

### Q68 ⭐ 🟢 What is a lift or gain chart, and how does it help an HR or marketing team decide how many people to contact?
<!-- ANSWER_PENDING -->

### Q69 ⭐ 🟢 What is Cohen's kappa in plain words, and why might it be used when labels are imbalanced?
<!-- ANSWER_PENDING -->

### Q70 ⭐ 🟡 Lift calculation: of 1,000 employees, 100 leave. The top decile of model scores (100 people) contains 35 leavers. What is the lift for that decile?
<!-- ANSWER_PENDING -->

### Q71 ⭐ 🟡 Why can ROC-AUC look flattering on a heavily imbalanced problem, and what would you look at instead?
<!-- ANSWER_PENDING -->

### Q72 ⭐ 🟡 What is the Matthews correlation coefficient (MCC), and why do some practitioners prefer it to F1?
<!-- ANSWER_PENDING -->

### Q73 ⭐ 🟡 What is log loss (cross-entropy), and how does it differ from accuracy as a metric?
<!-- ANSWER_PENDING -->

### Q74 ⭐ 🟡 What is calibration of predicted probabilities, and why does it matter if HR will use a '70% risk' number?
<!-- ANSWER_PENDING -->

### Q75 ⭐ 🟡 What is adjusted R-squared, and why would it be preferred to R-squared when comparing models with different numbers of features?
<!-- ANSWER_PENDING -->

### Q76 ⭐ 🟡 Why is MAE minimised by the median and RMSE by the mean, and does that matter to an analyst?
<!-- ANSWER_PENDING -->

### Q77 ⭐ 🟡 You use ChatGPT or Claude to tag 1,000 survey comments as positive, neutral or negative. How would you evaluate how good the tagging is using a human-labelled sample of 100?
<!-- ANSWER_PENDING -->

### Q78 ⭐ 🟡 Employee data contains personal details. What do you have to consider before using a real employee confusion matrix or predictions in a public tool or an AI assistant?
<!-- ANSWER_PENDING -->

### Q79 ⭐ 🟡 When would you choose PR-AUC over ROC-AUC, and how do you explain the choice in one sentence?
<!-- ANSWER_PENDING -->

### Q80 ⭐ 🟡 Which metrics would you show on a single slide for a non-technical audience about a churn model, and which would you keep in an appendix?
<!-- ANSWER_PENDING -->

### Q81 ⭐ 🟡 A classifier needs to hit at least 90% precision for a fraud team. How would you choose the threshold, and what happens to recall?
<!-- ANSWER_PENDING -->

### Q82 ⭐ 🟡 Does a change of random_state in train_test_split change your precision and recall? What would you do about the instability?
<!-- ANSWER_PENDING -->

### Q83 ⭐ 🔴 Your model beats the baseline in offline recall, but the retention campaign it supports shows no change in resignations. Give possible reasons and how you would investigate.
<!-- ANSWER_PENDING -->

### Q84 ⭐ 🔴 Explain data leakage using an attrition model that includes the column 'exit_interview_done'. How would it affect the evaluation metrics?
<!-- ANSWER_PENDING -->

### Q85 ⭐ 🔴 What is the difference between a model that predicts well and one that explains why employees leave, and how does that change the metrics you report?
<!-- ANSWER_PENDING -->

### Q86 ⭐ 🔴 How would you evaluate a model whose classes are heavily imbalanced and where only about 20 positive cases exist in the test set?
<!-- ANSWER_PENDING -->

### Q87 ⭐ 🔴 How would you choose between two models with similar recall when one is a logistic regression and the other a random forest, given your audience is HR?
<!-- ANSWER_PENDING -->
