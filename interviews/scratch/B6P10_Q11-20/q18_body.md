**Say this first (1 line):** 20,000 metrics x 1,440 minutes = 28,800,000 points a day, so 15 false alerts a day means a false-alert probability of at most 15 / 28,800,000 = 5.2 in ten million per point; that is a very strict threshold, so I would alert on persistent, grouped, business-relevant deviations, not on single points.

**Clarifying questions:**
- What does a "false alert" mean to on-call: a spike that self-heals, a real anomaly nobody needs to act on, or noise? Only actionable alerts count against the 15.
- Which metrics matter most (customer-facing, revenue, errors) and which are noise? Tiering lets the strict budget go to the right ones.
- Are metrics seasonal (daily and weekly cycles, deploys, campaigns)? Seasonality is the main source of false alerts.
- Are metrics correlated (one outage moves hundreds)? It decides how alerts should be grouped.
- Is there labelled incident history? Without it I can only estimate false alerts by replay and on-call feedback.

**Approach:**
1. Clarify and frame. Goal: catch incidents that need a human, within 15 false alerts a day, across 20,000 metrics. Separate detection (score each point) from alerting (decide who is paged).
2. Metrics and guardrails. Precision of pages (actionable pages / pages), recall of known incidents, time to detect, false pages per day. Guardrail: the 15 a day budget and missed severe incidents.
3. Data and labels. Collect past incidents, on-call acknowledgements and "not actionable" marks. Few metrics have labels, so evaluate on a sample of important metrics and by replay of history.
4. Baseline first. Static thresholds plus a same-hour-last-week comparison with robust scale (median and median absolute deviation). Measure false pages by replay.
5. Model and trade-offs. Per-metric forecast with seasonality, residual scoring, a persistence rule, then grouping by service or time. Budget maths: 28,800,000 points, so a per-point false probability of 5.2e-7, roughly a 4.9 sigma Gaussian threshold (see the code); real residuals have heavier tails and autocorrelation, so I would calibrate thresholds on history rather than trust the Gaussian. Trade-off: stricter thresholds cut false pages but delay or miss small real anomalies.
6. Evaluation. Offline replay on 3 to 6 months: false pages per day, recall of past incidents, detection delay. Online: shadow alerts to a channel before paging, then page only the tiered top metrics.
7. Launch and experiment plan. Shadow for 2 to 4 weeks, tune thresholds per tier, page on tier 1 first. Review every false page weekly.
8. Monitoring, retraining and risks. Track false pages per day against 15, refit forecasts on schedule, add holiday and deploy calendars, suppress alerts during known maintenance.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 5, 5, 11, 6, 5, 5.

**Metrics:**
- Points a day = metrics x points per metric = 20,000 x 1,440 = 28,800,000.
- Maximum per-point false-alert probability = allowed false alerts / points = 15 / 28,800,000 = 5.2083e-7 (this is expected value, which needs no independence).
- Precision of pages = actionable pages / all pages; recall = incidents caught / incidents that occurred.
- Detection delay = time from incident start to page; false pages per day.
- Guardrail: false pages per day under 15.

**Risks:**
- Alert fatigue: if on-call stops trusting pages, real incidents get missed.
- Autocorrelation and bursts: false alerts arrive in clusters (one noisy hour), so the day-to-day count varies more than the average suggests.
- Seasonality and deploys cause predictable false positives.
- A very strict threshold may miss small but real degradations.
- Correlated failures produce alert storms; grouping is essential.

**What the interviewer scores:**
- Strong: 28.8 million points and 5.2e-7 per point, noticing how strict it is.
- Strong: persistence rules, tiering, grouping, seasonal baselines, and replay evaluation.
- Strong: says grouping raises the allowed per-point probability but the budget is really per page.
- Weak: "train an autoencoder on all metrics" with no alert budget or evaluation.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "Flag anything beyond 3 standard deviations."
- Strong: "20,000 metrics a minute is 28.8 million points a day, so to stay at 15 false alerts the per-point false rate must be near 5 in ten million. Three sigma would page thousands of times, so I would use seasonal forecasts, require persistence over several minutes, group by service so one outage is one page, tier the metrics, and tune on replayed history with on-call feedback."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- How does grouping change the answer? The budget applies to pages, not points; if 20 correlated metrics become one page, the per-point probability can be about 20 times higher for the same page count (1.04e-5), but only if they really fail together and are grouped reliably.
- What does a 3-sigma rule cost? A one-sided 3-sigma tail is about 0.00135 per point, which is about 38,900 false alerts a day on 28.8 million independent Gaussian points, far above 15.
- How do you handle new metrics? Start in shadow with a longer warm-up and a looser tier until history exists.

**Common mistakes:**
- Forgetting to multiply by 1,440 points per metric per day.
- Assuming independent Gaussian noise and trusting the resulting z threshold.
- Counting alerts per metric instead of per page.
- Tuning thresholds on only the incidents, with no replay for false alerts.
