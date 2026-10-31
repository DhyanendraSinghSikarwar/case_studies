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
