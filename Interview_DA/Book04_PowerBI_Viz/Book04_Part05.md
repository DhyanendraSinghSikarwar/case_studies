# Book 4 — Power BI & Visualization | Part 5: DAX Advanced (Filter Context, Time Intelligence, ALL vs ALLEXCEPT, RANKX, Variables) 🔴

**Target:** 35 questions | **Actual:** 35 questions
**Scope:** advanced practical DAX for analysts: filter and row context, CALCULATE modifiers (ALL, ALLEXCEPT, ALLSELECTED, REMOVEFILTERS, KEEPFILTERS), context transition, time intelligence, RANKX and Top N, variables, DAX debugging and performance. Basics (calculated column vs measure, SUM vs SUMX, COUNT, basic CALCULATE) are in Part 4.

### Q1 ⭐⭐⭐ 🟢 What is the difference between ALL and ALLEXCEPT in DAX?
**Asked at:** commonly asked; research/interview_processes.md lists "ALL vs ALLEXCEPT" among Power BI/DAX concept questions for service MNCs (no single company named).
**What the interviewer is checking:** Do you understand filter context (the filters a visual silently applies to a measure) and how to remove some or all of it?
**Say this in the interview:** "ALL removes every filter from a table or column, so I get the grand total. ALLEXCEPT removes every filter on the table except the columns I name, so I get a subtotal that still respects those columns. I use ALL for percent of grand total and ALLEXCEPT for percent of a group total."
**Explain simply:**
- Filter context = the slicers, rows and columns of a visual that decide which rows a measure sees.
- `ALL(Sales)` ignores all of them. `ALLEXCEPT(Sales, Sales[Region])` ignores all of them except Region.
- Both are used inside `CALCULATE`, the function that changes filter context.
**Example:** Sales by region and product. For North-Laptop (300), the grand total is 1,250 (ALL) and the North total is 600 (ALLEXCEPT on Region). Share of North = 300/600 = 50%.
**Sample data:**

*Table Sales (one row per region and product):*

| Region | Product | Amount |
|---|---|---|
| North | Laptop | 300 |
| North | Phone | 200 |
| North | Tablet | 100 |
| East | Laptop | 200 |
| East | Phone | 100 |
| East | Tablet | 50 |
| West | Laptop | 100 |
| West | Phone | 150 |
| West | Tablet | 50 |

**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Total Sales = SUM ( Sales[Amount] )
Grand Total = CALCULATE ( [Total Sales], ALL ( Sales ) )
Region Total = CALCULATE ( [Total Sales], ALLEXCEPT ( Sales, Sales[Region] ) )
```
**Alternative:** `CALCULATE ( [Total Sales], REMOVEFILTERS ( Sales[Product] ) )` gives the same Region Total when Product is the only other filter (see Q29).
**Result:** (reproduced with pandas) in the North rows:

| Region | Product | Total Sales | Grand Total | Region Total |
|---|---|---|---|---|
| North | Laptop | 300 | 1250 | 600 |
| North | Phone | 200 | 1250 | 600 |
| North | Tablet | 100 | 1250 | 600 |

**Pandas check:**
```python
tot = S.Amount.sum(); north = S[S.Region=="North"].Amount.sum()
print(tot, north)   # 1250 600
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** ALLEXCEPT keeps filters only on the columns you list; a slicer on any other column of that table is removed too. In a visual that has no filter on the kept column, ALLEXCEPT behaves like ALL.
**Likely follow-ups:** 1) *Does ALL ignore slicers?* Yes, all of them on that table (use ALLSELECTED to respect them, Q7). 2) *Why do some experts avoid ALLEXCEPT?* It is fragile when columns are added (Q29).
**Common mistakes:** Naming a column from another table in ALLEXCEPT; using ALL(Table) when only one column should be cleared.

### Q2 ⭐⭐⭐ 🟢 Why do time intelligence functions need a date table, and what rules must it follow?
**Asked at:** commonly asked (no company-specific report found); the date-table topic appears in the Weekday Power BI list and most DAX prep sets we found.
**What the interviewer is checking:** Do you know why YTD, YoY and similar measures break without a proper calendar?
**Say this in the interview:** "Time intelligence functions move through dates, like 'same period last year'. They need a separate date table with one row per day, no gaps, covering whole years, with a Date column of Date type, marked as the date table and related to the fact table."
**Explain simply:**
- Time intelligence = functions such as TOTALYTD and SAMEPERIODLASTYEAR that shift or widen a date range.
- The date table must have a continuous list of dates (no missing days), every date once, starting 1 January of the first year and ending 31 December of the last year.
- The column must be Date or Date/Time type; time parts should be removed so each date is unique.
- Mark it as a date table, and relate its Date column to the date column in the fact table (one-to-many, Date table on the one side).
- Use the date table's columns (Month, Year) in visuals, not the fact table's dates.
**Example:** An HR table of joining dates has no row for 5 March because nobody joined. Without a full calendar, "same period last year" can land on a missing day and give wrong or blank numbers.
**DAX / Steps:** Creation steps in Q11. Check: Table view > select Date column > the table should show as marked. (Not run here (no DAX engine available); the values below were reproduced with pandas.)
**Alternative:** Rely on Power BI's automatic date/time hidden tables (an option in Options > Data Load). Fine for quick work, but you cannot share one calendar across tables or add fiscal columns, so a real date table is preferred.
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** Fact data with dates beyond the calendar end are not covered; time-of-day values in the fact column break the relationship match; several date columns in one fact table need extra relationships (Q22).
**Likely follow-ups:** 1) *Can I use the fact table's date column?* Only with auto date/time; a dedicated table is better. 2) *Fiscal year?* Add FY columns or use the year-end argument (Q24).
**Common mistakes:** Building the calendar only from the dates that appear in the data; not marking it; leaving it unrelated.

### Q3 ⭐⭐⭐ 🟡 Write a DAX measure for percentage of total sales (each product's share of the grand total).
**Asked at:** commonly asked (no company-specific report found); "percent of total" is on the Weekday 2026 Power BI list.
**What the interviewer is checking:** Can you divide a row's value by a total that ignores the row's filter?
**Say this in the interview:** "I divide the current sales by sales with the product filter removed, using DIVIDE so a zero denominator does not error."
**Explain simply:**
- Each product row sees only its own sales; to get the grand total I remove the product filter inside CALCULATE.
- DIVIDE returns blank instead of an error if the denominator is 0.
- Format the measure as Percentage.
**Example:** Laptop sells 600 out of 1,250 in total, so its share is 48%.
**Sample data:** Table Sales in Q1 (grouped by product):

| Product | Total Sales |
|---|---|
| Laptop | 600 |
| Phone | 450 |
| Tablet | 200 |

**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Total Sales = SUM ( Sales[Amount] )
% of Total = DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALL ( Sales[Product] ) ) )
```
**Alternative:** Use `REMOVEFILTERS ( Sales[Product] )` instead of ALL, or use ALLSELECTED if the share should be of what the slicers selected (Q7).
**Result:** (reproduced with pandas) Laptop 48.0%, Phone 36.0%, Tablet 16.0%; the Total row shows 100%.
**Pandas check:**
```python
p = S.groupby("Product").Amount.sum(); print((p/p.sum()*100).round(1).to_dict())
# {'Laptop': 48.0, 'Phone': 36.0, 'Tablet': 16.0}
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** With a Region slicer, ALL(Sales[Product]) still keeps the Region filter, so the share is of the region total; use ALL(Sales) for the true grand total. Blank products show nothing.
**Likely follow-ups:** 1) *Percent of parent in a hierarchy?* Use ISINSCOPE-based logic (later question). 2) *Why DIVIDE over `/`?* Safe zero handling.
**Common mistakes:** Using ALL on the whole table when only one column should be cleared; writing the denominator as SUM, which still obeys the row filter.

### Q4 ⭐⭐⭐ 🟡 Write a DAX measure for year-to-date (YTD) sales.
**Asked at:** commonly asked (no company-specific report found); YTD is on the Weekday 2026 list.
**What the interviewer is checking:** Do you know the time-intelligence shortcut and its date-table requirement?
**Say this in the interview:** "I use TOTALYTD on the date table's Date column. It adds up sales from 1 January of the year to the latest date in the current filter."
**Explain simply:**
- YTD = year to date: running total since the start of the year, restarting each year.
- It works on the Dates table, not the fact table's date column.
- In a monthly visual, each month shows the total from January up to that month.
**Example:** Monthly sales for 2025: Jan 110, Feb 130, Mar 100. YTD in March = 110+130+100 = 340.
**Sample data:**

*Table Dates (one row per day, marked as date table) and fact table Sales; monthly totals of Sales[Amount]:*

| Month | 2024 | 2025 |
|---|---|---|
| Jan | 100 | 110 |
| Feb | 120 | 130 |
| Mar | 90 | 100 |
| Apr | 150 | 170 |
| May | 130 | 150 |
| Jun | 170 | 190 |
| Jul-Dec | 160, 180, 140, 200, 190, 210 | no data yet |

**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Total Sales = SUM ( Sales[Amount] )
Sales YTD = TOTALYTD ( [Total Sales], Dates[Date] )
```
**Alternative:** `CALCULATE ( [Total Sales], DATESYTD ( Dates[Date] ) )` (Q9).
**Result:** (reproduced with pandas) 2025: Jan 110, Feb 240, Mar 340, Apr 510, May 660, Jun 850. 2024: Jan 100, Feb 220, Mar 310, Apr 460, May 590, Jun 760.
**Pandas check:**
```python
M["YTD"] = M.groupby("Year").Sales.cumsum(); print(M[M.Year==2025].YTD.tolist())
# [110, 240, 340, 510, 660, 850]
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** Month with no data still shows the carried YTD; a year-level total shows the full-year YTD. For a 31 March year end use the year_end_date argument (Q24).
**Likely follow-ups:** 1) *MTD/QTD?* Q13. 2) *Fiscal year?* Q24.
**Common mistakes:** Passing the fact table's date column; no marked date table; showing YTD against a Month name text column that sorts alphabetically.

### Q5 ⭐⭐⭐ 🟡 Write a DAX measure for year-over-year (YoY) sales growth percentage.
**Asked at:** commonly asked (no company-specific report found); YoY is on the Weekday 2026 list.
**What the interviewer is checking:** Can you combine a variable, a time shift and safe division?
**Say this in the interview:** "I store current sales and last year's sales in variables, then return (current minus last year) divided by last year, with DIVIDE so a missing prior year gives blank."
**Explain simply:**
- YoY growth % = (this year - last year) / last year.
- `SAMEPERIODLASTYEAR` shifts the dates in the current filter back one year.
- A variable (VAR) stores a value once so it is easy to read and reuse.
**Example:** March 2025 sales 100 vs March 2024 90: growth = 10/90 = 11.1%.
**Sample data:** Monthly totals as in Q4.
**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Sales PY = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( Dates[Date] ) )
Sales YoY % =
VAR Cur = [Total Sales]
VAR PY  = [Sales PY]
RETURN DIVIDE ( Cur - PY, PY )
```
**Alternative:** `CALCULATE ( [Total Sales], DATEADD ( Dates[Date], -1, YEAR ) )` for the prior-year measure (Q10).
**Result:** (reproduced with pandas) 2025 vs 2024: Jan 10.0%, Feb 8.3%, Mar 11.1%, Apr 13.3%, May 15.4%, Jun 11.8%.
**Pandas check:**
```python
M["PY"] = M.Sales.shift(12); print(((M.Sales-M.PY)/M.PY*100).round(1).iloc[12:].tolist())
# [10.0, 8.3, 11.1, 13.3, 15.4, 11.8]
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** First year has no prior year, so DIVIDE returns blank. If the date table already runs to 31 Dec 2025 but data stops in June, the 2025 total (850) is compared with full-year 2024 (1,840) and shows -53.8%; like-for-like (Jan-Jun 2024 = 760) is +11.8%. Limit the calendar or add a cut-off.
**Likely follow-ups:** 1) *Why not subtract in one line?* Variables read better and avoid recomputing. 2) *Difference vs previous month?* Use DATEADD(-1, MONTH).
**Common mistakes:** Dividing by current year; using the fact table date; ignoring partial-year totals.

### Q6 ⭐⭐⭐ 🟡 How does RANKX work? Write a measure that ranks employees by salary.
**Asked at:** commonly asked (no company-specific report found); RANKX is on the Weekday 2026 list.
**What the interviewer is checking:** Do you know RANKX ranks a value across a table you specify, and that the table must ignore the row's own filter?
**Say this in the interview:** "RANKX goes through each row of a table, calculates my measure for each, and returns where the current value sits. For employees I use ALL on the employee column so every employee is ranked against all others, highest salary first."
**Explain simply:**
- RANKX(table, expression, value, order, ties): the table is the list to compare; the expression is the measure.
- Default order is descending (biggest = 1) and default ties is Skip (Q16).
- The table must be un-filtered by the visual row, otherwise each row is alone and gets 1 (Q17).
**Example:** Five employees: Divya 91,000 is rank 1, Karan 58,000 rank 5.
**Sample data:** Table Employees:

| Employee | Salary |
|---|---|
| Asha | 85000 |
| Ravi | 62000 |
| Meena | 74000 |
| Karan | 58000 |
| Divya | 91000 |

**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Total Salary = SUM ( Employees[Salary] )
Salary Rank = RANKX ( ALL ( Employees[Employee] ), [Total Salary], , DESC )
```
**Alternative:** `ALLSELECTED ( Employees[Employee] )` to rank only among employees left after slicers (Q7).
**Result:** (reproduced with pandas) Divya 1, Asha 2, Meena 3, Ravi 4, Karan 5.
**Pandas check:**
```python
E["Rank"]=E.Salary.rank(method="min",ascending=False).astype(int); print(E.sort_values("Rank").Rank.tolist())
# [1, 2, 3, 4, 5]
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched). The research/Book04_Part05_sources.md file records an earlier fetch of the Microsoft Learn RANKX page (Skip default, Dense option, BLANK treated as 0); I did not re-read it.
**Edge cases:** Blank salaries are treated as 0 for ranking (per the sources note); at total level the rank is meaningless, so wrap with `IF ( HASONEVALUE ( Employees[Employee] ), ... )`.
**Likely follow-ups:** 1) *Ascending rank?* Use ASC. 2) *Ties?* Q16.
**Common mistakes:** Using the Employees table without ALL; ranking on a column instead of a measure.

### Q7 ⭐⭐ 🟢 What is the difference between ALL and ALLSELECTED?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know slicers can be respected or ignored for a total?
**Say this in the interview:** "ALL removes every filter, including slicers, so I get the true grand total. ALLSELECTED removes only the filters from the visual's own rows and columns, but keeps filters from slicers and outside the visual."
**Explain simply:**
- ALL = grand total of everything.
- ALLSELECTED = total of what the user has selected.
- For percent-of-visible-total use ALLSELECTED so the visual adds to 100%.
**Example:** Region slicer = North and East. Laptop is 500 of 950 visible (52.6%) but only 40% of 1,250 overall.
**Sample data:** Table Sales in Q1 with a Region slicer on North + East.
**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
% of All     = DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALL ( Sales ) ) )
% of Visible = DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALLSELECTED ( Sales[Product] ) ) )
```
Note: `ALL(Sales[Product])` alone would keep the Region slicer, so `ALL(Sales)` is used for the true grand total.
**Alternative:** Clear the slicer, which makes both identical.
**Result:** (reproduced with pandas) with ALL(Sales) as denominator (1,250): Laptop 40.0%, Phone 24.0%, Tablet 12.0%. With ALLSELECTED (950): 52.6%, 31.6%, 15.8%.
**Pandas check:**
```python
sel=S[S.Region.isin(["North","East"])]; ps=sel.groupby("Product").Amount.sum()
print((ps/1250*100).round(1).tolist(), (ps/ps.sum()*100).round(1).tolist())
# [40.0, 24.0, 12.0] [52.6, 31.6, 15.8]   (alphabetical: Laptop, Phone, Tablet)
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** ALLSELECTED depends on the visual shape; in a table with only a total row, it can behave differently. Filters inside the visual (visual-level filters) count as outside filters.
**Likely follow-ups:** 1) *Running total?* Often built with ALLSELECTED (Q15). 2) *Can both take columns?* Yes.
**Common mistakes:** Expecting ALL to respect slicers; using ALL(Column) and still getting a region-filtered total.

### Q8 ⭐⭐ 🟢 What is the difference between ALL and REMOVEFILTERS?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know REMOVEFILTERS is the clearer modern name for the "remove filters" role of ALL?
**Say this in the interview:** "They remove filters in the same way, but REMOVEFILTERS can only be used as a CALCULATE modifier, while ALL can also return a table of values for iterators like RANKX or FILTER. I use REMOVEFILTERS when I only want to clear a filter, because it states intent."
**Explain simply:**
- Same behaviour as a filter modifier.
- ALL(Column) also returns a table of distinct values, which you can loop over.
- REMOVEFILTERS returns nothing; it is just an instruction to CALCULATE.
**Example:** Share of Laptop: both versions return 600 / 1,250 = 48%.
**Sample data:** Table Sales in Q1.
**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Share ALL     = DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALL ( Sales ) ) )
Share REMOVE  = DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], REMOVEFILTERS ( Sales ) ) )
Rank          = RANKX ( ALL ( Sales[Product] ), [Total Sales] )  -- needs ALL, REMOVEFILTERS would not work here
```
**Alternative:** ALL for the table-returning cases.
**Result:** (reproduced with pandas) Both share measures give Laptop 48%, Phone 36%, Tablet 16% (600, 450, 200 of 1,250).
**Pandas check:**
```python
p=S.groupby("Product").Amount.sum(); print((p/S.Amount.sum()*100).tolist())  # [48.0, 36.0, 16.0]
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched). REMOVEFILTERS was added later than ALL; I could not confirm the exact Desktop release here, so very old Desktop versions may lack it.
**Edge cases:** REMOVEFILTERS with no argument clears every filter in the model.
**Likely follow-ups:** 1) *Which do you prefer?* REMOVEFILTERS for clearing, ALL when a table is needed. 2) *Why pair it with VALUES?* Q29.
**Common mistakes:** Using REMOVEFILTERS as an iterator table argument.

### Q9 ⭐⭐ 🟢 What is the difference between TOTALYTD and CALCULATE with DATESYTD?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know TOTALYTD is a shortcut for CALCULATE plus DATESYTD?
**Say this in the interview:** "They give the same answer. TOTALYTD is shorthand: expression, dates, optional filter, optional year-end. With CALCULATE and DATESYTD I write the filter explicitly, which is more flexible when I need extra modifiers."
**Explain simply:**
- DATESYTD returns the list of dates from the start of the year to the last date in context.
- CALCULATE applies that list to a measure; TOTALYTD does both in one call.
- Both take an optional year-end date for fiscal years (Q24).
**Example:** March 2025 YTD is 340 either way.
**Sample data:** Monthly totals as in Q4.
**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
YTD A = TOTALYTD ( [Total Sales], Dates[Date] )
YTD B = CALCULATE ( [Total Sales], DATESYTD ( Dates[Date] ) )
```
**Alternative:** DATESYTD with extra filters, e.g. `CALCULATE ( [Total Sales], DATESYTD ( Dates[Date] ), Sales[Region] = "North" )`.
**Result:** (reproduced with pandas) both: Jan 110, Feb 240, Mar 340, Apr 510, May 660, Jun 850 for 2025.
**Pandas check:** Same as Q4: `M[M.Year==2025].YTD.tolist()` prints `[110, 240, 340, 510, 660, 850]`.
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched). The Part 5 sources file notes Microsoft Learn describes the optional year_end_date string such as "3/31" for TOTALYTD (checked in an earlier session, not re-read by me).
**Edge cases:** Both give blank for dates not in the date table.
**Likely follow-ups:** 1) *Which is faster?* Same engine behaviour in practice. 2) *Can I add a filter?* Yes, in both.
**Common mistakes:** Believing they differ in result.

### Q10 ⭐⭐ 🟢 What is the difference between SAMEPERIODLASTYEAR, DATEADD and PARALLELPERIOD?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know which time-shift function returns exactly the same dates and which returns whole periods?
**Say this in the interview:** "SAMEPERIODLASTYEAR is a shortcut to move back one year. DATEADD shifts the dates by any number of days, months, quarters or years and keeps the same dates. PARALLELPERIOD shifts to a whole period, so a two-month selection comes back as the full parallel period."
**Explain simply:**
- SAMEPERIODLASTYEAR = DATEADD(-1, YEAR) in effect.
- DATEADD keeps the selected span (Jan-Feb stays Jan-Feb).
- PARALLELPERIOD expands to full periods of the interval (a full year if the interval is YEAR).
**Example:** Selection Jan-Feb 2025 (sales 240). SAMEPERIODLASTYEAR and DATEADD give Jan-Feb 2024 (220). PARALLELPERIOD(-1, YEAR) gives all of 2024 (1,840).
**Sample data:** Monthly totals as in Q4.
**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
PY SPLY  = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( Dates[Date] ) )
PY DATEADD = CALCULATE ( [Total Sales], DATEADD ( Dates[Date], -1, YEAR ) )
PY PARALLEL = CALCULATE ( [Total Sales], PARALLELPERIOD ( Dates[Date], -1, YEAR ) )
```
**Alternative:** `DATEADD ( Dates[Date], -1, MONTH )` for previous month comparison.
**Result:** (reproduced with pandas) 220, 220, 1840.
**Pandas check:**
```python
print(sum(m24[:2]), sum(m24[:2]), sum(m24))   # 220 220 1840
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** DATEADD needs a continuous selection of dates; month-end handling (31 Mar minus a month) follows the calendar. PARALLELPERIOD behaviour for partial periods is from memory; test it.
**Likely follow-ups:** 1) *Which for YoY?* SAMEPERIODLASTYEAR. 2) *Which for previous month?* DATEADD.
**Common mistakes:** Using PARALLELPERIOD for YoY and getting full-year denominators.

### Q11 ⭐⭐ 🟢 How do you create and mark a date table in Power BI, and what is the difference between CALENDAR and CALENDARAUTO?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you build a calendar and know the two generators?
**Say this in the interview:** "I create a calculated table with CALENDAR using my own start and end dates, or CALENDARAUTO, which looks at all date columns in the model and gives full years automatically. Then I add Year, Month and Quarter columns, mark it as a date table and relate it to the fact table."
**Explain simply:**
- CALENDAR(start, end): exactly the range you give.
- CALENDARAUTO(): scans the model's date columns, then returns 1 January of the earliest year to 31 December of the latest year.
- Marking as date table tells Power BI which column is the date key.
**Example:** Data runs 15 Mar 2024 to 20 Jun 2025. CALENDARAUTO returns 1 Jan 2024 to 31 Dec 2025, which is 731 rows.
**Sample data:** Fact dates 2024-03-15 and 2025-06-20 (min and max).
**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Dates = CALENDAR ( DATE ( 2024, 1, 1 ), DATE ( 2025, 12, 31 ) )
Dates Auto = CALENDARAUTO ()
Year = YEAR ( Dates[Date] )
Month = FORMAT ( Dates[Date], "MMM" )
Month No = MONTH ( Dates[Date] )
```
Click-path (menu names unverified, may differ by build): Modeling tab > New table > type the formula; add columns with New column; select the table, then Table tools/Modeling > Mark as date table > choose Date column; sort Month by Month No (Column tools > Sort by column).
**Alternative:** Build the calendar in Power Query (List.Dates) or import a calendar table from the data warehouse.
**Result:** (reproduced with pandas) 2024-01-01 to 2025-12-31, 731 rows.
**Pandas check:**
```python
print((pd.Timestamp(2025,12,31)-pd.Timestamp(2024,1,1)).days+1)   # 731
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched). Desktop is the authoring tool; the calculated table is created in Desktop.
**Edge cases:** CALENDARAUTO takes an optional fiscal year-end month (from memory); a stray date like 1900 in the data stretches the calendar for decades; pick CALENDAR then.
**Likely follow-ups:** 1) *Why not use the fact dates?* Gaps (Q2). 2) *Fiscal year?* Q24.
**Common mistakes:** Forgetting Sort by column for months; leaving a 1900 default date in the data.

### Q12 ⭐⭐ 🟡 What happens when you pass two filters on the same column, or on different columns, to CALCULATE?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know how CALCULATE combines filters?
**Say this in the interview:** "Filters in CALCULATE are combined with AND. Two Boolean filters on the same column both have to be true, so Product = Laptop and Product = Phone returns blank. For OR I use IN or the || operator. Filters on different columns intersect, like North AND Laptop."
**Explain simply:**
- A filter in CALCULATE replaces any existing filter on the same column, unless wrapped in KEEPFILTERS (Q28).
- A filter on a different column adds to the existing filters.
- Multiple arguments = AND.
**Example:** Product IN {Laptop, Phone} = 1,050; Region North AND Product Laptop = 300.
**Sample data:** Table Sales in Q1.
**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Both Same Col = CALCULATE ( [Total Sales], Sales[Product] = "Laptop", Sales[Product] = "Phone" )  -- blank
Either         = CALCULATE ( [Total Sales], Sales[Product] IN { "Laptop", "Phone" } )            -- 1050
Diff Cols      = CALCULATE ( [Total Sales], Sales[Region] = "North", Sales[Product] = "Laptop" )   -- 300
```
**Alternative:** `FILTER ( ALL ( Sales[Product] ), ... )` for complex conditions.
**Result:** (reproduced with pandas) blank (0 rows), 1050, 300. Extra: in a visual filtered to Phone, `CALCULATE(..., Product = "Laptop")` returns 600 (replaces), and with KEEPFILTERS returns blank.
**Pandas check:**
```python
print(S[(S.Product=="Laptop")&(S.Product=="Phone")].Amount.sum(), S[S.Product.isin(["Laptop","Phone"])].Amount.sum(), S[(S.Region=="North")&(S.Product=="Laptop")].Amount.sum())
# 0 1050 300
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** Boolean filters work on one column only; using two columns in one Boolean needs FILTER.
**Likely follow-ups:** 1) *OR across two columns?* FILTER with ||. 2) *Visual filter on same column?* Overridden.
**Common mistakes:** Expecting OR; expecting the slicer to combine with a same-column filter.

### Q13 ⭐⭐ 🟡 Write a DAX measure for month-to-date (MTD) and quarter-to-date (QTD) values.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you extend the YTD idea to month and quarter?
**Say this in the interview:** "TOTALMTD and TOTALQTD, or CALCULATE with DATESMTD and DATESQTD, on the date table. They add up from the start of the month or quarter to the current date."
**Explain simply:**
- MTD resets each month, QTD each calendar quarter.
- In a daily view the value grows through the period.
**Example:** At 28 Mar 2025: MTD = 270, QTD (Jan-Mar) = 840.
**Sample data:** Table Sales (date, amount):

| Date | Amount |
|---|---|
| 2025-01-10 | 100 |
| 2025-01-25 | 150 |
| 2025-02-05 | 200 |
| 2025-02-20 | 120 |
| 2025-03-03 | 180 |
| 2025-03-28 | 90 |
| 2025-04-02 | 160 |
| 2025-04-18 | 140 |
| 2025-05-06 | 110 |

**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Sales MTD = TOTALMTD ( [Total Sales], Dates[Date] )
Sales QTD = TOTALQTD ( [Total Sales], Dates[Date] )
```
**Alternative:** `CALCULATE ( [Total Sales], DATESMTD ( Dates[Date] ) )`, same for DATESQTD.
**Result:** (reproduced with pandas)

| As of | MTD | QTD |
|---|---|---|
| 2025-02-20 | 320 | 570 |
| 2025-03-28 | 270 | 840 |
| 2025-04-18 | 300 | 300 |
| 2025-05-06 | 110 | 410 |

**Pandas check:** period filter on `Date.dt.to_period("M")` / `"Q"` and `Date <= d`; output matches the table above.
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** Quarters are calendar quarters; a fiscal quarter needs a custom calendar column approach.
**Likely follow-ups:** 1) *Month-level visual?* Shows the full month to date. 2) *Fiscal?* Q24.
**Common mistakes:** Using the fact date column; expecting fiscal quarters.

### Q14 ⭐⭐ 🟡 Write a DAX measure for a rolling 3-month average using DATESINPERIOD.
**Asked at:** commonly asked; DATESINPERIOD is on the Weekday 2026 Power BI list.
**What the interviewer is checking:** Can you build a moving window and average monthly totals, not rows?
**Say this in the interview:** "I take the last 3 months ending at the current date with DATESINPERIOD, then use AVERAGEX over the months to average the monthly totals."
**Explain simply:**
- DATESINPERIOD(dates, end, -3, MONTH) returns the 3 months up to the end date.
- AVERAGEX loops over months, evaluates the monthly sales, and averages them (blank months are skipped).
**Example:** March 2024: (100+120+90)/3 = 103.3.
**Sample data:** Monthly totals as in Q4.
**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Sales 3M Avg =
AVERAGEX (
    DATESINPERIOD ( Dates[Date], MAX ( Dates[Date] ), -3, MONTH ),
    [Total Sales] )   -- averages daily totals, wrong
```
That version averages days, so use months:
```dax
Sales 3M Avg =
VAR Win = DATESINPERIOD ( Dates[Date], MAX ( Dates[Date] ), -3, MONTH )
RETURN
    AVERAGEX ( CALCULATETABLE ( VALUES ( Dates[YearMonth] ), Win ), [Total Sales] )
```
(Needs a `YearMonth` column in Dates, e.g. `FORMAT ( Dates[Date], "yyyy-mm" )`.)
**Alternative:** Divide `CALCULATE ( [Total Sales], Win )` by 3 (fixed divisor; wrong for the first months).
**Result:** (reproduced with pandas, partial windows at the start averaged over available months) 2024: Jan 100.0, Feb 110.0, Mar 103.3, Apr 120.0, May 123.3, Jun 150.0, Jul 153.3, Aug 170.0; 2025: Jan 170.0, Feb 150.0, Mar 113.3, Apr 133.3, May 140.0, Jun 170.0.
**Pandas check:**
```python
M["Roll3"]=M.Sales.rolling(3,min_periods=1).mean().round(1); print(M.Roll3.iloc[:4].tolist())  # [100.0, 110.0, 103.3, 120.0]
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** Whether the first window averages 1 month or shows blank is a design choice; the calendar must cover the prior months.
**Likely follow-ups:** 1) *Why not AVERAGE?* Averages rows. 2) *Month-end problems?* Dates end at month end in a monthly visual.
**Common mistakes:** Averaging the daily/row values; hard-coding divide by 3.

### Q15 ⭐⭐ 🟡 Write a DAX measure for a running (cumulative) total over dates.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know how to write "all dates up to the current one"?
**Say this in the interview:** "I remove the date filter and re-add every date up to the latest date in the current context, so each point shows everything so far."
**Explain simply:**
- ALL on the date column clears the date filter; the FILTER keeps dates less than or equal to the latest visible date.
- Unlike YTD it never resets.
**Example:** Cumulative at Mar 2024 = 100+120+90 = 310; at Jun 2025 = 2,690.
**Sample data:** Monthly totals as in Q4 (2024 full, 2025 Jan-Jun).
**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Running Total =
CALCULATE ( [Total Sales], FILTER ( ALL ( Dates[Date] ), Dates[Date] <= MAX ( Dates[Date] ) ) )
```
**Alternative:** `FILTER ( ALLSELECTED ( Dates[Date] ), ... )` to start from the first selected date; or `DATESBETWEEN ( Dates[Date], BLANK(), MAX ( Dates[Date] ) )` (from memory, test it).
**Result:** (reproduced with pandas) Jan 2024 100, Feb 220, Mar 310, Dec 1,840, Jan 2025 1,950, Feb 2,080, Jun 2,690.
**Pandas check:**
```python
print(M.Sales.cumsum().iloc[[0,1,2,11,12,13,17]].tolist())  # [100, 220, 310, 1840, 1950, 2080, 2690]
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** Future months with no sales still show the last cumulative value; hide with `IF ( MAX ( Dates[Date] ) <= MAX ( Sales[Date] ), ... )`. The Total row shows the grand cumulative.
**Likely follow-ups:** 1) *Reset each year?* Use YTD. 2) *Performance?* ALL over the full date column is fine at normal sizes.
**Common mistakes:** Forgetting ALL, so the filter stays at one month.

### Q16 ⭐⭐ 🟡 How does RANKX handle ties, and what is the difference between Skip and Dense?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the tie options and how they change later ranks?
**Say this in the interview:** "Skip is the default: tied values share a rank and the next rank jumps. Dense does not leave gaps. For two people tied at 2, Skip gives 1, 2, 2, 4 and Dense gives 1, 2, 2, 3."
**Explain simply:**
- Ties = equal values.
- Skip leaves a gap after ties; Dense numbers consecutively.
- Choose Dense for "top 3 levels", Skip for "position in a league table".
**Example:** Two employees at 85,000 are both rank 2.
**Sample data:** Table Employees:

| Employee | Salary |
|---|---|
| Divya | 91000 |
| Asha | 85000 |
| Meena | 85000 |
| Ravi | 74000 |
| Karan | 62000 |
| Neha | 62000 |

**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Rank Skip  = RANKX ( ALL ( Employees[Employee] ), [Total Salary], , DESC, Skip )
Rank Dense = RANKX ( ALL ( Employees[Employee] ), [Total Salary], , DESC, Dense )
```
**Alternative:** Add a tie-breaker (e.g. employee ID) to get unique ranks.
**Result:** (reproduced with pandas)

| Employee | Skip | Dense |
|---|---|---|
| Divya | 1 | 1 |
| Asha | 2 | 2 |
| Meena | 2 | 2 |
| Ravi | 4 | 3 |
| Karan | 5 | 4 |
| Neha | 5 | 4 |

**Pandas check:**
```python
print(T.Salary.rank(method="min",ascending=False).astype(int).tolist(), T.Salary.rank(method="dense",ascending=False).astype(int).tolist())
# [1, 2, 2, 4, 5, 5] [1, 2, 2, 3, 4, 4]
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched). Skip as default and the Dense option are recorded in research/Book04_Part05_sources.md from an earlier fetch of the RANKX page.
**Edge cases:** Decimal precision noise can break ties (tiny differences); round the measure.
**Likely follow-ups:** 1) *Unique ranks?* Tie-breaker. 2) *Rank filter in a Top N?* Q18.
**Common mistakes:** Assuming no gaps; floating-point ties.

### Q17 ⭐⭐ 🟡 Why does a RANKX measure return 1 for every row in a visual, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found; a standard debugging question).
**What the interviewer is checking:** Do you understand filter context applies to the table you rank over?
**Say this in the interview:** "Each row of the visual filters the table, so RANKX only sees that one row's product and ranks it against itself. Wrapping the table in ALL (or ALLSELECTED) removes that row filter so all products are compared."
**Explain simply:**
- Rank needs a list of all competitors; a filtered list has just one.
- Fix: `ALL ( Products[Product] )` or `ALLSELECTED`.
- Check the measure is a real measure, not a column.
**Example:** Seven products; wrong measure gives 1 in every row, fixed gives 1, 2, 2, 4, 5, 6, 7.
**Sample data:** Table Products by Sales:

| Product | Sales |
|---|---|
| A | 500 |
| B | 420 |
| C | 420 |
| D | 380 |
| E | 300 |
| F | 250 |
| G | 90 |

**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Rank Wrong = RANKX ( Products, [Total Sales] )                      -- 1 on every row
Rank Fixed = RANKX ( ALL ( Products[Product] ), [Total Sales] )
```
**Alternative:** `ALLSELECTED ( Products[Product] )` to rank only the selected products.
**Result:** (reproduced with pandas) wrong = 1 for all; fixed = 1, 2, 2, 4, 5, 6, 7.
**Pandas check:**
```python
print(P.Sales.rank(method="min",ascending=False).astype(int).tolist())  # [1, 2, 2, 4, 5, 6, 7]
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** At the total row, ranking is not meaningful; guard with HASONEVALUE.
**Likely follow-ups:** 1) *Other cause?* Ranking over a fact table. 2) *Slicers?* ALLSELECTED respects them.
**Common mistakes:** Ranking the visual's own table; ALL(Table) when other filters should stay.

### Q18 ⭐⭐ 🟡 How would you show only the Top 5 products by sales using TOPN or RANKX?
**Asked at:** commonly asked; "Top 5" appears on the Weekday 2026 Power BI list (Top 5 + Others).
**What the interviewer is checking:** Do you know the simple visual filter and the DAX approaches?
**Say this in the interview:** "The simplest way is a Top N visual-level filter. In DAX I use RANKX and return sales only if the rank is 5 or less, or TOPN to build the list of top 5 products. I mention ties: TOPN can return more than 5."
**Explain simply:**
- TOPN(5, table, measure) returns the five highest rows.
- RANKX approach: `IF ( [Rank] <= 5, [Total Sales] )` hides the others.
- Visual route: Filters pane > product field > Filter type Top N > Show items Top 5 > By value.
**Example:** Sales A 500, B 420, C 420, D 380, E 300, F 250, G 90: top 5 are A to E (1,720 total).
**Sample data:** Table Products in Q17.
**DAX / Steps:** (Not run here (no DAX engine available); the values below were reproduced with pandas.)
```dax
Top 5 Sales =
VAR R = RANKX ( ALL ( Products[Product] ), [Total Sales] )
RETURN IF ( R <= 5, [Total Sales] )

Top 5 Total =
CALCULATE ( [Total Sales], TOPN ( 5, ALL ( Products[Product] ), [Total Sales] ) )
```
**Alternative:** Visual-level Top N filter (no DAX).
**Result:** (reproduced with pandas) A, B, C, D, E shown (F, G blank); Top 5 total 1,720. With a tie at 5th (E and F both 300) both TOPN and rank <= 5 return six products: A to F.
**Pandas check:**
```python
print(P.nlargest(5,"Sales",keep="all").Product.tolist())   # ['A','B','C','D','E']
# tie case (E=F=300): ['A', 'B', 'C', 'D', 'E', 'F']
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft Learn page was fetched).
**Edge cases:** Ties at the cut-off return extra rows; the Total row of "Top 5 Sales" sums only the visible ones.
**Likely follow-ups:** 1) *Top 5 plus Others?* Add a measure for total minus top 5. 2) *Top 5 per category?* Rank inside ALLEXCEPT or VALUES category.
**Common mistakes:** Forgetting ALL, so TOPN sees one row; ignoring ties.

### Q19 ⭐⭐ 🟡 Write a DAX measure for employee attrition rate (leavers divided by average headcount).
**Asked at:** commonly asked (no company-specific report found); HR measures are gap-fill questions in the sources file, not seen in a source list.
**What the interviewer is checking:** Can you turn an HR formula (leavers / average headcount) into a DAX measure that follows the date filter?
**Say this in the interview:** "Attrition rate is people who left in the period divided by the average headcount of that period. In DAX I count leavers between the first and last date in the filter, work out opening and closing headcount, average them, and use DIVIDE so a zero denominator does not error."
**Explain simply:**
- **Leavers** = employees whose exit date falls inside the selected period.
- **Average headcount** = (headcount at the start + headcount at the end) / 2. Some companies average 12 month-ends instead; say which you use.
- **Headcount on a day** = joined on or before that day and not yet exited (exit date blank or later).
- `DIVIDE(a, b)` is a safe divide: it returns blank, not an error, when b is 0.
- Monthly attrition is not yearly: multiply a monthly rate by 12 only if the interviewer asks to annualise.
**Example:** Calendar 2025: 8 people on payroll on 31 Dec 2024, 6 on 31 Dec 2025, 4 leavers. Average = 7, so attrition = 4 / 7 = 57.1% (tiny 10-person sample, chosen so every case is visible).
**Sample data:** Table `Employees` (blank ExitDate = still working). `Dates` is a normal date table with no active relationship to Employees.

| EmpID | JoinDate | ExitDate |
|---|---|---|
| 1 | 2022-03-01 | |
| 2 | 2023-06-15 | 2025-04-30 |
| 3 | 2021-01-10 | |
| 4 | 2024-02-01 | 2025-09-15 |
| 5 | 2020-08-20 | 2025-01-31 |
| 6 | 2023-11-05 | |
| 7 | 2025-02-10 | |
| 8 | 2025-07-01 | 2025-11-30 |
| 9 | 2019-05-05 | |
| 10 | 2024-09-09 | |

**DAX / Steps (not run here):**
```dax
Leavers =
VAR StartD = MIN ( Dates[Date] )
VAR EndD   = MAX ( Dates[Date] )
RETURN
    CALCULATE (
        COUNTROWS ( FILTER ( Employees,
            Employees[ExitDate] >= StartD && Employees[ExitDate] <= EndD ) ),
        REMOVEFILTERS ( Dates )
    )

Average Headcount =
VAR StartD  = MIN ( Dates[Date] )
VAR EndD    = MAX ( Dates[Date] )
VAR Opening =
    CALCULATE (
        COUNTROWS ( FILTER ( Employees,
            Employees[JoinDate] < StartD
            && ( ISBLANK ( Employees[ExitDate] ) || Employees[ExitDate] >= StartD ) ) ),
        REMOVEFILTERS ( Dates )
    )
VAR Closing =
    CALCULATE (
        COUNTROWS ( FILTER ( Employees,
            Employees[JoinDate] <= EndD
            && ( ISBLANK ( Employees[ExitDate] ) || Employees[ExitDate] > EndD ) ) ),
        REMOVEFILTERS ( Dates )
    )
RETURN ( Opening + Closing ) / 2

Attrition % = DIVIDE ( [Leavers], [Average Headcount] )
```
**Alternative:** Average the 12 month-end headcounts with `AVERAGEX ( VALUES ( Dates[MonthEnd] ), [Headcount EOM] )` (see Q20). Smoother when headcount swings inside the year.
**Result (reproduced with pandas, not run in Power BI):** Opening 8, closing 6, leavers 4, average 7.0, attrition 57.1% for 2025.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({
 "EmpID":[1,2,3,4,5,6,7,8,9,10],
 "JoinDate":pd.to_datetime(["2022-03-01","2023-06-15","2021-01-10","2024-02-01","2020-08-20","2023-11-05","2025-02-10","2025-07-01","2019-05-05","2024-09-09"]),
 "ExitDate":pd.to_datetime([None,"2025-04-30",None,"2025-09-15","2025-01-31",None,None,"2025-11-30",None,None])})
S, E_ = pd.Timestamp("2025-01-01"), pd.Timestamp("2025-12-31")
def hc(d):   # on payroll at end of day d
    return ((emp.JoinDate<=d) & (emp.ExitDate.isna() | (emp.ExitDate>d))).sum()
opening = hc(S - pd.Timedelta(days=1))
closing = hc(E_)
leavers = emp.ExitDate.between(S, E_).sum()
avg = (opening+closing)/2
print(emp.assign(JoinDate=emp.JoinDate.dt.date, ExitDate=emp.ExitDate.dt.date).to_string(index=False))
print("opening",opening,"closing",closing,"leavers",leavers,"avg",avg,"attrition %",round(leavers/avg*100,1))
```
Output:
```
 EmpID   JoinDate   ExitDate
     1 2022-03-01        NaT
     2 2023-06-15 2025-04-30
     3 2021-01-10        NaT
     4 2024-02-01 2025-09-15
     5 2020-08-20 2025-01-31
     6 2023-11-05        NaT
     7 2025-02-10        NaT
     8 2025-07-01 2025-11-30
     9 2019-05-05        NaT
    10 2024-09-09        NaT
opening 8 closing 6 leavers 4 avg 7.0 attrition % 57.1
```
**Version / licensing note:** DAX syntax from memory, unverified: learn.microsoft.com was not reachable from this session (DNS blocked), so no Microsoft Learn page was fetched.
**Edge cases:** Someone who joined and left inside the period counts as a leaver but is in neither opening nor closing, so the average slightly understates their effect. Zero average headcount returns blank. Exit on the very first day: counted as a leaver.
**Likely follow-ups:** 1) *Voluntary vs involuntary?* Add an ExitType filter inside both measures. 2) *Annualised?* Multiply a monthly rate by 12, or use the yearly window.
**Common mistakes:** Dividing by closing headcount only; counting rows with blank ExitDate as leavers; leaving an active relationship on ExitDate so the date filter silently trims the Employees rows.

### Q20 ⭐⭐ 🟡 Write a DAX measure for headcount at the end of each month from joining and exit dates.
**Asked at:** commonly asked (no company-specific report found); gap-fill HR question.
**What the interviewer is checking:** Can you build a point-in-time (snapshot) count from start and end dates, with no pre-made headcount column?
**Say this in the interview:** "Headcount at month end is everyone who joined on or before that date and had not left by it. I take the last date in the current month with MAX of the date table, then count employees where JoinDate is on or before it and ExitDate is blank or after it."
**Explain simply:**
- A **snapshot** measure answers "how many on this exact day", not "how many events happened in the month".
- `MAX ( Dates[Date] )` returns the last date visible in the current row, so in a month row it is the month end.
- The exit rule is "ExitDate > month end": someone who leaves on 30 April is not on payroll at 30 April close. Agree that rule with HR first.
- On a Total or Year row, MAX gives the last day of that period, so the total shows the latest headcount, not a sum (headcount is semi-additive, see Q30).
**Example:** Using the same 10 employees as Q19: end of Jan 7, Feb 8, Mar 8, Apr 7.
**Sample data:** Table `Employees` as in Q19 (EmpID, JoinDate, ExitDate).
**DAX / Steps (not run here):**
```dax
Headcount EOM =
VAR EndD = MAX ( Dates[Date] )
RETURN
    CALCULATE (
        COUNTROWS ( FILTER ( Employees,
            Employees[JoinDate] <= EndD
            && ( ISBLANK ( Employees[ExitDate] ) || Employees[ExitDate] > EndD ) ) ),
        REMOVEFILTERS ( Dates )
    )
```
Put `Dates[MonthName]` on matrix rows and this measure in values.
**Alternative:** Running difference: `joins to date - exits to date`, i.e. `CALCULATE ( COUNT ( Employees[EmpID] ), Employees[JoinDate] <= EndD ) - CALCULATE ( COUNT ( Employees[EmpID] ), Employees[ExitDate] <= EndD )`. Same answer, easier to read, and two Boolean filters are cheaper than FILTER on the table (Q31). COUNT skips blank IDs only, so make sure EmpID is never blank.
**Result (reproduced with pandas, not run in Power BI):** 7, 8, 8, 7, 7, 7 for Jan to Jun 2025 (month ends).
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({
 "EmpID":[1,2,3,4,5,6,7,8,9,10],
 "JoinDate":pd.to_datetime(["2022-03-01","2023-06-15","2021-01-10","2024-02-01","2020-08-20","2023-11-05","2025-02-10","2025-07-01","2019-05-05","2024-09-09"]),
 "ExitDate":pd.to_datetime([None,"2025-04-30",None,"2025-09-15","2025-01-31",None,None,"2025-11-30",None,None])})
for m in pd.date_range("2025-01-31", periods=6, freq="ME"):
    n = ((emp.JoinDate<=m) & (emp.ExitDate.isna() | (emp.ExitDate>m))).sum()
    print(m.date(), n)
```
Output:
```
2025-01-31 7
2025-02-28 8
2025-03-31 8
2025-04-30 7
2025-05-31 7
2025-06-30 7
```
**Version / licensing note:** DAX from memory, unverified (learn.microsoft.com not reachable from this session).
**Edge cases:** Months with no joins or exits still show a value because the date table has every date. Re-hires need one row per employment spell. Future-dated exits are still counted until that date.
**Likely follow-ups:** 1) *Why REMOVEFILTERS(Dates)?* So an active date relationship cannot cut the Employees rows before FILTER runs. 2) *Daily headcount?* Same measure on a date axis.
**Common mistakes:** Counting only joins in the month; using `<=` on ExitDate and counting leavers as present; summing monthly headcounts for a year total.

### Q21 ⭐⭐ 🟡 How do you calculate employee tenure in years with DATEDIFF, and what are its limits?
**Asked at:** Wipro reports DATEDIFF in its DAX questions (research/interview_processes.md; unverified there too); otherwise commonly asked.
**What the interviewer is checking:** Do you know DATEDIFF counts calendar boundaries, so "years" can be wrong for tenure?
**Say this in the interview:** "DATEDIFF ( start, end, YEAR ) gives the number of year boundaries crossed, not completed years. Someone who joined 20 December 2024 shows 1 year on 1 January 2025 after 12 days. For real tenure I subtract one if the anniversary has not happened yet, or divide days by 365.25."
**Explain simply:**
- Syntax: `DATEDIFF ( start_date, end_date, interval )` where interval is YEAR, MONTH, DAY and so on.
- With YEAR it just compares calendar years: 2025 minus 2024 = 1, whatever the month.
- Completed years need an anniversary check; fractional years need days / 365.25.
- If the start is later than the end, DATEDIFF returns an error (from memory, unverified), so guard future join dates.
- `TODAY()` changes daily; in a calculated column it only refreshes when the data refreshes.
**Example:** Asha joined 20 Dec 2024, as of 31 Dec 2025 she has 1 completed year; Ravi joined 15 Jan 2020 and has 5 completed years (5.96 fractional).
**Sample data:** Table `Employees`, as-of date 31 Dec 2025 (stands in for TODAY()).

| Name | JoinDate |
|---|---|
| Asha | 2024-12-20 |
| Ravi | 2020-01-15 |
| Meena | 2021-07-01 |
| Karan | 2023-03-10 |

**DAX / Steps (not run here):**
```dax
Tenure Years (boundaries) = DATEDIFF ( Employees[JoinDate], TODAY (), YEAR )

Tenure Years (completed) =
VAR AsOf = TODAY ()
VAR Raw  = DATEDIFF ( Employees[JoinDate], AsOf, YEAR )
VAR Anniversary = DATE ( YEAR ( AsOf ), MONTH ( Employees[JoinDate] ), DAY ( Employees[JoinDate] ) )
RETURN Raw - IF ( Anniversary > AsOf, 1, 0 )
```
**Alternative:** `DIVIDE ( DATEDIFF ( Employees[JoinDate], TODAY (), DAY ), 365.25 )` for fractional years, or `YEARFRAC ( Employees[JoinDate], TODAY () )`.
**Result (reproduced with pandas, not run in Power BI):** boundary-years 1, 5, 4, 2 vs completed years 1, 5, 4, 2 and fractional 1.03, 5.96, 4.50, 2.81. They agree here only because the as-of date is year-end; on 15 Jan 2025 Asha would show 1 (boundary) vs 0 (completed).
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Name":["Asha","Ravi","Meena","Karan"],
 "JoinDate":pd.to_datetime(["2024-12-20","2020-01-15","2021-07-01","2023-03-10"])})
asof = pd.Timestamp("2025-12-31")   # stands in for TODAY() so the result is repeatable
emp["YearsDATEDIFF"] = asof.year - emp.JoinDate.dt.year   # DATEDIFF(...,YEAR) counts calendar-year boundaries crossed
emp["Days"] = (asof - emp.JoinDate).dt.days
emp["YearsDays365_25"] = (emp.Days/365.25).round(2)
# completed years only
emp["CompletedYears"] = emp.apply(lambda r: asof.year-r.JoinDate.year-((asof.month,asof.day)<(r.JoinDate.month,r.JoinDate.day)),axis=1)
print(emp.assign(JoinDate=emp.JoinDate.dt.date).to_string(index=False))
```
Output:
```
 Name   JoinDate  YearsDATEDIFF  Days  YearsDays365_25  CompletedYears
 Asha 2024-12-20              1   376             1.03               1
 Ravi 2020-01-15              5  2177             5.96               5
Meena 2021-07-01              4  1644             4.50               4
Karan 2023-03-10              2  1027             2.81               2
```
**Version / licensing note:** DAX from memory, unverified (learn.microsoft.com not reachable from this session).
**Edge cases:** Blank JoinDate; exited employees need the ExitDate instead of TODAY (`COALESCE ( ExitDate, TODAY () )`); 29 Feb joiners; TODAY depends on the service server time zone (from memory).
**Likely follow-ups:** 1) *Average tenure?* `AVERAGEX ( Employees, [completed years logic] )` over active staff. 2) *Months?* Same boundary caveat with MONTH.
**Common mistakes:** Treating DATEDIFF YEAR as completed years; forgetting exited staff; subtracting dates and reading the result as years.

### Q22 ⭐⭐ 🟡 What is USERELATIONSHIP, and how would you use it with hire date and exit date in one date table?
**Asked at:** commonly asked (Weekday 2026 prep list names USERELATIONSHIP; no company report).
**What the interviewer is checking:** Do you know a model has only one active relationship between two tables and how to switch to another inside one measure?
**Say this in the interview:** "Between Dates and Employees I keep JoinDate as the active relationship and ExitDate as inactive. When I need leavers by month, I wrap the measure in CALCULATE with USERELATIONSHIP ( Dates[Date], Employees[ExitDate] ), which turns that inactive relationship on for that measure only."
**Explain simply:**
- Two tables can have many relationships, but only one is **active** (solid line). The others are **inactive** (dashed line).
- `USERELATIONSHIP ( column1, column2 )` activates one inactive relationship for the duration of that CALCULATE.
- One date table, many roles: hire date, exit date, offer date. No need to copy the date table.
- Dates go to the matrix rows once; each measure picks its own date.
- Rows with blank ExitDate never match a date, so they drop out of the leaver count automatically.
**Example:** Month rows Jan to Dec 2025. Hires uses the active JoinDate link, Leavers uses ExitDate.
**Sample data:** Table `Employees` as in Q19. Relationships: Dates[Date] to Employees[JoinDate] active; Dates[Date] to Employees[ExitDate] inactive.
**DAX / Steps (not run here):**
```dax
Hires = COUNTROWS ( Employees )

Leavers =
CALCULATE (
    COUNTROWS ( Employees ),
    USERELATIONSHIP ( Dates[Date], Employees[ExitDate] )
)
```
Click-path: Model view > drag Dates[Date] onto Employees[ExitDate] > double-click the dashed line > untick "Make this relationship active".
**Alternative:** Skip the second relationship and filter by columns: `CALCULATE ( COUNTROWS ( Employees ), FILTER ( Employees, Employees[ExitDate] >= MIN ( Dates[Date] ) && Employees[ExitDate] <= MAX ( Dates[Date] ) ), REMOVEFILTERS ( Dates ) )`. Works, but slower and does not group by month on the axis.
**Result (reproduced with pandas, not run in Power BI):** hires Feb 1, Jul 1; leavers Jan 1, Apr 1, Sep 1, Nov 1 (other months 0 or blank).
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({
 "EmpID":[1,2,3,4,5,6,7,8,9,10],
 "JoinDate":pd.to_datetime(["2022-03-01","2023-06-15","2021-01-10","2024-02-01","2020-08-20","2023-11-05","2025-02-10","2025-07-01","2019-05-05","2024-09-09"]),
 "ExitDate":pd.to_datetime([None,"2025-04-30",None,"2025-09-15","2025-01-31",None,None,"2025-11-30",None,None])})
hires = emp[emp.JoinDate.dt.year==2025].groupby(emp.JoinDate.dt.to_period("M")).size()
leav  = emp[emp.ExitDate.dt.year==2025].groupby(emp.ExitDate.dt.to_period("M")).size()
print(pd.DataFrame({"Hires":hires,"Leavers":leav}).fillna(0).astype(int))
```
Output:
```
         Hires  Leavers
2025-01      0        1
2025-02      1        0
2025-04      0        1
2025-07      1        0
2025-09      0        1
2025-11      0        1
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com not reachable): inactive relationships and USERELATIONSHIP exist in Power BI Desktop and Service models; it cannot be used with relationships that RLS depends on in the same query (recalled caveat, verify).
**Edge cases:** Months with no hires show blank, not 0 (add `+ 0` if the report needs zero).
**Likely follow-ups:** 1) *Why not two date tables?* Doubles model size and breaks time intelligence consistency. 2) *Can a slicer on Dates filter ExitDate?* Only inside measures that activate it.
**Common mistakes:** Forgetting CALCULATE; expecting the visual axis to change relationship; leaving both relationships active (Power BI refuses, one stays inactive).

### Q23 ⭐⭐ 🟡 Why does the Total row in a matrix not equal the sum of the rows shown, and how do you fix it?
**Asked at:** commonly asked (PracHub 2026 snippet lists non-additive totals; no company report).
**What the interviewer is checking:** Do you understand that a measure is calculated again at the total level, not added from the rows?
**Say this in the interview:** "A Total row is not a sum of the rows. DAX re-runs the measure with the filter removed. For a ratio like attrition, the total is total leavers divided by total headcount, which is correct, not the sum of percentages. If the business wants something else I use SUMX over VALUES to build the total deliberately."
**Explain simply:**
- At the Total row there is no Department filter, so the measure sees all rows at once.
- Ratios, averages, distinct counts and rankings are **non-additive**: the whole is not the sum of the parts.
- A distinct count of employees can even be smaller than the sum of department counts, if someone worked in two.
- Fix only if the total is wrong for the business: iterate the visible rows with `SUMX ( VALUES ( col ), [Measure] )`, or hide the total.
**Example:** IT 14.0%, Sales 14.0%, HR 10.0% add up to 38.0%, but the real overall rate is 22 leavers / 160 average headcount = 13.8%.
**Sample data:** Table `Org` (average headcount and leavers per team row).

| Dept | AvgHeadcount | Leavers |
|---|---|---|
| Sales | 40 | 8 |
| Sales | 60 | 6 |
| IT | 30 | 3 |
| IT | 20 | 4 |
| HR | 10 | 1 |

**DAX / Steps (not run here):**
```dax
Attrition % = DIVIDE ( SUM ( Org[Leavers] ), SUM ( Org[AvgHeadcount] ) )

Attrition % (sum of rows) =
IF (
    ISINSCOPE ( Org[Dept] ),
    [Attrition %],
    SUMX ( VALUES ( Org[Dept] ), [Attrition %] )
)
```
**Alternative:** Average of the row percentages: `AVERAGEX ( VALUES ( Org[Dept] ), [Attrition %] )` gives an unweighted average (12.7%), which treats small and big departments equally. Rarely what you want.
**Result (reproduced with pandas, not run in Power BI):** Rows: HR 10.0%, IT 14.0%, Sales 14.0%. Sum of rows 38.0%; true total 13.8% (22 leavers / 160); simple average of rows 12.7%. The plain measure shows 13.8% in the Total row, which is right.
**Pandas check:**
```python
import pandas as pd
df = pd.DataFrame({"Dept":["Sales","Sales","IT","IT","HR"],
 "AvgHeadcount":[40,60,30,20,10],"Leavers":[8,6,3,4,1]})
g = df.groupby("Dept")[["Leavers","AvgHeadcount"]].sum()
g["Attrition %"] = (g.Leavers/g.AvgHeadcount*100).round(1)
print(g)
print("Sum of row %:", g["Attrition %"].sum())
print("Real total % :", round(g.Leavers.sum()/g.AvgHeadcount.sum()*100,1))
print("Average of row %:", round(g["Attrition %"].mean(),1))
```
Output:
```
       Leavers  AvgHeadcount  Attrition %
Dept                                     
HR           1            10         10.0
IT           7            50         14.0
Sales       14           100         14.0
Sum of row %: 38.0
Real total % : 13.8
Average of row %: 12.7
```
**Version / licensing note:** DAX behaviour from memory, unverified (learn.microsoft.com not reachable).
**Edge cases:** Filters applied by a slicer change what the total covers. A measure using SELECTEDVALUE returns blank at the total. Matrix subtotals follow the same logic at each level.
**Likely follow-ups:** 1) *Why does my sum of an average look wrong?* Averages need weights. 2) *How to hide totals?* Format pane > Row subtotals / Column grand total off.
**Common mistakes:** Assuming Total = sum of rows; "fixing" a correct weighted total with SUMX; using AVERAGE of a percentage column.

### Q24 ⭐⭐ 🟡 How do you make TOTALYTD follow an Indian financial year that ends on 31 March?
**Asked at:** commonly asked (no company-specific report found); gap-fill question; behaviour of the year_end_date argument was checked on Microsoft Learn by the Wave A sources file (accessed 2026-10-24); not re-fetched here.
**What the interviewer is checking:** Do you know TOTALYTD has an optional year-end argument for non-calendar years?
**Say this in the interview:** "TOTALYTD takes an optional third argument, the year-end date as text. For an Indian financial year running April to March I pass \"3/31\", so the running total restarts every 1 April."
**Explain simply:**
- **YTD** means year to date: the running total from the start of the year to the current date.
- Default year end is 31 December. Pass `"3/31"` (month/day, year part ignored) to start the year on 1 April.
- The date column must come from a proper marked date table.
- India's tax and company financial year is 1 April to 31 March, so FY2025-26 YTD at 30 June 2025 is April + May + June only.
**Example:** Jan to Jun 2025 sales 100, 120, 90, 110, 130, 150. Calendar YTD at 30 June = 700; Indian FY YTD at 30 June = 110 + 130 + 150 = 390.
**Sample data:** Table `Sales` (monthly totals).

| Month end | Sales |
|---|---|
| 2025-01-31 | 100 |
| 2025-02-28 | 120 |
| 2025-03-31 | 90 |
| 2025-04-30 | 110 |
| 2025-05-31 | 130 |
| 2025-06-30 | 150 |

**DAX / Steps (not run here):**
```dax
FY YTD Sales = TOTALYTD ( [Total Sales], Dates[Date], "3/31" )
```
**Alternative:** `CALCULATE ( [Total Sales], DATESYTD ( Dates[Date], "3/31" ) )`, or add a FiscalYear column to the date table (`IF ( MONTH ( [Date] ) >= 4, YEAR ( [Date] ) + 1, YEAR ( [Date] ) )`) and filter on it.
**Result (reproduced with pandas, not run in Power BI):** FY YTD: Jan 100, Feb 220, Mar 310, Apr 110, May 240, Jun 390 (calendar YTD would be 100, 220, 310, 420, 550, 700).
**Pandas check:**
```python
import pandas as pd
s = pd.DataFrame({"Month":pd.to_datetime(["2025-01-31","2025-02-28","2025-03-31","2025-04-30","2025-05-31","2025-06-30"]),
 "Sales":[100,120,90,110,130,150]})
def fy_ytd(d):
    fy_start = pd.Timestamp(d.year if d.month>=4 else d.year-1, 4, 1)
    return s[(s.Month>=fy_start)&(s.Month<=d)].Sales.sum()
def cal_ytd(d): return s[(s.Month.dt.year==d.year)&(s.Month<=d)].Sales.sum()
for d in s.Month: print(d.date(), "calendar YTD", cal_ytd(d), "FY YTD (Apr-Mar)", fy_ytd(d))
```
Output:
```
2025-01-31 calendar YTD 100 FY YTD (Apr-Mar) 100
2025-02-28 calendar YTD 220 FY YTD (Apr-Mar) 220
2025-03-31 calendar YTD 310 FY YTD (Apr-Mar) 310
2025-04-30 calendar YTD 420 FY YTD (Apr-Mar) 110
2025-05-31 calendar YTD 550 FY YTD (Apr-Mar) 240
2025-06-30 calendar YTD 700 FY YTD (Apr-Mar) 390
```
**Version / licensing note:** Per the sources file, Microsoft Learn says year_end_date is an optional string, "month/day" recommended, year ignored, default 31 December, and is not allowed with calendar-based time intelligence (from the sources file, not re-fetched here).
**Edge cases:** Format "3/31" is locale-safe; "31-Mar" may not be. The Jan to Mar rows belong to the previous FY, so a YTD there includes the earlier April months (not shown in this half-year sample).
**Likely follow-ups:** 1) *Prior year FY YTD?* Wrap with `SAMEPERIODLASTYEAR`. 2) *Label as FY25-26?* Build it in the date table.
**Common mistakes:** Passing a real date instead of text; forgetting the sample shows only half a year; using calendar year columns on the axis and thinking YTD is wrong.

### Q25 ⭐⭐ 🟡 What does EARLIER do in a calculated column, and how can variables replace it?
**Asked at:** commonly asked (no company-specific report found); gap-fill question; EARLIER description from the Microsoft Learn check recorded in the sources file (2026-10-24).
**What the interviewer is checking:** Do you understand row context and how to read an old-style DAX pattern?
**Say this in the interview:** "EARLIER lets an inner calculation reach back to the outer row of a calculated column. Today I would store the outer row's values in variables instead, which is easier to read and does the same job."
**Explain simply:**
- A **calculated column** is evaluated row by row; the **row context** is "the current row".
- Inside FILTER, a new row context starts, so plain `Employees[Salary]` means the inner row. EARLIER reaches the outer row.
- A **variable** (`VAR`) saves a value before the inner loop starts, so there is nothing to reach back for.
- The sources file notes Learn says EARLIER is mostly for calculated columns and can be slow.
**Example:** Rank each employee's salary within their department.
**Sample data:** Table `Employees`.

| Name | Dept | Salary |
|---|---|---|
| Asha | IT | 90 |
| Ravi | IT | 80 |
| Meena | IT | 80 |
| Karan | HR | 50 |
| Neha | HR | 70 |
| Ola | HR | 60 |

**DAX / Steps (not run here):**
```dax
Rank in Dept (EARLIER) =
COUNTROWS (
    FILTER ( Employees,
        Employees[Dept] = EARLIER ( Employees[Dept] )
        && Employees[Salary] > EARLIER ( Employees[Salary] ) )
) + 1

Rank in Dept (VAR) =
VAR d = Employees[Dept]
VAR s = Employees[Salary]
RETURN
    COUNTROWS ( FILTER ( Employees, Employees[Dept] = d && Employees[Salary] > s ) ) + 1
```
**Alternative:** A measure with `RANKX ( ALLSELECTED ( Employees ), [Salary], , DESC )` per department (see Q16 and Q17).
**Result (reproduced with pandas, not run in Power BI):** Asha 1, Ravi 2, Meena 2 (tie), Karan 3, Neha 1, Ola 2.
**Pandas check:**
```python
import pandas as pd
e = pd.DataFrame({"Name":["Asha","Ravi","Meena","Karan","Neha","Ola"],
 "Dept":["IT","IT","IT","HR","HR","HR"],"Salary":[90,80,80,50,70,60]})
e["Rank"] = e.groupby("Dept").Salary.rank(method="min",ascending=False).astype(int)
# literal translation of the DAX: count rows in same dept with higher salary, plus 1
e["Rank_check"] = e.apply(lambda r: ((e.Dept==r.Dept)&(e.Salary>r.Salary)).sum()+1, axis=1)
print(e)
```
Output:
```
    Name Dept  Salary  Rank  Rank_check
0   Asha   IT      90     1           1
1   Ravi   IT      80     2           2
2  Meena   IT      80     2           2
3  Karan   HR      50     3           3
4   Neha   HR      70     1           1
5    Ola   HR      60     2           2
```
**Version / licensing note:** Calculated columns work in Desktop and are stored in the model; details from the sources file only, not re-fetched here.
**Edge cases:** Ties get the same rank and the next rank is skipped (Meena and Ravi are both 2). EARLIER (not EARLIEST) is the one used in practice. Calculated columns are stored in memory, so large tables grow.
**Likely follow-ups:** 1) *Why not a measure?* A column is fixed per row; a measure reacts to slicers. 2) *EARLIEST?* Reaches the very first outer row context; rarely needed.
**Common mistakes:** Using EARLIER outside a row context (error); comparing the wrong column; forgetting the +1.

### Q26 ⭐⭐ 🟡 Write a measure for the average monthly sales in a selected year (average of the monthly totals, not of the order rows).
**Asked at:** commonly asked (no company-specific report found); gap-fill question.
**What the interviewer is checking:** Can you average a measure over a list of months, instead of averaging raw rows?
**Say this in the interview:** "I use AVERAGEX over the distinct months in the selected year and evaluate the total-sales measure for each month. That averages the monthly totals. AVERAGE on the Amount column would average order rows, which gives a very different number."
**Explain simply:**
- `AVERAGEX ( table, expression )` goes through each row of `table`, evaluates the expression, then averages the results.
- The table here is the list of months: `VALUES ( Dates[MonthStart] )`, the months visible in the year filter.
- The expression is the [Total Sales] measure, which sums sales for each month (a measure inside an iterator re-evaluates for each row: this is called **context transition**).
- Months with no sales return blank and AVERAGEX skips blanks.
**Example:** Orders in Jan, Feb, Apr, May 2025 give monthly totals 400, 200, 600, 250: the average of monthly totals is 362.5 across four months.
**Sample data:** Table `Orders` (2025).

| OrderDate | Amount |
|---|---|
| 2025-01-05 | 100 |
| 2025-01-20 | 300 |
| 2025-02-10 | 200 |
| 2025-04-02 | 150 |
| 2025-04-15 | 150 |
| 2025-04-28 | 300 |
| 2025-05-09 | 250 |

**DAX / Steps (not run here):**
```dax
Total Sales = SUM ( Orders[Amount] )

Avg Monthly Sales = AVERAGEX ( VALUES ( Dates[MonthStart] ), [Total Sales] )

Avg Monthly Sales (zero months) = AVERAGEX ( VALUES ( Dates[MonthStart] ), [Total Sales] + 0 )
```
**Alternative:** `DIVIDE ( [Total Sales], DISTINCTCOUNT ( Dates[MonthStart] ) )` (this one divides by all months in the year in the filter, so it behaves like the zero-months version), or, for active months only, `DIVIDE ( [Total Sales], COUNTROWS ( FILTER ( VALUES ( Dates[MonthStart] ), [Total Sales] > 0 ) ) )` (reasoned, not run).
**Result (reproduced with pandas, not run in Power BI):** Monthly totals Jan 400, Feb 200, Apr 600, May 250. Average of order rows 207.14; average of monthly totals 362.50 (blank months ignored); average over all 12 months with blank = 0 is 120.83.
**Pandas check:**
```python
import pandas as pd
o = pd.DataFrame({"OrderDate":pd.to_datetime(["2025-01-05","2025-01-20","2025-02-10","2025-04-02","2025-04-15","2025-04-28","2025-05-09"]),
 "Amount":[100,300,200,150,150,300,250]})
m = o.groupby(o.OrderDate.dt.month).Amount.sum().reindex(range(1,13))   # calendar has 12 months; Mar, Jun-Dec have no sales
print(m.dropna())
print("avg of order rows:", round(o.Amount.mean(),2))
print("avg of monthly totals (blank months ignored):", round(m.mean(),2))
print("avg over all 12 months (blank = 0):", round(m.fillna(0).mean(),2))
```
Output:
```
OrderDate
1    400.0
2    200.0
4    600.0
5    250.0
Name: Amount, dtype: float64
avg of order rows: 207.14
avg of monthly totals (blank months ignored): 362.5
avg over all 12 months (blank = 0): 120.83
```
**Version / licensing note:** DAX from memory, unverified (learn.microsoft.com not reachable).
**Edge cases:** Whether empty months count is a business decision: say so. If the date table covers only months with data, the two versions agree. The current, partial month drags the average down.
**Likely follow-ups:** 1) *Why not AVERAGE?* It averages rows. 2) *Average per day?* Iterate `VALUES ( Dates[Date] )`.
**Common mistakes:** `AVERAGE ( Orders[Amount] )`; iterating the Orders table itself; forgetting the date table should hold all dates.

### Q27 ⭐⭐ 🔴 Your YoY or YTD measure returns blank or wrong numbers: how do you debug it?
**Asked at:** commonly asked (Fabric community threads on SAMEPERIODLASTYEAR and DATESYTD pitfalls are anecdotal; no company report).
**What the interviewer is checking:** Do you debug in a methodical order, rather than guessing?
**Say this in the interview:** "I split the measure: show current value and prior-year value as separate measures in a table. If prior-year is blank, I check the date table: marked as date table, continuous, no gaps, relationship active, and the visual using Dates[Date] not the fact table's date. Then I check for partial-period comparisons."
**Explain simply:**
- **Date table rules:** one row per day, no gaps, covers all fact dates and the prior year, one date column marked as the date table.
- Time functions only work on the date table column; using the fact table's own date column breaks them.
- Compare like with like: a partial current year vs a full prior year gives nonsense.
- First year of data has no prior year, so blank is correct there.
- Divide with DIVIDE so a zero or blank denominator gives blank, not an error.
**Example:** Sales 2023 blank, 2024 1,200, 2025 1,500: YoY for 2025 = 25%. 2025 YTD to March (310) vs 2024 full year (1,200) gives -74.2%; vs the same three months (290) it is +6.9%.
**Sample data:** Table `YearlySales` (year totals) and `Q1` (months) as listed in the example.
**DAX / Steps (not run here):**
1. Add two plain measures: `[Total Sales]` and `PY Sales = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( Dates[Date] ) )` and put them in a table by month.
2. Model view: is Dates marked as date table (Table tools > Mark as date table)? Is the relationship Dates[Date] to Sales[OrderDate] active, one-to-many, single direction?
3. Is the axis field Dates[Date] (or its Year/Month), not Sales[OrderDate]?
4. Check for gaps: `COUNTROWS ( Dates )` vs expected days; does the date table reach the end of the sales data and the prior year start?
5. Check for time stamps in OrderDate (a date-time breaks the match); trim to a date.
6. Test the prior-year value for one row by hand; then wrap in DIVIDE.
```dax
YoY % = VAR cur = [Total Sales] VAR py = [PY Sales] RETURN DIVIDE ( cur - py, py )
```
**Alternative:** `DATEADD ( Dates[Date], -1, YEAR )` instead of SAMEPERIODLASTYEAR; or DAX query view / DAX Studio to see the table each part returns.
**Result (reproduced with pandas, not run in Power BI):** 2023 YoY blank (no prior year); 2024 blank (2023 has no data); 2025 +25.0%. Partial-year trap: -74.2% against the full prior year, +6.9% against the same three months.
**Pandas check:**
```python
import pandas as pd
y = pd.Series({2023:None,2024:1200,2025:1500},dtype="float")
print(pd.DataFrame({"Sales":y,"PY":y.shift(1),"YoY %":((y/y.shift(1)-1)*100).round(1)}))
q = pd.DataFrame({"Month":["Jan","Feb","Mar"],"2025":[100,120,90],"2024":[80,100,110]})
print("2025 YTD to Mar:", q["2025"].sum(), " 2024 same period:", q["2024"].sum(), " 2024 full year: 1200")
print("YoY vs same period %:", round((310/290-1)*100,1), " vs full-year (wrong):", round((310/1200-1)*100,1))
```
Output:
```
       Sales      PY  YoY %
2023     NaN     NaN    NaN
2024  1200.0     NaN    NaN
2025  1500.0  1200.0   25.0
2025 YTD to Mar: 310  2024 same period: 290  2024 full year: 1200
YoY vs same period %: 6.9  vs full-year (wrong): -74.2
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com not reachable). Whether a date table must be marked depends on the model; recalled behaviour, verify.
**Edge cases:** YTD in a month with no data yet (future dates) can show prior-year values only; filter to dates <= today. Fiscal years need the year-end argument (Q24). Leap day: SAMEPERIODLASTYEAR handles it.
**Likely follow-ups:** 1) *Why does it work in a card but not in a matrix?* Different filter context. 2) *Blank vs 0?* Blank is hidden in visuals, 0 is shown.
**Common mistakes:** Using the fact table's date column; not marking the date table; comparing partial year to full year; hiding errors with IFERROR.

### Q28 ⭐ 🟡 What does KEEPFILTERS do, and when would you use it?
**Asked at:** commonly asked (PracHub 2026 snippet lists KEEPFILTERS; no company report).
**What the interviewer is checking:** Do you know that a CALCULATE filter normally replaces the filter on the same column and KEEPFILTERS makes it intersect instead?
**Say this in the interview:** "Normally a filter in CALCULATE overwrites an existing filter on that column. KEEPFILTERS says: do not overwrite, combine both. So in the South row, North-only sales without KEEPFILTERS wrongly show North's value; with it they correctly show blank."
**Explain simply:**
- **Filter context** = the filters currently applied by rows, slicers and filters on the page.
- CALCULATE's `Region = "North"` replaces whatever Region filter the row had.
- KEEPFILTERS keeps the row's filter, so the result is rows that are both North and in the current row.
- Use it when a measure should respect the slicer or row, such as a "high value" or "selected list" measure.
**Example:** A "North sales" measure in a Region table: without KEEPFILTERS every row shows 150; with it only the North row shows 150.
**Sample data:** Table `Sales`.

| Region | Amount |
|---|---|
| North | 100 |
| North | 50 |
| South | 80 |
| South | 70 |
| East | 60 |

**DAX / Steps (not run here):**
```dax
North Sales (overrides) = CALCULATE ( SUM ( Sales[Amount] ), Sales[Region] = "North" )

North Sales (respects row) =
CALCULATE ( SUM ( Sales[Amount] ), KEEPFILTERS ( Sales[Region] = "North" ) )
```
**Alternative:** `CALCULATE ( SUM ( Sales[Amount] ), FILTER ( VALUES ( Sales[Region] ), Sales[Region] = "North" ) )` also intersects with the current selection (reasoned, not run).
**Result (reproduced with pandas, not run in Power BI):** North 150/150, South 150 vs blank, East 150 vs blank; Total row 150 either way.
**Pandas check:**
```python
import pandas as pd
s = pd.DataFrame({"Region":["North","North","South","South","East"],"Amount":[100,50,80,70,60]})
by = s.groupby("Region").Amount.sum()
no_keep = {r: s[s.Region=="North"].Amount.sum() for r in by.index}                     # filter overwrites the row's Region
keep = {r: s[(s.Region==r)&(s.Region=="North")].Amount.sum() or None for r in by.index} # filter intersects with the row's Region
print(pd.DataFrame({"Plain sales":by,"No KEEPFILTERS":pd.Series(no_keep),"With KEEPFILTERS":pd.Series(keep)}))
print("Total row: plain",s.Amount.sum(),"| no keep",150,"| keep",150)
```
Output:
```
       Plain sales  No KEEPFILTERS  With KEEPFILTERS
East            60             150               NaN
North          150             150             150.0
South          150             150               NaN
Total row: plain 360 | no keep 150 | keep 150
```
**Version / licensing note:** Same in all Power BI / Analysis Services models (from memory, unverified: learn.microsoft.com not reachable).
**Edge cases:** On the Total row there is no Region filter, so both return the same. KEEPFILTERS also matters in iterators and with TREATAS/IN lists.
**Likely follow-ups:** 1) *Does it work on tables?* Yes, it wraps a filter argument. 2) *Row-level security?* RLS filters are kept anyway.
**Common mistakes:** Expecting a slicer to limit a CALCULATE that sets the same column; wrapping the whole CALCULATE instead of the filter argument.

### Q29 ⭐ 🟡 Why do many experts prefer REMOVEFILTERS with VALUES over ALLEXCEPT?
**Asked at:** ALL vs ALLEXCEPT is named in research/interview_processes.md; this variant is a differentiator from the SQLBI article in the sources file (summary only).
**What the interviewer is checking:** Do you know modern DAX style and why it reads better?
**Say this in the interview:** "ALLEXCEPT says 'remove all filters except these columns'. REMOVEFILTERS on the table plus VALUES of the column I want to keep says the same thing in two clear steps, and it is easier to extend, for example to keep a filter coming from another table. Results are the same here; the preference is clarity and flexibility."
**Explain simply:**
- `ALLEXCEPT ( Employees, Employees[Dept] )` clears every filter on Employees except Dept.
- `REMOVEFILTERS ( Employees )` clears all; `VALUES ( Employees[Dept] )` puts the current Dept selection back. Together the same effect.
- REMOVEFILTERS is a modifier only (it cannot return a table), which makes intent clear; ALL can be both.
- Premise note: "many experts prefer" is a style view from the SQLBI summary, not a rule; both are correct.
**Example:** Gender share of salary within each department: IT females 30 of 100 = 30.0%.
**Sample data:** Table `Employees`.

| Dept | Gender | Salary |
|---|---|---|
| IT | F | 10 |
| IT | F | 20 |
| IT | M | 30 |
| IT | M | 40 |
| HR | F | 50 |
| HR | M | 60 |

**DAX / Steps (not run here):**
```dax
Share of Dept (ALLEXCEPT) =
DIVIDE ( SUM ( Employees[Salary] ),
    CALCULATE ( SUM ( Employees[Salary] ), ALLEXCEPT ( Employees, Employees[Dept] ) ) )

Share of Dept (REMOVEFILTERS) =
DIVIDE ( SUM ( Employees[Salary] ),
    CALCULATE ( SUM ( Employees[Salary] ), REMOVEFILTERS ( Employees ), VALUES ( Employees[Dept] ) ) )
```
**Alternative:** `REMOVEFILTERS ( Employees[Gender] )` only, which is the simplest when you know exactly which column to clear.
**Result (reproduced with pandas, not run in Power BI):** HR F 45.5%, HR M 54.5%, IT F 30.0%, IT M 70.0%.
**Pandas check:**
```python
import pandas as pd
e = pd.DataFrame({"Dept":["IT"]*4+["HR"]*2,"Gender":["F","F","M","M","F","M"],"Salary":[10,20,30,40,50,60]})
g = e.groupby(["Dept","Gender"]).Salary.sum().reset_index()
g["DeptTotal"] = g.groupby("Dept").Salary.transform("sum")      # what both ALLEXCEPT(Dept) and REMOVEFILTERS+VALUES(Dept) give
g["Share %"] = (g.Salary/g.DeptTotal*100).round(1)
print(g)
```
Output:
```
  Dept Gender  Salary  DeptTotal  Share %
0   HR      F      50        110     45.5
1   HR      M      60        110     54.5
2   IT      F      30        100     30.0
3   IT      M      70        100     70.0
```
**Version / licensing note:** REMOVEFILTERS needs a reasonably current Power BI Desktop (a newer function than ALL, from memory, unverified); Microsoft Learn not reachable from this session.
**Edge cases:** If one Dept is picked in a slicer, both keep it. Filters from related tables can behave differently from direct column filters; test when dimensions are involved.
**Likely follow-ups:** 1) *ALL vs REMOVEFILTERS?* Q8. 2) *ALLSELECTED?* Q7.
**Common mistakes:** Calling one "wrong"; forgetting VALUES, which makes the denominator the grand total.

### Q30 ⭐ 🟡 How do you write a closing-balance (semi-additive) measure using LASTDATE or LASTNONBLANK?
**Asked at:** commonly asked (no company-specific report found); gap-fill question.
**What the interviewer is checking:** Do you know balances (stock, headcount, leave) must not be summed over time, and how to take the last value?
**Say this in the interview:** "A balance is semi-additive: add across employees but not across months. For a quarter I take the balance on the last date that has data. LASTDATE returns the last calendar date and is blank if there is no row that day, so I use LASTNONBLANK, which finds the last date that actually has data."
**Explain simply:**
- **Semi-additive**: summable across some dimensions (people), not across time.
- `LASTDATE ( Dates[Date] )` = last date in the current filter, found in the date table.
- `LASTNONBLANK ( column, expression )` = last value of the column where the expression is not blank.
- If the snapshot did not run on 31 March, LASTDATE gives blank.
**Example:** Leave balance snapshots on 31 Jan, 28 Feb and 30 Mar (31 Mar missing).
**Sample data:** Table `Balances`.

| Date | Employee | LeaveBalance |
|---|---|---|
| 2025-01-31 | Asha | 12 |
| 2025-01-31 | Ravi | 8 |
| 2025-02-28 | Asha | 10 |
| 2025-02-28 | Ravi | 9 |
| 2025-03-30 | Asha | 8 |
| 2025-03-30 | Ravi | 7 |

**DAX / Steps (not run here):**
```dax
Closing Balance (LASTDATE) =
CALCULATE ( SUM ( Balances[LeaveBalance] ), LASTDATE ( Dates[Date] ) )

Closing Balance (LASTNONBLANK) =
CALCULATE (
    SUM ( Balances[LeaveBalance] ),
    LASTNONBLANK ( Dates[Date], CALCULATE ( COUNTROWS ( Balances ) ) )
)
```
**Alternative:** `VAR LastD = MAX ( Balances[Date] ) RETURN CALCULATE ( SUM ( Balances[LeaveBalance] ), Balances[Date] = LastD )`.
**Result (reproduced with pandas, not run in Power BI):** Jan 20/20, Feb 19/19, Mar blank (LASTDATE) vs 15 on 30 Mar (LASTNONBLANK).
**Pandas check:**
```python
import pandas as pd
b = pd.DataFrame({"Date":pd.to_datetime(["2025-01-31","2025-01-31","2025-02-28","2025-02-28","2025-03-30","2025-03-30"]),
 "Employee":["Asha","Ravi"]*3,"LeaveBalance":[12,8,10,9,8,7]})
for q,(a,z) in {"Jan":("2025-01-01","2025-01-31"),"Feb":("2025-02-01","2025-02-28"),"Mar":("2025-03-01","2025-03-31")}.items():
    w = b[(b.Date>=a)&(b.Date<=z)]
    last_cal = pd.Timestamp(z)                      # LASTDATE of the calendar period
    on_last = w[w.Date==last_cal].LeaveBalance.sum()
    last_nb = w.Date.max()                           # LASTNONBLANK: last date having data
    print(q,"LASTDATE ->", on_last if (w.Date==last_cal).any() else "blank","| LASTNONBLANK ->", w[w.Date==last_nb].LeaveBalance.sum(), "on", last_nb.date())
```
Output:
```
Jan LASTDATE -> 20 | LASTNONBLANK -> 20 on 2025-01-31
Feb LASTDATE -> 19 | LASTNONBLANK -> 19 on 2025-02-28
Mar LASTDATE -> blank | LASTNONBLANK -> 15 on 2025-03-30
```
**Version / licensing note:** DAX from memory, unverified (learn.microsoft.com not reachable).
**Edge cases:** A quarter row with no snapshot at all returns blank. Weekends. Year Total row picks the last date in the year.
**Likely follow-ups:** 1) *Opening balance?* FIRSTNONBLANK. 2) *Why not SUM?* Adds month-ends together.
**Common mistakes:** Summing balances over months; LASTDATE on a fact table column; leaving the CALCULATE out of LASTNONBLANK's expression.

### Q31 ⭐ 🟡 Why is FILTER on a whole table inside CALCULATE slow, and how do you rewrite it?
**Asked at:** commonly asked (no company-specific report found); Deloitte USI optimisation topics appear in research/interview_processes.md but not this question.
**What the interviewer is checking:** Do you know a column filter is cheaper than a whole-table filter, and what changes when you rewrite it?
**Say this in the interview:** "FILTER ( Sales, ... ) walks every row of the table, which is slow and carries all columns. A Boolean filter such as Sales[Amount] > 1000 is turned into a filter on that one column. I rewrite to the Boolean form when the condition is on one column, and I keep FILTER only when the condition needs a measure or several columns."
**Explain simply:**
- FILTER is an **iterator**: it visits each row one by one.
- Passing the whole table means a large temporary table with every column; filtering one column keeps it small.
- Boolean shortcut: `Sales[Amount] > 1000` filters only that column and overrides any existing filter on Amount.
- Not identical in every case: if a slicer already filters Amount, the Boolean overrides it, `FILTER ( Sales, ... )` respects it.
**Example:** Sales on orders above 1,000.
**Sample data:** Table `Sales`.

| Region | Amount |
|---|---|
| North | 500 |
| North | 1500 |
| North | 2500 |
| South | 1200 |
| South | 900 |

**DAX / Steps (not run here):**
```dax
Big Orders (slow) = CALCULATE ( SUM ( Sales[Amount] ), FILTER ( Sales, Sales[Amount] > 1000 ) )

Big Orders (faster) = CALCULATE ( SUM ( Sales[Amount] ), Sales[Amount] > 1000 )
```
**Alternative:** `FILTER ( ALL ( Sales[Amount] ), Sales[Amount] > 1000 )` is what the Boolean form expands to; use `KEEPFILTERS` (Q28) if you want to respect an existing Amount filter.
**Result (reproduced with pandas, not run in Power BI):** With a North filter, both return 4,000 (1,500 + 2,500); all regions 5,200. Speed difference not measured here.
**Pandas check:**
```python
import pandas as pd
s = pd.DataFrame({"Region":["North","North","North","South","South"],"Amount":[500,1500,2500,1200,900]})
sel = s[s.Region=="North"]                   # a Region = North filter from a slicer
print("Big orders (>1000), North:", sel[sel.Amount>1000].Amount.sum())
print("Big orders (>1000), all regions:", s[s.Amount>1000].Amount.sum())
```
Output:
```
Big orders (>1000), North: 4000
Big orders (>1000), all regions: 5200
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com not reachable). The size of the speed gain depends on table size and model; measure it (Q32).
**Edge cases:** A condition that compares two columns or uses a measure needs FILTER; then iterate a small table such as `VALUES ( column )`.
**Likely follow-ups:** 1) *How to measure?* Q32. 2) *Is FILTER bad?* No, only on a large table when avoidable.
**Common mistakes:** FILTER over the fact table out of habit; assuming both forms are always equal.

### Q32 ⭐ 🟡 How do you find and fix a slow DAX measure with Performance Analyzer and DAX Studio?
**Asked at:** Deloitte USI Power BI round includes optimisation (research/interview_processes.md, unverified there); this exact question is a gap-fill.
**What the interviewer is checking:** Can you measure first, then fix, instead of guessing?
**Say this in the interview:** "I record in Performance Analyzer to see which visual is slow and how much time is DAX query versus visual display. I copy the slow query into DAX Studio, run it with Server Timings, and look at storage-engine vs formula-engine time. Then I fix the measure, commonly by replacing FILTER on tables, reducing iterators, and using variables, and compare."
**Explain simply:**
- **Performance Analyzer** is a built-in pane in Desktop that times each visual.
- **DAX Studio** is a free external tool that runs a query and shows timings; it is not made by Microsoft (from memory).
- A slow visual may be slow because of too many visuals, not DAX: check display time as well.
- Fix, then retest with a cold cache.
**Example:** A matrix takes 8 seconds; the DAX query part is 7.5 s. The measure used FILTER over a 5-million-row table; after the rewrite it takes 1.2 s (illustrative numbers, not measured).
**DAX / Steps (not run here):**
1. Desktop: View tab > Performance analyzer > Start recording > Refresh visuals.
2. Expand the slow visual; note "DAX query" vs "Visual display".
3. Click Copy query.
4. DAX Studio: connect to the open model > paste > turn on Server Timings > Run.
5. Check storage-engine queries (many, large) vs formula-engine time.
6. Rewrite the measure, clear the cache, re-run, compare.
**Alternative:** DAX query view in Desktop (from memory, recent builds) to run queries without an external tool; also use VAR to avoid recomputing.
**Result:** Not applicable (process question); no measurement was run here.
**Version / licensing note:** From memory, unverified: Performance analyzer is in Desktop (Windows) and the Service; DAX Studio is Windows-only and free (verify). Microsoft Learn not reachable.
**Edge cases:** First run is slower (cold cache); a model on DirectQuery has source delays; Performance Analyzer times include other visuals running at the same moment.
**Likely follow-ups:** 1) *What if the model is large?* Remove unused columns, reduce cardinality. 2) *Variables?* Compute once and reuse.
**Common mistakes:** Optimising without measuring; testing with a warm cache; blaming DAX for slow visuals.

### Q33 ⭐ 🔴 How would you build time intelligence once for many measures using calculation groups?
**Asked at:** commonly asked as an advanced differentiator (no company-specific report found).
**What the interviewer is checking:** Do you know how to avoid writing YTD, PY and YoY versions of every measure?
**Say this in the interview:** "A calculation group is a set of calculation items, such as Current, YTD and Prior Year, that apply to any measure using SELECTEDMEASURE. I write the time logic once; users pick the item on a slicer or matrix and every measure follows."
**Explain simply:**
- Without it, 10 measures x 4 time views = 40 measures.
- A **calculation item** is a rule like "take the measure and shift it to the year to date". `SELECTEDMEASURE ( )` stands for whichever measure is in the visual.
- Needs a good date table.
- Calculation groups are authored in the model view in Desktop or with Tabular Editor (from memory, unverified).
**Example:** Sales and Orders each get a YTD and a prior-year view automatically.
**Sample data:** Monthly table (2024 Jan to 2025 Mar, shown for 2025 Q1 results).

| Month | Sales | Orders |
|---|---|---|
| 2025-01 | 130 | 13 |
| 2025-02 | 140 | 14 |
| 2025-03 | 150 | 15 |
| (2024 Jan to Mar) | 100, 110, 120 | 10, 11, 12 |

**DAX / Steps (not run here):**
```dax
-- Calculation group "Time Intelligence", items:
Current = SELECTEDMEASURE ( )
YTD     = CALCULATE ( SELECTEDMEASURE ( ), DATESYTD ( Dates[Date] ) )
PY      = CALCULATE ( SELECTEDMEASURE ( ), SAMEPERIODLASTYEAR ( Dates[Date] ) )
YoY %   = DIVIDE ( SELECTEDMEASURE ( ) - CALCULATE ( SELECTEDMEASURE ( ), SAMEPERIODLASTYEAR ( Dates[Date] ) ),
                   CALCULATE ( SELECTEDMEASURE ( ), SAMEPERIODLASTYEAR ( Dates[Date] ) ) )
```
Click-path (from memory): Model view > Home > Calculation group > rename group and column > add items > paste the expressions.
**Alternative:** Write separate measures per view, or build the 2-3 time views as field parameters; fewer measures, less flexible.
**Result (reproduced with pandas, not run in Power BI):** Sales YTD 130, 270, 420; PY 100, 110, 120; Orders YTD 13, 27, 42; PY 10, 11, 12.
**Pandas check:**
```python
import pandas as pd
m = pd.DataFrame({"Month":pd.period_range("2024-01","2025-03",freq="M")})
m["Sales"]=[100,110,120,130,140,150,160,170,180,190,200,210,130,140,150]
m["Orders"]=[10,11,12,13,14,15,16,17,18,19,20,21,13,14,15]
m["Yr"]=m.Month.dt.year
out=m[m.Yr==2025].copy()
for c in ["Sales","Orders"]:
    m[c+" YTD"]=m.groupby("Yr")[c].cumsum()
    m[c+" PY"]=m[c].shift(12)
print(m[m.Yr==2025].drop(columns="Yr").to_string(index=False))
```
Output:
```
  Month  Sales  Orders  Sales YTD  Sales PY  Orders YTD  Orders PY
2025-01    130      13        130     100.0          13       10.0
2025-02    140      14        270     110.0          27       11.0
2025-03    150      15        420     120.0          42       12.0
```
**Version / licensing note:** From memory, unverified (Microsoft Learn not reachable; sources file flagged availability as unverified). Do not claim a licence tier.
**Edge cases:** Creating a calculation group can switch off implicit measures (from memory); YoY % on a count and on a currency measure needs a format string expression; precedence when several groups exist.
**Likely follow-ups:** 1) *Format string?* Use a dynamic format string per item. 2) *Tools?* Tabular Editor.
**Common mistakes:** Using it without a proper date table; forgetting SELECTEDMEASURE; expecting item order to equal slicer order.

### Q34 ⭐ 🔴 What are visual calculations in Power BI, and how do they differ from measures?
**Asked at:** commonly asked as a newer-feature differentiator (no company-specific report found).
**What the interviewer is checking:** Do you know the newer feature and when it is simpler than a measure?
**Say this in the interview:** "Visual calculations are DAX calculations written inside a visual. They work on the data in that visual, such as running sum or moving average, so there is no filter-context fiddling. A measure is stored in the model and works anywhere, a visual calculation only in that visual."
**Explain simply:**
- Created from the visual itself, stored in the visual, not in the model.
- They refer to fields already in the visual, row by row of the visual table.
- Functions like `RUNNINGSUM`, `MOVINGAVERAGE`, `PREVIOUS`, `FIRST` (from memory, unverified).
- A measure is reusable across visuals and available in Q&A and other tools.
- Where it fits: running totals and previous-period comparisons that need quick results.
**Example:** A monthly sales table with a running sum and 3-month average.
**Sample data:** Visual with Month and Sales.

| Month | Sales |
|---|---|
| Jan | 100 |
| Feb | 120 |
| Mar | 90 |
| Apr | 110 |
| May | 130 |

**DAX / Steps (not run here):** Select the visual > Home tab > New calculation (from memory, unverified) > enter:
```dax
Running Sales = RUNNINGSUM ( [Total Sales] )
Moving Avg 3  = MOVINGAVERAGE ( [Total Sales], 3 )
Prev Month    = PREVIOUS ( [Total Sales] )
```
**Alternative:** The measure form of a running total (Q15), reusable in any visual.
**Result (reproduced with pandas, not run in Power BI):** Running sum 100, 220, 310, 420, 550; 3-month moving avg (partial window at start) 100.0, 110.0, 103.3, 106.7, 110.0; previous blank, 100, 120, 90, 110.
**Pandas check:**
```python
import pandas as pd
d = pd.DataFrame({"Month":["Jan","Feb","Mar","Apr","May"],"Sales":[100,120,90,110,130]})
d["RUNNINGSUM"]=d.Sales.cumsum()
d["MOVINGAVERAGE(3)"]=d.Sales.rolling(3,min_periods=1).mean().round(1)
d["PREVIOUS"]=d.Sales.shift(1)
print(d)
```
Output:
```
  Month  Sales  RUNNINGSUM  MOVINGAVERAGE(3)  PREVIOUS
0   Jan    100         100             100.0       NaN
1   Feb    120         220             110.0     100.0
2   Mar     90         310             103.3     120.0
3   Apr    110         420             106.7      90.0
4   May    130         550             110.0     110.0
```
**Version / licensing note:** From memory, unverified: it was introduced as a preview in 2024; check the current status on Microsoft Learn before claiming it is GA (the sources file also marks this unverified; learn.microsoft.com not reachable here).
**Edge cases:** If the field is removed from the visual the calculation breaks; sorting changes the order of calculation; moving-average window at the edges (check behaviour, pandas shown uses partial windows).
**Likely follow-ups:** 1) *Can I use it in another visual?* No; copy it. 2) *Can it reference a column not in the visual?* No (from memory).
**Common mistakes:** Expecting reuse across visuals; confusing with measures or calculated columns.

### Q35 ⭐ 🔴 What does ISINSCOPE do, and how do you use it to show a different calculation at each level of a matrix hierarchy?
**Asked at:** commonly asked as a differentiator (no company-specific report found); function behaviour per the sources file Learn check (2026-10-24), SWITCH(TRUE(), ISINSCOPE(...)) percent-of-parent example.
**What the interviewer is checking:** Can you make one measure behave differently at each level of a matrix?
**Say this in the interview:** "ISINSCOPE returns TRUE when a column is the level currently being shown in the matrix. I wrap SWITCH ( TRUE (), ... ) around it so the team level shows percent of department, the department level shows percent of total, and the grand total shows 100%."
**Explain simply:**
- A matrix with a hierarchy (Dept > Team) drills down. At each level, different columns are "in scope".
- Check the lowest level first, because Dept is also in scope on a Team row.
- Typical uses: percent of parent, hide values at certain levels.
**Example:** IT has 50 people: Data 20 (40%), Web 15 (30%), QA 15 (30%). IT is 83.3% of 60.
**Sample data:** Table `Org`.

| Dept | Team | HC |
|---|---|---|
| IT | Data | 20 |
| IT | Web | 15 |
| IT | QA | 15 |
| HR | Payroll | 6 |
| HR | Hiring | 4 |

**DAX / Steps (not run here):**
```dax
HC = SUM ( Org[HC] )

% of Parent =
SWITCH (
    TRUE (),
    ISINSCOPE ( Org[Team] ), DIVIDE ( [HC], CALCULATE ( [HC], REMOVEFILTERS ( Org[Team] ) ) ),
    ISINSCOPE ( Org[Dept] ), DIVIDE ( [HC], CALCULATE ( [HC], REMOVEFILTERS ( Org[Dept] ) ) ),
    1
)
```
**Alternative:** `HASONEVALUE` (cruder: works on one value, not on levels), or separate measures per visual.
**Result (reproduced with pandas, not run in Power BI):** Team % of dept: Data 40.0, Web 30.0, QA 30.0, Payroll 60.0, Hiring 40.0; Dept % of total: HR 16.7, IT 83.3; Total row 100.
**Pandas check:**
```python
import pandas as pd
o = pd.DataFrame({"Dept":["IT","IT","IT","HR","HR"],"Team":["Data","Web","QA","Payroll","Hiring"],"HC":[20,15,15,6,4]})
tot=o.HC.sum()
dept=o.groupby("Dept").HC.sum()
o["Team % of dept"]=(o.HC/o.Dept.map(dept)*100).round(1)
print(o)
print((dept/tot*100).round(1).rename("Dept % of total"))
print("Total row:",100)
```
Output:
```
  Dept     Team  HC  Team % of dept
0   IT     Data  20            40.0
1   IT      Web  15            30.0
2   IT       QA  15            30.0
3   HR  Payroll   6            60.0
4   HR   Hiring   4            40.0
Dept
HR    16.7
IT    83.3
Name: Dept % of total, dtype: float64
Total row: 100
```
**Version / licensing note:** From the sources file: ISINSCOPE checked on Microsoft Learn on 2026-10-24; not re-fetched. Works in matrix and other visuals with a hierarchy of columns.
**Edge cases:** Order of SWITCH conditions; a flat table with several columns is not "in scope" the same way; the Total row hits the default.
**Likely follow-ups:** 1) *ISINSCOPE vs ISFILTERED?* ISFILTERED asks if a filter exists on the column, ISINSCOPE asks if it is a level in the visual. 2) *Why 1?* The grand total is 100% of itself.
**Common mistakes:** Checking Dept before Team; forgetting the default value.
