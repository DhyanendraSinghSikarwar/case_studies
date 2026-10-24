# Book 1 — Excel | Part 9: What-if, Goal Seek, Conditional Formatting, Data Validation 🟡

**Target:** 40 questions | **Actual:** 46 questions
**Scope:** What-If Analysis (Goal Seek, Data Table, Scenario Manager), conditional formatting and data validation including drop-down lists, with HR-flavoured practical tasks.

### Q1 ⭐⭐⭐ 🟢 What is conditional formatting in Excel, and where would you use it as an analyst?
**Asked at:** commonly asked (no company-specific report found). One candidate-reported MIS-executive technical round (2025, snippet only) mentioned conditional formatting among SUMIFS, COUNTIFS and pivots; it is not named in any job-description sample in this repo's research.
**What the interviewer is checking:** Do you know it formats cells automatically by rule, and can you give a practical use?
**Say this in the interview:** "Conditional formatting changes how a cell looks, such as its fill colour, based on a rule about its value. I use it to make problems jump out: attendance below 90%, duplicate employee IDs, contracts about to expire."
**Explain simply:**
- A "rule" is a test, like "is this number below 90%?". If the test is TRUE for a cell, Excel applies the colour or icon. If FALSE, nothing changes.
- The cell's value is not changed, only its look. Change the number and the colour updates by itself.
- Microsoft says it makes "patterns and trends in your data more apparent" (Microsoft Support, "Use conditional formatting to highlight information in Excel").
- Built-in families: Highlight Cells Rules, Top/Bottom Rules, Data Bars, Color Scales, Icon Sets, plus your own formula rule (same page).
**Example:** An HR attendance sheet has 400 employees. A red fill for anyone below 90% lets the manager see the 23 at-risk people in seconds instead of scanning 400 rows.
**Sample sheet:**
| | A (Employee) | B (Attendance %) |
|---|---|---|
| 2 | Asha | 96% |
| 3 | Bala | 86% |
| 4 | Chitra | 90% |
| 5 | Dev | 72% |

**Formula / Steps:** Select B2:B5 > Home tab > Styles group > Conditional Formatting > Highlight Cells Rules > Less Than > 90% > choose a fill > OK (not run here; steps from Microsoft Support). The test itself, `=B2<0.9`, returns FALSE, TRUE, FALSE, TRUE for B2:B5 (run with LibreOffice 24.2 in Q5).
**Alternative:** A plain formula column (`=IF(B2<0.9,"Low","OK")`) gives a text flag you can filter; conditional formatting gives a visual flag.
**Result:** Bala (86%) and Dev (72%) are flagged; Chitra at exactly 90% is not.
**Version note:** Available in Excel 2016, 2019, 2021, 2024 and Microsoft 365; the web version has a narrower set of steps (Microsoft Support, same page).
**Edge cases:** Formatting is not data: filtering or counting by colour needs a helper column. Copy-paste can duplicate rules and slow big files.
**Likely follow-ups:** 1) *Can it use a formula?* Yes (Q7). 2) *Does it change the cell value?* No.
**Common mistakes:** Colouring by hand and expecting it to update; stacking too many overlapping rules.

### Q2 ⭐⭐⭐ 🟢 What is data validation in Excel, and why is it important for data accuracy?
**Asked at:** commonly asked (no company-specific report found). Data validation is named in about 6% (2 of 32) of the MIS/people job-description samples in this repo's research.
**What the interviewer is checking:** Do you see validation as prevention of bad data at entry, not clean-up afterwards?
**Say this in the interview:** "Data validation controls what a user is allowed to type into a cell, for example only a list of departments or only ages between 18 and 60. It stops bad data at the door, so reports and lookups don't break later."
**Explain simply:**
- It is a rule attached to a cell. Types include whole number, decimal, list, date, time, text length and custom formula (Microsoft Support, "Apply data validation to cells").
- It can show an input message (a hint) and an error alert (a refusal or warning).
- It protects later formulas: "Hyd" and "Hyderabad" typed differently will split a COUNTIF or pivot.
**Example:** A recruiter tracker where "Status" is free text ends up with "Selected", "selected ", "Slected". A drop-down with four allowed values gives clean counts.
**Formula / Steps:** Select cells > Data tab > Data Tools group > Data Validation > Settings tab > Allow: choose a type > set criteria > OK (not run here; steps from Microsoft Support). The "Data Validation command is unavailable if the sheet is protected or the workbook is shared" (same page).
**Alternative:** Protect the sheet and unlock only entry cells; or use a form (Microsoft Forms) for collection. Validation is only one layer.
**Version note:** Same page lists Excel 2016, 2019, 2021, 2024 and Microsoft 365 (also Excel for the web).
**Edge cases:** Validation does not check existing values, and pasting can overwrite it (Q40).
**Likely follow-ups:** 1) *How do you find existing bad data?* Circle Invalid Data (Q32). 2) *Can it be bypassed?* Yes, by pasting.
**Common mistakes:** Assuming it cleans old data; forgetting that users can paste over it.

### Q3 ⭐⭐⭐ 🟢 How do you create a drop-down list in a cell using Data Validation?
**Asked at:** commonly asked (no company-specific report found). Hirist's data-analyst list (2025-26) mentions drop-downs for dashboard data entry.
**What the interviewer is checking:** Can you do the click-path and point the list at a range?
**Say this in the interview:** "Select the cell, Data tab, Data Validation, Allow List, then either type the items separated by commas or point the Source at a range. Users then pick from an arrow instead of typing."
**Explain simply:**
- A drop-down only allows entries from the list (with Stop alert).
- Best practice: keep the items in a range (ideally an Excel table) and refer to it, leaving out the header (Microsoft Support, "Create a drop-down list").
- "In-cell dropdown" must stay ticked to see the arrow; "Ignore blank" lets users leave it empty.
**Example:** Department cells accept only Sales, HR, Finance, IT.
**Sample sheet:**
| | A (Typed entry) | H (Source list) |
|---|---|---|
| 2 | HR | Sales |
| 3 | hr | HR |
| 4 | Legal | Finance |
| 5 | IT (trailing space) | IT |
| 6 | (blank) | |

**Formula / Steps:** 1) Type the list in H2:H5. 2) Select the target cell(s). 3) Data > Data Tools > Data Validation > Settings > Allow: List. 4) Source: `=$H$2:$H$5` (or type `Sales,HR,Finance,IT`). 5) Keep In-cell dropdown ticked > OK. Not run here (steps from Microsoft Support).
**Alternative:** Type items directly into Source (comma-separated), fine for 3 to 4 fixed items.
**Result:** Entry check run in LibreOffice 24.2 with `=COUNTIF($H$2:$H$5,A2)>0` on rows 2-6 gives TRUE, TRUE, FALSE, FALSE, FALSE (HR and hr accepted since the match ignores case; Legal, "IT " with a space and blank fail). This simulates the list rule; it is not the dialog itself.
**Version note:** Works in Excel 2016 through Microsoft 365 (Microsoft Support, "Create a drop-down list"). Google Sheets has its own dropdown (Q38).
**Edge cases:** Typed entries are accepted case-insensitively; pasted values bypass the list.
**Likely follow-ups:** 1) *Source on another sheet?* Yes, see Q34 and the Cities example on the Microsoft page. 2) *Auto-grow?* Q22.
**Common mistakes:** Including the header in the source; typing a comma list with spaces.

### Q4 ⭐⭐⭐ 🟢 How do you highlight duplicate values in a column using conditional formatting?
**Asked at:** commonly asked (no company-specific report found); duplicates appear in TrumpExcel and Careers360 prep lists.
**What the interviewer is checking:** Do you know the built-in rule and the formula version?
**Say this in the interview:** "Select the column, Home, Conditional Formatting, Highlight Cells Rules, Duplicate Values. For more control I use a COUNTIF rule so I can colour only the second and later copies."
**Explain simply:**
- Built-in route needs no formula and colours every copy, including the first.
- Formula route: COUNTIF counts how many times a value appears. More than 1 means duplicate.
- An expanding range (`$A$2:A2`, anchored only at the top) counts only copies seen so far, so the first occurrence stays unformatted.
**Example:** Duplicate employee IDs in a joiners list: E102 and E101 each appear twice.
**Sample sheet:**
| | A (Emp ID) |
|---|---|
| 2 | E101 |
| 3 | E102 |
| 4 | E103 |
| 5 | E102 |
| 6 | E104 |
| 7 | E101 |
| 8 | E105 |

**Formula / Steps:** Built-in: select A2:A8 > Home > Conditional Formatting > Highlight Cells Rules > Duplicate Values > choose format (not run here; Microsoft Support). Formula rule: New Rule > Use a formula > `=COUNTIF($A$2:$A$8,A2)>1`. Second-and-later only: `=COUNTIF($A$2:A2,A2)>1`.
**Alternative:** Data > Remove Duplicates deletes them; helper column `=COUNTIF(...)` for filtering.
**Result:** Run in LibreOffice 24.2, rows 2-8. All copies rule: TRUE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE. Second-and-later rule: FALSE, FALSE, FALSE, TRUE, FALSE, TRUE, FALSE.
**Version note:** Duplicate Values rule exists in Excel 2016 to 365 (Microsoft Support, "Use conditional formatting to highlight information in Excel").
**Edge cases:** Matching is case-insensitive; extra spaces make "E101 " different; very long numeric IDs (16+ digits) can be mis-matched by COUNTIF (from memory, unverified).
**Likely follow-ups:** 1) *Highlight whole duplicate rows?* Use COUNTIFS across columns. 2) *Unique only?* Pick "Unique" in the same dialog.
**Common mistakes:** Locking the range wrongly (A2 instead of $A$2:$A$8) so the count slides.

### Q5 ⭐⭐⭐ 🟢 In an attendance sheet, how do you highlight every employee whose attendance percentage is below 90%?
**Asked at:** commonly asked (no company-specific report found); the "below a threshold" highlight is the canonical practical form of conditional formatting in the prep lists.
**What the interviewer is checking:** Can you set a threshold rule and handle blanks and text?
**Say this in the interview:** "Select the percentage column, Conditional Formatting, Highlight Cells Rules, Less Than, 90%. If blanks or text exist, I use a formula rule with ISNUMBER so those are not coloured by mistake."
**Explain simply:**
- Attendance % = days present divided by working days.
- 90% is stored as 0.9, so type 90% in the dialog.
- A blank cell counts as zero for a "less than" test, so it would be coloured red. That can hide a data problem or create a false alarm.
**Example:** Out of 7 employees below, 4 fall under 90%.
**Sample sheet:**
| | A (Name) | B (Present) | C (Working days) | D (Attendance %) |
|---|---|---|---|---|
| 2 | Asha | 27 | 28 | `=IFERROR(B2/C2,"")` |
| 3 | Bala | 24 | 28 | |
| 4 | Chitra | 27 | 30 | |
| 5 | Dev | 18 | 25 | |
| 6 | Esha | (blank) | 30 | |
| 7 | Farid | n/a | 30 | |
| 8 | Gita | 26 | 30 | |

**Formula / Steps:** Select D2:D8 > Home > Conditional Formatting > Highlight Cells Rules > Less Than > 90% (not run here; Microsoft Support). Safer formula rule: New Rule > Use a formula > `=AND(ISNUMBER(D2),D2<0.9)`.
**Alternative:** Plain `=D2<0.9` as the rule, or a helper column `=IF(D2<0.9,"Low","OK")`.
**Result:** Run in LibreOffice 24.2. D2:D8 = 0.964, 0.857, 0.9, 0.72, 0, "" (text error caught), 0.867. The ISNUMBER rule flags: FALSE, TRUE, FALSE, TRUE, TRUE, FALSE, TRUE. Chitra at exactly 0.9 is not flagged. Esha (blank present days) shows 0 and is flagged, which is a data gap to chase; Farid's text gives "" and stays unflagged.
**Version note:** Works in all versions Excel 2016 to 365 (Microsoft Support).
**Edge cases:** Floating-point: a percentage computed like 0.9 from 27/30 equals 0.9 here, but results from long calculations may show 0.8999999; use ROUND if needed.
**Likely follow-ups:** 1) *Between 90 and 95?* Use Between. 2) *Whole row?* Q7.
**Common mistakes:** Typing 90 instead of 90% (or 0.9); forgetting blanks count as zero.

### Q6 ⭐⭐⭐ 🟢 What is Goal Seek in Excel, and when would you use it?
**Asked at:** commonly asked (no company-specific report found); Goal Seek appears in the TrumpExcel list and in a Hirist scenario-modelling question.
**What the interviewer is checking:** Do you know it works backwards from a target result to one input?
**Say this in the interview:** "Goal Seek is reverse calculation. I tell Excel the result I want from a formula and which single input cell it may change, and it finds the input value that gets there."
**Explain simply:**
- Normal: inputs go in, formula gives answer. Goal Seek: answer fixed, find the input.
- You give three things: Set cell (the formula cell), To value (the target), By changing cell (the input) (Microsoft Support, "Use Goal Seek...").
- It handles only one input: "Goal Seek works with only one variable input value" (Microsoft Support, "Introduction to What-If Analysis"). Use Solver for more.
- The changing cell must be a typed number and the Set cell must depend on it.
**Example:** 20 employees at Rs 50,000 each cost Rs 10,00,000 a month. The budget is Rs 11,00,000. What hike % fits?
**Sample sheet:**
| | B | C |
|---|---|---|
| 1 | 20 (headcount) | |
| 2 | 50000 (salary) | |
| 3 | 0 (hike %, changing cell) | 0.1 |
| 4 | `=B1*B2*(1+B3)` | `=B1*B2*(1+C3)` |

**Formula / Steps:** Data tab > Forecast group (Data Tools in older builds) > What-If Analysis > Goal Seek > Set cell: B4 > To value: 1100000 > By changing cell: B3 > OK. Not run here (steps from Microsoft Support).
**Alternative:** Algebra: 1,100,000 / 1,000,000 - 1 = 0.10. Or Solver for several inputs.
**Result:** Goal Seek itself not run here. By algebra the answer is B3 = 0.10; I checked it by running the formula in LibreOffice 24.2: at 0.1, `=B1*B2*(1+C3)` returns 1,100,000; at 0 it returns 1,000,000.
**Version note:** Excel 2016, 2019, 2021, 2024 and Microsoft 365 (Microsoft Support, "Use Goal Seek to find the result you want by adjusting an input value"). Google Sheets has a Goal Seek add-on (from memory, unverified).
**Edge cases:** Result is a static number; it does not update if inputs later change.
**Likely follow-ups:** 1) *Several inputs?* Solver. 2) *Does it always find a solution?* No (Q36).
**Common mistakes:** Picking a changing cell that holds a formula; expecting live updates.

### Q7 ⭐⭐⭐ 🟡 How do you highlight an entire row based on the value in one cell (for example, every row where Status is "Resigned")?
**Asked at:** commonly asked (no company-specific report found); row-highlight by custom formula appears in a Placement Preparation snippet.
**What the interviewer is checking:** Do you know the formula rule with a locked column (`$C2`)?
**Say this in the interview:** "Select the whole table range, New Rule, Use a formula, and enter `=$C2="Resigned"`. The dollar locks the column so every cell in the row looks at Status, and leaving the row unlocked lets each row check its own."
**Explain simply:**
- The formula is written for the top-left cell of the selected range, then Excel adjusts it for the others.
- `$C` (column locked) means "always look at column C". `2` (row free) means each row checks its own row.
- A formula rule must return TRUE or FALSE.
**Example:** Highlight every leaver in a headcount list.
**Sample sheet:**
| | A (ID) | B (Name) | C (Status) |
|---|---|---|---|
| 2 | E01 | Asha | Active |
| 3 | E02 | Bala | Resigned |
| 4 | E03 | Chitra | Active |
| 5 | E04 | Dev | Resigned |
| 6 | E05 | Esha | resigned (trailing space) |
| 7 | E06 | Farid | Notice |

**Formula / Steps:** Select A2:C7 > Home > Conditional Formatting > New Rule > Use a formula to determine which cells to format > `=$C2="Resigned"` > Format > OK (not run here; Microsoft Support).
**Alternative:** Tolerant of spaces: `=TRIM($C2)="Resigned"`.
**Result:** Rule formula run per row in LibreOffice 24.2 (rows 2-7): `=$C2="Resigned"` gives FALSE, TRUE, FALSE, TRUE, FALSE, FALSE. `=TRIM($C2)="Resigned"` also flags Esha (row 6): FALSE, TRUE, FALSE, TRUE, TRUE, FALSE. With the wrong, unlocked `=C2="Resigned"` the test for column A or B in row 3 would look at A3/B3 and be FALSE, so only column C would colour.
**Version note:** Formula rules available in Excel 2016 to 365 (Microsoft Support).
**Edge cases:** The text match ignores case in Excel; use EXACT for case-sensitive.
**Likely follow-ups:** 1) *Several statuses?* `=OR($C2="Resigned",$C2="Terminated")`. 2) *Why mixed reference?* Q25.
**Common mistakes:** `=C2=...` without the dollar; selecting from row 1 headers but writing the formula for row 2.

### Q8 ⭐⭐⭐ 🟡 What is the difference between Goal Seek, Data Table and Scenario Manager?
**Asked at:** commonly asked (no company-specific report found); the "compare the three" framing appears in several prep blogs (snippet level).
**What the interviewer is checking:** Can you pick the right tool for the question being asked?
**Say this in the interview:** "Goal Seek works backwards: given a target, find one input. A Data Table shows results for many values of one or two inputs at once. Scenario Manager saves named sets of inputs, like best, base and worst, and switches between them."
**Explain simply:**
| Tool | Question it answers | Inputs |
|---|---|---|
| Goal Seek | "What input gives this result?" | exactly one |
| Data Table | "What results for these many values?" | one or two |
| Scenario Manager | "What if everything changes together as a set?" | several cells per scenario, up to 32 values |

- Microsoft: scenarios "can only accommodate up to 32 values"; data tables don't support more than two variables; Goal Seek works with one input; scenario summary reports "are not automatically recalculated" (Microsoft Support, "Introduction to What-If Analysis").
**Example:** HR budget: Goal Seek finds the hike % that fits a Rs 11 lakh budget; a Data Table shows total cost for hikes of 5% to 15%; scenarios compare a "hiring freeze" vs "aggressive hiring" plan.
**Formula / Steps:** All three sit at Data > Forecast > What-If Analysis (Data Tools group in some builds). Not run here (steps from Microsoft Support).
**Alternative:** Solver for many inputs with constraints (Q30).
**Version note:** The Goal Seek and data-table pages list Excel 2016, 2019, 2021, 2024 and Microsoft 365; the scenarios page lists only 365, 2024 and 2021, so Scenario Manager in 2016/2019 is from memory, unverified (Microsoft Support, fetched). The command sits in the Forecast group on the Data tab.
**Edge cases:** Data Table output is live; Goal Seek and scenario summary reports are static.
**Likely follow-ups:** 1) *Which for 3 inputs at once?* Scenario Manager or Solver. 2) *Which stays live?* Data Table.
**Common mistakes:** Using Goal Seek for two inputs; thinking scenario reports update.

### Q9 ⭐⭐ 🟢 What is What-If Analysis in Excel, and which tools does it include?
**Asked at:** commonly asked (no company-specific report found); appears in the TrumpExcel list.
**What the interviewer is checking:** Do you know the three built-in tools and the idea of changing inputs to see outputs?
**Say this in the interview:** "What-If Analysis means changing input values to see how the results change. It includes Scenario Manager, Goal Seek and Data Tables, all under the Data tab. Solver is a separate add-in for harder problems."
**Explain simply:**
- Microsoft: "The three built-in What-If tools: Scenarios, Goal Seek, and Data Tables"; Solver "is similar to Goal Seek, but it can accommodate more variables" (Microsoft Support, "Introduction to What-If Analysis").
- Use it to test assumptions before a decision: attrition rate, hiring cost, price.
- The model must be formulas: if the output is hard-typed, nothing can change.
**Example:** A payroll model: change the hike % and watch total cost, or ask which hike keeps cost under Rs 11 lakh.
**Formula / Steps:** Data tab > Forecast group > What-If Analysis > Scenario Manager / Goal Seek / Data Table (not run here; steps from Microsoft Support).
**Alternative:** Plain manual testing: change an input and read the result.
**Version note:** Excel 2016, 2019, 2021, 2024 and Microsoft 365 (Microsoft Support, data-table and Goal Seek pages).
**Edge cases:** Solver must be switched on via File > Options > Add-ins (from memory, unverified).
**Likely follow-ups:** 1) *Difference between them?* Q8. 2) *Is it forecasting?* No, it tests assumptions.
**Common mistakes:** Calling it "forecasting"; forgetting Solver is an add-in.

### Q10 ⭐⭐ 🟢 Walk me through using Goal Seek to find the units you must sell to reach a target profit.
**Asked at:** commonly asked (no company-specific report found); Hirist's list has a Goal Seek/Solver scenario question.
**What the interviewer is checking:** Can you set up profit as a formula and use the dialog's three boxes correctly?
**Say this in the interview:** "Profit must be a formula that depends on units. Then Goal Seek: Set cell is the profit cell, To value is the target, By changing cell is the units cell."
**Explain simply:**
- Profit = units x (price - variable cost) - fixed cost.
- The units cell must hold a typed number, not a formula.
- Goal Seek tries values until the profit equals the target, and overwrites the units cell with its answer.
**Example:** Price Rs 500, variable cost Rs 300, fixed cost Rs 80,000. Target profit Rs 1,20,000.
**Sample sheet:**
| | B | C | D |
|---|---|---|---|
| 1 | 500 (price) | | |
| 2 | 300 (variable cost) | | |
| 3 | 80000 (fixed cost) | | |
| 4 | 0 (units, changing cell) | 1000 | 800 |
| 5 | `=B4*(B1-B2)-B3` | `=C4*(B1-B2)-B3` | `=D4*(B1-B2)-B3` |

**Formula / Steps:** Data > What-If Analysis > Goal Seek > Set cell: B5 > To value: 120000 > By changing cell: B4 > OK > OK to keep the answer (not run here; steps from Microsoft Support).
**Alternative:** Algebra: units = (target + fixed) / (price - variable) = (120000 + 80000) / 200 = 1000.
**Result:** Goal Seek not run here; answer by algebra = 1,000 units. Checked by running the profit formula in LibreOffice 24.2: at 0 units it returns -80,000 (B5), at 800 it returns 80,000, at 1,000 it returns 1,20,000.
**Version note:** Excel 2016 to Microsoft 365 (Microsoft Support, Goal Seek page).
**Edge cases:** If units must be whole, check the answer (Goal Seek may return 999.9999); round up when needed.
**Likely follow-ups:** 1) *Two inputs (price and units)?* Solver. 2) *Result changes when price changes?* No, rerun.
**Common mistakes:** Setting the changing cell to a formula cell; putting the target in "Set cell".

### Q11 ⭐⭐ 🟢 What are Color Scales, Data Bars and Icon Sets in conditional formatting, and when would you use each?
**Asked at:** commonly asked (no company-specific report found); colour-scale heat maps appear in 2025 prep-site snippets.
**What the interviewer is checking:** Do you know the three visual styles and a sensible use for each?
**Say this in the interview:** "Color Scales shade cells on a gradient from low to high, like a heat map. Data Bars draw a bar inside each cell sized by value. Icon Sets sort values into 3 to 5 groups with icons such as traffic lights."
**Explain simply:**
- Color Scales: two or three colours; "visual guides which help you understand data distribution and variation" (Microsoft Support, "Use conditional formatting to highlight information in Excel").
- Data Bars: "A data bar helps you see the value of a cell relative to other cells" (same page). Good for comparing headcount by department.
- Icon Sets: "three to five categories that are distinguished by a threshold value" (Microsoft Support, "Use data bars, color scales, and icon sets to highlight data"). Good for on-track/at-risk/off-track.
**Example:** Colour-scale the monthly attrition % by department; bars for headcount; traffic lights for offer-acceptance (green 80% and above, amber 60-79%, red below 60%).
**Formula / Steps:** Select range > Home > Conditional Formatting > Color Scales / Data Bars / Icon Sets > pick a style. Edit thresholds: Manage Rules > Edit Rule (not run here; steps from Microsoft Support).
**Alternative:** Sparklines or a chart for trends; a formula rule for a single threshold.
**Version note:** Available in Excel 2016 to 365 (Microsoft Support, same page).
**Edge cases:** Outliers stretch a colour scale so every other cell looks the same; set fixed min and max. Icon thresholds default to percent of range, not fixed numbers (from memory, unverified).
**Likely follow-ups:** 1) *Show only the icon?* Yes, tick "Show Icon Only". 2) *Colour blind readers?* Prefer icons or shape, not red/green alone.
**Common mistakes:** Applying a colour scale to mixed units; leaving default percent thresholds.

### Q12 ⭐⭐ 🟢 How do you highlight cells that contain errors such as #N/A or #DIV/0! using conditional formatting?
**Asked at:** commonly asked (no company-specific report found); the error-highlight question is in the TrumpExcel list.
**What the interviewer is checking:** Do you know ISERROR / ISNA inside a formula rule?
**Say this in the interview:** "Use a formula rule: `=ISERROR(D2)` to colour any error, or `=ISNA(E2)` for only #N/A. I like to flag errors rather than hide them so I can fix the cause."
**Explain simply:**
- ISERROR returns TRUE for any error type. ISNA returns TRUE only for #N/A (a failed lookup).
- The formula refers to the first cell of the selected range, without dollars so it moves.
- Hiding errors with IFERROR can bury real problems; highlighting shows them.
**Example:** Achievement % = sales / target; a rep with target 0 or a blank target gives #DIV/0!. A grade lookup returns #N/A for a rep missing from the table.
**Sample sheet:**
| | A (Rep) | B (Sales) | C (Target) | D (Ach%) | E (Grade) |
|---|---|---|---|---|---|
| 2 | Asha | 90 | 100 | `=B2/C2` | `=VLOOKUP(A2,$I$2:$J$3,2,FALSE)` |
| 3 | Bala | 50 | 0 | | |
| 4 | Chitra | 70 | 80 | | |
| 5 | Dev | 40 | (blank) | | |
| 6 | Esha | 60 | 60 | | |

(Lookup table: I2 Asha = A, I3 Chitra = B.)
**Formula / Steps:** Select D2:E6 > Home > Conditional Formatting > New Rule > Use a formula > `=ISERROR(D2)` > Format > OK (not run here; Microsoft Support). Alternative path: Highlight Cells Rules has no error option; use the formula.
**Alternative:** `=ISNA(E2)` for lookups only; `=ISNUMBER(D2)=FALSE` is not the same (also flags text).
**Result:** Run in LibreOffice 24.2. D2:D6 = 0.9, #DIV/0!, 0.875, #DIV/0!, 1. E2:E6 = A, #N/A, B, #N/A, #N/A. `=ISERROR(D2)` per row: FALSE, TRUE, FALSE, TRUE, FALSE. `=ISNA(E2)` per row: FALSE, TRUE, FALSE, TRUE, TRUE.
**Version note:** Formula rules work in Excel 2016 to 365 (Microsoft Support).
**Edge cases:** Esha's grade is #N/A because Esha is missing from the lookup table, not because of her sales; ISNA catches this.
**Likely follow-ups:** 1) *Why not IFERROR?* It hides the problem. 2) *Which function for #REF!?* ISERROR (ISNA misses it).
**Common mistakes:** Using ISNA for #DIV/0!; locking the reference so all cells test the same one.

### Q13 ⭐⭐ 🟢 How do you view, edit, reorder or delete conditional formatting rules (Rules Manager)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you manage rules, not just create them?
**Say this in the interview:** "Home, Conditional Formatting, Manage Rules. In the box I switch 'Show formatting rules for' to This Worksheet to see all, then edit, delete, or move rules up and down. Higher rules take priority."
**Explain simply:**
- The desktop Manage Rules dialog is where "You create, edit, delete, and view all conditional formatting rules"; the same page covers a Duplicate Rule button and Move Up / Move Down arrows, and says "A rule higher in the list has greater precedence" (Microsoft Support, "Use conditional formatting to highlight information in Excel", fetched).
- Clear Rules (same menu) removes rules from the selection or the whole sheet.
- "Applies to" lets you widen or narrow the range a rule covers.
**Example:** After months of copy-paste, an attendance sheet has 14 overlapping rules and is slow. You open Manage Rules, delete the duplicates, and fix "Applies to".
**Formula / Steps:** 1) Home > Styles > Conditional Formatting > Manage Rules. 2) Set "Show formatting rules for" to Current Selection or This Worksheet. 3) Select a rule > Edit Rule / Delete Rule / Move Up / Move Down. 4) Adjust "Applies to" if needed > OK. Not run here (steps from Microsoft Support).
**Alternative:** Home > Conditional Formatting > Clear Rules > Clear Rules from Selected Cells / Entire Sheet.
**Version note:** Dialog on desktop Excel 2016 to 365; Excel for the web shows a Manage Rules task pane (Microsoft Support, same page).
**Edge cases:** Copy-pasting rows splits one rule into many fragments with small "Applies to" ranges.
**Likely follow-ups:** 1) *What is Stop If True?* Q29. 2) *Which rule wins?* The higher one, if formats conflict.
**Common mistakes:** Only looking at the current selection and missing other rules; deleting instead of editing "Applies to".

### Q14 ⭐⭐ 🟢 What are the three error alert styles in data validation (Stop, Warning, Information), and when would you use each?
**Asked at:** commonly asked (no company-specific report found); error alert styles appear in prep-list snippets.
**What the interviewer is checking:** Do you know how strict each style is?
**Say this in the interview:** "Stop refuses the entry completely. Warning says it looks invalid and asks Yes or No to continue. The third style shows a message and lets the user proceed after clicking OK. I use Stop for rules that must hold, like valid status, and the softer ones for guidance."
**Explain simply:**
- Stop: "Require users to fix the error before proceeding." Warning: warn and require Yes or No to continue. Third style: warn but allow proceeding after dismissing (Microsoft Support, "Apply data validation to cells").
- Label point (both pages fetched 2026-10-22): "Apply data validation to cells" lists the third style as "Important" (and never says "Information"), while "Create a drop-down list" says "Information" and "Warning" show a message without blocking entry. The two Microsoft pages genuinely disagree. I recall the dialog showing "Information" (from memory, unverified in the current UI); if asked, say "the third, softer style, called Information in the dialog and Important on one Microsoft page".
- Warning and Information can be overridden, so bad data can still get in.
**Example:** Employee ID: Stop (must be unique). Joining date older than a year: Warning (could be a rehire). Phone number format hint: Information.
**Formula / Steps:** Select cells > Data > Data Validation > Error Alert tab > tick "Show error alert after invalid data is entered" > Style: Stop / Warning / Information > Title and Error message > OK (not run here; steps from Microsoft Support).
**Alternative:** Combine with an Input Message (Q16) so people know the rule before they type.
**Version note:** Excel 2016, 2019, 2021, 2024, 365 and Excel for the web (Microsoft Support).
**Edge cases:** Default message if blank: "The value you entered is not valid. A user has restricted values that can be entered into this cell." (Microsoft Support, "Create a drop-down list").
**Likely follow-ups:** 1) *Which is default?* Stop. 2) *Does Warning log anything?* No.
**Common mistakes:** Using Warning when the data must be exact; leaving the default message.

### Q15 ⭐⭐ 🟢 How do you restrict a cell so that it accepts only whole numbers between 18 and 60 (for example, employee age)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the Whole number type and Between?
**Say this in the interview:** "Select the cells, Data, Data Validation, Allow Whole number, Data between, Minimum 18, Maximum 60. Add an error message telling the user the allowed range."
**Explain simply:**
- Whole number means no decimals, so 35.5 is rejected.
- Between includes both ends: 18 and 60 are accepted.
- Text such as "abc" is rejected.
**Example:** An age column in a joiners form.
**Sample sheet:**
| | A (Age typed) |
|---|---|
| 2 | 17 |
| 3 | 18 |
| 4 | 35.5 |
| 5 | 60 |
| 6 | 61 |
| 7 | abc |
| 8 | (blank) |
| 9 | '25 (text) |

**Formula / Steps:** Data > Data Validation > Settings > Allow: Whole number > Data: between > Minimum 18 > Maximum 60 > Error Alert tab: Stop, message "Enter age 18 to 60" > OK (not run here; steps from Microsoft Support, "Apply data validation to cells").
**Alternative:** Custom rule `=AND(ISNUMBER(A2),A2=INT(A2),A2>=18,A2<=60)`.
**Result:** The dialog is not run here. The custom formula equivalent, run in LibreOffice 24.2 on rows 2-9: FALSE, TRUE, FALSE, TRUE, FALSE, #VALUE! (for "abc" the INT test errors on text in LibreOffice; how Excel treats an error result inside a validation rule is not verified, so wrap it as `=IF(ISNUMBER(A2),AND(A2=INT(A2),A2>=18,A2<=60),FALSE)` to get a clean FALSE), FALSE (blank), FALSE (text 25, entered here as the text 25).
**Version note:** Excel 2016 to 365 (Microsoft Support).
**Edge cases:** With "Ignore blank" ticked, an empty cell is allowed (not tested by the formula above). A text "25" typed with an apostrophe fails; pasted values bypass the rule.
**Likely follow-ups:** 1) *Allow decimals?* Use Decimal. 2) *Dynamic limits?* Reference cells instead of numbers.
**Common mistakes:** Choosing Decimal instead of Whole number; forgetting the error message.

### Q16 ⭐⭐ 🟢 How do you add an input message and a custom error message to a data validation rule?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the two other tabs of the dialog?
**Say this in the interview:** "In the Data Validation dialog, the Input Message tab shows a hint when someone clicks the cell. The Error Alert tab lets me write my own title and message and choose the style."
**Explain simply:**
- Input message appears as a small note when the cell is selected.
- Error alert appears when a bad value is entered; without custom text Excel uses a generic message.
- Good messages say what is allowed: "Enter a whole number from 18 to 60."
**Example:** Age cell: input title "Age", message "18 to 60 only". Error title "Invalid age", message "Age must be a whole number between 18 and 60."
**Formula / Steps:** 1) Select cells > Data > Data Validation. 2) Input Message tab > tick "Show input message when cell is selected" > Title, Input message. 3) Error Alert tab > tick "Show error alert after invalid data is entered" > Style > Title, Error message > OK. Not run here (steps from Microsoft Support, "Apply data validation to cells").
**Alternative:** A visible note column beside the entry area, or cell comments.
**Version note:** Excel 2016 to 365 (Microsoft Support).
**Edge cases:** Titles and message have length limits (from memory, unverified: about 32 and 255 characters; the Microsoft page I fetched, "Apply data validation to cells", states no limits).
**Likely follow-ups:** 1) *Error style?* Q14. 2) *Does the message show on paste?* No (Q40).
**Common mistakes:** Setting the message but leaving the tick box off.

### Q17 ⭐⭐ 🟢 How do you highlight cells that contain specific text, for example every department that contains "Sales"?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know "Text that Contains" and the SEARCH formula alternative?
**Say this in the interview:** "Highlight Cells Rules, Text that Contains, type Sales. For a formula rule I use `=ISNUMBER(SEARCH("Sales",A2))`; SEARCH finds the text anywhere in the cell and ignores capitals."
**Explain simply:**
- SEARCH returns the position of the text, or an error if absent. ISNUMBER turns that into TRUE/FALSE.
- FIND is the same but case-sensitive.
- "Contains" matches inside words: "Salesforce Admin" also matches.
**Example:** Colour every Sales-related department row.
**Sample sheet:**
| | A (Department) |
|---|---|
| 2 | Sales |
| 3 | Inside Sales |
| 4 | Pre-sales |
| 5 | Marketing |
| 6 | SALES Ops |
| 7 | Finance |
| 8 | Salesforce Admin |

**Formula / Steps:** Select A2:A8 > Home > Conditional Formatting > Highlight Cells Rules > Text that Contains > Sales > choose format (not run here; Microsoft Support). Formula rule: `=ISNUMBER(SEARCH("Sales",A2))`.
**Alternative:** Starts with only: `=LEFT(A2,5)="Sales"`; case-sensitive: `=ISNUMBER(FIND("Sales",A2))`.
**Result:** Run in LibreOffice 24.2, rows 2-8. SEARCH rule: TRUE, TRUE, TRUE, FALSE, TRUE, FALSE, TRUE. FIND rule: TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, TRUE. LEFT rule: TRUE, FALSE, FALSE, FALSE, TRUE, FALSE, TRUE.
**Version note:** Excel 2016 to 365 (Microsoft Support, highlight rules).
**Edge cases:** Wildcard characters like * and ? in the search text are treated as wildcards by SEARCH.
**Likely follow-ups:** 1) *Case-sensitive?* FIND. 2) *Cell references for the text?* `SEARCH($F$1,A2)`.
**Common mistakes:** Forgetting that "Contains" also hits "Salesforce"; using FIND and missing "SALES".

### Q18 ⭐⭐ 🟡 What is a one-variable data table, and how do you build one?
**Asked at:** commonly asked (no company-specific report found); the one- and two-variable data table questions are in the TrumpExcel list.
**What the interviewer is checking:** Do you know the layout and which input cell box to use?
**Say this in the interview:** "It shows the result of a formula for a list of values of one input. I put the values in a column, the formula one row above and one cell to the right, select all, then Data, What-If Analysis, Data Table, and give the column input cell."
**Explain simply:**
- Excel substitutes each listed value into your input cell and records the formula's answer.
- The input cell must be a real cell the formula uses.
- Microsoft's layout: column-oriented tables put the formula "one row above and one cell to the right of the values" (Microsoft Support, "Calculate multiple results by using a data table").
**Example:** Loan Rs 10,00,000 over 60 months. How does the monthly EMI (loan payment) change with the interest rate?
**Sample sheet:**
| | B | D (Rates) | E |
|---|---|---|---|
| 1 | 1000000 (loan) | | `=B4` |
| 2 | 0.09 (rate) | 0.08 | table result |
| 3 | 60 (months) | 0.09 | |
| 4 | `=-PMT(B2/12,B3,B1)` | 0.10 | |
| 5 | | 0.11 | |
| 6 | | 0.12 | |

**Formula / Steps:** Select D1:E6 > Data > Forecast > What-If Analysis > Data Table > Column input cell: B2 > OK. Excel fills E2:E6 with an array formula `{=TABLE(,B2)}`. Not run here (steps from Microsoft Support).
**Alternative:** Write `=-PMT(D2/12,$B$3,$B$1)` beside each rate (live and easier to audit).
**Result:** The Data Table command is not run here. The equivalent PMT formula, run in LibreOffice 24.2: base EMI (9%) 20,758.36; for 8% to 12%: 20,276.39, 20,758.36, 21,247.04, 21,742.42, 22,244.45.
**Version note:** Excel 2016 to 365; in Excel 2016 What-If Analysis sits in the Forecast group (Microsoft Support, same page).
**Edge cases:** You cannot edit part of the result block; each formula in a one-variable table must refer to only one input cell (same page).
**Likely follow-ups:** 1) *Row input vs column input?* Values down a column use Column input cell. 2) *Two inputs?* Q19.
**Common mistakes:** Entering the wrong input cell box; pointing at a cell the formula does not use.

### Q19 ⭐⭐ 🟡 How do you build a two-variable data table, for example loan EMI against interest rate and tenure?
**Asked at:** commonly asked (no company-specific report found); in the TrumpExcel list.
**What the interviewer is checking:** Can you place the corner formula and assign row and column input cells correctly?
**Say this in the interview:** "Put the formula in the top-left corner, rates down the column, tenures across the row, select the whole block, Data Table, then Row input cell is the tenure cell and Column input cell is the rate cell."
**Explain simply:**
- Two inputs, one formula. Row input cell goes with the values across the top row; Column input cell with the values down the side (Microsoft Support, "Calculate multiple results by using a data table").
- More than two variables is not supported; use scenarios (same page).
- The corner formula must depend on both input cells.
**Example:** EMI for a Rs 10 lakh loan at five rates and four tenures.
**Sample sheet:**
| | B | D | E | F | G | H |
|---|---|---|---|---|---|---|
| 1 | 1000000 | `=-PMT(B2/12,B3,B1)` | 36 | 48 | 60 | 72 |
| 2 | 0.09 | 0.08 | | | | |
| 3 | 60 | 0.09 | | | | |
| 4 | | 0.10 | | | | |
| 5 | | 0.11 | | | | |
| 6 | | 0.12 | | | | |

**Formula / Steps:** Select D1:H6 > Data > What-If Analysis > Data Table > Row input cell: B3 (months) > Column input cell: B2 (rate) > OK. Excel writes `{=TABLE(B3,B2)}`. Not run here (steps from Microsoft Support).
**Alternative:** Mixed-reference formula in E2: `=-PMT($D2/12,E$1,$B$1)` copied across and down.
**Result:** Data Table not run here. The equivalent PMT grid, run in LibreOffice 24.2 (rows 8% to 12%; columns 36, 48, 60, 72 months): 8%: 31,336.37 / 24,412.92 / 20,276.39 / 17,533.24; 9%: 31,799.73 / 24,885.04 / 20,758.36 / 18,025.54; 10%: 32,267.19 / 25,362.58 / 21,247.04 / 18,525.84; 11%: 32,738.72 / 25,845.52 / 21,742.42 / 19,034.08; 12%: 33,214.31 / 26,333.84 / 22,244.45 / 19,550.19.
**Version note:** Excel 2016 to 365 (Microsoft Support).
**Edge cases:** Swapping row and column input cells gives wrong numbers with no error. Input cells must be on the same sheet as the table (from memory, unverified).
**Likely follow-ups:** 1) *Why slow?* Data tables recalculate often (Q37). 2) *Three variables?* Scenario Manager or Solver.
**Common mistakes:** Swapping the two input boxes; putting hard-typed numbers in the corner.

### Q20 ⭐⭐ 🟡 How do you prevent duplicate entries in a column (for example, Employee ID) using data validation?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the Custom rule with COUNTIF and when it fires?
**Say this in the interview:** "Select the column range, Data Validation, Allow Custom, formula `=COUNTIF($A$2:$A$8,A2)=1`. If someone types an ID that already exists, the count is 2 and Excel rejects it."
**Explain simply:**
- Microsoft's example: "=COUNTIF($A$2:$A$10,A2)=1" makes all values unique; write it for the first cell, then it adjusts for the rest (Microsoft Support, "Apply data validation to cells").
- It only checks new entries; old duplicates stay until you clean them.
- COUNTIF ignores letter case: e101 matches E101.
**Example:** Employee IDs must be unique.
**Sample sheet:**
| | A (Emp ID) |
|---|---|
| 2 | E101 |
| 3 | E102 |
| 4 | E103 |
| 5 | E104 |
| 6 | E105 |
| 7 | E103 (new entry) |
| 8 | e101 (new entry) |

**Formula / Steps:** Select A2:A8 > Data > Data Validation > Allow: Custom > Formula: `=COUNTIF($A$2:$A$8,A2)=1` > Error Alert: Stop > OK (not run here; steps from Microsoft Support).
**Alternative:** Highlight duplicates with conditional formatting (Q4) instead of blocking; or `=COUNTIF(A:A,A2)=1` for the whole column.
**Result:** Dialog not run here. The rule formula run in LibreOffice 24.2 on rows 2-8: FALSE, TRUE, FALSE, TRUE, TRUE, FALSE, FALSE. Because E101 (row 2, matched by e101) and E103 now each appear twice, both copies of each fail; E102, E104, E105 pass. In real entry, Excel evaluates only the cell being typed, so the typed E103 and e101 are the ones rejected.
**Version note:** Excel 2016 to 365 (Microsoft Support).
**Edge cases:** Trailing spaces make "E103 " unique; pasting bypasses the rule; very long numeric IDs can be miscounted (from memory, unverified).
**Likely follow-ups:** 1) *Case-sensitive?* Use SUMPRODUCT with EXACT. 2) *Existing duplicates?* Circle Invalid Data (Q32).
**Common mistakes:** Forgetting the dollar signs on the range; using `>0` instead of `=1`.

### Q21 ⭐⭐ 🟡 How do you create a dependent (cascading) drop-down list, for example State and then City?
**Asked at:** commonly asked (no company-specific report found); dependent drop-down is a standard follow-up in prep sources (snippet level).
**What the interviewer is checking:** Do you know the named-range plus INDIRECT technique?
**Say this in the interview:** "I make a named range for each state's cities, with the name equal to the state. The City drop-down source is `=INDIRECT(A2)`, so it shows the cities for whatever State was chosen in A2."
**Explain simply:**
- INDIRECT turns text ("Telangana") into a reference to the range of that name.
- Named ranges can't contain spaces: "Tamil Nadu" must be named Tamil_Nadu, so use `=INDIRECT(SUBSTITUTE(A2," ","_"))`.
- If the name doesn't match, the drop-down errors.
**Example:** State list in A2; city lists under each state heading.
**Sample sheet:**
| | A (Telangana) | B (Tamil Nadu) | C (Kerala) | E |
|---|---|---|---|---|
| 2 | Hyderabad | Chennai | Kochi | Tamil Nadu (selected state) |
| 3 | Warangal | Coimbatore | Kozhikode | |
| 4 | Nizamabad | | | |

**Formula / Steps:** 1) Select A1:C4 > Formulas > Create from Selection > Top row (names Telangana, Tamil_Nadu, Kerala; then resize each name to its filled cells). 2) State cell: Data Validation > List > source `=$A$1:$C$1`. 3) City cell: Data Validation > List > Source `=INDIRECT(SUBSTITUTE(E2," ","_"))`. Not run here (dialog steps; from memory, unverified: Microsoft's pages I fetched do not cover this).
**Alternative:** Without named ranges: Source `=OFFSET($A$1,1,MATCH(E2,$A$1:$C$1,0)-1,COUNTA(OFFSET($A$1,1,MATCH(E2,$A$1:$C$1,0)-1,10,1)),1)`.
**Result:** Re-run in LibreOffice 24.2 with the three named ranges defined (headers typed as "Tamil Nadu" with a space): `=INDIRECT(SUBSTITUTE(E2," ","_"))` returns a 2-item range (second item Coimbatore); the OFFSET version also returns 2 rows (second item Coimbatore). The drop-down dialog is not run here.
**Version note:** INDIRECT method works in all desktop versions Excel 2016 to 365 (from memory, unverified). Dynamic-array alternatives (Q22) need 365/2021.
**Edge cases:** Blank city cells inside a named range show as blanks in the list; INDIRECT is volatile (recalculates every change).
**Likely follow-ups:** 1) *Why #REF!?* Name doesn't match the state text. 2) *Without INDIRECT?* OFFSET/MATCH.
**Common mistakes:** Spaces in names; naming ranges with the header included.

### Q22 ⭐⭐ 🟡 How do you make a drop-down list update automatically when new items are added to the source list?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know tables or dynamic ranges, not fixed ranges?
**Say this in the interview:** "Put the source list in an Excel table and base the drop-down on it, or use a dynamic named range. Then new rows are picked up without editing the validation."
**Explain simply:**
- Fixed `$A$2:$A$5` won't include row 6.
- Tables: Microsoft says that when your data is in a table, "any drop-downs you based on that table will automatically update" (Microsoft Support, "Create a drop-down list").
- Dynamic range: `OFFSET` with `COUNTA` sizes the list to the filled cells.
**Example:** Department list Sales, HR, Finance, IT; HR adds Legal.
**Sample sheet:**
| | A (Dept) |
|---|---|
| 1 | Dept |
| 2 | Sales |
| 3 | HR |
| 4 | Finance |
| 5 | IT |
| 6 | Legal (added later) |

**Formula / Steps:** Table route: select A1:A5 > Ctrl+T > data validation source: select the data cells (A2:A5, no header). Dynamic-name route: Formulas > Name Manager > New > name `DeptList`, Refers to `=OFFSET($A$2,0,0,COUNTA($A$2:$A$100),1)`; Source `=DeptList`. Not run here (steps from Microsoft Support for the table route; the named-range steps are from memory, unverified).
**Alternative:** 365/2021 only: source `=$D$2#` pointing to a spilled formula such as UNIQUE. Not run here. The Microsoft pages I fetched do not mention spill references; my only support is third-party blog snippets (WPS, Office Watch, Excel University via search), so treat it as unverified.
**Result:** The OFFSET/COUNTA sizing was run in LibreOffice 24.2: list size is 4 rows with four items, 5 after adding Legal in A6. Drop-down behaviour itself is not run here.
**Version note:** Table route: Excel 2016 to 365 (Microsoft Support). Spill-range route: Excel 365 or 2021 only (third-party, unverified). In Google Sheets a range-based dropdown also picks up added rows if you pick an open-ended range (from memory, unverified).
**Edge cases:** A cell holding a formula that returns "" counts in COUNTA: size rose to 6 in my test with one `=""` cell, so the list gains a blank entry. Leave no gaps.
**Likely follow-ups:** 1) *Table reference in validation?* Use a named range pointing to the table column. 2) *Why not whole column A:A?* Blank entries and the header appear.
**Common mistakes:** Including the header; leaving blank rows in the list.

### Q23 ⭐⭐ 🟡 How do you highlight employee contracts that expire within the next 30 days?
**Asked at:** commonly asked (no company-specific report found); a natural HR task, gap-filled from standard practice.
**What the interviewer is checking:** Can you write a date-window rule with TODAY and exclude expired contracts?
**Say this in the interview:** "A formula rule: `=AND(B2>=TODAY(),B2<=TODAY()+30)`. That is today or later, and no more than 30 days away, so already expired contracts are not coloured."
**Explain simply:**
- Dates in Excel are numbers, so adding 30 means 30 days later.
- TODAY() changes every day, so the highlight updates by itself.
- Without the first test, every past date also satisfies "less than today + 30".
**Example:** Today is 22-Oct-2026. Contracts ending by 21-Nov-2026 are due.
**Sample sheet:** (H1 holds the date 22-Oct-2026, standing in for TODAY() so the result is repeatable)
| | A (Emp) | B (End date) |
|---|---|---|
| 2 | E01 | 10-Oct-2026 |
| 3 | E02 | 22-Oct-2026 |
| 4 | E03 | 05-Nov-2026 |
| 5 | E04 | 21-Nov-2026 |
| 6 | E05 | 22-Nov-2026 |
| 7 | E06 | (blank) |
| 8 | E07 | 30-Nov-2026 typed as text |

**Formula / Steps:** Select B2:B8 (or A2:B8 for the row, with `$B2`) > Home > Conditional Formatting > New Rule > Use a formula > `=AND($B2>=TODAY(),$B2<=TODAY()+30)` > Format > OK (not run here; steps from Microsoft Support).
**Alternative:** Built-in: Highlight Cells Rules > A Date Occurring > Next Month (calendar month, not 30 days; from memory, unverified). Add `ISNUMBER` to exclude text.
**Result:** Rule logic run in LibreOffice 24.2 with H1 as today: `=AND(B2>=$H$1,B2<=$H$1+30)` gives FALSE (12 days past), TRUE (today), TRUE (14 days), TRUE (30 days, boundary included), FALSE (31 days), FALSE (blank), FALSE (text). The text date stayed text in this test, so it is not matched; the ISNUMBER-guarded version also gives FALSE.
**Version note:** TODAY and formula rules work in Excel 2016 to 365 (Microsoft Support for the formula-rule feature).
**Edge cases:** A blank date is 0 and fails the test, good. Text dates are not numbers; convert them. TODAY() uses the PC clock. In Excel a text date may be coerced differently than in LibreOffice (from documentation/memory, unverified).
**Likely follow-ups:** 1) *Show expired in red?* Add a second rule `=AND(ISNUMBER($B2),$B2<TODAY())`. 2) *Business days?* Use WORKDAY.
**Common mistakes:** Forgetting the lower bound; locking B2 as $B$2.

### Q24 ⭐⭐ 🟡 How do you highlight the top 10 values, the bottom 10% or the values above average?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the built-in Top/Bottom Rules and what each one measures (a count, a percentage, or the average)?
**Say this in the interview:** "Home > Conditional Formatting > Top/Bottom Rules has Top 10 Items, Bottom 10%, and Above Average. I pick the rule, type the number if needed, choose a colour, and Excel re-colours itself whenever the numbers change."
**Explain simply:**
- *Conditional formatting* means a cell changes colour automatically based on its value or a formula.
- *Top 10 Items* picks the N biggest values (you can change 10 to any number from 1 to 1000); *Bottom 10%* picks the smallest tenth of the cells by count; *Above Average* compares each cell with the average of the selected range.
- These rules only look at numbers in the range you selected, so select just the data column, not the header.
**Example:** 12 employees' bonuses (Rs 000). Average is 56.58. Rule "Top 3" colours 70, 66 and 90; Bottom 10% of 12 cells colours only the lowest value, 35; Above Average colours the 6 values above 56.58 (61, 70, 66, 90, 58, 64).
**Sample sheet:**

Column A = Employee, column B = Bonus (Rs 000).

|  | A | B |
|---|---|---|
| 2 | Asha | 42 |
| 3 | Ravi | 55 |
| 4 | Meena | 61 |
| 5 | Karan | 38 |
| 6 | Divya | 70 |
| 7 | Imran | 66 |
| 8 | Sneha | 52 |
| 9 | Vikram | 48 |
| 10 | Neha | 90 |
| 11 | Arjun | 35 |
| 12 | Pooja | 58 |
| 13 | Rahul | 64 |

**Formula / Steps:** Conditional-formatting dialog: not run here (steps from Microsoft Support, "Use conditional formatting to highlight information in Excel"): 1) select B2:B13. 2) Home tab > Styles group > Conditional Formatting > Top/Bottom Rules > Top 10 Items (change 10 to 3 for the demo) / Bottom 10% / Above Average. 3) Pick a format > OK. Equivalent rule formulas (Manage Rules > New Rule > "Use a formula"), entered for B2:B13: Top 3 `=B2>=LARGE($B$2:$B$13,3)`; bottom 10% (my equivalent) `=B2<=SMALL($B$2:$B$13,MAX(1,INT(COUNT($B$2:$B$13)*0.1)))`; above average `=B2>AVERAGE($B$2:$B$13)`.
**Alternative:** The advanced route: Manage Rules > New Rule > "Format only top or bottom ranked values" (tick "% of the selected range" for percentages) or "Format only values that are above or below average" (Microsoft Support, same page).
**Result:** Rule formulas run in LibreOffice 24.2 on each row (TRUE = cell would be coloured):

| Row | Employee | Bonus | Top 3 | Bottom 10% | Above avg |
|---|---|---|---|---|---|
| 2 | Asha | 42 | FALSE | FALSE | FALSE |
| 3 | Ravi | 55 | FALSE | FALSE | FALSE |
| 4 | Meena | 61 | FALSE | FALSE | TRUE |
| 5 | Karan | 38 | FALSE | FALSE | FALSE |
| 6 | Divya | 70 | TRUE | FALSE | TRUE |
| 7 | Imran | 66 | TRUE | FALSE | TRUE |
| 8 | Sneha | 52 | FALSE | FALSE | FALSE |
| 9 | Vikram | 48 | FALSE | FALSE | FALSE |
| 10 | Neha | 90 | TRUE | FALSE | TRUE |
| 11 | Arjun | 35 | FALSE | TRUE | FALSE |
| 12 | Pooja | 58 | FALSE | FALSE | TRUE |
| 13 | Rahul | 64 | FALSE | FALSE | TRUE |

The dialog itself: not run here.
**Version note:** All three rules exist in every desktop version since Excel 2007 (from memory, unverified); Microsoft Support page documents Windows, Mac and web paths.
**Edge cases:** Ties at the cut-off can colour more cells than N. Excel's own rounding for "Bottom 10%" is not documented on the page I read; my formula (1 cell for 12 rows) is an equivalent, not a copy of Excel's internals. Text and blanks are ignored.
**Likely follow-ups:** 1) *Top 10 by what?* By the selected column only; add a rule per column. 2) *Top 10 per department?* The built-in rule cannot; use a helper column with the rank inside each department (RANK or COUNTIFS) and a formula rule on it, or a PivotTable. 3) *Above average of what?* Of the whole selected range.
**Common mistakes:** Selecting the header row too; expecting Top 10 to pick "10 percent"; using a fixed colour rule per month instead of one rule that updates itself.

### Q25 ⭐⭐ 🟡 Why do formula-based conditional formatting rules need mixed references such as $B2, and what goes wrong if you get them wrong?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand relative versus absolute references inside a rule that Excel copies across many cells?
**Say this in the interview:** "The rule is written for the top-left cell and Excel shifts it for every other cell. $B2 locks the column but lets the row move, so every cell in the row checks column B of its own row. Without the $ the check drifts sideways."
**Explain simply:**
- A *relative reference* (B2) shifts when copied; an *absolute reference* ($B$2) never shifts; a *mixed reference* ($B2) locks only the column.
- Excel evaluates your rule as if typed in the first (active) cell of the range, then adjusts it for every other cell.
- For "colour the whole row when Status is Resigned", the Status column must stay fixed (column locked) while the row changes: `=$C2="Resigned"`.
- Pitfall: the active cell when you open New Rule decides what "B2" means; if the active cell is not the top-left of the range, the rule is shifted wrong.
**Example:** Applied to A2:C7, a correct rule colours the whole row of Ravi and Karan (2 rows x 3 columns = 6 cells). The no-$ version colours only the Status cells (2 cells). The fully locked `$C$2` colours nothing, because C2 is "Active".
**Sample sheet:**

Column A = Employee, B = Department, C = Status.

|  | A | B | C |
|---|---|---|---|
| 2 | Asha | Sales | Active |
| 3 | Ravi | HR | Resigned |
| 4 | Meena | Finance | Active |
| 5 | Karan | Sales | Resigned |
| 6 | Divya | IT | Active |
| 7 | Imran | HR | Active |

**Formula / Steps:** Conditional-formatting dialog: not run here (steps from Microsoft Support, "Use conditional formatting to highlight information in Excel"): select A2:C7 (start from A2) > Home > Conditional Formatting > New Rule > "Use a formula to determine which cells to format" > `=$C2="Resigned"` > Format > OK.
**Alternative:** Make the whole row check from a helper column: D2 `=C2="Resigned"` and rule `=$D2`. Or use a table column and structured highlighting, but the mixed reference is the standard answer.
**Result:** Rule formula evaluated in LibreOffice for each of the 18 cells of A2:C7 (TRUE = coloured). Correct `=$C2="Resigned"`:

| Row | A | B | C |
|---|---|---|---|
| 2 | FALSE | FALSE | FALSE |
| 3 | TRUE | TRUE | TRUE |
| 4 | FALSE | FALSE | FALSE |
| 5 | TRUE | TRUE | TRUE |
| 6 | FALSE | FALSE | FALSE |
| 7 | FALSE | FALSE | FALSE |

Wrong, no dollar `=A2="Resigned"` (shifts across columns):

| Row | A | B | C |
|---|---|---|---|
| 2 | FALSE | FALSE | FALSE |
| 3 | FALSE | FALSE | TRUE |
| 4 | FALSE | FALSE | FALSE |
| 5 | FALSE | FALSE | TRUE |
| 6 | FALSE | FALSE | FALSE |
| 7 | FALSE | FALSE | FALSE |

Wrong, fully locked `=$C$2="Resigned"`:

| Row | A | B | C |
|---|---|---|---|
| 2 | FALSE | FALSE | FALSE |
| 3 | FALSE | FALSE | FALSE |
| 4 | FALSE | FALSE | FALSE |
| 5 | FALSE | FALSE | FALSE |
| 6 | FALSE | FALSE | FALSE |
| 7 | FALSE | FALSE | FALSE |

The colouring itself: not run here.
**Version note:** Same in all Excel versions and Google Sheets (Sheets: write the formula for the first cell of the range, using dollar signs, Google Docs Editors Help, "Use conditional formatting rules in Google Sheets").
**Edge cases:** Text compare `="Resigned"` is not case-sensitive. Spaces in the data ("Resigned ") make the test FALSE. A rule formula that returns an error colours nothing (Microsoft Support page).
**Likely follow-ups:** 1) *Locking the row too ($C$2)?* Every cell checks C2 only. 2) *Why does my rule colour the wrong rows?* The active cell was not the top-left cell, so references shifted. 3) *Mixed with the row locked?* `C$2` is for header-driven rules, e.g. weekends (Q28).
**Common mistakes:** Typing `=C2="Resigned"` and wondering why only one column colours; clicking a cell with the mouse while the formula box is active (Excel inserts a fully locked address); applying the rule to the wrong "Applies to" range.

### Q26 ⭐⭐ 🟡 What is Scenario Manager, and how do you create best-case, base-case and worst-case scenarios?
**Asked at:** commonly asked; Scenario Manager appears in a prep-site question list (TrumpExcel, per Part 9 sources file); no company-specific report found
**What the interviewer is checking:** Can you save several sets of inputs and compare the outcome, instead of retyping numbers?
**Say this in the interview:** "Scenario Manager stores named sets of input values, say Best, Base and Worst, and swaps them into the sheet with one click. A Summary report then puts the results side by side."
**Explain simply:**
- A *scenario* is a saved set of values for chosen *changing cells* (the input cells). A scenario can hold up to 32 values, but you can make as many scenarios as you want (Microsoft Support, "Switch between various sets of values by using scenarios").
- The result cell must be a formula that depends on the changing cells, here Profit.
- Scenario Manager sits under Data > Forecast > What-If Analysis.
**Example:** Product with unit cost Rs 300 and fixed cost Rs 1,20,000. Best: price 500, 1,200 units. Base: 450 and 1,000. Worst: 400 and 700. Profit = Units x (Price - Unit cost) - Fixed cost.
**Sample sheet:**

Inputs in B1:B4, result in B6.

|  | A | B |
|---|---|---|
| 1 | Price | 450 |
| 2 | Units | 1000 |
| 3 | Unit cost | 300 |
| 4 | Fixed cost | 120000 |
| 5 |  |  |
| 6 | Profit | =B2*(B1-B3)-B4 |

**Formula / Steps:** Scenario Manager dialog: not run here (steps from Microsoft Support). 1) Data tab > Forecast group > What-If Analysis > Scenario Manager > Add. 2) Scenario name "Best", Changing cells `B1:B2` > OK. 3) Type 500 and 1200 > OK. 4) Add again for "Base" (450, 1000) and "Worst" (400, 700). 5) Select a scenario > Show to load it. 6) Summary > Scenario summary > Result cells `B6` > OK.
**Alternative:** Without the dialog: lay the three cases in columns and one profit formula under each (as run below), or use a two-variable Data Table (Q19).
**Result:** Profit formula run in LibreOffice 24.2 for each scenario's inputs:

| Row | A Case | B Price | C Units | D Unit cost | E Fixed cost | F Profit |
|---|---|---|---|---|---|---|
| 2 | Best | 500 | 1200 | 300 | 120000 | 120000 |
| 3 | Base | 450 | 1000 | 300 | 120000 | 30000 |
| 4 | Worst | 400 | 700 | 300 | 120000 | -50000 |

Scenario Manager itself: not run here.
**Version note:** Scenario Manager is in all desktop Excel versions; Microsoft Support page "Introduction to What-If Analysis" lists Excel 365, 2024 and 2021 (older versions: from memory, available). Google Sheets has no Scenario Manager (from memory, unverified).
**Edge cases:** The Summary report is a static snapshot (Q42). Changing cells must hold values, not formulas. More than 32 inputs cannot be in one scenario (Microsoft Support). Scenarios are stored in the sheet where they were created.
**Likely follow-ups:** 1) *Limit?* 32 values per scenario. 2) *Can I merge scenarios?* Yes, from other workbooks via Merge (Microsoft Support). 3) *vs Data Table?* Data Table varies 1-2 inputs across many values; scenarios save named bundles (Q8).
**Common mistakes:** Naming scenarios vaguely; pointing the summary at an input cell instead of the profit cell; forgetting that the sheet shows the last scenario you clicked Show on.

### Q27 ⭐⭐ 🟡 How do you highlight names in List A that are missing from List B (for example, employees on the payroll but not on the attendance list)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you write a rule that checks one list against another with COUNTIF or MATCH?
**Say this in the interview:** "Select the payroll list and add a formula rule: `=COUNTIF(attendance list, first cell)=0`. If the name is not found anywhere in the attendance list the count is zero and the cell is coloured."
**Explain simply:**
- *COUNTIF(range, value)* counts how many cells in the range equal the value. Zero means "missing".
- Lock the other list with dollar signs ($D$2:$D$6) so it does not slide down; leave the first cell relative (A2).
- A rule can look at cells on another worksheet of the same workbook, but not at another workbook (Microsoft Support, "Use conditional formatting to highlight information in Excel", fetched). Which Excel versions allow the direct sheet reference was not verified; a named range is the safe route.
**Example:** Payroll has 7 names, attendance has 5. Meena, Karan and Sneha are on payroll but not in attendance: 3 people to investigate.
**Sample sheet:**

Payroll names in A2:A8, attendance names in D2:D6.

|  | A (Payroll) | D (Attendance) |
|---|---|---|
| 2 | Asha | Ravi |
| 3 | Ravi | Asha |
| 4 | Meena | Divya |
| 5 | Karan | Imran |
| 6 | Divya | Neha |
| 7 | Imran |  |
| 8 | Sneha |  |

**Formula / Steps:** Conditional-formatting dialog: not run here (steps from Microsoft Support, "Use conditional formatting to highlight information in Excel"): select A2:A8 > Home > Conditional Formatting > New Rule > "Use a formula to determine which cells to format" > `=COUNTIF($D$2:$D$6,A2)=0` > Format > OK.
**Alternative:** `=ISNA(MATCH(A2,$D$2:$D$6,0))`, or `=ISERROR(MATCH(...))`. In 365 you can also test `=NOT(ISNUMBER(XMATCH(...)))` (not run here).
**Result:** Rule formulas run in LibreOffice 24.2 (TRUE = coloured):

| Row | Name | COUNTIF rule | MATCH rule |
|---|---|---|---|
| 2 | Asha | FALSE | FALSE |
| 3 | Ravi | FALSE | FALSE |
| 4 | Meena | TRUE | TRUE |
| 5 | Karan | TRUE | TRUE |
| 6 | Divya | FALSE | FALSE |
| 7 | Imran | FALSE | FALSE |
| 8 | Sneha | TRUE | TRUE |

Colouring itself: not run here.
**Version note:** COUNTIF and MATCH work in every version and in Google Sheets (use a custom formula rule; for another sheet wrap the range in INDIRECT, Google Docs Editors Help).
**Edge cases:** COUNTIF ignores case and treats `*` and `?` as wildcards (Microsoft Support CF page notes wildcards for duplicates). Trailing spaces make names unequal: TRIM the data first. Same name spelt differently counts as missing. Blank cells in List A would be coloured unless you add `A2<>""`.
**Likely follow-ups:** 1) *Show names in B missing from A?* Select list B and swap the ranges. 2) *Extract the list instead of colouring?* Use FILTER in 365 or a helper column. 3) *Two columns must match (ID and name)?* Use COUNTIFS.
**Common mistakes:** Forgetting `$` on the second list; using `=COUNTIF(...)` without `=0`, which colours the names that are present; mixing text IDs and number IDs.

### Q28 ⭐⭐ 🟡 How do you highlight weekends in an attendance sheet with a date row?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use WEEKDAY inside a rule with a row-locked reference so the rule reads the date header for every row?
**Say this in the interview:** "I select the grid and use `=WEEKDAY(C$1,2)>5`. WEEKDAY with type 2 numbers Monday as 1 and Sunday as 7, so greater than 5 means Saturday or Sunday. The dollar locks the date row."
**Explain simply:**
- *WEEKDAY(date,2)* returns 1 for Monday to 7 for Sunday.
- `C$1` locks row 1 (the date row) but lets the column move, so each column reads its own date.
- Public holidays are not weekends; add a holiday list and test it with COUNTIF in the same rule (shown below).
**Example:** Dates 01-Oct-2026 to 08-Oct-2026: Saturday 03 and Sunday 04 are weekends. If 02-Oct is a company holiday, three columns are shaded.
**Sample sheet:**

Dates in C1:J1 (a holiday date in M1).

|  | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-01 | 2026-10-02 | 2026-10-03 | 2026-10-04 | 2026-10-05 | 2026-10-06 | 2026-10-07 | 2026-10-08 |
| day | Thu | Fri | Sat | Sun | Mon | Tue | Wed | Thu |

**Formula / Steps:** Conditional-formatting dialog: not run here (steps from Microsoft Support, "Use conditional formatting to highlight information in Excel"): select C1:J20 (dates plus employee rows) > Home > Conditional Formatting > New Rule > "Use a formula to determine which cells to format" > `=WEEKDAY(C$1,2)>5` > Format > OK.
**Alternative:** `=OR(WEEKDAY(C$1)=1,WEEKDAY(C$1)=7)` (default type 1: Sunday=1, Saturday=7), or with holidays `=OR(WEEKDAY(C$1,2)>5,COUNTIF($M$1:$M$1,C$1)>0)`, or `=NETWORKDAYS(C$1,C$1,$M$1:$M$1)=0`.
**Result:** Rule formulas run in LibreOffice 24.2 per column (TRUE = shaded):

| Rule | Thu | Fri | Sat | Sun | Mon | Tue | Wed | Thu |
|---|---|---|---|---|---|---|---|---|
| WEEKDAY(,2)>5 | FALSE | FALSE | TRUE | TRUE | FALSE | FALSE | FALSE | FALSE |
| OR(WEEKDAY=1,=7) | FALSE | FALSE | TRUE | TRUE | FALSE | FALSE | FALSE | FALSE |
| NETWORKDAYS=0 (no holiday list) | FALSE | FALSE | TRUE | TRUE | FALSE | FALSE | FALSE | FALSE |
| weekend OR holiday (02-Oct) | FALSE | TRUE | TRUE | TRUE | FALSE | FALSE | FALSE | FALSE |

Colouring itself: not run here.
**Version note:** All versions and Google Sheets. In weekend-different countries use `NETWORKDAYS.INTL` (Excel 2010+, from memory).
**Edge cases:** Dates typed as text (not real dates) make WEEKDAY return #VALUE! and nothing colours. If the header shows only "Mon, Tue" as text labels, the rule cannot work: keep real dates and format them as "ddd". Blank header cells count as date 0 (a Saturday in the 1900 system): add `C$1<>""`.
**Likely follow-ups:** 1) *Colour the header only?* Apply the rule to row 1 only. 2) *Different weekends?* NETWORKDAYS.INTL. 3) *Highlight today?* `=C$1=TODAY()`.
**Common mistakes:** Locking the column (`$C1`) so only the first column is checked; using type 1 and testing `>5`; leaving the date row as text.

### Q29 ⭐⭐ 🟡 What happens when several conditional formatting rules apply to the same cell, and what does Stop If True do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know rule precedence and that Stop If True is mainly a legacy switch?
**Say this in the interview:** "Excel checks rules from the top of the Rules Manager list down. If two rules clash on the same property, such as fill colour, the higher rule wins. Stop If True tells Excel not to look at any rule below that one."
**Explain simply:**
- Rules are evaluated top to bottom; new rules are added at the top (Microsoft Support, Conditional Formatting page).
- If rules do not conflict (one sets fill, another sets bold), both formats show (from memory, unverified on the page I read).
- Stop If True exists for backward compatibility with older Excel and cannot be set for data bars, colour scales or icon sets (Microsoft Support). Google Sheets works differently: the first rule that is true wins (Google Docs Editors Help).
**Example:** Attendance below 75% should be red; below 90% amber. A 62% employee satisfies both rules; because the red rule is higher, the cell is red, not amber.
**Sample sheet:**

Attendance % in B2:B7.

|  | A | B |
|---|---|---|
| 2 | Asha | 0.62 |
| 3 | Ravi | 0.74 |
| 4 | Meena | 0.88 |
| 5 | Karan | 0.93 |
| 6 | Divya | 0.8 |
| 7 | Imran | 0.97 |

**Formula / Steps:** Conditional-formatting dialog: not run here (steps from Microsoft Support, "Use conditional formatting to highlight information in Excel"): Home > Conditional Formatting > Manage Rules > select the rule > Move Up / Move Down to set order > tick "Stop If True" on a rule if wanted > OK. Rule 1 (top, red): `=B2<0.75`. Rule 2 (amber): `=B2<0.9`.
**Alternative:** Write non-overlapping rules so order does not matter: red `=B2<0.75`, amber `=AND(B2>=0.75,B2<0.9)`.
**Result:** Rule formulas run in LibreOffice 24.2; the "Shown" column applies top-to-bottom precedence by my own logic (not run in Excel):

| Row | Name | Attendance | Rule 1 (<0.75) | Rule 2 (<0.9) | Shown |
|---|---|---|---|---|---|
| 2 | Asha | 0.62 | TRUE | TRUE | Red |
| 3 | Ravi | 0.74 | TRUE | TRUE | Red |
| 4 | Meena | 0.88 | FALSE | TRUE | Amber |
| 5 | Karan | 0.93 | FALSE | FALSE | none |
| 6 | Divya | 0.8 | FALSE | TRUE | Amber |
| 7 | Imran | 0.97 | FALSE | FALSE | none |

**Version note:** Behaviour is the same in all desktop versions; Stop If True is not described for Excel for the web in the Microsoft page.
**Edge cases:** Order matters only when formats conflict. Stop If True matters when a lower rule would add a format you do not want. "Applies to" ranges can differ between rules; check the "Show formatting rules for: This Worksheet" list.
**Likely follow-ups:** 1) *Where do I reorder?* Manage Rules arrows. 2) *Does Stop If True speed things up?* Possibly a little; I would not rely on that (unverified). 3) *Why is my new rule not showing?* An older rule above it sets the same fill.
**Common mistakes:** Putting the broad rule (<90%) on top so the red rule never shows; thinking the last rule wins; leaving stray duplicate rules after copy-paste.

### Q30 ⭐⭐ 🟡 What is the difference between Goal Seek and Solver, and when do you need Solver?
**Asked at:** commonly asked; a Goal Seek/Solver scenario-modelling question appears on the Hirist Excel list (Part 9 sources file); no company-specific report found
**What the interviewer is checking:** Do you know Goal Seek handles one input and no limits, whereas Solver handles many inputs with constraints and can maximise or minimise?
**Say this in the interview:** "Goal Seek changes one cell until a formula hits a number I give it. Solver changes many cells, respects rules like 'budget at most 7 lakh', and can find the best possible value, a maximum or minimum."
**Explain simply:**
- Goal Seek works only with one variable input value; Solver is an add-in that "is similar to Goal Seek, but can accommodate more variables" (Microsoft Support, "Use Goal Seek..." and "Introduction to What-If Analysis").
- Solver can adjust up to 200 variable cells and accept constraints (<=, =, >=, int, bin, dif) and set the objective to max, min or a value (Microsoft Support, "Define and solve a problem by using Solver").
- Solver is on Data tab > Analysis group; if missing, enable the add-in (Microsoft Support). It is not supported in Excel for the web.
**Example:** Hiring budget Rs 7,00,000 (Rs 700 thousand). Referral costs Rs 20k per hire (max 15), job portal Rs 30k (max 12), agency Rs 50k (min 3, max 10). Maximise total hires within budget.
**Sample sheet:**

Changing cells B2:B4 = hires from Referral, Portal, Agency; cost B5.

|  | A | B | C (Cost per hire, Rs 000) |
|---|---|---|---|
| 1 | Channel | Hires | Cost |
| 2 | Referral |  | 20 |
| 3 | Portal |  | 30 |
| 4 | Agency |  | 50 |
| 5 | Total hires | =SUM(B2:B4) |  |
| 6 | Total cost | =SUMPRODUCT(B2:B4,C2:C4) |  |

**Formula / Steps:** Solver dialog: not run here (steps from Microsoft Support). 1) Data > Analysis > Solver. 2) Set Objective `B5`, To: Max. 3) By Changing `B2:B4`. 4) Add constraints: `B6<=700`, `B2<=15`, `B3<=12`, `B4>=3`, `B4<=10`, `B2:B4=integer`. 5) Method: Simplex LP / GRG, Solve.
**Alternative:** Goal Seek (Data > What-If Analysis > Goal Seek) can only answer "what single number makes this cell equal X", e.g. the cost per hire that makes total cost exactly 700.
**Result:** Solver: not run here. Reproduced with a Python brute-force over all integer plans: maximum is 26 hires, e.g. 14 referral + 9 portal + 3 agency, costing Rs 700k (Rs 7,00,000). There are 2 optimal plans: [[14, 9, 3], [15, 8, 3]]. Solver may return either one.
**Version note:** Goal Seek is built into all versions; Solver is an add-in in desktop Excel (Microsoft Support, "Define and solve a problem by using Solver", lists 365, 2024, 2021, 2019 and 2016). Google Sheets has a Solver add-on (from memory, unverified).
**Edge cases:** Several plans can tie. Solver may stop at a local best with non-linear models. Without the "integer" constraint, Solver may give fractional hires. Constraints must be on cells, not typed into formulas.
**Likely follow-ups:** 1) *Can Goal Seek do two inputs?* No (Microsoft Support). 2) *Which engine?* Simplex LP for linear, GRG Nonlinear for smooth curves, Evolutionary for rough ones (same Solver page, fetched). 3) *Is the answer saved?* Choose Keep Solver Solution; save a scenario if you want to reuse it.
**Common mistakes:** Forgetting the integer constraint; not enabling the add-in first; expecting Goal Seek to respect limits.

### Q31 ⭐⭐ 🟡 How do you highlight blank cells or rows with missing mandatory fields in a hiring tracker?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you flag incomplete records with a COUNTBLANK or blank test rule, and do you know the trap with formula-blanks ("")?
**Say this in the interview:** "For missing mandatory fields I use a formula rule on the whole data rows: `=AND($A2<>"",COUNTBLANK($B2:$E2)>0)`. If the candidate name exists but any mandatory column is blank, the row is coloured."
**Explain simply:**
- *COUNTBLANK(range)* counts empty cells, including cells that contain a formula returning "" (empty text).
- *ISBLANK(cell)* is TRUE only for truly empty cells, so a formula returning "" fools it.
- The `$A2<>""` part stops completely empty rows below the data from being coloured.
**Example:** Tracker has 5 candidates and one empty row. Ravi has no Source, Meena has no Role or Interview date, Karan has no Recruiter, Divya has a formula that returns "" in Source: 4 rows flagged.
**Sample sheet:**

Mandatory fields B:E.

|  | A Candidate | B Role | C Source | D Interview date | E Recruiter |
|---|---|---|---|---|---|
| 2 | Asha | Analyst | Referral | 12-Oct | Pooja |
| 3 | Ravi | Analyst |  | 14-Oct | Pooja |
| 4 | Meena |  | Portal |  | Rahul |
| 5 | Karan | Manager | Agency | 15-Oct |  |
| 6 | Divya | Analyst | (formula ="") | 16-Oct | Rahul |
| 7 |  |  |  |  |  |

**Formula / Steps:** Conditional-formatting dialog: not run here (steps from Microsoft Support, "Use conditional formatting to highlight information in Excel"): select A2:E500 > Home > Conditional Formatting > New Rule > "Use a formula to determine which cells to format" > `=AND($A2<>"",COUNTBLANK($B2:$E2)>0)` > Format > OK. Single mandatory cell: `=AND($A2<>"",C2="")`.
**Alternative:** Highlight only the blank cells: Home > Conditional Formatting > New Rule > "Format only cells with" > Blanks. Or `=OR($B2="",$C2="",$D2="",$E2="")`.
**Result:** Rule formulas run in LibreOffice 24.2 (TRUE = coloured). Row 7 is empty; Divya's Source is a formula returning "":

| Row | Candidate | Row rule (COUNTBLANK) | ISBLANK(C) | C="" |
|---|---|---|---|---|
| 2 | Asha | FALSE | FALSE | FALSE |
| 3 | Ravi | TRUE | TRUE | TRUE |
| 4 | Meena | TRUE | FALSE | FALSE |
| 5 | Karan | TRUE | FALSE | FALSE |
| 6 | Divya | TRUE | FALSE | TRUE |
| 7 |  | FALSE | TRUE | TRUE |

Note row 6: ISBLANK says FALSE but the cell looks empty; COUNTBLANK and `=""` catch it. Colouring itself: not run here.
**Version note:** All versions and Google Sheets (custom formula; Sheets also has a built-in "Is empty" condition, from memory, unverified).
**Edge cases:** Cells holding only spaces are not blank; use `LEN(TRIM(C2))=0`. A zero is not blank. Colour is only a visual cue; to force entry use data validation or a tracker status check column.
**Likely follow-ups:** 1) *Count incomplete rows?* Put the rule formula in a helper column (G2 `=AND($A2<>"",COUNTBLANK($B2:$E2)>0)`) and count TRUE with COUNTIF. 2) *Make blank cells impossible?* Validation cannot force an entry; use a form. 3) *Highlight in a pivot?* Use "For empty cells show".
**Common mistakes:** Using ISBLANK on formula cells; colouring all empty rows below the data; forgetting the `$` before the column letters.

### Q32 ⭐ 🟢 How do you find and remove invalid data and clear data validation from a range (Circle Invalid Data, Clear All)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know validation only checks new entries, and how to audit data that is already there?
**Say this in the interview:** "Data > Data Validation > Circle Invalid Data draws a red circle round every cell that breaks its rule, even values that were pasted in. To remove the rule itself I open Data Validation and click Clear All."
**Explain simply:**
- Validation rules check typing; values already in the cell or pasted may break the rule without any message.
- *Circle Invalid Data* marks them, including values that were typed, copied or filled, or even calculated by formulas or macros (Microsoft Support, "Display or hide circles around invalid data"). It is available only in desktop Excel.
- *Clear All* removes the rule from the selected cells; the data stays.
**Example:** Age column should be a whole number between 18 and 60. Of 8 entries, 4 are fine; 17, 61, 34.5 and the text "thirty" get circled.
**Sample sheet:**

Ages in A2:A9, rule is whole number 18 to 60.

|  | A (Age) |
|---|---|
| 2 | 25 |
| 3 | 17 |
| 4 | 61 |
| 5 | 34.5 |
| 6 | thirty |
| 7 | 45 |
| 8 | 18 |
| 9 | 60 |

**Formula / Steps:** Dialog: not run here (steps from Microsoft Support). Circle: Data tab > Data Tools group > Data Validation arrow > Circle Invalid Data; clear circles: same arrow > Clear Validation Circles. Remove rule: select cells > Data > Data Validation > Clear All > OK.
**Alternative:** To find cells with validation on a big sheet: Home > Find & Select > Go To Special > Data Validation (from memory, unverified). Or use a helper column with the rule test, shown below, and filter the FALSE rows.
**Result:** Rule test `=IF(ISNUMBER(A2),AND(A2=INT(A2),A2>=18,A2<=60),FALSE)` run in LibreOffice 24.2 (FALSE = would be circled):

| Row | Age | Valid? |
|---|---|---|
| 2 | 25 | TRUE |
| 3 | 17 | FALSE |
| 4 | 61 | FALSE |
| 5 | 34.5 | FALSE |
| 6 | thirty | FALSE |
| 7 | 45 | TRUE |
| 8 | 18 | TRUE |
| 9 | 60 | TRUE |

The circles themselves: not run here.
**Version note:** Circle Invalid Data is a desktop Excel feature; Microsoft says in Excel for the web "you may not see this feature" (Microsoft Support, "Display or hide circles around invalid data", seen in search results, page not opened); and I know of no direct Google Sheets equivalent (from memory, unverified).
**Edge cases:** Circles disappear when the cell is corrected or when you click Clear Validation Circles; they do not save as a filter. Blank cells are not circled if "Ignore blank" is ticked.
**Likely follow-ups:** 1) *Does it fix the data?* No, it only marks it. 2) *Remove validation but keep the values?* Clear All. 3) *Remove validation from the whole sheet?* Select all then Clear All.
**Common mistakes:** Expecting validation to flag existing data; using Delete on the cell (clears the value, not the rule); not realising Clear All also removes the drop-down.

### Q33 ⭐ 🟢 How do you copy conditional formatting or data validation from one range to another?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know Format Painter and Paste Special options and how relative references adjust?
**Say this in the interview:** "For conditional formatting I use Format Painter. For data validation I copy the cell and use Paste Special > Validation, so the values underneath stay untouched."
**Explain simply:**
- *Format Painter* (Home > Clipboard) copies conditional formatting ("use Format Painter to copy the conditional formatting", Microsoft Support, Conditional Formatting page, fetched); double-click it to paste to several places.
- Pasting changes the rule's "Applies to" range, and relative references shift with it, so `$B2` becomes `$B12` when the range starts at row 12.
- Paste Special > Validation copies only the rule (from memory, unverified).
**Example:** Attendance table 1 has the rule "below 90%". You paste it to table 2 further down and it keeps working, flagging 88% and 60%.
**Sample sheet:**

Table 1 in A2:C5 with rule `=$B2<0.9`; table 2 in A12:B15.

|  | A | B |
|---|---|---|
| 2 | Asha | 0.95 |
| 3 | Ravi | 0.82 |
| 4 | Meena | 0.9 |
| 5 | Karan | 0.71 |
| 12 | Divya | 0.88 |
| 13 | Imran | 0.97 |
| 14 | Neha | 0.6 |
| 15 | Arjun | 0.91 |

**Formula / Steps:** Not run here (steps from Microsoft Support, Conditional Formatting page, plus memory for validation). CF: select a formatted cell > Home > Format Painter > drag over the target range (Esc to stop). Validation: copy the source cell > select target > Home > Paste > Paste Special > Validation > OK.
**Alternative:** Edit "Applies to" in Manage Rules to extend the rule (`=$A$2:$B$15`) instead of copying. Or drag the fill handle.
**Result:** Rule `=$B12<0.9` as Excel would rewrite it for the pasted range, run in LibreOffice (TRUE = coloured):

| Row | Name | Pct | Rule shifted to this row |
|---|---|---|---|
| 12 | Divya | 0.88 | TRUE |
| 13 | Imran | 0.97 | FALSE |
| 14 | Neha | 0.6 | TRUE |
| 15 | Arjun | 0.91 | FALSE |

Wrong version that keeps the old row `=$B2<0.9` inside table 2:

| Row | Name | Pct | Old row rule (reads row-10 value) |
|---|---|---|---|
| 12 | Divya | 0.88 | FALSE |
| 13 | Imran | 0.97 | TRUE |
| 14 | Neha | 0.6 | FALSE |
| 15 | Arjun | 0.91 | TRUE |

The painting itself: not run here.
**Version note:** Format Painter and Paste Special exist in all versions. Microsoft's page says pasting cells with conditional formats creates a new rule for the destination cells. Google Sheets: Paste special > Conditional formatting only / Data validation only (from memory, unverified).
**Edge cases:** Format Painter also copies fonts and borders. Data validation pasted over a cell with a formula does not change the value. Rules that reference other workbooks cannot exist (Microsoft Support).
**Likely follow-ups:** 1) *Copy only the rule, not the colour?* Not possible in Format Painter; use Paste Special > Validation for validation. 2) *Many rules got duplicated?* Open Manage Rules and clean up. 3) *Does Fill Down copy CF?* Yes, formats copy with fill (from memory).
**Common mistakes:** Using normal paste (overwrites values); pasting from a different workbook and expecting the rule to follow; leaving stale "Applies to" fragments.

### Q34 ⭐ 🟢 How do you create a drop-down list whose source list is on another sheet?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a list can live on another sheet and that a named range or a table keeps it tidy?
**Say this in the interview:** "I keep the list on a Lists sheet. In Data Validation I choose List and point the source to it, like `=Lists!$A$2:$A$6`, or better a named range so it is easier to read."
**Explain simply:**
- *Data Validation > List* gives a drop-down where the choices come from a range or a typed list.
- In current Excel you can click the other sheet while setting the source; older versions needed a named range (from memory, unverified).
- Putting the list in an Excel Table makes the drop-down update automatically when items are added (Microsoft Support, "Create a drop-down list"). Hide and protect that sheet to stop edits (same page).
**Example:** Employee department drop-down uses a Lists sheet with Sales, HR, Finance, IT, Operations. HR picks a department from the list instead of typing; "Finanse" would be rejected.
**Sample sheet:**

Sheet Lists, A2:A6; entry sheet column A (Department).

|  | Lists!A |
|---|---|
| 2 | Sales |
| 3 | HR |
| 4 | Finance |
| 5 | IT |
| 6 | Operations |

**Formula / Steps:** Dialog: not run here (steps from Microsoft Support). 1) Select the target cells. 2) Data tab > Data Tools > Data Validation. 3) Settings > Allow: List. 4) Source: `=Lists!$A$2:$A$6` (or a name like `=DeptList`). 5) Keep "In-cell dropdown" ticked > OK.
**Alternative:** Name the range: Formulas > Define Name > `DeptList`, source `=DeptList`. Or `=INDIRECT("Lists!A2:A6")`, which breaks if the sheet is renamed.
**Result:** The validity test behind a list, run in LibreOffice 24.2 against Lists!A2:A6 (TRUE = would be accepted):

| Row | Entry | Match in list (COUNTIF) | Exact-case match |
|---|---|---|---|
| 2 | 'Sales' | TRUE | TRUE |
| 3 | 'sales' | TRUE | FALSE |
| 4 | 'Finanse' | FALSE | FALSE |
| 5 | 'IT' | TRUE | TRUE |
| 6 | 'HR ' | FALSE | FALSE |
| 7 | 'Operations' | TRUE | TRUE |

The drop-down itself: not run here.
**Version note:** Works in Excel 2016 to 365 (the drop-down page lists 365, 2024, 2021, 2019, 2016). Google Sheets: Data > Data validation > Dropdown (from a range) (Google Docs Editors Help).
**Edge cases:** If the source range has blanks, users can type blanks unless "Ignore blank" is off. For a typed list (`Yes,No`) validation is case-sensitive, for a range source it is not (from memory, unverified): "sales" passes against the range test above. Trailing spaces ("HR ") fail. If the Lists sheet is deleted, the source becomes #REF!.
**Likely follow-ups:** 1) *Source on another workbook?* Not reliable; use a named range with the workbook open. 2) *Auto-grow list?* Use an Excel Table (Q22). 3) *Hide the list?* Hide and protect the sheet.
**Common mistakes:** Typing the list without `=`; relative addresses (`Lists!A2:A6`) that shift when copied; deleting the list sheet.

### Q35 ⭐ 🟡 How do you restrict an entry to exactly 10 digits (for example, a mobile number) using data validation?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know Text Length versus a custom formula, and why Text Length alone lets letters through?
**Say this in the interview:** "Text Length equal to 10 is quick but it lets in letters. For a strict rule I use a Custom formula that checks length 10 and that all ten characters are digits."
**Explain simply:**
- Data Validation has a *Text Length* type for limits on characters (Microsoft Support, "Apply data validation to cells").
- Text Length = 10 accepts "98765abc10" because it counts characters only.
- The custom formula counts digit characters: it removes each digit 0-9 in turn and adds up what was removed.
- Store mobile numbers as Text format (Home > Number Format > Text) if numbers may begin with 0; Excel drops leading zeros in numbers.
**Example:** Mobile column for 7 entries. "9876543210" (twice) and "8123456789" pass; "98765 43210", "987654321", "98765abc10" and "09876543210" fail.
**Sample sheet:**

Mobile numbers in A2:A8 (A2, A6, A8 stored as numbers; others as text).

|  | A (Mobile) |
|---|---|
| 2 | 9876543210 |
| 3 | 98765 43210 |
| 4 | 987654321 |
| 5 | 98765abc10 |
| 6 | 8123456789 |
| 7 | 09876543210 |
| 8 | 9876543210 |

**Formula / Steps:** Dialog: not run here (steps from Microsoft Support). Select A2:A8 > Data > Data Validation > Settings > Allow: Custom > Formula `=AND(LEN(A2)=10,SUMPRODUCT(LEN(A2)-LEN(SUBSTITUTE(A2,{0,1,2,3,4,5,6,7,8,9},"")))=10)` > Error Alert tab: Style Stop, message "Enter 10 digits only" > OK. Add `,ISNUMBER(MATCH(LEFT(A2,1),{"6","7","8","9"},0))` for Indian mobile numbers starting with 6-9 (assumption, not from a source).
**Alternative:** Simple route: Allow: Text length > equal to > 10, which does not block letters.
**Result:** Rule formulas run in LibreOffice 24.2 (TRUE = accepted):

| Row | Entry | Text length = 10 | Digits-only custom | Custom + starts 6-9 |
|---|---|---|---|---|
| 2 | 9876543210 | TRUE | TRUE | TRUE |
| 3 | 98765 43210 | FALSE | FALSE | FALSE |
| 4 | 987654321 | FALSE | FALSE | FALSE |
| 5 | 98765abc10 | TRUE | FALSE | FALSE |
| 6 | 8123456789 | TRUE | TRUE | TRUE |
| 7 | 09876543210 | FALSE | FALSE | FALSE |
| 8 | 9876543210 | TRUE | TRUE | TRUE |

The dialog: not run here.
**Version note:** Works in Excel 2016 to 365 and Google Sheets (Sheets custom formula, array constants support from memory, unverified).
**Edge cases:** Pasting bypasses validation (Q40). Numbers formatted as text and real numbers both pass LEN. Spaces or hyphens ("98765-43210") fail the digit count. 11-digit numbers with +91 or 0 prefix fail by design. A number larger than 15 digits loses precision in Excel: not relevant to 10 digits.
**Likely follow-ups:** 1) *Use Whole number instead?* `between 6000000000 and 9999999999` blocks letters but breaks leading zeros; fine for Indian mobiles. 2) *Allow spaces?* Strip with SUBSTITUTE in the formula. 3) *Why not regex?* Excel has none in formulas.
**Common mistakes:** Choosing Text Length only; writing the formula for the wrong first cell; a custom rule with a fully locked `$A$2`.

### Q36 ⭐ 🟡 What are the limitations of Goal Seek, and why might it say it may not have found a solution?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand Goal Seek is an iterative search that can fail or return an approximate answer?
**Say this in the interview:** "Goal Seek only changes one cell, needs that cell to be a typed value that drives the formula, and searches by trial and error. If there is no answer, or it starts in a bad place, it reports that it may not have found a solution."
**Explain simply:**
- Goal Seek works only with one variable input value (Microsoft Support, "Use Goal Seek...").
- The formula in the Set cell must depend on the By-changing cell (Microsoft Support). The changing cell must hold a value, not a formula (from memory, unverified).
- It is *iterative*: it tries values, checks the result and adjusts, stopping when close enough (Excel's limits, 100 iterations and 0.001 maximum change, are from memory, unverified).
- It finds one answer even when there are several, and depends on the starting value.
**Example:** Set cell = x squared. Target 25: starting from 3 it finds 5; starting from -3 it finds -5. Target -4: no real input exists, so Excel cannot find a solution.
**Sample sheet:**

Set cell B2 `=B1^2`, changing cell B1.

|  | A | B |
|---|---|---|
| 1 | x (changing) | 3 |
| 2 | x squared (Set cell) | =B1^2 |

**Formula / Steps:** Not run here (Goal Seek dialog; steps from Microsoft Support): Data > What-If Analysis > Goal Seek > Set cell `B2` > To value `25` > By changing cell `B1` > OK. If the result is not acceptable, click Cancel, change the start value, try again.
**Alternative:** For more inputs, limits or best/worst answers use Solver (Q30). For a closed form, solve the equation algebraically.
**Result:** Not run here (my Python Newton-style illustration, not Excel's exact algorithm): target 25 gives 5.0 from start 3 and -5.0 from start -3. Target -4 for x squared has no real solution: x squared is never below 0, so the gap to -4 can never be less than 4 and no search can close it (by hand; I did not simulate Excel's stopping point). The 5.0 / -5.0 figures were re-run with a simple Newton loop.
**Version note:** Goal Seek exists in all desktop Excel versions (Microsoft Support page "Introduction to What-If Analysis" lists 365, 2024, 2021). Google Sheets has no built-in Goal Seek; there is a Goal Seek add-on (from memory, unverified).
**Edge cases:** It stops once within tolerance, so you may see 24.9996 instead of 25. Flat, jumpy (IF-based) or discontinuous formulas confuse it. Results are not updated if inputs change later (Goal Seek is a one-off). Ranges with errors in the chain stop it.
**Likely follow-ups:** 1) *Why different answers on repeat?* Different start values. 2) *Can it keep a limit like units >= 0?* No, use Solver. 3) *Can a macro run it?* Yes, Range.GoalSeek in VBA (from memory).
**Common mistakes:** Setting the By-changing cell to a formula; typing a number in the Set cell box instead of a cell address; assuming the answer is exact or unique.

### Q37 ⭐ 🟡 Why does a data table sometimes not recalculate, and what does "Automatic except for data tables" mean?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the calculation mode and how to refresh a stale data table?
**Say this in the interview:** "If calculation is set to Automatic except for data tables, normal formulas update but data tables wait. I press F9 to refresh, or switch the calculation option back to Automatic."
**Explain simply:**
- A *data table* (Data > What-If Analysis > Data Table) fills a grid with results of a formula for many input values (Microsoft Support, "Calculate multiple results by using a data table").
- Data tables can be slow in big workbooks, so Excel lets you recalculate them manually. The setting named "Automatic except for data tables" is from memory (unverified wording); the page I fetched only says to set Automatic in File > Options > Formulas > Calculation options and press F9 to recalculate a data table.
- In Manual mode nothing recalculates until you press F9.
**Example:** Loan EMI table for Rs 5,00,000 over 60 months at 8%-12%. Someone changes the loan to Rs 6,00,000; the table keeps old EMIs until F9, so 8% still shows 10,138 instead of 12,166.
**Sample sheet:**

Rates in A2:A6, EMI for the current loan in B.

|  | A (Rate) | B (EMI, Rs 5,00,000) |
|---|---|---|
| 2 | 0.08 | 10138 |
| 3 | 0.09 | 10379 |
| 4 | 0.1 | 10624 |
| 5 | 0.11 | 10871 |
| 6 | 0.12 | 11122 |

**Formula / Steps:** Dialog: not run here (steps from Microsoft Support). Check: File > Options > Formulas > Calculation options > choose Automatic (or Formulas tab > Calculation Options). Refresh a stale table: select it and press F9, or Formulas > Calculate Now.
**Alternative:** Keep the speed benefit but refresh when needed: leave the "except data tables" mode and press F9 before sharing. Or replace the data table with direct formulas.
**Result:** EMI formula `=ROUND(-PMT(A2/12,60,500000),0)` run in LibreOffice 24.2 for both loan amounts:

| Rate | EMI at Rs 5,00,000 (stale table) | EMI at Rs 6,00,000 (fresh) |
|---|---|---|
| 8% | 10138 | 12166 |
| 9% | 10379 | 12455 |
| 10% | 10624 | 12748 |
| 11% | 10871 | 13045 |
| 12% | 11122 | 13347 |

The Excel data table and its mode setting: not run here.
**Version note:** Data tables and calculation options exist in all desktop versions. Google Sheets has no Data Table feature (from memory, unverified).
**Edge cases:** The row and column input cells must be on the same sheet as the table (from memory). Manual mode also freezes every other formula. Opening a file saved with a different mode can change your mode.
**Likely follow-ups:** 1) *Why is every cell the same?* Wrong input cell references. 2) *Can I edit one cell inside?* No, it is a single array result. 3) *Does F9 recalc the whole workbook?* Yes in Manual mode.
**Common mistakes:** Assuming "Automatic" includes tables; changing inputs and not pressing F9; pointing the input cell at a cell that does not drive the formula.

### Q38 ⭐ 🟡 How do you apply conditional formatting and a drop-down list in Google Sheets, and how do they differ from Excel?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the Sheets menus and the main differences, especially rule order and multiple selections?
**Say this in the interview:** "In Sheets, Format > Conditional formatting opens a side panel; for rows I choose Custom formula. A drop-down comes from Insert > Dropdown or Data > Data validation. Differences: Sheets stops at the first true rule, and drop-downs can allow multiple selections as chips."
**Explain simply:**
- Conditional formatting: select cells > Format > Conditional formatting; under "Format cells if" choose "Custom formula is" and enter a formula for the first cell with dollar signs (Google Docs Editors Help, "Use conditional formatting rules in Google Sheets").
- Rules are evaluated in the order listed and the first true rule sets the format (same page); in Excel several true rules can combine.
- Drop-down: Insert > Dropdown, or Data > Data validation > Add rule > Dropdown from a range, or right-click > Dropdown (Google Docs Editors Help, "Create an in-cell dropdown list", fetched; the same page says unmatched entries are rejected by default, or you can set "Show a warning").
- A custom formula that points to another sheet needs INDIRECT in Sheets ("To reference another sheet in the formula, use the INDIRECT function", "Use conditional formatting rules in Google Sheets", fetched).
- *Chip format* means each choice shows as a small coloured label inside the cell. Only chip-format drop-downs can allow several choices in one cell, so Sheets now has native multi-select where Excel does not.
**Example:** Highlight resigned employees: select A2:E50, custom formula `=$D2="Resigned"`. Add a Status drop-down with Active, Resigned.
**Sample sheet:**

Status in column D.

|  | A (Employee) | D (Status) |
|---|---|---|
| 2 | Asha | Active |
| 3 | Ravi | Resigned |
| 4 | Meena | Active |
| 5 | Karan | Resigned |
| 6 | Divya | Active |

**Formula / Steps:** Not run here (steps from Google Docs Editors Help). CF: select range > Format > Conditional formatting > Format cells if > Custom formula is > `=$D2="Resigned"` > choose colour > Done. Drop-down: select cells > Insert > Dropdown > add options > Done.
**Alternative:** Excel steps for comparison: Home > Conditional Formatting > New Rule > "Use a formula..."; Data > Data Validation > List (Q3).
**Result:** The rule formula is the same in Excel and Sheets; run in LibreOffice 24.2 (TRUE = coloured):

| Row | Employee | Status | Rule |
|---|---|---|---|
| 2 | Asha | Active | FALSE |
| 3 | Ravi | Resigned | TRUE |
| 4 | Meena | Active | FALSE |
| 5 | Karan | Resigned | TRUE |
| 6 | Divya | Active | FALSE |

The Sheets panel: not run here.
**Version note:** Sheets multi-select: "Allow multiple selections" can only be enabled for chip format dropdowns, and on mobile "you currently can't select multiple dropdown options even when multiple selection is enabled" (Google Docs Editors Help, "Create an in-cell dropdown list", fetched 2026-10-22). Excel has no built-in multi-select that I could find (Microsoft's "Create a drop-down list" page, fetched, does not mention multiple selection; unverified beyond that). Excel 2016 to 365 all have CF and validation (the drop-down page lists 2016-365).
**Edge cases:** Sheets applies rules by order (first true wins); Excel applies all true rules unless Stop If True. Excel conditional formatting can read another worksheet of the same workbook directly (Microsoft Support CF page, fetched). Sheets data validation can reject or just warn (from memory).
**Likely follow-ups:** 1) *Colour scale in Sheets?* Yes: Color scale tab. 2) *Drop-down from another sheet?* Choose range on other sheet. 3) *Does validation stop pasting?* No in either (Q40).
**Common mistakes:** Writing the formula for the wrong first cell; forgetting dollar signs; pasting from Excel and expecting the same rule order.

### Q39 ⭐ 🟡 How do you shade alternate rows (banded rows) with conditional formatting so the banding survives sorting and filtering?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know why `MOD(ROW(),2)` breaks after filtering and what to use instead?
**Say this in the interview:** "MOD(ROW(),2)=0 looks at the sheet row number, so after a filter the visible rows are no longer alternate. I count only visible rows with SUBTOTAL(103,...) and use that count inside MOD, so the stripes stay even."
**Explain simply:**
- `MOD(ROW(),2)=0` colours even sheet rows; sorting is fine (colour follows the row number, not the person) but filtering hides rows and leaves uneven stripes.
- `SUBTOTAL(103,$A$2:$A2)` counts visible non-blank cells from A2 down to this row; `103` is the COUNTA version that ignores hidden rows.
- An Excel Table with "Banded Rows" ticked also re-bands after sorting and filtering (from memory, unverified); this answer is for plain ranges.
**Example:** Employee list of 8; rows 3 and 5 are filtered out. With ROW(), the visible stripes read shaded, shaded, shaded, plain, shaded, plain. With the SUBTOTAL rule they read plain, shaded, plain, shaded, plain, shaded.
**Sample sheet:**

Names in A2:A9.

|  | A |
|---|---|
| 2 | Asha |
| 3 | Ravi |
| 4 | Meena |
| 5 | Karan |
| 6 | Divya |
| 7 | Imran |
| 8 | Sneha |
| 9 | Vikram |

Rows 3 and 5 hidden.

**Formula / Steps:** Conditional-formatting dialog: not run here (steps from Microsoft Support, "Use conditional formatting to highlight information in Excel"): select A2:A9 (or the whole data width, e.g. A2:H500) > Home > Conditional Formatting > New Rule > "Use a formula..." > `=MOD(SUBTOTAL(103,$A$2:$A2),2)=0` > Format > OK.
**Alternative:** Simple route (breaks on filtering): `=MOD(ROW(),2)=0`. Table route: Table Design > Banded Rows.
**Result:** Rule formulas run in LibreOffice 24.2 with rows 3 and 5 hidden by the hidden-row setting (not a real AutoFilter). Showing only visible rows (TRUE = shaded):

| Row | Name | ROW() rule | SUBTOTAL rule |
|---|---|---|---|
| 2 | Asha | TRUE | FALSE |
| 4 | Meena | TRUE | TRUE |
| 6 | Divya | TRUE | FALSE |
| 7 | Imran | FALSE | TRUE |
| 8 | Sneha | TRUE | FALSE |
| 9 | Vikram | FALSE | TRUE |

The SUBTOTAL column alternates FALSE/TRUE as wanted; the ROW() column does not. Behaviour in real Excel AutoFilter: not run here (from Microsoft documentation/memory).
**Version note:** Works in all desktop versions (from memory, unverified). Google Sheets has Format > Alternating colors for simple banding (from memory, unverified).
**Edge cases:** Reference column ($A) must be a column that is never blank, else rows are skipped in the count. Slow on very long sheets because the range grows per row (see Q44). Manually hidden rows are ignored by 103; rows hidden via grouping also.
**Likely follow-ups:** 1) *Why 103 not 3?* 3 counts hidden rows too. 2) *Banding after sort?* The rule follows positions, so yes. 3) *Excel Table?* Banded Rows is simpler.
**Common mistakes:** Using ROW() on filtered data; locking the range end (`$A$2:$A$2`) so every row counts one; using a column with blanks.

### Q40 ⭐ 🟡 Can data validation be bypassed, and how can you make it more reliable?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know validation only guards typing, and what extra controls exist?
**Say this in the interview:** "Yes. Pasting, fill, formulas, macros and Clear All can all put wrong data past it. I add Circle Invalid Data audits, a check column, and sheet protection, and I keep rules in tables so they copy down."
**Explain simply:**
- Validation checks only what is typed into the cell. Circle Invalid Data catches values that were typed, copied, filled, calculated or entered by macros (Microsoft Support, "Display or hide circles around invalid data").
- Pasting from another cell replaces both the value and the rule if you use normal paste (from memory, unverified); Paste Special > Values keeps the rule.
- Validation commands are not available on protected sheets or shared workbooks (Microsoft Support, "Apply data validation to cells"), so protecting the sheet stops users from changing the rules (assumption to confirm in your Excel).
- Add a visible check: a helper column that returns TRUE/FALSE using the same rule.
**Example:** Employee ID column must be unique. Someone pastes seven IDs: E102 and E103 are repeated and nothing stops it. The audit column flags rows E102 (x2) and E103 (x3).
**Sample sheet:**

Employee IDs in A2:A8 (pasted).

|  | A (Employee ID) |
|---|---|
| 2 | E101 |
| 3 | E102 |
| 4 | E103 |
| 5 | E102 |
| 6 | E105 |
| 7 | E103 |
| 8 | E103 |

**Formula / Steps:** Dialog: not run here (steps from Microsoft Support). Safer setup: 1) Data > Data Validation > Custom `=COUNTIF($A$2:$A$500,A2)=1` (enter for the first cell, then copy; Microsoft Support). 2) Check column `=COUNTIF($A$2:$A$500,A2)=1`. 3) Data > Data Validation arrow > Circle Invalid Data. 4) Review > Protect Sheet.
**Alternative:** Use Excel Tables, forms (Microsoft Forms), or Power Query checks, or a macro that re-checks on change.
**Result:** Audit rule `=COUNTIF($A$2:$A$8,A2)=1` run in LibreOffice 24.2 (FALSE = would be circled):

| Row | ID | Unique? |
|---|---|---|
| 2 | E101 | TRUE |
| 3 | E102 | FALSE |
| 4 | E103 | FALSE |
| 5 | E102 | FALSE |
| 6 | E105 | TRUE |
| 7 | E103 | FALSE |
| 8 | E103 | FALSE |

Paste bypass behaviour: not run here.
**Version note:** Same in all versions; Circle Invalid Data is desktop only (Microsoft Support). Google Sheets validation can also be bypassed by paste (from memory, unverified; ICAEW article noted in the sources file was not read in full).
**Edge cases:** Custom rules referencing other sheets work in current Excel (from memory). "Ignore blank" lets blanks through. Hidden rows with bad data still count in COUNTIF. VBA changes never trigger validation.
**Likely follow-ups:** 1) *Can validation be hidden?* The rule is not visible but can be found via Go To Special > Data Validation. 2) *Block pasting?* Only with VBA or locked cells. 3) *Is Stop style enough?* Only for typed entries.
**Common mistakes:** Believing pasted data is checked; relying on colour alone; applying a custom rule to row 2 and not copying it down.

### Q41 ⭐ 🟡 Your drop-down arrow is not showing in a cell. What are the common reasons?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you troubleshoot systematically, starting with the In-cell dropdown tick?
**Say this in the interview:** "First I check that the cell is selected, then Data > Data Validation: is the type List and is In-cell dropdown ticked? Then the source range, sheet protection and whether the validation was overwritten by a paste."
**Explain simply:**
- The arrow shows only when the cell is selected (from memory, unverified).
- "Make sure that the In-cell dropdown check box is selected. Otherwise, you won't see the drop-down arrow" (Microsoft Support, "Apply data validation to cells").
- The validation command can be unavailable when the sheet is protected or the workbook is shared (same page).
- Another common cause: the validation was removed or replaced when someone pasted over the cell (from memory).
**Example:** An HR tracker used to show a Status drop-down. After an intern pasted Status values from another file, 12 cells lost their arrow because the paste replaced the validation. Reapplying validation fixed it.
**Formula / Steps:** Not run here (steps from Microsoft Support). Checklist: 1) Click the cell. 2) Data > Data Validation: Allow must be List. 3) Tick In-cell dropdown. 4) Check the Source: range exists, no #REF!, delimiters use commas or semicolons per your regional setting (from memory). 5) Review > Unprotect Sheet; Review > Share Workbook off. 6) Data > Data Validation arrow > Circle Invalid Data to see if rules exist.
**Alternative:** Home > Find & Select > Go To Special > Data Validation to find every cell with a rule (from memory, unverified). Reapply by copying a good cell and Paste Special > Validation.
**Version note:** Applies to Excel 2016 to 365 (the Microsoft drop-down page lists 365, 2024, 2021, 2019, 2016). Excel for the web: from memory, unverified.
**Edge cases:** Zoom or a very narrow column can make the arrow look missing. Source list that is empty gives a drop-down with nothing. Merged cells and shapes covering the cell can hide it (from memory).
**Likely follow-ups:** 1) *Arrow shows but list empty?* Source range blank or filtered. 2) *Can users type values not in list?* Yes if error alert is Warning/Information. 3) *Hide the arrow on purpose?* Untick In-cell dropdown.
**Common mistakes:** Assuming the file is broken; re-creating the list instead of checking In-cell dropdown; forgetting that Paste removes validation.

### Q42 ⭐ 🟡 Why does the Scenario Summary report not update when you change an input, and how do you refresh it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the summary is a static snapshot, not a live formula?
**Say this in the interview:** "The Scenario Summary is a snapshot created on a new sheet. It does not recalculate, so after changing an input I delete the old summary sheet and create a new one."
**Explain simply:**
- "Scenario reports don't automatically recalculate" (Microsoft Support, "Switch between various sets of values by using scenarios"). Changes appear only in a new report.
- The report lists the saved scenarios and, in the Current Values column, the values at the time it was created.
- If you change a scenario, use Edit in Scenario Manager first, then rebuild the report.
**Example:** Base case price 450, units 1,000, unit cost 300, fixed 1,20,000 gives profit Rs 30,000 in the summary. You change price to 480; the sheet now gives Rs 60,000 but the summary still says 30,000.
**Sample sheet:**

Inputs B1:B4, profit B6.

|  | A | B |
|---|---|---|
| 1 | Price | 450 |
| 2 | Units | 1000 |
| 3 | Unit cost | 300 |
| 4 | Fixed cost | 120000 |
| 5 |  |  |
| 6 | Profit | =B2*(B1-B3)-B4 |

**Formula / Steps:** Not run here (steps from Microsoft Support). 1) Data > What-If Analysis > Scenario Manager > Edit the scenario if its values changed. 2) Delete the old "Scenario Summary" sheet. 3) Scenario Manager > Summary > Scenario summary > Result cells `B6` > OK.
**Alternative:** Avoid the static summary: build a small comparison table with formulas for each case (Q26), which updates on its own.
**Result:** Profit formula run in LibreOffice 24.2: with price 450 the formula returns 30000; with price 480 it returns 60000. The summary shows 30000 until recreated (by Microsoft documentation). Scenario Manager itself: not run here.
**Version note:** Same in all desktop versions (Microsoft Support page covers 365 and the others from memory).
**Edge cases:** A PivotTable-style summary also needs refreshing (from memory). Result cells in the summary must be re-selected each time. Old summaries pile up as sheets named "Scenario Summary 2".
**Likely follow-ups:** 1) *Can the report be formula-driven?* No. 2) *Where does it appear?* A new sheet. 3) *Alternative?* Data table or manual table.
**Common mistakes:** Editing numbers inside the old summary; forgetting to include the result cell; leaving old summaries in the file.

### Q43 ⭐ 🟡 How do you build a traffic-light attrition indicator with Icon Sets, and how do you show only the icon without the number?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you set thresholds and reverse the icon order, since high attrition is bad?
**Say this in the interview:** "Home > Conditional Formatting > Icon Sets > 3 Traffic Lights. Then Manage Rules > Edit Rule: I set red when attrition is 15% or more, yellow from 10%, and use Reverse Icon Order because a higher number is worse. I tick Show Icon Only to hide the figure."
**Explain simply:**
- *Icon sets* mark each cell with an icon for the range its value falls in (Microsoft Support, "Use data bars, color scales, and icon sets to highlight data").
- By default the first icon (green) is for the highest values. For attrition the highest is bad, so reverse the order or set the thresholds yourself.
- The page I read gives a 67%/33% example but does not state defaults, so I set explicit thresholds with Type = Number.
- Show Icon Only: "To show only the icon and not the value in the cell, select Show Icon Only"; Reverse Icon Order: "To make the first icon represent lower values and the last icon represent higher values, select Reverse Icon Order" (both Microsoft Support, "Use conditional formatting to highlight information in Excel", fetched).
**Example:** Attrition by department: Sales 8% green, Support 12% yellow, Ops 18% red, Finance 5% green, IT 15% red, Admin 9.5% green.
**Sample sheet:**

Attrition in B2:B7.

|  | A (Department) | B (Attrition) |
|---|---|---|
| 2 | Sales | 0.08 |
| 3 | Support | 0.12 |
| 4 | Ops | 0.18 |
| 5 | Finance | 0.05 |
| 6 | IT | 0.15 |
| 7 | Admin | 0.095 |

**Formula / Steps:** Not run here (steps from Microsoft Support plus memory). 1) Select B2:B7 > Home > Conditional Formatting > Icon Sets > 3 Traffic Lights (Unrounded). 2) Manage Rules > Edit Rule. 3) Icon Style 3 Traffic Lights; tick Reverse Icon Order. 4) Set Type Number: red icon "when value is >= 0.15", yellow ">= 0.1" (typed as 0.15 and 0.1). 5) Tick Show Icon Only > OK.
**Alternative:** Hide the number with a custom number format `;;;` instead (Format Cells > Custom), keeping the icon.
**Result:** Threshold logic run in LibreOffice 24.2:

| Row | Department | Attrition | Light |
|---|---|---|---|
| 2 | Sales | 0.08 | Green |
| 3 | Support | 0.12 | Yellow |
| 4 | Ops | 0.18 | Red |
| 5 | Finance | 0.05 | Green |
| 6 | IT | 0.15 | Red |
| 7 | Admin | 0.095 | Green |

The icons: not run here.
**Version note:** Icon Sets exist from Excel 2007 (from memory). Google Sheets has no icon sets (from memory, unverified); use colour or emoji with IF.
**Edge cases:** Percent cells use decimal values 0.15, not 15, if Type is Number. A value exactly at the threshold takes the higher icon (">=", Microsoft Support example).
**Likely follow-ups:** 1) *Colour the whole cell instead?* Use three formula rules. 2) *Change cut-offs?* Edit Rule. 3) *Does Show Icon Only change the value?* No.
**Common mistakes:** Leaving the default order; using percent numbers like 15; hiding the number with white font (still readable).

### Q44 ⭐ 🟡 Can too many conditional formatting rules slow a workbook down, and how do you keep them efficient?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know what makes rules heavy and the habits that keep them light?
**Say this in the interview:** "Yes, especially rules on whole columns, many duplicated rules, or heavy formulas such as COUNTIF over a big range for every cell. I apply rules to exact ranges, clean duplicates in Manage Rules, avoid volatile functions, and use helper columns."
**Explain simply:**
- Every rule is re-evaluated for each cell it covers whenever the sheet recalculates, so cost grows with rules x cells (from memory; not measured here).
- Copy and paste creates many duplicate rules with fragmented "Applies to" ranges: check Manage Rules > Show formatting rules for: This Worksheet.
- *Volatile* functions (TODAY, OFFSET, INDIRECT) recalculate on every change.
- A duplicate check using COUNTIF over the whole column for each cell is slow; a helper column computes the count once per row.
**Example:** A 50,000-row employee sheet has a duplicate rule on whole column A (1,048,576 cells). Limiting it to A2:A50001 and using a helper column keeps the sheet responsive. (Speed gain not measured here.)
**Formula / Steps:** Not run here (steps from Microsoft Support, Manage Rules). Clean up: Home > Conditional Formatting > Manage Rules > Show formatting rules for This Worksheet > delete duplicates and merge ranges > edit "Applies to" to exact ranges. Clear stray rules: Clear Rules from Entire Sheet, then rebuild.
**Alternative:** Helper column: C2 `=COUNTIF($A$2:$A$8,A2)`, rule `=$C2>1`. Avoid whole-column rules (`$A:$A`) unless needed.
**Result:** The same duplicate answer by different formulas, run in LibreOffice 24.2 (TRUE = flagged):

| Row | ID | COUNTIF per cell | Helper count C | Rule `$C>1` | Expanding range (2nd+ only) |
|---|---|---|---|---|---|
| 2 | E101 | FALSE | 1 | FALSE | FALSE |
| 3 | E102 | TRUE | 2 | TRUE | FALSE |
| 4 | E103 | TRUE | 3 | TRUE | FALSE |
| 5 | E102 | TRUE | 2 | TRUE | TRUE |
| 6 | E105 | FALSE | 1 | FALSE | FALSE |
| 7 | E103 | TRUE | 3 | TRUE | TRUE |
| 8 | E103 | TRUE | 3 | TRUE | TRUE |

All give the same flags. Timing differences: not measured here.
**Version note:** No version limit that I know of (from memory, unverified).
**Edge cases:** Rules referencing other workbooks are not allowed (Microsoft Support). Formulas that return errors apply no format. A fully locked reference and a row-locked reference differ in cost only slightly; the range size drives cost.
**Likely follow-ups:** 1) *How do I find the heavy rule?* Disable rules one by one in Manage Rules (delete and test). 2) *Do icon sets cost more?* Not measured. 3) *Alternative?* A Table or PivotTable.
**Common mistakes:** Applying rules to entire columns; pasting repeatedly so ranges split; using OFFSET/INDIRECT inside rules.

### Q45 ⭐ 🔴 How can you allow multiple selections in a single drop-down cell in Excel, and what is the Google Sheets alternative?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know Excel has no built-in multi-select drop-down, and that it needs VBA or a workaround, while Google Sheets offers it natively?
**Say this in the interview:** "Excel has no built-in multi-select drop-down. The usual way is a small VBA macro that appends each pick to the cell. In Google Sheets it is built in: turn on Allow multiple selections for a chip drop-down."
**Explain simply:**
- The Microsoft drop-down page I read describes picking one item and does not cover multiple selection (Microsoft Support, "Create a drop-down list"); I found no Excel built-in for it (from memory, unverified).
- The common solution is a *Worksheet_Change macro* (VBA code that runs when a cell changes). Programmatic edits skip validation (from memory).
- Such a file must be saved as .xlsm and macros must be enabled; VBA does not run in Excel for the web (from memory, unverified).
- Google Sheets: "Allow multiple selections" can only be enabled for chip format dropdowns, and mobile cannot pick multiple (Google Docs Editors Help, "Create an in-cell dropdown list", fetched 2026-10-22).
**Example:** A skills column where a candidate can pick "Excel, SQL, Power BI". After picks the cell contains one comma-separated text, which you can count with a formula.
**Sample sheet:**

Skills in A2:A5 after multiple picks.

|  | A (Skills) |
|---|---|
| 2 | Python, Excel |
| 3 | SQL |
| 4 | Excel, SQL, Power BI |
| 5 |  |

**Formula / Steps:** VBA macro: not run here (no Excel available; from common practice). Right-click the sheet tab > View Code > paste:

```vba
Private Sub Worksheet_Change(ByVal Target As Range)
    Dim oldVal As String, newVal As String
    If Target.Cells.Count > 1 Then Exit Sub
    If Intersect(Target, Me.Range("A2:A100")) Is Nothing Then Exit Sub
    On Error GoTo Done
    Application.EnableEvents = False
    newVal = Target.Value
    Application.Undo
    oldVal = Target.Value
    If oldVal = "" Then
        Target.Value = newVal
    ElseIf InStr(1, ", " & oldVal & ",", ", " & newVal & ",", vbTextCompare) = 0 Then
        Target.Value = oldVal & ", " & newVal
    End If
Done:
    Application.EnableEvents = True
End Sub
```

Save as .xlsm. Set A2:A100 to a normal Data Validation list first (Q3). Sheets: select cells > Insert > Dropdown > add options > turn on "Allow multiple selections" (chip format).
**Alternative:** No-macro routes: one column per choice, check boxes (Developer > Insert), or Power Apps/Forms (from memory, unverified). To count picks use the formula below.
**Result:** The macro's "append unless already there" logic simulated in Python (not VBA): pick "Excel" -> "Excel"; pick "SQL" -> "Excel, SQL"; pick "Excel" again -> unchanged (this macro ignores repeats; removing an item on a second pick needs extra code); pick "Power BI" -> "Excel, SQL, Power BI". Count formula `=IF(A2="",0,LEN(A2)-LEN(SUBSTITUTE(A2,",",""))+1)` run in LibreOffice 24.2: row 2 = 2, row 3 = 1, row 4 = 3, row 5 (blank) = 0. VBA and Sheets chips: not run here.
**Version note:** VBA works in desktop Excel (all versions); not in Excel for the web (from memory). Google Sheets: chips with multiple selection (Google Docs Editors Help, fetched; no version stated).
**Edge cases:** Items with commas in their names break the count. A macro that writes values bypasses the validation so the list "Allow only list items" will block manual editing of the combined text. Undo history is cleared by the macro (from memory).
**Likely follow-ups:** 1) *Need security approval for macros?* Yes. 2) *Count/lookup each item?* TEXTSPLIT in 365 (not run here). 3) *Alternative in Sheets?* chips as above.
**Common mistakes:** Expecting the plain list to allow multiple; leaving events off after an error; sharing as .xlsx and losing the macro.

### Q46 ⭐ 🔴 How do you build a dependent drop-down in Excel 365 using UNIQUE and FILTER spilled ranges, and what breaks it (#SPILL!, older versions)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know spilled-range references (`E2#`) as validation source, and the typical failure points?
**Say this in the interview:** "I put UNIQUE in a helper cell to list departments, then FILTER in another cell to list job titles for the chosen department. In Data Validation I set Source to the helper cell followed by a hash, like `=$E$2#`, so the drop-down grows and shrinks."
**Explain simply:**
- *UNIQUE* returns each value once; *FILTER* returns only rows meeting a test; both *spill* (fill several cells automatically).
- The `#` after a cell address means "the whole spilled range". Data Validation List cannot take a dynamic array formula directly, so a helper cell and `#` are needed (Excel University and Office Watch pages, fetched; not from Microsoft Support).
- Excel Tables make the spill resize when rows are added (Microsoft Support, "UNIQUE function").
- #SPILL! appears when "there is anything blocking the output range" (Microsoft Support, "Dynamic array formulas and spilled array behavior").
**Example:** Department to Job title. Choosing "IT" in D2 offers Data Analyst, Developer, Tester in the second drop-down.
**Sample sheet:**

Table Roles in A1:B9 (A Dept, B Job).

|  | A (Dept) | B (Job) |
|---|---|---|
| 2 | Sales | Sales Exec |
| 3 | Sales | Account Mgr |
| 4 | HR | HR Exec |
| 5 | HR | Recruiter |
| 6 | IT | Data Analyst |
| 7 | IT | Developer |
| 8 | IT | Tester |
| 9 | Finance | Accountant |

**Formula / Steps:** Not run here (LibreOffice 24.2 lacks UNIQUE/FILTER): 1) Convert A1:B9 to a Table named `Roles`. 2) E2 `=UNIQUE(Roles[Dept])`. 3) G2 `=FILTER(Roles[Job],Roles[Dept]=$D$2,"None")`. 4) D2: Data > Data Validation > List > Source `=$E$2#`. 5) D3 (job): List > Source `=$G$2#`.
**Alternative:** Old-version route: named ranges per department with `=INDIRECT($D$2)` (Q21).
**Result:** Not run here. Expected from pandas: UNIQUE gives ['Sales', 'HR', 'IT', 'Finance']; FILTER for "IT" gives ['Data Analyst', 'Developer', 'Tester'].
**Version note:** UNIQUE and FILTER need Excel 365, 2021 or 2024 (Microsoft Support pages list 365, 2024, 2021 and the Excel apps; they do not mention 2019 or earlier). Using the `#` source in validation: Excel University (fetched) and Office Watch (fetched; "Excel 365, 2021, 2024") describe it; I found no Microsoft Support page that documents it, so treat as third-party verified. In Excel 2019 or earlier the formulas return #NAME? (from memory, unverified).
**Edge cases:** #SPILL!: anything in the spill cells (text, another formula, merged cells) blocks the spill; clear the cells. #CALC!: FILTER with no match and no third argument (Microsoft Support, "FILTER function"). Changing the parent selection does not clear the old child value; add a check. Cross-workbook spills need both files open (Microsoft Support).
**Likely follow-ups:** 1) *Why a helper range?* Validation does not take a dynamic array formula directly. 2) *Works in Excel 2016?* No, formulas unsupported. 3) *Two-level only?* Chain more FILTERs.
**Common mistakes:** Typing `=UNIQUE(...)` directly in the validation Source; leaving cells under the helper formula occupied; forgetting the `#`.

