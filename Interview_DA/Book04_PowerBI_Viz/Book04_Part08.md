# Book 4 — Power BI & Visualization | Part 8: Dashboard design principles and storytelling with data 🟢🟡

**Target:** 45 questions | **Actual:** 47 questions
**Scope:** dashboard design principles (layout, colour, chart choice, accessibility, KPIs) and data storytelling for stakeholders; Power BI build/fix tasks live in Part 9.

### Q1 ⭐⭐⭐ 🟢 What are the key principles of good dashboard design?
**Asked at:** commonly asked (no company-specific report found); design-principle answers (balance, contrast, alignment, hierarchy, white space) appear in prep blogs such as eduyush (snippet only).
**What the interviewer is checking:** Whether you design for the reader, not for yourself.
**Say this in the interview:** "I start with the audience and the decision they must make. Then: few visuals, the most important number top-left, the right chart for each question, consistent and restrained colour, clear labels, and no clutter. If a reader cannot get the main message in about five seconds, I redesign."
**Explain simply:**
- **Audience first:** an HR head wants attrition and open positions; a recruiter wants pipeline details. Different people, different pages.
- **One screen, one message:** a "dashboard" is a single page you can take in at a glance; too many visuals hides the point.
- **Visual hierarchy:** big, bold items are read first (hierarchy means ordering things by importance using size, position and colour).
- **Right chart, honest scales:** bars for comparing, lines for time; bars start at zero.
- **Consistency and accessibility:** same colours mean the same thing everywhere; do not rely on colour alone.
**Example:** An HR dashboard opens with four cards (headcount 500, attrition 1.8%, open roles 24, offer-accept 80%), then one trend line and one bar by department.
**Alternative:** Remember it as "audience, message, layout, chart, colour, test with a real user".
**Version / licensing note:** Design principles are tool-independent. Microsoft's own design-tips page was not reachable here (learn.microsoft.com fetch failed with ENOTFOUND), so any claim about Power BI wording is from memory, unverified.
**Edge cases:** Some audiences (analysts) want dense detail; then use a separate detail page instead of cramming the overview.
**Likely follow-ups:** 1) *Which principle matters most?* Knowing the audience's decision. 2) *How do you test it?* Show it to a real user and ask what they take away in five seconds.
**Common mistakes:** Adding every available chart; using rainbow colours; designing before asking what decision the report supports.

### Q2 ⭐⭐⭐ 🟢 How do you choose the right chart type for your data (bar, line, pie, table, card)?
**Asked at:** commonly asked (no company-specific report found); "choosing a visual for the audience" appears in storytelling prep lists (Yardstick/Adaface, snippets only).
**What the interviewer is checking:** Do you match the chart to the question being asked?
**Say this in the interview:** "I begin with the question. Comparing categories: bar chart. Change over time: line chart. Parts of a whole with very few slices: maybe a pie or, better, a bar. One headline number: a card. Exact values or lookup: a table."
**Explain simply:**
- **Bar/column:** compare things (attrition by department). Easy for the eye to judge lengths.
- **Line:** shows a trend over time (monthly headcount).
- **Pie/donut:** only for a handful of slices adding to 100% (see Q10).
- **Card:** a single KPI (key performance indicator, a headline number tied to a goal).
- **Table:** when people need exact numbers or many columns.
**Example:** "Attrition by department" is six comparisons, so a sorted horizontal bar. "Monthly attrition for 12 months" is a line. "Total headcount today: 500" is a card.
**Alternative:** Ask three questions: compare, trend, or composition? How many categories? Do they need exact numbers?
**Version / licensing note:** All these visuals ship in Power BI Desktop's built-in set (from memory, unverified).
**Edge cases:** Over 7-8 categories, switch from pie to bar. Time on the x-axis with gaps still needs a line or column, not a pie.
**Likely follow-ups:** 1) *Bar or column?* Horizontal bars when labels are long. 2) *When a table?* When users need exact figures or to export.
**Common mistakes:** Choosing the chart first and bending the data to fit; pies with 10 slices; lines for unordered categories.

### Q3 ⭐⭐⭐ 🟢 How do you decide which KPIs and visuals go on a dashboard?
**Asked at:** commonly asked (no company-specific report found); "list 3-5 business questions first" advice appears in consultancy blogs (Al Rafay, sranalytics, snippets only).
**What the interviewer is checking:** Can you link metrics to decisions instead of dumping data?
**Say this in the interview:** "I ask the stakeholder which decisions the dashboard must support, write down 3 to 5 questions, and pick the KPI that answers each. A number that changes no decision stays off the page."
**Explain simply:**
- Start from questions: "Are we losing people faster?" leads to attrition rate.
- Each KPI needs a definition, an owner and a target; otherwise arguments follow.
- Keep a few headline KPIs; push the rest to a detail page or drill-through (a click that opens a related page filtered to the chosen item).
- Pick one visual per question, then remove any that nobody would miss.
**Example:** Recruiting head's questions: how long to hire, where candidates drop, are we hitting joins. KPIs: time-to-fill (days from opening to joining), funnel conversion, joins vs target. Three cards plus a funnel and a trend.
**Alternative:** Do a "so what" test: for each KPI, ask what someone would do differently if it moved.
**Version / licensing note:** Tool-independent. Not run, no fetch; from memory, unverified.
**Edge cases:** Vanity metrics (total applications) look good but drive no action; lagging indicators (attrition) may need leading ones (engagement score).
**Likely follow-ups:** 1) *How many KPIs?* About 4-6 on the main view. 2) *Who signs off the definitions?* The business owner, documented.
**Common mistakes:** Letting stakeholders request "everything"; no agreed definitions; no targets, so cards have no meaning.

### Q4 ⭐⭐⭐ 🟢 What is data storytelling, and why does it matter for an analyst?
**Asked at:** commonly asked (no company-specific report found); appears in storytelling/behavioural prep lists (Yardstick, Adaface, InterviewQuery, snippets only).
**What the interviewer is checking:** Can you turn numbers into a message that gets action?
**Say this in the interview:** "Data storytelling is combining the data, a clear visual and a narrative so the audience understands what happened, why it matters and what to do next. A correct analysis that nobody acts on has not helped the business."
**Explain simply:**
- Three parts: data (facts), visuals (make patterns easy to see), narrative (context, insight, recommendation).
- It is not decoration: each chart supports one sentence of the story.
- It matters because decision-makers are busy and non-technical; they act on what they understand.
**Example:** Instead of "attrition is 18% annualised", say: "Support loses 1 in 5 people each year, mostly within the first six months. Fixing onboarding could save about 12 hires a year."
**Alternative:** The one-line test: write the takeaway as a headline sentence for each chart.
**Version / licensing note:** Tool-independent; from memory, unverified.
**Edge cases:** If the data is weak, say so; honest uncertainty builds more trust than a polished overclaim.
**Likely follow-ups:** 1) *Give an example.* Use the attrition sentence above. 2) *Is it only for presentations?* No, dashboards need titles that state the insight too.
**Common mistakes:** Showing everything you analysed; ending without a recommendation; chart titles that only name the field.

### Q5 ⭐⭐⭐ 🟡 Walk me through how you would approach designing a dashboard from scratch when a stakeholder asks for one.
**Asked at:** commonly asked (no company-specific report found); a "design a dashboard" scenario appears in prep lists (snippets only).
**What the interviewer is checking:** Do you have a repeatable, business-first process?
**Say this in the interview:** "I clarify the purpose and audience, agree the questions and KPI definitions, check the data exists, sketch a wireframe on paper, build a first version, get feedback, and then publish with documentation and a plan to review usage."
**Explain simply:**
- **1. Clarify:** who uses it, what decision, how often, on what device.
- **2. Define KPIs** with formulas and targets.
- **3. Check data:** where it lives, how clean, how often it refreshes.
- **4. Sketch:** a wireframe (a rough layout drawing) so changes are cheap.
- **5. Build, then test** with two or three real users; iterate.
- **6. Launch and measure** use (who opens it); schedule a review.
**Example:** HR head asks for "an attrition dashboard". I learn she wants to find hot-spot departments monthly on her laptop. Sketch: four cards, trend line, department bar, reason breakdown. Two feedback rounds, then publish.
**Alternative:** A shorter spoken version: "ask, define, sketch, build, test, launch, review".
**Version / licensing note:** Sharing in the Power BI Service typically needs Pro or capacity licences; from memory, unverified.
**Edge cases:** If source data is not available, say so early and offer a smaller first version.
**Likely follow-ups:** 1) *What if requirements change mid-way?* Agree scope in writing, add changes to a v2 list. 2) *Why sketch first?* Cheap to change.
**Common mistakes:** Opening Power BI before talking to the user; no KPI definitions; no feedback loop.

### Q6 ⭐⭐⭐ 🟡 How do you design a dashboard for non-technical senior executives?
**Asked at:** commonly asked; a Dataford practice question on designing a Power BI dashboard for non-technical business leaders is listed for Vertiv (search snippet only; unverified) and the Taggd recruiter PDF mentions executive dashboards (snippet only).
**What the interviewer is checking:** Can you simplify without losing the message?
**Say this in the interview:** "Executives want the answer in seconds. I put a few headline KPIs with targets top-left, use plain labels, show exceptions in red, keep one page for the overview, and let them drill into detail only if they want it."
**Explain simply:**
- Fewer numbers, each with context (vs target, vs last period).
- Plain language: "People who left" rather than technical field names.
- Highlight what needs attention (exceptions), not everything.
- Works on a phone or projector: big text, high contrast.
- Offer detail on demand through drill-through or a second page.
**Example:** CHRO page: headcount 500, attrition 1.8% (target 1.5%, red), open roles 24, offer acceptance 80%; below, a department bar with the two departments over threshold in red.
**Alternative:** Pair the dashboard with a three-line email summary of what changed this month.
**Version / licensing note:** Mobile layouts exist in Desktop/Service (see Q28); from memory, unverified.
**Edge cases:** Executives may only view on mobile; test there. Numbers must tie to finance/HR official figures or trust is lost.
**Likely follow-ups:** 1) *What if they ask for more?* Add a detail page, not more tiles on the front. 2) *How do you know it works?* Watch them use it.
**Common mistakes:** Jargon; too many charts; no targets so nobody knows if a number is good.

### Q7 ⭐⭐⭐ 🟡 How do you present your insights to non-technical stakeholders?
**Asked at:** commonly asked; explaining findings to a non-technical audience is a standard item in data-storytelling prep lists (Yardstick, Adaface, snippets only).
**What the interviewer is checking:** Clear communication and business focus.
**Say this in the interview:** "I lead with the conclusion and its business impact, support it with one or two simple visuals, avoid technical terms, give a clear recommendation, and leave time for questions. Method details go in the appendix."
**Explain simply:**
- Answer first: "Attrition is concentrated in Support" before showing how you found it.
- Translate numbers into money, people or time.
- One message per slide or visual; remove everything else.
- Use their vocabulary and analogies.
- End with a decision: what you want them to approve.
**Example:** "Support lost 24 of 120 people (20%). Replacing them costs about 24 hires of effort. I recommend a 90-day onboarding buddy programme; we can review in three months."
**Alternative:** Use the "headline, evidence, action" structure for every slide.
**Version / licensing note:** Tool-independent; from memory, unverified.
**Edge cases:** For mixed audiences, give the one-page summary to all and the technical backup on request.
**Likely follow-ups:** 1) *How do you handle a question you cannot answer?* Say so, note it, follow up. 2) *How long should it be?* As short as the decision allows.
**Common mistakes:** Walking through the methodology first; reading numbers off slides; no recommendation.

### Q8 ⭐⭐⭐ 🟡 A stakeholder says the numbers on your dashboard do not match their own Excel numbers. What do you do?
**Asked at:** commonly asked; "numbers did not match expectations" and inconsistent-data dashboard scenarios appear in prep blogs (Techcanvass, FanRuan, Adaface, snippets only).
**What the interviewer is checking:** Calm, systematic reconciliation and trust-building.
**Say this in the interview:** "I don't defend or panic. I ask for their file, agree the exact metric, period and filters, then compare both at the lowest level until I find the first row where they differ. Then I fix my model or explain the difference and document the definition."
**Explain simply:**
- Reconcile means matching two sets of numbers and finding the gap.
- Common causes: different date range, different filter (active staff only?), different definition (headcount at month-end vs average), duplicates, data refreshed at a different time, rounding.
- Compare totals, then by department, then by employee, until the gap is isolated.
- Record the agreed definition so it does not come back.
**Example:** Dashboard says 500 headcount; Excel says 512. Gap of 12 = contractors included in Excel. Agree: dashboard shows employees only, add a contractors line.
**Alternative:** In Power BI, show a table of the underlying rows (visual with employee ID) next to their Excel list and use a join in Power Query to list mismatches.
**Version / licensing note:** Tool-independent; from memory, unverified.
**Edge cases:** Both may be right under different definitions; sometimes the Excel is stale or manually edited.
**Likely follow-ups:** 1) *What if you were wrong?* Own it, fix, tell everyone who uses it. 2) *How to prevent it?* Metric definitions page and data-refresh timestamp on the report.
**Common mistakes:** Arguing before checking; changing the dashboard to match Excel without understanding why; not documenting the definition.

### Q9 ⭐⭐⭐ 🟡 Users are not using the dashboard you built (low adoption). How do you find out why and fix it?
**Asked at:** commonly asked; a low-adoption scenario appears in the Taggd recruiter PDF (snippet only, unverified).
**What the interviewer is checking:** Do you treat adoption as a problem to investigate, with users and data?
**Say this in the interview:** "First I check the usage numbers, then I talk to users. Typical reasons are: it does not answer their question, it is slow, they do not trust the numbers, they do not know it exists, or it is hard to access. I fix the cause, not just the look."
**Explain simply:**
- **Measure:** the Power BI Service has usage metrics (views per user) for reports; check who opens it and when.
- **Ask:** short interviews with 3-5 intended users: "what do you use instead?"
- **Diagnose:** relevance, speed, trust, discoverability, training.
- **Fix and re-test:** simplify, speed up, add definitions, put it where people already work (Teams, email subscription).
**Example:** 40 managers invited, only 6 opened it last month. Interviews: it loads in 30 seconds and they prefer a weekly Excel email. Fix: speed up, add a scheduled email snapshot; views reach 25.
**Alternative:** Run a 15-minute walkthrough session and collect feedback live.
**Version / licensing note:** Usage metrics and subscriptions are Service features whose availability depends on licence; from memory, unverified.
**Edge cases:** Low usage may be fine if the report is only needed quarterly.
**Likely follow-ups:** 1) *If it is slow?* Reduce visuals, simplify the model. 2) *If they don't trust it?* Reconcile numbers (Q8).
**Common mistakes:** Assuming users are lazy; redesigning colours without asking; no launch or training.

### Q10 ⭐⭐ 🟢 Why are pie charts often discouraged, and when are they acceptable?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of how people read charts, and balance rather than dogma.
**Say this in the interview:** "People compare lengths accurately but angles and areas poorly, so similar slices are hard to rank. A bar chart is usually clearer. A pie is acceptable with only two to five slices that add to a whole and where one slice clearly dominates."
**Explain simply:**
- Slices of similar size look the same; bars make differences obvious.
- Many slices become unreadable, and labels crowd.
- Acceptable: gender split 60/40, "joined vs did not join".
- Microsoft's design guidance, as recalled, suggests pies only for fewer than about eight categories (from memory, unverified).
**Example:** Seven departments with headcount 150, 120, 130, 115, 110, 105, 100: pie slices look equal; a sorted bar shows the order instantly.
**Alternative:** Sorted bar chart, or a 100% stacked single bar for a share.
**Version / licensing note:** Pie and donut are standard Power BI visuals; from memory, unverified.
**Edge cases:** Negative values cannot be shown in a pie; slices must sum to a meaningful whole.
**Likely follow-ups:** 1) *Donut instead?* Same problem, plus less area. 2) *Would you ever use a pie?* Yes, two or three slices, one dominant.
**Common mistakes:** 3D pies; pies with 10+ slices; not sorting; comparing two pies side by side.

### Q11 ⭐⭐ 🟢 How do you use colour effectively in a dashboard?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Colour as a tool for meaning, not decoration.
**Say this in the interview:** "I use a neutral base, such as grey and one brand colour, and keep bright colours for the thing I want noticed. Same colour always means the same thing. I use red/green sparingly and never as the only signal."
**Explain simply:**
- Grey for context, one strong colour for the focus.
- Colour has meaning: red for bad, blue for neutral series; keep it consistent on every page.
- Use sequential shades (light to dark) for amounts, and two-colour scales for above/below a midpoint.
- Check contrast so text is readable; about 4.5:1 for text is a common guideline (third-party source, unverified).
- Roughly 8% of men have red-green colour blindness (commonly cited figure, unverified), so add labels or icons (see Q24).
**Example:** Attrition bar chart: all bars grey, the two departments above 15% in dark red.
**Alternative:** Put the key values in bold labels instead of colour.
**Version / licensing note:** Report themes in Desktop (View > Themes) set colours centrally; from memory, unverified.
**Edge cases:** Dark mode or projectors wash out light colours; test on the real screen.
**Likely follow-ups:** 1) *How many colours?* A few. 2) *Why not rainbow?* No natural order, and it distracts.
**Common mistakes:** Default multi-colour palette everywhere; using red for something that is not bad; relying on colour alone.

### Q12 ⭐⭐ 🟢 What role do white space, alignment and visual hierarchy play in a dashboard?
**Asked at:** commonly asked; "balance, contrast, alignment, hierarchy, white space" is the suggested answer wording in a prep blog (eduyush, snippet only).
**What the interviewer is checking:** Do you know layout makes a dashboard readable?
**Say this in the interview:** "White space lets the eye rest and separates groups. Alignment makes the page look ordered and trustworthy. Hierarchy, by size, position and weight, tells the reader what to read first."
**Explain simply:**
- **White space** (empty space) is not wasted; it reduces clutter.
- **Alignment:** edges of visuals line up on a grid; Desktop has Format > Align and Distribute.
- **Hierarchy:** biggest and top-left = most important; supporting detail smaller.
- Together they let people scan without effort.
**Example:** Four KPI cards of the same size in a row, aligned, with equal gaps, above a trend chart twice as wide.
**Alternative:** Use a background grid or a template page to guarantee alignment.
**Version / licensing note:** Align/distribute tools are in Desktop (View/Format ribbon; exact menu names from memory, unverified).
**Edge cases:** Too much white space on a small mobile screen wastes room; use a separate mobile layout.
**Likely follow-ups:** 1) *How do you create hierarchy?* Size, position, colour, weight. 2) *What is a grid?* Invisible columns that visuals snap to.
**Common mistakes:** Visuals crammed edge to edge; slightly misaligned boxes; all text the same size.

### Q13 ⭐⭐ 🟢 Where on the page should the most important information be placed, and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowledge of reading patterns.
**Say this in the interview:** "Top-left, because people in left-to-right languages start there and scan across and down in a Z or F shape. The headline KPIs go there, with detail below and to the right."
**Explain simply:**
- Readers look first at the top-left and the largest element.
- Put summary at the top, trend in the middle, detail at the bottom.
- Microsoft's design tips, as recalled, recommend placing the most important view at top-left (from memory, unverified; page not reachable).
- Navigation and filters often sit left or top, consistently across pages.
**Example:** Top row: headcount, attrition, open roles cards. Middle: attrition trend. Bottom: department table.
**Alternative:** For right-to-left language audiences, mirror the layout.
**Version / licensing note:** Tool-independent; from memory, unverified.
**Edge cases:** On mobile the order is vertical, so most important goes at the top.
**Likely follow-ups:** 1) *Z or F pattern?* Both describe eyes moving across then down. 2) *Where do filters go?* Consistent spot, top or left.
**Common mistakes:** Burying the key KPI at the bottom; placing a logo or title in the prime position and wasting it.

### Q14 ⭐⭐ 🟢 Why do dashboards use KPI cards, and what context should a KPI card show?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a number alone is not information?
**Say this in the interview:** "A card gives one headline number at a glance. On its own it is meaningless, so I add context: the target, the change versus last period, and ideally a small trend and the time period."
**Explain simply:**
- A **KPI card** shows one key number, big and clear.
- Context: vs target, vs previous period (up or down), time period, and colour status.
- A small trend line (sparkline, see Q33) shows direction.
**Example:** October attrition is 1.8%, target 1.5%, last month 1.4%, so the card shows "1.8%, 0.3 points above target, up 0.4 points vs September" in red.
**Sample data:** table `Monthly` (reproduced in pandas)

| Month | Leavers | AvgHeadcount |
|---|---|---|
| Sep | 7 | 500 |
| Oct | 9 | 500 |

**DAX / Steps (not run here):**
```dax
Attrition % = DIVIDE ( SUM ( Monthly[Leavers] ), SUM ( Monthly[AvgHeadcount] ) )
Attrition Target = 0.015
Gap vs Target (pp) = [Attrition %] - [Attrition Target]
```
Steps (not run here): Visualizations pane > Card (or the newer "Card" visual) > drag `Attrition %` > add the gap measure to the callout/reference label.
**Alternative:** Use the KPI visual (value, goal, trend axis) instead of a plain card.
**Result:** Reproduced with pandas, not a DAX engine: Sep 1.4%, Oct 1.8%; vs target +0.3 points; month on month +0.4 points.
**Pandas check:**
```python
m["AttritionPct"]=(m.Leavers/m.AvgHeadcount*100).round(1)
# Sep 1.4, Oct 1.8 ; Oct - target 1.5 = 0.3 ; Oct - Sep = 0.4
```
**Version / licensing note:** Card/KPI visuals are in Desktop; new card visual vs classic names changed recently; from memory, unverified. DIVIDE not checked on Microsoft Learn (site unreachable).
**Edge cases:** DIVIDE returns blank when the denominator is zero; "up" is not always good (attrition up is bad), so colour the logic accordingly.
**Likely follow-ups:** 1) *Why DIVIDE?* Safe division. 2) *KPI vs card?* KPI adds goal and trend.
**Common mistakes:** Naked numbers; showing 1.8333333% instead of formatting; green for rising attrition.

### Q15 ⭐⭐ 🟢 How many visuals should you put on one report page?
**Asked at:** commonly asked (no company-specific report found); "limit visuals" advice appears in a consultancy blog (Al Rafay, snippet only).
**What the interviewer is checking:** Discipline and awareness of performance.
**Say this in the interview:** "There is no fixed law, but a good rule is roughly 5 to 8 visuals including cards. If the page needs more, I split it into pages or use drill-through. Fewer visuals are easier to read and load faster."
**Explain simply:**
- Each visual adds reading effort and queries that slow the page.
- The number is a guideline, not an official limit (the 5-8 range is common practice, unverified).
- Test: can a user find the key message in about five seconds?
**Example:** Overview page: 4 cards, 1 trend, 1 bar, 1 table = 7 visuals. Reasons for leaving move to a second page.
**Alternative:** Use bookmarks or tooltips to hide secondary detail.
**Version / licensing note:** The Performance Analyzer tool in Desktop (View > Performance analyzer) shows visual load times; from memory, unverified.
**Edge cases:** Dense operational screens (call-centre wallboard) may legitimately hold more.
**Likely follow-ups:** 1) *Do cards count?* Yes, they add load and clutter. 2) *How do you cut?* Remove what nobody would miss.
**Common mistakes:** Treating every requested metric as mandatory; quoting a number as a rule.

### Q16 ⭐⭐ 🟢 Why should you avoid 3D charts and decorative effects?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you value clarity over looks?
**Say this in the interview:** "3D distorts the data: bars at the back look smaller, slices at the front look bigger, and the added depth carries no information. Decorations like shadows and gradients use up attention. Clean flat charts are read faster and more accurately."
**Explain simply:**
- 3D adds a third visual dimension where the data has only two.
- Hard to read exact values; gridlines mislead.
- Decorative backgrounds, shadows and icons compete with the data (Tufte's data-ink idea, see Q35).
- Microsoft's design tips, as recalled, also advise against 3D (from memory, unverified).
**Example:** A 3D pie showing 30% and 28% slices makes the nearer one look bigger, which can mislead the HR head about which team is larger.
**Alternative:** A flat sorted bar chart.
**Version / licensing note:** Power BI has no true 3D chart in its default set; some custom visuals do (from memory, unverified).
**Edge cases:** A subtle brand banner or icon is fine if it does not distract.
**Likely follow-ups:** 1) *Any case for 3D?* 3D maps or real physical models, rarely. 2) *What about gradients?* Use only if they encode data.
**Common mistakes:** Fancy visuals to impress; heavy backgrounds behind charts.

### Q17 ⭐⭐ 🟢 What is the difference between a KPI and a metric?
**Asked at:** commonly asked as a gap-fill (not seen in any source; added from standard practice).
**What the interviewer is checking:** Conceptual clarity.
**Say this in the interview:** "A metric is any number you can measure. A KPI is a metric that is tied to a business goal, with a target, that tells you whether you're on track. All KPIs are metrics, but not all metrics are KPIs."
**Explain simply:**
- Metric: "number of applications received" (just a measure).
- KPI: "offer-acceptance rate, target 85%" (linked to the hiring goal).
- A KPI has a target, a time period and an owner.
- Too many KPIs and none of them is key.
**Example:** Metrics: headcount 500, leavers 9, applications 1,200. KPI: monthly attrition 1.8% vs target 1.5%.
**Alternative:** Quick test: "Does missing it make someone act?" If yes, KPI.
**Version / licensing note:** Conceptual; Power BI's "KPI" visual is only one way to show a KPI; from memory, unverified.
**Edge cases:** The same metric can be a KPI for one team and just context for another.
**Likely follow-ups:** 1) *KPI vs KRA?* KRA is a responsibility area; KPI measures it. 2) *Leading vs lagging?* Leading predicts (engagement), lagging reports (attrition).
**Common mistakes:** Calling everything a KPI; KPIs without targets.

### Q18 ⭐⭐ 🟢 What is decluttering in data visualization, and how do you apply it?
**Asked at:** commonly asked (no company-specific report found); the term is associated with Storytelling with Data (Knaflic), whose pages could not be fetched, so attribution is unverified.
**What the interviewer is checking:** Can you edit your own work down to the message?
**Say this in the interview:** "Decluttering means removing anything that does not help the reader: extra gridlines, borders, repeated labels, legends where direct labels work, and decorations. I then use the freed-up space for emphasis."
**Explain simply:**
- Every element costs attention (cognitive load: mental effort to read).
- Remove: heavy gridlines, chart borders, 3D, background images, duplicate axis titles.
- Replace the legend with direct labels; light grey for secondary text.
- Group related items using white space (Gestalt, Q36).
**Example:** A bar chart with 12 gridlines, a legend and a border becomes one with no gridlines, bars labelled with values, and one highlighted bar.
**Alternative:** The "squint test": blur your eyes; the key thing should still stand out.
**Version / licensing note:** Formatting pane options in Desktop (Visual > gridlines, borders, data labels); from memory, unverified.
**Edge cases:** Do not remove what users need, such as units or a source note.
**Likely follow-ups:** 1) *Where do you start?* Gridlines and borders. 2) *Is less always better?* No, remove only non-informative items.
**Common mistakes:** Removing axis labels people need; keeping defaults.

### Q19 ⭐⭐ 🟡 Describe a dashboard you built and the business decision it supported.
**Asked at:** commonly asked (no company-specific report found); dashboard walkthroughs are a standard DA interview item (Adaface, snippet only).
**What the interviewer is checking:** Real ownership, business impact, and your role.
**Say this in the interview:** "Use a story: situation, who needed it, what I built, the decision it supported, and the result. Example: an attrition dashboard that showed Support at 20% attrition and led to an onboarding programme." Use your own real project; do not copy the example.
**Explain simply:**
- Structure with STAR: Situation, Task, Action, Result.
- Name the data source, tools, and your specific contribution.
- Quantify the outcome, only with numbers you can defend.
- Mention one problem you solved (data quality, stakeholder change).
**Example (illustrative, not a real claim):** "HR reported attrition quarterly from Excel. I built a monthly Power BI report from HRIS data. It showed Sales and Support above 15%. Leadership started exit interviews there. Attrition in those teams fell over two quarters." Only say this if true for you.
**Alternative:** If you have no work project, use a personal or course project and say so honestly (an HR dataset from Kaggle, for example).
**Version / licensing note:** Not applicable.
**Edge cases:** If asked for impact you cannot prove, say what you observed and what you cannot attribute to the dashboard.
**Likely follow-ups:** 1) *What would you improve?* Mention one real limitation. 2) *How did you get data?* Name the system and refresh frequency.
**Common mistakes:** Describing visuals only; no decision or result; inventing numbers.

### Q20 ⭐⭐ 🟡 What is the difference between operational, analytical and strategic dashboards?
**Asked at:** commonly asked as a gap-fill (standard classification; no source found).
**What the interviewer is checking:** Matching design to purpose and audience.
**Say this in the interview:** "Operational dashboards track what is happening now for front-line teams, analytical ones let analysts explore why, and strategic ones show a few long-term KPIs for leaders."
**Explain simply:**
- **Operational:** real-time or daily, detail-heavy; example: today's attendance by shift.
- **Analytical:** interactive, filters, drill-down; example: attrition by tenure, manager, reason.
- **Strategic:** high-level, monthly or quarterly; example: headcount, attrition and cost vs annual plan.
- Refresh frequency, density and interactivity differ.
**Example:**

| Type | HR example | Audience | Refresh |
|---|---|---|---|
| Operational | Today's absentees by site | Supervisors | Hourly/daily |
| Analytical | Attrition drivers | HR analysts | Daily/weekly |
| Strategic | Workforce plan vs actual | CHRO | Monthly |

**Alternative:** Some authors use "tactical" in place of analytical.
**Version / licensing note:** Real-time/streaming and frequent refresh depend on licence and capacity; from memory, unverified.
**Edge cases:** One report can mix them, but usually better as separate pages.
**Likely follow-ups:** 1) *Which needs most interactivity?* Analytical. 2) *Which refreshes fastest?* Operational.
**Common mistakes:** Giving executives an analytical maze; giving analysts only top-level KPIs.

### Q21 ⭐⭐ 🟡 How would you show actual versus target in Power BI (card, gauge, bullet chart, variance)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you choose a clear actual-vs-target visual and build the variance measure?
**Say this in the interview:** "For one number, a card with the gap or the KPI visual. For many categories, a bar of actual with a target marker, or a bullet-style chart, plus a variance measure in a table with conditional colours. I avoid gauges because they use a lot of space for one number."
**Explain simply:**
- **Variance** = actual minus target; **variance %** = variance divided by target.
- **Card/KPI visual:** one headline.
- **Bar with target line/marker:** compare departments (a bullet chart is a bar plus a marker for target).
- **Gauge:** a dial; it works for one number but wastes space (Q42).
**Example:** Hires vs target by department this quarter.
**Sample data:** table `Hiring`

| Department | Actual | Target |
|---|---|---|
| Engineering | 42 | 50 |
| Sales | 60 | 55 |
| HR | 8 | 10 |
| Operations | 30 | 30 |
| Finance | 6 | 5 |

**DAX / Steps (not run here):**
```dax
Actual = SUM ( Hiring[Actual] )
Target = SUM ( Hiring[Target] )
Variance = [Actual] - [Target]
Variance % = DIVIDE ( [Variance], [Target] )
```
Steps (not run here): Build clustered bar with Actual > Format > add Target as a "Target"/reference value via the Bar chart's error bar or use a column+line combination; or use Visualizations > Bullet chart (custom visual from AppSource).
**Alternative:** Table or matrix with Variance % and conditional-format icons (Q23).
**Result:** Reproduced with pandas (not a DAX engine): Engineering -8 (-16.0%), Sales +5 (+9.1%), HR -2 (-20.0%), Operations 0 (0.0%), Finance +1 (+20.0%). Total row: actual 146, target 150, variance -4 (-2.7%).
**Pandas check:**
```python
d["Variance"]=d.Actual-d.Target; d["VarPct"]=(d.Variance/d.Target*100).round(1)
# Eng -8 -16.0 | Sales 5 9.1 | HR -2 -20.0 | Ops 0 0.0 | Fin 1 20.0 | total 146 150 -4 -2.7
```
**Version / licensing note:** Bullet chart is a custom visual from AppSource, not core; from memory, unverified.
**Edge cases:** Target 0 gives a blank from DIVIDE; the total variance % is computed on totals, not by averaging row percentages.
**Likely follow-ups:** 1) *Why not average the row %?* It would give a different answer. 2) *Where does the target live?* A separate table or the same one; keep it by period.
**Common mistakes:** Gauge with no scale; target not at same grain; averaging percentages.

### Q22 ⭐⭐ 🟡 How would you visualize a hiring funnel from application to joining?
**Asked at:** commonly asked as a gap-fill (no source found).
**What the interviewer is checking:** Choice of visual and the two conversion views (stage to stage vs overall).
**Say this in the interview:** "A funnel chart or, even better, a horizontal bar of stage counts with the percentage converted from the previous stage next to each bar. It shows where candidates drop off."
**Explain simply:**
- Each stage is a subset of the one before: applied, screened, interviewed, offered, joined.
- Show counts plus **conversion** (share that moves to the next stage).
- The funnel visual is easy but bars are easier to compare precisely.
- Slice by source or role to find the weak spot.
**Example:** 1,200 applied, 36 joined.
**Sample data:** table `Funnel`

| Stage | Candidates |
|---|---|
| Applied | 1200 |
| Screened | 480 |
| Interviewed | 150 |
| Offered | 45 |
| Joined | 36 |

**DAX / Steps (not run here):**
```dax
Candidates = SUM ( Funnel[Candidates] )
% of Applied = DIVIDE ( [Candidates], CALCULATE ( [Candidates], Funnel[Stage] = "Applied" ) )
```
Steps (not run here): Visualizations > Funnel > Group = Stage, Values = Candidates; sort by Candidates descending. Stage-to-previous needs a stage-order column and an OFFSET or a prior-stage column.
**Alternative:** Sorted horizontal bar with data labels; or a table with the percentages.
**Result:** Reproduced with pandas: % of previous stage: Screened 40.0, Interviewed 31.2, Offered 30.0, Joined 80.0; % of applied: 100, 40.0, 12.5, 3.8, 3.0.
**Pandas check:**
```python
f["PctOfPrev"]=(f.Candidates/f.Candidates.shift()*100).round(1)
f["PctOfApplied"]=(f.Candidates/f.Candidates.iloc[0]*100).round(1)
```
**Version / licensing note:** Funnel is a built-in visual; from memory, unverified. CALCULATE and DIVIDE not checked on Microsoft Learn (site unreachable).
**Edge cases:** Stages must be in business order, not alphabetical; candidates who skip a stage; time lag (an applicant may join next month).
**Likely follow-ups:** 1) *Biggest drop?* Screened to interviewed (31.2%). 2) *Cohort or snapshot?* Cohort by application month is fairer.
**Common mistakes:** Funnel sorted alphabetically; mixing stage-to-stage with overall percentages.

### Q23 ⭐⭐ 🟡 How do you highlight exceptions, such as departments above an attrition threshold, using conditional formatting?
**Asked at:** commonly asked as a gap-fill (HR attrition dashboard; no source found).
**What the interviewer is checking:** Rules-based highlighting that keeps the page calm.
**Say this in the interview:** "I put the threshold in a measure, then use conditional formatting by rules or by field value so bars, table cells or card text turn red when attrition is at or above 15%. Everything else stays grey."
**Explain simply:**
- **Conditional formatting** changes colour based on the data.
- Options: rules (if value >= 15% then red), gradient, or field value from a measure that returns a colour.
- Add an icon or text so it is not colour only (Q24).
**Example:** Departments with attrition of 15% or more.
**Sample data:** table `Attrition`

| Department | Leavers | AvgHeadcount |
|---|---|---|
| Sales | 30 | 150 |
| Support | 24 | 120 |
| Engineering | 18 | 240 |
| HR | 2 | 20 |
| Finance | 3 | 40 |
| Operations | 16 | 130 |

**DAX / Steps (not run here):**
```dax
Attrition % = DIVIDE ( SUM ( Attrition[Leavers] ), SUM ( Attrition[AvgHeadcount] ) )
Attrition Colour = IF ( [Attrition %] >= 0.15, "#C00000", "#A6A6A6" )
```
Steps (not run here): select the bar chart > Format visual > Bars > Colors > fx (conditional formatting) > Format style: Field value > choose `Attrition Colour`. For a table: Format > Cell elements > Background colour > fx > Rules.
**Alternative:** Rules without DAX: "If value >= 0.15 then red" in the fx dialog.
**Result:** Reproduced with pandas: Sales 20.0% red, Support 20.0% red, Engineering 7.5%, HR 10.0%, Finance 7.5%, Operations 12.3% (all normal).
**Pandas check:**
```python
a["AttritionPct"]=(a.Leavers/a.AvgHeadcount*100).round(1)
a["Flag"]=a.AttritionPct.apply(lambda x:"Red" if x>=15 else "Normal")
```
**Version / licensing note:** Conditional formatting exists in Desktop and Service; exact menu labels vary by build; from memory, unverified.
**Edge cases:** Small departments (HR: 20 people, 2 leavers) swing wildly; consider a minimum headcount. At the total level, the colour should apply to total attrition, not an average of rows. Blank values should not turn red.
**Likely follow-ups:** 1) *Where does the threshold live?* A parameter or table, so it can change. 2) *Boundary?* Decide >= or > and state it.
**Common mistakes:** Highlighting too many items; hard-coding 15% in many places; red/green only.

### Q24 ⭐⭐ 🟡 How do you make a Power BI report accessible and colour-blind friendly?
**Asked at:** commonly asked; accessibility guidance (colour-blind themes, not relying on colour alone, contrast, alt text) appears in third-party guides (UA accessibility, iSoftStone, snippets only).
**What the interviewer is checking:** Inclusive design awareness and practical steps.
**Say this in the interview:** "I don't rely on colour alone, I use a colour-blind-safe palette, check contrast, add alt text to visuals, set tab order and titles so screen readers can follow, and keep fonts large enough."
**Explain simply:**
- **Colour:** use blue/orange rather than red/green; add icons, labels or patterns.
- **Contrast:** dark text on light background; guideline of 4.5:1 for normal text (third-party, unverified).
- **Alt text:** a short description of each visual for screen readers.
- **Tab order and titles:** so keyboard users move in a logical sequence.
- **Themes:** apply an accessible theme and test in Desktop's colour-blind preview if available.
**Example:** Attrition bars: red for above threshold, but also a label "Above 15%" and a warning icon, so a colour-blind user still sees the exception.
**Alternative:** Use high-contrast built-in themes and test with a colour-blindness simulator on a screenshot.
**Version / licensing note:** Steps (not run here): select a visual > Format visual > General > Properties > Alt text; View > Selection pane/Tab order; View > Themes. Menu paths from memory, unverified; Microsoft accessibility page not fetched.
**Edge cases:** Custom visuals may not support screen readers; export-to-PDF loses interactivity.
**Likely follow-ups:** 1) *How do you test?* Screen reader, keyboard-only, simulator. 2) *Why alt text?* Blind users get the message in words.
**Common mistakes:** Colour as the only signal; low-contrast grey text; skipping alt text.

### Q25 ⭐⭐ 🟡 What makes a chart misleading (truncated axis, wrong scale, cherry-picked period), and how do you avoid it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you protect the reader from a wrong impression, even by accident?
**Say this in the interview:** "A chart is misleading when the picture says something bigger or smaller than the numbers do. I start bar axes at zero, keep scales honest and consistent, show a long enough period, and label what is plotted."
**Explain simply:**
- **Truncated axis:** the vertical axis starts at, say, 11.9 instead of 0. Bars are compared by their length, so a tiny change looks huge.
- **Wrong scale:** two charts side by side with different axis ranges, or a scale that jumps (0, 10, 50, 100), distort comparison. Use the same range for charts that are meant to be compared.
- **Cherry-picked period:** showing only the 3 months that fit the story and hiding the 2-year trend.
- Other traps: 3D effects, pies that do not add to 100%, unlabelled axes, dual axes scaled to force a correlation.
- Line charts may use a non-zero axis because the eye follows the slope, not the length; bars should not.
**Example:** Attrition went from 12.0% in Jan to 13.0% in Apr, a real rise of about 8.3%. A bar chart with the axis starting at 11.9% makes the April bar 11 times taller than January's.
**Sample data:** table `Attrition` (reproduced below)

| Month | Attrition % | Bar height, axis from 0 (Jan = 1) | Bar height, axis from 11.9 (Jan = 1) |
|---|---|---|---|
| Jan | 12.0 | 1.00 | 1.0 |
| Feb | 12.5 | 1.04 | 6.0 |
| Mar | 12.8 | 1.07 | 9.0 |
| Apr | 13.0 | 1.08 | 11.0 |

**DAX / Steps (not run here):** Power BI Desktop > Report view > select the visual > Visualizations pane > Format visual > Y axis > Range > set Minimum to 0 for bar/column charts. Add a title that states the period, e.g. "Attrition %, Jan-Apr 2026".
**Alternative:** If the change is genuinely small, show a line chart (slope) or a variance card ("+1.0 pt vs Jan") instead of a stretched bar.
**Result:** reproduced with pandas: the true rise is 8.3%, the truncated chart shows an 11x difference.
**Pandas check:**
```python
d["from0"]=d.Attrition_pct/d.Attrition_pct.iloc[0]
d["from11.9"]=(d.Attrition_pct-11.9)/(d.Attrition_pct.iloc[0]-11.9)
# Apr: 1.08 vs 11.0 ; true rise (13/12-1)*100 = 8.3
```
**Version / licensing note:** Axis range settings exist in Desktop and Service; from memory, unverified (learn.microsoft.com unreachable in this session).
**Edge cases:** Negative values need an axis that includes zero; log scales are fine only if labelled; a time axis with missing months silently hides gaps.
**Likely follow-ups:** "Is a non-zero axis ever OK?" Yes for lines or when zero is meaningless (e.g. temperature), if clearly labelled. "How do you pick the period?" Match the decision: at least one full business cycle or 12 months for seasonal data.
**Common mistakes:** Letting Power BI's auto axis pick a tight range; hiding the period in a slicer so the viewer cannot see it; using different scales on small multiples.

### Q26 ⭐⭐ 🟡 What is a Power BI theme, and why would you use one across reports?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you think about consistency and reuse, not just one report?
**Say this in the interview:** "A theme is a saved set of colours, fonts and visual formatting, stored as a JSON file. I apply one so every report looks the same, follows brand and accessibility rules, and I do not recolour each chart by hand."
**Explain simply:**
- **JSON file** = a small text file with settings written in a fixed format; Power BI reads it and restyles the report.
- A theme sets the colour palette for data series, text fonts and sizes, page background, and defaults for visuals (titles, borders, gridlines).
- Benefits: brand consistency, one change updates every visual, colour-blind-safe palette can be built in, new team members start with the right look.
- Power BI ships built-in themes, and you can import a custom JSON or save the current look.
**Example:** The HR analytics team of 5 builds 12 reports. A company theme (navy, teal, grey; red reserved for "bad") means every attrition and headcount report looks like one family and a rebrand is a single file swap.
**DAX / Steps (not run here):** Desktop > View tab > Themes group > pick a built-in theme, or Themes dropdown > Browse for themes (import JSON) / Customize current theme / Save current theme. Use the Themes gallery to reset.
**Alternative:** A report template (.pbit) carries layout plus theme plus model structure; a theme alone carries only styling.
**Version / licensing note:** from memory, unverified. Themes work in Desktop (Windows) and are stored in the report; no extra licence. learn.microsoft.com was unreachable here.
**Edge cases:** Manual formatting on a visual overrides the theme; a theme does not change data or page layout; fonts must be installed on viewers' machines or the Service uses a fallback.
**Likely follow-ups:** "Where do you get a theme?" Built-in, community galleries, or export your own. "Theme vs template?" See above.
**Common mistakes:** Hard-coding colours on every visual so the theme has no effect; using red/green as the only good/bad signal in the palette.

### Q27 ⭐⭐ 🟡 How do you structure a multi-page report so users move from overview to detail?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you design a guided path, not a pile of pages?
**Say this in the interview:** "Page 1 is a one-screen summary with headline KPIs; later pages go one level deeper by theme, and detail pages are reached by clicking, through drill-through or buttons. Each page answers one question."
**Explain simply:**
- **Overview first:** 4-6 KPIs and 2-3 charts that answer "are we OK?".
- **Analysis pages:** one theme each (attrition, hiring, attendance) with the same filters in the same place.
- **Detail pages:** row-level tables, reached by **drill-through** (right-click a data point to jump to a detail page already filtered to that item).
- **Navigation:** page navigator or buttons, a consistent menu, a "back" button.
- **Bookmarks** = saved states of a page (filters, visibility) used for view toggles.
**Example:** Overview shows company attrition 14%. User right-clicks "Sales" > Drill through > "Attrition detail" page filtered to Sales, listing exits by manager and tenure band.
**DAX / Steps (not run here):** Home > Insert > Buttons > Navigator > Page navigator. Drill-through: create the detail page, drag the field (e.g. Department) into Drill through > Add drill-through fields here. Page order: Overview first; hide detail pages via the page's eye icon (Format page, or right-click the tab > Hide).
**Alternative:** One-page report with bookmarks toggling summary and detail; or a separate summarised dashboard in the Service linking to the report.
**Version / licensing note:** from memory, unverified; learn.microsoft.com unreachable. Drill-through and buttons exist in Desktop and Service; no special licence.
**Edge cases:** Detail pages should show what filter is applied; sync slicers carefully so a filter on one page does not surprise users on another.
**Likely follow-ups:** "How many pages?" As few as answer the questions; 3-7 is typical. "Drill-down vs drill-through?" Drill-down moves down a hierarchy inside a visual; drill-through jumps to another page.
**Common mistakes:** Duplicating the same chart across pages; no way back; burying the headline on page 4.

### Q28 ⭐⭐ 🟡 How do you design a report layout for mobile users in Power BI?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the phone layout is a separate design step?
**Say this in the interview:** "I build the desktop report, then create a phone layout in Mobile layout view: fewer visuals, stacked vertically, with the key cards at the top and large touch-friendly items."
**Explain simply:**
- Phones are narrow and vertical, so pick the 3-5 most important visuals, not all of them.
- Cards and short bar charts work; wide tables and dense matrices do not.
- Order by importance because users scroll down.
- Keep slicers minimal; touch targets must be big enough for a finger.
- Test in the Power BI mobile app.
**Example:** For a store manager checking daily attendance on a phone: attendance % card, late-arrival card, absent-by-team bar, then a single slicer for date.
**DAX / Steps (not run here):** Desktop > View tab > Mobile layout (Mobile group) > drag visuals from the Page visuals pane onto the phone canvas > resize/arrange > Save. Visuals you do not place stay out of the phone view.
**Alternative:** Build one simple page design that works on both (mostly cards and vertical stacks) when no custom mobile layout is feasible.
**Version / licensing note:** from memory, unverified (learn.microsoft.com unreachable). Mobile layout is authored in Desktop; viewing in the mobile app needs access to the content, usually a Pro or equivalent licence to view shared reports; not verified.
**Edge cases:** Some visuals (custom visuals) may not render well in mobile; test dark mode and orientation.
**Likely follow-ups:** "Is mobile layout automatic?" No, it is designed per page. "What about the desktop version?" It stays unchanged.
**Common mistakes:** Cramming every visual into the phone canvas; forgetting to test on a real phone.

### Q29 ⭐⭐ 🟡 How do you collect feedback on a dashboard and iterate on its design?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you treat a dashboard as a product that improves, not a one-time delivery?
**Say this in the interview:** "I show early wireframes, watch real users try it, collect feedback in a simple log, check usage data, then release small changes and re-test. I fix what blocks decisions first."
**Explain simply:**
- **Before building:** a sketch or wireframe (a rough drawing of the layout) reviewed with 2-3 users.
- **After launch:** a 15-minute walkthrough where the user does a real task while you watch; do not explain.
- **Usage data:** see which pages and visuals are opened (Power BI usage metrics exist for report owners).
- **Feedback channel:** one place (a short form or a shared list) with date, who, what, priority.
- Prioritise by impact on decisions; communicate what changed, with a version note on the report.
**Example:** HR business partners ask "why is attrition different from my Excel?" Feedback: add a definition tooltip and a "last refreshed" stamp. v1.1 ships both within a week.
**DAX / Steps (not run here):** Service > workspace > report > ... > View usage metrics (if available) to see views per page; add a "Feedback" button via Insert > Buttons > Web URL linking to a form.
**Alternative:** A short pulse survey (3 questions) after each release; or a monthly 30-minute review with key users.
**Version / licensing note:** from memory, unverified (learn.microsoft.com unreachable). Usage metrics depend on workspace type and licence; check before promising them.
**Edge cases:** Loud users may not represent everyone; conflicting requests (see Q46).
**Likely follow-ups:** "How do you measure success?" Views, repeat users, fewer ad-hoc requests, decisions made. "How often do you change it?" In small, scheduled releases.
**Common mistakes:** Changing the dashboard after every comment; not telling users what changed; asking "do you like it?" instead of watching a task.

### Q30 ⭐⭐ 🟡 When is a dual-axis chart appropriate, and what are its risks?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use a tricky chart carefully?
**Say this in the interview:** "A dual-axis chart puts two measures with different units on one chart, left and right axis. It is fine for something like headcount (bars) and attrition % (line) over time, but the two scales can be stretched to fake a link, so I label both axes clearly or use two stacked charts."
**Explain simply:**
- **Dual axis** = one chart, two vertical axes with different scales (in Power BI: "Line and clustered column chart").
- Appropriate when the units differ (count vs %) and you want to see timing together.
- Risks: readers assume the lines cross meaning something; changing one axis range changes the apparent correlation; hard to read for beginners.
- Safer: two small charts sharing the same time axis, aligned vertically.
**Example:** Monthly joiners (bars, 20 to 60) and offer-decline % (line, 8% to 20%). Stretch the % axis and the line looks like it mirrors hiring, but it may just be noise.
**DAX / Steps (not run here):** Visualizations pane > Line and clustered column chart > Column y-axis: Joiners; Line y-axis: Offer decline %. Format visual > Y axis and Secondary Y axis: set titles and (optionally) ranges.
**Alternative:** Two charts stacked with the same X axis, or indexed lines (both set to 100 at the start).
**Version / licensing note:** from memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** Different axis zero points; colours must match axis titles; negative values on one axis.
**Likely follow-ups:** "Does a visual relationship mean correlation?" No; check with the actual statistic. "Alternative?" Scatter plot for relationship.
**Common mistakes:** Truncating the secondary axis to make lines overlap; using more than two series; forgetting axis titles.

### Q31 ⭐⭐ 🟡 How do you structure a presentation of findings: what goes first, what goes last?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you lead with what the audience cares about?
**Say this in the interview:** "Answer first: the headline and the recommendation up front, then the evidence, then the detail and risks, and I end with the decision I need and next steps."
**Explain simply:**
- **First:** the one-line conclusion and why it matters to the audience (the "so what").
- **Middle:** 2-3 supporting points, each with one clear chart.
- **Then:** caveats (data limits, assumptions), briefly and honestly.
- **Last:** the ask: decision, owner, deadline. Put long detail in an appendix.
- Time-box: executives get 5 minutes, analysts get the method.
**Example:** "Attrition in Sales is 22% vs 14% company-wide, costing about Rs 1.2 crore a year in replacement (illustrative). I recommend a retention review for Sales in Q1." Then three charts; then assumptions; then "I need approval for a pilot by 15 Dec."
**Alternative:** Situation-Complication-Resolution storyline (see Q37) for a longer story.
**Version / licensing note:** Not applicable (general practice; no Microsoft facts used).
**Edge cases:** Hostile audience: pre-wire key people before the meeting; bad news: still lead with it.
**Likely follow-ups:** "How long?" Shorter than you think. "How do you handle questions?" Appendix backup slides.
**Common mistakes:** Starting with methodology; ending with "thank you" and no ask; too many charts.

### Q32 ⭐ 🟢 What is the difference between a dashboard, a scorecard and an infographic?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the vocabulary of reporting formats?
**Say this in the interview:** "A dashboard is an interactive screen to monitor and explore; a scorecard tracks KPIs against targets; an infographic is a designed, static story for communication."
**Explain simply:**
- **Dashboard:** several visuals, usually live data, filters; for monitoring and drilling.
- **Scorecard:** a short list of KPIs with target, actual and status (red/amber/green); answers "are we on track?".
- **Infographic:** a one-time visual summary mixing text and graphics; for sharing, not exploring.
- Note: in Power BI, "dashboard" has a specific meaning too (a one-page canvas of pinned tiles in the Service) different from a "report" (multi-page, interactive).
**Example:** HR dashboard: attrition by dept with slicers. HR scorecard: 6 KPIs vs target. Infographic: "Year in numbers" poster for an annual townhall.
**Alternative:** Many teams use "dashboard" loosely; clarify with the stakeholder.
**Version / licensing note:** Power BI dashboard vs report distinction and Metrics/scorecards feature: from memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** A dashboard with targets and RAG status behaves like a scorecard.
**Likely follow-ups:** "Report vs dashboard in Power BI?" Report = multi-page, built in Desktop; dashboard = single page of pinned tiles in the Service.
**Common mistakes:** Calling every report a dashboard; making an infographic when users need to filter.

### Q33 ⭐ 🟢 What is a sparkline, and when would you use one next to a KPI?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you give numbers context cheaply?
**Say this in the interview:** "A sparkline is a tiny line chart without axes that shows the trend behind a number. Next to a KPI card it tells you whether 14% is rising, falling or stable."
**Explain simply:**
- No axes or labels; just the shape of the trend, in a small space.
- Best beside a KPI, or in table rows (one per department).
- It shows direction and volatility, not exact values.
- Pair with a comparison ("+1.0 pt vs last month").
**Example:** Attrition card shows 14%; sparkline over 12 months shows it climbing since July. Without it, 14% means little.
**DAX / Steps (not run here):** Add a Table or Matrix > Format visual > Cell elements > turn on Sparklines (choose the measure and the date axis). For a card-style tile, use the "Card (new)" visual if available in your build, or place a small line chart beside a card with axes hidden.
**Alternative:** An arrow plus percentage change, or a mini column chart.
**Version / licensing note:** Sparklines in tables/matrices were added to Desktop in 2021 as I recall; from memory, unverified (learn.microsoft.com unreachable); exact menu names change between builds.
**Edge cases:** Short or irregular history produces a misleading shape; consistent scales across rows are needed for comparison.
**Likely follow-ups:** "Can it show targets?" Not usually; use a bullet chart. "How many points?" Enough to show a trend, e.g. 12 months.
**Common mistakes:** Adding axes and legends (then it is no longer a sparkline); different scales on rows compared side by side.

### Q34 ⭐ 🟡 What are preattentive attributes, and how do you use them to direct attention?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know why a good design guides the eye?
**Say this in the interview:** "Preattentive attributes are visual features the brain notices in under a second, before you consciously look: colour, size, position, shape, boldness. I use one of them, usually a single bright colour, to point at the thing that matters."
**Explain simply:**
- Examples: colour (hue and intensity), size, position, orientation, bold text, enclosure.
- **Use sparingly:** if everything is bold or red, nothing stands out.
- Grey out everything else; highlight one bar in a strong colour.
- Caution: colour alone is not accessible; add a label or icon.
**Example:** Attrition by department: all bars grey, Sales bar in orange with label "22%". The viewer's eye lands there in under a second.
**DAX / Steps (not run here):** Format visual > Bars > Colors, or use conditional formatting (fx) to colour only values above threshold. Increase title size for headline KPI.
**Alternative:** Annotation with a text box and arrow.
**Version / licensing note:** Concept from data-visualisation practice (Knaflic / Few); not verified against a fetched source. Power BI menu paths from memory, unverified.
**Edge cases:** Colour-blind users; printing in greyscale.
**Likely follow-ups:** "Which is strongest?" Colour and position are very effective for noticing; size for quantity. "How many highlights?" One or two.
**Common mistakes:** Rainbow charts; highlighting every number.

### Q35 ⭐ 🟡 What is the data-ink ratio (Edward Tufte), and how does it guide chart design?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the classic principle behind decluttering?
**Say this in the interview:** "Tufte's data-ink ratio is the share of a chart's ink that actually shows data. The idea is to remove ink that adds nothing, like heavy gridlines, borders and 3D effects, so the data stands out."
**Explain simply:**
- Data-ink = ink that would be lost if you removed the data; non-data-ink = decoration.
- Rule of thumb: maximise the share, but not to the point of removing helpful labels or context.
- Practical: lighten or remove gridlines, delete borders and backgrounds, label bars directly, drop redundant legends.
- It is a guide, not a law; some context ink helps readers.
**Example:** A bar chart with a shaded background, thick gridlines, 3D bars and a legend for one series becomes: flat bars, direct labels, no gridlines. Same data, quicker read.
**DAX / Steps (not run here):** Format visual > Gridlines Off; Visual > Border off; Data labels On; Legend Off (single series).
**Alternative:** "Decluttering" from Storytelling with Data (see Q18).
**Version / licensing note:** Concept (Tufte, The Visual Display of Quantitative Information); not verified from a fetched source in this session.
**Edge cases:** Over-pruning removes axes needed for accuracy; dense tables may need light rules.
**Likely follow-ups:** "Is minimal always better?" No, clarity is the goal. "Related idea?" Chartjunk.
**Common mistakes:** Quoting it as "remove everything"; leaving default gridlines.

### Q36 ⭐ 🟡 What are the Gestalt principles (proximity, similarity, enclosure), and how do they apply to dashboards?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use psychology to organise a page?
**Say this in the interview:** "Gestalt principles describe how people group things automatically: items close together belong together, items that look alike are related, and items inside a box are a set. I use them to group visuals without adding clutter."
**Explain simply:**
- **Proximity:** place related visuals close and leave white space between groups.
- **Similarity:** same colour/shape means same meaning (all headcount visuals in blue).
- **Enclosure:** a light background panel groups related items; use sparingly.
- Also: alignment and continuity (eyes follow lines) help.
- The Microsoft dashboard design tips page referenced Gestalt (per the research sources file); I could not re-fetch it.
**Example:** Left block: three hiring KPIs close together on a pale grey panel; right block: attrition visuals. No dividers, no borders.
**DAX / Steps (not run here):** Insert > Shapes > Rectangle (light fill, send to back) behind related visuals; View > Gridlines and Snap to grid to align.
**Alternative:** Use spacing alone instead of boxes.
**Version / licensing note:** Concept; Power BI menu paths from memory, unverified.
**Edge cases:** Too many boxes create clutter; colour grouping fails for colour-blind users without other cues.
**Likely follow-ups:** "Which matters most on dashboards?" Proximity. "Do you use borders?" Only where grouping is unclear.
**Common mistakes:** Equal spacing everywhere so nothing groups; boxes around every visual.

### Q37 ⭐ 🟡 What narrative structure would you use for a data story (context, insight, recommendation)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you turn analysis into a story that leads to action?
**Say this in the interview:** "I use context, insight, recommendation: why it matters, what the data shows, what we should do. Each step is one slide or one chart, and the story ends with a decision."
**Explain simply:**
- **Context:** the business question, scope, and period in one or two lines.
- **Insight:** the finding, shown with one clear chart and a headline that states the point ("Sales attrition doubled in 6 months").
- **Recommendation:** specific action, owner, expected impact, timing.
- Add tension where possible: what happens if nothing changes.
- Keep supporting detail in an appendix.
**Example:** Context: "Offer declines affect our Q4 hiring target of 120." Insight: "Declines rose from 12% to 21%, mostly where offers are 10% below market." Recommendation: "Review offer bands for 3 roles; pilot for 1 month."
**Alternative:** Situation-Complication-Resolution, or the "answer first" pyramid (Q31).
**Version / licensing note:** Not applicable.
**Edge cases:** If the data is inconclusive, say so and recommend what to measure.
**Likely follow-ups:** "How is this different from a dashboard?" A story picks one message; a dashboard supports exploration.
**Common mistakes:** Insight with no recommendation; titles that name the chart instead of the finding.

### Q38 ⭐ 🟡 How do you handle a chart with too many categories (Top N, grouping into Other)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you simplify without hiding the story?
**Say this in the interview:** "I show the Top N that matter, group the long tail into 'Other' so the total still adds up, and let users drill into the detail on demand. I sort bars by value."
**Explain simply:**
- **Top N filter:** show only the N biggest by a measure (a built-in filter type in Power BI).
- **Grouping into Other:** the rest are summed so nothing disappears silently.
- Alternatives: a table with data bars, a search-enabled slicer, or a drill-through page.
- Always tell the reader how many are in "Other".
**Example:** 8 departments, 120 exits. Top 3 plus Other keeps the chart readable.
**Sample data:** table `Exits` (department totals); result of Top 3 + Other

| Dept | Exits | Share % |
|---|---|---|
| Sales | 42 | 35.0 |
| Support | 30 | 25.0 |
| Ops | 18 | 15.0 |
| Other (IT, Finance, HR, Legal, Admin) | 30 | 25.0 |

**DAX / Steps (not run here):**
1. Select the visual > Filters pane > Department > Filter type: Top N > Show items Top 3 > By value: Total Exits > Apply filter. This simply drops the rest (no "Other" bar).
2. For an "Other" bar, use a ranking measure and a grouping column. Sketch (from memory, unverified against Microsoft Learn):
```dax
Exits = SUM ( Attrition[Exits] )
Dept Rank = RANKX ( ALL ( Dept[Dept] ), [Exits] )
```
then a calculated column or a disconnected table that maps ranks above 3 to "Other". The right-click Group feature on a visual field (Data groups) is a simpler manual route.
**Alternative:** Keep all categories in a sorted bar chart with a scrollbar, or use a treemap.
**Result:** reproduced with pandas: Top 3 = 90 exits (75%), Other = 30 (25%), total 120.
**Pandas check:**
```python
top=d.sort_values("Exits",ascending=False).head(3)
other=d.sort_values("Exits",ascending=False).iloc[3:].Exits.sum()  # 30
```
Printed: Sales 42, Support 30, Ops 18, Other 30, total 120.
**Version / licensing note:** Top N filter and grouping exist in Desktop and Service; from memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** Ties at rank N; the Top N changes with filters, so "Other" size changes; a Top N filter hides items in totals unless you handle it.
**Likely follow-ups:** "Does the total change?" With a Top N filter the visual total shows only the shown items; with "Other" it adds up. "Dynamic N?" Use a what-if parameter.
**Common mistakes:** Dropping the tail without saying so; pie charts with 15 slices; unsorted bars.

### Q39 ⭐ 🟡 Which visual would you use to show a payroll change from last month to this month (waterfall)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the right visual for a start-to-end bridge?
**Say this in the interview:** "A waterfall chart. It starts with last month's payroll, adds or subtracts each driver such as new hires, increments, exits and overtime, and ends with this month's payroll, so you see exactly what moved the total."
**Explain simply:**
- **Waterfall chart** = floating bars that show how a starting value becomes an ending value through increases (up) and decreases (down).
- Each bar is a driver; first and last bars are the totals.
- Power BI colours increases, decreases and totals differently by default.
- Keep drivers to 5-8; group small ones.
**Example:** Payroll Rs 500 lakh last month, 530 this month: +40 new hires, +25 increments, -30 attrition savings, -5 overtime reduction, net +30 (6.0%).
**Sample data:** table `Payroll_Bridge` (Rs lakh)

| Driver | Amount |
|---|---|
| Last month payroll | 500 |
| New hires | +40 |
| Increments | +25 |
| Attrition savings | -30 |
| Overtime | -5 |
| This month payroll | 530 |

**DAX / Steps (not run here):** Visualizations pane > Waterfall chart > Category: Driver; Y axis: Amount. Set the first and last bars as totals via Format visual > Breakdown / Sentiment colours; or build a Driver column with the two totals as categories. 
**Alternative:** A clustered bar of drivers sorted by size, or a table with variance and conditional formatting.
**Result:** reproduced with pandas: running totals 500, 540, 565, 535, 530; net change +30, +6.0%.
**Pandas check:**
```python
d["Running"]=[500,540,565,535,530,530]
net=d.Amount[1:5].sum()  # 30.0 ; 30/500=6.0%
```
**Version / licensing note:** Waterfall is a built-in core visual in Desktop and Service; from memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** Mix of totals and drivers can be wrongly treated as increases; negative running totals; many tiny drivers.
**Likely follow-ups:** "Waterfall for time?" It can be used on a date axis but bridges are clearer. "Sort order?" Logical order, or by size.
**Common mistakes:** Drivers that do not add up to the ending value; using a pie for changes.

### Q40 ⭐ 🟡 How would you visualize employee attendance patterns by day and department (matrix with heatmap formatting)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you spot patterns across two dimensions at once?
**Say this in the interview:** "A matrix with departments in rows, weekdays in columns, attendance % in values, and background colour scale conditional formatting, so low-attendance pockets jump out."
**Explain simply:**
- **Matrix** = a pivot-style table with rows and columns; **heatmap** = colouring the cells by value.
- Use a single-hue or a diverging scale with a sensible midpoint.
- Show the value in the cell as well as colour (accessibility).
- Sort days Mon-Sun properly, not alphabetically.
**Example:** Ops on Friday: 79%, the lowest cell; IT is above 90% every day.
**Sample data:** table `Attendance` (Present %)

| Dept | Mon | Tue | Fri |
|---|---|---|---|
| IT | 96 | 97 | 90 |
| Ops | 88 | 94 | 79 |
| Sales | 92 | 95 | 84 |

**DAX / Steps (not run here):** Visualizations > Matrix > Rows: Department; Columns: Weekday (sorted by weekday number); Values: [Present %]. Format visual > Cell elements > Background colour > fx > Format style: Gradient > Minimum (red-ish) to Maximum (green-ish), or choose Rules.
```dax
Present % = DIVIDE ( SUM ( Attendance[Present] ), SUM ( Attendance[Scheduled] ) )
```
**Alternative:** A clustered column per department, or a calendar-style visual for daily patterns.
**Result:** reproduced with pandas (pivot of the table above): lowest cell Ops/Fri = 79; the DAX is not run here.
**Pandas check:**
```python
m=d.pivot(index="Dept",columns="Day",values="Present_pct")[["Mon","Tue","Fri"]]
m.stack().idxmin()   # ('Ops','Fri')
```
**Version / licensing note:** Conditional formatting on matrix cells is in Desktop and Service; from memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** Totals row may be coloured by another scale; blanks (no shift) should not be coloured as zero; small teams give noisy percentages.
**Likely follow-ups:** "Colour-blind safe?" Use blue-orange or a single hue and show numbers. "Why DIVIDE?" Safe division: returns blank instead of an error when dividing by zero.
**Common mistakes:** Average of averages instead of sum/sum; default alphabetical weekdays.

### Q41 ⭐ 🟡 Which chart would you use to show the distribution of salaries or tenure (histogram or box plot)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know distribution visuals and what Power BI offers natively?
**Say this in the interview:** "A histogram to see the shape: how many people fall in each salary band. A box plot to compare spread and outliers across groups. Power BI has no built-in histogram, so I create bins and use a column chart, or use a custom visual for the box plot."
**Explain simply:**
- **Histogram** = columns showing counts in ranges (bins), e.g. 0-20k, 21-40k.
- **Box plot** = box from the 25th to 75th percentile, a line at the median, whiskers for the range, dots for outliers.
- Averages hide skew; the distribution shows it.
- **Bins** = equal-size ranges you create (Power BI: right-click a numeric field > New group > Bin).
**Example:** 15 employees' monthly pay (Rs k): most below 30; one at 60 is an outlier. Mean 22.7 vs median 20.
**Sample data:** table `Salary` (Rs thousand): 3, 5, 8, 12, 14, 16, 18, 20, 22, 24, 28, 30, 35, 45, 60. Bins:

| Band | Count |
|---|---|
| 0-20 | 8 |
| 21-40 | 5 |
| 41-60 | 2 |
| 61-80 | 0 |

**DAX / Steps (not run here):** Fields pane > right-click Salary > New group > Group type: Bin > Bin size 20 > OK. Then Column chart: X axis: Salary (bins); Y axis: Count of EmployeeID. For a box plot, add a custom visual from AppSource (Insert > More visuals > From AppSource); availability may depend on your organisation's rules.
**Alternative:** A violin or density visual (custom), or a simple table of percentiles.
**Result:** reproduced with pandas: bin counts 8/5/2/0; quartiles 13/20/29; upper fence 53; outlier 60.
**Pandas check:**
```python
pd.cut(s,[0,20,40,60,80]).value_counts().sort_index()
q=s.quantile([.25,.5,.75]); fence=q[.75]+1.5*(q[.75]-q[.25])  # 53 ; outlier 60
```
**Version / licensing note:** Native histogram absence and AppSource custom visuals: from memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** Bin size changes the shape; blank salaries; very skewed data.
**Likely follow-ups:** "What is an outlier?" Common rule: beyond 1.5 x IQR (the spread between 25th and 75th percentile) from the box; a convention, not a law. "Mean or median?" Median for skewed pay.
**Common mistakes:** Showing only average salary; bins of uneven width.

### Q42 ⭐ 🟡 Why do some experts criticise gauge charts, and what would you use instead?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you pick visuals for clarity, not for looks?
**Say this in the interview:** "Gauges use a lot of space to show one number, are hard to read precisely, and give no history. I use a KPI card with variance to target, or a bullet chart, or a bar with a target line."
**Explain simply:**
- A gauge shows a single value against a min and max, like a speedometer.
- Criticisms: wasted space, angles are hard to compare, little context (trend, history).
- Better: card with target and variance, **bullet chart** (a bar with a target marker and bands), or a bar with a reference line.
- The Microsoft design tips page (per the research sources file) discusses bar vs pie vs gauge choice; I could not re-fetch it, so this is unverified.
**Example:** Hiring: 84 of 100 target. Card shows "84 / 100 (-16%)" with sparkline; a gauge shows only a needle at 84%.
**DAX / Steps (not run here):** Visualizations > Card (or KPI visual with target) or Bar chart with Format > Reference lines (Analytics pane > Constant/Target line).
**Alternative:** Gauge acceptable for one simple executive KPI with clear thresholds.
**Version / licensing note:** from memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** Gauge with min/max/target settings that do not match the measure shows misleading fill.
**Likely follow-ups:** "When is a gauge OK?" Rarely; single metric, strong thresholds. "Bullet chart in Power BI?" Via a custom visual or a bar with target line.
**Common mistakes:** A page of 6 gauges; leaving max at a default that makes everything look "full".

### Q43 ⭐ 🟡 How do you keep dashboards consistent across a team (templates, style guide, naming)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you work in a team and scale standards?
**Say this in the interview:** "A shared style guide, a Power BI template with the theme and layout already set, naming conventions for measures, and peer review before publishing."
**Explain simply:**
- **Template (.pbit):** a report file with theme, page layout and model structure but no data, to start every new report.
- **Style guide:** colours, fonts, chart choices, title formats, where filters go.
- **Naming:** clear measure names (e.g. `Attrition %`), folders for measures, one table for measures.
- **Review:** a simple checklist before publishing; versioning of files.
- Shared semantic model (a published data model many reports reuse) keeps numbers consistent.
**Example:** Five analysts, five attrition definitions, five different numbers. A shared model with one `Attrition %` measure and a common theme ends the debate.
**DAX / Steps (not run here):** Desktop > File > Save as > Power BI template (.pbit). Publish a certified/promoted semantic model in the Service workspace.
**Alternative:** A written checklist only (low effort).
**Version / licensing note:** Template saving is a Desktop feature; promoting/certifying content in the Service may need specific licences or roles; from memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** Templates drift unless owned by someone; changes to the theme do not auto-update old reports.
**Likely follow-ups:** "Who owns the style guide?" A named owner. "How do you enforce it?" Review checklist.
**Common mistakes:** Copy-pasting old reports and dragging old errors along; each person defining the same KPI differently.

### Q44 ⭐ 🟡 What would you check when reviewing a colleague's cluttered dashboard?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you critique constructively with a method?
**Say this in the interview:** "I start with the purpose and audience, then check the hierarchy, number of visuals, chart choice, colour, labels, and accuracy. I give specific, kind suggestions, not just 'it is messy'."
**Explain simply:**
- **Purpose:** can I say in one sentence what decision this supports?
- **Layout:** most important top left, aligned, white space, grouped sensibly.
- **Visuals:** too many? wrong chart types? pie with many slices, 3D?
- **Clutter:** gridlines, borders, repeated legends, unlabeled axes.
- **Colour:** meaningful, consistent, accessible.
- **Accuracy and performance:** definitions, filters, axis, refresh time (the Performance Analyzer tool measures visual speed).
**Example:** 18 visuals, 3 pies, red used for both "good" and a brand colour. Suggest cutting to 7 visuals, one highlight colour, pushing detail to a drill-through page.
**DAX / Steps (not run here):** Desktop > View tab > Performance analyzer > Start recording > Refresh visuals. Selection pane (View > Selection) shows the objects and order.
**Alternative:** A written checklist with scores.
**Version / licensing note:** from memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** The "clutter" may be a power user's request; ask first.
**Likely follow-ups:** "How do you give feedback?" Specific, with a suggested fix, praise what works.
**Common mistakes:** Restyling without understanding the user; critiquing taste instead of clarity.

### Q45 ⭐ 🔴 A leader has asked for 15 metrics on one page. How do you handle the request and redesign it?
**Asked at:** commonly asked (no company-specific report found; "stakeholder asks for too much" appears in generic prep lists, not as a named-company report)
**What the interviewer is checking:** Can you push back politely and still deliver value?
**Say this in the interview:** "I ask what decisions those metrics support, then group them: 4-5 headline KPIs on top, the rest one click away on detail pages. I show a quick mock-up so the leader sees the trade-off."
**Explain simply:**
- Clarify first: "Which 3 questions do you ask every Monday?"
- Rank metrics: decision-critical vs nice to have.
- Redesign: top row of 4-6 KPI cards with comparison; a trend or breakdown below; remaining metrics on drill-through or a second page.
- Offer a scorecard-style table if they truly want everything visible, with conditional formatting.
- Agree to review after 4 weeks using usage data.
**Example:** 15 HR metrics become: headcount, attrition %, time-to-hire, offer acceptance %, absenteeism % (top row). Cost per hire, tenure, training hours and others move to a "Details" page.
**DAX / Steps (not run here):** Insert > Buttons > Navigator > Page navigator; set up Drill through to detail pages (see Q27). Use a Table with conditional formatting for the compact all-metrics view.
**Alternative:** Role-specific pages (finance view, HR view), a tip from a consultancy blog in the sources file, snippet only.
**Version / licensing note:** from memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** A leader may insist; deliver both and let usage data decide.
**Likely follow-ups:** "What if they refuse?" Build as asked, plus the simpler view, and review usage. "How do you decide the top 5?" Link to goals.
**Common mistakes:** Saying no without an alternative; cramming 15 cards in tiny font.

### Q46 ⭐ 🔴 Two stakeholders want conflicting things from the same dashboard. How do you resolve it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Stakeholder management, not just technical skill.
**Say this in the interview:** "I find the underlying need behind each request, check which supports the dashboard's main decision, and look for a design that serves both, like separate pages. If it is still a real conflict, I escalate to the dashboard owner for a decision."
**Explain simply:**
- Ask each "what decision will you make with this?"; requests often differ on form, not need.
- Options: separate views or pages, a toggle (bookmark), role-based pages, or two dashboards.
- Agree the primary audience and success measure up front.
- Document the decision and share it with both.
- If definitions conflict (e.g. attrition counts), agree one official definition.
**Example:** Finance wants cost per employee; HR wants engagement scores on the main page. Solution: shared overview, plus a Finance page and an HR page.
**DAX / Steps (not run here):** Insert > Bookmarks and Buttons to toggle views; or separate pages with navigator.
**Alternative:** Sponsor decides if priorities collide.
**Version / licensing note:** Row-level security (limits which rows a person sees) can give each group a different view; needs Service set-up; from memory, unverified (learn.microsoft.com unreachable).
**Edge cases:** One stakeholder is more senior; do not let seniority replace a clear criterion.
**Likely follow-ups:** "Who decides?" The dashboard owner/sponsor. "What if both are equal?" Escalate with options and a recommendation.
**Common mistakes:** Quietly building both and confusing users; taking sides.

### Q47 ⭐ 🔴 How would you present a finding that contradicts a senior leader's long-held belief?
**Asked at:** commonly asked (no company-specific report found; a "surprising finding vs CEO belief" question is mentioned in generic prep sites in the sources file, snippet only)
**What the interviewer is checking:** Courage, tact and rigour.
**Say this in the interview:** "I first recheck the data and method, then share privately before any big meeting, start with what we agree on, show the evidence simply, and frame it as new information with a suggested next step, not as 'you were wrong'."
**Explain simply:**
- Validate: recheck data, definitions, sample size, alternative explanations.
- Pre-wire: show the leader (or their trusted colleague) in a one-to-one first.
- Start with shared goals ("we both want lower attrition").
- Let the data speak: one clear chart, plain wording, state uncertainty.
- Offer a low-risk test (pilot) if the conclusion is uncertain.
- Be open to being wrong: ask what could explain it.
**Example:** The leader believes salary is why people leave. Exit data shows 60% of leavers cite manager issues, and pay was similar to market. You show this privately, propose a 2-month manager-feedback pilot.
**DAX / Steps:** Not applicable (no tool step).
**Alternative:** Bring a neutral third party's benchmark; run an A/B pilot to let the evidence settle it.
**Version / licensing note:** Not applicable.
**Edge cases:** Data may have quality limits; say them. Culture: some leaders prefer hearing it privately.
**Likely follow-ups:** "What if they dismiss it?" Keep the evidence documented, propose a test, escalate carefully. "What if you are wrong?" Acknowledge and update.
**Common mistakes:** Surprising the leader in public; hiding behind complex stats; softening the message until it disappears.
