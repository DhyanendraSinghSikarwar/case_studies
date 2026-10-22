# Book 1 — Excel | Part 10: Scenario and Practical Tasks (MIS Reports, HR Attrition Sheet) 🟡🔴

**Target:** 60 questions | **Actual:** 60 questions
**Scope:** Scenario and practical tasks an analyst gets live or in a take-home: MIS reports, reconciliation, HR attrition, attendance, payroll and hiring sheets, report hygiene and handover.

### Q1 ⭐⭐⭐ 🟢 How do you prepare an MIS report in Excel from raw data?
**Asked at:** MIS-executive question lists, e.g. Indeed India's MIS executive interview questions (undated hiring-site list, read in earlier research); no company-specific interview report found.
**What the interviewer is checking:** Do you have a repeatable, checked routine, not a one-off copy-paste?
**Say this in the interview:** "I keep the raw data untouched on one sheet, clean a copy, build the summary with formulas that point at the data, reconcile the summary total to the raw total, and only then format and send."
**Explain simply:**
- MIS (Management Information System) report: a regular summary sheet that tells managers how the business or workforce is doing.
- Steps: (1) save raw export as-is; (2) clean (remove extra spaces, fix text-numbers, remove duplicates); (3) summarise with SUMIFS or a pivot table (a drag-and-drop summary tool); (4) check totals; (5) format; (6) send with a short note.
- The reconciliation check (summary total minus raw total = 0) is what separates a reliable report from a risky one.
**Example:** September hiring export has 6 lines totalling 17 hires. One department is typed "Sales " with a trailing space, so a summary on the raw column shows only 15. After a TRIM helper column the summary shows 17.
**Sample sheet:**

| | A (Date) | B (Dept) | C (Hires) | D (Dept clean) |
|---|---|---|---|---|
| 2 | 02-Sep-24 | Sales | 4 | Sales |
| 3 | 05-Sep-24 | Ops | 3 | Ops |
| 4 | 09-Sep-24 | Sales␣ | 2 | Sales |
| 5 | 12-Sep-24 | IT | 5 | IT |
| 6 | 18-Sep-24 | Ops | 1 | Ops |
| 7 | 25-Sep-24 | IT | 2 | IT |

**Formula / Steps:** D2: `=TRIM(B2)` (fill down). Summary in F2:G4, e.g. G2: `=SUMIFS($C$2:$C$7,$D$2:$D$7,F2)`; total G5: `=SUM(G2:G4)`; check I3: `=G5-SUM(C2:C7)`; trailing-space count I4: `=SUMPRODUCT(--(LEN(B2:B7)<>LEN(TRIM(B2:B7))))`.
**Alternative:** Insert > PivotTable on the cleaned range, then refresh when data changes (pivot not run here).
**Result:** Using the raw column B in SUMIFS gave Sales 4, Ops 4, IT 7 = 15 (missing 2). With the clean column D: Sales 6, Ops 4, IT 7, total 17; check = 0; trailing-space rows found = 1.
**Version note:** SUMIFS, TRIM, SUMPRODUCT work in all modern versions; pivot tables in all (from memory, unverified). Same in Google Sheets (from memory, unverified).
**Edge cases:** Hidden rows still count in SUM; text-numbers are ignored by SUM; non-breaking spaces (from web exports) survive TRIM (from memory).
**Likely follow-ups:** 1) *Formulas or pivot?* Formulas for fixed layouts, pivot for exploration. 2) *Why keep raw untouched?* So you can re-check and rerun.
**Common mistakes:** Overwriting raw data; hard-typing totals; no check against the source; sending without a date and "as of" note.

### Q2 ⭐⭐⭐ 🟢 What is an MIS report, and what do daily, weekly and monthly MIS reports usually contain?
**Asked at:** MIS-executive question lists (Indeed India, undated); commonly asked, no company-specific report found.
**What the interviewer is checking:** Do you understand who reads these reports and what decision each one supports?
**Say this in the interview:** "An MIS report turns raw operational data into a few numbers a manager can act on. Daily is operational, weekly is trend, monthly is performance against target."
**Explain simply:**
- MIS = Management Information System: the routine reporting that tells managers "what happened and where to look".
- Daily: counts that need same-day action (attendance, absentees, open positions, tickets or orders).
- Weekly: trends and pending items (joiners vs exits, hiring pipeline, week-on-week change).
- Monthly: results vs target, rates and comparisons (attrition %, headcount movement, payroll cost, absenteeism %, month-on-month change).
- Note: these contents are standard practice, not an official definition; teams differ.
**Example:** HR MIS: daily = "142 of 150 present, 8 absent (5.3%)"; weekly = "5 joiners, 2 exits, 14 interviews pending"; monthly = "attrition 1.2%, payroll Rs 48 lakh, absenteeism 3.1%".
**Sample sheet:**

| Report | Typical contents | Reader |
|---|---|---|
| Daily | Present/absent, late marks, open requisitions | Team lead |
| Weekly | Joiners, exits, pipeline by stage | HR manager |
| Monthly | Attrition %, headcount, payroll, absenteeism, vs target | Leadership |

**Formula / Steps:** Concept question; the formulas behind each line are in Q3, Q5, Q9, Q13 and Q19.
**Alternative:** Many teams automate the same layout in Power BI or Power Query (not run here; see later parts).
**Result:** Not applicable (concept question).
**Version note:** No version dependence.
**Edge cases:** Always state the period and "as of" date; a daily number without a date is unusable.
**Likely follow-ups:** 1) *KPI vs MIS?* A KPI is one measured number; an MIS report packages many KPIs. 2) *How do you decide contents?* Ask the reader what decision they take.
**Common mistakes:** Too many numbers; no comparison to target or last period; mixing definitions month to month.

### Q3 ⭐⭐⭐ 🟢 How do you calculate an employee's tenure in years and months in Excel?
**Asked at:** commonly asked (no company-specific report found); tenure and joining dates appear in HR-MIS JDs researched in this repo.
**What the interviewer is checking:** Do you know DATEDIF, and how to treat people still employed?
**Say this in the interview:** "I use DATEDIF with 'y' for complete years and 'ym' for the leftover months, and for current employees I use a fixed as-of date instead of an exit date."
**Explain simply:**
- Tenure = how long someone has been with the company.
- DATEDIF counts complete years ("y"), complete months ("m") or leftover months ignoring years ("ym"). It is an older function that does not appear in Excel's function list but works (Microsoft Support, "DATEDIF function", lists Excel 2016 to 365).
- Avoid the "MD" unit: Microsoft says it has known limitations and can give a negative, zero or wrong result.
- For active staff, use a report date cell (not TODAY) so the report does not change when reopened.
**Example:** E101 joined 15-Mar-2022 and is active at 31-Dec-2024: 2 years 9 months.
**Sample sheet:**

| | A (ID) | B (Dept) | C (Join) | D (Exit) | K1 (As of) |
|---|---|---|---|---|---|
| 2 | E101 | Sales | 15-Mar-22 | | 31-Dec-24 |
| 3 | E102 | Sales | 01-Jun-23 | 10-Feb-24 | |
| 4 | E103 | Ops | 10-Jan-21 | | |
| 5 | E104 | Ops | 08-Jan-24 | 20-May-24 | |
| 6 | E105 | IT | 01-Jul-20 | 31-Mar-24 | |
| 7 | E106 | IT | 20-Nov-23 | | |

**Formula / Steps:** G2: `=DATEDIF(C2,IF(D2="",$K$1,D2),"y")&" yrs "&DATEDIF(C2,IF(D2="",$K$1,D2),"ym")&" mths"`
**Alternative:** Decimal years: `=ROUND(YEARFRAC(C2,IF(D2="",$K$1,D2)),2)`.
**Result:** G2 "2 yrs 9 mths"; G3 "0 yrs 8 mths"; G4 "3 yrs 11 mths"; G5 "0 yrs 4 mths"; G6 "3 yrs 8 mths"; G7 "1 yrs 1 mths". YEARFRAC: 2.79, 0.69, 3.98, 0.37, 3.75, 1.11.
**Version note:** DATEDIF works in Excel 2016, 2019, 2021, 2024, 365 (Microsoft Support). YEARFRAC from memory, unverified. Google Sheets also has DATEDIF (from memory, unverified).
**Edge cases:** Start date after end date: Microsoft documents #NUM!; LibreOffice returned #VALUE! when I tested, so wrap in `IFERROR(...,"Check dates")`. Dates stored as text will fail. Singular/plural ("1 yrs") needs extra IF if presentation matters.
**Likely follow-ups:** 1) *Tenure in days?* `=end-start`. 2) *Why not TODAY()?* Reports change every time they are opened; use a fixed as-of cell.
**Common mistakes:** Using (end-start)/365 (leap years drift); using "MD"; forgetting blank exit dates, which makes DATEDIF run to 1900.

### Q4 ⭐⭐⭐ 🟡 Walk me through how you would reconcile two reports from different sources in Excel.
**Asked at:** reconciliation appears as a standard prompt on practice sites such as Dataford (search snippet only); no company-specific report found.
**What the interviewer is checking:** Do you have a method that finds every difference, in both directions?
**Say this in the interview:** "I clean both lists, pick a unique key like Employee ID, look up each side in the other, compute the difference, and list missing records and amount mismatches separately."
**Explain simply:**
- Reconcile = prove two sources agree, and explain each difference.
- Step 1 clean: trim spaces, same data type, no duplicate keys. Step 2 compare totals and counts. Step 3 match by key both ways. Step 4 variance column. Step 5 summarise by reason.
- Reverse check matters: a lookup from A to B never shows rows that exist only in B.
**Example:** HR master vs payroll. E3 is in HR but not payroll, E6 is in payroll but not HR, and E2 is paid 41,000 versus 42,000 in HR. Total gap = 6,000.
**Sample sheet:**

| | A (ID) | B (HR amt) | D (ID) | E (Payroll amt) |
|---|---|---|---|---|
| 2 | E1 | 50000 | E1 | 50000 |
| 3 | E2 | 42000 | E2 | 41000 |
| 4 | E3 | 38000 | E4 | 61000 |
| 5 | E4 | 61000 | E5 | 29000 |
| 6 | E5 | 29000 | E6 | 33000 |

**Formula / Steps:** G2: `=IF(COUNTIF($D$2:$D$6,A2)=0,"Missing in payroll","Yes")`; H2: `=IFERROR(VLOOKUP(A2,$D$2:$E$6,2,FALSE),"")`; I2: `=IF(H2="","",B2-H2)`; J2: `=IF(G2<>"Yes","Missing",IF(I2=0,"Match","Amount differs"))`; reverse L2: `=IF(COUNTIF($A$2:$A$6,D2)=0,"Missing in HR","OK")`; gap N1: `=SUM(B2:B6)-SUM(E2:E6)`.
**Alternative:** XLOOKUP (365/2021) or INDEX/MATCH, then a pivot of differences by reason (XLOOKUP and pivot not run here).
**Result:** J2:J6 = Match, Amount differs (diff 1000), Missing, Match, Match; L6 = "Missing in HR" (E6), others OK; N1 = 6000.
**Version note:** COUNTIF, VLOOKUP, IFERROR work in all versions in scope (IFERROR listed for Excel 2016 to 365, Microsoft Support "IFERROR function"). XLOOKUP is 365/2021 only (from memory, unverified).
**Edge cases:** Duplicate IDs return only the first match; IDs stored as text in one file and numbers in the other never match; the net total can be zero while individual rows differ.
**Likely follow-ups:** 1) *Differences explained by timing?* Tag them as timing, not errors. 2) *Large files?* Power Query merge (not run here).
**Common mistakes:** Matching on names; one-direction lookup only; trusting total equality.

### Q5 ⭐⭐⭐ 🟡 Given employee data (Employee ID, Department, Join Date, Exit Date, Status), how would you build a department-wise headcount and attrition summary?
**Asked at:** the HR-attrition-sheet task appears in practice projects (Maven Analytics HR attrition project, GitHub HR-Analysis-Excel; search snippets only); no company-specific report found.
**What the interviewer is checking:** Can you derive opening, joiners, leavers, closing and a correct attrition % from dates?
**Say this in the interview:** "Opening headcount is people who joined before the period and had not left; closing is opening plus joiners minus leavers; attrition is leavers divided by average of opening and closing headcount."
**Explain simply:**
- Headcount = number of employees on the payroll on a date.
- Attrition % = employees who left / average headcount x 100, where average = (start + end) / 2 (AIHR, "attrition rate").
- COUNTIFS counts rows meeting several conditions at once; blank exit date means still employed.
**Example:** Year 2024, Sales: opening 2, joined 1, left 2, closing 1; average headcount 1.5; attrition 133% (a tiny base makes the percent absurd, which is why real reports use hundreds of people).
**Sample sheet:** (Start H2 = 01-Jan-24, End I2 = 31-Dec-24)

| | A (ID) | B (Dept) | C (Join) | D (Exit) |
|---|---|---|---|---|
| 2 | E101 | Sales | 15-Mar-22 | |
| 3 | E102 | Sales | 01-Jun-23 | 10-Feb-24 |
| 4 | E103 | Ops | 10-Jan-21 | |
| 5 | E104 | Ops | 08-Jan-24 | 20-May-24 |
| 6 | E105 | IT | 01-Jul-20 | 31-Mar-24 |
| 7 | E106 | IT | 20-Nov-23 | |
| 8 | E107 | Sales | 05-Feb-24 | 28-Jun-24 |
| 9 | E108 | Ops | 12-Sep-22 | |

**Formula / Steps:** For dept in M5: Opening N5: `=COUNTIFS($B$2:$B$9,M5,$C$2:$C$9,"<"&$H$2)-COUNTIFS($B$2:$B$9,M5,$C$2:$C$9,"<"&$H$2,$D$2:$D$9,"<"&$H$2)`; Joined O5: `=COUNTIFS($B$2:$B$9,M5,$C$2:$C$9,">="&$H$2,$C$2:$C$9,"<="&$I$2)`; Left P5: `=COUNTIFS($B$2:$B$9,M5,$D$2:$D$9,">="&$H$2,$D$2:$D$9,"<="&$I$2)`; Closing Q5: `=N5+O5-P5`; Attrition R5: `=IFERROR(P5/AVERAGE(N5,Q5),0)`.
**Alternative:** A pivot table with Department in rows and counts of join/exit year (not run here); a Status column can be used but misses time windows.
**Result:** Sales 2/1/2/1 and 133.3%; Ops 2/1/1/2 and 50.0%; IT 2/0/1/1 and 66.7%; Total 6/2/4/4 and 80.0%.
**Version note:** COUNTIFS is in Excel 2016 to 365 and Excel Web (Microsoft Support, "COUNTIFS function"); Google Sheets also has it (from memory, unverified).
**Edge cases:** Exit before join (data error), joiners who leave in the same period, zero headcount (hence IFERROR), Status column disagreeing with Exit Date.
**Likely follow-ups:** 1) *Why average headcount?* Closing alone flatters growing firms. 2) *Annualise a month?* Multiply by 12 only if stated.
**Common mistakes:** Dividing by closing headcount; counting everyone with Status "Left" regardless of period; forgetting blank exit dates.

### Q6 ⭐⭐⭐ 🟡 What checks do you run on data accuracy before sending an MIS report to management?
**Asked at:** data accuracy and error handling are listed for MIS roles in x0pa's hiring guide (search snippet only); commonly asked, no company-specific report found.
**What the interviewer is checking:** Do you test before you send?
**Say this in the interview:** "I check duplicates, blanks, wrong data types, impossible dates, totals against the source, and I compare to last month for anything that looks unreasonable."
**Explain simply:**
- Duplicates: the same ID twice inflates headcount.
- Blanks and text-numbers: a number stored as text is skipped by SUM.
- Logic checks: exit date before join date, negative salary, future dates.
- Control totals: count and sum equal the source system.
- Sense check: is this month wildly different from last month? Investigate before sending.
**Example:** In 5 rows, ID E2 repeats, one salary "52000" is text, one salary is blank, one exit date precedes the join date. COUNTA says 4 salaries but COUNT says only 3 are numbers.
**Sample sheet:**

| | A (ID) | B (Join) | C (Exit) | D (Salary) |
|---|---|---|---|---|
| 2 | E1 | 05-Jan-23 | | 50000 |
| 3 | E2 | 01-Apr-23 | 01-Jan-24 | "52000" (text) |
| 4 | E2 | 01-Apr-23 | 01-Jan-24 | 42000 |
| 5 | E4 | 01-May-24 | 01-Mar-24 | 38000 |
| 6 | E5 | 01-Feb-22 | | |

**Formula / Steps:** F2: `=IF(COUNTIF($A$2:$A$6,A2)>1,"Duplicate","")`; G2: `=IF(AND(C2<>"",C2<B2),"Check","")`; H2: `=IF(ISTEXT(D2),"Text","")`; I2: `=IF(D2="","Blank","")`; control cells `=COUNTA(D2:D6)`, `=COUNT(D2:D6)`, `=COUNTBLANK(D2:D6)`.
**Alternative:** Data > Remove Duplicates, conditional formatting (Home > Conditional Formatting > Highlight Cells Rules > Duplicate Values), or Data > Data Validation to prevent bad entries (not run here).
**Result:** Duplicate flagged on rows 3 and 4; row 3 salary "Text"; row 5 "Check" (exit before join); row 6 "Blank". COUNTA = 4, COUNT = 3, COUNTBLANK = 1, SUM = 130000 (the text 52000 is not in it).
**Version note:** All functions are in every version in scope (from memory, unverified).
**Edge cases:** A text-number in a cell compared with `=` can look equal but not sum; SUM adds typed numbers but ignores number-like text in cells.
**Likely follow-ups:** 1) *Who signs off?* A second person or a checklist. 2) *Automate checks?* Put them in a Checks sheet with a pass/fail cell.
**Common mistakes:** Checking only the total; fixing data silently without telling the source owner; no record of what was checked.

### Q7 ⭐⭐⭐ 🟡 How would you set up a monthly report so that it updates with minimal manual work when new data is pasted in?
**Asked at:** report automation appears in MIS role lists (Careers360, search snippet only); commonly asked, no company-specific report found.
**What the interviewer is checking:** Can you separate data, calculation and output so only the data changes?
**Say this in the interview:** "One data sheet, one report sheet driven by formulas and a month cell, and ranges that grow automatically, so each month I paste data, change the month, and check."
**Explain simply:**
- Put raw data in an Excel Table (Insert > Table); tables and structured references grow with new rows (Microsoft Support "Create and format tables" does not itself state auto-expansion; this is from memory, unverified).
- Drive the report from one input cell (report month) with SUMIFS and EOMONTH, so no formula is edited each month.
- Keep a Checks block (totals tie to the data).
- Next level: Power Query refresh (Data > Refresh All) or macro; not run here.
**Example:** Data holds Sep and Oct hires. Month cell H1 = 01-Sep-24 gives Sales 4. After pasting another September Sales line of 6 hires, the report says 10 with no edit.
**Sample sheet:**

| | A (Date) | B (Dept) | C (Hires) | E (Dept) | F (Hires) |
|---|---|---|---|---|---|
| 2 | 02-Sep-24 | Sales | 4 | Sales | formula |
| 3 | 05-Sep-24 | Ops | 3 | Ops | formula |
| 4 | 12-Sep-24 | IT | 5 | IT | formula |
| 5 | 01-Oct-24 | Sales | 9 | | |
| 6 | (new paste) 20-Sep-24 | Sales | 6 | | |

**Formula / Steps:** F2: `=SUMIFS($C:$C,$B:$B,E2,$A:$A,">="&$H$1,$A:$A,"<="&EOMONTH($H$1,0))` with H1 holding the month start. Whole-column references pick up pasted rows.
**Alternative:** Same SUMIFS with table references like `Data[Hires]` (structured references not run here), or Power Query + pivot refresh.
**Result:** Before paste: Sales 4, Ops 3, IT 5. After adding row 6: Sales 10, Ops 3, IT 5 (Oct row correctly excluded).
**Version note:** SUMIFS and EOMONTH are in all versions in scope; Power Query is built in from Excel 2016 (from memory, unverified; confirm in Part 7).
**Edge cases:** Pasted dates arriving as text silently drop out; leave no stray totals row inside the column; whole-column formulas slow huge files.
**Likely follow-ups:** 1) *Why not hard-code ranges?* New rows fall outside. 2) *Manual calculation mode?* Check Formulas > Calculation Options is Automatic.
**Common mistakes:** Typing the month inside formulas; pasting over formulas; no check after refresh.

### Q8 ⭐⭐⭐ 🟡 How do you handle #N/A, #DIV/0! and #REF! errors in a report before you send it?
**Asked at:** error handling is listed for MIS roles (x0pa hiring guide, search snippet only); commonly asked, no company-specific report found.
**What the interviewer is checking:** Do you fix causes, not just hide the error?
**Say this in the interview:** "First understand why: #N/A is a lookup that found nothing, #DIV/0! is division by zero, #REF! is a broken reference. I use IFERROR or IFNA only where a blank or message is a real business answer, and I repair #REF! at the source."
**Explain simply:**
- #N/A: lookup value not found. #DIV/0!: divide by zero (empty headcount). #REF!: a referenced cell or column was deleted.
- IFERROR(value, fallback) catches all seven error types, including #REF! (Microsoft Support, "IFERROR function"). That is the danger: it can hide real mistakes.
- IFNA catches only #N/A, safer for lookups (page only links it; from memory, unverified).
- For division, test the denominator: `IF(G2=0,"n/a",H2/G2)`.
**Example:** Looking up bonus % for E9, who is not in the table, returns #N/A. A department with zero headcount makes attrition #DIV/0!.
**Sample sheet:**

| | A (ID) | C (Salary) | G (Headcount) | H (Left) | L:M (lookup) |
|---|---|---|---|---|---|
| 2 | E1 | 50000 | 120 | 3 | E1 : 0.10 |
| 3 | E9 | 40000 | 0 | 0 | E2 : 0.12 |

**Formula / Steps:** D2: `=VLOOKUP(A2,$L$2:$M$3,2,FALSE)`; E2: `=IFERROR(VLOOKUP(A2,$L$2:$M$3,2,FALSE),"Not found")`; IFNA version `=IFNA(VLOOKUP(...),"Not found")`; I2: `=H2/G2`; J2: `=IF(G2=0,"n/a",H2/G2)`.
**Alternative:** Fix upstream: add the missing ID to the lookup table; or Home > Find & Select > Go To Special > Formulas > Errors to locate all errors.
**Result:** D3 = #N/A; E3 and IFNA version = "Not found"; I2 = 0.025, I3 = #DIV/0!, J3 = "n/a"; `=IFERROR(#REF!,"x")` returned "x" (hidden error); `=IFERROR(50000/0,"masked")` returned "masked". LibreOffice also showed `=IFNA(1/0,"x")` correctly left #DIV/0!.
**Version note:** IFERROR Excel 2016 to 365 (Microsoft Support). IFNA from Excel 2013 (from memory, unverified); Sheets has both (from memory, unverified).
**Edge cases:** Wrapping a whole report in IFERROR turns genuine mistakes into blanks; "n/a" text in a numeric column breaks later SUMs.
**Likely follow-ups:** 1) *How do you stop #REF!?* Do not delete referenced columns; use tables. 2) *Show 0 or blank?* Depends on meaning: 0 means measured zero, blank means unknown.
**Common mistakes:** IFERROR everywhere; hiding the error with font colour; not investigating why.

### Q9 ⭐⭐⭐ 🟡 How do you calculate the absenteeism rate by department for a month?
**Asked at:** commonly asked (no company-specific report found); absence reporting appears in HR-MIS JDs.
**What the interviewer is checking:** Do you get the denominator right (headcount x working days)?
**Say this in the interview:** "Absenteeism rate = absent days divided by total scheduled working days, which is headcount times working days in the month, excluding holidays and weekends."
**Explain simply:**
- Absenteeism rate = absent days / (employees x working days) x 100. This is a common definition, not a single legal standard; confirm whether approved leave counts.
- NETWORKDAYS counts weekdays between two dates and can exclude a holiday list (Microsoft Support, "NETWORKDAYS function").
- Use SUMIFS for absent days and COUNTIF for headcount by department.
**Example:** September 2024 has 21 weekdays; one holiday (16 Sep) leaves 20. Sales has 3 people, 3 absent days: 3 / (3 x 20) = 5.0%.
**Sample sheet:** (F1 = 01-Sep-24, F2 = 30-Sep-24, F3 = 16-Sep-24 holiday)

| | A (Emp) | B (Dept) | C (Absent days) |
|---|---|---|---|
| 2 | E1 | Sales | 2 |
| 3 | E2 | Sales | 0 |
| 4 | E3 | Sales | 1 |
| 5 | E4 | Ops | 3 |
| 6 | E5 | Ops | 0 |
| 7 | E6 | IT | 1 |

**Formula / Steps:** F4: `=NETWORKDAYS(F1,F2,F3)`; I2: `=COUNTIF($B$2:$B$7,H2)`; J2: `=SUMIFS($C$2:$C$7,$B$2:$B$7,H2)`; K2: `=IFERROR(J2/(I2*$F$4),0)`; company K5: `=J5/(I5*$F$4)`.
**Alternative:** Pivot with Department rows and Sum of Absent days, then divide (not run here).
**Result:** Working days 20. Sales 3 heads, 3 days, 5.0%; Ops 2, 3, 7.5%; IT 1, 1, 5.0%; Total 6, 7, 5.83%.
**Version note:** NETWORKDAYS Excel 2016 to 365 (Microsoft Support). NETWORKDAYS.INTL for custom weekends (Microsoft page mentions it in earlier research; not re-fetched).
**Edge cases:** Mid-month joiners/leavers (use days on roll), half-day leave (0.5), different weekly-offs, text dates give #VALUE!.
**Likely follow-ups:** 1) *Include approved leave?* Report both "total absence" and "unplanned absence". 2) *Bradford factor?* Not needed here.
**Common mistakes:** Dividing absent days by headcount alone; counting weekends; using calendar days.

### Q10 ⭐⭐⭐ 🟡 Your report total does not match the source total. How do you find the difference?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you have a systematic hunt, not random guessing?
**Say this in the interview:** "I compare row counts first, then look for text-numbers, extra spaces, duplicates, filtered or hidden rows and wrong ranges, and I split the data in half to isolate where the gap starts."
**Explain simply:**
- Step 1: compare record counts (COUNT vs COUNTA). A gap means text or blank cells.
- Step 2: check labels with spaces, so SUMIFS misses them.
- Step 3: check ranges stop short, hidden or filtered rows, duplicates.
- Step 4: size the gap; a gap equal to one row's value points to that row.
**Example:** Source total 5,500. Report by region adds up to 4,000. Gap 1,500 = "North " with trailing space (700) + a text-number "800" in South.
**Sample sheet:**

| | A (Region) | B (Amount) |
|---|---|---|
| 2 | North | 1000 |
| 3 | South | 1500 |
| 4 | North␣ | 700 |
| 5 | East | 900 |
| 6 | South | "800" (text) |
| 7 | East | 600 |

**Formula / Steps:** Region report E2: `=SUMIFS(B2:B7,A2:A7,"North")+SUMIFS(B2:B7,A2:A7,"South")+SUMIFS(B2:B7,A2:A7,"East")`; gap E3: `=D2-E2` (D2 = 5500); diagnostics G1: `=COUNT(B2:B7)`; G2: `=COUNTA(B2:B7)`; G3: `=SUMPRODUCT(--(LEN(A2:A7)<>LEN(TRIM(A2:A7))))`; G5: `=SUMPRODUCT(VALUE(B2:B7))`.
**Alternative:** Pivot of the source vs your report by region, or `SUBTOTAL(109,range)` to see what filters hide (not run here).
**Result:** Report total 4000; gap 1500; COUNT 5 vs COUNTA 6 (one text-number); trailing-space labels 1; SUM(B2:B7) 4700 (ignores the text); SUMPRODUCT(VALUE) 5500.
**Version note:** All formulas in all versions in scope (from memory, unverified). Excel's text-to-number handling can differ slightly from LibreOffice; confirm in Excel.
**Edge cases:** Two errors can cancel out; currency or date differences between sources; rounding differences (sum of rounded vs rounded sum).
**Likely follow-ups:** 1) *Gap is exactly 2x a number?* Likely a double-count. 2) *Gap tiny?* Rounding.
**Common mistakes:** Plugging the difference; assuming the source is always right.

### Q11 ⭐⭐⭐ 🔴 Given a raw attendance log (Employee ID, Date, In-time, Out-time), how do you calculate hours worked per day and flag late arrivals?
**Asked at:** candidates report a hands-on Excel test with formulas at EXL Service (Glassdoor review, search snippet only); the attendance task itself is general practice.
**What the interviewer is checking:** Do you know that Excel times are fractions of a day, and can you handle missing punches and night shifts?
**Say this in the interview:** "Out minus in gives a fraction of a day, so I multiply by 24 for hours. MOD handles night shifts that cross midnight, and I flag blank punches as 'Check' instead of guessing."
**Explain simply:**
- Excel stores a time as a fraction of 24 hours (12:00 = 0.5), so (Out - In) x 24 = hours.
- MOD(Out-In,1) fixes negative results when Out is after midnight.
- Late = In-time later than the cutoff cell (here 09:30).
- Missing In or Out: show "Check", never 0.
**Example:** Emp E1 in 09:05, out 18:10: 9.08 hours, not late. E1 on 3 Sep in 09:48: late.
**Sample sheet:** (I1 = 09:30 cutoff)

| | A (Emp) | B (Date) | C (In) | D (Out) |
|---|---|---|---|---|
| 2 | E1 | 02-Sep-24 | 09:05 | 18:10 |
| 3 | E1 | 03-Sep-24 | 09:48 | 18:00 |
| 4 | E2 | 02-Sep-24 | 09:30 | 17:45 |
| 5 | E2 | 03-Sep-24 | 10:15 | (blank) |
| 6 | E3 | 02-Sep-24 | 22:00 | 06:00 |
| 7 | E3 | 04-Sep-24 | 09:00 | 13:30 |

**Formula / Steps:** E2: `=IF(OR(C2="",D2=""),"Check",ROUND(MOD(D2-C2,1)*24,2))`; F2: `=IF(C2="","No in-time",IF(C2>$I$1,"Late",""))`. Format C:D as time.
**Alternative:** `=TEXT(D2-C2,"h:mm")` for display (text, not summable); add a shift-start lookup per employee for multi-shift teams.
**Result:** E2:E7 = 9.08, 8.2, 8.25, "Check", 8, 4.5. F2:F7 = blank, Late, blank (09:30 exactly is not late), Late, Late (night shift wrongly flagged), blank.
**Version note:** All functions in every version in scope (from memory, unverified).
**Edge cases:** The night-shift row is flagged late because the cutoff assumes a day shift; needs a shift roster. Times with dates attached, times stored as text, multiple punches per day, overtime beyond 24h not applicable.
**Likely follow-ups:** 1) *Sum weekly hours?* `=SUM(E2:E7)` after setting formats to number, or [h]:mm if kept as time. 2) *Grace period?* Use `>$I$1+TIME(0,10,0)`.
**Common mistakes:** Forgetting x24; negative hours over midnight; treating a blank punch as zero; summing time cells above 24h without [h]:mm.

### Q12 ⭐⭐ 🟢 How do you protect a worksheet so that others cannot change your formulas?
**Asked at:** "how do you keep worksheets secure" appears in the Indeed India MIS executive list (undated).
**What the interviewer is checking:** Do you know the two-step process (unlock inputs, then protect) and its limits?
**Say this in the interview:** "By default every cell is locked, but that does nothing until I protect the sheet. So I unlock the input cells, then protect the sheet, so only inputs are editable."
**Explain simply:**
- Protection stops users changing, moving or deleting data in locked cells. It is not real security and is different from password-protecting the file (Microsoft Support, "Protect a worksheet").
- Step 1: select input cells, Ctrl+1 > Protection tab > clear Locked.
- Step 2: Review > Protect Sheet, choose allowed actions (sorting, filtering, formatting), optional password.
- Forgotten passwords cannot be recovered by Microsoft (same page).
**Example:** A monthly template: month cell and data paste area unlocked; summary formulas locked.
**Sample sheet:**

| Cell | Content | Locked? |
|---|---|---|
| H1 | Report month | No |
| A:C | Data paste area | No |
| F2:F4 | Summary formulas | Yes |

**Formula / Steps:** 1. Select H1 and A:C. 2. Home > Format > Format Cells (or Ctrl+1) > Protection > untick Locked. 3. Review > Protect Sheet. 4. Tick allowed actions, enter password, OK. Undo: Review > Unprotect Sheet. Not run here (UI steps, from the Microsoft page).
**Alternative:** Protect Workbook structure, Allow Edit Ranges, share as PDF or values-only copy. Hiding formulas via "Hidden" on the Protection tab is from memory, unverified.
**Result:** Not applicable (UI steps, not run here).
**Version note:** Review > Protect Sheet is in every desktop version; in Excel for the web it is Review > Manage Protection (Microsoft Support). Google Sheets uses Data > Protect sheets and ranges (from memory, unverified).
**Edge cases:** Protected sheets block pasting into locked cells, and some features (pivot refresh on protected sheets) need permissions; passwords are weak.
**Likely follow-ups:** 1) *Is it secure?* No, treat it as protection against accidents. 2) *Protect against opening?* File > Info > Protect Workbook > Encrypt with Password (from memory, unverified).
**Common mistakes:** Protecting without unlocking inputs, locking yourself out, trusting the password for confidentiality.

### Q13 ⭐⭐ 🟢 How do you calculate month-on-month growth or variance percentage in a report?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The (new - old) / old formula and what to do when old is zero.
**Say this in the interview:** "(This month minus last month) divided by last month, shown as a percent, with IFERROR for a zero base."
**Explain simply:**
- MoM % = (current - previous) / previous.
- Variance = current - previous (the raw difference). Report both when possible.
- Zero previous month makes the percent undefined; show "n/a", not 0%.
**Example:** Hires Jan 40, Feb 46: (46-40)/40 = 15%. Mar 41: -10.9%.
**Sample sheet:**

| | A (Month) | B (Hires) | C (MoM %) | D (Change) |
|---|---|---|---|---|
| 2 | Jan | 40 | | |
| 3 | Feb | 46 | formula | formula |
| 4 | Mar | 41 | formula | formula |
| 5 | Apr | 0 | formula | formula |
| 6 | May | 12 | formula | formula |

**Formula / Steps:** C3: `=IFERROR((B3-B2)/B2,"n/a")` (format as %); D3: `=B3-B2`. Fill down.
**Alternative:** `=B3/B2-1` (same result, but #DIV/0! if B2 is 0).
**Result:** C3 15%, C4 -10.87%, C5 -100%, C6 "n/a"; D from the same rows. May vs Jan `=(B6-B2)/B2` = -70%; `=B6/B5-1` gave #DIV/0! (Apr was 0).
**Version note:** Basic arithmetic, any version.
**Edge cases:** Negative base (variance sign confusing), percent-points vs percent (2.0% to 2.5% is +0.5 points, +25%), small bases.
**Likely follow-ups:** 1) *Year-on-year?* Same formula against the same month last year. 2) *Percent change vs percentage points?* Say which.
**Common mistakes:** Dividing by the new month; showing 0% when previous is zero; mixing points and percent.

### Q14 ⭐⭐ 🟢 How do you group employees into age bands or tenure bands in Excel?
**Asked at:** age-group attrition appears in HR attrition practice projects (Maven Analytics; snippet only); no company-specific report found.
**What the interviewer is checking:** Approximate-match lookup or nested conditions, without long IF chains.
**Say this in the interview:** "I keep the band limits in a small table and use an approximate-match lookup, so changing a band means editing the table, not the formula."
**Explain simply:**
- Band = a labelled range, e.g. 25-34.
- Approximate-match VLOOKUP (last argument TRUE) finds the largest lower limit that is less than or equal to the value; the table must be sorted ascending.
- Same pattern works for tenure bands (0, 1, 3, 5 years).
**Example:** Age 35 falls in 35-44, age 34 in 25-34.
**Sample sheet:** (band table F:G)

| | A (Emp) | B (Age) | F (Lower) | G (Band) |
|---|---|---|---|---|
| 2 | E1 | 23 | 0 | Under 25 |
| 3 | E2 | 29 | 25 | 25-34 |
| 4 | E3 | 35 | 35 | 35-44 |
| 5 | E4 | 41 | 45 | 45+ |
| 6 | E5 | 52 | | |
| 7 | E6 | 24 | | |
| 8 | E7 | 34 | | |

**Formula / Steps:** C2: `=VLOOKUP(B2,$F$2:$G$5,2,TRUE)`; count in a band `=COUNTIF(C2:C8,"25-34")`.
**Alternative:** `=IFS(B2<25,"Under 25",B2<35,"25-34",B2<45,"35-44",TRUE,"45+")` (Excel 2019 and later, from memory, unverified); or `LOOKUP`.
**Result:** C2:C8 = Under 25, 25-34, 35-44, 35-44, 45+, Under 25, 25-34 (both methods agree); COUNTIF "25-34" = 2.
**Version note:** VLOOKUP all versions; IFS needs 2019/365 (from memory, unverified; not in Excel 2016). Sheets has IFS (from memory).
**Edge cases:** Unsorted band table gives wrong bands silently; blank age returns "Under 25"; boundary ages (24/25) must be tested; age should come from DOB (use DATEDIF "y").
**Likely follow-ups:** 1) *Bands in a pivot?* Right-click a number field > Group (not run here). 2) *Compute age?* `=DATEDIF(DOB,asof,"y")`.
**Common mistakes:** Overlapping bands; TRUE vs FALSE in VLOOKUP; unsorted limits.

### Q15 ⭐⭐ 🟢 How do you add GST to an amount, or take GST out of a GST-inclusive amount, in Excel?
**Asked at:** a Glassdoor MIS interview-search result lists "Excel based questions on sum and gst" as a title only (snippet); no more detail found.
**What the interviewer is checking:** The classic trap: removing GST from a gross price by dividing by (1 + rate), not by multiplying by the rate.
**Say this in the interview:** "To add GST I multiply by 1 plus the rate. To remove it from a GST-inclusive amount I divide by 1 plus the rate; I never take 18% of the gross."
**Explain simply:**
- GST (Goods and Services Tax, India) is charged as a percent of the base price. Rates such as 5, 12, 18 are examples; check the current rate.
- Gross = Base x (1 + rate). Base = Gross / (1 + rate). GST part = Gross - Base.
- Intra-state sales split GST equally into CGST and SGST (from memory, unverified): 9% + 9% for 18%.
**Example:** Training fee 50,000 at 18%: GST 9,000, gross 59,000. Reverse: gross 59,000 gives base 50,000; wrong method 59,000 x 18% = 10,620 overstates GST.
**Sample sheet:**

| | A (Item) | B (Base) | C (GST rate) | D (GST) | E (Gross) |
|---|---|---|---|---|---|
| 2 | Training | 50000 | 18% | | |
| 3 | Books | 2000 | 5% | | |
| 4 | Laptop bag | 1500 | 12% | | |
| 5 | Software | 10000 | 18% | | |

**Formula / Steps:** D2: `=B2*C2`; E2: `=B2*(1+C2)`; reverse H2: `=ROUND(G2/(1+C2),2)`; GST inside I2: `=G2-H2`; wrong J2: `=G2*C2`.
**Alternative:** Put the rate in one input cell and reference it with `$C$1`.
**Result:** GST 9000, 100, 180, 1800; gross 59000, 2100, 1680, 11800; reverse base 50000, 2000, 1500, 10000; GST inside 9000, 100, 180, 1800; wrong method 10620, 105, 201.6, 2124. CGST half of 9000 = 4500.
**Version note:** Basic arithmetic, any version.
**Edge cases:** Rounding to 2 decimals per line vs on the total can differ by paise; mixed rates on one invoice; amounts with text.
**Likely follow-ups:** 1) *Percent as 18 or 18%?* Enter 18% or divide by 100. 2) *Total GST by rate?* SUMIFS by rate.
**Common mistakes:** Multiplying the gross by the rate; typing 18 instead of 18%; rounding too early.

### Q16 ⭐⭐ 🟢 How do you highlight the top 10 or bottom 5 performers in a report?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Conditional formatting rules, and how ties behave.
**Say this in the interview:** "Home > Conditional Formatting > Top/Bottom Rules for the quick way, or a formula rule using LARGE and SMALL when I need ties or text labels handled."
**Explain simply:**
- Conditional formatting colours cells automatically when a rule is true.
- Top/Bottom rules take a number from 1 to 1000, or percent from 1 to 100 (Microsoft Support, "Use conditional formatting to highlight information").
- Formula rules need a true/false formula; start with `=`; use relative references.
**Example:** Scores of 8 people; Top 3 and Bottom 2. Two people tie at 88, so "Top 3" highlights four people.
**Sample sheet:**

| | A (Emp) | B (Score) |
|---|---|---|
| 2 | E1 | 92 |
| 3 | E2 | 88 |
| 4 | E3 | 95 |
| 5 | E4 | 70 |
| 6 | E5 | 88 |
| 7 | E6 | 61 |
| 8 | E7 | 79 |
| 9 | E8 | 55 |

**Formula / Steps:** 1. Select B2:B9. 2. Home > Conditional Formatting > Top/Bottom Rules > Top 10 Items (change 10 to 3), pick colour. 3. Repeat with Bottom 10 Items (set 2). Formula route: Conditional Formatting > New Rule > Use a formula: `=B2>=LARGE($B$2:$B$9,3)`; label in D2: `=IF(B2>=LARGE($B$2:$B$9,3),"Top 3",IF(B2<=SMALL($B$2:$B$9,2),"Bottom 2",""))`. Rank column: `=RANK.EQ(B2,$B$2:$B$9,0)`. Visual formatting not run here; the formulas were.
**Alternative:** Sort descending and take the first rows; or a pivot Top 10 value filter (not run here).
**Result:** LARGE(…,3) = 88; SMALL(…,2) = 61. Labels: E1, E2, E3, E5 = "Top 3" (four people: tie); E6, E8 = "Bottom 2". Ranks: 2, 3, 1, 6, 3, 7, 5, 8.
**Version note:** Top/Bottom rules in all versions; RANK.EQ Excel 2010+ (from memory, unverified).
**Edge cases:** Ties extend the group; blanks and text are ignored; text scores will not rank.
**Likely follow-ups:** 1) *Exactly 3 only?* Break ties with a second sort key. 2) *Top 10%?* Tick "% of the selected range".
**Common mistakes:** Absolute reference mistakes in the formula rule; formatting a range containing a totals row.

### Q17 ⭐⭐ 🟢 How do you present MIS findings to a non-technical manager, beyond sending the sheet?
**Asked at:** commonly asked (no company-specific report found); stakeholder communication is a soft-skill expectation in MIS JDs researched in this repo.
**What the interviewer is checking:** Can you turn numbers into a message and a decision?
**Say this in the interview:** "I lead with one headline, show the number against target or last month, explain the likely reason, and end with what I recommend. The sheet is the backup, not the message."
**Explain simply:**
- Structure: headline, evidence (one chart or three numbers), reason, recommended action, next step.
- Compare: always against target or last period.
- One page or a few lines in the email; details in an appendix tab.
- A formula can write the headline sentence so it never goes stale.
**Example:** "Attrition in March was 2.5%, up 0.9 points from February; most exits were voluntary in Sales within the first year. Suggest exit interviews and a 90-day check-in."
**Sample sheet:**

| | A (Month) | B (Attrition %) |
|---|---|---|
| 2 | Jan | 2.02% |
| 3 | Feb | 1.63% |
| 4 | Mar | 2.48% |

**Formula / Steps:** D1: `="Attrition in "&A4&" was "&TEXT(B4,"0.0%")&", up "&TEXT((B4-B3)*100,"0.0")&" points from "&A3&"."`
**Alternative:** A single chart with one-line title stating the message (Insert > Charts, not run here), or a short dashboard.
**Result:** "Attrition in Mar was 2.5%, up 0.9 points from Feb."
**Version note:** TEXT works in all versions; format codes may be locale-dependent (from memory, unverified).
**Edge cases:** Too many caveats bury the message; TEXT output is text and cannot be summed; a drop in a rate may be a denominator change.
**Likely follow-ups:** 1) *Manager asks something not in the sheet?* Say what you will check and by when. 2) *Slides or email?* Match their habit.
**Common mistakes:** Sending raw tables; reading numbers aloud; no recommendation.

### Q18 ⭐⭐ 🟢 How do you calculate the average and the median salary by department in Excel, and which one would you report?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that outliers distort the average?
**Say this in the interview:** "I calculate both. If a few very high salaries pull the average up, I report the median as the typical salary and mention the average."
**Explain simply:**
- Average (mean) = total / count. Median = middle value when sorted.
- One very high salary moves the average a lot but barely moves the median.
- AVERAGEIFS gives the average by department; median by department needs an IF inside MEDIAN, entered as an array formula (Ctrl+Shift+Enter in older Excel).
**Example:** Sales salaries 32k, 35k, 38k and a 150k manager. Average 63,750; median 36,500, which is what a typical Sales employee earns.
**Sample sheet:**

| | A (Emp) | B (Dept) | C (Salary) |
|---|---|---|---|
| 2-5 | E1-E4 | Sales | 32000, 35000, 38000, 150000 |
| 6-8 | E5-E7 | Ops | 28000, 30000, 31000 |
| 9-10 | E8-E9 | IT | 60000, 64000 |

(Each employee is on its own row; grouped here for space.)
**Formula / Steps:** F2: `=AVERAGEIFS($C$2:$C$10,$B$2:$B$10,E2)`; G2 (array formula): `=MEDIAN(IF($B$2:$B$10=E2,$C$2:$C$10))`.
**Alternative:** Pivot table average (Value Field Settings); a standard pivot does not offer Median (from memory, unverified; the Data Model/DAX route is for Part 11, not run here).
**Result:** Sales average 63,750, median 36,500; Ops 29,667, 30,000; IT 62,000, 62,000.
**Version note:** AVERAGEIFS Excel 2007+; MEDIAN(IF()) needs Ctrl+Shift+Enter in Excel 2016/2019 and works natively in 365/2021 (from memory, unverified). Sheets: wrap in ARRAYFORMULA (from memory).
**Edge cases:** Blank salary cells are ignored; zero salaries (unpaid) distort; tiny groups; text salaries.
**Likely follow-ups:** 1) *Why not the mode?* Rarely useful for salary. 2) *Compa-ratio?* Salary divided by band midpoint.
**Common mistakes:** Reporting only the average; forgetting array entry for conditional MEDIAN; averaging averages.

### Q19 ⭐⭐ 🟡 How do you calculate the voluntary and involuntary attrition split for a month?
**Asked at:** commonly asked (no company-specific report found); the split follows AIHR's definitions.
**What the interviewer is checking:** Correct classification, the same denominator for both, and month boundaries.
**Say this in the interview:** "I count leavers by exit type within the month, divide each by average headcount, and also show the share of total exits that were voluntary."
**Explain simply:**
- Voluntary: the employee chose to leave (resignation, relocation). Involuntary: the company initiated it (dismissal, restructuring) (AIHR, "attrition rate").
- Rate = leavers / average headcount; use the same average for both types so they add up.
- Month window: from the 1st to EOMONTH (last day of month).
**Example:** March: 6 exits (4 voluntary, 2 involuntary); opening 500, closing 494, average 497. Total 1.21%, voluntary 0.80%, involuntary 0.40%.
**Sample sheet:** (E1 = 01-Mar-24, E2 opening 500, E3 closing 494)

| | A (Exit date) | B (Type) |
|---|---|---|
| 2 | 26-Feb-24 | Voluntary |
| 3 | 04-Mar-24 | Voluntary |
| 4 | 11-Mar-24 | Involuntary |
| 5 | 15-Mar-24 | Voluntary |
| 6 | 22-Mar-24 | Voluntary |
| 7 | 28-Mar-24 | Involuntary |
| 8 | 29-Mar-24 | Voluntary |
| 9 | 02-Apr-24 | Voluntary |

**Formula / Steps:** E5: `=AVERAGE(E2:E3)`; E6: `=COUNTIFS($B$2:$B$9,"Voluntary",$A$2:$A$9,">="&$E$1,$A$2:$A$9,"<="&EOMONTH($E$1,0))`; E7: same with "Involuntary"; E8: `=E6+E7`; rates F6: `=E6/$E$5`; share G6: `=E6/$E$8`.
**Alternative:** Pivot with Exit Type in columns and Exit Month in rows (not run here).
**Result:** Average headcount 497; voluntary 4, involuntary 2, total 6; rates 0.805%, 0.402%, 1.207%; voluntary share 66.7%. The 26-Feb and 02-Apr rows are correctly excluded.
**Version note:** COUNTIFS, EOMONTH in all versions in scope (COUNTIFS per Microsoft Support).
**Edge cases:** Exit types spelled inconsistently ("Resigned" vs "Voluntary"); date with time part on the last day (use `<` next month start); retirements/deaths need an agreed class.
**Likely follow-ups:** 1) *Annualise?* Multiply by 12 (state it). 2) *Regretted attrition?* A separate tag decided by managers.
**Common mistakes:** Different denominators for each type; including leavers from other months; typos in the type column.

### Q20 ⭐⭐ 🟡 How do you calculate first-year (early) attrition in Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you define "first-year attrition" clearly, since there are two common readings?
**Say this in the interview:** "I state the definition first: either the share of this year's leavers who had under 12 months of service, or, better, the share of a hiring cohort that left within 12 months. Then I compute tenure at exit with DATEDIF."
**Explain simply:**
- Early attrition = people leaving soon after joining. AIHR flags early-tenure exits as a risk and suggests bands such as 0-3 and 3-6 months, but gives no first-year formula (AIHR, "attrition rate", fetched).
- The formulas below are my own working definitions, an inference, not a published standard.
- Definition A (leavers mix): early leavers / all leavers in the period.
- Definition B (cohort): of people hired in a window, how many left within 12 months.
**Example:** In 2024, 5 people left; 3 of them had under 12 months of service: 60% (A). Of 4 hired in 2023-24, 3 left within 12 months: 75% (B).
**Sample sheet:**

| | A (ID) | B (Dept) | C (Join) | D (Exit) | G (Tenure months) |
|---|---|---|---|---|---|
| 2 | E101 | Sales | 15-Mar-22 | | |
| 3 | E102 | Sales | 01-Jun-23 | 10-Feb-24 | 8 |
| 4 | E109 | Ops | 01-May-22 | 30-Aug-24 | 27 |
| 5 | E104 | Ops | 08-Jan-24 | 20-May-24 | 4 |
| 6 | E105 | IT | 01-Jul-20 | 31-Mar-24 | 44 |
| 7 | E106 | IT | 20-Nov-23 | | |
| 8 | E107 | Sales | 05-Feb-24 | 28-Jun-24 | 4 |
| 9 | E108 | Ops | 12-Sep-22 | | |

**Formula / Steps:** G2: `=IF(D2="","",DATEDIF(C2,D2,"m"))`. Leavers M1: `=COUNTIFS(D2:D9,">="&DATE(2024,1,1),D2:D9,"<="&DATE(2024,12,31))`; early M2: same plus `,G2:G9,"<12"`; A: `=M2/M1`. Cohort hires M4: `=COUNTIFS(C2:C9,">="&DATE(2023,1,1),C2:C9,"<="&DATE(2024,12,31))`; early leavers in cohort M5: same plus `,G2:G9,"<12"`; B: `=M5/M4`.
**Alternative:** Tenure bands with COUNTIFS (Q21), or a pivot of leavers by tenure band (not run here).
**Result:** Tenure months 8, 27, 4, 44, 4. Leavers 5, early leavers 3, A = 60%. Cohort 4, early 3, B = 75%. Using "<=12" instead of "<12" gave the same count here.
**Version note:** DATEDIF Excel 2016 to 365 (Microsoft Support); COUNTIFS also (Microsoft Support).
**Edge cases:** The cohort must be old enough to have had 12 months (E106 joined Nov-23 and is still active, so counts as a non-leaver only because the as-of date is 31-Dec-24). Boundary at exactly 12 months, rehires, tiny cohorts, blank exit dates (G blank is ignored by "<12").
**Likely follow-ups:** 1) *Which definition is better?* B, because A is distorted by how many veterans left. 2) *Why does it matter?* High early attrition points to hiring or onboarding problems.
**Common mistakes:** Not saying which definition; dividing by total headcount; counting active people with blank tenure as early.

### Q21 ⭐⭐ 🟡 How do you calculate attrition by tenure band using COUNTIFS?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you turn dates into a number (months of service), bucket it, and count with two or three conditions at once?
**Say this in the interview:** "First I add a helper column with tenure in completed months, using the exit date for leavers and the report date for people still here. Then COUNTIFS counts everyone in each band, and the leavers in each band. Leavers divided by headcount gives the rate per band."
**Explain simply:**
- *Tenure* means how long a person has worked for the company. A *band* is a range, such as 0-3 months.
- A *helper column* is an extra column you add only to make the next formula easy.
- AIHR (aihr.com, "Attrition rate", fetched) suggests splitting attrition by tenure bands such as 0 to 3 months, 3 to 6 months, 6 to 12 months and 1+ years, because early exits drive attrition.
- COUNTIFS counts rows meeting all conditions; ">="&H4 glues a comparison to a cell value.
- The "leavers / headcount in band" rate below is my own simple method (stayers are placed in a band by tenure up to the report date). AIHR gives the overall formula (departures / average headcount), not this per-band rate.
**Example:** At 31-Dec-2025, 10 people have ever been on the list and 7 have left. Of the 3 people with under 3 months of service, all 3 left (100%). That tells HR the problem is in onboarding, not in senior staff.
**Sample sheet:**

| | A | B | C | D | E | | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Emp | Join | Exit | Tenure_m | Left | | AsOf | 31-Dec-2025 | | | | |
| 2 | E1 | 10-Jan-25 | 20-Mar-25 | 2 | 1 | | | | | | | |
| 3 | E2 | 01-Feb-25 | 15-Aug-25 | 6 | 1 | | Band | From | To | Headcount | Leavers | Attr% |
| 4 | E3 | 01-Mar-24 | | 21 | 0 | | 0-3 | 0 | 3 | 3 | 3 | 1.000 |
| 5 | E4 | 01-Apr-25 | 20-May-25 | 1 | 1 | | 3-6 | 3 | 6 | 0 | 0 | #DIV/0! |
| 6 | E5 | 01-Jun-24 | 30-Sep-25 | 15 | 1 | | 6-12 | 6 | 12 | 3 | 2 | 0.667 |
| 7 | E6 | 01-Jun-25 | | 6 | 0 | | 12+ | 12 | 999 | 4 | 2 | 0.500 |
| 8 | E7 | 05-Jan-25 | 01-Dec-25 | 10 | 1 | | | | Total | 10 | 7 | |
| 9-11 | E8 to E10 continue (tenure 29, 2, 18) | | | | | | | | | | | |

**Formula / Steps:**
- D2: `=DATEDIF(B2,IF(C2="",$H$1,C2),"m")` (completed months)
- E2: `=IF(C2="",0,1)`
- J4: `=COUNTIFS($D$2:$D$11,">="&H4,$D$2:$D$11,"<"&I4)`
- K4: `=COUNTIFS($D$2:$D$11,">="&H4,$D$2:$D$11,"<"&I4,$E$2:$E$11,1)`
- L4: `=IFERROR(K4/J4,"n/a")` (the sheet above shows the bare K/J result so the error is visible)
**Alternative:** `=SUMPRODUCT(($D$2:$D$11>=H4)*($D$2:$D$11<I4)*$E$2:$E$11)` for leavers; or a PivotTable on a Band helper column (not run here).
**Result:** Run in LibreOffice 24.2: headcount 3, 0, 3, 4 (total 10); leavers 3, 0, 2, 2 (total 7); rates 1.0, #DIV/0!, 0.667, 0.5. The IFERROR wrapper was not run separately.
**Version note:** DATEDIF works in Excel 2016 to 365 (Microsoft Support, "DATEDIF function"); COUNTIFS is in all versions you will meet (listed for 2016 on its sibling SUMIFS page; Google Sheets from memory, unverified).
**Edge cases:** Empty band gives #DIV/0! (wrap in IFERROR); DATEDIF returns #NUM! if join is after the end date (Microsoft Support); boundaries must be "from <=, to <" or people are counted twice; exit dates entered as text break the formula.
**Likely follow-ups:** 1) *Why DATEDIF "m" and not days/30?* It counts completed months exactly. 2) *Is this rate the same as monthly attrition?* No, it is a share of people ever in the band, not a rate per period.
**Common mistakes:** Using "<=" on both band edges; measuring leavers' tenure to today instead of to the exit date; leaving stayers out of the headcount.

### Q22 ⭐⭐ 🟡 How do you find the opening and closing headcount of a month from join dates and exit dates?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand headcount as "joined before, minus left before" at a point in time?
**Say this in the interview:** "Opening headcount is everyone who joined before the 1st minus everyone who left before the 1st. Closing is opening plus joiners in the month minus leavers in the month. I cross-check closing with the same 'joined minus left' count at month end."
**Explain simply:**
- *Headcount* is the number of employees on the rolls on a given date.
- Counting joiners and leavers separately avoids needing a row per day.
- A blank exit date means the person is still working; COUNTIFS on the Exit column simply skips blanks when you ask for dates.
- Decide a convention and state it: here a person whose exit date is 31-Jan is still counted on 31-Jan, and gone from 1-Feb.
**Example:** Month is January 2026. 3 people are on the rolls on 1 Jan, 2 join, 2 leave: closing = 3 + 2 - 2 = 3.
**Sample sheet:**

| | A | B | C | | E | F |
|---|---|---|---|---|---|---|
| 1 | Emp | Join | Exit | Month start | 01-Jan-26 | |
| 2 | E1 | 01-Jun-25 | 15-Jan-26 | Month end | 31-Jan-26 | |
| 3 | E2 | 10-Aug-25 | | | | |
| 4 | E3 | 20-Dec-25 | 31-Jan-26 | Opening | 3 | |
| 5 | E4 | 05-Jan-26 | | Joiners | 2 | |
| 6 | E5 | 25-Jan-26 | 10-Feb-26 | Leavers | 2 | |
| 7 | E6 | 01-May-24 | 31-Dec-25 | Closing | 3 | |
| 8 | E7 | 03-Feb-26 | | Closing (direct) | 3 | |

**Formula / Steps:** (month start in F1, month end `=EOMONTH(F1,0)` in F2)
- Opening: `=COUNTIFS(B2:B8,"<"&F1)-COUNTIFS(C2:C8,"<"&F1)`
- Joiners: `=COUNTIFS(B2:B8,">="&F1,B2:B8,"<="&F2)`
- Leavers: `=COUNTIFS(C2:C8,">="&F1,C2:C8,"<="&F2)`
- Closing: `=F4+F5-F6`
**Alternative:** Direct closing: `=COUNTIFS(B2:B8,"<="&F2)-COUNTIFS(C2:C8,"<="&F2)`; or `=SUMPRODUCT((B2:B8<=F2)*((C2:C8="")+(C2:C8>F2)>0))`.
**Result:** Run in LibreOffice 24.2: opening 3, joiners 2, leavers 2, closing 3, direct closing 3 (matches).
**Version note:** Works in every Excel version and in Google Sheets (functions are old; Sheets from memory, unverified).
**Edge cases:** Rejoiners need one row per stint, or they are miscounted; exit dates stored as text are not counted; E6 left on 31-Dec so is correctly outside January; joined and left in the same month counts in both joiners and leavers.
**Likely follow-ups:** 1) *Average headcount?* (opening + closing)/2, as AIHR does for attrition. 2) *Why not a running total?* It drifts when data is corrected.
**Common mistakes:** Using "<=" for the opening date; forgetting that closing must equal next month's opening; counting blank exit cells as dates.

### Q23 ⭐⭐ 🟡 How do you build an HR attrition dashboard in Excel with slicers for department, gender and age band?
**Asked at:** commonly asked (no company-specific report found). HR attrition dashboards by gender, education and age group appear as practice projects (Maven Analytics HR attrition project, snippet only).
**What the interviewer is checking:** Can you structure data, summarise it with PivotTables, and make it interactive without breaking it?
**Say this in the interview:** "I clean the data into a Table, add helper columns for age band and a 1/0 Left flag, build PivotTables for headcount, leavers and attrition rate, add charts, and connect department, gender and age-band slicers to all of them."
**Explain simply:**
- A *PivotTable* is a drag-and-drop summary of a table. A *slicer* is a button panel that filters it.
- Averaging a 1/0 Left flag gives the share who left, so one pivot field gives the rate.
- One slicer can drive several PivotTables through Report Connections.
- Keep a hidden or separate data sheet so users only touch the dashboard.
**Example:** 8 employees, 3 left (37.5%). By department HR is 50%, IT and Sales 33.3% each; by gender F 50% and M 25%; the under-30 band is 100% (3 of 3), so the story is early-career exits.
**Sample sheet:**

| | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 1 | Emp | Dept | Gender | Age | AgeBand | Left |
| 2 | E1 | Sales | F | 24 | <30 | 1 |
| 3 | E2 | Sales | M | 31 | 30-39 | 0 |
| 4 | E3 | Sales | F | 45 | 40+ | 0 |
| 5 | E4 | IT | M | 28 | <30 | 1 |
| 6 | E5 | IT | F | 35 | 30-39 | 0 |
| 7 | E6 | IT | M | 52 | 40+ | 0 |
| 8 | E7 | HR | F | 29 | <30 | 1 |
| 9 | E8 | HR | M | 41 | 40+ | 0 |

**Formula / Steps (not run here: PivotTables and slicers cannot run in this environment):**
1. Select data > Insert > Table. Add `E2: =IF(D2<30,"<30",IF(D2<40,"30-39","40+"))`, and F as a 1/0 flag.
2. Insert > PivotTable > new sheet; Rows = Dept, Values = Count of Emp, Sum of Left, Average of Left (format as %).
3. Build one pivot each for Gender and AgeBand; Insert > PivotChart for each.
4. Click a pivot > PivotTable Analyze > Insert Slicer > tick Dept, Gender, AgeBand.
5. Slicer > Slicer tab > Report Connections > tick every pivot.
6. Arrange on a dashboard sheet, add KPI cells with GETPIVOTDATA or direct formulas, hide the pivot sheet.
**Alternative:** Skip pivots: charts driven by COUNTIFS/AVERAGEIFS formulas, with a data-validation drop-down instead of slicers.
**Result:** Reproduced with pandas (the Excel dashboard was not run here): overall 0.375; HR 0.50, IT 0.333, Sales 0.333; F 0.50, M 0.25; <30 1.0, 30-39 0.0, 40+ 0.0.
**Version note:** Slicers on PivotTables exist from Excel 2010 and Tables slicers from 2013; Google Sheets has slicers and pivots but with different menus (both from memory, unverified).
**Edge cases:** Average of a 1/0 flag is a simple share of everyone listed, not leavers over average headcount (AIHR's formula); new data needs Refresh All; small groups make rates swing wildly.
**Likely follow-ups:** 1) *Why a Table?* Pivots pick up new rows. 2) *Why use Report Connections?* So one slicer filters all charts.
**Common mistakes:** Slicers connected to one pivot only; age bands created by hand per row; hiding rate denominators.

### Q24 ⭐⭐ 🟡 Given a hiring tracker with candidate stages, how do you calculate the conversion rate from one stage to the next?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you count "reached at least this stage" rather than "currently at this stage"?
**Say this in the interview:** "I record the furthest stage each candidate reached as a number, count candidates at or beyond each stage with COUNTIF and '>=', and divide each stage by the one before. I also give the overall applied-to-joined rate."
**Explain simply:**
- A *funnel* is the series of hiring stages; *conversion rate* is the percentage who move on from one stage to the next.
- Someone who reached Offered also passed Screened and Interviewed, so counts must be cumulative.
- Counting only "current stage" undercounts earlier stages.
**Example:** 12 applicants, 10 screened, 7 interviewed, 4 offered, 2 joined. Offer-to-join is 50%, overall 16.7%.
**Sample sheet:**

| | A | B | | D | E | F | G |
|---|---|---|---|---|---|---|---|
| 1 | Cand | Furthest stage | | # | Stage | Reached | Conv. from prev |
| 2 | C1 | 5 | | 1 | Applied | 12 | |
| 3 | C2 | 5 | | 2 | Screened | 10 | 0.833 |
| 4 | C3 | 4 | | 3 | Interviewed | 7 | 0.700 |
| 5 | C4 | 4 | | 4 | Offered | 4 | 0.571 |
| 6 | C5 | 3 | | 5 | Joined | 2 | 0.500 |
| 7-13 | C6 to C12: 3,3,2,2,2,1,1 | | | | | | |

**Formula / Steps:**
- F2: `=COUNTIF($B$2:$B$13,">="&D2)` filled down
- G3: `=IFERROR(F3/F2,0)` filled down
- Overall (H2): `=F6/F2`
**Alternative:** One date column per stage and `=COUNT(C2:C13)` for each; or a PivotTable on stage with Show Values As (not run here).
**Result:** Run in LibreOffice 24.2: reached 12, 10, 7, 4, 2; conversions 0.833, 0.700, 0.571, 0.500; overall 0.1667.
**Version note:** All functions work in every Excel version and in Google Sheets (Sheets from memory, unverified).
**Edge cases:** Rejected candidates must keep their furthest stage; candidates who skipped a stage still count at later ones; blank stage numbers are ignored by COUNTIF; division by zero when a stage is empty.
**Likely follow-ups:** 1) *Where is the biggest drop?* Lowest conversion, offered to joined here at 50% after 57% before. 2) *Why track by date?* To measure time between stages.
**Common mistakes:** Dividing by total applicants for every stage; using "=" instead of ">="; mixing stage names and numbers.

### Q25 ⭐⭐ 🟡 How do you calculate average time-to-hire by department from requisition and joining dates?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Date subtraction, handling open requisitions, and AVERAGEIFS.
**Say this in the interview:** "I add a Days column, joining date minus requisition date, left blank when nobody has joined yet. Then AVERAGEIFS by department averages only the filled rows. I also show how many requisitions are still open."
**Explain simply:**
- *Requisition* means an approved request to hire someone. *Time-to-hire* is days from that request to the joining date (some companies measure to offer acceptance instead; say which).
- Excel stores dates as numbers, so subtracting works.
- AVERAGEIFS averages one column for rows that meet a condition and ignores text such as "".
**Example:** Sales has 2 filled requisitions at 40 and 40 days and 1 open: average 40. IT has 58 and 50 days (average 54).
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Dept | Req date | Join date | Days |
| 2 | Sales | 05-Jan-25 | 14-Feb-25 | 40 |
| 3 | Sales | 20-Jan-25 | 01-Mar-25 | 40 |
| 4 | IT | 01-Feb-25 | 31-Mar-25 | 58 |
| 5 | IT | 10-Feb-25 | | |
| 6 | HR | 01-Mar-25 | 26-Mar-25 | 25 |
| 7 | Sales | 03-Mar-25 | | |
| 8 | IT | 05-Mar-25 | 24-Apr-25 | 50 |

**Formula / Steps:**
- D2: `=IF(C2="","",C2-B2)`
- Average by dept: `=IFERROR(AVERAGEIFS($D$2:$D$8,$A$2:$A$8,F2),"")`
- Filled count: `=COUNTIFS($A$2:$A$8,F2,$D$2:$D$8,">=0")`
- Open requisitions: `=COUNTIFS(A2:A8,F2)-` filled count
**Alternative:** PivotTable with Average of Days by Dept (not run here); or `=SUMIFS(D:D,A:A,F2)/COUNTIFS(A:A,F2,D:D,">=0")`.
**Result:** Run in LibreOffice 24.2: Sales 40, IT 54, HR 25, all 42.6; filled counts 2, 2, 1.
**Version note:** AVERAGEIFS exists from Excel 2007, so all current versions; Google Sheets has it (from memory, unverified).
**Edge cases:** Open requisitions must not count as zero; join before requisition gives negative days (data error); text dates fail; averages hide outliers, so also show the median.
**Likely follow-ups:** 1) *Why median too?* One 150-day hire distorts the average. 2) *Offer acceptance vs joining?* Joining is later, include notice period.
**Common mistakes:** Putting 0 for open roles; using AVERAGE on the whole column; mixing calendar and working days.

### Q26 ⭐⭐ 🟡 How do you build a payroll summary by department and month using SUMIFS?
**Asked at:** commonly asked (no company-specific report found). Payroll MIS reports appear in payroll JDs in the repo's research files.
**What the interviewer is checking:** Mixed references ($) and a two-way summary grid.
**Say this in the interview:** "I make department names down the side and month-start dates across the top, then one SUMIFS with the department locked by column and the month locked by row, filled across and down. Totals on the edges reconcile to the source total."
**Explain simply:**
- SUMIFS adds numbers where several conditions are all true.
- `$E2` locks the column, `F$1` locks the row, so one formula fills the whole grid.
- A total row and column plus a check against `SUM` of the raw data proves nothing was missed.
**Example:** January: IT 90,000 and Sales 100,000; February: HR 40,000, IT 121,000, Sales 50,000; grand total 401,000.
**Sample sheet:**

| | A | B | C | | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| 1 | Dept | Month | Gross | | Dept | 01-Jan-26 | 01-Feb-26 | Total |
| 2 | Sales | 01-Jan-26 | 52,000 | | HR | 0 | 40,000 | 40,000 |
| 3 | Sales | 01-Jan-26 | 48,000 | | IT | 90,000 | 121,000 | 211,000 |
| 4 | IT | 01-Jan-26 | 90,000 | | Sales | 100,000 | 50,000 | 150,000 |
| 5 | Sales | 01-Feb-26 | 50,000 | | Total | 190,000 | 211,000 | 401,000 |
| 6-8 | IT 91,000; IT 30,000; HR 40,000 (Feb) | | | | | | | |

**Formula / Steps:**
- F2: `=SUMIFS($C$2:$C$8,$A$2:$A$8,$E2,$B$2:$B$8,F$1)` filled to G4
- H2: `=SUM(F2:G2)`; row 5: `=SUM(F2:F4)`
- Check: `=SUM(C2:C8)` must equal H5
**Alternative:** PivotTable with Dept in Rows and Month in Columns (not run here); or SUMPRODUCT.
**Result:** Run in LibreOffice 24.2: grid as shown; check cell returns 401,000. SUMIFS requires criteria ranges the same size as the sum range (Microsoft Support, "SUMIFS function").
**Version note:** SUMIFS is listed for Excel 2016, 2019, 2021, 2024 and 365 (Microsoft Support, "SUMIFS function"); Google Sheets has it (from memory, unverified).
**Edge cases:** Month stored as text vs real date breaks the match; dates with a time part or mid-month dates miss the first-of-month key; a department spelt two ways splits the total; blank cells return 0, which may look like an error.
**Likely follow-ups:** 1) *How to avoid month typing issues?* Use a helper `=EOMONTH(date,-1)+1`. 2) *Net pay vs gross?* Add more value columns or sheets.
**Common mistakes:** Forgetting the $ signs; criteria ranges of unequal size; not reconciling to the source total.

### Q27 ⭐⭐ 🟡 How do you calculate overtime hours and overtime pay from daily hours worked?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** MAX(0, ...) logic and keeping policy numbers in input cells.
**Say this in the interview:** "Overtime hours per day are hours worked minus standard hours, floored at zero. Pay is overtime hours times hourly rate times the overtime multiplier. I keep standard hours, days in the month and multiplier in separate cells because policy decides them."
**Explain simply:**
- *Overtime* is time beyond standard hours; the multiplier (1.5x, 2x) is a company or legal rule, so I never hard-code it.
- MAX(0, x) stops short days from giving negative overtime.
- Hourly rate = monthly salary / (days x hours). Using 26 days is an assumption in this example, not a rule.
**Example:** Salary 31,200, 26 days, 8 hours: rate 150/hour. Hours 8.5, 10, 7.5, 9.25, 8 give 3.75 overtime hours; at 2x that is 1,125.
**Sample sheet:**

| | A | B | C | D | | F | G |
|---|---|---|---|---|---|---|---|
| 1 | Day | Hours | OT hrs | OT pay | | Monthly salary | 31,200 |
| 2 | Day 1 | 8.5 | 0.5 | 150 | | Std hrs/day | 8 |
| 3 | Day 2 | 10 | 2 | 600 | | Days/month | 26 |
| 4 | Day 3 | 7.5 | 0 | 0 | | OT multiplier | 2 |
| 5 | Day 4 | 9.25 | 1.25 | 375 | | Hourly rate | 150 |
| 6 | Day 5 | 8 | 0 | 0 | | | |
| 7 | | | 3.75 | 1,125 | | | |

**Formula / Steps:**
- G5: `=G1/(G3*G2)`
- C2: `=MAX(0,B2-$G$2)`
- D2: `=C2*$G$5*$G$4`; totals with SUM
**Alternative:** `=SUMPRODUCT((B2:B6>G2)*(B2:B6-G2))` gives total overtime hours in one cell (3.75).
**Result:** Run in LibreOffice 24.2: OT hours 0.5, 2, 0, 1.25, 0 (total 3.75); pay 150, 600, 0, 375, 0 (total 1,125); SUMPRODUCT also 3.75.
**Version note:** All versions and Google Sheets (Sheets from memory, unverified).
**Edge cases:** Hours stored as time values (8:30) need `*24`; weekly overtime rules differ from daily; floating-point hours may need ROUND; the legal multiplier and cut-offs depend on law and policy (not verified here).
**Likely follow-ups:** 1) *Weekly instead of daily?* Sum the week first, then MAX(0, week - 48 or policy). 2) *Weekend rates?* Add a day-type column and a lookup of multipliers.
**Common mistakes:** Letting negative overtime net against long days; hard-coding 1.5; dividing salary by 30 vs 26 without stating it.

### Q28 ⭐⭐ 🟡 How do you find employees who are in the HR master list but missing from the payroll sheet, and the reverse?
**Asked at:** commonly asked (no company-specific report found). Reconciliation is a standard prompt in MIS question lists (Dataford, snippet only).
**What the interviewer is checking:** Two-way comparison using a key column.
**Say this in the interview:** "I put a COUNTIF in the HR sheet that checks each ID against the payroll list, and a mirror COUNTIF in the payroll sheet against HR. Zero means missing. I trim and standardise IDs first."
**Explain simply:**
- A *key* is the column that identifies the same person in both sheets (Employee ID).
- COUNTIF returning 0 means the ID is not in the other list.
- Checking both directions matters because each list can have people the other lacks.
**Example:** HR has E1 to E6, payroll has E1, E2, E4, E6, E7, E8. E3 and E5 are missing in payroll (not paid, or on leave without pay?). E7 and E8 are paid but not in HR (ghost employees or late master update).
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | HR master | HR check | Payroll | Payroll check |
| 2 | E1 | OK | E1 | OK |
| 3 | E2 | OK | E2 | OK |
| 4 | E3 | Missing in payroll | E4 | OK |
| 5 | E4 | OK | E6 | OK |
| 6 | E5 | Missing in payroll | E7 | Not in HR master |
| 7 | E6 | OK | E8 | Not in HR master |

**Formula / Steps:**
- B2: `=IF(COUNTIF($C$2:$C$7,A2)=0,"Missing in payroll","OK")`
- D2: `=IF(COUNTIF($A$2:$A$7,C2)=0,"Not in HR master","OK")`
- Count: `=COUNTIF(B2:B7,"Missing*")`
**Alternative:** `=IF(ISNA(MATCH(A2,$C$2:$C$7,0)),"Missing","OK")`. In 365 `=FILTER(A2:A7,COUNTIF(C2:C7,A2:A7)=0)` lists them (not run here, LibreOffice 24.2 lacks FILTER).
**Result:** Run in LibreOffice 24.2: E3 and E5 flagged missing in payroll (count 2); E7 and E8 flagged not in HR master; the MATCH version agrees. FILTER version not run here; by hand it returns E3, E5.
**Version note:** COUNTIF and MATCH work everywhere; FILTER needs Excel 365/2021 (from memory, unverified); Sheets has FILTER (from memory, unverified).
**Edge cases:** Trailing spaces, text vs number IDs, leading zeros, duplicates (COUNTIF > 1), and COUNTIF treating "E1*" wildcards; use TRIM and a duplicate check first.
**Likely follow-ups:** 1) *Why not VLOOKUP?* It also works but returns #N/A you must wrap. 2) *What next after finding them?* Ask payroll and HR for the reason; do not edit silently.
**Common mistakes:** Checking one direction only; comparing different ID formats; deleting mismatches instead of explaining them.

### Q29 ⭐⭐ 🟡 How do you consolidate monthly files from several branches or teams into one report?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you pick Power Query for repeatable stacking, and know the manual options?
**Say this in the interview:** "If the files share the same layout I use Power Query's From Folder, which stacks every file into one table and refreshes next month. For a one-off, Data > Consolidate or a 3-D sum across identical sheets also works."
**Explain simply:**
- *Consolidate* means combining several tables into one summary.
- Power Query (Get & Transform) is Excel's built-in data-cleaning tool; "From Folder" reads every file in a folder.
- Microsoft says all files in the folder and subfolders are included, so keep unrelated files out; files should share headers, data types and column count (Microsoft Support, "Import data from a folder with multiple files (Power Query)", seen in a search summary).
- Add a Source column (branch name) so rows stay traceable.
**Example:** Pune sends 5 and 2 hires, Delhi sends 7. Combined: Pune 7, Delhi 7, total 14.
**Sample sheet (identical single-cell sheets for the 3-D example):**

| | A | B |
|---|---|---|
| Pune!1 | Branch | Hires |
| Pune!2 | Pune | 5 |
| Delhi!2 | Delhi | 7 |
| Chennai!2 | Chennai | 3 |

**Formula / Steps:**
1. Put all branch files in one folder (same column headers).
2. Data > Get Data > From File > From Folder; pick the folder; choose Combine > Combine & Load.
3. Check the file list, add a Source column, close and load.
4. Next month: add the new files and Data > Refresh All.
5. Formula route for same-layout sheets in one workbook: `=SUM(Pune:Chennai!B2)`
**Alternative:** Data > Consolidate (by position or by category); in 365, `=VSTACK(Sheet1!A1:D50,Sheet2!A1:D50)` (both named in Microsoft Support, "Combine data from multiple sheets", search summary).
**Result:** The 3-D formula was run in LibreOffice 24.2 and returns 15 (5+7+3), the same as adding the three cells by hand. The Power Query folder load is not run here; reproduced with pandas: Pune 7, Delhi 7.
**Version note:** Power Query is built in from Excel 2016 for Windows (from memory, unverified); VSTACK is 365 only (from memory, unverified). Consolidate may be missing in Excel for the web (Microsoft Support search summary).
**Edge cases:** Different header spellings, extra total rows inside source files, text numbers, and files left open; column order may differ but names must match.
**Likely follow-ups:** 1) *Why not copy-paste?* It breaks when a branch changes layout and cannot be audited. 2) *How to stop errors from a bad file?* Remove errors step and a row-count check.
**Common mistakes:** Leaving temp files in the folder; mixing header rows from each file; hard-coding file paths on one PC.

### Q30 ⭐⭐ 🟡 How do you rank employees by performance rating within each department?
**Asked at:** commonly asked (no company-specific report found). Rank formulas appear in the Novartis Excel case report in the repo's interview_processes.md (candidate report, unverified).
**What the interviewer is checking:** Conditional ranking, ties, and why plain RANK is not enough.
**Say this in the interview:** "I count how many people in the same department have a higher rating and add 1. That ranks within the group and handles ties as equal ranks. If a unique rank is needed I add a tie-break."
**Explain simply:**
- *Rank within a group* means each department starts again at 1.
- COUNTIFS with the department and ">"&rating counts better people in the same department.
- Ties get the same rank; the next rank is skipped (Microsoft Support, "RANK.EQ function", fetched, says duplicates share a rank and later ranks skip).
**Example:** Sales: Asha and Chitra both 4.5 are rank 1, Bala 4.0 is rank 3, Dev rank 4. A dense rank would say 1, 1, 2, 3.
**Sample sheet:**

| | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 1 | Dept | Emp | Rating | Rank | Dense | Unique |
| 2 | Sales | Asha | 4.5 | 1 | 1 | 1 |
| 3 | Sales | Bala | 4.0 | 3 | 2 | 3 |
| 4 | Sales | Chitra | 4.5 | 1 | 1 | 2 |
| 5 | Sales | Dev | 3.5 | 4 | 3 | 4 |
| 6 | IT | Esha | 4.8 | 1 | 1 | 1 |
| 7 | IT | Farid | 4.1 | 2 | 2 | 2 |
| 8 | IT | Gita | 4.1 | 2 | 2 | 3 |

**Formula / Steps:**
- D2: `=COUNTIFS($A$2:$A$8,A2,$C$2:$C$8,">"&C2)+1`
- E2 (dense): `=SUMPRODUCT(($A$2:$A$8=A2)*($C$2:$C$8>C2)/COUNTIFS($A$2:$A$8,$A$2:$A$8,$C$2:$C$8,$C$2:$C$8))+1`
- F2 (unique): `=D2+COUNTIFS($A$2:A2,A2,$C$2:C2,C2)-1`
**Alternative:** PivotTable with Rating, Show Values As > Rank Largest to Smallest, base field Dept (not run here). Plain `=RANK.EQ(C2,$C$2:$C$8)` ranks across all departments, not within.
**Result:** Run in LibreOffice 24.2: rank 1,3,1,4,1,2,2; dense 1,2,1,3,1,2,2; unique 1,3,2,4,1,2,3.
**Version note:** RANK.EQ is listed for Excel 2016 to 365 (Microsoft Support); the COUNTIFS method works in every version; Sheets from memory, unverified.
**Edge cases:** Blank ratings count as lower in some layouts (filter them out); text ratings are ignored by ">"; tie-break rule must be agreed (employee ID, tenure).
**Likely follow-ups:** 1) *RANK vs DENSE_RANK?* Skip vs no skip. 2) *Top 3 per department?* Filter rank <= 3.
**Common mistakes:** Using RANK across the whole list; forgetting `$`; not stating how ties are treated.

### Q31 ⭐⭐ 🟡 How do you speed up a slow, heavy Excel workbook?
**Asked at:** commonly asked (no company-specific report found). Slowness appears among the MIS questions seen in snippets (spreadsheetweb, Microsoft performance article).
**What the interviewer is checking:** Do you diagnose before changing things, and know the usual causes?
**Say this in the interview:** "I first switch to manual calculation to confirm formulas are the cause. Then I cut whole-column references, repeated lookups and volatile functions, convert finished formulas to values, trim unused ranges and formatting, and move heavy joins into Power Query."
**Explain simply:**
- *Calculation mode* decides when Excel recalculates; Formulas > Calculation Options > Manual recalculates only on F9. Microsoft suggests manual mode to test whether automatic recalculation causes the slowness (Microsoft Support, "Change formula recalculation, iteration, or precision in Excel", search summary).
- *Volatile functions* (TODAY, NOW, OFFSET, INDIRECT) recalculate on every change; Microsoft advises limiting them, calculating TODAY once and referencing that cell (Microsoft Support, "Clean up an Excel workbook so that it uses less memory", search summary).
- Lookup-style array formulas (LOOKUP, INDEX, MATCH) and whole-column references use heavy memory (same page).
- Cell-level extras: heavy conditional formatting, huge used ranges and file size (spreadsheetweb.com, snippet only).
**Example:** A payroll file with 80,000 rows and 12 columns of VLOOKUP on full columns takes a minute to recalc. Replacing them with one lookup key column and a MATCH done once drops the work.
**Formula / Steps:**
1. Formulas > Calculation Options > Manual; time the F9 recalculation.
2. Replace `A:A` with exact ranges or a Table reference.
3. Compute `MATCH` once in a helper column, then `INDEX` several columns from it.
4. Copy > Paste Special > Values for finished history.
5. Remove unused formatting (Home > Find & Select > Go To Special) and save as .xlsx or .xlsb.
6. Move merges and joins to Power Query; consider 64-bit Excel for big files.
**Alternative:** Split data and report into separate files; or use the Data Model for millions of rows (see Q40).
**Version note:** The steps are the same across 2016 to 365; XLOOKUP/XMATCH in 365 are said to be faster for lookups on the Microsoft performance page (only the page intro was seen, so unverified). Sheets differs: from memory, unverified.
**Edge cases:** Manual mode can leave stale numbers (Excel shows strikethrough on stale cells in manual mode, per the Microsoft search summary); calculation mode is shared by all open workbooks.
**Likely follow-ups:** 1) *What if it is still slow?* Profile by sheet; remove one block at a time. 2) *Is deleting formatting safe?* Yes for blank cells, check first.
**Common mistakes:** Leaving the workbook on manual and forgetting to recalculate before sending; replacing formulas with values without a backup.

### Q32 ⭐⭐ 🟡 How do you find employees with more than a set number of absences in the last 12 months?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Rolling date windows and COUNTIFS with date criteria.
**Say this in the interview:** "I keep the as-of date and the limit in input cells, compute the window start with EDATE, and count each employee's absence dates inside the window. Anyone over the limit gets a Review flag."
**Explain simply:**
- A *rolling window* always looks back a fixed time from a chosen date.
- EDATE(date, -12) moves back 12 months; add 1 day to avoid counting the same day twice.
- COUNTIFS counts rows that satisfy several conditions, including date ranges.
**Example:** As of 31-Dec-2025 with limit 3: E1 has absences on 3-Feb, 12-May, 1-Aug, 20-Oct (4 in window; a Sep-2024 absence falls outside), so E1 is flagged; E2 has 2; E3 has 4.
**Sample sheet:**

| | A | B | | D | E | | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Emp | Absence date | | As-of | 31-Dec-25 | | Emp | Days in 12m | Flag |
| 2 | E1 | 03-Feb-25 | | Limit | 3 | | E1 | 4 | Review |
| 3 | E1 | 12-May-25 | | Window start | 01-Jan-25 | | E2 | 2 | OK |
| 4 | E1 | 01-Aug-25 | | | | | E3 | 4 | Review |
| 5 | E1 | 20-Oct-25 | | | | | | | |
| 6-12 | E1 05-Sep-24; E2 03-Mar-25, 09-Sep-25; E3 06-Jun, 07-Jun, 07-Jul, 21-Nov-25 | | | | | | | | |

**Formula / Steps:**
- E3: `=EDATE(E1,-12)+1`
- H2: `=COUNTIFS($A$2:$A$12,G2,$B$2:$B$12,">="&$E$3,$B$2:$B$12,"<="&$E$1)`
- I2: `=IF(H2>$E$2,"Review","OK")`
**Alternative:** PivotTable with a date filter (not run here); or `=SUMPRODUCT(($A$2:$A$12=G2)*($B$2:$B$12>=$E$3)*($B$2:$B$12<=$E$1))`.
**Result:** Run in LibreOffice 24.2: E1 = 4 (Review), E2 = 2 (OK), E3 = 4 (Review); window start 01-Jan-2025.
**Version note:** EDATE and COUNTIFS work in all versions and Sheets (Sheets from memory, unverified).
**Edge cases:** Half-day leave, weekends and holidays in the log, approved vs unapproved absence types (add a type condition), and using TODAY() instead of a fixed as-of date makes reports change when reopened.
**Likely follow-ups:** 1) *More than or at least?* "More than 3" is `>3`. 2) *Consecutive absences?* Needs sorted dates and a gap check.
**Common mistakes:** Using TODAY() so last month's report cannot be reproduced; counting leave types that are not absences.

### Q33 ⭐⭐ 🟡 How do you build a leave balance tracker from opening balance, leaves taken and leaves credited?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Balance logic and pulling taken leave from a log with SUMIFS.
**Say this in the interview:** "Balance equals opening plus credited minus taken. Taken comes from the leave log with SUMIFS on the employee ID, and I flag negative balances."
**Explain simply:**
- *Opening balance* is leave left at the start of the period; *credited* is leave added (monthly accrual); *taken* is leave used.
- Keeping a separate log means nobody edits the balance by hand.
- A negative balance usually means leave without pay or an error.
**Example:** E3 opens with 3 days, is credited 1.5, and takes 8 (4+3+1): balance -3.5, flagged.
**Sample sheet:**

| | A | B | C | D | E | F | | H | I |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Emp | Opening | Credited | Taken | Balance | Flag | | Month | Days |
| 2 | E1 | 2 | 1.5 | 3 | 0.5 | | | Jan (E1) | 1 |
| 3 | E2 | 0 | 1.5 | 1 | 0.5 | | | Mar (E1) | 2 |
| 4 | E3 | 3 | 1.5 | 8 | -3.5 | Negative | | Feb (E2) | 1 |
| 5 | E4 | 5 | 1.5 | 0 | 6.5 | | | (E3: Jan 4, Apr 3, May 1) | |

(The log lives in G2:I7 with columns Emp, Month, Days.)
**Formula / Steps:**
- D2: `=SUMIFS($I$2:$I$7,$G$2:$G$7,A2)`
- E2: `=B2+C2-D2`
- F2: `=IF(E2<0,"Negative","")`
**Alternative:** PivotTable on the log, then a lookup of the pivot result (not run here).
**Result:** Run in LibreOffice 24.2: taken 3, 1, 8, 0; balances 0.5, 0.5, -3.5, 6.5; only E3 flagged.
**Version note:** SUMIFS works in all versions listed by Microsoft Support (2016 to 365); Sheets from memory, unverified.
**Edge cases:** Half days, carry-forward caps, leave types with different rules, joiners with pro-rata credit; the log should be a Table so SUMIFS ranges grow.
**Likely follow-ups:** 1) *Carry-forward cap?* `=MIN(cap, balance)` at year end. 2) *Per leave type?* Add a type condition to SUMIFS.
**Common mistakes:** Typing the balance directly; fixed ranges that miss new log rows; mixing leave types in one balance.

### Q34 ⭐⭐ 🟡 Which would you use for a recurring daily MIS report: manual formulas, Power Query or a macro, and why?
**Asked at:** commonly asked (no company-specific report found). MIS roles in JDs mention VLOOKUP, pivots and macros (Ninjacart MIS JD in the repo's research files).
**What the interviewer is checking:** Judgement: right tool for the repeat frequency and the person who maintains it.
**Say this in the interview:** "For a daily report I would use Power Query for the cleaning and joining, because it refreshes with one click and records every step. Formulas and pivots sit on top for the summary. I would add a macro only for what Power Query cannot do, such as emailing or formatting a final sheet."
**Explain simply:**
- *Manual formulas*: quick for small one-offs, but repeated copy-paste each day causes errors.
- *Power Query*: records cleaning steps; refresh reapplies them to new data. No code writing needed.
- *Macro (VBA)*: recorded or coded automation of clicks; powerful but needs an .xlsm file, security prompts and someone who can maintain code.
- The test: how often does it run, how messy is the data, who inherits it?
**Example:** Daily attendance export, 5,000 rows, 20 minutes of manual cleaning. With Power Query it becomes one Refresh All (a few seconds, my estimate, not measured); the macro just saves and mails the PDF.
**Formula / Steps (not run here):**
1. Data > Get Data > From File and load the daily export (or a folder).
2. Apply cleaning steps once (types, remove blanks, merge with master).
3. Close & Load to a Table; pivots and formulas reference that Table.
4. Daily: replace the file, then Data > Refresh All.
5. Optional macro for save/PDF/email.
**Alternative:** Office Scripts or Power Automate (365) for cloud schedules; Python for large or messy jobs (not covered here).
**Version note:** Power Query is built in from Excel 2016 on Windows; VBA needs desktop Excel and macro-enabled files (both from memory, unverified).
**Edge cases:** Source column renamed (query breaks); IT policy blocks macros; refresh does not run when the file is closed.
**Likely follow-ups:** 1) *When is a macro better?* UI tasks, formatting, email. 2) *How do you handle a failed refresh?* Check the failed step and a row-count control.
**Common mistakes:** Building a macro for what Power Query does; unnamed steps; no check totals after refresh.

### Q35 ⭐⭐ 🟡 How do you build a report that shows each month's figure as a percentage of the annual total?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Absolute reference ($) for the total.
**Say this in the interview:** "Each month divided by the annual total, with the total locked using dollar signs so it does not move when I fill down. I check the percentages add to 100%."
**Explain simply:**
- A *percentage of total* shows each part's share.
- Without `$`, the total cell shifts as you copy the formula, giving wrong or #DIV/0! results.
- A check cell that sums the shares to 100% catches mistakes.
**Example:** Monthly hires across the year: 120, 95, 130, ... total 1,400. January share is 120/1,400 = 8.6%.
**Sample sheet:** (12 months in rows 2-13; first rows shown)

| | A | B | C |
|---|---|---|---|
| 1 | Month | Hires | % of year |
| 2 | M1 | 120 | 8.6% |
| 3 | M2 | 95 | 6.8% |
| 4 | M3 | 130 | 9.3% |
| 5 | M4 | 110 | 7.9% |
| 6-13 | M5 to M12: 105, 140, 125, 100, 115, 135, 90, 135 | | |
| 14 | Total | 1,400 | 100% |

**Formula / Steps:**
- C2: `=B2/SUM($B$2:$B$13)`, filled down; format as %
- Check: `=SUM(C2:C13)`
**Alternative:** `=B2/$B$14` with a total cell; or PivotTable, Show Values As > % of Grand Total (not run here).
**Result:** Run in LibreOffice 24.2: total 1,400; shares 0.0857, 0.0679, 0.0929, 0.0786, 0.075, 0.1, 0.0893, 0.0714, 0.0821, 0.0964, 0.0643, 0.0964; check cell 1.
**Version note:** All versions and Sheets (Sheets from memory, unverified).
**Edge cases:** A zero total gives #DIV/0!; if the year is incomplete the shares are of the partial total, so label it; negative months make shares exceed 100%.
**Likely follow-ups:** 1) *Cumulative %?* Running sum divided by total. 2) *Share within a department?* Use SUMIFS as the denominator.
**Common mistakes:** Missing `$`; formatting as % after multiplying by 100; total range that excludes the last month.

### Q36 ⭐⭐ 🟡 How do you build a department-wise cost summary with subtotals and a grand total for a management report?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** SUBTOTAL vs SUM, and avoiding double counting.
**Say this in the interview:** "I sort by department and use Data > Subtotal, or SUBTOTAL(9, ...) formulas per department. The grand total also uses SUBTOTAL so Excel ignores the subtotal rows instead of double counting them."
**Explain simply:**
- *Subtotal* is a mid-level total for a group.
- SUBTOTAL(9, range) is a sum that skips other SUBTOTAL results in the range (Microsoft Support, "SUBTOTAL function", fetched). It also ignores rows removed by a filter.
- 9 includes manually hidden rows; 109 ignores them (same page).
**Example:** HR 230,000 + IT 1,050,000 + Sales 570,000 = 1,850,000. A plain SUM over the same range returns 3,700,000 (double counted).
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 2 | HR | Salary | 200,000 |
| 3 | HR | Training | 30,000 |
| 4 | HR Total | | 230,000 |
| 5 | IT | Salary | 900,000 |
| 6 | IT | Tools | 150,000 |
| 7 | IT Total | | 1,050,000 |
| 8-10 | Sales Salary 500,000; Travel 70,000; Sales Total 570,000 | | |
| 11 | Grand Total | | 1,850,000 |

**Formula / Steps:**
- C4: `=SUBTOTAL(9,C2:C3)`, C7: `=SUBTOTAL(9,C5:C6)`, C10: `=SUBTOTAL(9,C8:C9)`
- C11: `=SUBTOTAL(9,C2:C10)`
- Feature route: sort by Dept, Data > Subtotal > At each change in: Dept; Use function: Sum; Add subtotal to: Cost.
**Alternative:** SUMIF per department and `=SUM` of those; or PivotTable with subtotals (not run here).
**Result:** Run in LibreOffice 24.2: subtotals 230,000; 1,050,000; 570,000; SUBTOTAL grand total 1,850,000; plain `=SUM(C2:C10)` returns 3,700,000 (double counted).
**Version note:** SUBTOTAL is listed for Excel 2016 to 365 (Microsoft Support); Sheets has SUBTOTAL (from memory, unverified).
**Edge cases:** Inserted rows outside the range; filtered views change the total (a feature, but say so); Data > Subtotal needs sorted data and is removed with Remove All.
**Likely follow-ups:** 1) *9 vs 109?* Hidden rows. 2) *Why not a PivotTable?* Pivots are fine; Subtotal gives a printable layout.
**Common mistakes:** Using SUM for the grand total over subtotal rows; unsorted data before Data > Subtotal.

### Q37 ⭐⭐ 🔴 How do you calculate a rolling 12-month attrition rate?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you divide 12 months of leavers by an average headcount, and can you explain the choice?
**Say this in the interview:** "I add up leavers in the last 12 months and divide by the average headcount over the same window, then multiply by 100. For the average I use the start and end headcount, as the standard formula does."
**Explain simply:**
- *Rolling* means the window moves forward each month, so every month shows the latest 12-month figure.
- AIHR (aihr.com, "Attrition rate", fetched) gives attrition % = employees who left / average employees x 100, with average = (start + end) / 2, and says organisations track monthly, quarterly or annually. It does not describe a rolling 12-month method; applying the formula to a moving 12-month window is my own extension.
- Using the average rather than only the closing headcount avoids flattering a growing company.
**Example:** Headcount was 100 at the start of the window and 113 at the end. 22 people left in 12 months: 22 / 106.5 = 20.7%.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Month | Month-end HC | Leavers | Rolling 12m % |
| 2 | Dec (start) | 100 | 0 | |
| 3 | Jan | 102 | 2 | |
| 4 | Feb | 101 | 3 | |
| 5-13 | Mar to Nov: HC 104, 103, 106, 108, 107, 109, 111, 110, 112 | | | |
| 14 | Dec2 | 113 | 1 | 20.7% |

(Leavers Jan to Dec2: 2,3,1,2,2,1,3,2,1,2,2,1 = 22.)
**Formula / Steps:**
- D14: `=SUM(C3:C14)/AVERAGE(B2,B14)`, then fill down each later month so the window slides
**Alternative:** Average of all 13 month-end headcounts: `=SUM(C3:C14)/AVERAGE(B2:B14)`.
**Result:** Run in LibreOffice 24.2: 0.2066 (20.7%) for the first method; 0.2063 for the 13-point average. The two agree to the first decimal.
**Version note:** Plain SUM/AVERAGE work in every version and Sheets (Sheets from memory, unverified); no dynamic arrays are used.
**Edge cases:** Fewer than 12 months of history (do not annualise silently); rapid growth or shrinking; include or exclude involuntary exits and say which.
**Likely follow-ups:** 1) *Why not use closing headcount only?* It understates attrition in a growing team. 2) *Annualised monthly rate?* Monthly rate x 12 is a rough approximation.
**Common mistakes:** Dividing by the current month's headcount only; windows of 11 or 13 months from off-by-one ranges; mixing voluntary and total without a label.

### Q38 ⭐⭐ 🔴 Case: given a sales table (Region, Product, Month, Sales), how would you produce a summary with pivot, rank and formulas in a timed Excel test?
**Asked at:** Novartis: a March 2023 candidate report describes an Excel case study with pivots, rank and formulas (research/interview_processes.md; Glassdoor candidate report, unverified). Otherwise commonly asked (no company-specific report found).
**What the interviewer is checking:** Speed and order: clean, pivot, check with formulas, rank, state insights.
**Say this in the interview:** "First I make it a Table and check for blanks, duplicates and text numbers. Then a PivotTable for region by product, SUMIFS to cross-check, RANK for ordering regions, share-of-total for context, and a two-line insight at the end."
**Explain simply:**
- Under time pressure: clean first (1-2 minutes), summarise (pivot), verify (a second method), then present.
- A *PivotTable* summarises by region and product without formulas.
- RANK orders the regions; share of total shows weight.
- Always write one insight sentence, since interviewers listen for that.
**Example:** Eight sales rows: East 300 (42.3%), West 300 (42.3%), North 110 (15.5%); total 710. Laptop 440, Phone 270.
**Sample sheet:**

| | A | B | C | D | | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Region | Product | Month | Sales | | Region | Total | Share | Rank |
| 2 | East | Laptop | Jan | 120 | | East | 300 | 42.3% | 1 |
| 3 | East | Phone | Jan | 80 | | North | 110 | 15.5% | 3 |
| 4 | West | Laptop | Jan | 150 | | West | 300 | 42.3% | 1 |
| 5 | West | Phone | Jan | 60 | | Total | 710 | | |
| 6-9 | East Laptop Feb 100; West Phone Feb 90; North Laptop Feb 70; North Phone Jan 40 | | | | | | | | |

**Formula / Steps:**
1. Ctrl+T to make a Table; check totals with `=SUM(D2:D9)`.
2. Insert > PivotTable: Rows Region, Columns Product, Values Sum of Sales (not run here).
3. G2: `=SUMIFS($D$2:$D$9,$A$2:$A$9,F2)`; H2: `=G2/$G$5`; I2: `=RANK.EQ(G2,$G$2:$G$4,0)`
4. State the insight, for example: "East and West tie at 42% each; North is the smallest region."
**Alternative:** In 365, `=SORTBY(...)`/`=GROUPBY(...)` (not run here, newer functions); or a pivot with Show Values As > Rank.
**Result:** Formulas run in LibreOffice 24.2: totals 300, 110, 300 (710); shares 0.4225, 0.1549, 0.4225; ranks 1, 3, 1 (East and West tie, rank 2 is skipped). The PivotTable was not run here; reproduced with pandas: East Laptop 220 / Phone 80, North 70 / 40, West 150 / 150, totals Laptop 440, Phone 270, all 710.
**Version note:** RANK.EQ listed for Excel 2016 to 365 (Microsoft Support, "RANK.EQ function"); pivots work in all versions. GROUPBY/SORTBY availability from memory, unverified.
**Edge cases:** Ties in rank, text numbers, blank months, duplicate rows, a region typed two ways.
**Likely follow-ups:** 1) *Month-wise trend?* Months in Columns of the pivot. 2) *Top product per region?* Pivot sorted by value, or INDEX/MATCH on the product totals.
**Common mistakes:** Pivot without checking totals; skipping the insight sentence; spending time formatting first.

### Q39 ⭐ 🟢 How do you share an Excel report with a team without people breaking it or creating conflicting versions?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Process thinking: one source of truth, protection, version control.
**Say this in the interview:** "I keep one master on a shared drive such as OneDrive or SharePoint, protect formulas and unlock input cells, and send people a read-only view or a PDF. Edits happen only in the master, and I keep a change log and dated backups."
**Explain simply:**
- *One source of truth* means a single master file, not copies in email.
- *Protect Sheet* locks formulas; people can still type in unlocked input cells (Microsoft Support, "Protect a worksheet", search summary: unlock editable cells first, then protect; sheet protection is not a security feature).
- Co-authoring in the cloud lets several people edit one file; version history lets you restore (from memory, unverified).
- Read-only copies or PDFs prevent edits when people only need to read.
**Example:** A monthly attrition report is edited by three HR analysts. The master sits on a shared drive; each analyst owns one input tab; finished numbers go to managers as a PDF.
**Formula / Steps:**
1. Select input cells > Format Cells > Protection > untick Locked.
2. Review > Protect Sheet (set a password only if needed and store it safely).
3. Data > Data Validation on input cells (drop-downs, date or number limits).
4. Save to OneDrive/SharePoint; Share with Can view or Can edit as needed.
5. Add a "Read me / change log" tab; file name with date, for example `Attrition_2026-10.xlsx`.
**Alternative:** Publish a Power BI report or send a PDF for readers only (not run here).
**Version note:** The older Shared Workbook feature still has a Microsoft Support merge page ("Merge copies of a Shared Workbook", search result title), but I rely on cloud co-authoring in modern Excel (from memory, unverified). Sheets handles sharing natively (from memory, unverified).
**Edge cases:** Protection with no password is easy to remove (Microsoft Support); macros do not run in the browser version; links to local paths break for others.
**Likely follow-ups:** 1) *Is sheet protection secure?* No, it prevents accidents, not determined users. 2) *What about sensitive pay data?* Use access permissions, not just passwords.
**Common mistakes:** Emailing multiple copies; protecting without unlocking inputs; relying on a password you then lose.

### Q40 ⭐ 🟢 What would you do if your data has more rows than Excel's row limit?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the limit and the escape routes?
**Say this in the interview:** "A worksheet holds 1,048,576 rows. If I have more, I do not force it into a sheet. I load the data into the Data Model through Power Query and summarise with a PivotTable, or I aggregate it in a database or Python first and bring the summary into Excel."
**Explain simply:**
- Microsoft's limit is 1,048,576 rows by 16,384 columns per worksheet (Microsoft Support, "Excel specifications and limits", fetched).
- The *Data Model* is Excel's internal compressed store; data loaded there is not limited by sheet rows. Its size is bounded by memory: in 32-bit Excel the data model's share can be roughly 500 to 700 MB, while 64-bit has no hard file-size limit (same page).
- Opening a big CSV directly loads only the first 1,048,576 rows (Excel shows a warning, from memory, unverified), so check the source row count first.
- If you only need totals, filter or aggregate before loading.
**Example:** A 3-million-row attendance export arrives. Power Query loads it to the Data Model only; a PivotTable shows days present by department. Excel itself never stores the rows on a sheet.
**Sample sheet:** not meaningful. The limit check was run: `=ROWS(A:A)` returns 1048576 and `=COLUMNS(1:1)` returns 16384 in LibreOffice 24.2 (matches Microsoft's figures).
**Formula / Steps (not run here):**
1. Data > Get Data > From File > From Text/CSV > Transform Data.
2. Filter columns and rows you do not need; remove unused columns.
3. Close & Load To... > Only Create Connection > tick Add this data to the Data Model.
4. Insert > PivotTable > Use this workbook's Data Model.
**Alternative:** Split into several sheets or files; summarise in SQL or pandas first and paste results; use Power BI for big data.
**Version note:** The row limit applies across modern versions (the specifications page); Data Model/Power Pivot availability varies by edition and version (from memory, unverified). Google Sheets has a different cell limit (from memory, unverified).
**Edge cases:** Formulas on the Data Model need DAX measures, not normal cell formulas; 32-bit Excel runs out of memory sooner; a CSV opened normally is truncated at the row limit.
**Likely follow-ups:** 1) *Can you see all rows then?* Not on a sheet; you see summaries. 2) *When do you stop using Excel?* When refresh is slow or data is shared across teams: use a database.
**Common mistakes:** Opening a huge CSV by double-click, ignoring the warning and trusting the totals; splitting by hand into many sheets that no longer reconcile.

### Q41 ⭐ 🟢 How do you document and hand over a recurring report so someone else can run it?
**Asked at:** Indeed India MIS-executive question list (fetched) includes routine and handover questions; no company-specific report found.
**What the interviewer is checking:** Can someone else run your report on day one without calling you?
**Say this in the interview:** "I write a one-page runbook: where the data comes from, the exact steps, the checks, the owner and the deadline. Then I make the person who is taking over run it once while I watch."
**Explain simply:**
- Runbook = a short written recipe for the report. Anyone should be able to follow it without asking you.
- Put it in the workbook itself on a 'README' sheet, so the instructions travel with the file.
- Cover six things: purpose and audience, data source and refresh time, step-by-step process, formula/field definitions (for example how 'attrition %' is calculated), checks and control totals, and who to call.
- Add a built-in control total, so the file tells the next person when something went wrong.
**Example:** Monthly payroll MIS: the README says 'Download the payroll register from HRMS by the 3rd, paste into Data!A1, refresh, check cell F2 says OK, send by 5 pm to the CFO.' The handover person ran it once with you watching, then once alone.
**Sample sheet:**

| row | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 1 | Employee | Net pay |  | Report total | Source (HRMS) total | Check |
| 2 | E01 | 42000 |  | 179000 | 179000 | OK |
| 3 | E02 | 51000 |  |  |  |  |
| 4 | E03 | 38500 |  |  |  |  |
| 5 | E04 | 47500 |  |  |  |  |

**Formula / Steps:** 1. Add a sheet named README (Home tab > right-click sheet tab > Insert). 2. Write the six headings above. 3. Name input cells (Formulas tab > Defined Names > Define Name) and protect formula cells (Review tab > Protect Sheet). 4. Add the control check: `D2 =SUM(B2:B5)`, `F2 =IF(D2=E2,"OK","CHECK")`, where E2 is the total printed by the source system.
**Alternative:** A 3-minute screen recording of one full run plus a change log sheet (date, who, what changed). Or a Power Query refresh with the steps saved in the query (not run here).
**Result:** Run in LibreOffice: D2 = 179000, F2 = "OK". If the source total were 181000 the same formula returns "CHECK".
**Version note:** Defined names, Protect Sheet and the SUM/IF check work in every Excel version (from memory, unverified). Sheets has the same checks.
**Edge cases:** Data pasted with a different column order breaks formulas; put a header check (`=IF(Data!A1="Employee","OK","Headers changed")`). Totals that match by luck are rare, but also record row counts.
**Likely follow-ups:** 1) *What if the source layout changes?* The header check fails loudly. 2) *Where do you store it?* Shared drive with version name and the change log.
**Common mistakes:** Handing over only the file with no steps; keeping logic in your head; hardcoded paths to your own laptop folders.

### Q42 ⭐ 🟡 How do you check the salary data for outliers and wrong entries?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you sanity-check numbers before they reach payroll or a report?
**Say this in the interview:** "First I look for impossible values: text, blanks, zero, negatives. Then I use a statistical fence, Q3 plus 1.5 times the IQR, to flag extreme values, and I check each flagged row with the source before changing anything."
**Explain simply:**
- Wrong entry = typo such as an extra zero, a salary stored as text, a blank or zero.
- Quartiles split sorted data into four equal parts. Q1 is the 25% mark, Q3 the 75% mark; the gap between them is the IQR (inter-quartile range, the 'middle half' spread).
- The IQR rule: anything above Q3 + 1.5 x IQR or below Q1 - 1.5 x IQR is a suspected outlier (a flag, not proof).
- Always confirm with the source; a CEO salary can be a real outlier.
**Example:** Seven salaries are between 39,000 and 48,000 and one is 450,000 (an extra zero on 45,000). One more was typed as text '46000', which Excel ignores in totals and quartiles.
**Sample sheet:**

| row | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 1 | Emp | Salary | Flag |  |  |  |
| 2 | E01 | 42000 | OK |  | Q1 | 41500 |
| 3 | E02 | 45000 | OK |  | Q3 | 46500 |
| 4 | E03 | 39000 | OK |  | Upper fence | 54000 |
| 5 | E04 | 48000 | OK |  | Lower fence | 34000 |
| 6 | E05 | 41000 | OK |  |  |  |
| 7 | E06 | 450000 | Outlier |  |  |  |
| 8 | E07 | 44000 | OK |  |  |  |
| 9 | E08 | 46000 | Text entry |  |  |  |

**Formula / Steps:** `F2 =QUARTILE(B2:B9,1)`, `F3 =QUARTILE(B2:B9,3)`, `F4 =F3+1.5*(F3-F2)`, `F5 =F2-1.5*(F3-F2)`, then in C2 fill down: `=IF(ISTEXT(B2),"Text entry",IF(OR(B2<$F$5,B2>$F$4),"Outlier","OK"))`.
**Alternative:** Compare each salary with its grade's min and max from a band table (more business-meaningful), or use conditional formatting > Top/Bottom Rules > Above Average; or a box plot (Insert > Statistics chart, not run here).
**Result:** Run: Q1 = 41500, Q3 = 46500, fences 34000 to 54000. Flags: E06 = Outlier, E08 (text) = Text entry, all others OK.
**Version note:** QUARTILE works in all versions; QUARTILE.INC is the modern name (from memory, unverified).
**Edge cases:** Text numbers are skipped by QUARTILE (so quartiles use 7 values here); zero salaries would drag Q1 down, so filter them first; with tiny groups the fence is unstable; Excel and LibreOffice agree on QUARTILE (inclusive method) here.
**Likely follow-ups:** 1) *Why 1.5?* Tukey's convention, a common default. 2) *Mean or median for checking?* Median, because outliers distort the mean.
**Common mistakes:** Deleting outliers without asking; checking only the max; forgetting text-stored numbers.

### Q43 ⭐ 🟡 How do you calculate compa-ratio (salary against the band midpoint) for each employee?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine a lookup with simple division, and do you understand pay positioning?
**Say this in the interview:** "Compa-ratio is salary divided by the midpoint of the pay band for the employee's grade. 1.00 means paid at the midpoint, below 1 is under the middle, above 1 is over it. I look up the midpoint by grade, then divide."
**Explain simply:**
- Pay band = the min-to-max salary range set for a grade; midpoint = (min + max) / 2.
- Compa-ratio = salary / midpoint. About 0.8-1.2 is a typical range, but companies set their own (from memory).
- Used for pay reviews: many people below 0.9 in one team means a pay-equity or attrition risk.
**Example:** Grade L2 band is 50,000-70,000 so the midpoint is 60,000. E03 earns 66,000, so compa-ratio = 66,000 / 60,000 = 1.10.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Emp | Grade | Salary | Compa-ratio |  | Grade | Min | Max | Midpoint |
| 2 | E01 | L1 | 36000 | 0.9 | 0.9 | L1 | 30000 | 50000 | 40000 |
| 3 | E02 | L1 | 48000 | 1.2 |  | L2 | 50000 | 70000 | 60000 |
| 4 | E03 | L2 | 66000 | 1.1 |  | L3 | 80000 | 120000 | 100000 |
| 5 | E04 | L2 | 54000 | 0.9 |  |  |  |  |  |
| 6 | E05 | L3 | 95000 | 0.95 |  |  |  |  |  |
| 7 | E06 | L3 | 110000 | 1.1 |  |  |  |  |  |

**Formula / Steps:** `I2 =(G2+H2)/2` (fill down), then `D2 =ROUND(C2/VLOOKUP(B2,$F$2:$I$4,4,FALSE),2)`. FALSE forces an exact grade match.
**Alternative:** `=C2/INDEX($I$2:$I$4,MATCH(B2,$F$2:$F$4,0))` (in E2). In 365, `=C2/XLOOKUP(B2,$F$2:$F$4,$I$2:$I$4)` (not run here: LibreOffice 24.2 has no XLOOKUP).
**Result:** Run: D2:D7 = 0.9, 1.2, 1.1, 0.9, 0.95, 1.1; INDEX/MATCH in E2 = 0.9 (same as D2).
**Version note:** VLOOKUP and INDEX/MATCH work in every version; XLOOKUP is 365/2021+ (Microsoft Support, "XLOOKUP function": its applies-to list names 2016/2019 but its own note says it is not available there, so treat it as 2021 and 365 only).
**Edge cases:** A grade missing from the table gives #N/A: wrap in IFERROR(...,"No band"). Grade typed with a trailing space breaks the match (TRIM it). Never use approximate match (TRUE) here. Compare like with like: part-time and different currencies need adjusting.
**Likely follow-ups:** 1) *Below 0.8?* Flag for review. 2) *Why not salary vs average?* Midpoint is the policy target, the average is whatever history gave you.
**Common mistakes:** Using the band minimum instead of the midpoint; hardcoding midpoints; approximate match.

### Q44 ⭐ 🟡 How do you track training completion by department against a target?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build a simple tracking table with a target and a status flag?
**Say this in the interview:** "I count how many were assigned and how many completed per department with COUNTIF and COUNTIFS, divide for the percentage, and compare it with the target to show on or below target."
**Explain simply:**
- COUNTIF counts rows that meet one condition; COUNTIFS counts rows meeting several at once.
- Completion % = completed / assigned. Never average the department percentages: a 3-person team would weigh the same as a 300-person one. Use the Total row's own division.
- Keep the target in one cell (L1) so it can change without editing formulas.
**Example:** Sales: 3 assigned, 2 done = 66.7%, below a 90% target. HR: 2 of 2 = 100%.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Emp | Dept | Training done |  | Dept | Assigned | Completed | Completion % | vs target |  | Target | 0.9 |
| 2 | E01 | Sales | Yes |  | Sales | 3 | 2 | 0.6667 | Below target |  |  |  |
| 3 | E02 | Sales | Yes |  | HR | 2 | 2 | 1 | On target |  |  |  |
| 4 | E03 | Sales | No |  | IT | 3 | 1 | 0.3333 | Below target |  |  |  |
| 5 | E04 | HR | Yes |  | Total | 8 | 5 | 0.625 |  |  |  |  |
| 6 | E05 | HR | Yes |  |  |  |  |  |  |  |  |  |
| 7 | E06 | IT | Yes |  |  |  |  |  |  |  |  |  |
| 8 | E07 | IT | No |  |  |  |  |  |  |  |  |  |
| 9 | E08 | IT | No |  |  |  |  |  |  |  |  |  |

**Formula / Steps:** `F2 =COUNTIF($B$2:$B$9,E2)`, `G2 =COUNTIFS($B$2:$B$9,E2,$C$2:$C$9,"Yes")`, `H2 =G2/F2`, `I2 =IF(H2>=$L$1,"On target","Below target")`; total `H5 =G5/F5`.
**Alternative:** A pivot table on Dept with Count of Completed set to 'Show Values As > % of Row Total' (not run here), plus conditional formatting on the % column.
**Result:** Run: completion % Sales = 0.6667, HR = 1, IT = 0.3333; overall = 0.625; statuses: Below target, On target, Below target.
**Version note:** COUNTIFS is in Excel 2007 and later (from memory, unverified); all versions fine.
**Edge cases:** A dept with zero assigned gives #DIV/0!: wrap in IF(F2=0,"",...). 'yes ' with a trailing space or 'Y' will not match: standardise first. Employees who left during the year should be removed from the assigned count.
**Likely follow-ups:** 1) *Overdue vs pending?* Add a due-date column and a COUNTIFS on date < today. 2) *Show visually?* Bar with a target line.
**Common mistakes:** Averaging percentages; typing the target into each formula; counting leavers as non-compliant.

### Q45 ⭐ 🟡 How do you calculate the headcount of each manager's team (span of control) from an employee list with a manager ID?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you count 'how many rows point at this ID' with COUNTIF?
**Say this in the interview:** "Each employee row stores their manager's ID. To get a manager's team size, I count how many times their own ID appears in the manager-ID column, using COUNTIF."
**Explain simply:**
- Span of control = number of people who report directly to a manager.
- Direct reports only: this counts one level. Indirect (the whole tree) needs a loop or Power Query / recursion.
- People with 0 are not managers; exclude them when you average the span.
**Example:** Ravi (E2) manages Karan, Divya and Imran, so his span is 3. Asha manages Ravi and Meera, so 2.
**Sample sheet:**

| row | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 1 | Emp ID | Name | Manager ID | Direct reports |  | Managers with 3+ reports |
| 2 | E1 | Asha |  | 2 |  | 1 |
| 3 | E2 | Ravi | E1 | 3 |  | Average span (managers only) |
| 4 | E3 | Meera | E1 | 2 |  | 2.3333 |
| 5 | E4 | Karan | E2 | 0 |  |  |
| 6 | E5 | Divya | E2 | 0 |  |  |
| 7 | E6 | Imran | E2 | 0 |  |  |
| 8 | E7 | Neha | E3 | 0 |  |  |
| 9 | E8 | Pooja | E3 | 0 |  |  |

**Formula / Steps:** `D2 =COUNTIF($C$2:$C$9,A2)` filled down; managers with 3 or more: `F2 =COUNTIF(D2:D9,">=3")`; average span `F4 =AVERAGEIF(D2:D9,">0")`.
**Alternative:** Pivot table with Manager ID in Rows and Count of Emp ID in Values (not run here); or in 365 `=UNIQUE(C2:C9)` next to `COUNTIF` (not run here).
**Result:** Run: D2:D9 = 2, 3, 2, 0, 0, 0, 0, 0; managers with 3+ = 1; average span = 2.3333.
**Version note:** COUNTIF/AVERAGEIF: all versions. UNIQUE: Excel 2021, 2024 and 365 (Microsoft Support, "UNIQUE function").
**Edge cases:** Blank manager ID for the top person is fine. IDs with spaces or text-vs-number mismatch (E1 vs 'E1 ') give 0. Duplicate employee IDs double-count.
**Likely follow-ups:** 1) *Indirect reports?* Repeat the lookup level by level or use Power Query. 2) *Ideal span?* Company-specific; do not quote a magic number.
**Common mistakes:** Counting by manager name (names repeat); forgetting the $ anchors; including non-managers in the average.

### Q46 ⭐ 🟡 How would you build the same attrition report in Google Sheets, and what differs from Excel?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the spreadsheet tool is not the point, and which parts differ between Excel and Sheets?
**Say this in the interview:** "The logic is identical. COUNTIFS, SUMIFS, AVERAGE and IF work the same in Google Sheets. The differences are in sharing, a few newer functions, array handling and what replaces pivots, Power Query and macros."
**Explain simply:**
- Same: attrition % = leavers / average headcount x 100, and the formulas COUNTIFS, SUMIFS, IF, VLOOKUP, INDEX/MATCH.
- Different: Sheets is browser-based with live co-editing and version history; Excel is a desktop file (co-authoring needs OneDrive/SharePoint).
- Google's Help Center has function pages for FILTER, UNIQUE and XLOOKUP (fetched), so these exist in Sheets. QUERY (a SQL-like function) is Sheets-only and ARRAYFORMULA applies a formula to a whole range (both from memory, unverified).
- Power Query and VBA have no direct Sheets equivalent; Sheets uses Apps Script (JavaScript) for automation (from memory, unverified).
- Large data: Sheets is slower on big files (from memory, unverified, check the current cell limit).
**Example:** Monthly attrition table built the same in both tools: Sales 4 leavers / average 49 = 8.2%.
**Sample sheet:**

| row | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Dept | Start HC | End HC | Leavers | Attrition % |
| 2 | Sales | 50 | 48 | 4 | 0.0816 |
| 3 | HR | 10 | 10 | 1 | 0.1 |
| 4 | IT | 40 | 44 | 3 | 0.0714 |
| 5 | Ops | 80 | 76 | 6 | 0.0769 |
| 6 | Total | 180 | 178 | 14 | 0.0782 |

**Formula / Steps:** `E2 =ROUND(D2/AVERAGE(B2:C2),4)` (same cell syntax in Excel and Sheets). Sheets-only shortcut for the whole column: `=ARRAYFORMULA(D2:D5/((B2:B5+C2:C5)/2))` (not run here). Leavers count from a raw list works the same: `=COUNTIFS(Data!C:C,">="&A2,Data!C:C,"<="&B2)`.
**Alternative:** In Excel use a PivotTable or Power Query; in Sheets use a pivot table (Insert > Pivot table) or `=QUERY(...)` (not run here).
**Result:** Run (LibreOffice): attrition % Sales = 0.0816, HR = 0.1, IT = 0.0714, Ops = 0.0769, total = 0.0782. Sheets results were not run here.
**Version note:** Sheets function availability is confirmed only as far as the Google Docs Editors Help pages titled "FILTER function" and "XLOOKUP function" that were fetched; everything else about Sheets above is from memory, unverified.
**Edge cases:** Date handling and locale can differ (date format, week start). Importing from Excel keeps formulas but may drop VBA and some newer Excel functions.
**Likely follow-ups:** 1) *Which would you choose for a recurring report?* Excel with Power Query for heavy work, Sheets for team sharing. 2) *Can Sheets use pivots?* Yes.
**Common mistakes:** Claiming a feature exists in Sheets without checking; copying an Excel macro into Sheets expecting it to run.

### Q47 ⭐ 🟡 What would you do differently in a monthly report if your company is on Excel 2016 instead of Microsoft 365?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you build reports that still work for the colleagues' older Excel, and do you know what you cannot rely on?
**Say this in the interview:** "I first ask which version the readers have. On Excel 2016 I avoid dynamic-array and newer functions and use INDEX/MATCH, SUMIFS, SUMPRODUCT and PivotTables, so the file opens everywhere without #NAME? errors."
**Explain simply:**
- Dynamic array functions (UNIQUE, FILTER, SORT) and XLOOKUP are not available in Excel 2016. UNIQUE's page lists Excel 365, 2024 and 2021 only; XLOOKUP's Microsoft page contradicts itself (applies-to lists 2016/2019 but its note says not available in 2016/2019), so I would test it rather than assume (Microsoft Support, "UNIQUE function", "XLOOKUP function").
- Microsoft's "Dynamic array formulas and spilled array behavior" page lists 2016 and 2019 in its applies-to, which looks like the same page-level inconsistency; spilling itself is a 365/2021 feature (from memory, unverified).
- Older-safe toolkit: INDEX/MATCH or VLOOKUP, SUMIFS/COUNTIFS/AVERAGEIFS, SUMPRODUCT, IFERROR, PivotTables, Remove Duplicates.
- Power Query is built into Excel 2016 as Get & Transform (Data tab); in 2010/2013 it was an add-in (from memory, unverified, Microsoft page not fetched).
- IFS, MAXIFS, TEXTJOIN, SWITCH arrived in 2019 / 365 (from memory, unverified).
**Example:** A manager on Excel 2016 opens your file with XLOOKUP and sees #NAME?. Use INDEX/MATCH and the report works for both.
**Sample sheet:**

| row | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 1 | Emp | Dept | Salary |  | Look up Emp | E04 |
| 2 | E01 | Sales | 40000 |  | Salary found | 60000 |
| 3 | E02 | HR | 35000 |  | Distinct depts | 3 |
| 4 | E03 | Sales | 45000 |  | Sales payroll | 85000 |
| 5 | E04 | IT | 60000 |  | Max IT salary (no MAXIFS) | 72000 |
| 6 | E05 | IT | 72000 |  |  |  |
| 7 | E06 | HR | 38000 |  |  |  |

**Formula / Steps:** Lookup `F2 =INDEX($C$2:$C$7,MATCH(F1,$A$2:$A$7,0))`; distinct count (instead of UNIQUE) `F3 =SUMPRODUCT(1/COUNTIF(B2:B7,B2:B7))`; conditional total `F4 =SUMIFS(C2:C7,B2:B7,"Sales")`; conditional max without MAXIFS `F5 =SUMPRODUCT(MAX((B2:B7="IT")*C2:C7))`.
**Alternative:** 365 equivalents (not run here, LibreOffice 24.2 lacks them): `=XLOOKUP(F1,A2:A7,C2:C7)`, `=ROWS(UNIQUE(B2:B7))`, `=MAXIFS(C2:C7,B2:B7,"IT")`. Expected: 60000, 3, 72000 (pandas).
**Result:** Run: salary of E04 = 60000; distinct depts = 3; Sales payroll = 85000; max IT salary = 72000.
**Version note:** See bullets above. All 'run' formulas work in every Excel version.
**Edge cases:** The SUMPRODUCT distinct trick returns #DIV/0! if the range has blanks; and it is slow on big ranges. Files saved from 365 with dynamic formulas show them frozen as {=...} or #NAME? in older versions.
**Likely follow-ups:** 1) *Can they open the 365 file?* Yes, but new functions show #NAME?. 2) *Safest approach?* Ask the reader's version, or send values/PDF.
**Common mistakes:** Assuming everyone has 365; using a newer function and discovering the error after sending.

### Q48 ⭐ 🟡 How do you calculate gender diversity ratio by department and level?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you slice a headcount by two attributes and report a share, not just a count?
**Say this in the interview:** "I count total and female employees for each department and level with COUNTIFS, then divide for the percentage. I always show the headcount next to the percentage because 50% of 2 people is not meaningful."
**Explain simply:**
- Diversity ratio here = share of women (or men:women ratio) in a group.
- Cut by level matters: a healthy 50% overall can hide 0% in senior roles.
- Show counts with percentages to avoid small-number noise.
**Example:** HR has 4 people (3 women) = 75% women. Sales Senior has 2 people and 0 women = 0%.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H | I | J | K |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Emp | Dept | Level | Gender |  | Dept | Level | Total | Women | Women % | Men:Women |
| 2 | E01 | Sales | Junior | F |  | Sales | Junior | 2 | 1 | 0.5 | 1:1 |
| 3 | E02 | Sales | Junior | M |  | Sales | Senior | 2 | 0 | 0 | n/a |
| 4 | E03 | Sales | Senior | M |  | HR | Junior | 2 | 2 | 1 | 0:2 |
| 5 | E04 | Sales | Senior | M |  | HR | Senior | 2 | 1 | 0.5 | 1:1 |
| 6 | E05 | HR | Junior | F |  |  |  |  |  |  |  |
| 7 | E06 | HR | Junior | F |  |  |  |  |  |  |  |
| 8 | E07 | HR | Senior | F |  |  |  |  |  |  |  |
| 9 | E08 | HR | Senior | M |  |  |  |  |  |  |  |

**Formula / Steps:** `H2 =COUNTIFS($B$2:$B$9,F2,$C$2:$C$9,G2)`, `I2 =COUNTIFS($B$2:$B$9,F2,$C$2:$C$9,G2,$D$2:$D$9,"F")`, `J2 =IF(H2=0,"",ROUND(I2/H2,3))`.
**Alternative:** PivotTable: Dept and Level in Rows, Gender in Columns, Values = Count of Emp, 'Show Values As > % of Row Total' (not run here).
**Result:** Run (rows 2 to 5): women % = Sales Junior 0.5 (of 2), Sales Senior 0 (of 2), HR Junior 1 (of 2), HR Senior 0.5 (of 2).
**Version note:** COUNTIFS: Excel 2007+; PivotTable: all versions (from memory, unverified).
**Edge cases:** Non-binary or blank gender values need a separate row or an 'Undisclosed' bucket, else percentages will not sum to 100. Groups of size 0 give #DIV/0!. For small groups, reporting rules may require suppression (privacy).
**Likely follow-ups:** 1) *Why not one overall %?* It hides level gaps. 2) *Pay equity?* Needs salary by gender within same grade (compa-ratio).
**Common mistakes:** Dividing by total company headcount instead of the group; spelling variants (F, Female, female) not standardised.

### Q49 ⭐ 🟡 How do you reconcile headcount between the HRMS, payroll and the attendance system?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you treat HRMS as the master and reconcile the others to it, with reasons not just counts?
**Say this in the interview:** "Counts alone hide offsetting errors, so I compare employee by employee. HRMS (the HR master system) is the reference. I check each ID against payroll and attendance, and again in reverse, then explain each difference: joiner or leaver timing, contractors, long leave, duplicate IDs."
**Explain simply:**
- Reconcile = compare two or more sources and explain every difference.
- Do it both ways: HRMS-to-payroll and payroll-to-HRMS, because each direction finds different gaps.
- Agree a cut-off date (all systems as of the same day) before comparing.
- Typical reasons: exit processed late in payroll, new joiner not yet in attendance, contractor in payroll only, ID typed differently.
**Example:** HRMS says 6 employees, payroll 6, attendance 5. Same-looking counts for HRMS and payroll, but E6 is missing in payroll and E9 is in payroll but not in HRMS: two differences hidden by equal counts.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HRMS | Payroll | Attendance | HRMS in payroll? | HRMS in attendance? | Payroll not in HRMS |  | Counts |  |  |
| 2 | E1 | E1 | E1 | Yes | Yes |  |  | 6 | 6 | 5 |
| 3 | E2 | E2 | E2 | Yes | Yes |  |  | 1 |  |  |
| 4 | E3 | E3 | E4 | Yes | MISSING |  |  | 1 |  |  |
| 5 | E4 | E4 | E5 | Yes | Yes |  |  | 1 |  |  |
| 6 | E5 | E5 | E6 | Yes | Yes |  |  |  |  |  |
| 7 | E6 | E9 |  | MISSING | Yes | Not in HRMS |  |  |  |  |

(H2:J2 = row counts of HRMS, payroll, attendance; H3 = HRMS IDs missing in payroll; H4 = missing in attendance; H5 = payroll IDs not in HRMS.)

**Formula / Steps:** `D2 =IF(COUNTIF($B$2:$B$7,A2)>0,"Yes","MISSING")`, `E2` same against column C, and reverse `F2 =IF(COUNTIF($A$2:$A$7,B2)=0,"Not in HRMS","")`; counts `H3 =COUNTIF(D2:D7,"MISSING")`.
**Alternative:** Power Query: merge the three tables on Employee ID with Full Outer join, filter nulls (not run here); or `=ISNA(MATCH(A2,B:B,0))`.
**Result:** Run: HRMS 6, payroll 6, attendance 5; HRMS IDs missing in payroll = 1; missing in attendance = 1; payroll IDs not in HRMS = 1.
**Version note:** COUNTIF/MATCH: all versions. Power Query merge: Excel 2016+ built in (from memory, unverified).
**Edge cases:** Duplicate IDs inflate one side (check with COUNTIF>1). IDs stored as text in one system and numbers in another never match. Employees on unpaid leave appear in HRMS but not payroll legitimately.
**Likely follow-ups:** 1) *Which is the master?* HRMS unless policy says otherwise. 2) *Counts match, are we done?* No, offsetting errors.
**Common mistakes:** Comparing totals only; skipping the reverse check; no common cut-off date.

### Q50 ⭐ 🟡 How do you build an interview scheduling and hiring status tracker that flags overdue follow-ups?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine dates and IF logic to make a sheet that nags for you?
**Say this in the interview:** "I keep a follow-up due date per candidate, and a flag column that says Overdue when the due date is before today and the status is not closed. Conditional formatting turns those rows red."
**Explain simply:**
- The flag compares the due date with 'today' (TODAY() updates daily; here I fixed H1 to 22-Oct-2026 so results can be reproduced).
- Ignore closed items, otherwise the list is always red.
- Treat a missing due date as its own problem ('No date set').
**Example:** On 22-Oct, Bhavna's follow-up was due 21-Oct and is still open: Overdue 1d. Chirag's is due 25-Oct: not overdue.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| 1 | Candidate | Stage | Interview date | Follow-up due | Status | Flag | As of | 2026-10-22 |
| 2 | Anil | Round 1 | 2026-10-14 | 2026-10-16 | Open | Overdue 6d |  | Overdue count |
| 3 | Bhavna | Round 2 | 2026-10-18 | 2026-10-21 | Open | Overdue 1d |  | 2 |
| 4 | Chirag | HR round | 2026-10-20 | 2026-10-25 | Open |  |  |  |
| 5 | Deepa | Offer | 2026-10-10 | 2026-10-15 | Closed |  |  |  |
| 6 | Esha | Round 1 | 2026-10-19 |  | Open | No date set |  |  |
| 7 | Farhan | Round 1 | 2026-10-22 | 2026-10-22 | Open |  |  |  |

**Formula / Steps:** `F2 =IF(E2="Closed","",IF(D2="","No date set",IF(D2<$H$1,"Overdue "&($H$1-D2)&"d","")))`; in real use `H1 =TODAY()`. Count: `H3 =COUNTIF(F2:F7,"Overdue*")`. Highlight: Home > Conditional Formatting > New Rule > Use a formula `=LEFT($F2,7)="Overdue"`.
**Alternative:** Filter on the flag column, or Power Automate reminders (not run here).
**Result:** Run: flags = Anil: 'Overdue 6d'; Bhavna: 'Overdue 1d'; Chirag: ''; Deepa: ''; Esha: 'No date set'; Farhan: ''; overdue count = 2.
**Version note:** IF/COUNTIF/conditional formatting: all versions; Sheets the same (from memory, unverified).
**Edge cases:** Dates typed as text compare wrongly (check with ISNUMBER). TODAY() recalculates when opened, so a printed report changes; freeze the date for a month-end snapshot. Weekends: use WORKDAY if follow-ups skip weekends.
**Likely follow-ups:** 1) *Skip weekends?* =WORKDAY(C2,2). 2) *Email alerts?* Needs Power Automate or VBA, not plain Excel.
**Common mistakes:** Forgetting closed statuses; comparing text dates; using TODAY() in a historical report.

### Q51 ⭐ 🟡 How do you identify which department or tenure band has the highest attrition risk using a simple weighted score?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you turn several metrics into one defensible ranking, and say its limits?
**Say this in the interview:** "I put each metric on a 0 to 1 scale so they are comparable, multiply by weights agreed with HR leadership, add them, and rank. It is a screening tool to decide where to look first, not a prediction."
**Explain simply:**
- Min-max scaling: (value - lowest) / (highest - lowest) converts any metric to 0 (best) to 1 (worst) so percentages and months can be added fairly.
- Weights express importance (here attrition 50%, first-year share 30%, short tenure 20%) and must sum to 100%. They are a judgement call; show a sensitivity check.
- Flip the direction for metrics where lower is worse (shorter tenure = more risk), using 1 minus the scaled value.
**Example:** Ops has the highest attrition (28%), most first-year leavers (60%) and the shortest tenure (14 months), so it scores 1.0 and ranks first.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Dept | Attrition % | First-year share of leavers | Avg tenure (months) | Norm attr | Norm first-yr | Norm tenure (inverted) | Risk score | Rank |  | Weight |  |
| 2 | Sales | 0.22 | 0.5 | 18 | 0.6667 | 0.75 | 0.8462 | 0.728 | 2 |  | Attrition | 0.5 |
| 3 | HR | 0.1 | 0.2 | 40 | 0 | 0 | 0 | 0 | 4 |  | First-year | 0.3 |
| 4 | IT | 0.18 | 0.4 | 30 | 0.4444 | 0.5 | 0.3846 | 0.449 | 3 |  | Short tenure | 0.2 |
| 5 | Ops | 0.28 | 0.6 | 14 | 1 | 1 | 1 | 1 | 1 |  |  |  |

**Formula / Steps:** `E2 =(B2-MIN(B$2:B$5))/(MAX(B$2:B$5)-MIN(B$2:B$5))` (F likewise on C), `G2 =1-(D2-MIN(D$2:D$5))/(MAX(D$2:D$5)-MIN(D$2:D$5))`, `H2 =ROUND($L$2*E2+$L$3*F2+$L$4*G2,3)`, `I2 =RANK.EQ(H2,$H$2:$H$5)`. Weights sit in L2:L4 so they can be changed.
**Alternative:** Use `SUMPRODUCT` over a row of normalised values and a row of weights, or z-scores `STANDARDIZE` instead of min-max; or a statistical model in Python (not run here).
**Result:** Run: risk scores Sales 0.728 (rank 2), HR 0 (rank 4), IT 0.449 (rank 3), Ops 1 (rank 1).
**Version note:** RANK.EQ exists from Excel 2010 (from memory, unverified); RANK works everywhere.
**Edge cases:** If MAX = MIN the scale divides by zero. Tiny departments give noisy rates; show headcount. One extreme value squeezes everyone else (min-max is outlier-sensitive). Never present the score as a prediction of who will leave.
**Likely follow-ups:** 1) *How choose weights?* Agree with HR, test other sets, see if the top group changes. 2) *Better method?* Logistic regression on employee-level data.
**Common mistakes:** Adding raw numbers with different units; forgetting to invert 'lower is riskier' metrics; weights not summing to 1.

### Q52 ⭐ 🟡 How do you create a monthly revenue-per-employee or cost-per-hire metric in Excel?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you pick the right denominator and avoid dividing by zero?
**Say this in the interview:** "Revenue per employee is revenue divided by average headcount for the month. Cost per hire is total recruitment cost divided by the number of hires. I use the average headcount, not just the closing figure, because people join and leave during the month. For totals, I divide the totals, not average the monthly ratios."
**Explain simply:**
- Average headcount = (opening + closing) / 2, the same denominator as attrition.
- Cost per hire = total hiring cost (agency fees, ads, referral bonus, interviewer time if the company counts it) / number of hires. What counts as cost differs by company, so state the definition.
- Months with zero hires would give #DIV/0!; show n/a.
**Example:** July: 9,000,000 revenue / average of 100 and 104 = 102 people = 88,235 per employee. Recruitment cost 240,000 / 4 hires = 60,000 per hire.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Month | Revenue | Opening HC | Closing HC | Avg HC | Revenue per employee | Hires | Recruitment cost | Cost per hire |
| 2 | Jul | 9000000 | 100 | 104 | 102 | 88235 | 4 | 240000 | 60000 |
| 3 | Aug | 9500000 | 104 | 106 | 105 | 90476 | 3 | 150000 | 50000 |
| 4 | Sep | 9200000 | 106 | 105 | 105.5 | 87204 | 0 | 0 | n/a |
| 5 | Oct | 10100000 | 105 | 110 | 107.5 | 93953 | 6 | 420000 | 70000 |
| 6 | Total | 37800000 |  |  |  |  | 13 | 810000 | 62308 |

**Formula / Steps:** `E2 =AVERAGE(C2:D2)`, `F2 =ROUND(B2/E2,0)`, `I2 =IF(G2=0,"n/a",ROUND(H2/G2,0))`; total `I6 =ROUND(H6/G6,0)`.
**Alternative:** PivotTable from a monthly table with a calculated field Revenue / Headcount (not run here); or Power BI measure with DIVIDE().
**Result:** Run: revenue per employee Jul-Oct = 88235, 90476, 87204, 93953; cost per hire Jul-Oct = 60000, 50000, n/a, 70000; overall cost per hire = 62308.
**Version note:** All versions. DIVIDE() is a Power BI/DAX function, not Excel.
**Edge cases:** Zero hires: handled by IF. Annual ratio: sum revenue / average of monthly average headcounts. Contractors: decide whether in or out of headcount and say so.
**Likely follow-ups:** 1) *Why not closing headcount?* Understates in growth. 2) *Cost per hire target?* Company-specific, no universal figure.
**Common mistakes:** Averaging the monthly ratios; unclear cost definition; forgetting zero-hire months.

### Q53 ⭐ 🟡 How do you calculate loss-of-pay (unpaid leave) deductions from an attendance sheet and monthly salary?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you turn an attendance record into money, and do you know the rule depends on company policy?
**Say this in the interview:** "Loss of pay is salary divided by the days in the month, times the unpaid days. I count LOP days from the attendance sheet with COUNTIF, count half-days as 0.5, and confirm with payroll whether the divisor is calendar days, 30 or working days."
**Explain simply:**
- Loss of pay (LOP) = days of unpaid absence for which salary is cut.
- Per-day rate = monthly salary / divisor. Divisor is a policy choice: actual calendar days, a fixed 30, or working days. Ask before assuming.
- Half-day LOP = 0.5 day.
- Only the first 8 days of the month are shown in the sample to keep it small.
**Example:** Salary 60,000, September has 30 days, so one day = 2,000. With 2.5 LOP days: deduction = 5,000, net 55,000.
**Sample sheet:**

| row | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Date | Status |  | Item | Value |
| 2 | 2026-09-01 | Present |  | Monthly salary | 60000 |
| 3 | 2026-09-02 | Present |  | Month start | 2026-09-01 |
| 4 | 2026-09-03 | LOP |  | Days in month | 30 |
| 5 | 2026-09-04 | Present |  | LOP days | 2.5 |
| 6 | 2026-09-05 | Half LOP |  | Deduction | 5000 |
| 7 | 2026-09-06 | Present |  | Net salary | 55000 |
| 8 | 2026-09-07 | Weekly off |  | Deduction (26 working days basis) | 5769 |
| 9 | 2026-09-08 | LOP |  |  |  |

**Formula / Steps:** `E4 =DAY(EOMONTH(E3,0))`, `E5 =COUNTIF(B2:B9,"LOP")+0.5*COUNTIF(B2:B9,"Half LOP")`, `E6 =ROUND(E2/E4*E5,0)`, `E7 =E2-E6`.
**Alternative:** Fixed divisor `=ROUND(E2/30*E5,0)`, or a working-days basis `E2/26*E5` (cell E8 shows the 26-day version); or SUMPRODUCT over a LOP-weight lookup table.
**Result:** Run: days in month = 30, LOP days = 2.5, deduction = 5000, net = 55000; 26-day basis deduction = 5769.
**Version note:** EOMONTH, COUNTIF: all versions (from memory, unverified).
**Edge cases:** Month with 28 vs 31 days changes the daily rate. Weekly offs and holidays inside a LOP stretch may also be counted as LOP by policy (sandwich rule). Salary components: LOP may apply to basic only or gross; check. Statutory deductions then change. This is not legal advice.
**Likely follow-ups:** 1) *Sandwich rule?* Company policy, ask HR. 2) *Mid-month joiner?* Pro-rate by days worked / days in month.
**Common mistakes:** Assuming 30 days; counting weekly offs as present or LOP without checking policy; rounding too early.

### Q54 ⭐ 🔴 How do you calculate a cohort-wise retention table (joiners of each month and how many remain after 3, 6 and 12 months)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build a cohort table, with care about who has had enough time to be measured?
**Say this in the interview:** "A cohort is everyone who joined in the same month. For each person I flag whether they were still employed 3 and 6 months after joining, but only if that much time has passed. Then I group by joining month and divide."
**Explain simply:**
- Cohort = a group of people who share a starting month; retention % = how many of them are still here after N months.
- Helper columns keep it simple: cohort month, then a 1/0 flag per milestone.
- A person who joined 2 months ago cannot be judged at 6 months yet, so the flag stays blank and the person is left out of the denominator.
- Retained at 3 months means exit date blank, or exit on or after join date + 3 months (EDATE adds whole months).
**Example:** Jan 2026 joiners: 3. After 3 months one had left (E1, Feb), so 2 of 3 = 66.7% kept. After 6 months E3 (left May) is gone too, so 1 of 3 = 33.3%.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| 1 | Emp | Join date | Exit date | Cohort month | Kept 3m? | Kept 6m? | As of | 2026-10-22 |
| 2 | E1 | 2026-01-05 | 2026-02-20 | 2026-01-01 | 0 | 0 |  |  |
| 3 | E2 | 2026-01-12 |  | 2026-01-01 | 1 | 1 |  |  |
| 4 | E3 | 2026-01-20 | 2026-05-02 | 2026-01-01 | 1 | 0 |  |  |
| 5 | E4 | 2026-02-03 |  | 2026-02-01 | 1 | 1 |  |  |
| 6 | E5 | 2026-02-17 | 2026-03-10 | 2026-02-01 | 0 | 0 |  |  |
| 7 | E6 | 2026-02-25 | 2026-09-01 | 2026-02-01 | 1 | 1 |  |  |
| 8 | E7 | 2026-05-10 |  | 2026-05-01 | 1 |  |  |  |
| 9 | E8 | 2026-06-15 | 2026-07-01 | 2026-06-01 | 0 |  |  |  |

| row | J | K | L | M | N | O | P |
|---|---|---|---|---|---|---|---|
| 1 | Cohort | Joiners | Kept 3m | 3m % | Kept 6m | 6m eligible | 6m % |
| 2 | 2026-01-01 | 3 | 2 | 0.667 | 1 | 3 | 0.333 |
| 3 | 2026-02-01 | 3 | 2 | 0.667 | 2 | 3 | 0.667 |
| 4 | 2026-05-01 | 1 | 1 | 1 | 0 | 0 | not yet |
| 5 | 2026-06-01 | 1 | 0 | 0 | 0 | 0 | not yet |

**Formula / Steps:** `D2 =DATE(YEAR(B2),MONTH(B2),1)`, `E2 =IF(EDATE(B2,3)>$H$1,"",IF(OR(C2="",C2>=EDATE(B2,3)),1,0))` (F2 with 6), cohort table: `K2 =COUNTIF($D$2:$D$9,J2)`, `L2 =SUMIFS($E$2:$E$9,$D$2:$D$9,J2)`, `M2 =ROUND(L2/SUMPRODUCT(($D$2:$D$9=J2)*ISNUMBER($E$2:$E$9)),3)`. For 12 months repeat with 12.
**Alternative:** PivotTable with Cohort month in Rows, Flag in Columns and Average of flag as value (not run here); or Power Query with months-since-join (not run here).
**Result:** Run: 3-month retention Jan = 0.667, Feb = 0.667, May = 1, Jun = 0; 6-month Jan = 0.333, Feb = 0.667, May = not yet, Jun = not yet.
**Version note:** EDATE, SUMIFS, SUMPRODUCT: all versions (from memory, unverified). The as-of date H1 is fixed for reproducibility; use TODAY() or the report date in practice.
**Edge cases:** Rehires (same ID, two join dates) need a rule. Exit date before join date = data error. Small cohorts give jumpy percentages; show the counts. EDATE of 31 Aug +6 months gives 28 Feb: day-of-month clamping.
**Likely follow-ups:** 1) *Show as a triangle?* Cohorts in rows, months-since-join in columns, conditional-format colours. 2) *Why exclude young cohorts?* Else retention looks falsely high.
**Common mistakes:** Including people who have not reached the milestone; using YEAR/MONTH difference instead of EDATE; ignoring rehires.

### Q55 ⭐ 🔴 How do you build a variance report between budget and actual headcount cost with drill-down to the cause?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you explain why a number moved, not just by how much?
**Say this in the interview:** "I split the cost variance into a volume part (we have more or fewer people than planned) and a rate part (each person costs more or less than planned). The two add up to the total, and I link each to the detail rows so a manager can drill down."
**Explain simply:**
- Variance = actual - budget; over budget is positive here.
- Volume variance = (actual headcount - budget headcount) x budget cost per head.
- Rate variance = actual headcount x (actual cost per head - budget cost per head).
- The two parts always add to the total, which gives a built-in check.
- Drill-down: a pivot or SUMIFS over the employee-level payroll data shows which people or components (overtime, hiring bonus) drive the rate part.
**Example:** Sales planned 20 people at 50,000 = 1,000,000; actual 22 at 52,000 = 1,144,000. Over by 144,000: 100,000 because of 2 extra people, 44,000 because each costs 2,000 more.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H | I | J | K |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Dept | Budget HC | Actual HC | Budget cost/head | Actual cost/head | Budget cost | Actual cost | Total variance | Volume variance | Rate variance | Check |
| 2 | Sales | 20 | 22 | 50000 | 52000 | 1000000 | 1144000 | 144000 | 100000 | 44000 | OK |
| 3 | HR | 8 | 8 | 45000 | 48000 | 360000 | 384000 | 24000 | 0 | 24000 | OK |
| 4 | IT | 15 | 14 | 70000 | 69000 | 1050000 | 966000 | -84000 | -70000 | -14000 | OK |
| 5 | Total | 43 | 44 |  |  | 2410000 | 2494000 | 84000 | 30000 | 54000 | OK |

**Formula / Steps:** `F2 =B2*D2`, `G2 =C2*E2`, `H2 =G2-F2`, `I2 =(C2-B2)*D2`, `J2 =C2*(E2-D2)`, `K2 =IF(H2=I2+J2,"OK","CHECK")`. Drill down to detail: `=SUMIFS(Payroll!$F:$F,Payroll!$B:$B,A2,Payroll!$C:$C,"Overtime")`.
**Alternative:** PivotTable with Dept and Cost Component in Rows and Double-click on a value to see its underlying rows (not run here); or Data > Group outline levels.
**Result:** Run: total variance Sales = 144000, HR = 24000, IT = -84000; company = 84000 split into volume 30000 and rate 54000; checks: OK, OK, OK, OK.
**Version note:** All versions for the formulas; PivotTable double-click drill-down: all versions (from memory, unverified).
**Edge cases:** Order of the split matters: using actual headcount for the rate effect and budget rate for the volume effect (as here) leaves no leftover; other conventions put a 'mix' term in the remainder. Timing (mid-month joiners) and one-off items distort rates. Floating-point decimals can break exact `=` checks; round both sides.
**Likely follow-ups:** 1) *Favourable vs adverse?* Sign convention: state it. 2) *Mix variance?* Needed if roles with different costs shift.
**Common mistakes:** Showing only the total; no check column; mixing monthly budget with annual actuals.

### Q56 ⭐ 🔴 How do you clean and standardise a messy attendance export where timestamps are text and some are blank?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you repair data instead of giving up when it arrives dirty?
**Say this in the interview:** "I never calculate on raw text. I trim spaces, standardise separators, convert to real time values with TIMEVALUE, leave blanks as blanks, and flag missing punches so someone fixes them instead of the report guessing."
**Explain simply:**
- Text time looks like 09:15 but Excel cannot subtract it until it is a real time value (a fraction of a day).
- TRIM removes extra spaces; SUBSTITUTE replaces '.' with ':' when the export uses 09.30.
- Blank in or out = missing punch; show a flag, not a made-up number.
- Hours = (out - in) x 24, because Excel stores one day as 1.
**Example:** E2's in-time is ' 9:20 ' with spaces and E3's is '09.30' with a dot. Cleaning turns them into 09:20 and 09:30, giving 8.5 and 8.67 hours. E4 has no out punch: flagged, not guessed.
**Sample sheet:**

| row | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 1 | Emp | In (text) | Out (text) | In time | Out time | Hours |
| 2 | E1 | 09:15 | 18:05 | 09:15 | 18:05 | 8.83 |
| 3 | E2 |  9:20  | 17:50 | 09:20 | 17:50 | 8.5 |
| 4 | E3 | 09.30 | 18:10 | 09:30 | 18:10 | 8.67 |
| 5 | E4 | 09:05 |  | 09:05 |  | Missing punch |
| 6 | E5 |  |  |  |  | Missing punch |
| 7 | E6 | 10:00 | 19:00  | 10:00 | 19:00 | 9 |

(Columns D:E are real time values; they are shown formatted as hh:mm.)

**Formula / Steps:** `D2 =IF(TRIM(B2)="","",TIMEVALUE(SUBSTITUTE(TRIM(B2),".",":")))`, `E2` the same on C2, `F2 =IF(OR(D2="",E2=""),"Missing punch",ROUND((E2-D2)*24,2))`. Format D:E as Time (Home > Number Format).
**Alternative:** Power Query: Data > Get Data > From Table/Range, change type to Time with Locale, Replace Values, Trim (not run here). Or Text to Columns for a quick convert.
**Result:** Run: hours = E1: 8.83, E2: 8.5, E3: 8.67, E4: Missing punch, E5: Missing punch, E6: 9.
**Version note:** TIMEVALUE/TRIM/SUBSTITUTE: all versions; Power Query: Excel 2016+ built in (from memory, unverified). TIMEVALUE parsing of unusual strings (AM/PM, locale) can differ between Excel and LibreOffice; test on your own export.
**Edge cases:** Night shifts crossing midnight give negative hours: use `MOD(E2-D2,1)*24`. Text '09:15:00 AM' needs a locale-aware conversion. Time stored as text with a leading apostrophe. Seconds are dropped by ROUND.
**Likely follow-ups:** 1) *Date and time in one text?* Use DATEVALUE and TIMEVALUE or Power Query. 2) *Many blank punches?* Count with COUNTIF(F:F,"Missing punch") and send HR a list.
**Common mistakes:** Subtracting text; replacing blanks by zero, which creates 0 or negative hours; forgetting x24.

### Q57 ⭐ 🔴 How do you prepare an exit-interview analysis in Excel where reasons are free text?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you turn messy comments into numbers you can chart, and say how far to trust them?
**Say this in the interview:** "I build a small keyword table that maps words to reason categories, tag every comment with a formula, and count by category. Anything unmatched goes to 'Other', and I read a sample of those to improve the keyword list. I'm clear that it is a first pass, not a perfect classification."
**Explain simply:**
- Free text = comments people type in their own words, so no two look alike.
- SEARCH finds a word inside text (not case sensitive); ISNUMBER turns 'found' into TRUE.
- LOOKUP(2,1/ISNUMBER(...)) returns the category of the last keyword that matched. Put the most important keyword last, or order the list deliberately.
- Count by category with COUNTIF and chart the result.
**Example:** Of 8 exit comments: 'Better pay elsewhere' and 'Salary too low' go to Pay; 'My Manager never listens' and 'Boss micromanages' to Manager; 'Moving abroad' matches no keyword and goes to Other.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| 1 | Exit reason (free text) | Category |  | Keyword | Category |  | Category | Count |
| 2 | Better pay elsewhere | Pay |  | salary | Pay |  | Pay | 2 |
| 3 | My Manager never listens | Manager |  | pay | Pay |  | Manager | 2 |
| 4 | No growth here | Career |  | manager | Manager |  | Career | 2 |
| 5 | Long commute every day | Commute |  | boss | Manager |  | Commute | 1 |
| 6 | Moving abroad | Other |  | growth | Career |  | Other | 1 |
| 7 | Salary too low | Pay |  | promotion | Career |  | Total | 8 |
| 8 | Wanted a promotion | Career |  | commute | Commute |  |  |  |
| 9 | Boss micromanages | Manager |  |  |  |  |  |  |

**Formula / Steps:** `B2 =IFERROR(LOOKUP(2,1/ISNUMBER(SEARCH($D$2:$D$8,A2)),$E$2:$E$8),"Other")`, count `H2 =COUNTIF($B$2:$B$9,G2)`, check `H7 =SUM(H2:H6)` equals number of comments.
**Alternative:** Pivot table on the Category column (not run here); Power Query with a custom column; in 365, `XLOOKUP` with wildcards is not a direct fit, a `FILTER`/`TEXTJOIN` approach is possible but not run here. Large volumes: text analytics in Python (not run here).
**Result:** Run: Pay = 2, Manager = 2, Career = 2, Commute = 1, Other = 1; total = 8.
**Version note:** SEARCH, LOOKUP, COUNTIF: all versions. The LOOKUP(2,1/...) trick works without Ctrl+Shift+Enter in Excel; verified here in LibreOffice only (from memory for Excel behaviour).
**Edge cases:** A comment mentioning two reasons gets only one category. Keywords can mislead ('pay' also matches 'payroll', 'repay'; 'manager' matches 'managerial'). Spelling mistakes are missed. Exit-interview data is small and subjective: treat as directional and protect confidentiality.
**Likely follow-ups:** 1) *Multiple reasons per person?* Add one flag column per category. 2) *Better method?* Manual coding of a sample, or text classification in Python.
**Common mistakes:** Treating keyword tags as facts; ignoring 'Other'; revealing individual comments in small teams.

### Q58 ⭐ 🔴 How do you audit someone else's MIS workbook to find hidden formula errors?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you have a method for finding errors that do not show as #REF! or #N/A?
**Say this in the interview:** "The worst errors look fine. I check for typed numbers hiding among formulas, ranges that miss the last row, inconsistent formulas down a column, and I recompute the total independently. Every finding is logged, not silently fixed."
**Explain simply:**
- Show formulas: Formulas tab > Show Formulas (Ctrl+`), to see logic instead of values.
- Home > Find & Select > Go To Special > Constants or Formulas (or Errors) finds hardcoded numbers inside a formula column.
- ISFORMULA tells whether a cell holds a formula and FORMULATEXT shows it, so you can audit a column with formulas.
- Formulas tab > Trace Precedents/Dependents and Error Checking show where numbers come from.
- Independent re-calculation: total the data a different way (SUMPRODUCT vs SUM of column) and compare; a difference exposes hidden problems.
**Example:** Revenue D2:D6 should be Units x Price. D4 (Sep) was overtyped as 4000 (correct would be 4,500), and the total SUM(D2:D5) stops at Oct, missing Nov.
**Sample sheet:**

| row | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 1 | Month | Units | Price | Revenue | Formula? | Formula text |
| 2 | Jul | 100 | 50 | 5000 | True | =B2*C2 |
| 3 | Aug | 120 | 50 | 6000 | True | =B3*C3 |
| 4 | Sep | 90 | 50 | 4000 | False | #N/A |
| 5 | Oct | 110 | 55 | 6050 | True | =B5*C5 |
| 6 | Nov | 130 | 55 | 7150 | True | =B6*C6 |
| 7 |  |  |  |  |  |  |
| 8 | Total |  |  | 21050 |  |  |
| 9 | Independent total |  |  | 28700 |  |  |
| 10 | Difference |  |  | 7650 |  |  |

(F4 shows #N/A because D4 is not a formula: that itself is a tell.)

**Formula / Steps:** `E2 =ISFORMULA(D2)` and `F2 =FORMULATEXT(D2)` filled down; independent total `D9 =SUMPRODUCT(B2:B6,C2:C6)`; difference `D10 =D9-D8`. Then Go To Special > Constants on D2:D6 highlights D4.
**Alternative:** Review > Inquire add-in (Spreadsheet Compare, Workbook Analysis) on supported editions; or Formulas > Evaluate Formula to step through a calculation (not run here).
**Result:** Run: D4 formula? False; others True; independent total 28700 vs sheet total 21050, difference 7650 (= Sep gap 500 plus Nov 7,150).
**Version note:** ISFORMULA and FORMULATEXT: Excel 2013 and later (from memory, unverified). Inquire add-in: only some Office editions (from memory, unverified). Sheets also has ISFORMULA and FORMULATEXT (from memory, unverified).
**Edge cases:** Hidden rows/columns and sheets, links to external workbooks (Data > Edit Links), manual calculation mode (Formulas > Calculation Options), number stored as text, rounding differences, and merged cells inside ranges.
**Likely follow-ups:** 1) *First thing you check?* Calculation mode and external links. 2) *How record?* An audit log: cell, issue, fix, owner, date.
**Common mistakes:** Fixing without documenting; trusting totals that 'look right'; checking only error cells.

### Q59 ⭐ 🔴 If a stakeholder disputes the attrition number in your report, how do you trace and defend it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Are you calm, transparent and able to rebuild a number from its raw rows?
**Say this in the interview:** "I would not argue; I would rebuild it live. I show the list of people counted, the dates and the definition, the denominator used, and then agree on the definition. Most disputes are definition differences, not wrong arithmetic."
**Explain simply:**
- Trace: start from the reported number, list the exact employees behind it (filter or SUMPRODUCT flag), tie the count back to the source.
- Common causes of disagreement: exit date vs last working day, denominator (opening, closing or average headcount), contractors or interns included, rehires, date range edges.
- Defend with definitions written on the report, plus a reconciliation: 'my 4 leavers, your 5: the 5th is E1, who left on 28 Aug and was processed in September'.
- If you were wrong, say so quickly, fix and log the change.
**Example:** The report shows 4 September leavers (E2, E3, E4, E6). The stakeholder expected 5 because E1 was processed in September although the last working day was 28 August. Rebuilding the list from exit dates settles it: E1 belongs to August.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| 1 | Emp | Dept | Exit date | In Sep? |  |  | Item | Value |
| 2 | E1 | Sales | 2026-08-28 | 0 |  |  | Month start | 2026-09-01 |
| 3 | E2 | Sales | 2026-09-05 | 1 |  |  | Month end | 2026-09-30 |
| 4 | E3 | IT | 2026-09-12 | 1 |  |  | Leavers in month | 4 |
| 5 | E4 | HR | 2026-09-30 | 1 |  |  | Cross-check COUNTIFS | 4 |
| 6 | E5 | IT | 2026-10-01 | 0 |  |  | Opening HC | 120 |
| 7 | E6 | Ops | 2026-09-18 | 1 |  |  | Closing HC | 110 |
| 8 |  |  |  |  |  |  | Average HC | 115 |
| 9 |  |  |  |  |  |  | Attrition % (avg HC) | 0.0348 |
| 10 |  |  |  |  |  |  | Attrition % (opening HC) | 0.0333 |

**Formula / Steps:** `D2 =IF(AND(C2>=$H$2,C2<=$H$3),1,0)`, `H4 =SUM(D2:D7)`, cross-check `H5 =COUNTIFS(C2:C7,">="&H2,C2:C7,"<="&H3)`, average headcount `H8 =AVERAGE(H6:H7)`, rate `H9 =ROUND(H4/H8,4)`.
**Alternative:** Filter the data on the exit-date column (Data > Filter > Date Filters > Between) and show the rows; or a pivot with exit month (not run here).
**Result:** Run: leavers = 4 (COUNTIFS confirms 4); attrition on average headcount 0.0348; on opening headcount 0.0333. The two bases differ by 0.15 percentage points, which alone can explain a dispute.
**Version note:** All functions: all versions.
**Edge cases:** Exit date stored as text; time part in date-time (a 30-Sep 23:00 exit fails `<=EOMONTH` if the cutoff has no time; use `<EOMONTH+1`); duplicates; rehires.
**Likely follow-ups:** 1) *Whose number is right?* Whoever matches the written definition; agree and fix the definition. 2) *Prevent repeat?* Put the definition and denominator on the report footnote.
**Common mistakes:** Defending the number without checking; changing numbers silently; mixing opening and average headcount between months.

### Q60 ⭐ 🔴 How do you build a six-month headcount forecast from the hiring plan and an expected attrition rate?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build a month-by-month roll-forward where each month feeds the next?
**Say this in the interview:** "It is a roll-forward: closing headcount equals opening plus hires minus leavers, and each month's opening equals the previous month's closing. Leavers come from an assumed monthly attrition rate. I keep the rate in one input cell so HR can try 15%, 18% or 22%."
**Explain simply:**
- Roll-forward = a table where this month's closing becomes next month's opening.
- Monthly attrition rate = annual rate / 12 (a simple approximation; compounding gives a slightly different number).
- Leavers = opening headcount x monthly rate, rounded to whole people.
- Keep assumptions (annual rate, hires) in clearly marked input cells and label the forecast as an estimate.
**Example:** Start Nov with 220 people, 18% annual attrition = 1.5% a month, so about 3 leavers in Nov (220 x 0.015 = 3.3 rounded to 3). With 6 hires, closing = 220 + 6 - 3 = 223.
**Sample sheet:**

| row | A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Month | Opening HC | Planned hires | Expected leavers | Closing HC |  | Annual attrition | 0.18 |  | Unrounded closing |
| 2 | Nov | 220 | 6 | 3 | 223 |  | Monthly rate | 0.015 |  | 222.7 |
| 3 | Dec | 223 | 4 | 3 | 224 |  |  |  |  | 223.3595 |
| 4 | Jan | 224 | 8 | 3 | 229 |  |  |  |  | 228.0091 |
| 5 | Feb | 229 | 5 | 3 | 231 |  |  |  |  | 229.589 |
| 6 | Mar | 231 | 5 | 3 | 233 |  |  |  |  | 231.1451 |
| 7 | Apr | 233 | 6 | 3 | 236 |  |  |  |  | 233.678 |
| 8 | Total |  | 34 | 18 | 236 |  |  |  |  |  |

**Formula / Steps:** `H2 =H1/12`, `B3 =E2` (fill down), `D2 =ROUND(B2*$H$2,0)`, `E2 =B2+C2-D2`. Totals `C8 =SUM(C2:C7)`, `D8 =SUM(D2:D7)`, `E8 =E7`. Column J keeps decimals as a check on rounding.
**Alternative:** Scenario Manager or a one-variable Data Table (Data > What-If Analysis) to show 15%/18%/22% side by side (not run here); or attrition by tenure band for a better estimate.
**Result:** Run: April closing = 236 people; planned hires 34, expected leavers 18; unrounded closing 233.68 (rounding changes it by 2.32).
**Version note:** All versions.
**Edge cases:** Rounding each month can drift: compare with the unrounded column. Hires start at different dates (use a join-date lag). Seasonal attrition (after appraisal) is not captured by a flat rate. Hiring plans often slip: consider a fill-rate assumption.
**Likely follow-ups:** 1) *Flat or variable rate?* Variable by month or tenure if data shows it. 2) *Sensitivity?* Show best/base/worst.
**Common mistakes:** Hardcoding the rate in formulas; applying annual rate each month; not labelling the forecast as an assumption-based estimate.

