**Say this first (1 line):** I put numbers on both paths: waiting costs the daily loss times the retrain days, and a patch is worth it when what it recovers, net of its own side-costs and build cost, beats that; I ship the patch only with a backtest, a shadow run, a kill switch and a sunset date.

**Clarifying questions:**
- How certain is the Rs 2 lakh a day figure, and how does it vary by day? The whole case depends on it.
- What does the patch do (extra rule, higher cut-off, manual review) and what is the side-effect, for example good customers wrongly declined?
- Can the patch be backtested on recent data before launch? A crude rule with no backtest can cost more than it saves.
- Is the retrain date firm at two weeks, or could it be faster with a reduced scope?
- Who owns the patch and who can switch it off?

**Approach:**
1. Cost of waiting = daily loss x retrain days. Here 2 lakh x 14 = Rs 28 lakh.
2. Model the patch: days it is live x (share of loss it recovers x daily loss - its daily side-cost) - build cost. Include the day or two before it is live.
3. Find the break-even recovery fraction and the sensitivity: how much must the patch recover to pay for itself, and what happens in a bad case?
4. Test the patch: backtest on the last few weeks of matured data; run it in shadow for a day or two if time allows; check segment effects and customer impact; define a rollback rule and who can use it.
5. Roll out in steps (a share of traffic first) with monitoring of loss, declines and complaints.
6. Retire it: define the exit before launch. Switch it off when the retrained model beats model plus patch on matured data, delete the code by a fixed date, and record it in the change log.
7. Do the retrain in parallel and ask whether the scope can be cut to deliver sooner.

**Metrics:**
- Net benefit of patch = (retrain days - days before live) x (loss per day x recovery fraction - side-cost per day) - build cost.
- Break-even recovery fraction = (build cost / days protected + side-cost per day) / loss per day.
- Guardrails: wrongful decline rate, approval rate, complaints, loss per day by segment.

**Risks:**
- The recovery fraction is an estimate; an untested rule may recover little and hurt customers.
- Patches become permanent and interact with the new model.
- The loss estimate may itself be wrong.
- Fast, ad hoc changes to a risk decision may bypass model-risk governance.

**What the interviewer scores:**
- Strong: quantifies both options, finds a break-even and a worst case. Weak: "patches are hacky" or "ship it".
- Strong: designs the test and the exit. Weak: no plan to remove the patch.
- Strong: respects governance (approval, audit). Weak: ignores it.

**Example:** (illustrative, Rs lakh) Waiting 14 days costs 2 x 14 = 28. A patch live from day 1 protects 13 days. If it recovers 50% of the daily loss (1.0) with a side-cost of 0.2 a day and a build cost of 1.5, the net is 13 x (1.0 - 0.2) - 1.5 = 8.9. Break-even recovery is 15.8%. At 10% recovery the patch loses 1.5; at 20% it gains 1.1; at 30%, 3.7; at 70%, 14.1. In a bad case (20% recovery, side-cost 0.4 a day) it loses 1.5. So I would ship the patch if the backtest supports recovery well above about 16% and the side-cost is controlled. Weak: "Wait for the proper retrain." Strong: "The patch pays for itself above about 16% recovery; I will backtest it, stage it, and set its sunset date."

**Code:**
