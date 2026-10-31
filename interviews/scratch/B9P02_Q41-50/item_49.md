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
