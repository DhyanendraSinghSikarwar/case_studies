**Say this first (1 line):** 148 of 200 is 74%, with a 95% interval of roughly 67% to 80%, so it is clearly below the 95% bar for unsupervised use, but it may be good enough for a hybrid where the tool drafts and a human checks.

**Clarifying questions:**
- What does a wrong answer cost (a bad decision, or a mild rework)? Why: it sets the acceptable error rate per question type.
- How were the 200 questions sampled, and who judged "correct"? Why: a biased test misleads either way.
- What types of questions fail? Why: errors are concentrated, which makes routing possible.
- Is there a certified semantic layer or metric definitions the tool can use? Why: it usually raises accuracy a lot.
- Who reviews outputs and how fast? Why: it sets whether supervised use is affordable.

**Approach:**
1. Present 74% with its interval, and translate it: 26 wrong answers per 100 questions versus 5 allowed at 95%.
2. Break results down by question type. Show where it is strong and weak.
3. Propose tiers: (a) unsupervised for simple questions on certified metrics once a tier is proven at 95% or better with a large enough sample, (b) tool drafts SQL and an analyst reviews for the rest, (c) humans own open-ended and high-stakes questions.
4. Add guardrails: show the generated SQL, log every query, spot-check a weekly sample, and re-test on new questions.
5. Define the promotion rule: a tier goes unsupervised only when its lower confidence bound reaches the target.
6. Report the time saved honestly, net of review time.

**Metrics:** Accuracy = correct answers / questions tested. 95% Wilson interval for a proportion. Per tier accuracy. Review time per question. Guardrail: wrong-answer rate on the weekly audit sample.

**Risks:**
- Confident wrong answers get used without anyone noticing.
- A test set that is easier than real traffic.
- Proving 95% needs enough samples: with zero errors, 73 straight correct answers are needed before the lower bound reaches 95%.

**What the interviewer scores:**
- Strong: interval, error translation, tiers, promotion rule.
- Strong: neither dismisses nor oversells the tool.
- Weak: "74% is too low, no", or "it will improve, roll it out".

**Example:** Illustrative split that adds to 148 of 200: simple certified-metric questions 114 of 120 (95.0%, interval 89.5% to 97.7%), open-ended questions 34 of 80 (42.5%). So only the simple tier is near the bar and still unproven.
- Weak: "74 percent is not good enough, so we keep the analytics team as is."
- Strong: "74% overall hides a 95% tier and a 43% tier. Let the tool serve the first tier with SQL shown and audited, draft for the second, and keep humans on the rest."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Would more prompt work fix it? Maybe, but re-test on fresh questions, not the same 200.
- What does the analytics team do afterwards? See Q45 of this part.

**Common mistakes:** Quoting 74% without an interval. Averaging over question types. Testing on the questions used to tune prompts. Skipping an audit after launch.
