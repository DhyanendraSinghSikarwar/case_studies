# Book 4 — Power BI & Visualization | Part 11: Copilot and AI Features in Power BI 🟢🟡🔴

**Target:** 20 questions | **Actual:** 27 questions
**Scope:** Copilot in Power BI (what it does, licensing and capacity, admin settings, report/DAX/narrative features, preparing models, limits, privacy, verification) plus the built-in AI visuals; Fabric/Copilot admin depth only as far as an analyst is asked.

### Q1 ⭐⭐ 🟢 What is Copilot in Power BI, and what can it do?
**Asked at:** commonly asked (no company-specific report found); AI tools such as Copilot appear in 8 of 40 pooled job descriptions in the repo research (research/Book04_Part11_sources.md).
**What the interviewer is checking:** Do you understand Copilot as an assistant that speeds up work, not a replacement for checking?
**Say this in the interview:** "Copilot is Microsoft's AI assistant inside Power BI. I type a request in plain English and it can build report pages, answer questions about my data, write DAX, summarise a report and add measure descriptions. I treat everything it produces as a first draft that I review."
**Explain simply:**
- **Copilot** = a chat assistant built on a large language model (an AI trained on lots of text) that reads your semantic model (the tables, columns and measures behind the report).
- Typical jobs: create or edit report pages, add a narrative summary, answer questions in a chat, help write DAX (the Power BI formula language), write measure descriptions.
- It needs set-up (licence/capacity and an admin switch): see Q4, Q19.
- It does not know your business rules unless the model is named and described well (Q15).
**Example:** An HR analyst types "Show attrition by department for 2025 as a bar chart" and gets a draft page in seconds, then fixes the labels and checks the numbers against the HR system.
**DAX / Steps:** Concept question, no measure. Not run here.
**Alternative:** Without Copilot, you build the same page manually with the Build pane and write DAX yourself.
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be fetched here). The research file reports a Microsoft page "Copilot for Power BI overview" (dated 2026-08-24 in that file) listing these capabilities; not re-checked by me.
**Edge cases:** Features differ between Desktop and Service, and several are in preview (Q9).
**Likely follow-ups:** 1) *Can Copilot replace an analyst?* No, it drafts; the analyst owns correctness (Q3). 2) *What do you need to use it?* Q4.
**Common mistakes:** Calling it magic; sharing its output unchecked.

### Q2 ⭐⭐ 🟢 What are the AI visuals in Power BI (key influencers, decomposition tree, anomaly detection, smart narrative), and when would you use each?
**Asked at:** commonly asked (no company-specific report found); listed in generic Power BI guides per the sources file.
**What the interviewer is checking:** Can you match each AI visual to a business question?
**Say this in the interview:** "Key influencers tells me what factors push a metric up or down. Decomposition tree lets me drill into a number along any path I choose. Anomaly detection flags unusual points on a line chart. Smart narrative writes a text summary of the page."
**Explain simply:**
- **Key influencers:** "What drives attrition?" It ranks factors (overtime, department, tenure) by how strongly they relate to the outcome.
- **Decomposition tree:** "Where is the number coming from?" You split total leavers by department, then by manager, step by step.
- **Anomaly detection:** on a line chart over time, marks unusual spikes or dips (for example a sudden jump in absenteeism) and can suggest possible causes.
- **Smart narrative:** auto-written sentences that update with filters.
**Example:** Monthly leavers: 4, 5, 4, 5, 19, 5. Anomaly detection highlights the 19; the decomposition tree shows 14 of the 19 came from one department; key influencers shows overtime as the top factor.
**DAX / Steps:** Click-path (not run here): Report view > Visualizations pane > pick the visual icon > drag fields into its wells. Anomaly detection: line chart > Analytics pane > Find anomalies (menu names from memory).
**Alternative:** Plain bar charts and matrices answer simpler questions without AI.
**Version / licensing note:** from memory, unverified. The sources file says decomposition tree and anomaly detection descriptions were only seen as snippets, not fetched in full.
**Edge cases:** These visuals show correlation (things that move together), not proof of cause.
**Likely follow-ups:** 1) *Key influencers vs decomposition tree?* Q24. 2) *Does anomaly detection need Copilot?* No, from memory, unverified.
**Common mistakes:** Presenting "top influencer" as the cause; using them on tiny data.

### Q3 ⭐⭐ 🟡 How do you check a DAX measure or report page that Copilot generated before you share it?
**Asked at:** commonly asked (no company-specific report found); a blog snippet in the sources file suggests interviewers test checking AI-generated DAX (one author's anecdote).
**What the interviewer is checking:** Do you verify AI output instead of trusting it?
**Say this in the interview:** "I read the DAX line by line, test it against a small case I can calculate by hand, compare totals to a trusted source, check it under different slicers, and only then share it."
**Explain simply:**
- **Read it:** does the formula match the business definition (for example, attrition = leavers / headcount)?
- **Hand-check:** build a tiny table, calculate the answer yourself, compare.
- **Filter test:** click each slicer (a filter control); do totals and blanks behave?
- **Totals:** does the Total row make sense, and does it match the source system?
- **Page check:** titles, axis, units, sorting, wrong field used (for example headcount counted twice).
**Example:** Copilot gives attrition 25%. You count 3 leavers of 12 employees by hand: 25%. Then filter to HR: expected 0%.
**Sample data:** Table Employees (12 rows) is given in Q12 (3 leavers, 12 staff); the pandas snippet below rebuilds it.
**DAX / Steps (not run here, from memory):** open the measure in DAX query view and compare it to your own hand-built check, `EVALUATE ROW("Check", DIVIDE(3,12))` (`ROW` returns a one-row table; `DIVIDE` is safe division).
**Alternative:** Ask Copilot to explain the DAX in words, then compare the explanation to your intent.
**Result:** Reproduced with pandas: 3 / 12 = 0.25; HR = 0 / 3 = 0.
**Pandas check:**
```python
import pandas as pd
# the 12-row Employees table from Q12 (reused by Q12, Q13, Q23, Q24)
e = pd.DataFrame({
 'EmpID': range(1, 13),
 'Dept': ['Sales']*5 + ['IT']*4 + ['HR']*3,
 'Overtime': ['Yes','Yes','Yes','No','No','Yes','No','No','No','No','No','Yes'],
 'Left': [1,1,0,0,0,1,0,0,0,0,0,0]})
print(e.Left.sum()/len(e))             # 0.25
print(e[e.Dept=='HR'].Left.sum()/3)    # 0.0
```
Output: `0.25` then `0.0` (run with pandas 3.0.5).
**Version / licensing note:** from memory, unverified. The research file reports a Microsoft privacy page advising review of DAX before applying; not re-checked.
**Edge cases:** Blanks, duplicate employee rows, wrong date filter, totals that do not equal the sum of rows.
**Likely follow-ups:** 1) *Copilot gave a wrong answer, now what?* Fix the prompt or write it manually. 2) *Who is accountable?* The analyst.
**Common mistakes:** Checking only that it "returns a number".

### Q4 ⭐⭐ 🟡 What licence or capacity do you need to use Copilot in Power BI?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it is capacity-based, not just a per-user licence?
**Say this in the interview:** "Copilot needs paid capacity: a Fabric capacity (F2 or higher) or a Premium capacity (P1 or higher), plus the admin enabling the setting and a supported region. Trial and free capacities are not supported."
**Explain simply:**
- **Capacity** = a pool of computing power the company rents; Copilot work is charged to it.
- **Fabric F SKUs** (F2, F4, ...) and **Premium P SKUs** (P1, ...) are the paid sizes; a SKU is just a product size you can buy, bigger number = more computing power.
- Admin must enable Copilot in the tenant settings; the region must be supported.
- Older blogs say F64; the research file notes the fetched page said F2 or higher.
**Example:** Company has an F8 capacity; HR analysts with workspaces on it can use Copilot once the admin switch is on.
**DAX / Steps:** Concept. Steps for admin: see Q19.
**Alternative:** A Fabric Copilot capacity (FCC) can be used so Copilot usage is billed separately (Q25).
**Version / licensing note:** from memory, unverified (Microsoft Learn not reachable here). The research file reports the overview page (dated 2026-08-24 there) lists: paid Fabric F2+ or Premium P1+, trial/free unsupported, admin setting, supported region, sovereign clouds unsupported. Capacity rules change; re-check before quoting. No prices quoted.
**Edge cases:** Sovereign clouds (separate government/regional Microsoft clouds) unsupported; Private Link (a private network route to Azure) not supported (per the research file, unverified).
**Likely follow-ups:** 1) *Is Pro enough?* Q5. 2) *Trial?* Not supported per the file.
**Common mistakes:** Saying "any Pro licence works"; quoting the old F64 rule.

### Q5 ⭐ 🟢 Is a Power BI Pro licence enough to use Copilot?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Quick licensing fact check.
**Say this in the interview:** "No. Pro or PPU on its own is not enough. Copilot also needs the workspace on a paid Fabric or Premium capacity, or access through a Fabric Copilot capacity."
**Explain simply:**
- **Pro** = per-user licence to share and view reports. **PPU** (Premium Per User) = per-user premium features.
- Copilot is paid for through capacity, so the licence alone does not switch it on.
- Admin setting must also be on.
**Example:** An analyst has Pro, but the workspace is on shared capacity: no Copilot. Move it to an F-capacity workspace, or have the admin delegate an FCC: Copilot works.
**DAX / Steps:** Concept.
**Alternative:** Ask the admin to delegate a Fabric Copilot capacity (Q25).
**Version / licensing note:** from memory, unverified. The research file reports the overview page says Pro/PPU alone is not sufficient; the smart narrative page says Copilot mode "requires a Copilot license", which is looser; the overview is treated as authoritative.
**Edge cases:** PPU workspaces are reported as unsupported for the Desktop path (unverified).
**Likely follow-ups:** 1) *What do you need then?* Q4.
**Common mistakes:** Assuming "Copilot licence" is a separate per-user add-on.

### Q6 ⭐ 🟢 How do you start Copilot in Power BI Desktop and in the Power BI service to build a report page?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Hands-on familiarity.
**Say this in the interview:** "In Desktop I click the Copilot button on the Home ribbon, pick a workspace with Copilot capacity, and type my request. In the service I open the report in edit mode and use the Copilot button there."
**Explain simply:**
- Desktop: you must sign in and choose a workspace that has Copilot access.
- Service: you need edit rights on the report.
- Then describe the page you want; review the result.
**Example:** Prompt: "Create a page showing headcount and attrition by department."
**DAX / Steps (not run here, menu names from memory):**
1. Desktop: Home tab > Copilot button > choose workspace > type prompt > Send.
2. Service: open report > Edit > Copilot button > type prompt.
3. Review visuals, then Keep or Undo.
**Alternative:** Build manually from the Build pane.
**Version / licensing note:** from memory, unverified. The research file reports the Desktop button is disabled if neither the tenant setting nor delegation is on.
**Edge cases:** Button missing: Q22.
**Likely follow-ups:** 1) *Mac?* Desktop is Windows-only (from memory, unverified).
**Common mistakes:** Not picking a Copilot-enabled workspace.

### Q7 ⭐ 🟢 What is the Narrative visual with Copilot, and how is it different from the custom smart narrative?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the two narrative options?
**Say this in the interview:** "The Narrative visual with Copilot uses AI to write a summary of the report that I can steer with prompts. The custom smart narrative is the older, template-based one where I edit the text and insert dynamic values."
**Explain simply:**
- **Copilot narrative:** AI-written summary, refreshable, needs Copilot capacity.
- **Custom smart narrative:** you edit the text and add dynamic values (numbers that update with filters); no AI generation needed.
- Copilot narrative body text is not freely editable (per the research file).
**Example:** Copilot: "Attrition rose to 25% driven by Sales." Custom: "Attrition was [25%] in [2025]" with the brackets linked to measures.
**DAX / Steps (not run here, menu names from memory):** Insert > Narrative (or Smart narrative visual) > choose Copilot or custom mode.
**Alternative:** Write the summary text in a text box manually.
**Version / licensing note:** from memory, unverified. The research file reports a separate Microsoft page on the Copilot narrative visual (2026-05-11) and the smart narrative page (2026-09-25); not re-read.
**Edge cases:** Key influencers visual not supported by the Copilot narrative (per file).
**Likely follow-ups:** 1) *Do values update with slicers?* Smart narrative dynamic values do.
**Common mistakes:** Publishing an AI summary without checking numbers.

### Q8 ⭐ 🟢 What is the difference between the Copilot pane in a report and the standalone Copilot experience?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the two entry points.
**Say this in the interview:** "The pane lives inside one report and works on that report and its model. The standalone Copilot is a full-page chat that can search across reports and semantic models I have access to."
**Explain simply:**
- **Report pane:** scoped to the open report.
- **Standalone:** broader; you ask questions and it finds relevant items.
- Admin settings control both.
**Example:** Pane: "Summarise this attrition report." Standalone: "Which of my reports shows headcount by location?"
**DAX / Steps (not run here):** Pane: open report > Copilot icon. Standalone: Service left navigation > Copilot.
**Alternative:** Use search or the workspace list.
**Version / licensing note:** from memory, unverified. The research file reports standalone is on by default since September 2025 for the tenant; not re-checked.
**Edge cases:** It only surfaces items you have permission to see.
**Likely follow-ups:** 1) *Who controls it?* Admin (Q19).
**Common mistakes:** Assuming standalone sees everything in the company.

### Q9 ⭐ 🟢 Which Copilot experiences in Power BI are generally available and which are still in preview?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness that status changes, and honesty.
**Say this in the interview:** "It changes often, so I check the current Microsoft page. As far as I know, core things like report creation and DAX query view help are available, while some features such as Prepare data for AI were preview. I would not rely on a preview feature for production without approval."
**Explain simply:**
- **GA (generally available)** = supported for production. **Preview** = may change or be removed.
- Per the research file, Prepare data for AI (verified answers, AI instructions) is a preview feature.
- I cannot give a reliable list from memory.
**Example:** Do not build the company HR dashboard process on a preview feature without sign-off.
**DAX / Steps:** Check the status label at the top of each Microsoft Learn feature page.
**Alternative:** Read the monthly Power BI feature summary blog.
**Version / licensing note:** from memory, unverified; no page could be fetched here.
**Edge cases:** Features can move from preview to GA between your prep and the interview.
**Likely follow-ups:** 1) *How do you stay current?* Monthly release notes.
**Common mistakes:** Stating a fixed list confidently.

### Q10 ⭐ 🟡 What is the difference between Copilot and the Q&A visual in Power BI?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Old vs new natural-language tools.
**Say this in the interview:** "Q&A is the older feature: it turns a typed question into a visual using the model's synonyms. Copilot uses a large language model, handles broader requests such as building pages, DAX help and summaries. Microsoft has announced Q&A is going away."
**Explain simply:**
- **Q&A:** rule-based, needs you to set up synonyms (alternative names, for example "staff" = Employee).
- **Copilot:** AI, understands looser wording, can do more than one visual.
- The research file saw a banner saying Q&A experiences go away in February 2027, but another source said December 2026: dates conflict, unresolved.
**Example:** Q&A: "attrition by department" works if fields match. Copilot: "Build a one-page attrition overview" also works.
**DAX / Steps:** Concept.
**Alternative:** Keep Q&A until retirement for simple questions.
**Version / licensing note:** from memory, unverified; retirement date conflict stated above.
**Edge cases:** Prepare data for AI reportedly needs Q&A enabled (per file).
**Likely follow-ups:** 1) *When is Q&A retired?* Check Microsoft; dates conflict.
**Common mistakes:** Quoting one retirement date as fact.

### Q11 ⭐ 🟡 Write a Copilot prompt that builds an HR attrition report page, and explain why it is a good prompt.
**Asked at:** gap-fill practical question (no company-specific report found).
**What the interviewer is checking:** Can you write a specific, constrained prompt?
**Say this in the interview:** "A good prompt names the audience, the metrics, the breakdowns, the time period and the visuals, and stays in simple language."
**Explain simply:**
- Be specific about **fields** (use real column and measure names).
- State **audience** and **period**.
- Limit the size: one page, 5-6 visuals.
- Iterate: refine with follow-up prompts.
**Example prompt:**
"Create a one-page attrition overview for the HR leadership team. Use the Attrition Rate and Headcount measures. Show: cards for Headcount, Leavers and Attrition Rate; a bar chart of Attrition Rate by Department; a line chart of Leavers by month for 2025; a table of top 5 job roles by Leavers. Add a slicer for Location."
**Why good:** names measures (no guessing), audience, specific visuals, period, one page. Bad prompt: "make an HR dashboard".
**DAX / Steps:** Paste into the Copilot box (Q6). Not run here.
**Alternative:** Build by hand, or ask Copilot "suggest content for this report" first.
**Version / licensing note:** from memory, unverified. The research file reports a 10,000-character prompt limit.
**Edge cases:** If a measure does not exist in the model Copilot may create an implicit one (unverified).
**Likely follow-ups:** 1) *Prompt did not use my measure?* Name it exactly and check descriptions (Q14).
**Common mistakes:** Vague prompts; no time period; asking for ten things at once.

### Q12 ⭐ 🟡 How would you use Copilot to help write a DAX measure for attrition rate, and what would you check in the result?
**Asked at:** gap-fill practical question; a blog snippet in the sources file hints interviewers test checking AI DAX.
**What the interviewer is checking:** Can you define the metric precisely and verify the AI's formula?
**Say this in the interview:** "I tell Copilot the exact definition: leavers divided by headcount, using the Employees table and its Left column. Then I check it against a hand calculation, test the filters, and make sure it handles zero headcount."
**Explain simply:**
- **Attrition rate** = people who left / headcount (simple version). Better version uses average headcount for the period.
- **DIVIDE** = division that returns blank instead of an error when the denominator is zero.
- **CALCULATE** = changes the filter on a calculation.
- Always state the definition: AI cannot guess your HR policy.
**Example:** 3 leavers among 12 employees = 25%.
**Sample data:** Table Employees

| EmpID | Dept | Overtime | Left |
|---|---|---|---|
| 1 | Sales | Yes | 1 |
| 2 | Sales | Yes | 1 |
| 3 | Sales | Yes | 0 |
| 4 | Sales | No | 0 |
| 5 | Sales | No | 0 |
| 6 | IT | Yes | 1 |
| 7-9 | IT | No | 0 |
| 10-11 | HR | No | 0 |
| 12 | HR | Yes | 0 |

(Rows 7-9 and 10-11 are shown grouped for brevity; the pandas run uses 12 separate rows.)

**DAX (not run here):**
```dax
Headcount = COUNTROWS ( Employees )
Leavers = CALCULATE ( COUNTROWS ( Employees ), Employees[Left] = 1 )
Attrition Rate = DIVIDE ( [Leavers], [Headcount] )
```
**Alternative:** `Attrition Rate = DIVIDE ( SUM ( Employees[Left] ), COUNTROWS ( Employees ) )` since Left is 0/1; or use average headcount in the denominator.
**Result:** Reproduced with pandas (not a DAX engine): Leavers 3, Headcount 12, rate 0.25 (25%). By dept: HR 0.0, IT 0.25, Sales 0.40.
**Pandas check:**
```python
# uses the DataFrame e built in Q3
print(e.Left.sum(), len(e), round(e.Left.sum()/len(e),4))
print(e.groupby('Dept').Left.mean().round(3))
```
Output (run with pandas 3.0.5): `3 12 0.25`, then HR 0.00, IT 0.25, Sales 0.40.
**Version / licensing note:** DAX function behaviour (DIVIDE, CALCULATE, COUNTROWS) from memory, unverified: Microsoft Learn could not be fetched.
**Edge cases:** Zero headcount (DIVIDE returns blank); leavers counted by exit date vs a flag; duplicates; rehires; period filters.
**Likely follow-ups:** 1) *Average headcount?* (Start + End)/2. 2) *Why DIVIDE not "/"?* Safe on zero.
**Common mistakes:** Not telling Copilot the definition; using the leavers table count against current headcount only.

### Q13 ⭐ 🟡 How does Copilot work in DAX query view?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Familiarity with DAX query view and its Copilot features.
**Say this in the interview:** "DAX query view is where you write and run DAX queries against your model. Copilot there can write a query from plain English, explain a query or a measure, and help fix mistakes. I still review and run the result."
**Explain simply:**
- **DAX query** = starts with `EVALUATE` and returns a table, useful for testing measures.
- Copilot can generate a query, explain DAX, and suggest edits.
- Per the research file, it checks syntax and retries once; very large models may hit size limits; newer DAX functions may be unknown to it.
**Example:** Prompt: "Show attrition rate by department." Copilot writes a query that groups by department; you read it and run it.
**DAX (not run here):**
```dax
EVALUATE
SUMMARIZECOLUMNS ( Employees[Dept], "Attrition", [Attrition Rate] )
ORDER BY Employees[Dept]
```
**Alternative:** Write the query yourself, or use a table visual to test.
**Result:** Reproduced with pandas (not a DAX engine), assuming the `[Attrition Rate]` measure from Q12 exists: HR 0.0, IT 0.25, Sales 0.40.
**Pandas check:**
```python
# uses the DataFrame e built in Q3
print(e.groupby('Dept').Left.mean().round(3))
```
Output (run with pandas 3.0.5): HR 0.00, IT 0.25, Sales 0.40.
**Version / licensing note:** from memory, unverified. The research file reports a Microsoft page "Write DAX queries with Copilot" (updated 2026-06-29 there) with the points above; not re-read.
**Edge cases:** Model too large; hidden objects; Copilot may not know new functions.
**Likely follow-ups:** 1) *Can it change my model?* It suggests; you apply.
**Common mistakes:** Running generated queries without reading them.

### Q14 ⭐ 🟡 How do you use Copilot to add descriptions to your measures, and why do descriptions matter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know descriptions feed Copilot's understanding.
**Say this in the interview:** "I select the measure, use the Copilot option to create a description, review and edit it, and save. Descriptions matter because Copilot and other users rely on them to understand what a measure means."
**Explain simply:**
- **Description** = a short text on a measure or column, shown on hover.
- Per the research file, Copilot uses the DAX formula and table name; it ignores comments; the measure must have no errors; descriptions have a 200-character limit in that context.
- Good descriptions reduce wrong measure choices by Copilot.
**Example:** "Attrition Rate: Leavers divided by headcount for the selected period; excludes contractors."
**DAX / Steps (not run here, from memory):** Model view or Report view > select measure > Properties pane > Description > Create with Copilot > review > Apply.
**Alternative:** Type descriptions manually.
**Version / licensing note:** from memory, unverified; the file cites "Copilot measure descriptions" (2026-05-19 there).
**Edge cases:** AI wording may omit business exclusions; edit it.
**Likely follow-ups:** 1) *Other metadata?* Synonyms, display folders, hidden helper columns (Q15).
**Common mistakes:** Accepting generated text that misstates the logic.

### Q15 ⭐ 🟡 How do you prepare a semantic model so that Copilot gives better answers?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know model hygiene drives AI quality.
**Say this in the interview:** "Clean, well-named, well-described models give better answers: clear table and column names, descriptions, hidden technical columns, correct relationships, proper data types and ready-made measures."
**Explain simply:**
- **Semantic model** = the data model behind the report.
- Rename `col_x1` to `Exit Date`; hide helper columns.
- Create explicit measures for key metrics instead of relying on auto-sum.
- Add descriptions and synonyms (Q14).
- Use Prep data for AI: AI data schema, AI instructions, verified answers (Q16).
**Example:** Table `tblEmp` with column `Flg` becomes `Employees` with `Left (1 = left)` and a described Attrition Rate measure.
**DAX / Steps:** Concept. Not run here.
**Alternative:** Use a curated, certified dataset owned by the data team.
**Version / licensing note:** from memory, unverified; the research file lists Prepare data for AI (2026-05-26) as a preview feature.
**Edge cases:** Ambiguous column names (two "Date" columns).
**Likely follow-ups:** 1) *First fix?* Names and relationships.
**Common mistakes:** Blaming Copilot for a messy model.

### Q16 ⭐ 🟡 What are verified answers and AI instructions in Prep data for AI?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of the tools to steer Copilot.
**Say this in the interview:** "AI instructions are plain-language rules I give Copilot about my model, for example 'attrition means leavers divided by headcount'. Verified answers are pre-approved visuals tied to trigger questions, so Copilot returns the vetted answer."
**Explain simply:**
- **AI instructions** = business rules and context in words.
- **Verified answers** = a saved visual that answers specific questions consistently.
- Also an AI data schema to choose which fields Copilot may use.
- Per the research file, Prep data for AI is a preview feature and Q&A must be enabled.
**Example:** Verified answer for "What is our attrition rate?" shows the approved card, so every user gets the same number.
**DAX / Steps (not run here, from memory):** Desktop Home > Prep data for AI > AI data schema / Verified answers / AI instructions.
**Alternative:** Description fields and naming conventions.
**Version / licensing note:** from memory, unverified; preview per the research file.
**Edge cases:** Preview features may change.
**Likely follow-ups:** 1) *Does it make Copilot deterministic?* Reduces variation, not guarantees (Q21).
**Common mistakes:** Writing long, contradictory instructions.

### Q17 ⭐ 🟡 What does Approved for Copilot mean for a semantic model?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Governance awareness.
**Say this in the interview:** "It is a flag the model owner sets to say this semantic model has been prepared and is suitable for Copilot, so users and Copilot treat it as a trusted source."
**Explain simply:**
- A signal, not a guarantee of correct numbers.
- Part of Prep data for AI, per the research file.
- Unapproved models may be deprioritised or flagged (from memory, unverified).
**Example:** The HR team marks `HR Core Model` approved after adding descriptions and verified answers.
**DAX / Steps (not run here):** Prep data for AI > Mark as approved for Copilot (exact name from memory).
**Alternative:** Endorsement (Certified/Promoted), a related but separate feature.
**Version / licensing note:** from memory, unverified; preview per file.
**Edge cases:** Approval does not fix bad data.
**Likely follow-ups:** 1) *Who sets it?* The model owner/admin.
**Common mistakes:** Treating it as certification of accuracy.

### Q18 ⭐ 🟡 What are the limitations of creating or editing report pages with Copilot?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Realistic expectations.
**Say this in the interview:** "It does not control detailed styling, does not work with some data sources, may not use custom visuals, and sometimes picks the wrong fields, so I always review and finish by hand."
**Explain simply:**
- Per the research file: limits include Q&A having to be switched on, streaming datasets (live-feed data), live Analysis Services connections (a model hosted on a separate server), implicit measures (auto-sum fields), custom visuals, and no styling control.
- Prompts are limited in length (about 10,000 characters per prompt, per the research file).
- Output is a draft.
**Example:** Copilot builds the page but you must set company colours and fix titles.
**DAX / Steps:** Not applicable.
**Alternative:** Build manually, or use a template.
**Version / licensing note:** from memory, unverified; the file cites "Create and edit reports with Copilot" (2026-07-06 there).
**Edge cases:** Large models may be truncated.
**Likely follow-ups:** 1) *Can it delete visuals?* Yes, per file, it can add, change or delete visuals.
**Common mistakes:** Expecting final design quality.

### Q19 ⭐ 🟡 Who can turn Copilot on or off in a company, and where do they do it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it is an admin control.
**Say this in the interview:** "A Fabric administrator, in the Fabric admin portal under tenant settings. As an analyst I would ask them, not change it myself."
**Explain simply:**
- **Tenant setting** = a company-wide switch in the admin portal.
- Per the research file there are settings for Copilot, cross-geo processing and delegating capacity; Fabric tenants with paid capacity F2+ have it on by default per another page.
- Capacity admins can also decide which capacity is used.
**Example:** The company enables it for a security group of HR analysts only.
**DAX / Steps (not run here, from memory):** Settings (gear) > Admin portal > Tenant settings > Copilot settings > enable > Apply.
**Alternative:** Delegation via a Fabric Copilot capacity (Q25).
**Version / licensing note:** from memory, unverified; the file cites "Enable Fabric Copilot for Power BI" (updated 2026-07-23 there).
**Edge cases:** Cross-geo setting if the capacity region lacks Azure OpenAI.
**Likely follow-ups:** 1) *Can you restrict to a group?* Typically yes via security groups (unverified).
**Common mistakes:** Assuming the report author controls it.

### Q20 ⭐ 🟡 Does Copilot send your company data outside the organisation, and is it used to train models?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Privacy awareness, without overclaiming.
**Say this in the interview:** "According to Microsoft documentation, prompts and data go to the Azure OpenAI service within Microsoft's boundary and are not used to train the underlying models. Some regions may process data in another geography if the admin allows it. I would confirm the current policy with our security team."
**Explain simply:**
- Per the research file: no training on your data; processing stays in the tenant boundary; Azure OpenAI (Microsoft's hosted AI service) hosted in US and EU data boundary; cross-geo is an admin setting.
- Copilot only uses what the user can access; the page read did NOT state row-level security (RLS, rules that limit which rows each user sees) behaviour, so I make no claim.
**Example:** Salary data in the model: check with the security team before enabling.
**DAX / Steps:** Concept.
**Alternative:** Limit Copilot to non-sensitive models.
**Version / licensing note:** from memory, unverified; policy changes, re-check the Microsoft privacy page.
**Edge cases:** Sensitive HR data; cross-geo processing.
**Likely follow-ups:** 1) *Is RLS respected?* Not stated on the page read; verify.
**Common mistakes:** Saying "completely private, no data leaves" absolutely.

### Q21 ⭐ 🟡 Why can Copilot give a different answer to the same question, and what do you do about it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Understanding of non-deterministic AI.
**Say this in the interview:** "It is a language model, so output varies. It can also interpret an ambiguous question differently. I make prompts specific, add AI instructions and verified answers, and check the numbers."
**Explain simply:**
- **Non-deterministic** = the same input may give different outputs.
- Per the research file, Microsoft says this behaviour is expected.
- Ambiguous names or definitions increase variation.
- Fix: specific prompts, descriptions, instructions, verified answers (Q16).
**Example:** "Attrition by team" once uses Department, another time Manager.
**DAX / Steps:** Concept.
**Alternative:** Save the approved visual as a normal report page.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Cached answers (24-hour cache per file, unverified) can mask changes.
**Likely follow-ups:** 1) *Can you make it deterministic?* Not fully.
**Common mistakes:** Sharing a number from one run without a cross-check.

### Q22 ⭐ 🟡 The Copilot button is missing or disabled in Power BI Desktop. What do you check?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Structured troubleshooting.
**Say this in the interview:** "I check I am signed in, the Desktop version is current, the admin setting is on, my workspace is on a supported capacity, and my region and licence setup are right."
**Explain simply:**
1. Signed in with the work account?
2. Latest Desktop version?
3. Tenant Copilot setting on, or an FCC delegated? (Per file, the button is disabled if neither is on.)
4. Selected workspace on paid F2+/P1+ capacity? Not trial/PPU workspace (per file, unverified).
5. Supported region; no Private Link.
6. Ask the admin.
**Example:** Analyst's workspace was on shared capacity; moved to F8 workspace; button works.
**DAX / Steps:** Not run here.
**Alternative:** Use the service version.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Sovereign cloud.
**Likely follow-ups:** 1) *Still failing?* Raise an admin ticket with the error text.
**Common mistakes:** Reinstalling Desktop before checking admin settings.

### Q23 ⭐ 🟡 How would you use the key influencers visual to find what drives employee attrition?
**Asked at:** gap-fill practical question (no company-specific report found).
**What the interviewer is checking:** Can you configure and interpret it.
**Say this in the interview:** "I put Left as the field to Analyze, choose the value 1 (left), and add factors like Overtime, Department and Tenure under Explain by. The visual ranks what makes leaving more likely, and I treat it as a clue, not proof."
**Explain simply:**
- **Analyze** = the outcome; **Explain by** = candidate factors.
- Shows "when Overtime = Yes, attrition is X times more likely".
- Needs enough rows; per file, not supported with DirectQuery (a mode where Power BI queries the source live instead of storing a copy).
**Example:** In the sample, 60% of overtime employees left against 0% of non-overtime.
**Sample data:** Table Employees (Q12).
**DAX / Steps (not run here):** Visualizations > Key influencers > Analyze: Left (value 1) > Explain by: Overtime, Dept.
**Alternative:** Compare attrition rate by factor with a bar chart.
**Result:** Reproduced with pandas (plain rates, not the visual's machine-learning model; the Sales/IT/HR rates come from the Q12 run): Overtime Yes 3/5 = 0.6; No 0/7 = 0.0; Sales 0.4, IT 0.25, HR 0.0.
**Pandas check:**
```python
# uses the DataFrame e built in Q3
print(e.groupby('Overtime').Left.mean())
```
Output (run with pandas 3.0.5): No 0.0, Yes 0.6.
**Version / licensing note:** from memory, unverified; the file cites the key influencers page (2026-08-24).
**Edge cases:** 12 rows is far too few for real use; correlated factors; correlation is not cause.
**Likely follow-ups:** 1) *Next step?* Investigate why overtime and who.
**Common mistakes:** Using too few rows; claiming causation.

### Q24 ⭐ 🟡 What is the difference between the key influencers visual and the decomposition tree?
**Asked at:** gap-fill practical question (no company-specific report found).
**What the interviewer is checking:** Choosing the right tool.
**Say this in the interview:** "Key influencers uses statistics to rank what is associated with an outcome. The decomposition tree is manual drill-down: I split a total by fields in the order I choose, or let it pick the highest or lowest value."
**Explain simply:**
- Key influencers: automatic ranking, answers "what drives it".
- Decomposition tree: step-by-step breakdown, answers "where does it come from".
- Tree shows counts and totals; influencers shows likelihood.
**Example:** Total leavers 3. Tree: Sales 2, IT 1; then Overtime Yes for all. Influencers: Overtime strongest.
**Sample data:** Table Employees (Q12).
**DAX / Steps (not run here):** Decomposition tree: add the Leavers measure (Q12) to Analyze, Dept and Overtime to Explain by.
**Alternative:** Matrix with drill-down.
**Result:** Reproduced with pandas: leavers Sales/Yes 2, IT/Yes 1.
**Pandas check:**
```python
# uses the DataFrame e built in Q3
print(e[e.Left==1].groupby(['Dept','Overtime']).size())
```
Output (run with pandas 3.0.5): IT Yes 1, Sales Yes 2.
**Version / licensing note:** from memory, unverified; decomposition tree page not fetched in the earlier research either.
**Edge cases:** Tree shows share, not rate; rates need a measure.
**Likely follow-ups:** 1) *Which first?* Tree to explore, influencers to rank.
**Common mistakes:** Reading tree totals as rates.

### Q25 ⭐ 🔴 What is a Fabric Copilot capacity, and when would a company use one?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Capacity concepts at analyst level.
**Say this in the interview:** "A Fabric Copilot capacity, or FCC, is a paid capacity an admin sets aside so users anywhere in the company can use Copilot and the usage is billed to it, even if their own workspace is on Pro or PPU. A company uses it to give Copilot to many people without moving all workspaces to Fabric."
**Explain simply:**
- Per the research file: supports Desktop and Pro/PPU workspaces; needs F2 or P1 minimum; home region only; one FCC per user; Embedded mode unsupported.
- Central cost control for Copilot.
**Example:** Company keeps HR reports on Pro, buys an F4, designates it as FCC for the analytics team.
**DAX / Steps:** Admin steps from memory unverified: Admin portal > Copilot settings > select capacity.
**Alternative:** Move workspaces to Fabric capacity.
**Version / licensing note:** from memory, unverified; the file cites "Fabric Copilot capacity" (2026-10-20 there). No prices quoted; prices change.
**Edge cases:** Region mismatch.
**Likely follow-ups:** 1) *Who pays?* The capacity owner.
**Common mistakes:** Confusing it with a per-user licence.

### Q26 ⭐ 🔴 How does Copilot use capacity, and how would an admin monitor that usage?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of consumption and monitoring.
**Say this in the interview:** "Copilot requests consume capacity units, the capacity's unit of compute, as background usage. Admins monitor it in the Microsoft Fabric Capacity Metrics app, and heavy use can cause throttling."
**Explain simply:**
- **CU (capacity unit)** = measure of compute.
- Per the research file: Capacity Metrics app shows Copilot background usage; throttling warning on the Fabric overview page.
- Admin can watch trends and decide to scale up.
**Example:** Metrics app shows a Copilot spike at month-end when many analysts ask Copilot to summarise HR reports at the same time.
**DAX / Steps:** Admin installs the Capacity Metrics app (from memory unverified) and checks the Copilot operations.
**Alternative:** Separate FCC to isolate cost.
**Version / licensing note:** from memory, unverified; exact billing rates not stated.
**Edge cases:** Throttling also affects other workloads on the same capacity.
**Likely follow-ups:** 1) *How to cut usage?* Fewer, specific prompts; separate capacity.
**Common mistakes:** Assuming Copilot is free once enabled.

### Q27 ⭐ 🔴 Your company wants to roll Copilot out to its HR dashboards. What do you check before switching it on?
**Asked at:** gap-fill scenario question (no company-specific report found).
**What the interviewer is checking:** Judgement: privacy, quality, cost, accuracy.
**Say this in the interview:** "I check data sensitivity and access, licensing and capacity, model readiness, accuracy testing, and training users to verify outputs."
**Explain simply:**
1. **Sensitivity:** HR data (salary, health, performance) is sensitive; get security and legal sign-off; confirm data residency and cross-geo settings (Q20).
2. **Access:** who sees what; test RLS (row-level security, rules limiting rows per user) behaviour with Copilot yourself, since not confirmed on the page read.
3. **Licensing/capacity:** F2+/P1+ or FCC; monitor usage (Q25, Q26).
4. **Model readiness:** names, descriptions, instructions, verified answers (Q15, Q16).
5. **Testing:** a set of 20 known questions with known answers; compare.
6. **Rollout:** pilot group, guidance that outputs are drafts, a feedback channel.
**Example:** Pilot with 5 HR analysts for a month; 18 of 20 test questions correct; fix descriptions for the other 2.
**DAX / Steps:** Checklist. Not run here.
**Alternative:** Enable only for non-sensitive models first.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Preview features; Q&A retirement; Private Link unsupported (per file).
**Likely follow-ups:** 1) *Who signs off?* Security, legal, HR head.
**Common mistakes:** Turning it on tenant-wide first and sorting privacy later.
