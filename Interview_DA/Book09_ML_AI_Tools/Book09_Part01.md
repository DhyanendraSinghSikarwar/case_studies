# Book 9 — Basic ML + AI Tools for Analysts | Part 1: What ML Is; Supervised vs Unsupervised; When Analysts Use It 🟢

**Target:** 76 questions | **Actual:** 77 questions
**Scope:** what machine learning is, supervised vs unsupervised learning, features and labels, classification vs regression, basic sklearn/pandas reading, and when and when not to use ML as an analyst (including bias, privacy and explainability basics).

### Q1 ⭐⭐⭐ 🟢 Explain machine learning to a non-technical manager in two or three sentences.
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is the difference between supervised and unsupervised learning?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is the difference between machine learning and traditional rule-based programming?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What are features and a label (target) in a machine learning dataset? Name them for an employee attrition dataset.
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What is the difference between classification and regression? Give one HR example of each.
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 Give one real business example each of supervised and unsupervised learning.
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 When would a data analyst reach for machine learning instead of a dashboard, pivot table or SQL query?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 What is the difference between AI, machine learning, deep learning and data science?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟢 What does it mean to "train" a model, and what is the difference between an algorithm and a model?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟢 Label each task as classification, regression or clustering: (a) predict next month's sales amount, (b) group customers by buying behaviour with no predefined groups, (c) predict whether an employee will resign within six months, (d) predict delivery time in minutes.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟢 Does every analytics problem need machine learning? Describe one situation where ML is the wrong tool.
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟢 Look at the columns of this HR table. Which one is the label, which are usable features, and which would you drop before modelling?
Columns: emp_id, age, tenure_months, monthly_salary, department, overtime_hours, left_company (Yes/No)
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟢 Does a machine learning model give certain answers? How would you explain its output to a stakeholder who expects a yes or no?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 What is the difference between machine learning and classical statistics, and where do they overlap for an analyst?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Read this code. What does each line do, and what is the role of fit and predict?
```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X, y)
new_pred = model.predict(X_new)
```
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 Walk through the steps of a typical machine learning project, from business question to a result the business can use.
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 How do you decide whether a business problem is really a machine learning problem? What would you check first?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 Your manager says "can we use AI to predict attrition?" Which clarifying questions do you ask before touching any data?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🟡 Why does a supervised model need historical data with known outcomes, and what goes wrong if the labels are wrong or missing for many rows?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐⭐ 🟡 A stakeholder asks "why did the model flag this employee?" How do you answer without technical jargon?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 Classify each scenario as supervised or unsupervised learning and name the task type: (a) predict which loan applicants will default using past repayment records, (b) group stores by sales pattern with no labels, (c) predict house price from area and location, (d) find unusual expense claims with no past fraud labels, (e) predict whether a candidate will accept an offer using past offers.
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 Name five common machine learning algorithms and say whether each is mainly used for supervised or unsupervised learning.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 What is clustering, in plain words, and what is one business use of it?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟢 What is deep learning, and what is a neural network in simple terms?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟢 Which Python library do analysts normally use for basic machine learning, and what is the common fit and predict pattern it offers?
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟢 In this pandas snippet, what are X and y, and why are they separated?
```python
X = df.drop('left', axis=1)
y = df['left']
```
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟢 What does "garbage in, garbage out" mean for machine learning, with an example from HR data?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟢 Will machine learning replace data analysts? How do you see your role next to ML?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟢 How does the work of a data analyst differ from that of a data scientist and an ML engineer?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟢 What is a baseline model, and why should you build one before anything complicated?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟢 Name three ways machine learning is used in HR analytics.
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟢 Name three ways machine learning is used in e-commerce.
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟢 Name three ways machine learning is used in banking and finance.
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟢 Classify each column as numeric, categorical, date, text or identifier, and say which are useful as features.
Columns: emp_id, joining_date, grade (A/B/C), monthly_salary, manager_comment, city, performance_rating (1-5)
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟢 A trained model is: predicted_salary = 25000 + 4000 x years_experience. Predict the salary for a candidate with 3 years, and explain what the model has "learned".
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟢 After loading a CSV for modelling, what does df.shape tell you and how do you read rows and columns in ML language?
print(df.shape)  # (5000, 12)
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟢 Why do analysts check df.isna().sum() before building a model?
print(df.isna().sum())
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟢 Coming from an HR background, how would you use machine learning on HR data in your first year as an analyst?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 What is semi-supervised learning, and when does it make sense for a company with few labelled rows?
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 Name three problems that unsupervised learning solves, besides clustering, with a business example each.
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 Why do we convert categorical columns such as department into numbers before modelling?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 What is the difference between a model parameter and a hyperparameter?
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 What is anomaly detection, and when is it supervised versus unsupervised?
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 You have 20,000 customer records and none are labelled with an outcome. What can you do with machine learning, and what can you not do?
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 Trace the unsupervised code below. What does it return, and why is there no y?
```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3, n_init=10, random_state=0)
km.fit(X)
print(km.labels_[:5])
```
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 Spot the mistake in this snippet before it is used to predict attrition.
```python
X = df[['age','tenure_months','left']]
y = df['left']
model.fit(X, y)
```
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟡 A model predicts that nobody will leave. In a team of 200 employees, 30 left last year. What accuracy does this useless model get, and what does it teach you about judging a model?
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟡 Compare a simple rule with a model. The rule: tenure under 12 months means will leave. Use the 10 rows below to count how many the rule gets right.
tenure_months / left: 5/Yes, 8/Yes, 10/No, 11/Yes, 14/No, 20/No, 7/Yes, 30/No, 9/No, 40/No
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🟡 Predict with a one-nearest-neighbour idea: copy the label of the closest known employee. Who is closest to a new employee, and what is the prediction?
```python
Known (tenure_months, overtime_hours/week): A (6, 12) Left; B (30, 2) Stayed; C (10, 10) Left; D (48, 0) Stayed
New employee: (9, 11)
```
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🟡 Estimate whether an attrition model is worth building using the hypothetical figures below.
500 employees; 12% leave each year; each exit costs about 3 lakh; assume a model-led retention effort could prevent 10% of exits; model and effort cost 12 lakh per year.
<!-- ANSWER_PENDING -->

### Q51 ⭐⭐ 🟡 Using the hypothetical counts below, can you train a supervised model, and what would you do with the rest?
1,000 resumes in the file; 200 have a hired or rejected outcome recorded; 800 have no outcome.
<!-- ANSWER_PENDING -->

### Q52 ⭐⭐ 🟡 What is AutoML, and should an analyst use it?
<!-- ANSWER_PENDING -->

### Q53 ⭐⭐ 🟡 Which ML-style features exist inside Excel and Power BI that an analyst can use without writing code?
<!-- ANSWER_PENDING -->

### Q54 ⭐⭐ 🟡 An HR model is trained on ten years of past promotions. What bias risk exists, and what do you do about it?
<!-- ANSWER_PENDING -->

### Q55 ⭐⭐ 🟡 What should you consider before using employee personal data to train a model?
<!-- ANSWER_PENDING -->

### Q56 ⭐⭐ 🟡 What is interpretability, and when would you choose a simpler, explainable model over a more accurate black box?
<!-- ANSWER_PENDING -->

### Q57 ⭐⭐ 🟡 Which columns would you keep out of an attrition model, and why?
Columns: emp_id, age, tenure_months, last_rating, exit_interview_done (Yes/No), exit_date, overtime_hours, left_company
<!-- ANSWER_PENDING -->

### Q58 ⭐⭐ 🟡 Tell me about a predictive or machine learning project you have done or would pitch for HR or sales data, covering the problem, data, model type and outcome.
<!-- ANSWER_PENDING -->

### Q59 ⭐⭐ 🟡 Only 20 of 1,000 employees in your file left. Why is this a problem for a supervised model, and what are your first practical steps?
1,000 rows; 20 with left = Yes; 980 with left = No
<!-- ANSWER_PENDING -->

### Q60 ⭐⭐ 🟡 You have only 300 employee records. Is machine learning still sensible? What would you say about the reliability of the result?
<!-- ANSWER_PENDING -->

### Q61 ⭐⭐ 🟡 Without labels, how do you judge whether the groups from an unsupervised method are useful to the business?
<!-- ANSWER_PENDING -->

### Q62 ⭐⭐ 🟡 A model produces a risk score for each employee. What is the difference between the score, the decision and the action, and who owns each?
<!-- ANSWER_PENDING -->

### Q63 ⭐ 🟢 What is reinforcement learning, and where does it appear in business?
<!-- ANSWER_PENDING -->

### Q64 ⭐ 🟢 What is the difference between a predictive model and a generative model?
<!-- ANSWER_PENDING -->

### Q65 ⭐ 🟢 What is a recommendation system, in simple terms?
<!-- ANSWER_PENDING -->

### Q66 ⭐ 🟡 What is dimensionality reduction, and what is PCA trying to do in intuition?
<!-- ANSWER_PENDING -->

### Q67 ⭐ 🟡 Is ChatGPT trained with supervised or unsupervised learning? Explain at a high level without claiming details you are unsure of.
<!-- ANSWER_PENDING -->

### Q68 ⭐ 🟡 Why can a model that worked last year degrade over time?
<!-- ANSWER_PENDING -->

### Q69 ⭐ 🟡 Your CEO says "we need an AI strategy". How do you respond as an analyst?
<!-- ANSWER_PENDING -->

### Q70 ⭐ 🟡 Why should you try a simple model first, even when a complex one is available?
<!-- ANSWER_PENDING -->

### Q71 ⭐ 🟡 What is an ML pipeline, and why do teams automate it?
<!-- ANSWER_PENDING -->

### Q72 ⭐ 🟡 What is a feature store or feature table, and why does consistent feature definition matter between training and use?
<!-- ANSWER_PENDING -->

### Q73 ⭐ 🟡 How do hype claims about AI differ from what ML can reliably do on small, messy company data?
<!-- ANSWER_PENDING -->

### Q74 ⭐ 🟡 Show with an example how supervised and unsupervised learning can be combined in one project.
<!-- ANSWER_PENDING -->

### Q75 ⭐ 🔴 How would you decide between explaining the past with analytics and predicting the future with ML, when leadership wants both with one dataset and two weeks?
<!-- ANSWER_PENDING -->

### Q76 ⭐ 🔴 A vendor claims their black-box tool predicts attrition with high accuracy. What do you ask before trusting it, and what evidence do you request?
<!-- ANSWER_PENDING -->

### Q77 ⭐ 🔴 Design a minimal, responsible attrition-risk workflow: data, label definition, model type, who sees the output, and what action follows.
<!-- ANSWER_PENDING -->
