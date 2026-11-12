# Book 8 — Scenario-Based & Data Interpretation | Part 2: Stakeholder Request Scenarios (Vague Asks, Urgent Reports) 🟡

**Target:** 70 questions | **Actual:** 79 questions
**Scope:** On-the-job stakeholder scenarios for an analyst: vague or ambiguous asks, urgent and conflicting requests, scope creep, pushback, communicating caveats and errors, and privacy-sensitive asks, with some exercise data for a checkable figure.

### Q1 ⭐⭐⭐ 🟢 A manager messages you, "Can you send me the sales numbers?" with no other detail. What do you do before you touch any data?
**Asked at:** commonly asked (no company-specific report found); vague-request prompts appear on prep question banks (unverified).
**What the interviewer is checking:** Whether you ask before you pull, instead of guessing and sending the wrong thing.
**Say this in the interview:** "I would not open the data yet. I would reply with three or four short questions: what decision it is for, which period and level, and by when. Then I send exactly that."
**First, clarify / contain:** Reply in the same chat within minutes so the manager knows it is picked up. Ask: (a) What will you use the numbers for (a review, a target, a customer call)? (b) Which period and which cut (by region, product, salesperson)? (c) What does "sales" mean here: orders booked, invoiced, or cash received, and before or after returns? (d) What format and deadline? I do not start any query until at least (a) and (c) are answered; I may offer a default ("last month, total by region, booked orders") so they can just say yes.
**What I would check, in order:**
1. Whether a similar report already exists, so I reuse its definition.
2. Which table or system is the agreed source for sales.
3. Whether the period is complete (no late-loading days).
4. Whether returns, cancellations and test orders are excluded.
5. A total I can reconcile to a number finance already published.
**If I find...:** A report already exists: send it with a note. The definition is unclear: confirm in writing before building. The manager cannot say the purpose: deliver the simplest default and label the assumptions.
**What I would tell the stakeholder:** "Happy to send this today. To get it right I need two things: which month and cut you want, and whether you mean booked or invoiced sales. If I do not hear back by 2 pm I will send last month, total by region, booked orders, and mark it clearly."
**Prevent it next time:** A short request form or template (purpose, period, definition, deadline); a one-page metric glossary.
**Likely follow-ups:** 1) *What if the manager is too busy to answer?* Send the labelled default and let them correct it. 2) *Is asking questions slow?* A two-minute exchange is cheaper than rebuilding a wrong report.
**Common mistakes / traps:** Sending a big file with no definition; asking ten questions at once; asking nothing and guessing.

### Q2 ⭐⭐⭐ 🟢 What clarifying questions would you ask when a stakeholder asks for "a dashboard on employee performance"?
**Asked at:** commonly asked (no company-specific report found); dashboard-for-a-vague-ask is a theme on prep blogs (unverified).
**What the interviewer is checking:** That you tie the dashboard to a decision and think about privacy, since performance data is sensitive.
**Say this in the interview:** "First I would ask who will use it and what decision it supports. 'Performance' can mean ratings, sales targets or productivity, and I need to know which before building anything."
**First, clarify / contain:** Ask in this order: (1) Who are the users (HR business partners, line managers, leadership) and what will they decide (promotions, coaching, pay)? (2) What does performance mean: the annual rating, goal achievement, output numbers? (3) Which employees and period are in scope? (4) How often must it refresh? (5) Who may see individual-level data, and who sees only team totals? I do not build until the metric and audience are agreed.
**What I would check, in order:**
1. Where the rating or goal data lives and how complete it is.
2. Whether rating scales changed between cycles (not comparable).
3. Whether teams have enough people to show without identifying individuals.
4. Whether HR policy or legal needs to approve who can see it (confirm with HR and legal; not verified here).
5. A one-page sketch the stakeholder signs off before the real build.
**If I find...:** Ratings are only yearly: a live dashboard adds little, so propose a cycle report. Individual-level view is requested: raise access and fairness concerns and escalate to the HR head.
**What I would tell the stakeholder:** "Here is a one-page mock-up with three views: rating distribution by team, goal achievement, and movement versus last cycle. Please confirm the definitions and who gets access. I can have a first version in one week."
**Prevent it next time:** Keep a metric glossary and a role-based access list.
**Likely follow-ups:** 1) *Why a mock-up first?* It exposes disagreements cheaply. 2) *Should managers see each other's teams?* Default to no; share only what they need.
**Common mistakes / traps:** Building charts before agreeing what performance means; ignoring privacy; showing tiny groups.

### Q3 ⭐⭐⭐ 🟢 How do you find out what a stakeholder actually needs when what they ask for (a report) differs from the decision they are trying to make?
**Asked at:** commonly asked (no company-specific report found); "request that will not solve the underlying problem" appears on prep banks (unverified).
**What the interviewer is checking:** That you look past the requested deliverable to the decision behind it.
**Say this in the interview:** "I ask 'what will you do differently depending on what the numbers show?' That one question usually reveals the real need."
**Clarify first:** The decision (what choice, by whom, by when), what would change their mind, and what they have already tried. The analysis exists to support that decision, not to fill a report.
**Plan:**
1. Ask open questions: "What is the problem you are trying to solve? What happens if we do nothing?"
2. Restate in my words: "So you must decide whether to extend the training programme, and need to know if it reduced exits. Right?"
3. Propose the smallest analysis that answers it, and say what I will not cover.
4. Check the data can answer it before promising.
5. Share a rough first cut early and adjust.
**Method choice and why:** A short conversation plus a written restatement. If the person is senior and short of time, bring a draft question and let them correct it, which is faster than a blank-page interview.
**Pitfalls:** Taking the request literally; lecturing the stakeholder that they asked wrongly; delivering what you think they need without telling them.
**Deliverable:** A one-paragraph brief: decision, question, metric definitions, data source, deadline, agreed by the stakeholder in writing.
**Likely follow-ups:** 1) *What if they insist on the original report?* Deliver it, and add a short note with the answer to the real question. 2) *How do you stay polite?* Frame it as "so I get it right", not "you are wrong".
**Common mistakes / traps:** Skipping the decision question; assuming you know their goal; never confirming in writing.

### Q4 ⭐⭐⭐ 🟢 How do you decide whether a request is a one-off ad-hoc pull or something that should become a recurring, automated report?
**Asked at:** commonly asked (no company-specific report found); intake and ad-hoc load themes appear on prep banks and an analyst blog (unverified).
**What the interviewer is checking:** That you think about repeat effort and automation value, not just the request in front of you.
**Say this in the interview:** "I ask how often the question will come back and who needs it. If it comes back more than a couple of times, I automate it; if it is tied to one decision, I do it once."
**Clarify first:** Is it tied to a single event (a board paper) or an ongoing need (a weekly attrition view)? Who will use it, and how often?
**Plan:**
1. Ask the stakeholder how often they will want it.
2. Check my request log for the same ask earlier.
3. Estimate effort: one-off pull versus building and maintaining an automated version.
4. Decide with a simple rule of thumb: a third request for the same thing, or three or more recurring users, means automate.
5. Agree an owner, a refresh schedule and a definition before automating.
**Method choice and why:** A light rule of thumb and a log, not a formal model. If the data source is unstable, stay manual until it settles.
**Pitfalls:** Automating on the first request; automating something nobody reads; building with no owner so it breaks quietly; keeping everything ad-hoc and drowning in repeats.
**Deliverable:** A decision recorded in the request log: "one-off" or "recurring, owner X, refresh weekly, definition link".
**Likely follow-ups:** 1) *What if they ask for a dashboard "just in case"?* Ask what decision it informs; start with a manual version for a month. 2) *How do you judge effort?* Hours to build plus hours per month to maintain.
**Common mistakes / traps:** Treating every request as unique; forgetting maintenance cost.

### Q5 ⭐⭐⭐ 🟢 What should go into the message or email when you hand over a report, besides the file itself?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That your handover prevents misreading, and shows you communicate the "so what".
**Say this in the interview:** "The file is not enough. I lead with the one-line finding, then definitions, caveats and what I need from them."
**First, clarify / contain:** Decide who the reader is and what they must do with it before writing.
**What I would check, in order (before sending):**
1. The totals reconcile to a known figure.
2. The period and filters are stated correctly.
3. Any data lag or exclusions are noted.
4. A second person or a re-run has confirmed the main figure.
**If I find...:** Anything unresolved: say it in the message, not in a footnote.
**What I would tell the stakeholder:** Use this structure: (1) headline in one sentence; (2) what is in the file and the period covered; (3) definitions used (for example attrition = leavers in the month divided by average headcount); (4) caveats and data cutoff date; (5) the question or decision it supports; (6) next step and who to contact. Example: "Attrition for Q2 is 12%, up from 10% in Q1, mostly in support roles. Data is as of 30 June; contractors excluded. Please tell me if you want it split by manager."
**Prevent it next time:** Save the message as a template and keep a version note in the file.
**Likely follow-ups:** 1) *How long should it be?* Short enough to read in a minute. 2) *Should I attach methodology?* Link it; do not bury the finding.
**Common mistakes / traps:** Sending a file with no context; hiding caveats; no date stamp.

### Q6 ⭐⭐⭐ 🟢 How do you confirm that you and the stakeholder share the same definition of a term like "active customer" or "attrition" before you build anything?
**Asked at:** commonly asked (no company-specific report found); aligning definitions such as "active user" before analysis is a theme on prep blogs (unverified).
**What the interviewer is checking:** That you treat definitions as the first risk, not an afterthought.
**Say this in the interview:** "I write the definition down with a tiny worked example and ask them to confirm it. People agree to words and still mean different things."
**First, clarify / contain:** Ask what counts and what does not, in their words, then restate as a rule with numbers.
**What I would check, in order:**
1. Whether a company glossary or earlier report already defines the term.
2. The inclusion rules (who is in: contractors, interns, notice-period staff).
3. The time window (monthly, rolling 12 months, year to date).
4. The denominator (average headcount, opening headcount, closing headcount).
5. A small example both of us can check by hand.
**If I find...:** Two people define it differently: show both numbers side by side and ask the owner to choose, or label them (attrition including versus excluding retirements). No owner: propose one and get written approval.
**What I would tell the stakeholder:** "By 'attrition' I mean employees who left in the quarter divided by average headcount, voluntary and involuntary separately, excluding contractors. For a team of 100 with 6 leavers that is 6%. Does that match what you have in mind?"
**Prevent it next time:** A shared glossary with owner and date; definitions printed on every dashboard.
**Likely follow-ups:** 1) *What if you still disagree?* Escalate to the metric owner, not the loudest voice. 2) *Where do you record it?* Glossary plus a line in the request log.
**Common mistakes / traps:** Assuming a common word means one thing; agreeing verbally only.

### Q7 ⭐⭐⭐ 🟢 A stakeholder wants the report "by end of day", but you are already committed to two other deadlines. How do you respond?
**Asked at:** commonly asked (no company-specific report found); prioritisation prompts appear on prep banks (unverified).
**What the interviewer is checking:** That you negotiate openly instead of silently overcommitting or refusing.
**Say this in the interview:** "I would say what I can deliver and when, ask what is truly urgent, and offer a smaller version today or a full one tomorrow."
**First, clarify / contain:** Ask what the deadline is driven by (a meeting, a decision) and what the minimum useful version looks like. Do not say yes automatically and do not say no flatly.
**What I would check, in order:**
1. How much effort this really needs (an hour or a day).
2. The real cost of delay on my two other commitments.
3. Whether my manager has a priority view.
4. Whether a partial version (headline number, one cut) would be enough today.
**If I find...:** It is small: do it and tell the others nothing changes. It is large and truly urgent: ask my manager to decide the priority, then inform the owners of the other two deadlines. It is not time-critical: agree a later date.
**What I would tell the stakeholder:** "I can give you the headline total by 5 pm today and the full regional split by noon tomorrow. If you need the full version today, one of my other deliverables will slip, so I would like to check priorities with my manager. Which works better?"
**Prevent it next time:** Share a simple team queue so requesters see load; ask for a day's notice for non-urgent asks.
**Likely follow-ups:** 1) *What if they escalate?* Let the managers settle the priority. 2) *Do you ever just stay late?* Occasionally, but not as a habit; hiding overload hides the problem.
**Common mistakes / traps:** Saying yes and missing something else; saying no with no alternative; going silent.

### Q8 ⭐⭐⭐ 🟢 How would you explain a finding to a non-technical senior leader who gives you only two minutes?
**Asked at:** commonly asked (no company-specific report found); communication appears as a must-have in most analyst job descriptions in the research sample (see market_skills_2026.md).
**What the interviewer is checking:** Whether you can lead with the answer, keep it simple and ask for a decision.
**Say this in the interview:** "Answer first, then why it matters, then what I recommend. No method, no jargon, one number and one chart at most."
**First, clarify / contain:** Before the meeting, write one sentence: "Because X, we should do Y." If I cannot, I am not ready.
**What I would check, in order:**
1. The single most important number, verified.
2. A comparison that gives it meaning (last quarter, target).
3. One likely question I can answer from the backup.
4. The decision or action I want from them.
**If I find...:** The leader interrupts: answer that question first; it is what they care about. Finding is uncertain: say so in one sentence, with what would settle it.
**What I would tell the stakeholder:** "Exits in support roles rose from 10% to 12% this quarter, almost all within a year of joining. I recommend we look at onboarding for those roles. With your OK, I will bring a plan next week." (Illustrative figures.) Then stop and listen.
**Prevent it next time:** Keep a one-page summary with the headline on top and detail below, ready for any request.
**Likely follow-ups:** 1) *How do you handle a hostile question?* Answer plainly, and offer to follow up with data. 2) *What if you need more time?* Ask for ten minutes and bring a short written note.
**Common mistakes / traps:** Starting with method; showing five charts; ending with "so, any questions?" and no recommendation.

### Q9 ⭐⭐⭐ 🟢 What is the difference between answering the question that was asked and answering the question that should have been asked, and when is each right?
**Asked at:** commonly asked (no company-specific report found); "decision behind the request" framing appears on prep banks (unverified).
**What the interviewer is checking:** That you use judgement about when to stay literal and when to dig deeper.
**Say this in the interview:** "I answer exactly what was asked, and flag the better question when I see one. I never replace their question silently."
**Explain simply:**
- **The question asked** is literal: "How many people left last month?" You answer it directly.
- **The question that should have been asked** is the one behind it: "Is attrition getting worse, and where?"
- Answer as asked when it is a clear, factual ask, it is time-critical, or the stakeholder already knows the context.
- Answer the deeper question when the literal answer would mislead (a single month with a holiday spike), or the person is clearly stuck on a decision.
- Best practice: give the literal answer first, then one line, "this might also be worth looking at", and let them choose.
**Mini-example:** Asked: "What was last month's headcount?" Literal answer: 1,180 distinct employees. Better question: "Do you mean employees on payroll, or including contractors?" Ask it before answering, since the numbers differ.
**Practice step:** Take three past requests and write the literal question, the likely real question and your one-line flag.
**Likely follow-ups:** 1) *What if they get annoyed?* Keep it short and offer the answer first. 2) *Who decides?* The stakeholder; I advise.
**Common mistakes / traps:** Overriding the ask with your own agenda; never questioning a misleading ask; delivering a long essay when a number was needed.

### Q10 ⭐⭐⭐ 🟡 The HR head says, "Attrition is too high, find out why." You have an HRIS export, exit-interview notes and two days. How do you scope and run this?
**Asked at:** commonly asked (no company-specific report found); attrition analysis is a standard HR-analytics prompt (prep-site level, unverified).
**What the interviewer is checking:** That you can scope an open question into a doable plan with honest limits.
**Say this in the interview:** "In two days I cannot prove why. I can show where attrition is concentrated and what leavers say, then recommend what to test next."
**Clarify first:** What is "too high" (versus last year, target, industry)? Which attrition (voluntary, regret, all)? Which decision follows (retention budget, manager training)? Confirm that day two ends with a short readout.
**Plan:**
1. Define attrition: leavers in the period divided by average headcount (illustrative: 48 leavers on average 400 heads is 12%, computed). Split voluntary and involuntary.
2. Clean the export: remove duplicates, contractors and wrong dates.
3. Cut by tenure, team, manager, location, role and grade; look for concentration, not averages.
4. Tag exit-interview notes into themes (pay, manager, growth, relocation) and count them.
5. Compare leavers with stayers on a few factors (tenure, last rating, time since promotion).
6. Write findings and a ranked list of hypotheses with the evidence for each.
**Method choice and why:** Counts and rates by group first. A regression or survival model only if time allows and the cuts show something worth testing.
**Pitfalls:** Small groups giving swingy rates; exit notes biased (people are polite when leaving); calling correlation a cause; naming individuals.
**Deliverable:** A two-page summary: headline rate, top three hot spots, themes, caveats, and next steps (for example a pulse survey in the hot spots).
**Likely follow-ups:** 1) *What if the data is messy?* State the cleaning rules and what is excluded. 2) *Can you say why?* I can say where and what leavers report; "why" needs more.
**Common mistakes / traps:** Promising the cause; using only the overall rate; ignoring the denominator.

### Q11 ⭐⭐⭐ 🟡 A vice president needs numbers for a board meeting in three hours, but the latest week of data is only about 90% loaded. What do you do and what do you tell them?
**Asked at:** commonly asked (no company-specific report found); incomplete-data-under-deadline appears on prep banks (unverified).
**What the interviewer is checking:** Whether you deliver something useful, protect the VP from a wrong number, and are clear about the gap.
**Say this in the interview:** "I would not present the partial week as final. I would give the last complete period as firm and the latest week as provisional, with a clearly labelled estimate."
**First, clarify / contain:** Tell the VP now that the latest week is incomplete, so there are no surprises. Ask whether the board needs the exact latest week or the trend.
**What I would check, in order:**
1. Which sources are late and when the load will finish (ask data engineering).
2. Whether the missing 10% is random or concentrated (one region, one system).
3. Past weeks: how much does a 90%-loaded week typically change once complete?
4. Whether I can produce a firm number up to the last complete week.
**If I find...:** Missing part is random: a rough estimate may work (illustrative: 4,500 shown at 90% loaded suggests about 5,000, computed as 4,500 divided by 0.9; label it as an estimate, range stated). Missing part is one region or system: do not scale up; show the gap by region. Load finishes before the meeting: refresh and re-verify.
**What I would tell the stakeholder:** "Through last week the number is 4,200 and firm (illustrative). The latest week is 90% loaded and shows 4,500; it will probably land near 5,000 but I cannot guarantee that. I suggest showing last week as final and this week as provisional. I will update you the moment the load completes."
**Prevent it next time:** Show a "data complete through" date on every report; automate a load-completeness check.
**Likely follow-ups:** 1) *Why not just scale up by 10%?* It assumes the missing data looks like the rest. 2) *What if the VP insists on a single number?* Give the estimate with the label attached.
**Common mistakes / traps:** Presenting a partial total as final; silently dropping the week; hiding the gap.

### Q12 ⭐⭐⭐ 🟡 The sales head and the finance head both ask you for "revenue by region", but their definitions differ (booked versus recognised). How do you handle it?
**Asked at:** commonly asked (no company-specific report found); conflicting metric definitions are a theme on prep banks (unverified).
**What the interviewer is checking:** That you reconcile definitions openly instead of picking a side or producing two unexplained numbers.
**Say this in the interview:** "Both are valid but they answer different questions. I would label them clearly, show a bridge between them, and ask for one agreed name for each."
**First, clarify / contain:** Do not pick one quietly. Ask each head what decision they use the number for. Booked usually measures sales performance; recognised measures what counts in the accounts under accounting rules.
**What I would check, in order:**
1. The written definitions each team uses (dates, cancellations, discounts).
2. Whether the totals differ because of timing (a contract booked in March, recognised over twelve months).
3. A reconciliation bridge: booked, plus or minus timing, equals recognised.
4. Whether the regional mapping is also the same in both.
**If I find...:** Differences are only timing: publish both with a bridge. Region mapping differs: align it first. A real data error: fix and re-issue.
**What I would tell the stakeholder:** "Sales and finance are both right: sales is looking at booked revenue, finance at recognised revenue. I will send both numbers, labelled, with a one-line bridge showing the difference. Can the two of you confirm which to call 'revenue' in the monthly deck?"
**Prevent it next time:** A shared metric glossary with distinct names (Booked Revenue, Recognised Revenue) and an owner for each.
**Likely follow-ups:** 1) *What if they refuse to agree?* Escalate to the CFO or analytics head for a ruling. 2) *Which is the default?* The one the board and finance reports use, but ask.
**Common mistakes / traps:** Sending one number and angering the other; using the word "revenue" for both.

### Q13 ⭐⭐⭐ 🟡 A stakeholder rejects your analysis because it contradicts what they expected. How do you respond in the meeting and afterwards?
**Asked at:** commonly asked (no company-specific report found); stakeholder pushback prompts appear on several prep banks (unverified).
**What the interviewer is checking:** That you stay calm, test your own work honestly, and neither cave in nor get defensive.
**Say this in the interview:** "I would ask what they expected and why, walk through my method, and re-check anything they can point to. If I am right I hold the position politely; if I am wrong I say so quickly."
**First, clarify / contain:** In the meeting: listen, do not argue. Ask, "What did you expect to see, and what is that based on?" Their expectation may contain information I lack (a policy change, a data issue).
**What I would check, in order:**
1. Their reasoning: is there something I missed (definition, filter, period)?
2. My data and logic again, with a fresh re-run.
3. A different cut or a smaller sample that could explain the gap.
4. A second opinion from a colleague.
**If I find...:** I made an error: correct it quickly and openly. Their view rests on a different definition: align and show both. The data truly contradicts them: present evidence, confidence level and limits, and agree what would change the conclusion.
**What I would tell the stakeholder:** "I understand it differs from what you expected. I will re-check the filters and definitions today and come back by tomorrow noon. If it still holds, I will show you the underlying rows so we can look at it together."
**Prevent it next time:** Share early drafts and assumptions before the final meeting so surprises are smaller.
**Likely follow-ups:** 1) *What if they escalate?* Let a neutral reviewer check the work. 2) *Do you ever change your answer?* Yes, when the evidence changes, not when pressure does.
**Common mistakes / traps:** Defensiveness; caving without evidence; blaming the stakeholder's intuition.

### Q14 ⭐⭐⭐ 🟡 You discover an error in a report you sent yesterday, and leadership has already quoted the number. What exactly do you do, in what order?
**Asked at:** commonly asked (no company-specific report found); error-before-or-after-presentation prompts appear on prep banks (unverified).
**What the interviewer is checking:** Integrity, speed and a calm, orderly correction.
**Say this in the interview:** "Tell my manager and the affected people immediately, fix it, send a clear correction, then find the root cause. I do not wait to be asked."
**First, clarify / contain:** First 15 minutes: confirm the error is real and size it (how wrong, which numbers, who has used them). Do not quietly fix and resend without telling anyone.
**What I would check, in order:**
1. What exactly was wrong (a filter, a join, a wrong period) and which other outputs share it.
2. The corrected number, verified by a second method.
3. Who received the report and who has quoted it.
4. Whether the correction changes the conclusion or only the size.
**If I find...:** Conclusion unchanged: send a short correction with the new figure. Conclusion changes: speak to the main stakeholder directly first, then send it in writing. Already in a deck or external: tell my manager so the owner can correct it.
**What I would tell the stakeholder:** "I found an error in yesterday's report: the filter excluded one region, so the figure should be X, not Y. The trend and recommendation are unchanged (or: the recommendation changes as follows). I have fixed the file and will send a revised version in an hour, and I will add a check so it does not happen again."
**Prevent it next time:** Peer review for numbers leaders will quote; reconciliation checks against totals; a version log.
**Likely follow-ups:** 1) *What if no one has noticed?* Still correct it; quoted numbers spread. 2) *Do you explain how it happened?* Briefly and without excuses.
**Common mistakes / traps:** Hiding it; correcting silently; over-apologising and not saying the right figure.

### Q15 ⭐⭐⭐ 🟡 A stakeholder keeps adding "just one more cut" to a request you have already started. How do you manage the scope?
**Asked at:** commonly asked (no company-specific report found); scope creep prompts appear on prep banks (unverified).
**What the interviewer is checking:** That you protect the deadline and quality while staying helpful.
**Say this in the interview:** "I would write down what was agreed, price each addition in time, and offer to put extras into a second phase."
**First, clarify / contain:** Pause and restate the original scope in writing: what, which period, due date. Ask whether the new cuts change the decision or are "nice to know".
**What I would check, in order:**
1. Does the new cut change the decision? If not, it can wait.
2. Is the data available at that level (for example by manager)?
3. Effort: minutes or a day?
4. Group-size rules: does the cut produce groups too small to be reliable?
**If I find...:** Cheap: add it and note it. Expensive: offer Phase 2 with a date. Truly critical: ask which part of the original scope can move, so the deadline holds.
**What I would tell the stakeholder:** "Happy to add the cut by location. It adds about half a day. I can deliver the agreed version on Thursday as planned, and send the location view on Friday, or move everything to Friday. Which do you prefer?"
**Prevent it next time:** A short written brief signed off at the start; a rule that new asks after sign-off go in a "v2 list".
**Likely follow-ups:** 1) *What if it is a senior person?* Same approach; trade-offs are easier to accept when visible. 2) *Do you ever refuse?* Rarely; I defer and make the cost visible.
**Common mistakes / traps:** Saying yes every time; never writing the scope down; delivering a cluttered report.

### Q16 ⭐⭐⭐ 🟡 The marketing head asks, "Did the campaign work?" What do you ask back, and what do you deliver?
**Asked at:** commonly asked (no company-specific report found); campaign-impact prompts appear on prep banks (unverified).
**What the interviewer is checking:** That you define "work", insist on a fair comparison and avoid claiming cause without evidence.
**Say this in the interview:** "I would ask what success was meant to be, then compare against what would have happened without the campaign, not just before versus after."
**Clarify first:** What was the goal (sales, sign-ups, awareness)? Which metric and target? Which dates, channels, audience? Was there a control group, a holdout or a comparable region? Were other things happening (price change, festival season)?
**Plan:**
1. Agree the success metric and target in writing.
2. Pull results for the campaign period and a comparison: same period last year, or a similar group that did not see it.
3. Adjust for trend and seasonality (compare growth rates, not raw totals).
4. Add cost: campaign spend divided by extra sales (cost per incremental sale).
5. Give a verdict with a range and a confidence level.
**Method choice and why:** Simple comparison with a control or last-year baseline first. A test and control design or difference-in-differences only if the data allows; do not run a model for a one-page question.
**Pitfalls:** Before-and-after with no baseline; selection bias (campaign shown to likely buyers); several campaigns overlapping; one short period.
**Deliverable:** A one-page answer: "Sales rose X%, of which about Y points above the normal trend; cost per extra sale Z; confidence moderate; next time run a holdout."
**Likely follow-ups:** 1) *No control group?* Use last year's pattern and say it is weaker evidence. 2) *Does lift equal profit?* No, include costs and margin.
**Common mistakes / traps:** Reading the raw increase as the effect; promising causation; ignoring cost.

### Q17 ⭐⭐⭐ 🟡 Three stakeholders each send an "urgent" request at 10 am. How do you decide the order, and how do you tell the two who wait?
**Asked at:** commonly asked (no company-specific report found); "prioritizing when everything is urgent" appears on prep banks (unverified).
**What the interviewer is checking:** A clear prioritisation rule and transparent communication.
**Say this in the interview:** "I would rank by decision impact and the real deadline, then reply to all three quickly with a time, so nobody is left guessing."
**First, clarify / contain:** Reply to all three within minutes: acknowledge, ask for the actual deadline and what the number is for. Do not start the loudest one by default.
**What I would check, in order:**
1. Real deadline (a board meeting at 3 pm, or just "soon").
2. Impact: money, customers, compliance or a leader's decision.
3. Effort: a five-minute pull can go first.
4. Dependencies, for example another team waiting on me.
5. My manager's view if two are close.
**If I find...:** A tiny task: do it between larger ones. A genuine tie: ask my manager to decide. One has a hard external deadline: it goes first.
**What I would tell the stakeholder:** "I have three requests due today. Yours is third in the queue because the meeting is tomorrow; I will send it by 4 pm. If your deadline is earlier than I understood, tell me and I will re-plan."
**Prevent it next time:** A visible team queue with agreed priority levels (urgent means a hard deadline and a named decision).
**Likely follow-ups:** 1) *What if all three really are critical?* Escalate to the manager to set priority; do not decide alone. 2) *Do you tell them why?* Yes, one line.
**Common mistakes / traps:** Doing whoever is most senior or loudest; staying silent; promising all three by 5 pm.

### Q18 ⭐⭐⭐ 🟡 A stakeholder says, "Just give me the number, I do not need the caveats." The number depends on a shaky assumption. How do you respond?
**Asked at:** commonly asked (no company-specific report found); communicating caveats is a theme on prep banks (unverified).
**What the interviewer is checking:** That you stay honest and still respect their time.
**Say this in the interview:** "I will give the number first, then one sentence that says how far to trust it. A figure without that sentence can embarrass them later."
**First, clarify / contain:** Do not argue about caveats; shorten them. Ask what they will do with the number, since that decides how much the assumption matters.
**What I would check, in order:**
1. How sensitive the number is to the assumption (rerun with a low and a high case).
2. Whether a better assumption can be validated quickly.
3. What decision hinges on the number: if both cases lead to the same decision, the caveat is minor.
**If I find...:** Both cases support the same action: give one number, one short caveat line. Range crosses a decision threshold: say so clearly and recommend what to verify first.
**What I would tell the stakeholder:** "The number is about 120. It rests on the assumption that conversion stays the same; if it drops, it could be as low as 90. Either way, the decision to proceed holds. I will confirm the assumption by Thursday." (Illustrative figures.)
**Prevent it next time:** Standardise a "number, range, one-line reason" format so caveats become habit.
**Likely follow-ups:** 1) *What if they delete your caveat in their deck?* Raise it with them directly. 2) *Is a range ever too vague?* Give a best estimate inside it.
**Common mistakes / traps:** Handing over a bare number; burying them in caveats; sulking if overruled.

### Q19 ⭐⭐⭐ 🟡 A manager asks you to find data that supports a decision they have already made. How do you handle it?
**Asked at:** commonly asked (no company-specific report found); ethics-in-analysis prompts appear on prep banks (unverified).
**What the interviewer is checking:** Integrity: you will look for evidence honestly, not cherry-pick.
**Say this in the interview:** "I would say I will test the decision with the data and report what it shows, supportive or not. That protects them as well as me."
**First, clarify / contain:** Ask what decision was made and what was the original reason. Do not agree to find only supporting data; do not accuse them of bias either.
**What I would check, in order:**
1. The claim being made, stated as a testable question.
2. Data for and against it, with fair comparison groups.
3. Whether the evidence is strong, weak or mixed.
4. What conditions would make the decision go wrong.
**If I find...:** Data supports: say so, with limits. Data is mixed: report both sides and suggest risk controls. Data contradicts: tell the manager privately first, with evidence, and suggest what to adjust.
**What I would tell the stakeholder:** "I will review all the evidence on this so the case holds up when challenged. If it supports your decision, great. If it shows some risk, I will raise it early so you can plan for it."
**Prevent it next time:** Agree the question and success measure before the analysis starts.
**Likely follow-ups:** 1) *What if they insist?* Present results fairly, and escalate privately if misleading use is likely. 2) *Is supporting evidence ever fine?* Yes, if the full picture is shown.
**Common mistakes / traps:** Cherry-picking; refusing outright; lecturing about bias.

### Q20 ⭐⭐⭐ 🟡 A senior leader pings you for a "quick insight" from a dataset you have not yet validated. How much checking do you do before replying, and what do you say?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Speed with safety: a proportionate level of checking and honest labelling.
**Say this in the interview:** "I do a fast sanity check, 10 to 15 minutes, then reply with the insight clearly marked as preliminary. I would not send something I have not even eyeballed."
**First, clarify / contain:** Ask what they will use it for. If it goes into a decision or a deck, I check more; if it is for their own curiosity, a labelled quick view is fine.
**What I would check, in order:**
1. Row counts and date range against what I expect.
2. Duplicates and missing values in the key fields.
3. One total that I can reconcile to a known report.
4. Whether the finding is large and stable, or sits on a few rows.
5. An outlier check, for example extremely large or small values.
**If I find...:** Everything is clean: send with "preliminary". Something is off: tell them it is not reliable yet and give an ETA. No time to check: say what I did and did not verify.
**What I would tell the stakeholder:** "Early read: attrition looks higher in support roles. I have checked totals and duplicates, but not yet the definitions, so treat it as preliminary. I will confirm by tomorrow before anything goes into a deck."
**Prevent it next time:** A standard five-line validation checklist; keep clean, documented datasets for common questions.
**Likely follow-ups:** 1) *What if they forward it?* The "preliminary" label travels with the message. 2) *Would you ever refuse?* Only if the data is clearly broken; then say what is wrong.
**Common mistakes / traps:** Replying with no checking; replying with no label; taking two days when two hours was needed.

### Q21 ⭐⭐⭐ 🟡 How do you say no, or "not yet", to a request without damaging the relationship?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can protect capacity and quality while staying collaborative.
**Say this in the interview:** "I say what I can do, not only what I cannot, give a date, and explain the trade-off in a sentence."
**First, clarify / contain:** Understand why they want it and how urgent. Often "no" is really "not this week" or "not in this form".
**What I would check, in order:**
1. Priority versus my other commitments.
2. Whether a smaller version or an existing report can serve.
3. Whether data or access is missing (a real blocker).
4. Whether another person or team should own it.
**If I find...:** Capacity issue: offer a later date. Data or privacy issue: explain and propose an alternative (grouped or anonymised view). Out of scope: point to the right owner.
**What I would tell the stakeholder:** "I cannot do the full analysis this week because of the quarter-end report, but I can send the headline numbers by Thursday and the full cut on the 20th. Would that work?" Or: "I cannot share individual salaries, but I can give team averages for groups of at least five."
**Prevent it next time:** Share the team's priorities and queue openly, so a "not yet" is understood.
**Likely follow-ups:** 1) *What if it is your boss?* Show the trade-off and let them choose. 2) *How often can you say no?* Rarely; mostly "yes, and here is when".
**Common mistakes / traps:** A flat "no" with no reason; vague "will try"; apologising excessively.

### Q22 ⭐⭐⭐ 🟡 The recruiting head asks for "time to hire" for the quarter. What do you ask before computing it, and how do you present the result?
**Asked at:** commonly asked (no company-specific report found); HR-metric definition prompt (judgement, not a sourced report).
**What the interviewer is checking:** That you define start and end points, handle skew and avoid a misleading average.
**Say this in the interview:** "I would first agree the start and end of the clock, then report the median with the spread, not just the average."
**Clarify first:** Start point: job approved, job posted, or candidate applied? End point: offer accepted or joining date? Does it count hires made in the quarter, or requisitions opened? Are internal moves, withdrawn or cancelled roles included? Is it split by role or level?
**Plan:**
1. Fix definitions in writing (for example posting date to offer acceptance).
2. Pull each hire's start and end dates; check for missing or out-of-order dates.
3. Compute days per hire, then the median, the 75th percentile and the count.
4. Split by role family and level; show only groups with enough hires.
5. Compare with last quarter on the same definition.
**Method choice and why:** Median first, because a few very slow hires pull the average up. Illustrative: seven hires took 30, 35, 40, 42, 45, 50 and 120 days; the mean is about 52 days (51.7, rounded), the median 42. Report both and say why.
**Pitfalls:** Counting only closed roles (hides roles still open and slow); mixing leadership and entry roles; blending different definitions.
**Deliverable:** A small table: median, range, number of hires, by role family, with the definition on the page and a note on any open requisitions.
**Likely follow-ups:** 1) *Why is "time to fill" different?* Often measured from the requisition approval; confirm the company's usage. 2) *Open roles?* Report the age of open roles separately.
**Common mistakes / traps:** Not defining the clock; using the mean only; ignoring roles still open.

### Q23 ⭐⭐⭐ 🟡 A stakeholder quotes your chart in a slide deck with a different conclusion from yours. What do you do?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you correct misuse of your work firmly, privately and constructively.
**Say this in the interview:** "I would first make sure I am reading it right, then talk to them directly and offer a corrected slide, not wait for the meeting."
**First, clarify / contain:** Look at exactly what the slide claims and compare it with what the chart supports. Check whether their reading is defensible, since sometimes a different view is fair.
**What I would check, in order:**
1. Whether they changed the chart, or just the words around it.
2. Whether my original caveats were lost.
3. Who will see the deck and when it is presented.
4. Whether their conclusion is a different but valid reading.
**If I find...:** A valid alternative reading: discuss and add both. A clear misreading (for example causation claimed from a correlation): ask them to change the wording; offer a suggested sentence. They refuse and it matters: raise it with my manager before the presentation.
**What I would tell the stakeholder:** "Thanks for using the chart. I noticed the slide says the campaign caused the rise, but the data shows sales rose and the same happened last year without a campaign. Could we change the title to 'Sales rose 20%, similar to the usual seasonal rise'? I can send updated wording now."
**Prevent it next time:** Put the conclusion and caveats on the chart itself, and add a source line and owner name.
**Likely follow-ups:** 1) *What if it is already presented?* Follow up in writing and correct it in the next meeting. 2) *Public or private?* Private first.
**Common mistakes / traps:** Ignoring it; criticising in front of others; assuming bad intent.

### Q24 ⭐⭐⭐ 🟡 Your manager asks for a figure from an HRIS export you know includes contractors and exited staff. The ask was "how many employees do we have?". How do you answer?
Illustrative export: 1,250 rows, 1,180 distinct employee IDs, of which 1,090 have status Active and 90 have status Exited with a past end date.
(Exercise data only.)
**Asked at:** commonly asked (no company-specific report found); HRIS headcount ambiguity is a judgement gap-fill (not a sourced report).
**What the interviewer is checking:** That you clean and define before you count, and show how the total was reached.
**Say this in the interview:** "I would not say 1,250. I would remove duplicates and exited staff, ask whether contractors count, and give the cleaned number with the bridge."
**What the data shows:** The export has 1,250 rows but only 1,180 distinct IDs, so 70 rows are repeats. Of the 1,180 people, 1,090 are active and 90 have already left.
**Working:**
1. Duplicate rows: 1,250 minus 1,180 = 70 rows to remove (keep one row per employee ID).
2. People in the file: 1,180 distinct IDs.
3. Exited staff: 90, who are not current employees. 1,180 minus 90 = 1,090 active (check: 1,090 + 90 = 1,180).
4. Contractors: the data does not say how many are among the 1,090. If "employees" excludes contractors, the number is 1,090 minus the contractor count; I would filter by worker type.
**Result:** Current headcount is at most 1,090 (active, distinct IDs), and lower once contractors are removed. Not 1,250 (which would overstate by 160, or about 12.8% of 1,250).
**Caveats / what else I would check:** Why the duplicate rows exist (rehires, multiple assignments, transfers); whether "Active" includes staff on long leave or notice period; the date of the export; and whether finance or payroll holds a different official figure to reconcile against.
**Next step / recommendation:** Reply: "1,090 active people as of the export date; this includes contractors, which I can split out. The raw file has 1,250 rows, including 70 duplicates and 90 exited staff." Agree the definition and keep a standing headcount rule.
**Likely follow-ups:** 1) *Why not use the row count?* It double-counts. 2) *What if payroll shows a different number?* Reconcile by status and date.
**Common mistakes / traps:** Reporting row count; ignoring contractors; counting leavers as current staff.

### Q25 ⭐⭐⭐ 🟡 A stakeholder says, "Sales were 500 before the campaign and 600 after, so the campaign grew sales 20%." The same period last year grew 18% without a campaign. What do you say?
Before: 500 | After: 600 | Same-period growth last year: 18% (exercise data).
**Asked at:** commonly asked (no company-specific report found); before-and-after versus baseline is a standard prep-site theme (unverified).
**What the interviewer is checking:** That you separate the total change from the change caused by the campaign.
**Say this in the interview:** "The 20% is right as growth, but most of it was likely to happen anyway. Against last year's 18% trend, the campaign explains about 2 percentage points, and I would not call even that proven."
**What the data shows:** Sales rose from 500 to 600, which is a 20% increase. The same period last year also rose 18% with no campaign, so growth was normal for this time of year.
**Working:**
1. Observed growth: (600 minus 500) divided by 500 = 20%.
2. Expected growth without the campaign, using last year's pattern: 500 x 1.18 = 590.
3. Extra sales above expectation: 600 minus 590 = 10.
4. As growth: 10 divided by 500 = 2 percentage points (20% minus 18%). As a share of the expected 590: about 1.7%.
**Result:** Observed growth 20%; baseline growth 18%; apparent campaign effect about 10 units, or 2 percentage points (not 2%, since 20% minus 18% is a difference in rates). Only one comparison year and one period.
**Caveats / what else I would check:** One year is a thin baseline; check other years; week-to-week noise (is 10 units inside normal variation?); price changes, stock, festivals; campaign cost; whether the audience was already likely to buy.
**Next step / recommendation:** Say "the campaign probably added a small amount at most; to know, run a holdout region next time". Compare 10 extra units against spend before judging.
**Likely follow-ups:** 1) *Is 2 points significant?* Not from this data; need several periods or a control. 2) *Percentage versus percentage point?* 20% to 18% is a 2-point gap, which is about an 11% relative difference.
**Common mistakes / traps:** Claiming the full 20%; mixing percent and percentage points; ignoring seasonality.

### Q26 ⭐⭐⭐ 🟡 A stakeholder asks for "average ticket resolution time" and you see these five resolution times in hours: 2, 2, 3, 4, 40. Which figure do you report, and what do you tell them?
Resolution times (hours): 2, 2, 3, 4, 40 (exercise data).
**Asked at:** commonly asked (no company-specific report found); mean versus median with outliers is a standard prep-site theme (unverified).
**What the interviewer is checking:** That you notice skew and choose the figure that tells the truth, while still being transparent.
**Say this in the interview:** "I would report the median, 3 hours, because the 40-hour ticket drags the mean up to 10.2. I would also mention that one ticket and why."
**What the data shows:** Four tickets were solved in 2 to 4 hours; one took 40 hours. The "average" depends heavily on that one.
**Working:**
1. Sum: 2 + 2 + 3 + 4 + 40 = 51 hours.
2. Mean: 51 divided by 5 = 10.2 hours.
3. Median: sorted 2, 2, 3, 4, 40; the middle value is 3 hours.
4. Mean without the 40-hour ticket: 11 divided by 4 = 2.75 hours.
5. The single slow ticket accounts for 40 of 51 hours, about 78%.
**Result:** Median 3 hours; mean 10.2 hours. Typical ticket: about 3 hours. Mean says 10.2, which does not describe any normal ticket.
**Caveats / what else I would check:** Five tickets is too few for firm conclusions; is the 40-hour ticket a real delay or a data error (a reopened or forgotten ticket)? Do not delete it silently; investigate it. Also check clock rules (business hours or calendar hours, waiting-for-customer time).
**Next step / recommendation:** Report "median 3 hours, mean 10.2 hours, one ticket took 40 hours and I am checking why", and for a service target suggest a percentage resolved within X hours (here 4 of 5, or 80%, within 4 hours).
**Likely follow-ups:** 1) *Why not drop the outlier?* It may be a real problem the team needs to know about. 2) *When is the mean right?* For totals, such as workload hours.
**Common mistakes / traps:** Reporting 10.2 as "typical"; deleting 40 without saying so; no definition of the clock.

### Q27 ⭐⭐⭐ 🟡 Your team receives about 12 ad-hoc requests a week, each taking roughly 90 minutes. Your working week is 40 hours. What share of time do they use, and what would you propose to your manager?
12 requests x 90 minutes; 40-hour week (exercise data).
**Asked at:** commonly asked (no company-specific report found); reserved ad-hoc capacity and intake triage are common themes in prep banks (unverified).
**What the interviewer is checking:** Whether you do the arithmetic first, then propose a system instead of just complaining about workload.
**Say this in the interview:** "12 requests at 90 minutes is 18 hours, which is 45% of a 40-hour week. I would not accept that open-ended; I would propose a capped, triaged intake."
**Clarify first:** Is this one person's load or the whole team's? Does the 40 hours already include meetings and project work? I will assume the 18 hours land on one analyst.
**Plan:**
1. Working: 12 x 90 = 1,080 minutes = 18 hours. 18 / 40 = 45%. That leaves 22 hours for meetings, planned projects, dashboards and fixes.
2. Look at the 12 requests: how many repeat (same question every week), how many are really decisions that need data, how many are "nice to know".
3. Propose to the manager: a reserved ad-hoc budget of about 20 to 25% (8 to 10 hours, so roughly 5 to 6 requests of 90 minutes at that size; my suggestion, not a standard).
**Method choice and why:** Simple triage first: a single intake form, a priority rule (decision date, who is affected), and a weekly "ad-hoc quota" the manager can see. Turn repeating requests into a recurring report or self-service dashboard (that pays back fast: build once, answer many times).
**Pitfalls:** Saying "I am overloaded" without numbers; refusing everything; letting urgent-looking asks bypass the log.
**Deliverable:** A one-page note: current load (45%), request mix, proposed cap, what gets automated, what gets declined or deferred, and a review in a month.
**Likely follow-ups:** 1) What if the manager says keep taking all of them? Show the cost: 45% now leaves 22 hours, and every extra request displaces planned work; ask them to choose what drops. 2) How do you measure success? Share of ad-hoc time, median turnaround, number of repeat asks converted.
**Common mistakes / traps:** Quoting 45% as if it were a problem on its own (some ad-hoc work is the job); no proposal; forgetting that estimates of 90 minutes are rough and should be tracked for a few weeks.

### Q28 ⭐⭐⭐ 🔴 Your manager and a director give you conflicting priorities for the same week, and each says theirs is more important. What do you do?
**Asked at:** commonly asked (no company-specific report found); conflicting-priority prompts appear in prep banks (unverified).
**What the interviewer is checking:** Whether you surface the conflict openly and let the right people decide, rather than guessing or quietly picking a side.
**Say this in the interview:** "I would not choose between them myself. I would put both asks, the effort and the deadlines side by side and ask my manager to agree the order with the director, because that decision is theirs."
**First, clarify / contain:** Confirm both requests are really in conflict (can I do both with a smaller scope or a later date for one?). Do not start on one in silence, and do not tell either of them the other is less important.
**What I would check, in order:**
1. Deadline and what decision each piece of work supports.
2. Effort of each (hours) and what I can finish in the week.
3. Whether one can be delivered in a lighter version (a rough number now, the full analysis later).
4. Who is the owner of my priorities (usually my manager).
**If I find...:** Both fit with a partial scope: do that and tell both. They truly clash: go to my manager first with the facts and a recommended order; if the director is senior, ask the manager to talk to them, or ask for a short three-way message so the decision is on record. One is urgent and one is not: say so factually.
**What I would tell the stakeholder:** "I have two requests due this week and I cannot finish both in full. Request A needs about 12 hours and B about 15. Could you and the director confirm which goes first? Until I hear, I will start with A, which has the earlier deadline, and I will update you by noon tomorrow."
**Prevent it next time:** A shared priority list or intake log that managers can see, and a weekly planning note on what is committed.
**Likely follow-ups:** 1) What if the director insists on it right now? Do it if the manager agrees, and tell the manager what it displaces. 2) What if my manager is unavailable? Message both with the trade-off, work on the earlier deadline, and follow up.
**Common mistakes / traps:** Silently picking the more senior person; working extra hours and hiding the problem; complaining about the other party; delivering both late.

### Q29 ⭐⭐⭐ 🔴 A senior stakeholder insists that a metric you know is misleading goes into the monthly review deck unchanged. How do you handle this?
**Asked at:** commonly asked (no company-specific report found); stakeholder pushback and caveat communication are frequent themes in prep banks (unverified).
**What the interviewer is checking:** Whether you protect accuracy without being rude or obstructive, and know when to escalate.
**Say this in the interview:** "I would first show them concretely why it misleads, then offer a fix that still serves their purpose. If they still want it, I would add a clear footnote and tell my manager, but I would not present something I know is wrong as fact."
**First, clarify / contain:** Ask what the metric is meant to show and what decision it feeds. Do not argue in the meeting, and do not quietly change the number.
**What I would check, in order:**
1. Exactly how it misleads (wrong denominator, mix change, partial period, different definition).
2. Size of the distortion, with one example computed both ways.
3. A replacement that gives the stakeholder what they need (the same metric with context, or a better one beside it).
4. Whether my company has a metric definition or data owner I can cite.
**If I find...:** The distortion is small and the label can fix it: keep the metric with a clear definition and footnote. It changes the conclusion: propose showing both versions side by side. They still refuse and it is material: tell my manager, keep the footnote ("definition: ..., excludes ..."), and do not sign it off as my own analysis.
**What I would tell the stakeholder:** "I want this to hold up if someone challenges it. On the current definition it shows X, but on the like-for-like basis it is Y, which changes the message. Can we show X with a one-line note, plus Y on the next slide? I can have it ready by tomorrow."
**Prevent it next time:** A written KPI definition owned by one person, reviewed before each deck.
**Likely follow-ups:** 1) What if they are the CEO? Same approach, with the one-page evidence and my manager in the loop. 2) Is it ever fine to leave it? If the difference is trivial and labelled, yes.
**Common mistakes / traps:** Lecturing on statistics; refusing outright; silently changing the number; going over their head first.

### Q30 ⭐⭐⭐ 🔴 You are asked for a number you cannot produce reliably in the time given. How do you decide between delivering a rough estimate, delivering late, and declining, and how do you phrase each?
**Asked at:** commonly asked (no company-specific report found); tight-deadline and incomplete-data scenarios appear in prep banks (unverified).
**What the interviewer is checking:** Whether you can pick an option on purpose, label uncertainty, and keep trust.
**Say this in the interview:** "I decide by what the number will be used for. If a rough range is enough for the decision, I give it clearly labelled. If a wrong number would cause harm, I deliver late. I decline only when it cannot be produced responsibly at all."
**First, clarify / contain:** Ask what decision this feeds and when it is made. Do not send a precise-looking number you cannot defend.
**What I would check, in order:**
1. Decision and deadline: what error is tolerable?
2. What data I have, what is missing, and how much that could move the answer.
3. Can I get a bounded estimate (range, sample, last period scaled)?
4. How long the reliable version would take.
**If I find...:** A range will do for the decision: deliver an estimate. The decision is high-stakes or the number is audited (payroll, finance, regulatory): deliver late, with a firm date. The data does not exist or a number would mislead: decline that specific number and offer an alternative.
**What I would tell the stakeholder:** Estimate: "My best estimate is 1,100 to 1,300, based on last quarter's data; it is not final because two sources are missing. Fine for planning, not for external use." Late: "The reliable figure needs the March file; I can give it by Thursday 5 pm. Is that in time?" Decline: "I cannot give a trustworthy number for this because the data is not tracked; here is what I can give instead."
**Prevent it next time:** Log data gaps, agree standard turnaround for new metrics.
**Likely follow-ups:** 1) Can you combine options? Yes: a labelled rough figure today and the final later. 2) What if they ignore the label? Repeat it in writing and mention the range with the number.
**Common mistakes / traps:** One-point estimates with no range; saying yes then silently being late; declining without an alternative.

### Q31 ⭐⭐ 🟢 What is the difference between an ad-hoc request, a recurring report and a self-service dashboard, and how do you steer stakeholders towards the right one?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand the three delivery modes and can match them to the need, not just build whatever is asked.
**Say this in the interview:** "Ad-hoc is a one-off question, a recurring report is the same answer on a schedule, and a self-service dashboard lets people explore on their own. I steer by how often the question comes back and who needs to ask it."
**Explain simply:**
- Ad-hoc request: one question, answered once (for example, "how many people left from Pune in March?"). Quick, but costs analyst time each time.
- Recurring report: a fixed set of numbers sent on a schedule (a weekly attendance summary). Predictable, needs maintenance when definitions change.
- Self-service dashboard: an interactive page (Power BI, Tableau) where users filter and slice themselves. Highest set-up cost, lowest cost per question, needs a trusted data model and training.
**How I steer:** Ask "how often will you need this?" and "who else will?" Once or twice: ad-hoc. Same question every week or month: recurring report. Many people asking varied slice-and-dice questions: dashboard.
**Worked mini-example:** If three people ask the same headcount-by-department question each week at 30 minutes each, that is 1.5 hours a week; a dashboard built in a few days removes it.
**Practice step:** Look at your last 10 requests and tag each as ad-hoc, recurring or dashboard candidate.
**Likely follow-ups:** 1) When is a dashboard a bad idea? When the question is a one-off or the definitions are still unsettled. 2) How do you get people to adopt it? Involve users, train them, retire the old report.
**Common mistakes / traps:** Building a dashboard for a one-off; leaving recurring reports manual forever; sending ad-hoc numbers that nobody can reproduce later.

### Q32 ⭐⭐ 🟢 A stakeholder asks for "all the data" on a topic. What do you do?
**Asked at:** commonly asked; "all the data" is a standard vague-request prompt in prep question banks (Dataford-style, unverified).
**What the interviewer is checking:** Whether you find the decision behind the request instead of dumping files.
**Say this in the interview:** "I would ask what they are trying to decide, then offer a focused dataset or summary. A data dump rarely answers a question and can create privacy and accuracy problems."
**First, clarify / contain:** Ask, politely: what question are you trying to answer, who will use it, by when, and in what form (summary or rows)? Do not export everything yet.
**What I would check, in order:**
1. The decision or problem behind the ask.
2. Which fields and period actually matter.
3. Sensitivity: personal data, salaries, anything restricted.
4. Whether a summary table or dashboard answers it better than raw rows.
**If I find...:** A clear question: deliver a focused summary and offer the detail on request. They truly need rows for their own analysis: share a cleaned, documented extract with only needed columns and access approval. They cannot say what they want: offer two or three example outputs and let them pick.
**What I would tell the stakeholder:** "To give you something useful rather than 50 columns to wade through, could you tell me what decision this supports? I can send a one-page summary by Wednesday, and the detailed extract if you still need it."
**Prevent it next time:** A short request form with "decision, deadline, format".
**Likely follow-ups:** 1) What if they insist? Share a minimal, approved extract with a data dictionary. 2) What if it contains personal data? Check access rules first.
**Common mistakes / traps:** Sending everything to be safe; refusing without helping; not documenting column meanings.

### Q33 ⭐⭐ 🟢 How do you keep track of incoming requests so nothing is lost, and what information do you log for each?
**Asked at:** commonly asked (no company-specific report found); request intake logs appear in prioritisation guides (unverified).
**What the interviewer is checking:** Whether you work in an organised way and make workload visible.
**Say this in the interview:** "One place for every request, whichever channel it came in on: a simple tracker or ticket board with a few fixed fields."
**Explain simply:**
- Single intake point: a form, shared inbox or ticket board (Jira, Trello, even a shared sheet). Chat and hallway asks get entered by me, then confirmed back to the requester.
- Fields to log: date received, requester and team, the question in one line, the decision it supports, deadline, priority, estimated effort, data sources, status (new, in progress, waiting, done), owner, date delivered, link to the output.
- Weekly review: look at the open list, re-prioritise, close finished items.
**Worked mini-example:** A row might read: "12 Nov, HR business partner, attrition by tenure band for exit review, due 15 Nov, estimate 2 hours, status: waiting for HRIS extract."
**Practice step:** Set up a sheet with these columns and log your next five requests; check after a month how many repeated.
**Likely follow-ups:** 1) How do you handle urgent asks? Log them first, then triage; urgent does not mean unlogged. 2) What do you do with the log later? Count types and time to find automation candidates.
**Common mistakes / traps:** Keeping requests in your head or inbox; no deadline or purpose field; never closing items, so the list becomes noise.

### Q34 ⭐⭐ 🟢 How do you set expectations on turnaround time when a request arrives without a deadline?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you handle missing deadlines proactively rather than guessing or ignoring them.
**Say this in the interview:** "I ask when the decision is made, then give my own estimate in writing, and agree on it. No deadline usually means the urgency is unknown, not that there is none."
**Explain simply:**
- Ask: "When will you use this, and is there a meeting or decision it is for?"
- Estimate: size the work (a quick count, a new analysis, data not yet available) and add a buffer for questions and checks.
- Offer standard service levels: for example "simple counts same or next day, new analyses in about three working days" (my illustration; use your team's norm).
- Confirm in writing with a date and say what could change it.
**Worked mini-example:** "I can send the headcount split by Friday noon. If the HRIS extract is late, I will tell you by Thursday."
**Practice step:** Write down your actual turnaround times for your last 10 tasks; use them as your realistic norm.
**Likely follow-ups:** 1) What if they then say it is urgent? Re-triage, and show what it displaces. 2) What if you miss the date? Tell them early with a new date.
**Common mistakes / traps:** Silently choosing a date; promising "as soon as possible"; forgetting the data-wait time.

### Q35 ⭐⭐ 🟢 What do you do when a stakeholder asks for a chart type that will mislead (for example a truncated bar chart or a 3D pie)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know why some charts mislead and can persuade instead of refusing.
**Say this in the interview:** "I would find out what message they want, show a clearer version beside theirs, and explain in one sentence why. I would not simply refuse or simply comply."
**Explain simply:**
- Truncated bar chart: the axis starts above zero, so small differences look huge. Bars encode length, so they should start at zero. A line chart can use a non-zero axis because it shows change.
- 3D pie: depth and angle distort slice sizes, and many slices are hard to compare. A sorted bar chart is easier to read.
**What I would do:**
1. Ask what point they want to make.
2. Build both versions quickly; show the honest one and the requested one.
3. Say: "Bars are read by length; if the axis starts at 90, a 2-point gap looks like a doubling."
4. If they still insist, mark the axis clearly (a break symbol and a label) or add the numbers on the bars.
**Worked mini-example:** Bars of 92 and 96 on an axis starting at 90 show one bar about three times as tall as the other (6 vs 2 units), although the real gap is about 4%. (96 / 92 = 1.043.)
**Likely follow-ups:** 1) Is a truncated axis ever fine? On a line chart, if labelled. 2) What if it is for external use? Escalate to my manager.
**Common mistakes / traps:** Being preachy; saying "pie charts are always bad"; refusing the task.

### Q36 ⭐⭐ 🟢 When should you involve your manager in a stakeholder conflict, and when should you resolve it yourself?
**Asked at:** commonly asked (no company-specific report found); team-conflict behavioural prompts are common (unverified).
**What the interviewer is checking:** Judgement on escalation: not hiding problems, not running to the manager over small things.
**Say this in the interview:** "Small, factual disagreements I resolve directly. If it involves priorities, seniority, data accuracy, ethics, or it has not been resolved after one honest attempt, my manager hears about it early."
**Explain simply:**
- Resolve myself: misunderstanding of a definition, a format preference, a deadline I can renegotiate, a difference I can settle with data.
- Involve the manager: two seniors want different things; the request breaks a data-privacy or ethics rule; the stakeholder is unresponsive and blocking delivery; a mistake with real impact; conflict that has become personal.
- How: bring facts, what I tried, and what I recommend, not just the complaint.
**Worked mini-example:** Two teams report different headcount numbers. I check definitions with both and fix it myself. If one team demands I change the number against policy, I involve the manager.
**Practice step:** Write a two-line escalation note: facts, impact, my recommendation.
**Likely follow-ups:** 1) Will escalating look weak? Not if done early and with a proposal. 2) What if the manager is the conflict? Check HR or a skip-level, carefully.
**Common mistakes / traps:** Escalating everything; escalating only after missing the deadline; criticising the stakeholder instead of describing the issue.

### Q37 ⭐⭐ 🟡 A stakeholder asks for a quick forecast and says, "Just tell me the exact number we will hit." How do you respond?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you communicate uncertainty in a useful way instead of faking precision or being unhelpful.
**Say this in the interview:** "A forecast is a best estimate with a range, not an exact promise. I would give one planning number, a realistic range, and what could move it."
**First, clarify / contain:** Ask what decision it feeds (hiring plan, stock, target) and the horizon. Do not give one exact number with no caveat.
**What I would check, in order:**
1. History: how stable was this measure, how seasonal?
2. A simple baseline (last year same period, recent average and trend).
3. Known changes coming (promotion, hiring freeze, policy).
4. How far past forecasts missed, to size the range.
**If I find...:** Stable history: narrow range. Volatile or short history: wide range and say so. They need one number: give the central estimate and name the range next to it.
**What I would tell the stakeholder:** "My best estimate is about 1,000, and I would plan for 900 to 1,100. It would be lower if X happens. I will recheck it at month end and send an updated number."
**Prevent it next time:** Track forecast versus actual each month and share the error.
**Likely follow-ups:** 1) What if they hold you to the exact figure? Explain that it is a target to manage towards, and the range shows the risk. 2) Which method? Start with a baseline and trend; complexity only if it beats the baseline.
**Common mistakes / traps:** False precision; a vague "it depends"; hiding assumptions.

### Q38 ⭐⭐ 🟡 How do you handle a stakeholder who sends the same request in three different channels (email, chat, a hallway ask) with slightly different wording each time?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you consolidate duplicates and confirm what they really want.
**Say this in the interview:** "I would treat it as one request, log it once, and send back a single written summary asking them to confirm which version is right."
**First, clarify / contain:** Do not build three things. Collect all three messages and compare the differences.
**What I would check, in order:**
1. Are the wordings really the same ask, or are the differences (period, filter, metric) meaningful?
2. Which version is the newest or most specific.
3. Whether other people are also asking for the same thing.
**If I find...:** Same ask: merge and reply on one channel. Different asks hidden in the wording: list the options and ask them to pick. Repeated pinging because of urgency: confirm the deadline.
**What I would tell the stakeholder:** "I received your request by email, chat and in person; I have combined them as: attrition by department for Q2, excluding contractors, due Friday. Is that right? I will treat this thread as the master."
**Prevent it next time:** One intake channel and a polite redirect ("please add it to the tracker so it does not get lost").
**Likely follow-ups:** 1) What if it is a senior person? Same, just more gently. 2) What if they dislike the process? Offer to log it for them.
**Common mistakes / traps:** Answering each message separately and giving different numbers; ignoring the duplicates; being sharp about the repetition.

### Q39 ⭐⭐ 🟡 An offshore or client-side stakeholder in another time zone sends vague requirements late on Friday for a Monday morning deliverable. How do you handle it?
**Asked at:** commonly asked (no company-specific report found); offshore delivery is typical in services firms (unverified).
**What the interviewer is checking:** Whether you manage ambiguity and time zones calmly, without wasting a weekend or guessing.
**Say this in the interview:** "I would reply within the hour with a short list of assumptions and questions, start on the parts that are clear, and tell them what I will deliver by Monday if I do not hear back."
**First, clarify / contain:** Read the request once. Do not silently guess the vague parts, and do not drop everything for the whole weekend.
**What I would check, in order:**
1. What is clear enough to start now (data pull, shell of the report).
2. The three to five questions that change the output (metric definition, period, filters, format).
3. How long the work really takes against the Monday deadline.
4. Whether my manager should know about the deadline risk.
**If I find...:** The questions can be answered by assumption: state my assumptions and proceed. The ambiguity is critical: ask a concrete multiple-choice question so they can answer quickly. The work cannot fit: tell them now, offer a partial version Monday and the full one on a named date.
**What I would tell the stakeholder:** "Thanks. I will assume: headcount at month end, India only, summary by department. Please correct me by 9 am your time Monday. I have started and will send a first version by 10 am IST, and I will flag anything I assumed."
**Prevent it next time:** A requirements template, a Thursday cut-off for Monday asks, and a shared agreement on response times.
**Likely follow-ups:** 1) Would you work the weekend? Only if the business need is clear and my manager agrees. 2) What if the client never replies? Deliver on the stated assumptions, labelled.
**Common mistakes / traps:** Waiting silently until Monday; guessing without saying so; over-promising.

### Q40 ⭐⭐ 🟡 A stakeholder asks you to share an employee-level salary list with their team "for planning". What do you do?
**Asked at:** commonly asked (no company-specific report found); privacy and minimum-group-size themes appear in HR-analytics question banks (unverified).
**What the interviewer is checking:** Whether you protect sensitive HR data and still help the business need.
**Say this in the interview:** "I would not send named salaries right away. I would ask what the planning needs and check whether they are authorised. Most planning can be done with aggregated or banded data."
**First, clarify / contain:** Pause the sharing; do not say "no" bluntly. Ask what the purpose is and who in their team would see it.
**What I would check, in order:**
1. The business purpose (budget, headcount plan, pay review) and what level of detail it really needs.
2. Authorisation: is this person's role entitled to this data under company policy? Does the HR head or data owner need to approve?
3. Whether aggregated data (by grade, band or department) or an anonymised file works.
4. Applicable rules: the company's data policy and privacy law (for India, the DPDP Act is relevant; from memory, unverified, confirm with legal or the data protection team).
**If I find...:** Aggregates are enough: send those, with small groups suppressed. Names are truly needed and approved: share via a controlled, access-restricted file, only needed fields, and log it. Not authorised: decline politely and point them to the data owner.
**What I would tell the stakeholder:** "Salary data is restricted, so I cannot send named lists directly. For planning I can give average and range by grade and department by Wednesday. If you need individual data, the HR head can approve it and I will prepare it securely."
**Prevent it next time:** Role-based access, a data-sharing checklist, and approval trail.
**Likely follow-ups:** 1) What if they are very senior? Still confirm authority with the data owner. 2) How do you send aggregated data safely? No small groups, no hidden columns.
**Common mistakes / traps:** Emailing the file to be helpful; saying only "policy says no"; sending a spreadsheet with hidden columns.

### Q41 ⭐⭐ 🟡 A team lead asks for average salary by department. One department has only two employees. How do you handle the request?
Department sizes (exercise data): Finance 38, Support 120, Legal 2.
**Asked at:** commonly asked (no company-specific report found); small-group suppression is a standard privacy practice in HR analytics (unverified).
**What the interviewer is checking:** Whether you notice that an average over two people reveals individual pay.
**Say this in the interview:** "Finance with 38 and Support with 120 are fine to report. An average for Legal's 2 people nearly exposes each salary, so I would suppress or combine it."
**First, clarify / contain:** Ask what the average is for and whether the lead may see salary data at all. Do not send the Legal number yet.
**What I would check, in order:**
1. Group sizes: 38, 120 and 2, total 160.
2. Company or policy minimum group size for reporting (often something like 5 or 10; the rule is set by your organisation, confirm it).
3. With 2 people, if one person knows their own salary and the average, they can work out the colleague's salary exactly. A manager who knows one salary does the same.
4. Whether the lead needs department averages or something else (budget by grade).
**If I find...:** Group below the minimum: show "n<5, suppressed" or combine Legal with a related function ("Corporate functions"), only if the combined group is large enough. Policy has no rule: propose one and ask the data owner.
**What I would tell the stakeholder:** "Here are averages for Finance and Support. Legal has only two people, so showing its average would effectively reveal individual salaries; I have grouped it under Corporate functions. If you need Legal separately, the HR head would need to approve."
**Prevent it next time:** Build suppression into the report or dashboard (a minimum group size rule).
**Likely follow-ups:** 1) What about reporting the median? Same issue with two people. 2) What about repeated reports that let someone subtract? Watch for differencing; suppress the complement too.
**Common mistakes / traps:** Reporting the average because "it is only an average"; hiding the group without saying so; forgetting that combining reports can reveal it.

### Q42 ⭐⭐ 🟡 A product manager wants to claim in a leadership update that a feature "caused" a rise in retention, based on a before-and-after comparison. How do you respond?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand correlation versus causation and can offer a more defensible alternative.
**Say this in the interview:** "A before-and-after comparison shows retention rose after launch, not that the feature caused it. I would suggest 'is associated with', and show what else changed, ideally with a comparison group."
**First, clarify / contain:** Ask what exactly was compared (which users, which period) and whether anything else changed. Do not say the claim is false; say it is not yet supported.
**What I would check, in order:**
1. Other changes in the same period: pricing, a marketing campaign, seasonality, a new cohort mix.
2. Whether the trend was already rising before the launch.
3. Users who used the feature versus those who did not (they may have been more engaged already, which is selection bias, where the group chose itself).
4. A fair comparison: a holdout group, a staggered rollout, or an A/B test.
**If I find...:** Another cause fits: say so. A comparison group shows the same lift: stronger claim possible. No comparison possible: report the lift with caveats.
**What I would tell the stakeholder:** "Retention rose from X to Y after launch. That is encouraging, but other things changed too, so I would word it as 'retention rose after the launch' rather than 'the feature caused it'. If we hold back the feature for 10% of users for a month, we can say it with confidence."
**Prevent it next time:** Plan the measurement before launch.
**Likely follow-ups:** 1) Is A/B testing always possible? No; consider difference-in-differences or matched groups. 2) What if leadership wants the strong claim? Use the cautious wording and offer the test.
**Common mistakes / traps:** Accepting "after therefore because of"; lecturing; ignoring seasonality.

### Q43 ⭐⭐ 🟡 A stakeholder reads a survey result and says, "85% of employees are satisfied, so morale is great." What do you check and say?
Survey sent to 800 employees; 40 responded; 34 of the 40 chose satisfied or very satisfied (exercise data).
**Asked at:** commonly asked (no company-specific report found); survey response-rate caveats are a gap-fill theme (judgement).
**What the interviewer is checking:** Whether you check response rate, bias and uncertainty before accepting a headline.
**Say this in the interview:** "34 of 40 is 85% of respondents, but only 5% of employees responded. I would call it 'among those who answered', not 'employees'."
**What the data shows:** 34 / 40 = 85% satisfied among respondents. Response rate: 40 / 800 = 5%. Non-responders: 760 people.
**Working:**
1. Satisfied share of respondents: 34 / 40 = 0.85.
2. Response rate: 40 / 800 = 0.05 (5%).
3. Sampling error: with only 40 answers the 95% interval for 85% is roughly 71% to 93% (Wilson method; the simple margin of error is about plus or minus 11 points).
4. Bound for everyone: if none of the 760 silent employees were satisfied, the company-wide figure is 34 / 800 = 4.25%; if they were as satisfied as respondents, 85%. The data cannot tell us which.
**Result:** 85% of respondents, 5% response rate, so the survey cannot support "morale is great" for the whole company.
**Caveats / what else I would check:** Who responded (happy or angry people respond more; self-selection), mix by department, location and tenure compared with the workforce, whether the survey was anonymous, whether the question was leading, and the trend against previous surveys.
**Next step / recommendation:** Say "85% of the 40 who responded are satisfied; the response rate is low, so treat it as indicative". Push for higher response (reminders, manager time, anonymity assurance), and compare respondents with headcount by group.
**Likely follow-ups:** 1) What is a good response rate? It depends; ask your survey team for your usual level (not verified here). 2) Could you weight it? Yes, by group, if you have enough responses per group.
**Common mistakes / traps:** Treating respondents as the whole workforce; quoting the 85% without n; calling it statistically significant.

### Q44 ⭐⭐ 🟡 A manager says attrition in a 40-person team "doubled" this quarter. You see the leavers count. How do you respond and how would you present the change?
Previous quarter: 2 leavers; this quarter: 4 leavers; team size about 40 (exercise data).
**Asked at:** commonly asked (no company-specific report found); small-number changes are a gap-fill theme (judgement).
**What the interviewer is checking:** Whether you separate a true statement ("doubled") from a useful one, and avoid overreacting to small counts.
**Say this in the interview:** "Technically yes, 2 to 4, but that is 5% to 10% of the team in a quarter, an increase of 5 percentage points, and with numbers this small it can be noise. I would show counts and rates together."
**What the data shows:** Leavers went from 2 to 4 in a team of about 40.
**Working:**
1. Last quarter rate: 2 / 40 = 5.0% (of headcount, about).
2. This quarter rate: 4 / 40 = 10.0%.
3. Relative change: (4 - 2) / 2 = +100%, the "doubled". Absolute change: 10% - 5% = 5 percentage points (pp, the plain difference of two percentages).
4. Annualised for scale: 4 x 4 / 40 = 40% a year if this pace continued (a crude scale-up, not a forecast).
5. Uncertainty: treating leavers as counts, an exact 95% range for 2 leavers is about 0.2 to 7.2 and for 4 is about 1.1 to 10.2, so the two ranges overlap heavily.
**Result:** Doubled in count (+100%), up 5 percentage points of headcount (5% to 10%). The difference between the two quarters is small relative to the noise.
**Caveats / what else I would check:** Average headcount (not a rough 40), reasons for leaving (regretted or not, retirement, transfer), who left (one manager? one role?), seasonality (appraisal cycle), the company rate for comparison and a longer trend (12 months).
**Next step / recommendation:** Show "2 leavers (5%), then 4 leavers (10%)" with a trailing 12-month line; look into the reasons for the 4 exits before calling it a trend.
**Likely follow-ups:** 1) Is it significant? Not on two quarters of small counts. 2) What would worry you? A pattern: same manager, same role, regretted exits.
**Common mistakes / traps:** Agreeing with "doubled" without the base; mixing percent and percentage points; panic over 4 people; ignoring that it is still real people.

### Q45 ⭐⭐ 🟡 A stakeholder wants to know the conversion rate. Sessions were 20,000, unique visitors 16,000 and orders 500. Which denominator do you use, and what do you tell them?
Sessions: 20,000 | Unique visitors: 16,000 | Orders: 500 (exercise data).
**Asked at:** commonly asked (no company-specific report found); conversion denominators are a gap-fill theme (judgement).
**What the interviewer is checking:** Whether you know the denominator changes the answer and you pick one deliberately and label it.
**Say this in the interview:** "It depends on the question, so I would name the definition. Per session it is 2.5%, per unique visitor 3.125%; I would report both with labels and agree which one is the standard."
**What the data shows:** The same 500 orders give two different rates depending on what you divide by.
**Working:**
1. Session conversion rate: 500 / 20,000 = 2.5%.
2. Visitor conversion rate: 500 / 16,000 = 3.125%, about 3.1%.
3. Sessions per visitor: 20,000 / 16,000 = 1.25, so some visitors came back.
4. The gap: 3.125% / 2.5% = 1.25 times, the same 1.25.
**Result:** 2.5% per session; 3.1% per unique visitor (rounded to one decimal; 3.125% exactly). Not 20 or 31 percent: the difference is the denominator, not an error.
**Caveats / what else I would check:** Are orders counted as orders or as buyers (one person with two orders)? What period and does it include bots or internal traffic? Is "unique visitor" counted by device or by login (one person on two devices counts twice)? Does the order belong to the session where it was placed or an earlier visit?
**Next step / recommendation:** Use session conversion for trend and comparing marketing channels (it is the usual industry convention in e-commerce, from memory, unverified); use visitor conversion when asking how many people ever buy. Document the definition on the dashboard and keep it the same each month.
**Likely follow-ups:** 1) Which is higher and why? Visitor-based, because the denominator is smaller. 2) Why not divide by page views? It would mix in browsing depth.
**Common mistakes / traps:** Quoting a rate without saying the denominator; switching denominators between months; mixing sessions from one source and visitors from another.

### Q46 ⭐⭐ 🟡 A stakeholder disputes your number because their own spreadsheet shows a different total. How do you resolve it without turning it into a blame exercise?
**Asked at:** commonly asked (no company-specific report found); conflicting-metric prompts appear in prep banks (unverified).
**What the interviewer is checking:** Whether you reconcile calmly and systematically instead of defending or conceding.
**Say this in the interview:** "I would say 'let us work out why they differ', ask for their file, and compare definitions and filters step by step. Often both numbers are right for different definitions."
**First, clarify / contain:** Do not defend the number or assume they are wrong. Do not change anything yet. Agree to a short reconciliation.
**What I would check, in order:**
1. Definition: what each of us counts (headcount at month-end versus average, with or without contractors).
2. Period and cut-off date (data pulled on different days).
3. Filters and joins in each (location, status, duplicates).
4. Source and refresh: system export versus manual copy, any edits in their sheet.
5. Compare at the smallest level (a list of IDs) and find the exact rows that differ.
**If I find...:** Different definitions: document both and agree on one standard. Their data is stale or edited: share the current source. My error: say so plainly, fix it, tell all recipients.
**What I would tell the stakeholder:** "Thanks for sharing your file. I compared the two: the 12 difference comes from 9 contractors included in yours and 3 joiners after the cut-off. Both are correct for their definitions; I suggest we use the HRIS definition and I will label it on the report."
**Prevent it next time:** A written KPI definition, a single source of truth, and a version/date stamp on every report.
**Likely follow-ups:** 1) What if you are wrong? Own it quickly and fix it. 2) What if they will not agree? Take the definition question to the metric owner or my manager.
**Common mistakes / traps:** Defending first; saying "your spreadsheet is wrong"; fixing silently without telling others who used the old number.

### Q47 ⭐⭐ 🟡 You are asked to build a weekly report that you suspect nobody will read. How do you check before investing the time?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you test value before building, and avoid creating shelfware.
**Say this in the interview:** "I would ask who will use it and for which decision, then start with a small version, track whether it is opened and used, and keep it only if it is."
**First, clarify / contain:** Ask: who reads it, what do they do differently after reading it, and what happens if it does not exist for a month? Do not build the full automated version yet.
**What I would check, in order:**
1. A named owner and a decision it supports.
2. Whether an existing report or dashboard already answers it.
3. A manual, simple version for two to four weeks (a sheet or email).
4. Evidence of use: replies, open counts, questions in meetings, decisions linked to it.
5. Cost to build and maintain versus time saved.
**If I find...:** It is used and drives a decision: automate it. Used by one person only occasionally: keep it manual or on-demand. Nobody uses it: stop and tell the sponsor kindly, with the evidence.
**What I would tell the stakeholder:** "I will send a simple version for four weeks and check whether it helps. If it does not change a decision, we stop it and I move to something that does. Does that work?"
**Prevent it next time:** A review of all recurring reports every quarter; retire those unused.
**Likely follow-ups:** 1) What if the senior person says build it anyway? Build the lightest version and agree a review date. 2) How do you measure use? Opens in the BI tool, replies, and asking directly.
**Common mistakes / traps:** Building a big automated pipeline first; assuming "no feedback" means "liked it"; refusing without trying.

### Q48 ⭐⭐ 🟡 A new stakeholder who has never worked with data asks you to "use AI to tell us what to do". How do you reset the expectation and still help them?
**Asked at:** commonly asked (no company-specific report found); a judgement-based scenario.
**What the interviewer is checking:** Whether you can translate hype into a concrete problem without talking down.
**Say this in the interview:** "I would not say no and I would not promise magic. I would ask what decision they are trying to make, then show what data and simple methods can do, and where AI could help."
**First, clarify / contain:** Ask: what decision or problem is this for, what do you do today, and what would a good answer look like? Do not start a model.
**What I would check, in order:**
1. The real problem (reduce attrition, speed up hiring, forecast demand).
2. Data available: how much, how clean, how long a history.
3. A simple descriptive analysis first (where is the problem, how big).
4. Whether a model adds value and whether we can act on its output.
5. Risks: bias, privacy, explainability, especially with people decisions.
**If I find...:** Data is thin or messy: fix and count first. A clear prediction problem with data: pilot a simple model and test it. They want AI to "decide": explain it informs the decision; a person stays accountable.
**What I would tell the stakeholder:** "AI works on data, and it suggests rather than decides. Let us start with what is driving the problem: I can give you a one-page view in a week, and then we can see whether a prediction tool is worth it."
**Prevent it next time:** A short data-and-analytics primer for stakeholders; shared examples of past analyses.
**Likely follow-ups:** 1) Can you use AI tools at all? Where company policy and data privacy allow it, for drafting or coding help, not for sensitive data. 2) What if they are disappointed? Show a quick win.
**Common mistakes / traps:** Jargon; promising a model; dismissing the idea; skipping the basics.

### Q49 ⭐⭐ 🟡 A stakeholder asks you for a number the same afternoon that your data source team says is not available until next week. How do you handle both sides?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you negotiate between both sides with options instead of passing the message along.
**Say this in the interview:** "I would ask the stakeholder what they need it for and ask the data team what is really blocking, then offer options: a labelled estimate today, or the confirmed number next week."
**First, clarify / contain:** Do not promise today's number, and do not just say "not available". Check both sides first.
**What I would check, in order:**
1. With the stakeholder: the decision, how accurate it must be, and the real deadline.
2. With the data team: what exactly is missing, why, and is there a partial or earlier extract.
3. Alternatives: last period's figure, a sample, a partial-month figure, a proxy from another source.
4. Who can approve a faster route (the data owner or manager).
**If I find...:** An estimate is enough: give it today, clearly labelled with a range. Accuracy matters: give a date and keep them updated. Data team can give part of it sooner: use that.
**What I would tell the stakeholder:** "The final number is only available next Tuesday. For this afternoon I can give you an estimate of about X, based on last month's data, accurate to roughly plus or minus 5%. If you need it final for the meeting on Friday, I will ask the data team to prioritise it."
**What I would tell the data team:** "Which part is delayed, and what is the earliest date for a partial extract? The stakeholder needs it for a decision on Friday."
**Prevent it next time:** Share data availability schedules; set known refresh dates on the dashboard.
**Likely follow-ups:** 1) What if the estimate is quoted as final? Label it in writing. 2) What if the data team will not move? Escalate with the business impact.
**Common mistakes / traps:** Blaming the data team in front of the stakeholder; sending a rough number with no label; staying silent until the deadline.

### Q50 ⭐⭐ 🟡 You deliver an analysis and the stakeholder says, "This is not what I asked for." How do you recover, and how do you prevent it next time?
**Asked at:** commonly asked (no company-specific report found); scope and expectation mismatch is a common theme (unverified).
**What the interviewer is checking:** Whether you respond without defensiveness and fix the root cause in the process.
**Say this in the interview:** "I would listen, ask what they expected to see, and find the gap. Then I would fix it quickly, and next time I would confirm the question in writing before starting."
**First, clarify / contain:** Stay calm; do not argue about what was said. Ask "what did you expect to see, and what decision is it for?"
**What I would check, in order:**
1. The original request wording versus what they now describe.
2. Whether the gap is the question, the definition, the format or the level of detail.
3. How much of the existing work can be reused.
4. The new deadline and realistic effort.
**If I find...:** The request was ambiguous: share the responsibility and fix it. Requirements changed: agree the new scope and time. I misread: own it and correct quickly.
**What I would tell the stakeholder:** "Thanks for the feedback. So you need attrition by manager rather than by department, for the last 12 months. I can reuse most of the data and send the revised version by tomorrow noon. I will send you a short summary of the question first, to confirm."
**Prevent it next time:** Restate the request in one line plus the decision, definition, period and format; share a mock-up or sample output before building; show a draft early.
**Likely follow-ups:** 1) Who is at fault? It does not matter; the process is. 2) What if it keeps happening with one person? Use a short request template with them.
**Common mistakes / traps:** Defending the work; blaming vague requirements; redoing everything from scratch; not confirming the revised ask.

### Q51 ⭐⭐ 🟡 A stakeholder wants to change the definition of a KPI mid-quarter because the current one looks bad. How do you respond?
**Asked at:** commonly asked (no company-specific report found); KPI redefinition is a gap-fill theme (judgement).
**What the interviewer is checking:** Whether you protect metric integrity while recognising that some definitions do need fixing.
**Say this in the interview:** "I would ask why: if the old definition is genuinely flawed, change it openly for the future and show both. If it is only because it looks bad, I would hold the definition and discuss the underlying issue."
**First, clarify / contain:** Ask what is wrong with the current definition and what they would change. Do not change it quietly and do not refuse without hearing them.
**What I would check, in order:**
1. Is the definition genuinely flawed (counts the wrong thing, includes ineligible cases)?
2. The effect: recompute the quarter under both definitions and see the difference.
3. Whether the change is documented, approved by the metric owner and applied to all periods.
4. Whether it affects incentives, targets or external reporting.
**If I find...:** A real flaw: change it with approval, recompute history on the new basis, and show the old definition as a bridge. Cosmetic: keep it, discuss the real drivers. The owner insists: record it in writing; escalate if it is material.
**What I would tell the stakeholder:** "I am happy to review the definition. Under the current one we are at X and under the proposed one at Y. If we change it, we should apply it to all periods, document it, and show the old figure for one quarter so people can follow the change. Shall we put it to the metric owner?"
**Prevent it next time:** A KPI definition document with an owner, a change log and a review at quarter boundaries.
**Likely follow-ups:** 1) Is it ever fine mid-quarter? If the old one is plainly broken and everyone agrees, with a restated history. 2) What if targets were set on the old one? Re-baseline them.
**Common mistakes / traps:** Quietly switching; changing only the recent period; assuming bad intent.

### Q52 ⭐⭐ 🟡 A request arrives through a chain: the CEO asked a director, who asked a manager, who asked you. The request makes no sense to you. What do you do?
**Asked at:** commonly asked (no company-specific report found); a judgement-based scenario.
**What the interviewer is checking:** Whether you can trace the original need through a chain without being intimidated or guessing.
**Say this in the interview:** "I would go back to the person who gave it to me and ask for the original question and purpose, because requests change as they pass along. If needed, I would ask to speak to the director."
**First, clarify / contain:** Do not build something that does not make sense. Do not skip the chain and go straight to the CEO.
**What I would check, in order:**
1. Ask my manager for the exact original wording, the context and the deadline.
2. Write down my reading in one or two lines and confirm it (it often turns out a number or term got garbled).
3. Identify the decision behind it and who will use the answer.
4. If still unclear, ask to join a short call with the director or the originator.
**If I find...:** The message was garbled: fix and proceed. The original need is clear but the proposed analysis will not answer it: suggest what will. The request is real but unreasonable on time: say what can be done by when.
**What I would tell the stakeholder:** To the manager: "I want to get this right for the CEO. Could you share the original wording or ask what decision it supports? My understanding is X; is that right? I can have a first view by tomorrow." To the director, if reached: "I would like to confirm the definition and the purpose so the number answers what the CEO needs."
**Prevent it next time:** Request template that travels with the ask (question, decision, deadline, owner), and direct access to the originator for clarification.
**Likely follow-ups:** 1) What if the manager says "just do it"? Do the best interpretation, state assumptions in writing, and confirm early. 2) What if it is politically sensitive? Keep it factual and involve my manager.
**Common mistakes / traps:** Guessing silently; assuming the CEO must be right; going over heads; delivering an analysis nobody asked for.

### Q53 ⭐⭐ 🟡 A request from the finance team conflicts with a data-privacy rule your company follows. How do you handle it?
**Asked at:** commonly asked (no company-specific report found); privacy and minimum-group-size themes appear in people-analytics prep material (unverified).
**What the interviewer is checking:** Whether you protect personal data without being unhelpful, and whether you escalate instead of quietly breaking or quietly refusing.
**Say this in the interview:** "I would not send anything yet. I would find out what finance actually needs, then offer the closest version the rule allows, and ask the data owner or privacy lead to approve anything in the grey zone."

**First, clarify / contain:** Ask finance what decision the data supports (for example, cost per department, not names). Do not share the raw data, and do not say a flat "no" either. Note down the request and the rule it touches.
**What I would check, in order:**
1. Which rule applies (for example, no employee-level salary outside HR), by reading the written policy, not by guessing.
2. Whether finance's goal can be met with totals, averages or grouped data instead of named rows.
3. Whether finance already has approved access through another route.
4. Who owns the rule (privacy officer, HR head, legal) and how exceptions are approved.
**If I find...:** The need is met by grouped data: send that. The need truly needs row-level data: raise a written exception request to the data owner with purpose, fields, who sees it and for how long. The rule is unclear: ask the privacy team before sending anything. Laws such as India's DPDP Act may apply (from memory, unverified); I would confirm with legal, not interpret them myself.
**What I would tell the stakeholder:** "I want to get you what you need. Employee-level pay is restricted, so I can give you cost by department today. If you need named rows, I will send an exception request to the privacy owner now and update you by tomorrow noon."
**Prevent it next time:** Agree a short data-sharing guide with finance (what is open, what needs approval) and use role-based access so the question does not depend on one analyst's judgement.

**Likely follow-ups:** 1) *What if the finance head insists?* Escalate to my manager and the data owner together; I do not override the rule. 2) *What if time is short?* Send the safe aggregated version first.
**Common mistakes / traps:** Sending the data "just this once"; refusing without offering an alternative; deciding the legal question yourself.

### Q54 ⭐⭐ 🟡 How would you handle a stakeholder who wants a dashboard "with everything on it"?
**Asked at:** commonly asked (no company-specific report found); "all the data" requests appear in prep question banks (unverified, snippet-level).
**What the interviewer is checking:** Whether you turn a wish into decisions and keep a dashboard focused.
**Say this in the interview:** "I would ask what decisions the dashboard must support, then build a short first page for those, with detail one click away."

**Clarify first:** Who will use it, how often, and what they will do differently after seeing it. "Everything" usually means "I do not want to ask again later."
**Plan:**
1. Ask for the top 3 to 5 questions the person asks every week.
2. Map each question to one metric, with a written definition.
3. List the other requests separately as "phase 2" with a reason each.
4. Sketch a one-page wireframe on paper or slides before touching the tool.
5. Build page 1 (headline numbers, one trend, one breakdown), and put detail on drill-through pages.
6. Review with the stakeholder after one week of real use.
**Method choice and why:** Start with a sketch, because changing a drawing costs minutes and changing a built dashboard costs days. If they still want more, a separate "data explorer" page works better than crowding page 1.
**Pitfalls:** 30 charts nobody reads; metrics with no definitions; slow loading; saying "no" without showing the cost (more clutter, slower report, harder to trust).
**Deliverable:** A one-page dashboard, a definitions tab, and a short backlog for phase 2. I would show them usage after a month and drop unused visuals.

**Likely follow-ups:** 1) *They insist?* Build the extra pages but keep page 1 clean. 2) *How do you know it worked?* Usage and whether decisions cite it.
**Common mistakes / traps:** Agreeing to everything to avoid conflict; building before the wireframe is agreed.

### Q55 ⭐⭐ 🟡 How do you present a negative finding (for example, a flagship programme is not working) to the person who owns that programme?
**Asked at:** commonly asked (no company-specific report found); bad-news communication is a standard behavioural theme in prep material (unverified).
**What the interviewer is checking:** Whether you are honest, fair to the owner, and constructive.
**Say this in the interview:** "I would meet the owner privately before anyone else sees it, show the evidence calmly, and come with options, not only the bad news."

**First, clarify / contain:** Recheck my own work first: definitions, filters, comparison group. Do not circulate the finding or put it in a group deck before the owner hears it.
**What I would check, in order:**
1. The result holds on a second cut (different period, different group).
2. What "working" meant when the programme started (the owner's own success measure).
3. Whether the result could be due to timing, small numbers or who joined the programme.
4. Whether any part works (for example, one location or segment).
**If I find...:** The result is solid: present it as "here is what we learned, here are options". It is fragile: say it is early and name the extra data needed. A segment works: lead with that as a path forward.
**What I would tell the stakeholder:** "Before I share this wider, I want you to see it first. Against the goal we agreed, the numbers are below target. Here is how I checked it, here is what I am unsure about, and here are three options. Can we go through it for 30 minutes tomorrow?"
**Prevent it next time:** Agree the success metric and evaluation plan before a programme launches, so the finding is no surprise.

**Likely follow-ups:** 1) *They disagree with the data?* Walk through the method together and invite them to point to a flaw. 2) *They ask you to soften it?* I can change tone, never the numbers.
**Common mistakes / traps:** Surprising the owner in a big meeting; blaming people; hiding the finding in an appendix.

### Q56 ⭐⭐ 🔴 The finance head asks for a daily cost report and the data engineering team says the daily feed is unreliable. You must satisfy both. What do you propose?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can find a middle path that serves both sides instead of picking one.
**Say this in the interview:** "I would offer a daily report that is clearly labelled provisional, plus a reliable final version, and agree with data engineering a plan to fix the feed."

**First, clarify / contain:** Ask finance what they do with the daily number (spot overspend? approve payments?). Ask data engineering exactly how the feed fails (late, missing rows, duplicates) and how often.
**What I would check, in order:**
1. Failure pattern over the last few weeks (days failed, size of error).
2. Whether the daily decision needs exact figures or a rough trend.
3. Whether a reliable source exists for the final numbers (for example, month-end ledger).
4. What simple automatic checks could flag a bad load (row count, total versus yesterday).
**If I find...:** Errors are small and rare: publish daily with a "provisional" tag and a data-quality status line. Errors are large: publish daily only a trend with a range, and give the exact figure at T+2 days. The feed is mostly late: schedule the report after the load and show "data as of".
**What I would tell the stakeholder:** "You will get a daily cost report at 10 am marked provisional, with a check light showing whether the feed passed. The final numbers are confirmed on day two. Data engineering and I will review the failures weekly and aim to retire the label once it is stable."
**Prevent it next time:** Write the agreement down (what is daily, what is final, who fixes what) and automate the load checks.

**Likely follow-ups:** 1) *What if finance quotes the provisional number externally?* The label and a footnote say it must not be. 2) *How do you measure improvement?* Share of days passing checks.
**Common mistakes / traps:** Promising an exact daily number you cannot guarantee; blaming data engineering.

### Q57 ⭐⭐ 🔴 You made an error that changed a hiring or pay decision before it was caught. Describe how you handle the first hour, the first day and the follow-up.
**Asked at:** commonly asked (no company-specific report found); "error discovered after delivery" is a common prep theme (unverified).
**What the interviewer is checking:** Ownership, speed, honest communication, and fixing the cause.
**Say this in the interview:** "I would stop the harm first, tell my manager immediately, and fix and document it, without hiding or blaming."

**Illustrative size (made-up numbers):** a formula error put 6 of 40 offers in the wrong pay band, each Rs 50,000 a year too high. That is 15% of offers and Rs 3,00,000 a year in total.
**First hour (contain):** Confirm the error is real, then tell my manager and the HR or finance owner. Ask them to pause the affected decisions. Do not quietly fix and re-send, and do not guess the impact.
**First day:**
1. Find the exact scope: which records, which decisions, what has already gone out.
2. Correct the numbers and have a colleague check them.
3. Send a short note: what happened, who is affected, the corrected figures, what the decision owners should do.
4. Let HR and legal handle how affected individuals are told; I do not contact them myself.
**Follow-up (days to weeks):** Write a short root-cause note (for example, a lookup range was off by one row). Add a check (reconcile totals to the source, second-person review for anything affecting pay or hiring) and a test case. Share lessons with the team.
**What I would tell the stakeholder:** "I found an error in the pay-band lookup I built. Six of forty offers are affected. Here is the correct list. Nothing further goes out until you confirm. I will send the cause and prevention steps by Friday."

**Likely follow-ups:** 1) *Would you tell your manager before fixing?* Yes, first. 2) *What if no one noticed?* I would still report it; hiding it is worse.
**Common mistakes / traps:** Silent fix; defensiveness; vague "there was a small issue"; no prevention step.

### Q58 ⭐⭐ 🔴 Two stakeholders disagree about whether a pilot succeeded and each cites a different metric. You are asked to decide. What do you do?
**Asked at:** commonly asked (no company-specific report found); conflicting-metric scenarios appear in prep banks (unverified).
**What the interviewer is checking:** Whether you agree success criteria first, rather than choosing a winner to please someone.
**Say this in the interview:** "I would not pick a side. I would bring both to the original pilot goal and show each metric next to it."

**Clarify first:** What was the pilot's goal and success measure when it was approved? Was it written down? Who owns the decision it informs?
**Plan:**
1. Find the pilot charter or kickoff notes with the agreed target.
2. Define each stakeholder's metric precisely and check how it was computed.
3. Compare pilot with a control group, not before versus after only.
4. Show all metrics side by side, with sample sizes and uncertainty.
5. Run a short joint meeting to agree what counts as success.
**Method choice and why:** Simple pilot versus control comparison. Example (made-up): 200 people in each group; completion 62% in the pilot versus 55% in control, a gain of 7 percentage points (about 12.7% relative), or 124 versus 110 completers. One stakeholder may quote "12.7% better", the other "only 7 points", and both are the same fact. Whether it is "enough" depends on the target and cost.
**Pitfalls:** Choosing the metric after seeing the result; ignoring cost or side effects; small samples; pilot participants that were not typical.
**Deliverable:** A one-page summary: goal, each metric, the result against the target, confidence, and a recommendation (scale, extend or stop) with the decision owner named. The decision stays with the owner.

**Likely follow-ups:** 1) *No agreed target?* Say so, and propose one with both sides. 2) *Results mixed?* Recommend a longer or larger pilot.
**Common mistakes / traps:** Declaring a winner; hiding the disagreement; mixing relative and absolute change.

### Q59 ⭐⭐ 🔴 A stakeholder asks you for a regional breakdown that you know will look like a performance ranking of specific managers, and some of the groups are tiny. How do you handle it?
**Asked at:** commonly asked (no company-specific report found); minimum group size and privacy for HR data are noted in people-analytics guides (unverified).
**What the interviewer is checking:** Whether you spot fairness, privacy and small-number risks before delivering.
**Say this in the interview:** "I would clarify the decision, avoid a manager league table, and combine or hide tiny groups, with sign-off from HR."

**First, clarify / contain:** Ask what decision this serves. If the real aim is "where are the problem areas", a ranking of named managers is the wrong output. Do not build the manager-level view yet.
**What I would check, in order:**
1. Group sizes: how many people sit under each manager or region.
2. Whether the metric is affected by things the manager does not control (role mix, location, hiring season).
3. Whether the company has a minimum group size rule (commonly 5 to 10, assumed; confirm with HR or privacy).
4. Who would see the output and how it might be used.
**If I find...:** Small groups: a team of 4 where one person leaves shows 25% attrition, and a team of 120 with 30 leavers also shows 25%, yet the first is a single event. Combine small groups into larger ones, or show "fewer than 10" instead of a rate. Large groups: show regional results, with the factors that explain them. A true manager-performance review: that is an HR process, and I need explicit approval and method from HR leadership.
**What I would tell the stakeholder:** "I can give you a regional view that points to where to look. Manager-level percentages on teams of four are mostly noise and could be unfair, so I suggest we combine small teams. I would like HR to confirm this."
**Prevent it next time:** Put a minimum group size and a "no ranking of individuals" rule in the reporting guidelines.

**Likely follow-ups:** 1) *They insist?* Escalate to HR and the data owner. 2) *What about showing counts?* Counts of tiny groups can still identify people.
**Common mistakes / traps:** Delivering rates on groups of 3; ignoring context; being unhelpful instead of offering an alternative.

### Q60 ⭐⭐ 🔴 You are the only analyst and receive a flood of requests after a leadership change. How do you reorganise your intake, priorities and communication within a week?
**Asked at:** commonly asked (no company-specific report found); ad-hoc request triage is a common theme (unverified).
**What the interviewer is checking:** Structure under pressure: one intake route, visible priorities, and honest communication.
**Say this in the interview:** "I would put every request in one list, ask the new leader to rank the top few, and tell everyone else what will wait and when."

**First, clarify / contain:** Do not start the loudest request. Ask my manager who sets my priorities. Stop taking requests by chat; ask people to use one form or email.
**What I would check, in order:**
1. Day 1: list every open request: who, what decision, deadline, effort.
2. Day 2: group them into urgent with a real date, important, and nice to have.
3. Day 2 to 3: meet the new leader (15 minutes), ask for their top three, and agree the rest.
4. Day 3: split my 40-hour week (assumed): about 24 hours planned work, about 8 hours for ad hoc requests, about 8 hours for review and documentation.
5. Day 5: publish a short priority list with expected dates.
**If I find...:** Two requests conflict: ask the leader or my manager to decide, in writing. A request is a repeat: reuse earlier work. A request is bigger than it sounds: give a smaller first version.
**What I would tell the stakeholder:** "I am the only analyst and have 25 requests open. Here is the list with dates. Your item is third; the earliest slot is next Wednesday. If it is more urgent, tell me what to move."
**Prevent it next time:** Keep a standing request log, a weekly review of it with the manager, and a short intake form.

**Likely follow-ups:** 1) *Someone senior pushes in?* Show the trade-off and let my manager or the leader decide. 2) *Overtime?* Only as an agreed exception.
**Common mistakes / traps:** Saying yes to everyone; working silently late; never telling people about delays.

### Q61 ⭐ 🟢 What does "managing up" mean for a junior data analyst, and give two practical habits?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand that your manager's success is part of your job, and that you act without being chased.
**Say this in the interview:** "Managing up means making my manager's job easier: no surprises, clear information, and a clear ask."

**Explain simply:**
- Managing up does not mean flattering the boss. It means working out what they need and giving it in a form they can use.
- Habit 1: No surprises. Send a short weekly update (done, next, blocked) and raise problems early, with a proposed fix.
- Habit 2: Bring options, not only questions. "I have two ways: A is faster, B is more accurate. I suggest A because the deadline is Friday. Okay?"
**Worked mini-example:** Report due Friday, data arrives Thursday. On Monday I tell my manager: "Data is late; I will build with last month's data and swap in the new file; I may need a day if it breaks." That is managing up.
**Practice step:** For one week, send a 3-line Friday update and note whether your manager's questions go down.

**Likely follow-ups:** 1) *How often do you update?* Weekly by default; same day for risks. 2) *What if your manager is too busy?* Make updates short and put the ask first.
**Common mistakes / traps:** Saying only "all good"; hiding problems until the deadline; showing up with problems and no options.

### Q62 ⭐ 🟢 How do you ask a stakeholder for feedback on your reports, and what do you do with it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you seek feedback in a useful way and act on it.
**Say this in the interview:** "I ask specific questions, soon after delivery, write down the answers, and tell people what changed."

**Explain simply:**
- Ask specific questions, not "was it good?": What did you do with it? Which part did you skip? What is missing? Was anything confusing?
- Ask at a natural time: two minutes at the end of a review meeting, or a short message a week after delivery.
- Make it easy: two or three questions, a choice of answers, or a quick call.
**What I do with it:** Log every comment; sort into quick fixes (do now), changes that need a decision, and requests I will not do (with a reason). Tell the stakeholder what I changed ("You said the table was too long; I moved details to page 2"). Look for patterns across people.
**Worked mini-example:** Three managers say the attrition report is "too busy". I cut it to one page, usage goes up, and the next review asks for one detail, which I put on a drill-through page.
**Practice step:** After your next report, ask: "What is the one thing you would change?"

**Likely follow-ups:** 1) *What if feedback conflicts?* Ask who uses it for which decision. 2) *What if the feedback is harsh?* Ask for an example and treat it as information.
**Common mistakes / traps:** Asking only "is it fine?"; collecting feedback and never acting; taking it personally.

### Q63 ⭐ 🟡 A stakeholder always asks for last-minute changes during their review meeting. How do you reduce the friction over time?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Process thinking: moving the discussion earlier rather than just absorbing the pain.
**Say this in the interview:** "I would find out why changes appear in the meeting, and move that thinking earlier with a draft preview and a clear list of what can change on the spot."

**First, clarify / contain:** In the meeting, note every change and say which ones I can do live and which need a day. Do not promise everything. Afterwards ask the stakeholder privately what makes them see it only in the meeting.
**What I would check, in order:**
1. Whether the stakeholder sees the report for the first time in the meeting.
2. Which types of change repeat (colour, filters, a new cut, a new metric).
3. Whether the original request was unclear.
4. Which changes could be self-service (a slicer, a filter, a parameter).
**If I find...:** They see it too late: send a draft 1 to 2 days ahead with 3 review questions. Changes repeat: build them in. They are new requests: log them as phase 2 with a date.
**What I would tell the stakeholder:** "To make the meeting more productive, I will send a draft on Tuesday. If you can send comments by Wednesday noon, the final version will be ready on Thursday. Anything new in the meeting goes on a follow-up list."
**Prevent it next time:** Wireframe sign-off before building, and a short change log per report.

**Likely follow-ups:** 1) *What if it still happens?* Time-box live changes and raise the pattern with their manager if it affects delivery. 2) *Is it always bad?* No, it is information about what they need.
**Common mistakes / traps:** Silent frustration; refusing all changes; making changes live without checking numbers.

### Q64 ⭐ 🟡 How do you document a stakeholder's request so that a colleague can pick it up if you are on leave?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you work in a way others can take over.
**Say this in the interview:** "I keep one page per request: who, why, what, definitions, data source, status and where the files are, so a colleague can continue without calling me."

**Explain simply:** A good request record answers: what was asked, why, and by when, without needing me.
**Fields (one row or page per request):**
- Requester, date, decision the work supports, deadline.
- Exact ask in their words, and my restated version they agreed to.
- Definitions (for example, "attrition = leavers in the month divided by average headcount").
- Data sources and refresh method, file locations.
- Assumptions and known issues.
- Status, next step, open questions, what was already sent to whom.
- Contacts: who to ask for which question.
**Worked mini-example:** "R-014, Priya (HR head), monthly attrition by department, due the 5th. Source: HRIS export, tab Leavers. Excluded: contractors (agreed 3 Nov). Status: draft sent; waiting on her comment on the layout. Next: update on 5th."
**Practice step:** Ask a friend to read one of your records and tell you what they cannot understand.

**Likely follow-ups:** 1) *Where do you keep it?* A shared tracker or wiki, not my own drive. 2) *How detailed?* Enough to repeat the work.
**Common mistakes / traps:** Notes only in your head or chat; no definitions; files named "final_v3".

### Q65 ⭐ 🟡 A stakeholder asks you to attend a call where they present your numbers. You think they will overstate them. What do you do beforehand, and during the call?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Courage to protect accuracy without embarrassing the stakeholder.
**Say this in the interview:** "I would agree the message beforehand, give them a one-line caveat to say, and during the call, restate the limits politely if needed."

**First, clarify / contain:** Ask what they plan to say and which numbers they will quote. Do not wait for the call to find out.
**What I would check, in order:**
1. Which claims go beyond the data (for example, a cause stated for a correlation).
2. Whether the figures are final or provisional.
3. What the safest wording is.
4. What the audience will probably ask.
**If I find...:** Small stretch: suggest softer wording ("associated with" rather than "caused"). Large stretch: raise it with the stakeholder privately and, if needed, my manager. During the call: if a figure is wrong, say calmly, "One clarification so we are accurate: that figure is a provisional estimate based on X."
**What I would tell the stakeholder:** "I will send a half-page note with the three numbers and one-line caveats. If you quote them as written, we are safe. Can we spend 10 minutes before the call?"
**Prevent it next time:** Put caveats on the slide itself, and send a short "how to use these numbers" note with every deliverable.

**Likely follow-ups:** 1) *They ignore you?* Correct gently in the call, then follow up in writing. 2) *Should you stay quiet to avoid conflict?* No; the numbers have my name behind them.
**Common mistakes / traps:** Silence; public correction with a harsh tone; skipping the prep.

### Q66 ⭐ 🟡 How do you build trust with a stakeholder who has been burnt before by bad data from another team?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Patience and practical steps to rebuild confidence.
**Say this in the interview:** "I would listen to what went wrong, start small, show my checks, and deliver exactly what I promised."

**Explain simply:** Trust grows from small, visible, repeated reliability.
- Ask what happened before and what would make them confident now.
- Start with a small request I can do correctly.
- Show the checks: totals match the source, with the reconciliation in one line.
- Say what I do not know; do not oversell.
- Keep promises on dates; if I will be late, say so early.
- Make errors visible: if I find one, tell them first.
**Worked mini-example:** Headcount from HRIS is 1,240 and finance says 1,236. I show the 4-person difference with the reason (4 joiners starting on the 31st) rather than hoping nobody asks. (Made-up numbers.)
**Practice step:** Add a "checks done" box to your next report, with three items.

**Likely follow-ups:** 1) *How long does it take?* Several months of consistency; no shortcut. 2) *What if they distrust the other team's data you rely on?* Show the source and reconcile it.
**Common mistakes / traps:** Defending your team too quickly; overpromising; skipping reconciliation.

### Q67 ⭐ 🟡 A request is clearly valuable but sits outside your team's remit (for example, it needs data engineering time). How do you route it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you route and advocate through the right channels instead of saying no or doing it informally.
**Say this in the interview:** "I would write a short business case, send it to the right team's intake with my manager's support, and give the requester an interim option."

**First, clarify / contain:** Confirm the real need and its value. Do not start informal work that creates a fragile process or promises I cannot keep.
**What I would check, in order:**
1. Value: what decision or cost does it affect, and how big.
2. Which team owns it (data engineering, IT, vendor) and how they take requests.
3. Whether a manual or partial version can work in the meantime.
4. Dependencies and a rough effort.
**If I find...:** High value: write a one-page case (problem, impact, ask, deadline) and get my manager to sponsor it. Low value: park it on the backlog with a review date. An interim exists: do a manual version with clear limits.
**What I would tell the stakeholder:** "This is valuable but needs data engineering, who own the pipeline. I have sent them the request with the impact, and I will update you on Friday with their timeline. Meanwhile I can give you a manual version for this month."
**Prevent it next time:** Agree a monthly cross-team prioritisation meeting and a shared request board.

**Likely follow-ups:** 1) *What if the other team refuses?* Escalate through managers with the value case. 2) *Do you do it yourself?* Only if it is safe, supported and documented.
**Common mistakes / traps:** Quietly building a workaround that breaks; just saying "not my job"; no follow-up.

### Q68 ⭐ 🟡 A stakeholder challenges you: "Why should I trust your numbers over my gut feeling?" How do you answer?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Respect for experience combined with evidence, without arrogance.
**Say this in the interview:** "Your experience is a great starting point, so let me show where the data agrees and where it does not, and how sure I am."

**First, clarify / contain:** Do not get defensive. Ask what their gut says and why; it may point to something the data missed.
**What I would check, in order:**
1. State their hypothesis as a test I can run.
2. Check my data for gaps that could explain a difference (missing period, definitions).
3. Show the evidence: source, method and sample size.
4. Identify what each of us is better at.
**If I find...:** Data agrees with them: say so, and quantify it. Data disagrees: show it, with uncertainty, and suggest a small test. Data is thin: say "I cannot tell yet; here is what would settle it."
**What I would tell the stakeholder:** "Your instinct may be right, and I would like to test it. Here is what the numbers show, how I checked them, and what I am not sure about. Where we differ, I suggest a small trial for two weeks."
**Prevent it next time:** Share the method and checks in every report, and keep a record of cases where either side was right.

**Likely follow-ups:** 1) *What if gut is right and data is wrong?* Then I fix the data and learn from it. 2) *Isn't data always better?* No; it is better when it is clean and relevant.
**Common mistakes / traps:** "The data says so, end of story"; hiding uncertainty; mocking experience.

### Q69 ⭐ 🟡 How do you tailor the same finding for three audiences: an executive, a functional manager and a fellow analyst?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Audience awareness.
**Say this in the interview:** "Same fact, three depths: the decision for the executive, the actions for the manager, the method for the analyst."

**Explain simply:** Take one finding: monthly attrition in the support team rose from 2% to 3%, an increase of 1 percentage point.
- Executive (30 seconds): "Attrition in support is up 1 point to 3%, which is about 50% higher than before. Recommended: approve a retention review. Cost of inaction: replacing leavers." They need the decision and the size.
- Functional manager (5 minutes): Which teams, how many people, what changed (for example, more leavers in the first year), and 2 or 3 actions to try. They need what to do on Monday.
- Fellow analyst (full detail): Definition of attrition, data source, filters, test or confidence, caveats, code, and where to find the query. They need to reproduce it.
**Check the maths:** 3% against 2% is 1 percentage point, or 50% relative.
**Practice step:** Write the finding in one sentence for each audience and check each fits in the time.

**Likely follow-ups:** 1) *What if an executive asks for detail?* Have a backup slide ready. 2) *Same numbers for all?* Yes; the depth changes, never the facts.
**Common mistakes / traps:** Sending the analyst's version to the executive; leaving out the "so what".

### Q70 ⭐ 🟡 Role-play: a stakeholder says only, "Revenue looks off." What are your first three replies, in order?
**Asked at:** commonly asked (no company-specific report found); vague-ask role-plays appear in prep banks (unverified).
**What the interviewer is checking:** Whether you ask calm, specific questions before touching data.
**Say this in the interview:** "I would acknowledge, narrow it down, and set a time for an answer. I would not start digging blindly."

**Reply 1 (acknowledge and narrow):** "Thanks for flagging. What made it look off: a number you expected, a drop in a chart, or a mismatch with another report? Can you send me the report name and the figure?"
**Reply 2 (compare):** "What did you expect to see, and where does that expectation come from (last month, another system, a forecast)? Which period, region or product looks off?"
**Reply 3 (commit):** "I will check whether it is a data issue (a missing load, a duplicate, a changed definition) or a real change, and update you by 3 pm today with what I know and do not know."
**Behind the replies:** I then check in order: refresh time of the data, row counts against yesterday, filters and currency or date settings, and a reconciliation to the source system.
**Practice step:** Write your own three replies for "Attrition looks high."

**Likely follow-ups:** 1) *What if they will not explain?* Run the quick checks anyway, and report what I found. 2) *And if it is a real change?* Break it down by segment and explain the drivers.
**Common mistakes / traps:** Replying "I will look" and nothing else; changing numbers before finding the cause; blaming the data team publicly.

### Q71 ⭐ 🟡 What are the warning signs that a stakeholder request is really a political request rather than an analytical one, and how do you respond?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of office politics, handled professionally.
**Say this in the interview:** "If the conclusion is decided before the question, I stay neutral, document the method, and bring in my manager."

**Explain simply:** Warning signs:
- The answer is stated in the request ("show that the new process worked").
- They ask for specific people or teams to be highlighted or excluded.
- They push to change the metric definition or time window after seeing results.
- They want numbers by a tight deadline for a meeting where something is being decided about people.
- They ask to avoid sharing it with others who would normally see it.
**How I respond:** Rephrase as a neutral question ("Let me check whether the new process improved outcomes, and by how much"); agree the method and metric in writing before running it; run the analysis the same way whatever the result; share the same output with all who should see it; and tell my manager if I am being pushed.
**Worked mini-example:** "Prove sales region X performs best" becomes "compare all regions on revenue per rep, using last four quarters."
**Practice step:** Look at your last three requests and mark any that had an answer baked in.

**Likely follow-ups:** 1) *Is politics always bad?* No; context matters, but my method must stay neutral. 2) *What if they insist?* Escalate.
**Common mistakes / traps:** Assuming bad intent without evidence; going along silently; getting drawn into taking sides.

### Q72 ⭐ 🟡 What are the common mistakes junior analysts make when responding to a vague request, and how would you avoid each?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Self-awareness about typical junior errors.
**Say this in the interview:** "The big ones are starting without clarifying, guessing silently, and delivering something nobody checked against the need."

**Explain simply:**
1. Starting the query straight away. Fix: ask what decision it supports and by when.
2. Guessing definitions silently (for example, what counts as "active employee"). Fix: write the definition and get it confirmed.
3. Asking too many questions at once and annoying the stakeholder. Fix: ask the top 3, and propose assumptions they can just approve.
4. Delivering too much. Fix: give the answer first, detail after.
5. Not restating the request. Fix: send a two-line summary "I understand you need X by Y; correct?"
6. Saying yes to an impossible deadline. Fix: give a smaller first version with a date.
7. Never checking in during work. Fix: share a rough draft early.
8. No documentation. Fix: keep a request log.
**Practice step:** Take one vague request and write the 3 questions and the restated summary.

**Likely follow-ups:** 1) *What if they say "just do it"?* State my assumptions in the deliverable. 2) *What if I cannot reach them?* Choose the most likely reading, label it clearly and ask for confirmation.
**Common mistakes / traps:** Perfecting the wrong output; hiding confusion out of fear of looking junior.

### Q73 ⭐ 🟡 You are asked for a headcount and attrition report for a client under offshore-delivery rules: a fixed template, a fixed turnaround and no direct contact with the end user. How do you protect quality when you cannot ask questions directly?
**Asked at:** commonly asked (no company-specific report found); offshore-delivery constraints are described from general knowledge (unverified).
**What the interviewer is checking:** Whether you build quality into the process when you cannot clarify directly.
**Say this in the interview:** "I would write down my assumptions, validate against totals I can check, and ask questions through the proper channel in one consolidated list."

**Clarify first:** Through the permitted channel (the client lead or onshore coordinator), send one batch of questions: definitions of headcount and attrition, period, treatment of contractors and transfers, and the data source. Ask early, because answers take time.
**Plan:**
1. Read the template and any past reports: they reveal definitions.
2. Write a short assumptions list (for example, headcount at month end; attrition = leavers divided by average headcount).
3. Clean data: remove duplicates, check dates, check missing departments.
4. Reconcile: opening headcount plus joiners minus leavers equals closing headcount.
5. Compare with last period; investigate large swings.
6. A second person reviews with a checklist.
7. Deliver in the fixed template, with an assumptions and checks sheet attached.
**Method choice and why:** Keep it standard, so it fits the template. Illustration (made-up): 1,000 opening, 40 joiners, 30 leavers gives 1,010 closing; leavers divided by average headcount (1,005) is 2.99%, about 3.0% (computed).
**Pitfalls:** Silent assumptions; wrong period; template locks hiding errors; missing the deadline due to waiting for answers.
**Deliverable:** The completed template plus a half-page of assumptions, open questions and checks, in writing.

**Likely follow-ups:** 1) *No reply by the deadline?* Deliver using my stated assumption, flagged clearly. 2) *Personal data in the file?* Follow the client's handling rules.
**Common mistakes / traps:** Guessing silently; skipping reconciliation; changing the template.

### Q74 ⭐ 🔴 A department head asks you to produce an attrition analysis that quietly excludes a recent round of layoffs, "to keep the trend clean". How do you respond?
**Asked at:** commonly asked (no company-specific report found); ethics-of-exclusion is a judgement gap-fill rather than a sourced company question.
**What the interviewer is checking:** Integrity: whether you refuse to hide data but find a legitimate way to meet the real need.
**Say this in the interview:** "I would not quietly exclude them. I would show the trend with and without layoffs, label both clearly, and let the audience see the difference."

**First, clarify / contain:** Ask what they want to understand: voluntary attrition, which is a valid and common cut, or a hidden picture. Do not remove the rows silently.
**What I would check, in order:**
1. How leavers are coded (layoff versus resignation), and whether the code is reliable.
2. The size of the layoff effect.
3. Whether the company has a standard attrition definition.
4. Who will read the report and whether the exclusion would mislead them.
**If I find...:** Illustration (made-up): average headcount 1,000, 90 resignations and 60 layoffs. Voluntary attrition is 9.0%; total attrition is 15.0%; layoffs add 6.0 percentage points. So excluding layoffs changes the story a lot. Reporting both is fine: "voluntary attrition 9.0% (excludes 60 layoffs); total 15.0%". Reporting only the 9.0% as "attrition" is misleading.
**What I would tell the stakeholder:** "I can show voluntary attrition for trend purposes, and it is a normal cut. I need to show total attrition next to it with a clear label, because leaving the layoffs out silently would mislead people. Would that work?"
**Prevent it next time:** Define attrition types (voluntary, involuntary, total) in a metric dictionary and use them every time.

**Likely follow-ups:** 1) *They still say no?* Escalate to my manager and HR leadership; I do not publish a misleading figure. 2) *Is excluding ever fine?* Yes, if it is declared and the full number is available.
**Common mistakes / traps:** Quietly complying; refusing without offering the voluntary cut; mixing definitions between periods.

### Q75 ⭐ 🔴 You suspect a stakeholder has been cherry-picking your outputs across several decks to build a misleading story. How do you handle it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Evidence over suspicion, and a calm, professional way to protect accuracy.
**Say this in the interview:** "I would first confirm the pattern with evidence, then talk to the stakeholder directly, and make my outputs harder to misuse."

**First, clarify / contain:** Do not accuse. Collect the examples: which slides, which numbers, what I originally said versus what is shown. It may be innocent (they only saw part of my output).
**What I would check, in order:**
1. Compare each use with my original caveats and context.
2. Look for a pattern (always dropping the same caveat or period).
3. Check whether the story changes the decision.
4. Ask who else has seen the decks.
**If I find...:** Innocent selection: add clearer headlines and caveats. A repeated pattern with a real decision effect: talk to them first, then my manager if it continues.
**What I would tell the stakeholder:** "I noticed the last three decks use the March figure without the full-year trend. I worry the picture is incomplete. Can we agree that the trend chart goes with it? I can prepare a one-slide version."
**Prevent it next time:** Put a headline, caveat and "use with" note on each output; share the whole analysis in a common place; offer to review decks that use my numbers.

**Likely follow-ups:** 1) *Do you go over their head?* Only after speaking to them and if the misuse continues and matters. 2) *What if you are wrong?* Then the conversation costs little.
**Common mistakes / traps:** Accusing without evidence; saying nothing; gossiping.

### Q76 ⭐ 🔴 The same stakeholder sends you urgent requests every week and your other work is suffering. How do you address the pattern, not just the single request?
**Asked at:** commonly asked (no company-specific report found); ad-hoc load arithmetic is a judgement gap-fill.
**What the interviewer is checking:** Pattern thinking: addressing the root cause rather than just coping.
**Say this in the interview:** "I would measure the load, show the stakeholder the data, and agree a standing slot or a self-service fix."

**First, clarify / contain:** Handle this week's request on its merits. Then look at the pattern with numbers.
**What I would check, in order:**
1. Log the last 4 to 6 weeks of their requests: topic, hours, real deadline.
2. Illustration (made-up): 12 hours a week of a 40-hour week is 30%, or 48 hours in four weeks, leaving 28 hours (70%) for everything else.
3. Which requests repeat and could be automated.
4. Why they are always urgent (late planning, their own deadlines, habit).
**If I find...:** Repeats: build a recurring report or dashboard. Late planning: agree a weekly planning call and a "request by Tuesday for Friday" rule. Truly urgent: reserve a fixed ad hoc slot (for example, 4 hours a week).
**What I would tell the stakeholder:** "Your requests have taken about 30% of my time over the last four weeks, which has delayed two other projects. I would like to set a weekly 30-minute planning slot and automate the three reports you ask for often. Urgent items would still be possible within an agreed slot."
**Prevent it next time:** Standard intake, a visible priority list, and a manager who agrees the split.

**Likely follow-ups:** 1) *They ignore it?* Escalate with the data to my manager. 2) *Is it personal?* No, I treat it as a process.
**Common mistakes / traps:** Silent resentment; refusing everything; arguing without numbers.

### Q77 ⭐ 🔴 You join a company where nobody can say who owns the main revenue number and each team reports its own. How do you approach your first stakeholder requests?
**Asked at:** commonly asked (no company-specific report found); ownerless-metric onboarding is a judgement gap-fill.
**What the interviewer is checking:** Whether you reconcile definitions first and do not add a fifth version of the number.
**Say this in the interview:** "I would not add another number. I would list each team's definition, show where they differ, and propose an owner."

**First, clarify / contain:** For my first requests, state which version I use and why. Do not call any version the truth yet, and do not criticise teams.
**What I would check, in order:**
1. Collect each team's number, definition, source system and refresh timing.
2. Reconcile: gross versus net of returns, booking date versus invoice date, currency, tax, cut-off time.
3. Bridge the numbers in one table (for example, Sales 100, minus returns 4, minus tax 8 gives Finance 88; illustrative).
4. Find the system closest to the money (usually the ledger, from memory, unverified) as a candidate source.
**If I find...:** Differences are explained: write down the definitions and name each (for example, "booked revenue", "recognised revenue"). Differences are unexplained: pause and investigate with both teams.
**What I would tell the stakeholder:** "There are four revenue numbers, each correct under its own definition. I have a one-page bridge. For this request I used finance's recognised revenue and labelled it. I suggest we name one owner for the official definition."
**Prevent it next time:** A metric dictionary with owner, definition, source and a change log; ask leadership to name the owner.

**Likely follow-ups:** 1) *Who should own it?* Usually finance for money numbers, but leadership decides. 2) *What if teams resist?* Show the bridge so no one feels blamed.
**Common mistakes / traps:** Picking a number quietly; blaming a team; building a new version.

### Q78 ⭐ 🔴 A stakeholder asks you to turn a rough analysis into an executive recommendation overnight, and you are not confident in the numbers. How do you handle the recommendation?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you refuse to overstate confidence, but still deliver something useful.
**Say this in the interview:** "I would give a clearly labelled preliminary recommendation with the confidence level and the checks still needed, not a firm one."

**First, clarify / contain:** Find out what decision is made tomorrow and what happens if it is wrong. Do not hide my doubts, and do not present rough numbers as final.
**What I would check, in order:**
1. Which numbers I am least sure about, and why.
2. Quick checks: totals against source, a second method, spot-check sample rows.
3. Whether the direction holds even if the exact figures change.
4. Whether the decision is easy to reverse.
**If I find...:** Direction is robust: recommend with a range and caveats. Direction depends on shaky numbers: say "not enough to decide; here is what would settle it, and by when". Decision is hard to reverse: ask for more time.
**What I would tell the stakeholder:** "Preliminary: the data points toward option A, with moderate confidence. The estimate could move by about 10 to 15 percent (assumed range) because of X. I have not yet verified Y. I recommend a decision on Friday after the check, or a reversible first step now."
**Prevent it next time:** Ask for decision deadlines early, keep a standard "confidence and caveats" box on every recommendation.

**Likely follow-ups:** 1) *They want a firm answer?* Offer the options and risks, and let them decide knowingly. 2) *Would you refuse?* I would not refuse; I would label.
**Common mistakes / traps:** Bluffing; delivering a long hedge with no recommendation; staying up all night to hide the problem.

### Q79 ⭐ 🔴 Design a lightweight intake process (form, triage rules and service levels) for a small analytics team that currently gets requests by chat and email.
**Asked at:** commonly asked (no company-specific report found); intake design is a judgement gap-fill.
**What the interviewer is checking:** Practical design: simple enough to be used, firm enough to help.
**Say this in the interview:** "One short form, a weekly triage, three priority levels with clear response times, and a visible board."

**Clarify first:** How many requests per week, who sends them, how many analysts, and what hurts most (lost requests, shifting priorities, no visibility). The goal is to reduce chaos, not to add bureaucracy.
**Plan:**
1. Form (5 fields, 2 minutes): what you need; what decision it supports; deadline and why it is fixed; who the audience is; data or past reports you know of.
2. One front door: a form link pinned in chat and an auto-reply to emails. Anything arriving elsewhere is redirected politely.
3. Triage rules, done twice a week by the team lead: P1 urgent with a real, dated business impact (response same day, assumed); P2 important (within 3 working days); P3 nice to have (backlog, reviewed monthly).
4. Reserve capacity: for example, about 20% of time for ad hoc requests (8 of 40 hours, assumed).
5. Visible board with statuses: New, Accepted, In progress, Review, Done, Declined (with reason).
6. Close the loop: confirmation within 1 working day, update when dates slip, a 2-question feedback note on completion.
**Method choice and why:** A spreadsheet or shared form with a board is enough to start. Move to a ticket tool only if volume grows.
**Pitfalls:** Too many form fields; no one owns triage; "urgent" overused; no feedback.
**Deliverable:** The form, a one-page triage guide, the board, and a monthly metric (volume, time to first response, time to complete).

**Likely follow-ups:** 1) *Senior people bypass it?* Ask my manager to make the form the standard and log their requests for them. 2) *How to measure success?* Fewer lost requests and shorter time to first response.
**Common mistakes / traps:** Over-engineering; no service levels; no exceptions policy.

