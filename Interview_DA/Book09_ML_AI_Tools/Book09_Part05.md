# Book 9 — Basic ML + AI Tools for Analysts | Part 5: Model Evaluation (Accuracy, Precision, Recall, Confusion Matrix, RMSE) 🟡

**Target:** 80 questions | **Actual:** 87 questions
**Scope:** accuracy, precision, recall, F1, confusion matrix, thresholds and class imbalance, RMSE/MAE/MAPE, reading sklearn and statsmodels evaluation output, and explaining model quality to non-technical stakeholders.

### Q1 ⭐⭐⭐ 🟢 What is a confusion matrix, and what do the four cells TP, FP, FN and TN mean for a binary classification model?
**Asked at:** commonly asked (no company-specific report found); confusion-matrix questions top every fresher model-evaluation list (prep-site lists seen as search snippets, unverified).
**What the interviewer is checking:** That you can name the four outcomes and say what each means in a real situation.
**Say this in the interview:** "A confusion matrix is a 2 by 2 table that compares what the model predicted with what really happened. It counts the model's right calls and its two kinds of wrong calls, so I can see the type of mistake and not only how many."
**Explain simply:**
- A **binary classification model** predicts one of two answers, for example "will leave" (positive) or "will stay" (negative). The "positive" class is simply the one you are hunting for.
- **TP (true positive):** model said "leaves", employee did leave. Correct.
- **TN (true negative):** model said "stays", employee stayed. Correct.
- **FP (false positive):** model said "leaves", employee stayed. A false alarm.
- **FN (false negative):** model said "stays", employee left. A miss.
- Every other metric (accuracy, precision, recall) is built from these four counts.
**Worked example (concept questions):** 200 employees, attrition model: TP = 24, FP = 16, FN = 6, TN = 154 (24 + 16 + 6 + 154 = 200).

| | Predicted leaves | Predicted stays |
|---|---|---|
| **Actually left** | TP = 24 | FN = 6 |
| **Actually stayed** | FP = 16 | TN = 154 |

**Alternative / pitfalls:** Layouts differ between books and tools. sklearn puts "actual" in rows and "predicted" in columns, with the negative class first. Always read the labels before reading the numbers.
**Likely follow-ups:** 1) *Which mistake is worse?* Depends on cost: a missed leaver and a wasted call cost different amounts (see Q10). 2) *Can you have it for more than two classes?* Yes, it becomes a bigger square (Q47 style).
**Common mistakes:** Mixing up FP and FN; forgetting that "positive" means the class you care about, not "good news"; reading rows and columns the wrong way round.

### Q2 ⭐⭐⭐ 🟢 How is accuracy defined, and how do you calculate it from a confusion matrix?
**Asked at:** commonly asked (no company-specific report found); a Tiger Analytics first-round report mentions accuracy, precision and recall fundamentals (anonymous candidate report seen as a snippet, unverified).
**What the interviewer is checking:** That you know the formula and also that you know it is only a starting point.
**Say this in the interview:** "Accuracy is the share of all predictions that were correct: right calls divided by all calls. From the confusion matrix it is (TP + TN) divided by the total of all four cells."
**Explain simply:**
- Accuracy = (TP + TN) / (TP + TN + FP + FN).
- It answers "out of everyone, how often was the model right?" in one number between 0 and 1 (or 0% to 100%).
- It treats a false alarm and a miss as equally bad, which is often not true in business.
**Worked example (concept questions):** Using the attrition matrix from Q1 (TP 24, TN 154, FP 16, FN 6): (24 + 154) / 200 = 178 / 200 = 0.89, so 89% of the 200 calls were right.
**Alternative / pitfalls:** 89% sounds great, but a model that says "everyone stays" would score (154 + 16) / 200 = 85% here with zero leavers found. Always compare against that kind of baseline (Q6, Q32).
**Likely follow-ups:** 1) *Is accuracy enough?* No, add recall and precision. 2) *What is error rate?* 1 minus accuracy.
**Common mistakes:** Dividing by only the positives; quoting accuracy alone on imbalanced data; mixing up accuracy with precision.

### Q3 ⭐⭐⭐ 🟢 What is precision, in plain words, and what is its formula?
**Asked at:** commonly asked (no company-specific report found); precision and recall appear in nearly every prep-site evaluation list (unverified).
**What the interviewer is checking:** Whether you can explain precision as "how trustworthy are the flags".
**Say this in the interview:** "Precision answers: of all the people the model flagged, how many really were positive? It is TP divided by (TP + FP). High precision means few false alarms."
**Explain simply:**
- Precision = TP / (TP + FP). The bottom is "everyone the model flagged".
- Think of it as the quality of the list you hand to a team.
- It ignores the positives the model missed entirely; that is recall's job (Q4).
**Worked example (concept questions):** Model flags 40 employees as likely leavers; 24 really leave (TP = 24, FP = 16). Precision = 24 / 40 = 0.60. Out of every 10 retention calls, 6 reach someone who was truly at risk.
**Alternative / pitfalls:** A model that flags just one very obvious leaver and gets it right has precision 100% yet is nearly useless. Never quote precision without recall.
**Likely follow-ups:** 1) *Another name?* Positive predictive value. 2) *When does it matter most?* When each flag triggers an expensive action.
**Common mistakes:** Dividing TP by all actual positives (that is recall); forgetting precision depends on the class you call positive.

### Q4 ⭐⭐⭐ 🟢 What is recall (also called sensitivity), in plain words, and what is its formula?
**Asked at:** commonly asked (no company-specific report found); a Tiger Analytics first-round report lists sensitivity and recall (anonymous report seen as a snippet, unverified).
**What the interviewer is checking:** That you understand recall as "how many of the real cases did we catch".
**Say this in the interview:** "Recall answers: of everyone who truly was positive, how many did the model find? It is TP divided by (TP + FN). High recall means few misses."
**Explain simply:**
- Recall = TP / (TP + FN). The bottom is "everyone who really was positive".
- Also called **sensitivity** or true positive rate: the same number under different names.
- It ignores false alarms; a model that flags everyone has recall 100% (Q57).
**Worked example (concept questions):** 30 employees really leave; the model catches 24 of them (TP = 24, FN = 6). Recall = 24 / 30 = 0.80, so 8 in 10 real leavers were flagged and 2 in 10 slipped through.
**Alternative / pitfalls:** Recall alone rewards over-flagging. Pair it with precision.
**Likely follow-ups:** 1) *Recall and sensitivity?* Same thing. 2) *What is the opposite error?* False negatives, the "misses".
**Common mistakes:** Using TP + FP in the denominator; thinking high recall means a good model on its own.

### Q5 ⭐⭐⭐ 🟢 Explain the difference between precision and recall to a non-technical HR manager using an employee attrition model as the example.
**Asked at:** commonly asked (no company-specific report found); HR-flavoured recall versus precision framing appears in attrition tutorials (unverified).
**What the interviewer is checking:** Whether you can drop the formulas and use a story the manager recognises.
**Say this in the interview:** "Precision is how many of the people we flag actually were going to leave. Recall is how many of the people who really left we managed to flag. One is about the quality of our list; the other is about how much of the problem we caught."
**Explain simply:**
- Precision: "When the model says Priya will resign, how often is it right?"
- Recall: "Of all who resigned, how many were on our list beforehand?"
- Flag more people and recall goes up, but precision usually falls because more flags are wrong.
- Flag only the surest cases and precision goes up, but you miss many leavers.
**Worked example (concept questions):** 200 employees; 30 truly leave. The model flags 40 and 24 of them leave. Precision = 24 / 40 = 0.60 (6 in 10 flags are right). Recall = 24 / 30 = 0.80 (we reached 8 in 10 leavers).
**Alternative / pitfalls:** Tie each metric to a rupee or time cost so the manager can choose (Q10, Q25).
**Likely follow-ups:** 1) *Which is more important?* Depends on the cost of a miss versus a wasted call. 2) *Can both be 100%?* Only for a perfect model, which is a warning sign (Q66).
**Common mistakes:** Using formulas on a non-technical audience; swapping the two definitions; saying one is always better.

### Q6 ⭐⭐⭐ 🟢 Why can accuracy be a misleading metric, especially when one class is rare?
**Asked at:** commonly asked (no company-specific report found); the "is 93% accuracy good?" question is a standard prep-site item (unverified).
**What the interviewer is checking:** That you know the accuracy paradox and the metrics to use instead.
**Say this in the interview:** "If one class is rare, a model can be highly accurate by always predicting the common class and never finding the rare one. So I look at recall and precision for the rare class, and compare against a do-nothing baseline."
**Explain simply:**
- **Class imbalance** means one outcome is far more common than the other (most employees stay, most transactions are honest).
- Accuracy counts all correct calls equally, so the common class dominates the score.
- A model with zero useful insight can still look excellent.
**Worked example (concept questions):** 1,000 employees, 50 leave. A model that says "stays" for everyone is right 950 times: accuracy 95%, yet it finds 0 of the 50 leavers (recall 0). See Q14.
**Alternative / pitfalls:** Report the confusion matrix, recall and precision for the rare class, and the baseline accuracy next to your model's.
**Likely follow-ups:** 1) *What would you report instead?* Recall, precision, F1, and maybe PR-AUC. 2) *What is the baseline here?* 95%, the share of the majority class.
**Common mistakes:** Celebrating 95% without checking the majority share; averaging away the rare class.

### Q7 ⭐⭐⭐ 🟢 A model for fraud detection gives you a confusion matrix. Explain its components and how you would choose between optimising precision or recall.
**Asked at:** Tiger Analytics (a Dataford page lists this exact fraud confusion-matrix and precision-versus-recall question; anonymous candidate report seen as a snippet, not opened, unverified).
**What the interviewer is checking:** That you link the metric to the cost of each mistake.
**Say this in the interview:** "In fraud, TP is fraud caught, FP is a good customer wrongly flagged, FN is fraud missed, TN is a good transaction passed. I choose by cost: if missed fraud is very expensive I push recall; if blocking good customers is costly or the review team is small, I push precision."
**Explain simply:**
- FN (missed fraud) costs the fraud amount plus trust; FP costs a review hour or an annoyed customer.
- Optimise **recall** when the miss is far costlier than the alarm (large-value fraud, safety checks).
- Optimise **precision** when every flag consumes scarce effort or harms customers (a small review team, card blocks).
- In practice you move the decision threshold (Q23) until cost and team capacity balance, and monitor both metrics.
**Worked example (concept questions):** Q22 below: a model flags 150 of 10,000 transactions with 60 truly fraud: precision 0.40, recall 0.60. If the team can review only 150 cases a day, precision decides how much of that effort is wasted.
**Alternative / pitfalls:** A two-step design works: a high-recall automatic screen, then humans or a second model raise precision.
**Likely follow-ups:** 1) *Which metric if the cost is unknown?* Show both and F1 or a precision-recall curve. 2) *Who decides?* The business, with your numbers.
**Common mistakes:** Choosing without discussing costs; quoting accuracy for fraud; treating precision and recall as independent knobs.

### Q8 ⭐⭐⭐ 🟢 What do sensitivity and specificity mean, and how do they relate to recall and the confusion matrix?
**Asked at:** Tiger Analytics (a first-round report lists sensitivity and specificity; anonymous candidate report seen as a snippet, unverified).
**What the interviewer is checking:** That you know sensitivity equals recall and that specificity is its mirror image on the negatives.
**Say this in the interview:** "Sensitivity is the share of real positives we catch, TP over (TP + FN); it is exactly recall. Specificity is the share of real negatives we correctly clear, TN over (TN + FP)."
**Explain simply:**
- Sensitivity = recall = TP / (TP + FN): "how good are we at finding the sick?"
- Specificity = TN / (TN + FP): "how good are we at clearing the healthy?"
- They use different halves of the confusion matrix: sensitivity uses the actual-positive row, specificity uses the actual-negative row.
- Specificity = 1 minus false positive rate (Q29).
**Worked example (concept questions):** Screen of 200 people: TP = 40, FN = 10, TN = 130, FP = 20. Sensitivity = 40 / 50 = 0.80. Specificity = 130 / 150 = 0.867.
**Alternative / pitfalls:** Precision is not specificity: precision looks at the flagged column, specificity at the actual-negative row.
**Likely follow-ups:** 1) *Can both be high?* Yes for a good model; raising one by moving the threshold usually lowers the other. 2) *Where used?* Medical tests, screening, ROC curves.
**Common mistakes:** Calling specificity "precision"; forgetting that sensitivity is recall.

### Q9 ⭐⭐⭐ 🟢 What is RMSE, and why is it easier to explain to a business user than MSE?
**Asked at:** commonly asked (no company-specific report found); RMSE and MAE are core items in regression-metric Q&A lists (unverified).
**What the interviewer is checking:** That you know RMSE is back in the original units.
**Say this in the interview:** "RMSE is the typical size of the model's prediction error. I square the errors, average them (that is MSE), then take the square root so the answer is back in the same units as the thing I predict, like lakh of sales."
**Explain simply:**
- Steps: error = predicted minus actual; square it; average; square root.
- MSE (mean squared error) is in squared units: lakh squared means nothing to a sales head.
- RMSE is in lakh, so "we are off by about 9 lakh a month, typically" is a sentence a manager can use.
- Squaring makes big misses count more.
**Worked example (concept questions):** Monthly sales forecast errors of +10, -5, +10, -10, -10 lakh (see Q18): MSE = 85 lakh squared; RMSE = square root of 85 = 9.22 lakh.
**Alternative / pitfalls:** Say "typical error" loosely; strictly it leans toward the larger errors (Q20).
**Likely follow-ups:** 1) *Lower is better?* Yes, 0 is perfect. 2) *Compared with what?* A baseline (Q32, Q44).
**Common mistakes:** Quoting MSE to a business user; forgetting the unit; reading RMSE without knowing the scale of the target.

### Q10 ⭐⭐⭐ 🟢 An attrition model flags employees who may resign. Would you prioritise precision or recall, and why?
**Asked at:** commonly asked (no company-specific report found); the HR recall-versus-precision framing appears in attrition tutorials (unverified).
**What the interviewer is checking:** That you decide from costs and capacity, not by habit.
**Say this in the interview:** "Usually I lean to recall, because losing a good employee costs far more than an extra check-in conversation. But if HR can only call a few people, precision matters too, so I would agree the budget first and then tune the threshold."
**Explain simply:**
- A missed leaver (FN) means replacement cost, lost knowledge, team strain.
- A false alarm (FP) means a friendly conversation and some wasted time, though calling people "at risk" can also create anxiety, so FPs are not free.
- If the retention budget is limited, a low-precision list wastes it: use precision@K (Q45).
- Either way, report both numbers.
**Worked example (concept questions):** Q25 gives Rs 50,000 per miss and Rs 2,000 per wasted call: a miss costs 25 wasted calls. At those costs, recall is worth chasing.
**Alternative / pitfalls:** Do not use flags for firing or ranking people; use them to offer support.
**Likely follow-ups:** 1) *What if HR wants both?* Q56. 2) *How to move the balance?* Change the threshold (Q23).
**Common mistakes:** Saying "recall always"; ignoring budget; ignoring ethical effects of labelling people.

### Q11 ⭐⭐⭐ 🟢 What is the F1 score, and when would you report it instead of accuracy?
**Asked at:** commonly asked (no company-specific report found); F1 versus accuracy is a standard prep-site topic (unverified).
**What the interviewer is checking:** That you know F1 balances precision and recall and suits imbalanced data.
**Say this in the interview:** "F1 is a single score that combines precision and recall using their harmonic mean. I report it instead of accuracy when the positive class is rare and I care about both false alarms and misses."
**Explain simply:**
- F1 = 2 x precision x recall / (precision + recall).
- **Harmonic mean** is a kind of average that punishes imbalance: if one of the two is low, F1 stays low (Q17).
- It ignores true negatives, so a huge pile of easy negatives cannot inflate it the way it inflates accuracy.
**Worked example (concept questions):** Precision 0.60 and recall 0.80 (Q5): F1 = 2 x 0.6 x 0.8 / 1.4 = 0.686. Accuracy for the same model was 0.89, hiding how many flags were wrong.
**Alternative / pitfalls:** F1 treats precision and recall as equally important; if misses cost far more, look at recall directly or use an F-beta score (from memory, unverified: F2 weights recall more).
**Likely follow-ups:** 1) *Is a higher F1 always better?* Only if equal weighting suits your costs. 2) *Why not the normal average?* Q17.
**Common mistakes:** Reporting F1 with no precision and recall; using it when costs are lopsided.

### Q12 ⭐⭐⭐ 🟢 How do you decide whether to use classification metrics (accuracy, precision, recall) or regression metrics (RMSE, MAE) for a problem?
**Asked at:** commonly asked (no company-specific report found); the classification versus regression split opens most evaluation question lists (unverified).
**What the interviewer is checking:** That you choose the metric from the type of the answer column.
**Say this in the interview:** "I look at what I am predicting. If it is a category, like leaves or stays, it is classification, so accuracy, precision, recall. If it is a number, like sales or salary, it is regression, so RMSE and MAE."
**Explain simply:**
- **Target** (or label) is the column you predict.
- Categories (yes/no, A/B/C): count right and wrong calls, so use confusion-matrix metrics.
- Numbers: measure how far off in the same units, so use RMSE, MAE, MAPE.
- A number turned into a band (salary under or over 50,000) becomes classification.
**Worked example (concept questions):** "Will this employee resign this year?" is classification (recall, precision). "How many days will this employee be absent?" is regression (MAE in days).
**Alternative / pitfalls:** A classifier can also output a probability (a number); you still judge its final yes/no calls with classification metrics.
**Likely follow-ups:** 1) *Is R-squared a regression metric?* Yes, but report it with an error in units (Q55). 2) *Can you use RMSE for yes/no?* Not usefully.
**Common mistakes:** Using accuracy on a numeric target; using RMSE on category codes.

### Q13 ⭐⭐⭐ 🟢 Accuracy calculation: using the confusion matrix below, what is the accuracy of the model?
TP = 40, FP = 10, FN = 20, TN = 130
**Asked at:** commonly asked (no company-specific report found); hand calculation from a confusion matrix is a common screening task (unverified).
**What the interviewer is checking:** Clean arithmetic and correct formula.
**Say this in the interview:** "Correct calls are TP plus TN, 170, out of 200 total, so accuracy is 85%."
**Explain simply:**
- Total = 40 + 10 + 20 + 130 = 200.
- Correct = TP + TN = 170.
- Accuracy = 170 / 200.
**Code (what you write in the interview):**
```python
tp, fp, fn, tn = 40, 10, 20, 130

# correct predictions divided by all predictions
accuracy = (tp + tn) / (tp + fp + fn + tn)
print(accuracy)
```
**Output:**
```
0.85
```
**What it means:** The model is right 85 times in 100. Report it with recall: here recall is 40 / 60 = 0.67, so a third of the real positives are missed.
**Alternative / pitfalls:** Check the majority-class baseline: 150 actual negatives out of 200 is 75%, so 85% is only 10 points better.
**Likely follow-ups:** 1) *Precision?* 40 / 50 = 0.80. 2) *Is 85% good?* Depends on the baseline and costs.
**Common mistakes:** Leaving out TN; dividing by 100.

### Q14 ⭐⭐⭐ 🟢 A model predicts that no employee will leave. Of 1,000 employees, 950 stay and 50 leave. What are the accuracy and the recall for the 'leaves' class, and what does this tell you?
**Asked at:** commonly asked (no company-specific report found); this accuracy paradox example is standard in prep-site lists (unverified).
**What the interviewer is checking:** That you see accuracy hiding total failure.
**Say this in the interview:** "Accuracy is 95% but recall for leavers is zero. The model is useless for the one job we want, so accuracy alone is misleading here."
**Explain simply:**
- Everyone predicted "stays": 950 stayers are right (TN = 950); 50 leavers are missed (FN = 50); no one flagged (TP = 0, FP = 0).
- Accuracy = 950 / 1,000. Recall = 0 / 50.
- Precision is undefined (0 flags, so 0 divided by 0).
**Code (what you write in the interview):**
```python
# the model never predicts "leaves", so nothing is flagged
tp, fp, fn, tn = 0, 0, 50, 950

accuracy = (tp + tn) / (tp + fp + fn + tn)
recall = tp / (tp + fn)
print("accuracy:", accuracy)
print("recall:", recall)
```
**Output:**
```
accuracy: 0.95
recall: 0.0
```
**What it means:** 95% right, 0% of leavers found. Tell the manager: "this model is no better than doing nothing."
**Alternative / pitfalls:** This "always stays" model is the baseline any real model must beat on recall and precision.
**Likely follow-ups:** 1) *What would you report?* Recall, precision, confusion matrix. 2) *How to fix it?* Better features, a lower threshold, class weights (covered in other parts).
**Common mistakes:** Proudly quoting 95%; computing precision as 0 instead of "undefined".

### Q15 ⭐⭐⭐ 🟡 Precision calculation: an attrition model produced the matrix below. What is its precision for the 'leaves' class, and what does that figure mean for the HR team acting on the flags?
TP = 24, FP = 16, FN = 6, TN = 154
**Asked at:** commonly asked (no company-specific report found); hand-computing precision from a matrix is a common screening task (unverified).
**What the interviewer is checking:** Correct formula plus translating it into HR action.
**Say this in the interview:** "Precision is 24 out of the 40 people flagged, so 60%. That means about 4 in every 10 retention conversations will go to someone who was not actually at risk."
**Explain simply:**
- Flagged = TP + FP = 24 + 16 = 40.
- Precision = TP / flagged = 24 / 40.
- Recall for context: 24 / 30 = 0.80, so most leavers are found.
**Code (what you write in the interview):**
```python
tp, fp, fn, tn = 24, 16, 6, 154

# of everyone flagged, how many really were at risk
precision = tp / (tp + fp)
print(precision)
```
**Output:**
```
0.6
```
**What it means:** Report "60% of flags are real, 80% of leavers are caught". The team should budget for 16 wasted conversations per 40 and treat them as light-touch check-ins.
**Alternative / pitfalls:** The base rate of leavers is 30 / 200 = 15%; precision of 60% is four times better than picking at random.
**Likely follow-ups:** 1) *How to raise precision?* Raise the threshold; recall will fall. 2) *Is 60% good?* Depends on the cost of a wasted call.
**Common mistakes:** Dividing by 30 (that is recall); ignoring the practical meaning.

### Q16 ⭐⭐⭐ 🟡 Recall calculation: of 60 employees who actually resigned, the model flagged 45 of them. It also flagged 30 employees who stayed. What is the recall, and what is the precision?
**Asked at:** commonly asked (no company-specific report found); a standard hand-computation prompt (unverified).
**What the interviewer is checking:** That you build TP, FN and FP from the story before using the formulas.
**Say this in the interview:** "Recall is 45 of 60, which is 75%. Total flagged is 45 plus 30, which is 75, so precision is 45 of 75, which is 60%."
**Explain simply:**
- TP = 45 (resigned and flagged).
- FN = 60 - 45 = 15 (resigned but not flagged).
- FP = 30 (stayed but flagged).
- True negatives are not given and not needed for either metric.
**Code (what you write in the interview):**
```python
tp = 45
fn = 60 - 45
fp = 30

recall = tp / (tp + fn)
precision = tp / (tp + fp)
print("recall:", recall)
print("precision:", precision)
```
**Output:**
```
recall: 0.75
precision: 0.6
```
**What it means:** The model finds three quarters of leavers, and six in ten flags are right. Both can be reported without the TN count.
**Alternative / pitfalls:** F1 here is 2 x 0.6 x 0.75 / 1.35 = 0.667.
**Likely follow-ups:** 1) *Accuracy?* Cannot be computed without TN. 2) *Which to improve?* Depends on costs.
**Common mistakes:** Using 30 as the FN; trying to compute accuracy without TN.

### Q17 ⭐⭐⭐ 🟡 F1 calculation: a model has precision 0.80 and recall 0.50. What is its F1 score, and why is it lower than the simple average of the two?
**Asked at:** commonly asked (no company-specific report found); F1 arithmetic is a typical screening item (unverified).
**What the interviewer is checking:** The formula and the idea of the harmonic mean.
**Say this in the interview:** "F1 is 2 times 0.8 times 0.5 divided by 1.3, about 0.615. The simple average would be 0.65. F1 is lower because it is a harmonic mean, which is pulled toward the weaker number."
**Explain simply:**
- F1 = 2PR / (P + R) = 0.80 / 1.30.
- The simple average treats 0.8 and 0.5 as an even trade.
- The harmonic mean punishes a big gap: a model cannot hide terrible recall behind great precision.
- Extreme case: precision 1.0 and recall 0.0 gives a simple average of 0.5 but an F1 of 0.
**Code (what you write in the interview):**
```python
precision = 0.80
recall = 0.50

f1 = 2 * precision * recall / (precision + recall)
print("F1:", round(f1, 3))
print("simple average:", (precision + recall) / 2)
```
**Output:**
```
F1: 0.615
simple average: 0.65
```
**What it means:** The model scores 0.615 overall; the gap to 0.65 shows its recall is dragging it down.
**Alternative / pitfalls:** For different weights use F-beta (from memory, unverified).
**Likely follow-ups:** 1) *Range of F1?* 0 to 1. 2) *Can F1 exceed both inputs?* No, it lies between them.
**Common mistakes:** Averaging precision and recall; forgetting the factor 2.

### Q18 ⭐⭐⭐ 🟡 RMSE calculation: compute the RMSE from the five predictions below.
Actual monthly sales (lakh): 100, 120, 90, 110, 130
Predicted: 110, 115, 100, 100, 120
**Asked at:** commonly asked (no company-specific report found); a standard regression-metric calculation (unverified).
**What the interviewer is checking:** The four steps: error, square, mean, root.
**Say this in the interview:** "Errors are +10, -5, +10, -10, -10. Squares are 100, 25, 100, 100, 100, which sum to 425. Mean is 85. Square root is about 9.2 lakh."
**Explain simply:**
- Error = predicted minus actual (the sign does not matter once squared).
- MSE = 425 / 5 = 85 (lakh squared).
- RMSE = square root of 85.
**Code (what you write in the interview):**
```python
import numpy as np

actual = np.array([100, 120, 90, 110, 130])
predicted = np.array([110, 115, 100, 100, 120])

# prediction error for each month
errors = predicted - actual

# square, average, then square root
rmse = np.sqrt(np.mean(errors ** 2))
print("errors:", errors)
print("RMSE:", round(rmse, 2))
```
**Output:**
```
errors: [ 10  -5  10 -10 -10]
RMSE: 9.22
```
**What it means:** The forecast is typically about 9 lakh away from the real monthly sales (average sales are 110 lakh, so roughly 8%).
**Alternative / pitfalls:** sklearn has `root_mean_squared_error` (see Q51 in this part for the version note).
**Likely follow-ups:** 1) *How does it compare with MAE?* MAE is 9.0 (Q19); RMSE is a bit larger. 2) *Good or bad?* Compare with a baseline.
**Common mistakes:** Forgetting the square root; dividing by 4; forgetting units.

### Q19 ⭐⭐⭐ 🟡 MAE calculation: using the same five predictions below, what is the MAE, and how would you say it to a sales head?
Actual monthly sales (lakh): 100, 120, 90, 110, 130
Predicted: 110, 115, 100, 100, 120
**Asked at:** commonly asked (no company-specific report found); a standard regression-metric calculation (unverified).
**What the interviewer is checking:** That you can compute it and put it in a plain sentence.
**Say this in the interview:** "MAE is the average size of the miss, ignoring direction: 9 lakh. I would tell the sales head: on average, our forecast is off by about 9 lakh a month."
**Explain simply:**
- Absolute errors: 10, 5, 10, 10, 10; sum 45; divided by 5 gives 9.
- Same units as sales (lakh), so no translation is needed.
**Code (what you write in the interview):**
```python
import numpy as np

actual = np.array([100, 120, 90, 110, 130])
predicted = np.array([110, 115, 100, 100, 120])

# average size of the miss, ignoring direction
mae = np.mean(np.abs(predicted - actual))
print("MAE:", mae)
```
**Output:**
```
MAE: 9.0
```
**What it means:** Typical miss of 9 lakh. Say it with the scale: about 8% of average monthly sales of 110 lakh.
**Alternative / pitfalls:** MAE does not say whether the model tends to over- or under-predict; look at the signed errors for that (here: two over-predictions, three under).
**Likely follow-ups:** 1) *Why is RMSE bigger?* Squaring weights big misses more (Q20). 2) *Percentage version?* MAPE (Q53).
**Common mistakes:** Averaging signed errors (they cancel); quoting without units.

### Q20 ⭐⭐⭐ 🟡 What is the difference between RMSE and MAE, and when would you report each?
**Asked at:** commonly asked (no company-specific report found); RMSE versus MAE is a standard regression Q&A item (unverified).
**What the interviewer is checking:** That you know the outlier sensitivity and can choose for the audience.
**Say this in the interview:** "Both are error sizes in the original units. MAE is the plain average miss. RMSE squares first, so big misses count more. I report MAE for 'typical error' and RMSE when large misses are especially costly, and often I show both."
**Explain simply:**
- MAE = average of absolute errors. Easy to explain, treats every rupee of error equally.
- RMSE = square root of the average squared error. Always at least as large as MAE.
- A big gap between RMSE and MAE hints at a few large errors (outliers).
- If all errors are the same size, the two are equal.
**Worked example (concept questions):** Errors 2, 2, 2, 2, 12: MAE = 4.0, RMSE = 5.66 (see Q43). One big miss lifts RMSE much more.
**Alternative / pitfalls:** Choose by cost: if a 12-lakh miss is far worse than six 2-lakh misses, RMSE reflects that; if costs are proportional to the miss, MAE does.
**Likely follow-ups:** 1) *Which is more robust to outliers?* MAE. 2) *Which is easier to explain?* MAE.
**Common mistakes:** Saying RMSE is "more accurate"; quoting only one without saying why.

### Q21 ⭐⭐⭐ 🟡 Code reading: what confusion matrix does this code print, and what are the precision and recall?
```python
from sklearn.metrics import confusion_matrix
y_true = [1,0,1,1,0,0,1,0,0,0]
y_pred = [1,0,0,1,0,1,1,0,0,0]
print(confusion_matrix(y_true, y_pred))
```
**Asked at:** commonly asked (no company-specific report found); reading sklearn confusion-matrix output is a common screening task (unverified).
**What the interviewer is checking:** That you know sklearn's layout: rows actual, columns predicted, class 0 first.
**Say this in the interview:** "It prints [[5, 1], [1, 3]]. Top row is actual 0: 5 true negatives, 1 false positive. Bottom row is actual 1: 1 false negative, 3 true positives. Precision is 3 over 4, recall is 3 over 4, both 0.75."
**Explain simply:**
- Rows are the actual values; columns are the predicted values; the order is 0 then 1.
- So the layout is [[TN, FP], [FN, TP]].
- Check by hand: position 2 is a missed 1 (FN), position 5 is a false alarm (FP), positions 0, 3, 6 are hits (TP), the other five are TN.
- Precision = 3 / (3 + 1); recall = 3 / (3 + 1).
**Output:**
```
[[5 1]
 [1 3]]
```
**What it means:** The model finds 3 of 4 actual positives and 3 of its 4 flags are right.
**Alternative / pitfalls:** If labels were text, pass `labels=[...]` to fix the order (from memory, unverified).
**Likely follow-ups:** 1) *How to get precision and recall?* `precision_score` and `recall_score`. 2) *Accuracy?* (5 + 3) / 10 = 0.8.
**Common mistakes:** Reading the matrix as [[TP, FP], [FN, TN]]; swapping rows and columns.

### Q22 ⭐⭐⭐ 🟡 Accuracy paradox: a card-fraud model is tested on 10,000 transactions of which 100 are fraud. It flags 150 transactions, 60 of them truly fraud. Calculate accuracy, precision and recall, and say whether you would call this model good.
**Asked at:** commonly asked (no company-specific report found); hand computation from a fraud confusion matrix appears on prep sites (unverified).
**What the interviewer is checking:** That you rebuild the four cells, compute all three, and judge honestly.
**Say this in the interview:** "Accuracy is 98.7%, which looks superb, but precision is only 40% and recall 60%. Doing nothing would already score 99%. So I would not call it good on accuracy; whether it is usable depends on the cost of a missed fraud versus a wasted review."
**Explain simply:**
- TP = 60. FP = 150 - 60 = 90. FN = 100 - 60 = 40. TN = 10,000 - 60 - 90 - 40 = 9,810.
- Accuracy = (60 + 9,810) / 10,000.
- Baseline "no fraud ever": 9,900 right = 99%, higher than the model's accuracy.
- Precision = 60 / 150; recall = 60 / 100.
**Code (what you write in the interview):**
```python
total, fraud, flagged, caught = 10000, 100, 150, 60

# build the four cells from the story
tp = caught
fp = flagged - caught
fn = fraud - caught
tn = total - tp - fp - fn

print("accuracy:", (tp + tn) / total)
print("precision:", tp / (tp + fp))
print("recall:", tp / (tp + fn))
```
**Output:**
```
accuracy: 0.987
precision: 0.4
recall: 0.6
```
**What it means:** The model catches 60% of fraud, but 6 in 10 flagged cases are good customers. It may still be valuable if each fraud is costly and reviews are cheap; present all three numbers and the baseline.
**Alternative / pitfalls:** Compare precision with the random baseline of 1% (100 of 10,000): 40% is 40 times better than guessing, which is the real story.
**Likely follow-ups:** 1) *F1?* 2 x 0.4 x 0.6 / 1.0 = 0.48. 2) *How to improve?* Tune the threshold, add features.
**Common mistakes:** Calling it excellent because of 98.7%; forgetting to compute TN; ignoring cost.

### Q23 ⭐⭐⭐ 🟡 How does lowering the classification threshold from 0.5 to 0.3 change the number of false positives, false negatives, precision and recall?
**Asked at:** commonly asked (no company-specific report found); "threshold hiding in the confusion matrix" appears in prep-site Q&A (unverified snippets).
**What the interviewer is checking:** That you know a model gives a score, and the threshold you pick moves errors from one type to the other.
**Say this in the interview:** "A lower threshold flags more people. False negatives go down and recall goes up, but false positives go up and precision usually goes down. It is a trade-off, and I choose the threshold from the cost of each error."
**Explain simply:**
- A model gives each employee a **score** (a probability-like number from 0 to 1). The **threshold** is the cut-off: score at or above it means "flag as will leave".
- At 0.3 more people cross the line, so you catch more real leavers (fewer **false negatives**, FN = leavers we missed) but also flag more stayers by mistake (more **false positives**, FP = stayers we wrongly flagged).
- **Recall** = TP / (TP + FN), the share of real leavers caught. **Precision** = TP / (TP + FP), the share of flags that are right.
- Recall can only stay the same or rise when you lower the threshold. Precision usually falls, though not always step by step.
**Worked example (concept questions):** 1,000 employees, 218 real leavers, simulated scores. How it was made, so you can rerun it: numpy `default_rng(42)`; each employee leaves with chance 0.2; the score is a normal random number with mean 0.75 for leavers and 0.25 for stayers (spread 0.2), cut to the range 0 to 1.

| Threshold | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| 0.5 | 186 | 78 | 32 | 0.70 | 0.85 |
| 0.3 | 213 | 310 | 5 | 0.41 | 0.98 |

Lowering to 0.3 caught 27 more leavers but added 232 extra false alarms.
**Alternative / pitfalls:** 0.5 is only a default, not a law. If leavers are rare, the best threshold is often well below 0.5. Pick it from cost (see Q25), not habit.
**Likely follow-ups:** 1) *What if I raise it to 0.7?* Fewer flags: precision up, recall down. 2) *How to see all thresholds at once?* ROC or precision-recall curve (Q36).
**Common mistakes:** Saying precision and recall always move in exact opposite directions; reporting one threshold's numbers without saying the threshold.

### Q24 ⭐⭐⭐ 🟡 Your manager asks 'how accurate is the churn model?' How do you answer in a way that is honest and useful, rather than quoting one accuracy number?
**Asked at:** commonly asked (no company-specific report found); "is 93% accuracy good?" style questions appear in prep-site lists (unverified).
**What the interviewer is checking:** That you give context (baseline, rare class, error types, cost) and not a single headline number.
**Say this in the interview:** "Accuracy alone can mislead. I would say: of customers who really churn, the model catches X%; of those it flags, Y% really churn; and that beats a simple baseline by Z. Then I translate it into customers and rupees."
**Explain simply:**
- Give **recall** (share of real churners caught) and **precision** (share of flags that are right) in plain sentences.
- Give the **baseline**: what you would get by guessing "nobody churns". If only 22% churn, that guess is 78% accurate.
- Say which dataset the numbers come from (unseen test data, not training data) and how many rows.
- Turn it into action: "if we call 250 flagged customers, about 175 will be real churners".
- Mention the limits: one time period, small groups, threshold chosen.
**Worked example (concept questions):** From the Q23 numbers at threshold 0.5 (treat the leavers as churners): accuracy 0.89, but baseline 0.78. Better statement: "It catches 85 of every 100 churners, and 70 of every 100 flagged customers are real churners. Guessing 'no churn' would have been 78% accurate and caught nobody."
**Alternative / pitfalls:** Offer a one-line summary for the manager and keep the confusion matrix in a backup slide.
**Likely follow-ups:** 1) *Which number is most important?* Depends on the cost of missing versus wasted calls. 2) *Would you quote accuracy at all?* Yes, next to the baseline.
**Common mistakes:** Quoting accuracy only; no baseline; quoting training results; jargon like "F1" without translating.

### Q25 ⭐⭐⭐ 🟡 Cost-based choice: a missed leaver (FN) costs about Rs 50,000 in replacement; a wasted retention call (FP) costs Rs 2,000. Using the counts below, which model has the lower total error cost, and by how much?
Model A: FN = 10, FP = 40
Model B: FN = 20, FP = 10
**Asked at:** commonly asked (no company-specific report found); asymmetric-cost prompts appear in prep-site lists (unverified).
**What the interviewer is checking:** That you weigh errors by their business cost instead of counting them equally.
**Say this in the interview:** "Total cost is FN times 50,000 plus FP times 2,000. Model A costs Rs 5.8 lakh, Model B Rs 10.2 lakh, so A is cheaper by Rs 4.4 lakh, even though it makes more errors in total."
**Explain simply:**
- **FN** (false negative): a leaver the model missed. **FP** (false positive): a stayer the model flagged, so the call was wasted.
- Model A makes 50 errors, Model B only 30, but A's errors are mostly cheap FPs.
- One missed leaver costs 25 wasted calls, so FN deserves much more weight.
**Code (what you write in the interview):**
```python
cost_per_missed_leaver = 50000
cost_per_wasted_call = 2000

cost_model_a = 10 * cost_per_missed_leaver + 40 * cost_per_wasted_call
cost_model_b = 20 * cost_per_missed_leaver + 10 * cost_per_wasted_call

print("Model A cost:", cost_model_a)
print("Model B cost:", cost_model_b)
print("B costs more by:", cost_model_b - cost_model_a)
```
**Output:**
```
Model A cost: 580000
Model B cost: 1020000
B costs more by: 440000
```
**What it means:** Model A saves Rs 4.4 lakh. Report cost, not just error count.
**Alternative / pitfalls:** The costs are rough estimates; test how the answer changes if a missed leaver costs Rs 30,000 or Rs 70,000. Here A saves 10 missed leavers and adds 30 wasted calls, so A stays cheaper as long as a missed leaver costs more than Rs 6,000 (10 x miss > 30 x 2,000).
**Likely follow-ups:** 1) *Does the cost include the cost of the retention offer itself?* Not here; add it for a full picture. 2) *Can you tune the threshold for cost?* Yes, pick the threshold with the lowest total cost.
**Common mistakes:** Comparing error counts only; mixing up which error is costlier.

### Q26 ⭐⭐⭐ 🟡 Code reading: in scikit-learn, in what order does confusion_matrix(y_true, y_pred).ravel() return its four values, and how would you unpack them to compute recall?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the order is TN, FP, FN, TP (for labels 0 and 1) and do not mix up the cells.
**Say this in the interview:** "For a binary 0/1 problem it returns TN, FP, FN, TP, in that order. I unpack with `tn, fp, fn, tp = ...ravel()` and recall is tp / (tp + fn)."
**Explain simply:**
- sklearn's matrix has rows = actual, columns = predicted, with class 0 first: `[[TN, FP], [FN, TP]]`. `.ravel()` flattens it row by row.
- Recall = TP / (TP + FN): of all real positives (leavers), how many we caught.
- Many people expect TP first. That is the common trap.
**Sample data:** 10 employees, 1 = leaves.
**Code (what you write in the interview):**
```python
from sklearn.metrics import confusion_matrix

y_true = [1, 0, 1, 1, 0, 0, 0, 1, 0, 0]
y_pred = [1, 0, 0, 1, 0, 1, 0, 1, 0, 0]

# sklearn order: TN, FP, FN, TP
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

recall = tp / (tp + fn)
print(tn, fp, fn, tp)
print("Recall:", recall)
```
**Output:**
```
5 1 1 3
Recall: 0.75
```
**What it means:** 4 people really left; the model caught 3, so recall is 0.75.
**Alternative / pitfalls:** `recall_score(y_true, y_pred)` gives the same answer directly. If the data contains only one class, `.ravel()` returns a single value (checked on the installed version) and the four-way unpacking fails; guard with `labels=[0, 1]`.
**Likely follow-ups:** 1) *What if labels are strings?* Pass `labels=["stay", "leave"]` to fix the order. 2) *Precision?* tp / (tp + fp).
**Common mistakes:** Unpacking as tp, fp, fn, tn; reading the matrix with columns as actual.

### Q27 ⭐⭐⭐ 🟡 Two analysts report 'model accuracy' for the same attrition data and get 0.92 and 0.81. Name three reasons the numbers might differ legitimately.
**Asked at:** commonly asked (no company-specific report found); a gap-fill question (not taken from a reported interview).
**What the interviewer is checking:** That you understand a metric depends on how it was measured.
**Say this in the interview:** "Different train/test split or random seed, different data or time period, and different threshold or metric definition. I would ask both for the code and the test set before deciding anything."
**Explain simply:**
- **Different split:** a small random test set gives noisy accuracy. Different `random_state` values give different results.
- **Different data:** one analyst may have used train data (optimistic) and the other test data; or different years, filters, or different class mix.
- **Different threshold or metric:** accuracy at cut-off 0.5 versus 0.3, or "balanced accuracy", or cross-validated average versus one split.
- Also possible: different features, preprocessing, or an unnoticed leak in one pipeline.
**Worked example (concept questions):** Same logistic model, same synthetic data (1,000 rows, about 15% leave; the generator is in Q52), only the split seed changes (random_state 0 to 4, test set 250 rows, plain random split). Accuracy: 0.92, 0.92, 0.90, 0.88, 0.90. Recall on the leavers swung much more: 0.66, 0.64, 0.57, 0.43, 0.73.
**Alternative / pitfalls:** If the leavers are about 15%, guessing "nobody leaves" gives about 0.85 (0.82 to 0.85 in the test sets above), so accuracy alone says little.
**Likely follow-ups:** 1) *How do you settle it?* Same data, same split, same metric, then cross-validate. 2) *Is one of them wrong?* Not necessarily.
**Common mistakes:** Assuming one analyst made an error; not asking what data the number came from.

### Q28 ⭐⭐ 🟢 What is specificity (true negative rate), and how is it calculated from a confusion matrix?
TP = 30, FN = 20, TN = 180, FP = 20
**Asked at:** commonly asked (no company-specific report found); sensitivity and specificity are reported as first-round fundamentals in Tiger Analytics candidate summaries (anonymous, unverified).
**What the interviewer is checking:** That you can define specificity as the mirror image of recall.
**Say this in the interview:** "Specificity is the share of real negatives the model correctly leaves alone: TN / (TN + FP). Here 180 / 200, so 0.90."
**Explain simply:**
- Real negatives here are employees who stay: TN + FP = 200.
- The model left 180 of them alone (**TN**, true negative) and wrongly flagged 20 (**FP**).
- Recall (sensitivity) looks at real leavers; specificity looks at real stayers.
- Specificity = 1 minus false positive rate (Q29).
**Code (what you write in the interview):**
```python
tn, fp = 180, 20

specificity = tn / (tn + fp)
print("Specificity:", specificity)
```
**Output:**
```
Specificity: 0.9
```
**What it means:** The model correctly leaves alone 90 of every 100 employees who stay. For the same table, recall is 30 / 50 = 0.60.
**Likely follow-ups:** 1) *Relation to recall?* Recall is sensitivity (positives), specificity is for negatives. 2) *When does it matter?* When false alarms are costly.
**Common mistakes:** Using FN instead of FP in the denominator.

### Q29 ⭐⭐ 🟢 What is the false positive rate, and why does a screening team care about it?
**Asked at:** commonly asked (no company-specific report found); false positive rate hand-calculations appear in prep-site fraud prompts (unverified).
**What the interviewer is checking:** That you know FPR is measured against all real negatives, and understand the workload it creates.
**Say this in the interview:** "False positive rate is the share of real negatives wrongly flagged: FP / (FP + TN). A screening team cares because every false alarm uses reviewer time and can annoy or wrongly burden a person."
**Explain simply:**
- FPR = FP / (FP + TN). It is 1 minus specificity.
- It is a rate within the negatives, so it ignores how many real positives exist.
- Even a small FPR matters when negatives are huge: 1% of 100,000 clean transactions is 1,000 false alarms.
**Worked example (concept questions):** From the Q28 table, 20 of 200 stayers were wrongly flagged: FPR = 20 / 200 = 0.10. If HR flags 10 of every 100 stayers, those calls are wasted effort.
**Alternative / pitfalls:** A low FPR can still mean low precision when positives are rare (many more negatives than positives), so also report precision.
**Likely follow-ups:** 1) *Where is it used?* The x-axis of the ROC curve. 2) *FPR vs precision?* Different denominators.
**Common mistakes:** Dividing FP by all flagged items (that is 1 minus precision); forgetting the base rate.

### Q30 ⭐⭐ 🟢 What is MAE (mean absolute error), and what are its units?
**Asked at:** commonly asked (no company-specific report found); MAE vs RMSE appears in regression-metric Q&A (unverified).
**What the interviewer is checking:** That you know it is an average size of error in the target's own units.
**Say this in the interview:** "MAE is the average of the absolute gaps between predictions and actual values. It is in the same units as the thing you predict, so an MAE of Rs 2,400 means predictions are off by about Rs 2,400 on average."
**Explain simply:**
- Error = actual minus predicted; **absolute** means ignore the sign, so over- and under-predictions do not cancel.
- MAE = average of those absolute errors.
- Units are the target's units: rupees, units sold, days.
**Worked example (concept questions):** Monthly pay actual (Rs thousand) 50, 60, 55, 70, 65 versus predicted 52, 57, 55, 76, 64. Absolute errors 2, 3, 0, 6, 1; MAE = 12 / 5 = 2.4, that is Rs 2,400.
**Alternative / pitfalls:** MAE treats all errors in proportion; RMSE penalises big errors more (Q20).
**Likely follow-ups:** 1) *How do you say it to a manager?* "Typically off by about Rs 2,400." 2) *Is smaller better?* Yes, relative to the baseline and the target's scale.
**Common mistakes:** Forgetting absolute values; giving a unitless number.

### Q31 ⭐⭐ 🟢 What is MSE, and why do we square the errors instead of just averaging them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know plain errors cancel out and squaring fixes that and punishes big misses.
**Say this in the interview:** "MSE is the mean of squared errors. Without squaring, positive and negative errors cancel and a bad model can look perfect. Squaring removes the sign and punishes large errors more."
**Explain simply:**
- **Error** (residual) = actual minus predicted.
- Averaging raw errors can give zero even for poor predictions.
- Squaring makes every error positive, and a miss of 10 counts four times as much as a miss of 5.
- Squared units (rupees squared) are hard to explain, so we take the square root: RMSE (Q9).
**Worked example (concept questions):** Two errors, +10 and -10. Plain average = 0 (looks perfect). Squared: 100 and 100; MSE = 100; RMSE = 10, which says "off by 10".
**Alternative / pitfalls:** Squaring also makes the metric sensitive to outliers, and it is smooth for training (maths convenience).
**Likely follow-ups:** 1) *Why not absolute values?* That is MAE; both are valid. 2) *Units?* Squared target units.
**Common mistakes:** Quoting MSE to a manager; saying squaring is only for maths convenience.

### Q32 ⭐⭐ 🟢 What is a baseline model, and why should you compare a new model against one before reporting its metric?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you never report a metric without a "does this beat a simple guess" check.
**Say this in the interview:** "A baseline is the simplest sensible prediction, like 'nobody leaves' or 'always predict the average'. If my model barely beats it, the model adds little, however good its number sounds."
**Explain simply:**
- Classification baseline: always predict the most common class. Regression baseline: always predict the mean (or last month's value).
- Gives meaning to a number: 95% accuracy is poor if the baseline is 95%.
- Also protects against hype and over-engineering.
**Worked example (concept questions):** 1,000 employees, 50 leave. The baseline "no one leaves" is 95% accurate with 0% recall. A model with 96% accuracy is only 1 point better, so judge it by recall and precision on the leavers.
**Alternative / pitfalls:** For time series use the "same as last period" baseline, not the overall average.
**Likely follow-ups:** 1) *Baseline for regression?* Predict the mean (Q44). 2) *How much better should the model be?* Enough to change a business decision.
**Common mistakes:** Comparing only to another complex model; ignoring the baseline when classes are imbalanced.

### Q33 ⭐⭐ 🟢 What is the difference between a false positive and a false negative? Give one example each from a hiring-screening model.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you attach the terms to real people and consequences.
**Say this in the interview:** "A false positive is the model saying yes when the truth is no: it shortlists an unsuitable candidate. A false negative is it saying no when the truth is yes: it rejects a candidate who would have been good."
**Explain simply:**
- "Positive" means what the model flags (here, shortlist).
- **False positive (FP):** shortlisted but unsuitable; costs interviewer time.
- **False negative (FN):** rejected but suitable; the company loses a good hire and the candidate is treated unfairly, and nobody ever sees this error.
- Which is worse depends on the situation; with a large applicant pool, FNs are often costlier and hidden.
**Worked example (concept questions):** 500 applicants, 60 suitable. Shortlisting 50 with 30 suitable gives 20 FP and 30 FN (see Q41).
**Alternative / pitfalls:** Always say which class you call "positive".
**Likely follow-ups:** 1) *How would you reduce FN?* Lower the threshold. 2) *Fairness?* Check error rates by group.
**Common mistakes:** Swapping the two; forgetting the hidden cost of FN.

### Q34 ⭐⭐ 🟢 What does a residual mean in a regression model, and how is it linked to RMSE?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you see RMSE as a summary of the residuals.
**Say this in the interview:** "A residual is actual minus predicted for one row. RMSE squares all the residuals, averages them and takes the square root, so it is a typical residual size in the target's units."
**Explain simply:**
- Residual = actual value minus the model's prediction. Positive: model under-predicted; negative: over-predicted.
- Plot residuals to spot patterns (a good model leaves random-looking residuals).
- RMSE = square root of mean of squared residuals.
**Worked example (concept questions):** Actual 30, 40, 50, 60; predicted 33, 38, 50, 64. Residuals: -3, 2, 0, -4 (mean -1.25). Squared: 9, 4, 0, 16; mean 7.25; RMSE = 2.69.
**Alternative / pitfalls:** Residuals averaging near zero does not mean the model is good (positives cancel negatives); look at their size.
**Likely follow-ups:** 1) *Residual vs error?* On the test set people say error; for training data, residual. 2) *What does a pattern mean?* The model misses something.
**Common mistakes:** Treating the mean residual as the model's error.

### Q35 ⭐⭐ 🟢 What is the difference between precision and accuracy in model evaluation (not in measurement)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you do not confuse the everyday word with the specific metric.
**Say this in the interview:** "Accuracy is the share of all predictions that are right. Precision is the share of positive flags that are right. Accuracy can be high while precision, or recall, is poor."
**Explain simply:**
- Accuracy = (TP + TN) / all rows. Precision = TP / (TP + FP), looking only at flagged rows.
- Accuracy mixes both classes; precision focuses on the flags.
- With a rare class, accuracy is dominated by the easy majority.
**Worked example (concept questions):** 1,000 employees, 50 leave. Model flags 10, of whom 9 truly leave: TP 9, FP 1, FN 41, TN 949. Accuracy = 958 / 1000 = 0.96; precision = 9 / 10 = 0.90; recall = 9 / 50 = 0.18. High accuracy and precision hide that 82% of leavers were missed.
**Alternative / pitfalls:** Precision alone can be gamed by flagging very few cases.
**Likely follow-ups:** 1) *Which to report?* Precision with recall. 2) *Measurement sense?* Spread of repeated readings; different topic.
**Common mistakes:** Using the two words interchangeably.

### Q36 ⭐⭐ 🟢 What does an ROC curve show, and what do AUC values of 0.5 and 1.0 mean?
**Asked at:** commonly asked (no company-specific report found); ROC-AUC is named in a Flipkart Data Scientist report (single forum post, snippet, unverified).
**What the interviewer is checking:** That you can describe the curve without formulas and give the AUC reading.
**Say this in the interview:** "The ROC curve shows, across all thresholds, the share of real positives caught (recall) against the share of real negatives wrongly flagged (false positive rate). AUC is the area under it: 0.5 is no better than a coin flip, 1.0 is perfect separation."
**Explain simply:**
- Each point on the curve is one threshold. Moving along it trades recall against false alarms.
- **AUC** (area under the curve) has a simple meaning: the chance that a random leaver gets a higher score than a random stayer.
- 0.5 = random ranking (diagonal line). 1.0 = every leaver scored above every stayer. Below 0.5 means the ranking is backwards.
- AUC measures ranking, not whether a given threshold is good.
**Worked example (concept questions):** Six employees, 3 leavers. Perfect scores (leavers all higher): AUC 1.0. One leaver ranked below one stayer: AUC 0.78. All scores equal: AUC 0.50. Random 0/1 labels and random scores on 2,000 rows (numpy `default_rng(1)`): AUC about 0.50 (0.498 here).
**Alternative / pitfalls:** On rare-event problems ROC-AUC can look flattering (Q71); also check precision-recall.
**Likely follow-ups:** 1) *Good AUC?* Context-dependent; above 0.5 and beating a simple baseline. 2) *Does it pick the threshold?* No.
**Common mistakes:** Calling AUC "accuracy"; thinking 0.5 means 50% accurate.

### Q37 ⭐⭐ 🟢 Which single metric would you not report alone for a rare-event model, and what would you add to it?
**Asked at:** commonly asked (no company-specific report found); the accuracy paradox is a staple of prep lists (unverified).
**What the interviewer is checking:** That you spot the accuracy trap and name what to add.
**Say this in the interview:** "Accuracy. With a rare event, predicting 'no event' is already highly accurate. I would add recall and precision for the rare class, plus the baseline."
**Explain simply:**
- If 5% leave, "nobody leaves" is 95% accurate and useless.
- Add **recall** (how many real events we catch) and **precision** (how many alarms are real), or F1 as a combined number.
- Show the confusion matrix counts so people see the numbers.
**Worked example (concept questions):** 1,000 employees, 50 leave. "No one leaves": accuracy 0.95, recall 0.00. The real model from Q35: accuracy 0.96, recall 0.18, precision 0.90. Accuracy barely moved; recall tells the story.
**Alternative / pitfalls:** PR-AUC or lift can also help (Q79, Q68).
**Likely follow-ups:** 1) *Why not F1 alone?* It hides the precision-recall balance. 2) *What if the event is not rare?* Accuracy is fine as one of several.
**Common mistakes:** Reporting accuracy alone; reporting recall alone.

### Q38 ⭐⭐ 🟢 What does 'test-set performance' mean, and why do we report metrics on it rather than on training data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know a model can memorise training data.
**Say this in the interview:** "Test-set performance is how the model does on rows it never saw while learning. Training scores are too optimistic because the model can memorise the training rows, while the business cares about new employees."
**Explain simply:**
- We split data: the **training set** teaches the model; the **test set** is kept aside as a fair exam.
- **Overfitting** means learning the noise in training data, so training scores look great and test scores are worse.
- Test performance estimates how the model will behave on future data.
- Do not tune the model repeatedly against the test set, or it stops being a fair exam.
**Worked example (concept questions):** Unrestricted decision tree on 500 synthetic rows (`make_classification(n_samples=500, n_features=10, n_informative=5, flip_y=0.1, random_state=42)`, 70/30 split with random_state 42, `DecisionTreeClassifier(random_state=42)`): training accuracy 1.00, test accuracy 0.75. Reporting 1.00 would mislead the manager.
**Alternative / pitfalls:** Use cross-validation for a steadier estimate (Q54). Tuning decisions should use a separate validation set.
**Likely follow-ups:** 1) *Typical split?* Often 70-80% train, 20-30% test. 2) *What if test is small?* Results are noisy (Q59).
**Common mistakes:** Quoting training accuracy; peeking at the test set repeatedly.

### Q39 ⭐⭐ 🟢 What is the difference between a metric (like recall) and a loss function used when a model is trained?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the model learns from a smooth loss but we judge it with business-friendly metrics.
**Say this in the interview:** "The loss function is what the training algorithm minimises while learning. A metric is what I use to judge the finished model for the business. They are often different."
**Explain simply:**
- **Loss function:** a number the computer lowers step by step (for logistic regression, log loss; for linear regression, squared error). It must be smooth so the maths works.
- **Metric:** a measure we report to people: recall, precision, RMSE.
- Recall cannot be minimised directly because it is a count-based step function, not smooth.
- A model can have a low loss and still have a poor recall at your chosen threshold.
**Worked example (concept questions):** Four employees, true labels 1, 0, 1, 0. Model A scores 0.6, 0.4, 0.9, 0.1; model B scores 0.99, 0.01, 0.99, 0.01. Both have recall 1.0 at threshold 0.5, yet log loss is 0.31 for A and 0.01 for B. The loss rewards confidence; the metric only sees the cut-off decision.
**Alternative / pitfalls:** You can adjust training weights or the threshold so the model serves the metric you care about.
**Likely follow-ups:** 1) *Examples of loss?* Squared error, log loss. 2) *Can the same thing be both?* MSE can be both.
**Common mistakes:** Treating them as the same thing; assuming a lower loss always means higher recall.

### Q40 ⭐⭐ 🟢 If a regression model's RMSE is 8 and the target is monthly salary in thousands of rupees, how do you read it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you attach units and judge size against the target's scale.
**Say this in the interview:** "RMSE is in the target's units, so 8 means predictions are typically off by about Rs 8,000 a month, with bigger misses weighing more. Whether that is good depends on typical salary and on a baseline."
**Explain simply:**
- Units: thousands of rupees, so 8 means Rs 8,000.
- It is a typical error size, not a maximum; some rows may be off by much more.
- Judge it against the salary level: Rs 8,000 on a Rs 20,000 salary is large; on Rs 2,00,000 it is small.
- Compare with a baseline model (predict the average salary) and with MAE.
**Worked example (concept questions):** If average salary is Rs 40,000 (40 in the target units), RMSE 8 is about 20% of the average. If the baseline RMSE (always the mean) were 15, the model cut typical error from Rs 15,000 to Rs 8,000.
**Alternative / pitfalls:** The 8 and the salary range here are exercise inputs; no mean salary is given in the question, so the "good or bad" call needs more context.
**Likely follow-ups:** 1) *Does 8 mean 8% error?* No, it is in the units, not percent. 2) *How to compare across targets?* Use relative measures like MAPE or a baseline ratio.
**Common mistakes:** Reading it as a percent; forgetting the thousands.

### Q41 ⭐⭐ 🟡 Hiring screen: a resume-screening model shortlists 50 of 500 applicants; 30 shortlisted are actually suitable, and 60 suitable applicants exist in total. What are its precision and recall?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you pick the right denominators from the story.
**Say this in the interview:** "Precision is 30 out of the 50 shortlisted, 0.60. Recall is 30 out of the 60 suitable people, 0.50. So the shortlist is 60% clean but it misses half of the suitable applicants."
**Explain simply:**
- TP = 30 (shortlisted and suitable), FP = 20 (shortlisted, not suitable), FN = 30 (suitable but not shortlisted).
- Precision: of those flagged, how many are right. Recall: of those who matter, how many we found.
**Code (what you write in the interview):**
```python
shortlisted = 50
suitable_shortlisted = 30
suitable_total = 60

precision = suitable_shortlisted / shortlisted
recall = suitable_shortlisted / suitable_total
print("Precision:", precision)
print("Recall:", recall)
```
**Output:**
```
Precision: 0.6
Recall: 0.5
```
**What it means:** Tell the manager: "Six in ten shortlisted people are suitable, but half of the suitable applicants never reach the shortlist." Check the rejected group for hidden bias.
**Alternative / pitfalls:** A random shortlist of 50 would have precision about 12% (60 / 500), so this model is useful but not a replacement for human review.
**Likely follow-ups:** 1) *Accuracy?* TN = 440 - 20 = 420, so accuracy = (30 + 420) / 500 = 0.90. 2) *How to raise recall?* Lower the threshold; precision may drop.
**Common mistakes:** Using 500 as the denominator; swapping precision and recall.

### Q42 ⭐⭐ 🟡 Threshold calculation: using the scores below, compute precision and recall at a threshold of 0.5 and again at 0.3.
Scores: 0.90, 0.70, 0.55, 0.40, 0.35, 0.10
Actual (1 = leaves): 1, 1, 0, 1, 0, 0
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can apply a threshold by hand and count TP, FP, FN.
**Say this in the interview:** "At 0.5 I flag three people: two right, one wrong, one leaver missed, so precision and recall are both 0.67. At 0.3 I flag five: three right, two wrong, no leaver missed, so precision 0.60 and recall 1.0."
**Explain simply:**
- Flag when score is at or above the threshold.
- At 0.5: flagged 0.90 (leaver), 0.70 (leaver), 0.55 (stayer). TP 2, FP 1, FN 1 (the 0.40 leaver).
- At 0.3: also flagged 0.40 (leaver) and 0.35 (stayer). TP 3, FP 2, FN 0.
- Lower threshold: recall up (0.67 to 1.0), precision down (0.67 to 0.60).
**Code (what you write in the interview):**
```python
import numpy as np
from sklearn.metrics import precision_score, recall_score

scores = np.array([0.90, 0.70, 0.55, 0.40, 0.35, 0.10])
actual = np.array([1, 1, 0, 1, 0, 0])

for threshold in [0.5, 0.3]:
    predicted = (scores >= threshold).astype(int)
    precision = precision_score(actual, predicted)
    recall = recall_score(actual, predicted)
    print(threshold, "precision:", round(precision, 2), "recall:", round(recall, 2))
```
**Output:**
```
0.5 precision: 0.67 recall: 0.67
0.3 precision: 0.6 recall: 1.0
```
**What it means:** With only six rows these numbers are very unstable; they show the mechanics, not a reliable model.
**Alternative / pitfalls:** Whether a score exactly equal to the threshold counts as flagged is a choice; sklearn's `predict` uses the model's own cut-off, so state yours.
**Likely follow-ups:** 1) *Which threshold?* Depends on cost (Q25). 2) *At 0.6?* Two flagged, both right: precision 1.0, recall 0.67.
**Common mistakes:** Counting the 0.40 leaver as caught at 0.5; using "greater than" and "at least" inconsistently.

### Q43 ⭐⭐ 🟡 Outliers: the errors of a sales model on five months are shown below. Compute MAE and RMSE and explain why they differ.
Absolute errors: 2, 2, 2, 2, 12
**Asked at:** commonly asked (no company-specific report found); "high RMSE relative to MAE signals outliers" appears in regression Q&A (unverified).
**What the interviewer is checking:** That you know RMSE punishes big misses more than MAE.
**Say this in the interview:** "MAE is 4 and RMSE is about 5.66. RMSE is higher because squaring makes the one big miss of 12 count much more. A gap between the two is a sign of an occasional large error."
**Explain simply:**
- MAE = (2 + 2 + 2 + 2 + 12) / 5 = 4.
- RMSE = square root of (4 + 4 + 4 + 4 + 144) / 5 = square root of 32 = 5.66.
- If all five errors were equal, MAE and RMSE would be the same. The bigger the gap, the more uneven the errors.
- Without the outlier month the RMSE would be exactly 2.
**Code (what you write in the interview):**
```python
import numpy as np

errors = np.array([2, 2, 2, 2, 12])

mae = np.mean(np.abs(errors))
rmse = np.sqrt(np.mean(errors ** 2))
print("MAE:", mae)
print("RMSE:", round(rmse, 2))
```
**Output:**
```
MAE: 4.0
RMSE: 5.66
```
**What it means:** The model is usually off by about 2 but has one bad month of 12. Investigate that month (a festival, a stock-out, a data error) before trusting either figure.
**Alternative / pitfalls:** Report both; choose RMSE if big misses are especially costly, MAE for a robust "typical" error.
**Likely follow-ups:** 1) *Would you delete the outlier?* Not without understanding it. 2) *Units?* Both in sales units.
**Common mistakes:** Saying RMSE is always the better metric; ignoring the outlier month.

### Q44 ⭐⭐ 🟡 Baseline vs model: compute the RMSE of the model and of a baseline that always predicts the mean of the actuals. Is the model worthwhile?
Actual: 10, 20, 30, 40
Model predictions: 12, 18, 33, 38
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you compare against a simple benchmark and say its limits.
**Say this in the interview:** "The model's RMSE is 2.29. The baseline predicts the mean, 25, every time, and has RMSE 11.18. The model's error is about a fifth of the baseline, so it looks worthwhile, but four points is a tiny sample."
**Explain simply:**
- Mean of the actuals = 25, so baseline errors are 15, 5, 5, 15 (mean squared 125, RMSE 11.18).
- Model errors are 2, 2, 3, 2 (mean squared 5.25, RMSE 2.29).
- 2.29 / 11.18 is about 0.2: the model removes roughly 80% of the baseline error.
**Code (what you write in the interview):**
```python
import numpy as np

actual = np.array([10, 20, 30, 40])
model_predictions = np.array([12, 18, 33, 38])

# baseline: always predict the average of the actuals
baseline_predictions = np.full(4, actual.mean())

model_rmse = np.sqrt(np.mean((actual - model_predictions) ** 2))
baseline_rmse = np.sqrt(np.mean((actual - baseline_predictions) ** 2))
print("Model RMSE:", round(model_rmse, 2))
print("Baseline RMSE:", round(baseline_rmse, 2))
```
**Output:**
```
Model RMSE: 2.29
Baseline RMSE: 11.18
```
**What it means:** The model clearly beats the guess-the-average baseline. Report both numbers side by side.
**Alternative / pitfalls:** The baseline here uses the test actuals' own mean, which is slightly generous to the baseline; in practice use the training mean. Four rows is far too few to trust.
**Likely follow-ups:** 1) *A better baseline?* Last period's value for time series. 2) *Is 2.29 good on its own?* Only relative to the baseline and the scale (10 to 40).
**Common mistakes:** Quoting only the model's RMSE; forgetting the baseline can be beaten trivially on small data.

### Q45 ⭐⭐ 🟡 Precision at top K: HR can only call 20 employees. The model's top 20 contains 14 actual leavers, and 40 employees leave in total. What are precision@20 and recall@20?
**Asked at:** commonly asked (no company-specific report found); top-K style prompts are a judgement-based gap-fill, not tied to a named company.
**What the interviewer is checking:** Whether you can turn a capacity limit into precision and recall, and read both correctly.
**Say this in the interview:** "Precision@20 is 14 out of 20, so 70%. Recall@20 is 14 out of 40, so 35%. HR's calls are well spent, but they can only reach about a third of the people who will leave."
**Explain simply:**
- **Precision@K** = of the K people the model ranked highest, how many really left: 14 / 20 = 0.70.
- **Recall@K** = of all people who really left, how many are inside the top K: 14 / 40 = 0.35.
- K is set by capacity (20 calls), not by the model. Recall is capped by K: even a perfect model could reach at most 20 / 40 = 50% recall here.
**Worked example (concept questions):** Precision 0.70 means 6 of the 20 calls go to people who were not going to leave. The 26 leavers outside the top 20 are the missed ones (40 - 14 = 26).
**Alternative / pitfalls:** Compare precision@20 with the base rate of leaving, not with zero. If the overall leaving rate were 10%, 70% is a big improvement; if it were 65%, it is hardly any.
**Likely follow-ups:** 1) *How do you raise recall@K?* A better ranking, or a larger K (more budget). 2) *Why not accuracy?* Accuracy mixes in the thousands of people nobody calls.
**Common mistakes:** Dividing 14 by 40 for precision (swapping the two); forgetting that the cap on K limits recall.

### Q46 ⭐⭐ 🟡 Model comparison: Model A has precision 0.30 and recall 0.90; Model B has precision 0.80 and recall 0.60. Which would you choose for a retention campaign with a small budget, and which if the company can afford to call everyone at risk?
**Asked at:** commonly asked (no company-specific report found); precision-versus-recall choice by cost is a standard theme in the prep-site lists in the sources file (unverified).
**What the interviewer is checking:** That you choose the metric from the business cost, not from habit.
**Say this in the interview:** "With a small budget I pick Model B, because most of the people it flags are real leavers, so little money is wasted. If we can contact everyone at risk, I pick Model A, because it catches 90% of leavers and wasted calls are cheap."
**Explain simply:**
- **Precision** = of the people flagged, how many really leave. **Recall** = of the people who really leave, how many we flag.
- Small budget: every wasted call is a cost, and we cannot call many people anyway, so we want high precision (B: 0.80).
- Large budget: a missed leaver is the expensive mistake, so we want high recall (A: 0.90).
- F1 (a single blended score) is A = 2 x 0.30 x 0.90 / 1.20 = 0.45 and B = 2 x 0.80 x 0.60 / 1.40 = 0.69. It favours B, but F1 ignores your budget, so the business situation decides.
**Alternative / pitfalls:** Check that both models use the same threshold rule; a model can look like A or B just by moving the cut-off. Compare them with precision@K at the number you can actually call.
**Likely follow-ups:** 1) *What if cost of a missed leaver is known?* Put rupees on each error and pick the lower total cost. 2) *Is Model A bad?* No, it is right when calls are cheap and leavers are costly.
**Common mistakes:** Always choosing the higher F1; ignoring the budget; thinking one model is "better" in every situation.

### Q47 ⭐⭐ 🟡 Multi-class reading: given the confusion matrix below (rows = actual, columns = predicted), what is the overall accuracy and the precision for class B?
Classes A, B, C
Row A: 50, 5, 5
Row B: 10, 30, 10
Row C: 0, 10, 40
**Asked at:** commonly asked (no company-specific report found); hand-computing metrics from a confusion matrix is a common fresher exercise in the prep sources (unverified).
**What the interviewer is checking:** That you can read a matrix: diagonal for correct, columns for precision, rows for recall.
**Say this in the interview:** "Accuracy is the diagonal over the total: 120 out of 160, so 75%. Precision for B is 30 out of the 45 predicted as B, about 67%."
**Explain simply:**
- Rows are the real class, columns are what the model said. The **diagonal** (50, 30, 40) holds the correct calls.
- Accuracy = (50 + 30 + 40) / 160 = 120 / 160 = 0.75. (Row totals: A 60, B 50, C 50.)
- **Precision for B** = correct B predictions / everything predicted B. Column B is 5 + 30 + 10 = 45, so 30 / 45 = 0.667.
- Check yourself: precision uses the column, recall uses the row (B recall = 30 / 50 = 0.60).
**Alternative / pitfalls:** In sklearn, `confusion_matrix` also puts actual in rows and predicted in columns by default; some tools flip it, so always check the axis labels.
**Likely follow-ups:** 1) *Which class is weakest?* B, with recall 0.60. 2) *Where do B's errors go?* 10 to A and 10 to C.
**Common mistakes:** Dividing by the row total for precision; adding the whole matrix wrongly; mixing up rows and columns.

### Q48 ⭐⭐ 🟡 What is the difference between macro-averaged and weighted-averaged recall in a classification report, and which would you use for an imbalanced set of ticket categories?
**Asked at:** commonly asked (no company-specific report found); averaging in multi-class reports is a standard topic in the per-class metrics prep material (unverified).
**What the interviewer is checking:** That you know averages hide or reveal rare classes.
**Say this in the interview:** "Macro recall averages the per-class recalls equally, so a rare class counts as much as a big one. Weighted recall weights each class by how many rows it has. For imbalanced ticket categories I report macro and the per-class numbers, because weighted can hide a rare category that is failing."
**Explain simply:**
- **Recall** for a class = of the tickets that really belong to it, how many the model found.
- **Macro** = simple average of the class recalls. **Weighted** = average weighted by class size (support).
- Weighted recall equals overall accuracy, so big classes dominate it.
**Worked example (concept questions):** 100 tickets: 80 payroll, 15 leave, 5 legal. Class recalls: payroll 0.95, leave 0.80, legal 0.00. Macro recall = (0.95 + 0.80 + 0.00) / 3 = 0.58. Weighted recall = (80 x 0.95 + 15 x 0.80 + 5 x 0.00) / 100 = 0.88. Weighted looks fine; macro exposes that no legal ticket is found.
**Alternative / pitfalls:** If the business only cares about the big classes, weighted is fair, but say so. Always show the per-class table too.
**Likely follow-ups:** 1) *What is micro?* It pools all predictions; for recall across all classes it equals accuracy. 2) *Which column holds support?* The `support` column of `classification_report`.
**Common mistakes:** Reporting only weighted recall on imbalanced data; thinking macro is always better.

### Q49 ⭐⭐ 🟡 Code reading: what does this print, and what is wrong with the idea of using it as the only evaluation?
```python
from sklearn.metrics import accuracy_score
import numpy as np
y_true = np.array([0,0,0,0,0,0,0,0,1,1])
y_pred = np.zeros(10)
print(accuracy_score(y_true, y_pred))
```
**Asked at:** commonly asked (no company-specific report found); "is 93% accuracy good" style questions appear across the prep sources (unverified).
**What the interviewer is checking:** Whether you spot the accuracy trap on imbalanced data.
**Say this in the interview:** "It prints 0.8. The model predicts 0 for everyone, so it never finds a single positive, yet accuracy looks decent. Accuracy alone hides that."
**Explain simply:**
- `y_pred` is all zeros: the model says "nobody" every time. It is right on the 8 zeros and wrong on the 2 ones: 8 / 10 = 0.8.
- This is the **accuracy paradox**: when one class is rare, doing nothing scores high.
- Recall for the positive class here is 0 out of 2 = 0, and precision is undefined (no positives predicted).
**Output:** `0.8` (run on the installed scikit-learn 1.9.1).
**What it means:** 80% accuracy equals the share of zeros in the data. Report recall and precision for the rare class alongside the confusion matrix.
**Alternative / pitfalls:** Compare any model with this "always the majority class" baseline.
**Likely follow-ups:** 1) *What would you add?* Confusion matrix, recall, precision. 2) *Why is precision undefined?* There are no predicted positives, so the division is 0 / 0.
**Common mistakes:** Saying 0.8 is "good"; not noticing that `np.zeros(10)` is a float array of predictions.

### Q50 ⭐⭐ 🟡 Code task: write short code that applies a 0.3 threshold to model.predict_proba(X_test)[:, 1] and prints the confusion matrix and recall.
**Asked at:** commonly asked (no company-specific report found); threshold choice is a standard theme in the evaluation prep sources (unverified).
**What the interviewer is checking:** That you know `predict` uses 0.5 by default and that you can set your own cut-off.
**Say this in the interview:** "I take the probability of the positive class, turn it into 1 or 0 with my own threshold, then compare with the real answers. Lowering the threshold catches more leavers but flags more people wrongly."
**Explain simply:**
- `predict_proba(...)[:, 1]` gives each person's probability of the positive class (for example, leaving).
- A **threshold** is the cut-off: probability at or above 0.3 becomes a flag.
- Lowering from 0.5 to 0.3 usually raises recall and lowers precision.
**Sample data:** Synthetic: `make_classification(n_samples=1000, n_features=20, n_informative=2, n_redundant=2, weights=[0.85], flip_y=0.01, random_state=42)`, about 15% positive, `train_test_split(test_size=0.25, stratify=y, random_state=42)` (`stratify=y` keeps the same share of positives in train and test), `LogisticRegression()`. `model`, `X_test`, `y_test` are assumed already created.
**Code (what you write in the interview):**
```python
from sklearn.metrics import confusion_matrix, recall_score

# probability of the positive class, then cut at 0.3
probabilities = model.predict_proba(X_test)[:, 1]
y_pred = (probabilities >= 0.3).astype(int)

print(confusion_matrix(y_test, y_pred))
print(recall_score(y_test, y_pred))
```
**Output:** (depends on the data and seed 42)
```
[[202  10]
 [ 10  28]]
0.7368421052631579
```
**What it means:** Rows are actual (0, 1), columns are predicted. 28 of 38 real positives are caught: recall 0.74. At the default 0.5 threshold the same model caught 24 of 38 (recall 0.63), so the lower threshold found 4 more, at the cost of 2 more false alarms (10 versus 8).
**Alternative / pitfalls:** Choose the threshold on a validation set or with cross-validation, not by peeking at the test set.
**Likely follow-ups:** 1) *How do you pick 0.3?* From the cost of a miss versus a false alarm. 2) *Does the model change?* No, only the decision rule.
**Common mistakes:** Using `predict_proba(X_test)` without `[:, 1]`; using `>` instead of `>=` without noticing; tuning the threshold on the test set.

### Q51 ⭐⭐ 🟡 Code task: use sklearn to report RMSE and MAE for y_test and y_pred, and say which function names you would use in a recent scikit-learn version.
**Asked at:** commonly asked (no company-specific report found); RMSE and MAE are core regression-metric questions in the sources (unverified).
**What the interviewer is checking:** That you can compute error metrics and know the current function names.
**Say this in the interview:** "I use `root_mean_squared_error` and `mean_absolute_error`. The old trick of `mean_squared_error(..., squared=False)` no longer works in current versions, so I would not rely on it."
**Explain simply:**
- **MAE** (mean absolute error) = average size of the miss, in the same units as the target.
- **RMSE** (root mean squared error) = squares the misses, averages, then square-roots. It punishes big misses more.
- Verified here on scikit-learn 1.9.1: `root_mean_squared_error` exists, and `mean_squared_error(..., squared=False)` raises `TypeError: unexpected keyword argument 'squared'`. For older versions, use `mean_squared_error(...) ** 0.5` (works everywhere); which version first added or removed what is from memory, unverified.
**Sample data:** Salaries (Rs): actual 30000, 45000, 52000, 38000, 60000; predicted 33000, 43000, 50000, 41000, 55000.
**Code (what you write in the interview):**
```python
from sklearn.metrics import root_mean_squared_error, mean_absolute_error

y_test = [30000, 45000, 52000, 38000, 60000]
y_pred = [33000, 43000, 50000, 41000, 55000]

print("RMSE:", root_mean_squared_error(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
```
**Output:**
```
RMSE: 3193.743884534262
MAE: 3000.0
```
**What it means:** On average the model is about Rs 3,000 off; RMSE is a bit higher (Rs 3,194) because the Rs 5,000 miss counts extra. Report both in rupees.
**Alternative / pitfalls:** `mean_squared_error(y_test, y_pred) ** 0.5` gives the same RMSE and works in any version.
**Likely follow-ups:** 1) *Which is bigger, RMSE or MAE?* RMSE is always at least MAE. 2) *When prefer MAE?* When outliers should not dominate.
**Common mistakes:** Swapping the order of `y_true` and `y_pred` (fine for these two metrics, wrong for others); reporting MSE as if it were in rupees.

### Q52 ⭐⭐ 🟡 Code reading: what does cross_val_score(model, X, y, cv=5, scoring='recall') return, and why choose recall as the scoring?
**Asked at:** commonly asked (no company-specific report found); cross-validation scoring appears in the fresher ML lists in the sources (unverified).
**What the interviewer is checking:** That you know it returns one score per fold, and you choose the score for the business goal.
**Say this in the interview:** "It returns an array of five recall values, one for each fold. I choose recall when missing a real case is the costly error, such as an employee who leaves without warning."
**Explain simply:**
- The data is split into 5 parts (**folds**). Five times, the model trains on 4 parts and is scored on the held-out part.
- You get five numbers; the mean tells the typical performance, the spread tells how stable it is.
- Default scoring for a classifier would be accuracy, which misleads on imbalanced data. `scoring='recall'` swaps in recall for the positive class.
**Sample data:** Synthetic data as in Q50 (`make_classification(n_samples=1000, n_features=20, n_informative=2, n_redundant=2, weights=[0.85], flip_y=0.01, random_state=42)`, about 15% positive), `LogisticRegression()`; `model`, `X`, `y` assumed already created.
**Code (what you write in the interview):**
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring="recall")
print(scores)
print(scores.mean(), scores.std())
```
**Output:** (depends on the synthetic data, seed 42)
```
[0.6        0.7        0.63333333 0.58064516 0.64516129]
0.6318279569892472 0.04113433798091872
```
**What it means:** Typical recall is about 0.63, with folds ranging from 0.58 to 0.70. Report "about 63%, give or take 4 points".
**Alternative / pitfalls:** For classifiers `cv=5` uses stratified folds (same class mix in each fold), which matters for rare classes. Precision and recall should both be checked, so use `cross_validate` with several scorings if needed.
**Likely follow-ups:** 1) *Why not just one split?* See Q54. 2) *Recall of which class?* The positive class (label 1) by default.
**Common mistakes:** Quoting only one fold; forgetting that high recall can come with terrible precision.

### Q53 ⭐⭐ 🟡 MAPE calculation: compute the MAPE for the four predictions below and say when MAPE becomes unreliable.
Actual: 200, 100, 50, 400
Predicted: 180, 110, 60, 380
**Asked at:** commonly asked (no company-specific report found); MAPE appears in the regression KPI Q&A in the sources (unverified, and the search noted some quiz answers there are inconsistent).
**What the interviewer is checking:** That you can compute MAPE by hand and know it breaks near zero.
**Say this in the interview:** "MAPE is the average of the percentage errors: here 11.25%. It becomes unreliable when actual values are zero or very small, because dividing by them explodes the percentage."
**Explain simply:**
- **MAPE** (mean absolute percentage error) = average of |actual - predicted| / actual.
- Errors: 20/200 = 10%, 10/100 = 10%, 10/50 = 20%, 20/400 = 5%. Average = 45 / 4 = 11.25%.
- Problem 1: zero actuals make it undefined or infinite. Problem 2: tiny actuals give huge percentages (actual 2, predicted 12 is a 500% error). Problem 3: it punishes over-prediction more than under-prediction (an under-forecast can never exceed 100%).
**Sample data:** The four pairs above.
**Code (what you write in the interview):**
```python
import numpy as np

actual = np.array([200, 100, 50, 400])
predicted = np.array([180, 110, 60, 380])

mape = np.mean(np.abs(actual - predicted) / actual) * 100
print(mape)
```
**Output:**
```
11.25
```
**What it means:** The forecasts are off by about 11% on average. Check: sklearn's `mean_absolute_percentage_error` returned 0.1125 (a fraction, not a percent) on the same data.
**Worked example (concept questions):** Actuals 2, 100, 150 with predictions 12, 100, 150: MAE is only 3.3 but MAPE is 166.7%, driven by one tiny actual.
**Alternative / pitfalls:** For small or zero values use MAE, RMSE or a weighted MAPE (total absolute error divided by total actual).
**Likely follow-ups:** 1) *Percent or fraction?* sklearn gives a fraction; multiply by 100. 2) *Alternative?* WAPE or MAE.
**Common mistakes:** Dividing by the predicted value instead of the actual; ignoring zeros in the actuals.

### Q54 ⭐⭐ 🟡 What is k-fold cross-validation, and why does it give a steadier estimate of a metric than a single train/test split?
**Asked at:** commonly asked (no company-specific report found); cross-validation is a staple of the fresher ML lists in the sources (unverified).
**What the interviewer is checking:** That you understand a single split is luck-dependent.
**Say this in the interview:** "I split the data into k parts, train on k minus 1 and test on the remaining part, and rotate until every part has been the test set once. Then I average. Every row is used for testing exactly once, so one lucky or unlucky split does not decide the result."
**Explain simply:**
- **Fold** = one of the k parts. With k = 5, each fold is 20% of the data.
- A single split gives one number that depends on which rows landed in the test set, especially when the data is small or the positive class is rare.
- Averaging k numbers smooths out that luck, and the spread (standard deviation) tells you how unstable the estimate is.
- Cost: you train the model k times.
**Worked example (concept questions):** Same model, same data, five different single splits (random_state 0 to 4) gave recall 0.66, 0.64, 0.57, 0.43 and 0.73 (synthetic data from Q52, plain random splits with test size 25%). A reader who saw only seed 3 would think the model was poor; one who saw seed 4 would think it was great. 5-fold cross-validation on the same data gave a mean of 0.63 with a spread of 0.04.
**Alternative / pitfalls:** Use stratified folds for imbalanced classes, and time-ordered splits for forecasting (never shuffle the future into the past). Keep a final hold-out set for the last check; preprocessing must be fitted inside each fold to avoid leakage.
**Likely follow-ups:** 1) *What k?* 5 or 10 are common. 2) *Is CV used to train the final model?* No; it estimates performance, then you fit on all training data.
**Common mistakes:** Calling it "5 different models"; scaling the whole dataset before splitting; reporting only the best fold.

### Q55 ⭐⭐ 🟡 A model has R-squared 0.90 but its RMSE is Rs 40,000 on salaries that range from Rs 30,000 to Rs 60,000. How do you explain this to a manager, and what do you report?
**Asked at:** commonly asked (no company-specific report found); the R-squared versus RMSE reporting angle is a gap-fill, not tied to a named company.
**What the interviewer is checking:** Whether you notice the numbers cannot both be right, and that you report error in rupees.
**Say this in the interview:** "These two numbers do not fit together. If salaries only range from 30,000 to 60,000, an error of 40,000 is worse than guessing the average. I would recheck the calculation, and report RMSE in rupees alongside R-squared."
**Explain simply:**
- **R-squared** = share of the ups and downs in salary that the model explains (1 is perfect, 0 is no better than always guessing the average). **RMSE** = typical miss, in rupees.
- Premise problem: salaries spread over a Rs 30,000 range have a standard deviation of roughly Rs 9,000 to Rs 10,000 (Rs 10,000 for an evenly spread example with 7 values from 30,000 to 60,000). A model with R-squared 0.90 would then have RMSE about Rs 3,000 (0.316 x 10,000). With RMSE Rs 40,000, R-squared would be strongly negative (about -15).
- Likely causes: R-squared measured in-sample and RMSE out-of-sample, different datasets or units (monthly versus annual), or an outlier-driven RMSE.
- So I solve the sensible version: after fixing it, report RMSE (and MAE) in rupees on test data, say what share of the salary range it is, and give R-squared only as a supporting number.
**Alternative / pitfalls:** A high R-squared can still mean a large rupee error when the target spreads widely; a small R-squared can be fine for a noisy target. Managers act on rupees.
**Likely follow-ups:** 1) *Can R-squared be negative?* Yes, on test data when the model is worse than the average. 2) *What would you check first?* Units and which data each number came from.
**Common mistakes:** Presenting R-squared alone; accepting an impossible pair of numbers without checking.

### Q56 ⭐⭐ 🟡 What is the precision-recall trade-off, and what do you do when HR wants both to be high?
**Asked at:** commonly asked (no company-specific report found); precision versus recall is the most repeated theme in the sources, including a prep-site Tiger Analytics fraud-detection prompt (anonymous report, unverified).
**What the interviewer is checking:** That you know both cannot be pushed up freely and can explain the choice with costs.
**Say this in the interview:** "Raising the threshold flags fewer people, which makes the flags more accurate (precision up) but misses more leavers (recall down); lowering it does the opposite. When HR wants both high, I ask what each mistake costs, show them the trade-off at a few thresholds, and look for a better model or better features rather than a magic setting."
**Explain simply:**
- **Precision** = of those flagged, how many really leave. **Recall** = of those who leave, how many are flagged.
- A strict model flags only the sure cases (high precision, low recall). A loose model flags many (high recall, low precision).
- To get both up, the model must separate leavers from stayers better: more or cleaner features, more data, a better model type. Changing only the threshold just moves along the curve.
- Practical answer: pick the operating point from capacity and cost (for example, "we can call 50 people a week"), and report precision and recall at that point.
**Alternative / pitfalls:** F1 balances the two but hides the cost difference. A precision-recall curve shows the whole trade-off at once.
**Likely follow-ups:** 1) *What if HR insists?* Show the table of thresholds and let them pick. 2) *Is there a single number?* F1, with caveats.
**Common mistakes:** Promising both at 95%; changing the threshold and calling it a "better model".

### Q57 ⭐⭐ 🟡 Always-positive model: 10% of customers churn, and a model flags every customer as a churner. What are its recall, precision and F1?
**Asked at:** commonly asked (no company-specific report found); the sources note one prep page had a wrong F1 for this case, so the arithmetic here is computed directly.
**What the interviewer is checking:** That you can compute the three numbers and see why recall alone is not enough.
**Say this in the interview:** "Recall is 100%, because every churner is flagged. Precision is 10%, the churn rate, because 90% of the flags are wrong. F1 is about 0.18."
**Explain simply:**
- Take 1,000 customers: 100 churn, 900 do not. The model flags all 1,000.
- True positives = 100, false positives = 900, false negatives = 0.
- **Recall** = 100 / 100 = 1.0. **Precision** = 100 / 1,000 = 0.10.
- **F1** (the harmonic mean, a blend that is dragged down by the smaller value) = 2 x 0.10 x 1.0 / (0.10 + 1.0) = 0.2 / 1.1 = 0.1818.
**What it means:** Precision for a flag-everyone model equals the base rate, so it is the baseline any real model must beat. A recall of 100% means nothing on its own.
**Alternative / pitfalls:** Do not average precision and recall (that gives 0.55, which looks much better than F1 0.18).
**Likely follow-ups:** 1) *Accuracy of this model?* 10%. 2) *Opposite model, flags nobody?* Recall 0, accuracy 90%.
**Common mistakes:** Quoting F1 as 0.55 (a simple average); saying precision is undefined.

### Q58 ⭐⭐ 🟡 A random guesser flags employees as 'will leave' with probability 0.2 in a dataset where 20% really leave. What precision and recall do you expect, and why does this matter as a benchmark?
**Asked at:** commonly asked (no company-specific report found); benchmark thinking is a gap-fill, not tied to a named company.
**What the interviewer is checking:** Whether you know the baseline a model must beat.
**Say this in the interview:** "A random guesser gets precision of about 20% and recall of about 20%, the base rate in both cases. Any model I build should clearly beat that."
**Explain simply:**
- Guessing is independent of the truth, so the flagged group has the same 20% leavers as everyone: precision = 0.2.
- Also 20% of the real leavers happen to be flagged: recall = 0.2.
- Check by 100,000-row simulation (numpy `default_rng(42)`, 20% truly leave, 20% guessed): precision 0.202, recall 0.204. (Accuracy for the guesser is 0.68 = 0.2 x 0.2 + 0.8 x 0.8, which looks decent but is meaningless.)
- Benchmark: precision of a real model should be compared with the base rate (0.2), not with 0 or 0.5. A model with precision 0.30 is a 1.5x improvement; one with 0.80 is 4x.
**Alternative / pitfalls:** Also compare with simple rules (for example "tenure under one year") and the majority-class baseline; a fancy model that cannot beat a rule is not worth deploying.
**Likely follow-ups:** 1) *What is lift?* Precision divided by the base rate. 2) *Does flag rate change precision?* No, for a random guesser precision stays at the base rate.
**Common mistakes:** Expecting 50% for a random guess; comparing precision with zero.

### Q59 ⭐⭐ 🟡 Your test set has only 20 rows and accuracy is 85%. Why should you be cautious, and what would you do?
**Asked at:** commonly asked (no company-specific report found); small-sample caution is a gap-fill; the sources raise a "small minority count caveat" (unverified).
**What the interviewer is checking:** Whether you understand sampling uncertainty in a metric.
**Say this in the interview:** "85% of 20 is 17 correct. One more or fewer correct answer moves accuracy by 5 points, and the plausible range is huge, roughly 64% to 95%. I would use cross-validation or get more data, and report the range, not the single number."
**Explain simply:**
- Each row is worth 5 percentage points. The result can swing a lot by luck.
- A 95% **confidence interval** (a range that would capture the true accuracy in most repeats of the study) for 17 out of 20 is about 64% to 95% by the Wilson method (the exact method gives 62% to 97%).
- If only a few rows are positives (say 3 leavers), recall is based on three people and means almost nothing.
- Also check the class mix: 85% might equal the share of the majority class.
**What to do:** Use stratified k-fold cross-validation on all labelled data, repeat it with different seeds, collect more labelled rows if possible, and report with the interval and the counts.
**Likely follow-ups:** 1) *How many rows is enough?* Enough positives for the metric to be stable; hundreds is better than dozens. 2) *Bootstrap?* Resampling the test rows to see the spread of the metric.
**Common mistakes:** Quoting 85% as a fact; tuning the model to this 20-row set.

### Q60 ⭐⭐ 🟡 Code reading: how do you build a confusion matrix from two pandas columns with pd.crosstab, and what do the rows and columns represent?
**Asked at:** commonly asked (no company-specific report found); a gap-fill for analysts who prefer pandas to sklearn.
**What the interviewer is checking:** That you can build and read a confusion matrix in pandas, and know which axis is which.
**Say this in the interview:** "`pd.crosstab(df['actual'], df['predicted'])` counts how often each pair occurs. The first argument becomes the rows (actual) and the second the columns (predicted). The diagonal is the correct calls."
**Explain simply:**
- A **confusion matrix** is a table of counts: real outcome against predicted outcome.
- With `crosstab`, the first column you pass gives the row labels and the second gives the column labels, so the order matters.
- Add `rownames` and `colnames` so a reader knows which is which.
**Sample data:** 8 employees with columns `actual` and `predicted`.
**Code (what you write in the interview):**
```python
import pandas as pd

df = pd.DataFrame({
    "actual":    ["Left", "Stay", "Left", "Stay", "Stay", "Left", "Stay", "Stay"],
    "predicted": ["Left", "Stay", "Stay", "Stay", "Left", "Left", "Stay", "Stay"],
})

print(pd.crosstab(df["actual"], df["predicted"],
                  rownames=["Actual"], colnames=["Predicted"]))
```
**Output:**
```
Predicted  Left  Stay
Actual               
Left          2     1
Stay          1     4
```
**What it means:** 2 leavers caught (true positives), 1 leaver missed, 1 stayer wrongly flagged, 4 stayers correctly left alone. Recall = 2/3, precision = 2/3, accuracy = 6/8.
**Alternative / pitfalls:** `sklearn.metrics.confusion_matrix` gives the same counts as a bare array with no labels (rows actual, columns predicted). Crosstab drops a category that never appears; for a clean matrix make both columns categorical with the same levels.
**Likely follow-ups:** 1) *Percentages?* `normalize="index"` gives row-wise shares (recall per class). 2) *Totals?* `margins=True`.
**Common mistakes:** Swapping the arguments; forgetting the order of labels.

### Q61 ⭐⭐ 🟡 How would you read a scikit-learn classification_report for a three-class model, and which columns would you look at first?
**Asked at:** commonly asked (no company-specific report found); reading the sklearn report is a standard task in the prep sources (unverified).
**What the interviewer is checking:** That you can read per-class numbers rather than only the headline.
**Say this in the interview:** "I look at `support` first to see class sizes, then recall and precision per class for the classes I care about, then accuracy and macro average. A decent accuracy can hide one weak class."
**Explain simply:**
- Each row is one class. **precision** = of the predictions for this class, how many were right. **recall** = of the real members, how many were found. **f1-score** = a blend of the two. **support** = number of real rows in that class.
- Below the classes: **accuracy** (overall), **macro avg** (plain average over classes) and **weighted avg** (weighted by support).
- Order of reading: support, then the weakest class's recall and precision, then macro versus weighted (a big gap means a small class is doing badly).
**Worked example (concept questions):** Synthetic 100-employee example (Stay 50, Leave soon 30, Promoted 20), from `classification_report(y_true, y_pred, target_names=[...])`. It comes from this confusion matrix (rows actual, columns predicted; order Stay, Leave soon, Promoted): [[44, 4, 2], [8, 18, 4], [2, 5, 13]].
```
              precision    recall  f1-score   support

        Stay       0.81      0.88      0.85        50
  Leave soon       0.67      0.60      0.63        30
    Promoted       0.68      0.65      0.67        20

    accuracy                           0.75       100
   macro avg       0.72      0.71      0.71       100
weighted avg       0.74      0.75      0.75       100
```
Reading: overall accuracy is 75%, but "Leave soon" recall is only 0.60, so 4 in 10 future leavers are missed. If leavers are the point, that row matters more than the 75%.
**Alternative / pitfalls:** The rare class has few rows, so its numbers are shaky; see Q59. Use `zero_division=0` if a class is never predicted.
**Likely follow-ups:** 1) *Why is weighted avg recall equal to accuracy?* Support-weighted recall is the share of all rows correct. 2) *Which average for imbalance?* Macro, plus per-class (see Q48).
**Common mistakes:** Quoting accuracy only; mixing up precision and recall columns.

### Q62 ⭐⭐ 🟡 Code reading: a statsmodels OLS result is used as below. What does this measure, and why is it optimistic as a report of model quality?
```python
import numpy as np, statsmodels.api as sm
model = sm.OLS(y, sm.add_constant(X)).fit()
rmse = np.sqrt(np.mean(model.resid ** 2))
```
**Asked at:** commonly asked (no company-specific report found); the statsmodels in-sample RMSE point is a gap-fill, not tied to a named company.
**What the interviewer is checking:** That you recognise in-sample error and why it flatters the model.
**Say this in the interview:** "This is an OLS (ordinary least squares, the standard regression) fit, and the code measures the typical miss on the same rows the model was fitted on, that is, the in-sample RMSE. It is optimistic because the model was tuned to those exact rows. I would report the error on data it has not seen."
**Explain simply:**
- `model.resid` = actual minus fitted value for each training row. Squaring, averaging and square-rooting gives RMSE.
- Because OLS chooses coefficients to make these residuals as small as possible on this very data, adding more columns can only shrink the error here, even if the columns are noise.
- Illustration (synthetic: numpy `default_rng(42)`, 60 rows, 15 random feature columns of which only 3 matter, noise spread 20; first 42 rows to fit, last 18 held out): in-sample RMSE 14.2, but on the held-out rows RMSE 34.8, more than double.
- Note: this RMSE divides by n, while statsmodels' own `model.mse_resid` divides by the degrees of freedom left, so they differ slightly.
**What it means:** Report RMSE from a hold-out set or cross-validation, and say which one it is.
**Alternative / pitfalls:** Adjusted R-squared and AIC penalise extra columns, but a real hold-out check is more convincing.
**Likely follow-ups:** 1) *How to fix it?* Split first, fit on train, predict test with `model.predict(sm.add_constant(X_test))`. 2) *Is in-sample useless?* No, it is a lower bound and good for diagnosing the fit.
**Common mistakes:** Forgetting `add_constant` on the test data too; reporting training RMSE as "model accuracy".

### Q63 ⭐⭐ 🟡 What is the difference between in-sample RMSE and out-of-sample RMSE, and which one do you give to a stakeholder?
**Asked at:** commonly asked (no company-specific report found); a gap-fill that pairs with the train/test basics.
**What the interviewer is checking:** That you give the honest error, not the flattering one.
**Say this in the interview:** "In-sample RMSE is the error on the data the model learned from; out-of-sample RMSE is the error on new data. The stakeholder gets the out-of-sample number, because that is what they will experience when the model is used."
**Explain simply:**
- In-sample (training) error is almost always lower; a model can even memorise the training rows (**overfitting**: learning the noise and quirks of that data, so it does worse on new data).
- Out-of-sample (test or cross-validated) error estimates real-world performance.
- A big gap between the two warns of overfitting. In the Q62 illustration, 14.2 versus 34.8 (synthetic data, seed 42).
- For time series, "out-of-sample" means later periods than the training period.
**What it means:** Report the out-of-sample RMSE in business units (rupees, days), with MAE, and state how the test data was chosen.
**Alternative / pitfalls:** If the test set is small, use cross-validation and give a range. Never tune settings on the test set, or it stops being truly out-of-sample.
**Likely follow-ups:** 1) *What if both are high?* Underfitting; try better features. 2) *What if in-sample is tiny and out-of-sample large?* Overfitting.
**Common mistakes:** Quoting the training RMSE; peeking at the test set while tuning.

### Q64 ⭐⭐ 🟡 Which regression metric would you pick when over-predicting and under-predicting inventory carry very different costs, and how would you handle that?
**Asked at:** commonly asked (no company-specific report found); asymmetric-cost prompts appear in prep sites (a PracHub page on asymmetric costs is named in the sources, snippet only, unverified).
**What the interviewer is checking:** That you see RMSE and MAE treat both directions the same, and can add the real costs.
**Say this in the interview:** "RMSE and MAE count a 10-unit over-forecast and a 10-unit under-forecast the same. I would define a cost metric: rupees lost per unit of stock-out versus per unit of excess stock, and judge the forecast by total cost. I can also train the model to be deliberately a bit high."
**Explain simply:**
- Under-predicting demand means lost sales; over-predicting means unsold stock. If a lost sale costs Rs 50 and extra unit costs Rs 5, the errors are not equal.
- Write the cost as: 50 x (units short) + 5 x (units extra), then average it. This is a custom **asymmetric loss**.
- Example (5 products, demand 100, 120, 80, 150, 90; forecast 110, 100, 85, 130, 95): total shortfall 40 units, total excess 20 units, cost = 50 x 40 + 5 x 20 = Rs 2,100 (Rs 420 per product). MAE for the same forecast is 12 units and says nothing about which side is worse.
- Handling: **quantile loss** (for example `GradientBoostingRegressor(loss="quantile", alpha=0.9)`, which aims the forecast at the 90th percentile of demand; I confirmed it runs on the installed version) pushes forecasts upward when shortages are costlier. Or add a safety-stock margin on top of a normal forecast.
**Alternative / pitfalls:** Check bias too: mean of (forecast - actual). Cost numbers must come from finance, not from guesses.
**Likely follow-ups:** 1) *Which direction does alpha 0.9 favour?* Over-forecasting (avoiding shortage). 2) *How do you choose between models?* Lower total cost on held-out data.
**Common mistakes:** Picking RMSE by default; forgetting to evaluate on unseen data.

### Q65 ⭐⭐ 🔴 Macro recall: using the 3-class matrix below (rows = actual), calculate the macro-averaged recall.
Row A: 50, 5, 5
Row B: 10, 30, 10
Row C: 0, 10, 40
**Asked at:** commonly asked (no company-specific report found); hand calculation from a multi-class matrix, as in Q47.
**What the interviewer is checking:** That you calculate recall per row, then average.
**Say this in the interview:** "Recall per class is the diagonal over the row total: A 50 of 60, B 30 of 50, C 40 of 50. Macro recall is the simple average, about 0.744."
**Explain simply:**
- Recall asks: of the real members of this class, how many did the model catch? That uses rows (real classes).
- A: 50 / 60 = 0.833. B: 30 / 50 = 0.600. C: 40 / 50 = 0.800.
- Macro = (0.833 + 0.600 + 0.800) / 3 = 2.233 / 3 = 0.744.
- Weighted recall uses the row sizes (60, 50, 50) and equals accuracy, 120 / 160 = 0.75. The two are close here because the classes are nearly equal in size.
**Alternative / pitfalls:** Dividing by column totals gives precision, not recall. Macro recall is also called balanced accuracy.
**Likely follow-ups:** 1) *Which class is weakest?* B at 0.60. 2) *Why report macro?* Every class counts equally.
**Common mistakes:** Using column totals; averaging without noticing the class sizes differ.

### Q66 ⭐⭐ 🔴 Your attrition model shows 96% recall on the test set, which is far above anything in the earlier versions. What would you suspect, and what would you check before reporting it?
**Asked at:** commonly asked (no company-specific report found); the "too good to be true" check is standard practice; the sources link attrition work to recall-versus-precision trade-offs (unverified).
**What the interviewer is checking:** Whether your first reaction to a great number is suspicion, and whether you know leakage.
**Say this in the interview:** "A jump that large makes me suspect data leakage first: a column that reveals the answer, such as one filled in only after someone resigns. I would check the features, how I split the data, the precision, and whether the test set is separate and large enough, before telling anyone."
**Explain simply:**
- **Leakage** = information in the features that would not be available at prediction time (for example, `exit_interview_done`, `notice_period_days`, `final_settlement_date`).
- Checks: (1) list features by importance and look at the top ones; (2) ask "would I know this before the person resigns?"; (3) confirm the split happened before any scaling, balancing or feature building, and no employee appears in both train and test; (4) look at precision, since flagging everyone gives high recall too (see Q57); (5) confirm the number with cross-validation and a later time period; (6) check how many leavers the test set holds.
- Illustration (the synthetic data of Q84, seed 42): a model using tenure and overtime had recall 0.68 and precision 0.31. Adding a leaky column `exit_interview_done` lifted recall to 0.90 and precision to 0.92, a "brilliant" model that is useless on live employees, because the column does not exist yet for people who are still working.
**What it means:** Do not report 96% until the features and the split are checked. Report the honest, leak-free number with the date range it covers.
**Alternative / pitfalls:** Other causes: duplicate rows across train and test, a threshold set very low, tuning on the test set, a target definition that includes people who already resigned.
**Likely follow-ups:** 1) *How do you prevent leakage?* Build features only from data available at the prediction date. 2) *What would you report meanwhile?* "Promising, under validation."
**Common mistakes:** Celebrating the number; looking only at recall; fixing the model before finding the cause.

### Q67 ⭐⭐ 🔴 A model's recall is 60% overall, but 80% for men and 40% for women in the test data. How do you investigate and report this, and what are the risks of acting on the model?
**Asked at:** commonly asked (no company-specific report found); a fairness-check gap-fill question, not tied to a named company.
**What the interviewer is checking:** That you never stop at one overall number and that you can raise a fairness problem calmly, with evidence.
**Say this in the interview:** "An overall 60% hides a big gap: the model finds 80% of the men who leave but only 40% of the women. I would confirm the gap with counts, look for the cause, and tell the manager the model should not drive decisions until it is understood."
**Explain simply:**
- **Recall** = of the people who really left, the share the model caught. Check it per group (a "subgroup" or "slice") and also show how many people are in each group, because small groups give shaky numbers.
- Check the other side too: precision and the share of each group flagged. Here women are flagged less often, so they receive fewer retention conversations.
- Look for causes: fewer women leavers in the training data, features that describe men's careers better, or labels that differ by group (for example resignations recorded differently).
- Risk of acting on it: the retention budget goes mostly to men, women who are about to leave are missed, and the company could face fairness or legal questions (check with HR legal; do not rely on this answer for law).
- Do not "fix" it by dropping the gender column and calling it done: other columns (part-time, job family) can still carry the same signal.
**Sample data:** Made-up test results: 500 men and 500 women, 100 real leavers in each group.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.metrics import recall_score, precision_score

# test results: 500 men and 500 women, 100 real leavers in each group
rows = (
    [("Men", 1, 1)] * 80 + [("Men", 1, 0)] * 20 + [("Men", 0, 1)] * 30 + [("Men", 0, 0)] * 370
    + [("Women", 1, 1)] * 40 + [("Women", 1, 0)] * 60 + [("Women", 0, 1)] * 10 + [("Women", 0, 0)] * 390
)
results = pd.DataFrame(rows, columns=["gender", "actual", "predicted"])

print("Overall recall:", recall_score(results["actual"], results["predicted"]))
for group, part in results.groupby("gender"):
    recall = recall_score(part["actual"], part["predicted"])
    precision = precision_score(part["actual"], part["predicted"])
    flagged_share = part["predicted"].mean()
    print(f"{group}: recall {recall:.2f}, precision {precision:.2f}, flagged {flagged_share:.0%}")
```
**Output:**
```
Overall recall: 0.6
Men: recall 0.80, precision 0.73, flagged 22%
Women: recall 0.40, precision 0.80, flagged 10%
```
**What it means:** The model is cautious with women: when it flags one it is usually right (80%), but it flags too few, so 60 of 100 women leavers are missed. Report the per-group table, not just 60%.
**Alternative / pitfalls:** Report gaps with group sizes and an uncertainty range (see Q86); with small groups a 40-point gap can still be partly chance. Fixes include more data for the weaker group, group-specific thresholds (a policy decision, not only a technical one), or not using the model for that group.
**Likely follow-ups:** 1) *Would you remove gender from the model?* Not enough alone; proxies remain, and you still need gender in the evaluation to measure the gap. 2) *Who decides what to do?* HR leadership with legal advice; the analyst supplies the evidence.
**Common mistakes:** Reporting only the overall metric; ignoring group sizes; assuming removing a column removes bias; hiding the finding.

### Q68 ⭐ 🟢 What is a lift or gain chart, and how does it help an HR or marketing team decide how many people to contact?
**Asked at:** commonly asked (no company-specific report found); lift/gain appears in the churn and marketing-model topics of prep lists (unverified).
**What the interviewer is checking:** Whether you can turn a model's scores into a practical "how many people do we contact" decision.
**Say this in the interview:** "Sort people from highest to lowest model score and cut them into ten equal groups, called deciles. A gain chart shows what share of all leavers you reach as you contact more groups; lift says how many times better than random each group is."
**Explain simply:**
- **Decile** = one tenth of the people. Decile 1 holds those with the highest scores.
- **Lift** of a decile = its leaver rate divided by the overall leaver rate. Lift 3.5 means 3.5 times better than picking at random.
- **Cumulative gain** = share of all leavers found so far. Contacting the top 20% of people reaching, say, 57% of leavers is the picture a manager understands.
- Choose how far to go by cost: stop when the next group's lift falls near 1 (no better than random) or when the budget ends.
**Sample data:** Leavers found in each group of 100 employees (1,000 employees, 100 leavers; made up).
**Code (what you write in the interview):**
```python
import pandas as pd

# leavers found in each group of 100 employees, from highest model score (decile 1) to lowest
leavers_per_decile = [35, 22, 14, 10, 7, 5, 3, 2, 1, 1]
deciles = pd.DataFrame({"decile": range(1, 11), "leavers": leavers_per_decile})
total_leavers = deciles["leavers"].sum()
overall_rate = total_leavers / 1000
deciles["lift"] = (deciles["leavers"] / 100) / overall_rate
deciles["cumulative_gain"] = deciles["leavers"].cumsum() / total_leavers
print(deciles.round(2).to_string(index=False))
```
**Output:**
```
 decile  leavers  lift  cumulative_gain
      1       35   3.5             0.35
      2       22   2.2             0.57
      3       14   1.4             0.71
      4       10   1.0             0.81
      5        7   0.7             0.88
      6        5   0.5             0.93
      7        3   0.3             0.96
      8        2   0.2             0.98
      9        1   0.1             0.99
     10        1   0.1             1.00
```
**What it means:** Talking to the top 30% of people reaches 71% of leavers; after decile 4 the lift is 1.0, so extra contacts are no better than random. Tell the manager: "contact the top 3 to 4 groups, then compare the cost of each extra conversation with what a saved employee is worth."
**Alternative / pitfalls:** Build the table on test data, never training data. Lift depends on the base rate, so compare lift across models only on the same population.
**Likely follow-ups:** 1) *Gain chart vs ROC curve?* Both rank people; gain is framed in contacts and is easier for business people. 2) *What if budget covers 10% only?* Use decile 1: lift 3.5.
**Common mistakes:** Calling lift "accuracy"; computing it on training data; forgetting to sort by score.

### Q69 ⭐ 🟢 What is Cohen's kappa in plain words, and why might it be used when labels are imbalanced?
**Asked at:** commonly asked (no company-specific report found); kappa is a rarer metric named in some evaluation lists (unverified).
**What the interviewer is checking:** Whether you understand "agreement beyond chance".
**Say this in the interview:** "Kappa measures how much a model and the truth agree after removing the agreement you would get by luck. Zero means no better than chance; one means perfect. With 95% stayers, a lazy 'everyone stays' model gets 95% accuracy but kappa zero."
**Explain simply:**
- Accuracy counts matches only. If one class is huge, many matches happen by luck.
- Kappa = (observed agreement minus chance agreement) divided by (1 minus chance agreement). It also scores two human raters against each other.
- Rough reading (a common rule of thumb, not a law): below 0.2 weak, 0.4 to 0.6 moderate, above 0.8 strong.
- It is useful for imbalanced labels and for checking AI or human labelling (Q77).
**Sample data:** 1,000 employees, 50 leavers. A lazy model says "stays" for all; a real model catches 30 of 50 leavers and wrongly flags 40 stayers.
**Code (what you write in the interview):**
```python
from sklearn.metrics import cohen_kappa_score, accuracy_score

# 1,000 employees: 50 leavers. A lazy model says "stays" for everyone.
actual = [1] * 50 + [0] * 950
lazy_model = [0] * 1000
# a real model: catches 30 of 50 leavers, wrongly flags 40 stayers
real_model = [1] * 30 + [0] * 20 + [1] * 40 + [0] * 910
for name, predicted in [("lazy", lazy_model), ("real", real_model)]:
    print(name, "accuracy", accuracy_score(actual, predicted), "kappa", round(cohen_kappa_score(actual, predicted), 2))
```
**Output:**
```
lazy accuracy 0.95 kappa 0.0
real accuracy 0.94 kappa 0.47
```
**What it means:** Accuracy ranks the useless model above the useful one; kappa correctly gives the lazy model zero and the real one a moderate 0.47.
**Alternative / pitfalls:** MCC (Q72), recall and precision say similar things. Kappa depends on class balance, so do not compare it across datasets with different balance.
**Likely follow-ups:** 1) *Can kappa be negative?* Yes, worse than chance. 2) *Weighted kappa?* For ordered labels such as 1 to 5 ratings; bigger misses cost more.
**Common mistakes:** Treating 0.47 like 47% accuracy; using kappa without also looking at recall and precision.

### Q70 ⭐ 🟡 Lift calculation: of 1,000 employees, 100 leave. The top decile of model scores (100 people) contains 35 leavers. What is the lift for that decile?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you divide the group's rate by the overall rate, not the counts.
**Say this in the interview:** "Overall 10% leave. In the top decile 35% leave. Lift is 35% divided by 10%, which is 3.5: the top-scored people are 3.5 times more likely to leave than a random group."
**Explain simply:**
- Overall rate = 100 / 1,000 = 10%.
- Top decile rate = 35 / 100 = 35%.
- Lift = 35% / 10% = 3.5. A random group has lift 1.
- Another route: random picking would find 10 leavers in 100 people; the model found 35, and 35 / 10 = 3.5.
**Code (what you write in the interview):**
```python
total_employees = 1000
total_leavers = 100
top_decile_size = 100
leavers_in_top_decile = 35
overall_leaver_rate = total_leavers / total_employees
top_decile_leaver_rate = leavers_in_top_decile / top_decile_size
lift = top_decile_leaver_rate / overall_leaver_rate
print("Overall rate:", overall_leaver_rate)
print("Top decile rate:", top_decile_leaver_rate)
print("Lift:", round(lift, 1))
```
**Output:**
```
Overall rate: 0.1
Top decile rate: 0.35
Lift: 3.5
```
**What it means:** Contacting only the top 10% of people reaches 35% of all leavers, 3.5 times more efficient than random calls. Maximum possible lift here is 10 (all 100 people in the decile leave).
**Alternative / pitfalls:** The trap is quoting 35% as the lift or comparing 35 with 100. Lift on a tiny test set is noisy.
**Likely follow-ups:** 1) *What is lift of 1?* No better than random. 2) *Highest possible lift?* 1 divided by the base rate (10 here).
**Common mistakes:** Dividing 35 by 100 and stopping; mixing up lift with recall (35% of leavers caught).

### Q71 ⭐ 🟡 Why can ROC-AUC look flattering on a heavily imbalanced problem, and what would you look at instead?
**Asked at:** commonly asked; ROC-AUC vs PR-AUC and F1 for imbalanced problems appears in prep-site lists and in one forum report of a Flipkart Data Scientist 2 interview (snippet level, unverified).
**What the interviewer is checking:** Whether you know ROC-AUC includes the huge number of true negatives.
**Say this in the interview:** "ROC-AUC uses the false positive rate, which divides by the many negatives, so a few hundred false alarms still look like a small rate. Precision-recall AUC and precision at the cut-off I would actually use show the real cost of those alarms."
**Explain simply:**
- **ROC-AUC** = chance the model scores a random leaver above a random stayer (0.5 is guessing, 1 is perfect).
- **False positive rate** = false alarms / all real stayers. With 99% stayers, 5% of them is still hundreds of people.
- **Precision** = of those flagged, how many really left. It is not diluted by the many stayers.
- Look at **PR-AUC** (average precision), precision and recall at the chosen threshold, and top-K precision.
**Sample data:** Synthetic 6,000-person test set with only 60 leavers (1%), logistic regression, seed 42.
**Code (what you write in the interview):**
```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score
import numpy as np

X, y = make_classification(n_samples=20000, n_features=10, n_informative=4, weights=[0.99], flip_y=0.0, class_sep=1.4, n_clusters_per_class=1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
scores = model.predict_proba(X_test)[:, 1]
print("positives in test:", y_test.sum(), "of", len(y_test))
print("ROC-AUC:", round(roc_auc_score(y_test, scores), 3))
print("PR-AUC (average precision):", round(average_precision_score(y_test, scores), 3))
print("PR-AUC of random guessing = share of positives:", round(y_test.mean(), 3))
# flag the 120 highest-scored people and see how many are real leavers
top = np.argsort(scores)[::-1][:120]
print("precision in top 120:", round(y_test[top].mean(), 2))
```
**Output:**
```
positives in test: 60 of 6000
ROC-AUC: 0.905
PR-AUC (average precision): 0.513
PR-AUC of random guessing = share of positives: 0.01
precision in top 120: 0.29
```
**What it means:** 0.905 sounds excellent, yet flagging 120 people yields only about 29% real leavers. PR-AUC (0.513, against 0.01 for guessing) tells the more honest story.
**Alternative / pitfalls:** ROC-AUC is still fine for ranking and for balanced data. Output depends on the seed.
**Likely follow-ups:** 1) *Is ROC-AUC wrong then?* No, it answers a different question. 2) *What would you tell HR?* "Of the people we flag, about 3 in 10 will really leave."
**Common mistakes:** Quoting AUC alone; forgetting the base rate is the PR-AUC baseline.

### Q72 ⭐ 🟡 What is the Matthews correlation coefficient (MCC), and why do some practitioners prefer it to F1?
**Asked at:** commonly asked (no company-specific report found); MCC appears in imbalanced-data lists (unverified).
**What the interviewer is checking:** That you know F1 ignores true negatives and can be fooled by which class you call "positive".
**Say this in the interview:** "MCC is a single score from minus one to plus one that uses all four boxes of the confusion matrix. F1 ignores the true negatives, so a model that says 'positive' for everyone can still score a high F1; MCC would give it zero."
**Explain simply:**
- **Confusion matrix** boxes: true positives, false positives, false negatives, true negatives.
- MCC is basically the correlation between predicted and actual labels: 1 perfect, 0 no better than guessing, minus 1 always wrong.
- **F1** = balance of precision and recall; it never looks at true negatives.
- MCC is only high if the model does well on both classes.
**Sample data:** 1,000 employees, 950 stayed (label 1 in this example), 50 left. One model says "stayed" for all; another is genuinely good.
**Code (what you write in the interview):**
```python
from sklearn.metrics import f1_score, matthews_corrcoef

# 1,000 employees: 950 stayed (label 1 here), 50 left (label 0)
actual = [1] * 950 + [0] * 50
say_stayed_always = [1] * 1000
print("F1:", round(f1_score(actual, say_stayed_always), 3))
print("MCC:", matthews_corrcoef(actual, say_stayed_always))
# a model that separates the groups: 900 of 950 right, 40 of 50 right
good_model = [1] * 900 + [0] * 50 + [0] * 40 + [1] * 10
print("good model F1:", round(f1_score(actual, good_model), 3), "MCC:", round(matthews_corrcoef(actual, good_model), 3))
```
**Output:**
```
F1: 0.974
MCC: 0.0
good model F1: 0.968 MCC: 0.569
```
**What it means:** F1 ranks the useless model above the good one; MCC gives the useless model 0 and the good model 0.57.
**Alternative / pitfalls:** If "positive" means the rare class (leavers), F1 is less fooled, so the criticism depends on how you define positive. MCC is harder to explain to non-technical people; use it in the appendix.
**Likely follow-ups:** 1) *Can MCC be negative?* Yes, down to minus 1. 2) *Why not accuracy?* It rewards the lazy model (95%).
**Common mistakes:** Believing F1 is always bad; treating MCC as a percentage.

### Q73 ⭐ 🟡 What is log loss (cross-entropy), and how does it differ from accuracy as a metric?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know accuracy judges the yes/no answer while log loss judges the probability.
**Say this in the interview:** "Log loss punishes a model for being confidently wrong. Accuracy only counts right or wrong after a cut-off, while log loss reads the actual probability, so lower is better and a hesitant right answer scores worse than a confident right one."
**Explain simply:**
- For each person, log loss looks at the probability given to the true outcome: a true leaver given 0.9 costs little; given 0.01 costs a lot.
- It is averaged over everyone. 0 is perfect; higher is worse.
- Accuracy cannot tell 0.51 from 0.99; log loss can.
- It matters when probabilities are used (risk scores) and when comparing models during training.
**Sample data:** 5 employees (1 = left): 2 leavers, 3 stayers; three models give different probabilities.
**Code (what you write in the interview):**
```python
from sklearn.metrics import log_loss, accuracy_score

# 5 employees: 1 = left, 0 = stayed
actual = [1, 0, 0, 1, 0]
models = {
    "confident and right": [0.9, 0.1, 0.1, 0.8, 0.1],
    "hesitant but right": [0.55, 0.45, 0.45, 0.55, 0.45],
    "confident and wrong once": [0.99, 0.01, 0.01, 0.01, 0.01],
}
for name, probabilities in models.items():
    # turn each probability into a yes/no using a 0.5 cut-off
    predicted = [1 if p >= 0.5 else 0 for p in probabilities]
    print(f"{name}: accuracy {accuracy_score(actual, predicted):.1f}, log loss {log_loss(actual, probabilities):.3f}")
```
**Output:**
```
confident and right: accuracy 1.0, log loss 0.129
hesitant but right: accuracy 1.0, log loss 0.598
confident and wrong once: accuracy 0.8, log loss 0.929
```
**What it means:** The first two models have the same accuracy but very different log loss; the confident, one-time-wrong model is punished hardest.
**Alternative / pitfalls:** Log loss is hard to explain to managers; use it to compare models internally and report recall/precision outward. It is sensitive to a few extreme wrong probabilities.
**Likely follow-ups:** 1) *Can log loss be above 1?* Yes. 2) *Same as cross-entropy?* Yes, for two classes.
**Common mistakes:** Thinking higher is better; computing it from yes/no predictions instead of probabilities.

### Q74 ⭐ 🟡 What is calibration of predicted probabilities, and why does it matter if HR will use a '70% risk' number?
**Asked at:** commonly asked; calibration appears in one forum report of a Flipkart Data Scientist 2 interview (snippet level, unverified); gap-fill for analyst roles.
**What the interviewer is checking:** Whether you know a score is not automatically a true probability.
**Say this in the interview:** "A model is calibrated when people it calls 70% risk really do leave about 70% of the time. A model can rank people well and still give numbers that are too high or too low, so before HR quotes a percentage I would check it against what actually happened."
**Explain simply:**
- **Calibration** = promised probability matches the real share.
- Ranking (who is riskier) and calibration (how risky) are different skills.
- Check by grouping people into risk bands and comparing the average quoted risk with the real share who left (a calibration table or curve).
- Common cause: using `class_weight="balanced"` or resampling to find more leavers inflates probabilities. Fix with recalibration (for example `CalibratedClassifierCV`, from memory, check the sklearn docs).
**Sample data:** Synthetic 5,000 rows, about 10% leave; logistic regression with `class_weight="balanced"`; seed 42.
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.calibration import calibration_curve

# about 10% of the people leave
X, y = make_classification(n_samples=5000, n_features=10, n_informative=5, weights=[0.9], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, stratify=y, random_state=42)
# class_weight="balanced" helps find leavers but inflates the probabilities
model = LogisticRegression(class_weight="balanced", max_iter=1000).fit(X_train, y_train)
risk_scores = model.predict_proba(X_test)[:, 1]
# put people into 5 risk bands; compare the risk we quote with the share who really left
actual_share, promised_risk = calibration_curve(y_test, risk_scores, n_bins=5, strategy="quantile")
print(pd.DataFrame({"quoted_risk": promised_risk.round(2), "actual_share_left": actual_share.round(2)}))
```
**Output:**
```
   quoted_risk  actual_share_left
0         0.04               0.00
1         0.14               0.02
2         0.29               0.03
3         0.49               0.10
4         0.78               0.37
```
**What it means:** The top band is quoted at 78% risk but only 37% really left. The ranking is fine; the percentage must not be shown to HR as it is.
**Alternative / pitfalls:** Tell HR "high / medium / low band" with real observed rates instead of raw percentages. Bands with few people are noisy.
**Likely follow-ups:** 1) *Which metric measures it?* Brier score or log loss (Q73). 2) *Does calibration change recall?* The ranking stays the same; only the numbers move.
**Common mistakes:** Treating a score as a probability; checking calibration on training data.

### Q75 ⭐ 🟡 What is adjusted R-squared, and why would it be preferred to R-squared when comparing models with different numbers of features?
**Asked at:** commonly asked (no company-specific report found); adjusted R-squared is listed in regression-metric Q&A pages (unverified).
**What the interviewer is checking:** Whether you know plain R-squared can only go up when you add columns.
**Say this in the interview:** "R-squared is the share of the variation the model explains, but it never falls when you add a feature, even a useless one. Adjusted R-squared charges a penalty for each extra feature, so it only rises if the new feature really helps."
**Explain simply:**
- **R-squared** = share of the ups and downs in the outcome (for example salary) that the model explains; 1 is perfect.
- **Feature** = an input column.
- Adjusted R-squared lowers the score as features increase, relative to the number of rows.
- Use it to compare models with different feature counts; for prediction quality, also check held-out error (RMSE or MAE).
**Sample data:** 40 employees (made up): salary depends on experience and grade; five more columns are pure random noise.
**Code (what you write in the interview):**
```python
import numpy as np, pandas as pd
import statsmodels.api as sm

rng = np.random.default_rng(42)
n = 40
employees = pd.DataFrame({"experience_years": rng.uniform(1, 15, n), "grade": rng.integers(1, 6, n)})
employees["salary"] = 20000 + 2500 * employees["experience_years"] + 4000 * employees["grade"] + rng.normal(0, 6000, n)
# five columns of pure random noise that mean nothing
for i in range(1, 6):
    employees[f"noise_{i}"] = rng.normal(size=n)
useful = ["experience_years", "grade"]
with_noise = useful + [f"noise_{i}" for i in range(1, 6)]
for name, columns in [("2 useful features", useful), ("2 useful + 5 noise", with_noise)]:
    fit = sm.OLS(employees["salary"], sm.add_constant(employees[columns])).fit()
    print(f"{name}: R2 {fit.rsquared:.3f}, adjusted R2 {fit.rsquared_adj:.3f}")
```
**Output:**
```
2 useful features: R2 0.885, adjusted R2 0.878
2 useful + 5 noise: R2 0.895, adjusted R2 0.872
```
**What it means:** Adding five meaningless columns raised R-squared (0.885 to 0.895) but lowered adjusted R-squared (0.878 to 0.872), correctly signalling they add nothing.
**Alternative / pitfalls:** Cross-validated error is a better guide for prediction. Adjusted R-squared still measures fit on the training data.
**Likely follow-ups:** 1) *Can adjusted R-squared be negative?* Yes. 2) *Does high R-squared mean a good model?* No; check residuals and held-out error.
**Common mistakes:** Picking the model with the highest R-squared regardless of feature count.

### Q76 ⭐ 🟡 Why is MAE minimised by the median and RMSE by the mean, and does that matter to an analyst?
**Asked at:** commonly asked (no company-specific report found); MAE vs RMSE is a common regression-metric question (prep lists, unverified).
**What the interviewer is checking:** Whether you understand how squaring makes big errors count much more.
**Say this in the interview:** "If I must give one number for everybody, the best guess for the smallest average absolute miss is the median; for the smallest average squared miss it is the mean. So RMSE chases the average and is pulled by outliers, while MAE is more typical-case."
**Explain simply:**
- **MAE** = average size of the miss. Every unit of error counts the same, so moving your guess past the middle person always costs more than it gains: the best spot is the median.
- **RMSE** = square the misses, average, take the root. Big misses count extra, so the guess is pulled toward extreme values: the best spot is the mean.
- It matters for choosing the metric: when large errors are very costly (for example payroll forecasts) use RMSE; when you care about the typical error and have outliers, MAE (or report both). RMSE much greater than MAE signals outliers.
**Sample data:** Monthly overtime hours for 7 employees: 4, 5, 6, 6, 7, 8, 40.
**Code (what you write in the interview):**
```python
import numpy as np

# monthly overtime hours for 7 employees; one extreme value
overtime_hours = np.array([4, 5, 6, 6, 7, 8, 40])
for guess in [overtime_hours.mean(), np.median(overtime_hours)]:
    mae = np.abs(overtime_hours - guess).mean()
    rmse = np.sqrt(((overtime_hours - guess) ** 2).mean())
    print(f"guess {guess:.2f}: MAE {mae:.2f}, RMSE {rmse:.2f}")
```
**Output:**
```
guess 10.86: MAE 8.33, RMSE 11.96
guess 6.00: MAE 5.71, RMSE 12.91
```
**What it means:** Guessing the median (6) gives the lowest MAE (5.71); guessing the mean (10.86) gives the lowest RMSE (11.96). The 40-hour outlier drags the mean up.
**Alternative / pitfalls:** The lowest-MAE guess is the median only for a constant guess; for a model it means MAE-trained models aim at the conditional median. Report which metric you used and why.
**Likely follow-ups:** 1) *Which would you show a manager?* MAE, since it is in plain units (hours). 2) *Why is RMSE never below MAE?* Squaring and rooting weights big errors more.
**Common mistakes:** Comparing MAE of one model with RMSE of another.

### Q77 ⭐ 🟡 You use ChatGPT or Claude to tag 1,000 survey comments as positive, neutral or negative. How would you evaluate how good the tagging is using a human-labelled sample of 100?
**Asked at:** commonly asked (no company-specific report found); gap-fill for AI-tool questions.
**What the interviewer is checking:** That you treat AI output as something to test against human labels, with honest uncertainty.
**Say this in the interview:** "I would draw a random sample of 100 comments, have a person label them blind, compare with the AI's labels using a confusion matrix, accuracy, kappa and per-class recall, and quote a range because 100 is small. Only then would I trust the other 900."
**Explain simply:**
- Sample **randomly** (or by group, so rare topics are included) and let the human label **before** seeing the AI tag.
- Use a **confusion matrix** (humans in rows, AI in columns) to see which mistakes happen, often neutral vs the others.
- Report agreement, kappa (agreement beyond chance), and per-class precision and recall.
- Give an uncertainty range (95% confidence interval): with 100 comments the accuracy is only known to about plus or minus 8 points.
- Privacy: do not paste real, identifiable employee comments into a public AI tool; check company policy (from memory, unverified; confirm with IT or legal). Re-check after any prompt change.
**Sample data:** 100 comments labelled by a person and the AI (made-up counts).
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.metrics import accuracy_score, cohen_kappa_score, classification_report
from statsmodels.stats.proportion import proportion_confint

# 100 comments labelled by a person and by the AI (made-up counts)
pairs = (
    [("positive", "positive")] * 34 + [("positive", "neutral")] * 5 + [("positive", "negative")] * 1
    + [("neutral", "neutral")] * 17 + [("neutral", "positive")] * 5 + [("neutral", "negative")] * 8
    + [("negative", "negative")] * 25 + [("negative", "neutral")] * 5
)
sample = pd.DataFrame(pairs, columns=["human_label", "ai_label"])
print(len(sample), "comments")
print(pd.crosstab(sample["human_label"], sample["ai_label"]))
agreement = accuracy_score(sample["human_label"], sample["ai_label"])
low, high = proportion_confint((sample["human_label"] == sample["ai_label"]).sum(), len(sample), method="wilson")
print(f"Agreement {agreement:.0%}, 95% range {low:.0%} to {high:.0%}")
print("Kappa:", round(cohen_kappa_score(sample["human_label"], sample["ai_label"]), 2))
print(classification_report(sample["human_label"], sample["ai_label"]))
```
**Output:**
```
100 comments
ai_label     negative  neutral  positive
human_label                             
negative           25        5         0
neutral             8       17         5
positive            1        5        34
Agreement 76%, 95% range 67% to 83%
Kappa: 0.64
              precision    recall  f1-score   support

    negative       0.74      0.83      0.78        30
     neutral       0.63      0.57      0.60        30
    positive       0.87      0.85      0.86        40

    accuracy                           0.76       100
   macro avg       0.75      0.75      0.75       100
weighted avg       0.76      0.76      0.76       100
```
**What it means:** The AI agrees with the human on 76% of comments (true value likely 67% to 83%). Neutral is the weak class (recall 0.57). Report: "good for overall mood trends, not reliable for individual comments; neutral needs review."
**Alternative / pitfalls:** Have two humans label and measure their agreement first; the AI cannot be expected to beat human-human agreement. Tag results can change between runs and model versions.
**Likely follow-ups:** 1) *Would you fix it?* Improve the prompt with clear definitions and examples, then re-test on a fresh sample. 2) *Is 100 enough?* Enough for a rough view, not for fine class-level claims.
**Common mistakes:** Judging by a few examples that look right; using the same sample to tune the prompt and to evaluate it.

### Q78 ⭐ 🟡 Employee data contains personal details. What do you have to consider before using a real employee confusion matrix or predictions in a public tool or an AI assistant?
**Asked at:** commonly asked (no company-specific report found); gap-fill for AI-tool and HR-data questions.
**What the interviewer is checking:** That you protect personal data by default and know the safe alternatives.
**Say this in the interview:** "A confusion matrix of counts is usually low risk, but row-level predictions linked to named employees are personal data, and a public AI tool may store or reuse what I paste. I would use aggregated or synthetic data, follow company policy, and ask IT or legal if unsure."
**Explain simply:** (principles only; laws and tool terms are from memory, unverified: confirm with your company's IT, data protection officer or legal team)
- **Personal data** includes names, IDs, and also combinations (small department, age, gender) that can identify someone. Predictions like "likely to resign" are sensitive.
- Aggregated counts are safer, but small cells (for example 2 women in a team) can still reveal individuals.
- Public tools may keep or learn from inputs depending on settings and plans; an approved company tool with agreed data terms is different. Check the provider's terms.
- Laws such as India's DPDP Act or GDPR can require a lawful purpose, minimal data and care with sharing; a legal team decides what applies.
- Safer practice: remove identifiers, use made-up or summarised data, ask the AI for method help rather than pasting data, get approval first.
**Worked example (concept questions):** Instead of pasting 500 rows with names and risk scores, paste: "I have a confusion matrix with TP=40, FN=60, FP=10, TN=390. Explain precision and recall for an HR audience." No person is identifiable.
**Alternative / pitfalls:** The model's predictions about people can themselves be unfair or wrong; also consider who sees them and how they are used (never as the only basis for a decision about a person).
**Likely follow-ups:** 1) *Is anonymised data always safe?* No; combinations can re-identify. 2) *What if your company has an enterprise AI tool?* Still follow policy and get approval.
**Common mistakes:** Pasting a spreadsheet "just to get the chart quickly"; assuming deleting the name column is enough.

### Q79 ⭐ 🟡 When would you choose PR-AUC over ROC-AUC, and how do you explain the choice in one sentence?
**Asked at:** commonly asked; PR-AUC vs ROC-AUC appears in prep lists and a Flipkart Data Scientist 2 forum report (snippet level; the sources disagree on details; mainstream view used).
**What the interviewer is checking:** That you tie the choice to rare positives and the cost of false alarms.
**Say this in the interview:** "I choose PR-AUC when the thing I care about is rare and the flagged people will be acted on, because it measures how many of my flagged people are real, which ROC-AUC hides behind the huge pool of easy negatives."
**Explain simply:**
- **PR-AUC** summarises precision against recall across thresholds. Its random baseline is the share of positives (1% positives gives 0.01), not 0.5.
- **ROC-AUC** is steadier and fine for balanced data or when both groups matter.
- A rare-event example: 10,000 employees, 100 leavers. A model catches 80% of leavers with a 5% false positive rate. That sounds good, but 5% of 9,900 stayers is 495 false alarms.
**Worked example (concept questions):** True positives = 80, false positives = 495, so precision = 80 / 575 = 13.9%: only about 1 in 7 flagged people leaves. ROC would show a point at (0.05, 0.80), near the top-left corner.
**Alternative / pitfalls:** PR-AUC values cannot be compared between datasets with different base rates. With only a few positives (Q86) both are noisy.
**Likely follow-ups:** 1) *Baseline PR-AUC?* The positive rate. 2) *Does ROC-AUC ever beat it?* When classes are balanced or you care equally about both classes.
**Common mistakes:** Calling PR-AUC "better" universally; forgetting its random baseline is not 0.5.

### Q80 ⭐ 🟡 Which metrics would you show on a single slide for a non-technical audience about a churn model, and which would you keep in an appendix?
**Asked at:** commonly asked (no company-specific report found); gap-fill for stakeholder-communication questions.
**What the interviewer is checking:** Whether you can translate metrics into business terms.
**Say this in the interview:** "On the slide: how many real churners we catch, how many of those we flag are right, and what that means in people or rupees against doing nothing. Everything technical, such as AUC, log loss and calibration plots, goes to the appendix."
**Explain simply:**
- **Slide**: recall in plain words ("we catch 6 of every 10 leavers"), precision ("4 of every 10 flagged actually leave"), the number of people to contact, lift or gain versus random, the comparison with the current approach, and the cost/benefit.
- **Appendix**: confusion matrix, ROC-AUC, PR-AUC, F1, MCC, kappa, calibration plot, threshold choice, per-group results (fairness) and limitations.
- Always say what the numbers rest on: test data, dates, size, and the main risk.
**Worked example (concept questions):** Test set of 1,000 people, 100 leavers; the model flags 150 and 60 of them really leave. Precision = 60 / 150 = 40%, recall = 60 / 100 = 60%. Slide line: "Contact 150 people to reach 60 of 100 leavers; a random 150 would reach about 15." (Random: 150 x 10% = 15.)
**Alternative / pitfalls:** Do not show accuracy alone (Q6, Q14), and keep the slide to 3 numbers and one recommendation. Mention uncertainty and group gaps (Q67) if they matter.
**Likely follow-ups:** 1) *Is the threshold business or technical?* Business: it trades recall against effort. 2) *What if a manager wants one number?* Recall at a fixed contact budget.
**Common mistakes:** Showing a confusion matrix without explanation; listing 10 metrics; no comparison with the do-nothing baseline.

### Q81 ⭐ 🟡 A classifier needs to hit at least 90% precision for a fraud team. How would you choose the threshold, and what happens to recall?
**Asked at:** commonly asked; precision-vs-recall trade-offs for fraud appear in prep-site and Tiger Analytics reports (anonymous, snippet level, unverified).
**What the interviewer is checking:** That you know the threshold is a choice and that raising precision usually costs recall.
**Say this in the interview:** "I would compute precision and recall at every threshold on held-out data, pick the lowest threshold that still gives at least 90% precision, because it keeps the most recall, and report the recall I give up."
**Explain simply:**
- A **threshold** is the score above which a transaction is flagged. Raising it flags fewer, more certain cases: precision tends to rise, recall tends to fall.
- `precision_recall_curve` returns the pair at each threshold (`precision` and `recall` are one longer than `thresholds`).
- Choose using validation data, then check the final number on separate test data.
- Precision at a high threshold may rest on few flagged cases, so it can be unstable.
**Sample data:** Synthetic 6,000-transaction test set, about 5% fraud, logistic regression with `class_weight="balanced"`, seed 42.
**Code (what you write in the interview):**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, precision_score, recall_score

# made-up transactions: about 5% are fraud
X, y = make_classification(n_samples=20000, n_features=10, n_informative=5, weights=[0.95], class_sep=1.0, n_clusters_per_class=1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
model = LogisticRegression(class_weight="balanced", max_iter=1000).fit(X_train, y_train)
fraud_scores = model.predict_proba(X_test)[:, 1]

# precision and recall at every possible threshold
precision, recall, thresholds = precision_recall_curve(y_test, fraud_scores)
# keep thresholds that reach 90% precision (the last precision value has no threshold, so drop it)
reaches_target = precision[:-1] >= 0.90
# the lowest such threshold keeps as much recall as possible
position = np.where(reaches_target)[0][0]
print("Chosen threshold:", round(thresholds[position], 3))
print("Precision:", round(precision[position], 3), " Recall:", round(recall[position], 3))

# compare with the default 0.5 cut-off
default_flags = fraud_scores >= 0.5
print("Default 0.5: precision", round(precision_score(y_test, default_flags), 3), " recall", round(recall_score(y_test, default_flags), 3))
```
**Output:**
```
Chosen threshold: 0.778
Precision: 0.901  Recall: 0.798
Default 0.5: precision 0.475  recall 0.876
```
**What it means:** The default 0.5 cut-off catches 88% of fraud but only 47.5% of flags are real. Moving to 0.778 reaches 90% precision and still catches about 80%: report "we give up about 8 points of recall to remove most false alarms".
**Alternative / pitfalls:** If precision never reaches 90%, say so and discuss improving the model or accepting a lower target. Picking the threshold on the test set makes the result too optimistic.
**Likely follow-ups:** 1) *What if the team wants 95%?* Recall falls further; show the curve. 2) *Could you review borderline cases manually?* Yes, a middle band sent to a human is common.
**Common mistakes:** Assuming 0.5 is special; reporting precision without recall; tuning on test data.

### Q82 ⭐ 🟡 Does a change of random_state in train_test_split change your precision and recall? What would you do about the instability?
**Asked at:** commonly asked (no company-specific report found); gap-fill question.
**What the interviewer is checking:** Whether you understand a single split gives a noisy estimate.
**Say this in the interview:** "Yes, a different random_state sends different people to the test set, so the numbers move, especially with a small or imbalanced dataset. I would not trust one split; I would use stratified cross-validation and report the average and spread."
**Explain simply:**
- `random_state` is the seed that fixes which rows go to train and test. Different seed, different rows, different scores.
- It does not mean the model is broken; it shows how uncertain the estimate is.
- Fixes: `stratify=y` (keeps the same leaver share in both parts), cross-validation, and reporting a mean with a spread.
- Keep a fixed seed (42) so your own work can be repeated, but do not shop for a lucky seed.
**Sample data:** Synthetic 600-employee attrition table, about 15% leave, logistic regression, seeds 1 to 5, test size 25%.
**Code (what you write in the interview):**
```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import precision_score, recall_score

# made-up attrition table: 600 employees, about 15% leave
X, y = make_classification(n_samples=600, n_features=8, n_informative=5, weights=[0.85], class_sep=1.0, random_state=42)
model = LogisticRegression(max_iter=1000)
for seed in [1, 2, 3, 4, 5]:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=seed)
    predicted = model.fit(X_train, y_train).predict(X_test)
    print(f"random_state={seed}: precision {precision_score(y_test, predicted):.2f}, recall {recall_score(y_test, predicted):.2f}")
# 5-fold cross-validation: every employee is tested once; report the average and spread
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
recall_scores = cross_val_score(model, X, y, cv=folds, scoring="recall")
print("5-fold recall:", recall_scores.round(2), "mean", recall_scores.mean().round(2), "std", recall_scores.std().round(2))
```
**Output:**
```
random_state=1: precision 1.00, recall 0.58
random_state=2: precision 0.79, recall 0.62
random_state=3: precision 0.89, recall 0.67
random_state=4: precision 0.86, recall 0.75
random_state=5: precision 0.86, recall 0.79
5-fold recall: [0.68 0.63 0.79 0.68 0.63] mean 0.68 std 0.06
```
**What it means:** Recall ranges from 0.58 to 0.79 across five splits, and precision from 0.79 to 1.00. Tell the manager: "recall is about 68%, give or take 6 points", not one lucky figure.
**Alternative / pitfalls:** Repeated cross-validation gives a steadier picture; more data helps most. Exact numbers depend on the seeds shown.
**Likely follow-ups:** 1) *Does cross-validation remove the problem?* It reduces it and shows the spread. 2) *Why stratify?* Keeps rare-class counts steady.
**Common mistakes:** Trying seeds until the score looks good; quoting one split as the truth.

### Q83 ⭐ 🔴 Your model beats the baseline in offline recall, but the retention campaign it supports shows no change in resignations. Give possible reasons and how you would investigate.
**Asked at:** commonly asked (no company-specific report found); gap-fill for model-versus-outcome questions.
**What the interviewer is checking:** That you separate "predicts well" from "the action works".
**Say this in the interview:** "A good prediction does not guarantee a good intervention. I would check whether the model is still accurate on current data, whether the right people were contacted, whether the offer reached them and could change their mind, and whether the campaign was measured against a fair control group."
**Explain simply:**
- **Model problems:** drift (staff and market changed since the training data), leakage that inflated offline recall (Q84), low precision so most contacts went to people who would have stayed anyway.
- **Action problems:** people flagged are leaving for reasons a conversation cannot fix (pay, relocation, retirement); the offer was too late, too weak, or never delivered by managers.
- **Measurement problems:** no control group, too short a window, seasonality, small numbers, or comparing different populations.
- Predicting who leaves is not the same as predicting who can be **persuaded** to stay.
- Investigate: compare campaign-time recall and precision against offline; check how many flagged were actually contacted; compare flagged-and-contacted with flagged-and-not-contacted (ideally a randomised holdout); list stated exit reasons.
**Alternative / pitfalls:** For future campaigns, keep a random control group among the flagged people, and track the outcome you want (retention), not only model scores.
**Likely follow-ups:** 1) *What is uplift?* Modelling who is changed by the action, not who is at risk (from memory, a specialist topic). 2) *Would you scrap the model?* Not yet; first find whether the problem is the model or the action.
**Common mistakes:** Blaming the model without checking the campaign; no control group; judging the result in a few weeks.

### Q84 ⭐ 🔴 Explain data leakage using an attrition model that includes the column 'exit_interview_done'. How would it affect the evaluation metrics?
**Asked at:** commonly asked (no company-specific report found); leakage is a standard evaluation-theme question (unverified).
**What the interviewer is checking:** Whether you spot a feature that is only known after the outcome.
**Say this in the interview:** "An exit interview only happens after someone has resigned, so the column hands the model the answer. Test scores look brilliant, but at prediction time, when the person is still employed, the column does not exist, so the model would fail in real use."
**Explain simply:**
- **Data leakage** = using information in training that would not be available when you make a real prediction.
- `exit_interview_done` is a consequence of leaving, not a cause. Others: termination date, final-settlement flag, notice-period fields.
- Effect on metrics: recall, precision and AUC are inflated on the test set, because the leak sits in both train and test; a normal split does not catch it.
- Spot it by asking for each column "would I know this on the day I score?", and by suspiciously high scores or one feature dominating.
**Sample data:** Synthetic 1,000 employees (209 leavers); exit interview done for 95% of leavers and 2% of stayers; logistic regression with `class_weight="balanced"`, seed 42.
**Code (what you write in the interview):**
```python
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score

rng = np.random.default_rng(42)
n = 1000
employees = pd.DataFrame({
    "tenure_years": rng.uniform(0, 10, n),
    "overtime_hours": rng.normal(10, 5, n),
})
chance_of_leaving = 1 / (1 + np.exp(-(-1.5 - 0.15 * employees["tenure_years"] + 0.08 * employees["overtime_hours"])))
employees["left"] = (rng.random(n) < chance_of_leaving).astype(int)
# an exit interview only happens AFTER someone resigns (95% of leavers get one, 2% of stayers by mistake)
employees["exit_interview_done"] = np.where(employees["left"] == 1, rng.random(n) < 0.95, rng.random(n) < 0.02).astype(int)
print("Leavers:", employees["left"].sum())
for name, features in [("without exit_interview_done", ["tenure_years", "overtime_hours"]), ("with exit_interview_done", ["tenure_years", "overtime_hours", "exit_interview_done"])]:
    X_train, X_test, y_train, y_test = train_test_split(employees[features], employees["left"], test_size=0.3, stratify=employees["left"], random_state=42)
    predicted = LogisticRegression(class_weight="balanced", max_iter=1000).fit(X_train, y_train).predict(X_test)
    print(f"{name}: recall {recall_score(y_test, predicted):.2f}, precision {precision_score(y_test, predicted):.2f}")
```
**Output:**
```
Leavers: 209
without exit_interview_done: recall 0.68, precision 0.31
with exit_interview_done: recall 0.90, precision 0.92
```
**What it means:** Adding the leaked column lifts recall from 0.68 to 0.90 and precision from 0.31 to 0.92, but that gain is fake. Report the honest model (recall about 0.68) and explain the exclusion.
**Alternative / pitfalls:** Time-based checks help: build features only from data before a cut-off date and predict later resignations. Other leakage: scaling or encoding on the full data before splitting.
**Likely follow-ups:** 1) *How would you notice?* Unusually high score, one dominant feature, drop in live performance. 2) *Is every post-event column leakage?* Yes if you would not have it at scoring time.
**Common mistakes:** Celebrating a 96% score without checking features (Q66); thinking a train/test split alone prevents leakage.

### Q85 ⭐ 🔴 What is the difference between a model that predicts well and one that explains why employees leave, and how does that change the metrics you report?
**Asked at:** commonly asked (no company-specific report found); gap-fill for prediction-versus-explanation questions.
**What the interviewer is checking:** That you know prediction is not causation and that the goal sets the metric.
**Say this in the interview:** "A predictive model asks 'who is likely to leave', and I judge it by recall, precision and calibration on unseen data. An explanatory model asks 'why', and I judge it by whether the effect sizes are stable, interpretable and credibly causal. A good predictor can use signals that are not causes."
**Explain simply:**
- **Prediction**: any signal that helps, even a symptom (for example sudden drop in login activity). Metrics: recall, precision, lift, calibration, all on held-out data.
- **Explanation**: understanding drivers, such as pay gaps or manager changes. Metrics: coefficients with confidence intervals, p-values, model fit (adjusted R-squared in linear models), checks for confounding; a clean, interpretable model such as logistic regression often fits.
- Prediction models (especially black-box ones) show association, not cause. "Overtime predicts leaving" does not prove cutting overtime stops leaving; a randomised pilot or careful design is needed for that.
- Say which question the business is asking before choosing the model and the metrics.
**Alternative / pitfalls:** Feature importance charts from a predictive model are not causal evidence. Explanatory models can predict poorly out of sample; check both if you need both.
**Likely follow-ups:** 1) *Can one model do both?* Partly, but state limits. 2) *How would you test a cause?* A pilot with random assignment.
**Common mistakes:** Treating feature importance as "reasons"; reporting recall to answer a "why" question.

### Q86 ⭐ 🔴 How would you evaluate a model whose classes are heavily imbalanced and where only about 20 positive cases exist in the test set?
**Asked at:** commonly asked; the "small minority count" caveat appears in imbalanced-data lists (unverified).
**What the interviewer is checking:** That you admit the numbers are shaky and use sound methods anyway.
**Say this in the interview:** "With 20 positives, each missed case moves recall by 5 points, so a single number is fragile. I would avoid accuracy, use recall, precision and PR-AUC, put an uncertainty range on them, and use stratified cross-validation so more positives get tested."
**Explain simply:**
- Never accuracy: a model saying "negative" for everyone looks great.
- Use **recall, precision, PR-AUC**, and the confusion matrix with raw counts.
- Show a **confidence interval** (a range likely to contain the true value); with 20 positives it will be wide.
- Use **stratified k-fold cross-validation** (repeated if possible) so every positive case is tested once, and consider collecting more data or a longer time window.
- Be careful with oversampling: only inside training folds, never before splitting.
**Sample data:** Test set with 20 real leavers; model caught 15.
**Code (what you write in the interview):**
```python
from statsmodels.stats.proportion import proportion_confint

# test set: 20 real leavers; the model caught 15
caught, leavers = 15, 20
low, high = proportion_confint(caught, leavers, method="wilson")
print(f"Recall {caught / leavers:.0%}, 95% range {low:.0%} to {high:.0%}")
# same 75% recall with 10 times as many leavers
low, high = proportion_confint(150, 200, method="wilson")
print(f"With 200 leavers: 95% range {low:.0%} to {high:.0%}")
```
**Output:**
```
Recall 75%, 95% range 53% to 89%
With 200 leavers: 95% range 69% to 80%
```
**What it means:** Recall of 75% on 20 leavers could really be anywhere from about 53% to 89%. Report "about 75%, but the range is wide because only 20 leavers were tested".
**Alternative / pitfalls:** Compare models on identical folds; differences of a few points are not meaningful at this size. Output uses the Wilson method for the range (other methods exist).
**Likely follow-ups:** 1) *Would you oversample?* Only within training data, and check calibration afterwards. 2) *What else?* A simple rule-based baseline for comparison.
**Common mistakes:** Quoting 75% as precise; oversampling before splitting (leakage).

### Q87 ⭐ 🔴 How would you choose between two models with similar recall when one is a logistic regression and the other a random forest, given your audience is HR?
**Asked at:** commonly asked (no company-specific report found); gap-fill for model-choice questions.
**What the interviewer is checking:** That you weigh explainability, stability and cost, not just one score.
**Say this in the interview:** "If recall is similar, I would pick the logistic regression: HR can see which factors raise or lower the risk, it is easier to audit for fairness and to defend to managers. I would pick the random forest only if it clearly wins on several metrics, such as precision and calibration, in cross-validation."
**Explain simply:**
- **Logistic regression** gives one coefficient per feature (direction and size), so you can say "each extra overtime hour raises the odds of leaving by x".
- **Random forest** averages many decision trees; it can catch curved, interacting patterns but is a "black box": harder to explain and audit.
- Compare more than recall: precision, calibration (Q74), stability across folds (Q82), subgroup gaps (Q67), effort to maintain.
- A tiny gain is not worth losing explainability; HR decisions about people need reasons.
- Check for leakage on both (Q84).
**Alternative / pitfalls:** Tools such as feature importance or SHAP can help to explain a forest (from memory, check docs), but they explain the model, not the cause. If the forest is far better, say so and agree on how decisions will be reviewed.
**Likely follow-ups:** 1) *What if forest recall is 5 points higher?* Check whether it holds across folds and what it costs in precision; then decide with the business. 2) *Which is faster to build?* Logistic regression is simple to train and check.
**Common mistakes:** Choosing the more complex model by default; judging only on one metric; ignoring who has to explain results to employees.

