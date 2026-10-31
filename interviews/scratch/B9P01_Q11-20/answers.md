### Q11 ⭐⭐⭐ 🟡 Tell me about a time you worked closely with engineers or product managers to ship something. What did each side need from you?
**Asked at:** Public data science behavioural guides (an Analytics Vidhya list and a Coursera guide frame stakeholder, explanation and business-decision stories; a KDNuggets piece says the technical reasoning should stay visible inside the story); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I treat engineers and product managers as two different customers: engineers need a clear, testable spec from me, and product managers need a decision they can explain.

**Structure:** Use STAR (see "STAR and CARL" above). Put most of the time on Action.
- Situation and Task: the feature, who was on the team, and your specific part.
- Action: what the engineers needed (input and output format, latency, a way to test, how failures show up) and what the product manager needed (a plain-language trade-off, a date, a success metric). Say how you worked with each side, for example a short written spec, a shared test set, a weekly check-in.
- Result: shipped or not, the metric, and one thing that went wrong.
- Learning: one working habit you kept.

**Strong sample answer (spoken):** Illustrative; replace with your own. "We were shipping a ranking model inside an existing product. My task was the model and its handoff. The engineers needed a fixed input format, a response time budget and a small test set they could run without me. The product manager needed to know what quality we could promise and what we would give up to hit the date. I wrote a one-page spec for the engineers, and a three-line summary of options for the PM. When the model was slower than the budget, I brought both groups together and we agreed on a smaller model for launch. It shipped on the planned date, and we kept the larger model as a follow-up. Looking back, I would have agreed the test set earlier, because we lost two days arguing about what 'working' meant."

**Weak version (and why it fails):** "I built the model and handed it to the engineers, and the PM was happy." It has no detail on what each side needed, no friction, no decisions, and it hides your own part. The interviewer cannot tell whether you worked with them or just threw work over a wall.

**What the interviewer scores:**
- Do you understand what each partner needs, in their terms?
- Did you adapt how you communicate for each side?
- Can you handle a trade-off (speed, quality, date) openly?
- Did you own the handoff, not only the model?
- Is the technical reasoning visible inside the story?

**Make it yours:**
- Pick a real project that shipped, even a small one. Name your exact role.
- Write one line on what the engineers needed and one on what the product manager needed, from what you actually saw.
- Find the moment of friction or a trade-off and what you decided.
- Check any number or date you will quote against your own records.
- If you have no shipped project, use an internship or course team and say so.

**Follow-ups:**
- What did you do when an engineer said your model was too hard to deploy? "I asked what limit they were hitting, then offered options: a simpler model, a smaller input, or moving work off the request path."
- How did you handle a PM who wanted more than the data could support? "I showed what the data supported, offered a smaller promise, and agreed how we would measure the rest."
- How do you know it worked after launch? "A named metric, plus an agreed check with the engineers on monitoring."

**Common mistakes:**
- Talking only about the model, not the collaboration.
- Saying "we" for everything, so your part is invisible.
- Treating the PM or engineers as obstacles.
- Skipping the handoff: monitoring, documentation, who owns it after launch.
- AI-era note: a story polished by an AI tool tends to be short on specifics; expect follow-ups such as "what did the spec say?" and prepare real details. Do not use AI to write your story.

### Q12 ⭐⭐⭐ 🟡 Tell me about a time you had to deliver under a tight deadline or heavy pressure. What did you cut, protect or escalate?
**Asked at:** Public data science behavioural guides (Analytics Vidhya, DataLemur, Interview Query and Coursera guides list teamwork, conflict, ambiguity, failure and influencing-without-authority prompts); commonly reported in public guides; behavioural rounds appear in the Book 7 Part 1 profiles (Google, Microsoft, Amazon, Meta; see those profiles for their evidence tags and caveats); search snippets only, not opened
**Say this first (1 line):** Under a tight deadline I first agree what must not break, then cut or defer everything else in the open, and I escalate early rather than quietly missing the date.

**Structure:** Use CARL or STAR (see "STAR and CARL" above); the Action is the decision about cut, protect and escalate.
- Context: the deadline, what was at stake, and your role.
- Action: what you protected (correctness, a key metric, a check you would not skip), what you cut or deferred and who agreed, what you escalated and when.
- Result: what shipped, what was deferred, how the team felt about it afterwards.
- Learning: what you now do earlier next time.

**Strong sample answer (spoken):** Illustrative; replace with your own. "We had a reporting deadline for a leadership review, and the data arrived late. I had about half the time I planned. First I wrote down what could not go wrong: the main metric had to be correct and reproducible. Then I listed what could wait: extra segment cuts and a polished dashboard. I told my manager on day one that the full scope would not fit and asked her to confirm the cut. She agreed. I shipped the core analysis on time with a clear note about what was missing, and added the segments the following week. What I do differently now is flag scope risk the first day the input slips, not the third."

**Weak version (and why it fails):** "I worked late nights and got everything done." It sounds heroic but shows no judgement: no prioritisation, no communication, and no honesty about quality. It can also signal that you hide problems until they explode, and it rewards a pattern that does not scale.

**What the interviewer scores:**
- Prioritisation: a clear rule for what is protected and what is cut.
- Early, honest communication with the people affected.
- Quality judgement: you did not cut the part that makes the result trustworthy.
- Calm under pressure, and what you learned.
- Whether you sought help or agreement instead of deciding alone.

**Make it yours:**
- Choose a real deadline you lived through. Write the date pressure in plain words.
- List what you protected, cut and escalated, in that order, using what really happened.
- Name the person who agreed to the cut.
- State one honest cost of the cut.
- For data-science trade-off scenarios with numbers, see Book 6 Part 6 (for example the scenario on a promised launch date and a rules baseline); this answer is the general story version.

**Follow-ups:**
- Did anyone push back on the cut? "Yes; I explained the risk of the alternative and offered a date for the deferred part."
- What if you had not been allowed to cut anything? "I would show the options and risk, ask for a decision from the owner, and write down what we accepted."
- Would you work extra hours? "Sometimes, for a short stretch, but I would not use it to hide a planning problem."

**Common mistakes:**
- Bragging about long hours as the main action.
- Blaming others for the late input.
- Cutting testing or validation without saying so.
- Never mentioning escalation, so it sounds like you hid the problem.
- Claiming everything was delivered with no trade-off, which sounds invented.

### Q13 ⭐⭐⭐ 🟡 Tell me about a time you received critical feedback. What was it, how did you react, and what changed afterwards?
**Asked at:** Public data science behavioural guides (Analytics Vidhya, DataLemur, Interview Query and Coursera guides list teamwork, conflict, ambiguity, failure and influencing-without-authority prompts); commonly reported in public guides; behavioural rounds appear in the Book 7 Part 1 profiles (Google, Microsoft, Amazon, Meta; see those profiles for their evidence tags and caveats); search snippets only, not opened
**Say this first (1 line):** I take feedback as information: I listen first, check I understood, act on it, and then close the loop with the person.

**Structure:** CARL suits this question because the Learning step is what is being asked (see "STAR and CARL" above).
- Context: what you were working on and who gave the feedback (one sentence).
- Action: what they said in plain words, your first reaction honestly, what you asked to understand it, and the concrete change you made.
- Result: what changed in your work, and how you know (a later review, the same person's reaction).
- Learning: the habit you kept.

**Strong sample answer (spoken):** Illustrative; replace with your own. "A senior colleague told me my analysis write-ups were hard to follow because I led with method and put the conclusion at the end. My first reaction was a bit defensive, because I had worked hard on the method. I thanked her and asked for one example of what a good version looked like. She showed me a short summary she liked. I rewrote my next report with the recommendation in the first paragraph and the method below it, and asked her to review it. She said it was much easier to act on, and two stakeholders replied with decisions the same day. I now draft the first paragraph before I start the analysis, to keep my own thinking on the decision."

**Weak version (and why it fails):** "I do not get much critical feedback, my work is usually good," or a story where you were right and the other person was wrong. It signals low self-awareness or defensiveness, and a made-up non-answer is easy to probe.

**What the interviewer scores:**
- Self-awareness: an honest first reaction, not a polished one.
- Openness: you asked questions and did not argue.
- Action: a specific change you made, not a promise.
- Follow-through: evidence it stuck.
- Maturity: no blame, and the feedback was real, not a fake weakness.

**Make it yours:**
- Pick real feedback you received, ideally from a manager or reviewer.
- Write down the actual words, as close as you remember.
- Be honest about how you felt and what you did first.
- Choose one change that you can show, such as a template or a checklist.
- Avoid a disguised compliment ("I work too hard").

**Follow-ups:**
- Did you agree with the feedback? "Partly. I agreed with the main point and asked about the part I was unsure of; I did not just accept all of it."
- How do you ask for feedback? "I ask for one specific thing after a deliverable, such as 'what would have made this easier to use?'"
- What if the feedback is unfair? "I ask for an example, separate the useful part from the rest, and thank them anyway."

**Common mistakes:**
- Choosing trivial feedback that costs you nothing.
- Defending yourself during the story.
- Reporting a change with no evidence.
- Blaming the reviewer's style.
- Reciting an AI-polished version with no real moment of discomfort; interviewers notice flat stories.

### Q14 ⭐⭐⭐ 🟡 You had five requests from different people and time for two. Tell me about a time like that and how you chose.
**Asked at:** Public data science behavioural guides (Analytics Vidhya, DataLemur, Interview Query and Coursera guides list teamwork, conflict, ambiguity, failure and influencing-without-authority prompts); commonly reported in public guides; behavioural rounds appear in the Book 7 Part 1 profiles (Google, Microsoft, Amazon, Meta; see those profiles for their evidence tags and caveats); search snippets only, not opened
**Say this first (1 line):** I sort requests by impact, deadline and who is blocked, say no or "later" to the rest in the open, and ask my manager to settle conflicts I cannot.

**Structure:** STAR works; the Action is your method for choosing, so state it clearly (see "STAR and CARL" above).
- Situation and Task: the requests, from whom, and your capacity.
- Action: the criteria you used (business impact, deadline, effort, whether someone else is blocked), how you checked with your manager or the requesters, and how you told people about the ones you deferred.
- Result: what got done, what was deferred or dropped, and the reaction.
- Learning: a habit, such as a visible queue.

**Strong sample answer (spoken):** Illustrative; replace with your own. "One week I had five requests: a dashboard fix, a quick data pull, a model retrain, a question from finance, and a new analysis. I had time for two. I wrote them in a list with who needed it, by when, and what happens if it waits. The retrain fed a decision on Friday and the data pull was blocking a colleague, so those came first. I messaged the other three requesters the same day with a date and a reason, and offered a simpler option for the finance question. My manager saw the list and backed it. Nobody was surprised, and two of the deferred ones turned out to be less urgent than they sounded. Since then I keep a shared request list."

**Weak version (and why it fails):** "I just did them all, I worked faster." It is not credible, it hides quality cost, and it shows no way to choose. Another weak version: choosing whoever is most senior or loudest, which shows no judgement.

**What the interviewer scores:**
- Clear prioritisation criteria, not gut feel.
- Willingness to say no or later, politely.
- Proactive communication with those deferred.
- Use of the manager for real conflicts.
- Result and reflection.

**Make it yours:**
- Recall a real week when requests collided.
- Write the real criteria you used, even if rough.
- Name what you dropped and what it cost.
- Say how the people you deferred reacted.
- If your first approach was poor, say so and what you changed.

**Follow-ups:**
- What if two senior people both said theirs was urgent? "I put both options and the cost of each in front of my manager and asked them to decide, or asked the two to agree."
- How do you say no? "With a reason, a new date, and, where possible, a smaller version I can do now."
- Did you ever get it wrong? "Yes, once I underestimated a request; I now ask what the request is for before ranking it."

**Common mistakes:**
- Describing the heavy workload but not the choice.
- Saying yes to everything.
- Silently dropping requests.
- Ranking by seniority only.
- Never checking what was really needed.

### Q15 ⭐⭐⭐ 🔴 Tell me about a time a model, pipeline or analysis you owned failed or underperformed in production. How did you diagnose it, who did you tell, and what did you change?
**Asked at:** Public ML engineer question banks (Yardstick, BrightHire and Jobrise pages list model-failure-in-production, data-quality, ambiguity and changed-approach prompts); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I stay factual and own it: I contain the damage first, tell the right people early, find the cause with evidence, and then fix both the problem and the process that let it through.

**Structure:** STAR with a diagnosis thread (see "STAR and CARL" above); keep the technical reasoning visible.
- Situation and Task: what you owned, what failed or underperformed, how you found out, and the impact.
- Action: contain (roll back, pause, add a fallback), tell (who, when, what you said), diagnose (what you checked and ruled out: data drift, pipeline change, label delay, a bug), fix.
- Result: what recovered, what did not, the cost.
- Learning: a prevention you added, for example monitoring, a data check or a rollback plan.

**Strong sample answer (spoken):** Illustrative; replace with your own. "A model I owned started giving worse predictions after a pipeline change upstream. A monitoring alert showed the score distribution had shifted. First I paused the automatic use of the score and told my manager and the product owner what I knew and did not know. Then I compared recent inputs with training data and found one feature had changed its units. I fixed the mapping, backfilled the affected days, and told the same people the cause and the impact. Afterwards I added a data check on that input and a short runbook, and asked the upstream team to tell us about schema changes. The part I own is that I had no check on that feature before. That is what I changed."

**Weak version (and why it fails):** "The model failed because the data team changed something." Blame with no ownership, no sign you told anyone, and no prevention. Or the opposite: a failure so small it is not a failure, which looks like avoiding the question.

**What the interviewer scores:**
- Ownership without blame.
- Speed and order: contain, communicate, diagnose.
- Technical diagnosis, with evidence and ruled-out causes.
- Honest communication to the right people.
- Prevention: monitoring, tests, process.

**Make it yours:**
- Use a real failure you owned, even a modest one. Do not invent a dramatic one.
- Write the timeline: how you found out, who you told, what you did first.
- Be exact about the cause and what you did not know at the time.
- State the real impact, and only numbers you can back.
- Name the prevention you actually put in place.

**Follow-ups:**
- How did you tell stakeholders? "Short message: what happened, impact, what we are doing, next update time; no jargon."
- How could you have caught it earlier? "A distribution check on inputs and an alert on prediction drift."
- Was it your fault? "The cause was upstream, but not having a check was mine to fix, and I did."

**Common mistakes:**
- Starting with the cause and skipping containment.
- Blaming another team.
- Technical depth with no communication.
- Claiming the fix without evidence it worked.
- No change to the process afterwards.

### Q16 ⭐⭐⭐ 🔴 Tell me about a time the data contradicted your intuition or a belief your team held. What did you do with the finding?
**Asked at:** Public data science behavioural guides (Analytics Vidhya, DataLemur, Interview Query and Coursera guides list teamwork, conflict, ambiguity, failure and influencing-without-authority prompts); commonly reported in public guides; behavioural rounds appear in the Book 7 Part 1 profiles (Google, Microsoft, Amazon, Meta; see those profiles for their evidence tags and caveats); search snippets only, not opened
**Say this first (1 line):** When data disagrees with what we believed, I check my own work first, then show the finding simply and invite the team to test it with me.

**Structure:** CARL fits well, because the learning matters (see "STAR and CARL" above).
- Context: the belief, who held it, and what you expected the data to show.
- Action: how you checked the finding was real (data quality, sample, a second method, a colleague's review), how you presented it (to the people who held the belief, with the evidence and its limits), and what you proposed.
- Result: what the team decided, and what happened.
- Learning: how it changed how you form hypotheses.

**Strong sample answer (spoken):** Illustrative; replace with your own. "Our team believed a certain feature drove most of our user retention. When I looked at the data, the effect nearly disappeared once I controlled for how long users had been active. I did not trust it at first. I checked the joins, reran it on a different time window, and asked a colleague to review my code. The result held. I showed the team two plots and said what I could and could not claim: it was an association, not proof. I suggested a small experiment. The team agreed, the test confirmed the smaller effect, and we shifted effort to other ideas. What I took from it: I now write down what I expect before I look, so I can notice when I am wrong."

**Weak version (and why it fails):** "The data showed I was right." That is not the question. Another weak version: you found a surprising result and announced it with no checking, or you buried it because it upset people. Both show poor judgement.

**What the interviewer scores:**
- Intellectual honesty: you checked yourself first.
- Rigor: a second look before claiming a surprise.
- Communication: you brought people along, not a "gotcha".
- Humility about what the data does and does not prove.
- Whether the finding changed a decision.

**Make it yours:**
- Choose a real case where the result surprised you or the team.
- Write the belief and the evidence in one line each.
- List the checks you actually ran.
- Say how people reacted, honestly, including pushback.
- Keep claims modest: use association language unless you ran an experiment.

**Follow-ups:**
- What if the team did not accept it? "I would offer a test that could prove either side, and agree beforehand what result would change our minds."
- How did you rule out a bug? "Reran with different code and data windows, and had a colleague review."
- What did you change afterwards? "I record my expectation before analysis."

**Common mistakes:**
- Choosing a story where you were simply right all along.
- Overclaiming causation.
- Presenting the result as a win over colleagues.
- Skipping the checks.
- Never saying what decision followed.

### Q17 ⭐⭐⭐ 🔴 How do you use AI tools such as coding assistants or LLM chat in your work, and tell me about a time one gave you a wrong or risky output that you caught.
**Asked at:** 2026 AI-era behavioural guides (TheInterviewGuys, TechInterview.org, Tredence, PrachHub and FacePrep pages list daily AI-tool use, catching AI mistakes and judgement on when to use AI; PrachHub attributes one set to Amazon engineering loops, which is secondhand); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I use AI tools as a fast first draft that I always check, and I do not paste in anything I am not allowed to share.

**Structure:** Two parts: your practice, then one STAR story (see "STAR and CARL" above).
- Practice (about 30 seconds): what you use it for (boilerplate code, explaining an error, drafting tests, summarising), what you do not use it for (private data, final conclusions without checking), and your checks (run it, test it, read it, compare with documentation).
- Story: Situation (the task), Action (what the tool produced, how you spotted the problem, what you did), Result (what would have happened, how you fixed it), Learning (the check you added).
- Follow your employer's or school's rules on AI tools; if you do not know them, ask.

**Strong sample answer (spoken):** Illustrative; replace with your own. "I use a coding assistant for boilerplate, tests and explaining errors, and I never share private data with it. I treat its output like code from a new colleague: I read it and run it. Once it wrote a data-cleaning step that dropped rows with missing values without telling me. The code ran fine, but my row count fell by a lot. I noticed because I always compare counts before and after a step. I rewrote it to keep those rows and flag them, and added a count check to my pipeline. The lesson is that code that runs is not code that is right, so I test the result, not just the code."

**Weak version (and why it fails):** "I use it for everything, it saves me hours," or "I do not use AI at all." The first has no checking and no judgement; the second can sound out of touch or untrue. A story with no specific error, or one that sounds AI-written, will collapse on follow-up questions.

**What the interviewer scores:**
- Practical, honest use, not hype or fear.
- Verification habits: tests, comparisons, review.
- Judgement on data privacy and what not to share.
- A real, specific error you caught.
- Willingness to disclose how you used it.

**Make it yours:**
- Describe how you really use the tools this month.
- Recall one real wrong or risky output, even a small one.
- State your own check, as you actually do it.
- If you have no such story, say so and describe how you would check, and do not invent one.
- Know your employer's or school's AI policy and say you follow it.

**Follow-ups:**
- Would you tell us if you used AI on a take-home? "Yes. I would follow the stated rules, and say what I used it for and what I checked."
- When would you not use AI? "When the data is private, when I cannot verify the answer, or when the task is to show my own reasoning."
- How do you catch subtle errors? "Test on small cases I can compute by hand, and compare with a trusted reference."

**Common mistakes:**
- Claiming you never need to check it.
- Pasting private or company data into a public tool.
- A generic story with no detail.
- Using AI to write this answer. Live follow-up depth is how rehearsed or AI-written stories are found out.
- Blaming the tool instead of owning the check.

### Q18 ⭐⭐ 🟢 Why are you looking to leave your current role, or why did you leave your last one?
**Asked at:** General HR-style questions listed on aggregator pages (Glassdoor data science question pages, Prepfully and InterviewPal job-change-reason pages, an edX data-industry sample list); commonly reported in public guides; behavioural rounds appear in the Book 7 Part 1 profiles (Google, Microsoft, Amazon, Meta; see those profiles for their evidence tags and caveats); search snippets only, not opened
**Say this first (1 line):** I explain what I am moving towards in a sentence or two, keep the reasons about growth and fit, and say nothing negative about my current or past team.

**Structure:** This is not a STAR question; use a short three-part shape.
- Past (one line): what the role gave you, said with respect.
- Gap (one line): what you want that is not available there, framed as scope, skills or domain, not as complaints.
- Pull (one or two lines): why this role and team match it, with something specific you know about the work.
- If you were laid off or left without a job lined up, say so briefly and calmly, then move to what you learned and what you want next.
- Keep pay out of it unless the interviewer asks; if asked, see the script.

**Strong sample answer (spoken):** Illustrative; replace with your own. "I have learned a lot in my current role, mostly on forecasting models for one product. What I want next is to work on problems closer to deployment and to own a model end to end, and my current team is not planning that kind of work this year. I talked with my manager about it and we agreed it is not on the roadmap. When I looked at this team, the work on [specific area from the job posting] matches what I want to build. I am not leaving because of any one problem; I am looking for the next step in what I want to do."

**Weak version (and why it fails):** "My manager is bad and the company is disorganised," or "I want more pay" as the only reason. Criticism of a former employer makes interviewers wonder how you will talk about them. A reason with no pull towards the new role sounds like running away.

**What the interviewer scores:**
- Professionalism: no blame, no gossip.
- A reason that is credible and consistent with your CV.
- Motivation that points forward, to this role.
- Self-awareness about what you want.
- Whether you tried to fix it where you were.

**Make it yours:**
- Write your real reason in one honest sentence, then remove blame from it.
- Find one true thing you valued in the old role.
- Find one specific thing about this team that connects to your reason.
- If the reason is hard (layoff, conflict, a break), prepare a short, calm, true version.
- Check that the story matches what your references would say.

**Script (copy and adapt):**
```
I have learned [one thing] in my current role and I am grateful for it.
What I want next is [scope, skill or domain], and that is not available there right now.
This role looks like a strong match because [specific reason from the posting or the team's work].
```
If asked about pay or notice terms: "I would like to understand the whole package first. Could you tell me how the range works for this role?" For notice period and what applies to you, ask the recruiter or HR and check your own contract and official sources; this book gives no legal advice.

**Follow-ups:**
- Did you talk to your manager first? "Yes, [what you discussed]; that is how I know it is not available there."
- Would a better offer from your current employer keep you? "I am mostly driven by the work, so the main question is whether the scope changes."
- Why so many short jobs (if true)? "Give a short true reason for each, and what you have looked for since."

**Common mistakes:**
- Speaking badly of a manager or team.
- Making pay the only reason.
- A vague answer with no pull towards the new role.
- A story that differs from what a reference would say.
- Memorising an AI-written line that does not sound like you.

### Q19 ⭐⭐ 🟢 Where do you want your career to be in three to five years, and how does this role help you get there?
**Asked at:** General HR-style questions listed on aggregator pages (Glassdoor data science question pages, Prepfully and InterviewPal job-change-reason pages, an edX data-industry sample list); commonly reported in public guides; behavioural rounds appear in the Book 7 Part 1 profiles (Google, Microsoft, Amazon, Meta; see those profiles for their evidence tags and caveats); search snippets only, not opened
**Say this first (1 line):** I want to grow into deeper ownership of data or ML work that people use, and this role is a good next step because of the scope it offers.

**Structure:** Three beats, not STAR.
- Direction: what you want to get better at or take on (technical depth, owning a product area, mentoring), in one or two sentences. Keep it flexible, since plans change.
- Link: how this role gives it to you, with one concrete example from the posting or team.
- Contribution: what you will give the team along the way.
- Be careful with "I want your job" and with plans that suggest you will leave soon. Match the direction to the level (see "What companies expect by level" above), for example deeper ownership for mid level and wider influence for senior.

**Strong sample answer (spoken):** Illustrative; replace with your own. "In three to five years I want to be the person who can take a vague problem, choose the right approach and see it through to something people use. Right now I am strong on modelling, and I want to get better at deployment and at working with product teams. This role gives me that, because the team ships models into a live product and I would work with engineers and product managers from the start. I would also like to start mentoring newer teammates. I do not have a fixed title in mind; I care more about the scope growing as I show I can handle it."

**Weak version (and why it fails):** "I want to be a manager in two years" with no link to the role, or "I have not thought about it". The first can sound like a plan to leave this job quickly; the second shows no direction. A plan that has nothing to do with the team also sounds rehearsed.

**What the interviewer scores:**
- Reasonable ambition that fits the role and level.
- Self-awareness about skills to build.
- Fit: the role would really help you grow.
- Commitment: you are not planning to leave soon.
- Whether the plan is realistic and flexible.

**Make it yours:**
- Write what you actually want to be doing in three to five years, in plain words.
- Pick one skill gap you are honestly working on now.
- Read the posting and find the part of the role that supports your direction.
- Say what you will offer, not only what you want.
- If you are unsure, say what you are exploring and how you will decide.

**Script (copy and adapt):**
```
In three to five years I would like to [own / lead / specialise in ...].
To get there I am working on [skill], and this role would help because [specific part of the role].
I would also like to contribute by [what you can give the team].
```

**Follow-ups:**
- What if the role does not lead there? "Then I would talk to my manager about it early; I am looking for a team where growth is a normal conversation."
- Do you want to manage people? "[Your honest answer]. Either way I want to keep building technical depth and helping others grow."
- What have you done recently towards that goal? "[One real step: a course, a project, mentoring, a talk.]"

**Common mistakes:**
- Naming a title or date with no link to the work.
- Saying you do not know and stopping.
- A plan that points at a different field.
- Making it all about what you will get and nothing about what you will give.
- Copying an AI or website answer that does not match your real CV.

### Q20 ⭐⭐ 🟢 What kind of work energises you, and what kind of work drains you, in data or ML?
**Asked at:** General HR-style questions listed on aggregator pages (Glassdoor data science question pages, Prepfully and InterviewPal job-change-reason pages, an edX data-industry sample list); commonly reported in public guides; behavioural rounds appear in the Book 7 Part 1 profiles (Google, Microsoft, Amazon, Meta; see those profiles for their evidence tags and caveats); search snippets only, not opened
**Say this first (1 line):** I am energised by solving open problems with data and seeing people use the result, and drained by work with no clear purpose or no feedback, and I know how to manage that.

**Structure:** Use a short pattern, not STAR.
- Energisers (two): name the kind of work and one example of when it happened. Use real episodes.
- Drainers (one or two): name them honestly and add how you handle them, so it does not sound like a complaint.
- Fit: link to the role, saying which side of the work this job has more of.
- Avoid choosing a drainer that is the core of the job (for example, saying you dislike working with data cleaning when the role is mostly that).

**Strong sample answer (spoken):** Illustrative; replace with your own. "I get energy from the early part of a problem, when it is unclear what the question is, and from the moment someone uses what I built to make a decision. I also like working through a hard debugging problem with a colleague. What drains me is repetitive manual work, such as re-running the same report by hand, and projects where nobody can say what the result is for. I deal with the first by automating it, and with the second by asking early what decision the work supports. From the posting, this role has a lot of the kind of work I enjoy, and I would be comfortable with the routine parts too."

**Weak version (and why it fails):** "I love everything about data and nothing drains me." It is not believable. Another weak version: naming the main part of the job as a drainer ("I hate meetings and talking to stakeholders" for a role that needs it). It signals poor fit.

**What the interviewer scores:**
- Self-awareness, with real examples.
- Fit between what energises you and the role's day-to-day.
- Honesty about drainers without complaining.
- Ability to manage the drainers.
- Consistency with the rest of your story.

**Make it yours:**
- Think of the last three weeks and note which tasks gave you energy and which did not.
- Pick two energisers and write one real example each.
- Pick a real drainer that is not the core of this job, and how you cope.
- Read the posting and compare honestly.
- If the job has a lot of your drainers, consider whether it is a good fit.

**Follow-ups:**
- Give me an example of the energising work. "[A real episode, with what you did and why it felt good.]"
- What if the job has lots of the drainers? "I would plan around them, but I would also check with the team how much of the week it is."
- How do you stay motivated on routine work? "I automate where I can, and link it to the decision it supports."

**Common mistakes:**
- Saying nothing drains you.
- Naming the central task of the job as a drainer.
- Vague answers like "challenging work" with no example.
- Listing only technical tasks and skipping people and impact.
- Reading a polished answer that does not match your own experience, which falls apart when asked for an example.
