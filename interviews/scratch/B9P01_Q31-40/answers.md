### Q31 ⭐⭐ 🟡 Tell me about a time you took initiative to fix a process, tool or recurring problem that nobody had asked you to fix.
**Asked at:** No public page found for this exact framing, editor-designed; the theme is adjacent to prompts in general behavioural guides; search snippets only, not opened
**Say this first (1 line):** I fixed a recurring problem that was costing my team time, I checked with the owner before changing anything, and I measured whether it helped.

**Structure:** Use CARL (see the STAR and CARL section at the top of this part), because the learning matters here.
- Context: the recurring problem and who it hurt, in one or two sentences. Say nobody had asked you.
- Action: how you confirmed it was a real problem, who you told, what you built or changed, and what you chose not to do.
- Result: a measured change (time saved, errors avoided) or a plain description, plus anything that did not work.
- Learning: what you now check before starting an unrequested fix.

**Strong sample answer (spoken):** (Illustrative template; replace with your own real example.)
"Our team re-ran the same data pull by hand every Monday, and it broke whenever a column name changed. Nobody owned it. I first asked my lead if fixing it was a good use of my time, and she said yes if it stayed small. I wrote a short script with a schema check and a clear error message, and I added a page to the team wiki. I also asked the two people who used the pull to try it before I switched it on. The Monday task went from about an hour to a few minutes, and the breaking changes now show up as a clear message instead of a silent bad number. One thing I missed: I forgot to hand over who maintains it. A month later I fixed that by naming an owner. Now I ask who will own a fix before I build it."

**Weak version (and why it fails):** "I saw the process was bad, so I rebuilt the whole thing over a weekend and told everyone to use it." It shows no check with the owner, no users involved, no result and no hand-over. It sounds like a solo project that created new work for others.

**What the interviewer scores:**
- You spotted a real problem without being told, and you can say why it mattered.
- Judgement: you checked scope and who was affected before acting.
- You brought others along instead of imposing a fix.
- A result you can defend, including what stayed unsolved.
- Follow-through: someone still benefits after you moved on.

**Make it yours:**
- Pick one real fix you made without being asked. Smaller and true beats big and vague.
- Write the cost of the problem before your fix in your own measured terms (time, errors, reruns).
- Name who you talked to first and what they said.
- Say what you would do differently, such as hand-over or documentation.
- If you have no fix like this, use a smaller real one, or say so and describe a near-miss where you raised the problem without owning it.

**Follow-ups:**
- "Why was it your job?" It was not; I judged that the cost to the team was higher than the time I would spend, and I checked with my lead.
- "How do you know it helped?" Say how you measured it and what you cannot claim.
- "Did it stay fixed?" Answer honestly, including maintenance.

**Common mistakes:** Picking a heroic story with no result. Saying "we" for everything. Skipping the check with stakeholders. Presenting a fix that created work for others. AI-era note: a rehearsed or AI-written story gets exposed when the interviewer asks what the code or process actually did; use your own example.

### Q32 ⭐⭐ 🟡 Tell me about a time you caught a data quality problem before it reached a model or a decision. How did you find it and who did you tell?
**Asked at:** Public ML engineer question banks (Yardstick, BrightHire and Jobrise pages list model-failure-in-production, data-quality, ambiguity and changed-approach prompts); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I found a data problem by checking, not luck; I told the data owner and the people using the result straight away, and I added a check so it would not recur.

**Structure:** CARL or STAR (see the STAR and CARL section at the top of this part). Keep the technical reasoning visible.
- Context: what the data fed (a model, a report, a decision) and when you found the issue.
- Action: how you found it (the check or the odd pattern), how you confirmed it, who you told and in what order, what you held back.
- Result: what was avoided or corrected, and the check you added.
- Learning: one monitoring or validation habit you now keep.

**Strong sample answer (spoken):** (Illustrative template; replace with your own real example.)
"Before training a model, I compared the label rate by week and one week dropped sharply. I did not trust the model result until I knew why. I traced it to a join that had silently dropped rows after an upstream schema change. I confirmed it by counting rows on both sides. Then I told the data owner and my lead the same day, with the counts and a one-line description, and I paused the training run. The owner fixed the join, and I reran everything. I also added a row-count and null-rate check to our pipeline, so a drop like that fails loudly. I did not claim the old results were wrong in a specific direction, because I had not tested that. The learning: I now compare distributions across time before any training run."

**Weak version (and why it fails):** "I noticed some bad data and fixed it myself." No method, nobody told, no prevention. If the data belongs to another team, quietly patching it leaves the cause in place and surprises people later.

**What the interviewer scores:**
- Technical care: you check data before trusting a result.
- Method: how you found and confirmed the cause.
- Communication: you told the right people quickly, with evidence.
- Prevention: a check or monitor, not a one-off fix.
- Honesty about what you did and did not verify.

**Make it yours:**
- Choose a real case, even a small one from a course project or internship.
- Write the signal that tipped you off and the check that confirmed it.
- List who you told, in order.
- State the effect avoided in plain words, without inventing a number.
- Name the check you added or would add.

**Follow-ups:**
- "What if the owner disagreed?" Show the evidence (counts, examples), ask what they see, and agree a next step; escalate only if the risk is real.
- "How do you catch this earlier?" Schema checks, row counts, null and distribution monitors.
- "Was any decision already made?" Say what you did about it, honestly.

**Common mistakes:** No method. Fixing silently. Overclaiming impact. No prevention step. AI-era note: if you used an AI tool to help find the issue, say so and say how you verified its suggestion yourself.

### Q33 ⭐⭐ 🟡 Tell me about a time a teammate was struggling or underdelivering and it affected your work. What did you do?
**Asked at:** Public data science behavioural guides (Analytics Vidhya, DataLemur, Interview Query and Coursera guides list teamwork, conflict, ambiguity, failure and influencing-without-authority prompts); commonly reported in public guides; behavioural rounds appear in the Book 7 Part 1 profiles (Google, Microsoft, Amazon, Meta; see those profiles for their evidence tags and caveats); search snippets only, not opened
**Say this first (1 line):** I started by understanding why, talked to the person directly and privately, offered specific help, and only escalated when the work was at risk.

**Structure:** STAR (see the STAR and CARL section at the top of this part).
- Situation: the project, and how the teammate's gap affected your work, with no blame in the tone.
- Task: what you were responsible for protecting (a deadline, a deliverable).
- Action: the private conversation, what you learned, the help or change you offered, how you protected the deadline, when you told the manager.
- Result: what happened to the work and the relationship, honestly, even if it was only partly fixed.

**Strong sample answer (spoken):** (Illustrative template; replace with your own real example.)
"A teammate's part of our pipeline was late twice, and my analysis depended on it. I did not go to the manager first. I asked him privately how it was going. He said the data source was unclear and he did not want to ask again. I offered thirty minutes to walk through it with him, and I agreed smaller handoffs with dates. That helped, but one piece was still late, so I told our lead the risk and what I had already tried, and I asked her to adjust the scope. I did not say he was careless. We shipped with one piece cut, and he now asks questions earlier. What I learned is to ask about blockers sooner and to agree handoffs in writing at the start."

**Weak version (and why it fails):** "He was lazy, so I told my manager and did his work myself." It blames, skips the conversation, and shows no process. Doing the work silently also hides the problem and teaches nothing.

**What the interviewer scores:**
- Empathy and curiosity about the cause.
- Direct, respectful communication before escalation.
- Protecting the outcome while helping the person.
- Sensible escalation: timing and framing.
- No blame or gossip.

**Make it yours:**
- Choose a real situation; keep the person anonymous and speak about them fairly.
- Recall what they told you about the cause.
- List what you offered and what you changed in your own plan.
- Say when and how you involved the manager.
- Give the real outcome, even if mixed.

**Follow-ups:**
- "What if they did not improve?" Document, escalate with facts, and focus on the outcome.
- "Did you tell them you escalated?" Yes; tell people before or as it happens, not behind their back.
- "Would you do it differently?" One specific change.

**Common mistakes:** Blaming. Going straight to the manager. Rescuing silently. Telling a story where you were perfect. Check Book 7 Part 1 for how companies frame teamwork rounds; this answer is general [G].

### Q34 ⭐⭐ 🟡 Tell me about a time your first approach did not work and you had to change course part-way through a project.
**Asked at:** Public ML engineer question banks (Yardstick, BrightHire and Jobrise pages list model-failure-in-production, data-quality, ambiguity and changed-approach prompts); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** My first approach failed, I saw the evidence early, I told the team, I changed course on purpose, and I can say what I learned.

**Structure:** CARL (see the STAR and CARL section at the top of this part), with the decision point as the centre.
- Context: the project and the first approach, with why you chose it.
- Action: the signal that it was not working, how long you kept going and why, the alternatives you weighed, the decision, who you told.
- Result: what the new approach delivered, and the cost of the switch.
- Learning: how you now set early checkpoints.

**Strong sample answer (spoken):** (Illustrative template; replace with your own real example.)
"I started a forecasting task with a complex model because it won on paper. After two weeks the validation results were unstable and I could not explain them. I stopped and listed what I knew: the data was short and noisy. I compared a simple baseline and it was nearly as good and much steadier. I told my lead what had happened, that I had lost about a week, and that I wanted to switch. She agreed. We shipped the simpler model with a clear monitoring plan. It was less impressive but it held up. The learning is that I now run a baseline in the first days and set a checkpoint where I decide to continue or change. I would also say my first choice was partly about wanting a harder model."

**Weak version (and why it fails):** "Nothing went wrong, but I adjusted the plan a bit." Or the opposite: blaming data or a colleague. Both avoid showing judgement. Interviewers want to see how you decide, not a spotless record.

**What the interviewer scores:**
- You noticed the problem on evidence, not feeling.
- You accepted the sunk cost and changed course.
- You communicated the change and its cost.
- The new approach was reasoned.
- You learned something specific.

**Make it yours:**
- Use a real project where you changed method, even in a course or a side project.
- Write the signal that told you the first approach was failing.
- Say what the switch cost in time.
- State what the second approach actually gave, in your measured terms.
- Add the habit you built afterwards.

**Follow-ups:**
- "Why did you not switch sooner?" Be honest: what you thought, and what you would check now.
- "How did you tell your manager?" Facts, cost, a proposal.
- "How do you pick when to stop?" Checkpoints agreed early.

**Common mistakes:** A failure that is really a humblebrag. Blaming data. No cost stated. No learning. AI-era note: an AI-polished story may skip the awkward detail; interviewers probe exactly there.

### Q35 ⭐⭐ 🟡 Tell me about a cross-functional project that went well. What was your part in making it work?
**Asked at:** Public data science behavioural guides (an Analytics Vidhya list and a Coursera guide frame stakeholder, explanation and business-decision stories; a KDNuggets piece says the technical reasoning should stay visible inside the story); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** It went well because we agreed on the goal and the decision early; my part was the analysis and keeping the group aligned on what the numbers could and could not say.

**Structure:** STAR (see the STAR and CARL section at the top of this part), with your own role clear.
- Situation: the project, the functions involved (product, engineering, design, business) and the goal.
- Task: your specific role, and what you committed to deliver.
- Action: how you agreed on the question and metric, how you shared progress, how you handled one disagreement or a handoff, and your technical choices.
- Result: the outcome, what the others would say about your part, and anything that fell short.

**Strong sample answer (spoken):** (Illustrative template; replace with your own real example.)
"We built a recommendation feature with product, engineering and design. My role was the model and the evaluation. At the start I asked product what decision this would change and agreed one success metric with them. I sent a short weekly note in plain language, including what was not working. When engineering worried about latency, I tested a smaller model and showed the trade-off, and we chose together. The feature launched on time, and the experiment results were mixed: engagement rose modestly but one segment dropped, so we changed the rollout. I think it worked because the metric and the decision rights were clear from week one. I would add earlier design reviews next time."

**Weak version (and why it fails):** "Everyone worked really well together and we launched." There is no role, no action, no friction and no result. It does not show what you personally did.

**What the interviewer scores:**
- Your role is clear and specific, not just "we".
- You understand other functions' constraints.
- How you handled friction or trade-offs.
- Technical reasoning stays visible.
- Results are honest.

**Make it yours:**
- Pick a project with at least two other functions, real and recent if possible.
- List your decisions as opposed to the team's.
- Recall one moment of friction and how it resolved.
- Say what a partner would credit you with.
- Include the result, even if mixed.

**Follow-ups:**
- "What was the hardest part?" One friction point and your move.
- "What did you learn about the other function?" A specific constraint.
- "What would you change?" One concrete change.

**Common mistakes:** All "we". Too much background. A project with no friction. Technical detail missing. See Book 9 Part 2 for communication craft and Book 6 Part 6 for numeric trade-off scenarios.

### Q36 ⭐⭐ 🟡 Tell me about a time you worked with someone whose working style was very different from yours. How did you make it work?
**Asked at:** No public page found for this exact framing, editor-designed; the theme is adjacent to prompts in general behavioural guides; search snippets only, not opened
**Say this first (1 line):** I treat a different style as information: I asked how they like to work, agreed a few simple ways of working, and kept the focus on the shared goal.

**Structure:** STAR or CARL (see the STAR and CARL section at the top of this part).
- Situation: the person's style, described neutrally (for example, prefers written updates versus talking things through), and the friction it caused.
- Task: what needed to work between you.
- Action: what you asked, what you adjusted in your own style, what you agreed, how you checked it worked.
- Result: the effect on the work and the relationship; what you kept doing.

**Strong sample answer (spoken):** (Illustrative template; replace with your own real example.)
"On one project my colleague liked detailed written plans before any work started, and I liked to prototype first and talk. We were getting frustrated. I asked him how he liked to work and told him how I did. We agreed that I would send a short written plan before I started, and he would be fine with a quick prototype review after. I also asked what would help him trust my timelines, and he asked for earlier progress notes. It took a few weeks, but the friction dropped and we finished on time. I noticed that his plans caught two risks I would have missed. Now I ask about working style in the first week with anyone new."

**Weak version (and why it fails):** "He was difficult, but I just ignored it and did my job." It treats the other person as the problem, shows no adaptation, and suggests you avoid conflict instead of managing it.

**What the interviewer scores:**
- Self-awareness about your own style.
- Respect for the other person's.
- Willingness to adapt, with practical agreements.
- Focus on the work, not personality.
- A result and a habit.

**Make it yours:**
- Choose a real colleague; describe behaviours, not character.
- Write what you did that clashed and what they did.
- List the agreements you made.
- Say what improved and how you know.
- Keep it fair: no judgements about who they are.

**Follow-ups:**
- "What if they would not adapt?" I adapt what I can, agree the minimum with them, and involve the manager only if work suffers.
- "What did you learn?" One concrete habit.
- "Which style are you?" Honest, with a strength and a cost.

**Common mistakes:** Labelling the person. A story where only they changed. No agreement or result. Generalising about groups of people; keep to the individual's behaviour.

### Q37 ⭐⭐ 🔴 Tell me about a time you disagreed with your manager's decision, you did not get your way, and you still had to carry it out. What did you do afterwards?
**Asked at:** Public data science behavioural guides (Analytics Vidhya, DataLemur, Interview Query and Coursera guides list teamwork, conflict, ambiguity, failure and influencing-without-authority prompts); commonly reported in public guides; behavioural rounds appear in the Book 7 Part 1 profiles (Google, Microsoft, Amazon, Meta; see those profiles for their evidence tags and caveats); search snippets only, not opened
**Say this first (1 line):** I made my case once with evidence, accepted the decision, committed fully, and then checked the outcome honestly instead of saying "I told you so".

**Structure:** STAR with an emphasis on the Action after the decision (see the STAR and CARL section at the top of this part).
- Situation: the decision and why you disagreed, in one or two sentences.
- Task: your role, and the fact that the decision was your manager's to make.
- Action: how you raised it (evidence, private, early), what you asked, how you accepted the decision, how you carried it out, any risk you flagged.
- Result: what happened, including if you were wrong, and what you did afterwards.

**Strong sample answer (spoken):** (Illustrative template; replace with your own real example.)
"My manager decided to launch a model with a simpler validation than I wanted. I thought it risked missing a segment. I raised it in a one-to-one with a small table of what I had found, and asked what constraint he was working under. He had a deadline and a plan to monitor after launch. I disagreed but it was his call, so I helped set up the monitoring and wrote down which segment to watch. At launch I did not hold back effort. Two weeks later the segment did look weaker, and I showed him the data without comment. We fixed it in the next release. I learned to ask what constraint sits behind a decision, and to turn my concern into a concrete check."

**Weak version (and why it fails):** "I disagreed, he overruled me, so I did the minimum and waited for it to fail." This shows resentment and no ownership. Another weak version: "I escalated over his head," with no sign you first listened.

**What the interviewer scores:**
- You disagree with evidence and respect.
- You accept decisions you do not control.
- Commitment to the plan after you lose.
- Handling outcomes fairly, win or lose.
- Maturity, not ego.

**Make it yours:**
- Choose a real disagreement where you did not get your way.
- Write the evidence you showed and when.
- Say what the constraint behind the decision was.
- Describe what you did to make it work.
- Give the outcome, even if you were wrong.

**Follow-ups:**
- "When would you escalate?" When there is a serious risk to people or users, after raising it directly; ask HR or the relevant policy owner how this is handled; no legal advice here.
- "Were you right?" Answer honestly.
- "How did it affect the relationship?" Specific.

**Common mistakes:** Making yourself the hero. Quiet resentment. Skipping the outcome. No change afterwards. AI-era note: a polished story with no stakes gets probed; keep the real tension.

### Q38 ⭐⭐ 🔴 Tell me about a time you were under pressure to ship or report something you were not fully comfortable with. What did you do?
**Asked at:** Public guides list data-ethics behavioural prompts (Yardstick data-ethics page, Dataford ethics questions); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I said clearly what I was not comfortable with and why, offered a safer option that still met the need, and escalated through the right channel if the risk was serious.

**Structure:** STAR (see the STAR and CARL section at the top of this part), centred on the judgement call.
- Situation: what was due and what the concern was (a result not checked, a weak validation, a data use you doubted).
- Task: your responsibility for the quality of what you shipped or reported.
- Action: what you checked, what you said and to whom, the options you offered (ship with a clear caveat, delay a little, limit the scope), who decided.
- Result: the decision and outcome, and what you changed afterwards.

**Strong sample answer (spoken):** (Illustrative template; replace with your own real example.)
"Before a leadership review I was asked to report an uplift from an experiment that had run too short. I was not comfortable saying it was a win. I told my manager that day: the result might be noise, and here is what the data showed so far. I offered two options. We could report it as early and unconfirmed, with a date for the final read. Or we could wait one more week. We chose the first, and I wrote the caveat on the slide in plain words. The final read came back smaller than the early number. People were glad the early slide had said it might. Afterwards we agreed a minimum run time for experiments. I still try to give options, not just objections."

**Weak version (and why it fails):** "I just did what I was told and reported it." Or: "I refused and went to the director." The first shows no judgement; the second skips the conversation and options.

**What the interviewer scores:**
- Integrity: you do not hide uncertainty.
- Courage to speak up, with tact.
- Problem solving: you bring options.
- Right escalation route.
- Reflection on how it affected process.

**Make it yours:**
- Choose a real moment, even a small one from a course or a first job.
- Write exactly what worried you and the evidence.
- Say what you said, to whom, and when.
- List the options you offered.
- Give the outcome without inflating it.

**Follow-ups:**
- "What if your manager insisted?" Put my concern in writing, state the caveat, and use the company's escalation route if real harm is possible; ask HR how this is handled; no legal advice here.
- "Was the deadline real?" Check what was fixed and what could move.
- "What would you do now?" One change.

**Common mistakes:** Silent compliance. Dramatic refusal. No alternative. Claiming you never faced pressure. Naming a real company's internal event as yours. Keep the example your own.

### Q39 ⭐⭐ 🔴 Tell me about a time you had to give your manager or a team bad news about a result, a delay or an error. How did you do it?
**Asked at:** No public page found for this exact framing, editor-designed; the theme is adjacent to prompts in general behavioural guides; search snippets only, not opened
**Say this first (1 line):** I give bad news early, plainly and with a plan: what happened, the impact, what I know and do not know, and what I propose next.

**Structure:** STAR or CARL (see the STAR and CARL section at the top of this part).
- Situation: the error, delay or result and who needed to know.
- Task: your duty to tell, and to limit the damage.
- Action: when you told them (as soon as you were sure enough), the format (a call, then a short message), the facts, what you owned, the options.
- Result: how they reacted, what you changed, what trust looked like afterwards.

**Strong sample answer (spoken):** (Illustrative template; replace with your own real example.)
"I found a bug in my own pipeline that had inflated a weekly metric for three weeks. As soon as I confirmed it, I messaged my manager and asked for ten minutes. I said: there is an error in my code, the metric was too high, here is the size of the difference, and here is what I do not yet know, which is whether any decision used it. I proposed to correct the numbers that day and list the affected reports by the next morning. She asked two questions and thanked me for the early warning. I sent a short note to the readers with the corrected figures. I added a test so it cannot happen the same way again. I would rather say it early than let someone find it."

**Weak version (and why it fails):** "I waited until I had a perfect fix, then mentioned it at the end of a meeting." It hides the problem, delays action, and shifts the cost to others. Another weak version blames a tool or a colleague.

**What the interviewer scores:**
- Early and honest disclosure.
- Ownership without drama.
- Clarity: facts, impact, unknowns.
- A plan, not only a problem.
- Prevention afterwards.

**Make it yours:**
- Use a real error, delay or disappointing result, even a small one.
- Write the exact words you used.
- Say how soon after finding out you spoke up.
- List what you proposed and what you changed.
- Include how the other person responded.

**Script (copy and adapt):**
```
Hi [name], can I have 10 minutes today? I found a problem in [piece of work].
What happened: [one sentence].
Impact: [who or what is affected, as far as I know].
What I do not know yet: [open question].
What I propose: [fix and date], and I will update you by [time].
```

**Follow-ups:**
- "Did anyone get upset?" Yes or no, honestly, and how I handled it.
- "What if you were not sure?" Say what is confirmed and what is not, and when you will know.
- "What did you change?" A test, a review step or a checklist.

**Common mistakes:** Delay. Burying the news. Blaming. No next step. AI-era note: if an AI tool produced the error, say so plainly and what you now verify yourself.

### Q40 ⭐ 🟢 Junior level: tell me about an academic, internship or personal project where you worked with messy data. What did you do and what would you do differently?
**Asked at:** Level-specific behavioural guidance (Taro level-specific expectations, a Towards Data Science data scientist hierarchy piece, an Interview Kickstart senior data scientist guide, a MentorCruise senior and staff story workshop page, which is promotional); level framing in public guides is opinion, not a company rubric; Book 7 Part 1 notes the Meta and Microsoft level evidence with caveats; search snippets only, not opened
**Say this first (1 line):** I cleaned messy data carefully and recorded every choice I made, and with more time I would have checked those choices with someone and tested how much they mattered.

**Structure:** CARL or STAR (see the STAR and CARL section at the top of this part), pitched at junior level: "I did X, with help from Y".
- Context: the project (course, internship, personal), the dataset and what was messy.
- Action: how you found the problems (missing values, duplicates, inconsistent labels), the choices you made and why, how you checked the effect, who you asked for help.
- Result: what the cleaned data allowed, and an honest limit.
- Learning: one thing you would do differently.

**Strong sample answer (spoken):** (Illustrative template; replace with your own real example.)
"For a course project I used survey data with many missing answers and inconsistent labels. I started by counting missing values by column and looking at duplicates. I decided to drop two columns that were mostly empty and to fill the others with the median, and I wrote each decision in a notebook with the reason. I asked my instructor about the labels and she pointed out two categories meant the same thing. After cleaning, my model results were steadier. If I did it again, I would test how much each cleaning choice changed the result, instead of assuming the median was fine. I would also keep the raw file untouched from the start. That is the habit I use now."

**Weak version (and why it fails):** "I just removed the rows with missing data and ran the model." It shows no inspection, no reasons, and no awareness that dropping rows may bias the results. Another weak version claims the data was perfect after cleaning.

**What the interviewer scores:**
- Basic data care: you looked before you cleaned.
- You can explain your choices.
- You asked for help at the right moment.
- Honesty about limits.
- Ability to learn and name a specific change.

**Make it yours:**
- Use a real project from a course, internship or personal work.
- List three specific problems you found in the data.
- Write the choice and reason for each.
- Say who you asked and what they told you.
- Name what you would change, genuinely.

**Follow-ups:**
- "Why median and not drop?" Dropping loses rows and may bias; I checked how much was missing and chose by that.
- "How did you check the cleaning?" Compared results before and after.
- "Did you document it?" Yes; say where.

**Common mistakes:** Saying the data was easy. No reasons given. Claiming results you did not test. Inflating a small project. AI-era note: if an AI tool suggested the cleaning steps, say so and say what you checked yourself; interviewers will ask you to explain each choice.
