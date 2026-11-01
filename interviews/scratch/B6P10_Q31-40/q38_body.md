**Say this first (1 line):** Break-even accuracy is 20,000 / 20,800 = 96.15%, the replay's 97% sits only a little above it with an interval that crosses it, so I would not give the agent full autonomy; I would start with suggestions and approvals and widen autonomy as live evidence builds.

**Clarifying questions:**
- Is 20,000 rupees the whole cost of a wrong restart, or the extra cost on top of the lost saving? It is the loss term in the break-even.
- Were the 400 replayed incidents random or the easy ones? A sample from a biased set overstates accuracy.
- Do errors cluster by service (a database restart is not like a stateless one)? Averages hide the dangerous cases.
- Can a restart be undone quickly, and what is the blast radius? It changes how much risk is tolerable.
- Who is on call and how fast can a human intervene? It decides which autonomy level fits.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 5, data 5, baseline 4, model and autonomy design 10, evaluation 6, rollout 6, monitoring and risks 4):**
1. Clarify and frame: a decision under unequal costs, so the threshold comes from the cost ratio.
2. Metrics and guardrails: accuracy of the action (right action / actions taken), cost per incident, rollback rate, incidents made worse.
3. Data and labels: replayed incidents with an expert label of the correct action; add live shadow decisions.
4. Baseline first: runbook rules and the current manual handling cost.
5. Model and autonomy levels: L0 recommend only, L1 act after one-click approval, L2 act alone on low-risk services with a confidence threshold, L3 broader scope. Break-even: 800 p = 20,000 (1 - p), so p = 0.9615. Expected value at 97% is 800 x 0.97 - 20,000 x 0.03 = 176 rupees per incident; at the break-even it is zero. The 95% Wilson interval for 388 of 400 is 94.8% to 98.3%, so the true accuracy may be below break-even, where the expected value is negative (-275 at the lower end).
6. Evaluation: replay on a larger, stratified set; if the true accuracy is 98%, about 1,000 incidents put the lower bound (96.9%) above break-even, while 400 do not (96.1%).
7. Rollout: L0 then L1 in shadow, measure agreement with humans; L2 for stateless services with a cap on actions per hour and an automatic stop after errors; widen by evidence.
8. Monitoring and risks: live accuracy with an interval against 96.15%, a kill switch, audit log of every action; limiting the cost of a wrong action (for example to 5,000) lowers the break-even to 86.2%.

**Metrics:**
- Accuracy = correct autonomous actions / autonomous actions taken (388 / 400 in the replay).
- Break-even accuracy = loss / (saving + loss) = 20,000 / 20,800.
- Net value per incident = 800 x accuracy - 20,000 x (1 - accuracy); guardrails: actions per hour, rollbacks, repeat incidents.

**Risks:**
- A replay is a sample and is not live behaviour; novel incidents are missing.
- Errors can be correlated (one bad action triggers many).
- Averaging hides a high-cost service class.
- Over-trust: humans stop checking.

**What the interviewer scores:**
- Strong: derives 96.15%, computes 176, and says the 97% sample does not clear it with confidence.
- Strong: levels, a kill switch and a cap on blast radius.
- Weak: "97% is above 96%, ship it"; no interval; no rollback.

**Example:** Illustrative numbers. 20,000 / 20,800 = 0.9615; 388 / 400 = 0.97; Wilson interval 0.948 to 0.983.
- Weak: "It is 97% accurate, which is better than the 96% we need, so let it run."
- Strong: "Break-even is 96.15 percent and we saw 97 percent on 400 replays, but the range is 94.8 to 98.3, so we cannot rule out losing money. I would run it with approvals first, restrict it to low-impact services, and move up only when the live lower bound clears break-even."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *What if wrong actions could be capped at 5,000?* Break-even falls to 86.2%.
- *Would more samples help?* Yes if accuracy is really 98%: about 1,000 incidents put the interval above break-even.

**Common mistakes:** Comparing 97% with 96% as if exact. Ignoring the interval. One accuracy for all services. No kill switch. Treating replay as live.
