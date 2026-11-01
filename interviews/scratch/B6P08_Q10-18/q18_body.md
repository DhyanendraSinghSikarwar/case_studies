**Say this first (1 line):** Monitoring counted HTTP success, not useful answers; I would add a degraded-response metric (fallback flag and the share of exact 0.5 scores), alert on that share, and count the 300,000 past requests from logs.

**Clarifying questions:**
- Does the response say the score is a default, or is it indistinguishable from a real 0.5? It decides whether we can count exactly or only estimate.
- What decisions use the score (ranking, fraud, credit)? It sets how serious 15% defaults are and who must be told.
- Which feature lookup times out, and since when? The start time sets the number of affected requests.
- Is the timeout a symptom of load, a slow store, or a bad deploy? It tells whether the fix is capacity or rollback.
- Are there downstream effects, such as the default score being logged as a label or used in retraining? It would contaminate later data.

**Approach:**
1. First 15 minutes: confirm with logs (rows with a timeout and score exactly 0.5), find when it started, and page the owner of the feature store. Mitigate: raise the lookup timeout or fix the slow store, roll back a bad change, or add a cache and a better fallback than 0.5 (for example the last known feature value or a segment average, as a reasoned choice). Escalate to the incident lead if decisions are money-bearing. Roll back the change if the degraded share does not fall under 1% within a set time after the fix.
2. First day: count affected requests (flag or score 0.5 plus timeout log), segment them (which customers, which hours), assess business impact with the owner, decide whether to re-score or notify. Quarantine default-score rows from training data, labels and metrics.
3. Detection: add a counter `degraded_responses_total` with a reason label (feature_timeout, missing_feature, fallback_model) and ship it as a metric. Return a `degraded=true` field in the response so clients can react. Alert on the degraded share above 1% for 5 minutes. Add feature-coverage metrics (share of requests with all features fresh), score-distribution monitoring (a spike at one exact value), and a synthetic canary request every minute.
4. Change the SLI: availability should count a request as good only if it is 200 and not degraded, and latency is measured on good requests. Here the useful share is 84.9%, not 99.9%.
5. Next quarter: set an SLO for degraded share (for example 99% non-degraded), track feature-store latency and timeout budgets, and run a game day that breaks the lookup.
6. Blameless postmortem: the service did what it was coded to do (return 0.5 on timeout). The gap is that nobody defined "healthy" beyond HTTP. Detection delay is unknown (days at 300,000 requests); with the alert it is 5 to 10 minutes. Action items: metric, alert, response flag, SLI change.

**Metrics:**
- Degraded share = degraded responses / all responses = 300,000 / 2,000,000 = 15% (the HTTP error rate is only 0.1%, or 2,000 requests).
- Useful-response SLI = (200 and not degraded) / all = 84.9% in this incident.
- Per 5-minute window: about 6,944 requests; alert at 70 or more degraded (1%), normal is about 7 (0.1%).
- Guardrail: false-alarm rate of the alert and the rate of legitimate 0.5 scores.

**Risks:**
- Counting exact 0.5 as degraded over-counts if real scores can equal 0.5 (illustratively 400 requests a day at 0.02%); use the flag, not the value.
- The default of 0.5 may be fed to downstream rules or logged as a prediction; check consumers.
- A very sensitive alert pages on every blip; use a window and a floor.
- A new fallback (last known value) hides the problem unless the degraded counter still fires.

**What the interviewer scores:**
- Strong: defines healthy as useful answers, not HTTP 200; proposes a flag, a metric and an alert threshold with arithmetic.
- Strong: counts the damage after the fact and cleans training data.
- Strong: first 15 minutes, first day, next quarter; blameless action items.
- Weak: "add more dashboards"; "alert on latency".

**Example:** Illustrative numbers. Weak versus strong:
- Weak: "I would add more dashboards for the feature store."
- Strong: "Our SLI counted 200s, so 15% defaults looked fine; the useful rate was 84.9%. I would add a degraded counter with a reason label, page when it passes 1% for five minutes, which is about 70 requests against a normal 7, and return a degraded flag in the response. Then I would count the 300,000 from logs, keep them out of training, and run a blameless review of what 'healthy' meant."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Why not alert on exact 0.5? It can be legitimate; flag fallbacks explicitly and use the score spike as a second signal.
- What fallback is better than 0.5? A cached last-known feature or a segment average, chosen with the business, with the degraded flag still set.
- How do you handle past decisions? Re-score those with correct features where possible and decide with the owner whether to correct or notify.

**Common mistakes:**
- Using HTTP status as the only health signal.
- Using the score value instead of an explicit flag.
- Leaving default-score rows in training data.
- Alerting without a window or a baseline.
