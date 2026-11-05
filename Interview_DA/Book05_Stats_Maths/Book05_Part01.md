# Book 5 — Statistics & Maths for Data Analysts | Part 1: Maths Foundations 🟢

**Target:** 60 questions | **Actual:** 61 questions
**Scope:** business/analyst maths: percentages, percentage points, ratios, averages, weighted average, growth rates (YoY, MoM, CAGR), attrition and funnel arithmetic.

### Q1 ⭐⭐⭐ 🟢 How do you calculate percentage change, and what is the base you divide by?
**Asked at:** commonly asked (no company-specific report found); percentage change appears as a live "calculate" task on practice platforms (Dataford) and in consulting-style prep guides (Umbrex).
**What the interviewer is checking:** Whether you divide by the right number (the starting value) and can say what the result means.
**Say this in the interview:** "Percentage change is the new value minus the old value, divided by the old value, times 100. The base is always the starting point, the value you are comparing against, not the new value."
**Explain simply:**
- Step 1: find the change (new minus old). A positive answer is an increase, a negative answer is a decrease.
- Step 2: divide by the base, which is the old (starting) value. This turns the raw change into "how big is it compared to where we began".
- Step 3: multiply by 100 to show it as a percentage.
- The base matters because the same change looks big against a small start and small against a big start.
**Formula in plain words:** (new value minus old value) divided by old value, times 100. In symbols: % change = (New - Old) / Old x 100.
**Worked example:** Headcount grew from 200 to 250 employees. Change = 50. Base = 200 (the old headcount). 50 / 200 = 0.25, so 25% growth. Dividing by 250 by mistake would give 20%, which is wrong.
**Excel / Python:**
```python
# Headcount at the start and at the end of the period
old_headcount = 200
new_headcount = 250

# Step 1: the raw change
change_in_headcount = new_headcount - old_headcount

# Step 2: divide by the starting value (the base), then turn into a percentage
percentage_change = change_in_headcount / old_headcount * 100

print("Change:", change_in_headcount)
print("Percentage change:", percentage_change)
```
```text
Change: 50
Percentage change: 25.0
```
The headcount rose by 50 people, which is 25% of where we started.
Excel (all versions, not run in Excel here): old value in B2 (200), new value in C2 (250). In D2 type `=(C2-B2)/B2`, then format the cell as Percentage. It returns 25%.
**Likely follow-ups:** 1) *What if the old value is zero?* The percentage is undefined; report the absolute change instead (see Q37). 2) *What if the result is negative?* It is a decrease, say "fell by".
**Common mistakes:** Dividing by the new value; forgetting to format as a percentage in Excel; reporting a drop as a positive number.

### Q2 ⭐⭐⭐ 🟢 Sales went from 80,000 to 92,000. What is the percentage increase?
**Asked at:** commonly asked (no company-specific report found); the same style of task (cost 80 to 62) is a live question on Dataford.
**What the interviewer is checking:** Quick, accurate mental arithmetic with the correct base.
**Say this in the interview:** "The increase is 12,000. Divided by the starting 80,000 that is 0.15, so sales grew 15%."
**Explain simply:**
- Increase = 92,000 minus 80,000 = 12,000.
- Base = 80,000, the earlier figure.
- 12,000 / 80,000 = 0.15 = 15%.
- Shortcut: 10% of 80,000 is 8,000, and half of that (5%) is 4,000, so 15% is 12,000. That confirms the answer.
**Formula in plain words:** (new minus old) divided by old, times 100.
**Worked example:** As above: 80,000 to 92,000 is a 15% increase. Check by going forward: 80,000 x 1.15 = 92,000.
**Excel / Python:**
```python
# Sales in the earlier and the later period
sales_last_year = 80000
sales_this_year = 92000

# The raw increase
increase_in_sales = sales_this_year - sales_last_year

# Divide by the earlier figure (the base) to get the percentage increase
percentage_increase = increase_in_sales / sales_last_year * 100

print("Increase:", increase_in_sales)
print("Percentage increase:", percentage_increase)
```
```text
Increase: 12000
Percentage increase: 15.0
```
Sales rose by 12,000, which is 15% of last year's sales.
Excel (not run in Excel here): `=(92000-80000)/80000` returns 0.15, shown as 15% when formatted as a percentage.
**Likely follow-ups:** 1) *What if it went from 92,000 down to 80,000?* The fall is 12,000 / 92,000 = 13.04%, not 15%, because the base changed (see Q12). 2) *How do you double-check?* Multiply the old value by 1.15.
**Common mistakes:** Dividing by 92,000 (gives 13.04%); saying "12%" because the difference is 12 thousand.

### Q3 ⭐⭐⭐ 🟢 What is the difference between a percentage and a percentage point? Attrition moved from 10% to 12%: how do you report it?
**Asked at:** commonly asked (no company-specific report found); the percentage vs percentage point distinction is standard in case-interview maths guides (Umbrex).
**What the interviewer is checking:** Whether you can avoid the most common reporting error on rates.
**Say this in the interview:** "A percentage point is the plain difference between two percentages; a percentage is a relative change. Attrition moved from 10% to 12%, so it rose by 2 percentage points, which is a 20% relative increase. I would report both, and say which is which."
**Explain simply:**
- A percentage point (pp) is subtraction on the percentage scale: 12% minus 10% = 2 pp.
- A percentage change is relative to the starting rate: 2 divided by 10 = 20%.
- Both statements are true, but they say different things, so label them clearly.
- Safe wording: "Attrition rose from 10% to 12%, up 2 percentage points (a 20% relative increase)."
**Formula in plain words:** Percentage-point change = new rate minus old rate. Relative change = percentage-point change divided by old rate, times 100.
**Worked example:** Attrition 10% to 12%: 2 pp absolute, 20% relative. If the company has 1,000 employees, that is 100 leavers becoming 120 leavers, which is 20 more people.
**Excel / Python:**
```python
# Attrition rate in percent, last year and this year
old_attrition_rate = 10
new_attrition_rate = 12

# Difference on the percentage scale (percentage points)
change_in_percentage_points = new_attrition_rate - old_attrition_rate

# Relative change compared to the old rate
relative_change_percent = change_in_percentage_points / old_attrition_rate * 100

print("Percentage points:", change_in_percentage_points)
print("Relative change (%):", relative_change_percent)
```
```text
Percentage points: 2
Relative change (%): 20.0
```
The rate moved by 2 percentage points, and that move equals 20% of the old rate.
Excel (not run in Excel here): rates in B2 (10%) and C2 (12%). `=C2-B2` returns 2% (read it as 2 pp); `=(C2-B2)/B2` returns 20%.
**Likely follow-ups:** 1) *Which is better to report?* Both, with labels; pp for the simple gap, relative for impact. 2) *What is a basis point?* 1 percentage point = 100 basis points (see Q43).
**Common mistakes:** Writing "attrition rose 2%" (ambiguous); saying "up 20 percentage points".

### Q4 ⭐⭐⭐ 🟢 How do you calculate the attrition rate of a company? Why do we use average headcount?
**Asked at:** commonly asked (no company-specific report found); the formula "leavers divided by average headcount x 100" is given in HR glossaries (Kredily, Intervue) and an Excel guide on Flevy.
**What the interviewer is checking:** Whether you know the standard HR metric and why the denominator is an average.
**Say this in the interview:** "Attrition rate is the number of employees who left in the period, divided by the average headcount in that period, times 100. I use the average because headcount changes during the year, and the average represents the typical size of the workforce that was exposed to the risk of leaving."
**Explain simply:**
- Leavers: everyone who left in the period (resignations, terminations, retirements; define whether you include all or only voluntary).
- Average headcount: (opening headcount + closing headcount) / 2. Opening is the number at the start, closing at the end.
- Using only the opening number overstates the rate if the company grew; using only the closing number understates it.
- For monthly figures, a stricter average uses all 12 month-end headcounts.
**Formula in plain words:** Attrition rate = leavers divided by average headcount, times 100.
**Worked example:** Opening headcount 200, closing 240, leavers 30. Average = (200 + 240) / 2 = 220. Attrition = 30 / 220 = 13.64%. Using opening only gives 15%, closing only gives 12.5%; the average sits between them.
**Excel / Python:**
```python
# Headcount at start and end of the year, and number of leavers
opening_headcount = 200
closing_headcount = 240
employees_who_left = 30

# Average headcount over the year
average_headcount = (opening_headcount + closing_headcount) / 2

# Attrition rate based on the average headcount
attrition_rate = employees_who_left / average_headcount * 100

# For comparison: what opening-only and closing-only would give
rate_using_opening = employees_who_left / opening_headcount * 100
rate_using_closing = employees_who_left / closing_headcount * 100

print("Average headcount:", average_headcount)
print("Attrition rate (%):", round(attrition_rate, 2))
print("Opening-only (%):", rate_using_opening)
print("Closing-only (%):", rate_using_closing)
```
```text
Average headcount: 220.0
Attrition rate (%): 13.64
Opening-only (%): 15.0
Closing-only (%): 12.5
```
About 13.6% of the typical workforce left; the other two bases give 15% and 12.5%, so the choice of base matters.
Excel (not run in Excel here): opening in B1 (200), closing in B2 (240), leavers in B3 (30). `=B3/AVERAGE(B1:B2)` returns 0.1364; format as Percentage.
**Likely follow-ups:** 1) *Voluntary vs total attrition?* Keep leavers consistent; many firms report both. 2) *Should the leavers include new joiners who left within the year?* Yes, they left, and they also count in the average via headcount.
**Common mistakes:** Dividing by opening or closing headcount without saying so; mixing monthly leavers with an annual headcount.

### Q5 ⭐⭐⭐ 🟢 What is the difference between a simple average and a weighted average?
**Asked at:** commonly asked (no company-specific report found); weighted vs simple average is a core topic in analyst number-basics guides (Fuse Academics snippet).
**What the interviewer is checking:** Whether you know that groups of different sizes must not count equally.
**Say this in the interview:** "A simple average treats every value as equally important: add them up and divide by how many. A weighted average gives each value a weight, such as headcount, so bigger groups count more. If the groups are different sizes, the weighted average is the correct one."
**Explain simply:**
- Simple average: sum of values / number of values.
- Weighted average: sum of (value x weight) / sum of weights.
- Weights are usually counts (employees, orders, candidates) or importance scores (KPI weights).
- If all weights are equal, both averages give the same answer.
**Formula in plain words:** Multiply each value by its weight, add these up, then divide by the total of the weights. In symbols: sum(value x weight) / sum(weight).
**Worked example:** A company has three salary bands: 8 employees earn 30,000, 1 earns 50,000, 1 earns 90,000. The simple average of the three band salaries is 56,667, but that pretends each band has one person. The true average salary per employee is (8 x 30,000 + 50,000 + 90,000) / 10 = 38,000.
**Excel / Python:**
```python
# Salary of each band and how many employees are in it
band_salaries = [30000, 50000, 90000]
employees_in_band = [8, 1, 1]

# Simple average: every band counts the same
simple_average = sum(band_salaries) / len(band_salaries)

# Weighted average: multiply each salary by its headcount, add, divide by total headcount
total_salary_bill = 0
for salary, headcount in zip(band_salaries, employees_in_band):
    total_salary_bill = total_salary_bill + salary * headcount

total_employees = sum(employees_in_band)
weighted_average = total_salary_bill / total_employees

print("Simple average:", round(simple_average))
print("Weighted average:", weighted_average)
```
```text
Simple average: 56667
Weighted average: 38000.0
```
The simple average (56,667) is much too high because it ignores that most people are in the lowest band; the weighted average (38,000) is the real average per employee.
Excel (2007+, not run in Excel here): salaries in B2:B4, headcounts in C2:C4. `=SUMPRODUCT(B2:B4,C2:C4)/SUM(C2:C4)` returns 38000, while `=AVERAGE(B2:B4)` returns 56666.67.
**Likely follow-ups:** 1) *When are they equal?* When all weights are equal. 2) *Give a weight other than headcount.* KPI importance in a scorecard (Q56).
**Common mistakes:** Averaging the band averages; using AVERAGE on a column of group averages.

### Q6 ⭐⭐⭐ 🟢 Two branches have 90% and 80% pass rates with 100 and 400 candidates. What is the overall pass rate?
**Asked at:** commonly asked (no company-specific report found); averaging-ratios pitfalls are discussed in HR analytics writing (HR Exchange Network).
**What the interviewer is checking:** Whether you weight by group size instead of averaging the two percentages (which would give the wrong 85%).
**Say this in the interview:** "I count the people. Branch A passes 90 of 100, Branch B passes 320 of 400. Total passed is 410 out of 500, so the overall pass rate is 82%, not 85%."
**Explain simply:**
- Turn each rate back into a count: 90% of 100 = 90; 80% of 400 = 320.
- Add the passes (410) and the candidates (500).
- Divide: 410 / 500 = 82%.
- The simple average of 90% and 80% is 85%, which wrongly treats both branches as equal in size. Branch B is four times bigger, so the answer sits close to 80%.
**Formula in plain words:** Overall rate = total successes divided by total candidates (a weighted average of the branch rates, weighted by candidates).
**Worked example:** As above: 410 / 500 = 82%. Weighted form: (0.90 x 100 + 0.80 x 400) / 500 = 0.82.
**Excel / Python:**
```python
# Pass rate and number of candidates for each branch
branch_pass_rates = [0.90, 0.80]
branch_candidates = [100, 400]

# Turn each rate into a number of people who passed
branch_passed = []
for rate, candidates in zip(branch_pass_rates, branch_candidates):
    branch_passed.append(rate * candidates)

# Overall rate = total passed / total candidates
overall_pass_rate = sum(branch_passed) / sum(branch_candidates)

# The wrong shortcut, for comparison
simple_average_of_rates = sum(branch_pass_rates) / len(branch_pass_rates)

print("Passed per branch:", branch_passed)
print("Overall pass rate:", overall_pass_rate)
print("Wrong simple average:", round(simple_average_of_rates, 2))
```
```text
Passed per branch: [90.0, 320.0]
Overall pass rate: 0.82
Wrong simple average: 0.85
```
Of 500 candidates, 410 passed, so 82%. The simple average of 85% overstates it.
Excel (2007+, not run in Excel here): rates in B2:B3, candidates in C2:C3. `=SUMPRODUCT(B2:B3,C2:C3)/SUM(C2:C3)` returns 0.82.
**Likely follow-ups:** 1) *When would 85% be right?* Only if both branches had equal candidates. 2) *Name this effect.* Weighting by group size; the same trap underlies Simpson's paradox (Q41).
**Common mistakes:** Averaging 90 and 80; forgetting to convert rates back into counts.

### Q7 ⭐⭐⭐ 🟢 Why can you not just average two percentages? When is it acceptable?
**Asked at:** commonly asked (no company-specific report found); "averaging ratios" is a known reporting pitfall (HR Exchange Network).
**What the interviewer is checking:** Whether you know a percentage hides its denominator.
**Say this in the interview:** "A percentage is a part divided by a whole, and the wholes can differ. Averaging two percentages ignores the group sizes. It is acceptable only when the denominators are equal, or when I truly want each group to count equally, such as comparing branches as units rather than people."
**Explain simply:**
- 90% of 100 and 80% of 400 are not equally important; the second group has four times the people.
- Correct method: add the numerators (successes), add the denominators (totals), then divide.
- Acceptable cases: equal group sizes; or a deliberate "each team counts once" metric, stated clearly.
- Even then, say which average you used.
**Formula in plain words:** Combined rate = sum of numerators divided by sum of denominators.
**Worked example:** Equal groups: 90% of 250 and 80% of 250 gives (225 + 200) / 500 = 85%, the same as averaging the percentages. Unequal groups (100 and 400) gives 82% (Q6), not 85%.
**Excel / Python:**
```python
# Equal group sizes: simple average and true combined rate agree
equal_sizes = [250, 250]
rates = [0.90, 0.80]

passed_equal = 0
for rate, size in zip(rates, equal_sizes):
    passed_equal = passed_equal + rate * size

combined_equal = passed_equal / sum(equal_sizes)
average_of_rates = sum(rates) / len(rates)

print("Equal sizes, combined rate:", round(combined_equal, 4))
print("Simple average of rates:", round(average_of_rates, 4))
```
```text
Equal sizes, combined rate: 0.85
Simple average of rates: 0.85
```
With equal sizes both methods give 85%; with unequal sizes they differ (Q6).
Excel (not run in Excel here): `=AVERAGE(B2:B3)` is only valid when C2 equals C3; otherwise use SUMPRODUCT as in Q6.
**Likely follow-ups:** 1) *What is the safe default?* Pool the counts. 2) *What if I only have percentages and no counts?* Say the figure is an unweighted average and flag the limitation.
**Common mistakes:** Using AVERAGE on a percentage column from a pivot table; not stating which average was used.

### Q8 ⭐⭐⭐ 🟢 What is year-over-year (YoY) growth versus month-over-month (MoM) growth, and how do you calculate each?
**Asked at:** commonly asked (no company-specific report found); YoY and MoM calculation tasks appear in SQL/analytics practice material (Dataford, besthub).
**What the interviewer is checking:** Whether you pick the right comparison period and know what each one removes (seasonality) or shows (momentum).
**Say this in the interview:** "YoY compares a period with the same period one year earlier, for example January 2026 against January 2025. MoM compares with the previous month. Both use the same formula, (current minus previous) divided by previous. YoY removes seasonality; MoM shows short-term momentum."
**Explain simply:**
- YoY: same month (or quarter) a year ago is the base. Good for seasonal businesses such as hiring in March or festive-season sales.
- MoM: last month is the base. Quick to react, but noisy and affected by seasons.
- Both are percentage changes, so the base is the earlier period.
- If the earlier period is zero, the growth is undefined (Q37).
**Formula in plain words:** Growth = (this period minus comparison period) divided by comparison period, times 100.
**Worked example:** Applications received: Jan 2025 = 400, Jan 2026 = 460, Feb 2026 = 437. YoY for January = (460 - 400) / 400 = 15%. MoM for February = (437 - 460) / 460 = -5%. February applications are down 5% on January even though the year is growing.
**Excel / Python:**
```python
# Applications received in three periods
january_2025 = 400
january_2026 = 460
february_2026 = 437

# YoY: compare January 2026 with January 2025
yoy_growth = (january_2026 - january_2025) / january_2025 * 100

# MoM: compare February 2026 with January 2026
mom_growth = (february_2026 - january_2026) / january_2026 * 100

print("YoY growth (%):", yoy_growth)
print("MoM growth (%):", mom_growth)
```
```text
YoY growth (%): 15.0
MoM growth (%): -5.0
```
January is 15% above last January, while February is 5% below January.
Excel (not run in Excel here): monthly values in column B, January 2025 in B2 and January 2026 in B14. YoY: `=(B14-B2)/B2`. MoM for a row: `=(B15-B14)/B14`.
**Likely follow-ups:** 1) *Why prefer YoY for seasonal data?* It compares like with like. 2) *Does MoM compound?* Monthly rates do not add up to a yearly rate (see Q58, Q60).
**Common mistakes:** Comparing a month with the previous month in a seasonal business and calling it a trend; dividing by the current period.

### Q9 ⭐⭐⭐ 🟢 What is a ratio, and how is it different from a percentage and a fraction?
**Asked at:** commonly asked (no company-specific report found); basic number literacy, part of aptitude-style screening.
**What the interviewer is checking:** Whether you understand part-to-part versus part-to-whole.
**Say this in the interview:** "A ratio compares two quantities, like 3:2, and can be part-to-part. A fraction is a part of a whole, like 3/5. A percentage is a fraction out of 100. So the ratio 3:2 means fractions 3/5 and 2/5, or 60% and 40%."
**Explain simply:**
- Ratio: how one amount compares with another (men : women = 60 : 40, or 3 : 2).
- Fraction: part divided by the whole (60 of 100 = 3/5).
- Percentage: a fraction expressed per 100 (60%).
- A ratio can exceed 1 (1.5 : 1); a fraction of a whole cannot.
**Formula in plain words:** Ratio a:b has a total of a + b parts; each part's share = its number divided by (a + b).
**Worked example:** In a team of 100 there are 60 women and 40 men. Ratio women : men = 60 : 40 = 3 : 2 = 1.5 to 1. Fraction of women = 60/100 = 3/5. Percentage of women = 60%.
**Excel / Python:**
```python
# A team of 100 people: 60 women and 40 men
women = 60
men = 40
team_size = women + men

# Ratio of women to men (part to part)
ratio_women_to_men = women / men

# Fraction and percentage of women (part to whole)
fraction_women = women / team_size
percentage_women = fraction_women * 100

print("Women per man:", ratio_women_to_men)
print("Fraction women:", fraction_women)
print("Percentage women:", percentage_women)
```
```text
Women per man: 1.5
Fraction women: 0.6
Percentage women: 60.0
```
There are 1.5 women for every man, and women are 0.6 (60%) of the team.
Excel (not run in Excel here): women in B1, men in B2. `=B1/B2` returns 1.5; `=B1/(B1+B2)` returns 0.6.
**Likely follow-ups:** 1) *Convert 3:2 to numbers?* See Q23. 2) *Is "1.5 to 1" the same as 3:2?* Yes, same ratio.
**Common mistakes:** Treating 3:2 as 3/2 of the whole instead of 3/5; mixing up the order (men:women vs women:men).

### Q10 ⭐⭐⭐ 🟢 What is CAGR, and what is the formula?
**Asked at:** commonly asked (no company-specific report found); CAGR and its comparison with YoY and the arithmetic mean are a standard finance/consulting prep topic (PrepLounge).
**What the interviewer is checking:** Whether you can give the one smooth yearly growth rate that links a start and an end value.
**Say this in the interview:** "CAGR, the compound annual growth rate, is the constant yearly growth rate that would take you from the starting value to the ending value over a number of years. Formula: (ending value divided by starting value) to the power of one over the number of years, minus one."
**Explain simply:**
- It smooths uneven yearly growth into one steady rate, as if growth happened at the same rate every year.
- "Compound" means each year's growth builds on the previous year's larger base.
- The number of years is the gap between the dates (2021 to 2024 is 3 years, not 4).
- It ignores what happened in between, so it can hide volatility.
**Formula in plain words:** Divide the end value by the start value, take the n-th root (n = number of years), subtract 1. In symbols: CAGR = (End / Start)^(1/n) - 1.
**Worked example:** Headcount 100 growing to 150 in 3 years. 150/100 = 1.5. The cube root of 1.5 is 1.1447, so CAGR = 14.47% per year. Check: 100 x 1.1447^3 = 150.
**Excel / Python:**
```python
# Start value, end value and the number of years between them
starting_value = 100
ending_value = 150
number_of_years = 3

# Growth factor over the whole period
total_growth_factor = ending_value / starting_value

# Take the n-th root to get the yearly factor, then subtract 1
cagr = total_growth_factor ** (1 / number_of_years) - 1

# Check: grow the start value for 3 years at this rate
check_value = starting_value * (1 + cagr) ** number_of_years

print("CAGR (%):", round(cagr * 100, 2))
print("Check, should be 150:", round(check_value, 2))
```
```text
CAGR (%): 14.47
Check, should be 150: 150.0
```
Growing 14.47% every year for 3 years turns 100 into 150.
Excel (not run in Excel here): start in B1 (100), end in B2 (150), years in B3 (3). `=(B2/B1)^(1/B3)-1` returns 0.1447. `=RRI(B3,B1,B2)` gives the same (Excel 2013+).
**Likely follow-ups:** 1) *Why not average the yearly growth rates?* Q16 and Q32. 2) *Limitations?* Hides ups and downs; depends on the chosen start and end years; needs positive values.
**Common mistakes:** Using the number of data points (4) instead of years (3); forgetting to subtract 1.

### Q11 ⭐⭐⭐ 🟢 A price rises 20% and then falls 20%. Is it back to the original price?
**Asked at:** commonly asked (no company-specific report found); a classic successive-percentage puzzle (see Careers360 arithmetic shortcuts).
**What the interviewer is checking:** Whether you know percentage changes compound and use different bases.
**Say this in the interview:** "No. After the 20% rise the price is 120. A 20% fall is now 20% of 120, which is 24, so the price is 96. It ends 4% below the start."
**Explain simply:**
- The rise is calculated on the original (100); the fall is calculated on the new, higher price (120).
- So the fall removes more rupees than the rise added.
- Multiplying the factors: 1.20 x 0.80 = 0.96, a 4% net fall.
- To get back to 100 from 96 you would need a rise of 4.17%.
**Formula in plain words:** Final value = start x (1 + first change) x (1 + second change).
**Worked example:** A salary of 100 raised 20% to 120, then cut 20% gives 96, which is 4% less than the start.
**Excel / Python:**
```python
# Start at 100, rise by 20 percent, then fall by 20 percent
original_price = 100
price_after_rise = original_price * (1 + 0.20)
price_after_fall = price_after_rise * (1 - 0.20)

# Net change compared to the original
net_change_percent = (price_after_fall - original_price) / original_price * 100

print("After rise:", price_after_rise)
print("After fall:", price_after_fall)
print("Net change (%):", round(net_change_percent, 2))
```
```text
After rise: 120.0
After fall: 96.0
Net change (%): -4.0
```
The price ends at 96, a 4% net loss.
Excel (not run in Excel here): `=100*1.2*0.8` returns 96.
**Likely follow-ups:** 1) *What if it falls first, then rises 20%?* Same result: 0.8 x 1.2 = 0.96. 2) *What rise restores it?* Q12 style: 100/96 - 1 = 4.17%.
**Common mistakes:** Assuming +20% and -20% cancel out.

### Q12 ⭐⭐⭐ 🟢 Revenue fell from 500 to 400. By what percentage must it grow to return to 500?
**Asked at:** commonly asked (no company-specific report found); a standard base-effect puzzle.
**What the interviewer is checking:** Whether you switch the base to the new, lower value.
**Say this in the interview:** "The fall was 100 on a base of 500, so 20%. To recover, it must grow 100 on a base of 400, which is 25%."
**Explain simply:**
- Fall: (400 - 500) / 500 = -20%.
- Recovery: (500 - 400) / 400 = +25%.
- The same 100 gap is a bigger share of the smaller number.
- General rule: a fall of f needs a rise of f / (1 - f). A 50% fall needs a 100% rise.
**Formula in plain words:** Required growth = gap divided by the current (lower) value.
**Worked example:** Revenue 500 to 400 (-20%), then 400 x 1.25 = 500.
**Excel / Python:**
```python
# Revenue before and after the fall
original_revenue = 500
fallen_revenue = 400

# Percentage fall, based on the original revenue
percentage_fall = (fallen_revenue - original_revenue) / original_revenue * 100

# Percentage rise needed, based on the lower revenue
percentage_rise_needed = (original_revenue - fallen_revenue) / fallen_revenue * 100

# Check: grow the lower revenue by that percentage
revenue_after_recovery = fallen_revenue * (1 + percentage_rise_needed / 100)

print("Fall (%):", percentage_fall)
print("Rise needed (%):", percentage_rise_needed)
print("After recovery:", revenue_after_recovery)
```
```text
Fall (%): -20.0
Rise needed (%): 25.0
After recovery: 500.0
```
A 20% fall needs a 25% rise to get back to 500.
Excel (not run in Excel here): `=(500-400)/400` returns 0.25.
**Likely follow-ups:** 1) *A 50% fall needs what rise?* 100%. 2) *Why is this asymmetric?* Different bases.
**Common mistakes:** Answering 20%.

### Q13 ⭐⭐⭐ 🟢 How do you calculate a percentage of a total (share or contribution) in a table, and what should the shares add up to?
**Asked at:** commonly asked (no company-specific report found); a routine task in Excel and BI reporting.
**What the interviewer is checking:** Whether you divide each item by the grand total and check that shares add to 100%.
**Say this in the interview:** "Each item divided by the grand total gives its share. Shares should add up to 100%. If they show 99.9% or 100.1%, it is rounding, which I mention or fix."
**Explain simply:**
- Compute the grand total first (the sum of all parts).
- Each share = part / grand total, then format as a percentage.
- In Excel lock the total cell with dollar signs so it stays fixed when copied down.
- Rounded shares may not add to exactly 100%; that is a display issue, not an error (see Q46).
**Formula in plain words:** Share = this part divided by the total of all parts, times 100.
**Worked example:** Hires by region: North 120, South 80, East 50, West 50. Total 300. North = 40%, South = 26.7%, East = 16.7%, West = 16.7%. Rounded to one decimal they add to 100.1%.
**Excel / Python:**
```python
# Number of hires by region
hires_by_region = {"North": 120, "South": 80, "East": 50, "West": 50}

# Grand total of all hires
total_hires = sum(hires_by_region.values())

# Share of each region in the total
shares_in_percent = {}
for region, hires in hires_by_region.items():
    shares_in_percent[region] = hires / total_hires * 100

# Show each share rounded to one decimal, and the sum of the rounded values
rounded_shares = {}
for region, share in shares_in_percent.items():
    rounded_shares[region] = round(share, 1)

print("Total hires:", total_hires)
print("Rounded shares:", rounded_shares)
print("Sum of exact shares:", round(sum(shares_in_percent.values()), 6))
print("Sum of rounded shares:", round(sum(rounded_shares.values()), 1))
```
```text
Total hires: 300
Rounded shares: {'North': 40.0, 'South': 26.7, 'East': 16.7, 'West': 16.7}
Sum of exact shares: 100.0
Sum of rounded shares: 100.1
```
The exact shares add to exactly 100; the rounded ones add to 100.1 because of rounding.
Excel (not run in Excel here): regions in A2:A5, hires in B2:B5, total in B6 `=SUM(B2:B5)`. In C2 type `=B2/$B$6` and copy down; format as Percentage. `$B$6` stays locked.
**Likely follow-ups:** 1) *Why lock the total?* So every row divides by the same cell. 2) *What if shares add to 99.9%?* Rounding; adjust the largest item or note it.
**Common mistakes:** Forgetting the dollar signs; including the total row inside the sum.

### Q14 ⭐⭐⭐ 🟡 Explain weighted average to a non-technical manager using one example with numbers.
**Asked at:** commonly asked (no company-specific report found); tests communication as much as maths.
**What the interviewer is checking:** Whether you can explain it plainly, with a believable business example.
**Say this in the interview:** "Imagine a team of 8: six juniors earn 40,000 and two seniors earn 70,000. Averaging the two salary levels gives 55,000, but that is wrong because there are far more juniors. Counting each person once, the real average is 47,500. A weighted average means 'count each group in proportion to how many people it has'."
**Explain simply:**
- Plain average: treats every group equally.
- Weighted average: gives bigger groups a bigger say.
- Real-life comparison: your overall exam percentage when the final exam is worth more than the quiz.
- Check: the weighted average always lies between the lowest and highest group values, closer to the biggest group.
**Formula in plain words:** Add up (group value x group size), then divide by the total people.
**Worked example:** (6 x 40,000 + 2 x 70,000) / 8 = 380,000 / 8 = 47,500.
**Excel / Python:**
```python
# Two salary groups and how many people are in each
salary_per_group = [40000, 70000]
people_per_group = [6, 2]

# Wrong way: average the two group salaries
simple_average = sum(salary_per_group) / len(salary_per_group)

# Right way: total salary bill divided by total people
total_salary_bill = 6 * 40000 + 2 * 70000
total_people = sum(people_per_group)
weighted_average = total_salary_bill / total_people

print("Simple average:", simple_average)
print("Weighted average:", weighted_average)
```
```text
Simple average: 55000.0
Weighted average: 47500.0
```
The team's real average is 47,500; the simple average of 55,000 overstates it by 7,500.
Excel (2007+, not run in Excel here): salaries in B2:B3, people in C2:C3. `=SUMPRODUCT(B2:B3,C2:C3)/SUM(C2:C3)` returns 47500.
**Likely follow-ups:** 1) *What is the weight here?* Headcount. 2) *Another example?* Course grades with different credit weights.
**Common mistakes:** Using jargon with the manager; picking an example with equal group sizes (no difference shows).

### Q15 ⭐⭐⭐ 🟡 Headcount is 250 and 30 people left during the year with 20 joiners. Calculate the attrition rate and explain your headcount choice.
**Asked at:** commonly asked (no company-specific report found); the formula follows HR glossaries (Kredily, Intervue).
**What the interviewer is checking:** Whether you notice the ambiguity ("headcount 250" at which date?) and choose the average headcount.
**Say this in the interview:** "I assume 250 is the opening headcount. With 30 leavers and 20 joiners, closing headcount is 240, so average headcount is 245. Attrition = 30 / 245 = 12.24%. I would state that assumption, since the question does not say whether 250 is the opening number."
**Explain simply:**
- The question is ambiguous: 250 could be opening, closing or average. I assume opening, the most natural reading, and say so.
- Closing headcount = 250 - 30 + 20 = 240.
- Average headcount = (250 + 240) / 2 = 245.
- Attrition rate = 30 / 245 = 12.24%.
- Joiners are not in the numerator: they change the headcount, they are not leavers.
- If the interviewer meant 250 as average, the answer is 30 / 250 = 12%.
**Formula in plain words:** Attrition = leavers divided by average headcount, times 100.
**Worked example:** Under the stated assumption: 12.24%. Using opening only: 12%. Using closing only: 12.5%. The differences are small here because the headcount barely moved.
**Excel / Python:**
```python
# Facts from the question (assuming 250 is the opening headcount)
opening_headcount = 250
employees_who_left = 30
new_joiners = 20

# Closing headcount after leavers and joiners
closing_headcount = opening_headcount - employees_who_left + new_joiners

# Average of opening and closing
average_headcount = (opening_headcount + closing_headcount) / 2

# Attrition rate on the average headcount
attrition_rate = employees_who_left / average_headcount * 100

print("Closing headcount:", closing_headcount)
print("Average headcount:", average_headcount)
print("Attrition rate (%):", round(attrition_rate, 2))
```
```text
Closing headcount: 240
Average headcount: 245.0
Attrition rate (%): 12.24
```
About 12.2% of the workforce left during the year.
Excel (not run in Excel here): opening in B1 (250), leavers B2 (30), joiners B3 (20). Closing in B4 `=B1-B2+B3`; attrition `=B2/AVERAGE(B1,B4)` returns 0.1224.
**Likely follow-ups:** 1) *Would joiners change the answer?* Only through the average headcount. 2) *What if 250 was closing?* Opening would be 260, average 255, attrition 11.76%.
**Common mistakes:** Adding joiners to the leavers; not stating the headcount assumption.

### Q16 ⭐⭐⭐ 🟡 Revenue was 100 in 2021 and 150 in 2024. Calculate CAGR and compare it with the simple average of the yearly growth rates.
**Asked at:** commonly asked (no company-specific report found); CAGR vs arithmetic mean is a standard comparison in finance prep (PrepLounge).
**What the interviewer is checking:** Whether you know the arithmetic mean of growth rates overstates the true compound rate, and that the yearly path is not given.
**Say this in the interview:** "CAGR over 3 years is (150/100) to the power of one third, minus 1, which is 14.47%. The question does not give the middle years, so a simple average of yearly rates depends on the path; for any uneven path it comes out higher than the CAGR, for example about 14.9% for one path. Only the CAGR is certain."
**Explain simply:**
- 2021 to 2024 is 3 years, so n = 3.
- CAGR = 1.5^(1/3) - 1 = 14.47%.
- The yearly growth rates in between are not given, so I assume a path to compare. Premise note: this cannot be answered uniquely without that path.
- The arithmetic mean of yearly rates is always at least the CAGR, and only equal when every year grows by exactly the same percentage.
- Reason: growth compounds, so a big year after a small one, or the reverse, makes the simple average look better than the real result.
**Formula in plain words:** CAGR = (end / start) to the power 1/n, minus 1. Simple average of growth = add the yearly rates and divide by their count.
**Worked example:** Path A: 100, 130, 140, 150 gives yearly rates 30%, 7.69%, 7.14%, with an average of about 14.94%. Path B: 100, 120, 135, 150 gives 20%, 12.5%, 11.11%, average 14.54%. Path C: 100, 105, 115, 150 gives about 5%, 9.52%, 30.43%, average about 14.98%. CAGR is 14.47% in all three; the simple average is always higher.
**Excel / Python:**
```python
# Revenue at the start and end, and the years between them
revenue_2021 = 100
revenue_2024 = 150
number_of_years = 3

# CAGR: one steady yearly rate that links start and end
cagr = (revenue_2024 / revenue_2021) ** (1 / number_of_years) - 1
print("CAGR (%):", round(cagr * 100, 2))

# Three possible revenue paths that all end at 150 (middle years are assumed)
possible_paths = [[100, 130, 140, 150], [100, 120, 135, 150], [100, 105, 115, 150]]

for path in possible_paths:
    # Yearly growth rates for this path
    yearly_growth_rates = []
    for year in range(1, len(path)):
        previous_revenue = path[year - 1]
        current_revenue = path[year]
        rate = (current_revenue - previous_revenue) / previous_revenue * 100
        yearly_growth_rates.append(round(rate, 2))

    # Simple average of those rates
    simple_average_growth = sum(yearly_growth_rates) / len(yearly_growth_rates)
    print(path, yearly_growth_rates, "average:", round(simple_average_growth, 2))
```
```text
CAGR (%): 14.47
[100, 130, 140, 150] [30.0, 7.69, 7.14] average: 14.94
[100, 120, 135, 150] [20.0, 12.5, 11.11] average: 14.54
[100, 105, 115, 150] [5.0, 9.52, 30.43] average: 14.98
```
Every path has the same 14.47% CAGR but a different, higher simple average; only the CAGR matches the real result.
Excel (not run in Excel here): `=(150/100)^(1/3)-1` returns 0.1447; `=RRI(3,100,150)` (Excel 2013+) is the same. For a path in B2:B5 with growth rates in C3:C5, `=AVERAGE(C3:C5)` is the simple average.
**Likely follow-ups:** 1) *Why is the arithmetic mean higher?* Compounding (the AM-GM inequality). 2) *When are they equal?* When every year grows by the same rate.
**Common mistakes:** Using 4 years instead of 3; presenting the simple average of rates as "the growth rate".

### Q17 ⭐⭐ 🟢 What does it mean to say a metric is up "15% vs last year"? What can go wrong with this comparison?
**Asked at:** commonly asked (no company-specific report found); year-on-year (YoY) base-period pitfalls appear in practice-platform questions (Dataford, besthub; search snippets only).
**What the interviewer is checking:** Whether you can state the formula and spot a misleading baseline.
**Say this in the interview:** "It means this year's value is 15% higher than last year's value, so last year is the base. Before I trust it I check the base, the period, and whether the two years are like for like."
**Explain simply:**
- **YoY (year over year)** compares one period with the same period a year earlier.
- **Base effect:** if last year was unusually low, a big percentage is easy to get. Always say what the base was.
- **Not like for like:** a different number of months, seasonality (hiring peaks in April), a changed definition, or a bigger company.
- **Percent vs absolute:** 15% of a tiny number may be 3 people. Show both.
**Formula in plain words:** (this year minus last year) divided by last year, times 100. (New - Old) / Old x 100.
**Worked example:** Hires were 200 in 2022, 100 in 2023, 115 in 2024. "Up 15% vs last year" is true, yet 2024 is still 42.5% below 2022.
**Excel / Python:**
```python
# Hires in three years
hires_2022 = 200
hires_2023 = 100
hires_2024 = 115

# Percentage change versus the previous year
change_2023 = (hires_2023 - hires_2022) / hires_2022 * 100
change_2024 = (hires_2024 - hires_2023) / hires_2023 * 100

# Percentage change versus two years ago
change_vs_2022 = (hires_2024 - hires_2022) / hires_2022 * 100

print(change_2023, change_2024, change_vs_2022)
```
```text
-50.0 15.0 -42.5
```
The 15% is real, but it is a recovery from a 50% fall, not growth beyond the old level.
**Likely follow-ups:** 1) *What if last year was zero?* The percentage is undefined; report the absolute number. 2) *Which comparison fixes seasonality?* Same month last year, not the previous month.
**Common mistakes:** Quoting the percentage without the base; comparing a part year with a full year.

### Q18 ⭐⭐ 🟢 What are the main ways to express an average (mean, median, weighted)? Which would you use for average salary and why?
**Asked at:** commonly asked (no company-specific report found); simple vs weighted average is covered in generic analytics prep (Fuse Academics, snippet only).
**What the interviewer is checking:** Whether you know that one outlier can distort the mean.
**Say this in the interview:** "Mean is total divided by count, median is the middle value, weighted mean gives each group its proper size. For salary I report the median because a few very high salaries pull the mean up, and I use a weighted mean when I combine groups of different sizes."
**Explain simply:**
- **Mean:** add everything, divide by how many.
- **Median:** sort the values, take the middle one; not moved by extreme values.
- **Weighted mean:** each value counts according to its weight, such as headcount.
- Salary data is usually skewed (a few very high pay packets), so the median describes the "typical" employee better.
**Formula in plain words:** Weighted mean = sum of (value x weight) divided by sum of weights.
**Worked example:** Nine monthly salaries include one at 400,000. The mean is 79,111 but the median is 40,000; eight of nine people earn less than the mean.
**Excel / Python:**
```python
import statistics

# Monthly salaries of 9 people, the last one is a senior outlier
monthly_salaries = [30000, 32000, 35000, 38000, 40000, 42000, 45000, 50000, 400000]

# Mean: total divided by count
mean_salary = statistics.mean(monthly_salaries)

# Median: the middle value after sorting
median_salary = statistics.median(monthly_salaries)

print(round(mean_salary), median_salary)
```
```text
79111 40000
```
The single large salary drags the mean far above what most people earn. Excel (layout: salaries in B2:B10): `=AVERAGE(B2:B10)` returns 79111.11 and `=MEDIAN(B2:B10)` returns 40000 (not run in Excel here; both work in every Excel version).
**Likely follow-ups:** 1) *When is the mean fine?* When data is roughly symmetric, such as engagement scores. 2) *What is the mode?* The most common value.
**Common mistakes:** Reporting the mean for skewed pay; averaging group averages without weights (Q25).

### Q19 ⭐⭐ 🟢 How do you calculate conversion rate, and what is the denominator?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you pick the right "who could have converted" group.
**Say this in the interview:** "Conversion rate is the number who completed the step divided by the number who were eligible to complete it. The denominator is the starting group for that step, and I always say which one I used."
**Explain simply:**
- Numerator: people who did the action (joined).
- Denominator: people who had the chance (applicants, or offered candidates).
- Different denominators give different, equally valid rates, so label them.
**Formula in plain words:** Conversion rate = people who completed the step / people who entered the step x 100.
**Worked example:** 1,000 applicants, 50 offers, 40 joined. Applicant-to-joiner is 4%; offer acceptance (offered-to-joined) is 80%.
**Excel / Python:**
```python
# Counts from the hiring process
applicants = 1000
offers = 50
joined = 40

# Overall conversion: joiners out of all applicants
overall_conversion = joined / applicants * 100

# Offer acceptance: joiners out of those who got an offer
offer_acceptance = joined / offers * 100

print(overall_conversion, offer_acceptance)
```
```text
4.0 80.0
```
Same 40 joiners, two different rates, because the denominator changed. Excel: with joined in B2 and applicants in B3, `=B2/B3` formatted as percentage.
**Likely follow-ups:** 1) *Should the denominator include people still in process?* Better to use a fixed cohort so unfinished cases do not lower the rate. 2) *What if the denominator is zero?* Show blank, not 0%.
**Common mistakes:** Using the wrong denominator (all employees instead of applicants); mixing cohorts from different months.

### Q20 ⭐⭐ 🟢 The hiring funnel has 1,000 applicants, 200 interviewed, 50 offered and 40 joined. Calculate the conversion at each stage and overall.
**Asked at:** commonly asked (no company-specific report found); funnel maths is a standard analytics exercise.
**What the interviewer is checking:** Stage-by-stage division and the link between stage and overall rates.
**Say this in the interview:** "Each stage rate is the next count divided by the previous count: 20%, 25%, 80%. Overall is 40 out of 1,000, which is 4%, and it equals the product of the stage rates."
**Explain simply:**
- Each stage uses the previous stage as its denominator.
- Overall conversion uses the very first stage.
- Stage rates multiply to the overall rate: 0.20 x 0.25 x 0.80 = 0.04.
- The weakest step to improve is interview-to-offer at 25%, or applicant screening at 20%.
**Formula in plain words:** Stage conversion = this stage count / previous stage count x 100.
**Worked example:** Applied to Interviewed 20%, Interviewed to Offered 25%, Offered to Joined 80%, overall 4%.
**Excel / Python:**
```python
# Funnel stages in order with their counts
stages = [("Applied", 1000), ("Interviewed", 200), ("Offered", 50), ("Joined", 40)]

# Conversion from each stage to the next
for position in range(1, len(stages)):
    previous_name, previous_count = stages[position - 1]
    current_name, current_count = stages[position]
    stage_conversion = current_count / previous_count * 100
    print(previous_name, "to", current_name, stage_conversion)

# Overall conversion: last stage over first stage
overall_conversion = stages[-1][1] / stages[0][1] * 100
print("Overall", overall_conversion)
```
```text
Applied to Interviewed 20.0
Interviewed to Offered 25.0
Offered to Joined 80.0
Overall 4.0
```
Excel: counts in B2:B5; in C3 enter `=B3/B2`, copy down to C5; overall is `=B5/B2` (not run in Excel here).
**Likely follow-ups:** 1) *Which stage would you fix first?* The biggest drop that you can influence, with cost in mind. 2) *Why do the rates multiply?* Each is a fraction of the previous group.
**Common mistakes:** Dividing every stage by 1,000; adding the stage percentages.

### Q21 ⭐⭐ 🟢 How do you calculate a percentage of a percentage (e.g. 20% of the 30% who responded)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Multiplying fractions, and knowing what the result is a percentage of.
**Say this in the interview:** "Multiply them: 20% of 30% is 0.20 x 0.30 = 0.06, so 6% of the original group. I always state what the 6% is out of."
**Explain simply:**
- Turn each percentage into a decimal, then multiply.
- The answer is a share of the original total, not of the 30%.
- It is not 20% + 30% and not 50%.
**Formula in plain words:** Part of a part = first rate x second rate.
**Worked example:** An engagement survey goes to 500 employees; 30% respond (150). Of those, 20% (30 people) report low engagement. That is 6% of all 500.
**Excel / Python:**
```python
# Survey sent to 500 employees
total_employees = 500
response_rate = 0.30
low_engagement_share = 0.20

# People who responded
responders = total_employees * response_rate

# Responders who report low engagement
low_engagement_people = responders * low_engagement_share

# Share of all employees
share_of_everyone = response_rate * low_engagement_share * 100

print(responders, low_engagement_people, share_of_everyone)
```
```text
150.0 30.0 6.0
```
30 people is 20% of the 150 responders and 6% of all 500 employees. Excel: `=500*0.3*0.2` returns 30.
**Likely follow-ups:** 1) *Can the low-engagement group be generalized to all 500?* Only if responders resemble non-responders. 2) *Percent vs percentage point?* 6% is a share; a move from 30% to 36% is 6 percentage points.
**Common mistakes:** Reporting 6% as "of responders"; adding the percentages.

### Q22 ⭐⭐ 🟢 What is the difference between mean of ratios and ratio of sums?
**Asked at:** commonly asked (no company-specific report found); averaging ratios is flagged as a pitfall in an HR trade article (HR Exchange Network, snippet only).
**What the interviewer is checking:** Whether you avoid averaging percentages from groups of different sizes.
**Say this in the interview:** "Mean of ratios averages each group's percentage and treats every group equally. Ratio of sums adds the numerators and denominators first, so bigger groups count more. For company-wide attrition I use the ratio of sums."
**Explain simply:**
- Mean of ratios: (ratio A + ratio B + ratio C) / 3.
- Ratio of sums: (all leavers) / (all headcount).
- They agree only when all groups are the same size.
- The ratio of sums is the true overall rate.
**Formula in plain words:** Ratio of sums = total numerator / total denominator.
**Worked example:** Departments: 5 leavers of 50, 2 of 10, 30 of 300. The mean of ratios is 13.33%; the ratio of sums is 37/360 = 10.28%. The small department with 20% inflated the first figure.
**Excel / Python:**
```python
# Leavers and headcount for three departments
leavers = [5, 2, 30]
headcount = [50, 10, 300]

# Attrition ratio of each department
department_ratios = []
for department_leavers, department_headcount in zip(leavers, headcount):
    department_ratios.append(department_leavers / department_headcount)

# Mean of ratios: simple average of the three percentages
mean_of_ratios = sum(department_ratios) / len(department_ratios) * 100

# Ratio of sums: total leavers over total headcount
ratio_of_sums = sum(leavers) / sum(headcount) * 100

print(round(mean_of_ratios, 2), round(ratio_of_sums, 2))
```
```text
13.33 10.28
```
The honest company figure is 10.28%. Excel: leavers in B2:B4, headcount in C2:C4: `=SUM(B2:B4)/SUM(C2:C4)` (not run in Excel here).
**Likely follow-ups:** 1) *When is mean of ratios right?* When each group matters equally, such as "the typical department". 2) *Name the related trap.* Simpson's paradox: group trends can flip when combined.
**Common mistakes:** `=AVERAGE` of a percentage column; reporting the result without saying which method.

### Q23 ⭐⭐ 🟢 How do you convert a ratio such as 3:2 into percentages and into actual numbers for a total of 500?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic ratio parts arithmetic.
**Say this in the interview:** "Add the parts: 3 + 2 = 5. Each part is 3/5 = 60% and 2/5 = 40%. For 500 people, one part is 100, so the groups are 300 and 200."
**Explain simply:**
- Total parts = sum of the ratio numbers.
- Percentage of a group = its parts / total parts.
- Actual number = total x its share.
- Example: a 3:2 ratio of full-time to contract staff.
**Formula in plain words:** Group size = total x (group's parts / all parts).
**Worked example:** 500 employees, full-time:contract = 3:2 gives 60% and 40%, so 300 full-time and 200 contract.
**Excel / Python:**
```python
# Ratio parts and total headcount
full_time_parts = 3
contract_parts = 2
total_headcount = 500

# Total parts in the ratio
total_parts = full_time_parts + contract_parts

# Percentage share of each group
full_time_percent = full_time_parts / total_parts * 100
contract_percent = contract_parts / total_parts * 100

# Actual head counts
full_time_people = total_headcount * full_time_parts / total_parts
contract_people = total_headcount * contract_parts / total_parts

print(full_time_percent, contract_percent, full_time_people, contract_people)
```
```text
60.0 40.0 300.0 200.0
```
Excel: `=500*3/(3+2)` returns 300.
**Likely follow-ups:** 1) *Is 3:2 the same as 3/2?* No; 3/2 compares the groups (1.5 times), 3:2 splits a whole. 2) *Three-part ratio?* Same method with three parts.
**Common mistakes:** Dividing by 2 (the other part) instead of 5 (all parts).

### Q24 ⭐⭐ 🟢 Salary increased 10% in year one and 8% in year two. What is the total increase, and why is it not 18%?
**Asked at:** commonly asked (no company-specific report found); successive percentage changes are a standard aptitude topic (Careers360, snippet only).
**What the interviewer is checking:** Whether you know that percentages chain by multiplication.
**Say this in the interview:** "Multiply the growth factors: 1.10 x 1.08 = 1.188, a total rise of 18.8%. Year two's 8% applies to the already higher salary, so it adds a little extra, 0.8%."
**Explain simply:**
- Each percentage uses a different base: year two's base is the new salary.
- Total = (1 + 10%) x (1 + 8%) - 1.
- Extra over 18% is 10% x 8% = 0.8%, the "growth on growth".
**Formula in plain words:** Total change = (factor one x factor two) - 1.
**Worked example:** Salary of 50,000 becomes 55,000, then 59,400. Increase = 9,400, which is 18.8%, not 9,000 (18%).
**Excel / Python:**
```python
# Starting salary and the two raises
starting_salary = 50000
year_one_raise = 0.10
year_two_raise = 0.08

# Apply raise one, then raise two on the new salary
salary_after_year_one = starting_salary * (1 + year_one_raise)
salary_after_year_two = salary_after_year_one * (1 + year_two_raise)

# Total percentage increase
total_increase_percent = (salary_after_year_two / starting_salary - 1) * 100

print(round(salary_after_year_one), round(salary_after_year_two), round(total_increase_percent, 1))
```
```text
55000 59400 18.8
```
Excel: `=50000*1.1*1.08` returns 59400.
**Likely follow-ups:** 1) *10% rise then 10% cut?* 100 to 110 to 99, a net 1% fall. 2) *Average yearly rate?* Use the geometric mean (Q32).
**Common mistakes:** Adding percentages; applying the second raise to the original salary.

### Q25 ⭐⭐ 🟢 How do you calculate average salary for a department with different headcounts per grade?
**Asked at:** commonly asked (no company-specific report found); weighted vs simple average is standard (Fuse Academics, snippet only).
**What the interviewer is checking:** Weighted average using headcount as weights.
**Say this in the interview:** "I multiply each grade's average salary by its headcount, add those up, and divide by total headcount. A simple average of the four grade averages would treat 5 directors like 40 juniors."
**Explain simply:**
- Weight = how many people sit behind each average.
- Total pay = sum of (average x headcount); then divide by total people.
- The weighted answer equals the average of all 80 individual salaries.
**Formula in plain words:** Weighted average = sum of (grade average x grade headcount) / total headcount.
**Worked example:** Grades G1 to G4 have 40, 25, 10, 5 people earning 30,000, 50,000, 90,000, 150,000 on average. Total pay is 4,100,000 for 80 people: 51,250. The unweighted mean is 80,000, which overstates.
**Excel / Python:**
```python
# Headcount and average salary per grade
grade_headcount = [40, 25, 10, 5]
grade_average_salary = [30000, 50000, 90000, 150000]

# Total salary bill: average times headcount for each grade
total_salary_bill = 0
for headcount, average_salary in zip(grade_headcount, grade_average_salary):
    total_salary_bill = total_salary_bill + headcount * average_salary

# Divide by total number of people
total_people = sum(grade_headcount)
weighted_average = total_salary_bill / total_people

# Unweighted average of the four grade averages (misleading)
unweighted_average = sum(grade_average_salary) / len(grade_average_salary)

print(total_salary_bill, total_people, weighted_average, unweighted_average)
```
```text
4100000 80 51250.0 80000.0
```
Excel (headcount in B2:B5, average salary in C2:C5): `=SUMPRODUCT(B2:B5,C2:C5)/SUM(B2:B5)` returns 51250 (SUMPRODUCT works in all versions; not run in Excel here).
**Likely follow-ups:** 1) *Why not AVERAGE of C2:C5?* It ignores group size. 2) *Weights other than headcount?* Hours worked or FTE.
**Common mistakes:** Averaging the averages; weights that do not match the data being averaged.

### Q26 ⭐⭐ 🟢 How do you calculate the percentage difference between two values where neither is the baseline?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness that percentage change needs a baseline, and the symmetric alternative.
**Say this in the interview:** "When neither is the baseline, I divide the gap by the average of the two values. That gives the same answer whichever way round I compare, unlike percentage change, which depends on the base."
**Explain simply:**
- Percentage change picks one value as the base, so A vs B differs from B vs A.
- Symmetric percentage difference uses the midpoint as base.
- Alternatively, name a baseline (such as the company average) and use ordinary percentage change.
**Formula in plain words:** Difference / average of the two x 100; that is |A - B| / ((A + B) / 2) x 100.
**Worked example:** Average salary is 52,000 in Pune and 60,000 in Chennai. Symmetric difference is 14.29%. Using Pune as base gives 15.38%; using Chennai gives 13.33%.
**Excel / Python:**
```python
# Average salaries in two offices
pune_salary = 52000
chennai_salary = 60000

# Gap between them
salary_gap = abs(chennai_salary - pune_salary)

# Symmetric difference: gap over the midpoint
midpoint = (pune_salary + chennai_salary) / 2
symmetric_difference = salary_gap / midpoint * 100

# Ordinary percentage change with each office as the base
change_from_pune = (chennai_salary - pune_salary) / pune_salary * 100
change_from_chennai = (pune_salary - chennai_salary) / chennai_salary * 100

print(round(symmetric_difference, 2), round(change_from_pune, 2), round(change_from_chennai, 2))
```
```text
14.29 15.38 -13.33
```
The symmetric figure sits between the two baseline-dependent ones. Excel (values in B1 and B2): `=ABS(B1-B2)/AVERAGE(B1,B2)` (not run in Excel here).
**Likely follow-ups:** 1) *Which do you report?* State the formula; with a clear "before", use ordinary percentage change. 2) *Percent vs percentage point?* Points are the arithmetic gap of two percentages.
**Common mistakes:** Silently picking a base; mixing up percent and percentage points.

### Q27 ⭐⭐ 🟢 What is the difference between percentage change and percentage of total?
**Asked at:** commonly asked (no company-specific report found); percentage change is a live "calculate" task on practice platforms (Dataford, snippet only).
**What the interviewer is checking:** Whether you separate growth over time from share at one moment.
**Say this in the interview:** "Percentage change compares the same thing across two times. Percentage of total compares a part with the whole at one time. One tells growth, the other tells mix."
**Explain simply:**
- Percentage change needs two periods; percentage of total needs one period and a total.
- Shares add up to 100%; changes do not.
- A department can have a large share but a falling headcount.
**Formula in plain words:** Change = (now - before) / before x 100. Share = part / total x 100.
**Worked example:** Headcount now (last year): Sales 120 (100), Ops 200 (210), HR 30 (30), IT 50 (40); total 400. Ops is 50% of the company yet shrank 4.76%; IT is only 12.5% of staff but grew 25%.
**Excel / Python:**
```python
# Headcount this year and last year by department
headcount_now = {"Sales": 120, "Ops": 200, "HR": 30, "IT": 50}
headcount_last_year = {"Sales": 100, "Ops": 210, "HR": 30, "IT": 40}

# Company total this year
company_total = sum(headcount_now.values())

for department in headcount_now:
    # Share of the whole at one point in time
    share_of_total = headcount_now[department] / company_total * 100
    # Growth versus last year
    change = (headcount_now[department] - headcount_last_year[department]) / headcount_last_year[department] * 100
    print(department, round(share_of_total, 1), round(change, 2))
```
```text
Sales 30.0 20.0
Ops 50.0 -4.76
HR 7.5 0.0
IT 12.5 25.0
```
Read each row as: share of company, then growth. Excel: share `=B2/SUM($B$2:$B$5)`, change `=(B2-C2)/C2` (not run in Excel here).
**Likely follow-ups:** 1) *Contribution to growth?* A department's change divided by the company's total change. 2) *Can shares change with no one joining?* Yes, if others shrink.
**Common mistakes:** Calling a share "growth"; forgetting the absolute reference on the total.

### Q28 ⭐⭐ 🟢 How do you calculate the rate of absenteeism and the average attendance for a team?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Choosing the right denominator (scheduled days) for an HR metric.
**Say this in the interview:** "Absenteeism rate is absent days divided by total scheduled working days for the team. Attendance rate is the rest, 100 minus that, and average attendance per person is days present divided by team size."
**Explain simply:**
- Scheduled days = team size x working days in the period; do not count approved holidays as working days if your policy excludes them (state your definition).
- Absenteeism and attendance always add up to 100%.
- Define whether approved leave counts as absence.
**Formula in plain words:** Absenteeism % = days absent / (employees x working days) x 100.
**Worked example:** Team of 5, 22 working days = 110 scheduled days. Absences 2, 0, 1, 4, 0 = 7 days. Absenteeism 6.36%, attendance 93.64%, an average of 20.6 days present per person.
**Excel / Python:**
```python
# Team details for one month
team_size = 5
working_days = 22
days_absent_per_person = [2, 0, 1, 4, 0]

# Total days the team was expected to work
scheduled_days = team_size * working_days

# Total days lost
total_days_absent = sum(days_absent_per_person)

# Rates
absenteeism_rate = total_days_absent / scheduled_days * 100
attendance_rate = 100 - absenteeism_rate

# Average days present per person
days_present = scheduled_days - total_days_absent
average_days_present = days_present / team_size

print(scheduled_days, total_days_absent, round(absenteeism_rate, 2), round(attendance_rate, 2), average_days_present)
```
```text
110 7 6.36 93.64 20.6
```
Excel (absences in B2:B6, 22 days in E1): `=SUM(B2:B6)/(COUNT(B2:B6)*E1)` returns 0.0636 (not run in Excel here).
**Likely follow-ups:** 1) *Does it differ from attrition?* Yes, absence is days off, attrition is people leaving. 2) *Part-timers?* Use their scheduled days, not 22.
**Common mistakes:** Dividing by calendar days; not defining whether approved leave counts.

### Q29 ⭐⭐ 🟡 Average salary of 20 men is 50,000 and of 30 women is 40,000. What is the overall average?
**Asked at:** commonly asked (no company-specific report found); a standard weighted-average aptitude question.
**What the interviewer is checking:** Weighted average instead of the easy (50,000 + 40,000) / 2.
**Say this in the interview:** "It is 44,000. I weight by headcount: (20 x 50,000 + 30 x 40,000) / 50. The simple 45,000 is wrong because there are more women, so the answer must lean toward 40,000."
**Explain simply:**
- Total pay of men: 1,000,000. Of women: 1,200,000. Combined 2,200,000 for 50 people.
- Overall average sits closer to the larger group's average.
- Quick check: the answer must be between 40,000 and 50,000, and nearer 40,000.
**Formula in plain words:** (count A x average A + count B x average B) / (count A + count B).
**Worked example:** 2,200,000 / 50 = 44,000.
**Excel / Python:**
```python
# Group sizes and group averages
men_count = 20
men_average = 50000
women_count = 30
women_average = 40000

# Total pay of each group
men_total = men_count * men_average
women_total = women_count * women_average

# Overall average: all pay divided by all people
overall_average = (men_total + women_total) / (men_count + women_count)

# The wrong shortcut
simple_average = (men_average + women_average) / 2

print(men_total, women_total, overall_average, simple_average)
```
```text
1000000 1200000 44000.0 45000.0
```
The weighted answer is 44,000; the shortcut gives 45,000. Excel: `=(20*50000+30*40000)/50`.
**Likely follow-ups:** 1) *What would make it 45,000?* Equal group sizes. 2) *Does this show a pay gap?* The averages differ by 10,000, but grade mix must be checked first.
**Common mistakes:** Taking the simple midpoint.

### Q30 ⭐⭐ 🟡 You were asked to report average rating per store; which is better, average of store averages or pooled average? Explain.
**Asked at:** commonly asked (no company-specific report found); store order-value averages are used as an example in a data analytics textbook (Fuse Academics, snippet only).
**What the interviewer is checking:** Whether you tie the method to the business question and spot weighting.
**Say this in the interview:** "It depends on the question. If we ask how customers rate us overall, I use the pooled average, which weights every rating equally. If we want how a typical store performs, I use the average of store averages. I would state which one I used and ask what the stakeholder needs."
**Explain simply:**
- **Pooled average:** all ratings added, divided by number of ratings; busy stores count more.
- **Average of store averages:** each store counts once, whatever its size.
- Averages built on few ratings are unreliable; show the number of ratings next to each store.
- The wording "average rating per store" suggests a per-store figure, so the ambiguity is worth clarifying.
**Formula in plain words:** Pooled = sum of all ratings / number of ratings = weighted mean of store averages using rating counts.
**Worked example:** Store A 4.5 (10 ratings), B 3.8 (200), C 4.2 (40). Average of averages 4.17; pooled 3.89 (973 rating points over 250 ratings). The pooled figure is lower because big store B is weaker.
**Excel / Python:**
```python
# Average rating and number of ratings per store
store_average_ratings = [4.5, 3.8, 4.2]
store_rating_counts = [10, 200, 40]

# Average of store averages: every store counts once
average_of_averages = sum(store_average_ratings) / len(store_average_ratings)

# Pooled average: total rating points over total ratings
total_rating_points = 0
for average_rating, rating_count in zip(store_average_ratings, store_rating_counts):
    total_rating_points = total_rating_points + average_rating * rating_count
pooled_average = total_rating_points / sum(store_rating_counts)

print(round(average_of_averages, 2), round(pooled_average, 2), round(total_rating_points), sum(store_rating_counts))
```
```text
4.17 3.89 973 250
```
Both are valid but answer different questions. Excel: `=SUMPRODUCT(B2:B4,C2:C4)/SUM(C2:C4)` for pooled (not run in Excel here).
**Likely follow-ups:** 1) *What if a store has 2 ratings?* Flag low sample size. 2) *Equivalent HR case?* Engagement score per team vs company-wide.
**Common mistakes:** Averaging averages by default; hiding the rating counts.

### Q31 ⭐⭐ 🟡 What is compound growth, and how does it differ from simple growth?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand growth on growth.
**Say this in the interview:** "Simple growth adds the same amount every period, based on the original value. Compound growth applies the rate to the latest value, so the increase itself grows. Over several years compound pulls ahead."
**Explain simply:**
- Simple: start x (1 + rate x years).
- Compound: start x (1 + rate) ^ years.
- Year one is identical; the gap widens each year.
- Headcount, revenue and salary with annual percentage hikes compound.
**Formula in plain words:** Compound value = starting value x (1 + rate) raised to the number of years.
**Worked example:** Payroll of 100,000 growing 10% a year for 5 years: simple gives 150,000; compound gives 161,051.
**Excel / Python:**
```python
# Payroll of 100,000 growing 10% a year
starting_payroll = 100000
yearly_rate = 0.10

simple_value = starting_payroll
compound_value = starting_payroll

for year in range(1, 6):
    # Simple: add the same fixed amount each year
    simple_value = simple_value + starting_payroll * yearly_rate
    # Compound: grow the latest value
    compound_value = compound_value * (1 + yearly_rate)
    print(year, round(simple_value), round(compound_value))
```
```text
1 110000 110000
2 120000 121000
3 130000 133100
4 140000 146410
5 150000 161051
```
Excel: `=100000*(1+10%)^5` returns 161051 (not run in Excel here).
**Likely follow-ups:** 1) *Rule of 72?* Years to double is roughly 72 divided by the percentage rate. 2) *Does it work for decline?* Yes, with a negative rate.
**Common mistakes:** Multiplying the rate by years for compound; using the original base each year.

### Q32 ⭐⭐ 🟡 How do you calculate the average growth rate over several years, and why is the arithmetic mean of growth rates misleading?
**Asked at:** commonly asked (no company-specific report found); CAGR and geometric vs arithmetic mean appear in consulting prep (PrepLounge, snippet only).
**What the interviewer is checking:** Whether you use the geometric mean (CAGR) for growth.
**Say this in the interview:** "The right average is CAGR: (end / start) to the power of 1 over the number of years, minus 1. The plain average of yearly rates ignores compounding and overstates growth when rates swing."
**Explain simply:**
- CAGR (compound annual growth rate) is the single steady rate that gets you from start to end.
- Arithmetic mean of rates: +50% then -50% averages 0%, but 100 becomes 75.
- The more volatile the rates, the bigger the gap.
**Formula in plain words:** CAGR = (ending value / starting value) ^ (1 / number of years) - 1.
**Worked example:** Revenue 100, 150, 120, 180 (3 years). Yearly growth is +50%, -20%, +50%. Arithmetic mean 26.67% would imply 203.2 at the end; actual end is 180. CAGR is 21.64%, which reproduces 180.
**Excel / Python:**
```python
# Revenue at the end of each year
revenue = [100, 150, 120, 180]

# Growth rate of each year versus the previous year
yearly_growth = []
for year in range(1, len(revenue)):
    growth = revenue[year] / revenue[year - 1] - 1
    yearly_growth.append(growth)

# Misleading plain average of the rates
arithmetic_mean = sum(yearly_growth) / len(yearly_growth)

# CAGR: steady rate from start to end
number_of_years = len(revenue) - 1
cagr = (revenue[-1] / revenue[0]) ** (1 / number_of_years) - 1

# Check: what each average rate would give after 3 years
end_with_arithmetic = revenue[0] * (1 + arithmetic_mean) ** number_of_years
end_with_cagr = revenue[0] * (1 + cagr) ** number_of_years

print([round(growth * 100, 2) for growth in yearly_growth])
print(round(arithmetic_mean * 100, 2), round(cagr * 100, 2))
print(round(end_with_arithmetic, 1), round(end_with_cagr, 1))
```
```text
[50.0, -20.0, 50.0]
26.67 21.64
203.2 180.0
```
Only CAGR lands on the true ending revenue of 180. Excel: `=(180/100)^(1/3)-1` returns 0.2164; `RRI(3,100,180)` also works (Excel 2013+; not run in Excel here).
**Likely follow-ups:** 1) *Limits of CAGR?* It hides the ups and downs in between. 2) *Can CAGR be negative?* Yes, when the end is below the start.
**Common mistakes:** Averaging yearly percentages; counting years wrongly (3 years between 4 data points).

### Q33 ⭐⭐ 🟡 How do you compute a moving average, and how does it help read a trend?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can smooth noisy monthly data and explain why that helps.
**Say this in the interview:** "A moving average takes the average of the last few periods, say 3 months, and slides forward one period at a time. It flattens random ups and downs so I can see the real direction."
**Explain simply:**
- Pick a window (3 months, 7 days). Each point is the average of the latest window of values.
- The first points have no value, because there are not enough earlier months yet.
- Bigger window = smoother line but slower to react; smaller window = more responsive but noisier.
- It describes the past; it does not predict by itself.
**Formula in plain words:** Add the last N values and divide by N. In symbols: MA(t) = (x(t) + x(t-1) + ... + x(t-N+1)) / N.
**Worked example:** Monthly resignations jump around between 8 and 18. The 3-month average moves from 10.0 in March to 15.0 in December, so the underlying trend is upward even though some months dipped.
**Excel / Python:** Excel (2007+; not run in Excel here): put months in A2:A13 and resignations in B2:B13. In D4 type `=AVERAGE(B2:B4)` and copy down; it returns 10 (matches Python for March).
```python
import pandas as pd

# Resignations per month for one year (HR example)
monthly_resignations = pd.Series(
    [8, 12, 10, 15, 9, 14, 11, 18, 13, 16, 12, 17],
    index=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
)

# 3-month moving average: average of this month and the 2 months before it
moving_average_3m = monthly_resignations.rolling(window=3).mean()

# Put both side by side and round for easy reading
result_table = pd.DataFrame({
    "resignations": monthly_resignations,
    "3-month moving avg": moving_average_3m.round(2),
})
print(result_table)
```
Output:
```
     resignations  3-month moving avg
Jan             8                 NaN
Feb            12                 NaN
Mar            10               10.00
Apr            15               12.33
May             9               11.33
Jun            14               12.67
Jul            11               11.33
Aug            18               14.33
Sep            13               14.00
Oct            16               15.67
Nov            12               13.67
Dec            17               15.00
```
Each row's moving average uses that month and the two before it; Jan and Feb are blank (NaN) because they lack 3 months.
**Likely follow-ups:** 1) *How to choose the window?* Match the business cycle (12 months to remove seasonality, 3 for a quarterly view). 2) *Why does it lag?* It includes old values, so turns show up late.
**Common mistakes:** Averaging the wrong rows after copying; using a window that hides a seasonal pattern; treating the moving average as a forecast.

### Q34 ⭐⭐ 🟡 Marks of five candidates average 60. A sixth candidate scores 78. What is the new average? Show a shortcut.
**Asked at:** commonly asked (no company-specific report found); typical aptitude-style question.
**What the interviewer is checking:** Whether you think in totals and can do quick mental maths.
**Say this in the interview:** "New average is 63. Five candidates total 300, add 78 gives 378, divide by 6. Shortcut: the new person is 18 above the old average, and that 18 is shared among 6 people, so the average moves up by 3."
**Explain simply:**
- An average hides a total: average x count = total.
- Add the new value to the total and divide by the new count.
- Shortcut: new average = old average + (new value - old average) / new count.
**Formula in plain words:** The new average is the old average plus the newcomer's gap from the old average, shared across the new headcount.
**Worked example:** 5 x 60 = 300; 300 + 78 = 378; 378 / 6 = 63. Shortcut: 78 - 60 = 18; 18 / 6 = 3; 60 + 3 = 63.
**Excel / Python:**
```python
# Five candidates average 60, sixth scores 78
old_average = 60
old_count = 5
new_score = 78

# Long way: rebuild the total, add the new score, divide by the new count
old_total = old_average * old_count
new_total = old_total + new_score
new_average_long_way = new_total / (old_count + 1)

# Shortcut: new average = old average + (new score - old average) / new count
gap_from_old_average = new_score - old_average
new_average_shortcut = old_average + gap_from_old_average / (old_count + 1)

print("Long way :", new_average_long_way)
print("Shortcut :", new_average_shortcut)
```
Output:
```
Long way : 63.0
Shortcut : 63.0
```
Both routes give 63, so the shortcut is safe.
**Likely follow-ups:** 1) *What if a score is removed?* Same idea in reverse: subtract it from the total and divide by one fewer. 2) *Is the median also 63?* No, the median is a different measure (Part 2).
**Common mistakes:** Averaging 60 and 78 to get 69; forgetting that the count is now 6.

### Q35 ⭐⭐ 🟡 How do you calculate contribution to growth when total sales grew 10% and one region caused most of it?
**Asked at:** commonly asked; the contribution-to-growth idea is covered in a Towards Data Science article (no company-specific interview report found).
**What the interviewer is checking:** Whether you can split an overall growth figure into parts that add up to it.
**Say this in the interview:** "Contribution to growth is each region's change divided by the total of the previous period. Those contributions are in percentage points and add up exactly to the total growth, so I can say North delivered 7 of the 10 points."
**Explain simply:**
- Region's own growth rate uses the region's own base. Contribution uses the company total as the base.
- Because every region is divided by the same base, contributions add up to total growth.
- A small region can grow fast (high own growth) yet contribute little.
**Formula in plain words:** Contribution (in percentage points) = region's change / total last year x 100. Symbols: (R_new - R_old) / Total_old x 100.
**Worked example:** Total grew from 1,000 to 1,100 (10%). North added 70, so contributed 7.0 points (its own growth was 23.3%). South 2.0, East 1.0, West 0.0; sum 10.0.
**Excel / Python:** Excel (not run in Excel here): last year in B2:B5, this year in C2:C5. In D2 `=(C2-B2)/SUM($B$2:$B$5)` formatted as %, copy down; North returns 0.07 (7%).
```python
import pandas as pd

# Sales by region, last year and this year
sales = pd.DataFrame({
    "region": ["North", "South", "East", "West"],
    "last_year": [300, 250, 250, 200],
    "this_year": [370, 270, 260, 200],
})

# Step 1: change in sales for each region
sales["change"] = sales["this_year"] - sales["last_year"]

# Step 2: total sales last year (the common base for everyone)
total_last_year = sales["last_year"].sum()

# Step 3: contribution to growth = region change / TOTAL last year, in percent
sales["contribution_pp"] = (sales["change"] / total_last_year * 100).round(1)

# Step 4: the region's own growth rate, for comparison
sales["own_growth_pct"] = (sales["change"] / sales["last_year"] * 100).round(1)

print(sales)
print("Total growth %:", round(sales["change"].sum() / total_last_year * 100, 1))
print("Sum of contributions:", sales["contribution_pp"].sum())
```
Output:
```
  region  last_year  this_year  change  contribution_pp  own_growth_pct
0  North        300        370      70              7.0            23.3
1  South        250        270      20              2.0             8.0
2   East        250        260      10              1.0             4.0
3   West        200        200       0              0.0             0.0
Total growth %: 10.0
Sum of contributions: 10.0
```
North's 70 on a 1,000 base is 7.0 points, and the four contributions add to the 10.0 total.
**Likely follow-ups:** 1) *Why not use each region's own growth?* They do not add up and ignore size. 2) *What if a region falls?* Its contribution is negative and pulls total growth down.
**Common mistakes:** Dividing by the region's own old value; saying "7%" instead of "7 percentage points of the 10%".

### Q36 ⭐⭐ 🟡 Cost per hire fell from 80 to 62. Calculate the percentage change and explain the direction.
**Asked at:** a practice-platform question (Dataford, cost per acquisition falling from 80 to 62, labelled Red Ventures); no confirmed interview report found.
**What the interviewer is checking:** Correct base (old value), correct sign, and whether you notice that a fall can be good news.
**Say this in the interview:** "The change is minus 22.5%. New minus old is minus 18, divided by the old value 80. The negative sign only means it fell; for cost per hire that is an improvement."
**Explain simply:**
- Always divide by the starting value (80), not the ending value.
- Negative = decrease. Whether that is good depends on the metric: lower cost is good, lower sales is bad.
- Sanity check: 80 x (1 - 0.225) = 62.
**Formula in plain words:** (new - old) / old x 100.
**Worked example:** (62 - 80) / 80 = -18 / 80 = -0.225, so -22.5%. If you hire 50 people, that saves 18 x 50 = 900 in total.
**Excel / Python:** Excel: old in B2, new in C2, `=(C2-B2)/B2` formatted as % returns -22.5%.
```python
# Cost per hire before and after
old_cost_per_hire = 80
new_cost_per_hire = 62

# Absolute change, then relative change against the OLD value
absolute_change = new_cost_per_hire - old_cost_per_hire
percentage_change = absolute_change / old_cost_per_hire * 100

print("Absolute change:", absolute_change)
print("Percentage change:", percentage_change, "%")
```
Output:
```
Absolute change: -18
Percentage change: -22.5 %
```
The cost dropped by 18, which is 22.5% of the old cost.
**Likely follow-ups:** 1) *How much must it rise to come back to 80?* 18 / 62 = 29.0%, because the base is now smaller (Q12). 2) *Would you quote -22.5% or 18?* Both: relative and absolute.
**Common mistakes:** Dividing by 62 (gives 29%); dropping the minus sign; calling the fall "bad" without context.

### Q37 ⭐⭐ 🟡 How do you handle division by zero when calculating growth from a zero base?
**Asked at:** commonly asked (no company-specific report found); the zero-denominator pitfall appears in practice-platform YoY/MoM write-ups.
**What the interviewer is checking:** Whether you protect formulas against errors and choose an honest way to report the result.
**Say this in the interview:** "Growth from zero is mathematically undefined, so I do not force a number. I test for a zero base, show 'n/a' or 'new', and report the absolute change instead. In SQL I use NULLIF; in Excel an IF or IFERROR."
**Explain simply:**
- Growth = change / old. If old is 0, you divide by zero.
- Showing 0% or 100% would be wrong; infinite growth is not useful either.
- Best practice: return blank/"n/a", flag it, and add the absolute change next to it.
- Do not hide real data errors with a blanket IFERROR; check for zero explicitly.
**Formula in plain words:** If old = 0, show "n/a"; otherwise (new - old) / old.
**Worked example:** Team C had 0 resignations last year and 3 this year. Growth is undefined, but "+3 people" is clear. Teams A and B have normal growth (20% and 0%).
**Excel / Python:** Excel (not run in Excel here): old in B2, new in C2: `=IF(B2=0,"n/a",(C2-B2)/B2)`. SQL idea: `(new - old) / NULLIF(old, 0)` returns NULL instead of an error.
```python
import numpy as np

# Resignations by team: last year vs this year (Team C had zero last year)
teams = ["Team A", "Team B", "Team C"]
last_year = [10, 4, 0]
this_year = [12, 4, 3]

# Growth rate that refuses to divide by zero
def safe_growth_percent(old_value, new_value):
    if old_value == 0:
        return np.nan        # undefined: no base to compare against
    return (new_value - old_value) / old_value * 100

for team, old_value, new_value in zip(teams, last_year, this_year):
    growth = safe_growth_percent(old_value, new_value)
    absolute_change = new_value - old_value
    print(team, "| growth %:", growth, "| absolute change:", absolute_change)
```
Output:
```
Team A | growth %: 20.0 | absolute change: 2
Team B | growth %: 0.0 | absolute change: 0
Team C | growth %: nan | absolute change: 3
```
Team C shows nan (not a number) for growth but still shows the absolute change of 3.
**Likely follow-ups:** 1) *Why not use IFERROR?* It also hides unrelated errors. 2) *What if both are zero?* Show 0 change or "n/a"; agree the rule with the business.
**Common mistakes:** Reporting "infinite" or 100% growth; silently turning errors into zeros so averages are wrong.

### Q38 ⭐⭐ 🟡 What is the Rule of 72, and when can you use it?
**Asked at:** commonly asked; the Rule of 72 is mentioned in consulting-prep CAGR pages (snippet only), no company-specific report found.
**What the interviewer is checking:** Quick mental estimation of doubling time, and awareness of its limits.
**Say this in the interview:** "Divide 72 by the yearly growth rate in percent to estimate years to double. At 8% it is about 9 years. It works for compound growth at moderate rates, roughly 4% to 15%."
**Explain simply:**
- Years to double is approximately 72 / rate (in percent, not decimals).
- It assumes steady compound growth, like a salary rising 8% every year.
- It is an estimate, not exact; accuracy falls at very low or very high rates.
- Reverse: needed rate to double in N years is about 72 / N.
**Formula in plain words:** Years to double is about 72 divided by the percentage rate. Exact: ln(2) / ln(1 + rate).
**Worked example:** A salary growing 6% a year doubles in about 72 / 6 = 12 years (exact 11.90). Headcount growing 12% a year doubles in about 6 years (exact 6.12).
**Excel / Python:** Excel (not run in Excel here): rate as 8 in A2: `=72/A2` returns 9. Exact: `=NPER(8%,0,-1,2)` returns 9.006.
```python
import math

# Compare the Rule of 72 with the exact doubling time at several growth rates
print("rate %  rule of 72  exact years")
for annual_rate_percent in [2, 4, 6, 8, 12, 18, 36]:
    years_by_rule = 72 / annual_rate_percent
    growth_factor = 1 + annual_rate_percent / 100
    exact_years = math.log(2) / math.log(growth_factor)
    print(f"{annual_rate_percent:>5}  {years_by_rule:>10.2f}  {exact_years:>11.2f}")
```
Output:
```
rate %  rule of 72  exact years
    2       36.00        35.00
    4       18.00        17.67
    6       12.00        11.90
    8        9.00         9.01
   12        6.00         6.12
   18        4.00         4.19
   36        2.00         2.25
```
The rule is very close from 4% to 12% and drifts at 2% or 36%.
**Likely follow-ups:** 1) *Why 72 and not 70?* 72 divides evenly by many numbers; 69.3 or 70 is more exact for tiny rates. 2) *Rule of 114 or 144?* Triple or quadruple, same logic (from memory, unverified).
**Common mistakes:** Using it for simple (non-compounding) growth; entering 0.08 instead of 8.

### Q39 ⭐⭐ 🟡 How would you calculate the average of a column of percentages in Excel correctly?
**Asked at:** commonly asked (no company-specific report found); the averaging-ratios pitfall is discussed in HR-analytics trade articles (HR Exchange Network).
**What the interviewer is checking:** Whether you know when AVERAGE is wrong and how to weight.
**Say this in the interview:** "If every row has the same size, AVERAGE is fine. If sizes differ, I weight by the base with SUMPRODUCT divided by SUM of the sizes, or better, add up the underlying numerators and denominators and divide once."
**Explain simply:**
- A percentage is a ratio; a big group should count more than a small group.
- Weighted average = sum(percentage x size) / sum(size).
- Check the cells are real numbers, not text with a % sign typed in.
- Even better: total attended / total possible, if you have the raw counts.
**Formula in plain words:** Multiply each percentage by its group size, add, then divide by the total size.
**Worked example:** Sales 95% (100 people), Support 80% (400), Finance 90% (50). Simple average 88.33%; weighted 83.64%, because the big Support team pulls the true figure down.
**Excel / Python:** Excel 2007+ (not run in Excel here): headcount in B2:B4, attendance % in C2:C4 as 95, 80, 90. Simple: `=AVERAGE(C2:C4)` returns 88.33. Weighted: `=SUMPRODUCT(B2:B4,C2:C4)/SUM(B2:B4)` returns 83.64.
```python
import pandas as pd

# Attendance % by department, with the headcount behind each percentage
attendance = pd.DataFrame({
    "department": ["Sales", "Support", "Finance"],
    "headcount": [100, 400, 50],
    "attendance_pct": [95, 80, 90],
})

# Wrong for unequal groups: plain average of the three percentages
simple_average = attendance["attendance_pct"].mean()

# Right: weight each percentage by its headcount
weighted_sum = (attendance["attendance_pct"] * attendance["headcount"]).sum()
total_headcount = attendance["headcount"].sum()
weighted_average = weighted_sum / total_headcount

print("Simple average  :", round(simple_average, 2))
print("Weighted average:", round(weighted_average, 2))
```
Output:
```
Simple average  : 88.33
Weighted average: 83.64
```
The weighted figure is 4.7 points lower than the simple one.
**Likely follow-ups:** 1) *When is simple average fine?* Equal-sized groups. 2) *Same as pooled?* Yes, if the weights are the true bases (Q30).
**Common mistakes:** Using AVERAGE on rates from unequal groups; mixing 0.95 and 95 formats.

### Q40 ⭐⭐ 🔴 What is a base effect, and how can it make growth look small or large?
**Asked at:** commonly asked (no company-specific report found); the base-period pitfall appears in practice-platform YoY write-ups.
**What the interviewer is checking:** Whether you question a growth figure by asking how big the starting point was.
**Say this in the interview:** "A base effect means the percentage depends heavily on the starting value. A tiny base makes a small increase look huge; a very high base, such as a one-off spike last year, makes normal results look like a fall. So I always show the absolute numbers next to the percentage."
**Explain simply:**
- Same absolute change, different bases, very different percentages.
- Low base: 2 to 4 is +100%. High base: 200 to 210 is +5%, though the second added more people.
- Abnormal base periods distort too: a recession year or a one-time hiring drive.
- Fix: show absolute change, compare against a normal period, or use a longer average as the base.
**Formula in plain words:** Percentage change = change / base, so a smaller base inflates the result.
**Worked example:** Team X resignations rose from 2 to 4 (+100%); Team Y from 200 to 210 (+5%). Team Y lost 10 more people, X lost 2 more, yet X "looks" 20 times worse.
**Excel / Python:**
```python
# Two teams, both with resignations rising
small_base_last, small_base_now = 2, 4
large_base_last, large_base_now = 200, 210

# Relative change (percent) against each team's own base
small_team_growth = (small_base_now - small_base_last) / small_base_last * 100
large_team_growth = (large_base_now - large_base_last) / large_base_last * 100

print("Small team: +", small_base_now - small_base_last, "people, growth", small_team_growth, "%")
print("Large team: +", large_base_now - large_base_last, "people, growth", large_team_growth, "%")
```
Output:
```
Small team: + 2 people, growth 100.0 %
Large team: + 10 people, growth 5.0 %
```
Same method, but the small team's 2 extra people give 100% and the large team's 10 extra give only 5%.
**Likely follow-ups:** 1) *How would you present it?* Both the percentage and the absolute number, plus context. 2) *Example of a high base?* Hiring after a lockdown compared with a boom year.
**Common mistakes:** Reporting the percentage alone; comparing growth rates of teams of very different size.

### Q41 ⭐⭐ 🔴 Explain Simpson's-paradox-style trap in averages: how can every group's rate improve while the overall rate falls?
**Asked at:** commonly asked (no company-specific report found); the weighted-average and Simpson material is in the references (Wolfram demonstration, arXiv paper).
**What the interviewer is checking:** Whether you understand that overall rates depend on the mix of groups, not only on each group's rate.
**Say this in the interview:** "The overall rate is a weighted average of group rates. If volume shifts toward the group with the lower rate, the overall rate can fall even though every group improved. Always check the mix, not just the headline."
**Explain simply:**
- Overall rate = sum of (group rate x group share of volume).
- Changing the shares (mix) changes the overall rate on its own.
- Here the hard-to-close Senior group grew from 20 to 100 offers, so it dominates Year 2.
- Remedy: compare group by group, or hold the mix fixed (standardise).
**Formula in plain words:** Overall rate = total successes / total attempts = weighted average of the group rates.
**Worked example:** Junior acceptance went 80% to 85%, Senior 20% to 25%, yet the overall rate fell from 70% to 35% because most offers in Year 2 went to Seniors.
**Excel / Python:**
```python
# Offer-acceptance by job group: [offers made, offers accepted]
# Group "Junior" is easy to close, "Senior" is hard.
year_1 = {"Junior": (100, 80), "Senior": (20, 4)}
year_2 = {"Junior": (20, 17), "Senior": (100, 25)}

def show_year(label, year_data):
    total_offers = 0
    total_accepted = 0
    for group, (offers, accepted) in year_data.items():
        rate = accepted / offers * 100
        print(label, group, ": rate", round(rate, 1), "% on", offers, "offers")
        total_offers += offers
        total_accepted += accepted
    overall = total_accepted / total_offers * 100
    print(label, "OVERALL:", round(overall, 1), "%")

show_year("Year 1", year_1)
show_year("Year 2", year_2)
```
Output:
```
Year 1 Junior : rate 80.0 % on 100 offers
Year 1 Senior : rate 20.0 % on 20 offers
Year 1 OVERALL: 70.0 %
Year 2 Junior : rate 85.0 % on 20 offers
Year 2 Senior : rate 25.0 % on 100 offers
Year 2 OVERALL: 35.0 %
```
Both groups improved by 5 points, yet the overall rate halved because of the mix change.
**Likely follow-ups:** 1) *Which number do you report?* Both, and explain the mix. 2) *How do you quantify mix effect?* Decompose into rate effect and mix effect (Q59).
**Common mistakes:** Reporting only the overall rate; assuming a falling overall rate means all groups got worse.

### Q42 ⭐⭐ 🔴 A metric rises 25%, then falls to a level 10% below the start. What was the second change?
**Asked at:** commonly asked (no company-specific report found); a classic successive-percentage question in exam prep.
**What the interviewer is checking:** That you use the new base for the second change, and set up an equation cleanly.
**Say this in the interview:** "Start at 100, rise 25% to 125. Ending 10% below the start means 90. The fall from 125 to 90 is minus 35 out of 125, so the second change is minus 28%."
**Explain simply:**
- Percentages chain by multiplying, not adding: 1.25 x (1 + x) = 0.90.
- Solve: 1 + x = 0.90 / 1.25 = 0.72, so x = -28%.
- Using any starting number gives the same answer; 100 is just easy.
**Formula in plain words:** Second change = (final / after first change) - 1.
**Worked example:** 100 to 125 to 90. Fall = 35; 35 / 125 = 28%.
**Excel / Python:** Excel (not run in Excel here): `=0.9/1.25-1` returns -0.28.
```python
# Start at 100, rise 25%, then fall to a level 10% below the start
start_level = 100
after_rise = start_level * 1.25
final_level = start_level * 0.90

# Second change measured against the level AFTER the rise
second_change_percent = (final_level - after_rise) / after_rise * 100

print("After rise:", after_rise)
print("Final level:", final_level)
print("Second change %:", round(second_change_percent, 2))
# Check: apply that fall to the raised level
print("Check:", round(after_rise * (1 + second_change_percent / 100), 2))
```
Output:
```
After rise: 125.0
Final level: 90.0
Second change %: -28.0
Check: 90.0
```
A 28% drop (not 35% or 10%) is needed, and the check lands on 90.
**Likely follow-ups:** 1) *Why not 35%?* 35 is the fall in points, measured on the original 100, not on 125. 2) *And to get from 125 back to 100?* A fall of 20% (25 / 125).
**Common mistakes:** Subtracting 25 from 10 or adding percentages; dividing by 100 instead of 125.

### Q43 ⭐ 🟢 What is basis point (bps), and how is it different from percentage point?
**Asked at:** commonly asked (no company-specific report found); a finance term more than an HR one.
**What the interviewer is checking:** Precision with units when describing changes in rates.
**Say this in the interview:** "A basis point is one hundredth of a percentage point. 100 bps equals 1 percentage point. So a rate going from 10% to 12% is 2 percentage points or 200 bps. Bps are used for small moves in interest rates and margins."
**Explain simply:**
- Percentage point (pp): the plain subtraction of two percentages.
- Basis point (bps): the same change measured in hundredths, so 1 pp = 100 bps.
- Neither is "percent of percent": 10% to 12% is +2 pp but a 20% relative increase.
- Use bps when changes are tiny and you want whole numbers.
**Formula in plain words:** bps = percentage points x 100.
**Worked example:** A loan rate rising from 7.50% to 7.75% is +25 bps (0.25 pp). Attrition rising from 10% to 12% is +200 bps.
**Excel / Python:**
```python
# Attrition moved from 10% to 12%
old_rate_percent = 10
new_rate_percent = 12

# Percentage points = simple subtraction of the two percentages
change_in_percentage_points = new_rate_percent - old_rate_percent

# Basis points = percentage points x 100
change_in_basis_points = change_in_percentage_points * 100

# A 25 bps move on a 7.50% rate
rate_after_25_bps = 7.50 + 25 / 100

print("Percentage points:", change_in_percentage_points)
print("Basis points:", change_in_basis_points)
print("7.50% plus 25 bps =", rate_after_25_bps, "%")
```
Output:
```
Percentage points: 2
Basis points: 200
7.50% plus 25 bps = 7.75 %
```
The 2-point move equals 200 bps, and 25 bps takes 7.50% to 7.75%.
**Likely follow-ups:** 1) *Which would you use for attrition?* Percentage points, simpler for HR audiences. 2) *Convert 0.5 pp?* 50 bps.
**Common mistakes:** Treating 100 bps as 100% (it is 1 percentage point); mixing bps with relative percent change.

### Q44 ⭐ 🟢 How do you calculate a growth rate from index numbers (base year = 100)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you handle index series, especially year-on-year growth between two non-base years.
**Say this in the interview:** "An index shows each value as a percentage of the base year, which is 100. Growth since the base year is index minus 100. For growth between two later years I divide the later index by the earlier one and subtract 1, not subtract the two indexes."
**Explain simply:**
- Index 117 means 17% above the base year.
- Growth between year A and year B: index B / index A - 1.
- Subtracting indexes gives index points, which are not percentages unless the earlier year is the base.
- To change the base, divide the whole series by the new base year's value and multiply by 100.
**Formula in plain words:** Growth = (later index / earlier index) - 1.
**Worked example:** Headcount index 2021 = 100, 2022 = 108, 2023 = 117, 2024 = 120. 2023 vs 2022 is 117 / 108 - 1 = 8.33%, not 9%. Since 2021 the total growth is 20%.
**Excel / Python:** Excel (not run in Excel here): index in B2:B5; in C3 `=B3/B2-1` returns 0.08, copy down; 2023 returns 0.0833.
```python
import pandas as pd

# Headcount index, 2021 = 100
index_values = pd.Series([100, 108, 117, 120], index=[2021, 2022, 2023, 2024])

# Growth vs the base year: index minus 100 (because base = 100)
growth_vs_base_year = index_values - 100

# Year-on-year growth: this year's index / last year's index - 1
yearly_growth_percent = (index_values / index_values.shift(1) - 1) * 100

print(pd.DataFrame({
    "index": index_values,
    "growth vs 2021 (%)": growth_vs_base_year,
    "YoY growth (%)": yearly_growth_percent.round(2),
}))
```
Output:
```
      index  growth vs 2021 (%)  YoY growth (%)
2021    100                   0             NaN
2022    108                   8            8.00
2023    117                  17            8.33
2024    120                  20            2.56
```
Compared with the base year growth is simply index minus 100; year-on-year growth is the ratio of neighbouring indexes.
**Likely follow-ups:** 1) *Why is 9 index points not 9%?* The base for that step is 108, not 100. 2) *How to rebase to 2022 = 100?* Divide every value by 108 and multiply by 100.
**Common mistakes:** Subtracting indexes for non-base years; forgetting the base year must be 100.

### Q45 ⭐ 🟢 What is the difference between absolute change and relative change? When do you report each?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you give both numbers so the audience is not misled.
**Say this in the interview:** "Absolute change is new minus old in the original units. Relative change is that difference divided by the old value, shown as a percentage. I report absolute for scale and relative for comparison, ideally together."
**Explain simply:**
- Absolute: tells how big the change is (+4,000 rupees, +10 people).
- Relative: tells how big compared with the starting point (+10%).
- Absolute change alone cannot compare different-sized groups; relative alone hides the scale (see base effect, Q40).
- For rates, use percentage points as the absolute change.
**Formula in plain words:** Absolute = new - old. Relative = (new - old) / old x 100.
**Worked example:** Salary 40,000 to 44,000: +4,000 absolute, +10% relative. Going from 4 to 6 people is +50%, going from 400 to 402 is +0.5%, but both are +2 people.
**Excel / Python:** Excel: old in B2, new in C2; absolute `=C2-B2`, relative `=(C2-B2)/B2`.
```python
# Same salary rise seen two ways
old_salary = 40000
new_salary = 44000
absolute_change = new_salary - old_salary
relative_change_percent = absolute_change / old_salary * 100
print("Salary: absolute", absolute_change, "| relative", relative_change_percent, "%")

# Same absolute change (+2 people) on very different bases
for base in [4, 400]:
    change = 2
    print("Base", base, "-> absolute +", change, "| relative", change / base * 100, "%")
```
Output:
```
Salary: absolute 4000 | relative 10.0 %
Base 4 -> absolute + 2 | relative 50.0 %
Base 400 -> absolute + 2 | relative 0.5 %
```
The same +2 people is 50% on a base of 4 but only 0.5% on a base of 400.
**Likely follow-ups:** 1) *Which is better for a board report?* Both. 2) *For a rate like attrition?* Percentage points plus the relative change.
**Common mistakes:** Quoting only the dramatic one; calling the absolute change in a rate "percent".

### Q46 ⭐ 🟢 How do you round numbers in reports without distorting totals?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Attention to detail: shares that add to 100 and totals that tie.
**Say this in the interview:** "I never round in the middle of a calculation; I keep full precision and round only for display. If rounded shares do not add to 100, I either add a note 'figures may not add due to rounding' or use the largest remainder method to adjust the biggest leftovers."
**Explain simply:**
- Rounding each part can make the parts sum to 99.9 or 100.1.
- Use number formatting (display only) rather than ROUND when the values feed further calculations.
- Calculate the total from unrounded values, then round it.
- If a visible total must tie, give the extra tenth to the item with the largest rounded-off remainder.
**Formula in plain words:** Keep full values, round last; for a forced tie, round down everything and give the leftover units to the biggest remainders.
**Worked example:** Three equal departments are each 33.333...%. Rounded to one decimal each is 33.3 and the total shows 99.9. After adjustment the shares are 33.4, 33.3 and 33.3, which total 100.0.
**Excel / Python:** Excel: `=ROUND(B2,1)` rounds the value itself; formatting with one decimal changes only how it looks. Totals: `=ROUND(SUM(B2:B4),1)`.
```python
# Three equal departments: each share is 33.333...% of the company
raw_shares = [100 / 3, 100 / 3, 100 / 3]

# Naive: round each share to 1 decimal
naive_rounded = [round(share, 1) for share in raw_shares]
print("Naive rounded:", naive_rounded, "sum =", round(sum(naive_rounded), 1))

# Largest remainder method, working in tenths of a percent (integers)
raw_tenths = [share * 10 for share in raw_shares]
rounded_down = [int(value) for value in raw_tenths]       # drop decimals
shortfall = 1000 - sum(rounded_down)                       # tenths still to give out
remainders = [raw_tenths[i] - rounded_down[i] for i in range(3)]

# Give the missing tenths to the items with the biggest leftover
order = sorted(range(3), key=lambda i: remainders[i], reverse=True)
for position in order[:shortfall]:
    rounded_down[position] += 1

adjusted_shares = [value / 10 for value in rounded_down]
print("Largest remainder:", adjusted_shares, "sum =", round(sum(adjusted_shares), 1))
```
Output:
```
Naive rounded: [33.3, 33.3, 33.3] sum = 99.9
Largest remainder: [33.4, 33.3, 33.3] sum = 100.0
```
Plain rounding totals 99.9; the adjusted version gives 100.0.
**Likely follow-ups:** 1) *ROUND or format?* Format for display, ROUND for values that must be stored at that precision. 2) *Is adjusting honest?* Yes, if you note it; the change is within rounding error.
**Common mistakes:** Rounding early and compounding errors; forcing totals silently.

### Q47 ⭐ 🟢 What is a run rate, and how do you annualise a monthly figure?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can extrapolate sensibly and know its limits.
**Say this in the interview:** "Run rate projects the current pace over a full year. For monthly data, multiply by 12; for quarterly, by 4. It is a quick estimate that assumes the recent pace continues, so I am careful with seasonal or one-off months."
**Explain simply:**
- Annual run rate = recent monthly figure x 12.
- Year-to-date version: total so far / months elapsed x 12.
- Averaging several months is safer than using one month.
- It is not a forecast; seasonality (festival hiring, appraisal cycles) can mislead.
**Formula in plain words:** Total so far divided by months elapsed, multiplied by 12.
**Worked example:** 18 joiners in 3 months is 6 a month, so 72 a year. If you used only a strong month of 10 joiners, you would claim 120, which is too high.
**Excel / Python:** Excel (not run in Excel here): joiners YTD in B2, months in B3: `=B2/B3*12` returns 72.
```python
# Joiners in the first 3 months of the year
joiners_first_quarter = 18
months_elapsed = 3

# Monthly average so far, then annualise by x 12
monthly_average = joiners_first_quarter / months_elapsed
annual_run_rate = monthly_average * 12

# Using only the latest month (can mislead if the month was unusual)
latest_month_joiners = 10
run_rate_from_latest_month = latest_month_joiners * 12

print("Monthly average:", monthly_average)
print("Annual run rate:", annual_run_rate)
print("Run rate from latest month alone:", run_rate_from_latest_month)
```
Output:
```
Monthly average: 6.0
Annual run rate: 72.0
Run rate from latest month alone: 120
```
Averaging three months gives 72; one unusual month would give 120.
**Likely follow-ups:** 1) *When is it unreliable?* Seasonal or new businesses. 2) *Run rate vs forecast?* A forecast models changes; run rate does not.
**Common mistakes:** Annualising a peak month; mixing months and days when computing the multiplier.

### Q48 ⭐ 🟡 How do you calculate the weighted average cost or average price when quantities purchased differ?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you weight prices by quantity instead of averaging them plainly.
**Say this in the interview:** "Total money spent divided by total quantity bought. Each price is weighted by how many units were bought at that price, so in Excel it is SUMPRODUCT of quantity and price divided by SUM of quantity."
**Explain simply:**
- Bigger batches should influence the average more.
- Plain average of prices treats a 10-unit and a 25-unit batch equally, which is wrong.
- Same idea as weighted average in Q5, with quantity as the weight.
**Formula in plain words:** Weighted average price = total cost / total quantity. Symbols: sum(q x p) / sum(q).
**Worked example:** 10 laptops at 50,000, 25 at 48,000 and 15 at 52,000. Total spend 2,480,000 for 50 units, so 49,600 each. A plain average gives 50,000, which overstates it by 400.
**Excel / Python:** Excel 2007+ (not run in Excel here): quantity in B2:B4, price in C2:C4: `=SUMPRODUCT(B2:B4,C2:C4)/SUM(B2:B4)` returns 49,600.
```python
import pandas as pd

# Laptop purchases in three batches
purchases = pd.DataFrame({
    "batch": ["April", "June", "September"],
    "quantity": [10, 25, 15],
    "price_per_laptop": [50000, 48000, 52000],
})

# Step 1: total spend per batch = quantity x price
purchases["spend"] = purchases["quantity"] * purchases["price_per_laptop"]

# Step 2: weighted average price = total spend / total quantity
total_spend = purchases["spend"].sum()
total_quantity = purchases["quantity"].sum()
weighted_average_price = total_spend / total_quantity

# For comparison: plain average of the three prices (ignores quantities)
simple_average_price = purchases["price_per_laptop"].mean()

print("Total spend:", total_spend, "| total quantity:", total_quantity)
print("Weighted average price:", weighted_average_price)
print("Simple average price:", round(simple_average_price, 2))
```
Output:
```
Total spend: 2480000 | total quantity: 50
Weighted average price: 49600.0
Simple average price: 50000.0
```
The weighted price is lower because most units were bought at the cheaper 48,000 rate.
**Likely follow-ups:** 1) *What about inventory valuation?* Weighted average cost is a standard method, with FIFO as an alternative (from memory). 2) *Same as harmonic mean?* Only when weights are amounts spent, not units (Q51).
**Common mistakes:** Averaging the prices; weighting by price instead of quantity.

### Q49 ⭐ 🟡 What is a geometric mean, and when do you use it instead of the arithmetic mean?
**Asked at:** commonly asked (no company-specific report found); the geometric vs arithmetic mean contrast appears in consulting CAGR prep (PrepLounge).
**What the interviewer is checking:** Do you know that growth rates multiply, so averaging them needs a different mean?
**Say this in the interview:** "The geometric mean is the average for things that multiply, like growth rates. I use it instead of the simple average whenever each period builds on the one before, because the simple average overstates the true growth."
**Explain simply:**
- Arithmetic mean: add up, divide by count. Right for things that add (salaries, marks).
- Geometric mean: multiply the values together, then take the n-th root (square root for 2 values, cube root for 3). Right for things that multiply (growth factors, index ratios).
- Work with growth *factors*: +20% is 1.20, -20% is 0.80. Take the geometric mean of the factors, then subtract 1.
**Formula in plain words:** Multiply all the factors, then take the n-th root. Symbols: (f1 x f2 x ... x fn) ^ (1/n).
**Worked example:** Headcount grows 20% in year one, then shrinks 20% in year two. The simple average says "0% a year", but 100 people become 96.
**Excel / Python:** Excel (2007+, not run in Excel here): put the factors 1.2 and 0.8 in A2:A3, then `=GEOMEAN(A2:A3)-1`; it returns about -2.02%.
```python
import numpy as np

# Yearly growth factors: +20% then -20%
growth_factors = np.array([1.20, 0.80])

# Simple average of the factors (misleading)
arithmetic_mean = growth_factors.mean()

# Multiply the factors, then take the n-th root
product_of_factors = np.prod(growth_factors)
number_of_years = len(growth_factors)
geometric_mean = product_of_factors ** (1 / number_of_years)

print("Arithmetic mean growth:", round(arithmetic_mean - 1, 4))
print("Geometric mean growth:", round(geometric_mean - 1, 4))
print("100 people after two years:", 100 * product_of_factors)
```
```text
Arithmetic mean growth: 0.0
Geometric mean growth: -0.0202
100 people after two years: 96.0
```
The simple average claims zero growth, but headcount really falls from 100 to 96. The geometric mean (-2.02% a year) matches reality.
**Likely follow-ups:** 1) *Is CAGR a geometric mean?* Yes, it is the geometric mean growth rate (Q10). 2) *Can the geometric mean handle zero or negative values?* No, all values must be positive.
**Common mistakes:** Averaging percentages like +20% and -20% directly; forgetting to convert to factors; using it on values that add up.

### Q50 ⭐ 🟡 How do you calculate a percentage change when the value is negative (e.g. profit from -10 to 5)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you notice the standard formula breaks with a negative base, and can choose a sensible alternative.
**Say this in the interview:** "I divide the change by the absolute value of the old number, so -10 to 5 is +150%. But honestly, percentage change on a negative base is hard to interpret, so I would also report the absolute change of +15 and say it moved from a loss to a profit."
**Explain simply:**
- Usual formula: (new - old) / old. With old = -10 the sign flips and the answer misleads.
- Fix: divide by the absolute value (the number ignoring its minus sign), so the direction is right.
- When the sign changes (loss to profit), many analysts write "turned positive" instead of a percentage.
**Formula in plain words:** Change divided by the size of the old value. Symbols: (new - old) / |old|.
**Worked example:** A unit's profit moves from -10 to +5. Naive formula: 15 / -10 = -150%, which wrongly says "fell". Correct: 15 / 10 = +150%.
**Excel / Python:** Excel: old in B2, new in C2, `=(C2-B2)/ABS(B2)` returns 1.5 (150%).
```python
# Old and new profit (in lakhs)
old_profit = -10
new_profit = 5

# Absolute change: how many lakhs it moved
absolute_change = new_profit - old_profit

# Naive formula divides by a negative number
naive_change = absolute_change / old_profit

# Safer formula divides by the size of the old value
safe_change = absolute_change / abs(old_profit)

print("Absolute change:", absolute_change)
print("Naive percentage change:", naive_change * 100)
print("Safe percentage change:", safe_change * 100)
```
```text
Absolute change: 15
Naive percentage change: -150.0
Safe percentage change: 150.0
```
The naive method gives -150% even though profit clearly improved; the absolute-value method gives +150%.
**Likely follow-ups:** 1) *What if both are negative, -10 to -5?* The loss halved: +50% with the ABS formula (an improvement). 2) *What if the base is zero?* Percentage is undefined (Q37).
**Common mistakes:** Quoting -150% for an improvement; reporting a big percentage when the sign flips, without the absolute change.

### Q51 ⭐ 🟡 What is the harmonic mean, and when does it apply (e.g. average speed or price per unit)?
**Asked at:** commonly asked (no company-specific report found); a differentiator question, rarely listed in generic guides.
**What the interviewer is checking:** Whether you can spot averages of rates where the "per" quantity is held fixed.
**Say this in the interview:** "The harmonic mean is the right average for rates when the same amount of the bottom quantity is used each time, like equal distance at two speeds, or equal money spent at two prices. It is the reciprocal of the average of reciprocals."
**Explain simply:**
- A rate is "something per something", for example cost per hire.
- If you spend the *same budget* on each channel, you buy more hires where cost per hire is low, so the simple average overstates your true cost.
- The harmonic mean gives the true overall rate in that situation.
**Formula in plain words:** Number of values divided by the sum of (1 / each value). Symbols: n / (1/x1 + 1/x2 + ... + 1/xn).
**Worked example:** Spend Rs 10,000 on Channel A (Rs 500 per hire) and Rs 10,000 on Channel B (Rs 2,000 per hire). Hires: 20 + 5 = 25 for Rs 20,000, so the true cost is Rs 800 per hire, not Rs 1,250.
**Excel / Python:** Excel (not run in Excel here): costs in A2:A3, `=HARMEAN(A2:A3)` returns 800.
```python
from statistics import harmonic_mean

# Cost per hire on two channels, equal budget on each
cost_per_hire_channel_a = 500
cost_per_hire_channel_b = 2000
budget_each = 10000

# Direct calculation: total spend divided by total hires
hires_a = budget_each / cost_per_hire_channel_a
hires_b = budget_each / cost_per_hire_channel_b
true_cost_per_hire = (2 * budget_each) / (hires_a + hires_b)

# Harmonic mean of the two costs
harmonic_result = harmonic_mean([cost_per_hire_channel_a, cost_per_hire_channel_b])

# Simple average for comparison
simple_average = (cost_per_hire_channel_a + cost_per_hire_channel_b) / 2

print("True cost per hire:", true_cost_per_hire)
print("Harmonic mean:", harmonic_result)
print("Simple average (wrong here):", simple_average)
```
```text
True cost per hire: 800.0
Harmonic mean: 800.0
Simple average (wrong here): 1250.0
```
The harmonic mean matches the true Rs 800; the simple average of Rs 1,250 overstates it.
**Likely follow-ups:** 1) *Speed example?* 60 km/h one way and 40 km/h back is 48 km/h, not 50. 2) *If quantities bought differ?* Use a weighted average (Q48).
**Common mistakes:** Using the simple average for rates; using the harmonic mean when the quantities (not the budgets) are equal.

### Q52 ⭐ 🟡 How do you adjust figures for inflation to compare salaries over years (real vs nominal)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a rupee in 2024 buys less than a rupee in 2020, so raw salaries are not comparable?
**Say this in the interview:** "Nominal means the figure as paid. Real means adjusted to a common year's purchasing power using a price index like CPI. I divide each year's salary by its index and multiply by the base-year index."
**Explain simply:**
- Nominal salary: the actual number on the payslip.
- Real salary: that number restated in the prices of a chosen base year.
- CPI (Consumer Price Index) tracks how a basket of everyday goods gets more expensive; base year = 100.
- A raise smaller than inflation is a real pay cut.
**Formula in plain words:** Real salary = nominal salary x (base-year index / this-year index).
**Worked example:** Salary Rs 6,00,000 in 2020 (CPI 100) and Rs 7,20,000 in 2024 (CPI 126). Nominal rise is 20%, but in 2020 rupees the 2024 salary is worth about Rs 5,71,429, a real fall of about 4.8%. The CPI numbers here are made up for illustration.
**Excel / Python:** Excel: salary in B2, CPI in C2, base CPI in C$2, `=B3*C$2/C3` gives real salary.
```python
# Salary and price index (CPI) for 2020 and 2024 (illustrative CPI values)
salary_2020 = 600000
salary_2024 = 720000
cpi_2020 = 100
cpi_2024 = 126

# Convert 2024 salary into 2020 prices
real_salary_2024 = salary_2024 * cpi_2020 / cpi_2024

# Compare nominal and real change
nominal_change = (salary_2024 - salary_2020) / salary_2020
real_change = (real_salary_2024 - salary_2020) / salary_2020

print("Real 2024 salary in 2020 rupees:", round(real_salary_2024))
print("Nominal change %:", round(nominal_change * 100, 1))
print("Real change %:", round(real_change * 100, 1))
```
```text
Real 2024 salary in 2020 rupees: 571429
Nominal change %: 20.0
Real change %: -4.8
```
Pay went up 20% on paper but, after inflation, buys about 4.8% less than in 2020.
**Likely follow-ups:** 1) *Quick approximation?* Real growth is roughly nominal growth minus inflation (20% - 26% = about -6%); the exact method gives -4.8%. 2) *Which base year?* Any, but state it.
**Common mistakes:** Comparing nominal salaries across years; multiplying instead of dividing by the index; not stating the base year.

### Q53 ⭐ 🟡 How do you combine two groups' averages into one when only averages and counts are given?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you weight by group size instead of averaging the averages?
**Say this in the interview:** "I multiply each group's average by its count to recover that group's total, add the totals, and divide by the combined count. That is simply a weighted average."
**Explain simply:**
- Average x count = total, so you can rebuild the totals even without the raw data.
- Add the totals and add the counts, then divide.
- The bigger group pulls the answer toward its own average.
**Formula in plain words:** (average1 x count1 + average2 x count2) / (count1 + count2).
**Worked example:** Team A: 12 people, average engagement score 4.2. Team B: 28 people, average 3.6. Combined average is 3.78, not 3.9.
**Excel / Python:** Excel: averages in B2:B3, counts in C2:C3, `=SUMPRODUCT(B2:B3,C2:C3)/SUM(C2:C3)` returns 3.78.
```python
# Average score and headcount for each team
team_a_average = 4.2
team_a_count = 12
team_b_average = 3.6
team_b_count = 28

# Rebuild each team's total score
team_a_total = team_a_average * team_a_count
team_b_total = team_b_average * team_b_count

# Divide the combined total by the combined headcount
combined_average = (team_a_total + team_b_total) / (team_a_count + team_b_count)

# The wrong way: average of the two averages
average_of_averages = (team_a_average + team_b_average) / 2

print("Combined average:", round(combined_average, 2))
print("Average of averages (wrong):", round(average_of_averages, 2))
```
```text
Combined average: 3.78
Average of averages (wrong): 3.9
```
Team B is more than twice as big, so the correct answer (3.78) sits closer to its 3.6.
**Likely follow-ups:** 1) *When would the simple average be fine?* When both groups are the same size. 2) *Can I combine medians this way?* No, you need the raw data.
**Common mistakes:** Averaging the two averages; trying to combine medians or percentiles from summaries.

### Q54 ⭐ 🟡 How do you calculate the break-even point as a ratio or percentage, and when does an analyst need it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you find the volume at which two options cost the same, or a business stops losing money?
**Say this in the interview:** "Break-even is where total income equals total cost. Divide fixed costs by the contribution per unit, which is price minus variable cost. As a percentage it is break-even volume over expected volume."
**Explain simply:**
- Fixed cost: paid regardless of volume (salary of an in-house recruiter).
- Variable cost: grows with each unit (cost per hire).
- Contribution per unit: what each unit saves or earns after its variable cost.
- An analyst uses it for make-vs-buy decisions, pricing, and "is this programme worth running?".
**Formula in plain words:** Break-even units = fixed costs / (price per unit - variable cost per unit). Break-even % = break-even units / expected units.
**Worked example:** An in-house recruiting team costs Rs 6,00,000 a year fixed plus Rs 20,000 variable per hire. An agency charges Rs 80,000 per hire. In-house is cheaper beyond 10 hires a year. If we expect 16 hires, break-even is 62.5% of expected volume.
**Excel / Python:** Excel: fixed in B1, agency fee in B2, in-house variable in B3, `=B1/(B2-B3)` returns 10.
```python
# Yearly numbers for in-house vs agency hiring
fixed_cost_in_house = 600000
variable_cost_in_house_per_hire = 20000
agency_fee_per_hire = 80000
expected_hires = 16

# Saving per hire by using in-house instead of agency
saving_per_hire = agency_fee_per_hire - variable_cost_in_house_per_hire

# Hires needed for the fixed cost to be recovered
break_even_hires = fixed_cost_in_house / saving_per_hire

# Break-even as a share of expected hiring
break_even_share = break_even_hires / expected_hires

print("Break-even hires:", break_even_hires)
print("Break-even as % of expected hires:", break_even_share * 100)
```
```text
Break-even hires: 10.0
Break-even as % of expected hires: 62.5
```
Above 10 hires a year the in-house team wins; at 16 expected hires we are comfortably past break-even.
**Likely follow-ups:** 1) *Break-even revenue?* Fixed cost / contribution margin ratio. 2) *What is margin of safety?* How far expected volume is above break-even (here 37.5%).
**Common mistakes:** Ignoring that part of the cost is fixed; using total instead of per-unit variable cost.

### Q55 ⭐ 🟡 How do you calculate a percentage hike so that the new salary equals a target amount?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you work backwards from a target to the percentage, using the old salary as the base?
**Say this in the interview:** "Hike % is target minus current, divided by current. For example, going from 48,000 to 60,000 needs a 25% hike."
**Explain simply:**
- It is just percentage change (Q1) with the target as the "new" value.
- The base is the *current* salary, not the target.
- Check by multiplying: current x (1 + hike) should equal the target.
**Formula in plain words:** Hike % = (target - current) / current.
**Worked example:** An offer must reach Rs 60,000 for a candidate earning Rs 48,000. Hike = 12,000 / 48,000 = 25%. Note: 25% takes you up; the candidate going back down from 60,000 to 48,000 is only -20%.
**Excel / Python:** Excel: current in B2, target in C2, `=(C2-B2)/B2` returns 0.25.
```python
# Current salary and the target
current_salary = 48000
target_salary = 60000

# Hike needed as a fraction of the current salary
hike_fraction = (target_salary - current_salary) / current_salary

# Check: apply the hike and confirm we land on the target
check_salary = current_salary * (1 + hike_fraction)

print("Hike needed %:", hike_fraction * 100)
print("Salary after hike:", check_salary)
```
```text
Hike needed %: 25.0
Salary after hike: 60000.0
```
A 25% hike turns 48,000 into exactly 60,000, so the answer checks out.
**Likely follow-ups:** 1) *Hike to reach target after a 5% tax deduction?* Work on the take-home number the same way. 2) *Hike on CTC vs fixed pay?* State which base you use.
**Common mistakes:** Dividing by the target instead of the current salary (gives 20%, which is wrong).

### Q56 ⭐ 🟡 How do you calculate the weighted average for a scorecard where KPIs carry different weights?
**Asked at:** commonly asked (no company-specific report found); the weighted-average idea is covered in generic prep guides.
**What the interviewer is checking:** Can you apply weights that add to 100% and use SUMPRODUCT?
**Say this in the interview:** "I multiply each KPI score by its weight, add them up, and divide by the sum of the weights. If the weights add to 100%, the sum of score times weight is already the answer."
**Explain simply:**
- Weight = how much a KPI matters (a share of the total).
- Check that weights add to 100%; if not, divide by their total.
- Put scores on the same scale first (e.g. 0 to 100), otherwise one KPI dominates just by its units.
**Formula in plain words:** Sum of (score x weight) / sum of weights.
**Worked example:** A recruiter scorecard: time-to-fill 80 (weight 40%), offer-acceptance 90 (30%), quality of hire 70 (20%), candidate experience 60 (10%). Overall score is 79.
**Excel / Python:** Excel (2007+, not run in Excel here): scores B2:B5, weights C2:C5, `=SUMPRODUCT(B2:B5,C2:C5)/SUM(C2:C5)` returns 79.
```python
# KPI scores (0-100) and weights for one recruiter
kpi_names = ["Time to fill", "Offer acceptance", "Quality of hire", "Candidate experience"]
kpi_scores = [80, 90, 70, 60]
kpi_weights = [0.40, 0.30, 0.20, 0.10]

# Multiply each score by its weight and add them up
weighted_total = 0
for score, weight in zip(kpi_scores, kpi_weights):
    weighted_total = weighted_total + score * weight

# Divide by total weight (1.0 here) to be safe
overall_score = weighted_total / sum(kpi_weights)

print("Weights add up to:", round(sum(kpi_weights), 2))
print("Overall scorecard score:", round(overall_score, 1))
print("Simple average (ignores weights):", sum(kpi_scores) / len(kpi_scores))
```
```text
Weights add up to: 1.0
Overall scorecard score: 79.0
Simple average (ignores weights): 75.0
```
The weighted score (79) is higher than the simple average (75) because the strongest KPIs carry more weight.
**Likely follow-ups:** 1) *Weights add to 110%?* Divide by the total weight. 2) *KPI on a different scale?* Convert to a common scale first.
**Common mistakes:** Weights that do not add up to 100%; mixing scales; using AVERAGE instead of SUMPRODUCT.

### Q57 ⭐ 🟡 How do you scale a target proportionally when team size changes (direct and inverse proportion)?
**Asked at:** commonly asked (no company-specific report found); an aptitude-style question.
**What the interviewer is checking:** Can you tell whether a change makes the result go up with it (direct) or down against it (inverse)?
**Say this in the interview:** "If output grows with team size, it is direct proportion: find the per-person figure and multiply. If the work is fixed and more people finish faster, it is inverse proportion: people times days stays constant."
**Explain simply:**
- Direct: more recruiters means more closures. Per-person output x new headcount.
- Inverse: fixed workload, more people means fewer days. People x time = constant.
- This assumes everyone is equally productive, which is a simplification.
**Formula in plain words:** Direct: new target = old target x (new size / old size). Inverse: new time = old time x (old size / new size).
**Worked example:** 8 recruiters close 96 requisitions a quarter, so 12 each; with 10 recruiters the target is 120. Separately, 8 recruiters need 15 days to screen a fixed pile of CVs, so 12 recruiters need 10 days.
**Excel / Python:** Excel: `=96*(10/8)` returns 120; `=15*(8/12)` returns 10.
```python
# Direct proportion: target grows with team size
old_team_size = 8
old_target = 96
new_team_size = 10
new_target = old_target * new_team_size / old_team_size

# Inverse proportion: fixed workload, more people means fewer days
old_days = 15
bigger_team_size = 12
new_days = old_days * old_team_size / bigger_team_size

print("New quarterly target:", new_target)
print("New screening days:", new_days)
```
```text
New quarterly target: 120.0
New screening days: 10.0
```
Ten recruiters should close 120 requisitions; twelve recruiters finish the screening in 10 days instead of 15.
**Likely follow-ups:** 1) *Why might it not hold?* New joiners ramp up slowly, and some work cannot be split. 2) *How do you know direct vs inverse?* Ask: if one goes up, does the other go up (direct) or down (inverse)?
**Common mistakes:** Using direct scaling for a fixed workload; ignoring ramp-up time.

### Q58 ⭐ 🔴 A company has 50% growth in month 1 and -50% in month 2. What is the net change and the average monthly growth?
**Asked at:** commonly asked (no company-specific report found); a classic trick question.
**What the interviewer is checking:** Whether you multiply growth factors instead of adding percentages.
**Say this in the interview:** "Net change is 1.5 x 0.5 = 0.75, so down 25%. The average monthly growth is not 0%; the geometric mean is the square root of 0.75, about -13.4% a month."
**Explain simply:**
- +50% then -50% are not opposites: the -50% is taken from a bigger base.
- Convert to factors (1.5 and 0.5) and multiply.
- The simple average of +50 and -50 is 0%, which would wrongly say "no change".
**Formula in plain words:** Net factor = product of monthly factors. Average monthly growth = (net factor) ^ (1 / months) - 1.
**Worked example:** Starting with 100 applications: month 1 gives 150, month 2 gives 75.
**Excel / Python:** Excel: `=1.5*0.5-1` returns -0.25; `=SQRT(0.75)-1` returns about -0.134.
```python
# Start value and monthly growth rates
starting_value = 100
monthly_growth_rates = [0.50, -0.50]

# Apply each month's growth in turn
current_value = starting_value
for growth_rate in monthly_growth_rates:
    current_value = current_value * (1 + growth_rate)
    print("Value after this month:", current_value)

# Net change over the two months
net_change = current_value / starting_value - 1

# Average monthly growth using the geometric mean
number_of_months = len(monthly_growth_rates)
average_monthly_growth = (1 + net_change) ** (1 / number_of_months) - 1

print("Net change %:", round(net_change * 100, 2))
print("Average monthly growth %:", round(average_monthly_growth * 100, 2))
print("Simple average of rates %:", sum(monthly_growth_rates) / number_of_months * 100)
```
```text
Value after this month: 150.0
Value after this month: 75.0
Net change %: -25.0
Average monthly growth %: -13.4
Simple average of rates %: 0.0
```
The company ends 25% lower; averaging the rates to 0% would hide that loss.
**Likely follow-ups:** 1) *What growth is needed to recover?* +33.3% (Q12). 2) *Why can't I just average?* Because each month builds on the previous one.
**Common mistakes:** Saying net change is 0%; stating the average growth as 0%.

### Q59 ⭐ 🔴 How do you decompose a change in an average (e.g. average salary) into effect of rate and effect of mix?
**Asked at:** commonly asked (no company-specific report found); weighted average and mix effects are covered in Simpson's-paradox material (Wolfram, arXiv).
**What the interviewer is checking:** Can you separate "people got paid more" from "the workforce shape changed"?
**Say this in the interview:** "An overall average is each group's average times the group's share. So it can change because group averages changed (rate effect) or because group shares changed (mix effect). I measure the rate effect with old shares and the mix effect with the share change at new rates; they add to the total."
**Explain simply:**
- Rate effect: pay changed within each grade, shares held at last year's.
- Mix effect: the proportion of juniors and seniors changed.
- Together they exactly equal the total change.
**Formula in plain words:** Rate effect = sum of (old share x change in grade average). Mix effect = sum of (change in share x new grade average).
**Worked example:** Last year 70 juniors at Rs 30,000 and 30 seniors at Rs 60,000: average 39,000. This year 80 juniors at Rs 32,000 and 20 seniors at Rs 63,000: average 38,200. Both grades got a raise, yet the average fell by Rs 800: rate +2,300, mix -3,100.
**Excel / Python:** Excel: put shares and averages in columns, then `=SUMPRODUCT(old_share, new_avg-old_avg)` for rate, `=SUMPRODUCT(new_share-old_share, new_avg)` for mix (not run in Excel here).
```python
import numpy as np

# Grades: junior, senior
old_headcount = np.array([70, 30])
new_headcount = np.array([80, 20])
old_average_salary = np.array([30000, 60000])
new_average_salary = np.array([32000, 63000])

# Share of headcount in each grade
old_share = old_headcount / old_headcount.sum()
new_share = new_headcount / new_headcount.sum()

# Overall averages (weighted by share)
old_overall = (old_share * old_average_salary).sum()
new_overall = (new_share * new_average_salary).sum()

# Rate effect: pay changes inside each grade, using old shares
rate_effect = (old_share * (new_average_salary - old_average_salary)).sum()

# Mix effect: change in shares, valued at new pay
mix_effect = ((new_share - old_share) * new_average_salary).sum()

print("Old overall average:", old_overall)
print("New overall average:", new_overall)
print("Total change:", round(new_overall - old_overall, 2))
print("Rate effect:", round(rate_effect, 2))
print("Mix effect:", round(mix_effect, 2))
print("Rate + mix:", round(rate_effect + mix_effect, 2))
```
```text
Old overall average: 39000.0
New overall average: 38200.0
Total change: -800.0
Rate effect: 2300.0
Mix effect: -3100.0
Rate + mix: -800.0
```
Pay rose inside both grades (+2,300 on average) but the share of well-paid seniors shrank (-3,100), so the overall average fell by 800.
**Likely follow-ups:** 1) *Is this Simpson's paradox?* It is the same mechanism (Q41). 2) *Does the split depend on order?* Yes, there are other ways to attribute the interaction; state your convention.
**Common mistakes:** Reporting only the overall average; double counting the interaction; forgetting the effects must add to the total.

### Q60 ⭐ 🔴 How do you calculate compounded monthly growth rate (CMGR) and convert it to an annual figure?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Do you know CMGR is CAGR at monthly frequency, and that you count intervals, not data points?
**Say this in the interview:** "CMGR is the steady monthly growth rate that would take you from the first month's value to the last. It is (last / first) raised to 1 over the number of month-to-month intervals, minus 1. To annualise, I compound it: (1 + CMGR) to the power 12, minus 1."
**Explain simply:**
- Six months of data (Jan to Jun) is only 5 intervals; that is the exponent.
- Annualising by multiplying by 12 is wrong because growth compounds.
- Annualising a short window is an extrapolation; say so.
**Formula in plain words:** CMGR = (last value / first value) ^ (1 / months between) - 1. Annual = (1 + CMGR) ^ 12 - 1.
**Worked example:** Monthly applications rose from 400 in January to 520 in June. CMGR is about 5.4%, which annualises to about 88%.
**Excel / Python:** Excel: first in B2, last in G2, `=(G2/B2)^(1/5)-1` returns about 0.0539; `=(1+H2)^12-1` returns about 0.88.
```python
# Applications in the first and last month
first_month_value = 400
last_month_value = 520

# January to June is 5 steps between months
months_between = 5

# Steady monthly growth rate
cmgr = (last_month_value / first_month_value) ** (1 / months_between) - 1

# Compound the monthly rate over 12 months
annual_growth = (1 + cmgr) ** 12 - 1

# Wrong shortcut for comparison
wrong_annual = cmgr * 12

print("CMGR %:", round(cmgr * 100, 2))
print("Annualised %:", round(annual_growth * 100, 1))
print("Wrong shortcut (CMGR x 12) %:", round(wrong_annual * 100, 1))
```
```text
CMGR %: 5.39
Annualised %: 87.7
Wrong shortcut (CMGR x 12) %: 64.6
```
Growing about 5.4% every month compounds to roughly 88% a year, not 65%.
**Likely follow-ups:** 1) *CMGR vs CAGR?* Same formula, monthly vs yearly steps. 2) *Seasonal data?* A short window can mislead; use a full year if possible.
**Common mistakes:** Using 6 instead of 5 as the exponent; multiplying by 12; extrapolating a short run.

### Q61 ⭐ 🔴 A manager says "attrition is 12%, up from 10%, so 20% more people left". Is that statement correct?
**Asked at:** commonly asked (no company-specific report found); a classic percent vs percentage-point trap.
**What the interviewer is checking:** Do you separate the rate from the number of people, and percentage points from percent?
**Say this in the interview:** "It is partly right. The rate rose 2 percentage points, which is a 20% relative increase in the rate. But '20% more people left' is only true if headcount stayed the same."
**Explain simply:**
- 10% to 12% is +2 percentage points, and 2 / 10 = a 20% rise in the rate.
- People who left = rate x average headcount, so headcount matters.
- If headcount grew, even more people left; if it shrank, fewer than 20% more.
**Formula in plain words:** Leavers = attrition rate x average headcount.
**Worked example:** With headcount 1,000 both years: 100 leavers become 120, so +20% is right. If headcount grew to 1,200: 144 leavers, +44%. If it shrank to 800: 96 leavers, which is -4%.
**Excel / Python:** Excel: `=(B2*C2)/(B1*C1)-1` where row 1 is last year and row 2 this year, rates in B and headcount in C.
```python
# Last year attrition rate and headcount
old_rate = 0.10
old_headcount = 1000
old_leavers = old_rate * old_headcount

# This year rate with three headcount scenarios
new_rate = 0.12
scenario_headcounts = [1000, 1200, 800]

# Change in the rate itself
percentage_point_change = (new_rate - old_rate) * 100
relative_change_in_rate = (new_rate - old_rate) / old_rate * 100
print("Percentage point change:", round(percentage_point_change, 1))
print("Relative change in rate %:", round(relative_change_in_rate, 1))

# Change in number of leavers for each headcount scenario
for new_headcount in scenario_headcounts:
    new_leavers = new_rate * new_headcount
    leavers_change = (new_leavers - old_leavers) / old_leavers * 100
    print("Headcount", new_headcount, "-> leavers", round(new_leavers), "change %", round(leavers_change, 1))
```
```text
Percentage point change: 2.0
Relative change in rate %: 20.0
Headcount 1000 -> leavers 120 change % 20.0
Headcount 1200 -> leavers 144 change % 44.0
Headcount 800 -> leavers 96 change % -4.0
```
The "20%" describes the rate; the change in actual leavers depends on how headcount moved.
**Likely follow-ups:** 1) *How would you report it?* "Attrition rose 2 percentage points, from 10% to 12%." 2) *Why does it matter?* Mixing the two overstates or understates the problem.
**Common mistakes:** Saying attrition rose 2%; assuming the number of leavers moves with the rate.
