**Say this first (1 line):** Show the complicated starting point in one sentence, the simpler version you chose and why, and the proof that it worked.

**Structure:** STAR with a simplification focus [G, editor guidance].
1. Situation: what was complicated, and what it cost (time, errors, confusion).
2. Task: your responsibility for fixing or replacing it.
3. Action: how you found what could go (steps nobody used, duplicate code, unneeded features); what you removed or merged; how you checked that nothing important broke; who you told.
4. Result: what is faster, clearer or cheaper, shown by a real observation.

Company note: Amazon-style loops tie questions to principle names and real past examples (Book 7 Part 1, Amazon, C3; anecdotal and third-party). Principle names are editor knowledge: check the company's current list (older guides cite 14, Amazon's own guide mentions 16).

**Strong sample answer (spoken):** Illustrative; replace with your own. "Our team's model pipeline had grown to [number] steps with several scripts that nobody fully understood. A rerun took most of a day, and small changes broke things. I was asked to make it more reliable. I mapped every step and asked who used each output; a few steps fed nothing. I removed those, merged repeated cleaning code into one function, and added a short test comparing outputs before and after. I showed the team the map and the results of the test before changing the main branch. The rerun became much quicker and new joiners could follow it. One thing I would change: I should have written the documentation as I simplified, not afterwards."

**Weak version (and why it fails):** "I rewrote everything to make it cleaner." No evidence of why, no checking, no result, and risk of a rewrite nobody asked for.

**What the interviewer scores:**
- Do you notice and name complexity as a real cost?
- Do you remove with evidence, not taste?
- Do you protect against breakage?
- Do you involve and inform the people affected?
- Do you measure the result?

**Make it yours:**
- Pick a real process, notebook, model or report you simplified.
- Write what was wrong, and what it cost.
- List what you removed, kept and tested.
- State the effect honestly, even if small.
- Note one thing you would do differently.

**Follow-ups:**
- How did you know nothing important broke? "Describe the before-and-after check."
- Did anyone resist? "Explain the concern and how you addressed it."
- When is complexity worth keeping? "When it handles a real case; I ask what each part is for first."

**Common mistakes:**
- Rewriting without a reason or test.
- Calling a cosmetic change simplification.
- No result.
- AI-era note: an AI tool can suggest cuts, but you are responsible for what you removed; be ready to explain each decision.
