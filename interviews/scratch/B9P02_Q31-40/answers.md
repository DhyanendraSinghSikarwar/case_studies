### Q31 ⭐⭐ 🟡 How do you write a README or handover note for a model or analysis that someone else will have to run and explain?
**Asked at:** Guidance on written communication for data scientists (Towards Data Science pieces on writing, a Yardstick communication-skills page, a HelloInterview page on design-doc experience, postmortem-writing guides, which are practitioner blogs, not interview lists); written-format prompts are partly editor-designed; search snippets only, not opened
**Say this first (1 line):** I write it for a tired colleague who has never seen the project: what it is for, how to run it, what it assumes, where it breaks, and who to ask.

**Structure:** Writing structure, in this order (editor guidance [G]; see the pattern section above for the "answer first" habit).
1. Purpose in two sentences: the decision or product it supports and who uses the output.
2. How to run it: exact commands, environment, data location and expected run time. Test it on a clean machine.
3. Inputs and outputs: what goes in, what comes out, and what a normal result looks like.
4. Assumptions and known limits: data period, groups it was not tested on, metrics and their meaning in plain words.
5. What to check when it breaks: the two or three usual failures and the first check for each.
6. Owner, last updated date, and open questions.
Keep it short, link to detail, and write dates, not "recently".

**Strong sample answer (spoken):** (Illustrative; replace with your own.)
"I picture the person who inherits this in a hurry, and I write for them. The top of the README says in two lines what the model predicts and who uses it. Next come the commands to run it, which I try on a fresh machine so I know they work. Then what goes in and what comes out, with a normal example. Then a short limits section: the date range of the data, the groups it was weak on, and what the main metric means in plain words. After that, the usual ways it fails and what to check first. At the end, an owner and a date. For a handover I add one page: what is finished, what is half done and what I would do next. I ask a colleague to follow it without me. Wherever they get stuck, the document is wrong."

**Weak version (and why it fails):** "I add comments in the code and a README with the library list." It explains how you built it, not how someone else runs and explains it, and it hides the assumptions that cause wrong decisions later.

**What the interviewer scores:**
- Reader focus: you write for the person who will run it, not for yourself.
- Completeness where it matters: assumptions, limits and failure checks, not only setup.
- Testing the document: you check that someone else can follow it.
- Brevity and upkeep: dated, owned, short, linked.

**Make it yours:**
- Think of a real project you handed over or inherited. What did the next person ask you that the notes did not say?
- Which assumption in your own work would surprise a newcomer?
- Open your latest README and try it as a stranger. What is missing?
- Who could test your handover note for you?

**Script (copy and adapt):**
```
# [Project name]: handover note ([date])
Purpose: [one or two lines: decision supported, who uses the output]
Run it: [commands, environment, data path, expected run time]
Inputs / outputs: [what goes in, what comes out, a normal example]
Assumptions and limits: [data period, groups not tested, what the metric means in plain words]
If it breaks, check first: [failure 1 -> check], [failure 2 -> check]
Status: [done / half done / next steps]
Owner and contact: [name, how to reach]
```

**Follow-ups:**
- "How long should it be?" Short enough to read in ten minutes; link to detail for the rest.
- "How do you keep it current?" Date it, name an owner and update it in the same change as the code.
- "What if you have no time?" Write the limits and the failure checks first; those save the most pain.

**Common mistakes:**
- Describing the code and not the decision it supports.
- Leaving out assumptions and known weak spots.
- Never testing the instructions on a clean setup.
- No owner or date, so nobody trusts it later.

### Q32 ⭐⭐ 🟡 Engineering and product disagree on priorities for a data feature and both look to you. How do you bring them to one plan?
**Asked at:** Public stakeholder-management pages (Dataford questions on unclear or conflicting requirements, handling pushback and setting realistic expectations; one Dataford page tags a request-conflicts-with-model-limits question to a KPMG data scientist interview, which is a secondhand listing; a Towards Data Science stakeholder piece); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I would put both sides in front of the same facts and the same goal, agree how we will decide, and write down one plan with an owner and a review date.

**Structure:** A handling sequence (editor guidance [G]; the numeric versions of such clashes are in Book 6 Part 6).
1. Listen to each side separately first: what do they need, and what are they afraid of?
2. Find the shared goal (the user outcome or the business metric) and say it out loud.
3. Make the trade-off visible: a one-page table with options, effort, expected value, risks and what each side gives up.
4. Agree the decision rule before the decision: who decides, by when, on what evidence.
5. Offer a small test or a phased plan if the facts are unclear.
6. Write the plan and send it to both. Review on a set date.
If it still stalls, escalate the choice with a recommendation, not the quarrel.

**Strong sample answer (spoken):** (Illustrative; replace with your own.)
"I would first talk to each side on their own and ask what happens to them if their priority slips. Usually one side fears a customer problem and the other fears a technical one. Then I would bring them together around the goal we share, for example fewer failed orders. I would put the two options on one page, with effort, expected gain and risk, and what each side gives up. I would ask who makes the call and what evidence they need. Often the answer is a small first step, like doing the data fix now and the new feature next month. I would send the agreed plan in writing, with names and a review date. If we could not agree, I would take the options and my recommendation to the person who owns the decision. I would not ask them to referee the argument."

**Weak version (and why it fails):** "I would side with whoever has the stronger case and tell the other to accept it." It skips what the other side needs, damages the relationship and leaves no agreed rule for next time.

**What the interviewer scores:**
- Neutrality: you gather both views before you propose anything.
- Structure: shared goal, visible trade-off, decision rule.
- Written closure: a plan, owners and a date.
- Escalation judgement: you bring options and a recommendation, not a complaint.

**Make it yours:**
- Recall a real clash between two teams you worked with. What did each side actually need?
- What shared goal could you have named?
- What would your one-page comparison have shown?
- If you have not led one, describe how you would explain a smaller disagreement and what you did.

**Follow-ups:**
- "What if both say theirs is urgent?" Ask what happens if it waits two weeks; the answer usually separates them.
- "What if you are junior?" Facilitate: ask questions, write the options, and let the owner decide.
- "What if the loser is unhappy?" Say what they will get and when, and keep the review date.

**Common mistakes:**
- Taking sides in the room.
- Debating opinions without shared facts.
- Ending with a verbal agreement nobody wrote down.
- Escalating before trying to bring them to one page.

### Q33 ⭐⭐ 🟡 Six teams send you requests and you can do two this quarter. How do you prioritise, and how do you tell the other four?
**Asked at:** Public stakeholder-management pages (Dataford questions on unclear or conflicting requirements, handling pushback and setting realistic expectations; one Dataford page tags a request-conflicts-with-model-limits question to a KPMG data scientist interview, which is a secondhand listing; a Towards Data Science stakeholder piece); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I score every request on the same few criteria, pick the two that earn the most for the effort, and tell the other four a clear no or not-now with the reason and a way back.

**Structure:** A prioritising and telling sequence (editor guidance [G]).
1. List all six in one place: requester, goal, decision it supports, effort, deadline.
2. Score on shared criteria: value to the business, effort, urgency, risk of not doing it, and fit with team goals. A simple table is enough; do not pretend the scores are exact.
3. Check dependencies and quick wins: sometimes a small piece of one request serves two teams.
4. Show the choice to your manager or the priority owner before you announce it.
5. Tell each team yourself, with the reason. For the four: what you decided, why, what would change it, and an alternative (a self-serve option, a smaller version, a later quarter).
6. Publish the list so everyone sees the same order.

**Strong sample answer (spoken):** (Illustrative; replace with your own.)
"I would put all six on one page and score them the same way: how much value, how much effort, how urgent, and what it costs if we do nothing. I would check the top choices with my manager, because priority is a shared decision. Then I would tell each team myself. For the two we take, I confirm scope and date. For the other four, I say it plainly: 'We cannot do this quarter. Here is why, here is what we chose instead, and here is what would move it up.' Where I can, I offer something small, like a template, a short consult or a place in next quarter's plan. And I share the full list, so nobody feels their request vanished or that someone else jumped the queue."

**Weak version (and why it fails):** "I would do the loudest or the most senior request first and tell the rest I am busy." Priority by volume feels unfair, hides your reasoning and teaches teams to shout.

**What the interviewer scores:**
- A clear, repeatable method rather than gut feel.
- Alignment with your manager or the owner of priorities.
- Respectful, direct no: reason, alternative, path back.
- Transparency across teams.

**Make it yours:**
- Think of a real time you had more requests than capacity. What did you use to decide?
- Which request did you decline or delay, and how did you say it?
- What alternative could you have offered?
- Name the criteria you would use in your current or target role.

**Script (copy and adapt):**
```
Hi [name], thanks for sending [request]. This quarter we are focusing on [two chosen items] because [reason tied to team goals]. We cannot take [request] now.
What would help: [smaller version / self-serve option / a short consult on date].
It would move up if [condition]. I will put it on the list for [next planning date] and keep you posted.
```

**Follow-ups:**
- "What if a senior person pushes theirs up?" Show the trade-off: "I can do it if we drop X. Do you want that?"
- "What if a no damages the relationship?" Say it early, say it kindly and offer something real.
- "How do you avoid scoring games?" Keep criteria few, public and reviewed with your manager.

**Common mistakes:**
- Saying yes to everything and missing all of it.
- Announcing the no by silence.
- Letting rank decide with no reasoning shared.
- A long apology instead of a clear alternative.

### Q34 ⭐⭐ 🟡 How do you get a decision out of busy leaders who keep postponing it?
**Asked at:** Public stakeholder-management pages (Dataford questions on unclear or conflicting requirements, handling pushback and setting realistic expectations; one Dataford page tags a request-conflicts-with-model-limits question to a KPMG data scientist interview, which is a secondhand listing; a Towards Data Science stakeholder piece); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I make the decision small, dated and easy: one page, two options with a recommendation, a deadline tied to a real cost of delay, and a named owner.

**Structure:** A sequence for getting decisions (editor guidance [G]).
1. Find out why it is stuck: unclear options, missing information, fear of risk, or no owner.
2. Reduce the ask to one question that can be answered yes or no, or a choice between two.
3. Bring your recommendation and the default: "If I hear nothing by [date], I will proceed with option A."
4. State the cost of delay in their terms: what slips, who waits, what it costs.
5. Make deciding cheap: a ten-minute slot, a one-page note sent beforehand, or a reply by message.
6. Record the decision and the reason in writing and send it back.

**Strong sample answer (spoken):** (Illustrative; replace with your own.)
"First I would find out why it keeps slipping. Sometimes the options are unclear, sometimes they want more evidence, sometimes nobody feels it is theirs to decide. Then I would shrink the ask. I would send a one-page note: the decision needed, two options, my recommendation and what we lose by waiting. I would put a date on it and say what I will do by default if I hear nothing, for example 'I will go with option A on Friday unless you tell me otherwise.' I would ask for ten minutes, not an hour. When they decide, I write it down and send it back: what was decided, why and who owns the next step. That stops it coming back as a new question next week."

**Weak version (and why it fails):** "I keep reminding them every few days until they answer." Repeated nudges add noise, never clarify the choice and make you the person who nags rather than the person who helps them decide.

**What the interviewer scores:**
- Diagnosis: you ask why before you push.
- Making the decision easy: one page, options and a recommendation.
- Respect for their time and a clear default or deadline.
- Written closure and ownership.

**Make it yours:**
- Recall a real decision that stalled. What was the real reason?
- What cost of delay could you have shown?
- What would your one-page note have said?
- Is a default date comfortable in your culture and role? Adapt the wording rather than drop the idea.

**Script (copy and adapt):**
```
Hi [name], a quick decision needed on [topic] by [date].
Options: A) [..] B) [..]. My recommendation: [A], because [reason].
If we wait past [date], [cost of delay].
Could you reply with A or B, or take ten minutes on [slot]? If I do not hear back I will proceed with [default] and let you know.
```

**Follow-ups:**
- "What if they still do not reply?" Ask your manager or their assistant for a short slot, or confirm the default in writing and proceed.
- "What if the default turns out wrong?" Choose defaults that are easy to reverse, and say so.
- "Is that pushy?" Not if you are brief, give the reason and offer an easy way to say no.

**Common mistakes:**
- Sending long background with no question.
- Offering many options and no recommendation.
- No date and no consequence.
- Not recording the decision.

### Q35 ⭐⭐ 🟡 A launched model or dashboard is in use. How do you follow up with stakeholders, and what do you report back?
**Asked at:** Public stakeholder-management pages (Dataford questions on unclear or conflicting requirements, handling pushback and setting realistic expectations; one Dataford page tags a request-conflicts-with-model-limits question to a KPMG data scientist interview, which is a secondhand listing; a Towards Data Science stakeholder piece); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** After launch I check in on a schedule, report whether it is being used and whether it still works, and ask the users what is not working before they tell me.

**Structure:** A follow-up plan (editor guidance [G]).
1. Plan it before launch: agree the success measure, the owner and the dates for check-ins (for example after two weeks and after a quarter).
2. Report three things: use (who, how often), outcome (did the decision or metric move, with the honest range), and health (data freshness, errors, drift, complaints).
3. Ask users directly: what do you do with it, what do you ignore, what is missing, where do you not trust it?
4. Bring what you changed and what you propose next, with the cost.
5. Say what you do not yet know.
6. Keep it short and send it in the channel they already read.

**Strong sample answer (spoken):** (Illustrative; replace with your own.)
"Before launch I agree what success looks like and when we will look again. After launch I do a short check-in at two weeks and then regularly. I report three things. Is it used: how many people, how often, and where people have stopped. Is it working: did the metric we agreed move, and how sure are we. Is it healthy: data on time, errors, and any drift. I also speak to a few users and ask what they ignore and what they do not trust, because that tells me more than usage numbers. In the report I say what we fixed, what we propose next and what we still do not know. I keep it to one page, in the place they already read."

**Weak version (and why it fails):** "I send a message saying it is live and ask them to tell me if there are problems." It leaves the checking to busy users, so silent failure and silent abandonment go unseen.

**What the interviewer scores:**
- Ownership beyond launch: you care about outcomes, not delivery.
- Honest measures: use, outcome and health, with uncertainty.
- Listening: you ask users, not only dashboards.
- Brevity and a clear next step.

**Make it yours:**
- Pick a real model, dashboard or analysis you shipped. What happened a month later?
- What did you check, and what did you not?
- Who could you have asked about real use?
- Which one measure would you promise next time?

**Follow-ups:**
- "What if nobody uses it?" Find out why before judging: wrong format, wrong time, or no trust. Then fix it or retire it and say so.
- "What if it works but benefits are unclear?" Report the range and what evidence would settle it.
- "How often do you report?" Match their rhythm; fewer, shorter reports beat many long ones.

**Common mistakes:**
- Treating launch as the finish line.
- Reporting usage only, with no outcome.
- Hiding drift or problems until a stakeholder finds them.
- Long reports nobody reads.

### Q36 ⭐⭐ 🟡 During your presentation someone interrupts repeatedly and then asks a hostile question. How do you respond?
**Asked at:** General presentation guidance on hostile and hard questions (HighSpark, a board-presentation guide and other training pages, none data-science specific); no public data-science interview list found for this prompt, so it is editor-designed; search snippets only, not opened
**Say this first (1 line):** I stay calm, answer the substance briefly, park what I cannot do in the room, and offer a follow-up, without matching the tone.

**Structure:** A response sequence (editor guidance [G]; public presentation guides give the same core advice: answer first, keep it short, follow up if you do not know; snippets only).
1. For repeated interruptions: acknowledge, then set a rule. "Good point. Let me finish this section, then take questions."
2. For the hostile question: pause, breathe, and take the question as a real concern.
3. Restate it neutrally in one sentence so you answer the substance, not the tone.
4. Answer in two or three sentences with evidence. If the answer is "I do not know", say so and give a date for a follow-up.
5. Check: "Does that answer it?" Offer to continue after the session.
6. Return to your point. If it continues, involve the host or take it offline.

**Strong sample answer (spoken):** (Illustrative; replace with your own.)
"If someone interrupts a few times, I would say, 'Thanks, I want to give that proper time. Can I finish this part and come to you right after?' Then I do. When the hostile question comes, I pause and restate it in plain words: 'You are asking whether this model is reliable enough to trust. That is fair.' Then I answer in a few sentences, with the evidence, and say what the limit is. If I do not know, I say, 'I do not know yet. I will check and send you the answer by Thursday.' I ask whether that answers it, and I offer to carry on afterwards. I do not defend my pride. If it keeps going, I ask the host to help us come back to it after the meeting."

**Weak version (and why it fails):** "I would defend my analysis strongly so nobody doubts it." Raising your tone confirms the audience's worry, and a long defence loses the room.

**What the interviewer scores:**
- Composure: steady voice, no defensiveness.
- Substance over tone: you answer the real concern.
- Honesty about limits, with a follow-up promise.
- Control of the room without rudeness.

**Make it yours:**
- Think of a real meeting where someone pushed hard on your work. What was the real concern behind it?
- What phrase can you use to pause and restate?
- What do you say when you do not know?
- Practise the first sentence aloud until it sounds like you.

**Follow-ups:**
- "What if they are right?" Say so: "You are right, that changes the conclusion for this group. I will rerun it."
- "What if the host does nothing?" Offer a short one-to-one afterwards; do not argue in public.
- "What if you freeze?" Take a breath and ask them to repeat the question; that buys time and nobody minds.

**Common mistakes:**
- Answering the tone, not the question.
- Long defensive answers.
- Guessing instead of saying you will follow up, and then not following up.
- Treating the person as an enemy.

### Q37 ⭐⭐ 🔴 A business owner plans to put an LLM chatbot in front of customers. How do you explain the hallucination risk and what you would put in place?
**Asked at:** Vendor and explainer pages on LLM hallucination in business (Kili, Glean, DataRobot and similar, which are marketing material, not interview lists); no interview question list found for the exact prompt, so it is editor-designed; search snippets only, not opened
**Say this first (1 line):** I would say plainly that the chatbot writes plausible text and does not check facts, so it will sometimes be wrong with confidence, and then show the safeguards that match the cost of a wrong answer.

**Structure:** An explanation structure plus a safeguards list (editor guidance [G]; public explainers, mostly vendor pages, repeat that the model predicts likely text, cannot be assumed to verify truth, and that elimination of errors is not realistic; snippets only, vendor figures not used).
1. Decision: go live, in what scope, with what checks.
2. Plain meaning: it predicts likely words, so it can state a wrong thing fluently.
3. One example in their domain: a made-up policy, price or refund rule stated confidently.
4. Cost of an error: low (a casual question) or high (money, health, safety, promises to customers).
5. Safeguards: answer only from approved documents, show sources, refuse topics outside scope, easy handover to a human, logging and review of sample conversations, a test set of real questions before launch, and a rollback plan.
6. What you cannot promise: zero errors. Offer to measure the error rate and report it.

**Strong sample answer (spoken):** (Illustrative; replace with your own.)
"A chatbot like this does not look things up the way a person does. It writes the most likely next words, so it can sound sure and still be wrong. Imagine it telling a customer about a refund rule that does not exist. That is the risk. We cannot promise zero errors, but we can make them rarer and less costly. I would limit it to answers from our approved documents and show where they came from. I would block topics it should not handle and give an easy route to a person. Before launch I would test it on a few hundred real customer questions, and afterwards review a sample of conversations every week. For anything involving money or promises, a human checks. If the error rate is too high on the test, we do not launch."

**Weak version (and why it fails):** "Do not worry, we will tune the prompt and it will be accurate." It promises what cannot be promised, and the owner learns about the risk from a customer complaint.

**What the interviewer scores:**
- Plain, accurate explanation with no promise of zero errors.
- Match between safeguards and the cost of a wrong answer.
- Testing before launch and monitoring after.
- Willingness to say "not yet" with a measure behind it.

**Make it yours:**
- If you have built or tested an LLM feature, what wrong answer did it give? Use that real example.
- What would a wrong answer cost in your domain?
- Which two safeguards would you insist on?
- Check your claims about the tool against its current documentation; do not rely on memory.

**Follow-ups:**
- "Can you fix hallucination completely?" Not with current approaches as far as I know; reduce it, detect it and limit the harm.
- "What do you measure?" Error rate on a real-question test set, how often it hands over to a person, and complaints.
- "Who is accountable?" The owner and the team, not the model; agree that before launch.

**Common mistakes:**
- Using jargon such as "temperature" or "tokens" with a business owner.
- Promising accuracy without a test.
- Treating all errors as equal.
- Launching without a human route or a rollback.

### Q38 ⭐⭐ 🔴 A model failure reached customers. Write the incident report summary: what do you include, and how do you word cause and blame?
**Asked at:** Guidance on written communication for data scientists (Towards Data Science pieces on writing, a Yardstick communication-skills page, a HelloInterview page on design-doc experience, postmortem-writing guides, which are practitioner blogs, not interview lists); written-format prompts are partly editor-designed; search snippets only, not opened
**Say this first (1 line):** I write it for the reader who was not there: what happened, who was affected, the cause in system terms, what we did, and what changes now, with no names and no blame.

**Structure:** Writing structure for the summary (editor guidance [G]; practitioner postmortem guides in the sources note advise writing for a future engineer and avoiding naming individuals; snippets only).
1. Impact first: what customers saw, from when to when, how many were affected (use known figures; label estimates).
2. Timeline in a few lines: detection, response, fix.
3. Cause: the conditions that allowed it, in system terms (a check was missing, a change was untested, an alert did not fire). Say "contributing factors" if there are several.
4. What we did to stop it and to help affected customers.
5. What changes now: specific actions, each with an owner and a date.
6. What we do not yet know.
Wording rule: describe what the system and process allowed, not who made a mistake. Check your company's own incident process and who approves external wording.

**Strong sample answer (spoken):** (Illustrative; replace with your own.) The written summary:
```
Summary: Between [start] and [end], [what customers saw]. About [number or "an estimate of"] customers were affected.
Detection and response: We detected it on [date] through [alert/report] and rolled back on [time].
Cause: A change to [component] reached production without a check on [condition], and monitoring did not alert on [signal].
Customer impact and remedy: [what we did for affected customers].
Actions: 1) Add [check] before release, owner [role], by [date]. 2) Add alert on [signal], owner [role], by [date].
Open questions: [what we are still investigating].
```
"I would read that aloud as: here is what happened, here is who it hit, here is why the system let it through, and here is what we are changing."

**Weak version (and why it fails):** "The analyst pushed a bad model and did not test it." It names a person, hides the process gaps that will let it happen again and leaves no actions.

**What the interviewer scores:**
- Clarity: impact and facts before story.
- Blameless wording that still states a real cause.
- Concrete actions with owners and dates.
- Honesty about unknowns and customer remedy.

**Make it yours:**
- Think of a real incident or failure you were part of or read about internally. Rewrite its cause in system terms.
- What actions would have prevented it?
- Where does your company require wording to be reviewed?
- Do not publish anything confidential; practise on a general or anonymised case.

**Follow-ups:**
- "Where does accountability go if nobody is blamed?" Actions have owners; accountability is for fixing, not for naming.
- "What if one person clearly erred?" Describe what they did in terms of the process that allowed it; the manager handles any people issue separately.
- "How long should it be?" One page for the summary; detail in an appendix.

**Common mistakes:**
- Naming or hinting at an individual.
- Vague causes ("human error", "unexpected data").
- Actions with no owner or date.
- Hiding customer impact or guessing numbers without labelling them.

### Q39 ⭐⭐ 🔴 You used AI tools to help with an analysis and a stakeholder asks how much you can trust it. How do you explain what the AI did and what you checked?
**Asked at:** 2026 AI-era guides (a PrachHub prompt on describing an analysis where you used AI responsibly, Dataford questions on explaining AI concepts to business stakeholders, a Gartner session title on explaining AI and ML models to stakeholders); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I would say exactly what the AI did, what I checked myself, what I did not check, and that I am accountable for the result.

**Structure:** An explanation structure (editor guidance [G]; public prompts on responsible AI-assisted analysis stress that the person stays accountable and that testing beats "it looked right"; snippets only). Check your employer's AI policy; policies differ.
1. Scope: which parts the AI helped with (code, a first draft, a summary) and which it did not.
2. Verification: how you checked it (reran on a sample by hand, compared with an independent calculation, read the code, tested on cases with known answers, reviewed with a colleague).
3. Residual risk: what you could not check and how it could be wrong.
4. Data safety: what data went into the tool, and that it followed the approved rules.
5. Accountability: you own the result; here is who else reviewed it.
6. Offer to show the checks.

**Strong sample answer (spoken):** (Illustrative; replace with your own.)
"Good question. I used an AI assistant to draft the code for the data cleaning and to suggest a first version of the summary. I did not use it for the conclusions. To check it, I read the code, reran the key numbers by hand on a small sample, and compared totals with the source system. The summary I rewrote, and I changed two sentences that went further than the data did. What I could not fully check is [the one thing], so treat that part as lower confidence. I used only data that our policy allows in the tool. I am accountable for the result, and I am happy to walk you through the checks or have a colleague repeat them."

**Weak version (and why it fails):** "The AI did most of it, but it looked accurate to me." It gives no checks, shifts responsibility to the tool and invites a distrust you cannot answer.

**What the interviewer scores:**
- Honest account of the AI's role.
- Concrete verification, not "it looked right".
- Stated residual risk and data handling.
- Ownership of the result.

**Make it yours:**
- Think of a real analysis where you used an AI tool. What did it do, and what did it get wrong?
- What was your single strongest check?
- What could you not verify?
- What does your employer or target employer say about AI use? Check their current policy; do not assume.
- Do not use AI to write this answer; follow-ups will test whether you did the work.

**Follow-ups:**
- "Would you use it again?" Yes for drafts and code I can check; no for anything I cannot verify.
- "What if the tool was wrong and you missed it?" Say it, correct it, tell the reader and add the check that would have caught it.
- "Do you tell people every time?" Follow the employer's expectations and disclose when it affects trust.

**Common mistakes:**
- Hiding or downplaying the AI use.
- Saying "I checked it" with no method.
- Pasting sensitive data into tools without approval.
- Blaming the tool for an error.

### Q40 ⭐ 🟢 You must present your results over a video call to people you cannot see. What do you change compared with presenting in a room?
**Asked at:** General presentation and virtual-meeting guidance; no public data-science list found for this exact wording, editor-designed; search snippets only, not opened
**Say this first (1 line):** I make it more interactive and more explicit: shorter, with the answer first, simple slides, planned pauses for questions, and a clear way to hear from people I cannot see.

**Structure:** What to change (editor guidance [G]; general presentation advice, no data-science source).
1. Before: test sound, camera, screen share and the link; close other windows and notifications; have a backup way to share the slides.
2. Open: state the decision and the agenda in the first minute; ask people to use chat or raise a hand.
3. Slides: fewer words, bigger charts, one point each; say what to look at.
4. Pace: pause every few minutes with a named question ("Does this match what you see?"), because you cannot read faces.
5. Questions: tell people how to ask (chat, voice), watch the chat or have a helper do it, and repeat questions before answering.
6. Close: summarise the decision and next steps, and send the slides and a short written summary afterwards.

**Strong sample answer (spoken):** (Illustrative; replace with your own.)
"I assume I will lose people faster, so I tighten everything. I test my screen share and sound beforehand and have the slides ready to send if sharing fails. In the first minute I say what we need to decide and how to ask questions: use the chat or just speak. I keep slides simple, one point per slide, and I point at what to look at. Because I cannot see faces, I stop every few minutes and ask a real question, like 'Does that match what you see in your area?' I keep an eye on the chat or ask a colleague to. At the end I repeat the decision and the next steps and send a short summary with the slides."

**Weak version (and why it fails):** "I present the same way and just speak louder." You get no signal from the audience, and attention drifts without you noticing.

**What the interviewer scores:**
- Awareness of the lost signal and a plan for it.
- Preparation for technical failures.
- Interaction and clear closing.
- Simplicity of slides and message.

**Make it yours:**
- Recall a real video presentation of yours. Where did you lose people or miss a question?
- Which one change would help most?
- Practise a pause question for your own topic.
- Check the meeting tool's features you will use before the day.

**Follow-ups:**
- "What if the video freezes?" Pause, say what happened in the chat, share the slides to everyone and offer to continue by phone.
- "What if nobody speaks?" Name a person kindly or ask for a chat vote; silence is not agreement.
- "Camera on or off?" Follow the group's norm; on helps connection when bandwidth allows.

**Common mistakes:**
- Reading dense slides aloud.
- Going 20 minutes without a check-in.
- Not testing the setup.
- Ignoring the chat.
