**Say this first (1 line):** Both of them are protecting something real: the delay costs 75,000 (3 weeks x 25,000, illustrative), but a shipped defect can cost far more, so I offer a risk-ranked, shorter review plus a capped launch instead of picking a side.

**Clarifying questions:**
- Which checks are still open, and which are the ones that catch the worst failures? Why: not all checks carry equal risk, so I can rank them.
- Is the 25,000 a week lost benefit or deferred benefit, and does it scale with traffic? Why: if it scales with exposure, a capped launch captures part of it.
- What does a serious defect cost, and who owns that loss? Why: this sets the break-even failure probability.
- Is model-risk's three weeks calendar time or effort, and can parts run in parallel? Why: parallel work shortens the clock.
- Who signs off, and is there a rollback or kill switch? Why: a safe launch needs a reversible one.

**Approach:**
1. Say the delay cost out loud with the model-risk lead and the business head together: 75,000 for 3 weeks.
2. Ask model-risk to rank the remaining checks by what harm they prevent. Keep the top ones non-negotiable.
3. Offer to speed up their work: hand over data, code, and documentation up front, and run checks in parallel.
4. Propose a staged launch: one week of the critical checks, then a 20% exposure launch with monitoring and a rollback trigger, remaining checks finishing in parallel.
5. Tell the business head which checks I will not skip, and why, in terms of loss.
6. Write the decision, owners and rollback thresholds in one page that both sign.

**Metrics:** Cost of delay = weekly benefit x weeks not live. Capped launch captures weekly benefit x exposure share x weeks live. Break-even defect probability = delay cost / loss if a defect ships. Guardrails: defect found in monitoring within the cap, rollback time, share of high-risk checks completed before any launch.

**Risks:**
- A capped launch can still harm the 20% who see it. Pick low-stakes exposure first.
- Model-risk may feel I am going around them. Always give them a veto on the critical checks.
- "Lost benefit" may just be deferred, which makes delay cheaper than it looks.

**What the interviewer scores:**
- Strong: quantifies both sides, ranks checks by risk, offers staging with rollback, keeps model-risk independent.
- Strong: speaks to each party's actual concern.
- Weak: "I would escalate", or "I would skip the low-value checks" without saying how they are chosen.
- Weak: treats model-risk as an obstacle.

**Example:** Illustrative numbers: 25,000 a week, 3 weeks, 75,000. Option B: 1 week of critical checks, then 20% launch for 2 weeks. Benefit captured is 25,000 x 20% x 2 = 10,000, so net delay cost is 65,000. Skipping checks is justified only if the extra defect risk times the loss is below 75,000. With a 1,000,000 loss, break-even is 7.5%, and a 10-point rise in risk is 100,000 expected loss.
- Weak: "We cannot skip checks, that is policy." / "Just ship, three weeks is too long."
- Strong: "The delay costs 75,000. I would not skip the checks that catch the worst failures, but I can get you live on 20% of traffic after week one with a rollback trigger, while the rest finishes."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if model-risk refuses a staged launch? Respect it, show the numbers to the shared sponsor, and ask them to decide with both views on one page.
- What if the business head insists on skipping everything? Say which skipped check I would be unwilling to own, and escalate that item only.

**Common mistakes:** Calling the delay cost a reason to skip checks. Siding with whoever is more senior. Offering a launch with no rollback. Never quantifying the downside.
