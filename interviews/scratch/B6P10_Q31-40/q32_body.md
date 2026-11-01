**Say this first (1 line):** Raw reporting is 3,456,000 bytes per bike per day against a 2,000,000 cap, so I need at least a 1.73x cut, and I would get it by summarising on the bike and uploading only the windows around suspicious events.

**Clarifying questions:**
- What does a battery fault cost (fire, a stranded rider, a replacement) and what lead time is useful? It sets how many false alerts are tolerable.
- Are there any labelled faults, or only maintenance records with dates? It decides supervised versus anomaly methods.
- Is the 2,000,000 bytes a hard cap or a cost target? A hard cap forces on-bike processing.
- What is the compute on the bike and can it run a small model? It decides where detection runs.
- How are faults defined (voltage sag, temperature rise, rapid capacity loss) and who acts on an alert? A rule nobody acts on has no value.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data and labels 6, baseline 6, model 8, evaluation 6, rollout and monitoring 6, risks and cost 4):**
1. Clarify and frame: predict a fault early enough to swap a battery, within a data cap.
2. Metrics and guardrails: recall of true faults with enough lead time, alerts per bike per month (workload), bytes per bike per day.
3. Data and labels: faults are rare, so label from maintenance and swap records; expect few positives and noisy dates.
4. Baseline first: threshold rules (voltage drop under load, temperature rise above a per-bike baseline). They are cheap, explainable and fit on the bike.
5. Model and trade-offs: robust per-bike baselines and a small anomaly score on summaries (rolling statistics); add a supervised model only when there are enough labelled faults. Bandwidth: raw is 17,280 readings x 200 = 3,456,000 bytes, factor needed 1.728. Options: one reading every 9 seconds (1.92 MB, loses detail), or a 400-byte summary a minute (576,000 bytes, a 6x cut) with about 118 sixty-reading event windows of spare cap.
6. Evaluation: replay history, measure recall at a fixed number of alerts, and check lead time; do not use accuracy.
7. Rollout: shadow alerts to the maintenance team, compare with their findings, then act on the top alerts; keep a fallback rule that works offline.
8. Monitoring and cost: alert precision from technician feedback, drift by battery age and season, cap usage per bike; retrain when the fault mix changes.

**Metrics:**
- Recall of faults = faults alerted at least N days before failure / all faults in the period.
- Precision of alerts = alerts that technicians confirm / alerts raised.
- Bytes per bike per day (guardrail <= 2,000,000) and alerts per bike per month.

**Risks:**
- Very few labelled faults; any recall number is a wide range.
- Summaries can hide the short spike that matters; keep an event-window upload.
- Seasonal heat and rider weight shift the baseline.
- Mobile dropouts create gaps that look like anomalies.

**What the interviewer scores:**
- Strong: computes 3,456,000 bytes and 1.728x, then chooses where processing happens.
- Strong: starts with rules, uses recall at an alert budget, and speaks about label scarcity.
- Weak: proposes a deep model with no labels; ignores the cap; quotes accuracy on rare faults.

**Example:** Illustrative numbers. 86,400 / 5 = 17,280 readings; x 200 B = 3,456,000 B; / 2,000,000 = 1.728.
- Weak: "Train an LSTM on all sensor data and flag anomalies."
- Strong: "Raw is 3.46 MB a day and the cap is 2 MB, so I need at least 1.73x. I would summarise each minute on the bike, which is about 0.58 MB, and keep the rest of the cap for raw windows around rule hits. I start with per-bike threshold rules, because I have few labelled faults."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *Why not just send every 9 seconds?* It fits (1.92 MB) but loses the short event; summaries plus windows keep the shape of the spike.
- *Which metric with so few faults?* Recall at a fixed alert budget, with a range from the few positives.

**Common mistakes:** Forgetting per-day conversion. Treating the cap as per fleet. Quoting accuracy. Training before there is a rule baseline.
