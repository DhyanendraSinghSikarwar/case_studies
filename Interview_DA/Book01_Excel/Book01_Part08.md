# Book 1 — Excel | Part 8: Charts and Excel Dashboards 🟡

**Target:** 50 questions | **Actual:** 54 questions
**Scope:** Excel chart types and formatting, combo and special charts, dynamic charts, KPI cards, interactive dashboards with slicers, dashboard design and presentation (Google Sheets and version differences included).

### Q1 ⭐⭐⭐ 🟢 What types of charts are available in Excel, and how do you choose the right one for your data?
**Asked at:** commonly asked (no company-specific report found); "chart types" appears in the ClimbTheLadder "20 Excel Charts Interview Questions" list (undated).
**What the interviewer is checking:** Do you pick a chart by the question you are answering, not by what looks nice?
**Say this in the interview:** "I first decide what the reader needs to see: comparison, trend over time, share of a whole, or relationship between two numbers. Comparison is column or bar, trend is line, share is pie only when there are very few slices, and relationship is scatter."
**Explain simply:**
- Excel's chart families include Column, Line, Pie and doughnut, Bar, Area, XY (scatter) and bubble, Stock, Surface, Radar, Treemap, Sunburst, Histogram and Pareto, Box and whisker, Waterfall, Funnel, Combo and Map (Microsoft Support, "Available chart types in Office").
- Microsoft's own guidance: column compares categories or change over time; bar suits long category names; line shows trends at evenly spaced intervals such as months; pie shows parts of a whole for one series, no negatives, at most seven categories; scatter compares pairs of numbers; bubble adds a third number as bubble size (same page).
- Rule of thumb: one message per chart. If you cannot say the message in one sentence, the chart is wrong.
**Example:** HR leadership asks three things. "Which department is biggest?" (bar, 6 departments). "Is attrition rising?" (line, 12 months). "Does tenure relate to salary?" (scatter, one dot per employee).
**Sample sheet:**

| Question | Data shape | Chart |
|---|---|---|
| Headcount by department | 6 categories, 1 number | Bar (sorted) |
| Monthly attrition % | 12 months, 1 number | Line |
| Share of hires by source | 4 sources, sums to 100% | Pie (or bar) |
| Tenure vs salary | 2 numbers per person | Scatter |

**Formula / Steps:** 1. Select the data including headers. 2. Insert tab > Charts group > Recommended Charts (Microsoft Support, "Create a chart from start to finish"). 3. Preview each option, use the All Charts tab for the full list, click OK. Chart building is not run here (charts cannot run in this environment); only the numbers behind charts were checked.
**Alternative:** Pick the chart by message type first, then check that Excel's Recommended Charts agrees.
**Result:** Not run here (chart choice). The numbers in later answers behind each chart were recalculated.
**Version note:** Column, bar, line, pie, scatter, bubble are in every version (from memory, unverified). Fetched Microsoft pages: waterfall, histogram, box and whisker and sunburst list Excel 2016 in their Applies To lists; the Pareto and treemap pages list only 365, 2024 and 2021 (2016 availability of those two is unconfirmed; see Q35 of this part). Funnel needs Office 2021 or Microsoft 365 on Windows per the current Microsoft page; map needs Microsoft 365 (Microsoft Support pages above).
**Edge cases:** A chart type that does not fit the data (pie with negatives or 15 slices) is a red flag.
**Likely follow-ups:** 1) *Pie or bar?* Bar when slices are close or many. 2) *Many series on a line chart?* Limit to about 4-5 lines or use small multiples.
**Common mistakes:** Choosing the flashy chart first; 3D effects; too many categories; forgetting the title says what the chart shows.

### Q2 ⭐⭐⭐ 🟢 When would you use a column or bar chart, and when a line chart?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you tell comparison from trend?
**Say this in the interview:** "Column or bar compares separate categories, like departments. Line shows how one thing moves through time, like monthly attrition. If the horizontal axis is time in order, I use a line; if names, a column or bar."
**Explain simply:**
- Column (vertical bars): compare categories, or a few time periods (Microsoft Support, "Available chart types in Office").
- Bar (horizontal bars): same job, better when category names are long, such as "Learning and Development".
- Line: best for trends over evenly spaced intervals and many points (same page).
- A line joins points, which implies "in between" values exist, so it makes no sense for unrelated categories like departments.
**Example:** Headcount by department (Sales 210, Operations 180, IT 120) is a bar chart. Monthly attrition (Jan 2.02%, Feb 1.63%, Mar 2.48%, ...) is a line chart.
**Sample sheet (trend data, then a separate headcount table):**

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Month | Opening | Leavers | Closing | Attrition % |
| 2 | Jan | 500 | 10 | 492 | 2.02% |
| 3 | Feb | 492 | 8 | 488 | 1.63% |
| 4 | Mar | 488 | 12 | 480 | 2.48% |
| 5 | Apr | 480 | 9 | 474 | 1.89% |
| 6 | May | 474 | 7 | 469 | 1.48% |
| 7 | Jun | 469 | 11 | 462 | 2.36% |
| 8 | Jul | 462 | 10 | 456 | 2.18% |
| 9 | Aug | 456 | 6 | 452 | 1.32% |
| 10 | Sep | 452 | 8 | 448 | 1.78% |
| 11 | Oct | 448 | 12 | 440 | 2.70% |
| 12 | Nov | 440 | 7 | 436 | 1.60% |
| 13 | Dec | 436 | 9 | 431 | 2.08% |

**Formula / Steps:** `E2: =C2/AVERAGE(B2,D2)`, fill down to row 13. Annual: `=SUM(C2:C13)/AVERAGE(B2:B13)`. Peak month: `=INDEX(A2:A13,MATCH(MAX(E2:E13),E2:E13,0))`. Chart (not run here): select A1:A13 and E1:E13 > Insert > Line with Markers > add title and axis titles.
**Alternative:** Add a rolling 12-month line (leavers in last 12 months divided by average headcount) to smooth seasonality; or a column chart of leavers with attrition % line (Q8).
**Result:** Re-run in LibreOffice on the full 12-row table above: monthly 2.02%, 1.63%, 2.48%, 1.89%, 1.48%, 2.36%, 2.18%, 1.32%, 1.78%, 2.70%, 1.60%, 2.08%; annual 109 / 466.42 = 23.37%; peak month Oct.
**Version note:** Line charts in all versions.
**Edge cases:** Months with zero leavers give 0%, not blank; a month with zero headcount would give #DIV/0!, wrap in IFERROR.
**Likely follow-ups:** 1) *Monthly vs annualised?* Multiply monthly by 12 only as an approximation. 2) *Voluntary vs involuntary?* Show as two lines.
**Common mistakes:** Dividing by closing headcount only; mixing counts and % on one axis; starting the axis above zero.

### Q10 ⭐⭐ 🟢 What is the difference between a clustered column chart and a stacked column chart, and when do you use each?
**Asked at:** commonly asked (no company-specific report found); appears in the ClimbTheLadder Excel charts list (undated).
**What the interviewer is checking:** Compare parts versus show total and parts.
**Say this in the interview:** "Clustered puts each series side by side so you can compare them directly; stacked piles them up so you see the total and the make-up. For share of total across periods I use 100% stacked."
**Explain simply:**
- *Series* = one set of values, e.g. one hiring source.
- Clustered: easy to compare individual values, hard to see totals.
- Stacked: shows totals; only the bottom segment has a common baseline, so the upper ones are hard to compare.
- 100% stacked: each column is scaled to 100%.
**Example:** Hires per quarter by source (Referral, Portal, Agency): Q1 30/20/10 = 60; Q2 35/22/13 = 70; Q3 40/18/12 = 70; Q4 45/25/15 = 85. Referral share Q1 50%, Q4 52.9%.
**Sample sheet:**

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Quarter | Referral | Portal | Agency | Total |
| 2 | Q1 | 30 | 20 | 10 | 60 |
| 3 | Q2 | 35 | 22 | 13 | 70 |
| 4 | Q3 | 40 | 18 | 12 | 70 |
| 5 | Q4 | 45 | 25 | 15 | 85 |

**Formula / Steps:** `E2: =SUM(B2:D2)`; share `=B2/E2`. Chart (not run here): select A1:D5 > Insert > Insert Column or Bar Chart > Clustered Column or Stacked Column.
**Alternative:** Use a 100% stacked column when the question is "share", or a line chart for 3 series over time.
**Result:** Run in LibreOffice: totals 60, 70, 70, 85; Referral share 0.5 (Q1) and 0.5294 (Q4).
**Version note:** All versions.
**Edge cases:** Stacked charts cannot show negative values meaningfully.
**Likely follow-ups:** 1) *When avoid stacked?* More than 4-5 segments. 2) *Add totals?* Add a hidden line series of totals with labels.
**Common mistakes:** Stacking series that do not add to a meaningful whole; unsorted segments.

### Q11 ⭐⭐ 🟢 When is a pie chart appropriate, and when should you avoid it?
**Asked at:** commonly asked (no company-specific report found); on the ClimbTheLadder Excel charts list (undated).
**What the interviewer is checking:** Do you know pie's narrow use?
**Say this in the interview:** "Pie is fine for one series, parts of a whole, with a handful of slices and no negatives. Microsoft says no more than seven categories. If slices are similar or many, I use a sorted bar chart."
**Explain simply:**
- Microsoft: pie shows each part's share; use for a single series, no negative values, few zeros, no more than seven categories (Microsoft Support, "Available chart types in Office").
- People compare lengths better than angles, so close slices are hard to rank.
- Slices must sum to 100% of something meaningful.
**Example:** Headcount 600: Sales 210 (35%), Operations 180 (30%), IT 120 (20%), Finance 45 (7.5%), HR 30 (5%), Legal 15 (2.5%). The top two are 65%. Pie is acceptable but a sorted bar is clearer.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Dept | Headcount | Share |
| 2 | Sales | 210 | 35% |
| 3 | Operations | 180 | 30% |
| 4 | IT | 120 | 20% |
| 5 | Finance | 45 | 7.5% |
| 6 | HR | 30 | 5% |
| 7 | Legal | 15 | 2.5% |

**Formula / Steps:** `C2: =B2/SUM($B$2:$B$7)`. Chart (not run here): select A1:B7 > Insert > Insert Pie or Doughnut Chart > Pie > Chart Design > Add Chart Element > Data Labels (percentage).
**Alternative:** Sorted bar chart, or a stacked 100% bar for one total.
**Result:** Run in LibreOffice: shares 0.35, 0.30, 0.20, 0.075, 0.05, 0.025; total 600.
**Version note:** All versions.
**Edge cases:** Negative values cannot be plotted in a pie; zero slices clutter labels.
**Likely follow-ups:** 1) *Doughnut?* Same, harder to read. 2) *3D pie?* Avoid (Q53).
**Common mistakes:** Pie with 12 months; exploded slices; legends instead of direct labels.

### Q12 ⭐⭐ 🟢 What are a data series, the category axis, the value axis and the legend in an Excel chart?
**Asked at:** commonly asked (no company-specific report found); "data series" is on the ClimbTheLadder list (undated).
**What the interviewer is checking:** Vocabulary of chart anatomy.
**Say this in the interview:** "A data series is one set of values, like Hires. The category axis labels the groups, such as months. The value axis is the numeric scale. The legend explains which colour is which series."
**Explain simply:**
- *Data series*: one row or column of numbers plotted together, with a name.
- *Category axis* (horizontal in column charts, also called X axis): the labels.
- *Value axis* (vertical, Y axis): the numeric scale.
- *Legend*: the key; unnecessary with a single series.
**Example:** Table with Month, Hires, Exits: two series (Hires, Exits), categories Jan to Apr, values 0-25 on the axis.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Month | Hires | Exits |
| 2 | Jan | 12 | 8 |
| 3 | Feb | 18 | 10 |
| 4 | Mar | 15 | 12 |
| 5 | Apr | 22 | 9 |

**Formula / Steps:** Right-click chart > Select Data > check Legend Entries (Series) on the left and Horizontal (Category) Axis Labels on the right (path from memory, unverified). Not run here.
**Alternative:** Chart Design > Select Data in the Data group.
**Result:** Not run here (concept). By hand: 2 series, 4 categories, max value 22 so the axis auto-scales to 0-25.
**Version note:** Same in all versions.
**Edge cases:** Header cells left blank may turn a text column into a series.
**Likely follow-ups:** 1) *Primary vs secondary axis?* Q8. 2) *How to swap?* Q16.
**Common mistakes:** Mixing up category and value axis; keeping a legend for one series.

### Q13 ⭐⭐ 🟢 How do you add or edit a chart title, axis titles and data labels?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic chart formatting fluency.
**Say this in the interview:** "Click the chart, use the green plus button or Chart Design > Add Chart Element, and choose Chart Title, Axis Titles or Data Labels. I click the title text to edit it, or link it to a cell."
**Explain simply:**
- *Chart title*: say the message, e.g. "Attrition peaked in October".
- *Axis titles*: name the unit (Month; Attrition %).
- *Data labels*: values printed on the bars or points; by default they are linked to worksheet values and update automatically (Microsoft Support, "Add or remove data labels in a chart").
- Pie and doughnut charts have no axes, so no axis titles (Microsoft Support, screen-reader chart guide).
**Example:** Headcount chart: title "Headcount by department, Dec", axis title "Employees", labels 210, 180, 120.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Dept | Headcount |
| 2 | Sales | 210 |
| 3 | Operations | 180 |
| 4 | IT | 120 |

**Formula / Steps:** (not run here) 1. Select the chart. 2. Chart Design tab > Add Chart Element > Chart Title > Above Chart (the page lists this menu path in its keyboard shortcuts). 3. Add Chart Element > Axis Titles > Primary Horizontal / Vertical. 4. Add Chart Element > Data Labels, or the green plus icon > tick Data Labels (Microsoft Support). 5. Click the text to edit.
**Alternative:** Select the title, type `=` in the formula bar and click a cell to link it (from memory, unverified); a worked formula for a changing title is `="Attrition: "&TEXT(E14,"0.0%")`, which returned "Attrition: 23.4%" when the % is 0.2337 (calculated by hand, not run in LibreOffice).
**Result:** Not run here (formatting).
**Version note:** The label page lists Microsoft 365, 2024 and 2021; the same options exist in 2016/2019 (from memory, unverified).
**Edge cases:** Removing and re-adding a title loses custom text.
**Likely follow-ups:** 1) *Labels for one series only?* Select the series first. 2) *Percent labels on pie?* Format Data Labels > Percentage.
**Common mistakes:** Default titles like "Chart Title"; labels overlapping; missing units.

### Q14 ⭐⭐ 🟢 What are sparklines, and what types are available?
**Asked at:** commonly asked (no company-specific report found); sparklines appear in dashboard course material (OpenClassrooms, snippet only).
**What the interviewer is checking:** Awareness of in-cell mini charts.
**Say this in the interview:** "Sparklines are tiny charts inside a single cell showing a trend for a row of data. There are three types: Line, Column and Win/Loss."
**Explain simply:**
- A sparkline lives in one cell next to the numbers, so a table shows trends at a glance.
- Types: Line, Column, Win/Loss (Microsoft Support, "Use sparklines to show data trends").
- Win/Loss shows positive or negative only.
- You can mark high/low points with Markers and show the axis for negative values (same page).
**Example:** Salary index per employee over 5 reviews: 88, 92, 95, 90, 101. Max 101, min 88, change +13 (+14.8%).
**Sample sheet:**

| | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| 1 | Employee | R1 | R2 | R3 | R4 | R5 | Trend |
| 2 | Asha | 88 | 92 | 95 | 90 | 101 | (sparkline) |

**Formula / Steps:** 1. Click G2. 2. Insert tab > Sparklines group > Line (or Column / Win/Loss). 3. Data Range: B2:F2 > OK. 4. Drag the fill handle down (Microsoft Support). Check: `=MAX(B2:F2)`, `=MIN(B2:F2)`, `=F2-B2`. Sparkline itself not run here.
**Alternative:** A normal small chart; or REPT-based in-cell bars (from memory, unverified).
**Result:** Run in LibreOffice: max 101, min 88, change 13, growth 14.77%.
**Version note:** The Microsoft page lists Excel 2016, 2019, 2021, 2024, 365. Sparklines originated in Excel 2010 (from memory, unverified). Google Sheets has `=SPARKLINE()` (from memory, unverified).
**Edge cases:** Blank cells are shown as gaps by default; each sparkline scales independently unless you set same axis min/max.
**Likely follow-ups:** 1) *Same scale for all?* Sparkline > Axis > Same for All Sparklines (from memory, unverified). 2) *Difference from a chart?* Sparklines have no axes, titles or labels.
**Common mistakes:** Comparing sparklines drawn on different scales; no numbers beside them.

### Q15 ⭐⭐ 🟢 How do you add a trendline to a chart, and what does the R-squared value tell you?
**Asked at:** commonly asked (no company-specific report found); trendline is on the ClimbTheLadder list (undated).
**What the interviewer is checking:** Do you know a trendline is a fitted line and R-squared measures fit, not causation?
**Say this in the interview:** "Select the chart, click the green plus, tick Trendline, and choose linear or another type. In Format Trendline I can tick Display R-squared. R-squared runs from 0 to 1 and says how closely the line fits the data; it does not prove cause."
**Explain simply:**
- *Trendline*: a line that best fits the points. Types: linear, exponential, logarithmic, polynomial, power, moving average (Microsoft Support, "Add a trend or moving average line to a chart").
- *R-squared*: a number from 0 to 1 showing how closely the trendline's estimates match actual data (same page, Microsoft's example 0.9792).
- 0.94 means the line explains about 94% of the ups and downs; 0.01 means almost none.
- *Moving average* trendline smooths noise; points equal total minus the period (same page).
**Example:** Monthly offers accepted for 8 months: 62, 66, 65, 71, 74, 73, 79, 83. Slope 2.85 per month, intercept 58.82, R-squared 0.945. Forecast for month 9: 84.4.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Month no. | Offers accepted |
| 2 | 1 | 62 |
| 3 | 2 | 66 |
| 4 | 3 | 65 |
| 5 | 4 | 71 |
| 6 | 5 | 74 |
| 7 | 6 | 73 |
| 8 | 7 | 79 |
| 9 | 8 | 83 |

**Formula / Steps:** Chart (not run here): select chart > green plus (Chart Elements) > Trendline > pick type; Format Trendline pane > tick Display R-squared value on chart (the R-squared tick-box path is from memory, unverified: the fetched page gave no steps for it). Check with formulas: `=SLOPE(B2:B9,A2:A9)`, `=INTERCEPT(B2:B9,A2:A9)`, `=RSQ(B2:B9,A2:A9)`, `=FORECAST(9,B2:B9,A2:A9)`.
**Alternative:** Skip the chart and use `=RSQ()` / `LINEST` on the sheet.
**Result:** Run in LibreOffice: slope 2.8452, intercept 58.8214, R-squared 0.9448, forecast(9) 84.4286. A scrambled series (62, 95, 40, 88, 50, 91, 45, 70) gave R-squared 0.011 (pandas).
**Version note:** Microsoft page applies to Microsoft 365, 2024, 2021 versions; trendlines exist in 2016/2019 (from memory, unverified).
**Edge cases:** Microsoft notes the Trendline button only appears in the Elements menu for multi-series charts when no series is selected; select a series first for a single-series chart. High R-squared with 8 points is not strong evidence.
**Likely follow-ups:** 1) *Does high R-squared mean cause?* No. 2) *Forecast ahead?* Trendline > Forecast Forward periods.
**Common mistakes:** Extrapolating far ahead; reading R-squared as accuracy of the forecast; using a polynomial of high order to force a good fit.

### Q16 ⭐⭐ 🟢 A chart is plotting the wrong way round (months as series instead of categories). How do you fix it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Switch Row/Column and the rule behind it?
**Say this in the interview:** "I click the chart, go to Chart Design and press Switch Row/Column. It swaps what is plotted as series and what is plotted as categories."
**Explain simply:**
- Excel decides automatically: it puts the larger number of rows or columns on the horizontal axis; if equal, rows are plotted on the vertical axis and columns on the horizontal (Microsoft Support, "Change how rows and columns of data are plotted in a chart", fetched: "Excel places the larger number on the horizontal axis"; for equal counts it "plots the rows of data on the vertical axis, and the columns of data on the horizontal axis").
- So a square block (4 months x 4 departments) can come out the wrong way round.
- Switching changes what appears in the legend versus the axis labels.
**Example:** Headcount for 4 months (rows) by 4 departments (columns). Equal counts, so months become the legend; Switch Row/Column puts months on the axis, 4 series (departments) x 4 categories (months) = 16 bars either way.
**Sample sheet:**

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | | Sales | IT | HR | Finance |
| 2 | Jan | 210 | 120 | 30 | 45 |
| 3 | Feb | 205 | 124 | 30 | 45 |
| 4 | Mar | 200 | 126 | 31 | 44 |
| 5 | Apr | 198 | 130 | 31 | 44 |

**Formula / Steps:** 1. Click a point in the chart (Chart Design and Format tabs appear). 2. Chart Design tab > Data group > Switch Row/Column (Microsoft Support). Alternatively Chart Design > Select Data > Switch Row/Column. Not run here.
**Alternative:** Re-lay out the table so the larger dimension runs along the axis you want, or select the data again.
**Result:** Not run here (chart behaviour). By hand: 4 x 4 = 16 data points either way.
**Version note:** The fetched page's Applies To list names only Microsoft 365, 2024 and 2021; the button also exists in Excel 2016 and 2019 (from memory, unverified; the page is silent on them).
**Edge cases:** Does not work if the chart is not selected or the data is a PivotChart (change the pivot layout instead, from memory, unverified).
**Likely follow-ups:** 1) *Why did it happen?* Equal rows and columns. 2) *Fix for a PivotChart?* Move fields between Axis and Legend.
**Common mistakes:** Retyping data instead of switching; selecting the entire sheet.

### Q17 ⭐⭐ 🟢 You have headcount by department in a table. Which chart would you make for HR leadership, and how would you present it?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured scenario.
**What the interviewer is checking:** Chart choice, ordering, and a message-first presentation.
**Say this in the interview:** "A sorted horizontal bar chart, largest at the top, with data labels and a title that states the finding, for example 'Sales and Operations hold 65% of headcount'. Pie is fine only if there are very few departments."
**Explain simply:**
- Bars are easiest to compare, and horizontal bars fit long names.
- Sort descending so ranking is obvious.
- Direct labels remove the need for gridlines or a legend.
- Add the "so what" in the title.
**Example:** 600 employees: Sales 210, Operations 180 (together 390 = 65%), IT 120, Finance 45, HR 30, Legal 15. The smallest three are 15% combined.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Dept | Headcount | Share |
| 2 | Sales | 210 | 35% |
| 3 | Operations | 180 | 30% |
| 4 | IT | 120 | 20% |
| 5 | Finance | 45 | 7.5% |
| 6 | HR | 30 | 5% |
| 7 | Legal | 15 | 2.5% |

**Formula / Steps:** `C2: =B2/SUM($B$2:$B$7)`; top-two share `=SUMPRODUCT(LARGE(B2:B7,{1,2}))/SUM(B2:B7)`. Chart (not run here): Data > Sort Z to A on Headcount > Insert > Bar > Clustered Bar > Format Axis > Categories in reverse order (largest on top, from memory, unverified) > Add Data Labels > edit title.
**Alternative:** A treemap (Microsoft's treemap page lists 365, 2024 and 2021; 2016 not confirmed, see Q35) or a pie for 3-4 departments.
**Result:** Run in LibreOffice: shares 0.35, 0.30, 0.20, 0.075, 0.05, 0.025; top two = 0.65; bottom three = 0.15; total 600.
**Version note:** Bar charts in all versions.
**Edge cases:** Include a total in the title; mention the date of the snapshot.
**Likely follow-ups:** 1) *Compare against last year?* Clustered bar or dot plot. 2) *Many departments?* Group small ones as Other (Q41).
**Common mistakes:** Alphabetical order; 3D; no date or total.

### Q18 ⭐⭐ 🟢 What are good practices for choosing colours and formatting in Excel charts?
**Asked at:** commonly asked (no company-specific report found); colour practice is on the ClimbTheLadder list (undated).
**What the interviewer is checking:** Taste and accessibility, not decoration.
**Say this in the interview:** "Use one neutral colour for most bars and one accent for what matters, keep consistent colours across the dashboard, avoid red-green only distinctions, make sure text contrasts with the background, and remove clutter like heavy gridlines."
**Explain simply:**
- Colour should carry meaning: grey for context, one accent for the message.
- About 1 in 12 men have colour vision deficiency (US National Eye Institute, "Color Blindness", fetched), so do not rely on red versus green alone; add labels or icons.
- Contrast ratio compares text and background brightness; the WCAG 2.1 Level AA rule asks at least 4.5:1 for normal text (W3C, "Understanding Success Criterion 1.4.3: Contrast (Minimum)", fetched).
- Remove 3D, shadows, heavy borders; keep fonts consistent and at least 10-12 pt.
**Example:** Contrast on white background (calculated with the WCAG formula in Python): dark blue #1F4E79 8.66, dark red #C00000 6.48, mid-grey #7F7F7F 4.00 (fails 4.5), light grey #BFBFBF 1.84, yellow #FFFF00 1.07.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Colour | Contrast vs white |
| 2 | #1F4E79 | 8.66 |
| 3 | #C00000 | 6.48 |
| 4 | #7F7F7F | 4.00 |
| 5 | #FFFF00 | 1.07 |

**Formula / Steps:** (not run here) Select a series > Format tab > Shape Fill; or Chart Design > Change Colors; set Page Layout > Colors > a theme so the workbook stays consistent. Highlight one bar: click the bar twice > Shape Fill.
**Alternative:** Use a company theme palette (Page Layout > Themes) so charts match slides.
**Result:** Contrast ratios computed in Python (not Excel); the 4.5:1 target is confirmed by the W3C page named above. Re-computed here: 8.66, 6.48, 4.00, 1.84, 1.07 all match.
**Version note:** Format options are in all versions.
**Edge cases:** Printing in black and white removes colour distinctions; use patterns or labels.
**Likely follow-ups:** 1) *Rainbow palette?* Avoid for ordered data. 2) *Red and green?* Add arrows or text.
**Common mistakes:** Every bar a different colour; yellow text; the default style with gridlines everywhere.

### Q19 ⭐⭐ 🟢 How do you hide gridlines and headings on a dashboard sheet so it looks clean?
**Asked at:** commonly asked (no company-specific report found); dashboard-building is a standard MIS/reporting task.
**What the interviewer is checking:** Do you know the basic "make it presentable" steps, not just how to make a chart?
**Say this in the interview:** "I go to the View tab and untick Gridlines and Headings, which removes the grey cell lines and the A, B, C and 1, 2, 3 labels. Then I fill the background white or a light colour, hide the formula bar and keep the layout inside one screen."
**Explain simply:**
- **Gridlines** are the faint lines between cells. **Headings** are the column letters and row numbers.
- Both are display settings only. Formulas and cell addresses still work; turning them off does not delete anything.
- Microsoft's dashboard walkthrough does exactly this: its example dashboard "turned off Headings and Gridlines from the View tab" (Microsoft Support, "Create and share a Dashboard with Excel and Microsoft Groups").
- The setting is per sheet, so repeat it on every dashboard sheet. Keep your data and calculation sheets with gridlines on, so they are easy to audit.
**Example:** An HR attrition dashboard on a sheet called "Dashboard": gridlines off, headings off, KPI cards in cells B2:M5, charts below. The data sits on a separate sheet named "Data" that still shows gridlines.
**Formula / Steps (not run here: display settings cannot be executed headlessly):**
1. Click the dashboard sheet tab.
2. View tab > Show group > untick **Gridlines**; untick **Headings**; optionally untick **Formula Bar**.
3. Select all (Ctrl+A) > Home > Fill Color > white, so the background is uniform.
4. Hide unused columns/rows (right-click > Hide) so nobody scrolls into empty space.
**Alternative:** Page Layout tab > Sheet Options > Gridlines "View" and Headings "View" boxes (from memory, unverified). Ctrl+F1 collapses the ribbon for more room.
**Version note:** The Microsoft page applies to Excel for Microsoft 365, 2024, 2021, 2019 and 2016 (Microsoft Support, same page). Google Sheets: View > Show > Gridlines; headings via View > Show (from memory, unverified).
**Edge cases:** Printing is separate: gridlines do not print unless ticked under Page Layout > Sheet Options > Gridlines "Print". A white fill hides gridlines visually but the setting is still on.
**Likely follow-ups:** 1) *Does hiding headings stop formulas?* No. 2) *How do you stop users scrolling away?* Hide unused rows/columns and protect the sheet (see Q33).
**Common mistakes:** Hiding gridlines on the data sheet too; using white cell fill everywhere (file gets heavy and hard to edit) instead of the View setting.

### Q20 ⭐⭐ 🟢 How do you copy an Excel chart into PowerPoint or Word, and what is the difference between pasting as a picture, embedding and linking?
**Asked at:** commonly asked (no company-specific report found); reporting to leadership usually ends in a slide.
**What the interviewer is checking:** Can you move a chart into a deck without breaking it, and do you understand what happens when the data changes?
**Say this in the interview:** "I click the chart, Ctrl+C, paste in PowerPoint with Ctrl+V and then pick from the Paste Options button. Picture is a frozen image, Embed carries a copy of the data inside the slide, Link stays connected to my Excel file and updates when it changes."
**Explain simply:**
- Steps from Microsoft: click the chart and press Ctrl+C; click in the other program and press Ctrl+V; click the **Paste Options** button at the bottom of the chart and choose a method (Microsoft Support, "Copy from Excel to another Office program").
- **Embed Workbook** (Use Destination Theme or Keep Source Formatting): the data travels inside the document. Editable, but a separate copy; it will not follow later changes in your Excel file.
- **Link Data** (either theme option): stays linked to the source worksheet and updates when that worksheet changes.
- **Picture**: a static image that cannot be edited or updated.
- "Destination Theme" restyles to the deck's colours; "Keep Source Formatting" keeps the Excel look.
**Example:** A monthly attrition chart goes to the CHRO deck. If the numbers are final, paste as a picture (small file, nothing to leak). If the deck is refreshed every month from the same workbook, use Link Data.
**Formula / Steps (not run here):** Excel: click chart > Ctrl+C. PowerPoint: Home > Paste dropdown or Ctrl+V > Paste Options button > choose one of five options. To refresh a link in PowerPoint: File > Info > Edit Links to Files (from memory, unverified).
**Alternative:** Excel Home > Copy dropdown > Copy as Picture, then paste (from memory, unverified); or Insert > Object in Word/PowerPoint to embed a whole workbook.
**Version note:** The copy tools are not available in Office for the web; use desktop apps (Microsoft Support, same page, as read in a search snippet). Google Sheets: chart > Copy chart, then paste into Slides with "Link to spreadsheet" (from memory, unverified).
**Edge cases:** A linked chart breaks if the Excel file is renamed, moved, or the viewer lacks access. Embedded charts can carry the whole data sheet, which may include confidential salaries; use Picture when sharing outside HR.
**Likely follow-ups:** 1) *Which is safest for confidential data?* Picture. 2) *Which updates automatically?* Link Data.
**Common mistakes:** Emailing a linked deck without the workbook; embedding a chart whose workbook contains salary data.

### Q21 ⭐⭐ 🟡 How do you make a chart update automatically when new rows of data are added?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that a chart on a fixed range will miss new rows, and the two fixes (Table or dynamic named range)?
**Say this in the interview:** "I convert the data into an Excel Table with Ctrl+T and build the chart on the whole table. Because the table grows with new rows, the chart grows with it. If I cannot use a table, I use a named range with OFFSET."
**Explain simply:**
- A normal chart points at fixed cells such as A1:B13. Add row 14 and the chart ignores it.
- An **Excel Table** (a data block Excel treats as one growing object) expands automatically when you type directly beneath it; a chart built on the full table follows (Microsoft Q&A answer from a search result; not a Microsoft Support page).
- The older method is **defined names** with OFFSET and COUNTA. Microsoft documents this: Name = `=OFFSET($B$2,0,0,COUNTA($B:$B)-1)`, then use `=Sheet1!Name` in Select Data (Microsoft Learn, "Use defined names to automatically update a chart range").
- COUNTA counts non-empty cells, so the range height grows by one per new row.
**Example:** Monthly headcount typed in A2:B5 (Jan to Apr). Adding May in row 6 should add a fifth bar.
**Sample sheet:**

| | A | B | D |
|---|---|---|---|
| 1 | Month | Headcount | `=COUNTA(A:A)-1` |
| 2 | Jan | 500 | `=SUM(OFFSET($B$2,0,0,COUNTA($B:$B)-1))` |
| 3 | Feb | 505 | |
| 4 | Mar | 498 | |
| 5 | Apr | 510 | |

**Formula / Steps (chart part not run here):**
1. Click inside the data > Insert > Table (Ctrl+T) > My table has headers.
2. Select the table > Insert > Column chart.
3. Type the next month directly under the table; the chart redraws.
Dynamic name route: Formulas > Define Name > Name `Sales`, Refers to `=OFFSET($B$2,0,0,COUNTA($B:$B)-1)`; right-click chart > Select Data > Edit series values `=Sheet1!Sales`.
**Alternative:** Named range with INDEX instead of OFFSET (`=Sheet1!$B$2:INDEX(Sheet1!$B:$B,COUNTA(Sheet1!$B:$B))`), which does not recalculate on every edit (from memory, unverified).
**Result:** Run in LibreOffice: with Jan to Apr, D1 = 4 and D2 = 2013; after adding May (515) in row 6, D1 = 5 and D2 = 2528. So the OFFSET range grew from 4 to 5 cells. The chart itself is not run here.
**Version note:** Tables and OFFSET names work in Excel 2016 to 365 (Microsoft Learn page describes "Excel 2007 and later"). Google Sheets has no Table feature for this; a chart on a whole column range (B2:B) picks up new rows (from memory, unverified).
**Edge cases:** Blank rows inside the data break COUNTA-based names. A table chart will not grow if you leave a blank row between the table and the new entry.
**Likely follow-ups:** 1) *Why prefer Table over OFFSET?* Simpler and not volatile (OFFSET recalculates every time, so it can slow big files). 2) *Pivot charts?* Refresh the pivot (Q32).
**Common mistakes:** Selecting only part of a table for the chart; typing new data one row away from the table.

### Q22 ⭐⭐ 🟡 What is a waterfall chart, when would you use it, and how do you create one?
**Asked at:** commonly asked (no company-specific report found); waterfall appears in standard Excel chart lists.
**What the interviewer is checking:** Do you know the "bridge" chart for explaining how a total moves from a start value to an end value, and can you build it?
**Say this in the interview:** "A waterfall chart shows a starting number, the increases and decreases that happen in between, and the final number. I use it for headcount bridges, like opening headcount plus hires minus exits equals closing headcount. In Excel it is Insert > Waterfall, and I set the opening and closing bars as totals."
**Explain simply:**
- Each step is a floating bar: up for increases, down for decreases. The first and last bars are totals starting from zero.
- It answers "why did the number change?" better than a plain column chart.
- Microsoft: select your data, Insert > Insert Waterfall icon > Waterfall; to mark a total, right-click the data point and choose **Set as Total** (Microsoft Support, "Create a waterfall chart").
**Example:** A company starts the year with 500 employees, hires 60, loses 45 to resignations, brings in 8 transfers and sends out 5. Closing headcount is 518.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Step | Change | Running total |
| 2 | Opening headcount | 500 | |
| 3 | Hires | 60 | |
| 4 | Resignations | -45 | |
| 5 | Transfers in | 8 | |
| 6 | Transfers out | -5 | |
| 7 | Closing headcount | | |

**Formula / Steps:** C2 `=SUM($B$2:B2)` filled down to C6; B7 `=SUM(B2:B6)`. Chart (not run here): select A1:B7 > Insert > Waterfall > right-click the Opening bar and the Closing bar > Set as Total. For a Closing row that is already a total value, leave B7 as the sum and mark it as total.
**Alternative:** Build it as a stacked column chart with an invisible "base" series (works in any version, more work); or on Excel 2013 and older use that method only.
**Result:** Run in LibreOffice: running totals 500, 560, 515, 523, 518; B7 = 518. The chart image itself is not run here.
**Version note:** Waterfall is listed for Excel 2016, 2019, 2021, 2024 and 365 (Microsoft Support, "Create a waterfall chart"). It is not in Excel 2013 or earlier (from memory, unverified). Google Sheets has a waterfall chart type (Google Docs Editors Help, "Add & edit a chart or graph" lists waterfall among chart types).
**Edge cases:** If you forget "Set as Total", the closing bar floats instead of standing on zero. Chart titles cannot be linked to a cell on waterfall charts (Microsoft Support, "Link a chart title, label, or text box to a worksheet cell").
**Likely follow-ups:** 1) *Colours?* Increase, Decrease and Total are coloured separately. 2) *Can it start from a total?* Yes, mark the first bar as total.
**Common mistakes:** Entering the closing value as another change (double counting); not setting totals.

### Q23 ⭐⭐ 🟡 How do you create a histogram in Excel, and how does it differ from a column chart?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand that a histogram counts how many values fall into ranges (bins), whereas a column chart compares categories?
**Say this in the interview:** "A histogram groups numbers into ranges called bins and counts how many values land in each, so it shows the shape of the data. A column chart compares separate categories like departments. In Excel I use Insert > Statistic Chart > Histogram, or COUNTIFS with my own bins."
**Explain simply:**
- **Bin** = a range such as 30 to 40. Bars touch each other because the ranges are continuous.
- Column chart: one bar per category, you decide the order. Histogram: one bar per numeric range, order is fixed by the numbers.
- Microsoft: Insert > Insert Statistic Chart > Histogram; in Format Axis you choose By Category, Automatic (Scott's normal reference rule), Bin width, Number of bins, Overflow and Underflow bins (Microsoft Support, "Create a histogram").
**Example:** 15 employees' monthly salaries (in thousand rupees): 22, 25, 28, 31, 34, 36, 38, 41, 45, 47, 52, 58, 64, 72, 95.
**Sample sheet:**

| | A | C | D | E |
|---|---|---|---|---|
| 1 | Salary | Bin from (above) | Bin to (up to) | Count |
| 2 | 22 | 20 | 30 | |
| 3 | 25 | 30 | 40 | |
| 4 | 28 | 40 | 50 | |
| 5 | 31 | 50 | 60 | |
| 6 | 34 | 60 | 100 | |

(A7 to A16 hold the other nine salaries.)

**Formula / Steps:** E2 `=COUNTIFS($A$2:$A$16,">"&C2,$A$2:$A$16,"<="&D2)` filled to E6. Chart (not run here): select A1:A16 > Insert > Insert Statistic Chart > Histogram > right-click the horizontal axis > Format Axis > set Bin width 10.
**Alternative:** `=FREQUENCY(A2:A16,D2:D6)` as an array formula, then a column chart with gap width 0; or the old Analysis ToolPak Histogram tool, which outputs a table and chart on a new sheet (Microsoft page describes this older tool without naming the ToolPak).
**Result:** Run in LibreOffice: counts 3, 4, 3, 2, 3 (total 15). Mean 45.87, median 41, confirmed with pandas. The skew (mean above median) is the "long right tail" the histogram shows. The chart is not run here.
**Version note:** Histogram chart is listed for Excel 2016, 2019, 2021, 2024 and 365 (Microsoft Support, "Create a histogram"); the mobile version needs Microsoft 365. Google Sheets has a histogram chart type (Google Docs Editors Help list, as above).
**Edge cases:** Bin boundaries: Microsoft's histogram page (fetched) says a value falls in a bin if it is greater than the lower bound and "equal to or less than the greatest bound", so the upper bound is included; my COUNTIFS uses the same rule. The page does not use interval notation. Text or blank cells are ignored.
**Likely follow-ups:** 1) *Mean vs median?* Median is safer when a 95 outlier is present. 2) *Pareto?* See Q24.
**Common mistakes:** Using a column chart with a gap between bars; choosing bins so narrow that every bar is 1.

### Q24 ⭐⭐ 🟡 What is the difference between a Pareto chart and a histogram?
**Asked at:** Prep-blog question lists (ClimbTheLadder "20 Excel Charts Interview Questions", undated, question list read); no company-specific report found.
**What the interviewer is checking:** Do you know a Pareto is a sorted bar chart with a cumulative percentage line used to find the "vital few" causes?
**Say this in the interview:** "A histogram shows how numbers spread across ranges. A Pareto chart shows categories sorted from biggest to smallest with a cumulative percentage line, so you see which few causes explain most of the problem."
**Explain simply:**
- Microsoft calls Pareto a sorted histogram: columns in descending order plus "a line representing the cumulative total percentage" (Microsoft Support, "Create a Pareto chart").
- Histogram: x-axis is numeric ranges (salary bands), order is natural. Pareto: x-axis is categories (exit reasons), order is by size.
- Pareto is built to apply the 80/20 idea: find the few categories behind most of the impact.
**Example:** 100 resignations by exit-interview reason. The top three reasons cover 83 of the 100.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Reason | Exits | Share | Cumulative % |
| 2 | Better pay | 38 | | |
| 3 | Career growth | 27 | | |
| 4 | Manager | 18 | | |
| 5 | Relocation | 9 | | |
| 6 | Health | 5 | | |
| 7 | Other | 3 | | |

**Formula / Steps:** C2 `=B2/SUM($B$2:$B$7)`; D2 `=SUM($B$2:B2)/SUM($B$2:$B$7)`; fill down. Chart (not run here): select A1:B7 > Insert > Insert Statistic Chart > Histogram group > Pareto.
**Alternative:** Manual Pareto: sort descending, column chart for Exits plus a line on a secondary axis for Cumulative % (the combo method from Q8).
**Result:** Run in LibreOffice: shares 38%, 27%, 18%, 9%, 5%, 3%; cumulative 38%, 65%, 83%, 92%, 97%, 100%. The chart is not run here.
**Version note:** The current Microsoft page lists Microsoft 365, 2024 and 2021 in its Applies To list; Excel 2016 and 2019 are not listed. Pareto was added with the Excel 2016 statistic charts (from memory, unverified); in Excel 2016/2019 a manual combo chart is the safe route. Pareto charts cannot have their titles linked to cells (Microsoft Support link-title page).
**Edge cases:** The built-in Pareto sorts and groups categories for you; the manual method needs sorted data. "Other" is conventionally last even if larger than some others.
**Likely follow-ups:** 1) *Where would you use it?* Exit reasons, grievance types, absence causes. 2) *Why 80/20?* A rule of thumb that most effect comes from few causes; not a law.
**Common mistakes:** Not sorting; reading the cumulative line against the left axis.

### Q25 ⭐⭐ 🟡 How do you build KPI cards on a dashboard that show the value, target and variance with an up or down indicator?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you build live, formula-driven cards and handle "lower is better" metrics correctly?
**Say this in the interview:** "A KPI card is a few merged cells showing the actual, the target, the variance and an arrow. I calculate each value with formulas pointing to my calculation sheet, then use an IF formula or icon sets for the arrow. For metrics like attrition, lower is better, so the arrow logic flips."
**Explain simply:**
- **KPI** (key performance indicator) = one number the business tracks, such as attrition %.
- **Variance** = Actual minus Target; **variance %** = Variance divided by Target.
- The arrow must follow "good or bad", not just "up or down". Higher attrition is bad; higher offer acceptance is good.
- Cards should link to cells (`='Calc'!B5`) so they update with filters and refreshes.
**Example:** Attrition 11.2% vs target 10%; offer acceptance 78% vs 80%; days to hire 34 vs 40; training hours 12.5 vs 12.
**Sample sheet:**

| | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 1 | KPI | Actual | Target | Variance | Variance % | Status |
| 2 | Attrition % (lower is better) | 11.2% | 10% | | | |
| 3 | Offer acceptance % | 78% | 80% | | | |
| 4 | Avg days to hire (lower is better) | 34 | 40 | | | |
| 5 | Training hours per employee | 12.5 | 12 | | | |

**Formula / Steps:** D2 `=B2-C2`; E2 `=IF(C2=0,"",D2/C2)`; F2 (lower is better) `=IF(B2<=C2,"▲ On track","▼ Off track")`; F3 (higher is better) `=IF(B3>=C3,"▲ On track","▼ Off track")`. Colour: Home > Conditional Formatting > New Rule > Format only cells that contain "Off track" > red font (not run here). Card look: merge cells, large font, thick border, gridlines off (Q19).
**Alternative:** Home > Conditional Formatting > Icon Sets > 3 Arrows, with the rule set to formula-based thresholds (from memory, unverified); or Custom number format `[Color10]▲ 0.0%;[Red]▼ 0.0%` on the variance cell (from memory, unverified, not run).
**Result:** Run in LibreOffice: variance D2:D5 = 0.012, -0.02, -6, 0.5; variance % = 12%, -2.5%, -15%, 4.17%; status = Off track, Off track, On track, On track. The formatting is not run here.
**Version note:** IF, conditional formatting and icon sets exist in Excel 2016 to 365 and in Google Sheets (conditional formatting rules there; icon sets are not built in, from memory, unverified).
**Edge cases:** Target 0 gives #DIV/0!, hence the IF. Percent values must be real numbers (0.112), not text.
**Likely follow-ups:** 1) *Why not sort arrows by sign only?* Because direction of "good" differs per KPI. 2) *Link to filters?* Use GETPIVOTDATA or formulas on the pivot output.
**Common mistakes:** Green arrow for rising attrition; hard-typing values into cards instead of linking.

### Q26 ⭐⭐ 🟡 How do you show actual versus target in an Excel chart?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you pick a chart that makes the gap to target obvious: columns for actual with a target line?
**Say this in the interview:** "I put actual and target in two columns, make a clustered column chart, and change the target series to a line using Change Series Chart Type. Columns show what happened, the line shows the goal, so misses are obvious at a glance."
**Explain simply:**
- Layout: Month, Actual, Target in adjacent columns, so one chart reads both.
- **Combo chart** = a chart mixing two types (columns and a line). Both can share the same axis because they have the same unit.
- Add a Variance column (Actual minus Target) and, if useful, a cumulative view for year-to-date.
**Example:** Hiring target 20 per month; actual hires Jan to Jun are 18, 22, 15, 25, 19, 24.
**Sample sheet:**

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Month | Actual hires | Target | Variance | Achievement % |
| 2 | Jan | 18 | 20 | | |
| 3 | Feb | 22 | 20 | | |
| 4 | Mar | 15 | 20 | | |
| 5 | Apr | 25 | 20 | | |
| 6 | May | 19 | 20 | | |
| 7 | Jun | 24 | 20 | | |

**Formula / Steps:** D2 `=B2-C2`; E2 `=B2/C2`; totals B8 `=SUM(B2:B7)`, C8 `=SUM(C2:C7)`. Chart (not run here): select A1:C7 > Insert > Combo chart > Clustered Column - Line (Actual as column, Target as line). Or right-click the Target series > Change Series Chart Type > Line. Put a data label on the last point only.
**Alternative:** Target as a thin horizontal marker series (dash markers, no line) for a "bullet" look; or two stacked bars (actual, remaining gap) for a progress bar.
**Result:** Run in LibreOffice: variance -2, 2, -5, 5, -1, 4; achievement 90%, 110%, 75%, 125%, 95%, 120%; totals actual 123 vs target 120, variance +3, achievement 102.5%. The chart is not run here.
**Version note:** Combo charts are in Excel 2013 and later, including 2016 to 365 (the Microsoft "Available chart types in Office" page lists Combo). Google Sheets: Chart type > Combo chart (from memory, unverified).
**Edge cases:** A target that changes each month needs the line to follow a column, not a single constant. If units differ (hires vs percentage), put one on a secondary axis (Q8).
**Likely follow-ups:** 1) *Year-to-date?* Use a cumulative column (running sum) for both. 2) *Colour misses red?* See Q47 approach (helper columns).
**Common mistakes:** Plotting target as another column of the same colour; mixing units without a secondary axis.

### Q27 ⭐⭐ 🟡 You are asked for an HR attrition dashboard. Which KPIs, charts and filters would you include?
**Asked at:** commonly asked (no company-specific report found); HR-analytics scenario question.
**What the interviewer is checking:** Do you think from the user's decision backwards, define attrition correctly, and keep the dashboard focused?
**Say this in the interview:** "First I would ask who uses it and what decision it supports. Then headline KPIs: attrition rate, leavers, average headcount, early attrition. Charts: a 12-month trend line, attrition by department, by tenure band and by exit reason. Filters: date, department, location, grade."
**Explain simply:**
- **Attrition rate** = leavers in a period divided by **average headcount** (average of opening and closing headcount, or the monthly average) for that period. Always state the formula, because companies differ.
- Keep 5 to 7 KPIs. Suggested: attrition % (monthly and year-to-date), voluntary vs involuntary, first-year (early) attrition, regretted attrition, headcount.
- Charts: line for trend (Q9), bar for departments, Pareto for exit reasons (Q24), stacked column for tenure band.
- Filters: slicers for Department, Location, Grade and a Timeline for date (Q28).
**Example:** Year with opening headcount 476 and 12 month-end headcounts; 54 people left.
**Sample sheet:**

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Month | Closing headcount | Leavers | Avg headcount | Monthly attrition % |
| 2 | Dec (opening) | 476 | | | |
| 3 | Jan | 480 | 4 | 478 | 0.84% |
| 4 | Feb | 484 | 6 | 482 | 1.24% |
| 5 | Mar | 490 | 5 | 487 | 1.03% |
| 6 | Apr | 492 | 7 | 491 | 1.43% |
| 7 | May | 495 | 3 | 493.5 | 0.61% |
| 8 | Jun | 497 | 4 | 496 | 0.81% |
| 9 | Jul | 499 | 6 | 498 | 1.20% |
| 10 | Aug | 500 | 5 | 499.5 | 1.00% |
| 11 | Sep | 501 | 5 | 500.5 | 1.00% |
| 12 | Oct | 502 | 3 | 501.5 | 0.60% |
| 13 | Nov | 503 | 2 | 502.5 | 0.40% |
| 14 | Dec | 500 | 4 | 501.5 | 0.80% |

**Formula / Steps:** D3 `=AVERAGE(B2:B3)`; E3 `=C3/D3`; year row: C15 `=SUM(C3:C14)`, D15 `=AVERAGE(D3:D14)`, E15 `=C15/D15`. Dashboard build (not run here): PivotTable from an employee table (Join Date, Exit Date, Dept, Grade) > PivotCharts > Slicers (Q6, Q7).
**Alternative:** Calculate attrition from the employee list with COUNTIFS on the exit date between month start and end, and headcount with COUNTIFS on join date <= month end and (exit date blank or > month end).
**Result:** Re-run in LibreOffice on the full table above (closing headcounts for Apr to Dec were chosen so the year averages 494.25): January 4/478 = 0.84%, February 6/482 = 1.24%, March 5/487 = 1.03%; year: 54 leavers, average headcount 494.25, annual attrition 10.93%. Summing the twelve monthly rates gives 10.94%, nearly identical.
**Version note:** Everything above works in Excel 2016 to 365 (slicers and timelines on pivots are covered in Microsoft's dashboard walkthrough for 2016 to 365). Google Sheets has slicers but no Timeline (Google Docs Editors Help, "Filter charts and tables with Slicers"; Timeline absence from memory, unverified).
**Edge cases:** Definition: some companies divide by opening headcount; say which you use. Mid-month joiners and leavers shift the average. Small departments give noisy percentages; show counts as well.
**Likely follow-ups:** 1) *Annualising a monthly rate?* Multiply by 12 or use year-to-date leavers over average headcount. 2) *Voluntary vs involuntary?* A split bar.
**Common mistakes:** Dividing by closing headcount without saying so; 15 KPIs; no clear definition on the page.

### Q28 ⭐⭐ 🟡 What is a Timeline in Excel, and how do you use it on a dashboard?
**Asked at:** commonly asked (no company-specific report found); Timelines appear in Microsoft's dashboard walkthrough.
**What the interviewer is checking:** Do you know the date-specific filter that works alongside slicers on PivotTables?
**Say this in the interview:** "A Timeline is a slicer built for dates. It shows a sliding bar for months, quarters or years, so a manager can drag to choose a period and all connected pivots and charts update."
**Explain simply:**
- It works only with a real **date field** in a PivotTable or PivotChart; text that looks like dates will not appear.
- Microsoft's steps: select any PivotTable > PivotTable Analyze > Filter > Insert Timeline > tick the date field (the example uses Order Date) (Microsoft Support, "Create and share a Dashboard with Excel and Microsoft Groups").
- Like slicers, one timeline can control several PivotTables if they share the same data source: select it, open Report Connections and tick the pivots (same Microsoft page).
- Time levels (Years, Quarters, Months, Days) are chosen from the dropdown at the top right of the timeline; that detail is from memory, unverified, since the Microsoft page does not describe levels.
**Example:** Joiners table with 8 joining dates in 2026. Selecting January to March on the timeline should show 5 joiners (Sales 2, Ops 2, HR 1) instead of all 8.
**Sample sheet (8 joiners, 2026):**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Join Date |
| 2 | E01 | Sales | 12-Jan-2026 |
| 3 | E02 | Ops | 20-Jan-2026 |
| 4 | E03 | HR | 09-Feb-2026 |
| 5 | E04 | Sales | 02-Mar-2026 |
| 6 | E05 | Ops | 23-Mar-2026 |
| 7 | E06 | Sales | 06-Apr-2026 |
| 8 | E07 | Ops | 18-May-2026 |
| 9 | E08 | HR | 15-Jun-2026 |

**Formula / Steps (not run here):**
1. Build the PivotTable(s) from an Excel Table with a true date column.
2. Click in the pivot > PivotTable Analyze > Insert Timeline > tick Join Date > OK.
3. Select the timeline > Timeline tab > Report Connections > tick all pivots.
4. Click and drag across months; Clear Filter button (top right) resets.
**Alternative:** A Date Group in the pivot (right-click date > Group > Months/Quarters) with a slicer on Months, or two data-validation dropdowns for start and end date driving SUMIFS.
**Result:** Pandas check on the sample (not run in Excel): Jan to Mar joiners = 5 (HR 1, Ops 2, Sales 2); quarterly counts Q1 = 5, Q2 = 3.
**Version note:** Applies to Excel 2016, 2019, 2021, 2024 and 365 (the Microsoft dashboard page's Applies To list). Google Sheets has no Timeline (from memory, unverified).
**Edge cases:** Blank or text dates stop the field showing. Slicers/timelines on a pivot do not filter plain formulas.
**Likely follow-ups:** 1) *Timeline vs date slicer?* Timeline is continuous with a bar. 2) *Does it work on tables?* Tables get slicers; timelines need a PivotTable (from memory, unverified; newer versions may differ).
**Common mistakes:** Dates stored as text; forgetting Report Connections, so only one pivot responds.

### Q29 ⭐⭐ 🟡 How do you create a chart title that changes automatically based on a cell value or filter selection?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a chart title can be linked to a cell and that the cell can be a formula?
**Say this in the interview:** "I build the title text in a cell with a formula, using & to join text and TEXT to format numbers, then click the chart title, type = in the formula bar, click that cell and press Enter. When the cell changes, the title changes."
**Explain simply:**
- Microsoft's steps: select the chart title (or pick it from the Chart Elements dropdown on the Format tab), type an equal sign in the formula bar, click the cell, press Enter (Microsoft Support, "Link a chart title, label, or text box to a worksheet cell").
- Editing the title directly on the chart breaks the link; repeat the steps to restore it (same page, as read in a search result).
- For slicer-driven titles, the cell reads a value the slicer changes, for example a pivot cell or a `GETPIVOTDATA` result.
**Example:** B1 = Sales, B2 = 0.112, B3 = FY26.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Department | Sales |
| 2 | Attrition | 11.2% |
| 3 | Year | FY26 |
| 4 | Title cell | formula |

**Formula / Steps:** B4 `=B1&" attrition, "&B3&": "&TEXT(B2,"0.0%")&" vs target 10.0%"`. Then click the chart title > type `=` > click B4 > Enter (not run here).
**Alternative:** A text box linked to a cell (same page): Insert > Text Box, select it, type `=` in the formula bar, click the cell.
**Result:** Run in LibreOffice: B4 = "Sales attrition, FY26: 11.2% vs target 10.0%".
**Version note:** Linking works in Excel 2016 to 365. It does not work for maps, treemap, sunburst, histogram, Pareto, box and whisker, waterfall and funnel charts (Microsoft Support, same page). Google Sheets chart titles cannot be a formula; use a title in a cell above the chart (from memory, unverified).
**Edge cases:** A chart must already have a title before you can link it. A link to a text that exceeds the chart width wraps oddly. Long title formulas over 255 characters can fail (from memory, unverified).
**Likely follow-ups:** 1) *Can it show the selected slicer item?* Yes, via a formula reading a pivot cell. 2) *Which chart types cannot do it?* The new statistic charts listed above.
**Common mistakes:** Typing text into the title after linking; forgetting TEXT, so percentages show as 0.112.

### Q30 ⭐⭐ 🟡 How do you make a chart change when the user picks an option from a dropdown list?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you combine data validation, a lookup helper range and a chart, without VBA?
**Say this in the interview:** "I create a dropdown with Data Validation, then build a helper column that pulls the chosen department's numbers with INDEX and MATCH. The chart points at that helper column, so it redraws when the dropdown changes."
**Explain simply:**
- **Data Validation list** = a cell that only accepts items from a list, shown as a dropdown.
- **Helper range** = a small block of formulas, next to the data, just for feeding the chart.
- MATCH finds which column the chosen department sits in; INDEX returns the value from that column for each month.
**Example:** Leavers by month for Sales, Ops and HR; the user picks Ops.
**Sample sheet:**

| | A | B | C | D | F | G | I | J |
|---|---|---|---|---|---|---|---|---|
| 1 | Month | Sales | Ops | HR | Pick department | Ops (dropdown) | Month | helper |
| 2 | Jan | 4 | 3 | 1 | Chart column | | Jan | |
| 3 | Feb | 6 | 2 | 0 | | | Feb | |
| 4 | Mar | 5 | 4 | 2 | | | Mar | |
| 5 | Apr | 7 | 3 | 1 | | | Apr | |

**Formula / Steps:** G1: Data > Data Tools > Data Validation > Allow: List > Source `=$B$1:$D$1`. G2 `=MATCH(G1,B1:D1,0)`; J1 `=G1`; J2 `=INDEX($B2:$D2,$G$2)` filled to J5. Chart (not run here): select I1:J5 > Insert > Line chart; the series name J1 is the title.
**Alternative:** `=INDEX($B$2:$D$5,ROW()-1,MATCH($G$1,$B$1:$D$1,0))`; or a pivot chart with a slicer (Q7); or a form control (Q50).
**Result:** Run in LibreOffice with Ops chosen: G2 = 2; J1 = "Ops"; J2:J5 = 3, 2, 4, 3. The dropdown and chart redraw are not run here.
**Version note:** Data Validation, INDEX and MATCH work in Excel 2016 to 365. Google Sheets has Data > Data validation with the same idea (from memory, unverified).
**Edge cases:** A misspelt item gives #N/A, which a line chart skips or errors on. Dropdown source from a Table column grows automatically.
**Likely follow-ups:** 1) *Multiple selections?* Not with a plain dropdown; use slicers. 2) *Why not VLOOKUP?* It can, but INDEX/MATCH looks across the headers easily.
**Common mistakes:** Pointing the chart at the raw table instead of the helper; hard-coding the column number.

### Q31 ⭐⭐ 🟡 How do you handle blank cells and gaps in a line chart?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the Hidden and Empty Cells setting and the difference between a truly blank cell and #N/A or an empty-text formula?
**Say this in the interview:** "By default blanks show as gaps. I can change that under Select Data > Hidden and Empty Cells to Gaps, Zero or Connect data points with line. If a formula produces the blank, I return NA() so the chart skips it instead of drawing a zero."
**Explain simply:**
- Microsoft's path: click the chart > Chart Design (Design) > Select Data > **Hidden and Empty Cells** > Show empty cells as Gaps, Zero or Connect data points with line; the line option is for line, scatter and radar charts (Microsoft Support, "Display empty cells, null (#N/A) values, and hidden worksheet data in a chart").
- The same page offers "Show #N/A as an empty cell" but says it needs a Microsoft 365 subscription and described it as off by default; the page text I read also called it Insiders-only, so check your build.
- A formula returning "" is not blank; charts treat it as text, which usually plots as zero (from memory, unverified).
- Hidden rows or columns are not plotted unless you tick "Show data in hidden rows and columns".
**Example:** March headcount was not reported. Showing 0 would make a false dip; a gap or a connecting line is more honest.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Month | Raw | Helper (NA) | Helper (blank text) |
| 2 | Jan | 510 | | |
| 3 | Feb | 505 | | |
| 4 | Mar | (blank) | | |
| 5 | Apr | 498 | | |
| 6 | May | 502 | | |

**Formula / Steps:** C2 `=IF(B2="",NA(),B2)`; D2 `=IF(B2="","",B2)`; fill down. Chart the Raw or Helper column, then Select Data > Hidden and Empty Cells (not run here).
**Alternative:** Keep raw blanks and choose "Connect data points with line"; or interpolate in a helper column (average of neighbours) and label it as estimated.
**Result:** Run in LibreOffice: C4 = #N/A; D4 shows blank text; `AVERAGE(B2:B6)` = 503.75; `AVERAGE(C2:C6)` = #N/A (one error spoils the average, so keep chart helpers separate from calculations); `COUNT(D2:D6)` = 4. Chart behaviour is not run here.
**Version note:** Hidden and Empty Cells exists in all versions; the #N/A-as-empty option needs Microsoft 365 per the Microsoft page. Google Sheets treats blanks as gaps by default with a "Missing data" option in some chart types (from memory, unverified).
**Edge cases:** A real zero is a value, not a gap. Data labels may show "#N/A" in older versions.
**Likely follow-ups:** 1) *Why not type 0?* It distorts the trend. 2) *Which is best for monthly headcount?* Gap if unknown; line if you trust the interpolation.
**Common mistakes:** Using "" and expecting a gap; letting #N/A flow into KPI formulas.

### Q32 ⭐⭐ 🟡 How do you refresh a dashboard when the source data changes?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that pivots do not update by themselves and that the source range must include new rows?
**Say this in the interview:** "I paste the new data into the source Table so the range grows, then press Data > Refresh All. That refreshes every PivotTable and PivotChart. If the data came through Power Query, Refresh All also reloads the query."
**Explain simply:**
- A **PivotTable** (a summary built from data) keeps a snapshot until you refresh it. Charts based on formulas update immediately; pivots and pivot charts need Refresh.
- Microsoft: select the PivotTable > PivotTable Analyze > Data > Refresh, or Alt+F5; **Refresh All** updates every PivotTable in the workbook (Microsoft Support, "Refresh PivotTable data", from a search snippet).
- Auto refresh for PivotTables on local data exists but was described as limited to Microsoft 365 Insiders when that page was written (same page); do not rely on it.
- If the source is a plain range, new rows below it may be missed; a Table avoids this (Q21).
**Example:** The leavers table lists Sales 4+3, Ops 2+5, HR 1. After two more rows (Sales 6, HR 2) are added, the pivot must be refreshed to show them.
**Sample sheet (pandas, not Excel):**

| Dept | Before refresh | After refresh |
|---|---|---|
| Sales | 7 | 13 |
| Ops | 7 | 7 |
| HR | 1 | 3 |

**Formula / Steps (not run here):**
1. Add new rows directly under the Table (it expands).
2. Data > Refresh All (Ctrl+Alt+F5).
3. Check slicers and the "Last refreshed" cell: type `=NOW()` only if volatile is acceptable, or enter the date manually.
Tip: PivotTable Analyze > Options > Data > tick "Refresh data when opening the file" (from memory, unverified).
**Alternative:** A short macro `ThisWorkbook.RefreshAll` on a button, or Power Query from a folder for new monthly files (Q52).
**Result:** Pandas sums on the sample: before Sales 7, Ops 7, HR 1; after adding the two rows Sales 13, Ops 7, HR 3. The Excel refresh itself is not run here.
**Version note:** Refresh/Refresh All exist in Excel 2016 to 365. Google Sheets pivot tables update automatically (from memory, unverified).
**Edge cases:** Refresh fails or loses formatting if column widths autofit is on (an option: "Autofit column widths on update"); renamed source columns break pivot fields.
**Likely follow-ups:** 1) *Why does my pivot not show new rows?* Source range is not a Table. 2) *Does the slicer refresh?* Yes, with the pivot.
**Common mistakes:** Forgetting to refresh and presenting stale numbers; overwriting the source column headers.

### Q33 ⭐⭐ 🟡 How do you protect a dashboard from accidental edits while keeping slicers usable?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know sheet protection and the specific settings that let users still click slicers?
**Say this in the interview:** "I unlock the slicers, then use Review > Protect Sheet and tick the option to allow PivotTable and PivotChart use. The formulas and layout are locked but the slicers still work. I also keep pivots and data on separate sheets."
**Explain simply:**
- **Protect Sheet** locks all cells that have the Locked property (default on). Objects like slicers are locked too, unless unlocked.
- Microsoft's VBA reference confirms the concept: `AllowUsingPivotTables = True` allows users to use PivotTable reports on a protected worksheet, default False (Microsoft Learn, "Worksheet.Protect method").
- Steps for the interface come from community guides, not a Microsoft Support page: right-click the slicer > Size and Properties > untick Locked; Review > Protect Sheet > tick "Use PivotTable & PivotChart" (from community guides and memory, unverified). Settings for "Select locked cells" vary by guide, so test.
- A password is optional; without one, anyone can unprotect, so it prevents accidents only.
**Example:** A monthly HR MIS file goes to five managers. Dashboard sheet protected; data sheet hidden and workbook structure protected so nobody deletes sheets.
**Formula / Steps (not run here):**
1. Right-click each slicer > Size and Properties > Properties > untick Locked.
2. Review tab > Protect Sheet > leave "Select locked cells" per guide > tick **Use PivotTable & PivotChart** > set a password > OK.
3. Review > Protect Workbook (structure) to stop sheet deletion.
4. Test as a user: click a slicer, then try typing in a cell.
**Alternative:** Save as PDF or "Mark as Final"; distribute through a read-only SharePoint link; or a VBA `Protect ... UserInterfaceOnly:=True` (Microsoft Learn, same page) so macros can still change a protected sheet.
**Result:** Not run here: protection and slicer behaviour cannot be exercised headlessly. The VBA argument and default come from the fetched Microsoft Learn page.
**Version note:** Sheet protection exists in all versions. Google Sheets: Data > Protect sheets and ranges (from memory, unverified).
**Edge cases:** Refreshing a pivot on a protected sheet can fail (from memory, unverified); keep pivots on an unprotected back sheet or refresh by macro. A forgotten password cannot be recovered by Microsoft (Microsoft Learn, same page).
**Likely follow-ups:** 1) *Is it secure?* No, only accident prevention. 2) *Hide formulas?* Format Cells > Protection > Hidden.
**Common mistakes:** Protecting before unlocking the slicers; forgetting the password; thinking protection equals security.

### Q34 ⭐⭐ 🟡 How would you decide between building a dashboard in Excel or in Power BI?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Judgement: can you choose the tool for the situation rather than just defending one?
**Say this in the interview:** "For a one-off or small-data analysis shared with one or two people, Excel is quick. For a recurring report with large data, many viewers, scheduled refresh and row-level access, I would choose Power BI. I often start in Excel, then move once the report gets used regularly."
**Explain simply:**
- **Power BI** = Microsoft's business-intelligence tool for interactive reports published online. **Excel** = flexible spreadsheet for calculation and ad hoc analysis.
- Choose Excel when: data is small (hundreds of thousands of rows at most), you need cell-level maths, the audience is small, or no Power BI licence exists.
- Choose Power BI when: data is large or from many sources, refresh is scheduled, viewers need self-service filtering in a browser, or you need role-based access.
- Common guidance from third-party articles: Excel for ad hoc and small work, Power BI for recurring, shared reporting; one guide gave roughly 100,000 rows as a rule of thumb (third-party blogs from a search, not Microsoft documentation; treat as opinion).
**Example:** Monthly attrition pack for the CHRO and 12 HRBPs, 200,000 rows, each HRBP seeing only their own business unit: Power BI. A quick check of one team's overtime: Excel pivot.
**Formula / Steps:** Decision checklist, no formula: data size, refresh frequency, number of viewers, access control, who maintains it, skills of the team.
**Alternative:** A hybrid: keep Excel for modelling, use Power Query for cleaning, publish visuals to Power BI.
**Result:** No calculation. The 100,000-row figure is an informal third-party rule of thumb, not a verified limit.
**Version note:** Excel's worksheet row limit is 1,048,576 (from memory, unverified). Power BI Desktop is free; sharing in the service needs licences (from memory, unverified). Pivot and Power Query work in Excel 2016 and later.
**Edge cases:** Company policy may block cloud sharing of employee data; then an Excel file on a secured drive may be the only option. Mention data privacy for salary and attrition.
**Likely follow-ups:** 1) *Can Excel refresh automatically?* With Power Query and a macro or scheduled flow. 2) *Which is better for finance models?* Excel.
**Common mistakes:** Saying "Power BI is always better"; ignoring who maintains the file once you leave.

### Q35 ⭐⭐ 🟡 Which chart types are available in Excel 2016, 2019 and Microsoft 365, and which are missing in older versions?
**Asked at:** commonly asked (no company-specific report found); a version-awareness question.
**What the interviewer is checking:** Do you know which modern charts depend on the Excel version, so you do not build something a colleague cannot open?
**Say this in the interview:** "The classic charts (column, bar, line, pie, scatter, area, combo) exist in every modern version. Waterfall, histogram and box and whisker are in 2016 and later (per their Microsoft pages). Funnel needs 2021 or Microsoft 365, and the Map chart needs Microsoft 365. If my audience has an older Excel, I stick to the classics or paste as a picture."
**Explain simply:**
- Classic types listed by Microsoft: column, line, pie and doughnut, bar, area, XY scatter and bubble, stock, surface, radar, combo (Microsoft Support, "Available chart types in Office").
- Newer types on the same page: treemap, sunburst, histogram and Pareto, box and whisker, waterfall, funnel, map (same page).
- Version facts from Microsoft pages I fetched are in the table below.

| Chart | Version evidence |
|---|---|
| Waterfall | Page applies to 2016, 2019, 2021, 2024, 365 (Microsoft Support, "Create a waterfall chart") |
| Histogram | Page applies to 2016, 2019, 2021, 2024, 365 (Microsoft Support, "Create a histogram") |
| Box and whisker | Applies To list includes Excel 2016 and 2019 (Microsoft Support, "Create a box and whisker chart") |
| Pareto | Applies To lists 365, 2024, 2021 only; 2016/2019 not listed (Microsoft Support, "Create a Pareto chart"); the page states no introduction date (only image file names mention 2016), so Excel 2016 availability is unconfirmed |
| Treemap | Applies To lists 365, 2024, 2021 only (Microsoft Support, "Create a treemap chart in Office"); an image caption says "Office 2016 for Windows" but no introduction date is stated, so 2016 availability is unconfirmed |
| Sunburst | Applies To list includes Excel 2016 (Microsoft Support, "Create a sunburst chart in Office"); no introduction date stated |
| Funnel | "only available in Excel for Windows if you have Office 2021, or ... a Microsoft 365 subscription" (Microsoft Support, "Create a funnel chart based on Excel data") |
| Map (filled) | "available if you have a Microsoft 365 subscription" (Microsoft Support, "Create a Map chart in Excel") |
| Dynamic charts | introduced with Office 2024 and in Microsoft 365 (Microsoft Support, "Available chart types in Office") |

- The Part 8 sources file marked funnel and map in Excel 2016 as uncertain. Resolved: per the fetched pages, neither is available in Excel 2016 or 2019 without a Microsoft 365 subscription (funnel arrives with 2021; map is 365 only). A search snippet that mentioned 2019 for funnel was an older copy; the fetched current page says 2021.
**Example:** Your HR team uses Excel 2019 and you built a funnel chart for hiring. They see a blank box. Fix: build the funnel as a stacked bar with a hidden base series, or send a picture.
**Formula / Steps:** Check version: File > Account > About Excel (from memory, unverified). Insert tab > Charts group shows what your version offers. Nothing to calculate; no formulas run.
**Alternative:** Recommended Charts (Insert > Recommended Charts) only suggests chart types your version supports (from memory, unverified).
**Result:** Not applicable (reference answer). Nothing was run; every availability line comes from the fetched pages cited above or is labelled unverified.
**Version note:** Excel 2013 and older lack the 2016 chart group (from memory, unverified). Google Sheets has a different list: the fetched Google page names line, area, column, bar, scatter, pie, waterfall, histogram, radar, candlestick and treemap; geo and gauge are not named there (from memory, unverified).
**Edge cases:** A file with a new chart opened in an older Excel shows an empty placeholder, losing the chart. "Excel 2019" is perpetual; Microsoft 365 receives features monthly, so 2019 gets none later.
**Likely follow-ups:** 1) *How to share safely?* Paste as picture (Q20). 2) *Which new charts can't link titles?* Waterfall, funnel, histogram and similar (Q29).
**Common mistakes:** Assuming everyone has 365; building with a map chart and emailing to a 2019 user.

### Q36 ⭐⭐ 🟡 How do you create charts and a simple dashboard in Google Sheets, and how does it differ from Excel?
**Asked at:** commonly asked (no company-specific report found); relevant for startups and companies using Google Workspace.
**What the interviewer is checking:** Can you work in Sheets as well as Excel and name the main differences?
**Say this in the interview:** "In Sheets I select the data, choose Insert > Chart, and edit it in the chart editor. For interactivity I add slicers from the Data menu, and I build the dashboard on one sheet with pivot tables and charts. Compared with Excel, it is easier to share and collaborate on, but has fewer chart types, no Timeline slicer and weaker handling of big data."
**Explain simply:**
- Google's steps: select the cells, Insert > Chart; double-click to open the editor, where **Setup** has Chart type and Data range and **Customize** has titles, gridlines and fonts (Google Docs Editors Help, "Add & edit a chart or graph").
- Slicers: click the chart or pivot table > Data > Add a slicer > pick a column > set a filter. One slicer per column; slicers affect all charts and pivots on the sheet that use the same data, but not formulas; selections stay private unless saved as default (Google Docs Editors Help, "Filter charts and tables with Slicers").
- Pivot tables update automatically in Sheets; Excel needs Refresh (Q32; Sheets claim from memory, unverified).
- Sheets extras (from memory, unverified): `SPARKLINE`, `QUERY`, `IMPORTRANGE`. Excel strengths: richer chart types, Power Query, VBA, Timeline, more data.
**Example:** HR attendance tracker in Sheets: Data tab, pivot of absences by department, a column chart and a slicer on Month, all on a "Dashboard" tab shared with team leads as view-only.
**Formula / Steps (not run here: Google Sheets cannot run in this environment):**
1. Put clean data on a "Data" tab with headers.
2. Insert > Pivot table (new sheet) > Rows Department, Values Absence days (SUM).
3. Select pivot > Insert > Chart; edit under Setup/Customize.
4. Click the chart > Data > Add a slicer > Month.
5. Move charts to a "Dashboard" tab; View > Show > Gridlines off (from memory, unverified).
**Alternative:** Looker Studio (formerly Data Studio) connecting to the sheet for a fuller dashboard (from memory, unverified).
**Result:** Not applicable. No Sheets action was run here; steps and slicer rules come from the fetched Google pages cited above.
**Version note:** Google Sheets is web-based with no versions. Excel 2016 to 365 comparisons are covered in Q35. Excel formulas such as SUMIFS, INDEX and MATCH work the same way in Sheets; XLOOKUP, FILTER and UNIQUE exist in Sheets as well (from memory, unverified).
**Edge cases:** Large datasets slow down Sheets sooner than Excel; slicer rules require matching ranges when several slicers use the same data (Google Docs Editors Help, as above). Shared link permissions control who sees employee data.
**Likely follow-ups:** 1) *Can Sheets charts link to Slides?* Yes (from memory, unverified). 2) *Offline?* Limited.
**Common mistakes:** Assuming every Excel chart type exists in Sheets; sharing the link with edit rights when view-only is enough.

### Q37 ⭐ 🟢 What is a scatter plot, and how does a bubble chart differ from it?
**Asked at:** ClimbTheLadder's "20 Excel Charts Interview Questions" (undated prep blog) lists scatter vs bubble; no company-specific report found.
**What the interviewer is checking:** Do you know when both axes are numbers, and how a third number is shown?
**Say this in the interview:** "A scatter plot puts one number on the X axis and another on the Y axis to see whether they move together. A bubble chart is a scatter plot where the size of each dot carries a third number."
**Explain simply:**
- Scatter (also called XY chart): each dot is one record, placed by two numbers. It never shows text categories on the horizontal axis (Microsoft Support, "Present your data in a scatter chart or a line chart").
- Use it to spot a relationship, clusters and outliers (unusual points far from the rest).
- Bubble chart: "Bubble size adds a third data dimension" (Microsoft Support, "Present your data in a bubble chart"). Both axes are still numbers.
- Correlation (how tightly two numbers move together, from -1 to +1) is not proof that one causes the other.
**Example:** Experience (years) against salary (lakh) for 6 grades, bubble size = headcount in that grade. Each extra year goes with about 0.95 lakh more pay.
**Sample sheet:**

| | A (Years) | B (Salary, lakh) | C (Headcount) |
|---|---|---|---|
| 1 | Years | Salary | Headcount |
| 2 | 1 | 3.0 | 40 |
| 3 | 2 | 3.6 | 35 |
| 4 | 3 | 4.4 | 28 |
| 5 | 5 | 6.0 | 20 |
| 6 | 7 | 8.1 | 12 |
| 7 | 10 | 11.5 | 5 |

**Formula / Steps:** (Chart click-path: not run here.)
1. Select A1:B7 (X first, Y second). Insert > Charts > Scatter (X, Y) > Scatter.
2. For bubbles, select A2:C7 without headings (the Microsoft page says not to select headings), then Insert > Scatter > Bubble.
3. Numbers behind the chart: `=CORREL(A2:A7,B2:B7)`, `=SLOPE(B2:B7,A2:A7)`, `=INTERCEPT(B2:B7,A2:A7)`, `=RSQ(B2:B7,A2:A7)`.
**Alternative:** Chart Elements > Trendline to draw the best-fit line and show R-squared on the chart.
**Result:** (Run in LibreOffice 24.2, pandas agrees.) CORREL 0.9952, SLOPE 0.9471, INTERCEPT 1.6802, RSQ 0.9905.
**Version note:** Scatter page lists Microsoft 365, 2024 and 2021; the bubble page lists the same. Both chart types exist in older versions too, from memory, unverified. Google Sheets has scatter and bubble charts, from memory, unverified.
**Edge cases:** Blank or text cells in the X column can make Excel treat X as 1,2,3...; the bubble page asks for at least four rows or columns of data; very different bubble sizes hide small ones.
**Likely follow-ups:** 1) *Scatter vs line?* Line spaces categories evenly; scatter places real numeric values. 2) *What does R-squared mean?* Share of the Y movement the line explains (0.99 = 99%).
**Common mistakes:** Selecting the heading row; using a scatter for months; reading correlation as cause.

### Q38 ⭐ 🟢 What are error bars, and when would you use them?
**Asked at:** ClimbTheLadder's Excel charts question list (undated prep blog) includes error bars; no company-specific report found.
**What the interviewer is checking:** Do you understand that an average has uncertainty, and can you show it honestly?
**Say this in the interview:** "Error bars are small whiskers on a chart point that show how uncertain or spread out the value is, for example the standard deviation around an average. I use them when I am showing averages from small samples."
**Explain simply:**
- An error bar shows the margin around a value: standard error, percentage, standard deviation, or custom values (Microsoft Support, "Add, change, or remove error bars in a chart").
- Standard deviation = how spread out the numbers are. Standard error = standard deviation divided by the square root of the count; it shows how precisely the average is known.
- Supported on 2-D area, bar, column, line, scatter and bubble charts (same page).
- A long bar means "do not over-read this difference".
**Example:** Days to fill a role, six months: 22, 24, 19, 26, 21, 25. Average 22.83 days, standard deviation 2.64, standard error 1.08. A bar of plus or minus 2.64 shows the monthly swing.
**Sample sheet:**

| | B | C | D | E | F | G | H (Avg) | I (SD) | J (SE) |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 22 | 24 | 19 | 26 | 21 | 25 | 22.83 | 2.64 | 1.08 |

**Formula / Steps:** (Chart steps: not run here.)
1. Click the chart > Chart Elements (+) > tick Error Bars > arrow > Standard Deviation, or More Options > Custom > Specify Value and pick I2.
2. Numbers: `=AVERAGE(B2:G2)`, `=STDEV.S(B2:G2)`, `=I2/SQRT(COUNT(B2:G2))`.
**Alternative:** A fixed percentage bar, e.g. 10% (`=H2*0.1` = 2.28), when you only want a rough tolerance.
**Result:** (Run.) 22.83, 2.64, 1.08, 2.28.
**Version note:** Page applies to 365, 2024, 2021, 2019 and 2016 (Microsoft Support). Google Sheets has error bars in the chart editor's Series section, from memory, unverified.
**Edge cases:** Standard deviation of one value is an error; use STDEV.S (sample) not STDEV.P unless you hold the whole population.
**Likely follow-ups:** 1) *SD vs SE?* Spread of data vs precision of the average. 2) *Horizontal bars?* Only scatter and bubble charts.
**Common mistakes:** Adding them without saying which type; hiding wide bars.

### Q39 ⭐ 🟢 Why can a chart whose value axis does not start at zero be misleading?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you present data honestly?
**Say this in the interview:** "Bars encode value by length. If the axis starts at 90, a bar of 100 looks far taller than a bar of 96 even though the real gap is 4%. For bar charts I start at zero."
**Explain simply:**
- The eye compares bar heights, not the axis labels.
- A cut axis exaggerates small differences; this can sway a leadership decision.
- Line charts show change over time, so a non-zero start is more acceptable, but label it clearly.
- Excel auto-picks the minimum, so check it: Format Axis > Axis Options > Minimum (Microsoft Support, "Change the scale of the vertical (value) axis in a chart").
**Example:** Team size grew from 96 to 100, a real rise of 4.2%. With the axis starting at 90, the Q2 bar is 10 units tall against 6 for Q1, so it looks 67% taller.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Q1 | 96 |
| 2 | Q2 | 100 |

**Formula / Steps:** Real change `=B2/B1-1`; apparent change with axis at 90 `=(B2-90)/(B1-90)-1`. Fix: click the value axis > Format Axis > Minimum = 0 (not run here).
**Alternative:** Show the change as a number label ("+4.2%") or use a line chart with a clear axis note.
**Result:** (Run.) 0.0417 (4.2%) vs 0.6667 (66.7%); ratio at zero base 1.0417.
**Version note:** Axis page lists 365, 2024 and 2021; the Format Axis pane exists in earlier versions too, from memory, unverified.
**Edge cases:** Data far from zero (e.g. temperatures, indexes) may justify a cut axis; say so on the chart.
**Likely follow-ups:** 1) *Is it ever fine?* On line charts, labelled. 2) *Dual axes?* Also easy to mislead.
**Common mistakes:** Accepting Excel's auto minimum; cutting the axis to make a small gain look big.

### Q40 ⭐ 🟢 What are Recommended Charts and Quick Analysis in Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the fast, built-in routes to a first chart?
**Say this in the interview:** "Both suggest charts that suit my selected data. Recommended Charts is on the Insert tab with a preview of each option; Quick Analysis is the small icon at the bottom-right of a selection. I use them to get a first draft, then format it."
**Explain simply:**
- Recommended Charts: Excel looks at your data layout and offers matching chart types with previews.
- Quick Analysis: a pop-up near the selection (Ctrl+Q) with tabs for Formatting, Charts, Totals, Tables and Sparklines (from memory, unverified).
- Alt+F1 drops in a default chart at once, which "may not be the best chart for the data" (Microsoft Support, "Create a chart from start to finish").
- If nothing fits, open the All Charts tab.
**Example:** Select a 12-month attrition table (months and %), Insert > Recommended Charts: Excel proposes a line or column chart; you pick the line.
**Formula / Steps:** (Not run here.) Select the data > Insert > Recommended Charts > click a preview > OK (Microsoft Support). Or select data > Quick Analysis icon > Charts tab > hover to preview.
**Alternative:** Insert > a specific chart group (Column, Line...), or Alt+F1.
**Version note:** Recommended Charts page applies to 365, 2024, 2021, 2019 and 2016 (Microsoft Support). The same page does not mention Quick Analysis; it arrived in Excel 2013, from memory, unverified. Google Sheets has "Explore" suggestions, from memory, unverified.
**Edge cases:** Headers in row 1 and no blank rows give better suggestions; merged cells confuse it.
**Likely follow-ups:** 1) *Do you trust the suggestion?* I check axis, labels and fit for the message. 2) *Fastest chart?* Alt+F1.
**Common mistakes:** Accepting the first suggestion without checking the story it tells.

### Q41 ⭐ 🟢 How do you group small categories into an Other slice or bar in a chart?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you cut clutter without losing the total?
**Say this in the interview:** "I add the small categories into one 'Other' row, either with a helper formula or by grouping items in the PivotTable, so the chart shows the few that matter and the total still adds up."
**Explain simply:**
- A threshold rule (for example under 5% of the total) decides who goes into Other.
- Helper column: a formula labels each row either with its own name or "Other"; then you chart a PivotTable of that column.
- PivotTable route: Ctrl+click two or more items, right-click > Group, then rename the group (Analyze > Field Settings > Custom Name) (Microsoft Support, "Group or ungroup data in a PivotTable").
- Say what Other contains (a footnote).
**Example:** 1,000 employees. HR (40), Legal (18), Admin (12), Fin (8), CSR (2) are each under 5%; together they are 80, or 8%.
**Sample sheet:**

| | A (Dept) | B (HC) | C (Group) |
|---|---|---|---|
| 2 | Sales | 420 | Sales |
| 3 | IT | 310 | IT |
| 4 | Ops | 190 | Ops |
| 5 | HR | 40 | Other |
| 6 | Legal | 18 | Other |
| 7 | Admin | 12 | Other |
| 8 | Fin | 8 | Other |
| 9 | CSR | 2 | Other |

**Formula / Steps:** C2: `=IF(B2/SUM($B$2:$B$9)<0.05,"Other",A2)`, copy down. Other total: `=SUMIF(C2:C9,"Other",B2:B9)`. Then Insert > PivotChart on column C (not run here).
**Alternative:** Group items in the PivotTable by Ctrl+click and Group (steps above, not run here).
**Result:** (Run.) Other = 80; total 1,000; Other share 8%. Chart slices: Sales 420, IT 310, Ops 190, Other 80.
**Version note:** Grouping page applies to 365, 2024, 2021, 2019 and 2016 (Microsoft Support). Google Sheets pivot tables can group manually too, from memory, unverified.
**Edge cases:** Do not hide a rare but important category (e.g. a compliance team); zero totals divide by zero.
**Likely follow-ups:** 1) *Why not a pie?* With few categories a sorted bar is clearer. 2) *Threshold?* Decide by audience.
**Common mistakes:** Letting Other be the biggest slice; deleting the small rows and breaking the total.

### Q42 ⭐ 🟢 How do you save a formatted chart as a template and reuse it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you work efficiently and keep a consistent look?
**Say this in the interview:** "I format one chart to the company style, right-click it, Save as Template, and then insert new charts from that template so every dashboard matches."
**Explain simply:**
- A chart template keeps the chart's formatting and the colours in use when saved (Microsoft Support, "Save a custom chart as a template").
- It is a .crtx file in the charts Templates folder.
- It does not store your data, only the look.
- Applying it in another workbook uses the template's colours, not the new workbook's theme (Microsoft Support, per a search summary of the older page, not re-verified).
**Example:** Your monthly attrition chart with navy bars, no gridlines and 10pt labels becomes "HR_Standard.crtx"; 12 dashboards now look identical.
**Formula / Steps:** (Not run here; from the fetched page.)
1. Right-click the chart > Save as Template.
2. Type a name in File name > Save.
3. New chart: select data > Insert > Chart (dialog) > Templates (All Charts tab), choose it.
4. Existing chart: Chart Design > Change Chart Type > Templates.
**Alternative:** Copy the formatted chart, paste, and use Select Data to point it at new data.
**Version note:** The fetched page lists Microsoft 365, 2024 and 2021 (Windows and Mac). Chart templates also exist in 2016 and 2019, from memory, unverified.
**Edge cases:** Different chart types need different templates; a template made from a combo chart creates a combo chart.
**Likely follow-ups:** 1) *Share it?* Send the .crtx file. 2) *Where is it?* Templates folder, shown under All Charts > Templates.
**Common mistakes:** Expecting the data to come along; forgetting to tick the chart type before saving.

### Q43 ⭐ 🟡 How do you build a hiring funnel chart, from applications to offers to joiners?
**Asked at:** commonly asked (no company-specific report found); HR scenario added from standard practice.
**What the interviewer is checking:** Can you show stage-by-stage drop-off and compute conversion rates correctly?
**Say this in the interview:** "I list the stages in order with their counts, calculate each stage's conversion from the previous one, and chart them. The built-in Funnel chart needs Excel 2021 or 365; in older versions I build it with a stacked bar."
**Explain simply:**
- A funnel chart is a set of bars that shrink down the stages.
- Conversion rate = this stage divided by the previous stage. Overall yield = joiners divided by applications.
- Microsoft's page: Funnel requires Office 2021 or a Microsoft 365 subscription (Microsoft Support, "Create a funnel chart based on Excel data").
- Without Funnel: a stacked bar with a hidden spacer series centres each bar.
**Example:** 1,200 applications, 600 screened, 240 interviewed, 60 offers, 45 joiners. The weakest conversion is interview to offer (25%). Offer acceptance is 75%.
**Sample sheet:**

| | A (Stage) | B (Count) | C (Conv.) | D (Spacer) |
|---|---|---|---|---|
| 2 | Applications | 1200 | | 0 |
| 3 | Screened | 600 | 50% | 300 |
| 4 | Interviewed | 240 | 40% | 480 |
| 5 | Offers | 60 | 25% | 570 |
| 6 | Joiners | 45 | 75% | 577.5 |

**Formula / Steps:** C3: `=B3/B2` (copy to C6). D2: `=(MAX($B$2:$B$6)-B2)/2` (copy down). Overall: `=B6/B2`.
Funnel: select A1:B6 > Insert > Waterfall, Funnel, Stock, Surface or Radar chart > Funnel (not run here).
**Alternative:** Select A1:B6 plus D, Insert > Stacked Bar, Format the spacer series No Fill, set Categories in reverse order (not run here; same technique as the Gantt page).
**Result:** (Run.) Conversions 50%, 40%, 25%, 75%; spacer 0, 300, 480, 570, 577.5; overall 3.75%.
**Version note:** Fetched page: Windows requires 2021 or 365; Mac 2021, 2024 or 365. Excel 2016 and 2019 are not listed, so use the stacked bar. (An earlier search summary mentioned 2019; the fetched page governs.) Google Sheets has no native funnel chart, from memory, unverified.
**Edge cases:** Stages must be sorted largest to smallest; a stage with no data breaks the conversion (use IFERROR).
**Likely follow-ups:** 1) *Where is the leak?* Lowest conversion, interview to offer. 2) *Time to fill?* Needs dates, a separate metric.
**Common mistakes:** Dividing by applications at every stage and calling it conversion.

### Q44 ⭐ 🟡 How do you show salary distribution by grade using a box and whisker chart?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand quartiles, medians and outliers?
**Say this in the interview:** "A box plot shows the middle half of salaries as a box, the median as a line, and flags unusual salaries as dots. I select salaries by grade and use Insert > Statistic Chart > Box and Whisker."
**Explain simply:**
- Median = the middle value. Quartiles split sorted data into four equal parts; the box runs from the 1st to 3rd quartile.
- IQR (interquartile range) = Q3 minus Q1. A common whisker rule: points beyond 1.5 x IQR from the box are outliers.
- The page's options: show inner points, outlier points, mean markers, mean line and a Quartile Calculation of inclusive or exclusive median (Microsoft Support, "Create a box and whisker chart").
- The chart needs a column per grade (or a Grade column and a Salary column).
**Example:** One grade, 8 salaries (lakh): 4.2, 4.8, 5.0, 5.5, 6.1, 6.4, 7.0, 15.0. The 15.0 pay is an outlier and drags the mean to 6.75 above the median of 5.8.
**Sample sheet (no header row, so cell numbers match the formulas):**

| | A (Salary) | C | D (Inclusive) | E (Exclusive) |
|---|---|---|---|---|
| 1 | 4.2 | Q1 | 4.95 | 4.85 |
| 2 | 4.8 | Median | 5.8 | 5.8 |
| 3 | 5.0 | Q3 | 6.55 | 6.85 |
| 4 | 5.5 | | | |
| 5 | 6.1 | | | |
| 6 | 6.4 | | | |
| 7 | 7.0 | | | |
| 8 | 15.0 | | | |

**Formula / Steps:** `=QUARTILE.INC(A1:A8,1)`, `=MEDIAN(A1:A8)`, `=QUARTILE.INC(A1:A8,3)`; `=QUARTILE.EXC(...)` for the exclusive method; upper fence `=D3+1.5*(D3-D1)` (inclusive column).
Chart (not run here): select the data > Insert > Insert Statistic Chart > Box and Whisker; right-click a box > Format Data Series to show outliers and the mean.
**Alternative:** Show median, Q1, Q3 in a PivotTable and a stacked-column "pseudo box" (not run here).
**Result:** (Run; QUARTILE.EXC needs the _xlfn. prefix when written through openpyxl.) INC: 4.95, 5.8, 6.55, IQR 1.6, upper fence 8.95, lower fence 2.55, mean 6.75; EXC: 4.85, 5.8, 6.85. So 15.0 is above the fence (outlier); the top whisker ends at 7.0 and the bottom at 4.2 (read off the data). Chart's exact quartile maths: not run here.
**Version note:** Page applies to 365, 2024, 2021, 2019 and 2016 (Microsoft Support). Google Sheets has no native box plot, only a candlestick workaround, from memory, unverified. Microsoft's box and whisker page (fetched) defines Inclusive/Exclusive median only as whether the median is included in the quartile calculation when N is odd; it does not say they equal QUARTILE.INC or QUARTILE.EXC, so which numbers the chart draws for N = 8 is unverified.
**Edge cases:** Small groups (under 5 people) make meaningless boxes; blanks are ignored.
**Likely follow-ups:** 1) *Why median over mean?* Outliers distort the mean. 2) *Pay compression?* Boxes of adjacent grades overlap.
**Common mistakes:** Calling the whisker the min and max; confusing quartile methods.

### Q45 ⭐ 🟡 How do you create a map chart of employees by state, and what are its requirements?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you summarise by location and know the tool's limits?
**Say this in the interview:** "I count employees per state, mark the state column as a Geography data type, then Insert > Maps > Filled Map. It needs a Microsoft 365 subscription and an internet connection to create."
**Explain simply:**
- Filled map = each region shaded by its value; darker means more employees.
- Excel reads place names through the Geography data type (Data tab > Data Types > Geography).
- Per Microsoft: only high-level places (country, state, county, city, postcode); no latitude/longitude or street addresses; one value per region; creating or extending needs an online connection (Bing Map service) (Microsoft Support, "Create a Map chart in Excel").
- Ambiguous names: put each level in its own column, for example State and Country.
**Example:** Seven employees across four states, shaded: Telangana 3, Karnataka 2, Maharashtra 1, Tamil Nadu 1.
**Sample sheet:**

| | A (State per employee) | C (State) | D (Employees) |
|---|---|---|---|
| 2 | Telangana | Telangana | 3 |
| 3 | Karnataka | Karnataka | 2 |
| 4 | Telangana | Maharashtra | 1 |
| 5 | Maharashtra | Tamil Nadu | 1 |
| 6-8 | Karnataka, Telangana, Tamil Nadu | | |

**Formula / Steps:** D2: `=COUNTIF($A$2:$A$8,C2)`, copy down.
Chart (not run here): select C2:C5 > Data > Data Types > Geography > click any cell in C1:D5 > Insert > Charts > Maps > Filled Map > OK.
**Alternative:** A sorted bar chart of employees by state (safer and works in every version), or 3D Maps for multi-dimensional data (Microsoft's page).
**Result:** (Run.) Telangana 3, Karnataka 2, Maharashtra 1, Tamil Nadu 1. Map rendering: not run here.
**Version note:** Fetched page applies to Microsoft 365 (Windows, Mac, mobile) and requires a subscription; it does not list Excel 2016, 2019 or 2021. Google Sheets has a geo chart, from memory, unverified. Whether every Indian state name resolves cleanly is unverified.
**Edge cases:** Misspelt states; mixing "Telangana" and "TS"; counts hide very small states.
**Likely follow-ups:** 1) *Works offline?* Existing maps can be viewed, new ones need internet. 2) *Per city?* Yes if cities are supported; ambiguous ones need a state column.
**Common mistakes:** Using Pincode plus area text; expecting coordinates to work.

### Q46 ⭐ 🟡 What is the difference between a dynamic chart range built with OFFSET and one built with an Excel Table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the modern, safe way to make charts grow with data?
**Say this in the interview:** "Both make the chart grow when I add rows. OFFSET uses a named formula that counts the rows; a Table expands by itself. I prefer a Table because it is simpler and not volatile."
**Explain simply:**
- Excel Table (Ctrl+T): add a row below and the table, and any chart based on it, extends automatically.
- OFFSET named range: a Name Manager formula that starts at the first cell and sizes itself by COUNTA of the labels.
- OFFSET is volatile, meaning it recalculates on every change, and it breaks if blanks appear in the label column.
- OFFSET names go into the chart's Select Data > Series values as `'Book.xlsx'!Name` (from memory, not run here).
**Example:** Monthly headcount 100, 104, 98, 110. Adding M5 = 115 should raise the total from 412 to 527.
**Sample sheet:**

| | A | B | D |
|---|---|---|---|
| 1 | Month | HC | |
| 2 | M1 | 100 | |
| 3 | M2 | 104 | |
| 4 | M3 | 98 | |
| 5 | M4 | 110 | |
| 6 | M5 (new) | 115 | |

**Formula / Steps:** Name Manager name `HC_Range` refers to `=OFFSET($B$2,0,0,COUNTA($A:$A)-1,1)`. Table route: select A1:B5 > Insert > Table, then build the chart from the table.
**Alternative:** `=SUM(OFFSET($B$2,0,0,COUNTA($A:$A)-1,1))` to test the range.
**Result:** (Run.) With 4 rows the OFFSET sum is 412; after adding M5 it is 527 and COUNTA(A:A)-1 = 5. Chart growth itself: not run here.
**Version note:** Tables and OFFSET work in all modern Excel versions, from memory, unverified. Google Sheets has no Tables for charts of this kind; open-ended ranges like B2:B work, from memory, unverified.
**Edge cases:** Blanks inside the data; text in the label column; whole-column COUNTA also counts the header or notes.
**Likely follow-ups:** 1) *Why avoid OFFSET?* Volatile, harder to audit. 2) *Pivot charts?* Refresh instead.
**Common mistakes:** Forgetting the "-1" for the header; building the chart on A1:B5 instead of the table.

### Q47 ⭐ 🟡 How do you colour bars red when they fall below target and green when they meet it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you make conditional formatting for charts, which Excel has no direct switch for?
**Say this in the interview:** "Charts do not support conditional formatting, so I split the values into two helper columns, Met and Missed, and plot both as one overlapped series each, coloured green and red."
**Explain simply:**
- Helper column "Met" shows the value if it reaches target, otherwise #N/A (an error Excel charts skip).
- "Missed" is the opposite.
- Plot both columns, set Series Overlap to 100% so they sit in the same slot, and colour one green, one red.
- It updates automatically when the actual changes.
**Example:** Monthly training completion against an 85% target.
**Sample sheet:**

| | A (Dept) | B (Actual) | C (Target) | D (Met) | E (Missed) |
|---|---|---|---|---|---|
| 2 | A | 92 | 85 | 92 | #N/A |
| 3 | B | 78 | 85 | #N/A | 78 |
| 4 | C | 85 | 85 | 85 | #N/A |
| 5 | D | 60 | 85 | #N/A | 60 |

**Formula / Steps:** D2: `=IF(B2>=C2,B2,NA())`, E2: `=IF(B2<C2,B2,NA())`, copy down. Select A1:A5 and D1:E5 > Insert > Clustered Column; right-click a bar > Format Data Series > Series Overlap 100% (not run here).
**Alternative:** Plot variance (Actual minus Target) as columns with "Invert if negative" and two fill colours (from memory, not run here); or colour single bars by hand (not dynamic).
**Result:** (Run.) Met: 92, #N/A, 85, #N/A. Missed: #N/A, 78, #N/A, 60.
**Version note:** Works in all versions, from memory, unverified. Google Sheets has conditional colour only via helper series, from memory, unverified.
**Edge cases:** Exactly on target (C = 85) counts as met because of `>=`; #N/A in a line chart creates gaps or connects points depending on settings.
**Likely follow-ups:** 1) *Why #N/A not 0?* Zero draws a zero-height bar and may show a label "0". 2) *Amber band?* Add a third column.
**Common mistakes:** Forgetting overlap 100%, leaving bars half-width and offset.

### Q48 ⭐ 🟡 How do you create a Gantt chart for a project plan in Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you bend a standard chart into a timeline?
**Say this in the interview:** "Excel has no Gantt type, so I use a stacked bar chart: the first series is the start date made invisible, the second is the duration."
**Explain simply:**
- Dates are numbers in Excel; the start is plotted as an invisible bar that pushes the visible duration bar to the right place.
- Duration = End minus Start (add 1 if both days count).
- The task list needs "Categories in reverse order" so the first task is at the top.
- Microsoft: "Excel doesn't have a predefined Gantt chart type" (Microsoft Support, "Present your data in a Gantt chart in Excel").
**Example:** A 4-task HR system rollout from 2 Nov 2026 to 8 Dec 2026, spanning 37 days.
**Sample sheet:**

| | A (Task) | B (Start) | C (End) | D (Duration) |
|---|---|---|---|---|
| 2 | Plan | 02-Nov | 06-Nov | 5 |
| 3 | Build | 09-Nov | 27-Nov | 19 |
| 4 | Test | 23-Nov | 04-Dec | 12 |
| 5 | Launch | 07-Dec | 08-Dec | 2 |

**Formula / Steps:** D2: `=C2-B2+1` (copy down). Chart (from the fetched page, not run here):
1. Select the data > Insert > Recommended Charts > Stacked Bar.
2. Click the Start series > Format > Shape Fill > No Fill.
3. Delete the legend and title if not needed.
4. Format Axis on the task axis > Categories in reverse order.
5. Set the date axis Minimum to the start serial 46328 (2 Nov 2026).
**Alternative:** Use a free Gantt template (the page links to them) or conditional-formatting cells across a date grid.
**Result:** (Run, LibreOffice date maths.) Durations 5, 19, 12, 2; project span 37 days; offsets from 2 Nov: Build 7, Test 21, Launch 35. Serial 46328 is date arithmetic from the 1899-12-30 base. Chart drawing: not run here.
**Version note:** Page applies to 365, 2024, 2021, 2019 and 2016 (Microsoft Support). Google Sheets needs a similar stacked-bar trick or a template, from memory, unverified.
**Edge cases:** Overlapping tasks (Build and Test overlap 23-27 Nov) are fine; weekends are not excluded unless you use NETWORKDAYS.
**Likely follow-ups:** 1) *Progress bar?* Add a third series for % complete. 2) *Today line?* Add a scatter series.
**Common mistakes:** Plotting End instead of Duration; leaving the axis at 0 so the dates are squashed.

### Q49 ⭐ 🟡 How do you create a gauge or speedometer chart for a KPI?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you build a custom visual, and do you know when not to?
**Say this in the interview:** "Excel has no gauge chart. I make one by combining a half-hidden doughnut for the coloured bands with a pie for the needle. It looks nice but I prefer a bullet bar for accuracy."
**Explain simply:**
- Doughnut: bands (e.g. red 50, amber 30, green 20) plus a hidden half of 100 so only a half-circle shows.
- Pie (needle): three slices, KPI value, a thin needle width, and the remainder; the slices must add to twice the maximum so only half the circle is used.
- Rotate both to start at 270 degrees; set the needle pie on the secondary axis; fill only the needle slice.
- Gauges take lots of space for a single number.
**Example:** Attrition-control score 72 out of 100: the needle covers 72 to 74 on the dial.
**Sample sheet:**

| | A | B | D (Needle) | F (Bands) |
|---|---|---|---|---|
| 1 | KPI | 72 | | |
| 2 | Max | 100 | 72 | 50 |
| 3 | | | 2 | 30 |
| 4 | | | 126 | 20 |
| 5 | | | 200 | 100 |

**Formula / Steps:** D2 `=B1`, D3 2 (needle width), D4 `=2*B2-D2-D3`, D5 `=SUM(D2:D4)`. Chart: (not run here) Insert > Doughnut with F2:F4 plus a 100 slice; add the needle series as Pie on the secondary axis; First slice angle 270; hide the unused slices.
**Alternative:** A bullet chart (bar plus target marker) or a single KPI card with a coloured arrow.
**Result:** (Run.) Needle data sums to 200 = 2 x max; bands sum to 100 (50+30+20). Visual: not run here.
**Version note:** Works in all versions, from memory, unverified. Google Sheets has a built-in gauge chart, from memory, unverified.
**Edge cases:** Needle width shifts the reading by half its width; values above max produce a negative remainder.
**Likely follow-ups:** 1) *Better option?* Bullet chart or card. 2) *Dynamic?* Yes, formula-driven.
**Common mistakes:** Forgetting the hidden half; mis-sized remainder.

### Q50 ⭐ 🟡 How do you use form controls such as a scroll bar or option buttons to make a chart interactive?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you add interactivity without macros?
**Say this in the interview:** "I insert a form control from the Developer tab and link it to a cell. The control writes a number into that cell, and formulas like INDEX use it to pull the data the chart plots."
**Explain simply:**
- Form controls: scroll bar, spin button, list box, combo box, option buttons.
- Cell link = the cell that receives the control's number. Dynamic chart data reads it with INDEX or OFFSET (Microsoft Support, "How to use the forms controls on a worksheet in Excel").
- Scroll bar and spin button settings: Current value, Minimum, Maximum, Incremental change; scroll bar also has Page change (same page).
- Option buttons: choosing one sets the link cell to 1, 2, 3... (from memory; the page does not cover option buttons).
**Example:** Four departments (Sales, IT, HR, Ops). Set the scroll bar to min 1, max 4. At value 3 the chart shows HR with attrition 6%.
**Sample sheet:**

| | A (Dept) | B (Attr %) | D |
|---|---|---|---|
| 1 | Dept | Attr% | 3 (link) |
| 2 | Sales | 14 | HR |
| 3 | IT | 9 | 6 |
| 4 | HR | 6 | |
| 5 | Ops | 11 | |

**Formula / Steps:** Enable Developer: File > Options > Customize Ribbon > tick Developer. Developer > Insert > Scroll Bar (Form Control), drag; right-click > Format Control > Min 1, Max 4, Cell link D1. D2 `=INDEX(A2:A5,D1)`, D3 `=INDEX(B2:B5,D1)`. Chart on D2:D3 (chart not run here).
**Alternative:** `=OFFSET(B1,D1,0)`, or a data-validation dropdown (no Developer tab needed).
**Result:** (Run, link value 3.) INDEX returns HR and 6; OFFSET returns 6.
**Version note:** Page applies to Excel 2024, 2021, 2019 and 2016 (Microsoft Support). Controls do not work in Google Sheets; use dropdowns, from memory, unverified.
**Edge cases:** The link cell holds integers only; macros are not needed, but form controls do not work in Excel for the web, from memory, unverified.
**Likely follow-ups:** 1) *Form vs ActiveX?* Form controls are simpler. 2) *Why not a slicer?* Slicers need PivotTables.
**Common mistakes:** Linking to the wrong cell; max value larger than the list.

### Q51 ⭐ 🔴 How would you speed up a dashboard that has become slow with several hundred thousand rows of data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you diagnose heavy calculation and choose a better structure?
**Say this in the interview:** "I first find what is slow: volatile functions, lookups over whole columns, or too many formulas on raw rows. Then I move the heavy work into Power Query and the Data Model, summarise with PivotTables, and keep the dashboard sheet light."
**Explain simply:**
- Fewer row-level formulas: replace per-row VLOOKUP/SUMIFS with a merge in Power Query or a Data Model relationship.
- Power Query: loading and transforming the data once is faster than formulas recalculating; it is built into all Excel 2016 or later Windows versions (Microsoft Support, "Power Query data sources in Excel versions").
- Avoid volatile functions (OFFSET, INDIRECT, TODAY) and whole-column references; set calculation to Manual while editing.
- Cut columns and rows you do not need; save as .xlsx or .xlsb (xlsb tip from memory, unverified).
**Example:** 500,000 rows. One SUMIFS over the data scans 500,000 rows; 50 summary cells means 25,000,000 row tests per recalculation. A SUMIFS in every row (helper column) would be 500,000 x 500,000 = 250 billion tests; a PivotTable does one pass.
**Formula / Steps:** (Not run here.) Data > Get Data > From Table/Range (or From File) > Load To > Only Create Connection + Add to Data Model; then Insert > PivotTable > Data Model. Formulas > Calculation Options > Manual while building.
**Alternative:** Move to Power BI for millions of rows.
**Result:** (Run, arithmetic.) 500,000 x 50 = 25,000,000; 500,000 x 500,000 = 250,000,000,000. Real timings not measured here.
**Version note:** Power Query: Excel 2016 or later (Windows) and Microsoft 365 (Microsoft Support); connector sets differ by version. Data Model needs Windows editions that include it, from memory, unverified. Google Sheets slows far earlier (about 10 million cells limit), from memory, unverified.
**Edge cases:** Excel rows cap at 1,048,576 (from memory, unverified); 32-bit Excel runs out of memory sooner.
**Likely follow-ups:** 1) *Table or range?* Tables help, formulas still recalc. 2) *When Power BI?* Beyond a few million rows or shared use.
**Common mistakes:** Blaming file size alone; leaving whole-column ranges and volatile formulas.

### Q52 ⭐ 🔴 Design a one-click monthly MIS dashboard that refreshes from new source files, using Power Query, pivots, slicers and a macro.
**Asked at:** commonly asked (no company-specific report found); MIS prep guides (x0pa, snippet-level) list dashboard questions.
**What the interviewer is checking:** Can you design an end-to-end, repeatable, low-error reporting pipeline?
**Say this in the interview:** "Drop the monthly files into one folder. Power Query combines the folder into one clean table, PivotTables and PivotCharts summarise it, slicers filter it, and a single macro button runs Refresh All."
**Explain simply:**
- Data layer: Power Query reads every file in the folder, cleans it, and loads it (Excel 2016 or later: Microsoft Support, "Power Query data sources in Excel versions").
- Calculation layer: PivotTables and measures on the combined data.
- Presentation layer: PivotCharts, KPI cards, slicers and a Timeline connected through Report Connections (Microsoft Support, "Create and share a dashboard with Excel and Microsoft Groups").
- Macro: a button that runs RefreshAll. A macro is a saved set of steps; the file must be .xlsm.
**Example:** Three monthly hiring files total 10 rows. Refresh gives Sales 11, IT 11, HR 4, Ops 3, total 29 hires.
**Sample sheet:** Jan: Sales 5, IT 3, HR 1, Sales 2. Feb: Sales 4, IT 2, HR 2. Mar: IT 6, HR 1, Ops 3.
**Formula / Steps:** (Not run here: Power Query, pivots, slicers, VBA.)
1. Data > Get Data > From File > From Folder > pick folder > Combine & Transform (path from memory; verify on your version).
2. Clean (types, headers) > Close & Load To > Table or Data Model.
3. Insert PivotTable and PivotCharts; add slicers and Timeline.
4. Alt+F11, in a module:
```
Sub RefreshMIS()
    ThisWorkbook.RefreshAll
End Sub
```
5. Developer > Insert > Button > assign RefreshMIS. Turn off background refresh in the query properties so the macro waits (from memory).
**Alternative:** No macro: Data > Refresh All (Ctrl+Alt+F5), or Power Automate/Task Scheduler.
**Result:** (pandas, run.) Combined 10 rows; pivot totals Sales 11, IT 11, HR 4, Ops 3, all 29. Dashboard and macro: not run here.
**Version note:** Power Query built in for 2016+ Windows (Microsoft Support); the macro needs desktop Excel; Google Sheets would use Apps Script, from memory, unverified.
**Edge cases:** Files with different column names or an added header row break the combine; password files need handling; macros are blocked in some company policies.
**Likely follow-ups:** 1) *New month's file?* Drop in the folder, refresh. 2) *Errors?* Add a row-count check cell.
**Common mistakes:** Hardcoding file names; pasting values over the pivots; forgetting to refresh pivots after the query.

### Q53 ⭐ 🔴 You are shown a cluttered dashboard with 3D pie charts and 15 KPIs. How would you critique and redesign it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Design judgement and the ability to give constructive criticism.
**Say this in the interview:** "I would ask who uses it and what decision it supports, then remove the 3D effect, cut to the few KPIs that drive action, use simple sorted bars and lines, and group the rest on a drill-down page."
**Explain simply:**
- 3D distorts: the front slice looks bigger and the back smaller; a flat sorted bar compares better.
- 15 KPIs mean no priority. Keep about 5, put the headline KPIs top-left, and move the rest to a detail tab.
- One consistent colour set, meaning-based colour (red only for bad), no gridline clutter, clear titles that state the message.
- Hide gridlines and headings for a clean sheet (View tab) (Microsoft Support, "Create and share a dashboard with Excel and Microsoft Groups").
**Example:** Original: 15 KPIs + 3D pie of 5 departments (35%, 25%, 20%, 12%, 8%). Redesign: 5 KPIs (headcount, attrition %, time to fill, offer acceptance, absenteeism), a sorted bar of those department shares, a 12-month attrition line, and 2 slicers (department, month).
**Formula / Steps:** (Not run here.) Click a chart > Chart Design > Change Chart Type > Bar; remove 3D; View > untick Gridlines and Headings; Insert > Slicer.
**Alternative:** Wireframe on paper first, then build.
**Result:** 15 KPIs to 5 (a two-thirds cut); the five shares sum to 100% (35+25+20+12+8, hand check).
**Version note:** No version dependence beyond slicer availability on PivotTables (Microsoft Support dashboard page, 2016 to 365). Google Sheets has slicers, from memory, unverified.
**Edge cases:** Leaders may insist on a favourite KPI; keep it, but justify its position.
**Likely follow-ups:** 1) *Colour use?* Limited palette, red only for off-target. 2) *How many KPIs?* About 5 on the front page.
**Common mistakes:** Criticising without asking the audience; removing information instead of moving it.

### Q54 ⭐ 🔴 How would you present an Excel dashboard to non-technical senior leaders and handle conflicting requests from different stakeholders?
**Asked at:** commonly asked (no company-specific report found); MIS prep guides (x0pa, snippet-level) list a stakeholder-conflict question.
**What the interviewer is checking:** Communication, prioritisation and stakeholder management, not just Excel.
**Say this in the interview:** "I start with the decision they need to make, show the headline in one line, then the trend and the reason, and finish with a recommended action. For conflicting asks I clarify the goals, agree priorities with the sponsor, and offer a drill-down so everyone gets what they need without crowding the main page."
**Explain simply:**
- Structure: headline, evidence (one or two charts), cause, recommendation. Avoid jargon; say "people who left" if "attrition" confuses.
- Test the slicers and numbers before the meeting (the Microsoft dashboard page lists testing as a step: Microsoft Support, "Create and share a dashboard with Excel and Microsoft Groups").
- Conflicts: ask what decision each person is making; have the business sponsor set the priority order; put the extra requests on secondary tabs.
- Write down agreed definitions (for example, how attrition is calculated) so everyone reads the same numbers.
**Example:** CHRO wants attrition, Finance wants cost per hire, Recruiting wants time to fill. Page 1: 5 shared KPIs. Three tabs, one per team. A 20-minute meeting: 5 minutes headline, 10 insights, 5 decisions.
**Formula / Steps:** (Not run here.) Pin the dashboard sheet first; View > hide gridlines/headings; Review > Protect Sheet with slicers unlocked (see Q33); use Print Preview/PDF for leaders who do not open Excel (from memory).
**Alternative:** Share a PDF or a screenshot with the three key points.
**Result:** None to compute; the 5/10/5 timing totals 20 minutes.
**Version note:** Dashboard page applies to 365, 2024, 2021, 2019 and 2016 (Microsoft Support). Google Sheets share links for live viewing, from memory, unverified.
**Edge cases:** A leader disputing a number; keep the source file and definitions ready. Two senior stakeholders in direct conflict: escalate to the sponsor rather than choose yourself.
**Likely follow-ups:** 1) *What if they ask for more KPIs?* Ask which decision it supports, and move it to a detail tab. 2) *What if the numbers differ from Finance?* Reconcile definitions first.
**Common mistakes:** Walking through every chart; saying yes to everyone; presenting numbers you have not checked.

