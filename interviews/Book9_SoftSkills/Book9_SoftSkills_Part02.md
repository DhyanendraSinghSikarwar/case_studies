# Book 9 — Part 2: Communication, Data Storytelling and Stakeholder Management

**Topic:** How to explain, write, present and handle things as a data science, ML engineer or GenAI practitioner. Explaining models and statistics to non-technical people (random forest and boosted trees, regression, clustering, neural networks, LLMs, accuracy, precision and recall, AUC, p-values, confidence intervals, A/B results, correlation versus causation, overfitting, bias and fairness, probability forecasts, limitations, hallucination risk), storytelling with data (structure, charts, executive summaries, one-slide updates, null results, conflicting numbers, defending an analysis), written communication (status updates, emails, READMEs, design-doc summaries, incident reports, Slack escalations, documenting assumptions), stakeholder management (vague requests, expectations, saying no, scope changes, prioritising, delays, decisions, post-launch follow-up), presentation skills (openings, hostile questions, whiteboards, failed demos, time cuts, remote talks) and AI-era communication (explaining and disclosing AI-assisted analysis, reviewing AI-written work, explaining LLM limits).

**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 17, ⭐⭐ 22, ⭐ 11)  |  **Date:** 2026-10-31  |  **Status:** Complete (answers merged, checked, reviewed)

**Scope note:** this part is editor guidance for the communication questions in data, ML and GenAI interviews. The answers in Wave B are templates, not scripts to memorise, and every one ends with a prompt to use your own real example. In this part the label Structure means the explanation or writing structure, and Strong sample answer means the spoken explanation or the short written sample (an email, an update, a summary). It gives no pay or negotiation figures and no legal advice. Behavioural stories ("tell me about a time") belong to Book 9 Part 1; numeric trade-off and stakeholder scenarios belong to Book 6 Part 6; metric definitions to Book 6 Part 1. This part asks "how would you explain, write, present or handle X". Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch result snippet or summary only (see research_notes/Book9_Part02_sources.md). The searches returned question banks (Dataford, Interview Query, TryExponent, Prepfully, Yardstick, Adaface), a few Towards Data Science pieces, general presentation-training pages and vendor LLM explainers. They agree on themes, not on wording, and none is a company rubric. 'Asked at' lines name guide families; 'commonly reported in public guides' is used only where a snippet supports the theme. Thin coverage: live-demo failures, remote presentations, Slack escalations, README writing, post-launch follow-up and the exact null-result and reconcile-two-dashboards framings; those lines say 'editor-designed' or name the nearest guidance. No company is named as asking a question except where a snippet listed it, and that listing is secondhand. Star counts and difficulty tags are editorial.

---

## A pattern for explaining anything to a non-technical person

This is editor guidance [G], not a company requirement. Public guides repeat the same core advice: check who is listening, tie the result to a decision, and use a concrete example (sources: research_notes/Book9_Part02_sources.md, snippets only). Treat the steps as a checklist for your own words, not a script.

1. **Name the decision.** Say what the listener has to decide or do, in one sentence. Everything else serves that.
2. **Answer first.** Give the conclusion or the plain-language meaning before any method.
3. **Use one familiar picture.** One analogy or one concrete example from their world. Not three.
4. **Give the number with its meaning.** Say what the figure means in people, orders or money, and how sure you are, in a range or in words such as "likely" and "not yet known".
5. **Say what it does not mean.** One common misreading and the correction, because that is where decisions go wrong.
6. **Name the limit and the safeguard.** Where it can fail, and what you will check or who reviews it.
7. **Check understanding and stop.** Ask "what would you want to know before you decide?" and leave room. Offer the detail, do not pour it out.

Worked example (illustrative; replace with your own): a p-value for a product manager. Decision: ship or not. Answer first: "The lift looks real but is small." Picture: "If the change did nothing, how often would we still see a gap this big by luck? The p-value answers that." Number: "About one time in twenty." Not meant: "It is not the chance the change works." Limit: "It says nothing about whether the lift is big enough to matter, so look at the range." Check: "Does the range change your decision?"

---

### Q1 ⭐⭐⭐ 🟢 Explain to a non-technical executive how a random forest or gradient-boosted tree model makes a prediction, in about a minute and without equations.
**Asked at:** Public question banks list explain-a-model-to-a-non-technical-stakeholder prompts in many variants (Dataford pages, a Prepfully answers page and a TryExponent ML-concepts guide, which advises checking whether the listener is technical); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** It is a panel of many simple checklists that each give a verdict and then vote, and the vote becomes a likelihood we can act on.

**Structure:** (follows the pattern in "A pattern for explaining anything to a non-technical person" above; this is the one-minute version)
1. Decision: what the executive will use the prediction for (for example, who gets a retention call).
2. Answer first: "It combines many small rule-sets into one score."
3. One picture: a panel of reviewers who each ask a few yes-or-no questions.
4. Difference in one line: forest means independent votes; boosting means each new reviewer studies the earlier ones' mistakes.
5. What the score means: a likelihood, not a certainty.
6. Limit and safeguard: hard to explain in one sentence, so you show top drivers and test on unseen cases.
7. Stop and ask what they need before deciding.

**Strong sample answer (spoken):** (illustrative; replace the churn example with your own)
"Think of a panel of reviewers. Each reviewer asks a short run of yes-or-no questions about a customer, like 'has usage dropped lately?', and gives a verdict. One reviewer can be wrong, so we train hundreds, each looking at slightly different data, and let them vote. In a random forest every reviewer votes equally. In a boosted model they work in sequence, and each new reviewer concentrates on the cases the earlier ones got wrong. The final answer is the vote, which we read as a likelihood, never a certainty. It performs well on this kind of table of customer data, but no single rule explains a score. So we show which factors matter most, and we test it on customers it has never seen. What would you want to know before you decide how to use the list?"

**Weak version (and why it fails):** "It builds many decision trees using bagging and random feature subsets, and boosting fits residuals with gradient descent." It is correct and useless to the listener: jargon, no decision, no limit, no picture.

**What the interviewer scores:**
- Plain language with no equations and no unexplained terms.
- One analogy that is accurate enough not to mislead.
- A link to the decision, not a lecture on method.
- Honest limits (not fully explainable, likelihood not certainty).
- Staying inside a minute and inviting a question.

**Make it yours:**
- Pick a model you really built or used and the real decision it fed.
- Replace the churn example with that decision and one feature you know mattered.
- Say the limit you actually found, such as a segment where it did worse.
- Time yourself aloud; if it runs past a minute, cut a sentence, not speed.
- Have a plain answer ready for "why not a simpler model?" from your own comparison.

**Follow-ups:**
- *Why is it a black box?* "Each piece is simple, but hundreds together are hard to trace. We use factor rankings and example-level explanations, and we say they are approximations."
- *Why not just one tree?* "One tree is easy to read but swings with small data changes. The group is steadier."

**Common mistakes:**
- Saying "bagging", "residuals" or "ensemble" without a plain meaning.
- Using three analogies in one minute.
- Implying the score is a guarantee.
- Never mentioning a limit.
- Memorising this wording; live follow-ups quickly expose a rehearsed or AI-written explanation, so build it from your own project.

### Q2 ⭐⭐⭐ 🟢 A product manager's fraud model flags transactions. Explain precision and recall to them in plain words, and say which one you would worry about first.
**Asked at:** Public question banks list translating precision, recall, PR curves and AUC-ROC for non-technical managers (several Dataford pages, one framed for a government programme manager and one for a corporate stakeholder); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** Precision is "when we raise an alert, how often is it right"; recall is "of all the real fraud, how much do we catch", and I would start by asking which mistake costs more.

**Structure:** (the explanation pattern, applied to two metrics)
1. Decision: where to set the alert threshold and how many reviewers are needed.
2. Define both with one concrete group of 100 or 1,000 transactions, not formulas.
3. Show the trade-off: catching more fraud means more false alarms.
4. Say which to worry about first, and the condition that flips it.
5. Name the limit: fraud is rare, so "accuracy" looks great and means little.
6. Close with the question that decides it: what does a miss cost versus a false alarm?

**Strong sample answer (spoken):** (illustrative numbers; replace with yours)
"Say we flag a hundred transactions. Precision is how many of those hundred really are fraud. If sixty are, our alerts are right sixty percent of the time. Recall is the other side: of all the fraud that happened, how much did we catch? If we caught half, the other half got through. You can't push both up for free. Flag more and you catch more fraud, but your reviewers drown in false alarms and customers get blocked for no reason. I'd worry about recall first if one missed fraud is very costly and reviewers have spare capacity. I'd worry about precision first if false blocks are driving customers away or the review team is full. So the real question for you is, what does one missed fraud cost, compared with one wrongly blocked customer?"

**Weak version (and why it fails):** "Precision is TP over TP plus FP, and recall is TP over TP plus FN; accuracy is misleading here." Right, but the listener cannot use it, and it never answers "which one first".

**What the interviewer scores:**
- Definitions a manager could repeat to someone else.
- A committed answer on "which first", with the reasoning and condition.
- Awareness that rare events make accuracy misleading.
- Linking the metric to cost and team capacity.
- Asking about the business context rather than guessing.

**Make it yours:**
- Use a real classification project of yours and what a false alarm and a miss cost there.
- Replace the fraud example only if you can describe the real consequences.
- Find the threshold trade-off you actually saw, in words not numbers if you cannot recall them.
- Practise the 100-transactions picture without writing it down.

For the worked numeric version, see Book 6 Part 6, "Q25" (the CEO and the 30 percent precision question).

**Follow-ups:**
- *What about AUC?* "It says how well the model ranks risky above safe overall, regardless of threshold. It does not tell you where to set the alert line."
- *Can we have both high?* "Only by a better model or better data; moving the threshold just trades one for the other."

**Common mistakes:**
- Defining with formulas only.
- Refusing to pick ("it depends") without saying on what.
- Quoting accuracy on rare events.
- Forgetting the human cost of false alarms.

### Q3 ⭐⭐⭐ 🟢 Explain a p-value to a non-technical colleague in under a minute, and say what it does not mean.
**Asked at:** Public statistics question banks list explain-a-p-value and explain-a-confidence-interval prompts for lay audiences (an Interview Query p-value page, a TryExponent confidence-interval page, Dataford statistics lists); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** A p-value asks "if nothing had really changed, how often would we still see a gap this big by luck?", and it is not the chance that the change works.

**Structure:** (the explanation pattern in a one-minute form)
1. Decision: what hangs on it (ship, stop, collect more data).
2. Plain meaning: the "if nothing changed" question.
3. A tiny picture: a coin that lands heads more than you expect.
4. The number in words: "about one time in twenty".
5. What it does not mean (the top misreading), and one more: it says nothing about size.
6. Where to look next: the range of plausible effect sizes and the cost of being wrong.

**Strong sample answer (spoken):** (illustrative; replace with your own example)
"Suppose we change a button and more people sign up. The p-value answers one question: if the button actually did nothing, how often would we still see a gap this big, just by luck? If it's about one in twenty, that is unusual but not impossible, so we treat the result as suggestive. What it does not tell you is the chance the button works. It is also silent on size: a tiny gain can have a very small p-value if we have lots of data, and a large gain can look uncertain with little data. So I'd never decide on the p-value alone. I'd look at how big the gain could plausibly be, and whether even the low end is worth shipping. Does that match how you were reading it?"

**Weak version (and why it fails):** "It's the probability that the null hypothesis is true." That is the classic misreading, and a statistician in the room will stop listening.

**What the interviewer scores:**
- A correct meaning in plain words.
- Explicitly naming what it does not mean.
- Separating "unlikely by luck" from "big enough to matter".
- Brevity and a concrete example.
- Calm, not condescending, tone.

**Make it yours:**
- Use a real test or comparison from your work, with the decision that followed.
- Recall one time a p-value was misread around you; describe it without naming people.
- Practise the "one in twenty" phrasing until it is natural, and check it fits your threshold.
- Write your own one-line "what it does not mean".

**Follow-ups:**
- *Why not just say 95 percent confident it works?* "That sentence is about a different quantity. The p-value starts from 'assume nothing changed', so it cannot give the chance that the change works."
- *What if p is 0.06?* "It is not a cliff. I'd report the range and the cost of a wrong call, and consider more data."

**Common mistakes:**
- Saying "the probability the result is a fluke" (close, but invites the wrong reading).
- Lecturing about null hypotheses.
- Ignoring effect size.
- Treating the cut-off as a pass or fail line.

### Q4 ⭐⭐⭐ 🟢 A marketing manager wants to say the campaign caused last month's sales rise because the two moved together. Explain correlation versus causation to them.
**Asked at:** No public page found for this exact framing, editor-designed; adjacent to general data-communication and statistics question banks that cover correlation versus causation for lay audiences; search snippets only, not opened
**Say this first (1 line):** Sales and the campaign moving together is a good reason to look closer, but it does not yet show the campaign caused the rise, because something else may have moved sales too.

**Structure:** (pattern: answer first, one picture, say what it does not mean)
1. Acknowledge what is true: the two did move together, which is worth a look.
2. Plain statement: moving together is not the same as one causing the other.
3. One picture from their world: ice cream sales and sunburn both rise in summer; the sun drives both.
4. Name the likely "something else" for this case (season, a price change, a competitor, a product launch).
5. Offer a better test: compare with places or weeks that did not get the campaign, or a holdout.
6. Give them a sentence they can safely say now.

**Strong sample answer (spoken):** (illustrative; replace with your own case)
"You are right that sales rose in the same month as the campaign, and that is a good reason to look closer. But two things moving together doesn't prove one caused the other. Ice cream sales and sunburn both rise in summer, and neither causes the other, the sun drives both. Last month may have had a seasonal lift, a price change, or a competitor running low on stock. To see what the campaign did, we need a comparison: regions or customers who did not get it, or a group we hold back next time. Until then, a fair line for the report is 'sales rose after the campaign, and we are testing how much was the campaign'. Would a small holdout group be possible for the next push?"

**Weak version (and why it fails):** "Correlation does not imply causation." Tidy and true, but it dismisses their point, gives them nothing to do, and can feel like a put-down.

**What the interviewer scores:**
- Respecting the stakeholder's reasoning before correcting it.
- A simple, accurate picture.
- Naming plausible confounders for the case in front of you.
- A practical path to the causal answer.
- A wording they can use today.

**Make it yours:**
- Think of a real correlation someone treated as causal in your work or studies, and the confounder.
- Use your own domain's version of the ice cream picture if it fits better.
- Name one comparison group you could genuinely build with the data you know.
- Rehearse a gentle opening sentence that does not start with "actually".

For a numeric treatment of the same situation, see Book 6 Part 6, "Q29" (the CEO and the holiday campaign).

**Follow-ups:**
- *So it didn't work?* "Not at all. It may have worked. We just can't tell yet how much of the rise it explains."
- *We can't run a test; what then?* "Compare against similar regions or periods and be open that it is an estimate with a range."

**Common mistakes:**
- Opening with the slogan and nothing else.
- Sounding as if the campaign was useless.
- Using a heavy example with no link to their business.
- Giving no next step.

### Q5 ⭐⭐⭐ 🟢 A senior leader stops you in a corridor and asks what you are working on. Give a thirty-second answer that tells them why it matters.
**Asked at:** No public page found, editor-designed; the theme is adjacent to prompts in general data and analytics communication guides; search snippets only, not opened
**Say this first (1 line):** Give the problem, what I am doing about it, and why it matters to them, in three sentences, then stop and let them ask.

**Structure:** (editor-designed question; a corridor version of the pattern)
1. Problem in their language: one sentence on the pain, tied to something they care about.
2. What I am doing: one sentence, plain verbs, no tool names.
3. Why it matters and when: the expected benefit and the next milestone, or an honest "too early to say".
4. One easy ask or hook: "happy to show you in five minutes."
5. Stop. Thirty seconds is about 70 spoken words.

**Strong sample answer (spoken):** (illustrative; replace with your project)
"We are working on why customers cancel in their first three months. Right now the support team finds out after they have gone. I'm building a way to flag who is likely to leave early, so the team can reach out while there's still time. We have a first version running on last year's data, and next month we test whether the outreach actually keeps people. If it works, it gives us a cheaper way to protect revenue than discounts. If it doesn't, we will know why, and that is useful too. I can send you a one-page summary if that would help."

**Weak version (and why it fails):** "I'm training a gradient-boosted model with some feature engineering on our customer table." The leader hears activity with no purpose, so the conversation ends or they move on, unimpressed.

**What the interviewer scores:**
- Leading with the problem and the benefit, not the method.
- Brevity and structure under social pressure.
- Honest status (no overclaiming).
- Awareness of the listener's priorities.
- A natural, human delivery.

**Make it yours:**
- Write your real current project in three sentences: problem, action, why it matters.
- Remove every tool name and acronym, then read it aloud against a timer.
- Add a truthful status line, including what is still uncertain.
- Make a second version for an interviewer who asks "what are you working on?"
- Do not stretch the benefit beyond what you know.

**Follow-ups:**
- *How will you know it worked?* "We compare people we contacted with similar people we did not, on whether they stayed."
- *What do you need from me?* "Name one owner on the support side so we can run the pilot." Only ask for what you really need.

**Common mistakes:**
- Describing the method first.
- Running to two minutes.
- Overselling an early result.
- Ending without a hook or an offer.

### Q6 ⭐⭐⭐ 🟢 How do you open a presentation of an analysis to a senior audience, and what do you say in the first minute?
**Asked at:** General presentation guidance on hostile and hard questions (HighSpark, a board-presentation guide and other training pages, none data-science specific); no public data-science interview list found for this prompt, so it is editor-designed; search snippets only, not opened
**Say this first (1 line):** I open with the decision they need to make and my answer in one sentence, then say what I will cover and what I need from them.

**Structure:** (editor-designed question; general presentation guidance, not a company rubric)
1. Anchor: one sentence on why we are here and the decision at stake.
2. Answer: the headline finding or recommendation, up front.
3. Roadmap: two or three points, so they know how long it takes.
4. Confidence: one line on how sure you are and what the main caveat is.
5. The ask: what you want from them today (a decision, feedback, a go-ahead).
6. Then move into the evidence, and leave the method for an appendix.

**Strong sample answer (spoken):** (illustrative; replace with your analysis)
"Thanks for the time. We're here to decide whether to extend the loyalty offer to all customers or keep it targeted. My recommendation is to keep it targeted, because the broader offer costs us more than it brings back in the group we tested. I'll take ten minutes: what we saw, why I trust it, and what could change the answer. I'm fairly confident about the direction, less so about the exact size. By the end I would like a yes or no on running a wider test next quarter. Let me start with what we saw."

**Weak version (and why it fails):** "First, a bit of background on the data and the approach we took..." Senior listeners lose patience before the point appears, and the first minute is when they decide how closely to listen.

**What the interviewer scores:**
- Leading with the answer and the decision.
- Respect for senior time.
- Calibrated confidence stated early.
- A clear ask.
- Presence: steady pace, no apology for being nervous.

**Make it yours:**
- Take a real analysis you have presented or will present and write its first 60 seconds in the five steps.
- State the real decision it informs and who owns it.
- Say your actual caveat, not a generic one.
- Say it aloud once with a timer and once to a colleague; ask them what they remember.

**Follow-ups:**
- *What if they interrupt in the first minute?* "Answer the question, then link back: 'that is exactly the third point, so let me jump there.'"
- *What if there is no decision, just information?* "Say that: 'no decision today, I want you to know X because it will affect Y'."

**Common mistakes:**
- Starting with methodology and background.
- Burying the recommendation on slide 12.
- Apologising for the slides.
- Opening without saying what you need from the room.

### Q7 ⭐⭐⭐ 🟡 An A/B test shows a lift with a confidence interval, and the product manager only wants to know whether to ship. How do you explain the result?
**Asked at:** Public A/B testing guides list explaining significance and intervals to a non-technical product manager (Dataford A/B pages, a DataLemur A/B guide that says to centre the answer on insights, implications and next steps); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** Give the ship or no-ship answer first, then the likely size of the lift as a range, then what the range means for the risk of shipping.

**Structure:** (answer first, range second, risk third)
1. Recommendation in one sentence: ship, do not ship, or wait, with the reason.
2. Likely lift, in the unit they care about (orders, sign-ups), as a range.
3. What the interval means: "the true effect is plausibly anywhere in this range".
4. Where the range crosses zero or the cost line: say so plainly.
5. The cost of being wrong either way, and what we do to limit it (staged rollout, monitoring).
6. One caveat about the test (duration, segment, novelty effect), then ask what else they need.

**Strong sample answer (spoken):** (illustrative; replace with your test)
"My recommendation is to ship, with a staged rollout. The new checkout looks better, we saw more completed orders, and the likely gain is somewhere between a small bump and a fairly solid one. I'd plan on the middle, not the top. Even at the low end of that range it is not harmful, so the downside is small. The test ran for two weeks, which may be too short to see whether the effect fades once the novelty wears off, so I'd ship to a portion first and watch it for a month. If the low end of the range had dipped below zero, my answer would be wait, and I would say so. What would you want to be true before you commit fully?"

**Weak version (and why it fails):** "The p-value is below 0.05, so it's significant." The listener learns nothing about size or risk, and "significant" will be heard as "big".

**What the interviewer scores:**
- A clear recommendation, not a statistics lecture.
- Presenting uncertainty as a range tied to a decision.
- Handling the "does the range include no change" case honestly.
- Naming test limits (duration, novelty, who was in it).
- A proposal that manages the risk.

**Make it yours:**
- Use a real experiment of yours, even a small one, and recall what decision followed.
- Write the recommendation sentence first, then the range in the real unit.
- Find the honest limit of your own test and put it in the answer.
- Decide in advance what range would change your answer from ship to wait.
- Do not borrow numbers from this sample.

For a numeric version where the online test comes out flat, see Book 6 Part 6, "Q35".

**Follow-ups:**
- *Just tell me yes or no.* "Yes, ship, staged. If you want a single figure, plan on the middle of the range."
- *The range includes zero.* "Then I cannot say it works. I'd either run longer or ship only if the change is cheap and safe, and say that it is a bet."

**Common mistakes:**
- Saying "significant" without size.
- Hiding the range to sound confident.
- Declining to recommend anything.
- Forgetting the test's limits.

### Q8 ⭐⭐⭐ 🟡 A business owner asks how accurate your model is and how often it will be wrong. How do you answer without hiding behind one number?
**Asked at:** Public question banks list translating precision, recall, PR curves and AUC-ROC for non-technical managers (several Dataford pages, one framed for a government programme manager and one for a corporate stakeholder); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** One number hides how and where the model is wrong, so I give three plain things: how often it is right, what kind of mistakes it makes, and where it struggles.

**Structure:** (explanation pattern: decision, answer, one example, limit)
1. Ask what the owner will do with the output; "accurate enough" depends on that.
2. Give the overall hit rate in plain words, with a range if you can.
3. Split the errors into two kinds, in their language (false alarms and misses), with a rough count per 100 or 1,000 cases.
4. Say where it is weaker (a segment, a rare case, new customers).
5. State the safeguard: a human check, a threshold, a review of the worst cases.
6. Offer a way to track it over time.

**Strong sample answer (spoken):** (illustrative; replace the numbers with your own, or leave them as words)
"In plain terms: out of every hundred cases, it gets most of them right, but 'most' hides two different mistakes. Sometimes it flags something that turns out fine, a false alarm. Sometimes it misses something real. Those cost you different amounts, so I'd rather show you both than one average. It is also weaker on new customers, because we have less history on them, so I'd keep a person checking those. I'd expect it to be wrong a noticeable share of the time, and the share can change as your customers change, so we'll track it monthly and tell you if it slips. Which mistake hurts your business more? That tells me where to tune it."

**Weak version (and why it fails):** "It's ninety-four percent accurate." Without the base rate, the error types or the weak spots, the owner may assume it is right ninety-four percent of the time on the cases that matter, which is often false.

**What the interviewer scores:**
- Refusing to hide behind a single figure, without drowning the listener.
- Plain description of error types.
- Honest weak spots and monitoring.
- Asking about the business cost of errors.
- Calm tone when the answer is "it will be wrong sometimes".

**Make it yours:**
- Pull up a real model's evaluation and write its weak spot in one plain sentence.
- Translate its real errors into counts per hundred or thousand cases.
- Name the real safeguard you used or would propose.
- Rehearse the line "it will be wrong sometimes, here is how we handle that".

For a worked numeric case, see Book 6 Part 6, "Q25" (precision and recall for a CEO).

**Follow-ups:**
- *So can I trust it?* "For this use, with this check, yes. For cases like X, no, and I would send those to a person."
- *Why not make it more accurate?* "Past a point, more data or better features help; just turning a dial trades one kind of mistake for the other."

**Common mistakes:**
- Quoting a single accuracy figure.
- Promising it will improve without a plan.
- Hiding the weak segment.
- Answering with jargon the owner cannot repeat.

### Q9 ⭐⭐⭐ 🟡 You found that churn is concentrated in one customer segment. How would you structure the story for leadership, from first sentence to recommendation?
**Asked at:** Data storytelling and analyst question pages (Adaface and Yardstick data-storytelling lists, a Dataford page on presenting findings to leadership, a Loopcv sample structure of what is happening, why it matters and what to recommend; Interview Query lists a take-home that asks for a summary for a marketing vice president); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I would tell it as a short chain: here is where we are losing customers, here is why it matters, here is what I think is behind it, and here is what to do next.

**Structure:** (a story arc for leadership; see also Loopcv-style "what is happening, why it matters, what to recommend" in the sources note, snippet only)
1. Headline: one sentence with the finding and the size of the stake.
2. Context: the overall churn picture in one line, so the segment stands out.
3. The evidence: one chart that shows the segment against the rest; point at the gap.
4. The likely cause: what you know, what you suspect, and how confident you are.
5. Recommendation: one action, an owner, a first step and how success will be measured.
6. Risks and what you do not know yet.
7. The ask: what you need decided today.

**Strong sample answer (spoken):** (illustrative; replace the segment and causes with your own)
"Most of our customer losses come from one group: customers who joined through the partner channel in their first three months. They are a small share of customers but a large share of those we lose. If we fix that group, we protect most of the revenue at risk. What I can see is that they leave after a billing event and rarely contact support first. My best guess is that the pricing was explained differently to them, but I haven't confirmed it. My recommendation is a small pilot: a clearer billing message plus a check-in call, with a comparison group. I'd like your approval for the pilot and a named owner on the partner team."

**Weak version (and why it fails):** "I ran a cohort analysis across twelve variables and segment C stood out." The audience gets a method, no stake, no cause and no action, so nothing is decided.

**What the interviewer scores:**
- A headline and recommendation, not a tour of the analysis.
- One clear chart idea.
- Separating evidence from guesses.
- A concrete, owned next step with a way to measure it.
- Fit with what leaders actually decide.

**Make it yours:**
- Take a real finding of yours and write the headline sentence first, in the leader's unit (revenue, customers).
- List what you know versus what you only suspect and say both.
- Pick the single chart that would carry the story.
- Name a real owner type and a measurable result for the recommendation.
- Practise telling it in two minutes without slides.

**Follow-ups:**
- *Could it be something else?* "Yes. That is why the pilot has a comparison group and why I'd rule out two other explanations first."
- *What if they only give you one slide?* "Headline, the one chart, the recommendation and the ask; the rest goes in an appendix."

**Common mistakes:**
- Starting with data cleaning and method.
- Showing six charts.
- Stating a guess as a cause.
- Ending with "thoughts?" instead of an ask.

### Q10 ⭐⭐⭐ 🟡 What goes into the executive summary of an analysis, in what order, and how long should it be?
**Asked at:** Data storytelling and analyst question pages (Adaface and Yardstick data-storytelling lists, a Dataford page on presenting findings to leadership, a Loopcv sample structure of what is happening, why it matters and what to recommend; Interview Query lists a take-home that asks for a summary for a marketing vice president); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** The summary goes first, stands alone, and runs half a page at most: the answer, the evidence, the caveats and the next step, in that order.

**Structure:** (a writing structure, editor guidance [G]; teams differ, so check any template your team already uses)
1. Question or decision: one line on what this analysis was for.
2. Answer or recommendation: the headline, in plain words.
3. Key evidence: two or three findings, each with the number and what it means.
4. Confidence and caveats: how sure you are, and the main thing that could change the answer.
5. Next step and owner: what should happen, by whom, and what you need decided.
6. Length: about a quarter to half a page, so a busy reader gets it in under a minute; details go below or in an appendix.
7. Test: could someone act on this having read only this part?

**Strong sample answer (spoken):** (a short written sample, illustrative; replace with your own)
Summary
"Question: should we keep the free-delivery threshold as it is? Recommendation: keep it for now; lowering it is unlikely to pay back. Evidence: (1) customers just under the threshold mostly add one item to qualify, so it is working; (2) a lower threshold would cut delivery income on orders we already get; (3) the one group that might respond, first-time buyers, is small. Confidence: moderate. The data covers one quarter and may miss a holiday effect. Next step: run a small test on first-time buyers next quarter; owner: growth team; decision needed from you by the end of the month. Method and charts are in the appendix."

**Weak version (and why it fails):** A summary that starts "We pulled data from three sources and cleaned it..." and runs a page. The decision is on page two, the caveat is missing, and the busy reader stops after the first paragraph.

**What the interviewer scores:**
- Putting the answer first.
- Brevity and ordering by what the reader needs.
- Caveats and confidence stated, not buried.
- A clear next step and owner.
- Awareness that the summary may be the only part read.

**Make it yours:**
- Take a real analysis and write its summary in the five parts, then cut it to half a page.
- Ask a colleague who did not do the work to say what they would do after reading it.
- Check that each number comes with a meaning.
- State your actual caveat, even if it is uncomfortable.
- If AI helps you tighten wording, you stay responsible for every claim; check each number against the source before sending.

**Follow-ups:**
- *Where does the method go?* "In an appendix or a linked doc; the summary says only how much to trust it."
- *What if the answer is 'we don't know yet'?* "Say that first, say what you tried, and say what would settle it."

**Common mistakes:**
- Writing the summary last and making it a table of contents.
- Leaving out the recommendation.
- Reporting findings with no stakes.
- Making it so long nobody reads it.

### Q11 ⭐⭐⭐ 🟡 A stakeholder asks you to 'look into why sales are down'. How do you turn that vague request into a clear analysis question?
**Asked at:** Public stakeholder-management pages (Dataford questions on unclear or conflicting requirements, handling pushback and setting realistic expectations; one Dataford page tags a request-conflicts-with-model-limits question to a KPMG data scientist interview, which is a secondhand listing; a Towards Data Science stakeholder piece); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I would not start pulling data; I would first turn "look into it" into a question, a decision and a deadline, and agree them with the stakeholder in writing.

**Structure:** Use the pattern in "A pattern for explaining anything to a non-technical person" above, adapted for a request.
1. Decision: what will you do differently depending on the answer?
2. Scope the words: sales of what (units, revenue, one region, one product), down compared with what (last month, last year, plan), and since when.
3. Check the basics: is the drop real, or a data, calendar or definition change? Say you will do this first.
4. List two or three candidate causes you will test, such as price, traffic, a channel, stock, or a competitor.
5. Agree the output and date: a one-page answer, not a dashboard.
6. Confirm back in two lines, and say what you will not cover.

**Strong sample answer (spoken):** Illustrative; replace with your own. "First I would ask what decision this feeds, because the answer changes what I look at. Then I would pin down the words: down compared with when, in which region or product, and measured how. Before I look for causes I would check the drop is real, meaning no change in how sales are counted, no missing data and no calendar effect. Then I would list a few likely causes, such as price, traffic, a channel or stock, and test them in order. I would agree what you get and by when, for example a one-page summary by Friday, and write it back to you so we both agree. If one cause explains most of it, I would say so, and if none do, I would say that too."

**Weak version (and why it fails):** "I would pull all the sales data and look for trends." No question, no decision, no date. You may do a week of work and answer something nobody asked, and the stakeholder cannot judge what you are doing.

**What the interviewer scores:**
- Do you ask about the decision before the data?
- Can you make a vague word (down, better) measurable?
- Do you check that the drop is real before explaining it?
- Do you agree scope and output, and confirm in writing?
- Do you stay calm and curious, not irritated by a vague ask?

**Make it yours:**
- Think of a real vague request you received, even in a course project or internship.
- Write the two clarifying questions you actually asked, or would ask now.
- Write the one-line question you ended up with.
- Note what you left out of scope and how you said so.
- If you have no work example, use a course or club project and say that.

**Script (copy and adapt):**
```
Thanks for flagging this. So I answer the right question, can I check three things?
1. What decision will this help with?
2. Down compared with what, where, and since when?
3. What would a useful answer look like, and by when?
I will first check the drop is real, then test the most likely causes. I will send you a short summary of what I understood before I start.
```

**Follow-ups:**
- What if they cannot say what decision it feeds? "I offer two or three example decisions and ask which is closest. If none, I propose a small first pass and say what it will and will not tell them."
- What if the drop is just a data problem? "That is a finding. I show the evidence, say what was wrong, and say who should fix it."
- What if they keep changing the question? "I write down the current version and the date, and ask whether the earlier one is dropped or added."

**Common mistakes:**
- Starting analysis with no agreed question.
- Asking so many questions that you look unhelpful; ask three, not ten.
- Skipping the check that the drop is real.
- Promising "the reason" when several causes may exist.
- AI-era note: an AI tool can suggest causes quickly, but the stakeholder context is yours; do not paste its list as your plan, and be ready to explain why you chose these checks.

### Q12 ⭐⭐⭐ 🟡 How do you say no, or push back, on a request that is not feasible, while keeping the relationship intact?
**Asked at:** Public stakeholder-management pages (Dataford questions on unclear or conflicting requirements, handling pushback and setting realistic expectations; one Dataford page tags a request-conflicts-with-model-limits question to a KPMG data scientist interview, which is a secondhand listing; a Towards Data Science stakeholder piece); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I say no to the request as stated, yes to the need behind it, and always bring an alternative.

**Structure:** A four-step pattern [G, editor guidance].
1. Understand the need: ask what they are trying to achieve before you refuse.
2. Say the constraint plainly and early: what is not feasible, and the reason in their terms (time, data, risk), not jargon.
3. Offer options: a smaller version, a later date, a different method, or what you would need to make it possible.
4. Hand over the decision: let them pick, and confirm in writing.

Tone: firm on facts, warm on the goal. Avoid "can't"; say what you can do and what it would take.

**Strong sample answer (spoken):** Illustrative; replace with your own. "Thanks for explaining what you need; the goal makes sense. I want to be straight with you: with the data we have today, I cannot give a reliable prediction for every single customer, and if I tried, we would act on guesses. Here is what I can do. In two weeks I can give you a ranked list of the customer groups most at risk, with a clear note on how sure we are. If you need the individual level, we would need about a month of extra data collection. Which of these fits your plan better? I will write it up so we are agreed, and I am happy to review it with your team."

**Weak version (and why it fails):** "That is not possible with our data." It closes the conversation, offers nothing, and sounds like a refusal to help. The stakeholder goes around you or loses trust. The opposite failure is agreeing and delivering something unreliable.

**What the interviewer scores:**
- Do you separate the request from the need?
- Is the reason clear and in plain words?
- Do you bring options, not only a refusal?
- Does the stakeholder keep the decision, with the trade-off visible?
- Is the relationship in better shape after the conversation?

**Make it yours:**
- Pick one real request you had to push back on, or a realistic one from your projects.
- Write the need behind it and the exact constraint, with evidence you really had.
- Write two options you would offer.
- Say it aloud once, and cut any jargon.
- Do not claim you pushed back if you did not; say what you would do.

**Script (copy and adapt):**
```
I want to help you get [their goal]. As described, [the request] is not something I can deliver reliably because [one plain reason].
What I can do: Option A, [smaller or sooner version]. Option B, [fuller version], which needs [what it takes].
Which is closer to what you need? I will send a short note with the choice so we are aligned.
```

**Follow-ups:**
- What if they insist? "I restate the risk once, ask them to decide with it written down, and escalate to my manager only if the risk is serious."
- What if your manager already said yes? "I go to my manager first with the facts and options, then we go back together."
- How do you say no to a senior person? "Same steps, with more preparation: evidence, options and a clear recommendation."

**Common mistakes:**
- A flat no with no alternative.
- Apologising so much that the message is lost.
- Using technical reasons they cannot judge.
- Saying yes and hoping to fix it later.
- AI-era note: AI tools can draft a polite refusal, but it may sound generic; interviewers ask for the real case, so rehearse with your own example.

### Q13 ⭐⭐⭐ 🟡 Your experiment found no detectable effect and the team was hoping for a win. How do you present the result?
**Asked at:** Guides on communicating A/B findings and uncertainty (a DataLemur A/B guide, a Yardstick behavioural prompt that asks how you conveyed uncertainty and still made a recommendation); no public page found for the exact null-result framing, so the framing is editor-designed; search snippets only, not opened
**Say this first (1 line):** A result of "no detectable effect" is a finding, so I report what we learned, how sure we are, and what to do next.

**Structure:** Explanation structure [G].
1. Answer first: "We did not see a difference we can distinguish from noise."
2. Say what was tested and for how many users, in plain words.
3. Give the range: the likely effect is between a small loss and a small gain, so we can rule out large gains.
4. Separate "no effect" from "not enough data to tell"; say which one it is.
5. State what it means for the decision: stop, iterate, or run longer, with the cost of each.
6. Say what you learned that helps the next test.

Do not search for a subgroup that "worked" after the fact.

**Strong sample answer (spoken):** Illustrative; replace with your own. "I know we were hoping for a win. Here is where we are. After [the planned run time], we did not see a difference we can tell apart from chance. The likely effect is between a small drop and a small gain, so a big win is unlikely. Our test could detect the size of change we planned for, so this is a real answer, not just a lack of data. My recommendation is not to ship it for the sake of the metric. We did learn that users clicked the new button but did not buy more, which suggests the problem is later in the flow. I suggest we test that next. If you want to run longer, here is the cost."

**Weak version (and why it fails):** "It was not significant, so it failed." It sounds like blame, hides what was learned, and conflates "no evidence of a change" with "no change". The other trap is spinning a subgroup result to rescue it.

**What the interviewer scores:**
- Do you report honestly without drama?
- Do you distinguish no effect from low power?
- Do you give a range and a recommendation?
- Do you resist after-the-fact subgroup digging?
- Do you turn the result into a next step?

**Make it yours:**
- Use a real test or analysis of yours that did not show an effect, even a course one.
- Write the plain-language result in two sentences.
- Say how sure you were and why, from your own work.
- Name what you learned and the next step you proposed.
- If you have none, describe how you would present a hypothetical one and label it as such.

**Follow-ups:**
- What if the team wants to run it longer? "I ask what size of effect we would still care about, work out the time that needs, and compare it with the cost of waiting."
- What if one segment looks positive? "I report it as an idea to test next, not as a finding, because I looked in many places."
- What if the sponsor wants it shipped anyway? "I state the evidence and the risk, and say the decision is theirs; I suggest a way to monitor it."

**Common mistakes:**
- Calling it a failure, or burying it.
- Saying "no effect" when the test was too small.
- Hunting for a subgroup win.
- Leaving out a next step.
- AI-era note: an AI summary may phrase a null result too confidently; check the wording against your range.

### Q14 ⭐⭐⭐ 🟡 Your project will slip by two weeks because of data problems. How do you tell the stakeholder, and what do you bring with you?
**Asked at:** Public stakeholder-management pages (Dataford questions on unclear or conflicting requirements, handling pushback and setting realistic expectations; one Dataford page tags a request-conflicts-with-model-limits question to a KPMG data scientist interview, which is a secondhand listing; a Towards Data Science stakeholder piece); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I tell them early, in person or on a call, with the reason, the new date, what it affects, and options.

**Structure:** Delay-message pattern [G].
1. Early: as soon as you are fairly sure, not on the due date.
2. Headline: "It will take two more weeks."
3. Cause in plain words, and what you have already tried.
4. Impact: what moves, what does not, who is affected.
5. Options: cut scope, add help, ship in phases, or accept the date.
6. Confidence in the new date, and the next check-in.
7. Confirm in writing after the call.

Bring: the evidence of the data issue, a revised plan, and a recommended option.

**Strong sample answer (spoken):** Illustrative; replace with your own. "I want to flag something early. The project will take about two weeks longer than planned. The reason is the data: [the source] has gaps in [the period], and the model cannot be trusted until we fix them. I have already [checked with the data owner and tried a workaround]. Here is the impact: the first version moves from [date] to [new date], and the report for [team] is not affected. I see three options: ship a smaller version on the original date, wait for the full version, or add a second person on the data cleanup. I recommend the smaller version first. I am fairly confident about the new date, and I will update you every Friday. I will send this in writing today."

**Weak version (and why it fails):** "There were some data issues, so it is a bit delayed." It is vague, offers no date or options, and sounds like an excuse. Worse is staying silent until the deadline.

**What the interviewer scores:**
- Do you communicate early and directly?
- Is the cause clear without blame?
- Do you bring a revised plan and options?
- Do you state confidence and a check-in rhythm?
- Do you take ownership of the new date?

**Make it yours:**
- Use a real delay you managed, even in a course or internship project.
- Note when you told people, relative to when you knew.
- Write your headline sentence and your options.
- Check the dates and facts against your records.
- If it never happened, practise with a made-up case and label it so.

**Script (copy and adapt):**
```
Subject: [Project] timeline update: new date [date]

Hi [name],
Heads-up: [project] will land on [new date], about two weeks later than planned.
Why: [one plain sentence on the data issue].
What it affects: [what moves, what does not].
Options: (A) [smaller version on the original date], (B) [full version on the new date], (C) [add help].
My recommendation: [option and reason].
I will update you on [day] each week. Can we talk for ten minutes on [time]?
```

**Follow-ups:**
- What if the cause was your own mistake? "I say so briefly, say what I changed, and focus on the plan."
- What if they push to keep the date? "I show which option keeps it and what quality or scope we give up."
- What if it slips again? "I tell them at the first sign, with what changed since last time."

**Common mistakes:**
- Telling people late.
- Blaming another team.
- Bringing a problem with no options.
- Giving a new date you are not confident in.
- AI-era note: AI can polish the email, but the date and cause must come from you; expect to be asked how you estimated the new date.

### Q15 ⭐⭐⭐ 🟡 Write a short weekly status update for a project that is partly on track and partly at risk. What does it contain?
**Asked at:** Guidance on written communication for data scientists (Towards Data Science pieces on writing, a Yardstick communication-skills page, a HelloInterview page on design-doc experience, postmortem-writing guides, which are practitioner blogs, not interview lists); written-format prompts are partly editor-designed; search snippets only, not opened
**Say this first (1 line):** A good status update lets a busy reader see in ten seconds whether the project is fine, what is at risk, and what I need from them.

**Structure:** Writing structure [G, editor guidance].
1. Overall status in one line (green, amber or red, with a plain word as well).
2. Done since last time: two or three items, as outcomes.
3. Next: two or three items with dates.
4. Risks: what, how likely, the impact, and what you are doing about it.
5. Asks: decisions or help needed, with an owner and a date.
6. Keep it under about 150 words and put the answer in the first line.

**Strong sample answer (spoken):** Short written sample, illustrative; replace with your own. "Project churn model, week of [date]. Status: amber. Overall on track for [date], one risk. Done: data pipeline running daily; first model beats the current rule on the holdout set. Next: add the new features by [date]; review with the product team on [date]. Risk: the [source] feed has missing days, which could make the results unreliable. Likelihood medium; impact one to two weeks. I am checking with the data owner and have a fallback source. Ask: can [name] confirm by [date] who owns the feed? Without that, the date moves."

**Weak version (and why it fails):** A long list of every task done, with no status, no risk and no ask. The reader must dig for the point, so they either skip it or ask for a meeting. Or the opposite: "all good" while a risk is hidden.

**What the interviewer scores:**
- Is the status clear in the first line?
- Do you state risks plainly, with a plan?
- Is the ask specific, with an owner and date?
- Is it short and written for the reader?
- Do you avoid both hiding bad news and alarmism?

**Make it yours:**
- Take a real project of yours and write its update in this format, in under 150 words.
- Use only facts you can show; no invented progress.
- Pick one real risk and write its impact in plain words.
- Check that one ask has a named person and date.
- Show the update to a friend and ask what they understood in ten seconds.

**Script (copy and adapt):**
```
[Project], week of [date]
Status: [green/amber/red]. [One-line reason].
Done: [outcome 1]; [outcome 2].
Next: [item and date]; [item and date].
Risk: [what]. Likelihood [low/medium/high]; impact [plain words]. Mitigation: [what you are doing].
Ask: [decision or help] from [name] by [date].
```

**Follow-ups:**
- When do you mark red? "When the date or the goal will be missed without a decision from someone else; I say so and what I need."
- How long should it be? "Short enough to read in a minute; links for detail."
- What if there is no news? "I say so, in one line, and keep the rhythm."

**Common mistakes:**
- Burying the status.
- Listing tasks, not outcomes.
- Risks with no mitigation or ask.
- Writing only when things are good.
- AI-era note: AI tools can tidy a draft; make sure every claim is something you can back up if asked.

### Q16 ⭐⭐⭐ 🔴 Two dashboards show different numbers for the same metric in a leadership meeting. How do you handle it in the room and afterwards?
**Asked at:** Data storytelling and analyst question pages (Adaface and Yardstick data-storytelling lists, a Dataford page on presenting findings to leadership, a Loopcv sample structure of what is happening, why it matters and what to recommend; Interview Query lists a take-home that asks for a summary for a marketing vice president); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** In the room I stay calm, do not argue about which is right, and promise a short follow-up; afterwards I trace the difference and write down one agreed definition.

**Structure:** Two-stage pattern [G].
In the room:
1. Acknowledge: "Good catch, the two numbers do not match."
2. Do not guess or pick a winner; offer likely reasons only if you are sure, such as definitions or timing.
3. Say what the decision needs: does the gap change today's decision? If not, carry on.
4. Commit: who finds out, and by when.

Afterwards:
5. Trace: compare definitions, filters, date ranges, time zones, data refresh times and sources.
6. Fix or document: one source of truth, one written definition, an owner.
7. Tell everyone who saw the numbers, briefly.

**Strong sample answer (spoken):** Illustrative; replace with your own. "In the meeting I would say: good catch, those two numbers do not match, and I would rather not guess which is right. Does the gap change the decision we are making today? If not, let us keep going using [one figure, with the caveat]. I will find the reason and send a note by tomorrow noon. Afterwards I would compare how each dashboard defines the metric, which filters and dates it uses, and when it last refreshed. Usually it is a definition or timing difference. I would write down one agreed definition, name an owner, and fix or label the other dashboard. Then I would tell the people who were in the room what we found."

**Weak version (and why it fails):** Defending your dashboard on the spot, or saying "the other one is wrong" without checking. Or going quiet and hoping nobody notices. Both cost trust in your numbers.

**What the interviewer scores:**
- Do you stay composed and avoid guessing?
- Do you link the gap to the decision?
- Do you have a concrete way to trace a mismatch?
- Do you close the loop with a definition and owner?
- Do you protect trust in data generally?

**Make it yours:**
- Recall a real mismatch you met in a project or course, or describe the likely sources in your own data.
- Write the two or three checks you would actually run.
- Write your one-sentence line for the room.
- Note who you would tell and how.
- Do not claim you resolved it if you did not.

**Script (copy and adapt):**
```
Good catch. The two numbers do not match, and I would rather check than guess.
For today's decision, I suggest we use [figure] with the caveat that it may change slightly.
I will find the reason and send a note by [time]. Can we agree [name] owns the final definition?
```

**Follow-ups:**
- What if someone says your number is wrong? "I say I will verify, and I do, with both sources side by side."
- What if both are right? "Then the definitions differ; I document both and recommend one for decisions."
- How do you prevent it? "One metric definition, an owner, and the dashboards read from the same source."

**Common mistakes:**
- Arguing in the room.
- Guessing a cause with no check.
- Not following up in writing.
- Blaming the other team.
- AI-era note: if an AI tool built either dashboard or query, you still own the number; be able to explain the logic.

### Q17 ⭐⭐⭐ 🔴 A senior leader says in a meeting that your analysis is wrong. How do you defend it without getting defensive, and how do you tell if they are right?
**Asked at:** General presentation guidance on hostile and hard questions (HighSpark, a board-presentation guide and other training pages, none data-science specific); no public data-science interview list found for this prompt, so it is editor-designed; search snippets only, not opened
**Say this first (1 line):** I listen to the claim fully, ask what they are seeing, test it against my work live or soon after, and say honestly if they are right.

**Structure:** Hard-question pattern [G].
1. Pause and listen to the whole point; do not interrupt.
2. Repeat it back to check you understood.
3. Separate the claim: wrong data, wrong method, or wrong conclusion?
4. Answer what you can with evidence; show your check, not your confidence.
5. If you cannot settle it in the room, say what you will check and when.
6. Afterwards, re-run the check; if they are right, say so plainly and fix it.

To tell if they are right: look for a specific, testable claim (a missing segment, a definition, a bias) and test it.

**Strong sample answer (spoken):** Illustrative; replace with your own. "Thank you for raising that. Let me check I understand: you think the result is wrong because [their reason]. I looked at that when I [did the specific check], and what I found was [result]. If I am missing something, I would like to know. Can you tell me what you are seeing that I am not? If we cannot settle it here, I will re-run the numbers with your assumption and send you both versions by [time]. If it changes the conclusion, I will tell the whole group, not just you."

**Weak version (and why it fails):** Repeating "the analysis is correct" more firmly, or caving instantly: "you may be right, I will redo it." The first shows defensiveness, the second shows you did not trust your own work.

**What the interviewer scores:**
- Do you stay calm and curious under challenge?
- Do you separate evidence from ego?
- Do you test their claim rather than defend or fold?
- Can you say "you are right" when they are?
- Do you follow up with a specific time?

**Make it yours:**
- Think of an analysis of yours that was challenged, or likely would be.
- List the three most probable objections and the check for each.
- Write your own sentence for "I will verify and come back".
- Practise out loud with a friend playing the sceptic.
- Describe only checks you really did or would do.

**Follow-ups:**
- What if they are senior and clearly upset? "Same steps, a calm tone, and I offer a short one-to-one after the meeting."
- What if you are wrong? "I thank them, correct it, and tell everyone who saw the first version."
- What if they are wrong? "I show both versions of the number and let the evidence decide; I keep the tone neutral."

**Common mistakes:**
- Defending before understanding.
- Folding without checking.
- Taking it personally.
- Promising to follow up with no time.
- AI-era note: if your analysis used an AI tool, be ready to explain each step without it; "the tool did it" is not a defence.

### Q18 ⭐⭐ 🟢 How do you choose a chart for a message to leadership, and what would make you pick a table or plain number instead?
**Asked at:** Data storytelling and analyst question pages (Adaface and Yardstick data-storytelling lists, a Dataford page on presenting findings to leadership, a Loopcv sample structure of what is happening, why it matters and what to recommend; Interview Query lists a take-home that asks for a summary for a marketing vice president); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I start from the message, not the chart: what should the reader take away, and what is the simplest way to show that.

**Structure:** Chart-choice steps [G].
1. Write the one-sentence message first.
2. Pick the form for the message: change over time (line), comparison (bars, sorted), part of a whole (a stacked bar, or a few numbers), relationship (scatter), a single key figure (a plain number).
3. Use a table when the reader needs exact values or looks things up; use a plain number when there is one thing to say.
4. Remove clutter: one colour for emphasis, labelled directly, a title that states the message.
5. Test: can someone get the point in five seconds?
6. Avoid 3D, many pie slices and dual axes unless essential.

**Strong sample answer (spoken):** Illustrative; replace with your own. "I start by writing the message in one sentence, for example: renewals fell in the last two months, mostly in one region. Then I choose the simplest picture that shows it: a line over time for the fall, maybe a sorted bar for the regions. If leadership only needs to know the one figure, I would put the number on the slide with one line of context, not a chart. If people need exact values, such as a price list, I would use a table. I give the chart a title that states the message, highlight one thing in colour, and check that someone outside the project can read it in five seconds."

**Weak version (and why it fails):** "I use whatever the tool suggests, or the most impressive chart." The chart ends up decorating, not making a point, and leadership has to do the work of finding the message.

**What the interviewer scores:**
- Do you start from the message and audience?
- Do you match chart form to the type of message?
- Do you know when not to use a chart?
- Do you remove clutter and label clearly?
- Do you test it on a fresh reader?

**Make it yours:**
- Pick a real chart you made and write its one-sentence message.
- Say what you would change today and why.
- Find a case where a table or number would have been better.
- Show the chart to someone outside the work and note what they said.
- Use your own examples, not stock ones.

**Follow-ups:**
- When is a pie chart fine? "A few slices with clear differences; otherwise a sorted bar is easier to read."
- How do you show uncertainty? "A range or interval on the chart, plus a plain sentence about it."
- What about a dashboard? "One question per view, with the key number first."

**Common mistakes:**
- Choosing the chart before the message.
- Too many colours and series.
- Titles that describe, not conclude.
- Hiding exact numbers people need.
- AI-era note: AI chart tools produce plausible defaults; check axes, scale and labels yourself.

### Q19 ⭐⭐ 🟢 Explain overfitting to a non-technical colleague with an everyday analogy, and say how you would tell them you are guarding against it.
**Asked at:** Public question banks list explain-a-model-to-a-non-technical-stakeholder prompts in many variants (Dataford pages, a Prepfully answers page and a TryExponent ML-concepts guide, which advises checking whether the listener is technical); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** Overfitting is memorising the practice questions instead of learning the subject, and I guard against it by testing on questions the model has never seen.

**Structure:** Use the "pattern for explaining anything" above.
1. Decision: why they care (the model must work on new customers, not just old ones).
2. Answer first: a model can look great on past data and fail on new data.
3. One picture: a student who memorises last year's exam answers and then meets new questions.
4. Number with meaning: "good on old data, much worse on new data" is the warning sign.
5. Not meant: a high score on past data does not prove it works.
6. Safeguard: keep some data hidden until the end, compare, keep the model simple enough, and monitor after launch.
7. Check: does that make sense?

**Strong sample answer (spoken):** Illustrative; replace with your own. "Imagine a student who memorises last year's exam, word for word. They score full marks on that paper, but on a new exam with different questions, they struggle. They learned the answers, not the subject. A model can do the same: it fits the past data so closely, including its quirks, that it fails on new cases. To guard against it, I hide part of the data until the end, like a surprise exam, and only trust the model if it does well on that too. I also keep the model as simple as the problem allows and check it again after launch. Does that picture make sense for your use case?"

**Weak version (and why it fails):** "The model has high variance and low bias, so it does not generalise." Correct to an engineer, meaningless to a business partner, who nods and learns nothing.

**What the interviewer scores:**
- Is the analogy accurate and everyday?
- Do you answer first, without jargon?
- Do you say what you actually do about it?
- Do you check understanding?
- Can you move to technical detail if asked?

**Make it yours:**
- Think of an analogy from your listener's own world (sales, cooking, sport) and test it for accuracy.
- Recall a time your model did well in training and worse on held-out data, and how you noticed.
- Write the one sentence for your safeguard using your real method.
- Say it aloud in under a minute.
- Be ready to explain the technical version too.

**Follow-ups:**
- Where does the analogy break down? "A student can understand; a model only finds patterns. I would say so if pushed."
- How would you explain it to a technical peer? "Gap between train and validation performance; regularisation, cross-validation, simpler models, more data."
- How do you know it is not overfitting after launch? "Monitor live performance against the held-out result."

**Common mistakes:**
- Jargon first.
- An analogy that implies the wrong thing.
- Naming the problem but no safeguard.
- Talking for five minutes.
- AI-era note: an AI-generated analogy may be generic; interviewers may ask for a second one, so understand why yours fits.

### Q20 ⭐⭐ 🟢 A business partner reads a regression output and asks what a coefficient means for their decision. How do you explain it, and what caution do you add?
**Asked at:** Public question banks list explain-a-model-to-a-non-technical-stakeholder prompts in many variants (Dataford pages, a Prepfully answers page and a TryExponent ML-concepts guide, which advises checking whether the listener is technical); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** A coefficient says how much the outcome tends to change when one input changes by one step, with the other inputs held the same, and it is not proof that the input causes the change.

**Structure:** Use the "pattern for explaining anything" above.
1. Decision: what will they do with it (change price, spend, staffing)?
2. Answer first: translate the coefficient into their units: "each extra [unit] goes with about [amount] more [outcome]".
3. Say "on average, other things equal".
4. Give the range: "somewhere between this and that", not one exact number.
5. Caution: association is not cause; it applies only to the range of data we saw; look at whether it is big enough to matter.
6. Next step: what test or experiment would settle it.

**Strong sample answer (spoken):** Illustrative; replace with your own. "The coefficient for advertising spend says that, in our past data, weeks with one more unit of spend had about [amount] more sales on average, comparing weeks that were otherwise similar. The data supports a range, roughly [low] to [high], so I would not plan on the exact figure. One caution: this shows a pattern, not proof that spending caused the sales. Busy weeks may have had both more spend and more sales. Also, we have only seen spend within a certain range, so I would not stretch it far beyond that. If this decision is large, we could run a small test to confirm. What decision are you weighing?"

**Weak version (and why it fails):** "The coefficient is 0.4 and the p-value is under 0.05, so spend drives sales." It states cause without evidence, gives no units or range, and the stakeholder may commit budget on a wrong reading.

**What the interviewer scores:**
- Do you translate into the listener's units?
- Do you add "on average, other things equal"?
- Do you give a range, not a false exact?
- Do you flag cause versus association and limits?
- Do you suggest a way to confirm?

**Make it yours:**
- Take a real regression you ran and write one coefficient in plain units.
- Write the range and the most likely confounder from your own data.
- Name one situation where the result would not apply.
- Say it aloud to someone from a different field.
- Use your real numbers; do not invent them.

**Follow-ups:**
- What if the coefficient is not significant? "I say the data does not show a clear effect, and show the range; it may be zero or small."
- What if two inputs move together? "The coefficients become unstable; I would say they cannot be separated and avoid reading either one alone."
- How would you confirm cause? "An experiment or a quasi-experiment, if it is feasible and ethical."

**Common mistakes:**
- Reading a coefficient as cause.
- Quoting it to false precision.
- Ignoring units and scale.
- Extrapolating beyond the data.
- AI-era note: AI tools can write fluent explanations that over-claim causation; check each sentence against what your model shows.

### Q21 ⭐⭐ 🟢 Write a short email to a stakeholder that shares a result, states how sure you are and asks for a decision. What do you put in it?
**Asked at:** Guidance on written communication for data scientists (Towards Data Science pieces on writing, a Yardstick communication-skills page, a HelloInterview page on design-doc experience, postmortem-writing guides, which are practitioner blogs, not interview lists); written-format prompts are partly editor-designed; search snippets only, not opened
**Say this first (1 line):** Put the answer and the ask in the first two lines, then how sure you are, then the one thing that could change it.

**Structure:** (Written structure, so a busy reader can stop after three lines. Pattern: see "A pattern for explaining anything" at the top of this part.)
1. **Subject line:** the decision, not the topic ("Decision needed by Thursday: ...").
2. **Line 1, the result in plain words,** with the number and what it means in people or orders.
3. **Line 2, the ask:** the exact decision, the options and the date.
4. **How sure:** a range or "likely / not yet known", plus one reason.
5. **What could change it:** one caveat and what you will check.
6. **Detail on request:** link to the long version. Do not paste it.

**Strong sample answer (spoken):** I would write it like this (illustrative; replace the details with your own):
- Subject: Decision needed by Thursday: roll out the new reminder email?
- "The reminder email looks like it helps. Customers who got it renewed more often than those who did not, by roughly [your lift]. I am fairly confident it is positive, but the true size could be smaller: my range is [low] to [high].
- I need one decision from you: roll out to everyone, extend the test two weeks, or stop. I recommend rolling out to half the customers first.
- The main risk is that the test ran during a quiet month. I will check the same effect on next month's data. Detail is in the linked note; happy to talk it through."

That is under 120 words, the reader can act after the first paragraph, and the uncertainty is a range, not a hedge.

**Weak version (and why it fails):** A long email that starts with the method, buries the result in paragraph four, says "results are promising, more analysis may be needed" and never asks for a decision. The reader cannot tell what you want or how much to trust it, so they reply later with questions or do nothing.

**What the interviewer scores:**
- Decision first, method last.
- Uncertainty stated as a range or plain words, not hidden and not buried.
- A clear ask with options and a date.
- Short enough to read on a phone.
- A recommendation you are willing to own.

**Make it yours:** Pick one real result you shared (a test, a model, a report). Write the two-line version of the result and the ask from memory. Fill in your own numbers and your own real caveat. If you cannot state the ask in one sentence, that is the gap to fix. Do not invent a result for the interview; use a real one or say plainly that it is a template.

**Script (copy and adapt):**
```
Subject: Decision needed by [date]: [the decision in a few words]

Hi [name],

[Result in one plain sentence, with the number and what it means.]
My recommendation: [option]. I need a decision on [A / B / C] by [date].

How sure I am: [range or "likely / not yet known"], because [one reason].
What could change it: [one caveat]. I will [check] by [date].

Detail is here if useful: [link]. Happy to walk through it in 10 minutes.

[Your name]
```

**Follow-ups:**
- *They reply "so is it significant?"* Answer in their terms: "It is unlikely to be luck, and the likely size is [range]. Whether that is worth the cost is your call."
- *What if you are not sure enough to recommend?* Say so and propose the cheapest next step: "I cannot recommend yet; two more weeks of data would settle it."
- *Would you send charts?* One chart at most, with the takeaway as its title.

**Common mistakes:** Leading with method; no ask; one precise-looking number with no range; hedging every sentence; attachments the reader must open to find the answer; a story you could not defend line by line when the interviewer asks "how did you get that range?". Write it yourself; live follow-ups expose AI-written answers.

### Q22 ⭐⭐ 🟢 How do you document the assumptions and caveats of an analysis so that a reader a year later does not misuse it?
**Asked at:** Guidance on written communication for data scientists (Towards Data Science pieces on writing, a Yardstick communication-skills page, a HelloInterview page on design-doc experience, postmortem-writing guides, which are practitioner blogs, not interview lists); written-format prompts are partly editor-designed; search snippets only, not opened
**Say this first (1 line):** I write the caveats next to the result, in a fixed short template, so the warnings travel with the numbers and say what the analysis can and cannot be used for.

**Structure:** (Written structure; pattern: see the pattern section at the top of this part.)
1. **Purpose and decision:** the question it answered and who asked, with the date.
2. **Data:** source, time window, what was excluded and why, known gaps.
3. **Assumptions:** each one as a plain sentence, with how you checked it or that you did not.
4. **Limits of use:** "Fine for X. Not fit for Y." The misuse you can foresee.
5. **Known weak spots:** groups, periods or cases where it is shaky.
6. **How to refresh or retest:** what would make it stale (a product change, a new data source).
7. **Owner and where to ask**, plus a version and a date.

**Strong sample answer (spoken):** "I keep a one-page note beside the analysis, never in a separate folder nobody opens. The top line says what it is for: 'This estimates last quarter's churn drivers for the retention team; it is not a forecast.' Then the data: where it came from, what period, what I dropped. Then the assumptions, one sentence each, for example 'customers who left within seven days are excluded because they are mostly trial accounts.' The part I care most about is 'do not use this for': I write the misuse I can imagine, such as applying it to a new market or reading the drivers as causes. I add when it goes stale, like after a pricing change, and who to ask. A reader a year later can then see in two minutes whether their question fits. I also put a short caveat line on the chart or table itself, because people copy those and lose the note." (Illustrative; replace the examples with your own.)

**Weak version (and why it fails):** "I add a note saying results may vary." Vague caveats get ignored, and nothing says what the analysis is not for. Or a ten-page appendix in a different place, which nobody reads and which drifts out of date.

**What the interviewer scores:**
- Writing for a future reader who lacks your context.
- Specific, testable caveats, not boilerplate.
- An explicit "not fit for" line.
- Caveats attached to the artefact people actually copy.
- Ownership: a date, version and contact.

**Make it yours:** Open a real analysis you did. Write its "do not use this for" line and three assumptions in plain words. Ask a colleague who was not involved to read it cold and say what they would use it for. Fix what they get wrong. Use your own real work as the example; if you have none, say you would apply this template to the next one.

**Follow-ups:**
- *How do you stop people ignoring it?* Keep it to one page, put the key caveat on the chart, and mention it when you hand the work over.
- *What if a stakeholder wants the caveats removed?* Offer to shorten them, not delete the misuse warnings; explain the cost of a wrong reuse.
- *Who keeps it current?* A named owner and a review trigger (a data or product change), not a calendar reminder alone.

**Common mistakes:** Generic disclaimers; hiding caveats in a footnote; no date or owner; documenting what you did but not what it should not be used for; writing only for yourself.

### Q23 ⭐⭐ 🟡 Explain customer clustering to a marketing team that wants to use the segments, including what the segments are not.
**Asked at:** Public question banks list explain-a-model-to-a-non-technical-stakeholder prompts in many variants (Dataford pages, a Prepfully answers page and a TryExponent ML-concepts guide, which advises checking whether the listener is technical); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** Clustering groups customers who behave alike, so the segments are useful labels for planning, not natural types of people and not a promise of how anyone will act.

**Structure:** (Explanation structure; pattern: see the pattern section at the top of this part.)
1. **Decision:** what marketing wants to do with the segments.
2. **Plain meaning:** the picture, here sorting a pile of shop receipts into piles that look alike.
3. **What it is built on:** which behaviours went in (and so what the groups really reflect).
4. **What it is not:** not fixed, not causal, not a description of identity, and the number of groups is a choice.
5. **How to use it safely:** test a message on a segment before building a campaign.
6. **Check:** "Can you describe each group in one line and say what you would do differently for it?"

**Strong sample answer (spoken):** "Think of sorting a big pile of shop receipts into piles that look alike: one pile of small, frequent baskets, one of big occasional ones, one of customers who only buy in sales. The model does the sorting from behaviour, with no names for the piles. We give the names afterwards. Here is what the segments are not. They are not types of people: the same person can move piles next season. They do not explain why people buy; they only describe what they did. And the count, say four or six, is a judgement call, not a fact. So I would use them as a starting point: pick one segment, try a message, and see if it behaves differently. If a segment does not change what you would do, merge it. I will send a one-line description of each group so we agree on the names before anything is built." (Illustrative; replace the example with your own data.)

**Weak version (and why it fails):** "It uses k-means to minimise within-cluster variance." The audience learns nothing usable. The opposite failure is "these are your customer personas", which turns a statistical grouping into a false description of people and lets marketing treat it as fact.

**What the interviewer scores:**
- A concrete picture, not an algorithm name.
- A clear "what the segments are not".
- Linking the output to a decision and a test.
- Admitting the number of clusters is a choice.
- Checking understanding.

**Make it yours:** Use a real clustering or grouping you built, or a simple one on a public dataset. Write the one-line description of each group and one action it would change. Then write the "not" list in your own words. If you have not done clustering for a team, say so and use the practice example, labelled as one.

**Follow-ups:**
- *How do you know the segments are good?* Stable when re-run, easy to describe, and different in something the business cares about, such as response to an offer.
- *Can we say segment 3 are loyal people?* Only if loyalty was measured; the label should match the behaviour that went in.
- *Will customers stay in them?* Not necessarily; plan a refresh.

**Common mistakes:** Naming the algorithm instead of the idea; naming segments with stereotypes about people; treating segments as causes; not saying the group count is a choice; no test plan.

### Q24 ⭐⭐ 🟡 An executive asks whether a neural network is a black box and whether that is a problem. How do you explain it?
**Asked at:** Public question banks list explain-a-model-to-a-non-technical-stakeholder prompts in many variants (Dataford pages, a Prepfully answers page and a TryExponent ML-concepts guide, which advises checking whether the listener is technical); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** Partly yes: we cannot read its reasoning like a rule, but whether that matters depends on the stakes, and we have ways to check it anyway.

**Structure:** (Explanation structure; pattern: see the pattern section at the top of this part.)
1. **Answer first:** "Somewhat, and it matters more in some uses than others."
2. **Picture:** an experienced assessor who is usually right but cannot list the rules they use.
3. **What we can still do:** test it on cases it has not seen, check which inputs drive it, review its mistakes by group, keep a human for high-stakes cases.
4. **The trade-off:** a simpler model is easier to explain but may be less accurate; choose by the cost of an error and any need to give reasons.
5. **Decision for them:** how much explanation the use case requires.
6. **Check:** "Do you need to give a reason to each customer, or only to know it works?"

**Strong sample answer (spoken):** "Partly, yes. A neural network learns from examples, and no one can read off a clean list of rules the way you can from a simple scorecard. Think of an experienced assessor who is usually right but cannot write down how they do it. Is that a problem? It depends on the stakes. For recommending a film, I would not worry. For deciding who gets a loan, I would, because people deserve reasons and regulators or auditors may ask for them; please check with the compliance team what is needed. Either way we are not helpless: we test it on cases it has never seen, check which inputs move its answers, and look at where it fails and for whom. If the decision is high-stakes, a simpler model or a human review step may be worth a small loss in accuracy. The decision I need from you is how much explanation this use needs." (Illustrative.)

**Weak version (and why it fails):** "It is a black box, nobody can explain it", which sounds alarming and helpless, or "It is fine, we validate it", which dismisses a real concern. Both skip the stakes and the safeguards.

**What the interviewer scores:**
- A balanced, honest answer, not defensive.
- A familiar analogy.
- Linking explainability to the cost of an error.
- Concrete safeguards beyond "trust me".
- Handing the decision back to the executive with a clear question.

**Make it yours:** Think of a model you built or used. Say what you would do to check it and explain a single prediction (for example, which inputs mattered). Write one sentence on whether a simpler model would have been enough, honestly. Do not claim you used interpretability tools you have not.

**Follow-ups:**
- *Can you explain one prediction?* Often partly, by showing which inputs pushed it up or down; these explanations are approximate, and I would say so.
- *Why not always use the simple model?* Sometimes we should; if it is nearly as good, I would.
- *Is this the same for LLMs?* Largely yes; see Q25 and Q29.

**Common mistakes:** Saying "it is a black box" without a safeguard; overselling explanation tools as exact; ignoring that stakes differ; jargon such as layers and activations.

### Q25 ⭐⭐ 🟡 Explain what a large language model is to a non-technical executive who is about to buy an AI product built on one.
**Asked at:** Public question banks list explain-a-model-to-a-non-technical-stakeholder prompts in many variants (Dataford pages, a Prepfully answers page and a TryExponent ML-concepts guide, which advises checking whether the listener is technical); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** An LLM is a system trained on huge amounts of text to predict plausible next words, which makes it fluent and useful, but it does not check facts, so buying one means planning for checking and for limits.

**Structure:** (Explanation structure; pattern: see the pattern section at the top of this part.)
1. **Decision:** what they are about to buy and what it will be used for.
2. **Plain meaning:** a very well-read assistant that writes what sounds right, trained on text, with no built-in fact check.
3. **What it is good at:** drafting, summarising, searching and rephrasing.
4. **What to watch:** confident wrong answers (often called hallucination), out-of-date knowledge, uneven quality, and what happens to the data you send it.
5. **Safeguards:** ground answers in your documents, human review matched to the cost of an error, testing on your own cases.
6. **Questions to ask the vendor:** how they test, what data they keep, how they handle mistakes.
7. **Check.**

**Strong sample answer (spoken):** "A large language model is a system trained on a very large amount of text to predict what words should come next. That is why it writes well. Think of a very well-read assistant who sounds sure of everything, even when they are guessing, because nothing in the system checks facts. It is good at drafting, summarising and answering questions over your own documents. The risks to plan for are confident wrong answers, knowledge that goes out of date, quality that varies by task, and what happens to the data you give it. You cannot remove those risks, but you can manage them: connect it to your own documents, have a person review anything where a mistake is costly, and test it on your real cases before you rely on it. Before you sign, I would ask the vendor how they test, what they do with your data, and who is responsible for errors. Which tasks are you planning to use it for?" (Illustrative.)

**Weak version (and why it fails):** "It is a transformer with billions of parameters trained with next-token prediction." Correct and useless to this listener. Or the sales version: "It understands your business", which overpromises and sets up a failure the data scientist will be blamed for.

**What the interviewer scores:**
- No jargon, one analogy.
- Honest on limits without scaring the listener.
- Decision-oriented: questions to ask before buying.
- Matching safeguards to the cost of errors.
- Not repeating vendor claims you have not verified.

**Make it yours:** Use a real LLM tool you have tried. Write one task it did well and one place it was wrong, from your own experience, and how you checked. State only what you have seen. AI-era note: do not have an AI write this explanation for you; interviewers follow up with "what happened when it was wrong for you?"

**Follow-ups:**
- *Can we make it never wrong?* No; we can reduce and catch errors, not eliminate them. Review should match the stakes.
- *Is our data safe?* Ask the vendor and your security team; I would not assume.
- *Why does it sound so sure?* It is trained to write fluent text, which is not the same as being correct.

**Common mistakes:** Anthropomorphic words ("it knows", "it thinks"); technical detail; either hype or doom; quoting vendor accuracy figures as fact; skipping the vendor questions.

### Q26 ⭐⭐ 🟡 Explain AUC to a non-technical manager, and tell them when it can mislead.
**Asked at:** Public question banks list translating precision, recall, PR curves and AUC-ROC for non-technical managers (several Dataford pages, one framed for a government programme manager and one for a corporate stakeholder); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** AUC tells you how well a model ranks the cases that matter above the ones that do not, across all cut-offs, but it does not tell you how it performs at the cut-off you will actually use.

**Structure:** (Explanation structure; pattern: see the pattern section at the top of this part.)
1. **Decision:** are we comparing models, or choosing how many cases to act on?
2. **Plain meaning:** pick one customer who left and one who stayed at random; AUC is how often the model scored the leaver higher. Half the time is a coin flip, always is perfect.
3. **What it is good for:** comparing models' ranking quality in one number.
4. **When it misleads:** it ignores the cut-off and the cost of each error; it can look good when positives are rare and the list you act on is still mostly wrong; it hides weak spots in one group.
5. **What to look at instead or as well:** precision and recall at the chosen cut-off, and the results by group.
6. **Check.**

**Strong sample answer (spoken):** "Imagine we take one customer who left and one who stayed, picked at random, and ask the model to score both. AUC is how often it gives the higher score to the one who left. A coin flip would be right half the time, so a value near one half means no skill, and closer to the top means better ranking. It is handy for comparing models. Here is when it can mislead. First, it looks at every possible cut-off, but you will use only one, say contacting the top thousand customers. A model with a good AUC can still give you a poor list at that cut-off. Second, when the thing we look for is rare, a good AUC can still mean most of the people you contact are false alarms. So I would show AUC for comparing, then the number of correct and wasted contacts at the cut-off we will use. Which cut-off is realistic for your team?" (Illustrative.)

**Weak version (and why it fails):** "The area under the ROC curve, true positive rate against false positive rate." That is the definition, not the meaning, and says nothing about when to trust it. Or "AUC of 0.9 means it is 90 percent accurate", which is wrong and sets the manager up for disappointment. Metric definitions are in Book 6 Part 1.

**What the interviewer scores:**
- A correct, plain-language meaning (ranking probability), not "accuracy".
- Naming at least two real limits.
- Linking to the operating cut-off and cost of errors.
- Offering a more decision-relevant number.
- Not drowning the manager in curves.

**Make it yours:** Take a classifier you have built and report AUC next to precision and recall at a sensible cut-off. Write the two-sentence explanation of what the gap means, with your own figures kept as placeholders if they are not shareable. Use a real result, not an invented one.

**Follow-ups:**
- *When would you prefer the precision-recall view?* When the positive class is rare and you care about the quality of the list you act on.
- *Is a higher AUC always better?* For ranking yes, but not necessarily for the decision, which depends on cut-off and costs.
- *Does AUC show fairness?* No; check by group.

**Common mistakes:** Equating AUC with accuracy; defining it with rates and curves; not mentioning the cut-off; no alternative number; sounding as if one number settles it.

### Q27 ⭐⭐ 🟡 A model says a customer has a 30 percent chance of leaving. How do you explain probability forecasts and uncertainty to people who want a yes or no?
**Asked at:** Public statistics question banks list explain-a-p-value and explain-a-confidence-interval prompts for lay audiences (an Interview Query p-value page, a TryExponent confidence-interval page, Dataford statistics lists); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** A 30 percent chance is not a verdict: it means that out of many customers like this one, about three in ten leave, and the yes or no is a business choice about what to do at that risk.

**Structure:** (Explanation structure; pattern: see the pattern section at the top of this part.)
1. **Decision:** what action hangs on the yes or no (call, offer, nothing).
2. **Plain meaning:** a weather-forecast picture, "30 percent chance of rain" and the right call is to take an umbrella or not depending on what getting wet costs.
3. **Meaning for one person versus a group:** for one customer it is a likelihood, across a hundred similar ones it is about thirty.
4. **Uncertainty:** the number itself is an estimate; say how reliable the scores are (are 30 percent customers really leaving about that often).
5. **Turn it into a yes or no:** pick a threshold from the cost of acting versus the cost of losing the customer.
6. **Check:** "What does an offer cost compared with a lost customer?"

**Strong sample answer (spoken):** "Think of a weather forecast. Thirty percent chance of rain does not mean it will or will not rain. It means that on days like this, about three in ten are wet. Same here: of a hundred customers with this score, we expect around thirty to leave and seventy to stay, and we cannot tell which ones in advance. So the model does not give a yes or no, you do, by choosing where to act. If a retention offer is cheap and losing a customer is expensive, you might act on everyone above 20 percent. If the offer is costly, you might wait until 50 percent. I have checked that when the model says thirty, about that share really do leave, so the number can be trusted as a rough guide. What does an offer cost compared with a lost customer? Then we can set the line together." (Illustrative; replace with your own figures.)

**Weak version (and why it fails):** "It is 30 percent, so no, they will not leave", which treats a probability as a verdict. Or a lecture on calibration and log-loss. Or refusing to give a yes or no at all, which leaves the stakeholder without help.

**What the interviewer scores:**
- Correct meaning of a probability, no false certainty.
- A familiar picture and a group-versus-individual framing.
- Helping the person set a threshold from costs.
- Honesty on whether the numbers are reliable.
- Not being preachy or evasive.

**Make it yours:** Use a model with scores you have actually worked with. Write how you would explain one score and how you would pick the action line with your own costs, or placeholders such as [cost of the offer] and [value of a kept customer]. Note whether you checked that the scores match reality; if you did not, say so.

**Follow-ups:**
- *So will this customer leave?* We cannot say for one person; we can say the group like them loses about three in ten.
- *Why not just say high or low risk?* Labels help but hide the threshold choice; I would show both.
- *How do you know 30 percent is right?* Compare predicted against actual rates across score bands.

**Common mistakes:** Treating the score as a verdict; false precision; hiding behind uncertainty; not tying the threshold to cost; jargon such as calibration without explanation. For numeric scenarios, see Book 6 Part 6.

### Q28 ⭐⭐ 🟡 A model works worse for one group of customers. How do you explain bias and fairness to leadership and what do you ask them to decide?
**Asked at:** Public question banks list explain-a-model-to-a-non-technical-stakeholder prompts in many variants (Dataford pages, a Prepfully answers page and a TryExponent ML-concepts guide, which advises checking whether the listener is technical); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** The model is less reliable for one group, which is a business and ethical risk, and the decision for leadership is what level of difference is acceptable and what we do about it.

**Structure:** (Explanation structure; pattern: see the pattern section at the top of this part.)
1. **Decision:** accept, fix, limit the use, or add review, and who owns that call.
2. **Plain meaning:** bias here means the model makes more mistakes, or different mistakes, for one group; fairness is a choice about which differences are acceptable.
3. **Evidence:** the specific gap in plain terms (for example, more missed cases for group X), with how sure you are.
4. **Likely causes (hypotheses):** too little data on that group, a signal that works differently for them, a label that reflects past decisions. Say you are checking.
5. **Options and costs:** collect more data, adjust the model, change the threshold, add a human check, narrow the use; each has trade-offs.
6. **Ask:** leadership decides the acceptable gap and the owner; check company policy and ask legal or compliance colleagues about obligations (this book gives no legal advice).
7. **Check.**

**Strong sample answer (spoken):** "Here is what we found: the model misses more real cases for [group] than for others, [your gap in plain words]. That matters because those customers get a worse service or a wrong decision more often. I do not yet know the cause. It might be that we have little data on them, or that a signal behaves differently for them, and I am checking. There is also no single definition of fair: equal error rates, equal outcomes and equal treatment can pull against each other, so this is a values choice as well as a technical one. I can offer options: collect more data, adjust the threshold for the group, add a human review for borderline cases, or limit where we use the model, each with a cost. What I need from you is how big a gap you accept, who owns this, and whether to involve our compliance team before launch. I would rather decide that now than after complaints." (Illustrative.)

**Weak version (and why it fails):** "The data was biased and it is hard to fix", which blames and stalls. Or a technical talk on fairness metrics with no ask. Or hiding the gap because it will delay the launch.

**What the interviewer scores:**
- Stating the finding plainly without defensiveness.
- Separating facts from hypotheses.
- Offering options with trade-offs.
- Making leadership own the value judgement.
- Pointing to compliance and policy without giving legal claims.

**Make it yours:** Use a real model where you checked results by segment, or a public dataset practice. Write the gap in plain words and the options you would offer. Do not describe a fairness check you did not run. Avoid assumptions about what any group is like; talk only about measured differences in the model.

**Follow-ups:**
- *Can we just remove the sensitive column?* Often not enough, since other columns can act as stand-ins; I would test it, not assume.
- *Is a gap always unfair?* Not always, but it must be looked at and justified.
- *What if leadership says ship anyway?* Document the gap, the decision and who made it; propose monitoring.

**Common mistakes:** Vague "bias" talk; metrics lecture; blaming data; offering no options; claiming the model is fair after one metric; stating legal conclusions.

### Q29 ⭐⭐ 🟡 Before a launch, how do you explain a model's limitations and likely failure modes to the people who will rely on it?
**Asked at:** Public guides cover explaining model limits and interpretability trade-offs to non-technical stakeholders (a Dataford page on interpretability versus predictive power, a TryExponent warning about picking an algorithm you cannot explain); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I tell them what the model is good for, where it fails and how they will notice, in a one-page note with examples, and I agree who does what when it fails.

**Structure:** (Explanation structure; pattern: see the pattern section at the top of this part.)
1. **Decision:** what the users will do with the output and what happens if it is wrong.
2. **Works well on:** the cases it was tested on, in plain words.
3. **Fails or is weak on:** specific failure modes with real or realistic examples: new types of customer, data drift, missing inputs, edge cases.
4. **How you will notice:** a monitor, a warning flag, a user check.
5. **What to do when it fails:** a fallback, escalation route, owner.
6. **What it must not be used for.**
7. **Walk through it together,** with two examples they can picture, then ask what they would do.

**Strong sample answer (spoken):** "Before launch I would sit down with the team who will use it with a one-page note. First, what it is good for: ranking leads in the regions and products we tested on. Second, where it is weak: new products it has never seen, customers with little history, and any change in how data is recorded. I show two real examples of misses so it is concrete. Third, how we will know: a weekly check of how often its top picks turn out right, and a flag whenever an input is missing. Fourth, what you do when it looks wrong: use the old process, tell me, and I will look within a day. Last, what not to use it for, such as judging individual staff. Then I ask the team to tell me, in their words, what they would do when a score looks odd. If they can say it, the note has worked." (Illustrative; replace with your own project.)

**Weak version (and why it fails):** "It is 90 percent accurate" with no failure modes, so users over-trust it. Or a 20-slide limitations deck read aloud, which no one remembers. Or hiding the limits to protect the launch.

**What the interviewer scores:**
- Concrete failure modes, not "may not be perfect".
- A way to detect failure after launch.
- A fallback and an owner.
- A format the users can actually remember.
- Willingness to say what it must not be used for.

**Make it yours:** From a real project, list its three most likely failure modes in plain words and the signal that would show each. Add one real example of a miss. If you have not launched a model, apply this to a project and say it is a plan. Book 6 Part 6 holds the numeric launch-risk scenarios.

**Follow-ups:**
- *Will that put them off?* Honest limits build trust, and unexpected failure costs more.
- *How do you keep it current?* Update the note when monitoring finds new failure modes.
- *What about an LLM product?* Add hallucination, out-of-date knowledge and prompt sensitivity to the list.

**Common mistakes:** One accuracy number; only technical limits; no fallback; a long document that nobody reads; no owner after launch.

### Q30 ⭐⭐ 🟡 You get one slide to update executives on a project. What is on it, and what do you leave out?
**Asked at:** Data storytelling and analyst question pages (Adaface and Yardstick data-storytelling lists, a Dataford page on presenting findings to leadership, a Loopcv sample structure of what is happening, why it matters and what to recommend; Interview Query lists a take-home that asks for a summary for a marketing vice president); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** One slide, one message: where the project stands, what changed, what I need from them, and nothing that does not support that.

**Structure:** (Written and presentation structure; pattern: see the pattern section at the top of this part.)
1. **Title is the message,** a full sentence ("On track for [date]; one decision needed on [x]").
2. **Status in one word and one line:** on track, at risk or late, with the reason.
3. **Result so far:** one number or one small chart that shows impact, with how sure you are.
4. **Next milestone and date.**
5. **Risks:** top one or two, with what you are doing about them.
6. **The ask:** the decision or help you need, with an owner and date.
7. **Leave out:** method detail, every metric, the history, tuning details, long lists. Keep them in a backup page.

**Strong sample answer (spoken):** "My slide has a title that says the message: 'Churn model on track for the March pilot; I need a decision on the offer budget.' Under it, three short blocks. Status: on track, because testing is finished. Result: one chart showing that the top-scored customers are [your result] times likelier to leave than average, with a note on how sure we are. Next: pilot starts [date]. One risk: customer data for two regions is late, and we will start without them if needed. And the ask, at the bottom in bold: 'Decide by Friday whether to fund the offer test.' I leave out how the model works, the other metrics and the earlier versions; they are in a backup slide if someone asks. If I only have two minutes, I read the title, the ask and the risk and stop. Then I ask: is there anything here that changes your decision?" (Illustrative.)

**Weak version (and why it fails):** A crowded slide with the architecture, five charts, a timeline and a dense table: the audience reads instead of listening and no one finds the ask. Or a slide with no ask, so a status meeting ends with nothing decided.

**What the interviewer scores:**
- Starting with the point and the ask.
- Ruthless selection of what to leave out.
- Honest status, including risks.
- Backup material ready for questions.
- Awareness of the audience's decision.

**Make it yours:** Take a real project and draw this slide on paper in ten minutes. Then show it to someone and ask them to say the message back. Write a list of what you cut. Use your real numbers, or placeholders if they are private.

**Follow-ups:**
- *What if they ask for more detail?* Go to the backup slide, answer briefly and return to the ask.
- *What if the news is bad?* Put it in the title with the plan; surprises later cost more trust.
- *What if the audience is technical?* The same slide, with a method page in backup.

**Common mistakes:** A topic title instead of a message; too many numbers; hiding bad news; no ask; reading the slide aloud; leaving out the uncertainty.

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
**Asked at:** Editor-designed; related public guidance covers presenting technical work and handling live questions (general training and interview-prep pages); search snippets only, not opened
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
**Asked at:** Editor-designed; related public guidance covers presenting technical work and handling live questions (general training and interview-prep pages); search snippets only, not opened
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
**Asked at:** Editor-designed; related public guidance covers explaining uncertainty and confidence intervals to lay audiences (TryExponent confidence-interval page, Dataford statistics lists, Interview Query p-value page); no public list found for the CFO single-number framing; search snippets only, not opened
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

