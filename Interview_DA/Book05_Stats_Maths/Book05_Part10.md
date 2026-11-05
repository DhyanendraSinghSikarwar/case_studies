# Book 5 — Statistics & Maths for Data Analysts | Part 10: Scenario-Based Statistics Questions 🔴

**Target:** 60 questions | **Actual:** 64 questions
**Scope:** scenario-based statistics and probability questions asked in Hyderabad/Bengaluru analyst loops: applying statistics to business and HR situations, judging evidence, bias, A/B pitfalls and explaining results.

### Q1 ⭐⭐⭐ 🟢 Average customer satisfaction (CSAT) fell 10% this quarter. How would you analyse it?
**Asked at:** commonly asked; the sources file lists "CSAT dropped 10%" as a typical scenario in prep guides such as Guvi (snippet only, no company-specific report).
**What the interviewer is checking:** Do you follow a calm order (is the number right, is it real, where did it fall) instead of jumping to a cause?
**Say this in the interview:** "First I check the number: how CSAT is defined, how many responses, and whether anything changed in the survey. Then I ask if the drop is bigger than normal wobble. Then I split it by channel, region, product and time to find where it fell, and check whether the mix of customers changed."
**Explain simply:**
- **CSAT** is the average score customers give in a satisfaction survey (for example 1 to 5).
- Step 1, data check: same survey, same question, same response rate, no broken data feed.
- Step 2, noise check: compare the drop with normal quarter-to-quarter variation and the margin of error.
- Step 3, segment: a fall can come from one channel getting worse, or from the **mix** shifting towards a channel that always scores lower.
- Step 4, only then look at causes (new policy, staffing, product issue) and say what is evidence and what is a guess.
**Worked example:** Overall CSAT fell from 4.34 to 3.92, about 10%. But each channel scored exactly the same as before; the survey simply got fewer chat responses and more email responses.

| Channel | Last quarter responses | This quarter responses | CSAT (both quarters) |
|---|---|---|---|
| Chat | 600 | 50 | 4.6 |
| Phone | 300 | 400 | 4.0 |
| Email | 100 | 550 | 3.8 |

**Excel / Python:**
```python
# Responses and average CSAT by channel (Chat, Phone, Email)
last_quarter_responses = [600, 300, 100]
last_quarter_avg_csat = [4.6, 4.0, 3.8]
this_quarter_responses = [50, 400, 550]
this_quarter_avg_csat = [4.6, 4.0, 3.8]

# Overall average = sum(responses * csat) / total responses
def overall_average(responses, averages):
    total_points = 0
    for count, avg in zip(responses, averages):
        total_points = total_points + count * avg
    return total_points / sum(responses)

last_overall = overall_average(last_quarter_responses, last_quarter_avg_csat)
this_overall = overall_average(this_quarter_responses, this_quarter_avg_csat)
print("Last quarter overall CSAT:", round(last_overall, 2))
print("This quarter overall CSAT:", round(this_overall, 2))
print("Change:", round((this_overall - last_overall) / last_overall * 100, 1), "%")
```
```text
Last quarter overall CSAT: 4.34
This quarter overall CSAT: 3.92
Change: -9.7 %
```
The headline fell almost 10% although no channel got worse; the drop is a mix effect, so the fix is in how we sample or serve customers, not in a service failure.
**Likely follow-ups:** 1) *What if it is real?* Segment further (agent, product, week) and read the comments. 2) *Is 10% a lot?* Compare with past quarters and the margin of error (Q5).
**Common mistakes:** Naming a cause before checking the data; ignoring changes in who responded.

### Q2 ⭐⭐⭐ 🟢 Your manager says the average salary of the team is 8 lakh, but most people feel they earn less. What could explain this, and what would you report instead?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that the mean is pulled by extreme values and that the median describes the typical person?
**Say this in the interview:** "The average, or mean, is dragged up by a few very high salaries, so most people really can earn less than it. I would report the median, with the 25th and 75th percentiles, and show the distribution."
**Explain simply:**
- **Mean** = total salary divided by headcount. One very large salary raises it for everyone.
- **Median** = the middle person's salary: half earn less, half earn more.
- **Percentiles** (25th, 75th) show the range where the middle half of people sit.
- Salary data is usually **right-skewed** (a long tail of high earners), so mean is above median.
**Formula in plain words:** mean = sum of all salaries / number of people; median = value at the middle after sorting.
**Worked example:** Ten people, nine earn 4.5 to 8 lakh, one senior manager earns 24.5 lakh. The mean is exactly 8 lakh, but eight of ten earn less than 8.
**Excel / Python:**
```python
import numpy as np

# Annual salaries of 10 team members, in lakh
salaries_in_lakh = [4.5, 5, 5.5, 5.5, 6, 6.5, 7, 7.5, 8, 24.5]

# Mean is pulled up by the one very high salary (the manager)
mean_salary = np.mean(salaries_in_lakh)
# Median is the middle value, so one big number cannot drag it
median_salary = np.median(salaries_in_lakh)
# 25th and 75th percentile show the typical spread
p25, p75 = np.percentile(salaries_in_lakh, [25, 75])
below_mean = sum(1 for s in salaries_in_lakh if s < mean_salary)

print("Mean:", mean_salary)
print("Median:", median_salary)
print("25th to 75th percentile:", p25, "to", p75)
print("People earning below the mean:", below_mean, "of", len(salaries_in_lakh))
```
```text
Mean: 8.0
Median: 6.25
25th to 75th percentile: 5.5 to 7.375
People earning below the mean: 8 of 10
```
The "typical" salary is about 6.25 lakh, not 8. In Excel: `=MEDIAN(B2:B11)` and `=QUARTILE.INC(B2:B11,1)` (Excel 2010+; not run in Excel here).
**Likely follow-ups:** 1) *Is the mean wrong?* No, it is right for total payroll cost, wrong for "typical". 2) *What else would you show?* A histogram or box plot.
**Common mistakes:** Reporting only the mean; calling the median "the average" without saying so.

### Q3 ⭐⭐⭐ 🟢 A report shows attrition went from 12% to 14% in one month. How do you decide whether this is a real increase or normal fluctuation?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that small headcounts make rates jumpy and that you must compare a change with its usual noise?
**Say this in the interview:** "I ask how many people that is, then compare the change with normal month-to-month variation. With 500 staff, 12% to 14% is only about 1.4 standard errors, so on its own it is within normal fluctuation. I would watch the trend over several months before calling it real."
**Explain simply:**
- Rates move by chance even when nothing changed, more so for small headcounts.
- **Standard error** = the typical size of that chance wobble.
- A **z-score** says how many standard errors the change is; beyond about 2 is usually treated as unusual.
- Also check the definition: monthly rate vs annualised rate (12% a month would be extreme, so I would confirm it is annualised or a rolling 12-month figure) and look at the last 6 to 12 months.
**Formula in plain words:** standard error = square root of (rate x (1 - rate) / headcount); z = (new rate - old rate) / standard error.
**Worked example:** Headcount 500: 12% is 60 leavers, 14% is 70.
**Excel / Python:**
```python
import math
from scipy import stats

# Headcount and attrition rate; compare last month with this month
headcount = 500
last_month_rate = 0.12
this_month_rate = 0.14

# Typical wobble if the true rate stayed at 12%
standard_error = math.sqrt(last_month_rate * (1 - last_month_rate) / headcount)
z_score = (this_month_rate - last_month_rate) / standard_error
p_value = 1 - stats.norm.cdf(z_score)

# A rough range of normal values (2 standard errors either side of 12%)
low_normal = last_month_rate - 2 * standard_error
high_normal = last_month_rate + 2 * standard_error

print("Standard error:", round(standard_error * 100, 2), "percentage points")
print("z-score:", round(z_score, 2))
print("One-sided p-value:", round(p_value, 3))
print("Normal range:", round(low_normal * 100, 1), "% to", round(high_normal * 100, 1), "%")
```
```text
Standard error: 1.45 percentage points
z-score: 1.38
One-sided p-value: 0.084
Normal range: 9.1 % to 14.9 %
```
A reading of 14% sits inside the normal 9% to 15% band, so I would call it "watch", not "alarm", and recheck next month.
**Likely follow-ups:** 1) *What if it stays at 14% for three months?* A sustained shift is real evidence even if one month is not. 2) *Better tool?* A control chart (Q19).
**Common mistakes:** Reacting to a single-month move; ignoring headcount size.

### Q4 ⭐⭐⭐ 🟢 The sales team claims a new campaign worked because sales rose 5% after launch. How would you check that claim?
**Asked at:** commonly asked (no company-specific report found); shaped like the "campaign effect" scenarios in generic prep material.
**What the interviewer is checking:** Do you ask "compared with what?" and think of seasonality and other causes?
**Say this in the interview:** "A 5% rise after launch is a before and after comparison, which also catches seasonality, festivals, price changes and trend. I would compare with a similar region or period that did not get the campaign, and check if 5% is bigger than normal weekly variation."
**Explain simply:**
- **Seasonality**: sales rise at some times of year anyway (festival season).
- Best check: a **control group** (similar stores or regions without the campaign), ideally chosen randomly.
- If no control exists: compare with the same weeks last year and with the earlier trend.
- Check the noise: how much do weekly sales normally move?
**Worked example:** Campaign region grew 5%, but a similar region with no campaign grew 4%. The extra effect is about 1 point (a **difference-in-differences**: change in test region minus change in control region).
**Excel / Python:**
```python
# Sales index: the campaign region vs a similar region without the campaign
campaign_region_before = 100
campaign_region_after = 105
control_region_before = 100
control_region_after = 104

campaign_growth = campaign_region_after - campaign_region_before
control_growth = control_region_after - control_region_before

# Growth beyond what happened anyway
extra_growth_due_to_campaign = campaign_growth - control_growth
print("Campaign region growth:", campaign_growth, "%")
print("Similar region growth without campaign:", control_growth, "%")
print("Growth we can credit to the campaign:", extra_growth_due_to_campaign, "%")
```
```text
Campaign region growth: 5 %
Similar region growth without campaign: 4 %
Growth we can credit to the campaign: 1 %
```
Only about 1 of the 5 points is plausibly the campaign, and even that needs a noise check.
**Likely follow-ups:** 1) *No control region?* Use same period last year and a trend model. 2) *Cost?* Compare the 1% extra sales with campaign spend.
**Common mistakes:** Crediting everything after launch to the campaign; skipping the noise check.

### Q5 ⭐⭐⭐ 🟡 You have survey responses from 200 of 5,000 employees. How confident can you be in the results, and what would you check first?
**Asked at:** commonly asked; the sources file notes entry-level stats questions revolve around sampling and generalisability (Taggd, 365 Data Science, snippet only).
**What the interviewer is checking:** Do you separate sample size (margin of error) from sample quality (bias)?
**Say this in the interview:** "Size is fine: 200 gives roughly plus or minus 7 points on a yes/no result. What I check first is who answered. If the 200 are not a fair mix of departments, grades and locations, or only the happy or angry people replied, a large margin of error is the smaller problem."
**Explain simply:**
- **Margin of error** = how far the sample result may be from the true figure due to chance alone.
- It depends on the sample size, not much on the total headcount (200 of 5,000 is about 4%).
- **Bias** (a sample that is not representative) is not fixed by a bigger sample.
- First check: response rate by department, grade, tenure and location compared with the real headcount mix.
**Formula in plain words:** margin of error = 1.96 x square root of (share x (1 - share) / sample size).
**Worked example:** 60% of the 200 respondents are satisfied.
**Excel / Python:**
```python
import math

# 200 of 5000 employees answered; 60% said they are satisfied
sample_size = 200
population_size = 5000
share_satisfied = 0.60

# Standard error of a proportion
standard_error = math.sqrt(share_satisfied * (1 - share_satisfied) / sample_size)
margin_of_error = 1.96 * standard_error

# Finite population correction (small effect because 200 is only 4% of 5000)
correction = math.sqrt((population_size - sample_size) / (population_size - 1))
corrected_margin = margin_of_error * correction

print("Margin of error:", round(margin_of_error * 100, 1), "points")
print("With population correction:", round(corrected_margin * 100, 1), "points")
print("Range:", round((share_satisfied - margin_of_error) * 100, 1), "% to",
      round((share_satisfied + margin_of_error) * 100, 1), "%")
```
```text
Margin of error: 6.8 points
With population correction: 6.7 points
Range: 53.2 % to 66.8 %
```
If the sample is fair, the true satisfaction is probably between 53% and 67%.
**Likely follow-ups:** 1) *How to improve?* Stratified sampling and follow-ups with non-responders. 2) *Does 5,000 vs 50,000 matter?* Hardly.
**Common mistakes:** Quoting the margin of error for a biased sample; thinking you need a fixed percentage of the population.

### Q6 ⭐⭐⭐ 🟡 A result has p = 0.03 but the effect is only 0.2% lift in revenue. Would you recommend acting on it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you separate statistical significance from practical importance?
**Say this in the interview:** "The p-value says the lift is probably not zero, not that it is big. I would convert 0.2% into rupees and compare with the cost and risk of the change. If it pays for itself, act; if not, it is statistically real but practically irrelevant."
**Explain simply:**
- **p-value**: how surprising the data would be if there were truly no effect. 0.03 means fairly surprising, so the effect is probably real.
- **Effect size** is how large the effect is; a tiny effect can be "significant" with huge samples.
- Look at the **confidence interval**: the lift may be anywhere from near 0 to a bit more.
- Decide on value: extra revenue minus cost of the change, plus whether it is repeatable.
**Worked example:** Revenue per user is 500 rupees with spread 800. A 0.2% lift is 1 rupee per user. To get p = 0.03 for that you need millions of users, and it is worth 20 lakh a month at 20 lakh users, which may or may not beat the cost.
**Excel / Python:**
```python
from scipy import stats

# Revenue per user: average 500 rupees, spread (standard deviation) 800 rupees
average_revenue = 500
spread = 800
lift_percent = 0.2
lift_in_rupees = average_revenue * lift_percent / 100   # 1 rupee per user

# Standard error needed for p = 0.03 (two-sided)
z_for_p = stats.norm.ppf(1 - 0.03 / 2)
standard_error_needed = lift_in_rupees / z_for_p

# Users per group needed to get a standard error that small
users_per_group = 2 * spread**2 / standard_error_needed**2

# What the lift is worth: 20 lakh users a month
monthly_users = 2_000_000
extra_revenue = monthly_users * lift_in_rupees

print("Lift per user (rupees):", lift_in_rupees)
print("z-score at p = 0.03:", round(z_for_p, 2))
print("Users per group behind such a result: about", round(users_per_group / 1e6, 1), "million")
print("Extra revenue per month (rupees):", extra_revenue)
```
```text
Lift per user (rupees): 1.0
z-score at p = 0.03: 2.17
Users per group behind such a result: about 6.0 million
Extra revenue per month (rupees): 2000000.0
```
The result is statistically believable but worth only about 20 lakh rupees a month; whether to act depends on cost.
**Likely follow-ups:** 1) *What would you ask for?* The confidence interval. 2) *Is p = 0.03 strong?* Moderate; not proof.
**Common mistakes:** Saying "significant means important"; ignoring cost.

### Q7 ⭐⭐⭐ 🟡 Two branches have average sales of 52 and 55 units. How do you tell whether the 3-unit gap is real?
**Asked at:** commonly asked; the sources file lists "is the class height difference significant?" style questions from an AmbitionBox question bank (snippet only).
**What the interviewer is checking:** Do you know the gap alone is meaningless without spread and sample size?
**Say this in the interview:** "I need the spread of daily sales and the number of days for each branch. Then I run a two-sample t-test, which compares the gap with its expected chance variation. The same 3 units can be noise or real depending on that."
**Explain simply:**
- **Standard deviation** = how much daily sales usually vary around the average.
- **t-test**: compares two averages, accounting for variation and sample size.
- **Welch's** version does not assume both branches have equal spread (safer default).
- Also report the confidence interval of the gap and whether 3 units matters for business.
**Worked example:** Daily spread is 10 units in both branches. With 30 days each the gap is not clear; with 200 days each it is.
**Excel / Python:**
```python
from scipy import stats

# Same 3-unit gap, but two different amounts of data (daily sales, spread of 10 units)
for days_of_data in [30, 200]:
    result = stats.ttest_ind_from_stats(
        mean1=55, std1=10, nobs1=days_of_data,
        mean2=52, std2=10, nobs2=days_of_data,
        equal_var=False)
    print(days_of_data, "days per branch: t =", round(result.statistic, 2),
          ", p =", round(result.pvalue, 3))
```
```text
30 days per branch: t = 1.16 , p = 0.25
200 days per branch: t = 3.0 , p = 0.003
```
With 30 days, the gap could easily be chance (p = 0.25); with 200 days it is very unlikely to be chance. In Excel: `=T.TEST(range1, range2, 2, 3)` (2 tails, unequal variance; Excel 2010+; not run in Excel here).
**Likely follow-ups:** 1) *Data not normal?* Use Mann-Whitney or bootstrap. 2) *Same days compared?* Check weekday mix and branch size.
**Common mistakes:** Judging only on the gap; forgetting that branches differ in size or location mix.

### Q8 ⭐⭐⭐ 🟡 Ice-cream sales and drowning incidents rise together. A manager says to ban ice cream. How do you respond?
**Asked at:** commonly asked (no company-specific report found); a classic correlation-vs-causation example.
**What the interviewer is checking:** Do you recognise a confounder and explain it simply, respectfully?
**Say this in the interview:** "They move together because both rise in hot weather: more people buy ice cream and more people swim. Temperature is the hidden third factor, called a confounder. Banning ice cream would not reduce drownings. If we compare days with the same temperature, the link disappears."
**Explain simply:**
- **Correlation**: two things move together. It does not say one causes the other.
- **Confounder**: a third factor that drives both.
- Test: hold the confounder fixed (compare similar-temperature days) and see if the link remains.
- The HR twin: employees who attend more training get promoted more, but high performers may do both.
**Worked example:** I simulated 120 months where temperature drives both series.
**Excel / Python:**
```python
import numpy as np

# Simulate 120 months: hot weather drives both ice-cream sales and swimming (and drownings)
random_generator = np.random.default_rng(seed=7)
temperature = random_generator.uniform(15, 40, size=120)
ice_cream_sales = 10 * temperature + random_generator.normal(0, 20, size=120)
drownings = 0.2 * temperature + random_generator.normal(0, 1.5, size=120)

# Raw correlation between ice cream and drownings
raw_correlation = np.corrcoef(ice_cream_sales, drownings)[0, 1]

# Remove the part explained by temperature from each, then correlate what is left
ice_cream_leftover = ice_cream_sales - np.polyval(np.polyfit(temperature, ice_cream_sales, 1), temperature)
drowning_leftover = drownings - np.polyval(np.polyfit(temperature, drownings, 1), temperature)
adjusted_correlation = np.corrcoef(ice_cream_leftover, drowning_leftover)[0, 1]

print("Correlation ice cream vs drownings:", round(raw_correlation, 2))
print("After removing temperature:", round(adjusted_correlation, 2))
```
```text
Correlation ice cream vs drownings: 0.63
After removing temperature: -0.09
```
The strong link (0.63) falls to about zero once temperature is accounted for (this is simulated data built that way).
**Likely follow-ups:** 1) *How do you prove causation?* A randomised experiment. 2) *Other examples?* Shoe size and reading ability in children (age).
**Common mistakes:** Saying "correlation is never useful"; or treating it as proof.

### Q9 ⭐⭐⭐ 🟡 A dashboard shows overall conversion rate fell, but every individual channel's rate rose. How is that possible and what would you do?
**Asked at:** commonly asked; the sources file lists "KPI dropped, investigate" conversion questions on Dataford with mix shift as a cause (titles only).
**What the interviewer is checking:** Do you know Simpson's paradox and mix shift?
**Say this in the interview:** "It is possible because the overall rate is a weighted average. If traffic shifts towards a low-converting channel, the overall rate falls even though each channel improved. I would report per-channel rates and the traffic mix, and explain the shift."
**Explain simply:**
- Overall rate = total conversions / total visitors, so each channel counts in proportion to its traffic.
- **Mix shift**: the share of visitors from each channel changed.
- Also called **Simpson's paradox** when a trend flips between groups and the total.
- Decide which view answers the business question (channel quality vs overall result).
**Worked example:** May: 80% of visitors from email (8%), 20% from paid (2%). June: 20% from email (9%), 80% from paid (2.5%).
**Excel / Python:**
```python
# Visitors and conversion rate by channel in two months
email_visitors_may, email_rate_may = 8000, 0.08
paid_visitors_may, paid_rate_may = 2000, 0.02
email_visitors_june, email_rate_june = 2000, 0.09
paid_visitors_june, paid_rate_june = 8000, 0.025

# Overall rate = total conversions / total visitors
may_overall = (email_visitors_may * email_rate_may + paid_visitors_may * paid_rate_may) / (email_visitors_may + paid_visitors_may)
june_overall = (email_visitors_june * email_rate_june + paid_visitors_june * paid_rate_june) / (email_visitors_june + paid_visitors_june)

print("Email rate: 8.0% -> 9.0% (up)")
print("Paid rate: 2.0% -> 2.5% (up)")
print("Overall May:", round(may_overall * 100, 1), "%")
print("Overall June:", round(june_overall * 100, 1), "%")
```
```text
Email rate: 8.0% -> 9.0% (up)
Paid rate: 2.0% -> 2.5% (up)
Overall May: 6.8 %
Overall June: 3.8 %
```
Both channels improved, yet overall fell from 6.8% to 3.8% because most traffic moved to the weaker channel.
**Likely follow-ups:** 1) *What would you present?* Rates by channel plus traffic share, maybe a fixed-mix comparison. 2) *Is the campaign shift bad?* Depends on cost per customer.
**Common mistakes:** Reporting only the overall number; concluding the channels got worse.

### Q10 ⭐⭐⭐ 🟡 Why would you report median instead of mean for salary, delivery time or order value, and how would you justify it to a manager?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand skew and can explain it in business terms?
**Say this in the interview:** "These numbers have a long tail: a few very high salaries, very late deliveries or very large orders. Those stretch the mean, so it describes nobody's typical experience. The median is the middle value and tells the manager what a typical case looks like. I would still show the mean for total cost and percentiles for the tail."
**Explain simply:**
- Mean = total / count; median = middle value after sorting.
- If one extreme value shifts the mean a lot but the median barely moves, use the median.
- Justify with a simple example: "one stuck parcel should not make every customer look slow".
- For delivery time, also report a high percentile (for example 90th) because the tail is what customers complain about.
**Worked example:** 11 deliveries, one stuck for 30 days.
**Excel / Python:**
```python
import numpy as np

# Delivery times in days for 11 orders; one order got stuck for 30 days
delivery_days = [2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 30]

mean_days = np.mean(delivery_days)
median_days = np.median(delivery_days)
days_within_5 = sum(1 for d in delivery_days if d <= 5)

print("Mean:", round(mean_days, 1), "days")
print("Median:", median_days, "days")
print("Orders delivered within 5 days:", days_within_5, "of", len(delivery_days))
```
```text
Mean: 5.9 days
Median: 4.0 days
Orders delivered within 5 days: 10 of 11
```
The mean (5.9) suggests nearly 6 days, but 10 of 11 orders arrived in 5 days or less; the median of 4 describes the typical order.
**Likely follow-ups:** 1) *When is mean better?* For totals, such as revenue or payroll. 2) *Mean or median for symmetric data?* Both are similar.
**Common mistakes:** Hiding the tail completely; mixing up median with mode.

### Q11 ⭐⭐⭐ 🟡 You find a few extremely large orders in the data. Do you delete them? Walk through your decision.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you investigate before deleting, and document your choice?
**Say this in the interview:** "I do not delete automatically. First I check whether they are errors (extra zeros, test orders, duplicates). If they are real, such as a genuine bulk corporate order, I keep them but report median or show results with and without them. I document what I did."
**Explain simply:**
- **Outlier**: a value far from the rest. A common rule flags values above Q3 + 1.5 x IQR (IQR = Q3 minus Q1, the spread of the middle half).
- Decision tree: error, so fix or remove; real but rare, so keep and use robust measures (median); real and important (big customers), so analyse separately.
- Sensitivity check: show results with and without.
**Worked example:** 20 orders, two worth 45,000 and 52,000 while others are about 800 to 2,400.
**Excel / Python:**
```python
import numpy as np

# 20 order values in rupees; the last two are unusually large
order_values = [800, 950, 1000, 1100, 1200, 1250, 1300, 1400, 1500, 1500,
                1600, 1700, 1800, 1900, 2000, 2100, 2200, 2400, 45000, 52000]

# Flag outliers with the IQR rule (anything above Q3 + 1.5 x IQR)
q1, q3 = np.percentile(order_values, [25, 75])
upper_fence = q3 + 1.5 * (q3 - q1)
flagged = [v for v in order_values if v > upper_fence]
kept = [v for v in order_values if v <= upper_fence]

print("Upper fence:", upper_fence)
print("Flagged orders:", flagged)
print("Mean with all orders:", round(np.mean(order_values)))
print("Mean without flagged:", round(np.mean(kept)))
print("Median with all orders:", np.median(order_values))
print("Median without flagged:", np.median(kept))
```
```text
Upper fence: 3206.25
Flagged orders: [45000, 52000]
Mean with all orders: 6235
Mean without flagged: 1539
Median with all orders: 1550.0
Median without flagged: 1500.0
```
The two big orders move the mean from 1,539 to 6,235 but the median only from 1,500 to 1,550, so the median is safe either way.
**Likely follow-ups:** 1) *Cap instead of delete?* Winsorising caps extremes; state it clearly. 2) *Is a flagged value always wrong?* No.
**Common mistakes:** Deleting because it spoils the average; deleting silently.

### Q12 ⭐⭐⭐ 🟡 A new employee training programme was tried on 50 people and their average score rose. How would you test if the programme actually worked?
**Asked at:** commonly asked; the sources file mentions hypothesis-test examples (ticket closing) in an AmbitionBox question bank (snippet only).
**What the interviewer is checking:** Do you see that before and after alone is not proof and that a comparison group helps?
**Say this in the interview:** "A rise after training could be due to practice, time or a busy season. I would use a paired t-test on the same 50 people before and after, and better, compare their gain with a similar group that was not trained, ideally randomly chosen."
**Explain simply:**
- **Paired t-test**: compares each person's before and after score; tests if the average gain is zero.
- **Control group**: similar people without training; shows what would have happened anyway.
- Check selection: were the 50 volunteers or the keenest people?
- Report the size of the gain with a confidence interval, not just the p-value.
**Worked example:** Simulated data: trained group gains about 6 points; untrained group gains about 2.3.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Simulated test scores: trained group (50) and a similar untrained group (50)
random_generator = np.random.default_rng(seed=11)
trained_before = random_generator.normal(60, 10, size=50)
trained_after = trained_before + random_generator.normal(5, 6, size=50)
untrained_before = random_generator.normal(60, 10, size=50)
untrained_after = untrained_before + random_generator.normal(2, 6, size=50)

# Step 1: did trained people improve? (paired t-test: same people before and after)
trained_gain = trained_after - trained_before
paired = stats.ttest_1samp(trained_gain, 0)

# Step 2: did they improve more than people who were not trained?
untrained_gain = untrained_after - untrained_before
versus_control = stats.ttest_ind(trained_gain, untrained_gain, equal_var=False)

print("Average gain, trained:", round(trained_gain.mean(), 1))
print("Average gain, untrained:", round(untrained_gain.mean(), 1))
print("Before/after p-value:", f"{paired.pvalue:.2e}")
print("Trained vs untrained gain p-value:", round(versus_control.pvalue, 4))
```
```text
Average gain, trained: 6.0
Average gain, untrained: 2.3
Before/after p-value: 1.73e-09
Trained vs untrained gain p-value: 0.0012
```
Both groups improved, but the trained group improved by about 3.7 points more, which is unlikely to be chance (p = 0.0012). In Excel: `=T.TEST(after, before, 2, 1)` for the paired test (not run in Excel here).
**Likely follow-ups:** 1) *No control group?* Say the result is suggestive only. 2) *Test is skewed?* Wilcoxon signed-rank test.
**Common mistakes:** Treating before and after as independent groups; ignoring the control.

### Q13 ⭐⭐ 🟢 A column has 30% missing values (for example, salary or age). How do you decide what to do, and what bias could each choice introduce?
**Asked at:** commonly asked; the sources file lists missing data as a typical scenario in prep guides (Guvi and others, snippet only).
**What the interviewer is checking:** Do you ask why values are missing before choosing a fix?
**Say this in the interview:** "First I ask why it is missing: random, related to other columns, or related to the value itself, like high earners skipping salary. Then I choose: drop rows, fill with median or a model, or keep a 'missing' flag. Each can bias results, so I check how the answer changes."
**Explain simply:**
- **Missing at random**: missingness unrelated to the value; dropping rows is mostly safe, only less data.
- **Missing not at random**: for example high earners hide salary; any average of the answered rows is biased.
- **Drop rows**: loses data and can bias if the missing pattern is not random.
- **Fill with mean or median**: keeps rows but squeezes variation and can hide relationships.
- **Model-based fill or multiple imputation**: better, but needs assumptions; add a "was missing" flag and compare results.
**Worked example:** 1,000 employees; high earners skip the salary question more often.
**Excel / Python:**
```python
import numpy as np

# 1,000 employees' true salaries (lakh); high earners skip the salary question more often
random_generator = np.random.default_rng(seed=3)
true_salaries = random_generator.lognormal(mean=1.9, sigma=0.4, size=1000)
chance_of_missing = np.where(true_salaries > np.percentile(true_salaries, 60), 0.6, 0.12)
is_missing = random_generator.random(1000) < chance_of_missing
observed_salaries = true_salaries[~is_missing]

print("Share missing:", round(is_missing.mean() * 100), "%")
print("True average salary:", round(true_salaries.mean(), 2))
print("Average of the people who answered:", round(observed_salaries.mean(), 2))
```
```text
Share missing: 32 %
True average salary: 7.36
Average of the people who answered: 6.62
```
Dropping the blanks understates the average (6.62 vs 7.36) because the missing values were mostly the high ones.
**Likely follow-ups:** 1) *Is filling with the mean fine?* Only for small, random gaps. 2) *When drop the column?* If most is missing and it is not essential.
**Common mistakes:** Filling blindly without asking why; not reporting how much was filled.

### Q14 ⭐⭐ 🟢 Your report says the average hiring time is 30 days. The recruiter says it feels like 45. How would you investigate the difference?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you test definitions, data coverage and averages before deciding who is right?
**Say this in the interview:** "I would check the definition (posting to offer, or to joining), which roles are included, and whether still-open roles are left out. A report that counts only filled roles understates the delay. Then I look at the median and the distribution by role."
**Explain simply:**
- **Definition**: time to fill (requisition opened to offer accepted) vs time to hire (candidate applies to accepts) vs to joining; they differ.
- **Open roles are missing**: the hardest roles take longest, and the report skips them until filled (this is **censoring**: we only see completed cases).
- **Mix**: easy roles dominate the count; the recruiter remembers the hard ones.
- Memory is biased to painful cases; check median, 75th and 90th percentiles by role.
**Worked example:** 7 filled roles and 3 still open (60, 75, 90 days so far).
**Excel / Python:**
```python
import numpy as np

# Days taken for 7 roles that are filled, plus 3 roles still open (days open so far)
filled_days = [18, 22, 25, 27, 30, 35, 40]
still_open_days = [60, 75, 90]

mean_filled_only = np.mean(filled_days)
mean_including_open = np.mean(filled_days + still_open_days)
median_including_open = np.median(filled_days + still_open_days)

print("Average of filled roles only:", round(mean_filled_only, 1))
print("Average if open roles are counted:", round(mean_including_open, 1))
print("Median if open roles are counted:", median_including_open)
```
```text
Average of filled roles only: 28.1
Average if open roles are counted: 42.2
Median if open roles are counted: 32.5
```
Counting open roles moves the average from about 28 to 42, close to the recruiter's feeling; the real figure is at least that, since open roles are still not finished.
**Likely follow-ups:** 1) *Which number to report?* Median plus percentiles by role type, and state the definition. 2) *Proper method?* Survival analysis handles open cases.
**Common mistakes:** Deciding the recruiter is "just wrong"; ignoring still-open roles.

### Q15 ⭐⭐ 🟢 Explain 95% confidence interval to a non-technical manager using an attendance or survey example.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you explain it in plain words without the common wrong version?
**Say this in the interview:** "We checked 100 employees, not all, so the average attendance of 90.7% is an estimate. The 95% confidence interval is 89.6% to 91.7%: a range built so that if we repeated the survey many times, about 95 out of 100 such ranges would contain the true company average."
**Explain simply:**
- A sample gives an estimate; the interval says how precise it is.
- "95%" describes the method's long-run success rate, not a 95% chance for this one range.
- A narrower interval comes from more data or less variation.
- The wrong version: "95% of employees are in this range". No: it is about the average, not individuals.
**Formula in plain words:** interval = sample average plus or minus (about 2) x standard error; standard error = spread / square root of sample size.
**Worked example:** Attendance of a random sample of 100 employees (simulated), true average 92%.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Attendance % of a random sample of 100 employees
random_generator = np.random.default_rng(seed=5)
attendance_sample = random_generator.normal(loc=92, scale=6, size=100)

sample_mean = attendance_sample.mean()
standard_error = stats.sem(attendance_sample)
low, high = stats.t.interval(0.95, df=99, loc=sample_mean, scale=standard_error)
print("Sample average attendance:", round(sample_mean, 1), "%")
print("95% confidence interval:", round(low, 1), "% to", round(high, 1), "%")

# Check the idea: repeat the survey 10,000 times, count how often the interval catches the true 92%
catches = 0
for repeat in range(10000):
    repeat_sample = random_generator.normal(92, 6, size=100)
    repeat_low, repeat_high = stats.t.interval(0.95, df=99, loc=repeat_sample.mean(), scale=stats.sem(repeat_sample))
    if repeat_low <= 92 <= repeat_high:
        catches = catches + 1
print("Intervals that caught the true value:", catches / 100, "%")
```
```text
Sample average attendance: 90.7 %
95% confidence interval: 89.6 % to 91.7 %
Intervals that caught the true value: 95.5 %
```
In this unlucky sample the interval (89.6 to 91.7) happens to miss the true 92%; across 10,000 repeats about 95% of intervals caught it, which is what "95% confidence" means. In Excel: `=CONFIDENCE.T(0.05, STDEV.S(A2:A101), 100)` gives the plus/minus amount (Excel 2010+; not run in Excel here).
**Likely follow-ups:** 1) *How to narrow it?* Bigger sample. 2) *90% vs 95%?* 90% is narrower but less often right.
**Common mistakes:** Saying "95% probability the true value is in this range"; mixing it with individual spread.

### Q16 ⭐⭐ 🟢 Employee engagement survey: 85% of responders are satisfied, but only 20% of staff responded. Can you trust the 85%?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you spot non-response bias and bound what you know?
**Say this in the interview:** "I can trust it as the view of the 20% who answered, not of the whole company. The 80% silent staff could feel very different; people who are happy or very angry answer more often. I would compare responders with the staff profile and report the 85% as 'among respondents', with a range."
**Explain simply:**
- **Non-response bias**: the people who answered differ from those who did not.
- Margin of error covers chance only, not bias.
- Bound the truth: if all non-responders were unhappy, the company figure is 17%; if all satisfied, 97%.
- Actions: compare response rate across departments, send reminders, follow up a small random sample of non-responders.
**Worked example:** 1,000 staff, 200 responded, 170 satisfied.
**Excel / Python:**
```python
# 1,000 staff, 200 responded, 85% of responders are satisfied
all_staff = 1000
responders = 200
satisfied_responders = int(responders * 0.85)
non_responders = all_staff - responders

# Whole-company satisfaction under different guesses about non-responders
for guess in [0.0, 0.5, 0.85, 1.0]:
    satisfied_total = satisfied_responders + non_responders * guess
    print("If", int(guess * 100), "% of non-responders are satisfied: company =",
          round(satisfied_total / all_staff * 100), "%")
```
```text
If 0 % of non-responders are satisfied: company = 17 %
If 50 % of non-responders are satisfied: company = 57 %
If 85 % of non-responders are satisfied: company = 85 %
If 100 % of non-responders are satisfied: company = 97 %
```
The true company figure could be anywhere from 17% to 97%; the 85% is only reliable if silent staff think like responders.
**Likely follow-ups:** 1) *How to fix?* Raise response rate; weight by department. 2) *Is 20% always bad?* Not if the responders are representative, but you must show it.
**Common mistakes:** Presenting 85% as the company's satisfaction; calling the margin of error the full uncertainty.

### Q17 ⭐⭐ 🟢 A candidate scores 78 in a test where the team average is 70 and the standard deviation is 8. How would you explain how good that score is?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can turn a raw score into a position relative to the group (z-score), in plain words.
**Say this in the interview:** "78 is 8 points above the team average, and one standard deviation is 8 points, so the candidate is exactly one standard deviation above average. If scores are roughly bell-shaped, that is better than about 84% of the team."
**Explain simply:**
- **Standard deviation** is the typical distance of a score from the average. Here, a typical person is about 8 points away from 70.
- A **z-score** counts how many standard deviations you are above or below average. It lets us compare scores from different tests on one scale.
- The "84% of people" statement only holds if scores are roughly bell-shaped (normal). With a skewed or tiny team, quote the actual rank instead.
**Formula in plain words:** z-score = (candidate score minus average) divided by standard deviation. Symbols: z = (x - mean) / SD = (78 - 70) / 8 = 1.
**Worked example:** z = 1.0, so the candidate is in about the top 16% of this team.
**Excel / Python:**
```python
from scipy import stats

candidate_score = 78
team_average = 70
team_std_dev = 8

# Z-score = how many standard deviations above (or below) the average
z_score = (candidate_score - team_average) / team_std_dev
print("z-score:", z_score)

# Share of people expected to score below this candidate (assumes a bell-shaped spread)
share_below = stats.norm.cdf(z_score)
print("Share scoring lower:", round(share_below * 100, 1), "%")
```
Output: `z-score: 1.0` and `Share scoring lower: 84.1 %`. In plain words: one standard deviation above average is roughly the 84th percentile.
Excel (cells: B1 = 78, B2 = 70, B3 = 8): `=(B1-B2)/B3` returns 1, and `=NORM.S.DIST((B1-B2)/B3,TRUE)` returns 0.841 (Excel 2010+; not run in Excel here).
**Likely follow-ups:** 1) *What if the test scores are not bell-shaped?* Use percentile rank from the actual data. 2) *Is 78 "good" for the job?* A score is relative to the team; also compare with a pass mark or what high performers scored.
**Common mistakes:** Saying "8 points above, so 8% better"; using the 84% figure for skewed data; forgetting the group is small.

### Q18 ⭐⭐ 🟢 How would you sanity-check a number in a report before sending it to a manager?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Your habit of verifying before sending; do you catch errors before the manager does?
**Say this in the interview:** "I ask four things: does it match an independent source or total, is it the right order of magnitude, are there duplicates, blanks or odd values, and is the definition and time period what the manager thinks it is. I rebuild the number a second way if it matters."
**Explain simply:**
- **Reconcile:** do the parts add up to the total, and does it match last month's report or finance/HR system?
- **Reasonableness:** is it plausible? Attrition of 180% or an average age of 7 is a red flag.
- **Data quality:** duplicates, blanks, text stored as numbers, outliers, wrong date range.
- **Definition:** attrition = leavers divided by average headcount or opening headcount? Say which.
- **Peer check:** show it to a colleague or explain it aloud.
**Worked example:** A report says attrition 18.2% (2 leavers out of 11 rows). The data had one employee listed twice, so the true figure is 2 out of 10 = 20%.
**Excel / Python:**
```python
import pandas as pd

# Small made-up headcount table for one month
employees = pd.DataFrame({
    "employee_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10],
    "department": ["Sales"] * 5 + ["Support"] * 6,
    "left_this_month": [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    "salary": [30000, 42000, 38000, 41000, 36000, 29000, 33000, 31000, 400000, 28000, 28000],
})
# The number in the report was calculated on all 11 rows, duplicate included
reported_attrition_rate = round(2 / 11 * 100, 1)

# Check 1: duplicate employee IDs
duplicate_rows = employees["employee_id"].duplicated().sum()
print("Duplicate IDs:", duplicate_rows)

# Check 2: rebuild the rate from raw data, without duplicates
unique_employees = employees.drop_duplicates(subset="employee_id")
rebuilt_rate = unique_employees["left_this_month"].mean() * 100
print("Rebuilt attrition rate:", rebuilt_rate, "% vs reported", reported_attrition_rate, "%")

# Check 3: department rows must add up to the total
rows_by_department = unique_employees.groupby("department").size()
print("Department rows add up to", rows_by_department.sum(), "of", len(unique_employees))

# Check 4: look for impossible or extreme values
print("Highest salary:", unique_employees["salary"].max(), "| median salary:", unique_employees["salary"].median())
```
Output: `Duplicate IDs: 1`, rebuilt `20.0 %` vs reported `18.2 %`, departments add to 10 of 10, highest salary 400000 vs median 34500. In plain words: the duplicate shifted the rate, and the 400000 salary needs a look (typo or a genuine senior person?).
**Likely follow-ups:** 1) *What if you cannot verify it?* Send it with the caveat stated. 2) *What is a quick magnitude check?* Compare with last period and the industry range.
**Common mistakes:** Trusting a pivot table without checking the source rows; not stating the definition; only checking totals, not individual odd values.

### Q19 ⭐⭐ 🟡 Sales dipped on one day. How do you decide whether to raise an alarm or treat it as normal variation?
**Asked at:** commonly asked (no company-specific report found); the "KPI dropped, investigate" shape appears widely in analyst scenario lists.
**What the interviewer is checking:** Whether you know normal day-to-day noise exists and can measure it.
**Say this in the interview:** "I first check how much sales normally bounce around. I take the recent average and standard deviation, and only call it unusual if the dip falls far outside, say beyond three standard deviations, or if low days keep repeating. I also check for known causes like a holiday or a data feed problem."
**Explain simply:**
- Every metric wobbles. A single bad day is only a signal if it is bigger than the usual wobble.
- **Control limits** = average plus or minus 3 standard deviations; points outside are rare by luck alone (about 3 in 1,000 for bell-shaped data).
- Compare like with like: this Monday against recent Mondays, not against Sunday.
- Check the boring causes first: public holiday, outage, missing data load, one big customer.
- A run of several low days in a row matters even if none is extreme.
**Worked example:** Last 30 days averaged about 489 with spread about 32, so the alarm lines are about 393 and 586. A 450 day (z = -1.22) is normal; a 360 day (z = -4.01) is an alarm.
**Excel / Python:**
```python
import numpy as np

# 30 normal days of sales (made-up, seeded so the result repeats)
random_generator = np.random.default_rng(10)
daily_sales = random_generator.normal(loc=500, scale=40, size=30).round()

normal_average = daily_sales.mean()
normal_spread = daily_sales.std(ddof=1)

# Alarm lines: average minus/plus 3 standard deviations
lower_alarm_line = normal_average - 3 * normal_spread
upper_alarm_line = normal_average + 3 * normal_spread
print("Average:", round(normal_average, 1), "| spread:", round(normal_spread, 1))
print("Alarm lines:", round(lower_alarm_line, 1), "to", round(upper_alarm_line, 1))

# Check two dip days against the lines
for dip_day_sales in [450, 360]:
    z_score = (dip_day_sales - normal_average) / normal_spread
    is_alarm = dip_day_sales < lower_alarm_line
    print("Sales", dip_day_sales, "-> z =", round(z_score, 2), "-> alarm:", is_alarm)
```
Output: alarm lines 392.6 to 585.8; 450 is not an alarm, 360 is. Excel: with daily sales in B2:B31, lower line `=AVERAGE(B2:B31)-3*STDEV.S(B2:B31)` (Excel 2010+; not run in Excel here).
**Likely follow-ups:** 1) *What if the data have a weekly pattern?* Compare against the same weekday. 2) *Too many false alarms?* Widen the limits or require two low days in a row.
**Common mistakes:** Reacting to a single day; ignoring seasonality; using limits built from data that already include the dip.

### Q20 ⭐⭐ 🟡 You run 20 different comparisons on the same data and one shows p < 0.05. Should you report it?
**Asked at:** commonly asked; multiple comparisons appears as a standard "statistical trap" in prep articles (KDnuggets, snippet only).
**What the interviewer is checking:** Awareness of the multiple-comparisons problem, and honesty in reporting.
**Say this in the interview:** "Not as a finding on its own. With 20 tests, a p below 0.05 by pure luck is more likely than not. I would report all 20 tests, adjust for multiple testing, and treat the one hit as a hypothesis to confirm on fresh data."
**Explain simply:**
- **p-value** below 0.05 means: if there were truly no difference, results this extreme would happen less than 5% of the time.
- Run 20 tests with no real effects and about one will still pass, so the chance of at least one false alarm is about 64%.
- **Bonferroni correction:** divide 0.05 by the number of tests (0.0025 each), which is strict but simple.
- Better still: decide the comparisons before looking, and confirm on new data.
**Formula in plain words:** Chance of at least one false alarm = 1 minus (0.95 multiplied by itself 20 times). Symbols: 1 - (1 - 0.05)^20 = 0.642.
**Worked example:** You compare attrition across 20 departments against the company average. One department shows p = 0.04. Alone, that is weak evidence; against a 0.0025 bar, it fails.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

number_of_tests = 20
alpha = 0.05

# Chance of at least one false alarm when nothing is really going on
chance_of_false_alarm = 1 - (1 - alpha) ** number_of_tests
print("Chance of at least one p<0.05 by luck:", round(chance_of_false_alarm * 100, 1), "%")

# Bonferroni: stricter bar for each single test
strict_bar = alpha / number_of_tests
print("Bonferroni bar per test:", strict_bar)

# Simulate 2,000 "studies", each running 20 tests where the truth is "no difference"
random_generator = np.random.default_rng(1)
studies_with_false_alarm = 0
for study in range(2000):
    smallest_p_value = 1.0
    for test in range(number_of_tests):
        group_a = random_generator.normal(50, 10, 30)
        group_b = random_generator.normal(50, 10, 30)
        p_value = stats.ttest_ind(group_a, group_b).pvalue
        smallest_p_value = min(smallest_p_value, p_value)
    if smallest_p_value < alpha:
        studies_with_false_alarm += 1
print("Simulated share of studies with a false alarm:", studies_with_false_alarm / 2000 * 100, "%")
```
Output: 64.2% by formula, 0.0025 bar, 62.7% in simulation. In plain words: when nothing is going on, about 6 in 10 such studies still find something "significant".
**Likely follow-ups:** 1) *Is Bonferroni too strict?* It can be; Benjamini-Hochberg (false discovery rate) is a gentler alternative. 2) *Is one pre-planned test fine?* Yes, that is the clean way.
**Common mistakes:** Reporting only the "winning" test (p-hacking); treating p = 0.049 as proof.

### Q21 ⭐⭐ 🟡 A model flags attrition risk with 95% accuracy, but only 3% of employees actually leave. Is 95% good?
**Asked at:** commonly asked; class imbalance is listed among frequent applied-stats scenarios in the sources, no company-specific report found.
**What the interviewer is checking:** Do you know accuracy can mislead when one outcome is rare?
**Say this in the interview:** "Not necessarily. If only 3% leave, a model that predicts 'nobody leaves' is already 97% accurate and useless. I would look at recall, how many real leavers we catch, and precision, how many flagged people actually leave."
**Explain simply:**
- **Accuracy** = share of all predictions that are right. Rare events let it hide failure.
- **Recall** = of the real leavers, what share did we catch?
- **Precision** = of the people flagged, what share really leave?
- The right balance depends on cost: a wasted retention chat is cheap, a missed key resignation is expensive.
**Formula in plain words:** Recall = leavers caught / all real leavers. Precision = leavers caught / everyone flagged.
**Worked example:** 1,000 employees, 30 leave. A model with 6 leavers caught, 24 missed, 26 stayers wrongly flagged and 944 correctly cleared has 95% accuracy but recall of only 20% and precision of about 19%.
**Excel / Python:**
```python
# Confusion table for 1,000 employees, 30 of whom truly leave (3%)
true_leavers_caught = 6
true_leavers_missed = 24
stayers_wrongly_flagged = 26
stayers_correctly_cleared = 944

total_employees = true_leavers_caught + true_leavers_missed + stayers_wrongly_flagged + stayers_correctly_cleared
accuracy = (true_leavers_caught + stayers_correctly_cleared) / total_employees
print("Accuracy:", accuracy)

# A "model" that predicts nobody leaves
total_stayers = stayers_wrongly_flagged + stayers_correctly_cleared
do_nothing_accuracy = total_stayers / total_employees
print("Predict-nobody-leaves accuracy:", do_nothing_accuracy)

# Recall: of the 30 real leavers, how many did we catch?
recall = true_leavers_caught / (true_leavers_caught + true_leavers_missed)
print("Recall:", recall)

# Precision: of the 32 flagged people, how many really leave?
precision = true_leavers_caught / (true_leavers_caught + stayers_wrongly_flagged)
print("Precision:", round(precision, 3))
```
Output: accuracy 0.95, do-nothing accuracy 0.97, recall 0.2, precision 0.188. In plain words: the "95% accurate" model is worse than doing nothing on accuracy and catches only 1 in 5 leavers. (This confusion table is an illustrative assumption; the question gives only 95% and 3%.)
**Likely follow-ups:** 1) *What metric would you use?* Recall and precision, or F1 or area under the curve. 2) *How to improve?* Rebalance data, adjust the flagging threshold.
**Common mistakes:** Quoting accuracy alone; not comparing with the do-nothing baseline.

### Q22 ⭐⭐ 🟡 A test for a rare issue is 99% accurate and 1 in 1,000 items is faulty. A flagged item is faulty with what probability, and how would you explain the result to a manager?
**Asked at:** commonly asked; Bayes-style rare-test questions appear in the sources' list of frequent applied stats, no company-specific report found.
**What the interviewer is checking:** Base-rate thinking (Bayes' rule) and plain explanation.
**Say this in the interview:** "About 9%, not 99%. The wording is ambiguous, so I assume the test catches 99% of faulty items and wrongly flags 1% of good ones. Faults are so rare that the false alarms from the many good items outnumber the true catches by about 10 to 1."
**Explain simply:**
- "99% accurate" can mean different things; I state my assumption: sensitivity 99% and false-alarm rate 1%.
- Imagine 100,000 items: 100 are faulty, 99,900 are good.
- The test flags 99 of the faulty ones and 999 of the good ones (1% of 99,900).
- So of about 1,098 flagged items, only 99 are truly faulty.
- Tell the manager: a flag means "worth a second look", not "definitely faulty".
**Formula in plain words:** P(faulty if flagged) = true flags / (true flags + false flags). Symbols: 99 / (99 + 999).
**Worked example:** As above: 99 / 1,098 = 9.02%.
**Excel / Python:**
```python
items_checked = 100000
faulty_rate = 1 / 1000
detection_rate = 0.99          # faulty items correctly flagged
false_alarm_rate = 0.01        # good items wrongly flagged

faulty_items = items_checked * faulty_rate
good_items = items_checked - faulty_items

# Count flagged items of each kind
faulty_and_flagged = faulty_items * detection_rate
good_but_flagged = good_items * false_alarm_rate
print("Faulty and flagged:", faulty_and_flagged)
print("Good but flagged:", good_but_flagged)

# Of everything flagged, what share is truly faulty?
probability_faulty_if_flagged = faulty_and_flagged / (faulty_and_flagged + good_but_flagged)
print("P(faulty | flagged):", round(probability_faulty_if_flagged * 100, 2), "%")
```
Output: 99.0 and 999.0 flagged, giving 9.02%. In plain words: about 1 in 11 flagged items is truly faulty.
**Likely follow-ups:** 1) *What if the base rate were 10%?* The probability rises to about 92%. 2) *How would you improve it?* A second independent test on flagged items only.
**Common mistakes:** Answering 99%; forgetting the base rate; not stating the assumption about what "99% accurate" means.

### Q23 ⭐⭐ 🟡 Customers who use the mobile app spend more than those who do not. Does that mean pushing everyone to the app will raise spending?
**Asked at:** commonly asked (no company-specific report found); correlation vs causation is a core scenario in the sources.
**What the interviewer is checking:** Spotting self-selection and confounding.
**Say this in the interview:** "Not necessarily. People who choose the app may already be more engaged or wealthier, so they would spend more anyway. To know if the app causes more spending, I would compare similar customers, or better, run a randomised test of nudging some customers to the app."
**Explain simply:**
- **Correlation** = two things move together. **Causation** = one makes the other happen.
- **Confounder** = a hidden factor that drives both, for example income or loyalty.
- **Self-selection:** customers chose the app themselves, so the groups were never comparable.
- Fix: match on similar customers, or run an **A/B test** with random assignment.
**Worked example:** In a made-up simulation, app users spend 2,499 vs 1,515 for non-users, but the app has zero effect; income drives both. Within a narrow income band the gap vanishes (2,016 vs 1,996).
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(5)
customers = 10000

# Richer, younger customers are more likely to install the app
income_level = random_generator.normal(0, 1, customers)
chance_of_using_app = 1 / (1 + np.exp(-2 * income_level))
uses_app = random_generator.random(customers) < chance_of_using_app

# Spending depends on income only; the app adds NOTHING in this made-up world
monthly_spend = 2000 + 800 * income_level + random_generator.normal(0, 300, customers)

app_users_average = monthly_spend[uses_app].mean()
non_users_average = monthly_spend[~uses_app].mean()
print("App users spend:", round(app_users_average), "| non-users:", round(non_users_average))

# Compare like with like: only customers in a narrow income band
similar_income = (income_level > -0.1) & (income_level < 0.1)
app_users_in_band = monthly_spend[similar_income & uses_app].mean()
non_users_in_band = monthly_spend[similar_income & ~uses_app].mean()
print("Same income band, app users:", round(app_users_in_band), "| non-users:", round(non_users_in_band))
```
Output: `2499` vs `1515`, then `2016` vs `1996`. In plain words: the headline gap is created by who chooses the app, not by the app.
**Likely follow-ups:** 1) *Could the app still help?* Yes; the data cannot tell us without a fair comparison. 2) *Best evidence?* A randomised experiment.
**Common mistakes:** Recommending a rollout from raw averages; ignoring who self-selects.

### Q24 ⭐⭐ 🟡 The A/B test shows a 2% lift after 3 days and the product team wants to stop early. What do you advise?
**Asked at:** commonly asked; peeking and novelty effects appear as typical A/B traps in prep articles (KDnuggets, snippet only).
**What the interviewer is checking:** Understanding of peeking, planned sample size and weekly cycles.
**Say this in the interview:** "I would advise against stopping on a good-looking early result. We should fix the sample size or duration in advance, usually at least one or two full weeks to cover weekday and weekend behaviour, and not stop just because the number looks good. Checking every day and stopping at the first significant result inflates false positives."
**Explain simply:**
- **Peeking:** looking repeatedly and stopping when p < 0.05. Each look is another chance for luck to fool you.
- Early results are noisy because the sample is small.
- 3 days misses the weekly cycle and may capture a **novelty effect** (people click on anything new).
- Better: calculate the needed sample size first (Q25 style), run to completion, or use a proper sequential method.
**Worked example:** Simulation of identical versions (no real lift), 14 days: checking once at the end gives about 5% false alarms; checking every day and stopping at the first p < 0.05 gives about 22%.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

random_generator = np.random.default_rng(7)
simulated_tests = 2000
days = 14
users_per_day_per_group = 500
true_conversion = 0.10        # both groups identical: there is NO real lift

stopped_early_wrongly = 0
significant_at_end = 0

for test in range(simulated_tests):
    conversions_a = random_generator.binomial(users_per_day_per_group, true_conversion, days).cumsum()
    conversions_b = random_generator.binomial(users_per_day_per_group, true_conversion, days).cumsum()
    users_so_far = users_per_day_per_group * np.arange(1, days + 1)

    found_significant_on_some_day = False
    for day_index in range(days):
        pooled = (conversions_a[day_index] + conversions_b[day_index]) / (2 * users_so_far[day_index])
        standard_error = np.sqrt(pooled * (1 - pooled) * 2 / users_so_far[day_index])
        z_value = (conversions_b[day_index] - conversions_a[day_index]) / users_so_far[day_index] / standard_error
        p_value = 2 * (1 - stats.norm.cdf(abs(z_value)))
        if p_value < 0.05:
            found_significant_on_some_day = True
            if day_index == days - 1:
                significant_at_end += 1
    if found_significant_on_some_day:
        stopped_early_wrongly += 1

print("False alarms if you check once at day 14:", significant_at_end / simulated_tests * 100, "%")
print("False alarms if you check every day:", stopped_early_wrongly / simulated_tests * 100, "%")
```
Output: 5.25% vs 22.25%. In plain words: daily peeking multiplies the false-positive rate by more than four.
**Likely follow-ups:** 1) *Can we ever stop early?* Yes, with a pre-planned sequential design or for clear harm. 2) *What about 2% lift, relative or absolute?* Always ask which.
**Common mistakes:** Stopping at the first significant day; ignoring the weekly cycle; not defining the sample size beforehand.

### Q25 ⭐⭐ 🟡 How would you decide how many people to survey to estimate employee satisfaction within plus or minus 3 points?
**Asked at:** commonly asked (no company-specific report found); sample-size questions are listed as frequent applied stats.
**What the interviewer is checking:** Whether you can size a survey, not just guess.
**Say this in the interview:** "For a proportion, I use n = z squared times p times (1 - p) divided by the margin of error squared. With 95% confidence, plus or minus 3 points and the cautious p of 0.5, that is about 1,068 people. For a company of 5,000 I adjust down to about 880, and then invite more to allow for non-response."
**Explain simply:**
- **Margin of error** = how far the survey result may sit from the truth (here, 3 points).
- **95% confidence** = z of 1.96.
- p = 0.5 is the worst case and gives the biggest (safest) sample if we do not know the true satisfaction rate.
- A small population allows a **finite population correction**, so you need fewer people.
- Then divide by the expected response rate. A random sample matters more than a big one.
**Formula in plain words:** Sample size = (1.96 squared x 0.5 x 0.5) / (0.03 squared). Adjusted = n / (1 + (n - 1) / population).
**Worked example:** 1,067.1, rounded up to 1,068, becomes 880 for 5,000 staff; with 60% response (assumed), send 1,467 invitations.
**Excel / Python:**
```python
import math

z_value = 1.96            # for 95% confidence
margin_of_error = 0.03    # plus or minus 3 points
assumed_share = 0.5       # worst case: gives the biggest sample size
population = 5000

# Sample size for a very large population
sample_size_large = (z_value ** 2) * assumed_share * (1 - assumed_share) / (margin_of_error ** 2)
print("Sample size (large population):", round(sample_size_large, 1), "->", math.ceil(sample_size_large))

# Shrink it because the company has only 5,000 people
sample_size_adjusted = sample_size_large / (1 + (sample_size_large - 1) / population)
print("Adjusted for 5,000 employees:", round(sample_size_adjusted, 1), "->", math.ceil(sample_size_adjusted))

# Allow for only 60% replying
needed_invitations = math.ceil(sample_size_adjusted) / 0.60
print("Invitations to send at 60% response:", math.ceil(needed_invitations))
```
Output: 1068, 880, 1467. Excel: `=1.96^2*0.5*0.5/0.03^2` returns 1067.1 (not run in Excel here).
**Likely follow-ups:** 1) *Why is 0.5 used?* It maximises p(1-p), so it is the safe choice. 2) *Does non-response matter?* Yes, bias from who replies is worse than a small sample.
**Common mistakes:** Using a percentage of the population (like 10%); forgetting non-response; assuming a bigger sample fixes a biased sample.

### Q26 ⭐⭐ 🟡 Two departments have attrition of 10% (of 20 people) and 12% (of 500 people). Which is a more reliable number and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Sample size and uncertainty intuition.
**Say this in the interview:** "The 12% from 500 people is more reliable. 10% of 20 is just 2 leavers, so one resignation more or less moves it by 5 points. A confidence interval makes this visible: about 1% to 32% for the small one against 9% to 15% for the large one."
**Explain simply:**
- More people means a more stable percentage; small teams swing wildly.
- A **confidence interval** is a range of plausible true values given the data.
- So we cannot say the small department is "better" at retention; the data cannot separate 10% from 12%.
- For small teams, report counts (2 of 20) next to the percentage, or pool several years.
**Worked example:** Small: 2 of 20 gives 10%, range 1.2% to 31.7%. Large: 60 of 500 gives 12%, range 9.3% to 15.2%.
**Excel / Python:**
```python
from scipy import stats

# (leavers, headcount) for each department
departments = {"Small dept": (2, 20), "Large dept": (60, 500)}

for name, (leavers, headcount) in departments.items():
    # Exact (Clopper-Pearson) 95% interval for a percentage
    interval = stats.binomtest(leavers, headcount).proportion_ci(confidence_level=0.95, method="exact")
    print(name, "rate:", leavers / headcount * 100, "% | 95% range:",
          round(interval.low * 100, 1), "% to", round(interval.high * 100, 1), "%")
```
Output: Small dept 10.0% (1.2% to 31.7%); Large dept 12.0% (9.3% to 15.2%). In plain words: the small department's true rate could be almost anything from 1% to 32%.
**Likely follow-ups:** 1) *Is 12% truly higher than 10%?* No evidence of that. 2) *Could a department of 20 ever be judged?* Use a longer period or counts.
**Common mistakes:** Ranking departments by raw percentage; ignoring headcount.

### Q27 ⭐⭐ 🟡 Average rating of Product A is 4.8 from 5 reviews and Product B is 4.5 from 500 reviews. Which is better?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Weighing the average against the number of reviews behind it.
**Say this in the interview:** "I cannot say A is better. Five reviews is too few to trust, so its true rating could be much lower. B's 4.5 from 500 reviews is well established. I would shrink A's rating towards the overall average, which puts it below B, and collect more reviews."
**Explain simply:**
- A rating from few reviews has a wide margin of error; from many, a narrow one.
- Assuming reviews vary by about 0.6 stars (my assumption, not given), A's plausible range is about 4.3 to 5.3 (the top cannot exceed 5), B's is 4.45 to 4.55.
- **Shrinkage (Bayesian average)** pulls ratings with few reviews towards the store average, say 4.0 with 20 pseudo-reviews (assumed). A becomes 4.16; B stays 4.48.
- Also check for fake or early-adopter reviews.
**Formula in plain words:** Adjusted rating = (rating x reviews + store average x extra reviews) / (reviews + extra reviews).
**Excel / Python:**
```python
# Assumptions: ratings vary with a standard deviation of about 0.6 (made up for illustration)
import math

assumed_rating_spread = 0.6
products = {"A": (4.8, 5), "B": (4.5, 500)}

for name, (average_rating, review_count) in products.items():
    standard_error = assumed_rating_spread / math.sqrt(review_count)
    lower = average_rating - 1.96 * standard_error
    upper = average_rating + 1.96 * standard_error
    print("Product", name, "rating range:", round(lower, 2), "to", round(upper, 2))

# Pull each rating towards the overall store average (4.0) as if every product had 20 extra "average" reviews
store_average = 4.0
extra_reviews = 20
for name, (average_rating, review_count) in products.items():
    adjusted = (average_rating * review_count + store_average * extra_reviews) / (review_count + extra_reviews)
    print("Product", name, "adjusted rating:", round(adjusted, 2))
```
Output: A 4.27 to 5.33, B 4.45 to 4.55; adjusted A 4.16, B 4.48. In plain words: A's range is wide and overlaps B, and after shrinkage B wins.
**Likely follow-ups:** 1) *How many reviews are enough?* Depends on spread; dozens at least. 2) *Why not just pick the highest?* It rewards luck.
**Common mistakes:** Picking the higher average; forgetting the review count.

### Q28 ⭐⭐ 🟡 A correlation of 0.8 between training hours and performance is found. What additional questions would you ask before concluding anything?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Critical thinking about correlation.
**Say this in the interview:** "0.8 is strong, but I would ask: who got the training and why, does a third factor such as experience drive both, which way does the cause run, how many people and any outliers, and is it a straight-line pattern. Only a controlled comparison tells me whether training causes better performance."
**Explain simply:**
- **Correlation (r)** runs from -1 to +1 and measures how closely two things move together in a straight line. r squared (0.64 for r = 0.8) is the share of ups and downs they share.
- Questions: **Confounder** (experience, grade, manager)? **Reverse causation** (strong performers get picked for training)? **Selection** (volunteers vs assigned)? **Sample size and outliers**? **Time order** (training before the performance rating)?
- Good evidence: before and after, with a comparison group, or random assignment.
**Worked example:** In a made-up simulation, experience drives both training and performance; the raw correlation is 0.81 (r squared 0.66), but after removing the effect of experience from both, it drops to 0.04.
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(3)
employees = 300

# Senior people get more training AND score higher; training itself does nothing here
years_of_experience = random_generator.uniform(0, 15, employees)
training_hours = 5 + 2 * years_of_experience + random_generator.normal(0, 4, employees)
performance_score = 50 + 2 * years_of_experience + random_generator.normal(0, 4, employees)

correlation = np.corrcoef(training_hours, performance_score)[0, 1]
print("Correlation training vs performance:", round(correlation, 2))
print("Share of ups and downs 'explained' (r squared):", round(correlation ** 2, 2))

# Remove experience's effect from both columns, then correlate what is left
training_left_over = training_hours - np.polyval(np.polyfit(years_of_experience, training_hours, 1), years_of_experience)
performance_left_over = performance_score - np.polyval(np.polyfit(years_of_experience, performance_score, 1), years_of_experience)
adjusted_correlation = np.corrcoef(training_left_over, performance_left_over)[0, 1]
print("Correlation after allowing for experience:", round(adjusted_correlation, 2))
```
Output: 0.81, 0.66, then 0.04. In plain words: the strong link was mostly experience in disguise. (In Excel, `=CORREL(A2:A301,B2:B301)` gives r.)
**Likely follow-ups:** 1) *Does r = 0.8 prove causation?* No. 2) *What if the relationship is curved?* Plot it; r only measures straight-line links.
**Common mistakes:** Saying "training causes performance"; not plotting the data.

### Q29 ⭐⭐ 🟡 Your team's average response time improved from 10 to 8 minutes, but customers still complain. What might you check in the data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Looking beyond the average to the tail, definitions and segments.
**Say this in the interview:** "An average can improve while the worst experiences stay bad. I would look at the distribution: median, 90th/95th percentile and share waiting beyond a service target, then break it down by channel, issue type, shift and customer. I would also check what 'response' measures, first reply or full resolution."
**Explain simply:**
- Averages hide a **long tail**: a few very slow tickets annoy customers a lot but barely move the mean.
- **Percentile** (95th) = the time that 95% of tickets beat; the slowest 5% take longer.
- Check the definition: first auto-reply counts as a "response"? Is resolution time measured?
- Check segments: one channel or shift may be much worse. Also reopened tickets, abandoned chats, and survey comments.
**Worked example:** Made-up 1,000 tickets (900 quick, 100 slow): average 8.5 minutes, median 5.2, 95th percentile 40.5, and 8.5% wait over 30 minutes.
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(2)

# 1,000 tickets: most are quick, but a few drag on (made-up)
quick_tickets = random_generator.normal(5, 1.5, 900).clip(1)
slow_tickets = random_generator.normal(40, 10, 100).clip(1)
response_minutes = np.concatenate([quick_tickets, slow_tickets])

print("Average:", round(response_minutes.mean(), 1), "minutes")
print("Median:", round(np.median(response_minutes), 1), "minutes")
print("95th percentile:", round(np.percentile(response_minutes, 95), 1), "minutes")
print("Share waiting over 30 minutes:", round((response_minutes > 30).mean() * 100, 1), "%")
```
Output: 8.5, 5.2, 40.5 and 8.5%. In plain words: the average looks fine while about 1 customer in 12 waits over half an hour. Excel: `=PERCENTILE.INC(B2:B1001,0.95)` (Excel 2010+; not run in Excel here).
**Likely follow-ups:** 1) *Could complaints be about something else?* Yes; resolution quality, not speed. 2) *What target would you set?* A percentile target, like 90% within 15 minutes.
**Common mistakes:** Trusting the mean alone; not checking how the metric is defined.

### Q30 ⭐⭐ 🟡 The sales data is right-skewed. Which summary statistics and chart would you show your manager, and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Choosing summaries that describe skewed data honestly.
**Say this in the interview:** "I would show the median and the spread by percentiles (25th, 75th, 90th), mention the mean only with context, and use a histogram, possibly with a log scale, or a box plot. A few very large sales pull the mean up, so the median describes the typical sale better."
**Explain simply:**
- **Right-skewed** = most values small, a long tail of a few very large ones (sales, salaries, delivery times).
- The **mean** gets dragged towards the tail; the **median** (middle value) does not.
- **Percentiles** show the tail: the 90th percentile is the value 90% of sales fall below.
- Chart: histogram shows the shape; box plot compares groups. Avoid a bare average bar chart.
- Keep the big sales in the story; they may matter most for revenue.
**Worked example:** Made-up 2,000 orders: mean 1,501, median 1,086, 25th to 75th percentile 650 to 1,891, 90th 3,153, 99th 6,549; only 34.6% of orders are above the mean.
**Excel / Python:**
```python
import numpy as np

random_generator = np.random.default_rng(4)
order_values = random_generator.lognormal(mean=7, sigma=0.8, size=2000).round()

print("Mean:", round(order_values.mean()))
print("Median:", round(np.median(order_values)))
print("25th, 75th percentile:", np.percentile(order_values, [25, 75]).round())
print("90th, 99th percentile:", np.percentile(order_values, [90, 99]).round())
print("Share of orders above the mean:", round((order_values > order_values.mean()).mean() * 100, 1), "%")
```
Output as listed above. In plain words: the mean sits above the median, and only about a third of orders exceed it.
**Likely follow-ups:** 1) *Why not delete the big orders?* They are real revenue. 2) *When is the mean still useful?* For totals and revenue forecasting.
**Common mistakes:** Reporting only the mean; truncating the chart; deleting genuine large values.

### Q31 ⭐⭐ 🟡 How would you check whether the gap in average pay between men and women in a company is statistically significant, and what else must you control for?
**Asked at:** commonly asked (no company-specific report found); HR-flavoured gap-fill.
**What the interviewer is checking:** Raw gap vs adjusted gap, and statistical vs practical significance.
**Say this in the interview:** "First I measure the raw gap and test it with a two-sample t-test, using the Welch version because the two groups may have different spreads. But a raw gap mixes in job level, experience and department, so I also run a regression that compares like with like, and report both gaps with their confidence intervals."
**Explain simply:**
- **Raw gap** = average men's pay minus average women's pay. **Adjusted gap** = difference after comparing people in the same grade, experience, role, location, tenure and so on.
- A **t-test** checks whether the raw gap could be luck; **regression** estimates the gap while holding other factors fixed.
- Statistically significant does not mean large, and not significant does not mean no gap (small samples).
- Caution: if women are held back from senior grades, controlling for grade can hide that issue, so report both views.
**Worked example:** Made-up company of 600. Raw gap about 7,544 a month (p = 4e-11), mostly because fewer women are in senior grades. After controlling for grade and experience the gap is about 901 lower for women (p = 0.009; range -1,579 to -223).
**Excel / Python:**
```python
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

random_generator = np.random.default_rng(8)
employees = 600

# Made-up company: women are less often in senior grades, but nearly the same pay within a grade
is_woman = random_generator.random(employees) < 0.45
chance_senior = np.where(is_woman, 0.25, 0.45)
is_senior = random_generator.random(employees) < chance_senior
years_experience = random_generator.uniform(1, 15, employees)
monthly_salary = (30000 + 25000 * is_senior + 1500 * years_experience
                  - 1000 * is_woman + random_generator.normal(0, 4000, employees))

pay_table = pd.DataFrame({
    "monthly_salary": monthly_salary,
    "gender": np.where(is_woman, "Woman", "Man"),
    "senior_grade": is_senior.astype(int),
    "years_experience": years_experience,
})

# Step 1: raw gap and Welch t-test
men_pay = pay_table.loc[pay_table["gender"] == "Man", "monthly_salary"]
women_pay = pay_table.loc[pay_table["gender"] == "Woman", "monthly_salary"]
print("Raw gap (men minus women):", round(men_pay.mean() - women_pay.mean()))
print("Welch t-test p-value:", stats.ttest_ind(men_pay, women_pay, equal_var=False).pvalue)

# Step 2: regression that compares like with like (same grade and experience)
model = smf.ols("monthly_salary ~ C(gender, Treatment('Man')) + senior_grade + years_experience", data=pay_table).fit()
gender_term = "C(gender, Treatment('Man'))[T.Woman]"
print("Adjusted gap for women:", round(model.params[gender_term]))
print("Adjusted p-value:", round(model.pvalues[gender_term], 3))
print("Adjusted 95% range:", model.conf_int().loc[gender_term].round().tolist())
```
Output: raw gap 7544, p about 4.2e-11; adjusted gap -901, p 0.009, range [-1579, -223]. In plain words: most of the raw gap is about grade mix; a smaller but still significant gap remains within grade.
**Likely follow-ups:** 1) *Which test if pay is heavily skewed?* Mann-Whitney or log of pay. 2) *Other controls?* Role, location, performance rating, tenure, education; and check for bias in those too.
**Common mistakes:** Stopping at the t-test; over-controlling (grade may itself be affected by bias); equating "not significant" with "no gap".

### Q32 ⭐⭐ 🟡 A survey was sent only to employees who are still with the company to ask why people leave. What is wrong with this design?
**Asked at:** commonly asked (no company-specific report found); survivorship bias is listed as a differentiator topic in the sources.
**What the interviewer is checking:** Spotting survivorship bias and who is missing from the sample.
**Say this in the interview:** "It is survivorship bias: we only hear from people who stayed, so we miss the people who actually left and their real reasons. Stayers may guess, or give a polite or different answer. I would survey or interview leavers (exit interviews, a follow-up some months later) and compare with stayers."
**Explain simply:**
- **Survivorship bias** = studying only those who "survived" a process and ignoring those removed by it.
- Stayers are not a random sample of everyone: they are the ones for whom things worked well enough.
- Their view on "why people leave" is second-hand opinion, not the leavers' experience.
- Better design: exit survey for leavers (anonymous, ideally via a third party), a later alumni follow-up, plus a stayers' "what keeps you" survey, and compare the two groups on the same questions.
- Also use hard data: tenure, pay vs market, manager change, promotion history for leavers and stayers.
**Worked example (illustrative numbers, not from data):** Suppose 100 left citing mostly manager issues (40%) and pay (35%), while 400 stayers, asked in a stayers-only survey, say pay (50%) and workload (30%) and rarely mention managers. Surveying only stayers would point the company at the wrong fix.
**Likely follow-ups:** 1) *Do leavers answer honestly?* Often more honestly after leaving; anonymity helps. 2) *Is the stayers' survey useless?* No, it answers a different question (what keeps people).
**Common mistakes:** Generalising from stayers to leavers; low-response exit surveys treated as the full story.

### Q33 ⭐⭐ 🟡 Marks of students from two coaching centres are given. Which test would you use to compare them, and what assumptions do you check?
**Asked at:** commonly asked (no company-specific report found); the sources file notes a candidate-reported "is the height difference between two classes significant" question (snippet only).
**What the interviewer is checking:** Do you pick the right test for two independent groups and know what must hold before trusting it?
**Say this in the interview:** "Two separate groups of students, so I would use a two-sample t-test, the Welch version. Before that I check the marks look roughly bell-shaped, there are no wild outliers, and the students are independent. If the data is badly skewed I use the Mann-Whitney test instead."
**Explain simply:**
- A **two-sample t-test** asks: is the gap between the two averages bigger than normal random noise would produce?
- **Welch** version does not assume both centres have equally spread marks, so it is the safe default.
- Assumptions: students in one centre do not influence the other (independence); marks are roughly normal, or the groups are large enough (about 30 or more each) that this matters less; no extreme outliers.
- **Mann-Whitney** compares the overall ranking of marks and needs no normality.
- If the same students were tested before and after, that is a paired test, not this one.
**Formula in plain words:** t = (average A minus average B) divided by the typical noise in that gap. Large t (far from 0) means the gap is unlikely to be chance.
**Worked example:** 12 students per centre. Centre A averages 71.42, Centre B 63.92. Welch t = 3.98 and p = 0.0007, so a gap this big would be very rare if the centres were truly equal.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Marks of 12 students from each coaching centre (made-up data)
centre_a_marks = np.array([62, 70, 75, 68, 80, 72, 66, 74, 71, 69, 77, 73])
centre_b_marks = np.array([58, 65, 60, 72, 63, 67, 59, 70, 61, 64, 66, 62])

# Check each group looks roughly normal (p above 0.05 means no strong sign of non-normality)
print("Shapiro A p =", round(stats.shapiro(centre_a_marks).pvalue, 3))
print("Shapiro B p =", round(stats.shapiro(centre_b_marks).pvalue, 3))

# Check whether the spread of marks is similar in both groups
print("Levene p =", round(stats.levene(centre_a_marks, centre_b_marks).pvalue, 3))

# Welch t-test: compares the two averages without assuming equal spread
t_result = stats.ttest_ind(centre_a_marks, centre_b_marks, equal_var=False)
print("Average A =", round(centre_a_marks.mean(), 2), " Average B =", round(centre_b_marks.mean(), 2))
print("Welch t =", round(t_result.statistic, 2), " p =", round(t_result.pvalue, 4))

# Backup test that does not need normality
u_result = stats.mannwhitneyu(centre_a_marks, centre_b_marks, alternative="two-sided")
print("Mann-Whitney p =", round(u_result.pvalue, 4))
```
```text
Shapiro A p = 1.0
Shapiro B p = 0.859
Levene p = 0.767
Average A = 71.42  Average B = 63.92
Welch t = 3.98  p = 0.0007
Mann-Whitney p = 0.002
```
Both centres pass the normality and equal-spread checks (p above 0.05), and both tests give a small p-value, so the gap of about 7.5 marks is real, not chance. In Excel: T.TEST(range_A, range_B, 2, 3) gives the two-sided Welch p-value (Excel 2010+; not run in Excel here).
**Likely follow-ups:** 1) *What if the data is skewed?* Use Mann-Whitney. 2) *Is p = 0.0007 proof that coaching quality differs?* No, it shows marks differ; students may have been different to begin with.
**Common mistakes:** Using a paired test on independent groups; skipping the plots; saying "p is small so the effect is big"; ignoring that the students were not randomly assigned to centres.

### Q34 ⭐⭐ 🟡 A manager says 'last month's best-performing salesperson will do well again.' Using statistics, how do you challenge or support that?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know regression to the mean: extreme results are partly luck and tend to fall back toward average?
**Say this in the interview:** "Not necessarily. A top month is part skill and part luck. The luck does not repeat, so the best performer will usually do somewhat worse next month. I would check how well one month predicts the next before agreeing."
**Explain simply:**
- Performance = skill + luck. The top person last month probably had good skill and good luck together.
- **Regression to the mean** is the tendency for extreme results to move closer to average next time, with no real change in the person.
- The test: take past months for everyone and see how strongly month 1 correlates with month 2. Weak correlation means mostly luck; strong correlation means real skill.
- Support the manager's claim only if the person was consistently top over many months.
**Worked example:** Simulation of 200 salespeople whose skill differs only a little compared with monthly luck. The month-1 top 10 averaged 119.0; the same people averaged 96.0 in month 2, below the company average of 97.4. None repeated in the top 10.
**Excel / Python:**
```python
import numpy as np

# Fixed seed so the simulation gives the same answer every run
random_generator = np.random.default_rng(7)
number_of_salespeople = 200

# Every salesperson has a true skill level; monthly sales = skill + luck
true_skill = random_generator.normal(100, 5, number_of_salespeople)
month_1_sales = true_skill + random_generator.normal(0, 10, number_of_salespeople)
month_2_sales = true_skill + random_generator.normal(0, 10, number_of_salespeople)

# Find the top 10 people in month 1
top_10_in_month_1 = np.argsort(month_1_sales)[-10:]

# Compare their month 1 and month 2 average sales
print("Top 10 average in month 1:", round(month_1_sales[top_10_in_month_1].mean(), 1))
print("Same people in month 2   :", round(month_2_sales[top_10_in_month_1].mean(), 1))
print("Everyone's average       :", round(month_2_sales.mean(), 1))

# How well does month 1 predict month 2 across all staff?
correlation = np.corrcoef(month_1_sales, month_2_sales)[0, 1]
print("Month 1 vs month 2 correlation:", round(correlation, 2))

# How many of the month 1 top 10 are in the month 2 top 10?
top_10_in_month_2 = set(np.argsort(month_2_sales)[-10:])
repeat_winners = len(set(top_10_in_month_1) & top_10_in_month_2)
print("Repeat top-10 people:", repeat_winners, "of 10")
```
```text
Top 10 average in month 1: 119.0
Same people in month 2   : 96.0
Everyone's average       : 97.4
Month 1 vs month 2 correlation: 0.08
Repeat top-10 people: 0 of 10
```
Month 1 hardly predicts month 2 (correlation 0.08), so "last month's best" says almost nothing here. This is a made-up simulation, where skill is deliberately weak; real data may show more skill. In Excel: CORREL(month_1_range, month_2_range).
**Likely follow-ups:** 1) *How would you check with real data?* Correlate several months, or compare the top group's next-month average with the rest. 2) *What if the correlation is 0.7?* Then skill matters a lot and the manager is mostly right.
**Common mistakes:** Rewarding or blaming people for one extreme month; treating the drop as "they got complacent"; judging on a single period.

### Q35 ⭐⭐ 🟡 You need to check if a dice or coin used in a promotion game is fair. How would you test it with data?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you turn "is it fair?" into a hypothesis test with expected counts?
**Say this in the interview:** "I would roll or toss it many times, record the counts, and compare them with what a fair one would give. For a coin I use a binomial test; for a die a chi-square goodness-of-fit test."
**Explain simply:**
- Start with the **null hypothesis**: the die or coin is fair.
- A fair die gives each face about 1/6 of the rolls; a fair coin gives about half heads.
- The **chi-square test** measures how far the observed counts are from the expected counts. A small **p-value** (below 0.05) means "too far to be chance".
- Need enough rolls: a rule of thumb is an expected count of at least 5 per face; hundreds of rolls are better.
**Formula in plain words:** chi-square = add up, over all faces, (observed minus expected) squared divided by expected. Symbols: sum of (O - E)^2 / E.
**Worked example:** 600 die rolls: 88, 97, 120, 101, 95, 99. Chi-square = 5.8, p = 0.326, so no evidence of bias even though face 3 looks high. A coin with 62 heads in 100 tosses gives p = 0.021 (suggests bias). A die where face 3 appears 140 times gives p = 0.0014.
**Excel / Python:**
```python
from scipy import stats

# Die: 600 rolls, a fair die should give about 100 of each face
observed_counts = [88, 97, 120, 101, 95, 99]
expected_counts = [100, 100, 100, 100, 100, 100]
die_result = stats.chisquare(observed_counts, f_exp=expected_counts)
print("Die chi-square =", round(die_result.statistic, 2), " p =", round(die_result.pvalue, 3))

# Coin: 100 tosses gave 62 heads; a fair coin should give about 50
coin_result = stats.binomtest(62, n=100, p=0.5)
print("Coin p-value =", round(coin_result.pvalue, 4))

# A bigger, clearer example: 600 rolls where face 3 shows 140 times
biased_counts = [88, 97, 140, 91, 90, 94]
biased_result = stats.chisquare(biased_counts, f_exp=expected_counts)
print("Biased die p =", round(biased_result.pvalue, 4))
```
```text
Die chi-square = 5.8  p = 0.326
Coin p-value = 0.021
Biased die p = 0.0014
```
A small p-value (0.021, 0.0014) is evidence of unfairness; a large one (0.326) only means "no evidence", not proof of fairness. In Excel: CHISQ.TEST(observed_range, expected_range) (2010+; not run in Excel here).
**Likely follow-ups:** 1) *How many tosses?* Detecting a small bias needs hundreds (see Q46). 2) *Why not just look at the counts?* Random variation makes counts differ even for a fair die.
**Common mistakes:** Too few rolls; saying "p = 0.33 so the die is fair"; deciding the face to test after seeing the data.

### Q36 ⭐⭐ 🟡 Product return rate is 8% overall. How do you tell if the rate for one region at 11% is genuinely higher?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you use sample size, not only the gap, to judge a rate?
**Say this in the interview:** "I would test 11% against 8% using a proportion test, but the answer depends on how many orders are in that region. With 400 orders it is significant; with 100 it is not."
**Explain simply:**
- A **proportion test** asks: if the true rate were 8%, how often would a sample show 11% or more extreme by chance?
- Small samples swing a lot, large samples swing little. So the same 11% means different things for 100 or 400 orders.
- Also give a **confidence interval** (a plausible range for the true rate).
- Premise note: the question gives no region size; I assume 400 orders and say so. The 8% overall includes this region, so comparing region vs the rest is slightly stricter, but the idea is the same.
**Formula in plain words:** gap between region rate and 8%, divided by its typical random noise, which shrinks as orders grow.
**Worked example:** 44 returns out of 400 orders (11%). p = 0.0334 and a 95% range of 8.3% to 14.4%. With 11 of 100 orders the p-value is 0.266: not convincing.
**Excel / Python:**
```python
from scipy import stats
import numpy as np

# One region: 400 orders, 44 returned (11%); company-wide return rate is 8%
region_orders = 400
region_returns = 44
company_return_rate = 0.08

# Exact test: is 44 of 400 unusual if the true rate were 8%?
test_result = stats.binomtest(region_returns, n=region_orders, p=company_return_rate)
print("Region rate =", region_returns / region_orders)
print("p-value =", round(test_result.pvalue, 4))

# 95% confidence interval for the region's own return rate
interval = test_result.proportion_ci(confidence_level=0.95, method="wilson")
print("95% interval:", round(interval.low, 3), "to", round(interval.high, 3))

# Same question if the region had only 100 orders and 11 returns
small_test = stats.binomtest(11, n=100, p=company_return_rate)
print("p-value with 100 orders =", round(small_test.pvalue, 3))
```
```text
Region rate = 0.11
p-value = 0.0334
95% interval: 0.083 to 0.144
p-value with 100 orders = 0.266
```
With 400 orders the 11% is probably higher than 8% (p below 0.05), but the range starts at 8.3%, so the true gap may be small. With 100 orders we cannot tell.
**Likely follow-ups:** 1) *Is "significant" the same as "important"?* No; ask whether 3 points matters for cost. 2) *How if you check all 20 regions?* Adjust for multiple comparisons (Q20).
**Common mistakes:** Ignoring sample size; comparing one region with the overall rate that already contains it without noting it; declaring cause (for example a bad courier) from a rate alone.

### Q37 ⭐⭐ 🟡 You are asked to present statistical findings to a leadership team with no analytics background. How do you structure the message?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you communicate findings to non-analysts without jargon and with a clear decision?
**Say this in the interview:** "I lead with the answer and the decision needed, then the one or two numbers that support it, a simple chart, how sure I am in plain words, and what could change the conclusion."
**Explain simply:**
- **Answer first:** one sentence, for example "Attrition rose from 12% to 14%, but this is within normal monthly variation, so I recommend watching, not acting yet."
- **Evidence:** two or three numbers and one simple chart (a bar or a line), not a table of tests.
- **Uncertainty in everyday words:** "we are fairly sure the true rate is between 11% and 17%", instead of "p = 0.03".
- **What it means and what to do next:** options with costs, plus the limits (small sample, missing data).
- Keep the technical details in an appendix and offer it if asked.
- Use an analogy: a 95% interval is like a weather forecast range, not a promise.
**Worked example:** Instead of "t(48) = 2.1, p = 0.04", say: "Trained employees scored 5 points higher on average. A gap this big would happen by luck only about 4 times in 100, so the training likely helped. The pilot was small, so I would confirm with a larger group."
**Likely follow-ups:** 1) *A leader asks "so is it true or not?"* Give a confidence level in words (high, medium, low) and the risk of being wrong. 2) *How long should it be?* One page or three slides.
**Common mistakes:** Starting with method; showing p-values and test names; hiding limits; giving a number with no range; no recommended action.

### Q38 ⭐⭐ 🔴 Your manager asks you to forecast next month's sales using only the last three months of data. What are the risks and how would you present the uncertainty?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that three points give a very uncertain forecast and can show the range honestly?
**Say this in the interview:** "Three months cannot show a trend or seasonality, so I would give a range, not a single number, state the assumptions, and recommend collecting more history or using last year's pattern."
**Explain simply:**
- **Risks:** cannot separate trend from random noise; cannot see seasonality (festival months, year-end); one odd month distorts everything; stats formulas rely on few data points.
- **Prediction range:** the range in which next month will probably fall. With only 3 points, the statistics widen the range a lot (a t multiplier of 4.3 instead of about 2).
- Present a base case, a low and a high case, and say what assumptions each rests on.
- Improve it: add last year's same months, use business knowledge (known orders, hiring plans), and update the forecast every month.
**Formula in plain words:** forecast = average of past months; range = forecast plus or minus (t multiplier times spread times a small extra factor for one new month). Symbols: mean +/- t * s * sqrt(1 + 1/n).
**Worked example:** Sales of 100, 108, 104 lakh give a forecast of 104 and a 95% range of 84.1 to 123.9. If the months had been 100, 120, 90 (same average), the range balloons to 27.4 to 179.2: almost useless.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Last three months of sales in lakh rupees (made-up)
last_three_months = np.array([100, 108, 104])

# Simple forecast: the average of the three months
forecast = last_three_months.mean()
spread = last_three_months.std(ddof=1)
print("Forecast =", round(forecast, 1), " Spread (std dev) =", round(spread, 2))

# 95% prediction range for ONE new month; with 3 points we must use t with 2 degrees of freedom
t_multiplier = stats.t.ppf(0.975, df=2)
margin = t_multiplier * spread * np.sqrt(1 + 1 / 3)
print("t multiplier =", round(t_multiplier, 3))
print("Range:", round(forecast - margin, 1), "to", round(forecast + margin, 1))

# Now suppose the 3 months were 100, 120, 90: same average, more spread
volatile_months = np.array([100, 120, 90])
volatile_spread = volatile_months.std(ddof=1)
volatile_margin = t_multiplier * volatile_spread * np.sqrt(1 + 1 / 3)
print("Volatile range:", round(volatile_months.mean() - volatile_margin, 1), "to", round(volatile_months.mean() + volatile_margin, 1))
```
```text
Forecast = 104.0  Spread (std dev) = 4.0
t multiplier = 4.303
Range: 84.1 to 123.9
Volatile range: 27.4 to 179.2
```
The same average of 104 can be reliable or nearly meaningless depending on the spread. In Excel: T.INV.2T(0.05, 2) returns 4.303 (2010+; not run in Excel here).
**Likely follow-ups:** 1) *What would you use instead?* Add history (12 to 24 months) and a seasonal method. 2) *What if the manager wants one number?* Give the base case and say the range next to it.
**Common mistakes:** Fitting a straight line to 3 points and extending it; showing one decimal-precise number; ignoring seasonality.

### Q39 ⭐⭐ 🔴 Overall, a hospital's treatment shows a lower success rate than a competitor, yet it does better for both mild and severe patients. Explain what is happening and what you would report.
**Asked at:** commonly asked (no company-specific report found); the sources file lists Simpson's paradox as a standard interview scenario (prep articles, snippet only).
**What the interviewer is checking:** Do you recognise **Simpson's paradox** and know which view to trust?
**Say this in the interview:** "This is Simpson's paradox. The hospital treats more severe patients, who have lower success for anyone, so the overall rate is dragged down. Compared like with like, the hospital does better in both groups, so I would report the results split by severity."
**Explain simply:**
- **Simpson's paradox**: a trend in the overall data reverses when you split into groups.
- Cause: the groups are not the same size at each hospital. Ours sees mostly severe patients (hard cases); the competitor sees mostly mild ones.
- The overall rate is a weighted mix, and the weights differ, so it is not a fair comparison.
- Which view is right depends on the cause. Here severity is a real factor that affects outcome and is not the hospital's choice, so the split view is the fair one.
**Formula in plain words:** overall rate = sum of (share of patients in each group times success rate of that group).
**Worked example:** Ours: mild 95/100 = 95%, severe 240/400 = 60%, overall 335/500 = 67%. Competitor: mild 360/400 = 90%, severe 50/100 = 50%, overall 410/500 = 82%. Ours wins both groups, loses overall.
**Excel / Python:**
```python
# (successes, patients) for each hospital and severity
our_hospital = {"mild": (95, 100), "severe": (240, 400)}
competitor = {"mild": (360, 400), "severe": (50, 100)}

def show(name, groups):
    total_success = 0
    total_patients = 0
    for severity, (success, patients) in groups.items():
        print(name, severity, ":", success, "/", patients, "=", round(100 * success / patients, 1), "%")
        total_success += success
        total_patients += patients
    print(name, "overall:", total_success, "/", total_patients, "=", round(100 * total_success / total_patients, 1), "%")

show("Ours", our_hospital)
show("Competitor", competitor)
```
```text
Ours mild : 95 / 100 = 95.0 %
Ours severe : 240 / 400 = 60.0 %
Ours overall: 335 / 500 = 67.0 %
Competitor mild : 360 / 400 = 90.0 %
Competitor severe : 50 / 100 = 50.0 %
Competitor overall: 410 / 500 = 82.0 %
```
Our hospital has higher success in each group (95 vs 90, 60 vs 50), yet a lower total (67 vs 82) because 80% of our patients are severe versus 20% at the competitor. (These numbers are made up to show the effect.)
**Likely follow-ups:** 1) *Is the split always the right view?* No; think about causes. 2) *What would you report?* Both tables, the mix of patients, and a severity-adjusted rate.
**Common mistakes:** Quoting only the overall number; not checking group sizes; assuming splitting is always right.

### Q40 ⭐⭐ 🔴 An A/B test shows an overall lift, but when split by new vs returning users, the lift disappears in both groups. How could this occur?
**Asked at:** commonly asked (no company-specific report found); the sources file lists Simpson-style and mix-shift scenarios in A/B prep articles (snippet only).
**What the interviewer is checking:** Do you spot a mix difference between groups (a Simpson-type effect) and suspect a broken experiment?
**Say this in the interview:** "The overall lift can come entirely from the groups having a different mix. If the test group got more returning users, who convert more, the overall rate rises even though no group improved. That points to a randomisation problem, so I would check the split first."
**Explain simply:**
- Returning users convert far better than new users (20% vs 5% in the example).
- If the test group has 80% returning users and control only 20%, the test group's average is higher purely by mix.
- Within each type the rates are identical, so the variant did nothing.
- Proper randomisation should give a similar mix in both groups. A big difference signals a bug (for example, the variant was only shown to logged-in users).
- Action: fix assignment and rerun, or compare within segments.
**Worked example:** Control: 800 new users at 5%, 200 returning at 20%, overall 8%. Test: 200 new at 5%, 800 returning at 20%, overall 17%. Overall "lift" of 9 points, zero lift in each segment.
**Excel / Python:**
```python
# (conversions, users) in each group; test has far more returning users
control = {"new": (40, 800), "returning": (40, 200)}
test = {"new": (10, 200), "returning": (160, 800)}

for group_name, group in [("Control", control), ("Test", test)]:
    total_conversions = 0
    total_users = 0
    for user_type, (conversions, users) in group.items():
        print(group_name, user_type, ":", round(100 * conversions / users, 1), "% of", users, "users")
        total_conversions += conversions
        total_users += users
    print(group_name, "overall:", round(100 * total_conversions / total_users, 1), "%")
```
```text
Control new : 5.0 % of 800 users
Control returning : 20.0 % of 200 users
Control overall: 8.0 %
Test new : 5.0 % of 200 users
Test returning : 20.0 % of 800 users
Test overall: 17.0 %
```
The overall difference (8% vs 17%) is entirely because the test group contains four times as many returning users. (Made-up numbers.)
**Likely follow-ups:** 1) *How would you detect this early?* Check the user mix and group sizes before reading results (Q48). 2) *Could the opposite happen?* Yes, a lift inside segments but not overall.
**Common mistakes:** Celebrating the headline lift; not checking group composition.

### Q41 ⭐⭐ 🔴 Two variants of a landing page show 5.0% vs 5.5% conversion with 2,000 visitors each. Is the difference significant? Show a rough calculation.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you do a two-proportion z-test by hand and say the result in plain words?
**Say this in the interview:** "The gap is 0.5 points. The noise in that gap is about 0.7 points, so z is roughly 0.7, p is about 0.48. That is not significant; the data cannot tell the pages apart."
**Explain simply:**
- Conversion = visitors who did the thing divided by visitors.
- **Standard error** is the typical random wobble in the gap.
- **z-score** = gap divided by the wobble; above about 2 (p below 0.05) means likely real.
- Here the gap is smaller than the wobble. A real 0.5 point lift would need a much bigger sample (roughly 30,000+ per variant).
**Formula in plain words:** pooled rate = total conversions / total visitors; standard error = square root of pooled rate times (1 - pooled rate) times (1/visitors A + 1/visitors B); z = (rate B - rate A) / standard error.
**Worked example:** A: 100 of 2,000 (5.0%). B: 110 of 2,000 (5.5%). Pooled rate 5.25%, standard error 0.0071, z = 0.71, p = 0.478.
**Excel / Python:**
```python
import math
from scipy import stats

# Variant A: 5.0% of 2,000 visitors; Variant B: 5.5% of 2,000 visitors
visitors_each = 2000
conversions_a = 100
conversions_b = 110
rate_a = conversions_a / visitors_each
rate_b = conversions_b / visitors_each

# Pooled rate: conversion rate if both variants were really the same
pooled_rate = (conversions_a + conversions_b) / (2 * visitors_each)

# Standard error of the difference between two rates
standard_error = math.sqrt(pooled_rate * (1 - pooled_rate) * (1 / visitors_each + 1 / visitors_each))

# z-score = gap divided by its typical noise; two-sided p-value from the normal curve
z_score = (rate_b - rate_a) / standard_error
p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
print("Gap =", round(rate_b - rate_a, 4), " Standard error =", round(standard_error, 4))
print("z =", round(z_score, 2), " p =", round(p_value, 3))
```
```text
Gap = 0.005  Standard error = 0.0071
z = 0.71  p = 0.478
```
p = 0.478: if the pages were identical, a gap this large would show up almost half the time. In Excel: compute z with =(B-A)/SQRT(pooled*(1-pooled)*(2/2000)) and the p-value with =2*(1-NORM.S.DIST(ABS(z),TRUE)) (2010+; not run in Excel here).
**Likely follow-ups:** 1) *Does this mean B is not better?* No, it means we cannot tell. 2) *How much data would you need?* Compute sample size for a 0.5-point lift (Q56).
**Common mistakes:** Calling B the winner because 5.5 is bigger; saying "no difference" instead of "not enough evidence".

### Q42 ⭐ 🟢 Two dice are rolled. What is the probability that the sum is greater than 6?
**Asked at:** commonly asked (no company-specific report found); reported as a probability puzzle in Tiger Analytics candidate reports (snippet only).
**What the interviewer is checking:** Can you list the outcomes cleanly and count?
**Say this in the interview:** "Two dice have 36 equally likely outcomes. Sums of 7 or more can happen in 6 + 5 + 4 + 3 + 2 + 1 = 21 ways, so the answer is 21/36 = 7/12, about 58%."
**Explain simply:**
- List all pairs (first die, second die): 6 times 6 = 36.
- Count pairs by sum: sum 7 has 6 ways, 8 has 5, 9 has 4, 10 has 3, 11 has 2, 12 has 1.
- Shortcut: sums below 7 are 15 ways, so 1 - 15/36 = 21/36.
**Formula in plain words:** probability = favourable outcomes / total outcomes.
**Worked example:** 21 / 36 = 0.5833.
**Excel / Python:**
```python
# List all 36 pairs of dice results and count the ones with a sum above 6
favourable = 0
total = 0
for first_die in range(1, 7):
    for second_die in range(1, 7):
        total += 1
        if first_die + second_die > 6:
            favourable += 1
print(favourable, "out of", total, "=", round(favourable / total, 4))
```
```text
21 out of 36 = 0.5833
```
About 58% of rolls give a sum above 6.
**Likely follow-ups:** 1) *Sum equal to 7?* 6/36 = 1/6. 2) *Sum at least 7?* Same as this (greater than 6).
**Common mistakes:** Treating sums as equally likely (11 sums, so "1/11"), or listing (1,2) and (2,1) as the same outcome.

### Q43 ⭐ 🟢 What is the probability that a 31-day month has five Sundays?
**Asked at:** commonly asked (no company-specific report found); reported as a puzzle in Tiger Analytics candidate reports ("five Sundays in a 31-day month", snippet only).
**What the interviewer is checking:** Can you reason with weeks and leftover days?
**Say this in the interview:** "31 days is 4 full weeks plus 3 extra days. Those 3 extra days are consecutive. There are 5 Sundays only if Sunday is among them, which happens for 3 of the 7 possible starting weekdays, so 3/7."
**Explain simply:**
- 4 full weeks always give exactly 4 Sundays.
- The extra 3 days are the 29th, 30th and 31st, which fall on the same weekdays as the 1st, 2nd and 3rd.
- So there is a fifth Sunday only if the month starts on Friday, Saturday or Sunday.
- Assume each starting weekday is equally likely (a simplification).
**Formula in plain words:** probability = starting days that work / 7.
**Worked example:** Starts on Fri, Sat or Sun gives 5 Sundays: 3/7 = 42.9%.
**Excel / Python:**
```python
# 31 days = 4 full weeks + 3 extra days. Try each possible starting weekday.
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
months_with_five_sundays = 0
for start_index in range(7):
    sundays = 0
    for day_number in range(31):
        if weekdays[(start_index + day_number) % 7] == "Sun":
            sundays += 1
    print("Month starts on", weekdays[start_index], "->", sundays, "Sundays")
    if sundays == 5:
        months_with_five_sundays += 1
print("Probability =", months_with_five_sundays, "/ 7 =", round(months_with_five_sundays / 7, 4))
```
```text
Month starts on Mon -> 4 Sundays
Month starts on Tue -> 4 Sundays
Month starts on Wed -> 4 Sundays
Month starts on Thu -> 4 Sundays
Month starts on Fri -> 5 Sundays
Month starts on Sat -> 5 Sundays
Month starts on Sun -> 5 Sundays
Probability = 3 / 7 = 0.4286
```
Three of the seven starting days give five Sundays.
**Likely follow-ups:** 1) *30-day month?* Starts on Sat or Sun: 2/7. 2) *February in a normal year?* Never has a fifth Sunday.
**Common mistakes:** Answering 1/7 or 5/31.

### Q44 ⭐ 🟡 You have 100 employees, 60 in sales and 40 in support. If you pick 2 at random, what is the probability both are from support?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know picking without replacement changes the second probability?
**Say this in the interview:** "First pick is support with 40/100. With one support person gone, the second is 39/99. Multiply: 40/100 times 39/99 = 26/165, about 15.8%."
**Explain simply:**
- **Without replacement:** the first person is not put back, so the numbers change for the second pick.
- Multiply because both things must happen.
- Alternative count: ways to choose 2 from 40 support divided by ways to choose 2 from 100: 780 / 4950.
**Formula in plain words:** P(both) = P(first) times P(second given first).
**Worked example:** 40/100 times 39/99 = 0.1576.
**Excel / Python:**
```python
from fractions import Fraction
from itertools import combinations

# Step by step: first pick from support, then second pick from support
first_pick = Fraction(40, 100)
second_pick = Fraction(39, 99)
exact_answer = first_pick * second_pick
print("Exact:", exact_answer, "=", round(float(exact_answer), 4))

# Check by counting every possible pair of employees
employees = ["support"] * 40 + ["sales"] * 60
both_support = 0
all_pairs = 0
for first_person, second_person in combinations(range(100), 2):
    all_pairs += 1
    if employees[first_person] == "support" and employees[second_person] == "support":
        both_support += 1
print("Pairs:", both_support, "/", all_pairs, "=", round(both_support / all_pairs, 4))
```
```text
Exact: 26/165 = 0.1576
Pairs: 780 / 4950 = 0.1576
```
Both methods agree: about 15.8%. In Excel: =COMBIN(40,2)/COMBIN(100,2) (not run in Excel here).
**Likely follow-ups:** 1) *One from each team?* 2 times 40/100 times 60/99 = 48/165 (about 29.1%). 2) *With replacement?* 0.4 times 0.4 = 16%.
**Common mistakes:** Using 40/100 times 40/100.

### Q45 ⭐ 🟡 A call centre gets 6 calls per hour on average. What is the chance of getting no call in a given 10-minute window?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you scale a rate to a shorter window and use the Poisson (events happening randomly at a steady average rate) model?
**Say this in the interview:** "6 calls an hour is 1 call on average in 10 minutes. With a Poisson model the chance of zero calls is e to the power minus 1, about 36.8%."
**Explain simply:**
- **Poisson** counts how many random events occur in a fixed window when they happen at a steady average rate and independently.
- First convert the rate to the window: 6 per hour times 10/60 hour = 1.
- Zero calls has probability e^(-average).
- The model assumes calls are independent and the rate is steady; real call centres have peak hours, so check that.
**Formula in plain words:** chance of 0 events = e raised to the minus (average events in the window). Symbols: P(0) = e^(-lambda).
**Worked example:** lambda = 1, so P(0) = 0.3679.
**Excel / Python:**
```python
import math
from scipy import stats

# 6 calls per hour means 1 call per 10 minutes on average
calls_per_hour = 6
average_calls_in_window = calls_per_hour * (10 / 60)

# Poisson formula for zero events: e to the power minus the average
by_formula = math.exp(-average_calls_in_window)
by_scipy = stats.poisson.pmf(0, average_calls_in_window)
print("Average calls in 10 minutes:", average_calls_in_window)
print("P(no calls) by formula:", round(by_formula, 4))
print("P(no calls) by scipy  :", round(by_scipy, 4))
```
```text
Average calls in 10 minutes: 1.0
P(no calls) by formula: 0.3679
P(no calls) by scipy  : 0.3679
```
About 37% of 10-minute windows would have no call. In Excel: =POISSON.DIST(0, 1, FALSE) returns 0.3679 (2010+; not run in Excel here).
**Likely follow-ups:** 1) *At least one call?* 1 - 0.3679 = 63.2%. 2) *Gap between calls?* Exponential distribution.
**Common mistakes:** Using 6 as the average in a 10-minute window; answering 1/6.

### Q46 ⭐ 🟡 An interviewer gives you a coin that you suspect is biased and asks how you would prove it with the fewest tosses. What do you say?
**Asked at:** commonly asked (no company-specific report found); the sources file does not cover this exact puzzle.
**What the interviewer is checking:** Do you know you cannot "prove" bias with few tosses, and that the needed tosses depend on how biased it is?
**Say this in the interview:** "I cannot prove it, only gather evidence. If it is very biased, 10 heads in 10 tosses is already strong evidence (p about 0.002). For a mild bias, like 60% heads, I need about 200 tosses. So the fewest tosses depends on the bias I want to detect."
**Explain simply:**
- Set the null: the coin is fair. Count heads and ask how surprising that count is (binomial test).
- Strongly biased coins reveal themselves quickly; slightly biased ones need hundreds of tosses.
- Decide the number of tosses before starting (do not stop when it looks good, see Q24 peeking).
- Be honest: I can show evidence, not certainty; 8 heads in 10 (p = 0.109) is not enough.
**Formula in plain words:** tosses needed = ((z for 5% error times spread under fair + z for 80% power times spread under biased) divided by the size of the bias) squared.
**Worked example:** 60% coin needs about 194 tosses; 70% coin about 47.
**Excel / Python:**
```python
from scipy import stats
import math

# How surprising are different results from a fair coin?
for heads, tosses in [(10, 10), (8, 10), (60, 100), (65, 100)]:
    p_value = stats.binomtest(heads, n=tosses, p=0.5).pvalue
    print(heads, "heads in", tosses, "tosses -> p =", round(p_value, 4))

# Tosses needed to detect a coin that lands heads 60% of the time (5% significance, 80% power)
z_alpha = stats.norm.ppf(0.975)
z_power = stats.norm.ppf(0.80)
fair_rate = 0.5
biased_rate = 0.6
numerator = (z_alpha * math.sqrt(fair_rate * (1 - fair_rate)) + z_power * math.sqrt(biased_rate * (1 - biased_rate))) ** 2
tosses_needed = numerator / (biased_rate - fair_rate) ** 2
print("Tosses needed for a 60% coin:", math.ceil(tosses_needed))

# Same for a 70% coin
biased_rate = 0.7
numerator = (z_alpha * math.sqrt(0.25) + z_power * math.sqrt(biased_rate * (1 - biased_rate))) ** 2
print("Tosses needed for a 70% coin:", math.ceil(numerator / (biased_rate - 0.5) ** 2))
```
```text
10 heads in 10 tosses -> p = 0.002
8 heads in 10 tosses -> p = 0.1094
60 heads in 100 tosses -> p = 0.0569
65 heads in 100 tosses -> p = 0.0035
Tosses needed for a 60% coin: 194
Tosses needed for a 70% coin: 47
```
10 of 10 heads is convincing, 8 of 10 is not, and 60 of 100 is borderline (p = 0.057). Plan the number of tosses to the smallest bias you care about.
**Likely follow-ups:** 1) *Can you test with 3 tosses?* No; the best p is 0.25 (two-sided). 2) *Bayesian view?* Update belief about the head rate as you toss.
**Common mistakes:** Saying "toss it 5 times"; claiming proof; stopping when the p-value first dips below 0.05.

### Q47 ⭐ 🟡 Your A/B test ran for a week and shows lift on Monday to Wednesday but none later. What could explain it?
**Asked at:** commonly asked (no company-specific report found); the sources file lists novelty effects and peeking as standard A/B pitfalls (snippet only).
**What the interviewer is checking:** Do you think of novelty effect, day-of-week mix and peeking, not only "it failed"?
**Say this in the interview:** "A lift that fades looks like a novelty effect: users try the new thing and then get used to it. I would also check weekday vs weekend behaviour, whether the traffic mix changed, and whether we read the result early and chose the good days."
**Explain simply:**
- **Novelty effect:** curiosity boosts the early numbers, then it fades. Opposite is a **primacy/learning effect**.
- **Day-of-week mix:** weekday and weekend users differ, so run full weeks.
- **Traffic change:** a campaign or holiday midweek can change who arrives.
- **Cherry-picking:** looking at the best days after the fact inflates false wins.
- Action: judge the whole planned period (at least 1 to 2 full weeks), and look at the trend by day, then decide whether to extend or rerun.
**Worked example:** Made-up daily data (2,000 users per group per day, 100 control conversions daily). Test lift: Mon +30%, Tue +26%, Wed +22%, Thu +4%, Fri 0%, Sat -1%, Sun -2%. The week overall is +11.3% (p = 0.035), but the effect is fading to zero.
**Excel / Python:**
```python
from scipy import stats

# Daily results: (control conversions, control users, test conversions, test users)
daily_results = {
    "Mon": (100, 2000, 130, 2000),
    "Tue": (100, 2000, 126, 2000),
    "Wed": (100, 2000, 122, 2000),
    "Thu": (100, 2000, 104, 2000),
    "Fri": (100, 2000, 100, 2000),
    "Sat": (100, 2000, 99, 2000),
    "Sun": (100, 2000, 98, 2000),
}

total_control = 0
total_test = 0
for day, (control_conv, control_users, test_conv, test_users) in daily_results.items():
    lift = (test_conv / test_users) / (control_conv / control_users) - 1
    print(day, "lift =", round(100 * lift, 1), "%")
    total_control += control_conv
    total_test += test_conv

# Whole-week lift
print("Week lift =", round(100 * (total_test / total_control - 1), 1), "%")

# Chi-square test on the full-week 2x2 table
table = [[total_test, 14000 - total_test], [total_control, 14000 - total_control]]
print("Full-week p =", round(stats.chi2_contingency(table, correction=False).pvalue, 3))
```
```text
Mon lift = 30.0 %
Tue lift = 26.0 %
Wed lift = 22.0 %
Thu lift = 4.0 %
Fri lift = 0.0 %
Sat lift = -1.0 %
Sun lift = -2.0 %
Week lift = 11.3 %
Full-week p = 0.035
```
The week looks "significant" only because of the first three days; the trend suggests the effect has vanished. Extend the test to see whether the fade continues.
**Likely follow-ups:** 1) *What do you recommend?* Do not launch on the headline; run longer or hold back a group. 2) *How to separate weekday from novelty?* Compare new users only, who see it for the first time.
**Common mistakes:** Reporting only Mon to Wed; stopping the test the moment p < 0.05; ignoring the trend.

### Q48 ⭐ 🟡 The experiment's control group has 10,200 users and the test group has 9,400 users when you expected an equal split. Is that a problem?
**Asked at:** commonly asked (no company-specific report found); the sources file lists SRM (sample ratio mismatch) as a standard A/B scenario (snippet only).
**What the interviewer is checking:** Do you know **sample ratio mismatch (SRM)**: group sizes that differ from the plan signal a broken experiment?
**Say this in the interview:** "Yes, it is a problem. 10,200 vs 9,400 is a 52/48 split, and a chi-square test shows it is far too uneven to be chance (p about 0.00000001). I would not trust the results until I find why users were lost or assigned unevenly."
**Explain simply:**
- Random assignment to equal groups should give near-equal counts; some small wobble is expected.
- A **chi-square goodness-of-fit test** checks whether the observed split is plausible for a 50/50 plan.
- Common causes: a bug in assignment, bots, one version loading slower so users leave before being counted, filters applied after assignment, caching.
- If groups were created unevenly, the users in them may differ, so comparisons are unfair (see Q40).
- Fix the cause and rerun.
**Formula in plain words:** chi-square = sum of (observed minus expected) squared divided by expected, with expected = 9,800 each.
**Worked example:** (10,200 - 9,800)^2 / 9,800 + (9,400 - 9,800)^2 / 9,800 = 32.65.
**Excel / Python:**
```python
from scipy import stats

# Users actually assigned to each group, and what a 50/50 split would give
observed_users = [10200, 9400]
expected_users = [9800, 9800]

# Chi-square goodness-of-fit: could a fair 50/50 split give a gap this big by chance?
result = stats.chisquare(observed_users, f_exp=expected_users)
print("Chi-square =", round(result.statistic, 2))
print("p-value =", result.pvalue)

# Same idea as the gap shown as a percentage
print("Control share =", round(100 * 10200 / 19600, 2), "%")
```
```text
Chi-square = 32.65
p-value = 1.1016577097039444e-08
Control share = 52.04 %
```
p-value is about 1 in 100 million, so this is not luck. In Excel: =CHISQ.TEST(observed_range, expected_range) (2010+; not run in Excel here).
**Likely follow-ups:** 1) *What p-value would you flag?* Usually below 0.001 for SRM checks. 2) *Can you still use the data?* Not without finding the cause.
**Common mistakes:** Shrugging off "only 4%"; not checking the split before reading the results.

### Q49 ⭐ 🟡 How would you handle a metric that has a strong weekly pattern (for example, weekday vs weekend attendance) when comparing two periods?
**Asked at:** commonly asked (no company-specific report found); the sources file lists "KPI changed, investigate" and mix-shift scenarios as typical shapes.
**What the interviewer is checking:** Do you compare like with like, so a calendar quirk is not mistaken for a real change?
**Say this in the interview:** "I would compare whole weeks, or the same weekday against the same weekday, so the number of weekends in each period cannot distort the result."
**Explain simply:**
- A weekly pattern (seasonality) means some days are always high and some always low. If one month has more weekends, its average drops even though nothing changed.
- Fix 1: compare full weeks (4 weeks vs 4 weeks), not calendar months.
- Fix 2: compare weekdays with weekdays and weekends with weekends, or use a 7-day rolling average, which always contains one of every weekday.
- Fix 3: compare with the same period last year if there is also a yearly pattern (festival months, appraisal season).
**Worked example:** Daily attendance is always 200 on weekdays and 60 on weekends. Month A has 20 weekdays and 8 weekend days; Month B has 19 weekdays and 11 weekend days. The raw averages differ although behaviour is identical.
**Excel / Python:**
```python
# Average daily attendance on weekdays and on weekends (same in both months)
weekday_attendance = 200
weekend_attendance = 60

# Month A has 20 weekdays and 8 weekend days; Month B has 19 weekdays and 11 weekend days
weekdays_in_month_a, weekend_days_in_month_a = 20, 8
weekdays_in_month_b, weekend_days_in_month_b = 19, 11

# Overall daily average for each month (simple average over all days)
total_a = weekdays_in_month_a * weekday_attendance + weekend_days_in_month_a * weekend_attendance
total_b = weekdays_in_month_b * weekday_attendance + weekend_days_in_month_b * weekend_attendance
average_a = total_a / (weekdays_in_month_a + weekend_days_in_month_a)
average_b = total_b / (weekdays_in_month_b + weekend_days_in_month_b)
print("Month A daily average:", round(average_a, 1))
print("Month B daily average:", round(average_b, 1))

# Fair comparison: compare weekdays with weekdays and weekends with weekends
print("Weekday average, A vs B:", weekday_attendance, weekday_attendance)
print("Weekend average, A vs B:", weekend_attendance, weekend_attendance)
```
Output:
```
Month A daily average: 160.0
Month B daily average: 148.7
Weekday average, A vs B: 200 200
Weekend average, A vs B: 60 60
```
The headline fell 11 people a day, but like-for-like nothing changed: Month B simply had three more weekend days.
**Likely follow-ups:** 1) *Why not just drop weekends?* You can, if weekends are not the question; otherwise report both separately. 2) *Rolling average?* A 7-day average smooths the weekly cycle.
**Common mistakes:** Comparing a 4-weekend month with a 5-weekend month; ignoring public holidays; calling a calendar effect a performance change.

### Q50 ⭐ 🟡 How would you tell whether an employee's sudden performance spike is skill or luck (regression to the mean)?
**Asked at:** commonly asked (no company-specific report found); regression to the mean is listed in the sources file as a differentiator topic.
**What the interviewer is checking:** Do you know that extreme results tend to move back toward average, and can you test for it?
**Say this in the interview:** "Any score is skill plus luck. Someone at the very top this period was probably helped by luck, so I would expect them to fall back somewhat, and I would look at several periods before calling it skill."
**Explain simply:**
- Regression to the mean: people picked because they scored extremely high or low will, on average, score closer to normal next time, even with no change in skill.
- The less a score repeats from one period to the next (low correlation), the stronger the pull back.
- Checks: look at a longer history (6 to 12 periods), see whether the spike has a cause (new territory, easier cases, one big deal), and see how others in the top group did next period.
- Skill shows as a repeatable high level; luck shows as one-off peaks.
**Worked example:** 1,000 employees, true skill averaging 70, plus random luck each year. The top 10% in year 1 scored 85.2 on average; the same people scored 76.8 in year 2. Nobody lost skill; the luck part did not repeat.
**Excel / Python:**
```python
import numpy as np

# Make 1,000 employees: each has a fixed true skill, plus luck that changes every year
random_generator = np.random.default_rng(1)
true_skill = random_generator.normal(70, 6, 1000)
score_year_1 = true_skill + random_generator.normal(0, 6, 1000)
score_year_2 = true_skill + random_generator.normal(0, 6, 1000)

# Pick the top 10% scorers of year 1 (the "spike" group)
cutoff_score = np.percentile(score_year_1, 90)
is_top_group = score_year_1 >= cutoff_score

# Compare the same people in year 1 and year 2
print("People in top group:", is_top_group.sum())
print("Top group, year 1 average:", round(score_year_1[is_top_group].mean(), 1))
print("Top group, year 2 average:", round(score_year_2[is_top_group].mean(), 1))
print("Everyone, year 1 vs year 2:", round(score_year_1.mean(), 1), round(score_year_2.mean(), 1))
print("Year 1 vs year 2 correlation:", round(np.corrcoef(score_year_1, score_year_2)[0, 1], 2))
```
Output:
```
People in top group: 100
Top group, year 1 average: 85.2
Top group, year 2 average: 76.8
Everyone, year 1 vs year 2: 69.8 69.8
Year 1 vs year 2 correlation: 0.48
```
The top group fell about 8 points while the whole company stayed flat, which is the regression effect. (This is a simulation I built, not real data.)
**Likely follow-ups:** 1) *Does that mean spikes are always luck?* No, only that part of them is; repeated high scores are skill. 2) *How do you stop rewarding luck?* Use a longer window or a control group.
**Common mistakes:** Giving a big reward or a training credit after one extreme month; "the coaching worked" after picking the worst performers and seeing them improve.

### Q51 ⭐ 🟡 A vendor claims their delivery time is 'on average 3 days'. What further statistics would you ask for before trusting this?
**Asked at:** commonly asked (no company-specific report found); similar to the mean-vs-median scenarios in the sources file.
**What the interviewer is checking:** Do you know an average hides the spread and the slow tail?
**Say this in the interview:** "An average does not tell me how bad the late deliveries are. I would ask for the median, the 90th and 95th percentile, the share delivered within the promised time, and the sample size and period."
**Explain simply:**
- Mean (average) can be dragged up by a few very late deliveries; median (the middle value) shows the typical order.
- Percentile: the 90th percentile is the time within which 90% of orders arrive. It shows the "bad day" experience.
- Also ask: how many deliveries, which months, which cities, what counts as "delivered", and whether failed or returned orders are excluded.
**Worked example:** 100 deliveries: 90 take about 2 days, 10 take about 8 days. The mean is 2.58 days, the median 2.1, 95th percentile 7.3, and the slowest is 9.4.
**Excel / Python:**
```python
import numpy as np

# 100 deliveries: 90 normal ones (about 2 days) and 10 very late ones (about 8 days)
random_generator = np.random.default_rng(2)
normal_deliveries = random_generator.normal(2, 0.4, 90).clip(1)
late_deliveries = random_generator.normal(8, 1, 10)
delivery_days = np.round(np.concatenate([normal_deliveries, late_deliveries]), 1)

# The statistics to ask the vendor for
print("Mean days:", round(delivery_days.mean(), 2))
print("Median days:", np.median(delivery_days))
print("90th percentile:", round(np.percentile(delivery_days, 90), 1))
print("95th percentile:", round(np.percentile(delivery_days, 95), 1))
print("Share delivered within 3 days:", (delivery_days <= 3).mean())
print("Slowest delivery:", delivery_days.max())
```
Output:
```
Mean days: 2.58
Median days: 2.1
90th percentile: 3.3
95th percentile: 7.3
Share delivered within 3 days: 0.9
Slowest delivery: 9.4
```
Here "about 2 to 3 days" is true for 9 in 10 orders, but 1 in 10 waits about a week. The vendor's single number hides that. (Simulated data.) In Excel: `=PERCENTILE.INC(A2:A101, 0.95)` (Excel 2010+; not run in Excel here).
**Likely follow-ups:** 1) *Which number do you trust most?* The on-time share against the promised date. 2) *What if the vendor will not share data?* Measure a sample of your own orders.
**Common mistakes:** Accepting one average; not asking about the sample size; ignoring cancelled orders.

### Q52 ⭐ 🟡 Customers who complain are 3 times more likely to churn. How would you check whether complaints cause churn?
**Asked at:** commonly asked (no company-specific report found); churn scenarios appear in the scenario guides listed in the sources file.
**What the interviewer is checking:** Can you separate "goes together" from "causes", by looking for a hidden third factor?
**Say this in the interview:** "I would look for a common cause, like a bad delivery, that makes people both complain and leave. I would compare complainers and non-complainers within the same experience group, and ideally test an intervention."
**Explain simply:**
- Confounder: a hidden factor that drives both things. A delayed delivery can cause both the complaint and the churn.
- Check 1: split customers by the suspected confounder and compare like with like.
- Check 2: timing. Did complaints come before churn?
- Check 3: an experiment, for example faster complaint resolution for a random half, then compare churn.
**Worked example:** 5,000 customers. Overall, complainers churn 23.8% vs 7.4% for non-complainers (3.2 times). But within delayed deliveries both groups churn 30%, and within on-time deliveries both churn 5%. The delay is the cause; complaining is only a signal.
**Excel / Python:**
```python
import pandas as pd

# Customers split by delivery experience and by whether they complained
customers_table = pd.DataFrame({
    "delivery": ["delayed", "delayed", "on_time", "on_time"],
    "complained": ["yes", "no", "yes", "no"],
    "customers": [600, 400, 200, 3800],
    "churned": [180, 120, 10, 190],
})

# Churn rate for complainers vs non-complainers (ignoring delivery)
overall = customers_table.groupby("complained")[["customers", "churned"]].sum()
overall["churn_rate"] = overall["churned"] / overall["customers"]
print(overall)

# Churn rate inside each delivery group (compare like with like)
customers_table["churn_rate"] = customers_table["churned"] / customers_table["customers"]
print(customers_table[["delivery", "complained", "churn_rate"]])
```
Output:
```
            customers  churned  churn_rate
complained                                
no               4200      310     0.07381
yes               800      190     0.23750
  delivery complained  churn_rate
0  delayed        yes        0.30
1  delayed         no        0.30
2  on_time        yes        0.05
3  on_time         no        0.05
```
The table is invented to show the idea; real data is rarely this clean, and some complaints will matter in themselves.
**Likely follow-ups:** 1) *Can regression handle this?* Yes, add delivery, plan, tenure as controls. 2) *Gold standard?* A randomised experiment.
**Common mistakes:** Saying "reduce complaints and churn will fall" (hiding complaints does not retain anyone); controlling for too few factors.

### Q53 ⭐ 🟡 How would you explain to a manager why two employees with the same average performance score may need different management?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand that spread (consistency) matters as well as the average?
**Say this in the interview:** "Same average, different story. One person is steady every month; the other swings between excellent and poor. The first needs recognition, the second needs us to find what causes the swings."
**Explain simply:**
- Standard deviation (SD) measures how far scores typically sit from the average: small SD means steady, large SD means erratic.
- Steady performer: manage with stretch goals and growth.
- Erratic performer: look at the lows (workload, leave, system issues, targets that arrive in lumps) and at the highs (what went right?).
- Look at the pattern over time too: trend, not just average.
**Worked example:** Five monthly scores. Asha: 70, 70, 70, 70, 70 (average 70, SD 0). Ravi: 40, 100, 55, 95, 60 (average 70, SD 26.2).
**Excel / Python:** Excel (2010+; not run in Excel here): scores in B2:B6, average `=AVERAGE(B2:B6)`, spread `=STDEV.S(B2:B6)`. Python check:
```python
import numpy as np

# Five monthly scores for each employee
asha_scores = np.array([70, 70, 70, 70, 70])
ravi_scores = np.array([40, 100, 55, 95, 60])

# Average and spread (sample standard deviation)
print("Asha average, spread:", asha_scores.mean(), asha_scores.std(ddof=1))
print("Ravi average, spread:", ravi_scores.mean(), round(ravi_scores.std(ddof=1), 1))
```
Output:
```
Asha average, spread: 70.0 0.0
Ravi average, spread: 70.0 26.2
```
Both average 70, but Ravi's months range from 40 to 100.
**Likely follow-ups:** 1) *Any other measure?* Range or minimum, and the trend. 2) *Is high spread always bad?* No, it may reflect seasonal or project-based work.
**Common mistakes:** Ranking only on averages; calling a high SD "inconsistent" without checking why.

### Q54 ⭐ 🟡 You must compare monthly attrition across 12 locations with very different headcounts. How would you do this fairly?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know small groups give noisy rates, and can you add context instead of ranking raw percentages?
**Say this in the interview:** "Use rates, not counts, but show headcount beside each rate and test each location against the company rate. Small locations swing a lot, so I would use longer windows or a rolling 12-month rate for them."
**Explain simply:**
- Counts are unfair (big sites have more leavers); rates (leavers divided by headcount) are fairer.
- But a rate from 25 people jumps with one resignation. Show a confidence interval or a funnel chart (limits that narrow as headcount grows).
- Test each location against the company rate; remember that with 12 tests, about 0.6 false alarms (12 x 0.05) are expected by chance (see multiple comparisons).
- Use a 12-month rolling or average headcount for stability.
**Worked example:** Company monthly attrition is 1.39%. Location L has 8.0% (2 of 25), J has 5.0% (3 of 60). Their exact-test p-values are 0.047 and 0.051; large sites A and B sit near the company rate.
**Excel / Python:**
```python
import pandas as pd
from scipy import stats

# Leavers in one month and headcount for each location
locations = pd.DataFrame({
    "location": list("ABCDEFGHIJKL"),
    "headcount": [2000, 1500, 1200, 800, 600, 400, 250, 150, 100, 60, 40, 25],
    "leavers": [24, 19, 13, 11, 8, 6, 5, 4, 2, 3, 2, 2],
})

# Company-wide monthly rate is the benchmark
company_rate = locations["leavers"].sum() / locations["headcount"].sum()
print("Company monthly attrition:", round(company_rate * 100, 2), "%")

# Each location's own rate, and an exact test of "is this location different from the company rate?"
locations["rate_pct"] = (locations["leavers"] / locations["headcount"] * 100).round(2)
p_values = []
for _, row in locations.iterrows():
    test_result = stats.binomtest(int(row["leavers"]), int(row["headcount"]), company_rate)
    p_values.append(round(test_result.pvalue, 3))
locations["p_value_vs_company"] = p_values
print(locations[["location", "headcount", "leavers", "rate_pct", "p_value_vs_company"]].to_string(index=False))
```
Output:
```
Company monthly attrition: 1.39 %
location  headcount  leavers  rate_pct  p_value_vs_company
       A       2000       24      1.20               0.566
       B       1500       19      1.27               0.825
       C       1200       13      1.08               0.458
       D        800       11      1.38               1.000
       E        600        8      1.33               1.000
       F        400        6      1.50               0.829
       G        250        5      2.00               0.406
       H        150        4      2.67               0.157
       I        100        2      2.00               0.405
       J         60        3      5.00               0.051
       K         40        2      5.00               0.107
       L         25        2      8.00               0.047
```
The tiny sites show the biggest rates, but only L is barely under 0.05 and, with 12 comparisons, I would call it "worth watching", not "a problem". (Invented data.)
**Likely follow-ups:** 1) *What chart?* A funnel plot or a bar chart with error bars. 2) *Rate definition?* Leavers divided by average headcount for the month.
**Common mistakes:** Ranking locations by raw rate; using start-of-month headcount for a location that grew; ignoring that tiny sites will top any "worst" list.

### Q55 ⭐ 🟡 A dataset shows that employees with more years of experience earn more, but your analysis shows the relationship disappears within each job grade. What does this tell you?
**Asked at:** commonly asked (no company-specific report found); the Simpson-style and confounding scenarios are listed in the sources file.
**What the interviewer is checking:** Can you interpret a confounder or mediator instead of just reporting a correlation?
**Say this in the interview:** "It tells me that experience is linked to pay mainly through grade: more experienced people sit in higher grades, and the grade sets the pay band. Inside a grade, experience adds little. I would then check whether promotion itself is fair."
**Explain simply:**
- Overall correlation can be strong because higher grades contain more experienced people and pay more.
- Within a grade, the correlation is near zero, so experience does not explain pay differences among people of the same grade.
- Two readings: grade is a confounder (a common cause), or grade is the route through which experience works (a mediator). Experience may still matter by earning promotion.
- Report both views and ask how promotion decisions are made.
**Worked example:** 300 employees, 100 per grade. Overall correlation of experience and salary: 0.93. Inside Grade 1: -0.01, Grade 2: -0.02, Grade 3: 0.15.
**Excel / Python:**
```python
import numpy as np
import pandas as pd

# 300 employees: higher grades have more experience and higher pay; within a grade, experience does not change pay
random_generator = np.random.default_rng(3)
grade_settings = {"Grade 1": (2, 5), "Grade 2": (6, 9), "Grade 3": (12, 15)}
rows = []
for grade_name, (typical_years, typical_salary) in grade_settings.items():
    for _ in range(100):
        years = max(0, random_generator.normal(typical_years, 1.5))
        salary = random_generator.normal(typical_salary, 0.6)
        rows.append((grade_name, years, salary))
employees = pd.DataFrame(rows, columns=["grade", "years_experience", "salary_lakh"])

# Correlation of experience and salary, all employees together
print("All employees:", round(employees["years_experience"].corr(employees["salary_lakh"]), 2))

# Correlation inside each grade
for grade_name, group in employees.groupby("grade"):
    print(grade_name, round(group["years_experience"].corr(group["salary_lakh"]), 2))
```
Output:
```
All employees: 0.93
Grade 1 -0.01
Grade 2 -0.02
Grade 3 0.15
```
The strong overall link is created by the grades. (Simulated data, built to show the pattern.) In Excel, `=CORREL(B2:B301, C2:C301)` on all rows, then again on each grade's rows.
**Likely follow-ups:** 1) *Is this Simpson's paradox?* Related: a pattern changes when you split by a hidden group. 2) *What would you tell HR?* Pay differences are driven by grade, so audit grading and promotions.
**Common mistakes:** Saying "experience does not matter"; forgetting that grade itself may reflect experience.

### Q56 ⭐ 🟡 How would you estimate how many people are needed in a pilot to detect a 5% improvement in a process?
**Asked at:** commonly asked (no company-specific report found); sample-size questions are listed as frequent applied stats in the sources file.
**What the interviewer is checking:** Do you know sample size depends on the size of effect, the noise, and the confidence and power you want?
**Say this in the interview:** "First I would pin down what '5%' means, relative or percentage points, and the current baseline and spread. Then I would use a power calculation with 5% significance and 80% power to get people per group."
**Explain simply:**
- Power: the chance that the test catches a real effect (80% is a common target).
- Smaller improvements and noisier data need more people; the sample needed grows with the square of how small the effect is.
- Premise note: "5% improvement" is ambiguous. 5% relative (60% to 63%) and 5 points (60% to 65%) give very different answers, so confirm first.
**Worked example:** Baseline success rate 60%. To detect 60% to 63% needs about 4,129 per group; to detect 60% to 65% about 1,471 per group. For a time-based process, 40 minutes with SD 12, a 5% gain (2 minutes) needs 567 per group.
**Excel / Python:**
```python
import numpy as np
from statsmodels.stats.power import NormalIndPower, TTestIndPower
from statsmodels.stats.proportion import proportion_effectsize

power_calculator = NormalIndPower()

# Case 1: success rate 60% now; "5% improvement" read as 5% relative (60% to 63%)
effect_relative = proportion_effectsize(0.63, 0.60)
people_relative = power_calculator.solve_power(effect_relative, alpha=0.05, power=0.80)
print("60% to 63%: people per group =", int(np.ceil(people_relative)))

# Case 2: "5% improvement" read as 5 percentage points (60% to 65%)
effect_points = proportion_effectsize(0.65, 0.60)
people_points = power_calculator.solve_power(effect_points, alpha=0.05, power=0.80)
print("60% to 65%: people per group =", int(np.ceil(people_points)))

# Case 3: processing time, average 40 minutes, spread (SD) 12; 5% faster = 2 minutes
effect_time = 2 / 12
people_time = TTestIndPower().solve_power(effect_time, alpha=0.05, power=0.80)
print("Time 40 to 38 min: people per group =", int(np.ceil(people_time)))
```
Output:
```
60% to 63%: people per group = 4129
60% to 65%: people per group = 1471
Time 40 to 38 min: people per group = 567
```
Per group means the pilot needs that many in the new process and that many in the comparison.
**Likely follow-ups:** 1) *What if we only have 100 people?* Then we can only detect a bigger effect, or use a before/after design with the same people. 2) *Where does SD come from?* Past data.
**Common mistakes:** Using a rule-of-thumb "30 people"; not saying whether the number is per group; ignoring dropouts.

### Q57 ⭐ 🔴 You have to measure the effect of a work-from-home policy but cannot randomise who gets it. How would you approach the analysis?
**Asked at:** commonly asked (no company-specific report found); causal inference without randomisation is listed in the sources file as a differentiator.
**What the interviewer is checking:** Do you know the main fair-comparison methods when an experiment is impossible?
**Say this in the interview:** "I would find a comparable group without the policy, compare the change before and after in both groups (difference-in-differences), and control for role, grade and tenure. I would be clear that this is an estimate with assumptions, not proof."
**Explain simply:**
- Problem: people who get WFH may differ (role, seniority, motivation), so a simple comparison is biased.
- Difference-in-differences: subtract the comparison group's change from the policy group's change, to remove changes that hit everyone (seasonality, a new tool).
- Matching or regression: compare similar people (same grade, team, tenure).
- Check the assumption: before the policy, both groups should have been moving in parallel.
- Also pick measures carefully (output, attrition, engagement) and watch for people who opted in.
**Worked example:** Productivity score: WFH team 72 to 78 (+6); comparison team 73 to 75 (+2). Estimated policy effect: +4.
**Excel / Python:**
```python
# Average productivity score before and after the policy
wfh_team_before, wfh_team_after = 72, 78
comparison_team_before, comparison_team_after = 73, 75

# Change in each team
wfh_team_change = wfh_team_after - wfh_team_before
comparison_team_change = comparison_team_after - comparison_team_before

# Difference-in-differences: the change beyond what the comparison team also saw
policy_effect = wfh_team_change - comparison_team_change
print("WFH team change:", wfh_team_change)
print("Comparison team change:", comparison_team_change)
print("Estimated policy effect:", policy_effect)
```
Output:
```
WFH team change: 6
Comparison team change: 2
Estimated policy effect: 4
```
Only 4 of the 6 points are credited to the policy. (Invented numbers; a real analysis would add a confidence interval.)
**Likely follow-ups:** 1) *Other options?* Phased rollout, or a cut-off rule (regression discontinuity). 2) *Biggest risk?* People self-select into WFH.
**Common mistakes:** Simple before/after with no comparison group; treating WFH employees as typical; claiming proof of cause.

### Q58 ⭐ 🔴 A test has 80% power and you ran 10 experiments where 2 are truly effective. Roughly how many significant results do you expect, and how many are false?
**Asked at:** commonly asked (no company-specific report found); power and false-discovery arithmetic is listed in the sources file as a differentiator.
**What the interviewer is checking:** Can you combine power and the 5% false-positive rate to think about how many "wins" are real?
**Say this in the interview:** "About 1.6 of the 2 real effects are detected, and about 0.4 of the 8 non-effects come up significant by chance, so around 2 significant results, one in five of them false. I am assuming a 5% significance level."
**Explain simply:**
- Power 80%: a real effect is detected 80% of the time.
- Significance level 5%: a non-effect still shows "significant" 5% of the time (false positive).
- Expected true hits: 2 x 0.80 = 1.6. Expected false hits: 8 x 0.05 = 0.4. Total about 2.0.
- False share of the significant results: 0.4 / 2.0 = 20%.
- Lesson: a "significant" result is not guaranteed real, especially when real effects are rare.
**Worked example:** Verified by simulating the 10 experiments 200,000 times.
**Excel / Python:**
```python
import numpy as np

# Expected counts by simple arithmetic
truly_effective, truly_ineffective = 2, 8
power, false_positive_rate = 0.80, 0.05
expected_true_hits = truly_effective * power
expected_false_hits = truly_ineffective * false_positive_rate
print("Expected true hits:", expected_true_hits)
print("Expected false hits:", expected_false_hits)
print("Expected significant total:", expected_true_hits + expected_false_hits)
print("Share of significant results that are false:", expected_false_hits / (expected_true_hits + expected_false_hits))

# Check by simulating the 10 experiments 200,000 times
random_generator = np.random.default_rng(5)
true_hits = random_generator.binomial(truly_effective, power, 200000)
false_hits = random_generator.binomial(truly_ineffective, false_positive_rate, 200000)
print("Simulated true hits:", round(true_hits.mean(), 2))
print("Simulated false hits:", round(false_hits.mean(), 2))
print("Simulated false share:", round(false_hits.sum() / (true_hits + false_hits).sum(), 2))
```
Output:
```
Expected true hits: 1.6
Expected false hits: 0.4
Expected significant total: 2.0
Share of significant results that are false: 0.2
Simulated true hits: 1.6
Simulated false hits: 0.4
Simulated false share: 0.2
```
The simulation agrees with the arithmetic.
**Likely follow-ups:** 1) *What if only 1 in 10 is truly effective?* The false share rises: 0.8 true hits and 9 x 0.05 = 0.45 false hits, so 0.45 / 1.25 = 36% of significant results are false. 2) *How to reduce false wins?* Stricter threshold, replication.
**Common mistakes:** Saying "5% of the results are false"; mixing up power with significance level.

### Q59 ⭐ 🔴 An A/B test on a rare event (0.5% conversion) needs a very large sample. What practical alternatives do you suggest to the business?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you offer practical options instead of only saying "we need more data"?
**Say this in the interview:** "I would first show the sample needed. If it is unrealistic, I would use an earlier, more frequent proxy metric, accept a bigger minimum effect, run longer, or loosen the decision threshold if the decision is cheap and reversible."
**Explain simply:**
- Rare events give few successes, so the signal is buried in noise.
- Options: (1) a proxy metric that happens more often (add-to-cart, shortlisted candidates instead of hires); (2) test only a bold change that gives a bigger effect; (3) run longer or include more traffic; (4) reduce noise using pre-experiment data (variance reduction); (5) use a looser threshold for low-risk decisions; (6) combine with qualitative evidence.
- Be clear about the trade-off of each (a proxy may not move the real goal).
**Worked example:** To detect 0.5% to 0.6% needs 85,686 per group. A common proxy (5% to 6%, the same 20% relative lift) needs 8,143. Accepting alpha 0.10 one-sided brings the rare-outcome case to 49,213.
**Excel / Python:**
```python
import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

power_calculator = NormalIndPower()

# Rare event: 0.5% to 0.6% conversion
effect_rare = proportion_effectsize(0.006, 0.005)
rare_per_group = power_calculator.solve_power(effect_rare, alpha=0.05, power=0.80)
print("Rare outcome 0.5% to 0.6%, per group:", int(np.ceil(rare_per_group)))

# Common proxy metric: 5% to 6% (same 20% relative lift)
effect_common = proportion_effectsize(0.06, 0.05)
common_per_group = power_calculator.solve_power(effect_common, alpha=0.05, power=0.80)
print("Proxy metric 5% to 6%, per group:", int(np.ceil(common_per_group)))

# Looser rule: alpha 0.10, one-sided, for a low-cost reversible decision
effect_loose = proportion_effectsize(0.006, 0.005)
loose_per_group = power_calculator.solve_power(effect_loose, alpha=0.10, power=0.80, alternative="larger")
print("Rare outcome, alpha 0.10 one-sided, per group:", int(np.ceil(loose_per_group)))
```
Output:
```
Rare outcome 0.5% to 0.6%, per group: 85686
Proxy metric 5% to 6%, per group: 8143
Rare outcome, alpha 0.10 one-sided, per group: 49213
```
A proxy needs roughly a tenth of the people; a looser threshold still needs a very large sample.
**Likely follow-ups:** 1) *Danger of proxies?* They may not move the real outcome. 2) *Can we peek?* Only with a proper sequential method.
**Common mistakes:** Stopping the test when it "looks good"; changing the metric after seeing results.

### Q60 ⭐ 🔴 Your boss insists on a result of 'no difference' after a non-significant test. What can and can't you conclude?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know "not significant" means "not proven different", not "proven the same"?
**Say this in the interview:** "A non-significant result says we did not find enough evidence of a difference. It does not show there is none. The confidence interval tells us which sizes of difference are still possible."
**Explain simply:**
- Absence of evidence is not evidence of absence: the test may simply be too small (low power).
- The confidence interval is the honest summary: if it runs from a meaningful loss to a meaningful gain, the test is inconclusive.
- To prove "no meaningful difference", define in advance a margin you would accept (equivalence test) and show the interval lies inside it.
**Worked example:** A pilot with 400 people per group: resolution rate 30% vs 33%. p = 0.361 (not significant). The 95% interval for the difference is -3.4 to +9.4 points, so the new process could be slightly worse or up to 9 points better.
**Excel / Python:**
```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# Pilot: 400 people per group; 120 resolved in control, 132 in new process
control_size, new_size = 400, 400
control_successes, new_successes = 120, 132

# Significance test
z_value, p_value = proportions_ztest([new_successes, control_successes], [new_size, control_size])
print("p-value:", round(p_value, 3))

# 95% confidence interval for the difference in rates
control_rate = control_successes / control_size
new_rate = new_successes / new_size
difference = new_rate - control_rate
standard_error = np.sqrt(control_rate * (1 - control_rate) / control_size + new_rate * (1 - new_rate) / new_size)
print("Observed difference:", round(difference * 100, 1), "points")
print("95% CI:", round((difference - 1.96 * standard_error) * 100, 1), "to", round((difference + 1.96 * standard_error) * 100, 1), "points")
```
Output:
```
p-value: 0.361
Observed difference: 3.0 points
95% CI: -3.4 to 9.4 points
```
What I would tell the boss: "inconclusive; we cannot rule out a useful improvement; a bigger pilot is needed." (Invented numbers.)
**Likely follow-ups:** 1) *How would we show equivalence?* Equivalence test (TOST) with a pre-agreed margin. 2) *What if the boss still wants to stop?* Report the interval and the risk.
**Common mistakes:** Writing "no effect" in the report; ignoring the sample size.

### Q61 ⭐ 🔴 Estimate the number of employees likely to attrite next quarter and give a range. How do you build and communicate it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you turn a rate into a number with an honest range, and explain the assumptions?
**Say this in the interview:** "I would take the recent quarterly attrition rate, apply it to current headcount for the point estimate, then add a range that covers both random chance and quarter-to-quarter variation. I would say what could move it, like appraisal season."
**Explain simply:**
- Point estimate: headcount times the expected quarterly rate.
- Chance-only range: even with a fixed 3% chance, the number of leavers varies (binomial spread).
- Wider range: the rate itself changes each quarter, so simulate with that variation too.
- Communicate: "about 24, most likely between 11 and 39", the assumptions (no major policy change, seasonality) and what would change the forecast. Optionally segment by team or tenure.
**Worked example:** Headcount 800. Last four quarters' leavers: 21, 27, 18, 30 (rates 2.6%, 3.4%, 2.3%, 3.8%), average 3.0%. Expected leavers = 800 x 0.03 = 24.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Headcount and last four quarters of leavers
current_headcount = 800
leavers_last_four_quarters = np.array([21, 27, 18, 30])
quarterly_rates = leavers_last_four_quarters / 800
average_rate = quarterly_rates.mean()
rate_spread = quarterly_rates.std(ddof=1)
print("Average quarterly rate:", round(average_rate, 4), "Spread of rate:", round(rate_spread, 4))

# Step 1: pure chance range (each person leaves with probability 3%)
low_chance, high_chance = stats.binom.ppf([0.025, 0.975], current_headcount, average_rate)
print("Expected leavers:", current_headcount * average_rate)
print("Chance-only 95% range:", int(low_chance), "to", int(high_chance))

# Step 2: also allow the underlying rate to vary quarter to quarter (simulation)
random_generator = np.random.default_rng(7)
simulated_rates = np.clip(random_generator.normal(average_rate, rate_spread, 100000), 0.001, None)
simulated_leavers = random_generator.binomial(current_headcount, simulated_rates)
low_wide, median_wide, high_wide = np.percentile(simulated_leavers, [2.5, 50, 97.5])
print("Wider 95% range:", int(low_wide), "to", int(high_wide), "median", int(median_wide))
```
Output:
```
Average quarterly rate: 0.03 Spread of rate: 0.0068
Expected leavers: 24.0
Chance-only 95% range: 15 to 34
Wider 95% range: 11 to 39 median 24
```
I would report "about 24, plausible range roughly 11 to 39". Only four quarters of history is thin, so the range is itself approximate.
**Likely follow-ups:** 1) *Better method?* A model with tenure, team and seasonality. 2) *What if a reorganisation is planned?* Adjust and say so.
**Common mistakes:** Giving a single number; forgetting that headcount changes; ignoring seasonality.

### Q62 ⭐ 🔴 A KPI improves after a policy change, but a similar KPI in a neighbouring unit with no change also improves. What does this suggest for your conclusion?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you use a comparison group to avoid crediting a policy for a general trend?
**Say this in the interview:** "It suggests part or all of the improvement came from something common to both units, like seasonality or a company-wide change. I would credit the policy only with the extra gain over the neighbour."
**Explain simply:**
- Before/after without a comparison attributes everything to the policy.
- The neighbouring unit shows what would likely have happened anyway (the common trend).
- The policy effect is the difference between the two changes (difference-in-differences), valid if the units were moving similarly before.
- Check the units are really similar, and whether the policy leaked to the neighbour.
**Worked example:** Policy unit 60 to 66 (+6); neighbour 61 to 65 (+4). Only 2 points are left for the policy.
**Excel / Python:**
```python
# Average KPI before and after, for the unit with the policy and the neighbouring unit without it
policy_unit_before, policy_unit_after = 60.0, 66.0
neighbour_unit_before, neighbour_unit_after = 61.0, 65.0

# Naive before/after claim vs the fairer comparison
naive_claim = policy_unit_after - policy_unit_before
common_trend = neighbour_unit_after - neighbour_unit_before
policy_effect = naive_claim - common_trend
print("Naive before/after gain:", naive_claim)
print("Gain also seen without the policy:", common_trend)
print("Gain left for the policy:", policy_effect)
```
Output:
```
Naive before/after gain: 6.0
Gain also seen without the policy: 4.0
Gain left for the policy: 2.0
```
Two thirds of the improvement would have happened anyway; whether the remaining 2 points are real needs a confidence interval. (Invented numbers.)
**Likely follow-ups:** 1) *What if the neighbour improved more?* Then the policy gets no credit. 2) *What if the units differ?* Add controls or use more comparison units.
**Common mistakes:** Claiming the whole gain; using a very different unit as comparison.

### Q63 ⭐ 🔴 Explain how survivorship bias could distort an analysis of the performance of employees hired three years ago.
**Asked at:** commonly asked (no company-specific report found); survivorship bias is listed in the sources file as a differentiator.
**What the interviewer is checking:** Do you notice who is missing from the data, and why it matters?
**Say this in the interview:** "Looking only at people still here after three years leaves out those who left or were let go, often the weaker performers. So the group looks better than the whole hiring batch, and a hiring source or training programme can look better than it was."
**Explain simply:**
- Survivorship bias: drawing conclusions only from the "survivors" because the ones who dropped out are not in the data.
- Effect: averages look too high, and the link between hiring source and performance is distorted.
- Fix: start from the full original hiring batch (the cohort), include leavers with their last known ratings, analyse retention as an outcome too.
- Caution: people may also leave because they were top performers poached by others, so the direction can vary; always ask why people left.
**Worked example:** 500 hires. Better performers are more likely to stay. 356 are still employed; their average ability is 73.1 against 70.2 for all 500.
**Excel / Python:**
```python
import numpy as np

# 500 people hired 3 years ago; true ability varies; better people are more likely to still be here
random_generator = np.random.default_rng(11)
true_ability = random_generator.normal(70, 8, 500)
chance_of_staying = 1 / (1 + np.exp(-(true_ability - 65) / 4))
still_employed = random_generator.random(500) < chance_of_staying

# What you see today (only stayers) vs the truth (everyone hired)
print("Employees still here:", still_employed.sum(), "of 500")
print("True average ability, all hired:", round(true_ability.mean(), 1))
print("Average ability, stayers only:", round(true_ability[still_employed].mean(), 1))
```
Output:
```
Employees still here: 356 of 500
True average ability, all hired: 70.2
Average ability, stayers only: 73.1
```
The stayers' average overstates the batch by about 3 points. (Simulated; in real life you would not know true ability, only recorded ratings.)
**Likely follow-ups:** 1) *Other examples?* Studying only successful startups, or only surveyed customers who stayed. 2) *How to check?* Compare leavers' and stayers' ratings at hiring.
**Common mistakes:** Using the current employee list as "everyone hired"; ignoring exit data.

### Q64 ⭐ 🔴 A metric moved from 20.0% to 20.4%, and the dashboard colours it green. How would you design the dashboard to avoid over-reading noise?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you design a dashboard so small random moves are not treated as signals?
**Say this in the interview:** "I would only colour a change when it passes a threshold based on normal variation. Otherwise it stays neutral grey. I would also show sample size, a trend line and an uncertainty band, so a 0.4-point move is shown as within normal range."
**Explain simply:**
- Green and red invite action; use them only when a change is statistically or practically meaningful.
- Add a neutral zone: small changes (within the usual month-to-month noise, or below a business minimum like 1 point) get grey with a flat-arrow symbol.
- Show the confidence interval or a control chart band (the normal range around the average) and the sample size.
- Show the trend over 12+ periods, not just last month vs this month.
- Separate "statistically significant" from "big enough to matter".
**Worked example:** The same 0.4-point change measured on different numbers of people per month: its 95% interval includes zero at every sample size shown.
**Excel / Python:**
```python
import numpy as np
from scipy import stats

# Same 20.0% to 20.4% move, measured on different numbers of people in each month
last_month_rate, this_month_rate = 0.200, 0.204
for people_per_month in [400, 2000, 10000, 50000]:
    standard_error = np.sqrt(last_month_rate * (1 - last_month_rate) / people_per_month + this_month_rate * (1 - this_month_rate) / people_per_month)
    z_value = (this_month_rate - last_month_rate) / standard_error
    p_value = 2 * (1 - stats.norm.cdf(z_value))
    low = (this_month_rate - last_month_rate - 1.96 * standard_error) * 100
    high = (this_month_rate - last_month_rate + 1.96 * standard_error) * 100
    print(people_per_month, "people: p =", round(p_value, 2), "| 95% CI of change:", round(low, 1), "to", round(high, 1), "points")
```
Output:
```
400 people: p = 0.89 | 95% CI of change: -5.2 to 6.0 points
2000 people: p = 0.75 | 95% CI of change: -2.1 to 2.9 points
10000 people: p = 0.48 | 95% CI of change: -0.7 to 1.5 points
50000 people: p = 0.12 | 95% CI of change: -0.1 to 0.9 points
```
Even with 50,000 people a month the move is not significant; with 2,000 it could be anything from -2 to +3 points. Green is not justified.
**Likely follow-ups:** 1) *What chart?* A line chart with a shaded normal range, or a control chart. 2) *What if it is significant but tiny?* Mark it "real but small", not as a success.
**Common mistakes:** Colouring every up-move green; showing percentages without counts; judging from one month.
