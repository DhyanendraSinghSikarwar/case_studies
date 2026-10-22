# Book 1 — Excel | Part 11: VBA Basics and Copilot in Excel and Google Sheets ⭐ 🟢🟡

**Target:** 20 questions | **Actual:** 21 questions
**Scope:** VBA and macro basics (12 questions plus 1 Apps Script gap-fill) and AI assistants in Excel and Google Sheets (8 questions).

### Q1 ⭐⭐ 🟢 What is a macro in Excel, and what is VBA?
**Asked at:** commonly asked (no company-specific report found). Candidate reports for MIS Executive interviews mention "Macro and VBA" questions (AmbitionBox/Naukri search snippets, not fetched, unverified). VBA appears in 13% of the repo's pooled job-description sample, about 19% of MIS/people postings (repo research).
**What the interviewer is checking:** Can you explain automation in one clear sentence and separate the two words?
**Say this in the interview:** "A macro is a saved set of steps that Excel can replay with one click. VBA, Visual Basic for Applications, is the programming language those steps are written in. I can record a macro, then open the code and adjust it."
**Explain simply:**
- Macro = a recorded or written list of instructions ("format this header, filter that column, save the file") that Excel repeats exactly.
- VBA = the language inside Excel that stores those instructions as text code. A recorded macro is just VBA that Excel wrote for you.
- You see and edit the code in the Visual Basic Editor (VBE), a separate window opened from the Developer tab (Microsoft Support, "Quick start: Create a macro").
- Use it for repetitive, rule-based work. Do not use it when a formula, PivotTable or Power Query already does the job and refreshes by itself.
**Example:** Every month an HR analyst does the same 9 clicks: delete blank rows, bold the header, filter "Absent", copy to a new sheet, save. A macro does it in about 2 seconds; the analyst clicks one button.
**Formula / Steps:** A tiny macro (VBA, not run here):
```vba
Sub BoldHeader()
    Rows(1).Font.Bold = True
End Sub
```
**Alternative:** Power Query for repeatable cleaning, Office Scripts or Power Automate for cloud automation (I have not read Microsoft's pages on those, so I will not describe their details).
**Version note:** VBA is part of desktop Excel (Windows and Mac). Whether the web version runs VBA: from memory, unverified. Google Sheets uses Apps Script instead (Q13).
**Edge cases:** Macros only run if the file is a macro-enabled workbook and the user allows macros (Q7).
**Likely follow-ups:** 1) *Is a macro a formula?* No, a formula calculates a value in a cell; a macro performs actions. 2) *Do you need to know VBA to use macros?* No, recording needs no coding, but editing needs the basics.
**Common mistakes:** Saying a macro "is" VBA (it is written in VBA); automating something a PivotTable would solve.

### Q2 ⭐⭐ 🟢 How do you record a macro in Excel, and where do you see and edit the code it creates?
**Asked at:** commonly asked (no company-specific report found); a basic step in every macro tutorial.
**What the interviewer is checking:** Have you actually done it, and do you know the Developer tab and the VBE?
**Say this in the interview:** "I turn on the Developer tab, click Record Macro, name it, do the steps once, click Stop Recording. To see the code I go Developer, Macros, pick it, Edit. That opens the Visual Basic Editor."
**Explain simply:**
- The Developer tab is hidden by default; you switch it on first (Microsoft Support, "Quick start: Create a macro").
- Record Macro asks for a name, an optional shortcut key and a description. Names cannot contain spaces and must start with a letter (Microsoft Support, Developer tab/macro article for Mac, seen in search results only).
- Everything you do while recording is written as code. Stop Recording ends it.
- Macros > Edit opens the Visual Basic Editor where "the actions that you recorded appear as code" (same Quick start page).
- To run from the editor: click inside the macro and press F5 (Microsoft Support, search result for "Run a macro in Excel").
**Example:** Record: select A1:F1, make it bold with a blue fill, Stop. Open Edit and you will see lines such as `Selection.Font.Bold = True` (typical recorder output, from memory, not run here).
**Formula / Steps:** 1. File > Options > Customize Ribbon > tick Developer (from memory) 2. Developer > Code > Record Macro 3. Name (for example `FormatHeader`), choose where to store it, OK 4. Do the actions 5. Developer > Stop Recording 6. Developer > Macros > select > Edit (not run here).
**Alternative:** Alt+F11 opens the VBE directly (from memory, unverified); View > Macros > Record Macro also works (from memory).
**Version note:** Same steps on Excel 2016, 2019, 2021, 2024 and Microsoft 365 desktop; the Mac menu names differ slightly (Microsoft Support, Mac Developer tab article, search result only). Google Sheets has its own recorder (Q13).
**Edge cases:** Recording captures every click, including mistakes; also the "Store macro in" choice decides whether it lives in this workbook or the Personal Macro Workbook (from memory, unverified).
**Likely follow-ups:** 1) *Can you assign a button?* Yes, insert a shape or button and Assign Macro. 2) *Can you undo a macro?* Usually not; save a copy first.
**Common mistakes:** Clicking around while recording; not saving as .xlsm (Q7); spaces in the name.

### Q3 ⭐⭐ 🟢 What is the difference between recording a macro and writing VBA code by hand?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand the recorder's limits (it cannot loop or decide)?
**Say this in the interview:** "Recording copies exactly what I did, so it is fast but rigid. Writing by hand lets me add loops, IF decisions and error handling, so it works on any number of rows. In practice I record first, then clean and extend the code."
**Explain simply:**
- Recorder: repeats your exact clicks, on the same cells, with lots of `.Select`; cannot loop or choose.
- Hand-written: you decide the logic: "for every row, if tenure is under a year, flag it".
- Recorded code is slow and long because it selects things on screen; handwritten code can work on cells directly.
- Best practice: use the recorder to discover the right commands, then rewrite.
**Example:** Task: bold the header and flag short-tenure staff. The recorder can do the bold. Only handwritten code can loop through however many rows exist and flag them (see Q14).
**Formula / Steps:** Typical recorded (from memory, not run here):
```vba
Range("A1:F1").Select
Selection.Font.Bold = True
```
Cleaner handwritten equivalent (not run here):
```vba
ThisWorkbook.Worksheets("Employees").Range("A1:F1").Font.Bold = True
```
**Alternative:** Mix: record, then edit.
**Version note:** Applies to all desktop Excel versions.
**Edge cases:** A recorded macro breaks if the data grows or the sheet name changes.
**Likely follow-ups:** 1) *Why avoid Select?* It is slow and fragile. 2) *Can the recorder do loops?* No.
**Common mistakes:** Assuming the recorder "understands" the intent; never reading the generated code.

### Q4 ⭐⭐ 🟢 Have you used a macro or VBA to automate a task? Give an example, such as a monthly HR attendance report.
**Asked at:** commonly asked (no company-specific report found); typical in MIS/reporting interviews (candidate-report snippets, unverified).
**What the interviewer is checking:** Real experience: problem, approach, result, and awareness of risk.
**Say this in the interview:** "Yes. If you have not, say so honestly and describe how you would do it. My example: a monthly attendance report. The macro calculates each person's attendance percentage, flags anyone under 90%, and tells me how many were flagged. It turns a 30-minute manual task into one click." (Only claim this if true; otherwise present it as a project you built.)
**Explain simply:**
- Describe: the input (raw HR export), the rule (below 90% = Low), the output (flag column plus a count).
- Mention safeguards: a zero working-days case (a new joiner) is marked "Check", not divided.
- Mention you kept a backup and tested on a copy.
**Example:** Seven employees; working days 22. Real run below (formulas run in LibreOffice 24.2; the macro itself not run here).
**Sample sheet:**
| | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| 1 | Emp ID | Name | Dept | Working days | Days present | Attendance % | Flag |
| 2 | E101 | Asha | Sales | 22 | 21 | | |
| 3 | E102 | Ravi | Sales | 22 | 17 | | |
| 4 | E103 | Meena | Ops | 22 | 22 | | |
| 5 | E104 | Kiran | Ops | 22 | 19 | | |
| 6 | E105 | Sana | HR | 22 | 14 | | |
| 7 | E106 | Dev | HR | 22 | 20 | | |
| 8 | E107 | Neha | Ops | 0 | 0 | | |

**Formula / Steps:** VBA (not run here):
```vba
Option Explicit
Sub MonthlyAttendanceReport()
    Dim ws As Worksheet, r As Long, lastRow As Long, lowCount As Long
    Set ws = ThisWorkbook.Worksheets("Attendance")
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    For r = 2 To lastRow
        If ws.Cells(r, "D").Value = 0 Then
            ws.Cells(r, "F").Value = "n/a"
            ws.Cells(r, "G").Value = "Check"
        Else
            ws.Cells(r, "F").Value = ws.Cells(r, "E").Value / ws.Cells(r, "D").Value
            If ws.Cells(r, "F").Value < 0.9 Then
                ws.Cells(r, "G").Value = "Low": lowCount = lowCount + 1
            Else
                ws.Cells(r, "G").Value = "OK"
            End If
        End If
    Next r
    ws.Range("F2:F" & lastRow).NumberFormat = "0.0%"
    MsgBox lowCount & " employees below 90%"
End Sub
```
**Alternative:** The same logic as formulas, `F2 =IF(D2=0,"n/a",E2/D2)` and `G2 =IF(ISNUMBER(F2),IF(F2<0.9,"Low","OK"),"Check")`.
**Result:** (Formulas run in LibreOffice; the macro is expected to give the same) F2:F8 = 95.5%, 77.3%, 100%, 86.4%, 63.6%, 90.9%, n/a; G2:G8 = OK, Low, OK, Low, Low, OK, Check. Low count `=COUNTIF(G2:G8,"Low")` = 3, so the message box should say "3 employees below 90%". Pandas gives the same three flags. Average attendance: Ops 93.2%, HR 77.3% (the "n/a" row is ignored by AVERAGEIFS).
**Version note:** Desktop Excel only; macros need .xlsm (Q7).
**Edge cases:** Blank working days counts as 0 in VBA; text in D would cause an error (Q16).
**Likely follow-ups:** 1) *Why not formulas?* For this, formulas are fine; macros earn their keep when steps include copying, saving, emailing. 2) *How did you test?* On a copy, comparing counts to a manual check.
**Common mistakes:** Claiming experience you cannot explain line by line; no zero-division guard.

### Q5 ⭐⭐ 🟢 What is Copilot in Excel, and how can a data analyst use it?
**Asked at:** commonly asked (no company-specific report found); AI tools are named in 14-20% of the repo's job-description samples (repo research).
**What the interviewer is checking:** Do you know it is an assistant to speed up work, and that you must verify it?
**Say this in the interview:** "Copilot in Excel is Microsoft's AI assistant inside Excel. I type a request in plain English, such as 'which department has the highest attrition', and it can summarize, build formulas, charts and PivotTables. I always check its answer against my own calculation before using it."
**Explain simply:**
- Microsoft says it can add and edit sheets, generate data and formulas, summarize data, create charts and PivotTables, sort/filter/highlight and import data from other workbooks (Microsoft Support, "Get started with Copilot in Excel").
- Modes: chat-only does not change your workbook; plan mode shows a plan for review; you can stop it any time (same page).
- It is probabilistic: it can be wrong. Microsoft warns the content "can be inaccurate or inappropriate" and to "review, edit, and verify anything Copilot creates" (Microsoft Support, "Frequently asked questions about Copilot in Excel").
- Analyst uses: quick first look, formula drafting, chart ideas, summarising comments.
**Example:** On the 8-employee sheet below, you ask for attrition by department. Reference answer I computed with COUNTIFS (run in LibreOffice): Sales 33.3%, HR 50%, Ops 0%. Copilot's reply is not run here; compare it to these.
**Sample sheet:**
| | A | B | C |
|---|---|---|---|
| 1 | Emp ID | Dept | Status |
| 2 | E1 | Sales | Active |
| 3 | E2 | Sales | Left |
| 4 | E3 | Ops | Active |
| 5 | E4 | Ops | Active |
| 6 | E5 | HR | Left |
| 7 | E6 | HR | Active |
| 8 | E7 | Sales | Active |
| 9 | E8 | Ops | Active |

**Formula / Steps:** Click the Copilot icon on the Home tab/ribbon (the pane opens at the side; exact location varies, from memory), type the request. Reference formula: `=COUNTIFS(B2:B9,"Sales",C2:C9,"Left")/COUNTIF(B2:B9,"Sales")`.
**Alternative:** A PivotTable with Status in Columns and Dept in Rows, "Show values as % of row".
**Result:** 33.3%, 50%, 0% (Sales, HR, Ops).
**Version note:** Microsoft's page lists Excel for Microsoft 365 on Windows, Mac, web, iPad, iPhone, Android with different modes; Android is chat mode only (Microsoft Support, "Get started with Copilot in Excel"). Not in Excel 2016-2024 perpetual versions: not stated on pages I read, from memory unverified.
**Edge cases:** Small samples (1-3 employees) make percentages look dramatic; Copilot may not say so.
**Likely follow-ups:** 1) *Is it a function?* The old COPILOT function is retired (Q18). 2) *Can you trust it?* Verify (Q6).
**Common mistakes:** Pasting its numbers into a report unchecked; assuming it is free in every plan (Q12).

### Q6 ⭐⭐ 🟡 How do you verify the output of Copilot or any AI tool before you send a report to a manager?
**Asked at:** commonly asked (no company-specific report found); the standard follow-up to any AI-tool question.
**What the interviewer is checking:** Professional skepticism and a repeatable checklist.
**Say this in the interview:** "I treat AI output like a junior colleague's draft. I recompute key numbers independently, reconcile totals back to the source, test a sample row by hand, and check the logic and filters it used. Nothing goes to a manager until the totals tie out."
**Explain simply:**
- Microsoft itself says to "review, edit, and verify anything Copilot creates" (Microsoft Support, "Frequently asked questions about Copilot in Excel"); Google's page also warns Gemini "may suggest inaccurate or inappropriate information" (Google Docs Editors Help, "Collaborate with Gemini in Google Sheets").
- Checklist: 1) re-derive headline numbers with a formula or PivotTable; 2) reconcile (parts add to total, row counts match source); 3) spot-check 3-5 rows by hand; 4) read the formula Copilot wrote; 5) check ranges include all rows; 6) sense-check against last month.
- Ask the tool to explain what it did and what data it used.
**Example:** Copilot says "attrition was 12.5%, 1 leaver". Source sheet has 8 employees. Check run in LibreOffice: leavers = 2, attrition = 25%. The AI was wrong, caught by a 10-second COUNTIF. (The Copilot claim here is an invented illustration.)
**Sample sheet:** (A:D = Emp ID, Dept, Status, Salary; rows 2-9; Status "Left" for E2 and E5)
| | F | G |
|---|---|---|
| 1 | Headcount | 8 |
| 2 | Leavers | 2 |
| 3 | Attrition % | 25% |
| 4 | Sales payroll | 139,000 |
| 5 | Total payroll | 354,000 |
| 6 | Reconciliation (Sales+Ops+HR − total) | 0 |

**Formula / Steps:** `G1 =COUNTA(A2:A9)`, `G2 =COUNTIF(C2:C9,"Left")`, `G3 =G2/G1`, `G4 =SUMIFS(D2:D9,B2:B9,"Sales")`, `G5 =SUM(D2:D9)`, `G6 =SUMIFS(D2:D9,B2:B9,"Sales")+SUMIFS(D2:D9,B2:B9,"Ops")+SUMIFS(D2:D9,B2:B9,"HR")-G5`.
**Alternative:** Rebuild the same figure in a PivotTable or ask a colleague to review.
**Result:** 8, 2, 0.25, 139000, 354000, 0 (run in LibreOffice 24.2).
**Version note:** The check formulas work in every Excel version and Google Sheets.
**Edge cases:** A reconciliation of 0 only proves totals agree, not that categories are right; check for misspelt departments.
**Likely follow-ups:** 1) *What if you can't verify?* Do not send it, or label it unverified. 2) *Do you share the prompt?* Yes, note AI was used and how it was checked.
**Common mistakes:** Checking only the final number; trusting a confident-sounding explanation.

### Q7 ⭐ 🟢 How do you save a workbook that contains macros, and why does Excel show a security warning for macros?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know .xlsm and the security reason?
**Say this in the interview:** "I save it as an Excel Macro-Enabled Workbook, .xlsm. A normal .xlsx cannot hold macros. Excel warns because macros can contain malicious code, so it asks before running them. I only enable macros in files from sources I trust."
**Explain simply:**
- Save As type: Excel Macro-Enabled Workbook (*.xlsm). If you try .xlsx, Excel offers to save without the macro, and choosing Yes removes the code (Microsoft Support, "Save a macro", Excel 2013 page, seen only in search results; wording may differ now).
- Microsoft: "some macros can pose a security risk by introducing viruses or malicious software" and "never enable macros in a Microsoft 365 file unless you're sure you know what those macros do" (Microsoft Support, "Enable or disable macros in Microsoft 365 files").
- The Trust Center (File > Options > Trust Center) offers: disable all without notification, disable with notification, disable except digitally signed, enable all (not recommended) (same page).
- Trusted locations are an alternative to trusting each file (same page).
**Example:** HR gets an "attendance_tool.xlsm" by email; the yellow bar says macros are disabled. You check with the sender, then click Enable Content.
**Formula / Steps:** File > Save As > Save as type > Excel Macro-Enabled Workbook (*.xlsm) > Save. Settings: File > Options > Trust Center > Trust Center Settings > Macro Settings.
**Alternative:** Keep reusable macros in the Personal Macro Workbook (from memory, unverified).
**Version note:** Same on Excel 2016-365 desktop. Files from the internet being blocked by default: Microsoft links an article titled "Macros from the internet are blocked by default in Office"; I did not read it, so details are from memory, unverified.
**Edge cases:** Corporate IT may lock the settings (the Microsoft page says administrators may prevent changes on managed devices).
**Likely follow-ups:** 1) *What is a digital signature?* Proof of who wrote the macro. 2) *Can you view the file without enabling macros?* Yes (same Microsoft page).
**Common mistakes:** Saving as .xlsx and losing the code; enabling all macros permanently.

### Q8 ⭐ 🟢 What is the difference between absolute and relative reference recording in the macro recorder?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know recording is absolute by default and when to switch?
**Say this in the interview:** "By default the recorder is absolute: it remembers exact cells, such as D2. With Use Relative References switched on, it remembers movement from wherever you started, like 'one cell down'. I use relative when the macro must work from different starting cells."
**Explain simply:**
- Absolute: always acts on the same cells, whatever is selected.
- Relative: acts relative to the active cell when you run it.
- Microsoft's VBA reference: `Application.RecordRelative` is "True if macros are recorded by using relative references; False if recording is absolute" (Microsoft Learn, "Application.RecordRelative property (Excel)").
- The toggle is a button on the Developer tab; click it before recording (button location from memory; Microsoft's relative-references article was not retrievable here).
**Example:** Record "type 'Present' in the next empty cell below the active cell". Absolute: always writes in D2. Relative: writes under wherever you are.
**Formula / Steps:** Typical recorder output (from memory, not run here):
```vba
' Absolute
Range("D2").Select
' Relative
ActiveCell.Offset(1, 0).Range("A1").Select
```
Steps: Developer > Use Relative References (toggle on) > Record Macro > actions > Stop.
**Alternative:** Hand-written code with `Offset` or a loop avoids the issue.
**Version note:** Same in all desktop versions.
**Edge cases:** The setting stays on until you turn it off or close Excel (from memory, unverified).
**Likely follow-ups:** 1) *Which is the default?* Absolute (Microsoft Learn above). 2) *Mixed?* You can toggle during recording.
**Common mistakes:** Forgetting to toggle, then wondering why the macro hits the wrong cells.

### Q9 ⭐ 🟢 What does Option Explicit do, and how do you declare variables in VBA (Dim and data types)?
**Asked at:** commonly asked (no company-specific report found); basic VBA lists include data types (AnalysisTabs, headings only).
**What the interviewer is checking:** Good habits: declaring variables, picking Long over Integer.
**Say this in the interview:** "Option Explicit forces me to declare every variable with Dim, so a typo becomes a compile error instead of a silent bug. I declare with a type, like Dim r As Long."
**Explain simply:**
- Microsoft: Option Explicit is "used at the module level to force explicit declaration of all variables in that module"; undeclared names cause "an error at compile time", and without it undeclared variables become Variant (Microsoft Learn, "Option Explicit statement (VBA)").
- It must be at the top of the module, before any procedures (same page).
- Dim name As Type creates a variable. Common types (from memory, unverified): Long (whole numbers, row numbers), Double (decimals), String (text), Date, Boolean (True/False), Variant (anything), Worksheet/Range (objects).
- Use Long for rows: Integer tops out at 32,767 but Excel has 1,048,576 rows (from memory).
**Example:** Typo case: you declare `totalDays` but later write `totaldys = totalDays + 1`. With Option Explicit, VBA stops and highlights it.
**Formula / Steps:** (VBA, not run here)
```vba
Option Explicit
Sub Demo()
    Dim r As Long, name As String, salary As Double, joined As Date
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("Employees")  ' objects need Set
    r = 2
End Sub
```
To turn it on automatically: VBE > Tools > Options > Require Variable Declaration (from memory).
**Alternative:** Skip declaration (not recommended).
**Version note:** All desktop versions.
**Edge cases:** `Dim a, b As Long` makes `a` a Variant, only `b` is Long (from memory).
**Likely follow-ups:** 1) *Dim vs Public?* Dim is local to a procedure/module; Public shares across modules. 2) *Why Variant is slow?* Flexible but uses more memory.
**Common mistakes:** Using Integer for row counts; forgetting `Set` for objects.

### Q10 ⭐ 🟢 What is the difference between a Sub and a Function in VBA, and what is a user-defined function (UDF)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Actions versus returned values, and the idea of custom worksheet functions.
**Say this in the interview:** "A Sub does things and returns nothing. A Function returns a value. A user-defined function is a Function I write in VBA that I can then use in a cell, like =TenureYears(C2), just like SUM."
**Explain simply:**
- Microsoft: unlike a Sub, a Function can be used "on the right side of an expression in the same way you use any intrinsic function" and returns a value by assigning it to the function's name (Microsoft Learn, "Function statement (VBA)").
- Sub: run from a button/Macros dialog. Function: called from a cell or other code.
- A UDF is a public Function in a standard module of an .xlsm workbook (from memory).
- UDFs normally only return a value; they should not change other cells (from memory).
**Example:** Excel has no "complete years of service" function except the hidden DATEDIF. A UDF `TenureYears` gives it a friendly name.
**Sample sheet:** (As-of 22-Oct-2026)
| | A | B | C |
|---|---|---|---|
| 1 | Hire | As of | DATEDIF "y" |
| 2 | 15-Jan-2024 | 22-Oct-2026 | 2 |
| 3 | 22-Oct-2025 | 22-Oct-2026 | 1 |
| 4 | 23-Oct-2025 | 22-Oct-2026 | 0 |
| 5 | 29-Feb-2020 | 28-Feb-2026 | 5 |
| 6 | 29-Feb-2020 | 01-Mar-2026 | 6 |

**Formula / Steps:** VBA (not run here):
```vba
Function TenureYears(hireDate As Date, asOf As Date) As Long
    Dim y As Long
    y = Year(asOf) - Year(hireDate)
    If DateSerial(Year(asOf), Month(hireDate), Day(hireDate)) > asOf Then y = y - 1
    TenureYears = y
End Function
```
Use in a cell: `=TenureYears(A2,B2)`.
**Alternative:** `=DATEDIF(A2,B2,"y")` without any VBA.
**Result:** DATEDIF column above was run in LibreOffice. I re-implemented the UDF's algorithm in Python and it matched all five rows (2, 1, 0, 5, 6); the VBA itself was not run.
**Version note:** UDFs need desktop Excel and macros enabled; whether they run in Excel for the web: from memory, unverified. Not available in Google Sheets (use Apps Script custom functions).
**Edge cases:** Feb 29 hire dates; DateSerial rolls 29-Feb-2026 to 1-Mar-2026, matching the sample.
**Likely follow-ups:** 1) *Why not just use DATEDIF?* Simpler; UDF only if logic is custom. 2) *Downside of UDFs?* Files must be .xlsm; others may block macros.
**Common mistakes:** Forgetting to assign the result to the function name; expecting a Function to be runnable from the Macros list (it is not, if it takes arguments).

### Q11 ⭐ 🟢 What is Gemini in Google Sheets, and what can it do for an analyst?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of the Google-side AI and the same verification mindset.
**Say this in the interview:** "Gemini is Google's AI assistant built into Sheets. I can ask in plain English for formulas, tables, charts or a summary of the data. It needs an eligible Workspace or Google AI plan, and I still verify its answers."
**Explain simply:**
- Google's help page says Gemini can build tables, write formulas, generate analysis and insights, create charts, and make edits such as conditional formatting, pivot tables, dropdowns, filters, sorting, find-and-replace (Google Docs Editors Help, "Collaborate with Gemini in Google Sheets").
- The same page: "This feature requires an eligible Google Workspace or Google AI plan" and "works best with native Google Sheets files", so convert .xlsx first.
- Chat history can be lost on reload; insert the output into the sheet to keep it (same page).
- Cell-level AI function: the fetched Google page does not document a GEMINI function. Third-party guides describe `=GEMINI()` or `=AI()`; names and plans conflict, so treat as unverified.
**Example:** Paste 500 survey comments, ask Gemini to suggest a formula that counts comments containing "manager". You check the formula on 5 rows.
**Formula / Steps:** Open the sheet > open the Gemini panel (button location from memory, unverified) > type request > review > insert.
**Alternative:** Normal formulas, PivotTables, or Apps Script.
**Version note:** Plan names and prices change often; check Google's current page (not verified).
**Edge cases:** Sensitive data: check the company's AI policy first (Q19).
**Likely follow-ups:** 1) *Copilot vs Gemini?* Same idea, different ecosystem. 2) *Is it accurate?* Google warns it may suggest inaccurate information.
**Common mistakes:** Assuming it can read Excel files directly; not saving the response.

### Q12 ⭐ 🟢 What do you need in place to use Copilot in Excel (licence, file location, data format)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Practical awareness that it is not automatically available.
**Say this in the interview:** "It needs an eligible Microsoft licence and an admin who has enabled it. The file should be in a modern format such as .xlsx. Other conditions I'd check are calculation set to Automatic and no forced SharePoint check-out. Plans change, so I check Microsoft's current page."
**Explain simply:**
- Licence: Microsoft's FAQ lists a Microsoft 365 Personal or Family subscription with an AI credits plan, a Microsoft 365 Premium subscription, a commercial Microsoft Copilot subscription, or a Copilot Chat-eligible business/enterprise subscription; availability "may vary" by licence and tenant settings (Microsoft Support, "Frequently asked questions about Copilot in Excel").
- File format: save as a modern format such as .xlsx; Strict Open XML is unsupported (same page).
- Settings: editing needs Calculation Options on Automatic; SharePoint check-out requirements stop it working on Windows and Mac (same page).
- Location and table: the pages I read do not state a required location or that data must be a table. Third-party guides say OneDrive/SharePoint with AutoSave and an Excel Table; I could not confirm this on Microsoft's pages. Tidy tabular data with headers helps in practice (from memory).
**Example:** The Copilot icon is missing for an HR analyst: check licence, then file format, then calculation mode.
**Formula / Steps:** Check: account settings licence > file is .xlsx > Formulas > Calculation Options > Automatic > select a cell in the data > open Copilot. To format as a table: Ctrl+T.
**Alternative:** If unavailable, use PivotTables/formulas.
**Version note:** Microsoft 365 apps on Windows, Mac, web, iPad, iPhone, Android with different modes (Microsoft Support, "Get started with Copilot in Excel"). Licence tiers are the most change-prone fact; verify.
**Edge cases:** Managed company devices may block it.
**Likely follow-ups:** 1) *Why grey/missing?* Licence, tenant admin, or file settings. 2) *Does it work offline?* From memory, no, it needs the service.
**Common mistakes:** Quoting a plan name from an old article; blank header cells.

### Q13 ⭐ 🟢 What is the Google Sheets equivalent of VBA macros, and how does it differ from Excel VBA?
**Asked at:** commonly asked (no company-specific report found); added as a gap-fill for Sheets-based teams.
**What the interviewer is checking:** Do you know Apps Script is JavaScript-based and cloud-run?
**Say this in the interview:** "Google Sheets uses Apps Script, which is JavaScript, plus a macro recorder. The recorder writes an Apps Script function for you. Unlike VBA, it runs in Google's cloud and is saved with the sheet, not in a .xlsm file."
**Explain simply:**
- Google: Sheets macros "duplicate a specific series of UI interactions that you define", and recording adds a function to an Apps Script project bound to the sheet, in a file called `macros.gs` (Google for Developers, "Google Sheets Macros").
- You can also import any existing script function as a macro (Extensions > Macros > Import); a sheet can only have ten macros with shortcuts (same page).
- Macros work only in bound scripts, not standalone scripts or web apps (same page).
- Differences from VBA (from memory unless stated): language JavaScript vs VBA; no .xlsm; each call to read/write is slow, so read and write in blocks; runs on Google servers with usage quotas.
**Example:** Same tenure-flag task as Q14 in Apps Script. Only the decision logic was run, in Node.js; Apps Script itself was not run here. Result on the Q14 sample: Under 1 yr, OK, Under 1 yr, OK, (blank), Check date, Under 1 yr, OK.
**Formula / Steps:** Extensions > Macros > Record macro (Google page) or Extensions > Apps Script. Code (not run here):
```javascript
function flagNewJoiners() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Employees');
  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return;
  const hires = sheet.getRange(2, 3, lastRow - 1, 1).getValues();
  const cutoff = new Date();
  cutoff.setFullYear(cutoff.getFullYear() - 1);
  cutoff.setHours(0, 0, 0, 0);
  const out = hires.map(([d]) =>
    d === '' ? [''] : !(d instanceof Date) ? ['Check date'] : d > cutoff ? ['Under 1 yr'] : ['OK']);
  sheet.getRange(2, 4, out.length, 1).setValues(out);
}
```
**Alternative:** Built-in formulas such as `ARRAYFORMULA`, or Excel's Office Scripts (not described here, not verified).
**Version note:** Apps Script is part of Google Workspace/Sheets; Excel VBA does not run in Sheets.
**Edge cases:** Time zones can shift dates; Apps Script returns Date objects.
**Likely follow-ups:** 1) *Can it email?* Yes, with Gmail/MailApp services (from memory). 2) *Can I run VBA in Sheets?* No.
**Common mistakes:** Calling `getValue` in a loop (slow); thinking recorded macros work outside the bound sheet.

### Q14 ⭐ 🟡 Write a VBA loop that goes through rows 2 to 500 and flags employees with less than one year of tenure.
**Asked at:** commonly asked (no company-specific report found); a classic practical VBA exercise.
**What the interviewer is checking:** Loop syntax, date logic, and handling blanks/bad data.
**Say this in the interview:** "I loop r from 2 to 500, read the hire date, skip blanks, mark text as 'Check date', and compare the hire date with one year ago. Under one year gets flagged."
**Explain simply:**
- `For r = 2 To 500 ... Next r` repeats the block for each row number.
- "Less than one year" means hired after the date exactly one year ago (`DateAdd("yyyy", -1, Date)`). Someone hired exactly one year ago has one full year, so is not flagged.
- `VarType(x) = vbDate` accepts real dates and rejects text such as "N/A".
- `IsEmpty` skips blank rows.
**Example:** As-of date 22-Oct-2026 (cutoff 22-Oct-2025). Formula route run in LibreOffice; VBA logic mirrored in Python; VBA not run here.
**Sample sheet:**
| | A | B | C | D |
|---|---|---|---|---|
| 1 | Emp ID | Name | Hire date | Flag |
| 2 | E201 | Ira | 10-Mar-2026 | |
| 3 | E202 | Om | 22-Oct-2025 | |
| 4 | E203 | Uma | 23-Oct-2025 | |
| 5 | E204 | Vik | 15-Jan-2024 | |
| 6 | E205 | Zed | (blank) | |
| 7 | E206 | Tia | N/A (text) | |
| 8 | E207 | Gus | 01-Sep-2026 | |
| 9 | E208 | Lee | 30-Jun-2020 | |

**Formula / Steps:** VBA (not run here):
```vba
Option Explicit
Sub FlagNewJoiners()
    Dim ws As Worksheet, r As Long, hireDate As Variant, cutoff As Date
    Set ws = ThisWorkbook.Worksheets("Employees")
    cutoff = DateAdd("yyyy", -1, Date)
    For r = 2 To 500
        hireDate = ws.Cells(r, "C").Value
        ws.Cells(r, "D").Interior.Pattern = xlNone
        If IsEmpty(hireDate) Then
            ws.Cells(r, "D").Value = ""
        ElseIf VarType(hireDate) <> vbDate Then
            ws.Cells(r, "D").Value = "Check date"
        ElseIf hireDate > cutoff Then
            ws.Cells(r, "D").Value = "Under 1 yr"
            ws.Cells(r, "D").Interior.Color = RGB(255, 235, 156)
        Else
            ws.Cells(r, "D").Value = "OK"
        End If
    Next r
End Sub
```
**Alternative:** Formula in D2: `=IF(C2="","",IF(ISNUMBER(C2),IF(DATEDIF(C2,$G$1,"y")<1,"Under 1 yr","OK"),"Check date"))`, copy down, with the as-of date in G1.
**Result:** D2:D9 = Under 1 yr, OK, Under 1 yr, OK, (blank), Check date, Under 1 yr, OK. The DATEDIF formula was run in LibreOffice 24.2; a Python mirror of the VBA rule gave the identical eight results.
**Version note:** Works in all desktop Excel versions; DATEDIF is an undocumented-but-working function (from memory, unverified).
**Edge cases:** Text dates; blank rows; hard-coded 500 misses rows beyond it (use Q15's last row); leap-day hire dates.
**Likely follow-ups:** 1) *Why not hard-code 500?* Use the last used row (Q15). 2) *Speed?* Read the column into an array first (Q17).
**Common mistakes:** Using `<` vs `<=` wrongly at the exact anniversary; assuming blank cells are zero dates.

### Q15 ⭐ 🟡 How do you find the last used row in a column with VBA, and why is it needed?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The standard `End(xlUp)` pattern.
**Say this in the interview:** "I start at the very bottom of the column and jump up to the last filled cell: `ws.Cells(ws.Rows.Count, "A").End(xlUp).Row`. It is needed so loops cover exactly the data, however many rows there are this month."
**Explain simply:**
- Microsoft: `Range.End` "is equivalent to pressing END+UP ARROW..." (Microsoft Learn, "Range.End property (Excel)").
- Starting at the bottom cell and going up finds the last filled cell even if there are gaps higher up.
- Going down from the top (`End(xlDown)`) stops at the first blank: gives the wrong answer with gaps.
- Needed because monthly data length changes; hard-coded ranges miss or waste rows.
**Example:** Column A has a gap at row 5. Results below.
**Sample sheet:**
| | A |
|---|---|
| 1 | Emp ID |
| 2 | E101 |
| 3 | E102 |
| 4 | E103 |
| 5 | (blank) |
| 6 | E105 |
| 7 | E106 |
| 8 | E107 |

**Formula / Steps:** VBA (not run here):
```vba
Dim lastRow As Long
lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row   ' expected 8
firstGapAbove = ws.Range("A1").End(xlDown).Row         ' expected 4 (stops at the gap)
```
**Alternative:** Worksheet formula that behaves the same way: `=SUMPRODUCT(MAX((A1:A1000<>"")*ROW(A1:A1000)))`.
**Result:** The worksheet formula returned 8 (last row), and `=MATCH(TRUE,INDEX(A1:A1000="",0),0)-1` returned 4 (rows before the first gap), run in LibreOffice 24.2. The VBA expectations (8 and 4) follow the same logic but were not run in Excel.
**Version note:** All desktop versions; `ws.Rows.Count` adapts to the sheet size (1,048,576 rows in modern Excel, from memory).
**Edge cases:** Empty column returns row 1; hidden/filtered rows still count; cells with formulas returning "" count as used; `UsedRange` can include formatted empty cells.
**Likely follow-ups:** 1) *Last column?* `ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column`. 2) *Why not UsedRange?* It can be inflated by formatting.
**Common mistakes:** Using `End(xlDown)` from the top; forgetting that an empty column gives 1, so `For r = 2 To lastRow` just does not run.

### Q16 ⭐ 🟡 How do you handle errors in VBA (On Error GoTo versus On Error Resume Next)?
**Asked at:** commonly asked; error handling appears in basic VBA lists (AnalysisTabs headings, not fetched in full).
**What the interviewer is checking:** Do you know that Resume Next hides errors rather than fixing them?
**Say this in the interview:** "On Error GoTo jumps to a handler where I show a message, clean up and exit. On Error Resume Next just skips the failing line, which is only safe for a single statement I check immediately with Err.Number. Used carelessly it hides bugs."
**Explain simply:**
- Microsoft: `On Error GoTo line` enables the handler at that label; `Resume Next` continues at the statement after the error; `GoTo 0` disables handling (Microsoft Learn, "On Error statement (VBA)").
- Without any On Error, a runtime error stops the macro with a message (same page).
- `Err.Number` and `Err.Description` tell you what failed (same page).
- Put `Exit Sub` before the handler so it does not run when all is fine (same page).
- Always restore settings (like ScreenUpdating) in the clean-up part.
**Example:** Row 8 has 0 working days, so `E/D` gives Division by zero (error 11, from memory). Simulation in Python of VBA's behaviour (not run in Excel): with Resume Next, the variable keeps the previous row's value, so Neha's attendance shows 90.9% instead of an error: attendance values written = 95.5, 77.3, 100, 86.4, 63.6, 90.9, 90.9.
**Formula / Steps:** VBA (not run here):
```vba
Sub SafeReport()
    Dim ws As Worksheet, r As Long, pct As Double
    On Error GoTo Fail
    Application.ScreenUpdating = False
    Set ws = ThisWorkbook.Worksheets("Attendance")
    For r = 2 To 8
        pct = ws.Cells(r, "E").Value / ws.Cells(r, "D").Value
        ws.Cells(r, "F").Value = pct
    Next r
Done:
    Application.ScreenUpdating = True
    Exit Sub
Fail:
    MsgBox "Row " & r & ": " & Err.Number & " - " & Err.Description
    Resume Done
End Sub
```
**Alternative:** Prevent the error: `If ws.Cells(r,"D").Value = 0 Then ... Else ...` (as in Q4).
**Version note:** All versions.
**Edge cases:** Handler errors inside a handler are not caught; Resume Next resets in called procedures (Microsoft page).
**Likely follow-ups:** 1) *When is Resume Next fine?* To test whether a sheet exists, then check `Err.Number`. 2) *What is `Resume`?* Retry the failing line.
**Common mistakes:** `On Error Resume Next` at the top of the whole macro; no clean-up so Excel is left with screen updating off.

### Q17 ⭐ 🟡 A macro takes five minutes to run on 50,000 rows. How would you speed it up?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowledge of the main VBA speed levers.
**Say this in the interview:** "First I turn off screen updating and set calculation to manual, then I stop touching cells one at a time: read the column into an array, loop in memory, write results back in one go. I also remove Select and Activate. I time before and after."
**Explain simply:**
- Microsoft: "Turn screen updating off to speed up your macro code... Remember to set the ScreenUpdating property back to True" (Microsoft Learn, "Application.ScreenUpdating property (Excel)").
- Manual calculation, events off (from memory): stops formulas recalculating after every write.
- Each cell read/write has an overhead; one block read + one block write replaces tens of thousands of calls (from memory). I did not time anything here, so I cannot quote a speed-up.
- Avoid `.Select`, use `With` blocks, avoid formulas copied per row if one array formula does it.
**Example:** The Q14 loop done on 50,000 rows: cell-by-cell is 50,000 reads and 50,000 writes; array version is 1 read and 1 write. Results are identical (checked by the logic in Q14).
**Formula / Steps:** VBA (not run here):
```vba
Option Explicit
Sub FlagFast()
    Dim ws As Worksheet, data As Variant, out() As Variant
    Dim r As Long, n As Long, cutoff As Date, calc As XlCalculation
    Set ws = ThisWorkbook.Worksheets("Employees")
    n = Application.Max(ws.Cells(ws.Rows.Count, "C").End(xlUp).Row, 3)
    cutoff = DateAdd("yyyy", -1, Date)
    calc = Application.Calculation
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
    On Error GoTo Cleanup
    data = ws.Range("C2:C" & n).Value
    ReDim out(1 To UBound(data, 1), 1 To 1)
    For r = 1 To UBound(data, 1)
        If IsEmpty(data(r, 1)) Then
            out(r, 1) = ""
        ElseIf VarType(data(r, 1)) <> vbDate Then
            out(r, 1) = "Check date"
        ElseIf data(r, 1) > cutoff Then
            out(r, 1) = "Under 1 yr"
        Else
            out(r, 1) = "OK"
        End If
    Next r
    ws.Range("D2").Resize(UBound(out, 1), 1).Value = out
Cleanup:
    Application.Calculation = calc
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    If Err.Number <> 0 Then MsgBox Err.Description
End Sub
```
**Alternative:** Replace the macro with a formula, Power Query, or a single `Range.Value = ` assignment where possible.
**Version note:** All desktop versions.
**Edge cases:** Reading a one-cell range returns a single value, not an array, so the code reads at least 2 cells; always restore settings even on error.
**Likely follow-ups:** 1) *Where is the time spent?* Usually in cell-by-cell access. 2) *How to measure?* `Timer` before and after.
**Common mistakes:** Turning off ScreenUpdating but not restoring it; leaving Calculation manual.

### Q18 ⭐ 🟡 What is the COPILOT function in Excel, and how is it different from functions such as SUM or IF?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of the function's status and the difference between rule-based and AI-generated results.
**Say this in the interview:** "The COPILOT function let you write a prompt in a cell, such as =COPILOT("Summarize this feedback", A2:A20). But Microsoft has retired it: its page says it is no longer available from 14 September 2026, and the Copilot pane replaces it. So today I would use the pane."
**Explain simply:**
- Microsoft's page ("COPILOT Function") shows examples of the form `=COPILOT("Summarize this feedback", A2:A20)`. It was a preview feature for Frontier/Insider users.
- As of 14 September 2026 the function "is no longer available"; old cells keep cached values but return #NAME? when they recalculate (same page).
- Microsoft's replacement: Copilot in Excel from the icon in the lower-right corner, asking in plain language (same page).
- Difference from SUM/IF: SUM and IF are deterministic (same input, same answer, offline, auditable). An AI function is probabilistic, needs a service, and could vary (from memory, reasoned, not on the page).
**Example:** `=SUM(B2:B9)` always gives 354,000 on the Q6 sheet. A prompt like "classify each comment" could give different wording tomorrow.
**Formula / Steps:** Today (22 Oct 2026) the formula is not usable (not run here). Instead: open the Copilot pane and ask: "Classify the comments in A2:A20 into themes and put the result in column B."
**Alternative:** Keyword formulas, e.g. `=IF(ISNUMBER(SEARCH("manager",A2)),"Manager","Other")`, which are repeatable.
**Version note:** Page says it applied to Microsoft 365 apps (Windows, Mac, web, iPhone); no licence terms stated on the page. Premise note: if the question assumes it is still available, that is out of date.
**Edge cases:** Workbooks containing it will show #NAME? after recalculation; convert to values before relying on it.
**Likely follow-ups:** 1) *Why did Microsoft retire it?* The page doesn't say. 2) *What replaces it?* The Copilot pane.
**Common mistakes:** Building a report on the function now; calling it deterministic.

### Q19 ⭐ 🟡 What data privacy risks should you consider when using AI tools on employee or payroll data?
**Asked at:** commonly asked (no company-specific report found); especially relevant to HR-to-analytics candidates.
**What the interviewer is checking:** Judgement: you protect personal data and follow policy.
**Say this in the interview:** "Employee and payroll data is personal and sensitive. Before using any AI tool I check company policy, use only approved tools, remove names and IDs where possible, share the minimum data, and make sure outputs do not expose individuals."
**Explain simply:**
- Risks: data leaving the company to a third-party tool; staff seeing data they should not; AI output or chat history exposing salaries; wrong AI output affecting someone's pay or career.
- Microsoft states that changes Copilot saves to a workbook can be seen by anyone with access to the file, including people in a coauthoring session, and that Copilot in Excel is a Copilot Chat tool that can't be turned off independently (Microsoft Support, "Frequently asked questions about Copilot in Excel").
- Microsoft also advises avoiding Copilot for decisions in sensitive areas (same page); Google notes Gemini conversation history can be lost on reload (Google Docs Editors Help, "Collaborate with Gemini in Google Sheets"), which affects what is recorded.
- India's Digital Personal Data Protection Act 2023 is relevant (from memory, unverified; check with legal/IT).
- Mitigation: anonymise (employee code instead of name), aggregate, use company-approved accounts, get approval, document usage.
**Example:** Instead of uploading 2,000 rows with names and salaries, share department and salary band with a random ID, or ask the AI for formula help using 5 dummy rows.
**Formula / Steps:** Pre-flight checklist: 1) Is the tool approved? 2) Do I need individual-level data? 3) Remove names/IDs/contact details 4) Use dummy rows to test the prompt 5) Keep an audit note.
**Alternative:** Use formulas or Power Query locally with no AI.
**Version note:** Data-handling terms differ by plan and tenant; check your company's admin documentation.
**Edge cases:** Free consumer AI tools versus company-managed accounts handle data differently (from memory, unverified).
**Likely follow-ups:** 1) *What data is most sensitive?* Pay, performance, health, disciplinary. 2) *Can anonymised data be re-identified?* Yes if small groups are unique.
**Common mistakes:** Pasting full payroll into a public chatbot; thinking removing names alone is enough.

### Q20 ⭐ 🟡 When would you use Copilot, and when would you use a formula, a PivotTable or Power Query instead?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Tool-selection judgement.
**Say this in the interview:** "Copilot for exploration and first drafts. Formulas for repeatable calculations I need to audit. PivotTables for quick summaries I will refresh. Power Query for monthly cleaning and combining. For anything going to a manager, I choose the method I can verify and repeat."
**Explain simply:**
- Copilot: unfamiliar data, ideas, drafting a formula, summarising text; results need checking (Microsoft Support FAQ).
- Formula: one clear rule, must update automatically and be auditable.
- PivotTable: grouping/counting/summing quickly by category.
- Power Query: same messy file every month; records the steps and refreshes (see Part 7).
**Example:** Attrition by department (Q5 sheet): PivotTable or COUNTIFS gives 33.3%, 50%, 0% each month by refresh. Copilot is good to ask "what looks unusual?" first. Merging 12 monthly attendance files: Power Query.
**Formula / Steps:** Decision rule: repeatable monthly? Use Power Query/PivotTable/formula. One-off exploration? Copilot, then verify. Sensitive data? No AI unless approved.
**Alternative:** Combine: ask Copilot to draft a formula, then paste and test it yourself.
**Version note:** Copilot needs a licence (Q12); formulas, PivotTables and Power Query (built in from Excel 2016, from memory here; see the Power Query answers in Part 7) work without one.
**Edge cases:** Copilot results can change on rerun; formulas do not.
**Likely follow-ups:** 1) *Which is fastest?* Copilot to start, PivotTable to summarise. 2) *Which is most auditable?* Formulas.
**Common mistakes:** Using AI for numbers that must be exact; rebuilding by hand what Power Query could refresh.

### Q21 ⭐ 🟡 Write a prompt you would give Copilot or Gemini to classify 500 employee feedback comments into themes.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you write a clear, constrained prompt and plan to check it?
**Say this in the interview:** "I give the tool a role, the data location, a fixed list of themes, one label per comment, the output layout, and a rule for unclear comments. Then I test on a sample of 30 and spot-check before trusting all 500."
**Explain simply:**
- State the input: "Column B, rows 2-501 (500 comments)".
- Give a closed list of themes, so labels stay consistent.
- Ask for one theme per comment plus a confidence note, and "Unclear" instead of guessing.
- Keep the output in a new column, never overwrite the originals; no names in the data (Q19).
- Verify: review a random sample, count themes, compare with a keyword check.
**Example:** Prompt:
"Act as an HR analyst. The sheet has 500 employee comments in column B (B2:B501). Classify each into exactly one theme from this list: Manager/Leadership, Pay & Benefits, Workload & Work-life balance, Career Growth, Culture & Team, Tools & Process, Other. If a comment is unclear or mixed, label 'Unclear' rather than guessing. Put the theme in column C and a short reason (max 10 words) in column D. Do not change column B. Afterwards give a count of comments per theme."
Illustrative expected output (hand-written, not a tool output):
| Comment | Theme |
|---|---|
| "My manager never gives feedback" | Manager/Leadership |
| "Salary is below market" | Pay & Benefits |
| "Too many late-night calls" | Workload & Work-life balance |

**Formula / Steps:** 1) Remove names/IDs 2) Test on 30 rows 3) Fix the theme list 4) Run on 500 5) Sample 10% (50 rows), count mistakes 6) Pivot the themes.
**Alternative:** Keyword formula `=IF(ISNUMBER(SEARCH("salary",B2)),"Pay & Benefits","Other")` as a transparent baseline to compare against.
**Version note:** Copilot in Excel or Gemini in Sheets need eligible plans (Q12, Q11); Copilot function is retired (Q18).
**Edge cases:** Comments with several themes, sarcasm, other languages (Microsoft says Copilot was trained predominantly on English sources).
**Likely follow-ups:** 1) *What if results change on rerun?* Fix the labels and save the output as values. 2) *How many to check?* A random sample, for example 50 of 500; no accuracy figure is claimed here.
**Common mistakes:** Open-ended prompt with no list; no sampling check; sending names with the comments.

