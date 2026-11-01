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
