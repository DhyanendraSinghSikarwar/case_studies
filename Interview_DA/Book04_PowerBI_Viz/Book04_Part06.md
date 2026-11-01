# Book 4 — Power BI & Visualization | Part 6: Visuals, Slicers, Drill-through, Bookmarks, Tooltips 🟢🟡

**Target:** 55 questions | **Actual:** 61 questions
**Scope:** choosing and formatting visuals, slicers and filters, visual interactions, drill down and drill-through, bookmarks and buttons, tooltips, conditional formatting.

### Q1 ⭐⭐⭐ 🟢 What is a slicer in Power BI, and how is it different from a filter in the Filters pane?
**Asked at:** commonly asked (no company-specific report found); research/interview_processes.md records a Cognizant 2022 report mentioning "slicers, filters" in general.
**What the interviewer is checking:** Do you know that a slicer is a visible on-page control for report users, while the Filters pane is a builder-side tool?
**Say this in the interview:** "A slicer is a visual on the page, like a Department drop-down, that the report reader clicks to filter other visuals. The Filters pane does the same job but sits at the side, is less prominent, and can be locked or hidden by the report author."
**Explain simply:**
- Slicer = a button panel on the canvas (a list of departments, a date range). The reader sees what is selected.
- Filters pane = a side panel where the author sets filters at visual, page or report level (Q3). Readers can change them unless locked.
- A slicer filters only the visuals it is allowed to affect (Edit interactions, Q9). A Filters-pane filter at page level hits every visual on that page.
- A slicer can be synced across pages (Q10); a page-level filter cannot.
**Example:** An HR dashboard has a Department slicer. The reader picks "Sales" and every chart shows only Sales' 200 employees. A report-level filter "Status = Active" in the Filters pane sits quietly in the background.
**DAX / Steps (not run here):** Visualizations pane > Slicer icon > drag Department into Field. Filters pane opens via View tab > Filters.
**Alternative:** A Filters-pane filter when you want the filter fixed and not tampered with; a slicer when readers must choose.
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be fetched: ENOTFOUND). Slicers work in Desktop and the Service on all licences as far as I recall.
**Edge cases:** Slicers work only on fields related to the visuals through the model; an unrelated table filters nothing.
**Likely follow-ups:** 1) *Can a slicer filter only some visuals?* Yes, Edit interactions. 2) *Which is better for end users?* Slicer.
**Common mistakes:** Calling them identical; using many slicers where one report-level filter would do.

### Q2 ⭐⭐⭐ 🟢 What is the difference between drill down and drill through in Power BI?
**Asked at:** commonly asked (no company-specific report found); a Telegram post lists "drilldown vs drill through" for Bajaj Auto but it is unofficial and unverified.
**What the interviewer is checking:** Can you separate "go deeper inside one visual" from "jump to another page with context"?
**Say this in the interview:** "Drill down moves within the same visual along a hierarchy, like Year to Quarter to Month. Drill through jumps to a different page, carrying the item I clicked, such as one department, to show detail."
**Explain simply:**
- Hierarchy = ordered levels of a field set, e.g. Region > City > Branch.
- Drill down: same visual, new level, same page. By default it does not change other visuals (Q37).
- Drill through: right-click a data point > Drillthrough > page name. A separate page opens already filtered to that point.
- Drill through needs a page built for it (Q8).
**Example:** On "Attrition by Department", drill down splits Sales into its four cities on the same chart. Drill through on Sales opens an "Employee detail" page listing Sales' 36 leavers.
**DAX / Steps (not run here):** Drill down: turn on drill mode (arrow icon at the visual's top) > click a bar > use the down arrow. Drill through: right-click a bar > Drillthrough > target page.
**Alternative:** A button with a Page navigation action when no context needs carrying.
**Version / licensing note:** from memory, unverified. The research file lists "Use drill mode" and "Drillthrough in Power BI reports" Microsoft pages, but I could not re-fetch them.
**Edge cases:** Drill down needs a hierarchy of at least two fields in the visual.
**Likely follow-ups:** 1) *Does drill down filter other visuals?* Not by default. 2) *Can drill-through go to another report?* Yes, with conditions (Q49).
**Common mistakes:** Mixing the two names; expecting drill through without building a target page.

### Q3 ⭐⭐⭐ 🟢 What are the different levels of filters in Power BI (visual, page and report level)?
**Asked at:** commonly asked (no company-specific report found); the Cognizant 2022 report in research/interview_processes.md mentions "filters" in general.
**What the interviewer is checking:** Do you know the scope of each level?
**Say this in the interview:** "Visual-level filters affect one visual, page-level filters affect every visual on that page, report-level filters affect every page. There is also a drillthrough filter for drill-through pages."
**Explain simply:**
- Scope = how far a filter reaches.
- Visual level: only the selected chart or table.
- Page level: all visuals on this page.
- Report level: all pages. Good for "Status = Active".
- All are in the Filters pane; slicers add to them. Filters combine (AND), they do not override each other.
**Example:** Report filter: Employment Status = Active. Page filter on the Hiring page: Year = 2025. Visual filter on one chart: Top 5 departments by hires.
**DAX / Steps (not run here):** View tab > Filters. Select a visual, page or nothing, then drag a field into "Filters on this visual", "on this page" or "on all pages".
**Alternative:** A slicer when readers should choose.
**Version / licensing note:** from memory, unverified.
**Edge cases:** A report-level filter hides data from every page, including pages where you wanted it; check totals.
**Likely follow-ups:** 1) *Can I lock one?* Yes, Q40. 2) *Do filters stack?* Yes, AND.
**Common mistakes:** Putting a filter at report level when it is only needed for one page; forgetting a hidden filter when numbers do not tie.

### Q4 ⭐⭐⭐ 🟢 What is a bookmark in Power BI, and what is it used for?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a bookmark saves a view, and the usual uses (navigation, toggles)?
**Say this in the interview:** "A bookmark captures the current state of a report page, including filters, slicers, and which visuals are visible. I use bookmarks with buttons for navigation, switching between a chart and a table, and guided storytelling."
**Explain simply:**
- Think of a screenshot you can click that restores the page exactly as saved.
- It stores filters, slicer choices, sort, visibility from the Selection pane, and more, depending on options (Q27).
- Uses: "Reset filters" button, chart/table switch (Q28), executive walkthrough.
- Bookmarks do not store data; they store settings.
**Example:** An attrition page with a bookmark "View: Chart" and another "View: Table" and two buttons to flip between them.
**DAX / Steps (not run here):** View tab > Bookmarks pane > Add > rename. Then Insert > Buttons > Action type = Bookmark.
**Alternative:** Page navigation buttons when you only need to go to another page.
**Version / licensing note:** from memory, unverified. The research file lists Microsoft's "Create report bookmarks" page, not re-fetched by me.
**Edge cases:** Slicers added after a bookmark was made may not be reflected (Q47).
**Likely follow-ups:** 1) *Report vs personal bookmark?* Q46. 2) *What if the bookmark should not change filters?* Untick Data.
**Common mistakes:** Not updating the bookmark after changing the page; leaving Data ticked on a pure visibility toggle.

### Q5 ⭐⭐⭐ 🟢 What is a tooltip in Power BI, and what is a report page tooltip?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the default tooltip and the custom-page version?
**Say this in the interview:** "A tooltip is the small box that appears when you hover over a data point. A report page tooltip replaces it with a mini report page, for example a small chart, so hovering gives richer detail."
**Explain simply:**
- Default tooltip shows the category and value (Sales: 36 leavers).
- You can add extra fields to the default tooltip (the Tooltips well in the Build pane).
- Report page tooltip: a small page, marked as a tooltip, that is shown on hover and filtered to the hovered point.
- Hover only; it is not clickable.
**Example:** Hover over the Sales bar in headcount and a mini line chart shows Sales' monthly attrition for the year.
**DAX / Steps (not run here):** Page tooltip: add a page > Format page > Page information > Allow use as tooltip on; Canvas settings > Type = Tooltip. Then on the visual: Format > General > Tooltips > Type = Report page > choose page. Full steps in Q26.
**Alternative:** Add fields to the Tooltips well for a simple text extension.
**Version / licensing note:** from memory, unverified. The research file notes tooltips are non-interactive and not available on dashboards (Microsoft page "Create report tooltips"; not re-fetched by me).
**Edge cases:** Needs a field that exists in the hovered visual, or the tooltip page shows unfiltered data.
**Likely follow-ups:** 1) *Can a user click inside it?* No. 2) *Phone use?* No hover.
**Common mistakes:** Leaving the tooltip page full-size; forgetting to choose the page on the visual.

### Q6 ⭐⭐⭐ 🟢 What is the difference between a table visual and a matrix visual?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Flat list versus pivot-style grid.
**Say this in the interview:** "A table is a flat list of rows and columns. A matrix is like an Excel pivot table: fields on rows and columns, with subtotals, expand/collapse, and one value at each intersection."
**Explain simply:**
- Table: every column is a field; good for an employee list.
- Matrix: has Rows, Columns and Values wells; it can show Department down and Month across.
- A matrix can drill with + / - and show subtotals; a table cannot.
- Both support conditional formatting (Q11, Q32).
**Example:** Table: ID, Name, Dept for 200 staff. Matrix: Department rows, Month columns, leaver count in cells.
**DAX / Steps (not run here):** Visualizations pane > Table or Matrix icon; drag fields to Columns/Rows/Values.
**Alternative:** An Excel PivotTable with Analyze in Excel.
**Version / licensing note:** from memory, unverified.
**Edge cases:** A matrix with a high-cardinality field (employee ID) on rows gets very slow.
**Likely follow-ups:** 1) *Which for a heat map?* Matrix. 2) *Which for an export list?* Table.
**Common mistakes:** Using a table for cross-tab data and then wondering why subtotals are missing.

### Q7 ⭐⭐⭐ 🟢 Which visual would you choose to show monthly headcount over two years, and why?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard chart-choice practice.
**What the interviewer is checking:** Do you choose by data shape (time trend) and not by habit?
**Say this in the interview:** "A line chart, with month on the x-axis and headcount on the y-axis, because time trends read naturally as a line. For two years, I would draw two lines on the same Jan-Dec axis for year-over-year comparison, or one continuous 24-month line."
**Explain simply:**
- Line = best for change over time; the eye follows the slope.
- Use a date hierarchy or a month column sorted in calendar order (Q25).
- A column chart also works for 24 bars, but a line is cleaner for trends.
- Avoid pie charts (Q14) for time.
- Start the axis at zero for columns; for lines a tight axis is fine if clearly labelled.
**Example:** Headcount grows 1,150 to 1,240 over 2024-25 with a dip in March. A line shows the dip immediately; a table would hide it.
**DAX / Steps (not run here):** Line chart > X-axis: Month (from Date table) > Y-axis: [Headcount] > Legend: Year (optional for two lines).
**Alternative:** Column chart, or area chart (Q39) if emphasising volume.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Headcount is a snapshot at month end, not a sum; a SUM measure would double count (a measure design question for Part 5).
**Likely follow-ups:** 1) *Add a target?* Analytics pane, Q22. 2) *Many categories?* Small multiples.
**Common mistakes:** Using clustered columns with 24 categories; alphabetical month order.

### Q8 ⭐⭐⭐ 🟡 How do you create a drill-through page in Power BI, step by step?
**Asked at:** commonly asked (no company-specific report found); drill-through set-up is listed in prep blogs (research/Book04_Part06_sources.md, snippet only).
**What the interviewer is checking:** Can you actually build it, including the right field in the drillthrough well?
**Say this in the interview:** "Add a new page, drag the field, for example Department, into the Drillthrough well, build the detail visuals, and Power BI adds a back button. Then on the summary page I right-click a department and choose Drillthrough."
**Explain simply:**
- Drillthrough well = the field that identifies the context passed to the page.
- Detail visuals on that page are then filtered to the chosen item automatically.
- A Back button is added automatically on the page.
- Users reach it by right-clicking a data point.
**Example:** Summary page: attrition by department. Drill-through page "Department detail" with a card of leavers and a table of employees. Right-click Sales, jump to Sales' 36 leavers.
**DAX / Steps (not run here):**
1. Home > New page; rename "Department detail".
2. Select the page canvas; in the Build pane find Drill through (Add drill-through fields here).
3. Drag Department into it (leave Cross-report off, Keep all filters as needed, Q48).
4. Add a card [Leavers], a table of Employee, Tenure.
5. On the summary page: right-click a bar > Drillthrough > Department detail.
**Alternative:** A button with Page navigation, or a report page tooltip (Q5) for light detail.
**Version / licensing note:** from memory, unverified.
**Edge cases:** The field must exist in the source visual; measures cannot be the drillthrough field (Q29).
**Likely follow-ups:** 1) *Multiple fields?* Yes, AND/OR rules depend on settings. 2) *Hide the page?* Yes.
**Common mistakes:** Forgetting that no field in the well means no Drillthrough option; the field is not in the clicked visual.

### Q9 ⭐⭐⭐ 🟡 How do you stop a slicer from filtering one particular visual on the page?
**Asked at:** commonly asked (no company-specific report found); "edit interactions" is a live-build task in prep blogs (snippets only).
**What the interviewer is checking:** Do you know Edit interactions?
**Say this in the interview:** "Select the slicer, turn on Edit interactions from the Format tab, then on the visual I want left alone I click the 'None' icon, the circle with a line through it."
**Explain simply:**
- Visual interactions = how one visual affects others (filter, highlight, none).
- Set per slicer-visual pair; other visuals stay filtered.
- Useful for a KPI card that should show the company total even when a department is selected.
**Example:** Department slicer = Sales, but a card "Company headcount 550" should stay at 550.
**DAX / Steps (not run here):** Click the slicer > Format tab > Edit interactions > on the card click None > turn off Edit interactions.
**Alternative:** Use a measure with ALL(Department) (DAX, not run here), so the card ignores the slicer; or put the card on a different page.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Interactions are per page; a synced slicer on another page needs its own setting.
**Likely follow-ups:** 1) *Does it apply to all slicers?* Per source visual. 2) *Cross-filter vs highlight?* Q15.
**Common mistakes:** Forgetting the setting is one-directional (slicer to visual), or leaving Edit interactions on.

### Q10 ⭐⭐⭐ 🟡 How do you make one slicer control several pages of a report?
**Asked at:** commonly asked (no company-specific report found); "sync slicers" appears in vendor guides (snippet only).
**What the interviewer is checking:** Sync slicers.
**Say this in the interview:** "View tab, Sync slicers pane. I tick the pages where the slicer should apply and, optionally, where it should be visible."
**Explain simply:**
- Sync = the same selection follows you from page to page.
- Two checkboxes per page: Sync (applies the selection) and Visible (shows the slicer).
- Fields must be the same field from the same table, otherwise sync does not link.
**Example:** A Year slicer on Page 1 set to 2025 also filters the Hiring and Attendance pages.
**DAX / Steps (not run here):** Click the slicer > View tab > Show panes > Sync slicers > tick the Sync column for each page and Visible if the slicer should show.
**Alternative:** Put the field as a report-level filter if readers need no choice.
**Version / licensing note:** from memory, unverified.
**Edge cases:** A slicer that is synced but not visible still filters; tell users.
**Likely follow-ups:** 1) *Sync only some slicers?* Yes, groups. 2) *Same name in two tables?* Not linked.
**Common mistakes:** Copying a slicer by hand to each page; synced-but-hidden slicers that confuse users.

### Q11 ⭐⭐⭐ 🟡 How would you colour an attrition rate column red when it is above 15% and green otherwise?
**Asked at:** commonly asked (no company-specific report found); conditional formatting is a standard build task in prep lists.
**What the interviewer is checking:** Rules-based conditional formatting and how totals behave.
**Say this in the interview:** "In the table, Format > Cell elements > Background colour > fx, choose Rules: if value is greater than 0.15 then red, otherwise green. The same can be done with a DAX measure for colour (field value formatting)."
**Explain simply:**
- Conditional formatting = colour decided by the number.
- Rules need an exact threshold; 15% is 0.15 for a decimal field.
- The Total row follows the same rule, so it can also turn red.
**Example:** Attrition = Leavers / Average headcount.
**Sample data:** Table `Dept`:

| Dept | AvgHeadcount | Leavers |
|---|---|---|
| Sales | 200 | 36 |
| IT | 150 | 18 |
| HR | 40 | 8 |
| Finance | 60 | 6 |
| Ops | 100 | 17 |

**DAX / Steps (not run here):**
```dax
Attrition Rate = DIVIDE(SUM(Dept[Leavers]), SUM(Dept[AvgHeadcount]))
Attrition Colour = IF([Attrition Rate] > 0.15, "#C0392B", "#27AE60")
```
Rules path: select visual > Format > Cell elements > Background colour > fx > Format style = Rules > add rule "If value is greater than 0.15" = red, then a second rule "If value is less than or equal to 0.15" = green (menu names from memory, unverified).
**Alternative:** Field value: Format style = Field value > Based on field = [Attrition Colour].
**Result (reproduced with pandas, not a DAX engine):** Sales 18% red, IT 12% green, HR 20% red, Finance 10% green, Ops 17% red; Total 15.45% red.
**Pandas check:**
```python
import pandas as pd
d=pd.DataFrame({"Dept":["Sales","IT","HR","Finance","Ops"],"AvgHeadcount":[200,150,40,60,100],"Leavers":[36,18,8,6,17]})
d["Attrition"]=d.Leavers/d.AvgHeadcount
d["Colour"]=d.Attrition.apply(lambda x:"Red" if x>0.15 else "Green")
print(d); print(d.Leavers.sum()/d.AvgHeadcount.sum())   # total 0.1545...
```
Output: Sales 0.18 Red; IT 0.12 Green; HR 0.20 Red; Finance 0.10 Green; Ops 0.17 Red; Total 0.1545 Red.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Exactly 15% is green with "> 0.15". Blank or divide-by-zero: DIVIDE returns blank, which gets no colour unless handled. Total row is a ratio of totals, not an average of rates.
**Likely follow-ups:** 1) *Why DIVIDE?* Avoids divide-by-zero errors. 2) *Colour on a card?* Via the same Field value route where supported.
**Common mistakes:** Typing 15 instead of 0.15; ignoring the Total row colour.

### Q12 ⭐⭐⭐ 🟡 A slicer selection is not changing one of the visuals on the page. What do you check?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice (a troubleshooting scenario).
**What the interviewer is checking:** A calm checklist, not guessing.
**Say this in the interview:** "First Edit interactions, whether that visual is set to None. Then whether the slicer's field is related to that visual's table in the model, whether the visual has its own filter, and whether the measure ignores filters, for example with ALL."
**Explain simply:**
- Check 1: Edit interactions: is the visual set to None for this slicer?
- Check 2: Relationships: is the slicer field in a table connected to the visual's table? Unrelated = no effect.
- Check 3: Does the measure remove filters (ALL, REMOVEFILTERS) or use a fixed filter?
- Check 4: Is the visual using a different, disconnected table, or a filter in the Filters pane that conflicts?
- Check 5: Is the slicer synced or in an unexpected state (e.g., Select all)?
**Example:** A "Company headcount" card never changes with a Department slicer because it was set to None, which was intended.
**DAX / Steps (not run here):** Select slicer > Format > Edit interactions and read the icons; Model view > check relationships.
**Alternative:** Test by dragging the slicer field into a plain table to see the relationship work.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Many-to-many or inactive relationships can make a filter appear not to propagate.
**Likely follow-ups:** 1) *Visual shows blank instead?* Filter direction. 2) *Only on Service?* Check the saved report.
**Common mistakes:** Blaming the visual before checking relationships.

### Q13 ⭐⭐ 🟢 What is the difference between a bar chart and a column chart, and between clustered and stacked?
**Asked at:** commonly asked (no company-specific report found); gap-fill.
**What the interviewer is checking:** Orientation and comparison versus composition.
**Say this in the interview:** "Bar is horizontal, column is vertical. Clustered puts series side by side to compare them; stacked piles them to show the total and the parts."
**Explain simply:**
- Bar charts suit long category names (department names); columns suit time or few categories.
- Clustered: compare each series across the category.
- Stacked: total plus composition. 100% stacked shows share, not size.
- Stacked makes the upper segments hard to compare.
**Example:** Hires by department split into male and female: clustered to compare the two; stacked to show total hires too.
**DAX / Steps (not run here):** Visualizations pane > pick Clustered bar / Stacked bar / Clustered column / Stacked column; add Legend for the series.
**Alternative:** 100% stacked when share matters.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Too many segments make stacked charts unreadable.
**Likely follow-ups:** 1) *Negative values?* Fine, but stacked gets confusing. 2) *Sort order?* By value for bars.
**Common mistakes:** Stacking when comparison of segments is the goal.

### Q14 ⭐⭐ 🟢 When would you use a pie or donut chart, and when should you avoid it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Judgement on part-to-whole charts.
**Say this in the interview:** "Only for a few categories, about two to five, that add up to a whole, when the message is a rough share. I avoid it with many slices, similar sizes or time trends; a bar chart is clearer."
**Explain simply:**
- Humans compare angles poorly, so close values (28% vs 31%) are hard to read.
- Good: gender split of 2 groups, or active vs exited.
- Bad: 12 departments, or a monthly trend.
- A donut is the same chart with a hole; you can put a total inside.
**Example:** Workforce 60% permanent / 30% contract / 10% intern fits a pie. Attrition by 12 departments fits a sorted bar.
**DAX / Steps (not run here):** Visualizations pane > Pie chart or Donut chart > Legend: category, Values: [Headcount].
**Alternative:** Sorted bar, or treemap for many parts.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Negative values cannot be shown; slices that do not sum to a whole mislead.
**Likely follow-ups:** 1) *Better for ranking?* Bar. 2) *Treemap?* Many parts.
**Common mistakes:** Pie for 10+ slices; 3D effects.

### Q15 ⭐⭐ 🟢 What are cross-filtering and cross-highlighting between visuals?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Default click behaviour of visuals.
**Say this in the interview:** "When I click a bar, the other visuals react. Cross-filtering shows only the related data in them; cross-highlighting keeps the full picture and dims or highlights the related part."
**Explain simply:**
- Cross-filter: other visuals show only the selected item's data.
- Cross-highlight: other visuals keep the full bars but darken the selected share. Default for many chart types.
- Controlled per visual pair with Edit interactions (Q9).
- Click again to clear.
**Example:** Click "Sales" in a department chart: a gender column chart shows only Sales (filter) or shows all with Sales' portion shaded (highlight).
**DAX / Steps (not run here):** Select the source visual > Format tab > Edit interactions > on each target choose Filter, Highlight or None.
**Alternative:** Slicer for explicit selection.
**Version / licensing note:** from memory, unverified. The research file notes the Microsoft page "Change how visuals interact" (an older cross-filter page returned 404 in the earlier research pass).
**Edge cases:** Highlight is not available for some visual types, which then filter instead.
**Likely follow-ups:** 1) *Stop one visual reacting?* None. 2) *Does drill affect others?* Q37.
**Common mistakes:** Confusing highlight with filter when numbers look unchanged.

### Q16 ⭐⭐ 🟢 What types of slicer are available, and when would you use each (list, dropdown, tile, between, relative date)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Matching slicer style to field type.
**Say this in the interview:** "List for a few options always visible, dropdown to save space with many options, tile buttons for a few categories, between for numeric or date ranges, relative date for 'last 30 days'."
**Explain simply:**
- List: all values shown; best for 3 to 8 options.
- Dropdown: one line until clicked; best for long lists such as 40 locations.
- Tile (buttons): friendly for months or Yes/No.
- Between (slider): a numeric or date range, for example tenure 0 to 10 years.
- Relative date: rolling windows such as last 3 months, which update daily.
- Relative time exists for time fields, and names change between Desktop versions.
**Example:** Department = dropdown, Year = tile, Tenure = between, "Joined in last 90 days" = relative date.
**DAX / Steps (not run here):** Slicer visual > Format > Slicer settings > Options > Style: List / Dropdown / Tile / Between / Relative date (style choices depend on the field's data type).
**Alternative:** Filters pane filter when no on-page control is wanted.
**Version / licensing note:** from memory, unverified. The research file warns slicer names (for example, list slicer, input slicer) changed across recent builds; recheck your Desktop version.
**Edge cases:** Relative date needs a real date field, not text.
**Likely follow-ups:** 1) *Single-select?* Format > Selection > Single select. 2) *Search box?* Dropdown/list option.
**Common mistakes:** A long list slicer taking half the page.

### Q17 ⭐⭐ 🟢 What is the difference between basic filtering, advanced filtering, Top N and relative date filtering?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The four filter types in the Filters pane.
**Say this in the interview:** "Basic: tick the values. Advanced: conditions like 'contains' or 'greater than', combined with And/Or. Top N: the top or bottom N by a measure. Relative date: a rolling time window."
**Explain simply:**
- Basic: choose items from a list.
- Advanced: rules such as "Department contains 'Sales' and Tenure is greater than 2".
- Top N: pick Top or Bottom, N, and the measure to rank by (Q18).
- Relative date: last/next/this N days, weeks, months, years.
- Which one appears depends on the field type (text, number, date).
**Example:** Basic: Sales and IT. Advanced: Salary greater than 50,000. Top N: top 5 departments by attrition. Relative date: joined in last 3 months.
**DAX / Steps (not run here):** Filters pane > hover on the field > expand > Filter type drop-down.
**Alternative:** Slicers for reader-controlled versions.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Top N ties can return more than N rows.
**Likely follow-ups:** 1) *Can a filter use a measure?* Yes, as a visual-level filter. 2) *Relative date vs slicer?* Same logic, different place.
**Common mistakes:** Applying a filter without clicking "Apply filter" in the Filters pane.

### Q18 ⭐⭐ 🟢 How do you show only the top 10 products by sales in a visual?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Visual-level Top N filter and the right ranking field.
**Say this in the interview:** "Select the visual, in the Filters pane open Product, change the filter type to Top N, set Top 10 by value, drag the Sales measure into By value, and click Apply filter."
**Explain simply:**
- Top N = keep the N items with the highest measure.
- It is a visual-level filter, so other visuals are unaffected.
- The ranking measure can differ from the one displayed.
**Example:** 12 products; keep the best 10.
**Sample data:** Table `Product` (Sales in thousands):

| Product | Sales |
|---|---|
| A | 120 |
| B | 95 |
| C | 300 |
| D | 40 |
| E | 210 |
| F | 80 |
| G | 150 |
| H | 60 |
| I | 175 |
| J | 25 |
| K | 110 |
| L | 260 |

**DAX / Steps (not run here):** Filters pane > Filters on this visual > Product > Filter type: Top N > Show items: Top, 10 > By value: [Total Sales] > Apply filter.
**Alternative:** A measure with TOPN or RANKX (DAX, not run here), for example `Rank = RANKX(ALL(Product[Product]), [Total Sales])`, then filter Rank <= 10.
**Result (reproduced with pandas):** Kept: C 300, L 260, E 210, I 175, G 150, A 120, K 110, B 95, F 80, H 60. Dropped: D 40, J 25. Top 10 total 1,560 of 1,625.
**Pandas check:**
```python
import pandas as pd
p=pd.DataFrame({"Product":list("ABCDEFGHIJKL"),"Sales":[120,95,300,40,210,80,150,60,175,25,110,260]})
print(p.nlargest(10,"Sales"))
print(p.nlargest(10,"Sales").Sales.sum(), p.Sales.sum())
```
Output: the ten rows above, then `1560 1625`.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Ties at rank 10 can return extra rows. Totals in the visual show the top 10 total only, not the grand total.
**Likely follow-ups:** 1) *Top 10 per region?* Needs a RANKX-style measure. 2) *Include "Others"?* Needs a custom grouping.
**Common mistakes:** Forgetting to click Apply filter; ranking by the wrong measure.

### Q19 ⭐⭐ 🟢 What is the difference between a card, a multi-row card and a KPI visual?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Choosing a headline-number visual.
**Say this in the interview:** "A card shows a single number. A multi-row card shows several fields, one block per row. A KPI visual shows a value against a target and a trend."
**Explain simply:**
- Card: one measure, for example Headcount 550.
- Multi-row card: a small block per category with several fields.
- KPI: needs an indicator (value), a trend axis (e.g., month) and a target; colours show good or bad.
- A newer "Card" visual may allow multiple values, and names have changed across builds.
**Example:** Card: Attrition 15.4%. KPI: Attrition 15.4% vs target 12% with a monthly trend.
**DAX / Steps (not run here):** Visualizations pane > Card / Multi-row card / KPI > drag the fields; for KPI: Value, Trend axis, Target goals.
**Alternative:** A gauge (single value against range).
**Version / licensing note:** from memory, unverified; card visuals were being redesigned, so check your build.
**Edge cases:** KPI colours treat higher as good by default; for attrition, flip the direction setting.
**Likely follow-ups:** 1) *Lower is better?* Format > Direction. 2) *Cards and slicers?* Cards respond to them.
**Common mistakes:** A KPI with no trend axis; leaving "higher is better" on for attrition.

### Q20 ⭐⭐ 🟢 What are buttons in Power BI, and what actions can a button perform?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know buttons are interaction elements for navigation and behaviour.
**Say this in the interview:** "Buttons are clickable shapes or icons on the page. Their actions include Back, Bookmark, Page navigation, Drillthrough, Q&A, Apply all slicers, Clear all slicers, and Web URL."
**Explain simply:**
- Action = what happens on click.
- Back: return from a drill-through page.
- Bookmark: restore a saved view (Q4).
- Page navigation: jump to a page.
- Drillthrough: go to a drill-through page.
- Apply/Clear all slicers: reader sets several slicers, then applies once.
- Web URL: open a link.
**Example:** A "Reset" button runs a bookmark; "HR detail" navigates to another page.
**DAX / Steps (not run here):** Home > Insert > Buttons > pick a style > select the button > Format > Action > On > Type and Destination.
**Alternative:** Images or shapes can carry the same actions.
**Version / licensing note:** from memory, unverified. The research file notes Apply all/Clear all button actions come from Microsoft's slicer page; I did not re-fetch it. Buttons do not work as actions when printed or in some embedded views.
**Edge cases:** Ctrl+click is needed to trigger a button in Desktop's editing mode.
**Likely follow-ups:** 1) *Can a button be disabled?* With conditional formatting. 2) *Tooltip on a button?* Yes, text.
**Common mistakes:** Forgetting to set the Action to On, or setting a destination that is empty.

### Q21 ⭐⭐ 🟢 What is the Selection pane used for?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know how to manage layered objects on a page, especially for bookmark-based designs.
**Say this in the interview:** "The Selection pane lists every object on the page: visuals, buttons, shapes. I use it to show or hide them, rename them, reorder the layers and pick items that are hidden behind others. It is the backbone of bookmark toggles."
**Explain simply:**
- Open it: **View tab > Show panes > Selection** (Desktop). Each object has an eye icon to show or hide it.
- The order in the list is the stacking order (front to back). Drag to change which object sits on top.
- Give objects clear names ("Chart - Headcount", "Table - Employees") so you can find them later. Use **Alt text** for accessibility separately.
- Hidden state is saved by bookmarks, so show/hide + bookmark + button = a custom view switcher.
**Example:** An HR page has a headcount chart and a headcount table stacked in the same spot. In the Selection pane you hide the table (click its eye), save that as a bookmark, then reverse it for a second bookmark.
**DAX / Steps (not run here):** 1) View > Show panes > Selection. 2) Click the eye next to an object to hide it. 3) Double-click a name to rename it. 4) Drag items up or down to reorder layers.
**Alternative:** Select a visual on the canvas and use Format > Arrange > Bring forward / Send backward (slower for crowded pages).
**Version / licensing note:** from memory, unverified (could not reach Microsoft Learn). Selection pane is a Desktop and Service editing feature; the Service needs edit rights on the report.
**Edge cases:** Hidden visuals still exist and can still be filtered; hiding does not remove them from the data load. Slicers hidden this way still apply their selection.
**Likely follow-ups:** 1) *Why rename objects?* So bookmarks and buttons are easy to maintain. 2) *Does hiding a visual reduce load time?* Not reliably; hidden visuals can still run queries (from memory, unverified).
**Common mistakes:** Leaving default names like "Visual 17"; forgetting that a hidden slicer still filters.

### Q22 ⭐⭐ 🟢 What is the Analytics pane, and how do you add an average line or a target line to a chart?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can add reference lines without writing extra measures.
**Say this in the interview:** "The Analytics pane, the magnifying-glass icon next to Format, adds helper lines to a chart: average, median, min, max, constant and percentile lines, trend lines and forecasts. For a target I add a Y-axis constant line at the target value, or a measure if the target changes."
**Explain simply:**
- Select the chart, open the **Analytics** pane, expand **Average line**, switch it on. You can choose which series it measures.
- **Y-axis constant line** is a fixed number, such as a target headcount of 440.
- Not every visual supports it (works on cartesian charts such as line, column, bar; not on pie or table) — from memory, unverified.
- If the target changes by month, make a measure and add it as a second line series instead.
**Example:** Monthly headcount Jan-Jun is 410, 420, 415, 430, 445, 450. The average line sits at 428.3. A constant line at 440 shows only May and June meet the target.
**Sample data:** Table `Headcount` (6 months)

| Month | Headcount |
|---|---|
| Jan | 410 |
| Feb | 420 |
| Mar | 415 |
| Apr | 430 |
| May | 445 |
| Jun | 450 |

**DAX / Steps (not run here):** Click chart > Analytics pane > Average line > On. For a measure-based average line:
```dax
Avg Headcount = AVERAGEX ( ALLSELECTED ( 'Calendar'[Month] ), [Headcount] )
```
**Alternative:** Add `Avg Headcount` as a second line series (works when the chart type has no Analytics line, or you need a custom calculation).
**Result:** reproduced with pandas: average = 428.33.
**Pandas check:**
```python
import pandas as pd
hc = pd.DataFrame({"Month":["Jan","Feb","Mar","Apr","May","Jun"],"Headcount":[410,420,415,430,445,450]})
print(hc.Headcount.mean())   # 428.3333333333333
```
**Version / licensing note:** from memory, unverified. DAX functions AVERAGEX and ALLSELECTED not checked against Microsoft Learn this session.
**Edge cases:** The built-in average line responds to filters/slicers; a Constant line does not. With a legend, the average is per series.
**Likely follow-ups:** 1) *Can the target come from data?* Yes, use a measure. 2) *Trend line vs average line?* A trend line shows direction; average is a flat level.
**Common mistakes:** Hard-coding a Constant line and forgetting it when the target changes; looking for the pane on a visual that does not support it.

### Q23 ⭐⭐ 🟢 How do you change the number format and display units (thousands, millions) of data labels?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can make numbers readable for executives.
**Say this in the interview:** "In the Format pane I open Data labels, then Value, and set Display units to Thousands or Millions and the decimal places. For the field's own number format I use Column tools or Measure tools on the ribbon."
**Explain simply:**
- **Display units** only changes how the number is shown (12,345,678 shows as 12.3M). The underlying value stays the same.
- Visual-level: select visual > **Format > Visual > Data labels > Value > Display units / Value decimal places**.
- Field-level: select the field > **Column tools / Measure tools tab > Format** (currency, %, thousands separator). Applies everywhere the field is used.
- Use "Auto" if you want it to adapt, but fixed units keep a dashboard consistent.
**Example:** Payroll by region: 12,345,678 shows as 12.3M with one decimal; 9,876,543 as 9.9M.
**Sample data:** Table `Payroll`

| Region | Payroll | Shown as (M, 1 dp) |
|---|---|---|
| North | 12,345,678 | 12.3M |
| South | 9,876,543 | 9.9M |
| East | 4,567,890 | 4.6M |
| West | 15,000,000 | 15.0M |

**DAX / Steps (not run here):** Format pane > Data labels > Value > Display units = Millions, Decimal places = 1. Or as text (not recommended for charts):
```dax
Payroll M = FORMAT ( [Total Payroll] / 1000000, "0.0" ) & "M"
```
**Alternative:** Set a custom format string on the measure, for example `0.0,,"M"` in Measure tools > Format (from memory, unverified); this keeps the measure numeric.
**Result:** reproduced with pandas: 12.3, 9.9, 4.6, 15.0 (millions, 1 decimal).
**Pandas check:**
```python
import pandas as pd
s = pd.DataFrame({"Payroll":[12345678,9876543,4567890,15000000]})
print((s.Payroll/1e6).round(1).tolist())   # [12.3, 9.9, 4.6, 15.0]
```
**Version / licensing note:** from memory, unverified. Indian grouping (lakh/crore) is not a built-in display unit; I believe a custom approach is needed (unverified).
**Edge cases:** FORMAT returns text, so it cannot be sorted or used on an axis as a number. Rounding in the label does not change totals.
**Likely follow-ups:** 1) *Lakhs and crores?* Divide the measure by 100,000 or 10,000,000 and label it. 2) *Axis units?* Same idea under the Axis settings.
**Common mistakes:** Using FORMAT everywhere, which turns numbers into text; changing units on one visual but not others.

### Q24 ⭐⭐ 🟢 What are themes in Power BI, and how do you apply one to a report?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you care about consistent branding and know the quick route to it.
**Say this in the interview:** "A theme is a saved set of colours and formatting defaults for the whole report, stored as a JSON file. I apply one from View > Themes, either a built-in one or my company's imported file, so every visual follows the same palette."
**Explain simply:**
- **View tab > Themes**: pick a built-in theme, or **Browse for themes** to import a JSON file, or **Customize current theme** to tweak colours and fonts.
- A theme sets default data colours, text styles and visual defaults; you can still override a single visual.
- Share the JSON file so every analyst's report looks the same.
- Good themes also care about contrast for colour-blind users.
**Example:** The HR team imports `HR_Brand.json` with navy and teal. All new charts use those colours automatically, instead of someone recolouring 20 visuals by hand.
**DAX / Steps (not run here):** 1) View > Themes (dropdown) > choose a theme. 2) Or Themes > Browse for themes > pick the .json. 3) Or Themes > Customize current theme to edit; save current theme to export it.
**Alternative:** Format each visual manually (slow, inconsistent), or set colours through a conditional-formatting measure (Q31) for rule-based colours.
**Version / licensing note:** from memory, unverified. Themes are available in free Desktop; the Service can import a theme in some cases (unverified).
**Edge cases:** Manual formatting on a visual overrides the theme. Changing the theme later does not recolour manually formatted items.
**Likely follow-ups:** 1) *Where do I get themes?* The built-in list, Microsoft's theme gallery or your brand team (from memory, unverified). 2) *Can I edit JSON?* Yes, but use Customize first.
**Common mistakes:** Formatting visuals first and applying a theme afterwards; picking low-contrast colours.

### Q25 ⭐⭐ 🟡 How do you sort a visual by a different column, for example month names in calendar order instead of alphabetical?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Do you know about "Sort by column" and why text sorts alphabetically?
**Say this in the interview:** "Month names are text, so Power BI sorts them A to Z: April, February, January. I add a month number column and use Column tools > Sort by column > MonthNum, so the chart shows Jan to Dec."
**Explain simply:**
- Text columns sort alphabetically by default; numbers sort numerically.
- Create a numeric helper column (1 to 12) in the Date table, or use `MONTH([Date])`.
- Select the Month Name column in the Data/Model view > **Column tools > Sort by column** > choose Month Number.
- Then on the visual, use **... > Sort axis > Month** and ascending.
**Example:** Hires per month Jan-Jun appear as Apr, Feb, Jan, Jun, Mar, May before the fix; Jan to Jun after.
**Sample data:** Table `Calendar`

| Month | MonthNum | Hires |
|---|---|---|
| Jan | 1 | 12 |
| Feb | 2 | 9 |
| Mar | 3 | 15 |
| Apr | 4 | 7 |
| May | 5 | 11 |
| Jun | 6 | 10 |

**DAX / Steps (not run here):**
```dax
MonthNum = MONTH ( 'Calendar'[Date] )
Month = FORMAT ( 'Calendar'[Date], "MMM" )
```
Then: select `Month` column > Column tools > Sort by column > `MonthNum`.
**Alternative:** Use a real date field with the built-in date hierarchy (its months already sort in order), or sort descending/ascending by the measure when you want "largest first".
**Result:** reproduced with pandas: alphabetical `['Apr','Feb','Jan','Jun','Mar','May']`; by MonthNum `['Jan','Feb','Mar','Apr','May','Jun']`.
**Pandas check:**
```python
import pandas as pd
m = pd.DataFrame({"Month":["Jan","Feb","Mar","Apr","May","Jun"],"MonthNum":range(1,7),"Hires":[12,9,15,7,11,10]})
print(m.sort_values("Month").Month.tolist()); print(m.sort_values("MonthNum").Month.tolist())
```
**Version / licensing note:** from memory, unverified. Available in all Desktop versions.
**Edge cases:** Each Month value must map to exactly one MonthNum, or Sort by column errors. For fiscal years (April start), number months from April = 1.
**Likely follow-ups:** 1) *Fiscal months?* Make the helper number start at April. 2) *Why not sort by Hires?* That orders by value, not time.
**Common mistakes:** Sorting the visual only (Sort axis) without fixing the column; mapping one name to two numbers.

### Q26 ⭐⭐ 🟡 How do you build a report page tooltip, step by step?
**Asked at:** commonly asked (no company-specific report found); the sources file lists tooltips as a standard fresher question.
**What the interviewer is checking:** Whether you can build a custom hover card, not just use the default one.
**Say this in the interview:** "I make a small new page, switch on Allow use as tooltip in Page information, set the page size to Tooltip, build visuals for it, then on the main visual I set Tooltips > Type > Report page and choose that page."
**Explain simply:**
- A **report page tooltip** is a mini page that pops up when you hover a data point, filtered to that point.
- Build on a new page, **Format page > Canvas settings > Type: Tooltip** (small size) and **Page information > Allow use as tooltip** on.
- Fields dragged into the **Tooltips** well of the target visual define which fields filter the tooltip page (for example Department).
- Then set the target visual: **Format > General > Tooltips > Type: Report page > Page**.
**Example:** Hover a department bar and the tooltip page shows that department's attrition trend and its top 3 exit reasons.
**DAX / Steps (not run here):** 1) New page "Tip - Dept". 2) Format page > Canvas settings > Type = Tooltip. 3) Page information > Allow use as tooltip = On. 4) Add visuals filtered by Department. 5) Optionally Format page > Canvas background to preview. 6) On the main chart: Format > General > Tooltips > Type = Report page, Page = "Tip - Dept". 7) Hide the tooltip page (right-click tab > Hide page).
**Alternative:** Drag extra measures into the visual's Tooltips well to enrich the default tooltip with no extra page.
**Version / licensing note:** from memory, unverified. Menu names (Page information, Canvas settings) change between builds.
**Edge cases:** If the tooltip page has no matching field, it shows unfiltered data. Tooltip pages are not interactive (see Q55, tooltip limitations) and are not available everywhere, e.g. dashboards (from memory, unverified).
**Likely follow-ups:** 1) *Can I click in a tooltip?* No (unverified). 2) *Why is it unfiltered?* Field mismatch.
**Common mistakes:** Forgetting to hide the page; making it too big; not putting the filtering field in the visual.

### Q27 ⭐⭐ 🟡 What do the Data, Display and Current page options of a bookmark do?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know what exactly a bookmark remembers and can control it.
**Say this in the interview:** "A bookmark saves a view. Display saves what is shown or hidden and spotlight/focus modes. Data saves the filters, slicers, sort order and drill location. Current page makes the bookmark open on the page where I saved it, instead of the page the user is currently on."
**Explain simply:**
- **Data:** filter and slicer selections, sort, drill state. Turn it off if the bookmark should only change visibility and leave user filters alone.
- **Display:** show/hide state from the Selection pane, spotlight and focus mode.
- **Current page:** if on, clicking the bookmark jumps to the saved page; if off, it stays on the page the user is on and applies the saved settings there.
- Right-click the bookmark (or click `...`) to switch each option off or on, in the Bookmarks pane.
**Example:** A "Chart view / Table view" toggle should use Display only, so it does not reset the department slicer the manager picked. Turn Data off.
**DAX / Steps (not run here):** View > Show panes > Bookmarks > Add > click `...` next to the bookmark > untick Data, Display or Current page as needed > Update.
**Alternative:** Use Page navigation buttons (no bookmarks) for pure page jumping.
**Version / licensing note:** from memory, unverified. Option names may be reworded in new builds.
**Edge cases:** A bookmark with Data on will overwrite a slicer the user just set. A visual added after the bookmark was saved may appear or behave unexpectedly until the bookmark is updated (see Q47 in this part).
**Likely follow-ups:** 1) *Which to turn off for a view toggle?* Data. 2) *Where do you update them?* Bookmarks pane > Update.
**Common mistakes:** Leaving Data on in a view switcher, so selections reset; forgetting to Update the bookmark after changing the layout.

### Q28 ⭐⭐ 🟡 How would you let users switch between a chart and a table on the same page using bookmarks?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can combine Selection pane, bookmarks and buttons into one working feature.
**Say this in the interview:** "I stack the chart and table in the same spot, make two bookmarks, one with the table hidden and one with the chart hidden, with Data turned off, then add two buttons and assign each one a bookmark action."
**Explain simply:**
- Put both visuals in the same area; name them in the Selection pane.
- **Bookmark 1 "Chart view":** hide the table (eye icon), add bookmark, rename it, set to Display only (Data off).
- **Bookmark 2 "Table view":** show the table, hide the chart, add bookmark, Data off.
- Add two buttons; for each select Format > Action > Type: Bookmark > pick the bookmark.
**Example:** A manager sees monthly exits as a chart and clicks "Table" to see the exact numbers per month, without losing the selected department.
**DAX / Steps (not run here):** 1) Insert > Buttons (blank or icons). 2) View > Selection pane: hide Table. 3) View > Bookmarks > Add > "Chart view". 4) Hide chart, show table > Add > "Table view". 5) For each, `...` > turn off Data. 6) Select button 1 > Format > Action > On > Type Bookmark > "Chart view"; same for button 2. 7) Test with Ctrl+click in Desktop.
**Alternative:** A field parameter or a switch measure to change the visual content (works for measures, not for chart-vs-table layout), or newer built-in visual-type approaches (unverified).
**Version / licensing note:** from memory, unverified. Buttons require Desktop; Ctrl+click activates actions while editing.
**Edge cases:** Bookmark-driven toggles do not work on dashboards or in some embedded/mobile cases (unverified). Hidden visuals are still filtered by slicers.
**Likely follow-ups:** 1) *Why turn Data off?* So slicers stay. 2) *Can the active button look highlighted?* Yes, with button states per bookmark (unverified).
**Common mistakes:** Forgetting to name visuals; saving bookmarks with Data on; testing without Ctrl+click.

### Q29 ⭐⭐ 🟡 The Drillthrough option does not appear when you right-click a visual. What do you check?
**Asked at:** commonly asked (no company-specific report found); the sources file notes drillthrough troubleshooting rules.
**What the interviewer is checking:** Whether you understand the matching rule behind drillthrough.
**Say this in the interview:** "The field in my drillthrough well must also exist in the source visual, as a plain field, not an aggregated one. I check the field names match, the visual's field is in Axis/Legend/Rows and I right-click an actual data point, not blank space."
**Explain simply:**
- Drillthrough fields on the target page (in the Drill through well) must be in the visual you right-click.
- The field must be a plain category (not summarised as Count or Sum) in the source visual.
- The target page must have the drillthrough field set up and not be only a tooltip page.
- You have to right-click a data point (a bar, a row), not an empty area or a card in some cases.
- Fields from unrelated tables or measures-only visuals may fail the match.
**Example:** The "Employee Detail" page has `Department` in its Drill-through well. A bar chart by `Division` has no Department, so nothing appears. Add Department (or use a matching field) and the option appears.
**DAX / Steps (not run here):** 1) Go to the target page > Visualizations > Build > Drill through well: confirm the field. 2) On the source visual, make sure the same field is in Axis / Legend / Rows. 3) Right-click a data point > Drill through > target page. 4) Check that the field is not summarised (Don't summarize).
**Alternative:** Add a page navigation button with a drillthrough action, or use a tooltip page instead.
**Version / licensing note:** from memory, unverified; Microsoft's drillthrough page was listed in the sources file but I could not re-read it here.
**Edge cases:** Selected multiple values across tables can disable it; a relationship to another table may be needed.
**Likely follow-ups:** 1) *Can drillthrough use a measure as filter?* Not directly. 2) *Cross-report?* Needs same workspace and matching names (Q49).
**Common mistakes:** Right-clicking a card; using different field names; keeping the field summarised.

### Q30 ⭐⭐ 🟡 How do you create a dynamic visual title that shows the department selected in a slicer?
**Asked at:** commonly asked (no company-specific report found); the sources file lists dynamic titles among HR build tasks.
**What the interviewer is checking:** Can you write a text measure and attach it to a title?
**Say this in the interview:** "I write a measure that builds the title text from the slicer selection with SELECTEDVALUE, then in the visual's Title > fx I pick that measure. If several departments are chosen, it falls back to 'All departments'."
**Explain simply:**
- A **measure** is a calculation that recalculates when slicers change. Text measures can feed titles.
- **SELECTEDVALUE** returns the value if exactly one is selected, otherwise a default you specify.
- Apply it: select visual > Format > General > **Title > Text > fx (conditional formatting) > Field value** > choose measure.
**Example:** Attrition table with Department slicer. Choose IT: title reads "Attrition - IT"; choose IT and HR together or nothing: "Attrition - All departments".
**Sample data:** Table `Employee`

| Department | Left |
|---|---|
| Sales | 1 |
| Sales | 0 |
| Sales | 0 |
| IT | 0 |
| IT | 1 |
| HR | 0 |
| HR | 0 |
| HR | 0 |

**DAX / Steps (not run here):**
```dax
Title Attrition =
"Attrition - " & SELECTEDVALUE ( Employee[Department], "All departments" )
```
Then Format > General > Title > Text > fx > Format style: Field value > Title Attrition.
**Alternative:** Show a list for multi-select: `CONCATENATEX ( VALUES ( Employee[Department] ), Employee[Department], ", " )`.
**Result:** reproduced with pandas (logic only): IT -> "Attrition - IT"; IT+HR -> "Attrition - All departments"; none -> "Attrition - All departments".
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Department":["Sales"]*3+["IT"]*2+["HR"]*3,"Left":[1,0,0,0,1,0,0,0]})
def title(sel):
    d = emp if not sel else emp[emp.Department.isin(sel)]
    u = d.Department.unique()
    return "Attrition - " + (u[0] if len(u)==1 else "All departments")
print(title(["IT"]), "|", title(["IT","HR"]), "|", title([]))
```
**Version / licensing note:** from memory, unverified. Field-value titles are available in current Desktop; DAX functions not checked against Microsoft Learn.
**Edge cases:** Multi-select returns the alternate result; add CONCATENATEX if you want the list. Cross-filtering from other visuals also changes the title.
**Likely follow-ups:** 1) *Date range in title?* Use MIN/MAX of the date column. 2) *Subtitle?* Same method.
**Common mistakes:** Forgetting the alternate result (returns blank); typing text in the title box rather than binding a measure.

### Q31 ⭐⭐ 🟡 How do you use a DAX measure to control conditional formatting colours (field value formatting)?
**Asked at:** commonly asked (no company-specific report found); the sources file lists conditional formatting as a live build task.
**What the interviewer is checking:** Whether you can go beyond the rules dialog to fully custom colours.
**Say this in the interview:** "I write a measure that returns a colour code as text, like a hex code, then in Format > Cell elements > Background colour > fx I choose Format style 'Field value' and pick that measure. The logic lives in DAX, so it can be as complex as I want."
**Explain simply:**
- **Field value formatting** means the colour itself comes from a measure.
- The measure returns a hex string such as `#2E8B57` (green) or a named colour.
- Use it for multi-condition rules (e.g. green at 95%+, amber 90-95%, red below).
- Handle blanks yourself; in DAX a blank compared with a number is treated as zero, which would turn a missing value red.
**Example:** Attendance % per employee: 97% green, 93% amber, 88% red, blank grey.
**Sample data:** Table `Attendance`

| Employee | Attendance |
|---|---|
| Asha | 0.97 |
| Ravi | 0.93 |
| Meena | 0.88 |
| Karan | (blank) |
| Divya | 0.95 |

**DAX / Steps (not run here):**
```dax
Attendance % = AVERAGE ( Attendance[Attendance] )
Attendance Colour =
VAR a = [Attendance %]
RETURN
    IF ( ISBLANK ( a ), "#BBBBBB",
        IF ( a >= 0.95, "#2E8B57",
            IF ( a >= 0.90, "#F0A500", "#C0392B" ) ) )
```
Steps: select the table/matrix > Format > Cell elements > turn on Background colour > fx > Format style = Field value > Based on field = Attendance Colour.
**Alternative:** Use **Rules** format style (no DAX) with ranges; simpler but less flexible; or use `SWITCH ( TRUE (), ... )` inside the measure.
**Result:** reproduced with pandas: Asha green, Ravi amber, Meena red, Karan grey, Divya green.
**Pandas check:**
```python
import pandas as pd
a = pd.DataFrame({"Employee":["Asha","Ravi","Meena","Karan","Divya"],"Attendance":[.97,.93,.88,None,.95]})
def col(x):   # mirrors the IF logic
    if pd.isna(x): return "grey"
    return "green" if x >= .95 else "amber" if x >= .90 else "red"
a["Colour"] = a.Attendance.map(col); print(a)
```
**Version / licensing note:** from memory, unverified. Field value format style exists in Desktop; Microsoft Learn conditional formatting page not re-read here.
**Edge cases:** Division results of 0/0 can give NaN; use DIVIDE. Totals row uses the measure at total level.
**Likely follow-ups:** 1) *Can it colour fonts and icons?* Yes, font colour and icons too. 2) *Why not hard-code?* Thresholds change.
**Common mistakes:** Not handling blanks; returning invalid colour text; formatting a field instead of a measure.

### Q32 ⭐⭐ 🟡 How would you build an attendance heat map for employees by day using a matrix?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Whether you can turn a matrix plus conditional formatting into a heat map.
**Say this in the interview:** "I use a matrix with employee on rows, day on columns and hours worked as values, then apply background colour conditional formatting, a gradient from light to dark, so low-attendance days stand out."
**Explain simply:**
- **Matrix:** a grid visual with rows and columns (like a pivot table).
- Rows = Employee, Columns = Day (in weekday order, use Sort by column as in Q25), Values = Hours (or a status code).
- Turn off subtotals if they distract. Apply **Cell elements > Background colour > fx > Gradient** (or Rules: 0 = red).
- A heat map is just numbers with colour showing the pattern.
**Example:** Asha was absent on Wednesday, Ravi worked a half day Tuesday and was absent Friday, Meena was absent Monday. Zero cells show red.
**Sample data:** Table `Attendance` (after pivot: hours per day)

| Employee | Mon | Tue | Wed | Thu | Fri |
|---|---|---|---|---|---|
| Asha | 8 | 8 | 0 | 8 | 7.5 |
| Meena | 0 | 8 | 8 | 8 | 8 |
| Ravi | 8 | 4 | 8 | 8 | 0 |

**DAX / Steps (not run here):**
```dax
Hours Worked = SUM ( Attendance[Hours] )
```
Matrix: Rows = Attendance[Employee], Columns = Calendar[DayName] (sorted by DayNum), Values = Hours Worked. Then Format > Cell elements > Background colour > fx > Gradient (Minimum red, Maximum green) or Rules.
**Alternative:** Show status text (P / A / L) using a measure with MAX of a status code and colour by a Field value measure (Q31).
**Result:** reproduced with pandas: the pivot table above (Asha 0 on Wed; Meena 0 on Mon; Ravi 0 on Fri, 4 on Tue).
**Pandas check:**
```python
import pandas as pd
w = pd.DataFrame({"Employee":["Asha","Meena","Ravi"],"Mon":[8,0,8],"Tue":[8,8,4],"Wed":[0,8,8],"Thu":[8,8,8],"Fri":[7.5,8,0]})
att = w.melt(id_vars="Employee", var_name="Day", value_name="Hours")   # long format, as stored in the model
print(att.pivot_table(index="Employee", columns="Day", values="Hours", aggfunc="sum")[["Mon","Tue","Wed","Thu","Fri"]])
```
**Version / licensing note:** from memory, unverified. Matrix and conditional formatting are in all Desktop versions.
**Edge cases:** A day with no row at all shows blank, not 0, unless Show items with no data is on. Gradient on subtotal cells distorts the scale.
**Likely follow-ups:** 1) *Weekday order?* Sort by day number. 2) *Many employees?* Group by department or use a slicer.
**Common mistakes:** Alphabetical day order; leaving subtotals on; treating blank as present.

### Q33 ⭐⭐ 🟡 A visual has no drill icons even though it uses several fields. Why, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Do you know that drill needs a hierarchy in the right well?
**Say this in the interview:** "Drill icons only appear when the visual has two or more fields stacked in a single drill-capable well, like Axis or Rows, or a hierarchy. Fields placed in Values or spread across wells don't create drill levels. I move them into Axis in order."
**Explain simply:**
- **Drill down** moves from a broad level to detail (Year > Quarter > Month) inside one visual.
- Fields stacked in the Axis well, or in Rows or Columns of a matrix, create levels in their order.
- Fields in Values, or one field in Axis and another in Legend, give no drill path.
- Some visuals (cards, gauges) never drill. Turn drill on from the icon (down arrow) in the visual header.
**Example:** A headcount chart has Department in Axis and Location in Legend: no drill. Put both Department and Location in Axis (Department on top): the arrows appear.
**DAX / Steps (not run here):** 1) Select visual > Build pane. 2) Drag both fields into the Axis well, order top-to-bottom = broad-to-detail. 3) Check the icons in the visual header (drill up, drill down, go to next level, expand). 4) For reuse, create a hierarchy in the Model/Data view (right-click field > Create hierarchy).
**Alternative:** Use drillthrough to a detail page instead of drilling within the visual (Q8 and Q29).
**Version / licensing note:** from memory, unverified; Microsoft's drill mode page was not re-read here.
**Edge cases:** Date hierarchy is automatic if Auto date/time is on; turning it off removes it. The Drill icons may be hidden if the report author turned off the visual header.
**Likely follow-ups:** 1) *Difference between next level and expand all?* See Q50. 2) *Does drill filter other visuals?* Not by default (Q37).
**Common mistakes:** Putting the second field in Legend; expecting drill on a card; wrong order in the Axis well.

### Q34 ⭐⭐ 🟡 When would you use a combo chart (line and clustered column), and what is the risk of a dual axis?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Chart judgement: pairing a volume with a rate, and knowing the dual-axis trap.
**Say this in the interview:** "I use a combo chart when I want to show a count and a rate on the same time axis, like exits as columns and attrition % as a line. The risk is a dual axis: the two scales can be stretched to make a false correlation, so I label both axes clearly or avoid it."
**Explain simply:**
- Columns suit amounts (exits, hires). A line suits a rate or trend (attrition %).
- A **dual axis** means a left scale for columns and a right scale for the line, because their units differ.
- Risk: you can choose axis ranges so the line seems to follow or diverge from columns. Viewers misread it.
- Mitigate: start the column axis at zero, label axes, or use two aligned charts.
**Example:** Jan-Mar exits 8, 6, 12 on headcount 400, 410, 405 give attrition 2.00%, 1.46%, 2.96%. Columns show exits, the line shows those percentages.
**Sample data:** Table `Monthly`

| Month | Exits | Headcount | Attrition % |
|---|---|---|---|
| Jan | 8 | 400 | 2.00 |
| Feb | 6 | 410 | 1.46 |
| Mar | 12 | 405 | 2.96 |

**DAX / Steps (not run here):**
```dax
Attrition % = DIVIDE ( [Exits], [Headcount] )
```
Visualizations > Line and clustered column chart; Column y-axis = Exits, Line y-axis = Attrition %.
**Alternative:** Two small charts stacked with the same x-axis, no dual-axis ambiguity.
**Result:** reproduced with pandas: 2.00%, 1.46%, 2.96%.
**Pandas check:**
```python
import pandas as pd
c = pd.DataFrame({"Exits":[8,6,12],"Headcount":[400,410,405]})
c["Attr%"] = (c.Exits/c.Headcount*100).round(2); print(c)
```
**Version / licensing note:** from memory, unverified.
**Edge cases:** Different scales mislead; a line across categories (not time) implies a trend that does not exist. Use DIVIDE to avoid divide-by-zero.
**Likely follow-ups:** 1) *Alternatives to dual axis?* Small multiples or two charts. 2) *Can the axes be synced?* Only manually.
**Common mistakes:** Truncated axes; using it for unrelated measures; hiding the secondary axis labels.

### Q35 ⭐⭐ 🟡 How would you let a manager click a department in a chart and see the list of its employees on another page?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know drillthrough in practice.
**Say this in the interview:** "I build an Employee Detail page, put Department in the Drill through well, and add a table of employees. The manager right-clicks a department bar and chooses Drill through > Employee Detail, and the table shows only that department."
**Explain simply:**
- **Drillthrough** jumps to another page filtered by what you right-clicked; it is different from drill down (Q33).
- Target page: add a **Department** field to the Drill through well; Power BI adds a back button automatically.
- Add a table with name, role, joining date, manager.
- Optionally add a button with a drillthrough action so users see a visible cue.
**Example:** Sales has 3 employees in the sample; right-click the Sales bar and the detail page lists those three.
**Sample data:** Table `Employee`

| Employee | Department |
|---|---|
| Asha | Sales |
| Ravi | Sales |
| Kiran | Sales |
| Meena | IT |
| Divya | HR |

**DAX / Steps (not run here):** 1) New page "Employee Detail". 2) Build > Drill through well > drag Department. 3) Add a table: Employee, Role, Join date. 4) Back on the chart: right-click Sales bar > Drill through > Employee Detail. 5) Optionally Insert > Buttons > Back/Drillthrough action.
**Alternative:** A tooltip page for a quick hover preview, or a table visual on the same page filtered by cross-filtering.
**Result:** reproduced with pandas: Sales -> Asha, Ravi, Kiran.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Employee":["Asha","Ravi","Kiran","Meena","Divya"],"Department":["Sales"]*3+["IT","HR"]})
print(emp[emp.Department=="Sales"].Employee.tolist())
```
**Version / licensing note:** from memory, unverified.
**Edge cases:** If the source visual has no Department field the option is missing (Q29). Right-click an actual bar. Keep-all-filters behaviour is in Q48.
**Likely follow-ups:** 1) *Row-level security?* RLS still limits the visible employees. 2) *Hide the page?* Yes, hide it from tabs.
**Common mistakes:** Forgetting to put the field in the well; leaving the detail page visible and confusing.

### Q36 ⭐⭐ 🟡 Which visuals would you use to show attrition by department and by tenure band, and why?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Chart choice and whether you compare rates, not raw counts.
**Say this in the interview:** "A bar chart of attrition rate by department, sorted high to low, a column chart by tenure band in natural order, and a matrix heat map of department by tenure to find hot spots. I show rate rather than count so a large team does not look worse just by size."
**Explain simply:**
- **Attrition rate** = leavers divided by employees (here, simply the share who left; a real report uses average headcount).
- Bars for categories that have long names (departments) and are ranked.
- Columns for ordered bands (<1y, 1-3y, 3y+) so the left-to-right order is meaningful.
- A matrix with conditional colour for the department-by-tenure combination.
**Example:** 15 employees, 5 left (33.3%). Sales 50%, IT 20%, HR 25%; by tenure, under 1 year 75%, 1-3 years 40%, 3+ years 0%.
**Sample data:** Table `Employee` (15 rows, summarised)

| Dept | Employees | Left | Rate % |
|---|---|---|---|
| Sales | 6 | 3 | 50.0 |
| IT | 5 | 1 | 20.0 |
| HR | 4 | 1 | 25.0 |

| Tenure | Employees | Left | Rate % |
|---|---|---|---|
| <1y | 4 | 3 | 75.0 |
| 1-3y | 5 | 2 | 40.0 |
| 3y+ | 6 | 0 | 0.0 |

**DAX / Steps (not run here):**
```dax
Attrition Rate = DIVIDE ( SUM ( Employee[Left] ), COUNTROWS ( Employee ) )
```
Bar chart: Axis = Dept; column chart: Axis = Tenure band (sorted by band order); Matrix: Rows = Dept, Columns = Tenure band, Values = Attrition Rate with Background colour gradient.
**Alternative:** Treemap or decomposition tree (Part 11) for exploration; but ranked bars are more precise.
**Result:** reproduced with pandas: the two tables above; overall 33.3%.
**Pandas check:**
```python
import pandas as pd
rows = [("Sales","<1y",1)]*2 + [("Sales","1-3y",1),("Sales","1-3y",0)] + [("Sales","3y+",0)]*2
rows += [("IT","<1y",1)] + [("IT","1-3y",0)]*2 + [("IT","3y+",0)]*2
rows += [("HR","<1y",0),("HR","1-3y",1)] + [("HR","3y+",0)]*2     # 15 employees, 5 left
e = pd.DataFrame(rows, columns=["Dept","Tenure","Left"])
for by in ("Dept","Tenure"):
    g = e.groupby(by).Left.agg(["sum","count"]); g["rate%"] = (g["sum"]/g["count"]*100).round(1); print(g)
print(round(100*e.Left.mean(),1))   # 33.3
```
**Version / licensing note:** from memory, unverified. Sample is tiny and invented for illustration.
**Edge cases:** Tiny groups give extreme rates (an HR cell with 1 person shows 100%); show counts alongside. Use average headcount for a proper annual rate.
**Likely follow-ups:** 1) *Why not pie?* Too many slices; hard to compare. 2) *Tenure bands?* Create with a calculated column or SWITCH.
**Common mistakes:** Plotting counts; unordered tenure bands; ignoring small samples.

### Q37 ⭐⭐ 🟡 By default, does drilling down in one visual change the other visuals on the page, and how can you change that?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know drill down is local to the visual, and how interactions work.
**Say this in the interview:** "No, drilling down only changes that visual; other visuals don't change. If I want other visuals to react, I select a data point (cross-filtering) or use Edit interactions, or use drillthrough to move to a filtered page."
**Explain simply:**
- **Drill down** just changes the level shown inside the visual, for example Year to Quarter. It does not filter anything.
- Clicking a bar or a point (not drilling) cross-filters other visuals by default.
- To change how visuals react: select the source visual > **Format tab > Edit interactions** and choose Filter, Highlight or None on each target.
- Drillthrough or bookmarks can pass the context to a different page.
**Example:** Drilling a headcount chart from Year to Quarter leaves the attrition card unchanged. Clicking the 2025 bar, on the other hand, filters the card to 2025.
**DAX / Steps (not run here):** Format tab > Edit interactions > click the filter/highlight/none icon above each other visual.
**Alternative:** Use the "Expand all down one level" or "Go to next level" combos and select points for cross-filtering (see Q50).
**Version / licensing note:** from memory, unverified. The sources file lists Microsoft's "Change how visuals interact" and "Use drill mode" pages, which I could not re-read here.
**Edge cases:** Interactions are per page. Some visuals (cards) support Highlight poorly.
**Likely follow-ups:** 1) *Difference between filter and highlight?* Filter removes other data; highlight dims it. 2) *Turn off a slicer on a visual?* Edit interactions > None (Q9).
**Common mistakes:** Expecting drill down to filter the page; forgetting that selecting a point does.

### Q38 ⭐ 🟢 What is a scatter chart, and when would you use it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the chart for relationships between two numbers.
**Say this in the interview:** "A scatter chart plots each item as a dot using two numbers, one on each axis. I use it to see whether two measures move together, for example tenure versus salary, and to spot outliers."
**Explain simply:**
- Each dot is one item (an employee or department); X and Y are numbers.
- Optional third value: dot size (Size well) and colour (Legend) for groups.
- Needs the **Details** well set (or dots collapse into a single total dot).
- Looks at relationship, not cause.
**Example:** Six employees: tenure 1, 2, 3, 5, 8, 10 years and salary 4.0, 4.5, 6.0, 7.2, 9.0, 9.8 lakh. The dots rise steadily; correlation 0.988.
**Sample data:** Table `Staff`

| Employee | Tenure (yrs) | Salary (lakh) |
|---|---|---|
| A | 1 | 4.0 |
| B | 2 | 4.5 |
| C | 3 | 6.0 |
| D | 5 | 7.2 |
| E | 8 | 9.0 |
| F | 10 | 9.8 |

**DAX / Steps (not run here):** Visualizations > Scatter chart; X Axis = Tenure, Y Axis = Salary, Values (Details) = Employee. Optionally Size = Headcount.
**Alternative:** A line chart if X is time; a table of correlation values.
**Result:** reproduced with pandas: correlation 0.988.
**Pandas check:**
```python
import pandas as pd
sc = pd.DataFrame({"Tenure":[1,2,3,5,8,10],"Salary":[4.0,4.5,6.0,7.2,9.0,9.8]})
print(round(sc.Tenure.corr(sc.Salary), 3))   # 0.988
```
**Version / licensing note:** from memory, unverified.
**Edge cases:** Without a Details field you see one dot; outliers stretch the axes; correlation is not causation.
**Likely follow-ups:** 1) *Bubble chart?* A scatter with the Size well. 2) *Play axis?* Animates a time field.
**Common mistakes:** Forgetting the Details field; using categories on the axes.

### Q39 ⭐ 🟢 What is the difference between a line chart and an area chart?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Chart-type judgement.
**Say this in the interview:** "Both show a trend over time. A line chart is best for comparing several series or reading exact movement. An area chart fills under the line, so it emphasises volume or total, and stacked area shows how parts add up to a total."
**Explain simply:**
- Line: clean, good for many series, and for small changes.
- Area: filled, good for one or two series and the sense of size; stacked area shows composition.
- Overlapping filled areas hide each other; avoid unstacked areas with several series.
- Start area charts at zero, because the fill implies size.
**Example:** Monthly headcount 410 to 450: a line shows the climb; a stacked area by department shows how each team contributes to the 450.
**DAX / Steps (not run here):** Visualizations > Line chart or Area chart (or Stacked area); Axis = Month, Values = Headcount, Legend = Department.
**Alternative:** Column chart for discrete month snapshots.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Gaps in dates; unsorted axes; negative values in area charts look odd.
**Likely follow-ups:** 1) *When avoid area?* Many series. 2) *Continuous axis?* Use a date axis type.
**Common mistakes:** Truncated area baselines; unstacked overlapping areas.

### Q40 ⭐ 🟢 How do you lock or hide a filter in the Filters pane?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can control what report readers can change.
**Say this in the interview:** "In Desktop's Filters pane each filter has a lock icon and an eye icon. Lock stops viewers from changing it, hide removes it from the pane in the published report but it still applies."
**Explain simply:**
- **Lock:** viewers see the filter but can't edit it.
- **Hide:** viewers don't see it, yet it still filters the data.
- Set at visual, page or report level (Q3).
- Hidden filters are not security; they only hide, so use row-level security for confidentiality.
**Example:** A report-level filter "Employment status = Active" is locked and hidden so readers can't remove it and don't see clutter.
**DAX / Steps (not run here):** Desktop > open Filters pane > hover over a filter card > click the lock icon (lock) or the eye icon (hide). Alternatively View tab > Show panes > Filters.
**Alternative:** Hide the whole Filters pane (Format/Report settings) or use row-level security for real restrictions.
**Version / licensing note:** from memory, unverified. The sources file cites Microsoft's "Format filters in reports" page which I could not re-read here.
**Edge cases:** A hidden filter is still visible in Desktop edit mode. Users with edit rights can unhide it.
**Likely follow-ups:** 1) *Is hiding secure?* No; use RLS. 2) *Filter levels?* Visual, page, report.
**Common mistakes:** Treating hide as security; hiding a filter and forgetting it.

### Q41 ⭐ 🟢 What are Spotlight and Focus mode in Power BI?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the simple viewing helpers.
**Say this in the interview:** "Focus mode expands one visual to fill the screen so you can inspect it. Spotlight dims the other visuals so one stands out on the page, handy in presentations."
**Explain simply:**
- **Focus mode:** hover over a visual > the Focus mode icon (expanding arrows); press Back to report to leave.
- **Spotlight:** `...` menu on a visual > Spotlight; other visuals fade.
- Both can be saved in a bookmark (Display option) to create guided stories.
- Neither changes the data or the layout permanently.
**Example:** In a review meeting, spotlight the attrition chart while the rest of the page is dimmed; use Focus mode to read all its labels.
**DAX / Steps (not run here):** Hover visual > Focus mode icon. Or visual `...` > Spotlight. Clear by clicking outside or choosing Remove spotlight.
**Alternative:** Create a dedicated page for one visual.
**Version / licensing note:** from memory, unverified; both are viewing features available in Desktop and Service.
**Edge cases:** Spotlight state is saved with a bookmark that has Display on (Q27).
**Likely follow-ups:** 1) *Can readers use it?* Yes, in Reading view. 2) *Does Focus change interactions?* No.
**Common mistakes:** Confusing Focus mode with a full-screen mode of the whole report.

### Q42 ⭐ 🟢 What are custom visuals, where do you get them, and what should you check before using one?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the built-in visuals are not the limit, and do you think about data safety before importing something?
**Say this in the interview:** "Custom visuals are extra chart types built by Microsoft partners or the community. I get them from AppSource through the Visualizations pane, or from a .pbiviz file. Before using one I check the publisher, whether it is certified, what it does with the data, and whether my organisation allows it."
**Explain simply:**
- A visual is a chart or table on the report page. Custom visuals add types that are not in the box (for example a Gantt chart or a Sankey flow diagram).
- Where from: Visualizations pane > three dots (**Get more visuals**) opens AppSource, Microsoft's app marketplace; a developer can also hand you a **.pbiviz** file (the visual's package); some companies keep an approved list in an organisational store.
- Check: (1) publisher and reviews; (2) a **certified** badge, which means Microsoft reviewed the code (certified visuals are also the ones that support extras like exporting to PowerPoint); (3) whether it sends data outside Power BI; (4) does it still get updates; (5) does it work in the Service and on mobile; (6) is it free or paid.
- Admins can restrict which visuals users may import.
**Example:** An HR analyst wants a Sankey (flow) chart of how 120 candidates move from "Applied" to "Hired". She picks a certified Sankey from AppSource, tests it on dummy data first, then confirms with IT that it is allowed.
**DAX / Steps (not run here):** 1) Report view > Visualizations pane > three dots > **Get more visuals**. 2) Search, check the publisher and the certified badge, **Add**. 3) Or three dots > **Import a visual from a file** for a .pbiviz. 4) Test on non-sensitive data.
**Alternative:** Try to build it with a built-in visual first (a stacked bar often works); fewer dependencies, no approval needed.
**Version / licensing note:** from memory, unverified (learn.microsoft.com was unreachable from this session, ENOTFOUND): menu names, the certified-visual benefits and the admin controls should be rechecked on Microsoft Learn.
**Edge cases:** Uncertified visuals may behave differently on refresh, export or mobile; a visual that disappears from the store can break old reports.
**Likely follow-ups:** 1) *What is a certified visual?* One Microsoft has code-reviewed against its requirements. 2) *Can you build your own?* Yes, developers use the Power BI visuals SDK (from memory).
**Common mistakes:** Importing random .pbiviz files from the internet; putting confidential employee data into an unchecked visual.

### Q43 ⭐ 🟢 What is the Mobile layout view in Power BI Desktop, and when do you build one?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you think about people who read the report on a phone?
**Say this in the interview:** "Mobile layout is a second, portrait (tall and narrow) arrangement of the same report page, built for the Power BI mobile app. I build it when managers or field teams will read the report on their phones."
**Explain simply:**
- The normal page is landscape (wide). On a phone it is tiny, so you must pinch and scroll.
- In Mobile layout you drag the visuals you want onto a phone-shaped canvas and resize them. Same data, same visuals, just a different arrangement per page.
- You only place the key ones (for example 3 KPI cards and one trend chart). Visuals you do not place are simply absent on the phone.
- Pages with no mobile layout still open on the phone, as the shrunken landscape page.
**Example:** A branch HR head checks attendance on her phone each morning. The mobile layout shows "Present today: 142", "Absent: 8" and one chart of the last 7 days; the 12 detail visuals stay on the desktop page only.
**DAX / Steps (not run here):** 1) Report view > **View** tab > **Mobile layout**. 2) From the Page visuals pane drag visuals onto the phone canvas. 3) Resize and align on the grid. 4) Return via View > Page layout (or the same toggle).
**Alternative:** Design a single simple page (few big cards) that works on both screen shapes; less work, less control.
**Version / licensing note:** from memory, unverified (learn.microsoft.com unreachable): the Mobile layout ribbon button, and whether viewers need the Power BI mobile app and a licence, should be rechecked.
**Edge cases:** Slicers and filters can be placed too; text-heavy tables read badly on a phone; a new visual added later to the desktop page does not appear in the mobile layout automatically.
**Likely follow-ups:** 1) *Do you build it for every page?* Only pages people will open on phones. 2) *Does it change the data?* No, only the layout.
**Common mistakes:** Cramming the whole desktop page in; forgetting to update the mobile layout after adding visuals.

### Q44 ⭐ 🟢 How do you make a Power BI report more accessible (alt text, tab order, colour choices)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you design for colour-blind users, screen-reader users and keyboard-only users?
**Say this in the interview:** "I add alt text to meaningful visuals, set a sensible tab order for keyboard users, use colours with strong contrast and never rely on colour alone, and give every visual a clear title."
**Explain simply:**
- **Alt text** (alternative text): a short description a screen reader (software that reads the page aloud) speaks for a visual. Written in the visual's Format pane under General.
- **Tab order**: the order in which the Tab key moves between visuals. Set it to follow the reading order (top-left to bottom-right), and hide purely decorative items from it.
- **Colour**: good contrast between text and background; do not use red vs green alone (about 1 in 12 men are red-green colour blind, a widely quoted figure, unverified here); add labels, icons or patterns.
- Other basics: clear titles, readable font sizes, avoid flashing or heavy animation, and use a theme with accessible colours.
**Example:** An attrition chart shows "Resigned" in red and "Retained" in green. The fix: labelled bars, and alt text "Attrition by department: IT highest at 50 per cent in Q1".
**DAX / Steps (not run here):** 1) Select a visual > Visualizations pane > **Format** > **General** > **Alt text**, type a description. 2) View tab > **Selection** pane > use its tab-order options to reorder visuals. 3) View tab > **Themes** > pick a high-contrast or colour-blind-friendly theme. 4) Test by pressing Tab through the page.
**Alternative:** Alt-text can also carry a dynamic value in some builds (a measure-driven alt text); treat as a nice-to-have (from memory, unverified).
**Version / licensing note:** from memory, unverified (learn.microsoft.com unreachable): exact pane names and keyboard shortcuts move between releases.
**Edge cases:** Decorative shapes should not carry alt text; a very long alt text is tiresome to hear; colour-only conditional formatting needs a text or icon backup.
**Likely follow-ups:** 1) *How do you test it?* Tab through the whole page without a mouse and listen with a screen reader. 2) *Is accessibility compulsory?* Often a corporate or legal requirement.
**Common mistakes:** Alt text like "chart"; random tab order; red/green status with no labels.

### Q45 ⭐ 🟡 What is a decomposition tree, and when is it useful?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you explain a "why is this number high?" tool and know its limits?
**Say this in the interview:** "A decomposition tree takes one number and splits it, level by level, by categories I choose, so I can click through to the part that explains it. It is useful when someone asks 'where is this coming from?' and I do not know the path in advance."
**Explain simply:**
- Visual with one **Analyze** field (a measure such as Headcount) and several **Explain by** fields (Dept, Location, Grade).
- You click the **+** beside a bar to pick the next split. You choose the order yourself, or choose an AI option ("high value" or "low value") so the visual picks the most influential field.
- It is for exploring, not for a fixed report layout; it uses plain sums and counts, not complex ranking.
**Example:** Headcount 9. Split by Department: Sales 3, Finance 2, IT 2, Ops 2. Click Sales and split by Location: Hyderabad 2, Bengaluru 1.
**Sample data:** Employees table (active on 31-Mar-2025), counts as printed in the Pandas check.
**DAX / Steps (not run here):** Measure used: `Headcount` (defined in Q51). Steps: 1) Visualizations > **Decomposition tree**. 2) Drag Headcount into **Analyze**. 3) Drag Dept, Location, Grade into **Explain by**. 4) Click the + under the root bar, pick Dept; click a bar and pick Location.
**Alternative:** A matrix with Dept and Location as row levels shows the same split in a fixed layout.
**Result:** Reproduced with pandas (see below); not run in Power BI.
**Pandas check:** (setup block from Q51)
```python
exec(open("setup.py").read())          # Q51 setup: emp, start, end, active_on
act = active_on(end)
print("Total headcount:", len(act)); print(act.groupby("Dept").size().sort_values(ascending=False))
print(act[act.Dept=="Sales"].groupby("Location").size())
```
Output: Total headcount 9; Sales 3, Finance 2, IT 2, Ops 2; Sales by Location: Bengaluru 1, Hyderabad 2.
**Version / licensing note:** from memory, unverified (learn.microsoft.com unreachable): whether the AI splits need a particular licence or Service-only features.
**Edge cases:** Blank categories appear as (Blank) branches; very many categories get truncated; whether it can drive other visuals or drillthrough the way a bar chart does should be tested in your build (from memory, unverified).
**Likely follow-ups:** 1) *Decomposition tree vs key influencers?* The tree lets you walk the path; key influencers ranks drivers statistically. 2) *Can users pick the order?* Yes, with the +.
**Common mistakes:** Using it as a dashboard centrepiece for fixed numbers; adding a measure to Explain by.

### Q46 ⭐ 🟡 What is the difference between a report bookmark and a personal bookmark?
**Asked at:** commonly asked (no company-specific report found); bookmarks appear in fresher Power BI question lists per research/Book04_Part06_sources.md.
**What the interviewer is checking:** Do you know who creates and who sees each kind?
**Say this in the interview:** "A report bookmark is created by the report author and everyone who opens the report sees it. A personal bookmark is created by a viewer in the Power BI Service for their own use, and only they see it."
**Explain simply:**
- A **bookmark** saves a snapshot of a page: filters, slicer choices, which visuals are visible, sort order, drill position (the exact list depends on the options you tick).
- **Report bookmark:** author builds it in Desktop (or Service edit mode), it sits in the Bookmarks pane and can be wired to buttons for navigation or "toggle a view".
- **Personal bookmark:** a reader in the Service saves their favourite filtered view (for example "my team only"); it is not shared and cannot be attached to buttons.
- Personal bookmarks are a Service feature; Desktop authors make report bookmarks.
**Example:** The author makes two report bookmarks, "Headcount view" and "Attrition view", behind two buttons. A manager saves her own "Hyderabad, Sales" slicer state as a personal bookmark.
**DAX / Steps (not run here):** Author: View tab > **Bookmarks** pane > set the page the way you want > **Add**; rename; use the three dots to **Update** or choose Data / Display / Current page options. Viewer in the Service: open report > **Bookmarks** > **Add a personal bookmark**.
**Alternative:** Reader-side alternative: browser favourite of a URL with filters, or "Subscribe" to a filtered email; both have different limits.
**Version / licensing note:** The existence of personal vs report bookmarks and the Data/Display/Current page options comes from the Microsoft Learn bookmarks page as summarised in research/Book04_Part06_sources.md (fetched in an earlier research pass, not re-fetched here). The exact Service menu wording and any licence needed for personal bookmarks: from memory, unverified.
**Edge cases:** A reader opening the report can see only report bookmarks the author published; deleting a field in the model can break bookmarks that used it.
**Likely follow-ups:** 1) *Can personal bookmarks be set as the default view?* In the Service you can mark one as the default (from memory, unverified). 2) *Bookmarks vs drillthrough?* A bookmark restores a saved state; drillthrough passes a selected item to a detail page.
**Common mistakes:** Building navigation with personal bookmarks; forgetting to update a bookmark after changing a slicer.

### Q47 ⭐ 🟡 What are the limitations of bookmarks (for example, visual positions and slicers added later)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Have you been bitten by bookmarks in practice, and do you know the workarounds?
**Say this in the interview:** "A bookmark only remembers what existed and what was ticked when I saved it. Visuals or slicers I add later are not part of it until I update the bookmark, and it does not keep layout changes such as moved visuals. So I finish the design first, then create or refresh the bookmarks."
**Explain simply:**
- A bookmark stores a **state** (filters, slicers, visibility from the Selection pane, sort, drill, spotlight/focus) per the Data / Display / Current page options.
- New visuals or slicers added after saving show in their normal state when the bookmark is applied, so the page can look inconsistent. Fix: use **Update** on each bookmark.
- Moved or resized visuals are not a bookmark feature; the usual trick is to stack visuals and show or hide them through the Selection pane (the premise about positions: from memory, unverified; confirm in Desktop).
- Data-heavy: a bookmark does not hold data, only the state; if a field is renamed or removed the bookmark can break.
- Turn **Data** off for bookmarks that should keep the reader's current slicer choice.
**Example:** You create "Overview" with a Dept slicer. A month later you add a Location slicer. Clicking "Overview" now leaves Location at whatever the reader last chose; you must update the bookmark.
**DAX / Steps (not run here):** View tab > **Bookmarks** > select the bookmark > make the page the way it should be > three dots > **Update**. Tick or untick **Data**, **Display**, **Current page** in the same menu.
**Alternative:** Use a button with a page navigation action for simple page switching; it does not store filter state.
**Version / licensing note:** The limitations list comes from the Microsoft Learn bookmarks page as summarised in research/Book04_Part06_sources.md (not re-fetched here, so I cannot quote exact wording); the visual-position point is from memory, unverified.
**Edge cases:** Personal bookmarks have the same limits; bookmarks with hidden visuals still run those visuals' queries, which can slow a page (from memory).
**Likely follow-ups:** 1) *How do you toggle two visuals?* Two bookmarks that show or hide each through the Selection pane, wired to buttons. 2) *How do you test?* Click every bookmark after each design change.
**Common mistakes:** Making bookmarks before the layout is final; leaving Data on when navigation bookmarks should not reset slicers.

### Q48 ⭐ 🟡 What does Keep all filters do on a drill-through page?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know which filters travel to the detail page?
**Say this in the interview:** "With Keep all filters On, the detail page receives the selected item and also every other filter from the source page, such as slicers. Off passes only the drill-through field values."
**Explain simply:**
- **Drillthrough**: right-click an item on one page and jump to a detail page about that item (for example one department's employee list).
- The drill-through field (Dept) always filters the detail page.
- **Keep all filters**: a toggle in the drillthrough well. On: the other filters in play on the source visual or page travel too. Off: they do not.
- Choose by what the reader expects: a detail page that must match the source numbers wants On.
**Example:** Source page has Location = Hyderabad. The user drills on Dept = Sales. On: Sales in Hyderabad (2 employees). Off: all Sales (3).
**DAX / Steps (not run here):** Detail page > Build/Visualizations pane > drag Dept into **Drill through** well > toggle **Keep all filters** On or Off > the page gets a Back button.
**Alternative:** Leave the toggle On and add a text box or dynamic title showing the carried filters so the reader sees them.
**Result:** Reproduced with pandas (below); not run in Power BI.
**Pandas check:** (setup block from Q51)
```python
exec(open("setup.py").read())
act = active_on(end); src = act[act.Location == "Hyderabad"]
print("ON :", (src.Dept == "Sales").sum()); print("OFF:", (act.Dept == "Sales").sum())
```
Output: `ON : 2` and `OFF: 3`.
**Version / licensing note:** The toggle is a known Desktop setting but the fetched Microsoft drillthrough page (per research/Book04_Part06_sources.md) did not describe it; the behaviour above is from memory, unverified.
**Edge cases:** The drill-through field must be in the source visual and not aggregated; if filters conflict (Location filter on a visual that excludes the selected item) the page can come up empty.
**Likely follow-ups:** 1) *Default?* I believe On, but verify in your build (from memory, unverified). 2) *Drill-through vs drill down?* Drill down stays on the same visual; drillthrough opens another page.
**Common mistakes:** Not noticing the detail page is also filtered by a hidden slicer; using Off then wondering why totals differ.

### Q49 ⭐ 🟡 What are the requirements for cross-report drillthrough?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it is a set-up feature with strict matching rules, and that it is Service-side?
**Say this in the interview:** "The target report must allow cross-report drillthrough, and the drillthrough field must have the same table and column names and data types in both reports. It works in the Power BI Service, not in Desktop, and the reports need to be in the same workspace."
**Explain simply:**
- **Cross-report drillthrough**: right-click an item in report A and land on a page in report B (for example a summary report linking to a separate employee-detail report).
- Requirements, per research/Book04_Part06_sources.md (from the Microsoft drillthrough page, not re-fetched here): same workspace, matching field names and types, Service only.
- Set-up, from memory (unverified): target page marked as drillthrough with the cross-report option On; source report allows drillthrough to other reports in its settings.
- The user needs permission on both reports.
**Example:** "HR Summary" report has Dept bars. "Employee Detail" report has a page with Dept as drillthrough field. Both sit in the HR workspace. Right-click Sales > Drill through > Employee Detail.
**DAX / Steps (not run here):** 1) Target report page > Page information / drillthrough pane > add Dept > turn on **Cross-report**. 2) Source report > File > Options and settings > Options > Report settings > allow visuals to use drillthrough targets from other reports. 3) Publish both to one workspace; test in the Service.
**Alternative:** One report with a drillthrough page, or a button with a URL carrying filters (a bookmark/filter URL) for different workspaces.
**Version / licensing note:** Requirements above come from the sources file; menu paths and licence needs: from memory, unverified (learn.microsoft.com unreachable, ENOTFOUND).
**Edge cases:** Rename Dept to Department in one report and the link silently stops working; a numeric vs text type mismatch breaks it too.
**Likely follow-ups:** 1) *Does it work in Desktop?* Not per the sources (Service only). 2) *Why not merge reports?* Different owners or sizes.
**Common mistakes:** Mismatched column names; testing in Desktop; forgetting to publish the target first.

### Q50 ⭐ 🟡 What is the difference between Go to the next level and Expand all down one level in a hierarchy visual?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you tell the two drill icons apart by result?
**Say this in the interview:** "Go to the next level replaces the current level with the next one for all items together. Expand all down one level keeps the current level and adds the next one underneath, so I see department and location combined."
**Explain simply:**
- A **hierarchy** is an ordered set of fields, such as Department > Location > Employee. Drill icons appear at the top of the visual.
- **Drill down (single arrow, drill mode on)**: click one bar to go into that item only.
- **Go to the next level (double down arrow)**: moves every item to the next level at once; Dept bars become Location bars (totals for all depts together).
- **Expand all down one level (fork icon)**: shows both levels, such as "Sales Hyderabad" and "Sales Bengaluru".
**Example:** Active headcount 9.
**Sample data:** Employees table (Q51); output below.
**DAX / Steps (not run here):** Build visual with Dept > Location in the Axis well (or a hierarchy) > use the icons at the top-right of the visual: single arrow (drill mode), double arrow (next level), fork (expand).
**Alternative:** A matrix with Dept and Location as rows gives the expanded view with +/- buttons.
**Result:** Reproduced with pandas: next level gives Bengaluru 5, Hyderabad 4; expand shows Finance (Bng 1, Hyd 1), IT (Bng 2), Ops (Bng 1, Hyd 1), Sales (Bng 1, Hyd 2).
**Pandas check:** (setup block from Q51)
```python
exec(open("setup.py").read())
act = active_on(end)
print(act.groupby("Location").size().to_string()); print(act.groupby(["Dept","Location"]).size().to_string())
```
**Version / licensing note:** Icon behaviour per Microsoft's "Use drill mode" page as listed in research/Book04_Part06_sources.md (not re-fetched); icon shapes from memory, unverified.
**Edge cases:** Drilling does not filter other visuals by default; icons vanish if only one field is in the axis.
**Likely follow-ups:** 1) *Drill-through vs drill-down?* Different page vs same visual. 2) *Why no icons?* Only one field in axis or visual type has no drill.
**Common mistakes:** Mixing up the two icons; expecting drill to filter the whole page.

### Q51 ⭐ 🟡 What are field parameters, and how would you let users choose which measure a chart shows?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the modern, no-code way to let a user switch measures or axes?
**Say this in the interview:** "A field parameter is a small generated table whose rows are fields or measures. I put it on a slicer so the user picks, and I put the same parameter on the chart so the chart switches to the chosen measure."
**Explain simply:**
- Old way: a disconnected table plus a SWITCH measure. New way: Modeling tab > New parameter > Fields, then tick the measures.
- Power BI writes a calculated table (a table made by a DAX formula) with each item's display name, a reference to the field, and an order number.
- Put the parameter in a slicer and in the chart's Values (or Axis) well; the chart follows the selection.
- Limits: parameters cannot be used as a drillthrough or tooltip field (see Q59).
**Example:** One bar chart by department; the user chooses Headcount, Attrition % or Average tenure.
**Sample data:** Employees (active status as of 31-Mar-2025, quarter = Jan-Mar 2025).

| EmpID | Dept | Location | Grade | JoinDate | ExitDate |
|---|---|---|---|---|---|
| E01 | Sales | Hyderabad | G1 | 2022-06-01 | |
| E02 | Sales | Bengaluru | G2 | 2023-01-15 | 2025-02-10 |
| E03 | Sales | Hyderabad | G1 | 2025-01-20 | |
| E04 | Ops | Bengaluru | G2 | 2021-09-01 | |
| E05 | Ops | Hyderabad | G1 | 2024-11-05 | 2025-03-05 |
| E06 | Ops | Hyderabad | G3 | 2020-04-10 | |
| E07 | IT | Bengaluru | G3 | 2019-08-01 | |
| E08 | IT | Bengaluru | G2 | 2025-03-03 | |
| E09 | IT | Hyderabad | G1 | 2023-07-01 | 2025-01-25 |
| E10 | Finance | Hyderabad | G2 | 2022-02-14 | |
| E11 | Finance | Bengaluru | G1 | 2025-01-06 | |
| E12 | Sales | Bengaluru | G2 | 2024-05-20 | |

**DAX / Steps (not run here):** Measures (table Employees; `Metrics` can be a measure table):
```dax
As Of Date = DATE ( 2025, 3, 31 )
Headcount =
VAR _d = [As Of Date]
RETURN COUNTROWS ( FILTER ( Employees, Employees[JoinDate] <= _d && ( ISBLANK ( Employees[ExitDate] ) || Employees[ExitDate] > _d ) ) )
Exits = COUNTROWS ( FILTER ( Employees, Employees[ExitDate] >= DATE ( 2025, 1, 1 ) && Employees[ExitDate] <= [As Of Date] ) )
Opening HC =
VAR _s = DATE ( 2025, 1, 1 )
RETURN COUNTROWS ( FILTER ( Employees, Employees[JoinDate] < _s && ( ISBLANK ( Employees[ExitDate] ) || Employees[ExitDate] >= _s ) ) )
Attrition % = DIVIDE ( [Exits], ( [Opening HC] + [Headcount] ) / 2 )
Avg Tenure (yrs) =
VAR _d = [As Of Date]
RETURN AVERAGEX ( FILTER ( Employees, Employees[JoinDate] <= _d && ( ISBLANK ( Employees[ExitDate] ) || Employees[ExitDate] > _d ) ), DATEDIFF ( Employees[JoinDate], _d, DAY ) / 365.25 )
```
Parameter (generated by Modeling > New parameter > Fields; shape from memory):
```dax
Measure Pick = {
    ( "Headcount", NAMEOF ( [Headcount] ), 0 ),
    ( "Attrition %", NAMEOF ( [Attrition %] ), 1 ),
    ( "Avg tenure (yrs)", NAMEOF ( [Avg Tenure (yrs)] ), 2 )
}
```
Steps: Modeling tab > **New parameter** > **Fields** > add the three measures > tick **Add slicer** > put `Measure Pick` in the chart's Y axis, Dept in X axis.
**Alternative:** Disconnected table `Pick[Name]` plus `SWITCH ( SELECTEDVALUE ( Pick[Name] ), "Headcount", [Headcount], "Attrition %", [Attrition %], [Avg Tenure (yrs)] )`; works in any build, but you maintain it by hand.
**Result:** Reproduced with pandas (DAX not run here). Headcount Sales 3, Ops 2, IT 2, Finance 2; Attrition % (quarter, not annualised) Sales 33.3, Ops 40.0, IT 50.0, Finance 0.0; Avg tenure Sales 1.3, Ops 4.3, IT 2.9, Finance 1.7 years; company: 9, 33.3, 2.4.
**Pandas check:** (this is the Q51 setup block reused by Q45, Q48, Q50, Q52, Q57, Q58, Q60, Q61 as `setup.py`)
```python
import pandas as pd
emp = pd.DataFrame([("E01","Sales","Hyderabad","G1","2022-06-01",None),("E02","Sales","Bengaluru","G2","2023-01-15","2025-02-10"),
 ("E03","Sales","Hyderabad","G1","2025-01-20",None),("E04","Ops","Bengaluru","G2","2021-09-01",None),("E05","Ops","Hyderabad","G1","2024-11-05","2025-03-05"),
 ("E06","Ops","Hyderabad","G3","2020-04-10",None),("E07","IT","Bengaluru","G3","2019-08-01",None),("E08","IT","Bengaluru","G2","2025-03-03",None),
 ("E09","IT","Hyderabad","G1","2023-07-01","2025-01-25"),("E10","Finance","Hyderabad","G2","2022-02-14",None),("E11","Finance","Bengaluru","G1","2025-01-06",None),
 ("E12","Sales","Bengaluru","G2","2024-05-20",None)], columns=["EmpID","Dept","Location","Grade","JoinDate","ExitDate"])
emp["JoinDate"] = pd.to_datetime(emp.JoinDate); emp["ExitDate"] = pd.to_datetime(emp.ExitDate)
start, end = pd.Timestamp("2025-01-01"), pd.Timestamp("2025-03-31")
def active_on(d, df=emp): return df[(df.JoinDate <= d) & (df.ExitDate.isna() | (df.ExitDate > d))]
def metrics(df):
    o = len(active_on(start - pd.Timedelta(days=1), df)); c = len(active_on(end, df))
    x = df.ExitDate.between(start, end).sum(); a = active_on(end, df)
    return pd.Series({"Headcount": c, "Attrition %": round(100*x/((o+c)/2),1) if o+c else None,
                      "Avg tenure (yrs)": round(((end-a.JoinDate).dt.days/365.25).mean(),1)})
print(emp.groupby("Dept").apply(metrics, include_groups=False)); print(metrics(emp))
```
Printed output (Headcount shows as 2.0, 3.0 etc. because pandas makes the table decimal): Finance 2 / 0.0 / 1.7; IT 2 / 50.0 / 2.9; Ops 2 / 40.0 / 4.3; Sales 3 / 33.3 / 1.3; total 9 / 33.3 / 2.4 (also by Location: Bengaluru 5 / 22.2 / 2.1, Hyderabad 4 / 44.4 / 2.8; by Grade: G1 3 / 66.7 / 1.1, G2 4 / 25.0 / 1.9, G3 2 / 0.0 / 5.3).
**Version / licensing note:** Field parameters are described on the Microsoft Learn "Field parameters" page (listed in research/Book04_Part06_sources.md, not re-fetched here). Which Desktop release introduced them and whether it was once a preview: from memory, unverified. Nothing about licence was verified.
**Edge cases:** Number formats differ per measure (a % next to a count) so set format inside each measure; average-of-ratios totals; a measure returning blank hides a bar.
**Likely follow-ups:** 1) *Can you also switch the axis?* Yes, a second parameter with Dept, Location, Grade columns (Q61). 2) *Title?* `SELECTEDVALUE` of the parameter's name column.
**Common mistakes:** Putting the parameter only in the slicer and not in the chart; editing the generated table by hand wrongly; mixing units without formatting.

### Q52 ⭐ 🟡 What does the Select all option in a slicer actually do to the filter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand the "inverted filter" behaviour that makes new values appear automatically?
**Say this in the interview:** "Select all is not a list of every value. It switches the slicer to an 'everything except what I untick' filter. So if I untick Finance, the filter is 'not Finance', and a department added later is included automatically."
**Explain simply:**
- Turn on via the slicer's Format pane (Slicer settings > Selection > **Select all**).
- Without it, ticking Sales, Ops and IT builds a fixed list of three; a new department is excluded.
- With it, ticking Select all then unticking Finance builds "all except Finance"; new values flow in. Per the slicers page as listed in research/Book04_Part06_sources.md this is an inverted filter.
**Example:** Four departments; Finance excluded. A new Legal team joins.
**Sample data:** the Q51 Employees table plus E13 (Legal, joined 2025-03-20).
**DAX / Steps (not run here):** Select slicer > Format pane > **Slicer settings** > **Selection** > **Select all** On. Click Select all, then untick Finance.
**Alternative:** Filter on the Filters pane with "Advanced filtering: is not Finance".
**Result:** Reproduced with pandas. Before Legal: both approaches give 7. After Legal joins: "all except Finance" gives 8, an explicit Sales/Ops/IT list stays 7.
**Pandas check:** (setup block from Q51)
```python
exec(open("setup.py").read())
act = active_on(end)
new = pd.DataFrame([("E13","Legal","Hyderabad","G2","2025-03-20",None)], columns=emp.columns)
new["JoinDate"]=pd.to_datetime(new.JoinDate); new["ExitDate"]=pd.to_datetime(new.ExitDate)
act2 = pd.concat([act, active_on(end, new)])
print((act.Dept != "Finance").sum(), act.Dept.isin(["Sales","Ops","IT"]).sum())
print((act2.Dept != "Finance").sum(), act2.Dept.isin(["Sales","Ops","IT"]).sum())
```
Output: `7 7` then `8 7`.
**Version / licensing note:** Behaviour per the Microsoft slicers page via the sources file (not re-fetched); the Format pane path is from memory, unverified.
**Edge cases:** Unticking everything while Select all is on shows nothing; synced slicers and report-level filters inherit the same logic.
**Likely follow-ups:** 1) *Why does it matter?* Reports stay correct as data grows. 2) *Is this like a NOT filter?* Yes.
**Common mistakes:** Believing Select all lists every item; not testing after data refresh adds a new value.

### Q53 ⭐ 🟡 What are Apply all slicers and Clear all slicers buttons, and why would you add them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you think about user experience and report speed with many slicers?
**Say this in the interview:** "Apply all slicers holds back the queries until the user has finished choosing, then applies everything at once. Clear all slicers resets every slicer in one click. They help on busy pages and on slow data sources."
**Explain simply:**
- Normally each slicer click immediately re-runs the visuals. With five slicers that is five refreshes.
- **Apply all slicers** button: the user makes all choices, then clicks Apply, so the page refreshes once.
- **Clear all slicers** button: one click removes every selection on the page.
- Both are in Insert > Buttons (per the slicers page in the sources file, not re-fetched; exact menu from memory, unverified). A query-reduction option in report settings can also add Apply buttons.
**Example:** A payroll page has Dept, Location, Grade, Month and Cost-centre slicers on a DirectQuery source (queries run live on the database). Two Apply clicks beat ten refreshes.
**DAX / Steps (not run here):** Home or Insert tab > **Buttons** > **Apply all slicers** (and **Clear all slicers**) > place on page > Format to style. For reduction: File > Options and settings > Options > Current file > **Query reduction**.
**Alternative:** The slicer's own Reset (eraser icon) clears one slicer; or a Bookmark with Data On to reset (see Q47).
**Version / licensing note:** Per the sources file; button wording and query-reduction path: from memory, unverified.
**Edge cases:** Clear all only affects slicers, not Filters pane filters; check synced slicers on other pages.
**Likely follow-ups:** 1) *Clear all vs bookmark reset?* Clear is simpler; a bookmark can reset more things. 2) *Is Apply needed on small data?* Rarely.
**Common mistakes:** Forgetting to label the buttons; adding Apply but leaving users to guess.

### Q54 ⭐ 🟡 How would you build a slicer of top customers without using a Top N filter on the visual (disconnected table approach)?
**Asked at:** one AmbitionBox candidate review (interview Mar 2024, DataToBiz Power BI developer, snippet only) lists this slicer-of-top-customers question per research/Book04_Part06_sources.md; treat as one unverified report.
**What the interviewer is checking:** Can you drive a calculation from a slicer that is not connected to the data?
**Say this in the interview:** "I create a small Top N table (3, 5, 10) with no relationship to the model, read the user's choice with SELECTEDVALUE, and use a measure that ranks customers and returns a value only for ranks up to N. The customer visual then shows just the top ones."
**Explain simply:**
- **Disconnected table**: a table with no relationship, so choosing in it filters nothing by itself; you read the choice in a measure.
- **RANKX** ranks customers by sales; **ALLSELECTED** keeps the ranking within what the user filtered.
- Customers outside the top N get blank and drop out of the visual.
- Ties: dense ranking keeps all tied customers.
**Example:** Eight customers; user picks Top 3.
**Sample data:** Table Sales, and disconnected table TopN.

| Customer | Sales |
|---|---|
| Acme | 90 |
| Birla | 75 |
| Cipla | 60 |
| Delta | 60 |
| Eon | 40 |
| Fynn | 30 |
| Gati | 20 |
| Hexa | 10 |

TopN table: values 3, 5, 10.
**DAX / Steps (not run here):**
```dax
Total Sales = SUM ( Sales[Sales] )
Top N Value = SELECTEDVALUE ( TopN[TopN], 3 )
Sales (Top N) =
VAR _rank = RANKX ( ALLSELECTED ( Sales[Customer] ), [Total Sales], , DESC, Dense )
RETURN IF ( _rank <= [Top N Value], [Total Sales] )
```
Steps: Enter data (or DAX table `TopN = { 3, 5, 10 }`, whose column is called Value by default: rename it to TopN to match the measure) > slicer on TopN > bar chart with Customer and `Sales (Top N)`. For a slicer that lists only top customers, add a `Is Top Customer = IF ( ... <= N, 1, 0 )` measure as a visual-level filter on the customer slicer (whether slicers accept a measure filter: from memory, unverified).
**Alternative:** Native visual-level Top N filter (fixed N, no user choice); or a bookmark per N.
**Result:** Reproduced with pandas. Top 3 returns Acme 90, Birla 75, Cipla 60, Delta 60 (tie), total 285; Top 5 adds Eon 40 and Fynn 30, total 355; all customers 385.
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"Customer":["Acme","Birla","Cipla","Delta","Eon","Fynn","Gati","Hexa"],"Sales":[90,75,60,60,40,30,20,10]})
sales["Rank"] = sales.Sales.rank(method="dense", ascending=False).astype(int)
for n in (3,5): sales[f"Top{n}"] = sales.Sales.where(sales.Rank <= n)
print(sales.to_string(index=False)); print(sales.Top3.sum(), sales.Top5.sum(), sales.Sales.sum())
```
Output totals: `285.0 355.0 385`.
**Version / licensing note:** RANKX, ALLSELECTED, SELECTEDVALUE syntax from memory; the Microsoft Learn DAX pages were not reachable (ENOTFOUND), so syntax is unverified against docs.
**Edge cases:** Dense vs skip ranking changes the tie count (Delta ties Cipla at rank 3, so Top 3 shows four people); blank sales; the user's own page filters change the ranking because of ALLSELECTED.
**Likely follow-ups:** 1) *Why not a Top N filter?* It is fixed; users cannot change N. 2) *Rank over everything instead?* Use ALL instead of ALLSELECTED.
**Common mistakes:** Creating a relationship to the disconnected table; forgetting the SELECTEDVALUE default, giving blank when nothing is chosen.

### Q55 ⭐ 🟡 What are the limitations of report page tooltips?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know where tooltips stop being the right tool?
**Say this in the interview:** "A tooltip page is small, fixed in size and not interactive: you cannot click inside it. It also does not work on dashboards, so for anything the reader needs to click, I use drillthrough."
**Explain simply:**
- **Report page tooltip**: a mini report page that appears when you hover on a data point instead of the plain text tooltip.
- Per the Microsoft tooltip page as listed in research/Book04_Part06_sources.md: non-interactive, and not available on dashboards.
- Other practical limits (from memory, unverified): small default size (about 320 by 240 pixels), runs queries on every hover so many heavy visuals feel slow, and no scrolling.
- Not usable for important content on touch screens or phones where hover does not exist.
**Example:** Hovering over the "Sales" bar shows a tooltip page with attrition trend for that department; clicking a point inside it does nothing.
**DAX / Steps (not run here):** 1) Add a page > Format > Page information > turn on **Allow use as tooltip**. 2) Format > Canvas settings > Type = Tooltip. 3) On the real chart: Format > General > Tooltips > Type: Report page > pick the page. 4) Add the field you want to receive as a tooltip field.
**Alternative:** Drillthrough page or a bookmarked detail panel when reader interaction is required.
**Version / licensing note:** Two limitations per the sources file; size and phone remarks from memory, unverified.
**Edge cases:** Dashboard tiles show the standard tooltip; a tooltip page filtered by the hovered field only if that field matches.
**Likely follow-ups:** 1) *Can a tooltip show many visuals?* Yes but keep it light. 2) *Phone?* Hover needs long-press (from memory, unverified).
**Common mistakes:** Packing slicers in a tooltip; forgetting to hide the tooltip page from navigation.

### Q56 ⭐ 🟡 A category shows as (Blank) in a chart. How do you find out why, and how do you handle it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you trace blanks to data quality or relationship issues instead of just hiding them?
**Say this in the interview:** "I check three causes: the source really has empty values, the fact table has keys that do not exist in the lookup table, or the visual is mixing fields from unrelated tables. Then I fix at the source or in Power Query, and only as a last resort filter the blank."
**Explain simply:**
- **Blank in the category** appears when an employee row has no department, or has a key like 9 that the department table does not contain (an "orphan").
- Find them: build a table visual with the key column; check the Data view for empty cells; Power Query column profile (Column quality shows empty %).
- Handle: fix the source; add the missing lookup row; in Power Query replace nulls with "Unassigned"; or apply a visual filter that removes (Blank) after telling the owner.
**Example:** 6 staff; Dept table has IDs 1, 2, 3. Staff E5 has DeptID 9 and E6 has none: both land under (Blank).
**Sample data:** Table Dept (DeptID 1 Sales, 2 Ops, 3 IT); table Staff.

| EmpID | DeptID |
|---|---|
| E1 | 1 |
| E2 | 1 |
| E3 | 2 |
| E4 | 3 |
| E5 | 9 |
| E6 | (empty) |

**DAX / Steps (not run here):**
```dax
Orphan Staff = COUNTROWS ( FILTER ( Staff, ISBLANK ( Staff[DeptID] ) || ISBLANK ( RELATED ( Dept[DeptName] ) ) ) )
```
```m
// Power Query: replace nulls in the DeptName column
= Table.ReplaceValue(Source, null, "Unassigned", Replacer.ReplaceValue, {"DeptName"})
```
Steps: Table view of Staff and Dept; Model view to confirm relationship; Transform data > column profile.
**Alternative:** Add an "Unknown" row to the Dept table and a default key such as -1 for staff with no department.
**Result:** Reproduced with pandas: Sales 2, Ops 1, IT 1, (Blank) 2; orphan key found: 9 (pandas prints it as `[9.0]` because the empty key makes the column decimal); rows with no key: 1.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID":[1,2,3],"DeptName":["Sales","Ops","IT"]})
staff = pd.DataFrame({"EmpID":["E1","E2","E3","E4","E5","E6"],"DeptID":[1,1,2,3,9,None]})
m = staff.merge(dept, on="DeptID", how="left")
print(m.assign(DeptName=m.DeptName.fillna("(Blank)")).groupby("DeptName").size())
print(sorted(set(staff.DeptID.dropna()) - set(dept.DeptID)), staff.DeptID.isna().sum())
```
**Version / licensing note:** DAX and M written from memory; Microsoft Learn was unreachable, so function behaviour (RELATED returning blank for no match) is unverified against docs.
**Edge cases:** Blank can be an empty string, not null (invisible but different); blank on a date axis is from missing dates; many-to-many relationships behave differently.
**Likely follow-ups:** 1) *Hide the blank?* Visual filter, but the totals still contain those rows. 2) *Why does a total not match?* The blank row is included in the total.
**Common mistakes:** Filtering the blank and hiding a data problem; replacing with 0 for text columns.

### Q57 ⭐ 🟡 What does Show items with no data do, and when would you turn it on?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know why a category or month "disappears" and how to force it to show.
**Say this in the interview:** "By default a chart hides categories that have no data. Show items with no data lists every category anyway, with a blank value. I turn it on when a missing category is itself information, such as a department with no hires."
**Explain simply:**
- Power BI drops axis items for which the measure is blank.
- Right-click the field in the Build pane > **Show items with no data** adds them back.
- Useful for time axes, matrices where gaps matter, and "zero hires this month" stories.
- Cost: more rows, so slower on large models; also a measure that returns 0 instead of blank shows the item even without the option.
**Example:** Q1 hires: Sales Jan 1, Finance Jan 1, IT Mar 1. Ops has none all quarter.
**Sample data:** Employees (Q51), hires by JoinDate in Jan-Mar 2025.
**DAX / Steps (not run here):** Build pane > right-click the Dept (or Month) field in Rows/Axis > **Show items with no data**. Measure:
```dax
Hires = COUNTROWS ( FILTER ( Employees, Employees[JoinDate] >= DATE ( 2025, 1, 1 ) && Employees[JoinDate] <= DATE ( 2025, 3, 31 ) ) )
```
**Alternative:** Make the measure return 0 with `+ 0`, but then every item appears everywhere, even irrelevant ones.
**Result:** Reproduced with pandas. Off: 3 rows (Finance-Jan 1, IT-Mar 1, Sales-Jan 1). On: 12 Dept x Month rows, 9 blank.
**Pandas check:** (setup block from Q51)
```python
exec(open("setup.py").read())
h = emp[emp.JoinDate.between(start, end)].copy(); h["Month"] = h.JoinDate.dt.strftime("%b")
t = h.groupby(["Dept","Month"]).size()
full = pd.MultiIndex.from_product([sorted(emp.Dept.unique()), ["Jan","Feb","Mar"]], names=["Dept","Month"])
print(t.to_string()); print(t.reindex(full).to_string())
```
**Version / licensing note:** From memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** Dates should come from a proper date table; combined with a slicer filter the items still follow the model's relationships.
**Likely follow-ups:** 1) *Why does zero hide gaps?* A 0 is a value; blank is not. 2) *Performance?* More cells to compute.
**Common mistakes:** Using it on fields from unrelated tables; expecting it to invent categories that are not in any table.

### Q58 ⭐ 🟡 How would you build a headcount waterfall (opening headcount, hires, exits, closing headcount)?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question per research/Book04_Part06_sources.md.
**What the interviewer is checking:** Can you define the four measures so they reconcile, and shape them for the waterfall visual?
**Say this in the interview:** "Closing equals opening plus hires minus exits. I write one measure for each, check that closing matches a direct count at the end date, and feed them to a waterfall through a small step table."
**Explain simply:**
- **Waterfall chart**: bars that float to show how a starting number changes to an ending number.
- Opening = people employed the day before the period starts; Hires = joined inside the period; Exits = left inside the period (shown negative); Closing = opening + hires - exits.
- Reconcile: closing must equal the count of active people on the last day.
**Example:** Q1 2025: opening 9, hires 3, exits 3, closing 9.
**Sample data:** Employees table from Q51.
**DAX / Steps (not run here):**
```dax
Step Value =
VAR _s = DATE ( 2025, 1, 1 ) VAR _e = DATE ( 2025, 3, 31 )
VAR _open = COUNTROWS ( FILTER ( Employees, Employees[JoinDate] < _s && ( ISBLANK ( Employees[ExitDate] ) || Employees[ExitDate] >= _s ) ) )
VAR _hires = COUNTROWS ( FILTER ( Employees, Employees[JoinDate] >= _s && Employees[JoinDate] <= _e ) )
VAR _exits = COUNTROWS ( FILTER ( Employees, Employees[ExitDate] >= _s && Employees[ExitDate] <= _e ) )
RETURN SWITCH ( SELECTEDVALUE ( Steps[Step] ), "Opening", _open, "Hires", _hires, "Exits", -_exits, "Closing", _open + _hires - _exits )
```
Steps: create table `Steps` (Step, Order: Opening 1, Hires 2, Exits 3, Closing 4; sort Step by Order) > Waterfall visual > Category = Steps[Step], Y = [Step Value]. Opening and Closing should be drawn as totals: the "set as total" option on a bar: from memory, unverified.
**Alternative:** Stacked column with an invisible "base" series (classic trick), or a matrix of four lines for a plain table.
**Result:** Reproduced with pandas: Opening 9, Hires 3, Exits -3, Closing 9; direct count at 31-Mar = 9. By department: Finance 1+1-0=2, IT 2+1-1=2, Ops 3+0-1=2, Sales 3+1-1=3.
**Pandas check:** (setup block from Q51)
```python
exec(open("setup.py").read())
o = len(active_on(start - pd.Timedelta(days=1))); h = emp.JoinDate.between(start, end).sum(); x = emp.ExitDate.between(start, end).sum()
print(o, h, -x, o + h - x, len(active_on(end)))
```
Output: `9 3 -3 9 9`.
**Version / licensing note:** From memory, unverified; Learn unreachable. Visual features (set as total, breakdown) vary by build.
**Edge cases:** Rehires (same person twice); someone who joins and leaves in the same quarter counts as both; exit date equal to period start; time zones/dates stored with time.
**Likely follow-ups:** 1) *Why is the closing a measure and not a sum?* A running sum can double count. 2) *By department?* Filter context handles it; the table above reconciles per dept.
**Common mistakes:** Exits as positive numbers; opening counted at period end; no reconciliation check.

### Q59 ⭐ 🟡 Can a field parameter be used as a drill-through or tooltip field, and what is the workaround?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the documented limitation and have a practical way round it?
**Say this in the interview:** "No. Microsoft documents that a field parameter cannot be a drillthrough or tooltip linked field. I use the real underlying columns (Department, Location) for drillthrough and tooltips, and keep the parameter only for the chart axis or values."
**Explain simply:**
- The limitation comes from the Microsoft Learn "Field parameters" page, as listed in research/Book04_Part06_sources.md (not re-fetched here).
- Why it bites: the detail page needs a fixed field to filter on, and a parameter's field changes with the user's choice.
- Workaround, unverified in a live build: (1) set the drillthrough page to use the real columns Dept, Location and Grade as drillthrough fields; (2) make sure the source visual contains the real column (for example in the Tooltips well); (3) for tooltip pages, add the real columns as the tooltip fields.
- A safer fallback: a detail table on the same page that responds to cross-filtering (clicking a bar), which works with the underlying value (from memory, unverified).
**Example:** A bar chart has the group parameter (Dept/Location/Grade). Right-click Sales > the drill-through page "Employee Detail" will not accept the parameter. Instead the page uses Dept, Location and Grade, and the chart also carries the real columns.
**DAX / Steps (not run here):** Employee Detail page > Drill through well > add Dept, Location, Grade > keep **Keep all filters** On (see Q48). On the source visual drag the same real columns into **Tooltips**. Test each grouping choice.
**Alternative:** Use a button that navigates to the detail page, with the filter carried by the slicers (sync), instead of right-click drillthrough.
**Version / licensing note:** Limitation per the sources file; workaround steps: from memory, unverified.
**Edge cases:** If only Location is the active group, the Dept column in the Tooltips well aggregates over several values and may confuse the drillthrough.
**Likely follow-ups:** 1) *Can the parameter be in the slicer?* Yes. 2) *Can it be a hierarchy?* Not in the way a native hierarchy drills.
**Common mistakes:** Dropping the parameter into the drill-through well and wondering why nothing happens.

### Q60 ⭐ 🔴 How would you build a report where a slicer filters most visuals but one visual still shows the company-wide total for comparison?
**Asked at:** commonly asked (no company-specific report found); a gap-fill scenario per research/Book04_Part06_sources.md.
**What the interviewer is checking:** Do you know the two tools: Edit interactions and DAX filter removal?
**Say this in the interview:** "Two ways. The visual-level way is Edit interactions: set the slicer's effect on that visual to None. The measure way is a company-total measure that removes the slicer's filter with ALL, so it can sit next to the filtered measure. I prefer the measure, because it also works for a comparison like share of company."
**Explain simply:**
- **Edit interactions** (Format tab > Edit interactions): choose how a slicer affects each other visual; the "None" icon stops filtering that visual.
- **ALL / REMOVEFILTERS**: a DAX instruction to ignore filters on a column inside one measure.
- Only remove the filter you mean to: `ALL ( Employees[Dept] )` clears Dept but keeps Location slicers; REMOVEFILTERS ( Employees ) clears everything on the table.
**Example:** Slicer Dept = Sales; the chart by Location shows selected and company numbers together.
**Sample data:** Employees table from Q51, active at 31-Mar-2025.
**DAX / Steps (not run here):**
```dax
Company Headcount = CALCULATE ( [Headcount], ALL ( Employees[Dept] ) )
Share of Company % = DIVIDE ( [Headcount], [Company Headcount] )
```
Steps: Dept slicer > both measures in a clustered bar by Location. Or: select the slicer > Format > **Edit interactions** > on the chosen visual click **None**.
**Alternative:** Edit interactions (no DAX); the visual then ignores every choice from that slicer, not only a part.
**Result:** Reproduced with pandas (DAX not run). With Dept = Sales: Bengaluru selected 1 vs company 5 (20.0%); Hyderabad 2 vs 4 (50.0%); totals 3 vs 9.
**Pandas check:** (setup block from Q51)
```python
exec(open("setup.py").read())
act = active_on(end); sel = act[act.Dept == "Sales"]
out = pd.DataFrame({"Selected": sel.groupby("Location").size(), "Company": act.groupby("Location").size()}).fillna(0).astype(int)
out["Share %"] = (100*out.Selected/out.Company).round(1); print(out)
```
**Version / licensing note:** Edit interactions behaviour per the Microsoft "Change how visuals interact" page listed in research/Book04_Part06_sources.md (not re-fetched). ALL/REMOVEFILTERS semantics from memory, unverified (Learn unreachable).
**Edge cases:** Other slicers (Location) still filter the "company" number if you only remove Dept; if the visual is a card without Location this is fine, but a share % can exceed 100 if filters are removed inconsistently; page and report filters in the Filters pane still apply.
**Likely follow-ups:** 1) *ALL vs ALLSELECTED?* ALLSELECTED respects outer filters; ALL ignores them. 2) *Does ALL also remove a Filters-pane filter?* Only a filter on the same column (here Dept); a page or report filter on another column, such as Year, still applies.
**Common mistakes:** Removing all filters and losing the date filter too; using Edit interactions then forgetting a new visual picks up the slicer by default.

### Q61 ⭐ 🔴 How would you design one HR page where managers pick the measure (headcount, attrition, average tenure) and the grouping (department, location, grade) and can still drill through to employees?
**Asked at:** commonly asked (no company-specific report found); a gap-fill scenario per research/Book04_Part06_sources.md.
**What the interviewer is checking:** Can you combine field parameters, measures and the drillthrough limitation into a working design?
**Say this in the interview:** "I use two field parameters, one for the measure and one for the grouping, each with a slicer, and one chart that uses both. For employee detail I use a drillthrough page based on the real columns, because parameters cannot be drillthrough fields, and I test it for every grouping choice."
**Explain simply:**
- Measure parameter: Headcount, Attrition %, Avg tenure (Q51). Grouping parameter: columns Dept, Location, Grade.
- One bar chart: Axis = grouping parameter, Values = measure parameter. Slicers sit next to it.
- Drillthrough: separate "Employee Detail" page with a table of employees; drillthrough fields are Dept, Location and Grade (real columns), per Q59.
- Safety net: if right-click drillthrough does not fire for a chosen grouping, add a detail table filtered by clicking the bar.
**Example:** Manager picks Attrition % by Location: Hyderabad 44.4, Bengaluru 22.2. Right-click Hyderabad > Drill through > list of Hyderabad employees.
**Sample data:** Employees table from Q51.
**DAX / Steps (not run here):**
```dax
Group Pick = {
    ( "Department", NAMEOF ( Employees[Dept] ), 0 ),
    ( "Location", NAMEOF ( Employees[Location] ), 1 ),
    ( "Grade", NAMEOF ( Employees[Grade] ), 2 )
}
Chart Title = SELECTEDVALUE ( 'Measure Pick'[Measure Pick], "Headcount" ) & " by " & SELECTEDVALUE ( 'Group Pick'[Group Pick], "Department" )
```
Steps: New parameter > Fields twice (Measure Pick from Q51; Group Pick above) > slicers > chart > Employee Detail page with drillthrough fields > Back button; hide the detail page from tabs.
**Alternative:** Separate pages per grouping (simple, repetitive), or a matrix with the three columns as a hierarchy.
**Result:** Reproduced with pandas (Q51 output): by Dept Attrition % Sales 33.3, Ops 40.0, IT 50.0, Finance 0.0; by Location Bengaluru 22.2, Hyderabad 44.4; by Grade G1 66.7, G2 25.0, G3 0.0; Headcount by Grade 3, 4, 2.
**Pandas check:** (setup block from Q51)
```python
exec(open("setup.py").read())
for by in ("Dept","Location","Grade"): print(emp.groupby(by).apply(metrics, include_groups=False))
```
Output matches the figures in the Result line above.
**Version / licensing note:** Field parameters and the drillthrough/tooltip limitation per the sources file (not re-fetched); the interaction of parameter axes with right-click drillthrough is unverified, from memory.
**Edge cases:** Small groups give silly percentages (Grade G1 66.7 from 3 people); quarterly attrition is not annual; blank grades; an unsorted parameter order; formats per measure.
**Likely follow-ups:** 1) *Row-level security?* Managers should only see their own team (a separate part). 2) *Why test each grouping?* Drillthrough context differs per choice.
**Common mistakes:** Using the parameter in the drillthrough well; mixing percentage and count axes without formatting; no Back button.
