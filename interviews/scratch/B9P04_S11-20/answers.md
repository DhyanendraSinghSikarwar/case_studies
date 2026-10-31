### S11 ⭐⭐⭐ 🟡 Stakeholder conflict: two senior stakeholders each say the other agreed to a different dashboard
**Asked at:** Conflicting stakeholder priorities appear in codemia.io 'conflicting priorities with a teammate or stakeholder' pages (crowd-sourced; snippet only) and Book 9 Part 2 Q32 covers a two-team version; the two-directors framing is editor-designed; search snippets only, not opened
**Situation:** One director wants the dashboard split by region and another wants it by product line. Each tells you separately that the other is on board. You have one week and one set of data.
**Weak response:** Quietly build the region view for the director you spoke to last, hoping the other one does not notice, or tell each director what they want to hear. Either way the clash arrives at the review, with you in the middle.

**Strong response:** Do not decide between them and do not carry messages between them. Check what each actually said, then get both into one short conversation, or write one shared note, with a single question: what decision will this dashboard support? Often region and product line answer different decisions, and a filter or a second tab can serve both. Bring a cheap option: a one-page mock-up showing both cuts from the same data, so the debate is about something visible. If they still disagree, ask your manager or the dashboard's sponsor to set the priority, and say what each choice costs in the one week you have. Do this only with what you really know: say "each of you mentioned the other was fine with it" rather than claiming either lied.

**Why it works:** It treats the conflict as a decision-clarity problem, not a loyalty test. It keeps you neutral, protects the week, and puts the choice with the person who owns it. See Book 9 Part 2 Q32 for the two-team version of this move.

**What the interviewer scores:** Whether you avoid triangulating, name the underlying decision, bring a concrete option, escalate the priority call without blame, and protect the timeline.

**Say it like this:**
```
"I've heard two slightly different requests, and each of you mentioned the other was fine with it, so I think we've missed a conversation. Could we take fifteen minutes together? I'd like to start with the decision this dashboard supports. I'll bring a mock-up showing both region and product line from the same data, so we can see whether one page covers you both. If we still need to choose, I'd like [sponsor] to set the order, and I'll tell you honestly what each option costs in this week."
```

**If they push back:** "Just build mine, I'll sort out the other director." Say you are happy to start, but a build that one director has not seen risks a rework in week two, so you want both to see the mock-up first; offer a short checkpoint rather than a refusal. If told to pick, say that the priority is the sponsor's call and you will follow it once it is written down.

**Common mistakes:** Playing messenger between the two. Deciding by seniority or by who spoke last. Accusing someone of misrepresenting the other. Overbuilding a dual-view dashboard in a week without agreeing scope. Giving an answer with no mock-up or option, only a complaint.

### S12 ⭐⭐⭐ 🟡 Ambiguity: a dataset arrives with no data dictionary and a deadline tomorrow
**Asked at:** Ambiguity is described as the harder behavioural category for data-science roles in a Towards Data Science snippet; Yardstick's data-scientist ambiguity page lists follow-ups on prioritising with unclear requirements; the missing-dictionary case is editor-designed; search snippets only, not opened
**Situation:** A partner team sends a table with forty columns, cryptic names and no documentation. The person who built it is on leave. You are asked for a first look by tomorrow afternoon.
**Weak response:** Guess what the columns mean, run a quick model or summary, and present it as if the meanings were known. Or reply that you cannot start without the dictionary.

**Strong response:** Aim for a labelled first look, not a finished answer. Spend the first hour profiling: types, missing values, distinct counts, ranges, duplicates, and how the columns relate. Write a "what I think each column is" table with a confidence level beside each guess. Then send three or four sharp questions to the partner team and to anyone who used the table before (a colleague, the pipeline code, a sibling table). Reading the code that produced the table often answers more than people expect. Deliver tomorrow with the guesses and the open questions at the top, and say which findings depend on an unconfirmed column. Never present an inferred meaning as fact.

**Why it works:** It delivers something useful on time while being honest about uncertainty. The confidence-tagged table lets the reader see exactly what to trust and gives the owner something quick to confirm.

**What the interviewer scores:** Comfort starting with ambiguity, a systematic profiling habit, asking targeted questions rather than "please explain everything", and honest labelling of assumptions.

**Say it like this:**
```
"Here is the first look you asked for. Before the findings, two things. First, there is no data dictionary, so this table lists what I believe each column means and how confident I am; the columns marked low are guesses from names and value patterns. Second, I've sent four questions to the partner team, and two findings change if my reading of the status column is wrong. I'd treat today's numbers as directional until those are confirmed."
```

**If they push back:** "Why not just wait until the builder is back?" Say the deadline matters, so you can give a clearly labelled first look now and update it when answers arrive. If asked to drop the caveats, keep them short but keep them; a wrong confident number costs more than one line of honesty.

**Common mistakes:** Presenting guesses as facts. Asking forty vague questions. Ignoring the code or other tables that could explain the columns. Spending the whole day exploring with nothing to send. Staying silent about the risk until the deadline.

### S13 ⭐⭐⭐ 🟡 Ambiguity: requirements change for the third time in two weeks
**Asked at:** Shifting requirements and managing expectations during a pivot appear in Yardstick's ambiguity follow-ups for data scientists (snippet); Book 9 Part 1 Q10 covers the story version; the three-change framing is editor-designed; search snippets only, not opened
**Situation:** A stakeholder first wanted a churn report, then a churn model, and now a customer-health score with a different definition. Each change came in a short message with no discussion. Your sprint is half gone.
**Weak response:** Keep saying yes and quietly restart each time, then miss the sprint and explain afterwards. Or complain that the stakeholder keeps changing their mind.

**Strong response:** Stop and ask for a short conversation, not another message. Play back the three asks and what each would change, then ask what decision the stakeholder is trying to make; the real need often sits under all three. Show the cost honestly: work done so far, what carries over (data prep, definitions), and what would be dropped. Propose a written one-page scope with the decision, the definition of "customer health", and a rule that changes after sign-off are traded against something else. Offer a smaller first deliverable that serves the likely need, and tell your manager so they are not surprised by the sprint.

**Why it works:** It turns three silent pivots into one explicit trade-off, keeps the stakeholder's goal at the centre, and gives them a way to change their mind that costs something visible. For the story version see Book 9 Part 1 Q10; for the data-science version with numbers see Book 6 Part 6 Q26.

**What the interviewer scores:** Calm under shifting scope, asking for the underlying decision, quantifying the cost of change without blame, and keeping your manager informed.

**Say it like this:**
```
"I want to make sure I build the right thing. In two weeks we've moved from a churn report to a model to a health score. Could we spend twenty minutes on the decision this supports? Here is what carries over from my work so far and what would be dropped. I'd suggest a one-page definition of customer health that we both sign, and a small first version this sprint. After that, a change is welcome, and we agree what moves out to make room."
```

**If they push back:** "It's just a small tweak." Agree that it may be, then show the effect on the plan in one line and ask for the priority. If they say the definition is still unclear, offer a time-boxed first version with the definition marked provisional.

**Common mistakes:** Silently absorbing every change. Blaming the stakeholder. Refusing to work until everything is final. Hiding the sprint risk from your manager. Building a model before the definition is agreed.

### S14 ⭐⭐⭐ 🟡 Failure and ownership: you find a filter bug in a dashboard the vice president saw yesterday
**Asked at:** Own-your-error prompts are a staple of data-science behavioural lists (resumegeni.com and codemia.io pages in the results; Book 9 Part 1 Q7 covers the story form); the dashboard framing is editor-designed; search snippets only, not opened
**Situation:** While checking something unrelated you discover that a date filter has been dropping a week of data. A vice president used the dashboard in a meeting yesterday. Nobody has noticed.
**Weak response:** Quietly fix the filter and hope nobody compares yesterday's numbers to today's. Or wait until you are sure of every detail before saying anything.

**Strong response:** First confirm the bug: reproduce it and measure how much the missing week changes the figures the vice president saw. Then tell your manager today, before the fix goes out, with facts: what was wrong, what the corrected numbers show, which decisions or slides used the old numbers, and when you can have the fix live. Agree who tells the vice president and send a short, plain correction. Fix the filter, add a check so a dropped period triggers an alert, and note what you changed. Do not speculate about the cause of the bug or blame the person who built it; stick to what you verified.

**Why it works:** Speed and plainness are what rebuild trust: the people relying on the numbers learn it from you, with the size of the impact and the repair. Book 9 Part 1 Q7 covers telling this as a story afterwards.

**What the interviewer scores:** Ownership without drama, quantifying impact before escalating, communicating up quickly, and preventing a repeat.

**Say it like this:**
```
"I found a problem in the dashboard from yesterday's meeting. A date filter was dropping one week of data. I've reproduced it and re-run the figures: [the headline metric] moves from [old value] to [new value], and the trend direction [does / does not] change. I'd like to send a short correction to the vice president today, and the fix will be live by [time]. I'm also adding a check so a missing period is flagged automatically."
```

**If they push back:** "Is it really worth raising? The change is small." Say that even small changes should be disclosed, because the vice president may have quoted the figure; let the manager decide how formal the note is. If asked who is to blame, say you are focused on the impact and the fix, and the review can look at the process afterwards.

**Common mistakes:** Silent fixing. Waiting days to be sure. Reporting the bug without an impact number. Blaming a colleague. Skipping the preventive check.

### S15 ⭐⭐⭐ 🟡 Communication: a CXO asks in a meeting why last week's metric dropped and you do not know yet
**Asked at:** Explaining a metric change to a senior audience is a roadmap item in the plan's communication scenarios; no public page found for this in-the-room framing, editor-designed; Book 9 Part 2 Q17 covers being told you are wrong; search snippets only, not opened
**Situation:** Mid-meeting the CXO points to a dip in a model metric and asks for the reason. You have seen the dip but have not diagnosed it. Several people look at you.
**Weak response:** Invent a plausible cause on the spot, such as "probably seasonality" or "data drift", to fill the silence. Or say "I don't know" and stop there.

**Strong response:** Be brief and honest, then show a plan. Confirm what you can: the size and timing of the dip, and that you have seen it. Say you have not diagnosed it. Offer two or three hypotheses as hypotheses, such as a data or pipeline change, a shift in the input mix or a real change in behaviour, and the first check for each. Commit to a time for an update and an owner, you. If a quick check can be done in the room (was there a deploy that week?), say so and do it after the meeting. Avoid blame and avoid certainty you do not have.

**Why it works:** Senior people usually value a calibrated "not yet, here is how I will find out and when" over a confident wrong story. It keeps the meeting moving and your credibility intact. Book 9 Part 2 Q17 covers staying steady when a leader challenges your analysis.

**What the interviewer scores:** Honesty, structured thinking under pressure, labelling guesses as guesses, and a committed follow-up time.

**Say it like this:**
```
"I've seen the dip and I haven't diagnosed it yet, so I don't want to guess. The three things I'd check first are whether any data or pipeline change landed that week, whether the mix of inputs shifted, and whether the model's behaviour actually changed. I can tell you which it is by [time tomorrow], and I'll send a short note either way."
```

**If they push back:** "Give me your best guess now." Offer the most likely hypothesis clearly labelled as unconfirmed, and say what would confirm or rule it out. Do not let a guess become the record in the meeting notes.

**Common mistakes:** Making up an explanation. Freezing or apologising at length. Naming a teammate or team as the cause. Promising an answer without a time. Using jargon to sound sure.

### S16 ⭐⭐⭐ 🟡 Team dynamics: a teammate on a shared deliverable is not delivering
**Asked at:** Underperforming-teammate prompts are listed on codemia.io and Dataford (title-only snippets, crowd-sourced); Book 9 Part 1 Q33 covers the story form; this scenario is the 'right now' decision with a deadline; search snippets only, not opened
**Situation:** You and a colleague own two halves of a report due in a week. Their half is late, thin and not responding to messages. You have not worked with them before and your manager is travelling.
**Weak response:** Wait silently and hope it resolves, then finish your half and present a partial report. Or complain about the colleague to others, or take over their half without telling anyone.

**Strong response:** Reach out directly and kindly first, using a different channel than the one they are ignoring, such as a call or a short chat: ask whether they are blocked and what would help. Agree on a concrete next step and a date. If there is no reply within a day or so, tell your manager (even though they are travelling, a short message works) with facts: what is due, what is done, what you have asked, and two options, for example narrowing the scope or reallocating part of the work. Meanwhile protect the deadline by drafting the parts you can, labelled clearly, and keep the interface between the two halves explicit so a late piece can drop in.

**Why it works:** It begins with curiosity, leaves a paper trail and escalates early enough to matter, with options rather than a complaint. Book 9 Part 1 Q33 covers the story version.

**What the interviewer scores:** Direct, respectful communication, timely escalation, focus on the deliverable and not on blame, and contingency planning.

**Say it like this:**
```
"Hi, I wanted to check in on your half of the report, since we're due next week and I haven't heard back. Is something blocking you? I'm happy to jump on a call today. If it helps, we could narrow the scope of your section. Could we agree on what I can expect by Wednesday?"
```
Then to the manager: "The report is due [date]. Their half isn't yet started to the agreed level, I've asked twice, and I'd like your steer on narrowing scope or moving part of it."

**If they push back:** If the colleague says they are overloaded, ask what can wait and offer to help prioritise, while asking the manager to confirm. If asked whether you went over their head, say you spoke to them first and only escalated when the deadline was at risk.

**Common mistakes:** Silence until the last day. Gossiping. Doing their work without telling anyone. Escalating with accusations. Assuming laziness before asking about blockers.

### S17 ⭐⭐⭐ 🟡 Influence without authority: a senior engineer's design has a flaw and you are the most junior person in the review
**Asked at:** Pushing back on a more senior person is a common prompt (codemia.io 'walk me through a time you had to push back under pressure' pages, and a coaching post on mid versus senior pushback, snippet only); the skew framing is editor-designed; search snippets only, not opened
**Situation:** In a design review a senior engineer proposes writing features at serving time with logic that differs from your training code. You suspect training-serving skew. Nobody else has raised it.
**Weak response:** Stay silent because you are the most junior person and nobody else has spoken. Or announce in front of everyone that the design is wrong.

**Strong response:** Raise it as a question about the design, not a verdict on the person. Name the specific concern: if the features are computed in a different way at serving time than in training, the model may see different inputs in production. Ask how the logic will be kept identical, for example through a shared feature code path or a feature store, or a test that compares training and serving values on the same records. Offer to write that comparison. If time is short, suggest a quick check that settles it with data. If the discussion is rushed, follow up in writing after the review. You may be wrong, and the senior engineer may have a reason, so ask first and listen.

**Why it works:** Questions are easier for a senior person to accept than corrections, and a concrete test turns an opinion into evidence. It treats your concern as worth the room's time without making it about status.

**What the interviewer scores:** Courage with courtesy, technical specificity, offering evidence and help, and willingness to be corrected.

**Say it like this:**
```
"Can I check one thing? In training we build these features one way, and at serving time the logic would be different. I'm worried about the model seeing slightly different values in production than it learned from. How will we keep the two paths identical? I could write a quick comparison of training and serving values on a sample of records so we can see whether there is any gap. If I've misread the design, I'd like to understand it."
```

**If they push back:** "We've done this before and it's fine." Ask what check made them confident and offer the comparison as a low-cost confirmation. If dismissed again, send a short written summary of the concern and the proposed check, and let the team decide.

**Common mistakes:** Saying nothing. Publicly declaring the design flawed. Being vague ("something feels off"). Offering no solution. Pressing the point repeatedly after it has been answered.

### S18 ⭐⭐⭐ 🟡 Ethics and judgement: you notice customer emails in a notebook open to the whole company
**Asked at:** Data-leak and privacy prompts appear in responsible-AI and ethics question lists in the results (hirevire, vintti, Yardstick pages; snippets, not employer rubrics); the shared-drive case is editor-designed. Editor note for Wave B: route through the proper internal channel and ask compliance or HR; no legal advice.; search snippets only, not opened
**Situation:** While browsing a shared drive you find a notebook with a table of customer email addresses and purchase history, visible to everyone in the company. It was saved by a colleague last month. You are not sure whether this is allowed.
**Weak response:** Ignore it because it is not your notebook. Or message the whole company, delete the file yourself, or ask the colleague in public chat.

**Strong response:** Do not copy, share or dig further into the data. Note where it is and what you saw, without saving the emails. Report it through the proper internal channel, such as the data owner, your manager, the security or privacy team, or compliance; your company will have a named route, so check the internal policy or ask HR or your manager where to send it. Say plainly that you are not sure whether this is allowed, and ask them to decide. Do not accuse the colleague; the file may be a mistake, and the report is about access. Do not give your own view on legal exposure: that is for compliance. Afterwards, let the colleague know in a kind and private way if the owners say that is fine.

**Why it works:** It protects customers quickly while leaving the judgement to the people who own it. You show you can notice risk, act, and not overstep. If AI tools or chat services were involved, say that too and use the same channel.

**What the interviewer scores:** Privacy instinct, using the right escalation path, no blame or vigilante action, and honest uncertainty.

**Say it like this:**
```
"I came across a notebook on the shared drive with customer email addresses and purchase history, and it looks open to everyone in the company. I haven't copied or shared it. I'm not sure whether that is permitted, so I'm passing it to you so the right team can decide. It's at [location], saved last month by a colleague. I'd like to keep the colleague out of trouble if it's an accident, and I'm happy to give more detail."
```

**If they push back:** "Why didn't you just tell the colleague?" Say you may do that after the owners decide, but access needed fixing quickly and the owners know the policy. If asked whether it is a breach, say that is for compliance to decide, and offer to share the facts you have.

**Common mistakes:** Doing nothing. Downloading the data as "evidence". Posting about it in a public channel. Blaming the colleague. Giving a confident opinion about legal consequences.

### S19 ⭐⭐⭐ 🔴 Failure and ownership: a production model starts giving odd predictions on a Friday evening
**Asked at:** Incident ownership is a theme in MLOps and behavioural lists; no public page found for this exact on-call framing, editor-designed; Book 4 covers the monitoring mechanics and Book 9 Part 2 Q38 the incident write-up; search snippets only, not opened
**Situation:** You are the one on call. Alerts show a sharp shift in scores for a model that feeds a customer-facing feature, and you cannot reach the model's usual owner. Your manager's phone is off.
**Weak response:** Wait for the owner to call back before touching anything, or make a large unreviewed change such as retraining or rewriting the model on your own at night.

**Strong response:** First check it is real: is the shift in the inputs, in the pipeline, or in the model's output, and is anything customer-facing visibly wrong? Use the runbook and any documented on-call escalation: page the secondary on-call, the team channel or the engineering manager on duty, not only the people you could not reach. Then choose the smallest safe action that is within your on-call remit, for example pausing the feature, falling back to the previous model or a rule, or switching to a safe default, and record what you did. If you are not authorised to roll back, get that approval from whoever the runbook names. Write down times, the evidence and the actions as you go. Message the owner and your manager with a summary so it is the first thing they see. Do the root-cause analysis on Monday, not at midnight.

**Why it works:** It reduces customer harm using the least irreversible step and keeps humans informed. Book 4 covers monitoring mechanics, and Book 9 Part 2 Q38 the incident write-up.

**What the interviewer scores:** Calm triage, using escalation paths, reversible action, documentation, and not heroics.

**Say it like this:**
```
"Scores for [model] have shifted sharply since [time] and it feeds [feature]. I haven't reached the owner or my manager, so I've paged the secondary on-call and posted in the team channel. Customer impact looks [limited / visible]. Under the runbook I've switched the feature to the previous model, and I've logged the times and screenshots. I'll keep watching and send an update at [time]. Root-cause work can wait until the owners are back."
```

**If they push back:** "Why not leave it until Monday?" Say that if customers were affected, a reversible fallback was a low-cost choice and you documented it. If asked why you did not retrain, say a fast retrain on suspect data could worsen things.

**Common mistakes:** Waiting passively. Big irreversible changes at night. Skipping the runbook. No notes. Telling no one what was done.

### S20 ⭐⭐⭐ 🔴 Ethics and judgement: your manager asks you to report the best of five runs as the headline number
**Asked at:** A responsible-AI question list in the results asks about advocating for good practice despite pressure to speed up (Yardstick page, snippet); no public page found for metric inflation specifically, editor-designed; Book 6 Part 6 covers a multi-metric version with numbers; search snippets only, not opened
**Situation:** You ran five versions of an experiment and one looks clearly better by chance-prone margins. Your manager wants that one in the board update and says the others are not needed. The deck goes out tonight.
**Weak response:** Put the best run in the deck as the headline and say nothing about the other four, since your manager asked. Or refuse flatly and say the manager is wrong.

**Strong response:** Talk to your manager before the deck goes out, with a solution rather than a lecture. Explain in one line that picking the best of five runs makes a result look stronger than it is, because some difference is expected by chance. Offer options that still give a clean headline: report the pre-planned metric; show all five runs in a small table or range; or call the best run exploratory and say it needs confirming on fresh data or a re-run. Ask which wording fits the board. If your manager still wants only the best run presented as fact, do not do it; ask for the claim to be worded honestly, and if still unresolved, take it through your company's escalation route or ask a senior colleague. Keep the tone cooperative and factual.

**Why it works:** It shows you can disagree with a manager on integrity and still help meet the deadline. See Book 9 Part 1 Q38 for the story form and Book 6 Part 6 Q28 for the multi-metric version with numbers.

**What the interviewer scores:** Honesty under pressure, statistical judgement stated plainly, offering workable alternatives, and escalating sensibly.

**Say it like this:**
```
"I'd like us to avoid a headline that the board may later find hard to reproduce. We ran five versions, and the best of five will tend to look better by chance. Could we show the planned metric, or all five in one small table, and call the top run promising but unconfirmed? I can have that slide ready within an hour, so the deck still goes out tonight."
```

**If they push back:** "The board doesn't want detail." Say a one-line caveat and a small table keep it simple while protecting you both. If told to drop it anyway, say you are not comfortable presenting it as a confirmed result, and ask who else should decide.

**Common mistakes:** Complying silently. Lecturing about p-values. Refusing with no alternative. Going over your manager's head first. Hiding the other runs in an appendix nobody sees.
