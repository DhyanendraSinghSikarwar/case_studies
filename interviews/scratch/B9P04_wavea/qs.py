# Scenario data for Book 9 Part 4. Tuple: (stars, difficulty, category, summary, situation, asked-at). No answers.
NS = "; search snippets only, not opened"
ED = "no public page found, editor-designed"
LEGAL = " Editor note for Wave B: route through the proper internal channel and ask compliance or HR; no legal advice."
SC, AM, FO, IN, TD, ET, CM, IV, RG = ("Stakeholder conflict", "Ambiguity", "Failure and ownership", "Influence without authority", "Team dynamics", "Ethics and judgement", "Communication", "Interview room", "Remote and global")
S = []
def add(st, d, c, summ, sit, asked): S.append((st, d, c, summ, sit, asked))

# ---------------- interview room, 3 stars ----------------
add(3,'🟢',IV,"your mind goes blank halfway through an answer",
 "You are two minutes into answering a model-evaluation question when you lose your train of thought. The interviewer is waiting and the silence is getting long. You were not nervous at the start.",
 "Blanking and what to say are covered by coaching pages (Bayt, Hays, intelligentpeople.co.uk and skillsyouneed.com results; their snippets suggest pausing, saying so honestly, restating the question or moving to a related example); commonly reported in public guides"+NS)
add(3,'🟢',IV,"a question about a method you have never used",
 "The interviewer asks how you would use survival analysis for a customer problem. You know the name and nothing more. You do not want to bluff, and you do not want to say only 'I don't know'.",
 "Handling a question you cannot answer is a standard theme in coaching pages (intelligentpeople.co.uk '4 ways', Manager Tools forum thread, CNN-syndicated KVIA piece; snippets say to be honest, show how you would reason and offer to follow up); the survival-analysis example is editor-designed"+NS)
add(3,'🟢',IV,"your connection is poor and a loud background is leaking in",
 "Ten minutes into a video interview your audio starts cutting out, and a neighbour begins drilling. The interviewer keeps asking you to repeat yourself. You have no quiet room to move to.",
 "No public page found on this exact situation, editor-designed; remote-interview guides in the results (hirevire offshore-candidate and remote-first interview pages) treat clear communication as part of remote work, vendor and guide content"+NS)
add(3,'🟢',IV,"the interviewer says 'any questions for us?' and you have covered everything",
 "The last five minutes arrive. Your prepared questions about the team, the data and the role were all answered during the loop. The interviewer smiles and waits.",
 "The questions-for-us slot is a standard final step in interview guides; Book 9 Part 1 Q6 covers which questions to ask, so this scenario is the narrower case of having none left; no public page found for that case, editor-designed"+NS)
add(3,'🟡',IV,"you freeze on the first line of a live-coding problem",
 "In a shared-editor round you are asked to write a groupby and merge in pandas. You make a syntax mistake, then a second one, and you go quiet. The interviewer has not said anything yet.",
 "Live-coding recovery is well covered in the results (PracHub 'what to do when you get stuck', interviewcake 'unstuck', algocademy recovery posts, datadriven.io live-coding page; snippets say to think aloud, ask for a hint and keep communicating); guide families, not a rubric"+NS)
add(3,'🟡',IV,"you think the interviewer's statement is wrong",
 "While discussing evaluation metrics the interviewer says accuracy is always the right choice for a balanced problem and asks you to continue on that basis. You believe the claim is too broad for the case you were asked about. You are not certain that you are right.",
 "No public page found for disagreeing with an interviewer's claim; the pushback-with-a-senior theme appears in codemia.io and a coaching post in the results (crowd-sourced, snippet only); the framing is editor-designed"+NS)

# ---------------- 3 stars, other categories ----------------
add(3,'🟢',FO,"you realise on Wednesday that Friday's deliverable will slip",
 "You promised a cleaned dataset and first model by Friday. Midweek you find that a source table has gaps that will take two more days to resolve. Nobody has asked you for an update yet.",
 "Missed deadlines and ownership are staple behavioural themes on data-science question banks (codemia.io, resumegeni.com and Analytics Vidhya list pages in the results, crowd-sourced); Book 9 Part 2 Q14 covers the slip-message wording, so this scenario is about the decision in the first hour; editor-designed"+NS)
add(3,'🟢',CM,"your manager asks for a standup update and nothing is finished",
 "Standup is in five minutes. You spent three days on a data problem and have no result to show. Your manager has said before that they want short, honest updates.",
 "Status-update prompts are a common workplace communication theme; Book 9 Part 2 Q15 covers the written weekly update, so this is the spoken, nothing-to-show case; no public page found for that exact case, editor-designed"+NS)
add(3,'🟢',RG,"the only team meeting is at 10pm your time",
 "Your team is spread across three time zones. The weekly planning call falls late at night for you, and you have joined it for two months. You are starting to miss details because you are tired.",
 "Time-zone friction is a recurring remote-work theme in the results (Dataford's cross-time-zone communication question, thoughtbot 'when async becomes the default', a Glassdoor candidate-reported overlap-hours question, techinterview.org's distributed-team playbook); the 10pm framing is editor-designed"+NS)
add(3,'🟡',SC,"a product lead says your finding 'does not match what customers tell us'",
 "Your analysis shows a popular feature has little effect on retention. The product lead says it contradicts customer feedback and asks you to leave it out of the quarterly review deck. The review is tomorrow.",
 "Stakeholder disagreement over what data show is a core theme in the results (KDnuggets 'STAR Doesn't Work' works a conflict with a marketing manager over attribution; Towards Data Science's behavioural-round piece; codemia.io difficult-stakeholder prompts, crowd-sourced); Book 6 Part 6 covers the numeric version"+NS)
add(3,'🟡',SC,"two senior stakeholders each say the other agreed to a different dashboard",
 "One director wants the dashboard split by region and another wants it by product line. Each tells you separately that the other is on board. You have one week and one set of data.",
 "Conflicting stakeholder priorities appear in codemia.io 'conflicting priorities with a teammate or stakeholder' pages (crowd-sourced; snippet only) and Book 9 Part 2 Q32 covers a two-team version; the two-directors framing is editor-designed"+NS)
add(3,'🟡',AM,"a dataset arrives with no data dictionary and a deadline tomorrow",
 "A partner team sends a table with forty columns, cryptic names and no documentation. The person who built it is on leave. You are asked for a first look by tomorrow afternoon.",
 "Ambiguity is described as the harder behavioural category for data-science roles in a Towards Data Science snippet; Yardstick's data-scientist ambiguity page lists follow-ups on prioritising with unclear requirements; the missing-dictionary case is editor-designed"+NS)
add(3,'🟡',AM,"requirements change for the third time in two weeks",
 "A stakeholder first wanted a churn report, then a churn model, and now a customer-health score with a different definition. Each change came in a short message with no discussion. Your sprint is half gone.",
 "Shifting requirements and managing expectations during a pivot appear in Yardstick's ambiguity follow-ups for data scientists (snippet); Book 9 Part 1 Q10 covers the story version; the three-change framing is editor-designed"+NS)
add(3,'🟡',FO,"you find a filter bug in a dashboard the vice president saw yesterday",
 "While checking something unrelated you discover that a date filter has been dropping a week of data. A vice president used the dashboard in a meeting yesterday. Nobody has noticed.",
 "Own-your-error prompts are a staple of data-science behavioural lists (resumegeni.com and codemia.io pages in the results; Book 9 Part 1 Q7 covers the story form); the dashboard framing is editor-designed"+NS)
add(3,'🟡',CM,"a CXO asks in a meeting why last week's metric dropped and you do not know yet",
 "Mid-meeting the CXO points to a dip in a model metric and asks for the reason. You have seen the dip but have not diagnosed it. Several people look at you.",
 "Explaining a metric change to a senior audience is a roadmap item in the plan's communication scenarios; no public page found for this in-the-room framing, editor-designed; Book 9 Part 2 Q17 covers being told you are wrong"+NS)
add(3,'🟡',TD,"a teammate on a shared deliverable is not delivering",
 "You and a colleague own two halves of a report due in a week. Their half is late, thin and not responding to messages. You have not worked with them before and your manager is travelling.",
 "Underperforming-teammate prompts are listed on codemia.io and Dataford (title-only snippets, crowd-sourced); Book 9 Part 1 Q33 covers the story form; this scenario is the 'right now' decision with a deadline"+NS)
add(3,'🟡',IN,"a senior engineer's design has a flaw and you are the most junior person in the review",
 "In a design review a senior engineer proposes writing features at serving time with logic that differs from your training code. You suspect training-serving skew. Nobody else has raised it.",
 "Pushing back on a more senior person is a common prompt (codemia.io 'walk me through a time you had to push back under pressure' pages, and a coaching post on mid versus senior pushback, snippet only); the skew framing is editor-designed"+NS)
add(3,'🟡',ET,"you notice customer emails in a notebook open to the whole company",
 "While browsing a shared drive you find a notebook with a table of customer email addresses and purchase history, visible to everyone in the company. It was saved by a colleague last month. You are not sure whether this is allowed.",
 "Data-leak and privacy prompts appear in responsible-AI and ethics question lists in the results (hirevire, vintti, Yardstick pages; snippets, not employer rubrics); the shared-drive case is editor-designed."+LEGAL+NS)
add(3,'🔴',FO,"a production model starts giving odd predictions on a Friday evening",
 "You are the one on call. Alerts show a sharp shift in scores for a model that feeds a customer-facing feature, and you cannot reach the model's usual owner. Your manager's phone is off.",
 "Incident ownership is a theme in MLOps and behavioural lists; no public page found for this exact on-call framing, editor-designed; Book 4 covers the monitoring mechanics and Book 9 Part 2 Q38 the incident write-up"+NS)
add(3,'🔴',ET,"your manager asks you to report the best of five runs as the headline number",
 "You ran five versions of an experiment and one looks clearly better by chance-prone margins. Your manager wants that one in the board update and says the others are not needed. The deck goes out tonight.",
 "A responsible-AI question list in the results asks about advocating for good practice despite pressure to speed up (Yardstick page, snippet); no public page found for metric inflation specifically, editor-designed; Book 6 Part 6 covers a multi-metric version with numbers"+NS)

# ---------------- 2 stars: interview room ----------------
add(2,'🟡',IV,"the interviewer arrives late, checks their phone and answers curtly",
 "The interviewer joins fifteen minutes late with a brief apology and shortens the slot. During your answers they glance at another screen and give one-word replies. You cannot tell whether they are interested.",
 "No public page found for late, distracted or rude interviewers (the search returned only generic curveball and blank-question pages, such as Computerworld's tough-tactics piece and CIO's interview-turning-bad article); editor-designed"+NS)
add(2,'🟡',IV,"the interviewer asks about your family plans",
 "Near the end of a friendly chat the interviewer asks whether you plan to have children soon. The question has nothing to do with the work. You feel your answer might matter.",
 "Guides on inappropriate interview questions exist (Welcome to the Jungle, UMass Humanities and Arts career guide; snippets suggest staying calm, answering only what you are comfortable with or asking what they want to learn); this book makes no legal claim. Editor note for Wave B: decide afterwards whether to raise it with the recruiter; no legal advice."+NS)
add(2,'🟡',IV,"a take-home assignment says two hours and is clearly much longer",
 "A take-home arrives with a note saying it takes about two hours. After one hour you have only loaded the data and the brief asks for modelling, a write-up and a presentation deck. You also have a full-time job.",
 "The results had little on over-long take-homes (a Wisemonk piece on async interviews and take-home tasks appeared; the snippet did not cover scope); editor-designed, with the advice to check scope with the recruiter"+NS)
add(2,'🟡',IV,"the interviewer pushes back hard on the solution you just proposed",
 "You propose a gradient-boosted model with a simple monitoring plan. The interviewer says the approach is too complicated and suggests a rule-based baseline. You still think your approach is better for the case.",
 "A live-coding results summary advised stating a decision, defending it briefly and changing your mind gracefully with new information (snippet; no dedicated source found); the case is editor-designed; Book 6 covers the technical trade-offs"+NS)
add(2,'🟡',IV,"a one-to-one interview turns into a panel of four",
 "You expected to meet one hiring manager. Three more people join, introduce themselves quickly and start asking questions in turn. You have prepared nothing for this format.",
 "Only a candidate anecdote about an unannounced panel was found (a Fishbowl post, anecdotal) and general curveball advice (Welcome to the Jungle, WebRecruit); editor-designed"+NS)
add(2,'🔴',IV,"you realise you gave a wrong answer an hour ago",
 "In the second round you stated a definition of regularisation incorrectly. Now, in the third round, you realise the mistake. The earlier interviewer may have shared notes.",
 "No public page found, editor-designed; the own-your-error theme appears in data-science behavioural lists (resumegeni.com, codemia.io; snippet only), and a coaching result suggested answering a missed question in a follow-up email"+NS)

# ---------------- 2 stars: others ----------------
add(2,'🟢',SC,"a stakeholder keeps messaging your junior teammate for quick numbers",
 "A business partner skips the team's request queue and sends your junior colleague ad hoc requests directly. The junior says yes every time and their own work is slipping. You learn about it by accident.",
 "Stakeholder-boundary and prioritisation themes appear in codemia.io stakeholder prompts and Book 9 Part 2 Q33 (priorities); no public page found for the bypass-the-queue case, editor-designed"+NS)
add(2,'🟡',SC,"a stakeholder asks you to rerun an analysis a third time until it looks better",
 "The first result disappointed a stakeholder, so you reran it with a different window. They are still not happy and ask for another rerun with different filters. They say they just want something to show their director.",
 "The KDnuggets snippet works a conflict where a marketing manager wanted data to show one channel drove all conversions; this scenario is a variant, editor-designed; Book 6 Part 6 Q28 covers headline-metric picking with numbers"+NS)
add(2,'🟡',AM,"your manager says 'find out what drives churn' and is away for a week",
 "You are handed an open-ended question and your manager is unreachable until next Monday. Colleagues have different ideas of what churn means here. Your next check-in is in two weeks.",
 "Vague-problem prompts are on Yardstick's data-scientist ambiguity page and in a Towards Data Science snippet; Book 9 Part 2 Q11 covers turning 'look into why sales are down' into a question; this version adds an absent manager, editor-designed"+NS)
add(2,'🔴',AM,"a stakeholder expects a classifier in a month and you have no labels",
 "A team wants a model that flags risky support tickets by the end of the month. No tickets have ever been labelled and nobody has time to label them. They already told their director it is coming.",
 "Plan.md lists no-labelled-data as an ambiguity example; interview lists mention vague problem statements (Yardstick, Towards Data Science snippets); the labelling-expectation case is editor-designed; Book 2 and Book 6 cover technical options"+NS)
add(2,'🟡',AM,"two teammates define the success metric differently mid-sprint",
 "One colleague optimises for click-through and another for completed purchases. Both think the project brief supports them. Reviews are in three days.",
 "Ambiguity and metric-definition disputes appear in data-science behavioural lists (Yardstick ambiguity page, snippet); editor-designed wording"+NS)
add(2,'🟡',FO,"a colleague finds your mistake in a code review in front of the team",
 "In a group review a colleague points out that your feature code leaks future information into training. The room goes quiet and your manager is present. Your results were already shared last week.",
 "Own-your-error themes appear on data-science behavioural lists (codemia.io, resumegeni.com; snippets); Book 6 Part 6 Q42 covers a leakage reveal to leadership; this scenario is the moment of being caught in public, editor-designed"+NS)
add(2,'🟡',FO,"you overwrote a shared table with a bad job run",
 "A job you launched replaced a table that two other teams read. You notice within ten minutes. A backup exists but restoring it needs another team's approval.",
 "No public page found for this exact case, editor-designed; a failure-and-ownership theme in data-science behavioural lists (codemia.io, resumegeni.com; snippet only)"+NS)
add(2,'🟡',IN,"you want engineering to adopt your pipeline but they have their own roadmap",
 "You built a feature pipeline that saves analysts time. The engineering team owns the platform and says it is not on their quarter's plan. You have no authority over their work.",
 "Plan.md names convincing engineering to adopt your pipeline as an influence-without-authority example; codemia.io pushback pages cover related prompts (snippet only); the case wording is editor-designed; Book 9 Part 1 Q27 covers the story form"+NS)
add(2,'🟡',IN,"you need another team's analyst but they have no reason to help",
 "Your project needs a week of an analyst's time from a team with its own targets. Their manager says yes in principle and nothing happens. Your own manager says to sort it out yourself.",
 "Cross-team influence appears in Book 9 Part 1 Q11 and Q35 as stories and in codemia.io pushback prompts; no public page found for this resourcing case, editor-designed"+NS)
add(2,'🟡',IN,"a product manager wants to launch without the A/B test you asked for",
 "You asked for a two-week experiment before launching a ranking change. The product manager says the deadline is fixed and a test is optional. You do not report to them.",
 "Pushing back under deadline pressure is covered by codemia.io 'push back under pressure' pages (snippet only); Book 6 Part 6 covers offline-versus-online tests with numbers; editor-designed framing"+NS)
add(2,'🟡',TD,"a colleague presents your analysis as their own in a team meeting",
 "At the weekly review a peer walks through slides built on your analysis and does not mention you. Your manager nods along. Nobody else knows the work was yours.",
 "Plan.md lists credit taken by others as a team-dynamics example; the search found no page on it (a Yardstick emotional-intelligence page appeared; snippet only); editor-designed"+NS)
add(2,'🟢',TD,"a junior colleague asks you the same questions every day",
 "A new joiner messages you several times a day with questions they could answer from the documentation. You like helping but your own work is falling behind. They seem anxious about asking the team lead.",
 "Mentoring prompts exist on behavioural lists (Book 9 Part 1 Q26 covers the story form); no public page found for this day-to-day load case, editor-designed"+NS)
add(2,'🟡',TD,"two teammates are in open conflict and each wants you on their side",
 "Two colleagues you work with argue in standup about who should own a data pipeline. Afterwards each of them messages you privately with their version. Both are friendly with you.",
 "Teammate conflict prompts appear on codemia.io and in resumegeni.com behavioural lists (snippets); this third-party-in-the-middle version is editor-designed"+NS)
add(2,'🟡',ET,"a product manager wants to join datasets in a way customers were not told about",
 "A product manager wants to link purchase data with contact details collected for a different purpose, to target messages. You are the person who would run the join. You are not sure customers agreed to this use.",
 "Privacy-concern prompts appear in ethics and responsible-AI interview lists in the results (hirevire, vintti, Yardstick; snippets); no public page found for this case, editor-designed."+LEGAL+NS)
add(2,'🔴',ET,"you notice the model errs more for one language group days before launch",
 "In a last review you see that error rates are clearly higher for users writing in one regional language. Launch is Monday and the team has already announced it. Fixing it would take at least two weeks.",
 "Bias-found-in-a-model prompts are common in the fairness question lists in the results (hirevire and Yardstick pages; a snippet asks how to handle fairness goals conflicting with business objectives); Book 6 Part 6 Q13 covers a numeric fairness trade-off; this is the 'right now' version"+NS)
add(2,'🟡',ET,"a teammate pastes customer data into a public AI chatbot",
 "You see a colleague paste a customer support export into a public AI chat tool to speed up an analysis. Company policy, as you understand it, says not to do that. They are senior to you and in a hurry.",
 "No public page found, editor-designed; AI-tool policy and disclosure are AI-era themes in this series (Book 9 Part 1 Q17 covers how you use AI tools; Part 2 Q39 how you disclose use); policy claims are by source quality"+NS+LEGAL)
add(2,'🟡',CM,"a stakeholder replies angrily to a message you meant as neutral",
 "You wrote a short message saying a result did not support their plan. They reply within minutes and call it unhelpful and unfair. A director is copied on the thread.",
 "Written-communication and tone problems are a general theme; no public page found for this exact case, editor-designed; Book 9 Part 2 Q41 covers escalation messages"+NS)
add(2,'🟡',CM,"a long email thread has fourteen replies and you are asked to summarise the decision",
 "A thread about whether to retrain a model has contradictory opinions and unclear owners. Your manager asks you to write the one-paragraph summary of where things stand. You are not sure a decision has been made.",
 "No public page found, editor-designed; Book 9 Part 2 Q45 covers summarising a design document and Q15 the weekly update"+NS)
add(2,'🟢',RG,"your question in a chat channel is unanswered for a day and you are blocked",
 "You asked a teammate in another time zone about a schema change, and they have not replied by the end of your day. You cannot continue the analysis without the answer. Your deadline is two days away.",
 "Async-communication norms are covered in the results (thoughtbot's async piece, OfferZen's async-communication post, Dataford's remote communication question; snippets only); the blocked-question framing is editor-designed"+NS)
add(2,'🟡',RG,"your new manager expects written pre-reads and you are used to talking things through",
 "Your manager works in a different region and wants a short written proposal before any meeting. You are used to explaining ideas live. Your first two meetings were postponed until you sent a document.",
 "Cultural and process guidance in this book is process-level only (Book 8 convention); remote and global team guides in the results (techinterview.org distributed-teams playbook; a Teamblind thread on working across zones, anecdotal) support the written-first theme; editor-designed framing"+NS)

# ---------------- 1 star ----------------
add(1,'🟡',SC,"an engineering lead refuses a logging change you need",
 "Your model needs a new event logged by the product's backend. The engineering lead says it is not on the roadmap and ends the call quickly. You suspect they feel overloaded rather than opposed.",
 "Cross-team friction is covered by codemia.io stakeholder-pushback prompts (snippets); no public page found for the logging-request case, editor-designed; niche, stronger at mid to senior level"+NS)
add(1,'🔴',SC,"your manager promised a client-facing team a feature without asking you",
 "In a meeting you learn that your manager told another department that your model would be available next month. You had not been told. The date is not realistic.",
 "Plan.md lists a launch date your model cannot meet as a stakeholder-conflict example; Book 6 Part 6 Q1 covers the numeric version, and this scenario is the manager-promised, you-find-out variant; editor-designed, senior-leaning"+NS)
add(1,'🟢',AM,"your first week and no documentation on a handed-over project",
 "You join a team and inherit a project whose previous owner has left. There are some notebooks, no README and a stakeholder expecting a monthly report. Your manager says you will figure it out.",
 "Ambiguity prompts in the results (Yardstick, Towards Data Science snippets) focus on mid-project cases; the new-joiner handover case is editor-designed and niche"+NS)
add(1,'🔴',FO,"a post-incident review blames 'the data team' and the cause is your commit",
 "After an outage the review document says the data team caused it. Your commit was the change that triggered it, but the wording avoids names. Your manager says it is better not to make waves.",
 "No public page found, editor-designed; blameless-review practice is covered in Book 9 Part 2 Q38 (incident report summary); senior-leaning"+NS)
add(1,'🔴',IN,"you want to retire a legacy report owned by a long-serving manager",
 "A report costs the team hours each month and few people read it. Its owner is a long-serving manager who built it and is proud of it. You have no authority over it and nobody else wants to raise it.",
 "No public page found, editor-designed; Book 6 Part 6 Q43 covers retiring a scorecard with numbers; this is the soft-skills framing, senior-leaning"+NS)
add(1,'🟡',IN,"a peer team keeps rebuilding what yours already built",
 "Another team's data scientists have built three features that already exist in your shared library, because they did not know about it. You would like a common standard, but neither team reports to you.",
 "Cross-team standards and influence themes appear in Book 9 Part 1 Q35 and Q48 as stories; no public page found for this duplication case, editor-designed"+NS)
add(1,'🟡',TD,"a new manager changes how the team works and others stay silent",
 "A new manager requires daily written updates and removes the weekly planning meeting. In the team chat, people say little, and in private they complain. You think the change has costs and some benefits.",
 "Team-dynamics themes appear in values-round guides and codemia.io prompts (snippets); no public page found for this exact case, editor-designed; niche"+NS)
add(1,'🟡',TD,"a teammate seems burned out and quality is slipping",
 "A colleague who used to be careful has started missing messages and making small errors in reviews. They told you privately last week that they are exhausted. Their manager has not noticed.",
 "Yardstick's emotional-intelligence page for data scientists is the nearest result (snippet only); no public page found for this case, editor-designed; niche"+NS)
add(1,'🔴',ET,"leadership wants a customer-facing chatbot live before the safety tests finish",
 "You asked for two weeks of red-team testing on an LLM chatbot. A senior leader wants it live this week because a competitor announced something. The tests so far have found a few harmful answers.",
 "A responsible-AI list in the results asks for an example of advocating responsible practice despite pressure to expedite (Yardstick, snippet); Book 2 covers evaluation and guardrails technically; senior-leaning, editor-designed wording"+NS)
add(1,'🟡',CM,"a loud colleague dominates the meeting and your recommendation is never heard",
 "In a planning meeting one colleague talks over others and steers the group away from your proposal. You have the data to show why it matters. The meeting ends in ten minutes.",
 "Meeting-dynamics prompts are on communication lists (Book 9 Part 2 Q36 covers interruptions during a presentation); no public page found for this case, editor-designed"+NS)
add(1,'🟡',CM,"your manager gives you blunt negative feedback in a team review",
 "In front of the team your manager says your last two analyses were hard to follow and late. You feel the criticism is partly fair and partly missing context. Everyone is waiting for your reaction.",
 "Receiving critical feedback is on behavioural lists (Book 9 Part 1 Q13 covers the story form); no public page found for the in-the-moment case, editor-designed"+NS)
add(1,'🟡',RG,"your video interviewer's camera is off and you cannot see any reaction",
 "In a remote interview you present a project to a panel with cameras off. You hear no responses and cannot tell whether your points are landing. Ten minutes in you are still talking.",
 "Presenting to people you cannot see is covered by Book 9 Part 2 Q40; remote-interview guides in the results (the bestpracticeinstitute remote-first interview guide, a Wisemonk piece; snippets only) treat remote interviews as their own format; editor-designed"+NS)
add(1,'🟡',RG,"a deadline lands at the start of the other region's morning and your reviewer is asleep",
 "A deliverable is due when your counterpart's working day begins, which is the middle of your night. Your reviewer in the other region will sign off only after you hand over. A small error found late would cost a day.",
 "Time-zone and deadline friction is covered in the results (thoughtbot, techinterview.org's distributed-teams playbook, a tianpan.co forum thread on 24-48 hour feedback loops, anecdotal); the handover-clash framing is editor-designed"+NS)
add(1,'🟡',RG,"a colleague in another zone hands over a pipeline at their end of day with no notes",
 "A teammate finishes their day and drops a message saying the pipeline is yours now. There are no notes and a failing job. They will not be online for another ten hours.",
 "Async handover is covered by general remote-work guides in the results (thoughtbot, OfferZen; snippets only); no public page found for the no-notes case, editor-designed"+NS)
