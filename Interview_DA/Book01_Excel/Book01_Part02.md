# Book 1 — Excel | Part 2: Core Functions (IF, AND/OR, COUNTIF(S), SUMIF(S), text and date functions) 🟢

**Target:** 70 questions | **Actual:** 74 questions
**Scope:** IF, nested IF/IFS, AND/OR, COUNTIF(S), SUMIF(S), AVERAGEIF(S), text functions, date functions and basic error handling.

### Q1 ⭐⭐⭐ 🟢 What does the IF function do, and what are its three arguments?
**Asked at:** Commonly asked (no company-specific report found). IF appears in every Excel formula prep list seen (e.g., Guru99 Excel formulas interview questions).
**What the interviewer is checking:** Whether you understand "test, then choose one of two results" - the base of all Excel decision-making.
**Say this in the interview:** "IF checks a condition and returns one value if it is true and another if it is false. The three arguments are the logical test, the value if true, and the value if false."
**Explain simply:**
- Argument (a "slot" you fill inside the brackets) 1, `logical_test`: a question that can only be TRUE or FALSE, like `B2>=40`.
- Argument 2, `value_if_true`: what the cell shows when the answer is TRUE.
- Argument 3, `value_if_false`: what it shows when the answer is FALSE. It is optional, but if you leave it out you get the word FALSE, which looks untidy.
- Text results go in double quotes; numbers and cell references do not.
**Example:** HR wants to flag employees who completed 12 or more training hours: `=IF(C2>=12,"Done","Pending")`.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Employee | Training hours |
| 2 | Asha | 14 |
| 3 | Ravi | 8 |

**Formula / Steps:** In C2 type `=IF(B2>=12,"Done","Pending")` and fill down.
**Alternative:** `=IFS(B2>=12,"Done",TRUE,"Pending")` (same result, useful with many conditions). Not run here for this exact sheet; the same IF/IFS pattern is run in Q3.
**Result:** By hand: C2 = Done, C3 = Pending (the same IF pattern is run with real values in Q2).
**Version note:** IF works in every version and in Google Sheets. Microsoft Support "IF function" lists Excel 2016 through 365/2024. It does not state a nesting limit (limit figure: from memory, unverified).
**Edge cases:** A blank cell counts as 0, so `B2>=12` is FALSE. Text such as "14" typed as text can behave differently from the number 14.
**Likely follow-ups:** (1) "Can IF return another formula?" Yes, any value or formula. (2) "How do you test two things?" Wrap them in AND/OR (Q4).
**Common mistakes:** Forgetting quotes around text results; mixing up the true/false order; typing `=IF(B2>=12)` and getting FALSE.

### Q2 ⭐⭐⭐ 🟢 Write a formula that returns "Pass" if the marks in B2 are 40 or more, otherwise "Fail".
**Asked at:** Commonly asked (no company-specific report found). The Pass/Fail IF is the classic first test.
**What the interviewer is checking:** That you can write a correct comparison and fill it down.
**Say this in the interview:** "`=IF(B2>=40,"Pass","Fail")` - and I use `>=` so that exactly 40 passes."
**Explain simply:**
- `>=` means "greater than or equal to"; `>` alone would fail someone with exactly 40.
- "Pass" and "Fail" are text, so they sit in quotes.
- Fill down by dragging the small square at the cell's bottom-right corner.
**Example:** Screening-test marks of candidates, pass mark 40.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Candidate | Marks | Result |
| 2 | Asha | 35 | |
| 3 | Ravi | 40 | |
| 4 | Meena | 72 | |

**Formula / Steps:** C2: `=IF(B2>=40,"Pass","Fail")`, copy down to C4.
**Alternative:** `=IF(B2<40,"Fail","Pass")` (flipped test), or `=IFS(B2>=40,"Pass",TRUE,"Fail")`.
**Result (run in LibreOffice 24.2):** C2 = Fail, C3 = Pass, C4 = Pass.
**Version note:** Works in all versions and Google Sheets.
**Edge cases:** Empty B cell counts as 0, so it shows Fail; use `=IF(B2="","",IF(B2>=40,"Pass","Fail"))` to leave it blank. Marks stored as text ("72") may misbehave: convert with VALUE.
**Likely follow-ups:** (1) "Show Absent if blank?" Add an outer `IF(B2="","Absent",...)`. (2) "More than two outcomes?" Nested IF (Q3).
**Common mistakes:** Using `=>` instead of `>=`; using `>40`; forgetting quotes.

### Q3 ⭐⭐⭐ 🟢 How do you write a nested IF to give grades A, B, C and D based on marks?
**Asked at:** Reported by candidates on Glassdoor MIS interview listings (seen as a search snippet only; company not identified).
**What the interviewer is checking:** Whether you can chain conditions in the right order.
**Say this in the interview:** "A nested IF puts one IF inside the false part of another. I test from the highest band down, so the first TRUE wins." (The question gives no cut-offs, so I assume A 80+, B 60-79, C 40-59, D below 40 and say so.)
**Explain simply:**
- "Nested" means an IF placed inside another IF.
- Excel reads left to right and stops at the first TRUE, so order matters.
- The last band needs no test: it is the leftover "false" value.
**Example:** Grading a 100-mark assessment for trainees.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Name | Marks | Grade |
| 2 | Asha | 92 | |
| 3 | Ravi | 78 | |
| 4 | Meena | 64 | |
| 5 | Imran | 45 | |
| 6 | Kiran | 30 | |

**Formula / Steps:** C2: `=IF(B2>=80,"A",IF(B2>=60,"B",IF(B2>=40,"C","D")))`, fill down.
**Alternative:** `=IFS(B2>=80,"A",B2>=60,"B",B2>=40,"C",TRUE,"D")`; or a lookup table with `VLOOKUP(B2,table,2,TRUE)` for many bands.
**Result (run in LibreOffice 24.2, both formulas agree):** A, B, B, C, D.
**Version note:** Nested IF works everywhere. IFS needs Excel 2019 or later, not 2016 (Microsoft Support, "IFS function", fetched earlier in the part's research; not re-fetched by me, so treat as from the sources file). Google Sheets has IFS.
**Edge cases:** Test order reversed (`>=40` first) gives everyone C or better. Blank marks give D. Decimal marks like 79.5 fall into B correctly.
**Likely follow-ups:** (1) "How many IFs can you nest?" Modern Excel allows 64 (from memory, unverified); better to switch to IFS or a lookup. (2) "Why not IFS?" Not in Excel 2016.
**Common mistakes:** Wrong order of tests; unbalanced closing brackets (one `)` per IF); typing grades without quotes.

### Q4 ⭐⭐⭐ 🟢 How do the AND and OR functions work, and how do you use them inside IF?
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you test several conditions together.
**Say this in the interview:** "AND returns TRUE only if every condition is true; OR returns TRUE if at least one is. They sit inside the IF's test slot."
**Explain simply:**
- `AND(test1, test2, ...)`: all must be true, like "must have rating 4+ AND tenure over 2 years".
- `OR(test1, test2, ...)`: any one is enough, like "late OR absent".
- On their own they return TRUE/FALSE; IF turns that into words or numbers.
**Example:** Promotion shortlist: rating at least 4 AND tenure over 2 years.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Name | Rating | Tenure (yrs) |
| 2 | Asha | 4 | 3 |
| 3 | Ravi | 5 | 1 |
| 4 | Meena | 3 | 6 |
| 5 | Imran | 2 | 0.5 |

**Formula / Steps:** D2 `=AND(B2>=4,C2>2)`; E2 `=OR(B2>=4,C2>2)`; F2 `=IF(AND(B2>=4,C2>2),"Eligible","No")`.
**Alternative:** Multiply tests: `=IF((B2>=4)*(C2>2),"Eligible","No")` (AND); add them for OR.
**Result (run in LibreOffice 24.2):** AND: TRUE, FALSE, FALSE, FALSE. OR: TRUE, TRUE, TRUE, FALSE. IF-AND: Eligible, No, No, No.
**Version note:** Available in all versions and Google Sheets.
**Edge cases:** Text compared with numbers does not error but gives odd results (text is treated as larger than numbers in comparisons). AND/OR ignore text inside a range reference.
**Likely follow-ups:** (1) "How do you do NOT?" `NOT(test)` or `<>`. (2) "Mix AND with OR?" Nest them: `AND(B2>=4,OR(C2>2,D2="Manager"))`.
**Common mistakes:** Writing `AND(B2>=4 AND C2>2)`; confusing AND with OR; writing a range like `4<=B2<=5` (does not work).

### Q5 ⭐⭐⭐ 🟢 How do you use COUNTIF to count how many employees are in the "Sales" department?
**Asked at:** Commonly asked (no company-specific report found). COUNTIF is on every prep list seen (e.g., Guru99).
**What the interviewer is checking:** Conditional counting.
**Say this in the interview:** "`=COUNTIF(B2:B9,"Sales")` counts the cells in the department column that equal Sales."
**Explain simply:**
- `COUNTIF(range, criteria)`: "range" is where to look, "criteria" is the rule.
- Matching is not case-sensitive: "sales" and "SALES" also count.
- A criteria cell reference works too, so `=COUNTIF(B2:B9,H1)` with Sales typed in H1 is easy to change.
**Example:** Headcount of Sales in an 8-person extract.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Emp ID | Dept | City | Salary |
| 2 | E01 | Sales | Hyderabad | 55000 |
| 3 | E02 | HR | Bengaluru | 48000 |
| 4 | E03 | Sales | Bengaluru | 62000 |
| 5 | E04 | Sales | Hyderabad | 45000 |
| 6 | E05 | Finance | Hyderabad | 70000 |
| 7 | E06 | Sales | Hyderabad | 80000 |
| 8 | E07 | HR | Hyderabad | 52000 |
| 9 | E08 | Sales | Chennai | 51000 |

**Formula / Steps:** `=COUNTIF(B2:B9,"Sales")`
**Alternative:** `=SUMPRODUCT(--(B2:B9="Sales"))`, or a PivotTable (Insert > PivotTable, Dept in Rows, Emp ID in Values as Count).
**Result (run in LibreOffice 24.2):** 5.
**Version note:** All versions and Google Sheets.
**Edge cases:** Trailing spaces ("Sales ") do not match; clean with TRIM. Wildcards `*` and `?` work in criteria (Q31 covers them).
**Likely follow-ups:** (1) "Count Sales in Hyderabad only?" COUNTIFS (Q10). (2) "Count everything except Sales?" `=COUNTIF(B2:B9,"<>Sales")`.
**Common mistakes:** Forgetting quotes around Sales; selecting different-sized ranges; counting hidden duplicates of the same employee.

### Q6 ⭐⭐⭐ 🟢 What is the difference between COUNT, COUNTA, COUNTBLANK and COUNTIF?
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know what each one actually counts.
**Say this in the interview:** "COUNT counts numbers, COUNTA counts anything not empty, COUNTBLANK counts empty cells, and COUNTIF counts cells meeting a condition."
**Explain simply:**
- COUNT: only numeric cells (dates are numbers too). Text and blanks are skipped.
- COUNTA: every non-empty cell, including text and even `""` returned by a formula.
- COUNTBLANK: truly empty cells and cells holding `""`.
- COUNTIF: conditional count (Q5).
**Example:** A column of employee IDs, some missing, one number stored as text.
**Sample sheet:**

| | A |
|---|---|
| 2 | 101 |
| 3 | Asha |
| 4 | *(empty)* |
| 5 | 250 |
| 6 | `=""` (looks empty) |
| 7 | '7 (number stored as text) |
| 8 | *(empty)* |
| 9 | 400 |

**Formula / Steps:** `=COUNT(A2:A9)`, `=COUNTA(A2:A9)`, `=COUNTBLANK(A2:A9)`, `=COUNTIF(A2:A9,">200")`
**Alternative:** `=ROWS(A2:A9)-COUNTBLANK(A2:A9)` equals COUNTA here.
**Result (run in LibreOffice 24.2):** COUNT 3; COUNTA 6; COUNTBLANK 3; COUNTIF >200 = 2.
**Version note:** All versions and Google Sheets. The `=""` handling was run in LibreOffice; Excel behaves the same by my memory (unverified).
**Edge cases:** Text-numbers are skipped by COUNT but counted by COUNTA. COUNTA counts `=""` but COUNTBLANK also counts it, so the two overlap.
**Likely follow-ups:** (1) "Which counts only truly empty cells?" `=SUMPRODUCT(--(A2:A9=""))` also catches `""`; use `ISBLANK` per cell for true empties (Q36 covers this). (2) "How do you count text cells?" `=COUNTIF(A2:A9,"*")`.
**Common mistakes:** Using COUNT on a text column and getting 0; assuming COUNTA ignores formula blanks.

### Q7 ⭐⭐⭐ 🟢 How do you use SUMIF to total the salary of one department?
**Asked at:** Commonly asked (no company-specific report found). SUMIF is on the Guru99 list and in Glassdoor MIS candidate snippets (company not identified).
**What the interviewer is checking:** Conditional totals and the argument order.
**Say this in the interview:** "`=SUMIF(B2:B9,"Sales",D2:D9)`: look in the department column, find Sales, add the matching salaries."
**Explain simply:**
- `SUMIF(range, criteria, sum_range)`: the range to test, the rule, then the numbers to add.
- The two ranges must line up row for row.
- If the range to test and the range to add are the same, you may leave out the third argument.
**Example:** Monthly payroll cost of Sales (sample sheet from Q5).
**Sample sheet:** Same table as Q5 (Dept in B2:B9, Salary in D2:D9).
**Formula / Steps:** `=SUMIF(B2:B9,"Sales",D2:D9)`
**Alternative:** `=SUMIFS(D2:D9,B2:B9,"Sales")` or `=SUMPRODUCT((B2:B9="Sales")*D2:D9)`.
**Result (run in LibreOffice 24.2):** All three return 293000 (55000+62000+45000+80000+51000).
**Version note:** All versions and Google Sheets.
**Edge cases:** Text in the sum column is ignored. Salaries stored as text give 0; convert them first.
**Likely follow-ups:** (1) "More than one condition?" SUMIFS (Q9). (2) "Sum for departments starting with S?" `"S*"`.
**Common mistakes:** Giving ranges of different size; swapping the criteria and sum range; leaving out quotes.

### Q8 ⭐⭐⭐ 🟢 What is the difference between COUNTIF and COUNTIFS? Give an example.
**Asked at:** Reported by candidates on Glassdoor MIS interview listings (search snippet only; company not identified).
**What the interviewer is checking:** One condition versus many.
**Say this in the interview:** "COUNTIF has one range and one condition. COUNTIFS takes many range/condition pairs and counts rows where all of them are true, like an AND."
**Explain simply:**
- COUNTIF: `(range, criteria)`.
- COUNTIFS: `(range1, criteria1, range2, criteria2, ...)`, up to 127 pairs (Microsoft Support, "COUNTIFS function"). All ranges must be the same size.
- COUNTIFS joins conditions with AND only; for OR add two COUNTIFs.
**Example:** Sales staff versus Sales staff in Hyderabad.
**Sample sheet:** Same as Q5.
**Formula / Steps:** `=COUNTIF(B2:B9,"Sales")`; `=COUNTIFS(B2:B9,"Sales",C2:C9,"Hyderabad")`
**Alternative:** `=SUMPRODUCT((B2:B9="Sales")*(C2:C9="Hyderabad"))`.
**Result (run in LibreOffice 24.2):** 5 and 3 (E01, E04, E06).
**Version note:** COUNTIFS applies to Excel 2016, 2019, 2021, 2024 and 365 (Microsoft Support). It exists in Excel 2007 onward and in Google Sheets (from memory, unverified).
**Edge cases:** Mismatched range sizes return #VALUE!. Use `*` and `?` wildcards in text criteria.
**Likely follow-ups:** (1) "OR condition?" `=COUNTIF(B2:B9,"Sales")+COUNTIF(B2:B9,"HR")`. (2) "Number criteria?" Use quotes: `">50000"`.
**Common mistakes:** Treating COUNTIFS as OR; using ranges of different length; writing `>50000` without quotes.

### Q9 ⭐⭐⭐ 🟢 What is the difference between SUMIF and SUMIFS, and how does the argument order differ?
**Asked at:** Reported by candidates on Glassdoor MIS interview listings (search snippet only; company not identified).
**What the interviewer is checking:** The classic gotcha: the sum range moves position.
**Say this in the interview:** "SUMIF takes one condition and the sum range comes last. SUMIFS takes many conditions and the sum range comes first."
**Explain simply:**
- `SUMIF(range, criteria, [sum_range])`.
- `SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2], ...)` (Microsoft Support, "SUMIFS function": SUMIF's sum_range is third, SUMIFS' is first).
- SUMIFS applies AND logic across all conditions.
**Example:** Sales salary total versus Sales-in-Hyderabad salary total.
**Sample sheet:** Same as Q5.
**Formula / Steps:** `=SUMIF(B2:B9,"Sales",D2:D9)` and `=SUMIFS(D2:D9,B2:B9,"Sales",C2:C9,"Hyderabad")`
**Alternative:** `=SUMPRODUCT((B2:B9="Sales")*(C2:C9="Hyderabad")*D2:D9)`.
**Result (run in LibreOffice 24.2):** 293000 and 180000 (55000+45000+80000).
**Version note:** SUMIFS applies to Excel 2016 through 365 (Microsoft Support); also in Google Sheets (from memory, unverified).
**Edge cases:** Range sizes must match in SUMIFS. Criteria like `">=50000"` need quotes.
**Likely follow-ups:** (1) "Which one for one condition?" Either; many people use SUMIFS always. (2) "Dates between two values?" Two criteria on the same range.
**Common mistakes:** Copying SUMIF argument order into SUMIFS and getting wrong totals or errors.

### Q10 ⭐⭐⭐ 🟢 Write a COUNTIFS formula to count employees in Sales, based in Hyderabad, with salary above 50,000.
**Asked at:** Commonly asked; a COUNTIFS test is mentioned in Glassdoor MIS analyst snippets (company not identified).
**What the interviewer is checking:** Three conditions at once, with a number comparison.
**Say this in the interview:** "`=COUNTIFS(B2:B9,"Sales",C2:C9,"Hyderabad",D2:D9,">50000")` - three range/criteria pairs."
**Explain simply:**
- Each pair is "where to look, what to match".
- The comparison `">50000"` goes in quotes, with the operator inside.
- All three must be true on the same row.
**Example:** Well-paid Sales staff in Hyderabad.
**Sample sheet:** Same as Q5 (B Dept, C City, D Salary).
**Formula / Steps:** `=COUNTIFS(B2:B9,"Sales",C2:C9,"Hyderabad",D2:D9,">50000")`
**Alternative:** `=SUMPRODUCT((B2:B9="Sales")*(C2:C9="Hyderabad")*(D2:D9>50000))`.
**Result (run in LibreOffice 24.2):** 2 (E01 at 55000 and E06 at 80000). E04 earns 45000, so is excluded.
**Version note:** COUNTIFS in Excel 2016 through 365 (Microsoft Support, "COUNTIFS function").
**Edge cases:** "Above" means strictly greater; 50000 itself is excluded (use `">=50000"` otherwise). Put limits in cells with `">"&F1`.
**Likely follow-ups:** (1) "Make threshold changeable?" `">"&F1`. (2) "Hyderabad or Bengaluru?" Add two COUNTIFS.
**Common mistakes:** Writing `>50000` unquoted; using different-sized ranges; typing `,` between criteria inside one string.

### Q11 ⭐⭐⭐ 🟢 What does IFERROR do, and when would you use it?
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** Error handling, and whether you know the risk of hiding errors.
**Say this in the interview:** "IFERROR returns my fallback value when a formula errors out, and the normal result otherwise. I use it for expected errors like divide by zero, but I avoid blanket use because it can hide real mistakes."
**Explain simply:**
- Syntax: `IFERROR(value, value_if_error)`.
- It traps #N/A, #VALUE!, #REF!, #DIV/0!, #NUM!, #NAME? and #NULL! (Microsoft Support, "IFERROR function").
- Typical uses: lookups with no match, percentages with a zero denominator.
**Example:** Cost per hire = cost / hires, but one month has zero hires.
**Sample sheet:**

| | B | C | D | E |
|---|---|---|---|---|
| 1 | Cost | Hires | Plain | With IFERROR |
| 2 | 5000 | 50 | | |
| 3 | 4000 | 0 | | |
| 4 | 6000 | n/a | | |

**Formula / Steps:** D2 `=B2/C2`; E2 `=IFERROR(B2/C2,"Check")`, fill down.
**Alternative:** `=IF(C2=0,"Check",B2/C2)` (fixes only the zero case), or `IFNA` for lookup #N/A only.
**Result (run in LibreOffice 24.2):** Plain: 100, #DIV/0!, #VALUE!. IFERROR: 100, Check, Check.
**Version note:** Excel 2007 onward; listed for 2016 to 365 (Microsoft Support). IFNA exists since 2013 (from memory, unverified). Google Sheets has both.
**Edge cases:** Row 4 shows the danger: a data-entry error ("n/a") is hidden just like the harmless zero. Do not wrap a whole workbook in IFERROR.
**Likely follow-ups:** (1) "IFERROR versus IFNA?" IFNA only catches #N/A. (2) "Can it return blank?" Yes, `""`.
**Common mistakes:** Hiding every error; returning 0, which then pollutes averages; putting IFERROR around the wrong part.

### Q12 ⭐⭐⭐ 🟢 How do you extract the first three characters of an employee ID such as "HYD-1045"? Which functions get the last four?
**Asked at:** Commonly asked (no company-specific report found). Text extraction is in standard fundamentals lists.
**What the interviewer is checking:** LEFT, RIGHT, MID basics.
**Say this in the interview:** "LEFT(A2,3) gives HYD and RIGHT(A2,4) gives 1045. MID is for the middle."
**Explain simply:**
- `LEFT(text, n)`: first n characters.
- `RIGHT(text, n)`: last n characters.
- `MID(text, start, n)`: n characters beginning at position start.
- All results are text, even digits.
**Example:** HYD = Hyderabad office code, 1045 = serial number.
**Sample sheet:**

| | A |
|---|---|
| 1 | Emp ID |
| 2 | HYD-1045 |
| 3 | BLR-2210 |
| 4 | CHN-0007 |

**Formula / Steps:** `=LEFT(A2,3)`; `=RIGHT(A2,4)`; `=MID(A2,5,4)`; as a number `=VALUE(RIGHT(A2,4))`.
**Alternative:** In 365, `=TEXTBEFORE(A2,"-")` and `=TEXTAFTER(A2,"-")` (not run here: LibreOffice does not support them; availability from memory, unverified). Or Data > Text to Columns with "-" as delimiter.
**Result (run in LibreOffice 24.2):** LEFT: HYD, BLR, CHN. RIGHT: 1045, 2210, 0007 (text). VALUE: 1045, 2210, 7 (leading zeros lost).
**Version note:** LEFT/RIGHT/MID in all versions and Google Sheets.
**Edge cases:** IDs of different lengths break fixed counts; use FIND on the dash. RIGHT output is text, so SUM ignores it.
**Likely follow-ups:** (1) "Last part when length varies?" `=RIGHT(A2,LEN(A2)-FIND("-",A2))`. (2) "Keep leading zeros?" Leave it as text.
**Common mistakes:** Expecting a number from RIGHT; wrong start position in MID; forgetting the dash counts as a character.

### Q13 ⭐⭐⭐ 🟢 How do you combine first name and last name into a full name?
**Asked at:** Commonly asked; CONCATENATE appears on the Guru99 formulas list.
**What the interviewer is checking:** Joining text with a space.
**Say this in the interview:** "`=A2&" "&B2`. The ampersand glues text together, and the quoted space goes in between."
**Explain simply:**
- `&` is the "join" operator.
- You must add the space yourself, as `" "`.
- CONCATENATE, CONCAT and TEXTJOIN do the same job (compared in Q35).
**Example:** Build full names for an offer-letter mail merge.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | First | Last |
| 2 | Asha | Rao |
| 3 | `Imran ` (trailing space) | Khan |
| 4 | Meena | *(blank)* |

**Formula / Steps:** `=A2&" "&B2`
**Alternative:** `=TRIM(A2&" "&B2)` or `=TEXTJOIN(" ",TRUE,A2,B2)`, or `=CONCATENATE(A2," ",B2)`.
**Result (run in LibreOffice 24.2):** `&`: "Asha Rao", "Imran  Khan" (double space), "Meena " (stray space). TRIM: "Asha Rao", "Imran Khan", "Meena". TEXTJOIN (ignore empty TRUE): same as TRIM.
**Version note:** `&` and CONCATENATE work everywhere. CONCAT: Microsoft Support page "CONCAT function" lists Excel 2016 to 365 and says it replaces CONCATENATE. TEXTJOIN: Excel 2019 and later (from the sources file, not re-fetched).
**Edge cases:** Blank last name leaves a trailing space; TRIM or TEXTJOIN fixes it. Dates join as serial numbers unless wrapped in TEXT.
**Likely follow-ups:** (1) "Last name first?" `=B2&", "&A2`. (2) "Proper case?" `PROPER` (Q24).
**Common mistakes:** Forgetting the space; joining numbers/dates without TEXT.

### Q14 ⭐⭐⭐ 🟢 What does the TODAY function do, and does its value change?
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know TODAY is "volatile", meaning live, not fixed.
**Say this in the interview:** "TODAY returns the current date from the computer clock. Yes, it changes: it recalculates every time the workbook recalculates or opens, so tomorrow it shows tomorrow's date."
**Explain simply:**
- Syntax `=TODAY()` with nothing inside the brackets.
- It returns a date serial number (a day count) displayed as a date (Microsoft Support, "TODAY function").
- Volatile = recalculates whenever anything changes. Calculation must be Automatic (File > Options > Formulas).
- For a fixed stamp use Ctrl+; (static date).
**Example:** Tenure and ageing reports that update daily.
**Sample sheet:** Not meaningful (output depends on the day it is run).
**Formula / Steps:** `=TODAY()`. Static date: select the cell, press Ctrl+;.
**Alternative:** `=INT(NOW())` gives the same date; or a typed date in a cell for an "as of" report.
**Result:** Not run here (output equals the day it is opened; on 21 Oct 2026 it shows 21-10-2026).
**Version note:** Applies to Excel 2016 through 365 (Microsoft Support). Same in Google Sheets.
**Edge cases:** Old reports re-open with a new date and silently change results. Freeze an "as-of date" cell when you need reproducible numbers.
**Likely follow-ups:** (1) "TODAY versus NOW?" NOW adds the time. (2) "Stop it changing?" Paste as values or use Ctrl+;.
**Common mistakes:** Typing `=TODAY` without brackets; expecting last month's report to keep its date.

### Q15 ⭐⭐⭐ 🟢 In an attendance sheet marked P, A and L, how do you count the days each employee was present?
**Asked at:** Reported by candidates on Glassdoor MIS listings (SUMIF/COUNTIF/IF scenarios; search snippet only, company not identified).
**What the interviewer is checking:** COUNTIF across a row.
**Say this in the interview:** "`=COUNTIF(B2:F2,"P")` for each employee row. I can do the same with A for absent and L for leave."
**Explain simply:**
- Each row is an employee, each column a day.
- COUNTIF works on a row range just as on a column.
- COUNTIF ignores upper/lower case, so "p" is counted as P too.
**Example:** A five-day week.
**Sample sheet:**

| | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| 1 | Name | Mon | Tue | Wed | Thu | Fri | Present |
| 2 | Asha | P | P | A | L | P | |
| 3 | Ravi | A | P | p | P | A | |
| 4 | Meena | L | L | P | A | A | |

**Formula / Steps:** G2: `=COUNTIF(B2:F2,"P")`, fill down. Absent: `=COUNTIF(B2:F2,"A")`.
**Alternative:** `=SUMPRODUCT(--EXACT(B2:F2,"P"))` (case-sensitive); or a PivotTable; or `COUNTIFS` with a date-range header test.
**Result (run in LibreOffice 24.2):** Present: 3, 3, 1. Ravi's lowercase "p" is counted by COUNTIF (3); the case-sensitive EXACT version returns 2. Absent for Asha 1; leave for Meena 2.
**Version note:** All versions and Google Sheets.
**Edge cases:** Half-days (e.g., "HD") need their own rule (`+0.5*COUNTIF(...,"HD")`). Stray spaces ("P ") are not matched.
**Likely follow-ups:** (1) "Attendance %?" `=G2/COUNTA(B2:F2)`. (2) "Count by month?" Use COUNTIFS with a month label row.
**Common mistakes:** Leaving out quotes around P; selecting the Name column in the range; ignoring lowercase or spaced entries.

### Q16 ⭐⭐⭐ 🟢 How do you calculate the average salary of each department?
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** AVERAGEIF, or PivotTable, plus awareness of the zero-rows error.
**Say this in the interview:** "`=AVERAGEIF(B2:B9,"Sales",D2:D9)` for one department; I can list each department in a small table and copy it down, or use a PivotTable with Average of Salary."
**Explain simply:**
- AVERAGEIF(range, criteria, average_range) works like SUMIF but averages.
- Equivalent logic: total of Sales / count of Sales.
- If no row matches, you get #DIV/0!.
**Example:** Compare average pay by department to spot pay gaps.
**Sample sheet:** Same as Q5 (Dept in B2:B9, Salary in D2:D9).
**Formula / Steps:** In a summary table with department names in H2:H4, use `=AVERAGEIF($B$2:$B$9,H2,$D$2:$D$9)`. Or PivotTable: Insert > PivotTable > Dept to Rows, Salary to Values > Value Field Settings > Average.
**Alternative:** `=SUMIF(B2:B9,"Sales",D2:D9)/COUNTIF(B2:B9,"Sales")`.
**Result (run in LibreOffice 24.2):** Sales 58600; HR 50000; Finance 70000. The SUMIF/COUNTIF version also gives 58600. A department with no staff ("Legal") gives #DIV/0!; wrapped in IFERROR it shows "No staff".
**Version note:** AVERAGEIF is Excel 2007 onward and in Google Sheets (from memory, unverified). The PivotTable route was not run here.
**Edge cases:** Blank salary cells are ignored by AVERAGEIF; zeros are not, and drag the average down. Averages can mislead when pay is skewed; mention the median.
**Likely follow-ups:** (1) "Two conditions?" AVERAGEIFS. (2) "Median by department?" Needs an array formula or PivotTable alternative.
**Common mistakes:** Averaging all salaries and calling it department-wise; not locking ranges with `$`; including the header row.

### Q17 ⭐⭐⭐ 🟡 How do you calculate an employee's tenure in years from the date of joining?
**Asked at:** Commonly asked; DATEDIF tenure is typical of HR/MIS dashboards (no company-specific report found).
**What the interviewer is checking:** Date arithmetic and DATEDIF.
**Say this in the interview:** "`=DATEDIF(B2,TODAY(),"Y")` gives complete years. For decimals I use `(TODAY()-B2)/365.25`."
**Explain simply:**
- Dates are numbers underneath (day counts), so you can subtract them.
- DATEDIF(start, end, unit): "Y" = complete years, "YM" = leftover months, "M" = total months.
- DATEDIF is an older, undocumented-in-the-menu function kept for old workbooks; Microsoft warns it can give wrong results in some cases and specifically advises against the "MD" unit (Microsoft Support, "DATEDIF function").
**Example:** Service-anniversary list, as on 21 Oct 2026 (put it in D1 to make the sample repeatable).
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Name / Joined | | As-of date in D1: 21-Oct-2026 |
| 2 | Asha | 15-Mar-2020 | |
| 3 | Ravi | 01-Dec-2024 | |
| 4 | Meena | 21-Oct-2023 | |

**Formula / Steps:** `=DATEDIF(B2,$D$1,"Y")` (use TODAY() instead of $D$1 for live). Years and months: `=DATEDIF(B2,$D$1,"Y")&" yrs "&DATEDIF(B2,$D$1,"YM")&" mths"`.
**Alternative:** `=YEARFRAC(B2,$D$1)` or `=ROUND(($D$1-B2)/365.25,1)`.
**Result (run in LibreOffice 24.2):** DATEDIF Y: 6, 1, 3. Text: "6 yrs 7 mths", "1 yrs 10 mths", "3 yrs 0 mths". Decimal: 6.6, 1.9, 3.0.
**Version note:** DATEDIF works in Excel 2016 to 365 (Microsoft Support) though it is hidden from autocomplete; Google Sheets supports it (from memory, unverified).
**Edge cases:** Joining date after the as-of date errors (LibreOffice returned #VALUE!; Excel returns #NUM! per Microsoft documentation/memory). Dates stored as text fail. Leavers need their exit date instead of TODAY.
**Likely follow-ups:** (1) "Why not just divide by 365?" Leap years drift slightly. (2) "Tenure in months?" `"M"`.
**Common mistakes:** Formatting the cell as a date so it shows 1900; swapping start and end; using the buggy "MD" unit.

### Q18 ⭐⭐⭐ 🟡 How do you calculate the attrition rate in Excel?
**Asked at:** Reported by candidates on Glassdoor MIS interview listings and in HR-analytics project examples (search snippets only; company not identified).
**What the interviewer is checking:** That you know the HR definition, not just a formula.
**Say this in the interview:** "Attrition rate = employees who left in the period divided by average headcount, times 100. Average headcount is opening plus closing headcount divided by two."
**Explain simply:**
- Attrition (employees leaving, by resignation or otherwise) is measured over a period such as a year.
- Headcount = number of employees on the rolls.
- Using the average headcount is the common HR convention; some teams divide by the opening headcount, so state which one you use (formula definition: from memory, unverified against an HR standard).
**Example:** Opening 120, closing 150, 18 leavers in the year.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Opening headcount | 120 |
| 2 | Closing headcount | 150 |
| 3 | Leavers in year | 18 |

**Formula / Steps:** `=B3/AVERAGE(B1:B2)` formatted as % (Home > Number > Percent). Or `=ROUND(B3/AVERAGE(B1:B2)*100,1)`.
**Alternative:** Opening-headcount method: `=B3/B1`. From a data list: `=COUNTIFS(Status,"Left")/AVERAGE(...)`.
**Result (run in LibreOffice 24.2):** 0.1333 which is 13.3% (average headcount 135). Opening-headcount method gives 0.15 (15%).
**Version note:** Plain arithmetic; works in every version and Google Sheets.
**Edge cases:** A monthly rate must be annualised (monthly x 12, approximate) to compare with annual. Separate voluntary from involuntary exits; new joiners who leave within the period still count.
**Likely follow-ups:** (1) "Voluntary attrition?" Count only resignations in the numerator. (2) "How to show by department?" COUNTIFS on department plus a PivotTable.
**Common mistakes:** Dividing by closing headcount; mixing monthly leavers with annual headcount; counting transfers as exits.

### Q19 ⭐⭐⭐ 🟡 Write an IF formula that pays a 10% bonus only if the rating is 4 or more and tenure is above 2 years.
**Asked at:** Commonly asked; this is the typical "IF with AND" payroll scenario (no company-specific report found).
**What the interviewer is checking:** IF + AND with the correct boundaries (>= versus >).
**Say this in the interview:** "`=IF(AND(B2>=4,C2>2),D2*10%,0)`. Rating 4 or more, so `>=`; tenure above 2, so `>`; the bonus is 10 percent of salary." (The question does not say what the bonus is a percentage of; I assume monthly salary in D.)
**Explain simply:**
- AND demands both conditions.
- `10%` can be typed directly; Excel reads it as 0.1.
- Put the 10% in an input cell (e.g., G1) so HR can change the rate without editing formulas.
**Example:** Annual bonus eligibility.
**Sample sheet:**

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Name | Rating | Tenure (yrs) | Salary | Bonus |
| 2 | Asha | 4 | 3 | 50000 | |
| 3 | Ravi | 5 | 2 | 60000 | |
| 4 | Meena | 3 | 5 | 45000 | |
| 5 | Imran | 4 | 2.5 | 80000 | |

**Formula / Steps:** `=IF(AND(B2>=4,C2>2),D2*10%,0)`, fill down. Input-cell version: `=IF(AND(B2>=4,C2>2),D2*$G$1,0)`.
**Alternative:** `=D2*10%*(B2>=4)*(C2>2)` (TRUE/FALSE become 1/0).
**Result (run in LibreOffice 24.2):** 5000, 0, 0, 8000. Ravi has 2 years exactly, which is not "above 2", so no bonus.
**Version note:** All versions and Google Sheets.
**Edge cases:** Blank rating or tenure means no bonus. Tenure should be a number of years (see Q17), not a text label.
**Likely follow-ups:** (1) "Different bonus by rating?" Nested IF or lookup. (2) "Rating 4 or tenure above 2?" Swap AND for OR.
**Common mistakes:** Using `>` for rating (excludes 4); using `>=` for tenure; returning "" instead of 0, which breaks totals.

### Q20 ⭐⭐⭐ 🟡 How do you COUNTIF with a cell reference in the criteria, for example salaries greater than the value in F1?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that a comparison sign must be joined to a cell with `&`?
**Say this in the interview:** "I put the operator in quotes and join the cell with an ampersand, like `">"&F1`, so changing F1 updates the count automatically."
**Explain simply:**
- COUNTIF counts cells that meet one rule. The rule (called the criteria) is text such as `">50000"`.
- A cell reference cannot sit inside the quotes, so you cut the rule in two: the operator in quotes, then `&`, then the cell.
- Typing the cell alone (`F1`) means "equal to F1", not "greater than".
**Example:** HR wants to know how many people earn above a threshold the manager keeps changing in F1.
**Sample sheet:**

| | C (Salary) | F |
|---|---|---|
| 1 | Salary | 50000 |
| 2 | 42000 | |
| 3 | 55000 | |
| 4 | 61000 | |
| 5 | 50000 | |
| 6 | 38000 | |
| 7 | 72000 | |

**Formula / Steps:** `=COUNTIF(C2:C7,">"&F1)`
**Alternative:** `=SUMPRODUCT(--(C2:C7>F1))` (the double minus turns TRUE/FALSE into 1/0 so they can be added).
**Result (run in LibreOffice):** `>`&F1 gives 3 (55000, 61000, 72000). `">="&F1` gives 4. `COUNTIF(C2:C7,F1)` (equals) gives 1. SUMPRODUCT gives 3.
**Version note:** COUNTIF works in every Excel version and Google Sheets.
**Edge cases:** Blank cells and text are ignored. Numbers stored as text are not counted by `>`. If F1 is blank, `">"&F1` becomes `">"` and the count is usually 0.
**Likely follow-ups:** 1) Two conditions? Use COUNTIFS. 2) Not equal to F1? `"<>"&F1`.
**Common mistakes:** Writing `">F1"` (Excel looks for the literal text "F1"); forgetting `&`; forgetting to lock ranges with `$` when copying down.

### Q21 ⭐⭐⭐ 🟡 How do you sum sales between two dates using SUMIFS?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use two conditions on the same date column with start and end dates in cells?
**Say this in the interview:** "SUMIFS takes the sum range first, then the date column twice: once with `>=` start date and once with `<=` end date, each joined with `&`."
**Explain simply:**
- SUMIFS adds numbers only for rows that pass every rule you give it.
- A date range is two rules on one column: on or after the start, and on or before the end.
- Dates are really serial numbers underneath, so `>=` and `<=` work like on numbers.
**Example:** Total sales between 10 Jan and 31 Jan 2026.
**Sample sheet:**

| | A (Date) | B (Sales) | F |
|---|---|---|---|
| 1 | | | 10-Jan-2026 |
| 2 | 03-Jan-2026 | 1200 | 31-Jan-2026 |
| 3 | 10-Jan-2026 | 800 | |
| 4 | 15-Jan-2026 | 1500 | |
| 5 | 20-Jan-2026 | 900 | |
| 6 | 31-Jan-2026 | 2000 | |
| 7 | 02-Feb-2026 | 700 | |

(Start date in F1, end date in F2.)
**Formula / Steps:** `=SUMIFS(B2:B7,A2:A7,">="&F1,A2:A7,"<="&F2)`
**Alternative:** `=SUMPRODUCT((A2:A7>=F1)*(A2:A7<=F2)*B2:B7)`
**Result (run in LibreOffice):** 5200 (800+1500+900+2000). Both formulas agree. Using `>` and `<` (exclusive) gives 2400.
**Version note:** SUMIFS: Excel 2007 onwards and Google Sheets.
**Edge cases:** If the date column has a time part (e.g. 31-Jan 14:30), `<=31-Jan` misses it; use `"<"&F2+1` (also gives 5200 here). Dates stored as text are not matched.
**Likely follow-ups:** 1) Add a region condition? Add another pair. 2) Whole month? Start `DATE(2026,1,1)`, end `EOMONTH(start,0)`.
**Common mistakes:** Putting the sum range last (that is SUMIF's order, not SUMIFS); typing dates as text like `">=10-01-2026"` (locale-dependent); mismatched range sizes.

### Q22 ⭐⭐ 🟢 What is the IFS function, and in which Excel versions is it available?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the cleaner alternative to nested IF, and its version limits?
**Say this in the interview:** "IFS tests conditions in order and returns the answer for the first TRUE one. It needs Excel 2019 or Microsoft 365, so in 2016 I use nested IF."
**Explain simply:**
- Syntax: `IFS(test1, result1, test2, result2, ...)`. No nesting brackets needed.
- It stops at the first TRUE test, so order from strictest to loosest.
- If nothing is TRUE, you get `#N/A`. Add `TRUE, "F"` at the end as a catch-all "else".
**Example:** Grades from marks: 90+ A, 75+ B, 60+ C, 40+ D, else F.
**Sample sheet:**

| | B (Marks) |
|---|---|
| 2 | 92 |
| 3 | 78 |
| 4 | 64 |
| 5 | 45 |
| 6 | 30 |

**Formula / Steps:** `=IFS(B2>=90,"A",B2>=75,"B",B2>=60,"C",B2>=40,"D",TRUE,"F")`
**Alternative:** `=IF(B2>=90,"A",IF(B2>=75,"B",IF(B2>=60,"C",IF(B2>=40,"D","F"))))`
**Result (run in LibreOffice):** A, B, C, D, F for rows 2 to 6 (identical for both formulas). Without the `TRUE` catch-all, `=IFS(B5>=90,"A")` returns `#N/A`.
**Version note:** Excel 2019, 2021, 2024 and Microsoft 365 (Microsoft Support, "IFS function"); not in Excel 2016. Google Sheets has IFS (from memory, unverified).
**Edge cases:** Blank marks count as 0 and fall to "F"; text marks may give errors.
**Likely follow-ups:** 1) Exact-match lookups instead? SWITCH. 2) Many bands? A lookup table with approximate match is easier to maintain.
**Common mistakes:** Wrong order of conditions; forgetting the catch-all; sending a file to someone on Excel 2016.

### Q23 ⭐⭐ 🟢 What does the LEN function return, and where would you use it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic text checks and data validation.
**Say this in the interview:** "LEN returns the number of characters in a cell, including spaces. I use it to validate ID lengths and to spot hidden extra spaces."
**Explain simply:**
- Characters means letters, digits, spaces and symbols; every one counts as 1.
- Compare `LEN(A2)` with `LEN(TRIM(A2))` (TRIM removes extra spaces); a difference means stray spaces.
- Use it to check that employee IDs or phone numbers have the right length.
**Example:** Employee IDs must be 8 characters like "HYD-1045".
**Sample sheet:**

| | A (ID) |
|---|---|
| 2 | HYD-1045 |
| 3 | ` BLR-2210 ` (spaces both sides) |
| 4 | HYD-9 |
| 5 | 98765 43210 |

**Formula / Steps:** `=LEN(A2)`, `=LEN(TRIM(A2))`, `=IF(LEN(A2)=8,"OK","Check")`
**Alternative:** `=SUMPRODUCT(--(LEN(A2:A5)<>8))` counts bad IDs in one go.
**Result (run in LibreOffice):** LEN: 8, 10, 5, 11. LEN(TRIM): 8, 8, 5, 11. Row 2 check "OK", row 4 "Check".
**Version note:** Works in all versions and Google Sheets.
**Edge cases:** LEN of a number counts digits as typed without formatting (a date gives its serial number's length, e.g. 5). Blank gives 0.
**Likely follow-ups:** 1) Count of a letter in a cell? `LEN(A2)-LEN(SUBSTITUTE(A2,"a",""))`. 2) Non-breaking spaces? TRIM misses them; use SUBSTITUTE(A2,CHAR(160),"").
**Common mistakes:** Forgetting that spaces count; expecting LEN to see cell formatting.

### Q24 ⭐⭐ 🟢 What do UPPER, LOWER and PROPER do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Data cleaning basics.
**Say this in the interview:** "UPPER makes everything capitals, LOWER makes everything small letters, PROPER capitalises the first letter of each word. I use them to clean messy names."
**Explain simply:**
- Each takes one text input and returns a new cleaned text; the original cell is unchanged.
- LOWER is handy for emails, so "Sunil@ABC.com" and "sunil@abc.com" match.
- PROPER also capitalises after any non-letter, so "o'neil" becomes "O'Neil" and "mcdonald" only "Mcdonald".
**Example:** Names typed inconsistently in an HR form.
**Sample sheet:**

| | A (Name) |
|---|---|
| 2 | rAVI kumar |
| 3 | PRIYA SHARMA |
| 4 | anita rao |
| 5 | SUNIL.Mehta@ABC.com |

**Formula / Steps:** `=UPPER(A2)`, `=LOWER(A2)`, `=PROPER(A2)`
**Alternative:** Flash Fill (Data tab > Flash Fill, or Ctrl+E) after typing one example; or `=PROPER(TRIM(A2))` to clean spaces too.
**Result (run in LibreOffice):** Row 2: RAVI KUMAR / ravi kumar / Ravi Kumar. Row 3: PRIYA SHARMA / priya sharma / Priya Sharma. Row 4: ANITA RAO / anita rao / Anita Rao. `LOWER(A5)` = sunil.mehta@abc.com.
**Version note:** All versions and Google Sheets.
**Edge cases:** Numbers pass through unchanged. Results are formulas; to keep them, copy > Paste Special > Values.
**Likely follow-ups:** 1) Are lookups case sensitive? No, VLOOKUP/MATCH ignore case. 2) Case-sensitive compare? EXACT().
**Common mistakes:** Overwriting the original column; expecting PROPER to handle names like "McDonald" or initials.

### Q25 ⭐⭐ 🟢 How do you pull the year, month and day out of a date?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Date function basics, used for tenure, cohort and monthly reports.
**Say this in the interview:** "YEAR, MONTH and DAY each return that part of a date as a number. If I want the month name I use TEXT."
**Explain simply:**
- Excel stores a date as a number; these functions read the part you want.
- Handy for grouping hires by year or month in a pivot table.
- `DATE(year,month,day)` does the reverse: builds a date from parts.
**Example:** Group joiners by year and month.
**Sample sheet:**

| | A (Joining date) |
|---|---|
| 2 | 15-Mar-2026 |
| 3 | 01-Dec-2025 |
| 4 | 28-Jul-2024 |

**Formula / Steps:** `=YEAR(A2)`, `=MONTH(A2)`, `=DAY(A2)`
**Alternative:** `=TEXT(A2,"mmmm")` gives the month name; `=TEXT(A2,"yyyy")` gives the year as text.
**Result (run in LibreOffice):** Row 2: 2026, 3, 15, "March". Row 3: 2025, 12, 1, "December". Row 4: 2024, 7, 28, "July". `TEXT(A2,"yyyy")` returns text "2026" (ISNUMBER = FALSE), whereas YEAR returns a number.
**Version note:** All versions and Google Sheets.
**Edge cases:** If the cell holds text that looks like a date, the functions may error or misread (see Q29). Blank cell returns year 1900 / month 1 / day 0.
**Likely follow-ups:** 1) First of the month? `=DATE(YEAR(A2),MONTH(A2),1)` (gives 01-Mar-2026). 2) Financial year? Use IF(MONTH>=4,...).
**Common mistakes:** Using TEXT and then doing maths on the text result; typing dates as text.

### Q26 ⭐⭐ 🟢 How does the TEXT function work? Show a date formatted as "dd-mmm-yyyy" and as a weekday name.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you control how a value displays inside a formula or label?
**Say this in the interview:** "TEXT converts a value to text in a format I choose: `TEXT(A2,"dd-mmm-yyyy")` for a date, `TEXT(A2,"dddd")` for the weekday name."
**Explain simply:**
- Syntax: `TEXT(value, "format code")`. The format code is the same one used in Format Cells > Custom.
- `dd` = day, `mmm` = short month, `yyyy` = year; `ddd` = Mon, `dddd` = Monday.
- The output is text, so you cannot do maths on it.
- Main use: joining numbers or dates into sentences.
**Example:** "Joined on 15-Mar-2026" labels in a report.
**Sample sheet:**

| | A (Date) |
|---|---|
| 2 | 15-Mar-2026 |
| 3 | 01-Dec-2025 |
| 4 | 26-Jan-2026 |

**Formula / Steps:** `=TEXT(A2,"dd-mmm-yyyy")`, `=TEXT(A2,"dddd")`, `="Joined on "&TEXT(A2,"dd-mmm-yyyy")`
**Alternative:** Format Cells (Ctrl+1) > Number > Custom, type `dd-mmm-yyyy`. This changes the look and keeps the value a real date.
**Result (run in LibreOffice):** Row 2: 15-Mar-2026, Sunday, Sun. Row 3: 01-Dec-2025, Monday. Row 4: 26-Jan-2026, Monday. Number examples: `TEXT(0.256,"0.0%")` = 25.6%; `TEXT(1234567.891,"#,##0")` = 1,234,568; `TEXT(7,"000")` = 007. Label: "Joined on 15-Mar-2026".
**Version note:** All versions and Google Sheets. Format codes are language/locale dependent in Excel (from memory, unverified); LibreOffice used English.
**Edge cases:** In non-English Excel the code letters can differ (e.g. `jjjj` for year in German). Text results align left.
**Likely follow-ups:** 1) Why does TEXT break my sum? It returns text; wrap in VALUE or keep the original. 2) Month-year? `"mmm-yy"`.
**Common mistakes:** Forgetting the quotes around the format; using `mm` for month inside time contexts (after `hh`, `mm` means minutes); doing arithmetic on the output.

### Q27 ⭐⭐ 🟢 How do you count working days between two dates, excluding weekends and holidays?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know NETWORKDAYS and its holiday list?
**Say this in the interview:** "NETWORKDAYS counts Monday to Friday days between two dates, both ends included, and a third argument takes a range of holiday dates to skip."
**Explain simply:**
- Syntax: `NETWORKDAYS(start_date, end_date, [holidays])` (Microsoft Support, "NETWORKDAYS function").
- Weekends (Saturday and Sunday) are skipped automatically. Holidays are dates you list in cells.
- If your weekend is different, use NETWORKDAYS.INTL.
**Example:** Working days in October 2026 for payroll, with two sample holidays.
**Sample sheet:**

| | A (Start) | B (End) | E (Holidays) |
|---|---|---|---|
| 2 | 01-Oct-2026 | 31-Oct-2026 | 02-Oct-2026 |
| 3 | | | 20-Oct-2026 |

**Formula / Steps:** `=NETWORKDAYS(A2,B2,E2:E3)`
**Alternative:** `=NETWORKDAYS.INTL(A2,B2,11,E2:E3)` where weekend code 11 means only Sunday is off.
**Result (run in LibreOffice):** Without holidays 22; with the two holidays 20. INTL with Sunday-only weekend: 25.
**Version note:** NETWORKDAYS exists in all modern Excel versions; NETWORKDAYS.INTL from Excel 2010 (from memory, unverified). Google Sheets has both.
**Edge cases:** Start and end are both counted if they are working days. If a holiday falls on a weekend it is not subtracted twice. A holiday typed as text gives `#VALUE!`. If the end date is earlier than the start you get a negative number.
**Likely follow-ups:** 1) Many holidays? Keep a named holiday list. 2) Date after N working days? WORKDAY (see Q48).
**Common mistakes:** Forgetting to lock the holiday range with `$`; using `end - start` (calendar days: 31 here, not 22).

### Q28 ⭐⭐ 🟢 How do you find the day of the week for a date?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** WEEKDAY vs TEXT, and awareness of the numbering options.
**Say this in the interview:** "WEEKDAY gives a number; with type 2 Monday is 1 and Sunday is 7. For the name I use TEXT with `dddd`."
**Explain simply:**
- `WEEKDAY(date)` by default says Sunday = 1 ... Saturday = 7.
- `WEEKDAY(date,2)` says Monday = 1 ... Sunday = 7, which is easier for "weekend if above 5".
- `TEXT(date,"dddd")` gives the name directly.
**Example:** Mark attendance dates as weekend or weekday.
**Sample sheet:**

| | A (Date) |
|---|---|
| 2 | 15-Mar-2026 |
| 3 | 14-Mar-2026 |
| 4 | 16-Mar-2026 |

**Formula / Steps:** `=WEEKDAY(A2)`, `=WEEKDAY(A2,2)`, `=TEXT(A2,"dddd")`, `=IF(WEEKDAY(A2,2)>5,"Weekend","Weekday")`
**Alternative:** `=CHOOSE(WEEKDAY(A2,2),"Mon","Tue","Wed","Thu","Fri","Sat","Sun")`
**Result (run in LibreOffice):** Row 2: 1, 7, Sunday, Weekend, Sun. Row 3: 7, 6, Saturday, Weekend, Sat. Row 4: 2, 1, Monday, Weekday, Mon.
**Version note:** All versions and Google Sheets.
**Edge cases:** Text dates fail. TEXT day names follow the language of Excel.
**Likely follow-ups:** 1) Count Mondays? SUMPRODUCT(--(WEEKDAY(range,2)=1)). 2) Why 1 for Sunday? Default type 1.
**Common mistakes:** Forgetting the second argument and assuming Monday = 1.

### Q29 ⭐⭐ 🟢 Why do dates sometimes show up as numbers like 45231, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that dates are numbers with a format?
**Say this in the interview:** "Excel stores dates as serial numbers counting days from 1 January 1900. 45231 is just the unformatted number; I apply a date format and it shows as 01-Nov-2023."
**Explain simply:**
- Serial number: day 1 = 1-Jan-1900, so each date is a count of days. That is why you can subtract dates.
- The cell format was General or Number, so the number shows.
- Another case: dates that are really text (left-aligned) need converting.
**Example:** A system export gives 45231 instead of a joining date.
**Sample sheet:**

| | A | 
|---|---|
| 2 | 45231 |
| 3 | `2026-03-15` (text) |
| 4 | 15-Mar-2026 (real date) |

**Formula / Steps:** Select cells > Home tab > Number group > drop-down > Short Date (or Ctrl+1 > Number > Date / Custom `dd-mmm-yyyy`). For text dates: `=DATEVALUE(A3)`, then format as date; or Data tab > Text to Columns > Finish with Column data format Date.
**Alternative:** `=TEXT(A2,"dd-mmm-yyyy")` to show it as text.
**Result (run in LibreOffice):** `TEXT(45231,"dd-mmm-yyyy")` = 01-Nov-2023. `DATEVALUE("2026-03-15")` = 46096, which displays as 15-Mar-2026 once formatted. `ISNUMBER` of the text date is FALSE; of the real date TRUE.
**Version note:** All versions. Excel on Mac with the old 1904 system starts 4 years later (from memory, unverified).
**Edge cases:** DATEVALUE on formats like 15-03-2026 depends on regional settings (from memory, unverified). Numbers below about 1 show as 00-Jan-1900. Dates before 1900 are not supported.
**Likely follow-ups:** 1) What is 0.5 as time? 12:00 noon. 2) How to check if it is real date? ISNUMBER.
**Common mistakes:** Retyping the numbers; formatting text cells (formatting does not convert text to date).

### Q30 ⭐⭐ 🟢 What is the difference between TODAY and NOW?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Date vs date-and-time, and volatile functions.
**Say this in the interview:** "TODAY gives today's date only; NOW gives today's date plus the current time. Both recalculate every time the sheet recalculates or opens."
**Explain simply:**
- TODAY = whole number (a date). NOW = whole number plus a fraction for the time.
- Both are volatile: they refresh automatically, so yesterday's report will change if reopened.
- To freeze a value, type Ctrl+; (date) or Ctrl+Shift+; (time), or paste as values.
**Example:** Tenure = TODAY() minus joining date, but NOW would add a fraction of a day.
**Sample sheet:** not meaningful (values change daily). Illustration only, if opened at 2:30 pm on 22-Oct-2026: TODAY = 22-Oct-2026, NOW = 22-Oct-2026 14:30.
**Formula / Steps:** `=TODAY()` and `=NOW()`
**Alternative:** `=INT(NOW())` equals TODAY. 
**Result (run in LibreOffice):** Checks returned TRUE: `INT(NOW())=TODAY()`, `NOW()-TODAY()>=0`, `NOW()-TODAY()<1`, TODAY is a whole number; NOW is not a whole number (`NOW()=INT(NOW())` is FALSE). Actual values change, so none are printed.
**Version note:** All versions and Google Sheets.
**Edge cases:** Uses the computer's clock and time zone. Not updated when calculation is set to manual.
**Likely follow-ups:** 1) Static date? Ctrl+;. 2) Does it slow Excel? Slightly in huge files (volatile).
**Common mistakes:** Using NOW for date comparisons (a record dated today at midnight is "before" NOW); forgetting that reports change on reopening.

### Q31 ⭐⭐ 🟢 How do you use wildcards (* and ?) in COUNTIF to count names starting with "A"?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Wildcards in criteria.
**Say this in the interview:** "A wildcard is a stand-in character. `*` means any number of characters, `?` means exactly one. `COUNTIF(A2:A9,"A*")` counts names starting with A."
**Explain simply:**
- `*` matches zero or more characters; `?` matches exactly one.
- To search for a real `*` or `?`, put `~` before it, e.g. `"~*"` (Microsoft Support, "COUNTIFS function").
- COUNTIF is not case sensitive, so "ajay" counts for "A*".
- Wildcards work only with text, not numbers.
**Example:** Count candidates whose names start with A.
**Sample sheet:**

| | A (Name) | F |
|---|---|---|
| 1 | | A |
| 2 | Anita | |
| 3 | Arun | |
| 4 | Bhavna | |
| 5 | Aarti | |
| 6 | Karan | |
| 7 | Amit | |
| 8 | Ankit | |
| 9 | ajay | |

**Formula / Steps:** `=COUNTIF(A2:A9,"A*")`; with a cell: `=COUNTIF(A2:A9,F1&"*")`
**Alternative:** `=SUMPRODUCT(--(LEFT(A2:A9,1)="A"))`
**Result (run in LibreOffice):** 6 (Anita, Arun, Aarti, Amit, Ankit, ajay). `"A???"` (4 letters starting with A) = 3 (Arun, Amit, ajay). `"*an*"` = 3 (Anita, Karan, Ankit). `"?a*"` = 2 (Aarti, Karan). Cell version = 6, SUMPRODUCT = 6.
**Version note:** All versions and Google Sheets.
**Edge cases:** Leading spaces break "A*". Excel's behaviour on `?` is identical to LibreOffice here, but LibreOffice can be set to use regular expressions instead (from memory, unverified).
**Likely follow-ups:** 1) Ends with "a"? `"*a"`. 2) Case sensitive? SUMPRODUCT with EXACT.
**Common mistakes:** Forgetting quotes; using `%` or `.*`; wildcards on numbers.

### Q32 ⭐⭐ 🟢 How do you count cells that contain specific text anywhere inside them?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** "Contains" logic with wildcards.
**Say this in the interview:** "I put an asterisk on both sides of the text: `COUNTIF(range,"*offer*")`, meaning anything before, the word, and anything after."
**Explain simply:**
- `*offer*` matches any cell that has "offer" anywhere inside.
- Not case sensitive.
- To use a cell instead of typed text: `"*"&D1&"*"`.
**Example:** Count exit comments that mention "offer".
**Sample sheet:**

| | A (Exit comment) |
|---|---|
| 2 | Left - better offer |
| 3 | Good performer |
| 4 | Relocation |
| 5 | Offer letter pending |
| 6 | Late joiner |
| 7 | OFFER withdrawn |

(D1 holds the word `offer`.)
**Formula / Steps:** `=COUNTIF(A2:A7,"*offer*")` or `=COUNTIF(A2:A7,"*"&D1&"*")`
**Alternative:** `=SUMPRODUCT(--ISNUMBER(SEARCH("offer",A2:A7)))`. For case-sensitive use FIND instead of SEARCH.
**Result (run in LibreOffice):** 3 for COUNTIF (both forms) and 3 for the SEARCH version. The FIND version returns 1 (only the lowercase "offer").
**Version note:** All versions and Google Sheets.
**Edge cases:** Wildcard characters in the search text need `~`. Cells longer than 255 characters can give `#VALUE!` in COUNTIF (from memory, unverified).
**Likely follow-ups:** 1) Starts with? `"offer*"`. 2) Contains either of two words? Add two COUNTIFs (watch double counting).
**Common mistakes:** Forgetting the asterisks (then it needs an exact match).

### Q33 ⭐⭐ 🟢 What is the difference between FIND and SEARCH?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Case sensitivity and wildcards.
**Say this in the interview:** "Both return the position of a piece of text inside another. FIND is case sensitive and has no wildcards; SEARCH ignores case and allows wildcards."
**Explain simply:**
- Syntax for both: `(find_text, within_text, [start_num])`.
- If the text is not found, both return `#VALUE!`.
- Used with LEFT/MID to cut text at a position.
**Example:** Get the number after the dash in "HYD-1045".
**Sample sheet:**

| | A (ID) |
|---|---|
| 2 | HYD-1045 |

**Formula / Steps:** `=FIND("-",A2)`, `=MID(A2,FIND("-",A2)+1,10)`
**Alternative:** `=SEARCH("h?d",A2)` uses a wildcard.
**Result (run in LibreOffice):** FIND("-")=4; SEARCH("-")=4. `FIND("hyd",A2)` = `#VALUE!` (case differs), `SEARCH("hyd",A2)` = 1. `SEARCH("h?d",A2)` = 1; `FIND("h?d",A2)` = `#VALUE!`. MID formula returns 1045 (as text). `IFERROR(FIND("hyd",A2),0)` = 0.
**Version note:** All versions and Google Sheets.
**Edge cases:** MID returns text; wrap with VALUE for a number. A start_num beyond the match returns `#VALUE!`.
**Likely follow-ups:** 1) Handle not found? IFERROR. 2) Which is faster? No practical difference.
**Common mistakes:** Mixing up which is case sensitive; not wrapping in IFERROR.

### Q34 ⭐⭐ 🟢 How do you replace one piece of text with another using SUBSTITUTE?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Text cleaning.
**Say this in the interview:** "SUBSTITUTE swaps specific old text for new text: `SUBSTITUTE(text, old, new, [instance])`. It is case sensitive."
**Explain simply:**
- It replaces every match unless you give an instance number (which occurrence to replace).
- REPLACE is different: it overwrites by position and length.
- Deleting characters: replace with `""`.
**Example:** Remove the dash from phone numbers; clean "Rs. 45,000" into a number.
**Sample sheet:**

| | A |
|---|---|
| 2 | 98765-43210 |
| 3 | Sales Dept |
| 4 | a-b-c |
| 5 | HR hr |
| 6 | Rs. 45,000 |

**Formula / Steps:** `=SUBSTITUTE(A2,"-","")`; `=SUBSTITUTE(A3,"Dept","Department")`; `=SUBSTITUTE(A4,"-","/",2)`
**Alternative:** `=REPLACE(A5,1,2,"X")` (by position); Home > Find & Select > Replace (Ctrl+H) for one-off changes.
**Result (run in LibreOffice):** 9876543210; Sales Department; a-b/c. `SUBSTITUTE(A5,"hr","X")` = "HR X" (case sensitive). `REPLACE(A5,1,2,"X")` = "X hr". `VALUE(SUBSTITUTE(SUBSTITUTE(A6,"Rs. ",""),",",""))` = 45000. Counting dashes in A4: `LEN(A4)-LEN(SUBSTITUTE(A4,"-",""))` = 2. The result of A2's SUBSTITUTE is text; `--` converts it to the number 9876543210.
**Version note:** All versions and Google Sheets.
**Edge cases:** Result is text, so IDs with leading zeros survive. Non-breaking spaces need `CHAR(160)`.
**Likely follow-ups:** 1) Several replacements? Nest SUBSTITUTE. 2) Ctrl+H vs formula? Ctrl+H changes the data permanently.
**Common mistakes:** Expecting case-insensitive replace; expecting a number back.

### Q35 ⭐⭐ 🟢 What is the difference between CONCATENATE, CONCAT, the & operator and TEXTJOIN?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Modern vs old functions and joining with delimiters.
**Say this in the interview:** "`&` and CONCATENATE join single cells. CONCAT does the same but also accepts ranges. TEXTJOIN adds a delimiter and can skip blanks, so it is the best for lists."
**Explain simply:**
- Delimiter = the separator between pieces (space, comma).
- CONCATENATE is the old function; CONCAT "replaces" it and CONCATENATE stays for compatibility (Microsoft Support, "CONCAT function").
- TEXTJOIN(delimiter, ignore_empty, text1, ...) is in Excel 2019 and Microsoft 365 (Microsoft Support, "TEXTJOIN function").
- `&` works everywhere and is the quickest.
**Example:** Build full names when some people have no middle name.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 2 | Ravi | Kumar | Singh |
| 3 | Priya | (blank) | Rao |

**Formula / Steps:** `=A2&" "&B2&" "&C2`; `=CONCATENATE(A2," ",B2," ",C2)`; `=CONCAT(A2," ",B2," ",C2)`; `=TEXTJOIN(" ",TRUE,A2:C2)`
**Alternative:** `=CONCAT(A2:C2)` joins a range with no spaces.
**Result (run in LibreOffice):** Row 2: all four give "Ravi Kumar Singh"; `CONCAT(A2:C2)` = RaviKumarSingh. Row 3: the first three give "Priya  Rao" (two spaces); TEXTJOIN gives "Priya Rao". `CONCATENATE(A2:C2)` with a range gives `#VALUE!` in LibreOffice (Excel's implicit-intersection behaviour differs; from memory, unverified).
**Version note:** The CONCAT page lists Excel 2016 among applies-to versions, while the usual advice is Excel 2019 or Microsoft 365 for CONCAT/TEXTJOIN (from memory, unverified; check on your Excel). Google Sheets has all four (from memory, unverified).
**Edge cases:** Dates and numbers join as raw serials/unformatted; wrap in TEXT. Results are limited to 32,767 characters (from memory, unverified).
**Likely follow-ups:** 1) Join with commas, skipping blanks? TEXTJOIN. 2) Join dates? `TEXT(A2,"dd-mmm-yyyy")`.
**Common mistakes:** Forgetting spaces; passing a range to CONCATENATE; showing a date as 46096.

### Q36 ⭐⭐ 🟢 How do you check whether a cell is blank, and what is the difference between a blank cell and a cell holding ""?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Truly empty versus empty-looking.
**Say this in the interview:** "ISBLANK is TRUE only for a truly empty cell. A cell with a formula returning "" looks empty but ISBLANK says FALSE; `A2=""` is TRUE for both."
**Explain simply:**
- Blank cell: nothing in it. "" cell: holds an empty text string, often from a formula like `=IF(x,"","")`.
- A cell with just a space is not blank either.
- COUNTBLANK counts both empty and "" cells; COUNTA counts the "" cell as non-empty.
**Example:** Attendance sheet where some cells come from formulas.
**Sample sheet:**

| | A | what it holds |
|---|---|---|
| 2 | (empty) | truly empty |
| 3 | `=""` | formula, empty text |
| 4 | ` ` | one space |
| 5 | x | text |
| 6 | 0 | zero |

**Formula / Steps:** `=ISBLANK(A2)`, `=A2=""`, `=LEN(A2)=0`, `=LEN(TRIM(A2))=0`
**Alternative:** `=COUNTBLANK(A2:A6)`
**Result (run in LibreOffice):** ISBLANK: TRUE, FALSE, FALSE, FALSE, FALSE. `A=""`: TRUE, TRUE, FALSE, FALSE, FALSE. LEN=0: TRUE, TRUE, FALSE, FALSE, FALSE. LEN(TRIM)=0: TRUE, TRUE, TRUE, FALSE, FALSE. COUNTBLANK = 2, COUNTA = 4, COUNT = 1.
**Version note:** All versions and Google Sheets (Sheets behaviour from memory, unverified).
**Edge cases:** `A2=0` is TRUE for a truly empty cell in Excel (empty acts as 0); in the row above 0 is a real number.
**Likely follow-ups:** 1) Which for a data check? `LEN(TRIM(x))=0`. 2) Why doesn't COUNTA match COUNTBLANK? "" cells are counted by both.
**Common mistakes:** Using ISBLANK on formula results; ignoring cells with a space.

### Q37 ⭐⭐ 🟢 What do ROUND, ROUNDUP and ROUNDDOWN do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Rounding rules and negative digits.
**Say this in the interview:** "ROUND goes to the nearest, ROUNDUP always away from zero, ROUNDDOWN always toward zero. The second argument is the number of decimal places; negative values round to tens, hundreds."
**Explain simply:**
- `ROUND(number, digits)`: 5 and above rounds up (away from zero) for ROUND.
- Digits 0 = whole number; 2 = two decimals; -2 = nearest hundred.
- Formatting only changes the display; ROUND changes the stored value.
**Example:** A 7.5% raise on a salary of 41,250.
**Sample sheet:**

| | A | B (=A2*1.075) |
|---|---|---|
| 2 | 41250 | 44343.75 |
| 3 | 2.5 | |
| 4 | -2.5 | |
| 5 | -2.7 | |

**Formula / Steps:** `=ROUND(B2,0)`, `=ROUNDUP(B2,0)`, `=ROUNDDOWN(B2,0)`, `=ROUND(B2,-2)`
**Alternative:** `=INT(B2)` (rounds down to the lower integer), `=TRUNC(B2)` (cuts decimals), MROUND for nearest multiple.
**Result (run in LibreOffice):** ROUND = 44344; ROUNDUP = 44344; ROUNDDOWN = 44343; ROUND(,-2) = 44300; ROUND(B2,1) = 44343.8. Row 3 (2.5): 3, 3, 2. Row 4 (-2.5): -3, -3, -2. Row 5 (-2.7): -3, -3, -2. `INT(-2.7)` = -3 but `TRUNC(-2.7)` = -2.
**Version note:** All versions and Google Sheets.
**Edge cases:** Negative numbers round away from zero for ROUND and ROUNDUP.
**Likely follow-ups:** 1) ROUND vs formatting? Formatting keeps hidden decimals and totals may look off by 1. 2) Round to nearest 5? MROUND(x,5).
**Common mistakes:** Using number format and thinking the value is rounded; confusing INT with ROUNDDOWN for negatives.

### Q38 ⭐⭐ 🟢 What does the #DIV/0! error mean, and how do you avoid it when calculating a percentage?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Error handling with care.
**Say this in the interview:** "#DIV/0! means a division by zero or by an empty cell. I avoid it with `IF(C2=0,"",B2/C2)`, so it only skips the real problem and does not hide other errors."
**Explain simply:**
- Dividing by 0 is undefined, so Excel shows the error.
- An empty cell counts as 0 here too.
- Better to test the denominator first than to hide every error.
**Example:** Attrition % by department = leavers / headcount; a new department has headcount 0.
**Sample sheet:**

| | A (Dept) | B (Leavers) | C (Headcount) |
|---|---|---|---|
| 2 | Sales | 6 | 48 |
| 3 | IT | 0 | 0 |
| 4 | Admin | 2 | (blank) |
| 5 | Ops | 4 | 40 |

**Formula / Steps:** `=IF(C2=0,"",B2/C2)`, then format as Percentage (Home > Number > %).
**Alternative:** `=IFERROR(B2/C2,0)`; or `=IF(N(C2)=0,"n/a",B2/C2)`.
**Result (run in LibreOffice):** Plain `B/C`: 0.125, #DIV/0!, #DIV/0!, 0.1. IF version: 12.5%, blank, blank, 10%. IFERROR version: 0.125, 0, 0, 0.1. N version: 0.125, "n/a", "n/a", 0.1.
**Version note:** All versions and Google Sheets (IFERROR from Excel 2007).
**Edge cases:** Returning 0 makes IT look like "0% attrition", which may be misleading; "" or "n/a" is more honest. A "" result breaks later maths.
**Likely follow-ups:** 1) IFERROR vs IF? IFERROR also hides typos. 2) Average over blanks? AVERAGE ignores them.
**Common mistakes:** Wrapping everything in IFERROR; returning 0 and skewing averages.

### Q39 ⭐⭐ 🟢 What causes the #VALUE! and #NAME? errors?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you read an error message, name the cause and fix it without guessing?
**Say this in the interview:** "#VALUE! means the formula got the wrong kind of input, usually text where it needed a number. #NAME? means Excel does not recognise a word in my formula, usually a misspelt function or a text value missing its quotes."
**Explain simply:**
- Excel shows an error code instead of a wrong answer, so the sheet never silently lies.
- #VALUE!: you add, subtract or multiply something that is text (for example "Not given" in a salary column), or the formula's ranges do not fit together.
- #NAME?: a typo in the function name (SUMM), a function your Excel version does not have, a named range that does not exist, or text typed without quotation marks.
- Fix #VALUE! by cleaning the data or using a function that skips text; fix #NAME? by correcting the spelling or checking the version.
**Example:** A payroll sheet has "Not given" typed where a bonus is missing. `=B2+B3` breaks because "Not given" is text.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Name | Salary |
| 2 | Asha | 50000 |
| 3 | Ravi | Not given |
| 4 | Meena | 42000 |

**Formula / Steps:**
1. Error: `=B2+B3` (in D2). Error: `=SUMM(B2:B4)` (in D3).
2. Fix: `=SUM(B2:B4)` (SUM skips text). Or guard it: `=IF(ISNUMBER(B3),B2+B3,B2)`.
3. Click the yellow warning icon beside the cell, or use Formulas > Formula Auditing > Evaluate Formula, to see which part fails.

**Alternative:** `=IFERROR(B2+B3,0)` hides the error, but also hides real problems; use it only after you know the cause.
**Result:** (run in LibreOffice) `=B2+B3` gives #VALUE!; `=SUMM(B2:B4)` gives #NAME?; `=SUM(B2:B4)` gives 92000; the ISNUMBER guard gives 50000; IFERROR version gives 0.
**Version note:** If a colleague on Excel 2016 opens a file using a newer function (for example XLOOKUP), they see #NAME?. Which version has which function: from memory, unverified, except where stated in other answers.
**Edge cases:** Numbers with a stray space or a non-breaking space copied from a web page or HRMS export can be text and cause #VALUE!; TRIM and VALUE help. Excel itself often converts "42000" typed as text in `+`, so the error mostly appears for words. This coercion can differ between Excel and LibreOffice.
**Likely follow-ups:**
1. Is IFERROR a fix? It hides the error; find the cause first.
2. Why #NAME? on a correct formula? Often the function is newer than the Excel version.
**Common mistakes:** Wrapping everything in IFERROR; typing text criteria without quotes; not checking for hidden spaces.

### Q40 ⭐⭐ 🟢 What does the #REF! error mean, and how does it happen?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand how Excel cell references break when the sheet structure changes?
**Say this in the interview:** "#REF! means the formula points to a cell that no longer exists. It usually happens when someone deletes a row, column or sheet that the formula was using, or when a lookup asks for a column number outside its table."
**Explain simply:**
- A reference is the address a formula reads, like B2. If that cell is deleted (not just cleared), the formula's address is destroyed and Excel writes #REF! inside the formula.
- Cutting and pasting over a cell that others point to can also cause it.
- VLOOKUP gives #REF! when the column number is larger than the number of columns in the table.
- Clearing contents (Delete key) does not cause it; deleting the row/column does.
**Example:** A bonus sheet uses `=B2*C2`. Someone deletes column C (the bonus rate). The formula becomes `=B2*#REF!`.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | EmpID | Name | Dept |
| 2 | E101 | Asha | HR |
| 3 | E102 | Ravi | Sales |
| 4 | E103 | Meena | IT |

**Formula / Steps:**
1. `=VLOOKUP("E102",A2:C4,3,FALSE)` gives the department.
2. `=VLOOKUP("E102",A2:C4,5,FALSE)` asks for column 5 of a 3-column table.
3. To repair a deleted-range #REF!, press Ctrl+Z straight away; otherwise rewrite the reference.

**Alternative:** Make the column number dynamic so it cannot drift: `=VLOOKUP("E102",A2:C4,MATCH("Dept",A1:C1,0),FALSE)`.
**Result:** (run) first formula gives Sales; the column-5 version gives #REF! in Excel. LibreOffice returned #VALUE! for this case, so the VLOOKUP-specific #REF! is from Excel documentation memory, not confirmed here; the match-based version gives Sales.
**Version note:** Applies to all versions and Google Sheets (Google Sheets shows #REF! too; unverified).
**Edge cases:** Deleting a whole worksheet breaks references to it; formulas in an Excel Table (structured references) survive row deletes better. Entire-column references like A:A are safer than fixed ranges when columns are removed.
**Likely follow-ups:**
1. Can you undo it after saving and closing? No, Ctrl+Z only works in the session; keep a backup.
2. How do you find all of them? Ctrl+F, search "#REF!" with "Look in: Formulas".
**Common mistakes:** Deleting columns instead of hiding them; leaving #REF! in a report; fixing by typing a value over the formula.

### Q41 ⭐⭐ 🟢 What causes the #N/A error, and how do you handle it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know #N/A means "not found" and that you can handle it deliberately?
**Say this in the interview:** "#N/A means a lookup could not find what it was asked for. I check for spaces, text-versus-number mismatch or a genuinely missing ID, then I use IFNA to show a friendly message only for this error."
**Explain simply:**
- #N/A stands for "not available": VLOOKUP, HLOOKUP, MATCH (and XLOOKUP in some cases) found no match.
- Common reasons: the ID really is missing, an invisible trailing space, a number stored as text on one side, or exact match used on wrongly typed data.
- IFNA only catches #N/A; IFERROR catches every error type, which can hide bugs like #REF!.
**Example:** HR checks 4 payroll IDs against an HRMS export; one ID, E999, left the company and is not in the list.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | EmpID | Name | Salary |
| 2 | E101 | Asha | 45000 |
| 3 | E102 | Ravi | 52000 |
| 4 | E103 | Meena | 61000 |
| 5 | E104 | Kiran | 38000 |

(E1 holds "E104 " with a trailing space.)
**Formula / Steps:**
1. `=VLOOKUP("E999",A2:C5,3,FALSE)`
2. `=IFNA(VLOOKUP("E999",A2:C5,3,FALSE),"Not on payroll")`
3. Fix a space problem: `=VLOOKUP(TRIM(E1),A2:C5,3,FALSE)`

**Alternative:** `=IFERROR(VLOOKUP(...),"Not on payroll")`, or test first with `=ISNA(...)`.
**Result:** (run) step 1 gives #N/A; step 2 gives "Not on payroll"; `VLOOKUP(E1,...)` with the trailing space gives #N/A; with TRIM gives 38000; IFERROR version gives "Not on payroll".
**Version note:** IFNA is available from Excel 2016 through 365 (Microsoft Support, "IFNA function"). Google Sheets has IFNA (from memory, unverified).
**Edge cases:** Approximate-match VLOOKUP (last argument TRUE) can return #N/A when the lookup value is smaller than the first item. Lookup value 101 (number) will not match "101" (text).
**Likely follow-ups:**
1. IFNA vs IFERROR? IFNA is narrower and safer.
2. Is #N/A ever useful? Yes, charts skip #N/A points.
**Common mistakes:** Hiding every error with IFERROR; not trimming spaces; assuming the ID exists.

### Q42 ⭐⭐ 🟢 How do you calculate the average of rows that meet one or more conditions (AVERAGEIF, AVERAGEIFS)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Conditional averages and the difference between the one-condition and many-condition functions.
**Say this in the interview:** "AVERAGEIF averages numbers where one condition is met; AVERAGEIFS handles several conditions, and its average range comes first."
**Explain simply:**
- An average is the total divided by how many numbers there are.
- AVERAGEIF(range to test, condition, range to average). AVERAGEIFS(range to average, test range 1, condition 1, test range 2, condition 2...).
- Cells in the average range that are blank or text are ignored.
- If no row matches, you get #DIV/0! (division by zero).
**Example:** Average salary of HR staff who have a rating of 3 or more.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Dept | Salary | Rating |
| 2 | Sales | 40000 | 4 |
| 3 | HR | 35000 | 3 |
| 4 | Sales | 52000 | 5 |
| 5 | IT | 60000 | 4 |
| 6 | HR | 41000 | 2 |
| 7 | Sales | 48000 | 3 |
| 8 | IT | 72000 | 5 |
| 9 | HR | (blank) | 4 |

**Formula / Steps:**
1. Sales average: `=AVERAGEIF(A2:A9,"Sales",B2:B9)`
2. HR with rating 3 or more: `=AVERAGEIFS(B2:B9,A2:A9,"HR",C2:C9,">=3")`
3. No match: `=IFERROR(AVERAGEIFS(B2:B9,A2:A9,"Finance"),0)`

**Alternative:** `=SUMIFS(B2:B9,A2:A9,"Sales")/COUNTIFS(A2:A9,"Sales")` (but this counts blank salaries in the denominator, so differs when blanks exist).
**Result:** (run) Sales 46666.67; HR with rating at least 3 gives 35000 (the blank row is ignored); IT 66000; Finance with no guard gives #DIV/0!; guarded gives 0.
**Version note:** AVERAGEIF and AVERAGEIFS exist from Excel 2007, so all supported versions (from memory, unverified); also in Google Sheets.
**Edge cases:** A zero is counted, a blank is not. Showing 0 for "no data" may mislead; "n/a" is often better.
**Likely follow-ups:**
1. AVERAGEIF vs AVERAGEIFS argument order? The average range moves to the front in AVERAGEIFS.
2. Why not a pivot table? Also fine; formulas update live in a dashboard.
**Common mistakes:** Mixing up argument order; using average range of different size in AVERAGEIFS (gives an error); forgetting quotes around ">=3".

### Q43 ⭐⭐ 🟢 How do you find the highest salary in each department using MAXIFS, and what do you do in Excel 2016?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Conditional maximum and a backup for older Excel.
**Say this in the interview:** "MAXIFS gives the largest value that meets a condition. It is not in Excel 2016, so there I use MAX with IF as an array formula, or a SUMPRODUCT-MAX trick."
**Explain simply:**
- MAXIFS(max range, test range, condition) returns the biggest value among matching rows.
- Excel 2016 (non-365) does not have MAXIFS; it shows #NAME?.
- Array formula means one formula that works on a whole list at once.
**Example:** Highest salary in Sales, HR and IT, to check pay bands.
**Sample sheet:**

| | A | B | | D |
|---|---|---|---|---|
| 1 | Dept | Salary | | Dept |
| 2 | Sales | 40000 | | Sales |
| 3 | HR | 35000 | | HR |
| 4 | Sales | 52000 | | IT |
| 5 | IT | 60000 | | |
| 6 | HR | 41000 | | |
| 7 | Sales | 48000 | | |
| 8 | IT | 72000 | | |
| 9 | HR | 39000 | | |

**Formula / Steps:** In E2, copy down: `=MAXIFS($B$2:$B$9,$A$2:$A$9,D2)`
**Alternative (Excel 2016):** `=SUMPRODUCT(MAX(($A$2:$A$9=D2)*$B$2:$B$9))`. Another: `=MAX(IF($A$2:$A$9=D2,$B$2:$B$9))` confirmed with Ctrl+Shift+Enter (not run here). A pivot table with Max of Salary by Dept also works (not run here).
**Result:** (run) Sales 52000, HR 41000, IT 72000 for both MAXIFS and the SUMPRODUCT version.
**Version note:** MAXIFS is available in Excel 2019, 2021, 2024 and 365, not 2016 (Microsoft Support, "MAXIFS function"). Google Sheets has MAXIFS (from memory, unverified).
**Edge cases:** The SUMPRODUCT-MAX trick returns 0 if every matching value is negative or no row matches; MAXIFS returns 0 when nothing matches. Blank/text cells are ignored.
**Likely follow-ups:**
1. How to get the employee name too? INDEX/MATCH on the max salary (watch ties).
2. Lowest? MINIFS or MIN with IF.
**Common mistakes:** Forgetting $ anchors when copying down; typing the array formula without Ctrl+Shift+Enter in old Excel.

### Q44 ⭐⭐ 🟢 What is the SWITCH function, and when is it better than nested IF?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Choosing a readable formula when one cell is compared with many exact values.
**Say this in the interview:** "SWITCH checks one value against a list of exact options and returns the matching result, with an optional default. It is easier to read than a long nested IF when I am testing one cell for exact matches."
**Explain simply:**
- Syntax: SWITCH(value, option1, result1, option2, result2, ..., default).
- It only tests equality. For ranges like "60 or more", use IFS or the SWITCH(TRUE, ...) trick.
- Without a default and no match, SWITCH returns #N/A (Microsoft Support).
**Example:** Convert rating codes 1-5 into labels in an appraisal sheet.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | EmpID | Rating |
| 2 | E101 | 5 |
| 3 | E102 | 4 |
| 4 | E103 | 3 |
| 5 | E104 | 2 |
| 6 | E105 | 1 |
| 7 | E106 | 9 |

**Formula / Steps:** `=SWITCH(B2,5,"Outstanding",4,"Exceeds",3,"Meets",2,"Needs work","Unknown")`
**Alternative:** Nested IF: `=IF(B2=5,"Outstanding",IF(B2=4,"Exceeds",IF(B2=3,"Meets",IF(B2=2,"Needs work","Unknown"))))`. Range version: `=SWITCH(TRUE,B2>=5,"Top",B2>=3,"Middle","Low")`.
**Result:** (run) 5 gives Outstanding, 4 Exceeds, 3 Meets, 2 Needs work, 1 and 9 give Unknown (both formulas agree). The TRUE version gives Top, Middle, Middle, Low, Low, Top. Without a default, `=SWITCH(B3,5,"Outstanding")` gives #N/A.
**Version note:** SWITCH is in Excel 2019, 2021, 2024 and 365, not 2016 (Microsoft Support, "SWITCH function"). In Excel 2016 use nested IF or CHOOSE/VLOOKUP. Google Sheets has SWITCH (from memory, unverified).
**Edge cases:** Text matching ignores case; 5 and "5" (text) do not match. Up to 126 value/result pairs (Microsoft Support).
**Likely follow-ups:**
1. SWITCH vs IFS? IFS takes full conditions; SWITCH compares one value.
2. Better than both for many codes? A lookup table with VLOOKUP, so rules live in cells.
**Common mistakes:** Using SWITCH for ranges directly; forgetting the default; using it in Excel 2016.

### Q45 ⭐⭐ 🟡 How do you extract the domain from an email address such as "ravi@abc.com"?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Combining FIND with MID/RIGHT/LEFT to cut text at a marker.
**Say this in the interview:** "I find the position of the @ sign with FIND, then take everything after it with MID or RIGHT."
**Explain simply:**
- FIND("@",A2) tells you at which character the @ sits (ravi@abc.com gives 5).
- MID(text, start, length) cuts a piece out; start one past the @, length can be any big number.
- The part before @ is LEFT(A2, FIND("@",A2)-1).
**Example:** Group candidates by email provider to see how many applied with company versus gmail addresses.
**Sample sheet:**

| | A |
|---|---|
| 1 | Email |
| 2 | ravi@abc.com |
| 3 | meena.k@xyz.co.in |
| 4 | asha@mail.gmail.com |
| 5 | kiran@abc.com |
| 6 | no-at-sign |

**Formula / Steps:** `=MID(A2,FIND("@",A2)+1,100)`
**Alternative:** `=RIGHT(A2,LEN(A2)-FIND("@",A2))`. In Microsoft 365: `=TEXTAFTER(A2,"@")` (not run here; availability from memory, unverified). No formula: Data > Text to Columns with "@" as delimiter, or Flash Fill (Ctrl+E).
**Result:** (run) abc.com, xyz.co.in, mail.gmail.com, abc.com. Username with LEFT: ravi, meena.k, asha, kiran. Row 6 with `=IFERROR(MID(A6,FIND("@",A6)+1,100),"Invalid email")` gives Invalid email.
**Version note:** MID/FIND/RIGHT work in every version and Google Sheets. TEXTAFTER is only in Microsoft 365 and newer Excel (from memory, unverified).
**Edge cases:** No @ gives #VALUE! from FIND, so wrap with IFERROR. Leading/trailing spaces: use TRIM first. FIND is case-sensitive; SEARCH is not (irrelevant for @).
**Likely follow-ups:**
1. Get only "abc" without ".com"? Use FIND(".") on the domain result and LEFT.
2. Two @ signs? The first one is used; flag as invalid.
**Common mistakes:** Forgetting +1 so the @ is included; using a fixed number of characters; not handling blanks.

### Q46 ⭐⭐ 🟡 How do you calculate age in years, months and days from a date of birth?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** DATEDIF knowledge and awareness of its quirks.
**Say this in the interview:** "I use DATEDIF three times: "Y" for complete years, "YM" for the leftover months and "MD" for the leftover days, and join them with &. For today's age I replace the end date by TODAY()."
**Explain simply:**
- DATEDIF(start, end, unit) counts complete periods between two dates. It is a hidden function, so Excel does not suggest it while typing, but it works (Microsoft Support, "DATEDIF function").
- Units: "Y" years, "M" months, "D" days, "YM" months ignoring years, "MD" days ignoring months and years.
- Microsoft warns that "MD" can give negative or wrong results in some cases, so check month-end birthdays.
**Example:** HR needs exact age to check minimum joining age or retirement date. I use a fixed as-of date here (21 Oct 2026) so the answer is repeatable; in real life use TODAY().
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | DOB | As-of date |
| 2 | 20-Aug-1995 | 21-Oct-2026 |
| 3 | 29-Feb-2000 | 21-Oct-2026 |
| 4 | 31-Dec-1990 | 21-Oct-2026 |

**Formula / Steps:** `=DATEDIF(A2,B2,"Y")&" yrs "&DATEDIF(A2,B2,"YM")&" mths "&DATEDIF(A2,B2,"MD")&" days"`
**Alternative:** Years only: `=INT(YEARFRAC(A2,B2,1))`. Days left over without "MD": `=B2-EDATE(A2,DATEDIF(A2,B2,"Y")*12+DATEDIF(A2,B2,"YM"))`.
**Result:** (run in LibreOffice) row 2: 31 yrs 2 mths 1 days; row 3: 26 yrs 7 mths 22 days; row 4: 35 yrs 9 mths 20 days. The "MD" part for 31-Dec births can differ in real Excel because of the documented MD issue; verify with the EDATE alternative.
**Version note:** DATEDIF works in all versions but is undocumented in the function list; Google Sheets has DATEDIF (from memory, unverified).
**Edge cases:** Start date after end date gives #NUM!. Leap-day birthdays (29 Feb) are treated differently by different methods.
**Likely follow-ups:**
1. Tenure instead of age? Same formula with joining date.
2. Why not (TODAY()-DOB)/365? It ignores leap years and gives decimals.
**Common mistakes:** Dividing days by 365; typing dates as text; trusting "MD" blindly.

### Q47 ⭐⭐ 🟡 How do you get the last day of the month and the date six months from today?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** EOMONTH and EDATE, and whether you know Excel dates are numbers.
**Say this in the interview:** "EOMONTH(date, 0) gives the last day of the same month; EDATE(date, 6) gives the same day number six months later. With TODAY() as the date, both stay current."
**Explain simply:**
- Excel stores a date as a serial number (days counted from 1900), so you can add and subtract days. Format the result cell as Date, otherwise you see a number like 46326.
- EOMONTH(start, months): month-end after moving that many months. EDATE(start, months): same day, moved by months.
- If the target month is shorter, EDATE gives that month's last day.
**Example:** Probation ends six months after joining; payroll cut-off is month-end. I use 21-Oct-2026 as "today" so results are repeatable.
**Sample sheet:**

| | A (date) |
|---|---|
| 2 | 21-Oct-2026 |
| 3 | 31-Aug-2026 |
| 4 | 31-Jan-2026 |

**Formula / Steps:**
- Month end: `=EOMONTH(A2,0)`
- Six months later: `=EDATE(A2,6)` (live version: `=EDATE(TODAY(),6)`)
- First day of month: `=EOMONTH(A2,-1)+1`

**Alternative:** `=DATE(YEAR(A2),MONTH(A2)+6,DAY(A2))` (rolls over to the next month if the day does not exist, e.g. 31 Aug + 6 gives 3 Mar).
**Result:** (run; serial numbers converted to dates) A2: month end 31-Oct-2026; EDATE +6 gives 21-Apr-2027; EOMONTH +6 gives 30-Apr-2027; first of month 1-Oct-2026. A3: EDATE +6 gives 28-Feb-2027. A4: EDATE +1 gives 28-Feb-2026.
**Version note:** EDATE and EOMONTH work in all versions and Google Sheets (from memory, unverified).
**Edge cases:** TODAY() changes every day, so saved reports change; paste dates as values for a frozen report. Text dates give #VALUE!.
**Likely follow-ups:**
1. Last day of previous month? `=EOMONTH(A2,-1)`.
2. Why does my result show 46498? Format as Date.
**Common mistakes:** Adding 180 days for six months; forgetting date formatting; using TODAY() in a historical report.

### Q48 ⭐⭐ 🟡 How do you calculate the end date of a project, skipping weekends and holidays?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** WORKDAY with a holiday list.
**Say this in the interview:** "WORKDAY(start, days, holidays) returns the date after that many working days, skipping Saturdays, Sundays and any dates in my holiday list. NETWORKDAYS does the reverse: counts working days between two dates."
**Explain simply:**
- Working day means a weekday that is not a listed holiday.
- The holiday list is a range of real dates (not text).
- WORKDAY.INTL lets you define a different weekend (Microsoft Support, "WORKDAY function").
**Example:** A 15-working-day onboarding plan starting Monday 19 Oct 2026, with holidays on 20 Oct and 9 Nov (sample dates, not an official calendar).
**Sample sheet:**

| | A | B | | D |
|---|---|---|---|---|
| 1 | Start | Working days | | Holidays |
| 2 | 19-Oct-2026 | 15 | | 20-Oct-2026 |
| 3 | | | | 09-Nov-2026 |

**Formula / Steps:** `=WORKDAY(A2,B2,D2:D3)`
**Alternative:** Weekend other than Sat/Sun: `=WORKDAY.INTL(A2,B2,11,D2:D3)` (11 means only Sunday off). Verify with `=NETWORKDAYS(A2,C3,D2:D3)`.
**Result:** (run) without holidays: 9-Nov-2026; with holidays: 11-Nov-2026 (Wednesday). NETWORKDAYS from start to that end date returns 16 (it counts the start day, so days worked is 16 inclusive). WORKDAY.INTL: LibreOffice here returned #NAME? for it, so "not run here"; a numpy check with Sunday-only weekend and the same holidays gives 6-Nov-2026.
**Version note:** WORKDAY is available in Excel 2016 through 365 (Microsoft Support, "WORKDAY function"); WORKDAY.INTL from Excel 2010 (from memory, unverified). Google Sheets has both (from memory, unverified).
**Edge cases:** WORKDAY does not count the start date as day 1. Negative days go backwards. Holiday on a weekend has no effect.
**Likely follow-ups:**
1. Days in a date range? NETWORKDAYS.
2. Half-day holidays? Not handled; adjust manually.
**Common mistakes:** Holidays typed as text; adding days with + instead of WORKDAY; forgetting the date format.

### Q49 ⭐⭐ 🟡 How do you apply OR logic in SUMIFS, for example total sales for Mumbai or Delhi?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** You know SUMIFS is AND-only and can work around it.
**Say this in the interview:** "SUMIFS joins conditions with AND. For OR on the same column I either add two SUMIFS, or pass both cities as a list and wrap in SUM or SUMPRODUCT."
**Explain simply:**
- AND: all conditions must be true on the same row. OR: any one is enough.
- Asking for city = Mumbai AND city = Delhi on one cell can never be true, so you get 0.
- A list in curly brackets {"Mumbai","Delhi"} is an array constant (a fixed list typed inside the formula).
**Example:** Sales for two regions in a monthly report.
**Sample sheet:**

| | A | B | C | | E |
|---|---|---|---|---|---|
| 1 | City | Product | Sales | | Cities |
| 2 | Mumbai | A | 100 | | Mumbai |
| 3 | Delhi | B | 200 | | Delhi |
| 4 | Pune | A | 150 | | |
| 5 | Mumbai | A | 300 | | |
| 6 | Chennai | B | 250 | | |
| 7 | Delhi | B | 120 | | |
| 8 | Pune | A | 80 | | |
| 9 | Mumbai | B | 60 | | |

**Formula / Steps:** `=SUMIFS(C2:C9,A2:A9,"Mumbai")+SUMIFS(C2:C9,A2:A9,"Delhi")`
**Alternative:** `=SUM(SUMIFS(C2:C9,A2:A9,{"Mumbai","Delhi"}))`, or with cities in cells `=SUMPRODUCT(SUMIFS(C2:C9,A2:A9,E2:E3))`. Add another condition: `=SUMPRODUCT(SUMIFS(C2:C9,A2:A9,E2:E3,B2:B9,"A"))`.
**Result:** (run) all three approaches give 780. With product A as well: 400. The wrong attempt `=SUMIFS(C2:C9,A2:A9,"Mumbai",A2:A9,"Delhi")` gives 0.
**Version note:** Works in all versions from Excel 2007 and in 365 without special entry; in Google Sheets the array-constant form may need ARRAYFORMULA (unverified).
**Edge cases:** If the list has a duplicate city, it is counted twice. Different columns OR (Mumbai or product B) need SUMPRODUCT with (A=..)+(B=..)>0 logic.
**Likely follow-ups:**
1. OR across different columns? SUMPRODUCT with plus signs.
2. Many cities? Put them in a list range.
**Common mistakes:** Stacking two conditions on the same column; double counting rows that satisfy both ORs across columns.

### Q50 ⭐⭐ 🟡 How do you flag duplicate employee IDs with COUNTIF?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Anchored ranges and a practical data-cleaning formula.
**Say this in the interview:** "I count how many times each ID appears in the full list with COUNTIF; if the count is above 1, it is a duplicate. To keep the first and flag only repeats, I use an expanding range."
**Explain simply:**
- COUNTIF(range, criteria) counts cells equal to the criteria.
- A dollar sign ($) locks a reference so it does not move when copied down.
- Full-list count flags every copy; expanding-range count flags only the second and later copies.
**Example:** Joiner data from two HRMS exports merged; E102 appears three times.
**Sample sheet:**

| | A |
|---|---|
| 1 | EmpID |
| 2 | E101 |
| 3 | E102 |
| 4 | E103 |
| 5 | E102 |
| 6 | E104 |
| 7 | E101 |
| 8 | E105 |
| 9 | E102 |

**Formula / Steps:**
- All copies: `=IF(COUNTIF($A$2:$A$9,A2)>1,"Duplicate","")`
- Repeats only: `=IF(COUNTIF($A$2:A2,A2)>1,"Repeat","First")`

**Alternative:** Highlight: Home > Conditional Formatting > Highlight Cells Rules > Duplicate Values. Remove: Data > Data Tools > Remove Duplicates.
**Result:** (run) first formula marks rows 2, 3, 5, 7 and 9 as Duplicate (E101 twice, E102 three times). Second formula marks rows 5, 7, 9 as Repeat and the rest First. Rows flagged: `=SUMPRODUCT(--(COUNTIF(A2:A9,A2:A9)>1))` gives 5; unique IDs `=SUMPRODUCT(1/COUNTIF(A2:A9,A2:A9))` gives 5.
**Version note:** Works in all versions and Google Sheets. In 365, UNIQUE and COUNTIF-by-array also work (not run here).
**Edge cases:** COUNTIF is not case-sensitive; "e101" matches "E101". Trailing spaces make duplicates invisible; use TRIM. COUNTIF is limited to 255-character strings (Microsoft Support, "COUNTIF function").
**Likely follow-ups:**
1. Duplicates on two columns? COUNTIFS.
2. Very large data? COUNTIF gets slow; use a pivot table or Remove Duplicates.
**Common mistakes:** Forgetting $ so the range slides; deleting duplicates without checking which is the right record.

### Q51 ⭐⭐ 🟡 How do you count rows between two values (for example salary from 30,000 to 50,000) with COUNTIFS?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Two conditions on the same column, and inclusive versus exclusive limits.
**Say this in the interview:** "I use COUNTIFS on the same salary range twice: at least 30,000 and at most 50,000. Using >= and <= makes both ends inclusive."
**Explain simply:**
- COUNTIFS counts rows where all conditions are true (AND logic). It accepts the same range twice.
- Comparison signs sit inside quotes: ">=30000".
- To use a cell in the condition, join with &: ">="&E1.
**Example:** Number of employees in the 30k-50k salary band.
**Sample sheet:**

| | A | B | | D | E |
|---|---|---|---|---|---|
| 1 | Emp | Salary | | Low | 30000 |
| 2 | E1 | 28000 | | High | 50000 |
| 3 | E2 | 30000 | | | |
| 4 | E3 | 35000 | | | |
| 5 | E4 | 50000 | | | |
| 6 | E5 | 50001 | | | |
| 7 | E6 | 42000 | | | |
| 8 | E7 | 60000 | | | |
| 9 | E8 | 29999 | | | |

**Formula / Steps:** `=COUNTIFS(B2:B9,">=30000",B2:B9,"<=50000")`
**Alternative:** `=COUNTIFS(B2:B9,">="&E1,B2:B9,"<="&E2)`; or `=SUMPRODUCT((B2:B9>=E1)*(B2:B9<=E2))`; or `=COUNTIF(B2:B9,">=30000")-COUNTIF(B2:B9,">50000")`.
**Result:** (run) all four give 4 (30000, 35000, 50000, 42000). Using strict > and < gives 2. SUMIFS on the same conditions totals 157000.
**Version note:** COUNTIFS is available from Excel 2016 through 365 (Microsoft Support, "COUNTIFS function"); also in Google Sheets (from memory, unverified).
**Edge cases:** Salaries stored as text are not counted by numeric comparisons. Blank cells are ignored by ">=" conditions.
**Likely follow-ups:**
1. Add a department condition? Add another range/criteria pair.
2. Build bands? Use FREQUENCY or a pivot table with grouping.
**Common mistakes:** Writing >=30000 without quotes; using a single COUNTIF with two conditions; off-by-one on whether the limit is inclusive.

### Q52 ⭐⭐ 🟡 How do you find the quarter or financial year (April to March) from a date?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Date arithmetic for the Indian financial year.
**Say this in the interview:** "Calendar quarter is the month divided by 3, rounded up. For the Indian financial year, which runs April to March, I shift the months by three: April-June becomes Q1."
**Explain simply:**
- Financial year (FY) 2026-27 means 1 Apr 2026 to 31 Mar 2027.
- A date in Jan-Mar belongs to the FY that started the previous April.
- MOD(MONTH-4,12) turns April into 0, May into 1 ... March into 11; dividing by 3 gives the FY quarter.
**Example:** Hiring numbers by FY quarter for a board report.
**Sample sheet:**

| | A |
|---|---|
| 1 | Date |
| 2 | 31-Mar-2026 |
| 3 | 01-Apr-2026 |
| 4 | 15-Jun-2026 |
| 5 | 30-Sep-2026 |
| 6 | 05-Dec-2026 |
| 7 | 20-Jan-2027 |

**Formula / Steps:**
- Calendar quarter: `="Q"&ROUNDUP(MONTH(A2)/3,0)`
- FY quarter: `="Q"&(INT(MOD(MONTH(A2)-4,12)/3)+1)`
- FY label: `=IF(MONTH(A2)>=4,YEAR(A2),YEAR(A2)-1)&"-"&RIGHT(IF(MONTH(A2)>=4,YEAR(A2)+1,YEAR(A2)),2)`

**Alternative:** `="FY"&RIGHT(YEAR(EDATE(A2,9)),2)` (shift the date nine months forward; the year then is the FY end year). Or CHOOSE(MONTH(A2),"Q4","Q4","Q4","Q1",...).
**Result:** (run) calendar quarter: Q1, Q2, Q2, Q3, Q4, Q1. FY quarter: Q4, Q1, Q1, Q2, Q3, Q4. FY label: 2025-26, 2026-27 (rows 3-7). EDATE version: FY26, FY27, FY27, FY27, FY27, FY27.
**Version note:** All functions used work in every version and Google Sheets (from memory, unverified).
**Edge cases:** 31 Mar belongs to the old FY; 1 Apr to the new one. Text dates fail; check with ISNUMBER.
**Likely follow-ups:**
1. FY for a different start month? Change the 4 and the 9 shift.
2. Group in a pivot? Add a helper column, then pivot on it.
**Common mistakes:** Using calendar quarters for an April FY; mislabelling Jan-Mar with the wrong year.

### Q53 ⭐⭐ 🟡 How do you keep leading zeros in employee IDs, and how do you add them with a formula?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Difference between a number's value and its display, and text formatting.
**Say this in the interview:** "Excel drops leading zeros because it treats 00123 as the number 123. I either format the cells as Text before typing, use a custom number format 00000 to display zeros, or build the ID with TEXT."
**Explain simply:**
- A number format changes how a value looks; the value stays 123.
- Text keeps exactly what you typed but can no longer be summed.
- TEXT(value, "00000") makes a five-character text ID padded with zeros.
**Example:** Employee numbers 7, 42, 305 should show as 00007, 00042, 00305, or EMP0007.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Raw | Padded 5 | With prefix | RIGHT trick |
| 2 | 7 | | | |
| 3 | 42 | | | |
| 4 | 305 | | | |
| 5 | 12345 | | | |

**Formula / Steps:**
- Keep zeros when typing: select the column, Home > Number group > format box > Text, then type; or type an apostrophe first ('00123).
- Display only: Home > Number group > dialog launcher > Custom > type 00000.
- Formula in B2: `=TEXT(A2,"00000")`; C2: `="EMP"&TEXT(A2,"0000")`

**Alternative:** `=RIGHT("00000"&A2,5)`.
**Result:** (run) B: 00007, 00042, 00305, 12345; C: EMP0007, EMP0042, EMP0305, EMP12345; D equals B. A cell typed as text 00123 stays 00123 (length 5), but `=A6+0` returns 123.
**Version note:** Works in all versions and Google Sheets (from memory, unverified).
**Edge cases:** IDs longer than the pad (12345 with "0000") are not cut. Opening a CSV in Excel removes zeros; import via Data > From Text/CSV and set the column to Text. TEXT results are text, so VLOOKUP against numeric IDs fails.
**Likely follow-ups:**
1. Why VLOOKUP fails after padding? One side is text, the other number; make both text.
2. Remove zeros? `=VALUE(A2)` or `=A2*1`.
**Common mistakes:** Typing then formatting as Text (zeros are already lost); using custom format and assuming the text still contains zeros.

### Q54 ⭐⭐ 🟡 Why can a COUNTIF or SUMIF formula return the wrong result when copied down, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Absolute versus relative references.
**Say this in the interview:** "When I copy a formula down, Excel shifts normal references one row each time, so the range being searched slides away from the data. I lock it with dollar signs, like $A$2:$A$7, or use an Excel Table."
**Explain simply:**
- Relative reference (A2:A7) moves when copied; absolute reference ($A$2:$A$7) stays put.
- F4 cycles through the lock options while the cursor is on a reference.
- Another cause: ranges of different sizes; SUMIFS gives #VALUE! if they do not match.
**Example:** Counting how often a name appears in a list of six names.
**Sample sheet:**

| | A | | C |
|---|---|---|---|
| 1 | Name | | Who |
| 2 | Asha | | Asha |
| 3 | Ravi | | Asha |
| 4 | Meena | | Ravi |
| 5 | Asha | | Ravi |
| 6 | Kiran | | |
| 7 | Ravi | | |

**Formula / Steps:**
- Wrong (in D2, copied down): `=COUNTIF(A2:A8,C2)` becomes A3:A9, A4:A10, A5:A11
- Right: `=COUNTIF($A$2:$A$7,C2)`; select reference and press F4.

**Alternative:** Convert the list to a Table (Insert > Table) and use `=COUNTIF(Table1[Name],C2)`.
**Result:** (run) wrong copied-down formulas return 2, 1, 1, 1; the anchored formulas return 2, 2, 2, 2. Also (run): `=SUMIF(A2:A4,"a",B2:B5)` quietly returns 4 on mismatched ranges, while the SUMIFS equivalent gives #VALUE!.
**Version note:** Same in all versions and Google Sheets (from memory, unverified).
**Edge cases:** Ranges that grow when rows are added: use whole-column references or Tables. Inserting rows outside the fixed range will not extend it.
**Likely follow-ups:**
1. When do you want relative references? The criteria cell (C2), which should move.
2. Mixed reference? $A2 locks the column only.
**Common mistakes:** Locking the criteria cell too; checking only the first row; mismatched range sizes.

### Q55 ⭐⭐ 🟡 Why does COUNTIF not count numbers stored as text, or count them differently?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Text-versus-number awareness and data cleaning.
**Say this in the interview:** "It depends on the function. Numbers stored as text are still text, so COUNT and SUM ignore them, comparison criteria like >100 skip them, and exact matches may treat them differently. I convert them first so every formula agrees."
**Explain simply:**
- Number stored as text: looks like 101, but Excel holds it as words (often a green corner triangle, or left-aligned).
- The premise needs care: in real Excel, COUNTIF with criteria 101 is, from memory (unverified), documented to match both number 101 and text "101". My LibreOffice test did not agree with that for every case, so test on your own file.
- Operators like ">100" only look at true numbers.
- COUNTIF also loses precision for numbers over 15 digits (from memory, unverified).
**Example:** Employee codes imported from an HRMS with some typed as text.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Code | Amt |
| 2 | 101 (number) | 10 |
| 3 | 101 (text) | 20 |
| 4 | 102 (number) | 30 |
| 5 | 102 (text) | 40 |
| 6 | 103 (text) | 50 |
| 7 | " 101" (text with space) | 60 |

**Formula / Steps:**
1. Test: `=COUNTIF(A2:A7,101)`, `=COUNTIF(A2:A7,"101")`, `=COUNT(A2:A7)`, `=COUNTIF(A2:A7,">100")`
2. Convert: select the cells > click the warning icon > Convert to Number; or Data > Text to Columns > Finish; or multiply by 1 in a helper column.

**Alternative:** `=SUMPRODUCT(--(VALUE(TRIM(A2:A7))=101))` counts every version regardless of type.
**Result:** (run in LibreOffice) `COUNTIF(...,101)` 1; `COUNTIF(...,"101")` 2; COUNT 2; COUNTA 6; `COUNTIF(...,">100")` 2; `SUMIF(...,101,B2:B7)` 10; the SUMPRODUCT/VALUE/TRIM version 3 (catches the space). Excel may return 2 for the first line; this is a known LibreOffice vs Excel difference, not verified here.
**Version note:** Behaviour is the same across Excel versions (from memory, unverified); Google Sheets can differ (unverified).
**Edge cases:** Hidden spaces and non-breaking spaces keep a "number" as text; TRIM and CLEAN help. ID-like numbers longer than 15 digits (card numbers) match falsely.
**Likely follow-ups:**
1. How do you detect text numbers? `=ISTEXT(A2)` or COUNT versus COUNTA.
2. Best permanent fix? Clean at import with Power Query (not run here).
**Common mistakes:** Assuming all counting functions behave alike; converting only some rows.

### Q56 ⭐⭐ 🟡 How do you do a multi-condition count or sum with SUMPRODUCT, and when would you use it instead of COUNTIFS?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Array-style logic and knowing when COUNTIFS is not enough.
**Say this in the interview:** "SUMPRODUCT multiplies TRUE/FALSE tests together row by row and adds the result. I use COUNTIFS for ordinary AND conditions, and SUMPRODUCT when I need OR logic, calculations on the columns, or a case-sensitive match."
**Explain simply:**
- A test like (A2:A9="Sales") gives TRUE/FALSE for every row; TRUE counts as 1 and FALSE as 0 when multiplied.
- Multiplying tests is AND; adding tests is OR.
- Multiply by a number column to get a sum.
- It does not need Ctrl+Shift+Enter, but is slower on big data than COUNTIFS.
**Example:** Sales staff earning at least 50,000, and total pay of women in Sales.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Dept | Gender | Salary |
| 2 | Sales | F | 52000 |
| 3 | HR | M | 38000 |
| 4 | Sales | M | 47000 |
| 5 | IT | F | 65000 |
| 6 | Sales | F | 58000 |
| 7 | HR | F | 41000 |
| 8 | IT | M | 70000 |
| 9 | Sales | F | 36000 |

**Formula / Steps:**
- Count: `=SUMPRODUCT((A2:A9="Sales")*(C2:C9>=50000))`
- Sum: `=SUMPRODUCT((A2:A9="Sales")*(B2:B9="F")*C2:C9)`
- OR (Sales or IT) with salary >= 50000: `=SUMPRODUCT(--(((A2:A9="Sales")+(A2:A9="IT"))>0),--(C2:C9>=50000))`

**Alternative:** `=COUNTIFS(A2:A9,"Sales",C2:C9,">=50000")` and `=SUMIFS(C2:C9,A2:A9,"Sales",B2:B9,"F")`.
**Result:** (run) count 2 (both methods); sum 146000 (both methods); OR version 4. Average Sales salary via SUMPRODUCT 48250. Case-sensitive test `=SUMPRODUCT(--EXACT(A2:A9,"sales"))` gives 0 because stored text is "Sales".
**Version note:** SUMPRODUCT works in all versions and Google Sheets (from memory, unverified).
**Edge cases:** Ranges must be the same size or you get #VALUE!. Errors in any cell (such as #N/A) make the whole result an error. Text in the number column is treated as 0 in the comma form but breaks the multiply form.
**Likely follow-ups:**
1. Why the double minus (--)? It turns TRUE/FALSE into 1/0.
2. Faster? COUNTIFS/SUMIFS on large data.
**Common mistakes:** Mismatched range sizes; mixing comma and * forms; using it where COUNTIFS is simpler.

### Q57 ⭐⭐ 🟡 How do you list headcount by joining month from a table of joining dates?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Counting by month, including the trap of mixing different years.
**Say this in the interview:** "I list the first day of each month and count joining dates that are on or after that day and before the first of the next month with COUNTIFS. For a quick look I can use a pivot table grouped by month and year."
**Explain simply:**
- A date is a number, so "within January 2026" means >= 1 Jan and < 1 Feb.
- Using only MONTH() ignores the year, so Jan 2026 and Jan 2027 would be combined.
- Headcount here means the number of people who joined in that month; do not confuse it with total employees on the roll.
**Example:** Eight joiners across 2026-27; the monthly counts feed a hiring trend chart.
**Sample sheet:**

| | A | B | | D |
|---|---|---|---|---|
| 1 | Emp | Joined | | Month start |
| 2 | E1 | 10-Jan-2026 | | 01-Jan-2026 |
| 3 | E2 | 25-Jan-2026 | | 01-Feb-2026 |
| 4 | E3 | 03-Feb-2026 | | 01-Mar-2026 |
| 5 | E4 | 14-Feb-2026 | | 01-Apr-2026 |
| 6 | E5 | 28-Feb-2026 | | |
| 7 | E6 | 05-Apr-2026 | | |
| 8 | E7 | 08-Jan-2027 | | |
| 9 | E8 | 20-Apr-2026 | | |

**Formula / Steps:** In E2 (copy down): `=COUNTIFS($B$2:$B$9,">="&D2,$B$2:$B$9,"<"&EDATE(D2,1))`
Pivot route (not run here): select data > Insert > PivotTable > put Joined in Rows, right-click a date > Group > Months and Years; put Emp in Values as Count.
**Alternative:** `=SUMPRODUCT((MONTH($B$2:$B$9)=MONTH(D2))*(YEAR($B$2:$B$9)=YEAR(D2)))`. Label: `=TEXT(D2,"mmm yyyy")`.
**Result:** (run) Jan 2026: 2; Feb 2026: 3; Mar 2026: 0; Apr 2026: 2; total of the four months 7 versus 8 joiners (the eighth joined Jan 2027). Month-only SUMPRODUCT (`MONTH()=1` without the year) returns 3 for January because it wrongly includes Jan 2027.
**Version note:** COUNTIFS, EDATE and pivot grouping work in Excel 2016 through 365 (COUNTIFS: Microsoft Support). Google Sheets supports them (unverified).
**Edge cases:** Dates with a time part (for example 31-Jan 14:00) still count correctly with the "<" next-month method. Dates stored as text are not counted.
**Likely follow-ups:**
1. Cumulative headcount? Running sum of the monthly counts minus leavers.
2. Months with zero joiners? Keep the month list typed so zero shows.
**Common mistakes:** Ignoring the year; using <= end-of-month with times; forgetting that blank months disappear in a pivot unless you show empty items.

### Q58 ⭐⭐ 🟡 How do you show a line break inside a cell using a formula, and combine several cells with commas?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know CHAR(10), Wrap Text and TEXTJOIN, and can you build text from several cells?
**Say this in the interview:** "A line break is character number 10, so I write A2&CHAR(10)&B2 and switch on Wrap Text. To join many cells with commas I use TEXTJOIN, or the & sign if the file must open in older Excel."
**Explain simply:**
- `&` glues text together. `CHAR(10)` is the hidden "new line" character (Windows Excel; on Mac older versions used CHAR(13)).
- The line break is invisible until you turn on **Wrap Text** (Home > Alignment > Wrap Text). Without it you see one long line.
- `TEXTJOIN(separator, ignore_empty, range)` joins a whole range in one go and can skip blanks.
**Example:** An HR mailing label needs "Asha / Rao / HR" on three lines, and a report needs the list of departments "HR, Payroll, Hiring" in one cell.
**Sample sheet:**
| | A | B | C |
|---|---|---|---|
| 1 | First | Last | Dept |
| 2 | Asha | Rao | HR |
| 3 | Vikram | Nair | Payroll |
| 4 | Meera | Iyer | Hiring |

**Formula / Steps:**
1. Line break: `=A2&CHAR(10)&B2&CHAR(10)&C2`, then Home > Alignment > Wrap Text.
2. Commas, one row: `=TEXTJOIN(", ",TRUE,A2:C2)`
3. Commas, a column: `=TEXTJOIN(", ",TRUE,C2:C4)`
**Alternative:** `=A2&", "&B2&", "&C2` works in every version. Or Find & Replace: Ctrl+J in the "Find what" box finds a line break.
**Result (run in LibreOffice):** line-break formula returns "Asha", "Rao", "HR" on three lines; `=TEXTJOIN(", ",TRUE,A2:C2)` returns `Asha, Rao, HR`; `=TEXTJOIN(", ",TRUE,C2:C4)` returns `HR, Payroll, Hiring`.
**Version note:** TEXTJOIN is Excel 2019, 2021, 365 only (Microsoft Support, "TEXTJOIN function"); not in Excel 2016, so use `&`. Google Sheets has TEXTJOIN too (from memory, unverified).
**Edge cases:** With ignore_empty FALSE, blank cells leave a stray ", " (run: `HR, Payroll, Hiring, ` when a blank cell was included). Text joined with TEXTJOIN is limited to 32,767 characters per cell (Microsoft Support, "Excel specifications and limits").
**Likely follow-ups:**
1. *Why doesn't my line break show?* Wrap Text is off.
2. *Can I join with a line break?* Yes: `=TEXTJOIN(CHAR(10),TRUE,A3:C3)` (run: returns the three values on separate lines).
**Common mistakes:** Typing "\n" (Excel does not understand it); forgetting Wrap Text; forgetting the space after the comma.

### Q59 ⭐⭐ 🟡 How do you use IF with text and dates, for example "Overdue" if the due date is before today?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you compare dates with TODAY() and return text, and handle blanks?
**Say this in the interview:** "I compare the due date to TODAY(): =IF(B2<TODAY(),"Overdue","On time"). Text results go in quotes. I also guard for completed tasks and blank dates."
**Explain simply:**
- Excel stores dates as serial numbers (days since 1900), so "<" works on dates like on numbers.
- `TODAY()` returns today's date and recalculates every time the file opens (a "volatile" function).
- Text you want returned goes in double quotes; to test text, compare with `="Done"`.
**Example:** HR task tracker: "Done" tasks should never show Overdue; blank due dates should show "No date" (a blank counts as 0, which is before today, so it would wrongly say Overdue).
**Sample sheet:** (as-of date in F1 = 21-Oct-2026 so the result is repeatable; replace `$F$1` by `TODAY()` in real use)
| | A | B | C |
|---|---|---|---|
| 1 | Task | Due | Status |
| 2 | Offer letters | 15-Oct-26 | Open |
| 3 | Payroll input | 21-Oct-26 | Open |
| 4 | Exit interview | 30-Oct-26 | Open |
| 5 | Induction deck | 10-Oct-26 | Done |
| 6 | Policy sign-off | (blank) | Open |

**Formula / Steps:** Basic: `=IF(B2<TODAY(),"Overdue","On time")`. Safe: `=IF(C2="Done","Done",IF(B2="","No date",IF(B2<TODAY(),"Overdue","On time")))`
**Alternative:** `=IF(AND(C2<>"Done",B2<>"",B2<TODAY()),"Overdue","OK")`, or `=IFS(...)` in 2019+.
**Result (run with $F$1 = 21-Oct-2026):** basic formula: Overdue, On time, On time, Overdue, Overdue (wrong for rows 5 and 6). Safe formula: Overdue, On time, On time, Done, No date.
**Version note:** IF and TODAY work in all versions and in Google Sheets.
**Edge cases:** Due today is "On time" because `<` is strict. Dates typed as text (e.g. "15/10/2026" left-aligned) compare wrongly; convert with DATEVALUE.
**Likely follow-ups:**
1. *Overdue only by 7+ days?* `B2<TODAY()-7`.
2. *Freeze today's date?* Type a static date or use Ctrl+; instead of TODAY().
**Common mistakes:** Putting the date in quotes without DATEVALUE; forgetting blanks equal 0; forgetting quotes round "Overdue".

### Q60 ⭐⭐ 🔴 How many IF functions can you nest, and what are the alternatives to deep nesting?
**Asked at:** Candidate reports (Glassdoor MIS pages, seen only as search snippets) mention nested IF for grades; no company-specific attribution is made.
**What the interviewer is checking:** Do you know the limit (64) and, more importantly, cleaner options?
**Say this in the interview:** "Excel allows 64 nested levels, but anything beyond three or four is hard to read and fix. I use IFS, or better a small lookup table with approximate-match VLOOKUP or LOOKUP."
**Explain simply:**
- "Nesting" means putting one IF inside another so you can test several conditions in order.
- The limit is 64 nested levels of functions (Microsoft Support, "Excel specifications and limits").
- A lookup table keeps the rules visible: change the grade bands in the table, not in 40 formulas.
**Example:** Performance rating from a score: 90+ = A, 75+ = B, 60+ = C, 45+ = D, else F.
**Sample sheet:** (A2:A6 scores; table in F2:G6)
| | A | F | G |
|---|---|---|---|
| 1 | Score | Min | Grade |
| 2 | 92 | 0 | F |
| 3 | 78 | 45 | D |
| 4 | 64 | 60 | C |
| 5 | 51 | 75 | B |
| 6 | 40 | 90 | A |

**Formula / Steps:** Nested: `=IF(A2>=90,"A",IF(A2>=75,"B",IF(A2>=60,"C",IF(A2>=45,"D","F"))))`
**Alternative:** `=IFS(A2>=90,"A",A2>=75,"B",A2>=60,"C",A2>=45,"D",TRUE,"F")`; table: `=VLOOKUP(A2,$F$2:$G$6,2,TRUE)` or `=LOOKUP(A2,$F$2:$F$6,$G$2:$G$6)`. Others: SWITCH, CHOOSE+MATCH.
**Result (run):** all four methods return A, B, C, D, F for 92, 78, 64, 51, 40.
**Version note:** IFS needs Excel 2019/365 (Microsoft Support, "IFS function"); the nested IF and the table approach work in every version.
**Edge cases:** The table must be sorted ascending for approximate match. IF tests run top to bottom, so order the conditions correctly. IFS gives #N/A if nothing is true unless you add `TRUE,"F"` at the end.
**Likely follow-ups:**
1. *Why not nest 20 IFs?* Unreadable and error-prone.
2. *Difference IFS vs nested IF?* Same logic, flatter writing.
**Common mistakes:** Wrong order of conditions; unsorted lookup table; missing a closing bracket per IF.

### Q61 ⭐⭐ 🔴 How do you count the number of unique values in a column using a formula?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you count distinct items, not rows (e.g. employees, not attendance entries)?
**Say this in the interview:** "In 365 I use COUNTA(UNIQUE(range)). In older versions SUMPRODUCT(1/COUNTIF(range,range)), with a blank-safe variation."
**Explain simply:**
- "Unique" here means distinct: E101 appearing 3 times counts as 1.
- `COUNTIF(range,range)` gives, for every cell, how many times it appears. `1/that` gives each value weights that add up to 1 per distinct item. `SUMPRODUCT` adds them.
- Blanks break it: COUNTIF of a blank gives 0, so 1/0 gives #DIV/0!.
**Example:** An attendance log has several rows per employee; the question is "how many different employees were present?"
**Sample sheet:**
| | A |
|---|---|
| 1 | Emp ID |
| 2 | E101 |
| 3 | E102 |
| 4 | E101 |
| 5 | E103 |
| 6 | (blank) |
| 7 | E102 |
| 8 | E101 |
| 9 | E104 |

**Formula / Steps:** Blank-safe: `=SUMPRODUCT((A2:A9<>"")/COUNTIF(A2:A9,A2:A9&""))`
**Alternative:** 365/2021: `=COUNTA(UNIQUE(A2:A9,,FALSE))` (blank still counted as one in some cases; filter first with `UNIQUE(FILTER(A2:A9,A2:A9<>""))`). Or a PivotTable with "Add this data to the Data Model" > Distinct Count.
**Result:** blank-safe SUMPRODUCT returns **4** (run). The plain `SUMPRODUCT(1/COUNTIF(A2:A9,A2:A9))` returns #DIV/0! (run). On A2:A5 only (no blank), the plain version returns 3 (run). UNIQUE version: **not run here**; by hand it gives E101, E102, E103, E104, so 4 once blanks are removed.
**Version note:** UNIQUE exists only in Excel 2021, 2024 and 365 (Microsoft Support, "UNIQUE function"). SUMPRODUCT works everywhere.
**Edge cases:** Text with trailing spaces or different case: COUNTIF ignores case but not spaces. SUMPRODUCT/COUNTIF becomes slow on 100,000+ rows.
**Likely follow-ups:**
1. *Count of values that appear only once?* `=SUMPRODUCT(--(COUNTIF(A2:A9,A2:A9)=1))` (E103 and E104 only; E101 and E102 repeat).
2. *Google Sheets?* `=COUNTUNIQUE(A2:A9)` (from memory, unverified).
**Common mistakes:** Counting rows with COUNTA; leaving blanks in the range; forgetting that the plain formula errors out.

### Q62 ⭐⭐ 🔴 How do you count the number of error cells in a range?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know ISERROR and SUMPRODUCT, and the difference between all errors and one type?
**Say this in the interview:** "=SUMPRODUCT(--ISERROR(range)) counts every kind of error. If I only want one type, COUNTIF with the error text, or ISNA for #N/A."
**Explain simply:**
- `ISERROR` checks each cell and says TRUE/FALSE. `--` turns TRUE/FALSE into 1/0. `SUMPRODUCT` adds the 1s.
- Common errors: #DIV/0! (divide by zero), #N/A (lookup found nothing), #VALUE! (text where a number is needed).
- Counting them is a data-quality check before reporting.
**Example:** Pay per day = Salary / Days worked. One employee has 0 days (#DIV/0!), one has "TBD" salary (#VALUE!).
**Sample sheet:**
| | A | B | C | D (=B/C) | E (VLOOKUP) |
|---|---|---|---|---|---|
| 2 | E101 | 60000 | 30 | 2000 | HR |
| 3 | E102 | 45000 | 0 | #DIV/0! | Pay |
| 4 | E103 | 52000 | 28 | 1857.14 | Hire |
| 5 | E104 | TBD | 30 | #VALUE! | #N/A |
| 6 | E105 | 48000 | 26 | 1846.15 | #N/A |
| 7 | E106 | 39000 | 25 | 1560 | #N/A |

**Formula / Steps:** `=SUMPRODUCT(--ISERROR(D2:D7))`
**Alternative:** One type: `=COUNTIF(D2:D7,"#DIV/0!")`, `=SUMPRODUCT(--ISNA(E2:E7))`. Manual: Home > Find & Select > Go To Special > Formulas > Errors (selects them; the count shows in the status bar/selection). 
**Result (run):** `SUMPRODUCT(--ISERROR(D2:D7))` = 2; over D2:E7 = 5; `ISNA(E2:E7)` = 3; `COUNTIF(D2:D7,"#DIV/0!")` = 1.
**Version note:** Works in all Excel versions and Google Sheets (Sheets: wrap in ARRAYFORMULA if needed, from memory, unverified). Old Excel with plain `SUM(IF(ISERROR(...)))` needs Ctrl+Shift+Enter.
**Edge cases:** Do not use SUMPRODUCT on a range of values that itself computes errors inside the multiplication; ISERROR is safe because it catches them first. COUNTIF with a wildcard cannot count errors in general.
**Likely follow-ups:**
1. *How to hide errors?* IFERROR (but fix the cause first).
2. *Difference between IFERROR and IFNA?* IFNA only hides #N/A.
**Common mistakes:** Using COUNTIF(range,"#N/A") and thinking it counts all errors; hiding errors instead of finding them.

### Q63 ⭐ 🟢 What does the EXACT function do, and is COUNTIF case-sensitive?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know COUNTIF ignores case and how to count case-sensitively?
**Say this in the interview:** "EXACT compares two texts and says TRUE only if they match including capital letters. COUNTIF is not case-sensitive; for a case-sensitive count I use SUMPRODUCT with EXACT."
**Explain simply:**
- `=` and COUNTIF treat "HR" and "hr" as the same. EXACT does not.
- EXACT also notices extra spaces: "HR " is not "HR".
- COUNTIF being case-insensitive is stated by Microsoft Support ("Use the COUNTIF function").
**Example:** Employee codes where "HR" (department) and "hr" (a typo) must be told apart.
**Sample sheet:**
| | A |
|---|---|
| 2 | HR |
| 3 | hr |
| 4 | Hr |
| 5 | HR (trailing space) |
| 6 | HRBP |
| 7 | HR |

**Formula / Steps:** `=EXACT(A2,A3)`; case-sensitive count: `=SUMPRODUCT(--EXACT(A2:A7,"HR"))`
**Alternative:** `=SUMPRODUCT(--(A2:A7="HR"))` is case-insensitive (same as COUNTIF); or use FIND (case-sensitive) for partial matches.
**Result (run):** `EXACT(A2,A3)` = FALSE; `EXACT(A2,A7)` = TRUE; `EXACT(A2,A5)` = FALSE; `COUNTIF(A2:A7,"HR")` = 4; `SUMPRODUCT(--EXACT(A2:A7,"HR"))` = 2.
**Version note:** All versions and Google Sheets (Sheets from memory, unverified).
**Edge cases:** Numbers and text-numbers: EXACT(1,"1") returns TRUE (it converts to text). Blank vs "" are equal.
**Likely follow-ups:**
1. *Is VLOOKUP case-sensitive?* No.
2. *Case-sensitive lookup?* INDEX/MATCH with EXACT in an array formula.
**Common mistakes:** Assuming `=` is case-sensitive; forgetting the `--`.

### Q64 ⭐ 🟢 What do the WORKDAY and YEARFRAC functions do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you calculate working-day deadlines and fractional years of service?
**Say this in the interview:** "WORKDAY gives the date that is N working days after a start date, skipping weekends and listed holidays. YEARFRAC gives the fraction of a year between two dates, such as 3.55 years of service."
**Explain simply:**
- `WORKDAY(start, days, [holidays])`: positive days go forward, negative go back (Microsoft Support, "WORKDAY function"). Saturday and Sunday are skipped.
- `YEARFRAC(start, end, [basis])`: basis 0/omitted = 30/360, 1 = actual/actual, 2 = actual/360, 3 = actual/365, 4 = European 30/360 (Microsoft Support, "YEARFRAC function").
- NETWORKDAYS counts working days; WORKDAY finds the date.
**Example:** Asha resigns on 22-Oct-2026 with a 30-working-day notice; company holidays 29-Oct and 9-Nov. When is her last day? And what is her tenure?
**Sample sheet:**
| | B (Resigned) | C (Joined) | F | H (Holidays) |
|---|---|---|---|---|
| 2 | 22-Oct-26 | 03-Apr-23 | As-of 22-Oct-26 | 29-Oct-26 |
| 3 | 01-Oct-26 | 22-Oct-25 | | 09-Nov-26 |

**Formula / Steps:** Last day: `=WORKDAY(B2,30,$H$2:$H$3)`. Tenure: `=YEARFRAC(C2,$F$2,1)`
**Alternative:** `=WORKDAY.INTL(B2,30,1,$H$2:$H$3)` for other weekends; tenure in whole years `=DATEDIF(C2,$F$2,"Y")`.
**Result (run):** `WORKDAY(B2,30)` = 03-Dec-2026; with holidays = 07-Dec-2026; `WORKDAY(B3,10)` = 15-Oct-2026. `YEARFRAC(C2,F2)` = 3.553 (basis 0), basis 1 = 3.554, `DATEDIF(...,"Y")` = 3, `ROUND(YEARFRAC(C2,F2,1),1)` = 3.6. `YEARFRAC(C3,F2)` = 1.
**Version note:** Both work in Excel 2016 and later (Microsoft Support pages list 2016 to 365); in Google Sheets as well (from memory, unverified).
**Edge cases:** WORKDAY ignores the start day itself (day 0). Holidays that fall on weekends make no difference. Format the result cell as a date or you see a serial number (46359).
**Likely follow-ups:**
1. *Half-day holidays?* Not supported.
2. *Which basis for tenure?* 1 is the most intuitive.
**Common mistakes:** Forgetting the holiday list; leaving result as a number; assuming YEARFRAC equals DATEDIF.

### Q65 ⭐ 🟢 How do you repeat a character or text, for example a star rating, with REPT?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use REPT for quick in-cell visuals?
**Say this in the interview:** "REPT repeats text a number of times. =REPT("★",B2) turns a rating of 4 into four stars; I can add empty stars for the rest."
**Explain simply:**
- `REPT(text, number_times)`: repeat the text that many times.
- It makes a small bar chart inside a cell without a chart object.
- The number can be a calculation, e.g. `B2*3`.
**Example:** Manager rating 1 to 5 shown as stars on a feedback sheet.
**Sample sheet:**
| | A | B |
|---|---|---|
| 1 | Employee | Rating |
| 2 | Asha | 5 |
| 3 | Vikram | 3 |
| 4 | Meera | 4 |
| 5 | Rohit | 1 |
| 6 | Isha | 0 |

**Formula / Steps:** `=REPT("★",B2)&REPT("☆",5-B2)`
**Alternative:** Bar: `=REPT("|",B2*3)`; or Conditional Formatting > Icon Sets / Data Bars (Home > Styles > Conditional Formatting).
**Result (run):** Asha ★★★★★; Vikram ★★★☆☆; Meera ★★★★☆; Rohit ★☆☆☆☆; Isha ☆☆☆☆☆. `REPT("ab",3)` = ababab.
**Version note:** All versions and Google Sheets (Sheets from memory, unverified).
**Edge cases:** Negative count gives #VALUE! (run); decimals are cut down (REPT("★",2.9) gave ★★, run); result cannot exceed 32,767 characters.
**Likely follow-ups:**
1. *How to type ★?* Insert > Symbol, or `UNICHAR(9733)` in 2013+.
2. *Make the stars gold?* Format the cell font colour.
**Common mistakes:** Rating above 5 makes `5-B2` negative and returns #VALUE!; forgetting quotes.

### Q66 ⭐ 🟢 Which functions in this part are available only in Excel 2019 or 365, and what do you use in Excel 2016?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Version awareness: will your file break on a colleague's older Excel?
**Say this in the interview:** "IFS, SWITCH, MAXIFS, TEXTJOIN and CONCAT need Excel 2019 or 365. UNIQUE, FILTER and XLOOKUP need 2021 or 365. TEXTSPLIT needs 365 or 2024. For 2016 I use nested IF, INDEX/MATCH, SUMPRODUCT and the & sign."
**Explain simply:** Availability from Microsoft Support pages fetched: IFS, SWITCH, MAXIFS, CONCAT, TEXTJOIN (Office 2019 or 365); UNIQUE (2021, 2024, 365); TEXTSPLIT (365, 2024); XLOOKUP (the page's note says it is not available in 2016 and 2019, although its Applies-to list names them).
**Example:** You send a 365 workbook with IFS to a manager on Excel 2016: the cell shows #NAME?.
**Sample sheet / table:**
| New function | Needs | Excel 2016 substitute |
|---|---|---|
| IFS | 2019+ | nested IF or lookup table |
| SWITCH | 2019+ | CHOOSE+MATCH or nested IF |
| MAXIFS / MINIFS | 2019+ | `SUMPRODUCT(MAX((cond)*range))` |
| TEXTJOIN, CONCAT | 2019+ | `&` |
| UNIQUE | 2021/365 | `SUMPRODUCT(1/COUNTIF())`, Remove Duplicates |
| XLOOKUP | 365/2021 | INDEX/MATCH |
| TEXTBEFORE/AFTER/SPLIT | 365 | LEFT/MID/FIND, Text to Columns |

**Formula / Steps:** `=MAXIFS(B2:B5,A2:A5,"HR")` becomes `=SUMPRODUCT(MAX((A2:A5="HR")*B2:B5))`
**Alternative:** Check File > Account > About Excel to see your version.
**Result (run):** MAXIFS = 65 and the SUMPRODUCT version = 65 on data HR 50/65 (rows 2 and 4), Sales 70, IT 40; CONCAT(A2:A5) and `A2&A3&A4&A5` both return HRSalesHRIT; SWITCH and CHOOSE+MATCH both return Human Resources.
**Version note:** TEXTBEFORE/TEXTAFTER availability is from memory, unverified (the TEXTBEFORE page 404ed when fetched); Microsoft's TEXTSPLIT page was read. The SUMPRODUCT/MAX trick fails if the range contains negatives (zero would win) or text.
**Edge cases:** Google Sheets has most of these (IFS, SWITCH, MAXIFS, TEXTJOIN, UNIQUE, FILTER) (from memory, unverified).
**Likely follow-ups:** *Will it open in 2016?* The file opens but new functions show #NAME?.
**Common mistakes:** Using 365 functions in shared files without checking users' versions.

### Q67 ⭐ 🟢 How do COUNTIFS and SUMIFS differ in Google Sheets compared with Excel?
**Asked at:** Candidate reports (Glassdoor MIS analyst pages, search snippet only) mention COUNTIFS/SUMIFS tests and Google Sheets use; no company-specific attribution.
**What the interviewer is checking:** Do you know the two behave almost the same, and the small differences?
**Say this in the interview:** "The syntax and logic are the same: range, criterion pairs, all must be true. The differences are small: array handling needs ARRAYFORMULA in Sheets, and wildcard and whole-column behaviour can differ."
**Explain simply:**
- Same syntax: `COUNTIFS(range1, crit1, range2, crit2…)`; `SUMIFS(sum_range, range1, crit1…)` (Google Docs Editors Help pages for COUNTIFS and SUMIFS, fetched).
- Ranges must be the same size in both (Google's COUNTIFS page says so; Microsoft Support too).
- Excel's COUNTIFS page describes wildcards ? and * and the ~ escape; Google's COUNTIFS page does not mention wildcards (though Sheets does support them in text criteria, from memory, unverified).
- In Sheets, passing a whole range as criteria to get several answers at once needs `ARRAYFORMULA`; Excel 365 spills automatically.
**Example:** Count of employees in "HR" who joined after 1-Jan-2025: `=COUNTIFS(A:A,"HR",B:B,">"&DATE(2025,1,1))` in either tool.
**Formula / Steps:** Same formula in both. Google: `=ARRAYFORMULA(COUNTIFS(A2:A,E2:E4))` for several criteria (**not run here**, from memory).
**Alternative:** Google Sheets QUERY function, Excel PivotTable.
**Version note:** COUNTIFS/SUMIFS exist from Excel 2007; Sheets always has them. Differences in regex-based criteria settings in Sheets are from memory, unverified.
**Edge cases:** Dates as text, trailing spaces, and criteria like ">"&cell work the same way.
**Likely follow-ups:** *Does COUNTIFS accept OR?* No; add two COUNTIFS or use SUMPRODUCT.
**Common mistakes:** Unequal range sizes; forgetting quotes around operators.

### Q68 ⭐ 🟡 What are TEXTBEFORE, TEXTAFTER and TEXTSPLIT, and how do they replace LEFT/MID/FIND?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the modern text functions and the classic way for older versions?
**Say this in the interview:** "TEXTBEFORE and TEXTAFTER return the text before or after a delimiter, and TEXTSPLIT splits into several cells. They replace the LEFT/MID plus FIND combination, but only in 365."
**Explain simply:**
- A "delimiter" is the separator character, like "@" or ",".
- `TEXTBEFORE(text, delimiter)`, `TEXTAFTER(text, delimiter)`, `TEXTSPLIT(text, col_delimiter, [row_delimiter], …)` spills the parts across cells (syntax from Microsoft Support, "TEXTSPLIT function", fetched).
- Old way: `FIND` locates the character position, `LEFT`/`MID` cuts there.
**Example:** Get the user name and domain from work emails.
**Sample sheet:**
| | A | B | C |
|---|---|---|---|
| 2 | ananya.rao@acme.com | | |
| 3 | vikram.nair@acme.in | | |
| 4 | no-email | | |

**Formula / Steps:** Classic: B2 `=LEFT(A2,FIND("@",A2)-1)`; C2 `=MID(A2,FIND("@",A2)+1,100)`. New: `=TEXTBEFORE(A2,"@")`, `=TEXTAFTER(A2,"@")`, `=TEXTSPLIT(A2,"@")`.
**Alternative:** Data > Text to Columns (feature route, any version, but static, not formula-driven).
**Result:** Classic formulas (run): row 2 gives ananya.rao and acme.com; row 3 gives vikram.nair and acme.in; row 4 gives #VALUE! (no "@"). New functions: **not run here**; by hand they return the same text, and TEXTBEFORE returns #N/A when the delimiter is missing (from memory).
**Version note:** TEXTSPLIT is Excel 365 and 2024 only (Microsoft Support); TEXTBEFORE/TEXTAFTER the same family (from memory, unverified). Not in 2016/2019/2021.
**Edge cases:** Missing delimiter; several delimiters (TEXTBEFORE has an instance number argument, from memory); trim spaces with TRIM. Wrap classic version in IFERROR.
**Likely follow-ups:** *Split into rows?* TEXTSPLIT row_delimiter argument.
**Common mistakes:** Forgetting -1/+1 in the classic formula; using these in Excel 2019.

### Q69 ⭐ 🟡 What are ARRAYFORMULA and the REGEX functions in Google Sheets, and how do they compare with Excel?
**Asked at:** Candidate reports (Glassdoor MIS analyst pages, search snippet) mention Google Sheets ARRAYFORMULA/QUERY; no company-specific attribution.
**What the interviewer is checking:** Google Sheets awareness and array thinking.
**Say this in the interview:** "ARRAYFORMULA makes one formula fill a whole column. REGEXMATCH, REGEXEXTRACT and REGEXREPLACE find or clean text using patterns. Excel 365 spills arrays automatically, and does not have the same REGEX set in all builds."
**Explain simply:**
- ARRAYFORMULA lets a formula work on a whole range and spill results (Google Docs Editors Help, "ARRAYFORMULA", fetched); many array formulas now expand automatically.
- "Regex" (regular expression) is a pattern language, e.g. `[0-9]+` means digits. REGEXMATCH(text, pattern) returns TRUE/FALSE and uses Google's RE2 syntax (Google Docs Editors Help, "REGEXMATCH", fetched). It accepts only text, so wrap numbers in TEXT.
- REGEXEXTRACT and REGEXREPLACE (extract / replace by pattern): from memory, unverified.
**Example:** Mark rows whose employee ID looks like E followed by 3 digits.
**Formula / Steps:** Sheets: `=ARRAYFORMULA(REGEXMATCH(A2:A5,"^E[0-9]{3}$"))` (**not run here**). By hand on E101, E12, e105, X200 returns TRUE, FALSE, FALSE, FALSE (regex is case-sensitive).
**Alternative:** Excel: `=LEFT(A2,1)="E"` plus LEN/ISNUMBER tests, wildcards in COUNTIF, or Flash Fill (Data > Flash Fill). Microsoft has been adding REGEX functions to Microsoft 365; check your build (from memory, unverified).
**Version note:** Excel 365 dynamic arrays spill without Ctrl+Shift+Enter; Excel 2016/2019 do not.
**Edge cases:** ARRAYFORMULA cannot be exported (Google page); regex differences between tools.
**Likely follow-ups:** *Alternative to ARRAYFORMULA?* Fill-down or QUERY.
**Common mistakes:** Passing numbers to REGEXMATCH; forgetting anchors ^ and $.

### Q70 ⭐ 🟡 How do you use the TEXT function inside a formula to build a label such as "Jan-2026: 45 hires"?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you control number/date format when joining text?
**Say this in the interview:** "When I join a date or number to text, Excel shows the raw serial. TEXT converts it with a format code: =TEXT(A2,"mmm-yyyy")&": "&B2&" hires"."
**Explain simply:**
- `TEXT(value, "format")` returns text formatted the way you ask.
- Dates are numbers underneath (e.g. 46023), so without TEXT you get "46023: 45 hires".
- Codes: mmm = Jan, mmmm = January, yyyy = year, #,##0 = thousands separator, 0.0% = percent.
**Example:** Dashboard titles for a monthly hiring report.
**Sample sheet:**
| | A (Month) | B (Hires) | C (Accept rate) |
|---|---|---|---|
| 2 | 01-Jan-26 | 45 | |
| 3 | 01-Feb-26 | 1234 | |
| 4 | | | 0.275 |

**Formula / Steps:** `=TEXT(A2,"mmm-yyyy")&": "&B2&" hires"`
**Alternative:** `="Offer accept rate: "&TEXT(C4,"0.0%")`; or CONCAT/TEXTJOIN around TEXT.
**Result (run):** row 2: `Jan-2026: 45 hires`; row 3 with `TEXT(B3,"#,##0")`: `Feb-2026: 1,234 hires`; `Offer accept rate: 27.5%`; `TEXT(A2,"dd mmm yyyy")` = 01 Jan 2026; `TEXT(A2,"mmmm")` = January.
**Version note:** All versions and Google Sheets. Format codes depend on the language of Excel (a German Excel uses "JJJJ" for year) (from memory, unverified).
**Edge cases:** The result is text, so you can't sum it. Unknown codes give odd output.
**Likely follow-ups:** *Show a rounded number?* `TEXT(x,"0.00")`.
**Common mistakes:** Forgetting quotes round the format; using lowercase "mm" in time context (minutes vs months).

### Q71 ⭐ 🟡 What are the criteria length and wildcard limits of COUNTIF (255 characters, ~ escape)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Awareness of COUNTIF's hidden limits.
**Say this in the interview:** "COUNTIF can give wrong results when the text it matches is longer than 255 characters. Wildcards are ? for one character and * for any run, and ~ makes them literal."
**Explain simply:**
- Microsoft Support ("Use the COUNTIF function") states COUNTIF can return incorrect results when matching strings longer than 255 characters.
- `?` matches one character, `*` any number of characters; put `~` before them to find a real ? or * (same page).
- To find a real tilde use `~~` (from memory, unverified; run below worked in LibreOffice).
**Example:** Counting job titles with "*" in them, e.g. "Ops*Lead".
**Sample sheet:**
| | A |
|---|---|
| 2 | Ops*Lead |
| 3 | Ops Lead |
| 4 | OpsXLead |
| 5 | What? |
| 6 | What1 |
| 7 | a~b |

**Formula / Steps:** `=COUNTIF(A2:A7,"Ops*Lead")`; literal: `=COUNTIF(A2:A7,"Ops~*Lead")`
**Alternative:** For long text or exact matching: `=SUMPRODUCT(--(A2:A7=C1))`.
**Result (run in LibreOffice):** "Ops*Lead" = 3; "Ops~*Lead" = 1; "What?" = 2; "What~?" = 1; "a~~b" = 1. Long text: LibreOffice has no 255 limit (300-character test returned 1), so **the 255 problem is not reproduced here**; it comes from Microsoft documentation.
**Version note:** Applies to Excel 365, 2024, 2021 per the page; behaviour of older versions unverified.
**Edge cases:** Criteria "=" on blanks; numbers stored as text.
**Likely follow-ups:** *Does SUMIF have the same limit?* Likely, from memory, unverified.
**Common mistakes:** Forgetting ~ when searching for "*"; trusting COUNTIF on very long strings.

### Q72 ⭐ 🔴 What is the known problem with the "MD" unit of DATEDIF, and how do you get remaining days correctly?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you spot a known bug and avoid it for tenure reports?
**Say this in the interview:** "Microsoft warns DATEDIF's MD unit can return negative, zero or wrong results. I get the leftover days as end date minus EDATE(start, full months)."
**Explain simply:**
- DATEDIF(start, end, "Y"/"M"/"D"/"MD"/"YM"/"YD") counts years, months, days; "MD" = days ignoring months and years.
- Microsoft Support ("DATEDIF function") says MD may return a negative number, zero or an inaccurate result and recommends against it.
- Better: months with `"M"`, then days = end minus the date you reach after those months.
**Example:** Tenure "2 years 5 months 2 days" for an exit letter.
**Sample sheet:**
| | A (Start) | B (End) |
|---|---|---|
| 2 | 31-Jan-26 | 01-Mar-26 |
| 3 | 31-Dec-25 | 28-Feb-26 |
| 4 | 15-Jan-26 | 10-Mar-26 |
| 5 | 20-May-24 | 22-Oct-26 |

**Formula / Steps:** Months `=DATEDIF(A2,B2,"M")`; days `=B2-EDATE(A2,DATEDIF(A2,B2,"M"))`
**Alternative:** Microsoft's own workaround: `=B2-DATE(YEAR(B2),MONTH(B2),1)` (days into the end month; not identical to leftover days after full months when the start day is later than the end day).
**Result (run in LibreOffice):** months = 1, 1, 1, 29; "MD" = -2, 28, 23, 2; EDATE method = 1, 28, 23, 2; Microsoft workaround = 0, 27, 9, 21. LibreOffice returned MD = -2 for row 2, an example of the negative result Microsoft describes; Excel's own MD numbers were **not run here** and may differ.
**Version note:** DATEDIF works in Excel 2016 to 365 (page lists them) but is not in the function-wizard list (from memory, unverified); Google Sheets has DATEDIF too (from memory).
**Edge cases:** End date before start gives #NUM!. Month-end starts (31st) are where MD misbehaves.
**Likely follow-ups:** *Exact years only?* `"Y"` works fine.
**Common mistakes:** Trusting "MD"; text dates.

### Q73 ⭐ 🔴 Why can COUNTIF match long numbers such as 16-digit IDs wrongly, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know Excel keeps only 15 digits of precision?
**Say this in the interview:** "Excel treats digit-only criteria as numbers and only keeps 15 digits, so two 16-digit IDs that differ in the last digit look equal. I compare as text with SUMPRODUCT or add a wildcard."
**Explain simply:**
- Excel's precision of numbers is 15 digits (Microsoft Support, "Excel specifications and limits").
- COUNTIF converts a digit-only criterion to a number, so 16-digit text IDs are compared at 15 digits. This mechanism is from memory, unverified.
- IDs (card, Aadhaar-like, employee numbers) should be stored as text.
**Example:** Three IDs ending 6, 7, 8 may all be counted for the ID ending in 7.
**Sample sheet:**
| | A (ID, text) | C |
|---|---|---|
| 2 | 1234567890123456 | Look-up: 1234567890123457 |
| 3 | 1234567890123457 | |
| 4 | 1234567890123458 | |
| 5 | 9876543210987654 | |

**Formula / Steps:** Risky: `=COUNTIF(A2:A5,C2)`. Safe: `=SUMPRODUCT(--(A2:A5=C2))` or `=SUMPRODUCT(--EXACT(A2:A5,C2))` or `=COUNTIF(A2:A5,C2&"*")`.
**Alternative:** Add a helper column with `"ID"&A2` so it is never numeric.
**Result:** In LibreOffice all four formulas returned 1; **the bug is not reproduced here**. In Excel the risky COUNTIF is expected to return 3 (by hand: the three IDs share the same first 15 digits; not run here, from memory). The safe versions return 1 (run).
**Version note:** Excel only; Google Sheets behaviour unverified.
**Edge cases:** A 16-digit number typed as a number is already rounded (last digit becomes 0); import as text.
**Likely follow-ups:** *Why do IDs show 1.23E+15?* Number format General; use Text format first.
**Common mistakes:** Typing long IDs into General-format cells.

### Q74 ⭐ 🔴 How would you build a monthly attrition table using COUNTIFS on joining and exit dates?
**Asked at:** Candidate reports (Glassdoor MIS pages, search snippet) mention attrition tasks; no company-specific attribution.
**What the interviewer is checking:** Can you turn dates into opening headcount, joiners, leavers, closing and attrition %?
**Say this in the interview:** "Opening headcount is people who joined before the month start minus people who left before it. Leavers and joiners are COUNTIFS between the month start and the next month start. Attrition % is leavers divided by average headcount."
**Explain simply:**
- "Attrition" = people leaving. Monthly rate = leavers / average of opening and closing headcount (this convention is from general practice, unverified; some firms divide by opening headcount).
- Blank exit date = still working; COUNTIFS with "<" ignores blanks.
- `EDATE(date,1)` gives the same day next month.
**Example:** 8 employees, months Jan to Mar 2026.
**Sample sheet:**
| | A (Emp) | B (Joined) | C (Exit) |
|---|---|---|---|
| 2 | E1 | 01-Jun-24 | |
| 3 | E2 | 10-Jan-25 | 12-Feb-26 |
| 4 | E3 | 05-Aug-25 | |
| 5 | E4 | 20-Nov-25 | 15-Jan-26 |
| 6 | E5 | 05-Jan-26 | |
| 7 | E6 | 03-Feb-26 | 09-Mar-26 |
| 8 | E7 | 02-Mar-26 | |
| 9 | E8 | 01-Sep-23 | 25-Mar-26 |

**Formula / Steps (month start in F2):**
- G2 Opening: `=COUNTIFS($B$2:$B$9,"<"&F2)-COUNTIFS($C$2:$C$9,"<"&F2)`
- H2 Joined: `=COUNTIFS($B$2:$B$9,">="&F2,$B$2:$B$9,"<"&EDATE(F2,1))`
- I2 Left: `=COUNTIFS($C$2:$C$9,">="&F2,$C$2:$C$9,"<"&EDATE(F2,1))`
- J2 Closing: `=G2+H2-I2`; K2 Attrition: `=I2/AVERAGE(G2,J2)`
**Alternative:** A PivotTable grouped by month (not run here), or SUMPRODUCT.
**Result (run):**
| Month | Opening | Joined | Left | Closing | Attrition |
|---|---|---|---|---|---|
| Jan-26 | 5 | 1 | 1 | 5 | 20.0% |
| Feb-26 | 5 | 1 | 1 | 5 | 20.0% |
| Mar-26 | 5 | 1 | 2 | 4 | 44.4% |

**Version note:** COUNTIFS and EDATE work in 2007+ and Google Sheets.
**Edge cases:** Exit dates typed as text are not counted; same-month join and exit; annualise by multiplying by 12 only for a rough view.
**Likely follow-ups:** *Annual rate?* Leavers in year / average headcount.
**Common mistakes:** Using "<="&month end date with times; counting blanks as exits; dividing by closing headcount only.

