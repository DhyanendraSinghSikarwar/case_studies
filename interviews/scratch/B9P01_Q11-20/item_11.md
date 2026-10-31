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
