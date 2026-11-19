# Book 9 — Basic ML + AI Tools for Analysts | Part 1: What ML Is; Supervised vs Unsupervised; When Analysts Use It 🟢

**Target:** 76 questions | **Actual:** 77 questions
**Scope:** what machine learning is, supervised vs unsupervised learning, features and labels, classification vs regression, basic sklearn/pandas reading, and when and when not to use ML as an analyst (including bias, privacy and explainability basics).

### Q1 ⭐⭐⭐ 🟢 Explain machine learning to a non-technical manager in two or three sentences.
**Asked at:** commonly asked (no company-specific report found); "what is ML" opens most question banks seen as snippets, and ML basics appear in about 4 candidate-reported DA interviews (Indium, Mu Sigma, LatentView, Wipro, one each; unverified anecdotes).
**What the interviewer is checking:** Can you explain a technical idea in plain words without buzzwords?
**Say this in the interview:** "Machine learning is software that learns patterns from past data instead of following rules a person wrote by hand. For example, it can look at thousands of past employees, see who left and who stayed, and then estimate how likely a current employee is to leave. It gives an estimate, not a guarantee, and it is only as good as the data it learned from."
**Explain simply:**
- "Learns" means the computer adjusts itself until its guesses on past cases are close to what really happened.
- Then it applies what it found to new cases it has not seen.
- Keep the manager's attention on the business use, not the algorithm name.
**Likely follow-ups:** 1) *Is it the same as AI?* ML is one way of building AI (see Q8). 2) *Does it always work?* No; it needs enough clean historical data and a pattern that actually exists.
**Common mistakes:** Starting with "algorithms, neural networks, gradient descent"; promising certainty; forgetting to give a business example.

### Q2 ⭐⭐⭐ 🟢 What is the difference between supervised and unsupervised learning?
**Asked at:** commonly asked; reported as a standard opener on prep-site question banks and one Glassdoor (Siemens) question page (snippet level, unverified).
**What the interviewer is checking:** Whether you know that the difference is "do we have the answers (labels) in the data or not".
**Say this in the interview:** "In supervised learning each past row comes with the correct answer, for example 'left the company: yes or no', and the model learns to predict that answer. In unsupervised learning there is no answer column; the model just looks for structure, such as groups of similar customers."
**Explain simply:**
- Label (also called target): the column we want to predict. Features: the columns we use to predict it.
- Supervised: has a label. Two types: classification (predict a category) and regression (predict a number).
- Unsupervised: no label. Common tasks: clustering (grouping similar rows) and anomaly detection (finding unusual rows).
- Think "teacher marks the homework" (supervised) versus "sort these photos into piles however they look alike" (unsupervised).
**Worked example (concept question):** 5,000 past employees with a column `left` (Yes/No) means supervised. 5,000 employees with only survey scores and no outcome, grouped into "engaged", "neutral", "disengaged" piles by similarity, is unsupervised.
**Alternative / pitfalls:** There is a third family, reinforcement learning, which is rarely needed by analysts. Do not call clustering "prediction": it describes, it does not predict a known outcome.
**Likely follow-ups:** 1) *Which needs more effort to prepare?* Supervised, because someone must collect reliable labels. 2) *Can the two be combined?* Yes (Q39).
**Common mistakes:** Saying "supervised means a human watches the model"; mixing up clustering with classification.

### Q3 ⭐⭐⭐ 🟢 What is the difference between machine learning and traditional rule-based programming?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand that in ML the rules come out of the data rather than being typed in?
**Say this in the interview:** "In rule-based programming a person writes the rules, such as 'flag anyone with more than 20 overtime hours'. In machine learning we give the computer past examples with outcomes and it works out the rules itself. Rules are great when they are simple and known; ML helps when the pattern is too messy to write by hand."
**Explain simply:**
- Rules: input data + hand-written rules produce answers. ML: input data + known answers produce the rules (the model).
- Rules are easy to explain and audit, but break when many factors interact.
- ML can weigh many columns together, but it is harder to explain and needs good historical data.
**Worked example (concept question):** On 10 past employees, the hand-written rule "overtime above 20 hours means will leave" matched what really happened for 8 of 10 (80%), computed by script. A model could look at overtime, tenure and more columns together and may do better, but you must test it on rows it has not seen (Book 9 later parts). If the 80% rule is good enough, use the rule.
**Alternative / pitfalls:** Many production systems mix both: a model gives a score and business rules decide the action.
**Likely follow-ups:** 1) *When prefer rules?* When the logic is known, legal or must be fully transparent (for example a leave policy). 2) *Is ML always more accurate?* No; compare against the simple rule as a baseline (Q30).
**Common mistakes:** Calling every IF statement "AI"; assuming ML needs no human judgement.

### Q4 ⭐⭐⭐ 🟢 What are features and a label (target) in a machine learning dataset? Name them for an employee attrition dataset.
**Asked at:** commonly asked (no company-specific report found); attrition datasets are a common prompt in prep-site question banks (unverified).
**What the interviewer is checking:** Basic vocabulary, and whether you can map it to an HR table.
**Say this in the interview:** "Features are the input columns the model uses to make its guess; the label is the column it is trying to predict. In an attrition dataset, features could be age, tenure, salary, department and overtime hours, and the label is whether the employee left, Yes or No."
**Explain simply:**
- Each row is one example (one employee). Each column is one fact about that example.
- Features are known at prediction time; the label is the outcome we want to know in advance.
- Columns that only exist after the outcome (for example "exit interview date") must not be features, or the model cheats (called leakage).
**Worked example (concept question):** Row: age 29, tenure 14 months, overtime 28 hours/month, department Sales, left = Yes. The first four are features; `left` is the label. An ID such as emp_id is neither: it is just a name tag.
**Likely follow-ups:** 1) *Another word for label?* Target or outcome. 2) *Another word for feature?* Predictor, input variable or independent variable.
**Common mistakes:** Using emp_id or exit-date columns as features; thinking the label is also an input.

### Q5 ⭐⭐⭐ 🟢 What is the difference between classification and regression? Give one HR example of each.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you pick the task type from the kind of answer wanted?
**Say this in the interview:** "Classification predicts a category, like 'will this employee resign: yes or no'. Regression predicts a number, like 'how many days of leave will this team take next month'. The deciding question is: is the answer a label or a quantity?"
**Explain simply:**
- Classification: answer is one of a few groups (resign / stay; high / medium / low risk).
- Regression: answer is a number on a scale (salary, days, rupees).
- Classification models often give a probability first, then a cut-off turns it into a category.
- Naming trap: "logistic regression" is used for classification.
**Worked example (concept question):** HR classification: will a candidate accept the offer (yes/no). HR regression: predict the expected time to hire in days for an open role (for example 38 days).
**Likely follow-ups:** 1) *What if the answer is a rating 1 to 5?* Treat as classification if categories, regression if you want a smooth number; say your choice. 2) *Which one is clustering?* Neither; clustering has no label (Q23).
**Common mistakes:** Deciding by the algorithm name instead of the answer type; calling a yes/no problem regression because of "logistic regression".

### Q6 ⭐⭐⭐ 🟢 Give one real business example each of supervised and unsupervised learning.
**Asked at:** commonly asked; examples requested in prep-site variants of the supervised vs unsupervised question (snippet level, unverified).
**What the interviewer is checking:** Can you tie each type to a concrete use?
**Say this in the interview:** "Supervised: a bank uses past loans marked 'repaid' or 'defaulted' to predict whether a new applicant will default. Unsupervised: an online store groups customers by what and how often they buy, with no predefined groups, so marketing can design different offers."
**Explain simply:**
- Supervised example needs a known outcome column; here it is repaid or defaulted.
- Unsupervised example needs only behaviour data; groups are discovered, then humans name them ("bargain hunters", "loyal weekly buyers").
- An HR pair: predict who will resign (supervised); group employees by survey answers (unsupervised).
**Likely follow-ups:** 1) *How do you check the groups are useful?* By whether the business can act on them and whether they are stable (Part 4 covers this). 2) *Fraud example?* With past fraud labels it is supervised; without labels, finding unusual claims is unsupervised (Q21, Q43).
**Common mistakes:** Giving an example with no data behind it; picking an example where the label does not exist.

### Q7 ⭐⭐⭐ 🟢 When would a data analyst reach for machine learning instead of a dashboard, pivot table or SQL query?
**Asked at:** commonly asked (no company-specific report found); the sources note ML is thin for 0 to 3 year analyst roles, so expect this as a judgement question.
**What the interviewer is checking:** Judgement: ML is a tool for prediction at scale, not the default.
**Say this in the interview:** "A dashboard, pivot or SQL query answers 'what happened and where'. I reach for ML when the business needs a prediction for each individual case, or a pattern across many columns that I cannot find by slicing, and there is enough clean history to learn from. Otherwise I stay with the simpler tool."
**Explain simply:**
- Use pivots and SQL for totals, trends and comparisons; they are faster, cheaper and easy to explain.
- Use ML to rank or score individual rows (which employees are at highest risk, which leads will buy), or to group rows when there are too many columns to eyeball.
- Prerequisites: a clear decision that will change because of the prediction, enough history, and labels if supervised.
**Alternative / pitfalls:** Often the best first step is a pivot of attrition by tenure band; if that already shows the story, ML adds little.
**Likely follow-ups:** 1) *How much data is enough?* No fixed rule; more rows and a clear signal help; say you would test and see. 2) *What if stakeholders just want a report?* Give the report.
**Common mistakes:** Using ML to look sophisticated; skipping the simple analysis that would have answered the question.

### Q8 ⭐⭐⭐ 🟢 What is the difference between AI, machine learning, deep learning and data science?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know how the terms nest, and that data science is a job area, not a model type?
**Say this in the interview:** "AI is the broad goal of making machines do tasks that look intelligent. Machine learning is a part of AI where the system learns from data. Deep learning is a part of ML that uses many-layered neural networks. Data science is the wider practice of getting insight from data, using statistics, coding and sometimes ML."
**Explain simply:**
- Nesting: AI contains ML, ML contains deep learning (like Russian dolls).
- Data science overlaps all of them but also includes cleaning, SQL, visualisation and communication.
- Generative AI tools (chatbots) are built with deep learning (general knowledge, not verified here).
- A simple rule-based chatbot is AI in a loose sense but not ML.
**Likely follow-ups:** 1) *Where do analysts sit?* Mostly in data analysis, using basic ML occasionally. 2) *Is Excel regression ML?* It is statistics; the line is blurry (Q14).
**Common mistakes:** Treating the four as separate and equal; saying "deep learning is always better".

### Q9 ⭐⭐⭐ 🟢 What does it mean to "train" a model, and what is the difference between an algorithm and a model?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The recipe-versus-dish distinction.
**Say this in the interview:** "An algorithm is the learning method, like a recipe. Training is running that recipe on historical data. The model is the result: the learned settings that I can now use to predict on new data."
**Explain simply:**
- Training = showing the algorithm many examples with answers so it adjusts its internal numbers to fit them. In code, `fit` does this.
- Algorithm: logistic regression, decision tree. Model: that algorithm after fitting to your attrition data, with its specific learned numbers.
- The same algorithm on different data gives a different model.
- Model can be saved and reused without retraining.
**Worked example (concept question):** Algorithm: "fit a straight line through salary versus experience". Model after training: salary = 25000 + 4000 x years (the line it found, see Q35).
**Likely follow-ups:** 1) *What are the learned numbers called?* Parameters (Part 3 style question; they differ from hyperparameters you choose beforehand). 2) *How do you know training worked?* By testing on rows it has not seen (later parts).
**Common mistakes:** Using algorithm and model as synonyms; thinking training means the model memorises every row.

### Q10 ⭐⭐⭐ 🟢 Label each task as classification, regression or clustering: (a) predict next month's sales amount, (b) group customers by buying behaviour with no predefined groups, (c) predict whether an employee will resign within six months, (d) predict delivery time in minutes.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you spot the answer type quickly and give a one-line reason?
**Say this in the interview:** "(a) Regression, the answer is a number. (b) Clustering, there are no labels. (c) Classification, the answer is yes or no. (d) Regression, the answer is a number of minutes."
**Explain simply:**
- (a) sales amount is a quantity, so regression (a time-based forecast is a special case, covered in later parts).
- (b) "no predefined groups" is the signature of clustering, which is unsupervised.
- (c) "whether" signals a category, so classification, which is supervised. The six-month window defines the label.
- (d) minutes are a number, so regression.
- Shortcut: "how many / how much" is regression, "which / whether" is classification, "group similar" is clustering.
**Likely follow-ups:** 1) *Can (c) be turned into regression?* Yes, predict months until resignation, but yes/no is usually what HR acts on. 2) *Which are supervised?* (a), (c), (d).
**Common mistakes:** Calling (a) classification because "high or low sales" is easier to say.

### Q11 ⭐⭐⭐ 🟢 Does every analytics problem need machine learning? Describe one situation where ML is the wrong tool.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Practical judgement; not every problem is an ML nail.
**Say this in the interview:** "No. If a pivot table, a SQL query or a fixed business rule answers the question, that is faster, cheaper and easier to explain. For example, calculating monthly payroll or checking who has crossed the leave limit is a fixed rule, so ML would be the wrong tool."
**Explain simply:**
- ML is wrong when the logic is known and exact (payroll, tax slabs, leave policy).
- Also wrong when there is almost no history (a new product with 30 rows), when labels are unreliable, or when a decision must be fully explainable by law or policy.
- Also wrong when nobody will act on the prediction.
**Worked example (concept question):** Payroll: net pay = gross minus deductions by a fixed formula; a model that "predicts" salary would sometimes be a few rupees wrong, which is unacceptable. The rule is exact.
**Likely follow-ups:** 1) *What would you do instead?* Rule, query or dashboard. 2) *When is the answer "maybe"?* When a simple rule exists but a model could beat it; test both (Q30).
**Common mistakes:** Saying yes to every ML request; forgetting that exact logic needs rules, not estimates.

### Q12 ⭐⭐⭐ 🟢 Look at the columns of this HR table. Which one is the label, which are usable features, and which would you drop before modelling?
Columns: emp_id, age, tenure_months, monthly_salary, department, overtime_hours, left_company (Yes/No)
**Asked at:** commonly asked (no company-specific report found); column-exclusion and leakage themes appear in community question banks (snippet level, unverified).
**What the interviewer is checking:** Label vs feature vs useless or risky column.
**Say this in the interview:** "The label is `left_company`. Usable features are age, tenure_months, monthly_salary, department and overtime_hours. I drop `emp_id`, because it is just an identifier with no pattern to learn. I would also think twice about age, as it can create fairness problems."
**Explain simply:**
- `emp_id`: unique per person, so it carries no repeatable pattern and can even let the model memorise individuals.
- `department` is text; it must be turned into numbers first (Q41).
- Check that features were known before the person left. For example, if `monthly_salary` is the final salary after a pre-exit adjustment, it may leak.
- Age and similar personal traits are legally and ethically sensitive in HR; confirm with HR policy and legal whether they may be used (rules differ by country; from memory, unverified).
**Alternative / pitfalls:** Dropping columns is a decision, not a rule: ask what each column means and when it is recorded.
**Likely follow-ups:** 1) *Would you keep tenure?* Yes, it is usually informative. 2) *Is salary safe?* Safe only if recorded before the outcome.
**Common mistakes:** Keeping emp_id as a feature; leaving the label in the feature set; ignoring fairness.

### Q13 ⭐⭐⭐ 🟢 Does a machine learning model give certain answers? How would you explain its output to a stakeholder who expects a yes or no?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you communicate uncertainty and do not oversell.
**Say this in the interview:** "No, a model gives an estimate with uncertainty, usually a probability. I would say: 'Out of employees who look like this one, about 3 in 10 have left in the past.' We then agree a cut-off for action, for example talk to anyone above 40%, and I tell them it will sometimes be wrong in both directions."
**Explain simply:**
- Most classifiers produce a score between 0 and 1 first; a threshold you choose turns it into yes or no.
- A wrong "yes" (false alarm) and a wrong "no" (missed case) have different costs; the business sets the threshold.
- Scores are only as reliable as the training data; a score is not a verdict on a person.
**Worked example (concept question):** Score 0.30 for an employee: among 100 similar past employees, about 30 left (0.30 x 100 = 30). If HR's rule is "act above 0.40", this employee gets no flag, yet could still resign.
**Alternative / pitfalls:** Probabilities from some models are not well calibrated, so "30%" may not mean exactly 30 in 100; treat them as a ranking unless checked.
**Likely follow-ups:** 1) *How do you set the cut-off?* From the cost of a missed case vs a false alarm. 2) *Can we use it to decide firing or promotion?* I would advise against using a score alone for decisions about people.
**Common mistakes:** Presenting the output as fact; hiding the error rate; giving a yes/no with no threshold explained.

### Q14 ⭐⭐⭐ 🟡 What is the difference between machine learning and classical statistics, and where do they overlap for an analyst?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand the difference in goal (explain versus predict) and see the overlap?
**Say this in the interview:** "Classical statistics mainly asks 'is this effect real and how big', using tests, confidence and assumptions. Machine learning mainly asks 'how well can we predict new cases', and is judged on accuracy on unseen data. They overlap a lot: linear and logistic regression are used by both."
**Explain simply:**
- Statistics: smaller data, explicit assumptions, interpretable coefficients, p-values and confidence intervals.
- ML: larger data, flexible models, success measured on held-out data, less concern about exact interpretation.
- Overlap: regression, sampling, distributions, checking data quality, avoiding misleading conclusions.
- For an analyst: use statistics to explain and test ("does overtime relate to attrition?"), ML to score and predict.
**Worked example (concept question):** A statistical question: "Is average tenure of leavers lower than stayers, and by how much?" An ML question: "Which of today's 800 employees look most likely to leave?"
**Likely follow-ups:** 1) *Which does logistic regression belong to?* Both. 2) *Can a good predictor still be misleading?* Yes; prediction does not prove cause.
**Common mistakes:** Saying they are completely separate; saying ML proves causes.

### Q15 ⭐⭐⭐ 🟡 Read this code. What does each line do, and what is the role of fit and predict?
```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X, y)
new_pred = model.predict(X_new)
```
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you read basic sklearn code and explain fit versus predict.
**Say this in the interview:** "Line 1 imports the logistic regression tool from scikit-learn. Line 2 creates an empty model. `fit` trains it on features X and known answers y. `predict` then gives answers for new rows X_new, which the model has never seen."
**Explain simply:**
- `LogisticRegression()` is a model object with no knowledge yet. Logistic regression is used for yes/no classification despite its name.
- `fit(X, y)`: X is the table of features, y the label column. This is where learning happens.
- `predict(X_new)`: X_new must have the same columns as X. It returns one answer per row.
- Not shown: `predict_proba` gives probabilities instead of yes/no.
**Sample data:** Tiny made-up attrition table (8 employees, left = 1 means left), two new employees.

| tenure_months | overtime_hours | left |
|---|---|---|
| 6 | 30 | 1 |
| 10 | 25 | 1 |
| 14 | 28 | 1 |
| 20 | 10 | 0 |
| 30 | 12 | 1 |
| 48 | 5 | 0 |
| 60 | 8 | 0 |
| 72 | 4 | 0 |

New employees: (8 months, 27 hours) and (55 months, 6 hours).
**Code (what you write in the interview):**
```python
import pandas as pd
from sklearn.linear_model import LogisticRegression

employees = pd.DataFrame({
    "tenure_months": [6, 10, 14, 20, 30, 48, 60, 72],
    "overtime_hours": [30, 25, 28, 10, 12, 5, 8, 4],
    "left": [1, 1, 1, 0, 1, 0, 0, 0],
})

# features (inputs) and label (answer)
X = employees[["tenure_months", "overtime_hours"]]
y = employees["left"]

new_employees = pd.DataFrame({"tenure_months": [8, 55], "overtime_hours": [27, 6]})

model = LogisticRegression()
model.fit(X, y)                        # learn from past employees
new_pred = model.predict(new_employees)  # predict for new employees
print(new_pred)
```
**Output:**
```text
[1 0]
```
**What it means:** The model predicts the first new employee will leave (1) and the second will stay (0). With only 8 rows this is a toy; real work needs far more data and testing on unseen rows.
**Likely follow-ups:** 1) *What if X_new has different columns?* sklearn raises an error or gives wrong results; the columns must match. 2) *Why separate fit and predict?* Training once, predicting many times.
**Common mistakes:** Calling `predict` before `fit`; fitting on the test data; passing the label inside X.

### Q16 ⭐⭐⭐ 🟡 Walk through the steps of a typical machine learning project, from business question to a result the business can use.
**Asked at:** commonly asked (no company-specific report found); "project workflow" is a reported discussion topic in some analyst interviews (for example a Deloitte USI Hyderabad review, unverified).
**What the interviewer is checking:** That you see ML as a business process, not just model fitting.
**Say this in the interview:** "I start with the business question and the decision it will change, then check the data exists, clean and explore it, build a simple baseline, train and test models on unseen data, explain the result in business terms, hand it over with a plan to monitor it."
**Explain simply:**
- 1) Define the question and the action ("which employees should managers talk to first").
- 2) Get and understand the data; confirm labels exist and are reliable.
- 3) Clean it: missing values, duplicates, text columns turned into numbers.
- 4) Split into training rows and test rows, kept separate.
- 5) Build a simple baseline first (Q30), then try better models.
- 6) Evaluate with a metric that matches the business cost (later parts).
- 7) Explain the drivers and limits, check fairness and privacy.
- 8) Deliver it as a dashboard or score file, and monitor it as the world changes.
**Likely follow-ups:** 1) *Where does most time go?* Usually data preparation (common view, not a measured figure). 2) *After launch?* Track whether predictions still hold and retrain if not.
**Common mistakes:** Jumping to the algorithm; no clear action; no monitoring.

### Q17 ⭐⭐⭐ 🟡 How do you decide whether a business problem is really a machine learning problem? What would you check first?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Problem framing and data-readiness thinking.
**Say this in the interview:** "First I ask what decision will change if we have a prediction. Then I check whether there is a clear outcome to predict, enough reliable history, and whether a simpler method already does the job. If any of these is missing, it is probably not an ML problem yet."
**Explain simply:**
- Check 1: a clear decision and an owner who will act.
- Check 2: a measurable outcome (the label) defined consistently.
- Check 3: enough past rows, with features known before the outcome.
- Check 4: can a rule, query or dashboard solve it more simply?
- Check 5: can we use the data legally and fairly?
**Worked example (concept question):** "Reduce attrition" is vague. Reframed: "Flag employees likely to resign within six months so HR can hold stay conversations." That has a label, a window and an action, so it is a workable ML problem if enough history exists.
**Likely follow-ups:** 1) *What if you have no labels?* Describe with clustering or fix data collection first (Q44). 2) *What if the data is tiny?* Use descriptive analysis.
**Common mistakes:** Accepting "use AI" as a problem statement.

### Q18 ⭐⭐⭐ 🟡 Your manager says "can we use AI to predict attrition?" Which clarifying questions do you ask before touching any data?
**Asked at:** commonly asked; attrition prediction is a recurring HR dataset prompt in practice banks (snippet level, unverified).
**What the interviewer is checking:** Do you clarify scope, purpose and ethics before building?
**Say this in the interview:** "I ask what we mean by attrition, what decision it will support, what data we have and how many past leavers, who will see the scores, and what privacy and fairness rules apply. I do not start with data."
**Explain simply:**
- Definition: voluntary only, or also layoffs? Resignation within 3, 6 or 12 months?
- Action: what will managers do with a flagged employee? If nothing, the model has no value.
- Data: how many years of history, how many leavers, which systems, how reliable?
- Audience and risk: a risk score on named people is sensitive; who may see it?
- Privacy and fairness: do we have permission to use this data, and are protected traits excluded? Confirm with legal, HR and IT (rules such as India's DPDP Act or GDPR vary; from memory, unverified).
- Success: what accuracy or saving makes this worth doing, versus a simple report by team and tenure?
**Alternative / pitfalls:** Offer a first step: a dashboard of attrition by tenure and manager, before any model.
**Likely follow-ups:** 1) *Which question matters most?* The action it will drive. 2) *What if leavers are rare?* Then predictions are harder; discuss in later parts.
**Common mistakes:** Asking only technical questions; ignoring privacy and employee trust.

### Q19 ⭐⭐⭐ 🟡 Why does a supervised model need historical data with known outcomes, and what goes wrong if the labels are wrong or missing for many rows?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that labels are the model's teacher.
**Say this in the interview:** "The model learns by comparing its guesses with the real outcomes, so it needs past examples where the answer is known. If labels are wrong, it learns the wrong lesson. If many are missing, we either lose data or, worse, the labelled rows may be an unrepresentative sample."
**Explain simply:**
- No labels, no supervised learning: nothing to learn from or to score against.
- Wrong labels (for example a resignation recorded as "terminated"): the model learns noise and its measured accuracy is unreliable.
- Missing labels, not at random: for example, outcomes are only recorded for employees who completed an exit process, so the model learns about a biased subset.
- Recent employees have not had time to leave, so marking them "stayed" may be wrong (the label is not final yet).
**Worked example (concept question):** 2,000 rows; 600 have a blank `left` column because the HR system did not record contract workers. Training on the 1,400 rows teaches the model about permanent staff only; applying it to contract workers is unreliable.
**Likely follow-ups:** 1) *What can you do?* Fix labels at source, drop or relabel carefully, or use semi-supervised methods (Q39). 2) *Is a few wrong labels fatal?* Small random noise is usually tolerable; systematic errors are not.
**Common mistakes:** Filling missing labels with "No"; ignoring how labels were created.

### Q20 ⭐⭐⭐ 🟡 A stakeholder asks "why did the model flag this employee?" How do you answer without technical jargon?
**Asked at:** commonly asked; explainability is a recurring theme in attrition practice questions (snippet level, unverified).
**What the interviewer is checking:** Can you explain a prediction honestly, in business language, without blaming the person.
**Say this in the interview:** "The model compares this employee with past employees. They resemble people who left in a few ways: high overtime, short tenure and no recent promotion. That is a pattern, not a certainty, and it is a prompt for a conversation, not a judgement about the person."
**Explain simply:**
- Name the top two or three factors that pushed the score up, in plain terms (tools such as feature importance or SHAP exist for this; from memory, unverified here).
- Compare with a typical person: "Their overtime is 30 hours; the average among stayers is 12."
- Say what the model cannot know: personal reasons, a recent pay change, a new manager.
- Suggest the next step: a supportive talk, not a penalty.
- Never reveal scores to people who should not see them.
**Worked example (concept question):** "Priya was flagged at 0.62. Her overtime (30 h) is well above the 12 h typical for stayers, and her tenure is 8 months. Among past employees with that profile, roughly six in ten left. It does not mean she will leave."
**Likely follow-ups:** 1) *What if the top factor is something sensitive like age?* Raise it with the team; consider removing it. 2) *What if you cannot explain it at all?* Prefer a simpler model.
**Common mistakes:** Saying "the algorithm decided"; reading causes into patterns; sharing individual scores widely.

### Q21 ⭐⭐ 🟢 Classify each scenario as supervised or unsupervised learning and name the task type: (a) predict which loan applicants will default using past repayment records, (b) group stores by sales pattern with no labels, (c) predict house price from area and location, (d) find unusual expense claims with no past fraud labels, (e) predict whether a candidate will accept an offer using past offers.
**Asked at:** commonly asked (no company-specific report found); a fraud-context variant of the supervised vs unsupervised question is reported on prep sites (unverified).
**What the interviewer is checking:** Fast, correct classification with a reason.
**Say this in the interview:** "(a) Supervised, classification. (b) Unsupervised, clustering. (c) Supervised, regression. (d) Unsupervised, anomaly detection. (e) Supervised, classification."
**Explain simply:**
- (a) past repayment records are the labels; default or not is a category.
- (b) "no labels" and "group" mean clustering.
- (c) price is a number, so regression.
- (d) with no past fraud labels there is nothing to learn the "fraud" answer from, so we look for claims that differ from the rest; unusual does not equal fraud.
- (e) past offers with accepted or declined outcomes are labels; two categories, so classification.
**Likely follow-ups:** 1) *In (d), what happens next?* A human reviews the flagged claims. 2) *If you later collected confirmed fraud cases?* You could switch to supervised classification.
**Common mistakes:** Calling (d) classification; treating "unusual" as proven fraud.

### Q22 ⭐⭐ 🟢 Name five common machine learning algorithms and say whether each is mainly used for supervised or unsupervised learning.
**Asked at:** commonly asked (no company-specific report found); "choosing an algorithm" appears in fresher ML lists (snippet level, unverified).
**What the interviewer is checking:** Can you name common methods and place them correctly, without overclaiming.
**Say this in the interview:** "Linear regression and logistic regression, decision trees and random forests are supervised; k-means clustering is unsupervised. Linear regression predicts numbers, logistic regression predicts categories, trees and forests can do both, and k-means groups similar rows."
**Explain simply:**
- Linear regression: supervised, predicts a number (salary).
- Logistic regression: supervised, predicts a category (leave or stay).
- Decision tree: supervised, a flowchart of yes/no questions on the features; easy to read.
- Random forest: supervised, many trees voting; usually more accurate, harder to explain.
- K-means: unsupervised, groups rows around k centres.
- Other unsupervised examples: hierarchical clustering, PCA (compresses many columns into a few).
**Likely follow-ups:** 1) *Which would you start with?* Logistic regression or a small tree as a baseline (Q30). 2) *Which is easiest to explain?* A decision tree or logistic regression.
**Common mistakes:** Calling logistic regression a regression-for-numbers method; putting k-means under supervised.

### Q23 ⭐⭐ 🟢 What is clustering, in plain words, and what is one business use of it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Plain-word understanding and a sensible use.
**Say this in the interview:** "Clustering sorts rows into groups so that members of a group are alike and different from other groups, without being told the groups in advance. A retailer can cluster customers by buying behaviour and design a different offer for each group."
**Explain simply:**
- No label column; the computer proposes the groups, humans interpret and name them.
- "Alike" depends on the columns you give it, so choice of columns matters.
- The number of groups is often chosen by you, so check the groups make business sense.
- HR use: group employees by engagement survey answers to see different "types" of sentiment.
**Worked example (concept question):** 1,000 customers with columns orders per year and average order value. Clustering might reveal three groups: few small orders, many small orders, few large orders. Marketing then names and treats them differently.
**Likely follow-ups:** 1) *Is it prediction?* No, it describes. 2) *How do you know the groups are good?* Whether they are distinct, stable and actionable (Part 4).
**Common mistakes:** Treating clusters as ground truth; not scaling columns (covered in Part 4).

### Q24 ⭐⭐ 🟢 What is deep learning, and what is a neural network in simple terms?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A simple, correct picture without math, and awareness of when it is not needed.
**Say this in the interview:** "A neural network is a model made of layers of simple connected calculation units that pass numbers forward, loosely inspired by the brain. Deep learning means networks with many layers. It is powerful for images, speech and text, but for ordinary table data, simpler models are usually enough and easier to explain."
**Explain simply:**
- Each unit takes numbers in, weighs them, and passes a result on; layers build up from simple patterns to complex ones.
- Training adjusts the weights so predictions match known answers.
- It needs a lot of data and computing power, and is hard to explain.
- Analysts rarely build these; you more likely use tools built on them (from memory, general knowledge, not verified here).
**Alternative / pitfalls:** For a 5,000-row HR table, a logistic regression or random forest is usually a better first choice.
**Likely follow-ups:** 1) *When is deep learning the right tool?* Images, audio, large text collections. 2) *Is a neural network a black box?* Mostly yes, explanations are approximate.
**Common mistakes:** Claiming it "thinks like a brain"; recommending it for small tabular data.

### Q25 ⭐⭐ 🟢 Which Python library do analysts normally use for basic machine learning, and what is the common fit and predict pattern it offers?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** You know scikit-learn and its consistent interface.
**Say this in the interview:** "scikit-learn, imported as `sklearn`. Almost every model follows the same pattern: create the model, `fit` it on features and labels, then `predict` on new data. Because the pattern is the same, swapping one algorithm for another needs only one line to change."
**Explain simply:**
- Pandas holds and cleans the table; scikit-learn builds the model; statsmodels is an alternative when you want statistical output such as p-values (from the installed-library list; role described from general knowledge).
- Pattern: `model = Algorithm()`, `model.fit(X, y)`, `model.predict(X_new)`.
- Unsupervised models also use `fit` (with X only); clustering models offer `predict` or `labels_` depending on type.
- Other helpers: `train_test_split` to separate training and test rows, and metric functions to score.
**Likely follow-ups:** 1) *What is X_new?* New rows with the same columns as X. 2) *Which other libraries?* statsmodels, XGBoost (from memory, unverified).
**Common mistakes:** Forgetting that data must be numeric and free of missing values before `fit` for most models.

### Q26 ⭐⭐ 🟢 In this pandas snippet, what are X and y, and why are they separated?
```python
X = df.drop('left', axis=1)
y = df['left']
```
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you read pandas code and explain features versus label.
**Say this in the interview:** "X is the table of features, every column except `left`. y is the label, the `left` column we want to predict. They are separated because the model must learn from X and be scored against y; if `left` stayed inside X, the model would simply read the answer."
**Explain simply:**
- `df.drop('left', axis=1)` returns a copy of the table without the column `left` (`axis=1` means columns, not rows). The original `df` is unchanged.
- `df['left']` picks just that one column (a pandas Series).
- X has many columns, y has one; both have the same number of rows, in the same order.
- Note: if an ID column is still in X (as below), you would drop it too.
**Sample data:** Small made-up HR table.

| emp_id | tenure_months | overtime_hours | left |
|---|---|---|---|
| 1 | 6 | 30 | 1 |
| 2 | 30 | 12 | 0 |
| 3 | 48 | 5 | 0 |
| 4 | 12 | 26 | 1 |

**Code (what you write in the interview):**
```python
# features: everything except the answer column
X = df.drop('left', axis=1)

# label: the answer we want to predict
y = df['left']

print(X.shape, y.shape)
```
**Output:**
```text
(4, 3) (4,)
```
**What it means:** X has 4 rows and 3 columns (emp_id, tenure_months, overtime_hours); y has 4 values, one per row. In practice also drop `emp_id`.
**Likely follow-ups:** 1) *What does axis=1 mean?* Drop a column. 2) *What is the leakage risk?* Leaving the label, or something computed from it, in X.
**Common mistakes:** Forgetting `axis=1` (pandas then looks for a row named 'left' and fails); leaving the label inside X; leaving the ID in X.

### Q27 ⭐⭐ 🟢 What does "garbage in, garbage out" mean for machine learning, with an example from HR data?
**Asked at:** commonly asked (no company-specific report found); data-quality questions appear in most ML question banks (prep sites, unverified).
**What the interviewer is checking:** That you know a model is only as good as its data, and that you check data before modelling.
**Say this in the interview:** "A model learns patterns from whatever data it gets. If the data is wrong, missing or biased, the predictions will be wrong too, however clever the algorithm. In HR, if half the exit dates are blank or 'left' is recorded inconsistently, the model learns a false picture of who leaves."
**Explain simply:**
- Machine learning does not know the data is wrong; it just finds patterns, including false ones.
- Typical HR garbage: blank exit dates, the same department spelled three ways ("HR", "Human Resources", "hr"), salaries in different currencies or units, duplicate employee rows, and ratings entered by managers who rate everyone 4.
- Biased history is garbage too: if past promotions favoured one group, the model copies that.
**Worked example:** Suppose 100 resignations were recorded in the HRIS but 40 of them were left as "active" because the exit form was never filed. The model is told those 40 people stayed, so it learns that the features of people who really left (for example low engagement) are linked to staying. The analysis looks fine and the numbers look precise, but the answer is wrong.
**Alternative / pitfalls:** The fix is boring and comes first: profile the data (missing values, duplicates, odd values), agree definitions with HR (what counts as "left"?), and fix the source, not only the file.
**Likely follow-ups:** 1) *How do you check?* Counts of missing values, duplicates, min/max, category lists. 2) *Can a better algorithm fix bad data?* No; a stronger model just learns the errors more confidently.
**Common mistakes:** Jumping straight to the algorithm; treating "no data" as "no event"; saying cleaning is only an IT job.

### Q28 ⭐⭐ 🟢 Will machine learning replace data analysts? How do you see your role next to ML?
**Asked at:** commonly asked (no company-specific report found); a general "AI and your career" question.
**What the interviewer is checking:** A balanced, honest view: not defensive, not hype.
**Say this in the interview:** "I think ML and AI tools will take over the repetitive parts, like first-draft queries and routine reports, but not the job. Someone still has to define the business question, check the data, judge whether the result makes sense, and explain it to a decision maker. I see ML as a tool I use, and my HR background helps me ask the right questions."
**Explain simply:**
- ML is good at finding patterns at scale; it is not good at knowing which question matters or whether the data is trustworthy.
- The analyst frames the problem, prepares data, chooses a sensible approach (often a simple one), checks results and communicates them.
- Tools change what the analyst spends time on; the demand for judgement and domain knowledge stays.
- Nobody can promise the future, so say "I expect", not "it will never".
**Alternative / pitfalls:** Do not say "AI will never affect my job" or "I am worried"; show you already use tools (for example AI help for drafting formulas) and still verify the output.
**Likely follow-ups:** 1) *Which skills protect your role?* Business understanding, data checking, communication. 2) *How do you use AI today?* As an assistant for drafts, always verified, never with real employee data in public tools.
**Common mistakes:** Giving a one-sided answer; ignoring that you must validate AI output yourself.

### Q29 ⭐⭐ 🟢 How does the work of a data analyst differ from that of a data scientist and an ML engineer?
**Asked at:** commonly asked (no company-specific report found); many analyst loops include a "where does this role sit" question.
**What the interviewer is checking:** That you understand the roles and know where you fit.
**Say this in the interview:** "The analyst answers business questions from data with SQL, Excel, dashboards and statistics. The data scientist builds predictive models and runs experiments. The ML engineer puts models into production so they run reliably on live data. Titles overlap between companies, and I would sit at the first, sometimes touching simple models."
**Explain simply:**
- **Data analyst:** "What happened and why?" (attrition by department, sales dashboard). Tools: SQL, Excel, Power BI, some Python.
- **Data scientist:** "What will happen, and what should we do?" Builds and tests models (who is likely to leave), more statistics and Python.
- **ML engineer:** "How do we run this model every day without it breaking?" Code, pipelines, monitoring, deployment.
- Analogy: analyst reads the map, scientist designs a new route, engineer builds and maintains the road.
**Alternative / pitfalls:** Job titles vary by company, especially in small teams where one person does all three; say so rather than claim a rigid split.
**Likely follow-ups:** 1) *Where do you want to grow?* Pick one honestly, for example toward predictive HR analytics. 2) *Does an analyst ever build a model?* Yes, simple ones such as a baseline or a regression.
**Common mistakes:** Saying analysts "only make charts"; claiming you can do all three roles on day one.

### Q30 ⭐⭐ 🟢 What is a baseline model, and why should you build one before anything complicated?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you measure improvement against something, and know a fancy model must beat a simple one.
**Say this in the interview:** "A baseline is the simplest sensible prediction, for example always guessing the most common outcome, or last month's value. It sets the bar. If my model cannot beat it clearly, the extra complexity is not worth it."
**Explain simply:**
- Without a baseline, "81% accurate" means nothing. If 69% of employees stay, always saying "stays" already scores 69%.
- Baselines: most frequent class (classification), the average or last value (numbers), or a business rule such as "tenure under 12 months leaves".
- It also checks your pipeline: if a baseline looks suspiciously good, suspect a data problem.
**Sample data:** `employees` is a 400-row practice table (simulated, seed 42) with `tenure_months`, `overtime_hours` and `left` (1 = left); about 31% left.
**Code (what you write in the interview):**
```python
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X = employees[['tenure_months', 'overtime_hours']]
y = employees['left']

# Hold back a test set so we judge on rows the model has not seen
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

# Baseline: always predict the most common outcome
baseline = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
model = LogisticRegression().fit(X_train, y_train)

print('baseline accuracy:', baseline.score(X_test, y_test))
print('model accuracy:', model.score(X_test, y_test))
```
**Output:**
```text
baseline accuracy: 0.69
model accuracy: 0.81
```
**What it means:** Doing nothing clever gets 69%; the model gets 81%, so it adds real value. Report both numbers to a manager, not just the model's.
**Alternative / pitfalls:** With rare outcomes, accuracy hides a lot (see Q47); also compare on a metric that matches the business goal.
**Likely follow-ups:** 1) *What if the model barely beats the baseline?* Use the simpler option or improve the data. 2) *Is a rule a valid baseline?* Yes (see Q48).
**Common mistakes:** Quoting accuracy with no baseline; building the complex model first.

### Q31 ⭐⭐ 🟢 Name three ways machine learning is used in HR analytics.
**Asked at:** commonly asked (no company-specific report found); attrition prediction appears as an HR dataset prompt on prep sites (unverified).
**What the interviewer is checking:** Realistic domain examples, with awareness of limits.
**Say this in the interview:** "Attrition prediction to flag teams at risk, resume screening support to shortlist faster, and workforce planning, such as forecasting hiring needs. Others are grouping employees by engagement pattern and analysing survey comments. All need human review, because decisions affect people."
**Explain simply:**
- **Attrition risk:** predict who may leave, from tenure, pay, overtime and engagement, so HR can act early (a conversation, not a punishment).
- **Resume screening / matching:** rank applications against a role; high risk of copying past bias, so humans decide.
- **Workforce forecasting:** predict headcount or hiring volume from past patterns and business plans.
- Also: clustering employees by behaviour, text analysis of survey comments, predicting time to hire.
**Alternative / pitfalls:** Mention fairness and privacy (Q54, Q55); a prediction is a prompt for a conversation, not a verdict.
**Likely follow-ups:** 1) *Which would you start with?* Attrition risk by team, on aggregate, because the data usually exists. 2) *What data?* HRIS records, exit dates, survey scores.
**Common mistakes:** Listing buzzwords with no example; ignoring bias and privacy.

### Q32 ⭐⭐ 🟢 Name three ways machine learning is used in e-commerce.
**Asked at:** commonly asked (no company-specific report found); the sources search for Flipkart/Swiggy/Meesho ML questions failed, so no company claim is made.
**What the interviewer is checking:** That you connect ML to a concrete business outcome.
**Say this in the interview:** "Recommendations ('customers also bought'), demand forecasting for stock planning, and fraud or return-abuse detection. Others are dynamic pricing and customer segmentation."
**Explain simply:**
- **Recommendations:** learn from what similar customers bought and suggest items; raises basket size.
- **Demand forecasting:** predict next month's sales per product so warehouses are not overstocked or empty.
- **Fraud detection:** flag unusual orders or payments for review.
- Also: customer segments for campaigns, search ranking, churn prediction.
**Alternative / pitfalls:** Name the metric each one moves (conversion, stock-outs, fraud loss), which shows analyst thinking.
**Likely follow-ups:** 1) *Supervised or unsupervised?* Fraud with past labels is supervised; segmentation is unsupervised. 2) *How would you check a recommender works?* Compare with a control group (A/B test).
**Common mistakes:** Naming only "recommendations"; not linking ML to a business result.

### Q33 ⭐⭐ 🟢 Name three ways machine learning is used in banking and finance.
**Asked at:** commonly asked (no company-specific report found); a fraud context appears in supervised-vs-unsupervised question variants (prep sites, unverified).
**What the interviewer is checking:** Domain awareness and attention to risk and regulation.
**Say this in the interview:** "Credit scoring, to estimate whether a borrower will repay; fraud detection on transactions; and customer churn or cross-sell models. Because lending decisions affect people, banks need models they can explain."
**Explain simply:**
- **Credit scoring:** predict default risk from past repayment records (supervised).
- **Fraud detection:** flag unusual transactions; rare events, so often combined with unsupervised anomaly detection (Q43).
- **Churn and cross-sell:** predict who may close an account or accept a product.
- Also: collections prioritisation, forecasting, document processing.
**Alternative / pitfalls:** Mention explainability and regulation in general terms; specific rules vary by country (check with compliance, from memory, unverified).
**Likely follow-ups:** 1) *Why must credit models be explainable?* A customer or regulator may ask why a loan was refused. 2) *Why is fraud hard?* Very few fraud cases among many normal ones.
**Common mistakes:** Forgetting fairness and explainability; treating fraud as a balanced problem.

### Q34 ⭐⭐ 🟢 Classify each column as numeric, categorical, date, text or identifier, and say which are useful as features.
Columns: emp_id, joining_date, grade (A/B/C), monthly_salary, manager_comment, city, performance_rating (1-5)
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can look at a column and decide how it is used in a model.
**Say this in the interview:** "emp_id is an identifier, so no. joining_date is a date; I turn it into tenure. grade and city are categorical. monthly_salary is numeric. manager_comment is free text, usable only with text processing. performance_rating is ordered categories stored as numbers."
**Explain simply:** A **feature** is an input column the model learns from.

| Column | Type | Use as feature? |
|---|---|---|
| emp_id | identifier | No: a unique label with no meaning; it only lets the model memorise people |
| joining_date | date | Not raw; convert to tenure in months (today minus joining date) |
| grade (A/B/C) | categorical (ordered) | Yes, after converting to numbers (Q41) |
| monthly_salary | numeric | Yes |
| manager_comment | text | Not as it is; needs text processing, and may carry bias or leak outcomes |
| city | categorical | Yes, with care if it has many values |
| performance_rating (1-5) | ordered categorical (stored as number) | Yes; treat as a number if gaps are even, else as categories |

**Alternative / pitfalls:** Check each feature would be known at prediction time (leakage, see Q46), and that sensitive fields are justified (Q55, Q57).
**Likely follow-ups:** 1) *How to use a date?* Extract tenure, month or day of week. 2) *Is a rating numeric?* It looks numeric but 4 is not exactly "twice" 2.
**Common mistakes:** Feeding emp_id into the model; using raw dates or text directly.

### Q35 ⭐⭐ 🟢 A trained model is: predicted_salary = 25000 + 4000 x years_experience. Predict the salary for a candidate with 3 years, and explain what the model has "learned".
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can use a fitted model and describe its two learned numbers in plain words.
**Say this in the interview:** "25000 + 4000 x 3 = 37,000. The model learned two numbers from past salary data: a starting point of 25,000 and an extra 4,000 for each year of experience. It is a pattern in past data, not a rule of nature."
**Explain simply:**
- 25,000 is the **intercept**: the predicted salary at zero years.
- 4,000 is the **coefficient** (slope): the predicted rise per extra year.
- Those two numbers are the **parameters** the model "learned" by fitting a straight line through past (experience, salary) pairs.
- Treat it as a rough estimate: it ignores role, city and skills, and may be unreliable far outside the experience range it saw (for example 30 years).
**Code (what you write in the interview):**
```python
years_experience = 3
predicted_salary = 25000 + 4000 * years_experience
print(predicted_salary)
```
**Output:**
```text
37000
```
**What it means:** The model estimates 37,000 per month for 3 years. Report it as "about 37,000" with a note that real offers vary.
**Alternative / pitfalls:** Extrapolation: do not predict for experience values far beyond the training data.
**Likely follow-ups:** 1) *What would 0 years give?* 25,000. 2) *Is this ML?* Yes, simple linear regression is the most basic form.
**Common mistakes:** Saying 4,000 is the salary instead of the increase per year; trusting predictions far outside the data.

### Q36 ⭐⭐ 🟢 After loading a CSV for modelling, what does df.shape tell you and how do you read rows and columns in ML language?
print(df.shape)  # (5000, 12)
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you connect pandas structure to ML vocabulary.
**Say this in the interview:** "(5000, 12) means 5,000 rows and 12 columns. In ML language, rows are observations or samples, here 5,000 employees, and columns are variables: usually one target and the rest features, so about 11 features if one column is the label."
**Explain simply:**
- `shape` is (rows, columns); it is an attribute, so no brackets.
- A **sample** (row) is one example, such as one employee. A **feature** (column) is an input. The **label** or target is what you predict (for example `left`).
- 5,000 samples is a modest size; the number of features vs rows tells you how much the model can safely learn.
- Some columns are IDs or dates and should not be features, so usable features are fewer than 11.
**Sample data:** a tiny table of 4 rows and 3 columns, to show the idea.
**Code (what you write in the interview):**
```python
import pandas as pd

df = pd.DataFrame({'emp_id': [1, 2, 3, 4],
                   'age': [25, 31, None, 40],
                   'dept': ['HR', 'IT', 'IT', None]})

rows, columns = df.shape
print(df.shape)
print('samples:', rows, 'columns:', columns)
```
**Output:**
```text
(4, 3)
samples: 4 columns: 3
```
**What it means:** 4 employees (samples), 3 columns. In the question, 5,000 samples and 12 columns.
**Alternative / pitfalls:** Always also check data types and missing values (Q37).
**Likely follow-ups:** 1) *Is more data always better?* More good data helps; more rows of bad data does not. 2) *How do you count features?* Columns minus the label and IDs.
**Common mistakes:** Writing `df.shape()` with brackets; mixing up rows and columns; counting the label as a feature.

### Q37 ⭐⭐ 🟢 Why do analysts check df.isna().sum() before building a model?
print(df.isna().sum())
**Asked at:** commonly asked (no company-specific report found); missing data appears in fresher ML question lists (prep sites, unverified).
**What the interviewer is checking:** That you check data quality first and know missing values need a decision.
**Say this in the interview:** "Many models cannot handle blanks and some libraries throw an error. It also tells me how complete each column is, and whether blanks are random or a pattern. Then I decide: drop the column, drop the rows, or fill the values."
**Explain simply:**
- `df.isna()` marks each blank as True; `.sum()` counts them per column.
- A column that is 60% empty is probably not usable; a column with 1% blank can be filled.
- Fill with a typical value (median for numbers, most common for categories), and add the fact "was missing" if it matters.
- Do the filling using only training data to avoid leakage (Part 6).
**Sample data:** the small `df` below with a blank age and a blank department.
**Code (what you write in the interview):**
```python
import pandas as pd

df = pd.DataFrame({'emp_id': [1, 2, 3, 4],
                   'age': [25, 31, None, 40],
                   'dept': ['HR', 'IT', 'IT', None]})

print(df.isna().sum())
```
**Output:**
```text
emp_id    0
age       1
dept      1
dtype: int64
```
**What it means:** `age` and `dept` each have one blank; `emp_id` is complete. Next step: decide how to treat those two.
**Alternative / pitfalls:** Blanks can hide as "NA", 0, or 999, which `isna()` will not find; scan value counts too.
**Likely follow-ups:** 1) *Mean or median?* Median when there are outliers (salary). 2) *Are blanks always errors?* No; a blank exit date can mean "still employed".
**Common mistakes:** Dropping all rows with a blank (losing most data); filling before splitting the data; missing disguised blanks.

### Q38 ⭐⭐ 🟢 Coming from an HR background, how would you use machine learning on HR data in your first year as an analyst?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Realism, a sensible plan, and whether you turn your HR knowledge into an advantage.
**Say this in the interview:** "First two to three months: clean and understand the data and build descriptive reports on attrition and hiring. Then a simple, explainable attrition risk model with a baseline, shown at team level. I would involve HR leaders early, check fairness and privacy, and only then consider anything more advanced."
**Explain simply:**
- **Months 1-3:** learn the data, fix quality problems, agree definitions (what is "attrition"?), build dashboards.
- **Months 4-6:** pick one business question with a clear action, such as which teams have high early attrition. Build a baseline, then a simple model (logistic regression or a small decision tree).
- **Months 7-12:** test it, explain drivers in plain words, pilot with one function, and measure whether the action reduced exits.
- My HR advantage: I know what the columns really mean and which actions HR can take.
**Alternative / pitfalls:** Avoid promising a magic model. State that small data and bias limit what is possible.
**Likely follow-ups:** 1) *What if you have little data?* Start with descriptive analysis and simple rules (Q60). 2) *Which first project?* Attrition by tenure band, with a cost-benefit view (Q50).
**Common mistakes:** Proposing deep learning on 300 rows; ignoring privacy and fairness; no link to an action.

### Q39 ⭐⭐ 🟡 What is semi-supervised learning, and when does it make sense for a company with few labelled rows?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the middle ground between labelled and unlabelled data.
**Say this in the interview:** "Semi-supervised learning uses a small labelled set plus a large unlabelled set. The labelled rows teach the model what to predict; the unlabelled rows help it see the overall structure of the data. It makes sense when labelling is expensive, like checking a few hundred resumes by hand."
**Explain simply:**
- **Labelled** rows have the answer (hired or rejected); **unlabelled** rows do not.
- Common approach: train on labelled rows, predict labels for the rest, keep the confident predictions, retrain. This is called self-training.
- Worth it when labelled rows are few, unlabelled rows are many, and both come from the same kind of data.
- Risk: early mistakes get repeated and reinforced.
**Worked example:** 200 resumes with outcomes and 800 without (Q51). A semi-supervised method could use the 800 to learn what resumes look like, but you must check its labels against a fresh set of human-labelled rows.
**Alternative / pitfalls:** Often a simpler path is better: label more rows, or use the 200 you have with a simple model.
**Likely follow-ups:** 1) *Does it replace labelling?* No, you still need some trusted labels to check results. 2) *Is it common for analysts?* Rarely; know the idea.
**Common mistakes:** Treating the model's own guesses as ground truth; skipping validation on human-labelled rows.

### Q40 ⭐⭐ 🟡 Name three problems that unsupervised learning solves, besides clustering, with a business example each.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That unsupervised learning is more than clustering.
**Say this in the interview:** "Anomaly detection, dimensionality reduction, and association rules. Examples: unusual expense claims, shrinking 40 survey questions into a few themes, and 'customers who buy X also buy Y'."
**Explain simply:** **Unsupervised** means no label column; the model looks for structure on its own.
- **Anomaly detection:** find rows unlike the rest (an expense claim far outside normal, with no fraud labels).
- **Dimensionality reduction (for example PCA):** compress many related columns into a few summary ones (40 engagement questions become 3 themes such as workload, manager, growth).
- **Association rules (market basket):** find items bought together (laptop and laptop bag), used for bundling and shelf placement.
- Also: topic discovery in text (themes in exit-interview comments).
**Alternative / pitfalls:** There is no "right answer" to check against, so results need business judgement.
**Likely follow-ups:** 1) *How do you know a result is good?* Does it make business sense and lead to action? 2) *Is clustering unsupervised?* Yes (Q23).
**Common mistakes:** Saying unsupervised learning "has no use without labels"; trusting the output with no sense-check.

### Q41 ⭐⭐ 🟡 Why do we convert categorical columns such as department into numbers before modelling?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know models do arithmetic, and how to encode text fairly.
**Say this in the interview:** "Models do maths, so they need numbers. A word like 'HR' means nothing to them. I use one-hot encoding: one 0/1 column per department. I avoid just numbering departments 1, 2, 3 because that invents a false order."
**Explain simply:**
- **Categorical** means a column with a limited set of labels (department, city).
- **One-hot encoding:** a new column per value; 1 if the row has it, 0 otherwise.
- Numbering HR=1, IT=2, Sales=3 would tell the model "Sales is three times HR", which is meaningless.
- Ordered categories (grade A/B/C, or low/medium/high) can be numbered 1, 2, 3 because order is real.
**Sample data:** 4 employees from HR, IT, Sales, IT.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({'department': ['HR', 'IT', 'Sales', 'IT']})

# One 0/1 column per department
encoded = pd.get_dummies(employees, columns=['department'], dtype=int)
print(encoded)
```
**Output:**
```text
   department_HR  department_IT  department_Sales
0              1              0                 0
1              0              1                 0
2              0              0                 1
3              0              1                 0
```
**What it means:** Each department is now its own yes/no column the model can use.
**Alternative / pitfalls:** Many categories (hundreds of cities) create too many columns; group rare ones as "Other". Some models also drop one column to avoid duplication.
**Likely follow-ups:** 1) *One-hot vs label encoding?* One-hot for unordered; numbers for ordered. 2) *New department at prediction time?* It must be handled, or the pipeline errors.
**Common mistakes:** Numbering unordered categories; encoding before splitting and then having mismatched columns in train and test.

### Q42 ⭐⭐ 🟡 What is the difference between a model parameter and a hyperparameter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know what the model learns versus what you set.
**Say this in the interview:** "Parameters are learned by the model from the data, like the slope and intercept in a regression. Hyperparameters are settings I choose before training, like the number of clusters or the depth of a tree."
**Explain simply:**
- **Parameter:** found during `fit()`. In salary = 25000 + 4000 x years (Q35), 25000 and 4000 are parameters.
- **Hyperparameter:** chosen by you, not learned: `n_clusters=3`, `max_depth=3`, number of neighbours.
- Hyperparameters are tried and compared (tuning) on data kept aside from the final test.
- Analogy: parameters are what a student learns; hyperparameters are how many hours per day you set for study.
**Alternative / pitfalls:** Tuning many settings on the test set makes the test result too optimistic.
**Likely follow-ups:** 1) *How do you pick hyperparameters?* Try a few values and compare with cross-validation or a validation set. 2) *Example in KMeans?* `n_clusters` is a hyperparameter; the cluster centres are learned.
**Common mistakes:** Mixing the two up; tuning on the final test data.

### Q43 ⭐⭐ 🟡 What is anomaly detection, and when is it supervised versus unsupervised?
**Asked at:** commonly asked (no company-specific report found); fraud appears in supervised-vs-unsupervised question variants (prep sites, unverified).
**What the interviewer is checking:** That you choose the method by whether past anomalies are labelled.
**Say this in the interview:** "Anomaly detection finds records that are very different from normal ones, like an unusual expense claim. If I have past cases labelled fraud or not, I can train a supervised classifier. If I have no labels, I use unsupervised methods that learn what normal looks like and flag what does not fit."
**Explain simply:**
- **Anomaly** (outlier) means a rare, unusual record; it is not automatically wrong or fraud.
- **Supervised:** enough labelled examples of both normal and bad cases. Frauds are rare, so the data is badly unbalanced (Q47).
- **Unsupervised:** no labels; flag records far from the typical pattern (for example by amount, time, frequency).
- Flagged items go to a human to check; the output is a "look at this" list, not a verdict.
**Worked example:** 10,000 expense claims, no fraud labels: flag the claims with the highest amounts relative to the employee's grade. Reviewers check the top 50 and the confirmed cases become labels for a supervised model later.
**Alternative / pitfalls:** Simple rules or statistics (a threshold, z-score) are often a good first step and easy to explain.
**Likely follow-ups:** 1) *Does an anomaly mean fraud?* No, it may be a genuine one-off. 2) *How do you get labels?* From reviewed cases.
**Common mistakes:** Treating every flag as guilt; claiming supervised works without enough labelled cases.

### Q44 ⭐⭐ 🟡 You have 20,000 customer records and none are labelled with an outcome. What can you do with machine learning, and what can you not do?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know unlabelled data limits you to unsupervised work.
**Say this in the interview:** "With no outcome column I cannot train a supervised model to predict anything, like churn. I can do unsupervised work: group customers into segments, find unusual records, and summarise patterns. To predict an outcome, I would first need to define and collect that outcome."
**Explain simply:**
- **Can do:** clustering into segments, anomaly detection, dimension reduction, association (what is bought together), and exploration.
- **Cannot do:** predict churn, spend or default, or measure accuracy, because there is no correct answer to learn from or check against.
- **Next step:** define an outcome (for example "no purchase in 90 days = churned") from history, or start recording one, then build a supervised model.
- Check that a derived outcome is not built from the same columns used as inputs (leakage).
**Alternative / pitfalls:** Clusters are descriptions, not truths; name and validate them with business people.
**Likely follow-ups:** 1) *Can you create labels?* Often yes, from past behaviour (purchased again or not). 2) *Is 20,000 rows enough for clustering?* Usually plenty.
**Common mistakes:** Promising predictions with no labels; skipping the question "what do we want to predict?".

### Q45 ⭐⭐ 🟡 Trace the unsupervised code below. What does it return, and why is there no y?
```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3, n_init=10, random_state=0)
km.fit(X)
print(km.labels_[:5])
```
**Asked at:** commonly asked (no company-specific report found); sklearn code reading is a typical screen.
**What the interviewer is checking:** That you can read a fit call and know unsupervised learning has no label column.
**Say this in the interview:** "It creates a k-means model asking for 3 groups, fits it to X, then prints the group number given to the first five rows. There is no y because there is no correct answer to learn from; the model finds the groups itself."
**Explain simply:**
- `n_clusters=3`: I ask for 3 groups (a hyperparameter, Q42).
- `n_init=10`: try 10 random starting positions and keep the best.
- `random_state=0`: fixes the randomness so the result repeats.
- `fit(X)` takes only inputs; `labels_` holds one group number per row. The numbers 0, 1, 2 are arbitrary names; they do not mean good or bad.
**Sample data:** X is not given in the question; here is a made-up 8-row version (tenure_months, overtime_hours). Output depends on the data and seed.
```python
import pandas as pd
X = pd.DataFrame([[2, 10], [3, 12], [24, 3], [30, 2], [60, 0], [55, 1], [4, 11], [28, 2]],
                 columns=['tenure_months', 'overtime_hours'])
```
**Output:**
```text
[2 2 1 1 0]
```
**What it means:** The first two rows (short tenure, high overtime) share group 2, the next two share group 1, the fifth is in group 0. K-means steps are covered in Part 4.
**Alternative / pitfalls:** Scale features first if they are on different units; and choose the number of clusters with judgement.
**Likely follow-ups:** 1) *Does label 2 mean anything?* No, just a name. 2) *Why random_state?* For repeatable results.
**Common mistakes:** Looking for y; reading cluster numbers as rankings.

### Q46 ⭐⭐ 🟡 Spot the mistake in this snippet before it is used to predict attrition.
```python
X = df[['age','tenure_months','left']]
y = df['left']
model.fit(X, y)
```
**Asked at:** commonly asked (no company-specific report found); data leakage is a common ML interview theme (community question banks, mostly data scientist roles, unverified).
**What the interviewer is checking:** That you spot target leakage.
**Say this in the interview:** "The label `left` is also inside X, so the model is given the answer. It will score almost perfectly in testing and be useless in real life, because for a current employee we do not know `left`. X should only contain age and tenure_months."
**Explain simply:**
- **Label (target):** what we predict. **Features:** what we use to predict it.
- **Leakage:** a feature that carries the answer, or information only known afterwards.
- A model that finds the answer in X can just copy it, so scores look amazing but are fake.
- Related leakage: exit-interview score, notice period date, or "final settlement paid" are only known after someone leaves.
**Code (what you write in the interview):**
```python
# Features exclude the label
X = df[['age', 'tenure_months']]
y = df['left']
model.fit(X, y)
```
**What it means:** Now the model must learn from age and tenure only, which is what it will have for current staff.
**Alternative / pitfalls:** If a result looks too good (near 100%), suspect leakage first.
**Likely follow-ups:** 1) *Other leaky columns?* Anything created after the exit. 2) *How would you notice?* Perfect accuracy, or one feature dominating.
**Common mistakes:** Celebrating a 99% score; forgetting to drop IDs and after-the-fact columns.

### Q47 ⭐⭐ 🟡 A model predicts that nobody will leave. In a team of 200 employees, 30 left last year. What accuracy does this useless model get, and what does it teach you about judging a model?
**Asked at:** commonly asked (no company-specific report found); class imbalance is a common ML interview theme (community question banks, unverified).
**What the interviewer is checking:** That you see why accuracy misleads on rare outcomes.
**Say this in the interview:** "It is right for the 170 who stayed and wrong for the 30 who left: 170 out of 200, so 85% accuracy, while finding none of the leavers. So accuracy alone is misleading when one outcome is rare; I would also look at how many leavers it catches."
**Explain simply:**
- Accuracy = correct predictions / all predictions = 170 / 200 = 0.85.
- The model catches 0 of 30 leavers (called **recall**, here 0%), which is the whole point of an attrition model.
- Lesson: always compare to a baseline (this one is the baseline!) and use measures that fit the goal. Metrics are covered in Part 5.
**Sample data:** 30 leavers (label 1) and 170 stayers (label 0).
**Code (what you write in the interview):**
```python
from sklearn.metrics import accuracy_score, recall_score

actual = [1] * 30 + [0] * 170
predicted = [0] * 200

print('accuracy:', accuracy_score(actual, predicted))
print('recall:', recall_score(actual, predicted))
```
**Output:**
```text
accuracy: 0.85
recall: 0.0
```
**What it means:** 85% looks good but the model finds none of the people who left. Tell a manager: "accuracy 85%, but it catches 0 of 30 leavers."
**Alternative / pitfalls:** Rebalancing, class weights, and the right metric are the usual fixes (Q59).
**Likely follow-ups:** 1) *What would you look at instead?* Recall and precision for leavers. 2) *What is the baseline here?* Always predict "stays".
**Common mistakes:** Quoting accuracy alone; calling 85% a good model.

### Q48 ⭐⭐ 🟡 Compare a simple rule with a model. The rule: tenure under 12 months means will leave. Use the 10 rows below to count how many the rule gets right.
tenure_months / left: 5/Yes, 8/Yes, 10/No, 11/Yes, 14/No, 20/No, 7/Yes, 30/No, 9/No, 40/No
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can test a rule on data and treat it as a baseline for a model.
**Say this in the interview:** "The rule is right on 8 of 10 rows: 80%. It catches all 4 leavers, but wrongly flags 2 stayers. A model must beat this, and it is also easy to explain. The 'always No' baseline would get 6 of 10."
**Explain simply:**
- Apply the rule to each row: tenure below 12 means predict Yes.
- Rows 10/No and 9/No are wrong (predicted Yes, actually stayed); all others match.
- Correct: 5, 8, 11, 7 (leavers) plus 14, 20, 30, 40 (stayers) = 8.
- Rule vs a model: a model finds the cut-off or combines columns itself; a rule is transparent. Only 10 rows is far too few to trust any of this.
**Sample data:**

| tenure_months | left | rule says | correct? |
|---|---|---|---|
| 5 | Yes | Yes | yes |
| 8 | Yes | Yes | yes |
| 10 | No | Yes | no |
| 11 | Yes | Yes | yes |
| 14 | No | No | yes |
| 20 | No | No | yes |
| 7 | Yes | Yes | yes |
| 30 | No | No | yes |
| 9 | No | Yes | no |
| 40 | No | No | yes |

**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    'tenure_months': [5, 8, 10, 11, 14, 20, 7, 30, 9, 40],
    'left': ['Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'No']})

# Rule: under 12 months means will leave
employees['rule_prediction'] = employees['tenure_months'].apply(
    lambda months: 'Yes' if months < 12 else 'No')

correct = (employees['rule_prediction'] == employees['left']).sum()
print('rule correct:', correct, 'of', len(employees))
```
**Output:**
```text
rule correct: 8 of 10
```
**What it means:** 80% right, versus 60% for always saying "No". Good for a first rule, but on 10 rows the figure is very uncertain.
**Alternative / pitfalls:** Test the rule on rows not used to invent it; small samples mislead.
**Likely follow-ups:** 1) *Why use a rule?* Easy to explain and a strong baseline. 2) *When prefer a model?* When many columns interact.
**Common mistakes:** Judging on 10 rows as if it were proof; not comparing with the do-nothing baseline.

### Q49 ⭐⭐ 🟡 Predict with a one-nearest-neighbour idea: copy the label of the closest known employee. Who is closest to a new employee, and what is the prediction?
```python
Known (tenure_months, overtime_hours/week): A (6, 12) Left; B (30, 2) Stayed; C (10, 10) Left; D (48, 0) Stayed
New employee: (9, 11)
```
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can compute a simple distance and apply nearest-neighbour logic.
**Say this in the interview:** "I measure straight-line distance from the new employee to each known one. C is closest at about 1.41, so I copy C's label: Left."
**Explain simply:**
- Distance = square root of (difference in tenure squared + difference in overtime squared).
- A: sqrt(3^2 + 1^2) = 3.16. B: 22.85. C: sqrt(1^2 + 1^2) = 1.41. D: 40.52.
- The smallest is C, labelled Left, so predict Left. This is "1-nearest-neighbour": the model just remembers examples.
- Caution: tenure and overtime are on different scales; usually you scale columns first so one does not dominate. Here C is closest by a clear margin.
**Code (what you write in the interview):**
```python
known = {'A': (6, 12, 'Left'), 'B': (30, 2, 'Stayed'),
         'C': (10, 10, 'Left'), 'D': (48, 0, 'Stayed')}
new_tenure, new_overtime = 9, 11

for name, (tenure, overtime, label) in known.items():
    distance = ((tenure - new_tenure) ** 2 + (overtime - new_overtime) ** 2) ** 0.5
    print(name, round(distance, 2), label)
```
**Output:**
```text
A 3.16 Left
B 22.85 Stayed
C 1.41 Left
D 40.52 Stayed
```
**What it means:** C is nearest, so the prediction is Left. With 4 known people this is only an illustration.
**Alternative / pitfalls:** Real k-nearest neighbours uses several neighbours (k > 1) and scaled features, to avoid being thrown by one odd record.
**Likely follow-ups:** 1) *Why scale features?* Otherwise the column with big numbers decides. 2) *Why k > 1?* Less sensitive to a single noisy neighbour.
**Common mistakes:** Forgetting the square root (the order stays the same, but the numbers differ); picking the farthest point.

### Q50 ⭐⭐ 🟡 Estimate whether an attrition model is worth building using the hypothetical figures below.
500 employees; 12% leave each year; each exit costs about 3 lakh; assume a model-led retention effort could prevent 10% of exits; model and effort cost 12 lakh per year.
**Asked at:** commonly asked (no company-specific report found); a cost-benefit gap-fill question.
**What the interviewer is checking:** That you tie a model to money and test the assumptions.
**Say this in the interview:** "500 x 12% is 60 exits a year, costing 180 lakh. Preventing 10% saves 6 exits, 18 lakh. Costs are 12 lakh, so net benefit is about 6 lakh a year, a 50% return. It is positive but thin; it depends heavily on the 10% assumption. Break-even is 4 exits prevented (about 6.7%)."
**Explain simply:**
- Exits per year: 500 x 0.12 = 60. Annual cost of exits: 60 x 3 = 180 lakh.
- Exits prevented: 60 x 0.10 = 6. Money saved: 6 x 3 = 18 lakh.
- Net = 18 - 12 = 6 lakh. Return = 6 / 12 = 50%.
- Break-even: 12 lakh / 3 lakh per exit = 4 exits, which is 4 / 60 = 6.7% of exits.
- All inputs are hypothetical; in real life, test the prevention rate with a pilot.
**Code (what you write in the interview):**
```python
employees = 500
exit_rate = 0.12
cost_per_exit = 3        # lakh
prevention_rate = 0.10
yearly_cost = 12         # lakh

exits = employees * exit_rate
exits_prevented = exits * prevention_rate
savings = exits_prevented * cost_per_exit
net_benefit = savings - yearly_cost

print('exits per year:', exits)
print('exits prevented:', exits_prevented)
print('savings (lakh):', savings)
print('net benefit (lakh):', net_benefit)
```
**Output:**
```text
exits per year: 60.0
exits prevented: 6.0
savings (lakh): 18.0
net benefit (lakh): 6.0
```
**What it means:** A net gain of about 6 lakh a year on these assumptions. If prevention is only 5% (3 exits, 9 lakh), it loses 3 lakh, so say it is worth a pilot, not a certainty.
**Alternative / pitfalls:** Add indirect costs (hiring, training, lost output) for a fuller picture; beware optimistic assumptions. A model also predicts exits, but prevention needs an action.
**Likely follow-ups:** 1) *What if prevention is 5%?* 3 exits, 9 lakh saved, net -3 lakh. 2) *Does the model itself prevent exits?* No; the retention action does.
**Common mistakes:** Forgetting the action cost; treating assumptions as facts.

### Q51 ⭐⭐ 🟡 Using the hypothetical counts below, can you train a supervised model, and what would you do with the rest?
1,000 resumes in the file; 200 have a hired or rejected outcome recorded; 800 have no outcome.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know only labelled rows train a supervised model, and how to use the rest sensibly.
**Say this in the interview:** "Yes, but only on the 200 labelled resumes; the 800 have no answer to learn from. 200 is small, so I would keep the model simple, test on held-out rows, and be modest about reliability. The 800 can be used for exploration, clustering, or labelled by hand, or by a semi-supervised method."
**Explain simply:**
- Supervised learning needs a label for each training row: 200 usable rows.
- Hired vs rejected is itself a human decision, so it may carry past bias (Q54). Also, rejected resumes may never have been interviewed.
- Use of the 800: look at them descriptively, cluster them, score them only as a "second opinion", or label some manually (HR review) to grow training data.
- Check how many are in each class (for example how many hired); too few of one makes a model weak.
**Alternative / pitfalls:** A model that ranks candidates affects people; keep a human in the loop and check fairness. Semi-supervised learning (Q39) is possible but needs care.
**Likely follow-ups:** 1) *Can you predict outcomes for the 800?* Yes, but treat them as unverified guesses. 2) *How would you get more labels?* Review and label a sample of the 800.
**Common mistakes:** Training on all 1,000 as if the blanks were "rejected"; auto-rejecting using model scores.

### Q52 ⭐⭐ 🟡 What is AutoML, and should an analyst use it?
**Asked at:** commonly asked (no company-specific report found). AutoML tool features and licensing are from memory, unverified; confirm with official documentation.
**What the interviewer is checking:** A balanced view: useful tool, but not a substitute for understanding.
**Say this in the interview:** "AutoML tools try many models and settings automatically and pick the best. As an analyst I would use it to get a fast baseline or compare options, but I would still check the data, avoid leakage, understand what the chosen model does, and be able to explain it. I would not paste in real employee data to an outside online tool without approval."
**Explain simply:**
- **AutoML** automates steps such as trying algorithms, tuning settings and comparing scores.
- Good for: quick baselines, saving time, checking whether a signal exists at all.
- Limits: it cannot fix bad data or leakage, it may pick a black box that is hard to explain, and it optimises whatever metric you give it.
- Always verify: check the score against a simple baseline, test on held-out rows, and look at which features it uses.
- Privacy: sensitive HR data should only go to tools approved by IT or legal.
**Alternative / pitfalls:** The danger is a high score you cannot explain, built on a leaked column.
**Likely follow-ups:** 1) *Does AutoML replace the analyst?* No: framing, data and interpretation stay human. 2) *Can you trust the top model?* Only after checking leakage and a baseline.
**Common mistakes:** Treating the AutoML score as final; uploading confidential data; not being able to explain the winning model.

### Q53 ⭐⭐ 🟡 Which ML-style features exist inside Excel and Power BI that an analyst can use without writing code?
**Asked at:** commonly asked (no company-specific report found); ML basics came up in about 4 analyst interview reports (internal research), usually as "what tools have you used".
**What the interviewer is checking:** Whether you know that useful "ML-like" help already sits inside tools you use daily, and whether you can name its limits.
**Say this in the interview:** "In Excel I would use Forecast Sheet for a trend with seasonality and Analyze Data for quick pattern suggestions. In Power BI, the Key Influencers visual and the forecast and anomaly options on a line chart. They are fast starting points, but I still check the data and never treat the output as proof."
**Explain simply:**
- *Excel* (from memory, unverified; names and availability vary by version and licence): Forecast Sheet and the FORECAST.ETS functions (predict a time series, with an upper and lower range); Analyze Data (suggests charts and summaries); Flash Fill (learns a text pattern from your examples); data types (look-up of company or geography facts).
- *Power BI* (from memory, unverified): Key Influencers (which factors go with a higher or lower outcome, such as attrition); Decomposition Tree (drill into what drives a number); forecast and anomaly detection on line charts; clustering to find groups; Smart Narratives (auto-written summaries); Q&A (ask questions in plain English).
- "ML-style" means a statistical model runs behind a button. You do not choose or tune it, so you cannot see every assumption.
- Confirm exact names, versions and licence needs in the official Microsoft documentation or with IT.
**Alternative / pitfalls:** Key Influencers shows association, not cause: "overtime goes with attrition" does not prove overtime makes people leave. A forecast on 12 months of data is rough. Sensitive HR data inside cloud features needs IT approval first.
**Likely follow-ups:** 1) *When would you leave the built-in tools?* When you need to control the method, validate it properly or put it in a repeatable process. 2) *Which one would you try first for attrition?* Key Influencers, to get a first list of candidate drivers to discuss.
**Common mistakes:** Presenting a built-in forecast as certain; reading influencers as causes; forgetting that the tool only sees the columns you gave it.

### Q54 ⭐⭐ 🟡 An HR model is trained on ten years of past promotions. What bias risk exists, and what do you do about it?
**Asked at:** commonly asked (no company-specific report found); ethics of individual-level HR predictions appears on practice pages (Analytics Vidhya, PracHub; unverified).
**What the interviewer is checking:** Whether you understand that a model learns past decisions, including unfair ones, and can propose practical checks.
**Say this in the interview:** "The model learns who got promoted in the past, not who deserved it. If past managers favoured some groups, the model repeats that and hides it behind a score. I would check outcomes by group, remove proxies, and keep a human decision-maker."
**Explain simply:**
- *Label bias:* "promoted" is a human decision, not a neutral fact. The model copies the habits behind it.
- *Proxy columns:* even if you remove gender, other columns (part-time flag, career-break gap, first name, postcode, college) can carry the same signal.
- *Old data:* ten years ago roles, policies and workforce mix were different.
- *What to do:* compare promotion rates and model scores across groups; drop or test proxy columns; use the model only to support review, never to decide alone; document and re-check on a schedule; involve HR leadership and legal.
**Worked example (hypothetical numbers):** History: 600 men, 90 promoted (15%); 400 women, 28 promoted (7%). Women's rate is 0.47 of men's. A model trained to match history will rank women lower on average, even with gender removed, if proxies remain. Some regions use a "four-fifths" style rule of thumb for such ratios (from memory, unverified; ask legal).
**Alternative / pitfalls:** Redefine the target (for example, performance after one year) rather than raw promotion; run the model silently alongside human decisions first and compare.
**Likely follow-ups:** 1) *Does removing the gender column fix it?* No, proxies remain. 2) *Is accuracy a good test?* No; a model can be accurate at copying biased decisions.
**Common mistakes:** Saying "the model is objective"; checking only overall accuracy; dropping the protected column and declaring it fair.

### Q55 ⭐⭐ 🟡 What should you consider before using employee personal data to train a model?
**Asked at:** commonly asked (no company-specific report found); privacy and ethics of attrition models appear on practice pages (unverified).
**What the interviewer is checking:** Whether you think about purpose, consent, minimum data, access and fairness before touching sensitive data.
**Say this in the interview:** "Before training I ask: do we have a legitimate, stated purpose, are we using the minimum data needed, who can see it, and could the output hurt individuals? I would involve HR, IT security and legal first."
**Explain simply:**
- *Purpose:* use data only for what employees were told it is for. "Reducing attrition" is not the same as "monitoring individuals".
- *Minimum data:* collect only the columns the model needs. Leave out health, religion, union membership and similar sensitive fields.
- *Protect it:* remove or mask names and IDs, limit access, store securely, and never paste real employee data into public AI tools.
- *Legal:* laws such as India's DPDP Act or GDPR set rules on consent, purpose and retention (from memory, unverified). I state the principle and confirm the details with legal.
- *Fairness and transparency:* check for bias, and decide whether employees should be told that a model is used.
**Alternative / pitfalls:** Aggregate or anonymised data (team-level attrition) often answers the business question with far less risk. Small groups can still be identified even without names.
**Likely follow-ups:** 1) *Is removing the name enough?* No; age, team and join date together can identify someone. 2) *Who approves?* Data owner (HR), IT security and legal, per company policy.
**Common mistakes:** "It is internal data so anything goes"; sharing a file with a public chatbot; keeping data forever.

### Q56 ⭐⭐ 🟡 What is interpretability, and when would you choose a simpler, explainable model over a more accurate black box?
**Asked at:** commonly asked (no company-specific report found); drivers and explainability are part of attrition prompts on practice banks (unverified).
**What the interviewer is checking:** Whether you can trade accuracy against trust and decisions about people.
**Say this in the interview:** "Interpretability means a person can see why the model gave an answer. For decisions about people, or when a manager must act on it and defend it, I choose a model I can explain unless the black box is clearly and reliably better."
**Explain simply:**
- *Interpretable:* a short rule list or a logistic regression, where each input has a size and direction ("more overtime, higher risk").
- *Black box:* many trees or a neural network; accurate but hard to explain in one sentence.
- Choose simple when: stakes affect individuals (pay, promotion, exits); rules or law require reasons; data is small; the accuracy gain is small.
- Choose the black box when the gain is large, the stakes are low (for example product recommendations) and you can still test it carefully.
**Sample data:** Employees with overtime_hours and tenure_months; 800 simulated rows (seed 42).
**Code (what you write in the interview):**
```python
# fit a logistic regression: predicts whether someone leaves (1) or stays (0)
model = LogisticRegression(max_iter=1000).fit(employees, left)

# odds multiplier for +10 overtime hours and +12 months of tenure
print("Overtime +10 hours:", np.exp(model.coef_[0][0]*10).round(2))
print("Tenure +12 months: ", np.exp(model.coef_[0][1]*12).round(2))
```
**Output:** (simulated data, seed 42)
```text
Overtime +10 hours: 2.46
Tenure +12 months:  0.78
```
**What it means:** In this simulated file, 10 more overtime hours multiplies the odds of leaving by about 2.5, and a year more tenure lowers them by about 22%. That sentence is something a manager can understand and challenge.
**Alternative / pitfalls:** Black boxes can be partly explained afterwards with tools such as SHAP or feature importance, but these are approximations. Simple models are easier to audit.
**Likely follow-ups:** 1) *Does explainable mean causal?* No, still association. 2) *What if the black box is 5 points better?* Ask whether 5 points changes any decision, and whether it holds on fresh data.
**Common mistakes:** Assuming accuracy is all that matters; treating a coefficient as a cause; claiming a black box cannot be checked at all.

### Q57 ⭐⭐ 🟡 Which columns would you keep out of an attrition model, and why?
Columns: emp_id, age, tenure_months, last_rating, exit_interview_done (Yes/No), exit_date, overtime_hours, left_company
**Asked at:** commonly asked (no company-specific report found); data leakage is a common ML interview theme on question banks (PracHub, TechPrep; mostly data scientist roles, unverified).
**What the interviewer is checking:** Whether you spot data leakage (columns that only exist because the person already left).
**Say this in the interview:** "left_company is the answer, so it is the label. exit_date and exit_interview_done only exist after someone leaves, so using them is cheating (leakage). emp_id is just a name tag. I would also discuss age with HR and legal before using it."
**Explain simply:**
- *Label:* left_company is what we predict, so it is not an input.
- *Leakage:* information from after the event. exit_date is filled only for leavers; exit interviews only happen for leavers. The model would look perfect in testing and be useless in real life, since the day we need a prediction these columns are empty.
- *ID:* emp_id carries no meaning and can mislead.
- *Age:* usable in some places but a protected, sensitive trait in many; decide with HR and legal, and check for unfair results.
- Keep: tenure_months, last_rating, overtime_hours (all known before the person leaves; confirm they are measured as of a date before leaving).
**Sample data:** (6 hypothetical rows)

| emp_id | age | tenure_months | last_rating | exit_interview_done | exit_date | overtime_hours | left_company |
|---|---|---|---|---|---|---|---|
| 101 | 29 | 14 | 3 | Yes | 2025-03-31 | 30 | Yes |
| 102 | 41 | 60 | 4 | No | (blank) | 5 | No |
| 103 | 35 | 33 | 3 | No | (blank) | 12 | No |
| 104 | 26 | 8 | 2 | Yes | 2025-05-15 | 40 | Yes |
| 105 | 50 | 120 | 5 | No | (blank) | 2 | No |
| 106 | 31 | 22 | 3 | Yes | 2025-06-30 | 25 | Yes |

**Code (what you write in the interview):**
```python
# does an exit column perfectly match the label? then it is leakage
print(pd.crosstab(employees["left_company"], employees["exit_interview_done"]))
print(employees["exit_date"].notna().eq(employees["left_company"].eq("Yes")).all())

# inputs (X) and label (y); leakage columns and the ID are dropped
X = employees.drop(columns=["emp_id", "exit_interview_done", "exit_date", "left_company"])
y = employees["left_company"]
print(list(X.columns))
```
**Output:**
```text
exit_interview_done  No  Yes
left_company                
No                    3    0
Yes                   0    3
True
['age', 'tenure_months', 'last_rating', 'overtime_hours']
```
**What it means:** The exit columns match the label perfectly. A perfect match is a warning sign, not good news.
**Likely follow-ups:** 1) *How do you spot leakage generally?* A feature that is suspiciously predictive, or one that would not exist at prediction time. 2) *Is last_rating safe?* Only if it was recorded before the exit.
**Common mistakes:** Keeping exit_date because "the model scored 100%"; leaving the ID in; forgetting that age may be a sensitive input.

### Q58 ⭐⭐ 🟡 Tell me about a predictive or machine learning project you have done or would pitch for HR or sales data, covering the problem, data, model type and outcome.
**Asked at:** commonly asked (no company-specific report found); attrition prediction is a standard HR dataset prompt on practice banks (PracHub, Analytics Vidhya; unverified).
**What the interviewer is checking:** Whether you can tell a clear, honest project story with a business problem, not a list of algorithms.
**Say this in the interview:** "I would pitch an early-attrition risk list: predict which employees may leave in the next 6 months so HR can hold stay conversations. Data is HR records, model is a logistic regression, and success means catching more leavers than random, not just high accuracy."
**Explain simply:**
- *Problem:* attrition costs money (hiring, training, lost output); HR wants earlier warning for the right teams.
- *Data:* past two or three years of employee records: tenure, rating, overtime, manager change, salary versus band. Label: left within 6 months of a snapshot date (Yes/No).
- *Model:* classification (predicting a category). Start with logistic regression; compare with a tree model only if it is clearly better.
- *Outcome:* report recall (share of real leavers caught) and precision (share of flagged who really leave) on held-out data, plus lift versus the 6% base rate (hypothetical). Say honestly if you only proposed it and have not built it.
- *Responsible use:* a human reviews the list, no automatic action, check for bias.
**Alternative / pitfalls:** If you have done no ML project, pitch a smaller one honestly (for example, a descriptive attrition analysis in Power BI plus a plan for the model). A sales version: predict which leads convert, so reps call the best ones first.
**Likely follow-ups:** 1) *What would you do with the output?* Stay conversations and fixing team issues, not penalties. 2) *How would you know it worked?* Compare with a control group or the earlier year.
**Common mistakes:** Naming a fancy algorithm without the business problem; claiming results you did not measure; quoting accuracy only.

### Q59 ⭐⭐ 🟡 Only 20 of 1,000 employees in your file left. Why is this a problem for a supervised model, and what are your first practical steps?
1,000 rows; 20 with left = Yes; 980 with left = No
**Asked at:** commonly asked (no company-specific report found); class imbalance is a common ML interview theme (PracHub, TechPrep; mostly data scientist roles, unverified).
**What the interviewer is checking:** Whether you know accuracy is misleading when one class is rare, and what to do instead.
**Say this in the interview:** "A model that says 'nobody leaves' is 98% accurate and completely useless. With only 20 leavers the model has little to learn from. I would use stratified splits, class weights, and judge it by recall and precision, not accuracy, and I would try to get more data."
**Explain simply:**
- *Imbalance:* one outcome (stay) is far more common than the other (leave). The rare one is the one we care about.
- *Accuracy trap:* guessing "stays" every time scores 98%.
- *Few examples:* 20 leavers is too few to learn a stable pattern, and a test set may hold only 4.
- *First steps:* (1) print the base rate; (2) split with `stratify` so train and test keep the same 2% share; (3) use `class_weight="balanced"` (gives rare cases more weight); (4) report recall and precision; (5) widen the label window (left within 12 months) or add earlier years to get more leavers.
**Sample data:** 1,000 simulated employees (overtime_hours, tenure_months, left), exactly 20 leavers, seed 42.
**Code (what you write in the interview):**
```python
print(employees["left"].value_counts())
print("Accuracy of 'nobody leaves':", 1 - employees["left"].mean())

X = employees[["overtime_hours", "tenure_months"]]
y = employees["left"]
# stratify keeps the same 2% leaver share in train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
print("Leavers in test set:", y_test.sum(), "of", len(y_test))

model = LogisticRegression(class_weight="balanced", max_iter=1000)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))
print("Recall:", recall_score(y_test, pred))
print("Precision:", precision_score(y_test, pred, zero_division=0))
```
**Output:** (simulated data, seed 42)
```text
left
0    980
1     20
Name: count, dtype: int64
Accuracy of 'nobody leaves': 0.98
Leavers in test set: 4 of 200
Accuracy: 0.79
Recall: 0.75
Precision: 0.06818181818181818
```
**What it means:** Accuracy fell to 79%, yet the model is more useful: it caught 3 of 4 leavers. But it flagged about 44 people to find them (precision 7%), and 4 leavers is far too few to trust. Report "promising but unproven, need more data".
**Alternative / pitfalls:** Resampling (oversampling the rare class) is another option, but do it only on the training part, otherwise test data leaks. Never tune on the test set.
**Likely follow-ups:** 1) *Why not just oversample?* It can copy the same 16 rows and overfit; do it only inside training. 2) *Which metric?* Recall and precision, plus lift.
**Common mistakes:** Celebrating 98% accuracy; random split without stratify; reporting results from 4 leavers as solid.

### Q60 ⭐⭐ 🟡 You have only 300 employee records. Is machine learning still sensible? What would you say about the reliability of the result?
**Asked at:** commonly asked (no company-specific report found); small-data judgement is a gap-fill question, not tied to a reported company.
**What the interviewer is checking:** Honesty about small samples: can you try a simple model and still say how unsure you are?
**Say this in the interview:** "It is sensible to try a simple model and useful as a learning exercise, but I would be very cautious about the result. With 300 rows, and maybe 30 leavers, scores swing a lot between splits. I would use cross-validation, compare with a do-nothing baseline, and report a range, not one number."
**Explain simply:**
- *Small data:* few rows mean noisy patterns; a model can pick up chance quirks.
- *Rare outcome:* what matters is how many leavers, not total rows (here 33 leavers in 300, hypothetical).
- *Cross-validation:* split the data several times, test on each part, and look at the spread.
- *Baseline:* compare against "predict that nobody leaves".
- Often basic descriptive analysis (attrition by team, tenure band) is the more reliable output at this size.
**Sample data:** 300 simulated employees, 33 leavers, overtime_hours and tenure_months, seed 42.
**Code (what you write in the interview):**
```python
print("Leavers:", employees["left"].sum(), "of", len(employees))
X = employees[["overtime_hours", "tenure_months"]]
y = employees["left"]
# repeat 5-fold cross-validation 10 times with different shuffles
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)
scores = cross_val_score(LogisticRegression(max_iter=1000), X, y, cv=cv, scoring="accuracy")
print("Mean accuracy:", round(scores.mean(), 3))
print("Lowest and highest fold:", round(scores.min(), 3), round(scores.max(), 3))
print("Accuracy of 'nobody leaves':", round(1 - y.mean(), 3))
recall = cross_val_score(LogisticRegression(max_iter=1000), X, y, cv=cv, scoring="recall")
print("Share of leavers caught (recall), mean:", round(recall.mean(), 3), "range:", round(recall.min(), 2), "to", round(recall.max(), 2))
```
**Output:** (simulated data, seed 42)
```text
Leavers: 33 of 300
Mean accuracy: 0.89
Lowest and highest fold: 0.867 0.9
Accuracy of 'nobody leaves': 0.89
Share of leavers caught (recall), mean: 0.0 range: 0.0 to 0.0
```
**What it means:** The 89% looks fine but equals the "nobody leaves" baseline, and the model caught none of the leavers. Tell the manager: "at this size the model adds nothing yet; I recommend descriptive analysis now and collecting more history."
**Alternative / pitfalls:** Use a simpler summary, such as attrition by tenure band, or pool more years of data. Do not tune many settings on 300 rows; you will fit noise.
**Likely follow-ups:** 1) *Is there a minimum size?* No fixed rule; look at the count of the rarer class and how stable the cross-validation results are. 2) *How would you report it?* Mean plus range, baseline and a caveat.
**Common mistakes:** Reporting one accuracy from one split; ignoring the baseline; presenting a weak model as a finding.

### Q61 ⭐⭐ 🟡 Without labels, how do you judge whether the groups from an unsupervised method are useful to the business?
**Asked at:** commonly asked (no company-specific report found); "how do you evaluate clustering" is a standard follow-up to supervised versus unsupervised questions.
**What the interviewer is checking:** Whether you judge groups by business usefulness, not only a statistic.
**Say this in the interview:** "With no right answer to compare against, I judge groups on four things: are they clearly different, can I describe each in one sentence, are they stable if I re-run, and does a different action make sense for each?"
**Explain simply:**
- *Profile each group:* average tenure, engagement, overtime, pay, size. If the groups look alike, they are not useful.
- *Name them:* "new, overloaded, at-risk" is useful; "group 2" is not.
- *Stability:* re-run with a different seed or a sample; if people jump between groups, the groups are shaky.
- *Outside check:* even though the groups were made without labels, see whether they differ on a business outcome such as attrition.
- *Actionable and sized:* a group of 5 people, or a group that needs the same action as another, adds little.
- Statistics like the silhouette score can help, but they do not replace the business test (Part 4 covers clustering steps).
**Worked example:** In a simulated file of 600 employees (see Q74), three groups came out with attrition of 34%, 4% and 10%, average overtime of 36, 5 and 15 hours, sizes 200, 209 and 191. The 34% group (high overtime, low tenure) is clearly different, easy to name and actionable. If all three had shown about 10% attrition and similar profiles, I would say the grouping is not useful.
**Alternative / pitfalls:** Different numbers of groups can all look "fine"; pick the one that supports distinct actions. Groups depend on which columns you fed in and how they were scaled.
**Likely follow-ups:** 1) *What if the groups are unstable?* Fewer groups, other features, or conclude there is no real structure. 2) *Is a high silhouette enough?* No, it measures separation, not value.
**Common mistakes:** Saying "the algorithm found them, so they are valid"; no profile or name; not checking stability.

### Q62 ⭐⭐ 🟡 A model produces a risk score for each employee. What is the difference between the score, the decision and the action, and who owns each?
**Asked at:** commonly asked (no company-specific report found); gap-fill question on responsible use of predictions.
**What the interviewer is checking:** Whether you separate a number from the choices people make with it.
**Say this in the interview:** "The score is the model's estimate, the decision is where we draw the line and who we flag, and the action is what a person actually does. The analyst owns the score, HR leadership owns the decision rule, and the manager or HR business partner owns the action."
**Explain simply:**
- *Score:* a number such as 0.72 for "estimated chance of leaving in 6 months". Owner: analyst or data team (quality, refresh, documentation).
- *Decision:* the rule, for example "flag everyone at 0.6 or above, and review them". Owner: HR leadership, which weighs cost of missing a leaver against effort on false alarms.
- *Action:* a stay conversation, workload review, development plan. Owner: line manager with HR support; a human decides, not the model.
- Keep the score out of performance reviews and pay decisions.
**Worked example (hypothetical numbers):** 1,000 employees, 6% (60) will really leave. The rule flags 80 people; 20 of them really leave. Precision: 20/80 = 25%. Recall: 20/60 = 33%. Lift: 25% / 6% = 4.2 times better than picking at random. Raise the line and you flag fewer, with higher precision but lower recall; HR chooses.
**Alternative / pitfalls:** Showing managers raw scores invites over-reading; give bands (high, medium, low) with plain reasons. Flagged people should not be treated worse.
**Likely follow-ups:** 1) *Who sets the threshold?* The business, with analyst input on trade-offs. 2) *What if managers ignore it?* Track actions and outcomes, simplify the output.
**Common mistakes:** Treating the score as a verdict; no named owner for the action; letting analysts set policy alone.

### Q63 ⭐ 🟢 What is reinforcement learning, and where does it appear in business?
**Asked at:** commonly asked (no company-specific report found); it appears as the third learning type on fresher lists (Indeed India, FacePrep; snippet only).
**What the interviewer is checking:** That you can place it next to supervised and unsupervised learning in plain words.
**Say this in the interview:** "Reinforcement learning is learning by trial and error with rewards: a system tries actions, sees a reward or penalty, and gradually learns which actions work best. It is not something I would build as an analyst, but I know where it is used."
**Explain simply:**
- *Agent, action, reward:* a program (the agent) picks an action, gets a score (reward), and adjusts to earn more over time.
- Unlike supervised learning there is no answer key; unlike unsupervised there is a goal signal.
- Business uses (typical examples, from memory, unverified for any given company): dynamic pricing, ad and recommendation placement, warehouse or delivery routing, game-playing and robotics.
- It needs many trials and a safe place to try them, which is why it is rare in everyday HR analytics.
**Worked example:** A website tests three banners. At first it shows each equally, then shows more of the one getting more clicks (the reward) while still testing the others sometimes.
**Alternative / pitfalls:** Simple A/B testing is the analyst's cousin of this idea.
**Likely follow-ups:** 1) *Do you need labels?* No, you need a reward signal. 2) *Is ChatGPT reinforcement learning?* Part of the training of some chat models uses human feedback as a reward (from memory, unverified).
**Common mistakes:** Mixing it up with unsupervised learning; claiming experience you do not have.

### Q64 ⭐ 🟢 What is the difference between a predictive model and a generative model?
**Asked at:** commonly asked (no company-specific report found); relevant because interviewers ask about AI tools in analyst work.
**What the interviewer is checking:** Whether you separate "predict a value or category" from "create new content".
**Say this in the interview:** "A predictive model estimates something from past data, such as whether an employee will leave or next month's sales. A generative model produces new content, such as text, images or code. They answer different questions, and the generative one can sound confident while being wrong."
**Explain simply:**
- *Predictive:* output is a number or a category with measurable accuracy against known answers. Example: attrition risk, sales forecast.
- *Generative:* output is new text, image, code or summaries. Example: a chatbot drafting an email or SQL.
- Predictive models can be checked with metrics on held-out data; generative output needs a human check, as there is often no single right answer.
- Generative tools can invent facts ("hallucinate").
**Worked example:** Predictive: "this employee has a 0.72 chance of leaving". Generative: "write a polite stay-interview invitation". Use both: the model picks who, the writing tool drafts the message, a person reviews both.
**Alternative / pitfalls:** The boundary is blurred (language models predict the next word), but for the interview, "predict a target" versus "produce content" is enough. Do not paste real employee data into public generative tools.
**Likely follow-ups:** 1) *Can a generative tool replace a forecast model?* No; it does not compute a forecast from your data unless connected to proper tools. 2) *How do you check its output?* Compare with independent numbers.
**Common mistakes:** Saying generative AI is "more advanced predictive models"; trusting generated numbers without checking.

### Q65 ⭐ 🟢 What is a recommendation system, in simple terms?
**Asked at:** commonly asked (no company-specific report found); the interview wording suits e-commerce and media roles.
**What the interviewer is checking:** Whether you can explain the idea without jargon.
**Say this in the interview:** "A recommendation system suggests what a person may want next, based on what similar people liked or bought, or on how similar the items are. It is the 'customers who bought this also bought' idea."
**Explain simply:**
- *Based on people:* find customers like you and suggest what they bought.
- *Based on items:* suggest items often bought together, or similar in features.
- Works best with a lot of history; new users or items have little data (the "cold start" problem).
- It is also used for HR: suggesting training courses to similar employees.
**Worked example (5 customers, hypothetical):** A, B, C and E bought a laptop. Of those four, A, B and C also bought a mouse, so 3 of 4 (75%). When a new laptop buyer appears, suggest a mouse first. A bag shows up for only 1 of the 4 (25%), so rank it lower. A short pandas crosstab confirmed these shares.
**Alternative / pitfalls:** Popular items dominate, so everyone gets the same suggestions. Recommendations need fairness and privacy checks, too.
**Likely follow-ups:** 1) *How do you measure success?* Click or purchase rate in an A/B test. 2) *What is cold start?* No history for a new user or item.
**Common mistakes:** Calling it "just a filter"; ignoring that popular items crowd out others.

### Q66 ⭐ 🟡 What is dimensionality reduction, and what is PCA trying to do in intuition?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic, not a standard analyst question.
**What the interviewer is checking:** Whether you grasp the idea without equations.
**Say this in the interview:** "Dimensionality reduction squeezes many columns into a few that keep most of the information. PCA finds new combined columns along the directions where the data varies the most, so columns that move together, like age, tenure and salary, collapse into one."
**Explain simply:**
- *Dimensions* are columns. Fewer columns are easier to plot, faster to model and less noisy.
- *PCA* (principal component analysis) builds new columns (components) as blends of the old ones. The first holds the most variation, the second the next most, and so on.
- Columns must be put on the same scale first, otherwise big-number columns dominate.
- Trade-off: the components are harder to explain than the original columns.
**Sample data:** 200 simulated employees with age, tenure_months, salary_k (thousands) and overtime_hours; the first three rise together (seed 42).
**Code (what you write in the interview):**
```python
# put columns on the same scale first, otherwise big numbers dominate
scaled = StandardScaler().fit_transform(employees)
pca = PCA(n_components=2)
components = pca.fit_transform(scaled)
print("Share of information kept:", pca.explained_variance_ratio_.round(2))
print(pd.DataFrame(pca.components_, columns=employees.columns, index=["PC1", "PC2"]).round(2))
```
**Output:** (simulated data, seed 42)
```text
Share of information kept: [0.71 0.25]
      age  tenure_months  salary_k  overtime_hours
PC1  0.58           0.58      0.58            0.04
PC2 -0.06          -0.01      0.00            1.00
```
**What it means:** Four columns became two that keep 96% of the variation. The first component is basically "seniority" (age, tenure and salary move together); the second is overtime on its own.
**Alternative / pitfalls:** PCA is not feature selection, since it blends all columns. It does not use a label, so the top components are not guaranteed to predict anything.
**Likely follow-ups:** 1) *Why scale first?* Otherwise salary in thousands outweighs rating from 1 to 5. 2) *When would you avoid it?* When you must explain each input.
**Common mistakes:** Forgetting to scale; thinking PCA removes columns; reading components as original columns.

### Q67 ⭐ 🟡 Is ChatGPT trained with supervised or unsupervised learning? Explain at a high level without claiming details you are unsure of.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can be accurate at a high level and honest about what you do not know.
**Say this in the interview:** "At a high level it is a mix. The first stage learns from a huge amount of text by predicting the next word, which is usually described as self-supervised, since the text provides its own answers. Later stages use human examples and feedback to make it more helpful. I do not know the exact details of any specific product."
**Explain simply:** (general public descriptions, from memory, unverified for any specific product)
- *Pre-training:* the model reads lots of text and learns to predict the next word. No one labels each example by hand, so it is often called self-supervised (a form of learning with labels created from the data itself).
- *Fine-tuning with examples:* people write good answers, and the model learns from them (supervised).
- *Feedback stage:* people rank answers, and the model is adjusted toward preferred ones (a reinforcement-learning-style step in several public descriptions).
- So "either/or" is too simple. Be clear about what you are unsure of, and point to the vendor's own documentation.
**Alternative / pitfalls:** Do not quote training data sizes, costs or internal methods as fact. For an analyst, the useful point is that the model predicts likely text, so it can be fluent and wrong.
**Likely follow-ups:** 1) *Does it look things up?* Not by default; depends on the product (confirm in the documentation). 2) *So what must the analyst do?* Verify its numbers and code.
**Common mistakes:** Answering with false certainty; saying "unsupervised, full stop"; claiming insider details.

### Q68 ⭐ 🟡 Why can a model that worked last year degrade over time?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** That you understand a model learns a snapshot of the world, and the world changes.
**Say this in the interview:** "A model learns patterns from past data. If people, policies or the market change, those patterns stop holding. This is called drift. So I monitor results on fresh data and retrain on a schedule."
**Explain simply:**
- *Data drift:* the inputs change (a new hiring mix, remote work, a new pay structure).
- *Concept drift:* the link between inputs and outcome changes (overtime used to cause exits; now the main reason is manager change).
- *Process changes:* a column is redefined, a system is replaced, a label is recorded differently.
- *Fix:* track performance on recent data, compare input averages with training, retrain, and keep an owner.
**Worked example (simulated, seed 42):** A logistic regression is trained on one year where overtime drives attrition. On a new year with the same pattern, the top-10% risk list caught 26% of leavers, against 10% by chance. After the pattern changes (overtime no longer matters), the same model's top-10% list caught 9%, worse than random.
**Alternative / pitfalls:** Not every drop is drift; check data quality and seasonality first. If true outcomes arrive slowly (leavers show up months later), drift is noticed late.
**Likely follow-ups:** 1) *How often to retrain?* Based on monitoring, not a fixed rule. 2) *How do you detect it early?* Watch input distributions and recent hit rate.
**Common mistakes:** Deploying and forgetting; blaming the algorithm; retraining without checking data definitions.

### Q69 ⭐ 🟡 Your CEO says "we need an AI strategy". How do you respond as an analyst?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you turn vague pressure into a concrete, cautious, business-first plan.
**Say this in the interview:** "I would ask what business problem we want to solve and what success looks like, before talking about tools. Then I would check what data we have, pick one or two low-risk pilots, and set rules for privacy and review."
**Explain simply:**
- *Clarify the goal:* cut cost, speed up reporting, reduce attrition, improve customer service?
- *Data readiness:* is the data clean, owned, and enough in volume?
- *Pilot small:* one use case with a measurable result in weeks, for example faster monthly reporting or an attrition risk list.
- *Guardrails:* which data may go into which tools, who reviews outputs, privacy, bias, approvals (IT and legal).
- *Skills and ownership:* who runs it afterward?
- Use simple analytics first where it solves the problem.
**Alternative / pitfalls:** Buying a tool first and looking for a problem afterwards. Over-promising: say what you can measure, and when.
**Likely follow-ups:** 1) *Which pilot first?* High value, low risk, clean data, for example report automation. 2) *How do you measure it?* Time saved or error reduction versus a baseline.
**Common mistakes:** Listing buzzwords; promising big savings with no numbers; ignoring data quality and privacy.

### Q70 ⭐ 🟡 Why should you try a simple model first, even when a complex one is available?
**Asked at:** commonly asked (no company-specific report found); gap-fill question.
**What the interviewer is checking:** Whether you use a simple baseline for honest comparison.
**Say this in the interview:** "A simple model is a baseline: quick to build, easy to explain, hard to break. If a complex model cannot clearly beat it on fresh data, the extra effort is not worth it."
**Explain simply:**
- *Baseline:* the yardstick every fancier model must beat.
- Simple models are easier to explain, audit and maintain, and are less likely to memorise noise (overfit).
- On small, messy data, complex models often add little.
- Complex only if the gain is large and consistent, and you can still explain and monitor it.
**Sample data:** 400 simulated employees: overtime_hours, tenure_months, last_rating, engagement, left (seed 42).
**Code (what you write in the interview):**
```python
X = employees.drop(columns="left")
y = employees["left"]
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)
simple = cross_val_score(LogisticRegression(max_iter=1000), X, y, cv=cv, scoring="roc_auc")
complex_model = cross_val_score(GradientBoostingClassifier(random_state=42), X, y, cv=cv, scoring="roc_auc")
print("Logistic regression AUC:", simple.mean().round(3))
print("Gradient boosting AUC:  ", complex_model.mean().round(3))
```
**Output:** (simulated data, seed 42)
```text
Logistic regression AUC: 0.727
Gradient boosting AUC:   0.681
```
**What it means:** AUC is a score from 0.5 (guessing) to 1 (perfect) for how well the model ranks leavers above stayers. Here the simple model beat the complex one on the same folds. That is not a law (here the true pattern was simple), but it shows the complex model has to earn its place.
**Alternative / pitfalls:** If the relationships are curved or interact in complicated ways, trees can win; test, do not assume.
**Likely follow-ups:** 1) *What if the complex model is 1 point better?* Probably not worth the loss of clarity. 2) *What is the simplest baseline?* The overall average, or "nobody leaves".
**Common mistakes:** Jumping straight to the fanciest algorithm; comparing on training data; ignoring explainability.

### Q71 ⭐ 🟡 What is an ML pipeline, and why do teams automate it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand a model as a repeatable process, not a one-off file.
**Say this in the interview:** "A pipeline is the chain of steps from raw data to a usable prediction: pull data, clean it, build features, train, check, score, and monitor. Teams automate it so it runs the same way every time and nobody has to redo it by hand."
**Explain simply:**
- *Steps:* data extract, cleaning, feature creation, training, evaluation, scoring, saving results, monitoring.
- *Why automate:* fewer manual errors, same steps for training and scoring, repeatable each month, easy to audit.
- *sklearn Pipeline* (tested to exist in the installed sklearn version here) chains preprocessing and a model, so scaling learned on training data is applied identically to new data and cannot leak from test data.
- Scheduling and tooling vary by company; I would describe the idea, not claim a specific platform.
**Worked example:** A monthly attrition list: Monday, the HR extract loads; cleaning rules run; features are rebuilt as of that date; the saved model scores everyone; a table feeds the dashboard; a check alerts if row counts or averages look odd.
**Alternative / pitfalls:** Automating a bad process just repeats errors faster. Add checks (row counts, missing values) and an owner.
**Likely follow-ups:** 1) *What breaks pipelines?* Changed source columns and late files. 2) *What would you monitor?* Data volumes, input averages, model hit rate.
**Common mistakes:** Treating the notebook as the product; scaling before splitting (leakage); no alerting.

### Q72 ⭐ 🟡 What is a feature store or feature table, and why does consistent feature definition matter between training and use?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** Whether you know that a column must mean the same thing when training and when scoring.
**Say this in the interview:** "A feature table is one agreed place where each model input is defined and stored, such as tenure in months as of a stated date. If training used one definition and live scoring uses another, predictions are quietly wrong."
**Explain simply:**
- *Feature:* a column used as input (tenure, overtime, rating).
- *Feature table or store:* a shared, documented table of features with one definition each, reused by many models and by scoring.
- *Why consistency:* the model learned what the number meant at training; change the meaning and it misreads.
- Always compute features as of a stated date, using only what was known then.
**Worked example (hypothetical, computed by script):** Employee 2 joined 2022-07-01. If training measured tenure as of 2025-06-30 she had 36.0 months; scoring a year later gives 48.0 months, which is correct only if the model was trained that way. A worse mismatch: a leaver who joined on 2023-03-15 and left 2025-03-14 has tenure 24.0 months counted to the exit date, while current staff are counted to today. The model sees leavers as "short tenure" for a reason that exists only after the event.
**Alternative / pitfalls:** A small team can use one shared SQL view or a documented table instead of a full feature-store product.
**Likely follow-ups:** 1) *What is this problem called?* Training-serving skew. 2) *Where do you document?* A data dictionary with definition and as-of date.
**Common mistakes:** Rebuilding features differently in two scripts; no as-of date; using post-event information.

### Q73 ⭐ 🟡 How do hype claims about AI differ from what ML can reliably do on small, messy company data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Realism: can you separate marketing from what your data supports?
**Say this in the interview:** "Hype says AI will predict anything with great accuracy. In practice ML on small, messy data can give a modest, useful ranking, if the data is clean and the question is clear. It cannot fix bad data, replace judgment, or find causes."
**Explain simply:**
- *Hype:* "99% accurate", "works out of the box", "replaces analysts".
- *Reality on small, messy data:* missing values and inconsistent definitions limit everything; rare outcomes give shaky results (see Q59, Q60); the model learns the past, including its biases.
- *What it can reliably do:* rank cases, spot patterns for a human to review, automate repetitive checks, draft text for review.
- *What it cannot:* guarantee accuracy, explain causes, work without clean data and ownership.
- Ask for evidence: test on held-out data, versus a baseline.
**Worked example:** "95% accurate" sounds great, but if 5% of employees leave, a model that predicts "nobody leaves" is also 95% accurate (950 of 1,000).
**Alternative / pitfalls:** Do not swing to the other extreme and call it useless; a modest, measured lift is still valuable.
**Likely follow-ups:** 1) *How do you test a claim?* Held-out data, baseline, right metric. 2) *What would you fix first?* Data quality and definitions.
**Common mistakes:** Repeating vendor claims; saying "ML cannot work with small data" without nuance.

### Q74 ⭐ 🟡 Show with an example how supervised and unsupervised learning can be combined in one project.
**Asked at:** commonly asked (no company-specific report found); gap-fill for interviewers who ask for an applied example.
**What the interviewer is checking:** Whether you know both types and can chain them sensibly.
**Say this in the interview:** "First, unsupervised: cluster employees into groups with no labels and profile them. Then supervised: use the groups, or compare their attrition, to explain or predict who leaves. The first step finds structure, the second links it to an outcome."
**Explain simply:**
- *Unsupervised step* (no answer column): group employees by engagement, overtime and tenure.
- *Profile:* describe the groups and compare attrition across them.
- *Supervised step* (with the answer column): feed the group as an extra input to a model that predicts leaving.
- Other chains: clustering customers, then a separate model per segment; PCA first, then a classifier.
**Sample data:** 600 simulated employees: engagement, overtime_hours, tenure_months, left; three hidden types (seed 42).
**Code (what you write in the interview):**
```python
features = ["engagement", "overtime_hours", "tenure_months"]
scaled = StandardScaler().fit_transform(employees[features])

# Step 1 (unsupervised, no labels): find 3 groups
employees["group"] = KMeans(n_clusters=3, n_init=10, random_state=42).fit_predict(scaled)

# Step 2: describe each group and check how many left
print(employees.groupby("group").agg(size=("left", "size"), engagement=("engagement", "mean"),
      overtime=("overtime_hours", "mean"), tenure=("tenure_months", "mean"), attrition=("left", "mean")).round(2))

# Step 3 (supervised): use the group as an extra input to predict who leaves
X = pd.get_dummies(employees[features + ["group"]], columns=["group"])
print("CV accuracy:", cross_val_score(LogisticRegression(max_iter=1000), X, employees["left"], cv=5).mean().round(3))
print("Accuracy of 'nobody leaves':", round(1 - employees["left"].mean(), 3))
```
**Output:** (simulated data, seed 42; group numbers are arbitrary labels)
```text
       size  engagement  overtime  tenure  attrition
group                                               
0       200        2.18     35.52   12.97       0.34
1       209        4.11      5.05   58.51       0.04
2       191        3.05     14.94   28.39       0.10
CV accuracy: 0.842
Accuracy of 'nobody leaves': 0.84
```
**What it means:** Group 0 (low engagement, heavy overtime, short tenure) loses 34% of people versus 4% in group 1: that profile is the business insight. Accuracy (84.2%) only matches the 84% baseline, so do not sell the model on accuracy; use the groups to focus conversations, and judge any risk model by recall and lift (Q59).
**Alternative / pitfalls:** Cluster only on training data if you will use the groups in a model, otherwise information leaks. Groups change when columns or scaling change.
**Likely follow-ups:** 1) *Why not just use the clusters as the answer?* Without a label we cannot say whether they matter for attrition. 2) *Another combination?* Segment customers, then forecast per segment.
**Common mistakes:** Treating cluster numbers as meaningful; skipping profiling; clustering on the whole data before splitting.

### Q75 ⭐ 🔴 How would you decide between explaining the past with analytics and predicting the future with ML, when leadership wants both with one dataset and two weeks?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Scoping and prioritisation: can you deliver value fast and be honest about what two weeks allows?
**Say this in the interview:** "I would deliver the descriptive analysis first, because it is reliable in two weeks and gives leadership something to act on. I would offer a simple predictive pilot as a clearly labelled second phase, if the data is good enough, and say what I would need to make it trustworthy."
**Explain simply:**
- *Ask first:* which decision will this change, and when? Prediction only pays off if someone will act on it.
- *Check the data:* how many rows, how many events (leavers), which time span, how clean? A few dozen events means prediction will be shaky.
- *Plan, as an example:* days 1-3 data checks and definitions; days 4-8 descriptive analysis (attrition by team, tenure, manager, pay band) and a dashboard; days 9-12 a baseline model with honest validation, if the data allows; days 13-14 write-up and next steps.
- *Say plainly:* descriptive results are firm; the model is a proof of concept, not a decision tool.
- Explaining the past often reveals the main drivers and is the best input for any model later.
**Alternative / pitfalls:** If the question is "who will leave next quarter" and there is enough clean history, build the baseline model sooner. Never promise accuracy before seeing the data.
**Likely follow-ups:** 1) *What if leadership insists on a prediction?* Offer a simple, flagged-as-early model plus the descriptive base, and show the limits. 2) *What would you need for a credible model?* More history, a clean label, an owner for the action.
**Common mistakes:** Agreeing to both without scoping; promising accuracy; skipping the descriptive work.

### Q76 ⭐ 🔴 A vendor claims their black-box tool predicts attrition with high accuracy. What do you ask before trusting it, and what evidence do you request?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Critical thinking about claims, evidence, fairness and data protection.
**Say this in the interview:** "I would ask how they measured accuracy, on whose data, against which baseline, and whether the result holds on our own data in a trial. I would also ask what data the tool uses, how it treats fairness, and where our employee data goes."
**Explain simply:**
- *Metric:* "accuracy" alone is a red flag when few people leave. With 5% attrition (hypothetical), "nobody leaves" scores 95%. Ask for recall, precision and lift versus a simple baseline.
- *Test method:* was it measured on data the model never saw, and on a later time period rather than a random split?
- *Relevance:* was the data from similar companies, sizes and roles? Ask to run a blind trial on our own history.
- *Leakage:* which inputs are used? Could any only exist after someone leaves?
- *Fairness and legal:* bias testing by group; what data is collected (confirm with legal against DPDP or GDPR, from memory, unverified).
- *Data handling:* where data is stored, who sees it, whether it trains their models, how it can be deleted.
- *Explainability and operations:* reasons per score, update schedule, monitoring, cost, and exit terms.
**Worked example (hypothetical):** In a trial on 1,000 employees, 50 left. The tool flags 100 people and 30 of them left. Precision 30/100 = 30%; recall 30/50 = 60%; lift 30% / 5% = 6 times random. That evidence is far more useful than "95% accurate".
**Alternative / pitfalls:** A pilot with a clear pass mark agreed in advance protects you. A black box does not excuse a missing explanation.
**Likely follow-ups:** 1) *What if they refuse a trial on your data?* Treat the claim as unproven. 2) *What if it works but cannot be explained?* Consider whether decisions about people can be made on it.
**Common mistakes:** Accepting one headline number; testing on the vendor's data only; ignoring data protection.

### Q77 ⭐ 🔴 Design a minimal, responsible attrition-risk workflow: data, label definition, model type, who sees the output, and what action follows.
**Asked at:** commonly asked (no company-specific report found); attrition prediction is a standard HR dataset prompt on practice banks (unverified).
**What the interviewer is checking:** Whether you can design a complete, careful process, not just a model.
**Say this in the interview:** "I would predict voluntary exits in the next 6 months from a few safe HR fields, using logistic regression, show only grouped risk bands to HR business partners, and the action is a supportive conversation. I would keep a human in charge, test fairness, and review it quarterly."
**Explain simply:**
- *Data:* HR system extract at a snapshot date: tenure, role, rating, overtime, time since last promotion, pay versus band, manager change. Leave out sensitive fields and anything only known after exit. Minimum data, restricted access, no real data in public AI tools.
- *Label:* "left voluntarily within 6 months after the snapshot date" (Yes/No). Exclude layoffs, retirements and end of contract. Write the definition down.
- *Model:* logistic regression as baseline (explainable). Split by time (train on older snapshots, test on the latest). Judge on recall, precision and lift against the base rate, not accuracy.
- *Who sees it:* a small group (HR business partner, senior HR); bands high, medium, low plus plain-language reasons; not the line manager's performance file, not pay decisions.
- *Action:* supportive stay conversation, workload or career review, fix team issues. Never penalise a flagged person.
- *Responsible checks:* compare scores and error rates across groups (gender, age band, location) (confirm legal requirements with legal); tell employees how data is used; keep a log; re-check drift and retrain on a schedule.
- *Success:* compare attrition in the flagged group with and without outreach (a pilot), not only model scores.
**Alternative / pitfalls:** If leavers are very few, start with team-level descriptive analytics and aggregate-level risk, which avoids individual predictions. Predicting an individual can become a self-fulfilling label.
**Likely follow-ups:** 1) *Would you tell the employee?* Per policy and law; transparency is the safer principle (confirm with legal). 2) *What if bias appears?* Pause use, investigate inputs, retrain or retire.
**Common mistakes:** Building the model first and thinking about use later; using accuracy; sharing named scores widely; no review cycle.

