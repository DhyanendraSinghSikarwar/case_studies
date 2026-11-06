# Book 1 — Excel | Part 12: How to Develop Excel Skills 🟢🟡

**Target:** 20 questions | **Actual:** 24 questions
**Scope:** learning-journey interview questions plus the full zero-to-job-ready skill-development plan (roadmap, daily plan, free resources, datasets, mini-projects, self-check tests).

## Questions

### Q1 ⭐⭐⭐ 🟢 How did you learn Excel, and how long did it take you?
**Asked at:** commonly asked (no company-specific report found). Learning-journey questions are a standard opener in entry-level analyst interviews; no source reports them at a named company.
**What the interviewer is checking:** Honesty about your path, whether you practised on real problems, and whether the timeline is believable.
**Say this in the interview:** "I used Excel for basic HR lists for years, but I only learned it properly over the last twelve weeks, about two hours a day. I went in order: basics, IF and COUNTIFS, lookups, data cleaning, pivot tables, charts, then Power Query. I practised on my own HR sheets and finished two small projects. I am comfortable with day-to-day MIS work and still learning Power Pivot and dynamic arrays."
**Explain simply:**
- Give a time frame you can defend. "12 weeks, about 2 hours a day, 6 days a week" is the roadmap in the "Skill-development plan" section at the end of this part. If your real timeline differs, say your real one.
- Name the order so it sounds structured, not random (reasons in Q13).
- Name one thing you built and one thing you are still weak at. Admitting a gap is safer than being caught overstating.
- "How long" is not "how good". Add one proof point: a self-test score (Q22) or a project file.
**Example:** "Weeks 1-3: sorting, filters, IF, COUNTIFS, SUMIFS on an attendance sheet. Weeks 4-5: VLOOKUP and INDEX-MATCH, then cleaning messy data. Weeks 6-8: pivot tables, charts, conditional formatting. Weeks 9-12: dynamic arrays, Power Query, an HR attrition workbook and timed mock tests."
**Weak vs strong:**
- Weak: "I watched some YouTube videos and tried a few formulas." (no order, no time frame, no proof)
- Strong: the answer above: a time frame, an order, a project, one honest gap.
**Version note:** Not version-specific; but say which version you practised on (Q3), because XLOOKUP and UNIQUE exist only in newer Excel.
**Likely follow-ups:**
- *What was the hardest part?* See Q6.
- *Show me what you can do now.* Be ready to build a SUMIFS and a pivot table live.
**Common mistakes:** Claiming "5 years of advanced Excel" when you have 3 months; saying you only watched videos; listing ten sites you opened once.

### Q2 ⭐⭐⭐ 🟢 How would you rate yourself in Excel out of 10, and why?
**Asked at:** commonly asked (no company-specific report found). A vendor guide, "How proficient are you in Excel?" (thebricks.com, Feb 2025 per search snippet, read in full), advises backing the level with examples and avoiding labels like "advanced"; it is one blog's advice, not a company report.
**What the interviewer is checking:** Self-awareness. A calibrated number with evidence beats a high number with no proof.
**Say this in the interview:** "About 6 out of 10 for a fresher. I can use IF, COUNTIFS, SUMIFS, VLOOKUP and INDEX-MATCH, build pivot tables with slicers and clean messy data without notes. I am slower on Power Pivot, dynamic arrays and VBA, and I am working on them. I would rather give you an honest 6 I can prove than a 9 I cannot."
**Explain simply:**
- Rate against a visible ladder (this ladder is my own teaching scale, not an industry standard):
  - 3-4: formatting, sorting, filters, SUM/AVERAGE, simple IF.
  - 5-6: COUNTIFS/SUMIFS, lookups, pivot tables, text and date functions, cleaning.
  - 7: Power Query, dynamic arrays (FILTER, UNIQUE), dashboards, error handling.
  - 8-9: Power Pivot data models, VBA, big-file performance, designing reusable models.
- Back the number with evidence: "I scored 7 of 8 on my own timed test" (Q22).
- Never say 9 or 10 in an entry-level interview; the next question will be a hard one.
**Example:** After Week 11 of the roadmap with Quiz 6 passed, "6 to 7 out of 10" is defensible. After Week 5, say "5".
**Weak vs strong:**
- Weak: "10/10, I know everything" or "maybe 2, I am just a beginner."
- Strong: a middle number, three things you can do, two things you are improving.
**Version note:** Not version-specific.
**Likely follow-ups:**
- *What would make it an 8?* Power Pivot models, VBA and a year of real work files.
- *Prove it.* Offer to build a pivot table or a lookup right now.
**Common mistakes:** Rating yourself 9 and freezing on a lookup question; refusing to give a number; giving a number with no evidence.

### Q3 ⭐⭐⭐ 🟢 Which version of Excel do you use (2016, 2019, 2021 or Microsoft 365), and does the version matter for your work?
**Asked at:** commonly asked (no company-specific report found). An Excel interview-question page from igmguru (training vendor, updated September 2026 per the page, first 100,000 of 114,839 characters read) asks how Excel 365 differs from older versions for analysts.
**What the interviewer is checking:** Whether you know which functions exist in which version, and whether you can work on the version the company actually has.
**Say this in the interview:** "I practise on Microsoft 365, so I have the newer functions like XLOOKUP, UNIQUE and FILTER. But many companies still run older versions, so I also know the classic way: INDEX-MATCH instead of XLOOKUP, and a pivot table instead of UNIQUE. I check the version before I send a file and I do not use a function my reader cannot open."
**Explain simply:**
- Microsoft 365 is the subscription version that keeps getting new functions. 2016, 2019, 2021 and 2024 are one-time-purchase versions frozen at release.
- Microsoft Support, "XLOOKUP function": a note says "XLOOKUP is not available in Excel 2016 and Excel 2019"; the page's "Applies To" list names 2016 and 2019 too, so the page contradicts itself. It also lists Excel for Microsoft 365 and Excel 2021.
- Microsoft Support, "UNIQUE function": the "Applies To" list names Microsoft 365, Excel 2024 and Excel 2021, and does not list 2016 or 2019 (the page has no availability sentence). FILTER, SORT and LET are not on a page I fetched: from memory, unverified, same group as UNIQUE.
- Power Query being built into Excel 2016 and later is from memory, unverified (I could not fetch a Microsoft page that confirms it).
- Reported, unverified (secondary sites in search snippets, Microsoft page returned 404): support for Excel 2016 and 2019 ended on 14 October 2025.
- If a file with XLOOKUP is opened in an older version, the cell shows `#NAME?`.
**Example:** Same job, "salary of employee 7", two ways: new `=XLOOKUP(7,A2:A11,F2:F11)` or classic INDEX-MATCH that works everywhere.
**Sample sheet:** (employee list used in the self-test kit; rows 2-11, columns A to G)

| | A emp_id | B name | C dept | D hire_date | E exit_date | F salary | G overtime |
|---|---|---|---|---|---|---|---|
| 5 | 4 | Dev | Sales | 2018-07-01 | | 110000 | N |
| 6 | 5 | Esha | Sales | 2020-03-05 | | 60000 | Y |
| 7 | 6 | Farhan | Sales | 2021-08-20 | 2024-02-29 | 58000 | Y |
| 8 | 7 | Gita | Sales | 2023-02-01 | | 57000 | N |
| 9 | 8 | Hari | Sales | 2023-05-15 | 2024-06-30 | 59000 | Y |

(Rows 2-4 and 10-11 of the full 10-row sheet are in Q22; the formulas below look at all rows 2 to 11.)
**Formula / Steps:** `=INDEX(F2:F11,MATCH(7,A2:A11,0))` (works in every version). Check your version: File > Account > About Excel.
**Alternative:** `=XLOOKUP(7,A2:A11,F2:F11)` (365/2021/2024). Not run here: LibreOffice 24.2 does not support XLOOKUP; the expected value is the same 57000.
**Result:** INDEX-MATCH returned 57000 (run in LibreOffice 24.2 on the full 10-row sheet).
**Version note:** See the sourced bullets above. Google Sheets has XLOOKUP, FILTER and UNIQUE: from memory, unverified.
**Edge cases:** If the ID is missing, both return `#N/A` (XLOOKUP can take a fifth argument for "not found"); IDs stored as text will not match numbers.
**Likely follow-ups:**
- *Does version matter for pivot tables?* Basic pivots work in all of them.
- *Is Excel 365 needed in 2026?* Useful, not essential; know the classic route too.
**Common mistakes:** Sending an XLOOKUP file to someone on Excel 2016; saying "the version does not matter".

### Q4 ⭐⭐⭐ 🟢 You come from HR with no technical background. How did you learn Excel?
**Asked at:** commonly asked (no company-specific report found). Common for career-switchers; the HR background is an asset if you frame it.
**What the interviewer is checking:** Whether the switch is genuine and sustained, and whether you can turn HR knowledge into data work.
**Say this in the interview:** "In HR I already lived in Excel: attendance, payroll and attrition sheets. But I was copying and pasting. So I took twelve weeks to learn it properly: COUNTIFS and SUMIFS, lookups, pivot tables and Power Query. I rebuilt my own monthly attrition report with formulas instead of manual counting. I know what the numbers mean in HR; now I can also produce them faster and with fewer errors."
**Explain simply:**
- Start from a real pain point: a monthly report that took hours by hand.
- Say what you did: structured plan, daily time, free resources (Q9), one project (Q5).
- Link to HR metrics you already understand: attrition rate, headcount, tenure, overtime, payroll cost.
- Be clear on your level: experienced in the business context, newer in analytics tools.
**Example:** "Counting exits by department used to take me an hour. With COUNTIFS it takes seconds: Sales had 2 exits out of 5 people, 40 percent." (This is the sample data in Q22.)
**Weak vs strong:**
- Weak: "I have no technical background but I am a fast learner."
- Strong: the pain point, the 12-week plan, the project with numbers, the honest gap.
**Version note:** Not version-specific.
**Likely follow-ups:**
- *Why leave HR?* Keep it positive: you want to work with the data you currently only report on.
- *Do you need training from us?* "On your files and tools, yes; on core Excel, no."
**Common mistakes:** Apologising for your background; hiding HR experience; claiming you were an analyst when you were not.

### Q5 ⭐⭐⭐ 🟡 Walk me through an Excel report or workbook you built from start to finish.
**Asked at:** commonly asked (no company-specific report found). Candidate reports on AmbitionBox/Glassdoor (search snippets only, about 4 to 6 anecdotes, e.g. a vivo MIS Executive report from Aug 2023) describe Excel tests of about 30 minutes and one reviewer asked to explain every formula used in the test. Anecdotal.
**What the interviewer is checking:** That you built it yourself and can explain every formula, and whether you think about checks and limits.
**Say this in the interview:** "I built a monthly HR attrition workbook. Question: which department loses people fastest? I cleaned the employee list, used COUNTIFS for headcount and exits per department, computed attrition percentage, and checked that the department totals add up to the full headcount. Sales was highest at 40 percent. It is a small practice file, so I trust the method more than the conclusion."
**Explain simply:** Five steps, 60 to 90 seconds:
- Business question in one sentence.
- Data: where it came from, how many rows, how you cleaned it.
- Method: the two or three formulas that matter and why.
- Result with numbers, and the check that proves it.
- Limitation and next step (for example, make it a pivot table or refresh with Power Query).
**Example:** Ten employees, three departments. Sales 5 people and 2 exits, HR 3 and 1, IT 2 and 0; overall 3 of 10 = 30 percent.
**Sample sheet:** summary block (columns L to P), built from the Q22 employee list (dept in C, exit date in E, salary in F)

| | L dept | M headcount | N exits | O attrition | P avg_salary |
|---|---|---|---|---|---|
| 2 | HR | 3 | 1 | 33.3% | 63,333 |
| 3 | Sales | 5 | 2 | 40.0% | 68,800 |
| 4 | IT | 2 | 0 | 0.0% | 112,500 |
| 5 | Total | 10 | 3 | 30.0% | |

**Formula / Steps:**
1. M2: `=COUNTIF($C$2:$C$11,L2)`
2. N2: `=COUNTIFS($C$2:$C$11,L2,$E$2:$E$11,"<>")` (exit date not empty means the person left)
3. O2: `=N2/M2`, then Home > Number > Percentage.
4. P2: `=AVERAGEIF($C$2:$C$11,L2,$F$2:$F$11)`
5. Check cell: `=ROWS(A2:A11)-M5` should be 0.
**Alternative:** A pivot table (Insert > PivotTable) with dept in Rows and Count of emp_id in Values; the pivot cannot show the exit-date condition without a helper column. Not run here (pivot tables cannot run headless).
**Result:** Values above came from running the formulas in LibreOffice 24.2: HR 3/1/0.3333/63333.33, Sales 5/2/0.4/68800, IT 2/0/0/112500, total 10/3/0.3, check cell M6 = 0.
**Version note:** All formulas work in every Excel version and Google Sheets (COUNTIFS and AVERAGEIF are Excel 2007+: from memory, unverified).
**Edge cases:** Exit dates typed as text or a space instead of a blank would break `"<>"`; a department with no exits and AVERAGEIFS on leavers returns `#DIV/0!` (wrap in IFERROR).
**Likely follow-ups:**
- *Why COUNTIFS, not a pivot?* Formulas update with the row and stay visible for audit; pivots need a refresh.
- *How do you know it is right?* Totals reconcile (Q14).
**Common mistakes:** Not being able to explain your own formula; showing a polished file with no checks; hard-coding numbers instead of formulas.

### Q6 ⭐⭐⭐ 🟡 Which Excel topic did you find hardest, and how did you overcome it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Honesty, learning method and resilience; a real topic, not a fake weakness.
**Say this in the interview:** "Lookups were hard at first, especially why VLOOKUP gave `#N/A` when the ID was clearly there. I traced it to a text-versus-number mismatch and trailing spaces. I fixed it by learning TRIM and VALUE, kept a mistakes log, and redid the failed exercises two days later. Now I switch to INDEX-MATCH when the lookup column is not on the left."
**Explain simply:**
- Pick a topic you really struggled with. Common honest choices: lookups, pivot table field layout, date arithmetic, absolute references (`$`).
- Use three beats: what went wrong, what you did (smaller examples, a mistakes log, redoing it), proof it works now.
- Avoid "perfectionism" or "no hard topic".
- Absolute reference means a cell address with `$` that does not move when you copy the formula.
**Example:** "In Week 4 my employee-ID lookup failed on 3 of 10 rows. Cause: IDs imported from the HR system were text. After cleaning, 10 of 10 matched."
**Weak vs strong:**
- Weak: "Nothing was really hard." or "VBA is hard" (when you never tried).
- Strong: a real topic, the cause, the fix, the evidence.
**Version note:** Not version-specific.
**Likely follow-ups:**
- *What would you still struggle with?* Power Pivot data models and VBA.
- *How do you avoid the `#N/A` now?* Check data types and use `0` or `FALSE` for exact match.
**Common mistakes:** Naming a topic and then showing you cannot explain it; blaming the tool; no concrete fix.

### Q7 ⭐⭐ 🟢 Which Excel functions and features do you use most often, and which have you not tried yet?
**Asked at:** commonly asked (no company-specific report found). Candidate reports describe MIS tests with VLOOKUP, HLOOKUP, SUMIFS, COUNTIFS and pivots (about 4 to 6 anecdotes, search snippets).
**What the interviewer is checking:** Real daily toolkit, plus self-awareness about gaps.
**Say this in the interview:** "Daily: filters, COUNTIFS, SUMIFS, INDEX-MATCH or VLOOKUP, IF, pivot tables, and TRIM for cleaning. Weekly: Power Query and charts. Not tried yet: VBA macros and Power Pivot measures; they are on my next-quarter plan."
**Explain simply:**
- Split your list into daily, sometimes and not yet.
- Market context from the project's own sample of 186 India analyst job postings (not random, about plus or minus 7 points): Excel appears in 60 percent, dashboards/reporting in 75 percent, VBA/macros in 13 percent. So VBA is a "later" skill.
- Pair each tool with a use: "SUMIFS for payroll by department".
**Example:** Monthly HR pack: COUNTIFS for headcount, SUMIFS for payroll cost, pivot for attrition by month, a chart for the exit trend.
**Weak vs strong:**
- Weak: "SUM and AVERAGE mostly."
- Strong: a ranked list with a use for each, and one honest "not yet".
**Version note:** Say which of your tools need Microsoft 365 or 2021 (XLOOKUP, UNIQUE, FILTER: Q3).
**Likely follow-ups:**
- *Why not VBA yet?* Only 13 percent of sampled postings asked for it; formulas and pivots first.
- *Favourite function?* Pick one and explain a real use.
**Common mistakes:** Listing 20 functions; naming functions you cannot explain.

### Q8 ⭐⭐ 🟢 How do you learn an Excel function or feature you have never used before?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can learn independently on the job.
**Say this in the interview:** "I read the official help for the syntax, build a tiny test with five rows I can check by eye, then break it on purpose with blanks and wrong types. Only then do I use it on real data. Last month I learned TEXTJOIN this way."
**Explain simply:**
- Steps: (1) Read the function help (Microsoft Support, or the formula tooltip). (2) Tiny sheet with a known answer. (3) Change one thing and predict the result. (4) Test edge cases. (5) Write a one-line note in your own cheat sheet.
- Use the Function Wizard (the fx button) to see each argument's meaning.
- Tiny test first, real data second.
**Example:** Learning TEXTJOIN: three names in A1:A3 and `=TEXTJOIN(", ",TRUE,A1:A3)`.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Asha | |
| 2 | Dev | |
| 3 | Isha | |
| 4 | (blank) | |

**Formula / Steps:** `=TEXTJOIN(", ",TRUE,A1:A4)`; `TRUE` means "ignore empty cells".
**Alternative:** `=A1&", "&A2&", "&A3` (manual, breaks when rows change).
**Result:** `Asha, Dev, Isha` (run in LibreOffice 24.2; the blank in A4 is skipped). With `FALSE` the run returned `Asha, Dev, Isha, ` (trailing comma and space).
**Version note:** Microsoft Support, "TEXTJOIN function" (fetched 2026-10-22): its Applies To list names Microsoft 365, Excel 2024, Excel 2021 and Excel 2019, and it says the feature is available "if you have Office 2019, or if you have a Microsoft 365 subscription". Excel 2016 is not listed, so avoid TEXTJOIN there. Run here with the `_xlfn.` prefix that file-writing tools need; in the Excel cell you just type `=TEXTJOIN(...)`.
**Edge cases:** With `FALSE` instead of `TRUE`, an empty cell leaves a trailing `, `.
**Likely follow-ups:**
- *Where do you look it up?* Microsoft Support function pages and Exceljet (Q9).
- *Do you use AI?* Yes, to explain, then I verify (Q16).
**Common mistakes:** Pasting a formula from the internet unchanged; testing only on the perfect case.

### Q9 ⭐⭐ 🟢 Which free resources would you recommend to a beginner learning Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know good sources and can match them to a stage; no brand hype.
**Say this in the interview:** "Microsoft's own Excel help for exact function syntax, Exceljet for short formula and shortcut explanations, and Google's Sheets training if someone wants to learn Sheets. For practice I use free HR datasets from TrumpExcel and AIHR. I check what is free before recommending, because some sites mix free and paid content."
**Explain simply:** What each page itself stated when checked on 2026-10-21 (research/Book01_Part12_sources.md):

| Resource | What was observed | Price/free status |
|---|---|---|
| Microsoft Support Excel hub (support.microsoft.com/en-us/excel) | Written help articles; links to training on Microsoft Learn | Price not stated on the page |
| Microsoft "Excel video training" page | The fetched page was a help hub, not a video library | Free video courses: unverified; do not claim |
| Exceljet (exceljet.net) | "We offer free resources and paid training"; formulas, shortcuts, articles; videos page lists core formulas, pivots, charts, dynamic arrays | Free vs paid per item: unverified |
| Google Sheets training and help (support.google.com/a/users/answer/9282959) | Lessons, a cheat sheet, "Switch from Microsoft Excel to Sheets" | Price not stated |
| TrumpExcel sample data | "15 Free Datasets", 1,000 rows each, includes an Employee HR Records set | Free per title; licence unverified |
| AIHR, 9 HR datasets | 8 of 9 free (some may need a Kaggle sign-in); one needs a paid AIHR course | Licences unverified |

- Chandoo.org blocked our fetch (HTTP 403), so I do not recommend it by name. YouTube, Coursera, Udemy and LinkedIn Learning were not checked.
**Example:** Week 4 (lookups): Microsoft Support page for VLOOKUP for syntax, an Exceljet example, then 10 lookups on the TrumpExcel HR file.
**Weak vs strong:**
- Weak: "YouTube and Google."
- Strong: two or three named sources, what each is for, and a note on what is free.
**Version note:** Sources describe whichever version they were written for; check function availability (Q3).
**Likely follow-ups:**
- *Paid or free?* Free is enough to become job-ready; certification is optional (Q19).
- *One source you would skip?* Anything with no worked example.
**Common mistakes:** Saying "all free" without checking; collecting resources instead of practising.

### Q10 ⭐⭐ 🟢 Which practice datasets have you worked with in Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you practised on realistic data and can say what you found in it.
**Say this in the interview:** "I started with a small HR sheet I built myself, ten employees with hire date, exit date and salary, so I could check every answer by hand. Then I used a free 1,000-row employee HR records file from TrumpExcel, and a public HR attrition dataset for a portfolio project. I would only name datasets I really opened."
**Explain simply:**
- Stage 1: self-made 10-20 rows. You know the true answer, so mistakes show up.
- Stage 2: a free 1,000-row practice set for lookups, pivots and cleaning (TrumpExcel "15 Free Datasets", includes Employee HR Records; licence unverified).
- Stage 3: a public HR set for a project. AIHR's page lists 9 HR datasets (8 free; one needs a paid course; licences unverified). The IBM HR Analytics Attrition set is on Kaggle; I saw only the page title, so size, licence and login are unverified. It is a CSV, which opens in Excel.
- Always record the source and check the licence before publishing a portfolio (Q20).
**Example:** "10 rows by hand: Sales attrition 40 percent. Then 1,000 rows: same COUNTIFS pattern, faster than checking by eye."
**Weak vs strong:**
- Weak: "Kaggle datasets." (which one? what did you find?)
- Strong: two datasets, one finding each, how you verified.
**Version note:** CSV opens in any version; Data > From Text/CSV (Power Query) is from memory, unverified for Excel 2016 menus.
**Likely follow-ups:**
- *Real company data?* Never use confidential HR data in a portfolio.
- *How big?* Excel handles 1,048,576 rows by 16,384 columns per worksheet (Microsoft Support, "Excel specifications and limits", fetched 2026-10-22).
**Common mistakes:** Publishing real employee data; naming a famous dataset you never opened.

### Q11 ⭐⭐ 🟢 Have you used Google Sheets as well as Excel, and how did you pick it up?
**Asked at:** commonly asked (no company-specific report found). In the project's sample of 186 India analyst job postings, Google Sheets appeared in 8 percent (non-random, about plus or minus 7 points); Excel in 60 percent.
**What the interviewer is checking:** Flexibility: can you work in whichever spreadsheet the team uses?
**Say this in the interview:** "Yes. The core formulas are almost the same, so I picked Sheets up in a few days from Google's own training page, which has a cheat sheet and a guide for switching from Excel. The new things I learned were sharing and comments, and functions like QUERY and ARRAYFORMULA. I would not claim I am expert in Sheets; Excel is my main tool."
**Explain simply:**
- Google's training page (support.google.com/a/users/answer/9282959) lists lessons, a cheat sheet and "Switch from Microsoft Excel to Sheets"; it states no price.
- Same: SUM, IF, COUNTIFS, VLOOKUP, charts, pivot tables.
- Different (from memory, unverified): QUERY, IMPORTRANGE and ARRAYFORMULA exist in Sheets; no Power Query or VBA (Sheets uses Apps Script).
- Real-time co-editing is the main practical advantage.
**Example:** Export a Sheets attendance file as .xlsx, and your COUNTIFS formulas still work in Excel.
**Weak vs strong:**
- Weak: "Yes, it is the same as Excel."
- Strong: what is the same, two differences, one use.
**Version note:** Sheets updates continuously (no versions). Whether XLOOKUP, FILTER and UNIQUE exist in Sheets: from memory, unverified.
**Likely follow-ups:**
- *Which would you pick for a team?* Depends on files, size and tools in the company.
- *Can Sheets open .xlsx?* Yes, with some features lost: from memory, unverified.
**Common mistakes:** Claiming Sheets expertise from one afternoon; saying Excel macros will work in Sheets.

### Q12 ⭐⭐ 🟢 How much time do you spend practising Excel each day or week?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Consistency, and whether the number is believable.
**Say this in the interview:** "During my learning phase about two hours a day, six days a week. Now about forty-five minutes a day: one new exercise, one revision of yesterday's mistake, and I try to automate one real task from my current job. I treat Sunday as rest."
**Explain simply:**
- The daily plan in this book is 120 minutes: Learn 30, Guided practice 30, Problem solving 40, Review 20 (see the plan at the end of this part).
- Hours are my study-plan targets, not researched figures. Use your own real hours.
- Consistent 1 hour a day beats a weekend marathon.
**Example:** 6 days x 2 hours = 12 hours a week; 12 weeks = 144 hours. For comparison, Microsoft's MOS Excel Associate page suggests about 150 hours of instruction and practice (as shown on the page; see Q19).
**Weak vs strong:**
- Weak: "Whenever I get time."
- Strong: a schedule, a method, and what you do on busy days.
**Version note:** Not version-specific.
**Likely follow-ups:**
- *What if you are busy?* Fifteen minutes: redo one failed exercise.
- *Do you practise at work?* Automate one real task per week.
**Common mistakes:** Quoting 6 hours a day (not believable); no revision time.

### Q13 ⭐⭐ 🟡 In what order did you study Excel topics, and why that order?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand dependencies: what each topic builds on.
**Say this in the interview:** "Basics first because everything uses cell references. Then logical and counting functions, then lookups, then data cleaning, because lookups fail on dirty data. Then pivot tables and charts, because they need clean tables. Then advanced tools like dynamic arrays and Power Query, and MIS scenario practice. VBA and Copilot last."
**Explain simply:**
- Order and reason (mirrors the Book 1 parts): 1 Basics (cell references, filters, shortcuts) → 2 Core functions (IF, COUNTIFS, SUMIFS, text, dates) → 3 Lookups → 5 Data cleaning → 4 Pivot tables → 8 Charts and dashboards → 9 Conditional formatting, validation, Goal Seek → 6 Dynamic arrays → 7 Power Query/Power Pivot → 10 Scenario tasks → 11 VBA and Copilot.
- Cleaning before pivoting: one extra space ("Sales ") makes a pivot show two Sales groups.
- Dynamic arrays after the classic route, so you can work on any version.
**Example:** Learning pivots before cleaning: a pivot on 1,000 rows showed "HR" and "HR " separately and the attrition percentages looked wrong. After TRIM, one group.
**Weak vs strong:**
- Weak: "Whatever the video said."
- Strong: an order with a reason for each step.
**Version note:** Dynamic arrays (FILTER, UNIQUE) need 365/2021 or later (Q3).
**Likely follow-ups:**
- *Would you change it?* Move pivots earlier if the job is MIS reporting.
- *Where does Power BI fit?* After pivots and Power Query.
**Common mistakes:** Starting with macros or advanced functions; skipping cleaning.

### Q14 ⭐⭐ 🟡 How do you check that your own Excel work is correct when there is no answer key?
**Asked at:** commonly asked (no company-specific report found). Candidate MIS-test reports (anecdotes, search snippets) mention being asked to explain every formula, which is a check of understanding.
**What the interviewer is checking:** Quality habits: do you test, reconcile and look for traps before sending numbers?
**Say this in the interview:** "I check three ways: totals reconcile with an independent calculation, I count rows and look for duplicates and text-numbers, and I spot-check three rows by hand. Before I send, I compare a pivot table total with a SUMIFS total. If they differ, something is wrong in the data."
**Explain simply:**
- Reconcile: department totals must sum to the grand total.
- Data-type check: a number stored as text is ignored by SUM and gives a silently low total.
- Duplicate check: duplicate IDs inflate counts.
- Spot-check 3 random rows by hand; try extremes (smallest, largest, a blank).
**Example:** A payroll column with 5 rows should total 290,000, but SUM shows 230,000: one salary is text.
**Sample sheet:** A = id, B = salary (B3 is the text "60000"; ID 3 is repeated in rows 4 and 5)

| | A id | B salary |
|---|---|---|
| 2 | 1 | 50000 |
| 3 | 2 | "60000" (text) |
| 4 | 3 | 55000 |
| 5 | 3 | 55000 |
| 6 | 4 | 70000 |

**Formula / Steps:**
1. `=SUM(B2:B6)` vs `=SUMPRODUCT(VALUE(B2:B6))` (should be equal if all are numbers).
2. `=COUNT(B2:B6)` vs `=COUNTA(B2:B6)` (COUNT counts numbers only; they should match).
3. `=SUMPRODUCT(--ISTEXT(B2:B6))` counts text-numbers.
4. `=ROWS(A2:A6)-SUMPRODUCT(1/COUNTIF(A2:A6,A2:A6))` gives the number of extra duplicate rows.
**Alternative:** Home > Conditional Formatting > Highlight Cells Rules > Duplicate Values; Data > Remove Duplicates after copying the data aside. Green-triangle warnings flag text-numbers.
**Result:** (run in LibreOffice 24.2) SUM = 230000; SUMPRODUCT(VALUE) = 290000; COUNT = 4; COUNTA = 5; text cells = 1; extra duplicate rows = 1.
**Version note:** All of these work in every version. Excel and LibreOffice may treat text-to-number coercion differently in edge cases (from memory, unverified).
**Edge cases:** A number with a trailing space or a non-breaking space may fail VALUE too; clean first with TRIM and SUBSTITUTE.
**Likely follow-ups:**
- *Pivot vs formula?* Compare the two totals; they should match.
- *Why keep inputs separate?* So you can see what you typed versus calculated.
**Common mistakes:** Trusting a pivot without checking source types; not checking row counts after a lookup or import.

### Q15 ⭐⭐ 🟡 How would you prepare for a live Excel test in one week?
**Asked at:** commonly asked (no company-specific report found). Candidate reports (4 to 6 anecdotes, search snippets only) describe tests of about 30 minutes with VLOOKUP, HLOOKUP, SUMIFS, COUNTIFS and pivot tables; one Novartis report (March 2023, Glassdoor via interview_processes.md) mentions an Excel case study with pivots, rank and formulas. Anecdotal.
**What the interviewer is checking:** Whether you can prioritise and practise under time pressure.
**Say this in the interview:** "I would drill the likely topics first: SUMIFS, COUNTIFS, lookups, pivot tables, IF, and text and date cleaning. Two days practising each, then two timed 30-minute mock tests and a final review of my mistakes. During the test I speak my approach and check totals."
**Explain simply:** 7-day plan (these hours and targets are my study-plan targets, not researched figures):

| Day | Focus | Target |
|---|---|---|
| 1 | IF, COUNTIFS, SUMIFS, AVERAGEIFS | 15 exercises |
| 2 | VLOOKUP, INDEX-MATCH (and XLOOKUP if on 365) | 12 exercises |
| 3 | Pivot tables, slicers, grouping dates | 8 pivots |
| 4 | Cleaning: TRIM, Text to Columns, duplicates; text and dates | 10 exercises |
| 5 | Timed mock 1 (30 min) on the Q22 kit style | review misses |
| 6 | Charts, conditional formatting, shortcuts; Timed mock 2 | review misses |
| 7 | Rest, review mistakes log, set up files | none |

- In the test: read the question twice, sort/filter the data first, name your assumptions aloud.
**Example:** A 30-minute mock: 8 questions at under 4 minutes each; pass 6 of 8.
**Weak vs strong:**
- Weak: "I would practise a lot of formulas."
- Strong: a day-by-day plan, timed mocks, a mistakes review.
**Version note:** Ask which Excel version the test uses; avoid XLOOKUP, FILTER, UNIQUE if not confirmed (Q3).
**Likely follow-ups:**
- *What if you get stuck?* Say your approach, do the part you can, move on.
- *Keyboard shortcuts?* Learn five: Ctrl+Shift+L (filter), Ctrl+T (table), F4 (lock reference), Ctrl+Z, Ctrl+Arrow (from memory, unverified).
**Common mistakes:** Learning new features the last week; not practising under a timer.

### Q16 ⭐⭐ 🟡 How do you use AI assistants such as Copilot or ChatGPT to learn Excel without depending on them?
**Asked at:** commonly asked (no company-specific report found). In the project's sample of 186 India analyst job postings, GenAI/AI tools were named in 14 percent (non-random, about plus or minus 7 points).
**What the interviewer is checking:** Whether AI sharpens your skills or replaces them, and whether you verify outputs.
**Say this in the interview:** "I use AI as a tutor, not an answer machine. I first try the formula myself, then ask the AI to explain a function or critique mine. I never paste an AI formula into real work without testing it on five rows where I know the answer. On a live test I do it myself without AI."
**Explain simply:**
- Good uses: explain a formula in plain words; suggest edge cases; find why `#N/A` appears; generate practice questions.
- Rule: try first, ask second, verify third.
- AI can invent functions or make a wrong assumption about your columns. Test on a small known sheet.
- Never paste confidential employee data into a public AI tool.
- Copilot in Excel is a paid-plan feature in Microsoft 365: from memory, unverified (see Book 1 Part 11).
**Example:** AI suggests `=SUMIF(C:C,"Sales",F:F)`. I test on the Q22 sheet: expected Sales payroll 110000+60000+58000+57000+59000 = 344000, and I check the formula returns it.
**Weak vs strong:**
- Weak: "I ask ChatGPT for all my formulas."
- Strong: AI explains, I verify; I can do the task without it.
**Version note:** Copilot availability depends on the Microsoft plan: from memory, unverified.
**Likely follow-ups:**
- *What if AI is wrong?* Test on a tiny known sample; compare with a hand calculation.
- *Can AI replace Excel skill?* No; you must check its output.
**Common mistakes:** Sharing sensitive data; trusting output without testing; being unable to explain the formula.

### Q17 ⭐⭐ 🟡 Is Excel enough for a data analyst role, and what would you learn next?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand the market and have a sensible next step.
**Say this in the interview:** "Excel is enough to start, not to stay. In the sample of 186 India analyst postings the project collected, Excel appeared in 60 percent, SQL in 54 percent and dashboards or reporting in 75 percent. So after Excel I learn SQL, then Power BI. Excel stays my fast tool for small data and checking."
**Explain simply:**
- Figures are from the project's pooled sample of 186 India analyst job descriptions (non-random, about plus or minus 7 points; VBA/macros 13 percent, Google Sheets 8 percent, GenAI 14 percent). They show demand, not what you must know.
- Excel handles small to medium data, quick analysis and reporting. SQL is for pulling data from databases; Power BI or Tableau is for dashboards.
- Interview reports (project research, anecdotal) show Excel cases and SQL both appear; SQL is the most common technical constant in the profiles.
- Next steps, in order: SQL (Book 2), then Power BI (Book 4), then basic statistics.
**Example:** A 2-million-row employee log does not fit in one Excel sheet; load it from a database with SQL and summarise it in Excel or Power BI.
**Weak vs strong:**
- Weak: "Excel is enough for everything." or "Excel is outdated."
- Strong: where Excel stops, what comes next and why.
**Version note:** Not version-specific (the 60 percent is across JD samples).
**Likely follow-ups:**
- *When do you outgrow Excel?* When data is huge, needs repeatable pipelines or multi-user dashboards.
- *Python?* After SQL, for larger automation.
**Common mistakes:** Dismissing Excel; promising to learn five tools at once.

### Q18 ⭐⭐ 🟡 How do you keep your Excel skills current as new functions are added?
**Asked at:** commonly asked (no company-specific report found). The igmguru page (updated September 2026 per the page) asks whether Excel 365 knowledge is needed in 2026, so version awareness is a topic.
**What the interviewer is checking:** Whether you keep learning and know what is new without chasing hype.
**Say this in the interview:** "I check Microsoft Support's Excel pages for what is new, try each new function on a small test file and note which versions support it. I follow one or two Excel teaching sites. Before I use a new function in shared work, I check my colleagues' versions."
**Explain simply:**
- Routine: 30 minutes a week on one new function; check Microsoft's support page for its "Applies To" list; add it to your cheat sheet.
- Keep the old way too: INDEX-MATCH beside XLOOKUP, pivot beside UNIQUE.
- Microsoft 365 receives new functions over time; one-time versions do not (from memory, unverified).
**Example:** Learn `UNIQUE`: Microsoft Support lists 365, 2021 and 2024 as applicable; so for a team on Excel 2019, use a pivot table or Remove Duplicates.
**Weak vs strong:**
- Weak: "I read tech news."
- Strong: a weekly routine, a source, a test method, a version check.
**Version note:** See Q3 (sourced items).
**Likely follow-ups:**
- *Last thing you learned?* Name one, with a use.
- *Do you rewrite old files?* Only when it helps.
**Common mistakes:** Using new functions in files sent to older versions; chasing every new feature.

### Q19 ⭐ 🟢 Do Excel certifications help, and have you done any (for example Microsoft Office Specialist)?
**Asked at:** commonly asked (no company-specific report found). The project's JD research did not record Excel certification (including MOS) in the sample tallies; none was named as required.
**What the interviewer is checking:** Honesty about credentials and judgement about what proves skill.
**Say this in the interview:** "I have not taken the Microsoft Office Specialist exam. In the job descriptions the project sampled, no Excel certification was named as required. I invest the time in projects and timed practice, which show skill directly. If an employer asked for it, I would consider the exam." (Say this only if true; if you hold a certificate, say which and when.)
**Explain simply:**
- Microsoft Office Specialist: Excel Associate (Office 2019), page checked 2026-10-21: proctored, 50 minutes, renewal 60 months, about 150 hours of instruction and practice suggested, "No training available for this exam". It is a paid exam by implication: "Price based on the country or region". No amount stated here. I did not find an India price; a non-official article gave a figure I could not verify, so I do not quote one.
- Exam MO-200 outline as shown: worksheets, cells and ranges, tables, formulas and functions, charts. Power Query, pivot-based and dynamic-array skills did not appear in that outline.
- Value: helps a fresher with no experience; does not replace a project.
**Example:** A candidate with an MOS badge but no project may still fail a lookup question; a candidate with a portfolio can show work.
**Weak vs strong:**
- Weak: "Certifications are useless." or "I plan to get five."
- Strong: balanced, honest, tied to evidence.
**Version note:** The MOS page is based on Office 2019.
**Likely follow-ups:**
- *Would you do it?* If the employer values it.
- *Cost?* Depends on country; check Microsoft's page.
**Common mistakes:** Claiming a certificate you do not hold; quoting an unchecked price.

### Q20 ⭐ 🟢 Have you shared your Excel work publicly or kept a portfolio of it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Proof of work and judgement about privacy.
**Say this in the interview:** "I keep two small projects online: an HR attrition workbook and a sales analysis, with a README that states the question, the data source, the method and one limitation. I only use public or self-made data. I never share real employee data."
**Explain simply:**
- Portfolio = files a recruiter can open: .xlsx files and a short README on GitHub or a shared drive.
- Each project: question, data source and licence, steps, five findings with numbers, one limitation.
- Never publish confidential or personal data; use public datasets (Q10) or data you created, and check the licence.
- Remove hidden sheets, personal names and file-path metadata before sharing: File > Info > Inspect Workbook (from memory, unverified).
**Example:** README line: "Finding: Sales attrition 40 percent (2 of 5), HR 33.3 percent, IT 0 percent (self-made 10-row sample)."
**Weak vs strong:**
- Weak: "No, I only practised."
- Strong: two projects with a README and a sentence on privacy.
**Version note:** Share .xlsx; mention the Excel version used.
**Likely follow-ups:**
- *Show me one.* Have it open.
- *Which dataset?* Say the source and licence status.
**Common mistakes:** Uploading real company data; no README; broken links.

### Q21 ⭐ 🟡 How would you build an Excel portfolio project from a public HR dataset?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Your end-to-end method: question, cleaning, analysis, checks, story.
**Say this in the interview:** "I would pick a public HR attrition dataset, such as the IBM HR Analytics set on Kaggle (I have only seen its title, so I would check the licence), write the business question first, clean it, analyse with COUNTIFS and a pivot table, add two charts and write five findings with numbers and one limitation."
**Explain simply:**
- Steps: (1) one question; (2) download and copy the raw file aside; (3) clean (TRIM, types, duplicates); (4) analyse (COUNTIFS, AVERAGEIFS, pivot); (5) chart; (6) checks (Q14); (7) README with findings and limitations.
- The sample rows below are my own illustrative rows using IBM-style column names. They are not rows from the Kaggle file.
- Do not claim causes from one table; say "associated with".
**Example:** Question: "Which department has the highest attrition, and what is the average monthly income of leavers?"
**Sample sheet:** A = Department, B = Attrition, C = MonthlyIncome

| | A Department | B Attrition | C MonthlyIncome |
|---|---|---|---|
| 2 | Sales | Yes | 4200 |
| 3 | Sales | No | 6100 |
| 4 | Sales | No | 5500 |
| 5 | R&D | No | 7200 |
| 6 | R&D | Yes | 3900 |
| 7 | R&D | No | 8100 |
| 8 | R&D | No | 6500 |
| 9 | HR | No | 5200 |

**Formula / Steps:**
1. Attrition rate, F2: `=COUNTIFS($A$2:$A$9,E2,$B$2:$B$9,"Yes")/COUNTIF($A$2:$A$9,E2)` with E2 = Sales.
2. Average income of leavers, G2: `=AVERAGEIFS($C$2:$C$9,$A$2:$A$9,E2,$B$2:$B$9,"Yes")`.
3. Overall rate, F5: `=COUNTIF(B2:B9,"Yes")/COUNTA(B2:B9)`.
**Alternative:** Pivot table: Department in Rows, Attrition in Columns, Count in Values, "Show Values As > % of Row Total". Not run here.
**Result:** (run in LibreOffice 24.2) Sales 33.3% and 4200; R&D 25% and 3900; HR 0% and `#DIV/0!`; overall 25%. The HR `#DIV/0!` happens because HR has no leavers; wrap it: `=IFERROR(AVERAGEIFS(...),"no leavers")`.
**Version note:** All formulas work in every version; the pivot percentage option is from memory, unverified for old versions.
**Edge cases:** Attrition coded Yes/No versus 1/0; blanks; duplicate employee IDs; small groups make percentages unstable.
**Likely follow-ups:**
- *Is this causal?* No; it is descriptive.
- *Which chart?* Bar chart of attrition by department.
**Common mistakes:** Starting without a question; no raw copy; over-claiming; not citing the source.

### Q22 ⭐ 🟡 How would you set up a self-check test to measure your own Excel level?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you measure progress objectively instead of guessing.
**Say this in the interview:** "I made a small test kit: a ten-row HR sheet and eight questions with an answer key I wrote before solving. I solve it closed-book in 30 minutes, score it, log mistakes and retake it after a week on a fresh sheet. I pass at 7 of 8 and then I say my level with evidence."
**Explain simply:**
- Write the key before solving, and use a dataset you did not practise on for the real test.
- Time it (30 minutes is my target; MIS tests were reported at about 30 minutes in anecdotal reports).
- Pass marks are my study-plan targets, not researched figures. Rate yourself using Q2 only after passing.
**Example:** Score 7 of 8 with one error: T6 tenure used YEAR difference instead of DATEDIF.
**Sample sheet:** employee list in A1:G11 (the full sheet for all kit formulas)

| | A emp_id | B name | C dept | D hire_date | E exit_date | F salary | G overtime |
|---|---|---|---|---|---|---|---|
| 2 | 1 | Asha | HR | 2019-04-01 | | 90000 | N |
| 3 | 2 | Bala | HR | 2021-06-15 | | 52000 | N |
| 4 | 3 | Chitra | HR | 2022-01-10 | 2023-09-30 | 48000 | Y |
| 5 | 4 | Dev | Sales | 2018-07-01 | | 110000 | N |
| 6 | 5 | Esha | Sales | 2020-03-05 | | 60000 | Y |
| 7 | 6 | Farhan | Sales | 2021-08-20 | 2024-02-29 | 58000 | Y |
| 8 | 7 | Gita | Sales | 2023-02-01 | | 57000 | N |
| 9 | 8 | Hari | Sales | 2023-05-15 | 2024-06-30 | 59000 | Y |
| 10 | 9 | Isha | IT | 2017-11-01 | | 130000 | N |
| 11 | 10 | Jai | IT | 2020-09-14 | | 95000 | Y |

**Formula / Steps:** Eight questions (T1-T8; the formula key was run in full, see Result):

| Test | Question | Formula |
|---|---|---|
| T1 | Active employees (blank exit date) | `=COUNTBLANK(E2:E11)` |
| T2 | Monthly payroll of active staff | `=SUMIFS(F2:F11,E2:E11,"")` |
| T3 | Sales attrition rate | `=COUNTIFS(C2:C11,"Sales",E2:E11,"<>")/COUNTIF(C2:C11,"Sales")` |
| T4 | Average HR salary | `=AVERAGEIF(C2:C11,"HR",F2:F11)` |
| T5 | Salary of employee 7 (lookup) | `=INDEX(F2:F11,MATCH(7,A2:A11,0))` |
| T6 | Asha's full years of service at 1 Jan 2025 | `=DATEDIF(D2,DATE(2025,1,1),"Y")` |
| T7 | Second-highest salary | `=LARGE(F2:F11,2)` |
| T8 | Share of staff doing overtime | `=COUNTIF(G2:G11,"Y")/COUNTA(G2:G11)` |

**Alternative:** Tests T9+: a pivot of exits by department, and a dashboard question (not run here).
**Result:** (all eight run in LibreOffice 24.2) T1 = 7; T2 = 594000; T3 = 0.4 (40%); T4 = 63333.33; T5 = 57000; T6 = 5; T7 = 110000; T8 = 0.5 (50%).
**Version note:** All eight work in every Excel version and (from memory, unverified) Google Sheets; DATEDIF is an undocumented-in-menu function: from memory, unverified.
**Edge cases:** `COUNTBLANK` counts truly empty cells and also cells with `""`; cells containing a space would not be blank; SUMIFS with criteria `""` matched empty cells in LibreOffice (Excel behaviour: from memory, unverified).
**Likely follow-ups:**
- *How often?* Once per phase, always on fresh data.
- *Quizzes?* See "Skill-development plan", section F.
**Common mistakes:** Writing the key after solving; reusing the same sheet; ignoring the mistakes log.

### Q23 ⭐ 🟡 What is your plan to improve your Excel over the next three months?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you have a concrete, measurable plan.
**Say this in the interview:** "Month one: core formulas and lookups. Month two: data cleaning, pivot tables and charts. Month three: Power Query, dynamic arrays, a dashboard and timed mock tests. I will finish two portfolio projects and pass my self-test twice. Then SQL."
**Explain simply:**
- Three months = 12 weeks, about 2 hours a day, 6 days a week (see the roadmap at the end of this part).
- Milestones: Month 1 pass Quiz 2; Month 2 pass Quiz 4 and one project online; Month 3 pass the Final twice and finish a second project.
- The hours, exercise counts and pass marks are my study-plan targets, not researched figures. Adjust them to your time.
**Example:** "In Month 1 (weeks 1-4) I will complete 105 exercises: 20+30+30+25, from the roadmap table, and pass Quiz 1 and Quiz 2 at 6 of 8."
**Weak vs strong:**
- Weak: "I will keep practising."
- Strong: months, milestones, a measurable pass mark and a project.
**Version note:** Dynamic arrays in week 9 need 365 or 2021 or later; skip them if your tool does not have them (Q3).
**Likely follow-ups:**
- *What if you fall behind?* Repeat the week; retake the quiz after 3 days.
- *After three months?* SQL and Power BI.
**Common mistakes:** Plans with no checks; planning every topic in the first month.

### Q24 ⭐ 🟡 An HR colleague uses Excel only as a list maker. How would you coach them towards pivot tables and lookups?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Communication and teaching: can you explain simply and respect a non-technical colleague?
**Say this in the interview:** "I would start from a task they already do by hand, like counting leave days per department, and show it with one lookup and one pivot table. I would use their own file, make it small, let them click, and give them a one-page cheat sheet. I would not start with theory."
**Explain simply:**
- Teach in three small sessions (20 minutes each): (1) turn the list into a table and filter (Ctrl+T); (2) a lookup to add the department name from a code; (3) a pivot table for totals.
- Use their data, not abstract data. Let them drive the mouse.
- Explain terms: a lookup finds a value in a list by a key (like an employee ID); a pivot table summarises a list into totals without formulas.
- Celebrate the first time-saving.
**Example:** Attendance list with a department code and days present. Replace manual regrouping with a lookup and a total per department.
**Sample sheet:** A = emp_id, B = dept_code, C = days_present, D = dept_name (lookup), reference table E:F

| | A emp_id | B dept_code | C days_present | D dept_name | E code | F dept_name |
|---|---|---|---|---|---|---|
| 2 | 101 | S | 22 | Sales | H | HR |
| 3 | 102 | H | 20 | HR | S | Sales |
| 4 | 103 | S | 18 | Sales | I | IT |
| 5 | 104 | I | 21 | IT | | |
| 6 | 105 | H | 19 | HR | | |
| 7 | 106 | S | 23 | Sales | | |

**Formula / Steps:**
1. D2: `=VLOOKUP(B2,$E$2:$F$4,2,FALSE)` and fill down.
2. Click inside the table, Insert > PivotTable > OK; drag dept_name to Rows and days_present to Values (Sum).
3. Totals by formula: `=SUMIFS($C$2:$C$7,$D$2:$D$7,"Sales")`.
**Alternative:** `=INDEX($F$2:$F$4,MATCH(B2,$E$2:$E$4,0))`.
**Result:** (run in LibreOffice 24.2) both lookups give Sales, HR, Sales, IT, HR, Sales; SUMIFS totals: HR 39, Sales 63, IT 21. A missing code such as "Z" gives `#N/A`; `=IFERROR(VLOOKUP("Z",$E$2:$F$4,2,FALSE),"code missing")` shows "code missing". The pivot table gives the same totals: not run here (pivot tables cannot run headless); the totals are hand-checked (20+19 = 39; 22+18+23 = 63; 21).
**Version note:** VLOOKUP, INDEX-MATCH and pivots work in all versions; XLOOKUP only in 365/2021/2024 (Q3).
**Edge cases:** The fourth argument `FALSE` forces exact match; without it a lookup can return a wrong row silently.
**Likely follow-ups:**
- *What if they resist?* Start with a 10-minute win on their own report.
- *How do you check learning?* Ask them to repeat on next month's file.
**Common mistakes:** Teaching with abstract data; too much at once; making the colleague feel slow.

## Skill-development plan

This is the plan the questions above refer to. It is a study design, not a research finding: the hours, exercise counts and pass marks are my study-plan targets, not researched figures. Resource notes come from research/Book01_Part12_sources.md (accessed 2026-10-21).

### A. Zero-to-job-ready roadmap (12 weeks, about 2 hours a day, 6 days a week)

| Week | Topics (Book 1 part) | Exercise target | Check at the end |
|---|---|---|---|
| 1 | Cell references, sorting, filters, formatting, shortcuts (Part 1) | 20 | none |
| 2 | IF, AND/OR, COUNTIF(S), SUMIF(S) (Part 2) | 30 | Quiz 1: 6 of 8 |
| 3 | Text and date functions, consolidate on HR sheets (Part 2) | 30 | Quiz 2: 6 of 8 |
| 4 | VLOOKUP, HLOOKUP, INDEX-MATCH, XLOOKUP (Part 3) | 25 | none |
| 5 | Data cleaning: duplicates, TRIM, Text to Columns, Flash Fill (Part 5) | 20 | Quiz 3: 6 of 8 |
| 6 | Pivot tables (Part 4) | 25 | none |
| 7 | Pivot charts, slicers, charts (Parts 4, 8) | 20 | Quiz 4: 5 of 6 |
| 8 | Conditional formatting, validation, what-if, Goal Seek (Part 9) | 20 | none |
| 9 | Dynamic arrays FILTER/UNIQUE/SORT/LET if on 365 or 2021 (Part 6) | 20 | Quiz 5: 5 of 6 |
| 10 | Power Query and Power Pivot introduction (Part 7) | 15 | none |
| 11 | Scenario tasks: MIS reports, HR attrition sheet (Part 10) | 15 | Quiz 6: 4 of 5 scenarios |
| 12 | Revisit weak parts; VBA and Copilot optional (Part 11); two timed mocks; finish projects | mocks | Final: 7 of 8 in 30 minutes |

Weeks 1-11 add up to 240 exercises (20+30+30+25+20+25+20+20+20+15+15, checked by running the sum). If you miss a pass mark, repeat that week and retake the quiz after 3 days. Job-ready signal: pass the Final twice in a row on two different datasets and have two finished mini-projects online (Q22).

### B. Daily practice plan (120 minutes)

| Block | Minutes | What you do |
|---|---|---|
| Learn | 30 | Read the Book 1 part or one help article |
| Guided practice | 30 | Re-type worked examples, change one input, predict the result |
| Problem solving | 40 | 3 to 5 exercises alone, no hints for the first 10 minutes |
| Review | 20 | Update the mistakes log; redo yesterday's failed exercise |

With 1 hour a day, halve each block and never skip Review; the roadmap then takes about 24 weeks. One day a week is rest.

### C. Free resources
Full table in Q9. Stage guide: Microsoft Support function pages (all weeks, for syntax), Exceljet articles (weeks 2-9; free vs paid per item unverified), Google's Sheets training page (optional, Q11). Not verified and therefore not recommended by name: Chandoo.org (blocked, HTTP 403), Microsoft free video courses (page showed no videos), YouTube, Coursera, Udemy, LinkedIn Learning (not checked). The MOS Excel Associate exam is paid by implication (price depends on country; no amount stated) and optional (Q19).

### D. Practice datasets
Self-made 10-row HR sheet first (Q22), then TrumpExcel's 15 free 1,000-row datasets including Employee HR Records (licence unverified), then a public HR attrition set for a portfolio project (AIHR's list: 8 of 9 free; IBM HR Analytics Attrition on Kaggle: size, licence and login unverified). See Q10.

### E. Mini-projects

| Project | Question | Data | Skills shown | Where explained |
|---|---|---|---|---|
| 1 HR attrition workbook | Which department loses people fastest? | Self-made employee sheet | COUNTIFS, AVERAGEIF, checks, pivot, chart | Q5 |
| 2 Public HR dataset analysis | Which department has the highest attrition; what is the leavers' average income? | Public HR attrition CSV | Cleaning, COUNTIFS/AVERAGEIFS, pivot, charts | Q21 |
| 3 Attendance MIS report | Days present by department and month | Self-made attendance list with department codes | Lookup, SUMIFS, pivot, slicers | Q24 |

Each project: README with the question, data source and licence, steps, five findings with numbers, one limitation (Q20).

### F. Self-check tests
Six quizzes (weeks 2, 3, 5, 7, 9, 11) and a Final (week 12) use the pass marks in table A. Each quiz is 5 to 8 questions on that week's topics, written with an answer key before you solve and tried on a dataset you did not practise on, closed book, with your approach spoken aloud. The Final is the eight-question kit T1-T8 in Q22; verified results (run in LibreOffice 24.2): T1 = 7, T2 = 594000, T3 = 0.4, T4 = 63333.33, T5 = 57000, T6 = 5, T7 = 110000, T8 = 0.5. Retake on fresh data and aim for 7 of 8 in 30 minutes, twice.

