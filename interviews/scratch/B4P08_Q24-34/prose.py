Q = {}

Q[24] = dict(
say="If the scores are calibrated, each score is the chance the prediction is right, so I can add those chances up to get expected accuracy and precision with no labels; it holds under covariate shift, and it breaks under concept drift or miscalibration, so I use it as an early estimate and then confirm with real labels.",
explain="""- **The idea:** a calibrated score of 0.8 means 8 in 10 such cases are positive. So for every row you know the expected true positive, false positive, false negative and true negative. Sum them over a batch, then read off accuracy, precision, recall.
- **Where it works:** covariate shift. The inputs change (new customer mix), scores move, but `P(y | x)` is the same, so the calibration still holds and the estimate tracks the truth.
- **Where it fails:** concept drift (the link from inputs to outcome changed, scores stay confident but wrong) and a model that was never calibrated. The estimate then stays flat and happily wrong. Calibration is a claim about the past; the method assumes it still holds.
- **NannyML CBPE:** this is the same family as NannyML's confidence-based performance estimation. I only describe the idea here, I do not reproduce its internals; check current docs for what the library adds (for example the calibration step).
- **Limits:** needs a threshold, needs a calibrated model checked on recent labelled data, and gives an estimate with noise at small batch sizes. It is blind to the very thing (concept drift) that hurts most. Keep a label-based metric when labels mature.""",
example="""Four predictions with scores 0.9, 0.8, 0.6, 0.3 and threshold 0.5. Predicted positive: 0.9, 0.8, 0.6. Expected TP = 0.9+0.8+0.6 = 2.3, expected FP = 0.1+0.2+0.4 = 0.7. The 0.3 row is predicted negative: expected FN = 0.3, expected TN = 0.7. Accuracy = (2.3+0.7)/4 = 0.75. Precision = 2.3/3 = 0.767. In the run below the same formulas are applied to 200,000 simulated rows.""",
code=[("python", ["cbpe_lite.py"])],
outnote="(real run, Python 3.13, numpy 2.5.4, seed 24; no labels are used for the estimate, labels are only simulated to get the truth)",
follow="""- **What if the model is not calibrated?** Calibrate first (isotonic or Platt on a recent labelled set), then check the reliability curve. Without that, the estimate is not meaningful.
- **Can you detect that concept drift happened?** Not from this estimate. Use the label-based metric when labels mature, a canary label sample (Q25), or watch for a gap between estimated and observed performance.""",
mistakes="""- Trusting the estimate on a model that was never calibrated.
- Using it as proof that nothing is wrong. It cannot see concept drift.
- Using one threshold in the estimate and a different one in production.
- Reporting a point estimate from a few hundred rows without an interval.""")

Q[25] = dict(
say="Labels cost money, so I label a sample, not everything: stratify by score, give each case an inverse-probability weight, and size the sample from the margin I want, which for plus or minus 3 points on precision is a few hundred labels, not thousands.",
explain="""- **Sampling choices:** random is simple and unbiased. Stratified by score gives lower variance and lets you put more labels where the model is least sure. Score-weighted (for example only labelling the highest scores) is cheap but biased unless you reweight.
- **Sample size:** `n = z^2 * p(1-p) / margin^2`. If you do not know `p`, use 0.5 for the worst case. If you expect precision near 0.9, you need far fewer labels.
- **Reweighting:** if a case had sampling probability `pi`, count it with weight `1/pi`. Stratified estimate is `sum(N_h * p_h) / N`. Interval uses the within-stratum variance.
- **Failure modes:** labelling only easy or convenient cases and not reweighting; reviewers who see the model score and agree with it; sample too small per stratum (one or two labels give no variance); forgetting that "90 percent" can mean the confidence level or the expected precision, so state which.
- **Scope:** this is about precision of flagged cases. Recall needs labels from the unflagged cases too, which is usually the expensive part.""",
example="""Hand check of the formula: 90% confidence, margin 0.03, expected precision 0.9. z = 1.645, so n = 2.706 x 0.09 / 0.0009 = 270.6, round up to 271. With the worst case p = 0.5 it is 752. Weighting example: 1,000 cases in a low stratum with 80% correct and 9,000 in a high stratum with 95% correct. Estimate = 0.1 x 0.80 + 0.9 x 0.95 = 0.935, not the simple mean of the two samples.""",
code=[("python", ["label_budget.py"])],
outnote="(real run, numpy 2.5.4, scipy 1.18.1, seeds 25, 250, 251; labels for the whole population are simulated so we know the truth)",
follow="""- **Why oversample low scores?** That is where the label is least predictable, so variance is highest. A Neyman-like allocation puts more labels there, and the weights fix the bias.
- **Can I label only the top scores?** You get a cheap number that is wrong (0.9747 vs 0.9124 above). Weights only help if every stratum has a non-zero chance of being sampled.""",
mistakes="""- Sizing the sample with the wrong meaning of "90 percent".
- Not weighting a deliberately skewed sample.
- Giving reviewers the model score, so labels copy the model.
- Reporting a number without an interval.""")

Q[26] = dict(
say="An SLI is a measured good-over-total ratio, an SLO is the target, the error budget is what is left, and I alert when the budget burns fast in both a long and a short window; for ML I add data-quality SLIs, which is my extension of the SRE idea, not a standard.",
explain="""- **Plain SRE part:** SLI = good events / all events over a window. SLO = target, say 99 percent. Error budget = 1 minus the SLO. Burn rate = (actual bad share) / (allowed bad share). Burn 1 means you spend the budget exactly at the pace allowed. Availability and latency SLIs are Part 6.
- **ML-specific SLIs (extension, not a standard):** data validity rate (rows passing checks), feature freshness, share of predictions with a drifted-input flag, matured-label metric (accuracy on labels that have arrived), model age.
- **Two windows:** page only when a long window shows real budget loss and a short window shows it is still happening. That avoids paging on a blip and avoids paging after the problem is already fixed. The SRE Workbook chapter on alerting on SLOs describes multiwindow, multi-burn-rate alerts; check it for the thresholds, the ones below are illustrative.
- **Where it does not fit:** slow labels. A label-based SLI is days late, so a burn rate on it is a ticket signal, not a page. Use fast proxy SLIs (data validity, null rate, score distribution) for paging.
- **Failure modes:** a window shorter than the data cadence (hourly counts and a 5 minute window); SLO set with no owner; too many SLOs.""",
example="""SLO 99 percent, so budget is 1 percent. In hour 34 the bad share is 8.6 percent, so the 1 hour burn is 8.6 / 1 = 8.6. The 6 hour window covers hours 29 to 34: bad shares 0.6, 7.9, 7.9, 8.2, 8.0, 8.6 average to about 6.9, so burn 6.9. Both are at or above 6 (my illustrative threshold), so the two-window rule fires at hour 34. At hour 38 the feed is fixed: 1 hour burn drops to 0.3, so the two-window rule stops while the long window alone would still fire.""",
code=[("python", ["burn_rate.py"])],
outnote="(real run, numpy 2.5.4, seed 26; hourly counts are simulated: a data bug from hour 30 to 37)",
follow="""- **Why not alert on the SLO itself?** It reacts too late and too slowly. Burn rate tells you how fast you are heading to a miss.
- **What window do I use for labels?** Do not page on label metrics. Use a ticket on the matured window and keep the paging SLIs on fast signals.""",
mistakes="""- Presenting ML SLIs as if there is a standard.
- Paging on a single long window, which keeps firing after recovery.
- Using thresholds copied from a blog without checking your own budget maths.
- Counting bad rows without counting traffic, so quiet hours look worse.""")

Q[27] = dict(
say="Every alert gets one owner, a severity, a runbook link and a first safe action, I check that with a script so an alert without those cannot merge, and Alertmanager routes by those labels so the right team gets it.",
explain="""- **Who is paged:** by cause, not by model. Broken feed or null spike: data engineering. Drift or score-shape change: data science. Stale model or failed retrain job: ML platform. Anything user-visible and urgent goes to whoever is on call for the service, then they hand over.
- **A runbook has:** what the alert means, how to confirm (which dashboard, which query), safe first actions (fall back to the previous model or a rule, pause automatic decisions), who to escalate to, and how to close it (what has to be true, what to write down).
- **Orphan alerts:** keep the catalogue in git, check it in CI (every alert has owner, severity, runbook, action; owner must be a real team), and review alerts that nobody acted on every quarter. An alert with no owner gets deleted or fixed.
- **Alertmanager routing:** group by alert name and model, route by `owner` and `severity` labels, keep a default receiver so nothing is dropped. Shown below, but Alertmanager was not run here.
- **Failure modes:** owner is a person who left; runbook link is dead; "page" severity with no clear action; routing tree that sends two teams the same alert.""",
example="""`FeatureNullRateHigh` has owner `data-engineering`, severity `page`. The route matches severity=page and owner=data-engineering, so it reaches `data-eng-pager`. `ModelStale` is a ticket owned by `ml-platform`; no child route matches it, so it falls through to the default receiver `ml-platform-ticket`. The first draft of the catalogue had one alert with no action, and the validator caught it; the version below is the fixed one.""",
code=[("yaml", ["catalogue.yaml", "alertmanager.yml"]), ("python", ["validate_catalogue.py", "check_routing.py"])],
outnote="""not executed: Alertmanager was not available in this sandbox and the receivers have no real integrations. What did run: the Python validator on the catalogue (a good file and a deliberately bad file) and a script that parses `alertmanager.yml` with PyYAML 6.0.3 and checks that every route points to a defined receiver (python3 -I).""",
follow="""- **How do you stop alert sprawl?** Each alert needs an owner and an action, review which alerts led to action, delete or demote the rest.
- **Who owns a drift alert when the cause is upstream?** Data science confirms and routes to the upstream owner; the runbook says so.""",
mistakes="""- A runbook that says "investigate".
- Paging for things that can wait until morning.
- Routing everything to one shared channel.
- Never testing the route (send a test alert after each change).""")

Q[28] = dict(
say="Without labels I watch selection rate and score distribution per group; with labels I add the true positive rate gap and calibration by group; I always attach an interval and a minimum group size, so a tiny group does not page anyone.",
explain="""- **No labels needed:** selection rate (share approved or flagged) per group, the selection-rate ratio against a reference group, score distribution per group. These can move for legitimate reasons, so they are a signal, not a verdict.
- **Labels needed:** TPR and FPR gap by group (equal opportunity looks at the TPR gap), calibration by group. These arrive late, so they are a slower check.
- **Small groups:** a group of 100 gives a wide interval. A Wilson interval for the rate shows how wide. Alert only when the group has a minimum count and even the favourable end of the interval breaks the rule. For tiny groups, pool over longer windows.
- **Indian context (hedged, check current guidance):** sensitive attributes such as caste or religion may not be collected or may not be allowed to be used, so teams use proxies (region, language, device tier) and offline audits on a consented sample. Do not quote a legal rule from memory; check current guidance and counsel.
- **Failure modes:** the 0.8 ratio is a US-origin rule of thumb (four-fifths), not Indian law; proxies can be wrong; alerting per group per hour multiplies false alarms.""",
example="""Week 2, group C has 108 decisions and selection 0.278 against the reference 0.362: ratio 0.77, below 0.8. The naive rule fires. The Wilson interval is [0.20, 0.37], so the data are also consistent with parity; and n < 200, so the guarded rule stays quiet. In weeks 3 and 4, group B (over 1,000 rows) has ratio 0.37 and 0.44 and an interval that is clearly below, so the guarded rule fires. That is the injected problem.""",
code=[("python", ["fairness.py"])],
outnote="(real run, pandas 3.1.0, numpy 2.5.4, seed 28; outcomes and a drop in group B's scores from week 3 are simulated)",
follow="""- **What if C is really being harmed?** The guard hides it in a single week. Pool several weeks for small groups, and do a periodic offline audit.
- **Is a ratio under 0.8 a violation?** No. It is a convention to start an investigation. Check current guidance for your market.""",
mistakes="""- Alerting on a small-group rate with no interval.
- Treating selection-rate gaps as proof of bias, or as proof of none.
- Reporting group metrics only at training time.
- Using a sensitive proxy without a review of what it encodes.""")

Q[29] = dict(
say="Log only what I need, from an allow-list, redact patterns in free text, replace the customer id with a keyed hash, set a retention limit, and be honest that none of this makes the data anonymous.",
explain="""- **What can be personal data:** direct identifiers (name, email, phone, ID numbers), but also a customer id, device id, exact location, and sometimes a combination of ordinary features. Predictions about a person are personal data too.
- **Controls:** minimise (allow-list fields), mask or redact patterns in free text, pseudonymise ids with a keyed hash (HMAC) with the key in a secret manager, short retention, role-based access, a way to find and delete one person's records on request.
- **Audit vs minimisation:** audit wants enough to reproduce a decision (model version, inputs used, score, decision); minimisation wants less. Settle it with a written purpose, log the features the model used rather than the raw record, and keep access tight.
- **Legal text:** I have not quoted the India DPDP Act and Rules, GDPR or sector rules here. Check the current text and ask your privacy or legal team about retention and deletion duties.
- **What the code does not protect:** regexes miss formats; a keyed hash of a small id space can be reversed by anyone with the key; free text may hold names; combinations of fields can re-identify; it does nothing for backups or downstream copies.""",
example="""Record 1 has an email and phone in the note and a PAN number in a field that is not on the allow-list. After `safe_record`, the PAN field is gone, the note reads `caller [EMAIL] asked on [PHONE]`, and `C1001` becomes a 16-character id that is the same in every record for that customer, so you can still join and count per customer.""",
code=[("python", ["safe_log.py"])],
outnote="(real run, Python 3.13, standard library only; the salt in the file is a demo value)",
follow="""- **Why HMAC and not a plain hash?** A plain hash of a guessable id can be reversed by trying all ids. A keyed hash needs the key, but is still pseudonymous, not anonymous.
- **How do you handle a deletion request?** Keep an index from the pseudonymous id to storage locations, or store logs partitioned so one person's records can be found, and delete or tombstone them.""",
mistakes="""- Logging the full request body "for debugging".
- Hard-coding the salt in the repo.
- Calling hashed data anonymous.
- Keeping logs forever because storage is cheap.""")

Q[30] = dict(
say="I write alerts that must hold for a duration before they fire, keep Alertmanager routing and inhibition separate from the rules, and say honestly that here I only checked the YAML structure and re-implemented the for-logic, because Prometheus, Alertmanager and promtool were not available.",
explain="""- **Rules:** sustained high drift score for 2h, null rate above a limit for 15m, label-join lag, model older than a set age. The `for:` clause makes the alert pending first and firing only if the expression stays true for the whole time; one good sample resets it.
- **Alertmanager route:** group by alertname and model so ten features do not make ten pages; `group_wait`, `group_interval` and `repeat_interval` control batching and repeats.
- **Inhibition:** if `UpstreamFeedDown` is firing for a model, mute the drift, null-rate and score-shift alerts for the same model (`equal: [model]`), since they are consequences. Silences are manual and time-boxed, for planned work.
- **Failure modes:** `for` shorter than the scrape or scoring cadence; a metric that disappears (stale series) so the alert never fires, so also alert on absence; high-cardinality labels; metric names in this answer are my own.
- **Not run:** promtool, Prometheus, Alertmanager.""",
example="""Drift is scored every 30 minutes; the rule is score above 0.3 for 2 hours, which is 4 samples in a row. In the series below, two high samples then a dip to 0.2 resets the clock. Four high samples in a row (t=120 to 210) make it fire at t=210. One spike never fires.""",
code=[("yaml", ["ml_rules.yml", "alertmanager.yml"]), ("python", ["check_files.py", "for_logic.py"])],
outnote="""not executed: promtool, Prometheus and Alertmanager were not installed here, so the rules and routing were not evaluated by the real tools. What did run: PyYAML structural checks (alert, expr, for format, labels, runbook link, receivers exist, inhibit fields) and the pure-Python `for` logic below. Passing this check does not prove the PromQL is valid.""",
follow="""- **Does `for` cause late pages?** Yes, by design: you trade speed for fewer false alarms. Use a short `for` for page-worthy data faults and a long one for drift.
- **How do you alert on a metric that stops?** Alert on absence (for example `absent()` or a last-success timestamp), as in `UpstreamFeedDown`.""",
mistakes="""- Alerting on a raw drift score with no duration.
- Forgetting inhibition, so one feed outage sends five pages.
- Calling a YAML parse "validated alerting".
- Silences with no expiry.""")

Q[31] = dict(
say="Both managed monitors work the same way at concept level: take a baseline from training data, turn it into constraints or thresholds, capture live requests, compare on a schedule and report violations; they need your data capture and, for quality metrics, your labels, and they do not decide what to do about a violation.",
explain="""- **SageMaker Model Monitor (check current docs):** monitoring types for data quality, model quality, bias drift and feature attribution drift. A baseline job profiles training data and suggests statistics and constraints; scheduled jobs compare captured endpoint data against them. Model quality needs ground-truth labels you supply.
- **Vertex AI Model Monitoring (check current docs):** skew compares serving data with training data; drift compares serving data over time. Thresholds per feature, and request data can be logged to BigQuery. Attribution-based monitoring uses Explainable AI.
- **Azure ML:** has its own model monitoring; not covered here, check current docs. Parts 10 and 11 own the cloud services.
- **They do not:** fix the cause, retrain, page the right person unless you wire it, or tell you whether a flagged drift matters for accuracy. Labels, thresholds and ownership are still your job.
- **Failure modes:** baseline from a bad sample; thresholds left at defaults; alert noise; capture sampling rate too low for rare classes.""",
example="""A training set has `income` between 7,906 and 169,360, a null share of 2 percent, and `channel` in {app, web, branch}. A baseline step writes those as constraints (with slack on nulls). A serving sample with 20 percent null `age`, income mean 38 percent above reference and 14.8 percent unseen `channel` values fails three checks. This mirrors the workflow, not any vendor's schema.""",
code=[("python", ["constraints_check.py"])],
outnote="""not executed for SageMaker Model Monitor, Vertex AI Model Monitoring and Azure ML: no cloud account or access here. What did run: my own constraints-style baseline and checker (pandas 3.1.0, numpy 2.5.4, seed 31); the field names are mine and are not any vendor's format. The JSON it wrote is code/q31/constraints.json.""",
follow="""- **Skew vs drift?** Skew: serving differs from training. Drift: serving changes over time. You need training data for skew.
- **Why build your own anyway?** Cross-cloud needs, custom checks, and control of alert routing. A managed monitor is a good start.""",
mistakes="""- Thinking a managed monitor means monitoring is done.
- Leaving default thresholds.
- Forgetting to give it labels for model quality.
- Quoting service limits from memory.""")

Q[32] = dict(
say="For a batch run I validate the run itself, not each row: input volume and schema, nulls, output row count equals input, runtime, and score distribution against the last run and the reference, and I fail the run before results are published.",
explain="""- **Per run checks:** input rows versus last run, schema, null rate, output rows equal input rows, runtime versus normal, score distribution versus last run and the reference set.
- **Cadence:** a drift test per run is cheap for a daily batch; labels join later (days or weeks), so a performance check is a lagged job, not part of the run gate.
- **Real-time difference:** real-time uses rolling windows and alerts with `for` durations; batch has a natural unit (the run) so you can block publishing. Part 5 owns the scheduler and Part 6 batch serving mechanics.
- **Failure modes:** comparing only with the last run so a slow drift is never caught (also compare with the reference); a truncated input that still produces a matching output; a threshold on row count that breaks on holidays; blocking forever with nobody on call.
- **Action on failure:** keep yesterday's output, alert the owner, do not publish.""",
example="""Three nights. Night 1: 10,200 rows against 10,000 last time, passes. Night 2: 4,100 rows is 41 percent of last night, fails on volume (a truncated extract). Night 3: row count fine but scores moved (KS D = 0.58 against last run and reference), fails on score distribution.""",
code=[("python", ["batch_validate.py"])],
outnote="(real run, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, seed 32; the batches are simulated. The 0.7 to 1.3 row ratio, 2x runtime and KS 0.1 limits are my illustrative choices, tune them on your history.)",
follow="""- **Why did night 2 not fail on runtime?** A short run is not checked here; add a lower bound if truncation matters to you.
- **Last run or reference?** Both: last run catches sudden changes, reference catches slow drift.""",
mistakes="""- Letting a failed validation still publish scores.
- Comparing only with yesterday.
- KS on a huge batch with no minimum effect size.
- Not storing the per-run metrics, so there is no history to set limits from.""")

Q[33] = dict(
say="If the model decides which cases get a label, retraining on those labels learns a biased picture: the measured metric looks fine while the true metric on everyone is worse, so I keep an exploration holdout, weight it, and gate retrains.",
explain="""- **Selection bias:** loans are approved by the old policy and only approved loans get repayment labels; fraud blocked is never confirmed. The new model is trained and measured only on the cases the old model liked.
- **Other pitfalls:** retraining on drifted or corrupted data (gate the data first), retraining so often that a bad week is learned, a recommender learning from what it chose to show (exposure feedback loop).
- **Mitigations:** an exploration holdout (approve or show a small random share, weight by 1 over its probability), reject inference at concept level (careful, it adds its own assumptions), recency weights, data gates and a champion-challenger check before swap.
- **Costs:** exploration means knowingly taking some risk, so it needs business sign-off and a cap.
- **Failure modes:** reporting the AUC on approved cases only; weights that are huge for a few cases; using the holdout for tuning and for evaluation.""",
example="""Policy rejects applicants whose bureau-like score is below a cutoff (30 percent). In the simulation, thin-file applicants behave the opposite way on a second feature. A model trained on approved cases gets measured AUC 0.774 on approved cases but true AUC 0.735 on all, and 0.467 inside the rejected region. With 916 exploration labels (5 percent of rejected) weighted by 20, true AUC is 0.814 and 0.803 in the rejected region. The measured AUC on approved cases barely changes (0.773), which is why it cannot tell you.""",
code=[("python", ["loop.py"])],
outnote="(real run, numpy 2.5.4, scikit-learn 1.9.1, seed 33; the data and the rejected-region behaviour are simulated by me, real data will not be so tidy)",
follow="""- **Why not just use reject inference?** It needs assumptions about rejected cases that you cannot check; an exploration holdout gives real labels.
- **How big should the holdout be?** Big enough to give stable labels in the rejected region, small enough for the risk budget; this is a business choice.""",
mistakes="""- Evaluating the new model only on cases the old model approved.
- Retraining automatically with no gate on the data.
- Weights applied to the holdout but not to the metric.
- Asking for exploration without a loss cap.""")

Q[34] = dict(
say="First stop the damage (roll back or use the fallback), then communicate, find the cause, and write a blameless post-mortem that names the trigger, the amplifier and the concealer, with numbers for time to detect and time to mitigate and action items with owners.",
explain="""- **Order:** detect, triage (how bad, who is affected, which decisions), mitigate (roll back, fallback rule, pause decisions), communicate (a named owner sends updates), find the root cause, then learn. Mitigation comes before understanding.
- **Blameless:** write about systems and decisions, not people. The question is why the system let it happen.
- **Trigger, amplifier, concealer:** trigger started it (unit change upstream), amplifier made it bigger (no input check, so bad rows flowed on), concealer hid it (only a dashboard, no alert, an average that moved slowly, labels days late).
- **Times:** time to notice (any human), time to detect (ML team), time to mitigate, time to resolve. A long gap before detection is usually a gap in monitoring or handoff, not in the fix.
- **Failure modes:** fixing the data but not the missing check; action items with no owner or date; a dashboard that nobody looks at counted as monitoring.""",
example="""Upstream switches income from rupees to thousands of rupees on 2 March 02:00. Approval rate falls; an ops analyst notices on 4 March (55 hours), the ML ticket opens a day later, the dashboard confirms 81 hours after the fault started, the fallback rule is on 0.8 hours after that. The log below is simulated; there is no real company incident behind it.""",
code=[("python", ["incident.py"]), ("markdown", ["postmortem_template.md"])],
outnote="(real run, pandas 3.1.0, seed not needed (fixed log); the timeline and the owners are invented for the exercise)",
follow="""- **Roll back or fix forward?** Roll back (or use the fallback) when it is quick and safe; fix forward only when rollback is not possible and the fix is simple.
- **How do you stop the next one?** Input checks at ingestion, alerts with owners and runbooks (Q27, Q30), contracts with upstream, and a drill.""",
mistakes="""- Naming a person as the cause.
- Counting time to detect from when the ticket opened.
- Action items like "be more careful".
- Closing the incident with no check that the new alert would really have fired.""")
