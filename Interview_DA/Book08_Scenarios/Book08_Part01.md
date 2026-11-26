# Book 8 — Scenario-Based & Data Interpretation | Part 1: Data Quality Scenarios (Missing, Wrong, Duplicate Data) 🟢🟡🔴

**Target:** 70 questions | **Actual:** 72 questions
**Scope:** On-the-job data quality scenarios for an analyst: missing, wrong, inconsistent and duplicate data, reconciliation between sources, and how to check, fix and communicate, with inline exercise data where a figure can be derived.

### Q1 ⭐⭐⭐ 🟢 What are the main dimensions of data quality (completeness, accuracy, consistency, uniqueness, validity, timeliness), and what is one HR-data example of a failure in each?
**Asked at:** commonly asked (no company-specific report found); data-quality dimensions appear in prep-site question banks (unverified).
**What the interviewer is checking:** Whether you have a vocabulary for "bad data" instead of just saying "the data is messy".
**Say this in the interview:** "Data quality has six common dimensions. I check each one before trusting a dataset, and I can give you an HR example of each."
**Explain simply:**
- **Completeness:** are required values present? Failure: 150 new joiners have a blank date of joining.
- **Accuracy:** does the value match reality? Failure: a monthly salary field typed as 5,20,000 when payroll paid 52,000 (an extra zero).
- **Consistency:** do two places (or two rows) agree? Failure: HRIS says "Active" while payroll says "Exited" for the same person.
- **Uniqueness:** is each real thing recorded once? Failure: a rehired employee gets a new ID and is counted twice.
- **Validity:** does the value follow the allowed format or range? Failure: a date of birth in 2031, or gender coded "X1" when only M/F/O are allowed.
- **Timeliness:** is the data recent enough for the decision? Failure: attrition is reported on an exit list that was last refreshed two months ago.
**Mini-example:** If 20 of 400 records have a blank manager ID, completeness for that field is 380/400 = 95%.
**Practice step:** Take any HR sheet you know and write one check per dimension.
**Likely follow-ups:** 1) *Which matters most?* It depends on the decision; for payroll, accuracy; for a weekly dashboard, timeliness. 2) *Are accuracy and validity the same?* No: "31 Feb" is invalid; a valid-looking but wrong date of joining is inaccurate.
**Common mistakes / traps:** Treating accuracy and validity as one thing; listing the words with no example; forgetting that a field can be complete yet wrong.

### Q2 ⭐⭐⭐ 🟢 You are handed a new dataset and asked for analysis by tomorrow. What checks do you run before doing any analysis?
**Asked at:** commonly asked (no company-specific report found); "what do you check first" is a staple of question banks (unverified).
**What the interviewer is checking:** That you inspect data before trusting it, and in a sensible order under time pressure.
**Say this in the interview:** "I spend the first part of the time on a quick health check: size, keys, missing values, duplicates, ranges and totals against a known number. Then I analyse."
**Clarify first:** What decision will this support, what does one row represent, what is the date range, and who owns the data?
**Plan:**
1. Size and shape: row count, column count, data types; does the row count match what the owner expected?
2. Grain and key: which column(s) identify one row; count distinct values against rows.
3. Missing values: blank share per column, especially the columns I need.
4. Duplicates: exact and on the business key.
5. Ranges and valid values: min/max, impossible values (negative age, future joining dates), category spellings.
6. Reconcile: one total (headcount, revenue) against a trusted source.
7. Write down every assumption and fix in a short log.
**Method choice and why:** Simple counts, filters and a pivot first; code only if the file is too large for Excel.
**Pitfalls:** Starting the analysis before knowing what a row means; silently deleting rows; trusting a file because it "came from the system".
**Deliverable:** A half-page data-check note sent with the analysis: what I found, what I fixed, what I assumed.
**Likely follow-ups:** 1) *What if there is no time?* Do keys, totals and nulls on needed columns, and state the limits. 2) *Do you fix the source?* I flag it to the owner; I fix my copy and log it.
**Common mistakes / traps:** Jumping to charts; overwriting the raw file; no reconciliation to a known total.

### Q3 ⭐⭐⭐ 🟢 An HRIS export has 1,250 rows. 30 employee IDs appear twice and 10 employee IDs appear three times; every other ID appears once. How many unique employees are there, and by what percentage would a row count overstate headcount?
Inline data: rows 1,250; IDs appearing twice 30; IDs appearing three times 10.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate rows from unique entities and can do the arithmetic cleanly.
**Say this in the interview:** "There are 1,200 unique employees. Counting rows gives 1,250, which overstates headcount by about 4.2%."
**What the data shows:** Some IDs repeat, so rows are more than people.
**Working:**
1. Rows used by repeated IDs: 30 x 2 + 10 x 3 = 60 + 30 = 90 rows.
2. Rows with a once-only ID: 1,250 - 90 = 1,160 IDs.
3. Unique IDs: 1,160 + 30 + 10 = 1,200.
4. Extra rows: 1,250 - 1,200 = 50 (30 x 1 + 10 x 2).
5. Overstatement: 50 / 1,200 = 4.17%.
**Result:** 1,200 unique employees; the row count overstates by 50 people, 4.2% (rounded to one decimal).
**Caveats / what else I would check:** Whether repeats are true duplicates or legitimate history rows (transfers, promotions, rehires) with different effective dates; if a rehire has a new ID the count could be wrong the other way.
**Next step / recommendation:** Count distinct employee ID (`COUNT(DISTINCT employee_id)`), keep the latest effective row per ID, and tell the owner the export is not one row per person.
**Likely follow-ups:** 1) *Overstatement against rows instead?* 50 / 1,250 = 4.0%; say which base you use. 2) *How do you find them?* Group by ID and keep those with count above 1.
**Common mistakes / traps:** Subtracting only 30 + 10 = 40 (forgetting the third copies); dividing by 1,250 without saying so; deleting repeats before checking they are really duplicates.

### Q4 ⭐⭐⭐ 🟢 In a 2,000-row orders table, 140 rows have a blank discount_amount. What share is missing, and would you treat the blanks as zero discount?
Inline data: rows 2,000; blank discount_amount 140.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you do not assume a blank means zero without evidence.
**Say this in the interview:** "7% are blank. I would not assume zero until I confirm with the system owner whether blank means 'no discount' or 'not recorded'."
**What the data shows:** A small minority of rows have no discount value.
**Working:**
1. Missing share: 140 / 2,000 = 0.07 = 7%.
2. Check what blank means: are blanks concentrated in one channel, date range or payment type? Does the order total equal list price x quantity (which would suggest no discount)?
3. Compare the blank rows' total against list price: if price paid equals list price, zero is reasonable; if the price is lower, a discount existed but was not recorded.
**Result:** 7% missing. Zero only if evidence supports it; otherwise leave as missing and report it.
**Caveats / what else I would check:** The system may write blank for "no discount" and 0 for "discount of zero" differently; a data-entry form may have changed; treating blanks as zero can understate total discount and overstate net revenue.
**Next step / recommendation:** Confirm the rule with the owner, then either fill 0 with a note or report totals "with 140 orders unverified". Show both numbers if the difference is material.
**Likely follow-ups:** 1) *If 7% were randomly missing?* Impact is small; if concentrated in one region, bias is likely. 2) *What would you do in SQL?* `COALESCE(discount_amount, 0)` only after confirming.
**Common mistakes / traps:** Filling zero by habit; averaging discounts over only non-blank rows without saying so; not asking what blank means.

### Q5 ⭐⭐⭐ 🟢 How do you find duplicate records in a dataset, and how do you decide which copy to keep?
**Asked at:** commonly asked (no company-specific report found); duplicate handling and "keep the latest record" appear in question banks (unverified).
**What the interviewer is checking:** A method for finding duplicates and a rule (not a guess) for choosing the survivor.
**Say this in the interview:** "I first decide what makes two rows 'the same thing', then group by that key and count. I keep one record using a written rule, usually the most recent or most complete."
**Clarify first:** What is the business key (employee ID, order ID, email plus date)? Are repeats errors or valid history?
**Plan:**
1. Define the key; count rows per key (`GROUP BY key HAVING COUNT(*) > 1`; in Excel, a pivot or a COUNTIF helper column).
2. Separate exact copies (all columns equal) from conflicting ones (same key, different values).
3. Choose the survivor by a rule: latest update date, most filled fields, trusted source system.
4. Keep the removed rows in a separate "duplicates removed" table for audit.
5. Recount and reconcile the total.
**Method choice and why:** A simple group-and-count first; ranking with `ROW_NUMBER()` when I must keep exactly one row per key.
**Pitfalls:** Removing history rows that are valid; keeping the first row by file order (arbitrary); not logging the removal.
**Deliverable:** A clean table, a list of removed records and the rule used, in one line each.
**Likely follow-ups:** 1) *What if copies disagree?* Ask the data owner or use the source-priority rule. 2) *Could you lose data?* Yes, so I archive the removed rows.
**Common mistakes / traps:** Using "Remove Duplicates" on all columns when only the key is repeated; no rule for the survivor; not checking counts afterwards.

### Q6 ⭐⭐⭐ 🟢 What is the difference between an exact duplicate and a near-duplicate, and how would you handle each in an employee master file?
**Asked at:** commonly asked (no company-specific report found); HR-data duplicate sources (rehires, name changes) are described in vendor blogs (unverified).
**What the interviewer is checking:** That you know simple de-duplication is not enough when spelling or format varies.
**Say this in the interview:** "An exact duplicate is identical in every field and is safe to drop. A near-duplicate is the same person with small differences, so I flag it for review rather than delete automatically."
**Explain simply:**
- **Exact duplicate:** same ID, name, date of joining, everything. Often caused by exporting twice or a bad join. Remove, keeping one, and log it.
- **Near-duplicate:** "Rahul Sharma" and "Rahul K Sharma", a surname change after marriage, a rehire with a new ID, or the same person with two email spellings.
- **How to handle near-duplicates:** standardise text (trim, lower case), then match on stronger fields (date of birth, PAN-style ID or phone, treated carefully as personal data); list candidate pairs; a person reviews; merge using a "golden record" rule.
**Mini-example:** Two rows for E1021, identical: drop one. Two rows "Priya Nair, DOB 1994-05-02" and "Priya R Nair, DOB 1994-05-02" with different IDs: flag, check with HR, then link.
**Practice step:** Build a pivot of name plus date of birth with count above 1 and look at what turns up.
**Likely follow-ups:** 1) *Why not auto-merge?* Two different people can share a name; a wrong merge is worse than a duplicate. 2) *Privacy?* Limit access to personal fields; follow company policy (confirm with the data protection owner).
**Common mistakes / traps:** Trusting name alone; deleting without review; ignoring leading or trailing spaces that hide duplicates.

### Q7 ⭐⭐⭐ 🟢 How do you decide whether to drop rows with missing values, impute them, or leave them as missing?
**Asked at:** commonly asked (no company-specific report found); drop-versus-impute is a repeated theme in prep guides (unverified).
**What the interviewer is checking:** A reasoned decision based on how much is missing, why, and what the analysis needs.
**Say this in the interview:** "I first ask why it is missing and how much. Small, random gaps I may drop; important or structured gaps I impute carefully or keep as 'unknown' and say so."
**Clarify first:** Which column, what share is missing, and is the gap random or tied to a group (for example, one office not filling the field)?
**Plan:**
1. Measure missing share per column and per group.
2. Decide if the field is needed for this question at all.
3. Choose: drop rows if the share is small and the gap looks random; impute (median, mode, or a value from a related field) if the field matters and the pattern is understood; leave as "Unknown" if missing itself carries meaning (for example, no exit date means still employed).
4. Run the result with and without the choice to see if the conclusion changes.
5. Document the choice.
**Method choice and why:** Simplest defensible option first; no imputation at all is often the honest choice for reports.
**Pitfalls:** Dropping rows that are all from one department (bias); filling the mean, which hides spread; treating a legitimate blank as an error.
**Deliverable:** The result plus a line such as "12% of engagement scores were blank; conclusions hold with and without them."
**Likely follow-ups:** 1) *What threshold do you use?* No fixed rule; judgement per column (I would say so). 2) *Mean or median?* Median if there are outliers.
**Common mistakes / traps:** One rule for every column; imputing without telling the reader; dropping rows before checking the pattern.

### Q8 ⭐⭐⭐ 🟡 Your dashboard shows 5,000 active customers but the CRM team says 4,600. How do you find out why the numbers differ before replying to your manager?
Inline data: dashboard 5,000; CRM 4,600.
**Asked at:** commonly asked (no company-specific report found); source-mismatch and reconciliation prompts appear in question banks (unverified).
**What the interviewer is checking:** That you investigate step by step, starting with definitions, instead of defending your number or accepting theirs.
**Say this in the interview:** "I would not pick a side yet. The gap is 400, about 8%; I would first compare how each side defines 'active', then reconcile down to a list of the differing customers."
**First, clarify / contain:** Do not reply with a number yet. Tell my manager "I am reconciling and will update by a fixed time". Ask the CRM team for their definition, extract date and filters.
**What I would check, in order:**
1. Definition of "active" (purchase in last 90 days vs account status flag).
2. Date and time of each extract (timing and refresh lag).
3. Filters: test accounts, internal users, regions or product lines excluded on one side.
4. Duplicates: the same customer under two IDs in my model (`COUNT(DISTINCT customer_id)` vs rows).
5. Join problems: a join that multiplies customers.
6. Record-level match: get both ID lists and find IDs only in one list; sample 20 to see the pattern.
**If I find...:** Definition difference means agree one written definition and show both numbers labelled; duplicates or a join fan-out mean fix my model and republish; timing difference means align the cut-off; CRM missing records means raise with the CRM owner.
**What I would tell the stakeholder:** "The two systems differ by 400 customers (8% of my figure, 8.7% of CRM's). I have compared definitions and am matching the two lists; I will confirm the cause and the figure to use by 4 pm."
**Prevent it next time:** A shared metric definition in a data dictionary, and a monthly automated reconciliation between dashboard and CRM.
**Likely follow-ups:** 1) *Which number is right?* Whichever matches the agreed definition; neither is "right" until defined. 2) *What if the manager needs a number now?* Give the range 4,600 to 5,000 with the reason.
**Common mistakes / traps:** Defending your dashboard; blaming the other team; changing the dashboard before finding the cause.

### Q9 ⭐⭐⭐ 🟡 You find that a pipeline bug has put wrong values in a key column for the last three weeks, and reports using it have already gone to leadership. What do you do, and what do you say?
**Asked at:** commonly asked (no company-specific report found); pipeline-error-after-reporting is a common scenario prompt (unverified).
**What the interviewer is checking:** Ownership, speed, honest communication, and a lasting fix, in that order.
**Say this in the interview:** "I would tell the right people early, before they find it, stop the wrong data from spreading, size the impact, and come back with a corrected number and a fix."
**First, clarify / contain:** Tell my manager and the pipeline owner now. Pause the affected refresh or mark the dashboard "under review". Do not quietly patch and hope nobody notices.
**What I would check, in order:**
1. Exact start and end date of the bug, and the column affected.
2. Which reports, dashboards and downstream tables used it, and who received them.
3. How wrong the values are: compare against a trusted source for a sample of rows.
4. Which decisions or figures leadership took from them.
5. Whether the correct values can be rebuilt from the source (backfill).
**If I find...:** Small impact on figures means send a short correction note; material impact means a prompt call with the leaders before the note; source data missing means state what cannot be restored.
**What I would tell the stakeholder:** "For the last three weeks a pipeline error affected the [column], so [report] figures sent on [dates] are wrong. The effect is about [x]. Corrected figures will be ready by [time]. Please hold decisions based on the earlier numbers until then."
**Prevent it next time:** Automated checks on key columns (ranges, null share, reconciliation to source) with alerts, and a short written post-incident note.
**Likely follow-ups:** 1) *Who do you tell first?* My manager and the pipeline owner, same hour. 2) *Do you resend all reports?* Resend the affected ones with the changes highlighted.
**Common mistakes / traps:** Waiting to be fully sure; fixing quietly; blaming a colleague; sending a correction with no corrected number.

### Q10 ⭐⭐⭐ 🟡 How do you explain a data quality problem to a non-technical stakeholder who still needs a number today?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can be honest and still useful: a number, a confidence level, and a next step.
**Say this in the interview:** "I give the best available number first, say how confident I am, name the problem in one plain sentence, and say when a better one will arrive."
**First, clarify / contain:** Ask what decision the number feeds and how precise it must be; that tells me whether a rough figure is enough.
**What I would check, in order:**
1. How big the problem is (share of records affected).
2. Which direction it pushes the number (over or under).
3. The best estimate I can defend (for example, with the bad rows excluded) and a range.
4. Whether the decision would change anywhere in that range.
**If I find...:** Decision unaffected by the range means give the figure and note it; decision sensitive means say "do not finalise on this yet" and give the time for the fix.
**What I would tell the stakeholder:** "Attrition for the quarter is about 14%, and I would put it between 13% and 15% (illustrative figures). Around 5% of exit dates are missing, which is why I cannot be exact. I will confirm by tomorrow noon. For today's discussion, 14% is safe to use as a rough figure."
**Prevent it next time:** Show a data-quality note (coverage, last refresh) on the report itself.
**Likely follow-ups:** 1) *Avoid jargon?* Yes: "blank", "duplicate", "late", not "null" or "referential integrity". 2) *What if they insist on one exact number?* Give the best number, mark it provisional.
**Common mistakes / traps:** Refusing to give a number; hiding the problem; giving a long technical explanation; false precision.

### Q11 ⭐⭐⭐ 🟡 A payroll file has one salary of 9,50,00,000 per annum while every other value is between 3 and 40 lakh. How do you decide what to do with it?
**Asked at:** commonly asked (no company-specific report found); outlier handling is a standard theme (unverified).
**What the interviewer is checking:** That you investigate an outlier before deleting or keeping it.
**Say this in the interview:** "9,50,00,000 is 9.5 crore, about 24 times the next possible maximum. I would first check whether it is a typing error, a unit error or a real executive package, and not delete it blindly."
**First, clarify / contain:** Keep the raw file. Do not delete or edit the row yet. Check the figure: 9,50,00,000 / 40,00,000 is 23.75 times the highest normal value.
**What I would check, in order:**
1. Employee, grade and role: is the person plausible for such a package (leadership, a joining or retention bonus counted as salary)?
2. Digits: could 9,50,000 (9.5 lakh) have received extra zeros, or monthly vs annual confusion?
3. Compare with the same employee's previous months or years, and with the payroll register.
4. Whether the column holds annual CTC or also bonuses and stock value.
**If I find...:** Typing or unit error means correct with the owner's confirmed value; real figure means keep it and report with and without it, or use the median; cannot be verified means exclude from averages, flag it, and say so.
**What I would tell the stakeholder:** "One record shows 9.5 crore against a normal range of 3 to 40 lakh. I have asked Payroll to confirm; until then I show the average both with and without it."
**Prevent it next time:** A validation rule that flags salary outside an expected band for the grade.
**Likely follow-ups:** 1) *Mean or median?* Median for pay summaries because one value can distort the mean. 2) *Is it sensitive?* Yes; share only with those allowed.
**Common mistakes / traps:** Deleting it as "obviously wrong"; keeping it so the average is distorted; editing the source file.

### Q12 ⭐⭐⭐ 🟡 After joining an orders table to a customers table, the row count rises from 10,000 to 10,900. What has probably happened and how do you confirm it?
Inline data: orders before join 10,000; rows after join 10,900.
**Asked at:** commonly asked (no company-specific report found); nulls and duplicates in joins appear in question banks (unverified).
**What the interviewer is checking:** Whether you know that a join on a non-unique key multiplies rows.
**Say this in the interview:** "The customers table probably has some customers more than once, so each matching order was repeated. I would count rows per customer ID in the customers table to confirm."
**What the data shows:** A join of orders (many) to customers (should be one per customer) should keep 10,000 rows. It gave 900 extra, a 9% increase.
**Working:**
1. Extra rows: 10,900 - 10,000 = 900.
2. Increase: 900 / 10,000 = 9.0%.
3. Check uniqueness: `SELECT customer_id, COUNT(*) FROM customers GROUP BY customer_id HAVING COUNT(*) > 1`.
4. Find affected orders: those joined to a duplicated customer ID.
5. Compare `COUNT(DISTINCT order_id)` after the join to 10,000.
**Result:** Likely a fan-out (rows multiplied) from duplicate keys in the customers table; 900 extra rows. (Not certain: it could also be a join on a non-key column.)
**Caveats / what else I would check:** The customers table may be a history table with one row per address change; revenue totals are now overstated by the repeated orders; a join on the wrong column can also multiply rows.
**Next step / recommendation:** Reduce customers to one row per ID (keep the current record), rejoin, and confirm the row count returns to 10,000 and revenue matches the orders table.
**Likely follow-ups:** 1) *Could it be a LEFT JOIN issue?* A left join keeps at least all orders; rows only rise with repeated keys. 2) *What if the count fell?* An inner join dropped unmatched orders.
**Common mistakes / traps:** Not checking row counts after a join; using DISTINCT to hide the problem; not checking the totals.

### Q13 ⭐⭐⭐ 🟡 The dashboard shows total revenue of 12,40,000 while Finance's ledger shows 11,98,000 for the same month. What is the gap in rupees and as a percentage of the Finance figure, and what are the first causes you check?
Inline data: dashboard 12,40,000; Finance 11,98,000.
**Asked at:** commonly asked (no company-specific report found); revenue reconciliation between sources is a common prompt (unverified).
**What the interviewer is checking:** Correct arithmetic and a sensible order of checks.
**Say this in the interview:** "The dashboard is higher by Rs 42,000, which is 3.5% of Finance's figure. I would check definitions and timing first, then duplicates and returns."
**What the data shows:** Dashboard is higher than the ledger.
**Working:**
1. Gap: 12,40,000 - 11,98,000 = Rs 42,000.
2. As a share of Finance: 42,000 / 11,98,000 = 3.51% (3.5%).
**Result:** Rs 42,000 higher on the dashboard; 3.5% of the Finance figure.
**Caveats / what else I would check (in order):**
1. Definition: gross vs net of returns, discounts, GST (tax), cancellations.
2. Cut-off: orders booked vs invoiced vs cash received; month-end timing and time zone.
3. Duplicates in my data (repeat orders, join fan-out).
4. Returns, refunds and credit notes recorded in Finance but not in the dashboard.
5. Test or internal orders in the dashboard.
6. Then match transaction by transaction: list IDs in one but not the other.
**Next step / recommendation:** Build a bridge: dashboard total, minus each explained item, equals Finance total, with any remainder shown as unexplained. Agree one definition with Finance.
**Likely follow-ups:** 1) *Percentage of dashboard?* 42,000 / 12,40,000 = 3.4%; state the base. 2) *Is 3.5% acceptable?* Depends on the tolerance agreed with Finance.
**Common mistakes / traps:** Using the wrong base; assuming Finance is always right; reporting a gap with no explanation.

### Q14 ⭐⭐⭐ 🟡 A column you need is 45% null. How do you decide whether you can still use it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you test whether the non-missing data is representative and decide in terms of the analysis, not a fixed cut-off.
**Say this in the interview:** "45% null does not automatically make it unusable. I check why it is blank, whether the filled 55% represents everyone, and whether I can answer the question on that subset."
**Clarify first:** What question needs the column, and is a partial answer acceptable ("for the 55% with data")?
**Plan:**
1. Why is it blank: not applicable (for example, exit reason for active staff), not collected, or lost?
2. Compare the filled and blank groups on other fields (department, location, tenure) to see whether missingness is random.
3. If random and the filled sample is large enough, analyse that subset and say so.
4. If biased, either find another source for the field, impute with a stated method, or avoid the conclusion.
5. Show a sensitivity check (results with the available data vs alternatives).
**Method choice and why:** Subset analysis with a clear caveat first; imputation only when the gaps are understood and the field is critical.
**Pitfalls:** Assuming the 55% represents everyone; imputing 45% of values and calling them data; dropping the column without telling anyone.
**Deliverable:** The result labelled with coverage ("based on the 55% who answered") and a recommendation to improve collection.
**Likely follow-ups:** 1) *Is there a cut-off like 30%?* Rules of thumb exist, but I treat them as unverified; the reason and pattern matter more. 2) *Would you impute?* Only with a stated method.
**Common mistakes / traps:** Applying a fixed cut-off blindly; ignoring who is missing; hiding the coverage.

### Q15 ⭐⭐⭐ 🟡 How do you make your data cleaning steps documented and reproducible so that someone else can audit them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether your work can be repeated and checked by someone else, not just done once.
**Say this in the interview:** "I never edit the raw file. Every fix is a scripted or written step, in order, with counts before and after, so another person can rerun it and get the same result."
**Clarify first:** Who will audit it, how often will it be repeated, and which tool is the team standard?
**Plan:**
1. Keep the raw data untouched and read-only; work on a copy.
2. Do cleaning in a script, SQL view, Power Query or a recorded sequence of steps, not manual cell edits.
3. Keep a change log: step, reason, rows affected before and after, who and when.
4. Save removed or changed rows in a separate table.
5. Run checks at the end: row count, totals and uniqueness agree with the log.
6. Version the files and write a short data dictionary and assumptions note.
**Method choice and why:** Power Query or a script gives an automatic record; if Excel manual edits are unavoidable, log each one.
**Pitfalls:** Silent manual edits; "final_v3_new" files; fixes that cannot be repeated next month.
**Deliverable:** Clean data, a cleaning log and a one-page assumptions note, stored where the team can reach them.
**Likely follow-ups:** 1) *Why keep raw data?* To redo or challenge any step. 2) *How would an auditor verify?* Rerun the script on the raw file and compare counts.
**Common mistakes / traps:** Overwriting the source; no counts in the log; undocumented assumptions.

### Q16 ⭐⭐⭐ 🟡 You raise a data error that originates in another team's system, and they say it is low priority. How do you get it addressed while still delivering your analysis?
**Asked at:** commonly asked (no company-specific report found); stakeholder-influence scenarios are standard behavioural prompts (unverified).
**What the interviewer is checking:** Influence without authority: evidence, business impact, and not stalling your own work.
**Say this in the interview:** "I would not wait, and I would not argue. I would deliver with a workaround and a clear caveat, and show the other team the business impact so the priority is judged on facts."
**First, clarify / contain:** Ask what their priority rule is and what they need to act (examples, a ticket, impact figures). Do not escalate in anger.
**What I would check, in order:**
1. A clear example set: 5 to 10 records, what is wrong, what the correct value should be.
2. Impact: how many records, which report or decision, what cost (for example, headcount off by 2%).
3. A workaround I can apply on my side and still be transparent.
4. Who owns the data and who has authority to prioritise (my manager, a data governance lead).
**If I find...:** Impact is small means keep the workaround and a ticket with a review date; impact is material means ask my manager to raise it with their lead with my evidence.
**What I would tell the stakeholder:** "The analysis is delivered with a workaround for [issue]. It affects about [x]% of rows and moves the result by about [y]. A ticket is open with the source team; I will update the numbers when it is fixed."
**Prevent it next time:** A shared data-issue log with owners, severity and dates; agreed data-quality checks at the source.
**Likely follow-ups:** 1) *Do you escalate?* Yes, with evidence, after trying direct conversation, through my manager. 2) *Do you fix their system?* No; I do not change another team's data.
**Common mistakes / traps:** Waiting silently; escalating without evidence; patching quietly with no caveat; blaming.

### Q17 ⭐⭐⭐ 🟡 An attendance export shows an employee with 26 days present in a month that has 22 working days. List the possible causes and say how you would fix the file.
Inline data: working days 22; days present 26.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can list plausible HR-process causes, not only technical ones.
**Say this in the interview:** "26 present against 22 working days is 4 extra days, which is 18% above the maximum. Before correcting, I would check whether this is weekend or holiday work, duplicate punches, or a data error."
**First, clarify / contain:** Keep the raw export. Ask how "days present" is defined and whether working days include weekly offs or holidays.
**What I would check, in order:**
1. Days worked on weekly offs or public holidays (valid; usually compensatory off or overtime).
2. Duplicate rows or double punches (same date counted twice).
3. Shifts crossing midnight counted as two days.
4. Overlap of two records (transfer between locations, two ID entries for one person).
5. Regularisation or manual entries added twice.
6. A wrong calendar or month in the report.
**If I find...:** Valid weekend or holiday work means keep it and add a column to separate "worked on a non-working day"; duplicates mean remove the extra rows and log it; two employee IDs mean link and merge; unexplained means flag to HR operations, not guess.
**What I would tell the stakeholder:** "One employee shows 26 days against 22 working days. Four of those days may be weekend or holiday work, which I am checking; the attendance report will show them separately once confirmed, and payroll should confirm the comp-off rule."
**Prevent it next time:** A validation rule: days present cannot exceed days in the month, and exceptions above working days must carry a reason code.
**Likely follow-ups:** 1) *Could 26 be right?* Yes, if weekly off or holiday days were worked. 2) *Fix by capping at 22?* No; that would hide valid overtime.
**Common mistakes / traps:** Capping at 22 without checking; deleting the row; not asking how the system defines a working day.

### Q18 ⭐⭐⭐ 🟡 HRIS says 5,240 active employees, payroll says 5,198, and Finance says 5,215. How would you reconcile headcount, and what is the largest gap between any two sources?
Inline data: HRIS 5,240; payroll 5,198; Finance 5,215.
**Asked at:** commonly asked (no company-specific report found); reconciling HRIS, payroll and Finance headcount is a typical HR-analytics task (unverified as a reported question).
**What the interviewer is checking:** Correct gaps and a record-level reconciliation approach, with definitions first.
**Say this in the interview:** "The largest gap is 42 between HRIS (5,240) and payroll (5,198), about 0.8%. I would fix the definition and cut-off date first, then match the lists by employee ID."
**What the data shows:** Three sources, none equal.
**Working:**
1. HRIS vs payroll: 5,240 - 5,198 = 42.
2. HRIS vs Finance: 5,240 - 5,215 = 25.
3. Finance vs payroll: 5,215 - 5,198 = 17.
4. Largest gap 42 = 0.81% of payroll (0.80% of HRIS).
**Result:** Largest gap is 42 employees (HRIS vs payroll), about 0.8% (rounded).
**Caveats / what else I would check:** Different definitions (contractors, interns, notice period, long leave, new joiners not yet on payroll, exits not yet removed from HRIS), different cut-off dates, and whether Finance counts positions or paid people.
**Next step / recommendation:** Agree the definition and date; extract the three ID lists; find IDs in HRIS but not in payroll and the reverse; categorise each difference (timing, definition, error); prepare a bridge from 5,240 to 5,198 and send the genuine errors to the owners.
**Likely follow-ups:** 1) *Which source is correct?* Depends on purpose: HRIS for people records, payroll for paid people, Finance for cost; agree one primary source. 2) *Is 0.8% a problem?* Depends on the tolerance agreed.
**Common mistakes / traps:** Comparing counts without a common date; picking a source without a rule; reporting the gap with no breakdown.

### Q19 ⭐⭐⭐ 🔴 HRIS and payroll disagree on the employment status of about 3% of employees. How do you decide on a source of truth and put a lasting fix in place?
**Asked at:** commonly asked (no company-specific report found); source-of-truth decisions appear in reconciliation prompts and HRIS data-integrity articles (unverified).
**What the interviewer is checking:** Whether you move from firefighting to ownership, rules and automation, with people involved.
**Say this in the interview:** "I would not choose a system by feeling. I would find out which team owns each fact, why they differ, then define one owner per field and automate a regular check."
**First, clarify / contain:** Do not overwrite either system. Confirm the definition of "status" in both, and the cut-off date. Pause any report that depends on status if the risk is high (for example, a payroll run).
**What I would check, in order:**
1. Pull both lists and match by employee ID; size the 3% (for example, 3% of 5,240 is about 157 people, an exercise figure).
2. Categorise each mismatch: timing lag, status-code mapping differences, manual updates in one system, ID mismatch, genuine error.
3. Sample 20 cases and trace with the HR operations and payroll teams.
4. Find the process break: who updates what, when (exits, leave, rehires).
**If I find...:** Mostly timing means set a sync schedule; code mapping means build a mapping table; manual edits in one system mean restrict edits and make HRIS the entry point; genuine errors mean correct at source with the owner's approval.
**What I would tell the stakeholder:** "About 3% of statuses differ. Most are timing and coding differences; [n] need correction. I propose HRIS owns employment status and dates, payroll owns pay fields, with a weekly mismatch report to both teams."
**Prevent it next time:** A written data owner per field, a status mapping table, a weekly automated mismatch report with an agreed tolerance, and a rule that status changes enter HRIS first.
**Likely follow-ups:** 1) *Why not just trust payroll?* Payroll is precise for paid people but may lag on non-pay status changes. 2) *Who decides?* A data owner or governance group (HR head, payroll head, IT).
**Common mistakes / traps:** Fixing rows without finding the cause; picking a system on seniority; no owner or schedule for the fix.

### Q20 ⭐⭐ 🟢 What is the difference between data cleaning, data validation and data verification?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Clear, non-overlapping definitions.
**Say this in the interview:** "Validation checks that data follows the rules when it comes in. Verification checks that it matches reality or the source. Cleaning is fixing the problems those checks find."
**Explain simply:**
- **Data validation:** rules on format and range. Is a date a real date? Is age between 18 and 65? Is the department on the allowed list?
- **Data verification:** is it true or does it match the source? Does the salary equal the signed offer letter? Does the headcount equal the payroll register?
- **Data cleaning:** fixing or removing what is wrong: trimming spaces, standardising spellings, removing duplicates, fixing types.
- Order in practice: validate and verify to find problems, clean to fix them, then re-check.
**Mini-example:** An employee age of 250 fails validation; an age of 32 that should be 23 passes validation but fails verification against the date of birth.
**Practice step:** Write one validation rule, one verification check and one cleaning step for any HR column.
**Likely follow-ups:** 1) *Can data pass validation and be wrong?* Yes; a valid-looking wrong value passes. 2) *Who verifies?* Often the owner of the source record.
**Common mistakes / traps:** Treating the three as the same thing; thinking validation proves truth.

### Q21 ⭐⭐ 🟢 City names in a customer table appear as 'Bengaluru', 'Bangalore', 'BLR' and 'bengaluru '. How do you standardise them?
**Asked at:** commonly asked (no company-specific report found); standardisation is named in a Meesho data-quality prompt in a vendor guide (unverified).
**What the interviewer is checking:** A repeatable cleaning method, not typing fixes by hand.
**Say this in the interview:** "I trim spaces and fix the case, then use a mapping table from each variant to one official city name, and apply it consistently."
**Explain simply:**
1. Look at all distinct values with counts first (a pivot or `SELECT DISTINCT city, COUNT(*)`), so I see every variant.
2. Remove extra spaces and unify case: `TRIM`, then `LOWER`. This fixes 'bengaluru ' directly.
3. Build a small mapping table: bangalore, blr, bengaluru all map to "Bengaluru".
4. Join or look up against the mapping table; keep the original column next to the cleaned one.
5. Check for unmapped values left over and add them to the table (or use a standard city list from a master).
**Mini-example:** After trimming and lower-casing, four spellings become three distinct values (bengaluru, bangalore, blr), and the mapping table collapses them to one.
**Practice step:** Make a 10-row table of messy city names and build the mapping.
**Likely follow-ups:** 1) *What about typos?* Fuzzy matching can suggest candidates, but I review them. 2) *How to prevent it?* A dropdown list at data entry.
**Common mistakes / traps:** Overwriting the original column; fixing only the spellings you noticed; not rerunning the count afterwards.

### Q22 ⭐⭐ 🟢 What is a primary key, and why does its uniqueness matter for data quality?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know a key identifies one row and why duplicates in it cause wrong numbers.
**Say this in the interview:** "A primary key is a column, such as employee ID, that identifies each row uniquely and is never blank. If it repeats, joins multiply rows and counts become wrong."
**Explain simply:**
- A **primary key** uniquely identifies a row in a table. Employee ID in an employee master is a typical example. It must be unique and not blank.
- If it is not unique, a join to another table repeats rows, so headcount or revenue is overstated.
- If it is blank, the record cannot be matched to other data.
- Check: compare `COUNT(*)` with `COUNT(DISTINCT employee_id)`; they should be equal, and no blanks.
**Mini-example:** If 1,000 rows have only 970 distinct IDs, 30 rows are repeats of an existing ID, so joins to payroll will produce extra rows.
**Practice step:** Run the count check on any table you use at work.
**Likely follow-ups:** 1) *Can a key be two columns?* Yes, a composite key, such as employee ID plus effective date in a history table. 2) *What is a foreign key?* A column that points to another table's primary key.
**Common mistakes / traps:** Assuming a column is unique without testing; using names as keys; forgetting that history tables need a composite key.

### Q23 ⭐⭐ 🟢 In a store sales file, one store shows 0 for a month because it did not report. Four stores show 120, 0, 100 and 80 (in thousands). What is the average with and without the unreported store, and which would you present?
Inline data: store sales 120, 0 (not reported), 100, 80 (in thousands).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you distinguish a true zero from a missing value.
**Say this in the interview:** "Including the 0 gives 75 thousand; excluding it gives 100 thousand. A non-reporting store is missing data, not zero sales, so I present 100 and state that one store is missing."
**What the data shows:** One of four stores shows 0 only because it did not report.
**Working:**
1. With the 0: (120 + 0 + 100 + 80) / 4 = 300 / 4 = 75.
2. Without it: (120 + 100 + 80) / 3 = 300 / 3 = 100.
**Result:** Average 75 thousand with the 0; 100 thousand per reporting store without it.
**Caveats / what else I would check:** Confirm with the store or regional manager that the store did not report (versus sold nothing); 100 describes reporting stores only; a total for the chain is understated until the store reports; compare the store's usual sales to estimate a range if a total is needed.
**Next step / recommendation:** Present 100 thousand per reporting store (3 of 4 stores), with a note and the expected update date. Show total as "at least 300 thousand".
**Likely follow-ups:** 1) *What if the store really sold zero?* Then 0 is valid and the average is 75. 2) *Estimate the missing store?* Possibly from past months, labelled as an estimate.
**Common mistakes / traps:** Averaging in a false zero; dropping the store silently; presenting a chain total as complete.

### Q24 ⭐⭐ 🟢 An order placed at 20:00 UTC on 31 March appears in the March report, but the business works in IST. On which date and month did the order happen in IST, and how do you prevent this issue in reports?
Inline data: order timestamp 2025-03-31 20:00 UTC; IST is UTC+5:30.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Time zone conversion and awareness that it moves orders across month ends.
**Say this in the interview:** "20:00 UTC plus 5 hours 30 minutes is 01:30 on 1 April IST, so the order belongs to April, not March."
**What the data shows:** The system stores UTC; the business reports in IST.
**Working:**
1. 20:00 + 5:30 = 25:30, which is 01:30 the next day.
2. Next day after 31 March is 1 April.
**Result:** 1 April 2025, 01:30 IST, so April (not March).
**Caveats / what else I would check:** Confirm the stored time zone (UTC vs server local time); daylight saving does not apply to IST, but may apply to other regions in the data; check that the month-end total in the report really uses UTC dates; late-evening orders near midnight are the ones affected.
**Next step / recommendation:** Convert timestamps to IST in the data model before taking the date (for example, add a column `order_time_ist`), group by that, and write "all dates are IST" on the report. Reconcile month-end totals with Finance after conversion.
**Likely follow-ups:** 1) *How many orders move?* Those placed from 18:30 to 23:59 UTC on the last day of a month. 2) *Where to fix it?* Once, in the data model, not in each report.
**Common mistakes / traps:** Taking the date from a UTC timestamp; converting in the wrong direction (subtracting 5:30); fixing it in one report only.

### Q25 ⭐⭐ 🟢 Employee IDs such as 00453 become 453 after someone opens the file in Excel, and a lookup to the HR master now fails. What happened and how do you fix it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know IDs are labels, not numbers, and can repair and prevent the problem.
**Say this in the interview:** "Excel guessed the column was a number and dropped the leading zeros, so 00453 no longer equals 453 in the master. I would restore the IDs as text with a fixed width, rerun the lookup, and stop it happening again."

**First, clarify / contain:** Ask how many IDs have a fixed length (is it always 5 digits?) and whether the original CSV still exists. Do not overwrite the damaged file; keep a copy.
**What I would check, in order:**
1. Compare ID lengths in the master (`LEN`) to confirm they are all the same width.
2. Count how many file IDs are shorter than that width (these are the damaged ones).
3. Check the original export: if it still has 00453, re-import it with the column set to Text (Data > From Text/CSV, set type to Text), not a plain double-click open.
4. Check for IDs that are legitimately different (e.g. 453 and 00453 both existing in the master).
**If I find...:** Fixed width everywhere: rebuild with `=TEXT(A2,"00000")` and match again. Original available: re-import, no repair needed. Mixed widths or both 453 and 00453 in the master: do not pad blindly; ask the HRIS owner for the rule.
**What I would tell the stakeholder:** "The lookup failed because Excel stripped the leading zeros from employee IDs. I have restored them from the original export and the match rate is back to X%. Nothing in the HR master was changed. I will share the file only as CSV with the ID column set to text."
**Prevent it next time:** Treat IDs as text in every tool; share through a database, a CSV with a documented schema, or Power Query rather than manual opens.
**Likely follow-ups:** 1) Why not just convert the master to numbers? Leading zeros may be meaningful and other systems expect them. 2) How do you test the fix? Count unmatched IDs before and after.
**Common mistakes / traps:** Padding to the wrong width; formatting the cell as "00000" (display only, the stored value is still a number); saving the damaged file over the original.

### Q26 ⭐⭐ 🟢 A survey export shows 'Male', 'male ', 'M' and 'MALE' in the gender column. How do you clean it and prevent the issue recurring?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you standardise categories with a mapping table instead of ad-hoc edits.
**Say this in the interview:** "I would list every distinct value, trim spaces and fix case, then map them to a small approved list through a mapping table. To stop it recurring, the survey should use a dropdown."

**First, clarify / contain:** Ask which values the organisation allows (for example Male, Female, Other, Prefer not to say). Do not delete rows or guess for blank or unclear values.
**What I would check, in order:**
1. List distinct values with counts (`SELECT gender, COUNT(*) ... GROUP BY gender`, or a pivot table).
2. Strip hidden spaces: `TRIM` in Excel, `TRIM` or `LOWER` in SQL.
3. Make case uniform (`UPPER`), so 'male ' and 'MALE' become one value.
4. Map short codes ('M') to the approved label using a lookup table kept with the analysis.
5. Re-count: total rows before and after must be equal, and no value outside the approved list should remain.
**If I find...:** Values I cannot map ('Other', blank, odd text) go to "Unknown" or stay as they are, flagged for the data owner. Never force a guess.
**What I would tell the stakeholder:** "The column had four spellings of the same two or three answers. I standardised them with a documented mapping; row counts are unchanged and the unmapped values (N rows) are listed for you."
**Prevent it next time:** Use a dropdown or coded options in the survey form; add a validation check that flags any value outside the list.
**Likely follow-ups:** 1) Why a mapping table, not find-and-replace? It is repeatable and auditable. 2) Is gender sensitive data? Yes; report only in groups large enough to avoid identifying people, and follow your company policy (confirm with HR/legal).
**Common mistakes / traps:** Forgetting trailing spaces (the visible text looks identical); overwriting the raw column instead of adding a clean column.

### Q27 ⭐⭐ 🟡 A survey of 100 employees has 20 blank answers on a 1-100 satisfaction question. The mean of the 80 answers is 60. What is the mean after mean imputation, what happens to the spread, and is it a good idea?
Inline data: responses 100; blank 20; mean of answered 60.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know mean imputation keeps the mean but shrinks the spread, and hides bias.
**Say this in the interview:** "The mean stays at 60, but the spread shrinks, so it looks more certain than it is. I would not use it blindly; I would first ask why the answers are blank."

**What the data shows:** 80 people answered and 20 did not (20% missing).
**Working:**
1. Sum of answers = 80 x 60 = 4,800.
2. Fill 20 blanks with 60: add 20 x 60 = 1,200, so the total is 6,000.
3. New mean = 6,000 / 100 = 60.
4. The 20 new values sit exactly on the mean, so they add zero to the sum of squared distances, but the count grows. The sample variance falls by a factor of 79/99, so the standard deviation falls by a factor of about 0.893 (about 10.7% lower). Example: if the SD was 15, it becomes about 13.4 (illustrative).
**Result:** Mean after imputation = 60 (unchanged); spread = about 11% smaller; the 20 invented values look like real data.
**Caveats / what else I would check:** If the blanks are not random (unhappy people skip the question), the true mean is probably lower than 60 and imputation hides that. Check blank rates by department and tenure. Confidence intervals and tests become falsely tight.
**Next step / recommendation:** Report the mean of the 80 with "20 did not answer"; do a sensitivity check (what if the 20 averaged 40 or 80? Overall mean would be 56 or 64). Use group-based or model-based imputation only if blanks look random, and label it.
**Likely follow-ups:** 1) Better option? Report the missing rate and analyse complete cases, or impute within groups. 2) When is mean imputation acceptable? Very few blanks, a quick view, clearly labelled.
**Common mistakes / traps:** Saying "the mean is unchanged so it is fine"; forgetting that spread and correlations are distorted.

### Q28 ⭐⭐ 🟡 Missing values by department are: Sales 10 of 200, Operations 60 of 300, HR 5 of 100. What is the overall missing rate, which department needs attention, and why might the pattern matter?
Inline data: Sales 10/200; Operations 60/300; HR 5/100 missing.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you compute rates per group, not only counts, and spot non-random missingness.
**Say this in the interview:** "Overall 12.5% is missing, but it is not spread evenly: Operations is at 20% against 5% elsewhere. I would find out why before filling anything."

**What the data shows:** Operations has both the most missing values and the highest rate.
**Working:**
1. Total missing = 10 + 60 + 5 = 75; total records = 200 + 300 + 100 = 600.
2. Overall rate = 75 / 600 = 12.5%.
3. Sales = 10/200 = 5%; Operations = 60/300 = 20%; HR = 5/100 = 5%.
**Result:** Overall 12.5%; Operations 20% (4 times the others); Sales and HR 5% each.
**Caveats / what else I would check:** Operations alone has 60 of the 75 gaps (80%). A pattern like that points to a cause: a different form, shift workers without system access, or a field that does not apply to them. If it is not random, simple deletion or filling will bias results towards Sales and HR. Check which field is missing and over what dates.
**Next step / recommendation:** Talk to the Operations data owner, fix collection at source, and report results with the missing rate by department; do not average over the gap silently.
**Likely follow-ups:** 1) Is 12.5% too high? It depends on the field and use; there is no universal cut-off. 2) Delete or impute? Only after knowing the reason.
**Common mistakes / traps:** Comparing counts without denominators (60 vs 10); averaging the three department rates ((5% + 20% + 5%) / 3 = 10% is wrong, since sizes differ; the true overall rate is 12.5%).

### Q29 ⭐⭐ 🟡 A feedback survey received 800 submissions from 765 unique email addresses; 1,000 people were invited. The team reported an 80% response rate. What is the corrected rate, and how would you present it?
Inline data: submissions 800; unique emails 765; invited 1,000.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you count people, not submissions, in a response rate.
**Say this in the interview:** "The honest figure is 765 of 1,000, which is 76.5%. The 80% counted people who submitted twice."

**What the data shows:** 35 submissions came from people who had already answered.
**Working:**
1. Duplicate submissions = 800 - 765 = 35.
2. Reported rate = 800 / 1,000 = 80%.
3. Corrected rate = 765 / 1,000 = 76.5%.
**Result:** 76.5% response rate; the reported 80% was overstated by 3.5 percentage points (about 4.6% in relative terms).
**Caveats / what else I would check:** I assume every unique email belongs to one invited person; check that none are outside the invite list or test addresses, and that one person did not use two emails. Decide which duplicate to keep (usually the latest complete one), and check whether the duplicates differ in answers.
**Next step / recommendation:** Present: "765 of 1,000 invited employees responded (76.5%); 35 repeat submissions were removed." Add the response rate by department to show who is under-represented.
**Likely follow-ups:** 1) Is the 3.5-point gap important? It is small, but it matters for trust and for reports compared over time. 2) Anonymous survey? Then you cannot deduplicate by email; use a one-response-per-link setting.
**Common mistakes / traps:** Counting submissions; calling a 3.5 point change "3.5%"; silently changing a figure already shared (flag the correction).

### Q30 ⭐⭐ 🟡 Payment gateway retries create duplicate transactions with different transaction IDs but the same customer, amount and time. How do you detect and remove them without deleting genuine repeat purchases?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you define a duplicate carefully and protect real repeat orders.
**Say this in the interview:** "I would define a duplicate as the same customer, amount and item within a short window, flag instead of delete, and check the flagged rows against gateway status and order numbers."

**First, clarify / contain:** Ask what a retry looks like (seconds apart? same order number? one failed and one success?). Do not delete anything yet; add a flag column.
**What I would check, in order:**
1. Group by customer, amount and (if present) order or cart ID; count groups with more than one row.
2. Measure the time gap between rows in each group (`LAG` window function); retries are typically seconds apart, genuine repeats minutes or days apart.
3. Check gateway status: a failed attempt followed by a success is not a duplicate charge; two successes are.
4. Sample 20 flagged pairs and check them by hand with the payments team.
**If I find...:** Same order ID or gap under the agreed window (say 60 seconds, confirm with the owner): mark as duplicate, keep the earliest successful row. Same amount but a different cart or a long gap: genuine, keep both.
**What I would tell the stakeholder:** "I found N likely retry duplicates worth Rs X. They are flagged, not deleted. Revenue figures exclude them; if customers were actually charged twice, finance needs to refund."
**Prevent it next time:** Idempotency keys at the gateway, and a daily duplicate check by customer, amount and time.
**Likely follow-ups:** 1) Why not delete by customer and amount alone? You would remove a real repeat purchase. 2) Where do you fix it? At the source or in a clean staging layer, with the raw data kept.
**Common mistakes / traps:** Using a window that is too wide; deleting rows permanently; ignoring whether the customer was really charged twice.

### Q31 ⭐⭐ 🟡 A revenue column mixes INR and USD values with no currency field. How do you detect and handle it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you detect unit mixing from patterns and refuse to guess unconfirmed.
**Say this in the interview:** "I would look for a clear split in the values by country, product and date, confirm the rule with the owner, and add a currency column instead of overwriting."

**First, clarify / contain:** Ask the source team which systems feed the file and which countries or entities bill in USD. Do not convert anything before the rule is confirmed.
**What I would check, in order:**
1. Plot or bucket the values: a cluster of small values beside a cluster of large ones suggests two currencies (a USD price is often about 80 times smaller; the rate is an assumption to confirm).
2. Compare the same product's price across rows.
3. Cross-tab values against country, entity or customer type.
4. Check against a control total from finance.
**If I find...:** A clear rule (for example, non-India entities bill in USD): add a currency column, convert with a dated exchange rate from finance. No reliable rule: report the totals separately or exclude the unclear rows and flag them.
**What I would tell the stakeholder:** "The revenue column mixes currencies, so the total is not meaningful. Based on entity, I separated INR and USD rows (N rows unclear). Please confirm the rule and the exchange rate to use."
**Prevent it next time:** Make currency a mandatory field and store the original amount, currency, rate and converted amount.
**Likely follow-ups:** 1) Which exchange rate? Ask finance: transaction date, month average or reporting rate. 2) Why not use a value threshold? It misclassifies cheap INR or costly USD items.
**Common mistakes / traps:** Guessing from magnitude alone; summing mixed currencies; overwriting the original value.

### Q32 ⭐⭐ 🟡 A tenure column holds values 2, 3, 36, 48 and 5, and you suspect some are in months and some in years. How do you investigate and what do you assume?
Inline data: tenure values 2, 3, 36, 48, 5.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you test assumptions against a second field (joining date) before converting.
**Say this in the interview:** "Values like 36 and 48 are unlikely to be years, so they look like months, but I would verify against joining dates before converting anything."

**First, clarify / contain:** Ask the owner which system produced each row. Do not convert yet.
**What I would check, in order:**
1. Compute tenure independently: (report date minus joining date) in years and months.
2. Compare to the column row by row; see which unit matches.
3. Look at the distribution: are there values in a gap (e.g. 6 to 24) that fit neither?
4. Check by source system or file: units are often consistent within one source.
**If I find...:** Dates confirm 36 and 48 are months (3 and 4 years): convert with a "tenure_unit" flag. Values 2, 3, 5 are ambiguous: 3 could be 3 years or 3 months; use the date test to settle each. No dates available: assume values above about 40 are months only as a documented, temporary assumption, and say so.
**What I would tell the stakeholder:** "Tenure is in mixed units. Using joining dates I confirmed N rows, and M rows are still unresolved. Results exclude the unresolved ones; please confirm the unit with the HRIS team."
**Prevent it next time:** Name columns with units (tenure_months) and add a range check.
**Likely follow-ups:** 1) Is a threshold rule safe? Only as a temporary assumption; 3 months and 3 years overlap. 2) Compare 2 months vs 2 years? Different in kind: a new joiner and an experienced employee.
**Common mistakes / traps:** Converting by guess; computing averages across mixed units.

### Q33 ⭐⭐ 🟡 Your production orders table contains test records such as 'Test User' and orders of Rs 1. How do you find and exclude them, and how do you check they do not distort metrics?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you exclude test data by explicit rules and measure the effect.
**Say this in the interview:** "I would find test records by names, emails, tiny values and internal accounts, agree the rules with the owner, flag them, and show the metric with and without them."

**First, clarify / contain:** Ask engineering whether there is a test-account list or flag. Do not delete rows.
**What I would check, in order:**
1. Search names and emails for patterns: test, dummy, demo, internal company domain.
2. List the smallest order values and count Rs 1 orders.
3. Check unusual times, repeated IDs, and orders without a shipment or payment.
4. Review a sample of matches by hand to avoid dropping real customers (a person named Tester is possible).
**If I find...:** Clear rule matches: add an `is_test` flag and filter it in reports. Ambiguous rows: keep and list them for the owner.
**What I would tell the stakeholder:** "I found N test orders (X% of orders, Rs Y of revenue). Excluding them changes revenue by Z% and average order value from A to B. The rule list is attached."
**Prevent it next time:** Keep a test account flag in the source or a separate test environment.
**Likely follow-ups:** 1) Why not delete? Audit trail and reversibility. 2) What if a real Rs 1 promo order exists? Check the promo code before excluding.
**Common mistakes / traps:** Filtering by value alone; not measuring the impact; permanent deletion.

### Q34 ⭐⭐ 🟡 Apply the rules 'joining date is not in the future (today is 12 Nov 2026) and exit date is strictly after joining date' to these four records. How many fail, and what do you do with them?
Inline data: E1 joined 2022-03-01, exit 2024-05-10; E2 joined 2023-06-15, exit 2023-01-20; E3 joined 2031-01-01, no exit; E4 joined 2021-08-01, exit 2021-08-01.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you apply rules literally, including the "strictly after" edge case.
**Say this in the interview:** "Three of the four fail: E2, E3 and E4. I would flag them with a reason code and send them to the HR data owner, not fix them myself."

**What the data shows:** Only E1 is clean.
**Working:**
1. E1: joined 2022-03-01 is before today; exit 2024-05-10 is after joining. Pass.
2. E2: exit 2023-01-20 is before joining 2023-06-15. Fail (exit before joining).
3. E3: joined 2031-01-01 is after 12 Nov 2026. Fail (future joining date); no exit date to test.
4. E4: exit equals joining date, not strictly after. Fail (zero-length stay; may be a same-day exit or a typo).
**Result:** 3 of 4 records fail (75%): E2, E3, E4.
**Caveats / what else I would check:** E2 may be swapped dates; E3 may be a wrong year (2021?) or a genuine future joiner, which belongs in a "pipeline" table, not active headcount; E4 may be a real same-day offer withdrawal. The rule on E4 is a business choice: confirm whether same-day exit is allowed.
**Next step / recommendation:** Add a `dq_flag` and reason, exclude failed rows from tenure and attrition calculations (state the count), send the list to HRIS owners for correction at source, and track the failure rate weekly.
**Likely follow-ups:** 1) Should you correct E2 by swapping? Only after confirmation. 2) Can a joining date be in the future? Yes for accepted offers, if the table is meant for them.
**Common mistakes / traps:** Treating E4 as a pass (the rule says strictly after); silently deleting rows.

### Q35 ⭐⭐ 🟡 A payroll file shows 18 employees paid twice in March at Rs 52,000 each. What is the overpayment, how did it probably happen, and who do you notify?
Inline data: employees paid twice 18; salary per payment Rs 52,000.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you size the problem, find causes calmly and escalate to the right owners.
**Say this in the interview:** "The overpayment is 18 x Rs 52,000 = Rs 9,36,000. I would confirm it is a true double payment, tell payroll and finance quickly, and not touch the data myself."

**First, clarify / contain:** Confirm the second payments are real bank transfers, not just duplicate rows in the file. Do not reverse or edit anything; recovery is payroll's decision.
**What I would check, in order:**
1. Count and sum: 18 employees x Rs 52,000 = Rs 9,36,000 (if the Rs 52,000 is gross, the net transferred figure may differ).
2. Compare payment dates, batch IDs and bank references for the two payments.
3. Check whether all 18 share a batch, a team, a joining date or a recent change (bank detail update, rerun).
4. Reconcile the file total with the bank statement.
**If I find...:** Same batch run twice or a payroll re-run: a process fault. A repeated file upload or duplicate rows only: a data issue, with no money lost. Different batches: look for manual adjustments.
**What I would tell the stakeholder:** "18 employees appear to have been paid twice for March, a total of Rs 9,36,000. Cause not confirmed yet; likely a rerun or a duplicate upload. I am sharing the list with Payroll and Finance today and will update by [time]."
**Prevent it next time:** Duplicate check (employee, month, amount) before release, plus batch sign-off.
**Likely follow-ups:** 1) Who do you notify? Payroll head, Finance, HR lead (and the employees' recovery is handled by payroll and HR per policy). 2) Share names widely? No, keep it to those who need it.
**Common mistakes / traps:** Emailing the list broadly; assuming a cause; stating "recovered" before it is.

### Q36 ⭐⭐ 🟡 Of 1,000 hires in your ATS, 912 match an HRIS record on email. What is the match rate, what might explain the unmatched 88, and what do you do before building a time-to-hire report?
Inline data: hires 1,000; matched 912.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you investigate a join gap before reporting on it.
**Say this in the interview:** "The match rate is 91.2%, and 88 hires have no HRIS record. I would find out why before building time-to-hire, because those 88 could bias it."

**What the data shows:** 912 of 1,000 matched; 88 (8.8%) did not.
**Working:**
1. Match rate = 912 / 1,000 = 91.2%.
2. Unmatched = 1,000 - 912 = 88 (8.8%).
**Result:** 91.2% matched; 88 unmatched.
**Caveats / what else I would check:** Likely causes: personal vs company email, typos or case and spaces, name changes, hires who never joined, not yet loaded into HRIS, or rehires. Compare the unmatched on other keys (name plus date of birth, phone). Are the 88 concentrated in one month, source or location? If they are the slow (or fast) hires, time-to-hire would be biased.
**Next step / recommendation:** Clean the emails (trim, lower case), rematch on a second key, sample 20 unmatched by hand, then report the final match rate along with time-to-hire. If unmatched hires cannot be fixed, show results for matched hires and say that 8.8% are excluded.
**Likely follow-ups:** 1) Is 91.2% good enough? Depends on the decision; check bias, not just the rate. 2) Which key is best? An immutable employee or candidate ID.
**Common mistakes / traps:** Dropping the 88 silently; fuzzy matching without checking the precision.

### Q37 ⭐⭐ 🟡 Five employee salaries (in thousands) are 30, 40, 50, 60 and 70, but the file has the 70 row twice. What are the wrong and correct average salaries, and how does the error affect pay-band reporting?
Inline data: file salaries 30, 40, 50, 60, 70, 70 (in thousands).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can quantify how one duplicate row shifts mean, median and headcount.
**Say this in the interview:** "The wrong average is 53.3 thousand against the correct 50, about 6.7% too high, and the duplicate also changes headcount and the top pay band."

**What the data shows:** One person was counted twice, which pushes everything upward.
**Working:**
1. Wrong: sum = 30+40+50+60+70+70 = 320; mean = 320 / 6 = 53.33.
2. Correct: sum = 250; mean = 250 / 5 = 50.
3. Difference = 3.33, which is 6.7% above the correct mean.
4. Median: wrong = (50 + 60) / 2 = 55; correct = 50.
**Result:** Wrong mean 53.3 thousand vs correct 50 thousand (+6.7%); wrong median 55 vs 50 (+10%); headcount 6 vs 5 (+20%).
**Caveats / what else I would check:** In pay bands, the top band gets 2 people instead of 1, and band averages, compa-ratios and pay-gap figures move; payroll cost is overstated. Check whether the duplicate is a true duplicate (same employee ID) or two people with the same pay; use the ID, not the salary.
**Next step / recommendation:** Dedupe on employee ID, rerun band reports, and add a rule: one row per employee ID per period.
**Likely follow-ups:** 1) Why does the median move so much? With few rows, one extra value shifts the middle. 2) How do you catch it? `COUNT(*)` vs `COUNT(DISTINCT employee_id)`.
**Common mistakes / traps:** Deduplicating by salary value; ignoring the headcount effect.

### Q38 ⭐⭐ 🟡 A recruiter says there were 600 applications and 45 hires, so conversion is 7.5%. You find 450 unique candidates because many applied to several roles. What is the per-candidate conversion, and which would you report?
Inline data: applications 600; unique candidates 450; hires 45.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you match the denominator to the question being asked.
**Say this in the interview:** "Both are correct but answer different questions: 7.5% per application and 10% per candidate. I would report both, labelled clearly."

**What the data shows:** On average, a candidate made 600 / 450 = 1.33 applications.
**Working:**
1. Per application = 45 / 600 = 7.5%.
2. Per candidate = 45 / 450 = 10%.
3. Applications per candidate = 600 / 450 = 1.33.
**Result:** 7.5% per application; 10% per unique candidate (2.5 percentage points higher).
**Caveats / what else I would check:** Assume each hire is one candidate hired once; hires can come from applications made in earlier periods (a timing mismatch). Per-role funnels need per-application counts; "how good is our candidate pool" needs per-candidate. Define "unique" by candidate ID, not name.
**Next step / recommendation:** For a funnel by role, report per application; for overall hiring efficiency, report per candidate. State the definition under every chart.
**Likely follow-ups:** 1) Which is correct? Neither is wrong; the label matters. 2) How do you dedupe candidates? A stable candidate ID, with email and phone as backups.
**Common mistakes / traps:** Mixing both numbers in one trend; calling the gap "2.5%" instead of 2.5 percentage points.

### Q39 ⭐⭐ 🟡 A sales report has five mandatory fields in 1,000 records. Null counts are 20, 150, 0, 30 and 100. What is the cell-level completeness, and why is it not the same as the share of complete records?
Inline data: records 1,000; mandatory fields 5; nulls per field 20, 150, 0, 30, 100.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can distinguish cell-level from record-level completeness.
**Say this in the interview:** "Cell-level completeness is 94%, but the share of fully complete records is lower, somewhere between 70% and 85%, depending on how the gaps overlap."

**What the data shows:** The worst field is the second one, with 15% null.
**Working:**
1. Total cells = 1,000 x 5 = 5,000.
2. Total nulls = 20+150+0+30+100 = 300.
3. Cell-level completeness = (5,000 - 300) / 5,000 = 94%.
4. Records with at least one null: at least 150 (if all nulls sit in the same rows as the worst field), at most 300 (if no row has two nulls).
5. So complete records = between 700 and 850 of 1,000.
**Result:** Cell-level completeness 94%; complete records 70% to 85% (exact value needs a row-level count).
**Caveats / what else I would check:** A single record with any missing mandatory field may be unusable, so the record-level figure is the one that matters for analysis that needs all five. Count it exactly: `WHERE f1 IS NOT NULL AND ... f5 IS NOT NULL`.
**Next step / recommendation:** Report both figures plus nulls per field; focus on field two (15%).
**Likely follow-ups:** 1) Why is it lower? Gaps spread across rows make more rows incomplete. 2) Which to track? Both; use record-level for decisions.
**Common mistakes / traps:** Saying "94% of records are complete"; averaging field percentages when field sizes differ.

### Q40 ⭐⭐ 🟡 How do nulls in join keys affect join results and row counts, and what do you do about them?
**Asked at:** commonly asked (no company-specific report found); the sources note Swiggy-style prompts on null handling in joins (snippet-level, unverified).
**What the interviewer is checking:** Whether you know that NULL never equals NULL in a join.
**Say this in the interview:** "A null key matches nothing, so inner joins silently drop those rows and left joins keep them with empty columns. I would count nulls in the key before every join."

**First, clarify / contain:** Ask what a null key means (unknown, not applicable, not yet assigned). Do not replace nulls with a dummy value before knowing.
**What I would check, in order:**
1. Count null keys in both tables (`COUNT(*) - COUNT(key)`).
2. Compare row counts before and after the join.
3. Check the unmatched rows with an anti-join (`LEFT JOIN ... WHERE right.key IS NULL`).
4. Check duplicates in the keys; they cause the opposite problem (extra rows).
**If I find...:** Nulls from missing data: fix at source, or use a second key. Nulls that are legitimate (order with no customer): use a left join and report them as "Unassigned". Placeholders like 0 or -1 on both sides would falsely match each other; clean them.
**What I would tell the stakeholder:** "N rows (X%) have no key, so they are not in the matched report. I am showing them as a separate line, and the totals reconcile."
**Prevent it next time:** Not-null constraints and a null-rate check on keys at load.
**Likely follow-ups:** 1) Does NULL = NULL in SQL? No, it is unknown; use `IS NULL`. 2) Inner vs left join? Inner drops the unmatched, left keeps them.
**Common mistakes / traps:** Not noticing the row count fall after an inner join; filling nulls with 0.

### Q41 ⭐⭐ 🟡 You have been given a dataset with no data dictionary or owner. What do you do before you trust any column?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you profile, find the owner and reconcile before using the data.
**Say this in the interview:** "I would profile every column, find someone who knows its origin, and reconcile at least one total with a known source before using any number."

**Clarify first:** What decision is this data for, and who gave it to you? That person can often point to the owner or the source system.
**Plan:**
1. Profile: row count, data types, distinct values, null rates, min, max and top values for each column.
2. Guess meaning from names and values, and write it down as a draft dictionary marked "unconfirmed".
3. Check keys: is one column unique per row?
4. Reconcile a total (headcount, revenue) against a trusted report.
5. Find the owner (team that exports it, the system admin) and confirm the draft; record refresh time and definitions.
**Method choice and why:** Simple profiling and reconciliation first; no modelling until definitions are confirmed.
**Pitfalls:** Assuming column names are accurate (status, amount, date might each mean several things); unknown units, time zones and filters; stale data.
**Deliverable:** A one-page data dictionary with confidence per column, open questions, and a note of the checks passed. Share that before any analysis.
**Likely follow-ups:** 1) What if no owner can be found? Present results as provisional and list assumptions. 2) What is the first check? Row count and key uniqueness.
**Common mistakes / traps:** Starting the analysis straight away; trusting a column because the name sounds right.

### Q42 ⭐⭐ 🟡 What automated checks would you add to a daily data load to catch quality problems early (for example row counts, null rates, freshness)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can name practical checks and decide what happens when one fails.
**Say this in the interview:** "I would add checks on volume, freshness, nulls, duplicates, valid values and reconciliation, each with a threshold and an owner who gets alerted."

**Clarify first:** Which tables matter most, and what would break a decision or a dashboard? Start with those.
**Plan:**
1. Volume: today's row count is within a normal range of recent days (for example, plus or minus 20%, tuned from history).
2. Freshness: the latest timestamp is recent enough.
3. Nulls: key and mandatory fields stay below a set null rate.
4. Uniqueness: primary key has no duplicates.
5. Validity: values are within allowed lists and ranges (no future joining dates, no negative salaries).
6. Referential: foreign keys exist in the parent table.
7. Reconciliation: totals match the source system (headcount, revenue).
8. Schema: columns and types have not changed.
**Method choice and why:** Simple rule-based checks first (SQL tests, or tools such as dbt tests or Great Expectations, from memory, confirm what your team uses); add anomaly detection later.
**Pitfalls:** Too many alerts (people ignore them); thresholds with no owner; checks that run after the dashboard has refreshed.
**Deliverable:** A check list with thresholds, severity (block the load or just warn), owner, and a small quality dashboard of pass/fail history.
**Likely follow-ups:** 1) Block or warn? Block for keys and reconciliation; warn for small drifts. 2) Who is alerted? The data owner first.
**Common mistakes / traps:** Only checking that the job ran; fixed thresholds that ignore weekends and seasons.

### Q43 ⭐⭐ 🟡 Exit interview data exists for only 25% of employees who left. What can and can you not conclude from it for an attrition analysis?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you recognise response bias and avoid generalising to all leavers.
**Say this in the interview:** "I can describe what that 25% said, but I cannot say it represents all leavers. I would first check who gave interviews and who did not."

**Clarify first:** Which decision is it for (retention action, manager coaching)? Was the interview voluntary, and who conducted it (HR or the manager)?
**Plan:**
1. Compare the 25% who responded with all leavers on department, tenure, grade, age band, manager and reason type.
2. Check by exit type: resignations may be more likely to be interviewed than terminations or absconders.
3. Read the themes as "among those who answered".
4. Triangulate with other data: engagement survey, performance, pay, promotion, manager changes, for all leavers.
**Method choice and why:** Descriptive comparison and weighting by group only if the responders resemble the leavers within groups; do not model on 25% alone.
**Pitfalls:** Non-response bias (people leaving on bad terms may skip it, or may be too polite to be honest); small numbers in subgroups; leading questions; interviewing by the line manager.
**Deliverable:** "Exit themes (n = 25% of leavers), with representativeness checks" next to numbers from the HRIS for all leavers. Recommend improving the response rate (neutral interviewer, online option).
**Likely follow-ups:** 1) Can I call the top reason the main cause of attrition? No, only the top stated reason among respondents. 2) What if 25% responded evenly across groups? Better, but still self-reported.
**Common mistakes / traps:** Quoting percentages as if they cover all leavers; ignoring who is missing.

### Q44 ⭐⭐ 🟡 Duplicate keys in a dimension table cause fan-out in your report. How do you detect this before the join and fix it at the right level?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you test key uniqueness before joining and fix the source, not the symptom.
**Say this in the interview:** "I would check that the join key is unique in the dimension before joining, and fix the duplicates in the dimension, instead of patching it with DISTINCT in the report."

**First, clarify / contain:** Ask whether duplicates are expected (history rows with effective dates). Do not hide them with `SELECT DISTINCT`, which can mask real differences.
**What I would check, in order:**
1. `SELECT key, COUNT(*) FROM dim GROUP BY key HAVING COUNT(*) > 1`.
2. Compare the fact table row count and sum before and after the join; extra rows and an inflated total mean fan-out.
3. Look at the duplicate rows: identical (load error) or different (history, or conflicting attributes)?
4. Check how many fact rows are affected.
**If I find...:** Exact duplicates: dedupe in the dimension load. History rows: join with a date or an "is current" flag. Conflicting values: send to the data owner to choose a golden record.
**What I would tell the stakeholder:** "Revenue was overstated by X% because N products appeared twice in the product table. I fixed the table, the report now reconciles to finance, and I have added a uniqueness test."
**Prevent it next time:** A unique constraint or a daily test on dimension keys, and a row-count and total check after every join.
**Likely follow-ups:** 1) Why not DISTINCT at the end? It does not undo inflated sums. 2) What level is the right one? The dimension (one row per key) or a clearly defined history key.
**Common mistakes / traps:** Fixing in the dashboard; joining to a table at a different grain without checking.

### Q45 ⭐⭐ 🟡 The extract from an Excel report has merged cells, subtotal rows and repeated header rows in the middle. How do you turn it into analysis-ready data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can reshape a presentation file into one clean table, with checks.
**Say this in the interview:** "I would rebuild it as one header row and one record per row, remove subtotals and repeated headers by rule, fill merged cells down, and reconcile the totals to the original."

**Clarify first:** Is there a source system that can give me the raw data directly? That is better than cleaning a report.
**Plan:**
1. Keep the original untouched; work in Power Query or a script so steps are repeatable.
2. Unmerge and fill down the merged label cells (Power Query: Fill Down).
3. Remove repeated header rows (filter rows where a column equals its own header text).
4. Remove subtotal and total rows (rows labelled Total or Subtotal), after noting their values.
5. Set data types (dates, numbers, text IDs).
6. Check: sum of cleaned values equals the report's grand total; row count is as expected.
**Method choice and why:** Power Query or a short Python/R script, because it repeats when next month's file arrives; manual copy-paste does not.
**Pitfalls:** Deleting a genuine row that contains the word "Total"; subtotals left in, which double counts; numbers stored as text.
**Deliverable:** A clean table (one row per record, one column per field), a repeatable query, and a reconciliation note.
**Likely follow-ups:** 1) Why keep the subtotals' values? They are your check totals. 2) How to avoid this next time? Ask for the raw extract.
**Common mistakes / traps:** Cleaning by hand every month; not reconciling.

### Q46 ⭐⭐ 🟡 Percentages in a survey chart add up to 134%. Is this a data quality problem, and how do you check?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you consider multi-select questions before calling it an error.
**Say this in the interview:** "Not necessarily. If people could tick more than one option, percentages of respondents can exceed 100%. I would check the question type and the denominator first."

**First, clarify / contain:** Ask how the question was asked (single choice or "select all that apply") and what the chart's denominator is. Do not change the chart yet.
**What I would check, in order:**
1. Question type: multi-select gives sums above 100% legitimately.
2. Denominator: is each percentage option count / respondents (can exceed 100% in total), or option count / total selections (should equal 100%)?
3. Average selections per respondent: if the total is 134%, this is about 1.34 options each (if respondent-based).
4. Duplicates: the same person counted twice, or a table that includes a "Total" row.
5. Rounding explains only small differences (about 100% plus or minus 1), not 34 points.
**If I find...:** Multi-select with respondent base: not an error; label it "multiple answers allowed". Single-choice: it is a real fault (duplicates, wrong denominator); fix and re-chart.
**What I would tell the stakeholder:** "The percentages total 134% because respondents could choose more than one answer; each bar is the share of respondents who chose it. I have added a note to the chart."
**Prevent it next time:** Label multi-select charts, and show the base (n =) on every chart.
**Likely follow-ups:** 1) Would you show a pie chart? No; bars fit overlapping answers. 2) If the question was single-choice? Investigate duplicates and denominators.
**Common mistakes / traps:** Forcing the figures to sum to 100%; using a pie chart for multi-select.

### Q47 ⭐⭐ 🟡 Negative quantities appear in a sales table. How do you decide whether they are returns, corrections or errors?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate valid business events from errors using evidence.
**Say this in the interview:** "I would not delete or flip them. I would match each to an original sale, a reason or document type, and then classify it as a return, a correction or an error."

**First, clarify / contain:** Ask whether the system records returns as negative quantities. Do not apply `ABS()` or remove rows yet.
**What I would check, in order:**
1. Count negatives and their share of rows and of value.
2. Look for a matching positive row (same order, customer, product, earlier date): a likely return.
3. Check document type, status or reason codes (credit note, return, cancellation).
4. Check for a pair of the same quantity (+5, -5) on the same day: a correction.
5. Look for negatives with no original, unusual size, or odd products: possible errors.
**If I find...:** Matched to an earlier sale: a return, keep and net against sales. A correcting pair: keep, since it nets to zero. No match and no reason: flag as errors and query the owner.
**What I would tell the stakeholder:** "N% of rows have negative quantities. Most are returns (matched to original orders), M are corrections, K cannot be explained and are excluded pending your confirmation. Net sales are Rs X."
**Prevent it next time:** Use a transaction-type field and not the sign alone; add a check for negatives without an original.
**Likely follow-ups:** 1) Should gross or net sales be reported? Both, labelled. 2) Return rate? Returns / sales, using the same period or matched orders.
**Common mistakes / traps:** Dropping negatives (overstates sales); flipping the sign (double counts).

### Q48 ⭐⭐ 🟡 An attrition analysis was built from a file of current employees only. What is wrong with that, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found); the sources list survivorship in attrition files as a gap-fill question (judgement).
**What the interviewer is checking:** Whether you see survivorship bias: you cannot measure leavers from a list of stayers.
**Say this in the interview:** "A file of current employees contains only people who stayed, so it cannot show who left. I would rebuild it from a full employee history, including leavers, with joining and exit dates."

**First, clarify / contain:** Ask what the analysis is claiming (for example, "people with long commutes do not leave"). Pause any conclusions drawn from it.
**What I would check, in order:**
1. Does the file contain any exit date or leaver flag? (If everyone is active, attrition is zero by construction.)
2. Is a leavers or terminations table available, and can it join on employee ID?
3. Define the period (for example, the last 12 months) and the population at risk: everyone employed at any point in that period.
4. Rebuild: attrition rate = leavers in the period / average headcount in the period.
5. Compare leaver and stayer profiles (tenure, department, pay, manager) on the combined data.
**If I find...:** A leavers table exists: combine it, and rerun. It does not exist: the analysis cannot be done honestly; request the history from HRIS, and until then report only "what current staff look like".
**What I would tell the stakeholder:** "The file had only people still employed, so it could not show who leaves, and the conclusions would be biased. I have asked HRIS for the full history; the rebuilt analysis will be ready by [date]."
**Prevent it next time:** Keep snapshots or a history table with start and end dates; never overwrite records when someone leaves.
**Likely follow-ups:** 1) Example of the bias? Average tenure of current staff looks long because short-stayers have already gone. 2) What if you only have snapshots? Compare consecutive snapshots to find leavers.
**Common mistakes / traps:** Dividing leavers by the current headcount only; concluding "current employees are all happy".

### Q49 ⭐⭐ 🟡 Two teams define 'active customer' differently, so their counts never match. Is this a consistency problem or an accuracy problem, and how do you resolve it?
**Asked at:** commonly asked (no company-specific report found); reconciliation between two sources is a recurring prep-site theme (unverified).
**What the interviewer is checking:** Whether you separate "the data is wrong" (accuracy) from "the definitions differ" (consistency), and whether you resolve it with governance, not a quick fix.
**Say this in the interview:** "Mainly a consistency problem: both numbers can be correct for their own definition. I would write both definitions down, reconcile the gap, and get one agreed definition with a named owner."

**First, clarify / contain:** Ask each team for the exact rule (for example, Sales: bought in the last 12 months; Marketing: logged in in the last 90 days). Do not declare either team wrong yet, and do not publish a third number.
**What I would check, in order:**
1. Write each definition as a filter (time window, event type, which accounts are excluded such as test or internal).
2. Rebuild both counts from the same raw table so the only difference is the rule.
3. Bridge the gap: customers in A only, B only, both (a simple Venn count).
4. Spot-check 20 customers in each gap group to confirm each rule is applied as written (this is the accuracy test).
5. Check whether any records are simply wrong (duplicates, stale statuses); that part is accuracy.
**If I find...:** Both rules applied correctly and counts differ: consistency problem, so agree one definition for company reporting and keep the other under a different name (for example "engaged user"). A rule applied wrongly or duplicates: accuracy problem, so fix the data or logic.
**What I would tell the stakeholder:** "The two counts differ because we define 'active' differently, not because either is miscounted. Here is the bridge. I propose one official definition, and the second metric gets its own name. I need a decision from you by Friday."
**Prevent it next time:** Keep a metric dictionary (name, rule, owner, source table) and build all reports from one shared definition.

**Likely follow-ups:** 1) *Who decides the definition?* The business owner of the metric, guided by the decision it supports; the analyst proposes. 2) *Can both stay?* Yes, if clearly named differently.
**Common mistakes / traps:** Picking the bigger or friendlier number; calling everything "bad data"; fixing it in one dashboard only.

### Q50 ⭐⭐ 🟡 Customer IDs show as 1.23457E+11 after a CSV is opened in Excel. What has gone wrong and how do you recover the real IDs?
**Asked at:** commonly asked (no company-specific report found); Excel ID problems are a common data-cleaning theme (unverified).
**What the interviewer is checking:** Whether you know Excel treats long digit strings as numbers, and whether you protect the source file.
**Say this in the interview:** "Excel guessed the ID column was a number and displayed it in scientific notation. If I have not saved over the file, the real IDs are still in the CSV; I would re-import the column as Text."

**First, clarify / contain:** Close the file without saving. Saving a CSV from Excel can overwrite the original with the damaged values. Keep a copy of the untouched CSV.
**What I would check, in order:**
1. Click a cell: if the formula bar shows the full number (for example 123456789012), only the display is wrong. If it shows zeros at the end (for example 123457000000), digits were already lost. A CSV saved from Excel writes the shortened display value, which is how damage becomes permanent; IDs of more than about 15 digits are cut even on opening (from memory, unverified).
2. Open the original CSV in a text editor to confirm the full IDs are there.
3. Re-import with Data > From Text/CSV (or Power Query) and set the ID column type to Text.
4. Count digits: `=LEN(A2)` should be the same for every row (for example 12).
5. Check for lost leading zeros and duplicates created by rounding.
**If I find...:** Display only: widen the column or set the format to Number with 0 decimals, then re-import as Text anyway. Digits already replaced by zeros: they cannot be recovered from the damaged file (Excel keeps about 15 significant digits, from memory, unverified), so go back to the source system or the original CSV.
**What I would tell the stakeholder:** "The ID column was altered by Excel, not by our system. I am re-pulling it as text; nothing downstream should use the damaged file. Corrected file by end of day."
**Prevent it next time:** Treat IDs as text, never numbers; load CSVs through Power Query or Python with the ID column declared as a string.

**Likely follow-ups:** 1) *Why not just widen the column?* The display improves, but if the value was rounded the loss is permanent. 2) *Why store IDs as text?* You never do arithmetic on them, and text keeps leading zeros.
**Common mistakes / traps:** Double-clicking the CSV, then saving; formatting as Number and thinking it is fixed; joining on damaged IDs and getting false matches.

### Q51 ⭐⭐ 🟡 Phone numbers entered as free text appear as '98765 43210', '+91-9876543210' and '09876543210'. How do you clean and validate them?
**Asked at:** commonly asked (no company-specific report found); a Meesho data-quality prompt on deduplication, validation and standardisation was seen in a vendor guide snippet (unverified).
**What the interviewer is checking:** That you standardise first, then validate against a rule, and keep the original.
**Say this in the interview:** "I strip everything that is not a digit, remove the country code or leading zero, then check the result is a valid 10-digit number. Failures go to a review list, not the bin."

**First, clarify / contain:** Confirm the market (India only, or international), and keep the raw column untouched; I write the clean number to a new column.
**What I would check, in order:**
1. Remove spaces, hyphens, brackets: keep digits only (Excel `SUBSTITUTE`, Power Query, or a regex).
2. If 12 digits starting 91, drop the 91; if 11 digits starting 0, drop the 0.
3. Validate: exactly 10 digits and, for Indian mobiles, first digit 6 to 9 (from memory, unverified; confirm the rule with the telecom or CRM owner).
4. Store the result as text (so no leading-zero or scientific-notation damage).
5. Count rows passed, fixed and failed.
**If I find...:** The three examples all become 9876543210 and all three pass the 10-digit check. Short, long or letter-filled values: flag as invalid, send for review, do not guess digits. Same cleaned number on many customers: possible duplicates or a shared family number; investigate before merging.
**What I would tell the stakeholder:** "I standardised phone numbers to 10 digits. X% passed as-is, Y% were reformatted, Z% need someone to confirm with the customer."
**Prevent it next time:** Validate at entry (a 10-digit field with a country-code dropdown) instead of free text.

**Likely follow-ups:** 1) *Does a valid format mean a real number?* No, only that it looks right; reachability needs an OTP or call test. 2) *Landlines?* Different length rules; define the scope first.
**Common mistakes / traps:** Overwriting raw data; deleting invalid rows silently; treating phone as a number and losing leading zeros.

### Q52 ⭐⭐ 🟡 Do you fix a data error in the report or at the source, and what do you do if you cannot get the source fixed?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand that report-level patches do not scale, and whether you stay transparent when forced to patch.
**Say this in the interview:** "Fix it at the source, because otherwise every report repeats the error. If I cannot, I patch it in one documented, repeatable step in my pipeline and tell users."

**First, clarify / contain:** Find out where the error is created (data entry, a system rule, my own transformation) and who owns that place. Do not hand-edit numbers in the final report.
**What I would check, in order:**
1. Is the error in the raw source, or did my query or join cause it?
2. How many rows are affected and how much does it move the key numbers?
3. Who owns the source and how long would a fix take?
4. Who else uses this data (other reports will have the same error)?
**If I find...:** My own logic: fix it in my query. Source error, owner can fix: raise a ticket with examples and impact, and re-run after. Source error, no fix coming: add a visible correction rule in the data-prep layer (one place, commented, with a counter of rows corrected), never manual cell edits.
**What I would tell the stakeholder:** "The error comes from the source system. I have raised it with its owner. Meanwhile, my report applies a documented correction affecting 140 rows; the unadjusted figure is X, adjusted is Y." (Figures illustrative.)
**Prevent it next time:** A data-quality check that alerts on this error each load, and a log of known issues with owners and dates.

**Likely follow-ups:** 1) *Why not fix in the report?* It hides the problem and others keep using bad data. 2) *When is a report fix fine?* As a temporary, documented bridge.
**Common mistakes / traps:** Silent manual edits; fixing without telling the data owner; no record of what was changed.

### Q53 ⭐⭐ 🟡 You cannot fix a known data issue before a deadline. How do you deliver the analysis responsibly?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Judgement under time pressure: honesty about limits without refusing to deliver.
**Say this in the interview:** "I deliver on time, but I size the issue, state it up front, show how it could change the conclusion, and agree a fix date."

**First, clarify / contain:** Ask what decision the analysis supports and how precise it must be. Do not quietly ignore the issue, and do not delay without telling anyone.
**What I would check, in order:**
1. How many rows or how much value is affected (for example 4% of records)?
2. Direction of the error: does it inflate or deflate the result?
3. Run a best-case and worst-case version (include versus exclude the bad rows).
4. Does the conclusion hold in both? If yes, the issue is minor for this decision.
**If I find...:** Conclusion unchanged either way: deliver, with a short caveat. Conclusion flips: deliver a range, label the result "provisional", and recommend the decision waits or is reversible. Impact large and unfixable: escalate to the sponsor before the deadline, not after.
**What I would tell the stakeholder:** "Here is the analysis. One known issue: 4% of records have missing region. Including or excluding them moves the total by under 1% and does not change the ranking. Full fix planned by Thursday; I will send an update."
**Prevent it next time:** Raise data issues at project kickoff, add data-readiness checks a week before deadlines, and keep a known-issues list.

**Likely follow-ups:** 1) *Would you miss the deadline instead?* Only if the decision would be misleading otherwise, and I would warn early. 2) *Where do caveats go?* On the first page, not buried.
**Common mistakes / traps:** Hiding the issue; over-caveating so nothing is usable; discovering and revealing it only after the meeting.

### Q54 ⭐⭐ 🟡 Tell me about a time you found an error in data you were about to use. How did you find it, and what did you do?
**Asked at:** commonly asked (no company-specific report found); behavioural "tell me about a time" data-quality prompts appear in question banks (unverified).
**What the interviewer is checking:** Whether you validate before using data, own the problem and communicate it.
**Say this in the interview:** "I will use a real example: I noticed something that did not reconcile, traced it to its cause, fixed or flagged it, and added a check." (Say it only if true; replace the illustration below with your own.)

**Answer structure (STAR):** Situation (what data, for whom, deadline), Task (what you needed it for), Action (how you found it and what you did), Result (impact, check added).
**Illustrative HR example, replace with your real one:** "Before a monthly attrition report, I compared my HRIS headcount with payroll headcount. HRIS showed 1,204 and payroll 1,176. I filtered the 28 extra and found they were employees on long leave coded active in HRIS. I confirmed the rule with the HR operations lead, reported attrition both with and without them, and the lead updated the status codes. I then added a monthly headcount reconciliation step."
**What I would check, in order (if you describe the method):** 1) A total versus a trusted total. 2) Row counts and nulls. 3) Duplicates on the key. 4) Ranges and impossible values (negative tenure, future dates). 5) Trace a handful of rows to the source.
**If I find...:** Say what you did NOT do: you did not quietly delete rows or change numbers without telling the owner.
**What I would tell the stakeholder:** Mention exactly who you told, how fast, and the result in numbers.
**Prevent it next time:** The check you added.

**Likely follow-ups:** 1) *What if the error was yours?* Say so directly and what you changed; owning it scores well. 2) *What was the impact?* Give one figure before and after.
**Common mistakes / traps:** An invented story you cannot defend under questioning; blaming others; no result or lesson.

### Q55 ⭐⭐ 🟡 After you filter a table, 30% of rows disappear unexpectedly. How do you debug where the rows went?
**Asked at:** commonly asked (no company-specific report found); Swiggy null-handling and join prompts were seen in a vendor guide snippet (unverified).
**What the interviewer is checking:** A systematic, step-by-step way to find the cause instead of guessing.
**Say this in the interview:** "I count rows before and after each step, and find the step where the drop happens. The usual suspects are nulls, text mismatches and joins."

**First, clarify / contain:** Confirm the expected row count and what the filter was meant to keep. Do not overwrite the source table.
**What I would check, in order:**
1. Row count of the raw table (`SELECT COUNT(*)`), then after each filter or join.
2. Nulls: in SQL, `col <> 'X'` drops rows where col is NULL, so those vanish silently.
3. Text issues: extra spaces, upper versus lower case, "Delhi" versus "New Delhi" (`TRIM`, `LOWER`).
4. Data types: a date stored as text, or a number as text, so a comparison fails.
5. Joins: an INNER join drops rows with no match; use a LEFT join and count the unmatched.
6. Look at 10 of the removed rows (an anti-join or "rows not in result") and ask what they have in common.
**If I find...:** Nulls dropped: decide to include them explicitly (`OR col IS NULL`). Format mismatch: standardise, then re-filter. Unmatched join keys: fix keys or report the unmatched share. If the drop is correct (a real 30% fit the filter), confirm with the business before moving on.
**What I would tell the stakeholder:** "The filter removed 30% because those rows had blank departments. That is expected or not depending on your definition; here is the count both ways."
**Prevent it next time:** Add row-count checks after each step and print them in the log.

**Likely follow-ups:** 1) *Which cause is most common?* Nulls and failed joins. 2) *How do you prove it?* By listing the removed rows.
**Common mistakes / traps:** Assuming the filter is right; fixing by switching to a different filter without understanding; not keeping a before-count.

### Q56 ⭐⭐ 🟡 You have 45 leavers recorded in HRIS but only 38 in the exit-interview log. What is the coverage and what might explain the missing 7?
Inline data: HRIS leavers 45; exit log 38.
**Asked at:** commonly asked (no company-specific report found); reconciling two systems is a recurring prep-site theme (unverified).
**What the interviewer is checking:** Simple coverage arithmetic, then reasoned hypotheses and a plan to test them.
**Say this in the interview:** "Coverage is 38 out of 45, about 84%. I would match the two lists by employee ID to find exactly which 7 are missing and why."

**What the data shows:** The exit log covers most leavers but not all. Seven leavers have no exit record (assuming every exit-log person is also an HRIS leaver).
**Working:**
1. Coverage = 38 / 45 = 0.8444 = 84.4%.
2. Missing = 45 - 38 = 7, which is 7 / 45 = 15.6% of leavers (84.4% + 15.6% = 100%).
**Result:** Coverage 84.4% (rounded to one decimal); 7 leavers (15.6%) have no exit interview.
**Caveats / what else I would check:** The counts may not line up one to one: the exit log could contain people not in HRIS (IDs mistyped, rehires) so the true gap could be larger than 7. Possible reasons for missing: employees who left abruptly or absconded, termination cases where interviews are not offered, refusals, notice-period timing (interview scheduled after the data cut), leavers in a different period, ID or name mismatch, or interviews held but not logged. Also check whether non-responders differ (for example, mostly involuntary or from one team), because that biases any exit-reason analysis.
**Next step / recommendation:** Match by employee ID (a left join from HRIS to the exit log), categorise the 7, and report exit-reason findings as "based on 84% of leavers". Track coverage monthly; set a target.

**Likely follow-ups:** 1) *Is 84% good enough?* It depends on whether the missing are random; if they skew toward one group, conclusions may mislead. 2) *Name or ID to match?* ID; names clash.
**Common mistakes / traps:** Calling it 16% without rounding care; assuming the 7 are a random sample; matching on names.

### Q57 ⭐⭐ 🔴 An employee history table keeps one row per change in role or manager. A headcount report counts rows and overstates staff. How do you diagnose and fix it?
**Asked at:** commonly asked (no company-specific report found); HRIS history-table duplication is a gap-fill scenario (judgement, not from a source).
**What the interviewer is checking:** That you understand the grain (what one row represents) and count people, not rows.
**Say this in the interview:** "The table's grain is one row per change, so counting rows counts changes. I count distinct employees whose row is current on the report date."

**First, clarify / contain:** Ask what the table's columns mean (employee ID, start date, end date, a current flag) and what date the headcount is for. Do not simply delete duplicates; the history is valuable.
**What I would check, in order:**
1. Compare `COUNT(*)` with `COUNT(DISTINCT employee_id)`; the gap is the extra rows.
2. Look at one employee with five rows to see the pattern.
3. Check how current rows are marked (an end date empty or 9999-12-31, or a flag).
4. Check for overlapping date ranges, which would double count even after filtering.
**If I find...:** Clean effective dating: count rows where `start_date <= report_date` and (`end_date > report_date` or end_date is empty). Missing or messy flags: take the latest row per employee by date. Overlaps or gaps: flag them to HR operations to fix at the source.
**What I would tell the stakeholder:** "Headcount was inflated because it counted job changes as people. Corrected figure is X as of the report date; previous reports using rows were overstated by Y. The history is still available for movement analysis."
**Prevent it next time:** A validation: headcount must equal one row per employee on the report date, and test it every load.

**Likely follow-ups:** 1) *Why not remove old rows?* You lose the ability to ask what headcount was on past dates. 2) *Which date to use?* Always state the as-of date.
**Common mistakes / traps:** `COUNT(*)` on a history table; deleting history; forgetting employees who left (end date passed).

### Q58 ⭐⭐ 🔴 Salary is missing for many senior employees in a pay analysis because they opted not to disclose. Why is simple imputation risky, and what do you do?
**Asked at:** commonly asked (no company-specific report found); missing-value handling (delete versus impute) is a repeated prep-guide theme (unverified).
**What the interviewer is checking:** Whether you recognise that the missingness is related to the value itself, so filling in an average biases results.
**Say this in the interview:** "The missing salaries are not random: they are concentrated among seniors, so filling with the average would understate pay. I would report the gap, avoid imputing blindly, and show results as a range."

**First, clarify / contain:** Ask how many are missing and in which bands and levels; ask the data owner whether non-disclosure has a policy basis. Do not fill in anything yet.
**What I would check, in order:**
1. Missing rate by grade, department and gender (a table).
2. Compare known characteristics of missing versus present (grade, tenure, location).
3. Check whether salary band data (min and max) exists for these grades, which gives a valid range.
4. Test how the headline (for example median pay by grade) changes under different treatments.
**If I find...:** Missing concentrated at the top: mean imputation pulls senior pay toward the overall mean, so averages and any pay-gap result are biased. Options: analyse only disclosed employees and say so; use grade-based imputation with caveats; or use bands for a sensitivity range (lower, upper). Very high missing in one group: say the analysis cannot answer the question for that group.
**What I would tell the stakeholder:** "Pay for 22% of senior employees (illustrative figure) is not disclosed, so the average I can calculate covers disclosed staff only and likely understates senior pay. I show the result under three assumptions. A firm number needs HR approval to use the confidential payroll figures."
**Prevent it next time:** Agree up front with HR and payroll which fields the analyst may access, under confidentiality rules; confirm applicable privacy obligations with the legal team.

**Likely follow-ups:** 1) *When is imputation fine?* When missing is random and small, and you report it. 2) *Why not drop the rows?* You then analyse a biased subset.
**Common mistakes / traps:** Filling with the overall mean; deleting silently; ignoring the ethics of inferring a person's disclosed-private pay.

### Q59 ⭐⭐ 🔴 Delivery times in an operations log range from 0 to 1,440 minutes, with a median of 32. How do you tell errors from genuine extremes before you treat them?
Inline data: delivery time minimum 0, maximum 1,440, median 32 minutes.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you investigate extremes with business logic and timestamps before deleting or capping.
**Say this in the interview:** "Zero minutes is impossible for a delivery, and 1,440 minutes is exactly 24 hours, which smells like a default or a data-entry problem. I would test each extreme against business rules and timestamps."

**What the data shows:** The middle delivery is 32 minutes, so typical performance is fine, but both ends look suspicious: 0 minutes is not plausible, and 1,440 = 24 x 60 is exactly one full day, a round number that often signals a missing end time or an overnight order.
**Working:**
1. 1,440 / 60 = 24 hours; 1,440 / 32 = 45 times the median.
2. Pull the rows near both ends and check their pickup, drop and order timestamps.
3. Compare the same order against rider, GPS or customer-confirmation logs.
4. Check the distribution (percentiles 1, 5, 95, 99) instead of just min and max.
**Result:** Zero-minute values are very likely errors (clock mismatch, same timestamp entered twice). 1,440 is a suspected error or a data default; it is genuine only if corroborated (for example, a held scheduled delivery or a failed attempt logged as delivered next day).
**Caveats / what else I would check:** Delivery type matters (instant versus scheduled orders); time zones and midnight crossings; how many rows are affected; whether errors cluster on one app version, store or rider. Statistical rules (such as the 1.5 x IQR rule) flag candidates but do not prove errors.
**Next step / recommendation:** Classify each extreme as error (fix or exclude, with a count reported), genuine (keep, and consider a separate segment), or unknown (keep, and run results with and without). Report median and percentiles, which resist extremes, rather than only the mean.

**Likely follow-ups:** 1) *Why not just remove outliers above 3 standard deviations?* Genuine delays are exactly what operations wants to see. 2) *Mean or median?* Median for typical; add the 90th percentile for service level.
**Common mistakes / traps:** Deleting extremes without checking; trusting one statistical rule; not reporting how many were excluded.

### Q60 ⭐⭐ 🔴 Fuzzy matching flags 12% of 10,000 customer records as probable duplicates. You check a random 400 flagged records and confirm 200 as true duplicates. Estimate how many true duplicates exist among the flagged records and how you would proceed.
Inline data: records 10,000; flagged 12%; sample 400; confirmed 200.
**Asked at:** commonly asked (no company-specific report found); a Meesho prompt on deduplication was seen in a vendor guide snippet (unverified).
**What the interviewer is checking:** Whether you can scale a sample result to a population with an honest range, and know precision from recall.
**Say this in the interview:** "Flagged is 1,200; half the sample was real, so about 600 are true duplicates, give or take roughly 50. That is precision; I would still need to check what the matcher missed."

**What the data shows:** The matcher is only about 50% precise: half the flagged records are false alarms.
**Working:**
1. Flagged = 12% x 10,000 = 1,200.
2. Sample precision = 200 / 400 = 50%.
3. Estimated true duplicates among flagged = 1,200 x 0.50 = 600; false positives about 600.
4. Uncertainty: standard error = sqrt(0.5 x 0.5 / 400) = 0.025; 95% interval is 50% +/- 4.9 points, about 45.1% to 54.9%, so about 541 to 659 records. (With a finite-population correction, since 400 is a third of 1,200, it tightens to about 46.0% to 54.0%, or 552 to 648.)
**Result:** About 600 true duplicates among the flagged (roughly 540 to 660; computed by script, rounded). Precision 50%.
**Caveats / what else I would check:** This says nothing about duplicates the matcher did not flag (recall), so total duplicates could be higher; test by reviewing a random sample of unflagged records. "Duplicate records" may count both members of a pair; define whether you are counting records or pairs. Reviewers can disagree; use two reviewers on a subset. A random sample must really be random.
**Next step / recommendation:** Do not auto-merge at 50% precision. Raise the match threshold or add rules (same phone or email plus similar name), re-sample, and auto-merge only very high-confidence matches while sending the rest for human review. Keep a merge log so merges can be undone.

**Likely follow-ups:** 1) *Why not trust the tool?* A 50% hit rate would merge about 600 different customers wrongly. 2) *What is a larger sample's benefit?* A narrower range; quadrupling the sample halves it.
**Common mistakes / traps:** Reporting 200 as the total; ignoring recall; merging automatically; forgetting the margin of error.

### Q61 ⭐⭐ 🔴 Daily figures for yesterday change when you rerun the report today because some data arrives late. How do you handle late-arriving data in reporting?
**Asked at:** commonly asked (no company-specific report found); late-arriving data and restatement are a gap-fill scenario (judgement).
**What the interviewer is checking:** That you know data settles over time and design reporting for it.
**Say this in the interview:** "Yesterday's number is provisional until late records land. I measure how long data typically takes to settle, mark recent days as provisional, and refresh a rolling window."

**First, clarify / contain:** Confirm the cause (delayed upload, batch job, offline entries). Do not hide the change or silently overwrite what people saw.
**What I would check, in order:**
1. Measure the lag: for each record, the gap between event date and load date; find the point by which, say, 99% have arrived.
2. Compare yesterday's first-run and re-run figures to see typical revision size.
3. Check the report uses event date (when it happened), not load date, for the trend.
4. Check no records are lost, only late.
**If I find...:** Small and predictable revisions: refresh the last N days every run, label recent days "provisional", and freeze older ones. Large revisions: delay publishing until the data matures, or show a range. Records never arriving: treat as a data-loss issue and escalate.
**What I would tell the stakeholder:** "The last 2 days are provisional: yesterday's sales typically rise by about 3% (illustrative) as late data lands. Figures older than 3 days are stable."
**Prevent it next time:** Keep snapshots of what each report showed on each day, add a visible "data as of" timestamp, and agree a cut-off time for publishing.

**Likely follow-ups:** 1) *Event date or load date?* Event date for trends; load date for tracking arrival. 2) *Do you re-state old numbers?* Within the settle window yes; beyond it, only by a controlled correction (see Q62).
**Common mistakes / traps:** Comparing a partial day with a full one and reporting a drop; no "as of" label; treating revisions as errors.

### Q62 ⭐⭐ 🔴 A correction to old data changes numbers that leadership has already seen. How do you handle versioning and communication?
**Asked at:** commonly asked (no company-specific report found); restatement is a gap-fill scenario (judgement).
**What the interviewer is checking:** Calm, early, transparent communication and a clean audit trail.
**Say this in the interview:** "I tell leadership before they find out, show old versus new with the reason, keep both versions on record, and say whether any decision changes."

**First, clarify / contain:** Confirm the correction is right and complete (do not send a second correction later). Pause using the old figures in new materials.
**What I would check, in order:**
1. Root cause and what exactly changed (rows, rule, period).
2. Size of the impact on each reported figure (old, new, difference, percent).
3. Which decisions or documents used the old numbers.
4. Whether other reports share the same data and need the same correction.
**If I find...:** Immaterial change: note it in the next regular report with a footnote. Material, or a conclusion changes: contact the sponsor directly first, then send a written correction. Externally shared or audited: involve the manager and the owner of the external communication.
**What I would tell the stakeholder:** "Last month's attrition was reported as 14.2%; after correcting duplicate leavers it is 13.1% (illustrative figures). The cause was X, now fixed. This does not change the recommendation to Y. Revised dashboard is live; the earlier version is archived as v1."
**Prevent it next time:** Version reports (v1, v2) with a change log, keep dated snapshots, and require a quick peer review before leadership numbers go out.

**Likely follow-ups:** 1) *Do you overwrite the old numbers?* No; keep versions, show the restatement. 2) *Who do you tell first?* The person who relies on it most, ahead of the broader audience.
**Common mistakes / traps:** Quietly updating the dashboard; over-apologising without facts; delay while "checking more".

### Q63 ⭐ 🟢 What is a golden record, and how does it help with duplicate customer or employee records?
**Asked at:** commonly asked (no company-specific report found); HRIS vendor blogs describe golden records and master data (unverified).
**What the interviewer is checking:** Whether you know the concept and how it links to duplicate handling.
**Say this in the interview:** "A golden record is the single best, trusted version of a person built from all the duplicate rows for them."

**Explain simply:**
- The same person can exist several times (a rehire, a name change, a customer who signed up twice). Each version may have different pieces of correct information.
- You group the duplicates, then build one record by applying survivorship rules: choose the most recent address, the most complete phone number, the verified email, and so on, per field.
- All the old IDs stay linked to the golden record's master ID, so history is not lost.
**Worked mini-example:** Row A: Priya Shah, phone blank, email old. Row B: P. Shah, phone present, email current. Golden record: Priya Shah, phone from B, email from B, with both source IDs linked.
**Practice step:** Take 10 duplicate-looking rows from a sample file, write one rule per field for which value wins, and build the merged row.
**Likely follow-ups:** 1) *Who owns the rules?* The business data owner (for HR, the HR data steward). 2) *Is it the same as deleting duplicates?* No; you merge and keep links.
**Common mistakes / traps:** Keeping only the first row; losing history; merging different people with similar names.

### Q64 ⭐ 🟡 A source system renames a column overnight and your report goes blank. How do you detect and prevent schema drift problems?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you handle the immediate fix and design early detection.
**Say this in the interview:** "Schema drift is a change in the structure of the source. I would restore the report quickly by mapping the new name, then add a check that alerts me before reports break."

**First, clarify / contain:** Tell users the report is down and give a time. Confirm with the source owner that it is a rename, not a different meaning.
**What I would check, in order:**
1. Compare the current columns to the last working list.
2. Confirm the renamed column holds the same data (types, sample values, row count).
3. Check the other dependent reports and queries.
4. Update the mapping in one place (a staging view), not in each report.
**If I find...:** A pure rename: map the new name to the old and refresh. A changed meaning or type: treat as a bigger change, validate numbers against the old version before publishing. Several columns changed: ask the source team for a change notice and a test window.
**What I would tell the stakeholder:** "The source renamed a field overnight; the dashboard is fixed as of 11:00 and numbers reconcile with yesterday. I have asked the source team to notify us before changes."
**Prevent it next time:** An automated schema check at load time (expected columns and types, failing loudly), a staging layer between source and reports, and change-notification agreements with source owners.

**Likely follow-ups:** 1) *Why a staging layer?* One fix point instead of many. 2) *Why alert rather than blank?* An error message is better than a silently empty chart.
**Common mistakes / traps:** Fixing each report separately; not checking that the data meaning is unchanged; no monitoring.

### Q65 ⭐ 🟡 What is a data quality score or scorecard, and how would you build one for a stakeholder audience?
**Asked at:** commonly asked (no company-specific report found); data-quality dimensions are common in question banks (unverified).
**What the interviewer is checking:** That you can turn abstract quality into a few measurable, understandable numbers.
**Say this in the interview:** "A scorecard measures quality dimensions such as completeness, validity and uniqueness per dataset, with a threshold, a trend and an owner."

**Explain simply:**
- Pick the dimensions that matter: completeness (not blank), validity (right format and range), uniqueness (no duplicates), consistency (matches across systems), timeliness (fresh).
- For each critical field, define one check and a rule, then calculate a percentage pass.
- Show a traffic light against agreed targets, a trend over months, and the owner for each red item.
**Worked mini-example (illustrative):** Employee file of 2,000 rows: date of joining blank on 40 rows, so completeness = 1,960 / 2,000 = 98.0%. Duplicate IDs on 10 rows, so uniqueness = 99.5%. A simple overall score = average of the checks, but keep the individual scores visible, since one average can hide a bad field.
**Practice step:** Build a five-line scorecard for one table you know, with target and owner per line.
**Likely follow-ups:** 1) *Weight the checks?* Yes, by business impact (a wrong salary matters more than a blank middle name). 2) *Audience?* Executives want one page and trend; data owners want the failing records list.
**Common mistakes / traps:** A single score with no detail; measuring everything; no owner or action.

### Q66 ⭐ 🟡 Survey completion times show many responses under 30 seconds for a 15-question survey. How do you identify low-quality responses and handle them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you use several signals and a transparent rule, and check the effect on results.
**Say this in the interview:** "Under 30 seconds for 15 questions is about 2 seconds a question, so many are probably rushed. I would combine speed with other signals and compare results with and without them."

**First, clarify / contain:** Ask whether the survey allows pre-filled or very simple questions, and whether it was mandatory. Do not delete anything yet.
**What I would check, in order:**
1. The completion-time distribution (median, 5th percentile), and relative cut-off such as under one third of the median.
2. Straight-lining: the same answer for every rating question.
3. Contradictions, failed attention-check questions, and gibberish text answers.
4. Duplicate respondents (same ID or device).
5. Patterns: did these come from one team, one link or one day?
**If I find...:** Speed plus straight-lining or failed checks: exclude as low quality. Fast but sensible and varied answers: keep (some people read quickly). Heavy clustering from a group: find out why (pressure to finish, a bulk-sent link).
**What I would tell the stakeholder:** "I excluded 9% of responses that were both very fast and showed identical answers. Headline scores moved by 0.1 points, so findings are unchanged. Rules and counts are listed in the appendix." (Illustrative.)
**Prevent it next time:** Add attention-check questions, show a progress bar, and record time per page.

**Likely follow-ups:** 1) *Is a fast completion enough to exclude?* No, use it with other signals. 2) *HR survey confidentiality?* Look at patterns, never try to identify individuals.
**Common mistakes / traps:** An arbitrary cut-off with no justification; excluding silently; no sensitivity check.

### Q67 ⭐ 🟡 A shared Excel file is edited by five people and versions conflict. How do you control quality?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Practical process thinking: one source of truth, access control, and validation.
**Say this in the interview:** "I would stop the copies, move to one shared source with controlled edit rights, and add validation and a change log."

**First, clarify / contain:** Freeze the current state, save a backup, and ask who edits what and why. Do not merge by eye.
**What I would check, in order:**
1. List the versions and compare them (Excel Compare, or a lookup of each key against the other copies).
2. Identify conflicting records and who is right (agree with the owners).
3. Create one master and mark the retired copies.
4. Add data validation (drop-downs, date and number rules), locked formula cells and a version or last-updated cell.
5. Decide edit rights: one owner per tab or column, others read-only.
**If I find...:** A few people need entry: use a form or an input tab with rules. Many editors or growing complexity: move to a shared database or a SharePoint-style list with version history (confirm what your organisation supports).
**What I would tell the stakeholder:** "Five copies created conflicting numbers. From Monday there is one master file; edits go through the owners and every change is logged."
**Prevent it next time:** A short written process, a change log, and a periodic check against the source system.

**Likely follow-ups:** 1) *Why not just trust the latest save?* Newest is not necessarily correct. 2) *Is co-authoring enough?* It avoids copies but not bad entries; validation is still needed.
**Common mistakes / traps:** Emailing attachments; fixing by hand without telling owners; no single owner.

### Q68 ⭐ 🟡 What is the difference between missing data that is truly absent and data that is not applicable? Give an HR example and say how each is coded.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you do not treat every blank as the same, because they need different handling.
**Say this in the interview:** "Absent means the value exists but we do not have it. Not applicable means no value can exist for that row. I code them differently so analysis does not mix them."

**Explain simply:**
- **Truly missing:** the answer exists but was not recorded. Example: an active employee's date of birth is blank. Code: null, or an explicit "Unknown", plus a missing flag.
- **Not applicable:** the field does not apply. Example: "Exit date" for a current employee, or "Notice-period end date" for someone who has not resigned. Code: a separate label such as "N/A" (or null, with a documented rule); never zero.
- **Zero is a real value:** zero leave taken is different from leave not recorded.
**Worked mini-example:** 100 employees, 10 have blank exit date. If all 10 are current staff, exit date is N/A, not a problem. If 6 are leavers with blank exit date, those 6 are missing data to fix (6% of the rows).
**Practice step:** Take one HR table and write, for each column, what a blank means and how you would code it.
**Likely follow-ups:** 1) *Why does it matter?* Averages and counts treat them differently; N/A should be excluded, missing needs follow-up or a decision. 2) *What about "refused"?* A third category, "declined to answer".
**Common mistakes / traps:** Filling blanks with 0; using one code for everything; removing N/A rows as errors.

### Q69 ⭐ 🔴 Ages in an employee file cluster at 30, 40 and 50 far more than at neighbouring values. What does this suggest, and what do you do?
**Asked at:** commonly asked (no company-specific report found); heaping is a gap-fill question (judgement).
**What the interviewer is checking:** Whether you recognise rounding behaviour (heaping) and its effect on analysis.
**Say this in the interview:** "Spikes at round numbers suggest people (or a form) rounded or guessed ages, called heaping. I would check where the data comes from and avoid over-precise use of age."

**First, clarify / contain:** Ask how age is captured: typed by employees, copied from a document, or calculated from date of birth. Do not delete the spikes; they are real records, just imprecise.
**What I would check, in order:**
1. Histogram of age by single year, and compare counts at 30, 40, 50 with their neighbours.
2. Check whether the field is derived from date of birth (then it should not heap) or typed in.
3. Look for dates of birth with 1 January, a common default or guess (from memory, unverified).
4. Check by source, branch or time of entry; heaping may come from one legacy system.
**If I find...:** Typed ages: the field is unreliable at the single-year level. Use age bands (such as 30 to 34) so rounding doesn't matter. If a verified date of birth exists in documents, correct from that source. Default dates of birth: flag them as "estimated".
**What I would tell the stakeholder:** "Age data shows rounding at 30, 40 and 50, so I report by 5-year bands, not exact ages. Single-year age results would be misleading."
**Prevent it next time:** Capture date of birth, calculate age, and validate against ID documents where policy allows.

**Likely follow-ups:** 1) *Does it affect averages?* Slightly; it hurts exact-age cut-offs (for example, "under 30" thresholds) the most. 2) *Why not fix it?* You cannot know the true age without a source.
**Common mistakes / traps:** Treating as genuine age clusters (a hiring wave); deleting records; making decisions at an exact age threshold.

### Q70 ⭐ 🔴 GPS pings from a delivery-partner app have gaps of several minutes. When would you interpolate, and when would you leave the gaps?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether the fill method depends on the question being answered.
**Say this in the interview:** "I interpolate only when the question needs a continuous path and the gap is short and plausible. When the gap could hide a real event or the question is about behaviour, I leave it as a gap and report it."

**First, clarify / contain:** Ask what the analysis is for (distance travelled, ETA accuracy, or detecting stops and rider issues). Do not fill anything until I know.
**What I would check, in order:**
1. Gap lengths: how many are under 1 minute, a few minutes, or much longer?
2. Where they happen (tunnels, low battery, poor signal, app closed) and whether they cluster by device or area.
3. Speed implied across the gap: a straight-line fill is plausible only if the speed is realistic.
4. Whether the rider was probably stopped (before and after pings in the same place).
**If I find...:** Short gap, moving steadily along a road: linear interpolation (or snap to the road) is reasonable for distance estimates. Long gap, or start and end far apart with road turns in between: leave it empty or flag it as an "estimated path"; do not invent a route. Gap with the same location either side: treat as a stop, and not as movement. Gaps that coincide with rider behaviour (switched off): that is a finding, not noise.
**What I would tell the stakeholder:** "Distances use interpolation for gaps under 2 minutes (about 6% of pings, illustrative); longer gaps are excluded and counted. Totals are therefore a lower bound."
**Prevent it next time:** Log the reason for gaps where the app allows it and set minimum ping standards.

**Likely follow-ups:** 1) *Does interpolation add information?* No, it adds assumption; document it. 2) *Alternative?* Analyse the data as it is, with the gap share reported.
**Common mistakes / traps:** Filling everything; straight lines through buildings; hiding the gap rate; ignoring privacy of location data (confirm policy with the owner).

### Q71 ⭐ 🔴 MCAR, MAR and MNAR describe different missing-data mechanisms. How would you tell them apart in a real dataset, and why does the distinction change your approach?
**Asked at:** commonly asked (no company-specific report found); an MNAR diagnosis question is a differentiator (judgement).
**What the interviewer is checking:** Conceptual understanding and an honest view that you can test some, but not all, of the three.
**Say this in the interview:** "MCAR is missing by pure chance, MAR depends on other columns I can see, and MNAR depends on the missing value itself. I can check the first two with data; the third I can only argue from business knowledge."

**Explain simply:**
- **MCAR (missing completely at random):** random. Example: a form lost by a technical glitch. Dropping rows loses only sample size.
- **MAR (missing at random):** missingness depends on observed data. Example: sales staff skip a survey question more often than engineers (department is known). Handled by modelling or imputing using the observed columns.
- **MNAR (missing not at random):** missingness depends on the unseen value. Example: very low (or very high) earners do not state salary; unhappy employees skip the engagement question. Simple fixes bias results.
**How to tell them apart:** make a missing flag (1 if blank) and compare it across groups: if the rate differs by department, grade or location, it is not MCAR (likely MAR). A formal test exists for MCAR (Little's test, from memory, unverified). MNAR cannot be proved from the data; ask the people who collected it, check an external source for a few cases, or follow up with a sample of non-responders.
**Worked mini-example:** Missing salary rate: 5% in junior grades, 40% in senior grades. That tells you it is not MCAR; whether it depends on salary itself still needs judgement.
**Why it changes the approach:** MCAR: deletion is usually safe. MAR: impute using the related columns. MNAR: report the limitation and run sensitivity checks (best and worst case).
**Practice step:** Pick a column with blanks in any file and chart the missing rate by two other columns.
**Likely follow-ups:** 1) *Which is the most common in reality?* Rarely pure MCAR; assume some pattern until shown otherwise. 2) *Is MAR safe to impute?* Only if the related variables are in the data.
**Common mistakes / traps:** Assuming MCAR by default; claiming you can prove MNAR from data alone; mean-imputing everything.

### Q72 ⭐ 🔴 Records show that the same person was rehired under a new employee ID. How do you link them for tenure and attrition analysis?
**Asked at:** commonly asked (no company-specific report found); HRIS blogs describe duplicates from rehires and name changes (unverified); rehire linking is a gap-fill question (judgement).
**What the interviewer is checking:** Careful, rule-based linking and awareness of what the business definition of tenure and attrition is.
**Say this in the interview:** "I would find rehires using a stable identifier and supporting fields, link them to a person-level master ID, and then agree with HR whether tenure counts continuous service or each stint."

**First, clarify / contain:** Ask HR how rehires are treated (is service continuous, is there a break rule, are benefits reinstated). Do not merge on name alone.
**What I would check, in order:**
1. Matching keys in order of strength: a government or official ID (if lawfully held and accessible; confirm with HR and legal), then date of birth plus name, then personal email or phone, then bank account details (access-restricted).
2. Normalise names (case, spaces, initials) before comparing; use fuzzy matching only for review candidates.
3. Check dates: the new hire date should be after the old exit date; overlapping dates suggest a duplicate or a data error, not a rehire.
4. Create a person ID that maps all employee IDs for the same person, with a record of how each match was made (rule and confidence).
5. Review ambiguous matches manually.
**If I find...:** Clear rehire with a short gap: tenure by policy (continuous or by stint). Long gap: usually treat as separate stints for attrition (the first exit is a real exit, and the rehire is a new hire), but follow the agreed definition. Overlapping dates: send to HR for correction.
**What I would tell the stakeholder:** "I identified 63 rehires by matching on a verified ID and date of birth. Counting them as one person changes average tenure from 3.4 to 3.7 years (all figures illustrative), and attrition counts each exit separately. Please confirm the rule."
**Prevent it next time:** Reuse the old employee ID on rehire, or store a person-level ID that persists across hires.

**Likely follow-ups:** 1) *Do rehires count as attrition?* Yes, the first exit was a real leaver; label rehires separately in hiring metrics. 2) *Privacy?* Restrict who sees identifying fields; use the person ID in analysis.
**Common mistakes / traps:** Matching on name only (two people with the same name); counting rehires as brand-new hires; counting one person twice in headcount.

