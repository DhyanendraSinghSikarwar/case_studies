# Question data for Book 9 Part 1. Tuple: (stars, difficulty, question text, asked-key). No answers.
NS = "; search snippets only, not opened"
B7 = "behavioural rounds appear in the Book 7 Part 1 profiles (Google, Microsoft, Amazon, Meta; see those profiles for their evidence tags and caveats)"
AS = {
 'DS': "Public data science behavioural guides (Analytics Vidhya, DataLemur, Interview Query and Coursera guides list teamwork, conflict, ambiguity, failure and influencing-without-authority prompts); commonly reported in public guides; " + B7 + NS,
 'DS2': "Public data science behavioural guides (an Analytics Vidhya list and a Coursera guide frame stakeholder, explanation and business-decision stories; a KDNuggets piece says the technical reasoning should stay visible inside the story); commonly reported in public guides" + NS,
 'ML': "Public ML engineer question banks (Yardstick, BrightHire and Jobrise pages list model-failure-in-production, data-quality, ambiguity and changed-approach prompts); commonly reported in public guides" + NS,
 'AI': "2026 AI-era behavioural guides (TheInterviewGuys, TechInterview.org, Tredence, PrachHub and FacePrep pages list daily AI-tool use, catching AI mistakes and judgement on when to use AI; PrachHub attributes one set to Amazon engineering loops, which is secondhand); commonly reported in public guides" + NS,
 'HR': "General HR-style questions listed on aggregator pages (Glassdoor data science question pages, Prepfully and InterviewPal job-change-reason pages, an edX data-industry sample list); commonly reported in public guides; " + B7 + NS,
 'ET': "Public guides list data-ethics behavioural prompts (Yardstick data-ethics page, Dataford ethics questions); commonly reported in public guides" + NS,
 'LV': "Level-specific behavioural guidance (Taro level-specific expectations, a Towards Data Science data scientist hierarchy piece, an Interview Kickstart senior data scientist guide, a MentorCruise senior and staff story workshop page, which is promotional); level framing in public guides is opinion, not a company rubric; Book 7 Part 1 notes the Meta and Microsoft level evidence with caveats" + NS,
 'LVS': "Senior and staff behavioural guidance (a MentorCruise senior and staff workshop page and an Interview Kickstart senior guide describe mentoring, prioritisation and influence stories; promotional or prep-site material); no public rubric found; editor-designed framing" + NS,
 'ED': "No public page found for this exact framing, editor-designed; the theme is adjacent to prompts in general behavioural guides" + NS,
 'REM': "No public page found for this exact framing, editor-designed; a search on cross-time-zone collaboration returned only generic remote-work pages (Data Science Dojo remote jobs guides), so no question list was located" + NS,
}
Q = []
def add(s, d, t, a): Q.append((s, d, t, a))

# ===== 3 stars =====
add(3, '🟢', "Tell me about yourself: give me a two-minute walk through your background in data, ML or GenAI work and what you are doing now.", 'HR')
add(3, '🟢', "Why do you want this role and this team, and what about the work makes it a good fit for you?", 'HR')
add(3, '🟢', "What are your two biggest strengths and one real weakness as a data or ML practitioner, and what are you doing about the weakness?", 'HR')
add(3, '🟢', "Tell me about a project you are proud of. What was the problem, what did you personally do, and what changed because of it?", 'DS')
add(3, '🟢', "Tell me about a time you had to learn a new tool, method or domain quickly to deliver something. How did you go about it?", 'DS')
add(3, '🟢', "At the end of the interview we ask what questions you have for us. Which two or three questions would you ask, and why those?", 'HR')
add(3, '🟡', "Tell me about a mistake you made in an analysis or model. How did you find it, what did you do, and what do you do differently now?", 'DS')
add(3, '🟡', "Tell me about a time you had a conflict with a teammate. What was it about and how did it end?", 'DS')
add(3, '🟡', "Tell me about a time you disagreed with a stakeholder about what the data showed or what to do next, and how you handled it.", 'DS2')
add(3, '🟡', "Tell me about a time you were given a vague or shifting problem. How did you decide what to work on first?", 'ML')
add(3, '🟡', "Tell me about a time you worked closely with engineers or product managers to ship something. What did each side need from you?", 'DS2')
add(3, '🟡', "Tell me about a time you had to deliver under a tight deadline or heavy pressure. What did you cut, protect or escalate?", 'DS')
add(3, '🟡', "Tell me about a time you received critical feedback. What was it, how did you react, and what changed afterwards?", 'DS')
add(3, '🟡', "You had five requests from different people and time for two. Tell me about a time like that and how you chose.", 'DS')
add(3, '🔴', "Tell me about a time a model, pipeline or analysis you owned failed or underperformed in production. How did you diagnose it, who did you tell, and what did you change?", 'ML')
add(3, '🔴', "Tell me about a time the data contradicted your intuition or a belief your team held. What did you do with the finding?", 'DS')
add(3, '🔴', "How do you use AI tools such as coding assistants or LLM chat in your work, and tell me about a time one gave you a wrong or risky output that you caught.", 'AI')

# ===== 2 stars =====
add(2, '🟢', "Why are you looking to leave your current role, or why did you leave your last one?", 'HR')
add(2, '🟢', "Where do you want your career to be in three to five years, and how does this role help you get there?", 'HR')
add(2, '🟢', "What kind of work energises you, and what kind of work drains you, in data or ML?", 'HR')
add(2, '🟢', "Describe the team and manager style in which you do your best work, and one situation where you adapted to a different style.", 'ED')
add(2, '🟢', "How do you keep up with fast-moving ML and GenAI developments, and tell me about one thing you learned recently that you then used?", 'AI')
add(2, '🟢', "Tell me about a time you helped a teammate succeed on something that was not your own deliverable.", 'DS')
add(2, '🟡', "Tell me about a time you changed your mind about a technical approach or a conclusion. What made you change it?", 'DS')
add(2, '🟡', "Tell me about a time you gave a colleague difficult feedback, such as on code, an analysis or their working habits. How did you say it and what happened?", 'DS')
add(2, '🟡', "Tell me about a time you mentored or coached someone more junior. What did you do, and how did you know it was working?", 'LV')
add(2, '🟡', "Tell me about a time you got people to act on your recommendation when you had no authority over them.", 'DS')
add(2, '🟡', "Tell me about a time you worked with a non-technical partner who was sceptical of data or ML work. How did you build trust?", 'DS2')
add(2, '🟡', "Tell me about a time you worked with teammates in other time zones or on a mostly remote team. What broke down, and what did you change?", 'REM')
add(2, '🟡', "Tell me about a time you noticed an ethical, privacy or fairness concern in a data or ML project. What did you do about it?", 'ET')
add(2, '🟡', "Tell me about a time you took initiative to fix a process, tool or recurring problem that nobody had asked you to fix.", 'ED')
add(2, '🟡', "Tell me about a time you caught a data quality problem before it reached a model or a decision. How did you find it and who did you tell?", 'ML')
add(2, '🟡', "Tell me about a time a teammate was struggling or underdelivering and it affected your work. What did you do?", 'DS')
add(2, '🟡', "Tell me about a time your first approach did not work and you had to change course part-way through a project.", 'ML')
add(2, '🟡', "Tell me about a cross-functional project that went well. What was your part in making it work?", 'DS2')
add(2, '🟡', "Tell me about a time you worked with someone whose working style was very different from yours. How did you make it work?", 'ED')
add(2, '🔴', "Tell me about a time you disagreed with your manager's decision, you did not get your way, and you still had to carry it out. What did you do afterwards?", 'DS')
add(2, '🔴', "Tell me about a time you were under pressure to ship or report something you were not fully comfortable with. What did you do?", 'ET')
add(2, '🔴', "Tell me about a time you had to give your manager or a team bad news about a result, a delay or an error. How did you do it?", 'ED')

# ===== 1 star =====
add(1, '🟢', "Junior level: tell me about an academic, internship or personal project where you worked with messy data. What did you do and what would you do differently?", 'LV')
add(1, '🟢', "Junior level: tell me about a time you were stuck. How long did you try on your own, when did you ask for help, and who did you ask?", 'LV')
add(1, '🟡', "Mid level: tell me about a project you owned from problem definition to delivery with little supervision. What decisions were yours?", 'LV')
add(1, '🟡', "Mid level: tell me about a time you pushed back on a request from a more senior person and what came of it.", 'LV')
add(1, '🟡', "A teammate relied heavily on AI-generated code or analysis and it contained errors. Tell me about a time something like this happened and how you handled it.", 'AI')
add(1, '🟡', "You moved into data, ML or GenAI work from another field or role. Tell me why you made that move and what you did to close the gaps.", 'ED')
add(1, '🔴', "Senior level: tell me about a time you set the technical direction for a team and had to bring sceptical people along.", 'LVS')
add(1, '🔴', "Senior level: tell me about how you have grown other people's skills across a team, beyond one-to-one mentoring.", 'LVS')
add(1, '🔴', "Staff level: tell me about a time you influenced a decision across several teams that did not report to you, with no formal authority.", 'LVS')
add(1, '🔴', "Staff level: tell me about a time you stopped or cut back a long-running project or programme. How did you decide and how did you communicate it?", 'LVS')
add(1, '🔴', "Staff level: tell me about a time you defined a strategy or roadmap for an area that was ambiguous, and how you decided what not to work on.", 'LVS')
