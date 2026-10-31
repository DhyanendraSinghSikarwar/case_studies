### Q41 ⭐ 🟢 Write a Slack message escalating a blocker to a senior person. What makes it easy to act on?
**Asked at:** Guidance on written communication for data scientists (Towards Data Science pieces on writing, a Yardstick communication-skills page, a HelloInterview page on design-doc experience, postmortem-writing guides, which are practitioner blogs, not interview lists); written-format prompts are partly editor-designed; search snippets only, not opened
**Say this first (1 line):** A good escalation is a message the senior person can act on without a call: the blocker, the impact and date, what I already tried, and the one thing I need from them.

**Structure:** Write it as five short lines, in this order (editor guidance [G]).
- Ask up front: what you need and by when.
- Blocker: one sentence, no history.
- Impact: what slips, for whom, and the date at which it hurts.
- Tried so far: two or three things, so they do not suggest them again.
- Options or a recommendation, plus where the details live (a link, not a wall of text).
Send it in a channel or thread the right person reads, and use their name once at the top.

**Strong sample answer (spoken):** Illustrative; replace with your own. "I would write it so it works on a phone in thirty seconds. Something like: 'Hi Priya, I need a decision from you by Thursday. The customer table feed has been missing since Monday and the churn refresh depends on it. If it is not back by Friday, the leadership review goes out with last month's numbers. I have asked the data platform team twice and checked that the job is not failing on our side. The options are: you ask the platform lead to prioritise the fix, or we ship with a clear note about stale data. I prefer the first. Details are in the ticket linked below.' I do not blame anyone, I keep it factual, and I say what I will do next if I hear nothing."

**Weak version (and why it fails):** "Hey, are you free? Have a problem with data." It forces the senior person to ask what, why, how bad and what you want, and it can sit unread for a day. A long wall of history is just as bad: the ask is buried and the reader cannot tell if it is urgent.

**What the interviewer scores:**
- Clarity: the ask and deadline are visible in the first line.
- Judgement about impact: you show why it matters to the business, not just to you.
- Ownership: you tried things first and bring options, not only a complaint.
- Tone: factual, no blame, no drama.
- Sense of when to escalate and to whom.

**Make it yours:**
- Pick a real blocker you have faced (a missing data feed, a stuck approval, an access request).
- Write the message in five lines using the order above, with the real date and impact.
- Cut every sentence that does not help the reader act.
- Name who you would send it to and why that person, not their manager.

**Script (copy and adapt):**
```
[Name], I need [specific help] from you by [day].
Blocker: [one sentence].
Impact: [what slips, for whom, by when].
Tried: [1], [2], [3].
Options: A) [..] B) [..]. I recommend [A] because [reason].
Details: [link]. If I do not hear back by [time], I will [fallback].
```

**Follow-ups:**
- When do you escalate instead of waiting? "When the date is at risk and I have tried the owner directly, early enough that there is still a choice to make."
- What if the senior person does not reply? "I follow up once in the same thread with the deadline, then ask someone who works with them how they prefer to be reached."
- Should you copy your own manager? "Usually yes, so nobody is surprised, and I say that I am doing so."

**Common mistakes:**
- Starting with a greeting and waiting for a reply before saying anything.
- Describing history instead of the ask.
- Naming a person as the cause.
- Arriving with no option or recommendation.
- Escalating before trying the owner of the problem.

### Q42 ⭐ 🟡 You are asked to explain a model on a whiteboard to a mixed group of engineers and business people. How do you structure it?
**Asked at:** General presentation guidance on hostile and hard questions (HighSpark, a board-presentation guide and other training pages, none data-science specific); no public data-science interview list found for this prompt, so it is editor-designed; search snippets only, not opened
**Say this first (1 line):** I would draw the whole thing as three boxes, inputs, model and decision, answer the business question first, then add one layer of detail at a time so engineers can go deeper without losing the others.

**Structure:** Layered whiteboard (editor guidance [G]; see also the pattern section "A pattern for explaining anything to a non-technical person" above).
1. Ask who is in the room and what each group needs to decide or build. Write the decision at the top of the board.
2. Draw three boxes left to right: data in, model, decision out. Say it in plain words as you draw.
3. Give one concrete example moving through the boxes (one customer, one order).
4. Add layers on request: features and training data below the first box, evaluation and monitoring below the third. Engineers get depth, business people can ignore the lower layer.
5. Mark the limit and the safeguard in a corner, then invite questions by group.

**Strong sample answer (spoken):** Illustrative; replace with your own. "Before I draw, what decision are we here to make? Good. I will put that at the top. Now three boxes. On the left, the data we have about each customer. In the middle, the model, which learns from past cases which customers left and what they looked like. On the right, the decision: a score that tells the retention team who to call first. Let me walk one customer through. Engineers, underneath the middle box I will add how we build features and validate, and I will mark where it can go wrong. Business colleagues, the thing to remember is the score ranks people, it does not promise anyone will leave. Tell me which part you want me to open up."

**Weak version (and why it fails):** Starting with the architecture diagram and jargon for the engineers. The business people disengage within a minute and never reach the decision. The opposite fails too: a vague story with no detail, which loses the engineers' trust.

**What the interviewer scores:**
- Audience awareness: you asked, then adapted.
- A clean top-level picture before detail.
- Use of one concrete example.
- Ability to go deeper without losing the room.
- Honesty about limits.

**Make it yours:**
- Choose a model you have actually built or studied and sketch it in three boxes on paper.
- Write the one-sentence decision it supports.
- Pick one real example case to walk through.
- Decide which detail you would add for engineers and which limit you would flag for the business side.
- Practise it aloud with a marker and a timer.

**Follow-ups:**
- What if an engineer pulls you into detail? "I answer briefly, note it, and offer to go deeper after, so the others stay with me."
- What if someone asks something you do not know? "I say so, write it on the board as an open question and follow up."
- What if there is no whiteboard? "The same three boxes on paper or a shared screen."

**Common mistakes:**
- Drawing before knowing the audience.
- Starting with the algorithm name instead of the decision.
- Writing too small or too much.
- Talking to the board with your back to the room.
- Skipping the limits.

### Q43 ⭐ 🟡 Your live demo fails in front of the stakeholders. What do you do in the next two minutes?
**Asked at:** General presentation guidance on hostile and hard questions (HighSpark, a board-presentation guide and other training pages, none data-science specific); no public data-science interview list found for this prompt, so it is editor-designed; search snippets only, not opened
**Say this first (1 line):** I would stay calm, say plainly what happened, switch to a backup I prepared (screenshots, a recording or slides) and keep going, then fix the cause after the meeting.

**Structure:** The two-minute plan (editor guidance [G]).
- Seconds 0-20: pause and say it in one calm sentence. No apology spiral.
- Seconds 20-60: move to the backup. Screenshots or a short recording of the demo, or walk through the result on slides.
- Minutes 1-2: keep the story going. Repeat the key point the demo was meant to show, and ask whether they want the live version later.
- Afterwards: find the cause, send the working demo or recording, and note what you will test before next time.
Prevention matters more than recovery: test the setup before the meeting, have an offline copy, and keep the demo short.

**Strong sample answer (spoken):** Illustrative; replace with your own. "I would say, 'The demo environment is not responding. Let me show you what it does with screenshots I captured this morning.' Then I would switch straight to the backup and walk through the same steps: here is the input, here is the prediction, here is how the reviewer sees it. I would say the point again in one sentence, so the demo failing does not change the message. At the end I would offer, 'I will send a working recording this afternoon and we can do a live session next week.' I would not blame the network or anyone else, and I would not spend time debugging in front of the room."

**Weak version (and why it fails):** Trying to fix it live for ten minutes while everyone watches, apologising repeatedly, or blaming IT. The meeting loses its purpose and your credibility drops more than the failure itself deserved.

**What the interviewer scores:**
- Composure and a calm tone.
- A prepared fallback, which shows planning.
- Keeping the message and the audience's time at the centre.
- Ownership without blame.
- Follow-through after the meeting.

**Make it yours:**
- Think of a demo or live walkthrough you have given or will give.
- List what could fail (network, login, data, a notebook kernel) and one backup for each.
- Write your one-sentence opening line for a failure.
- Name the follow-up you would send and by when.
- If you have actually had a demo fail, use that experience honestly; do not invent one.

**Script (copy and adapt):**
```
"The live environment is not responding, so let me show the same flow
with the recording I prepared. The point is [one sentence].
I will send the working version by [time]."
```

**Follow-ups:**
- Would you ever do a live demo again? "Yes, with a tested backup and a short script."
- What if there is no backup? "I explain the flow on a whiteboard or slide and offer a follow-up session."
- Whose fault is it? "It does not matter in the room. Afterwards I find the cause and fix the process."

**Common mistakes:**
- Debugging live in front of stakeholders.
- Over-apologising or joking nervously.
- Blaming a colleague or another team.
- Having no offline copy.
- Never following up after the meeting.

### Q44 ⭐ 🟡 You are told halfway through that your slot is cut from thirty minutes to ten. How do you adapt?
**Asked at:** General presentation guidance on hostile and hard questions (HighSpark, a board-presentation guide and other training pages, none data-science specific); no public data-science interview list found for this prompt, so it is editor-designed; search snippets only, not opened
**Say this first (1 line):** I would give the decision and recommendation first, then the two or three points that support it, move the rest to an appendix or a follow-up note, and ask the most senior person what they most want from the time left.

**Structure:** Cut by purpose, not by speed (editor guidance [G]).
1. Say it out loud: "I have ten minutes, so I will focus on the decision and the three things behind it."
2. Start from the answer: the result, the recommendation and the decision you need.
3. Keep only the evidence that would change the decision. Skip method, history and extra cuts.
4. Check the room: "Is there one area you want me to spend the time on?"
5. Leave time for questions and promise the detail in writing afterwards.
Prevention: always prepare a ten-minute and a one-minute version of any talk, and put the decision on the first or second slide.

**Strong sample answer (spoken):** Illustrative; replace with your own. "Understood, I will focus on what you need to decide. The short version: I recommend we launch to the two regions where the result is clear and wait on the third, because the data there is thin. Three reasons. First, the lift in the first two regions is consistent across weeks. Second, the third region has too little data to say either way. Third, the risk of waiting is small. I have the method and the extra segments in the appendix, and I will send them today. Is there one of these you would like me to open up first? I would like to leave five minutes for your questions."

**Weak version (and why it fails):** Racing through all thirty minutes of slides at triple speed, or dropping the conclusion and ending on methods. The audience gets noise and the decision is never made.

**What the interviewer scores:**
- Prioritisation: you know what changes the decision.
- Composure when plans change.
- Answer-first structure.
- Checking with the audience instead of guessing.
- Keeping accuracy: you do not hide the limits to save time.

**Make it yours:**
- Take a real presentation or report you have given and mark the three slides that matter most.
- Write a ten-minute and a one-minute version of its main message.
- List what moves to the appendix and what you would say about it.
- Practise the opening sentence aloud with a timer.

**Follow-ups:**
- What if they ask for something you cut? "I answer briefly from the appendix or promise a follow-up by a date."
- What if the cut happens before you start? "The same method, plus I ask the host who the key decision-maker is."
- Do you skip the caveats? "No. I shorten them to one sentence, because the limit can change the decision."

**Common mistakes:**
- Speeding up instead of cutting.
- Dropping the recommendation to keep the method.
- Not telling the audience what you are skipping.
- Leaving no time for questions.
- Having only one version prepared.

### Q45 ⭐ 🟡 How do you summarise a long technical design document for executives, while keeping it accurate for the engineers?
**Asked at:** Guidance on written communication for data scientists (Towards Data Science pieces on writing, a Yardstick communication-skills page, a HelloInterview page on design-doc experience, postmortem-writing guides, which are practitioner blogs, not interview lists); written-format prompts are partly editor-designed; search snippets only, not opened
**Say this first (1 line):** I would write a one-page summary built for the decision, with the recommendation, the trade-off, the risks and the cost first, and link every claim to the section of the design document where engineers can check the detail.

**Structure:** Two layers that point to each other (editor guidance [G]).
1. Top line: what is being proposed and what decision or approval is needed, in two sentences.
2. Why: the problem and the benefit in business terms, with the number that matters and how sure we are.
3. The main alternative considered and why it lost, in one or two lines.
4. Cost, timeline and dependencies, and the top risks with the safeguard for each.
5. Open questions and what is explicitly out of scope.
6. Links: each statement points to its section number so engineers can verify it.
Keep it to one page. Have an engineer read it for accuracy before it goes out, and keep the same terms and numbers as the design document.

**Strong sample answer (spoken):** Illustrative; replace with your own. "I would write the summary like this. 'We propose moving the recommendation model to a nightly batch job, replacing the live calls. This needs your approval for two engineers for six weeks. It cuts serving cost and removes a weekly outage risk. The trade-off is that recommendations will be up to a day old; we think that is acceptable for this use and will check with a test. We considered a streaming design but it costs more and adds little here. Main risk: the nightly job fails and shows stale results; we will alert and fall back to the previous day. Details in sections three and five.' Then I would ask the tech lead to read it and tell me if anything is simplified in a way that is wrong."

**Weak version (and why it fails):** Pasting the design doc's introduction, or dropping all caveats to make it sound clean. Executives still do not know what is asked of them, and engineers see an inaccurate summary and stop trusting it.

**What the interviewer scores:**
- Decision-first structure and a clear ask.
- Translation of technical choices into cost, risk and benefit.
- Accuracy: caveats and trade-offs survive.
- Traceability to the source document.
- Using a technical reviewer.

**Make it yours:**
- Pick a real design doc or project write-up you know.
- Write the two-sentence top line and the one number that matters.
- Choose the one trade-off you would not leave out.
- Ask a colleague to check that the summary is accurate for them.
- Do not summarise a document you have not read in full.

**Follow-ups:**
- What do you cut? "Method detail, history and rejected options beyond the main one, but I link them."
- How do you stay accurate? "I use the document's own terms and numbers and have an engineer review it."
- What if executives want even less? "One sentence plus the ask, with the page available behind it."

**Common mistakes:**
- Leaving out the trade-off so it reads as risk-free.
- Writing in the document's order, not the decision's.
- Changing numbers or terms.
- Using jargon the readers will not know.
- Skipping a technical review.

### Q46 ⭐ 🟡 Your manager asks whether AI wrote your analysis. How do you describe your use of AI tools honestly, and what policy questions do you check first?
**Asked at:** 2026 AI-era guides (a PrachHub prompt on describing an analysis where you used AI responsibly, Dataford questions on explaining AI concepts to business stakeholders, a Gartner session title on explaining AI and ML models to stakeholders); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I would say honestly what I used AI for, what I checked myself and what I own, and before that I would check my employer's policy on AI tools and on what data can go into them.

**Structure:** Policy first, then a plain account (editor guidance [G]; employer rules differ, so this book does not state what any policy says; ask your manager or check the official policy).
1. Policy check: Which tools are allowed? What data may go into them? Must I disclose use, and in what form? Who do I ask if unsure?
2. What the AI did: drafting code, summarising, suggesting charts, first-pass text. Be specific.
3. What I did and verified: logic, queries, numbers reproduced, results sanity-checked, sources read.
4. What I own: the conclusions and any mistake in them.
5. What I would do differently or flag, and how the work can be reproduced.

**Strong sample answer (spoken):** Illustrative; replace with your own. "Yes, I used an AI assistant for part of it, and I would rather say so plainly. I used it to draft the first version of some data-cleaning code and to suggest wording for the summary. I wrote the analysis plan, ran and reviewed every query, rechecked the main numbers against the source table, and rewrote the conclusions myself. The results are my responsibility, whatever helped me get there. I did not put any customer data into the tool, which I checked against our guidance first. If you want, I can show you the checks and the notebook so you can reproduce it. And if the policy asks for a note in the document, I will add one."

**Weak version (and why it fails):** "No, I did it myself" when you did not, or "It was mostly AI, I just ran it." The first is dishonest and gets exposed by a simple follow-up question; the second shows no ownership or checking.

**What the interviewer scores:**
- Honesty and a calm tone.
- Awareness that policy and data rules exist and that you check them.
- Evidence of verification, not trust.
- Ownership of the final work.
- Ability to explain the work well enough that it is clearly yours.

**Make it yours:**
- Write down how you really use AI tools in analysis today, task by task.
- For each, note what you check before you trust it.
- Find your employer's or school's guidance and read it; if there is none, note that you would ask.
- Prepare a two-sentence honest answer. Do not use AI to write your story; follow-ups on a rehearsed or AI-written answer expose it quickly.

**Script (copy and adapt):**
```
"I used [tool] for [specific task]. I did [analysis steps] myself and
checked [numbers/queries/results] against [source]. I own the
conclusions. I did not share [type of data] with the tool. Here is how
to reproduce it: [link]. Is there a policy I should follow for notes?"
```

**Follow-ups:**
- What if there is no policy? "I ask my manager what is expected and write down what we agree."
- Would you use it again? "Yes, for drafting, with the same checks."
- How do you know it did not make an error? "I do not assume; I verify numbers against the source and review the logic."

**Common mistakes:**
- Denying or hiding use.
- Over-claiming credit for what the tool did.
- Pasting sensitive data into a tool without checking the rules.
- Being unable to explain the work.
- Treating policy as someone else's problem.

### Q47 ⭐ 🔴 You have one result that must go to executives, engineers and operations staff. How do you tailor it for each group without changing the facts?
**Asked at:** Data storytelling and analyst question pages (Adaface and Yardstick data-storytelling lists, a Dataford page on presenting findings to leadership, a Loopcv sample structure of what is happening, why it matters and what to recommend; Interview Query lists a take-home that asks for a summary for a marketing vice president); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** The facts stay the same for everyone; I change the order, the depth and the vocabulary: decision and impact for executives, method and limits for engineers, and what to do on Monday for operations.

**Structure:** One core, three views (editor guidance [G]; the pattern section "A pattern for explaining anything to a non-technical person" above applies).
1. Write the core: the finding, the number, the uncertainty, the main caveat. These sentences are identical in every version.
2. Executives: decision first, business impact, risk, ask. One page or one slide.
3. Engineers: data, method, validation, assumptions, failure modes, links to code and the full write-up.
4. Operations: what changes for their work, what to do, what to watch, who to call, a short example.
5. Check consistency: put the three versions side by side and confirm the numbers and caveats match.
6. Say where the other versions are, so nobody feels they got a different story.

**Strong sample answer (spoken):** Illustrative; replace with your own. "Say the result is that late deliveries drop when we use the new routing, with a range we are fairly sure of. For executives I would lead with the decision: roll it out to two depots, expected effect, risk and the cost. For engineers I would start with the data and method, how we validated and where it could break, and link the code. For operations I would say what changes on the shift: which routes the system suggests, when to override and who to tell. The core sentences, including the range and the main caveat, are the same in all three. Before sending, I would check the three side by side to be sure the numbers match."

**Weak version (and why it fails):** Sending the same long report to everyone, or softening the caveat for executives and hiding the limits from operations. One audience is lost and another is misled, and when the versions meet in a meeting, trust drops.

**What the interviewer scores:**
- Audience analysis: you know what each group needs.
- Integrity: facts, numbers and caveats stay constant.
- Structure and economy in each version.
- Planning for consistency across versions.
- Awareness of who acts and how.

**Make it yours:**
- Take a real result you produced and write the core in four sentences.
- Draft the executive, engineering and operations versions using that core.
- Highlight the sentences that must be identical.
- Ask a person from one of the groups what you missed.

**Follow-ups:**
- What if executives ask for fewer caveats? "I keep the main one and offer the rest in the appendix; I do not drop what could change the decision."
- What if two groups disagree? "I point back to the shared core and bring them together."
- How do you check accuracy? "I read the versions side by side and have a technical colleague review."

**Common mistakes:**
- Telling each audience a slightly different story.
- Dropping caveats for the senior audience.
- Giving operations a method lecture instead of actions.
- Overloading executives with detail.
- Sending versions at different times without cross-links.

### Q48 ⭐ 🔴 The CFO wants a single number from your forecast. How do you communicate the range, and what do you do if they insist on one number?
**Asked at:** Public statistics question banks list explain-a-p-value and explain-a-confidence-interval prompts for lay audiences (an Interview Query p-value page, a TryExponent confidence-interval page, Dataford statistics lists); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I would give the CFO a point estimate with a range and what drives it, and if they still need one number I would give the planning figure, say what it is and what it is not, and say what would make me change it.

**Structure:** Number, range, drivers, decision (editor guidance [G]).
1. Lead with the answer: "My best estimate is [X]; I would plan between [low] and [high]."
2. Say how sure: how often reality has landed inside such ranges in past forecasts, or "wider because we have little history".
3. Name the two or three drivers that move it, and which one to watch.
4. Tie the range to the decision: what changes if it lands high, and low (a buffer, a trigger).
5. If they insist on one number: give the one that suits the decision (often the central estimate, or a cautious one for budgets), label it a planning figure, and commit to a review date and a trigger for revising it.
Do not invent false precision, and do not refuse to answer.

**Strong sample answer (spoken):** Illustrative; replace with your own. "My best single estimate is [X]. I would plan on a range of [low] to [high], because demand in the last two quarters moved more than usual. The two things that move it most are the renewal rate and the new-customer pipeline. If you need one figure for the budget, use [X], and treat it as a planning number, not a promise. I would set a buffer for the low case and a trigger: if renewals fall below [threshold] by month two, I will update you. I would rather give you the range and a plan for it than a single number that looks more certain than it is."

**Weak version (and why it fails):** "It is impossible to give one number" with a lecture on uncertainty, or a single precise number with no range. The first looks unhelpful and the second looks confident and then misleads when reality lands elsewhere.

**What the interviewer scores:**
- A direct answer: you give a number.
- Honest uncertainty in plain words, tied to a decision.
- Knowing what drives the forecast.
- Flexibility under pressure without losing integrity.
- A follow-up trigger and review.

**Make it yours:**
- Take a real forecast or estimate you made and write its central value and range using placeholders until you fill in your own.
- Name its two main drivers.
- Decide which single number you would hand over if forced, and why.
- Write the trigger you would use to revisit it.
- For a stakeholder-pressure scenario with numbers, see Book 6 Part 6; this answer is the communication version.

**Script (copy and adapt):**
```
"Best estimate: [X]. Plan for [low] to [high].
It moves most with [driver 1] and [driver 2].
If you need one number for the budget, use [X] as a planning figure.
I will review it on [date], or earlier if [trigger]."
```

**Follow-ups:**
- Why not just give the average? "I do, as the central estimate, but the range shows the risk around it."
- What if the CFO says ranges are useless? "I show the cost of the high and low cases, so the range becomes a plan."
- How do you know the range is good? "I check how past forecasts compared with outcomes."

**Common mistakes:**
- Refusing to give any number.
- Giving false precision.
- Burying the number under statistics.
- Using words like "confidence interval" without explaining them.
- Not saying when you will revise it.

### Q49 ⭐ 🔴 An LLM feature gave a customer a confidently wrong answer and it became a public complaint. How do you explain what happened to executives?
**Asked at:** Vendor and explainer pages on LLM hallucination in business (Kili, Glean, DataRobot and similar, which are marketing material, not interview lists); no interview question list found for the exact prompt, so it is editor-designed; search snippets only, not opened
**Say this first (1 line):** I would tell executives plainly what happened, that the model predicts plausible text and can be fluent and wrong, what we did for this customer, and what we are changing, without blaming a person or hiding behind jargon.

**Structure:** Facts, cause, impact, fix (editor guidance [G]; use the pattern section "A pattern for explaining anything to a non-technical person" above).
1. What happened in two sentences: the question, the wrong answer, who saw it, when.
2. Why, in plain words: a language model writes the most plausible answer from patterns; it does not look up or verify facts unless we give it a source and check.
3. What we did already: contacted the customer, corrected the record, limited or paused the feature if needed.
4. What it exposed: which control was missing (no source grounding, no confidence handling, no human check for high-stakes answers).
5. What changes: grounding in approved content, topic limits, a way to say "I do not know", testing on known risky questions, monitoring and an escalation path.
6. What we do not yet know, and when the next update comes.

**Strong sample answer (spoken):** Illustrative; replace with your own. "Here is what happened. A customer asked about our refund terms and the assistant answered confidently with a policy we do not have. The cause is how these systems work: they generate likely-sounding text and do not check facts unless we connect them to approved sources and test them. We have contacted the customer, corrected the answer and tightened the feature for pricing and refund questions. What this exposed is that we had no check for high-stakes topics. We are adding answers drawn only from our policy pages, a clear fallback when it is unsure, and a regular review of real conversations. We are still checking how many similar answers went out, and I will update you by Friday."

**Weak version (and why it fails):** "The AI hallucinated; it is a known limitation." It sounds like an excuse, offers no fix and ignores the customer. Blaming an individual or the vendor outright is just as poor.

**What the interviewer scores:**
- Plain explanation of why LLMs produce confident errors.
- Calm, honest tone under pressure.
- Ownership and a concrete action plan.
- Distinction between the immediate fix and the systemic fix.
- Candour about what is still unknown.

**Make it yours:**
- Recall a real incident with any model or system (not necessarily an LLM) where a confident output was wrong.
- Write its facts, cause, impact and fix in four lines, using only what is true.
- If you have none, write how you would explain a test failure you found in an LLM prototype.
- Practise saying the cause without jargon.
- Check how your employer handles customer-facing incidents; this book gives no policy or legal advice.

**Follow-ups:**
- Can this be eliminated? "Not fully; we reduce it with grounding, limits and checks, and match human review to the cost of an error."
- Should we turn it off? "For high-stakes topics, until the controls are in; for others, with monitoring."
- Who is to blame? "The gap was in our controls, so that is what we fix."

**Common mistakes:**
- Calling it a glitch or blaming the technology.
- Naming a colleague as the cause.
- Promising it will never happen again.
- Over-explaining how transformers work.
- Skipping the customer-facing steps.

### Q50 ⭐ 🔴 A colleague sends you an AI-written analysis for review. What do you check, and how do you word your feedback so they learn from it?
**Asked at:** 2026 AI-era guides (a PrachHub prompt on describing an analysis where you used AI responsibly, Dataford questions on explaining AI concepts to business stakeholders, a Gartner session title on explaining AI and ML models to stakeholders); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I would check the question, the data, the numbers and the conclusions as if a junior colleague wrote it, rerun the key steps myself, and word my feedback about the work, with specific examples and one thing to try next time.

**Structure:** Check in layers, then give feedback in a fixed shape (editor guidance [G]).
1. Question: does the analysis answer what was asked, and are the assumptions stated?
2. Data: sources real and correct, filters and joins sensible, no leakage, nothing made up.
3. Numbers: rerun the key query or calculation, compare totals with a source, check sample sizes and outliers.
4. Method: is the test or model suitable, is uncertainty shown, are claims causal without support?
5. Conclusions and wording: does the evidence support each claim, are any references or figures invented?
6. Feedback: what is good, what is wrong with evidence, why it matters, one next step, and an offer to pair. Ask how they produced it and what they checked, with curiosity, not suspicion.
Follow your team's rules on AI use; they differ by employer.

**Strong sample answer (spoken):** Illustrative; replace with your own. "First I would reproduce the main number from the source myself. Then I would look for the usual weak spots: filters that quietly drop rows, a metric defined differently from ours, a causal claim with no support, and any figure or citation I cannot trace. When I give feedback I would say: 'The structure is clear and the summary is useful. I could not reproduce the conversion figure; I get a different total when I include returning customers, so we should check the definition. The claim that the campaign caused the rise needs a comparison group. Could you add how you checked the numbers? Happy to go through it together.' I would be specific, not say 'AI makes mistakes', and make clear that the author owns the result."

**Weak version (and why it fails):** Approving it because it reads well, or rejecting it with "this is just AI rubbish". The first lets errors through; the second teaches nothing and damages the relationship.

**What the interviewer scores:**
- A systematic review order, not a vague skim.
- Independent reproduction of key numbers.
- Awareness of typical failure modes of AI-written analysis.
- Constructive, specific, respectful feedback.
- Focus on accountability and learning.

**Make it yours:**
- Take a real piece of analysis (yours, a colleague's or an AI draft) and review it using the six layers.
- Write down two things you could not verify and how you would check them.
- Draft your feedback in the shape above, with one example and one suggestion.
- Notice which checks you usually skip.

**Follow-ups:**
- What if they say the AI did it, not them? "The author still owns the result, so we check it together."
- What if you cannot tell if AI was used? "It does not change the review: I check the evidence, and I ask how it was produced."
- How much time do you spend? "Proportional to the stakes: more for a number that drives a decision."

**Common mistakes:**
- Trusting polished writing.
- Reviewing only the text and not the data and numbers.
- Making the feedback about the tool or the person.
- Vague comments with no examples.
- Not rerunning anything.
