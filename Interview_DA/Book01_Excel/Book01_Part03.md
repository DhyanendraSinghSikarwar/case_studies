# Book 1 — Excel | Part 3: Lookups: VLOOKUP, HLOOKUP, INDEX-MATCH, XLOOKUP 🟢🟡

**Target:** 60 questions | **Actual:** 60 questions
**Scope:** VLOOKUP, HLOOKUP, INDEX-MATCH, XLOOKUP and XMATCH: syntax, match modes, errors, left lookups, multi-criteria and two-way lookups, version differences.

### Q1 ⭐⭐⭐ 🟢 What is VLOOKUP, and what are its four arguments?
**Asked at:** commonly asked (no company-specific report found); named in MIS job descriptions we sampled (Ninjacart MIS, Tata Advanced Systems).
**What the interviewer is checking:** Do you know the most-used Excel lookup and can you say what each part does?
**Say this in the interview:** "VLOOKUP finds a key, like an Employee ID, in the first column of a table and returns a value from another column in the same row. It takes four arguments: what to look for, where to look, which column to return, and exact or approximate match."
**Explain simply:**
- Lookup = Excel finds a value in one table and brings related information from another, like finding a name in a phone book and reading the number next to it.
- `VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])`.
- `lookup_value`: the key you have (ID 102). `table_array`: the table to search; the key must be in its **first** column. `col_index_num`: which column of that table to return, counted from 1. `range_lookup`: FALSE (or 0) = exact match, TRUE = approximate.
- It reads left to right only.
**Example:** HR has Employee ID 102 and wants the name and department from the master list.
**Sample sheet:** Sheet `Master` (A1:E6):

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | EmpID | Name | Dept | City | Salary |
| 2 | 101 | Asha | HR | Hyderabad | 42000 |
| 3 | 102 | Ravi | Finance | Pune | 55000 |
| 4 | 103 | Meena | IT | Bengaluru | 68000 |
| 5 | 104 | Karan | HR | Chennai | 39000 |
| 6 | 105 | Divya | Sales | Mumbai | 47000 |

Sheet `S`: G1 = 102.
**Formula / Steps:** `=VLOOKUP(G1,Master!A2:C6,3,FALSE)`
**Alternative:** `=INDEX(Master!C2:C6,MATCH(G1,Master!A2:A6,0))`, or `=XLOOKUP(G1,Master!A2:A6,Master!C2:C6)` in 365/2021.
**Result:** Run in LibreOffice: column 3 returns `Finance`; `=VLOOKUP(G1,Master!A2:C6,2,FALSE)` returns `Ravi`.
**Version note:** Works in every Excel version and Google Sheets (VLOOKUP is a standard function; from memory, unverified).
**Edge cases:** Key not found returns #N/A. Leaving out the 4th argument defaults to approximate match (Microsoft Support: "VLOOKUP function"). Duplicate keys: the first match wins.
**Likely follow-ups:** 1) *Can it look left?* No, use INDEX-MATCH or XLOOKUP. 2) *What if you skip the 4th argument?* Approximate match, risky.
**Common mistakes:** Forgetting FALSE; counting the column from the sheet instead of from the table's first column; leaving the key column not first in the table.

### Q2 ⭐⭐⭐ 🟢 What is the difference between exact match and approximate match in VLOOKUP, and which one do you use most often?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the risky default and the slab use case?
**Say this in the interview:** "Exact match (FALSE) finds only the identical key, or gives #N/A. Approximate match (TRUE) finds the largest value that is less than or equal to the key, and needs the first column sorted ascending. I use exact about 90% of the time, for IDs; approximate for slabs like grades or tax bands."
**Explain simply:**
- Exact: "find employee 103 exactly".
- Approximate: "find which band a score falls in". The table lists the *lower limit* of each band, sorted smallest to largest.
- If you leave the 4th argument out, Excel uses approximate. On unsorted IDs this silently gives wrong answers.
**Example:** Score 78 should get grade B (70 to 84).
**Sample sheet:**

| | A | B | | D | E |
|---|---|---|---|---|---|
| 1 | Score from | Grade | | | |
| 2 | 0 | D | | 78 | |
| 3 | 50 | C | | 85 | |
| 4 | 70 | B | | 49 | |
| 5 | 85 | A | | | |

**Formula / Steps:** `E2: =VLOOKUP(D2,A2:B5,2,TRUE)`, same for E3 and E4. Exact on the same table: `=VLOOKUP(78,A2:B5,2,FALSE)`.
**Alternative:** `=LOOKUP(D2,A2:A5,B2:B5)` or `=INDEX(B2:B5,MATCH(D2,A2:A5,1))`.
**Result:** Run: 78 returns `B`; 85 returns `A` (also with the 4th argument omitted); 49 returns `D`; exact match for 78 returns `#N/A` because 78 is not literally in the list.
**Version note:** All versions; Google Sheets behaves the same (from memory, unverified).
**Edge cases:** Approximate on an unsorted list gives unpredictable results; a value below the first limit returns #N/A.
**Likely follow-ups:** 1) *Why sorted?* It uses a fast binary search that assumes order. 2) *What does TRUE return for text?* The nearest earlier item alphabetically, rarely useful.
**Common mistakes:** Omitting the 4th argument for IDs; sorting descending; using band upper limits instead of lower limits.

### Q3 ⭐⭐⭐ 🟢 You have an attendance sheet with Employee ID and a master sheet with Employee ID, name and department. Write the formula to bring the department into the attendance sheet.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you write a correct, drag-safe lookup?
**Say this in the interview:** "I put `=VLOOKUP(A2,Master!$A$2:$C$6,3,FALSE)` next to the ID and drag it down. I lock the table with dollar signs so it does not slide."
**Explain simply:**
- `$` = absolute reference: it freezes the table address when the formula is copied.
- 3 is the Department column counted within the table A to C.
- FALSE because IDs must match exactly.
**Example:** Five attendance rows, each ID gets its department.
**Sample sheet:** Sheet `S` (Master as in Q1):

| | A | B |
|---|---|---|
| 1 | EmpID | Dept |
| 2 | 103 | |
| 3 | 101 | |
| 4 | 105 | |
| 5 | 102 | |
| 6 | 104 | |

**Formula / Steps:** `B2: =VLOOKUP(A2,Master!$A$2:$C$6,3,FALSE)`, then double-click the fill handle (small square at the cell corner) to fill down.
**Alternative:** `=INDEX(Master!$C$2:$C$6,MATCH(A2,Master!$A$2:$A$6,0))`; or `=XLOOKUP(A2,Master!$A$2:$A$6,Master!$C$2:$C$6)` in 365/2021 (not run here).
**Result:** Run: IT, HR, Sales, Finance, HR.
**Version note:** VLOOKUP and INDEX-MATCH work everywhere; XLOOKUP needs 2021/365.
**Edge cases:** New joiners missing in Master give #N/A (see Q6). Use whole-column refs (`Master!$A:$C`) if the master grows.
**Likely follow-ups:** 1) *Master grows?* Use an Excel Table or full columns. 2) *Two departments for one ID?* First match only.
**Common mistakes:** No `$`; table starting at the header but key not in first column; forgetting FALSE.

### Q4 ⭐⭐⭐ 🟢 What are the limitations of VLOOKUP?
**Asked at:** commonly asked (no company-specific report found); appears in the MIS-executive question lists we found.
**What the interviewer is checking:** Do you know why people move to INDEX-MATCH and XLOOKUP?
**Say this in the interview:** "It only looks right of the key column, returns only the first match, breaks when columns are inserted because the column number is hard-coded, defaults to approximate match, and is slow on huge data."
**Explain simply:**
- Key must be the first column of the table; no looking left.
- `col_index_num` is a typed number; insert a column and it points to the wrong one (Q12).
- Returns only the first match; duplicates ignored.
- Default approximate match can give wrong answers silently.
- Text and number mismatch, or stray spaces, give #N/A (Q14).
- Not case-sensitive; one return column per formula.
**Example:** A payroll table with Salary left of Employee ID cannot be searched by ID with VLOOKUP.
**Sample sheet:** Sheet `S`: A1:C4 = Salary, EmpID, Name; rows 2 to 4 = (42000, 101, Asha), (55000, 102, Ravi), (68000, 103, Meena). E1 = 102.
**Formula / Steps:** Fixes: `=INDEX(return_col,MATCH(key,key_col,0))` or `=XLOOKUP(key,key_col,return_col)`.
**Alternative:** Convert the range to an Excel Table (Insert > Table) so references adjust automatically.
**Result:** Run: `=VLOOKUP(E1,A1:C4,1,FALSE)` returns `#N/A` (it searches column A, which holds salaries); `=INDEX(A2:A4,MATCH(E1,B2:B4,0))` returns `55000`.
**Version note:** XLOOKUP not in Excel 2016/2019 (Microsoft Support, "XLOOKUP function": "XLOOKUP is not available in Excel 2016 and Excel 2019").
**Edge cases:** Whole-column lookups on 500k rows can be slow.
**Likely follow-ups:** 1) *Which one would you pick today?* XLOOKUP if everyone has 2021/365, else INDEX-MATCH. 2) *Is VLOOKUP dead?* No, still everywhere in legacy files.
**Common mistakes:** Saying "it is slow" without context; forgetting the approximate default.

### Q5 ⭐⭐⭐ 🟢 Why does VLOOKUP return #N/A, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you troubleshoot a lookup systematically?
**Say this in the interview:** "#N/A means 'not available', so the key was not found. Usually the ID truly is missing, or it has a hidden space, or one side is text and the other a number. I check with LEN and ISNUMBER, then clean with TRIM and VALUE."
**Explain simply:**
- Causes: key genuinely absent; typo; trailing/leading spaces; text-number mismatch; exact match used on wrong column; approximate match on unsorted data.
- Check: `=LEN(A5)` (a 3-digit ID showing 4 means a hidden space); `=ISNUMBER(A5)`.
- Fix: `TRIM` removes extra spaces; `VALUE` turns text into a number.
**Example:** HR exports IDs from one system with a trailing space.
**Sample sheet:** Sheet `S`, Master as in Q1:

| | A | B | C |
|---|---|---|---|
| 2 | 101 | | |
| 3 | 999 | | |
| 4 | '102 (text) | | |
| 5 | '103 + trailing space | | |
| 6 | 105 | | |

**Formula / Steps:** `B2: =VLOOKUP(A2,Master!$A$2:$C$6,3,FALSE)`; fixed version `=VLOOKUP(VALUE(TRIM(A5)),Master!$A$2:$C$6,3,FALSE)`.
**Alternative:** Clean once with Data > Text to Columns (Finish), or Find & Replace spaces.
**Result:** Run: B2 `HR`, B3 `#N/A` (999 truly absent), B5 `#N/A` (space), B6 `Sales`; the fixed formula on A5 returns `IT`. Caution: LibreOffice returned `Finance` for the text "102" in A4 because it silently converts text to numbers; Excel returns #N/A there (from Microsoft documentation / memory: Excel treats text "102" and number 102 as different).
**Version note:** All versions.
**Edge cases:** Non-breaking spaces (CHAR(160), from web copy) are not removed by TRIM (see Q14).
**Likely follow-ups:** 1) *How to tell missing vs mismatch?* Test with COUNTIF or LEN. 2) *Can you hide it?* Q6.
**Common mistakes:** Hiding the error without finding the cause; fixing only one side of the mismatch.

### Q6 ⭐⭐⭐ 🟢 How do you hide or replace the #N/A error that VLOOKUP returns, for example with "Not found"?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know IFERROR / IFNA and their risk?
**Say this in the interview:** "I wrap it: `=IFNA(VLOOKUP(...),"Not found")`. IFNA only catches #N/A, so real errors like a wrong column still show up. IFERROR catches everything, which can hide bugs."
**Explain simply:**
- IFERROR(value, if_error) shows your text when the formula gives any error.
- IFNA does the same only for #N/A.
- "Not found" is more useful to a reader than a blank.
**Example:** A new joiner, ID 999, is not in the master list yet.
**Sample sheet:** `A2 = 103`, `A3 = 999` (Master as Q1).
**Formula / Steps:** `=IFERROR(VLOOKUP(A3,Master!$A$2:$C$6,3,FALSE),"Not found")`
**Alternative:** `=IFNA(VLOOKUP(A3,Master!$A$2:$C$6,3,FALSE),"Not found")`
**Result:** Run: A2 gives `IT`, A3 gives `Not found` with either function.
**Version note:** IFERROR is Excel 2007+. IFNA applies to Excel 2016 and later per Microsoft Support, "IFNA function" (page does not list Excel 2013; I believe it arrived in 2013, from memory, unverified). Both exist in Google Sheets (from memory, unverified).
**Edge cases:** Note: in LibreOffice the formula needs the `_xlfn.` prefix when written by script; in normal Excel typing you do not.
**Likely follow-ups:** 1) *Which is safer?* IFNA (Q20). 2) *Return blank?* Use "" instead of text.
**Common mistakes:** Wrapping everything in IFERROR from the start, so a broken column number goes unnoticed.

### Q7 ⭐⭐⭐ 🟢 What is XLOOKUP, and how is it different from VLOOKUP?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the modern replacement and why it is better?
**Say this in the interview:** "XLOOKUP is the newer lookup: `XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])`. Exact match is the default, it can look left, has a built-in not-found message, and returns by column range so inserting columns does not break it."
**Explain simply:**
- You pick the column to search and the column to return separately, so no column counting.
- Default is exact match (safe); VLOOKUP defaults to approximate.
- Can search bottom-to-top (last match) and return several columns at once.
- Needs Excel 2021 or 365.
**Example:** Find Ravi's city from a master sheet.
**Sample sheet:** Master as in Q1; G1 = 102.
**Formula / Steps:** `=XLOOKUP(G1,Master!A2:A6,Master!D2:D6,"Not found")`
**Alternative:** `=INDEX(Master!D2:D6,MATCH(G1,Master!A2:A6,0))` for older Excel.
**Result:** not run here (LibreOffice 24.2 has no XLOOKUP). By hand: 102 is in row 3 of the range, so the city is `Pune`. The INDEX-MATCH alternative returns the same.
**Version note:** Microsoft Support, "XLOOKUP function" says "XLOOKUP is not available in Excel 2016 and Excel 2019", though its "Applies to" list also names those versions (conflict inside the page); I treat it as 2021/2024/365 only. Google Sheets has XLOOKUP (from memory, unverified).
**Edge cases:** A workbook with XLOOKUP opened in 2016/2019 shows #NAME? on recalculation.
**Likely follow-ups:** 1) *Argument 4?* if_not_found (Q23). 2) *Is it faster?* Often similar; not guaranteed.
**Common mistakes:** Using a different-sized lookup and return range; sharing files with 2016 users.

### Q8 ⭐⭐⭐ 🟢 What is INDEX-MATCH, and why would you use it instead of VLOOKUP?
**Asked at:** Named in a sampled MIS job description (Vee Technologies, Bengaluru); otherwise commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the classic fix for VLOOKUP's limits?
**Say this in the interview:** "MATCH finds the row position of the key; INDEX returns the value at that position from the column I choose. Together they can look left and do not break when columns are inserted."
**Explain simply:**
- `MATCH(key, key_column, 0)` gives a position number (the 4th ID is position 4).
- `INDEX(return_column, position)` gives the value at that position.
- Because you point at the return column directly, no hard-coded column number.
**Example:** Department of employee 104.
**Sample sheet:** Master as in Q1; A2 = 104.
**Formula / Steps:** `=INDEX(Master!$C$2:$C$6,MATCH(A2,Master!$A$2:$A$6,0))`
**Alternative:** `=VLOOKUP(A2,Master!$A$2:$C$6,3,FALSE)` or XLOOKUP (365/2021).
**Result:** Run: `MATCH` returns `4`; the full formula returns `HR`.
**Version note:** Works in all Excel versions and Google Sheets (from memory, unverified).
**Edge cases:** Always put 0 in MATCH (Q38). Duplicates: first match.
**Likely follow-ups:** 1) *Two-way?* Q30. 2) *Drawback?* Longer to type.
**Common mistakes:** Mismatched row ranges (INDEX range starts at row 2, MATCH at row 1); forgetting 0.

### Q9 ⭐⭐⭐ 🟢 What does the INDEX function do, and what are its arguments?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand INDEX alone, not just inside INDEX-MATCH?
**Say this in the interview:** "INDEX returns the value at a given row and column inside a range: `INDEX(array, row_num, [column_num])`. Think of it as giving seat coordinates."
**Explain simply:**
- `array`: the block of cells; `row_num`: which row inside it; `column_num`: which column inside it.
- With one column, you can give just the row number.
- Row or column 0 means "the whole row/column"; useful inside SUM.
**Example:** The third employee's name; total salary.
**Sample sheet:** Master as in Q1.
**Formula / Steps:** `=INDEX(Master!A2:E6,3,2)`; `=INDEX(Master!C2:C6,4)`; `=SUM(INDEX(Master!A2:E6,0,5))`
**Alternative:** Direct reference `=Master!B4`, which breaks if rows are sorted; INDEX with MATCH is dynamic.
**Result:** Run: `Meena`; `HR`; `251000`.
**Version note:** All versions and Google Sheets.
**Edge cases:** Row number larger than the range gives #REF!.
**Likely follow-ups:** 1) *INDEX vs OFFSET?* INDEX is non-volatile (recalculates only when needed), better. 2) *Where does the number come from?* MATCH.
**Common mistakes:** Counting rows from the sheet instead of from the array's first row.

### Q10 ⭐⭐⭐ 🟢 What does the MATCH function do, and what do the match types 0, 1 and -1 mean?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the three modes and when each applies?
**Say this in the interview:** "MATCH returns the position of a value in a list. 0 is exact match, 1 finds the largest value less than or equal (list ascending), -1 finds the smallest value greater than or equal (list descending)."
**Explain simply:**
- `MATCH(lookup_value, lookup_array, [match_type])`.
- 0: exact, any order. 1: ascending list, "nearest below". -1: descending list, "nearest above".
- Returns a position, not the value.
**Example:** Position of ID 103; where 104.5 lands.
**Sample sheet:** Master IDs in A2:A6 (101 to 105); descending list in C1:C4 = 90, 70, 50, 30.
**Formula / Steps:** `=MATCH(103,Master!A2:A6,0)`; `=MATCH(104.5,Master!A2:A6,1)`; `=MATCH(60,C1:C4,-1)`
**Alternative:** XMATCH in 365/2021 (Q40), not run here.
**Result:** Run: `3`; `4` (104 is the largest not above 104.5); `2` (70 is the smallest value not below 60). `=MATCH(104.5,Master!A2:A6,-1)` on an ascending list returns `#N/A`.
**Version note:** All versions; Google Sheets same.
**Edge cases:** Wrong sort order for 1/-1 gives wrong or #N/A results.
**Likely follow-ups:** 1) *Omitted type?* Defaults to 1 (Q38). 2) *Wildcards?* Work with 0 on text.
**Common mistakes:** Using 1 with unsorted data; mixing up 1 and -1.

### Q11 ⭐⭐⭐ 🟢 Which Excel versions have XLOOKUP, and what do you do if a colleague uses Excel 2016 or 2019?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Real-world awareness that office files get shared across versions.
**Say this in the interview:** "XLOOKUP is in Microsoft 365 and Excel 2021 and later. 2016 and 2019 do not have it, so for shared files I use INDEX-MATCH, which works everywhere."
**Explain simply:**
- Microsoft Support, "XLOOKUP function": "XLOOKUP is not available in Excel 2016 and Excel 2019." Its "Applies to" list names 365, 2024, 2021, 2019 and 2016, which contradicts that note; the note is the reliable statement. It also says you may still see XLOOKUP in workbooks made in newer versions.
- Options for 2016/2019 colleagues: INDEX-MATCH; VLOOKUP; or send values only (Copy > Paste Special > Values) so no formula needs to run.
- Excel for the web: not confirmed on the page I read.
**Example:** Your HR dashboard goes to a regional manager on Excel 2016.
**Formula / Steps:** Replace `=XLOOKUP(A2,Master!A:A,Master!C:C)` with `=INDEX(Master!C:C,MATCH(A2,Master!A:A,0))`.
**Alternative:** Paste as values; or share a PDF.
**Result:** Not applicable to a version question. The INDEX-MATCH replacement was run on the Q1 Master sheet with `103` in A2: it returns `IT`, the same as `VLOOKUP(A2,Master!A:C,3,FALSE)`; the XLOOKUP original is not run here.
**Version note:** Google Sheets supports XLOOKUP (Google Docs Editors Help, "XLOOKUP function", fetched).
**Edge cases:** In an old version, XLOOKUP cells show #NAME? after recalculation; cached values may display until then.
**Likely follow-ups:** 1) *Find out the version?* File > Account > About Excel. 2) *Which do you default to?* INDEX-MATCH in mixed teams.
**Common mistakes:** Sending an XLOOKUP workbook without checking recipients.

### Q12 ⭐⭐⭐ 🟡 Your VLOOKUP gave correct values yesterday, but after someone inserted a column in the lookup table it returns wrong values. Why, and how do you prevent it?
**Asked at:** commonly asked (no company-specific report found); this scenario is the standard reason cited for moving to INDEX-MATCH.
**What the interviewer is checking:** Do you understand the hard-coded column number?
**Say this in the interview:** "The column number is typed in. If someone inserts a column before it, the number now points at a different column. I prevent it by finding the column with MATCH on the header, or by using INDEX-MATCH or XLOOKUP."
**Explain simply:**
- Excel adjusts cell references when columns are inserted, but not a plain number like 3.
- Fix: `MATCH("Dept",header_row,0)` as the column number.
- Or reference the return column directly.
**Example:** Someone adds a Phone column before Dept.
**Sample sheet:** Before: A EmpID, B Name, C Dept (rows: 101 Asha HR; 102 Ravi Finance). After: A EmpID, B Name, C Phone, D Dept (Phone: 9700011111 for Asha, 9700022222 for Ravi). F1 = 102.
**Formula / Steps:** Fragile: `=VLOOKUP(F1,A1:D3,3,FALSE)`. Robust: `=VLOOKUP(F1,A1:D3,MATCH("Dept",A1:D1,0),FALSE)`.
**Alternative:** `=INDEX(A1:D3,MATCH(F1,A1:A3,0),MATCH("Dept",A1:D1,0))`; or XLOOKUP (not run here).
**Result:** Run: before the insert, fragile returns `Finance`. After the insert, fragile returns `9700022222` (the phone, wrong), while both robust versions still return `Finance`.
**Version note:** All versions for MATCH-based fixes.
**Edge cases:** Renaming the header breaks MATCH; use an Excel Table so headers stay consistent.
**Likely follow-ups:** 1) *Does INDEX-MATCH always survive?* Yes if ranges adjust. 2) *Silent or loud?* Silent, which is the danger.
**Common mistakes:** Not noticing because no error appears.

### Q13 ⭐⭐⭐ 🟡 You write a VLOOKUP in the first row and drag it down, but many rows return #N/A even though the IDs exist. What is the most likely cause?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know reference anchoring?
**Say this in the interview:** "The table range was not locked with dollar signs, so as I dragged down it slid down too and the lower IDs fell outside the range. I fix it with absolute references: `$A$2:$C$6`, or press F4."
**Explain simply:**
- Relative reference: moves when copied (`A2:C6` becomes `A3:C7`, then `A4:C8`).
- Absolute reference: fixed (`$A$2:$C$6`).
- F4 cycles through the `$` combinations while the cursor is on the reference.
**Example:** Row 6 searches Master!A6:C10, which no longer includes ID 101 to 104.
**Sample sheet:** Master as in Q1; IDs in S!A2:A6 = 101..105.
**Formula / Steps:** Wrong: `B2: =VLOOKUP(A2,Master!A2:C6,3,FALSE)` copied down. Right: `=VLOOKUP(A2,Master!$A$2:$C$6,3,FALSE)`.
**Alternative:** Convert Master to an Excel Table and use `Master[#All]` style references, or name the range.
**Result:** Run, two cases. (1) IDs in master order 101 to 105 with the unlocked range copied down: B2:B6 = HR, Finance, IT, HR, Sales, all correct, because each key sits at the top of its own sliding window. So the slide does not always show up. (2) IDs in a different order, like Q3's 103, 101, 105, 102, 104, with `Master!A2:C6` sliding to `A3:C7`, `A4:C8`, and so on: B2:B6 = `IT`, `#N/A`, `Sales`, `#N/A`, `#N/A`. Takeaway: always lock the range, even when it happens to work.
**Version note:** All versions.
**Edge cases:** The other likely cause is text-versus-number mismatch (Q14).
**Likely follow-ups:** 1) *Other causes?* Spaces, text IDs. 2) *Range name?* Named ranges avoid the issue.
**Common mistakes:** Locking only the first cell (`$A2:C6`).

### Q14 ⭐⭐⭐ 🟡 Two employee IDs look identical, but VLOOKUP says #N/A. What could be wrong with the data, and how do you check and fix it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Data-cleaning instincts, very relevant for HR exports.
**Say this in the interview:** "Usually hidden characters: a trailing space, a non-breaking space from a web or HRMS export, or one ID stored as text and the other as a number. I check with LEN and ISNUMBER and clean with TRIM, SUBSTITUTE and VALUE."
**Explain simply:**
- `LEN(A2)`: counts characters; a 3-digit ID returning 4 has a hidden character.
- `ISNUMBER(A2)`: TRUE for real numbers, FALSE for text numbers (usually left-aligned, with a green triangle).
- `TRIM` removes ordinary extra spaces; `SUBSTITUTE(A2,CHAR(160)," ")` converts non-breaking spaces; `VALUE` turns text to number.
**Example:** IDs pasted from an HRMS export.
**Sample sheet:** Sheet `S` (Master as Q1):

| | A | B (LEN) | C (VLOOKUP) | D (ISNUMBER) |
|---|---|---|---|---|
| 2 | '101 + space | | | |
| 3 | '102 (text) | | | |
| 4 | '103 + CHAR(160) | | | |
| 5 | 105 (number) | | | |
| 6 | '104 (text) | | | |

**Formula / Steps:** `=LEN(A2)`, `=ISNUMBER(A2)`, fix: `=VLOOKUP(VALUE(TRIM(SUBSTITUTE(A2,CHAR(160)," "))),Master!$A$2:$C$6,3,FALSE)`
**Alternative:** Select the column > Data > Text to Columns > Finish (converts text numbers); or multiply by 1 (`=A2*1`).
**Result:** Run: LEN gives 4, 3, 4, 3, 3; the fixed formula returns HR, Finance, IT, Sales, HR. Raw VLOOKUP gave `#N/A` for the two rows with hidden characters. LibreOffice also matched plain text IDs (rows 3 and 6) without cleaning because it coerces text to numbers; Excel does not (from Microsoft documentation / memory), so there it would also return #N/A for those rows.
**Version note:** All versions.
**Edge cases:** Leading zeros in IDs (like 00123) stored as text: convert both sides to text instead.
**Likely follow-ups:** 1) *Why does TRIM miss some spaces?* It handles only code 32. 2) *Clean whole column?* Helper column then Paste Special > Values.
**Common mistakes:** Cleaning one table but not the other.

### Q15 ⭐⭐⭐ 🟡 How do you look up a value that sits to the left of the key column?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you work around VLOOKUP's biggest limit?
**Say this in the interview:** "I use INDEX-MATCH: MATCH searches the key column, INDEX returns from any column, left or right. With XLOOKUP it is even simpler."
**Explain simply:**
- VLOOKUP only returns columns to the right of the key.
- INDEX and MATCH take separate ranges, so direction does not matter.
**Example:** Find the Employee ID (column A) when you only know the name (column B, to the right).
**Sample sheet:** Master as in Q1; A1 = Divya in sheet S.
**Formula / Steps:** `=INDEX(Master!$A$2:$A$6,MATCH(A1,Master!$B$2:$B$6,0))`
**Alternative:** `=XLOOKUP(A1,Master!B2:B6,Master!A2:A6)` (365/2021, not run here); or `=VLOOKUP(A1,CHOOSE({1,2},Master!$B$2:$B$6,Master!$A$2:$A$6),2,FALSE)`, an old trick that builds a virtual table with columns swapped.
**Result:** Run: INDEX-MATCH returns `105`; the CHOOSE trick returns `105`. XLOOKUP expected `105` by hand (not run here).
**Version note:** INDEX-MATCH all versions; XLOOKUP 2021/365.
**Edge cases:** Duplicate names return the first ID; use ID as the key where possible.
**Likely follow-ups:** 1) *Why not rearrange columns?* Often the source is not yours. 2) *Names not unique?* Use two criteria (Q31).
**Common mistakes:** Using VLOOKUP with a name in the wrong column and getting an unrelated value.

### Q16 ⭐⭐⭐ 🟡 How do you pull data with VLOOKUP from a different sheet or a different workbook?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you use sheet and external references?
**Say this in the interview:** "I click the other sheet while building the table_array, which adds `Sheet name!`; for another workbook, I open it and select the range so Excel writes the file name in square brackets."
**Explain simply:**
- Same workbook: `Master!$A$2:$C$6` (add quotes if the sheet name has spaces: `'Staff Master'!$A$2:$C$6`).
- Other workbook: `[Employees.xlsx]Master!$A$2:$C$6`, with a full path in quotes when the source is closed.
- External links break if the file is moved or renamed (Data > Edit Links).
**Example:** Attendance in one file, master data in another.
**Sample sheet:** Master as in Q1 on sheet `Master`.
**Formula / Steps:** Same workbook: `=VLOOKUP(A2,Master!$A$2:$C$6,3,FALSE)`. Other workbook: `=VLOOKUP(A2,[Employees.xlsx]Master!$A$2:$C$6,3,FALSE)`.
**Alternative:** Power Query merge (Data > Get Data > Combine Queries > Merge), or copy the master in as a sheet.
**Result:** Same-sheet-workbook formula run: returns the department (see Q3: IT, HR, Sales, Finance, HR). The external-workbook form was not run here.
**Version note:** All versions; in Google Sheets use `IMPORTRANGE` for another file (from memory, unverified).
**Edge cases:** Closed source files show a long path; moved files cause #REF! or an update prompt.
**Likely follow-ups:** 1) *Risks of external links?* Broken links, security prompts. 2) *Better option?* Power Query.
**Common mistakes:** Forgetting quotes around sheet names with spaces.

### Q17 ⭐⭐ 🟢 What is HLOOKUP, and when do you use it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the horizontal twin of VLOOKUP?
**Say this in the interview:** "HLOOKUP searches across the top row of a table and returns a value from a row below. I use it when headers run across, such as months in columns."
**Explain simply:**
- `HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup])`.
- The H stands for horizontal: the key must be in the first row.
**Example:** Hires and exits by month.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Month | Jan | Feb | Mar |
| 2 | Hires | 12 | 9 | 15 |
| 3 | Exits | 4 | 6 | 3 |

F1 = Feb.
**Formula / Steps:** `=HLOOKUP(F1,A1:D3,2,FALSE)` and `=HLOOKUP(F1,A1:D3,3,FALSE)`
**Alternative:** `=INDEX(B2:D2,MATCH(F1,B1:D1,0))`; `=XLOOKUP(F1,B1:D1,B2:D2)` (365/2021, not run here).
**Result:** Run: `9` hires and `6` exits.
**Version note:** All versions; Google Sheets same.
**Edge cases:** Same approximate-default risk as VLOOKUP.
**Likely follow-ups:** 1) *Looking up above?* Not possible. 2) *Replacement?* XLOOKUP works in both directions.
**Common mistakes:** Mixing row and column numbers; leaving out FALSE.

### Q18 ⭐⭐ 🟢 What is the difference between VLOOKUP and HLOOKUP?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic understanding of orientation.
**Say this in the interview:** "VLOOKUP searches down the first column and returns from a column to the right; HLOOKUP searches across the first row and returns from a row below. Same logic, different direction."
**Explain simply:**
- V = vertical (data in columns, one record per row); H = horizontal (data in rows).
- VLOOKUP takes a column number; HLOOKUP takes a row number.
- Most real data is vertical, so VLOOKUP is far more common.
**Example:** Same hires/exits data, once laid out horizontally (Q17) and once vertically.
**Sample sheet (vertical layout):**

| | A | B | C |
|---|---|---|---|
| 1 | Month | Hires | Exits |
| 2 | Jan | 12 | 4 |
| 3 | Feb | 9 | 6 |
| 4 | Mar | 15 | 3 |

F1 = Feb.
**Formula / Steps:** Vertical: `=VLOOKUP(F1,A1:C4,3,FALSE)`. Horizontal (Q17 layout): `=HLOOKUP(F1,A1:D3,3,FALSE)`.
**Alternative:** `TRANSPOSE` the data (or Paste Special > Transpose) to switch orientation; or use INDEX-MATCH, which works either way.
**Result:** Run: both return `6` (Feb exits).
**Version note:** All versions.
**Edge cases:** None beyond VLOOKUP's.
**Likely follow-ups:** 1) *Which do you use?* VLOOKUP, or XLOOKUP for both. 2) *Convert one to other?* Transpose.
**Common mistakes:** Using VLOOKUP on horizontal data.

### Q19 ⭐⭐ 🟢 What is col_index_num in VLOOKUP, and what happens if it is larger than the number of columns in the table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand the column counting and the resulting error?
**Say this in the interview:** "col_index_num is the position of the column to return, counted from the first column of the table_array, not from column A of the sheet. If it exceeds the table width, Excel returns #REF!; zero or less gives #VALUE!."
**Explain simply:**
- 1 = the key column itself; 2 = next column; and so on.
- Table A2:C6 has 3 columns, so 4 is out of range.
- Microsoft Support ("VLOOKUP function", fetched): "If col_index_num is greater than the number of columns in table-array, you'll get the #REF! error value." The same page's #VALUE! line is worded as "If the table_array is less than 1", which looks like a typo for col_index_num.
**Example:** Asking for column 4 in a three-column table.
**Sample sheet:** Master as in Q1.
**Formula / Steps:** `=VLOOKUP(103,Master!A2:C6,3,FALSE)`; too big: `=VLOOKUP(103,Master!A2:C6,4,FALSE)`; safe: `=VLOOKUP(103,Master!A2:E6,COLUMNS(Master!A2:E6),FALSE)` returns the last column.
**Alternative:** `MATCH` on the header name (Q29).
**Result:** Run: `IT` for column 3. Column 4 returned `#VALUE!` and column 0 returned `#VALUE!` in LibreOffice; Excel returns `#REF!` for column 4 (Microsoft Support, "VLOOKUP function"; not run here). Last column via COLUMNS returned `68000`.
**Version note:** All versions.
**Edge cases:** IFERROR would hide this bug, so test the formula before wrapping it.
**Likely follow-ups:** 1) *Make it dynamic?* Q29. 2) *Decimal like 2.7?* LibreOffice used column 2 (run); Excel is believed to truncate the same way (the Microsoft page does not cover it; from memory, unverified).
**Common mistakes:** Counting from sheet column A; table starting at column C but counting from the sheet.

### Q20 ⭐⭐ 🟢 What is the difference between IFERROR and IFNA, and which one is safer around a lookup?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that hiding all errors hides real bugs?
**Say this in the interview:** "IFERROR replaces every error type; IFNA only replaces #N/A, which is what a failed lookup produces. IFNA is safer because a wrong column number or broken reference will still show up."
**Explain simply:**
- Error types: #N/A (not found), #REF! (bad reference), #VALUE! (wrong type), #DIV/0!, #NAME?.
- A missing employee is a legitimate #N/A; a typo in the formula is a bug you want to see.
**Example:** Missing ID 999 versus the wrong column number 4.
**Sample sheet:** Master as in Q1 (3-column table A2:C6).
**Formula / Steps:** `=IFERROR(VLOOKUP(999,Master!A2:C6,3,FALSE),"Not found")`; `=IFNA(VLOOKUP(999,Master!A2:C6,3,FALSE),"Not found")`; bug case: `=IFNA(VLOOKUP(103,Master!A2:C6,4,FALSE),"Not found")`.
**Alternative:** `=IF(COUNTIF(Master!A2:A6,999)=0,"Not found",VLOOKUP(...))` tests existence first.
**Result:** Run: both functions return `Not found` for ID 999. For the bad column, IFERROR returned `Not found` (bug hidden) while IFNA let the error through (`#VALUE!` in LibreOffice; `#REF!` in Excel, from documentation).
**Version note:** IFERROR: Excel 2007+. IFNA: Microsoft Support, "IFNA function" lists Excel 2016, 2019, 2021, 2024 and 365 (Excel 2013 not listed on that page). Google Sheets has both (from memory, unverified).
**Edge cases:** IFNA does not catch #REF! or #VALUE!.
**Likely follow-ups:** 1) *Return blank?* Use "". 2) *Show the error for debugging?* Remove the wrapper.
**Common mistakes:** Wrapping with IFERROR "to make it clean" and shipping wrong numbers.

### Q21 ⭐⭐ 🟢 What happens when the lookup column has duplicate values? Which row does VLOOKUP return?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know VLOOKUP stops at the first match and silently ignores the rest?
**Say this in the interview:** "VLOOKUP returns the first matching row from the top and never warns me about the others. So if an Employee ID appears three times, I get only the first row's value. I check for duplicates with COUNTIF first, and if I need the latest row I use a different formula."
**Explain simply:**
- Duplicate = the same key appears more than once, for example one Employee ID with a row per month.
- VLOOKUP, INDEX-MATCH and XLOOKUP all read top to bottom and stop at the first hit (default settings).
- No error appears, so the wrong number looks perfectly normal. That is the danger.
- Microsoft's VLOOKUP page does not state which duplicate wins; the first-match behaviour is from my own testing and memory.
**Example:** Employee 102 has sales in Jan, Feb and Mar. You want the latest month but VLOOKUP gives January.
**Sample sheet:** F1 = 102

| | A | B | C |
|---|---|---|---|
| 1 | EmpID | Month | Sales |
| 2 | 101 | Jan | 500 |
| 3 | 102 | Jan | 700 |
| 4 | 103 | Jan | 300 |
| 5 | 102 | Feb | 900 |
| 6 | 102 | Mar | 650 |

**Formula / Steps:** `=VLOOKUP(F1,A2:C6,3,FALSE)` and the duplicate check `=COUNTIF(A2:A6,F1)`
**Alternative:** Last match: `=LOOKUP(2,1/(A2:A6=F1),C2:C6)` (works in all versions). In 365/2021: `=XLOOKUP(F1,A2:A6,C2:C6,,0,-1)` (not run here). Or sum all of them with `=SUMIFS(C2:C6,A2:A6,F1)`.
**Result:** Run in LibreOffice: VLOOKUP returns `700` (the January row), COUNTIF returns `3`, the LOOKUP trick returns `650` (the March row). The XLOOKUP version is not run here; by hand it also gives 650.
**Version note:** VLOOKUP and LOOKUP work in all versions and Google Sheets (from memory, unverified); the XLOOKUP form needs 365/2021.
**Edge cases:** If duplicates are mistakes (same employee listed twice in the master), fix the data (Data > Remove Duplicates). If they are legitimate (one row per month), use SUMIFS, a helper key or the last-match formula.
**Likely follow-ups:** 1) *How do you get the latest entry?* Reverse search with XLOOKUP, or the LOOKUP(2,1/...) trick. 2) *How do you spot duplicates?* COUNTIF greater than 1, or conditional formatting > Duplicate Values.
**Common mistakes:** Trusting a lookup on a key that is not unique; not noticing because no error is shown.

### Q22 ⭐⭐ 🟢 Is VLOOKUP case-sensitive?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the lookup treats "abc" and "ABC" as the same and how to force an exact-case match?
**Say this in the interview:** "No, VLOOKUP ignores upper and lower case, so 'ABC' and 'abc' match the first of the two it meets. If case matters, for example case-sensitive asset codes, I combine INDEX, MATCH and EXACT, because EXACT compares text letter by letter including case."
**Explain simply:**
- Case-sensitive = treats capital and small letters as different. VLOOKUP does not.
- Microsoft's MATCH page says "MATCH does not distinguish between uppercase and lowercase" (Microsoft Support, "MATCH function"). The VLOOKUP page is silent; for VLOOKUP I rely on my test and memory.
- `EXACT(a,b)` returns TRUE only if both texts are identical including case.
**Example:** Two asset codes `abc` (laptop) and `ABC` (monitor) exist; the user types `ABC`.
**Sample sheet:** D1 = ABC

| | A | B |
|---|---|---|
| 1 | Code | Item |
| 2 | abc | lower |
| 3 | ABC | upper |
| 4 | Abd | other |

**Formula / Steps:** Case-insensitive: `=VLOOKUP(D1,A2:B4,2,FALSE)`. Case-sensitive: `=INDEX(B2:B4,MATCH(TRUE,INDEX(EXACT(A2:A4,D1),0),0))`
**Alternative:** Count exact-case hits first with `=SUMPRODUCT(--EXACT(A2:A4,D1))`.
**Result:** Run: VLOOKUP returns `lower` (the first of the two); the EXACT version returns `upper`; the SUMPRODUCT count is `1`.
**Version note:** All Excel versions and Google Sheets (from memory, unverified). The `INDEX(...,0)` wrapper avoids Ctrl+Shift+Enter in older Excel (from memory; I only ran it in LibreOffice).
**Edge cases:** Trailing spaces are a bigger real-life problem than case; use TRIM. If no exact-case match exists, MATCH returns #N/A.
**Likely follow-ups:** 1) *Is XLOOKUP case-sensitive?* Microsoft's page does not say; in my understanding it is not (unverified). 2) *Is SUMIF case-sensitive?* No.
**Common mistakes:** Assuming "ABC" will not match "abc"; forgetting the `,0` inside INDEX so the formula needs array entry in old versions.

### Q23 ⭐⭐ 🟢 What is the if_not_found argument in XLOOKUP?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know XLOOKUP has a built-in "not found" message so IFERROR is not needed?
**Say this in the interview:** "It is the fourth argument. If XLOOKUP finds nothing, it shows the text I give instead of #N/A. So `=XLOOKUP(A2,Master!A:A,Master!D:D,"Not found")` shows 'Not found' for an unknown ID. If I leave it out, I get #N/A."
**Explain simply:**
- Full syntax: `XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])`.
- Microsoft Support ("XLOOKUP function"): "If a valid match is not found, and [if_not_found] is missing, #N/A is returned."
- It handles only "not found". Other errors in the data still show, which is safer than IFERROR hiding everything.
**Example:** HR pastes 2 IDs, one valid (102) and one typo (999).
**Sample sheet:** Master (A1:D6, EmpID, Name, Dept, City; 102 = Ravi, Finance, Pune)

| | A | B |
|---|---|---|
| 1 | Request | City |
| 2 | 102 | |
| 3 | 999 | |

**Formula / Steps:** `B2: =XLOOKUP(A2,Master!A2:A6,Master!D2:D6,"Not found")`, copy to B3.
**Alternative:** Older Excel: `=IFNA(VLOOKUP(A2,Master!A2:D6,4,FALSE),"Not found")`.
**Result:** XLOOKUP is **not run here** (LibreOffice 24.2 lacks it); expected from the data: B2 `Pune`, B3 `Not found`. The IFNA alternative was run: B2 `Pune`, B3 `Not found`.
**Version note:** XLOOKUP is not in Excel 2016 and 2019 (Microsoft Support, "XLOOKUP function": "XLOOKUP is not available in Excel 2016 and Excel 2019"), so treat it as 365/2021/2024. Google Sheets has XLOOKUP with a `missing_value` argument (Google Docs Editors Help, "XLOOKUP function").
**Edge cases:** The argument can be a number, text or even `""` for blank. An empty argument slot (`,,`) is, as far as I know, treated like leaving that argument out (from memory, unverified, not run here).
**Likely follow-ups:** 1) *Why not IFERROR?* It hides every error, even a wrong range. 2) *Can it return another lookup?* Yes, you can nest a second XLOOKUP there.
**Common mistakes:** Putting if_not_found in the wrong (fifth) position, which is match_mode; forgetting quotes around text.

### Q24 ⭐⭐ 🟢 Can XLOOKUP look to the left? Show a formula that returns the employee ID when you only know the name.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the main VLOOKUP weakness and how XLOOKUP and INDEX-MATCH solve it?
**Say this in the interview:** "Yes. XLOOKUP takes the search column and the result column separately, so the result can be to the left or right. To get an ID from a name I write `=XLOOKUP(A2,Master!B:B,Master!A:A)`. VLOOKUP cannot do this because it only returns columns to the right of the key."
**Explain simply:**
- Look left = the answer sits in a column before the column you search. In the master, ID is column A and Name is column B.
- XLOOKUP gets two separate ranges: where to search (names) and what to return (IDs).
- In older Excel, INDEX-MATCH does the same job.
**Example:** A manager sends names; payroll needs IDs.
**Sample sheet:** Master A1:E6 (EmpID, Name, Dept, City, Salary). Sheet S column A holds names.

| | A | B |
|---|---|---|
| 1 | Name | EmpID |
| 2 | Meena | |
| 3 | Karan | |
| 4 | Zoya | |

**Formula / Steps:** `B2: =XLOOKUP(A2,Master!$B$2:$B$6,Master!$A$2:$A$6,"Not found")`
**Alternative:** `=INDEX(Master!$A$2:$A$6,MATCH(A2,Master!$B$2:$B$6,0))`
**Result:** XLOOKUP **not run here**; expected from the data: 103, 104, "Not found". The INDEX-MATCH version was run: Meena returns `103`, Karan returns `104`, Zoya returns `#N/A` (wrapped in IFNA it shows `Not found`). `VLOOKUP(A2,Master!A2:B6,1,FALSE)` run on the same data returns `#N/A`, which shows the left-lookup limit.
**Version note:** XLOOKUP needs 365/2021/2024, not 2016/2019 (Microsoft Support, "XLOOKUP function"); INDEX-MATCH works everywhere.
**Edge cases:** Two employees with the same name: first match wins, so look up on ID where possible.
**Likely follow-ups:** 1) *Old trick with VLOOKUP?* CHOOSE({1,2},...) rebuilds the table, but INDEX-MATCH is cleaner. 2) *Name has trailing space?* Wrap in TRIM.
**Common mistakes:** Giving ranges of different sizes; typing the lookup and return ranges in the wrong order.

### Q25 ⭐⭐ 🟢 Convert this formula to XLOOKUP: =VLOOKUP(A2, Master!A:D, 4, FALSE).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you translate old syntax to new, understanding that the column number becomes a column range?
**Say this in the interview:** "`=XLOOKUP(A2, Master!A:A, Master!D:D)`. The first column of the old table becomes the search range, and the fourth column becomes the return range. XLOOKUP is exact match by default, so I do not type FALSE, and there is no column number to break."
**Explain simply:**
- VLOOKUP's `Master!A:D, 4` means "search column A, return the 4th column, D".
- XLOOKUP: `lookup_array` = `Master!A:A`, `return_array` = `Master!D:D`.
- Default match_mode is 0 = exact (Microsoft Support, "XLOOKUP function"); VLOOKUP defaults to approximate.
**Example:** Bring City (column D) for an Employee ID.
**Sample sheet:** Master A1:E6 as in Q1 (104 = Karan, HR, Chennai). Sheet S: A2 = 104.
**Formula / Steps:** `=XLOOKUP(A2,Master!A:A,Master!D:D)`; with a message: `=XLOOKUP(A2,Master!A:A,Master!D:D,"Not found")`.
**Alternative:** `=INDEX(Master!D:D,MATCH(A2,Master!A:A,0))`
**Result:** The VLOOKUP and INDEX-MATCH versions were run on A2:D6: both return `Chennai`. XLOOKUP is **not run here**; expected `Chennai`.
**Version note:** XLOOKUP is 365/2021/2024 only (Microsoft Support, "XLOOKUP function"); Google Sheets also has it.
**Edge cases:** Whole columns include the header row; harmless for exact match unless the ID equals the header. VLOOKUP with `Master!A:D` and 4 would break if someone deleted column D (#REF!); XLOOKUP's ranges adjust.
**Likely follow-ups:** 1) *Why prefer it?* Exact by default, looks left, no column counting, built-in not-found text. 2) *What if the file goes to someone with 2016?* Keep INDEX-MATCH.
**Common mistakes:** Keeping `4` or `FALSE` in the XLOOKUP; choosing a return range that does not start on the same row as the lookup range when using partial ranges.

### Q26 ⭐⭐ 🟢 How do you return several columns (for example name, department and city) with a single XLOOKUP formula?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know XLOOKUP can return a block of columns that spill into neighbouring cells?
**Say this in the interview:** "I give XLOOKUP a return range that is several columns wide, for example `=XLOOKUP(A2,Master!A:A,Master!B:D)`. It returns Name, Dept and City together, spread across three cells. That spread is called a spill. One formula replaces three VLOOKUPs."
**Explain simply:**
- Return array = the columns you want back. Microsoft Support ("XLOOKUP function"): "XLOOKUP can return an array with multiple items."
- Spill = the result flows automatically into the empty cells to the right. You type the formula once, in the first cell.
- The cells to the right must be empty, otherwise you get #SPILL! (see Q42).
**Example:** Show name, department and city for employee 103.
**Sample sheet:** Master A1:D6 (EmpID, Name, Dept, City). Sheet S: A2 = 103; formula in B2.

| | A | B | C | D |
|---|---|---|---|---|
| 1 | EmpID | Name | Dept | City |
| 2 | 103 | | | |

**Formula / Steps:** `B2: =XLOOKUP($A2,Master!$A$2:$A$6,Master!$B$2:$D$6)`
**Alternative:** Without spill, one formula per column: `=VLOOKUP($A2,Master!$A$2:$D$6,COLUMN(B1),FALSE)` copied right (COLUMN(B1) = 2, then 3, then 4), or INDEX-MATCH per column.
**Result:** XLOOKUP is **not run here**; expected B2:D2 = `Meena`, `IT`, `Bengaluru`. The per-column alternatives were run: `Meena`, `IT`, `Bengaluru` from both the VLOOKUP-COLUMN and INDEX-MATCH versions.
**Version note:** Spilling needs 365/2021/2024; not in 2016/2019 (Microsoft Support, "XLOOKUP function"). Google Sheets XLOOKUP can also return several columns: "If result_range spans more than one row or column, the function returns the entire matching row or column" (Google Docs Editors Help, "XLOOKUP function", fetched, paraphrased). `B2#` and CHOOSECOLS are from memory, unverified.
**Edge cases:** If the ID is missing, the result is #N/A, or your if_not_found text; how that text is spread over the three cells was not tested (from memory, unverified, not run here).
**Likely follow-ups:** 1) *Reference the whole spill?* Use `B2#` in 365. 2) *Pick non-adjacent columns?* Use CHOOSECOLS in 365, or separate formulas.
**Common mistakes:** Typing the formula in all three cells; leaving something in the spill area.

### Q27 ⭐⭐ 🟢 How do you wrap a lookup in an absolute reference properly (table_array with $) and why does it matter when you drag the formula?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand relative vs absolute references, the most common cause of lookups failing after fill-down?
**Say this in the interview:** "I lock the table with dollar signs, `Master!$A$2:$C$6`, so it stays fixed when I drag down. Without the dollars, the table slides down one row with each row I copy, so later lookups miss the top rows and return #N/A. F4 adds the dollars."
**Explain simply:**
- Relative reference (`A2`) shifts when copied; absolute (`$A$2`) does not.
- The lookup value should move (A2, A3, A4); the table must not.
- Click inside the reference in the formula bar and press F4 (cycles `$A$2`, `A$2`, `$A2`, `A2`). On a laptop, Fn+F4. Alternative: turn the data into an Excel Table or use a named range.
**Example:** Three IDs are looked up; the third row should still reach the top of the master.
**Sample sheet:** Master A1:E6 (101 Asha HR, 102 Ravi Finance, ..., 105 Divya Sales). Sheet S:

| | A | B | C |
|---|---|---|---|
| 1 | EmpID | Locked | Not locked |
| 2 | 105 | | |
| 3 | 101 | | |
| 4 | 102 | | |

**Formula / Steps:** B2: `=VLOOKUP(A2,Master!$A$2:$C$6,3,FALSE)` copied down. Without dollars, copying C2 down turns the table into `Master!A3:C7`, then `Master!A4:C8`.
**Alternative:** Named range `=VLOOKUP(A2,EmpTable,3,FALSE)` or an Excel Table reference.
**Result:** Run: locked column returns `Sales`, `HR`, `Finance`; unlocked column returns `Sales`, `#N/A`, `#N/A` (I wrote the shifted addresses explicitly, which is what copying does).
**Version note:** All versions; F4 shortcut applies to Excel for Windows (Mac: Cmd+T, from memory, unverified).
**Edge cases:** When the master is on another sheet, the `$` goes on the range, not on the sheet name. Lookup in a different workbook can show the full path.
**Likely follow-ups:** 1) *When do you want a mixed reference?* Copying across and down, like `$A2`. 2) *What else prevents drift?* Excel Tables.
**Common mistakes:** Locking the lookup value too (all rows get the same result); testing only the first row.

### Q28 ⭐⭐ 🟡 How do you assign a performance grade, incentive slab or tax slab from a score or salary using VLOOKUP approximate match?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you build a slab table correctly: lower limits, ascending order, TRUE as last argument?
**Say this in the interview:** "I build a small slab table with the lower limit of each band in ascending order, then use VLOOKUP with TRUE. Excel finds the largest limit that is less than or equal to the value and returns that row's rate. It replaces a long nested IF."
**Explain simply:**
- Slab = a band, for example salary 30,000 to 49,999 gets 5%.
- The first column holds the start of each band, sorted smallest to largest, beginning with 0 so every value has a band.
- Approximate match needs sorted data (Microsoft Support, "VLOOKUP function": it assumes the first column is sorted).
**Example:** Incentive percent from salary.
**Sample sheet:**

| | A | B | | D | E |
|---|---|---|---|---|---|
| 1 | Salary from | Slab % | | Salary | Slab % |
| 2 | 0 | 0 | | 42000 | |
| 3 | 30000 | 5 | | 50000 | |
| 4 | 50000 | 10 | | 69999 | |
| 5 | 70000 | 15 | | 25000 | |
| 6 | | | | 90000 | |

(Row 2 of the table starts at 0, so 25,000 gets 0%.)
**Formula / Steps:** `E2: =VLOOKUP(D2,$A$2:$B$5,2,TRUE)` copied down.
**Alternative:** `=INDEX($B$2:$B$5,MATCH(D2,$A$2:$A$5,1))`; in 365, `=XLOOKUP(D2,$A$2:$A$5,$B$2:$B$5,,-1)` (not run here).
**Result:** Run: 42000 returns `5`; 50000 returns `10`; 69999 returns `10`; 25000 returns `0`; 90000 returns `15`. INDEX-MATCH run on 42000: `5`.
**Version note:** VLOOKUP/INDEX-MATCH in all versions and Google Sheets; XLOOKUP only 365/2021/2024.
**Edge cases:** Without the 0 row, a value below 30,000 returns #N/A (run: wrapped IFERROR shows "below slab"). Exactly on a boundary (50000) falls in the higher band. Real income-tax is progressive (each band taxed separately), so this lookup gives the rate, not the total tax.
**Likely follow-ups:** 1) *Why not nested IF?* Hard to maintain; a table is editable by HR. 2) *Text grades?* Works, return column is text.
**Common mistakes:** Using upper limits; unsorted limits; forgetting TRUE (exact match gives #N/A).

### Q29 ⭐⭐ 🟡 How do you make the column number in VLOOKUP dynamic so it does not break when columns move?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the MATCH-inside-VLOOKUP technique?
**Say this in the interview:** "I replace the typed column number with a MATCH on the header name: `=VLOOKUP(G1,A1:E4,MATCH(H1,A1:E1,0),FALSE)`. MATCH finds the position of the header 'City' in the header row, so if somebody inserts or moves columns the number updates by itself."
**Explain simply:**
- col_index_num is a hard-coded count; adding a column inside the table can make it point to the wrong field.
- `MATCH("City", header row, 0)` returns the position of that header (here 4).
- Bonus: change H1 to Dept or Salary and the same formula returns a different field.
**Example:** A monthly report where HR often adds new columns to the master.
**Sample sheet:** G1 = 103, H1 = City. (For the "after" test, a Grade column with values L2, L3, L4 for rows 2 to 4 is inserted before City.)

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | EmpID | Name | Dept | City | Salary |
| 2 | 101 | Asha | HR | Hyderabad | 42000 |
| 3 | 102 | Ravi | Finance | Pune | 55000 |
| 4 | 103 | Meena | IT | Bengaluru | 68000 |

**Formula / Steps:** `G2: =VLOOKUP(G1,A1:E4,MATCH(H1,A1:E1,0),FALSE)`
**Alternative:** `=INDEX(A2:E4,MATCH(G1,A2:A4,0),MATCH(H1,A1:E1,0))`, or XLOOKUP (365) which has no column number at all.
**Result:** Run: MATCH returns `4`, the formula returns `Bengaluru`. After inserting a Grade column before City (new table A1:F4) the MATCH version still returns `Bengaluru` (run). A hard-coded `4` would then land on Grade, and return `L4` (run in the same test).
**Version note:** All versions and Google Sheets (from memory, unverified).
**Edge cases:** A header typo or trailing space gives #N/A; duplicate headers return the first. Inserting a column just outside the table edge does not stretch the range automatically.
**Likely follow-ups:** 1) *Another fix?* COLUMNS($A:C) trick or INDEX-MATCH. 2) *Why FALSE?* Exact match.
**Common mistakes:** MATCH range that starts at a different column than the table, giving an offset position; forgetting the `0` in MATCH.

### Q30 ⭐⭐ 🟡 How do you do a two-way lookup, for example the sales of a given month for a given employee, using INDEX and MATCH?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand row-and-column lookup with two MATCH functions inside INDEX?
**Say this in the interview:** "INDEX returns the cell at a given row and column of a block. I use one MATCH to find the employee's row and a second MATCH to find the month's column: `=INDEX(B2:D5,MATCH(F1,A2:A5,0),MATCH(G1,B1:D1,0))`. It is like finding where a row and a column cross on a grid."
**Explain simply:**
- `INDEX(range, row_number, column_number)` gives the value at that position inside the range.
- First MATCH: employee name down the left side. Second MATCH: month across the top.
- The data block B2:D5 must not include the headers, so positions line up.
**Example:** Sales of Meena in February.
**Sample sheet:** F1 = Meena, G1 = Feb.

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Employee | Jan | Feb | Mar |
| 2 | Asha | 500 | 620 | 580 |
| 3 | Ravi | 700 | 650 | 720 |
| 4 | Meena | 300 | 410 | 390 |
| 5 | Karan | 450 | 480 | 510 |

**Formula / Steps:** `H1: =INDEX(B2:D5,MATCH(F1,A2:A5,0),MATCH(G1,B1:D1,0))`
**Alternative:** `=VLOOKUP(F1,A1:D5,MATCH(G1,A1:D1,0),FALSE)`; in 365, `=XLOOKUP(F1,A2:A5,XLOOKUP(G1,B1:D1,B2:D5))` (see Q39).
**Result:** Run: row MATCH = `3`, column MATCH = `2`, INDEX returns `410`; the VLOOKUP alternative also returns `410`.
**Version note:** All Excel versions and Google Sheets (from memory, unverified).
**Edge cases:** Month typed as a real date vs text "Feb" will not match; spelling or spaces give #N/A.
**Likely follow-ups:** 1) *What if names repeat?* Use a unique ID. 2) *Sum instead?* `SUMIFS` does not need the match positions.
**Common mistakes:** INDEX range includes the header row but MATCH ranges do not; swapping row and column order.

### Q31 ⭐⭐ 🟡 How do you look up a value using two or more criteria (for example Employee ID and Month) with a helper column?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the simplest, most readable multi-criteria method?
**Say this in the interview:** "I add a helper column that joins the criteria into one key, for example `=B2&"|"&C2`, which gives '102|Feb'. Then I look up the joined key the same way: `VLOOKUP(F1&"|"&G1, A2:D6, 4, FALSE)`. The separator stops false matches like 1+23 versus 12+3."
**Explain simply:**
- Helper column = an extra column you add just to make the lookup easier.
- `&` joins text. The key must be built the same way in the data and in the search.
- Easy to audit: anyone can see the key.
**Example:** Sales for employee 102 in Feb, where IDs repeat every month.
**Sample sheet:** F1 = 102, G1 = Feb. Column A is the new helper.

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Key | EmpID | Month | Sales |
| 2 | 101\|Jan | 101 | Jan | 500 |
| 3 | 102\|Jan | 102 | Jan | 700 |
| 4 | 101\|Feb | 101 | Feb | 620 |
| 5 | 102\|Feb | 102 | Feb | 650 |
| 6 | 103\|Feb | 103 | Feb | 410 |

**Formula / Steps:** A2 `=B2&"|"&C2` (copy down), then `H1: =VLOOKUP(F1&"|"&G1,A2:D6,4,FALSE)`
**Alternative:** Helper column anywhere: `=INDEX(D2:D6,MATCH(F1&"|"&G1,A2:A6,0))`; or `SUMIFS(D2:D6,B2:B6,F1,C2:C6,G1)` for numbers.
**Result:** Run: the key in A2 is `101|Jan`; VLOOKUP returns `650`; INDEX-MATCH returns `650`; a non-existent combination (103|Jan) returns `#N/A`.
**Version note:** All versions and Google Sheets (from memory, unverified).
**Edge cases:** Numbers and text-numbers join identically (102 and "102"), but stray spaces break the match; use TRIM. Key columns must be values you can rely on being unique.
**Likely follow-ups:** 1) *Downside?* Extra column, file size. 2) *Without it?* See Q32.
**Common mistakes:** No separator; building the search key differently from the helper.

### Q32 ⭐⭐ 🟡 How do you look up with multiple criteria in INDEX-MATCH without a helper column?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you use Boolean (TRUE/FALSE) arithmetic inside MATCH?
**Say this in the interview:** "I multiply conditions: `=INDEX(C2:C6, MATCH(1, INDEX((A2:A6=F1)*(B2:B6=G1),0), 0))`. Each test gives TRUE/FALSE, which becomes 1/0 when multiplied. Only a row where all conditions hold gives 1, and MATCH finds the first 1. If the answer is a number, SUMIFS is simpler."
**Explain simply:**
- `(A2:A6=F1)` tests every row and returns a list of TRUE/FALSE.
- Multiplying two lists = AND. Rows that pass both give 1.
- `INDEX(...,0)` forces the calculation of the whole list, so older Excel does not need Ctrl+Shift+Enter (from memory; I only ran it in LibreOffice). In 365 you can drop the INDEX wrapper.
**Example:** Sales for 102 in Feb.
**Sample sheet:** F1 = 102, G1 = Feb.

| | A | B | C |
|---|---|---|---|
| 1 | EmpID | Month | Sales |
| 2 | 101 | Jan | 500 |
| 3 | 102 | Jan | 700 |
| 4 | 101 | Feb | 620 |
| 5 | 102 | Feb | 650 |
| 6 | 103 | Feb | 410 |

**Formula / Steps:** `H1: =INDEX(C2:C6,MATCH(1,INDEX((A2:A6=F1)*(B2:B6=G1),0),0))`
**Alternative:** For numeric results `=SUMIFS(C2:C6,A2:A6,F1,B2:B6,G1)` or `=SUMPRODUCT((A2:A6=F1)*(B2:B6=G1)*C2:C6)`; in 365 `=XLOOKUP(1,(A2:A6=F1)*(B2:B6=G1),C2:C6)` (not run here).
**Result:** Run: INDEX-MATCH `650`; SUMPRODUCT `650`; SUMIFS `650`. For the missing pair 103/Jan, the INDEX-MATCH wrapped in IFERROR returns `Not found`.
**Version note:** Works in all versions (array behaviour in older Excel per memory); XLOOKUP form needs 365/2021/2024.
**Edge cases:** SUMIFS/SUMPRODUCT return 0 or sum duplicates when there is more than one match; INDEX-MATCH returns the first. Text results need INDEX-MATCH, not SUMIFS.
**Likely follow-ups:** 1) *OR instead of AND?* Add the tests instead of multiplying. 2) *Slow?* Yes on big ranges, calculates every row.
**Common mistakes:** Using `*` between ranges but forgetting the brackets; mismatched range sizes; whole-column ranges in an array formula.

### Q33 ⭐⭐ 🟡 How do you find the last (latest) matching entry for an employee with XLOOKUP?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know search_mode -1 (search from the bottom)?
**Say this in the interview:** "XLOOKUP's sixth argument, search_mode, set to -1, searches from the last row upward, so the first hit it finds is the latest entry: `=XLOOKUP(F1,A2:A7,C2:C7,,0,-1)`. This works if the data is in date order with the newest at the bottom."
**Explain simply:**
- search_mode: 1 = top to bottom (default), -1 = bottom to top (Microsoft Support, "XLOOKUP function").
- The empty fourth argument (`,,`) skips if_not_found; `0` is exact match.
- "Latest" really means "lowest in the list", so sort by date first or use MAXIFS on the date.
**Example:** The latest appraisal rating for employee 101.
**Sample sheet:** F1 = 101.

| | A | B | C |
|---|---|---|---|
| 1 | EmpID | Date | Rating |
| 2 | 101 | 2025-04-30 | 3 |
| 3 | 102 | 2025-04-30 | 4 |
| 4 | 101 | 2025-07-31 | 4 |
| 5 | 103 | 2025-07-31 | 2 |
| 6 | 101 | 2025-10-31 | 5 |
| 7 | 102 | 2025-10-31 | 3 |

**Formula / Steps:** `=XLOOKUP(F1,A2:A7,C2:C7,,0,-1)`
**Alternative:** Works in every version: `=LOOKUP(2,1/(A2:A7=F1),C2:C7)`.
**Result:** XLOOKUP **not run here**; expected `5` (row 6). The LOOKUP trick was run and returns `5`; plain VLOOKUP exact returns `3`, the first row.
**Version note:** XLOOKUP is 365/2021/2024, not 2016/2019 (Microsoft Support, "XLOOKUP function"). Google Sheets XLOOKUP has a search_mode argument too (Google Docs Editors Help, "XLOOKUP function").
**Edge cases:** If the data is not in date order, the bottom row is not the latest. Then use `MAXIFS` for the latest date, and look up on ID plus that date (Q31).
**Likely follow-ups:** 1) *How does LOOKUP(2,1/...) work?* Dividing 1 by FALSE gives errors, which LOOKUP skips; the last 1 wins. 2) *First entry?* Default search.
**Common mistakes:** Assuming "bottom" is "latest" on unsorted data; wrong comma count.

### Q34 ⭐⭐ 🟡 How do you do a partial-text lookup using wildcards in VLOOKUP and XLOOKUP?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know `*` and `?` and that XLOOKUP needs match_mode 2?
**Say this in the interview:** "A wildcard is a stand-in character: `*` means any run of characters and `?` means exactly one. In VLOOKUP I write `"*"&D1&"*"` with FALSE. In XLOOKUP I must set match_mode to 2: `=XLOOKUP("*"&D1&"*",A2:A5,B2:B5,,2)`."
**Explain simply:**
- `"*Kumar*"` = any text containing Kumar. `"Ra*"` = starts with Ra. `"Mee?a*"` = Mee, any one character, a, then anything.
- Microsoft Support ("VLOOKUP function"): wildcards work with FALSE and text lookup values; tilde `~` before `*` or `?` finds the real symbol. XLOOKUP wildcard needs match_mode 2 (Microsoft Support, "XLOOKUP function").
- The search column must be the text you are matching (names), not the ID.
**Example:** The user knows only the surname "Kumar".
**Sample sheet:** D1 = Kumar. Names in column A (searched), IDs in column B (returned).

| | A | B |
|---|---|---|
| 1 | Name | EmpID |
| 2 | Asha Rao | 101 |
| 3 | Ravi Kumar | 102 |
| 4 | Meena Raoji | 103 |
| 5 | Karan Shah | 104 |

**Formula / Steps:** `=VLOOKUP("*"&D1&"*",A2:B5,2,FALSE)`
**Alternative:** `=INDEX(B2:B5,MATCH("*"&D1&"*",A2:A5,0))`; XLOOKUP: `=XLOOKUP("*"&D1&"*",A2:A5,B2:B5,"Not found",2)` (not run here).
**Result:** Run: VLOOKUP `102`; INDEX-MATCH `102`; `"Mee?a*"` returns ID `103`; `"*Rao*"` returns `101` because Asha Rao is the first of two hits (Meena Raoji also matches). XLOOKUP not run; expected `102`.
**Version note:** VLOOKUP/MATCH wildcards in all Excel versions; XLOOKUP is 365/2021/2024 only. Google Sheets wildcard handling differs for some functions (unverified).
**Edge cases:** Wildcards do not work on numbers. Several hits: first wins, so too-short search text returns wrong people.
**Likely follow-ups:** 1) *Find a literal `*`?* `~*`. 2) *Why FALSE?* Wildcards need exact-style matching.
**Common mistakes:** Forgetting match_mode 2 in XLOOKUP (it then looks for a literal `*`); searching a numeric ID column.

### Q35 ⭐⭐ 🟡 Which is faster on a large dataset: VLOOKUP, INDEX-MATCH or XLOOKUP, and what can you do to speed up lookups?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Practical sense of performance, not just function names.
**Say this in the interview:** "On normal HR-sized data (tens of thousands of rows) the difference is not noticeable. What matters more is how I use them: exact match scans row by row, so I limit the range, avoid repeating the same lookup many times, and for very large sorted data use a binary search. I have not benchmarked them myself; the general view is that the three are close, with XLOOKUP and INDEX-MATCH tending to be at least as fast as VLOOKUP."
**Explain simply:**
- Exact match = Excel checks rows from the top until it finds the key. Binary search = Excel jumps to the middle and halves the list each time, much faster, but the data must be sorted.
- XLOOKUP supports binary search via search_mode 2 (ascending) or -2 (descending); unsorted data gives invalid results (Microsoft Support, "XLOOKUP function").
- Speed tips: (1) use exact ranges, not extra-large ranges; (2) look up once into a helper column and reuse it; (3) one MATCH helper column for many INDEX formulas; (4) sort and use approximate/binary search where valid; (5) convert to values when the data is final; (6) put huge joins into Power Query; (7) set calculation to manual while building.
**Example:** 100,000 payroll rows, each needing 6 fields from the master: compute the MATCH once in a helper column, then 6 INDEX formulas read that position.
**Formula / Steps:** Helper `=MATCH(A2,Master!$A$2:$A$50000,0)` in column H, then `=INDEX(Master!$C$2:$C$50000,$H2)`.
**Alternative:** Power Query merge (Data > Get Data > Combine Queries > Merge) for refreshable joins.
**Sample sheet:** Not meaningful for speed; correctness of the helper pattern was checked on the Q1 Master sheet with A2 = 104.
**Result:** Run: `MATCH` returns `4`; the INDEX reads give `HR` (Dept) and `Chennai` (City), equal to `VLOOKUP(A2,Master!A2:D6,3,FALSE)` = `HR`. No timing was measured.
**Version note:** Speed claims here are from memory, unverified, and not run (LibreOffice timings would not represent Excel). Power Query: "available in all Excel 2016 or later Windows stand alone versions" and Microsoft 365 plans (Microsoft Support, "Power Query data sources in Excel versions", fetched).
**Edge cases:** Whole-column references are fine for lookups in modern Excel but add cost in array formulas like SUMPRODUCT.
**Likely follow-ups:** 1) *Does sorting help exact match?* Not unless you use binary mode. 2) *Volatile functions?* OFFSET and INDIRECT recalculate constantly; avoid them.
**Common mistakes:** Claiming a fixed "X is 10 times faster"; thousands of lookups each returning one column.

### Q36 ⭐⭐ 🟡 You have two lists, active employees and payroll records. How do you find which employees are missing from payroll using a lookup?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Reconciliation skill: can you test "is it present in the other list?" and read the result.
**Say this in the interview:** "I check each active employee's ID against the payroll list. `=IF(ISNA(MATCH(A2,$D$2:$D$5,0)),"Missing","OK")`. MATCH returns #N/A if the ID is not in payroll, ISNA turns that into TRUE. Then I filter on Missing. I also run it the other way round to catch payroll records for people who are not active."
**Explain simply:**
- Reconciliation = comparing two lists to find differences.
- MATCH with 0 finds an exact position or gives #N/A. ISNA = "is this #N/A?".
- Running both directions finds two kinds of problem: missed payments and possible ghost payments.
**Example:** 5 active employees; payroll has 4 rows, one of which (106) is not active.
**Sample sheet:** Active in A:B, payroll IDs in D.

| | A | B | | D |
|---|---|---|---|---|
| 1 | EmpID | Name | | PayEmpID |
| 2 | 101 | Asha | | 101 |
| 3 | 102 | Ravi | | 103 |
| 4 | 103 | Meena | | 104 |
| 5 | 104 | Karan | | 106 |
| 6 | 105 | Divya | | |

**Formula / Steps:** `E2: =IF(ISNA(MATCH(A2,$D$2:$D$5,0)),"Missing","OK")`, copy to E6. Reverse check in F2: `=IF(ISNA(MATCH(D2,$A$2:$A$6,0)),"Not in active list","OK")`.
**Alternative:** `=IF(COUNTIF($D$2:$D$5,A2)=0,"Missing","OK")`; or `=IFNA(VLOOKUP(A2,$D$2:$D$5,1,FALSE),"Missing")`; in 365, `=IF(ISNA(XLOOKUP(A2,$D$2:$D$5,$D$2:$D$5)),"Missing","OK")` (not run here).
**Result:** Run: E2:E6 = `OK`, `Missing`, `OK`, `OK`, `Missing` (Ravi 102 and Divya 105 are missing). COUNTIF version gives the same. Reverse check: 101, 103, 104 `OK`; 106 `Not in active list`.
**Version note:** MATCH/COUNTIF in all versions and Google Sheets (from memory, unverified); IFNA is 2013+ per my memory (the Microsoft IFNA page lists 2016 onward).
**Edge cases:** IDs stored as text in one list and numbers in the other make everything "Missing"; fix with VALUE or a clean-up. Duplicate IDs in payroll hide double payment; add a COUNTIF > 1 check.
**Likely follow-ups:** 1) *Without formulas?* Conditional Formatting > Duplicate Values, or Power Query Merge with Left Anti. 2) *Count the missing?* `COUNTIF(E2:E6,"Missing")`.
**Common mistakes:** Checking only one direction; leaving the lookup range unlocked; using approximate match.

### Q37 ⭐⭐ 🟡 How do you use XLOOKUP for an approximate match, for example to pick the slab that applies to a given salary?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know match_mode -1 and that, unlike VLOOKUP, the table does not need sorting?
**Say this in the interview:** "I set match_mode to -1, which means exact match, or else the next smaller item: `=XLOOKUP(D2,$A$2:$A$5,$B$2:$B$5,,-1)`. With slab lower limits, 'next smaller' is the band the salary falls in. The nice part is it also works if the slab table is not sorted."
**Explain simply:**
- match_mode: 0 exact (default), -1 exact or next smaller, 1 exact or next larger, 2 wildcard (Microsoft Support, "XLOOKUP function").
- Slab tables hold the lower limit of each band, as in Q28.
- Unlike VLOOKUP TRUE and MATCH 1, the linear modes (not binary) do not demand sorted data (my understanding of the page; the page warns about sorting only for the binary search modes).
**Example:** Same incentive slab as Q28.
**Sample sheet:**

| | A | B | | D |
|---|---|---|---|---|
| 1 | Salary from | Slab % | | Salary |
| 2 | 0 | 0 | | 42000 |
| 3 | 30000 | 5 | | 50000 |
| 4 | 50000 | 10 | | 69999 |
| 5 | 70000 | 15 | | 90000 |

**Formula / Steps:** `E2: =XLOOKUP(D2,$A$2:$A$5,$B$2:$B$5,,-1)`, copy down.
**Alternative:** `=VLOOKUP(D2,$A$2:$B$5,2,TRUE)` or `=INDEX($B$2:$B$5,MATCH(D2,$A$2:$A$5,1))` (sorted ascending).
**Result:** XLOOKUP **not run here**. Expected by hand: 42000 gives 5; 50000 gives 10; 69999 gives 10; 90000 gives 15. The VLOOKUP TRUE alternative was run and returns exactly `5, 10, 10, 15`.
**Version note:** XLOOKUP is 365/2021/2024 only (Microsoft Support, "XLOOKUP function"); Google Sheets XLOOKUP also has match_mode (Google Docs Editors Help).
**Edge cases:** A salary below the smallest limit returns #N/A (or if_not_found). Do not use binary search_mode with unsorted tables.
**Likely follow-ups:** 1) *Next larger?* match_mode 1, useful for "which target is next". 2) *Descending slab table?* Works with -1 too.
**Common mistakes:** Using match_mode 1 when you meant -1; typing the slab upper limits.

### Q38 ⭐⭐ 🟡 What happens if you omit the third argument of MATCH, and why should you almost always type 0?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know MATCH's risky default, same trap as VLOOKUP's?
**Say this in the interview:** "If I leave it out, MATCH assumes 1, which is approximate match. It returns the position of the largest value that is less than or equal to what I look up, and it expects ascending order. A missing ID can silently return the neighbouring position instead of #N/A. Typing 0 means exact match."
**Explain simply:**
- Microsoft Support ("MATCH function"): match_type 1 or omitted finds the largest value less than or equal to lookup_value (array in ascending order); 0 finds the first exact value, any order; -1 finds the smallest value greater than or equal to it (descending order).
- Approximate match is right for slabs and wrong for IDs, names and codes.
- Wrong position fed into INDEX returns a real but wrong employee's data.
**Example:** Sorted IDs 101, 102, 104, 105. Looking up 103 (not in the list).
**Sample sheet:** D1 = 103.

| | A |
|---|---|
| 1 | EmpID |
| 2 | 101 |
| 3 | 102 |
| 4 | 104 |
| 5 | 105 |

**Formula / Steps:** `=MATCH(D1,A2:A5)` versus `=MATCH(D1,A2:A5,0)`
**Alternative:** To make approximate intent explicit, type `1` instead of leaving it blank; for slabs use `MATCH(x,limits,1)`.
**Result:** Run: omitted returns `2` (the position of 102, wrong); with 0 it returns `#N/A`. `INDEX(A2:A5, MATCH(D1,A2:A5))` returns `102`, a wrong employee. On unsorted data LibreOffice returned `#N/A` or arbitrary positions; Excel's exact behaviour on unsorted data may differ from LibreOffice (from memory).
**Version note:** The default applies in all Excel versions (Microsoft page applies to 365, 2024, 2021, 2019, 2016). XMATCH defaults to exact (Q40). Google Sheets MATCH default is also 1 (from memory, unverified).
**Edge cases:** Text lookups with 1 compare alphabetically; wildcards only work with 0.
**Likely follow-ups:** 1) *When is 1 right?* Slabs on sorted lower limits. 2) *What is -1?* Descending lists.
**Common mistakes:** Copying `MATCH(x,range)` from the web; trusting a result that looks plausible.

### Q39 ⭐⭐ 🟡 How do you do a two-way lookup with XLOOKUP?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you nest XLOOKUP, using the inner one to pick a column?
**Say this in the interview:** "I nest two XLOOKUPs: the inner one picks the month's column from the grid, and the outer one picks the employee's row from it: `=XLOOKUP(F1,A2:A5,XLOOKUP(G1,B1:D1,B2:D5))`. No row or column numbers needed."
**Explain simply:**
- Inner `XLOOKUP(G1,B1:D1,B2:D5)` searches the month headers and returns the whole matching column of values.
- Outer XLOOKUP then searches names (A2:A5) and returns the value from that column in Meena's position.
- Microsoft's page says XLOOKUP can return arrays, which is what makes the nesting work.
**Example:** Meena's February sales.
**Sample sheet:** F1 = Meena, G1 = Feb.

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Employee | Jan | Feb | Mar |
| 2 | Asha | 500 | 620 | 580 |
| 3 | Ravi | 700 | 650 | 720 |
| 4 | Meena | 300 | 410 | 390 |
| 5 | Karan | 450 | 480 | 510 |

**Formula / Steps:** `H1: =XLOOKUP(F1,A2:A5,XLOOKUP(G1,B1:D1,B2:D5))`
**Alternative:** `=INDEX(B2:D5,MATCH(F1,A2:A5,0),MATCH(G1,B1:D1,0))`, or `=SUMPRODUCT((A2:A5=F1)*(B1:D1=G1)*B2:D5)` (numbers only).
**Result:** XLOOKUP **not run here**; expected by hand: the inner returns the Feb column (620, 650, 410, 480), the outer picks the third item: `410`. INDEX-MATCH and SUMPRODUCT were run: both `410`.
**Version note:** 365/2021/2024 only (Microsoft Support, "XLOOKUP function"); INDEX-MATCH works everywhere.
**Edge cases:** Add an if_not_found to the outer to handle a missing name; if the month is missing, the inner gives #N/A.
**Likely follow-ups:** 1) *Why not VLOOKUP?* It needs a column number, so you add MATCH. 2) *Duplicates?* First match.
**Common mistakes:** Including header cells in the return grid; swapping the inner and outer.

### Q40 ⭐⭐ 🟡 What is XMATCH, and how is it different from MATCH?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of the modern function set and its improvements.
**Say this in the interview:** "XMATCH is the newer MATCH. It also returns the position of a value, but it defaults to exact match, can search from the bottom, supports wildcards with a setting, and has binary search options. MATCH defaults to approximate, searches only from the top."
**Explain simply:**
- Syntax: `XMATCH(lookup_value, lookup_array, [match_mode], [search_mode])` (Microsoft Support, "XMATCH function").
- match_mode: 0 exact (default), -1 exact or next smaller, 1 exact or next larger, 2 wildcard. search_mode: 1 first-to-last (default), -1 last-to-first, 2 or -2 binary search ascending/descending (same page).
- MATCH: default 1 (approximate), wildcards only with 0, no reverse search (Microsoft Support, "MATCH function").
- Use it inside INDEX the same way as MATCH.
**Example:** Find the position of the latest "Asha" entry in a list.
**Sample sheet:** D1 = Asha.

| | A |
|---|---|
| 1 | Name |
| 2 | Asha |
| 3 | Ravi |
| 4 | Asha |
| 5 | Meena |
| 6 | Asha |

**Formula / Steps:** First position: `=XMATCH(D1,A2:A6)`. Last position: `=XMATCH(D1,A2:A6,0,-1)`.
**Alternative:** `=MATCH(D1,A2:A6,0)` for the first; for the last in any version `=SUMPRODUCT(MAX((A2:A6=D1)*(ROW(A2:A6)-1)))`.
**Result:** XMATCH is **not run here**; expected by hand: first = 1, last = 5. Run in LibreOffice: MATCH exact returns `1`; the SUMPRODUCT last-position formula returns `5`; `MATCH("As*",A2:A6,0)` returns `1`.
**Version note:** XMATCH is listed for Excel 365, 2024 and 2021; the page does not mention 2016/2019 (Microsoft Support, "XMATCH function"). Google Sheets XMATCH: I have not verified.
**Edge cases:** Not found returns #N/A like MATCH. Binary modes on unsorted data give invalid results (Microsoft page).
**Likely follow-ups:** 1) *Why XMATCH + INDEX?* Same flexibility as XLOOKUP in two steps. 2) *Is MATCH obsolete?* No, it works in every version.
**Common mistakes:** Assuming XMATCH works in 2016/2019; using binary search on unsorted data.

### Q41 ⭐⭐ 🟡 How do structured (Excel Table) references help lookups when new rows are added every month?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you build lookups that keep working when the data grows, without editing formulas?
**Say this in the interview:** "I convert the master data into an Excel Table and point my lookup at the table's columns by name. When HR pastes new joiners at the bottom, the table grows and the formula automatically covers them. A fixed range like A2:C500 would silently miss row 501."
**Explain simply:**
- An **Excel Table** (Ctrl+T) is a range Excel treats as one object with a name, such as `tblEmp`, and named columns.
- A **structured reference** is a formula that uses those names, like `tblEmp[Dept]`, instead of cell addresses. Microsoft Support ("Using structured references with Excel tables"): the names adjust whenever you add or remove data in the table.
- No `$` signs are needed, and the formula reads like English.
**Example:** The payroll team adds about 30 joiners a month. With `$A$2:$C$500`, joiner number 500 is missed; with the table, nobody is missed.
**Sample sheet:** Table `tblEmp` (A1:C5), lookup key in F1:

| | A | B | C |
|---|---|---|---|
| 1 | EmpID | Name | Dept |
| 2 | 101 | Asha | HR |
| 3 | 102 | Ravi | Finance |
| 4 | 103 | Meena | IT |
| 5 | 104 | Karan | HR |

**Formula / Steps:**
1. Click any cell in the data, Insert tab > Tables group > Table (or Ctrl+T), tick "My table has headers".
2. Table Design tab > Table Name box: type `tblEmp`.
3. `=XLOOKUP(F1,tblEmp[EmpID],tblEmp[Dept])` or `=VLOOKUP(F1,tblEmp,3,FALSE)`.
**Alternative:** `=INDEX(tblEmp[Dept],MATCH(F1,tblEmp[EmpID],0))` (works in every version that has tables).
**Result:** **Not run here** (LibreOffice cannot create Excel Tables). By hand, F1 = 103 returns `IT`. Add a row 6 (105, Divya, Sales) and F1 = 105 returns `Sales` with no edit to the formula.
**Version note:** Tables and structured references are listed for Excel 2016, 2019, 2021, 365 (Microsoft Support, "Using structured references with Excel tables"); The page also lists Excel 2019, 2021, 2024 and Mobile; Excel 2007 origin is from memory, unverified. Google Sheets now has its own tables with named references (Google Docs Editors Help, "Use tables in Google Sheets", fetched). XLOOKUP needs 2021/365.
**Edge cases:** Type the new row directly under the table, with no blank row between. A lookup in a different workbook that uses a table name needs that workbook open.
**Likely follow-ups:** 1) *Alternative without tables?* Whole-column references (`A:C`) or a dynamic named range. 2) *Why not whole columns?* Fine for VLOOKUP, but slower in huge files.
**Common mistakes:** Leaving the data as a plain range; leaving a blank row so the table does not extend; typing `Table1` and forgetting to rename it.

### Q42 ⭐⭐ 🟡 Your XLOOKUP shows #SPILL!. What does it mean and how do you fix it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand how modern Excel formulas "spill" into neighbouring cells?
**Say this in the interview:** "#SPILL! means the formula wants to return several values into the cells below or beside it, and something is in the way. I clear the blocking cells, or change the formula so it returns one value."
**Explain simply:**
- A **spill** is a formula whose result takes more than one cell; Excel fills the neighbours automatically. This is called a **dynamic array** formula.
- XLOOKUP spills when the lookup value is a whole range (`A2:A20`) or when the return range has several columns.
- Microsoft Support ("Dynamic array formulas and spilled array behavior"): #SPILL! means the output range is blocked by other data.
- Fixes: delete or move whatever sits in the spill area (even a space or a hidden value counts); or make the formula return one cell, for example by looking up one key instead of a range.
**Example:** In E2 you type `=XLOOKUP(A2:A4,Master!A:A,Master!C:C)`, which wants to fill E2:E4, but E3 already holds a typed note. Result: #SPILL!. Clear E3.
**Sample sheet:** E3 holds the text "check" and blocks the spill from E2:

| | A | B | E |
|---|---|---|---|
| 2 | 101 | | `=XLOOKUP(A2:A4,Master!A:A,Master!C:C)` |
| 3 | 102 | | check |
| 4 | 103 | | |

**Formula / Steps:** 1. Click the cell with #SPILL!; the warning icon shows "Spill range isn't blank". 2. Choose "Select Obstructing Cells". 3. Delete or move them.
**Alternative:** Return a single value, `=XLOOKUP(A2,Master!A:A,Master!C:C)`, then drag down. Other causes: an Excel Table (spilled formulas are not supported inside tables: Microsoft Support, "Dynamic array formulas and spilled array behavior", fetched); merged cells in the spill area and a spill that runs off the sheet (from memory, unverified).
**Result:** **Not run here** (LibreOffice has no spill). Expected in Excel 365 once E3 is cleared: E2:E4 show the three departments.
**Version note:** Spilling exists only in 365 and 2021 (XLOOKUP and FILTER are listed only for those, Microsoft Support). The dynamic-array page's own "Applies to" list also names 2016 and 2019 and the page gives no version statement, which looks inconsistent; treat it as 2021/365 (the FILTER page lists only 365/2024/2021 plus mobile). The `E2#` spill operator is not covered on the page read (from memory, unverified).
**Edge cases:** A hidden or "empty-looking" cell with a space blocks the spill.
**Likely follow-ups:** 1) *How do you reference the spilled result?* `E2#`. 2) *How do you stop spilling?* Use one lookup value.
**Common mistakes:** Typing over the spill area; trying it inside a Table; thinking the formula is wrong when the output area is simply blocked.

### Q43 ⭐⭐ 🟡 A lookup returns 0 instead of blank when the matching cell is empty. How do you handle it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that lookups turn empty cells into 0, and can you fix it cleanly?
**Say this in the interview:** "A lookup cannot return 'nothing', so Excel shows an empty source cell as 0. I either add `&""` to turn it into empty text, or test it with IF and return blank."
**Explain simply:**
- VLOOKUP and INDEX return the *value* of the cell; an empty cell has value 0 when treated as a number.
- A 0 in a Manager column looks like real data and can mislead a report.
- `&""` joins an empty piece of text to the result: blank stays blank (empty text), "Rohit" stays "Rohit". Side effect: numbers become text.
**Example:** Ravi (102) has no manager recorded; the report shows 0.
**Sample sheet:** E1 = 102:

| | A | B | C |
|---|---|---|---|
| 1 | EmpID | Name | Manager |
| 2 | 101 | Asha | Rohit |
| 3 | 102 | Ravi | |
| 4 | 103 | Meena | Rohit |
| 5 | 104 | Karan | |

**Formula / Steps:** Plain: `=VLOOKUP(E1,A2:C5,3,FALSE)`. Fix 1: `=VLOOKUP(E1,A2:C5,3,FALSE)&""`. Fix 2: `=IF(VLOOKUP(E1,A2:C5,3,FALSE)="","",VLOOKUP(E1,A2:C5,3,FALSE))`.
**Alternative:** `=IF(INDEX(C2:C5,MATCH(E1,A2:A5,0))="","",INDEX(C2:C5,MATCH(E1,A2:A5,0)))`. In 365, `LET` avoids repeating the lookup (not run here).
**Result:** Run in LibreOffice: plain formula returns `0`; fix 1, fix 2 and the INDEX version return empty text (shown as blank). For 103 all return `Rohit`.
**Version note:** All versions for these formulas; Google Sheets behaves the same (from memory, unverified).
**Edge cases:** `&""` converts numeric results (salary) to text, so SUM ignores them. For numbers use the IF version, which returns the number untouched. A cell holding a formula that returns "" is not zero, it is already empty text.
**Likely follow-ups:** 1) *Can you hide zeros with formatting?* Yes (`0;-0;;@`), but a real 0 would also vanish. 2) *Is the cell really empty?* Check with `ISBLANK`.
**Common mistakes:** Using `&""` on salary columns; testing `=0` so a genuine 0 is also blanked.

### Q44 ⭐ 🟢 What is the LOOKUP function, and how is it different from VLOOKUP?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the older function and its sorted-data rule?
**Say this in the interview:** "LOOKUP is an old, simpler function. In its vector form it searches one row or column and returns the item at the same position in another. It always does approximate matching and needs sorted data. VLOOKUP lets me choose exact match, so I prefer it."
**Explain simply:**
- **Vector form:** `LOOKUP(lookup_value, lookup_vector, [result_vector])`: two separate ranges. **Array form:** one block; Microsoft says it exists for compatibility and recommends VLOOKUP/HLOOKUP instead (Microsoft Support, "LOOKUP function").
- No exact-match option: values must be in ascending order, otherwise results may be wrong. If the value is smaller than everything, it returns #N/A.
- It can look left, because the result range is separate.
**Example:** Score 78 goes to a grade band.
**Sample sheet:**

| | A | B | | D |
|---|---|---|---|---|
| 1 | 0 | D | | 78 |
| 2 | 50 | C | | 49 |
| 3 | 70 | B | | |
| 4 | 85 | A | | |

**Formula / Steps:** `=LOOKUP(D1,A1:A4,B1:B4)`
**Alternative:** `=VLOOKUP(D1,A1:B4,2,TRUE)` or `=INDEX(B1:B4,MATCH(D1,A1:A4,1))`.
**Result:** Run in LibreOffice: 78 returns `B`; 49 returns `D`; `=LOOKUP(-5,A1:A4,B1:B4)` returns `#N/A`; 1000 returns `A`; array form `=LOOKUP(70,A1:B4)` returns `B`.
**Version note:** Listed for Excel 2016, 2019, 2021, 2024, 365 (Microsoft Support, "LOOKUP function"); older versions have it too (from memory, unverified).
**Edge cases:** Unsorted data gives wrong answers with no error. Case is ignored.
**Likely follow-ups:** 1) *Why not use it for IDs?* It cannot force exact match. 2) *Any famous use?* The last-match trick (Q58).
**Common mistakes:** Using it on unsorted IDs; mixing the array form with a table wider than two columns.

### Q45 ⭐ 🟢 What are TRUE/FALSE and 1/0 as the last argument of VLOOKUP, and are they interchangeable?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the 4th argument's exact meaning and the risky default?
**Say this in the interview:** "FALSE and 0 both mean exact match; TRUE and 1 both mean approximate. Yes, they are interchangeable. I type FALSE or 0 for IDs. If I leave it out, Excel assumes TRUE, which is the trap."
**Explain simply:**
- Excel treats 0 as FALSE and any other number as TRUE, so 1, 2 or -1 all mean approximate.
- Approximate = largest value not above the key, on ascending-sorted data.
- Omitted = TRUE (Microsoft Support, "VLOOKUP function").
**Example:** Looking up a score of 78 in a grade table (lower limits 0, 50, 70, 85).
**Sample sheet:** A1:B4 = (0,D), (50,C), (70,B), (85,A); D1 = 78.
**Formula / Steps:** `=VLOOKUP(D1,A1:B4,2,TRUE)`; with `1`; with `FALSE`; with `0`; with the argument omitted.
**Alternative:** For exact matching, `=INDEX(B1:B4,MATCH(D1,A1:A4,0))` has no ambiguity.
**Result:** Run in LibreOffice for 78: TRUE `B`, 1 `B`, omitted `B`, 2 `B`; FALSE `#N/A`, 0 `#N/A`. For 70: FALSE returns `B`.
**Version note:** All versions and Google Sheets (Sheets names it `is_sorted`; Google Docs Editors Help, "VLOOKUP", describes it as the optional exact/approximate setting).
**Edge cases:** Text-typed "FALSE" (in quotes) is not the logical FALSE.
**Likely follow-ups:** 1) *Which is more readable?* FALSE. 2) *Why dangerous when omitted?* Unsorted IDs give wrong rows silently.
**Common mistakes:** Forgetting the argument; assuming 1 means exact.

### Q46 ⭐ 🟢 How do you get the row number or position of a value in a list?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know MATCH, and the difference between position in a range and the sheet row?
**Say this in the interview:** "MATCH with 0 gives the position of the value inside the range I give it. If the range starts at row 1 that equals the sheet row; otherwise I add the starting row minus one, or use ROW with INDEX."
**Explain simply:**
- **Position** = "it is the 4th item in the list". **Sheet row** = the number on the left of the grid.
- `MATCH(value, range, 0)` returns position; 0 means exact.
**Example:** Where is employee 104 in the ID list?
**Sample sheet:**

| | A |
|---|---|
| 1 | EmpID |
| 2 | 101 |
| 3 | 102 |
| 4 | 103 |
| 5 | 104 |
| 6 | 105 |

D1 = 104.
**Formula / Steps:** Position: `=MATCH(D1,A2:A6,0)`. Sheet row: `=MATCH(D1,A1:A6,0)` or `=ROW(INDEX(A2:A6,MATCH(D1,A2:A6,0)))`.
**Alternative:** `=XMATCH(D1,A2:A6)` in 2021/365 (not run here). Result by hand: 4.
**Result:** Run in LibreOffice: `MATCH(D1,A2:A6,0)` = `4`; `MATCH(D1,A1:A6,0)` = `5`; ROW/INDEX version = `5`; `MATCH(999,A2:A6,0)` = `#N/A`.
**Version note:** MATCH: all versions and Google Sheets. XMATCH: 2021/365 (Microsoft Support, "XMATCH function").
**Edge cases:** Duplicates give the first position. Text-numbers do not match real numbers.
**Likely follow-ups:** 1) *Use for INDEX?* Yes, MATCH feeds INDEX. 2) *Last position?* Use XMATCH with search_mode -1.
**Common mistakes:** Confusing position with sheet row; omitting the 0.

### Q47 ⭐ 🟢 Do VLOOKUP, INDEX-MATCH and XLOOKUP work in Google Sheets, and what differs from Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you move between Excel and Sheets, since many HR teams use both?
**Say this in the interview:** "All three work in Google Sheets. VLOOKUP is the same four inputs. INDEX-MATCH is the same. XLOOKUP exists too, with slightly different argument names. The main difference is in how formulas spill and how cross-file lookups work."
**Explain simply:**
- **VLOOKUP:** same four inputs: search key, range, column index, optional exact/approximate setting (Google Docs Editors Help, "VLOOKUP").
- **XLOOKUP:** `XLOOKUP(search_key, lookup_range, result_range, [missing_value], [match_mode], [search_mode])`; the default for missing is #N/A; match modes 0, -1, 1, 2 and search modes 1, -1, 2, -2 as in Excel (Google Docs Editors Help, "XLOOKUP function"). Excel calls the third optional argument `if_not_found`.
- **INDEX-MATCH:** works (from memory, unverified).
- Differences: another file is read with `IMPORTRANGE`, which "pulls a block of cells from another spreadsheet" (Google Docs Editors Help, "IMPORTRANGE", fetched; title and gist only); `ARRAYFORMULA` lets results fill several rows and lets non-array functions work with arrays (Google Docs Editors Help, "ARRAYFORMULA", fetched). Using them for lookups is from memory, unverified; Sheets has no *Excel* Tables, but it now has its own Tables feature (Format > Convert to table; Google Docs Editors Help, "Use tables in Google Sheets", fetched).
**Example:** The same HR master list queried in both tools.
**Sample sheet:** Same Master layout as Q1 (EmpID, Name, Dept, City, Salary); not rebuilt in Sheets.
**Formula / Steps:** Same text works in both: `=VLOOKUP(A2,Master!A:C,3,FALSE)`. Sheets: `=XLOOKUP(A2,Master!A:A,Master!C:C,"Not found")`.
**Alternative:** `=INDEX(Master!C:C,MATCH(A2,Master!A:A,0))`.
**Result:** Not run here (Google Sheets is not available in this environment); behaviour as documented above.
**Version note:** Excel XLOOKUP is 2021/365 only; Sheets has no versions to worry about, which is its advantage.
**Edge cases:** Sheets' VLOOKUP, like Excel's, is not case-sensitive (from memory, unverified).
**Likely follow-ups:** 1) *Cross-file?* IMPORTRANGE. 2) *Fill-down?* ARRAYFORMULA.
**Common mistakes:** Assuming an Excel-only function (LET, XMATCH) behaves identically in Sheets without checking.

### Q48 ⭐ 🟡 A VLOOKUP only returns the first match. How can you return all rows that match a value?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know VLOOKUP's limit and a workaround for one-to-many lookups?
**Say this in the interview:** "In 365 or 2021 I use FILTER, which returns every match in one formula. In older versions I add a helper column that numbers each occurrence, like HR-1, HR-2, and look those up one by one."
**Explain simply:**
- **One-to-many lookup** = one key, several answers (one department, many employees).
- **FILTER** (365/2021 only; Microsoft Support, "FILTER function") returns all rows that meet a condition.
- **Helper column** = an extra column that makes each key unique, so VLOOKUP can find the 1st, 2nd, 3rd.
**Example:** List all HR employees.
**Sample sheet:** A is the helper key:

| | A | B | C |
|---|---|---|---|
| 1 | Key | Name | Dept |
| 2 | HR-1 | Asha | HR |
| 3 | Finance-1 | Ravi | Finance |
| 4 | HR-2 | Meena | HR |
| 5 | IT-1 | Karan | IT |
| 6 | HR-3 | Divya | HR |

E1 = HR; F1:F4 = 1, 2, 3, 4.
**Formula / Steps:** Helper A2: `=C2&"-"&COUNTIF(C$2:C2,C2)` (drag down). Then G1: `=IFERROR(VLOOKUP($E$1&"-"&F1,$A$2:$B$6,2,FALSE),"")` (drag down).
**Alternative:** 365/2021: `=FILTER(B2:B6,C2:C6=E1)`. Older: array formula `=IFERROR(INDEX($B$2:$B$6,SMALL(IF($C$2:$C$6=$E$1,ROW($C$2:$C$6)-ROW($C$2)+1),F1)),"")` (Ctrl+Shift+Enter).
**Result:** Run in LibreOffice: helper approach returns `Asha`, `Meena`, `Divya`, then blank; the INDEX/SMALL array formula, entered as an array formula, returns the same (without array entry it returned wrong values such as `Ravi`). FILTER **not run here**; expected (pandas-style by hand) Asha, Meena, Divya.
**Version note:** FILTER: Excel 2021, 2024, 365 plus mobile apps (Microsoft Support, "FILTER function", Applies-to list). Helper and array methods: all versions.
**Edge cases:** FILTER returns #CALC! when nothing matches unless you add the third argument, e.g. `"None"` (Microsoft Support, "FILTER function", fetched: "a #CALC! error will result"). Helper keys break if rows are sorted after the numbering is hard-typed; keep it as a formula.
**Likely follow-ups:** 1) *Pivot alternative?* Yes, a PivotTable lists names under each dept. 2) *Count matches?* `COUNTIF`.
**Common mistakes:** Expecting VLOOKUP to loop; hard-typing helper keys.

### Q49 ⭐ 🟡 How do you look up many values at once with one XLOOKUP formula instead of dragging it down?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand dynamic arrays and spilling?
**Say this in the interview:** "I give XLOOKUP the whole range of keys as the first argument. In 365 or 2021 it returns one answer per key and spills down by itself, so there is nothing to drag."
**Explain simply:**
- Normally the first argument is one cell. Give it `D2:D5` and XLOOKUP answers for each item.
- The results **spill** into the cells below (see Q42), so the cells below the formula must be empty.
- If the list of keys grows, point to its spill with `D2#` if the keys themselves come from a spilling formula.
**Example:** Fetch departments for four attendance IDs.
**Sample sheet:**

| | A | B | | D |
|---|---|---|---|---|
| 1 | EmpID | Dept | | Query |
| 2 | 101 | HR | | 103 |
| 3 | 102 | Finance | | 101 |
| 4 | 103 | IT | | 104 |
| 5 | 104 | HR | | 999 |

**Formula / Steps:** In E2: `=XLOOKUP(D2:D5,A2:A5,B2:B5,"Not found")`
**Alternative:** `=VLOOKUP(D2:D5,A2:B5,2,FALSE)` also spills in 365; classic way is to write one formula and drag.
**Result:** **Not run here** (no spill in LibreOffice). Expected, by hand: E2:E5 = IT, HR, HR, Not found.
**Version note:** Needs 365/2021 (XLOOKUP not in 2016/2019, Microsoft Support, "XLOOKUP function"). Google Sheets: the XLOOKUP help page describes search_key as one value and does not address a range of keys; whether it spills or needs `ARRAYFORMULA` was not confirmed (unverified).
**Edge cases:** Blocked spill area gives #SPILL!. If `if_not_found` is omitted, missing keys show #N/A in their rows.
**Likely follow-ups:** 1) *Return several columns?* Make the return range wider (Q26). 2) *Excel 2019?* Write one formula and drag.
**Common mistakes:** Typing over the spill; using it in an Excel Table.

### Q50 ⭐ 🟡 How do you do a case-sensitive lookup?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know lookups ignore case, and can you use EXACT?
**Say this in the interview:** "VLOOKUP, MATCH and XLOOKUP treat 'ab12' and 'AB12' as the same. For case-sensitive matching I use EXACT, which compares letter by letter, inside INDEX and MATCH."
**Explain simply:**
- **EXACT(text1, text2)** returns TRUE only if both are identical including capitals.
- Wrap it: MATCH finds the position of the first TRUE, INDEX returns the result from that position.
**Example:** Badge codes `ab12`, `AB12`, `Ab12` belong to different people.
**Sample sheet:** D1 = AB12:

| | A | B |
|---|---|---|
| 1 | Code | Name |
| 2 | ab12 | Asha |
| 3 | AB12 | Ravi |
| 4 | Ab12 | Meena |

**Formula / Steps:** `=INDEX(B2:B4,MATCH(TRUE,INDEX(EXACT(D1,A2:A4),0),0))` (the inner `INDEX(...,0)` avoids Ctrl+Shift+Enter).
**Alternative:** `=INDEX(B2:B4,SUMPRODUCT(EXACT(D1,A2:A4)*(ROW(A2:A4)-ROW(A2)+1)))`; 365/2021: `=XLOOKUP(TRUE,EXACT(D1,A2:A4),B2:B4)` (not run here).
**Result:** Run in LibreOffice: ordinary `VLOOKUP(D1,A2:B4,2,FALSE)` returns `Asha` (wrong, first case-blind match); the EXACT-based formulas return `Ravi`. A missing code wrapped in IFERROR returns the text you choose.
**Version note:** All versions for INDEX/MATCH/EXACT; XLOOKUP form 365/2021. Google Sheets: same functions (from memory, unverified).
**Edge cases:** SUMPRODUCT version breaks if duplicates exist (it adds positions); the MATCH version returns the first. Trailing spaces still count as different.
**Likely follow-ups:** 1) *Is VLOOKUP case-sensitive?* No (Q22). 2) *Why EXACT?* It is the only built-in case-sensitive text comparison.
**Common mistakes:** Using `=` instead of EXACT (the equals sign ignores case).

### Q51 ⭐ 🟡 How do you find the closest date or the nearest value in a list (for example the policy period a joining date falls in)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know approximate match for periods, and a "nearest" formula for values?
**Say this in the interview:** "For 'which period does this date fall in' I list each period's start date in ascending order and use approximate match: it returns the last start date on or before the joining date. For the truly nearest number I find the smallest absolute difference."
**Explain simply:**
- **Approximate match** returns the largest value that is not above the key.
- **Absolute difference** = distance ignoring direction, `ABS(range - target)`.
- Excel stores dates as numbers, so date lookups work like number lookups.
**Example:** Joining date 15-Nov-2025: which policy period applies?
**Sample sheet:** D1 = 15-Nov-2025, D2 = 01-Feb-2024:

| | A | B |
|---|---|---|
| 1 | Start date | Policy |
| 2 | 01-Apr-2024 | P1 |
| 3 | 01-Jan-2025 | P2 |
| 4 | 01-Oct-2025 | P3 |
| 5 | 01-Apr-2026 | P4 |

**Formula / Steps:** `=VLOOKUP(D1,A2:B5,2,TRUE)`. Nearest value, with salaries in H2:H6 (42000, 47000, 55000, 68000, 39000) and J1 = 50000: array formula (Ctrl+Shift+Enter in older Excel) `=INDEX(H2:H6,MATCH(MIN(ABS(H2:H6-J1)),ABS(H2:H6-J1),0))`.
**Alternative:** `=INDEX(B2:B5,MATCH(D1,A2:A5,1))`; 365/2021: `=XLOOKUP(D1,A2:A5,B2:B5,,-1)` (not run here; match_mode -1 means exact or next smaller).
**Result:** Run in LibreOffice: D1 gives `P3`; INDEX-MATCH gives `P3`; D2 (before first start) gives `#N/A`, which `IFERROR(...,"Before first policy")` turns into text; nearest to 50000 returns `47000` (distance 3000 against 5000 for 55000).
**Version note:** VLOOKUP/MATCH: all versions. XLOOKUP form: 2021/365. The nearest formula run as an array formula (Ctrl+Shift+Enter) returned `47000`; entered normally it returned a wrong value (`42000`) in LibreOffice, so array-enter it in older Excel. In 365 it works natively (from memory, unverified).
**Edge cases:** Ties return the first. Dates stored as text will not work.
**Likely follow-ups:** 1) *Closest date after?* match_mode 1. 2) *Unsorted starts?* Sort first.
**Common mistakes:** Unsorted period list; using end dates as the table.

### Q52 ⭐ 🟡 How would you build an employee look-up card where choosing a name from a drop-down shows their department, manager and salary?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you combine data validation with lookups into a usable mini-tool?
**Say this in the interview:** "I make a drop-down of names with Data Validation, then each field on the card uses a lookup keyed on that cell. Change the name and the whole card updates."
**Explain simply:**
- **Data Validation list** = a cell that only accepts values from a list, shown as a drop-down arrow.
- Each card field is one lookup using the selected name.
- Wrap in IFERROR so an empty selection shows blank, not #N/A.
**Example:** HR helpdesk picks "Meena" and sees IT, Sam, 68000.
**Sample sheet:** Sheet `Data` A1:E5; card on another sheet with the selected name in G1:

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | EmpID | Name | Dept | Manager | Salary |
| 2 | 101 | Asha | HR | Rohit | 42000 |
| 3 | 102 | Ravi | Finance | Neha | 55000 |
| 4 | 103 | Meena | IT | Sam | 68000 |
| 5 | 104 | Karan | HR | Rohit | 39000 |

**Formula / Steps:**
1. Select G1 > Data tab > Data Tools > Data Validation > Allow: List > Source: `=$B$2:$B$5` > OK.
2. G2 (Dept): `=INDEX(C2:C5,MATCH(G1,B2:B5,0))`; G3 (Manager): same with D; G4 (Salary): same with E.
**Alternative:** `=XLOOKUP(G1,B2:B5,E2:E5)` (365/2021) or `=VLOOKUP(G1,B2:E5,4,FALSE)` (the name must be the first column).
**Result:** Run in LibreOffice for "Meena": Dept `IT`, Manager `Sam`, Salary `68000`; VLOOKUP version gives `IT` for dept. The Data Validation drop-down itself is a feature step, not run here. A blank or unknown name wrapped in IFERROR returns blank.
**Version note:** Data Validation and INDEX-MATCH: all versions. Google Sheets: Data > Data validation (from memory, unverified).
**Edge cases:** Two employees with the same name: use EmpID in the drop-down. Make the source a Table column so new joiners appear automatically (Q41).
**Likely follow-ups:** 1) *Dependent drop-downs?* Possible with INDIRECT. 2) *Protect formulas?* Review > Protect Sheet.
**Common mistakes:** Duplicate names; list range not covering new rows; forgetting IFERROR.

### Q53 ⭐ 🟡 You do not know which of three monthly sheets holds an employee. How do you search across the sheets?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you chain lookups with fallbacks?
**Say this in the interview:** "I nest IFERROR around three VLOOKUPs: try January, if it errors try February, then March, else show 'Not in any sheet'. I also use COUNTIF to tell me which sheet had it."
**Explain simply:**
- IFERROR(a, b) runs b only if a gives an error. Nesting makes a chain of fallbacks.
- COUNTIF counts matches per sheet: 0 means not there.
- With many sheets, consider combining them into one table (Power Query) instead.
**Example:** Find salary for ID 104, which might be in Jan, Feb or Mar.
**Sample sheet:** Each of `Jan`, `Feb`, `Mar` has EmpID in A and Salary in B (rows 2-3):

| Sheet | A2 | B2 | A3 | B3 |
|---|---|---|---|---|
| Jan | 101 | 42000 | 102 | 55000 |
| Feb | 103 | 68000 | 104 | 39000 |
| Mar | 105 | 47000 | 106 | 51000 |

Search IDs in `S`!A2:A5 = 104, 106, 101, 999.
**Formula / Steps:** `=IFERROR(VLOOKUP(A2,Jan!$A$2:$B$3,2,FALSE),IFERROR(VLOOKUP(A2,Feb!$A$2:$B$3,2,FALSE),IFERROR(VLOOKUP(A2,Mar!$A$2:$B$3,2,FALSE),"Not in any sheet")))`
**Alternative:** Sheet finder: `=IF(COUNTIF(Jan!$A$2:$A$3,A2),"Jan",IF(COUNTIF(Feb!$A$2:$A$3,A2),"Feb",IF(COUNTIF(Mar!$A$2:$A$3,A2),"Mar","none")))`. 365: `VSTACK` the sheets then XLOOKUP (not run here, from memory).
**Result:** Run in LibreOffice: 104 returns `39000` (Feb); 106 returns `51000` (Mar); 101 returns `42000` (Jan); 999 returns `Not in any sheet`. Sheet finder returns Feb, Mar, Jan, none.
**Version note:** All versions for IFERROR/COUNTIF (IFERROR is 2007+).
**Edge cases:** IFERROR also hides other errors (typo in range). An ID in two sheets returns the earliest sheet in the chain. Use IFNA to hide only "not found" (Q20).
**Likely follow-ups:** 1) *More than three sheets?* Combine with Power Query. 2) *Which sheet?* The COUNTIF finder.
**Common mistakes:** Forgetting `$` so ranges slide; forgetting the final fallback.

### Q54 ⭐ 🟡 You are asked to replace all VLOOKUPs in a workbook with XLOOKUP. What do you check first?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you think about who opens the file and where behaviour differs before mass-changing formulas?
**Say this in the interview:** "First I check that everyone who opens the file has 2021 or 365, since XLOOKUP is missing in 2016 and 2019. Then I check the behaviour differences: exact match is the default, there are no wildcards by default, and the column index becomes a return range."
**Explain simply:**
- **Versions:** XLOOKUP is not available in Excel 2016 and 2019 (Microsoft Support, "XLOOKUP function"); those users see #NAME?.
- **Match default:** VLOOKUP without the 4th argument is approximate; XLOOKUP defaults to exact. A silent bug may become a visible #N/A. That is usually good, but it changes numbers.
- **Wildcards:** exact VLOOKUP honours `*` and `?`; XLOOKUP needs match_mode 2 (Microsoft Support, "XLOOKUP function").
- **Return range:** map column 3 to the third column of the table.
- Also: links from other workbooks, Google Sheets users, macros that read the formula text.
**Example:** A bonus table where someone omitted FALSE.
**Sample sheet:** A2:B5 = (101 Asha), (103 Meena), (105 Divya), ("107" Karan, text); D1 = 104, D2 = "Me*", D3 = 107.
**Formula / Steps:** Old: `=VLOOKUP(D1,A2:B5,2)`. New: `=XLOOKUP(D1,A2:A5,B2:B5,"Not found")`.
**Alternative:** Keep VLOOKUP for files shared with 2016/2019 users, or switch to INDEX-MATCH, which works for everyone.
**Result:** Run in LibreOffice: `VLOOKUP(104,...)` with no 4th argument returns `Meena` (ID 103, wrong); with FALSE `#N/A`; `VLOOKUP("Me*",B2:B5,1,FALSE)` returns `Meena`; number 107 against text "107" returns `#N/A`. The XLOOKUP results (`Not found` for 104; no wildcard by default) are **not run here**.
**Version note:** See above; Google Sheets has XLOOKUP (Google Docs Editors Help).
**Edge cases:** Compare before and after on a copy; difference counts should be investigated, not ignored.
**Likely follow-ups:** 1) *Is it worth it?* Not if files circulate to 2019 users. 2) *How to test?* Compare old and new columns with `=A2=B2`.
**Common mistakes:** Replacing blindly, then discovering colleagues see #NAME?; ignoring the approximate-match default.

### Q55 ⭐ 🟡 What is binary search mode in XLOOKUP, and when is it safe to use?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the speed-versus-risk trade-off of sorted-data searching?
**Say this in the interview:** "Binary search repeatedly halves the list, so it is very fast on huge data, but it only works if the data is sorted. I set search_mode to 2 for ascending or -2 for descending, and only use it when I am sure of the sort order."
**Explain simply:**
- **Binary search** = open the list in the middle, decide whether to go up or down, repeat. Like finding a name in a sorted phone book.
- search_mode values: 1 first to last (default), -1 last to first, 2 binary ascending, -2 binary descending (Microsoft Support, "XMATCH function"; XLOOKUP uses the same codes). If not sorted, "invalid results will be returned".
- Safe when: IDs are always sorted and the list is large (hundreds of thousands of rows). Not worth it for small lists.
**Example:** 500,000 sorted transaction IDs.
**Sample sheet:** Sorted A2:B6 = 101 B, 103 C, 105 D, 107 E, 109 F; unsorted D2:E6 = 105 B, 101 C, 109 D, 103 E, 107 F; G1 = 107.
**Formula / Steps:** `=XLOOKUP(G1,A2:A6,B2:B6,"Not found",0,2)`.
**Alternative:** `VLOOKUP(...,TRUE)` also uses binary search; `MATCH(...,1)` too.
**Result:** XLOOKUP **not run here**. The same logic run in LibreOffice with VLOOKUP TRUE: sorted list returns `E` (correct); unsorted list returns `C` for 107 (wrong, row 101), and `#N/A` for 101, while exact match returns `F`.
**Version note:** XLOOKUP/XMATCH: 2021 and 365 (Microsoft Support, "XMATCH function"). Google Sheets XLOOKUP also has search_mode 2/-2 (Google Docs Editors Help).
**Edge cases:** No error is raised on unsorted data, only wrong answers.
**Likely follow-ups:** 1) *Default mode?* Linear, safe. 2) *Gain?* Noticeable only on very large data.
**Common mistakes:** Using binary on unsorted data; trusting speed over correctness.

### Q56 ⭐ 🔴 How can the CHOOSE function be used to make VLOOKUP look to the left?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the classic workaround and when INDEX-MATCH is cleaner?
**Say this in the interview:** "CHOOSE with {1,2} builds a temporary two-column table in whatever order I want, so I can put the name column first and the ID column second, then VLOOKUP into that. It works, but I would normally use INDEX-MATCH."
**Explain simply:**
- **VLOOKUP** returns only columns to the right of its key column.
- **CHOOSE(index_num, value1, value2)**: with an array `{1,2}` as index it returns both ranges side by side as one virtual table.
- Swap the order so the search column comes first.
**Example:** Find the EmpID of "Meena" when the ID sits left of the name.
**Sample sheet:** D1 = Meena:

| | A | B |
|---|---|---|
| 1 | EmpID | Name |
| 2 | 101 | Asha |
| 3 | 102 | Ravi |
| 4 | 103 | Meena |
| 5 | 104 | Karan |

**Formula / Steps:** `=VLOOKUP(D1,CHOOSE({1,2},B2:B5,A2:A5),2,FALSE)`
**Alternative:** `=INDEX(A2:A5,MATCH(D1,B2:B5,0))`; 365: `=XLOOKUP(D1,B2:B5,A2:A5)` (not run here).
**Result:** Run in LibreOffice: all three variants (`{1,2}`, `{2,1}`, INDEX-MATCH) return `103`.
**Version note:** Works in all versions as an array construct; in pre-dynamic-array Excel some people needed Ctrl+Shift+Enter (from memory, unverified). Google Sheets needs `{B2:B5,A2:A5}` curly braces instead (from memory, unverified).
**Edge cases:** Slower on big ranges because the virtual table is rebuilt.
**Likely follow-ups:** 1) *Better way?* INDEX-MATCH. 2) *Why braces?* `{1,2}` is an array constant.
**Common mistakes:** Mixing up the order; ranges of different lengths.

### Q57 ⭐ 🔴 How do you return the nth match (second or third occurrence) of a value using INDEX with SMALL?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you extract the kth matching row without a helper column?
**Say this in the interview:** "IF builds a list of row numbers where the department matches, SMALL picks the nth smallest of those, and INDEX returns the name in that row. The nth is a number I can drag down."
**Explain simply:**
- Inside the IF, non-matching rows become FALSE, which SMALL ignores.
- `SMALL(list, 2)` = second smallest, i.e. the second match.
- Older Excel needs Ctrl+Shift+Enter (an **array formula**, one formula working on many cells at once).
**Example:** The 1st, 2nd, 3rd HR employee.
**Sample sheet:** D1 = HR; E1:E4 = 1, 2, 3, 4:

| | A | B |
|---|---|---|
| 1 | Dept | Name |
| 2 | HR | Asha |
| 3 | IT | Karan |
| 4 | HR | Meena |
| 5 | Finance | Ravi |
| 6 | HR | Divya |
| 7 | IT | Sam |

**Formula / Steps:** F1: `=IFERROR(INDEX($B$2:$B$7,SMALL(IF($A$2:$A$7=$D$1,ROW($A$2:$A$7)-ROW($A$2)+1),E1)),"none")` (array formula), drag down.
**Alternative:** 365/2021: `=INDEX(FILTER(B2:B7,A2:A7=D1),E1)` (not run here). Without array entry: `AGGREGATE(15,6,...)` divides by the condition; it did not work in LibreOffice here, and I cannot confirm it from a source, so treat it as unverified for Excel.
**Result:** Run in LibreOffice (array formula): `Asha`, `Meena`, `Divya`, `none`.
**Version note:** Array-entered version: all versions; FILTER 2021/365 (Microsoft Support, "FILTER function").
**Edge cases:** When n exceeds the matches, SMALL errors; IFERROR handles it.
**Likely follow-ups:** 1) *Last match?* Q58. 2) *Easier?* FILTER.
**Common mistakes:** Forgetting array entry; wrong ROW offset.

### Q58 ⭐ 🔴 What is the classic LOOKUP(2,1/(range=value),result_range) trick, and what does it return?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you recognise the last-match trick and can you explain why it works?
**Say this in the interview:** "It returns the last matching entry. The test makes TRUE or FALSE, 1 divided by that gives 1 or an error, and LOOKUP searching for the big number 2 skips the errors and lands on the last 1."
**Explain simply:**
- `range=value` gives TRUE/FALSE per row. `1/TRUE` = 1; `1/FALSE` = #DIV/0! (error).
- LOOKUP searches for 2 (bigger than any 1), so it settles on the last 1, ignoring errors. Microsoft states LOOKUP needs sorted data; this works because every non-error is 1, so the data is effectively sorted.
- Returns the matching row's value from the result range, or #N/A if nothing matches.
**Example:** The latest department record for each employee in a log.
**Sample sheet:** D1 = HR (same list as Q57):

| | A | B |
|---|---|---|
| 2 | HR | Asha |
| 3 | IT | Karan |
| 4 | HR | Meena |
| 5 | Finance | Ravi |
| 6 | HR | Divya |
| 7 | IT | Sam |

**Formula / Steps:** `=LOOKUP(2,1/(A2:A7=D1),B2:B7)`
**Alternative:** 365/2021: `=XLOOKUP(D1,A2:A7,B2:B7,,0,-1)` (not run here). Last row: `=LOOKUP(2,1/(A2:A7=D1),ROW(A2:A7))`.
**Result:** Run in LibreOffice: returns `Divya`; for "Legal" `#N/A`; the ROW variant returns `6`.
**Version note:** LOOKUP: 2016 onward listed (Microsoft Support, "LOOKUP function"); works in earlier versions without Ctrl+Shift+Enter (from memory, unverified).
**Edge cases:** The ranges must be the same size.
**Likely follow-ups:** 1) *Why 2?* Any number above 1. 2) *Modern alternative?* XLOOKUP with search_mode -1.
**Common mistakes:** Expecting the first match; mismatched ranges.

### Q59 ⭐ 🔴 How can INDIRECT make a VLOOKUP pick its sheet from a cell value, and what are the risks?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know dynamic references and their costs?
**Say this in the interview:** "INDIRECT turns text like 'Jan'!A2:C3 into a real reference, so the sheet name can come from a cell. The risks: it is volatile, breaks if sheets are renamed, and needs other workbooks to be open."
**Explain simply:**
- INDIRECT "returns the reference specified by a text string" (Microsoft Support, "INDIRECT function").
- **Volatile** = recalculates at every change, slowing big files (the Microsoft INDIRECT page read does not mention this; from memory, unverified).
- If the text points to a closed workbook, it returns #REF! (Microsoft Support).
- Names with spaces need single quotes inside the text.
**Example:** A summary sheet pulls salary from the monthly sheet named in column B.
**Sample sheet:** Sheets `Jan`, `Feb`, `Pay Mar` each have A2:C3: (101 Asha, salary), (102 Ravi, salary). In `S`, A = 102, B = sheet name. Salaries of ID 102: Jan 55000, Feb 56500, Pay Mar 57000 (ID 101 earns 1000 less in each); no sheet named Apr.

| | A | B |
|---|---|---|
| 2 | 102 | Jan |
| 3 | 102 | Feb |
| 4 | 102 | Pay Mar |
| 5 | 102 | Apr |

**Formula / Steps:** `=IFERROR(VLOOKUP(A2,INDIRECT("'"&B2&"'!$A$2:$C$3"),3,FALSE),"sheet missing")`
**Alternative:** Fixed nested IFERROR (Q53), or combine sheets with Power Query.
**Result:** Run in LibreOffice: Jan `55000`, Feb `56500`, Pay Mar `57000`, Apr `sheet missing`. Without the quotes, `Pay Mar` returns `#REF!`.
**Version note:** All versions; Google Sheets uses `INDIRECT` the same way (from memory, unverified).
**Edge cases:** Renaming a sheet does not update text inside INDIRECT. Formula auditing cannot trace it.
**Likely follow-ups:** 1) *Alternative?* Consolidate data. 2) *Why slow?* Volatile.
**Common mistakes:** Missing quotes; typos.

### Q60 ⭐ 🔴 How can XLOOKUP return a reference so that you can sum between two lookup points?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know XLOOKUP returns a cell reference, not just a value?
**Say this in the interview:** "Because XLOOKUP returns a reference, I can put a colon between two XLOOKUPs, which makes a range from the first found cell to the second, and SUM it. For example, total sales from February to May."
**Explain simply:**
- XLOOKUP's result is a cell reference, so `XLOOKUP(...):XLOOKUP(...)` is a range. Microsoft Support ("XLOOKUP function", Example 6, fetched) uses exactly this pattern inside SUM and says "XLOOKUP returns a range".
- Older equivalent is `INDEX(...):INDEX(...)`, which also returns references.
- Both ends are included.
**Example:** Total sales from the month in D1 to the month in E1.
**Sample sheet:** D1 = Feb, E1 = May:

| | A | B |
|---|---|---|
| 1 | Month | Sales |
| 2 | Jan | 10 |
| 3 | Feb | 20 |
| 4 | Mar | 30 |
| 5 | Apr | 40 |
| 6 | May | 50 |
| 7 | Jun | 60 |

**Formula / Steps:** `=SUM(XLOOKUP(D1,A2:A7,B2:B7):XLOOKUP(E1,A2:A7,B2:B7))`
**Alternative:** `=SUM(INDEX(B2:B7,MATCH(D1,A2:A7,0)):INDEX(B2:B7,MATCH(E1,A2:A7,0)))`.
**Result:** XLOOKUP form **not run here**; by hand 20+30+40+50 = `140`. INDEX form run in LibreOffice: `140`; excluding both ends (`+1`/`-1`) gives `70`.
**Version note:** XLOOKUP form 2021/365; INDEX form all versions. Google Sheets XLOOKUP reference behaviour: not verified.
**Edge cases:** If the end comes before the start, Excel still builds the range (from memory, unverified); check the order. Missing month gives #N/A.
**Likely follow-ups:** 1) *Why not SUMIFS?* Also fine with dates. 2) *Exclude ends?* Shift with +1/-1.
**Common mistakes:** Thinking XLOOKUP only returns values.

