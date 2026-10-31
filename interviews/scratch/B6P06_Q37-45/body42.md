**Say this first (1 line):** I would verify the bug, tell the sponsor myself and privately first, then correct the record with everyone who relied on the 0.91, because staying quiet is not an option.

**Clarifying questions:**
- Is the bug confirmed by someone independent of me? Why: I need to be sure before raising it.
- Which decisions used the model and what did they commit (money, customers)? Why: sets urgency.
- Is the model still live? Why: ongoing harm requires acting immediately.
- Are there reporting, audit or regulatory duties? Why: they decide who must be told.
- Who is the sponsor's boss or the model-risk contact? Why: I need an escalation route.

**Approach:**
1. Reproduce: fix the leak, re-run, and have a peer confirm 0.78.
2. Size the impact: what the real number means for the decisions made.
3. Go to the sponsor first, privately, with the fix, the impact and a proposed correction plan. Present it as a problem we solve together.
4. Ask for the correction to go out within days, with the sponsor presenting it.
5. If the sponsor still refuses, escalate to the model-risk or governance owner and tell the sponsor I am doing so. Do not go around silently.
6. Fix the process: add a leakage check and a second reviewer before any future presentation.

**Metrics:** AUC before and after the fix; positives caught in the top 10% before versus after; decisions affected; time from discovery to correction. Guardrail: written record of who was told and when.

**Risks:**
- Career risk. A late discovery by someone else is worse.
- Blaming the original author instead of the process.
- Corrections that omit the consequence for decisions.

**What the interviewer scores:**
- Strong: verifies first, goes to the sponsor first with a plan, corrects the record, escalates if needed, fixes the process.
- Weak: stays quiet, or goes straight to leadership over the sponsor.

**Example:** Illustrative binormal model with 10% positives. At AUC 0.91 reviewing the top 10% of customers catches about 58%; at 0.78 about 36%. Per 100,000 customers that is 5,844 promised versus 3,551 real, a shortfall of 2,292.
- Weak: "It is only a few points, it is probably fine."
- Strong: "I found a leakage bug. The real AUC is 0.78, not 0.91, and it changes how many customers we catch. I want us to tell leadership this week and I have a plan."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if the sponsor threatens you? Keep a written record, use the governance route.
- How do you prevent it? Temporal splits, a leakage review, a second reviewer. Book 1 Part 03 has the thresholding material, and Book 1 Part 01 has the leakage question: "What is data leakage? Give 4 real examples (target, preprocessing, temporal, group) and how you would detect it."

**Common mistakes:** Waiting for a better moment. Going public before the sponsor. Hiding the impact. Fixing silently and swapping the number.
