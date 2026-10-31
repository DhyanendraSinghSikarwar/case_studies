### S31 ⭐⭐ 🟡 Ambiguity: two teammates define the success metric differently mid-sprint
**Asked at:** Ambiguity and metric-definition disputes appear in data-science behavioural lists (Yardstick ambiguity page, snippet); editor-designed wording; search snippets only, not opened
**Situation:** One colleague optimises for click-through and another for completed purchases. Both think the project brief supports them. Reviews are in three days.
**Weak response:** Pick the metric you personally find more convincing, build to it, and present the result on review day. Or wait and hope the two colleagues sort it out.

**Strong response:** Treat it as a definition gap, not a vote. First, re-read the brief and write down what decision the project is meant to support. Then ask each colleague what decision their metric would change. Often click-through is a leading signal and completed purchases is the outcome, so both can be reported with a clear order: one primary, one guardrail or diagnostic. Put the proposal in a short written note to both, copy the project owner or whoever wrote the brief, and ask for a yes or no before the review. If they still disagree, ask the owner to decide and say plainly what you will show in the meantime. Report both numbers on review day, labelled, so nobody is surprised.

**Why it works:** It shows you resolve ambiguity by going back to the decision, not to personalities. A written proposal with a deadline keeps the work moving and creates a record. Reporting both metrics, labelled, is honest and keeps you from picking a side.

**What the interviewer scores:** Whether you clarify the goal before building. Whether you stay neutral between two peers. Whether you use the brief owner as tiebreaker instead of deciding alone. Whether you protect the review date.

**Say it like this:**
```
Before we argue about the metric, can we agree what decision this project is meant to change? From the brief, I read it as [decision]. If that is right, I would propose [metric A] as the primary measure and [metric B] as a diagnostic, and show both on [review day]. I will write that up today and send it to both of you and [brief owner]. If either of you disagrees, tell me by [time] and we can ask [owner] to settle it.
```

**If they push back:** If one colleague says "the brief clearly says my metric", answer: "It may, and I will quote it in the note. If the brief supports both readings, that is exactly why I want [owner] to confirm." If time runs out, show both metrics and state the open question, rather than silently choosing.

**Common mistakes:** Quietly choosing the winner. Building two full versions and burning the three days. Treating it as a personality clash. Escalating before trying a written proposal. Hiding the disagreement from the reviewers.

### S32 ⭐⭐ 🟡 Failure and ownership: a colleague finds your mistake in a code review in front of the team
**Asked at:** Own-your-error themes appear on data-science behavioural lists (codemia.io, resumegeni.com; snippets); Book 6 Part 6 Q42 covers a leakage reveal to leadership; this scenario is the moment of being caught in public, editor-designed; search snippets only, not opened
**Situation:** In a group review a colleague points out that your feature code leaks future information into training. The room goes quiet and your manager is present. Your results were already shared last week.
**Weak response:** Get defensive ("it only affects a small part"), argue about whether it is really leakage, or say nothing and fix it quietly afterwards. Another weak version is over-apologising so much that the room gets uncomfortable and no plan emerges.

**Strong response:** Pause, check the claim against the code in front of you, and if it holds, say so right there: "You are right, that leaks future information, thank you for catching it." Then state what you do not yet know (how much the results change), and commit to a concrete next step with a time: re-run with the leak removed, and update everyone who saw last week's numbers. After the meeting, send the correction in writing, with the corrected figures when you have them, and tell your manager directly what happened and what you changed in your process (for example a time-based split check before sharing results). If your quick check does not confirm the leak, say you want to verify it with the colleague after the meeting instead of arguing in front of the team.

**Why it works:** Being caught is survivable; how you respond is what people remember. Quick acknowledgement, a dated fix and an early correction to those who saw the old results show ownership and protect trust. It also shows you can take review feedback in public.

**What the interviewer scores:** Composure. Honesty without drama. Speed and completeness of the correction, including people who already saw the result. A process change, not just a patch. Not blaming the reviewer or the tool.

**Say it like this:**
```
Thanks for catching that. Let me check the split with you... yes, that feature uses information from after the prediction date, so last week's numbers are probably too optimistic. I do not know yet by how much. I will rerun with the leak removed by [day], and I will send a correction to everyone who saw the first results. Afterwards I will add a check on the time split to my review checklist.
```

**If they push back:** If a colleague says it is minor, say: "It might be, but I would rather show the corrected number than argue about it." If your manager asks why it was missed, give the honest reason (no time-split check) without excuses. For a leadership-level version of this mistake see Book 6 Part 6 Q42.

**Common mistakes:** Defending the original number. Blaming the data or the deadline. Fixing it silently so earlier readers keep the wrong figure. Promising a result before you have rerun it. Making the apology the main event.

### S33 ⭐⭐ 🟡 Failure and ownership: you overwrote a shared table with a bad job run
**Asked at:** No public page found for this exact case, editor-designed; a failure-and-ownership theme in data-science behavioural lists (codemia.io, resumegeni.com; snippet only); search snippets only, not opened
**Situation:** A job you launched replaced a table that two other teams read. You notice within ten minutes. A backup exists but restoring it needs another team's approval.
**Weak response:** Quietly try to rebuild the table yourself and hope nobody notices. Or wait to see whether anyone complains before telling anyone.

**Strong response:** Act in order. First, stop the damage: pause or disable the job so it cannot run again. Second, tell people now, not after you have fixed it: message the owners of the two reading teams and your manager with what happened, what is affected and when it started. Third, start the restore through the proper route: ask the team that must approve the backup restore, state the impact and urgency, and give them what they need (table name, backup time, what changed since). Do not bypass their approval or reach into systems you are not cleared for. While waiting, offer the readers a stopgap if one exists, such as a stale-data warning. Afterwards, write a short blameless account: cause, fix, and one safeguard, for example a write-to-staging-then-swap step or a confirmation before replacing shared tables.

**Why it works:** Containment, communication and restore happen in the right order, and the approval process is respected even under pressure. Telling people within minutes limits the harm others unknowingly take on bad data, and it builds trust.

**What the interviewer scores:** Speed of disclosure. Respect for access controls. Clear impact description. Ownership without self-blame. A preventive change.

**Say it like this:**
```
I need to flag a problem right now. A job I ran about ten minutes ago replaced [table], which your team reads. The data in it is currently wrong. I have stopped the job. A backup exists, and I am asking [approving team] to approve the restore. Please treat [table] as unreliable until I confirm it is back, and I will update you by [time].
```

**If they push back:** If the approving team says it will take a day, ask what they need to move faster and whether a partial restore is possible, but do not go around them. If a reader team is angry, acknowledge the impact and give them a time for the next update.

**Common mistakes:** Fixing first and telling later. Going around the approval. Vague messages ("some data issue"). Spending the message explaining why it was not your fault. Skipping the safeguard afterwards.

### S34 ⭐⭐ 🟡 Influence without authority: you want engineering to adopt your pipeline but they have their own roadmap
**Asked at:** Plan.md names convincing engineering to adopt your pipeline as an influence-without-authority example; codemia.io pushback pages cover related prompts (snippet only); the case wording is editor-designed; Book 9 Part 1 Q27 covers the story form; search snippets only, not opened
**Situation:** You built a feature pipeline that saves analysts time. The engineering team owns the platform and says it is not on their quarter's plan. You have no authority over their work.
**Weak response:** Keep pitching the pipeline as a great idea and ask why they will not prioritise it, or complain to your manager that engineering is blocking you. Another weak move is to build around them and hand them a surprise.

**Strong response:** Start from their plan, not your pipeline. Learn what their quarter is committed to and what they are measured on. Then translate your pipeline into their terms: does it cut support requests, reduce duplicate work, or remove a risk? Offer to reduce their cost: a small pilot, your own time for the integration, documentation, tests, and a named contact. Ask for something small and specific, such as a review of the design or a trial on one use case, instead of a place on the roadmap. Gather evidence from your own real use: hours saved, number of analysts using it. If the answer is still not this quarter, ask what would need to be true for next quarter and agree a check-in date, and keep the pipeline running on your side as it is.

**Why it works:** Influence without authority means lowering the other side's cost and tying your idea to their goals. A small, reversible first step is easier to say yes to than a roadmap change.

**What the interviewer scores:** Understanding of the other team's incentives. Willingness to do work to reduce their burden. Respectful persistence. Evidence, not opinion. Accepting a no gracefully.

**Say it like this:**
```
I understand this is not on your plan for [quarter]. I am not asking you to change it. Could we try one small thing: a thirty-minute review of the design, and a pilot on [one use case] that I would maintain? Right now it saves analysts about [measured hours]. If it holds up, we can talk about the next step then. If not, I would like to know what would make it worth your time.
```

**If they push back:** If they say they cannot support it, ask what they would need: security review, tests, ownership. Offer to do the part you can. For the story form of this skill see Book 9 Part 1 Q27 and Q11.

**Common mistakes:** Pitching features instead of their benefits. Escalating over their heads first. Claiming savings you have not measured. Building something that creates maintenance work for them without asking. Taking a no personally.

### S35 ⭐⭐ 🟡 Influence without authority: you need another team's analyst but they have no reason to help
**Asked at:** Cross-team influence appears in Book 9 Part 1 Q11 and Q35 as stories and in codemia.io pushback prompts; no public page found for this resourcing case, editor-designed; search snippets only, not opened
**Situation:** Your project needs a week of an analyst's time from a team with its own targets. Their manager says yes in principle and nothing happens. Your own manager says to sort it out yourself.
**Weak response:** Keep reminding the manager who said yes, or tell your own manager it is blocked and wait. Another weak move is to ask the analyst directly to do extra work on top of their targets without anyone agreeing.

**Strong response:** Turn a vague yes into a concrete, small agreement. Find what the other team is measured on and see where your project helps them or where you can return something: a shared dataset, a dashboard they wanted, or credit in the review. Make the ask specific: which days, which tasks, what outcome, and how it will be handed over. Then take it to the manager with a short written summary and ask for a named person and dates. Talk to the analyst too, so they know what is being asked and can say what is realistic. If it is still stuck after one follow-up, go back to your own manager and ask them to bring in the other manager, since you have done your part, or ask about a smaller scope that fits without the extra analyst.

**Why it works:** "Yes in principle" fails because it has no owner or date. A narrow request and a visible benefit make it easy to say yes. Involving the analyst treats them as a person with a workload, not a resource.

**What the interviewer scores:** Initiative within limits. Specificity of the ask. Fairness to the other team's goals. Knowing when to escalate and how.

**Say it like this:**
```
Thanks for agreeing in principle. To make it concrete, I am asking for [analyst] for [number] days between [dates] on [specific task], and in return I can share [what you offer]. Could you confirm that by [date]? If it does not fit your targets, I would rather know now so I can reduce the scope.
```

**If they push back:** If the manager says the team is overloaded, ask which smaller piece could work, or whether a later week would. If your own manager repeats "sort it out", ask what they would be comfortable with you escalating.

**Common mistakes:** Repeated vague nudges. Going around the manager to the analyst. Offering nothing in return. Escalating immediately without a written ask. Resentment in your tone.

### S36 ⭐⭐ 🟡 Influence without authority: a product manager wants to launch without the A/B test you asked for
**Asked at:** Pushing back under deadline pressure is covered by codemia.io 'push back under pressure' pages (snippet only); Book 6 Part 6 covers offline-versus-online tests with numbers; editor-designed framing; search snippets only, not opened
**Situation:** You asked for a two-week experiment before launching a ranking change. The product manager says the deadline is fixed and a test is optional. You do not report to them.
**Weak response:** Give in ("fine, ship it") or dig in and refuse, telling the product manager launch without a test is irresponsible. Both treat it as a contest.

**Strong response:** Separate what you know from what you want. Ask what the deadline is protecting and what happens if the change is wrong. Then offer options that respect the date: a shorter or smaller test, a ramp-up to a small share of traffic with a clear stop rule, or a launch with a holdout group so you can measure afterwards. Write down the risk plainly: what you cannot know without the test, and what a bad outcome would cost. Name who has the decision (the product manager, or their lead) and make sure it is a decision, not a drift. If they still launch, agree on monitoring and a rollback condition in advance, and put the plan in writing. If you think the risk affects users or the business seriously, tell your own manager, not to override anyone but so they are informed.

**Why it works:** You keep the relationship and the evidence standard at the same time. Options are easier to accept than a no. A written risk note and rollback rule protect everyone.

**What the interviewer scores:** Not caving and not blocking. Offering a middle path. Clear risk communication. Knowing the decision belongs to someone else, and informing your manager.

**Say it like this:**
```
I understand the date is fixed. A two-week test is my preference, but here are options that keep the date: roll out to [small share] first with a holdout group, and agree a stop rule in advance. What I cannot tell you without some test is whether the change helps or hurts [metric]. I will write that down so the decision is clear, and I will watch the numbers daily after launch.
```

**If they push back:** If they say the test is optional, answer: "It is your call, and I want to make it a well-informed one." For offline-versus-online test trade-offs with numbers, see Book 6 Part 6.

**Common mistakes:** Lecturing on statistics. Saying "I told you so" afterwards. Agreeing to a launch with no monitoring. Going over the manager's head before offering options. Presenting the test as the only acceptable answer.

### S37 ⭐⭐ 🟡 Team dynamics: a colleague presents your analysis as their own in a team meeting
**Asked at:** Plan.md lists credit taken by others as a team-dynamics example; the search found no page on it (a Yardstick emotional-intelligence page appeared; snippet only); editor-designed; search snippets only, not opened
**Situation:** At the weekly review a peer walks through slides built on your analysis and does not mention you. Your manager nods along. Nobody else knows the work was yours.
**Weak response:** Interrupt in the meeting to correct them, or say nothing and stew, then complain to others. Both leave the real problem unresolved, and the first can look petty in front of your manager.

**Strong response:** In the meeting, stay calm. If a natural moment exists, add something neutral that places you in the work: "Happy to add detail on the method, since I built that part." Do not accuse anyone. Afterwards, talk to the colleague privately and early: assume it might be carelessness, say what you noticed, and ask for a specific fix, such as crediting the work in the next version and in the notes. Then make your work visible in the normal way: share your analysis notebook or write-up with your manager, send a short update on what you did, and put your name on documents. If the pattern repeats after you have raised it, bring it to your manager as a factual description, not a complaint about character, and ask how work should be credited on the team.

**Why it works:** You protect the relationship and your credit at the same time. A private, factual conversation gives the colleague a chance to correct, and a written trail makes future attribution clear.

**What the interviewer scores:** Maturity and self-advocacy. Not escalating on the first instance. A concrete, factual request. Making your contribution visible without self-promotion.

**Say it like this:**
```
Hey, do you have five minutes? In today's review, the slides were based on the [analysis] I built, and my name was not mentioned. I am not assuming it was on purpose. Could we add a line crediting the analysis in the deck and in the notes? Going forward, I would like to agree who presents what before we share results.
```

**If they push back:** If they say it was a team effort, ask "Then could we say that explicitly, including who did what?" If they dismiss it, tell your manager what you shared with the colleague and ask how the team handles credit.

**Common mistakes:** Public confrontation. Accusing intent. Staying silent and resentful. Overclaiming work that was shared. Going straight to the manager without speaking to the colleague.

### S38 ⭐⭐ 🟡 Team dynamics: two teammates are in open conflict and each wants you on their side
**Asked at:** Teammate conflict prompts appear on codemia.io and in resumegeni.com behavioural lists (snippets); this third-party-in-the-middle version is editor-designed; search snippets only, not opened
**Situation:** Two colleagues you work with argue in standup about who should own a data pipeline. Afterwards each of them messages you privately with their version. Both are friendly with you.
**Weak response:** Take a side because one of them is closer to you, agree with each privately, or carry messages back and forth. It makes you part of the conflict.

**Strong response:** Listen briefly and stay neutral. Reply kindly that you have heard that they feel strongly, that you do not want to judge without both sides in the room, and that the ownership question is probably for the people who assign work to settle. Suggest they speak to each other directly, or to the manager or tech lead who decides pipeline ownership. Offer something you can do: help write down what the pipeline does, who uses it and what ownership would involve, so the decision is easier. Do not repeat what one said to the other. If the conflict keeps disrupting work, tell your manager the facts about the impact on delivery, not who said what, and ask who decides ownership.

**Why it works:** You keep both relationships by not being a messenger or judge, and you move the problem to the people who can decide. Offering neutral documentation is a real help.

**What the interviewer scores:** Neutrality. Discretion. Moving the issue to the right owner. Focus on work outcomes. Whether you avoid gossip.

**Say it like this:**
```
Thanks for telling me how you see it. I can tell it matters to you. I do not think I should take a side without hearing both of you, and the ownership question is probably for [manager or lead] to decide. Could you raise it with them, or with [colleague] directly? If it helps, I can write down what the pipeline does and who depends on it, so the decision is easier to make.
```

**If they push back:** If one says "just tell me whose side you are on", say: "I am on the side of the pipeline working. I would like both of you to be fine with the outcome." If they ask you to keep it secret, say you will not pass on what they said, but cannot promise to ignore a delivery risk.

**Common mistakes:** Agreeing with both. Passing messages. Gossiping to others. Playing therapist. Ignoring the issue until it hurts the delivery.

### S39 ⭐⭐ 🟡 Ethics and judgement: a product manager wants to join datasets in a way customers were not told about
**Asked at:** Privacy-concern prompts appear in ethics and responsible-AI interview lists in the results (hirevire, vintti, Yardstick; snippets); no public page found for this case, editor-designed. Editor note for Wave B: route through the proper internal channel and ask compliance or HR; no legal advice.; search snippets only, not opened
**Situation:** A product manager wants to link purchase data with contact details collected for a different purpose, to target messages. You are the person who would run the join. You are not sure customers agreed to this use.
**Weak response:** Run the join because the product manager asked and you only execute queries. Or refuse flatly and lecture about privacy without checking anything.

**Strong response:** Pause before running it, and say why, politely. You do not know whether customers agreed to this use, and neither do you need to decide it yourself. Ask the product manager what the purpose is and whether the privacy or data-protection team has reviewed it. Then route it to the proper internal channel: your manager, and the privacy, compliance or data-governance contact if your company has one, and read your company's data-use policy and the privacy notice customers saw. Do not give legal advice and do not guess; the people responsible for that decide. Offer alternatives meanwhile, such as segment-level analysis without personal contact details, or using only data customers consented to for this purpose. Keep it factual and in writing. Run the join only once it has been cleared through that channel.

**Why it works:** You protect customers and the company without blocking the work. Asking the right people shows judgement about the limits of your own knowledge, and offering alternatives shows you are still trying to help the product manager.

**What the interviewer scores:** Noticing the issue. Not assuming. Knowing who owns the decision. Constructive alternatives. Calm, non-accusing tone.

**Say it like this:**
```
Before I run this, I want to check one thing. These contact details were collected for [original purpose], and I am not sure customers agreed to this use. I do not want to guess. Could we ask [privacy or compliance contact] to confirm? I will write up what the join does, and in the meantime I can start on a version that uses only [data already cleared].
```

**If they push back:** If the product manager says it is fine and urgent, say you are happy to proceed once the privacy contact confirms, and that a quick check protects the project. If your own manager agrees to skip the check and you remain uncomfortable, ask for it to be put in writing and consider your company's ethics or compliance channel. Check official company sources; this is not legal advice.

**Common mistakes:** Silently complying. Silently refusing. Accusing the product manager of bad intent. Making legal claims you cannot support. Going outside the company first.

### S40 ⭐⭐ 🟡 Ethics and judgement: a teammate pastes customer data into a public AI chatbot
**Asked at:** No public page found, editor-designed; AI-tool policy and disclosure are AI-era themes in this series (Book 9 Part 1 Q17 covers how you use AI tools; Part 2 Q39 how you disclose use); policy claims are by source quality; search snippets only, not opened Editor note for Wave B: route through the proper internal channel and ask compliance or HR; no legal advice.
**Situation:** You see a colleague paste a customer support export into a public AI chat tool to speed up an analysis. Company policy, as you understand it, says not to do that. They are senior to you and in a hurry.
**Weak response:** Say nothing because they are senior and busy, or confront them loudly in front of others. Another weak move is to join in because everyone does it.

**Strong response:** First, be sure of what you saw and what the policy says: check the written policy rather than relying on your memory of it. Then speak to the colleague privately and kindly, soon, since data in a public tool cannot be pulled back: "I noticed the export went into [tool]. I thought our policy said not to. Could we check?" Give them an easy way out and suggest a compliant route, such as an approved internal tool or a redacted sample. If they brush it off, or if the data clearly included customer details, report it to the proper channel: your manager, the security or privacy team, or the compliance contact, factually and without drama. Do not investigate on your own or delete anything. Ask the channel what to do about the data already shared. Check your company's current policy and official channels; this is not legal advice.

**Why it works:** A private, kind first step respects seniority and gives a chance to fix it. A clear fallback to the official channel shows you do not leave a possible data exposure unreported. Facts, not accusations, keep trust.

**What the interviewer scores:** Courage to speak to a senior person. Checking the policy. Proportionate escalation. Offering a safe alternative. Not turning it into a personal attack.

**Say it like this:**
```
Hey, quick thing. I saw the support export go into [tool]. I thought our policy said customer data should not go into public AI tools, but I could be wrong. Could we check the policy together? If it is a problem, I think we should tell [security or privacy contact] now, since it is hard to undo. For the rest of the analysis, I can help with a masked sample or [approved tool].
```

**If they push back:** If they say everyone does it, reply that you are happy to be wrong, and ask to confirm with the policy owner. If they ask you to keep quiet, say you cannot promise that for customer data, and that reporting it early is better for both of you. For your own use of AI tools see Book 9 Part 1 Q17, and for disclosure Part 2 Q39.

**Common mistakes:** Assuming bad intent. Public call-outs. Reporting before checking the policy. Doing your own cleanup. Staying silent because of seniority.
