# Book 6 — Aptitude & Business Maths | Part 8: Data Interpretation (Tables, Bar, Pie and Line Charts) 🟢🟡🔴

**Target:** 80 questions | **Actual:** 94 questions
**Scope:** reading tables and bar, pie and line charts under time pressure: percentage change, shares, ratios, averages, growth and approximation, with business and HR data.

### Q1 ⭐⭐⭐ 🟢 What is the formula for percentage change, and why must the base be the original (earlier) value?
**Asked at:** commonly asked (no company-specific report found); percent change and the "base rule" are listed as core DI formulas in prep material (unverified).
**What the interviewer is checking:** Whether you know the formula and which number goes in the denominator (the "base").
**Say this in the interview:** "Percentage change = (new value minus old value) / old value x 100. The old value is the base because we are measuring growth from where we started."
**Answer:** **Percentage change = (New - Old) / Old x 100. A positive result is an increase, a negative result is a decrease.**
**Step-by-step working (mini-example):**
1. Headcount was 400 last year and is 464 this year.
2. Change = 464 - 400 = 64.
3. Divide by the old value (the base): 64 / 400 = 0.16.
4. Multiply by 100: 16% increase.
5. Why the old value? Using 464 as the base gives 64 / 464 = 13.79%, which answers a different question ("what share of this year's headcount is the extra 64?").
**Check:** 400 x 1.16 = 464 (verified by script).
**Explain simply:**
- "Base" means the number you compare against; it always sits at the bottom of the fraction.
- Percent change answers: "for every 100 we had before, how many did we gain or lose?"
- Rises and falls are not symmetric: +20% then -20% does not bring you back (100 to 120 to 96).
**Likely follow-ups:** 1) Salary Rs 50,000 to Rs 56,000? 6,000 / 50,000 = 12%. 2) What if the old value is 0? Percent change is undefined (cannot divide by zero).
**Common mistakes / traps:** Dividing by the new value; for a decrease, dividing by the smaller (new) number and getting a bigger percentage than the right one.

### Q2 ⭐⭐⭐ 🟢 What is the difference between a percentage-point change and a percent change? Attrition rises from 10% to 12%: state both.
**Asked at:** commonly asked (no company-specific report found); percentage points versus percent is listed as a standard DI trap in prep material (unverified).
**What the interviewer is checking:** Whether you can tell a subtraction of two percentages from a relative change.
**Say this in the interview:** "Going from 10% to 12% is a 2 percentage-point rise, but a 20% rise in the attrition rate itself, because 2 is 20% of 10."
**Answer:** **2 percentage points (pp) and 20% (percent change).**
**Step-by-step working:**
1. Percentage-point change = new rate - old rate = 12 - 10 = 2 pp.
2. Percent change = (12 - 10) / 10 x 100 = 2 / 10 x 100 = 20%.
**Fast method (30 seconds):** Subtract for points; divide that gap by the old rate for percent. Points are always smaller than the percent change when the old rate is under 100%.
**Check:** 10% x 1.20 = 12% (verified by script).
**Explain simply:**
- A percentage point is the unit for the gap between two percentages (a rate measured in %).
- Percent change is relative: "how much bigger is the new rate compared with the old one".
- Attrition is the share of employees who leave, so it is already a percentage; that is why both views exist.
**Likely follow-ups:** Attrition falls from 15% to 10%? That is 5 pp, or 33.33% fall (5 / 15).
**Common mistakes / traps:** Saying "2%" for both; or saying "12% rise". Headlines saying "attrition up 20%" and "up 2 points" are both true but mean different things.

### Q3 ⭐⭐⭐ 🟢 What is the percentage increase in total headcount from 2024 to 2025?

Headcount by department (employees):

| Department | 2024 | 2025 |
|---|---|---|
| HR | 40 | 50 |
| Finance | 60 | 66 |
| Sales | 120 | 150 |
| IT | 80 | 104 |
| Operations | 100 | 94 |

**Asked at:** commonly asked (no company-specific report found); simple table percent change is a core DI item in prep material (unverified).
**What the interviewer is checking:** Totalling columns first, then applying percent change to the totals (not averaging department percentages).
**Say this in the interview:** "2024 total is 400, 2025 total is 464, so the rise is 64 on a base of 400, which is 16%."
**Answer:** **16%**
**Step-by-step working:**
1. 2024 total = 40 + 60 + 120 + 80 + 100 = 400.
2. 2025 total = 50 + 66 + 150 + 104 + 94 = 464.
3. Increase = 464 - 400 = 64.
4. Percentage = 64 / 400 x 100 = 16%.
**Fast method (30 seconds):** Add the row changes instead: +10, +6, +30, +24, -6 = +64. Then 64 on 400 is 16 on 100.
**Check:** 400 x 1.16 = 464 (verified by script).
**Explain simply:**
- Use the total of the column as the base, because the question asks about the whole company.
- Each department has its own percentage; they cannot just be averaged because departments differ in size.
**Likely follow-ups:** What if the 2025 Operations figure were 100? Total 470, increase 17.5%.
**Common mistakes / traps:** Averaging the five department percentages (25, 10, 25, 30, -6 gives 16.8%, a wrong answer that looks close).

### Q4 ⭐⭐⭐ 🟢 Which department shows the highest percentage growth in headcount from 2024 to 2025?

Headcount by department (employees):

| Department | 2024 | 2025 |
|---|---|---|
| HR | 40 | 50 |
| Finance | 60 | 66 |
| Sales | 120 | 150 |
| IT | 80 | 104 |
| Operations | 100 | 94 |

**Asked at:** commonly asked (no company-specific report found); "absolute versus percentage" trap is a standard DI theme in prep material (unverified).
**What the interviewer is checking:** Comparing percentages (growth on each department's own base), not raw additions.
**Say this in the interview:** "I compute each department's change over its own 2024 base. IT grew 24 on 80, which is 30%, the highest."
**Answer:** **IT (30%)**
**Step-by-step working:**
1. HR: (50 - 40) / 40 = 10 / 40 = 25%.
2. Finance: (66 - 60) / 60 = 6 / 60 = 10%.
3. Sales: (150 - 120) / 120 = 30 / 120 = 25%.
4. IT: (104 - 80) / 80 = 24 / 80 = 30%.
5. Operations: (94 - 100) / 100 = -6%.
6. Highest is IT at 30%.
**Fast method (30 seconds):** Compare "added / old" mentally: 10/40 = 1/4, 6/60 = 1/10, 30/120 = 1/4, 24/80 = 3/10. The 3/10 is the largest.
**Check:** 80 x 1.30 = 104 (verified by script).
**Explain simply:**
- Sales added the most people (30) but on a bigger base, so its growth rate is only 25%.
- Percentage growth is fair across different sizes; absolute growth is not.
**Likely follow-ups:** Which department added the most employees? Sales (+30).
**Common mistakes / traps:** Picking Sales because it added the most heads.

### Q5 ⭐⭐⭐ 🟢 By what percentage did Operations headcount decrease from 2024 to 2025?

Headcount by department (employees):

| Department | 2024 | 2025 |
|---|---|---|
| HR | 40 | 50 |
| Finance | 60 | 66 |
| Sales | 120 | 150 |
| IT | 80 | 104 |
| Operations | 100 | 94 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Percent decrease on the original base.
**Say this in the interview:** "Operations went from 100 to 94, a fall of 6 on a base of 100, so 6%."
**Answer:** **6% decrease**
**Step-by-step working:**
1. Fall = 100 - 94 = 6.
2. Percentage = 6 / 100 x 100 = 6%.
**Fast method (30 seconds):** A base of 100 means the number of heads lost is the percentage.
**Check:** 100 x (1 - 0.06) = 94 (verified by script).
**Explain simply:**
- A decrease uses the old (2024) value as base, exactly like an increase.
**Likely follow-ups:** If the department then grows back from 94 to 100, the rise is 6 / 94 = 6.38%, not 6%, because the base is now 94.
**Common mistakes / traps:** Dividing 6 by 94 (the new value) and getting 6.38%.

### Q6 ⭐⭐⭐ 🟢 How much money (Rs) is allotted to Bonus in the salary budget?

Pie chart, annual salary budget of Rs 60,00,000, split as: Basic 40%, HRA 20%, Bonus 10%, PF 12%, Allowances 18%.
**Asked at:** a pie chart with percentages and follow-up questions was reported in a 2025 Glassdoor review for Novartis (via search summary; mapping of detail not verified); otherwise commonly asked.
**What the interviewer is checking:** Turning a pie percentage into an amount.
**Say this in the interview:** "Bonus is 10% of Rs 60,00,000, which is Rs 6,00,000."
**Answer:** **Rs 6,00,000**
**Step-by-step working:**
1. Check the shares add to 100%: 40 + 20 + 10 + 12 + 18 = 100.
2. Bonus = 10% of 60,00,000 = 60,00,000 x 10 / 100 = Rs 6,00,000.
**Fast method (30 seconds):** 10% means drop one zero: 60,00,000 becomes 6,00,000.
**Check:** 10 x 6,00,000 = 60,00,000 (verified by script).
**Explain simply:**
- In a pie chart each sector is a percentage of one total; amount = percentage / 100 x total.
- Rs 60,00,000 is "60 lakh"; 1 lakh = 1,00,000.
**Likely follow-ups:** PF amount? 12% of 60,00,000 = Rs 7,20,000.
**Common mistakes / traps:** Misplacing zeros in lakh figures; use lakh units (60 lakh x 10% = 6 lakh) to stay safe.

### Q7 ⭐⭐⭐ 🟢 What is the central angle (in degrees) of the Allowances sector?

Pie chart, annual salary budget of Rs 60,00,000, split as: Basic 40%, HRA 20%, Bonus 10%, PF 12%, Allowances 18%.
**Asked at:** commonly asked (no company-specific report found); pie sector angles are a standard DI item in prep material (unverified).
**What the interviewer is checking:** Knowing that a full circle is 360 degrees.
**Say this in the interview:** "A full circle is 360 degrees, so 18% of it is 0.18 x 360 = 64.8 degrees."
**Answer:** **64.8 degrees**
**Step-by-step working:**
1. Full circle = 360 degrees = 100%.
2. 1% = 360 / 100 = 3.6 degrees.
3. Allowances = 18 x 3.6 = 64.8 degrees.
**Fast method (30 seconds):** Multiply the percentage by 3.6: 18 x 3.6 = 18 x 3 + 18 x 0.6 = 54 + 10.8 = 64.8.
**Check:** all angles: 144 + 72 + 36 + 43.2 + 64.8 = 360 (verified by script).
**Explain simply:**
- Central angle is the angle at the middle of the pie that a slice takes up.
- Each 1% of the whole is 3.6 degrees.
**Likely follow-ups:** Angle of Basic? 40 x 3.6 = 144 degrees.
**Common mistakes / traps:** Using 100 instead of 360, or forgetting the answer is a decimal.

### Q8 ⭐⭐⭐ 🟢 What is the ratio of Basic to PF in the salary budget, in simplest form?

Pie chart, annual salary budget of Rs 60,00,000, split as: Basic 40%, HRA 20%, Bonus 10%, PF 12%, Allowances 18%.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Ratios can use the percentages directly; the total cancels out.
**Say this in the interview:** "Basic is 40% and PF is 12%, so the ratio is 40:12, which reduces by 4 to 10:3."
**Answer:** **10:3**
**Step-by-step working:**
1. Basic = 40% of 60,00,000 = Rs 24,00,000; PF = 12% = Rs 7,20,000.
2. Ratio = 24,00,000 : 7,20,000 = 40 : 12 (divide both by 60,000).
3. HCF of 40 and 12 is 4, so 40:12 = 10:3.
**Fast method (30 seconds):** Skip the rupees; both are shares of the same total, so write 40:12 and cancel.
**Check:** 10 / 3 = 3.33 and 40 / 12 = 3.33 (verified by script).
**Explain simply:**
- When two parts come from one total, their ratio equals the ratio of their percentages.
**Likely follow-ups:** HRA to Bonus? 20:10 = 2:1.
**Common mistakes / traps:** Stopping at 20:6 (not fully reduced); writing the ratio the wrong way round (3:10).

### Q9 ⭐⭐⭐ 🟢 How much more (in Rs) is spent on Allowances than on Bonus?

Pie chart, annual salary budget of Rs 60,00,000, split as: Basic 40%, HRA 20%, Bonus 10%, PF 12%, Allowances 18%.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Subtract the percentages first, then convert once.
**Say this in the interview:** "The gap is 18% minus 10% = 8% of Rs 60,00,000, which is Rs 4,80,000."
**Answer:** **Rs 4,80,000**
**Step-by-step working:**
1. Allowances = 18% of 60,00,000 = Rs 10,80,000.
2. Bonus = 10% of 60,00,000 = Rs 6,00,000.
3. Difference = 10,80,000 - 6,00,000 = Rs 4,80,000.
**Fast method (30 seconds):** 18 - 10 = 8 percent; 8% of 60 lakh = 4.8 lakh.
**Check:** 8 x 60,000 = 4,80,000 (1% of the budget is Rs 60,000) (verified by script).
**Explain simply:**
- Working with percentages first saves two multiplications.
**Likely follow-ups:** How much more on Basic than HRA? 20% = Rs 12,00,000.
**Common mistakes / traps:** Answering "8%" when rupees are asked.

### Q10 ⭐⭐⭐ 🟢 What are the total sales of Product A from January to June (Rs lakh)?

Monthly sales (Rs lakh):

| Month | Product A | Product B |
|---|---|---|
| Jan | 40 | 50 |
| Feb | 45 | 40 |
| Mar | 55 | 60 |
| Apr | 50 | 45 |
| May | 60 | 55 |
| Jun | 70 | 65 |

**Asked at:** commonly asked (no company-specific report found); simple table lookups and totals are core DI items in prep material (unverified).
**What the interviewer is checking:** Accurate reading and adding of the right column.
**Say this in the interview:** "I add the Product A column: 40+45+55+50+60+70 = 320 lakh."
**Answer:** **Rs 320 lakh**
**Step-by-step working:**
1. 40 + 45 = 85.
2. 85 + 55 = 140.
3. 140 + 50 = 190.
4. 190 + 60 = 250.
5. 250 + 70 = 320.
**Fast method (30 seconds):** Pair numbers that make round sums: (40 + 70) + (45 + 55) + (50 + 60) = 110 + 100 + 110 = 320.
**Check:** average 320 / 6 = 53.33, which sits between the smallest (40) and largest (70) (verified by script).
**Explain simply:**
- Units matter: the table is in Rs lakh, so the answer is also in lakh.
**Likely follow-ups:** Total of Product B? 315 lakh.
**Common mistakes / traps:** Reading the Product B column by mistake.

### Q11 ⭐⭐⭐ 🟢 What is the average monthly sales of Product B over the six months (Rs lakh)?

Monthly sales (Rs lakh):

| Month | Product A | Product B |
|---|---|---|
| Jan | 40 | 50 |
| Feb | 45 | 40 |
| Mar | 55 | 60 |
| Apr | 50 | 45 |
| May | 60 | 55 |
| Jun | 70 | 65 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Average = total / count.
**Say this in the interview:** "Product B totals 315 lakh over 6 months, so the average is 52.5 lakh."
**Answer:** **Rs 52.5 lakh per month**
**Step-by-step working:**
1. Total B = 50 + 40 + 60 + 45 + 55 + 65 = 315.
2. Number of months = 6.
3. Average = 315 / 6 = 52.5.
**Fast method (30 seconds):** Guess an average of 50 and add the gaps: 0, -10, +10, -5, +5, +15 = +15; 15 / 6 = 2.5; so 52.5.
**Check:** 52.5 x 6 = 315 (verified by script).
**Explain simply:**
- Average (mean) is what each month would be if all months were equal and the total stayed the same.
**Likely follow-ups:** Average of Product A? 320 / 6 = 53.33 lakh.
**Common mistakes / traps:** Dividing by 5 or by 2 (the number of products).

### Q12 ⭐⭐⭐ 🟢 In which month is the absolute difference between sales of Product A and Product B the largest?

Monthly sales (Rs lakh):

| Month | Product A | Product B |
|---|---|---|
| Jan | 40 | 50 |
| Feb | 45 | 40 |
| Mar | 55 | 60 |
| Apr | 50 | 45 |
| May | 60 | 55 |
| Jun | 70 | 65 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** "Absolute difference" means the size of the gap, ignoring which product is ahead.
**Say this in the interview:** "I take the gap each month: 10, 5, 5, 5, 5, 5. January is largest at 10 lakh."
**Answer:** **January (gap Rs 10 lakh)**
**Step-by-step working:**
1. Jan: |40 - 50| = 10.
2. Feb: |45 - 40| = 5.
3. Mar: |55 - 60| = 5.
4. Apr: |50 - 45| = 5.
5. May: |60 - 55| = 5.
6. Jun: |70 - 65| = 5.
7. The largest gap is January, 10 lakh (B ahead).
**Check:** every other month is exactly 5 (verified by script).
**Explain simply:**
- Absolute difference ignores the sign: B ahead by 10 and A ahead by 10 count the same.
**Likely follow-ups:** In how many months was A ahead? Four (Feb, Apr, May, Jun).
**Common mistakes / traps:** Ignoring the sign and picking a month where A is ahead, or stopping before January because the later gaps look the same.

### Q13 ⭐⭐⭐ 🟢 What should you read first when a chart or table is shown in a data interpretation set, and what common errors does this prevent?
**Asked at:** commonly asked (no company-specific report found); "read the title, units and footnotes first" is standard advice in prep material (unverified). Accenture-style guides name axis and unit misreading as the main error (prep sites, unverified).
**What the interviewer is checking:** Test discipline: whether you check the labels before calculating.
**Say this in the interview:** "I read the title, axis labels, units and any footnotes first, then the question. That stops unit and scale mistakes."
**Answer:** **Read the title, units (Rs, lakh, crore, thousand, %), axis labels and scale, legend and footnotes before touching the numbers.**
**Mini-example:**
1. A table says "Salary in Rs thousand per month" and shows 80. The real figure is Rs 80,000, not Rs 80.
2. A bar chart whose axis starts at 40 instead of 0 makes a 45 versus 50 gap look huge; read the numbers, not the bar heights.
**Explain simply:**
- Units: lakh versus crore, thousand versus million, count versus percentage.
- Axis: does it start at zero, and is the step uniform?
- Time and base: which year, whether figures are totals or per-person.
- Footnotes: "estimates" or "excluding contract staff" change the answer.
- Then choose the method; approximate when the options are far apart.
**Likely follow-ups:** What if units differ between two tables? Convert both to the same unit first (1 crore = 100 lakh).
**Common mistakes / traps:** Jumping straight into arithmetic; confusing percentage with absolute count; reading a percentage-point change as a percent change.

### Q14 ⭐⭐⭐ 🟢 How many candidates qualified in Test C?

Online test results:

| Test | Appeared | Qualified % |
|---|---|---|
| A | 400 | 40% |
| B | 500 | 30% |
| C | 600 | 35% |
| D | 250 | 48% |

**Asked at:** commonly asked (no company-specific report found); percentage-of-a-table-value is a core DI item (prep sites, unverified).
**What the interviewer is checking:** Applying a percentage to the right row's base.
**Say this in the interview:** "35% of 600 candidates is 0.35 x 600 = 210."
**Answer:** **210 candidates**
**Step-by-step working:**
1. Test C: appeared = 600, qualified = 35%.
2. 10% of 600 = 60, so 30% = 180.
3. 5% of 600 = 30.
4. 35% = 180 + 30 = 210.
**Fast method (30 seconds):** 35 x 6 = 210 (because 600 / 100 = 6 per percent).
**Check:** 210 / 600 = 0.35 (verified by script).
**Explain simply:**
- "Qualified %" is the share of those who appeared, so the appeared count is the base.
**Likely follow-ups:** Test D qualifiers? 48% of 250 = 120.
**Common mistakes / traps:** Using a different row's "Appeared" figure.

### Q15 ⭐⭐⭐ 🟢 A pie chart of 7,200 employees has a Sales sector with a central angle of 90 degrees. How many employees are in Sales?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Converting an angle to a fraction of the whole.
**Say this in the interview:** "90 degrees out of 360 is one quarter, so Sales is a quarter of 7,200, which is 1,800."
**Answer:** **1,800 employees**
**Step-by-step working:**
1. Fraction = 90 / 360 = 1/4.
2. Employees = 7,200 x 1/4 = 1,800.
**Fast method (30 seconds):** 90 degrees is a quarter (a right angle), so divide by 4.
**Check:** 1,800 / 7,200 = 25%, and 25% of 360 is 90 (verified by script).
**Explain simply:**
- Employees in a sector = (angle / 360) x total.
**Likely follow-ups:** A 60-degree sector? 60 / 360 = 1/6, so 1,200 employees.
**Common mistakes / traps:** Treating 90 as a percentage and taking 90% of 7,200.

### Q16 ⭐⭐⭐ 🟢 What is the average annual profit over the five years (Rs crore)?

Revenue and expenditure (Rs crore):

| Year | Revenue | Expenditure |
|---|---|---|
| 2021 | 80 | 64 |
| 2022 | 99 | 90 |
| 2023 | 110 | 88 |
| 2024 | 120 | 108 |
| 2025 | 150 | 120 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Profit = revenue - expenditure, then the mean of the five profits.
**Say this in the interview:** "Profits are 16, 9, 22, 12 and 30. They total 89, so the average is 17.8 crore."
**Answer:** **Rs 17.8 crore**
**Step-by-step working:**
1. 2021: 80 - 64 = 16.
2. 2022: 99 - 90 = 9.
3. 2023: 110 - 88 = 22.
4. 2024: 120 - 108 = 12.
5. 2025: 150 - 120 = 30.
6. Total = 16 + 9 + 22 + 12 + 30 = 89.
7. Average = 89 / 5 = 17.8.
**Fast method (30 seconds):** Total revenue 559 minus total expenditure 470 = 89, then divide by 5.
**Check:** 17.8 x 5 = 89 (verified by script).
**Explain simply:**
- Profit is what is left after costs; average profit is the total profit shared equally over the years.
**Likely follow-ups:** In which year was profit highest? 2025 (Rs 30 crore).
**Common mistakes / traps:** Averaging revenue and expenditure separately with a rounding slip, or dividing by 4.

### Q17 ⭐⭐⭐ 🟢 In a pie chart the sector angles for A, B and C are 72, 108 and 90 degrees, and D takes the rest. What percentage does D represent, and what does A represent?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Using 360 degrees as the total and converting angles to percentages.
**Say this in the interview:** "A, B and C use 270 degrees, so D gets 90 degrees, which is 25%. A is 72 out of 360, which is 20%."
**Answer:** **D = 25% (90 degrees); A = 20%.**
**Step-by-step working:**
1. A + B + C = 72 + 108 + 90 = 270 degrees.
2. D = 360 - 270 = 90 degrees.
3. D% = 90 / 360 x 100 = 25%.
4. A% = 72 / 360 x 100 = 20%.
**Fast method (30 seconds):** Divide an angle by 3.6 to get its percentage: 72 / 3.6 = 20; 90 / 3.6 = 25.
**Check:** B = 108 / 3.6 = 30%, C = 25%, so 20 + 30 + 25 + 25 = 100 (verified by script).
**Explain simply:**
- 360 degrees equals 100%; each 3.6 degrees is 1%.
**Likely follow-ups:** If the pie represents 2,000 people, how many are in B? 30% of 2,000 = 600.
**Common mistakes / traps:** Using 100 as the total of angles, or forgetting that D is "the rest".

### Q18 ⭐⭐⭐ 🟢 In which quarter did attrition fall the most compared with the previous quarter, and by how many percentage points?

Quarterly attrition rate (%):

| Quarter | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Attrition % | 12 | 15 | 10 | 14 |

**Asked at:** commonly asked (no company-specific report found); percentage points versus percent is a standard DI trap (prep sites, unverified).
**What the interviewer is checking:** Quarter-on-quarter differences in percentage points, and only counting falls.
**Say this in the interview:** "Changes are +3, -5, +4. The only fall is in Q3, down 5 percentage points."
**Answer:** **Q3, a fall of 5 percentage points (15% to 10%).**
**Step-by-step working:**
1. Q2 vs Q1: 15 - 12 = +3 (rise).
2. Q3 vs Q2: 10 - 15 = -5 (fall of 5).
3. Q4 vs Q3: 14 - 10 = +4 (rise).
4. Only one quarter fell: Q3.
**Check:** 15 - 5 = 10 (verified by script).
**Explain simply:**
- The question asks for percentage points (the plain subtraction of two rates), not percent change.
- In relative terms, the fall is 5 / 15 = 33.33%.
**Likely follow-ups:** Percent fall in Q3? 33.33%.
**Common mistakes / traps:** Choosing Q4 because 14 looks big, or answering "33.33%" when points are asked.

### Q19 ⭐⭐⭐ 🟡 What is the profit percentage on expenditure in 2024 (to 2 decimals)?

Revenue and expenditure (Rs crore):

| Year | Revenue | Expenditure |
|---|---|---|
| 2021 | 80 | 64 |
| 2022 | 99 | 90 |
| 2023 | 110 | 88 |
| 2024 | 120 | 108 |
| 2025 | 150 | 120 |

**Asked at:** commonly asked (no company-specific report found); profit percent is listed as a core DI item (prep sites, unverified).
**What the interviewer is checking:** That the base is expenditure (the cost), not revenue.
**Say this in the interview:** "2024 profit is 120 - 108 = 12; on expenditure of 108 that is 11.11%."
**Answer:** **11.11%** (rounded to 2 decimals; exactly 100/9 %)
**Step-by-step working:**
1. Profit = 120 - 108 = 12 crore.
2. Profit % on expenditure = 12 / 108 x 100.
3. 12 / 108 = 1/9 = 0.1111.
4. Percentage = 11.11%.
**Fast method (30 seconds):** 12/108 reduces to 1/9; 1/9 is 11.11%.
**Check:** 108 x 1.1111 = 120 (verified by script).
**Explain simply:**
- Profit % = profit / cost price x 100, so cost (expenditure) is the base.
- On revenue the margin would be 12 / 120 = 10%, a different number.
**Likely follow-ups:** Profit % on revenue in 2024? 10%.
**Common mistakes / traps:** Dividing by revenue (10%).

### Q20 ⭐⭐⭐ 🟡 What is the percentage growth in revenue from 2021 to 2025?

Revenue and expenditure (Rs crore):

| Year | Revenue | Expenditure |
|---|---|---|
| 2021 | 80 | 64 |
| 2022 | 99 | 90 |
| 2023 | 110 | 88 |
| 2024 | 120 | 108 |
| 2025 | 150 | 120 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Percent change across a multi-year gap, with the earlier year as base.
**Say this in the interview:** "Revenue went from 80 to 150, a rise of 70 on a base of 80, which is 87.5%."
**Answer:** **87.5%**
**Step-by-step working:**
1. Increase = 150 - 80 = 70 crore.
2. Growth = 70 / 80 x 100 = 87.5%.
**Fast method (30 seconds):** 70 / 80 = 7/8 = 0.875.
**Check:** 80 x 1.875 = 150 (verified by script).
**Explain simply:**
- This is total growth over four years, not a yearly rate. A per-year (compound) rate would be about 17% a year ((150/80)^(1/4) - 1 = 16.99%).
**Likely follow-ups:** Growth 2024 to 2025? 30 / 120 = 25%.
**Common mistakes / traps:** Using 150 as the base (46.67%), or dividing the 87.5% by 4 and calling it the yearly rate.

### Q21 ⭐⭐⭐ 🟡 In which year was the profit percentage on expenditure the lowest, and what was it?

Revenue and expenditure (Rs crore):

| Year | Revenue | Expenditure |
|---|---|---|
| 2021 | 80 | 64 |
| 2022 | 99 | 90 |
| 2023 | 110 | 88 |
| 2024 | 120 | 108 |
| 2025 | 150 | 120 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Computing a ratio for every year instead of picking the smallest profit.
**Say this in the interview:** "Profit percent on expenditure is 25, 10, 25, 11.11 and 25. The lowest is 2022 at 10%."
**Answer:** **2022, at 10%**
**Step-by-step working:**
1. 2021: 16 / 64 = 25%.
2. 2022: 9 / 90 = 10%.
3. 2023: 22 / 88 = 25%.
4. 2024: 12 / 108 = 11.11%.
5. 2025: 30 / 120 = 25%.
6. Lowest: 2022 (10%).
**Fast method (30 seconds):** Look at profit as a fraction of cost: 1/4, 1/10, 1/4, 1/9, 1/4. The smallest fraction is 1/10.
**Check:** 90 x 1.10 = 99 (verified by script).
**Explain simply:**
- The lowest profit amount (9 crore) is also in 2022 in this data, but that is a coincidence; always compute the ratios.
**Likely follow-ups:** Which year had the highest profit amount? 2025 (Rs 30 crore), though three years tie on percentage (25%).
**Common mistakes / traps:** Choosing 2024 (11.11%) because it looks low, without checking 2022.

### Q22 ⭐⭐⭐ 🟡 What is the total number of Tech employees in Company A and Company B together?

Two pie charts of department-wise employees. Company A has 8,000 employees and Company B has 12,000.

| Department | Company A % | Company B % |
|---|---|---|
| Sales | 30 | 25 |
| Tech | 40 | 30 |
| Operations | 20 | 35 |
| Admin | 10 | 10 |

**Asked at:** commonly asked (no company-specific report found); two-pie combination questions are standard (prep sites, unverified).
**What the interviewer is checking:** Applying each pie's percentage to its own total before adding.
**Say this in the interview:** "A has 40% of 8,000 = 3,200 Tech; B has 30% of 12,000 = 3,600. Together 6,800."
**Answer:** **6,800 employees**
**Step-by-step working:**
1. Company A Tech = 40% x 8,000 = 3,200.
2. Company B Tech = 30% x 12,000 = 3,600.
3. Total = 3,200 + 3,600 = 6,800.
**Fast method (30 seconds):** 40 x 80 = 3,200 and 30 x 120 = 3,600 (since 8,000 / 100 = 80, 12,000 / 100 = 120).
**Check:** 6,800 / 20,000 = 34%, between 30% and 40% (verified by script).
**Explain simply:**
- Each pie has its own total, so percentages from different pies cannot be added directly (40% + 30% = 70% would be meaningless).
**Likely follow-ups:** Admin employees in both? 800 + 1,200 = 2,000.
**Common mistakes / traps:** Adding 40% and 30% and taking 70% of 20,000 (14,000).

### Q23 ⭐⭐⭐ 🟡 How many more Operations employees does Company B have than Company A?

Two pie charts of department-wise employees. Company A has 8,000 employees and Company B has 12,000.

| Department | Company A % | Company B % |
|---|---|---|
| Sales | 30 | 25 |
| Tech | 40 | 30 |
| Operations | 20 | 35 |
| Admin | 10 | 10 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Converting each pie to counts before subtracting.
**Say this in the interview:** "B has 35% of 12,000 = 4,200 and A has 20% of 8,000 = 1,600. B has 2,600 more."
**Answer:** **2,600 more employees**
**Step-by-step working:**
1. Company B Operations = 35% x 12,000 = 4,200.
2. Company A Operations = 20% x 8,000 = 1,600.
3. Difference = 4,200 - 1,600 = 2,600.
**Fast method (30 seconds):** 35 x 120 = 4,200; 20 x 80 = 1,600.
**Check:** 1,600 + 2,600 = 4,200 (verified by script).
**Explain simply:**
- The percentage gap (35 - 20 = 15) is not the answer, because the two companies are different sizes.
**Likely follow-ups:** Which company has more Sales employees? A: 2,400; B: 3,000; B has more.
**Common mistakes / traps:** Taking 15% of either total (15% of 12,000 = 1,800 or 15% of 8,000 = 1,200).

### Q24 ⭐⭐⭐ 🟡 What percentage of the combined workforce of both companies is in Sales?

Two pie charts of department-wise employees. Company A has 8,000 employees and Company B has 12,000.

| Department | Company A % | Company B % |
|---|---|---|
| Sales | 30 | 25 |
| Tech | 40 | 30 |
| Operations | 20 | 35 |
| Admin | 10 | 10 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The weighted average: combined percentage depends on company sizes.
**Say this in the interview:** "Sales is 2,400 + 3,000 = 5,400 out of 20,000 employees, which is 27%."
**Answer:** **27%**
**Step-by-step working:**
1. Company A Sales = 30% x 8,000 = 2,400.
2. Company B Sales = 25% x 12,000 = 3,000.
3. Combined Sales = 5,400.
4. Combined workforce = 8,000 + 12,000 = 20,000.
5. Percentage = 5,400 / 20,000 x 100 = 27%.
**Fast method (30 seconds):** Weight by size, 2 : 3 (8,000 : 12,000): (2 x 30 + 3 x 25) / 5 = (60 + 75) / 5 = 27.
**Check:** 27% of 20,000 = 5,400 (verified by script).
**Explain simply:**
- A weighted average gives bigger companies more say. The plain average of 30 and 25 is 27.5%, which ignores that B is larger.
- The answer is closer to 25% (B) than to 30% (A), as expected since B is bigger.
**Likely follow-ups:** Combined Tech share? (3,200 + 3,600) / 20,000 = 34%.
**Common mistakes / traps:** Averaging 30 and 25 to get 27.5%.

### Q25 ⭐⭐⭐ 🟡 In which month did orders show the largest percentage increase over the previous month, and what was it?

Monthly orders processed:

| Month | Jan | Feb | Mar | Apr | May | Jun |
|---|---|---|---|---|---|---|
| Orders | 200 | 250 | 225 | 270 | 300 | 240 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Month-on-month percent change with the previous month as the base.
**Say this in the interview:** I work out each month's change divided by the month before. February is the biggest at 25 percent.
**Answer:** **February, with a 25% increase over January.**
**Step-by-step working:**
1. Feb: (250 - 200) / 200 = 50 / 200 = 25%.
2. Mar: (225 - 250) / 250 = -10% (a fall).
3. Apr: (270 - 225) / 225 = 45 / 225 = 20%.
4. May: (300 - 270) / 270 = 30 / 270 = 11.11%.
5. Jun: (240 - 300) / 300 = -20% (a fall).
6. The largest increase is 25% in February.
**Fast method (30 seconds):** April has the largest rise in orders (+45) but only 20%, because its base (225) is bigger than January's base (200). Scan the small bases first: 200 to 250 is a clean quarter, 25%.
**Check:** verified by script; going forward, 200 x 1.25 = 250.
**Explain simply:**
- Percent change = (this month - last month) / last month x 100. The base is the earlier month.
- A bigger absolute jump is not always a bigger percentage jump, because the base differs.
- Months with a fall (Mar, Jun) cannot win a question that asks for an increase.
**Likely follow-ups:** 1) *Which month had the largest absolute increase?* April, +45 orders. 2) *Largest fall in percent?* June, -20%, versus March at -10%.
**Common mistakes / traps:** Picking April because +45 is the biggest raw jump; dividing by the new month instead of the old (Feb would give 20%).

### Q26 ⭐⭐⭐ 🟡 What is the percentage decline in orders from February to March?

Monthly orders processed:

| Month | Jan | Feb | Mar | Apr | May | Jun |
|---|---|---|---|---|---|---|
| Orders | 200 | 250 | 225 | 270 | 300 | 240 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Percent decrease, with the earlier month as the base.
**Say this in the interview:** Orders fell from 250 to 225, a drop of 25. Over the starting 250, that is 10 percent.
**Answer:** **10% decline.**
**Step-by-step working:**
1. Orders in February = 250 (the base); orders in March = 225.
2. Change = 225 - 250 = -25.
3. -25 / 250 = -0.10.
4. So orders declined by 10%.
**Fast method (30 seconds):** 10% of 250 is 25, which is exactly the drop, so no long division is needed.
**Check:** verified by script; 250 x 0.90 = 225.
**Explain simply:**
- Decline percent = (old - new) / old x 100, base is the earlier value.
- A negative percent change simply means a fall; say "declined by 10%" rather than "-10% decline".
**Likely follow-ups:** 1) *What rise from March gets back to February's level?* 25 / 225 = 11.11%, not 10%. 2) *Percent change from Mar to Apr?* +20%.
**Common mistakes / traps:** Dividing by 225 (the new value) gives 11.11%, which is a wrong option the setter includes; saying the decline is 25 (units) when percent is asked.

### Q27 ⭐⭐⭐ 🟡 What is the total payroll and the weighted average salary of the three departments (Rs thousand per month)? Find Operations headcount first.

Payroll table (salary in Rs thousand per month):

| Department | Employees | Average salary | Total payroll |
|---|---|---|---|
| IT | 50 | 80 | 4000 |
| Operations | ? | 40 | 2000 |
| Finance | 25 | 70 | 1750 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Using total payroll = employees x average salary to fill a missing value, then a weighted average.
**Say this in the interview:** I back out Operations as 2000 divided by 40, which is 50 people. Then total payroll over total people gives the weighted average.
**Answer:** **Operations headcount = 50; total payroll = Rs 7,750 thousand per month; weighted average salary = Rs 62 thousand per month.**
**Step-by-step working:**
1. Total payroll = employees x average salary, so Operations employees = 2000 / 40 = 50.
2. Total payroll = 4000 + 2000 + 1750 = 7,750 (Rs thousand per month, which is Rs 77.5 lakh).
3. Total employees = 50 + 50 + 25 = 125.
4. Weighted average salary = 7,750 / 125 = 62 (Rs thousand per month).
5. Check the Finance row: 25 x 70 = 1750, consistent.
**Fast method (30 seconds):** Weighted average = total payroll / total headcount. 125 x 62 = 7,750, so it is easy to confirm. Do not average 80, 40, 70.
**Check:** verified by script; 125 x 62 = 7,750.
**Explain simply:**
- A "weighted" average counts each department by how many people it has.
- Payroll (Rs) = headcount x average salary, so any one of the three can be found from the other two.
- Units: salary is in Rs thousand, so 62 means Rs 62,000 per person per month.
**Likely follow-ups:** 1) *If Finance added 25 more people at 70?* Payroll 9,500, headcount 150, average 63.33. 2) *Which department has the largest payroll share?* IT, 4000 / 7750 = 51.6%.
**Common mistakes / traps:** Simple-averaging the three department salaries (63.33); forgetting the units (Rs thousand); leaving the Operations headcount as a guess.

### Q28 ⭐⭐⭐ 🟡 Why is the overall average salary not the simple average of the department averages? Compute both for this table, using Operations headcount from its payroll.

Payroll table (salary in Rs thousand per month):

| Department | Employees | Average salary | Total payroll |
|---|---|---|---|
| IT | 50 | 80 | 4000 |
| Operations | ? | 40 | 2000 |
| Finance | 25 | 70 | 1750 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Knowing why averages of averages mislead and when to weight.
**Say this in the interview:** A simple average treats a 25-person team the same as a 50-person team. The true overall average divides total payroll by total headcount: 62, against a simple 63.33.
**Answer:** **Weighted (true overall) average = Rs 62 thousand per month; simple average of department averages = Rs 63.33 thousand per month (rounded to 2 decimals). They differ because department sizes differ.**
**Step-by-step working:**
1. Operations headcount = 2000 / 40 = 50.
2. Simple average of averages = (80 + 40 + 70) / 3 = 190 / 3 = 63.33.
3. True overall average = total payroll / total employees = (4000 + 2000 + 1750) / (50 + 50 + 25) = 7,750 / 125 = 62.
4. The gap (63.33 vs 62) arises because Operations (low salary, 40) has 50 people, a larger weight than Finance (70, only 25 people), so it pulls the real average down.
**Fast method (30 seconds):** Ask: are the groups the same size? If not, weight by headcount. Here weights are 50 : 50 : 25 = 2 : 2 : 1, so (2x80 + 2x40 + 1x70) / 5 = 310 / 5 = 62.
**Check:** verified by script.
**Explain simply:**
- Each department average already hides how many people it covers; a mean of means ignores that.
- Weights are the group sizes. The simple average is right only when all groups are equal in size.
- This is the same reason an overall attrition rate is not the mean of team attrition rates.
**Likely follow-ups:** 1) *When would the simple average equal the weighted one?* If all departments had equal headcount. 2) *Overall average if Operations had 25 people?* Payroll 4000 + 1000 + 1750 = 6750, headcount 100, average 67.5.
**Common mistakes / traps:** Reporting 63.33 as the company average; forgetting to find Operations headcount before averaging.

### Q29 ⭐⭐⭐ 🟡 What is the overall qualification percentage across all four tests (to 2 decimals)?

Online test results:

| Test | Appeared | Qualified % |
|---|---|---|
| A | 400 | 40% |
| B | 500 | 30% |
| C | 600 | 35% |
| D | 250 | 48% |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Weighted percentage: convert each percent to a count, then divide total qualified by total appeared.
**Say this in the interview:** I turn each percentage into a head count, add them up, and divide by total candidates. 640 out of 1,750 is 36.57 percent.
**Answer:** **36.57% (640 qualified out of 1,750 appeared).**
**Step-by-step working:**
1. Test A: 40% of 400 = 160.
2. Test B: 30% of 500 = 150.
3. Test C: 35% of 600 = 210.
4. Test D: 48% of 250 = 120.
5. Total qualified = 160 + 150 + 210 + 120 = 640.
6. Total appeared = 400 + 500 + 600 + 250 = 1,750.
7. Overall % = 640 / 1,750 x 100 = 36.571...%, which is 36.57% to 2 decimals.
**Fast method (30 seconds):** Simple average of the four percentages is (40 + 30 + 35 + 48) / 4 = 38.25, which is wrong. The answer must lie near the big tests (B, C): about 36 to 37, so 36.57 fits.
**Check:** verified by script; 1,750 x 0.3657 = 640.
**Explain simply:**
- Percentages from different-sized groups cannot be averaged directly; go back to counts.
- Overall rate = total successes / total attempts.
**Likely follow-ups:** 1) *Which test had the most qualified candidates?* C, 210. 2) *Overall percentage if Test D is dropped?* 490 / 1,500 = 32.67%.
**Common mistakes / traps:** Taking the plain average of the four percentages (38.25%), the trap option.

### Q30 ⭐⭐⭐ 🟡 Product A's June sales are what percentage of its January to June total (to 2 decimals)?

Monthly sales (Rs lakh):

| Month | Product A | Product B |
|---|---|---|
| Jan | 40 | 50 |
| Feb | 45 | 40 |
| Mar | 55 | 60 |
| Apr | 50 | 45 |
| May | 60 | 55 |
| Jun | 70 | 65 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Share of total: part divided by sum of the series.
**Say this in the interview:** I add Product A's six months to get 320, then June's 70 over 320, about 21.88 percent.
**Answer:** **21.88% (70 / 320 = 21.875%, rounded to 2 decimals).**
**Step-by-step working:**
1. Product A, Jan to Jun: 40 + 45 + 55 + 50 + 60 + 70 = 320 (Rs lakh).
2. June = 70.
3. 70 / 320 = 0.21875.
4. x 100 = 21.875%, which rounds to 21.88% (rounding half up).
**Fast method (30 seconds):** 70 / 320 = 7 / 32. Since 1 / 32 = 3.125%, 7 x 3.125 = 21.875%.
**Check:** verified by script.
**Explain simply:**
- Share (%) = part / whole x 100, and the whole is the total of the row, not the biggest month.
- Here the exact value ends in 5 at the third decimal; 21.88 comes from rounding half up.
**Likely follow-ups:** 1) *Which month's share is smallest for A?* January, 40 / 320 = 12.5%. 2) *Share of Product B's June in B's total?* 65 / 315 = 20.63%.
**Common mistakes / traps:** Dividing by 70 or by the sum including Product B (635); mixing up the two products' columns.

### Q31 ⭐⭐⭐ 🟡 By what percentage were Product B's March sales higher than its February sales?

Monthly sales (Rs lakh):

| Month | Product A | Product B |
|---|---|---|
| Jan | 40 | 50 |
| Feb | 45 | 40 |
| Mar | 55 | 60 |
| Apr | 50 | 45 |
| May | 60 | 55 |
| Jun | 70 | 65 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Percent difference with the earlier month as the base.
**Say this in the interview:** B went from 40 in February to 60 in March, a rise of 20 on a base of 40, so 50 percent.
**Answer:** **50% higher.**
**Step-by-step working:**
1. Product B: February = 40 (base), March = 60.
2. Difference = 60 - 40 = 20.
3. 20 / 40 = 0.5 = 50%.
**Fast method (30 seconds):** 60 is one and a half times 40, so it is 50% more.
**Check:** verified by script; 40 x 1.5 = 60.
**Explain simply:**
- "Higher than February" makes February the base.
- The reverse question (February lower than March by what percent) uses March as base: 20 / 60 = 33.33%.
**Likely follow-ups:** 1) *By what percent is February lower than March?* 33.33%. 2) *Product A, Feb to Mar?* (55 - 45) / 45 = 22.22%.
**Common mistakes / traps:** Dividing by 60 (giving 33.33%); reading Product A's column by mistake.

### Q32 ⭐⭐⭐ 🟡 What is the percent change (not percentage points) in attrition from Q2 to Q3?

Quarterly attrition rate (%):

| Quarter | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Attrition % | 12 | 15 | 10 | 14 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Distinguishing percent change from percentage-point change.
**Say this in the interview:** Attrition went from 15 percent to 10 percent. That is 5 percentage points down, which is a one-third fall in percent terms: minus 33.33 percent.
**Answer:** **-33.33% (a fall of one third); in percentage points the fall is 5 points.**
**Step-by-step working:**
1. Q2 attrition = 15% (base); Q3 attrition = 10%.
2. Percentage-point change = 10 - 15 = -5 points.
3. Percent change = (10 - 15) / 15 x 100 = -5 / 15 x 100 = -33.33%.
**Fast method (30 seconds):** 5 is one third of 15, so the fall is one third, 33.33%.
**Check:** verified by script; 15 x (1 - 1/3) = 10.
**Explain simply:**
- Percentage points are the simple subtraction of two percentages.
- Percent change compares that gap with the starting percentage.
- The question says "not percentage points" so -5 is the wrong answer.
**Likely follow-ups:** 1) *Percent change Q3 to Q4 (10 to 14)?* +40%. 2) *Percentage-point change Q1 to Q4?* +2 points.
**Common mistakes / traps:** Answering 5% (the points) or dividing by 10 (giving 50%).

### Q33 ⭐⭐⭐ 🟡 When should you approximate in data interpretation, and how do you keep rounding errors from changing the answer?

**Asked at:** commonly asked (no company-specific report found); CAT-style prep sources advise approximating when options are far apart and rounding late.
**What the interviewer is checking:** Time management and numerical judgement: speed without losing the right option.
**Say this in the interview:** I approximate when the options are well separated and round only at the end, never in the middle of a calculation.
**Answer:** **Approximate when answer options are far apart, and keep full precision in intermediate steps, rounding only the final answer.**
**Step-by-step working:**
1. Look at the options first: if they differ by more than a few percent, round the inputs (for example 4,987 to 5,000).
2. If options are close (like 36.57 and 36.75), compute exactly.
3. Round numbers to the same degree in both numerator and denominator, so errors partly cancel.
4. Never round percentages and then reuse them; return to counts.
5. Round only the final answer, as the question asks (e.g. 2 decimals).
6. Example: 49 / 205. Approximating as 50 / 200 = 25%; exact is 23.9%. If options are 25, 35, 45, 55 pick 25; if options are 23.9 and 25.0, compute exactly.
**Fast method (30 seconds):** Approximate, then test whether the estimate separates the options. If rounding up and rounding down both point to the same option, stop.
**Check:** Rounding 49 / 205 to 50 / 200 gives 25%, but the exact value is 23.9%, so a close pair of options needs exact working.
**Explain simply:**
- Approximation saves time; the risk is picking among close options.
- Early rounding compounds: round 36.57% to 37%, multiply by 1,000 and you are off by 4 people.
**Likely follow-ups:** 1) *Round 33.33% up to 33% and use it for 900?* 297 instead of 300. 2) *When is exact working a must?* When options differ by under 1%.
**Common mistakes / traps:** Rounding every intermediate step; approximating when options are close; rounding one side only.

### Q34 ⭐⭐⭐ 🟡 In a company of 800 employees, 55% are male. 40% of males and 30% of females work in Tech. How many employees work in Tech?

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Two-stage percentage (split into groups, then apply a different rate to each).
**Say this in the interview:** I split 800 into 440 males and 360 females, then take 40 percent of males and 30 percent of females, and add: 176 plus 108 is 284.
**Answer:** **284 employees work in Tech.**
**Step-by-step working:**
1. Males = 55% of 800 = 440.
2. Females = 800 - 440 = 360 (45%).
3. Male Tech = 40% of 440 = 176.
4. Female Tech = 30% of 360 = 108.
5. Total Tech = 176 + 108 = 284.
**Fast method (30 seconds):** Weighted rate = 0.55 x 40% + 0.45 x 30% = 22% + 13.5% = 35.5%. And 35.5% of 800 = 284.
**Check:** verified by script; 284 / 800 = 35.5%.
**Explain simply:**
- Each group has its own rate, so the overall rate is a weighted average.
- 40% and 30% do not average to 35%, because the male group is larger.
**Likely follow-ups:** 1) *What share of the Tech team is male?* 176 / 284 = 61.97%. 2) *Overall Tech rate?* 35.5%.
**Common mistakes / traps:** Using (40 + 30) / 2 = 35% of 800 = 280; forgetting that 30% is for the female group, not for all.

### Q35 ⭐⭐⭐ 🟡 A company starts the year with 500 employees. 60 leave and 80 join during the year. What is the attrition rate on average headcount (to 2 decimals)?

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Attrition rate definition: leavers divided by average headcount.
**Say this in the interview:** End headcount is 500 minus 60 plus 80, which is 520. Average is 510. Leavers 60 over 510 is 11.76 percent.
**Answer:** **11.76% attrition on average headcount (60 / 510).**
**Step-by-step working:**
1. Closing headcount = 500 - 60 + 80 = 520.
2. Average headcount = (500 + 520) / 2 = 510.
3. Attrition rate = leavers / average headcount x 100 = 60 / 510 x 100 = 11.7647...%.
4. Rounded to 2 decimals: 11.76%.
**Fast method (30 seconds):** 60 / 510 = 6 / 51 = 2 / 17, and 1 / 17 is about 5.88%, so 2 / 17 is 11.76%.
**Check:** verified by script. (Against opening headcount only it would be 12%.)
**Explain simply:**
- Attrition rate (%) = employees who left / average headcount x 100.
- Average headcount is (opening + closing) / 2, because people left and joined during the year.
- Joiners do not count as leavers; they only change the average.
**Likely follow-ups:** 1) *Attrition on opening headcount?* 60 / 500 = 12%. 2) *If 100 joined instead?* Closing 540, average 520, rate 11.54%.
**Common mistakes / traps:** Using 500 or 520 as the base; subtracting joiners from leavers (20); forgetting to average.

### Q36 ⭐⭐⭐ 🟡 Which region has the highest percentage growth in sales from 2024 to 2025, and what is the overall growth percentage (to 2 decimals)?

Regional sales (Rs crore):

| Region | 2024 | 2025 |
|---|---|---|
| North | 120 | 141 |
| South | 90 | 108 |
| East | 60 | 57 |
| West | 150 | 165 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Percent growth per row, and total-versus-row growth.
**Say this in the interview:** I work growth for each region on its own base. South leads at 20 percent. Overall, 420 to 471 is 12.14 percent.
**Answer:** **South has the highest growth, 20%; overall growth is 12.14% (420 to 471).**
**Step-by-step working:**
1. North: (141 - 120) / 120 = 21 / 120 = 17.5%.
2. South: (108 - 90) / 90 = 18 / 90 = 20%.
3. East: (57 - 60) / 60 = -5%.
4. West: (165 - 150) / 150 = 10%.
5. Highest percentage growth = South, 20%.
6. Total 2024 = 120 + 90 + 60 + 150 = 420; total 2025 = 141 + 108 + 57 + 165 = 471.
7. Overall growth = (471 - 420) / 420 = 51 / 420 = 12.142...%, which is 12.14%.
**Fast method (30 seconds):** South's 18 on 90 is one fifth (20%). North's 21 on 120 is 17.5%. Compare quickly by checking 18 / 90 versus 21 / 120.
**Check:** verified by script; 420 x 1.1214 = 471.
**Explain simply:**
- Compute growth on each region's own 2024 base.
- The overall growth uses the totals, not the average of four growth rates (which would give 10.63%).
**Likely follow-ups:** 1) *Which region fell?* East, -5%. 2) *Overall growth ignoring East?* Without East, 2024 is 360 and 2025 is 414, so 54 / 360 = 15%.
**Common mistakes / traps:** Picking North (largest rupee increase, 21); averaging the four percentages for the overall figure.

### Q37 ⭐⭐⭐ 🟡 Which region contributed the largest absolute increase in sales, and how does that differ from the region with the highest percentage growth?

Regional sales (Rs crore):

| Region | 2024 | 2025 |
|---|---|---|
| North | 120 | 141 |
| South | 90 | 108 |
| East | 60 | 57 |
| West | 150 | 165 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Absolute versus relative growth.
**Say this in the interview:** North added the most money, 21 crore. South grew fastest in percent, 20 percent, because its base is smaller.
**Answer:** **North has the largest absolute increase (Rs 21 crore); South has the highest percentage growth (20%). They differ because South's starting base (90) is smaller than North's (120).**
**Step-by-step working:**
1. Absolute change: North = 141 - 120 = +21; South = 108 - 90 = +18; East = 57 - 60 = -3; West = 165 - 150 = +15.
2. Largest absolute increase: North, Rs 21 crore.
3. Percent growth: North 21 / 120 = 17.5%; South 18 / 90 = 20%; East -5%; West 10%.
4. Highest percent growth: South, 20%.
5. They differ: North wins on rupees, South on percent.
**Fast method (30 seconds):** Do two passes: scan the difference column for the biggest number, then divide each by its base only for the leading candidates.
**Check:** verified by script.
**Explain simply:**
- Absolute change is a difference; percent growth is that difference relative to the starting size.
- A smaller base lets a smaller addition give a higher percentage.
- Use absolute for "how much more money", percent for "how fast it grew".
**Likely follow-ups:** 1) *Which region had the largest percent fall?* East, -5%. 2) *Whose share of total rose most?* Check shares: South 21.43% to 22.93%.
**Common mistakes / traps:** Assuming the biggest rupee gain is also the biggest percent gain.

### Q38 ⭐⭐⭐ 🟡 What is West's share of total 2025 sales (to 2 decimals)?

Regional sales (Rs crore):

| Region | 2024 | 2025 |
|---|---|---|
| North | 120 | 141 |
| South | 90 | 108 |
| East | 60 | 57 |
| West | 150 | 165 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Share of total from a table column.
**Say this in the interview:** West is 165 of a 2025 total of 471, which is 35.03 percent.
**Answer:** **35.03% (165 / 471).**
**Step-by-step working:**
1. 2025 total = 141 + 108 + 57 + 165 = 471.
2. West 2025 = 165.
3. 165 / 471 = 0.35031...
4. x 100 = 35.03% (2 decimals).
**Fast method (30 seconds):** Estimate: 471 is a bit under 500, one third of 471 is 157, and 165 is a bit more, so slightly above 33.3%, so about 35%.
**Check:** verified by script; 471 x 0.3503 = 165.0.
**Explain simply:**
- Share = part / total x 100 for the same year.
- The 2024 total (420) is the wrong whole.
**Likely follow-ups:** 1) *West's share in 2024?* 150 / 420 = 35.71%. 2) *Did West's share rise or fall?* Fell by 0.68 percentage points.
**Common mistakes / traps:** Dividing by the 2024 total or by the other three regions only; mixing the years.

### Q39 ⭐⭐⭐ 🟡 What is the combined amount (Rs crore) spent on Marketing and Miscellaneous?

Pie chart of annual expenses of Rs 8 crore: Salaries 45%, Rent 15%, Marketing 12%, Technology 18%, Miscellaneous 10%.

**Asked at:** a pie chart with percentages and follow-up questions was reported in a 2025 Glassdoor Novartis review (seen only via a search summary; mapping to this exact question not verified); otherwise commonly asked
**What the interviewer is checking:** Reading pie percentages and converting a share into rupees of the total.
**Say this in the interview:** Marketing and Miscellaneous together are 22 percent of Rs 8 crore, which is Rs 1.76 crore.
**Answer:** **Rs 1.76 crore.**
**Step-by-step working:**
1. Marketing = 12% of 8 = 0.96 crore.
2. Miscellaneous = 10% of 8 = 0.80 crore.
3. Together = 0.96 + 0.80 = 1.76 crore.
4. Or add shares first: 12% + 10% = 22%; 22% of 8 = 1.76.
**Fast method (30 seconds):** Add the percentages first, then multiply once: 22 x 8 = 176, and move the decimal two places.
**Check:** verified by script; the five shares add to 100%.
**Explain simply:**
- Pie sector = share of the whole; amount = share x total.
- Adding shares first is quicker and avoids rounding.
**Likely follow-ups:** 1) *How much is Rent?* 15% of 8 = Rs 1.2 crore. 2) *Salaries minus Technology?* 27% of 8 = Rs 2.16 crore.
**Common mistakes / traps:** Reading the shares as rupees directly (22 crore); using 8 crore as lakh; forgetting that the shares total 100%.

### Q40 ⭐⭐⭐ 🟡 If salary expenses rise by 10% and all other expenses stay the same, what is the new share of salaries in total expense (to 2 decimals)?

Pie chart of annual expenses of Rs 8 crore: Salaries 45%, Rent 15%, Marketing 12%, Technology 18%, Miscellaneous 10%.

**Asked at:** a pie chart with percentages and follow-up questions was reported in a 2025 Glassdoor Novartis review (seen only via a search summary; mapping to this exact question not verified); otherwise commonly asked
**What the interviewer is checking:** Recomputing a share when one slice changes (the total changes too).
**Say this in the interview:** Salaries go from 3.6 to 3.96 crore, the total goes from 8 to 8.36, so the new share is 47.37 percent, not 55 percent.
**Answer:** **47.37% (3.96 / 8.36).**
**Step-by-step working:**
1. Salaries now = 45% of 8 = Rs 3.6 crore.
2. 10% rise: 3.6 x 1.10 = Rs 3.96 crore.
3. Other expenses = 8 - 3.6 = Rs 4.4 crore (unchanged).
4. New total = 3.96 + 4.4 = Rs 8.36 crore.
5. New share = 3.96 / 8.36 = 0.47368.
6. = 47.37% (2 decimals).
**Fast method (30 seconds):** A 10% rise in a 45% slice cannot lift the share by 10%, since the total grows too. Estimate: 3.96 / 8.36 is just under 4 / 8.4, about 47.6, so 47.37% fits.
**Check:** verified by script; 8.36 x 0.4737 = 3.96.
**Explain simply:**
- When one slice grows, the whole grows, so every other slice's share shrinks.
- The share rose from 45% to 47.37%, a gain of 2.37 percentage points.
**Likely follow-ups:** 1) *New Rent share?* 1.2 / 8.36 = 14.35%. 2) *By what percent does the total rise?* 0.36 / 8 = 4.5%.
**Common mistakes / traps:** Answering 55% (adding 10 points) or 49.5% (45 x 1.1) by keeping the total at 8.

### Q41 ⭐⭐⭐ 🟡 What is the central angle of the Technology sector, and what is the sum of all sector angles in any pie chart?

Pie chart of annual expenses of Rs 8 crore: Salaries 45%, Rent 15%, Marketing 12%, Technology 18%, Miscellaneous 10%.

**Asked at:** a pie chart with percentages and follow-up questions was reported in a 2025 Glassdoor Novartis review (seen only via a search summary; mapping to this exact question not verified); otherwise commonly asked
**What the interviewer is checking:** Pie-chart angles: share x 360.
**Say this in the interview:** A full circle is 360 degrees. Technology is 18 percent of that: 64.8 degrees.
**Answer:** **Technology sector angle = 64.8 degrees; all sector angles in any pie chart add to 360 degrees.**
**Step-by-step working:**
1. 100% of the pie = 360 degrees, so 1% = 3.6 degrees.
2. Technology = 18% x 360 = 18 x 3.6 = 64.8 degrees.
3. Sum check for this chart: (45 + 15 + 12 + 18 + 10)% = 100%, so angles are 162 + 54 + 43.2 + 64.8 + 36 = 360 degrees.
**Fast method (30 seconds):** Multiply the percentage by 3.6. 18 x 3.6 = 64.8 (18 x 4 = 72, minus 18 x 0.4 = 7.2).
**Check:** verified by script.
**Explain simply:**
- A pie is a circle, so its slices sum to 360 degrees (100%).
- angle = share x 360; share = angle / 360.
**Likely follow-ups:** 1) *Angle for Salaries?* 162 degrees. 2) *A sector of 90 degrees is what share?* 25%.
**Common mistakes / traps:** Using 100 or 180 as the total; mixing up the share with the angle.

### Q42 ⭐⭐⭐ 🔴 If revenue is Rs 100 crore in year 1 and Rs 144 crore in year 3 with the same growth each year, what is the yearly growth rate? Write the CAGR formula.

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** CAGR (compound annual growth rate) and compounding over periods.
**Say this in the interview:** Year 1 to year 3 is two growth steps. The multiplier is 144 over 100, 1.44, and its square root is 1.2, so 20 percent a year.
**Answer:** **20% per year. CAGR = (End value / Start value)^(1 / number of years) - 1.**
**Step-by-step working:**
1. Growth steps from year 1 to year 3 = 3 - 1 = 2 (not 3).
2. Total growth factor = 144 / 100 = 1.44.
3. Per-year factor = square root of 1.44 = 1.2.
4. Rate = 1.2 - 1 = 20%.
5. Check: 100 x 1.2 = 120; 120 x 1.2 = 144.
**Fast method (30 seconds):** Recognise 144 = 12 x 12 and 100 = 10 x 10, so the factor is 12 / 10 = 1.2. Compound growth multiplies, so find the root, not the half.
**Check:** verified by script; 100 x 1.2 x 1.2 = 144.
**Explain simply:**
- CAGR is the constant yearly rate that gives the same start-to-end result.
- Simple division (44% / 2 = 22%) ignores compounding.
- Count the number of intervals between years, not the number of years.
**Likely follow-ups:** 1) *What if it were 100 to 169 over 2 years?* 13%. 2) *Year 4 revenue at the same rate?* 144 x 1.2 = 172.8 crore.
**Common mistakes / traps:** Dividing 44% by 2 for 22%; using 3 years in the formula.

### Q43 ⭐⭐⭐ 🔴 Revenue grows 20% in the first year and 50% in the second year. Why is the average yearly growth not 35%, and what is the total two-year growth?

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Compound growth: multiply growth factors, never average percentages.
**Say this in the interview:** 20 percent then 50 percent means 1.2 times 1.5, which is 1.8, so 80 percent in total. The yearly average is about 34.16 percent, not 35, because the second 50 percent applies to a bigger base.
**Answer:** **Total two-year growth = 80%. The average yearly (compound) growth is 34.16%, not 35%, because growth compounds.**
**Step-by-step working:**
1. Take a start of 100. After year 1: 100 x 1.20 = 120.
2. After year 2: 120 x 1.50 = 180.
3. Total growth = (180 - 100) / 100 = 80%.
4. Simple averaging gives (20 + 50) / 2 = 35% a year, which would give 100 x 1.35 x 1.35 = 182.25, too high.
5. The true constant rate: square root of 1.8 = 1.3416, so 34.16% a year.
**Fast method (30 seconds):** Use growth factors: 1.2 x 1.5 = 1.8. A quick trap check: 20 + 50 = 70 is not 80, because 20% of 50% adds the 10 extra.
**Check:** verified by script; 1.3416^2 = 1.8.
**Explain simply:**
- The second year's 50% is on 120, not on 100, so it adds 60, not 50.
- Cross-effect: 20% + 50% + (20% x 50%) = 80%.
- The average that works across years is the geometric mean (CAGR), not the arithmetic mean.
**Likely follow-ups:** 1) *Growth of +20% then -20%?* 1.2 x 0.8 = 0.96, a 4% fall overall. 2) *What if year 2 growth is 25%?* 1.2 x 1.25 = 1.5, so 50%.
**Common mistakes / traps:** Answering 70% (adding) or 35% a year; saying +20% then -20% returns to the start.

### Q44 ⭐⭐⭐ 🔴 In which quarter did the company make a loss, and what is the profit percentage on cost for Q4?

Quarterly revenue and cost (Rs lakh):

| Quarter | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Revenue | 50 | 55 | 60 | 70 |
| Cost | 40 | 52 | 62 | 60 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Profit = revenue - cost, and profit percent on cost uses cost as the base.
**Say this in the interview:** Only Q3 is a loss, with costs of 62 against revenue of 60. Q4 makes 10 on a cost of 60, which is 16.67 percent.
**Answer:** **Q3 was the loss quarter (Rs 2 lakh loss). Q4 profit percentage on cost = 16.67%.**
**Step-by-step working:**
1. Profit per quarter = revenue - cost: Q1 = 50 - 40 = +10; Q2 = 55 - 52 = +3; Q3 = 60 - 62 = -2; Q4 = 70 - 60 = +10.
2. The only negative is Q3, so Q3 made a loss of Rs 2 lakh.
3. Q4 profit = 10; cost = 60.
4. Profit % on cost = 10 / 60 x 100 = 16.666...%, so 16.67%.
**Fast method (30 seconds):** Scan the revenue and cost rows: only in Q3 does cost exceed revenue. For Q4, 10 / 60 = 1 / 6 = 16.67%.
**Check:** verified by script; 60 x 1.1667 = 70.
**Explain simply:**
- Profit percentage on cost = profit / cost x 100; on revenue it would be profit / revenue (10 / 70 = 14.29%).
- Use the base that the question names.
**Likely follow-ups:** 1) *Q4 profit percentage on revenue?* 14.29%. 2) *Q1 profit % on cost?* 10 / 40 = 25%.
**Common mistakes / traps:** Dividing by revenue (14.29%); calling Q2 a loss since its profit is small.

### Q45 ⭐⭐⭐ 🔴 What is the total profit (or loss) in Rs lakh across the four quarters?

Quarterly revenue and cost (Rs lakh):

| Quarter | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Revenue | 50 | 55 | 60 | 70 |
| Cost | 40 | 52 | 62 | 60 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Aggregating signed values (profits and losses) across periods.
**Say this in the interview:** I work out profit each quarter, with a minus sign for the loss quarter, and add them. Total is a profit of 21 lakh.
**Answer:** **Total profit = Rs 21 lakh (a profit, not a loss).**
**Step-by-step working:**
1. Quarterly results: Q1 +10, Q2 +3, Q3 -2, Q4 +10.
2. Sum = 10 + 3 - 2 + 10 = 21.
3. Cross-check with totals: revenue = 50 + 55 + 60 + 70 = 235; cost = 40 + 52 + 62 + 60 = 214; 235 - 214 = 21.
**Fast method (30 seconds):** Total revenue minus total cost in one step: 235 - 214 = 21.
**Check:** verified by script; both routes give 21.
**Explain simply:**
- Profit = revenue - cost; a loss counts as a negative number and reduces the total.
- The one loss quarter does not make the year a loss.
**Likely follow-ups:** 1) *Overall profit % on cost?* 21 / 214 = 9.81%. 2) *If Q3 cost were 66?* Total 17.
**Common mistakes / traps:** Adding the loss as +2 (giving 25); ignoring Q3 (giving 23).

### Q46 ⭐⭐ 🟢 What is the overall average score of all employees across the three batches?

Training batches:

| Batch | Employees | Average score |
|---|---|---|
| 1 | 20 | 70 |
| 2 | 30 | 80 |
| 3 | 50 | 90 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Weighted average across groups of unequal size.
**Say this in the interview:** Total marks are 20 times 70 plus 30 times 80 plus 50 times 90, so 8,300 over 100 people: 83.
**Answer:** **83.**
**Step-by-step working:**
1. Batch 1 total = 20 x 70 = 1,400.
2. Batch 2 total = 30 x 80 = 2,400.
3. Batch 3 total = 50 x 90 = 4,500.
4. Total score = 1,400 + 2,400 + 4,500 = 8,300.
5. Total employees = 20 + 30 + 50 = 100.
6. Overall average = 8,300 / 100 = 83.
**Fast method (30 seconds):** Weights 20 : 30 : 50 sum to 100: 0.2 x 70 + 0.3 x 80 + 0.5 x 90 = 14 + 24 + 45 = 83. The simple average (80) is too low because the biggest batch scores highest.
**Check:** verified by script.
**Explain simply:**
- Weighted average = sum of (count x average) / total count.
- The biggest group pulls the overall average toward its own value.
**Likely follow-ups:** 1) *Overall average if batch 3 had only 10 employees?* (1,400 + 2,400 + 900) / 60 = 78.33. 2) *Simple average?* 80.
**Common mistakes / traps:** Answering 80 (simple mean of 70, 80, 90).

### Q47 ⭐⭐ 🟢 Which product sold more in total from January to June, and by how much (Rs lakh)?

Monthly sales (Rs lakh):

| Month | Product A | Product B |
|---|---|---|
| Jan | 40 | 50 |
| Feb | 45 | 40 |
| Mar | 55 | 60 |
| Apr | 50 | 45 |
| May | 60 | 55 |
| Jun | 70 | 65 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Totaling a column and comparing two series.
**Say this in the interview:** A totals 320 and B totals 315, so A sold more, by 5 lakh.
**Answer:** **Product A sold more, by Rs 5 lakh (A = 320, B = 315).**
**Step-by-step working:**
1. Product A: 40 + 45 + 55 + 50 + 60 + 70 = 320.
2. Product B: 50 + 40 + 60 + 45 + 55 + 65 = 315.
3. Difference = 320 - 315 = 5.
4. A is higher by Rs 5 lakh (about 1.59% of B's total).
**Fast method (30 seconds):** Add month-by-month differences (A - B): -10, +5, -5, +5, +5, +5 = +5. Only six small numbers.
**Check:** verified by script; both methods give 5.
**Explain simply:**
- Total over the period = sum of all months.
- Differences can be summed directly, which saves adding two long columns.
**Likely follow-ups:** 1) *By what percent does A exceed B?* 5 / 315 = 1.59%. 2) *Which product has the higher average month?* A, 53.33 vs 52.5.
**Common mistakes / traps:** Judging by one month only (June) instead of the six-month totals; arithmetic slips when adding long columns.

### Q48 ⭐⭐ 🟢 In how many months did Product A outsell Product B?

Monthly sales (Rs lakh):

| Month | Product A | Product B |
|---|---|---|
| Jan | 40 | 50 |
| Feb | 45 | 40 |
| Mar | 55 | 60 |
| Apr | 50 | 45 |
| May | 60 | 55 |
| Jun | 70 | 65 |

**Asked at:** commonly asked (no company-specific report found); data interpretation sits in TCS NQT, Accenture and similar aptitude gates per prep sites (unverified)
**What the interviewer is checking:** Row-by-row comparison and counting from a table.
**Say this in the interview:** I compare A with B month by month: A is ahead in February, April, May and June, so 4 months.
**Answer:** **4 months (Feb, Apr, May and Jun).**
**Step-by-step working:**
1. Jan: A 40 vs B 50, B higher.
2. Feb: A 45 vs B 40, A higher.
3. Mar: A 55 vs B 60, B higher.
4. Apr: A 50 vs B 45, A higher.
5. May: A 60 vs B 55, A higher.
6. Jun: A 70 vs B 65, A higher.
7. Count of months where A beats B = 4 (2, 4, 5, 6).
**Fast method (30 seconds):** Run a finger down the two columns and tick months where A is greater; 4 ticks.
**Check:** verified by script.
**Explain simply:**
- Outsell means strictly greater sales in that month.
- Winning more months need not mean a higher total (here A wins 4 months and the total gap is only 5).
**Likely follow-ups:** 1) *How many months did B outsell A?* 2 (Jan and Mar). 2) *Largest monthly gap?* January, 10.
**Common mistakes / traps:** Reading the total instead of monthly counts; counting a month with a tie as a win (there is no tie here).

### Q49 ⭐⭐ 🟢 What is Operations' share of total 2025 headcount (to 2 decimals)?
Headcount by department (employees):

| Department | 2024 | 2025 |
|---|---|---|
| HR | 40 | 50 |
| Finance | 60 | 66 |
| Sales | 120 | 150 |
| IT | 80 | 104 |
| Operations | 100 | 94 |

**Asked at:** commonly asked (no company-specific report found); share-of-total and table-lookup items are core to every DI set per prep sites (unverified).
**What the interviewer is checking:** Whether you add the right column (2025, not 2024) for the total, then divide the part by that total.
**Say this in the interview:** "Share means part divided by total. 2025 total is 464 and Operations is 94, so 94/464 is 20.26%."
**Answer:** **20.26%**
**Step-by-step working:**
1. Use only the 2025 column: HR 50, Finance 66, Sales 150, IT 104, Operations 94.
2. Total 2025 headcount = 50 + 66 + 150 + 104 + 94 = 464.
3. Operations share = 94 / 464 x 100 = 20.2586...%.
4. Rounded to 2 decimals: 20.26%.
**Fast method (30 seconds):** Estimate 94/464 as about 100/500 = 20%; the exact value is a little above that because 94/464 is slightly more than 1/5 (464/5 = 92.8 < 94).
**Check:** 20.26% of 464 = 94.0 (verified by script).
**Explain simply:**
- Share (or contribution) = part / total x 100.
- The total must be the total of the same year; mixing 2024 and 2025 columns is the usual slip.
- Mini-example: 50 HR out of 464 is 50/464 = 10.78%.
**Likely follow-ups:** What was Operations' share in 2024? Total 2024 = 400, so 100/400 = 25%. It fell from 25% to 20.26%, a drop of 4.74 percentage points.
**Common mistakes / traps:** Dividing by the 2024 total (400) to get 23.5%, or reporting 20.25% by truncating instead of rounding (the next digit is 8, so round up to 20.26).

### Q50 ⭐⭐ 🟢 What is the ratio of qualified candidates in Test A to those in Test D?
Online test results:

| Test | Appeared | Qualified % |
|---|---|---|
| A | 400 | 40% |
| B | 500 | 30% |
| C | 600 | 35% |
| D | 250 | 48% |

**Asked at:** commonly asked (no company-specific report found); ratio-from-percent items are a standard table question per prep sites (unverified).
**What the interviewer is checking:** Whether you convert percentages into actual head counts before forming a ratio.
**Say this in the interview:** "Qualified = appeared x percent. Test A is 160 and Test D is 120, so the ratio is 160:120 = 4:3."
**Answer:** **4:3**
**Step-by-step working:**
1. Test A qualified = 40% of 400 = 160.
2. Test D qualified = 48% of 250 = 120.
3. Ratio = 160 : 120.
4. Divide both by 40: 4 : 3.
**Fast method (30 seconds):** Compute each count mentally: 40% of 400 is 4 x 40 = 160; 48% of 250 is 250 x 0.48 = 120 (half of 250 is 125, minus 2% of 250 = 5).
**Check:** 160/120 = 1.333 = 4/3 (verified by script).
**Explain simply:**
- A ratio compares two quantities of the same kind, so use counts, not the raw percentages (40:48 = 5:6 would be wrong).
- Simplest form means dividing both sides by their highest common factor (here 40).
**Likely follow-ups:** Ratio of qualified in Test B to Test C? B = 150, C = 210, ratio 5:7.
**Common mistakes / traps:** Comparing 40% with 48% directly. The two tests have different numbers of candidates (400 and 250), so percentages alone cannot give the ratio.

### Q51 ⭐⭐ 🟢 How many percent more Tech employees does Company B have than Company A?
Two pie charts of department-wise employees. Company A has 8,000 employees and Company B has 12,000.

| Department | Company A % | Company B % |
|---|---|---|
| Sales | 30 | 25 |
| Tech | 40 | 30 |
| Operations | 20 | 35 |
| Admin | 10 | 10 |

**Asked at:** commonly asked (no company-specific report found); two-pie comparison is a 2-star DI pattern per prep sites (unverified).
**What the interviewer is checking:** Whether you convert each pie to actual numbers first, then use the correct base (Company A) for the percent difference.
**Say this in the interview:** "Tech in A is 40% of 8,000 = 3,200; in B it is 30% of 12,000 = 3,600. B has 400 more, and 400 over 3,200 is 12.5% more."
**Answer:** **12.5% more**
**Step-by-step working:**
1. Company A Tech = 40% of 8,000 = 3,200.
2. Company B Tech = 30% of 12,000 = 3,600.
3. Difference = 3,600 - 3,200 = 400.
4. 'B has how many percent more than A' means A is the base: 400 / 3,200 x 100 = 12.5%.
**Fast method (30 seconds):** 3,600/3,200 = 9/8 = 1.125, so B is 12.5% above A (1/8 = 12.5%).
**Check:** 3,200 x 1.125 = 3,600 (verified by script).
**Explain simply:**
- 'X is how much more than Y' always uses Y (the thing you compare against) as the base.
- A bigger percentage slice (40% vs 30%) does not mean a bigger head count, because the company totals differ.
- Mini-example: 50 vs 40, 50 is 10/40 = 25% more than 40.
**Likely follow-ups:** By what percent are Company A's Tech employees fewer than B's? 400/3,600 = 11.11% (base changes to B).
**Common mistakes / traps:** Using 30 vs 40 (percent slices) and saying B is 25% less, or dividing by 3,600 and getting 11.11%.

### Q52 ⭐⭐ 🟢 What percentage of applicants eventually joined, and what percentage of offers were accepted?
Hiring funnel for one drive:

| Stage | Candidates |
|---|---|
| Applied | 2000 |
| Screened in | 800 |
| Interviewed | 300 |
| Offered | 90 |
| Joined | 72 |

**Asked at:** commonly asked (no company-specific report found); hiring-funnel conversion questions appear in HR-flavoured DI sets per prep sites (unverified).
**What the interviewer is checking:** Whether you pick the right denominator for each conversion rate.
**Say this in the interview:** "Joined over applied is 72/2000 = 3.6%. Offer acceptance is joined over offered: 72/90 = 80%."
**Answer:** **3.6% of applicants joined; 80% of offers were accepted**
**Step-by-step working:**
1. Joined = 72, Applied = 2,000: 72 / 2,000 x 100 = 3.6%.
2. Offers accepted means those who joined out of those offered: 72 / 90 x 100 = 80%.
**Fast method (30 seconds):** 72/90 simplifies to 4/5 = 80%. 72/2000: 72/20 = 3.6 per 100.
**Check:** 80% of 90 = 72 and 3.6% of 2,000 = 72 (verified by script).
**Explain simply:**
- A funnel (a chart whose stages narrow, like applied then screened then hired) shows drop-off at each step.
- Each conversion rate uses the previous relevant stage as its base, not always the first stage.
- Overall conversion (3.6%) is the product of the step rates: 40% x 37.5% x 30% x 80% = 3.6%.
**Likely follow-ups:** What percentage of interviewed candidates received offers? 90/300 = 30%.
**Common mistakes / traps:** Dividing joined by screened-in (72/800 = 9%) or by interviewed, instead of the two bases the question asks for.

### Q53 ⭐⭐ 🟢 What percentage of the screened-in candidates were interviewed, and what percentage of applicants was rejected at screening?
Hiring funnel for one drive:

| Stage | Candidates |
|---|---|
| Applied | 2000 |
| Screened in | 800 |
| Interviewed | 300 |
| Offered | 90 |
| Joined | 72 |

**Asked at:** commonly asked (no company-specific report found); funnel items are a 2-star DI pattern per prep sites (unverified).
**What the interviewer is checking:** Whether you use the correct base for each percentage and convert 'rejected' into a count.
**Say this in the interview:** "Interviewed over screened-in is 300/800 = 37.5%. Rejected at screening is 2000 - 800 = 1200, which is 60% of applicants."
**Answer:** **37.5% of screened-in candidates were interviewed; 60% of applicants were rejected at screening**
**Step-by-step working:**
1. Interviewed / Screened in = 300 / 800 x 100 = 37.5%.
2. Rejected at screening = 2,000 - 800 = 1,200 candidates.
3. Rejected share of applicants = 1,200 / 2,000 x 100 = 60%.
4. Cross-check: screened-in share is 800/2,000 = 40%, and 40% + 60% = 100%.
**Fast method (30 seconds):** 300/800 = 3/8 = 0.375; 1,200/2,000 = 6/10 = 60%.
**Check:** 37.5% + 62.5% = 100% for the first part, and 40% + 60% = 100% for the second (verified by script).
**Explain simply:**
- Rejected = the ones who did not pass, so subtract from the base (2,000), then divide by the same base.
- Complement rule: share kept + share rejected = 100%.
**Likely follow-ups:** What percentage of applicants were interviewed? 300/2,000 = 15%.
**Common mistakes / traps:** Taking 800 as the base for the second part (giving 150%, which is impossible, a clue that the base is wrong).

### Q54 ⭐⭐ 🟢 What is the average attrition across the four quarters?
Quarterly attrition rate (%):

| Quarter | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Attrition % | 12 | 15 | 10 | 14 |

**Asked at:** commonly asked (no company-specific report found); simple average of a row of values, a 3-star-level basic in prep material (unverified).
**What the interviewer is checking:** Whether you can take a simple average of rates when the four quarters are equal in weight.
**Say this in the interview:** "Add the four rates, 12 + 15 + 10 + 14 = 51, and divide by 4: 12.75%."
**Answer:** **12.75%**
**Step-by-step working:**
1. Add: 12 + 15 = 27; 27 + 10 = 37; 37 + 14 = 51.
2. Divide by 4 quarters: 51 / 4 = 12.75.
**Fast method (30 seconds):** Pick 12 as a guess; deviations are 0, +3, -2, +2 which sum to +3; 3/4 = 0.75 added to 12 gives 12.75.
**Check:** 12.75 x 4 = 51 (verified by script).
**Explain simply:**
- Average = sum of values / number of values.
- A plain average of quarterly rates is only exact when headcount is about the same each quarter; otherwise use a weighted average (weights = headcount).
- Percent sign stays: the answer is an attrition rate, not a count.
**Likely follow-ups:** If Q2 were 11 instead of 15, new average? (12 + 11 + 10 + 14)/4 = 11.75%.
**Common mistakes / traps:** Averaging only two quarters, or writing 51% (the sum) instead of dividing by 4.

### Q55 ⭐⭐ 🟢 What are the percentage of females and the male to female ratio in the 3-5 years band?
Employees by experience band and gender:

| Band | Male | Female |
|---|---|---|
| 0-2 yrs | 120 | 80 |
| 3-5 yrs | 90 | 70 |
| 5+ yrs | 40 | 10 |

**Asked at:** commonly asked (no company-specific report found); gender and band split tables are common HR-flavoured DI items (unverified).
**What the interviewer is checking:** Whether you read the right row, and tell a percentage (part of total) from a ratio (part to part).
**Say this in the interview:** "In 3-5 years there are 90 males and 70 females, 160 in all. Females are 70/160 = 43.75%. Male to female is 90:70 = 9:7."
**Answer:** **Females = 43.75%; male : female = 9:7**
**Step-by-step working:**
1. Read only the 3-5 yrs row: Male 90, Female 70.
2. Band total = 90 + 70 = 160.
3. Female percentage = 70 / 160 x 100 = 43.75%.
4. Ratio male : female = 90 : 70; divide by 10 to get 9 : 7.
**Fast method (30 seconds):** 70/160 = 7/16 = 0.4375 (one sixteenth is 6.25%, so 7 sixteenths is 43.75%).
**Check:** 43.75% of 160 = 70 and 9/7 = 90/70 (verified by script).
**Explain simply:**
- Percentage compares a part with the whole; ratio compares one part with another part.
- Ratio is written in simplest whole numbers: divide both by their common factor.
**Likely follow-ups:** What is the male percentage in the 5+ yrs band? 40/50 = 80%.
**Common mistakes / traps:** Writing the ratio as 90:160 (male to total) or giving 56.25% males when females were asked.

### Q56 ⭐⭐ 🟢 If a company's 2020 sales index is 100, the 2021 index is 110 and the 2022 index is 121, and 2020 sales were Rs 50 crore, what were 2022 sales, and what was the percent change from 2021 to 2022?
**Asked at:** commonly asked (no company-specific report found); index-number questions are a 2-star DI topic per prep sites (unverified).
**What the interviewer is checking:** Whether you understand an index (a base year set to 100) and can convert it to rupees.
**Say this in the interview:** "An index of 121 means 121% of the base year, so 2022 sales are 1.21 x 50 = Rs 60.5 crore. From 110 to 121 is 11/110 = 10%."
**Answer:** **2022 sales = Rs 60.5 crore; percent change 2021 to 2022 = 10%**
**Step-by-step working:**
1. The base year 2020 has index 100 and sales Rs 50 crore, so 1 index point = Rs 0.5 crore.
2. 2022 sales = 121 x 0.5 = Rs 60.5 crore. (2021 sales = 110 x 0.5 = Rs 55 crore.)
3. Percent change 2021 to 2022 = (121 - 110) / 110 x 100 = 10%.
4. Cross-check with rupees: (60.5 - 55) / 55 = 10%.
**Fast method (30 seconds):** Index 121 over base 100 means multiply by 1.21: 50 x 1.21 = 60.5. Two years of 10% growth give 1.1 x 1.1 = 1.21.
**Check:** 55 x 1.10 = 60.5 (verified by script).
**Explain simply:**
- An index number rebases a series so the starting year equals 100; every other value reads as a percent of that year.
- Percent change between two later years uses the earlier year's index as base (110), not 100.
- The total two-year rise is 21%, but each year's rise is 10%.
**Likely follow-ups:** What is the percent change from 2020 to 2022? (121 - 100)/100 = 21%.
**Common mistakes / traps:** Dividing 11 by 100 (index points over the base year) and getting 11% instead of 10%.

### Q57 ⭐⭐ 🟡 What is the overall percentage of females across all bands, and which band has the highest female share?
Employees by experience band and gender:

| Band | Male | Female |
|---|---|---|
| 0-2 yrs | 120 | 80 |
| 3-5 yrs | 90 | 70 |
| 5+ yrs | 40 | 10 |

**Asked at:** commonly asked (no company-specific report found); shares by category within a table are core DI per prep sites (unverified).
**What the interviewer is checking:** Whether you compute each band's own share and compare, and sum correctly for the overall share.
**Say this in the interview:** "Females total 80 + 70 + 10 = 160 of 410 employees, which is 39.02%. By band the female shares are 40%, 43.75% and 20%, so 3-5 years is highest."
**Answer:** **Overall female share = 39.02%; the 3-5 yrs band has the highest female share (43.75%)**
**Step-by-step working:**
1. Total males = 120 + 90 + 40 = 250; total females = 80 + 70 + 10 = 160; all employees = 410.
2. Overall female % = 160 / 410 x 100 = 39.02%.
3. 0-2 yrs: 80 / 200 = 40%.
4. 3-5 yrs: 70 / 160 = 43.75%.
5. 5+ yrs: 10 / 50 = 20%.
6. Highest is 43.75%, the 3-5 yrs band.
**Fast method (30 seconds):** Do not pick the band with the most females (0-2 yrs has 80); compare shares. Rough check: 160/410 is just under 40%.
**Check:** Band shares weighted by band size (200, 160, 50) give 160/410 again (verified by script).
**Explain simply:**
- A share is always 'part of its own group', so each band is judged against its own total.
- The overall share is a weighted average of the band shares, not the simple average of 40, 43.75 and 20 (which would be 34.58%).
**Likely follow-ups:** Which band has the highest number of females? 0-2 yrs (80).
**Common mistakes / traps:** Choosing 0-2 yrs because it has the most females (80), which confuses a count with a share.

### Q58 ⭐⭐ 🟡 Which region has the highest revenue per rep, and how much is it?
Regional revenue and sales reps:

| Region | Revenue (Rs lakh) | Reps |
|---|---|---|
| North | 840 | 12 |
| South | 600 | 10 |
| East | 450 | 9 |
| West | 936 | 13 |

**Asked at:** commonly asked (no company-specific report found); per-unit ratio questions (revenue per rep) are a 2-star DI pattern per prep sites (unverified).
**What the interviewer is checking:** Whether you divide revenue by headcount for every region instead of just spotting the largest revenue.
**Say this in the interview:** "Revenue per rep is revenue divided by reps: North 70, South 60, East 50, West 72. West is highest at Rs 72 lakh."
**Answer:** **West, Rs 72 lakh per rep**
**Step-by-step working:**
1. North: 840 / 12 = 70.
2. South: 600 / 10 = 60.
3. East: 450 / 9 = 50.
4. West: 936 / 13 = 72.
5. Highest is West at Rs 72 lakh per rep.
**Fast method (30 seconds):** West's 936/13: 13 x 72 = 936 (13 x 70 = 910, plus 13 x 2 = 26). The three others divide cleanly by inspection.
**Check:** 72 x 13 = 936, 70 x 12 = 840 (verified by script).
**Explain simply:**
- Revenue per rep measures productivity (output per person), which allows fair comparison between regions of different size.
- Largest total revenue (West 936) happens to coincide here, but that is not guaranteed.
**Likely follow-ups:** Which region has the lowest revenue per rep? East at Rs 50 lakh.
**Common mistakes / traps:** Choosing the region with the biggest total revenue without dividing; in other data sets the answer would differ.

### Q59 ⭐⭐ 🟡 What is the combined revenue per rep across all regions (to 2 decimals)?
Regional revenue and sales reps:

| Region | Revenue (Rs lakh) | Reps |
|---|---|---|
| North | 840 | 12 |
| South | 600 | 10 |
| East | 450 | 9 |
| West | 936 | 13 |

**Asked at:** commonly asked (no company-specific report found); weighted-average vs simple-average trap is a standard DI item per prep sites (unverified).
**What the interviewer is checking:** Whether you divide total revenue by total reps instead of averaging the four per-rep figures.
**Say this in the interview:** "Combined revenue per rep is total revenue over total reps: 2,826 / 44 = 64.23 lakh."
**Answer:** **Rs 64.23 lakh per rep (to 2 decimals)**
**Step-by-step working:**
1. Total revenue = 840 + 600 + 450 + 936 = 2,826 lakh.
2. Total reps = 12 + 10 + 9 + 13 = 44.
3. Combined revenue per rep = 2,826 / 44 = 64.2272...
4. Rounded to 2 decimals: 64.23.
**Fast method (30 seconds):** Estimate 2,826/44: 44 x 64 = 2,816, remainder 10, so about 64.2.
**Check:** 44 x 64.2273 = 2,826 (verified by script).
**Explain simply:**
- The combined figure is a weighted average of the regional figures, with reps as weights.
- The simple average of 70, 60, 50 and 72 is 63.00, which is wrong because regions have different numbers of reps (regions with more reps count for more).
**Likely follow-ups:** If the East region is dropped, what is the new figure? (2,826 - 450)/(44 - 9) = 2,376/35 = 67.89.
**Common mistakes / traps:** Giving 63 (the plain average of the four per-rep figures).

### Q60 ⭐⭐ 🟡 What is the overall attrition rate across grades, and how many employees left?
Headcount and attrition by grade:

| Grade | Headcount | Attrition % |
|---|---|---|
| L1 | 600 | 15% |
| L2 | 300 | 10% |
| L3 | 100 | 5% |

**Asked at:** commonly asked (no company-specific report found); weighted attrition across grades is a 2-star DI pattern per prep sites (unverified).
**What the interviewer is checking:** Whether you convert each grade's percentage to a headcount before adding, instead of averaging the percentages.
**Say this in the interview:** "Leavers: 15% of 600 = 90, 10% of 300 = 30, 5% of 100 = 5, so 125 of 1,000, a 12.5% overall rate."
**Answer:** **12.5% overall attrition; 125 employees left**
**Step-by-step working:**
1. L1 leavers = 15% of 600 = 90.
2. L2 leavers = 10% of 300 = 30.
3. L3 leavers = 5% of 100 = 5.
4. Total leavers = 90 + 30 + 5 = 125.
5. Total headcount = 600 + 300 + 100 = 1,000.
6. Overall rate = 125 / 1,000 x 100 = 12.5%.
**Fast method (30 seconds):** Because the total is 1,000, the overall rate is simply leavers/10: 125/10 = 12.5%.
**Check:** Weighted: 0.6 x 15 + 0.3 x 10 + 0.1 x 5 = 9 + 3 + 0.5 = 12.5 (verified by script).
**Explain simply:**
- Attrition rate = leavers / headcount x 100.
- Overall rate is a weighted average of grade rates, with headcount as weights.
- The plain average of 15, 10 and 5 is 10%, which ignores that most people are in L1.
**Likely follow-ups:** What if L3 had 300 employees and L1 400? Leavers = 60 + 30 + 15 = 105, rate = 105/1,000 = 10.5%.
**Common mistakes / traps:** Answering 10% (simple average), which is the option placed to catch you.

### Q61 ⭐⭐ 🟡 What is the constant yearly growth rate of Product P, and what would 2026 sales be at the same rate?
Sales of Product P (Rs lakh):

| Year | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Sales | 40 | 60 | 90 | 135 |

**Asked at:** commonly asked (no company-specific report found); constant growth rate and projection are line-graph tasks per prep sites (unverified).
**What the interviewer is checking:** Whether you check that the growth is the same each year, then project forward correctly.
**Say this in the interview:** "Each year divided by the one before is 1.5 (60/40, 90/60, 135/90), so growth is 50% a year. 2026 is 135 x 1.5 = Rs 202.5 lakh."
**Answer:** **50% per year; 2026 sales = Rs 202.5 lakh**
**Step-by-step working:**
1. 2023 vs 2022: 60 / 40 = 1.5, growth 50%.
2. 2024 vs 2023: 90 / 60 = 1.5, growth 50%.
3. 2025 vs 2024: 135 / 90 = 1.5, growth 50%. All equal, so the rate is a constant 50%.
4. 2026 = 135 x 1.5 = 202.5 lakh.
**Fast method (30 seconds):** Constant growth of 50% means multiplying by 3/2 each year; 135 x 3/2 = 202.5. The yearly rupee increase is not constant (20, 30, 45), which tells you it is compound growth, not straight-line.
**Check:** 40 x 1.5 x 1.5 x 1.5 x 1.5 = 202.5 (verified by script).
**Explain simply:**
- Compound growth multiplies by the same factor every year (here 1.5), so rupee gains get bigger each year.
- Straight-line (linear) growth would add the same rupees each year, which is not the case here.
**Likely follow-ups:** What would 2027 be? 202.5 x 1.5 = 303.75 lakh.
**Common mistakes / traps:** Adding the average increase (31.67 per year) to get about 166.7 for 2026, which ignores compounding.

### Q62 ⭐⭐ 🟡 How many times are Product P's 2025 sales as compared with 2022 (as a decimal)?
Sales of Product P (Rs lakh):

| Year | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Sales | 40 | 60 | 90 | 135 |

**Asked at:** commonly asked (no company-specific report found); growth-multiple questions are core line-graph items per prep sites (unverified).
**What the interviewer is checking:** Whether you read 'times' as a ratio (2025 over 2022) rather than a percentage or a difference.
**Say this in the interview:** "2025 divided by 2022 is 135/40 = 3.375 times."
**Answer:** **3.375 times**
**Step-by-step working:**
1. 2025 sales = 135 and 2022 sales = 40.
2. Multiple = 135 / 40.
3. 135 / 40 = 3.375.
**Fast method (30 seconds):** Equals 1.5 x 1.5 x 1.5 = 3.375, because growth was 1.5x in each of three years.
**Check:** 40 x 3.375 = 135 (verified by script).
**Explain simply:**
- 'How many times' is a plain ratio of later to earlier value.
- As a percent change, 3.375 times means a rise of 237.5% (a rise of 2.375 times the original), not 337.5%.
- Mini-example: 20 to 70 is 3.5 times, a 250% rise.
**Likely follow-ups:** What is the percent increase from 2022 to 2025? (135 - 40)/40 = 237.5%.
**Common mistakes / traps:** Reporting 237.5 as 'times', or 337.5% as the increase.

### Q63 ⭐⭐ 🟡 Pie sectors are P = 25%, Q = 2x%, R = x% and S = 15%. Find x and the central angle of Q.
**Asked at:** commonly asked (no company-specific report found); a missing-value pie problem, 2-star per prep sites (unverified).
**What the interviewer is checking:** Whether you know sectors of a pie add to 100% and can set up a one-variable equation.
**Say this in the interview:** "All sectors sum to 100%: 25 + 2x + x + 15 = 100, so 3x = 60 and x = 20. Q is 40%, which is 40 x 3.6 = 144 degrees."
**Answer:** **x = 20; central angle of Q = 144 degrees**
**Step-by-step working:**
1. Sum of sectors = 100%: 25 + 2x + x + 15 = 100.
2. Combine: 40 + 3x = 100, so 3x = 60 and x = 20.
3. Q = 2x = 40%, R = 20%.
4. Angle = percentage x 3.6 (because 360 / 100 = 3.6): 40 x 3.6 = 144 degrees.
**Fast method (30 seconds):** Quick angle: 40% of 360 = 0.4 x 360 = 144.
**Check:** 25 + 40 + 20 + 15 = 100 and the angles 90 + 144 + 72 + 54 = 360 (verified by script).
**Explain simply:**
- A full circle is 360 degrees and also 100%, so 1% = 3.6 degrees.
- Check that all your sectors add to 100 before trusting x.
**Likely follow-ups:** If P = 20%, Q = 3x%, R = x%, S = 20%, find x. 40 + 4x = 100 so x = 15.
**Common mistakes / traps:** Treating 2x as 2% or forgetting to include P and S in the sum.

### Q64 ⭐⭐ 🟡 How many candidates were selected in total, and what share of all hires came from referrals?
Pie chart of 4,000 candidates by source: Referral 30%, Portal 40%, Campus 20%, Agency 10%. Selection rate by source:

| Source | Referral | Portal | Campus | Agency |
|---|---|---|---|---|
| Selected % | 20% | 5% | 15% | 10% |

**Asked at:** commonly asked (no company-specific report found); pie plus table mix, 2-star DI per prep sites (unverified).
**What the interviewer is checking:** Whether you turn the pie percentages into candidate counts, apply each selection rate, then total.
**Say this in the interview:** "Candidates: Referral 1,200, Portal 1,600, Campus 800, Agency 400. Selected: 240, 80, 120, 40 = 480. Referrals are 240 of 480, which is 50%."
**Answer:** **480 candidates selected; referrals are 50% of all hires**
**Step-by-step working:**
1. Referral candidates = 30% of 4,000 = 1,200; Portal = 40% = 1,600; Campus = 20% = 800; Agency = 10% = 400.
2. Selected: Referral 20% of 1,200 = 240; Portal 5% of 1,600 = 80; Campus 15% of 800 = 120; Agency 10% of 400 = 40.
3. Total selected = 240 + 80 + 120 + 40 = 480.
4. Referral share of hires = 240 / 480 x 100 = 50%.
**Fast method (30 seconds):** Work in a table: candidates times rate for each source, then add. Referrals supply only 30% of candidates but half of the hires because their selection rate (20%) is the highest.
**Check:** 50% of 480 = 240 and the four counts add to 480 (verified by script).
**Explain simply:**
- Two layers of percentages: first a share of candidates (pie), then a selection rate inside each source (table). Multiply them.
- Share of hires is not the same as share of candidates (30%).
**Likely follow-ups:** Which source has the lowest share of hires? Agency: 40/480 = 8.33%.
**Common mistakes / traps:** Answering 30% for the referral share (that is its share of candidates, not of hires), or averaging 20, 5, 15, 10.

### Q65 ⭐⭐ 🟡 What is the overall selection percentage across all sources?
Pie chart of 4,000 candidates by source: Referral 30%, Portal 40%, Campus 20%, Agency 10%. Selection rate by source:

| Source | Referral | Portal | Campus | Agency |
|---|---|---|---|---|
| Selected % | 20% | 5% | 15% | 10% |

**Asked at:** commonly asked (no company-specific report found); weighted overall rate, 2-star DI per prep sites (unverified).
**What the interviewer is checking:** Whether you weight each source's rate by its number of candidates instead of taking a plain average.
**Say this in the interview:** "480 selected out of 4,000 candidates is 12%. A plain average of the four rates (12.5%) would be wrong."
**Answer:** **12%**
**Step-by-step working:**
1. Selected per source (from the same pie and table): 240, 80, 120, 40, total 480.
2. Total candidates = 4,000.
3. Overall selection % = 480 / 4,000 x 100 = 12%.
4. Weighted form: 0.30 x 20 + 0.40 x 5 + 0.20 x 15 + 0.10 x 10 = 6 + 2 + 3 + 1 = 12.
**Fast method (30 seconds):** 480/4,000 = 12/100. The weighted form confirms it without needing counts: 6 + 2 + 3 + 1 = 12.
**Check:** Both routes give 12 (verified by script).
**Explain simply:**
- Overall rate = total selected / total candidates.
- A simple average of rates (20 + 5 + 15 + 10)/4 = 12.5% is close here but wrong in principle, since Portal has four times the candidates of Agency.
- The weights are the pie shares (30%, 40%, 20%, 10%).
**Likely follow-ups:** If Portal were 10% and Referral 60% of candidates, the new overall rate? 0.6 x 20 + 0.1 x 5 + 0.2 x 15 + 0.1 x 10 = 12 + 0.5 + 3 + 1 = 16.5%.
**Common mistakes / traps:** Giving 12.5% (the plain average); it is the tempting near-miss option.

### Q66 ⭐⭐ 🟡 What was the percentage change in Product P's sales from 2024 to 2025, in rupees (not share)?
Product sales shares (pie charts):

| Product | 2024 (total Rs 400 lakh) | 2025 (total Rs 500 lakh) |
|---|---|---|
| P | 40% | 30% |
| Q | 35% | 40% |
| R | 25% | 30% |

**Asked at:** commonly asked (no company-specific report found); shares-versus-rupees trap, 2-star DI per prep sites (unverified).
**What the interviewer is checking:** Whether you convert each year's share to rupees before comparing, because the totals differ between years.
**Say this in the interview:** "P was 40% of 400 = 160 lakh in 2024 and 30% of 500 = 150 lakh in 2025. Change is -10/160 = -6.25%, a fall."
**Answer:** **Decrease of 6.25%**
**Step-by-step working:**
1. 2024 P sales = 40% of 400 = 160 lakh.
2. 2025 P sales = 30% of 500 = 150 lakh.
3. Change = 150 - 160 = -10 lakh.
4. Percent change = -10 / 160 x 100 = -6.25%, so a 6.25% decrease.
**Fast method (30 seconds):** 10/160 = 1/16 = 6.25%. Remember 1/16 = 6.25%.
**Check:** 160 x 0.9375 = 150 (verified by script).
**Explain simply:**
- A falling share does not always mean falling sales; it falls in rupees only if the total grows by less than the share shrinks.
- Here the total grew 25% (400 to 500) but P's share shrank by one quarter (40 to 30), a net small fall.
- Percent change base is always the earlier value (160).
**Likely follow-ups:** What would P's 2025 share need to be for no rupee change? 160/500 = 32%.
**Common mistakes / traps:** Saying P fell by 10% (the percentage-point drop in share) or by 25% (30 vs 40 as a ratio).

### Q67 ⭐⭐ 🟡 By what percentage did Product R's sales grow from 2024 to 2025?
Product sales shares (pie charts):

| Product | 2024 (total Rs 400 lakh) | 2025 (total Rs 500 lakh) |
|---|---|---|
| P | 40% | 30% |
| Q | 35% | 40% |
| R | 25% | 30% |

**Asked at:** commonly asked (no company-specific report found); percent change from pie shares, 2-star DI per prep sites (unverified).
**What the interviewer is checking:** Whether you compute rupee values from each pie before finding the percent change.
**Say this in the interview:** "R was 25% of 400 = 100 lakh and 30% of 500 = 150 lakh, so growth is 50/100 = 50%."
**Answer:** **50%**
**Step-by-step working:**
1. 2024 R sales = 25% of 400 = 100 lakh.
2. 2025 R sales = 30% of 500 = 150 lakh.
3. Increase = 50 lakh.
4. Growth % = 50 / 100 x 100 = 50%.
**Fast method (30 seconds):** Shortcut: share ratio times total ratio: (30/25) x (500/400) = 1.2 x 1.25 = 1.5, so +50%.
**Check:** 100 x 1.5 = 150 (verified by script).
**Explain simply:**
- Value = share x total; the growth factor is the product of the share factor and the total factor.
- The share alone rose from 25% to 30% (a 20% rise, or 5 percentage points), but sales rose by more because the total also grew.
**Likely follow-ups:** Share-times-total shortcut for P: (30/40) x (500/400) = 0.75 x 1.25 = 0.9375, so -6.25%.
**Common mistakes / traps:** Answering 20% (growth of the share) or 5% (percentage points).

### Q68 ⭐⭐ 🟡 By what percentage did Product Q's sales grow from 2024 to 2025 (to 2 decimals)?
Product sales shares (pie charts):

| Product | 2024 (total Rs 400 lakh) | 2025 (total Rs 500 lakh) |
|---|---|---|
| P | 40% | 30% |
| Q | 35% | 40% |
| R | 25% | 30% |

**Asked at:** commonly asked (no company-specific report found); percent change from pie shares, 2-star DI per prep sites (unverified).
**What the interviewer is checking:** Whether you compute rupee values first and round only at the end.
**Say this in the interview:** "Q was 35% of 400 = 140 lakh and 40% of 500 = 200 lakh. Growth is 60/140 = 42.86%."
**Answer:** **42.86% (to 2 decimals)**
**Step-by-step working:**
1. 2024 Q sales = 35% of 400 = 140 lakh.
2. 2025 Q sales = 40% of 500 = 200 lakh.
3. Increase = 200 - 140 = 60 lakh.
4. Growth % = 60 / 140 x 100 = 42.857...%, which rounds to 42.86%.
**Fast method (30 seconds):** 60/140 = 3/7 = 0.42857. Remember 1/7 = 14.29%, so 3/7 = 42.86%. Shares route: (40/35) x (500/400) = 8/7 x 5/4 = 10/7 = 1.4286.
**Check:** 140 x 1.428571 = 200 (verified by script).
**Explain simply:**
- Percent change = (new - old) / old x 100, with old as the base.
- Round only at the last step; the 42.857 rounds up because the next digit is 7.
**Likely follow-ups:** Which product grew fastest in rupees, P, Q or R? R at 50%, then Q at 42.86%, and P fell 6.25%.
**Common mistakes / traps:** Dividing by 200 (the new value) and getting 30%, or using share points (40 - 35 = 5 points on 35, 14.29%).

### Q69 ⭐⭐ 🟡 A pie chart shows Tech at 40% of Company X and 30% of Company Y. Can you say Company X has more Tech employees than Company Y? Why or why not?
**Asked at:** commonly asked (no company-specific report found); a share-versus-count trap, 2-star DI per prep sites (unverified).
**What the interviewer is checking:** Whether you notice that a percentage needs the company total to become a head count.
**Say this in the interview:** "No. Forty percent of a small company can be fewer people than 30% of a big one. I would need each company's total headcount."
**Answer:** **No, it cannot be said without knowing the total number of employees in each company**
**Step-by-step working:**
1. Tech in X = 40% of total X; Tech in Y = 30% of total Y.
2. Example 1: X has 1,000 and Y has 1,000: Tech is 400 vs 300, so X has more.
3. Example 2: X has 1,000 and Y has 2,000: Tech is 400 vs 600, so Y has more.
4. Since the answer flips depending on the totals, the pie charts alone are not enough.
**Fast method (30 seconds):** X has more Tech people only if 0.40 x TotalX > 0.30 x TotalY, that is TotalX > 0.75 x TotalY.
**Check:** The two examples are verified by script (400 vs 300, 400 vs 600).
**Explain simply:**
- A pie chart shows shares within one whole, not sizes of different wholes.
- To compare across two pies you need the two totals (or a stated 'same total' in the question).
- Mini-example: 40% of 500 = 200, but 30% of 1,000 = 300.
**Likely follow-ups:** At what Y-size would X (1,000 employees) match Y's Tech count? 400 = 0.30 x Y gives Y = 1,333.
**Common mistakes / traps:** Saying 'yes, 40% is more than 30%', the trap answer built on comparing percentages across different bases.

### Q70 ⭐⭐ 🟡 A bar chart's y-axis starts at 80 instead of 0. How can this mislead, and what should you check?
**Asked at:** commonly asked (no company-specific report found); misleading-axis checks are standard in numerical-reasoning guides (unverified).
**What the interviewer is checking:** Whether you read the axis scale before judging bar heights.
**Say this in the interview:** "A truncated axis exaggerates differences, because bar length no longer matches value. I would read the actual labels and compute the real percent difference."
**Answer:** **It exaggerates differences between bars; always read the axis start, the scale and the data labels, and compute real values**
**Step-by-step working:**
1. Bars are normally read by length, which is correct only when the axis starts at 0.
2. If the axis starts at 80, a bar of 100 shows as 20 units long and a bar of 90 as 10 units long: the first looks twice as tall.
3. Real values: 100 vs 90 is only (100 - 90)/90 = 11.1% higher.
4. Check also: the unit (lakh or crore), whether the axis is broken, the scale steps, and data labels.
**Fast method (30 seconds):** Always read the axis labels before the bars, and compute the real ratio from the numbers, not the picture.
**Check:** Visual ratio (20/10 = 2.0) vs true ratio (100/90 = 1.11), verified by script.
**Explain simply:**
- Bars encode value by length, so the baseline must be zero for a fair visual comparison.
- A truncated axis is acceptable for line charts when the goal is showing change, but must be labelled.
- For exam questions the numbers, not the visual impression, give the answer.
**Likely follow-ups:** Bars of 120 and 100 on an axis starting at 80: visual 40 vs 20, 2x apart; real difference is 20%.
**Common mistakes / traps:** Estimating the answer by eye from bar heights without reading where the axis starts.

### Q71 ⭐⭐ 🟡 If B is 25% more than A, then A is what percent less than B? Check with A = 40 and B = 50.
**Asked at:** commonly asked (no company-specific report found); a 3-star-style asymmetry between 'more than' and 'less than' (unverified).
**What the interviewer is checking:** Whether you swap the base correctly when reversing a percentage comparison.
**Say this in the interview:** "If B = 1.25 A, then A = B / 1.25 = 0.8 B, so A is 20% less than B. Check with 40 and 50: 10 on 50 is 20%."
**Answer:** **20%**
**Step-by-step working:**
1. B = A x 1.25 (25% more).
2. So A = B / 1.25 = 0.8 x B.
3. A is 1 - 0.8 = 0.2, that is 20% less than B.
4. Check with numbers: A = 40, B = 50. B is 10/40 = 25% more than A. A is 10/50 = 20% less than B.
**Fast method (30 seconds):** Rule: if the rise is x/y, then the matching fall is x/(x + y). Here 25% = 1/4, so the fall is 1/(1 + 4) = 1/5 = 20%.
**Check:** 50 x 0.8 = 40 (verified by script).
**Explain simply:**
- The base changes: the 'more than' is measured on the smaller number (A) and the 'less than' on the larger number (B).
- The same gap of 10 is a bigger fraction of 40 than of 50.
- Mini-example: a 50% rise (1/2) reverses to a fall of 1/3 = 33.33%.
**Likely follow-ups:** If A is 20% less than B, how much more is B than A? B = A / 0.8 = 1.25 A, so 25% more.
**Common mistakes / traps:** Saying 25%, assuming the percentage is symmetric.

### Q72 ⭐⭐ 🟡 The 2025 revenue is Rs 150 crore. What expenditure gives a 40% profit on cost (to 2 decimals)?

Revenue and expenditure (Rs crore):

| Year | Revenue | Expenditure |
|---|---|---|
| 2021 | 80 | 64 |
| 2022 | 99 | 90 |
| 2023 | 110 | 88 |
| 2024 | 120 | 108 |
| 2025 | 150 | 120 |

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Whether you know profit % on cost uses cost as the base, and can reverse it.
**Say this in the interview:** "Profit on cost of 40% means revenue is 1.40 times expenditure, so expenditure is 150 divided by 1.4, about Rs 107.14 crore."
**Answer:** **Expenditure = Rs 107.14 crore (150 / 1.4 = 107.142857..., rounded to 2 decimals).**
**Step-by-step working:**
1. Profit % on cost = (Revenue - Expenditure) / Expenditure x 100, so cost is the base.
2. 40% profit on cost means Revenue = Expenditure x 1.40.
3. Expenditure = 150 / 1.40 = 107.142857.
4. Rounded: Rs 107.14 crore. Profit would be 150 - 107.14 = Rs 42.86 crore.
**Fast method (30 seconds):** 1.4 = 7/5, so divide by 7/5, i.e. 150 x 5 / 7 = 750 / 7 = 107.14. Divide, do not subtract 40% from 150.
**Check:** Reverse: 107.14 x 1.4 = 150.0. Verified by script.
**Explain simply:**
- Profit on cost uses the spending as 100%; profit on revenue (margin) uses the revenue as 100%.
- "40% more than cost" means multiply cost by 1.4, so going backwards you divide.
**Likely follow-ups:** 1) *What is the actual 2025 profit % on cost in the table?* Expenditure is Rs 120 crore, so (150 - 120) / 120 = 25%. 2) *What expenditure gives a 40% margin on revenue?* 60% of 150 = Rs 90 crore.
**Common mistakes / traps:** Taking 150 x 0.60 = 90 (that is margin on revenue) or 150 - 40% of 150. Another trap is using the table's 120 as the answer; the question asks for a hypothetical cost.

### Q73 ⭐⭐ 🟡 When is a stacked bar chart better than a clustered bar chart, and when is it worse?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Whether you can pick a chart for the message, not for looks.
**Say this in the interview:** "Stacked bars are best for showing the total and the parts together; clustered bars are best when you need to compare the parts with each other."
**Answer:** **Stacked is better for totals and for one bottom segment; it is worse for comparing middle segments across bars. Clustered is the opposite.**
**Step-by-step working:**
1. Take Q1 sales: Product A 30 and Product B 20 (Rs lakh). A stacked bar shows one bar of height 50, split into 30 and 20.
2. The total (50) is easy to see and compare across quarters; the bottom segment (A, starting at zero) is easy too.
3. The top segment (B) floats on top of A, so its start moves from bar to bar; comparing B across quarters by eye is hard.
4. A clustered bar puts A and B side by side from the same zero line, so every part compares fairly, but the total is not shown.
**Fast method (30 seconds):** Ask: what is the message? Total plus composition means stacked; compare parts means clustered.
**Explain simply:**
- Stacked bar: parts add to a whole, good when there are few categories (2-4).
- Clustered bar: each series has its own bar on a common baseline, good for side-by-side comparison.
- Too many segments in a stack turns into a colourful puzzle that nobody can read.
**Likely follow-ups:** 1) *Which would you use for share of headcount by department over years?* A 100% stacked bar. 2) *In a stacked bar, is the top segment easy to compare across bars?* No, because it does not start at a common baseline.
**Common mistakes / traps:** Using a stacked chart when the audience must compare the middle series, or reading the top segment's height as if it began at zero.

### Q74 ⭐⭐ 🔴 Headcount rises from 200 to 220 and average salary rises from Rs 50,000 to Rs 55,000 per month. By what percentage does total payroll rise?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Whether you know payroll is headcount times average salary, so growth rates multiply.
**Say this in the interview:** "Payroll is headcount times average salary. 1.10 times 1.10 is 1.21, so payroll rises 21%, not 20%."
**Answer:** **Total payroll rises by 21%.**
**Step-by-step working:**
1. Old payroll = 200 x 50,000 = Rs 1,00,00,000 (Rs 1 crore) per month.
2. New payroll = 220 x 55,000 = Rs 1,21,00,000 (Rs 1.21 crore) per month.
3. Rise = (1.21 - 1.00) / 1.00 x 100 = 21%.
**Fast method (30 seconds):** Headcount grew 10% (200 to 220) and salary grew 10% (50,000 to 55,000). Two successive 10% factors: 1.1 x 1.1 = 1.21. Shortcut: a% and b% combine to a + b + ab/100 = 10 + 10 + 1 = 21%.
**Check:** Verified by script: 12,100 / 10,000 = 1.21.
**Explain simply:**
- When a total is a product of two things (count x average), their percent changes multiply, not add.
- The extra 1% is the "growth on growth" term.
**Likely follow-ups:** 1) *If headcount rises 10% and average salary falls 10%?* 1.1 x 0.9 = 0.99, so payroll falls 1%. 2) *Headcount +20%, salary +5%?* 1.2 x 1.05 = 1.26, so +26%.
**Common mistakes / traps:** Answering 20% by adding the two percentages.

### Q75 ⭐⭐ 🔴 What is the overall average salary of all employees (Rs lakh per year)?

Employees by pay band:

| Band | % of employees | Average salary (Rs lakh per year) |
|---|---|---|
| Below 3L | 30% | 2.4 |
| 3L to 6L | 45% | 4.4 |
| Above 6L | 25% | 9 |

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Weighted average: weights are the shares of employees, not equal.
**Say this in the interview:** "I weight each band's average by its share of employees: 0.30 x 2.4 plus 0.45 x 4.4 plus 0.25 x 9, which gives 4.95 lakh."
**Answer:** **Overall average salary = Rs 4.95 lakh per year.**
**Step-by-step working:**
1. Below 3L: 30% x 2.4 = 0.72.
2. 3L to 6L: 45% x 4.4 = 1.98.
3. Above 6L: 25% x 9 = 2.25.
4. Add: 0.72 + 1.98 + 2.25 = 4.95.
5. The weights add to 100% (30 + 45 + 25), so no further division is needed.
**Fast method (30 seconds):** Imagine 100 employees: 30 x 2.4 = 72, 45 x 4.4 = 198, 25 x 9 = 225; total 495 lakh for 100 people = 4.95.
**Check:** The simple average of the three averages is (2.4 + 4.4 + 9) / 3 = 5.27, which is the wrong answer; ours is lower because most staff sit in the lower bands. Verified by script.
**Explain simply:**
- A weighted average gives more importance to the group that has more people.
- Percent shares can be treated as head-counts out of 100.
**Likely follow-ups:** 1) *If the Above 6L band were 35% and Below 3L only 20%?* 0.2 x 2.4 + 0.45 x 4.4 + 0.35 x 9 = 0.48 + 1.98 + 3.15 = 5.61. 2) *What is the total annual payroll for 400 employees?* 400 x 4.95 = Rs 1,980 lakh.
**Common mistakes / traps:** Picking 5.27 (the plain average of the three numbers), the expected wrong option.

### Q76 ⭐⭐ 🔴 What is Finance's share of total payroll (to 2 decimals)?

Payroll table (salary in Rs thousand per month):

| Department | Employees | Average salary | Total payroll |
|---|---|---|---|
| IT | 50 | 80 | 4000 |
| Operations | ? | 40 | 2000 |
| Finance | 25 | 70 | 1750 |

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Reading a table with a missing value and computing a share of a total.
**Say this in the interview:** "Finance payroll is 1,750 out of a total payroll of 4,000 + 2,000 + 1,750 = 7,750, so its share is 22.58%."
**Answer:** **Finance's share of total payroll = 22.58% (1,750 / 7,750 x 100).**
**Step-by-step working:**
1. The payroll column already gives each total: IT 4,000, Operations 2,000, Finance 1,750 (Rs thousand per month).
2. Total payroll = 4,000 + 2,000 + 1,750 = 7,750.
3. Share = 1,750 / 7,750 = 0.225806 = 22.58%.
4. The missing Operations headcount (2,000 / 40 = 50 employees) is not needed here; it is a distractor.
**Fast method (30 seconds):** Divide by 250: 1,750 / 250 = 7 and 7,750 / 250 = 31, so 7/31 = 22.58%.
**Check:** The three shares: IT 51.61%, Operations 25.81%, Finance 22.58%, sum 100%. Verified by script.
**Explain simply:**
- A share is part divided by the whole, times 100.
- Use the payroll column for payroll shares; use headcount for headcount shares.
**Likely follow-ups:** 1) *IT's share of payroll?* 4,000 / 7,750 = 51.61%. 2) *Finance's share of headcount?* Total heads 50 + 50 + 25 = 125, so 25 / 125 = 20%.
**Common mistakes / traps:** Using the average-salary column (70 / 190 = 36.84%), which ignores headcount.

### Q77 ⭐⭐ 🔴 A pie sector for Department A is 20% of total expense and equals Rs 2.4 crore. What is the total expense, and what amount does a 35% sector represent?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Using a known part and its percentage to find the whole.
**Say this in the interview:** "20% equals 2.4 crore, so the total is 2.4 divided by 0.2, which is 12 crore. A 35% sector is 0.35 x 12 = 4.2 crore."
**Answer:** **Total expense = Rs 12 crore; the 35% sector = Rs 4.2 crore.**
**Step-by-step working:**
1. 20% of total = 2.4 crore.
2. Total = 2.4 / 0.20 = 12 crore (or 2.4 x 5).
3. 35% of 12 = 0.35 x 12 = 4.2 crore.
4. Alternative: 1% = 2.4 / 20 = 0.12 crore, so 35% = 35 x 0.12 = 4.2.
**Fast method (30 seconds):** Find the value of 1% first (0.12), then multiply by any percent you need.
**Check:** 4.2 / 12 = 35%. Verified by script.
**Explain simply:**
- A pie chart is a whole split into percent shares that sum to 100%.
- "Unitary method": find 1%, then scale.
**Likely follow-ups:** 1) *What central angle is the 20% sector?* 0.20 x 360 = 72 degrees. 2) *What if 25% equals Rs 3 crore?* Total Rs 12 crore.
**Common mistakes / traps:** Multiplying 2.4 x 0.20 = 0.48, which treats 2.4 as the total instead of the part.

### Q78 ⭐⭐ 🔴 Product P's share fell from 40% to 30%. Did its rupee sales fall, and which product had the largest rupee increase?

Product sales shares (pie charts):

| Product | 2024 (total Rs 400 lakh) | 2025 (total Rs 500 lakh) |
|---|---|---|
| P | 40% | 30% |
| Q | 35% | 40% |
| R | 25% | 30% |

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Whether you know that a falling share does not mean falling rupees when the total changes.
**Say this in the interview:** "The total grew from 400 to 500, so I convert shares to rupees. P went from 160 to 150, a small fall. Q rose most, by 60 lakh."
**Answer:** **Yes, P's rupee sales fell, from Rs 160 lakh to Rs 150 lakh (down Rs 10 lakh, 6.25%); Q had the largest rupee increase, Rs 60 lakh (140 to 200).**
**Step-by-step working:**
1. 2024 rupees: P = 40% of 400 = 160; Q = 35% of 400 = 140; R = 25% of 400 = 100.
2. 2025 rupees: P = 30% of 500 = 150; Q = 40% of 500 = 200; R = 30% of 500 = 150.
3. Changes: P 150 - 160 = -10; Q 200 - 140 = +60; R 150 - 100 = +50.
4. Largest rupee increase: Q (+60).
**Fast method (30 seconds):** Note the P share fell 10 percentage points, yet rupees fell only 10 because the pie itself grew 25%.
**Check:** Rupee changes sum to the total change: -10 + 60 + 50 = +100 = 500 - 400. Verified by script.
**Explain simply:**
- A pie shows shares, not amounts. Always multiply by the total of that year's pie.
- Share can fall while the amount rises if the whole grows faster.
**Likely follow-ups:** 1) *Which product has the highest percent growth?* Q: 60 / 140 = 42.86%; R: 50 / 100 = 50%, so R is highest by percent. 2) *If the 2025 total were Rs 600 lakh, would P fall?* 30% x 600 = 180, no, it would rise.
**Common mistakes / traps:** Saying "P fell 10%" or that Q and R must be compared on shares only. Also confusing the largest rupee gain (Q) with the largest percent gain (R).

### Q79 ⭐ 🟢 Which chart type would you use to show share of sales by region, trend over 12 months, and comparison across 5 products?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Matching the chart to the message.
**Say this in the interview:** "Pie or stacked bar for share by region, line chart for the 12-month trend, bar chart for comparing 5 products."
**Answer:** **Share by region: pie (or 100% stacked bar); trend over 12 months: line chart; comparison across 5 products: (clustered) bar chart.**
**Step-by-step working:**
1. Share of a whole (parts add to 100%): pie chart, best with about 5 or fewer regions; otherwise a 100% stacked bar.
2. Change over time: line chart, because the slope shows rise and fall month to month.
3. Comparing separate categories: bar chart, because length from a common zero line is the easiest thing for the eye to compare. With 5 products, sort the bars by size.
**Fast method (30 seconds):** Whole = pie, time = line, categories = bar.
**Explain simply:**
- Pick the chart by the question the viewer must answer.
- Pies fail when slices are many or similar in size.
**Likely follow-ups:** 1) *Relationship between ad spend and sales?* Scatter plot. 2) *Distribution of salaries?* Histogram.
**Common mistakes / traps:** Using a line chart for unordered categories (it implies a trend) or a pie for 12 months.

### Q80 ⭐ 🟢 What is the difference between a bar chart and a histogram?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Knowing which chart suits categories versus continuous ranges.
**Say this in the interview:** "A bar chart compares separate categories with gaps between bars; a histogram shows how a continuous number is spread across ranges, with touching bars."
**Answer:** **Bar chart: categories, gaps between bars, order can change. Histogram: continuous bins, bars touch, order is fixed, and it shows a distribution.**
**Step-by-step working:**
1. Bar example: headcount by department (IT, Finance, Operations). You can reorder the bars without changing meaning.
2. Histogram example: salaries grouped into 20-30, 30-40, 40-50 and so on (Rs thousand). The bars touch because the ranges run on continuously.
3. In a histogram, the bar height shows the count in the range (with equal-width bins), and the shape shows whether salaries are bunched or skewed.
**Fast method (30 seconds):** Gaps mean categories; no gaps mean a number line.
**Explain simply:**
- Continuous data can take any value in a range (salary, age); categories are labels.
- Histogram bin widths should be equal, or the height misleads.
**Likely follow-ups:** 1) *Can you reorder histogram bars?* No. 2) *Which one shows the median band?* A histogram (via cumulative counts).
**Common mistakes / traps:** Treating a histogram as a bar chart of categories, or leaving unequal bin widths.

### Q81 ⭐ 🟢 What does a dual-axis chart show, and why can it mislead?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Whether you notice that two scales can manufacture a visual story.
**Say this in the interview:** "A dual-axis chart plots two measures with different units on left and right scales. It can mislead because the scales are chosen freely, so lines can be made to cross or move together."
**Answer:** **It shows two measures with different units on one chart (e.g. revenue in Rs lakh on the left, margin % on the right); it misleads because each axis scale is arbitrary, so the visual relationship can be manufactured.**
**Step-by-step working:**
1. Example: revenue 200, 250, 300 (Rs lakh) with margin 10%, 12%, 15%.
2. Stretch the right axis from 0-20% and the lines look steep; use 0-100% and they look flat.
3. Where the two lines cross has no real meaning, because the crossing depends only on the scale choice.
4. Read each axis separately and check where each starts.
**Fast method (30 seconds):** Always ask: what are the two axes, where do they start, and would the story hold on a single scale?
**Explain simply:**
- Dual axis lets you show two units at once, which is useful for revenue (bars) and margin (line).
- The danger is the apparent link between lines that may have no real connection.
**Likely follow-ups:** 1) *How do you reduce the risk?* Label axes clearly, start bars at zero, or use two small charts. 2) *Do crossing lines mean margin overtook revenue?* No, they are different units.
**Common mistakes / traps:** Reading line crossings as a real event, or comparing the heights of the two series directly.

### Q82 ⭐ 🟡 What percentage of employees earn less than Rs 50 thousand per month, and in which band does the median lie?

Salary bands (Rs thousand per month) and number of employees:

| Band | 20-30 | 30-40 | 40-50 | 50-60 | 60-70 |
|---|---|---|---|---|---|
| Employees | 15 | 25 | 30 | 20 | 10 |

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Reading a frequency table, cumulative counts, and locating the median band.
**Say this in the interview:** "Total is 100. Under 50 means the first three bands: 15 + 25 + 30 = 70, so 70%. The 50th and 51st person fall in 40-50, so the median is there."
**Answer:** **70% earn less than Rs 50 thousand; the median lies in the 40-50 band.**
**Step-by-step working:**
1. Total employees = 15 + 25 + 30 + 20 + 10 = 100.
2. Below 50 = bands 20-30, 30-40, 40-50 = 15 + 25 + 30 = 70 employees = 70%.
3. Cumulative counts: 15, 40, 70, 90, 100.
4. The median is at position 50 and 51 (middle of 100). Cumulative 40 is below 50 and cumulative 70 is above, so the median sits in 40-50.
5. Estimated median by interpolation: 40 + (50 - 40) / 30 x 10 = 43.33 thousand.
**Fast method (30 seconds):** With a total of 100, counts are already percents. Add running totals until you cross 50.
**Check:** Median band checked by cumulative table. Verified by script.
**Explain simply:**
- Median = middle value; cumulative frequency means running total.
- The band is exact; the number inside the band is only an estimate.
**Likely follow-ups:** 1) *What percent earns Rs 50 thousand or more?* 30%. 2) *If the 20-30 band had 35 people instead (total 120)?* Cumulative 35, 60, 90; the 60th/61st person is in 30-40.
**Common mistakes / traps:** Taking the middle band (40-50) just because it is in the middle, or using the middle of the five bands rather than the middle person.

### Q83 ⭐ 🟡 Estimate the mean salary using class mid-points (Rs thousand).

Salary bands (Rs thousand per month) and number of employees:

| Band | 20-30 | 30-40 | 40-50 | 50-60 | 60-70 |
|---|---|---|---|---|---|
| Employees | 15 | 25 | 30 | 20 | 10 |

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Mean from grouped data using class mid-points.
**Say this in the interview:** "I use each band's mid-point as the salary, multiply by the headcount, add and divide by 100. It comes to 43.5 thousand."
**Answer:** **Estimated mean = Rs 43.5 thousand per month.**
**Step-by-step working:**
1. Mid-points: 25, 35, 45, 55, 65.
2. Multiply by employees: 25 x 15 = 375; 35 x 25 = 875; 45 x 30 = 1,350; 55 x 20 = 1,100; 65 x 10 = 650.
3. Sum = 375 + 875 + 1,350 + 1,100 + 650 = 4,350.
4. Mean = 4,350 / 100 = 43.5.
**Fast method (30 seconds):** Use 45 as an assumed mean: deviations -20, -10, 0, 10, 20 times counts = -300 - 250 + 0 + 200 + 200 = -150; -150/100 = -1.5; 45 - 1.5 = 43.5.
**Check:** Verified by script.
**Explain simply:**
- When only ranges are known, we assume everyone in a band earns the mid-point; the result is an estimate.
- It is a weighted average with counts as weights.
**Likely follow-ups:** 1) *Is 43.5 exact?* No, actual salaries inside bands are unknown. 2) *Mean if the counts doubled?* Still 43.5, since the shares do not change.
**Common mistakes / traps:** Dividing by 5 (number of bands) instead of 100, or using band edges instead of mid-points.

### Q84 ⭐ 🟡 What is Product B's share of total sales over Q1 to Q3 (to 2 decimals), and what is it in Q3?

Stacked bar, product sales (Rs lakh):

| Quarter | Product A | Product B |
|---|---|---|
| Q1 | 30 | 20 |
| Q2 | 36 | 24 |
| Q3 | 40 | 40 |

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Share of a total from stacked bar data across several periods.
**Say this in the interview:** "B totals 20 + 24 + 40 = 84 and all products total 190, so 44.21%. In Q3 B is 40 of 80, which is 50%."
**Answer:** **Product B's share over Q1 to Q3 = 44.21%; in Q3 alone = 50%.**
**Step-by-step working:**
1. Product A total = 30 + 36 + 40 = 106.
2. Product B total = 20 + 24 + 40 = 84.
3. Combined = 106 + 84 = 190.
4. B's share = 84 / 190 = 0.44211 = 44.21%.
5. Q3: A 40 + B 40 = 80; B share = 40 / 80 = 50%.
**Fast method (30 seconds):** 84/190 = 42/95, a bit below 45%, since 45% of 190 = 85.5.
**Check:** A share = 106 / 190 = 55.79%; 44.21 + 55.79 = 100. Verified by script.
**Explain simply:**
- In a stacked bar the total is the sum of the segments.
- Do not average the quarterly shares; add the rupees first, then divide.
**Likely follow-ups:** 1) *Q1 share of B?* 20 / 50 = 40%. 2) *Q2 share of B?* 24 / 60 = 40%.
**Common mistakes / traps:** Averaging (40 + 40 + 50) / 3 = 43.33%, which is wrong because quarters have different totals.

### Q85 ⭐ 🟡 What was the profit in each year, and by what percentage did profit rise from 2023 to 2025?

Revenue (bar) and profit margin (line):

| Year | Revenue (Rs lakh) | Profit margin |
|---|---|---|
| 2023 | 200 | 10% |
| 2024 | 250 | 12% |
| 2025 | 300 | 15% |

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Combining a bar series with a percentage line to get profit, then percent change.
**Say this in the interview:** "Profit is revenue times margin: 20, 30 and 45 lakh. From 20 to 45 is up 125%."
**Answer:** **Profit: 2023 = Rs 20 lakh, 2024 = Rs 30 lakh, 2025 = Rs 45 lakh; profit rose 125% from 2023 to 2025.**
**Step-by-step working:**
1. 2023: 200 x 10% = 20.
2. 2024: 250 x 12% = 30.
3. 2025: 300 x 15% = 45.
4. Rise = (45 - 20) / 20 x 100 = 125%.
**Fast method (30 seconds):** Revenue rose 50% and margin rose from 10% to 15% (factor 1.5), so profit factor = 1.5 x 1.5 = 2.25, i.e. +125%.
**Check:** 45 = 2.25 x 20. Verified by script.
**Explain simply:**
- Profit = revenue x margin %. The bar gives revenue, the line gives margin.
- Margin moving from 10% to 15% is 5 percentage points, which is a 50% relative rise.
**Likely follow-ups:** 1) *Percent rise in profit 2023 to 2024?* 10 / 20 = 50%. 2) *Revenue growth 2023 to 2025?* 50%.
**Common mistakes / traps:** Answering 5 (the percentage-point rise in margin), or saying profit rose 50% because revenue did.

### Q86 ⭐ 🟡 What are the first and last 3-month moving averages for monthly sales of 20, 26, 23, 29, 32?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Moving average mechanics: window slides one step at a time.
**Say this in the interview:** "A 3-month moving average averages three consecutive months. The first is (20 + 26 + 23) / 3 = 23, the last is (23 + 29 + 32) / 3 = 28."
**Answer:** **First 3-month moving average = 23; last = 28.**
**Step-by-step working:**
1. There are 5 months, so there are 5 - 3 + 1 = 3 averages.
2. First: (20 + 26 + 23) / 3 = 69 / 3 = 23.
3. Middle: (26 + 23 + 29) / 3 = 78 / 3 = 26.
4. Last: (23 + 29 + 32) / 3 = 84 / 3 = 28.
**Fast method (30 seconds):** Slide the window: drop the oldest, add the newest, adjust by the difference / 3. From 23: drop 20, add 29: +9/3 = +3, giving 26; drop 26, add 32: +6/3 = +2, giving 28.
**Check:** Verified by script (23, 26, 28).
**Explain simply:**
- A moving average smooths short-term ups and downs to show the trend.
- Each average is placed at the end (or the middle) of its window.
**Likely follow-ups:** 1) *4-month moving average first value?* (20 + 26 + 23 + 29) / 4 = 24.5. 2) *Why does smoothing help?* It reduces random noise from month to month.
**Common mistakes / traps:** Dividing by 5 or using the wrong window, or counting only 2 averages.

### Q87 ⭐ 🟡 Complaints by category are 120, 80, 50, 30 and 20. What percentage do the top two categories contribute, and what is a Pareto chart?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Cumulative contribution and the 80/20 idea.
**Say this in the interview:** "Total complaints are 300. The top two are 120 + 80 = 200, which is 66.67%. A Pareto chart sorts causes from biggest to smallest with a cumulative line, so you can find the vital few."
**Answer:** **The top two categories contribute 66.67% of complaints. A Pareto chart is a descending bar chart of causes with a cumulative percentage line.**
**Step-by-step working:**
1. Total = 120 + 80 + 50 + 30 + 20 = 300.
2. Top two = 120 + 80 = 200.
3. Share = 200 / 300 = 66.67%.
4. Cumulative percent for the Pareto line: 40%, 66.67%, 83.33%, 93.33%, 100%.
**Fast method (30 seconds):** 200/300 = 2/3, so 66.67%.
**Check:** The five shares are 40, 26.67, 16.67, 10, 6.67 and sum to 100. Verified by script.
**Explain simply:**
- A Pareto chart is sorted from largest to smallest so the biggest causes come first.
- The Pareto principle (80/20) says a few causes produce most of the effect; here the top 3 (60% of categories) cover 83.33%.
**Likely follow-ups:** 1) *How many categories to reach at least 80%?* Three (83.33%). 2) *Why sort the bars?* So the vital few are visible immediately.
**Common mistakes / traps:** Not sorting the categories, or calculating top-two share against only the other categories rather than all complaints.

### Q88 ⭐ 🟡 A headcount waterfall starts at 500, adds 90 hires and 20 transfers in, and subtracts 60 attrition and 10 transfers out. What is the closing headcount and the net percent change?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Following a waterfall: inflows added, outflows subtracted, then percent change.
**Say this in the interview:** "500 + 90 + 20 - 60 - 10 = 540. The net change is +40 on 500, which is 8%."
**Answer:** **Closing headcount = 540; net change = +8%.**
**Step-by-step working:**
1. Start: 500.
2. Add hires: 500 + 90 = 590.
3. Add transfers in: 590 + 20 = 610.
4. Subtract attrition: 610 - 60 = 550.
5. Subtract transfers out: 550 - 10 = 540.
6. Net change = 540 - 500 = +40; 40 / 500 x 100 = 8%.
**Fast method (30 seconds):** Total inflow 110, total outflow 70, net +40.
**Check:** Verified by script.
**Explain simply:**
- A waterfall chart starts with an opening value, shows each increase or decrease as a floating bar, and ends with the closing value.
- Order does not change the closing number, only how the chart looks.
**Likely follow-ups:** 1) *Attrition rate on opening headcount?* 60/500 = 12%. 2) *Net percent change if hires were 40 instead of 90?* 490, down 2%.
**Common mistakes / traps:** Forgetting that transfers are inflows and outflows too, or dividing the net change by the closing headcount (40/540 = 7.41%).

### Q89 ⭐ 🟡 A scatter plot of training hours versus sales shows an upward trend. Can you conclude training causes higher sales?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Correlation versus causation.
**Say this in the interview:** "No. The scatter shows the two move together (correlation), but it does not prove training caused the higher sales. Other factors, such as experience, territory or motivation, could drive both."
**Answer:** **No. An upward trend shows association, not cause.**
**Step-by-step working:**
1. Example: employees who volunteer for more training hours may already be the keener, more experienced ones, who would sell more anyway (a confounder).
2. The direction could also be reverse: high performers are given more training.
3. To support cause, you need a test: randomly assign training to one group and compare against a similar group without it, or control for experience and territory.
**Fast method (30 seconds):** Correlation says "move together"; causation needs controlled comparison.
**Explain simply:**
- Correlation: two measures move together.
- Confounder: a hidden third factor that drives both.
- A scatter plot shows relationship strength and direction, nothing more.
**Likely follow-ups:** 1) *What does a tight cloud of points mean?* A strong relationship, still not cause. 2) *What would you do next as an analyst?* Run a pilot with a control group.
**Common mistakes / traps:** Saying "training increases sales" straight from the chart.

### Q90 ⭐ 🔴 Total expense is Rs 12 crore and Department A spends Rs 2.4 crore. If total expense rises 10% while A's spend stays flat, what is A's new share (to 2 decimals)?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Share changes when the denominator changes even if the numerator is flat.
**Say this in the interview:** "The new total is 12 x 1.10 = 13.2. A is still 2.4, so its share is 2.4 / 13.2 = 18.18%, down from 20%."
**Answer:** **A's new share = 18.18% (down from 20%).**
**Step-by-step working:**
1. Old share = 2.4 / 12 = 20%.
2. New total = 12 x 1.10 = 13.2 crore.
3. A is flat at 2.4 crore.
4. New share = 2.4 / 13.2 = 0.181818 = 18.18%.
**Fast method (30 seconds):** Share scales by 1/1.1: 20 / 1.1 = 18.18%.
**Check:** 18.18% x 13.2 = 2.4. Verified by script.
**Explain simply:**
- A share depends on both the part and the whole; if the whole grows and the part does not, the share falls.
- Fall = 20 - 18.18 = 1.82 percentage points (a 9.09% relative fall).
**Likely follow-ups:** 1) *If A also rose 10%?* The share stays 20%. 2) *What spend by A keeps the share at 20% of 13.2?* 2.64 crore.
**Common mistakes / traps:** Writing 20% - 10% = 10%, or adding 10% to the share instead of to the total expense.

### Q91 ⭐ 🔴 What is the CAGR from 100 to 133.1 in 3 years, and why is the simple average of annual growth rates misleading?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** CAGR (compound annual growth rate) and why growth rates are not averaged simply.
**Say this in the interview:** "CAGR is (end / start) to the power 1/years minus 1. 133.1 / 100 is 1.331, whose cube root is 1.1, so 10% a year."
**Answer:** **CAGR = 10% per year; the simple average of annual rates misleads because growth compounds on a changing base.**
**Step-by-step working:**
1. CAGR = (End / Start)^(1/n) - 1.
2. End / Start = 133.1 / 100 = 1.331.
3. 1.331^(1/3) = 1.1 because 1.1 x 1.1 x 1.1 = 1.331.
4. CAGR = 1.1 - 1 = 10%.
5. Why simple averages mislead: take two years of +20% then +50%: simple average is 35% but 100 x 1.2 x 1.5 = 180, which is 34.16% a year (sqrt(1.8) = 1.3416). Averages over-state the compound rate.
**Fast method (30 seconds):** Recognise 1.1 cubed = 1.331, so 10%. Otherwise estimate and test.
**Check:** 100 x 1.1^3 = 133.1. Verified by script.
**Explain simply:**
- CAGR is the single steady yearly rate that gives the same end result.
- Each year's growth applies to a bigger (or smaller) base, so rates multiply rather than add.
**Likely follow-ups:** 1) *CAGR if 100 grows to 144 in 2 years?* 20%. 2) *What is the 3-year total growth?* 33.1%, not 30%.
**Common mistakes / traps:** Dividing the total growth by years (33.1 / 3 = 11.03%), which over-states the rate.

### Q92 ⭐ 🔴 What is the difference between a caselet and a standard data interpretation set, and how should you structure a caselet?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Reading skills: extracting structured data from a text passage.
**Say this in the interview:** "A caselet is a paragraph of numbers with no table. I turn it into a table or tree first, then answer."
**Answer:** **A standard DI set gives a ready table or chart; a caselet gives the same data hidden in a paragraph, so you must build the table yourself before answering.**
**Step-by-step working:**
1. Read the question lines first, so you know which numbers matter.
2. List every number with its label (what, which group, which year, unit).
3. Draw a small table, Venn diagram or tree; fill in the data; use equations for missing values (e.g. total = A + B).
4. Check that parts add up to totals; then answer.
5. Example: "A company has 800 employees; 55% male; 40% of males and 30% of females in Tech." Table: males 440, females 360; Tech males 176, Tech females 108; total Tech 284.
**Fast method (30 seconds):** Turn words into a table, then it is an ordinary table question.
**Explain simply:**
- Caselets cost more time because you build the table before you can answer; they reward neat structure.
- Re-read for qualifiers like "of which", "more than", "only".
**Likely follow-ups:** 1) *Which first: question or passage?* Skim the questions first. 2) *If a number is not given?* Use a variable and the totals to find it.
**Common mistakes / traps:** Skipping the table and reading from memory, and mistaking a percent of a subgroup for a percent of the total.

### Q93 ⭐ 🔴 How should you approach a mixed-graph set (a bar chart plus a table), and what do you check first?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Combining sources and checking consistent units.
**Say this in the interview:** "I read titles, axes and units of both the bar chart and the table first, then see how they link: usually one gives a total and the other a share or a rate."
**Answer:** **Check titles, units, years and the link between the two sources (the shared key such as year or department) first, then answer, converting units so both agree.**
**Step-by-step working:**
1. Read the chart title, axis labels and units (Rs lakh? thousand? percent?).
2. Read the table headings and footnotes (is it a percentage or a count?).
3. Find the link: for example a bar shows revenue by year and the table shows margin % by year, so profit = revenue x margin.
4. Read only the cells you need and write the formula.
5. Check units and base before the final calculation.
**Fast method (30 seconds):** Ask "what does one source give that the other lacks?" and join them on the common label.
**Explain simply:**
- Mixed sets usually need a two-step: one value from each source.
- Mismatched units (lakh versus crore) are the usual trap.
**Likely follow-ups:** 1) *Bar gives revenue 300 lakh, table gives margin 15%: profit?* 45 lakh. 2) *What if the table is in crore?* Convert first (1 crore = 100 lakh).
**Common mistakes / traps:** Mixing a percent from the table with a count from the chart as if both were counts.

### Q94 ⭐ 🔴 What is a good time budget per data interpretation question in a 12 question, 12 minute set, and which questions should you skip?

**Asked at:** commonly asked (no company-specific report found); data interpretation (DI) appears in prep-site lists for TCS NQT, Infosys, Accenture and a pie chart set was reported in a 2025 Novartis review (unverified prep-site and snippet-level claims).
**What the interviewer is checking:** Time management under pressure.
**Say this in the interview:** "12 minutes for 12 questions is 60 seconds each. I do quick lookups first, skip heavy multi-step ones, and return if time remains."
**Answer:** **About 60 seconds per question (12 min / 12 = 1 min); skip or defer the long multi-step calculations and attempt the direct lookups and simple percentages first.**
**Step-by-step working:**
1. Time budget: 12 minutes / 12 questions = 1 minute each; aim for 45 to 50 seconds on easy ones to bank time for harder ones.
2. Triage on the first read: lookup, a sum or a simple percent is easy (do now); weighted averages, compound changes or three-step questions are hard (flag and skip).
3. Skip a question if you have used 90 seconds without a clear route; guess an option only if there is no negative marking.
4. Spend any saved time on the flagged ones.
**Fast method (30 seconds):** Use approximations when the options are far apart; calculate fully only when options are close.
**Explain simply:**
- The goal is the maximum marks in the set, not clearing in order.
- Many tests have no penalty for guessing, so check the marking rule.
**Likely follow-ups:** 1) *How long for the first read of a set?* About 15 to 20 seconds. 2) *How to practise?* Time 12-question sets and review which types burned time.
**Common mistakes / traps:** Spending three minutes on one hard question and leaving the easy ones unattempted.

