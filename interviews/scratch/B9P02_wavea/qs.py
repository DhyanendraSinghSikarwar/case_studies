# Question data for Book 9 Part 2. Tuple: (stars, difficulty, question text, asked-key). No answers.
NS = "; search snippets only, not opened"
AS = {
 'EXP': "Public question banks list explain-a-model-to-a-non-technical-stakeholder prompts in many variants (Dataford pages, a Prepfully answers page and a TryExponent ML-concepts guide, which advises checking whether the listener is technical); commonly reported in public guides" + NS,
 'MET': "Public question banks list translating precision, recall, PR curves and AUC-ROC for non-technical managers (several Dataford pages, one framed for a government programme manager and one for a corporate stakeholder); commonly reported in public guides" + NS,
 'STAT': "Public statistics question banks list explain-a-p-value and explain-a-confidence-interval prompts for lay audiences (an Interview Query p-value page, a TryExponent confidence-interval page, Dataford statistics lists); commonly reported in public guides" + NS,
 'AB': "Public A/B testing guides list explaining significance and intervals to a non-technical product manager (Dataford A/B pages, a DataLemur A/B guide that says to centre the answer on insights, implications and next steps); commonly reported in public guides" + NS,
 'STORY': "Data storytelling and analyst question pages (Adaface and Yardstick data-storytelling lists, a Dataford page on presenting findings to leadership, a Loopcv sample structure of what is happening, why it matters and what to recommend; Interview Query lists a take-home that asks for a summary for a marketing vice president); commonly reported in public guides" + NS,
 'NULL': "Guides on communicating A/B findings and uncertainty (a DataLemur A/B guide, a Yardstick behavioural prompt that asks how you conveyed uncertainty and still made a recommendation); no public page found for the exact null-result framing, so the framing is editor-designed" + NS,
 'STK': "Public stakeholder-management pages (Dataford questions on unclear or conflicting requirements, handling pushback and setting realistic expectations; one Dataford page tags a request-conflicts-with-model-limits question to a KPMG data scientist interview, which is a secondhand listing; a Towards Data Science stakeholder piece); commonly reported in public guides" + NS,
 'WRI': "Guidance on written communication for data scientists (Towards Data Science pieces on writing, a Yardstick communication-skills page, a HelloInterview page on design-doc experience, postmortem-writing guides, which are practitioner blogs, not interview lists); written-format prompts are partly editor-designed" + NS,
 'PRES': "General presentation guidance on hostile and hard questions (HighSpark, a board-presentation guide and other training pages, none data-science specific); no public data-science interview list found for this prompt, so it is editor-designed" + NS,
 'AI': "2026 AI-era guides (a PrachHub prompt on describing an analysis where you used AI responsibly, Dataford questions on explaining AI concepts to business stakeholders, a Gartner session title on explaining AI and ML models to stakeholders); commonly reported in public guides" + NS,
 'LLM': "Vendor and explainer pages on LLM hallucination in business (Kili, Glean, DataRobot and similar, which are marketing material, not interview lists); no interview question list found for the exact prompt, so it is editor-designed" + NS,
 'LIM': "Public guides cover explaining model limits and interpretability trade-offs to non-technical stakeholders (a Dataford page on interpretability versus predictive power, a TryExponent warning about picking an algorithm you cannot explain); commonly reported in public guides" + NS,
 'ED': "No public page found, editor-designed; the theme is adjacent to prompts in general data and analytics communication guides" + NS,
}
Q = []
def add(s, d, t, a): Q.append((s, d, t, a))

# ===== 3 stars (17) =====
add(3, '🟢', "Explain to a non-technical executive how a random forest or gradient-boosted tree model makes a prediction, in about a minute and without equations.", 'EXP')
add(3, '🟢', "A product manager's fraud model flags transactions. Explain precision and recall to them in plain words, and say which one you would worry about first.", 'MET')
add(3, '🟢', "Explain a p-value to a non-technical colleague in under a minute, and say what it does not mean.", 'STAT')
add(3, '🟢', "A marketing manager wants to say the campaign caused last month's sales rise because the two moved together. Explain correlation versus causation to them.", 'STAT')
add(3, '🟢', "A senior leader stops you in a corridor and asks what you are working on. Give a thirty-second answer that tells them why it matters.", 'ED')
add(3, '🟢', "How do you open a presentation of an analysis to a senior audience, and what do you say in the first minute?", 'PRES')
add(3, '🟡', "An A/B test shows a lift with a confidence interval, and the product manager only wants to know whether to ship. How do you explain the result?", 'AB')
add(3, '🟡', "A business owner asks how accurate your model is and how often it will be wrong. How do you answer without hiding behind one number?", 'MET')
add(3, '🟡', "You found that churn is concentrated in one customer segment. How would you structure the story for leadership, from first sentence to recommendation?", 'STORY')
add(3, '🟡', "What goes into the executive summary of an analysis, in what order, and how long should it be?", 'STORY')
add(3, '🟡', "A stakeholder asks you to 'look into why sales are down'. How do you turn that vague request into a clear analysis question?", 'STK')
add(3, '🟡', "How do you say no, or push back, on a request that is not feasible, while keeping the relationship intact?", 'STK')
add(3, '🟡', "Your experiment found no detectable effect and the team was hoping for a win. How do you present the result?", 'NULL')
add(3, '🟡', "Your project will slip by two weeks because of data problems. How do you tell the stakeholder, and what do you bring with you?", 'STK')
add(3, '🟡', "Write a short weekly status update for a project that is partly on track and partly at risk. What does it contain?", 'WRI')
add(3, '🔴', "Two dashboards show different numbers for the same metric in a leadership meeting. How do you handle it in the room and afterwards?", 'STORY')
add(3, '🔴', "A senior leader says in a meeting that your analysis is wrong. How do you defend it without getting defensive, and how do you tell if they are right?", 'PRES')

# ===== 2 stars (22) =====
add(2, '🟢', "How do you choose a chart for a message to leadership, and what would make you pick a table or plain number instead?", 'STORY')
add(2, '🟢', "Explain overfitting to a non-technical colleague with an everyday analogy, and say how you would tell them you are guarding against it.", 'EXP')
add(2, '🟢', "A business partner reads a regression output and asks what a coefficient means for their decision. How do you explain it, and what caution do you add?", 'EXP')
add(2, '🟢', "Write a short email to a stakeholder that shares a result, states how sure you are and asks for a decision. What do you put in it?", 'WRI')
add(2, '🟢', "How do you document the assumptions and caveats of an analysis so that a reader a year later does not misuse it?", 'WRI')
add(2, '🟡', "Explain customer clustering to a marketing team that wants to use the segments, including what the segments are not.", 'EXP')
add(2, '🟡', "An executive asks whether a neural network is a black box and whether that is a problem. How do you explain it?", 'EXP')
add(2, '🟡', "Explain what a large language model is to a non-technical executive who is about to buy an AI product built on one.", 'EXP')
add(2, '🟡', "Explain AUC to a non-technical manager, and tell them when it can mislead.", 'MET')
add(2, '🟡', "A model says a customer has a 30 percent chance of leaving. How do you explain probability forecasts and uncertainty to people who want a yes or no?", 'STAT')
add(2, '🟡', "A model works worse for one group of customers. How do you explain bias and fairness to leadership and what do you ask them to decide?", 'EXP')
add(2, '🟡', "Before a launch, how do you explain a model's limitations and likely failure modes to the people who will rely on it?", 'LIM')
add(2, '🟡', "You get one slide to update executives on a project. What is on it, and what do you leave out?", 'STORY')
add(2, '🟡', "How do you write a README or handover note for a model or analysis that someone else will have to run and explain?", 'WRI')
add(2, '🟡', "Engineering and product disagree on priorities for a data feature and both look to you. How do you bring them to one plan?", 'STK')
add(2, '🟡', "Six teams send you requests and you can do two this quarter. How do you prioritise, and how do you tell the other four?", 'STK')
add(2, '🟡', "How do you get a decision out of busy leaders who keep postponing it?", 'STK')
add(2, '🟡', "A launched model or dashboard is in use. How do you follow up with stakeholders, and what do you report back?", 'STK')
add(2, '🟡', "During your presentation someone interrupts repeatedly and then asks a hostile question. How do you respond?", 'PRES')
add(2, '🔴', "A business owner plans to put an LLM chatbot in front of customers. How do you explain the hallucination risk and what you would put in place?", 'LLM')
add(2, '🔴', "A model failure reached customers. Write the incident report summary: what do you include, and how do you word cause and blame?", 'WRI')
add(2, '🔴', "You used AI tools to help with an analysis and a stakeholder asks how much you can trust it. How do you explain what the AI did and what you checked?", 'AI')

# ===== 1 star (11) =====
add(1, '🟢', "You must present your results over a video call to people you cannot see. What do you change compared with presenting in a room?", 'PRES')
add(1, '🟢', "Write a Slack message escalating a blocker to a senior person. What makes it easy to act on?", 'WRI')
add(1, '🟡', "You are asked to explain a model on a whiteboard to a mixed group of engineers and business people. How do you structure it?", 'PRES')
add(1, '🟡', "Your live demo fails in front of the stakeholders. What do you do in the next two minutes?", 'PRES')
add(1, '🟡', "You are told halfway through that your slot is cut from thirty minutes to ten. How do you adapt?", 'PRES')
add(1, '🟡', "How do you summarise a long technical design document for executives, while keeping it accurate for the engineers?", 'WRI')
add(1, '🟡', "Your manager asks whether AI wrote your analysis. How do you describe your use of AI tools honestly, and what policy questions do you check first?", 'AI')
add(1, '🔴', "You have one result that must go to executives, engineers and operations staff. How do you tailor it for each group without changing the facts?", 'STORY')
add(1, '🔴', "The CFO wants a single number from your forecast. How do you communicate the range, and what do you do if they insist on one number?", 'STAT')
add(1, '🔴', "An LLM feature gave a customer a confidently wrong answer and it became a public complaint. How do you explain what happened to executives?", 'LLM')
add(1, '🔴', "A colleague sends you an AI-written analysis for review. What do you check, and how do you word your feedback so they learn from it?", 'AI')
