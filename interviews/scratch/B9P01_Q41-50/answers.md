### Q41 ⭐ 🟢 Junior level: tell me about a time you were stuck. How long did you try on your own, when did you ask for help, and who did you ask?
**Asked at:** Level-specific behavioural guidance (Taro level-specific expectations, a Towards Data Science data scientist hierarchy piece, an Interview Kickstart senior data scientist guide, a MentorCruise senior and staff story workshop page, which is promotional); level framing in public guides is opinion, not a company rubric; Book 7 Part 1 notes the Meta and Microsoft level evidence with caveats; search snippets only, not opened
**Say this first (1 line):** I tried on my own for a set amount of time, wrote down what I had tried, then asked the right person a specific question.

**Structure:** Use CARL (Learning matters here); see "STAR and CARL" at the top of this part and the Entry / junior column of the level table.
- Context: what you were stuck on and the deadline, one sentence.
- Action: how long you tried alone and what you tried; how you decided it was time to ask; who you asked and why that person; the exact question you brought.
- Result: unblocked, how long it took, what you delivered.
- Learning: the rule you now use for when to ask (for example, a time limit).

**Strong sample answer (spoken):** (illustrative; replace with your own)
"I was building a churn feature pipeline and my join kept dropping about [some] rows. I gave myself a rule: [timebox] on my own first. In that time I checked the keys, compared row counts at each step and wrote the checks down. Then I messaged the engineer who owned the source table. I did not say 'it's broken'. I sent my query, the counts at each step and my guess, which was duplicate IDs after a migration. She confirmed it in a few minutes and pointed me to the dedup view. I finished that day. What I took from it: I now write the question before I ask, and half the time writing it solves it. When it does not, the person can answer in one reply. I also add a note to the pipeline README so the next person skips the same trap."

**Weak version (and why it fails):** "I was stuck for three days and then my manager helped me." No timebox, no attempts, no named help, no learning. It also hides how you decide. The opposite failure is "I never ask for help", which reads as risky for a junior.

**What the interviewer scores:**
- Self-reliance first: you tried real things and can list them.
- Good judgement on when to escalate, not too early and not too late.
- A clear, specific ask that respects the other person's time.
- Honest account of what you did not know.
- Learning you applied afterwards.

**Make it yours:**
- Pick one real moment you were blocked, even a small one.
- Write down how long you tried and what you tried, from your notes or chat history.
- Name who you asked and what you sent them.
- State what you do differently now, only if it is true.
- Keep numbers you can defend.

**Follow-ups:**
- "What if the person had been busy?" Say what you would do: post the written question in the team channel, or ask a second person, and keep working on a different part meanwhile.
- "Did you ever ask too soon?" Give one honest example and the rule you changed.

**Common mistakes:** No timebox. A story where someone else fixed everything. Saying "I never get stuck". Skipping what you learned. AI note: if you used an AI tool while stuck, say so plainly and say how you checked its answer; do not use AI to write the story, because follow-ups on the details will show it.

### Q42 ⭐ 🟡 Mid level: tell me about a project you owned from problem definition to delivery with little supervision. What decisions were yours?
**Asked at:** Level-specific behavioural guidance (Taro level-specific expectations, a Towards Data Science data scientist hierarchy piece, an Interview Kickstart senior data scientist guide, a MentorCruise senior and staff story workshop page, which is promotional); level framing in public guides is opinion, not a company rubric; Book 7 Part 1 notes the Meta and Microsoft level evidence with caveats; search snippets only, not opened
**Say this first (1 line):** I will walk through one project where I defined the problem, made the key decisions and delivered, and say which decisions were mine.

**Structure:** Use STAR (a longer project needs the set-up); see "STAR and CARL" and the Mid column of the level table in this part.
- Situation and Task: the vague request and what you took ownership of.
- Action: how you turned it into a clear question and success measure; two or three decisions with the alternative you rejected; how you kept people informed without being chased.
- Result: what shipped, how it was measured, what did not work.
- Learning (one line): what you would change.

**Strong sample answer (spoken):** (illustrative; replace with your own)
"A team lead said support tickets were 'taking too long'. That was the whole brief. I owned it from there. First I asked what 'too long' meant and agreed one measure with her: [time-to-first-response]. Three decisions were mine. I chose a simple ranking model over a language model, because the team needed something they could debug. I chose to ship to one queue first. And I decided to drop a feature that was hard to compute live. I sent a short update every [week] without being asked. The queue's measure improved by [a number I can show], though one ticket type got worse and I said so. Afterwards I wrote down the assumptions, so the next owner could pick it up. If I did it again I would agree the rollout check earlier."

**Weak version (and why it fails):** "We built a model and the team was happy." No problem definition, no personal decisions, no result. It sounds like a task, not ownership.

**What the interviewer scores:**
- You turned a vague ask into a testable problem.
- Clear decisions that were yours, with trade-offs.
- Little need for supervision, but you kept stakeholders informed.
- A measured result, including what fell short.
- Level fit: "I owned X and made these decisions".

**Make it yours:**
- Choose a project where you really owned the outcome.
- List three decisions you made and the alternative for each.
- Find the real measure and where it came from.
- Name one thing that fell short.
- Separate your work from the team's.

**Follow-ups:**
- "Who disagreed with you?" Name the person's concern and what evidence settled it.
- "What was the riskiest assumption?" Name it and how you checked it.

**Common mistakes:** Using "we" for everything. Describing tools, not decisions. No success measure. Claiming a result you cannot explain. AI note: live follow-ups on the details are how a rehearsed or AI-written story is found out.

### Q43 ⭐ 🟡 Mid level: tell me about a time you pushed back on a request from a more senior person and what came of it.
**Asked at:** Level-specific behavioural guidance (Taro level-specific expectations, a Towards Data Science data scientist hierarchy piece, an Interview Kickstart senior data scientist guide, a MentorCruise senior and staff story workshop page, which is promotional); level framing in public guides is opinion, not a company rubric; Book 7 Part 1 notes the Meta and Microsoft level evidence with caveats; search snippets only, not opened
**Say this first (1 line):** I disagreed respectfully, brought evidence and an alternative, and then supported the final decision.

**Structure:** Use STAR; see "STAR and CARL" at the top of this part. For data-science trade-off pushback with numbers, see Book 6 Part 6 (Stakeholder Conflicts and Trade-off Decisions) instead of repeating it here.
- Situation and Task: who asked for what and why you had a concern.
- Action: how you checked your concern first; how and where you raised it (privately, with data); the alternative you offered; how you handled "no".
- Result: what was decided, what happened, and what you learned.

**Strong sample answer (spoken):** (illustrative; replace with your own)
"A director asked me to present a model's headline score to the board by Friday. I had checked it and saw that the test data overlapped with training. So the score was too optimistic. I did not say no in the meeting. I booked ten minutes with her and brought one chart: the score with and without the overlap. I said, 'I want this to hold up when someone asks. Here is a fix that takes [a short time]'. She agreed to a one-day delay and a note about the method. The corrected score was lower but defensible. A board member did ask how we tested it, and she could answer. I learned to bring the evidence and a way forward together, not just the concern. If she had said no, I would have asked for the caveat in writing and then helped deliver it."

**Weak version (and why it fails):** "I told my VP the request was wrong and refused." Or the other extreme: "I just did what I was told." The first shows no judgement about how to disagree; the second shows no spine.

**What the interviewer scores:**
- Evidence before opinion.
- Timing and tone: private, specific, respectful.
- An alternative, not just an objection.
- Commitment once the decision is made.
- Honest outcome, even if you lost.

**Make it yours:**
- Pick a real case where you disagreed with someone senior.
- Write the evidence you brought.
- Say what you proposed instead.
- Say what was decided, even if it was not your way.
- Note what you would do differently.

**Follow-ups:**
- "What if they overruled you?" I would ask to record my concern, deliver the decision well, and watch the risk I flagged.
- "Would you escalate?" Only for real harm, after talking to them first, and I would say so openly.

**Common mistakes:** Making the senior person the villain. Pushing back in public. No alternative. A story where you were simply right and everyone agreed.

### Q44 ⭐ 🟡 A teammate relied heavily on AI-generated code or analysis and it contained errors. Tell me about a time something like this happened and how you handled it.
**Asked at:** 2026 AI-era behavioural guides (TheInterviewGuys, TechInterview.org, Tredence, PrachHub and FacePrep pages list daily AI-tool use, catching AI mistakes and judgement on when to use AI; PrachHub attributes one set to Amazon engineering loops, which is secondhand); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I check AI output like any colleague's work, so when a teammate's AI-assisted work had errors, I helped fix it and agreed a review habit without blaming them.

**Structure:** Use STAR or CARL; see "STAR and CARL" at the top of this part. This is editor guidance [G]; do not claim a company policy.
- Situation: what the AI-assisted work was and who relied on it.
- Task: your role (reviewer, teammate, owner of the result).
- Action: how you spotted the problem; how you raised it kindly; how you fixed it; what review step you suggested.
- Result and Learning: the impact avoided or limited, and the team habit that came out of it.

**Strong sample answer (spoken):** (illustrative; replace with your own)
"A teammate sent me an analysis that an AI assistant had helped draft. One chart looked too clean. I re-ran the query myself and found the code had filtered out a segment without saying so. I did not say 'the AI got it wrong'. I messaged him privately: 'I get a different total when I include this segment. Can we look together?' We found the bug in ten minutes, and he fixed the chart before it went to the product team. Afterwards we agreed on three things: re-run the key numbers independently, read AI-written code line by line, and note in the doc where AI was used. I use AI tools too, so this was not about blame. The lesson for me is that the person who sends the work owns the result, whoever or whatever drafted it."

**Weak version (and why it fails):** "AI code is unreliable, so I told him to stop using it." That ignores your own use, blames the tool and misses the process fix. "I fixed it quietly myself" also fails: the teammate learns nothing.

**What the interviewer scores:**
- You verify instead of trusting output.
- Kind, specific feedback that keeps the relationship.
- Ownership of results regardless of the tool.
- A practical team habit, not a ban.
- Honest, balanced view of AI tools.

**Make it yours:**
- Use a real case; if you have none, describe a similar one with human-written work, or say what you would do. Do not invent one.
- Say what you checked and how.
- Describe how you spoke to the person.
- Name the habit you or the team adopted.
- Say how you use AI yourself and how you disclose it.

**Follow-ups:**
- "What if it had already shipped?" Tell the owner, assess the impact, fix forward, and write down what check would have caught it.
- "When do you not use AI?" For work where I cannot verify the answer, or where the data is sensitive and the policy says no; ask the team what the policy is.

**Common mistakes:** Blaming the person or the tool. Hiding your own AI use. A story with no checking step. AI note: do not use AI to write this story; follow-ups on details will show if it is not yours.

### Q45 ⭐ 🟡 You moved into data, ML or GenAI work from another field or role. Tell me why you made that move and what you did to close the gaps.
**Asked at:** No public page found for this exact framing, editor-designed; the theme is adjacent to prompts in general behavioural guides; search snippets only, not opened
**Say this first (1 line):** I moved because of a real pull toward the work, and I closed the gaps with a specific plan and evidence you can check.

**Structure:** Use CARL; see "STAR and CARL" at the top of this part. This is a career-story question rather than an incident.
- Context: what you did before, and the moment you noticed the pull toward data, ML or GenAI.
- Action: the gaps you named; what you did about each (courses, projects, work tasks, a mentor); how you tested yourself.
- Result: what you can do now, shown by something concrete.
- Learning: what your earlier field gives you and what you are still building.

**Strong sample answer (spoken):** (illustrative; replace with your own)
"I spent [some years] in [your earlier field]. I kept ending up as the person who built the spreadsheets and dashboards, and I enjoyed the questions more than the reports. So I made a plan. I listed the gaps honestly: statistics, Python at work scale and modelling. For each one I picked something practical. I took [a course], then used it on a real problem from my old job, and I built [a project] and asked a data scientist to review it. That review taught me more than the course did. Now I can [what you can really do]. I am still building [one honest gap]. What I bring from my earlier field is that I understand how the business uses the numbers, and I think that helps me ask better questions."

**Weak version (and why it fails):** "Data science is the hot field and pays well." That shows no real interest. Another weak version: hiding the move or saying "I have no gaps".

**What the interviewer scores:**
- A genuine, specific reason for the move.
- Honest awareness of gaps.
- A plan you carried out, not a list of courses.
- Evidence of ability, such as work you can show.
- How your past field adds value.

**Make it yours:**
- Write your real reason for moving, in two sentences.
- List your real gaps and what closed each.
- Pick one piece of work you can show or explain in depth.
- Name the gap still open.
- Link your earlier field to this role honestly.

**Follow-ups:**
- "Why not stay in your old field?" Give the honest pull, without criticising your old field.
- "What is still weakest?" Name one and your current plan.

**Common mistakes:** Talking about pay or trends. Listing certificates only. Running down the previous field. Claiming skills you cannot show. AI note: you may have used AI to learn; say how you checked what it taught you.

### Q46 ⭐ 🔴 Senior level: tell me about a time you set the technical direction for a team and had to bring sceptical people along.
**Asked at:** Senior and staff behavioural guidance (a MentorCruise senior and staff workshop page and an Interview Kickstart senior guide describe mentoring, prioritisation and influence stories; promotional or prep-site material); no public rubric found; editor-designed framing; search snippets only, not opened
**Say this first (1 line):** I set a direction by laying out the options and evidence, listening to the sceptics first, and testing the risky part with a small pilot.

**Structure:** Use STAR with a decision in the Action; see "STAR and CARL" and the Senior column of the level table in this part (the pitch is "I decided X, aligned people and handled the fall-out").
- Situation and Task: the team, the choice, why it was contested.
- Action: the options you compared; who was sceptical and why; how you listened and changed the plan; the pilot or evidence you used; how you documented the decision.
- Result: what the team did, how it turned out, what was costly.
- Learning.

**Strong sample answer (spoken):** (illustrative; replace with your own)
"Our team had three ways to build [a system], and half the team wanted to keep the old one. I was asked to set the direction. First I spoke to each sceptic alone and asked what would make them wrong. One engineer worried about on-call load. I wrote a short options doc with the costs of each path, including the ones against my preference. We ran a [short] pilot on one use case, with success measures agreed beforehand. The pilot supported the new approach but showed the on-call worry was fair, so I changed the plan to include a runbook and a rollback step. The team moved over in stages. One person still disagreed, and I said so in the doc. What I learned is that a sceptic's concern often improves the plan."

**Weak version (and why it fails):** "I decided, explained why, and everyone followed." No sceptics, no trade-off, no cost. It sounds like authority, not influence, and no one will believe it.

**What the interviewer scores:**
- Real decision, with options and trade-offs.
- You listened to sceptics and changed something.
- Evidence and a low-risk test over argument.
- Written record that others can build on.
- Honest about costs and leftover disagreement.

**Make it yours:**
- Pick a decision where people really disagreed.
- Write each sceptic's concern in their words.
- Note what changed because of them.
- Find your evidence or pilot result.
- Include one thing that went badly.

**Follow-ups:**
- "What if the pilot had failed?" I would have said so and either changed course or stopped.
- "How did you keep the sceptic on board?" Gave them a role in the review of the pilot.

**Common mistakes:** No named sceptic. Calling the decision "obvious". Skipping costs. Using "we" to hide that you did not decide. AI note: rehearsed or AI-written leadership stories collapse on "who disagreed and what did you change".

### Q47 ⭐ 🔴 Senior level: tell me about how you have grown other people's skills across a team, beyond one-to-one mentoring.
**Asked at:** Senior and staff behavioural guidance (a MentorCruise senior and staff workshop page and an Interview Kickstart senior guide describe mentoring, prioritisation and influence stories; promotional or prep-site material); no public rubric found; editor-designed framing; search snippets only, not opened
**Say this first (1 line):** I built things that keep teaching after I leave the room: reviews, shared standards and a growth path for people, not just one-to-one help.

**Structure:** Use STAR; see "STAR and CARL" and the Senior column of the level table in this part (mentors openly, sets direction).
- Situation and Task: the team skill gap or uneven quality.
- Action: the mechanism you built (review habit, guide, pairing rota, shared examples); how you got buy-in; how you checked it worked.
- Result: changes you can point to in people's work or in team practice, and what did not land.
- Learning.

**Strong sample answer (spoken):** (illustrative; replace with your own)
"On my team, model reviews were uneven. Some people got deep feedback and others got none, so quality depended on who you sat near. Mentoring one by one would not fix that. I proposed a short review checklist, and I wrote it with two teammates so it was not just mine. I ran the first few reviews in the open, so people could see what good feedback looked like. Then I moved to a rota where everyone reviewed and was reviewed. After [a few months] I looked at what changed. Reviews were happening on most projects, and [a measure you can show] improved. Two people said they had started reviewing others' work with confidence. One part failed: the written guide was rarely read, so I replaced it with worked examples."

**Weak version (and why it fails):** "I mentor three juniors and answer their questions." That is one-to-one help only, with no mechanism and no result.

**What the interviewer scores:**
- Scaling yourself beyond individual help.
- A mechanism others own, not dependence on you.
- Evidence it worked, and honesty about what did not.
- Care for people's growth, not just output.
- Senior-level scope.

**Make it yours:**
- Pick something you really set up: a review habit, doc, talk, rota.
- Say who it helped and how you know.
- Include what you tried that did not land.
- Credit the teammates who helped.
- Keep claims to what you can show.

**Follow-ups:**
- "How did you handle someone who did not want feedback?" Ask what they want to get better at, and start there.
- "How do you measure it?" Behaviour change and quality of work, not attendance.

**Common mistakes:** Only one-to-one stories. Claiming team results you did not drive. No evidence. Taking all the credit.

### Q48 ⭐ 🔴 Staff level: tell me about a time you influenced a decision across several teams that did not report to you, with no formal authority.
**Asked at:** Senior and staff behavioural guidance (a MentorCruise senior and staff workshop page and an Interview Kickstart senior guide describe mentoring, prioritisation and influence stories; promotional or prep-site material); no public rubric found; editor-designed framing; search snippets only, not opened
**Say this first (1 line):** I had no authority, so I used a shared problem, evidence and each team's own goals to get a decision.

**Structure:** Use STAR; see "STAR and CARL" and the Staff / principal column of the level table in this part ("I changed how several teams do X"). Level framing is editor judgement [G].
- Situation and Task: the cross-team problem and why nobody owned it.
- Action: how you framed it in each team's terms; who you talked to first; the document or data that made the case; how you handled the team that lost out.
- Result: the decision, how it was adopted, what it cost.
- Learning.

**Strong sample answer (spoken):** (illustrative; replace with your own)
"Three teams each kept their own definition of [a key metric], and leadership kept seeing different numbers. No one owned it. I started by asking each team lead what the numbers were used for. I found their needs overlapped more than they thought. I wrote a short proposal with one shared definition and an exception for one team, and I showed what each team's number would have been under it. I met each lead before the group meeting, so nobody was surprised. One team lost a convenience, so I offered to do the migration work for them. The three teams agreed, and the shared definition went live [in a few weeks]. Later two other teams adopted it too. What I learned is that you win on the shared problem, not on the argument."

**Weak version (and why it fails):** "I got my manager to tell the other teams to do it." That is borrowed authority, not influence. Or "I convinced everyone because I was right", with no listening and no cost.

**What the interviewer scores:**
- Reading each team's incentives.
- Evidence and a written proposal others can use.
- Pre-meetings and no surprises.
- Care for who loses, with a concrete offer.
- Scope across teams, with a lasting outcome.

**Make it yours:**
- Pick a real cross-team decision you influenced.
- List the teams and what each wanted.
- Write the one document or analysis that moved things.
- Note who lost and what you did for them.
- Say what lasted.

**Follow-ups:**
- "What if a team had refused?" Escalate only after trying again with their concern addressed, and tell them first.
- "What did you personally give up?" Name your time or a preference.

**Common mistakes:** Borrowing a manager's authority. One team's view only. Skipping the cost. Over-claiming scope you did not have.

### Q49 ⭐ 🔴 Staff level: tell me about a time you stopped or cut back a long-running project or programme. How did you decide and how did you communicate it?
**Asked at:** Senior and staff behavioural guidance (a MentorCruise senior and staff workshop page and an Interview Kickstart senior guide describe mentoring, prioritisation and influence stories; promotional or prep-site material); no public rubric found; editor-designed framing; search snippets only, not opened
**Say this first (1 line):** I stopped it because the evidence no longer supported the cost, and I told everyone early, openly and with respect for the people who built it.

**Structure:** Use CARL (Learning matters); see "STAR and CARL" and the Staff / principal column of the level table in this part ("decides what not to do").
- Context: the programme, how long it had run, why it was hard to question.
- Action: the criteria you used; the evidence; the options (stop, shrink, change); who you consulted; how you announced it and what you did for the team.
- Result: what was freed up, reaction, what you would do differently.
- Learning.

**Strong sample answer (spoken):** (illustrative; replace with your own)
"A programme had been running for [over a year] to build [a platform]. Usage had stayed flat and maintenance was taking a third of the team. I did not want to decide from a feeling, so I wrote down three questions: who uses it, what does it cost, what else could that time do? The data showed [a small number of] real users. I talked to the owner first, before anyone else, and I took her objections seriously. We agreed to wind down in stages, keep the one feature people did use, and move the rest of the team to [a new priority]. I told the wider group with a short note that said what we learned and thanked the builders by name. Some people were upset, and I did not hide that. I now set stop criteria at the start of programmes."

**Weak version (and why it fails):** "It was a waste, so I killed it." That shows no process, no people care and a risk of blame. Another weak version is a story where you quietly let it fade.

**What the interviewer scores:**
- Clear criteria and evidence, not a gut call.
- Willingness to stop something sunk-cost heavy.
- Talking to the owner first, then communicating widely.
- Care for the people and for what is worth keeping.
- Learning that changes how you start work.

**Make it yours:**
- Use a real project you stopped or cut back; if none, a smaller real example, and say its size.
- Write the criteria you used.
- Describe how you told the owner and the team.
- Note the effect on people and what happened to their work.
- Say what you changed afterwards.

**Follow-ups:**
- "What if you had been wrong?" I wrote down what would change my mind and reviewed it at a set date.
- "Who pushed back most?" Name the concern, and what you did about it.

**Common mistakes:** Blaming predecessors. Announcing by surprise. No evidence. Pretending it was easy.

### Q50 ⭐ 🔴 Staff level: tell me about a time you defined a strategy or roadmap for an area that was ambiguous, and how you decided what not to work on.
**Asked at:** Senior and staff behavioural guidance (a MentorCruise senior and staff workshop page and an Interview Kickstart senior guide describe mentoring, prioritisation and influence stories; promotional or prep-site material); no public rubric found; editor-designed framing; search snippets only, not opened
**Say this first (1 line):** I made the ambiguity smaller by naming the options and criteria, chose a direction with the team, and wrote down what we would not do and why.

**Structure:** Use STAR; see "STAR and CARL" and the Staff / principal column of the level table in this part ("decides what not to do"). Level framing is editor judgement [G].
- Situation and Task: the area, why it was unclear, who needed a plan.
- Action: how you gathered inputs; the criteria you ranked by; what you chose and what you cut; how you shared it and kept it revisable.
- Result: what was built, what the "not now" list protected, how the plan changed.
- Learning.

**Strong sample answer (spoken):** (illustrative; replace with your own)
"I was asked to set a roadmap for [an area] that had no owner and ten requests from different teams. I interviewed the main users and listed the requests against three criteria: value to the business, how sure we were, and effort. That gave me a short list of two bets and a long list we would not do this year. The 'not now' list was the hard part, so I wrote the reason beside each item and met the requesters in person before publishing. Two were unhappy, but they could see the logic. I set a review date, and at the review I changed one bet because the data had moved. The team shipped [the first bet] and stayed out of firefighting for [that period]. I learned that a roadmap people trust has an honest list of what is off it."

**Weak version (and why it fails):** "I made a roadmap with everything on it so everyone was happy." No priorities, no cuts. A strategy that says yes to everything is not a strategy.

**What the interviewer scores:**
- Structuring ambiguity with criteria.
- Willingness to say no, with reasons.
- Talking to the people affected before publishing.
- Revising the plan when evidence changes.
- Outcomes beyond one team.

**Make it yours:**
- Pick a real plan you defined; it can be smaller than a company strategy.
- Write your criteria and the items you cut.
- Describe how you told people no.
- Say what changed at the first review.
- State what you would do differently.

**Follow-ups:**
- "How did you know it was the right call?" Say what you measured and what you would not claim.
- "What did you cut that you regret?" Give one honest example.

**Common mistakes:** A plan with no cuts. Inflated scope. No evidence. Omitting the people who were told no.
