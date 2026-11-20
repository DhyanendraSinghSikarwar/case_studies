# Book 9 — Basic ML + AI Tools for Analysts | Part 8: Attrition Prediction and Churn Mini-Projects 🟡🔴

**Target:** 30 questions | **Actual:** 33 questions
**Scope:** HR-friendly attrition and churn mini-projects: framing the target, leakage, imbalance, metrics on small confusion matrices, threshold and cost thinking, sklearn/statsmodels snippets, explaining scores to HR, fairness and privacy, and defending a portfolio project.

### Q1 ⭐⭐⭐ 🟢 You are asked to build an attrition prediction model for an HR team from raw HRIS data. Walk me through the steps from the business question to handing the result over.
**Asked at:** commonly asked (no company-specific report found); project-walkthrough prompts appear in HR-analytics question banks (PracHub, interviewprep.org style, seen only as search snippets, unverified as real company questions).
**What the interviewer is checking:** That you start from the business decision and finish with a hand-over, not just "I trained a model".
**Say this in the interview:** "I would first agree with HR what decision the model supports, define who counts as a leaver and over what window, clean the HRIS data, split before any tuning, start with a simple baseline, judge it on leaver-focused metrics, and hand over a ranked list with plain-words drivers and its limits."
**Explain simply:**
- **Business question:** "Which employees should get a stay-interview this quarter?" This fixes the prediction window (say the next 12 months) and the list size HR can handle.
- **Target and data:** the **target** (also called the label) is the column you predict: left in the next 12 months, yes or no. Use only information known on the snapshot date.
- **Clean and explore:** fix duplicates, missing values and inconsistent codes; check how many leavers you have (the class balance).
- **Split first:** hold out a **test set** (rows the model never sees while learning) before any tuning. Keep the leaver share equal in both parts.
- **Baseline, then model:** compare against "predict nobody leaves", then try logistic regression, then a tree-based model if needed.
- **Evaluate:** precision and recall for leavers, and precision at the list size (see Q4, Q5, Q10), not accuracy alone.
- **Hand over:** a list, the main drivers in plain words (as associations, not causes), known limits, a fairness check, and a plan to re-check the model every few months.
**Alternative / pitfalls:** Jumping straight to modelling; using the final exit-interview data as a feature (leakage, see Q6); handing over a score without telling HR what action it supports.
**Likely follow-ups:** 1) *Where would you spend most time?* Defining the target and cleaning data. 2) *How would HR use it?* To prioritise conversations, never as the only basis for a decision about a person.
**Common mistakes:** Skipping the business question; reporting only accuracy; leaving privacy and fairness out of the hand-over.

### Q2 ⭐⭐⭐ 🟢 How would you define the target variable for an employee attrition model, and why does it matter whether you include voluntary and involuntary exits together?
**Asked at:** commonly asked (no company-specific report found); target-definition prompts appear in attrition and churn question banks (unverified).
**What the interviewer is checking:** That you see the target as a business definition with a time window, not a ready-made column.
**Say this in the interview:** "I would define it as 'resigned voluntarily within the next 12 months of the snapshot date', and keep involuntary exits out or separate, because the reasons and the HR action for each are different."
**Explain simply:**
- The **target** needs a clear who (all employees active on a snapshot date), what (exit type) and when (a fixed window such as 12 months).
- **Voluntary** exits (resignations) are what stay-interviews and retention offers can influence.
- **Involuntary** exits (dismissals, redundancies, end of contract) are driven by company decisions. Mixed together, the model learns "poor performer" patterns and "restructured team" patterns, and the score no longer means "likely to resign".
- Retirements, deaths and internal transfers need a clear rule too (usually excluded or not counted as attrition).
- Employees who joined in the last few months have not had the full window yet, so decide how to treat them (see Q25 for the same issue in churn).
**Worked example (concept questions):** Of 1,000 employees, 150 left in 12 months: 110 resigned and 40 were laid off in a restructuring. Predicting all 150 as one class targets a 15% rate; predicting resignations targets 11%. A retention budget is aimed at the 110, so that is the target that matches the decision.
**Alternative / pitfalls:** Keep the involuntary exits out of the training data as leavers; do not label them "stayed", because they did not stay. Drop them or model them separately.
**Likely follow-ups:** 1) *What window?* One that matches how far ahead HR can act, often 6 to 12 months. 2) *Where does the exit type come from?* The HRIS termination reason, which should be checked for quality.
**Common mistakes:** Using the raw "Attrition = Yes" column without asking what it contains; changing the window between training and use.

### Q3 ⭐⭐⭐ 🟢 Your model gives an employee an attrition risk score of 0.72. How would you explain to an HR head what that number does and does not mean?
**Asked at:** commonly asked (no company-specific report found); "explain model output to HR" appears in HR-analytics question banks (unverified).
**What the interviewer is checking:** That you can explain a probability honestly and warn against over-reading it.
**Say this in the interview:** "0.72 means this employee looks more like past leavers than most people do. It is a ranking signal, not a 72% guarantee, and it does not say why the person might leave or that they will."
**Explain simply:**
- A **risk score** is the model's output between 0 and 1. It is a good ranking tool: higher means more similar to past leavers.
- It is only a true "72 in 100 will leave" if the model is **calibrated** (its probabilities match real rates; see Q31). Many models are not, especially after rebalancing.
- It does not say what to do. It does not prove anything about this person; it describes patterns in past data.
- It can be wrong in both directions: some high scorers stay, some low scorers leave.
- The score should start a conversation, not end a career: never use it alone for pay, promotion or dismissal decisions (see Q29).
**Worked example (concept questions):** Among 100 past employees with scores near 0.72, if 40 actually left, the honest message is "about 4 in 10", not 7 in 10. HR can check this by comparing scores with outcomes on past data.
**Alternative / pitfalls:** Show bands (high, medium, low) rather than two decimal places; false precision invites over-reading.
**Likely follow-ups:** 1) *What would you show next to the score?* The top contributing factors and the base rate. 2) *Should the employee see it?* A policy and consent question for HR and legal, not for the analyst alone.
**Common mistakes:** Saying "72% chance of leaving"; treating a score as a verdict; hiding that the model is wrong a lot of the time.

### Q4 ⭐⭐⭐ 🟢 Why is accuracy a misleading metric for an attrition model?
Data: 1,000 employees, 150 left in the next 12 months. A model predicts "stays" for everyone. Compute its accuracy, recall for leavers and precision for leavers.
**Asked at:** commonly asked (no company-specific report found); the "accuracy trap on imbalanced data" is a standard theme of churn and attrition tutorials and question banks (unverified).
**What the interviewer is checking:** That you notice a useless model can still score high accuracy when one class is rare.
**Say this in the interview:** "Because 85% of employees stay, a model that says 'everyone stays' is 85% accurate and finds zero leavers. Accuracy rewards the majority; I look at recall and precision for the leaver class instead."
**Explain simply:**
- **Accuracy** = correct predictions divided by all predictions.
- **Recall** (for leavers) = of the people who really left, how many did we catch.
- **Precision** (for leavers) = of the people we flagged, how many really left.
- Here: TP = 0, FP = 0, FN = 150, TN = 850.
- Accuracy = (0 + 850) / 1,000 = 0.85. Recall = 0 / 150 = 0. Precision = 0 / 0, which is undefined (no one was flagged); report it as 0 or "not defined".
**Code (what you write in the interview):**
```python
total, leavers = 1000, 150
true_positive, false_positive = 0, 0
true_negative = total - leavers      # everyone predicted "stays"
false_negative = leavers

accuracy = (true_positive + true_negative) / total
recall = true_positive / (true_positive + false_negative)
print("Accuracy:", accuracy)
print("Recall for leavers:", recall)
```
**Output:**
```
Accuracy: 0.85
Recall for leavers: 0.0
```
**What it means:** The model looks 85% good and is worthless for HR. Always compare against this "predict the majority" baseline, and report recall and precision for leavers to a manager.
**Alternative / pitfalls:** Balanced accuracy, PR-AUC and F1 are also less fooled by imbalance. In sklearn, `precision_score` warns on 0/0 and returns 0.
**Likely follow-ups:** 1) *What is a good baseline?* The majority-class model: 85% accuracy here. 2) *Which metric then?* See Q5.
**Common mistakes:** Quoting 85% as a success; forgetting that precision is undefined with no flags.

### Q5 ⭐⭐⭐ 🟡 Compute precision, recall and F1 for the leaver class and say which one matters more for an HR stay-interview programme.
Data (confusion matrix, leaver = positive): TP = 30, FP = 20, FN = 30, TN = 920.
**Asked at:** commonly asked (no company-specific report found); precision, recall and F1 from a small confusion matrix are standard in churn question banks (unverified).
**What the interviewer is checking:** Correct formulas, and a judgement about which error costs more.
**Say this in the interview:** "Precision is 60%, recall is 50%, F1 about 0.55. For stay-interviews, where a wasted conversation is cheap but a missed leaver is costly, recall matters more, as long as precision stays high enough for HR's capacity."
**Explain simply:**
- **TP:** flagged and left. **FP:** flagged but stayed. **FN:** not flagged but left. **TN:** not flagged and stayed.
- Precision = TP / (TP + FP) = 30 / 50 = 0.60.
- Recall = TP / (TP + FN) = 30 / 60 = 0.50.
- **F1** is a single score that balances both (their harmonic mean) = 2 x 0.60 x 0.50 / (0.60 + 0.50) = 0.545.
- Accuracy would be (30 + 920) / 1,000 = 0.95, but only 6% of employees are leavers, so it hides the story.
**Code (what you write in the interview):**
```python
tp, fp, fn, tn = 30, 20, 30, 920

precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)

print("Precision:", round(precision, 2))
print("Recall:", round(recall, 2))
print("F1:", round(f1, 3))
```
**Output:**
```
Precision: 0.6
Recall: 0.5
F1: 0.545
```
**What it means:** Of 50 people flagged, 30 really were at risk; the model found half of all leavers. To a manager: "We catch 1 in 2 leavers, and 6 in 10 conversations are well aimed."
**Alternative / pitfalls:** If HR has few interview slots (Q10), precision at that list size is the metric that matters; if conversations are cheap, push recall.
**Likely follow-ups:** 1) *How do you raise recall?* Lower the cut-off; precision usually falls. 2) *Why not just use F1?* It treats both errors equally, which may not match the costs.
**Common mistakes:** Swapping precision and recall; calling 95% accuracy good.

### Q6 ⭐⭐⭐ 🟡 What is data leakage in an attrition model? Name three columns in an HR file that could leak the outcome.
**Asked at:** commonly asked (no company-specific report found); leakage is a recurring theme in attrition-project prep content (PracHub-style leak-free pipeline exercise, snippet-level, unverified).
**What the interviewer is checking:** That you know a model can look brilliant by using information it would not have at prediction time.
**Say this in the interview:** "Leakage is when the training data contains information that is only known after, or because of, the outcome. The model looks great in testing and fails in real use. For attrition, think exit-interview score, notice-period flag and last working day."
**Explain simply:**
- At prediction time you only know what HR knows today. Any column filled in because the person is leaving is a **leak**.
- Three examples: **exit interview score or notes** (only exist for leavers); **notice period or resignation date** (exists only once they resigned); **final settlement / full-and-final amount or last working day** (created by the exit). Others: "eligible for rehire" and "access revoked" flags.
- A softer leak: **tenure computed up to the exit date** for leavers but up to today for stayers.
- Leakage can also come from process: scaling or oversampling before the train-test split (Q7).
- Symptom: near-perfect accuracy on a hard problem. Fix: build features as of the snapshot date, then ask for each column "would I know this before the person decided?".
**Worked example (concept questions):** A column "notice_served_days" is above 0 for all 150 leavers and 0 for the 850 stayers. A model using it scores about 100% in testing and predicts nothing in advance, because it only sees the notice once the resignation is in.
**Alternative / pitfalls:** Features that are legitimately available but near-duplicates of the target (an "exit_flag" column) are caught by checking single-feature predictive power.
**Likely follow-ups:** 1) *How do you spot it?* Suspiciously high scores and a feature that dominates importance. 2) *How do you prevent it?* Fixed snapshot dates and a column-by-column timing review.
**Common mistakes:** Believing a 99% score; only checking leakage after the model is built.

### Q7 ⭐⭐⭐ 🟡 What is wrong with this workflow, and how would you fix it?
```python
X_res, y_res = SMOTE().fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
```
**Asked at:** commonly asked (no company-specific report found); "SMOTE before the split" is a classic mistake flagged in attrition-project write-ups (snippet-level, unverified).
**What the interviewer is checking:** That you know rebalancing belongs inside training only.
**Say this in the interview:** "SMOTE creates synthetic leavers before the split, so the test set contains fake rows built from training rows. The score is inflated and the test is no longer real data. I would split first, rebalance the training set only, and score on untouched real rows with recall and precision, not accuracy."
**Explain simply:**
- **SMOTE** invents new minority-class rows by interpolating between existing similar ones (a method from the imbalanced-learn package).
- Done before the split, copies and near-copies of the same employee land on both sides, so the model is tested on what it has already seen. This is **data leakage** (Q6).
- The test set also no longer has the real 15% leaver share, so the score does not describe real life.
- `model.score` is accuracy, which is the wrong metric here (Q4).
- Fix, in order: stratified split first; rebalance `X_train, y_train` only (or inside a pipeline so cross-validation does it per fold); evaluate on the original test set with recall, precision and a confusion matrix.
**Worked example (concept questions):** I ran a simple version of this on pure random noise (1,000 rows, 5 random columns, about 15% leavers picked by chance, so there is nothing to learn), with plain duplication of leavers instead of SMOTE and a random forest, numpy seed 42. Duplicating before the split gave a test accuracy of about 0.95, which is meaningless because copies of the same leaver sit in both train and test. Splitting first and duplicating training rows only gave an honest accuracy of 0.805 with leaver recall of 2 of 35 (0.06), which is what random noise deserves. Exact figures depend on the seed and the generator; the gap between the two is the lesson.
**Alternative / pitfalls:** Fixed code (imbalanced-learn is not installed here, so this snippet is from memory, unverified):
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)
X_res, y_res = SMOTE(random_state=42).fit_resample(X_train, y_train)
model.fit(X_res, y_res)
```
Also consider simply `class_weight="balanced"`, which needs no new rows.
**Likely follow-ups:** 1) *Does SMOTE help at all?* Sometimes; try class weights and threshold change first. 2) *How with cross-validation?* Use an imbalanced-learn pipeline so it resamples per training fold only.
**Common mistakes:** Resampling the whole file; scoring with accuracy; forgetting `stratify` and `random_state`.

### Q8 ⭐⭐⭐ 🟡 How do you read a logistic regression coefficient in an attrition model when you explain it to HR?
Data: coefficient for OverTime = Yes is 0.90 (other variables held constant). Use e^0.90 ≈ 2.46. State what the odds ratio means and what it does not mean.
**Asked at:** commonly asked (no company-specific report found); coefficient and odds-ratio reading is a standard question in attrition-model prep (unverified).
**What the interviewer is checking:** That you convert a coefficient to an odds ratio and avoid saying "2.46 times the probability".
**Say this in the interview:** "Employees who work overtime have about 2.5 times the odds of leaving compared with similar employees who do not. It is an association in past data, not proof that overtime causes people to leave, and odds are not the same as probability."
**Explain simply:**
- A **coefficient** is the model's weight on a column. In logistic regression it is on the **log-odds** scale, so raise e to its power to get the **odds ratio**: e^0.90 = 2.46.
- **Odds** = chance of leaving divided by chance of staying. A 15% chance is odds of 0.15 / 0.85 = 0.18.
- Odds ratio 2.46 means odds are multiplied by 2.46 for overtime versus no overtime, **holding the other columns fixed**.
- It does not mean the probability is 2.46 times bigger: starting at 15%, odds 0.18 x 2.46 = 0.43, which is a probability of 30%, double, not 2.46 times. From a 5% start it becomes about 11.5%.
- It does not prove cause (Q11): overtime may be a symptom of an overloaded team or a particular manager.
**Worked example (concept questions):** Baseline leaver rate 15%. With the odds multiplied by 2.46 the rate becomes about 30%. Overtime employees in the model look twice as likely to leave, if everything else is equal.
**Alternative / pitfalls:** Coefficients of unscaled numeric columns depend on units (per year, per 1,000 rupees). A coefficient near 0 is an odds ratio near 1 (no effect).
**Likely follow-ups:** 1) *What if the coefficient is negative?* Odds ratio below 1, for example e^-0.5 = 0.61, meaning lower odds. 2) *How sure are you?* Check the confidence interval (see Q24 for statsmodels).
**Common mistakes:** Saying "2.46 times more likely"; ignoring "holding others constant"; reading it as a cause.

### Q9 ⭐⭐⭐ 🟡 Leavers are about 15% of your attrition dataset. List the ways you can handle this imbalance and say which you would try first.
**Asked at:** commonly asked (no company-specific report found); imbalance handling (class weights, SMOTE, threshold) is the standard theme of churn and attrition tutorials (unverified).
**What the interviewer is checking:** That you know several options, their risks, and that you start simple.
**Say this in the interview:** "First I would check that 15% is really a problem: use stratified splits and judge with recall and precision. Then I would try class weights, then moving the decision threshold, and only then resampling such as SMOTE, always on training data only."
**Explain simply:**
- **Class imbalance** means one class is much rarer (here 15% leavers). 15% is mild; the model can still learn.
- **Right metrics and stratified split:** keep 15% in train and test; judge with recall, precision, PR-AUC, not accuracy (Q4).
- **Class weights:** tell the model that a missed leaver costs more (`class_weight="balanced"`). No data is changed.
- **Change the threshold:** instead of flagging at 0.5, flag at a lower cut-off, or take the top N (Q10).
- **Resample:** oversample leavers (copies or SMOTE) or undersample stayers, in the training set only (Q7). Undersampling throws data away.
- **Collect more data** or a longer history, when feasible.
**Worked example (concept questions):** With 1,000 employees and 150 leavers, `class_weight="balanced"` makes each leaver count about 3.3 times a stayer (1,000 / (2 x 150)) and each stayer about 0.59 times (1,000 / (2 x 850)), so errors on leavers hurt more during learning.
**Alternative / pitfalls:** Resampling and weights shift predicted probabilities upward, so scores stop meaning real chances (Q31); fine for ranking.
**Likely follow-ups:** 1) *Why not undersample first?* Small HR data; you lose information. 2) *Does 15% really need SMOTE?* Often no.
**Common mistakes:** Resampling before the split; reporting accuracy; assuming balance is always required.

### Q10 ⭐⭐⭐ 🟡 HR can hold stay-interviews with only 50 employees this quarter. How do you turn the model's scores into that list, and how do you pick the cut-off?
Data: 1,000 employees scored; the top 50 by score contain 20 actual leavers; 150 employees leave in total.
Compute precision at 50 and the share of all leavers captured.
**Asked at:** commonly asked (no company-specific report found); capacity-limited thresholding is a standard "turn scores into action" prompt (unverified).
**What the interviewer is checking:** That the cut-off is set by HR capacity and cost, not by 0.5.
**Say this in the interview:** "I rank everyone by score and take the top 50, because that is HR's capacity. Precision at 50 is 40%, and the list captures 13% of all leavers. A random list of 50 would contain only 7.5 leavers, so the model is about 2.7 times better than random."
**Explain simply:**
- **Precision at 50** = leavers in the top 50 divided by 50 = 20 / 50 = 0.40.
- **Share captured (recall at 50)** = 20 / 150 = 0.133.
- The overall leaver rate is 150 / 1,000 = 15%, so a random 50 would hold 7.5 leavers. **Lift** = 0.40 / 0.15 = 2.67.
- Picking the cut-off: set it by capacity (top 50) or by comparing the cost of a wasted interview with the cost of losing someone. With more capacity, recall rises and precision usually falls.
- Also spread the list sensibly (for example check it is not all one team), and confirm the list with HR before use.
**Code (what you write in the interview):**
```python
total, leavers_total = 1000, 150
list_size, leavers_in_list = 50, 20

precision_at_50 = leavers_in_list / list_size
share_captured = leavers_in_list / leavers_total
lift = precision_at_50 / (leavers_total / total)

print("Precision at 50:", precision_at_50)
print("Share of leavers captured:", round(share_captured, 3))
print("Lift over random:", round(lift, 2))
```
**Output:**
```
Precision at 50: 0.4
Share of leavers captured: 0.133
Lift over random: 2.67
```
**What it means:** 4 of every 10 conversations reach someone who really would have left, and the list catches 1 in 8 leavers. Tell the manager that 50 slots cannot cover 150 leavers, so the model prioritises rather than solves.
**Alternative / pitfalls:** Pick the cut-off on validation data, not on the test set you report; and remember a stay-interview may itself change who leaves (so measure outcomes carefully).
**Likely follow-ups:** 1) *What if HR gets 100 slots?* Recompute the same two numbers at 100. 2) *Would you use 0.5?* No, a probability cut-off may flag far more or far fewer than 50.
**Common mistakes:** Using 0.5 by habit; calling 13% recall "bad" without noting the capacity limit.

### Q11 ⭐⭐⭐ 🟡 The model shows that employees with low satisfaction scores are more likely to leave. Can HR conclude that raising satisfaction will cut attrition? Explain.
**Asked at:** commonly asked (no company-specific report found); "association is not causation" is a stock follow-up in attrition-model prep (unverified).
**What the interviewer is checking:** That you separate prediction from causal claims.
**Say this in the interview:** "Not from this model alone. It shows that low satisfaction goes with leaving; it does not show that raising satisfaction would stop people leaving. To test that, HR needs a pilot or a comparison group."
**Explain simply:**
- A predictive model finds patterns. It cannot say what would happen if HR **changed** a column.
- **Reverse effect:** people who already plan to leave may report lower satisfaction, so the score may follow the decision rather than cause it.
- **Hidden third factor:** a poor manager or heavy workload can lower satisfaction and also cause exits. Fixing the survey score alone would not fix that.
- Survey scores can be gamed, and the survey may only be answered by some people.
- Better evidence: a pilot where one comparable group gets an intervention and a similar group does not, then compare exit rates.
**Worked example (concept questions):** Teams with satisfaction below 3 out of 5 have a 25% exit rate; teams above have 10%. If low satisfaction there comes from a manager with heavy overtime, a pizza party raises the score and leaves the exit rate unchanged.
**Alternative / pitfalls:** Use cautious words: "is associated with", "flags", "is linked to".
**Likely follow-ups:** 1) *How would you test it?* A pilot with a comparison group, or analyse a past policy change. 2) *Is the model then useless?* No, it is still useful for prioritising attention.
**Common mistakes:** Recommending actions as if the model proved cause; ignoring the reverse direction.

### Q12 ⭐⭐⭐ 🟡 A recruiter says: "I built a churn model on the Telco dataset with 80% accuracy." As the interviewer, what follow-up questions would you ask, and how should a candidate answer them?
**Asked at:** commonly asked (no company-specific report found); project-challenge questions on the Telco churn dataset appear in prep sites (unverified). The Telco dataset is a common public practice dataset; its details here are not verified.
**What the interviewer is checking:** Whether the candidate understands what 80% hides and can defend their own project.
**Say this in the interview:** "I would say: 80% accuracy means little until you compare it with predicting everyone stays. I report the churn rate, recall and precision for churners, how I split the data, and what the business would do with the list."
**Explain simply:**
- **Follow-up 1: "What is the churn rate?"** If about a quarter of customers churn (check your own data), a do-nothing model already scores about 75%, so 80% is a small gain.
- **Follow-up 2: "Precision and recall for churners?"** Give both numbers and the confusion matrix.
- **Follow-up 3: "How did you split and validate?"** Stratified train-test split or cross-validation, with scaling and encoding done inside the training part only.
- **Follow-up 4: "Any leakage?"** Name columns you checked, such as anything recorded after cancellation.
- **Follow-up 5: "What baseline did you beat?"** Majority class and a simple logistic regression.
- **Follow-up 6: "What would the business do with it?"** A retention offer list sized to budget, with the cost of each offer weighed against customer value.
- **Follow-up 7: "Which features mattered, and can you say they cause churn?"** Say associations only.
**Worked example (concept questions):** If 26 of 100 customers churn, "nobody churns" gives 74% accuracy; 80% gets only 6 more right per 100. A model with 80% accuracy and 20% recall would be nearly useless for retention.
**Alternative / pitfalls:** If you have not run these checks on your own project, say so honestly and run them before the interview.
**Likely follow-ups:** 1) *Why not 99%?* Suspect leakage. 2) *How would you improve it?* Better features, threshold tuning, more data.
**Common mistakes:** Defending 80% as good; not knowing your own class balance; claiming business impact that was never measured.

### Q13 ⭐⭐ 🟢 Which features would you engineer for an attrition model beyond the raw columns in an HRIS export? Give four with a reason each.
**Asked at:** commonly asked (no company-specific report found); feature ideas for attrition appear in question banks (unverified).
**What the interviewer is checking:** That your features come from HR understanding and are known before the outcome.
**Say this in the interview:** "I would build features that capture change and comparison: time since last promotion, pay compared with peers, manager change in the last year, and recent absence trend. All of them are known at the snapshot date."
**Explain simply:**
- A **feature** is a column the model uses to predict. **Feature engineering** means creating new ones from raw columns.
- **Months since last promotion or last raise:** stagnation is a common reason people look elsewhere.
- **Pay ratio to peers (salary divided by median pay for the same grade or role):** a raw salary hides whether the person feels underpaid relative to colleagues.
- **Manager change count in the last 12 months:** instability around a person often matters more than a static label.
- **Absence or leave trend (last 3 months versus the previous 3):** a change in pattern is more informative than the total.
- Other ideas: tenure bands, commute distance, team size, overtime hours trend, rating change since last cycle.
- Every feature must be computed only from information available at the snapshot date (Q6).
**Worked example (concept questions):** Two employees both earn 60,000. One is in a role where the median is 50,000 (ratio 1.2); the other where the median is 75,000 (ratio 0.8). The raw column shows no difference; the ratio shows one is likely feeling underpaid.
**Alternative / pitfalls:** Fairness: features such as commute distance or age can act as proxies for protected groups (Q30).
**Likely follow-ups:** 1) *How do you know a feature helps?* Compare model scores with and without it on held-out data. 2) *Any caution?* Missing history for new joiners.
**Common mistakes:** Features that look into the future; dozens of features on 300 rows; ignoring fairness.

### Q14 ⭐⭐ 🟢 How is a customer churn mini-project the same as, and different from, an employee attrition mini-project?
**Asked at:** commonly asked (no company-specific report found); comparison framing is a judgement-based gap-fill rather than a reported question.
**What the interviewer is checking:** That you can transfer the method and see what changes with people versus customers.
**Say this in the interview:** "The method is the same: define who left and when, avoid leakage, handle imbalance, judge on recall and precision, and tie the score to an action. The differences are the action, the data volume and the ethics, since employees are people we employ and not only revenue."
**Explain simply:**
- **Same:** a yes/no target with a time window, imbalance, leakage risk, train-test split, the same metrics, and the need for a business action.
- **Different, target:** customers can leave silently (no cancellation event, see Q17), whereas employees have a clear exit date and reason.
- **Different, data size:** a company may have many thousands of customers but only a few hundred employees, which limits complex models (Q33).
- **Different, action and cost:** a churn offer has a measurable price and revenue; a stay-interview has a harder-to-measure payoff.
- **Different, ethics:** employee scores touch careers, privacy and fairness more closely (Q29), and may need consent and legal review.
**Worked example (concept questions):** A telecom with 100,000 customers and 25% churn trains happily on a random forest. A 300-person firm with 40 leavers a year cannot do that reliably and may need a simple model and cautious claims.
**Alternative / pitfalls:** Customer data is often richer in behaviour (usage); HR data is mostly static records.
**Likely follow-ups:** 1) *Which one is harder?* Attrition, because of small data and ethics. 2) *Same metrics?* Yes.
**Common mistakes:** Treating employees as pure numbers; copying a customer churn threshold without reconsidering cost.

### Q15 ⭐⭐ 🟢 Would you start with logistic regression or a random forest for an HR attrition model, and why?
**Asked at:** commonly asked (no company-specific report found); simple-versus-complex model choice appears in attrition and churn guides (unverified).
**What the interviewer is checking:** That you choose by data size and explainability, not by what sounds impressive.
**Say this in the interview:** "I would start with logistic regression: HR datasets are small, the result is easy to explain, and it sets a baseline. If a random forest beats it clearly on held-out data, I would consider it and explain it with feature importance."
**Explain simply:**
- **Logistic regression** gives a weight per column and a probability. It is easy to explain to HR (Q8) and stable on small data.
- **Random forest** is many decision trees voting together. It can capture non-straight-line patterns and interactions, but is harder to explain.
- Start simple: a baseline tells you whether the added complexity is worth it.
- If both score similarly, choose the simple one.
- HR decisions affect people, so being able to explain "why this person is flagged" has real value.
**Worked example (concept questions):** If logistic regression gets leaver recall 0.55 and a random forest 0.57 on the same test set, a gap that small is noise on a few hundred rows; keep the simpler model.
**Alternative / pitfalls:** Compare on identical splits, with the same metric. Tree models also need care with leakage.
**Likely follow-ups:** 1) *Do you need scaling?* For logistic regression, usually yes; for forests, no. 2) *When would you use the forest?* When nonlinear patterns matter and accuracy gain is clear.
**Common mistakes:** Picking the forest by default; comparing models on different splits.

### Q16 ⭐⭐ 🟢 Write the short code to split an attrition dataset into train and test sets and fit a logistic regression, keeping the leaver share equal in both sets.
Data: a pandas DataFrame `df` with numeric features and a 0/1 column `Attrition`.
**Asked at:** commonly asked (no company-specific report found); stratified split plus logistic regression is a basic sklearn exercise (unverified).
**What the interviewer is checking:** That you know `stratify`, a fixed `random_state` and that you fit on train only.
**Say this in the interview:** "I separate the features from the target, split with `stratify=y` so both sets keep the same leaver share, fix the random seed, and fit only on the training part."
**Explain simply:**
- **Features (X)** are the predictor columns; **target (y)** is `Attrition`.
- `stratify=y` keeps the 0/1 mix the same in both sets.
- `random_state=42` makes the split repeatable.
- The model **fits** (learns) on the training set only; the test set is kept for the final check.
**Sample data:** My check used 1,000 synthetic rows (not real employees) with five numeric columns (Age, Tenure, Salary, OverTimeHours, SatisfactionScore) and about 15% leavers, made with `make_classification(n_samples=1000, n_features=5, n_informative=2, n_redundant=2, weights=[0.85], random_state=42)` from `sklearn.datasets`, with the five columns then named as above (the names are labels only; the values are random). With this call the output below reproduces on scikit-learn 1.9.1.
**Code (what you write in the interview):**
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X = df.drop(columns="Attrition")
y = df["Attrition"]

# stratify=y keeps the same leaver share in train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print("Leaver share, train:", round(y_train.mean(), 3))
print("Leaver share, test:", round(y_test.mean(), 3))
print("Test accuracy:", round(model.score(X_test, y_test), 3))
```
**Output:**
```
Leaver share, train: 0.151
Leaver share, test: 0.15
Test accuracy: 0.975
```
**What it means:** Both sets have about 15% leavers, as in the full data. The 0.975 accuracy is on easy synthetic data; on a real attrition file, report recall and precision for leavers, not accuracy.
**Alternative / pitfalls:** With text categories, encode them inside a pipeline (Q22). Add `class_weight="balanced"` if leavers are rare. Scale numeric columns if features have very different ranges.
**Likely follow-ups:** 1) *Why stratify?* With few leavers, a random split can leave very few in the test set. 2) *Why `random_state`?* So results are repeatable.
**Common mistakes:** Leaving the target in `X`; fitting on the full data; no `stratify`.

### Q17 ⭐⭐ 🟢 An e-commerce company has no subscriptions. How would you define a churned customer for a churn model?
Data (days between orders for one customer): 12, 20, 15, 30, 18. Suggest an inactivity window and justify it from these gaps.
**Asked at:** commonly asked (no company-specific report found); the non-contractual churn definition is a judgement-based gap-fill (no source names it).
**What the interviewer is checking:** That you turn "no cancel button" into a time-based rule tied to normal buying rhythm.
**Say this in the interview:** "Without a cancellation event, I define churn as no purchase for longer than a window based on normal buying gaps. This customer's longest gap is 30 days, so I would use about 60 days, roughly twice the longest usual gap, and then check the rule across all customers."
**Explain simply:**
- In a **non-contractual** business, customers just stop coming; nobody tells you. So churn must be defined by **inactivity**.
- From the gaps: average 19 days, longest 30 days. A silence well beyond the longest normal gap is unusual, so 60 days (2 x 30) is a reasonable start.
- Five gaps from one customer is far too little. In practice, look at the gap distribution across all customers (for example the 90th or 95th percentile) and by product type, since groceries and furniture differ.
- Check the window with business: a 60-day rule on a yearly-purchase product would label everyone churned.
- Then build the label: as of a snapshot date, customer is "churned" if no order in the next 60 days (see Q25 for the timing issue).
**Code (what you write in the interview):**
```python
import pandas as pd

gaps = pd.Series([12, 20, 15, 30, 18])   # days between orders, one customer
print("Average gap:", gaps.mean())
print("Longest gap:", gaps.max())

# churned if silent for about twice the longest usual gap
window = 2 * gaps.max()
print("Churn window (days):", window)

days_since_last_order = 75
print("Churned?", days_since_last_order > window)
```
**Output:**
```
Average gap: 19.0
Longest gap: 30
Churn window (days): 60
Churned? True
```
**What it means:** A customer silent for 75 days is well outside their normal 12 to 30 day pattern, so they count as churned under a 60-day rule. The 75 days is an example value I added.
**Alternative / pitfalls:** Other choices: a fixed company rule (no purchase in 90 days), or a spend drop (revenue below a fraction of the usual). Seasonal customers (a festival-season buyer) may look churned wrongly.
**Likely follow-ups:** 1) *How do you tune the window?* Pick one where few "churned" customers come back soon after. 2) *What about one-time buyers?* Treat them as a separate group.
**Common mistakes:** Picking 30 days without checking the data; using one window for all products; forgetting that a window too short flags customers who are simply between orders.

### Q18 ⭐⭐ 🟡 Two attrition models are tested on the same 1,000 employees. Which would you give to HR for stay interviews, and why?
Data: Model A precision 0.50, recall 0.60. Model B precision 0.70, recall 0.30. Total leavers = 150. Compute how many leavers each model catches and how many people each flags.
**Asked at:** commonly asked (no company-specific report found); precision/recall trade-off questions appear in churn and attrition question banks (unverified).
**What the interviewer is checking:** Whether you can turn precision and recall into head-counts and pick a model by the HR team's capacity, not by one metric.
**Say this in the interview:** "Recall tells me how many leavers we catch; precision tells me how many interviews are well spent. Model A catches 90 of 150 leavers but flags 180 people; Model B catches 45 but flags only about 64. If HR can run roughly 180 interviews, I give them A; if they can only do about 60, B wastes less effort."
**Explain simply:**
- **Precision** = of the people flagged, the share who really leave. **Recall** = of all real leavers, the share we flagged.
- Leavers caught = recall x 150. People flagged = leavers caught / precision.
- Model A: caught 0.60 x 150 = 90; flagged 90 / 0.50 = 180; false alarms 90; missed leavers 60.
- Model B: caught 0.30 x 150 = 45; flagged 45 / 0.70 = 64.3; false alarms about 19; missed leavers 105.
- F1 (a single blend of precision and recall) is 0.55 for A and 0.42 for B, but F1 ignores the capacity question, so do not stop there.
**Premise check:** 45 / 0.70 is 64.29, not a whole person. The figures are rounded in the question; read it as about 64 flagged (45 / 64 = 0.70).
**What it means:** A finds twice as many leavers, B is more efficient per interview (70% of its flags are right, against 50%). Report both head-counts to the manager and let interview capacity decide.
**Alternative / pitfalls:** The fairest test is to compare both models at the same number of flags (for example the top 50 by score), because a model can raise precision just by flagging fewer people.
**Likely follow-ups:** 1) *Can you tune B to catch more?* Yes, lower its cut-off; recall rises and precision falls. 2) *What if a stay interview is cheap?* Prefer A, since a missed leaver costs far more than a wasted conversation.
**Common mistakes:** Picking the model with the higher precision without asking how many people HR can actually talk to; forgetting that the two numbers are linked to the cut-off.

### Q19 ⭐⭐ 🟡 Estimate the net value of an attrition model with the figures below, and state which assumptions the answer depends on.
Data (illustrative): model flags 40 employees, 24 of them are real leavers. A stay interview costs 5,000 per person. It retains 20% of true leavers. Replacing a leaver costs 400,000.
**Asked at:** commonly asked (no company-specific report found); cost-benefit framing of a model appears in prep-site banks (unverified).
**What the interviewer is checking:** Whether you connect a model to money and are honest about the assumptions behind the number.
**Say this in the interview:** "Cost is 40 x 5,000 = 200,000. Benefit is 20% of 24 true leavers, so 4.8 people retained, times 400,000 = 1,920,000. Net is about 1.72 million, but it rests on the 20% retention rate and the replacement cost, so I would show a range."
**Explain simply:**
- Everyone flagged gets an interview, including the 16 false alarms, so cost counts all 40.
- Only true leavers can be retained; 4.8 is an expected average, not a real count of people.
- Break-even: the interviews pay for themselves if retention is above 200,000 / (24 x 400,000) = about 2.1%.
**Sensitivity (computed):**

| Retention rate | Net value |
|---|---|
| 5% | 280,000 |
| 10% | 760,000 |
| 20% | 1,720,000 |

**What it means:** The programme looks profitable even if the 20% is far too optimistic. Tell the manager the answer depends on the assumptions below, not on the model alone.
**Alternative / pitfalls:** The answer assumes: the 20% retention is real (ideally measured against a group that was not interviewed); replacement cost is 400,000 for everyone (it varies by role); the flagged leavers would truly have left without the interview; no cost for missed leavers is counted, and no side effects (a flagged person may feel watched).
**Likely follow-ups:** 1) *Does it count the 16 non-leavers?* Yes, as cost only. 2) *How would you prove the 20%?* A small randomised pilot: interview half the flagged list, compare exits.
**Common mistakes:** Counting the benefit for all 40 flagged people; presenting 1.72 million as certain.

### Q20 ⭐⭐ 🟡 Should you split attrition data randomly or by time? Explain with an example of what can go wrong with a random split.
**Asked at:** commonly asked (no company-specific report found); train/test split design is a standard prep-site topic (unverified).
**What the interviewer is checking:** Whether you test the model the way it will really be used: on future data and on people it has never seen.
**Say this in the interview:** "A model is used to predict the future, so I prefer a time-based split: train on the past, test on later months. A random split can put the same employee, or next month's rows, on both sides, so the score looks better than reality."
**Explain simply:**
- **Train set** is what the model learns from; **test set** is the exam it has not seen.
- A random split is fine for one-row-per-person snapshots where nothing changes over time.
- It goes wrong with employee-month tables (one row per person per month): the same person lands in both sets, and the model simply recognises them.
- It also hides drift: policies, pay and the job market change, and a random split mixes old and new together.
**Worked example (concept question):** Made-up table: 400 employees x 1 to 12 monthly rows each, 25% leave, and age and salary are random per person (tiny month-to-month wobble) with no link to leaving. A random forest scored on a random 70/30 row split gets an AUC of about 0.98 (AUC: 0.5 is a coin flip, 1.0 is perfect), because it recognises the same person in both sets. The same model tested on employees it never saw (a group split) gets about 0.51, which is the honest answer. Seed 42; exact values change with the generator.
**Alternative / pitfalls:** Best of both: split by time, and keep each employee on only one side (group split). Watch out: with only a few years of data, a time split leaves a small test set, so report the uncertainty.
**Likely follow-ups:** 1) *What is a group split?* Keep all rows of one person together in train or test. 2) *Time split for a static snapshot?* Use snapshot date A for training and later date B for testing.
**Common mistakes:** Calling a 0.98 score from a random split "model performance"; forgetting that one person has many rows.

### Q21 ⭐⭐ 🟡 Why would you use stratified k-fold cross-validation for a churn or attrition model?
**Asked at:** commonly asked (no company-specific report found); validation for imbalanced churn data appears in question banks (unverified).
**What the interviewer is checking:** Whether you understand imbalance and why each test fold needs enough leavers.
**Say this in the interview:** "Cross-validation tests the model several times on different slices. Leavers are rare, so a plain split can leave a slice with almost no leavers. Stratified folds keep the leaver share the same in every slice, so the scores are stable and comparable."
**Explain simply:**
- **k-fold cross-validation**: cut the data into k parts, train on k-1, test on the remaining one, repeat k times, then average.
- **Stratified** means each part keeps the same share of leavers as the full data.
- Without it, a fold could hold zero leavers, and recall or precision would be undefined for it.
**Sample data:** 100 employees, 10 leavers, listed with the leavers first (a common accident when data is sorted by outcome).
**Code (what you write in the interview):**
```python
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold

# 100 employees, only 10 leavers (1 = left); sorted so leavers sit together
left = np.array([1] * 10 + [0] * 90)
X = np.arange(100).reshape(-1, 1)

for name, splitter in [("KFold", KFold(5)), ("StratifiedKFold", StratifiedKFold(5))]:
    leavers_per_test_fold = [int(left[test].sum()) for _, test in splitter.split(X, left)]
    print(name, leavers_per_test_fold)
```
**Output:**
```text
KFold [10, 0, 0, 0, 0]
StratifiedKFold [2, 2, 2, 2, 2]
```
**What it means:** The plain version puts every leaver in one fold, so four folds cannot measure recall at all. Stratified gives two leavers in each.
**Alternative / pitfalls:** With a strong ordering by date, use time-aware splits instead; for repeated people use group folds. Do any resampling (such as SMOTE) inside the training folds only.
**Likely follow-ups:** 1) *Does `cross_val_score` stratify by default?* For a classifier with a yes/no target and an integer k, yes: I checked that scikit-learn 1.9.1 picks `StratifiedKFold` without shuffling (it does not for regression targets). 2) *How many folds?* 5 is common; with very few leavers use fewer folds or repeat.
**Common mistakes:** Shuffling and stratifying but still letting the same person appear in several folds; reporting only the average without the spread.

### Q22 ⭐⭐ 🟡 Write a scikit-learn pipeline that one-hot encodes the categorical columns, scales the numeric columns and fits a class-weighted logistic regression.
Data: `cat_cols = ["Department", "JobRole"]`, `num_cols = ["Age", "MonthlyIncome", "YearsAtCompany"]`.
**Asked at:** commonly asked (no company-specific report found); a leak-free preprocessing pipeline is a typical exercise in prep-site banks (unverified).
**What the interviewer is checking:** That preprocessing and model live in one object, so nothing is learned from test data.
**Say this in the interview:** "I put the encoder, scaler and model in one pipeline, so when I fit on the training set, the scaling numbers and categories come only from training. `class_weight='balanced'` makes each leaver count more because leavers are rare."
**Explain simply:**
- **One-hot encoding** turns a text column (Department) into 0/1 columns, one per value.
- **Scaling** puts numbers on a similar range so income (thousands) does not drown age (tens).
- **Class weight** tells the model that a missed leaver costs more than a missed stayer.
- `handle_unknown="ignore"` stops a crash if a new job role appears later.
**Sample data:** 600 made-up employees in `employees` (about 10% leavers), columns Department, JobRole, Age, MonthlyIncome, YearsAtCompany, Attrition (1 = left). Only for running the code; this builder is not part of the interview answer:
```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
rows = 600
employees = pd.DataFrame({
    "Department": rng.choice(["Sales", "HR", "R&D"], rows),
    "JobRole": rng.choice(["Executive", "Analyst", "Manager", "Technician"], rows),
    "Age": rng.integers(21, 60, rows),
    "MonthlyIncome": rng.normal(6000, 2000, rows).round(),
    "YearsAtCompany": rng.integers(0, 20, rows),
    "Attrition": (rng.random(rows) < 0.10).astype(int),   # random, no real signal
})
```
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import recall_score, precision_score

cat_cols = ["Department", "JobRole"]
num_cols = ["Age", "MonthlyIncome", "YearsAtCompany"]

X = employees[cat_cols + num_cols]
y = employees["Attrition"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# One-hot the text columns, scale the number columns
preprocess = ColumnTransformer([
    ("categories", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ("numbers", StandardScaler(), num_cols),
])

model = Pipeline([
    ("preprocess", preprocess),
    ("classifier", LogisticRegression(class_weight="balanced", max_iter=1000)),
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("Recall:", round(recall_score(y_test, predictions), 2))
print("Precision:", round(precision_score(y_test, predictions), 2))
print("Columns after encoding:", model[:-1].transform(X_test).shape[1])
```
**Output:** (data from the builder above, numpy seed 42; a different build gives different numbers)
```text
Recall: 0.5
Precision: 0.12
Columns after encoding: 10
```
**What it means:** 10 columns = 3 departments + 4 roles + 3 numbers. The model catches half of the leavers in the test set but only 12% of its flags are right; with 10% leavers, class weights trade precision for recall. On this made-up data, that is expected and not a real finding.
**Alternative / pitfalls:** `make_column_transformer` is a shorter spelling. Class weights distort predicted probabilities (see Q31), so do not read the scores as true chances.
**Likely follow-ups:** 1) *Why not scale before the split?* The test set would influence the scaling numbers (leakage). 2) *Why a pipeline?* So cross-validation refits every step on each training fold.
**Common mistakes:** Fitting the encoder on the full dataset; one-hot encoding an ID column; forgetting `max_iter` warnings.

### Q23 ⭐⭐ 🟡 A random forest ranks MonthlyIncome as the most important feature for attrition. What cautions would you give before presenting this to HR?
**Asked at:** commonly asked (no company-specific report found); "explain the drivers" and "association is not causation" appear in attrition question banks (unverified).
**What the interviewer is checking:** Whether you know importance is not cause, and that correlated features share or steal credit.
**Say this in the interview:** "Importance says which column the model leaned on, not that pay causes people to leave. Income moves with job level and tenure, so it may be a stand-in for those. I would check permutation importance, drop-column tests and what happens within the same job level before telling HR to raise pay."
**Explain simply:**
- **Feature importance** is how much the model used a column to predict; it says nothing about what happens if HR changes that column.
- With **correlated features**, the model can pick one and ignore its twin, so the winner looks bigger than it is.
- The default (impurity) importance can favour columns with many distinct values, like income.
- Importance shows size, not direction: it does not say whether low or high income leaves.
**Worked example (concept question):** Made-up 2,000 employees where income is almost a copy of job level (correlation 0.96) and leaving truly depends on level and overtime, not income itself. With only income and overtime, the forest gives income 0.56 of the importance. Add job level and income drops to 0.44 while level takes only 0.13: income still looks like the top driver, partly because it has many distinct values (the bias in the second point above) and partly because it shares credit with level. Permutation importance (shuffle a column and see how much accuracy falls, on held-out rows) is small for every column here: income 0.00, level 0.02, overtime 0.04. Within level 3 alone, income and leaving have a correlation of only -0.09. Random forest with seed 42; made-up data, and exact values change with the seed.
**What it means:** Present it as "income is associated with leaving, partly through level"; never as "raise salaries to cut attrition" without testing.
**Alternative / pitfalls:** Use a plain logistic regression or partial-dependence plots for direction; check importance on test data; run a small pay pilot to learn the causal effect.
**Likely follow-ups:** 1) *Better method?* Permutation importance on test data, or SHAP (explanation tool, from memory; I would confirm usage in the docs). 2) *Does a high rank mean a big effect?* No, only that the model used it.
**Common mistakes:** Turning an importance chart into a policy recommendation; reading importance as direction.

### Q24 ⭐⭐ 🟡 Read this statsmodels output and tell the manager which findings you would act on and which you would treat carefully.
Data (logit, 1,470 rows): OverTime[Yes] coef 1.10, p < 0.001; YearsSinceLastPromotion coef 0.05, p = 0.30; JobSatisfaction coef -0.30, p = 0.002.
**Asked at:** commonly asked (no company-specific report found); reading regression output for attrition is common in prep-site banks (unverified).
**What the interviewer is checking:** Whether you convert coefficients into odds ratios and separate "statistically clear" from "causal" and "big enough to matter".
**Say this in the interview:** "Overtime has odds about 3 times higher of leaving, and that is clearly not noise. Job satisfaction is also clear: each extra point cuts the odds by about 26%. Promotion gap is not distinguishable from zero here. But all three are associations, not proof of cause."
**Explain simply:**
- A logit coefficient is a change in log-odds; exponentiate it to get an **odds ratio**: exp(1.10) = 3.00, exp(0.05) = 1.05, exp(-0.30) = 0.74.
- **p-value**: how surprising this result would be if the true effect were zero. Small (below 0.05) means "unlikely to be noise".
- Overtime: odds roughly triple (95% interval lower bound about 1.6, worked back from p < 0.001, so the effect is clearly above 1).
- Satisfaction: odds ratio 0.74 per point; approximate 95% interval 0.61 to 0.90 (reconstructed from the coefficient and p-value, so rounded).
- Promotion gap: odds ratio 1.05 per year, interval about 0.96 to 1.16, which includes 1 (no effect). It does not prove "no effect", only that this data cannot tell.
**What it means:** Act first on overtime (large and clear), take satisfaction seriously (clear but moderate, and a survey score may itself change after someone decides to leave), and do not build a policy on promotion gap from this model alone. Intervals are from the printed numbers only; the full table would give exact ones.
**Alternative / pitfalls:** Association not causation (Q11); overtime may be a sign of workload in specific teams; with about 1,470 rows and few leavers, intervals are wide; check units (satisfaction is per point, promotion per year).
**Likely follow-ups:** 1) *Is p = 0.30 proof it does nothing?* No, it is absence of evidence. 2) *Which is the biggest effect?* Overtime, but compare per sensible unit, not raw coefficients.
**Common mistakes:** Reading a coefficient as a percentage point change; calling p = 0.002 "a very big effect"; ignoring the sign.

### Q25 ⭐⭐ 🟡 Churn is very rare in a month. How does a customer who joined last month and has not yet cancelled create a labelling problem, and how would you handle it?
**Asked at:** commonly asked (no company-specific report found); censoring is a gap-fill topic beyond what the sources name (judgement).
**What the interviewer is checking:** Whether you notice that "has not left yet" is not the same as "will not leave".
**Say this in the interview:** "A new customer labelled 'stayed' may simply not have had time to churn. I define churn with a fixed window, such as cancels within 90 days of signup, and only label customers we have watched for the whole window. Newer customers are left out of training, or handled with survival analysis."
**Explain simply:**
- **Censoring**: for some customers, the story is not finished by the snapshot date, so the label is unknown.
- Treating them as "stayed" teaches the model that new customers never churn.
- Fix: choose a window, require enough observation time, and set the snapshot date explicitly.
**Sample data:** 6 customers, snapshot date 2025-10-31, window 90 days. Customers 5 and 6 joined in September and October.
**Code (what you write in the interview):**
```python
import pandas as pd

customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5, 6],
    "signup_date": pd.to_datetime(["2025-01-10", "2025-02-01", "2025-03-15",
                                   "2025-05-20", "2025-09-05", "2025-10-20"]),
    "cancel_date": pd.to_datetime(["2025-02-20", None, None, "2025-06-30", None, None]),
})
snapshot_date = pd.Timestamp("2025-10-31")
window_days = 90

# Only customers old enough to have been watched for the full window
customers["days_observed"] = (snapshot_date - customers["signup_date"]).dt.days
eligible = customers[customers["days_observed"] >= window_days].copy()

# Churned = cancelled within 90 days of signup
days_to_cancel = (eligible["cancel_date"] - eligible["signup_date"]).dt.days
eligible["churned_90d"] = (days_to_cancel <= window_days).astype(int)
print(eligible[["customer_id", "days_observed", "churned_90d"]])
print("Dropped as too new:", customers.loc[customers["days_observed"] < window_days, "customer_id"].tolist())
```
**Output:**
```text
   customer_id  days_observed  churned_90d
0            1            294            1
1            2            272            0
2            3            230            0
3            4            164            1
Dropped as too new: [5, 6]
```
**What it means:** Customers 5 and 6 are excluded because we cannot yet know their 90-day outcome. Their rows can be scored later once the window has passed.
**Alternative / pitfalls:** Survival analysis (for example Kaplan-Meier or Cox models) uses partial information from unfinished customers (name only, not computed here). Also drop old accounts that were already dead before the window if the business defines it that way.
**Likely follow-ups:** 1) *Does the same apply to attrition?* Yes: "still employed" at snapshot is not "never leaves". 2) *How long a window?* Match the business action time, for example how long marketing needs to respond.
**Common mistakes:** Labelling everyone without a cancel date as 0; using a different snapshot date for features than for labels.

### Q26 ⭐⭐ 🟡 Build a decile lift table by hand: what is the lift of the top decile, and what does it tell the marketing team?
Data: 1,000 customers, 100 churners overall. The top 100 by model score contain 40 churners.
**Asked at:** commonly asked (no company-specific report found); lift and gains tables appear in churn question banks (unverified).
**What the interviewer is checking:** Whether you can compute lift and say what it means for a campaign budget.
**Say this in the interview:** "The overall churn rate is 100 / 1,000 = 10%. The top decile has 40 / 100 = 40%. Lift is 40% / 10% = 4. Contacting the top 10% of customers finds churners four times as efficiently as random picking, and catches 40% of all churners."
**Explain simply:**
- **Decile**: sort customers by score, cut into 10 equal groups of 100.
- **Lift** = churn rate in the group / overall churn rate. Lift 1 means no better than random.
- **Cumulative capture** = share of all churners found so far (top decile: 40 / 100 = 40%).
- The question gives only the top decile; the rest of the table below is made up for illustration.
**Code (what you write in the interview):**
```python
import pandas as pd

# Churners per decile (top decile first); only the first figure is given, the rest are made up
churners_in_decile = [40, 20, 12, 8, 6, 5, 4, 3, 1, 1]
lift_table = pd.DataFrame({"decile": range(1, 11), "customers": 100, "churners": churners_in_decile})

overall_rate = lift_table["churners"].sum() / lift_table["customers"].sum()
lift_table["churn_rate"] = lift_table["churners"] / lift_table["customers"]
lift_table["lift"] = lift_table["churn_rate"] / overall_rate
lift_table["cumulative_capture"] = lift_table["churners"].cumsum() / lift_table["churners"].sum()
print(lift_table.round(2))
```
**Output:**
```text
   decile  customers  churners  churn_rate  lift  cumulative_capture
0       1        100        40        0.40   4.0                0.40
1       2        100        20        0.20   2.0                0.60
2       3        100        12        0.12   1.2                0.72
3       4        100         8        0.08   0.8                0.80
4       5        100         6        0.06   0.6                0.86
5       6        100         5        0.05   0.5                0.91
6       7        100         4        0.04   0.4                0.95
7       8        100         3        0.03   0.3                0.98
8       9        100         1        0.01   0.1                0.99
9      10        100         1        0.01   0.1                1.00
```
**What it means:** Spend the retention budget on the top two deciles: 20% of customers contain 60% of churners. For marketing: lift 4 at decile 1, and the model is useless beyond about decile 3 (lift near or below 1).
**Alternative / pitfalls:** Compute lift on test data only, and remember it depends on the base rate. A cumulative gains chart shows the same idea.
**Likely follow-ups:** 1) *Lift of a random model?* 1.0 everywhere. 2) *Why not accuracy?* Marketing contacts a fixed share, so ranking matters.
**Common mistakes:** Using training data; calling lift 4 "4% better"; forgetting to sort by score first.

### Q27 ⭐⭐ 🟡 The same attrition mini-project idea can predict offer dropouts in a hiring funnel. Describe the target, three features and one risk of that project.
**Asked at:** commonly asked (no company-specific report found); an offer-dropout variant is a gap-fill beyond what the sources name (judgement).
**What the interviewer is checking:** Whether you can transfer the method to a new HR problem, with a clear label and awareness of risks.
**Say this in the interview:** "Target: among candidates who accepted an offer, 1 if they did not join by the joining date, else 0. Features known at offer time: hike percentage over current pay, notice period, and the gap between offer and joining. The main risk is leakage, using information collected after the offer that already reveals the outcome."
**Explain simply:**
- **Target** (the label): offer accepted but candidate never joined, with a date window so every row has a known outcome.
- **Features** available at offer time: percentage hike versus current pay, notice period days, offer-to-joining gap, number of interview rounds, source of hire.
- **Risk 1 (leakage):** "last contact date" or "joining kit sent" are known only later and may leak the result.
- **Risk 2:** recruiters act on the score (extra calls), so future labels are changed by the model itself.
- **Risk 3:** features like college or city can act as proxies for protected groups, so scoring should help the recruiter support candidates, not screen them out.
**Worked example (concept question):** If 800 accepted offers contain 120 dropouts, the dropout rate is 15%. A model that always says "will join" is 85% accurate and finds none, so judge it by recall and precision on the dropout class, as in Q4.
**Alternative / pitfalls:** Small data (a few hundred offers a year) means a simple model and wide uncertainty; time-split the data.
**Likely follow-ups:** 1) *What action follows a high score?* A stay-in-touch call or faster paperwork. 2) *Should the score affect offers?* No, that crosses a fairness line.
**Common mistakes:** Including candidates who never accepted; using post-offer behaviour as a feature.

### Q28 ⭐ 🟡 Your model's recall for leavers differs by gender. Compute the gap and say how you would handle it before the model is used.
Data: Group A has 50 leavers, model catches 40. Group B has 50 leavers, model catches 20.
**Asked at:** commonly asked (no company-specific report found); subgroup error-rate audits appear in HR-analytics ethics articles (unverified trade-press claims).
**What the interviewer is checking:** Whether you can compute a subgroup gap, judge if it is real, and have a sensible plan before deployment.
**Say this in the interview:** "Recall is 40/50 = 0.80 for group A and 20/50 = 0.40 for group B, a gap of 40 percentage points; the model finds half as many leavers in B. With 50 per group this is unlikely to be chance, so I would pause deployment and investigate before anyone is scored."
**Explain simply:**
- **Recall** here = share of real leavers the model flagged. Gap = 0.80 - 0.40 = 0.40; ratio B/A = 0.5.
- Rough 95% ranges (computed): A 0.67 to 0.89, B 0.28 to 0.54. They do not overlap; a Fisher exact test gives p of about 0.00008.
- Group B leavers are being missed, so they get fewer stay interviews: a fair-access problem.
- Next check precision and false-alarm rates for each group too; equal recall alone is not the whole picture.
**What it means:** Report to the manager: "The model works noticeably worse for group B; do not use it until we find out why." Steps: check data quality and sample size per group, look for proxy columns, test different cut-offs per group (a policy and legal choice, to be reviewed with legal, from memory unverified), retrain with better features, and keep a human review.
**Alternative / pitfalls:** Small groups give noisy gaps, so always show intervals. Do not "fix" it by dropping the group from the report.
**Likely follow-ups:** 1) *Is equal recall the right target?* It is one fairness measure; others (equal precision, equal flag rate) can conflict with it. 2) *Does removing gender fix it?* Not necessarily (Q30).
**Common mistakes:** Quoting overall recall only (0.60 here hides the gap); acting on gaps from 5 leavers.

### Q29 ⭐ 🔴 Should HR use individual attrition risk scores to decide who gets promotions or training? Discuss fairness, consent and privacy, including proxy variables.
**Asked at:** commonly asked (no company-specific report found); the ethics angle appears in trade-press and vendor blogs on attrition prediction (unverified).
**What the interviewer is checking:** Judgement: do you know the limits and harms of scoring people, not just the maths?
**Say this in the interview:** "I would not use individual risk scores to decide promotions or training. The score predicts who might leave, not who deserves a chance, and it can create a self-fulfilling prophecy: passed over for training, the person leaves. I would use team-level views and support actions, with consent and human review."
**Explain simply:**
- **Wrong target:** a risk score is not a performance or potential score. Using it for rewards punishes people for being at risk.
- **Fairness:** historic leavers reflect past pay gaps and bias, so the model can repeat them; audit error rates by group (Q28).
- **Proxy variables:** columns that stand in for protected traits, for example postcode for community, career-break for gender, part-time for caregiving. Removing the protected column does not remove the effect (Q30).
- **Consent and privacy:** employees should know what data is used and why; collect the minimum, restrict access, and avoid sensitive data like health or union membership. Privacy law (India's DPDP Act, GDPR) sets rules on purpose and consent; from memory, unverified, so confirm with legal.
- **Safer use:** aggregate risk for teams, look for root causes (workload, pay, managers), and let people opt into support.
**Alternative / pitfalls:** If scores are used at all, limit them to offering help (a stay conversation), explain them, give employees a way to challenge, and review outcomes regularly.
**Likely follow-ups:** 1) *Is any use acceptable?* Yes, for planning support at team level. 2) *Who owns the decision?* A human manager and HR, never the score alone.
**Common mistakes:** Saying "the model is objective"; treating consent as a one-time checkbox; ignoring proxies.

### Q30 ⭐ 🔴 You removed gender from the features, yet the model's flags still differ by gender. How can that happen and what would you check?
**Asked at:** commonly asked (no company-specific report found); proxy variables appear in ethics-related attrition sources (unverified).
**What the interviewer is checking:** Whether you know that other columns can encode gender, and that real outcomes may differ too.
**Say this in the interview:** "Other columns can stand in for gender, such as part-time status, role or career breaks. The model uses them and the flags still differ. I would test whether the remaining features can predict gender, and compare flag rate, recall and precision by group."
**Explain simply:**
- A **proxy variable** is a column that moves with gender (or another protected trait) closely enough to carry the same signal.
- Flag rates can also differ because real leaving rates differ between groups; the real question is whether the errors differ.
- Checks: (1) Can the remaining features predict gender? A high AUC (a score where 0.5 is a coin flip) says proxies exist. (2) Compare flag rate, recall, precision and false alarms per group. (3) Drop or alter the suspect feature and see if the gap shrinks. (4) Check whether the training labels reflect biased past decisions.
**Worked example (concept question):** Made-up 4,000 employees: 8% of men and 39% of women work part-time, and part-time raises leaving odds. Leaving odds rise with part-time work, so women leave a bit more often in this data (about 15% against 9%). The model never sees gender, yet it flags the top 15% of scores: about 5% of men and 24% of women, with recall 0.25 for men and 0.46 for women. A model that sees only part-time and tenure can predict gender with an AUC of about 0.65. Part-time is the proxy. Logistic regression, seed 42; made-up data, exact figures change with the seed.
**What it means:** Dropping the column was cosmetic. Decide with HR and legal whether the proxy feature is justifiable, and monitor group metrics after launch.
**Alternative / pitfalls:** Keep gender in a separate audit table (not as a model input) so you can measure the gap; deleting it removes your ability to check fairness.
**Likely follow-ups:** 1) *Is a flag-rate gap always bias?* No, it may reflect real differences; compare error rates and look at causes. 2) *Fix?* Remove or redesign the proxy, retrain, review thresholds.
**Common mistakes:** Believing "fairness through unawareness"; auditing only overall accuracy.

### Q31 ⭐ 🔴 A model says 0.30 for a group of 100 similar employees but only 10 of them leave. What does that tell you about calibration, and does it matter for HR?
**Asked at:** commonly asked (no company-specific report found); calibration is a gap-fill topic beyond what the sources name (judgement).
**What the interviewer is checking:** Whether you know the difference between ranking people well and giving trustworthy probabilities.
**Say this in the interview:** "The model is over-predicting: 0.30 means about 30 of 100 should leave, but only 10 did, so it is poorly calibrated. If HR only ranks people and takes the top 50, it matters little. If HR uses 0.30 to forecast headcount or cost, it matters a lot."
**Explain simply:**
- **Calibration**: when the model says 30%, about 30% should happen. Here 30 expected versus 10 actual, three times too high.
- Chance does not explain it: if the true rate were 30%, getting 10 or fewer leavers out of 100 has probability about 0.0000016 (computed).
- Common cause: class weights or oversampling (SMOTE) used to handle imbalance push scores upward. They help catch leavers but distort probabilities.
- It matters when scores feed a budget (expected leavers x replacement cost); it matters less for a ranked top-50 list.
**Worked example (concept question):** Made-up 5,000 employees with an 11.5% leaver rate. A plain logistic regression's average score is 0.115 against an actual 0.115 (calibrated). The same model with `class_weight="balanced"` has an average score of 0.435, against the same actual rate, yet its ranking (AUC) is identical, 0.74 versus 0.74. Seed 42.
**Alternative / pitfalls:** Check a calibration curve (bucket scores, compare average score with actual rate); recalibrate on held-out data with Platt scaling or isotonic regression (scikit-learn `CalibratedClassifierCV`, from memory; verify before using). Keep calibration data separate from training data.
**Likely follow-ups:** 1) *Number to report?* Expected versus actual leavers by score band. 2) *Does good AUC mean good calibration?* No.
**Common mistakes:** Quoting a probability from a class-weighted model as real risk; judging calibration on training data.

### Q32 ⭐ 🔴 Six months after deployment, attrition jumps after a pay-policy change and the model's precision falls. How would you detect and respond to this drift?
**Asked at:** commonly asked (no company-specific report found); drift is a gap-fill topic beyond what the sources name (judgement).
**What the interviewer is checking:** Whether you know a model decays when the world changes and have a monitoring and response plan.
**Say this in the interview:** "I would track the leaver rate, the score distribution and precision of the top flags each month. A pay-policy change is a classic cause of drift: the reasons people leave change, so old patterns stop working. I would investigate, retrain on recent data and, until then, use the model with caution."
**Explain simply:**
- **Data drift**: input or score distributions change. **Concept drift**: the link between inputs and leaving changes (new leavers leave for new reasons).
- Detect: monthly precision and recall on matured outcomes, base rate, **PSI** (Population Stability Index, compares score shares between launch and now; a common rule of thumb says above 0.25 is a big shift, from memory, unverified), and feature shifts such as pay ratio.
- Note the puzzle in the question: a higher base rate by itself usually raises precision. Example arithmetic: with recall 0.6 and false-alarm rate 0.1, precision is 0.40 at a 10% base rate and 0.60 at 20%. If precision falls anyway, the model is missing the new type of leaver (recall falling to 0.35 at 20% gives 0.47), which points to concept drift.
- Respond: confirm the data is correct, retrain on post-change data (time split), add features for the new policy (for example pay band after the change), adjust the cut-off, and set retraining rules.
**Code (what you write in the interview):**
```python
import numpy as np

def population_stability_index(old_scores, new_scores, bins=10):
    # Cut points come from the old (training-time) scores
    cuts = np.quantile(old_scores, np.linspace(0, 1, bins + 1))[1:-1]
    old_share = np.bincount(np.digitize(old_scores, cuts), minlength=bins) / len(old_scores)
    new_share = np.bincount(np.digitize(new_scores, cuts), minlength=bins) / len(new_scores)
    return np.sum((new_share - old_share) * np.log(new_share / old_share))

rng = np.random.default_rng(42)
scores_at_launch = rng.beta(2, 8, 2000)      # made-up risk scores in month 0
scores_now = rng.beta(3, 6, 2000)            # made-up scores 6 months later
print("PSI:", round(population_stability_index(scores_at_launch, scores_now), 2))
```
**Output:** (made-up scores, seed 42)
```text
PSI: 0.96
```
**What it means:** The score mix has moved a lot since launch, so investigate and retrain. PSI only says "something changed", not why.
**Alternative / pitfalls:** Outcomes arrive late (people leave months after the score), so also watch early signals such as score shifts. Do not retrain blindly on a short period around the policy shock.
**Likely follow-ups:** 1) *How often to retrain?* On a schedule plus when monitoring triggers. 2) *Can you keep using the old model?* Only with a clear warning and human review.
**Common mistakes:** Watching only accuracy; waiting for the next annual review; retraining without checking why.

### Q33 ⭐ 🔴 A 200-person company has only 12 leavers in three years and wants an attrition model. What do you advise?
**Asked at:** commonly asked (no company-specific report found); tiny-data advice is a gap-fill beyond what the sources name (judgement).
**What the interviewer is checking:** Whether you can say "do not build it" and offer a more useful alternative.
**Say this in the interview:** "Twelve leavers is too few for a reliable prediction model. I would advise a descriptive analysis instead: exit reasons, leaver rates by team and tenure band, and a short survey. If they still want a model, treat it as an experiment with a very small number of features and wide uncertainty."
**Explain simply:**
- 12 of 200 is 6% overall (about 2% a year if headcount stayed steady), with a 95% range of 3.5% to 10.2% (computed). A model that says "nobody leaves" is 94% accurate and useless.
- A common rule of thumb is about 10 leavers per feature, so 12 supports about one feature (rule of thumb, not exact).
- Test sets would hold 2 or 3 leavers, so scores swing wildly.
**Worked example (concept question):** Made-up check (logistic regression, scikit-learn 1.9.1): 200 rows, 12 random "leavers", 8 features of pure noise, shuffled 4-fold stratified cross-validation, repeated with 200 different seeds. The average AUC is 0.50, as it should be, yet single runs range from 0.18 to 0.81, and about 9.5% of runs score above 0.65 by luck. A "good" result on 12 leavers can easily be noise.
**What it means:** Tell leadership that the data cannot support a trustworthy model; better use of time is understanding the 12 exits and collecting more.
**Alternative / pitfalls:** Add more history, pool similar groups, record reasons for leaving, or use exit and stay interviews. If a model is built, use logistic regression with 1 or 2 features, report intervals, and do not use scores to make decisions about individuals.
**Likely follow-ups:** 1) *Would SMOTE help?* No, it duplicates the same 12 stories. 2) *What would change your mind?* Several years more data or several hundred leavers.
**Common mistakes:** Running a complex model anyway and reporting 94% accuracy; trusting a single cross-validation score.

