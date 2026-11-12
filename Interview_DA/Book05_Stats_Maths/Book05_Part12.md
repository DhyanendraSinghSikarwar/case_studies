# Book 5 — Statistics & Maths for Data Analysts | Part 12: How to Develop Statistics & Maths Skills 🟢🟡

**Target:** 20 questions | **Actual:** 25 questions
**Scope:** learning-journey interview questions plus the zero-to-job-ready statistics and maths skill-development plan (roadmap, daily plan, free resources, datasets, mini-projects, self-check tests).

### Q1 ⭐⭐⭐ 🟢 How did you learn statistics, and how long did it take you?
**Asked at:** commonly asked (no company-specific report found); a standard opener for career switchers.
**What the interviewer is checking:** Is your learning structured and honest, and did you apply it to real data, not only watch videos?
**Say this in the interview:** "I learned in three stages: descriptive statistics first, then probability and sampling, then testing and regression, and at every stage I practised on HR-style data. I got comfortable with the basics in about three months at 8 to 10 hours a week, and I keep deepening it on real projects." (Replace the numbers with your true timeline; never claim a course or project you did not do.)
**Explain simply:**
- **Stage 1 (weeks 1-4):** average, median, spread, charts, using Excel on payroll or attendance data.
- **Stage 2 (weeks 5-8):** probability, sampling, the normal curve, confidence intervals (a range that likely contains the true value).
- **Stage 3 (weeks 9-12):** hypothesis tests (a formal check whether a difference is real or luck), correlation, simple regression (a line that predicts one number from another).
- The honest message: basics take months, mastery takes years of use.
**Worked example:** 3 months x 4.3 weeks x 9 hours is about 116 hours of practice; that is the scale to quote, not "I learned it in a weekend".
**Likely follow-ups:** 1) *What was your most useful resource?* Name one or two you really used (Q6). 2) *What is still weak?* Name one topic honestly (Q2).
**Common mistakes:** Listing ten courses without a single project; giving an unrealistic "two weeks" timeline.

### Q2 ⭐⭐⭐ 🟢 How would you rate yourself in statistics out of 10, and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Self-awareness: can you rate yourself with evidence instead of 10/10 or 3/10?
**Say this in the interview:** "I would say 6 out of 10: strong on descriptive statistics, sampling, confidence intervals and A/B-style tests that I have run on data, and still building depth in regression assumptions and advanced probability. I know where my edge is."
**Explain simply:**
- Pick a number between 5 and 7 for a fresher; 10 sounds arrogant, below 4 sounds unprepared.
- Always justify with 2 strengths and 1 named gap plus what you are doing about it.
- Back each strength with something you did (a test on attrition data, a confidence interval for a survey).
**Likely follow-ups:** 1) *Why not higher?* "Because I have not yet used time series or multivariate methods at work." 2) *Prove the 6.* Walk through one analysis end to end.
**Common mistakes:** Claiming 9/10 and then failing a basic question about p-values; being vague ("average").

### Q3 ⭐⭐⭐ 🟢 You come from HR with no maths or statistics background. How did you learn statistics for data analysis?
**Asked at:** commonly asked (no company-specific report found); typical for HR-to-analytics switchers.
**What the interviewer is checking:** Can you learn new technical material alone, and do you turn HR knowledge into an advantage?
**Say this in the interview:** "I started from the questions HR already asks: why do people leave, is pay fair, did the training work. Each question mapped to a statistic, so I learned averages and spread for pay, proportions for attrition, and tests for whether training worked. HR gave me the business sense; practice gave me the method."
**Explain simply:**
- Learn through questions you already care about; the maths becomes a tool, not a subject.
- Required maths is school level (percentages, averages, simple algebra); see Q8.
- Practise by hand in Excel first, then Python, so you see what the formula does.
- Your HR domain knowledge (what a sensible attrition rate looks like) catches errors that pure maths people miss.
**Worked example:** Attrition: 30 of 200 Sales staff left (15%), 12 of 200 in Support (6%). Question: is 15% vs 6% real? That one HR question introduces proportions, hypothesis tests and p-values (Q5).
**Likely follow-ups:** 1) *How many hours a week?* About 8 to 10 (Q9). 2) *Did you ever feel stuck?* Yes; mention a hard topic and the fix (Q4).
**Common mistakes:** Apologising for the HR background; hiding it instead of using it.

### Q4 ⭐⭐⭐ 🟡 Which statistics topic did you find hardest, and how did you overcome it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Honesty about difficulty and a concrete method for getting past it.
**Say this in the interview:** "The p-value was hardest, because the definition sounds like a riddle. I got past it by simulating it: shuffle the department labels thousands of times and count how often luck alone creates a gap as big as the one I saw. That share is the p-value." (Swap in your own hardest topic if different; p-values, confidence intervals and Bayes are the usual honest answers.)
**Explain simply:**
- **p-value:** the chance of seeing a difference at least this big if there were really no difference. Small (below 0.05 by convention) means luck is an unlikely explanation.
- Simulation turns an abstract definition into something you can watch.
- The method generalises: when stuck, make a tiny dataset and compute it by hand or by simulation.
**Worked example:** Sales attrition 15% (30 of 200) vs Support 6% (12 of 200), a 9-point gap.
**Excel / Python:**
```python
import numpy as np

# 1 = left the company, 0 = stayed; 30 of 200 left in Sales, 12 of 200 in Support
sales_employees = np.array([1] * 30 + [0] * 170)
support_employees = np.array([1] * 12 + [0] * 188)

# the gap we actually saw between the two attrition rates
observed_gap = sales_employees.mean() - support_employees.mean()

# put everyone in one pool; if department does not matter, labels are interchangeable
everyone = np.concatenate([sales_employees, support_employees])
random_generator = np.random.default_rng(1)

gaps_as_big_count = 0
for round_number in range(10000):
    # shuffle the pool and split it into two fake departments of 200
    random_generator.shuffle(everyone)
    fake_gap = everyone[:200].mean() - everyone[200:].mean()
    # count how often luck alone gives a gap at least as big as the real one
    if abs(fake_gap) >= abs(observed_gap):
        gaps_as_big_count += 1

print("Observed gap:", round(observed_gap, 2))
print("Share of shuffles with a gap this big:", gaps_as_big_count / 10000)
```
Output: `Observed gap: 0.09` and `Share of shuffles with a gap this big: 0.0052`. Only about 0.5% of random shuffles produce a gap this large, so luck is an unlikely explanation (the exact chi-square test in Q5 gives 0.0033; the simulated value varies slightly with the random seed).
**Likely follow-ups:** 1) *Does a small p-value prove the cause?* No, it only says luck is unlikely; the cause needs more thinking. 2) *What does 0.05 mean?* A convention, not a law.
**Common mistakes:** Saying "the p-value is the probability the hypothesis is true"; naming a topic you cannot then explain.

### Q5 ⭐⭐⭐ 🟡 Which statistical concepts have you actually used in a real analysis, and what was the result?
**Asked at:** commonly asked (no company-specific report found); "how have you used statistics" questions appear in analyst question banks.
**What the interviewer is checking:** Real application, not a vocabulary list. Can you link a method to a decision?
**Say this in the interview:** "I used proportions and a chi-square test to check whether attrition really differed by department. Sales lost 15% of staff and Support 6%; the test gave a p-value of about 0.003, so the gap was unlikely to be luck, and we focused the retention review on Sales." (This is a template example with illustrative numbers. Use your own real project; if you have none, say it is a practice project on public data.)
**Explain simply:**
- Typical concepts an HR analyst really uses: mean and median pay, standard deviation, percentiles, proportions, confidence intervals, chi-square or t-tests, correlation, simple regression.
- Always state the result and the action it led to.
- **Chi-square test:** compares counts in categories (left or stayed, by department) with what we would expect if department did not matter.
**Worked example:** 30 of 200 Sales left vs 12 of 200 Support.
**Excel / Python:**
```python
from scipy import stats

# rows: Sales, Support; columns: left, stayed
attrition_table = [[30, 170],
                   [12, 188]]

# chi-square test of independence (no continuity correction, to match the textbook formula)
chi_square_value, p_value, degrees_of_freedom, expected_counts = stats.chi2_contingency(attrition_table, correction=False)

print("Chi-square:", round(chi_square_value, 2))
print("p-value:", round(p_value, 4))
```
Output: `Chi-square: 8.62` and `p-value: 0.0033`. A p-value this small says the department gap is unlikely to be chance. (With the continuity correction scipy applies by default, p is 0.0056; same conclusion.)
**Likely follow-ups:** 1) *Does this prove Sales is a worse place to work?* No; workload, pay or manager could explain it. 2) *Effect size?* A 9 percentage-point gap.
**Common mistakes:** Quoting a p-value without the business meaning; claiming causation.

### Q6 ⭐⭐ 🟢 Which free resources would you recommend to a beginner learning statistics for data analysis?
**Asked at:** commonly asked (no company-specific report found). The sources file lists free-resource roundups (Statology, Analytics Vidhya) at snippet level only; none was read in full, so verify current links yourself.
**What the interviewer is checking:** Do you know quality resources and can you give a reasoned, not random, list?
**Say this in the interview:** "I would pair one video series for intuition with one practice site for hands-on work: StatQuest on YouTube for concepts, Khan Academy Statistics and Probability for fundamentals, and the free statistics tutorials on sites like Statology, then apply everything on a real dataset."
**Explain simply:**
- **Concepts (video):** StatQuest with Josh Starmer, Khan Academy (Statistics and Probability).
- **Reading and quick reference:** Statology tutorials, the free online textbook OpenIntro Statistics.
- **Practice:** Kaggle Learn (free short courses), Excel on your own HR-style data, Python with pandas and scipy.
- **Rule:** one resource per stage; finishing one beats sampling ten.
- The named resources are from memory, unverified; availability and contents change, and I have not re-checked every link today.
**Likely follow-ups:** 1) *Why free?* Fundamentals are well covered for free; paid courses add structure and certificates (Q17). 2) *Which first?* Descriptive statistics in Excel.
**Common mistakes:** Hoarding bookmarks; watching without doing exercises.

### Q7 ⭐⭐ 🟢 In what order did you study statistics topics, and why that order?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A logical build-up, each topic resting on the previous one.
**Say this in the interview:** "I went from describing data, to probability, to inferring from samples, to testing, to modelling. Each step needs the previous one: you cannot judge a p-value without understanding spread and sampling."
**Explain simply:**
1. **Descriptive statistics:** mean, median, mode, range, standard deviation (how spread out values are), percentiles, charts.
2. **Probability basics:** chances, independence, conditional probability.
3. **Distributions:** especially the normal (bell-shaped) curve.
4. **Sampling and the central limit theorem:** averages of samples behave predictably.
5. **Confidence intervals:** an estimate with a margin of error.
6. **Hypothesis tests:** t-test, chi-square, p-values.
7. **Correlation and regression.**
8. **A/B testing and communication of results.**
- Why: each layer answers the question the previous one raises ("how sure am I?").
**Likely follow-ups:** 1) *Where does maths fit?* Only what each step needs (Q8). 2) *Where did you spend the most time?* Steps 4 to 6, where ideas are subtler.
**Common mistakes:** Jumping to machine learning or tests before understanding spread and sampling.

### Q8 ⭐⭐ 🟢 How much maths do you really need to work as a data analyst?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question.
**What the interviewer is checking:** A realistic view: practical, school-level maths plus clear thinking, not advanced theory.
**Say this in the interview:** "Mostly school-level: percentages, ratios, averages, basic algebra and reading graphs. On top of that, statistical thinking: what a sample is, what spread means, and when a difference is real. Calculus and linear algebra matter only when you move towards machine learning."
**Explain simply:**
- **Needed daily:** percentages, percentage change, ratios, weighted averages, mean/median, rounding.
- **Needed often:** standard deviation, probability basics, confidence intervals, correlation.
- **Helpful later:** simple algebra for regression; calculus and matrices for machine learning (Q25).
- Software does the arithmetic; your job is to choose the right method and interpret.
**Worked example:** Headcount rises from 250 to 275: percentage change is (275 - 250) / 250 = 10%. Average attrition of two teams (200 and 50 people, 10% and 20%) is a weighted average: (200 x 0.10 + 50 x 0.20) / 250 = 12%, not the simple 15%.
**Likely follow-ups:** 1) *Do you need calculus?* Not for most analyst roles. 2) *How did you build the basics?* Practice on HR numbers.
**Common mistakes:** Averaging percentages without weighting (the 15% above); fearing advanced maths that the job does not need.

### Q9 ⭐⭐ 🟢 How much time do you spend practising statistics each week?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Discipline and a sustainable routine, with practice rather than passive watching.
**Say this in the interview:** "About 8 to 10 hours a week: roughly an hour each weekday and a longer block on the weekend, with most of the time spent solving problems on data, not watching videos." (Quote your true number.)
**Explain simply:**
- Weekdays (5 x 1 hour = 5 hours): 20 minutes of concept, 40 minutes of practice problems.
- Weekend (2 x 2 hours = 4 hours): one mini-project session and one review of mistakes.
- Total: 9 hours a week.
- Rule of thumb: at least 60% of time doing, not reading.
- Consistency beats long, rare sessions; keep a log of mistakes.
**Likely follow-ups:** 1) *What if you miss a week?* Resume with a short review, do not restart. 2) *How do you track progress?* A topic checklist and a score from self-tests (Q20).
**Common mistakes:** Binge-watching on Sunday then nothing for six days; never testing recall.

### Q10 ⭐⭐ 🟢 Which practice datasets have you used to apply statistics?
**Asked at:** commonly asked (no company-specific report found). Dataset descriptions below are from memory, unverified: they were not re-downloaded or checked today; confirm size and licence on the site.
**What the interviewer is checking:** Hands-on practice with realistic data, and sensible choice of dataset.
**Say this in the interview:** "I used the IBM HR Analytics employee attrition dataset on Kaggle for attrition and pay analysis, plus classic datasets like Titanic and Iris for fundamentals. HR data kept the work relevant to my background." (Name only datasets you really used.)
**Explain simply:**
- **HR:** IBM HR Analytics Employee Attrition (a fictional dataset of about 1,470 employees; attrition, income, age, overtime, satisfaction); good for proportions, chi-square, t-tests, regression.
- **General:** Titanic (survival by group), Iris and Palmer Penguins (distributions, comparing groups), Gapminder (trends), Superstore sales (business metrics).
- **Self-made:** your own mock payroll or attendance sheet in Excel, which forces you to define every column.
- Check data quality first: missing values, duplicates, odd ranges.
**Likely follow-ups:** 1) *Why not real company data?* Confidential; public or fictional data is safe to share in a portfolio. 2) *What did you find?* Give one concrete finding.
**Common mistakes:** Running tests without cleaning; treating a fictional dataset's findings as real-world facts.

### Q11 ⭐⭐ 🟡 How do you check that you truly understand a statistics concept and are not just memorising the formula?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Depth: can you explain, compute by hand and apply the concept?
**Say this in the interview:** "I use three checks: explain it in plain words as if to a manager, compute it by hand on five numbers and match the software, and say when it would be the wrong tool. If I can do all three, I understand it."
**Explain simply:**
- **Explain test:** teach it in two sentences with an HR example.
- **Rebuild test:** calculate by hand on a tiny dataset and compare with Excel or Python.
- **Break test:** state when it fails (outliers, tiny samples, wrong data type).
**Formula in plain words:** Sample standard deviation = square root of (sum of squared gaps from the average, divided by the number of values minus one).
**Worked example:** Five salaries (in thousands): 30, 32, 35, 38, 40. Average 35; squared gaps 25, 9, 0, 9, 25 add to 68; 68 / 4 = 17; square root is 4.12.
**Excel / Python:**
```python
import numpy as np

# five salaries in thousands
salaries = [30, 32, 35, 38, 40]

# step 1: the average
average_salary = sum(salaries) / len(salaries)

# step 2: how far each salary is from the average, squared
squared_gaps = [(salary - average_salary) ** 2 for salary in salaries]

# step 3: add up, divide by (count - 1) for a sample, then square root
sample_variance = sum(squared_gaps) / (len(salaries) - 1)
sample_standard_deviation = sample_variance ** 0.5

print("Average:", average_salary)
print("Squared gaps:", squared_gaps)
print("Sample standard deviation by hand:", round(sample_standard_deviation, 2))
print("Check with numpy (ddof=1):", round(np.std(salaries, ddof=1), 2))
```
Output: average 35.0, squared gaps `[25.0, 9.0, 0.0, 9.0, 25.0]`, and both methods give 4.12. In Excel, `=STDEV.S(A2:A6)` (Excel 2010 or later) returns the same 4.12 (not run in Excel here; verified by hand and Python). The `ddof=1` setting means "divide by n minus 1"; without it numpy divides by n and gives 3.69.
**Likely follow-ups:** 1) *Why n minus 1?* A sample's average is closer to its own data than the true average, so dividing by n underestimates spread. 2) *Break test for SD?* Strong outliers distort it.
**Common mistakes:** Memorising formulas without units or meaning; forgetting n versus n minus 1.

### Q12 ⭐⭐ 🟡 How do you learn a statistical test or concept you have never used before?
**Asked at:** commonly asked (no company-specific report found); the sources file notes interviewers ask about learning new techniques at snippet level.
**What the interviewer is checking:** A repeatable method for self-learning on the job, including checking assumptions.
**Say this in the interview:** "I follow a routine: what question does it answer, what assumptions does it need, a tiny example by hand, then run it on real data and compare with the software, and finally explain the result to a colleague. For the t-test, that meant checking that groups are independent and reasonably sized."
**Explain simply:**
1. **Purpose:** what business question is this for?
2. **Assumptions:** what must be true (independent groups, enough data)?
3. **Tiny example:** reproduce it by hand.
4. **Run it:** in Python or Excel on real data.
5. **Sanity check:** does the answer make business sense?
6. **Teach it:** write two lines for a manager.
**Worked example:** Compare engagement scores of two teams (8 people each): A averages 75.75, B 70.5.
**Excel / Python:**
```python
from scipy import stats
import numpy as np

# engagement scores of two teams
team_a_scores = [72, 75, 78, 80, 69, 74, 77, 81]
team_b_scores = [68, 70, 72, 75, 66, 71, 69, 73]

# Welch t-test: compares two averages without assuming equal spread
t_value, p_value = stats.ttest_ind(team_a_scores, team_b_scores, equal_var=False)

print("Team A average:", np.mean(team_a_scores))
print("Team B average:", np.mean(team_b_scores))
print("t:", round(t_value, 2), "p-value:", round(p_value, 4))
```
Output: averages 75.75 and 70.5, `t: 2.98`, `p-value: 0.0109`. A 5-point gap this size would be unusual by luck alone, but with 8 people per team treat it as a hint to investigate, not proof.
**Likely follow-ups:** 1) *What if assumptions fail?* Use a different test or a simulation. 2) *Which source do you trust?* Documentation and textbooks over random posts.
**Common mistakes:** Running a test from a tutorial without checking assumptions; reading p below 0.05 as "important".

### Q13 ⭐⭐ 🟡 How do you use AI assistants such as ChatGPT to learn statistics without depending on them?
**Asked at:** commonly asked (no company-specific report found); a modern gap-fill question.
**What the interviewer is checking:** Responsible AI use: you learn first, use AI as a tutor, and verify its output.
**Say this in the interview:** "I use AI to explain a concept another way, to generate practice problems and to review my work, but I never accept a number I have not checked. I attempt the problem first, then compare, and I recompute any figure with code or by hand."
**Explain simply:**
- **Good uses:** simpler explanations, practice questions, spotting errors in my reasoning, drafting code that I then read line by line.
- **Risks:** confident but wrong answers, wrong assumptions, invented references.
- **Habits:** attempt first; ask "why"; verify numbers independently; never paste confidential employee data into a public tool.
- **Test of independence:** can I solve a similar problem with no AI?
**Worked example:** An assistant claims "45 of 300 employees left, so the 95% interval is 10% to 20%". Check it: rate 15%, standard error about 2.06%, so the interval is about 11% to 19%.
**Excel / Python:**
```python
import math

# 45 of 300 employees left
leavers = 45
employees = 300
attrition_rate = leavers / employees

# standard error of a proportion, then 95% confidence interval
standard_error = math.sqrt(attrition_rate * (1 - attrition_rate) / employees)
lower_limit = attrition_rate - 1.96 * standard_error
upper_limit = attrition_rate + 1.96 * standard_error

print("Rate:", attrition_rate)
print("95% interval:", round(lower_limit * 100, 1), "to", round(upper_limit * 100, 1), "percent")
```
Output: `Rate: 0.15` and `95% interval: 11.0 to 19.0 percent`. The claimed 10% to 20% was a loose, rounded-out range (the real one is about 11% to 19%); recomputing caught it.
**Likely follow-ups:** 1) *Would you trust AI-written code?* Only after reading and testing it. 2) *Data privacy?* Use dummy or anonymised data.
**Common mistakes:** Copying answers without understanding; trusting a fluent but wrong explanation; sharing real employee data.

### Q14 ⭐⭐ 🟡 How would you prepare for a statistics and probability round in one week?
**Asked at:** commonly asked (no company-specific report found); the sources file says candidate reports describe probability and statistics as the hardest part of some analytics loops (snippet only, unverified).
**What the interviewer is checking:** Can you plan under time pressure and pick the highest-value topics instead of panicking?
**Say this in the interview:** "I would spend the week on the topics that are asked most: descriptive statistics, probability basics, distributions, hypothesis testing and confidence intervals. Each day I would learn one idea, solve problems on paper, and then say the answer out loud."
**Explain simply:**
- **Day 1:** mean, median, mode, standard deviation, outliers. **Day 2:** probability rules (and, or, conditional) and Bayes' theorem (updating a chance after new evidence).
- **Day 3:** normal distribution, z-score (how many standard deviations a value is from the average), sampling and the central limit theorem (averages of big samples look bell-shaped).
- **Day 4:** hypothesis testing, p-value, Type I and Type II errors. **Day 5:** confidence intervals, A/B tests, correlation versus causation.
- **Day 6:** mixed timed mock questions, mistakes written in a notebook. **Day 7:** revise the notebook, rehearse 60-second spoken answers, sleep early.
- Daily rhythm: 60 minutes learning, 60 minutes problems, 20 minutes speaking answers aloud.
**Worked example:** A quick drill from Day 2: two fair dice, probability the sum is 7? There are 6 winning pairs out of 36, so 6/36 = 0.1667 (checked in Python).
**Likely follow-ups:** 1) *What if you only had one day?* Do descriptive statistics, p-value meaning, and the confidence interval meaning, because they come up most. 2) *How do you know you are ready?* I can explain each topic to a non-technical person in under a minute (see Q20).
**Common mistakes:** Memorising formulas without being able to explain them; skipping speaking practice; learning new topics on the last night.

### Q15 ⭐⭐ 🟡 Tell me about a time you got a statistics concept wrong and how you corrected it.
**Asked at:** commonly asked (no company-specific report found); behavioural version of the learning-journey questions.
**What the interviewer is checking:** Honesty, self-awareness and whether you actually learn from errors.
**Say this in the interview:** "I used to read a p-value of 0.03 as a 3% chance that my result was just luck. That is wrong. It is the chance of seeing a result this extreme if there were truly no effect. I corrected it by simulating the idea and by explaining it to a colleague." (Use a real story of your own; this is a sample you can adapt only if it is true for you.)
**Explain simply:**
- Structure the story: what I believed, how I found out, what I did to fix it, what I do now.
- **Fix:** I wrote the correct definition in my own words and tested it with a small simulation.
- **Habit now:** I check the question, "what is this number the probability of?", before reporting it.
**Worked example:** Out of 1,000 tests, suppose 100 effects are real and 900 are not. With 80% power (chance of catching a real effect) and a 5% false-alarm rate, we get 80 true hits and 45 false alarms. So 45 of 125 "significant" results, about 36%, are false, far more than "5%". This shows why a single small p-value is not a 5% chance of being wrong (calculated in Python).
**Excel / Python:**
```python
# Out of 1,000 tests: 100 real effects, 900 with no real effect
real_effects = 100
no_effects = 900
power = 0.80
false_alarm_rate = 0.05

# Real effects we catch, and no-effect tests that still look significant
true_hits = real_effects * power
false_alarms = no_effects * false_alarm_rate

# Share of "significant" results that are false alarms
share_false = false_alarms / (true_hits + false_alarms)
print(true_hits, false_alarms, round(share_false * 100, 1), "%")
```
```text
80.0 45.0 36.0 %
```
So 36% of the "significant" results are false alarms, not 5%.
**Likely follow-ups:** 1) *What did you change afterwards?* A checklist before any report. 2) *Would you do it differently?* Yes, ask a reviewer to read my interpretation, not just my numbers.
**Common mistakes:** Giving a fake perfect answer ("I never get things wrong"); choosing a trivial mistake; blaming the tool or the data.

### Q16 ⭐⭐ 🟡 How do you explain a statistical result, such as a p-value or confidence interval, to a non-technical manager?
**Asked at:** commonly asked (no company-specific report found); no source in the sources file covers this question directly.
**What the interviewer is checking:** Can you translate numbers into a decision without jargon or false certainty?
**Say this in the interview:** "I start with the business answer, then the size of the effect, then how sure we are, in plain words. I avoid saying 'statistically significant' without saying what it means for the decision."
**Explain simply:**
- **Confidence interval** (a range of plausible values for the true figure): "Our best estimate is 17%, and the true figure is plausibly between 12% and 22%."
- **p-value** (how surprising our data would be if nothing were really going on): "If overtime made no difference, we would see a gap this large very rarely, so overtime is probably linked to leaving."
- Always add what it does not mean: a link is not proof of cause; a small p-value does not say the effect is big.
- Use a simple picture: a range bar rather than a table of statistics.
**Formula in plain words:** 95% interval = estimate, plus or minus 1.96 times the standard error (the typical wobble of the estimate between samples). Standard error for a percentage = square root of (rate x (1 - rate) / sample size).
**Worked example:** In an engagement survey of 200 employees, 34 plan to leave: 17%.
**Excel / Python:**
```python
import math

# Survey of 200 employees: 34 said they plan to leave
employees_surveyed = 200
employees_planning_to_leave = 34

# Our best single estimate: the sample percentage
leave_rate = employees_planning_to_leave / employees_surveyed

# Standard error: how much this percentage would wobble from sample to sample
standard_error = math.sqrt(leave_rate * (1 - leave_rate) / employees_surveyed)

# 95 percent confidence interval: estimate plus or minus 1.96 standard errors
lower_limit = leave_rate - 1.96 * standard_error
upper_limit = leave_rate + 1.96 * standard_error

print("Estimate:", round(leave_rate * 100, 1), "%")
print("95% interval:", round(lower_limit * 100, 1), "% to", round(upper_limit * 100, 1), "%")
```
```text
Estimate: 17.0 %
95% interval: 11.8 % to 22.2 %
```
To the manager: "About 17% plan to leave; the true company-wide figure is plausibly 12% to 22%. Even the low end is worth a retention plan." (This simple formula suits samples this large; very small samples need other methods.)
**Likely follow-ups:** 1) *Is 95% the chance the true value is inside this one interval?* Strictly, it describes how the method behaves over many samples; for a manager, "plausible range" is a fair plain version. 2) *What if the manager wants yes or no?* Give a recommendation with the uncertainty attached.
**Common mistakes:** Quoting "p < 0.05" with no meaning; hiding the range; claiming cause from a link.

### Q17 ⭐ 🟢 Do certifications or online courses in statistics help, and have you done any?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you learn actively, and do you know a certificate is not the same as skill?
**Say this in the interview:** "Courses help me get structure and a study order, but I judge them by what I can do afterwards. I pair every course with a small project so I can show the skill, not just the certificate."
**Explain simply:**
- Free, well-known options I am confident exist: Khan Academy "Statistics and Probability", the free OpenIntro Statistics textbook, StatQuest videos on YouTube, and Coursera or edX courses (many can be audited free; offers and content change, check the current page).
- A certificate may help a CV get past a first filter, but interviewers test understanding with questions.
- Only claim courses you have really done. If you have done none yet, say what you are doing now (see Q21).
**Likely follow-ups:** 1) *Which one would you pick first?* A free beginner course plus practice problems. 2) *Does a certificate replace experience?* No; a project shows more.
**Common mistakes:** Collecting certificates without practising; listing a course you only watched half of; saying a certificate makes you job-ready.

### Q18 ⭐ 🟢 Have you built a portfolio project that uses statistics?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Evidence that you applied statistics to a real question, not only studied it.
**Say this in the interview:** "Yes (only if true): I analysed an employee attrition dataset, tested whether overtime was linked to leaving, and reported the result with a confidence range and a recommendation." If you have not yet, say: "I am building one now" and describe it as in Q19.
**Explain simply:**
- A good project has: a clear business question, clean data, descriptive statistics, one or two tests, a chart, and a plain-language conclusion.
- Be ready to explain every number, including what you would not conclude.
- Keep it on GitHub or a shared notebook with a short README.
- **Mini-project ideas (each 1 to 2 weekends, public or self-made data):** 1) attrition rate by department with a confidence interval (Q16); 2) overtime versus leaving, chi-square test (Q19); 3) pay gap check: median and mean salary by group, with a t-test; 4) simulate a mock A/B test of two training formats on invented scores; 5) simple regression of salary on years of experience, with a residual plot.
**Likely follow-ups:** 1) *What was the hardest part?* Cleaning data and choosing the right test. 2) *What would you improve?* Add a model with controls (Q25), or more data.
**Common mistakes:** Claiming a project you cannot explain; showing code without interpretation; overclaiming cause.

### Q19 ⭐ 🟡 How would you build a statistics-based portfolio project from a public HR dataset such as employee attrition?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you turn a dataset into a structured, business-focused analysis?
**Say this in the interview:** "I would start with a business question, such as 'what is linked to employees leaving?', clean the data, describe it, test a few specific ideas, and finish with recommendations and the limits of the data."
**Explain simply:**
- **Dataset:** the IBM HR Analytics Employee Attrition and Performance dataset on Kaggle (a widely used, fictional dataset made by IBM data scientists; check the current Kaggle page and licence before use).
- **Steps:** 1) question; 2) check missing values and duplicates; 3) overall attrition rate; 4) attrition by group (department, overtime, tenure); 5) test with chi-square (for two categories) or t-test (for numbers such as income); 6) charts; 7) conclusions and limits.
- **State limits:** the data is fictional and observational, so links are not proof of cause.
**Worked example:** The numbers below are invented for teaching (not from the real dataset). Say 150 employees work overtime, 45 of them left; 450 do not, 60 left.
**Excel / Python:**
```python
from scipy import stats

# Rows: works overtime / no overtime. Columns: left / stayed
overtime_left, overtime_stayed = 45, 105
no_overtime_left, no_overtime_stayed = 60, 390
observed_table = [[overtime_left, overtime_stayed],
                  [no_overtime_left, no_overtime_stayed]]

# Attrition rate in each group
overtime_rate = overtime_left / (overtime_left + overtime_stayed)
no_overtime_rate = no_overtime_left / (no_overtime_left + no_overtime_stayed)
print("Attrition with overtime:", round(overtime_rate * 100, 1), "%")
print("Attrition without overtime:", round(no_overtime_rate * 100, 1), "%")

# Chi-square test of independence (is leaving linked to overtime?)
chi2_value, p_value, degrees_of_freedom, expected_counts = stats.chi2_contingency(
    observed_table, correction=False)
print("Chi-square:", round(chi2_value, 2))
print("p-value:", p_value)
```
```text
Attrition with overtime: 30.0 %
Attrition without overtime: 13.3 %
Chi-square: 21.65
p-value: 3.2806035450166277e-06
```
Attrition is 30% with overtime versus 13.3% without, and the tiny p-value says a gap this large is very unlikely by chance. Conclusion: overtime is linked to leaving, so review workloads; it does not prove overtime causes it. (Requires scipy; `correction=False` skips a small-sample adjustment.)
**Likely follow-ups:** 1) *Which other tests?* t-test for income by leaver status. 2) *How do you handle other factors?* Logistic regression (Q25).
**Common mistakes:** No business question; testing everything and reporting only "significant" hits (Q24); skipping the limits.

### Q20 ⭐ 🟡 How would you set up a self-check test to measure your own statistics level?
**Asked at:** commonly asked (no company-specific report found); this is a gap-fill question.
**What the interviewer is checking:** Do you measure your own skill honestly rather than guess?
**Say this in the interview:** "I would write a 20-question test across the core topics, answer it closed-book and timed, mark it honestly, and repeat it monthly. Each wrong answer goes into a mistakes notebook."
**Explain simply:**
- **Level 1 (basic):** mean, median, standard deviation, percentages, simple probability. **Level 2 (job-ready):** distributions, z-scores, sampling, p-value and confidence interval meaning, correlation versus causation, A/B test reading.
- **Level 3 (strong):** choosing the right test, assumptions, power, Bayes, regression interpretation.
- Mix three question types: calculate, explain aloud in plain words, and spot the error in a flawed claim.
- **Scoring (my own rule of thumb, not a standard):** below 60% revise Level 1; 60 to 80% focus on weak topics; above 80% move up a level.
- Sample questions: "A dice is rolled twice; chance of two sixes?" (1/36); "What does a 95% interval tell a manager?"; "Why is median pay better than mean pay when a few salaries are huge?"
- **A ready 8-question self-check (answers checked in Python; do it closed-book in 20 minutes):**
  1. Salaries 30, 32, 35, 38, 200 (thousands): mean and median? Answer: mean 67, median 35; the median is the fairer "typical" pay.
  2. Two dice, probability the sum is 7? Answer: 6/36 = 16.7%.
  3. Headcount 250 to 275: percentage change? Answer: 10%.
  4. Score 80, team average 70, standard deviation 5: z-score? Answer: 2 (two standard deviations above average).
  5. 45 of 300 left: rate and rough 95% interval? Answer: 15%, about 11% to 19%.
  6. In plain words, what is a p-value? Answer: how surprising our data would be if there were truly no effect; not the chance we are wrong.
  7. 20 tests at the 5% level, nothing real: chance of at least one false hit? Answer: about 64%.
  8. A disease affects 2% of people; a test catches 90% of cases and wrongly flags 10% of healthy people. If you test positive, chance you have it? Answer: about 15.5% (Bayes' theorem).
  Score 7 or 8: move up a level; 5 or 6: revise the missed topics; below 5: repeat Level 1.
**Likely follow-ups:** 1) *Where do you get questions?* The practice sets in free courses such as Khan Academy, plus the questions in this book. 2) *How often?* Monthly.
**Common mistakes:** Open-book testing; only checking calculations; not recording scores over time.

### Q21 ⭐ 🟡 What is your plan to improve your statistics and maths over the next three months?
**Asked at:** commonly asked (no company-specific report found); gap-fill.
**What the interviewer is checking:** Is your plan specific, realistic and tied to the job?
**Say this in the interview:** "Month one is foundations, month two is testing and inference, month three is a portfolio project and mock interviews. I study about an hour on weekdays and longer on weekends."
**Explain simply:**
- **Month 1:** descriptive statistics, probability, distributions; spreadsheet and Python practice on small HR data.
- **Month 2:** sampling, confidence intervals, hypothesis tests, A/B tests, correlation; start a mistakes notebook.
- **Month 3:** one end-to-end project (Q19), regression basics, mock interviews, explain results aloud.
- **Daily (about 60 to 90 minutes):** 30 minutes learn, 30 minutes problems, 15 minutes explain aloud or write a summary.
- **Checkpoints:** the self-check test (Q20) at the end of each month.
- **Job-ready means:** you can explain every Level 2 topic in under a minute, you have one finished project with a write-up (Q18), and you score above 80% on the self-check.
- **Free resources and datasets to use:** see Q6 and Q10.
- Maths needed is modest: percentages, algebra, basic probability, reading graphs (see Q8).
**Likely follow-ups:** 1) *What if you fall behind?* Cut scope, never skip practice. 2) *What would you drop?* Advanced theory such as proofs.
**Common mistakes:** An overloaded plan; only watching videos; no deadline or output.

### Q22 ⭐ 🟡 What is the difference between learning statistics for exams and learning it for day-to-day data analysis?
**Asked at:** commonly asked (no company-specific report found); gap-fill.
**What the interviewer is checking:** Do you understand that real work needs judgement, not only formulas?
**Say this in the interview:** "In exams the question is clean and the method is given. At work the question is vague, the data is messy, and my job is to choose the method, check assumptions and explain the result to someone who has to decide."
**Explain simply:**
- **Exams:** clean data, one right answer, memorised formulas, no consequences.
- **Work:** unclear questions, missing or biased data, several reasonable methods, decisions and money depend on the answer.
- **Work needs:** framing the question, cleaning data, choosing a method, checking assumptions, visualising, and communicating limits.
- Software does the arithmetic; the analyst must know what the numbers mean.
**Worked example:** An exam gives you two clean groups and asks for a t-test. At work, "why are people leaving?" has no group labels, some salary values are blank, and you must decide what to compare first.
**Likely follow-ups:** 1) *How do you bridge the gap?* Practise on real, messy datasets. 2) *Do formulas still matter?* Yes, for understanding, but not for memorising.
**Common mistakes:** Treating tools as magic; ignoring data quality; reporting results with no recommendation.

### Q23 ⭐ 🟡 How do you keep your statistics skills current while working a full-time job?
**Asked at:** commonly asked; the sources file notes a similar "how do you stay up to date with statistical methods" question (snippet only).
**What the interviewer is checking:** Is your learning habit sustainable and connected to real work?
**Say this in the interview:** "I use small daily habits: 20 to 30 minutes, tied to a real work question, plus one longer weekend session. I apply new ideas to my own data so they stick."
**Explain simply:**
- **Weekday habit:** one concept or one problem a day, on the commute or at lunch.
- **Weekend:** one mini-project or a mock question set.
- **Work link:** use the new idea in a real report (for example, add a confidence range to an attrition figure).
- **Community:** read a few trusted blogs, follow StatQuest or similar free video channels, discuss with peers.
- Re-take the self-check test (Q20) every quarter.
**Likely follow-ups:** 1) *What if you have no time in a busy week?* Do a 10-minute review rather than nothing. 2) *How do you choose what to learn?* Whatever the next work problem needs.
**Common mistakes:** Binge studying once a month; only passive reading; never applying anything at work.

### Q24 ⭐ 🟡 What are the most common statistics mistakes beginners make, and how do you avoid them?
**Asked at:** commonly asked (no company-specific report found); gap-fill.
**What the interviewer is checking:** Do you know the classic traps and have habits to avoid them?
**Say this in the interview:** "The big ones are confusing correlation with cause, misreading p-values, using the mean when data is skewed, testing many things and reporting only the hits, and ignoring sample size."
**Explain simply:**
- **Correlation is not causation:** overtime and attrition moving together does not prove one causes the other.
- **Misread p-value:** it is not the chance the result is wrong (Q15).
- **Mean with skewed data:** a few very high salaries drag the mean up; report the median too.
- **Many tests:** each extra test gives another chance of a false alarm (the multiple-testing problem). Fix: decide the questions in advance, or adjust the threshold (for example, the Bonferroni method divides 0.05 by the number of tests).
- **Small samples and bias:** a survey of 10 volunteers does not represent 5,000 employees.
- **Avoid by habit:** plot the data first, state the question first, report ranges, and write the limits.
**Worked example:** Run 20 independent tests at the 5% level when nothing is really going on: the chance of at least one false "significant" result is 1 minus 0.95 to the power 20.
**Excel / Python:**
```python
# Chance of at least one false alarm when running 20 tests at the 5 percent level
tests_run = 20
chance_of_no_false_alarm_per_test = 0.95
chance_of_no_false_alarm_at_all = chance_of_no_false_alarm_per_test ** tests_run
chance_of_at_least_one_false_alarm = 1 - chance_of_no_false_alarm_at_all
print(round(chance_of_at_least_one_false_alarm * 100, 1), "%")
```
```text
64.2 %
```
So with 20 tests, you are more likely than not to get a false hit. (This assumes the tests are independent.)
**Likely follow-ups:** 1) *How do you check for skew?* Plot a histogram and compare mean and median. 2) *How do you test causation?* A randomised experiment, not a data link.
**Common mistakes:** Hunting for significance; reporting only the favourable result; skipping charts.

### Q25 ⭐ 🟡 Where does statistics end and machine learning begin, and what would you learn after statistics?
**Asked at:** commonly asked (no company-specific report found); gap-fill.
**What the interviewer is checking:** Do you understand the relationship, without overclaiming ML skills?
**Say this in the interview:** "The two overlap. Statistics focuses on explaining relationships and measuring uncertainty. Machine learning focuses on predicting well on new data. I would learn regression properly first, then basic prediction models and how to test them fairly."
**Explain simply:**
- **Statistics:** "Is overtime linked to leaving, and how sure are we?" Emphasis on explanation and uncertainty.
- **Machine learning (ML):** "Which employees are most likely to leave next quarter?" Emphasis on prediction accuracy on unseen data.
- **Bridge:** linear and logistic regression belong to both worlds.
- **After statistics, in order:** 1) regression and its assumptions; 2) train and test split, cross-validation (testing on data the model has not seen); 3) overfitting (memorising noise); 4) simple models such as decision trees; 5) ethics and bias (especially in HR data).
- **Honest note:** a data analyst job rarely needs deep ML; strong statistics, SQL and communication matter first.
**Likely follow-ups:** 1) *Would you build an attrition prediction model?* Yes, as a learning project, with fairness checks and no automatic decisions about people. 2) *Why logistic regression first?* It is simple and explainable to managers.
**Common mistakes:** Jumping into ML without statistics; testing on the same data you trained on; claiming ML expertise from one tutorial.
