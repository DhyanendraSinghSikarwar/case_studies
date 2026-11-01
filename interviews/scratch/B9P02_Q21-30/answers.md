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
