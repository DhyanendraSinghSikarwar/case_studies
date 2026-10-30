**Say this first (1 line):** A thumbs-up drop with no release on my side points to something I do not control, so I replay a fixed, versioned question set through the old and new provider behaviour, show the paired drop, and then lock the provider version and add a daily canary.

**Clarifying questions:**
- Can I pin or even see the provider's model version, and do my logs record the version string returned? Without it I cannot date the change.
- Did anything else change that week: traffic mix, new documents indexed, a UI change to the thumbs button, a marketing push? These are rival causes.
- How many votes per week, and what share of answers get a vote? Few votes or a small share means selection bias.
- Do I have a frozen test set with expected answers or rubric scores from before the change? If not, building one is step zero.
- Is the retrieval layer unchanged (same index, same prompts, same temperature)? I need to isolate the generator.

**Approach:**
1. Rule out measurement: thumbs-up rate per day around the change date, vote volume, UI changes, user mix. A step change that lines up with the provider date is the first clue.
2. Check for retrieval or data changes: same retrieved passages for the same queries, same index version, same prompt hash.
3. Replay a fixed regression set (illustrative 300 questions) through the current provider and through any pinned older snapshot or archived outputs from before the change, with the same prompts and retrieved context.
4. Compare pass/fail per question with a paired test (exact McNemar): count questions that passed before and fail now versus the reverse.
5. Read the failures: format changes, refusals, shorter answers, citation style, tone. Provider updates usually change style and refusal behaviour, not only knowledge.
6. Mitigate: pin a dated model version if the provider offers one, adjust the prompt for the new behaviour, or switch provider/version; re-run the regression set before any change goes live.
7. Guard for the future: a daily canary of fixed questions with an alert on the pass rate, a provider-change log, and an eval gate for every model or prompt update.

**Metrics:**
- Thumbs-up rate = thumbs-up votes / (thumbs-up + thumbs-down votes), plus vote rate = votes / answers shown.
- Regression pass rate = questions meeting the rubric / questions in the fixed set.
- Paired discordance: b = passed before and failed now, c = failed before and passed now; the test statistic uses b versus c only.
- Guardrails: refusal rate, average answer length, latency, cost per answer, citation validity.

**Risks:**
- Thumbs are self-selected and noisy; a changed UI or user mix can move them without any model change.
- The fixed set can be stale; it may not represent today's questions.
- You cannot rerun the "before" model if the provider has retired it. Archive outputs on a schedule so a baseline exists.
- LLM-judge scores on the regression set can drift too (see Book 6 Part 2, Q45).
- A canary with too few questions misses small drops.

**What the interviewer scores:**
- Strong: separates "users are unhappier" from "answers got worse", using a controlled replay. Weak: guesses it is the provider.
- Strong: uses a paired comparison on the same questions. Weak: compares two different samples of live traffic.
- Strong: proposes pinning, a canary and an eval gate. Weak: only suggests re-prompting.
- Strong: notes the missing model-version logging as a root gap.

**Example:** (illustrative) 3,000 votes in each week: 78% is 2,340 up, 69% is 2,070 up; the two-proportion z is 7.9, so it is not noise, but it says nothing about cause. The fixed set has 300 questions: 255 passed before (85%), 231 pass now (77%). Of the discordant pairs, 38 went pass to fail and 14 went fail to pass: 255 - 38 + 14 = 231. The exact McNemar p-value is 0.0012 and the 95% interval for the paired difference is -12.6 to -3.4 points. A daily unpaired canary of 300 questions could only see a drop of about 8 points with 80% power, so a canary needs more questions or a paired design. Weak: "The provider changed it, nothing we can do." Strong: "Here is the paired replay showing an 8-point fall on the same 300 questions; I will read the 38 regressions, then pin a version and add a canary."

**Code:**
