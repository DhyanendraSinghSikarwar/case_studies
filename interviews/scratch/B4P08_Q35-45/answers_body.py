ENV = "Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs)."

A[35] = """
**Say this first (1 line):** For embeddings I do not run a test per dimension; I ask "can a classifier tell reference from production?" (AUC near 0.5 means no, near 1 means yes), and I back it with centroid distance and cheap metadata drift like text length or image size.

**Then explain:**
- **Why not per-dimension tests:** a 768-dim embedding has no meaning per axis, and 768 KS tests give false alarms. Use one score for the whole vector.
- **Centroid distance:** distance between the mean embedding of reference and of today, scaled by the reference spread. Cheap, one number, good for a trend line. It misses shape changes where the mean stays put.
- **Domain classifier:** label reference 0 and production 1, cross-validate a simple model, read the AUC. About 0.5 is "cannot tell apart". Higher is "different", and the model's top features or misclassified rows show where.
- **Metadata drift:** text length, language mix, image width and height, file type, null rate. Boring but catches broken upstream pipelines the embedding hides (for example a resized image).
- **Failure modes:** a new embedding model version changes every vector (always compare same-version embeddings); small batches give noisy AUC; a flag tells you "different", not "worse", so pair it with a quality or label check. Prompt, retrieval and answer-quality monitoring for LLM systems is Book 2; this answer stops at the input side.

**Example:** 32-dim embeddings, 1000 rows each. Only 4 of the 32 dims are shifted. The per-dim shift is invisible by eye, but the domain AUC climbs from 0.505 (no shift) to 0.666 (shift 0.3) to 0.915 (shift 1.0). Text length (Poisson mean 40 to 55) is flagged by plain KS.

**Code:** (seeded; `python3 -I`)
""" + code(("py", ["q35_embeddings.py"])) + """

**Output (my run):** """ + ENV + """
""" + out(("", "out_q35_embeddings.txt")) + """

**Follow-ups:**
- *What if the domain classifier says AUC 0.9 but metrics are fine?* The shift may not touch what the model uses. Log it, check a labelled sample, do not auto-retrain.
- *Why cross-validate?* Scoring the classifier on its own training rows always looks great; AUC must be on held-out rows.
- *Distances in high dimensions?* Distances concentrate; prefer cosine or a PCA-reduced space, and keep the classifier as the main signal.

**Common mistakes:** per-dimension KS on every axis; mixing embeddings from two model versions; reading AUC on training rows; treating "drift" as "bad"; forgetting metadata checks.
"""

A[36] = """
**Say this first (1 line):** Per-feature tests look only at one column at a time, so they miss a change in how features relate; I add a domain classifier, a PCA reconstruction error and a pairwise-correlation diff, which are loud when the marginals are quiet.

**Then explain:**
- **The blind spot:** two features can each stay N(0,1) while their correlation flips from +0.8 to -0.8. Every KS test passes, the joint distribution is totally different.
- **Correlation diff:** compare the correlation matrix to the reference. Cheap, readable ("x0 and x1 now move opposite"), but only sees linear pairs.
- **PCA reconstruction error:** fit PCA on reference, reconstruct production with the same components, watch the error. Rising error means production sits off the old structure. Linear again.
- **Domain classifier:** any model that can separate the two windows. A tree model sees non-linear changes too. Most general, and the most expensive to keep running.
- **Choosing:** daily and cheap, correlation diff plus PCA error. When one fires, or on a weekly cadence, run the domain classifier. Per-feature KS stays on, for single-column faults.
- **What the loud ones cannot say:** which feature changed. All of them only say "the joint changed". To localise: look at the pairwise cell with the biggest diff, or the classifier's feature importance; neither is proof of a cause.
- **Failure mode:** with many features, correlation diffs multiply (p features give p(p-1)/2 pairs), so set the threshold from a bootstrap (Q38).

**Example:** 2000 rows each, reference corr +0.81, production -0.79. KS p-values 0.53 and 0.46 (quiet). Random-forest domain AUC 0.893, correlation difference 1.60, PCA(1) error 0.188 to 1.781. In a control with no change the AUC is 0.512, corr diff 0.002 and errors 0.197 vs 0.202.

**Code:** (seeded; `python3 -I`)
""" + code(("py", ["q36_multivariate.py"])) + """

**Output (my run):** """ + ENV + """
""" + out(("", "out_q36_multivariate.txt")) + """

**Follow-ups:**
- *Why a random forest and not logistic regression?* A linear model on (x0, x1) cannot separate a flipped correlation; a tree model can. Pick a classifier that matches the shapes you worry about.
- *Does the model care?* Check feature-pair interactions in the model; a flipped correlation hurts a model that relies on the pair, and may do nothing to one that does not.

**Common mistakes:** trusting green per-feature KS as "no drift"; running a linear domain classifier and calling the joint "fine"; expecting these detectors to name the culprit.
"""

A[37] = """
**Say this first (1 line):** CUSUM and Page-Hinkley keep a running sum of "how far above normal, minus an allowance", and alarm when the sum crosses a threshold; that finds a small, lasting rise in an error rate much faster than repeating a KS test on windows.

**Then explain:**
- **CUSUM:** `s = max(0, s + z - k)`; alarm when `s > h`. `k` is the drift allowance (ignore wobble smaller than about k sd), `h` is the threshold.
- **Page-Hinkley:** same idea with a running mean as reference: accumulate `z - mean - delta`, alarm when the sum rises `lam` above its running minimum.
- **ADWIN (concept only, not implemented here):** keeps a window that grows while data is stable and drops the old part when two sub-windows have different means. It adapts the window so you do not pick one.
- **The trade-off:** a low threshold finds changes sooner and fires on noise more; a high threshold is quiet and slow. The "average run length" between false alarms and the detection delay move in opposite directions.
- **Why not repeated KS:** each KS test uses a fixed window, tests again and again (more chances to false-alarm), and is slow for a slow shift; a cumulative sum uses every point since the change.
- **Failure modes:** parameters are in units of the baseline sd, so a wrong baseline mean or sd means wrong alarms; reset the sum after an alarm; for stream infrastructure see Part 9.

**Example:** baseline 0.10, sd 0.02, a +1 sd step (0.12) at t=300, 600 points, 200 seeds. `h=5` is too jumpy (94/200 noise-only runs alarm). `h=8` gives 5/200 false alarms and a median delay of 14 points; Page-Hinkley `lam=15` gives 0/200 false alarms with a median delay of 31.5.

**Code:** (seeded, numpy only; `python3 -I`)
""" + code(("py", ["q37_cusum_ph.py"])) + """

**Output (my run):** """ + ENV + """ Delay is measured only on runs that had not already alarmed before the step, so it is slightly flattering for the jumpy settings.
""" + out(("", "out_q37_cusum_ph.txt")) + """

**Follow-ups:**
- *How do you pick h?* Simulate noise-only streams (as above) to hit a target false-alarm rate, then read the delay you get.
- *Two-sided?* Run one CUSUM for up and one for down.
- *Seasonal metric?* De-trend or compare to the same weekday first, or the weekly cycle looks like drift.

**Common mistakes:** k and h copied from a blog without matching your units; never resetting after an alarm; using it on a metric whose baseline is not stable; claiming a delay number without reporting false alarms next to it.
"""

A[38] = """
**Say this first (1 line):** I do not use "PSI above 0.1"; I draw many clean batches of my real batch size from history, see what PSI or KS D looks like when nothing changed, and set the threshold at the level that gives me my target false-alarm rate.

**Then explain:**
- **Why a fixed number fails:** PSI on small batches is noisy. At n=200 a clean batch exceeds 0.1 about 3 percent of the time; at n=2000 or 20000 never. 0.1 is a rule of thumb from credit scoring, not a standard.
- **Method:** bootstrap batches of size n from the reference, compute the statistic each time, take the 95th or 99th percentile as threshold. That is the null distribution for this batch size.
- **Backtest:** replay past days and past incidents through the chosen threshold. Count false alarms on known-quiet days and hits on known incidents. Adjust the percentile, not the story.
- **Many features:** with 50 features at a 1 percent per-feature rate you expect at least one alarm on 39.5 percent of days. Use a stricter per-feature level (about 0.0002 for a 1 percent daily rate over 50 independent features), or alert on "how many features moved".
- **Seasonality:** build the reference from the same weekday or season, or the null distribution itself is too narrow and every Monday alarms.
- **Failure modes:** a null built from a reference that already contains drift; bootstrapping with replacement from a tiny reference; a high threshold that no longer catches a real 0.15 sigma shift (check power as well).

**Example:** n=200 gives a PSI null p99 of 0.1217; n=2000 gives 0.0111; n=20000 gives 0.0010. The same 0.1 means "almost the noise ceiling" at 200 and "huge" at 20000. At n=2000 a threshold of 0.0114 had 1.5 percent false alarms on fresh clean batches and caught a 0.15-sigma shift 99 percent of the time.

**Code:** (seeded, numpy and scipy; `python3 -I`)
""" + code(("py", ["q38_threshold_calibration.py"])) + """

**Output (my run):** """ + ENV + """ (The batches are drawn from the same 50000-row history that is the reference, so the null is slightly narrower than with fully independent data.)
""" + out(("", "out_q38_threshold_calibration.txt")) + """

**Follow-ups:**
- *Why PSI and KS both?* PSI shrinks with n (noise), KS D shrinks too; a p-value alone grows sensitive at large n, so I also set a minimum effect size (Evidently's blog says the same for KS at large n; check current docs).
- *What target rate?* Whatever the on-call can bear: alert fatigue is the real cost, so tie it to one false page per feature-month, not 5 percent.

**Common mistakes:** one threshold for every batch size; quoting 0.1 and 0.25 as industry standards; calibrating on a reference that includes the incident; checking false alarms but never power.
"""

A[39] = """
**Say this first (1 line):** At scale I do not store or test every row; I keep small mergeable profiles (histograms and counts, whylogs-style) per day, merge them for longer windows, and compare profiles to the reference, which costs almost nothing compared with raw data.

**Then explain:**
- **Sampling:** a random sample is fine for aggregate drift; keep every flagged or rare event (fraud, errors) at 100 percent.
- **Sketches and profiles:** a profile stores counts, min/max, distribution sketches per column. Profiles are mergeable: day1 + day2 + day3 = a 3-day profile without the rows.
- **Pre-aggregated histograms:** if you already have bucket counts in your warehouse, compute PSI from those; no raw pull.
- **Windowed jobs:** schedule per model per window; cost scales as models x features x windows, so tier models (critical ones get more features and hourly windows).
- **Failure modes:** sketches are approximate; a profile cannot be re-sliced by a column you did not profile; high-cardinality columns blow up size; string columns failed here (see below).

**Example:** three daily batches of 50000 rows (day 3 has `amount` shifted up), compared to a 50000-row reference. Day 1 shows no drift on any column; day 3 shows drift on `amount` only (statistic 0.237); the merged 3-day profile shows `amount` drift (0.079) diluted by two clean days. Merged profile file about 61.8 KB against 3.6 MB of in-memory dataframes (58 times smaller, and it does not grow with rows).

**Code:** (seeded; whylogs env with `[viz]`; `python3 -I`)
""" + code(("py", ["q39_whylogs.py"])) + """

**Output (my run):** whylogs 1.6.4, pandas 3.1.0, numpy 2.5.4 in /tmp/claude-0/b8p08/e_whylogs. Drift scores come from `calculate_drift_scores` (needs `whylogs[viz]`); the number printed is the score for the KS algorithm, and the DRIFT or NO_DRIFT label uses whylogs' default threshold (check current docs). I did not rerun the string column case; a string column raised `AttributeError: np.unicode_ was removed in the NumPy 2.0 release` here, so I used numeric columns only. WhyLabs or any SaaS storage: not executed (no account or network service); the profile file above is the local equivalent.
""" + out(("", "out_q39_whylogs.txt")) + """

**Follow-ups:**
- *Are merged profiles exact?* Counts, min, max, mean are exact. Quantile or distribution sketches carry a small error.
- *What do you lose?* Row-level debugging; keep a small sampled raw store next to the profiles.
- *Cost lever?* Fewer features, a longer window, a lower tier for low-risk models.

**Common mistakes:** logging every row to the warehouse "just in case"; profiling only the averages (distribution shape lost); forgetting that a merged window hides a one-day spike; assuming a library works on a new numpy without running it.
"""

A[40] = """
**Say this first (1 line):** When the metric drops and every drift test is green, I suspect the relationship between inputs and the label changed (concept change), a label or join bug, so I compare feature importance on a recent labelled window against the reference; the model's key feature stops mattering.

**Then explain:**
- **Drift tests only see inputs (and scores).** If the inputs look the same but the label's meaning moved, they stay quiet. That is the classic case.
- **Permutation importance:** on a labelled recent window, shuffle one feature and measure the metric drop. A big feature that used to matter and now matters 0 is a strong sign. Needs labels, so it lags.
- **Mean absolute contribution** (linear coefficients times values, or tree SHAP values; check your library's docs): label-free, can run daily; a shift in contribution means the inputs push the score differently.
- **Cases drift tests miss:** concept change; a changed label definition (a new chargeback rule); a join bug (labels attached to the wrong rows, so everything looks fine on inputs); feedback loops.
- **Debugging order when metric is down and drift is green:** (1) is the metric itself right (label definition, cohort, time window)? (2) label and join integrity on a sample; (3) data quality and schema; (4) score distribution and thresholds; (5) importance and slice analysis; (6) then conclude concept change and retrain on new labels.
- **Failure mode:** importance on a tiny window is noisy; correlated features share importance; importance shift is a clue, not proof.

**Example:** f0 drives the label before, f1 after (marginals never change). AUC drops 0.933 to 0.511; KS p-values 0.52, 0.58, 0.75 (quiet); mean score 0.498 vs 0.500 (quiet). Permutation importance of f0 falls 0.413 to -0.001 while f1 stays near 0 (the model never learned it).

**Code:** (seeded; `python3 -I`)
""" + code(("py", ["q40_attribution.py"])) + """

**Output (my run):** """ + ENV + """
""" + out(("", "out_q40_attribution.txt")) + """

**Follow-ups:**
- *So what is the fix?* New labels under the new rule, retrain, validate (Q41 gates). A threshold tweak does not repair a concept change.
- *No labels yet?* Use contribution shift plus proxy labels, or an estimate like NannyML's CBPE (concept only here).

**Common mistakes:** "no drift so no problem"; blaming the model before checking the label definition; trusting a feature-importance diff on a few hundred rows.
"""

A[41] = """
**Say this first (1 line):** For a regulated lender I treat the model as a controlled asset: it is in an inventory, validated independently, monitored against thresholds that trigger a human review, changed only through change control, and every decision is traceable and explainable.

**Then explain:**
- **Model inventory:** every model has an owner, risk tier, intended use and version. If it is not in the inventory, it should not score.
- **Validation:** independent validation before go-live and periodic revalidation; monitoring feeds that, it does not replace it.
- **Thresholds that trigger review:** warn then breach levels (input PSI, score PSI, matured-cohort Gini or KS drop, approval-rate change, data quality). A breach opens a review, not an automatic retrain.
- **Challenger:** run a shadow challenger; promotion needs validation, approval and a rollback plan.
- **Audit trail:** log request id, model version, features (hashed or referenced), score, decision, reason codes, timestamp; retention set by compliance.
- **Explainability on request:** reason codes from contributions, reproducible for an old decision with the logged version.
- **Change control:** retrain request with ticket, validation report, approver who is not the author; rollback to the previous registered version.
- **Failure modes:** labels (defaults) mature slowly; a policy YAML nobody enforces; thresholds copied, not calibrated (Q38).
- **Regulator:** I did not look up RBI or other regulator guidance, so none is quoted. In the interview I would say "my policy follows whatever the bank's model-risk framework and current regulator guidance require; I would check with compliance".

**Example (whiteboard):** inventory -> validate -> deploy v3 -> monthly monitor -> warn: notify owner; breach: review meeting -> challenger in shadow -> committee approves -> versioned rollout with rollback. Next to it, a decision log row per application.

**Code:** (placeholders, not real policy numbers; validated with pyyaml)
""" + code(("yaml", ["q41_policy.yaml"]), ("py", ["q41_validate.py"])) + """

**Output (my run):** PyYAML 6.0.3. Structural validation only (sections present, thresholds numeric, warn < breach where both exist, breach actions are reviews or blocks). Actual regulator rules, audit-retention length and any bank tooling: not executed / not looked up.
""" + out(("", "out_q41.txt")) + """

**Follow-ups:**
- *Who approves a retrain?* Someone other than the author, per the policy (validation plus committee).
- *Why shadow challenger?* It scores live traffic without affecting decisions, so you compare before promotion.
- *Fairness?* Add segment-level checks to the policy (concept in the YAML for Q43; regulator expectations not looked up).

**Common mistakes:** automatic retraining with no validation; no model inventory; logging features without a version; quoting regulator rules from memory.
"""

A[42] = """
**Say this first (1 line):** Most classic monitoring carries over (input quality, schema, latency, cost, errors, feedback, privacy, incidents); what does not is quality judgement like hallucination, groundedness, prompt-injection and retrieval quality, which Book 2 and a later LLMOps part own.

**Then explain:**
- **Carries over:** request validity and schema, latency percentiles, error and timeout rate, token or cost per call, response length, drift on input categories, thumbs or other feedback with a delay, privacy of logs, an incident process.
- **Does not carry over cleanly:** there is no single label; "correct" is fuzzy. Hallucination, groundedness, injection and retrieval quality need their own evaluators (Book 2).
- **Log metadata first:** store length, latency, a hash of the prompt and feedback; store raw text only if policy allows, masked.
- **Rolling summary:** a fixed window of recent calls gives p50, p95, error rate, mean length and thumbs-up rate; compare to a baseline.
- **Failure modes:** feedback is sparse and biased (only unhappy users click); a rolling window over a quiet hour is noisy; changing the provider's model silently moves everything.

**Example:** 80 calls to a stub, window of 50. At call 50: error 0.06, p50 266 ms, p95 390 ms. At call 80 (a simulated slowdown): p50 362, p95 853, error 0.08, thumbs-up 0.812 on 16 votes (too few to read much into).

**Code:** (stub model, seeded; `python3 -I`). The real provider call is not executed; latencies are simulated numbers.
""" + code(("py", ["q42_llm_logger.py"])) + """

**Output (my run):** """ + ENV + """
""" + out(("", "out_q42_llm_logger.txt")) + """

**Follow-ups:**
- *Is the thumbs-up rate a quality metric?* A weak one; use it as a trend, and sample for human review.
- *What do you log about the prompt?* Length, hash, category; raw text only under a masking and retention policy.

**Common mistakes:** logging full prompts with personal data; treating latency as quality; reusing a classification-accuracy dashboard for generation; claiming a stub run proves anything about a real provider.
"""

A[43] = """
**Say this first (1 line):** Log every scored event with a feature snapshot, gate the data first, watch feature and score drift in real time as early warnings, measure true performance only on matured cohorts once chargebacks arrive, and use tiered alerts so only data-quality or score-collapse issues page someone.

**Then explain (whiteboard in order):**
- **Logging:** event id, timestamp, model version, feature snapshot reference, score, decision; tokenised card data; sampled raw rows plus all flagged.
- **Data-quality gates:** null rate, schema, freshness, volume vs same weekday. A failed gate pages the data owner and blocks drift alerts (no point testing garbage).
- **Drift:** daily feature drift with calibrated thresholds (Q38), hourly score drift plus a score-band pile-up check (Q44). These are early warnings, not proof of damage.
- **Delayed labels:** chargebacks arrive 30 to 90 days late. Compute recall and precision on matured cohorts (events old enough that most labels exist), and mark the share of labels received. Early proxies: analyst feedback labels, alert rate, score-based estimates.
- **Alert tiers:** page (gate failed, score collapse), ticket (persistent drift, matured-cohort drop), info (one-day feature drift).
- **Retraining:** hybrid (monthly schedule plus a trigger confirmed by labels); offline backtest, shadow challenger, approval; rollback to the previous version.
- **Fairness and privacy:** false-positive-rate gaps across segments monthly; minimise stored PII; access-controlled logs.
- **On-call:** a runbook per page; the model owner is on a rota; false-alert reviews monthly.
- **Concept only (not run):** fairness checks, shadow challenger, analyst labels, on-call routing. Run here: the YAML validation and the matured-cohort simulation.

**Example:** in the simulation real recall drops from 0.80 to 0.60 at day 120. By day 199, the day-110 cohort is 98 percent labelled and shows 0.80; day 130 is 68 percent labelled and shows 0.57; day 150 is only 32 percent labelled. The drop is visible only as old cohorts mature, which is why the proxies and drift stay as early warnings.

**Code:** (YAML spec with placeholders; validation and cohort simulation, seeded)
""" + code(("yaml", ["q43_fraud_spec.yaml"]), ("py", ["q43_validate.py", "q43_cohort.py"])) + """

**Output (my run):** PyYAML 6.0.3 for validation, numpy 2.5.4 for the simulation. Kafka, a feature store, the bank's alerting stack and on-call tooling: not executed. The simulation assumes label delay is independent of whether the fraud was caught.
""" + out(("validation", "out_q43_validate.txt"), ("matured cohorts", "out_q43_cohort.txt")) + """

**Follow-ups:**
- *Why not wait for chargebacks?* You would learn about a bad model 3 months late; hence drift and proxies as early warning.
- *Bias in analyst labels?* Analysts only review flagged cases, so labels are biased toward what the model already flags; keep a random review sample.
- *Millions of events?* Profiles and sketches (Q39), tiered features.

**Common mistakes:** computing recall on the latest week (labels missing); paging on any drift; one retraining trigger with no validation gate; forgetting that blocked transactions get no chargeback label.
"""

A[44] = """
**Say this first (1 line):** Adversaries and the model itself change the data, so I separate organic drift from adaptation: watch the score bands just below the decision threshold for a pile-up, filter internal and test traffic before drift tests, and read a rising score in a blocked segment as possibly the model working.

**Then explain:**
- **Adaptive attackers:** they probe, then tune inputs to land just under a threshold. Marginal feature drift is mild; the signature is a pile-up in the band below the line.
- **Performative drift:** decisions change behaviour (a declined user retries with different details), so the data you see after launch depends on the model. The old reference stops being "normal".
- **Bot, test and internal traffic:** synthetic or QA traffic can make drift tests fire or mask real shifts; tag it (header, IP list, test account) and filter it before computing drift.
- **Blocked segment:** if the blocked group's average score rises, that may be the model correctly catching more; do not "fix" it.
- **Detector:** compare mass just below the threshold with the reference band and with the band just above it; alert when the ratio is high and the count is large enough.
- **Failure modes:** label feedback is biased (you only see outcomes for approved cases); a retrain on attacker-shaped data teaches the model the attacker's pattern; threshold is public knowledge in some systems.

**Example:** threshold 0.80; 15 percent of week-8 traffic is an attacker with feature value 1.25 to 1.50 (score about 0.65 to 0.76). Feature KS D 0.134. The block rate falls from 6.05 to 5.24 percent. The band 0.70 to 0.80 holds 3.26 percent of traffic at week 0 and 12.2 percent at week 8 (ratio 3.74, 4.79 times the band above); the control run shows ratio 0.93 and no alert.

**Code:** (seeded, numpy and scipy; `python3 -I`)
""" + code(("py", ["q44_adaptive.py"])) + """

**Output (my run):** """ + ENV + """ The traffic filter was not simulated; it is a rule applied before the test.
""" + out(("", "out_q44_adaptive.txt")) + """

**Follow-ups:**
- *Do you tell the model team or the fraud ops?* Both: the model team for threshold or feature changes, ops for the attacker segment.
- *Randomise the threshold?* A defensive idea (check your risk team); it makes probing harder.

**Common mistakes:** retraining on traffic that includes the attacker's tuned samples without review; including QA traffic in the baseline; treating every score rise as a model failure.
"""

A[45] = """
**Say this first (1 line):** I test monitors like code: inject known faults into a clean batch, assert that the right monitor fires and the others stay quiet, measure detection and false-alarm rate over many seeds, and replay logged history through a new monitor version before enabling its alerts.

**Then explain:**
- **Fault injection helper:** one function per fault (null spike, unit change, mean shift, dropped partition) applied to a clean batch.
- **Detection matrix:** rows are faults, columns are monitors, cells are the fraction of seeds where it fired. You want a clean diagonal-like pattern and an all-zero "no fault" row.
- **Many seeds:** one lucky seed proves nothing; 30 to 200 seeds give a rate. Assert rates (at least 95 percent detect, at most 5 percent false alarm).
- **Backfill replay:** run the new monitor over past logged days, count alerts, compare with known incidents, then enable paging (concept here; the logic is the same function in a loop).
- **What the first run taught me:** the volume monitor (min ratio 0.7) missed a dropped region because 1 of 4 regions is only 25 percent of rows (75 percent remain). My first test failed (0 of 30 detections). I added a category-presence monitor and left a test that documents the volume monitor's limit.
- **Failure modes:** tests with fixed seeds that hide flakiness; thresholds tuned until the tests pass; asserting only "something fired".

**Example:** the matrix below. `none` row all 0.00 (no false alarms in 200 seeds). Unit change fires `drift` and `range`; mean shift only `drift`; null spike only `null`; dropped partition only `category`.

**Code:** (three files in `code/q45/`: monitors, tests, matrix script; pytest basics are Part 1)
""" + code(("py", ["q45/monitors.py", "q45/test_monitors.py", "q45/matrix.py"])) + """

**Output (my run):** """ + ENV + """ First pytest run (before adding the category monitor):
""" + out(("", "q45/first_run.txt")) + """After the fix:
""" + out(("pytest", "q45/out_pytest.txt"), ("matrix.py", "q45/matrix_out.txt")) + """

**Follow-ups:**
- *How do you avoid tuning to the tests?* Keep a held-out set of historic incidents and faults the thresholds never saw.
- *Which fault is the hardest?* Slow, small shifts; test with graded fault sizes and read power, not one size.

**Common mistakes:** testing only the happy path; asserting on one seed; no "no fault" row; enabling a new monitor's pager without a backfill replay.
"""
