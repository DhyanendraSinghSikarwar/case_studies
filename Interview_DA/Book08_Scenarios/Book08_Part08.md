# Book 8 — Scenario-Based & Data Interpretation | Part 8: Project Deep-Dive Questions 🟡

**Target:** 60 questions | **Actual:** 62 questions
**Scope:** Project-agnostic deep-dive questions an interviewer asks about any analytics project, each to be answered with a structure the candidate fills from their own project, plus HR-analytics project angles (attrition, hiring funnel, HRIS data, privacy).

### Q1 ⭐⭐⭐ 🟢 Walk me through your project in two minutes: how would you structure the answer so that the business problem, your role, the method and the result are all covered?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs appear in many prep guides and in about 14 profiles of the internal interview compilation (unverified as to any one company).
**What the interviewer is checking:** Whether you can give a clear, ordered, honest summary instead of a tool list.
**Say this in the interview:** "I will give it in four parts: the problem, my role, what I did, and what changed. About two minutes, then you can dig anywhere."

**Answer structure (about 20 seconds each, 6 sentences in total, so about two minutes):**
1. Problem and user: "HR wanted to know why first-year employees were leaving, and the HR head would use the answer."
2. My role: "I owned data preparation and the dashboard; the model/template came from the team." (say only what is true)
3. Data and method: source, size, the key cleaning step, the main technique.
4. Result: one number and one sentence a manager would repeat.
5. Impact or recommendation, and one limit.
6. Close by inviting questions: "Happy to go deeper on cleaning or the metric definitions."

**Illustrative project, replace with your real one:** "HR could not explain a 13.4% yearly attrition rate. I was the analyst on a team of two. I cleaned a 1,480-row HRIS export (the export from the HR system that holds employee records) down to 1,350 unique employees, defined attrition with HR, and built an Excel and Power BI view. It showed that 63 of 162 exits (39%) happened in the first year, although first-year staff were only about 15% of headcount. We recommended a 90-day check-in; the effect is not yet measured."
(13.4% = 162 exits / 1,205 average headcount; all figures are invented exercise data.)

**Likely follow-ups:** 1) *Which part took longest?* Cleaning; name the step. 2) *What would you change?* One honest improvement. 3) *Can you go slower on the method?* Have a 30-second version ready.
**Common mistakes / traps:** Starting with tools; talking five minutes; saying "we" for everything; no number in the result.

### Q2 ⭐⭐⭐ 🟢 What was the business problem or question behind your project, and who was going to use the answer?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That your work started from a decision, not from a dataset.
**Say this in the interview:** "The question was X, the user was Y, and the decision it fed was Z."

**Answer structure:**
1. State the question in business words, not "I analysed a dataset".
2. Name the user by role (HR head, sales manager, finance lead).
3. Name the decision it supports and what would be done with each possible answer.
4. If it was a course project with no real user, say so, then name the realistic user you designed for.

**Illustrative project, replace with your real one:** "The HR head asked: where are we losing people, and are the exits early or late in tenure? She would decide whether to invest in onboarding or in salary reviews. If exits were concentrated in year one, onboarding; if spread across senior staff, pay and growth."

**Likely follow-ups:** 1) *How did you know this was the real question?* I asked what she would do differently with the answer. 2) *Did the question change?* Describe honestly (see Q20).
**Common mistakes / traps:** Inventing a client for a self-study project; stating a vague goal ("improve retention"); no named user.

### Q3 ⭐⭐⭐ 🟢 What was your own contribution to the project, as distinct from what the team, your guide or a template provided?
**Asked at:** commonly asked (no company-specific report found); contribution probes are reported for some analyst interviews in prep sources (unverified).
**What the interviewer is checking:** Honesty and ownership; whether you can really defend what is on the resume.
**Say this in the interview:** "I will separate what I did myself from what I was given. I owned these three pieces and I can show them."

**Answer structure:**
1. List 2-4 concrete things you did yourself (the cleaning rules, the SQL, the DAX measures, the charts).
2. List what others provided (the dataset, the guide's outline, a template, the model from a lead).
3. Say what you changed in anything provided, and why.
4. Offer proof: "I can open the file and show the step."

**Illustrative project, replace with your real one:** "The data export came from the HR team and my mentor suggested the dashboard layout. I wrote the duplicate and transfer rules, defined attrition, built the monthly attrition measure, and added the tenure-band chart, which was not in the layout I was given."

**Likely follow-ups:** 1) *Show me one thing you built.* Be ready to open it. 2) *What did the mentor change?* Name one correction you accepted.
**Common mistakes / traps:** Claiming the whole project; hiding the template; being unable to show your own piece.

### Q4 ⭐⭐⭐ 🟢 Where did the data for your project come from, how large was it, and how did you check that it was fit for the question?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know your data's origin, grain and quality, not only the model.
**Say this in the interview:** "Source, size, then three fitness checks: coverage, definitions and consistency."

**Answer structure:**
1. Source and owner (system, export date, public or internal).
2. Size and grain: rows, columns, "one row per employee per month" or "per employee".
3. Fitness checks: time coverage covers the question; key fields filled; totals reconcile to an outside figure; no unexplained duplicates.
4. What was NOT in the data that you wished for.

**Illustrative project, replace with your real one:** "HRIS export, 1,480 rows, one row per employee record, 24 months. Checks: join/exit dates present for the full period, headcount reconciled (opening 1,210 + 152 hires - 162 exits = 1,200 closing, matching the HR report), 90 exact duplicate rows, and 40 transferred employees with two rows each, leaving 1,350 unique employees (1,480 - 90 - 40). Missing: exit reasons were free text and unreliable."

**Likely follow-ups:** 1) *How did you reconcile?* Against HR's own monthly headcount report. 2) *Was it representative?* Say one company, one period; no wider claim.
**Common mistakes / traps:** "I downloaded it from Kaggle" and nothing more; no row count; skipping the grain.

### Q5 ⭐⭐⭐ 🟢 What data cleaning did you do in your project, and which cleaning decision had the biggest effect on the result?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That cleaning was deliberate, recorded and understood for its impact.
**Say this in the interview:** "I did four cleaning steps; one of them, the treatment of transfers, changed the headcount base and so the rate."

**Answer structure:**
1. List steps in order: duplicates, missing values, standardised names/dates, outliers.
2. For each, the rule and rows affected.
3. Pick the one with the biggest effect and show before and after.
4. Say how you recorded it (cleaning log).

**Illustrative project, replace with your real one:** 1,480 rows; 90 exact duplicates removed (1,390); 40 employees with two rows from a department transfer collapsed to one (1,350 unique). The big decision was how to count transfers: counting both rows would have inflated headcount by 40 and counted a transfer as a leaver in the old department. Keeping the latest record and treating transfers as non-exits kept the rate honest.

**Likely follow-ups:** 1) *Why not delete missing rows?* Removing them can bias the result; record and decide. 2) *Did you test the sensitivity?* Rerun with the other choice and report the gap.
**Common mistakes / traps:** Saying "cleaned the data" without detail; deleting blanks silently; no before-and-after counts.

### Q6 ⭐⭐⭐ 🟢 Which tools did you use in the project (SQL, Excel, Python, Power BI or Tableau), and why that tool for each step rather than another?
**Asked at:** commonly asked (no company-specific report found); tool-choice probes are listed in prep sources (unverified).
**What the interviewer is checking:** That tool choice followed the task, not habit.
**Say this in the interview:** "Each tool for the step it suits: SQL to extract and filter, Excel for quick checks, Power BI to share."

**Answer structure:** A small table in words: step, tool, reason, and the alternative you rejected.
1. Extract and join: SQL (repeatable, handles volume).
2. Quick checks and pivot sanity: Excel (fast to eyeball).
3. Statistics or modelling: Python, only if needed.
4. Share: Power BI or Tableau (HR can filter without me).

**Illustrative project, replace with your real one:** "SQL for a clean employee table; Excel pivots to cross-check the headcount; Power BI for the dashboard because HR already had licences. I did not use Python modelling, because a descriptive question did not need it."

**Likely follow-ups:** 1) *Why not do all in Excel?* Volume, repeatability and auditability. 2) *Why not Python for the charts?* Users need slicers, not code.
**Common mistakes / traps:** Listing tools you only touched once; claiming Python for a project done in Excel.

### Q7 ⭐⭐⭐ 🟢 What was the key insight or result of your project, and how would you state it in one sentence to a non-technical manager?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can reduce an analysis to a plain, quantified message.
**Say this in the interview:** "One sentence, one number, one 'so what'."

**Answer structure:** Insight = who/what + size + comparison + so-what. Avoid method words.

**Illustrative project, replace with your real one:** First-year employees are about 15% of staff but account for 39% of exits (63 of 162), so the problem is in onboarding, not pay for senior staff. Computed: first-year exit rate about 35% versus about 9.7% for everyone else (on average headcounts of 180 and 1,025; invented data).
**One-line version for a manager:** "Roughly one in three new joiners leaves within a year, about three and a half times the rate of other staff."

**Likely follow-ups:** 1) *Is that causal?* No; it shows where, not why (see Q26). 2) *Is the number stable?* Check another period.
**Common mistakes / traps:** Reading out a statistical result; no comparison; claiming a cause.

### Q8 ⭐⭐⭐ 🟢 What business impact did your project have, and if it was a learning or portfolio project, how would you describe the impact you would expect in a real setting?
**Asked at:** commonly asked (no company-specific report found); quantifying impact is a standard STAR theme in prep sources (unverified).
**What the interviewer is checking:** Whether you separate achieved impact from expected impact.
**Say this in the interview:** "Real impact I will state only if it was measured; otherwise I will say clearly 'expected' and show the assumption."

**Answer structure:**
1. Real impact: only measured effects (time saved, a decision changed). Say how measured.
2. Portfolio project: say "no real deployment", then give expected impact with the arithmetic and the assumption.
3. Name the metric you would track to confirm it.

**Illustrative project, replace with your real one:** "Not deployed. If a 90-day check-in cut first-year exits by a quarter, that is about 16 fewer exits (63 x 0.25 = 15.75). At an assumed 2 lakh rupees per exit (my assumption, to be replaced with HR's figure), that is about 32 lakh a year. Separately, the dashboard replaced a manual report of about 6 hours a week with about 1.5, a 75% saving, which I timed myself."

**Likely follow-ups:** 1) *Where does 25% come from?* An assumption, not a finding; show a range. 2) *How would you confirm it?* Compare first-year exit rate before and after for matched cohorts.
**Common mistakes / traps:** Presenting an estimate as achieved; no assumption stated; huge round-number claims.

### Q9 ⭐⭐⭐ 🟢 What was the hardest problem you faced in the project, and how did you solve it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Problem-solving process and honesty, not heroics.
**Say this in the interview:** "The hardest part was X. I tried A, it failed because B, then I did C and verified it."

**Answer structure (STAR):** Situation and task in one line; the obstacle; what you tried (including a failed attempt); the fix; how you verified; what you learned.

**Illustrative project, replace with your real one:** "Headcount did not match HR's report. My first attempt, removing duplicates only, still left me 40 short of a clean base. Checking the extra rows by ID showed they were transfers with two records. I kept the latest record, re-ran, and the closing headcount matched at 1,200."

**Likely follow-ups:** 1) *Who helped?* Name them honestly. 2) *How did you know it was fixed?* The reconciliation tied out.
**Common mistakes / traps:** Choosing a trivial problem; no failed attempt; blaming the data owner.

### Q10 ⭐⭐⭐ 🟢 If you could redo the project, what would you do differently?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Self-awareness and growth, not perfection.
**Say this in the interview:** "Two things: I would agree definitions earlier, and I would test the result in a second period."

**Answer structure:** 1-2 specific changes, each with the reason and what it would have improved. Pick changes in process (definitions, validation, documentation), not "use a better model" only.

**Illustrative project, replace with your real one:** "I would fix the attrition definition with HR in week one; I lost two days when I discovered they excluded contract staff. I would also validate on a second year of data before showing the first-year finding."

**Likely follow-ups:** 1) *Why did you not do it then?* Time and a late discovery; say it plainly. 2) *What is the biggest remaining gap?* Name it (see Q27).
**Common mistakes / traps:** "Nothing"; a fake weakness ("I work too hard"); blaming others.

### Q11 ⭐⭐⭐ 🟢 Why did you choose this topic or project, and how does it relate to the role you are applying for?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Motivation and fit; whether the project connects to the job.
**Say this in the interview:** "I chose it because it uses the data I know from HR, and the skills carry directly to this role."

**Answer structure:** Personal link (your background), skill link (what the project proves: SQL, dashboards, stakeholder work), role link (name a team problem this role would have).

**Illustrative project, replace with your real one:** "From years in HR operations I knew attrition is where HR is asked the hardest questions with the weakest data. The project exercised the skills this role needs: cleaning HRIS data, defining a metric, and presenting to a non-technical user."

**Likely follow-ups:** 1) *Would you do another domain?* Yes; the method transfers (Q55). 2) *Why not a more advanced model?* The question needed description first.
**Common mistakes / traps:** "It was the assignment"; no link to the role; overselling the difficulty.

### Q12 ⭐⭐⭐ 🟢 How did you validate that your numbers were correct before you shared them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Habit of checking before publishing.
**Say this in the interview:** "I reconcile to a known total, test edge cases, and have someone else look at one figure."

**Answer structure (checklist):**
1. Reconcile to an independent source (HR's report, finance total).
2. Row-count and sum checks before and after every join or filter.
3. Recompute one figure a second way (a pivot against the SQL result).
4. Sanity ranges (a rate cannot exceed 100%; no negative tenure).
5. Peer or owner review of definitions.

**Illustrative project, replace with your real one:** Opening 1,210 + hires 152 - exits 162 = 1,200, equal to the system closing headcount; average headcount (1,210 + 1,200)/2 = 1,205; rate 162/1,205 = 13.4%, matching the Excel pivot.

**Likely follow-ups:** 1) *What if reconciliation had failed?* Stop and trace the gap before sharing. 2) *Did anyone else review?* Say honestly.
**Common mistakes / traps:** "I checked it looked right"; validating with the same formula you built.

### Q13 ⭐⭐⭐ 🟢 An interviewer says: "Your resume lists a dashboard project. Explain the dashboard: who the audience was, which KPIs you showed and why those." How do you answer?
**Asked at:** commonly asked (no company-specific report found); dashboard-project walk-throughs and Excel screenshares are reported for some retail/e-commerce analyst loops in prep sources (unverified).
**What the interviewer is checking:** Whether KPIs were chosen for a user and a decision.
**Say this in the interview:** "Audience first, then each KPI with the question it answers."

**Answer structure:**
1. Audience and how they use it (weekly review, 10 minutes, on laptop).
2. 4-6 KPIs, each with definition and why.
3. One-line layout logic: summary on top, drill-down below.
4. What you left off and why.
5. Usage or feedback, if any.

**Illustrative project, replace with your real one:** Audience: HR head and business-unit HR partners. KPIs: monthly attrition rate (13.4% yearly equivalent), voluntary vs involuntary split (138 vs 24 of 162 exits), first-year exit share (39%), headcount trend, and department rate. Left off: exit-interview scores (too sparse).

**Likely follow-ups:** 1) *Which KPI would you cut?* Name one (Q32). 2) *How do they filter?* Slicers for department and period.
**Common mistakes / traps:** Listing every chart; no audience; KPIs with no definition.

### Q14 ⭐⭐⭐ 🟢 You are asked to explain a project that you did as part of a team of four. How do you talk about it honestly without over-claiming or under-selling your part?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Honesty, teamwork and clarity about your contribution.
**Say this in the interview:** "I will say 'we' for the team result and 'I' for my piece, and name exactly which pieces were mine."

**Answer structure:**
1. One sentence on the team goal and your role.
2. "We" for decisions shared; "I" for work you did, each with a concrete artifact.
3. Credit teammates by function, without hedging your own work.
4. Be ready to demo your part and to explain the parts you did not build at a high level.

**Illustrative project, replace with your real one:** "Our team of four built the attrition analysis. I did the data cleaning and the dashboard; one teammate did the survey data, one the stakeholder meetings, one the report text. I can explain the model they used at a high level but I did not build it."

**Likely follow-ups:** 1) *Why only describe your part?* So you can defend every word. 2) *Any conflict?* Be factual and brief.
**Common mistakes / traps:** "I built the whole thing"; "I just helped"; unable to explain teammates' parts at all.

### Q15 ⭐⭐⭐ 🟡 Your project resume line says "improved efficiency by 20%". The interviewer asks how that 20% was measured. What do you say, and what if it was an estimate?
**Asked at:** commonly asked (no company-specific report found); impact-quantification probes appear in prep sources (unverified).
**What the interviewer is checking:** Whether your claims are verifiable and honestly labelled.
**Say this in the interview:** "Here is the baseline, the after-figure and how I timed it. If it was an estimate, I will say so and show the assumptions."

**Answer structure:**
1. Metric: what efficiency means (hours, steps, turnaround).
2. Baseline and after, with sample size and how timed.
3. The arithmetic: (before - after) / before.
4. If estimate: say "estimated", state the basis, give a range, and offer to fix the resume wording.

**Illustrative project, replace with your real one:** A weekly report took about 6 hours by hand and about 1.5 hours after automation; (6 - 1.5)/6 = 75%. If I had only guessed, I would write "cut weekly report time from about 6 to about 1.5 hours (my timing over 4 weeks)", not a percentage I cannot defend.

**Likely follow-ups:** 1) *Was there a control?* No; so it is a before-after comparison, not proof of cause. 2) *Would you change the bullet?* Yes, to what is verifiable.
**Common mistakes / traps:** Defending an invented number; confusing percent with percentage points; saying "I do not remember" about your own claim.

### Q16 ⭐⭐⭐ 🟡 The interviewer asks: "Why did you use that method or chart or model and not an alternative?" How do you justify a technical choice in a project?
**Asked at:** commonly asked (no company-specific report found); "why this approach over others" is a listed practice prompt (unverified).
**What the interviewer is checking:** Reasoning, trade-offs and awareness of alternatives.
**Say this in the interview:** "I chose it because of the question and the audience; here is the alternative I considered and why I did not pick it."

**Answer structure:**
1. The need (question, data size, audience).
2. The choice and one reason tied to the need.
3. One alternative and the trade-off (what you gave up).
4. A condition under which you would switch.

**Illustrative project, replace with your real one:** "I used a tenure-band bar chart with rates, not a pie of leavers, because the question compared rates across groups. Counts alone would mislead, since groups differ in size. If asked to predict individual leavers, I would then move to logistic regression (a method that predicts a yes/no outcome such as leave or stay)."

**Likely follow-ups:** 1) *What if it was just the tutorial's choice?* Say so honestly, then explain why it still fits. 2) *What would change your mind?* New data or a different question.
**Common mistakes / traps:** "It is the most popular"; no alternative; defending a choice you cannot explain.

### Q17 ⭐⭐⭐ 🟡 How do you explain your project to a non-technical stakeholder versus a technical interviewer, and how do you read which one you are talking to?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Communication range and audience awareness.
**Say this in the interview:** "I start with the outcome in plain words, then watch for cues and go deeper on method only if they ask."

**Answer structure:**
1. Start with the same plain headline for everyone.
2. Cues: terms they use (join, DAX, p-value) versus "so what should we do"; whether they ask "how" or "so what".
3. Non-technical: decision, number, risk, next step; no jargon; one picture.
4. Technical: data grain, cleaning rules, validation, method trade-offs.
5. When unsure, ask: "Shall I go into the method or stay on the outcome?"

**Illustrative project, replace with your real one:** To HR: "New joiners leave at about 3.5 times the rate of others; I suggest a 90-day check-in." To a technical panel: "Attrition rate on average headcount, 1,350 unique employees after de-duplication, tenure bands, compared by cohort."

**Likely follow-ups:** 1) *Can you do it in 30 seconds?* Yes; give it. 2) *What if both are present?* Headline first, then offer depth.
**Common mistakes / traps:** Jargon to a manager; oversimplifying to a technical panel; guessing the audience instead of asking.

### Q18 ⭐⭐⭐ 🟡 The interviewer interrupts and asks about a number in your project that you cannot remember exactly. How do you respond?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Honesty under pressure and ability to reason approximately.
**Say this in the interview:** "I do not remember the exact figure; it was roughly X, and I can confirm it from my file."

**Answer structure:**
1. Say you do not recall exactly; never invent one.
2. Give the approximate range you are confident about, labelled approximate.
3. Show you know how it was computed, so the number can be reconstructed.
4. Offer to confirm later (follow up in writing).

**Illustrative project, replace with your real one:** "I do not recall the exact first-year exit count; it was around 60, about two-fifths of all exits, and I would check the exact 63 in my notes. Computed as exits in the first 12 months of tenure divided by all exits."
(63 and 162 are the invented project figures; use your real ones.)

**Likely follow-ups:** 1) *Is it above or below 40%?* Reason from what you do know. 2) *How would you check?* Open the file or rerun the query.
**Common mistakes / traps:** Making up a precise number; freezing; being vague about the method too.

### Q19 ⭐⭐⭐ 🟡 Your project's result was surprising or contradicted the expectation of the business. How did you check it and how did you present it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Healthy scepticism plus courage to report an unwelcome result.
**Say this in the interview:** "First I tried to prove myself wrong with data checks; when it held, I presented it with evidence and caveats."

**Answer structure:**
1. State expectation versus result.
2. Checks: data errors, definition, filters, small groups, a different period.
3. Present: lead with the evidence, show the checks, state the confidence, avoid blame.
4. Agree the next step with the owner.

**Illustrative project, replace with your real one:** "Management believed pay was the main exit driver. The data showed 39% of exits in year one, mostly in a tenure band where pay was identical. I re-checked the definition, excluded transfers, and re-ran for a second half-year; the pattern held. I showed the checks first, then the result, and proposed an onboarding pilot instead of a pay review."

**Likely follow-ups:** 1) *What if they disagreed?* Offer a joint review of the data. 2) *Did you soften it?* No; I added the caveat that it is correlation.
**Common mistakes / traps:** Hiding the surprise; presenting it as certain; skipping data checks.

### Q20 ⭐⭐⭐ 🟡 Describe a stakeholder disagreement or changing requirement in your project, and how you handled it.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Professionalism and process under changing needs.
**Say this in the interview:** "I listened for the underlying need, wrote the change down, and agreed scope and date."

**Answer structure (STAR):** What the requirement was; what changed or conflicted; what you did (clarify the decision behind it, estimate the effect, agree a priority, confirm in writing); the result.

**Illustrative project, replace with your real one:** "Midway, HR asked to add contract staff to the attrition rate; I had excluded them. Instead of arguing, I showed both versions (with and without), explained the effect on the rate, agreed to report both with clear labels, and documented the definition. It cost one extra day, which I flagged."

**Likely follow-ups:** 1) *What if it was impossible by the deadline?* Offer a phased delivery. 2) *Who decided?* The metric owner (HR head).
**Common mistakes / traps:** Saying yes to everything; saying "the stakeholder was difficult"; no written agreement.

### Q21 ⭐⭐⭐ 🟡 What assumptions did you make in the project, which one was the riskiest, and how did you test or disclose it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of what the result depends on.
**Say this in the interview:** "I will list my assumptions, pick the riskiest and say how I tested or disclosed it."

**Answer structure:**
1. 3-4 assumptions (definition, data completeness, representativeness, stable behaviour over time).
2. The riskiest: the one that would most change the result.
3. Test: rerun without it, compare, or check against another source.
4. Disclose: put it on the report page, not in an appendix nobody reads.

**Illustrative project, replace with your real one:** Assumption: a blank exit date means the person is still employed. Riskiest, since a blank could also be missing data. Test: I checked 30 blanks against payroll status; 3 had actually left. Disclosure: I added a note, "blank exit date treated as active; about 10% of the sampled blanks were wrong", and I asked HR to correct the source.
(30 and 3 are invented illustrative figures; 3/30 = 10%.)

**Likely follow-ups:** 1) *How much would the result change?* Rerun both ways and show the range. 2) *Who owns the fix?* The data owner, with a date.
**Common mistakes / traps:** "I made no assumptions"; hiding assumptions in code; only listing trivial ones.

### Q22 ⭐⭐⭐ 🟡 Walk me through an HR-analytics project (attrition analysis, hiring funnel or attendance dashboard): the question, the data fields, the output and the decision it supported.
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** That you can tell one complete HR story: question, data, output, decision, in about two minutes.
**Say this in the interview:** "I will give it in four parts: the question HR asked, the fields I used, what I built, and what they decided. The numbers are from my project."
**Answer structure:**
1. **Question:** one sentence, phrased as a decision ("where should we focus retention effort this year?").
2. **Data fields:** employee ID, department, location, grade, date of joining, exit date, exit type, manager ID, last promotion date.
3. **Output:** the artefact (dashboard, one-page summary) and 2-3 headline findings.
4. **Decision:** what HR did or would do because of it.
**Illustrative project, replace with your real one:** "HR wanted to know why people were leaving in their first year. I took an HRIS export (the HR system's employee records) of 2,400 unique employees including past leavers, cleaned it, and built a Power BI page with attrition by department, tenure band and exit type. Over 12 months, 210 people left on an average headcount of 1,500, so attrition was 14.0% (210/1500); 168 were voluntary (11.2%). Of the 210 leavers, 84 (40%) had under one year of service. HR decided to pilot a 90-day check-in for new joiners in the two worst departments."
**Do not claim unless true:** the decision actually happened (say "recommended" if it did not), numbers you cannot reproduce, work done by others.
**Likely follow-ups:** 1) *Who used it?* Name the real audience. 2) *What would you add?* Exit-reason text, with privacy care. 3) *Did attrition fall afterwards?* Only say so if you measured it.
**Common mistakes / traps:** Starting with tools instead of the question; no decision at the end; presenting 14.0% without saying how it was calculated.

### Q23 ⭐⭐⭐ 🟡 In your attrition analysis project, how did you define "attrition" (voluntary only or all exits, which date, which employee groups), and why did that definition matter?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Whether you know "attrition" is a definition choice, not a given, and can show the effect of the choice on the number.
**Say this in the interview:** "I wrote the definition down with HR before calculating: who counts as a leaver, which date, and what the denominator is. Different choices gave 13.8% to 14.8% on the same data, so it had to be agreed."
**Answer structure:** (1) which exits count; (2) which date decides the period; (3) which employees are in or out; (4) denominator; (5) why it matters.
**Illustrative project, replace with your real one:** the export had 222 exit rows. I removed 8 internal transfers (not exits) and 4 contract-end or intern completions, leaving 210 exits in the 12 months by last working day (not resignation date). Average headcount was 1,500 (opening 1,520, closing 1,480). Results (rounded to 2 decimals): all exits 210/1500 = 14.00%; voluntary only 168/1500 = 11.20%; using closing headcount 210/1480 = 14.19%; using opening 210/1520 = 13.82%; if transfers and contract ends had stayed in, 222/1500 = 14.80%.
**Why it matters:** HR can act on voluntary exits (pay, manager, growth); layoffs and contract ends are planned. Mixing them hides the signal and makes year-on-year comparison unfair.
**Do not claim unless true:** that HR signed off the definition; that contract staff were excluded if you never checked.
**Likely follow-ups:** 1) *Why average headcount?* Headcount moves through the year, so average is fairer. 2) *Regretted attrition?* (exits of people the company wanted to keep) Needs a performance flag; mention only if you used one.
**Common mistakes / traps:** Counting resignation date instead of last working day; dividing by closing headcount without saying so; no written definition.

### Q24 ⭐⭐⭐ 🟡 Your HR project used an HRIS export with missing exit dates, duplicate employee IDs and inconsistent department names. How did you clean it, and what did you record about the cleaning?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** A disciplined cleaning routine and an audit trail, not silent edits.
**Say this in the interview:** "I never edited the raw file. I fixed each issue in a copy, one rule at a time, and logged the rule and how many rows it touched."
**Answer structure:** keep raw untouched; one issue, one rule, one count; decide with the data owner where judgement is needed; keep a cleaning log.
**What I did, in order (illustrative, replace with your real one):**
1. **Duplicate IDs:** separate exact duplicates (drop) from transferred employees with two rows (keep the latest by effective date for current-state, keep both in a history table).
2. **Missing exit dates:** 35 rows were marked "Terminated" with a blank exit date. For 28 I took the last payroll date as the proxy; 7 stayed unresolved and were reported as "date unknown", not guessed.
3. **Department names:** a mapping table turned spelling variants ("HR", "Human Resources", "H.R.") into one canonical name; the count of distinct names fell from 14 to 8 (illustrative).
4. Re-check: unique IDs, headcount against the HR figure.
**What I recorded:** a log with issue, rule, rows affected, owner who approved, and the date; plus the mapping table saved as its own file.
**Do not claim unless true:** specific counts, or that the owner approved a rule.
**Likely follow-ups:** 1) *Why not delete the 7?* Deleting leavers would understate attrition. 2) *Why latest record?* It shows where the person works now.
**Common mistakes / traps:** Overwriting raw data; dropping rows with a blank without asking what the blank means; no log.

### Q25 ⭐⭐⭐ 🟡 Project data: the raw HR export has 2,650 rows, of which 120 are exact duplicate rows; of the remaining rows, 130 are second records of employees who transferred department (each such employee has exactly two rows). How many unique employees are there, and which record would you keep for each transferred employee?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Row versus entity thinking, clean arithmetic, and a defensible keep rule.
**Say this in the interview:** "2,400 unique employees. I remove the 120 exact duplicates, then the 130 extra transfer rows, and for each transferred employee I keep the latest record for a current-state view."
**What the data shows:** two different kinds of repeats, and each needs its own treatment.
**Working:**
1. Start: 2,650 rows.
2. Drop exact duplicates: 2,650 - 120 = 2,530 rows.
3. Each transferred employee has exactly two rows, so each contributes one extra row: 130 extras. 2,530 - 130 = 2,400.
4. Check: 2,400 rows after keeping one per employee equals 2,400 unique IDs (confirm with a distinct count on employee ID).
**Result:** 2,400 unique employees. A raw row count would overstate headcount by 250 rows, about 10.4% of 2,400 (rounded).
**Which record to keep:** for headcount and current department, the latest record (by effective or transfer date). For attrition by department, ask which department the person was in at exit; for time-in-department, keep both rows in a separate history table.
**Caveats:** confirm "exact duplicate" means all columns match; check that no transferred employee has a missing effective date.
**Likely follow-ups:** 1) *What if one ID has three rows?* The premise says exactly two; I would test it with a count per ID. 2) *Why not keep the first record?* It is the old department.
**Common mistakes / traps:** Subtracting only 120; keeping the first row; deleting duplicates before looking at why they exist.

### Q26 ⭐⭐⭐ 🔴 A reviewer challenges your project: "Correlation is not causation; how do you know your recommendation will work?" How do you respond using only what your project data supports?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Intellectual honesty: do you agree, and do you know what your data can and cannot support?
**Say this in the interview:** "Fair challenge: I cannot prove it will work. My data shows an association, so I recommend a small pilot with a comparison group, not a company-wide rollout."
**Answer structure:** agree; state what the data does show; name possible other explanations; propose how to test; state what you would not claim.
**Illustrative project, replace with your real one:** among 1,500 employees, those with no promotion in three years had 66 leavers out of 300 (22.0%), against 108 out of 1,200 (9.0%) for others. That is a gap of 13 percentage points. But those without promotion may also be in lower grades, have weaker managers, or be near retirement. So I would not say "promotions will cut attrition by 13 points". I would compare within the same grade and tenure band, then pilot a promotion-review process in one unit, with a similar unit as comparison, for two quarters.
**Using only my data:** I can say the pattern exists and where it is strongest; I cannot say the cause or the size of the effect.
**Do not claim unless true:** a significance test or model you did not run; any pilot result.
**Likely follow-ups:** 1) *Could a model prove causality?* A model on this data still shows association; a pilot or randomised trial gets closer. 2) *What if a pilot is not possible?* Say the recommendation is a hypothesis and track the metric.
**Common mistakes / traps:** Getting defensive; quoting "p-value" as proof of cause; no way to test.

### Q27 ⭐⭐⭐ 🔴 The interviewer asks you to find the weakest point in your own project. Which would you pick and why is naming it a strength?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Self-awareness and judgement: can you rank your own risks without hiding them?
**Say this in the interview:** "The weakest point is the exit-reason field: it was free text and 18% blank, so my voluntary split is fragile. I flagged it in the report and I know what extra data would fix it."
**Answer structure:** pick one real weakness that matters to the conclusion; say its likely effect; say what you did to limit it; say what you would do next.
**Illustrative project, replace with your real one:** exit reasons came from a free-text field that managers filled in, and 18% were blank (illustrative). My voluntary versus involuntary split relied on it. I disclosed the 18%, showed the result with and without them, and recommended HR cross-check against resignation letters.
**Why naming it is a strength:** it shows you know where your conclusion is fragile, so a decision-maker can rely on you; hiding it only means someone else finds it later, usually at a worse moment. Choose a real weakness, not a fake one ("I work too hard") and not a fatal one you did nothing about.
**Do not claim unless true:** that you fixed it, if you only disclosed it.
**Likely follow-ups:** 1) *Did it change your result?* Give the with/without numbers. 2) *What else is weak?* Have a second one ready, smaller.
**Common mistakes / traps:** Saying "nothing"; naming a trivial weakness; naming a big one with no mitigation.

### Q28 ⭐⭐⭐ 🔴 Your project conclusion changes if one outlier group is removed. How do you decide what to report?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** That you do not cherry-pick: you disclose sensitivity and justify any exclusion on business grounds.
**Say this in the interview:** "I report both numbers, say which one I recommend and why, and I never drop a group just because it spoils the story."
**Answer structure:** (1) understand why the group is different; (2) decide if it belongs in the population for this question; (3) show the result with and without; (4) state the recommendation and the reason.
**Illustrative project, replace with your real one:** a branch of 60 staff closed, with 45 exits. All employees: 210/1500 = 14.0%. Without the branch: 165/1440 = 11.5% (11.46%). If HR's target is 12%, the conclusion flips. The closure exits are involuntary and one-off, so for a retention conversation the 11.5% is the better guide; for total workforce reduction, the 14.0% is the truth.
**Decision rule:** exclude only with a reason that exists before seeing the result (closure, data error, different population); otherwise keep it. Always show both.
**Do not claim unless true:** that the group was formally out of scope.
**Likely follow-ups:** 1) *What if no reason to exclude?* Keep it and report the sensitivity. 2) *Is it an outlier or an error?* Check the source records first.
**Common mistakes / traps:** Quietly removing the group; reporting only the nicer number; treating a real event as noise.

### Q29 ⭐⭐ 🟢 What did you learn from the project, technically and about working with business users?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Reflection, honesty and growth, with at least one real technical and one real business lesson.
**Say this in the interview:** "Technically I learned that cleaning and definitions take more time than charts; with business users I learned to agree the question and definitions before building."
**Answer structure:** two technical lessons, two stakeholder lessons, each tied to one moment in the project.
**Illustrative project, replace with your real one:** (technical) a join on employee ID duplicated rows and inflated headcount until I checked distinct counts; I now check row counts before and after every join. (Business) HR first asked for "attrition by department"; after one 15-minute conversation it became "first-year attrition by department and manager", which was the real question. I now ask "what will you decide with this?" first.
**Do not claim unless true:** lessons from tools you did not use; "everything went smoothly".
**Likely follow-ups:** 1) *How did you apply it later?* Give one concrete case. 2) *What would you learn next?* Name a specific skill, such as SQL window functions.
**Common mistakes / traps:** Generic lines like "I learned teamwork"; claiming no mistakes; no example.

### Q30 ⭐⭐ 🟢 How long did the project take, how did you plan it, and what did you do when a step took longer than expected?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Planning, realism, and how you handle a slipped step.
**Say this in the interview:** "It took four weeks against a three-week plan. Data cleaning ran long, so I cut scope on the extras, not on the checks, and told the stakeholder early."
**Answer structure:** total time; the plan in phases with rough shares; what slipped and why; what you did; what you would plan differently.
**Illustrative project, replace with your real one:** planned 3 weeks: week 1 question and data access, week 2 cleaning and analysis, week 3 dashboard and handover. Actual 4 weeks because the department names needed a mapping table and HR had to confirm exit types. I told HR on day 8 that the dashboard would be a week late, moved the "manager view" to phase two, and kept the validation step. Next time I would put about 40% of the time on data preparation from the start.
**Do not claim unless true:** the dates and the shares; a formal tool (Gantt, Jira) you did not use.
**Likely follow-ups:** 1) *What did you drop?* Say what and why it was the least important. 2) *Did the stakeholder mind?* Early notice helps.
**Common mistakes / traps:** Silent delay; cutting validation to save time; no numbers for time.

### Q31 ⭐⭐ 🟢 What were the key columns or metrics you created in the project, and how did you define each one?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** That you can define metrics precisely enough for someone else to reproduce them.
**Say this in the interview:** "For each column I can give the name, the formula, and the edge case. Here are the main ones."
**Answer structure:** name, plain-words definition, formula, one edge case.
**Illustrative project, replace with your real one:**
- **tenure_months:** months from date of joining to exit date, or to the report date if still employed. Edge: rehires use the latest joining date.
- **exited_flag:** 1 if the exit date falls in the period, else 0.
- **voluntary_flag:** 1 if exit type is resignation or retirement by choice; layoffs and contract ends are 0.
- **tenure_band:** under 1 year, 1-3, 3-5, 5+ years.
- **attrition_rate:** leavers in the period divided by average headcount, shown as a percentage (for example, 210/1500 = 14.0%).
**Do not claim unless true:** columns made in a tool you did not use; formulas you cannot explain.
**Likely follow-ups:** 1) *Why bands?* Easier to read than raw months. 2) *Edge cases?* Rehires, transfers, blank dates.
**Common mistakes / traps:** No denominator; metrics defined differently in different charts; vague words like "recent".

### Q32 ⭐⭐ 🟢 How did you choose the visuals in the project's report or dashboard, and which one would you remove if you had to cut one?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** That visuals were chosen to answer a question, and that you can prioritise.
**Say this in the interview:** "Each visual answered one question. The one I would remove is the one nobody used to make a decision."
**Answer structure:** question to visual match; audience; the cut and why.
**Illustrative project, replace with your real one:** KPI cards for the headline (attrition 14.0%, voluntary 11.2%); a bar chart of attrition by department (comparing categories); a line chart of monthly exits (trend); a stacked bar by tenure band (where in the career people leave); a table of top five departments for detail. I would remove the pie chart of exit reasons: nine slices were hard to compare, and a sorted bar says the same thing better.
**Do not claim unless true:** that users asked for or rejected a visual; a usability test you did not run.
**Likely follow-ups:** 1) *Why not a pie?* Humans compare lengths better than angles. 2) *Colour use?* One highlight colour for the point to act on.
**Common mistakes / traps:** Too many charts; 3D effects; choosing a visual because it looks good, not because it fits the question.

### Q33 ⭐⭐ 🟢 Which part of the project would you not trust yet, and what extra data would make you trust it?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Calibrated confidence: you know what is solid and what is not.
**Say this in the interview:** "I trust the headcount and department numbers; I would not yet trust the exit-reason split, because it came from free text. With payroll dates or resignation letters I would."
**Answer structure:** name the least reliable part; why; the extra data that would test it; how the conclusion would change.
**Illustrative project, replace with your real one:** exit reasons were free text, 18% blank. The "pay" reason looked large (31% of known reasons), but employees often say "better opportunity" instead of the real reason. Extra data to trust it: structured exit-interview codes, a second year of data, and survey scores from before the exit.
**Do not claim unless true:** the figures; any follow-up data you did not get.
**Likely follow-ups:** 1) *Would you still present it?* Yes, labelled "indicative". 2) *What decision depends on it?* Say which one, and keep it small until confirmed.
**Common mistakes / traps:** Saying "I trust everything"; saying nothing is reliable; no plan to improve it.

### Q34 ⭐⭐ 🟢 How did you document the project so that someone else could reproduce your numbers?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Reproducibility: can a colleague get the same numbers without calling you?
**Say this in the interview:** "I left a README, a data dictionary, a cleaning log, and the queries and file versions, so another analyst could rebuild every number."
**Answer structure:** what was documented, where it lives, how a newcomer would use it.
**Illustrative project, replace with your real one:** (1) README: question, data source, extraction date, file names. (2) Data dictionary: each column and metric definition. (3) Cleaning log: issue, rule, rows affected. (4) Saved SQL or Excel steps, in order, with comments. (5) A reconciliation note: for example, headcount 1,500 matches the HR report. (6) Version number and date on the dashboard.
**Test I used:** I asked a colleague to rebuild one number from the notes; where they got stuck, I fixed the notes (say this only if true).
**Do not claim unless true:** tools such as Git or a wiki you did not use.
**Likely follow-ups:** 1) *Where do you store it?* A shared folder with access control, because the data is sensitive. 2) *Who owns it after you?* Name the owner.
**Common mistakes / traps:** "It is in my head"; undated files named final_v3; no source date.

### Q35 ⭐⭐ 🟡 For an HR project, which people metrics did you track (attrition, time to hire, offer acceptance, absenteeism) and how did you pick them with HR?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** That metrics were tied to HR decisions, not picked because they are easy to calculate.
**Say this in the interview:** "I started from the decisions HR makes, then chose the few metrics that inform each, and agreed the definitions with them."
**Answer structure:** decision, metric, definition, owner.
**Illustrative project, replace with your real one:**
- **Attrition rate** (leavers / average headcount): retention planning.
- **First-year attrition** (leavers with under one year of service / joiners): onboarding quality.
- **Time to hire** (offer-accepted date minus requisition-open date, in days; companies define this differently, so agree the start and end dates): recruiting speed.
- **Offer acceptance rate** (joined / offers made; for example 24/30 = 80%): offer competitiveness.
- **Absenteeism rate** (days absent / scheduled working days): workload and wellbeing signal.
I picked them in a 30-minute session with the HR head, who ranked them; two were dropped as unused.
**Do not claim unless true:** that HR ranked them; metrics you never calculated.
**Likely follow-ups:** 1) *Why not more?* Too many KPIs dilute focus. 2) *Any benchmark?* Compare to your own history; external benchmarks are unverified and differ by industry.
**Common mistakes / traps:** Listing metrics with no definition; no link to a decision; mixing counts and rates.

### Q36 ⭐⭐ 🟡 Your HR project handled sensitive employee data. What privacy and confidentiality steps did you follow, and what did you leave out of the final report?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** That you treat employee data as sensitive and can describe concrete controls.
**Say this in the interview:** "I used only the fields I needed, removed direct identifiers, limited access, and left out anything that could point to one person."
**Answer structure:** minimise; de-identify; protect access; suppress small groups; follow policy.
**Illustrative project, replace with your real one:** (1) took only the columns needed; no salary, medical or Aadhaar-type IDs. (2) replaced employee names with a coded ID in my working file. (3) stored files in the approved folder, not on a personal laptop or email. (4) hid any group with fewer than five people (for example, a team of three) in the report. (5) left out free-text exit comments and individual risk scores. (6) deleted working copies at the end as the owner agreed.
**Legal note:** for India's DPDP Act and company policy, I would confirm requirements with the legal and IT teams (from memory, unverified).
**Do not claim unless true:** specific controls you did not use; a formal approval.
**Likely follow-ups:** 1) *Why five?* A commonly used minimum group size so individuals cannot be guessed (from memory, unverified; the threshold is a policy choice). 2) *Who approved access?* Name the data owner.
**Common mistakes / traps:** Emailing raw exports; showing small teams; treating a coded ID as fully anonymous.

### Q37 ⭐⭐ 🟡 Project exercise: in your attrition project, the sales team had 18 leavers on an average headcount of 120, and engineering had 30 leavers on an average of 400, for the year. Which team has the higher attrition rate, and how would you say it to HR in one line?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Rates versus counts, and a clear sentence for a non-technical audience.
**Say this in the interview:** "Engineering has more leavers, but sales has the higher rate: 15.0% against 7.5%, double."
**What the data shows:** engineering lost 30 people, sales 18, yet engineering is more than three times bigger.
**Working:**
1. Sales: 18 / 120 = 0.15 = 15.0%.
2. Engineering: 30 / 400 = 0.075 = 7.5%.
3. Ratio: 15.0 / 7.5 = 2.0; the gap is 7.5 percentage points.
**Result:** sales 15.0%, engineering 7.5% (annual, on average headcount).
**One line for HR:** "Sales loses 15 in every 100 people a year, engineering 7.5; sales is where retention effort will matter most."
**Caveats:** one year only; sales has 18 leavers, so a few exits move the rate; compare with last year and voluntary versus involuntary before acting.
**Likely follow-ups:** 1) *Is the gap significant?* With small counts, check more periods. 2) *Why average headcount?* Headcount changes during the year.
**Common mistakes / traps:** Saying engineering is worse because 30 is bigger than 18; mixing percent and percentage points.

### Q38 ⭐⭐ 🟡 Exercise: your hiring funnel project showed 1,000 applications, 250 screened in, 100 interviewed, 30 offers and 24 joined. What are the stage-to-stage conversions and the overall application-to-joining rate, and where would you look first?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Funnel arithmetic and judgement about where to look.
**Say this in the interview:** "Overall 2.4% of applicants join. The biggest loss in volume is at screening, 750 of 1,000, so I would look there first, then at the 6 offers that did not join."
**What the data shows:** each stage keeps a share of the previous one.
**Working:**
1. Application to screened: 250/1000 = 25.0%.
2. Screened to interviewed: 100/250 = 40.0%.
3. Interviewed to offer: 30/100 = 30.0%.
4. Offer to joined: 24/30 = 80.0%.
5. Overall: 24/1000 = 2.4%; check by multiplying 0.25 x 0.40 x 0.30 x 0.80 = 0.024.
**Result:** 25%, 40%, 30%, 80%; overall 2.4% (24 of 1,000).
**Where I would look first:** (a) screening: 750 rejected; is the job description attracting unsuitable applicants, or the filter too strict? (b) offer to joining: 6 offers lost; reasons for declines (pay, notice period, counter-offer). (c) quality: compare the source channel for those who joined. A low rate is not bad by itself; it depends on role and volume.
**Caveats:** funnel stage definitions, time lags (offers made this month join next month), and small numbers at the lower stages.
**Likely follow-ups:** 1) *Which stage to fix?* Where a small improvement gives most joiners per effort. 2) *Segment?* By role and source.
**Common mistakes / traps:** Dividing every stage by 1,000; saying 25% is "bad" without a benchmark; ignoring time lags.

### Q39 ⭐⭐ 🟡 Exercise: in your project, a model flagged 200 employees as likely leavers; 60 actually left, and 90 employees in total left in the period. What are precision and recall, and how would you explain them to an HR head?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Precision and recall from counts, and a plain explanation of the trade-off.
**Say this in the interview:** "Precision is 30%: of 200 flagged, 60 left. Recall is 66.7%: of 90 who left, we caught 60."
**What the data shows:** the model caught most leavers but raised many false alarms.
**Working:**
1. True positives (flagged and left) = 60.
2. Flagged but stayed = 200 - 60 = 140.
3. Left but not flagged = 90 - 60 = 30.
4. Precision = 60/200 = 30.0%.
5. Recall = 60/90 = 66.7% (66.67%).
**Result:** precision 30.0%, recall 66.7%.
**For an HR head:** "If we talk to the 200 people flagged, 60 are really at risk, and we reach two thirds of everyone who would leave. We miss 30." Accuracy cannot be computed here because total headcount is not given.
**Caveats:** compare with a baseline (what if we picked 200 at random? precision would equal the overall leaver rate); the cost of 140 conversations versus 30 missed exits; fairness and privacy of the flags.
**Likely follow-ups:** 1) *Raise precision?* Flag fewer, higher-risk people; recall drops. 2) *Which matters?* Depends on the cost of a missed leaver versus a wasted conversation.
**Common mistakes / traps:** Swapping the denominators; quoting accuracy; treating a flag as a certainty about a person.

### Q40 ⭐⭐ 🟡 How did you handle class imbalance or a small sample in a project, for example an HR dataset where only 12% of employees had left?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** That you know accuracy misleads on imbalanced data and can name practical remedies.
**Say this in the interview:** "A model that says nobody leaves is 88% accurate and useless. So I used precision and recall, stratified splits, and kept the model simple."
**Answer structure:** show the trap; pick the right metrics; split carefully; handle imbalance; be honest about small samples.
**Illustrative project, replace with your real one:** 1,000 employees, 120 leavers (12.0%). Always predicting "stays" gives 880/1000 = 88% accuracy with recall 0. So: (1) metrics: precision, recall and a confusion table, not accuracy. (2) stratified split (the leaver share is kept the same in the training and test parts) so a 200-row test set still contains about 24 leavers (12% of 200). (3) class weights or a simple threshold change, compared with a plain baseline. (4) repeated cross-validation for stability, because 24 leavers is a small test set. (5) in the report: say the result is indicative and give ranges.
**Do not claim unless true:** SMOTE, XGBoost or other methods you did not use; results beyond what you ran.
**Likely follow-ups:** 1) *Why not oversample?* It can leak duplicates into the test set if done before splitting. 2) *Enough data?* With a few dozen leavers, prefer simple, explainable analysis.
**Common mistakes / traps:** Reporting accuracy; oversampling before splitting; confident claims from a tiny test set.

### Q41 ⭐⭐ 🟡 How did you decide the project was finished, and how did you hand it over to its users?
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** That you define "done" by the stakeholder's need and hand over properly.
**Say this in the interview:** "It was finished when the stakeholder could answer their question from it without me, and the numbers were reconciled and documented."
**Answer structure:** done criteria agreed at the start; sign-off; handover steps; follow-up.
**Illustrative project, replace with your real one:** criteria: (1) the dashboard answers "where is first-year attrition highest?" (2) headcount reconciles to the HR report; (3) definitions documented; (4) HR head tested and signed off. Handover: 30-minute walkthrough, a one-page user guide, named owner for the monthly refresh, a contact for questions for two weeks, and a check-in after one month.
**Do not claim unless true:** a formal sign-off, training or adoption figures you do not have.
**Likely follow-ups:** 1) *What if they kept asking for changes?* Log extras as phase two. 2) *How did you know they used it?* Usage stats or a quick check, if available.
**Common mistakes / traps:** Finishing when the charts look good; no owner for refresh; no documentation.

### Q42 ⭐⭐ 🟡 Project data had 15% missing values in a key column. Describe the options you weighed and what you reported to the stakeholder.
**Asked at:** commonly asked (no company-specific report found); project walk-throughs show up in about 14 candidate profiles in the internal research, and prep-site prompts for HR attrition projects exist (unverified).
**What the interviewer is checking:** Whether you consider options, measure the effect, and tell the stakeholder plainly.
**Say this in the interview:** "First I find out why it is missing, because that decides the fix. Then I compare options and report how much the answer depends on the choice."
**Clarify first:** is it missing at random (a system gap) or for a reason (managers skip low ratings)?
**Options I weighed (illustrative, 2,000 rows, performance rating blank in 300, which is 15%):**
1. **Drop those rows:** 1,700 rows remain; simple, but biased if the missing rows differ.
2. **Fill with the typical value (median or most common):** keeps rows but can hide real differences.
3. **Treat "missing" as its own category:** honest and often informative in HR data.
4. **Go back to source:** ask HR to supply the ratings, best when feasible.
5. **Model-based filling:** possible, but hard to explain; only if needed.
**What I reported:** the 15%, the reason if known, results under two or three options, and which I used: "missing" as its own group, with the main conclusion unchanged under all options (say this only if true).
**Do not claim unless true:** the reasons for missingness; a test of randomness you did not run.
**Likely follow-ups:** 1) *When is dropping fine?* Small shares and random gaps. 2) *Is 15% too much?* There is no universal threshold; it depends on the column and the question.
**Common mistakes / traps:** Silently filling with zero; dropping without checking who is missing; not telling the stakeholder.

### Q43 ⭐⭐ 🟡 You built a dashboard in your project but the users did not use it. What would you investigate and how would you find out why?
**Asked at:** commonly asked (no company-specific report found); dashboard-project explanation appears in prep guides (unverified).
**What the interviewer is checking:** Whether you treat "nobody uses it" as a problem to diagnose, not blame on users.
**Say this in the interview:** "First I would check whether people are really not using it, using the usage log, then ask a few of them why. Usually it is about trust, fit with their routine, or the wrong questions."
**First, clarify / contain:** Who were the intended users, what decision was it meant to support, and what does "not used" mean (never opened, opened once, or opened but ignored)? I do not rebuild anything yet.
**What I would check, in order:**
1. Usage data: views per user per week, from the tool's usage report (Power BI has one; confirm what your tool offers).
2. Reach: how many intended users even have access or know it exists.
3. Fit: does it answer a question they ask weekly, or one I assumed they ask?
4. Trust: do its numbers match the report they already use?
5. Friction: slow load, too many filters, no mobile view, refresh older than the meeting.
6. Replacement: are they still using an Excel sheet that does the job?
**If I find...:** low reach means a short demo and a link in their weekly mail; numbers disagree means reconcile and publish a definitions page; wrong questions means redesign with them; no real need means retire it honestly.
**What I would tell the stakeholder:** "I looked at usage and spoke to five users. The main reasons are X and Y. I propose a one-page fix by next Friday and a check of usage a month later."
**Illustrative project, replace with your real one:** "In my attrition dashboard, 6 of 40 intended managers opened it in 30 days (15%). Interviews showed the headcount figure differed from their Excel list. After reconciling and adding a definitions tab, 22 of 40 opened it the next month (illustrative numbers)."
**Prevent it next time:** Involve two real users before building; agree the questions and the owner; track usage from week one.
**Likely follow-ups:** 1) *Why ask users instead of guessing?* Usage data says what, only users say why. 2) *What if only HR uses it?* Then the audience was wrong; say so.
**Common mistakes / traps:** Blaming users; adding more charts; claiming adoption you did not measure.

### Q44 ⭐⭐ 🟡 How would you scale your project to ten times the data, or to a weekly automatic refresh? What would break first?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you think beyond a one-off file: refresh, volume, ownership.
**Say this in the interview:** "The first thing to break is usually manual steps and slow spreadsheets, not the maths. I would automate the load, move heavy work to a database, and add automatic checks."
**Structure of the answer:**
1. Name the manual steps (download, copy, paste, fix names by hand); each one fails on a weekly schedule.
2. Volume: Excel struggles with large files; move cleaning and joins to SQL or a database view, and let the dashboard read the clean table.
3. Refresh: scheduled refresh, with credentials owned by a shared service account (a login belonging to the process, not one person), not a person's laptop (confirm with IT).
4. Checks: row counts, duplicate keys and totals compared with last week; alert when they jump.
5. Documentation and an owner for the pipeline.
**Illustrative project, replace with your real one:** "My attrition file had about 12,000 rows from an HRIS export. At ten times (120,000 rows) the Excel lookups would crawl, so I would load the export into a database table, write the cleaning as a view (a saved query that always shows the cleaned table), and refresh weekly. I would also add a check that headcount does not move more than a set percentage without an explanation (illustrative)."
**Must not claim unless true:** that you actually built automation; if you only designed it, say "I would".
**Likely follow-ups:** 1) *What breaks first, honestly?* The manual cleaning and any column rename in the export. 2) *How would you know a refresh failed?* A row-count and date check that sends an alert.
**Common mistakes / traps:** Saying "cloud" without a reason; ignoring data privacy when moving data; no owner for the refresh.

### Q45 ⭐⭐ 🟡 You are asked: "What would the business do differently because of your analysis?" How do you convert a finding into a recommendation?
**Asked at:** commonly asked (no company-specific report found); impact-and-recommendation probes appear in prep guides (unverified).
**What the interviewer is checking:** Whether you can move from "what happened" to "what to do", with size and limits.
**Say this in the interview:** "I turn each finding into one action, one owner, one measure, and one date, and I say how confident I am."
**Structure of the answer:**
1. Finding in one sentence with the number.
2. So what: why it matters in money, time or risk.
3. Action: specific and small enough to start (not "improve engagement").
4. Owner and how success is measured, with a review date.
5. Confidence and what would change my mind.
**Illustrative project, replace with your real one:** "Finding: first-year leavers were 40 of 120 joiners (33.3%) in one unit. Action: HR and the unit head run a 30-day check-in for new joiners. Measure: first-year exits in the next two hiring batches. I would say this is a pilot, because my data shows association, not proof it works (illustrative numbers)."
**Must not claim unless true:** a business result that was never measured.
**Likely follow-ups:** 1) *What if the business disagrees?* Offer a small pilot with a measure. 2) *Cost?* Estimate roughly and flag it as rough.
**Common mistakes / traps:** Recommendations that restate the chart; no owner; promising a percentage improvement with no basis.

### Q46 ⭐⭐ 🟡 Your project used a public dataset such as the commonly shared HR attrition sample. How do you answer "how is this different from what everyone else did?"
**Asked at:** commonly asked (no company-specific report found); public HR attrition samples are widely used in portfolios (unverified).
**What the interviewer is checking:** Honesty about a common dataset, and what you added of your own.
**Say this in the interview:** "Many people used this dataset, so I do not claim the data is mine. What is mine is the question I chose, the choices I made, and how I checked and presented it."
**Structure of the answer:**
1. Admit it is public; never imply it is company data.
2. Name your own question (for example a specific decision, not "explore attrition").
3. Show your choices: attrition definition, how you handled imbalance, what you refused to conclude.
4. Add something: a data dictionary, a reconciliation, a dashboard with an action table, or a second dataset or a simulated process for practice.
5. State limits: it is a sample, probably synthetic, with no real business context (unverified; say "I treated it as exercise data").
**Illustrative project, replace with your real one:** "I used the public sample but framed one question: which tenure band should a retention pilot target? I defined attrition by tenure band, tested the finding on a split of the data, and wrote what the data cannot say."
**Must not claim unless true:** real-world impact, or that the data represents any company.
**Likely follow-ups:** 1) *Why use it at all?* It is safe and lets me show method. 2) *What would you do with real data?* Reconcile to payroll headcount first.
**Common mistakes / traps:** Defensive tone; hiding that it is public; the same charts as every tutorial.

### Q47 ⭐⭐ 🟡 How do you present a project when your team lead did most of the modelling and you did data preparation and reporting?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Honest ownership, and that you understand the part you did not build.
**Say this in the interview:** "My part was data preparation and reporting. I can explain the model in plain terms and what it needs from the data, and I will be clear on where my lead made the choices."
**Structure of the answer:**
1. Say your part first, with specifics: cleaning rules, checks, the report.
2. Explain the model in one plain line (what it predicts, from what).
3. Show how your work affected the model: for example, your cleaning changed what the model could learn.
4. Name what you would ask your lead about, which shows you know the boundary.
5. Do not claim the modelling.
**Illustrative project, replace with your real one:** "My lead built a leaver-prediction model. I built the cleaned table: fixed 130 duplicate transfer records, standardised 14 department spellings, and defined 'left' by last working day. I then built the report showing risk bands and actions. I can explain that the model scores each employee by tenure, pay position and similar fields; the choice of model was my lead's (illustrative)."
**Likely follow-ups:** 1) *Why this model?* Say what you were told, and what you would check. 2) *Would you want to do the modelling?* Yes, and say how you are learning it.
**Common mistakes / traps:** Saying "we" for everything; claiming the model; saying "I only did cleaning" as if it were minor.

### Q48 ⭐⭐ 🔴 You discover, a week after sharing, an error in a project figure that stakeholders already used. Walk through what you do and say.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Integrity, speed and calm when you find your own mistake.
**Say this in the interview:** "I tell the people who used it quickly, before they find it themselves: what was wrong, who is affected, the corrected figure, and when."
**First, clarify / contain:** Confirm the error with a second check; find the cause; list who used the figure and where. Do not quietly fix and hope nobody noticed.
**What I would check, in order:**
1. Reproduce the error and find the exact cause (wrong filter, wrong denominator, stale data).
2. Size it: which figures change, and by how much.
3. Find every place it was used (slides, emails, dashboards).
4. Recompute the corrected figure and have it checked by a second person.
5. Check whether any decision was made on it.
**If I find...:** small and no decision affected means a correction note; a decision was affected means tell the decision-maker directly and early; a systemic cause means fix the process.
**What I would tell the stakeholder:** "I found an error in the attrition figure I sent on Monday. I used 600 as average headcount instead of 750. Attrition was 90 leavers / 750 = 12.0%, not 15.0%. I have updated the dashboard and will confirm in writing today."
**Illustrative project, replace with your real one:** the numbers above (600 vs 750 headcount, 90 leavers) are exercise values, not your project.
**Prevent it next time:** Reconcile to a known total before sharing, peer review, and a version and change log.
**Likely follow-ups:** 1) *Would you hide it if small?* No; say it. 2) *What if your manager prefers silence?* Escalate politely; I would not let a wrong number stand.
**Common mistakes / traps:** Blaming data; silence; sending a fix with no explanation of what changed.

### Q49 ⭐⭐ 🔴 The interviewer says your project's metric is flawed because it ignores a segment. How do you respond and, if they are right, what do you do?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can take criticism, test it, and fix scope honestly.
**Say this in the interview:** "That may be right. Let me check how big the segment is and whether it changes the answer. If it does, I would restate the metric."
**First, clarify / contain:** Ask which segment and why it matters; do not argue yet.
**What I would check, in order:**
1. Size of the segment (share of headcount or revenue).
2. Was it excluded on purpose (definition) or by accident (a filter)?
3. Recompute the metric with and without it.
4. Does the conclusion change, or only the level?
**If I find...:** they are right and it matters means redefine the metric, rerun and disclose; right but small means keep, and state the exclusion; wrong means show the numbers politely.
**What I would tell the stakeholder:** "My attrition rate counted only permanent staff: 60 leavers / 500 = 12.0%. Including 100 contract workers (assuming no contract leavers were recorded) gives 60 / 600 = 10.0%, which is misleading, so I would need contract exit data. Until then I would label the metric 'permanent staff only'."
**Illustrative project, replace with your real one:** exercise numbers above.
**Prevent it next time:** Write the metric definition with inclusions and exclusions up front and get it signed off.
**Likely follow-ups:** 1) *Why is the 10% misleading?* Denominator grew without matching leavers. 2) *What if the segment has no data?* Say so.
**Common mistakes / traps:** Defending instead of testing; quietly changing the definition; ignoring the segment's data gaps.

### Q50 ⭐⭐ 🔴 A model in your project showed high accuracy; the interviewer suspects data leakage. What checks would you describe and what leakage could exist in HR data such as exit-interview scores?
**Asked at:** commonly asked (no company-specific report found); leak-free pipelines appear in attrition prompts (unverified).
**What the interviewer is checking:** That you know leakage (using information that would not exist at prediction time) and test for it.
**Say this in the interview:** "Very high accuracy makes me suspicious. I would check each feature for whether it is known before the person leaves, and compare against a simple baseline."
**Clarify first:** What is the prediction moment (for example, the start of each quarter), and what is the target?
**Plan:**
1. Baseline: if 88% of employees stay, a model that says "stays" for everyone is 88% accurate, so accuracy alone says little.
2. Look at the most important features; anything that looks too good is a suspect.
3. Timing check: was each feature captured before the exit?
4. Split by time (train on earlier periods, test on later), not randomly.
5. Remove the suspect feature and see how the score falls.
**HR leakage examples:** exit-interview scores (only exist after resignation); "notice period" or "final settlement" fields; "exit reason"; a status field already set to "inactive"; a rehire or clearance flag; tenure computed to the exit date for leavers but to today for stayers.
**Illustrative project, replace with your real one:** "My first model reached 97% accuracy. Exit-interview score was the top feature. It only exists after resignation, so I removed it, and accuracy fell to 90%, which was more believable (illustrative)."
**Deliverable:** Say which fields you removed and why.
**Likely follow-ups:** 1) *Why a time split?* It mimics predicting the future. 2) *Use precision and recall instead?* Yes, for imbalanced data.
**Common mistakes / traps:** Celebrating accuracy; random splits; not listing fields by when they are created.

### Q51 ⭐⭐ 🔴 In your project, would your recommendation hold at a different time or in a different business unit? How would you test its generalisability?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness that findings from one place and time may not transfer.
**Say this in the interview:** "I would not assume it holds. I would test it on a later period and on another unit, and say plainly what I could not test."
**Clarify first:** What exactly is the recommendation, and what conditions made the finding true (a hiring drive, a policy change, a manager)?
**Plan:**
1. Re-run the same analysis on a later period (a holdout) and compare the pattern, not just the level.
2. Repeat it on another unit or location with enough people to be meaningful.
3. Compare the context: size, job mix, pay structure, manager changes.
4. Check consistency: does the direction hold in each group, even if levels differ?
5. Pilot before rolling out.
**Method choice and why:** Simple side-by-side comparison first; formal models only if the data allows.
**Pitfalls:** Small groups (9 leavers out of 90 is 10%, but one exit changes it by about 1.1 percentage points); one-off events; survivorship.
**Deliverable:** "The finding held in Sales at 15% (18 of 120) but I have no data for Support, so I recommend a pilot there (illustrative)."
**Illustrative project, replace with your real one:** numbers above are exercise values.
**Likely follow-ups:** 1) *What if it fails elsewhere?* Report it; it narrows the finding. 2) *Is a pilot necessary?* It is the cheapest test.
**Common mistakes / traps:** Claiming general truth from one dataset; ignoring small numbers.

### Q52 ⭐ 🟢 Which project of yours would you not put on the resume, and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Judgement and self-awareness about what a resume should contain.
**Say this in the interview:** "I would leave off any project I cannot explain end to end, or that is a copy of a tutorial with nothing of mine."
**Structure of the answer:**
1. Criteria: could I explain the data, my cleaning, my method and my result for ten minutes?
2. Weak candidates for removal: a tutorial copy, a project where I cannot name my contribution, a very old one with lost files, one with claims I cannot verify.
3. Say what you would do instead: keep fewer, stronger projects.
4. If it must stay, describe it honestly as practice.
**Illustrative project, replace with your real one:** "I removed a sales dashboard I built by following a video, because all the choices were the instructor's. I kept my HR attendance analysis, where I defined the metrics myself (illustrative; use your own)."
**Must not claim unless true:** that a project was independent when it was guided.
**Likely follow-ups:** 1) *Is a tutorial project always bad?* No, if you extended it and say so. 2) *How many projects?* Two or three you can defend.
**Common mistakes / traps:** Padding the resume; saying "none, all are good"; being unable to explain a listed one.

### Q53 ⭐ 🟢 How did you use AI tools (for code, queries or summaries) in your project, and how did you verify their output?
**Asked at:** commonly asked (no company-specific report found); an AI-project anecdote exists in the internal interview-process notes but is not company-confirmed.
**What the interviewer is checking:** Honest, careful use of AI, and that you still own the correctness.
**Say this in the interview:** "I use AI to draft and explain, but I treat its output as unverified. I test every query and number myself."
**Structure of the answer:**
1. What I used it for: a first SQL draft, explaining an error, wording a summary.
2. What I did not do: paste in real employee data (privacy; check company policy).
3. Verification: run on a tiny sample where I know the answer; compare row counts and totals with a manual check; read every line and be able to explain it.
4. Where it was wrong, with an example.
5. Disclosure: say so when asked.
**Illustrative project, replace with your real one:** "AI suggested a join that duplicated some rows because the key was not unique. I caught it because the total headcount rose from 1,200 to 1,250 (exercise numbers), then fixed it by de-duplicating first (say this only if it really happened to you)."
**Likely follow-ups:** 1) *Would you use it at work?* Within company rules, on non-sensitive data. 2) *Can you write the query without it?* Be ready to, say so only if true.
**Common mistakes / traps:** Hiding the use; trusting output blindly; uploading confidential data.

### Q54 ⭐ 🟡 What is the difference between a project you did in a course and one you would do in a job, and how do you show job-ready thinking from a course project?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand real-job constraints, and can show them.
**Say this in the interview:** "A course project has a clean question and a given dataset. A job project starts with a vague request, messy data and people who must act. I try to practise that in my projects."
**Explain simply:**
- Course: defined question, ready data, marks for method. Job: unclear question, data you must find and fix, value measured by decisions.
- Job extras: stakeholders, deadlines, data access and privacy, documentation, handover, maintenance.
**How to show job-ready thinking:** open with the business question and user; show how you handled a data problem; give a recommendation with an owner and a measure; state limits; describe how you would hand it over.
**Illustrative project, replace with your real one:** "In my course attrition project I wrote a one-page brief first (user: HR head, decision: where to run a retention pilot), a data-check log, and a handover note, as I would at work."
**Practice step:** Rewrite your project summary starting with the decision, not the tool.
**Likely follow-ups:** 1) *What would change at work?* Access, privacy, review and time pressure. 2) *What would you do first in a job?* Meet the users.
**Common mistakes / traps:** Leading with tools; pretending a course project had business impact.

### Q55 ⭐ 🟡 If your project was in a different domain (retail, finance) from the company's, how do you transfer its lessons to HR or operations analytics?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can transfer method, not just repeat your domain.
**Say this in the interview:** "The business words change but the method is the same: define the metric, check the data, segment, compare, recommend. I can map my retail example to HR."
**Structure of the answer:**
1. Name the transferable skills: cleaning, defining metrics, funnels, cohort and segment analysis, dashboards.
2. Map concepts: customer churn to employee attrition; sales funnel to hiring funnel; repeat purchase to retention; stock-outs to vacancy gaps.
3. Name what is new and how you will learn it: HR definitions, privacy, small numbers.
4. Show you have started (read the company's published HR metrics, or practised on a sample).
**Illustrative project, replace with your real one:** "In my retail project I built a customer funnel: 1,000 visits, 250 add to cart, 100 checkout, 24 pay. The hiring funnel is the same shape: applications, screen, interview, offer, joined. I would check the same drop-off points (illustrative)."
**Must not claim unless true:** HR domain expertise you do not have; but if you come from HR, say you know the domain.
**Likely follow-ups:** 1) *What is different in HR data?* Privacy and small groups. 2) *Biggest risk of transfer?* Assuming the same definitions.
**Common mistakes / traps:** Saying domain does not matter; no concrete mapping.

### Q56 ⭐ 🟡 Which ethical risks arise when employee data is used to predict who will leave or to rank performance, and how would your project have handled them?
**Asked at:** commonly asked (no company-specific report found); ethics angle appears in HR attrition prompts (unverified).
**What the interviewer is checking:** Awareness that predicting people is sensitive, and care in how you act.
**Say this in the interview:** "The risks are fairness, privacy, misuse and wrong labels. I would use the output to improve support, not to punish people, and I would keep the group-level view."
**Structure of the answer:**
1. Privacy and consent: use the minimum data needed, restrict access, check company policy and local law with legal (I cannot state the details from memory).
2. Fairness: check the model for different error rates across groups such as gender or age; avoid using protected attributes or close proxies.
3. Misuse: a "high risk" label could reduce someone's opportunities; share with HR leaders in aggregate, not with line managers by name.
4. Accuracy: with an imbalanced outcome, many flags will be wrong, so a label is not a fact.
5. Transparency: explain what the model does; allow human judgement; document limits.
6. Performance ranking: be careful with metrics that reflect manager bias or role differences.
**Illustrative project, replace with your real one:** "I reported attrition by team and tenure band only, hid groups under 10 people, and left out names, salary and exit comments (illustrative)."
**Likely follow-ups:** 1) *Would you build it if asked?* Yes with guardrails, or explain the risks first. 2) *What if the model is biased?* Report it and do not deploy.
**Common mistakes / traps:** Saying there is no risk; giving only the technical view.

### Q57 ⭐ 🟡 How would you describe your project in a single-line resume bullet, and what makes a bullet verifiable in an interview?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether your bullet is clear, honest and backed by something you can explain.
**Say this in the interview:** "A good bullet has an action, the method, the data scale and a result or purpose. I include only things I can defend line by line."
**Structure of the answer:**
1. Pattern: verb + what + with what + result.
2. Verifiable means: you can name the dataset size, the definition, how the number was computed, and your own role.
3. If the result is practice or estimated, say so.
**Illustrative project, replace with your real one:** "Built an HR attrition dashboard (Excel and Power BI) on 2,500 employee records; cleaned 120 duplicate rows and standardised department names; showed first-year attrition of 33% (40 of 120 joiners) to guide a retention pilot." Check: 40 / 120 = 33.3%. Use your own numbers.
**Must not claim unless true:** percentages or "saved X hours" you did not measure.
**Likely follow-ups:** 1) *How was that 33% computed?* 40 leavers in first year over 120 joiners. 2) *Any improvement claimed?* Only if measured.
**Common mistakes / traps:** Vague verbs ("worked on"); tool lists; invented impact; numbers you cannot reproduce.

### Q58 ⭐ 🟡 Your project timeline slipped because data access was delayed. How do you explain this without blaming others?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Ownership and calm problem-solving under delay.
**Say this in the interview:** "I describe the delay as a fact, then focus on what I did: re-planned, used what I had, and kept people informed."
**Structure of the answer:**
1. Fact, neutral: "Access to the HR export took three weeks longer than planned."
2. What I controlled: I wrote the data request earlier, flagged the risk at the start, and prepared the analysis plan and a mock-up on sample data.
3. Communication: told the sponsor the new date and what could still be delivered.
4. Learning: next time ask for data access on day one, and list dependencies in the plan.
**Illustrative project, replace with your real one:** "Access arrived in week 3 instead of week 1. Meanwhile I wrote definitions and tested my queries on a 200-row sample, so when the full data came I finished in four days (illustrative)."
**Must not claim unless true:** a recovery that did not happen.
**Likely follow-ups:** 1) *Could you have prevented it?* Request access and confirm the owner earlier. 2) *Who did you tell?* The sponsor, with a revised date.
**Common mistakes / traps:** Naming and blaming a team; no learning; saying you worked extra hours as the fix.

### Q59 ⭐ 🟡 How do you answer when the interviewer asks about a project you did in a previous non-analytics role, such as HR operations, and how do you reframe it as analytics?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can reframe real work in analytics terms, honestly.
**Say this in the interview:** "In HR operations I already worked with data: I will describe a task as a question, data, method and result, with only true numbers."
**Structure of the answer:**
1. Pick a task where you used data: attendance tracking, payroll reconciliation, joiner and leaver reports.
2. Frame it: the question, the data source, what you did with it (checks, pivots, reconciliation), what changed.
3. Use analytics words honestly, such as data validation, reporting, process metric.
4. Be clear about the gap: what you did by hand and what you would now do with SQL or Power BI.
**Illustrative project, replace with your real one:** "I reconciled monthly attendance with payroll for about 800 staff. I found that 35 people had mismatched leave days; I traced them to late approvals and built a pivot to flag them each month. I now would automate it in SQL (illustrative numbers)."
**Likely follow-ups:** 1) *Was that analytics?* It was data work; and I now add method and tools. 2) *What did you measure?* Only what is true.
**Common mistakes / traps:** Inflating titles; vague "did reporting"; hiding a non-analytics background (it is an asset in HR analytics).

### Q60 ⭐ 🔴 Interviewer role-play: they challenge each assumption you state in the project, five times in a row. How do you stay structured instead of defensive?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Composure, structure and honesty under repeated challenge.
**Say this in the interview:** "I would treat each challenge as a useful question: acknowledge it, answer with my reason or evidence, and say how I would test it if unsure."
**Structure of the answer (a repeatable loop):**
1. Pause and restate the challenge in my own words.
2. Say why I made the assumption (the evidence or constraint).
3. Say what would change if it were wrong (impact).
4. Say how I tested or would test it.
5. Agree where they are right; do not defend everything.
**Illustrative project, replace with your real one:** Interviewer: "You assumed blank exit dates mean still employed." Me: "Yes, because the HRIS status field said Active for all 85 of them; if that were wrong, attrition would be understated. I checked 20 of them against payroll, and would check all if I could (illustrative)."
**Preparation:** Keep an "assumptions and risks" list for every project; know the riskiest two.
**Likely follow-ups:** 1) *What if you do not know?* Say "I did not test that; here is how I would." 2) *What if you are wrong?* Say so and note the change.
**Common mistakes / traps:** Defensive tone; over-long answers; pretending certainty.

### Q61 ⭐ 🔴 You have no work project to show. How would you design and describe a self-initiated analytics project in two weeks so that it survives a deep-dive?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Initiative, realistic scoping, and a project that can bear questions.
**Say this in the interview:** "I would pick one clear question, a public or synthetic dataset I can describe honestly, and finish with a short report I can defend end to end."
**Clarify first:** Who is the imaginary user and what decision do they make?
**Plan (two weeks):**
1. Days 1-2: choose a question (for example, which tenure band needs a retention pilot?), data, and write definitions.
2. Days 3-5: data checks and cleaning with a log.
3. Days 6-9: analysis, segment comparisons, one test of robustness.
4. Days 10-12: dashboard or short report, one recommendation with a measure.
5. Days 13-14: write the assumptions, limits, a README, and rehearse questions.
**Method choice and why:** Simple counts, rates and comparisons; a basic model only if I can explain it and avoid leakage.
**Pitfalls:** Too big a scope; a tutorial copy; claiming real impact; no limits stated.
**Deliverable:** A one-page summary, a dashboard or workbook, and a short methodology note. Describe it as "self-initiated practice on public (or synthetic) data".
**Likely follow-ups:** 1) *What makes it survive a deep-dive?* A defined question, a cleaning log, assumptions and limits. 2) *Real data?* Use public data; no employer data.
**Common mistakes / traps:** Presenting it as client work; ten charts and no conclusion.

### Q62 ⭐ 🔴 How would you estimate the cost of attrition for the company in your HR project, and which parts of that estimate would you flag as weak?
**Asked at:** commonly asked (no company-specific report found); cost-of-attrition estimates are a common HR-analytics topic (unverified).
**What the interviewer is checking:** Whether you can build a rough, transparent estimate and be honest about weak inputs.
**Say this in the interview:** "I would add up the cost per leaver from hiring, ramp-up, manager time and exit costs, multiply by leavers, and mark the weakest inputs."
**Structure of the answer:**
1. Leavers in the period (from the attrition analysis).
2. Cost per leaver: recruitment (agency fees, ads, recruiter time), onboarding and training, ramp-up (lower productivity while new), manager and team time, exit costs; vacancy cost if applicable.
3. Total = cost per leaver x leavers; as a share of payroll.
4. Sensitivity: low and high ranges for the weak inputs.
**Illustrative project, replace with your real one (exercise numbers):** Average headcount 800, attrition 15%, so 800 x 0.15 = 120 leavers. Average salary 6,00,000 a year. Recruitment 15% of salary = 90,000; ramp-up loss 75,000; manager time 20,000; exit processing 10,000. Cost per leaver = 1,95,000 (32.5% of salary). Total = 120 x 1,95,000 = 2,34,00,000, about 4.9% of payroll. If ramp-up loss is half or double (37,500 or 1,50,000), the total ranges from 1.89 to 3.24 crore.
**Weak parts to flag:** ramp-up productivity loss (a guess), vacancy cost (hard to measure), and who would have left anyway; also whether replacement salaries differ and whether the departing people were low cost.
**Must not claim unless true:** that these percentages are real benchmarks; confirm with finance.
**Likely follow-ups:** 1) *Why a range?* Because inputs are uncertain. 2) *Who supplies the numbers?* Finance and talent acquisition.
**Common mistakes / traps:** One precise number with false confidence; counting costs that would occur anyway; omitting ranges.

